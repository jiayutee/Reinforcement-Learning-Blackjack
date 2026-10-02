// Optional integration gate. Requires Playwright and Chromium; see README.md here.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const {spawn}=require('node:child_process');
const fs=require('node:fs/promises');
const os=require('node:os');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
async function start(policy){
 const child=spawn(process.env.PYTHON||'python3',['-m','foundations.local_game','--port','0',...(policy?['--policy',policy]:[])],{cwd:root,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'},stdio:['ignore','pipe','pipe']});
 try{
  const url=await new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>reject(new Error('Server startup timed out')),10000);
   let output='',errors='';
   child.stderr.on('data',d=>errors+=d);
   child.on('error',e=>{clearTimeout(timer);reject(e)});
   child.on('exit',code=>{clearTimeout(timer);reject(new Error(`Server exited ${code}: ${errors}`))});
   child.stdout.on('data',d=>{output+=d;const match=output.match(/http:\/\/127\.0\.0\.1:\d+/);if(match){clearTimeout(timer);resolve(match[0])}});
  });return {child,url};
 }catch(e){child.kill();throw e}
}
async function stop(child){if(child.exitCode!==null)return;await new Promise(resolve=>{child.once('exit',resolve);child.kill('SIGTERM')})}
(async()=>{
 const dir=await fs.mkdtemp(path.join(os.tmpdir(),'blackjack-browser-'));
 let browser;
 try{
  const fixture={schema_version:1,artifact_type:'q_learning_control',rules:'foundations-v1: replacement draws, S17, no natural bonus, hit/stand',gamma:1,training:{episodes:100,environment_seed:7,epsilon:0.1,alpha:0.1},states:[{observation:[9,7,false],greedy_action:1,actions:[{action:0,value:-0.4,visits:10},{action:1,value:0.2,visits:20}]}]};
  const known=path.join(dir,'known.json'),missing=path.join(dir,'missing.json');
  await fs.writeFile(known,JSON.stringify(fixture));
  await fs.writeFile(missing,JSON.stringify({...fixture,states:[]}));
  browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  for(const [name,policy] of [['manual',null],['known',known],['missing',missing]]){
   const {child,url}=await start(policy);let page;
   try{
    page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
    await page.goto(url);await page.waitForFunction(()=>!document.querySelector('#deal').disabled);
    if(name==='manual')assert.match(await page.locator('#advice').textContent(),/No advisor loaded/);
    await page.click('#deal');await page.waitForFunction(()=>!document.querySelector('#hit').disabled);
    const state=await(await page.request.get(url+'/state')).json();
    assert.deepEqual(state.hand.dealer_cards,[7,null]);assert.equal(state.hand.dealer_total,null);
    if(name==='known'){assert.equal(state.advice.action,1);assert.match(await page.locator('#advice').textContent(),/Estimated choice: Hit/)}
    if(name==='missing'){assert.equal(state.advice.action,null);assert.match(await page.locator('#advice').textContent(),/No recommendation/)}
    await page.click('#refresh');await page.waitForFunction(()=>!document.querySelector('#refresh').disabled);
    assert.deepEqual(await(await page.request.get(url+'/state')).json(),state);
    // Replay the old revision after an accepted hit: must reject without mutation.
    await page.click('#hit');await page.waitForFunction(()=>document.querySelector('#player-total').textContent.includes('20'));
    const after=await(await page.request.get(url+'/state')).json();
    const token=(await page.content()).match(/'X-Game-Token':'([^']+)'/)[1];
    const stale=await page.request.post(url+'/command',{headers:{Origin:url,'X-Game-Token':token},data:{command:'hit',revision:1}});
    assert.equal(stale.status(),409);assert.deepEqual(await(await page.request.get(url+'/state')).json(),after);
    assert.equal((await page.request.post(url+'/command',{data:{command:'stand',revision:2}})).status(),403);
    await page.locator('#stand').focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('You win'));
    assert.equal(await page.locator('#dealer .hidden').count(),0);assert.equal(await page.locator('#hit').isDisabled(),true);
    const terminal=await(await page.request.get(url+'/state')).json();assert.equal(terminal.advice,null);
    await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    assert.deepEqual(errors,[]);console.log(`PASS ${name}: complete hand, evidence state, hidden card, refresh, stale/unauthorized requests, keyboard, mobile`);
   }finally{if(page)await page.close();await stop(child)}
  }
 }finally{if(browser)await browser.close();await fs.rm(dir,{recursive:true,force:true})}
})().catch(error=>{console.error(error);process.exitCode=1});

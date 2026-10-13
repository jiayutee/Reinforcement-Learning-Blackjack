const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const {spawn}=require('node:child_process');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
async function start(seed=7){
 const child=spawn(process.env.PYTHON||'python3',['-m','public_game.local_game','--port','0','--seed',String(seed)],{cwd:root,env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'},stdio:['ignore','pipe','pipe']});
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
 let browser,child;
 try{
  const server=await start();child=server.child;const url=server.url;
  browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(url);await page.waitForFunction(()=>document.querySelector('#state').textContent.includes('"ready"'));
  await page.fill('#wager','0');await page.click('[data-action="deal"]');
  assert.match(await page.locator('#status').textContent(),/positive whole-chip/);
  assert.equal((await(await page.request.get(url+'/state')).json()).revision,0);
  await page.fill('#wager','10');await page.click('[data-action="deal"]');
  await page.waitForFunction(()=>document.querySelector('#state').textContent.includes('"player_turn"'));
  const active=JSON.parse(await page.locator('#state').textContent());assert.equal(active.dealer[1],null);
  assert.equal(await page.locator('[data-action="deal"]').isDisabled(),true);
  await page.click('#refresh');await page.waitForFunction(()=>!document.querySelector('#refresh').disabled);
  assert.deepEqual(JSON.parse(await page.locator('#state').textContent()),active);
  await page.locator('[data-action="stand"]').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>document.querySelector('#state').textContent.includes('"settled"'));
  const done=JSON.parse(await page.locator('#state').textContent());assert.equal(done.profit,-20);assert.notEqual(done.dealer[1],null);
  assert.equal(await page.locator('[data-action="hit"]').isDisabled(),true);
  await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  assert.deepEqual(errors,[]);
  console.log('PASS public inspector: wager validation, deal, concealment, refresh, keyboard stand, settlement, mobile width, no JS errors');
 }finally{if(browser)await browser.close();if(child)await stop(child)}
})().catch(error=>{console.error(error);process.exitCode=1});

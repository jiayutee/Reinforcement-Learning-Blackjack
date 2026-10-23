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
  await page.addInitScript(()=>{window.audioStarts=0;const original=AudioContext.prototype.createOscillator;AudioContext.prototype.createOscillator=function(...args){window.audioStarts++;return original.apply(this,args)};});
  await page.goto(url);await page.waitForFunction(()=>document.querySelector('#state').textContent.includes('"ready"'));
  assert.equal(await page.getByRole('main').count(),1);
  assert.equal(await page.getByRole('group',{name:'Hand actions'}).count(),1);
  assert.equal(await page.getByRole('group',{name:'Sound settings'}).count(),1);
  assert.equal(await page.locator('[data-wager]').count(),4);
  assert.equal(await page.locator('#wager').isDisabled(),false);
  const affordability=await page.evaluate(()=>{const saved=state;state={...state,balance:20};render();const disabled=Array.from(document.querySelectorAll('[data-wager]'),button=>button.disabled);const input=document.querySelector('#wager');const deal=document.querySelector('[data-action="deal"]');input.value='10';syncWagerButtons();const exactLimit={dealDisabled:deal.disabled,invalid:input.getAttribute('aria-invalid')};input.value='11';syncWagerButtons();const custom={dealDisabled:deal.disabled,invalid:input.getAttribute('aria-invalid')};input.value='10';state=saved;render();return {disabled,exactLimit,custom};});
  assert.deepEqual(affordability,{disabled:[false,false,true,true],exactLimit:{dealDisabled:false,invalid:'false'},custom:{dealDisabled:true,invalid:'true'}});
  assert.equal(await page.locator('#wager').getAttribute('aria-describedby'),'wager-hint');
  assert.equal(await page.locator('[data-wager="10"]').getAttribute('aria-pressed'),'true');
  await page.locator('[data-wager="25"]').focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#wager').inputValue(),'25');
  assert.equal(await page.locator('[data-wager="25"]').getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator('[data-wager="10"]').getAttribute('aria-pressed'),'false');
  assert.equal((await(await page.request.get(url+'/state')).json()).revision,0);
  await page.fill('#wager','10');assert.equal(await page.locator('[data-wager="10"]').getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator('#rules').getAttribute('open'),null);
  await page.locator('#rules summary').focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#rules').evaluate(el=>el.open),true);
  const rulesText=await page.locator('#rules').textContent();
  for(const phrase of ['Six-deck shoe','soft 17','3:2','equal naturals push','four hands','cannot be resplit','Insurance and surrender are not offered'])assert.ok(rulesText.includes(phrase),`missing rule text: ${phrase}`);
  await page.keyboard.press('Space');assert.equal(await page.locator('#rules').evaluate(el=>el.open),false);
  assert.equal(await page.locator('#status').textContent(),'Round ready. Enter a wager and choose Deal.');
  assert.equal(await page.evaluate(()=>window.audioStarts),0);assert.equal(await page.locator('#sound-toggle').getAttribute('aria-pressed'),'false');
  await page.click('#sound-toggle');assert.equal(await page.locator('#sound-toggle').getAttribute('aria-pressed'),'true');
  await page.locator('#sound-volume').evaluate(el=>{el.value='0.35';el.dispatchEvent(new Event('input',{bubbles:true}))});assert.equal(await page.locator('#sound-volume').inputValue(),'0.35');
  await page.fill('#wager','0');
  assert.equal(await page.locator('#wager').getAttribute('aria-invalid'),'true');
  assert.equal(await page.locator('[data-action="deal"]').isDisabled(),true);
  assert.equal(await page.locator('[data-wager][aria-pressed="true"]').count(),0);
  assert.equal((await(await page.request.get(url+'/state')).json()).revision,0);assert.equal(await page.evaluate(()=>window.audioStarts),0);
  await page.fill('#wager','10');await page.click('[data-action="deal"]');
  await page.waitForFunction(()=>document.querySelector('#state').textContent.includes('"player_turn"'));
  assert.equal(await page.locator('#wager').isDisabled(),true);
  assert.equal(await page.locator('[data-wager]:disabled').count(),4);
  assert.equal(await page.evaluate(()=>window.audioStarts),1);
  assert.match(await page.locator('#status').textContent(),/Hand 1\. Hard total 18\. Dealer shows .+\. Available actions: hit, stand, double\./);
  const active=JSON.parse(await page.locator('#state').textContent());assert.equal(active.dealer[1],null);assert.match(await page.locator('.hand h3').textContent(),/Hard 18/);assert.equal(await page.locator('#dealer-title').textContent(),'Dealer');
  assert.equal(await page.locator('#dealer .back').count(),1);assert.equal(await page.locator('.hand.active').count(),1);assert.equal(await page.locator('#hands .card').count(),2);
  assert.equal(await page.locator('[data-action="deal"]').isDisabled(),true);
  await page.click('#refresh');await page.waitForFunction(()=>!document.querySelector('#refresh').disabled);
  assert.deepEqual(JSON.parse(await page.locator('#state').textContent()),active);assert.equal(await page.locator('#status').textContent(),'State refreshed.');assert.equal(await page.evaluate(()=>window.audioStarts),1);
  await page.locator('[data-action="stand"]').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>document.querySelector('#state').textContent.includes('"settled"'));
  const done=JSON.parse(await page.locator('#state').textContent());assert.equal(done.profit,-20);assert.notEqual(done.dealer[1],null);assert.equal(await page.locator('#dealer-title').textContent(),'Dealer · 20');
  assert.equal(await page.locator('#wager').isDisabled(),false);
  assert.equal(await page.locator('#status').textContent(),'Round complete. You lost. Net profit: -10 chips.');
  assert.equal(await page.locator('#dealer .back').count(),0);assert.equal(await page.locator('.hand.active').count(),0);assert.match(await page.locator('#summary').textContent(),/Round profit: -10 chips/);
  assert.equal(await page.locator('[data-action="hit"]').isDisabled(),true);
  assert.equal(await page.evaluate(()=>window.audioStarts),3); // deal plus two-note loss cue
  await page.click('#sound-toggle');assert.equal(await page.locator('#sound-toggle').getAttribute('aria-pressed'),'false');
  const mutedStarts=await page.evaluate(()=>window.audioStarts),revision=done.revision;
  await page.click('[data-action="deal"]');await page.waitForFunction(r=>JSON.parse(document.querySelector('#state').textContent).revision===r+1,revision);
  assert.equal(await page.evaluate(()=>window.audioStarts),mutedStarts);
  await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  assert.deepEqual(errors,[]);
  console.log('PASS public inspector: wager validation, opt-in sound/mute, deal cues, refresh silence, keyboard stand/settlement, mobile width, no JS errors');
  await page.close();await stop(child);child=null;
  const splitServer=await start(19);child=splitServer.child;
  const splitPage=await browser.newPage();const splitErrors=[];splitPage.on('pageerror',e=>splitErrors.push(e.message));
  await splitPage.goto(splitServer.url);
  await splitPage.waitForFunction(()=>document.querySelector('#state').textContent.includes('"ready"'));
  async function action(name,revision){await splitPage.click('[data-action="'+name+'"]');await splitPage.waitForFunction(r=>JSON.parse(document.querySelector('#state').textContent).revision===r,revision);}
  await action('deal',1);assert.equal(await splitPage.locator('[data-action="split"]').isDisabled(),false);
  await action('split',2);assert.equal(await splitPage.locator('.hand').count(),2);
  assert.match(await splitPage.locator('.hand.active h3').textContent(),/Hand 1/);
  if(process.env.SCREENSHOT_DIR){await splitPage.screenshot({path:path.join(process.env.SCREENSHOT_DIR,'public-desktop.png')});await splitPage.setViewportSize({width:390,height:844});await splitPage.screenshot({path:path.join(process.env.SCREENSHOT_DIR,'public-mobile.png')});}
  await action('double',3);assert.match(await splitPage.locator('.hand.active h3').textContent(),/Hand 2/);
  assert.match(await splitPage.locator('#status').textContent(),/Hand 2\. Hard total .+\. Dealer shows .+\. Available actions: hit, stand, double\./);
  assert.match(await splitPage.locator('.hand h3').first().textContent(),/20 chips/);
  assert.equal(await splitPage.locator('#dealer .back').count(),1);
  assert.doesNotMatch(await splitPage.locator('#summary').textContent(),/Round profit/);
  await action('stand',4);
  assert.equal(await splitPage.locator('.hand').count(),2);assert.equal(await splitPage.locator('.hand.active').count(),0);
  assert.equal(await splitPage.locator('#dealer .back').count(),0);
  assert.match(await splitPage.locator('#summary').textContent(),/Round profit: -30 chips/);
  assert.equal(await splitPage.locator('#status').textContent(),'Round complete. You lost. Net profit: -30 chips.');
  await splitPage.setViewportSize({width:390,height:844});assert.equal(await splitPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  assert.deepEqual(splitErrors,[]);
  console.log('PASS public split: two hands, double stake, active hand advance, concealed pending result, aggregate loss, mobile width');
  await splitPage.close();await stop(child);child=null;
  const aceServer=await start(4);child=aceServer.child;
  const acePage=await browser.newPage();const aceErrors=[];acePage.on('pageerror',e=>aceErrors.push(e.message));
  await acePage.goto(aceServer.url);await acePage.waitForFunction(()=>document.querySelector('#state').textContent.includes('"ready"'));
  await acePage.click('[data-action="deal"]');await acePage.waitForFunction(()=>JSON.parse(document.querySelector('#state').textContent).revision===1);
  assert.match(await acePage.locator('.hand h3').textContent(),/Soft 15/);
  await acePage.click('[data-action="hit"]');await acePage.waitForFunction(()=>JSON.parse(document.querySelector('#state').textContent).revision===2);
  assert.match(await acePage.locator('.hand h3').textContent(),/Hard 15/);
  assert.match(await acePage.locator('#status').textContent(),/Hand 1\. Hard total 15\. Dealer shows .+\. Available actions: hit, stand\./);
  assert.equal(await acePage.locator('#dealer-title').textContent(),'Dealer');
  assert.equal(await acePage.locator('#dealer .back').count(),1);
  assert.equal(await acePage.locator('[data-action="double"]').isDisabled(),true);
  const before=JSON.parse(await acePage.locator('#state').textContent());
  await acePage.reload();await acePage.waitForFunction(revision=>JSON.parse(document.querySelector('#state').textContent).revision===revision,before.revision);
  assert.match(await acePage.locator('#status').textContent(),/Hand 1\. Hard total 15\. Dealer shows .+\. Available actions: hit, stand\./);
  await acePage.click('#refresh');await acePage.waitForFunction(()=>!document.querySelector('#refresh').disabled);
  assert.deepEqual(JSON.parse(await acePage.locator('#state').textContent()),before);assert.equal(await acePage.locator('#status').textContent(),'State refreshed.');
  assert.deepEqual(aceErrors,[]);
  console.log('PASS public ace: soft15 to hard15, dealer concealed, post-hit double disabled, refresh unchanged');
 }finally{if(browser)await browser.close();if(child)await stop(child)}
})().catch(error=>{console.error(error);process.exitCode=1});

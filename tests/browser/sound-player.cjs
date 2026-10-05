// Deterministic control tests with a simulated DOM/audio backend; not a listening test.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../../foundations/sound-player.js'),'utf8');
function setup({stored=null,unsupported=false,storageBlocked=false,resumeFails=false}={}){
 const elements={};for(const id of ['sound-toggle','sound-volume','sound-status'])elements[id]={value:'',textContent:'',attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.events[k]=f}};
 const metrics={created:0,starts:0,stops:0};
 class Audio{
  constructor(){metrics.created++;this.state='suspended';this.currentTime=0;this.destination={}}
  async resume(){if(resumeFails)throw new Error('blocked');this.state='running'}
  createOscillator(){return {frequency:{value:0},connect(){},disconnect(){},start(){metrics.starts++},stop(){metrics.stops++}}}
  createGain(){return {gain:{setValueAtTime(){},linearRampToValueAtTime(){}},connect(){},disconnect(){}}}
 }
 let value=stored;const window={};if(!unsupported)window.AudioContext=Audio;
 const sandbox={window,document:{getElementById:id=>elements[id]},localStorage:{getItem(){if(storageBlocked)throw new Error('denied');return value},setItem(k,v){if(storageBlocked)throw new Error('denied');value=v}}};
 vm.runInNewContext(source,sandbox);
 return {elements,metrics,play:cue=>window.BlackjackSoundPlayer.play(cue),click:()=>elements['sound-toggle'].events.click(),volume(v){elements['sound-volume'].value=String(v);elements['sound-volume'].events.input()},saved:()=>value};
}
(async()=>{
 let h=setup();h.play('win');assert.equal(h.metrics.created,0);assert.equal(h.metrics.starts,0);
 await h.click();h.volume(0);h.play('win');assert.equal(h.metrics.starts,0);
 h.volume(0.35);h.play('win');assert.equal(h.metrics.starts,3);
 const persisted=h.saved();assert.deepEqual(JSON.parse(persisted),{enabled:true,volume:0.35});
 let reload=setup({stored:persisted});assert.equal(reload.elements['sound-volume'].value,'0.35');assert.equal(reload.metrics.created,0);reload.play('hit');assert.equal(reload.metrics.starts,0);assert.match(reload.elements['sound-status'].textContent,/activate audio/);
 await h.click();const stopped=h.metrics.stops;h.play('deal');assert.equal(h.metrics.starts,3);assert.ok(stopped>=6);assert.equal(JSON.parse(h.saved()).enabled,false);
 for(const options of [{unsupported:true},{resumeFails:true}]){const denied=setup(options);await denied.click();denied.play('hit');assert.equal(denied.metrics.starts,0);assert.match(denied.elements['sound-status'].textContent,/Play remains available/);}
 const blocked=setup({storageBlocked:true});await blocked.click();blocked.play('hit');assert.equal(blocked.metrics.starts,1);
 const corrupt=setup({stored:'not JSON'});assert.equal(corrupt.elements['sound-volume'].value,'0.2');
 console.log('PASS sound controls: zero-volume silence, mute, saved settings, gesture after reload, unsupported/blocked audio and denied/corrupt storage');
})().catch(error=>{console.error(error);process.exitCode=1});

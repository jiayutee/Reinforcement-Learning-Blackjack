const assert=require('node:assert/strict');
const {transitionCue}=require('../../foundations/sound-events.js');
const idle={revision:0,hand:null,reward:null,last_command:null};
const dealt={revision:1,hand:{done:false},reward:null,last_command:'deal'};
const hit={revision:2,hand:{done:false},reward:null,last_command:'hit'};
assert.equal(transitionCue(idle,dealt),'deal');
assert.equal(transitionCue(dealt,hit),'hit');
for(const [reward,cue] of [[1,'win'],[-1,'loss'],[0,'push']]){
 assert.equal(transitionCue(dealt,{revision:2,hand:{done:true},reward,last_command:'stand'}),cue);
}
assert.equal(transitionCue(dealt,{revision:2,hand:{done:true},reward:-1,last_command:'hit'}),'loss');
for(const [previous,current] of [[null,dealt],[dealt,dealt],[hit,dealt],[idle,hit],[dealt,{...hit,revision:2.5}],[dealt,{...hit,last_command:'unknown'}]])assert.equal(transitionCue(previous,current),null);
assert.equal(transitionCue(dealt,{...hit,hand:{done:true},reward:null}),null);
const before=JSON.stringify([dealt,hit]);transitionCue(dealt,hit);assert.equal(JSON.stringify([dealt,hit]),before);
console.log('PASS sound-event classification: deal/hit/outcomes, bust, refresh/replay/gaps/invalid state silence, no mutation');

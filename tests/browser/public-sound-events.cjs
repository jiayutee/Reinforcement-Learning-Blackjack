const assert=require('node:assert/strict');
const {transitionCue}=require('../../public_game/sound_events.js');
const before={revision:1,phase:'player_turn'};
function next(revision,phase,profit=null){return {revision,phase,normalized_profit:profit}}
assert.equal(transitionCue(before,next(2,'player_turn'),'hit'),'hit');
assert.equal(transitionCue(before,next(2,'player_turn'),'double'),'hit');
assert.equal(transitionCue(before,next(2,'player_turn'),'split'),'deal');
assert.equal(transitionCue(before,next(2,'player_turn'),'deal'),'deal');
for(const [profit,cue] of [[1,'win'],[-1,'loss'],[0,'push'],[1.5,'win'],[-2.5,'loss']]){
 for(const action of ['deal','hit','double','split','stand'])
  assert.equal(transitionCue(before,next(2,'settled',profit),action),cue);
}
for(const [previous,current,command] of [
 [null,next(2,'player_turn'),'hit'],[before,next(1,'player_turn'),'hit'],
 [before,next(3,'player_turn'),'hit'],[before,next(2,'player_turn'),'refresh'],
 [before,next(2,'player_turn'),'unknown'],[before,next(2,'settled'),'stand']
])assert.equal(transitionCue(previous,current,command),null);
assert.deepEqual(before,{revision:1,phase:'player_turn'});
console.log('PASS public sound events: accepted deal/hit/split and terminal normalized outcomes; rejected/gapped/refresh changes stay silent');

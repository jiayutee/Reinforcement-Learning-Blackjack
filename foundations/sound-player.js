/* Original synthesized cues; no external audio assets. Default is silent. */
(function(){
 const toggle=document.getElementById('sound-toggle'),slider=document.getElementById('sound-volume'),status=document.getElementById('sound-status');
 let context=null,enabled=false,volume=0.2,preferred=false;const nodes=new Set();
 try{const saved=JSON.parse(localStorage.getItem('blackjack-sound')||'null');if(saved){preferred=saved.enabled===true;if(Number.isFinite(saved.volume))volume=Math.max(0,Math.min(1,saved.volume));}}catch(_){}
 slider.value=String(volume);
 function save(){try{localStorage.setItem('blackjack-sound',JSON.stringify({enabled,volume}));}catch(_){}}
 function render(){toggle.textContent=enabled?'Mute sound':'Enable sound';toggle.setAttribute('aria-pressed',String(enabled));status.textContent=enabled?'Sound enabled.':'Sound off.';}
 function silence(){for(const node of nodes){try{node.stop();}catch(_){}}nodes.clear();}
 toggle.addEventListener('click',async()=>{
  if(enabled){enabled=false;silence();save();render();return;}
  try{const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)throw new Error('unsupported');context=context||new Audio();await context.resume();enabled=context.state==='running';save();render();if(!enabled)status.textContent='Audio could not start. Play remains available.';}
  catch(_){enabled=false;render();status.textContent='Sound unavailable in this browser. Play remains available.';}
 });
 slider.addEventListener('input',()=>{volume=Number(slider.value);silence();save();});
 render();if(preferred)status.textContent='Sound preference saved. Select Enable sound to activate audio for this page.';
 window.BlackjackSoundPlayer={play(cue){
  if(!enabled||!context||context.state!=='running'||volume===0)return;
  const notes={deal:[330],hit:[440],win:[523,659,784],loss:[220,165],push:[392,392]}[cue];if(!notes)return;
  try{silence();notes.forEach((frequency,index)=>{const oscillator=context.createOscillator(),gain=context.createGain();const start=context.currentTime+index*0.09;oscillator.type='sine';oscillator.frequency.value=frequency;gain.gain.setValueAtTime(0,start);gain.gain.linearRampToValueAtTime(volume*0.15,start+0.01);gain.gain.linearRampToValueAtTime(0,start+0.08);oscillator.connect(gain);gain.connect(context.destination);nodes.add(oscillator);oscillator.onended=()=>{nodes.delete(oscillator);oscillator.disconnect();gain.disconnect();};oscillator.start(start);oscillator.stop(start+0.09);});}
  catch(_){silence();enabled=false;render();status.textContent='Sound unavailable. Play remains available.';}
 }};
})();

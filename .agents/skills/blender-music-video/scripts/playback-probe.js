// Inject into the delivered page for actual playback QA. It deliberately sends ZERO gain
// to the speakers: analyser evidence is NOT listening. Reload the page for normal sound.
(() => {
  const v=document.querySelector('video'); if(!v)throw Error('No movie element');
  if(window.nativeMvQA)throw Error('Probe already attached; reload to start a fresh attempt');
  const context=new AudioContext(); const source=context.createMediaElementSource(v);
  const splitter=context.createChannelSplitter(2); source.connect(splitter);
  const analysers=[context.createAnalyser(),context.createAnalyser()];
  analysers.forEach((a,i)=>{a.fftSize=1024;splitter.connect(a,i)});
  const gain=context.createGain();gain.gain.value=0;source.connect(gain);gain.connect(context.destination);
  document.addEventListener('click',()=>context.resume(),{once:true});
  let active=false,timer,first=null,last=null,callbacks=0,maxRms=[0,0],errors=[],seeks=[],droppedStart=0,started=0;
  const callback=(now,metadata)=>{if(active){callbacks++;first??=metadata.mediaTime;last=metadata.mediaTime}v.requestVideoFrameCallback(callback)};
  v.requestVideoFrameCallback(callback);
  v.addEventListener('error',()=>errors.push(String(v.error?.message||v.error?.code)));
  v.addEventListener('seeking',()=>{if(active)seeks.push(v.currentTime)});
  function snapshot(){return {done:v.ended,active,time:v.currentTime,duration:v.duration,rate:v.playbackRate,loop:v.loop,paused:v.paused,first,last,callbacks,maxRms,errors,seeks,droppedDelta:v.getVideoPlaybackQuality().droppedVideoFrames-droppedStart,elapsed:(performance.now()-started)/1000,context:context.state,speakerGain:gain.gain.value,listened:false}}
  v.addEventListener('ended',()=>{if(active){active=false;clearInterval(timer);window.nativeMvQA.result=snapshot()}});
  window.nativeMvQA={snapshot,result:null,start(){if(!v.paused||v.currentTime>.01)throw Error('Pause/restart first; test controls before this uninterrupted pass');if(active)throw Error('Already running');active=true;first=last=null;callbacks=0;maxRms=[0,0];seeks=[];errors=[];droppedStart=v.getVideoPlaybackQuality().droppedVideoFrames;started=performance.now();timer=setInterval(()=>analysers.forEach((a,ch)=>{const data=new Float32Array(a.fftSize);a.getFloatTimeDomainData(data);maxRms[ch]=Math.max(maxRms[ch],Math.sqrt(data.reduce((sum,x)=>sum+x*x,0)/data.length))}),100);return snapshot()}};
  return {state:'PROBE_ATTACHED',speakerGain:0,note:'Use a real user gesture on Play; no autoplay or claimed listening'};
})()

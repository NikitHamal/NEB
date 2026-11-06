/* ============================================================================
   WhisperWeb — single-file on-device Whisper (tiny/base) transcriber
   Engine: @huggingface/transformers (onnxruntime-web) — WebGPU with WASM fallback
   Persistence: Cache API (model files, via transformers.js) + IndexedDB (history/settings)
   ========================================================================== */

const CDN = "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3";

/* ---------------- tiny helpers ---------------- */
const $ = (id) => document.getElementById(id);
const now = () => performance.now();
const fmtMB = (b) => (b / 1048576).toFixed(1);
const fmtT = (s) => { s = Math.max(0, s); const m = Math.floor(s / 60), ss = s - m * 60; return String(m).padStart(2,"0") + ":" + ss.toFixed(1).padStart(4,"0"); };
const fmtTs = (s) => { const h=Math.floor(s/3600),m=Math.floor(s/60)%60,sec=Math.floor(s%60); return (h?String(h).padStart(2,"0")+":":"")+String(m).padStart(2,"0")+":"+String(sec).padStart(2,"0"); };

function toast(msg, kind="", ms=3400){
  const t=document.createElement("div"); t.className="toast "+kind; t.innerHTML=msg;
  $("toasts").appendChild(t); setTimeout(()=>{t.style.opacity="0";t.style.transition="opacity .3s";setTimeout(()=>t.remove(),320)},ms);
}
function banner(html){ const b=$("banner"); if(!html){b.classList.remove("show");return;} b.innerHTML=html; b.classList.add("show"); }

/* ---------------- storage: IndexedDB with in-memory fallback ---------------- */
const Store = (() => {
  let db=null, mem={transcripts:[],kv:{}}, idbOK=true;
  function open(){
    return new Promise((res)=>{
      try{
        const rq=indexedDB.open("whisperweb",1);
        rq.onupgradeneeded=()=>{ const d=rq.result;
          if(!d.objectStoreNames.contains("transcripts")) d.createObjectStore("transcripts",{keyPath:"id",autoIncrement:true});
          if(!d.objectStoreNames.contains("kv")) d.createObjectStore("kv");
        };
        rq.onsuccess=()=>{db=rq.result;res(true)};
        rq.onerror=()=>{idbOK=false;res(false)};
        setTimeout(()=>{if(!db){idbOK=false;res(false)}},2500);
      }catch(e){idbOK=false;res(false)}
    });
  }
  const tx=(st,mode)=>db.transaction(st,mode).objectStore(st);
  return {
    open,
    get idbOK(){return idbOK},
    async put(st,val){ if(!idbOK){ if(st==="kv"){Object.assign(mem.kv,val)} else {mem.transcripts.push(val)} return; }
      return new Promise((res,rej)=>{const r=tx(st,"readwrite").put(val);r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)}) },
    async all(st){ if(!idbOK) return st==="kv"?[mem.kv]:mem.transcripts.slice().reverse();
      return new Promise((res,rej)=>{const r=tx(st,"readonly").getAll();r.onsuccess=()=>res(st==="kv"?[r.result[0]||{}]:r.result.reverse());r.onerror=()=>rej(r.error)}) },
    async del(st,key){ if(!idbOK){ if(st!=="kv"){const i=mem.transcripts.findIndex(x=>x.id===key); if(i>=0)mem.transcripts.splice(i,1);} return; }
      return new Promise((res,rej)=>{const r=tx(st,"readwrite").delete(key);r.onsuccess=()=>res();r.onerror=()=>rej(r.error)}) },
  };
})();

/* ---------------- settings — English only ---------------- */
const S = { model:"cactus/whistle", dtype:"q8", dev:"wasm", lang:"en", task:"transcribe",
            ts:true, auto:true, chunk:30, badDev:null };
async function loadSettings(){
  try{
    const [kv]=await Store.all("kv"); if(kv){
      Object.assign(S, kv);
      if(!S.model || (!S.model.endsWith(".en") && !S.model.includes("moonshine") && !S.model.includes("distil") && !S.model.includes("turbo") && !S.model.includes("large") && !S.model.includes("cactus/"))) S.model="cactus/whistle";
      S.lang="en"; S.task="transcribe";
      if(S.model==="onnx-community/moonshine-tiny") S.model="onnx-community/moonshine-tiny-ONNX";
      if(S.model==="onnx-community/moonshine-base") S.model="onnx-community/moonshine-base-ONNX";
      if(S.dev==="auto") S.dev="wasm";
      if(!S.dev) S.dev="wasm";
    }
  }catch(e){}
  syncUI();
}
async function saveSettings(){ try{ await Store.put("kv", {...S}); }catch(e){} }
function syncUI(){
  const m=$("selModel"); if(m) m.value=S.model;
  const d=$("selDtype"); if(d) d.value=S.dtype;
  const dv=$("selDev"); if(dv) dv.value=S.dev;
  const sl=$("selLang"); if(sl) sl.value="en";
  const st=$("selTask"); if(st) st.value="transcribe";
  const oTs=$("optTs"); if(oTs) oTs.checked=S.ts;
  const oAu=$("optAuto"); if(oAu) oAu.checked=S.auto;
  const oCh=$("optChunk"); if(oCh) oCh.value=S.chunk;
  try{ syncEngineUI(); }catch(e){}
}

/* ---------------- engine loading ---------------- */
let TF=null, pipe=null, pipeKey="", loadAbort=false;
let curDev="wasm", inferCount=0;   // curDev tracks the ACTIVE inference device
const dlRows=new Map();

/* race a promise against a timeout; rejection carries .timedOut */
function withTimeout(p, ms, label){
  return new Promise((res,rej)=>{
    const t=setTimeout(()=>rej(Object.assign(new Error(label+" timed out after "+Math.round(ms/1000)+"s"),{timedOut:true})),ms);
    p.then(v=>{clearTimeout(t);res(v)},e=>{clearTimeout(t);rej(e)});
  });
}
function isIsolated(){ try{ return !!self.crossOriginIsolated; }catch(e){ return false; } }
function configureWasmEnv(device){
  if(!TF||!TF.env||!TF.env.backends||!TF.env.backends.onnx||!TF.env.backends.onnx.wasm) return;
  const wasm = TF.env.backends.onnx.wasm;
  const isolated = isIsolated();
  if(device==="wasm"){
    wasm.proxy = isolated;
    wasm.numThreads = isolated ? Math.min(4, navigator.hardwareConcurrency||4) : 1;
    if(!isolated) wasm.simd = true;
  } else {
    wasm.proxy = false;
    wasm.numThreads = 1;
  }
}
/* pick device — English-only build defaults to WASM for stability */
function pickDevice(devSel){
  if(devSel==="webgpu"){
    if(S.badDev==="webgpu") toast("WebGPU stalled here before — will auto-switch to CPU if it hangs again","warn",5000);
    return "webgpu";
  }
  return "wasm";
}
/* kill a hung pipeline, remember the bad device, rebuild on WASM/CPU */
async function switchToWasm(reason){
  if(curDev!=="wasm"){ S.badDev=curDev; try{await saveSettings();}catch(e){} }
  try{ pipe&&await pipe.dispose(); }catch(e){}
  pipe=null; pipeKey="";
  if(TF&&TF.env&&TF.env.backends&&TF.env.backends.onnx&&TF.env.backends.onnx.wasm){
    try{ TF.env.backends.onnx.wasm.proxy = false; TF.env.backends.onnx.wasm.numThreads = 1; }catch(e){}
  }
  await new Promise(r=>setTimeout(r,150));
  toast(`⚠️ ${curDev==="webgpu"?"WebGPU":"GPU path"} ${reason} — switching to CPU (WASM) and retrying…`,"warn",6000);
  const d0 = S.dtype==="fp16"?"q8":S.dtype;
  try{
    return await loadWith(d0,"wasm",S.model);
  }catch(e){
    console.warn("[switchToWasm] q8 failed, retry fp32:", e);
    if(String(e&&e.message).includes("worker not ready") || String(e&&e.message).includes("proxy")){
      try{ TF.env.backends.onnx.wasm.proxy=false; TF.env.backends.onnx.wasm.numThreads=1; }catch(_){ }
    }
    return await loadWith("fp32","wasm",S.model);
  }
}

function setLED(id,cls,txt){ const l=$(id); l.className="led "+cls; if(txt!==undefined) $(txt.id||txt).textContent=txt.v; }

async function initEngine(){
  const net=$("netTxt"), led=$("ledNet");
  try{
    net.textContent="downloading engine…"; led.className="led warn";
    TF = await import(CDN);
    TF.env.allowLocalModels=false;
    TF.env.useBrowserCache=true;
    try{
      if(TF.env.backends&&TF.env.backends.onnx&&TF.env.backends.onnx.wasm){
        TF.env.backends.onnx.wasm.proxy = isIsolated();
        TF.env.backends.onnx.wasm.numThreads = isIsolated() ? Math.min(4, navigator.hardwareConcurrency||4) : 1;
      }
    }catch(e){}
    net.textContent="engine ready"; led.className="led on";
    return true;
  }catch(e){
    console.error(e);
    net.textContent="no network"; led.className="led err";
    banner(`⚠️ <b>Preview sandbox has no network access</b> — the AI engine can't be fetched here.
      This is expected inside the workspace preview. <b>Download this file and open it in Chrome/Edge/Firefox</b>
      (double-click works), or serve it with <code>python serve.py</code> — then the engine + models load and cache normally.
      Everything else in this page (recorder, VAD, waveform, history via memory fallback) still works for testing UI.`);
    return false;
  }
}

function dlUI(file,status,loaded,total){
  let row=dlRows.get(file);
  if(!row){
    const el=document.createElement("div"); el.className="dlrow";
    el.innerHTML=`<div class="fn"><span>${file.split("/").pop()}</span><span class="mb"></span></div><div class="bar"><i></i></div>`;
    $("dl").appendChild(el);
    row={el,pct:0,loaded:0}; dlRows.set(file,row);
  }
  const mb=row.el.querySelector(".mb"), bar=row.el.querySelector(".bar>i");
  if(status==="progress" && total){ row.loaded=loaded; row.pct=loaded/total*100; bar.style.width=row.pct.toFixed(1)+"%"; mb.textContent=fmtMB(loaded)+" / "+fmtMB(total)+" MB"; }
  if(status==="done"){ row.pct=100; bar.style.width="100%"; row.el.classList.add("done"); mb.textContent=mb.textContent||"✓"; }
  if(status==="initiate"){ mb.textContent="…"; }
}

async function loadPipeline(){
  if(whistleModel()) return loadWhistle();
  if(!TF && !(await initEngine())) return null;
  const model=$("selModel").value, dtype=$("selDtype").value, devSel=$("selDev").value;
  const device = pickDevice(devSel);
  if(dtype==="fp16" && device!=="webgpu"){ toast("fp16 needs WebGPU — falling back to q8","warn"); return loadWith("q8",device,model); }
  try{ return await loadWith(dtype,device,model); }
  catch(e){
    console.error("[loadPipeline] first attempt failed:", e);
    const msg0 = String(e&&e.message||e);
    if(msg0.includes("401") || msg0.includes("Unauthorized")){
      toast("Model not found (401) — this can happen if the model ID changed. Trying fallback tiny.en…","warn",6000);
      $("selModel").value="onnx-community/whisper-tiny.en"; S.model="onnx-community/whisper-tiny.en"; try{await saveSettings();}catch(_){}
      try{ return await loadWith(dtype==="fp16"?"q8":dtype,"wasm","onnx-community/whisper-tiny.en"); }catch(e2){ console.error("[loadPipeline] fallback also failed:",e2); }
    }
    const msg = String(e&&e.message||e);
    const isWebGPUFailure = msg.includes("null function") || msg.includes("WebGPU") || msg.includes("worker not ready") || device!=="wasm";
    if(isWebGPUFailure && device!=="wasm"){
      toast("WebGPU failed ("+msg.slice(0,90)+") — retrying on WASM/CPU…","warn",6000);
      try{ if(TF&&TF.env&&TF.env.backends&&TF.env.backends.onnx&&TF.env.backends.onnx.wasm){ TF.env.backends.onnx.wasm.proxy=false; TF.env.backends.onnx.wasm.numThreads=1; } }catch(_){}
      await new Promise(r=>setTimeout(r,200));
      try{ return await loadWith(dtype==="fp16"?"q8":dtype,"wasm",model); }catch(e2){
        console.error("[loadPipeline] wasm q8 also failed:", e2);
      }
    }
    if(dtype!=="fp32"){
      toast("q8 failed — retrying fp32 (bigger download)…","warn",5000);
      try{ if(TF&&TF.env&&TF.env.backends&&TF.env.backends.onnx&&TF.env.backends.onnx.wasm){ TF.env.backends.onnx.wasm.proxy=false; TF.env.backends.onnx.wasm.numThreads=1; } }catch(_){}
      return await loadWith("fp32","wasm",model);
    }
    throw e;
  }
}
async function loadWith(dtype,device,model){
  const key=model+"|"+dtype+"|"+device;
  if(pipe && pipeKey===key) return pipe;
  if(pipe){ try{ await pipe.dispose(); }catch(e){} pipe=null; await new Promise(r=>setTimeout(r,120)); }
  $("btnLoad").disabled=true; $("btnLoad").innerHTML=`<span class="spin"></span>&nbsp; loading`;
  $("dlStatus").innerHTML=`<b>${model.split("/")[1]}</b> · ${dtype} · ${device} — fetching/caching…`;
  $("mdlTxt").textContent=model.split("/")[1]+" "+dtype;
  $("devTxt").textContent = device==="webgpu" ? "WebGPU…" : "WASM (CPU)…";
  try{
    configureWasmEnv(device);
    const run = async () => TF.pipeline("automatic-speech-recognition", model, {
      dtype, device,
      progress_callback:(p)=>{ if(p.status) dlUI(p.file||"model",p.status,p.loaded,p.total); }
    });
    try{
      pipe = await run();
    }catch(e){
      const m = String(e&&e.message||e);
      if(m.includes("worker not ready") && TF.env.backends.onnx.wasm.proxy){
        console.warn("[loadWith] worker not ready with proxy=true, retrying proxy=false");
        TF.env.backends.onnx.wasm.proxy=false;
        TF.env.backends.onnx.wasm.numThreads=1;
        await new Promise(r=>setTimeout(r,150));
        pipe = await run();
      } else if(m.includes("null function") && device==="webgpu"){
        throw e;
      } else throw e;
    }
    pipeKey=key; curDev=device; inferCount=0;
    if(device==="webgpu" && S.badDev==="webgpu"){ S.badDev=null; try{await saveSettings();}catch(e){} }
    $("devTxt").textContent = device==="webgpu" ? "WebGPU ⚡" : (isIsolated()?"WASM ⚡ (threads)":"WASM (CPU)");
    $("dlStatus").innerHTML=`✅ <b>${model.split("/")[1]}</b> (${dtype}, ${device}) ready — cached for offline use`;
    $("btnLoad").innerHTML="✓ Model ready — reload / switch";
    toast("Model ready — you can record or drop audio now","ok");
    updateCacheInfo();
    return pipe;
  } catch(e){
    pipe=null; pipeKey="";
    if(device==="webgpu" && String(e&&e.message).includes("null function")){
      S.badDev="webgpu"; try{await saveSettings();}catch(_){}
    }
    throw e;
  } finally {
    $("btnLoad").disabled=false;
    if(!$("btnLoad").innerHTML.includes("ready")) $("btnLoad").innerHTML="⤓ Download / load model";
  }
}

async function ensurePipe(){
  if(whistleModel()){
    toast("Loading Whistle (one-time ~18MB download)…","",2600);
    const p=await loadPipeline(); if(!p) throw new Error("engine unavailable"); return p;
  }
  if(pipe) return pipe;
  toast("Loading model first (one-time download)…","",2600);
  const p=await loadPipeline(); if(!p) throw new Error("engine unavailable"); return p;
}

/* ---------------- Whistle engine (Cactus, default STT) ---------------- */
const WHISTLE_WORKER_URL = "/static/web/js/needle3/whistle.worker.js?v=1";
let whistleWorker=null, whistleReady=false, whistleInitPromise=null, whistleSeq=0;
const whistlePending=new Map();
let lastLang="en";
function whistleModel(){
  const v=($("selModel")&&$("selModel").value)||S.model||"";
  return v.indexOf("cactus/")===0;
}
function whistleStatus(m){
  if(m.status==="downloading"){
    dlUI(m.asset==="model"?"whistle/whistle.cact":"whistle/needle.wasm","progress",m.loaded,m.total);
    if(m.total) $("dlStatus").innerHTML=`<b>whistle</b> — fetching/caching… ${fmtMB(m.loaded||0)} / ${fmtMB(m.total)} MB`;
  }
  else if(m.status==="cache-hit"){ dlUI(m.asset==="model"?"whistle/whistle.cact":"whistle/needle.wasm","initiate"); }
  else if(m.status==="loading-engine"){ $("dlStatus").innerHTML=`<b>whistle</b> — starting engine…`; }
  else if(m.status==="loading-model"){ $("dlStatus").innerHTML=`<b>whistle</b> — loading 17MB model…`; }
}
function ensureWhistle(){
  if(whistleWorker&&whistleReady) return Promise.resolve(true);
  if(whistleInitPromise) return whistleInitPromise;
  whistleInitPromise=new Promise((resolve,reject)=>{
    let w;
    try{ w=new Worker(WHISTLE_WORKER_URL); }
    catch(e){ whistleInitPromise=null; reject(e); return; }
    whistleWorker=w;
    const fail=(msg)=>{ try{w.terminate();}catch(_){} if(whistleWorker===w) whistleWorker=null; whistleInitPromise=null; whistleReady=false; reject(new Error(msg)); };
    w.onmessage=(e)=>{
      const m=e.data||{};
      if(m.type==="status"){ whistleStatus(m); return; }
      if(m.type==="ready"){
        whistleReady=true; whistleInitPromise=null; curDev="wasm";
        $("mdlTxt").textContent="whistle 17MB"; $("devTxt").textContent="WASM (CPU)";
        resolve(true); return;
      }
      if(m.type==="result"){
        const p=whistlePending.get(m.id); if(p){ whistlePending.delete(m.id); p.res(m.result); }
        return;
      }
      if(m.type==="error"){
        if(m.id!=null&&whistlePending.has(m.id)){ const p=whistlePending.get(m.id); whistlePending.delete(m.id); p.rej(new Error(m.message||"whistle failed")); }
        else fail(m.message||"whistle init failed");
        return;
      }
    };
    w.onerror=(ev)=>fail("whistle worker error"+(ev&&ev.message?": "+ev.message:""));
    try{ w.postMessage({type:"init"}); }
    catch(e){ fail(e.message||"whistle init failed"); }
  });
  return whistleInitPromise;
}
function whistleTranscribe(f32){
  return ensureWhistle().then(()=>new Promise((res,rej)=>{
    const id=++whistleSeq;
    whistlePending.set(id,{res,rej});
    let view=f32 instanceof Float32Array?f32.slice(0):Float32Array.from(f32||[]);
    const max=16000*30;
    if(view.length>max) view=Float32Array.from(view.subarray(0,max));
    try{ whistleWorker.postMessage({type:"transcribe",id,pcm:view,language:null,wordTimestamps:false},[view.buffer]); }
    catch(e){ whistlePending.delete(id); rej(e); }
  }));
}
function killWhistle(){
  try{ if(whistleWorker) whistleWorker.terminate(); }catch(_){}
  whistleWorker=null; whistleReady=false; whistleInitPromise=null; whistleSeq=0;
  whistlePending.forEach(p=>{ try{p.rej(new Error("engine cleared"));}catch(_){} });
  whistlePending.clear();
}
function syncEngineUI(){
  const w=whistleModel();
  const row=$("precDevRow"), note=$("whistleEngineNote");
  if(row) row.style.display=w?"none":"";
  if(note) note.style.display=w?"block":"none";
  const fx=$("langFixedBox"), au=$("langAutoBox");
  if(fx) fx.style.display=w?"none":"flex";
  if(au) au.style.display=w?"flex":"none";
}
async function loadWhistle(){
  $("btnLoad").disabled=true; $("btnLoad").innerHTML=`<span class="spin"></span>&nbsp; loading`;
  try{
    await ensureWhistle();
    $("dlStatus").innerHTML=`✅ <b>whistle</b> (17MB, 7 languages) ready — cached for offline use`;
    $("btnLoad").innerHTML="✓ Whistle ready — reload / switch";
    toast("Whistle ready — you can record or drop audio now","ok");
    updateCacheInfo();
    return true;
  }catch(e){
    console.error("[loadWhistle]",e);
    toast("Whistle failed to load: "+(e.message||e)+" — pick a Whisper model instead","err",6000);
    throw e;
  }finally{
    $("btnLoad").disabled=false;
    if(!$("btnLoad").innerHTML.includes("ready")) $("btnLoad").innerHTML="⤓ Download / load model";
  }
}

/* ---------------- cache utils ---------------- */
async function updateCacheInfo(){
  try{
    let bytes=0;
    if(window.caches){
      for(const n of await caches.keys()){
        const c=await caches.open(n); const rs=await c.keys();
        for(const r of rs){ const resp=await c.match(r); const cl=resp&&resp.headers.get("content-length"); if(cl) bytes+= +cl; }
      }
    }
    const est = navigator.storage?.estimate ? await navigator.storage.estimate() : null;
    const shown = est?.usage ?? bytes;
    $("cacheTxt").textContent = shown ? fmtMB(shown)+" MB" : (bytes?"~":"—");
    $("cacheTag").textContent = shown ? fmtMB(shown)+" MB stored" : "";
  }catch(e){ $("cacheTxt").textContent="n/a"; }
}
const langFor = () => "en";
$("btnPersist").onclick=async()=>{
  try{ const ok=await navigator.storage.persist();
    toast(ok?"Storage marked persistent — browser won't evict your models 🎉":"Browser declined persistence (install the site as an app or keep visiting)",ok?"ok":"warn",5000);
  }catch(e){ toast("Persistence API unavailable here","warn"); }
};
$("btnWipe").onclick=async()=>{
  try{ if(window.caches){ for(const n of await caches.keys()) await caches.delete(n); }
    $("dl").innerHTML=""; dlRows.clear(); pipe=null; pipeKey=""; $("mdlTxt").textContent="none";
    S.badDev=null; try{await saveSettings();}catch(e){}
    banner("");
    await updateCacheInfo(); toast("Model cache + WebGPU blocklist cleared — you can retry WebGPU now","ok");
  }catch(e){ toast("Couldn't clear: "+e.message,"err"); }
};

/* ---------------- transcript state ---------------- */
let SEG=[];             // {text,t0,t1}
let lastRun={audioSec:0,inferSec:0};
function renderTx(){
  const el=$("transcript");
  if(!SEG.length){ el.innerHTML='<span class="ph">Nothing yet. Load the model, then record or drop audio.</span>'; updStats(); return; }
  el.innerHTML = SEG.map(s=>{
    const ts = (S.ts!==false && s.t0!=null) ? `<span class="ts">[${fmtTs(s.t0)}]</span>` : "";
    const cls = s.pending?"seg live":"seg";
    return `<div class="${cls}">${ts}${escapeHtml(s.text)}</div>`;
  }).join("");
  el.scrollTop=el.scrollHeight; updStats();
}
function escapeHtml(s){ return s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
function updStats(){
  const words=SEG.reduce((n,s)=>n+s.text.trim().split(/\s+/).filter(Boolean).length,0);
  $("stW").textContent=words;
  $("stA").textContent=lastRun.audioSec.toFixed(1)+"s";
  $("stI").textContent=lastRun.inferSec?lastRun.inferSec.toFixed(1)+"s":"—";
  $("stR").textContent=lastRun.inferSec&&lastRun.inferSec>0?(lastRun.audioSec/lastRun.inferSec).toFixed(2)+"× realtime":"—";
}
async function saveRun(meta){
  try{
    await Store.put("transcripts",{createdAt:Date.now(),model:S.model,dtype:S.dtype,dev:$("devTxt").textContent,
      lang:(whistleModel()?lastLang:"en"),task:"transcribe",text:SEG.map(s=>s.text).join(" "),chunks:SEG.map(s=>({text:s.text,t0:s.t0,t1:s.t1})),
      audioSec:lastRun.audioSec,inferSec:lastRun.inferSec,src:meta||"live"});
    renderHist();
  }catch(e){}
}
async function renderHist(){
  try{
    const items=await Store.all("transcripts");
    const h=$("hist");
    if(!items.length){h.innerHTML='<div class="hint">Your transcripts are saved on this device automatically.</div>';return;}
    h.innerHTML=items.slice(0,30).map(it=>`
      <div class="hitem" data-id="${it.id}">
        <button class="del" data-del="${it.id}" title="delete">✕</button>
        <div class="top"><b style="font-size:12.5px">${new Date(it.createdAt).toLocaleString()}</b><span class="when">${(it.audioSec||0).toFixed(0)}s · ${(it.inferSec? (it.audioSec/it.inferSec).toFixed(1)+"×":"")}</span></div>
        <div class="txt">${escapeHtml((it.text||"").slice(0,160)||"(empty)")}</div>
        <div class="meta">${(it.model||"").split("/")[1]} · ${it.lang||"en"} · transcribe</div>
      </div>`).join("");
    h.querySelectorAll(".hitem").forEach(el=>el.onclick=async(e)=>{
      if(e.target.dataset.del){ await Store.del("transcripts",+e.target.dataset.del); renderHist(); return; }
      const items2=await Store.all("transcripts"); const it=items2.find(x=>x.id===+el.dataset.id); if(!it)return;
      SEG=(it.chunks||[{text:it.text,t0:null}]).map(c=>({text:c.text,t0:c.t0,t1:c.t1}));
      lastRun={audioSec:it.audioSec||0,inferSec:it.inferSec||0};
      $("srcTag").textContent="from history · "+(it.model||"").split("/")[1];
      renderTx();
    });
  }catch(e){}
}

/* ---------------- exports ---------------- */
function dl(name,mime,txt){
  const a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([txt],{type:mime})); a.download=name; a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),4000);
}
const srtT=(t)=>{const h=Math.floor(t/3600),m=Math.floor(t/60)%60,s=Math.floor(t%60),ms=Math.floor((t%1)*1000);
  return `${String(h).padStart(2,"0")}:${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")},${String(ms).padStart(3,"0")}`;};
function buildSRT(vtt){
  const segs=SEG.filter(s=>s.t0!=null&&!s.pending);
  if(!segs.length) return null;
  return segs.map((s,i)=>`${i+1}\n${vtt?srtT(s.t0).replace(",",".")+" --> "+srtT(s.t1||s.t0+2).replace(",","."):srtT(s.t0)+" --> "+srtT(s.t1||s.t0+2)}\n${s.text.trim()}\n`).join("\n");
}
const baseName=()=>"transcript-"+new Date().toISOString().slice(0,16).replace(/[:T]/g,"-");
$("btnTxt").onclick=()=>dl(baseName()+".txt","text/plain",SEG.map(s=>s.text.trim()).join("\n"));
$("btnSrt").onclick=()=>{const s=buildSRT(false); s?dl(baseName()+".srt","text/plain",s):toast("No timestamped segments yet","warn");};
$("btnVtt").onclick=()=>{const s=buildSRT(true); s?dl(baseName()+".vtt","text/vtt","WEBVTT\n\n"+s):toast("No timestamped segments yet","warn");};
$("btnJson").onclick=()=>dl(baseName()+".json","application/json",JSON.stringify({model:S.model,dtype:S.dtype,lang:"en",task:"transcribe",audioSec:lastRun.audioSec,inferSec:lastRun.inferSec,segments:SEG},null,2));
$("btnCopy").onclick=async()=>{try{await navigator.clipboard.writeText(SEG.map(s=>s.text.trim()).join("\n"));toast("Copied","ok",1600);}catch(e){toast("Clipboard blocked here","warn")}};
$("btnClear").onclick=()=>{SEG=[];lastRun={audioSec:0,inferSec:0};$("srcTag").textContent="";renderTx();};

/* ---------------- audio: recorder + VAD ---------------- */
const SR=16000;
let ac=null, stream=null, node=null, worklet=null, recording=false;
let samples=0, recStart=0, inferSecAcc=0, audioSecAcc=0;
const vad={nf:1e-4,hist:[],inSpeech:false,speechRun:0,silRun:0,segStart:0,pre:[]};
const segQueue=[]; let qBusy=false;

async function getCtx(){
  if(!ac){ ac=new (window.AudioContext||window.webkitAudioContext)({sampleRate:SR}); }
  if(ac.state==="suspended") await ac.resume();
  return ac;
}
async function startRec(){
  const p=await ensurePipe(); if(!p) return;
  try{ stream=await navigator.mediaDevices.getUserMedia({audio:{channelCount:1,echoCancellation:true,noiseSuppression:true,autoGainControl:true}}); }
  catch(e){ toast("Mic permission denied or unavailable: "+e.message,"err",5000); return; }
  const ctx=await getCtx();
  const src=ctx.createMediaStreamSource(stream);
  try{
    if(location.protocol==="file:") throw new Error("file:// blocks blob: worklets");
    const code=`class VADProc extends AudioWorkletProcessor{ process(inputs){ const ch=inputs[0]&&inputs[0][0]; if(ch) this.port.postMessage(ch.slice(0)); return true; } }
      registerProcessor('vad-proc',VADProc);`;
    worklet=new Blob([code],{type:"application/javascript"});
    await ctx.audioWorklet.addModule(URL.createObjectURL(worklet));
    node=new AudioWorkletNode(ctx,"vad-proc");
  }catch(e){ node=ctx.createScriptProcessor(4096,1,1); }  // legacy fallback (works everywhere incl. file://)
  node.port ? node.port.onmessage=(e)=>onAudio(e.data) : node.onaudioprocess=(e)=>onAudio(e.inputBuffer.getChannelData(0));
  src.connect(node); node.connect(ctx.destination);
  recording=true; samples=0; inferSecAcc=0; audioSecAcc=0;
  Object.assign(vad,{nf:1e-4,inSpeech:false,speechRun:0,silRun:0,segStart:0,pre:[]});
  SEG=[]; renderTx(); recStart=now();
  $("btnRec").classList.add("on"); $("recState").textContent="● recording — VAD listening…";
  drawVU(true);
}
function stopRec(){
  recording=false;
  try{ stream&&stream.getTracks().forEach(t=>t.stop()); }catch(e){}
  try{ node&&node.disconnect(); }catch(e){}
  if(vad.inSpeech) finalizeSeg(samples- SR*0.12);
  $("btnRec").classList.remove("on"); $("recState").textContent="idle — click the red button to record";
  audioSecAcc=samples/SR; lastRun={audioSec:audioSecAcc,inferSec:inferSecAcc};
  updStats(); saveRun("mic");
}
$("btnRec").onclick=()=>recording?stopRec():startRec();

function onAudio(f32){
  if(!recording) return;
  samples+=f32.length;
  pushLevel(f32);
  for(let i=0;i<f32.length;i+=480){
    const w=f32.subarray(i,i+480); const rms=rmsOf(w);
    // adaptive noise floor (only learn from quiet)
    if(rms<vad.nf*2.5) vad.nf=vad.nf*0.96+rms*0.04;
    const thr=Math.max(vad.nf*2.8,0.0065);
    if(rms>thr){ vad.speechRun++; vad.silRun=0; } else { vad.silRun++; if(!vad.inSpeech) vad.speechRun=0; }
    if(!vad.inSpeech && vad.speechRun>=8){                 // ~240ms speech → start
      vad.inSpeech=true; vad.segStart=Math.max(0,samples-f32.length+i-480*8-SR*0.25);
      vad.pre=vad.pre.slice(-Math.floor(SR*0.25/480));
    }
    if(vad.inSpeech && vad.silRun>=18){                    // ~550ms silence → end
      finalizeSeg(samples-f32.length+i-480*4+SR*0.1); vad.inSpeech=false; vad.speechRun=0;
    }
    if(vad.inSpeech && (samples-vad.segStart)/SR>28){      // hard split at 28s
      finalizeSeg(samples); vad.segStart=samples; vad.silRun=0;
    }
    if(!vad.inSpeech){ vad.pre.push({w:Float32Array.from(w),at:samples-f32.length+i}); if(vad.pre.length>40) vad.pre.shift(); }
  }
  $("recTime").textContent=fmtT(samples/SR);
}
const rmsOf=(w)=>{let s=0;for(let i=0;i<w.length;i++)s+=w[i]*w[i];return Math.sqrt(s/w.length)};
let segBuf=null,segStartSample=0;
function finalizeSeg(endSample){
  const start=vad.segStart, len=endSample-start;
  if(len<SR*0.25) return;
  // we kept audio nowhere except preroll — accumulate live: (segments are assembled on the fly)
  // strategy: capture from preroll + ongoing buffers is complex; instead we record continuously into recBuffer
  const seg=recBuffer.subarray(start,endSample);
  if(!seg||!seg.length) return;
  segQueue.push({f32:Float32Array.from(seg),t0:start/SR,t1:endSample/SR});
  $("recState").textContent=`● recording — queued segment ${segQueue.length} (${len/SR|0}s)`;
  runQueue();
}
/* continuous recording buffer (supports VAD segmenting) */
let recBuffer=new Float32Array(SR*60*10), recLen=0;
const _origOnAudio=onAudio;
onAudio=function(f32){
  if(recLen+f32.length>recBuffer.length){ const nb=new Float32Array(recBuffer.length*2); nb.set(recBuffer); recBuffer=nb; }
  recBuffer.set(f32,recLen); recLen+=f32.length;
  _origOnAudio(f32);
};

async function runQueue(){
  if(qBusy||!segQueue.length) return; qBusy=true;
  while(segQueue.length){
    const {f32,t0,t1}=segQueue.shift();
    if(!S.auto){ SEG.push({text:"(segment recorded — auto-transcribe off)",t0,t1,pending:false}); renderTx(); continue; }
    SEG.push({text:"… transcribing",t0,t1,pending:true}); renderTx();
    const t=now();
    try{
      const audioSec=f32.length/SR;
      const ms=30000+audioSec*1500;
      let out=null, attempt=0;
      while(attempt<2){
        attempt++;
        const segP=SEG.find(s=>s.pending);
        if(segP) segP.text = attempt===1
          ? (curDev==="webgpu"&&inferCount===0 ? "… first WebGPU run — compiling shaders" : "… transcribing")
          : "… GPU stalled — retrying on CPU";
        renderTx();
        try{
          if(whistleModel()){
            const w=await withTimeout(whistleTranscribe(f32), ms, "inference");
            out={text:w.text||"", language:w.language||""};
            lastLang=w.language||"en";
            break;
          }
          if(!pipe) throw new Error("model not ready — reloading");
          const opts = S.model.endsWith(".en")
            ? { return_timestamps:false }
            : { language:langFor(), task:S.task, return_timestamps:false };
          out=await withTimeout(pipe(f32, opts), ms, "inference");
          break;
        }catch(e){
          console.error(e);
          const msg=String(e&&e.message||e);
          const isGpuCrash = msg.includes("null function") || msg.includes("RuntimeError");
          const shouldFallback = (e.timedOut || isGpuCrash) && attempt===1 && curDev!=="wasm";
          if(shouldFallback){ await switchToWasm(isGpuCrash?"crashed (null function)":"stalled"); continue; }
          throw e;
        }
      }
      if(!out) throw new Error("no output");
      inferCount++;
      inferSecAcc+=(now()-t)/1000; audioSecAcc+=f32.length/SR;
      const seg=SEG.find(s=>s.pending); if(seg){seg.text=(out.text||"").trim()||"(silence)";seg.pending=false;}
      lastRun={audioSec:audioSecAcc,inferSec:inferSecAcc};
      $("recState").textContent=`● recording — ${inferCount} segment${inferCount>1?"s":""} done (${curDev==="webgpu"?"WebGPU":"CPU"})`;
    }catch(e){ console.error(e); const seg=SEG.find(s=>s.pending); if(seg){seg.text="(error: "+e.message+")";seg.pending=false;} }
    renderTx();
    await new Promise(r=>setTimeout(r,0));
  }
  qBusy=false;
}

/* ---------------- VU meter / waveform ---------------- */
const vuC=$("vu"),vuX=vuC.getContext("2d");let levels=new Array(120).fill(0),vuOn=false;
function pushLevel(f32){ let m=0; for(let i=0;i<f32.length;i++){const a=Math.abs(f32[i]);if(a>m)m=a;} levels.push(m);if(levels.length>140)levels.shift(); }
function drawVU(on){ vuOn=on; if(on) requestAnimationFrame(drawFrame); }
function drawFrame(){
  vuC.width=vuC.clientWidth*devicePixelRatio; vuC.height=vuC.clientHeight*devicePixelRatio;
  const W=vuC.width,H=vuC.height,n=levels.length,bw=W/n;
  vuX.clearRect(0,0,W,H);
  for(let i=0;i<n;i++){
    const h=Math.max(2,levels[i]*H*1.6);
    const g=vuX.createLinearGradient(0,H,0,H-h);
    g.addColorStop(0,"#4f8cff");g.addColorStop(1,vad.inSpeech?"#2fd48a":"#8f6bff");
    vuX.fillStyle=g; vuX.fillRect(i*bw,(H-h)/2,bw*0.7,h);
  }
  if(vuOn) requestAnimationFrame(drawFrame);
}

/* ---------------- file transcription — English only ---------------- */
/* Live progressive mode: for files longer than ~36s we transcribe chunk-by-chunk
   and stream results into the transcript view, so a 3-min song shows text
   chunk-by-chunk instead of waiting for the whole file. Short files keep
   the original single-call path (which uses pipeline internal chunking). */
let _fileAbort = 0;
async function transcribeFile(buf,name){
  const myRun = ++_fileAbort;
  let p=await ensurePipe(); if(!p) return;
  if(myRun !== _fileAbort) return;
  banner("");
  $("recState").textContent="decoding "+name+"…";
  let f32;
  try{
    const ab=await buf.arrayBuffer();
    const tmp=new (window.AudioContext||window.webkitAudioContext)();
    const dec=await tmp.decodeAudioData(ab.slice(0));
    const off=new OfflineAudioContext(1,Math.ceil(dec.duration*SR),SR);
    const src=off.createBufferSource(); src.buffer=dec; src.connect(off.destination); src.start();
    const rend=await off.startRendering();
    f32=rend.getChannelData(0);
    await tmp.close();
  }catch(e){ toast("Couldn't decode this file: "+e.message,"err",5000); $("recState").textContent="idle"; return; }
  if(myRun !== _fileAbort) return;
  const dur=f32.length/SR;
  $("recTime").textContent=fmtT(dur);
  $("srcTag").textContent=name;
  const chunk_s = Math.min(30,Math.max(10,+S.chunk||30));
  const useStreaming = dur > chunk_s * 1.15;
  // short file: single call keeps timestamp chunk merging
  if(!useStreaming){
    SEG=[{text:"… transcribing "+dur.toFixed(1)+"s of audio (chunks of "+chunk_s+"s)",pending:true,t0:0}];
    renderTx();
    const t=now();
    try{
      let out=null, attempt=0;
      while(attempt<2){
        attempt++;
        if(myRun !== _fileAbort) return;
        if(SEG[0]) SEG[0].text = attempt===1
          ? `… transcribing ${dur.toFixed(1)}s of audio (chunks of ${chunk_s}s)${curDev==="webgpu"&&inferCount===0?" — first run compiles GPU shaders":""}`
          : "… GPU stalled — retrying on CPU (WASM)";
        renderTx();
        try{
          if(whistleModel()){
            const w=await withTimeout(whistleTranscribe(f32), 60000+dur*8000, "file inference");
            out={text:w.text||"", language:w.language||""};
            lastLang=w.language||"en";
            break;
          }
          if(!p) throw new Error("model not ready — reloading");
          const baseOpts = { return_timestamps:true, chunk_length_s: chunk_s, stride_length_s: chunk_s*0.4 };
          const opts = S.model.includes("moonshine") || S.model.endsWith(".en") ? baseOpts : { language:langFor(), task:S.task, ...baseOpts };
          out=await withTimeout(p(f32, opts), 60000+dur*8000, "file inference");
          break;
        }catch(e){
          console.error(e);
          const msg=String(e&&e.message||e);
          const isGpuCrash = msg.includes("null function") || msg.includes("RuntimeError");
          const shouldFallback = (e.timedOut || isGpuCrash) && attempt===1 && curDev!=="wasm";
          if(shouldFallback){ p = await switchToWasm(isGpuCrash?"crashed (null function)":"stalled"); if(myRun!==_fileAbort) return; continue; }
          throw e;
        }
      }
      if(!out) throw new Error("no output");
      if(myRun !== _fileAbort) return;
      inferCount++;
      const infer=(now()-t)/1000;
      lastRun={audioSec:dur,inferSec:infer};
      if(out.chunks&&out.chunks.length){
        SEG=out.chunks.map(c=>({text:c.text.trim(),t0:c.timestamp?.[0]??null,t1:c.timestamp?.[1]??null}));
      } else SEG=[{text:(out.text||"").trim(),t0:null}];
      if(!SEG.length||!SEG.map(s=>s.text).join("").trim()) SEG=[{text:"(no speech detected)",t0:null}];
      renderTx();
      if(whistleModel()) $("srcTag").textContent=name+" · "+lastLang;
      $("recState").textContent=`done — ${(infer? (dur/infer).toFixed(2):"?")}× realtime on ${$("devTxt").textContent}`;
      toast(`Transcribed ${dur.toFixed(1)}s in ${infer.toFixed(1)}s (${(dur/infer).toFixed(2)}× realtime)`,"ok",4500);
      saveRun("file:"+name);
    }catch(e){
      console.error(e);
      if(myRun!==_fileAbort) return;
      SEG=[{text:"⚠️ transcription failed: "+(e.message||e),t0:null}]; renderTx();
      $("recState").textContent="idle";
    }
    return;
  }
  // long file: progressive chunk-by-chunk streaming (overlap = stride 40% to match pipeline, guarantees no gaps)
  SEG=[];
  renderTx();
  const wall0=now();
  let doneSegs=[];
  let inferAcc=0;
  const stride_s = chunk_s*0.4;
  const step_s = chunk_s - stride_s;
  // build chunk start list with overlap, ensuring tail is covered (short last chunk is ok)
  const starts=[];
  for(let s=0; s<dur; s+=step_s) starts.push(s);
  const totalChunks = starts.length;
  toast(`Streaming ${dur.toFixed(0)}s in ${totalChunks} chunks (stride ${stride_s.toFixed(1)}s) — live transcript below`,"", 4000);
  for(let idx=0; idx<totalChunks; idx++){
    if(myRun !== _fileAbort) return;
    const start = starts[idx];
    const end = Math.min(dur, start+chunk_s);
    const sIdx = Math.floor(start*SR);
    const eIdx = Math.floor(end*SR);
    const chunk = f32.subarray(sIdx, eIdx);
    // placeholder for current chunk
    SEG = [...doneSegs, {text:`… transcribing chunk ${idx+1}/${totalChunks} (${start.toFixed(0)}–${end.toFixed(0)}s / ${dur.toFixed(0)}s)`, pending:true, t0:start, t1:end}];
    renderTx();
    $("recState").textContent=`transcribing ${idx+1}/${totalChunks} — ${((idx)/totalChunks*100).toFixed(0)}%`;
    $("dlStatus").textContent=`Streaming chunk ${idx+1}/${totalChunks} (${(end-start).toFixed(0)}s) — live below`;
    const tChunk=now();
    let out=null, attempt=0;
    while(attempt<2){
      attempt++;
      if(myRun !== _fileAbort) return;
      try{
        if(whistleModel()){
          const w=await withTimeout(whistleTranscribe(chunk), 25000 + chunk.length/SR*2200, "chunk inference");
          out={text:w.text||"", language:w.language||""};
          lastLang=w.language||"en";
          break;
        }
        if(!p) throw new Error("model not ready — reloading");
        // For English-only models omit language/task; moonshine also English-like so omit. Keep timestamps for live sub-segments.
        const opts = (S.model.includes("moonshine") || S.model.endsWith(".en")) ? { return_timestamps:true } : { language:langFor(), task:S.task, return_timestamps:true };
        const ms = 25000 + chunk.length/SR*2200;
        out=await withTimeout(p(chunk, opts), ms, "chunk inference");
        break;
      }catch(e){
        console.error(e);
        const msg=String(e&&e.message||e);
        const isGpuCrash = msg.includes("null function") || msg.includes("RuntimeError");
        const shouldFallback = (e.timedOut || isGpuCrash) && attempt===1 && curDev!=="wasm";
        if(shouldFallback){ p = await switchToWasm(isGpuCrash?"crashed (null function)":"stalled"); if(myRun!==_fileAbort) return; continue; }
        // per-chunk failure: keep error as segment and continue
        out={text:`(chunk ${idx+1} failed: ${e.message})`};
        break;
      }
    }
    if(myRun !== _fileAbort) return;
    inferAcc += (now()-tChunk)/1000;
    const txt = (out && (out.text|| (out.chunks&&out.chunks.map(c=>c.text).join(" "))) || "").trim() || "(silence)";
    // If pipeline returned timestamps per-chunk, offset them; otherwise use chunk bounds
    let segs=[];
    if(out && out.chunks && out.chunks.length){
      segs = out.chunks.map(c=>({text:c.text.trim(), t0: (c.timestamp?.[0]!=null? c.timestamp[0]+start : start), t1: (c.timestamp?.[1]!=null? c.timestamp[1]+start : null)}));
    } else {
      segs=[{text: txt, t0:start, t1:end}];
    }
    // deduplicate overlap: keep only segments starting in the non-overlapping window
    if(idx>0){
      const len = end - start;
      const cutoff = (idx===totalChunks-1 && len < stride_s) ? start : start + stride_s/2;
      const filtered = segs.filter(s=> (s.t0==null) || s.t0 >= cutoff - 0.05);
      if(filtered.length) segs = filtered;
    }
    if(idx < totalChunks-1){
      const tailCut = end - stride_s/2;
      const filtered2 = segs.filter(s=> (s.t0==null) || s.t0 < tailCut + 0.05);
      if(filtered2.length) segs = filtered2;
    }
    doneSegs.push(...segs);
    SEG=[...doneSegs];
    renderTx();
    inferCount++;
    lastRun={audioSec: end, inferSec: inferAcc};
    updStats();
    // allow UI to breathe
    await new Promise(r=>setTimeout(r,0));
  }
  if(myRun !== _fileAbort) return;
  const inferTot=(now()-wall0)/1000;
  lastRun={audioSec:dur,inferSec:inferTot};
  if(whistleModel()) $("srcTag").textContent=name+" · "+lastLang;
  $("recState").textContent=`done — ${(inferTot? (dur/inferTot).toFixed(2):"?")}× realtime on ${$("devTxt").textContent}`;
  $("dlStatus").textContent=`✅ ${totalChunks} chunks streamed — ${dur.toFixed(1)}s in ${inferTot.toFixed(1)}s`;
  toast(`Streamed ${dur.toFixed(1)}s in ${inferTot.toFixed(1)}s (${(dur/inferTot).toFixed(2)}× realtime)`,"ok",5000);
  saveRun("file:"+name);
}
$("btnFile").onclick=()=>$("fileIn").click();
$("fileIn").onchange=(e)=>{ const f=e.target.files[0]; if(f) transcribeFile(f,f.name); e.target.value=""; };
$("btnSample").onclick=async()=>{
  try{
    const r=await fetch("https://cdn.jsdelivr.net/gh/openai/whisper@main/tests/jfk.flac");
    if(!r.ok) throw new Error("HTTP "+r.status);
    const b=await r.blob();
    transcribeFile(b,"jfk.flac (sample)");
  }catch(e){ toast("Sample needs network (blocked in this preview): "+e.message,"warn",5000); }
};

/* drag & drop */
let dragN=0;
addEventListener("dragenter",(e)=>{e.preventDefault();dragN++;$("drop").classList.add("show")});
addEventListener("dragover",(e)=>e.preventDefault());
addEventListener("dragleave",(e)=>{dragN--;if(dragN<=0){dragN=0;$("drop").classList.remove("show")}});
addEventListener("drop",(e)=>{e.preventDefault();dragN=0;$("drop").classList.remove("show");
  const f=e.dataTransfer.files[0]; if(f) transcribeFile(f,f.name);});

/* ---------------- UI wiring ---------------- */
$("btnLoad").onclick=()=>loadPipeline();
$("selModel").onchange=async(e)=>{S.model=e.target.value; S.lang="en"; S.task="transcribe";
      if(S.model==="onnx-community/moonshine-tiny") S.model="onnx-community/moonshine-tiny-ONNX";
      if(S.model==="onnx-community/moonshine-base") S.model="onnx-community/moonshine-base-ONNX"; await saveSettings();syncUI();try{syncEngineUI();}catch(_){}};
$("selDtype").onchange=async(e)=>{S.dtype=e.target.value;await saveSettings()};
$("selDev").onchange=async(e)=>{S.dev=e.target.value;await saveSettings()};
$("optTs").onchange=async(e)=>{S.ts=e.target.checked;await saveSettings();renderTx()};
$("optAuto").onchange=async(e)=>{S.auto=e.target.checked;await saveSettings()};
$("optChunk").onchange=async(e)=>{S.chunk=+e.target.value||30;await saveSettings()};

addEventListener("keydown",(e)=>{
  if(e.target.matches("input,select,textarea"))return;
  if(e.key==="r"||e.key==="R"){recording?stopRec():startRec();}
  else if(e.key==="c"||e.key==="C"){$("btnCopy").click();}
  else if(e.key==="s"||e.key==="S"){$("btnSrt").click();}
  else if(e.key==="?"){toast("<b>WhisperWeb</b> — Whistle 17MB (default, 7 languages) or Whisper/Moonshine running fully in your browser. Models cache locally (Cache API) and transcripts persist (IndexedDB). No audio ever leaves this device.","",7000);}
});

/* ---------------- boot ---------------- */
(async()=>{
  await Store.open();
  if(!Store.idbOK) banner("ℹ️ IndexedDB is blocked in this sandboxed preview — history will be kept in memory only. In a normal browser tab it persists.");
  await loadSettings();
  await renderHist();
  renderTx();
  updateCacheInfo();
  const okEngine=await initEngine();
  const iso=isIsolated();
  if(S.badDev==="webgpu"){
    $("devTxt").textContent = iso ? "WASM ⚡ (threads)" : "WASM (CPU)";
    banner(`⚠️ WebGPU previously crashed on this device (<code>RuntimeError: null function</code>) — auto-switched to <b>WASM (CPU)</b> for stability. To retry WebGPU, set <b>Device → WebGPU</b> and hit Download. <button onclick="localStorage.clear();location.reload()" style="background:#2a2213;border:1px solid #5b4a2e;color:#ffd9a0;border-radius:8px;padding:3px 10px;font-size:12px;margin-left:8px;cursor:pointer">reset</button> <button onclick="document.getElementById('banner').classList.remove('show')" style="background:#2a2213;border:1px solid #5b4a2e;color:#ffd9a0;border-radius:8px;padding:3px 10px;font-size:12px;margin-left:4px;cursor:pointer">dismiss</button>`);
  } else if(navigator.gpu) $("devTxt").textContent = iso ? "WebGPU? · WASM ready" : "WASM (CPU) · WebGPU available";
  else $("devTxt").textContent = iso ? "WASM ⚡ (threads)" : "WASM (CPU)";
  if(okEngine && location.protocol==="file:"){
    banner($("banner").innerHTML + `<br>💡 You're running from <b>file://</b> — blob worklets are restricted and <code>crossOriginIsolated</code> is false (no threads). For max speed: run <code>python serve.py</code> → <code>http://localhost:8000</code> (threads 2–4× faster). <button onclick="document.getElementById('banner').classList.remove('show')" style="background:#2a2213;border:1px solid #5b4a2e;color:#ffd9a0;border-radius:8px;padding:3px 10px;font-size:12px;margin-left:8px;cursor:pointer">dismiss</button>`);
    if(!$("banner").classList.contains("show")) $("banner").classList.add("show");
  } else if(okEngine && !iso){
    console.warn("[boot] not crossOriginIsolated — WASM will run single-threaded. Use serve.py for threads.");
  }

/* friendly steps updater */
function updateSteps(){
  const hasModel = !!pipe || whistleReady;
  const hasText = SEG && SEG.length && SEG.some(s=> s.text && !s.pending && s.text.trim() && !s.text.startsWith('…'));
  const s1=document.getElementById('step1'), s2=document.getElementById('step2'), s3=document.getElementById('step3');
  if(!s1||!s2||!s3) return;
  s1.className = 'step ' + (hasModel? 'done':'active');
  s1.querySelector('.dot').innerHTML = hasModel? '<i class="ri-check-line"></i>' : '1';
  s2.className = 'step ' + (hasModel && !hasText ? 'active' : hasText ? 'done' : '');
  s2.querySelector('.dot').innerHTML = hasText? '<i class="ri-check-line"></i>' : '2';
  s3.className = 'step ' + (hasText ? 'active' : '');
  s3.querySelector('.dot').innerHTML = '3';
  const recCard=document.getElementById('recCard');
  if(recCard) recCard.classList.toggle('card--recording', false);
  if(typeof recording!=='undefined' && recording && recCard) recCard.classList.add('is-recording');
}
// hook into existing functions
const _origRenderTx = renderTx;
renderTx = function(){ _origRenderTx(); try{ updateSteps(); }catch(e){} };
const _origLoadWith = loadWith;
loadWith = async function(dtype,device,model){
  const r = await _origLoadWith(dtype,device,model);
  try{ updateSteps(); }catch(e){}
  return r;
};
setTimeout(updateSteps, 500);


/* custom selects + chunk + dialogs - overflow safe */
function initCustomSelects(){
  const ids=['selModel','selDtype','selDev'];
  ids.forEach(id=>{
    const native=document.getElementById(id);
    if(!native || native.dataset.csEnhanced) return;
    native.classList.add('cs-native');
    native.dataset.csEnhanced='1';
    const cs=document.createElement('div'); cs.className='cs'; cs.dataset.target=id;
    const trigger=document.createElement('button'); trigger.type='button'; trigger.className='cs-trigger'; trigger.setAttribute('aria-haspopup','listbox'); trigger.setAttribute('aria-expanded','false'); trigger.innerHTML='<span class="cs-value"></span><i class="ri-arrow-down-s-line cs-chevron"></i>';
    const list=document.createElement('div'); list.className='cs-list'; list.setAttribute('role','listbox'); list.hidden=true;
    Array.from(native.options).forEach(opt=>{
      const btn=document.createElement('button'); btn.type='button'; btn.className='cs-option'; btn.setAttribute('role','option'); btn.dataset.value=opt.value;
      const raw=opt.textContent.trim(); const parts=raw.split('·'); const main=parts[0].trim(); const hint=parts.slice(1).join('·').trim();
      btn.innerHTML= hint? `${main}<small>${hint}</small>` : main;
      if(opt.value===native.value) btn.classList.add('is-selected');
      btn.addEventListener('click', ()=>{ native.value=opt.value; native.dispatchEvent(new Event('change',{bubbles:true})); syncCustomSelect(id); closeAllCs(); trigger.focus(); });
      list.appendChild(btn);
    });
    function syncCustomSelect(targetId){
      const v=native.value; const opt=Array.from(native.options).find(o=>o.value===v); const valEl=cs.querySelector('.cs-value');
      if(opt && valEl){
        const raw=opt.textContent.trim(); const parts=raw.split('·'); const main=parts[0].trim(); const hint=parts.slice(1).join('·').trim();
        valEl.innerHTML= hint? `${main} <small style="opacity:.65;font-weight:400">· ${hint}</small>` : main;
      }
      cs.querySelectorAll('.cs-option').forEach(el=> el.classList.toggle('is-selected', el.dataset.value===v));
    }
    function closeAllCs(){ document.querySelectorAll('.cs-list').forEach(l=> l.hidden=true); document.querySelectorAll('.cs-trigger').forEach(b=> b.setAttribute('aria-expanded','false')); }
    trigger.addEventListener('click', (e)=>{ e.stopPropagation(); const isOpen=!list.hidden; closeAllCs(); if(!isOpen){ list.hidden=false; trigger.setAttribute('aria-expanded','true'); }});
    trigger.addEventListener('keydown', (e)=>{ if(e.key==='ArrowDown'||e.key==='Enter'||e.key===' '){ e.preventDefault(); list.hidden=false; trigger.setAttribute('aria-expanded','true'); (list.querySelector('.is-selected')||list.querySelector('.cs-option')).focus(); }});
    list.addEventListener('keydown', (e)=>{
      const opts=Array.from(list.querySelectorAll('.cs-option')); const idx=opts.indexOf(document.activeElement);
      if(e.key==='ArrowDown'){ e.preventDefault(); (opts[idx+1]||opts[0]).focus(); }
      else if(e.key==='ArrowUp'){ e.preventDefault(); (opts[idx-1]||opts[opts.length-1]).focus(); }
      else if(e.key==='Escape'){ e.preventDefault(); closeAllCs(); trigger.focus(); }
      else if(e.key==='Enter'){ e.preventDefault(); document.activeElement.click(); }
    });
    cs.appendChild(trigger); cs.appendChild(list); native.insertAdjacentElement('afterend', cs); syncCustomSelect(id);
    native.addEventListener('change', ()=> syncCustomSelect(id));
  });
  document.addEventListener('click', (e)=>{ if(!e.target.closest('.cs')){ document.querySelectorAll('.cs-list').forEach(l=> l.hidden=true); document.querySelectorAll('.cs-trigger').forEach(b=> b.setAttribute('aria-expanded','false')); }});
  // keep syncUI in sync
  if(window.syncUI && !window._csSyncPatched){
    const orig=window.syncUI; window._csSyncPatched=true;
    window.syncUI=function(){ orig(); ['selModel','selDtype','selDev'].forEach(sid=>{ const n=document.getElementById(sid); if(n){ const c=document.querySelector(`.cs[data-target="${sid}"]`); if(c){ const v=n.value; const opt=Array.from(n.options).find(o=>o.value===v); const valEl=c.querySelector('.cs-value'); if(opt&&valEl){ const raw=opt.textContent.trim(); const parts=raw.split('·'); const main=parts[0].trim(); const hint=parts.slice(1).join('·').trim(); valEl.innerHTML=hint? `${main} <small style="opacity:.65;font-weight:400">· ${hint}</small>` : main; c.querySelectorAll('.cs-option').forEach(el=> el.classList.toggle('is-selected', el.dataset.value===v)); } } } }); };
  }
}
/* The app asks with NebDialog; so does the rest of the web now. This page had
   its own overlay, its own escape handler and no focus trap -- NebUI.confirm is
   the same component the forum and the library use, so a destructive action
   looks and behaves the same wherever it is taken. */
function showCustomDialog({title='Confirm', message='', confirmText='Confirm', cancelText='Cancel', icon='', destructive=true}={}){
  if(!window.NebUI || !NebUI.confirm) return Promise.resolve(false);
  return NebUI.confirm({title, message, confirmLabel:confirmText, cancelLabel:cancelText, icon, destructive});
}
function patchHistoryDelete(){
  const hist=document.getElementById('hist');
  if(!hist || hist.dataset.patched) return; hist.dataset.patched='1';
  hist.addEventListener('click', async (e)=>{
    const delBtn=e.target.closest('.del'); if(!delBtn) return; e.preventDefault(); e.stopPropagation();
    const id=delBtn.dataset.del;
    const ok=await showCustomDialog({title:'Delete transcript?', message:'This will permanently remove this transcript from your device.', confirmText:'Delete', cancelText:'Cancel', icon:'delete'});
    if(!ok) return;
    try{ await Store.del('transcripts', +id); renderHist(); toast('Deleted','ok',1500);}catch(err){ toast('Delete failed: '+err.message,'err'); }
  }, true);
}
(function(){
  const hidden=document.getElementById('optChunk'), display=document.getElementById('chunkVal'), range=document.getElementById('chunkRange');
  if(hidden && display && range){
    function sync(val){ val=Math.max(10, Math.min(30, parseInt(val)||30)); hidden.value=val; display.textContent=val; range.value=val; hidden.dispatchEvent(new Event('change',{bubbles:true})); }
    document.querySelectorAll('.chunk-btn').forEach(btn=> btn.addEventListener('click', ()=> sync(parseInt(hidden.value)+(parseInt(btn.dataset.dir)))) );
    range.addEventListener('input', ()=> sync(range.value));
    const origSyncUI=window.syncUI;
    if(origSyncUI && !window._chunkSyncPatched2){
      window._chunkSyncPatched2=true;
      const prev=window.syncUI;
      window.syncUI=function(){ prev(); try{ const h=document.getElementById('optChunk'); const d=document.getElementById('chunkVal'); const r=document.getElementById('chunkRange'); if(h&&d&&r){ d.textContent=h.value; r.value=h.value; } }catch(e){} };
    }
    sync(hidden.value);
  }
})();
setTimeout(()=>{ try{ initCustomSelects(); patchHistoryDelete(); }catch(e){ console.warn(e); } }, 0);
setTimeout(()=>{
  const wipe=document.getElementById('btnWipe');
  if(wipe && !wipe.dataset.customPatched){
    wipe.dataset.customPatched='1';
    wipe.onclick = async ()=>{
      const ok=await showCustomDialog({title:'Clear cache?', message:'Delete all cached models? They will need to be downloaded again.', confirmText:'Clear cache', cancelText:'Cancel', icon:'cleaning_services'});
      if(!ok) return;
      try{ if(window.caches){ for(const n of await caches.keys()) await caches.delete(n); } const dlEl=document.getElementById('dl'); if(dlEl) dlEl.innerHTML=''; if(typeof dlRows!=='undefined') dlRows.clear(); pipe=null; pipeKey=''; try{killWhistle();}catch(_){} const mdl=document.getElementById('mdlTxt'); if(mdl) mdl.textContent='none'; S.badDev=null; try{await saveSettings();}catch(e){} const b=document.getElementById('banner'); if(b) b.classList.remove('show'); await updateCacheInfo(); toast('Cache cleared','ok'); }catch(e){ toast('Could not clear: '+e.message,'err'); }
    };
  }
}, 500);

console.log("WhisperWeb v1.4 ready — whistle-default+turbo+moonshine+distil+tools. engine:",!!TF,"gpu:",!!navigator.gpu,"isolated:",iso,"badDev:",S.badDev);
})();


/* ===== Extras: summarizer (on-device, superfast) ===== */
let sumPipe=null, sumLoading=false;
async function ensureSummarizer(){
  if(sumPipe) return sumPipe;
  if(sumLoading) return null;
  sumLoading=true;
  const st=document.getElementById('sumOut');
  if(st){ st.textContent='… loading summarizer (~80MB, first time only)…'; st.classList.add('show'); }
  toast('Loading summarizer …','',2600);
  try{
    configureWasmEnv('wasm');
    sumPipe = await TF.pipeline('summarization', 'Xenova/distilbart-cnn-6-6', {
      dtype:'q8', device:'wasm',
      progress_callback:(p)=>{ if(p.status) dlUI(p.file||'summarizer',p.status,p.loaded,p.total); }
    });
    toast('Summarizer ready','ok');
    return sumPipe;
  }catch(e){
    console.error(e); toast('Summarizer failed: '+e.message,'err',5000);
    if(st) st.textContent='Summarizer failed: '+e.message;
    return null;
  }finally{ sumLoading=false; }
}
async function doSummarize(){
  const text=SEG.map(s=>s.text).join(' ').trim();
  const st=document.getElementById('sumOut');
  const btn=document.getElementById('btnSumCopy');
  const clr=document.getElementById('btnSumClear');
  if(!text || text.split(/\s+/).length < 40){
    toast('Need ≥40 words to summarize','warn'); return;
  }
  if(st){ st.textContent='… summarizing on-device …'; st.classList.add('show'); }
  const pipe = await ensureSummarizer(); if(!pipe) return;
  try{
    const out = await pipe(text, { max_new_tokens:130, min_length:30 });
    const sum = (Array.isArray(out)? out[0].summary_text : out.summary_text) || JSON.stringify(out);
    if(st) st.textContent = sum;
    if(btn) btn.style.display='inline-flex';
    if(clr) clr.style.display='inline-flex';
    toast('Summary done','ok');
  }catch(e){
    console.error(e); toast('Summarize failed: '+e.message,'err',5000);
    if(st) st.textContent='Summarize failed: '+e.message;
  }
}
const _btnSum=document.getElementById('btnSummarize'); if(_btnSum) _btnSum.onclick=doSummarize;
const _btnSumCopy=document.getElementById('btnSumCopy'); if(_btnSumCopy) _btnSumCopy.onclick=async()=>{
  const st=document.getElementById('sumOut');
  try{ await navigator.clipboard.writeText(st.textContent); toast('Summary copied','ok',1500);}catch(e){ toast('Clipboard blocked','warn');}
};
const _btnSumClear=document.getElementById('btnSumClear'); if(_btnSumClear) _btnSumClear.onclick=()=>{
  const st=document.getElementById('sumOut'); if(st){ st.textContent=''; st.classList.remove('show'); }
  _btnSumClear.style.display='none'; const b=document.getElementById('btnSumCopy'); if(b) b.style.display='none';
};

/* ===== Extras: sentiment (superfast 67MB) + keywords (0MB) + embeddings (22MB) + TTS ===== */
let sentiPipe=null, sentiLoading=false;
async function ensureSentiment(){
  if(sentiPipe) return sentiPipe;
  if(sentiLoading) return null;
  sentiLoading=true;
  const out=document.getElementById('toolOut');
  if(out){ out.style.display='block'; out.textContent='… loading sentiment (67MB, first time)…'; out.classList.add('show'); }
  toast('Loading sentiment…','',2600);
  try{
    configureWasmEnv('wasm');
    sentiPipe = await TF.pipeline('sentiment-analysis', 'Xenova/distilbert-base-uncased-finetuned-sst-2-english', {
      dtype:'q8', device:'wasm',
      progress_callback:(p)=>{ if(p.status) dlUI(p.file||'sentiment',p.status,p.loaded,p.total); }
    });
    toast('Sentiment ready','ok');
    return sentiPipe;
  }catch(e){ console.error(e); toast('Sentiment failed: '+e.message,'err',5000); if(out) out.textContent='Sentiment failed: '+e.message; return null;}
  finally{ sentiLoading=false; }
}
async function doSentiment(){
  const text=SEG.map(s=>s.text).join(' ').trim();
  const out=document.getElementById('toolOut');
  if(!text || text.split(/\s+/).length < 3){ toast('Need some transcript first','warn'); return; }
  if(out){ out.style.display='block'; out.textContent='… analyzing sentiment on-device …'; out.classList.add('show'); }
  const pipe=await ensureSentiment(); if(!pipe) return;
  try{
    // chunk long text for BERT 512 tokens
    const chunks=text.match(/[^.!?]+[.!?]+|[^.!?]+$/g)||[text];
    let pos=0, neg=0, neu=0;
    for(let i=0;i<Math.min(chunks.length, 8); i++){
      const r=await pipe(chunks[i].slice(0,500));
      const arr=Array.isArray(r)?r:[r];
      for(const s of arr){
        const l=(s.label||'').toLowerCase();
        const sc=s.score||0;
        if(l.includes('pos')) pos+=sc;
        else if(l.includes('neg')) neg+=sc;
        else neu+=sc;
      }
    }
    const tot=pos+neg+neu||1;
    const pP=(pos/tot*100).toFixed(1), pN=(neg/tot*100).toFixed(1);
    let label= pos>neg ? 'POSITIVE' : neg>pos ? 'NEGATIVE' : 'NEUTRAL';
    let emoji = label==='POSITIVE' ? '😊' : label==='NEGATIVE' ? '😟' : '😐';
    if(out) out.textContent = `${emoji} ${label} — positive ${pP}% / negative ${pN}%  (${chunks.length} sentences, on-device)`;
    toast('Sentiment done','ok');
  }catch(e){ console.error(e); toast('Sentiment failed: '+e.message,'err',5000); if(out) out.textContent='Sentiment failed: '+e.message; }
}
let embedPipe=null, embedLoading=false, embedCache=null;
async function ensureEmbed(){
  if(embedPipe) return embedPipe;
  if(embedLoading) return null;
  embedLoading=true;
  const out=document.getElementById('toolOut');
  if(out){ out.style.display='block'; out.textContent='… loading embeddings (22MB, first time)…'; out.classList.add('show'); }
  toast('Loading embeddings…','',2600);
  try{
    configureWasmEnv('wasm');
    embedPipe = await TF.pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', {
      dtype:'q8', device:'wasm',
      progress_callback:(p)=>{ if(p.status) dlUI(p.file||'embed',p.status,p.loaded,p.total); }
    });
    toast('Embeddings ready','ok');
    return embedPipe;
  }catch(e){ console.error(e); toast('Embeddings failed: '+e.message,'err',5000); if(out) out.textContent='Embeddings failed: '+e.message; return null;}
  finally{ embedLoading=false; }
}
function cosine(a,b){
  let dot=0, na=0, nb=0;
  for(let i=0;i<a.length;i++){ dot+=a[i]*b[i]; na+=a[i]*a[i]; nb+=b[i]*b[i]; }
  return dot/(Math.sqrt(na)*Math.sqrt(nb)+1e-9);
}
async function doEmbed(){
  const text=SEG.map(s=>s.text).join(' ').trim();
  const out=document.getElementById('toolOut');
  const box=document.getElementById('embedBox');
  if(!text){ toast('No transcript to embed','warn'); return; }
  if(out){ out.style.display='block'; out.textContent='… embedding transcript (22MB) …'; out.classList.add('show'); }
  const pipe=await ensureEmbed(); if(!pipe) return;
  try{
    const sents=text.match(/[^.!?]+[.!?]+|[^.!?]+$/g)||[text];
    const toEmbed=sents.slice(0,24).map(s=>s.trim()).filter(Boolean);
    const embs=[];
    for(const s of toEmbed){
      const e=await pipe(s, {pooling:'mean', normalize:true});
      embs.push(Array.from(e.data || e[0]?.data || e));
    }
    embedCache={sents:toEmbed, embs};
    if(out) out.textContent=`✅ Embedded ${toEmbed.length} sentences — type a query below and hit Find (cosine).`;
    if(box) box.style.display='block';
    toast('Embeddings ready — search below','ok');
  }catch(e){ console.error(e); toast('Embed failed: '+e.message,'err',5000); if(out) out.textContent='Embed failed: '+e.message; }
}
async function doEmbedSearch(){
  const q=document.getElementById('embedQuery')?.value.trim();
  const res=document.getElementById('embedRes');
  if(!q){ toast('Type a query','warn'); return; }
  if(!embedCache){ toast('Click Embed first','warn'); return; }
  const pipe=await ensureEmbed(); if(!pipe) return;
  try{
    const qe=await pipe(q, {pooling:'mean', normalize:true});
    const qv=Array.from(qe.data || qe[0]?.data || qe);
    const scored=embedCache.embs.map((e,i)=>({i, score:cosine(qv,e), txt:embedCache.sents[i]}))
      .sort((a,b)=>b.score-a.score).slice(0,5);
    if(res) res.innerHTML=scored.map((s,idx)=> `<div style="padding:6px 8px;border:1px solid var(--border-line);border-radius:8px;margin-bottom:6px;background:var(--bg-elevated)"><b style="color:var(--text-primary)">#${idx+1} ${(s.score*100).toFixed(1)}%</b> — ${escapeHtml(s.txt)}</div>`).join('') || '<span class="hint">No match</span>';
    toast('Search done','ok',2000);
  }catch(e){ console.error(e); toast('Search failed: '+e.message,'err',5000); }
}
function doKeywords(){
  const text=SEG.map(s=>s.text).join(' ').toLowerCase();
  const out=document.getElementById('toolOut');
  if(!text.trim()){ toast('No transcript','warn'); return; }
  const stop=new Set(['the','a','an','and','or','but','in','on','at','to','for','of','with','is','are','was','were','be','been','being','have','has','had','do','does','did','will','would','could','should','this','that','these','those','it','its','as','by','from','up','out','about','into','over','after','before','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','can','just','don','should','now','i','you','he','she','we','they','me','him','her','us','them','my','your','his','our','their']);
  const words=text.replace(/[^a-z0-9\s]/g,' ').split(/\s+/).filter(w=>w.length>2 && !stop.has(w));
  const freq={};
  for(const w of words) freq[w]=(freq[w]||0)+1;
  const sorted=Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0,12);
  if(sorted.length===0){ if(out){ out.style.display='block'; out.textContent='No keywords found'; out.classList.add('show'); } return; }
  const max=sorted[0][1];
  if(out){
    out.style.display='block';
    out.classList.add('show');
    out.innerHTML=`<b>Top keywords (TF-IDF lite, on-device, 0MB):</b><br>` + sorted.map(([w,c])=> `<span style="display:inline-block;margin:4px 6px 0 0;padding:4px 8px;border:1px solid var(--border-line);border-radius:9999px;background:var(--bg-elevated);font-family:var(--font-mono);font-size:0.78rem">${escapeHtml(w)} <small style="opacity:.6">×${c}</small> <span style="display:inline-block;width:${Math.max(8, c/max*48)}px;height:4px;background:var(--text-primary);border-radius:999px;vertical-align:middle;margin-left:4px"></span></span>`).join('');
  }
  toast('Keywords done','ok',2000);
}
// wire extras tools (TTS now separate page: tts.html)
const _btnSenti=document.getElementById('btnSentiment'); if(_btnSenti) _btnSenti.onclick=doSentiment;
const _btnKw=document.getElementById('btnKeywords'); if(_btnKw) _btnKw.onclick=doKeywords;
const _btnEmb=document.getElementById('btnEmbed'); if(_btnEmb) _btnEmb.onclick=doEmbed;
const _btnEmbGo=document.getElementById('btnEmbedGo'); if(_btnEmbGo) _btnEmbGo.onclick=doEmbedSearch;
const _embedQ=document.getElementById('embedQuery'); if(_embedQ) _embedQ.addEventListener('keydown', e=>{ if(e.key==='Enter') doEmbedSearch(); });

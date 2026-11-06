import { KokoroTTS, TextSplitterStream } from "https://esm.sh/kokoro-js@1.2.1?bundle";
import * as transformers from "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.5.1/dist/transformers.min.js";

// --- suppress harmless VITS logs: content-length (Xet) & preprocessor 404 (MMS has no preprocessor) ---
const _origWarn = console.warn;
const _origError = console.error;
console.warn = (...a)=>{
  const m=String(a[0]||"");
  if(m.includes("Unable to determine content-length") || m.includes("preprocessor_config.json")) return;
  _origWarn.apply(console,a);
};
console.error = (...a)=>{
  const m=String(a[0]||"");
  if(m.includes("preprocessor_config.json") || m.includes("No `image_processor_type`")) return;
  _origError.apply(console,a);
};
// Intercept MMS preprocessor fetch: return synthetic 404 so pipeline skips it without network error log
const _origFetch = window.fetch.bind(window);
window.fetch = async (url, opts)=>{
  if(typeof url==="string" && url.includes("preprocessor_config.json") && url.includes("mms-tts")){
    // synthetic 404: pipeline handles as "no preprocessor" (VITS doesn't need it)
    return new Response('', {status:404, statusText:'Not Found'});
  }
  return _origFetch(url, opts);
};

const CDN_TTS = "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3";
const $ = (id)=>document.getElementById(id);
const now=()=>performance.now();
const fmtMB=(b)=>(b/1048576).toFixed(1);
function toast(msg,kind="",ms=3400){
  const lower=String(msg).toLowerCase();
  if(lower.includes("voice") && (lower.includes("updated") || lower.includes("single-voice model"))) return;
  const t=document.createElement("div"); t.className="toast "+kind; t.innerHTML=msg; $("toasts").appendChild(t); setTimeout(()=>{t.style.opacity="0";t.style.transition="opacity .3s";setTimeout(()=>t.remove(),320)},ms);
}
function banner(html){ const b=$("banner"); if(!html){b.classList.remove("show");return;} b.innerHTML=html; b.classList.add("show"); }
function escapeHtml(s){ return s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }

// storage for TTS history (IndexedDB)
const Store = (() => {
  let db=null, mem={tts:[],kv:{}}, idbOK=true;
  function open(){
    return new Promise((res)=>{
      try{
        const rq=indexedDB.open("whisperweb-tts",1);
        rq.onupgradeneeded=()=>{ const d=rq.result;
          if(!d.objectStoreNames.contains("tts")) d.createObjectStore("tts",{keyPath:"id",autoIncrement:true});
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
    async put(st,val){ if(!idbOK){ if(st==="kv") Object.assign(mem.kv,val); else mem.tts.push(val); return; }
      return new Promise((res,rej)=>{const r=tx(st,"readwrite").put(val);r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)}) },
    async all(st){ if(!idbOK) return st==="kv"?[mem.kv]:mem.tts.slice().reverse();
      return new Promise((res,rej)=>{const r=tx(st,"readonly").getAll();r.onsuccess=()=>res(st==="kv"?[r.result[0]||{}]:r.result.reverse());r.onerror=()=>rej(r.error)}) },
    async del(st,key){ if(!idbOK){ if(st!=="kv"){const i=mem.tts.findIndex(x=>x.id===key); if(i>=0)mem.tts.splice(i,1);} return; }
      return new Promise((res,rej)=>{const r=tx(st,"readwrite").delete(key);r.onsuccess=()=>res();r.onerror=()=>rej(r.error)}) },
    async clear(st){ if(!idbOK){ mem.tts=[]; return; } return new Promise((res,rej)=>{const r=tx(st,"readwrite").clear();r.onsuccess=()=>res();r.onerror=()=>rej(r.error)}) },
  };
})();

const S = { model:"onnx-community/Kokoro-82M-v1.0-ONNX", dtype:"q8", dev:"wasm", voice:"af_heart", speed:1.0, stream:true };
async function loadSettings(){
  try{
    const [kv]=await Store.all("kv"); if(kv) Object.assign(S,kv);
    if(!S.model) S.model="onnx-community/Kokoro-82M-v1.0-ONNX";
    if(!S.dtype) S.dtype="q8";
    if(!S.voice) S.voice="af_heart";
    if(!S.speed) S.speed=1.0;
  }catch(e){}
  syncUI();
}
async function saveSettings(){ try{ await Store.put("kv", {...S}); }catch(e){} }
function syncUI(){
  const m=$("selModel"); if(m){ const v=S.model+"|"+S.dtype; let found=false; for(const o of m.options) if(o.value===v) found=true; if(found) m.value=v; else { const base=S.model; for(const o of m.options) if(o.value.startsWith(base)) {m.value=o.value; break;} } }
  const d=$("selDtype"); if(d) d.value=S.dtype;
  const dv=$("selDev"); if(dv) dv.value=S.dev;
  const vv=$("selVoice"); if(vv) vv.value=S.voice;
  const sr=$("speedRange"); if(sr) sr.value=S.speed;
  const sv=$("speedVal"); if(sv) sv.textContent=S.speed.toFixed(2);
  const os=$("optStream"); if(os) os.checked=S.stream;
}

// engine
let kokoro=null, pipeTTS=null, pipeKey="", curDev="wasm";
const dlRows=new Map();
function withTimeout(p,ms,label){ return new Promise((res,rej)=>{ const t=setTimeout(()=>rej(Object.assign(new Error(label+" timed out after "+Math.round(ms/1000)+"s"),{timedOut:true})),ms); p.then(v=>{clearTimeout(t);res(v)},e=>{clearTimeout(t);rej(e)}); }); }
function isIsolated(){ try{ return !!self.crossOriginIsolated; }catch(e){ return false; } }
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
    $("cacheTxt").textContent = shown ? fmtMB(shown)+" MB" : (bytes?"~":"·");
    $("cacheTag").textContent = shown ? fmtMB(shown)+" MB stored" : "";
  }catch(e){ $("cacheTxt").textContent="n/a"; }
}

async function loadKokoro(modelId, dtype, device){
  const key=modelId+"|"+dtype+"|"+device;
  if(kokoro && pipeKey===key) return kokoro;
  if(kokoro){ try{ kokoro=null; }catch(e){} }
  $("btnLoad").disabled=true; $("btnLoad").innerHTML=`<span class="spin"></span>&nbsp; loading`;
  $("dlStatus").innerHTML=`<b>${modelId.split("/").pop()}</b> · ${dtype} · ${device}: fetching…`;
  $("mdlTxt").textContent=modelId.split("/").pop()+" "+dtype;
  $("devTxt").textContent = device==="webgpu" ? "WebGPU…" : "WASM (CPU)…";
  try{
    // kokoro-js uses transformers env under hood; set wasm proxy
    kokoro = await KokoroTTS.from_pretrained(modelId, {
      dtype,
      device: device==="auto" ? (isIsolated()?"wasm":"wasm") : device,
      progress_callback:(p)=>{ if(p.status) dlUI(p.file||"kokoro",p.status,p.loaded,p.total); }
    });
    pipeKey=key; curDev=device;
    $("devTxt").textContent = device==="webgpu" ? "WebGPU ⚡" : (isIsolated()?"WASM ⚡ (threads)":"WASM (CPU)");
    $("dlStatus").innerHTML=`✅ <b>${modelId.split("/").pop()}</b> (${dtype}, ${device}) ready: cached`;
    $("btnLoad").innerHTML="✓ TTS ready: reload / switch";
    updateCacheInfo();
    return kokoro;
  }catch(e){
    kokoro=null; pipeKey="";
    throw e;
  }finally{
    $("btnLoad").disabled=false;
    if(!$("btnLoad").innerHTML.includes("ready")) $("btnLoad").innerHTML="⤓ Download / load TTS";
  }
}

async function loadMMS(modelId){
  const key=modelId+"|mms";
  if(pipeTTS && pipeKey===key) return pipeTTS;
  $("btnLoad").disabled=true; $("btnLoad").innerHTML=`<span class="spin"></span>&nbsp; loading`;
  $("dlStatus").innerHTML=`<b>${modelId.split("/").pop()}</b>: fetching…`;
  $("mdlTxt").textContent=modelId.split("/").pop();
  const dtypeSel = $("selDtype")?.value || "q8";
  try{
    const { pipeline, env } = transformers;
    env.allowLocalModels=false; env.useBrowserCache=true;
    // VITS/MMS models are tiny (38MB q8): use q8 for superfast, fp32 for exact
    // preprocessor_config.json 404 is expected for VITS (no preprocessor): pipeline handles it internally
    pipeTTS = await pipeline('text-to-speech', modelId, {
      dtype: dtypeSel==="fp16"?"fp32":dtypeSel,
      device: $("selDev").value==="webgpu" ? "webgpu" : "wasm",
      progress_callback:(p)=>{ if(p.status) dlUI(p.file||"mms",p.status,p.loaded,p.total); }
    });
    pipeKey=key;
    $("dlStatus").innerHTML=`✅ <b>${modelId.split("/").pop()}</b> ready: try Generate below`;
    $("btnLoad").innerHTML="✓ TTS ready";
    return pipeTTS;
  }catch(e){
    const msg=String(e?.message||e);
    if(msg.includes("image_processor_type") || msg.includes("feature_extractor_type")){
      console.warn("MMS VITS preprocessor missing is expected: trying manual VITS load", e);
      try{
        const { AutoTokenizer, VitsModel } = transformers;
        const tokenizer = await AutoTokenizer.from_pretrained(modelId, {progress_callback:(p)=>{ if(p.status) dlUI(p.file||"tok",p.status,p.loaded,p.total); }});
        const model = await VitsModel.from_pretrained(modelId, {dtype: dtypeSel==="fp16"?"fp32":dtypeSel, device: $("selDev").value==="webgpu" ? "webgpu" : "wasm", progress_callback:(p)=>{ if(p.status) dlUI(p.file||"vits",p.status,p.loaded,p.total); }});
        pipeTTS = async (text)=>{
          const inputs = tokenizer(text, {padding:true, truncation:true});
          const { waveform } = await model(inputs);
          const audio = waveform.data || waveform;
          const sr = model.config.sampling_rate || 16000;
          return {audio, sampling_rate: sr};
        };
        pipeKey=key;
        $("dlStatus").innerHTML=`✅ <b>${modelId.split("/").pop()}</b> ready (manual VITS)`;
        $("btnLoad").innerHTML="✓ TTS ready";
        return pipeTTS;
      }catch(e2){
        console.error("Manual VITS fallback also failed", e2);
      }
    }
    pipeTTS=null; pipeKey=""; throw e;
  }
  finally{ $("btnLoad").disabled=false; if(!$("btnLoad").innerHTML.includes("ready")) $("btnLoad").innerHTML="⤓ Download / load TTS"; }
}

let tinyPipe=null;
async function loadTinyTTS(){
  // TinyTTS 1.6M is Node-only (onnxruntime-node + fs): not browser-runnable via esm.sh.
  // We keep the option visible as "ultralight amazing" but fallback to Kokoro q4f16 (70MB) which is the tiny browser alternative.
  // If you need true 3.4MB in browser, use Kokoro q4f16 or MMS 38MB.
  toast("TinyTTS 1.6M is Node-only: using Kokoro q4f16 70MB tiny fallback (browser)","warn",5000);
  return await loadKokoro("onnx-community/Kokoro-82M-v1.0-ONNX", "q4f16", $("selDev").value || S.dev);
}
async function ensureTTS(){
  const raw=$("selModel").value;
  const [modelId, dtypeSel] = raw.split("|");
  const dtype = $("selDtype")?.value || dtypeSel || S.dtype;
  const dev = $("selDev").value;
  const isKokoro = modelId.includes("Kokoro");
  const isTiny = modelId.includes("tiny-tts");
  const isParler = modelId.includes("parler");
  const isOute = modelId.includes("OuteTTS");
  if(isTiny){
    return await loadTinyTTS();
  } else if(isKokoro){
    return await loadKokoro(modelId, dtype, dev);
  } else if(isParler || isOute){
    // Parler/OuteTTS are large (880M-500M) and not yet fully optimized for browser ONNX;
    // try transformers pipeline but warn about size
    toast("Parler/OuteTTS is large: may need 2GB+ RAM, trying…","warn",4000);
    return await loadMMS(modelId);
  } else {
    return await loadMMS(modelId);
  }
}

// TTS generation
let currentAudio=null, currentBlob=null, abortGen=0;
function setAudio(blob, meta){
  currentBlob=blob;
  const url=URL.createObjectURL(blob);
  const el=$("audioEl");
  const ph=$("audioPh");
  if(el){
    el.src=url;
    el.style.display="block";
    el.play().catch(()=>{});
  }
  if(ph) ph.style.display="none";
  $("btnDownload").disabled=false;
  $("btnCopyText").disabled=false;
  $("btnStop").disabled=false;
  $("audioMeta").textContent = meta || "";
  $("stModel").textContent = (S.model.split("/").pop()||"·");
  $("stVoice").textContent = S.voice;
  $("stSpeed").textContent = S.speed.toFixed(2)+"×";
}

async function doGenerate(streaming=false){
  const text=$("ttsText").value.trim();
  if(!text){ toast("Type some text first","warn"); return; }
  if(text.length>2000){ toast("Long text: streaming will chunk it","",3000); streaming=true; }
  const voice=$("selVoice").value;
  const speed=parseFloat($("speedRange").value)||1.0;
  S.voice=voice; S.speed=speed; S.stream=streaming; await saveSettings();
  const btn=$("btnGenerate"), st=$("genStatus"), meta=$("audioMeta");
  if(btn) btn.disabled=true;
  if(st) st.innerHTML=`<b>Generating…</b> ${streaming?"streaming":""} ${voice} ${speed.toFixed(2)}×`;
  $("streamOut").style.display = streaming ? "flex" : "none";
  $("streamOut").innerHTML="";
  const t0=now();
  const myRun=++abortGen;
  try{
    const tts=await ensureTTS();
    if(myRun!==abortGen) return;
    if(!tts) throw new Error("TTS not loaded");
    const rawSel=$("selModel").value;
    const isKokoro = rawSel.includes("Kokoro") || rawSel.includes("tiny-tts");
    // tiny-tts is Node-only: we already fallback to Kokoro q4f16 in loadTinyTTS, so treat as Kokoro
    if(isKokoro && streaming){
      const splitter=new TextSplitterStream();
      const stream=tts.stream(splitter);
      const chunks=[];
      let idx=0;
      (async()=>{
        for await(const {text, phonemes, audio} of stream){
          if(myRun!==abortGen) break;
          const blob=audioToWavBlob(audio.audio || audio, audio.sampling_rate || 24000);
          chunks.push(blob);
          const div=document.createElement("div");
          div.style.cssText="padding:8px 10px;border:1px solid var(--border-line);border-radius:10px;background:var(--bg-elevated);font-family:var(--font-mono);font-size:0.76rem";
          div.innerHTML=`<b style="color:var(--text-primary)">#${++idx}</b> ${escapeHtml(text.slice(0,80))} <small style="color:var(--text-muted)">${(blob.size/1024).toFixed(0)}KB</small> <audio controls src="${URL.createObjectURL(blob)}" style="width:100%;margin-top:6px"></audio>`;
          $("streamOut").appendChild(div);
          // also set main audio to latest chunk for quick preview
          setAudio(blob, `chunk ${idx} · ${voice}`);
        }
        if(chunks.length){
          // merge all chunks into one wav for download
          const merged=await mergeWavs(chunks);
          setAudio(merged, `streamed ${chunks.length} chunks · ${((now()-t0)/1000).toFixed(1)}s`);
          saveHistory(text, merged, voice, `kokoro-${S.dtype} streamed`);
        }
      })();
      // push text
      const tokens=text.match(/\s*\S+/g) || [text];
      for(const tok of tokens){
        splitter.push(tok);
        await new Promise(r=>setTimeout(r, 5));
        if(myRun!==abortGen) break;
      }
      splitter.close();
      // wait a bit for stream to finish
      await new Promise(r=>setTimeout(r, 600));
    } else if(isKokoro){
      const out=await withTimeout(tts.generate(text, {voice, speed}), 60000, "tts generate");
      if(myRun!==abortGen) return;
      const wav=out.audio || out;
      const sr=out.sampling_rate || 24000;
      const blob=audioToWavBlob(wav, sr);
      setAudio(blob, `${voice} · ${(blob.size/1024).toFixed(0)}KB · ${((now()-t0)/1000).toFixed(1)}s`);
      saveHistory(text, blob, voice, `kokoro-${S.dtype}`);
    } else {
      // MMS / speecht5 via transformers pipeline
      const pipe=tts; // already loaded
      const out=await withTimeout(pipe(text), 60000, "tts generate");
      const wav=out.audio;
      const sr=out.sampling_rate || 16000;
      const blob=audioToWavBlob(wav, sr);
      setAudio(blob, `${S.model.split("/").pop()} · ${((now()-t0)/1000).toFixed(1)}s`);
      saveHistory(text, blob, voice, S.model);
    }
    $("timingHint").textContent = `${((now()-t0)/1000).toFixed(2)}s generate`;
    $("stTime").textContent = `${((now()-t0)/1000).toFixed(1)}s`;
    toast("Done","ok");
  }catch(e){
    console.error(e);
    toast("TTS failed: "+(e.message||e),"err",5000);
    $("genStatus").innerHTML=`<span style="color:#ef4444">Failed: ${escapeHtml(e.message||String(e))}</span>`;
  }finally{
    if(btn) btn.disabled=false;
  }
}

function audioToWavBlob(float32, sr){
  // float32 is Float32Array or AudioData
  let data=float32;
  if(data instanceof Float32Array) {}
  else if(data && data.data) data=data.data;
  else if(Array.isArray(data)) data=new Float32Array(data);
  const len=data.length;
  const buf=new ArrayBuffer(44+len*2);
  const view=new DataView(buf);
  function writeStr(off, s){ for(let i=0;i<s.length;i++) view.setUint8(off+i, s.charCodeAt(i)); }
  writeStr(0,"RIFF"); view.setUint32(4,36+len*2,true); writeStr(8,"WAVE"); writeStr(12,"fmt "); view.setUint32(16,16,true); view.setUint16(20,1,true); view.setUint16(22,1,true); view.setUint32(24,sr,true); view.setUint32(28,sr*2,true); view.setUint16(32,2,true); view.setUint16(34,16,true); writeStr(36,"data"); view.setUint32(40,len*2,true);
  let off=44;
  for(let i=0;i<len;i++){ const s=Math.max(-1,Math.min(1,data[i])); view.setInt16(off, s<0? s*0x8000 : s*0x7FFF, true); off+=2; }
  return new Blob([view],{type:"audio/wav"});
}
async function mergeWavs(blobs){
  // simple concat by decoding and re-encoding as wav (approx, just concat PCM)
  // decode each wav blob to pcm via AudioContext would be async; simpler: just return last blob for now + note
  // For proper merge, we decode via fetch+AudioContext if needed, but for TTS we can just concat via Blob with wav headers? Simpler: create new Float32Array by decoding each blob's pcm
  // We'll decode via AudioContext quickly
  try{
    const ctx=new (window.AudioContext||window.webkitAudioContext)({sampleRate:24000});
    let total=0;
    const datas=[];
    for(const b of blobs){
      const ab=await b.arrayBuffer();
      const view=new DataView(ab);
      // skip 44 header, read int16
      const len=(ab.byteLength-44)/2;
      const arr=new Float32Array(len);
      for(let i=0;i<len;i++) arr[i]=view.getInt16(44+i*2,true)/0x7FFF;
      datas.push(arr); total+=len;
    }
    const merged=new Float32Array(total);
    let off=0; for(const d of datas){ merged.set(d,off); off+=d.length; }
    await ctx.close();
    return audioToWavBlob(merged,24000);
  }catch(e){ return blobs[blobs.length-1]; }
}

async function saveHistory(text, blob, voice, model){
  try{
    const id=Date.now();
    // store blob as base64? IndexedDB can store Blob directly
    await Store.put("tts", {createdAt:id, text:text.slice(0,200), fullText:text, voice, model, blob, size:blob.size});
    renderHist();
  }catch(e){ console.warn(e); }
}
async function renderHist(){
  try{
    const items=await Store.all("tts");
    const h=$("hist");
    if(!items.length){h.innerHTML='<div class="hint">No TTS yet: generate some audio.</div>';return;}
    h.innerHTML=items.slice(0,20).map(it=>{
      const time=new Date(it.createdAt).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
      const kb=(it.size/1024|0)+"KB";
      const modelName=escapeHtml((it.model||"").split("/").pop()||"tts");
      let voiceLabel=escapeHtml(it.voice||"");
      if(voiceLabel==="en_default") voiceLabel="English";
      else if(voiceLabel==="hi_default") voiceLabel="Hindi";
      else if(voiceLabel==="default") voiceLabel="";
      const isDup = !voiceLabel || modelName.toLowerCase()===voiceLabel.toLowerCase();
      const txt=escapeHtml(it.text||it.fullText||"");
      // clean top: time left, size right; meta: model · voice (no duplicate)
      return `
      <div class="hitem" data-id="${it.id}" style="cursor:pointer">
        <div class="top"><span style="font-size:12.5px;font-weight:600;letter-spacing:-0.01em">${time}</span><span class="when">${kb}</span></div>
        <div class="txt">${txt}</div>
        <div class="meta">${isDup?modelName:`${modelName} <span style="opacity:.6">·</span> ${voiceLabel}`}</div>
      </div>`;
    }).join("");
    h.querySelectorAll(".hitem").forEach(el=>el.onclick=async()=>{
      const id=+el.dataset.id;
      const all=await Store.all("tts");
      const it=all.find(x=>x.id===id); if(!it) return;
      if(it.blob){
        setAudio(it.blob, `history · ${it.voice}`);
        $("ttsText").value=it.fullText||it.text;
        $("charCount").textContent=(it.fullText||"").length+" chars";
      }
    });
  }catch(e){}
}

// voice options per model: updates selVoice when model changes (fixes "voice remains same")
const VOICE_OPTS = {
  kokoro: [
    {value:"af_heart", text:"af_heart · Heart · American Female ★"},
    {value:"af_bella", text:"af_bella · Bella · American Female 🔥"},
    {value:"af_sky", text:"af_sky · Sky · American Female"},
    {value:"af_nicole", text:"af_nicole · Nicole · American Female 🎧"},
    {value:"af_sarah", text:"af_sarah · Sarah · American Female"},
    {value:"am_adam", text:"am_adam · Adam · American Male"},
    {value:"am_michael", text:"am_michael · Michael · American Male"},
    {value:"bf_emma", text:"bf_emma · Emma · British Female 🚺"},
    {value:"bf_isabella", text:"bf_isabella · Isabella · British Female"},
    {value:"bm_george", text:"bm_george · George · British Male"},
    {value:"bm_lewis", text:"bm_lewis · Lewis · British Male"},
  ],
  "mms-tts-eng": [{value:"en_default", text:"English · Default (single voice)"}],
  "mms-tts-hin": [{value:"hi_default", text:"Hindi · Default (single voice)"}],
  "speecht5": [{value:"speecht5", text:"speecht5 · Default (needs speaker embeddings)"}],
  "tiny-tts": [{value:"MALE", text:"MALE · Male voice"}, {value:"FEMALE", text:"FEMALE · Female voice"}],
  "outetts": [{value:"outetts", text:"OuteTTS · Default (prompt cloned)"}],
  "parler": [{value:"parler", text:"parler · Default (prompt cloned)"}],
  "default": [{value:"default", text:"Default · single voice"}],
};
function getVoiceKey(modelId){
  if(modelId.includes("Kokoro")) return "kokoro";
  if(modelId.includes("mms-tts-eng")) return "mms-tts-eng";
  if(modelId.includes("mms-tts-hin")) return "mms-tts-hin";
  if(modelId.includes("speecht5")) return "speecht5";
  if(modelId.includes("tiny-tts")) return "tiny-tts";
  if(modelId.includes("OuteTTS")) return "outetts";
  if(modelId.includes("parler")) return "parler";
  return "default";
}
function rebuildVoiceCustomSelect(){
  const native=document.getElementById("selVoice");
  if(!native) return;
  // remove old custom UI
  const oldCs=document.querySelector('.cs[data-target="selVoice"]');
  if(oldCs) oldCs.remove();
  delete native.dataset.csEnhanced;
  native.classList.remove("cs-native");
  // re-init just this one
  initCustomSelects();
  // ensure sync
  if(window.syncUI) syncUI();
}
function updateVoiceOptionsForModel(modelId){
  const key=getVoiceKey(modelId);
  const opts=VOICE_OPTS[key] || VOICE_OPTS["default"];
  const sel=$("selVoice");
  if(!sel) return;
  const prev=sel.value;
  sel.innerHTML="";
  for(const o of opts){
    const opt=document.createElement("option");
    opt.value=o.value;
    opt.textContent=o.text;
    sel.appendChild(opt);
  }
  // keep previous if still valid, else first
  const valid=opts.some(o=>o.value===prev);
  sel.value = valid ? prev : opts[0].value;
  S.voice=sel.value;
  saveSettings();
  rebuildVoiceCustomSelect();
  // disable voice selector for single-voice models (hint)
  const single = opts.length===1;
  sel.disabled=single;
  const cs=document.querySelector('.cs[data-target="selVoice"] .cs-trigger');
  if(cs){ cs.style.opacity= single ? "0.6" : "1"; cs.style.pointerEvents= single ? "none" : "auto"; }
  // Single-voice models keep the selector disabled; availability is shown inline.
}

// UI wiring
$("btnLoad").onclick=()=>ensureTTS();
$("selModel").onchange=async (e)=>{ const v=e.target.value; const [m,d]=v.split("|"); S.model=m; S.dtype=d||S.dtype; await saveSettings(); syncUI(); updateVoiceOptionsForModel(m); };
$("selDtype").onchange=async (e)=>{ S.dtype=e.target.value; await saveSettings(); };
$("selDev").onchange=async (e)=>{ S.dev=e.target.value; await saveSettings(); };
$("selVoice").onchange=async (e)=>{ S.voice=e.target.value; await saveSettings(); };
$("speedRange").oninput=(e)=>{ S.speed=parseFloat(e.target.value); $("speedVal").textContent=S.speed.toFixed(2); saveSettings(); };
$("btnSpeedDown").onclick=()=>{ S.speed=Math.max(0.7, S.speed-0.05); $("speedRange").value=S.speed; $("speedVal").textContent=S.speed.toFixed(2); saveSettings(); };
$("btnSpeedUp").onclick=()=>{ S.speed=Math.min(1.3, S.speed+0.05); $("speedRange").value=S.speed; $("speedVal").textContent=S.speed.toFixed(2); saveSettings(); };
$("optStream").onchange=async (e)=>{ S.stream=e.target.checked; await saveSettings(); };
$("btnGenerate").onclick=()=>doGenerate(false);
$("btnStream").onclick=()=>doGenerate(true);
$("btnStop").onclick=()=>{ abortGen++; toast("Stopped","ok"); $("btnStop").disabled=true; };
$("btnDownload").onclick=()=>{
  if(!currentBlob){ toast("No audio","warn"); return; }
  const ext = $("selFormat")?.value || "wav";
  const mimeMap={wav:"audio/wav", mp3:"audio/mpeg", ogg:"audio/ogg", webm:"audio/webm", mp4:"audio/mp4", m4a:"audio/mp4", flac:"audio/flac"};
  const mime=mimeMap[ext]||"audio/wav";
  // For now wav data is decoded PCM; we allow any extension by re-wrapping blob with new mime (player will still decode as wav if needed)
  // Future: could transcode via MediaRecorder/OfflineAudioContext for true mp4/ogg encoding
  const outBlob = (ext==="wav") ? currentBlob : new Blob([currentBlob], {type:mime});
  const a=document.createElement("a"); a.href=URL.createObjectURL(outBlob); a.download="tts-"+new Date().toISOString().slice(0,19).replace(/[:T]/g,"-")+"."+ext; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),4000);
  toast(`Download .${ext}`,"ok",1500);
};
$("btnCopyText").onclick=async()=>{ try{ await navigator.clipboard.writeText($("ttsText").value); toast("Copied","ok",1200);}catch(e){toast("Clipboard blocked","warn")} };
$("btnClear").onclick=()=>{ $("ttsText").value=""; $("charCount").textContent="0 chars"; };
$("btnSample").onclick=()=>{ $("ttsText").value="Life is like a box of chocolates. You never know what you're gonna get. Hello, this is Kokoro TTS running 100% on-device in your browser!"; $("ttsText").dispatchEvent(new Event('input')); };
$("btnPaste").onclick=async()=>{ try{ const t=await navigator.clipboard.readText(); $("ttsText").value=t; $("ttsText").dispatchEvent(new Event('input')); }catch(e){toast("Clipboard blocked","warn")} };
$("ttsText").addEventListener('input', ()=>{ $("charCount").textContent=$("ttsText").value.length+" chars"; });
$("ttsText").addEventListener('keydown', e=>{ if((e.ctrlKey||e.metaKey)&&e.key==="Enter") doGenerate($("optStream").checked); });
$("btnClearHist").onclick=async()=>{
  const ok=await showCustomDialog({title:'Clear history?', message:'Remove all TTS history? Audio blobs will be deleted.', confirmText:'Clear', cancelText:'Cancel', icon:'delete_sweep'});
  if(!ok) return;
  await Store.clear("tts"); renderHist(); toast("History cleared","ok");
};
$("btnPersist").onclick=async()=>{
  try{ const ok=await navigator.storage.persist(); toast(ok?"Storage persistent 🎉":"Browser declined persistence",ok?"ok":"warn",5000); }catch(e){toast("Persistence unavailable","warn")}
};
$("btnWipe").onclick=async()=>{
  const ok=await showCustomDialog({title:'Clear cache?', message:'Delete all cached TTS models? They will need to be downloaded again.', confirmText:'Clear cache', cancelText:'Cancel', icon:'cleaning_services'});
  if(!ok) return;
  try{ if(window.caches) for(const n of await caches.keys()) await caches.delete(n); $("dl").innerHTML=""; dlRows.clear(); kokoro=null; pipeTTS=null; pipeKey=""; $("mdlTxt").textContent="none"; await updateCacheInfo(); toast("Cache cleared","ok"); }catch(e){toast("Clear failed: "+e.message,"err")}
};

// custom selects: same as STT (Poppin mono, is-selected pill-bg, keyboard nav, syncUI patch)
function initCustomSelects(){
  const ids=['selModel','selDtype','selDev','selVoice','selFormat'];
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
      btn.addEventListener('click', ()=>{ native.value=opt.value; native.dispatchEvent(new Event('change',{bubbles:true})); syncCS(); closeAll(); trigger.focus(); });
      list.appendChild(btn);
    });
    function syncCS(){
      const v=native.value; const opt=Array.from(native.options).find(o=>o.value===v); const valEl=cs.querySelector('.cs-value');
      if(opt && valEl){
        const raw=opt.textContent.trim(); const parts=raw.split('·'); const main=parts[0].trim(); const hint=parts.slice(1).join('·').trim();
        valEl.innerHTML= hint? `${main} <small style="opacity:.65;font-weight:400">· ${hint}</small>` : main;
      }
      cs.querySelectorAll('.cs-option').forEach(el=> el.classList.toggle('is-selected', el.dataset.value===v));
    }
    function closeAll(){ document.querySelectorAll('.cs-list').forEach(l=> l.hidden=true); document.querySelectorAll('.cs-trigger').forEach(b=> b.setAttribute('aria-expanded','false')); }
    trigger.addEventListener('click', (e)=>{ e.stopPropagation(); const isOpen=!list.hidden; closeAll(); if(!isOpen){ list.hidden=false; trigger.setAttribute('aria-expanded','true'); }});
    trigger.addEventListener('keydown', (e)=>{ if(e.key==='ArrowDown'||e.key==='Enter'||e.key===' '){ e.preventDefault(); list.hidden=false; trigger.setAttribute('aria-expanded','true'); const sel=list.querySelector('.is-selected')||list.querySelector('.cs-option'); if(sel) sel.focus(); }});
    list.addEventListener('keydown', (e)=>{
      const opts=Array.from(list.querySelectorAll('.cs-option')); const idx=opts.indexOf(document.activeElement);
      if(e.key==='ArrowDown'){ e.preventDefault(); (opts[idx+1]||opts[0]).focus(); }
      else if(e.key==='ArrowUp'){ e.preventDefault(); (opts[idx-1]||opts[opts.length-1]).focus(); }
      else if(e.key==='Escape'){ e.preventDefault(); closeAll(); trigger.focus(); }
      else if(e.key==='Enter'){ e.preventDefault(); document.activeElement.click(); }
    });
    cs.appendChild(trigger); cs.appendChild(list); native.insertAdjacentElement('afterend', cs); syncCS();
    native.addEventListener('change', ()=> syncCS());
  });
  document.addEventListener('click', (e)=>{ if(!e.target.closest('.cs')){ document.querySelectorAll('.cs-list').forEach(l=> l.hidden=true); document.querySelectorAll('.cs-trigger').forEach(b=> b.setAttribute('aria-expanded','false')); }});
  // keep syncUI in sync for TTS (mirrors STT patch)
  if(window.syncUI && !window._csSyncPatched){
    const orig=window.syncUI; window._csSyncPatched=true;
    window.syncUI=function(){ orig(); ['selModel','selDtype','selDev','selVoice','selFormat'].forEach(sid=>{ const n=document.getElementById(sid); if(n){ const c=document.querySelector(`.cs[data-target="${sid}"]`); if(c){ const v=n.value; const opt=Array.from(n.options).find(o=>o.value===v); const valEl=c.querySelector('.cs-value'); if(opt&&valEl){ const raw=opt.textContent.trim(); const parts=raw.split('·'); const main=parts[0].trim(); const hint=parts.slice(1).join('·').trim(); valEl.innerHTML=hint? `${main} <small style="opacity:.65;font-weight:400">· ${hint}</small>` : main; c.querySelectorAll('.cs-option').forEach(el=> el.classList.toggle('is-selected', el.dataset.value===v)); } } } }); };
  }
}
/* The app asks with NebDialog; so does the rest of the web now. This page had
   its own overlay, its own escape handler and no focus trap -- NebUI.confirm is
   the same component the forum and the library use, so a destructive action
   looks and behaves the same wherever it is taken. */
function showCustomDialog({title='Confirm', message='', confirmText='Confirm', cancelText='Cancel', icon='', destructive=true}={}){
  if(!window.NebUI || !NebUI.confirm) return Promise.resolve(confirm(message));
  return NebUI.confirm({title, message, confirmLabel:confirmText, cancelLabel:cancelText, icon, destructive});
}

// boot
(async()=>{
  await Store.open();
  await loadSettings();
  await renderHist();
  updateCacheInfo();
  const iso=isIsolated();
  $("devTxt").textContent = iso ? "WASM ⚡ (threads)" : "WASM (CPU)";
  $("netTxt").textContent="engine ready";
  $("ledNet").className="led on";
  if(!isIsolated()) banner(`💡 For fastest TTS: run <code>python serve.py</code> → <code>http://localhost:8000/tts.html</code> (threads 2–4×).`);
  try{ updateVoiceOptionsForModel(S.model); }catch(e){}
  setTimeout(()=>{ try{ initCustomSelects(); }catch(e){} },0);
  // second sync after custom selects created (for voice)
  setTimeout(()=>{ try{ updateVoiceOptionsForModel(S.model); }catch(e){} }, 600);
  console.log("WhisperWeb TTS v1.0 ready. isolated:",iso);
})();

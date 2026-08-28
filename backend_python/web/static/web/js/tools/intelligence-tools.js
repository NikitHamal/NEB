(function(){
"use strict";
var CFG = window.DI_CONFIG || {};
var REG = CFG.registry || [];
var $ = function(id){ return document.getElementById(id); };
function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]}); }

var DB_NAME = "nebians-di";
var DB_VER = 1;
var STORE = "files";
var CACHE_NAME = "nebians-di-cache-v1";

function openDB(){
  return new Promise(function(res,rej){
    if(!window.indexedDB) return rej(new Error("IndexedDB unavailable"));
    var r = indexedDB.open(DB_NAME, DB_VER);
    r.onupgradeneeded = function(){ if(!r.result.objectStoreNames.contains(STORE)) r.result.createObjectStore(STORE); };
    r.onsuccess = function(){ res(r.result); };
    r.onerror = function(){ rej(r.error); };
  });
}
function idbGet(key){
  return openDB().then(function(db){
    return new Promise(function(res,rej){
      var tx=db.transaction(STORE,"readonly");
      var req=tx.objectStore(STORE).get(key);
      req.onsuccess=function(){ res(req.result); };
      req.onerror=function(){ rej(req.error); };
      tx.oncomplete=function(){ db.close(); };
    });
  });
}
function idbPut(key,val){
  return openDB().then(function(db){
    return new Promise(function(res,rej){
      var tx=db.transaction(STORE,"readwrite");
      tx.objectStore(STORE).put(val,key);
      tx.oncomplete=function(){ db.close(); res(); };
      tx.onerror=function(){ rej(tx.error); };
      tx.onabort=function(){ rej(tx.error); };
    });
  });
}
function idbDel(key){
  return openDB().then(function(db){
    return new Promise(function(res,rej){
      var tx=db.transaction(STORE,"readwrite");
      tx.objectStore(STORE).delete(key);
      tx.oncomplete=function(){ db.close(); res(); };
      tx.onerror=function(){ rej(tx.error); };
    });
  });
}

var Manager = {
  key: function(toolId,name){ return toolId+"::"+name; },
  isReady: async function(tool){
    if(!tool.files || !tool.files.length) return true;
    for(var i=0;i<tool.files.length;i++){
      var v = await idbGet(this.key(tool.id, tool.files[i].name));
      if(!v) return false;
    }
    return true;
  },
  getFile: async function(toolId,name){
    var v = await idbGet(""+toolId+"::"+name);
    if(v) return v;
    return null;
  },
  remove: async function(tool){
    for(var i=0;i<(tool.files||[]).length;i++) try{ await idbDel(this.key(tool.id, tool.files[i].name)); }catch(_){}
    try{ await idbDel(tool.id+"::vocab"); }catch(_){}
    try{ if(window.caches) await caches.delete(CACHE_NAME); }catch(_){}
  },
  clearAll: async function(){
    var db=await openDB();
    await new Promise(function(res,rej){
      var tx=db.transaction(STORE,"readwrite");
      tx.objectStore(STORE).clear();
      tx.oncomplete=function(){ db.close(); res(); };
      tx.onerror=function(){ rej(tx.error); };
    });
    try{ if(window.caches) await caches.delete(CACHE_NAME); }catch(_){}
  },
  download: async function(tool, onProgress){
    var total = tool.files.reduce(function(a,f){return a+(f.size||0)},0) || 1;
    var loaded=0;
    for(var i=0;i<tool.files.length;i++){
      var f=tool.files[i];
      var url=f.url;
      var progStart = loaded/total;
      var progSpan = (f.size||0)/total;
      var buf = await fetchWithProgress(url, function(add,tot){
        var frac = tot ? add/tot : 0;
        onProgress(Math.min(0.99, progStart + frac*progSpan), f.name);
      });
      await idbPut(this.key(tool.id, f.name), buf);
      loaded+= (f.size||buf.byteLength);
      onProgress(Math.min(1, loaded/total), f.name);
      try{
        if(window.caches){
          var c=await caches.open(CACHE_NAME);
          var res=new Response(buf.slice(0),{headers:{"Content-Length":String(buf.byteLength)}});
          await c.put(url,res);
        }
      }catch(_){}
    }
    if(tool.id==="handwritten_math"){
      try{
        var vocabUrl = tool.files.find(function(x){return x.name==="vocab.json"});
        if(vocabUrl){
          var vb = await idbGet(this.key(tool.id,"vocab.json"));
          if(vb) await idbPut(tool.id+"::vocab", vb);
        }
      }catch(_){}
    }
  },
  storageText: async function(){
    try{
      if(navigator.storage && navigator.storage.estimate){
        var e=await navigator.storage.estimate();
        var u=e.usage||0, q=e.quota||0;
        var mb=function(b){ return (b/1024/1024).toFixed(b>50*1024*1024?1:2)+" MB"; };
        if(q) return mb(u)+" / "+mb(q);
        return mb(u)+" used";
      }
    }catch(_){}
    return "on-device";
  }
};

function fetchWithProgress(url, onChunk){
  return new Promise(function(res,rej){
    var xhr=new XMLHttpRequest();
    xhr.open("GET",url,true);
    xhr.responseType="arraybuffer";
    xhr.onprogress=function(e){
      if(e.lengthComputable) onChunk(e.loaded, e.total);
    };
    xhr.onload=function(){
      if(xhr.status>=200 && xhr.status<300){
        var buf = xhr.response;
        onChunk(buf.byteLength, buf.byteLength);
        res(buf);
      } else rej(new Error("Fetch failed "+xhr.status+" for "+url));
    };
    xhr.onerror=function(){ rej(new Error("Network error for "+url)); };
    xhr.send();
  });
}

var state={tool:null, readyMap:{}};

function renderList(){
  var el=$("diToolList"); el.innerHTML="";
  REG.forEach(function(t){
    var b=document.createElement("button");
    b.type="button"; b.className="di-tool"; b.dataset.id=t.id;
    var st = state.readyMap[t.id];
    var cls = st===true ? "ready" : st===false ? "off" : "off";
    var label = st===true ? "Ready" : st===false ? "Setup" : "—";
    b.innerHTML='<span class="material-symbols-outlined">'+esc(t.icon||"build")+'</span><div class="di-tool-main"><div class="di-tool-title">'+esc(t.label)+'</div><div class="di-tool-sub">'+esc(t.desc.slice(0,52))+' · '+esc(t.size)+'</div></div><span class="di-tool-state '+cls+'">'+label+'</span>';
    b.addEventListener("click",function(){ selectTool(t.id); });
    el.appendChild(b);
  });
}

async function refreshReady(){
  for(var i=0;i<REG.length;i++){
    var t=REG[i];
    try{ state.readyMap[t.id]=await Manager.isReady(t); }catch(_){ state.readyMap[t.id]=false; }
  }
  renderList();
  updateStorageBadge();
}

async function updateStorageBadge(){
  try{ $("diStorageText").textContent = await Manager.storageText(); }catch(_){ $("diStorageText").textContent="on-device"; }
}

function selectTool(id){
  state.tool=id;
  document.querySelectorAll(".di-tool").forEach(function(b){ b.classList.toggle("active", b.dataset.id===id); });
  var t=REG.find(function(x){return x.id===id});
  if(!t) return;
  $("diPanelIcon").textContent = t.icon || "build";
  $("diPanelTitle").textContent = t.label;
  $("diPanelDesc").textContent = t.desc;
  $("diPanelBadge").textContent = t.badge || "ON-DEVICE";
  $("diModelSize").textContent = t.size || "";
  var bar=$("diModelBar"); bar.style.display="flex";
  updateModelBar(t);
  renderWorkspace(t);
}

async function updateModelBar(t){
  if(!t.files || !t.files.length){
    $("diModelStatus").textContent="Ready — no download needed";
    $("diSetupBtn").style.display="none";
    $("diRemoveBtn").style.display="none";
    return;
  }
  var ready = await Manager.isReady(t);
  $("diModelStatus").textContent = ready ? "Ready offline · forever" : "Not installed · one-time download";
  $("diSetupBtn").style.display = ready ? "none" : "inline-flex";
  $("diRemoveBtn").style.display = ready ? "inline-flex" : "none";
  $("diSetupBtn").innerHTML = ready ? '<span class="material-symbols-outlined">check</span> Ready' : '<span class="material-symbols-outlined">download</span> Setup ('+esc(t.size)+')';
  $("diProgressWrap").style.display="none";
}

function renderWorkspace(t){
  var w=$("diWorkspace"); w.innerHTML="";
  if(t.id==="handwritten_math") renderHandwritten(w,t);
  else if(t.id==="scan_clean") renderScan(w,t);
  else if(t.id==="photo_scan") renderPhotoScan(w,t);
  else if(t.id==="table_extract") renderTable(w,t);
  else w.innerHTML='<div style="color:var(--md-on-surface-variant)">Tool coming soon.</div>';
}

// HANDWRITTEN MATH
var comerState={encoder:null, decoder:null, vocab:null, ortReady:false, canvas:null, drawing:false, points:[]};

function renderHandwritten(root, tool){
  root.innerHTML='\
  <div class="di-work">\
    <div class="di-canvas-wrap" id="hwWrap">\
      <canvas id="hwCanvas" width="800" height="340" style="background:#0f1115"></canvas>\
      <div class="di-canvas-toolbar">\
        <button class="md-btn md-btn-outlined" id="hwClear"><span class="material-symbols-outlined">ink_eraser</span> Clear</button>\
        <button class="md-btn md-btn-outlined" id="hwUndo"><span class="material-symbols-outlined">undo</span> Undo</button>\
        <label class="md-btn md-btn-outlined" style="cursor:pointer"><span class="material-symbols-outlined">upload</span> Upload image<input type="file" id="hwFile" accept="image/*" hidden></label>\
        <div style="margin-left:auto;display:flex;gap:8px">\
          <button class="md-btn md-btn-primary" id="hwRun"><span class="material-symbols-outlined">function</span> Recognize</button>\
        </div>\
      </div>\
    </div>\
    <div style="font-size:.82rem;color:var(--md-on-surface-variant)">Draw or upload a handwritten formula. Tiny CoMER (7.2MB) runs offline after one-time setup.</div>\
    <div class="di-result" id="hwResult">\
      <div class="di-result-label"><span class="material-symbols-outlined" style="font-size:16px">code</span> LaTeX</div>\
      <div class="di-latex" id="hwLatex" style="min-height:28px;color:var(--md-on-surface-variant)">Draw something and hit Recognize…</div>\
      <div class="di-actions" style="margin-top:10px">\
        <button class="md-btn md-btn-outlined" id="hwCopy"><span class="material-symbols-outlined">content_copy</span> Copy LaTeX</button>\
        <button class="md-btn md-btn-outlined" id="hwCopyMath"><span class="material-symbols-outlined">content_copy</span> Copy $…$</button>\
      </div>\
      <div class="di-result-label" style="margin-top:14px"><span class="material-symbols-outlined" style="font-size:16px">preview</span> Preview</div>\
      <div class="di-katex" id="hwPreview" style="min-height:44px">Preview appears here.</div>\
    </div>\
  </div>';
  initHandwrittenCanvas();
  $("hwRun").addEventListener("click",function(){ runHandwritten(tool); });
  $("hwClear").addEventListener("click",function(){ clearHw(); });
  $("hwUndo").addEventListener("click",function(){ undoHw(); });
  $("hwFile").addEventListener("change",function(e){ if(e.target.files[0]) loadHwImage(e.target.files[0]); });
  $("hwCopy").addEventListener("click",function(){ copyText($("hwLatex").textContent); });
  $("hwCopyMath").addEventListener("click",function(){ copyText("$"+$("hwLatex").textContent+"$"); });
}

var hwStrokes=[];
function initHandwrittenCanvas(){
  var c=$("hwCanvas");
  if(!c) return;
  comerState.canvas=c;
  var ctx=c.getContext("2d");
  function resize(){
    var rect=c.getBoundingClientRect();
    var dpr=window.devicePixelRatio||1;
    if(c.width!==Math.round(rect.width*dpr) || c.height!==Math.round(rect.height*dpr)){
      var old=ctx.getImageData(0,0,c.width,c.height);
    }
  }
  function pos(e){
    var rect=c.getBoundingClientRect();
    var t=e.touches?e.touches[0]:e;
    return {x:(t.clientX-rect.left)*(c.width/rect.width), y:(t.clientY-rect.top)*(c.height/rect.height)};
  }
  var cur=[];
  function start(e){ e.preventDefault(); comerState.drawing=true; cur=[pos(e)]; hwStrokes.push(cur); }
  function move(e){
    if(!comerState.drawing) return;
    e.preventDefault();
    var p=pos(e);
    cur.push(p);
    var n=cur.length;
    if(n>1){
      ctx.lineCap="round"; ctx.lineJoin="round"; ctx.strokeStyle="#ffffff"; ctx.lineWidth=4;
      ctx.beginPath(); ctx.moveTo(cur[n-2].x,cur[n-2].y); ctx.lineTo(p.x,p.y); ctx.stroke();
    }
  }
  function end(e){ if(e) e.preventDefault(); comerState.drawing=false; }
  c.addEventListener("mousedown",start); c.addEventListener("mousemove",move); c.addEventListener("mouseup",end); c.addEventListener("mouseleave",end);
  c.addEventListener("touchstart",start,{passive:false}); c.addEventListener("touchmove",move,{passive:false}); c.addEventListener("touchend",end,{passive:false});
  ctx.fillStyle="#0f1115"; ctx.fillRect(0,0,c.width,c.height);
}
function clearHw(){ hwStrokes=[]; var c=$("hwCanvas"); if(!c) return; var ctx=c.getContext("2d"); ctx.fillStyle="#0f1115"; ctx.fillRect(0,0,c.width,c.height); $("hwLatex").textContent="Draw something and hit Recognize…"; $("hwPreview").innerHTML="Preview appears here."; }
function undoHw(){ if(!hwStrokes.length) return; hwStrokes.pop(); var c=$("hwCanvas"); var ctx=c.getContext("2d"); ctx.fillStyle="#0f1115"; ctx.fillRect(0,0,c.width,c.height); ctx.lineCap="round"; ctx.lineJoin="round"; ctx.strokeStyle="#ffffff"; ctx.lineWidth=4; hwStrokes.forEach(function(s){ for(var i=1;i<s.length;i++){ ctx.beginPath(); ctx.moveTo(s[i-1].x,s[i-1].y); ctx.lineTo(s[i].x,s[i].y); ctx.stroke(); } }); }
function loadHwImage(file){
  var c=$("hwCanvas"); var ctx=c.getContext("2d");
  var img=new Image();
  img.onload=function(){
    ctx.fillStyle="#0f1115"; ctx.fillRect(0,0,c.width,c.height);
    var scale=Math.min((c.width*0.9)/img.width, (c.height*0.9)/img.height);
    var w=img.width*scale, h=img.height*scale, x=(c.width-w)/2, y=(c.height-h)/2;
    ctx.filter="invert(1)"; ctx.drawImage(img,x,y,w,h); ctx.filter="none";
    var d=ctx.getImageData(0,0,c.width,c.height);
    for(var i=0;i<d.data.length;i+=4){ if(d.data[i]>200 && d.data[i+1]>200 && d.data[i+2]>200){ d.data[i]=255; d.data[i+1]=255; d.data[i+2]=255; } }
    ctx.putImageData(d,0,0);
  };
  img.src=URL.createObjectURL(file);
}

async function ensureComer(tool){
  if(comerState.encoder && comerState.decoder && comerState.vocab) return true;
  var ready = await Manager.isReady(tool);
  if(!ready) throw new Error("Model not installed. Click Setup first.");
  if(!window.ort){
    await loadScript("https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.0/dist/ort.min.js");
  }
  if(window.ort) { window.ort.env.wasm.wasmPaths="https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.0/dist/"; try{ window.ort.env.wasm.numThreads=1; }catch(_){} }
  var encBuf = await Manager.getFile(tool.id,"encoder_int8.onnx");
  var decBuf = await Manager.getFile(tool.id,"decoder_int8.onnx");
  var vocabBuf = await Manager.getFile(tool.id,"vocab.json");
  if(!encBuf||!decBuf) throw new Error("Model files missing. Please Setup again.");
  var voc = JSON.parse(new TextDecoder().decode(vocabBuf));
  var vocab = Array.isArray(voc) ? voc : (voc.vocab || voc.tokens || Object.keys(voc));
  comerState.vocab = vocab;
  try{
    comerState.encoder = await window.ort.InferenceSession.create(encBuf, {executionProviders:["wasm"]});
    comerState.decoder = await window.ort.InferenceSession.create(decBuf, {executionProviders:["wasm"]});
  }catch(e){ throw new Error("Failed to load ONNX: "+e.message); }
  return true;
}

function loadScript(src){
  return new Promise(function(res,rej){
    var s=document.createElement("script"); s.src=src; s.onload=res; s.onerror=function(){rej(new Error("Failed load "+src))}; document.head.appendChild(s);
  });
}
function copyText(t){
  navigator.clipboard.writeText(t).then(function(){ showSnack("Copied"); },function(){
    var ta=document.createElement("textarea"); ta.value=t; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove(); showSnack("Copied");
  });
}
function showSnack(m){
  var s=document.createElement("div"); s.textContent=m; s.style.cssText="position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#1f2937;color:#fff;padding:8px 14px;border-radius:999px;font-size:.82rem;z-index:9999";
  document.body.appendChild(s); setTimeout(function(){ s.remove(); },1400);
}
function renderKatex(latex){
  var el=$("hwPreview");
  if(!el) return;
  var txt=String(latex||"").trim();
  if(!txt){ el.textContent="Preview appears here."; return; }
  function doRender(){
    try{ window.katex.render(txt, el, {throwOnError:false, displayMode:true}); }catch(e){ el.textContent=txt; }
  }
  if(window.katex) doRender();
  else loadScript("https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js").then(function(){
    var l=document.createElement("link"); l.rel="stylesheet"; l.href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"; document.head.appendChild(l);
    doRender();
  }).catch(function(){ el.textContent=txt; });
}

function preprocessForComer(canvas){
  var H=256;
  var srcW=canvas.width, srcH=canvas.height;
  var ctx=canvas.getContext("2d");
  var data=ctx.getImageData(0,0,srcW,srcH).data;
  var minX=srcW, minY=srcH, maxX=0, maxY=0;
  var has=false;
  for(var y=0;y<srcH;y++) for(var x=0;x<srcW;x++){
    var idx=(y*srcW+x)*4;
    var v = (data[idx]+data[idx+1]+data[idx+2])/3;
    if(v>30){ if(x<minX)minX=x; if(y<minY)minY=y; if(x>maxX)maxX=x; if(y>maxY)maxY=y; has=true; }
  }
  if(!has){ minX=0; minY=0; maxX=srcW-1; maxY=srcH-1; }
  var pad=8;
  minX=Math.max(0,minX-pad); minY=Math.max(0,minY-pad); maxX=Math.min(srcW-1,maxX+pad); maxY=Math.min(srcH-1,maxY+pad);
  var bw=maxX-minX+1, bh=maxY-minY+1;
  var scale=H/bh;
  var newW=Math.ceil(bw*scale);
  newW=Math.max(64, Math.min(1024, Math.ceil(newW/64)*64));
  var off=document.createElement("canvas"); off.width=newW; off.height=H;
  var octx=off.getContext("2d");
  octx.fillStyle="#000000"; octx.fillRect(0,0,newW,H);
  octx.imageSmoothingEnabled=true; octx.imageSmoothingQuality="high";
  var tmp=document.createElement("canvas"); tmp.width=bw; tmp.height=bh; tmp.getContext("2d").putImageData(ctx.getImageData(minX,minY,bw,bh),0,0);
  var drawW=bw*scale, drawH=H;
  octx.drawImage(tmp,0,0,bw,bh,0,0,drawW,drawH);
  var img=octx.getImageData(0,0,newW,H);
  var f=new Float32Array(1*1*H*newW);
  var mask=new Float32Array(1*H*newW);
  for(var yy=0;yy<H;yy++) for(var xx=0;xx<newW;xx++){
    var id=(yy*newW+xx)*4;
    var gv=(img.data[id]+img.data[id+1]+img.data[id+2])/3/255;
    f[yy*newW+xx]=gv;
    mask[yy*newW+xx]= xx<drawW ? 1:0;
  }
  return {data:f, mask:mask, w:newW, h:H};
}

async function runHandwritten(tool){
  var btn=$("hwRun");
  var ready = await Manager.isReady(tool);
  if(!ready){ showSnack("Click Setup to download model first"); return; }
  btn.disabled=true; btn.innerHTML='<span class="material-symbols-outlined">hourglass_top</span> Working…';
  $("hwLatex").textContent="Running tiny model on your device…";
  try{
    await ensureComer(tool);
    var prep = preprocessForComer($("hwCanvas"));
    if(!comerState.encoder || !comerState.decoder) throw new Error("Encoder not loaded");
    var encIn={};
    var encNames=comerState.encoder.inputNames;
    var needImg = encNames[0];
    var imgTensor=new window.ort.Tensor("float32", prep.data, [1,1,prep.h,prep.w]);
    encIn[needImg]=imgTensor;
    if(encNames.length>1){
      try{ encIn[encNames[1]]=new window.ort.Tensor("float32", prep.mask, [1, prep.h, prep.w]); }catch(_){}
    }
    var encOut=await comerState.encoder.run(encIn);
    var featName=comerState.encoder.outputNames[0];
    var feat=encOut[featName];
    var decNames=comerState.decoder.inputNames;
    var outNames=comerState.decoder.outputNames;
    var vocab=comerState.vocab;
    var seq=[1];
    var maxSteps=48;
    for(var step=0; step<maxSteps; step++){
      var tgt=new window.ort.Tensor("int64", new BigInt64Array(seq.map(function(x){return BigInt(x)})), [1, seq.length]);
      var decIn={}; decIn[decNames[0]]=tgt;
      if(decNames.length>1){
        if(feat) decIn[decNames[1]]=feat;
        else decIn[decNames[1]]=feat;
      }
      for(var di=2; di<decNames.length; di++){
        var nm=decNames[di].toLowerCase();
        if(nm.includes("mask")){
          var ml = seq.length;
          var m = new Float32Array(ml* prep.w);
          decIn[decNames[di]]=new window.ort.Tensor("float32", m, [1, ml, prep.w]);
        }
      }
      var dOut;
      try{ dOut=await comerState.decoder.run(decIn); }catch(e){ break; }
      var logits=dOut[outNames[0]];
      var arr=logits.data;
      var vocabSize = logits.dims[logits.dims.length-1] || vocab.length;
      var lastOff = (seq.length-1)*vocabSize;
      var best=0, bestV=-1e9;
      for(var vi=0; vi<vocabSize; vi++){ var v=arr[lastOff+vi]; if(v>bestV){ bestV=v; best=vi; } }
      if(best===2) break;
      if(best!==0 && best!==1) seq.push(best);
      else if(best===0) seq.push(best);
      if(seq.length>60) break;
    }
    var tokens = seq.slice(1).map(function(id){ return vocab[id] || ""; }).filter(Boolean);
    var latex = tokens.join(" ").replace(/\s+/g," ").replace(/\\ /g,"\\").trim();
    latex = latex.replace(/<eos>|<bos>|<pad>/g,"").trim() || "\\text{(no result — try clearer writing)}";
    $("hwLatex").textContent=latex;
    renderKatex(latex);
    showSnack("Done — offline");
  }catch(e){
    console.error(e);
    $("hwLatex").textContent="Error: "+(e.message||e);
    $("hwPreview").textContent="Try redrawing more clearly or uploading a clearer image.";
  }finally{
    btn.disabled=false; btn.innerHTML='<span class="material-symbols-outlined">function</span> Recognize';
  }
}

// SCAN -> CLEAN TEXT
var scanWorker=null;
function renderScan(root, tool){
  root.innerHTML='\
  <div class="di-work">\
    <div class="di-drop" id="scanDrop"><span class="material-symbols-outlined">document_scanner</span><div><strong>Drop image or PDF page</strong><span class="di-drop-sub">JPG/PNG/PDF — printed NEB papers, notes. Runs offline.</span></div><input type="file" id="scanFile" accept="image/*,application/pdf" hidden></div>\
    <div id="scanPreview" style="display:none"><img id="scanImg" style="max-width:100%;border-radius:10px;border:1px solid var(--md-outline-variant)"></div>\
    <div style="display:flex;gap:8px;flex-wrap:wrap">\
      <button class="md-btn md-btn-primary" id="scanRun"><span class="material-symbols-outlined">text_fields</span> Extract Text</button>\
      <button class="md-btn md-btn-outlined" id="scanCopy"><span class="material-symbols-outlined">content_copy</span> Copy</button>\
      <button class="md-btn md-btn-outlined" id="scanDownload"><span class="material-symbols-outlined">download</span> Download .txt</button>\
      <select id="scanLang" style="padding:7px 10px;border-radius:8px;border:1px solid var(--md-outline);background:var(--md-surface);color:var(--md-on-surface)"><option value="eng">English</option><option value="eng+nep">English+Nepali</option></select>\
    </div>\
    <div class="di-result"><div class="di-result-label"><span class="material-symbols-outlined" style="font-size:16px">article</span> Clean Text</div><textarea id="scanOut" rows="12" style="width:100%;padding:12px;border-radius:10px;border:1px solid var(--md-outline-variant);background:var(--md-surface);color:var(--md-on-surface);font-family:ui-monospace,monospace;font-size:.88rem;resize:vertical" placeholder="Extracted text will appear here…"></textarea></div>\
  </div>';
  var drop=root.querySelector("#scanDrop"), inp=root.querySelector("#scanFile"), img=root.querySelector("#scanImg"), prev=root.querySelector("#scanPreview");
  drop.addEventListener("click",function(){ inp.click(); });
  inp.addEventListener("change",function(){ if(inp.files[0]) handleScanFile(inp.files[0], img, prev); });
  drop.addEventListener("dragover",function(e){e.preventDefault(); drop.style.borderColor="var(--md-primary)";});
  drop.addEventListener("dragleave",function(){drop.style.borderColor="";});
  drop.addEventListener("drop",function(e){ e.preventDefault(); drop.style.borderColor=""; if(e.dataTransfer.files[0]) handleScanFile(e.dataTransfer.files[0], img, prev); });
  root.querySelector("#scanRun").addEventListener("click",function(){ doScanOCR(); });
  root.querySelector("#scanCopy").addEventListener("click",function(){ copyText($("scanOut").value); });
  root.querySelector("#scanDownload").addEventListener("click",function(){ downloadTxt($("scanOut").value, "scan.txt"); });
}
var scanFileObj=null;
function handleScanFile(file, imgEl, prev){
  scanFileObj=file;
  if(file.type.startsWith("image/")){
    imgEl.src=URL.createObjectURL(file); prev.style.display="block";
  } else {
    prev.style.display="none";
  }
  $("scanOut").value="Ready to extract. Click Extract Text (first time downloads ~2MB OCR core, cached forever).";
}
async function ensureTesseract(){
  if(window.Tesseract) return window.Tesseract;
  await loadScript("https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js");
  return window.Tesseract;
}
async function doScanOCR(){
  var out=$("scanOut");
  if(!scanFileObj){ showSnack("Drop an image first"); return; }
  var btn=document.getElementById("scanRun");
  btn.disabled=true; btn.innerHTML='<span class="material-symbols-outlined">hourglass_top</span> Reading…';
  out.value="Loading OCR on your device… (one-time, then offline)\n";
  try{
    var T=await ensureTesseract();
    var lang=$("scanLang").value||"eng";
    if(!scanWorker){
      scanWorker=await T.createWorker(lang, 1, {
        cacheMethod:"readOnly",
        logger:function(m){ if(m.status==="recognizing text") out.value="Reading… "+Math.round((m.progress||0)*100)+"%"; }
      });
    }
    var imageSource = scanFileObj;
    if(scanFileObj.type==="application/pdf"){
      out.value="PDFs: rendering first page for OCR…";
      var pdfUrl=URL.createObjectURL(scanFileObj);
      var c=document.createElement("canvas");
      out.value="PDF extract: opening… (for full PDF, export images to this tool or use Lazy Tools)";
      imageSource=scanFileObj;
    }
    var ret=await scanWorker.recognize(imageSource);
    var text=(ret.data && ret.data.text) ? ret.data.text.trim() : "";
    if(!text) text="(No text found — try a clearer, higher-contrast scan)";
    text = text.replace(/\n{3,}/g,"\n\n").trim();
    out.value=text;
    showSnack("Done offline");
  }catch(e){
    out.value="Error: "+(e.message||e)+"\nTip: retry when online — first run needs ~2MB download.";
    console.error(e);
  }finally{
    btn.disabled=false; btn.innerHTML='<span class="material-symbols-outlined">text_fields</span> Extract Text';
  }
}
function downloadTxt(t, name){
  var blob=new Blob([t||""],{type:"text/plain;charset=utf-8"});
  var a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=name; a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); },1000);
}

// PHOTO SCAN
function renderPhotoScan(root, tool){
  root.innerHTML='\
  <div class="di-work">\
    <div class="di-drop" id="photoDrop"><span class="material-symbols-outlined">photo_camera</span><div><strong>Drop photo of notes</strong><span class="di-drop-sub">Auto-contrast + denoise + crop. Instant, no download.</span></div><input type="file" id="photoFile" accept="image/*" hidden></div>\
    <div class="di-enhance-preview" id="photoPrev" style="display:none"><div><div style="font-size:.75rem;font-weight:600;color:var(--md-on-surface-variant);margin-bottom:6px">Original</div><img id="photoOrig"></div><div><div style="font-size:.75rem;font-weight:600;color:var(--md-on-surface-variant);margin-bottom:6px">Enhanced</div><canvas id="photoCanvas"></canvas></div></div>\
    <div style="display:flex;gap:8px;flex-wrap:wrap">\
      <button class="md-btn md-btn-outlined" id="photoEnhance"><span class="material-symbols-outlined">auto_fix</span> Auto enhance</button>\
      <button class="md-btn md-btn-outlined" id="photoGray"><span class="material-symbols-outlined">contrast</span> B&W Scan</button>\
      <button class="md-btn md-btn-primary" id="photoSave"><span class="material-symbols-outlined">picture_as_pdf</span> Save as PDF</button>\
      <button class="md-btn md-btn-outlined" id="photoDl"><span class="material-symbols-outlined">download</span> Save image</button>\
    </div>\
    <div style="font-size:.82rem;color:var(--md-on-surface-variant)">Tip: take photo straight above page in good light. Use <em>Auto enhance</em> then <em>Save as PDF</em> to make a clean notes PDF.</div>\
  </div>';
  var drop=root.querySelector("#photoDrop"), inp=root.querySelector("#photoFile");
  var orig=document.getElementById("photoOrig"), canvas=document.getElementById("photoCanvas"), wrap=document.getElementById("photoPrev");
  var currentImg=null;
  drop.addEventListener("click",function(){ inp.click(); });
  inp.addEventListener("change",function(){ if(inp.files[0]) loadPhoto(inp.files[0]); });
  drop.addEventListener("dragover",function(e){e.preventDefault(); drop.style.borderColor="var(--md-primary)";});
  drop.addEventListener("dragleave",function(){drop.style.borderColor="";});
  drop.addEventListener("drop",function(e){ e.preventDefault(); drop.style.borderColor=""; if(e.dataTransfer.files[0]) loadPhoto(e.dataTransfer.files[0]); });
  function loadPhoto(file){
    var url=URL.createObjectURL(file);
    var img=new Image();
    img.onload=function(){
      currentImg=img;
      orig.src=url; wrap.style.display="grid";
      var c=canvas; c.width=img.width; c.height=img.height;
      c.getContext("2d").drawImage(img,0,0);
    };
    img.src=url;
  }
  root.querySelector("#photoEnhance").addEventListener("click",function(){ if(currentImg) enhanceCanvas(canvas, false); });
  root.querySelector("#photoGray").addEventListener("click",function(){ if(currentImg) enhanceCanvas(canvas, true); });
  root.querySelector("#photoSave").addEventListener("click",function(){ savePhotoPdf(canvas); });
  root.querySelector("#photoDl").addEventListener("click",function(){ var a=document.createElement("a"); a.href=canvas.toDataURL("image/jpeg",0.92); a.download="scan.jpg"; a.click(); });
}

function enhanceCanvas(canvas, bw){
  var ctx=canvas.getContext("2d");
  var w=canvas.width, h=canvas.height;
  var id=ctx.getImageData(0,0,w,h), d=id.data;
  var hist=new Array(256).fill(0);
  for(var i=0;i<d.length;i+=4){ var g=0.299*d[i]+0.587*d[i+1]+0.114*d[i+2]; hist[Math.round(g)]++; }
  var cdf=new Array(256).fill(0); cdf[0]=hist[0]; for(var k=1;k<256;k++) cdf[k]=cdf[k-1]+hist[k];
  var total=w*h, min=cdf.find(function(v){return v>total*0.01})||0;
  var max=cdf.findLastIndex? (function(){ for(var kk=255;kk>=0;kk--) if(cdf[kk]<total*0.99) return kk; return 255; })() : 255;
  for(var j=0;j<d.length;j+=4){
    for(var ch=0;ch<3;ch++){
      var v=d[j+ch];
      var nv = 255*(v-min)/(Math.max(1,max-min));
      nv = Math.max(0,Math.min(255, nv*1.1 - 8));
      d[j+ch]=nv;
    }
    if(bw){
      var gv=0.299*d[j]+0.587*d[j+1]+0.114*d[j+2];
      var th = gv>140? 255 : (gv>90? (gv-90)*3.1 : 0);
      d[j]=d[j+1]=d[j+2]=Math.max(0,Math.min(255,th));
    }
  }
  ctx.putImageData(id,0,0);
}

function savePhotoPdf(canvas){
  var w=canvas.width, h=canvas.height;
  var pw=Math.min(595, w*72/96), ph=pw * (h/w);
  if(typeof window.jspdf!=="undefined") return;
  var imgData=canvas.toDataURL("image/jpeg",0.88);
  var win=window.open("","_blank");
  if(!win){ showSnack("Pop-up blocked — instead Save image then use Images → PDF"); return; }
  win.document.write('<html><head><title>Scan</title></head><body style="margin:0;display:grid;place-items:center;min-height:100vh;background:#f3f4f6"><img src="'+imgData+'" style="max-width:100%;box-shadow:0 8px 30px rgba(0,0,0,.15)"><script>window.print()<\/script></body></html>');
  showSnack("Opened print view — Save as PDF there");
}

// TABLE
function renderTable(root, tool){
  root.innerHTML='\
  <div class="di-work">\
    <div class="di-drop" id="tblDrop"><span class="material-symbols-outlined">table</span><div><strong>Drop table photo</strong><span class="di-drop-sub">Shares OCR — extracts rows to CSV.</span></div><input type="file" id="tblFile" accept="image/*" hidden></div>\
    <button class="md-btn md-btn-primary" id="tblRun"><span class="material-symbols-outlined">table_rows</span> Extract to CSV</button>\
    <div class="di-result"><div class="di-result-label">CSV</div><textarea id="tblOut" rows="8" style="width:100%;padding:12px;border-radius:10px;border:1px solid var(--md-outline-variant);background:var(--md-surface);font-family:monospace;font-size:.85rem" placeholder="Rows appear here…"></textarea>\
      <div class="di-actions" style="margin-top:8px"><button class="md-btn md-btn-outlined" id="tblCopy"><span class="material-symbols-outlined">content_copy</span> Copy CSV</button><button class="md-btn md-btn-outlined" id="tblDl"><span class="material-symbols-outlined">download</span> Download .csv</button></div>\
    </div>\
    <div style="font-size:.82rem;color:var(--md-on-surface-variant)">Uses same offline OCR. For complex tables, open result in Sheets and fix lines.</div>\
  </div>';
  var drop=root.querySelector("#tblDrop"), inp=root.querySelector("#tblFile");
  drop.addEventListener("click",function(){ inp.click(); });
  inp.addEventListener("change",function(){ if(inp.files[0]){ scanFileObj=inp.files[0]; $("tblOut").value="Table image loaded. Click Extract to CSV (uses OCR)."; }});
  drop.addEventListener("dragover",function(e){e.preventDefault(); drop.style.borderColor="var(--md-primary)";});
  drop.addEventListener("dragleave",function(){drop.style.borderColor="";});
  drop.addEventListener("drop",function(e){ e.preventDefault(); drop.style.borderColor=""; if(e.dataTransfer.files[0]){ scanFileObj=e.dataTransfer.files[0]; $("tblOut").value="Table image loaded. Click Extract to CSV."; }});
  root.querySelector("#tblCopy").addEventListener("click",function(){ copyText($("tblOut").value); });
  root.querySelector("#tblDl").addEventListener("click",function(){ downloadTxt($("tblOut").value, "table.csv"); });
  root.querySelector("#tblRun").addEventListener("click",async function(){
    if(!scanFileObj){ showSnack("Drop a table image first"); return; }
    var btn=this; btn.disabled=true; btn.innerHTML='<span class="material-symbols-outlined">hourglass_top</span> Reading…';
    try{
      var T=await ensureTesseract();
      if(!scanWorker) scanWorker=await T.createWorker("eng",1,{cacheMethod:"readOnly"});
      var ret=await scanWorker.recognize(scanFileObj);
      var txt=(ret.data.text||"").trim();
      var rows=txt.split("\n").map(function(l){return l.trim().split(/\s{2,}|\t/).map(function(c){return '"'+c.replace(/"/g,'""')+'"';}).join(",");});
      $("tblOut").value=rows.join("\n")||"(no rows)";
      showSnack("Done");
    }catch(e){ $("tblOut").value="Error: "+e.message; }finally{ btn.disabled=false; btn.innerHTML='<span class="material-symbols-outlined">table_rows</span> Extract to CSV'; }
  });
}

// SETUP / REMOVE wiring
document.addEventListener("DOMContentLoaded", async function(){
  await refreshReady();
  if(REG[0]) selectTool(REG[0].id);
  $("diSetupBtn").addEventListener("click", async function(){
    var t=REG.find(function(x){return x.id===state.tool});
    if(!t) return;
    if(!t.files.length){ showSnack("No download needed"); return; }
    var btn=this; btn.disabled=true;
    $("diProgressWrap").style.display="flex"; $("diProgressFill").style.width="0%"; $("diProgressText").textContent="0%";
    $("diModelStatus").textContent="Downloading…";
    try{
      await Manager.download(t, function(frac, name){
        $("diProgressFill").style.width=Math.round(frac*100)+"%";
        $("diProgressText").textContent=Math.round(frac*100)+"% · "+name;
      });
      $("diModelStatus").textContent="Ready offline · forever";
      btn.style.display="none"; $("diRemoveBtn").style.display="inline-flex";
      showSnack("Ready — now offline forever");
      await refreshReady();
      selectTool(t.id);
    }catch(e){
      $("diModelStatus").textContent="Failed: "+(e.message||e);
      btn.disabled=false;
      console.error(e);
    }finally{
      $("diProgressWrap").style.display="none";
      btn.disabled=false;
    }
  });
  $("diRemoveBtn").addEventListener("click", async function(){
    var t=REG.find(function(x){return x.id===state.tool});
    if(!t||!confirm("Remove on-device model for "+t.label+"? You can re-Setup anytime.")) return;
    await Manager.remove(t);
    if(t.id==="handwritten_math"){ comerState.encoder=null; comerState.decoder=null; comerState.vocab=null; }
    if(scanWorker){ try{ await scanWorker.terminate(); }catch(_){} scanWorker=null; }
    showSnack("Removed");
    await refreshReady();
    selectTool(t.id);
  });
  $("diClearCache").addEventListener("click", async function(e){
    e.preventDefault();
    if(!confirm("Remove ALL on-device models? You can re-download anytime.")) return;
    await Manager.clearAll();
    comerState.encoder=null; comerState.decoder=null; comerState.vocab=null;
    if(scanWorker){ try{ await scanWorker.terminate(); }catch(_){} scanWorker=null; }
    showSnack("All models removed");
    await refreshReady();
    if(state.tool) selectTool(state.tool);
  });
});
})();

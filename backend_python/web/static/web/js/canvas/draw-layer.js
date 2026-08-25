(function(){
"use strict";
var C = window.CanvasCore;
if (!C) return;
var S = C.state, E = C.els;
S.tool = S.tool || "select";
S.objects = S.objects || [];
S.drawColor = S.drawColor || "#1f1f1f";
S.drawWidth = S.drawWidth || 3;
S.drawDirty = true;

var COLORS = ["#1f1f1f","#e53e3e","#dd6b20","#d69e2e","#38a169","#3182ce","#5a67d8","#ffffff"];
var WIDTHS = [2, 4, 8, 14];
var STICKY = ["#fff9c4","#c8e6c9","#bbdefb","#f8bbd0","#ffe0b2"];

var layer = document.createElement("canvas");
layer.id = "canvasDrawLayer";
layer.className = "canvas-draw-layer";
if (E.viewport) E.viewport.appendChild(layer);
var ctx = layer.getContext("2d");
var dpr = 1, vw = 0, vh = 0;
var drawing = false, path = [], shape0 = null, last = null, drag = null;
var selectedId = "";
var imgCache = {};
var saveTimer = null;
var fileInput = document.createElement("input");
fileInput.type = "file";
fileInput.accept = "image/*,.pdf,.png,.jpg,.jpeg,.webp,.gif,.txt,.md";
fileInput.hidden = true;
document.body.appendChild(fileInput);
var placeAt = { x: 0, y: 0 };

function uid(){ return "o_" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36); }
function isWidgetTool(t){ return t && t.indexOf("w-") === 0; }
function isDrawTool(t){ return t === "pen" || t === "highlighter" || t === "marker" || t === "rect" || t === "ellipse" || t === "line" || t === "arrow" || t === "eraser" || t === "lasso" || t === "text" || t === "sticky" || t === "image" || t === "file" || isWidgetTool(t); }
function intercept(){ return isDrawTool(S.tool) && !S.readOnly; }

function resize(){
  if (!E.viewport) return;
  dpr = Math.min(window.devicePixelRatio || 1, 2);
  vw = E.viewport.clientWidth;
  vh = E.viewport.clientHeight;
  layer.width = Math.round(vw * dpr);
  layer.height = Math.round(vh * dpr);
  layer.style.width = vw + "px";
  layer.style.height = vh + "px";
  S.drawDirty = true;
  paint();
}
function world(e){
  var r = E.viewport.getBoundingClientRect();
  return C.s2w(e.clientX - r.left, e.clientY - r.top);
}
function applyCam(){
  ctx.setTransform(dpr * S.view.scale, 0, 0, dpr * S.view.scale, dpr * S.view.x, dpr * S.view.y);
}

function bounds(el){
  if (!el) return null;
  if (el.type === "pen" || el.type === "highlighter" || el.type === "marker"){
    if (!el.points || !el.points.length) return null;
    var mnx=1e9,mny=1e9,mxx=-1e9,mxy=-1e9;
    for (var i=0;i<el.points.length;i++){
      var p=el.points[i];
      if (p.x<mnx)mnx=p.x; if(p.y<mny)mny=p.y; if(p.x>mxx)mxx=p.x; if(p.y>mxy)mxy=p.y;
    }
    return {x:mnx,y:mny,w:mxx-mnx,h:mxy-mny};
  }
  if (el.type === "line" || el.type === "arrow"){
    return {x:Math.min(el.x1,el.x2),y:Math.min(el.y1,el.y2),w:Math.abs(el.x2-el.x1),h:Math.abs(el.y2-el.y1)};
  }
  return {x:el.x,y:el.y,w:el.w||160,h:el.h||120};
}
function hit(wx, wy){
  for (var i = S.objects.length - 1; i >= 0; i--){
    var b = bounds(S.objects[i]);
    if (!b) continue;
    if (wx >= b.x - 10 && wx <= b.x + b.w + 10 && wy >= b.y - 10 && wy <= b.y + b.h + 10) return i;
  }
  return -1;
}

function drawEl(el, on){
  if (!el) return;
  if (window.CanvasWidgets && window.CanvasWidgets.isHtml(el)) return;
  ctx.save();
  if (el.type === "pen" || el.type === "highlighter" || el.type === "marker"){
    if (!el.points || el.points.length < 2){ ctx.restore(); return; }
    ctx.globalAlpha = el.type === "highlighter" ? 0.38 : 1;
    ctx.strokeStyle = el.color || "#111";
    ctx.lineWidth = el.lineWidth || (el.type === "highlighter" ? 18 : 3);
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    ctx.beginPath();
    ctx.moveTo(el.points[0].x, el.points[0].y);
    for (var i=1;i<el.points.length;i++) ctx.lineTo(el.points[i].x, el.points[i].y);
    ctx.stroke();
  } else if (el.type === "rect"){
    ctx.strokeStyle = el.stroke || "#111";
    ctx.lineWidth = el.lineWidth || 2;
    ctx.strokeRect(el.x, el.y, el.w, el.h);
  } else if (el.type === "ellipse"){
    ctx.strokeStyle = el.stroke || "#111";
    ctx.lineWidth = el.lineWidth || 2;
    ctx.beginPath();
    ctx.ellipse(el.x + el.w/2, el.y + el.h/2, Math.abs(el.w/2), Math.abs(el.h/2), 0, 0, Math.PI*2);
    ctx.stroke();
  } else if (el.type === "line" || el.type === "arrow"){
    ctx.strokeStyle = el.stroke || "#111";
    ctx.lineWidth = el.lineWidth || 2;
    ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(el.x1, el.y1); ctx.lineTo(el.x2, el.y2); ctx.stroke();
    if (el.type === "arrow"){
      var a = Math.atan2(el.y2-el.y1, el.x2-el.x1), h = Math.max(12, (el.lineWidth||2)*4);
      ctx.fillStyle = el.stroke || "#111";
      ctx.beginPath();
      ctx.moveTo(el.x2, el.y2);
      ctx.lineTo(el.x2 - h*Math.cos(a-0.4), el.y2 - h*Math.sin(a-0.4));
      ctx.lineTo(el.x2 - h*Math.cos(a+0.4), el.y2 - h*Math.sin(a+0.4));
      ctx.closePath(); ctx.fill();
    }
  } else if (el.type === "sticky"){
    ctx.fillStyle = el.bg || "#fff9c4";
    ctx.shadowColor = "rgba(0,0,0,.12)"; ctx.shadowBlur = 8; ctx.shadowOffsetY = 2;
    roundRect(el.x, el.y, el.w||160, el.h||120, 8); ctx.fill();
    ctx.shadowColor = "transparent";
    ctx.fillStyle = "#1f1f1f";
    ctx.font = "13px Poppins, sans-serif";
    wrap(el.text || "", el.x+10, el.y+12, (el.w||160)-20, 18);
  } else if (el.type === "text"){
    ctx.fillStyle = el.color || "#1f1f1f";
    ctx.font = (el.fontSize||18)+"px Poppins, sans-serif";
    ctx.textBaseline = "top";
    var lines = String(el.text||"").split("\n");
    for (var t=0;t<lines.length;t++) ctx.fillText(lines[t], el.x, el.y + t*((el.fontSize||18)*1.35));
  } else if (el.type === "image"){
    var img = imgCache[el.src];
    if (!img){
      img = new Image(); img.crossOrigin = "anonymous";
      img.onload = function(){ S.drawDirty = true; paint(); };
      img.src = el.src; imgCache[el.src] = img;
    }
    if (img.complete && img.naturalWidth) ctx.drawImage(img, el.x, el.y, el.w||240, el.h||160);
    else { ctx.fillStyle="rgba(0,0,0,.06)"; ctx.fillRect(el.x, el.y, el.w||240, el.h||160); }
  } else if (el.type === "file"){
    ctx.fillStyle = "#fff";
    ctx.strokeStyle = "rgba(0,0,0,.12)";
    ctx.lineWidth = 1;
    roundRect(el.x, el.y, el.w||220, el.h||64, 10); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#1e293b";
    ctx.font = "600 12px Poppins, sans-serif";
    ctx.fillText((el.title||"File").slice(0,28), el.x+14, el.y+24);
    ctx.fillStyle = "#64748b";
    ctx.font = "11px Poppins, sans-serif";
    ctx.fillText(el.kind || "Document", el.x+14, el.y+42);
  }
  if (on){
    var b = bounds(el); if (b){
      ctx.setLineDash([5/S.view.scale, 4/S.view.scale]);
      ctx.strokeStyle = "#2563eb"; ctx.lineWidth = 1.5/S.view.scale;
      ctx.strokeRect(b.x-6, b.y-6, b.w+12, b.h+12);
      ctx.setLineDash([]);
    }
  }
  ctx.restore();
}
function roundRect(x,y,w,h,r){
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(x,y,w,h,r);
  else { ctx.rect(x,y,w,h); }
}
function wrap(text, x, y, maxW, lh){
  ctx.textBaseline = "top";
  var words = String(text).split(" "), line="", cy=y;
  for (var i=0;i<words.length;i++){
    var test = line + words[i] + " ";
    if (ctx.measureText(test).width > maxW && line){ ctx.fillText(line.trim(), x, cy); line = words[i]+" "; cy += lh; }
    else line = test;
  }
  if (line.trim()) ctx.fillText(line.trim(), x, cy);
}

function paint(){
  if (!ctx) return;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,vw,vh);
  applyCam();
  for (var i=0;i<S.objects.length;i++) drawEl(S.objects[i], S.objects[i].id === selectedId);
  if (drawing && path.length > 1 && (S.tool==="pen"||S.tool==="highlighter"||S.tool==="marker")){
    drawEl({ type:S.tool, points:path, color:S.drawColor, lineWidth: S.tool==="highlighter"?18:S.drawWidth });
  }
  if (drawing && shape0 && last && (S.tool==="rect"||S.tool==="ellipse"||S.tool==="line"||S.tool==="arrow")){
    drawEl({
      type:S.tool, x:Math.min(shape0.x,last.x), y:Math.min(shape0.y,last.y),
      w:Math.abs(last.x-shape0.x), h:Math.abs(last.y-shape0.y),
      x1:shape0.x, y1:shape0.y, x2:last.x, y2:last.y,
      stroke:S.drawColor, lineWidth:S.drawWidth
    });
  }
  S.drawDirty = false;
}
function loop(){
  if (S.drawDirty) paint();
  if (window._canvasWidgets) window._canvasWidgets.sync();
  requestAnimationFrame(loop);
}

function add(el){
  S.objects.push(el);
  S.drawDirty = true;
  C.emit("objects", S.objects);
  persist();
  if (window.CanvasCollab && window.CanvasCollab.pushObject) window.CanvasCollab.pushObject(el);
}
function removeAt(i){
  var el = S.objects[i];
  if (!el) return;
  S.objects.splice(i,1);
  selectedId = "";
  S.drawDirty = true;
  persist();
  if (window.CanvasCollab && window.CanvasCollab.removeObject) window.CanvasCollab.removeObject(el.id);
}
function persist(){
  clearTimeout(saveTimer);
  saveTimer = setTimeout(flush, 500);
}
function flush(){
  if (S.readOnly) return;
  try { localStorage.setItem("canvas_objects_"+(S.boardId||"local"), JSON.stringify(S.objects)); } catch(e){}
  if (!S.isAuth || !S.boardId || String(S.boardId).indexOf("local_")===0) return;
  C.api("/ajax/canvas/boards/"+encodeURIComponent(S.boardId)+"/objects/", {
    method:"POST", body: JSON.stringify({ objects: S.objects })
  }).catch(function(){});
}
function loadLocal(){
  try {
    var raw = localStorage.getItem("canvas_objects_"+(S.boardId||"local"));
    if (raw){ var arr = JSON.parse(raw); if (Array.isArray(arr)) S.objects = arr; }
  } catch(e){}
  S.drawDirty = true;
}
function loadFromServer(){
  if (!S.isAuth || !S.boardId || String(S.boardId).indexOf("local_")===0){ loadLocal(); return; }
  C.api("/ajax/canvas/boards/"+encodeURIComponent(S.boardId)+"/objects/list/", {method:"GET"}).then(function(d){
    if (d.objects && d.objects.length) S.objects = d.objects;
    else loadLocal();
    S.drawDirty = true;
  }).catch(loadLocal);
}

function setTool(id){
  S.tool = id || "select";
  selectedId = "";
  layer.style.pointerEvents = intercept() ? "auto" : "none";
  layer.style.cursor = S.tool === "pan" ? "grab" : (S.tool === "text" ? "text" : (intercept() ? "crosshair" : "default"));
  if (E.viewport){
    E.viewport.classList.toggle("tool-draw", intercept());
    E.viewport.classList.toggle("tool-pan", S.tool === "pan");
  }
  paintDock();
  S.drawDirty = true;
}

function paintDock(){
  var wheel = window.canvasWheel;
  if (!wheel || !wheel.setDock) return;
  var drawish = S.tool==="pen"||S.tool==="highlighter"||S.tool==="marker"||S.tool==="rect"||S.tool==="ellipse"||S.tool==="line"||S.tool==="arrow"||S.tool==="text";
  if (!drawish){ wheel.setDock(""); return; }
  var html = "";
  COLORS.forEach(function(c){
    html += '<button type="button" class="rw-swatch'+(c===S.drawColor?" is-on":"")+'" data-color="'+c+'" style="background:'+c+'"></button>';
  });
  WIDTHS.forEach(function(w){
    html += '<button type="button" class="rw-stroke'+(w===S.drawWidth?" is-on":"")+'" data-width="'+w+'"><i style="width:'+Math.min(w*1.6,16)+'px;height:'+Math.max(2,w/2)+'px"></i></button>';
  });
  wheel.setDock(html);
  var dock = wheel._dock;
  if (!dock) return;
  dock.onclick = function(e){
    var sw = e.target.closest("[data-color]");
    if (sw){ S.drawColor = sw.dataset.color; paintDock(); }
    var st = e.target.closest("[data-width]");
    if (st){ S.drawWidth = parseInt(st.dataset.width,10); paintDock(); }
  };
}

function promptText(seed, done){
  var v = window.prompt("Text", seed || "");
  if (v === null) return;
  done(v);
}

fileInput.addEventListener("change", function(){
  var f = fileInput.files && fileInput.files[0];
  fileInput.value = "";
  if (!f) return;
  var isImg = /^image\//.test(f.type);
  var reader = new FileReader();
  reader.onload = function(){
    if (isImg){
      var img = new Image();
      img.onload = function(){
        var w = Math.min(360, img.naturalWidth);
        var h = w * (img.naturalHeight / img.naturalWidth);
        add({ id:uid(), type:"image", src: reader.result, x:placeAt.x-w/2, y:placeAt.y-h/2, w:w, h:h });
      };
      img.src = reader.result;
    } else {
      add({ id:uid(), type:"file", title:f.name, kind:(f.type||"file").split("/").pop(), x:placeAt.x-110, y:placeAt.y-32, w:220, h:64, url: reader.result });
    }
  };
  if (isImg) reader.readAsDataURL(f);
  else if (f.size < 1.5e6) reader.readAsDataURL(f);
  else add({ id:uid(), type:"file", title:f.name, kind:"file", x:placeAt.x-110, y:placeAt.y-32, w:220, h:64 });
});

layer.addEventListener("pointerdown", function(e){
  if (S.readOnly) return;
  if (S.tool === "select") return;
  if (S.tool === "pan") return;
  e.preventDefault();
  e.stopPropagation();
  var wp = world(e);
  if (isWidgetTool(S.tool) && window.CanvasWidgets){
    var wdg = window.CanvasWidgets.create(S.tool, wp.x, wp.y);
    wdg.x -= (wdg.w || 280) / 2;
    wdg.y -= (wdg.h || 180) / 2;
    add(wdg);
    setTool("select");
    if (window.canvasWheel && window.canvasWheel.setActive) window.canvasWheel.setActive("select");
    return;
  }
  if (S.tool === "image" || S.tool === "file"){
    placeAt = wp; fileInput.click(); return;
  }
  if (S.tool === "sticky"){
    add({ id:uid(), type:"sticky", x:wp.x-80, y:wp.y-60, w:160, h:120, text:"", bg: STICKY[0] });
    var lastEl = S.objects[S.objects.length-1];
    promptText("", function(t){ lastEl.text = t; S.drawDirty = true; persist(); });
    return;
  }
  if (S.tool === "text"){
    add({ id:uid(), type:"text", x:wp.x, y:wp.y, text:"", color:S.drawColor, fontSize:18 });
    var te = S.objects[S.objects.length-1];
    promptText("", function(t){ te.text = t; S.drawDirty = true; persist(); });
    return;
  }
  if (S.tool === "eraser" || S.tool === "lasso"){
    drawing = true;
    var i = hit(wp.x, wp.y);
    if (i >= 0) removeAt(i);
    return;
  }
  drawing = true;
  path = [{x:wp.x,y:wp.y}];
  shape0 = {x:wp.x,y:wp.y};
  last = {x:wp.x,y:wp.y};
  try { layer.setPointerCapture(e.pointerId); } catch(err){}
});
layer.addEventListener("pointermove", function(e){
  if (!drawing) return;
  var wp = world(e);
  last = wp;
  if (S.tool === "eraser" || S.tool === "lasso"){
    var i = hit(wp.x, wp.y);
    if (i >= 0) removeAt(i);
    return;
  }
  if (S.tool === "pen" || S.tool === "highlighter" || S.tool === "marker"){
    path.push(wp);
  }
  S.drawDirty = true;
});
layer.addEventListener("pointerup", function(){
  if (!drawing) return;
  if ((S.tool==="pen"||S.tool==="highlighter"||S.tool==="marker") && path.length>1){
    add({ id:uid(), type:S.tool, points:path.slice(), color:S.drawColor, lineWidth: S.tool==="highlighter"?18:S.drawWidth });
  }
  if (shape0 && last && (S.tool==="rect"||S.tool==="ellipse"||S.tool==="line"||S.tool==="arrow")){
    if (Math.abs(last.x-shape0.x)>4 || Math.abs(last.y-shape0.y)>4){
      if (S.tool==="rect"||S.tool==="ellipse"){
        add({ id:uid(), type:S.tool, x:Math.min(shape0.x,last.x), y:Math.min(shape0.y,last.y), w:Math.abs(last.x-shape0.x), h:Math.abs(last.y-shape0.y), stroke:S.drawColor, lineWidth:S.drawWidth });
      } else {
        add({ id:uid(), type:S.tool, x1:shape0.x, y1:shape0.y, x2:last.x, y2:last.y, stroke:S.drawColor, lineWidth:S.drawWidth });
      }
    }
  }
  drawing = false; path = []; shape0 = null; last = null;
});

window.addEventListener("keydown", function(e){
  var tag = (e.target && e.target.tagName) || "";
  if (tag === "INPUT" || tag === "TEXTAREA") return;
  if ((e.key === "Delete" || e.key === "Backspace") && selectedId){
    var i = S.objects.findIndex(function(o){ return o.id === selectedId; });
    if (i >= 0) removeAt(i);
  }
});

C.on("view", function(){ S.drawDirty = true; });
C.on("board", function(){ loadFromServer(); });

window.CanvasDraw = {
  setTool: setTool,
  add: add,
  objects: function(){ return S.objects; },
  replace: function(arr){ S.objects = Array.isArray(arr)?arr:[]; S.drawDirty = true; },
  persist: persist,
  paint: function(){ S.drawDirty = true; }
};

resize();
loadFromServer();
requestAnimationFrame(loop);
window.addEventListener("resize", resize);
if (E.viewport){
  var ro = new ResizeObserver(resize);
  ro.observe(E.viewport);
}

var host = document.getElementById("cvToolGroups") || document.getElementById("canvasRadialHost");
if (host && (window.ToolGroups || window.RadialWheel)){
  var Ctor = window.ToolGroups || window.RadialWheel;
  window.canvasWheel = new Ctor({
    host: host,
    bare: true,
    active: "select",
    onChange: function(id){ setTool(id); }
  });
  setTool("select");
}

if (window.CanvasWidgets && E.viewport){
  var widgetBoard = {
    root: E.viewport,
    get elements(){ return S.objects; },
    get camera(){ return { x: S.view.x, y: S.view.y, zoom: S.view.scale }; },
    get tool(){ return S.tool; },
    get selectedIdx(){
      for (var i = 0; i < S.objects.length; i++) if (S.objects[i].id === selectedId) return i;
      return -1;
    },
    set selectedIdx(i){
      selectedId = (i >= 0 && S.objects[i]) ? S.objects[i].id : "";
      S.drawDirty = true;
    },
    persist: persist,
    s2w: function(x, y){ return C.s2w(x, y); },
    xy: function(e){
      var r = E.viewport.getBoundingClientRect();
      return { x: e.clientX - r.left, y: e.clientY - r.top };
    },
    markDirty: function(){ S.drawDirty = true; }
  };
  window._canvasWidgets = new window.CanvasWidgets(widgetBoard);
}
})();

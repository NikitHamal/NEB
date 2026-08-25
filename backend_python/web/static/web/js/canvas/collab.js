(function(){
"use strict";
var C = window.CanvasCore;
if (!C) return;
var S = C.state;
var cursorsEl = document.getElementById("canvasCursors");
if (!cursorsEl && C.els.viewport){
  cursorsEl = document.createElement("div");
  cursorsEl.id = "canvasCursors";
  cursorsEl.className = "rw-cursors";
  C.els.viewport.appendChild(cursorsEl);
}

var yinst = null;
var yarray = null;
var applying = false;
var presence = {};
var color = "#3182ce";

function canLive(){
  return !S.readOnly && S.isAuth && S.boardId && String(S.boardId).indexOf("local_") !== 0 && window.Y;
}

function init(){
  teardown();
  if (!canLive()) return;
  if (typeof SSYjs === "function"){
    yinst = new SSYjs();
    yinst.channelPrefix = "canvas.";
    if (typeof yinst.initWithChannel === "function"){
      yinst.initWithChannel("canvas." + S.boardId, "", (window.CANVAS_CONFIG && window.CANVAS_CONFIG.username) || "You");
    } else {
      yinst.init(S.boardId, "", (window.CANVAS_CONFIG && window.CANVAS_CONFIG.username) || "You");
      yinst.spaceId = S.boardId;
      yinst._channel = "canvas." + S.boardId;
    }
    if (yinst.doc){
      yarray = yinst.doc.getArray("canvas_objects");
      yarray.observe(function(evt, tr){
        if (tr.origin === "local" || applying) return;
        applying = true;
        try {
          var next = [];
          for (var i=0;i<yarray.length;i++){
            try { next.push(JSON.parse(JSON.stringify(yarray.get(i)))); } catch(e){}
          }
          if (window.CanvasDraw) window.CanvasDraw.replace(next);
          S.objects = next;
        } finally { applying = false; }
      });
    }
    yinst._onRemoteCursor = function(map){
      presence = map || {};
      paintCursors();
    };
  }
  startPresence();
}

function teardown(){
  if (yinst && yinst.disconnect) yinst.disconnect();
  yinst = null; yarray = null; presence = {};
  if (cursorsEl) cursorsEl.innerHTML = "";
}

function pushObject(el){
  if (!yarray || !yinst || !yinst.doc || applying) return;
  yinst.doc.transact(function(){ yarray.push([JSON.parse(JSON.stringify(el))]); }, "local");
}
function removeObject(id){
  if (!yarray || !yinst || !yinst.doc || applying) return;
  yinst.doc.transact(function(){
    for (var i=yarray.length-1;i>=0;i--){
      var it = yarray.get(i);
      if (it && it.id === id) yarray.delete(i, 1);
    }
  }, "local");
}

function paintCursors(){
  if (!cursorsEl) return;
  var html = "";
  var keys = Object.keys(presence);
  for (var i=0;i<keys.length;i++){
    var c = presence[keys[i]];
    if (!c) continue;
    var sp = C.w2s(c.start || 0, c.end || 0);
    var col = c.color || color;
    html += '<div class="rw-cursor" style="left:'+sp.x+'px;top:'+sp.y+'px;color:'+col+'">' +
      '<svg width="16" height="20" viewBox="0 0 16 20"><path d="M1 1 L1 17 L6 12 L10 19 L13 17.5 L9 10.5 L15 10 Z" fill="'+col+'"/></svg>' +
      '<div class="rw-cursor-label" style="background:'+col+'">'+(c.name||"Someone")+'</div></div>';
  }
  cursorsEl.innerHTML = html;
}

function startPresence(){
  if (!C.els.viewport) return;
  C.els.viewport.addEventListener("pointermove", function(e){
    if (!yinst || !yinst._sendAwareness) return;
    var r = C.els.viewport.getBoundingClientRect();
    var w = C.s2w(e.clientX - r.left, e.clientY - r.top);
    yinst._sendAwareness(Math.round(w.x), Math.round(w.y));
  }, { passive: true });
}

C.on("board", function(){ init(); });
C.on("view", function(){ paintCursors(); });

window.CanvasCollab = {
  init: init,
  pushObject: pushObject,
  removeObject: removeObject,
  live: canLive
};

if (S.boardId) setTimeout(init, 80);
})();

(function(){
"use strict";
var C=window.CanvasCore;if(!C){return}
var S=C.state;
var $=function(id){return document.getElementById(id)};
var G={
  prompt:$("globalPrompt"),send:$("globalSendBtn"),
  selPop:$("selectionPop"),mini:$("miniPrompt"),miniInput:$("miniPromptInput"),miniSend:$("miniPromptSend"),
  boardModal:$("boardModal"),boardInput:$("boardModalInput"),boardCreate:$("boardModalCreate"),boardCancel:$("boardModalCancel"),
  newBtn:$("csNewBoardBtn"),shareBtn:$("csShareBtn"),collapseBtn:$("csCollapseBtn"),mobileToggle:$("csMobileToggle"),
  viewport:$("canvasViewport"),ctxMenu:$("ctxMenu"),highlightsBtn:$("cvHighlightsBtn")
};
var selData={text:"",nodeId:""};
var miniData={parentId:"",dir:"",x:0,y:0,sx:0,sy:0};
var miniOpen=false;

/* ── global bar ──────────────────────────────────────────── */
function autoSize(el){
  if(!el) return;
  el.style.height="auto";
  var newH=Math.min(el.scrollHeight||22,120);
  var val=typeof el.value==="string"?el.value.trim():"";
  el.style.height=(val?newH:22)+"px";
  var parent=typeof el.closest==="function"?el.closest(".cb-bar-inner"):null;
  if(parent){
    if(newH>32){
      parent.classList.add("multi-line");
    }else{
      parent.classList.remove("multi-line");
    }
  }
}
if(G.prompt){
  G.prompt.addEventListener("input",function(){autoSize(this);if(G.send)G.send.disabled=!this.value.trim()});
  G.prompt.addEventListener("keydown",function(e){
    if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();doSend()}
  });
  setTimeout(function(){autoSize(G.prompt)},40);
}
if(G.send) G.send.addEventListener("click",doSend);
function doSend(){
  if(!G.prompt||S.readOnly) return;
  var v=G.prompt.value.trim();if(!v) return;
  G.prompt.value="";autoSize(G.prompt);if(G.send)G.send.disabled=true;
  C.createRoot(v);
}

/* ── sidebar buttons ─────────────────────────────────────── */
function updateCollapseUI(isCollapsed){
  var sb=$("canvasSidebar");
  if(!sb) return;
  if(isCollapsed){
    sb.classList.add("collapsed");
  }else{
    sb.classList.remove("collapsed");
  }
  if(G.collapseBtn){
    var icon=G.collapseBtn.querySelector(".material-symbols-outlined");
    if(icon){
      icon.textContent=isCollapsed?"dock_to_right":"dock_to_left";
    }
    G.collapseBtn.title=isCollapsed?"Expand sidebar":"Collapse sidebar";
    G.collapseBtn.setAttribute("aria-label",isCollapsed?"Expand sidebar":"Collapse sidebar");
  }
}

if(G.newBtn&&!S.readOnly) G.newBtn.addEventListener("click",openBoardModal);
if(G.collapseBtn&&!window.matchMedia("(max-width:900px)").matches){
  var stored="0";
  try{stored=localStorage.getItem("canvas_sidebar_collapsed")||"0"}catch(e){}
  updateCollapseUI(stored==="1");
  G.collapseBtn.addEventListener("click",function(){
    var sb=$("canvasSidebar");
    var on=!sb.classList.contains("collapsed");
    updateCollapseUI(on);
    try{localStorage.setItem("canvas_sidebar_collapsed",on?"1":"0")}catch(e){}
    setTimeout(function(){C.renderEdges&&C.renderEdges()},240);
  });
}
var logoMark=document.querySelector(".cs-logo-mark");
if(logoMark){
  logoMark.addEventListener("click",function(){
    var sb=$("canvasSidebar");
    if(sb&&sb.classList.contains("collapsed")){
      updateCollapseUI(false);
      try{localStorage.setItem("canvas_sidebar_collapsed","0")}catch(e){}
      setTimeout(function(){C.renderEdges&&C.renderEdges()},240);
    }
  });
}
if(G.mobileToggle) G.mobileToggle.addEventListener("click",function(){$("canvasSidebar").classList.toggle("open")});
document.addEventListener("click",function(e){
  if(window.innerWidth<=900){
    var sb=$("canvasSidebar");
    if(sb&&sb.classList.contains("open")&&!sb.contains(e.target)&&!(G.mobileToggle&&G.mobileToggle.contains(e.target))) sb.classList.remove("open");
  }
});

/* share */
if(G.shareBtn&&!S.readOnly){
  G.shareBtn.addEventListener("click",function(){
    if(!S.boardId||String(S.boardId).indexOf("local_")===0){C.showToast("Create a canvas first — ask something!",true);return}
    G.shareBtn.disabled=true;
    C.api("/ajax/canvas/boards/"+S.boardId+"/share/",{method:"POST",body:"{}"}).then(function(d){
      var url=location.origin+d.url;
      return C.copyText(url).then(function(){
        C.showToast("View-only link copied — anyone can open it");
      },function(){C.showToast("Link ready: "+url)});
    }).catch(function(err){C.showToast((err&&err.error)||"Share failed",true)})
      .finally(function(){G.shareBtn.disabled=false});
  });
}

/* ── board modal ─────────────────────────────────────────── */
function openBoardModal(){G.boardModal.hidden=false;G.boardInput.value="";G.boardCreate.disabled=true;setTimeout(function(){G.boardInput.focus()},40)}
function closeBoardModal(){G.boardModal.hidden=true}
if(G.boardCancel) G.boardCancel.addEventListener("click",closeBoardModal);
G.boardModal&&G.boardModal.addEventListener("click",function(e){if(e.target===G.boardModal) closeBoardModal()});
if(G.boardInput){
  G.boardInput.addEventListener("input",function(){G.boardCreate.disabled=!this.value.trim()});
  G.boardInput.addEventListener("keydown",function(e){if(e.key==="Enter"&&!G.boardCreate.disabled) doBoardCreate();if(e.key==="Escape") closeBoardModal()});
}
if(G.boardCreate) G.boardCreate.addEventListener("click",doBoardCreate);
function doBoardCreate(){
  var t=G.boardInput.value.trim();if(!t) return;
  G.boardCreate.disabled=true;G.boardCreate.textContent="Creating…";
  C.createBoard(t).then(function(){closeBoardModal();C.showToast("Canvas created")})
   .catch(function(err){C.showToast((err&&err.error)||"Failed",true)})
   .finally(function(){G.boardCreate.disabled=false;G.boardCreate.textContent="Create"});
}

/* ── selection popup ─────────────────────────────────────── */
function hideSel(){if(G.selPop){G.selPop.hidden=true}selData.text="";selData.nodeId=""}
document.addEventListener("mouseup",function(e){
  if(S.readOnly) return;
  if(e.target.closest&&e.target.closest("#selectionPop")) return;
  setTimeout(evalSelection,28);
});
function evalSelection(){
  var sel=window.getSelection();
  if(!sel||sel.isCollapsed||sel.rangeCount===0){hideSel();return}
  var txt=sel.toString().trim();
  if(txt.length<3||txt.length>280){hideSel();return}
  var anc=sel.getRangeAt(0).startContainer.parentElement;
  var card=anc?anc.closest(".canvas-card"):null;
  var inside=anc?anc.closest(".text-block,.comp-table td,.card-ref-desc,.diagram-node-desc,.bullets-list li,.card-ref-title,.quote-text"):null;
  if(!card||!inside){hideSel();return}
  selData.text=txt;selData.nodeId=card.dataset.nodeId;
  G.selPop.hidden=false;
  requestAnimationFrame(function(){
    var r=sel.getRangeAt(0).getBoundingClientRect();
    if(!r.width&&!r.height){hideSel();return}
    var vw=window.innerWidth,pw=G.selPop.offsetWidth||240,ph=G.selPop.offsetHeight||46;
    G.selPop.style.left=Math.max(8,Math.min(vw-pw-8,r.left+r.width/2-pw/2))+"px";
    G.selPop.style.top=(r.bottom+10+ph+16>window.innerHeight?r.top-ph-10:r.bottom+10)+"px";
  });
}
document.addEventListener("mousedown",function(e){
  if(e.target.closest&&e.target.closest("#selectionPop")) return;
  hideSel();
},true);
var __selChgT=null;
document.addEventListener("selectionchange",function(){
  var s=window.getSelection();
  if(!s||s.isCollapsed){hideSel();return}
  if(window.matchMedia("(hover:none)").matches){
    clearTimeout(__selChgT);
    __selChgT=setTimeout(function(){if(!miniOpen) evalSelection()},340);
  }
});
window.addEventListener("scroll",hideSel,true);
G.viewport&&G.viewport.addEventListener("wheel",hideSel,{passive:true});
C.on&&C.on("view",hideSel);C.on&&C.on("pan-start",hideSel);C.on&&C.on("card-drag-start",hideSel);

if(G.selPop){
  G.selPop.querySelector('[data-action="dig-deeper"]').addEventListener("click",function(){
    var t=selData.text,nid=selData.nodeId;
    var sel=window.getSelection();
    var rng=(sel&&sel.rangeCount)?sel.getRangeAt(0).cloneRange():null;
    hideSel();window.getSelection().removeAllRanges();
    if(!t||!nid) return;
    var p=S.nodes.get(nid);if(!p) return;
    digDeeper(nid,t,p,rng);
  });
  G.selPop.querySelector('[data-action="save-highlight"]').addEventListener("click",function(){
    var t=selData.text;hideSel();
    if(!t) return;
    try{var a=JSON.parse(localStorage.getItem("canvas_highlights")||"[]");a.push({text:t,at:Date.now(),nodeId:selData.nodeId,boardId:S.boardId});localStorage.setItem("canvas_highlights",JSON.stringify(a))}catch(e){}
    C.showToast("Highlight saved");window.getSelection().removeAllRanges();
  });
}
function nodeW(id){var el=document.getElementById("node_"+id);return el&&el.offsetWidth?el.offsetWidth:560}
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function _wrapRangeWithDig(range, parentId, tmpId, text){
  if(!range) return null;
  try{
    var span=document.createElement("span");
    span.className="cv-dig-source";
    span.dataset.child=tmpId;
    span.dataset.parent=parentId;
    span.title="Open linked card";
    span.addEventListener("click",function(e){
      e.stopPropagation();
      var cid=span.dataset.child;
      if(cid&&S.nodes.has(cid)){
        C.selectNode(cid);
        var n=S.nodes.get(cid);
        if(n){
          var el=document.getElementById("node_"+cid);
          var h=C.state.heights[cid]||420;
          var vw=G.viewport.clientWidth,vh=G.viewport.clientHeight;
          var sc=Math.max(.65,Math.min(1.05,C.state.view.scale));
          var w=el&&el.offsetWidth?el.offsetWidth:560;
          C.animateTo(vw/2-(n.x+w/2)*sc, vh/2-(n.y+h/2)*sc, sc);
          el&&el.classList.add("selected");
          setTimeout(function(){el&&el.classList.remove("selected")},1600);
        }
      }else{
        // try to find by text if tmp still pending
        C.showToast("Linked card opening…");
      }
    });
    try{
      span.appendChild(range.extractContents());
      range.insertNode(span);
    }catch(e){
      try{ range.surroundContents(span);}catch(e2){ return null; }
    }
    try{
      var links=JSON.parse(localStorage.getItem("canvas_dig_links")||"[]");
      links.push({boardId:S.boardId, parentId:parentId, childId:tmpId, text:text, at:Date.now()});
      localStorage.setItem("canvas_dig_links", JSON.stringify(links.slice(-200)));
    }catch(e){}
    return span;
  }catch(e){ return null; }
}
function _updateDigLink(tmpId, realId){
  try{
    var links=JSON.parse(localStorage.getItem("canvas_dig_links")||"[]");
    var changed=false;
    links.forEach(function(l){ if(l.childId===tmpId){ l.childId=realId; changed=true; }});
    if(changed) localStorage.setItem("canvas_dig_links", JSON.stringify(links));
  }catch(e){}
  try{
    var span=document.querySelector('.cv-dig-source[data-child="'+tmpId+'"]');
    if(span) span.dataset.child=realId;
  }catch(e){}
}
function _reapplyDigHighlights(){
  try{
    var links=JSON.parse(localStorage.getItem("canvas_dig_links")||"[]");
    links.forEach(function(l){
      if(l.boardId!==S.boardId) return;
      if(document.querySelector('.cv-dig-source[data-child="'+l.childId+'"]')) return;
      var parentEl=document.getElementById("node_"+l.parentId);
      if(!parentEl) return;
      var body=parentEl.querySelector(".card-body");
      if(!body||!l.text) return;
      var walker=document.createTreeWalker(body, NodeFilter.SHOW_TEXT, null);
      var node, found=false;
      while(node=walker.nextNode()){
        var idx=node.nodeValue.indexOf(l.text);
        if(idx!==-1){
          var range=document.createRange();
          range.setStart(node, idx);
          range.setEnd(node, idx+l.text.length);
          var span=document.createElement("span");
          span.className="cv-dig-source";
          span.dataset.child=l.childId;
          span.dataset.parent=l.parentId;
          span.title="Open linked card";
          span.textContent=l.text;
          span.addEventListener("click",function(e){
            e.stopPropagation();
            var cid=span.dataset.child;
            if(cid&&S.nodes.has(cid)){
              var n=S.nodes.get(cid);
              var el=document.getElementById("node_"+cid);
              var h=C.state.heights[cid]||420;
              var vw=G.viewport.clientWidth,vh=G.viewport.clientHeight;
              var sc=Math.max(.65,Math.min(1.05,C.state.view.scale));
              var w=el&&el.offsetWidth?el.offsetWidth:560;
              C.animateTo(vw/2-(n.x+w/2)*sc, vh/2-(n.y+h/2)*sc, sc);
              C.selectNode(cid);
            }
          });
          try{
            range.deleteContents();
            range.insertNode(span);
          }catch(e){}
          found=true;
          break;
        }
      }
    });
  }catch(e){}
}
function digDeeper(parentNode,text,p,range){
  var wx=p.x+nodeW(parentNode)+48,wy=p.y+64;
  var sib=0;S.nodes.forEach(function(v){if(v.parentId===parentNode)sib++});wy+=sib*14;
  var ph={id:"tmp_"+Date.now(),boardId:S.boardId,parentId:parentNode,prompt:"Explain '"+text+"'",title:"",content:{title:"",summary:"",sections:[]},status:"generating",x:wx,y:wy};
  var digSpan=_wrapRangeWithDig(range, parentNode, ph.id, text);
  S.nodes.set(ph.id,ph);C.renderNode(ph);C.updateEmpty();C.renderEdges();
  centerOn(ph,wx,wy);
  if(!S.isAuth){
    setTimeout(function(){
      var m=C.mockLocal(text.toLowerCase().indexOf("world")>-1?"world model":text.toLowerCase());
      var real={id:"local_"+Date.now(),boardId:S.boardId,parentId:parentNode,prompt:"Explain '"+text+"'",title:m.title,content:m,status:"done",x:wx,y:wy};
      _updateDigLink(ph.id, real.id);
      swap(ph,real);
    },600);
    return;
  }
  C.api("/ajax/canvas/nodes/"+parentNode+"/dig-deeper/",{method:"POST",body:JSON.stringify({selected_text:text,x:wx,y:wy})}).then(function(d){
    d.node.x=wx;d.node.y=wy;_updateDigLink(ph.id, d.node.id);swap(ph,d.node);
  }).catch(function(err){
    ph.status="done";
    ph.content={title:"Failed",summary:(err&&err.error)||"Dig deeper failed",sections:[]};
    var old=document.getElementById("node_"+ph.id);if(old) old.remove();
    S.nodes.set(ph.id,ph);C.renderNode(ph);C.showToast((err&&err.error)||"Dig deeper failed",true);
    try{ var s=document.querySelector('.cv-dig-source[data-child="'+ph.id+'"]'); if(s) s.remove(); }catch(e){}
  });
}
function centerOn(ph,wx,wy){
  var vw=G.viewport.clientWidth,vh=G.viewport.clientHeight,target=clamp(S.view.scale,0.65,1);
  var w=nodeW(ph.id);
  C.animateTo(vw/2-(wx+w/2)*target,vh/2-(wy+140)*target,target);
}
function swap(ph,real){
  var old=document.getElementById("node_"+ph.id);if(old) old.remove();S.nodes.delete(ph.id);
  S.nodes.set(real.id,real);C.renderNode(real);C.renderEdges();
}

/* ── mini prompt (anchor click / wire drop / new thread here) ── */
function openMini(payload){
  miniData=payload;miniOpen=true;
  G.mini.hidden=false;
  var w=G.mini.offsetWidth||300,h=G.mini.offsetHeight||48;
  var x,y;
  if(payload.sx!=null){x=payload.sx-w/2;y=payload.sy+16}
  else{var s=C.w2s(payload.x,payload.y);x=s.x;y=s.y}
  x=Math.max(8,Math.min(window.innerWidth-w-8,x));
  y=Math.max(8,Math.min(window.innerHeight-h-80,y));
  G.mini.style.left=x+"px";G.mini.style.top=y+"px";
  G.miniInput.value="";G.miniSend.disabled=true;
  G.miniInput.placeholder=payload.parentId?"Ask a follow-up…":"What should this thread explore?";
  setTimeout(function(){G.miniInput.focus()},30);
}
function closeMini(){G.mini.hidden=true;miniOpen=false;miniData={parentId:"",dir:"",x:0,y:0,sx:0,sy:0}}
if(G.mini){
  G.miniInput.addEventListener("input",function(){G.miniSend.disabled=!this.value.trim()});
  G.miniInput.addEventListener("keydown",function(e){
    if(e.key==="Enter"){e.preventDefault();miniGo()}
  });
  G.miniSend.addEventListener("click",miniGo);
  function miniGo(){
    var v=G.miniInput.value.trim();if(!v) return;
    var p=miniData;closeMini();
    if(p.parentId) C.createChild(p.parentId,v,{x:p.x,y:p.y,dir:p.dir});
    else C.createRoot(v,p.x,p.y);
  }
  document.addEventListener("pointerdown",function(e){
    if(miniOpen&&!G.mini.contains(e.target)&&!(e.target.closest&&e.target.closest(".anchor"))) closeMini();
  },true);
  C.on&&C.on("view",function(){if(miniOpen) closeMini()});
  C.on&&C.on("wire-drop",function(payload){if(!S.readOnly) openMini(payload)});
  C.on&&C.on("anchor-click",function(payload){if(!S.readOnly){
    // position child near the clicked side
    var p=S.nodes.get(payload.parentId);
    if(!p) return;
    var h=S.heights[pay(p)]||420;
    function pay(x){return x}
    var pw2=nodeW(payload.parentId);
    var off={top:[p.x,p.y-500],bottom:[p.x,p.y+h+56],left:[p.x-pw2-48,p.y+64],right:[p.x+pw2+48,p.y+64]}[payload.dir]||[p.x,p.y+h+56];
    openMini({parentId:payload.parentId,dir:payload.dir,x:off[0],y:off[1],sx:payload.sx,sy:payload.sy});
  }});
}

/* ── right-click context menu ────────────────────────────── */
var MENU=[
  ["zoom_in","zoom_in","Zoom in","+"],
  ["zoom_out","zoom_out","Zoom out","−"],
  ["fit","fit_screen","Fit view","F"],
  ["sep"],
  ["reset","restart_alt","Reset zoom","0"],
  ["sep"],
  ["newthread","add_circle","New thread here","N"]
];
var MENU_CARD=[
  ["focus_card","center_focus_strong","Center card","F"],
  ["copy_prompt","content_copy","Copy prompt",""],
  ["dup","control_point_duplicate","Duplicate thread",""],
  ["sep"],
  ["del","delete","Delete card","Del","danger"]
];
function showMenu(items,x,y,nodeId){
  var m=G.ctxMenu;m.innerHTML="";
  items.forEach(function(it){
    if(it[0]==="sep"){var s=document.createElement("div");s.className="ctx-sep";m.appendChild(s);return}
    var actName=it[0], iconName=it[1], label=it[2], kbd=it[3], extraClass=it[4];
    var b=document.createElement("button");
    b.className="ctx-item"+(extraClass?" "+extraClass:"");
    b.innerHTML='<span class="material-symbols-outlined" style="font-size:17px">'+iconName+'</span><span>'+label+'</span>'+(kbd?'<kbd>'+kbd+'</kbd>':'');
    b.addEventListener("click",function(ev){ev.stopPropagation();hideMenu();act(actName,nodeId)});
    m.appendChild(b);
  });
  if(!nodeId){var n=document.createElement("div");n.className="ctx-note";n.textContent="Tip: drag blue + ports to draw threads · Ctrl+scroll zooms";m.appendChild(n)}
  m.hidden=false;
  var mw=m.offsetWidth||200,mh=m.offsetHeight||220;
  m.style.left=Math.max(6,Math.min(window.innerWidth-mw-6,x))+"px";
  m.style.top=Math.max(6,Math.min(window.innerHeight-mh-6,y))+"px";
}
function hideMenu(){if(G.ctxMenu) G.ctxMenu.hidden=true}
function act(name,nodeId){
  switch(name){
    case "zoom_in":C.zoomCenter(1.18);break;
    case "zoom_out":C.zoomCenter(1/1.18);break;
    case "fit":C.fitView();break;
    case "reset":{var vw0=G.viewport.clientWidth,vh0=G.viewport.clientHeight,cx=(vw0/2-S.view.x)/S.view.scale,cy=(vh0/2-S.view.y)/S.view.scale;C.animateTo(vw0/2-cx,vh0/2-cy,1);break}
    case "newthread":{
      var pt=pendingThreadAt||{x:window.innerWidth/2,y:window.innerHeight/2};
      var w=C.s2w(pt.x,pt.y);
      if(C.createEmptyRoot) C.createEmptyRoot(w.x-280,w.y-60);
      else if(G.prompt){G.prompt.focus()}
      break;
    }
    case "focus_card":if(nodeId)C.selectNode(nodeId),centerById(nodeId);break;
    case "copy_prompt":if(nodeId){var n=S.nodes.get(nodeId);if(n)C.copyText(n.prompt).then(function(){C.showToast("Prompt copied")})}break;
    case "dup":if(nodeId)C.duplicateNode(nodeId);break;
    case "del":if(nodeId)C.deleteNode(nodeId);break;
  }
}
function centerById(id){
  var n=S.nodes.get(id);if(!n) return;
  var h=S.heights[id]||420,vw=G.viewport.clientWidth,vh=G.viewport.clientHeight;
  C.animateTo(vw/2-(n.x+nodeW(id)/2)*S.view.scale,vh/2-(n.y+h/2)*S.view.scale,S.view.scale);
}
document.addEventListener("contextmenu",function(e){
  e.preventDefault();
  if(S.readOnly) return;
  if(e.target.closest&&e.target.closest(".card-head,.card-body")){
    var card=e.target.closest(".canvas-card");
    if(card){selectCard(card.dataset.nodeId);showMenu(MENU_CARD,e.clientX,e.clientY,card.dataset.nodeId);return}
  }
  if(e.target.closest&&e.target.closest(".canvas-card")) return;
  showMenu(MENU,e.clientX,e.clientY,null);
  pendingThreadAt={x:e.clientX,y:e.clientY};
});
var pendingThreadAt=null;
document.addEventListener("click",function(e){if(G.ctxMenu&&!G.ctxMenu.contains(e.target)) hideMenu()});
window.addEventListener("blur",hideMenu);
// wire "New thread here"
G.ctxMenu&&G.ctxMenu.addEventListener("click",function(){},true);

/* ── keyboard ────────────────────────────────────────────── */
document.addEventListener("keydown",function(e){
  var typing=e.target&&(e.target.tagName==="TEXTAREA"||e.target.tagName==="INPUT"||e.target.isContentEditable);
  if(e.key==="Escape"){
    if(G.ctxMenu&&!G.ctxMenu.hidden){hideMenu();return}
    if(miniOpen){closeMini();return}
    if(G.boardModal&&!G.boardModal.hidden){closeBoardModal();return}
    hideSel();return;
  }
  if(typing) return;
  if(S.readOnly){
    if(e.key==="f"||e.key==="F"){e.preventDefault();C.fitView()}
    return;
  }
  var k=e.key;
  if(k==="+"||k==="="){e.preventDefault();C.zoomCenter(1.15)}
  else if(k==="-"||k==="_"){e.preventDefault();C.zoomCenter(1/1.15)}
  else if(k==="0"){e.preventDefault();C.zoomCenter(1/S.view.scale)}
  else if(k==="f"||k==="F"){e.preventDefault();C.fitView()}
  else if(k==="Delete"||k==="Backspace"){
    if(S.selectedId){e.preventDefault();C.deleteNode(S.selectedId)}
  }else if(k.indexOf("Arrow")===0&&S.selectedId){
    e.preventDefault();
    var n=S.nodes.get(S.selectedId);if(!n) return;
    var step=e.shiftKey?4:24;
    if(k==="ArrowLeft")n.x-=step;if(k==="ArrowRight")n.x+=step;
    if(k==="ArrowUp")n.y-=step;if(k==="ArrowDown")n.y+=step;
    var el=document.getElementById("node_"+S.selectedId);
    if(el){el.style.left=n.x+"px";el.style.top=n.y+"px"}
    C.renderEdges();
    clearTimeout(window.__cvNudge);
    window.__cvNudge=setTimeout(function(){
      var nid=String(n.id),isDraft=nid.indexOf("draft_")===0||nid.indexOf("local_")===0||nid.indexOf("tmp_")===0;
      if(S.isAuth&&!isDraft)
        C.api("/ajax/canvas/nodes/"+n.id+"/move/",{method:"POST",body:JSON.stringify({x:n.x,y:n.y})}).catch(function(){});
      else if(!S.readOnly){
        try{localStorage.setItem("canvas_nodes_"+S.boardId,JSON.stringify(Array.from(S.nodes.values())))}catch(err){}
      }
    },400);
  }else if(k==="n"||k==="N"){
    // new thread at viewport center
    var c=C.s2w(G.viewport.clientWidth/2,G.viewport.clientHeight/2);
    openMini({parentId:S.selectedId,dir:"bottom",x:c.x-140,y:c.y-20,sx:G.viewport.clientWidth/2,sy:G.viewport.clientHeight/2});
  }
});
// ctx menu "New thread here" uses stored point
document.addEventListener("click",function(e){
  if(e.target.closest&&e.target.closest("#ctxMenu")){
    var item=e.target.closest(".ctx-item");if(!item) return;
    var label=item.querySelector("span:nth-child(2)");
    if(label&&label.textContent==="New thread here"&&pendingThreadAt){
      var r=G.viewport.getBoundingClientRect();
      var w=C.s2w(pendingThreadAt.x-r.left,pendingThreadAt.y-r.top);
      openMini({parentId:S.selectedId,dir:"bottom",x:w.x-140,y:w.y-16,sx:pendingThreadAt.x-r.left,sy:pendingThreadAt.y-r.top});
      pendingThreadAt=null;
    }
  }
},true);

function openHighlightsViewer(){
  var A=window.CanvasAdvanced;
  if(!A||!A.openPanel){ C.showToast("Highlights panel unavailable"); return; }
  var boardId=S.boardId;
  var hl=[]; try{ hl=JSON.parse(localStorage.getItem("canvas_highlights")||"[]"); }catch(e){ hl=[]; }
  var dig=[]; try{ dig=JSON.parse(localStorage.getItem("canvas_dig_links")||"[]"); }catch(e){ dig=[]; }
  var hlFiltered=hl.filter(function(h){ return !boardId||h.boardId===boardId||!h.boardId; });
  var digFiltered=dig.filter(function(l){ return !boardId||l.boardId===boardId; });
  if(!hlFiltered.length&&!digFiltered.length){
    A.openPanel("Highlights","Your canvas highlights",'<div class="cv-empty-state">No highlights yet. Select text on any card → <strong>Save highlight</strong> or <strong>Dig deeper</strong> to create highlights.</div>');
    return;
  }
  var html='<div style="display:flex;flex-direction:column;gap:14px">';
  if(hlFiltered.length){
    html+='<div class="cv-subhead">Saved highlights</div>';
    hlFiltered.slice(-30).reverse().forEach(function(h){
      var txt=C.esc(h.text);
      var node=S.nodes.get(h.nodeId);
      var title=node?C.esc(node.title||node.prompt.slice(0,40)):"Card";
      var dt=new Date(h.at||Date.now()).toLocaleDateString();
      html+='<div class="cv-suggestion"><div class="cv-suggestion-main"><div class="cv-suggestion-title" style="-webkit-line-clamp:3">'+txt+'</div><div class="cv-suggestion-why">From: '+title+' · '+dt+'</div></div><button data-jump-hl="'+C.esc(h.nodeId)+'" title="Go to card"><span class="material-symbols-outlined">center_focus_strong</span></button></div>';
    });
  }
  if(digFiltered.length){
    html+='<div class="cv-subhead">Dig deeper links</div>';
    digFiltered.slice(-30).reverse().forEach(function(l){
      var txt=C.esc(l.text);
      var p=S.nodes.get(l.parentId);
      var c=S.nodes.get(l.childId);
      var pTitle=p?C.esc(p.title||p.prompt.slice(0,30)):"Parent";
      var cTitle=c?C.esc(c.title||c.prompt.slice(0,30)):"Child";
      html+='<div class="cv-suggestion"><div class="cv-suggestion-main"><div class="cv-suggestion-title" style="-webkit-line-clamp:2">'+txt+'</div><div class="cv-suggestion-why">'+pTitle+' → '+cTitle+'</div></div><button data-jump-hl="'+C.esc(l.childId||l.parentId)+'" title="Open linked card"><span class="material-symbols-outlined">open_in_new</span></button></div>';
    });
  }
  html+='</div>';
  A.openPanel("Highlights","Your canvas highlights",html);
  setTimeout(function(){
    var body=document.getElementById("cvPanelBody");
    if(!body) return;
    body.querySelectorAll("[data-jump-hl]").forEach(function(b){
      b.addEventListener("click", function(){
        var nid=b.getAttribute("data-jump-hl");
        if(nid&&S.nodes.has(nid)){
          A.closePanel();
          var n=S.nodes.get(nid);
          var el=document.getElementById("node_"+nid);
          var h=C.state.heights[nid]||420;
          var vw=G.viewport.clientWidth, vh=G.viewport.clientHeight;
          var sc=Math.max(.65,Math.min(1.05,C.state.view.scale));
          var w=el&&el.offsetWidth?el.offsetWidth:560;
          C.animateTo(vw/2-(n.x+w/2)*sc, vh/2-(n.y+h/2)*sc, sc);
          C.selectNode(nid);
        } else {
          C.showToast("Card not found on this board");
        }
      });
    });
  },80);
}
if(G.highlightsBtn) G.highlightsBtn.addEventListener("click", openHighlightsViewer);
(function(){
  var fab=document.getElementById("cvNebyFab");
  if(!fab) return;
  var avatar=fab.querySelector("[data-neby-avatar]");
  var fallback=fab.querySelector(".cv-neby-fab-icon");
  if(avatar){
    var obs=new MutationObserver(function(){
      if(avatar.querySelector("canvas, svg")){
        if(fallback) fallback.style.display="none";
        avatar.style.display="block";
        obs.disconnect();
      }
    });
    try{ obs.observe(avatar,{childList:true,subtree:true}); }catch(e){}
    setTimeout(function(){ if(avatar.querySelector("canvas,svg")&&fallback){ fallback.style.display="none"; avatar.style.display="block"; } },1400);
  }
  fab.addEventListener("click", function(){
    var topBtn=document.getElementById("cvNebyBtn");
    if(topBtn){ topBtn.click(); return; }
    var A2=window.CanvasAdvanced;
    if(A2&&A2.openNeby) A2.openNeby();
  });
})();
if(C.on){ C.on("board", function(){ setTimeout(_reapplyDigHighlights, 320); }); }
setTimeout(_reapplyDigHighlights, 750);
var _origRenderHL=C.renderNode;
C.renderNode=function(n){ _origRenderHL(n); setTimeout(_reapplyDigHighlights, 50); };
function selectCard(id){C.selectNode(id,true)}
})();

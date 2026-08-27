(function(){
"use strict";
var cfg=window.CANVAS_CONFIG||{};
var S={
  boardId:cfg.boardId||"",
  isAuth:!!cfg.isAuthenticated,
  readOnly:!!cfg.readOnly,
  sharedToken:cfg.sharedToken||"",
  csrf:cfg.csrfToken||"",
  speedMode:"fast",
  nodes:new Map(),
  boards:new Map(),
  view:{x:0,y:0,scale:1},
  wire:null,
  dragging:null,
  selectedId:"",
  heights:{}
};
var E={
  sidebar:document.getElementById("canvasSidebar"),
  viewport:document.getElementById("canvasViewport"),
  world:document.getElementById("canvasWorld"),
  edges:document.getElementById("canvasEdges"),
  edgeLayer:document.getElementById("edgeLayer"),
  tempWire:document.getElementById("tempWire"),
  emptyHint:document.getElementById("canvasEmptyHint"),
  boardsEl:document.getElementById("csBoards"),
  toast:document.getElementById("toastPill")
};
var listeners={};
function on(ev,fn){(listeners[ev]=listeners[ev]||[]).push(fn)}
function emit(ev,d){(listeners[ev]||[]).forEach(function(fn){try{fn(d)}catch(e){}})}
function getCookie(name){
  var v=document.cookie.match('(^|;) ?'+name+'=([^;]*)(;|$)');
  if(v) return decodeURIComponent(v[2]);
  var inp=document.querySelector('input[name=csrfmiddlewaretoken]');
  return inp?inp.value:(S.csrf||"");
}
function api(path,opts){
  opts=opts||{};
  opts.headers=opts.headers||{};
  var csrf=getCookie("csrftoken")||S.csrf||"";
  if(csrf) opts.headers["X-CSRFToken"]=csrf;
  opts.headers["Content-Type"]="application/json";
  opts.credentials="same-origin";
  return fetch(path,opts).then(function(r){
    return r.json().catch(function(){return {error:"HTTP "+r.status}}).then(function(j){
      if(!r.ok) throw j;
      return j;
    });
  });
}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function md(s){
  if(!s) return "";
  var str = String(s);
  var codeBlocks = [];
  str = str.replace(/```([a-zA-Z0-9_#+-]*)\r?\n?([\s\S]*?)```/g, function(_, lang, code){
    var idx = codeBlocks.length;
    var l = (lang || "code").trim().toUpperCase();
    var cleanCode = code.replace(/^\r?\n+|\r?\n+$/g, '');
    var blockHtml = '<div class="code-block"><div class="code-block-head"><span class="code-lang">' +
      esc(l) + '</span><button class="code-copy" title="Copy code" aria-label="Copy code"><span class="material-symbols-outlined">content_copy</span></button></div><pre class="code-pre">' +
      esc(cleanCode) + '</pre></div>';
    codeBlocks.push(blockHtml);
    return "___CV_CODE_BLOCK_" + idx + "___";
  });
  str = esc(str);
  str = str.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
  str = str.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
           .replace(/\*(?!\s)([^*]+?)\*/g, "<em>$1</em>")
           .replace(/\r?\n/g, "<br>");
  for(var i = 0; i < codeBlocks.length; i++){
    str = str.replace("___CV_CODE_BLOCK_" + i + "___", codeBlocks[i]);
  }
  return str;
}
function w2s(wx,wy){return{x:wx*S.view.scale+S.view.x,y:wy*S.view.scale+S.view.y}}
function s2w(sx,sy){return{x:(sx-S.view.x)/S.view.scale,y:(sy-S.view.y)/S.view.scale}}
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function hostOf(u){try{return new URL(u).hostname.replace(/^www\./,"")}catch(e){return ""}}
function showToast(msg,err){
  if(!E.toast) return;
  E.toast.textContent=msg;E.toast.hidden=false;E.toast.classList.remove("out");
  if(err) E.toast.style.background="#b3261e";else E.toast.style.background="";
  clearTimeout(E.toast._t);
  E.toast._t=setTimeout(function(){E.toast.classList.add("out");setTimeout(function(){E.toast.hidden=true;E.toast.classList.remove("out")},280)},2600);
}
function applyView(){
  var rx=Math.round(S.view.x), ry=Math.round(S.view.y);
  E.world.style.transform="translate3d("+rx+"px,"+ry+"px,0) scale("+S.view.scale+")";
  E.world.style.backfaceVisibility="hidden";
  E.viewport.style.backgroundSize=(24*S.view.scale)+"px "+(24*S.view.scale)+"px";
  E.viewport.style.backgroundPosition=rx+"px "+ry+"px";
  requestAnimationFrame(renderEdges);
  emit("view",S.view);
}
function animateTo(tx,ty,sc){
  var sx=S.view.x,sy=S.view.y,ss=S.view.scale,t0=performance.now(),dur=420;
  function tick(now){
    var p=Math.min(1,(now-t0)/dur),e=1-Math.pow(1-p,3);
    S.view.x=sx+(tx-sx)*e;S.view.y=sy+(ty-sy)*e;S.view.scale=ss+(sc-ss)*e;
    applyView();if(p<1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
function zoomAt(cx,cy,factor){
  var ns=clamp(S.view.scale*factor,0.08,8);
  var wx=(cx-S.view.x)/S.view.scale, wy=(cy-S.view.y)/S.view.scale;
  S.view.scale=ns;S.view.x=cx-wx*ns;S.view.y=cy-wy*ns;
  applyView();
}
function zoomCenter(f){
  var r=E.viewport.getBoundingClientRect();
  zoomAt(r.width/2,r.height/2,f);
}
function fitView(){
  if(S.nodes.size===0){S.view.x=0;S.view.y=0;S.view.scale=1;applyView();return}
  var minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
  S.nodes.forEach(function(n){
    var h=S.heights[n.id]||420;
    minX=Math.min(minX,n.x);minY=Math.min(minY,n.y);
    maxX=Math.max(maxX,n.x+560);maxY=Math.max(maxY,n.y+h);
  });
  var vw=E.viewport.clientWidth,vh=E.viewport.clientHeight;
  var sc=clamp(Math.min(vw/(maxX-minX+160),vh/(maxY-minY+220)),0.12,1.4);
  var cx=(minX+maxX)/2,cy=(minY+maxY)/2;
  animateTo(vw/2-cx*sc,vh/2-cy*sc,sc);
}
function centerOnContent(){fitView()}
function saveBoardsLocal(a){try{localStorage.setItem("canvas_local_boards",JSON.stringify(a))}catch(e){}}
function loadBoardsLocal(){try{return JSON.parse(localStorage.getItem("canvas_local_boards")||"[]")}catch(e){return[]}}
function saveNodesLocal(){if(!S.boardId||String(S.boardId).indexOf("local_")!==0)return;var a=[];S.nodes.forEach(function(v){a.push(v)});try{localStorage.setItem("canvas_nodes_"+S.boardId,JSON.stringify(a))}catch(e){}}
function renderBoards(){
  if(!E.boardsEl) return;
  E.boardsEl.innerHTML="";
  var mk=function(b){
    var item=document.createElement("div");
    item.className="cs-board-item"+(b.id===S.boardId?" active":"");
    item.dataset.boardId=b.id;
    item.title=b.title||"Untitled canvas";
    item.setAttribute("role","button");item.tabIndex=0;
    item.innerHTML='<span class="cs-board-dot"></span><span class="cs-board-title"></span><button type="button" class="cs-board-more" title="Canvas options" aria-label="Canvas options"><span class="material-symbols-outlined">more_vert</span></button>';
    item.querySelector(".cs-board-title").textContent=b.title;
    var open=function(){switchBoard(b.id)};
    item.addEventListener("click",function(e){if(e.target.closest(".cs-board-more"))return;open()});
    item.addEventListener("keydown",function(e){if(e.key==="Enter"&&!e.target.closest(".cs-board-more"))open()});
    item.querySelector(".cs-board-more").addEventListener("click",function(e){e.stopPropagation();openBoardMenu(b,this)});
    E.boardsEl.appendChild(item);
  };
  if(S.isAuth){
    if(S.boards.size===0){E.boardsEl.innerHTML='<div class="cs-empty">No canvases yet.<br>Ask something below to begin.</div>';return}
    S.boards.forEach(mk);
  }else{
    var list=loadBoardsLocal();
    if(!list.length){E.boardsEl.innerHTML='<div class="cs-empty">Local canvas — sign in to save.</div>';return}
    list.forEach(function(b){
      if(!S.boards.has(b.id)) S.boards.set(b.id,b);
      mk(b);
    });
  }
}
function isRemoteBoard(b){return S.isAuth&&String(b.id).indexOf("local_")!==0}
function closeBoardMenu(){
  var m=document.getElementById("csBmenu");if(m) m.remove();
}
function openBoardMenu(b,anchor){
  closeBoardMenu();
  var items=[{act:"rename",ic:"edit",t:"Rename"}];
  if(isRemoteBoard(b)) items.push({act:"share",ic:"link",t:"Copy share link"});
  items.push({act:"delete",ic:"delete",t:"Delete",danger:true});
  var m=document.createElement("div");m.className="cs-bmenu";m.id="csBmenu";
  m.innerHTML=items.map(function(it,i){return '<button type="button" class="cs-bmenu-item'+(it.danger?" danger":"")+'" data-i="'+i+'"><span class="material-symbols-outlined">'+it.ic+'</span>'+esc(it.t)+'</button>'}).join("");
  document.body.appendChild(m);
  var r=anchor.getBoundingClientRect();
  var mw=m.offsetWidth||160,mh=m.offsetHeight||110;
  var left=Math.max(8,Math.min(r.left,window.innerWidth-mw-10));
  var top=r.bottom+6;
  if(top+mh>window.innerHeight-8) top=Math.max(8,r.top-mh-6);
  m.style.left=left+"px";m.style.top=top+"px";
  m.addEventListener("click",function(e){
    var bi=e.target.closest(".cs-bmenu-item");if(!bi) return;
    var it=items[+bi.dataset.i];
    closeBoardMenu();
    if(it.act==="rename") startInlineRename(b);
    else if(it.act==="share") copyBoardShare(b);
    else deleteBoardFlow(b);
  });
  setTimeout(function(){
    var off=function(ev){if(ev.target.closest&&ev.target.closest("#csBmenu"))return;closeBoardMenu()};
    document.addEventListener("mousedown",off,{once:true});
    document.addEventListener("keydown",function(es){if(es.key==="Escape")closeBoardMenu()},{once:true});
  },0);
}
function startInlineRename(b){
  var el=document.querySelector('.cs-board-item[data-board-id="'+b.id+'"] .cs-board-title');
  if(!el) return;
  var inp=document.createElement("input");
  inp.type="text";inp.className="cs-rename-input";inp.maxLength=80;inp.value=b.title||"";
  el.replaceWith(inp);
  inp.focus();inp.select();
  var done=false;
  var finish=function(save){
    if(done) return;done=true;
    var v=inp.value.trim().slice(0,80);
    if(save&&v&&v!==(b.title||"")) setBoardTitle(b,v);
    else renderBoards();
  };
  inp.addEventListener("keydown",function(e){
    if(e.key==="Enter"){e.preventDefault();finish(true)}
    else if(e.key==="Escape"){e.preventDefault();finish(false)}
  });
  inp.addEventListener("blur",function(){finish(true)});
  inp.addEventListener("click",function(e){e.stopPropagation()});
  inp.addEventListener("keydown",function(e){e.stopPropagation()});
}
function setBoardTitle(b,v){
  b.title=v;
  var fin=function(){renderBoards();showToast("Renamed")};
  if(isRemoteBoard(b)){
    api("/ajax/canvas/boards/"+b.id+"/update/",{method:"POST",body:JSON.stringify({title:b.title})}).then(function(d){
      if(d&&d.board) S.boards.set(b.id,d.board);
      fin();
    }).catch(function(err){showToast((err&&err.error)||"Rename failed",true);renderBoards()});
  }else{
    var a=loadBoardsLocal();
    a.forEach(function(x){if(x.id===b.id)x.title=v});
    saveBoardsLocal(a);fin();
  }
}
function copyBoardShare(b){
  api("/ajax/canvas/boards/"+b.id+"/share/",{method:"POST",body:"{}"}).then(function(d){
    var url=location.origin+d.url;
    return copyText(url).then(function(){showToast("Share link copied — anyone can view")},function(){showToast("Link: "+url)});
  }).catch(function(err){showToast((err&&err.error)||"Share failed",true)});
}
function deleteBoardFlow(b){
  var name=b.title||"Untitled canvas";
  if(!window.confirm('Delete "'+name+'"? This cannot be undone.')) return;
  var wasCurrent=(b.id===S.boardId);
  var after=function(){
    S.boards.delete(b.id);
    try{localStorage.removeItem("canvas_nodes_"+b.id)}catch(e){}
    renderBoards();updateEmpty();renderEdges();
    showToast("Canvas deleted");
    if(wasCurrent){
      var rest=[];S.boards.forEach(function(v,k){rest.push(k)});
      if(rest.length) switchBoard(rest[0]);
      else location.href="/canvas/";
    }
  };
  if(isRemoteBoard(b)){
    api("/ajax/canvas/boards/"+b.id+"/delete/",{method:"POST",body:"{}"}).then(after).catch(function(err){showToast((err&&err.error)||"Delete failed",true)});
  }else{
    saveBoardsLocal(loadBoardsLocal().filter(function(x){return x.id!==b.id}));
    after();
  }
}
function switchBoard(id){
  if(!id) return;
  S.boardId=id;document.body.dataset.boardId=id;
  var u=new URL(location.href);u.searchParams.set("board",id);history.replaceState({},"",u);
  document.querySelectorAll(".cs-board-item").forEach(function(el){el.classList.toggle("active",el.dataset.boardId===id)});
  loadBoard(id);emit("board",id);
}
function createBoard(title){
  title=(title||"Untitled canvas").trim().slice(0,80)||"Untitled canvas";
  if(S.isAuth){
    return api("/ajax/canvas/boards/create/",{method:"POST",body:JSON.stringify({title:title})}).then(function(d){
      S.boards.set(d.board.id,d.board);renderBoards();switchBoard(d.board.id);return d.board;
    }).catch(function(err){
      var b={id:"local_"+Date.now(),title:title,nodeCount:0};
      var a=loadBoardsLocal();a.unshift(b);saveBoardsLocal(a);renderBoards();switchBoard(b.id);
      return b;
    });
  }
  var b={id:"local_"+Date.now(),title:title,nodeCount:0};
  var a=loadBoardsLocal();a.unshift(b);saveBoardsLocal(a);renderBoards();switchBoard(b.id);return Promise.resolve(b);
}
function updateEmpty(){if(E.emptyHint) E.emptyHint.style.display=S.nodes.size?"none":""}
function loadBoards(){
  if(S.readOnly) return;
  if(cfg.boards && Array.isArray(cfg.boards) && cfg.boards.length){
    cfg.boards.forEach(function(b){S.boards.set(b.id,b)});
    renderBoards();
  }
  if(!S.isAuth){
    renderBoards();
    if(!S.boardId){
      var a=loadBoardsLocal();
      if(a.length) switchBoard(a[0].id);
    } else {
      loadBoard(S.boardId);
    }
    return;
  }
  api("/ajax/canvas/boards/",{method:"GET"}).then(function(d){
    (d.boards||[]).forEach(function(b){S.boards.set(b.id,b)});
    renderBoards();
    if(!S.boardId&&d.boards&&d.boards.length) switchBoard(d.boards[0].id);
    else if(S.boardId) loadBoard(S.boardId);
  }).catch(function(){
    if(S.boardId) loadBoard(S.boardId);
  });
}
function _populate(nodes){
  S.nodes.clear();E.world.querySelectorAll(".canvas-card").forEach(function(n){n.remove()});
  (nodes||[]).forEach(function(n){S.nodes.set(n.id,n);renderNode(n)});
  updateEmpty();requestAnimationFrame(renderEdges);
  setTimeout(fitView,80);
}
function loadBoard(id){
  if(!id) return;
  if(!S.isAuth&&String(id).indexOf("local_")===0){
    try{var a=JSON.parse(localStorage.getItem("canvas_nodes_"+id)||"[]")}catch(e){a=[]}
    _populate(a);return;
  }
  if(!S.isAuth) return;
  var reqId=id;
  api("/ajax/canvas/boards/"+id+"/",{method:"GET"}).then(function(d){
    if(S.boardId!==reqId) return;
    var nodes=d.nodes||[];
    if(nodes.length===0&&S.nodes.size>0){
      var hasPending=false;
      S.nodes.forEach(function(n){ if(n.boardId===reqId&&(n.status==="generating"||String(n.id).indexOf("tmp_")===0)) hasPending=true; });
      if(hasPending) return;
    }
    _populate(nodes);
  }).catch(function(e){showToast((e&&e.error)||"Failed to load",true)});
}
function loadShared(){
  if(!S.sharedToken) return;
  api("/ajax/canvas/shared/"+S.sharedToken+"/detail/",{method:"GET"}).then(function(d){_populate(d.nodes)}).catch(function(){showToast("This shared canvas is no longer available",true)});
}

/* ── mock generator (offline demo) ───────────────────────── */
function mockLocal(prompt){
  var p=(prompt||"").toLowerCase();
  if(p.indexOf("raw sensory")!==-1) return {title:"Raw Sensory Data",summary:"**Raw sensory data** is the unprocessed stream — pixels, audio waves, proprioceptive signals — before any abstraction.",sections:[{type:"flow",title:"From photons to plans",nodes:[{label:"Sensors",tone:"slate"},{label:"Encoder",tone:"blue"},{label:"Latent State",tone:"green"},{label:"World Model",tone:"amber"}],links:["captures","compresses","feeds"]},{type:"stats",items:[{k:"Raw video",v:"~1 Gbps"},{k:"Latent state",v:"~4 KB"}]},{type:"comparison",title:"Raw vs Latent",headers:["Aspect","Raw","Latent"],rows:[["Size","MB per frame","Hundreds of floats"],["Planning","Too heavy","Compact rollouts"]]}]};
  if(p.indexOf("world model")!==-1) return {title:"World Models",summary:"A **world model** is an internal predictive simulation — it imagines futures and plans without acting in the real world.",sections:[{type:"quote",text:"Instead of reacting on instinct, a world model mentally 'plays out' scenarios and plans long-term."},{type:"flow",title:"Components of a World Model",nodes:[{label:"Perception",tone:"green",desc:"encodes raw data"},{label:"Dynamics Predictor",tone:"blue",desc:"imagines next state"},{label:"Reward Estimator",tone:"amber"},{label:"Action Policy",tone:"rose",desc:"picks best move"}],links:["encodes","predicts","informs"]},{type:"timeline",title:"Milestones",steps:[{title:"1989",sub:"Sutton's Dyna"},{title:"2018",sub:"World Models paper"},{title:"2023",sub:"DreamerV3 — 150+ tasks"},{title:"2025",sub:"Video world models"}]},{type:"stats",items:[{k:"Rollout speed",v:"1000x realtime"},{k:"Dreamer tasks",v:"150+"}]}]};
  if(p.indexOf("control")!==-1) return {title:"Control Theory",summary:"**Control theory** steers systems to a goal by sensing error and correcting input via feedback.",sections:[{type:"flow",title:"Closed loop",nodes:[{label:"Reference",tone:"slate"},{label:"Controller",tone:"blue"},{label:"Plant",tone:"green"},{label:"Sensor",tone:"amber"}],links:["setpoint","drives","produces"]},{type:"proscons",title:"Open vs closed loop",pros:["Rejects disturbances","Self-correcting"],cons:["Sensor noise risk","Can oscillate"]}]};
  if(p.indexOf("chair")!==-1||p.indexOf("danish")!==-1) return {title:"Iconic Danish Chairs",summary:"Danish modern — honest materials and human proportions distilled to quiet craft.",sections:[{type:"quote",text:"A chair should be beautiful from all sides.",cite:"Hans J. Wegner"},{type:"cards",title:"Four icons",items:[{title:"CH07 Shell Chair",subtitle:"Wegner · 1963",bullets:["Molded plywood","Floating lightness"],desc:"Three shells, winged comfort."},{title:"Wishbone",subtitle:"Wegner · 1949",bullets:["Wood + paper cord"],desc:"Steamed Y-back."}]}]};
  return {title:(prompt||"Exploration").slice(0,36),summary:"An overview of **"+esc(prompt.slice(0,60))+"** — broken into a visual structure you can explore in parallel.",sections:[{type:"text",content:"**"+esc(prompt.slice(0,50))+"** works as interacting parts: perception → prediction → decision."},{type:"flow",title:"Core pipeline",nodes:[{label:"Input",tone:"slate"},{label:"Encode",tone:"blue"},{label:"Predict",tone:"green"},{label:"Decide",tone:"amber"}],links:["arrives as","into state","forward"]},{type:"stats",items:[{k:"Core idea",v:"Model → Imagine → Act"}]}]};
}

/* ── section renderers ───────────────────────────────────── */
var TONES=["blue","green","amber","rose","slate"];
function rFlow(sec){
  var h='<div class="flow-wrap"><div class="flow-title">'+esc(sec.title||"Flow")+'</div><div class="flow-col">';
  var links=sec.links||[];
  var nodes=sec.nodes||sec.steps||[];
  nodes.forEach(function(nd,i){
    var label=typeof nd==="string"?nd:(nd.label||nd.title||nd.name||"");
    var desc=typeof nd==="object"&&nd?(nd.desc||nd.description||""):"";
    var tone=(nd.tone&&TONES.indexOf(nd.tone)>-1)?nd.tone:TONES[i%TONES.length];
    h+='<div class="flow-node t-'+tone+'"'+(desc?' title="'+esc(desc)+'"':'')+'>'+esc(label)+(desc?'<span class="fn-desc">'+esc(desc)+'</span>':'')+'</div>';
    if(i<nodes.length-1){
      h+='<div class="flow-arrow">'+(links[i]?'<span class="fa-label">'+esc(links[i])+'</span>':'')+'<span class="fa-head"></span></div>';
    }
  });
  return h+'</div></div>';
}
function rTimeline(sec){
  var h='<div class="tl-wrap"><div class="tl-title">'+esc(sec.title||"Timeline")+'</div><div class="tl-row">';
  var steps=sec.steps||sec.items||[];
  steps.forEach(function(st,i){
    var title=typeof st==="string"?st:(st.title||st.name||st.label||"");
    var sub=typeof st==="object"&&st?(st.sub||st.subtitle||st.desc||""):"";
    h+='<div class="tl-item"><span class="tl-dot">'+(i+1)+'</span><span class="tl-label">'+esc(title)+'</span>'+(sub?'<span class="tl-sub">'+esc(sub)+'</span>':'')+'</div>';
  });
  return h+'</div></div>';
}
function rStats(sec){
  var h='<div class="stats-grid">';
  (sec.items||[]).forEach(function(it){
    var k=it.k||it.key||it.label||it.name||"";
    var v=it.v||it.val||it.value||it.stat||"";
    h+='<div class="stat-chip"><div class="stat-k">'+esc(k)+'</div><div class="stat-v">'+esc(v)+'</div></div>';
  });
  return h+'</div>';
}
function rQuote(sec){
  var txt=sec.text||sec.quote||sec.content||"";
  var cite=sec.cite||sec.author||sec.source||"";
  return '<div class="quote-block"><div class="quote-text">'+esc(txt)+'</div>'+(cite?'<div class="quote-cite">'+esc(cite)+'</div>':'')+'</div>';
}
function rCode(sec){
  var txt=sec.text||sec.code||sec.content||sec.snippet||"";
  var lang=sec.lang||sec.language||"code";
  return '<div class="code-block"><div class="code-block-head"><span class="code-lang">'+esc(lang.toUpperCase())+'</span><button class="code-copy" title="Copy code" aria-label="Copy code"><span class="material-symbols-outlined">content_copy</span></button></div><pre class="code-pre">'+esc(txt)+'</pre></div>';
}
function rProsCons(sec){
  function li(t){return '<li>'+esc(t)+'</li>'}
  return '<div class="pc-wrap">'+
    '<div class="pc-col pc-pros"><div class="pc-head"><span class="material-symbols-outlined">thumb_up</span> Pros</div><ul>'+(sec.pros||[]).map(li).join("")+'</ul></div>'+
    '<div class="pc-col pc-cons"><div class="pc-head"><span class="material-symbols-outlined">thumb_down</span> Cons</div><ul>'+(sec.cons||[]).map(li).join("")+'</ul></div>'+
    '</div>';
}
function rAskUser(sec,nodeId){
  var opts=(sec.options||[]).slice(0,4);
  var h='<div class="ask-wrap" data-ask-node="'+esc(nodeId)+'"><div class="ask-q"><span class="material-symbols-outlined">help</span> '+esc(sec.question||"Could you clarify?")+'</div>';
  if(opts.length){
    h+='<div class="ask-opts">';
    opts.forEach(function(o){h+='<button class="ask-opt" data-opt="'+esc(o)+'">'+esc(o)+'</button>'});
    h+='</div>';
  }
  h+='<div class="ask-input-row"><input class="ask-input" placeholder="'+esc(sec.placeholder||"Type your context…")+'" /><button class="ask-send" disabled><span class="material-symbols-outlined">arrow_upward</span></button></div>';
  h+='<div class="ask-hint">Pick an option or type above — I’ll tailor the next card precisely and truthfully.</div></div>';
  return h;
}
function renderSection(sec,idx,nodeId){
  if(!sec) return "";
  var t=String(sec.type||"").toLowerCase().trim();
  if((t==="text"||t==="summary"||t==="paragraph"||t==="note")&&(sec.content||sec.text||sec.body)){
    var c=sec.content||sec.text||sec.body||"";
    return '<div class="text-block">'+(sec.title?'<strong class="sec-subtitle">'+esc(sec.title)+'</strong><br>':'')+md(c)+'</div>';
  }
  if((t==="flow"||t==="pipeline"||t==="process"||t==="workflow")&&(sec.nodes||sec.steps)) return rFlow(sec);
  if((t==="timeline"||t==="steps"||t==="history")&&(sec.steps||sec.items)) return rTimeline(sec);
  if((t==="stats"||t==="metrics"||t==="numbers")&&sec.items) return rStats(sec);
  if((t==="quote"||t==="callout"||t==="definition")&&(sec.text||sec.quote||sec.content)) return rQuote(sec);
  if((t==="code"||t==="snippet"||t==="script"||t==="program")&&(sec.text||sec.code||sec.content||sec.snippet)) return rCode(sec);
  if((t==="proscons"||t==="tradeoffs")&&(sec.pros||sec.cons)) return rProsCons(sec);
  if((t==="diagram"||t==="chart"||t==="graph")&&sec.nodes){
    var h='<div class="diagram-wrap"><div class="diagram-title">'+esc(sec.title||"Diagram")+'</div><div class="diagram-grid">';
    sec.nodes.forEach(function(dn){h+='<div class="diagram-node" data-diag="'+idx+'" data-nid="'+esc(dn.id||dn.label||"")+'"><div class="diagram-node-label">'+esc(dn.label||dn.title||"")+'</div><div class="diagram-node-desc">'+esc(dn.desc||dn.description||"")+'</div></div>'});
    return h+'</div><div class="diagram-detail" id="diag_'+nodeId+'_'+idx+'"></div></div>';
  }
  if((t==="comparison"||t==="table")&&(sec.rows||sec.items)){
    var h2='<div class="comp-wrap"><div class="comp-title">'+esc(sec.title||"Comparison")+'</div><div class="comp-table-wrap"><table class="comp-table"><thead><tr>';
    (sec.headers||["Aspect","A","B"]).forEach(function(hh){h2+='<th>'+esc(hh)+'</th>'});
    h2+='</tr></thead><tbody>';
    (sec.rows||sec.items||[]).forEach(function(row){
      h2+='<tr>';
      if(Array.isArray(row)) row.forEach(function(v){h2+='<td>'+esc(v)+'</td>'});
      else if(typeof row==="object"&&row) Object.values(row).forEach(function(v){h2+='<td>'+esc(v)+'</td>'});
      h2+='</tr>';
    });
    return h2+'</tbody></table></div></div>';
  }
  if((t==="cards"||t==="references"||t==="sources")&&sec.items){
    if(t==="references"||t==="sources"||(sec.items[0]&&(sec.items[0].url||sec.items[0].source))){
      var h5='<div class="refs-wrap"><div class="refs-title"><span class="material-symbols-outlined">travel_explore</span> '+esc(sec.title||"Sources")+'</div>';
      sec.items.forEach(function(rf){
        var title=esc(rf.title||rf.url||"Source"),u=String(rf.url||"");
        if(u&&/^https?:\/\//i.test(u)) h5+='<a class="ref-item" href="'+esc(u)+'" target="_blank" rel="noopener noreferrer nofollow"><span class="ref-fav" aria-hidden="true">'+esc((rf.source||hostOf(u)).charAt(0).toUpperCase())+'</span><span class="ref-main"><span class="ref-t">'+title+'</span><span class="ref-s">'+esc(hostOf(u)||rf.source||"")+'</span></span><span class="material-symbols-outlined ref-arrow">north_east</span></a>';
        else h5+='<span class="ref-item static"><span class="ref-fav">'+esc((rf.source||"S").charAt(0).toUpperCase())+'</span><span class="ref-main"><span class="ref-t">'+title+'</span>'+(rf.source?'<span class="ref-s">'+esc(rf.source)+'</span>':'')+'</span></span>';
      });
      return h5+'</div>';
    }
    var h3='<div class="comp-wrap"><div class="comp-title">'+esc(sec.title||"References")+'</div><div class="cards-grid">';
    sec.items.forEach(function(it){h3+='<div class="card-ref"><div class="card-ref-title">'+esc(it.title||"")+'</div><div class="card-ref-sub">'+esc(it.subtitle||"")+'</div>';if(it.bullets){h3+='<ul class="card-ref-bullets">';it.bullets.forEach(function(b){h3+='<li>'+esc(b)+'</li>'});h3+='</ul>'}if(it.desc||it.description)h3+='<div class="card-ref-desc">'+esc(it.desc||it.description)+'</div>';h3+='</div>'});
    return h3+'</div></div>';
  }
  if((t==="bullets"||t==="list"||t==="points"||t==="key_points")&&sec.items){
    var h4='<div><div class="bullets-title">'+esc(sec.title||"")+'</div><ul class="bullets-list">';
    sec.items.forEach(function(v){h4+='<li>'+(typeof v==="string"?md(v):(v.text?md(v.text):esc(JSON.stringify(v))))+'</li>'});
    return h4+'</ul></div>';
  }
  if(t==="ask_user"&&(sec.question||sec.prompt)) return rAskUser(sec,nodeId);
  if(sec.code||sec.snippet) return rCode(sec);
  if(sec.content||sec.text||sec.body||sec.desc||sec.description){
    var txt=sec.content||sec.text||sec.body||sec.desc||sec.description||"";
    return '<div class="text-block">'+(sec.title?'<strong class="sec-subtitle">'+esc(sec.title)+'</strong><br>':'')+md(txt)+'</div>';
  }
  return "";
}

/* ── node rendering ──────────────────────────────────────── */
function selectNode(id,silent){
  S.selectedId=id||"";
  document.querySelectorAll(".canvas-card.selected").forEach(function(el){el.classList.remove("selected")});
  if(id){var el=document.getElementById("node_"+id);if(el) el.classList.add("selected")}
}
function renderNode(n){
  var old=document.getElementById("node_"+n.id);if(old) old.remove();
  var card=document.createElement("div");
  card.className="canvas-card";
  card.id="node_"+n.id;card.dataset.nodeId=n.id;
  card.style.left=n.x+"px";card.style.top=n.y+"px";card.tabIndex=0;
  var c=n.content||{};
  var isEmpty=n.status==="empty";
  if(isEmpty) card.classList.add("is-empty");
  else if(n.status==="generating") card.classList.add("is-generating");
  var title=isEmpty?"New thread":(c.title||n.title||n.prompt.slice(0,48));
  var gen=n.status==="generating";
  var head;
  if(isEmpty){
    head='<div class="card-head"><div class="card-title">New thread</div><div class="card-actions"><button class="card-icon-btn" data-action="delete" title="Delete"><span class="material-symbols-outlined">close</span></button></div></div>';
  }else{
    head='<div class="card-head"><div class="card-title">'+esc(title)+'</div><div class="card-actions"><button class="card-icon-btn" data-action="focus" title="Center (F)"><span class="material-symbols-outlined">center_focus_strong</span></button><button class="card-icon-btn" data-action="copy" title="Copy prompt"><span class="material-symbols-outlined">content_copy</span></button><button class="card-icon-btn" data-action="delete" title="Delete (Del)"><span class="material-symbols-outlined">delete</span></button></div></div>';
  }
  var body="";
  if(isEmpty){
    body='<div class="card-body empty-thread"><div class="empty-thread-hint">What should this thread explore?</div></div><div class="card-followup"><input class="draft-input" placeholder="Ask anything to start this thread…" aria-label="Thread prompt" autofocus><button class="cf-send" aria-label="Send" disabled><span class="material-symbols-outlined">arrow_upward</span></button></div>';
  }else if(gen){
    body='<div class="card-body"><div class="card-status"><span class="card-dots"><i></i><i></i><i></i></span> <em>Creating a visual…</em></div></div>';
  }else{
    body='<div class="card-body">';
    if(c.summary) body+='<div class="text-block">'+md(c.summary)+'</div>';
    (c.sections||[]).forEach(function(sec,idx){
      try{
        body+=renderSection(sec,idx,n.id);
      }catch(err){
        console.error("renderSection error:", err, sec);
      }
    });
    body+='</div><div class="card-followup"><input placeholder="Ask a follow-up…" aria-label="Ask follow-up"><button class="cf-send" aria-label="Send" disabled><span class="material-symbols-outlined">arrow_upward</span></button></div>';
  }
  card.innerHTML=head+body+
    '<button class="anchor top" data-dir="top" aria-label="New thread above"></button>'+
    '<button class="anchor bottom" data-dir="bottom" aria-label="New thread below"></button>'+
    '<button class="anchor left" data-dir="left" aria-label="New thread left"></button>'+
    '<button class="anchor right" data-dir="right" aria-label="New thread right"></button>';
  E.world.appendChild(card);
  S.heights[n.id]=card.offsetHeight;
  card.querySelectorAll(".code-copy").forEach(function(btn){
    btn.addEventListener("click", function(e){
      e.stopPropagation();
      var block=btn.closest(".code-block");
      if(!block) return;
      var preEl=block.querySelector(".code-pre");
      var txt=preEl?preEl.textContent:"";
      copyText(txt.trim()).then(function(){
        btn.classList.add("copied");
        btn.innerHTML='<span class="material-symbols-outlined">check</span>';
        showToast("Code copied");
        setTimeout(function(){ btn.classList.remove("copied"); btn.innerHTML='<span class="material-symbols-outlined">content_copy</span>'; }, 1400);
      }, function(){ showToast("Copy failed",true); });
    });
  });
  if(isEmpty&&!S.readOnly){
    var dInp=card.querySelector(".draft-input"),dBtn=card.querySelector(".cf-send");
    if(dInp&&dBtn){
      var dGo=function(){
        var v=dInp.value.trim();if(!v) return;
        var pid=n.parentId,wx=n.x,wy=n.y;
        var did=n.id;
        var el=document.getElementById("node_"+did);if(el) el.remove();S.nodes.delete(did);delete S.heights[did];
        renderEdges();updateEmpty();
        if(pid) createChild(pid,v,{x:wx,y:wy});
        else createRoot(v,wx,wy);
      };
      dInp.addEventListener("input",function(){dBtn.disabled=!this.value.trim()});
      dInp.addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();dGo()}});
      dBtn.addEventListener("click",dGo);
      var dDel=card.querySelector('[data-action="delete"]');
      if(dDel) dDel.addEventListener("click",function(e){e.stopPropagation();deleteNode(n.id)});
      setTimeout(function(){dInp.focus()},80);
    }
  }
  if(!gen&&!isEmpty&&!S.readOnly){
    var inp=card.querySelector(".card-followup input"),btn=card.querySelector(".cf-send");
    if(inp&&btn){
      inp.addEventListener("input",function(){btn.disabled=!this.value.trim()});
      inp.addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();var v=inp.value.trim();if(!v)return;inp.value="";btn.disabled=true;createChild(n.id,v,{})}});
      btn.addEventListener("click",function(){var v=inp.value.trim();if(!v)return;inp.value="";btn.disabled=true;createChild(n.id,v,{})});
    }
    card.querySelectorAll(".diagram-node").forEach(function(el){
      el.addEventListener("click",function(){
        var idx=el.dataset.diag,detail=document.getElementById("diag_"+n.id+"_"+idx);
        if(!detail) return;
        var was=el.classList.contains("active");
        card.querySelectorAll(".diagram-node").forEach(function(x){x.classList.remove("active")});
        if(!was){el.classList.add("active");detail.textContent=el.querySelector(".diagram-node-desc").textContent+" — tap again to dismiss.";detail.classList.add("show")}
        else detail.classList.remove("show");
      });
    });
    var askWrap=card.querySelector(".ask-wrap");
    if(askWrap){
      var askInput=askWrap.querySelector(".ask-input");
      var askSend=askWrap.querySelector(".ask-send");
      if(askInput&&askSend){
        var askGo=function(){
          var v=askInput.value.trim();if(!v) return;
          askInput.value="";askSend.disabled=true;
          askWrap.querySelectorAll(".ask-opt").forEach(function(b){b.disabled=true});
          createChild(n.id,"Context: "+v+" — please tailor the next card for this context.",{});
          showToast("Context received — generating tailored card");
        };
        askInput.addEventListener("input",function(){askSend.disabled=!this.value.trim()});
        askInput.addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();askGo()}});
        askSend.addEventListener("click",askGo);
      }
      askWrap.querySelectorAll(".ask-opt").forEach(function(btnOpt){
        btnOpt.addEventListener("click",function(){
          var opt=btnOpt.dataset.opt;if(!opt) return;
          askWrap.querySelectorAll(".ask-opt").forEach(function(b){b.disabled=true; b.style.opacity=".5"});
          btnOpt.disabled=false;btnOpt.style.opacity="1";btnOpt.style.background="var(--cv-primary)";btnOpt.style.color="#fff";
          createChild(n.id,"Selected context: '"+opt+"' — please tailor the next card for this context and be truthful. If still ambiguous, ask again.",{});
          showToast("Context selected");
        });
      });
    }
    card.querySelector('[data-action="focus"]').addEventListener("click",function(e){e.stopPropagation();centerCard(n.id)});
    card.querySelector('[data-action="copy"]').addEventListener("click",function(e){
      e.stopPropagation();
      copyText(n.prompt).then(function(){showToast("Prompt copied")},function(){showToast("Copy failed",true)});
    });
    card.querySelector('[data-action="delete"]').addEventListener("click",function(e){e.stopPropagation();deleteNode(n.id)});
  }
  // anchors: pointerdown starts potential wire OR click
  card.querySelectorAll(".anchor").forEach(function(a){
    a.addEventListener("pointerdown",function(e){
      if(S.readOnly) return;
      e.preventDefault();e.stopPropagation();
      startWire(n.id,a.dataset.dir,e);
    });
  });
  card.addEventListener("pointerdown",function(e){
    selectNode(n.id,true);
    if(e.target.closest("button")||e.target.closest("input")||e.target.closest(".anchor")) return;
    if(!e.target.closest(".card-head")) return;
    e.preventDefault();
    try{window.getSelection().removeAllRanges()}catch(err){}
    var rect=card.getBoundingClientRect();
    S.dragging={card:card,id:n.id,sx:e.clientX,sy:e.clientY,ox:n.x,oy:n.y,moved:false};
    card.classList.add("dragging");card.setPointerCapture(e.pointerId);
    E.viewport.classList.add("dragging-card");
    hideTempWire();
    emit("card-drag-start",n.id);
  });
}
function centerCard(id){
  var n=S.nodes.get(id);if(!n) return;
  var h=S.heights[id]||420;
  var vw=E.viewport.clientWidth,vh=E.viewport.clientHeight;
  animateTo(vw/2-(n.x+280)*S.view.scale, vh/2-(n.y+h/2)*S.view.scale, clamp(S.view.scale,0.7,1.05));
}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText) return navigator.clipboard.writeText(t);
  return new Promise(function(res,rej){
    try{var ta=document.createElement("textarea");ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove();res()}catch(e){rej(e)}
  });
}
function deleteNode(id){
  var n=S.nodes.get(id);if(!n) return;
  var isDraft=String(id).indexOf("draft_")===0||String(id).indexOf("local_")===0||String(id).indexOf("tmp_")===0;
  if(S.isAuth&&!isDraft){
    api("/ajax/canvas/nodes/"+id+"/delete/",{method:"POST"}).catch(function(){});
  }
  var el=document.getElementById("node_"+id);if(el) el.remove();
  S.nodes.delete(id);delete S.heights[id];
  S.nodes.forEach(function(v){if(v.parentId===id) v.parentId=n.parentId||""});
  if(S.selectedId===id) S.selectedId="";
  saveNodesLocal();updateEmpty();renderEdges();
  showToast("Card deleted");
}
function duplicateNode(id){
  var n=S.nodes.get(id);if(!n) return;
  if(n.parentId) createChild(n.parentId,n.prompt,{x:n.x+40,y:n.y+40});
  else createRoot(n.prompt,n.x+40,n.y+40);
}

/* ── edges (screen space) ────────────────────────────────── */
function anchorWorld(n,side){
  var el=document.getElementById("node_"+n.id);
  var w=el?el.offsetWidth:560, h=S.heights[n.id]||420;
  if(!el){w=560}
  if(side==="top") return{x:n.x+w/2,y:n.y};
  if(side==="bottom") return{x:n.x+w/2,y:n.y+h};
  if(side==="left") return{x:n.x,y:n.y+h/2};
  return{x:n.x+w,y:n.y+h/2};
}
function renderEdges(){
  if(!E.edgeLayer) return;
  while(E.edgeLayer.firstChild) E.edgeLayer.removeChild(E.edgeLayer.firstChild);
  if(!S.nodes.size) return;
  S.nodes.forEach(function(n){
    if(!n.parentId) return;
    var p=S.nodes.get(n.parentId);
    if(!p) return;
    var pe=document.getElementById("node_"+p.id),ce=document.getElementById("node_"+n.id);
    if(!pe||!ce) return;
    S.heights[p.id]=pe.offsetHeight;S.heights[n.id]=ce.offsetHeight;
    var pw=pe.offsetWidth||560,cw=ce.offsetWidth||560;
    var pcx=p.x+pw/2,pcy=p.y+(S.heights[p.id]/2),ccx=n.x+cw/2,ccy=n.y+(S.heights[n.id]/2);
    var dx=ccx-pcx,dy=ccy-pcy,a,b,vert;
    if(Math.abs(dy)>=Math.abs(dx)*0.7){vert=true;a=dy>0?anchorWorld(p,"bottom"):anchorWorld(p,"top");b=dy>0?anchorWorld(n,"top"):anchorWorld(n,"bottom")}
    else{vert=false;a=dx>0?anchorWorld(p,"right"):anchorWorld(p,"left");b=dx>0?anchorWorld(n,"left"):anchorWorld(n,"right")}
    var sa=w2s(a.x,a.y),sb=w2s(b.x,b.y);
    var off=clamp(Math.hypot(sb.x-sa.x,sb.y-sa.y)*0.38,36,120);
    var c1,c2;
    if(vert){c1={x:sa.x,y:sa.y+(sb.y>sa.y?off:-off)};c2={x:sb.x,y:sb.y+(sb.y>sa.y?-off:off)}}
    else{c1={x:sa.x+(sb.x>sa.x?off:-off),y:sa.y};c2={x:sb.x+(sb.x>sa.x?-off:off),y:sb.y}}
    var path=document.createElementNS("http://www.w3.org/2000/svg","path");
    path.setAttribute("d","M "+sa.x+" "+sa.y+" C "+c1.x+" "+c1.y+", "+c2.x+" "+c2.y+", "+sb.x+" "+sb.y);
    path.setAttribute("class","edge-path");path.setAttribute("marker-end","url(#edgeArrow)");
    E.edgeLayer.appendChild(path);
  });
}
function hideTempWire(){E.tempWire.style.display="none"}

/* ── wires from anchors (drag = drop anywhere, click = quick) */
function startWire(nodeId,dir,e){
  var n=S.nodes.get(nodeId);if(!n) return;
  var a=anchorWorld(n,dir);
  S.wire={nodeId:nodeId,dir:dir,ax:a.x,ay:a.y,sx:e.clientX,sy:e.clientY,moved:false,t0:performance.now()};
  document.body.classList.add("connecting");
  emit("wire-start",S.wire);
}
window.addEventListener("pointermove",function(e){
  if(PTRS.has(e.pointerId)) PTRS.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(PINCH&&PTRS.size>=2){
    var info=pinchInfo();if(!info) return;
    var k=clamp(PINCH.scale*(info.d/PINCH.d),0.08,8);
    var r=E.viewport.getBoundingClientRect();
    var wx=(PINCH.mx-r.left-PINCH.vx)/PINCH.scale,wy=(PINCH.my-r.top-PINCH.vy)/PINCH.scale;
    S.view.scale=k;
    S.view.x=info.mx-r.left-wx*k;
    S.view.y=info.my-r.top-wy*k;
    applyView();renderEdges();
    return;
  }
  if(S.wire){
    if(!S.wire.moved&&Math.hypot(e.clientX-S.wire.sx,e.clientY-S.wire.sy)<5) return;
    S.wire.moved=true;
    var sa=w2s(S.wire.ax,S.wire.ay);
    E.tempWire.setAttribute("d","M "+sa.x+" "+sa.y+" C "+(sa.x+(e.clientX-sa.x)*0.35)+" "+sa.y+", "+(e.clientX-(e.clientX-sa.x)*0.35)+" "+e.clientY+", "+e.clientX+" "+e.clientY);
    E.tempWire.style.display="";
    return;
  }
  if(S.dragging){
    var dx=(e.clientX-S.dragging.sx)/S.view.scale, dy=(e.clientY-S.dragging.sy)/S.view.scale;
    if(!S.dragging.moved&&Math.abs(dx*S.view.scale)+Math.abs(dy*S.view.scale)<4) return;
    S.dragging.moved=true;
    var nx=S.dragging.ox+dx,ny=S.dragging.oy+dy;
    var n=S.nodes.get(S.dragging.id);if(!n) return;
    n.x=nx;n.y=ny;
    S.dragging.card.style.left=nx+"px";S.dragging.card.style.top=ny+"px";
    renderEdges();
    return;
  }
  if(PAN){
    S.view.x=PAN.ox+(e.clientX-PAN.sx);S.view.y=PAN.oy+(e.clientY-PAN.sy);
    applyView();
  }
});
function createEmptyThread(parentId,dir,wx,wy){
  var p=S.nodes.get(parentId);if(!p) return;
  var el=document.getElementById("node_"+parentId);
  var pw=el?el.offsetWidth:560;
  if(wx==null||wy==null){
    var ph2=S.heights[p.id]||420;
    if(dir==="right"){wx=p.x+pw+48;wy=p.y+64}
    else if(dir==="left"){wx=p.x-pw-48;wy=p.y+64}
    else if(dir==="top"){wx=p.x;wy=p.y-ph2-64}
    else{wx=p.x;wy=p.y+ph2+56}
    var sib=0;S.nodes.forEach(function(v){if(v.parentId===parentId)sib++});
    wx+=sib*14;wy+=sib*10;
  }
  var id="draft_"+Date.now()+Math.floor(Math.random()*999);
  var draft={id:id,boardId:S.boardId,parentId:parentId,prompt:"",title:"New thread",content:{title:"New thread",summary:"",sections:[]},status:"empty",x:wx,y:wy};
  S.nodes.set(id,draft);renderNode(draft);updateEmpty();renderEdges();
  var del=document.getElementById("node_"+id),dw=del&&del.offsetWidth?del.offsetWidth:560;
  var vw=E.viewport.clientWidth,vh=E.viewport.clientHeight;
  animateTo(vw/2-(wx+dw/2)*S.view.scale, vh/2-(wy+120)*S.view.scale, S.view.scale);
  setTimeout(function(){
    var card=document.getElementById("node_"+id);
    if(card){var inp=card.querySelector(".draft-input");if(inp) inp.focus()}
  },120);
  return id;
}
function createEmptyRoot(wx,wy){
  if(wx==null||wy==null){
    var c=s2w(E.viewport.clientWidth/2-280,E.viewport.clientHeight/3);
    wx=c.x;wy=c.y;
  }
  var id="draft_"+Date.now()+Math.floor(Math.random()*999);
  var draft={id:id,boardId:S.boardId,parentId:"",prompt:"",title:"New thread",content:{title:"New thread",summary:"",sections:[]},status:"empty",x:wx,y:wy};
  S.nodes.set(id,draft);renderNode(draft);updateEmpty();renderEdges();
  var del=document.getElementById("node_"+id),dw=del&&del.offsetWidth?del.offsetWidth:560;
  var vw=E.viewport.clientWidth,vh=E.viewport.clientHeight;
  animateTo(vw/2-(wx+dw/2)*S.view.scale, vh/2-(wy+120)*S.view.scale, S.view.scale);
  setTimeout(function(){
    var card=document.getElementById("node_"+id);
    if(card){var inp=card.querySelector(".draft-input");if(inp) inp.focus()}
  },120);
  return id;
}
window.addEventListener("pointerup",function(e){
  if(S.wire){
    var w=S.wire;hideTempWire();document.body.classList.remove("connecting");S.wire=null;
    if(!w.moved&&performance.now()-w.t0<450){
      var p=S.nodes.get(w.nodeId);if(!p) return;
      var dir=w.dir,ph2=S.heights[p.id]||420,pel=document.getElementById("node_"+p.id),pw0=pel&&pel.offsetWidth?pel.offsetWidth:560,wx,wy;
      if(dir==="right"){wx=p.x+pw0+48;wy=p.y+64}
      else if(dir==="left"){wx=p.x-pw0-48;wy=p.y+64}
      else if(dir==="top"){wx=p.x;wy=p.y-ph2-64}
      else{wx=p.x;wy=p.y+ph2+56}
      var sib=0;S.nodes.forEach(function(v){if(v.parentId===w.nodeId)sib++});
      wx+=sib*14;wy+=sib*10;
      createEmptyThread(w.nodeId,dir,wx,wy);
    }else{
      var drop=s2w(e.clientX,e.clientY);
      createEmptyThread(w.nodeId,w.dir,drop.x-140,drop.y-16);
    }
    return;
  }
  if(S.dragging){
    var d=S.dragging,n=S.nodes.get(d.id);
    if(n&&d.moved){
      var isDraft=String(n.id).indexOf("draft_")===0||String(n.id).indexOf("local_")===0||String(n.id).indexOf("tmp_")===0;
      if(S.isAuth&&!isDraft){
        api("/ajax/canvas/nodes/"+n.id+"/move/",{method:"POST",body:JSON.stringify({x:n.x,y:n.y})}).catch(function(){});
      }else if(!S.readOnly){
        saveNodesLocal();
      }
      renderEdges();
    }
    d.card.classList.remove("dragging");
    E.viewport.classList.remove("dragging-card");
    S.dragging=null;emit("card-drag-end");
    return;
  }
  if(PAN){
    try{E.viewport.releasePointerCapture(e.pointerId)}catch(err){}
    E.viewport.classList.remove("panning");PAN=null;emit("pan-end");
  }
});
window.addEventListener("pointerup",function(e){
  PTRS.delete(e.pointerId);
  if(PINCH&&PTRS.size<2){
    PINCH=null;
    var rest=PTRS.values().next();
    if(!rest.done){
      PAN={sx:rest.value.x,sy:rest.value.y,ox:S.view.x,oy:S.view.y,pointerId:e.pointerId};
      E.viewport.classList.add("panning");
      return;
    }
  }
});
window.addEventListener("pointercancel",function(e){
  PTRS.delete(e.pointerId);PINCH=null;
  if(PAN){PAN=null;E.viewport.classList.remove("panning");emit("pan-end")}
});
var PAN=null,PTRS=new Map(),PINCH=null;
function pinchInfo(){
  var a=Array.from(PTRS.values());if(a.length<2) return null;
  var dx=a[0].x-a[1].x,dy=a[0].y-a[1].y;
  return{d:Math.hypot(dx,dy)||1,mx:(a[0].x+a[1].x)/2,my:(a[0].y+a[1].y)/2};
}
E.viewport.addEventListener("pointerdown",function(e){
  if(e.target.closest(".canvas-card")) return;
  if(e.button===2) return; // right-click handled separately
  if(e.button!==0&&e.pointerType==="mouse") return;
  PTRS.set(e.pointerId,{x:e.clientX,y:e.clientY});
  if(PTRS.size===2){
    var info=pinchInfo();
    if(info){
      PINCH={d:info.d,scale:S.view.scale,vx:S.view.x,vy:S.view.y,mx:info.mx,my:info.my};
      PAN=null;
      try{E.viewport.releasePointerCapture(e.pointerId)}catch(err){}
      E.viewport.classList.remove("panning");
      selectNode("",true);
      return;
    }
  }
  if(PTRS.size>1) return;
  selectNode("",true);
  try{window.getSelection().removeAllRanges()}catch(err){}
  PAN={sx:e.clientX,sy:e.clientY,ox:S.view.x,oy:S.view.y,pointerId:e.pointerId};
  E.viewport.setPointerCapture(e.pointerId);
  E.viewport.classList.add("panning");
  emit("pan-start");
});

/* ── wheel: allow native scroll only when card body is actually scrollable ── */
E.viewport.addEventListener("wheel",function(e){
  if(e.ctrlKey||e.metaKey){
    e.preventDefault();
    var r=E.viewport.getBoundingClientRect();
    zoomAt(e.clientX-r.left,e.clientY-r.top,e.deltaY>0?0.92:1.08);
    return;
  }
  var scrollable=e.target.closest&&e.target.closest(".card-body, .code-pre, .cs-boards, .cv-panel-body, .comp-table-wrap, .tl-wrap");
  if(scrollable){
    return;
  }
  var inCard=e.target.closest&&e.target.closest(".canvas-card");
  if(inCard){
    var b=inCard.querySelector(".card-body");
    if(b && b.scrollHeight>b.clientHeight){
      b.scrollTop += e.deltaY;
      e.preventDefault();
      return;
    }
  }
  e.preventDefault();
  var r2=E.viewport.getBoundingClientRect();
  zoomAt(e.clientX-r2.left,e.clientY-r2.top,e.deltaY>0?0.92:1.08);
},{passive:false});

/* ── creation ────────────────────────────────────────────── */
function ensureBoardForRoot(prompt,cb){
  if(S.boardId&&String(S.boardId).indexOf("local_")===-1){cb(S.boardId);return}
  if(S.boardId&&String(S.boardId).indexOf("local_")===0&&!S.isAuth){cb(S.boardId);return}
  if(S.isAuth){
    createBoard((prompt||"New thread").slice(0,32)).then(function(b){cb(b&&b.id?b.id:"")},function(){
      var b={id:"local_"+Date.now(),title:(prompt||"Untitled").slice(0,32)};
      var a=loadBoardsLocal();a.unshift(b);saveBoardsLocal(a);renderBoards();
      S.boardId=b.id;document.body.dataset.boardId=b.id;
      cb(b.id);
    });
  }else{
    var b={id:"local_"+Date.now(),title:(prompt||"Untitled").slice(0,32)};
    var a=loadBoardsLocal();a.unshift(b);saveBoardsLocal(a);renderBoards();
    S.boardId=b.id;document.body.dataset.boardId=b.id;
    history.replaceState({},"",new URL(location.href).pathname+"?board="+b.id);
    setTimeout(function(){cb(b.id)},60);
  }
}
function makePlaceholder(prompt,parentId,wx,wy){
  return {id:"tmp_"+Date.now()+Math.floor(Math.random()*999),boardId:S.boardId,parentId:parentId||"",prompt:prompt,title:prompt.slice(0,44),content:{title:prompt.slice(0,44),summary:"",sections:[]},status:"generating",x:wx,y:wy,modelUsed:"fast"};
}
function reveal(ph){
  S.nodes.set(ph.id,ph);renderNode(ph);updateEmpty();renderEdges();
  var rel=document.getElementById("node_"+ph.id);
  var rw=rel&&rel.offsetWidth?rel.offsetWidth:560,h=S.heights[ph.id]||420;
  var vw=E.viewport.clientWidth,vh=E.viewport.clientHeight;
  var target=clamp(S.view.scale,0.65,1);
  animateTo(vw/2-(ph.x+rw/2)*target, vh/2-(ph.y+h/2)*target, target);
}
function swapIn(tmpId,real){
  var old=document.getElementById("node_"+tmpId);if(old) old.remove();S.nodes.delete(tmpId);
  S.nodes.set(real.id,real);renderNode(real);renderEdges();
}
function failIn(ph,msg){
  ph.status="done";
  ph.content={title:"Failed",summary:"",sections:[{type:"quote",text:msg||"Generation failed. Try again."}]};
  var old=document.getElementById("node_"+ph.id);if(old) old.remove();
  S.nodes.set(ph.id,ph);renderNode(ph);showToast(msg||"Generation failed",true);
}
function createChild(parentId,prompt,opts){
  opts=opts||{};prompt=(prompt||"").trim().slice(0,2000);
  var p=S.nodes.get(parentId);if(!p||!prompt) return;
  var wx=opts.x,wy=opts.y;
  if(wx==null||wy==null){
    var dir=opts.dir||"bottom",ph2=S.heights[p.id]||420,cpel=document.getElementById("node_"+parentId),cpw=cpel&&cpel.offsetWidth?cpel.offsetWidth:560;
    if(dir==="right"){wx=p.x+cpw+48;wy=p.y+64}
    else if(dir==="left"){wx=p.x-cpw-48;wy=p.y+64}
    else if(dir==="top"){wx=p.x;wy=p.y-ph2-64}
    else{wx=p.x;wy=p.y+ph2+56}
    var sib=0;S.nodes.forEach(function(v){if(v.parentId===parentId)sib++});
    wx+=sib*14;wy+=sib*10;
  }
  var ph=makePlaceholder(prompt,parentId,wx,wy);
  reveal(ph);
  if(!S.isAuth){
    setTimeout(function(){swapIn(ph.id,{id:"local_"+Date.now(),boardId:S.boardId,parentId:parentId,prompt:prompt,title:"",content:mockLocal(prompt),status:"done",x:wx,y:wy})},600);
    return;
  }
  api("/ajax/canvas/nodes/"+parentId+"/followup/",{method:"POST",body:JSON.stringify({prompt:prompt,x:wx,y:wy})}).then(function(d){
    d.node.x=wx;d.node.y=wy;swapIn(ph.id,d.node);
  }).catch(function(err){failIn(ph,(err&&err.error)||"Follow-up failed")});
}
function createRoot(prompt,wx,wy){
  prompt=(prompt||"").trim().slice(0,2000);if(!prompt) return;
  var count=0;S.nodes.forEach(function(v){if(!v.parentId)count++});
  if(wx==null||wy==null){
    var c=s2w(E.viewport.clientWidth/2-280,E.viewport.clientHeight/3);
    wx=c.x+count*18;wy=c.y+(count%3)*12;
  }
  ensureBoardForRoot(prompt,function(brdId){
    var activeId=brdId||S.boardId;
    if(!activeId){showToast("Please create or select a canvas first",true);return}
    var ph=makePlaceholder(prompt,"",wx,wy);ph.boardId=activeId;reveal(ph);
    if(!S.isAuth||String(activeId).indexOf("local_")===0){
      setTimeout(function(){
        var low=prompt.toLowerCase(),m;
        if(low.indexOf("world")!==-1)m=mockLocal("world model");
        else if(low.indexOf("control")!==-1)m=mockLocal("control");
        else if(low.indexOf("chair")!==-1||low.indexOf("danish")!==-1)m=mockLocal("chair");
        else m=mockLocal(prompt);
        var real={id:"local_"+Date.now(),boardId:activeId,parentId:"",prompt:prompt,title:m.title,content:m,status:"done",x:wx,y:wy};
        swapIn(ph.id,real);saveNodesLocal();
        var lst=loadBoardsLocal(),b=lst.find(function(x){return x.id===activeId});
        if(b){b.title=prompt.slice(0,36);saveBoardsLocal(lst);renderBoards()}
      },620);
      return;
    }
    api("/ajax/canvas/boards/"+encodeURIComponent(activeId)+"/nodes/",{method:"POST",body:JSON.stringify({prompt:prompt,x:wx,y:wy})}).then(function(d){
      d.node.x=wx;d.node.y=wy;swapIn(ph.id,d.node);
      if(S.nodes.size===1){
        api("/ajax/canvas/boards/"+encodeURIComponent(activeId)+"/update/",{method:"POST",body:JSON.stringify({title:prompt.slice(0,36)})}).then(function(){if(S.boards.has(activeId)){S.boards.get(activeId).title=prompt.slice(0,36);renderBoards()}}).catch(function(){});
      }
    }).catch(function(err){failIn(ph,(err&&err.error)||"Generation failed")});
  });
}

/* ── reusable in-canvas prompt dialog (never window.prompt) ── */
function promptModal(opts){
  opts=opts||{};
  return new Promise(function(resolve){
    var ov=document.createElement("div");
    ov.className="modal-overlay";
    ov.innerHTML=
      '<div class="modal-card">' +
      '<h3 class="modal-title">'+esc(opts.title||"Input")+'</h3>' +
      (opts.sub?'<p class="modal-sub">'+esc(opts.sub)+'</p>':'') +
      '<input class="cv-pm-input" placeholder="'+esc(opts.placeholder||"")+'" value="'+esc(opts.seed||"")+'" maxlength="160">' +
      '<div class="modal-actions">' +
      '<button type="button" class="cv-action ghost" data-x>Cancel</button>' +
      '<button type="button" class="cv-action primary" data-ok>'+esc(opts.ok||"OK")+'</button>' +
      '</div></div>';
    document.body.appendChild(ov);
    var input=ov.querySelector(".cv-pm-input");
    function close(val){ ov.remove(); resolve(val); }
    ov.querySelector("[data-ok]").addEventListener("click",function(){close(input.value.trim())});
    ov.querySelector("[data-x]").addEventListener("click",function(){close(null)});
    ov.addEventListener("click",function(e){if(e.target===ov)close(null)});
    input.addEventListener("keydown",function(e){
      if(e.key==="Enter"){e.preventDefault();close(input.value.trim())}
      if(e.key==="Escape"){e.preventDefault();close(null)}
    });
    setTimeout(function(){input.focus()},40);
  });
}

/* ── init ────────────────────────────────────────────────── */
window.CanvasCore={
  state:S,els:E,api:api,on:on,emit:emit,
  w2s:w2s,s2w:s2w,applyView:applyView,renderEdges:renderEdges,renderNode:renderNode,
  createBoard:createBoard,switchBoard:switchBoard,loadBoards:loadBoards,loadBoard:loadBoard,loadShared:loadShared,
  createRoot:createRoot,createEmptyRoot:createEmptyRoot,createChild:createChild,deleteNode:deleteNode,duplicateNode:duplicateNode,
  selectNode:selectNode,zoomAt:zoomAt,zoomCenter:zoomCenter,fitView:fitView,animateTo:animateTo,
  showToast:showToast,copyText:copyText,esc:esc,md:md,mockLocal:mockLocal,updateEmpty:updateEmpty,startWire:startWire,
  promptModal:promptModal
};
document.addEventListener("DOMContentLoaded",function(){
  applyView();
  if(S.readOnly&&S.sharedToken){loadShared()}
  else{loadBoards()}
  updateEmpty();
  window.addEventListener("resize",renderEdges);
  window.addEventListener("orientationchange",function(){setTimeout(renderEdges,120);setTimeout(renderEdges,450)});
  if(window.visualViewport){
    window.visualViewport.addEventListener("resize",renderEdges);
    window.visualViewport.addEventListener("scroll",renderEdges);
  }
});
})();

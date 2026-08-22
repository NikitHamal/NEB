(function(){
var cfg=window.CANVAS_CONFIG||{};
var boardId=cfg.boardId||"";
var isAuth=!!cfg.isAuthenticated;
var csrf=cfg.csrfToken||"";
var world=document.getElementById("canvasWorld");
var viewport=document.getElementById("canvasViewport");
var edgesSvg=document.getElementById("canvasEdges");
var emptyHint=document.getElementById("canvasEmptyHint");
var globalPrompt=document.getElementById("globalPrompt");
var globalSend=document.getElementById("globalSendBtn");
var webSearch=document.getElementById("webSearchToggle");
var webSearchState=document.getElementById("webSearchState");
var speedBtn=document.getElementById("speedBtn");
var speedMenu=document.getElementById("speedMenu");
var boardsEl=document.getElementById("csBoards");
var sidebar=document.getElementById("canvasSidebar");
var selPop=document.getElementById("selectionPop");
var collapseBtn=document.getElementById("csCollapseBtn");
var mobileToggle=document.getElementById("csMobileToggle");
var newBoardBtn=document.getElementById("csNewBoardBtn");
var speedMode="fast";
var nodes=new Map();
var boards=new Map();
var viewportTx=0,viewportTy=0,viewportScale=1;
var draggingCard=null,dragOffX=0,dragOffY=0,dragStartX=0,dragStartY=0;
var panning=false,panStartX=0,panStartY=0,panOrigTx=0,panOrigTy=0;
var selectedText="",selectedNodeId="";
function api(path,opts){
  opts=opts||{};
  opts.headers=opts.headers||{};
  opts.headers["X-CSRFToken"]=csrf;
  opts.headers["Content-Type"]="application/json";
  opts.credentials="same-origin";
  return fetch(path,opts).then(function(r){return r.json().then(function(d){if(!r.ok) throw d;return d;});});
}
function saveLocalBoards(list){try{localStorage.setItem("canvas_local_boards",JSON.stringify(list));}catch(e){}}
function nowBoards(){try{return JSON.parse(localStorage.getItem("canvas_local_boards")||"[]");}catch(e){return [];}}
function setViewportTransform(){
  world.style.transform="translate("+viewportTx+"px,"+viewportTy+"px) scale("+viewportScale+")";
  edgesSvg.style.transform="translate("+viewportTx+"px,"+viewportTy+"px) scale("+viewportScale+")";
  edgesSvg.style.transformOrigin="0 0";
}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function boardSwitch(id){
  if(!id) return;
  boardId=id;
  document.body.dataset.boardId=id;
  var url=new URL(window.location.href);
  url.searchParams.set("board",id);
  history.replaceState({},"",url);
  boardsEl.querySelectorAll(".cs-board-item").forEach(function(el){el.classList.toggle("active",el.dataset.boardId===id);});
  loadBoard(id);
}
function createBoard(title){
  if(isAuth){
    return api("/ajax/canvas/boards/create/",{method:"POST",body:JSON.stringify({title:title||"Untitled canvas"})}).then(function(d){
      var b=d.board;boards.set(b.id,b);renderBoardsList();boardSwitch(b.id);return b;
    });
  } else {
    var b={id:"local_"+Date.now(),title:title||"Untitled canvas",nodeCount:0};
    var list=nowBoards();list.unshift(b);saveLocalBoards(list);renderBoardsList();boardSwitch(b.id);return Promise.resolve(b);
  }
}
function renderBoardsList(){
  if(isAuth){
    boardsEl.innerHTML="";
    if(boards.size===0){boardsEl.innerHTML='<div class="cs-empty">No canvases yet — ask something below to start.</div>';return;}
    boards.forEach(function(b){
      var btn=document.createElement("button");
      btn.className="cs-board-item"+(b.id===boardId?" active":"");
      btn.dataset.boardId=b.id;
      btn.innerHTML='<span class="cs-board-dot"></span><span class="cs-board-title"></span>';
      btn.querySelector(".cs-board-title").textContent=b.title;
      btn.addEventListener("click",function(){boardSwitch(b.id);sidebar.classList.remove("open");});
      boardsEl.appendChild(btn);
    });
  } else {
    var list=nowBoards();
    boardsEl.innerHTML="";
    if(!list.length){boardsEl.innerHTML='<div class="cs-empty">Local canvas — sign in to save permanently.</div>';return;}
    list.forEach(function(b){
      var btn=document.createElement("button");
      btn.className="cs-board-item"+(b.id===boardId?" active":"");
      btn.dataset.boardId=b.id;
      btn.innerHTML='<span class="cs-board-dot"></span><span class="cs-board-title"></span>';
      btn.querySelector(".cs-board-title").textContent=b.title;
      btn.addEventListener("click",function(){boardSwitch(b.id);sidebar.classList.remove("open");});
      boardsEl.appendChild(btn);
    });
  }
}
function loadBoards(){
  if(!isAuth){renderBoardsList();if(!boardId){var lb=nowBoards();if(lb.length) boardSwitch(lb[0].id);} else {loadBoard(boardId);}return;}
  api("/ajax/canvas/boards/",{method:"GET"}).then(function(d){
    (d.boards||[]).forEach(function(b){boards.set(b.id,b);});
    renderBoardsList();
    if(!boardId && d.boards && d.boards.length) boardSwitch(d.boards[0].id);
    else if(boardId) loadBoard(boardId);
  }).catch(function(){});
}
function loadBoard(id){
  if(!id) return;
  if(!isAuth && String(id).startsWith("local_")){
    try{var stored=JSON.parse(localStorage.getItem("canvas_nodes_"+id)||"[]");}catch(e){stored=[]}
    nodes.clear();world.querySelectorAll(".canvas-card").forEach(function(n){n.remove();});
    stored.forEach(function(n){nodes.set(n.id,n);renderNode(n);});
    updateEmpty();requestAnimationFrame(renderEdges);return;
  }
  if(!isAuth) return;
  api("/ajax/canvas/boards/"+id+"/",{method:"GET"}).then(function(d){
    nodes.clear();
    world.querySelectorAll(".canvas-card").forEach(function(n){n.remove();});
    (d.nodes||[]).forEach(function(n){nodes.set(n.id,n);renderNode(n);});
    updateEmpty();requestAnimationFrame(renderEdges);centerOnContent();
  }).catch(function(){});
}
function updateEmpty(){if(emptyHint) emptyHint.style.display=nodes.size?"none":"";}
function escapeHtml(s){return String(s||"").replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function mdBold(s){return escapeHtml(s).replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>").replace(/\n/g,"<br>");}
function centerOnContent(){
  if(nodes.size===0){viewportTx=0;viewportTy=0;viewportScale=1;setViewportTransform();return;}
  var minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
  nodes.forEach(function(n){minX=Math.min(minX,n.x);minY=Math.min(minY,n.y);maxX=Math.max(maxX,n.x+560);maxY=Math.max(maxY,n.y+420);});
  var vw=viewport.clientWidth,vh=viewport.clientHeight;
  var cx=(minX+maxX)/2,cy=(minY+maxY)/2;
  viewportTx=vw/2 - cx*viewportScale;
  viewportTy=vh/2 - cy*viewportScale - 60;
  setViewportTransform();renderEdges();
}
function renderNode(n){
  var existing=document.getElementById("node_"+n.id);
  if(existing) existing.remove();
  var card=document.createElement("div");
  card.className="canvas-card";
  card.id="node_"+n.id;
  card.dataset.nodeId=n.id;
  card.style.left=n.x+"px";
  card.style.top=n.y+"px";
  var content=n.content||{};
  var title=content.title||n.title||n.prompt.slice(0,48);
  var isGenerating=n.status==="generating";
  var head='<div class="card-head card-drag-handle"><div class="card-title">'+escapeHtml(title)+'</div><div class="card-prompt-pill" title="'+escapeHtml(n.prompt)+'"><span>'+escapeHtml(n.prompt.slice(0,50))+'</span></div><div class="card-actions"><button class="card-icon-btn" data-action="duplicate" title="Duplicate"><span class="material-symbols-outlined">content_copy</span></button><button class="card-icon-btn" data-action="expand" title="Expand"><span class="material-symbols-outlined">open_in_full</span></button></div></div>';
  var body="";
  if(isGenerating){
    body='<div class="card-body"><div class="card-status"><span class="card-dots"><i></i><i></i><i></i></span> Creating a visual...</div></div>';
  } else {
    body='<div class="card-body">';
    if(content.summary) body+='<div class="text-block">'+mdBold(content.summary)+'</div>';
    (content.sections||[]).forEach(function(sec,idx){
      if(sec.type==="text" && sec.content) body+='<div class="text-block">'+mdBold(sec.content)+'</div>';
      else if(sec.type==="diagram" && sec.nodes){
        body+='<div class="diagram-wrap"><div class="diagram-title">'+escapeHtml(sec.title||"Diagram")+'</div><div class="diagram-grid">';
        sec.nodes.forEach(function(dn){body+='<div class="diagram-node" data-diag="'+idx+'" data-node="'+escapeHtml(dn.id)+'"><div class="diagram-node-label">'+escapeHtml(dn.label)+'</div><div class="diagram-node-desc">'+escapeHtml(dn.desc||"")+'</div></div>';});
        body+='</div><div class="diagram-detail" id="diag_detail_'+n.id+'_'+idx+'"></div></div>';
      } else if(sec.type==="comparison" && sec.rows){
        body+='<div class="comp-wrap"><div class="comp-title">'+escapeHtml(sec.title||"Comparison")+'</div><table class="comp-table"><thead><tr>';
        (sec.headers||["Aspect","A","B"]).forEach(function(h){body+='<th>'+escapeHtml(h)+'</th>';});
        body+='</tr></thead><tbody>';
        sec.rows.forEach(function(r){body+='<tr>';r.forEach(function(c){body+='<td>'+escapeHtml(c)+'</td>';});body+='</tr>';});
        body+='</tbody></table></div>';
      } else if(sec.type==="cards" && sec.items){
        body+='<div class="comp-wrap"><div class="comp-title">'+escapeHtml(sec.title||"References")+'</div><div class="cards-grid">';
        sec.items.forEach(function(it){body+='<div class="card-ref"><div class="card-ref-title">'+escapeHtml(it.title)+'</div><div class="card-ref-sub">'+escapeHtml(it.subtitle||"")+'</div>';if(it.bullets){body+='<ul class="card-ref-bullets">';it.bullets.forEach(function(b){body+='<li>'+escapeHtml(b)+'</li>';});body+='</ul>';}if(it.desc) body+='<div class="card-ref-desc">'+escapeHtml(it.desc)+'</div>';body+='</div>';});
        body+='</div></div>';
      } else if(sec.type==="bullets" && sec.items){
        body+='<div><div class="bullets-title">'+escapeHtml(sec.title||"")+'</div><ul class="bullets-list">';
        sec.items.forEach(function(it){body+='<li>'+escapeHtml(it)+'</li>';});
        body+='</ul></div>';
      }
    });
    body+='</div>';
    body+='<div class="card-followup"><input placeholder="Ask a follow-up..." aria-label="Ask a follow-up"><button aria-label="Send"><span class="material-symbols-outlined">arrow_upward</span></button></div>';
  }
  var anchors='<div class="card-anchors"><button class="anchor top" data-dir="top"><span class="material-symbols-outlined">add</span></button><button class="anchor bottom" data-dir="bottom"><span class="material-symbols-outlined">add</span></button><button class="anchor left" data-dir="left"><span class="material-symbols-outlined">add</span></button><button class="anchor right" data-dir="right"><span class="material-symbols-outlined">add</span></button></div>';
  card.innerHTML=head+body+anchors;
  world.appendChild(card);
  if(!isGenerating){
    var inp=card.querySelector(".card-followup input");
    var btn=card.querySelector(".card-followup button");
    function sendFollow(){var v=inp.value.trim();if(!v) return;btn.disabled=true;inp.value="";createChildNode(n.id,v);}
    if(btn) btn.addEventListener("click",sendFollow);
    if(inp) inp.addEventListener("keydown",function(e){if(e.key==="Enter") sendFollow();});
    card.querySelectorAll(".diagram-node").forEach(function(dn){
      dn.addEventListener("click",function(){
        var idx=dn.dataset.diag;
        var detail=document.getElementById("diag_detail_"+n.id+"_"+idx);
        if(!detail) return;
        var isActive=dn.classList.contains("active");
        card.querySelectorAll(".diagram-node").forEach(function(x){x.classList.remove("active");});
        if(!isActive){dn.classList.add("active");detail.textContent=dn.querySelector(".diagram-node-desc").textContent+" — "+dn.querySelector(".diagram-node-label").textContent+" is a core component. Tap again to dismiss.";detail.classList.add("show");} else {detail.classList.remove("show");}
      });
    });
    card.querySelectorAll(".anchor").forEach(function(a){
      a.addEventListener("click",function(e){e.stopPropagation();var dir=a.dataset.dir;var prompt="Explore '"+title+"' further toward the "+dir+" direction.";createChildNode(n.id,prompt,dir);});
    });
  }
  card.addEventListener("mousedown",function(e){
    if(e.target.closest(".card-icon-btn")||e.target.closest(".anchor")||e.target.closest("input")||e.target.closest("button")) return;
    if(!e.target.closest(".card-head")) return;
    draggingCard=card;dragStartX=e.clientX;dragStartY=e.clientY;
    var scale=viewportScale;
    var rect=card.getBoundingClientRect();
    dragOffX=(e.clientX-rect.left)/scale;
    dragOffY=(e.clientY-rect.top)/scale;
    card.classList.add("selected");
    e.preventDefault();
  });
}
function renderEdges(){
  edgesSvg.innerHTML="";
  var defs=document.createElementNS("http://www.w3.org/2000/svg","defs");
  defs.innerHTML='<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#b8c1d3"/></marker>';
  edgesSvg.appendChild(defs);
  nodes.forEach(function(n){
    if(!n.parentId) return;
    var parent=nodes.get(n.parentId);
    if(!parent) return;
    var pEl=document.getElementById("node_"+parent.id);
    var cEl=document.getElementById("node_"+n.id);
    if(!pEl||!cEl) return;
    var px=parent.x+280,py=parent.y+pEl.offsetHeight;
    var cx=n.x+280,cy=n.y;
    if(n.x>parent.x+600){px=parent.x+560;py=parent.y+80;cx=n.x;cy=n.y+60;}
    else if(n.x+560<parent.x){px=parent.x;py=parent.y+80;cx=n.x+560;cy=n.y+60;}
    var dx=Math.abs(cx-px),dy=cy-py;
    var c1x=px,c1y=py+Math.min(90,dy*0.45);
    var c2x=cx,c2y=cy-Math.min(90,dy*0.45);
    if(Math.abs(cx-px)>Math.abs(cy-py)){c1x=px+(cx>px?80:-80);c1y=py;c2x=cx+(cx>px?-80:80);c2y=cy;}
    var d="M "+px+" "+py+" C "+c1x+" "+c1y+", "+c2x+" "+c2y+", "+cx+" "+cy;
    var path=document.createElementNS("http://www.w3.org/2000/svg","path");
    path.setAttribute("d",d);path.setAttribute("class","edge-path");path.setAttribute("marker-end","url(#arrow)");
    edgesSvg.appendChild(path);
  });
  edgesSvg.style.width="30000px";edgesSvg.style.height="30000px";
}
function saveLocalNodes(){if(!boardId||!String(boardId).startsWith("local_")) return;var arr=[];nodes.forEach(function(v){arr.push(v);});try{localStorage.setItem("canvas_nodes_"+boardId,JSON.stringify(arr));}catch(e){}}
function mockLocal(prompt){
  var p=prompt.toLowerCase();
  if(p.includes("raw sensory")) return {title:"Raw Sensory Data",summary:"**Raw sensory data** is the unprocessed stream from the environment — pixels, audio waves, or proprioceptive signals before any abstraction.",sections:[{type:"text",content:"Sensors deliver high-dimensional, noisy observations. **Perception** compresses this into a compact latent code that the **world model** can predict forward, filtering noise while preserving task-relevant structure."},{type:"bullets",title:"Why it matters",items:["Basis for every prediction the agent makes.","Quality of encoding limits planning accuracy.","Better compression → more imagined rollouts per second."]}]};
  if(p.includes("world model")) return {title:"World Models",summary:"A **world model** compresses raw sensory data into latent state, then simulates futures to plan without acting.",sections:[{type:"text",content:"It encodes **raw sensory data** into a compact latent state, predicts the next state and **reward**, and enables foresighted planning."}]};
  return {title:prompt.slice(0,34),summary:"An overview of **"+escapeHtml(prompt.slice(0,60))+"** — key ideas in a visual structure.",sections:[{type:"text",content:"**"+escapeHtml(prompt.slice(0,50))+"** can be seen as interacting parts: perception, prediction, and evaluation."},{type:"bullets",title:"Key ideas",items:["Compress the world into a compact state.","Model how actions change that state.","Imagine futures before acting."]}]};
}
function createChildNode(parentId,prompt,dir){
  var parent=nodes.get(parentId);
  if(!parent) return;
  var placeholder={id:"tmp_"+Date.now(),boardId:boardId,parentId:parentId,prompt:prompt,title:prompt.slice(0,40),content:{title:prompt.slice(0,40),summary:"",sections:[]},status:"generating",x:0,y:0,webSearchEnabled:!!(webSearch&&webSearch.checked),modelUsed:speedMode};
  var baseX=parent.x,baseY=parent.y+460;
  if(dir==="right"){baseX=parent.x+580;baseY=parent.y+70;}
  else if(dir==="left"){baseX=parent.x-580;baseY=parent.y+70;}
  else if(dir==="top"){baseX=parent.x;baseY=parent.y-460;}
  var siblings=0;nodes.forEach(function(v){if(v.parentId===parentId) siblings++;});
  placeholder.x=baseX+siblings*18;placeholder.y=baseY+siblings*6;
  nodes.set(placeholder.id,placeholder);renderNode(placeholder);updateEmpty();renderEdges();
  var ttx=viewport.clientWidth/2-(placeholder.x+280)*viewportScale;
  var tty=viewport.clientHeight/2-(placeholder.y+140)*viewportScale;
  viewportTx=ttx;viewportTy=tty;setViewportTransform();renderEdges();
  if(!isAuth){
    setTimeout(function(){
      var mock=mockLocal(prompt);
      var lower=prompt.toLowerCase();
      if(lower.includes("world")) mock={title:"World Models",summary:"A **world model** is an internal predictive simulation that lets an agent imagine futures and plan without acting in the real world.",sections:[{type:"text",content:"World models compress **raw sensory data** into latent state, predict next state and reward, and support model-based planning."},{type:"diagram",title:"Core Architecture",nodes:[{id:"perception",label:"Perception",desc:"Encodes raw data"},{id:"memory",label:"Memory",desc:"Latent state"},{id:"dynamics",label:"Dynamics Predictor",desc:"Predicts next state"},{id:"reward",label:"Reward Estimator",desc:"Predicts reward"},{id:"policy",label:"Action Policy",desc:"Chooses action"}],edges:[{from:"perception",to:"memory"},{from:"memory",to:"dynamics"},{from:"dynamics",to:"reward"},{from:"memory",to:"policy"}]},{type:"comparison",title:"World Models vs LLMs",headers:["Aspect","World Models","LLMs"],rows:[["Objective","Predict future states","Predict next token"],["Planning","Imagined rollouts","Generate text"],["Efficiency","High via imagination","Huge data needed"]]}]};
      var realId="local_"+Date.now();
      var real={id:realId,boardId:boardId,parentId:parentId,prompt:prompt,title:mock.title,content:mock,status:"done",x:placeholder.x,y:placeholder.y,webSearchEnabled:placeholder.webSearchEnabled,modelUsed:speedMode,createdAt:Date.now(),updatedAt:Date.now()};
      nodes.delete(placeholder.id);var old=document.getElementById("node_"+placeholder.id);if(old) old.remove();
      nodes.set(realId,real);renderNode(real);saveLocalNodes();renderEdges();
    },650);
    return;
  }
  var endpoint="/ajax/canvas/nodes/"+parentId+"/followup/";
  api(endpoint,{method:"POST",body:JSON.stringify({prompt:prompt,web_search_enabled:!!(webSearch&&webSearch.checked),speed_mode:speedMode})}).then(function(d){
    var n=d.node;nodes.delete(placeholder.id);var old=document.getElementById("node_"+placeholder.id);if(old) old.remove();
    n.x=placeholder.x;n.y=placeholder.y;
    api("/ajax/canvas/nodes/"+n.id+"/move/",{method:"POST",body:JSON.stringify({x:n.x,y:n.y})}).catch(function(){});
    nodes.set(n.id,n);renderNode(n);updateEmpty();renderEdges();
  }).catch(function(err){placeholder.status="failed";renderNode(placeholder);});
}
function createRootNode(prompt){
  if(!prompt) return;
  if(!boardId){
    if(isAuth){createBoard(prompt.slice(0,28)).then(function(b){doCreateRoot(prompt);});return;}
    else {var nb={id:"local_"+Date.now(),title:prompt.slice(0,28)||"Untitled",nodeCount:0};var list=nowBoards();list.unshift(nb);saveLocalBoards(list);renderBoardsList();boardSwitch(nb.id);setTimeout(function(){doCreateRoot(prompt);},120);return;}
  }
  doCreateRoot(prompt);
}
function doCreateRoot(prompt){
  var placeholder={id:"tmp_"+Date.now(),boardId:boardId,parentId:"",prompt:prompt,title:prompt.slice(0,40),content:{title:prompt.slice(0,40),summary:"",sections:[]},status:"generating",x:0,y:0,webSearchEnabled:!!(webSearch&&webSearch.checked),modelUsed:speedMode};
  var count=0;nodes.forEach(function(v){if(!v.parentId) count++;});
  placeholder.x=420+count*62;placeholder.y=120+(count%3)*18;
  nodes.set(placeholder.id,placeholder);renderNode(placeholder);updateEmpty();renderEdges();
  var ttx=viewport.clientWidth/2-(placeholder.x+280)*viewportScale;
  var tty=viewport.clientHeight/3-(placeholder.y)*viewportScale;
  viewportTx=ttx;viewportTy=tty;setViewportTransform();renderEdges();
  if(!isAuth){
    setTimeout(function(){
      var mock=mockLocal(prompt);var lower=prompt.toLowerCase();
      if(lower.includes("world")) mock={title:"World Models",summary:"A **world model** is an internal predictive simulation that lets an agent imagine futures.",sections:[{type:"text",content:"World models compress **raw sensory data** into latent state, then simulate futures."},{type:"diagram",title:"Core Architecture",nodes:[{id:"perception",label:"Perception",desc:"Encodes raw data"},{id:"memory",label:"Memory",desc:"Latent state"},{id:"dynamics",label:"Dynamics Predictor",desc:"Predicts next state"},{id:"reward",label:"Reward Estimator",desc:"Predicts reward"}],edges:[{from:"perception",to:"memory"},{from:"memory",to:"dynamics"},{from:"dynamics",to:"reward"}]}],};
      else if(lower.includes("control")) mock={title:"Control Theory",summary:"**Control theory** is the mathematics of steering systems toward desired behavior via feedback.",sections:[{type:"text",content:"A controller compares measured output to a reference and adjusts input to minimize error."},{type:"diagram",title:"Feedback Loop",nodes:[{id:"reference",label:"Reference",desc:"Desired value"},{id:"controller",label:"Controller",desc:"Computes correction"},{id:"plant",label:"Plant",desc:"System being controlled"},{id:"sensor",label:"Sensor",desc:"Measures output"}],edges:[{from:"reference",to:"controller"},{from:"controller",to:"plant"},{from:"plant",to:"sensor"}]}]};
      else if(lower.includes("danish")||lower.includes("chair")) mock={title:"Iconic Danish Chairs",summary:"Danish modern chairs distilled function to its purest form — honest materials and human proportions.",sections:[{type:"text",content:"Designers like **Hans Wegner** let wood and leather speak without ornament."},{type:"cards",title:"Four icons",items:[{title:"CH07 Shell Chair",subtitle:"Hans Wegner · 1963",bullets:["Material: Molded plywood + steel","Philosophy: Floating lightness"],desc:"Three curved shells give winged comfort."},{title:"Wishbone Chair",subtitle:"Hans Wegner · 1949",bullets:["Material: Solid wood + paper cord","Philosophy: Perfected craft"],desc:"Steamed Y-back and woven seat."}]}]};
      var realId="local_"+Date.now();
      var real={id:realId,boardId:boardId,parentId:"",prompt:prompt,title:mock.title,content:mock,status:"done",x:placeholder.x,y:placeholder.y,webSearchEnabled:placeholder.webSearchEnabled,modelUsed:speedMode,createdAt:Date.now(),updatedAt:Date.now()};
      nodes.delete(placeholder.id);var old=document.getElementById("node_"+placeholder.id);if(old) old.remove();
      nodes.set(realId,real);renderNode(real);saveLocalNodes();renderEdges();
      if(!isAuth){var lst=nowBoards();var b=lst.find(function(x){return x.id===boardId;});if(b){b.title=prompt.slice(0,28);saveLocalBoards(lst);renderBoardsList();}}
    },650);
    return;
  }
  api("/ajax/canvas/boards/"+boardId+"/nodes/",{method:"POST",body:JSON.stringify({prompt:prompt,web_search_enabled:!!(webSearch&&webSearch.checked),speed_mode:speedMode})}).then(function(d){
    var n=d.node;nodes.delete(placeholder.id);var old=document.getElementById("node_"+placeholder.id);if(old) old.remove();
    n.x=placeholder.x;n.y=placeholder.y;
    api("/ajax/canvas/nodes/"+n.id+"/move/",{method:"POST",body:JSON.stringify({x:n.x,y:n.y})}).catch(function(){});
    nodes.set(n.id,n);renderNode(n);updateEmpty();renderEdges();
    if(nodes.size===1){var t=prompt.slice(0,36);api("/ajax/canvas/boards/"+boardId+"/update/",{method:"POST",body:JSON.stringify({title:t})}).then(function(){if(boards.has(boardId)){boards.get(boardId).title=t;renderBoardsList();}}).catch(function(){});}
  }).catch(function(err){placeholder.status="failed";renderNode(placeholder);});
}
function handleGlobalSend(){
  var v=globalPrompt.value.trim();if(!v) return;
  globalPrompt.value="";autoResize(globalPrompt);globalSend.disabled=true;createRootNode(v);
}
globalPrompt.addEventListener("input",function(){autoResize(this);globalSend.disabled=!this.value.trim();});
globalPrompt.addEventListener("keydown",function(e){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();handleGlobalSend();}});
globalSend.addEventListener("click",handleGlobalSend);
function autoResize(el){el.style.height="auto";el.style.height=Math.min(el.scrollHeight,120)+"px";}
if(webSearch){webSearch.addEventListener("change",function(){webSearchState.textContent=this.checked?"on":"off";});}
if(speedBtn&&speedMenu){
  speedBtn.addEventListener("click",function(e){e.stopPropagation();speedMenu.hidden=!speedMenu.hidden;});
  speedMenu.querySelectorAll("button").forEach(function(b){b.addEventListener("click",function(){speedMode=b.dataset.speed;speedBtn.childNodes[0].textContent=(speedMode==="fast"?"Fast ":"Deep ");speedMenu.querySelectorAll("button").forEach(function(x){x.classList.toggle("active",x.dataset.speed===speedMode);});speedMenu.hidden=true;});});
  document.addEventListener("click",function(){speedMenu.hidden=true;});
}
if(collapseBtn) collapseBtn.addEventListener("click",function(){sidebar.classList.toggle("collapsed");});
if(mobileToggle) mobileToggle.addEventListener("click",function(){sidebar.classList.toggle("open");});
document.addEventListener("click",function(e){if(window.innerWidth<=900 && !sidebar.contains(e.target) && !mobileToggle.contains(e.target)) sidebar.classList.remove("open");});
if(newBoardBtn) newBoardBtn.addEventListener("click",function(){var t=prompt("Canvas title?","Untitled canvas");if(t!==null) createBoard(t||"Untitled canvas");});
viewport.addEventListener("mousedown",function(e){
  if(e.target.closest(".canvas-card")) return;
  if(e.button!==0&&e.button!==1) return;
  panning=true;panStartX=e.clientX;panStartY=e.clientY;panOrigTx=viewportTx;panOrigTy=viewportTy;viewport.classList.add("panning");
});
window.addEventListener("mousemove",function(e){
  if(draggingCard){
    var cardId=draggingCard.dataset.nodeId;var n=nodes.get(cardId);if(!n) return;
    var dx=(e.clientX-dragStartX)/viewportScale,dy=(e.clientY-dragStartY)/viewportScale;
    if(!draggingCard._origX){draggingCard._origX=n.x;draggingCard._origY=n.y;}
    var newX=draggingCard._origX+dx,newY=draggingCard._origY+dy;
    draggingCard.style.left=newX+"px";draggingCard.style.top=newY+"px";n.x=newX;n.y=newY;renderEdges();return;
  }
  if(panning){var dx=e.clientX-panStartX,dy=e.clientY-panStartY;viewportTx=panOrigTx+dx;viewportTy=panOrigTy+dy;setViewportTransform();}
});
window.addEventListener("mouseup",function(e){
  if(draggingCard){
    var cardId=draggingCard.dataset.nodeId;var n=nodes.get(cardId);
    if(n){n.x=parseFloat(draggingCard.style.left)||n.x;n.y=parseFloat(draggingCard.style.top)||n.y;draggingCard._origX=null;draggingCard._origY=null;
    if(isAuth && !String(n.id).startsWith("tmp_") && !String(n.id).startsWith("local_")){api("/ajax/canvas/nodes/"+n.id+"/move/",{method:"POST",body:JSON.stringify({x:n.x,y:n.y})}).catch(function(){});} else if(String(boardId).startsWith("local_")){saveLocalNodes();}renderEdges();}
    draggingCard.classList.remove("selected");draggingCard=null;
  }
  if(panning){panning=false;viewport.classList.remove("panning");}
  setTimeout(handleSelection,30);
});
viewport.addEventListener("wheel",function(e){
  e.preventDefault();
  var delta=e.deltaY>0?-0.08:0.08;
  var newScale=clamp(viewportScale*(1+delta),0.45,1.8);
  var rect=viewport.getBoundingClientRect();
  var mx=e.clientX-rect.left,my=e.clientY-rect.top;
  var wx=(mx-viewportTx)/viewportScale,wy=(my-viewportTy)/viewportScale;
  viewportScale=newScale;viewportTx=mx-wx*viewportScale;viewportTy=my-wy*viewportScale;setViewportTransform();renderEdges();
},{passive:false});
function handleSelection(){
  var sel=window.getSelection();
  if(!sel||sel.isCollapsed||sel.rangeCount===0){selPop.hidden=true;return;}
  var text=sel.toString().trim();
  if(text.length<3||text.length>220){selPop.hidden=true;return;}
  var range=sel.getRangeAt(0);
  var cardEl=range.startContainer&&range.startContainer.parentElement?range.startContainer.parentElement.closest(".canvas-card"):null;
  if(!cardEl){selPop.hidden=true;return;}
  var inside=range.startContainer.parentElement.closest(".text-block, .comp-table td");
  if(!inside){selPop.hidden=true;return;}
  selectedText=text;selectedNodeId=cardEl.dataset.nodeId;
  var rect=range.getBoundingClientRect();
  selPop.style.left=(rect.left+rect.width/2 - selPop.offsetWidth/2)+"px";
  selPop.style.top=(rect.bottom+8)+"px";
  selPop.hidden=false;
}
document.addEventListener("mousedown",function(e){if(!selPop.contains(e.target) && !e.target.closest(".canvas-card")) selPop.hidden=true;});
selPop.querySelector('[data-action="dig-deeper"]').addEventListener("click",function(){
  selPop.hidden=true;
  if(!selectedNodeId||!selectedText) return;
  var parent=nodes.get(selectedNodeId);if(!parent) return;
  window.getSelection().removeAllRanges();
  if(!isAuth){createChildNode(selectedNodeId,"Explain '"+selectedText+"' in depth — definition, why it matters, a tiny example, and how it connects to '"+(parent.title||"")+"'", "right");return;}
  var placeholder={id:"tmp_"+Date.now(),boardId:boardId,parentId:selectedNodeId,prompt:"Explain '"+selectedText+"' in depth",title:"Explain "+selectedText.slice(0,30),content:{title:"Explain "+selectedText.slice(0,30),summary:"",sections:[]},status:"generating",x:parent.x+580,y:parent.y+60,webSearchEnabled:!!(webSearch&&webSearch.checked),modelUsed:speedMode};
  var sib=0;nodes.forEach(function(v){if(v.parentId===selectedNodeId) sib++;});placeholder.y+=sib*18;
  nodes.set(placeholder.id,placeholder);renderNode(placeholder);updateEmpty();renderEdges();
  api("/ajax/canvas/nodes/"+selectedNodeId+"/dig-deeper/",{method:"POST",body:JSON.stringify({selected_text:selectedText,web_search_enabled:!!(webSearch&&webSearch.checked),speed_mode:speedMode})}).then(function(d){
    var n=d.node;nodes.delete(placeholder.id);var old=document.getElementById("node_"+placeholder.id);if(old) old.remove();
    n.x=placeholder.x;n.y=placeholder.y;
    api("/ajax/canvas/nodes/"+n.id+"/move/",{method:"POST",body:JSON.stringify({x:n.x,y:n.y})}).catch(function(){});
    nodes.set(n.id,n);renderNode(n);renderEdges();
  }).catch(function(){placeholder.status="failed";renderNode(placeholder);});
});
selPop.querySelector('[data-action="save-highlight"]').addEventListener("click",function(){
  selPop.hidden=true;if(!selectedText) return;
  try{var arr=JSON.parse(localStorage.getItem("canvas_highlights")||"[]");arr.push({text:selectedText,at:Date.now(),nodeId:selectedNodeId});localStorage.setItem("canvas_highlights",JSON.stringify(arr));}catch(e){}
  var toast=document.createElement("div");toast.textContent="Highlight saved";toast.style.cssText="position:fixed;left:50%;bottom:80px;transform:translateX(-50%);background:#1a1c1e;color:#fff;padding:10px 14px;border-radius:999px;font-size:13px;z-index:9999";document.body.appendChild(toast);setTimeout(function(){toast.remove();},1800);window.getSelection().removeAllRanges();
});
window.addEventListener("resize",function(){renderEdges();});
setViewportTransform();loadBoards();updateEmpty();
window.Canvas={nodes:nodes,boards:boards};
})();

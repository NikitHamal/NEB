(function(){
"use strict";
var C=window.CanvasCore;if(!C)return;
var S=C.state,E=C.els;
var mini=document.getElementById("cvMinimap"),world=document.getElementById("cvMinimapWorld"),view=document.getElementById("cvMinimapView");
var bounds=null,raf=0;
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}
function nodes(){return Array.from(S.nodes.values()).filter(function(n){return String(n.id).indexOf("tmp_")!==0&&String(n.id).indexOf("draft_")!==0})}
function depthMap(list){
  var by={},memo={};list.forEach(function(n){by[n.id]=n});
  function d(n,seen){if(memo[n.id]!=null)return memo[n.id];seen=seen||{};if(seen[n.id])return 0;seen[n.id]=1;var p=by[n.parentId];return memo[n.id]=p?d(p,seen)+1:0}
  list.forEach(function(n){d(n,{})});return memo;
}
function smartTree(){
  var list=nodes();if(!list.length)return;
  var d=depthMap(list),levels={},roots=[];
  list.forEach(function(n){(levels[d[n.id]]=levels[d[n.id]]||[]).push(n);if(!n.parentId||!S.nodes.has(n.parentId))roots.push(n)});
  Object.keys(levels).forEach(function(key){
    var level=levels[key],y=100+Number(key)*520,width=(level.length-1)*620;
    level.forEach(function(n,i){n.x=200+i*620-width/2;n.y=y});
  });
  if(roots.length>1){roots.forEach(function(n,i){n.x=(i-(roots.length-1)/2)*720})}
  applyLayout("tree",list);
}
function radial(){
  var list=nodes();if(!list.length)return;
  var d=depthMap(list),levels={},max=0;
  list.forEach(function(n){var lv=d[n.id];max=Math.max(max,lv);(levels[lv]=levels[lv]||[]).push(n)});
  var cx=360,cy=220;
  (levels[0]||[]).forEach(function(n,i,a){n.x=cx+(i-(a.length-1)/2)*620;n.y=cy});
  for(var level=1;level<=max;level++){
    var ring=levels[level]||[],radius=level*720;
    ring.forEach(function(n,i){var angle=(i/Math.max(1,ring.length))*Math.PI*2-Math.PI/2;n.x=cx+Math.cos(angle)*radius;n.y=cy+Math.sin(angle)*radius});
  }
  applyLayout("radial",list);
}
function grid(){
  var list=nodes();if(!list.length)return;
  list.sort(function(a,b){return (a.createdAt||0)-(b.createdAt||0)});
  var cols=Math.max(1,Math.ceil(Math.sqrt(list.length)));
  list.forEach(function(n,i){n.x=120+(i%cols)*610;n.y=100+Math.floor(i/cols)*470});
  applyLayout("grid",list);
}
function applyLayout(name,list){
  list.forEach(function(n){var el=document.getElementById("node_"+n.id);if(el){el.style.left=n.x+"px";el.style.top=n.y+"px"}});
  C.renderEdges();scheduleMini();setTimeout(C.fitView,60);
  if(S.isAuth&&S.boardId&&String(S.boardId).indexOf("local_")!==0){
    C.api("/ajax/canvas/boards/"+encodeURIComponent(S.boardId)+"/batch-move/",{method:"POST",body:JSON.stringify({layout:name,nodes:list.map(function(n){return{id:n.id,x:n.x,y:n.y}})})}).catch(function(){C.showToast("Layout saved locally, but server sync failed",true)});
  }else{
    try{localStorage.setItem("canvas_nodes_"+S.boardId,JSON.stringify(list))}catch(e){}
  }
  C.showToast(name==="tree"?"Smart tree applied":name==="radial"?"Radial map applied":"Compact grid applied");
}
function branchIds(id){
  var set={};if(!id)return set;set[id]=1;
  var cur=S.nodes.get(id),guard=0;while(cur&&cur.parentId&&guard++<80){set[cur.parentId]=1;cur=S.nodes.get(cur.parentId)}
  var changed=true;while(changed){changed=false;S.nodes.forEach(function(n){if(n.parentId&&set[n.parentId]&&!set[n.id]){set[n.id]=1;changed=true}})}
  return set;
}
function focusBranch(id){
  var cards=document.querySelectorAll(".canvas-card"),on=!!id;
  if(!on||document.body.classList.contains("cv-branch-focused")){
    document.body.classList.remove("cv-branch-focused");cards.forEach(function(el){el.classList.remove("cv-focus-dim")});C.showToast("Focus mode cleared");return false;
  }
  var keep=branchIds(id);document.body.classList.add("cv-branch-focused");cards.forEach(function(el){el.classList.toggle("cv-focus-dim",!keep[el.dataset.nodeId])});C.showToast("Focused selected branch");return true;
}
function calcBounds(list){
  if(!list.length)return null;var minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
  list.forEach(function(n){var el=document.getElementById("node_"+n.id),w=el&&el.offsetWidth?el.offsetWidth:560,h=S.heights[n.id]||300;minX=Math.min(minX,n.x);minY=Math.min(minY,n.y);maxX=Math.max(maxX,n.x+w);maxY=Math.max(maxY,n.y+h)});
  if(!isFinite(minX))return null;return{minX:minX,minY:minY,maxX:maxX,maxY:maxY,w:Math.max(1,maxX-minX),h:Math.max(1,maxY-minY)};
}
function renderMini(){
  raf=0;if(!mini||!world||!view)return;var list=nodes();world.innerHTML="";bounds=calcBounds(list);if(!bounds||!list.length){mini.style.display="none";return}mini.style.display="";
  var pad=8,mw=mini.clientWidth-pad*2,mh=mini.clientHeight-pad*2,scale=Math.min(mw/bounds.w,mh/bounds.h),ox=pad+(mw-bounds.w*scale)/2,oy=pad+(mh-bounds.h*scale)/2;
  list.forEach(function(n){var el=document.createElement("i"),card=document.getElementById("node_"+n.id),w=card&&card.offsetWidth?card.offsetWidth:560,h=S.heights[n.id]||280;el.className="cv-mini-node "+(n.kind||"ai");el.style.left=(ox+(n.x-bounds.minX)*scale)+"px";el.style.top=(oy+(n.y-bounds.minY)*scale)+"px";el.style.width=Math.max(4,w*scale)+"px";el.style.height=Math.max(3,h*scale)+"px";world.appendChild(el)});
  renderMiniView(scale,ox,oy);
  mini._map={scale:scale,ox:ox,oy:oy};
}
function renderMiniView(scale,ox,oy){
  if(!bounds||!view)return;var vw=E.viewport.clientWidth,vh=E.viewport.clientHeight,wx=(-S.view.x)/S.view.scale,wy=(-S.view.y)/S.view.scale,ww=vw/S.view.scale,wh=vh/S.view.scale;
  view.style.left=(ox+(wx-bounds.minX)*scale)+"px";view.style.top=(oy+(wy-bounds.minY)*scale)+"px";view.style.width=Math.max(8,ww*scale)+"px";view.style.height=Math.max(6,wh*scale)+"px";
}
function scheduleMini(){if(raf)return;raf=requestAnimationFrame(renderMini)}
if(mini){
  mini.addEventListener("click",function(e){if(!bounds||!mini._map)return;var r=mini.getBoundingClientRect(),m=mini._map,wx=bounds.minX+(e.clientX-r.left-m.ox)/m.scale,wy=bounds.minY+(e.clientY-r.top-m.oy)/m.scale,vw=E.viewport.clientWidth,vh=E.viewport.clientHeight;C.animateTo(vw/2-wx*S.view.scale,vh/2-wy*S.view.scale,S.view.scale)});
  if(E.world&&window.MutationObserver){new MutationObserver(scheduleMini).observe(E.world,{childList:true,subtree:true,attributes:true,attributeFilter:["style","class"]})}
}
C.on("view",function(){if(mini&&mini._map)renderMiniView(mini._map.scale,mini._map.ox,mini._map.oy)});C.on("board",scheduleMini);window.addEventListener("resize",scheduleMini);setInterval(scheduleMini,2400);
window.CanvasAdvanced=window.CanvasAdvanced||{};
window.CanvasAdvanced.layouts={
  tree:smartTree,
  radial:radial,
  grid:grid,
  apply:function(name){
    if(name==="tree")smartTree();
    else if(name==="radial")radial();
    else if(name==="grid")grid();
  }
};
window.CanvasAdvanced.focusBranch=focusBranch;
window.CanvasAdvanced.refreshMinimap=scheduleMini;
})();

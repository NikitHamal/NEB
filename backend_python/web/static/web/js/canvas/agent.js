(function(){
"use strict";
var C=window.CanvasCore;if(!C)return;
var S=C.state,E=C.els,A=window.CanvasAdvanced=window.CanvasAdvanced||{};
var btn=document.getElementById("cvNebyBtn");

function titleOf(n){var c=n&&n.content||{};return c.title||n.title||n.prompt||"Selected card"}
function ensureBoard(){if(S.boardId)return Promise.resolve(S.boardId);return C.createBoard("Neby exploration").then(function(b){return b.id})}

function openAgent(){
  if(S.readOnly)return;
  var anchor=S.nodes.get(S.selectedId);
  var anchorText=anchor?'Focusing on: '+titleOf(anchor):'Exploring entire knowledge map';
  A.openPanel(
    "Neby Explore",
    "",
    '<div class="cv-neby-head">' +
      '<div>' +
        '<strong>Neby reads your whole canvas</strong>' +
        '<span>Identifies gaps, deepens core mechanisms, and connects related concepts intelligently.</span>' +
      '</div>' +
    '</div>' +
    '<p class="cv-panel-copy">'+C.esc(anchorText)+'</p>' +
    '<div class="cv-field">' +
      '<label for="cvNebyGoal">What should Neby explore?</label>' +
      '<textarea id="cvNebyGoal" rows="4" maxlength="1200" placeholder="e.g. Find conceptual gaps, add derivations, practice problems, or compare real-world applications..."></textarea>' +
    '</div>' +
    '<div class="cv-actions">' +
      '<button class="cv-action primary" id="cvNebyRun"><span class="material-symbols-outlined">travel_explore</span>Explore canvas</button>' +
      '<button class="cv-action ghost" id="cvNebySuggest"><span class="material-symbols-outlined">explore</span>Suggest next moves</button>' +
    '</div>' +
    '<div id="cvNebyOutput"></div>' +
    '<div class="cv-subhead" id="cvHistoryHead" hidden>History</div>' +
    '<div id="cvNebyHistory"></div>'
  );
  var run=document.getElementById("cvNebyRun"),suggest=document.getElementById("cvNebySuggest");
  if(run)run.addEventListener("click",runExplore);
  if(suggest)suggest.addEventListener("click",runSuggestions);
  loadHistory();
  setTimeout(function(){var x=document.getElementById("cvNebyGoal");if(x)x.focus()},40);
}

function timeAgo(ms){
  var s=Math.max(1,Math.floor((Date.now()-Number(ms||0))/1000));
  if(s<60)return s+"s ago";
  if(s<3600)return Math.floor(s/60)+"m ago";
  if(s<86400)return Math.floor(s/3600)+"h ago";
  return Math.floor(s/86400)+"d ago";
}

function loadHistory(){
  var box=document.getElementById("cvNebyHistory"),head=document.getElementById("cvHistoryHead");
  if(!box)return;
  ensureBoard().then(function(boardId){
    return C.api("/ajax/canvas/boards/"+encodeURIComponent(boardId)+"/neby-history/");
  }).then(function(d){
    var runs=(d&&d.runs)||[];
    if(head)head.hidden=!runs.length;
    if(!runs.length){box.innerHTML="";return}
    box.innerHTML=runs.map(function(r,i){
      var label=r.kind==="suggest"?"Suggest":"Explore";
      return '<div class="cv-history-item" data-idx="'+i+'">' +
        '<button type="button" class="cv-history-head" data-toggle="'+i+'">' +
          '<span class="material-symbols-outlined cv-history-chev">chevron_right</span>' +
          '<span class="cv-history-kind '+r.kind+'">'+label+'</span>' +
          '<span class="cv-history-goal">'+C.esc((r.goal||"Untitled").slice(0,90))+'</span>' +
          '<span class="cv-history-time">'+timeAgo(r.created_at)+'</span>' +
        '</button>' +
        '<div class="cv-history-body" hidden>' +
          (r.summary?'<p class="cv-history-summary">'+C.esc(r.summary)+'</p>':'') +
          ((r.questions||[]).length?'<div class="cv-history-qs">'+r.questions.map(function(q){
            return '<button type="button" class="cv-history-q" data-follow="'+C.esc(q)+'"><span>'+C.esc(q)+'</span><span class="material-symbols-outlined">add</span></button>';
          }).join('')+'</div>':'<div class="cv-history-none">No suggestions recorded</div>') +
        '</div>' +
      '</div>';
    }).join("");
    box.querySelectorAll("[data-toggle]").forEach(function(b){
      b.addEventListener("click",function(){
        var item=b.closest(".cv-history-item");
        if(item)item.classList.toggle("open");
        var body=item&&item.querySelector(".cv-history-body");
        if(body)body.hidden=!body.hidden;
      });
    });
    box.querySelectorAll("[data-follow]").forEach(function(b){
      b.addEventListener("click",function(){
        var q=b.dataset.follow;
        if(S.selectedId&&S.nodes.has(S.selectedId))C.createChild(S.selectedId,q,{});
        else C.createRoot(q);
        A.closePanel();
      });
    });
  }).catch(function(){box.innerHTML=""});
}

function loading(label){
  var out=document.getElementById("cvNebyOutput");
  if(out)out.innerHTML='<div class="cv-loader"><i></i><i></i><i></i><span>'+C.esc(label)+'</span></div>';
}

function setButtons(disabled){
  ["cvNebyRun","cvNebySuggest"].forEach(function(id){
    var el=document.getElementById(id);if(el)el.disabled=disabled;
  });
}

function goal(){
  var el=document.getElementById("cvNebyGoal");
  return el?el.value.trim():"";
}

function addNodes(nodes){
  (nodes||[]).forEach(function(n){S.nodes.set(n.id,n);C.renderNode(n)});
  C.updateEmpty();
  C.renderEdges();
  if(A.decorateAll)A.decorateAll();
  setTimeout(C.fitView,80);
}

function renderNext(summary,questions){
  var out=document.getElementById("cvNebyOutput");if(!out)return;
  var html="";
  if(summary)html+='<div class="cv-agent-summary"><strong>What Neby explored</strong><p>'+C.esc(summary)+'</p></div>';
  if(questions&&questions.length){
    html+='<div class="cv-subhead">Continue from here</div>';
    questions.forEach(function(q){
      html+='<div class="cv-suggestion">' +
        '<div class="cv-suggestion-main">' +
          '<div class="cv-suggestion-title">'+C.esc(q)+'</div>' +
          '<div class="cv-suggestion-why">Create as the next connected knowledge card.</div>' +
        '</div>' +
        '<button data-follow="'+C.esc(q)+'" title="Add branch"><span class="material-symbols-outlined">add</span></button>' +
      '</div>';
    });
  }
  out.innerHTML=html||'<div class="cv-empty-state">Exploration complete. All concepts are cleanly linked.</div>';
  out.querySelectorAll("[data-follow]").forEach(function(b){
    b.addEventListener("click",function(){
      var q=b.dataset.follow;
      if(S.selectedId&&S.nodes.has(S.selectedId))C.createChild(S.selectedId,q,{});
      else C.createRoot(q);
      A.closePanel();
    });
  });
}

function runExplore(){
  setButtons(true);
  loading("Neby is analyzing the canvas and generating insightful branches");
  ensureBoard().then(function(boardId){
    return C.api("/ajax/canvas/boards/"+encodeURIComponent(boardId)+"/neby-explore/",{
      method:"POST",
      body:JSON.stringify({goal:goal()||"Find the most useful next branches and deepen this canvas.",anchorId:S.selectedId||""})
    });
  }).then(function(d){
    addNodes(d.nodes||[]);
    renderNext(d.summary,d.nextQuestions||[]);
    setButtons(false);
    loadHistory();
    C.showToast((d.nodes||[]).length+" Neby branches added");
  }).catch(function(err){
    setButtons(false);
    var out=document.getElementById("cvNebyOutput");
    if(out)out.innerHTML='<div class="cv-error-box">'+C.esc((err&&err.error)||"Neby Explore failed")+'</div>';
    C.showToast((err&&err.error)||"Neby Explore failed",true);
  });
}

function renderSuggestions(items){
  var out=document.getElementById("cvNebyOutput");if(!out)return;
  var html='<div class="cv-subhead">High-value next moves</div>';
  (items||[]).forEach(function(item){
    html+='<div class="cv-suggestion">' +
      '<div class="cv-suggestion-main">' +
        '<div class="cv-suggestion-title">'+C.esc(item.title||item.prompt)+'</div>' +
        '<div class="cv-suggestion-why">'+C.esc(item.why||"")+'</div>' +
      '</div>' +
      '<button data-prompt="'+C.esc(item.prompt||"")+'" title="Create branch"><span class="material-symbols-outlined">add</span></button>' +
    '</div>';
  });
  out.innerHTML=html;
  out.querySelectorAll("[data-prompt]").forEach(function(b){
    b.addEventListener("click",function(){
      var q=b.dataset.prompt;if(!q)return;
      if(S.selectedId&&S.nodes.has(S.selectedId))C.createChild(S.selectedId,q,{});
      else C.createRoot(q);
      A.closePanel();
    });
  });
}

function runSuggestions(){
  if(!S.boardId){C.showToast("Add something to the canvas first",true);return}
  setButtons(true);
  loading("Neby is finding conceptual gaps and high-impact questions");
  C.api("/ajax/canvas/boards/"+encodeURIComponent(S.boardId)+"/suggestions/",{
    method:"POST",
    body:JSON.stringify({goal:goal()})
  }).then(function(d){
    renderSuggestions(d.suggestions||[]);
    setButtons(false);
    loadHistory();
  }).catch(function(err){
    setButtons(false);
    var out=document.getElementById("cvNebyOutput");
    if(out)out.innerHTML='<div class="cv-error-box">'+C.esc((err&&err.error)||"Could not generate suggestions")+'</div>';
  });
}

if(btn)btn.addEventListener("click",openAgent);
if(A.registerAction)A.registerAction("neby",openAgent);
else{A.actions=A.actions||{};A.actions.neby=openAgent}
A.openNeby=openAgent;
})();

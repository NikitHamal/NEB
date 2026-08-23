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
      '<div class="cv-neby-orb"><span class="material-symbols-outlined">auto_awesome</span></div>' +
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
      '<button class="cv-action primary" id="cvNebyRun"><span class="material-symbols-outlined">spark</span>Explore canvas</button>' +
      '<button class="cv-action ghost" id="cvNebySuggest"><span class="material-symbols-outlined">explore</span>Suggest next moves</button>' +
    '</div>' +
    '<div id="cvNebyOutput"></div>'
  );
  var run=document.getElementById("cvNebyRun"),suggest=document.getElementById("cvNebySuggest");
  if(run)run.addEventListener("click",runExplore);
  if(suggest)suggest.addEventListener("click",runSuggestions);
  setTimeout(function(){var x=document.getElementById("cvNebyGoal");if(x)x.focus()},40);
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

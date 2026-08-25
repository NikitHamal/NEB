(function(){
"use strict";
var C = window.CanvasCore;
if (!C) return;
var S = C.state;
var A = window.CanvasAdvanced = window.CanvasAdvanced || {};

function ensureBoard(){
  if (S.boardId) return Promise.resolve(S.boardId);
  return C.createBoard("Neby exploration").then(function(b){ return b.id; });
}

function openAgent(){
  if (S.readOnly) return;
  var anchor = S.nodes.get(S.selectedId);
  var focus = anchor ? "Focusing on: " + ((anchor.content && anchor.content.title) || anchor.title || anchor.prompt) : "Exploring the whole canvas";
  A.openPanel(
    "Neby",
    "Agent",
    '<div class="cv-neby-head"><div><strong>Autonomous canvas agent</strong><span>Neby reads the board, picks tools, and keeps going until the goal is met.</span></div></div>' +
    '<p class="cv-panel-copy">'+C.esc(focus)+'</p>' +
    '<div class="cv-field"><label for="cvNebyGoal">Goal</label>' +
    '<textarea id="cvNebyGoal" rows="4" maxlength="1600" placeholder="e.g. Turn this into a revision map with practice questions and a misconception branch."></textarea></div>' +
    '<div class="cv-actions">' +
      '<button class="cv-action primary" id="cvNebyRun"><span class="material-symbols-outlined">auto_awesome</span>Run agent</button>' +
      '<button class="cv-action ghost" id="cvNebySuggest"><span class="material-symbols-outlined">explore</span>Suggest next</button>' +
    '</div>' +
    '<div id="cvNebyOutput"></div>'
  );
  var run = document.getElementById("cvNebyRun");
  var sug = document.getElementById("cvNebySuggest");
  if (run) run.addEventListener("click", runAgent);
  if (sug) sug.addEventListener("click", runSuggestions);
  setTimeout(function(){ var x=document.getElementById("cvNebyGoal"); if(x)x.focus(); }, 40);
}

function goal(){
  var el = document.getElementById("cvNebyGoal");
  return el ? el.value.trim() : "";
}
function setBusy(on){
  ["cvNebyRun","cvNebySuggest"].forEach(function(id){
    var el = document.getElementById(id); if (el) el.disabled = on;
  });
}
function outEl(){ return document.getElementById("cvNebyOutput"); }

function renderTrace(trace, summary){
  var out = outEl(); if (!out) return;
  var html = "";
  if (summary) html += '<div class="cv-agent-summary"><strong>Done</strong><p>'+C.esc(summary)+'</p></div>';
  (trace || []).forEach(function(step, i){
    html += '<div class="cv-agent-step">' +
      '<div class="cv-agent-turn">Turn '+(i+1)+'</div>' +
      (step.thought ? '<p class="cv-agent-thought">'+C.esc(step.thought)+'</p>' : '') +
      ((step.tools||[]).map(function(t){
        return '<div class="cv-agent-tool"><span class="material-symbols-outlined">build</span>'+C.esc(t.name)+'</div>';
      }).join("")) +
    '</div>';
  });
  out.innerHTML = html || '<div class="cv-empty-state">Agent finished.</div>';
}

function addNodes(nodes){
  (nodes||[]).forEach(function(n){ S.nodes.set(n.id, n); C.renderNode(n); });
  C.updateEmpty(); C.renderEdges();
  if (A.decorateAll) A.decorateAll();
  setTimeout(C.fitView, 80);
}

function runAgent(){
  setBusy(true);
  var out = outEl();
  if (out) out.innerHTML = '<div class="cv-loader"><i></i><i></i><i></i><span>Neby is gathering context and choosing tools</span></div>';
  ensureBoard().then(function(boardId){
    return C.api("/ajax/canvas/boards/"+encodeURIComponent(boardId)+"/agent/run/", {
      method: "POST",
      body: JSON.stringify({
        goal: goal() || "Deepen this canvas with the most useful next branches.",
        anchorId: S.selectedId || ""
      })
    });
  }).then(function(d){
    addNodes(d.nodes || []);
    if (d.objects && window.CanvasDraw){
      (d.objects||[]).forEach(function(o){ window.CanvasDraw.add(o); });
    }
    renderTrace(d.trace, d.summary);
    setBusy(false);
    C.showToast(d.summary ? "Neby finished" : "Agent run complete");
  }).catch(function(err){
    setBusy(false);
    var box = outEl();
    if (box) box.innerHTML = '<div class="cv-error-box">'+C.esc((err&&err.error)||"Agent failed")+'</div>';
    C.showToast((err&&err.error)||"Agent failed", true);
  });
}

function runSuggestions(){
  if (!S.boardId){ C.showToast("Add something first", true); return; }
  setBusy(true);
  var out = outEl();
  if (out) out.innerHTML = '<div class="cv-loader"><i></i><i></i><i></i><span>Finding high-value next moves</span></div>';
  C.api("/ajax/canvas/boards/"+encodeURIComponent(S.boardId)+"/suggestions/", {
    method:"POST", body: JSON.stringify({ goal: goal() })
  }).then(function(d){
    var html = '<div class="cv-subhead">Next moves</div>';
    (d.suggestions||[]).forEach(function(item){
      html += '<div class="cv-suggestion"><div class="cv-suggestion-main"><div class="cv-suggestion-title">'+C.esc(item.title||item.prompt)+'</div><div class="cv-suggestion-why">'+C.esc(item.why||"")+'</div></div>' +
        '<button data-prompt="'+C.esc(item.prompt||"")+'" title="Create"><span class="material-symbols-outlined">add</span></button></div>';
    });
    if (out) out.innerHTML = html;
    if (out) out.querySelectorAll("[data-prompt]").forEach(function(b){
      b.addEventListener("click", function(){
        var q = b.dataset.prompt; if (!q) return;
        if (S.selectedId && S.nodes.has(S.selectedId)) C.createChild(S.selectedId, q, {});
        else C.createRoot(q);
        A.closePanel();
      });
    });
    setBusy(false);
  }).catch(function(err){
    setBusy(false);
    if (out) out.innerHTML = '<div class="cv-error-box">'+C.esc((err&&err.error)||"Could not suggest")+'</div>';
  });
}

var fab = document.getElementById("cvNebyFab");
var btn = document.getElementById("cvNebyBtn");
if (fab) fab.addEventListener("click", openAgent);
if (btn) btn.addEventListener("click", openAgent);
if (A.registerAction) A.registerAction("neby", openAgent);
A.openNeby = openAgent;
})();

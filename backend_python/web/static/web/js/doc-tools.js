(function(){
"use strict";
var C=window.DT_CONFIG||{};
var registry=C.registry||[];
var state={tool:null,files:[]};
function $(id){return document.getElementById(id)}
function getCsrf(){
  var v=document.cookie.match('(^|;) ?csrftoken=([^;]*)(;|$)');
  if(v)return decodeURIComponent(v[2]);
  return C.csrf||"";
}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function mdInline(s){
  return String(s||"").replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\n/g,"<br>");
}
function toolBy(id){return registry.filter(function(t){return t.id===id})[0]}
function toolById(id){return toolBy(id)}

function renderToolList(){
  var el=$("dtToolList");el.innerHTML="";
  registry.forEach(function(t){
    var b=document.createElement("button");
    b.type="button";b.className="dt-tool";b.dataset.id=t.id;
    b.innerHTML='<span class="material-symbols-outlined">'+esc(t.icon||"build")+'</span><span>'+esc(t.label||t.id)+'</span>';
    b.addEventListener("click",function(){selectTool(t.id)});
    el.appendChild(b);
  });
}
function selectTool(id){
  state.tool=id;
  document.querySelectorAll(".dt-tool").forEach(function(b){b.classList.toggle("active",b.dataset.id===id)});
  var t=toolById(id);
  if(!t)return;
  $("dtTitle").textContent=t.label;
  $("dtDesc").textContent=t.desc;
  renderFields(t);
  renderFiles();
  updateRunBtn();
}
function renderFields(t){
  var f=$("dtFields");f.innerHTML="";
  (t.params||[]).forEach(function(p){
    var wrap=document.createElement("div");wrap.className="dt-field";
    var lab=document.createElement("label");lab.textContent=p.label||p.key;wrap.appendChild(lab);
    var input;
    if(p.type==="select"){
      input=document.createElement("select");
      (p.options||[]).forEach(function(o){var op=document.createElement("option");op.value=o;op.textContent=o;input.appendChild(op)});
    }else if(p.type==="textarea"){
      input=document.createElement("textarea");input.rows=2;
      if(p.placeholder)input.placeholder=p.placeholder;
    }else{
      input=document.createElement("input");
      input.type=p.type==="number"?"number":"text";
      if(p.placeholder)input.placeholder=p.placeholder;
    }
    input.dataset.key=p.key;
    wrap.appendChild(input);
    f.appendChild(wrap);
  });
}
function renderFiles(){
  var el=$("dtFileList");el.innerHTML="";
  state.files.forEach(function(f,i){
    var c=document.createElement("span");c.className="dt-file";
    c.innerHTML='<span class="material-symbols-outlined" style="font-size:16px;color:var(--md-primary)">insert_drive_file</span><span>'+esc(f.name)+'</span><button type="button" aria-label="Remove"><span class="material-symbols-outlined" style="font-size:16px">close</span></button>';
    c.querySelector("button").addEventListener("click",function(){state.files.splice(i,1);renderFiles();updateRunBtn()});
    el.appendChild(c);
  });
}
function updateRunBtn(){
  var t=toolById(state.tool);
  var ok=t && state.files.length>=(t.inputs.min||0);
  $("dtRunBtn").disabled=!ok;
}
function renderResult(r){
  var el=$("dtResult");el.innerHTML="";
  var wrap=document.createElement("div");
  var text=document.createElement("div");text.innerHTML=mdInline(r.text||"");wrap.appendChild(text);
  if(r.files&&r.files.length){
    var row=document.createElement("div");row.className="dt-files-out";
    r.files.forEach(function(f){
      var a=document.createElement("a");a.className="dt-out-file";a.href=f.url;a.target="_blank";a.rel="noopener";
      a.innerHTML='<span class="material-symbols-outlined" style="font-size:18px">download</span><span>'+esc(f.name)+'</span>';
      row.appendChild(a);
    });
    wrap.appendChild(row);
  }
  el.appendChild(wrap);
  el.scrollIntoView({behavior:"smooth",block:"nearest"});
}
function collectParams(){
  var p={};
  document.querySelectorAll("#dtFields [data-key]").forEach(function(inp){
    var v=inp.value.trim();
    if(v)p[inp.dataset.key]=v;
  });
  return p;
}


function doRun(){
  if(!state.tool)return;
  var btn=$("dtRunBtn");btn.disabled=true;
  var fd=new FormData();
  fd.append("tool",state.tool);
  fd.append("params",JSON.stringify(collectParams()));
  state.files.forEach(function(f){fd.append("files",f,f.name)});
  $("dtResult").innerHTML='<div class="dt-result-status">Working… this can take a few seconds for large files.</div>';
  fetch("/tools/run/",{method:"POST",credentials:"same-origin",headers:{"X-CSRFToken":getCsrf()},body:fd})
    .then(function(r){return r.json().then(function(j){if(!r.ok)throw j;return j})})
    .then(function(d){renderResult(d)})
    .catch(function(err){$("dtResult").innerHTML='<div class="dt-err">'+esc((err&&err.error)||"Request failed")+'</div>'})
    .then(function(){btn.disabled=false;updateRunBtn()});
}

document.addEventListener("DOMContentLoaded",function(){
  renderToolList();
  var drop=$("dtDrop"),input=$("dtFileInput");
  drop.addEventListener("click",function(){input.click()});
  input.addEventListener("change",function(){
    [].forEach.call(input.files,function(f){if(state.files.length<12)state.files.push(f)});
    input.value="";renderFiles();updateRunBtn();
  });
  var dragCount=0;
  drop.addEventListener("dragenter",function(e){e.preventDefault();dragCount++;drop.style.borderColor="var(--md-primary)"});
  drop.addEventListener("dragover",function(e){e.preventDefault()});
  drop.addEventListener("dragleave",function(e){e.preventDefault();if(--dragCount<=0)drop.style.borderColor=""});
  drop.addEventListener("drop",function(e){
    e.preventDefault();dragCount=0;drop.style.borderColor="";
    [].forEach.call(e.dataTransfer.files,function(f){if(state.files.length<12)state.files.push(f)});
    renderFiles();updateRunBtn();
  });
  $("dtRunBtn").addEventListener("click",doRun);
  $("dtClearBtn").addEventListener("click",function(){state.files=[];renderFiles();$("dtResult").innerHTML="";updateRunBtn()});
  if(registry[0])selectTool(registry[0].id);
});
})();
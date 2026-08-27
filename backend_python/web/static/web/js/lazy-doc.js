(function(){
"use strict";
var S={html:"",title:"",dirty:false,saveTimer:null,sessionIdFn:null};
function $(id){return document.getElementById(id)}
function getCsrf(){
  var v=document.cookie.match('(^|;) ?csrftoken=([^;]*)(;|$)');
  if(v)return decodeURIComponent(v[2]);
  return (window.LAZY_CONFIG&&window.LAZY_CONFIG.csrfToken)||"";
}
var panel,paper,titleInput,statusEl,backdrop;

function ensureBackdrop(){
  if(backdrop)return;
  backdrop=document.createElement("div");
  backdrop.className="lz-doc-panel-backdrop";
  backdrop.addEventListener("click",close);
  document.body.appendChild(backdrop);
}
function open(){
  if(!panel||!S.html.trim()){toastMini("No document yet");return}
  panel.hidden=false;
  requestAnimationFrame(function(){panel.classList.add("open")});
  ensureBackdrop();backdrop.hidden=false;
}
function close(){
  if(!panel)return;
  flushSave();
  panel.classList.remove("open");
  if(backdrop)backdrop.hidden=true;
  setTimeout(function(){panel.hidden=true},240);
}
function isOpen(){return panel&&!panel.hidden}
function toastMini(msg){
  var t=document.createElement("div");t.className="lz-toast";t.textContent=msg;
  document.body.appendChild(t);
  setTimeout(function(){t.classList.add("out");setTimeout(function(){t.remove()},260)},1800);
}
function setDoc(html,title,openPanel){
  S.html=html||"";S.title=title||"";
  if(paper){
    paper.innerHTML=S.html;
    paper.dataset.loaded=S.html?"1":"0";
  }
  if(titleInput)titleInput.value=S.title;
  S.dirty=false;setStatus("");
  if(openPanel)open();
  syncTopBtn();
}
function getDoc(){
  return paper?{html:paper.innerHTML,title:(titleInput&&titleInput.value.trim())||S.title}:{html:S.html,title:S.title};
}
function setStatus(msg){if(statusEl)statusEl.textContent=msg||""}
function scheduleSave(){
  S.dirty=true;
  clearTimeout(S.saveTimer);
  S.saveTimer=setTimeout(flushSave,800);
}
function flushSave(){
  clearTimeout(S.saveTimer);S.saveTimer=null;
  if(!S.sessionIdFn||!S.dirty)return;
  var sid=S.sessionIdFn();
  if(!sid)return;
  var d=getDoc();
  fetch("/ajax/lazy/sessions/"+sid+"/save/",{
    method:"POST",credentials:"same-origin",
    headers:{"Content-Type":"application/json","X-CSRFToken":getCsrf()},
    body:JSON.stringify({html:d.html,title:d.title})
  }).then(function(r){return r.json().then(function(j){if(!r.ok)throw j;return j})})
    .then(function(j){S.dirty=false;setStatus("Saved"+(j.docTitle?" · "+j.docTitle:""))})
    .catch(function(){setStatus("Save failed — will retry on next edit")});
}
function doExport(fmt){
  var sid=S.sessionIdFn&&S.sessionIdFn();
  if(!sid){toastMini("Send a message first");return}
  flushSave();
  window.open("/ajax/lazy/sessions/"+sid+"/export/?format="+encodeURIComponent(fmt),"_blank");
}
function syncTopBtn(){
  var btn=$("lzDocBtn");
  if(btn&&S.html)btn.hidden=false;
}

document.addEventListener("DOMContentLoaded",function(){
  panel=$("lzDocPanel");paper=$("lzPaper");
  titleInput=$("lzDocTitleInput");statusEl=$("lzDocStatus");
  if(!panel)return;

  paper.addEventListener("input",scheduleSave);
  titleInput.addEventListener("input",scheduleSave);
  $("lzDocClose").addEventListener("click",close);
  $("lzDocBtn").addEventListener("click",function(){
    if(isOpen())close();else open();
  });
  panel.querySelectorAll("[data-export]").forEach(function(btn){
    btn.addEventListener("click",function(){doExport(btn.getAttribute("data-export"))});
  });
});

window.LazyDoc={
  open:open,close:close,isOpen:isOpen,
  setDoc:setDoc,getDoc:getDoc,
  bindSession:function(fn){S.sessionIdFn=fn}
};
})();

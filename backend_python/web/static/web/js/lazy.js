(function(){
"use strict";
var cfg=window.LAZY_CONFIG||{};
var S={
  sessionId:"",streaming:false,abort:null,
  sessions:new Map(),attachments:[],
  liveEl:null,liveBuf:"",renderTimer:null,credits:cfg.credits||{}
};
function $(id){return document.getElementById(id)}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function getCsrf(){
  var v=document.cookie.match('(^|;) ?csrftoken=([^;]*)(;|$)');
  if(v)return decodeURIComponent(v[2]);
  var inp=document.querySelector('input[name=csrfmiddlewaretoken]');
  return inp?inp.value:(cfg.csrfToken||"");
}
function api(path,opts){
  opts=opts||{};opts.headers=opts.headers||{};
  var t=getCsrf();if(t)opts.headers["X-CSRFToken"]=t;
  if(!(opts.body instanceof FormData))opts.headers["Content-Type"]="application/json";
  opts.credentials="same-origin";
  return fetch(path,opts).then(function(r){
    return r.json().catch(function(){return{error:"HTTP "+r.status}}).then(function(j){
      if(!r.ok)throw j;return j;
    });
  });
}
var TOAST=null;
function toast(msg,err){
  if(TOAST)TOAST.remove();
  TOAST=document.createElement("div");TOAST.className="lz-toast"+(err?" err":"");
  TOAST.textContent=msg;document.body.appendChild(TOAST);
  clearTimeout(TOAST._t);TOAST._t=setTimeout(function(){TOAST.classList.add("out");setTimeout(function(){if(TOAST){TOAST.remove();TOAST=null}},260)},2400);
}

/* ── markdown ─────────────────────────────────────────── */
function renderInline(s){
  return s
    .replace(/`([^`]+)`/g,'<code class="inline">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>")
    .replace(/\*([^*\s][^*]*)\*/g,"<em>$1</em>")
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,'<a href="$2" target="_blank" rel="noopener noreferrer nofollow">$1</a>');
}
function md(src){
  src=String(src||"").replace(/\r\n/g,"\n");
  var blocks=[],self=this;
  src=src.replace(/```([a-zA-Z0-9_#+.-]*)\n?([\s\S]*?)```/g,function(_,lang,code){
    var i=blocks.length;
    blocks.push('<div class="code-block"><div class="code-head"><span>'+esc((lang||"code").trim()||"code")+'</span><button class="code-copy" data-code="'+i+'"><span class="material-symbols-outlined" style="font-size:13px">content_copy</span>Copy</button></div><pre>'+esc(code.replace(/\n$/,""))+'</pre></div>');
    return "\n@@LZCODE"+i+"@@\n";
  });
  var lines=esc(src).split("\n"),out=[],inUl=false,inOl=false,listBuf=[];
  function flushList(){
    if(listBuf.length){
      out.push("<"+(inOl?"ol":"ul")+">"+listBuf.map(function(x){return "<li>"+renderInline(x)+"</li>"}).join("")+"</"+(inOl?"ol":"ul")+">");
      listBuf=[];inUl=false;inOl=false;
    }
  }
  var para=[];
  function flushPara(){
    if(para.length){out.push("<p>"+renderInline(para.join("<br>"))+"</p>");para=[]}
  }
  for(var i=0;i<lines.length;i++){
    var ln=lines[i],t=ln.trim();
    var cm=t.match(/^@@LZCODE(\d+)@@$/);
    if(cm){flushPara();flushList();out.push(blocks[+cm[1]]);continue}
    if(!t){flushPara();flushList();continue}
    var h=t.match(/^(#{1,6})\s+(.*)$/);
    if(h){flushPara();flushList();out.push("<h3>"+renderInline(h[2])+"</h3>");continue}
    if(/^(---+|\*\*\*+)$/.test(t)){flushPara();flushList();out.push("<hr>");continue}
    if(/^&gt;\s?/.test(t)){flushPara();flushList();out.push("<blockquote>"+renderInline(t.replace(/^&gt;\s?/,""))+"</blockquote>");continue}
    var ul=t.match(/^[-*]\s+\[( |x|X)\]\s+(.*)$/);
    if(ul){if(inOl)flushList();inUl=true;listBuf.push('<input type="checkbox" disabled'+(ul[1].toLowerCase()==="x"?" checked":"")+'> '+renderInline(ul[2]));continue}
    if(/^[-*]\s+/.test(t)){if(inOl)flushList();inUl=true;listBuf.push(renderInline(t.replace(/^[-*]\s+/,"")));continue}
    var ol=t.match(/^\d+[.)]\s+(.*)$/);
    if(ol){if(inUl)flushList();inOl=true;listBuf.push(ol[1]);continue}
    if(/^\|.+\|$/.test(t)){
      flushPara();
      var rows=[t];var j=i+1;
      while(j<lines.length&&/^\|.+\|$/.test(lines[j].trim())){rows.push(lines[j].trim());j++}
      var cells=rows.filter(function(r){return !/^\|[\s:|-]+\|$/.test(r)}).map(function(r){
        return r.slice(1,-1).split("|").map(function(c){return c.trim()});
      });
      if(cells.length){
        var tbl='<div class="table-wrap"><table>';
        cells.forEach(function(row,ri){
          tbl+="<tr>"+row.map(function(c){return (ri===0?"<th>":"<td>")+renderInline(c)+(ri===0?"</th>":"</td>")}).join("")+"</tr>";
        });
        out.push(tbl+"</table></div>");
      }
      i=j-1;continue;
    }
    para.push(t);
  }
  flushPara();flushList();
  return out.join("");
}

/* ── messages ─────────────────────────────────────────── */
var msgsEl,threadEl,welcomeEl,inputEl,sendBtn,stopBtn,titleEl,subEl,sessionsEl;
function scrollBottom(){threadEl.scrollTop=threadEl.scrollHeight}
function hideWelcome(){if(welcomeEl)welcomeEl.style.display="none"}
function toolIcon(n){return{n_generate:"auto_awesome",generate_doc:"auto_awesome",edit_doc:"auto_fix_high",append_section:"playlist_add",breakdown:"checklist"}["n_"+n]||"auto_awesome"}
function addToolChip(container,name,label,live){
  var chip=document.createElement("span");
  chip.className="tool-chip"+(live?" live":"");
  chip.innerHTML='<span class="material-symbols-outlined">'+toolIcon(name)+'</span><span></span>'+(live?'<span class="tool-spin"></span>':"");
  chip.querySelector("span:nth-child(2)").textContent=label||name;
  container.appendChild(chip);return chip;
}
function newUserBubble(text,attNames){
  hideWelcome();
  var wrap=document.createElement("div");wrap.className="msg user";
  wrap.innerHTML='<div class="msg-avatar"></div><div class="msg-col"><div class="msg-bubble"></div>'+(attNames&&attNames.length?'<div class="msg-meta"></div>':"")+"</div>";
  wrap.querySelector(".msg-bubble").textContent=text;
  if(attNames&&attNames.length)wrap.querySelector(".msg-meta").textContent="📎 "+attNames.join(", ");
  msgsEl.appendChild(wrap);scrollBottom();return wrap;
}
function newAssistantShell(){
  hideWelcome();
  var wrap=document.createElement("div");wrap.className="msg assistant";
  wrap.innerHTML='<div class="msg-avatar">L</div><div class="msg-col"><div class="tool-row"></div><div class="msg-bubble"><span class="md-content"></span><span class="caret"></span></div></div>';
  msgsEl.appendChild(wrap);scrollBottom();return wrap;
}
function setMdContent(el,text){
  el.innerHTML=md(text);
  el.querySelectorAll(".code-copy").forEach(function(btn){
    btn.addEventListener("click",function(e){
      e.stopPropagation();
      var pre=btn.closest(".code-block").querySelector("pre");
      copyText(pre.textContent.trim()).then(function(){
        btn.classList.add("copied");btn.innerHTML="Copied!";
        setTimeout(function(){btn.classList.remove("copied");btn.innerHTML='<span class="material-symbols-outlined" style="font-size:13px">content_copy</span>Copy'},1300);
      });
    });
  });
}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText)return navigator.clipboard.writeText(t);
  return new Promise(function(res,rej){
    try{var ta=document.createElement("textarea");ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove();res()}catch(e){rej(e)}
  });
}
function scheduleLiveRender(){
  if(S.renderTimer)return;
  S.renderTimer=setTimeout(function(){
    S.renderTimer=null;
    if(S.liveEl){
      var holder=S.liveEl.querySelector(".md-content");
      setMdContent(holder,S.liveBuf);
      scrollBottom();
    }
  },70);
}

/* ── sidebar ──────────────────────────────────────────── */
function renderSessions(){
  if(!sessionsEl)return;
  sessionsEl.innerHTML="";
  var list=Array.from(S.sessions.values()).sort(function(a,b){return (b.updatedAt||0)-(a.updatedAt||0)});
  if(!list.length){sessionsEl.innerHTML='<div class="lz-empty-sessions">No chats yet. Start one below.</div>';return}
  list.forEach(function(ses){
    var b=document.createElement("button");
    b.className="lz-session"+(ses.id===S.sessionId?" active":"");
    b.innerHTML='<span class="lz-session-title"></span>'+(ses.hasDoc?'<span class="material-symbols-outlined lz-session-doc" title="Has document">description</span>':"")+'<span class="lz-session-del" title="Delete chat"><span class="material-symbols-outlined">delete</span></span>';
    b.querySelector(".lz-session-title").textContent=ses.title||"New chat";
    b.querySelector(".lz-session-doc")&&(b.querySelector(".lz-session-doc").style.fontSize="15px");
    b.addEventListener("click",function(e){
      if(e.target.closest(".lz-session-del")){deleteSession(ses.id);return}
      loadSession(ses.id);
    });
    sessionsEl.appendChild(b);
  });
}
function upsertSession(ses){S.sessions.set(ses.id,Object.assign(S.sessions.get(ses.id)||{},ses));renderSessions()}
function deleteSession(id){
  var ses=S.sessions.get(id);
  if(!window.confirm('Delete "'+((ses&&ses.title)||"this chat")+'"?'))return;
  api("/ajax/lazy/sessions/"+id+"/delete/",{method:"POST",body:"{}"}).then(function(){
    S.sessions.delete(id);
    if(id===S.sessionId)newChat();
    else renderSessions();
    toast("Chat deleted");
  }).catch(function(err){toast((err&&err.error)||"Delete failed",true)});
}
function closeSidebarMobile(){
  $("lzSidebar").classList.remove("open");
  $("lzScrim").hidden=true;
}
function loadSession(id){
  api("/ajax/lazy/sessions/"+id+"/",{method:"GET"}).then(function(d){
    S.sessionId=id;S.attachments=[];
    renderAttachRow();
    upsertSession(d);
    titleEl.textContent=d.title||"New chat";
    subEl.textContent=(d.messageCount||0)+" messages"+(d.hasDoc?" · has document":"");
    msgsEl.innerHTML="";
    if(window.LazyDoc)LazyDoc.setDoc(d.docHtml||"",d.docTitle||"",false);
    $("lzDocBtn").hidden=!d.hasDoc;
    (d.messages||[]).forEach(function(m){
      if(m.role==="user"){
        newUserBubble(m.content,m.attachments);
      }else{
        var shell=newAssistantShell();
        var row=shell.querySelector(".tool-row");
        (m.tools||[]).forEach(function(t){addToolChip(row,t.name,t.summary,false)});
        var holder=shell.querySelector(".md-content");
        setMdContent(holder,m.content||"");
        shell.querySelector(".caret").remove();
        if(m.docUpdated&&d.docHtml){
          var pill=document.createElement("button");
          pill.className="doc-pill";
          pill.innerHTML='<span class="material-symbols-outlined">description</span><span>Open document</span>';
          pill.addEventListener("click",function(){if(window.LazyDoc)LazyDoc.open()});
          shell.querySelector(".msg-col").appendChild(pill);
        }
      }
    });
    renderSessions();
    closeSidebarMobile();
    welcomeEl.style.display=(d.messages||[]).length?"none":"";
    scrollBottom();
  }).catch(function(err){toast((err&&err.error)||"Could not load chat",true)});
}

/* ── send / stream ────────────────────────────────────── */
function ensureSession(){
  if(S.sessionId)return Promise.resolve(S.sessionId);
  return api("/ajax/lazy/sessions/create/",{method:"POST",body:"{}"}).then(function(d){
    upsertSession(d.session);
    S.sessionId=d.session.id;
    renderSessions();
    return d.session.id;
  });
}
function updateCredits(c){
  if(!c)return;
  S.credits=c;
  var el=$("lzCredits");
  if(el)el.textContent=c.unlimited?"∞ credits":(Math.max(0,c.remaining)+" credits left");
}
function send(){
  if(S.streaming)return;
  var text=inputEl.value.trim();
  if(!text&&!S.attachments.length)return;
  var attNames=S.attachments.map(function(a){return a.name});
  var payload={text:text||"(see attachments)",attachments:S.attachments.slice()};
  inputEl.value="";autosize();sendBtn.disabled=true;
  S.attachments=[];renderAttachRow();
  newUserBubble(payload.text,attNames);
  var shell=newAssistantShell();
  S.liveEl=shell;S.liveBuf="";
  var row=shell.querySelector(".tool-row");
  S.streaming=true;sendBtn.hidden=true;stopBtn.hidden=false;
  S.abort=new AbortController();

  ensureSession().then(function(sid){
    return fetch("/ajax/lazy/sessions/"+sid+"/chat/",{
      method:"POST",credentials:"same-origin",
      headers:{"Content-Type":"application/json","X-CSRFToken":getCsrf()},
      body:JSON.stringify(payload),signal:S.abort.signal
    }).then(function(resp){
      if(!resp.ok)return resp.json().catch(function(){return{}}).then(function(j){throw j});
      var reader=resp.body.getReader(),dec=new TextDecoder(),buf="";
      function pump(){
        return reader.read().then(function(r){
          if(r.done)return finalize();
          buf+=dec.decode(r.value,{stream:true});
          var parts=buf.split("\n\n");buf=parts.pop();
          parts.forEach(handleFrame);
          return pump();
        });
      }
      return pump();
    });
  }).catch(function(err){
    if(err&&err.name==="AbortError"){appendNote(shell,"— stopped")}
    else toast((err&&(err.error||err.message))||"Request failed",true);
    finalize(true);
  });

  var thinkShown=false,statusChip=null;
  function handleFrame(line){
    line=line.trim();if(!line)return;
    if(line.indexOf("data:")!==0)return;
    var data=line.slice(5).trim();
    if(data==="[DONE]")return;
    var f;try{f=JSON.parse(data)}catch(e){return}
    if(f.type==="user"){
      if(f.title){titleEl.textContent=f.title;upsertSession({id:S.sessionId,title:f.title})}
    }else if(f.type==="think"){
      if(f.content&&!thinkShown){thinkShown=true;var tl=document.createElement("div");tl.className="think-line";tl.textContent=f.content;row.parentNode.insertBefore(tl,row)}
    }else if(f.type==="status"){
      if(statusChip)statusChip.remove();
      statusChip=addToolChip(row,f.tool,f.label,true);scrollBottom();
    }else if(f.type==="delta"){
      S.liveBuf+=f.content;scheduleLiveRender();
    }else if(f.type==="doc"){
      if(statusChip){statusChip.remove();statusChip=null}
      if(window.LazyDoc)LazyDoc.setDoc(f.html,f.title||"",true);
      $("lzDocBtn").hidden=false;
      upsertSession({id:S.sessionId,hasDoc:true,docTitle:f.title||""});
    }else if(f.type==="done"){
      if(f.tools&&f.tools.length){
        row.innerHTML="";
        f.tools.forEach(function(t){addToolChip(row,t.name,t.summary,false)});
        if(f.docUpdated){
          var col=shell.querySelector(".msg-col");
          var pill=document.createElement("button");pill.className="doc-pill";
          pill.innerHTML='<span class="material-symbols-outlined">description</span><span>Open document</span>';
          pill.addEventListener("click",function(){if(window.LazyDoc)LazyDoc.open()});
          col.appendChild(pill);
        }
      }
      if(f.credits)updateCredits(f.credits);
    }else if(f.type==="error"){
      toast(f.message||"Generation failed",true);
    }
  }
  function appendNote(sh,note){
    var meta=document.createElement("div");meta.className="msg-meta";meta.textContent=note;
    sh.querySelector(".msg-col").appendChild(meta);
  }
  function finalize(aborted){
    if(!S.streaming&&!aborted)return;
    S.streaming=false;S.abort=null;
    sendBtn.hidden=false;stopBtn.hidden=true;
    if(S.renderTimer){clearTimeout(S.renderTimer);S.renderTimer=null}
    if(statusChip)statusChip.remove();
    if(S.liveEl){
      var caret=S.liveEl.querySelector(".caret");if(caret)caret.remove();
      setMdContent(S.liveEl.querySelector(".md-content"),S.liveBuf||"_(no output)_");
      if(!S.liveBuf)S.liveEl.querySelector(".md-content").style.fontStyle="italic";
      S.liveEl=null;S.liveBuf="";
    }
    refreshSessionsQuiet();
    scrollBottom();
  }
}
function refreshSessionsQuiet(){
  api("/ajax/lazy/sessions/",{method:"GET"}).then(function(d){
    (d.sessions||[]).forEach(upsertSession);
  }).catch(function(){});
}

/* ── composer ─────────────────────────────────────────── */
function autosize(){
  inputEl.style.height="auto";
  inputEl.style.height=Math.min(inputEl.scrollHeight,180)+"px";
  sendBtn.disabled=S.streaming?true:(!inputEl.value.trim()&&!S.attachments.length);
}
function renderAttachRow(){
  var row=$("lzAttachRow");
  row.innerHTML="";row.hidden=!S.attachments.length;
  S.attachments.forEach(function(a,i){
    var chip=document.createElement("span");chip.className="attach-chip";
    chip.innerHTML='<span class="material-symbols-outlined">insert_drive_file</span><span></span><button type="button" aria-label="Remove"><span class="material-symbols-outlined">close</span></button>';
    chip.querySelector("span:nth-child(2)").textContent=a.name;
    chip.querySelector("button").addEventListener("click",function(){S.attachments.splice(i,1);renderAttachRow();autosize()});
    row.appendChild(chip);
  });
}
function uploadFile(file){
  if(!file)return;
  var ok=/\.(docx|pdf|txt)$/i.test(file.name);
  if(!ok){toast("Supported: .docx, .pdf, .txt",true);return}
  if(file.size>8*1024*1024){toast("Max file size is 8 MB",true);return}
  if(S.attachments.length>=3){toast("Up to 3 files per message",true);return}
  toast("Reading "+file.name+"…");
  var fd=new FormData();fd.append("file",file);
  fetch("/ajax/lazy/upload/",{method:"POST",credentials:"same-origin",headers:{"X-CSRFToken":getCsrf()},body:fd})
    .then(function(r){return r.json().then(function(j){if(!r.ok)throw j;return j})})
    .then(function(d){
      S.attachments.push(d);renderAttachRow();autosize();
      toast("Attached "+d.name+" ("+d.chars.toLocaleString()+" chars)");
    })
    .catch(function(err){toast((err&&err.error)||"Upload failed",true)});
}

/* ── new chat ─────────────────────────────────────────── */
function newChat(){
  S.sessionId="";S.liveBuf="";S.attachments=[];
  msgsEl.innerHTML="";
  welcomeEl.style.display="";
  titleEl.textContent="New chat";subEl.textContent="";
  $("lzDocBtn").hidden=true;
  if(window.LazyDoc){LazyDoc.setDoc("","",false);LazyDoc.close()}
  renderAttachRow();renderSessions();autosize();
  setTimeout(function(){inputEl.focus()},60);
}

/* ── init ─────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded",function(){
  msgsEl=$("lzMsgs");threadEl=$("lzThread");welcomeEl=$("lzWelcome");
  inputEl=$("lzInput");sendBtn=$("lzSend");stopBtn=$("lzStop");
  titleEl=$("lzTitle");subEl=$("lzSub");sessionsEl=$("lzSessions");

  (cfg.sessions||[]).forEach(function(s){S.sessions.set(s.id,s)});
  renderSessions();

  inputEl.addEventListener("input",autosize);
  inputEl.addEventListener("keydown",function(e){
    if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();if(!sendBtn.disabled)send()}
  });
  sendBtn.addEventListener("click",send);

  $("lzNewChat").addEventListener("click",newChat);
  $("lzMenuBtn").addEventListener("click",function(){
    $("lzSidebar").classList.add("open");$("lzScrim").hidden=false;
  });
  $("lzSbClose").addEventListener("click",closeSidebarMobile);
  $("lzScrim").addEventListener("click",closeSidebarMobile);

  $("lzAttachBtn").addEventListener("click",function(){$("lzFileInput").click()});
  stopBtn.addEventListener("click",function(){if(S.abort)S.abort.abort()});
  if(window.LazyDoc)LazyDoc.bindSession(function(){return S.sessionId});
  else setTimeout(function(){if(window.LazyDoc)LazyDoc.bindSession(function(){return S.sessionId})},60);
  $("lzFileInput").addEventListener("change",function(){
    uploadFile(this.files&&this.files[0]);this.value="";
  });
  document.querySelectorAll(".lz-card").forEach(function(card){
    card.addEventListener("click",function(){
      if(card.hasAttribute("data-attach")){$("lzFileInput").click();return}
      inputEl.value=card.getAttribute("data-fill");
      autosize();inputEl.focus();
    });
  });
  window.addEventListener("keydown",function(e){
    if(e.key==="Escape"){
      if(window.LazyDoc&&LazyDoc.isOpen())LazyDoc.close();
      else if($("lzSidebar").classList.contains("open"))closeSidebarMobile();
    }
  });
  autosize();
});
})();

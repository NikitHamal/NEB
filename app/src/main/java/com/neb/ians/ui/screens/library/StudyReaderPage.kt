package com.neb.ians.ui.screens.library

import com.neb.ians.data.api.ApiStudyDoc
import org.json.JSONObject

private fun esc(s: String) = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

/** A string as a JS literal that is also safe inside <script>. */
private fun jsString(s: String) = JSONObject.quote(s).replace("<", "\\u003c")

/** The whole page the WebView shows: the book's HTML in the app's colours, KaTeX from assets. */
internal fun readerPage(doc: ApiStudyDoc, state: StudyReaderState, vars: String, dark: Boolean): String {
    val body = doc.html.replace("src=\"/static/", "src=\"${doc.mediaBase}static/")
    val answers = JSONObject(state.answers.mapKeys { it.key.toString() }.mapValues { if (it.value) 1 else 0 }).toString()
    // a model paper can be taken as a timed test (EXAM_JS); its state comes back from StudyProgress
    val exam = doc.exam?.takeIf { it.minutes > 0 }
        ?.let { JSONObject().put("minutes", it.minutes).put("negative", it.negative).toString() } ?: "null"
    val eyebrow = listOfNotNull(
        state.label,
        doc.area?.takeIf { it.isNotBlank() },
        doc.hours?.takeIf { it.isNotBlank() && it != "0" }?.let { "$it hrs" },
        "${doc.readMin} min read"
    ).joinToString(" · ")
    return """<!doctype html><html lang="${doc.lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="katex/katex.min.css"><style>:root{$vars}$READER_CSS$EXAM_CSS</style></head>
<body class="${if (dark) "dark" else ""}"><article>
<p class="eyebrow">${esc(eyebrow)}</p><h1 class="title">${esc(doc.title)}</h1>
<div class="body">$body</div></article>
<script src="katex/katex.min.js"></script>
<script>var NEB_ANSWERS=$answers, NEB_MIN=${maxOf(1, doc.readMin)}, NEB_PLACE=${state.mark.place}, NEB_READ=${state.mark.read},
NEB_EXAM=$exam, NEB_EXAM_STATE=${jsString(state.examState.orEmpty())}, NEB_DOC=${jsString(state.key)};$READER_JS$ZOOM_JS$EXAM_JS</script>
</body></html>"""
}

private const val READER_CSS = """
:root{--rd-scale:1}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:calc(16px * var(--rd-scale))/1.75 system-ui,-apple-system,Roboto,'Noto Sans','Noto Sans Devanagari',sans-serif;overflow-wrap:break-word}
html:lang(ne) body{line-height:1.9}
article{padding:20px 18px 56px;max-width:760px;margin:0 auto}
.eyebrow{margin:0 0 8px;font-size:13px;font-weight:600;color:var(--pri)}
.title{margin:0 0 20px;font-size:27px;line-height:1.18;font-weight:700;letter-spacing:-.015em;color:var(--ink)}
.body{--rd-fs:calc(16px * var(--rd-scale));font-size:var(--rd-fs)}
.body p{margin:0 0 1em}
.body h2{margin:2.1em 0 .65em;padding-top:.2em;font-size:1.34em;line-height:1.3;font-weight:700;letter-spacing:-.01em;scroll-margin-top:24px}
.body h3{margin:1.65em 0 .5em;font-size:1.12em;line-height:1.35;font-weight:600}
.body h4{margin:1.35em 0 .4em;font-size:1em;font-weight:600}
.body ul,.body ol{margin:0 0 1em;padding-left:1.45em}.body li{margin:.32em 0}.body li.num{list-style:none}
.body strong{font-weight:650}.body a{color:var(--pri);text-decoration:underline;text-underline-offset:2px}
.body hr{border:0;border-top:1px solid var(--line);margin:2em 0}
.body code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.88em;padding:.12em .38em;border-radius:6px;background:var(--card2)}
.body pre{margin:1.2em 0;padding:14px 16px;border-radius:16px;background:var(--card2);border:1px solid var(--line);overflow-x:auto;font-size:.86em;line-height:1.55}.body pre code{background:none;padding:0}
.body blockquote{margin:1.25em 0;padding:.85em 1.05em;border-radius:16px;background:var(--card);border:1px solid var(--line);color:var(--mute)}
.body blockquote>:last-child{margin-bottom:0}
.body table{display:block;max-width:100%;overflow-x:auto;margin:1.4em 0;border:1px solid var(--line);border-radius:16px;border-collapse:separate;border-spacing:0;background:var(--card);font-size:.9em;line-height:1.5;font-variant-numeric:tabular-nums}
.body th,.body td{padding:.6em .85em;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.body th{color:var(--ink);font-size:.82em;font-weight:600;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;background:var(--pri-tint);border-bottom-color:var(--pri-line)}
.body tbody tr:nth-child(even){background:var(--zebra)}
.body tbody td:first-child{font-weight:600}
.body tbody tr:last-child>th,.body tbody tr:last-child>td{border-bottom:0}
.m{white-space:normal}.dm{margin:1em 0;overflow-x:auto;overflow-y:hidden;text-align:center;padding:.2em 0}.dm .m{display:block}.katex{font-size:1.06em}.katex-display{margin:0}
.dv{display:block;margin:.55em 0;padding:.55em .85em;border-radius:12px;background:var(--card);border:1px solid var(--line);overflow-x:auto}
.stps{display:grid;gap:.4em;margin:.55em 0}.stps>.stp{display:block;padding:.5em .8em;border-radius:12px;background:var(--card);border:1px solid var(--line)}
.fxs{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.55em;margin:.9em 0;text-align:center}
.fxs>span{display:flex;align-items:center;justify-content:center;padding:.7em .55em;border-radius:14px;background:var(--card);border:1px solid var(--line);overflow-x:auto}
.eqx .fr{display:inline-block;vertical-align:-.62em;text-align:center}.eqx .fr .fn{display:block;padding:0 .34em 1px;border-bottom:1px solid currentColor}.eqx .fr .fd{display:block;padding:1px .34em 0}
figure{margin:1.6em 0;text-align:center}figure img{display:block;max-width:100%;height:auto;margin:0 auto;border-radius:14px;background:#fff;padding:10px;border:1px solid var(--line)}figure.photo img{padding:0}
figcaption{margin-top:.7em;font-size:.86em;line-height:1.55;color:var(--mute);text-align:left}figcaption .src{display:block;margin-top:.3em;font-size:.85em;opacity:.8}
.photokey{display:grid;grid-template-columns:1fr;gap:.55em;margin:.7em auto 0;text-align:left;font-size:.86em}
.photokey .pk{display:grid;grid-template-columns:auto minmax(0,1fr);gap:.55em;align-items:start;padding:.5em .75em;border:1px solid var(--pri-line);border-radius:12px;background:var(--pri-tint)}
.photokey .pk i{display:grid;place-items:center;margin-top:.12em;min-width:1.45em;height:1.45em;padding:0 .2em;border-radius:20px;background:var(--pri);color:var(--on-pri);font-style:normal;font-weight:700;font-size:.8em;font-variant-numeric:tabular-nums}
.box{--box-c:var(--mute);--box-pad-x:calc(1.1 * var(--rd-fs));margin:1.4em 0;padding:.95em var(--box-pad-x) 1.05em;border-radius:18px;background:var(--card);border:1px solid var(--line)}
.box>:last-child{margin-bottom:0}
.box .bt,details.ans>summary{font-size:.78em;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--mute);margin-bottom:.45em}
.box .bt{color:var(--box-c);margin:0 calc(var(--box-pad-x) * -1) .65em;padding:0 var(--box-pad-x) .55em;border-bottom:1px solid var(--line)}
.box.key{--box-c:var(--pri);background:var(--pri-tint);border-color:var(--pri-line)}.box.key .bt{border-bottom-color:var(--pri-line)}
.box.definition{--box-c:var(--ink)}
.box.example{--box-c:#64748b}
.box.derivation{--box-c:#485a80}
.box.caution{--box-c:#a8650a}
.box.tip{--box-c:#0b7a70}
.box.memory{--box-c:#006782}
.box.note{--box-c:var(--mute)}
body.dark .box.caution{--box-c:#f0b35e}
body.dark .box.tip{--box-c:#5ed3c6}
body.dark .box.derivation{--box-c:#c0c6dc}
body.dark .box.memory{--box-c:#8fdcff}
.chsum{margin:2.1em 0 1.4em;padding:1.1em 1.2em .4em;border-radius:18px;background:var(--card);border:1px solid var(--line)}.chsum h2{margin-top:0;padding-bottom:.45em;border-bottom:1px solid var(--line);font-size:1.15em}
h2.qs{padding-top:1.15em;border-top:1px solid var(--line)}
.marks{margin-left:.35em;padding:.08em .52em;border-radius:20px;font-size:.74em;font-weight:600;color:var(--mute);background:var(--card2);white-space:nowrap}
.opts{display:grid;gap:.48em;margin:.6em 0 .25em}.opts.c3,.opts.c4{grid-template-columns:repeat(2,minmax(0,1fr))}.opts.c2,.opts.c1{grid-template-columns:1fr}
.opt{display:flex;gap:.55em;align-items:baseline;padding:.55em .8em;border-radius:14px;border:1px solid var(--line);background:var(--card);line-height:1.45;-webkit-tap-highlight-color:transparent}
.opt>.ob{display:block;min-height:0;height:auto;flex:1 1 auto;min-width:0;color:inherit}
.opt>i{flex:none;font-style:normal;font-weight:700;font-size:.85em;color:var(--mute)}.opt>i:after{content:"."}
[data-key] .opt{cursor:pointer}[data-key] .opt:active{background:var(--card2)}
.opt.right{border-color:#1f8a4c;background:rgba(31,138,76,.12)}.opt.right>i{color:#1f8a4c}
.opt.wrong{border-color:#c2412d;background:rgba(194,65,45,.11)}.opt.wrong>i{color:#c2412d}
body.dark .opt.right>i{color:#5fd391}body.dark .opt.wrong>i{color:#ff8a73}
ol.mcq>li,.mcq-p{margin-bottom:1.1em}.mcq-p>p{margin-bottom:.25em}
.parts{display:block;margin:.4em 0 0}.part{display:block;margin:.35em 0;padding-left:1.9em;text-indent:-1.9em}.part>i{display:inline-block;width:1.9em;text-indent:0;font-style:normal;font-weight:600;color:var(--mute)}
details.ans{margin:1em 0 1.55em;border-radius:16px;border:1px dashed var(--line2);background:transparent}
details.ans>summary{display:flex;align-items:center;margin:0;padding:.85em 1.05em;list-style:none;color:var(--ink);cursor:pointer}details.ans>summary::-webkit-details-marker{display:none}
details.ans>summary:after{content:"Show";margin-left:auto;text-transform:none;letter-spacing:.01em;font-size:.95em;font-weight:600;color:var(--pri)}
details.ans[open]{border-style:solid;border-color:var(--line);background:var(--card)}details.ans[open]>summary{border-bottom:1px solid var(--line);margin-bottom:.65em}details.ans[open]>summary:after{content:"Hide";color:var(--mute)}
.ans-body{padding:0 1.05em 1em}.ans-body>:last-child{margin-bottom:0}.ansline{margin:0 0 .5em}
.tip{font-size:.86em;color:var(--mute);margin:.2em 0 .85em;padding:.65em .9em;border-radius:14px;background:var(--card);border:1px solid var(--line)}
.score{margin:2em 0 0;padding:1em 1.15em;border-radius:18px;background:var(--card);border:1px solid var(--line);font-size:.95em}
.score button,.resume{border:0;background:var(--pri);color:var(--on-pri);font:600 14px system-ui,sans-serif;border-radius:28px;padding:10px 18px;margin-top:8px}
.resume{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);border:1px solid var(--line);z-index:5}
.zf{position:relative;display:inline-block;max-width:100%;cursor:zoom-in}.zf img{display:block}
.zf .zb{position:absolute;right:8px;bottom:8px;width:30px;height:30px;border-radius:15px;background:rgba(20,20,20,.68);color:#fff;display:flex;align-items:center;justify-content:center;pointer-events:none}
.zoom{position:fixed;inset:0;z-index:30;background:#0b0b0b;display:flex;flex-direction:column;-webkit-user-select:none;user-select:none}
.zoom-stage{flex:1;display:flex;align-items:center;justify-content:center;overflow:hidden;touch-action:none}
.zoom-stage img{max-width:100%;max-height:100%;background:#fff;border-radius:8px;transform-origin:50% 50%}
.zoom-x{position:absolute;z-index:2;top:12px;right:12px;width:44px;height:44px;border:1px solid rgba(255,255,255,.22);border-radius:22px;background:rgba(28,28,28,.85);color:#fff;font:400 26px/44px system-ui,sans-serif;padding:0}
.zoom-cap{margin:0;padding:10px 18px 16px;max-height:28vh;overflow:auto;color:#d6d6d6;font-size:13px;line-height:1.5}
.zoom-hint{position:absolute;z-index:2;left:50%;bottom:calc(28vh + 8px);transform:translateX(-50%);padding:6px 14px;border-radius:28px;background:rgba(255,255,255,.14);color:#eee;font-size:12px;transition:opacity .4s}
"""

private const val READER_JS = """
(function(){
var body=document.querySelector('.body');
function ty(el){if(el.dataset.done)return;el.dataset.done=1;try{katex.render(el.textContent,el,{throwOnError:false,displayMode:el.classList.contains('d'),strict:'ignore'})}catch(e){}}
var ms=document.querySelectorAll('.m');
if(window.katex){if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){ty(e.target);io.unobserve(e.target)}})},{rootMargin:'800px 0px'});ms.forEach(function(m){io.observe(m)})}else ms.forEach(ty)}
var qs=[].slice.call(body.querySelectorAll('ol.mcq > li[data-key], .mcq-p[data-key]'));
function mark(q,choice){var k=q.getAttribute('data-key');q.classList.add('done');q.querySelectorAll('.opt').forEach(function(o){var l=o.getAttribute('data-opt');o.classList.toggle('right',l===k);o.classList.toggle('wrong',l===choice&&choice!==k)})}
function score(){var el=document.querySelector('.score');if(!el)return;var a=0,r=0;qs.forEach(function(q){if(q.classList.contains('done')){a++;if(q.dataset.ok==='1')r++}});
el.style.display=a?'block':'none';el.firstChild.textContent=r+' of '+a+' right'+(a<qs.length?' · '+(qs.length-a)+' still to try':'')}
qs.forEach(function(q,i){q.querySelectorAll('.opt').forEach(function(o){if(!o.getAttribute('data-opt')){var t=o.querySelector('i');o.setAttribute('data-opt',t?t.textContent.trim():'')}
o.addEventListener('click',function(){if(window.nebExam&&nebExam.on())return;if(q.classList.contains('done'))return;var ok=o.getAttribute('data-opt')===q.getAttribute('data-key');q.dataset.ok=ok?'1':'0';mark(q,o.getAttribute('data-opt'));NebStudy.answer(i,ok);score()})});
if(NEB_ANSWERS[i]!==undefined){q.dataset.ok=String(NEB_ANSWERS[i]);mark(q,NEB_ANSWERS[i]?q.getAttribute('data-key'):'')}});
if(qs.length){var first=qs[0].tagName==='LI'?qs[0].parentNode:qs[0];var tip=document.createElement('p');tip.className='tip';tip.textContent='Tap an option to check it. Worked answers stay folded until you open them.';first.parentNode.insertBefore(tip,first);
var sc=document.createElement('div');sc.className='score';sc.appendChild(document.createTextNode(''));var b=document.createElement('button');b.textContent='Try the questions again';
b.onclick=function(){NebStudy.clear();qs.forEach(function(q){q.classList.remove('done');delete q.dataset.ok;q.querySelectorAll('.opt').forEach(function(o){o.classList.remove('right','wrong')})});score()};
sc.appendChild(document.createElement('br'));sc.appendChild(b);document.querySelector('article').appendChild(sc);score()}
window.nebAnswers=function(open){if(window.nebExam&&nebExam.on())return;body.querySelectorAll('details.ans').forEach(function(d){d.open=open})};
window.nebGo=function(id){var h=document.getElementById(id);if(h)window.scrollTo({top:h.getBoundingClientRect().top+scrollY-12,behavior:'smooth'})};
var rate=100/(NEB_MIN*60*0.25),credit=NEB_READ,here=0,last=Date.now(),sent=0;
function pos(){var h=document.documentElement.scrollHeight-innerHeight;return h>0?Math.max(0,Math.min(100,100*scrollY/h)):100}
function send(){if(Date.now()-sent<2000)return;sent=Date.now();NebStudy.reading(Math.round(credit),Math.round(here))}
addEventListener('scroll',function(){here=pos();send()},{passive:true});
setInterval(function(){var n=Date.now(),dt=Math.min(5,(n-last)/1000);last=n;here=pos();if(here>credit){credit=Math.min(here,credit+rate*dt);send()}},1000);
if(NEB_PLACE>4&&NEB_PLACE<95){var r=document.createElement('button');r.className='resume';r.textContent='Resume where you stopped ('+NEB_PLACE+'%)';
r.onclick=function(){var h=document.documentElement.scrollHeight-innerHeight;scrollTo({top:h*NEB_PLACE/100,behavior:'smooth'});r.remove()};document.body.appendChild(r);
setTimeout(function(){if(r.parentNode)r.remove()},9000);addEventListener('scroll',function x(){if(scrollY>200&&r.parentNode){r.remove();removeEventListener('scroll',x)}})}
})();
"""

/* Figures and photographs open full screen: pinch or double-tap to zoom, drag to pan, the close
 * button or Back to return. The page tells the app through NebStudy.zoom so Back closes the
 * viewer instead of leaving the chapter. */
private const val ZOOM_JS = """
(function(){
var ICON='<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path fill="currentColor" d="M4 4h6v2H7.41l3.3 3.29-1.42 1.42L6 7.41V10H4V4zm16 16h-6v-2h2.59l-3.3-3.29 1.42-1.42L18 16.59V14h2v6z"/></svg>';
var view=null,img=null,s=1,tx=0,ty=0,W=0,H=0,bw=0,bh=0,g=null,lastTap=0,moved=false;
function apply(){img.style.transform='translate('+tx+'px,'+ty+'px) scale('+s+')'}
function clamp(){var mx=Math.max(0,(bw*s-W)/2),my=Math.max(0,(bh*s-H)/2);tx=Math.max(-mx,Math.min(mx,tx));ty=Math.max(-my,Math.min(my,ty))}
function fit(){var st=view.firstChild,nw=img.naturalWidth||1,nh=img.naturalHeight||1,p=Math.min(24,Math.round(st.clientWidth*.04)),f=Math.min((st.clientWidth-2*p)/nw,(st.clientHeight-2*p)/nh,/[.]svg\b/i.test(img.src)?3:1);img.style.width=Math.round(nw*f)+'px';img.style.height=Math.round(nh*f)+'px'}
function measure(){var st=view.firstChild;fit();W=st.clientWidth;H=st.clientHeight;var t=img.style.transform;img.style.transform='none';bw=img.offsetWidth;bh=img.offsetHeight;img.style.transform=t}
function zoomAt(ns,px,py){ns=Math.max(1,Math.min(6,ns));var r=view.firstChild.getBoundingClientRect(),cx=r.left+W/2,cy=r.top+H/2;var ux=(px-cx-tx)/s,uy=(py-cy-ty)/s;s=ns;tx=px-cx-ux*s;ty=py-cy-uy*s;if(s===1){tx=0;ty=0}clamp();apply()}
function close(){if(!view)return;view.remove();view=null;img=null;document.body.style.overflow='';try{NebStudy.zoom(false)}catch(e){}}
window.nebZoomClose=close;
function open(src,alt,cap){
view=document.createElement('div');view.className='zoom';view.setAttribute('role','dialog');view.setAttribute('aria-modal','true');
var st=document.createElement('div');st.className='zoom-stage';img=document.createElement('img');img.src=src;img.alt=alt||'';st.appendChild(img);view.appendChild(st);
var x=document.createElement('button');x.className='zoom-x';x.setAttribute('aria-label','Close');x.textContent='×';x.onclick=close;view.appendChild(x);
if(cap){var c=document.createElement('p');c.className='zoom-cap';c.textContent=cap;view.appendChild(c)}
var hint=document.createElement('span');hint.className='zoom-hint';hint.textContent='Pinch or double-tap to zoom';view.appendChild(hint);setTimeout(function(){hint.style.opacity='0'},1800);
document.body.appendChild(view);document.body.style.overflow='hidden';s=1;tx=0;ty=0;
img.onload=measure;if(img.complete)measure();
st.addEventListener('touchstart',function(e){moved=false;var t=e.touches;if(t.length===2){var dx=t[0].clientX-t[1].clientX,dy=t[0].clientY-t[1].clientY;g={d:Math.hypot(dx,dy),s:s,mx:(t[0].clientX+t[1].clientX)/2,my:(t[0].clientY+t[1].clientY)/2,tx:tx,ty:ty}}else if(t.length===1){g={x:t[0].clientX,y:t[0].clientY,tx:tx,ty:ty}}},{passive:true});
st.addEventListener('touchmove',function(e){if(!g)return;e.preventDefault();moved=true;var t=e.touches;
if(t.length===2&&g.d){var dx=t[0].clientX-t[1].clientX,dy=t[0].clientY-t[1].clientY,mx=(t[0].clientX+t[1].clientX)/2,my=(t[0].clientY+t[1].clientY)/2;
var r=st.getBoundingClientRect(),cx=r.left+W/2,cy=r.top+H/2,ns=Math.max(1,Math.min(6,g.s*Math.hypot(dx,dy)/g.d)),ux=(g.mx-cx-g.tx)/g.s,uy=(g.my-cy-g.ty)/g.s;s=ns;tx=mx-cx-ux*s;ty=my-cy-uy*s;clamp();apply()}
else if(t.length===1&&g.x!==undefined&&s>1){tx=g.tx+t[0].clientX-g.x;ty=g.ty+t[0].clientY-g.y;clamp();apply()}},{passive:false});
st.addEventListener('touchend',function(e){var t=e.changedTouches[0];if(e.touches.length===0){if(!moved&&t){var now=Date.now();if(now-lastTap<300){zoomAt(s>1?1:2.5,t.clientX,t.clientY);lastTap=0}else{lastTap=now;if(s===1&&e.target===st)setTimeout(function(){if(lastTap&&Date.now()-lastTap>=290)close()},310)}}g=null;if(s<1.02){s=1;tx=0;ty=0;apply()}}else if(e.touches.length===1){g={x:e.touches[0].clientX,y:e.touches[0].clientY,tx:tx,ty:ty}}});
try{NebStudy.zoom(true)}catch(e){}
}
document.querySelectorAll('.body figure img').forEach(function(im){
var w=document.createElement('span');w.className='zf';im.parentNode.insertBefore(w,im);w.appendChild(im);
var b=document.createElement('span');b.className='zb';b.innerHTML=ICON;w.appendChild(b);
w.addEventListener('click',function(){var f=im.closest('figure'),cap=f&&f.querySelector('figcaption');open(im.currentSrc||im.src,im.alt,cap?cap.textContent.replace(/\s+/g,' ').trim():'')})});
addEventListener('resize',function(){if(view){measure();clamp();apply()}});
})();
"""

/* A model paper (doc.exam set) can be taken as a timed test: the keys and the folded answers are
 * hidden, a countdown runs to an absolute deadline (no pause; it keeps running while the student is
 * away), one option per question can be picked, changed or cleared, a palette jumps to any
 * question, and Submit or the deadline scores +1 per right answer and -negative per wrong one, with
 * a breakdown by the h2 section each question sits under; then the keys and explanations open.
 * The state (start, deadline, question count, picks, finish) goes to the app through NebStudy.examSave and comes
 * back as NEB_EXAM_STATE; NebStudy.exam(on) lets the screen hide "Show answers" meanwhile, and the
 * sheets borrow NebStudy.zoom so Back closes them first. */
private const val EXAM_CSS = """
.xstart{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:-4px 0 20px;padding:13px 15px;border-radius:18px;background:var(--card);border:1px solid var(--line)}
.xstart span{font-size:13px;line-height:1.4;color:var(--mute)}
.xbtn,.xbtn2{border:0;border-radius:28px;padding:10px 16px;font:600 14px/1.2 system-ui,sans-serif;cursor:pointer;-webkit-tap-highlight-color:transparent}
.xbtn{background:var(--pri);color:var(--on-pri)}.xbtn2{background:var(--card2);color:var(--ink);border:1px solid var(--line)}
.xbar{display:none}
body.exam-on .xbar{display:flex;position:fixed;left:12px;right:12px;bottom:12px;z-index:20;align-items:center;gap:8px;padding:10px 12px;border-radius:22px;background:var(--card);border:1px solid var(--line)}
.xtime{flex:none;padding:8px 10px;border-radius:12px;background:var(--card2);font:700 17px/1 ui-monospace,'Roboto Mono',monospace;font-variant-numeric:tabular-nums}
.xbar.low .xtime{background:#c2412d;color:#fff}
.xcount{flex:1;min-width:0;font-size:12px;line-height:1.3;color:var(--mute)}
.xbar .xbtn,.xbar .xbtn2{padding:9px 14px;font-size:13px}
body.exam-on article{padding-bottom:120px}
body.exam-on details.ans,body.exam-on .xkey,body.exam-on .tip,body.exam-on .score,body.exam-on .resume,body.exam-on .xstart{display:none!important}
body.exam-review .tip,body.exam-review .score,body.exam-review .xstart{display:none!important}
.xclr{display:none}
body.exam-on .xans>.xclr{display:inline-flex;align-items:center;margin:.45em 0 0;padding:4px 12px;border:1px solid var(--line);border-radius:20px;background:none;font:600 12.5px system-ui,sans-serif;color:var(--mute);cursor:pointer}
body.exam-on [data-xi] .opt{cursor:pointer}
.opt.xpick{border-color:var(--pri);background:var(--pri-tint)}.opt.xpick>i{color:var(--pri)}
.xflash{outline:2px solid var(--pri);outline-offset:6px;border-radius:8px}
body.exam-review .xblank:before{content:'Not answered';display:block;margin-bottom:.2em;font-size:.72em;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--mute)}
.xres{margin:0 0 24px;padding:16px 18px;border-radius:20px;background:var(--card);border:1px solid var(--line)}
.xres[hidden]{display:none}
.xres .xk{margin:0;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--mute)}
.xscore{margin:.15em 0 .2em;font-size:15px}.xscore b{font-size:34px;line-height:1.15;letter-spacing:-.02em}
.xmeta{margin:0 0 .8em;font-size:13px;line-height:1.5;color:var(--mute)}
.xtab{width:100%;margin:.2em 0 1em;border-collapse:collapse;font-size:13px;line-height:1.4}
.xtab th,.xtab td{padding:.45em .4em;border-bottom:1px solid var(--line);text-align:right}.xtab th{font-weight:600;color:var(--mute)}
.xtab th:first-child,.xtab td:first-child{text-align:left;padding-left:0}
.xm-note{font-size:13px;color:var(--mute)}
.xm{position:fixed;top:0;right:0;bottom:0;left:0;z-index:40;display:flex;align-items:flex-end;justify-content:center;background:rgba(0,0,0,.45)}
.xm-card{width:100%;max-width:560px;max-height:86vh;overflow:auto;padding:18px 18px 22px;border-radius:20px 20px 0 0;background:var(--bg);color:var(--ink)}
.xm-card h3{margin:0 0 .5em;font-size:18px;line-height:1.3}.xm-card p{margin:0 0 .7em;font-size:14.5px;line-height:1.5}
.xm-row{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:10px;margin-top:14px}
.xres .xm-row{display:grid;grid-template-columns:1fr 1fr}.xres .xm-row button{padding:10px 8px}
.xm-card .xpal-h,.xpal-h{margin:14px 0 6px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--mute)}
.xpal-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(42px,1fr));gap:6px}
.xpn{height:40px;padding:0;border-radius:10px;border:1px solid var(--line2);background:var(--bg);color:var(--ink);font:600 13px system-ui,sans-serif}
.xpn.on{background:var(--ink);border-color:var(--ink);color:var(--bg)}
"""

private const val EXAM_JS = """
(function(){
var X=window.NEB_EXAM;if(!X||!(X.minutes>0))return;
var body=document.querySelector('.body'),art=document.querySelector('article');
var qs=[].slice.call(body.querySelectorAll('ol.mcq > li[data-key], .mcq-p[data-key]'));if(!qs.length)return;
var MS=X.minutes*60000,NEG=Math.max(0,+X.negative||0),LS='neb.exam.v1:'+(window.NEB_DOC||''),bridge=!!(window.NebStudy&&NebStudy.examSave);
var st=null,timer=0,modal=null,stash=null;
try{if(window.NEB_EXAM_STATE)st=JSON.parse(NEB_EXAM_STATE)}catch(e){st=null}
if(!st&&!bridge){try{st=JSON.parse(localStorage.getItem(LS)||'null')}catch(e){st=null}}
if(st&&!(st.s>0&&st.e>st.s&&(!st.n||st.n===qs.length)))st=null;if(st)st.a=st.a||{};
function on(){return !!(st&&!st.f)}
window.nebExam={on:on};
function save(){var j=st?JSON.stringify(st):'';if(bridge){try{NebStudy.examSave(j)}catch(e){}return}try{if(j)localStorage.setItem(LS,j);else localStorage.removeItem(LS)}catch(e){}}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fmt(n){return String(Math.round(n*100)/100)}
function hms(ms){var s=Math.max(0,Math.ceil(ms/1000)),h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60;return h+':'+(m<10?'0':'')+m+':'+(x<10?'0':'')+x}
/* each question: its printed number (a paper is numbered straight through, ol start="41") and the h2 it sits under */
function num(q,i){if(q.tagName==='LI'){var ol=q.parentNode;return(parseInt(ol.getAttribute('start'),10)||1)+[].indexOf.call(ol.children,q)}var b=q.querySelector('strong');return parseInt(b&&b.textContent,10)||i+1}
function head(q){var n=q;while(n.parentNode&&n.parentNode!==body)n=n.parentNode;for(;n;n=n.previousElementSibling)if(n.tagName==='H2')return n;return null}
var Q=qs.map(function(q,i){q.setAttribute('data-xi',i);return{i:i,el:q,n:num(q,i),key:q.getAttribute('data-key'),h:head(q)}});
var secs=[];Q.forEach(function(x){var s=secs[secs.length-1];if(!s||s.h!==x.h){s={h:x.h,t:x.h?x.h.textContent.replace(/\s*\([^()]*\)\s*$/,'').trim():'Questions',q:[]};secs.push(s)}s.q.push(x)});
/* sections that hold only the answer key are hidden while the clock runs */
[].forEach.call(body.querySelectorAll('h2'),function(h){var g=[h],hasQ=false,hasA=false;for(var n=h.nextElementSibling;n&&n.tagName!=='H2';n=n.nextElementSibling){g.push(n);if(n.matches('details.ans')||n.querySelector('details.ans'))hasA=true;if(n.matches('ol.mcq,.mcq-p')||n.querySelector('[data-xi]'))hasQ=true}if(hasA&&!hasQ)g.forEach(function(e){e.classList.add('xkey')})});
var box=document.createElement('div');box.className='xstart';
box.innerHTML='<button type="button" class="xbtn">Take as a timed test</button><span>'+Q.length+' questions · '+X.minutes+' min'+(NEG?' · −'+fmt(NEG)+' a wrong answer':'')+'</span>';
var res=document.createElement('section');res.className='xres';res.hidden=true;
art.insertBefore(box,body);art.insertBefore(res,body);
box.firstChild.onclick=intro;
var bar=document.createElement('div');bar.className='xbar';
bar.innerHTML='<span class="xtime"></span><span class="xcount"></span><button type="button" class="xbtn2">Questions</button><button type="button" class="xbtn">Submit</button>';
document.body.appendChild(bar);
var tm=bar.children[0],cnt=bar.children[1];bar.children[2].onclick=palette;bar.children[3].onclick=ask;
Q.forEach(function(x){var b=document.createElement('button');b.type='button';b.className='xclr';b.textContent='Clear';b.onclick=function(){if(on())pick(x,null)};x.el.appendChild(b)});
body.addEventListener('click',function(e){if(!on())return;var o=e.target.closest&&e.target.closest('.opt');var q=o&&o.closest('[data-xi]');if(!q)return;pick(Q[+q.getAttribute('data-xi')],o.getAttribute('data-opt'))});
function answered(){return Object.keys(st.a).length}
function paintQ(x){var l=st&&st.a[x.i];x.el.classList.toggle('xans',!!l);[].forEach.call(x.el.querySelectorAll('.opt'),function(o){o.classList.toggle('xpick',!!l&&o.getAttribute('data-opt')===l)})}
function count(){var a=answered();cnt.textContent=a+' answered · '+(Q.length-a)+' left'}
function pick(x,l){if(l)st.a[x.i]=l;else delete st.a[x.i];paintQ(x);count();save()}
function tick(){if(!on())return;var left=st.e-Date.now();if(left<=0){finish(true);return}tm.textContent=hms(left);bar.classList.toggle('low',left<=300000)}
/* the practice marks (tapped earlier) would give the keys away: kept aside, put back for practice */
function keep(){if(!stash)stash=qs.map(function(q){return[q.className,[].map.call(q.querySelectorAll('.opt'),function(o){return o.className})]})}
function wipe(){Q.forEach(function(x){x.el.classList.remove('done','xans','xblank');[].forEach.call(x.el.querySelectorAll('.opt'),function(o){o.classList.remove('right','wrong','xpick')})})}
function closeModal(){if(!modal)return;modal.remove();modal=null;try{NebStudy.zoom(false)}catch(e){}}
function openModal(h,wire){closeModal();modal=document.createElement('div');modal.className='xm';modal.innerHTML='<div class="xm-card" role="dialog" aria-modal="true">'+h+'</div>';
modal.addEventListener('click',function(e){if(e.target===modal)closeModal()});document.body.appendChild(modal);wire(modal);try{NebStudy.zoom(true)}catch(e){}}
/* Back (the app routes it through nebZoomClose) closes a sheet before it leaves the chapter */
var zc=window.nebZoomClose;window.nebZoomClose=function(){if(modal){closeModal();return}if(zc)zc()};
var go=window.nebGo;window.nebGo=function(id){var h=document.getElementById(id);if(on()&&h&&h.classList.contains('xkey'))return;if(go)go(id)};
function btn(cls,x,t){return'<button type="button" class="'+cls+'" data-x="'+x+'">'+t+'</button>'}
function intro(){openModal('<h3>Take this paper as a timed test</h3><p><b>'+Q.length+' questions · '+X.minutes+' minutes</b></p><p>'+(NEG?'+1 for a right answer, −'+fmt(NEG)+' for a wrong one, 0 for a blank.':'+1 for a right answer, 0 for a wrong one or a blank.')+'</p><p>Answers and explanations stay hidden until you submit. The clock cannot be paused: it keeps running if you leave this page.</p><div class="xm-row">'+btn('xbtn2','no','Cancel')+btn('xbtn','go','Start the test')+'</div>',
function(m){m.querySelector('[data-x=no]').onclick=closeModal;m.querySelector('[data-x=go]').onclick=function(){closeModal();begin()}})}
function begin(){var now=Date.now();st={s:now,e:now+MS,n:Q.length,a:{},f:0};save();enter();window.scrollTo({top:Math.max(0,body.getBoundingClientRect().top+scrollY-12),behavior:'smooth'})}
function enter(){keep();wipe();res.hidden=true;document.body.classList.remove('exam-review');document.body.classList.add('exam-on');
body.querySelectorAll('details.ans').forEach(function(d){d.open=false});Q.forEach(paintQ);count();clearInterval(timer);timer=setInterval(tick,500);tick();try{NebStudy.exam(true)}catch(e){}}
function palette(){var a=answered(),h='<h3>Questions</h3><p class="xm-note">'+a+' answered · '+(Q.length-a)+' left. Tap a number to go to it.</p>';
secs.forEach(function(s){h+='<p class="xpal-h">'+esc(s.t)+'</p><div class="xpal-g">';s.q.forEach(function(x){h+='<button type="button" class="xpn'+(st.a[x.i]?' on':'')+'" data-i="'+x.i+'">'+x.n+'</button>'});h+='</div>'});
openModal(h+'<div class="xm-row">'+btn('xbtn2','no','Close')+btn('xbtn','sub','Submit')+'</div>',function(m){m.querySelector('[data-x=no]').onclick=closeModal;m.querySelector('[data-x=sub]').onclick=function(){closeModal();ask()};
[].forEach.call(m.querySelectorAll('.xpn'),function(b){b.onclick=function(){closeModal();jump(Q[+b.getAttribute('data-i')])}})})}
function jump(x){window.scrollTo({top:Math.max(0,x.el.getBoundingClientRect().top+scrollY-16),behavior:'smooth'});x.el.classList.add('xflash');setTimeout(function(){x.el.classList.remove('xflash')},1500)}
function ask(){if(!on())return;var b=Q.length-answered();if(!b){finish(false);return}
openModal('<h3>Submit the test?</h3><p>'+b+(b===1?' question is':' questions are')+' not answered. A blank scores 0.</p><div class="xm-row">'+btn('xbtn2','no','Keep going')+btn('xbtn','go','Submit now')+'</div>',function(m){m.querySelector('[data-x=no]').onclick=closeModal;m.querySelector('[data-x=go]').onclick=function(){finish(false)}})}
function finish(out){if(!on())return;st.f=Math.min(Date.now(),st.e);if(out)st.t=1;save();clearInterval(timer);closeModal();review(true)}
function review(scroll){keep();wipe();document.body.classList.remove('exam-on');document.body.classList.add('exam-review');
var T={c:0,w:0,b:0},rows=secs.map(function(s){var r={t:s.t,n:s.q.length,c:0,w:0,b:0};s.q.forEach(function(x){var l=st.a[x.i];if(!l)r.b++;else if(l===x.key)r.c++;else r.w++});T.c+=r.c;T.w+=r.w;T.b+=r.b;return r});
Q.forEach(function(x){var l=st.a[x.i];x.el.classList.add('done');x.el.classList.toggle('xblank',!l);[].forEach.call(x.el.querySelectorAll('.opt'),function(o){var v=o.getAttribute('data-opt');o.classList.toggle('right',v===x.key);o.classList.toggle('wrong',!!l&&v===l&&l!==x.key)})});
body.querySelectorAll('details.ans').forEach(function(d){d.open=true});
var att=T.c+T.w,used=Math.min(st.f,st.e)-st.s;
var h='<p class="xk">Timed test result</p><p class="xscore"><b>'+fmt(T.c-NEG*T.w)+'</b> / '+Q.length+'</p><p class="xmeta">'+T.c+' right · '+T.w+' wrong · '+T.b+' blank · accuracy '+(att?fmt(100*T.c/att)+'%':'–')+' · time '+hms(used)+(st.t?' (time ran out)':'')+'</p>';
if(rows.length>1){h+='<table class="xtab"><thead><tr><th>Section</th><th>Right</th><th>Wrong</th><th>Blank</th><th>Score</th></tr></thead><tbody>';rows.forEach(function(r){h+='<tr><td>'+esc(r.t)+'</td><td>'+r.c+'</td><td>'+r.w+'</td><td>'+r.b+'</td><td><b>'+fmt(r.c-NEG*r.w)+'</b> / '+r.n+'</td></tr>'});h+='</tbody></table>'}
h+='<p class="xm-note">Right answers are marked, your wrong picks crossed, and every explanation is open below.</p><div class="xm-row">'+btn('xbtn2','practice','Back to practice')+btn('xbtn','retake','Retake the test')+'</div>';
res.innerHTML=h;res.hidden=false;res.querySelector('[data-x=practice]').onclick=practice;res.querySelector('[data-x=retake]').onclick=function(){practice();intro()};
if(scroll)window.scrollTo({top:Math.max(0,res.getBoundingClientRect().top+scrollY-12),behavior:'smooth'});try{NebStudy.exam(false)}catch(e){}}
function practice(){st=null;save();clearInterval(timer);closeModal();wipe();res.hidden=true;document.body.classList.remove('exam-on','exam-review');
if(stash){qs.forEach(function(q,i){q.className=stash[i][0];[].forEach.call(q.querySelectorAll('.opt'),function(o,j){if(stash[i][1][j]!=null)o.className=stash[i][1][j]})});stash=null}
body.querySelectorAll('details.ans').forEach(function(d){d.open=false});try{NebStudy.exam(false)}catch(e){}}
document.addEventListener('visibilitychange',function(){if(!document.hidden)tick()});
if(st){if(st.f)review(false);else if(Date.now()>=st.e)finish(true);else enter()}
})();
"""

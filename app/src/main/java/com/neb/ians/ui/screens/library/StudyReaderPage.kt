package com.neb.ians.ui.screens.library

import com.neb.ians.data.api.ApiStudyDoc
import org.json.JSONObject

private fun esc(s: String) = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

/** The whole page the WebView shows: the book's HTML in the app's colours, KaTeX from assets. */
internal fun readerPage(doc: ApiStudyDoc, state: StudyReaderState, vars: String, dark: Boolean): String {
    val body = doc.html.replace("src=\"/static/", "src=\"${doc.mediaBase}static/")
    val answers = JSONObject(state.answers.mapKeys { it.key.toString() }.mapValues { if (it.value) 1 else 0 }).toString()
    val eyebrow = listOfNotNull(state.label, doc.area?.takeIf { it.isNotBlank() }, "${doc.readMin} min read").joinToString(" · ")
    return """<!doctype html><html lang="${doc.lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="katex/katex.min.css"><style>:root{$vars}$READER_CSS</style></head>
<body class="${if (dark) "dark" else ""}"><article>
<p class="eyebrow">${esc(eyebrow)}</p><h1 class="title">${esc(doc.title)}</h1>
<div class="body">$body</div></article>
<script src="katex/katex.min.js"></script>
<script>var NEB_ANSWERS=$answers, NEB_MIN=${maxOf(1, doc.readMin)}, NEB_PLACE=${state.mark.place}, NEB_READ=${state.mark.read};$READER_JS$ZOOM_JS</script>
</body></html>"""
}

private const val READER_CSS = """
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.72 system-ui,-apple-system,Roboto,'Noto Sans','Noto Sans Devanagari',sans-serif;overflow-wrap:break-word}
article{padding:18px 18px 48px;max-width:760px;margin:0 auto}
.eyebrow{margin:0 0 6px;font-size:13px;font-weight:600;color:var(--mute)}
.title{margin:0 0 18px;font-size:26px;line-height:1.2;font-weight:700;letter-spacing:-.01em}
.body p{margin:0 0 1em}.body h2{margin:2em 0 .6em;font-size:1.3em;line-height:1.3}.body h3{margin:1.6em 0 .5em;font-size:1.1em}
.body ul,.body ol{padding-left:1.4em}.body li{margin:.3em 0}.body li.num{list-style:none}
.body strong{font-weight:650}.body a{color:var(--ink)}
.body code{font-family:ui-monospace,monospace;font-size:.88em;padding:.1em .3em;border-radius:6px;background:var(--card2)}
.body pre{padding:12px 14px;border-radius:12px;background:var(--card2);overflow-x:auto;font-size:.85em;line-height:1.5}.body pre code{background:none;padding:0}
.body blockquote{margin:1em 0;padding-left:1em;border-left:3px solid var(--line);color:var(--mute)}
.body table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse;margin:1.2em 0;font-size:.88em;line-height:1.5}
.body th,.body td{padding:.5em .7em;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}.body th{background:var(--card);white-space:nowrap}
.m{white-space:normal}.dm{margin:1em 0;overflow-x:auto;overflow-y:hidden;text-align:center}.dm .m{display:block}.katex{font-size:1.05em}.katex-display{margin:0}
.eqx .fr{display:inline-block;vertical-align:-.62em;text-align:center}.eqx .fr .fn{display:block;padding:0 .3em 1px;border-bottom:1px solid currentColor}.eqx .fr .fd{display:block;padding:1px .3em 0}
figure{margin:1.4em 0;text-align:center}figure img{max-width:100%;height:auto;border-radius:12px;background:#fff;padding:8px}figure.photo img{padding:0}
figcaption{margin-top:.6em;font-size:.85em;line-height:1.5;color:var(--mute);text-align:left}figcaption .src{display:block;font-size:.85em;opacity:.8}
.photokey{display:block;text-align:left;font-size:.85em;margin-top:.5em}.photokey .pk{display:block}.photokey .pk i{font-style:normal;font-weight:700;display:inline-block;min-width:1.6em}
.box{margin:1.3em 0;padding:.9em 1em;border-radius:14px;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--line2)}
.box>:last-child{margin-bottom:0}.box .bt,details.ans>summary{font-size:.76em;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--mute);margin-bottom:.4em}
.box.key,.box.definition{border-left-color:var(--ink)}.box.key .bt,.box.definition .bt{color:var(--ink)}
.chsum{margin:2em 0 1.2em;padding:1em 1.1em .3em;border-radius:16px;background:var(--card);border:1px solid var(--line)}.chsum h2{margin-top:0;font-size:1.12em}
h2.qs{padding-top:1em;border-top:1px solid var(--line)}
.marks{margin-left:.3em;padding:.05em .45em;border-radius:99px;font-size:.72em;font-weight:600;color:var(--mute);background:var(--card2);white-space:nowrap}
.opts{display:grid;gap:.45em;margin:.55em 0 .2em}.opts.c4{grid-template-columns:repeat(2,minmax(0,1fr))}.opts.c2,.opts.c1{grid-template-columns:1fr}
.opt{display:flex;gap:.5em;align-items:baseline;padding:.5em .75em;border-radius:12px;border:1px solid var(--line);background:var(--bg);line-height:1.45}
.opt>i{flex:none;font-style:normal;font-weight:700;font-size:.85em;color:var(--mute)}.opt>i:after{content:"."}
[data-key] .opt{cursor:pointer}[data-key] .opt:active{background:var(--card2)}
.opt.right{border-color:#1f8a4c;background:rgba(31,138,76,.12)}.opt.right>i{color:#1f8a4c}
.opt.wrong{border-color:#c2412d;background:rgba(194,65,45,.11)}.opt.wrong>i{color:#c2412d}
body.dark .opt.right>i{color:#5fd391}body.dark .opt.wrong>i{color:#ff8a73}
ol.mcq>li,.mcq-p{margin-bottom:1em}.mcq-p>p{margin-bottom:.2em}
.parts{display:block;margin:.4em 0 0}.part{display:block;margin:.35em 0;padding-left:1.9em;text-indent:-1.9em}.part>i{display:inline-block;width:1.9em;text-indent:0;font-style:normal;font-weight:600;color:var(--mute)}
details.ans{margin:1em 0 1.5em;border-radius:14px;border:1px dashed var(--line2)}
details.ans>summary{display:flex;align-items:center;margin:0;padding:.85em 1em;list-style:none;color:var(--ink)}details.ans>summary::-webkit-details-marker{display:none}
details.ans>summary:after{content:"Show";margin-left:auto;text-transform:none;letter-spacing:0;font-size:1.05em;color:var(--mute)}
details.ans[open]{border-style:solid;background:var(--card)}details.ans[open]>summary:after{content:"Hide"}
.ans-body{padding:0 1em 1em}.ans-body>:last-child{margin-bottom:0}.ansline{margin:0 0 .5em}
.tip{font-size:.85em;color:var(--mute);margin:.2em 0 .8em}.score{margin:2em 0 0;padding:.9em 1em;border-radius:14px;background:var(--card);border:1px solid var(--line);font-size:.95em}
.score button,.resume{border:0;background:var(--ink);color:var(--bg);font:600 14px system-ui,sans-serif;border-radius:99px;padding:9px 16px;margin-top:8px}
.resume{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);box-shadow:0 6px 18px rgba(0,0,0,.25);z-index:5}
.zf{position:relative;display:inline-block;max-width:100%;cursor:zoom-in}.zf img{display:block}
.zf .zb{position:absolute;right:8px;bottom:8px;width:30px;height:30px;border-radius:15px;background:rgba(20,20,20,.62);color:#fff;display:flex;align-items:center;justify-content:center;pointer-events:none}
.zoom{position:fixed;inset:0;z-index:30;background:#0b0b0b;display:flex;flex-direction:column;-webkit-user-select:none;user-select:none}
.zoom-stage{flex:1;display:flex;align-items:center;justify-content:center;overflow:hidden;touch-action:none}
.zoom-stage img{max-width:100%;max-height:100%;background:#fff;border-radius:6px;transform-origin:50% 50%}
.zoom-x{position:absolute;top:10px;right:10px;width:44px;height:44px;border:0;border-radius:22px;background:rgba(255,255,255,.14);color:#fff;font:400 26px/44px system-ui,sans-serif;padding:0}
.zoom-cap{margin:0;padding:10px 18px 16px;max-height:28vh;overflow:auto;color:#d6d6d6;font-size:13px;line-height:1.5}
.zoom-hint{position:absolute;left:50%;bottom:calc(28vh + 8px);transform:translateX(-50%);padding:6px 12px;border-radius:99px;background:rgba(255,255,255,.12);color:#eee;font-size:12px;transition:opacity .4s}
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
o.addEventListener('click',function(){if(q.classList.contains('done'))return;var ok=o.getAttribute('data-opt')===q.getAttribute('data-key');q.dataset.ok=ok?'1':'0';mark(q,o.getAttribute('data-opt'));NebStudy.answer(i,ok);score()})});
if(NEB_ANSWERS[i]!==undefined){q.dataset.ok=String(NEB_ANSWERS[i]);mark(q,NEB_ANSWERS[i]?q.getAttribute('data-key'):'')}});
if(qs.length){var first=qs[0].tagName==='LI'?qs[0].parentNode:qs[0];var tip=document.createElement('p');tip.className='tip';tip.textContent='Tap an option to check it. Worked answers stay folded until you open them.';first.parentNode.insertBefore(tip,first);
var sc=document.createElement('div');sc.className='score';sc.appendChild(document.createTextNode(''));var b=document.createElement('button');b.textContent='Try the questions again';
b.onclick=function(){NebStudy.clear();qs.forEach(function(q){q.classList.remove('done');delete q.dataset.ok;q.querySelectorAll('.opt').forEach(function(o){o.classList.remove('right','wrong')})});score()};
sc.appendChild(document.createElement('br'));sc.appendChild(b);document.querySelector('article').appendChild(sc);score()}
window.nebAnswers=function(open){body.querySelectorAll('details.ans').forEach(function(d){d.open=open})};
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
function measure(){var st=view.firstChild;W=st.clientWidth;H=st.clientHeight;var t=img.style.transform;img.style.transform='none';bw=img.offsetWidth;bh=img.offsetHeight;img.style.transform=t}
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

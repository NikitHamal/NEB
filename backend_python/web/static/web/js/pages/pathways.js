/* Pathways (web). Concept UI from NEBians-Pathways.html on the real /api/pathways/ payload. Generated body: edit the
   concept first, then port. Data shapes come from pathways-data.js. */
(function(){
'use strict';
const root=document.getElementById('pwx');if(!root)return;
const fail=t=>{root.innerHTML='<div class="pw-fail">'+t+'</div>'};
fetch(root.dataset.src,{headers:{Accept:'application/json'}}).then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}).then(P=>{
root.innerHTML='<div class="app"><div class="top" id="pw-top"></div><div id="pw-main"></div><div class="peek" id="pw-peek"></div><nav class="nav" id="pw-nav"></nav><aside class="sheet" id="pw-sheet"></aside></div>';
const DATA=pwAdapt(P),{STAGES,C,K,X,G,COL,CT,SCH,CX}=DATA,TR=DATA.tracks,XGR=DATA.groups,GT=DATA.CTONE,grOf=t=>(TR.find(r=>r[0]===t)||[0,0,0,'gov'])[3];
const PMAX=Math.max(100,...Object.values(K).map(k=>k.pay[2]));
const VISA=Object.keys(G).find(k=>/visa/.test(k))||'';
Object.values(K).forEach(k=>{if(k.lx&&!X[k.lx])k.lx=''});
const firstStage=STAGES.find(s=>s.id==='after12')||STAGES[0],DEF=(()=>{const sm=firstStage.streams[0],withCol=Object.keys(C).find(id=>COL.some(x=>x.c.includes(id)));
  return {stage:firstStage.id,stream:sm.id,course:sm.courses[0]||null,cc:withCol||Object.keys(C)[0],xg:TR[0]?TR[0][0]:'',exam:(Object.values(X).find(x=>TR[0]&&x.g===TR[0][0])||Object.values(X)[0]||{}).id,guide:(Object.values(G)[0]||{}).id}})();
const STAGE_EDU=[0,1,2,3],STAGE_AGE=[14,16,18,22],EDU=['Class 8','SEE','+2','Bachelor','Master'];
const PROV=['Koshi','Madhesh','Bagmati','Gandaki','Lumbini','Karnali','Sudur&shy;pashchim'];
const INT=[['build','Building'],['heal','Healing'],['num','Numbers'],['ppl','People'],['make','Creating'],['law','Justice'],['nature','Nature'],['serve','Serving']];
const STR=[['math','Maths'],['sci','Science'],['bio','Biology'],['lang','Languages'],['biz','Business'],['comp','Computers'],['art','Art']];
const PRI=[['pay','Pay'],['demand','Demand'],['ease','Easy entry'],['cost','Low cost'],['abroad','Abroad'],['near','Near me']];
const IG={build:['tech','sci'],heal:['health'],num:['biz','sci','tech'],ppl:['edu','biz','arts','gov'],make:['arts','tech'],law:['law','gov'],nature:['ag','sci'],serve:['gov','edu','health']};
const SG={math:['tech','sci','biz'],sci:['sci','tech','health','ag'],bio:['health','ag'],lang:['arts','law','edu','gov'],biz:['biz'],comp:['tech'],art:['arts']};
const ABR={tech:1,health:.9,biz:.6,sci:.5,edu:.3,law:.2,arts:.3,ag:.3,gov:0};
const grpOf=c=>{const l=locate(c.id);return l?[l.sm.id]:[]};
const TONES=['pc','tc','yc','gc','rc'],MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],NOW=new Date().getMonth()+1,YEAR=new Date().getFullYear();
const pp=s=>s.split(',').map(x=>{const i=x.lastIndexOf(' ');return[x.slice(0,i),+x.slice(i+1)]});
const rv=o=>[Math.min(100,o.pay[1]/2),o.d,100-o.c,o.f.t[1],o.f.t[0],o.f.t[2]];
const AVG=[0,1,2,3,4,5].map(i=>{const a=Object.values(K);return a.reduce((s,o)=>s+rv(o)[i],0)/a.length});
/* ============ STATE ============ */
const S={view:'explore',stage:DEF.stage,stream:DEF.stream,course:DEF.course,career:null,sel:DEF.course?{t:'course',id:DEF.course}:null,open:false,
  tabs:{course:'journey',career:'pay',exam:'stages'},cmp:null,path:[],back:[],saved:new Set(),q:'',searching:false,lens:null,
  study:'nepal',cc:DEF.cc,prov:null,dist:null,cmax:null,csort:'fee',ab:null,abmax:30,stype:'All',slvl:'All',sk:null,schOpen:null,
  xg:DEF.xg,exam:DEF.exam,edu:2,age:18,woman:'0',gcat:'All',guide:DEF.guide,done:new Set(),docs:new Set(),have:new Set(),
  xf:'all',xs:'soon',gv:'guides',fqt:'All',fqo:null,fqs:'',fqh:new Set(),plan:'match',mi:new Set(),ms:new Set(),mp:new Set(),mq:false,mstep:0,mdone:false,medit:false,mdir:1,qa:false,mstg:DEF.stage,mst:'',my:0,mr:'mid',mopen:null,mweak:false,foc:false,mb:15,exp:3,hrs:3,cpriv:'0',live:'0',aid:0};
let lastKey='',freshT=0,lastWide=false;try{const o=JSON.parse(localStorage.getItem('pw-state')||'{}');['saved','done','docs','have'].forEach(k=>(o[k]||[]).forEach(v=>S[k].add(v)))}catch(e){}
const persist=()=>{try{localStorage.setItem('pw-state',JSON.stringify({saved:[...S.saved],done:[...S.done],docs:[...S.docs],have:[...S.have]}))}catch(e){}};

/* ============ HELPERS ============ */
const $=(s,r=root)=>r.querySelector(s),$$=(s,r=root)=>[...r.querySelectorAll(s)];
const wide=()=>root.clientWidth>=900;
const tog=(set,v)=>set.has(v)?set.delete(v):set.add(v);
const stage=()=>STAGES.find(s=>s.id===S.stage);
const stream=()=>stage().streams.find(s=>s.id===S.stream)||stage().streams[0];
const locate=id=>{for(const st of STAGES)for(const sm of st.streams)if(sm.courses.includes(id))return{st,sm}};
const cur=()=>S.view==='explore'?S.sel:S.view==='exams'?{t:'exam',id:S.exam}:S.view==='guides'?{t:'guide',id:S.guide}:null;
const fmt=v=>+(+v).toFixed(1);
const yr=y=>y<1?Math.round(y*12)+' mo':fmt(y)+' yr';
const dy=d=>d+(d===1?' day':' days');
const lakh=v=>v<=0?'Free':v<1?'NPR '+Math.round(v*100)+'k':'NPR '+fmt(v)+'L';
const num=v=>v>=1e5?fmt(v/1e5)+'L':v>=1e3?fmt(v/1e3)+'k':''+v;
const npr=v=>v?'NPR '+v.toLocaleString('en-IN'):'Free';
const payTxt=p=>'NPR '+p[0]+'–'+p[p.length-1]+'k / month';
const payAt=(k,y)=>y<=5?k.pay[0]+(k.pay[1]-k.pay[0])*y/5:k.pay[1]+(k.pay[2]-k.pay[1])*(y-5)/7;
const hasCol=id=>COL.some(x=>x.c.includes(id));
const inWin=(s,e,m)=>s<=e?m>=s&&m<=e:m>=s||m<=e;
const why=x=>S.edu<x.edu?'Needs '+EDU[x.edu]:x.age&&(S.age<x.age[0]||S.age>x.age[+S.woman?2:1])?'Age '+x.age[0]+'–'+x.age[+S.woman?2:1]:'';
const oddsOf=x=>{const r=x.apps/x.seats;return r>=20?{r,n:Math.round(r),pre:'1 in',post:'',txt:'1 in '+Math.round(r)}:{r,n:Math.round(100/r),pre:'',post:'in 100',txt:Math.round(100/r)+' in 100'}};
const gdone=g=>g.steps.filter((_,i)=>S.done.has(g.id+':'+i)).length;
const gsum=(g,i)=>g.steps.reduce((a,s)=>a+s[i],0);
const ICON={
route:'<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8.2 18H13a4 4 0 004-4V8.2"/>',
cap:'<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/>',
exam:'<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>',
list:'<path d="M3.5 6.5l1.8 1.8 3.2-3.6M3.5 16.5l1.8 1.8 3.2-3.6M12 7h9M12 17h9"/>',
flag:'<path d="M5 21V4M5 4h13l-3 4 3 4H5"/>',
pin:'<path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
search:'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
bookmark:'<path d="M7 4h10v16l-5-3.5L7 20z"/>',back:'<path d="M14 6l-6 6 6 6"/>',
arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>',close:'<path d="M6 6l12 12M18 6L6 18"/>',check:'<path d="M5 12.5l4.5 4.5L19 7.5"/>'};
const I=(n,s=22)=>`<svg class="i" width="${s}" height="${s}" viewBox="0 0 24 24">${ICON[n]}</svg>`;
// Material 3 Expressive scalloped shape with n lobes
const shape=(n,cls='')=>{let p='';for(let i=0;i<96;i++){const t=i/96*Math.PI*2,r=50*(.89+.11*Math.cos(n*t));p+=(i?'L':'M')+(50+r*Math.cos(t)).toFixed(1)+' '+(50+r*Math.sin(t)).toFixed(1)}return `<svg class="${cls}" viewBox="0 0 100 100"><path d="${p}Z"/></svg>`};
const ring=(v,l='',cls='',col='var(--p)')=>`<div class="ring ${cls}"><svg viewBox="0 0 44 44"><circle class="tr" cx="22" cy="22" r="18"/><circle class="fg" cx="22" cy="22" r="18" pathLength="100" style="stroke:${col};stroke-dashoffset:${100-v}"/></svg><b>${v}</b>${l?`<span>${l}</span>`:''}</div>`;
const sig=v=>{const n=v>=75?3:v>=50?2:1;return `<svg class="sig" viewBox="0 0 14 14">${[0,1,2].map(i=>`<rect x="${i*5}" y="${9-i*4}" width="3.6" height="${5+i*4}" rx="1.2" class="${i<n?'f':''}"/>`).join('')}</svg>`};
const months=f=>`<div class="mo">${MN.map((m,i)=>`<i class="${f(i+1)?'f':''} ${i+1===NOW?'now':''}">${m[0]}</i>`).join('')}</div>`;
const cal=rows=>`<div class="cal">${rows.map(([l,f])=>`<span>${l}</span>${months(f)}`).join('')}</div>`;
const examCal=x=>cal([['Apply',m=>inWin(x.win[0],x.win[1],m)],['Exam',m=>m===x.em]]);
const empty=t=>`<div class="empty">${shape(6)}${t}</div>`;
const lrow=(a,v,t,s,kind)=>`<button class="lrow" data-a="${a}" data-v="${v}"><div><b>${t}</b><span>${s}</span></div><em>${kind}</em></button>`;
const segHTML=(list,v,a,cls='full')=>`<div class="seg ${cls}">${list.map(([k,n])=>`<button class="${k===v?'on':''}" data-a="${a}" data-v="${k}">${n}</button>`).join('')}</div>`;
const chipsHTML=(list,v,a)=>`<div class="chips">${list.map(k=>`<button class="chip ${k===v?'on':''}" data-a="${a}" data-v="${k}">${k}</button>`).join('')}</div>`;
const tabsHTML=(list,v)=>`<div class="tabs">${list.map(([k,n])=>`<button class="${k===v?'on':''}" data-a="tab" data-v="${k}">${n}</button>`).join('')}</div>`;
const facts=l=>`<div class="facts">${l.map(([a,b])=>`<div class="fact"><small>${a}</small><b>${b}</b></div>`).join('')}</div>`;
// stacked bar with a tappable legend
function split(parts,f=v=>v+'%'){const ps=parts.filter(p=>p[1]>0);
  return `<div class="split"><div class="sbar">${ps.map((p,i)=>`<button class="g${i%7}" style="flex:${p[1]}" data-a="seg" data-v="${i}" aria-label="${p[0]}"></button>`).join('')}</div><div class="sleg">${ps.map((p,i)=>`<button class="g${i%7}" data-a="seg" data-v="${i}"><i></i><span>${p[0]}</span><b>${f(p[1])}</b></button>`).join('')}</div></div>`}

/* ============ VIEWS ============ */
const stagesHTML=()=>`<div class="stages">${STAGES.map(s=>`<button class="stg ${s.id===S.stage?'on':''}" data-a="stage" data-v="${s.id}">${s.id===S.stage?s.t:s.n}</button>`).join('')}</div>`;
function visaHTML(c){const v=c.vz;if(!v)return'';const st=v[1],dn=st.filter((_,i)=>S.done.has('v'+c.k+':'+i)).length;
  return `<div class="vsa"><small><span>Visa steps · ${v[0]}</span><span>${dn}/${st.length}</span></small><ol class="vs">${st.map(([n,d,cost,mode,note],i)=>{const on=S.done.has('v'+c.k+':'+i);
    return `<li class="${on?'d':''}" style="--i:${i}"><button data-a="vstep" data-v="${c.k}:${i}" aria-label="${on?'Undo':'Done'}: ${n}">${on?I('check',16):i+1}</button><div><span>${n}</span><small>${[d?dy(d):'',cost,mode].filter(Boolean).join(' · ')}</small>${note?`<em>${note}</em>`:''}</div></li>`}).join('')}</ol></div>`}
function abList(){const mx=Math.max(60,...CT.map(c=>c.cost+c.live)),tot=c=>c.cost+c.live,bl=S.abmax/mx*100;
  return [...CT].sort((a,b)=>tot(a)-tot(b)).map(c=>{const T=tot(c),on=S.ab===c.k,ok=T<=S.abmax,pt=c.wage*c.work*4.3/1e5;
    return `<div role="button" tabindex="0" class="ab ${ok?'ok':'over'} ${on?'on':''}" data-a="ctry" data-v="${c.k}">
    <div class="abh"><span class="abc">${c.k}</span><div class="abn"><b>${c.n}</b><small>Tuition ${c.cost}L + living ${c.live}L</small></div><div class="abt"><b>NPR ${T}L</b><small>per year</small></div></div>
    <div class="abb"><i class="a" style="width:${c.cost/mx*100}%"></i><i class="b" style="width:${c.live/mx*100}%"></i><s style="left:${bl}%"></s></div>
    <div class="abp"><span class="pl">${ok?'Within budget':'NPR '+(T-S.abmax)+'L over budget'}</span><span>${c.visa>=0?'Visa approval '+c.visa+'%':''}</span></div>
    ${on?`<div class="abx"><div><small>Work allowed</small><b>${c.work>0?c.work+' h / week':c.work===0?'None':'See notes'}</b></div><div><small>Stay after study</small><b>${c.stay||'See notes'}</b></div>
      <div><small>Entry test</small><b>${c.test}</b></div><div class="w2"><small>Intake months</small>${c.intake.length?months(m=>c.intake.includes(m)):'<b>See the university</b>'}</div>
      ${visaHTML(c)}<div class="chips w w2">${c.tx?`<button class="chip" data-a="goExam" data-v="${c.tx}">${X[c.tx].n}</button>`:''}<button class="chip" data-a="skf" data-v="${c.k}">Scholarships</button></div></div>`:''}</div>`}).join('')}
const STUDY={
nepal(){const cs=Object.keys(C).filter(hasCol),c=C[S.cc],list=COL.filter(x=>x.c.includes(S.cc)),fs=list.map(x=>x.fees[S.cc]).filter(v=>v!=null),lo=fs.length?Math.floor(Math.min(...fs)):0,hi=fs.length?Math.max(lo+1,Math.ceil(Math.max(...fs))):0;if(S.cmax==null)S.cmax=hi;
  return `<div class="chips">${cs.map(id=>`<button class="chip ${id===S.cc?'on':''}" data-a="cc" data-v="${id}">${C[id].n}</button>`).join('')}</div>
  <div class="nm" id="nmap"></div>
  <div class="ctl">${hi?`<div class="sl"><input type="range" id="cmax" min="${lo}" max="${hi}" step="${hi-lo>20?1:.5}" value="${S.cmax}" aria-label="Maximum fee"><output id="cmaxv">${lakh(S.cmax)}</output></div>`:'<span></span>'}${segHTML([['fee','Fee'],['seats','Seats']],S.csort,'csort','')}</div>
  <div id="clist"></div>`},
abroad(){return `<div class="abin"><b>Your budget for one year</b><span>Tuition plus living costs</span>
    <div class="sl"><input type="range" id="abmax" min="5" max="60" step="5" value="${S.abmax}" aria-label="Yearly budget"><output id="abv">NPR ${S.abmax}L</output></div></div>
  <div class="abkey"><span><i class="a"></i>Tuition</span><span><i class="b"></i>Living</span><span><s></s>Your budget</span></div>
  <div id="ablist">${abList()}</div>`},
funding(){const left=s=>(s.e-NOW+12)%12;
  const l=SCH.filter(s=>(S.stype==='All'||s.t===S.stype)&&(S.slvl==='All'||s.l.includes(S.slvl[0]))&&(!S.sk||s.k===S.sk)).sort((a,b)=>(inWin(b.s,b.e,NOW)-inWin(a.s,a.e,NOW))||left(a)-left(b));
  return `<div class="chips">${S.sk?`<button class="chip on" data-a="skf" data-v="">${S.sk}${I('close',14)}</button>`:''}${['All',...new Set(SCH.map(s=>s.t))].map(t=>`<button class="chip ${S.stype===t?'on':''}" data-a="stype" data-v="${t}">${t}</button>`).join('')}</div>
  ${segHTML(['All','Bachelor','Master','PhD'].map(t=>[t,t]),S.slvl,'slvl')}
  ${l.map(s=>{const o=inWin(s.s,s.e,NOW),key='sch:'+s.n;return `<div role="button" tabindex="0" class="srow ${o?'open':''}" data-a="sch" data-v="${s.n}"><div class="sh"><b>${s.n}</b><span class="cd">${s.k}</span><em>${s.fixed?'Check notice':o?'Closes '+MN[s.e-1]:'Opens '+MN[s.s-1]}</em></div>${s.fixed?'':months(m=>inWin(s.s,s.e,m))}
    ${S.schOpen===s.n?`<div class="sx"><div class="chips w z">${[['T','Tuition'],['S','Stipend'],['F','Flights']].map(([k,n])=>`<span class="skill ${s.cov.includes(k)?'yes':'no'}">${n}</span>`).join('')}</div>
    ${s.who?`<p class="mk-n">${s.who}</p>`:''}<div class="sxa"><b>${s.aw?s.aw+' awards':'Open call'}</b><button class="ib ${S.saved.has(key)?'on':''}" data-a="save" data-v="${key}" aria-label="Save">${I('bookmark')}</button>${s.link?`<a class="btn t" href="${s.link}" target="_blank" rel="noopener">Website</a>`:''}</div></div>`:''}</div>`}).join('')||empty('No match')}`}
};
const xst=x=>{const w=why(x);
  if(w)return{k:'no',t:'Not eligible',s:w,o:100};
  if(x.win[0]===1&&x.win[1]===12)return{k:'open',t:'Open all year',s:'Book any month',o:0};
  if(inWin(x.win[0],x.win[1],NOW))return{k:'open',t:'Open now',s:'Closes '+MN[x.win[1]-1],o:1};
  const n=(x.win[0]-NOW+12)%12;return{k:'soon',t:n<=2?'Opens soon':'Opens '+MN[x.win[0]-1],s:'In '+n+(n===1?' month':' months'),o:1+n}};
const xsc=x=>x.seats?Math.max(.06,Math.min(1,(Math.log10(x.seats/x.apps)+3)/3)):0;
const xpm=Math.max(...Object.values(X).map(x=>x.prep));
const xnext=l=>{const ok=l.filter(e=>e.st.k!=='no'),op=ok.filter(e=>e.st.k==='open'&&e.st.o===1).sort((a,b)=>(a.x.win[1]-NOW+12)%12-(b.x.win[1]-NOW+12)%12),e=op[0]||ok.find(o=>o.st.o>=1)||ok[0];
  if(!e)return '';const {x,st}=e,od=x.seats?oddsOf(x).txt:'';
  return `<button class="xnext" data-a="exam" data-v="${x.id}"><small>${op[0]?'Closing next':'Opens next'}</small><b>${x.n}</b><span>${x.b}</span>${months(m=>inWin(x.win[0],x.win[1],m))}
  <div class="xnf"><i>${st.t}</i><i>${npr(x.fee)}</i>${x.em?`<i>Exam ${MN[x.em-1]}</i>`:''}${od?`<i>${od}</i>`:''}</div></button>`};
const xyear=l=>{const el=l.filter(e=>e.st.k!=='no'),cnt=MN.map((_,i)=>el.filter(e=>inWin(e.x.win[0],e.x.win[1],i+1)).length),mx=Math.max(1,...cnt);
  return `<div class="xy"><small>Applications open each month</small><div class="xyb">${cnt.map((n,i)=>`<div class="${i+1===NOW?'now':''}"><i style="height:${Math.max(8,n/mx*100)}%"><u>${n}</u></i><span>${MN[i][0]}</span></div>`).join('')}</div></div>`};
const xb=(t,v,txt)=>`<div class="xb"><span>${t}</span><div><i style="width:${Math.round(v*100)}%"></i></div><b>${txt}</b></div>`;
const xlistHTML=()=>{const all=Object.values(X).filter(x=>x.g===S.xg).map(x=>({x,st:xst(x)})),
  n=k=>all.filter(e=>e.st.k===k).length,srt={soon:(a,b)=>a.st.o-b.st.o,odds:(a,b)=>(xsc(b.x)||.5)-(xsc(a.x)||.5),fee:(a,b)=>a.x.fee-b.x.fee}[S.xs],
  l=all.filter(e=>S.xf==='all'||e.st.k===S.xf).sort(srt),sm=(k,c,t)=>`<button class="${c} ${S.xf===k?'on':''}" data-a="xf" data-v="${k}"><b>${n(k)}</b><small>${t}</small></button>`;
  return xnext(all.slice().sort((a,b)=>a.st.o-b.st.o))+xyear(all)+
  `<div class="xsum">${sm('open','g','Open now')}${sm('soon','y','Coming up')}${sm('no','','Not eligible')}</div>`+
  segHTML([['soon','Soonest'],['odds','Best odds'],['fee','Lowest fee']],S.xs,'xs','xs')+
  (l.map(({x,st})=>`<button class="xc ${wide()&&S.exam===x.id?'on':''} ${st.k==='no'?'no':''}" data-a="exam" data-v="${x.id}"><div class="xh"><div><b>${x.n}</b><span>${x.b}</span></div><span class="pill ${st.k}">${st.t}</span></div>
  ${st.k==='no'?`<div class="xm"><span>${st.s}</span></div>`:months(m=>inWin(x.win[0],x.win[1],m))}
  ${st.k==='no'?'':`<div class="xbs">${x.seats?xb('Odds',xsc(x),oddsOf(x).txt):''}${xb('Prep',x.prep/xpm,x.prep+' h')}</div>`}
  <div class="xm"><span>${st.k==='no'?'Fee':st.s+' ·'} ${npr(x.fee)}</span>${x.em?`<span>Exam ${MN[x.em-1]}</span>`:''}${x.pay?`<span>Starts NPR ${x.pay}k</span>`:''}${x.seats?`<span>${fmt(x.seats)} seats</span>`:''}</div></button>`).join('')||empty('Nothing here'))};
/* ============ QUESTIONS ============ */
const FQ=DATA.faq,FQT=DATA.faqTopics,FQI=DATA.faqIcons;
const fqk=f=>{const c=f.r[0]&&C[f.r[0][1]];if(!c)return[];return[c.y?[yr(c.y),'Duration']:null,c.fee[1]?[lakh(c.fee[0]||c.fee[1]),c.fee[0]?'Fee from':'Fee up to']:null,c.pay?['NPR '+c.pay[0]+'k','Start pay']:null].filter(Boolean).slice(0,3)};
const lk=t=>t.replace(/(https?:\/\/[^\s<,]+[^\s<,.)]|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:gov|edu|org|com)\.np\b|\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b|\b0\d{1,2}-\d{6,7}\b|\b1660-\d{2}-\d{5}\b)/gi,m=>{const h=/^https?:/i.test(m)?m:m.includes('@')?'mailto:'+m:/^[\d-]+$/.test(m)?'tel:'+m.replace(/-/g,''):'https://'+m;return `<a href="${h}" target="_blank" rel="noopener">${m.replace(/^https?:\/\/(www\.)?/,'')}</a>`});
const fqCard=(f,i)=>`<div class="fq ${S.fqo===f.id?'open':''}" style="--i:${Math.min(i,10)}"><button class="fqh" data-a="fqo" data-v="${f.id}" aria-expanded="${S.fqo===f.id}"><u>${I(FQI[f.t]||'list',22)}</u><div><b>${f.q}</b><span>${f.t} · ${Math.max(1,Math.round(f.a.split(' ').length/40))} min read</span></div><i class="chv">${I('arrow',20)}</i></button>
  <div class="fqb"><div><div class="fqa"><p>${lk(f.a)}</p><div class="fqk">${fqk(f).map(([v,l])=>`<div><b>${v}</b><small>${l}</small></div>`).join('')}</div>
  <div class="chips w z">${f.r.map(([a,v,n])=>`<button class="chip" data-a="${a}" data-v="${v}">${n}</button>`).join('')}</div>
  <div class="fqx"><button class="btn t sm ${S.fqh.has(f.id)?'on':''}" data-a="fqh" data-v="${f.id}">${I('check',18)}<span>Helpful</span></button><span class="sp"></span><button class="ib ${S.saved.has('faq:'+f.id)?'on':''}" data-a="save" data-v="faq:${f.id}" aria-label="Save">${I('bookmark')}</button></div></div></div></div></div>`;
const faqList=()=>{const q=S.fqs.toLowerCase(),l=FQ.filter(f=>(S.fqt==='All'||f.t===S.fqt)&&(!q||(f.q+' '+f.a).toLowerCase().includes(q)));return l.map(fqCard).join('')||empty('No questions found')};
const faqView=()=>`<div class="fqs"><input id="fqq" placeholder="Search questions" value="${S.fqs}" autocomplete="off" aria-label="Search questions">${I('search',20)}</div>${chipsHTML(['All',...FQT],S.fqt,'fqt')}<div id="fqlist">${faqList()}</div>`;
const V={
explore(){const st=stage(),sm=stream(),cs=sm.courses,ks=[...new Set(cs.flatMap(id=>C[id].to))];
  return `<div class="wrap">${stagesHTML()}
  <div class="grp">${st.streams.map(x=>`<button class="gb t-${x.tone} ${x.id===sm.id?'on':''}" data-a="stream" data-v="${x.id}">${x.n}</button>`).join('')}</div>
  <div class="lens"><button class="lk" id="lk" data-a="foc"></button><span class="lg">${[['d','Demand'],['pay','Pay'],['ease','Odds']].map(([k,n])=>`<button class="lz ${S.lens===k?'on':''}" data-a="lens" data-v="${k}">${n}</button>`).join('')}</span></div>
  <div class="flow" id="flow"><svg id="links"></svg>
    <div class="col">${cs.map((id,i)=>`<button class="nd c" style="--i:${i}" data-a="course" data-v="${id}"><i class="fl"></i><span>${C[id].n}</span><small></small></button>`).join('')}</div>
    <div class="col">${ks.map((id,i)=>`<button class="nd k" style="--i:${i+3}" data-a="career" data-v="${id}"><i class="fl"></i>${sig(K[id].d)}<span>${K[id].n}</span><small></small></button>`).join('')}</div>
  </div></div>`},
study(){return `<div class="wrap pad">${segHTML([['nepal','Colleges'],['abroad','Abroad'],['funding','Funding']],S.study,'study')}${STUDY[S.study]()}</div>`},
exams(){const gt=TR.filter(t=>t[3]===grOf(S.xg));return `<div class="wrap pad">${XGR.length>1?segHTML(XGR,grOf(S.xg),'xgr'):''}${gt.length>1?`<div class="chips">${gt.map(t=>`<button class="chip ${t[0]===S.xg?'on':''}" data-a="xg" data-v="${t[0]}">${t[1]}</button>`).join('')}</div>`:''}
  <div class="xp"><small>Eligibility is checked against your profile</small><div class="chips">${[1,2,3,4].map(i=>`<button class="chip ${S.edu===i?'on':''}" data-a="edu" data-v="${i}">${EDU[i]}</button>`).join('')}</div>
  <div class="ctl"><div class="sl"><input type="range" id="age" min="14" max="45" value="${S.age}" aria-label="Age"><output id="agev">Age ${S.age}</output></div>${Object.values(X).some(x=>x.g===S.xg&&x.age&&x.age[2]>x.age[1])?segHTML([['1','Woman'],['0','Man']],S.woman,'woman',''):''}</div></div>
  <div id="xlist">${xlistHTML()}</div></div>`},
guides(){const l=Object.values(G).filter(g=>S.gcat==='All'||g.cat===S.gcat),top=segHTML([['guides','Guides'],['faq','Questions']],S.gv,'gv');
  if(S.gv==='faq')return `<div class="wrap pad">${top}${faqView()}</div>`;
  return `<div class="wrap pad">${top}${chipsHTML(DATA.cats,S.gcat,'gcat')}
  <div class="ggrid">${l.map(g=>{const n=g.steps.length;return `<button class="gd t-${(GT[g.cat]||'sc')} ${wide()&&S.guide===g.id?'on':''}" data-a="guide" data-v="${g.id}"><b>${g.n}</b><div class="gp"><i style="width:${gdone(g)/n*100}%"></i></div><div class="gm"><span>${n} steps</span><span>${dy(gsum(g,1))}</span></div></button>`}).join('')}</div></div>`},
plan(){if(S.plan==='match'&&S.mq)return qHTML();
  return `<div class="wrap pad">${segHTML([['match','Match'],['plan','My plan']],S.plan,'plan')}${S.plan==='plan'?
  `<p class="mad">I am <output id="pagev">${S.age}</output></p><input type="range" id="page" min="13" max="40" value="${S.age}" aria-label="Age"><div id="pout">${planOut()}</div>`:
  `<div id="mres"></div>`}</div>`}
};
// the plan assembles itself from the route chosen in Explore plus everything saved
const route=()=>{const ids=S.path.map(p=>p.course);if(S.course)ids.push(S.course);return ids.map(id=>C[id])};
function deadlines(){const m=new Map(),add=(key,n,s,e,a,v)=>{if(!(s===1&&e===12))m.set(key,{n,s,e,a,v})};
  route().forEach(c=>{const x=X[CX[c.id]];if(x)add('exam:'+x.id,x.n,x.win[0],x.win[1],'goExam',x.id)});
  S.saved.forEach(k=>{const i=k.indexOf(':'),t=k.slice(0,i),id=k.slice(i+1);
    if(t==='exam'&&X[id])add(k,X[id].n,X[id].win[0],X[id].win[1],'goExam',id);
    if(t==='sch'){const s=SCH.find(s=>s.n===id);if(s)add(k,s.n,s.s,s.e,'goSch',s.n)}});
  const until=d=>inWin(d.s,d.e,NOW)?-1:(d.s-NOW+12)%12;return [...m.values()].sort((a,b)=>until(a)-until(b))}
function planOut(){const r=route(),h=[];
  if(r.length&&r[r.length-1].to.length){const last=r[r.length-1],k=K[S.career&&last.to.includes(S.career)?S.career:last.to[0]],yrs=r.reduce((a,c)=>a+c.y,0),lo=r.reduce((a,c)=>a+c.fee[0],0),hi=r.reduce((a,c)=>a+c.fee[1],0),end=Math.ceil(S.age+yrs);
    h.push(`<div class="hl t-pc"><b>${k.n} at ${end}</b><div class="tl">${r.map(c=>`<div style="flex:${c.y}"><span>${c.n}</span><small>${yr(c.y)}</small></div>`).join('')}<div class="end">${end}</div></div>${facts([['Years',fmt(yrs)],['Cost, NPR',fmt(lo)+'–'+fmt(hi)+'L'],['First pay','NPR '+k.pay[0]+'k']])}</div>`)}
  const dl=deadlines();
  if(dl.length)h.push('<h4>Deadlines</h4>'+dl.map(d=>{const o=inWin(d.s,d.e,NOW);return `<div role="button" tabindex="0" class="srow ${o?'open':''}" data-a="${d.a}" data-v="${d.v}"><div class="sh"><b>${d.n}</b><em>${o?'Closes '+MN[d.e-1]:'Opens '+MN[d.s-1]}</em></div>${months(m=>inWin(d.s,d.e,m))}</div>`}).join(''));
  const gs=Object.values(G).filter(g=>S.saved.has('guide:'+g.id)||gdone(g));
  if(gs.length)h.push('<h4>Guides</h4>'+gs.map(g=>`<button class="row" data-a="goGuide" data-v="${g.id}"><b>${g.n}</b><em>${gdone(g)} of ${g.steps.length}</em><div class="rb still"><i style="left:0;width:${gdone(g)/g.steps.length*100}%"></i></div></button>`).join(''));
  const sv=[...S.saved].map(k=>{const i=k.indexOf(':'),t=k.slice(0,i),id=k.slice(i+1);return t==='course'&&C[id]?lrow('goCourse',id,C[id].n,C[id].f,'Course'):t==='career'&&K[id]?lrow('goCareer',id,K[id].n,payTxt(K[id].pay),'Career'):''}).join('');
  if(sv)h.push('<h4>Saved</h4>'+sv);
  return h.join('')||empty('Nothing planned')+`<button class="btn f" style="width:100%" data-a="nav" data-v="explore">Explore</button>`}
function vSearch(){const q=S.q.toLowerCase(),r=[],hit=s=>s.toLowerCase().includes(q);
  for(const id in C)if(hit(C[id].n+' '+C[id].f))r.push(lrow('goCourse',id,C[id].n,C[id].f,'Course'));
  for(const id in K)if(hit(K[id].n))r.push(lrow('goCareer',id,K[id].n,payTxt(K[id].pay),'Career'));
  for(const id in X)if(hit(X[id].n+' '+X[id].b))r.push(lrow('goExam',id,X[id].n,X[id].b,'Exam'));
  for(const id in G)if(hit(G[id].n))r.push(lrow('goGuide',id,G[id].n,G[id].cat,'Guide'));
  COL.forEach(x=>{if(x.c.length&&hit(x.n+' '+x.d))r.push(lrow('find',x.c[0],x.n,x.d,'College'))});
  SCH.forEach(s=>{if(hit(s.n))r.push(lrow('goSch',s.n,s.n,s.t,'Scholarship'))});
  return `<div class="wrap pad">${r.slice(0,40).join('')||empty('No results')}</div>`}

/* ============ SHEETS ============ */
function heroHTML(tone,key,badge,title,sub){return `<header class="hero t-${tone}"><div class="hr"><button class="ib x" data-a="close" aria-label="Back">${I('back')}</button><button class="ib ${S.saved.has(key)?'on':''}" data-a="save" data-v="${key}" aria-label="Save">${I('bookmark')}</button></div>
  <h2>${title}</h2><div class="badge">${badge}</div><p>${sub}</p></header>`}
function costOut(c){const t=c.fee[+S.cpriv]*(1-S.aid/100),l=[0,18,12][+S.live]*12*c.y/100,b=.15*c.y,tot=t+l+b,avg=c.pay?(c.pay[0]+c.pay[1])/2:0;
  return `<div class="big"><b>${lakh(tot)}</b>${avg?`<span>${Math.round(tot*100/avg)} months of starting pay</span>`:''}</div><div style="margin-top:16px">${split([['Tuition',t],['Living',l],['Books',b]],lakh)}</div>`}
function prepOut(x){const days=Math.ceil(x.prep/S.hrs),mb=Math.ceil(days/30),tot=x.syl.reduce((a,p)=>a+p[1],0),mx=Math.max(...x.syl.map(p=>p[1]));
  return `<div class="big"><b>${dy(days)}</b>${x.em?`<span>Start by ${MN[((x.em-1-mb)%12+12)%12]}</span>`:''}</div><h4>Hours a week</h4>${x.syl.map(([t,w])=>`<div class="row"><b>${t}</b><em>${fmt(S.hrs*7*w/tot)} h</em><div class="rb still"><i style="left:0;width:${w/mx*100}%"></i></div></div>`).join('')}`}
function waffle(x){const o=oddsOf(x),one=o.r>=20,n=one?Math.min(o.n,400):100,m=Math.floor(n*.37);
  return `<div class="waf">${[...Array(n)].map((_,i)=>`<i class="${one?(i===m?'me one':''):(i<o.n?'me':'')}"></i>`).join('')}</div>`}
function radar(k){const ax=['Pay','Demand','Entry','Stability','Flexibility','Growth'];
  const pt=(v,i,R=84)=>{const a=(i*60-90)*Math.PI/180,r=R*v/100;return[(160+r*Math.cos(a)).toFixed(1),(118+r*Math.sin(a)).toFixed(1)]};
  const poly=vs=>vs.map((v,i)=>pt(v,i).join(',')).join(' ');
  return `<svg class="radar" viewBox="0 0 320 236">${[33,66,100].map(g=>`<polygon points="${poly(Array(6).fill(g))}" fill="none" stroke="var(--ol)"/>`).join('')}
  <polygon points="${poly(AVG)}" fill="var(--s3)"/><polygon points="${poly(rv(k))}" fill="var(--p)" fill-opacity=".22" stroke="var(--p)" stroke-width="2.5" stroke-linejoin="round"/>
  ${ax.map((t,i)=>{const [x,y]=pt(100,i,102);return `<text x="${x}" y="${+y+4}" text-anchor="${i%3===0?'middle':i<3?'start':'end'}">${t}</text>`}).join('')}
  <circle cx="14" cy="12" r="5" fill="var(--s3)"/><text x="24" y="16">Average</text></svg>`}
function odds(o){return o.d-o.c}
function market(k,id){
  const me=K[id]||k,g=odds(me),all=Object.values(K).sort((a,b)=>odds(b)-odds(a)),rank=all.findIndex(o=>o.id===me.id)+1,n=all.length;
  const v=g>=30?['Great odds','Lots of jobs, few rivals','g']:g>=10?['Good odds','More jobs than rivals','g']:g>=-10?['Competitive','Jobs and rivals are about equal','y']:['Tough to enter','Many more rivals than jobs','r'];
  const lo=Math.max(0,Math.min(n-5,rank-3)),win=all.slice(lo,lo+5);
  const bar=(l,s,val,cls)=>`<div class="mk-b"><span>${l}</span><div class="mk-t"><i class="${cls}" style="width:${val}%"></i></div><b>${val}</b></div>`;
  return `<div class="mk"><div class="mk-v t-${v[2]}c"><b>${v[0]}</b><span>${v[1]}</span><em>#${rank} of ${n} careers</em></div>
  ${bar('Jobs available','',me.d,'a')}${bar('People competing','',me.c,'b')}
  <h5>Easiest careers to get into</h5>
  ${win.map(o=>`<button class="mk-r ${o.id===me.id?'me':''}" data-a="goCareer" data-v="${o.id}"><u>${all.indexOf(o)+1}</u><span>${o.n}</span><div class="mk-g"><i style="width:${Math.max(6,Math.min(100,Math.round((odds(o)+50)/110*100)))}%"></i></div></button>`).join('')}
  <p class="mk-n">Bar length shows jobs minus competition. Longer means easier to get a job.</p></div>`}
function spark(k){const v=k.hist&&k.hist.length>=2?k.hist.map(a=>Math.max(5,Math.min(99,a))):[0,1,2,3,4,5].map(i=>Math.max(5,Math.min(99,k.d-k.f.tr*(5-i))));
  const lo=Math.min(...v)-8,hi=Math.max(...v)+8,px=i=>16+i*288/(v.length-1),py=a=>78-(a-lo)/(hi-lo)*60,d=v.map((a,i)=>(i?'L':'M')+px(i).toFixed(0)+' '+py(a).toFixed(1)).join('');
  return `<svg class="plot" viewBox="0 0 320 104"><path d="${d}L304 92L16 92Z" fill="var(--pc)"/><path d="${d}" fill="none" stroke="var(--p)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><circle class="me" cx="304" cy="${py(v[v.length-1]).toFixed(1)}" r="6"/><text x="16" y="102">${YEAR-5}</text><text x="304" y="102" text-anchor="end">${YEAR}</text></svg>`}
const PANEL={
course(id){const c=C[id],{st,sm}=locate(id),t=S.tabs.course;
  if(t==='journey')return `<div class="steps">${c.plan.map((p,i)=>`<div class="step" style="--i:${i}"><b>${i+1}</b><span>${p}</span></div>`).join('')}</div>`;
  if(t==='careers')return c.to.map(k=>{const o=K[k];return `<button class="row" data-a="goCareer" data-v="${k}"><b>${o.n}</b><em>${o.pay[0]}–${o.pay[2]}k</em><div class="rb"><i style="left:${o.pay[0]*100/PMAX}%;width:${Math.max(2,(o.pay[2]-o.pay[0])*100/PMAX)}%"></i></div></button>`}).join('');
  if(t==='cost')return `${segHTML([['0','Public'],['1','Private']],S.cpriv,'cpriv')}${segHTML([['0','Home'],['1','Hostel'],['2','Room']],S.live,'live')}
    <div class="sl"><input type="range" id="aid" min="0" max="100" step="10" value="${S.aid}" aria-label="Scholarship"><output id="aidv">Aid ${S.aid}%</output></div><div id="costout">${costOut(c)}</div>`;
  if(t==='entry'){const x=X[CX[id]];return `<div class="tiles">${x?`<button class="tile lk" data-a="goExam" data-v="${x.id}"><div><small>Entrance</small><b>${c.ent}</b></div>${I('arrow',20)}</button>`:`<div class="tile"><small>Entrance</small><b>${c.ent}</b></div>`}
    <div class="tile"><small>Needs</small><b>${st.need}${st.id==='p2'?' '+sm.n:''}</b></div><div class="tile"><small>Duration</small><b>${yr(c.y)}</b></div></div>${x&&x.em?`<div style="margin-top:18px">${examCal(x)}</div>`:''}`}
  const sib=st.streams.flatMap(x=>x.courses).filter(x=>x!==id);if(!sib.length)return empty('Nothing to compare');
  const b=sib.includes(S.cmp)?S.cmp:sib[0],B=C[b],av=a=>a?(a[0]+a[1])/2:0;
  const rows=[['Demand',c.d,B.d,''],['Competition',c.c,B.c,''],['Start pay',av(c.pay),av(B.pay),'k'],['Fee',av(c.fee),av(B.fee),'L'],['Years',c.y,B.y,'']];
  return `<div class="chips">${sib.map(x=>`<button class="chip ${x===b?'on':''}" data-a="cmp" data-v="${x}">${C[x].n}</button>`).join('')}</div>
  <div class="bf"><div class="bfh"><b>${c.n}</b><b>${B.n}</b></div>${rows.map(([l,a,v,u])=>{const m=Math.max(a,v)||1;return `<div class="bfr"><span>${fmt(a)}${u}</span><div class="ba"><i style="width:${a/m*100}%"></i></div><em>${l}</em><div class="bb"><i style="width:${v/m*100}%"></i></div><span class="vb">${fmt(v)}${u}</span></div>`}).join('')}</div>`},
career(id){const k=K[id],t=S.tabs.career;
  if(t==='pay'){const max=k.pay[2],st=[0,3,7,12],yrs=['Year 0–2','Year 3–6','Year 7–11','Year 12+'];
    return `<h4>How your monthly pay grows</h4><div class="lad">${k.f.lad.map((n,i)=>{const v=Math.round(payAt(k,st[i]));return `<button class="lr" data-a="rung" data-v="${st[i]}"><u>${i+1}</u><div><b>${n}</b><small>${yrs[i]}</small></div><em>NPR ${v}k</em><div class="lb"><i style="width:${v/max*100}%"></i></div></button>`}).join('')}</div>
    <div class="exr"><label for="exp">Try a year</label><input type="range" id="exp" min="0" max="12" value="${S.exp}" aria-label="Years of experience"><output id="expo">Year ${S.exp}</output></div>
    <p class="mk-n">Monthly salary before tax, in thousands of rupees. Tap a step or drag the slider.</p>`}
  if(t==='profile')return `${k.f.hasT?radar(k):''}${k.f.day.length?`<h4>A ${k.f.hrs||40}-hour week</h4>${split(k.f.day)}`:''}${!k.f.hasT&&!k.f.day.length?empty('Profile details are not ready for this career'):''}`;
  if(t==='skills'){const have=k.sk.filter(s=>S.have.has(s)).length,routes=Object.keys(C).filter(c=>C[c].to.includes(id));
    return `<div class="rdy" id="rdy">${ring(Math.round(have/k.sk.length*100),'Ready','still')}<div class="chips w z">${k.sk.map(s=>`<button class="chip ${S.have.has(s)?'on':''}" data-a="have" data-v="${s}">${s}</button>`).join('')}</div></div>
    ${k.lic&&(k.lx||G.lic)?`<h4>Licence</h4>`+lrow(k.lx?'goExam':'goGuide',k.lx||'lic',k.lic,k.lx?X[k.lx].b:'Council registration',k.lx?'Exam':'Guide'):''}
    <h4>Routes in</h4><div class="chips w z">${routes.map(c=>`<button class="chip" data-a="goCourse" data-v="${c}">${C[c].n}</button>`).join('')}</div>`}
  return `<h4>Demand, 5 years</h4>${spark(k)}<h4>Your chances</h4>${market(k,id)}
  ${k.f.wh.length?'<h4>Where the jobs are</h4>'+split(k.f.wh):''}${k.f.emp.length?`<h4>Employers</h4><div class="chips w z">${k.f.emp.map(s=>`<span class="skill">${s}</span>`).join('')}</div>`:''}`},
exam(id){const x=X[id],t=S.tabs.exam;
  if(t==='stages'){const cs=Object.keys(CX).filter(c=>CX[c]===id);
    return `<div class="steps">${x.st.map(([n,m,f],i)=>`<div class="step" style="--i:${i}"><b>${i+1}</b><span>${n}<small>${f}</small></span><em>${+m?m:'Pass'}</em></div>`).join('')}</div>${cs.length?`<h4>Leads to</h4><div class="chips w z">${cs.map(c=>`<button class="chip" data-a="goCourse" data-v="${c}">${C[c].n}</button>`).join('')}</div>`:''}`}
  if(t==='syllabus')return split(x.syl);
  if(t==='odds')return `<p class="mad">${oddsOf(x).txt}</p>${waffle(x)}${x.quota?`<h4>Seats by category</h4>${split(x.quota)}`:''}`;
  if(t==='prepare')return `<p class="mad"><output id="hrv">${S.hrs}</output> h a day</p><input type="range" id="hrs" min="1" max="10" value="${S.hrs}" aria-label="Hours a day"><div id="prepout">${prepOut(x)}</div>`;
  return x.ladder.map((r,i)=>`<div class="rung ${i===x.rung?'on':i<x.rung?'dim':''}" style="--w:${Math.min(100,Math.round(55+i*45/Math.max(1,x.ladder.length-1)))}%"><span>${r[0]}</span><b>NPR ${r[1]}k</b></div>`).reverse().join('')}
};
const SHEET={
course(id){const c=C[id],{st,sm}=locate(id),nx=STAGES[STAGES.indexOf(st)+1],[yn,yu]=yr(c.y).split(' ');
  return heroHTML(sm.tone,'course:'+id,`${shape(8,'spin')}<div><b>${yn}</b><small>${yu}</small></div>`,c.n,c.f)+
  `<div class="meters">${ring(c.d,'Demand')}${ring(c.c,'Competition','','var(--on)')}${c.pay?`<div class="pay"><b>${c.pay[0]}–${c.pay[1]}k</b><span>NPR / month to start</span></div>`:'<span></span>'}</div>
  ${tabsHTML([['journey','Journey'],['careers','Careers'],['cost','Cost'],['entry','Entry'],['compare','Compare']],S.tabs.course)}<div id="tabp">${PANEL.course(id)}</div>
  <div class="acts">${hasCol(id)?`<button class="btn f" data-a="find" data-v="${id}">${I('pin',18)}Colleges</button>`:''}${nx?`<button class="btn t" data-a="next" data-v="${id}">${nx.t}${I('arrow',18)}</button>`:''}</div>`},
career(id){const k=K[id];
  return heroHTML('sc','career:'+id,`${shape(5,'spin')}<div>${sig(k.d)}</div>`,k.n,payTxt(k.pay))+
  `<div class="meters">${ring(k.d,'Demand')}${ring(k.c,'Competition','','var(--on)')}<div class="pay"><b id="expv"></b><span id="expl"></span></div></div>
  ${tabsHTML([['pay','Pay'],['profile','Profile'],['skills','Skills'],['market','Market']],S.tabs.career)}<div id="tabp">${PANEL.career(id)}</div>`},
exam(id){const x=X[id],o=x.seats?oddsOf(x):null,tabs=[['stages','Stages'],['syllabus','Syllabus']],f=[];
  if(o)tabs.push(['odds','Odds']);tabs.push(['prepare','Prepare']);if(x.rung!=null)tabs.push(['ladder','Ladder']);
  if(!tabs.some(t=>t[0]===S.tabs.exam))S.tabs.exam='stages';
  if(o)f.push(['Seats',num(x.seats)],['Applicants',num(x.apps)]);f.push(['Fee',npr(x.fee)],['Needs',EDU[x.edu]]);
  if(x.age)f.push(['Age',x.age[0]+'–'+x.age[1]+(x.age[2]>x.age[1]?', women '+x.age[2]:'')]);if(x.pay)f.push(['Starting pay','NPR '+x.pay+'k']);if(x.valid)f.push(['Valid',x.valid+' yr']);
  return heroHTML((TR.find(t=>t[0]===x.g)||[0,0,'sc'])[2],'exam:'+id,`${shape(7,'spin')}<div>${o?`${o.pre?`<small>${o.pre}</small>`:''}<b>${o.n}</b>${o.post?`<small>${o.post}</small>`:''}`:`<b>${x.st.length}</b><small>parts</small>`}</div>`,x.n,x.b)+
  facts(f)+(x.em?`<div class="blk">${examCal(x)}</div>`:'')+tabsHTML(tabs,S.tabs.exam)+`<div id="tabp">${PANEL.exam(id)}</div>`+
  (x.guide||x.k?`<div class="acts">${x.guide?`<button class="btn f" data-a="goGuide" data-v="${x.guide}">${I('list',18)}Steps</button>`:''}${x.k?`<button class="btn t" data-a="goCareer" data-v="${x.k}">${K[x.k].n}${I('arrow',18)}</button>`:''}</div>`:'')},
guide(id){const g=G[id],n=g.steps.length,d=gdone(g);
  return heroHTML((GT[g.cat]||'sc'),'guide:'+id,`${shape(6,'spin')}<div><b id="gdone">${d}</b><small>of ${n}</small></div>`,g.n,g.cat)+
  facts([['Time',dy(gsum(g,1))],['Cost','NPR '+num(gsum(g,2))],['Online',g.steps.filter(s=>s[3]==='O').length+' of '+n]])+
  `<div class="blk"><div class="gp lg"><i id="gbar" style="width:${d/n*100}%"></i></div></div>
  <div class="blk"><div class="steps">${g.steps.map(([t,ds,c,w],i)=>`<button class="step ck ${S.done.has(id+':'+i)?'done':''}" style="--i:${i}" data-a="step" data-v="${id}:${i}"><b><i>${i+1}</i>${I('check',18)}</b><span>${t}<small>${[ds?dy(ds):'',c?npr(c):'',w==='O'?'Online':'In person'].filter(Boolean).join(' · ')}</small></span></button>`).join('')}</div></div>
  <div class="blk"><h4>Documents</h4><div class="chips w z">${g.docs.map(x=>`<button class="chip ${S.docs.has(id+':'+x)?'on':''}" data-a="doc" data-v="${id}:${x}">${x}</button>`).join('')}</div></div>
  ${g.link?`<div class="acts"><button class="btn t" data-a="${g.link[0]}" data-v="${g.link[1]}">${g.link[2]}${I('arrow',18)}</button></div>`:''}`}
};
function updExp(){const c=cur();if(!c||c.t!=='career'||!$('#expv'))return;const k=K[c.id],v=payAt(k,S.exp),ri=S.exp<3?0:S.exp<7?1:S.exp<12?2:3;
  $('#expv').textContent='NPR '+Math.round(v)+'k';$('#expl').textContent=(S.exp?'Year '+S.exp:'Entry')+' · '+k.f.lad[ri];
  const r=$('#exp'),o=$('#expo');if(o)o.textContent=S.exp?'Year '+S.exp:'Entry';
  if(r&&+r.value!==S.exp)r.value=S.exp;$$('.lr').forEach((b,i)=>b.classList.toggle('on',i===ri))}

/* ============ RENDER ============ */
function renderTop(){const tr=[];
  S.path.forEach((p,i)=>tr.push(`<button class="tc" data-a="trail" data-v="${i}">${C[p.course].n}</button>`));
  tr.push(`<button class="tc" data-a="home">${stage().t}</button>`);
  if(S.course)tr.push(`<button class="tc on" data-a="goCourse" data-v="${S.course}">${C[S.course].n}</button>`);
  if(S.career)tr.push(`<button class="tc on" data-a="goCareer" data-v="${S.career}">${K[S.career].n}</button>`);
  $('#pw-top').innerHTML=`<div class="tbar">${S.searching?`<input id="q" placeholder="Search" autocomplete="off" aria-label="Search">`:`<div class="brand">Pathways</div>`}
    <button class="ib ${S.searching?'on':''}" data-a="search" aria-label="Search">${I(S.searching?'close':'search')}</button></div>
    ${S.view==='explore'&&!S.searching?`<div class="trail">${tr.join('<i class="sep"></i>')}</div>`:''}`}
function renderMain(){const m=$('#pw-main'),over=S.searching&&S.q,key=[over?S.q&&'q':'',S.mq,S.gv,S.view,S.stage,S.stream,S.dev,S.study,S.xg,S.plan,S.gcat].join('|');
  if(key!==lastKey){m.classList.add('fresh');m.scrollTop=0;clearTimeout(freshT);freshT=setTimeout(()=>m.classList.remove('fresh'),900);lastKey=key}
  m.innerHTML=over?vSearch():V[S.view]();
  if(over)return;
  const on=$('.stg.on',m);if(on){const r=on.parentNode;r.scrollLeft=on.offsetLeft-(r.clientWidth-on.offsetWidth)/2}
  if(S.view==='explore')paint();
  if(S.view==='study'&&S.study==='nepal'){renderCList();mountMap()}
  if(S.view==='plan'&&S.plan==='match')renderMatch()}
// one trunk in the gap: every line runs out to the same x, along it, and in again, so many links read as one bracket
let linkRaf=0,lastFoc=false;
function drawLinks(live){const f=$('#flow'),L=$('#links');if(!f||!L)return;
  const c=S.course,k=S.career;let es=[];
  if(c)es=(k&&C[c].to.includes(k)?[k]:C[c].to).map(x=>[c,x]);else if(k)es=Object.keys(C).filter(id=>C[id].to.includes(k)).map(id=>[id,k]);
  const N={};$$('.nd',f).forEach(e=>{N[(e.classList.contains('c')?'c':'k')+e.dataset.v]=e});
  const ds=[];for(const [a,b] of es){const A=N['c'+a],B=N['k'+b];if(!A||!B||A.classList.contains('gone')||B.classList.contains('gone'))continue;
    const x1=A.offsetLeft+A.offsetWidth,y1=A.offsetTop+A.offsetHeight/2,x2=B.offsetLeft,y2=B.offsetTop+B.offsetHeight/2,m=(x1+x2)/2,dy=y2-y1,r=Math.min(14,Math.abs(dy)/2,(x2-x1)/2),sg=dy<0?-1:1;
    ds.push(Math.abs(dy)<1?`M${x1} ${y1}H${x2}`:`M${x1} ${y1}H${m-r}Q${m} ${y1} ${m} ${y1+sg*r}V${y2-sg*r}Q${m} ${y2} ${m+r} ${y2}H${x2}`)}
  if(live&&L.children.length===ds.length){ds.forEach((d,i)=>L.children[i].setAttribute('d',d));return}
  L.innerHTML=ds.map((d,i)=>`<path pathLength="1" style="--i:${i}" d="${d}"/>`).join('')}
// course selected: its careers light up. career selected: every course that reaches it lights up.
function paint(){const c=S.course,k=S.career,any=c||k,foc=!!(S.foc&&any);
  const cs=id=>c?(id===c?2:0):k&&C[id].to.includes(k)?1:0,ks=id=>k?(id===k?2:0):c&&C[c].to.includes(id)?1:0;
  const set=(e,v)=>{e.classList.toggle('on',v===2);e.classList.toggle('lit',v===1);e.classList.toggle('dim',!!any&&!v&&!foc);e.classList.toggle('gone',foc&&!v)};
  $$('#flow .nd.c').forEach(e=>set(e,cs(e.dataset.v)));$$('#flow .nd.k').forEach(e=>set(e,ks(e.dataset.v)));
  const lk=$('#lk');if(lk){const n=$$('#flow .nd.lit').length+(c&&k?1:0);lk.classList.toggle('show',!!any);lk.classList.toggle('on',foc);lk.textContent='Linked '+n}
  lensPaint();drawLinks();
  cancelAnimationFrame(linkRaf);if(foc||lastFoc){const t0=performance.now();(function tick(t){drawLinks(true);if(t-t0<520)linkRaf=requestAnimationFrame(tick)})(t0)}
  lastFoc=foc}
// lens: fills every node with one metric so a whole stream can be read at a glance
function lensPaint(){$$('#flow .nd').forEach(e=>{const isC=e.classList.contains('c'),o=isC?C[e.dataset.v]:K[e.dataset.v];let w=0,t=isC?yr(o.y):'';
  if(S.lens==='d'){w=o.d;t=o.d}
  else if(S.lens==='ease'){w=100-o.c;t=100-o.c}
  else if(S.lens==='pay'){const p=isC?(o.pay?(o.pay[0]+o.pay[1])/2:0):o.pay[0];w=Math.min(100,p);t=p?Math.round(p)+'k':''}
  e.style.setProperty('--w',w+'%');$('small',e).textContent=t})}
function renderPeek(){const p=$('#pw-peek'),show=!wide()&&S.view==='explore'&&S.sel&&!S.searching;
  p.classList.toggle('show',!!show);if(!show){p.innerHTML='';return}
  const {t,id}=S.sel,o=t==='course'?C[id]:K[id];
  p.innerHTML=`<button class="pk t-${t==='course'?locate(id).sm.tone:'sc'}" data-a="open"><div><b>${o.n}</b><span>${t==='course'?o.f:payTxt(o.pay)}</span></div>${ring(o.d,'','s','currentColor')}<i class="go">${I('arrow')}</i></button>`}
function renderSheet(){const el=$('#pw-sheet'),c=cur();el.classList.toggle('open',!!(c&&(wide()||S.open)));
  el.innerHTML=c?SHEET[c.t](c.id):'';el.scrollTop=0;updExp()}
function repanel(){const c=cur(),p=$('#tabp');if(c&&p&&PANEL[c.t]){p.innerHTML=PANEL[c.t](c.id);updExp()}}
function renderNav(){$('#pw-nav').innerHTML=[['explore','route','Explore'],['study','cap','Study'],['exams','exam','Exams'],['guides','list','Guides'],['plan','flag','Plan']]
  .map(([v,ic,n])=>`<button class="${S.view===v?'on':''}" data-a="nav" data-v="${v}" aria-label="${n}" title="${n}"><i>${I(ic,24)}${v==='plan'&&S.saved.size?`<span class="cnt">${S.saved.size}</span>`:''}</i></button>`).join('')}
let NMAP=null;
const mapCounts=()=>{const m={};COL.filter(x=>x.c.includes(S.cc)).forEach(x=>{m[x.d]=(m[x.d]||0)+1});return m};
function mountMap(){const el=$('#nmap');NMAP=el&&window.PWMAP?PWMAP.mount(el,{counts:mapCounts(),selected:S.dist||'',onPick:n=>A.dist(n)}):null}
function renderCList(){const box=$('#clist');if(!box)return;const c=C[S.cc];let l=COL.filter(x=>x.c.includes(S.cc)).map(x=>({...x,fee:x.fees[S.cc]}));const MXF=Math.max(.1,...l.map(x=>x.fee||0));
  if(S.prov!=null)l=l.filter(x=>x.p===S.prov);
  const ds=[...new Set(l.map(x=>x.d))];if(!ds.includes(S.dist))S.dist=null;if(S.dist)l=l.filter(x=>x.d===S.dist);
  l=l.filter(x=>x.fee==null||x.fee<=S.cmax).sort((a,b)=>S.csort==='fee'?(a.fee??1e9)-(b.fee??1e9):b.seats-a.seats);const nAll=l.length;l=l.slice(0,60);
  box.innerHTML=(ds.length>1?`<div class="chips">${ds.map(d=>`<button class="chip ${S.dist===d?'on':''}" data-a="dist" data-v="${d}">${d}</button>`).join('')}</div>`:'')+
  (l.map(x=>`<div class="crow"><div><b>${x.n}</b><span>${x.d} · ${x.u}${x.seats?' · '+x.seats+' seats':''}</span></div><span class="tag t-${x.t==='Public'?'gc':'tc'}">${x.t}</span>${x.fee!=null?`<div class="fee"><i style="width:${x.fee/MXF*100}%"></i></div><span class="fv">${lakh(x.fee)}</span>`:''}</div>`).join('')||empty('No colleges'))+(nAll>60?`<p class="mk-n">Showing 60 of ${nAll}. Narrow by province, district or fee.</p>`:'')}
const QI={build:'Making and fixing things',heal:'Helping people get well',num:'Data, money, patterns',ppl:'Teaching, leading, talking',make:'Design, art, media',law:'Rules, fairness, debate',nature:'Land, plants, outdoors',serve:'Public service, community'};
const QP={pay:'A bigger salary',demand:'Plenty of jobs open',ease:'Easier to get in',cost:'Lower fees',abroad:'Chances overseas',near:'Colleges close to me'};
const QT=[0,['What have you finished?','This sets which courses we compare.'],['What do you enjoy?','Pick up to 3. Go with your gut.'],['What are you good at?','Pick up to 3 subjects or skills.'],['What matters most?','Pick up to 3. We weigh these hardest.'],['What can you spend?','Total fees for the whole course.'],['How do you take risks?','Some courses are hard to get into.']];
const mpool=()=>(STAGES.find(s=>s.id===S.mstg)||stage()).streams.flatMap(x=>x.courses).map(id=>C[id]);
const KW={build:['build','engineer','construct','machine','civil','mechanic','electric','software','repair'],heal:['health','patient','clinic','nurs','medic','pharma','care','dental'],num:['account','finance','statist','data','audit','bank','math','econom'],ppl:['teach','people','manage','communicat','lead','counsel','social','hospitality'],make:['design','art','media','creative','film','music','architect','journal'],law:['law','legal','court','justice','policy','police'],nature:['agricultur','forest','environment','plant','animal','land','veterin'],serve:['public','govern','service','community','army','police']};
const KS={math:['math','statist','account','data','physics'],sci:['science','physic','chem','lab','research'],bio:['biolog','anatomy','patient','clinic','agricultur'],lang:['english','writing','communicat','nepali','language','journal'],biz:['business','finance','account','market','sales','manage'],comp:['program','computer','software','coding','data'],art:['design','draw','creative','art']};
const mtext=c=>c._t||(c._t=(c.n+' '+c.f+' '+c.to.map(k=>K[k].n+' '+(K[k].sk||[]).join(' ')).join(' ')).toLowerCase());
const mavg=a=>a.length?a.reduce((p,v)=>p+v,0)/a.length:0;
/* How rare each keyword is across all courses: a word found in few courses is strong evidence, one found in every course says little. */
const IDF=(()=>{const T=Object.values(C).map(mtext),n=T.length,o={};[...Object.values(KW),...Object.values(KS)].flat().forEach(w=>{if(o[w]!=null)return;const df=T.filter(t=>t.includes(w)).length;o[w]=Math.max(.2,Math.log((n+1)/(df+1))+.4)});return o})();
/* Every answer becomes a 0..1 signal per course: tag = 1, group and keyword = .6 to 1 (keywords weighted by rarity), group = .6, keyword alone up to .55; a course whose stream the strengths cannot meet is cut by a fifth. Interests count the best signal and the average, so one strong hit is not drowned by a third pick. */
function matchOf(pool){
  const mxp=Math.max(1,...pool.map(c=>c.pay?c.pay[1]:0)),mxf=Math.max(1,...pool.map(c=>c.fee[0])),b=S.mb,R=S.mr;
  return pool.map(c=>{const g=grpOf(c),txt=mtext(c),hit=(m,x)=>(m[x]||[]).some(y=>g.includes(y)),kw=(m,x)=>{const h=m[x].filter(w=>txt.includes(w));if(!h.length)return 0;const all=m[x].reduce((a,w)=>a+(IDF[w]||1),0)||.1;return .45+.55*Math.min(1,h.reduce((a,w)=>a+(IDF[w]||1),0)/all*2.5)},
    sig=(set,tag,gm,km)=>[...set].map(x=>{if(tag(x))return 1;const k=kw(km,x),g=hit(gm,x);return g&&k?.6+.4*k:g?.6:k?.55*k:0}),
    agg=a=>!a.length?.5:a.some(v=>v>0)?.15+.85*(.5*Math.max(...a)+.5*mavg(a)):0,
    it=agg(sig(S.mi,x=>c.tags.includes(x),IG,KW)),sr0=agg(sig(S.ms,x=>c.st===x,SG,KS)),sr=S.ms.size&&!sr0?.1:sr0,
    [lo,hi]=c.fee,bf=hi<=b?1:lo<=b?.4+.6*(b-lo)/Math.max(.01,hi-lo):Math.max(0,.3*(1-(lo-b)/Math.max(lo,.01))),
    x=X[CX[c.id]],tr=mavg(c.to.map(k=>K[k].f.tr||0)),ez=x&&x.seats?Math.min(1,x.seats/x.apps*1.6):1-c.c/100,ease=.5*(1-c.c/100)+.5*ez,
    pr={pay:(c.pay?c.pay[1]:0)/mxp,demand:c.d/100,ease,cost:1-lo/mxf,abroad:g.length?Math.max(...g.map(y=>ABR[y]||0)):.3,near:S.dist&&COL.some(y=>y.d===S.dist&&y.c.includes(c.id))?1:0},
    ch=[...S.mp],ps=ch.length?mavg(ch.map(k=>pr[k])):(pr.demand+pr.pay)/2,
    yf=!S.my||c.y<=S.my?1:Math.max(0,1-(c.y-S.my)/Math.max(1,S.my)),
    base=R==='safe'?.4*c.d/100+.6*ease:R==='bold'?.4*c.d/100+.6*pr.pay:c.d/100,ol=Math.max(0,Math.min(1,base+tr/60)),
    nds=c.needs||[],met=n=>n==='sci'?[...S.ms].some(v=>['math','sci','bio','comp'].includes(v)):n==='bio'?S.ms.has('bio'):n==='math'?S.ms.has('math')||S.ms.has('comp'):S.ms.has('biz'),kn=S.mstg==='after12'&&S.mst,ok=!nds.length||(kn?nds.every(n=>STMET[n].includes(S.mst)):(!S.ms.size||nds.every(met))),
    t=(.32*it+.16*sr+.14*bf+.2*ps+.18*ol)*(.7+.3*yf)*(bf<.15?.85:1)*(ok?1:kn?.55:.8),why=[],neg=[];
    if(S.mi.size&&it>=.6)why.push('Fits your interests');if(S.ms.size&&sr>=.7)why.push('Plays to your strengths');if(bf>=1)why.push('In budget');if(nds.length&&ok&&(kn||S.ms.size))why.push(kn?'Open to your stream':'Matches the subjects it needs');if(!nds.length&&kn)why.push('Open to any stream');
    ch.filter(k=>pr[k]>=.7).forEach(k=>why.push(PRI.find(y=>y[0]===k)[1]));if(tr>=3)why.push('Demand is rising');
    if(bf<.4)neg.push('Fees start at '+lakh(lo));if(yf<1)neg.push('Takes '+yr(c.y));if(S.mi.size&&it<.6)neg.push('Not your interests');if(S.ms.size&&sr<.7)neg.push('Outside your strengths');if(nds.length&&!ok)neg.push('Needs '+nds.filter(n=>kn?!STMET[n].includes(S.mst):!met(n)).map(n=>NDL[n]).join(' and ')+(kn?', you studied '+STM.find(y=>y[0]===S.mst)[1]:''));if(R==='safe'&&ease<.35)neg.push('Hard to get into');
    return{c,s:Math.max(1,Math.min(99,Math.round(100*Math.pow(t,1.8)))),why:why.slice(0,3),neg,p:{Interests:it,Strengths:sr,Budget:bf,Priorities:ps,Outlook:ol}}}).sort((a,b)=>b.s-a.s)}
const MK='nebm';
function msave(){try{localStorage.setItem(MK,JSON.stringify({i:[...S.mi],s:[...S.ms],p:[...S.mp],b:S.mb,y:S.my,r:S.mr,g:S.mstg,m:S.mst,d:S.mdone}))}catch(e){}}
function mload(){try{const o=JSON.parse(localStorage.getItem(MK)||'null');if(!o||!STAGES.some(x=>x.id===o.g))return;
  S.mi=new Set(o.i);S.ms=new Set(o.s);S.mp=new Set(o.p);S.mb=+o.b||15;S.my=+o.y||0;S.mr=o.r||'mid';S.mstg=o.g;S.mst=STM.some(x=>x[0]===o.m)?o.m:'';S.mdone=!!o.d}catch(e){}}
const qo=(a,v,on,t,s)=>`<button class="qo ${on?'on':''}" data-a="${a}" data-v="${v}"><b>${t}</b>${s?`<span>${s}</span>`:''}</button>`;
/* The +2 stream the student finished. It is asked only at the After +2 stage, where it decides which degrees are open. */
const STM=[['pcm','Science, Physical group','Maths compulsory, Physics, Chemistry, Computer optional'],['pcb','Science, Biology group','Physics, Chemistry, Biology'],['mgt','Management','Accountancy, Economics, Business Studies'],['hum','Humanities','Sociology, Economics, Media, Population'],['edu','Education','Education and Development'],['law','Law','Constitutional and Procedural Law'],['tec','Technical','CTEVT or technical stream']],STMET={sci:['pcm','pcb'],bio:['pcb'],math:['pcm'],mgmt:['mgt']},NDL={sci:'Science',bio:'Biology',math:'Maths',mgmt:'Management'};
const mstHTML=()=>S.mstg==='after12'?`<h4 style="margin-top:18px">Which stream did you study?</h4><div class="qg">${STM.map(([v,n,d])=>qo('mst',v,S.mst===v,n,d)).join('')}</div>`:'';
const qset=k=>({2:S.mi,3:S.ms,4:S.mp})[k];
function qBody(k){
  if(k===1)return `<div class="qg one">${STAGES.map(s=>qo('mstg',s.id,S.mstg===s.id,s.l,s.streams.map(x=>x.n).join(' · '))).join('')}</div><div id="mstbox">${mstHTML()}</div>`;
  if(k===2)return `<div class="qg">${INT.map(([v,n])=>qo('mi',v,S.mi.has(v),n,QI[v])).join('')}</div>`;
  if(k===3)return `<div class="qg">${STR.map(([v,n])=>qo('ms',v,S.ms.has(v),n)).join('')}</div>`;
  if(k===4)return `<div class="qg">${PRI.filter(p=>p[0]!=='near'||S.dist).map(([v,n])=>qo('mp',v,S.mp.has(v),n,QP[v])).join('')}</div>`;
  if(k===5){const n=mpool().filter(c=>c.fee[1]<=S.mb).length;
    return `<div class="big" style="margin:0 0 4px"><b id="mbv">NPR ${S.mb}L</b><span id="mbn">${n} of ${mpool().length} courses fit fully</span></div>
    <input type="range" id="mb" min="1" max="60" value="${S.mb}" aria-label="Budget"><h4 style="margin-top:14px">How long can you study?</h4>
    <div class="qg three">${[[2,'Up to 2 yr'],[4,'Up to 4 yr'],[0,'Any length']].map(([v,n])=>qo('my',v,S.my===v,n)).join('')}</div>`}
  if(k===6)return `<div class="qg one">${[['safe','Play it safe','Courses where getting in is realistic'],['mid','Balanced','A mix of safe and ambitious'],['bold','Aim high','Tough entry is fine if the payoff is big']].map(([v,n,d])=>qo('mr',v,S.mr===v,n,d)).join('')}</div>`;
  return ''}
function qHTML(){const k=S.mstep;
  if(k===7){return `<div class="qz"><div class="qb"><div class="qld"><div class="qhero">${shape(8,'spin')}<b>${mpool().length}</b></div><p id="qlt">Reading your answers</p></div></div></div>`}
  const ms=qset(k),need=ms&&!ms.size,last=k===6;
  return `<div class="qz"><div class="qh"><button class="ib" data-a="mback" aria-label="Back">${I(k>1&&!S.medit?'back':'close')}</button>
    <div class="qp">${[1,2,3,4,5,6].map(i=>`<i class="${i<k?'f':''} ${i===k?(S.qa?'c':'c still'):''}"></i>`).join('')}</div>
    <button class="qs" data-a="mskip" ${ms?'':'hidden'}>Skip</button></div>
  <div class="qb ${S.qa?(S.mdir>0?'in':'rev'):''}"><h2 class="qt">${QT[k][0]}</h2><p class="qd">${QT[k][1]}</p>${qBody(k)}</div>
  <div class="qf"><div class="qn" id="qn">${ms?ms.size+' of 3 picked':''}</div><button class="btn f" id="qnext" data-a="mnext" ${need?'disabled':''}>${S.medit?'Update matches':last?'See my matches':'Next'}</button></div></div>`}
const mans=()=>{const l=(set,L)=>set.size?[...set].map(k=>(L.find(x=>x[0]===k)||[,k])[1]).join(', '):'Any';
  return [[1,'Stage',stage_of(S.mstg).l+(S.mstg==='after12'&&S.mst?' · '+STM.find(y=>y[0]===S.mst)[1]:'')],[2,'Enjoy',l(S.mi,INT)],[3,'Good at',l(S.ms,STR)],[4,'Care about',l(S.mp,PRI)],[5,'Budget','NPR '+S.mb+'L'+(S.my?' · '+S.my+' yr':'')],[6,'Style',{safe:'Safe',mid:'Balanced',bold:'Aim high'}[S.mr]]]};
const stage_of=id=>STAGES.find(s=>s.id===id)||stage();
function mcard(m,i){const {c,s,why,p}=m,open=S.mopen===c.id,k=C[c.id],pay=c.pay?'NPR '+c.pay[0]+'–'+c.pay[1]+'k':'Varies';
  return `<div class="mc ${i===0?'top':''} ${open?'open':''}"><button class="mt" data-a="mx" data-v="${c.id}">${ring(s,'','s still','currentColor')}<div><b>${c.n}</b>${why.length?`<div class="rz">${why.map(w=>`<i>${w}</i>`).join('')}</div>`:`<span>${c.f}</span>`}</div><i class="chv">${I('arrow',20)}</i></button>
  ${open?`<div class="md">${Object.entries(p).map(([l,v])=>`<div class="fb"><span>${l}</span><div><i style="width:${Math.max(4,Math.round(v*100))}%"></i></div><b>${Math.round(v*100)}</b></div>`).join('')}
  ${facts([['Duration',yr(c.y)],['Fees',lakh(c.fee[0])+'–'+lakh(c.fee[1]).replace('NPR ','')],['Start pay',pay]])}
  <div class="mx"><button class="btn t" data-a="goCourse" data-v="${c.id}">Open course</button><button class="ib ${S.saved.has('course:'+c.id)?'on':''}" data-a="save" data-v="course:${c.id}" aria-label="Save">${I('bookmark')}</button></div></div>`:''}</div>`}
function matchPanel(){
  if(!S.mdone){const prog=S.mstep>1;
    return `<div class="mh"><div class="qhero">${shape(8,'spin')}<b>Match</b></div><h3>${prog?'Pick up where you left off':'Find the course that fits you'}</h3>
    <p>${prog?'You are on step '+S.mstep+' of 6. Your answers so far are kept.':'Six quick questions, about a minute. We rank every course for your stage by your interests, strengths, budget and goals.'}</p>
    <button class="btn f" data-a="${prog?'mresume':'mstart'}">${prog?'Continue':'Start matching'}</button>${prog?`<button class="btn t" data-a="mretake">Start over</button>`:''}</div>
    <div class="chips w">${['Interests','Strengths','Budget','Priorities','Competition'].map(t=>`<span class="skill">${t}</span>`).join('')}</div>`}
  const all=matchOf(mpool()),strong=all.filter(m=>m.s>=65),poss=all.filter(m=>m.s>=40&&m.s<65),weak=all.filter(m=>m.s<40),good=strong.length+poss.length;
  if(!S.mopen&&S.mopen!==''&&all[0])S.mopen=all[0].c.id;
  const head=`<div class="mhd"><div><b>${good?'Your matches':'No matches yet'}</b><span>${stage_of(S.mstg).l} · ${strong.length} strong · ${poss.length} possible · ${S.mi.size+S.ms.size+S.mp.size+2+(S.mstg==='after12'&&S.mst?1:0)} answers</span></div><button class="btn t sm" data-a="mretake">Retake</button></div>
    <div class="chips">${mans().map(([i,l,v])=>`<button class="chip" data-a="medit" data-v="${i}">${l}: ${v}</button>`).join('')}</div>`;
  if(!good){const mn=Math.min(...mpool().map(c=>c.fee[0])),tips=[];
    if(mn>S.mb)tips.push('Cheapest course here starts at '+lakh(mn)+'. Your budget is NPR '+S.mb+'L.');
    if(S.my)tips.push('You limited study to '+S.my+' years. Try any length.');
    if(S.mi.size&&S.ms.size)tips.push('Your interests and strengths point in different directions. Try fewer picks.');
    tips.push('Try a different stage, or loosen one answer.');
    return head+`<div class="nom">${shape(6)}<h3>Nothing fits well</h3><p>None of the ${all.length} courses at this stage scored well on your answers.</p><div class="tips">${tips.slice(0,3).map(t=>`<div>${t}</div>`).join('')}</div>
    <button class="btn f" data-a="medit" data-v="5">Change budget</button><button class="btn t" data-a="medit" data-v="1">Try another stage</button></div>`}
  let i=0;const grp=(t,l)=>l.length?`<h4>${t}</h4>`+l.map(m=>mcard(m,i++)).join(''):'';
  return head+(strong.length?'':`<div class="note">No strong match, but these are the closest. Tap one to see why.</div>`)+grp('Best fit',strong)+grp(strong.length?'Worth a look':'Closest options',poss)+
    (weak.length?`<button class="mw" data-a="mweak"><span>Not a good fit (${weak.length})</span>${I('arrow',18)}</button>${S.mweak?weak.map(m=>lrow('goCourse',m.c.id,m.c.n,m.neg.join(' · ')||m.c.f,m.s)).join(''):''}`:'')}
function renderMatch(){const box=$('#mres');if(!box)return;box.innerHTML=matchPanel()}
function qUpd(){const k=S.mstep,ms=qset(k),b=$('#qnext');if(!ms||!b)return;b.disabled=!ms.size;$('#qn').textContent=ms.size+' of 3 picked'}
function qgo(n,d){S.mstep=n;S.mdir=d;S.qa=true;msave();renderMain();S.qa=false;
  if(n===7){const T=['Reading your answers','Weighing '+mpool().length+' courses','Ranking your matches'];T.forEach((t,i)=>setTimeout(()=>{const e=$('#qlt');if(e&&S.mstep===7)e.textContent=t},i*550));setTimeout(()=>{if(S.mq&&S.mstep===7)qdone()},1700)}}
function qdone(){S.mq=false;S.medit=false;S.mstep=0;S.mdone=true;S.mopen=null;S.mweak=false;msave();render()}
const qpush=()=>{try{history.pushState({q:S.mstep},'')}catch(e){}};
function qback(){if(!S.mq)return;if(S.mstep>1&&!S.medit)qgo(S.mstep-1,-1);else{S.mq=false;S.medit=false;if(!S.mdone&&S.mstep===1)S.mstep=0;render()}}
const pick1=t=>$$('.qo',t.parentNode).forEach(b=>b.classList.toggle('on',b===t));
const capped=(set,v,t)=>{if(!set.has(v)&&set.size>=3){if(t.animate)t.animate([{transform:'translateX(-6px)'},{transform:'translateX(6px)'},{transform:'none'}],{duration:240});return}tog(set,v);t.classList.toggle('on');msave();qUpd()};
addEventListener('popstate',()=>{if(S.mq)qback()});
function chrome(){const a=$('.app');if(a)a.classList.toggle('quiz',!!(S.view==='plan'&&S.plan==='match'&&S.mq))}
function render(){chrome();renderTop();renderNav();renderSheet();renderMain();renderPeek()}

/* ============ ACTIONS ============ */
const clearOver=()=>{S.searching=false;S.q=''};
const select=()=>{paint();renderTop();renderPeek();renderSheet()};
// cross-links between sections remember where they came from, so Back returns there
const jump=()=>{S.back.push({view:S.view,open:S.open});if(S.back.length>8)S.back.shift()};
const A={
nav(v){S.view=v;S.open=false;S.back=[];clearOver();render()},
stage(v){const i=STAGES.findIndex(s=>s.id===v);S.stage=v;S.stream=stage().streams[0].id;S.edu=STAGE_EDU[i];S.age=STAGE_AGE[i];S.course=S.career=S.sel=null;S.path=[];S.open=false;render()},
stream(v){S.stream=v;S.course=S.career=S.sel=null;render()},
home(){S.course=S.career=S.sel=null;render()},
foc(){S.foc=!S.foc;paint()},
lens(v){S.lens=S.lens===v?null:v;$$('.lz').forEach(b=>b.classList.toggle('on',b.dataset.v===S.lens));lensPaint()},
course(v){if(S.course===v){S.course=null;S.sel=S.career?{t:'career',id:S.career}:null}else{S.course=v;if(S.career&&!C[v].to.includes(S.career))S.career=null;S.sel={t:'course',id:v};S.tabs.course='journey';S.cmp=null}select()},
career(v){if(S.career===v){S.career=null;S.sel=S.course?{t:'course',id:S.course}:null}else{S.career=v;if(S.course&&!C[S.course].to.includes(v))S.course=null;S.sel={t:'career',id:v};S.exp=3}select()},
open(){S.open=true;renderSheet();renderPeek()},
close(){if(S.back.length){const b=S.back.pop();S.view=b.view;S.open=b.open;render()}else{S.open=false;renderSheet();renderPeek()}},
tab(v,t){const c=cur();if(!c)return;S.tabs[c.t]=v;$$('.tabs button').forEach(b=>b.classList.toggle('on',b===t));repanel()},
seg(v,t){const s=t.closest('.split'),was=t.classList.contains('on');$$('button',s).forEach(b=>b.classList.toggle('on',!was&&b.dataset.v===v));s.classList.toggle('has',!was)},
cmp(v){S.cmp=v;repanel()},
cpriv(v){S.cpriv=v;repanel()},live(v){S.live=v;repanel()},
rung(v){S.exp=+v;updExp()},
have(v,t){tog(S.have,v);t.classList.toggle('on');const c=cur(),box=$('#rdy');if(!c||c.t!=='career'||!box)return;
  const k=K[c.id],p=Math.round(k.sk.filter(s=>S.have.has(s)).length/k.sk.length*100);$('.fg',box).style.strokeDashoffset=100-p;$('b',box).textContent=p},
save(v,t){tog(S.saved,v);t.classList.toggle('on');renderNav()},
next(v){const {st,sm}=locate(v),nx=STAGES[STAGES.indexOf(st)+1];if(!nx)return;S.path.push({stage:st.id,stream:sm.id,course:v});
  S.stage=nx.id;S.stream=nx.streams.some(x=>x.id===C[v].ns)?C[v].ns:nx.streams[0].id;S.course=S.career=S.sel=null;S.open=false;S.back=[];S.view='explore';render()},
trail(i){const p=S.path[+i];if(!p)return;S.path=S.path.slice(0,+i);S.stage=p.stage;S.stream=p.stream;S.course=p.course;S.career=null;S.sel={t:'course',id:p.course};S.tabs.course='journey';render()},
goCourse(v){if(S.view!=='explore')jump();const {st,sm}=locate(v);if(st.id!==S.stage)S.path=[];S.stage=st.id;S.stream=sm.id;S.course=v;if(S.career&&!C[v].to.includes(S.career))S.career=null;
  S.sel={t:'course',id:v};S.tabs.course='journey';S.cmp=null;S.open=true;S.view='explore';clearOver();render()},
goCareer(v){if(S.view!=='explore')jump();
  if(!stream().courses.some(c=>C[c].to.includes(v))){const c=Object.keys(C).find(c=>C[c].to.includes(v)),{st,sm}=locate(c);S.stage=st.id;S.stream=sm.id;S.course=null;S.path=[]}
  if(S.course&&!C[S.course].to.includes(v))S.course=null;S.career=v;S.sel={t:'career',id:v};S.exp=3;S.open=true;S.view='explore';clearOver();render()},
goExam(v){jump();S.view='exams';S.xg=X[v].g;S.exam=v;S.tabs.exam='stages';S.open=true;clearOver();render()},
goGuide(v){jump();S.view='guides';S.gcat='All';S.guide=v;S.open=true;clearOver();render()},
goStudy(v){S.view='study';S.study=v;S.open=false;S.back=[];clearOver();render()},
goSch(v){S.view='study';S.study='funding';S.stype='All';S.slvl='All';S.sk=null;S.schOpen=v;S.open=false;S.back=[];clearOver();render()},
find(v){S.cc=v;S.cmax=null;S.prov=S.dist=null;S.view='study';S.study='nepal';S.open=false;S.back=[];clearOver();render()},
study(v){S.study=v;renderMain()},
cc(v){S.cc=v;S.cmax=null;S.prov=S.dist=null;renderMain()},
dist(v){S.dist=v&&S.dist!==v?v:null;renderCList();if(NMAP)NMAP.update(mapCounts(),S.dist||'')},
csort(v){S.csort=v;renderMain()},
vstep(v){const k='v'+v;if(S.done.has(k))S.done.delete(k);else S.done.add(k);const l=$('#ablist');if(l)l.innerHTML=abList()},
ctry(v){S.ab=S.ab===v?null:v;const l=$('#ablist');if(l)l.innerHTML=abList();else renderMain()},
skf(v){S.sk=v||null;S.study='funding';S.stype='All';S.slvl='All';renderMain()},
stype(v){S.stype=v;renderMain()},slvl(v){S.slvl=v;renderMain()},
sch(v){S.schOpen=S.schOpen===v?null:v;renderMain()},
xgr(v){const t=TR.find(r=>r[3]===v);if(t)A.xg(t[0])},
xg(v){S.xg=v;const l=Object.values(X).filter(x=>x.g===v);if(!l.some(x=>x.id===S.exam))S.exam=l[0].id;S.tabs.exam='stages';renderMain();renderSheet()},
edu(v){S.edu=+v;renderMain()},gv(v){S.gv=v;renderMain()},fqt(v){S.fqt=v;renderMain()},fqo(v,t){const e=t.closest('.fq'),o=e.classList.contains('open');$$('.fq.open').forEach(x=>x.classList.remove('open'));if(!o)e.classList.add('open');S.fqo=o?null:v},fqh(v,t){tog(S.fqh,v);t.classList.toggle('on')},xf(v){S.xf=S.xf===v?'all':v;$('#xlist').innerHTML=xlistHTML()},xs(v){S.xs=v;$('#xlist').innerHTML=xlistHTML()},
woman(v){S.woman=v;renderMain()},
exam(v){S.exam=v;S.tabs.exam='stages';S.open=true;renderMain();renderSheet()},
gcat(v){S.gcat=v;renderMain()},
guide(v){S.guide=v;S.open=true;renderMain();renderSheet()},
step(v,t){tog(S.done,v);t.classList.toggle('done');const g=G[v.split(':')[0]],w=gdone(g)/g.steps.length*100+'%',a=$('#gdone'),b=$('#gbar'),c=$(`.gd[data-v="${g.id}"] .gp i`);
  if(a)a.textContent=gdone(g);if(b)b.style.width=w;if(c)c.style.width=w},
doc(v,t){tog(S.docs,v);t.classList.toggle('on')},
plan(v){S.plan=v;renderMain()},
mi(v,t){capped(S.mi,v,t)},ms(v,t){capped(S.ms,v,t)},mp(v,t){capped(S.mp,v,t)},
mstart(){S.mq=true;S.medit=false;S.mstep=1;S.mdir=1;S.qa=true;qpush();render();S.qa=false},
mresume(){S.mq=true;S.mdir=1;S.qa=true;qpush();render();S.qa=false},
mretake(){S.mi=new Set();S.ms=new Set();S.mp=new Set();S.mb=15;S.my=0;S.mr='mid';S.mdone=false;S.mopen=null;A.mstart();msave()},
medit(v){S.mq=true;S.medit=true;S.mstep=+v;S.mdir=1;S.qa=true;qpush();render();S.qa=false},
mback(){if(history.state&&history.state.q)history.back();else qback()},
mnext(){if(S.medit)return qdone();if(S.mstep>=6){qpush();return qgo(7,1)}qpush();qgo(S.mstep+1,1)},
mskip(){const k=qset(S.mstep);if(k)k.clear();A.mnext()},
mstg(v,t){S.mstg=v;pick1(t);msave();const b=$('#mstbox');if(b)b.innerHTML=mstHTML();if(!S.medit&&v!=='after12')setTimeout(()=>{if(S.mq&&S.mstep===1)A.mnext()},280)},
mst(v,t){S.mst=S.mst===v?'':v;pick1(t);if(!S.mst)t.classList.remove('on');msave()},my(v,t){S.my=+v;pick1(t);msave()},mr(v,t){S.mr=v;pick1(t);msave()},
mx(v){S.mopen=S.mopen===v?'':v;renderMatch()},
mweak(){S.mweak=!S.mweak;renderMatch()},
search(){S.searching=!S.searching;S.q='';renderTop();renderMain();renderPeek();const q=$('#q');if(q)q.focus()}
};
const IN={
q(v){S.q=v.trim();renderMain();renderPeek()},
exp(v){S.exp=+v;updExp()},
cmax(v){S.cmax=+v;$('#cmaxv').textContent=lakh(S.cmax);renderCList()},
abmax(v){S.abmax=+v;$('#abv').textContent='NPR '+v+'L';$('#ablist').innerHTML=abList()},
mb(v){S.mb=+v;$('#mbv').textContent='NPR '+v+'L';const n=mpool().filter(c=>c.fee[1]<=S.mb).length;$('#mbn').textContent=n+' of '+mpool().length+' courses fit fully';msave()},
fqq(v){S.fqs=v;const b=$('#fqlist');b.classList.add('nan');b.innerHTML=faqList()},age(v){S.age=+v;$('#agev').textContent='Age '+v;$('#xlist').innerHTML=xlistHTML()},
page(v){S.age=+v;$('#pagev').textContent=v;$('#pout').innerHTML=planOut()},
hrs(v){S.hrs=+v;$('#hrv').textContent=v;$('#prepout').innerHTML=prepOut(X[S.exam])},
aid(v){S.aid=+v;$('#aidv').textContent='Aid '+v+'%';const c=cur();if(c&&c.t==='course')$('#costout').innerHTML=costOut(C[c.id])}
};
root.addEventListener('click',e=>{const t=e.target.closest('[data-a]');if(t&&A[t.dataset.a])A[t.dataset.a](t.dataset.v,t)});
root.addEventListener('input',e=>{const f=IN[e.target.id];if(f)f(e.target.value)});
root.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches('[role=button]')){e.preventDefault();e.target.click()}});
new ResizeObserver(()=>{if(wide()!==lastWide){lastWide=wide();render()}else drawLinks(true)}).observe($('#pw-main'));
new ResizeObserver(()=>{if(wide()!==lastWide){lastWide=wide();render()}}).observe(root);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(drawLinks);
mload();
render();
root.addEventListener("click",()=>setTimeout(persist,0));
}).catch(()=>fail("Pathways could not load. Check your connection and refresh."));
})();

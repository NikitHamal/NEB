
(function(window, document) {
  'use strict';

  var AvatarProceduralEngine=(function(e){Object.defineProperty(e,Symbol.toStringTag,{value:`Module`});var t=(e,t)=>Math.sign(e)*Math.abs(e)**t,n=(e,n,r,i,a,o,s)=>{let c=t(Math.cos(n),o);return[r/2*c*t(Math.sin(e),s),i/2*t(Math.sin(n),o),a/2*c*t(Math.cos(e),s)]},r=(e,t,n)=>{let r=e.width/2,i=e.depth/2,a=Math.min(r,e.height/2),o=Math.max(0,(e.height-a*2)/2),s=o*2+Math.PI*a,c=(n+Math.PI/2)/Math.PI*s,l=r,u=0;if(c<Math.PI*a/2){let e=-Math.PI/2+c/a;l=r*Math.cos(e),u=-o+a*Math.sin(e)}else if(c<=Math.PI*a/2+o*2)u=-o+c-Math.PI*a/2;else{let e=(c-Math.PI*a/2-o*2)/a;l=r*Math.cos(e),u=o+a*Math.sin(e)}let d=r?i/r:1;return[l*Math.sin(t),u,l*d*Math.cos(t)]},i=e=>Math.max(0,Math.min(2,e??0)),a=e=>1+i(e.roundness)/2,o=.04,s=e=>e.roundness<=0?1/0:2/(o+i(e.roundness)/2*.96),c=(e,t,n,r)=>{let i=Math.cos(n)*Math.sin(t),a=Math.sin(n),o=Math.cos(n)*Math.cos(t),s=Number.isFinite(r)?(Math.abs(i)**r+Math.abs(a)**r+Math.abs(o)**r)**(1/r)||1:Math.max(Math.abs(i),Math.abs(a),Math.abs(o))||1;return[e.width/2*(i/s),e.height/2*(a/s),e.depth/2*(o/s)]},l=(e,t,n)=>c(e,t,n,a(e)),u=(e,t,n)=>c(e,t,n,s(e)),d=.24,f=.2,p=.22,m=e=>i(e.morphRoundness)/2,h=(e,t,n)=>{let r=m(e),i=Math.max(0,Math.min(1,t)),a=Math.sin(i*Math.PI),o=(1-Math.cos(i*Math.PI))/2;return{radiusScale:n.radiusScale+(a-n.radiusScale)*r,verticalProgress:n.verticalProgress+(o-n.verticalProgress)*r}},g=(e,t,n,r,i)=>{let a=1-i;return a**3*e+3*a*a*i*t+3*a*i*i*n+i**3*r},_=e=>({tipFraction:(e.tipRoundness??0)*d,baseFraction:(e.baseRoundness??0)*f}),v=(e,t)=>{let n=Math.max(0,Math.min(1,t)),r=e.roundness*p;if(r<=0)return{radiusScale:1,verticalProgress:(Math.sin((n-.5)*Math.PI)+1)/2};if(n<r){let e=-Math.PI/2+n/r*(Math.PI/2);return{radiusScale:1-r+r*Math.cos(e),verticalProgress:(r+r*Math.sin(e))/2}}if(n>1-r){let e=(n-(1-r))/r*(Math.PI/2);return{radiusScale:1-r+r*Math.cos(e),verticalProgress:1-r/2+r*Math.sin(e)/2}}let i=(n-r)/(1-r*2);return{radiusScale:1,verticalProgress:r/2+i*(1-r)}},y=(e,t)=>h(e,t,v(e,t)),b=(e,t,n)=>{let r=Math.max(0,Math.min(1,t)),i=0,a=1;for(let t=0;t<14;t+=1){let t=(i+a)/2;n(e,t).verticalProgress<r?i=t:a=t}return n(e,(i+a)/2).radiusScale},x=(e,t)=>{let n=Math.max(0,Math.min(1,t)),{tipFraction:r,baseFraction:i}=_(e);if(i>0&&n<i){let e=n/i;return{radiusScale:g(1-i,1,1-i/2,1-i,e),verticalProgress:g(0,0,i/2,i,e)}}if(r>0&&n>1-r){let e=(n-(1-r))/r;return{radiusScale:g(r,r/2,r/4,0,e),verticalProgress:g(1-r,1-r/2,1,1,e)}}return{radiusScale:1-n,verticalProgress:n}},S=(e,t)=>h(e,t,x(e,t)),C=e=>{let t=e.height*.36,n=e.height-t;return{coneApexY:-e.height/2,coneBaseY:-e.height/2+t,bodyHeight:n,bodyCenterY:e.height/2-n/2,bodyWidth:e.width*.54,bodyDepth:e.depth*.62}},w=(e,t,a)=>{let{width:o,height:s,depth:c}=e;switch(e.type){case`sphere`:case`mickey`:return n(t,a,o,s,c,1,1);case`cube`:return u(e,t,a);case`cylinder`:{let n=y(e,(a+Math.PI/2)/Math.PI);return[o/2*n.radiusScale*Math.sin(t),-s/2+s*n.verticalProgress,c/2*n.radiusScale*Math.cos(t)]}case`cursor`:{let n=C(e),r=(a+Math.PI/2)/Math.PI,i=v({...e,width:n.bodyWidth,height:n.bodyHeight,depth:n.bodyDepth},r);return[n.bodyWidth/2*i.radiusScale*Math.sin(t),n.bodyCenterY-n.bodyHeight/2+n.bodyHeight*i.verticalProgress,n.bodyDepth/2*i.radiusScale*Math.cos(t)]}case`diamond`:return l(e,t,a);case`capsule`:return r(e,t,a);case`cone`:{let n=S(e,(a+Math.PI/2)/Math.PI);return[o/2*n.radiusScale*Math.sin(t),s/2-s*n.verticalProgress,c/2*n.radiusScale*Math.cos(t)]}case`torus`:{let e=(o+c)/4,n=Math.max(2,s/2),r=t,i=a*2,l=e+n*Math.cos(i);return[l*Math.sin(r),n*Math.sin(i),l*Math.cos(r)]}case`star`:{let e=t,n=(Math.abs(Math.sin(2*e))+.3)/1.3,r=Math.cos(a);return[o/2*r*Math.sin(e)*n,s/2*Math.sin(a)*n,c/2*r*Math.cos(e)*n]}case`cloud`:{let e=Math.cos(a),n=1+.18*Math.cos(3*t)*Math.cos(2*a),r=1+.15*Math.sin(3*t);return[o/2*e*Math.sin(t)*n,s/2*Math.sin(a)*r,c/2*e*Math.cos(t)*n]}case`book`:{let e=Math.sin(t),n=Math.cos(a);return[o/2*e,s/2*Math.sin(a),c/2*n*Math.cos(t)+c/2*Math.abs(e)*.28]}case`hand`:{let e=Math.cos(a),n=1+.15*Math.cos(t);return[o/2*e*Math.sin(t),s/2*Math.sin(a)*n,c/2*e*Math.cos(t)]}case`egg`:{let e=Math.sin(a),n=Math.cos(a),r=1-.17*e;return[o/2*n*Math.sin(t)*r,s/2*e,c/2*n*Math.cos(t)*r]}case`bean`:{let e=Math.sin(a),n=Math.cos(a),r=.88+.14*Math.cos(a*2);return[o*.08*(e*e-.35)+o/2*n*Math.sin(t)*r,s/2*e,c/2*n*Math.cos(t)*(1-.08*e)]}case`heart`:{let e=Math.sin(a),n=Math.cos(a),r=Math.cos(t),i=Math.sin(t),l=Math.max(0,-e),u=1+.18*l*Math.cos(t*2),d=1-.22*l*Math.max(0,r),f=1-.18*Math.max(0,e);return[o/2*n*i*u,s/2*e*f+s*.035,c/2*n*r*d]}case`droplet`:{let e=(a+Math.PI/2)/Math.PI,n=Math.sin(a),r=Math.cos(a),i=Math.max(.08,1.14-e*.78);return[o/2*r*Math.sin(t)*i,s/2*n,c/2*r*Math.cos(t)*i]}case`pebble`:{let r=n(t,a,o,s,c,.82+i(e.roundness)*.18,.82+i(e.roundness)*.2),l=1+.035*Math.cos(3*t)*Math.cos(a);return[r[0]*l,r[1],r[2]*l]}case`pyramid`:{let e=(a+Math.PI/2)/Math.PI,n=s/2-e*s,r=Math.max(.02,e),i=t+Math.PI/4,l=1/Math.max(Math.abs(Math.cos(i)),Math.abs(Math.sin(i)),.001);return[o/2*r*Math.sin(t)*l*.72,n,c/2*r*Math.cos(t)*l*.72]}case`flower`:{let e=Math.cos(a),n=.7+.3*(.5+.5*Math.cos(t*5)),r=.82+.18*Math.cos(a*2);return[o/2*e*Math.sin(t)*n,s/2*Math.sin(a)*n,c/2*e*Math.cos(t)*r]}case`disc`:return n(t,a,o,s,c,.9,.9)}},ee=(e,t)=>[e[0]-t[0],e[1]-t[1],e[2]-t[2]],T=([e,t,n])=>{let r=Math.hypot(e,t,n)||1;return[e/r,t/r,n/r]},te=(e,t,n)=>{let r=e.type===`cone`?-1:1;return T([r*(t[1]*n[2]-t[2]*n[1]),r*(t[2]*n[0]-t[0]*n[2]),r*(t[0]*n[1]-t[1]*n[0])])},ne=(e,t,n)=>{let r=5e-4;if(e.type===`cone`&&n>=Math.PI/2-r)return[0,-1,0];let i=w(e,t-r,n),a=w(e,t+r,n),o=w(e,t,Math.max(-Math.PI/2,n-r)),s=w(e,t,Math.min(Math.PI/2,n+r));return te(e,ee(a,i),ee(s,o))},E=(e,t)=>Math.sign(e)*Math.abs(e)**t,re=(e,t,n)=>{let r=e.width/2||1,i=e.height/2||1,a=e.depth/2||1;return T([E(t[0]/r,n-1)/r,E(t[1]/i,n-1)/i,E(t[2]/a,n-1)/a])},D=(e,t)=>re(e,t,a(e)),O=(e,t)=>{let n=s(e);if(Number.isFinite(n))return re(e,t,n);let r=[t[0]/(e.width/2||1),t[1]/(e.height/2||1),t[2]/(e.depth/2||1)],i=r.reduce((e,t,n)=>Math.abs(t)>Math.abs(r[e])?n:e,0);return[i===0?Math.sign(r[0]):0,i===1?Math.sign(r[1]):0,i===2?Math.sign(r[2]):0]},ie=(e,t,n,r,i)=>{let a=e.width/2||1,o=e.height/2||1,s=e.depth/2||1;if(!Number.isFinite(r)){let r=[Math.max(-a,Math.min(a,t)),Math.max(-o,Math.min(o,n)),s];return{point:r,normal:i(e,r)}}let c=Math.max(-1,Math.min(1,n/o)),l=Math.max(0,1-Math.abs(c)**r)**(1/r),u=Math.max(-a*l,Math.min(a*l,t)),d=u/a,f=Math.max(0,1-Math.abs(d)**r-Math.abs(c)**r)**(1/r),p=[u,c*o,s*f];return{point:p,normal:i(e,p)}},k=(e,t,n,r,i,a=0)=>{let o=t-a,s=Math.max(0,1-(e/(n||1))**2-(o/(r||1))**2),c=i*Math.sqrt(s);return{point:[e,t,c],normal:T([e/(n*n||1),o/(r*r||1),c/(i*i||1)])}},A=(e,t,n,r,i)=>{let a=e.width/2||1,o=e.depth/2||1,s=Math.max(0,Math.min(1,.5+i*(n/e.height))),c=b(e,s,r),l=a*c,u=o*c,d=Math.max(-l,Math.min(l,t)),f=l>0?Math.max(0,1-(d/l)**2):0,p=u*Math.sqrt(f),m=1e-4,h=Math.max(0,s-m),g=Math.min(1,s+m),_=b(e,h,r),v=(b(e,g,r)-_)/(g-h||1),y=Math.max(Math.sqrt(f),1e-4),x=-(o/a)*d/(l*y||1),S=i*o*v/(e.height*y||1);return{point:[d,n,p],normal:T([-x,-S,1])}},ae=(e,t,n)=>{let r=e.width/2||1,i=e.height/2||1,o=e.depth/2||1;switch(e.type){case`sphere`:case`mickey`:case`pebble`:case`disc`:return k(t,n,r,i,o);case`cube`:return ie(e,t,n,s(e),O);case`capsule`:{let e=Math.min(r,i),a=Math.max(0,i-e);return k(t,n,r,e,o,n<-a?-a:n>a?a:n)}case`cylinder`:return A(e,t,n,y,1);case`cursor`:{let r=C(e),i=A({...e,width:r.bodyWidth,height:r.bodyHeight,depth:r.bodyDepth},t,n-r.bodyCenterY,v,1);return{point:[i.point[0],i.point[1]+r.bodyCenterY,i.point[2]],normal:i.normal}}case`cone`:return A(e,t,n,S,-1);case`diamond`:return ie(e,t,n,a(e),D);default:return k(t,n,r,i,o)}},oe=(e,t,n)=>{let r=w(e,t,n);if(e.type===`sphere`||e.type===`mickey`||e.type===`pebble`||e.type===`disc`){let t=e.width/2||1,n=e.height/2||1,i=e.depth/2||1;return T([r[0]/(t*t),r[1]/(n*n),r[2]/(i*i)])}return e.type===`cylinder`&&e.roundness<=0&&(e.morphRoundness??0)<=0?T([Math.sin(t)/(e.width/2||1),0,Math.cos(t)/(e.depth/2||1)]):e.type===`diamond`?D(e,r):e.type===`cube`?O(e,r):ne(e,t,n)},se=(e,t,n)=>{let r=w(e,t,n);if(e.type===`sphere`||e.type===`mickey`||e.type===`pebble`||e.type===`disc`){let t=e.width/2||1,n=e.height/2||1,i=e.depth/2||1;return{point:r,normal:T([r[0]/(t*t),r[1]/(n*n),r[2]/(i*i)])}}return e.type===`cylinder`&&e.roundness<=0&&(e.morphRoundness??0)<=0?{point:r,normal:T([Math.sin(t)/(e.width/2||1),0,Math.cos(t)/(e.depth/2||1)])}:e.type===`diamond`?{point:r,normal:D(e,r)}:e.type===`cube`?{point:r,normal:O(e,r)}:{point:r,normal:ne(e,t,n)}},j=620,ce=14,le=[`headX`,`headY`,`headZ`,`widthLeft`,`widthRight`,`heightLeft`,`heightRight`,`spacing`,`positionXLeft`,`positionXRight`,`positionYLeft`,`positionYRight`,`leftAngle`,`rightAngle`,`perspective`],M=e=>e*Math.PI/180,ue=([e,t,n,r])=>{let i=Math.hypot(e,t,n,r)||1;return[e/i,t/i,n/i,r/i]},de=([e,t,n,r],[i,a,o,s])=>ue([e*i-t*a-n*o-r*s,e*a+t*i+n*s-r*o,e*o-t*s+n*i+r*a,e*s+t*o-n*a+r*i]),N=([e,t,n],r)=>{let i=r/2,a=Math.sin(i);return ue([Math.cos(i),e*a,t*a,n*a])},P=(e,t,n)=>{let r=N([1,0,0],e),i=N([0,1,0],t);return de(de(N([0,0,1],n),r),i)},F=([e,t,n,r],[i,a,o])=>{let s=2*(n*o-r*a),c=2*(r*i-t*o),l=2*(t*a-n*i);return[i+e*s+(n*l-r*c),a+e*c+(r*s-t*l),o+e*l+(t*c-n*s)]},fe=(e,t)=>{let n=e/2,r=t/2,i=Math.min(r,n),a=[],o=(e,t)=>{let n=Math.max(2,Math.ceil(Math.hypot(t[0]-e[0],t[1]-e[1])/1.5));for(let r=0;r<n;r+=1){let i=r/n;a.push([e[0]+(t[0]-e[0])*i,e[1]+(t[1]-e[1])*i])}},s=(e,t,n)=>{for(let r=0;r<ce;r+=1){let o=n+r/ce*(Math.PI/2);a.push([e+Math.cos(o)*i,t+Math.sin(o)*i])}};return o([-n+i,-r],[n-i,-r]),s(n-i,-r+i,-Math.PI/2),o([n,-r+i],[n,r-i]),s(n-i,r-i,0),o([n-i,r],[-n+i,r]),s(-n+i,r-i,Math.PI/2),o([-n,r-i],[-n,-r+i]),s(-n+i,-r+i,Math.PI),a},I=(e,t)=>{let n=j-e[2]*t,r=Math.abs(n)<1e-4?j/1e-4:j/n;return[e[0]*r,e[1]*r,e[2]]},L=(e,t=!0)=>e.length?`M${e[0][0].toFixed(2)} ${e[0][1].toFixed(2)}${e.slice(1).map(e=>`L${e[0].toFixed(2)} ${e[1].toFixed(2)}`).join(``)}${t?`Z`:``}`:``,pe=e=>({expression:e,orientation:P(M(e.headX),M(e.headY),M(e.headZ))}),me=24,he=25,ge=73,R=144,_e=33,ve=73,z=new Map,ye=new Map,be=new Map,B=e=>[e.type,e.width,e.height,e.depth,e.roundness,e.morphRoundness,e.tipRoundness,e.baseRoundness].map(e=>typeof e==`number`?e.toFixed(4):e).join(`:`),V=(e,t,n)=>(e.size>=me&&e.delete(e.keys().next().value),e.set(t,n),n),xe=(e,t,n)=>se(e,t,n),Se=(e,t)=>({point:I(F(e.orientation,t.point),e.expression.perspective),normal:F(e.orientation,t.normal)}),Ce=(e,t)=>{let n=e/120,r=t/120;return[120*Math.cos(r)*Math.sin(n),120*Math.sin(r)]},H=(e,t,n,r)=>{let[i,a]=Ce(n,r);return Se(e,ae(t,i,a))},we=(e,t,n,r,i={x:0,y:0})=>{let a=e.expression,o=n<0?`Left`:`Right`,s=a[`width${o}`],c=5+(a[`height${o}`]-5)*r,l=n*a.spacing/2+a[`positionX${o}`]+i.x,u=a[`positionY${o}`]+i.y,d=M(n<0?a.leftAngle:a.rightAngle);return fe(s,c).map(([n,r])=>{let i=n*Math.cos(d)-r*Math.sin(d),a=n*Math.sin(d)+r*Math.cos(d);return H(e,t,l+i,u+a)})},Te=e=>{let t=[],n=[];return e.forEach(({point:e,normal:r})=>{r[2]>0?n.push(e):n.length&&(t.push(n),n=[])}),n.length&&t.push(n),t.filter(e=>e.length>1).map(e=>L(e,!1)).join(``)},Ee=(e,t)=>{let n=B(t),r=be.get(n);if(!r){let e=[-60,-30,0,30,60].map(e=>Array.from({length:73},(n,r)=>xe(t,M(-180+r*5),M(e)))),i=Array.from({length:12},(e,t)=>-150+t*30).map(e=>Array.from({length:37},(n,r)=>xe(t,M(e),M(-90+r*5))));r=V(be,n,[...e,...i])}return r.map(t=>Te(t.map(t=>Se(e,t))))},U=e=>{let t=[...e].sort((e,t)=>e[0]-t[0]||e[1]-t[1]),n=(e,t,n)=>(t[0]-e[0])*(n[1]-e[1])-(t[1]-e[1])*(n[0]-e[0]),r=e=>{let t=[];return e.forEach(e=>{for(;t.length>=2&&n(t.at(-2),t.at(-1),e)<=0;)t.pop();t.push(e)}),t};return[...r(t).slice(0,-1),...r(t.reverse()).slice(0,-1)]},W=e=>{if(e.length<3)return L(e);let t=t=>e[(t+e.length)%e.length];return`M${e[0][0].toFixed(2)} ${e[0][1].toFixed(2)}${e.map((e,n)=>{let r=t(n-1),i=t(n+1),a=t(n+2),o=[e[0]+(i[0]-r[0])/6,e[1]+(i[1]-r[1])/6,e[2]],s=[i[0]-(a[0]-e[0])/6,i[1]-(a[1]-e[1])/6,i[2]];return`C${o[0].toFixed(2)} ${o[1].toFixed(2)} ${s[0].toFixed(2)} ${s[1].toFixed(2)} ${i[0].toFixed(2)} ${i[1].toFixed(2)}`}).join(``)}Z`},G=(e,t=7)=>e.flatMap((n,r)=>{let i=e[(r+1)%e.length],a=Math.max(1,Math.ceil(Math.hypot(i[0]-n[0],i[1]-n[1])/t));return Array.from({length:a},(e,t)=>{let r=t/a;return[n[0]+(i[0]-n[0])*r,n[1]+(i[1]-n[1])*r,n[2]+(i[2]-n[2])*r]})}),De=e=>e.length?e.length===1?`${e[0][0].toFixed(2)} ${e[0][1].toFixed(2)}`:e.slice(0,-1).map((t,n)=>{let r=e[Math.max(0,n-1)],i=e[n+1],a=e[Math.min(e.length-1,n+2)],o=t[0]+(i[0]-r[0])/6,s=t[1]+(i[1]-r[1])/6,c=i[0]-(a[0]-t[0])/6,l=i[1]-(a[1]-t[1])/6;return`C${o.toFixed(2)} ${s.toFixed(2)} ${c.toFixed(2)} ${l.toFixed(2)} ${i[0].toFixed(2)} ${i[1].toFixed(2)}`}).join(``):``,K=(e,t)=>I(F(e.orientation,t),e.expression.perspective),q=(e,t,n)=>Array.from({length:145},(r,i)=>{let a=i/R*Math.PI*2;return[e/2*Math.sin(a),n,t/2*Math.cos(a)]}),J=(e,t)=>{let n=B(t),r=z.get(n);return r||(r=Array.from({length:_e},(e,n)=>{let r=-Math.PI/2+n/32*Math.PI;return Array.from({length:ve},(e,n)=>w(t,-Math.PI+n/72*Math.PI*2,r))}).flat(),V(z,n,r)),W(G(U(r.map(t=>K(e,t)))))},Oe=(e,t)=>{if(t.roundness>0||(t.morphRoundness??0)>0)return J(e,t);let n=t.height/2;return W(G(U([...q(t.width,t.depth,-n),...q(t.width,t.depth,n)].map(t=>K(e,t)))))},ke=(e,t)=>{let n=C(t),r=n.bodyHeight/2;return W(G(U([...q(n.bodyWidth,n.bodyDepth,n.bodyCenterY-r),...q(n.bodyWidth,n.bodyDepth,n.bodyCenterY+r)].map(t=>K(e,t)))))},Ae=(e,t)=>{let n=C(t),r=K(e,[0,n.coneApexY,0]);return W(G(U([...q(t.width,t.depth,n.coneBaseY).map(t=>K(e,t)),r])))},je=(e,t)=>{if((t.morphRoundness??0)>0||(t.tipRoundness??0)>0||(t.baseRoundness??0)>0)return J(e,t);let n=K(e,[0,-t.height/2,0]),r=U([...q(t.width,t.depth,t.height/2).map(t=>K(e,t)),n]),i=r.findIndex(e=>Math.hypot(e[0]-n[0],e[1]-n[1])<.01);if(i<0)return W(r);let a=[...r.slice(i),...r.slice(0,i)].slice(1);return a.length<2?L(r):`M${n[0].toFixed(2)} ${n[1].toFixed(2)}L${a[0][0].toFixed(2)} ${a[0][1].toFixed(2)}${De(a)}L${n[0].toFixed(2)} ${n[1].toFixed(2)}Z`},Me=(e,t)=>{if(t.roundness>0)return J(e,t);let n=t.width/2,r=t.height/2,i=t.depth/2;return L(U([-1,1].flatMap(e=>[-1,1].flatMap(t=>[-1,1].map(a=>[e*n,t*r,a*i]))).map(t=>K(e,t))))},Ne=(e,t)=>{if(t.roundness>0)return J(e,t);let n=t.width/2,r=t.height/2,i=t.depth/2;return L(U([[-n,0,0],[n,0,0],[0,-r,0],[0,r,0],[0,0,-i],[0,0,i]].map(t=>K(e,t))))},Pe=(e,t,n,r,i)=>{let a=n+i,o=Math.hypot(n-i,r*2),s=(a+o)/2,c=(a-o)/2;return s<=0||c<=0?null:{centerX:e,centerY:t,majorRadius:Math.sqrt(s),minorRadius:Math.sqrt(c),rotation:Math.atan2(r*2,n-i)/2}},Y=({centerX:e,centerY:t,majorRadius:n,minorRadius:r,rotation:i})=>{let a=i*180/Math.PI,o=Math.cos(i)*n,s=Math.sin(i)*n,c=e+o,l=t+s,u=e-o,d=t-s;return`M${c.toFixed(2)} ${l.toFixed(2)}A${n.toFixed(2)} ${r.toFixed(2)} ${a.toFixed(2)} 0 1 ${u.toFixed(2)} ${d.toFixed(2)}A${n.toFixed(2)} ${r.toFixed(2)} ${a.toFixed(2)} 0 1 ${c.toFixed(2)} ${l.toFixed(2)}Z`},X=(e,t,n=[0,0,0])=>{let r=[F(e.orientation,[1,0,0]),F(e.orientation,[0,1,0]),F(e.orientation,[0,0,1])],i=F(e.orientation,n);if(Math.abs(e.expression.perspective)<1e-4){let e=r.reduce((e,n,r)=>e+n[0]*n[0]*t[r]*t[r],0),n=r.reduce((e,n,r)=>e+n[0]*n[1]*t[r]*t[r],0),a=r.reduce((e,n,r)=>e+n[1]*n[1]*t[r]*t[r],0);return Pe(i[0],i[1],e,n,a)}let a=t.map(e=>1/(e*e)),o=Array.from({length:3},(e,t)=>Array.from({length:3},(e,n)=>r.reduce((e,r,i)=>e+r[t]*a[i]*r[n],0))),s=j/e.expression.perspective,c=[-i[0],-i[1],s-i[2]],l=[o[0][0]*c[0]+o[0][1]*c[1]+o[0][2]*c[2],o[1][0]*c[0]+o[1][1]*c[1]+o[1][2]*c[2],o[2][0]*c[0]+o[2][1]*c[1]+o[2][2]*c[2]],u=c[0]*l[0]+c[1]*l[1]+c[2]*l[2]-1,d=[l[0],l[1],-s*l[2]],f=[[o[0][0],o[0][1],-s*o[0][2]],[o[1][0],o[1][1],-s*o[1][2]],[-s*o[2][0],-s*o[2][1],s*s*o[2][2]]],p=Array.from({length:3},(e,t)=>Array.from({length:3},(e,n)=>d[t]*d[n]-u*f[t][n])),m=p[0][0]*p[1][1]-p[0][1]*p[0][1];if(Math.abs(m)<1e-12)return null;let h=-(p[1][1]*p[0][2]-p[0][1]*p[1][2])/m,g=(p[0][1]*p[0][2]-p[0][0]*p[1][2])/m,_=-(p[2][2]+p[0][2]*h+p[1][2]*g);if(Math.abs(_)<1e-12)return null;let v=p[0][0]/_,y=p[0][1]/_,b=p[1][1]/_,x=v*b-y*y;return x<=0?null:Pe(h,g,b/x,-y/x,v/x)},Fe=(e,t)=>{let n=X(e,[t.width/2,t.height/2,t.depth/2]),r=t.width===t.height&&t.height===t.depth;if(n&&r){let e=(n.majorRadius+n.minorRadius)/2;return Y({centerX:0,centerY:0,majorRadius:e,minorRadius:e,rotation:0})}return n?Y(n):null},Ie=(e,t)=>{if(t.type!==`mickey`)return[];let n=Math.min(t.width,t.height)*.23,r=Math.min(n,t.depth*.29),i=t.width*.37,a=-t.height*.39,o=-t.depth*.12,s=[n,n,r];return[-1,1].map(t=>X(e,s,[t*i,a,o])).filter(e=>e!==null).map(Y)},Le=(e,t)=>t.type===`mickey`?Ie(e,t):t.type===`cursor`?[Ae(e,t)]:[],Re=e=>Array.from({length:R},(t,n)=>{let r=n/R*Math.PI*2,i=Math.cos(r)*e.majorRadius,a=Math.sin(r)*e.minorRadius;return[e.centerX+i*Math.cos(e.rotation)-a*Math.sin(e.rotation),e.centerY+i*Math.sin(e.rotation)+a*Math.cos(e.rotation),0]}),ze=e=>{if(e.length<3)return L(e);let t=e.map((t,n)=>{let r=e[(n+1)%e.length];return Math.hypot(r[0]-t[0],r[1]-t[1])}),n=[...t].sort((e,t)=>e-t),r=n[Math.floor(n.length/2)]||1,i=Math.max(8,r*3.5),a=t.map(e=>e>i);return`M${e[0][0].toFixed(2)} ${e[0][1].toFixed(2)}${e.map((t,n)=>{let r=(n+1)%e.length,i=e[r];if(a[n])return`L${i[0].toFixed(2)} ${i[1].toFixed(2)}`;let o=a[(n-1+e.length)%e.length]?t:e[(n-1+e.length)%e.length],s=a[r]?i:e[(n+2)%e.length],c=t[0]+(i[0]-o[0])/6,l=t[1]+(i[1]-o[1])/6,u=i[0]-(s[0]-t[0])/6,d=i[1]-(s[1]-t[1])/6;return`C${c.toFixed(2)} ${l.toFixed(2)} ${u.toFixed(2)} ${d.toFixed(2)} ${i[0].toFixed(2)} ${i[1].toFixed(2)}`}).join(``)}Z`},Be=(e,t)=>{let n=t.width/2,r=Math.min(n,t.height/2),i=t.depth/2,a=Math.max(0,(t.height-r*2)/2),o=[n,r,i],s=X(e,o,[0,a,0]),c=X(e,o,[0,-a,0]);return!s||!c?null:ze(U([...Re(s),...Re(c)]))},Ve=(e,t)=>{if(t.type===`sphere`||t.type===`mickey`){let n=Fe(e,t);if(n)return n}if(t.type===`capsule`){let n=Be(e,t);if(n)return n}if(t.type===`cylinder`)return Oe(e,t);if(t.type===`cursor`)return ke(e,t);if(t.type===`cone`)return je(e,t);if(t.type===`cube`)return Me(e,t);if(t.type===`diamond`)return Ne(e,t);let n=B(t),r=z.get(n);return r||(r=Array.from({length:he},(e,n)=>{let r=-Math.PI/2+n/24*Math.PI;return Array.from({length:ge},(e,n)=>w(t,-Math.PI+n/72*Math.PI*2,r))}).flat(),V(z,n,r)),L(U(r.map(t=>I(F(e.orientation,t),e.expression.perspective))))},He=(e,t)=>{let n=B(t.surface),r=ye.get(n);r||(r=Array.from({length:17},(e,n)=>{let r=-Math.PI/2+n/16*Math.PI;return Array.from({length:49},(e,n)=>{let i=-Math.PI+n/48*Math.PI*2;return w(t.surface,i,r)})}).flat(),V(ye,n,r));let i=P(M(t.rotation[0]),M(t.rotation[1]),M(t.rotation[2])),a=U(r.map(n=>{let r=F(i,n),a=[r[0]+t.position[0],r[1]+t.position[1],r[2]+t.position[2]];return I(F(e.orientation,a),e.expression.perspective)}));return(t.surface.type===`cube`||t.surface.type===`diamond`)&&t.surface.roundness<=0?L(a):W(G(a))},Ue=.1,We=(e,t)=>{let n=P(M(t.rotation[0]),M(t.rotation[1]),M(t.rotation[2])),r=[[1,0,0],[0,1,0],[0,0,1]].map(t=>F(e.orientation,F(n,t))[2]);return Math.hypot(r[0]*(t.surface.width/2),r[1]*(t.surface.height/2),r[2]*(t.surface.depth/2))},Ge=(e,t)=>{let n=t.map(t=>{let n=F(e.orientation,t.position)[2];return{id:t.id,path:He(e,t),depth:n,front:n>We(e,t)*Ue}}).sort((e,t)=>e.depth-t.depth);return{backPaths:n.filter(e=>!e.front).map(e=>e.path),frontPaths:n.filter(e=>e.front).map(e=>e.path),backNodeIds:n.filter(e=>!e.front).map(e=>e.id),frontNodeIds:n.filter(e=>e.front).map(e=>e.id)}},Ke=(e,t,n=`none`,r=1)=>{if(!n||n===`none`)return{path:``,visible:!1};let i=20*(r||1);if(n===`oMouth`||n===`kiss`){let i=[],a=0,o=(n===`kiss`?8:13)*(r||1),s=(n===`kiss`?6.5:12)*(r||1);for(let n=0;n<=20;n+=1){let r=n/20*Math.PI*2,c=H(e,t,Math.cos(r)*o,22+Math.sin(r)*s);i.push(c.point),a+=c.normal[2]}return i.length?{path:`${L(i)}Z`,visible:a>-.1}:{path:``,visible:!1}}let a=[],o=0;for(let r=0;r<15;r+=1){let s=r/14*2-1,c=s*i*(n===`grin`?1.2:1),l=n===`smile`?-7:n===`openSmile`||n===`grin`?-12:n===`frown`?7:0,u=n===`cat`?-5*Math.abs(Math.sin(s*Math.PI))+2.5:0,d=n===`smirk`?-6*(s+1)/2:0,f=H(e,t,c,22+((1-s*s)*l+u+d));a.push(f.point),o+=f.normal[2]}return a.length<2?{path:``,visible:!1}:{path:L(a,!1),visible:o>-.1}},qe=(e,t)=>{if(t.pattern!==`book`)return[];let n=1e-5,r=Math.PI/2-.001,i=e=>.4,a=({u:r,v:i})=>{let a=F(e.orientation,w(t,r,i)),o=F(e.orientation,oe(t,r,i)),s=e.expression.perspective;if(Math.abs(s)<1e-6)return o[2]-n;let c=j/s,l=-a[0],u=-a[1],d=c-a[2],f=Math.hypot(l,u,d)||1;return(o[0]*l+o[1]*u+o[2]*d)/f-n},o=(e,t)=>{let n=a(e)>=0?e:t,r=a(e)>=0?t:e;for(let e=0;e<12;e+=1){let e={u:(n.u+r.u)/2,v:(n.v+r.v)/2};a(e)>=0?n=e:r=e}return n},s=e=>{if(e.length<3)return[];let t=[];for(let n=0;n<e.length;n+=1){let r=e[n],i=e[(n+1)%e.length],s=a(r)>=0,c=a(i)>=0;s&&c?t.push(i):s&&!c?t.push(o(r,i)):!s&&c&&t.push(o(r,i),i)}return t},c=n=>{let r=s(n);if(r.length<3)return``;let i=r.map(({u:n,v:r})=>I(F(e.orientation,w(t,n,r)),e.expression.perspective)),a=`M${i[0][0].toFixed(2)} ${i[0][1].toFixed(2)}`;for(let e=1;e<i.length;e+=1)a+=` L${i[e][0].toFixed(2)} ${i[e][1].toFixed(2)}`;return`${a}Z`},l=(e,t,n)=>{let r=``;for(let i=0;i<144;i+=1){let a=-Math.PI+i/144*Math.PI*2,o=-Math.PI+(i+1)/144*Math.PI*2,s=e(a),l=e(o),u=t(a),d=t(o);for(let e=0;e<n;e+=1){let t=e/n,i=(e+1)/n,f=s+(u-s)*t,p=l+(d-l)*t,m=l+(d-l)*i,h=s+(u-s)*i;r+=c([{u:a,v:f},{u:o,v:p},{u:o,v:m},{u:a,v:h}])}}return r},u=l(i,()=>r,14),d=l(i,e=>i(e)+.1,2),f=l(e=>i(e)-.07,i,2);return[{path:u,fill:`#1d4ed8`,opacity:1},{path:d,fill:`#3b82f6`,opacity:1},{path:f,fill:`#93c5fd`,opacity:.92}].filter(e=>!!e.path)},Je=(e,t,n=1,r={})=>{let i=we(e,t,-1,n,r.eyeOffset),a=we(e,t,1,n,r.eyeOffset),o=i.map(e=>e.point),s=a.map(e=>e.point),c=r.bodyNodes??[],l=Ge(e,c),u=Le(e,t),d=t.pattern===`book`||(e.expression.mouth||`none`)===`none`?{path:``,visible:!1}:Ke(e,t,e.expression.mouth||`none`,e.expression.mouthScale||1),f=qe(e,t),p={};return c.forEach(e=>{p[e.id]={color:e.color,colorTo:e.colorTo,gradientType:e.gradientType,opacity:e.opacity,material:e.material}}),{backPaths:[...u,...l.backPaths],frontPaths:l.frontPaths,backNodeIds:[...u.map(()=>null),...l.backNodeIds],frontNodeIds:l.frontNodeIds,headPath:Ve(e,t),leftPath:L(o),rightPath:L(s),leftVisible:i.reduce((e,t)=>e+t.normal[2],0)>0,rightVisible:a.reduce((e,t)=>e+t.normal[2],0)>0,mouthPath:d.path,mouthVisible:d.visible,decals:f,nodeStyles:p,wirePaths:r.includeWire===!1?[]:Ee(e,t)}},Ye=e=>e*e*(3-2*e),Z=e=>{let t=Math.sin(e*127.1+311.7)*43758.5453;return(t-Math.floor(t))*2-1},Xe=e=>e.headX*.71+e.headY*1.13+e.headZ*1.37,Q=17.29,$=(e,t,n,r)=>{let i=e/r,a=Math.floor(i),o=Ye(i-a),s=Z(a*3+t+n);return s+(Z((a+1)*3+t+n)-s)*o},Ze=(e,t,n)=>{let r=1100;if(e<=0)return 0;let i=Math.floor(e/r),a=(e-i*r)/140,o=Ye(Math.min(a,1)),s=i===0?0:Z((i-1)*2+t+n);return s+(Z(i*2+t+n)-s)*o},Qe=e=>e.eyeMotion!==`none`||e.bodyMotion!==`none`,$e=(e,t,n=1)=>{let r=Xe(e);if(e.bodyMotion===`slowDrift`)return{x:$(t,3,r,2900)*1.45*n,y:$(t,4,r,3700)*1.1*n};if(e.bodyMotion===`breathe`){let e=t/1e3;return{x:0,y:Math.sin(e*1.7)*1.15*n}}if(e.bodyMotion===`bob`){let e=t/1e3;return{x:0,y:Math.sin(e*3.2)*2.2*n}}if(e.bodyMotion===`bounce`){let e=t/1e3;return{x:Math.sin(e*2.4)*.9*n,y:-Math.abs(Math.sin(e*3.6))*4.2*n}}if(e.bodyMotion===`sway`){let e=t/1e3;return{x:Math.sin(e*1.8)*2.1*n,y:Math.cos(e*1.4)*.55*n}}if(e.bodyMotion===`float`)return{x:$(t,5,r,4200)*2.2*n,y:$(t,6,r,5100)*2.5*n};if(e.bodyMotion===`shake`){let e=t/1e3;return{x:(Math.sin(e*31)+Math.sin(e*53)*.45)*1.35*n,y:(Math.sin(e*37)+Math.sin(e*61)*.4)*1.1*n}}return{x:0,y:0}},et=(e,t,n=1)=>{if(e.eyeMotion===`microSaccades`)return{x:Ze(t,0,Q)*1.5*n,y:Ze(t,1,Q)*.9*n};if(e.eyeMotion===`wander`)return{x:$(t,9,Q,2100)*3.2*n,y:$(t,10,Q,2700)*1.8*n};if(e.eyeMotion===`lookAround`){let e=t/1e3;return{x:Math.sin(e*1.8)*4.2*n,y:Math.sin(e*.9+.7)*1.4*n}}if(e.eyeMotion===`focusPulse`){let e=t/1e3;return{x:Math.sin(e*5.2)*.35*n,y:Math.cos(e*4.8)*.25*n}}if(e.eyeMotion===`shake`){let e=t/1e3;return{x:(Math.sin(e*47)+Math.sin(e*71)*.45)*1.2*n,y:(Math.sin(e*59)+Math.sin(e*83)*.4)*.8*n}}return{x:0,y:0}},tt=(e,t,n=1)=>{let r={...e},i=Xe(e);if(e.bodyMotion===`slowDrift`)r.headX+=$(t,0,i,2600)*.8*n,r.headY+=$(t,1,i,3300)*1.15*n,r.headZ+=$(t,2,i,4100)*.45*n;else if(e.bodyMotion===`breathe`){let e=t/1e3;r.headX+=Math.sin(e*1.7)*.45*n}else if(e.bodyMotion===`bob`){let e=t/1e3;r.headX+=Math.sin(e*3.2)*1.4*n}else if(e.bodyMotion===`bounce`){let e=t/1e3;r.headZ+=Math.sin(e*3.6)*2.2*n}else if(e.bodyMotion===`sway`){let e=t/1e3;r.headZ+=Math.sin(e*1.8)*3.4*n,r.headY+=Math.sin(e*.9)*1.2*n}else if(e.bodyMotion===`float`)r.headX+=$(t,7,i,4200)*1.25*n,r.headY+=$(t,8,i,5100)*1.8*n,r.headZ+=$(t,9,i,4700)*.9*n;else if(e.bodyMotion===`shake`){let e=t/1e3;r.headX+=(Math.sin(e*31)+Math.sin(e*53)*.45)*1.15*n,r.headY+=(Math.sin(e*37)+Math.sin(e*61)*.4)*1.35*n,r.headZ+=Math.sin(e*43)*.7*n}return r};return e.ambientBodyOffset=$e,e.ambientEyeOffset=et,e.applyAmbientBodyMotion=tt,e.applyAmbientMotion=(e,t,n=1)=>{let r=tt(e,t,n),i=et(e,t,n);return r.positionXLeft+=i.x,r.positionXRight+=i.x,r.positionYLeft+=i.y,r.positionYRight+=i.y,r},e.expressionFields=le,e.hasAmbientMotion=Qe,e.poseFromExpression=pe,e.renderAvatar=Je,e})({});

  const NEBY_DATA = {"avatar":{"name":"Neby","surface":{"type":"cube","width":240,"height":240,"depth":215,"roundness":2,"pattern":"book"},"bodyNodes":[],"colors":{"body":"#cce2ff","eyes":"#0a1c4d"}},"expressions":{"expression-00":{"id":"expression-00","headX":7.3,"headY":27.8,"headZ":-16.1,"widthLeft":22.501171874999997,"widthRight":22.501171874999997,"heightLeft":42.377734374999996,"heightRight":42.377734374999996,"spacing":54.3,"positionXLeft":0,"positionXRight":0,"positionYLeft":-20.5,"positionYRight":-20.5,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-01":{"id":"expression-01","headX":-15.057812500000004,"headY":0.14296874999999964,"headZ":-14.549218750000001,"widthLeft":22.401171875,"widthRight":22.401171875,"heightLeft":54.5703125,"heightRight":54.5703125,"spacing":57.7,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-05":{"id":"expression-05","headX":-16.528515625,"headY":-3.7679687499999996,"headZ":-13.7296875,"widthLeft":23.090625,"widthRight":49.924609375,"heightLeft":57.6796875,"heightRight":12.431640625,"spacing":56.3,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-06":{"id":"expression-06","headX":-4.232421875000001,"headY":14.362109375000003,"headZ":11.204296875,"widthLeft":22.066796874999998,"widthRight":22.066796874999998,"heightLeft":39.59921875,"heightRight":39.59921875,"spacing":50.9,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-12":{"id":"expression-12","headX":-19.20859375,"headY":15.2,"headZ":11.8,"widthLeft":52.084765625,"widthRight":53.11410881916995,"heightLeft":51.467159708498066,"heightRight":52.187699944416956,"spacing":69.5,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-03":{"id":"expression-03","headX":2.9468749999999986,"headY":-16.051171875,"headZ":-20.916015625,"widthLeft":51.68336723153048,"widthRight":51.68336723153048,"heightLeft":51.74054108796297,"heightRight":51.74054108796297,"spacing":70.9,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-04":{"id":"expression-04","headX":3.4,"headY":13.22578125,"headZ":8.976953125,"widthLeft":51.775,"widthRight":51.775,"heightLeft":13.02734375,"heightRight":13.02734375,"spacing":63.872265625,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-07":{"id":"expression-07","headX":8.063671874999999,"headY":17.626562500000002,"headZ":-11.116796874999999,"widthLeft":20.908203124999996,"widthRight":20.908203124999996,"heightLeft":40.40078125,"heightRight":40.40078125,"spacing":52.059765625,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":-30.865625,"rightAngle":28.781640625,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-08":{"id":"expression-08","headX":-12.303515625,"headY":-17.601171875,"headZ":5.9109375,"widthLeft":20.605859374999994,"widthRight":20.605859374999994,"heightLeft":47.769921874999994,"heightRight":47.769921874999994,"spacing":54.9,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":23.523046875000002,"rightAngle":-24.042578125000002,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-09":{"id":"expression-09","headX":-20.058203125,"headY":12.607421875,"headZ":-12.7,"widthLeft":42.5,"widthRight":22.1,"heightLeft":41.8,"heightRight":22.2,"spacing":61.7,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-10":{"id":"expression-10","headX":1.43359375,"headY":6.194140624999999,"headZ":10.56015625,"widthLeft":23.836718749999996,"widthRight":23.836718749999996,"heightLeft":58.130078125,"heightRight":58.130078125,"spacing":56.8,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-11":{"id":"expression-11","headX":-2.092968750000001,"headY":-15.899609374999999,"headZ":-14.469921875,"widthLeft":34.20086765973213,"widthRight":34.20086765973213,"heightLeft":85.330859375,"heightRight":83.17775668160692,"spacing":59.414453125,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-13":{"id":"expression-13","headX":-8.752343750000001,"headY":-8.743359375,"headZ":-10.773828125000001,"widthLeft":56.133984375,"widthRight":56.133984375,"heightLeft":15.5,"heightRight":15.15546875,"spacing":69.276171875,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-02":{"id":"expression-02","headX":-15.287109375000002,"headY":15.006640625,"headZ":12.787890625,"widthLeft":31.253906249999996,"widthRight":31.253906249999996,"heightLeft":76.720703125,"heightRight":76.720703125,"spacing":68.7,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-14":{"id":"expression-14","headX":3.5292968750000004,"headY":-7.0765625,"headZ":9.830078125,"widthLeft":24.306250000000002,"widthRight":48.92421875000001,"heightLeft":59.281640624999994,"heightRight":13.408203124999996,"spacing":62.218359375,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-15":{"id":"expression-15","headX":0.31914062500000184,"headY":35.307421874999996,"headZ":-10.904296875,"widthLeft":22.4609375,"widthRight":22.4609375,"heightLeft":39.820703125,"heightRight":39.820703125,"spacing":53.9,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-16":{"id":"expression-16","headX":-14.750781250000001,"headY":-19.350000000000005,"headZ":5.631640624999998,"widthLeft":19.602343750000003,"widthRight":19.602343750000003,"heightLeft":48.63984375,"heightRight":48.63984375,"spacing":55.1,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":-27.606640625,"rightAngle":26.1484375,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-17":{"id":"expression-17","headX":-4.3953125,"headY":14.07265625,"headZ":-16.126171874999997,"widthLeft":19.045145681988206,"widthRight":19.045145681988206,"heightLeft":43.370703125,"heightRight":43.370703125,"spacing":51.731249999999996,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":26.2921875,"rightAngle":-20.249218750000004,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-18":{"id":"expression-18","headX":6.585546875,"headY":4.737109375000001,"headZ":12.840234374999998,"widthLeft":42.1,"widthRight":22.2,"heightLeft":41.7,"heightRight":22.1,"spacing":60.4,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-19":{"id":"expression-19","headX":-6.077734375000001,"headY":-11.03515625,"headZ":-13.965625000000001,"widthLeft":23.045703125,"widthRight":23.045703125,"heightLeft":58.68515625,"heightRight":58.68515625,"spacing":56.2,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-20":{"id":"expression-20","headX":-17.127734375000003,"headY":18.070703124999998,"headZ":13.891796875,"widthLeft":35.452734375,"widthRight":35.452734375,"heightLeft":79.104296875,"heightRight":79.104296875,"spacing":70.8,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-21":{"id":"expression-21","headX":-5.428125,"headY":-11.71328125,"headZ":-13.472265625000002,"widthLeft":51.4,"widthRight":50.5,"heightLeft":50.1,"heightRight":49.4,"spacing":69,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-22":{"id":"expression-22","headX":10.292578125,"headY":3.39921875,"headZ":7.583203125,"widthLeft":55.672265625,"widthRight":55.672265625,"heightLeft":14.616015625,"heightRight":14.616015625,"spacing":68.416796875,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-23":{"id":"expression-23","headX":-17.8,"headY":10,"headZ":-10.894921875,"widthLeft":23.969921875,"widthRight":53.56328125,"heightLeft":55.89296875,"heightRight":13.333593750000002,"spacing":59.94375,"positionXLeft":0,"positionXRight":0,"positionYLeft":-9.8,"positionYRight":-9.8,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-24":{"id":"expression-24","headX":7.131640624999998,"headY":7.7828124999999995,"headZ":3.935546874999999,"widthLeft":21.5,"widthRight":23.2,"heightLeft":32,"heightRight":33.5,"spacing":51.2,"positionXLeft":0,"positionXRight":0,"positionYLeft":40,"positionYRight":40,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none"},"expression-3d2bed26-f97c-477d-922f-77600cb10e92":{"id":"expression-3d2bed26-f97c-477d-922f-77600cb10e92","headX":10.473974503042374,"headY":5.087293619785961,"headZ":4.698252132317348,"widthLeft":27.126562499999995,"widthRight":27.126562499999995,"heightLeft":63.028125,"heightRight":63.028125,"spacing":68.7,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":-36.244531249999994,"rightAngle":27.730078125000002,"perspective":1,"eyeMotion":"none","bodyMotion":"shake","bodyColor":"#ba3636","eyeColor":"#610000"},"expression-5220eaee-32fe-4bd8-ad31-432189534cc8":{"id":"expression-5220eaee-32fe-4bd8-ad31-432189534cc8","headX":-12.303515625,"headY":-17.601171875,"headZ":5.9109375,"widthLeft":20.605859374999994,"widthRight":20.605859374999994,"heightLeft":47.769921874999994,"heightRight":47.769921874999994,"spacing":54.9,"positionXLeft":0,"positionXRight":0,"positionYLeft":0,"positionYRight":0,"leftAngle":23.523046875000002,"rightAngle":-24.042578125000002,"perspective":1,"eyeMotion":"shake","bodyMotion":"slowDrift","bodyColor":"#adc3ff"},"joy":{"id":"joy","headX":5,"headY":-5,"headZ":-2,"widthLeft":30,"widthRight":30,"heightLeft":18,"heightRight":18,"spacing":38,"positionXLeft":0,"positionXRight":0,"positionYLeft":-2,"positionYRight":-2,"leftAngle":8,"rightAngle":-8,"perspective":1,"eyeMotion":"none","bodyMotion":"bob","mouth":"grin","mouthScale":1.15},"soft-smile":{"id":"soft-smile","headX":2,"headY":0,"headZ":0,"widthLeft":24,"widthRight":24,"heightLeft":30,"heightRight":30,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"breathe","mouth":"smile","mouthScale":0.9},"wink":{"id":"wink","headX":0,"headY":-10,"headZ":-6,"widthLeft":26,"widthRight":27,"heightLeft":8,"heightRight":34,"spacing":38,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":-8,"rightAngle":6,"perspective":1,"eyeMotion":"none","bodyMotion":"sway","mouth":"smirk","mouthScale":1},"love":{"id":"love","headX":4,"headY":0,"headZ":0,"widthLeft":31,"widthRight":31,"heightLeft":28,"heightRight":28,"spacing":39,"positionXLeft":0,"positionXRight":0,"positionYLeft":-3,"positionYRight":-3,"leftAngle":10,"rightAngle":-10,"perspective":1,"eyeMotion":"none","bodyMotion":"float","mouth":"smile","mouthScale":1.05,"bodyColor":"#ff6f91"},"smug":{"id":"smug","headX":0,"headY":14,"headZ":8,"widthLeft":27,"widthRight":19,"heightLeft":19,"heightRight":16,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-4,"positionYRight":-1,"leftAngle":-8,"rightAngle":10,"perspective":1,"eyeMotion":"none","bodyMotion":"none","mouth":"smirk","mouthScale":1},"skeptical":{"id":"skeptical","headX":0,"headY":-13,"headZ":-5,"widthLeft":24,"widthRight":20,"heightLeft":20,"heightRight":13,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-3,"positionYRight":1,"leftAngle":12,"rightAngle":-12,"perspective":1,"eyeMotion":"focusPulse","bodyMotion":"none","mouth":"flat","mouthScale":1},"side-eye":{"id":"side-eye","headX":0,"headY":8,"headZ":0,"widthLeft":23,"widthRight":23,"heightLeft":21,"heightRight":21,"spacing":35,"positionXLeft":11,"positionXRight":11,"positionYLeft":-3,"positionYRight":-3,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none","mouth":"flat","mouthScale":1},"focus":{"id":"focus","headX":-4,"headY":0,"headZ":0,"widthLeft":20,"widthRight":20,"heightLeft":22,"heightRight":22,"spacing":32,"positionXLeft":0,"positionXRight":0,"positionYLeft":-5,"positionYRight":-5,"leftAngle":-5,"rightAngle":5,"perspective":1,"eyeMotion":"focusPulse","bodyMotion":"breathe","mouth":"flat","mouthScale":1},"scan-left":{"id":"scan-left","headX":0,"headY":-10,"headZ":0,"widthLeft":23,"widthRight":23,"heightLeft":29,"heightRight":29,"spacing":35,"positionXLeft":-13,"positionXRight":-13,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"lookAround","bodyMotion":"none","mouth":"none","mouthScale":1},"scan-right":{"id":"scan-right","headX":0,"headY":10,"headZ":0,"widthLeft":23,"widthRight":23,"heightLeft":29,"heightRight":29,"spacing":35,"positionXLeft":13,"positionXRight":13,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"lookAround","bodyMotion":"none","mouth":"none","mouthScale":1},"talk-a":{"id":"talk-a","headX":0,"headY":0,"headZ":0,"widthLeft":24,"widthRight":24,"heightLeft":31,"heightRight":31,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"microSaccades","bodyMotion":"none","mouth":"openSmile","mouthScale":0.8},"talk-b":{"id":"talk-b","headX":0,"headY":0,"headZ":2,"widthLeft":23,"widthRight":23,"heightLeft":28,"heightRight":28,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none","mouth":"oMouth","mouthScale":0.72},"talk-c":{"id":"talk-c","headX":0,"headY":0,"headZ":-2,"widthLeft":25,"widthRight":25,"heightLeft":27,"heightRight":27,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"none","mouth":"smile","mouthScale":0.78},"gasp":{"id":"gasp","headX":7,"headY":0,"headZ":0,"widthLeft":33,"widthRight":33,"heightLeft":47,"heightRight":47,"spacing":40,"positionXLeft":0,"positionXRight":0,"positionYLeft":-5,"positionYRight":-5,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"bounce","mouth":"oMouth","mouthScale":1.1},"panic":{"id":"panic","headX":7,"headY":0,"headZ":5,"widthLeft":31,"widthRight":31,"heightLeft":48,"heightRight":48,"spacing":42,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":-14,"rightAngle":14,"perspective":1,"eyeMotion":"shake","bodyMotion":"shake","mouth":"oMouth","mouthScale":1},"sad-deep":{"id":"sad-deep","headX":-8,"headY":0,"headZ":0,"widthLeft":22,"widthRight":22,"heightLeft":20,"heightRight":20,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":4,"positionYRight":4,"leftAngle":-12,"rightAngle":12,"perspective":1,"eyeMotion":"none","bodyMotion":"slowDrift","mouth":"frown","mouthScale":1},"angry-hot":{"id":"angry-hot","headX":-5,"headY":0,"headZ":0,"widthLeft":25,"widthRight":25,"heightLeft":15,"heightRight":15,"spacing":32,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":18,"rightAngle":-18,"perspective":1,"eyeMotion":"none","bodyMotion":"shake","mouth":"frown","mouthScale":1,"bodyColor":"#ef5350"},"sleepy":{"id":"sleepy","headX":-6,"headY":0,"headZ":0,"widthLeft":24,"widthRight":24,"heightLeft":8,"heightRight":8,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":1,"positionYRight":1,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"breathe","mouth":"flat","mouthScale":1},"kiss":{"id":"kiss","headX":4,"headY":0,"headZ":-6,"widthLeft":25,"widthRight":25,"heightLeft":20,"heightRight":20,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":7,"rightAngle":-7,"perspective":1,"eyeMotion":"none","bodyMotion":"sway","mouth":"kiss","mouthScale":0.9},"cat-cute":{"id":"cat-cute","headX":3,"headY":0,"headZ":0,"widthLeft":30,"widthRight":30,"heightLeft":31,"heightRight":31,"spacing":38,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"bob","mouth":"cat","mouthScale":0.8},"dizzy":{"id":"dizzy","headX":0,"headY":0,"headZ":12,"widthLeft":19,"widthRight":29,"heightLeft":17,"heightRight":34,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":35,"rightAngle":-32,"perspective":1,"eyeMotion":"wander","bodyMotion":"sway","mouth":"oMouth","mouthScale":1},"notification":{"id":"notification","headX":6,"headY":0,"headZ":0,"widthLeft":31,"widthRight":31,"heightLeft":40,"heightRight":40,"spacing":39,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"focusPulse","bodyMotion":"bounce","mouth":"smile","mouthScale":1},"success":{"id":"success","headX":6,"headY":0,"headZ":-3,"widthLeft":28,"widthRight":28,"heightLeft":19,"heightRight":19,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"none","bodyMotion":"bounce","mouth":"grin","mouthScale":1,"bodyColor":"#39c98a"},"error":{"id":"error","headX":-5,"headY":0,"headZ":4,"widthLeft":24,"widthRight":24,"heightLeft":14,"heightRight":14,"spacing":35,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":14,"rightAngle":-14,"perspective":1,"eyeMotion":"none","bodyMotion":"shake","mouth":"frown","mouthScale":1,"bodyColor":"#ff5f6d"},"confetti":{"id":"confetti","headX":8,"headY":-4,"headZ":0,"widthLeft":32,"widthRight":32,"heightLeft":22,"heightRight":22,"spacing":40,"positionXLeft":0,"positionXRight":0,"positionYLeft":-7,"positionYRight":-7,"leftAngle":0,"rightAngle":0,"perspective":1,"eyeMotion":"microSaccades","bodyMotion":"bounce","mouth":"grin","mouthScale":1.2}},"animations":{"sleeping":{"name":"sleeping","description":"Yeux presque fermés, respiration lente et expression de sommeil.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":4800,"minIntervalMs":6500,"maxIntervalMs":9500,"durationMs":420},"steps":[{"expressionId":"expression-13","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-22","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-04","holdMs":3600,"transitionMs":500,"transition":"smooth"}]},"waking":{"name":"waking","description":"Séquence courte de réveil avant retour vers une expression neutre.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1200,"minIntervalMs":1800,"maxIntervalMs":3600,"durationMs":220},"steps":[{"expressionId":"expression-13","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"idle":{"name":"idle","description":"Micro-mouvements lents, expressions 00 et 08, clignement rare.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2600,"minIntervalMs":3400,"maxIntervalMs":6200,"durationMs":280},"steps":[{"expressionId":"expression-00","holdMs":5200,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-08","holdMs":5200,"transitionMs":500,"transition":"smooth"}]},"listening":{"name":"listening","description":"Expressions 10, 01 et 19, regard stable et clignement attentif.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":3200,"minIntervalMs":4800,"maxIntervalMs":7200,"durationMs":240},"steps":[{"expressionId":"expression-10","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-01","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-19","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"thinking":{"name":"thinking","description":"Regard haut et latéral, expressions asymétriques et changements fréquents.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-08","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-16","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-14","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-17","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-05","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"searching":{"name":"searching","description":"Balayage rapide et changements très fréquents.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-15","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-09","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-03","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-20","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-12","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-18","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"working":{"name":"working","description":"Rythme régulier et expressions concentrées.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-07","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-16","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-11","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-10","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"excited":{"name":"excited","description":"Grandes expressions et transitions rapides.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1200,"minIntervalMs":1800,"maxIntervalMs":3600,"durationMs":220},"steps":[{"expressionId":"expression-02","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-17","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-21","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-03","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-11","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"bored":{"name":"bored","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":4800,"minIntervalMs":6500,"maxIntervalMs":9500,"durationMs":420},"steps":[{"expressionId":"expression-04","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-22","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-00","holdMs":3600,"transitionMs":500,"transition":"smooth"}]},"suspicious":{"name":"suspicious","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-14","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-05","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-23","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"angry":{"name":"angry","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-07","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-16","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"drowsy":{"name":"drowsy","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":4800,"minIntervalMs":6500,"maxIntervalMs":9500,"durationMs":420},"steps":[{"expressionId":"expression-04","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-22","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-13","holdMs":3600,"transitionMs":500,"transition":"smooth"}]},"happy":{"name":"happy","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-02","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-11","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-17","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-19","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"curious":{"name":"curious","description":"Inclinaisons et forte asymétrie.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-03","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-21","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-00","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-15","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"confused":{"name":"confused","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-14","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-05","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-08","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"surprised":{"name":"surprised","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1200,"minIntervalMs":1800,"maxIntervalMs":3600,"durationMs":220},"steps":[{"expressionId":"expression-03","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-21","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"proud":{"name":"proud","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-15","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-08","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-02","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"shy":{"name":"shy","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-00","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-24","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-13","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"sad":{"name":"sad","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":4800,"minIntervalMs":6500,"maxIntervalMs":9500,"durationMs":420},"steps":[{"expressionId":"expression-04","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-13","holdMs":3600,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-22","holdMs":3600,"transitionMs":500,"transition":"smooth"}]},"laughing":{"name":"laughing","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1200,"minIntervalMs":1800,"maxIntervalMs":3600,"durationMs":220},"steps":[{"expressionId":"expression-02","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-11","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-17","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"scared":{"name":"scared","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1200,"minIntervalMs":1800,"maxIntervalMs":3600,"durationMs":220},"steps":[{"expressionId":"expression-03","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-21","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"playful":{"name":"playful","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":2100,"minIntervalMs":2800,"maxIntervalMs":5000,"durationMs":260},"steps":[{"expressionId":"expression-02","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-17","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-11","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-08","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"celebrate":{"name":"celebrate","description":"Cet état enchaîne un pool de presets et des clignements.","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1200,"minIntervalMs":1800,"maxIntervalMs":3600,"durationMs":220},"steps":[{"expressionId":"expression-02","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-08","holdMs":2300,"transitionMs":500,"transition":"smooth"},{"expressionId":"expression-17","holdMs":2300,"transitionMs":500,"transition":"smooth"}]},"speaking":{"name":"speaking","description":"Conversational mouth cycle with attentive micro-movement","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"talk-a","holdMs":360,"transitionMs":240,"transition":"smooth"},{"expressionId":"talk-b","holdMs":360,"transitionMs":240,"transition":"smooth"},{"expressionId":"talk-c","holdMs":360,"transitionMs":240,"transition":"smooth"},{"expressionId":"soft-smile","holdMs":360,"transitionMs":240,"transition":"smooth"}]},"presenting":{"name":"presenting","description":"Confident presenter loop with focus, joy and emphasis","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"focus","holdMs":920,"transitionMs":240,"transition":"smooth"},{"expressionId":"soft-smile","holdMs":920,"transitionMs":240,"transition":"smooth"},{"expressionId":"joy","holdMs":920,"transitionMs":240,"transition":"smooth"},{"expressionId":"confetti","holdMs":920,"transitionMs":240,"transition":"smooth"}]},"scanning":{"name":"scanning","description":"Search/scanning behavior with lateral gaze","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"scan-left","holdMs":620,"transitionMs":240,"transition":"smooth"},{"expressionId":"focus","holdMs":620,"transitionMs":240,"transition":"smooth"},{"expressionId":"scan-right","holdMs":620,"transitionMs":240,"transition":"smooth"},{"expressionId":"focus","holdMs":620,"transitionMs":240,"transition":"smooth"}]},"greeting":{"name":"greeting","description":"Warm hello with a wink and soft rebound","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"soft-smile","holdMs":420,"transitionMs":180,"transition":"spring"},{"expressionId":"wink","holdMs":420,"transitionMs":180,"transition":"spring"},{"expressionId":"joy","holdMs":420,"transitionMs":180,"transition":"spring"}]},"agree":{"name":"agree","description":"Quick positive acknowledgment","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"soft-smile","holdMs":360,"transitionMs":180,"transition":"spring"},{"expressionId":"success","holdMs":360,"transitionMs":180,"transition":"spring"},{"expressionId":"joy","holdMs":360,"transitionMs":180,"transition":"spring"}]},"disagree":{"name":"disagree","description":"Readable skeptical disagreement","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"skeptical","holdMs":430,"transitionMs":180,"transition":"spring"},{"expressionId":"side-eye","holdMs":430,"transitionMs":180,"transition":"spring"},{"expressionId":"angry-hot","holdMs":430,"transitionMs":180,"transition":"spring"}]},"wink":{"name":"wink","description":"Playful wink reaction","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"soft-smile","holdMs":360,"transitionMs":180,"transition":"spring"},{"expressionId":"wink","holdMs":360,"transitionMs":180,"transition":"spring"},{"expressionId":"smug","holdMs":360,"transitionMs":180,"transition":"spring"}]},"love":{"name":"love","description":"Affectionate floaty reaction","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"soft-smile","holdMs":520,"transitionMs":180,"transition":"spring"},{"expressionId":"love","holdMs":520,"transitionMs":180,"transition":"spring"},{"expressionId":"kiss","holdMs":520,"transitionMs":180,"transition":"spring"}]},"success":{"name":"success","description":"Energetic success acknowledgment","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"success","holdMs":330,"transitionMs":180,"transition":"spring"},{"expressionId":"confetti","holdMs":330,"transitionMs":180,"transition":"spring"},{"expressionId":"joy","holdMs":330,"transitionMs":180,"transition":"spring"}]},"error":{"name":"error","description":"Expressive error signal","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"error","holdMs":300,"transitionMs":180,"transition":"spring"},{"expressionId":"angry-hot","holdMs":300,"transitionMs":180,"transition":"spring"},{"expressionId":"panic","holdMs":300,"transitionMs":180,"transition":"spring"}]},"notification":{"name":"notification","description":"Attention pulse for alerts and events","playbackMode":"once","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"notification","holdMs":320,"transitionMs":180,"transition":"spring"},{"expressionId":"gasp","holdMs":320,"transitionMs":180,"transition":"spring"},{"expressionId":"soft-smile","holdMs":320,"transitionMs":180,"transition":"spring"}]},"dizzy":{"name":"dizzy","description":"Swaying dizzy reaction","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"dizzy","holdMs":450,"transitionMs":240,"transition":"smooth"},{"expressionId":"gasp","holdMs":450,"transitionMs":240,"transition":"smooth"},{"expressionId":"sleepy","holdMs":450,"transitionMs":240,"transition":"smooth"}]},"dance":{"name":"dance","description":"Bouncy celebratory dance loop","playbackMode":"loop","blink":{"enabled":true,"initialDelayMs":1800,"minIntervalMs":2600,"maxIntervalMs":5200,"durationMs":220},"steps":[{"expressionId":"confetti","holdMs":300,"transitionMs":240,"transition":"smooth"},{"expressionId":"wink","holdMs":300,"transitionMs":240,"transition":"smooth"},{"expressionId":"joy","holdMs":300,"transitionMs":240,"transition":"smooth"},{"expressionId":"kiss","holdMs":300,"transitionMs":240,"transition":"smooth"}]}}};

  const SVG_NS = 'http://www.w3.org/2000/svg';
  let instanceCount = 0;

  const clamp01 = v => Math.max(0, Math.min(1, v));
  const easeProgress = (p, transition) => {
    if (transition === 'smooth') return p * p * (3 - 2 * p);
    if (transition === 'snappy') return 1 - Math.pow(1 - p, 3);
    return 1 - Math.exp(-6 * p) * Math.cos(8 * p);
  };

  const nearestAngle = (target, current) => {
    let resolved = target;
    while (resolved - current > 180) resolved -= 360;
    while (resolved - current < -180) resolved += 360;
    return resolved;
  };

  const resolvedTargetExpression = (target, current) => ({
    ...target,
    headX: nearestAngle(target.headX, current.headX),
    headY: nearestAngle(target.headY, current.headY),
    headZ: nearestAngle(target.headZ, current.headZ),
    leftAngle: nearestAngle(target.leftAngle, current.leftAngle),
    rightAngle: nearestAngle(target.rightAngle, current.rightAngle),
  });

  const colorChannels = color => {
    const val = (color || '#000000').replace('#', '');
    const hex = val.length === 3 ? val.split('').map(c => c + c).join('') : val;
    const num = parseInt(hex, 16) || 0;
    return [(num >> 16) & 255, (num >> 8) & 255, num & 255];
  };

  const interpolateColor = (from, to, progress) => {
    const l = colorChannels(from);
    const r = colorChannels(to);
    const val = l.map((c, i) => Math.round(c + (r[i] - c) * progress));
    return '#' + val.map(c => c.toString(16).padStart(2, '0')).join('');
  };

  const resolveColors = expr => ({
    body: (expr && expr.bodyColor) || NEBY_DATA.avatar.colors.body,
    eyes: (expr && expr.eyeColor) || NEBY_DATA.avatar.colors.eyes,
  });

  const svgElement = name => document.createElementNS(SVG_NS, name);

  function createNebyInstance(container, options = {}) {
    if (!container) return null;
    const instanceId = ++instanceCount;
    const clipId = 'neby-clip-' + instanceId;
    const isHero = Boolean(options.hero || container.classList.contains('neby-avatar-hero'));
    const isInteractive = options.interactive !== false;

    container.classList.add('neby-avatar-container');
    if (isHero) container.classList.add('neby-hero-mode');

    const svg = svgElement('svg');
    svg.setAttribute('viewBox', '-150 -150 300 300');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Interactive Neby 3D Avatar');
    svg.classList.add('neby-avatar-svg');

    const defs = svgElement('defs');
    const clipPath = svgElement('clipPath');
    clipPath.id = clipId;
    const clipHead = svgElement('path');
    clipPath.append(clipHead);
    defs.append(clipPath);
    svg.append(defs);

    const motionLayer = svgElement('g');
    motionLayer.setAttribute('class', 'neby-motion-layer');

    const backLayer = svgElement('g');
    const head = svgElement('path');
    head.setAttribute('class', 'neby-head-base');

    const decalsLayer = svgElement('g');
    decalsLayer.setAttribute('class', 'neby-decals-layer');

    const eyesLayer = svgElement('g');
    eyesLayer.setAttribute('clip-path', 'url(#' + clipId + ')');
    const leftEye = svgElement('path');
    const rightEye = svgElement('path');
    eyesLayer.append(leftEye, rightEye);

    const mouth = svgElement('path');
    mouth.setAttribute('class', 'neby-mouth-path');
    mouth.setAttribute('fill', 'none');
    mouth.setAttribute('stroke-linecap', 'round');
    mouth.setAttribute('stroke-linejoin', 'round');

    const frontLayer = svgElement('g');

    motionLayer.append(backLayer, head, decalsLayer, eyesLayer, mouth, frontLayer);
    svg.append(motionLayer);
    container.innerHTML = '';
    container.append(svg);

    const ensurePaths = (group, paths, fill) => {
      while (group.children.length < paths.length) group.append(svgElement('path'));
      while (group.children.length > paths.length) group.lastElementChild.remove();
      paths.forEach((p, idx) => {
        const el = group.children[idx];
        el.setAttribute('d', p);
        el.setAttribute('fill', fill);
      });
    };

    const ensureDecals = (group, decals) => {
      while (group.children.length < decals.length) group.append(svgElement('path'));
      while (group.children.length > decals.length) group.lastElementChild.remove();
      decals.forEach((decal, idx) => {
        const el = group.children[idx];
        el.setAttribute('d', decal.path);
        el.setAttribute('fill', decal.fill);
        el.setAttribute('opacity', decal.opacity != null ? decal.opacity : 1);
      });
    };

    const animationNames = Object.keys(NEBY_DATA.animations);
    let currentAnimation = options.animation && NEBY_DATA.animations[options.animation]
      ? options.animation
      : (isHero ? 'idle' : 'idle');
    if (!NEBY_DATA.animations[currentAnimation]) currentAnimation = animationNames[0];

    const initialStep = NEBY_DATA.animations[currentAnimation].steps[0];
    const initialExpression = NEBY_DATA.expressions[initialStep.expressionId] || Object.values(NEBY_DATA.expressions)[0];

    let currentPose = AvatarProceduralEngine.poseFromExpression(initialExpression);
    let currentColors = resolveColors(initialExpression);
    let blinkAmount = 1;
    let transitionState = null;
    let blinkState = null;
    let frameRequest = null;
    let stepTimer = null;
    let blinkTimer = null;
    let blinkDueAt = null;
    let stepIndex = 0;
    let direction = 1;
    let playing = true;
    let paused = false;
    let stepDueAt = null;

    let eyeAmbientStartedAt = performance.now();
    let bodyAmbientStartedAt = performance.now();
    let eyeAmbientSignature = initialExpression.eyeMotion || 'microSaccades';
    let bodyAmbientSignature = initialExpression.bodyMotion || 'gentle';
    let ambientStrength = 1;
    let lastAmbientFrame = 0;

    // Look-at cursor tracking
    let cursorTargetX = 0;
    let cursorTargetY = 0;
    let cursorCurrentX = 0;
    let cursorCurrentY = 0;
    let isMouseOver = false;

    const render = (time = performance.now()) => {
      const eyeElapsed = time - eyeAmbientStartedAt;
      const bodyElapsed = time - bodyAmbientStartedAt;

      // Blend look-at offset
      cursorCurrentX += (cursorTargetX - cursorCurrentX) * 0.12;
      cursorCurrentY += (cursorTargetY - cursorCurrentY) * 0.12;

      let expr = { ...currentPose.expression };
      if (Math.abs(cursorCurrentX) > 0.001 || Math.abs(cursorCurrentY) > 0.001) {
        expr.headY = (expr.headY || 0) + cursorCurrentX * 18;
        expr.headX = (expr.headX || 0) - cursorCurrentY * 14;
        expr.positionXLeft = (expr.positionXLeft || 0) + cursorCurrentX * 4;
        expr.positionXRight = (expr.positionXRight || 0) + cursorCurrentX * 4;
      }

      if (expr.bodyMotion && expr.bodyMotion !== 'none') {
        expr = AvatarProceduralEngine.applyAmbientBodyMotion(expr, bodyElapsed, ambientStrength);
      }

      const eyeOffset = AvatarProceduralEngine.ambientEyeOffset(expr, eyeElapsed, ambientStrength);
      const renderedPose = AvatarProceduralEngine.poseFromExpression(expr);
      const geometry = AvatarProceduralEngine.renderAvatar(renderedPose, NEBY_DATA.avatar.surface, blinkAmount, {
        includeWire: false,
        bodyNodes: NEBY_DATA.avatar.bodyNodes,
        eyeOffset,
      });

      const bodyOffset = AvatarProceduralEngine.ambientBodyOffset(expr, bodyElapsed, ambientStrength);
      motionLayer.setAttribute('transform', 'translate(' + bodyOffset.x + ' ' + bodyOffset.y + ')');

      ensurePaths(backLayer, geometry.backPaths || [], currentColors.body);
      ensurePaths(frontLayer, geometry.frontPaths || [], currentColors.body);

      head.setAttribute('d', geometry.headPath || '');
      head.setAttribute('fill', currentColors.body);
      clipHead.setAttribute('d', geometry.headPath || '');

      ensureDecals(decalsLayer, geometry.decals || []);

      leftEye.setAttribute('d', geometry.leftPath || '');
      rightEye.setAttribute('d', geometry.rightPath || '');
      leftEye.setAttribute('fill', currentColors.eyes);
      rightEye.setAttribute('fill', currentColors.eyes);
      leftEye.style.display = geometry.leftVisible ? '' : 'none';
      rightEye.style.display = geometry.rightVisible ? '' : 'none';

      if (geometry.mouthVisible && geometry.mouthPath) {
        mouth.setAttribute('d', geometry.mouthPath);
        mouth.setAttribute('stroke', currentColors.eyes);
        mouth.setAttribute('stroke-width', (2.8 * (expr.mouthScale || 1)).toFixed(1));
        mouth.style.display = '';
      } else {
        mouth.style.display = 'none';
      }
    };

    const tick = time => {
      frameRequest = null;
      if (transitionState) {
        const linear = clamp01((time - transitionState.startedAt) / transitionState.durationMs);
        const eased = easeProgress(linear, transitionState.transition);
        ambientStrength = clamp01(eased);
        const expression = { ...transitionState.fromPose.expression };
        AvatarProceduralEngine.expressionFields.forEach(field => {
          const fromVal = transitionState.fromPose.expression[field] || 0;
          const toVal = transitionState.toPose.expression[field] || 0;
          expression[field] = fromVal + (toVal - fromVal) * eased;
        });
        expression.eyeMotion = transitionState.toPose.expression.eyeMotion;
        expression.bodyMotion = transitionState.toPose.expression.bodyMotion;
        expression.mouth = transitionState.toPose.expression.mouth;
        expression.mouthScale = transitionState.toPose.expression.mouthScale;
        currentPose = AvatarProceduralEngine.poseFromExpression(expression);
        currentColors = {
          body: interpolateColor(transitionState.fromColors.body, transitionState.toColors.body, clamp01(eased)),
          eyes: interpolateColor(transitionState.fromColors.eyes, transitionState.toColors.eyes, clamp01(eased)),
        };
        if (linear >= 1) {
          currentPose = transitionState.toPose;
          currentColors = transitionState.toColors;
          transitionState = null;
          ambientStrength = 1;
        }
      }

      if (blinkState) {
        const progress = clamp01((time - blinkState.startedAt) / blinkState.durationMs);
        if (progress <= 0.42) {
          const closeProgress = progress / 0.42;
          blinkAmount = 1 - closeProgress * closeProgress;
        } else {
          const openProgress = (progress - 0.42) / 0.58;
          blinkAmount = 1 - Math.pow(1 - openProgress, 2);
        }
        if (progress >= 1) {
          blinkAmount = 1;
          blinkState = null;
        }
      }

      const ambientActive = AvatarProceduralEngine.hasAmbientMotion(currentPose.expression);
      const trackingActive = Math.abs(cursorTargetX - cursorCurrentX) > 0.001 || Math.abs(cursorTargetY - cursorCurrentY) > 0.001;

      if (transitionState || blinkState || trackingActive || !ambientActive || time - lastAmbientFrame >= 1000 / 30) {
        render(time);
        if (ambientActive) lastAmbientFrame = time;
      }

      if (playing && (transitionState || blinkState || trackingActive || ambientActive)) {
        frameRequest = requestAnimationFrame(tick);
      }
    };

    const requestTick = () => {
      if (frameRequest === null && playing) frameRequest = requestAnimationFrame(tick);
    };

    const animateTo = (expressionId, durationMs, transition) => {
      const target = NEBY_DATA.expressions[expressionId];
      if (!target) return;
      const now = performance.now();
      if (target.eyeMotion !== eyeAmbientSignature) {
        eyeAmbientSignature = target.eyeMotion;
        eyeAmbientStartedAt = now;
      }
      if (target.bodyMotion !== bodyAmbientSignature) {
        bodyAmbientSignature = target.bodyMotion;
        bodyAmbientStartedAt = now;
      }
      const resolved = resolvedTargetExpression(target, currentPose.expression);
      const targetPose = AvatarProceduralEngine.poseFromExpression(resolved);
      const targetColors = resolveColors(target);

      if (durationMs <= 0) {
        ambientStrength = 1;
        transitionState = null;
        currentPose = targetPose;
        currentColors = targetColors;
        render();
        requestTick();
        return;
      }

      transitionState = {
        fromPose: currentPose,
        toPose: targetPose,
        fromColors: currentColors,
        toColors: targetColors,
        startedAt: now,
        durationMs,
        transition: transition || 'spring',
        expressionId,
      };
      ambientStrength = 0;
      requestTick();
    };

    const scheduleBlink = (anim, delay) => {
      if (!anim.blink || !anim.blink.enabled) return;
      blinkDueAt = performance.now() + delay;
      blinkTimer = setTimeout(() => {
        blinkDueAt = null;
        blinkState = { startedAt: performance.now(), durationMs: anim.blink.durationMs || 120 };
        requestTick();
        const minI = anim.blink.minIntervalMs || 2200;
        const maxI = anim.blink.maxIntervalMs || 6000;
        const range = maxI - minI;
        scheduleBlink(anim, (anim.blink.durationMs || 120) + minI + Math.random() * range);
      }, delay);
    };

    const advance = anim => {
      const last = anim.steps.length - 1;
      const mode = anim.playbackMode || 'loop';
      if (mode === 'once' && stepIndex >= last) return;
      if (mode === 'pingPong' && last > 0) {
        if (stepIndex >= last) direction = -1;
        else if (stepIndex <= 0) direction = 1;
        stepIndex += direction;
      } else {
        stepIndex = (stepIndex + 1) % (last + 1);
      }
      runStep(anim);
    };

    const runStep = anim => {
      if (!playing || !anim.steps.length) return;
      const step = anim.steps[stepIndex];
      animateTo(step.expressionId, step.transitionMs, step.transition);
      const duration = step.transitionMs + step.holdMs;
      stepDueAt = performance.now() + duration;
      stepTimer = setTimeout(() => advance(anim), duration);
    };

    const clearSchedule = () => {
      if (stepTimer !== null) clearTimeout(stepTimer);
      if (blinkTimer !== null) clearTimeout(blinkTimer);
      stepTimer = null;
      blinkTimer = null;
    };

    const playSequence = name => {
      const anim = NEBY_DATA.animations[name] || NEBY_DATA.animations['idle'];
      if (!anim) return;
      clearSchedule();
      currentAnimation = name;
      stepIndex = 0;
      direction = 1;
      playing = true;
      runStep(anim);
      scheduleBlink(anim, (anim.blink && anim.blink.initialDelayMs) || 1500);
      requestTick();
    };

    // Playful rich reaction animations
    const triggerReaction = type => {
      let animName = 'celebrate';
      if (type === 'wink') animName = 'wink';
      else if (type === 'joy' || type === 'celebrate' || type === 'happy') animName = 'celebrate';
      else if (type === 'think' || type === 'focus' || type === 'scanning') animName = 'scanning';
      else if (type === 'talk' || type === 'speaking' || type === 'chat') animName = 'speaking';
      else if (type === 'dance' || type === 'groove') animName = 'dance';
      else if (type === 'love' || type === 'heart' || type === 'kiss') animName = 'love';
      else if (type === 'agree' || type === 'nod' || type === 'yes' || type === 'affirm') animName = 'success';
      else if (type === 'disagree' || type === 'no' || type === 'skeptical') animName = 'disagree';
      else if (type === 'angry' || type === 'mad' || type === 'hot') animName = 'error';
      else if (type === 'sleepy' || type === 'sleep' || type === 'tired' || type === 'nap') animName = 'sad';
      else if (type === 'playful' || type === 'laugh' || type === 'laughing') animName = 'playful';
      else if (type === 'presenting') animName = 'presenting';
      else if (type === 'scared' || type === 'panic' || type === 'surprised') animName = 'surprised';
      else if (type === 'shy') animName = 'shy';
      else if (type === 'proud') animName = 'proud';
      else if (type === 'confused') animName = 'confused';
      else if (NEBY_DATA.animations[type]) animName = type;

      if (NEBY_DATA.animations[animName]) {
        playSequence(animName);
        if (animName !== 'idle') {
          setTimeout(() => {
            if (currentAnimation === animName) {
              playSequence('idle');
            }
          }, 3200);
        }
      } else if (NEBY_DATA.expressions[type]) {
        animateTo(type, 180, 'spring');
        stepTimer = setTimeout(() => {
          playSequence('idle');
        }, 1200);
      }
    };

    // Interactivity handlers
    if (isInteractive) {
      const onMouseMove = e => {
        const rect = container.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const range = isHero ? Math.max(window.innerWidth, window.innerHeight) * 0.7 : rect.width * 4;
        const dx = (e.clientX - cx) / range;
        const dy = (e.clientY - cy) / range;
        cursorTargetX = Math.max(-1, Math.min(1, dx));
        cursorTargetY = Math.max(-1, Math.min(1, dy));
        requestTick();
      };

      const onMouseEnter = () => {
        isMouseOver = true;
      };

      const onMouseLeave = () => {
        isMouseOver = false;
        cursorTargetX = 0;
        cursorTargetY = 0;
        requestTick();
      };

      const onClick = () => {
        const reactions = [
          'wink', 'dance', 'speaking', 
          'scanning', 'agree', 'disagree', 'sleepy', 'playful', 'shy'
        ];
        const randomReaction = reactions[Math.floor(Math.random() * reactions.length)];
        triggerReaction(randomReaction);
      };

      if (isHero) {
        window.addEventListener('mousemove', onMouseMove, { passive: true });
      } else {
        container.addEventListener('mousemove', onMouseMove, { passive: true });
      }
      container.addEventListener('mouseenter', onMouseEnter);
      container.addEventListener('mouseleave', onMouseLeave);
      container.addEventListener('click', onClick);
    }

    // Visibility Observer to save battery / CPU when offscreen
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            if (!playing) {
              playing = true;
              playSequence(currentAnimation);
            }
          } else {
            playing = false;
            clearSchedule();
          }
        });
      }, { threshold: 0.05 });
      observer.observe(container);
    }

    playSequence(currentAnimation);

    return {
      container,
      svg,
      play: playSequence,
      react: triggerReaction,
      setLookAt: (x, y) => {
        cursorTargetX = Math.max(-1, Math.min(1, x));
        cursorTargetY = Math.max(-1, Math.min(1, y));
        requestTick();
      },
      destroy: () => {
        playing = false;
        clearSchedule();
        if (frameRequest) cancelAnimationFrame(frameRequest);
        container.innerHTML = '';
      }
    };
  }

  function initAll() {
    document.querySelectorAll('[data-neby-avatar]:not([data-neby-initialized])').forEach(el => {
      el.setAttribute('data-neby-initialized', 'true');
      const anim = el.getAttribute('data-animation') || 'idle';
      const isHero = el.getAttribute('data-hero') === 'true' || el.classList.contains('neby-avatar-hero');
      const instance = createNebyInstance(el, {
        animation: anim,
        hero: isHero,
        interactive: true,
      });
      el.__nebyInstance = instance;
    });
  }

  // Auto-init on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  // MutationObserver for dynamic DOM updates (HTMX, fetch, threads, websockets)
  if (typeof MutationObserver !== 'undefined') {
    var observer = new MutationObserver(function (mutations) {
      var shouldInit = false;
      for (var i = 0; i < mutations.length; i++) {
        if (mutations[i].addedNodes.length > 0) {
          shouldInit = true;
          break;
        }
      }
      if (shouldInit) initAll();
    });
    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true });
    } else {
      document.addEventListener('DOMContentLoaded', function () {
        observer.observe(document.body, { childList: true, subtree: true });
      });
    }
  }

  // Delegated CSP-compliant handler for reaction buttons
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-neby-react]');
    if (btn) {
      var mood = btn.getAttribute('data-neby-react');
      var targetId = btn.getAttribute('data-neby-target') || 'profilePageNebyAvatar';
      var targetEl = document.getElementById(targetId) || document.querySelector('[data-hero="true"]') || document.querySelector('[data-neby-avatar]');
      if (targetEl && targetEl.__nebyInstance) {
        targetEl.__nebyInstance.react(mood);
      }
    }
  });

  window.NebyAvatar = {
    mount: createNebyInstance,
    initAll: initAll,
    data: NEBY_DATA,
  };

})(window, document);

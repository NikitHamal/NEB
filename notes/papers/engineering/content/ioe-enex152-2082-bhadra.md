---
file: NEBians-IOE-Past-Paper-Digital-Logic-ENEX152-2082-Bhadra.pdf
subject: Digital Logic
level: BE · Year I / Part II
code: ENEX 152
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Convert the following binary codes to gray codes. [[2+2]]

a) 101101

b) 110001

@q 2
What is 2's complement representation? Perform BCD addition of 23 + 48. [[1+2]]

@q 3
State and explain De Morgan's Theorem with truth table and necessary diagrams. [[4]]

@q 4
Minimize the function $F(A,B,C,D) = \sum m(0,1,2,4,7,8,9,10,12,15) + d(5,11,13)$ using K-Map and realize it with suitable logic gates. [[5]]

@q 5
What is magnitude comparator? Design a 3-bit magnitude comparator. [[1+5]]

@q 6
Implement a full adder circuit using Multiplexer. [[4]]

@q 7
Differentiate between combinational circuit and sequential circuit. With necessary steps and implementation, convert SR flip flop into JK flip flop. [[2+5]]

@q 8
Write briefly about different types of shift registers. With necessary circuit and timing diagram, explain the operation of how the shift register is used as a Johnson's Counter. [[2+3]]

@q 9
Describe the operation of 3-bit ripple up counter with positive edge triggered clock. [[5]]

@q 10
Design the synchronous mod-6 counter using S R flip-flop and draw its timing diagram also. [[7]]

@q 11
Design a synchronous sequential machine that has 1 bit serial input X and output Z which will be high when the input contains the message 110 (Use SR Flip Flop). [[7]]

@q 12
Write a short note on frequency counter. [[3]]

<!-- SOLUTIONS -->

@s 1
**(a)** Rule: the MSB of the Gray code equals the MSB of the binary code; every other Gray bit is $g_i = b_{i-1} \oplus b_i$.

- $g_1 = b_1 = 1$
- $g_2 = b_1 \oplus b_2 = 1 \oplus 0 = 1$
- $g_3 = b_2 \oplus b_3 = 0 \oplus 1 = 1$
- $g_4 = b_3 \oplus b_4 = 1 \oplus 1 = 0$
- $g_5 = b_4 \oplus b_5 = 1 \oplus 0 = 1$
- $g_6 = b_5 \oplus b_6 = 0 \oplus 1 = 1$

$$(101101)_2 = (111011)_{Gray}$$

**(b)** Rule: the MSB of the Gray code equals the MSB of the binary code; every other Gray bit is $g_i = b_{i-1} \oplus b_i$.

- $g_1 = b_1 = 1$
- $g_2 = b_1 \oplus b_2 = 1 \oplus 1 = 0$
- $g_3 = b_2 \oplus b_3 = 1 \oplus 0 = 1$
- $g_4 = b_3 \oplus b_4 = 0 \oplus 0 = 0$
- $g_5 = b_4 \oplus b_5 = 0 \oplus 0 = 0$
- $g_6 = b_5 \oplus b_6 = 0 \oplus 1 = 1$

$$(110001)_2 = (101001)_{Gray}$$


@s 2
**2's complement representation.** In an $n$-bit signed number the MSB is the sign bit (0 for positive, 1 for negative). A positive number is written in ordinary binary. A negative number $-N$ is stored as $2^n - N$, i.e. the **2's complement** of $N$:

1. write $N$ in $n$-bit binary, 2. invert every bit (1's complement), 3. add 1.

Range of an $n$-bit number: $-2^{n-1}$ to $+(2^{n-1}-1)$, and 0 has only one representation. Subtraction becomes addition, so one adder serves for both, which is why every computer uses it. Example (4 bits): $-5$: $0101 \to 1010 \to 1011$.

**BCD addition of 23 + 48.**

BCD addition: add the two BCD numbers as ordinary binary; any 4-bit group greater than 9 (or with a carry out) is corrected by adding $0110_2$ ($6$).

$$\begin{gathered}(23)_{BCD} = 0010 0011 \\ (48)_{BCD} = 0100 1000\end{gathered}$$

- Units: $0011 + 1000 = 01011$ (11). Since 11 > 9, add 0110: $1011 + 0110 = 10001$, giving the digit $0001$ and a carry 1 into the tens.
- Tens: $0010 + 0100 + 1 = 0111$ (7); a valid digit, no correction.

$$\begin{array}{r@{\;}l} & 0010 0011 \\ + & 0100 1000 \\ \hline & 0110\ 1011 \\ + & 0000\ 0110 \quad(\text{units corrected}) \\ \hline & 0111\ 0001 \end{array}$$

$$23 + 48 = 71 \quad\Rightarrow\quad \boxed{0111\ 0001}_{BCD} = (71)_{10}$$


@s 3
**De Morgan's theorems.**

1. The complement of a sum equals the product of the complements: $\overline{A+B} = \overline{A}\cdot\overline{B}$.
2. The complement of a product equals the sum of the complements: $\overline{A\cdot B} = \overline{A}+\overline{B}$.

They extend to any number of variables: $\overline{A+B+C+\dots} = \overline{A}\,\overline{B}\,\overline{C}\dots$ and $\overline{ABC\dots} = \overline{A}+\overline{B}+\overline{C}+\dots$

**Proof by truth table** (columns 3 and 4 are identical, and so are columns 5 and 6):

| A | B | $\overline{A+B}$ | $\overline{A}\,\overline{B}$ | $\overline{AB}$ | $\overline{A}+\overline{B}$ |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 | 0 |

The first case is 1 only when both inputs are 0 (a NOR gate), which is exactly when both $\overline{A}$ and $\overline{B}$ are 1 (an AND of the inverted inputs). The second is 0 only when both inputs are 1, which is when $\overline{A}$ or $\overline{B}$ is 1 fails to hold, matching an OR of inverted inputs.

```figure caption="De Morgan's theorems as gates: a NOR gate equals an AND gate with inverted inputs; a NAND gate equals an OR gate with inverted inputs."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.2,13.0),ylim=(-0.4,4.9))
# law 1: NOR = bubbled AND
ins,o=gn(ax,"NOR",1.0,3.8,n=2,w=1.0,lead=0.4); T(ax,0.2,4.05,"A",ha="right"); T(ax,0.2,3.55,"B",ha="right"); T(ax,o[0]+0.15,3.8,"$\\overline{A+B}$",ha="left"); T(ax,3.3,3.8,"=",size=11)
ins2,o2=gn(ax,"AND",6.0,3.8,n=2,w=1.0,lead=0.3)
for (px,py),nm in zip(ins2,"AB"):
    iin,iout=inv(ax,px-0.95,py,w=0.5,h=0.5,lead=0.15); L(ax,[iout,(px,py)]); T(ax,iin[0]-0.1,py,nm,ha="right")
T(ax,o2[0]+0.15,3.8,"$\\overline{A}\\,\\overline{B}$",ha="left"); T(ax,9.9,3.8,"NOR = bubbled AND",size=8,ha="left",color=MUTED)
# law 2: NAND = bubbled OR
ins,o=gn(ax,"NAND",1.0,1.5,n=2,w=1.0,lead=0.4); T(ax,0.2,1.75,"A",ha="right"); T(ax,0.2,1.25,"B",ha="right"); T(ax,o[0]+0.15,1.5,"$\\overline{AB}$",ha="left"); T(ax,3.3,1.5,"=",size=11)
ins2,o2=gn(ax,"OR",6.0,1.5,n=2,w=1.0,lead=0.3)
for (px,py),nm in zip(ins2,"AB"):
    iin,iout=inv(ax,px-0.95,py,w=0.5,h=0.5,lead=0.15); L(ax,[iout,(px,py)]); T(ax,iin[0]-0.1,py,nm,ha="right")
T(ax,o2[0]+0.15,1.5,"$\\overline{A}+\\overline{B}$",ha="left"); T(ax,9.9,1.5,"NAND = bubbled OR",size=8,ha="left",color=MUTED)
```

**Use.** De Morgan's laws convert AND-OR forms into NAND-NAND or NOR-NOR forms, which is how circuits are built with a single gate type.


@s 4
**Step 1 - K-map.** Enter 1 in each minterm cell and X (don't care) in each don't-care cell, Gray-code ordered rows and columns so neighbouring cells differ in one variable.

```figure caption="4-variable K-map of F with the prime-implicant loops (cell numbers are minterm numbers)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(3.2,2.92,xlim=(0,4.58),ylim=(-0.2,4.18))

kmap(ax,0.9,0.4,4,[0, 1, 2, 4, 7, 8, 9, 10, 12, 15],[5, 11, 13],[([0, 1, 4, 5, 8, 9, 12, 13], '#d9534f'), ([5, 7, 13, 15], '#1d6fb8'), ([0, 2, 8, 10], '#2e8b57')],names='ABCD',cs=0.72,title='F')
```

**Step 2 - groups (largest possible, power of two).**

- Group 1 (loop colour red), cells 0, 1, 4, 5, 8, 9, 12, 13: variables that do not change survive, giving $\overline{C}$.
- Group 2 (loop colour blue), cells 5, 7, 13, 15: variables that do not change survive, giving $BD$.
- Group 3 (loop colour green), cells 0, 2, 8, 10: variables that do not change survive, giving $\overline{B}\overline{D}$.

**Step 3 - minimised expression.**

$$\boxed{F(A,B,C,D) = \overline{C} + BD + \overline{B}\overline{D}}$$

**Step 4 - realisation with logic gates (AND-OR, two-level).** The complemented inputs come from NOT gates.

```figure caption="AND-OR realisation of F = C' + BD + B'D'"
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(5.9,3.82,xlim=(-0.5,8.8),ylim=(-4.2,1.8))

sopc(ax,[[(2, 0)], [(1, 1), (3, 1)], [(1, 0), (3, 0)]],['A', 'B', 'C', 'D'],out='F')
```

*Equivalent NAND-only form.* Replacing every AND and the OR by NAND gates (double inversion, De Morgan) gives the same function with 4 NAND gates (plus the input inverters).


@s 5
**Magnitude comparator.** A magnitude comparator is a combinational circuit that compares two binary numbers $A$ and $B$ and tells whether $A>B$, $A=B$ or $A<B$ (three outputs, only one of which is 1).

**Design of a 3-bit comparator** ($A=A_2A_1A_0$, $B=B_2B_1B_0$). Compare from the MSB downwards. Two bits of equal weight are equal when $x_i = A_i \odot B_i = \overline{A_i\oplus B_i}$ (XNOR).

$$(A=B) = x_2x_1x_0$$

$A>B$ if the MSBs differ with $A_2=1, B_2=0$, **or** the MSBs are equal and the next bits satisfy $A_1=1,B_1=0$, **or** the two upper bits are equal and $A_0=1, B_0 = 0$; $A<B$ is the mirror image:

$$\begin{gathered} (A>B) = A_2\overline{B_2} + x_2A_1\overline{B_1} + x_2x_1A_0\overline{B_0} \\ (A<B) = \overline{A_2}B_2 + x_2\overline{A_1}B_1 + x_2x_1\overline{A_0}B_0 \\ (A=B) = x_2x_1x_0 \end{gathered}$$

(All three expressions were checked against the 64 input combinations.) A few rows of the function table:

| A | B | A>B | A=B | A<B |
|---|---|---|---|---|
| 101 | 011 | 1 | 0 | 0 |
| 010 | 010 | 0 | 1 | 0 |
| 011 | 100 | 0 | 0 | 1 |
| 110 | 111 | 0 | 0 | 1 |
| 111 | 110 | 1 | 0 | 0 |

**Logic diagram.** The three XNOR gates give $x_2,x_1,x_0$, which feed the AND-OR networks of the three outputs:

```figure caption="The three XNOR gates producing x2 = A2 xnor B2, x1 and x0."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

fig,ax=ckt_canvas(5.9,1.9,xlim=(-1.2,11.2),ylim=(-0.2,3.0))
for k,(a,b) in enumerate([("A2","B2"),("A1","B1"),("A0","B0")]):
    x0=1.2+3.7*k
    ins,o=gate(ax,"XNOR",x0,1.4,w=1.2,h=0.9,lead=0.4)
    T(ax,ins[0][0]-0.1,ins[0][1],a,ha="right",size=8.4); T(ax,ins[1][0]-0.1,ins[1][1],b,ha="right",size=8.4)
    T(ax,o[0]+0.12,o[1],"x%d"%(2-k),ha="left",size=8.6)
```
```figure caption="Output logic of the 3-bit magnitude comparator (inputs x2, x1, x0 come from the XNOR gates above)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

def row(ax,y0,terms,out):
    m=len(terms); pitch=1.5; ys=[y0-k*pitch for k in range(m)]; outs=[]
    for k,t in enumerate(terms):
        ins,o=gn(ax,"AND",4.0,ys[k],n=len(t),w=0.9,lead=0.3)
        for (px,py),lab in zip(ins,t): T(ax,px-0.08,py,lab,ha="right",size=8.2)
        outs.append(o)
    if m==1:
        L(ax,[outs[0],(outs[0][0]+0.5,outs[0][1])]); T(ax,outs[0][0]+0.6,outs[0][1],out,ha="left",size=8.8); return
    yc=sum(ys)/m
    ins,o=gn(ax,"OR",7.0,yc,n=m,sp=pitch,w=1.0,lead=0.3)
    for (px,py),(ox,oy) in zip(ins,outs): L(ax,[(ox,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=8.8)
fig,ax=ckt_canvas(5.9,6.2,xlim=(0.5,10.5),ylim=(-12.6,2.0))
row(ax,1.0,[["A2","B2'"],["x2","A1","B1'"],["x2","x1","A0","B0'"]],"A>B")
row(ax,-5.2,[["x2","x1","x0"]],"A=B")
row(ax,-8.2,[["A2'","B2"],["x2","A1'","B1"],["x2","x1","A0'","B0"]],"A<B")
T(ax,0.9,1.9,"(an apostrophe means the complemented input, obtained with a NOT gate)",size=7.4,color=MUTED,ha="left")
```

The same design cascades: an IC such as the 7485 compares 4 bits and has cascading inputs $(A>B)_{in}, (A=B)_{in}, (A<B)_{in}$ so that two ICs make an 8-bit comparator.


@s 6
**Full adder.** It adds three bits $A$, $B$ and the carry-in $C$ (written $C_{in}$) and gives Sum and Carry-out:

| A | B | C | Sum | Cout |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

$$\begin{gathered}S = A\oplus B\oplus C \\ C_{out} = AB + BC + CA\end{gathered}$$

**Multiplexer implementation.** Use two 4:1 multiplexers with $A$ and $B$ on the select lines ($S_1 = A$, $S_0 = B$). For each of the four select combinations read the output as a function of the third variable $C$ (implementation table):

| AB (select) | Sum (data input) | Cout (data input) |
|---|---|---|
| 00 | C | 0 |
| 01 | $\overline{C}$ | C |
| 10 | $\overline{C}$ | C |
| 11 | C | 1 |

Check: for $AB=01$ the truth table rows $010 \to (S,C_{out}) = (1,0)$ and $011 \to (0,1)$ give $S=\overline{C}$ and $C_{out}=C$; for $AB=00$: $000\to(0,0)$, $001\to(1,0)$ give $S=C$, $C_{out}=0$; for $AB=11$: $110\to(0,1)$, $111\to(1,1)$ give $S=C$, $C_{out}=1$.

```figure caption="Full adder from two 4:1 multiplexers (A = S1, B = S0; data inputs are 0, 1, C and its complement)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

fig,ax=ckt_canvas(5.9,2.3,xlim=(-3.2,17.4),ylim=(-2.2,3.2))
m1=mux(ax,3.0,0.6,4,['C', '$\\overline{C}$', '$\\overline{C}$', 'C'],["A","B"],out="Sum",name="4:1 MUX (sum)")
m2=mux(ax,12.0,0.6,4,['0', 'C', 'C', '1'],["A","B"],out="Cout",name="4:1 MUX (carry)")
T(ax,7.5,-2.0,"select lines A (S1) and B (S0) are common to both multiplexers",size=7.6,color=MUTED)
```

One NOT gate (for $\overline{C}$) and two 4:1 multiplexers are enough. (With 8:1 multiplexers the select lines would be $A,B,C$ and the data inputs simply the constants of the truth table.)


@s 7
| Point | Combinational circuit | Sequential circuit |
|---|---|---|
| Output depends on | Present inputs only | Present inputs **and** the past (stored state) |
| Memory | None | Flip-flops / latches store the state |
| Clock | Not needed | Usually clocked (synchronous) or event driven |
| Feedback | No feedback path | Outputs fed back to the inputs through the memory |
| Building blocks | Gates, adders, MUX, decoders | Flip-flops + gates: counters, registers |
| Speed | Faster, only gate delays | Slower, limited by clock and flip-flop delays |
| Design tools | Truth table, K-map | State table, state diagram, excitation table |
| Example | Half adder, encoder, comparator | Counter, shift register, sequence detector |

**Converting an SR flip-flop into a JK flip-flop.**

*Step 1 - excitation table of the SR flip-flop* (what $S,R$ must be for each $Q\to Q^{+}$ change):

| Q | Q⁺ | S | R |
|---|---|---|---|
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | X | 0 |

*Step 2 - truth table of the required JK flip-flop with the S, R needed:*

| J | K | Q | Q⁺ | S | R |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | X |
| 0 | 0 | 1 | 1 | X | 0 |
| 0 | 1 | 0 | 0 | 0 | X |
| 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | X | 0 |
| 1 | 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 0 | 0 | 1 |

*Step 3 - K-maps* (rows $J$, columns $KQ$ in Gray order $00, 01, 11, 10$):

| S | KQ=00 | 01 | 11 | 10 |
|---|---|---|---|---|
| J=0 | 0 | X | 0 | 0 |
| J=1 | 1 | X | 0 | 1 |

| R | KQ=00 | 01 | 11 | 10 |
|---|---|---|---|---|
| J=0 | X | 0 | 1 | X |
| J=1 | 0 | 0 | 1 | 0 |

Looping the 1s together with the X cells: for S the two cells with $J=1$, $Q=0$ (columns 00 and 10) form one pair, giving $J\overline{Q}$; for R the two cells with $K=1$, $Q=1$ (column 11, both rows) form a pair, giving $KQ$:

$$\begin{gathered}\boxed{S = J\,\overline{Q}} \\ \boxed{R = K\,Q}\end{gathered}$$

*Step 4 - circuit.* Two 2-input AND gates fed back from the outputs:

```figure caption="JK flip-flop from an SR flip-flop: S = J Q', R = K Q."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

fig,ax=ckt_canvas(5.9,2.8,xlim=(-1.6,9.6),ylim=(-0.6,4.2))
P=ffb(ax,4.6,0.5,"SR flip-flop","SR",w=1.4,h=2.4)
S=P["S"]; R=P["R"]; ck=P["CK"]; q=P["Q"]; qn=P["QN"]
i1,o1=gn(ax,"AND",1.8,S[1],n=2,w=0.9,lead=0.3)
i2,o2=gn(ax,"AND",1.8,R[1]-0.15,n=2,w=0.9,lead=0.3)
L(ax,[o1,S]); L(ax,[o2,(o2[0]+0.1,o2[1]),(o2[0]+0.1,R[1]),R]) if abs(o2[1]-R[1])>1e-6 else L(ax,[o2,R])
T(ax,i1[0][0]-0.1,i1[0][1],"J",ha="right"); T(ax,i2[1][0]-0.1,i2[1][1],"K",ha="right")
L(ax,[qn,(qn[0]+0.4,qn[1]),(qn[0]+0.4,-0.1),(0.9,-0.1),(0.9,i1[1][1]),i1[1]])
L(ax,[q,(q[0]+0.8,q[1])]); T(ax,q[0]+0.9,q[1],"Q",ha="left"); T(ax,qn[0]+0.5,qn[1]-0.1,"Q$'$",ha="left")
L(ax,[(q[0]+0.6,q[1]),(q[0]+0.6,-0.45),(0.5,-0.45),(0.5,i2[0][1]),i2[0]]); dot(ax,q[0]+0.6,q[1])
T(ax,ck[0]-0.1,ck[1],"CLK",ha="right")
```

The forbidden state $S=R=1$ never occurs, because $S=J\overline{Q}$ and $R=KQ$ cannot both be 1; with $J=K=1$ the flip-flop toggles. (It still needs a master-slave or edge-triggered SR to avoid race-around.)


@s 8
A **shift register** is a chain of flip-flops with a common clock in which the stored word moves one position per clock pulse. According to how the data enter and leave there are four types:

| Type | Data in | Data out | Use |
|---|---|---|---|
| SISO | Serial | Serial | Delay line (n clock pulses), serial memory |
| SIPO | Serial | Parallel | Serial-to-parallel conversion (UART receiver) |
| PISO | Parallel | Serial | Parallel-to-serial conversion (UART transmitter) |
| PIPO | Parallel | Parallel | Temporary storage, buffer register |

Besides these, a shift register can shift in either direction (**bidirectional**) or be a **universal** register (parallel load + left shift + right shift), and when its output is fed back to the input it becomes a **ring counter** or a **Johnson (twisted-ring) counter**.

**Johnson counter.** The inverted output of the last flip-flop, $\overline{Q_D}$, is connected back to the serial input of the first. An $n$-bit register then has $2n$ distinct states (mod-$2n$ counter): for $n=4$, 8 states, $0000\to1000\to1100\to1110\to1111\to0111\to0011\to0001\to0000$. Each state is decoded by a 2-input AND gate (no decoding glitches), and the output frequency of any stage is $f/2n$.

**Johnson counter (3-bit example).** The shift register of three D flip-flops has $\overline{Q_2}$ connected back to $D_0$.

```figure caption="3-bit Johnson (twisted-ring) counter."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.4,12.6),ylim=(-1.9,3.0))
Ps=[ffb(ax,0.4+3.4*i,0.6,"FF"+"012"[i],"D",w=1.2,h=1.5,qn=True) for i in range(3)]
for i in range(2): L(ax,[Ps[i]["Q"],Ps[i+1]["D"]])
for i,P in enumerate(Ps):
    L(ax,[P["CK"],(P["CK"][0],-0.3)]); dot(ax,P["CK"][0],-0.3)
    T(ax,P["Q"][0]+0.12,P["Q"][1]+0.28,"Q"+"012"[i],size=8.2,ha="left") if i<2 else None
L(ax,[(Ps[0]["CK"][0],-0.3),(Ps[2]["CK"][0],-0.3)]); T(ax,Ps[0]["CK"][0]-0.1,-0.3,"CLK",ha="right")
q=Ps[2]["Q"]; qn=Ps[2]["QN"]; d0=Ps[0]["D"]
L(ax,[qn,(qn[0]+0.4,qn[1]),(qn[0]+0.4,-1.2),(d0[0]-0.6,-1.2),(d0[0]-0.6,d0[1]),d0]); T(ax,qn[0]+0.5,qn[1]-0.1,"Q$'_2$",ha="left",size=8.2)
L(ax,[q,(q[0]+0.8,q[1])]); T(ax,q[0]+0.9,q[1],"Q$_2$",ha="left")
```

Starting from 000 the sequence is

| Clock | Q0 | Q1 | Q2 |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 1 | 1 | 1 |
| 4 | 0 | 1 | 1 |
| 5 | 0 | 0 | 1 |
| 6 | 0 | 0 | 0 |

after which 000 recurs: $2n=6$ states, so the counter divides the clock by 6, and every output has a 50 % duty cycle.

```figure caption="Timing diagram of the 3-bit Johnson counter (6 states, each output is a square wave of frequency f/6, shifted by one clock period)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(5.9,2.61,xlim=(-1.9,7.7),ylim=(-0.3,4.05))

clock(ax,0,3.1499999999999995,7)
guides(ax,[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],3.8499999999999996,-0.1)
wave(ax,2.0,[(0.0, 0), (0.05, 1), (3.05, 0), (6.05, 1)],7,'Q0')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (4.05, 0)],7,'Q1')
wave(ax,0.1,[(0.0, 0), (2.05, 1), (5.05, 0)],7,'Q2')
```


@s 9
**3-bit asynchronous (ripple) up counter with positive-edge triggered clock.** Three T flip-flops (JK flip-flops with $J=K=1$) are cascaded. The external clock drives only the first stage. Since each flip-flop toggles on a *rising* edge, the clock of the next stage is taken from the **complemented output $\overline{Q}$ of the previous stage**: $\overline{Q}$ rises when $Q$ falls, so the next stage toggles when the previous bit goes from 1 to 0 (the carry).

```figure caption="3-bit ripple up counter built from rising-edge toggle flip-flops (clock of each stage from Q' of the previous one)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

fig,ax=ckt_canvas(5.9,2.2,xlim=(-1.6,14.5),ylim=(-0.4,3.0))
Ps=[ffb(ax,0.4+4.0*i,0.6,"FF%d"%i,"T",w=1.3,h=1.6,qn=True,neg=False) for i in range(3)]
for i,P in enumerate(Ps):
    T(ax,P["T"][0]-0.1,P["T"][1],"1",ha="right",size=8.4)
for i in range(3-1):
    Pa,Pb=Ps[i],Ps[i+1]
    src=Pa["QN"]
    L(ax,[src,(src[0]+0.5,src[1]),(src[0]+0.5,0.05),(Pb["CK"][0]-0.45,0.05),(Pb["CK"][0]-0.45,Pb["CK"][1]),Pb["CK"]])
L(ax,[(Ps[0]["CK"][0]-0.7,Ps[0]["CK"][1]),Ps[0]["CK"]]); T(ax,Ps[0]["CK"][0]-0.75,Ps[0]["CK"][1],"CLK",ha="right")
for i,P in enumerate(Ps):
    L(ax,[P["Q"],(P["Q"][0]+0.5,P["Q"][1])]); T(ax,P["Q"][0]+0.55,P["Q"][1],"Q%d"%i,ha="left",size=8.4)
```

**Operation.** $Q_0$ toggles on every clock pulse, so its frequency is $f/2$; $Q_1$ toggles whenever $Q_0$ falls, giving $f/4$; $Q_2$ toggles whenever $Q_1$ falls, giving $f/8$. The count is $Q_2Q_1Q_0$:

| Clock pulse | Q2 | Q1 | Q0 |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 1 | 1 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 0 | 1 |
| 6 | 1 | 1 | 0 |
| 7 | 1 | 1 | 1 |
| 8 | 0 | 0 | 0 |

The counter has $2^3 = 8$ states (mod-8) and returns to 000 on the 8th pulse.

```figure caption="Timing diagram of the 3-bit ripple up counter (rising-edge clock). Each Q changes slightly after the one before it (propagation delay), and each stage halves the frequency."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(5.9,2.37,xlim=(-1.9,8.7),ylim=(-0.3,4.05))

clock(ax,0,3.1499999999999995,8)
guides(ax,[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],3.8499999999999996,-0.1)
wave(ax,2.0,[(0.0, 0), (3.21, 1), (7.21, 0)],8,'Q2')
wave(ax,1.05,[(0.0, 0), (1.13, 1), (3.13, 0), (5.13, 1), (7.13, 0)],8,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (5.05, 0), (6.05, 1), (7.05, 0)],8,'Q0')
```

Because the stages respond one after another, the total settling time is $n\,t_{pd}$, which limits the clock frequency to $f_{max} \le 1/(n\,t_{pd}+t_{decode})$. This is the price of the simplicity of the asynchronous counter.


@s 10
**Design of the synchronous mod-6 counter with SR flip-flops.**

*Step 1 - number of flip-flops.* $2^{2} < N \le 2^{3}$ needs $n=3$ flip-flops (SR flip-flops), all clocked together (synchronous). The states are $Q2Q1Q0$.

*Step 2 - excitation table of the SR flip-flop.*

| Q | Q⁺ | S | R |
|---|---|---|---|
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | X | 0 |

*Step 3 - state / excitation table* (for each present state the next state, and the flip-flop inputs needed from the excitation table; X = don't care):

| Q2 | Q1 | Q0 | Q2⁺ | Q1⁺ | Q0⁺ | S2 | R2 | S1 | R1 | S0 | R0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 1 | 0 | X | 0 | X | 1 | 0 |
| 0 | 0 | 1 | 0 | 1 | 0 | 0 | X | 1 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 | 1 | 0 | X | X | 0 | 1 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 1 | X | 0 | 0 | X | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | X | 0 | 1 |

The unused states (110 and 111) never occur, so their next-state and input entries are don't-cares (X) in the K-maps.

*Step 4 - K-map simplification of every flip-flop input.*

```figure caption="K-maps for the flip-flop inputs (1 = needed, X = don't care); on the maps A, B, C, D stand for the present-state bits in the order of the table."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(6.6,2.79,xlim=(0,10.9),ylim=(-0.2,4.6))

kmap(ax,0.9,2.6,3,[3],[4, 6, 7],[([3, 7], '#d9534f')],names='ABCD',cs=0.55,title='S2')
kmap(ax,4.4,2.6,3,[5],[0, 1, 2, 6, 7],[([1, 5], '#d9534f')],names='ABCD',cs=0.55,title='R2')
kmap(ax,7.9,2.6,3,[1],[2, 6, 7],[([1], '#d9534f')],names='ABCD',cs=0.55,title='S1')
kmap(ax,0.9,0.4,3,[3],[0, 4, 5, 6, 7],[([3, 7], '#d9534f')],names='ABCD',cs=0.55,title='R1')
kmap(ax,4.4,0.4,3,[0, 2, 4],[6, 7],[([0, 2, 4, 6], '#d9534f')],names='ABCD',cs=0.55,title='S0')
kmap(ax,7.9,0.4,3,[1, 3, 5],[6, 7],[([1, 3, 5, 7], '#d9534f')],names='ABCD',cs=0.55,title='R0')
```

The loops give

$$\begin{gathered} S_{2} = Q_1Q_0 \\ R_{2} = \overline{Q_1}Q_0 \\ S_{1} = \overline{Q_2}\overline{Q_1}Q_0 \\ R_{1} = Q_1Q_0 \\ S_{0} = \overline{Q_0} \\ R_{0} = Q_0 \end{gathered}$$
*Step 5 - logic diagram.*

```figure caption="Logic diagram of the synchronous mod-6 counter with SR flip-flops."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(6.9,4.6,xlim=(-0.4,25.299999999999997),ylim=(-9.5,3.0))

seqcirc(ax,'SR',['Q2', 'Q1', 'Q0'],[{'S': [[(1, 1), (2, 1)]], 'R': [[(1, 0), (2, 1)]]}, {'S': [[(0, 0), (1, 0), (2, 1)]], 'R': [[(1, 1), (2, 1)]]}, {'S': [[(2, 0)]], 'R': [[(2, 1)]]}],zterms=None,extra=[])
```

```figure caption="Timing diagram of the synchronous mod-6 counter (states 000 to 101): Q2 is high for counts 4 and 5, so the output at Q2 has frequency f/6 (high for 2 of 6 clock periods)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(5.9,2.37,xlim=(-1.9,8.7),ylim=(-0.3,4.05))

clock(ax,0,3.1499999999999995,8)
guides(ax,[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],3.8499999999999996,-0.1)
wave(ax,2.0,[(0.0, 0), (3.05, 1), (5.05, 0)],8,'Q2')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (3.05, 0), (7.05, 1)],8,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (5.05, 0), (6.05, 1), (7.05, 0)],8,'Q0')
```


@s 11
**Design of the sequence detector for 110 (Mealy machine, overlapping sequences allowed, SR flip-flops).** One input $X$ (serial data), one output $Z$; $Z=1$ for the clock period in which the last bit of **110** arrives.

*Step 1 - state diagram.* States remember how much of the pattern has been matched:

- $S_0$: no part of the pattern seen yet (reset state)
- $S_1$: the last 1 input bit 1 seen
- $S_2$: the last 2 input bits 11 seen

Edge labels are $X/Z$. After a complete match the machine falls back to the longest prefix of the pattern that is also a suffix of what was received (overlap).

```figure caption="State diagram (Mealy) of the 110 detector; labels are X/Z."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(5.9,3.0,xlim=(-1.0,6.8),ylim=(-2.4,1.7))

statediag(ax,['S0', 'S1', 'S2'],[(0, 0, '0/0'), (0, 1, '1/0'), (1, 0, '0/0'), (1, 2, '1/0'), (2, 0, '0/1'), (2, 2, '1/0')])
```

*Step 2 - state table.*

| Present state | X = 0: next / Z | X = 1: next / Z |
|---|---|---|
| S0 | S0 / 0 | S1 / 0 |
| S1 | S0 / 0 | S2 / 0 |
| S2 | S0 / 1 | S2 / 0 |

*Step 3 - state assignment.* Three states need $n = 2$ flip-flops: $S_0=00$, $S_1=01$, $S_2=10$ ($Q_1Q_0$). The code 11 is unused (don't care).

*Step 4 - excitation table of the SR flip-flop.*

| Q | Q⁺ | S | R |
|---|---|---|---|
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | X | 0 |

*Step 5 - state/excitation table* with $Q_1Q_0$ the present state and $X$ the input:

| Q1 | Q0 | X | Q1⁺ | Q0⁺ | Z | S1 | R1 | S0 | R0 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | X | 0 | X |
| 0 | 0 | 1 | 0 | 1 | 0 | 0 | X | 1 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | X | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | X |
| 1 | 0 | 1 | 1 | 0 | 0 | X | 0 | 0 | X |

*Step 6 - K-maps* (variables $Q_1, Q_0, X$; the unused state 11 gives X entries):

```figure caption="K-maps for the flip-flop inputs and the output Z (variables Q1 Q0 X; A = Q1, B = Q0, C = X)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(6.6,2.75,xlim=(0,11.5),ylim=(-0.2,4.8))

kmap(ax,0.9,2.6999999999999997,3,[3],[5, 6, 7],[([3, 7], '#d9534f')],names='ABC',cs=0.6,title='S1')
kmap(ax,4.6000000000000005,2.6999999999999997,3,[4],[0, 1, 2, 6, 7],[([0, 2, 4, 6], '#d9534f')],names='ABC',cs=0.6,title='R1')
kmap(ax,8.3,2.6999999999999997,3,[1],[6, 7],[([1], '#d9534f')],names='ABC',cs=0.6,title='S0')
kmap(ax,0.9,0.4,3,[2, 3],[0, 4, 5, 6, 7],[([2, 3, 6, 7], '#d9534f')],names='ABC',cs=0.6,title='R0')
kmap(ax,4.6000000000000005,0.4,3,[4],[6, 7],[([4, 6], '#d9534f')],names='ABC',cs=0.6,title='Z')
```

$$\begin{gathered} S_{1} = Q_0X \\ R_{1} = \overline{X} \\ S_{0} = \overline{Q_1}\overline{Q_0}X \\ R_{0} = Q_0 \\ Z = Q_1\overline{X} \end{gathered}$$
*Step 7 - logic diagram.*

```figure caption="Logic diagram of the 110 sequence detector (SR flip-flops)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(6.9,4.6,xlim=(-0.4,23.2),ylim=(-9.5,3.0))

seqcirc(ax,'SR',['Q1', 'Q0'],[{'S': [[(1, 1), (2, 1)]], 'R': [[(2, 0)]]}, {'S': [[(0, 0), (1, 0), (2, 1)]], 'R': [[(1, 1)]]}],zterms=[[(0, 1), (2, 0)]],extra=['X'])
```

*Check with a test stream* $X = 1101100110$ (applied left to right): the states visited are S0, S1, S2, S0, S1, S2, S0, S0, S1, S2 and the output is $Z = 0010010001$, with a 1 exactly when the last three bits are 110 (including overlaps).

```figure caption="Timing diagram of the 110 detector for X = 1101100110: Z goes high in the period in which the last bit of 110 is applied (Mealy output, depends on X and the present state)."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
fig,ax=ckt_canvas(5.9,2.43,xlim=(-1.9,10.7),ylim=(-0.3,5.0))

clock(ax,0,4.1,10)
guides(ax,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],4.8,-0.1)
wave(ax,2.95,[(0.0, 1), (1.55, 0), (2.55, 1), (4.55, 0), (6.55, 1), (8.55, 0)],10,'X')
wave(ax,2.0,[(0.0, 0), (1.55, 1), (2.55, 0), (4.55, 1), (5.55, 0), (8.55, 1)],10,'Z',color='#d9534f')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (2.05, 0), (4.05, 1), (5.05, 0), (8.05, 1), (9.05, 0)],10,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (3.05, 1), (4.05, 0), (7.05, 1), (8.05, 0)],10,'Q0')
```


@s 12
**Frequency measurement (frequency counter).** Frequency is the number of cycles per second, so a digital frequency counter counts the cycles of the unknown signal during a **precise 1 s gate time** derived from a crystal oscillator.

```figure caption="Functional diagram of a digital frequency counter."
import numpy as _np, matplotlib.patches as mp
def T(ax,x,y,s,size=8.2,ha="center",va="center",color=INK,**k):
    return ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,**k)
def L(ax,pts,lw=1.4,color=INK,**k):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=color,lw=lw,solid_capstyle="round",solid_joinstyle="round",**k)
def dot(ax,x,y): ax.plot([x],[y],"o",ms=3.6,color=INK,zorder=5)
def box(ax,x,y,w,h,txt=None,fc="#f6f8fc",size=8.6,lw=1.4,ec=INK):
    ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,zorder=3))
    if txt: T(ax,x+w/2,y+h/2,txt,size=size,zorder=6)
def arr(ax,a,b,color=INK,lw=1.3,rad=0.0):
    ax.add_patch(mp.FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,color=color,lw=lw,connectionstyle="arc3,rad=%g"%rad,zorder=4))
def ffb(ax,x,y,name,kind="D",w=1.15,h=1.5,qn=True,neg=False,title=True,lead=0.32):
    """Flip-flop box, lower-left (x,y). Returns pin dict (outer ends of the stubs)."""
    ax.add_patch(mp.Rectangle((x,y),w,h,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    P={}
    if kind in ("D","T"):
        yd,yc=y+0.74*h,y+0.26*h; pins={kind:yd}
    elif kind=="JK":
        pins={"J":y+0.8*h,"K":y+0.2*h}; yc=y+0.5*h
    elif kind=="SR":
        pins={"S":y+0.8*h,"R":y+0.2*h}; yc=y+0.5*h
    for k,yy in pins.items():
        L(ax,[(x-lead,yy),(x,yy)]); T(ax,x+0.1,yy,k,size=8.2,ha="left",zorder=6); P[k]=(x-lead,yy)
    # clock pin
    cx0=x-lead
    if neg:
        ax.add_patch(mp.Circle((x-0.07,yc),0.07,fc="white",ec=INK,lw=1.2,zorder=5)); L(ax,[(cx0,yc),(x-0.14,yc)])
    else:
        L(ax,[(cx0,yc),(x,yc)])
    ax.add_patch(mp.Polygon([(x,yc-0.13),(x+0.2,yc),(x,yc+0.13)],closed=False,fc="none",ec=INK,lw=1.2,zorder=6))
    P["CK"]=(cx0,yc)
    L(ax,[(x+w,y+0.76*h),(x+w+lead,y+0.76*h)]); T(ax,x+w-0.1,y+0.76*h,"Q",size=8.2,ha="right",zorder=6); P["Q"]=(x+w+lead,y+0.76*h)
    if qn:
        L(ax,[(x+w,y+0.24*h),(x+w+lead,y+0.24*h)]); T(ax,x+w-0.1,y+0.24*h,"Q$'$",size=8.2,ha="right",zorder=6); P["QN"]=(x+w+lead,y+0.24*h)
    if title and name: T(ax,x+w/2,y+h+0.2,name,size=8.0)
    return P
def gn(ax,kind,x,y,n=2,sp=None,w=1.1,lead=0.4):
    """n-input AND/OR/NAND/NOR with left edge x, centred on y. Returns (input points, out point)."""
    kind=kind.upper(); h=max(0.9,n*0.4+0.2) if n>2 else 0.9
    if sp is None: sp=0.45 if n==2 else 0.4
    top,bot=y+h/2,y-h/2
    bub=kind in("NAND","NOR"); bw=0.18 if bub else 0.0; wb=w-bw
    if kind in("AND","NAND"):
        r=h/2; th=_np.linspace(_np.pi/2,-_np.pi/2,30)
        arc=_np.array([(x+wb-r+r*_np.cos(q),y+r*_np.sin(q)) for q in th])
        pts=_np.vstack([[(x,top)],arc,[(x,bot)]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3)); lx=lambda yy:x
    else:
        t=_np.linspace(-1,1,24)
        back=_np.array([(x+0.2*wb*(1-q*q),y+q*h/2) for q in t])
        def bez(p0,p1,p2):
            return _np.array([((1-s)**2*_np.array(p0)+2*s*(1-s)*_np.array(p1)+s*s*_np.array(p2)) for s in _np.linspace(0,1,24)])
        up=bez((x,top),(x+0.55*wb,top),(x+wb,y)); lo=bez((x+wb,y),(x+0.55*wb,bot),(x,bot))
        pts=_np.vstack([up,lo,back[::-1][1:]])
        ax.add_patch(mp.Polygon(pts,closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
        lx=lambda yy:x+0.2*wb*(1-((yy-y)/(h/2))**2)
    ins=[]
    for k in range(n):
        yy=y+(n-1)/2*sp-k*sp
        L(ax,[(x-lead,yy),(lx(yy),yy)]); ins.append((x-lead,yy))
    if bub: ax.add_patch(mp.Circle((x+wb+bw/2,y),bw/2,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x+w,y),(x+w+lead,y)])
    return ins,(x+w+lead,y)
def inv(ax,x,y,w=0.55,h=0.6,lead=0.25):
    """Inverter (triangle+bubble), left edge x. Returns (in, out)."""
    ax.add_patch(mp.Polygon([(x,y+h/2),(x,y-h/2),(x+w-0.14,y)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ax.add_patch(mp.Circle((x+w-0.07,y),0.07,fc="white",ec=INK,lw=1.4,zorder=4))
    L(ax,[(x-lead,y),(x,y)]); L(ax,[(x+w,y),(x+w+lead,y)])
    return (x-lead,y),(x+w+lead,y)
def sopc(ax,terms,names,x0=0.0,y0=0.0,out="F",nand=False):
    """AND-OR circuit of a sum of products. terms: list of lists of (var_index, polarity 1/0)."""
    nv=len(names); xs={}
    top=y0
    for i,v in enumerate(names):
        xt=x0+i*0.95; xc=xt+0.5; xs[(i,1)]=xt; xs[(i,0)]=xc
        T(ax,xt,top+1.15,v,size=9)
        L(ax,[(xt,top+0.95),(xt,top-0.2)]); 
        yb=top+0.55
        L(ax,[(xt,yb),(xc,yb)]); dot(ax,xt,yb)
        # downward inverter triangle on the complement line
        ax.add_patch(mp.Polygon([(xc-0.14,yb),(xc+0.14,yb),(xc,yb-0.28)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xc,yb-0.35),0.07,fc="white",ec=INK,lw=1.3,zorder=4))
    ybus=top-0.2
    for i in range(nv):
        L(ax,[(xs[(i,0)],top+0.13),(xs[(i,0)],None or top-0.2)])
    # extend buses downward later
    m=len(terms); sp=max(1.15,max(len(t) for t in terms)*0.42+0.3)
    gy=[top-0.9-k*sp for k in range(m)]
    xg=x0+nv*0.95+0.35
    bottom=gy[-1]-0.7
    for key,xx in xs.items(): L(ax,[(xx,top-0.2),(xx,bottom)])
    outs=[]
    for k,t in enumerate(terms):
        if len(t)==1:
            i,p=t[0]; yy=gy[k]; L(ax,[(xs[(i,p)],yy),(xg+1.5,yy)]); dot(ax,xs[(i,p)],yy)
            T(ax,xg+0.5,yy+0.2,("%s"%names[i])+("" if p else "$'$"),size=7.2,color=MUTED)
            outs.append((xg+1.5,yy)); continue
        ins,o=gn(ax,"NAND" if nand else "AND",xg,gy[k],n=len(t),w=1.0,lead=0.2)
        for (px,py),(i,p) in zip(ins,t):
            L(ax,[(xs[(i,p)],py),(px,py)]); dot(ax,xs[(i,p)],py)
        outs.append(o)
    xo=max(o[0] for o in outs)+0.55
    if m==1:
        L(ax,[outs[0],(xo+0.3,outs[0][1])]); yc=outs[0][1]
        T(ax,xo+0.4,yc,out,ha="left",size=9)
        return
    yc=sum(gy)/m
    ins,o=gn(ax,"NAND" if nand else "OR",xo,yc,n=m,sp=sp,w=1.1,lead=0.2)
    for (px,py),(ox,oy) in zip(ins,outs):
        L(ax,[(ox,oy),(px,py)] if abs(py-oy)<1e-6 else [(ox,oy),(px-0.0,oy),(px,py)])
    T(ax,o[0]+0.1,o[1],out,ha="left",size=9)
def kmap(ax,x0,y0,nv,ones,dcs=(),groups=(),names="ABCD",cs=0.62,title=None):
    g=[0,1,3,2]
    if nv==2: rows,cols,cb=[0,1],[0,1],1
    elif nv==3: rows,cols,cb=[0,1],g,2
    else: rows,cols,cb=g,g,2
    R,C=len(rows),len(cols)
    ri={v:i for i,v in enumerate(rows)}; ci={v:i for i,v in enumerate(cols)}
    for r in range(R):
        for c in range(C):
            m=rows[r]*(2**cb)+cols[c]; x=x0+c*cs; y=y0+(R-1-r)*cs
            ax.add_patch(mp.Rectangle((x,y),cs,cs,fc="white",ec=INK,lw=1.0,zorder=2))
            if m in ones: T(ax,x+cs/2,y+cs/2-0.02,"1",size=9.5,zorder=6,color=INK)
            elif m in dcs: T(ax,x+cs/2,y+cs/2-0.02,"X",size=9,zorder=6,color=MUTED)
            else: T(ax,x+cs/2,y+cs/2-0.02,"0",size=8.2,zorder=6,color="#9aa3b0")
            T(ax,x+cs-0.04,y+0.1,str(m),size=6.9,ha="right",color=MUTED,zorder=6)
    fmt=lambda v,b:format(v,"0%db"%b)
    rb=1 if nv<4 else 2
    for c in range(C): T(ax,x0+c*cs+cs/2,y0+R*cs+0.14,fmt(cols[c],cb),size=7.6)
    for r in range(R): T(ax,x0-0.1,y0+(R-1-r)*cs+cs/2,fmt(rows[r],rb),size=7.6,ha="right")
    rn=names[:nv-cb]; cn=names[nv-cb:nv]
    T(ax,x0-0.1,y0+R*cs+0.14,rn+"\\"+cn,size=7.6,ha="right")
    if title: T(ax,x0+C*cs/2,y0-0.22,title,size=8.4)
    def runs(idx,n):
        s=sorted(set(idx))
        if len(s)==n: return [(0,n-1)]
        rr=[]; st=pv=s[0]
        for v in s[1:]:
            if v==pv+1: pv=v
            else: rr.append((st,pv)); st=pv=v
        rr.append((st,pv)); return rr
    for gi,(cells,col) in enumerate(groups):
        rs=[ri[m>>cb] for m in cells]; cc=[ci[m&(2**cb-1)] for m in cells]
        ins=0.05+0.035*(gi%3)
        for (r0,r1) in runs(rs,R):
            for (c0,c1) in runs(cc,C):
                ax.add_patch(mp.FancyBboxPatch((x0+c0*cs+ins,y0+(R-1-r1)*cs+ins),(c1-c0+1)*cs-2*ins,(r1-r0+1)*cs-2*ins,boxstyle="round,pad=0,rounding_size=0.12",fc="none",ec=col,lw=1.7,zorder=7))
def clock(ax,x0,y,n,h=0.55,w=1.0,label="CLK"):
    pts=[]
    for i in range(n): pts+=[(x0+i*w,y),(x0+i*w,y+h),(x0+i*w+w/2,y+h),(x0+i*w+w/2,y)]
    pts.append((x0+n*w,y)); L(ax,pts); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def wave(ax,y,tr,xend,label,x0=0.0,h=0.55,color=ACCENT):
    pts=[(tr[0][0],y+tr[0][1]*h)]; lev=tr[0][1]
    for t,l in tr[1:]:
        pts+=[(t,y+lev*h),(t,y+l*h)]; lev=l
    pts.append((xend,y+lev*h)); L(ax,pts,color=color); T(ax,x0-0.12,y+h/2,label,ha="right",size=8)
def guides(ax,xs,ytop,ybot):
    for x in xs: ax.plot([x,x],[ybot,ytop],ls=(0,(3,3)),lw=0.7,color="#aab0ba",zorder=0)
def statediag(ax,names,edges,pos=None,r=0.42,gap=2.2,rad_scale=0.32,loopdir=1):
    """edges: list of (i,j,label). Nodes on a row unless pos given."""
    if pos is None: pos=[(k*gap,0.0) for k in range(len(names))]
    cs=[]
    for (px,py),nm in zip(pos,names):
        c=mp.Circle((px,py),r,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3); ax.add_patch(c); cs.append(c); T(ax,px,py,nm,size=8.6,zorder=6)
    pair={(i,j) for i,j,_ in edges}
    for i,j,lab in edges:
        (x1,y1),(x2,y2)=pos[i],pos[j]
        if i==j:
            d=loopdir; cx,cy=x1,y1+d*(r+0.05)
            ax.add_patch(mp.Arc((cx,cy),0.7,0.7,theta1=0 if d>0 else 180,theta2=180 if d>0 else 360,color=INK,lw=1.3,zorder=2))
            ax.annotate("",xy=(cx+0.35,cy-d*0.02),xytext=(cx+0.35,cy+d*0.18),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,mutation_scale=9))
            T(ax,cx,cy+d*0.55,lab,size=7.6)
            continue
        dx,dy=x2-x1,y2-y1; dist=(dx*dx+dy*dy)**0.5
        back=(j,i) in pair
        far=abs(i-j)>1
        rad=0.0
        if back or far: rad=-rad_scale*(1 if not far else 1.0+0.25*(abs(i-j)-1))
        if far and not back: rad=-rad_scale*1.6
        ax.add_patch(mp.FancyArrowPatch((x1,y1),(x2,y2),patchA=cs[i],patchB=cs[j],arrowstyle="-|>",mutation_scale=10,color=INK,lw=1.3,connectionstyle="arc3,rad=%g"%rad,zorder=2,shrinkA=0,shrinkB=0))
        mx,my=(x1+x2)/2,(y1+y2)/2
        if rad==0: lx,ly=mx,my+0.22
        else:
            nx,ny=dy/dist,-dx/dist; sg=1 if rad>0 else -1
            lx,ly=mx+0.5*rad*dy+0.2*sg*nx,my-0.5*rad*dx+0.2*sg*ny
        T(ax,lx,ly,lab,size=7.6,bbox=dict(fc="white",ec="none",pad=0.5),zorder=7)

def seqcirc(ax,kind,names,fin,zterms=None,extra=(),zname="Z",neg=False,clkname="CLK",ffnames=None):
    """Synchronous circuit: FFs left to right named `names` (Q-bus variables), extra input variables, logic per pin.
    fin[f] = {pin: terms | '0' | '1'} ; terms = list of lists of (var_index, polarity). Returns xmax."""
    nq=len(names); allv=list(names)+list(extra); nv=len(allv)
    pins={"T":["T"],"D":["D"],"JK":["J","K"],"SR":["S","R"]}[kind]
    yb={}; y=-0.75
    for i in range(nv):
        yb[(i,1)]=y; y-=0.5 if i<nq else 1.0
        yb[(i,0)]=y; y-=0.5
    ytop=y-0.5
    def bw(terms):
        if not isinstance(terms,list): return 0.6
        Lt=sum(len(t) for t in terms); m=len(terms)
        return 0.12*Lt+0.35+1.2+(0.35+1.1 if m>1 else 0)
    allt=[fin[f][p] for f in range(nq) for p in pins]
    if zterms: allt.append(zterms)
    Wb=max(bw(t) for t in allt)
    def hb(terms): return 1.2 if not isinstance(terms,list) or len(terms)==1 else len(terms)*1.45
    Hrow=max(hb(t) for t in allt)
    Wf=Wb+0.8+1.47+1.0
    X0=2.3+Wb+0.8
    def blk(terms,xs,yt):
        m=len(terms); Lt=sum(len(t) for t in terms); k=0; outs=[]; xg=xs+0.12*Lt+0.35
        pitch=1.45
        for gi,t in enumerate(terms):
            yg=yt-0.7-gi*pitch
            if len(t)==1:
                xd=xs+0.12*k; k+=1; v,p=t[0]
                L(ax,[(xd,yb[(v,p)]),(xd,yg),(xg+1.2,yg)]); dot(ax,xd,yb[(v,p)]); outs.append((xg+1.2,yg)); continue
            ins,o=gn(ax,"AND",xg,yg,n=len(t),w=0.8,lead=0.2)
            for (px,py),(v,p) in zip(ins,t):
                xd=xs+0.12*k; k+=1
                L(ax,[(xd,yb[(v,p)]),(xd,py),(px,py)]); dot(ax,xd,yb[(v,p)])
            outs.append(o)
        if m==1: return outs[0]
        xo=xg+1.2+0.35; yc=yt-0.7-(m-1)/2*pitch
        ins,o=gn(ax,"OR",xo,yc,n=m,sp=pitch if m>2 else 0.45,w=0.9,lead=0.2)
        for (px,py),(ox,oy) in zip(ins,outs):
            xm=px-0.12
            L(ax,[(ox,oy),(xm,oy),(xm,py),(px,py)] if abs(py-oy)>1e-6 else [(ox,oy),(px,py)])
        return o
    xend=X0+nq*Wf+(Wb+0.6 if zterms else 0.3)
    Pfs=[]
    for f in range(nq):
        xf=X0+f*Wf
        P=ffb(ax,xf,0,(ffnames[f] if ffnames else 'FF'+names[f][1:]),kind,neg=neg); Pfs.append(P)
        xq=P["Q"][0]
        L(ax,[P["Q"],(xq+0.42,P["Q"][1]),(xq+0.42,yb[(f,1)])]); dot(ax,xq+0.42,yb[(f,1)])
        L(ax,[P["QN"],(xq+0.18,P["QN"][1]),(xq+0.18,yb[(f,0)])]); dot(ax,xq+0.18,yb[(f,0)])
        T(ax,xq+0.55,P["Q"][1]+0.22,names[f],size=8,ha="left")
        for pi,p in enumerate(pins):
            terms=fin[f][p]; pp=P[p]
            if not isinstance(terms,list):
                L(ax,[(pp[0]-0.3,pp[1]),pp]); T(ax,pp[0]-0.38,pp[1],terms,size=8.6,ha="right"); continue
            xs=xf-0.8-Wb; yt=ytop-pi*(Hrow+0.3)
            o=blk(terms,xs,yt); xv=pp[0]-0.3-0.25*pi
            L(ax,[o,(xv,o[1]),(xv,pp[1]),pp])
        # clock from the bottom bus
        ck=P["CK"]; yclk=ytop-len(pins)*(Hrow+0.3)-0.2
        L(ax,[ck,(ck[0],yclk)])
    L(ax,[(Pfs[0]["CK"][0],yclk),(Pfs[-1]["CK"][0],yclk)])
    for f in range(nq): dot(ax,Pfs[f]["CK"][0],yclk)
    L(ax,[(Pfs[0]["CK"][0]-0.6,yclk),(Pfs[0]["CK"][0],yclk)]); T(ax,Pfs[0]["CK"][0]-0.65,yclk,clkname,size=8.2,ha="right")
    xl=1.0
    for (i,p),yy in yb.items():
        nm=allv[i] if p else r"$\overline{%s}$"%allv[i]
        L(ax,[(xl+0.5,yy),(xend,yy)],lw=1.1,color="#4a5565"); T(ax,xl+0.42,yy,nm,size=7.8,ha="right")
    for j,e in enumerate(extra):
        i=nq+j; xt=xl+0.9; yt_,yc_=yb[(i,1)],yb[(i,0)]
        L(ax,[(xt,yt_),(xt,yt_-0.2)]); dot(ax,xt,yt_)
        ax.add_patch(mp.Polygon([(xt-0.13,yt_-0.2),(xt+0.13,yt_-0.2),(xt,yt_-0.45)],closed=True,fc="#f6f8fc",ec=INK,lw=1.3,zorder=3))
        ax.add_patch(mp.Circle((xt,yt_-0.52),0.07,fc="white",ec=INK,lw=1.3,zorder=4)); L(ax,[(xt,yt_-0.59),(xt,yc_)]); dot(ax,xt,yc_)
    if zterms:
        o=blk(zterms,xend-Wb-0.3,ytop); L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],zname,size=9,ha="left")
        xend=o[0]+0.9
    return xend,yclk

def mux(ax,x,y,n,labels,sels,out="Y",sp=0.5,w=1.3,name=None):
    h=n*sp+0.3; top=y+h/2
    ax.add_patch(mp.Polygon([(x,y-h/2),(x,top),(x+w,top-0.3),(x+w,y-h/2+0.3)],closed=True,fc="#f6f8fc",ec=INK,lw=1.4,zorder=3))
    ins=[]
    for i in range(n):
        yy=top-0.15-sp/2-i*sp; L(ax,[(x-0.35,yy),(x,yy)]); ins.append((x-0.35,yy))
        T(ax,x+0.12,yy,str(i),size=7.4,ha="left",color=MUTED,zorder=6)
        if labels[i] is not None: T(ax,x-0.42,yy,labels[i],size=8,ha="right")
    sp_=[]
    k=len(sels)
    for j,sname in enumerate(sels):
        xs=x+w*(0.25+0.5*(j+0.5)/k*1.0)
        yb=(y-h/2)+0.3*(xs-x)/w
        L(ax,[(xs,yb),(xs,y-h/2-0.4)]); sp_.append((xs,y-h/2-0.4)); T(ax,xs,y-h/2-0.6,sname,size=8)
    L(ax,[(x+w,y),(x+w+0.4,y)]); T(ax,x+w+0.48,y,out,size=8.6,ha="left")
    T(ax,x+w*0.5,y+h/2+0.2,name or ("%d:1 MUX"%n),size=7.6)
    return dict(ins=ins,sel=sp_,out=(x+w+0.4,y))
def bubble(ax,x,y): ax.add_patch(mp.Circle((x,y),0.07,fc="white",ec=INK,lw=1.3,zorder=4))

fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.6,19.0),ylim=(-1.2,4.6))
box(ax,0.0,2.4,3.0,1.2,"Signal\nconditioner\n(Schmitt trigger)",size=7.4)
box(ax,0.0,0.0,3.0,1.2,"Crystal\noscillator",size=7.8)
box(ax,4.4,0.0,2.6,1.2,"Decade\ndivider",size=7.8)
box(ax,8.0,0.0,2.6,1.2,"Gate flip-flop\n(T = 1 s)",size=7.4)
ins,o=gn(ax,"AND",8.6,3.0,n=2,w=0.9,lead=0.4)
box(ax,11.8,2.4,2.6,1.2,"Decade\ncounter",size=7.8); box(ax,15.0,2.4,2.6,1.2,"Latch +\ndisplay",size=7.6)
arr(ax,(3.0,3.0),(ins[0][0],ins[0][1])); arr(ax,(3.0,0.6),(4.4,0.6)); arr(ax,(7.0,0.6),(8.0,0.6))
L(ax,[(9.3,1.2),(9.3,2.0),(7.6,2.0),(7.6,ins[1][1]),ins[1]]) if False else L(ax,[(9.3,1.2),(9.3,1.8),(6.6,1.8),(6.6,ins[1][1]),ins[1]])
arr(ax,o,(11.8,3.0)); arr(ax,(14.4,3.0),(15.0,3.0))
T(ax,7.0,4.2,"unknown frequency f$_x$",size=7.8,color=MUTED)
```

**Working.**

1. The unknown signal (sine, any shape) is squared by a **Schmitt-trigger signal conditioner**, giving clean pulses, one per cycle.
2. A crystal oscillator (say 1 MHz) is divided by decade dividers to give very accurate gate pulses; the gate flip-flop output is high for exactly $T = 1$ s (or 0.1 s, 10 s for other ranges).
3. The AND gate passes the input pulses to the decade counter only while the gate is high; the counter counts $N$ pulses.
4. At the end of the gate the count is transferred to the latch/display and the counter is reset for the next measurement.

$$f_x = \frac{N}{T}$$

For $T=1$ s the display reads $f_x$ directly in hertz; with $T=0.1$ s a decimal point is shifted. The uncertainty is $\pm 1$ count, i.e. $\pm 1/T$ hertz, plus the crystal error. At *low* frequencies the **period-measuring mode** is used instead (count clock pulses during one input period), which gives a better resolution.



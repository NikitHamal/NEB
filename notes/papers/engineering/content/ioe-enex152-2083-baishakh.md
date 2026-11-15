---
file: NEBians-IOE-Past-Paper-Digital-Logic-ENEX152-2083-Baishakh.pdf
subject: Digital Logic
level: BE · Year I / Part II
code: ENEX 152
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Convert the following gray codes to binary codes. [[2+2]]

a) 10011

b) 110001

@q 2
Differentiate between analog and digital signal. Convert 159 to excess-3 code. [[1+2]]

@q 3
Show that NAND and NOR gates are universal gates. [[3]]

@q 4
Minimize the function $F(A,B,C,D) = \sum m(1, 2, 4, 5, 6, 8, 10, 11, 13, 15)$ using K-Map and realize it with suitable logic gates. [[5]]

@q 5
Differentiate between encoder and decoder. Design octal to binary encoder with necessary diagrams. [[2+4]]

@q 6
Implement a full subtractor circuit using multiplexer. [[4]]

@q 7
Differentiate between latch and flipflop. Modify a D flip-flop such that it functions as a JK flip-flop. [[2+5]]

@q 8
Explain the working of 4-bit SIPO register with timing diagram of 1010 data input. [[5]]

@q 9
Describe the operation of asynchronous BCD (decade) counter with necessary diagrams. [[5]]

@q 10
Design the synchronous mod-10 up counter using T flip-flop and draw its timing diagram also. [[7]]

@q 11
Design a synchronous sequential machine that has 1 bit serial input X and output Z which will be high when the input contains the message 011 (Use T Flip Flop). [[7]]

@q 12
Explain about the main characteristics of digital logic families. [[4]]

<!-- SOLUTIONS -->

@s 1
**(a)** Rule: the MSB of the binary code equals the MSB of the Gray code; every other binary bit is $b_i = b_{i-1} \oplus g_i$.

- $b_1 = g_1 = 1$
- $b_2 = b_1 \oplus g_2 = 1 \oplus 0 = 1$
- $b_3 = b_2 \oplus g_3 = 1 \oplus 0 = 1$
- $b_4 = b_3 \oplus g_4 = 1 \oplus 1 = 0$
- $b_5 = b_4 \oplus g_5 = 0 \oplus 1 = 1$

$$(10011)_{Gray} = (11101)_2$$

**(b)** Rule: the MSB of the binary code equals the MSB of the Gray code; every other binary bit is $b_i = b_{i-1} \oplus g_i$.

- $b_1 = g_1 = 1$
- $b_2 = b_1 \oplus g_2 = 1 \oplus 1 = 0$
- $b_3 = b_2 \oplus g_3 = 0 \oplus 0 = 0$
- $b_4 = b_3 \oplus g_4 = 0 \oplus 0 = 0$
- $b_5 = b_4 \oplus g_5 = 0 \oplus 0 = 0$
- $b_6 = b_5 \oplus g_6 = 0 \oplus 1 = 1$

$$(110001)_{Gray} = (100001)_2$$

*Check by conversion back:* $11101 \to$ Gray: $1,\ 1\oplus1=0,\ 1\oplus1=0,\ 1\oplus0=1,\ 0\oplus1 = 1$ gives 10011 ✓; $100001\to 110001$ ✓.


@s 2
| Point | Analog signal | Digital signal |
|---|---|---|
| Values | Continuous in amplitude and time | Discrete levels (two for binary: 0 and 1) |
| Representation | Continuously varying voltage/current (sine wave) | Sequence of bits, square pulses |
| Noise immunity | Poor, noise adds to the signal and cannot be removed | Good, a threshold decides 0 or 1, so noise is rejected |
| Storage and processing | Difficult; processing by analog circuits | Easy; memories, microprocessors, error correction |
| Accuracy | Limited by component tolerance and drift | Set by the number of bits, can be made as high as required |
| Examples | Microphone output, temperature sensor, AM/FM radio | Computer data, CD/DVD, digital TV |

**Excess-3 code of 159.**

Excess-3 code = BCD code of the digit + 3 (0011), taken digit by digit.

| Digit | Digit + 3 | Excess-3 |
|---|---|---|
| 1 | 4 | 0100 |
| 5 | 8 | 1000 |
| 9 | 12 | 1100 |

$$(159)_{10} = (0100 1000 1100)_{XS-3}$$

The codeword has 12 bits, each decimal digit using its own 4-bit group, so $159 \to 0100\ 1000\ 1100$.


@s 3
A gate type is **universal** if every Boolean function (that is, NOT, AND and OR) can be built from it alone.

**(a) NAND is universal.** With $\overline{AA} = \overline{A}$ and De Morgan:

$$\begin{gathered}\text{NOT: } \overline{A\cdot A} = \overline{A} \\ \text{AND: } \overline{\overline{A\cdot B}} = AB \\ \text{OR: } \overline{\overline{A}\cdot\overline{B}} = A + B\end{gathered}$$

NOT: tie both inputs together. AND: a NAND followed by a NAND used as inverter. OR: invert each input with a NAND-inverter, then NAND the results.

```figure caption="Basic gates built only from NAND gates (NOT, AND, OR)."
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

def nt(ax,x,y):
    ins,o=gn(ax,"NAND",x,y,n=2,w=0.9,lead=0.25)
    xl=ins[0][0]-0.15
    L(ax,[ins[0],(xl,ins[0][1]),(xl,ins[1][1]),ins[1]]); dot(ax,xl,y); L(ax,[(xl,y),(xl-0.35,y)])
    return (xl-0.35,y),o
fig,ax=ckt_canvas(5.9,3.7,xlim=(-1.6,15.2),ylim=(-0.4,6.8))
T(ax,0.2,6.4,"NOT",size=8.2,color=MUTED); T(ax,5.0,6.4,"AND",size=8.2,color=MUTED); T(ax,5.0,3.1,"OR",size=8.2,color=MUTED)
i,o=nt(ax,1.0,5.2); T(ax,i[0]-0.1,5.2,"A",ha="right"); T(ax,o[0]+0.1,5.2,"$\\overline{A}$",ha="left")

ins,o=gn(ax,"NAND",5.2,5.2,n=2,w=0.9,lead=0.3); T(ax,ins[0][0]-0.1,ins[0][1],"A",ha="right"); T(ax,ins[1][0]-0.1,ins[1][1],"B",ha="right")
i2,o2=nt(ax,o[0]+1.0,5.2); L(ax,[o,i2]); T(ax,o2[0]+0.1,5.2,"$AB$",ha="left")

ia,oa=nt(ax,3.2,2.4); ib,ob=nt(ax,3.2,0.8); T(ax,ia[0]-0.1,2.4,"A",ha="right"); T(ax,ib[0]-0.1,0.8,"B",ha="right")
ins,o=gn(ax,"NAND",7.6,1.6,n=2,w=0.9,lead=0.3)
L(ax,[oa,(ins[0][0]-0.3,2.4),(ins[0][0]-0.3,ins[0][1]),ins[0]]) if False else L(ax,[oa,(6.4,oa[1]),(6.4,ins[0][1]),ins[0]])
L(ax,[ob,(6.4,ob[1]),(6.4,ins[1][1]),ins[1]]) if False else L(ax,[ob,(6.2,ob[1]),(6.2,ins[1][1]),ins[1]])
T(ax,o[0]+0.1,1.6,"$A+B$",ha="left")
```

**(b) NOR is universal.**

$$\begin{gathered}\text{NOT: } \overline{A+A} = \overline{A} \\ \text{OR: } \overline{\overline{A+B}} = A + B \\ \text{AND: } \overline{\overline{A}+\overline{B}} = AB\end{gathered}$$

NOT: tie the inputs. OR: NOR followed by a NOR-inverter. AND: invert each input with a NOR-inverter, then NOR the results.

```figure caption="Basic gates built only from NOR gates (NOT, AND, OR)."
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

def nt(ax,x,y):
    ins,o=gn(ax,"NOR",x,y,n=2,w=0.9,lead=0.25)
    xl=ins[0][0]-0.15
    L(ax,[ins[0],(xl,ins[0][1]),(xl,ins[1][1]),ins[1]]); dot(ax,xl,y); L(ax,[(xl,y),(xl-0.35,y)])
    return (xl-0.35,y),o
fig,ax=ckt_canvas(5.9,3.7,xlim=(-1.6,15.2),ylim=(-0.4,6.8))
T(ax,0.2,6.4,"NOT",size=8.2,color=MUTED); T(ax,5.0,6.4,"AND",size=8.2,color=MUTED); T(ax,5.0,3.1,"OR",size=8.2,color=MUTED)
i,o=nt(ax,1.0,5.2); T(ax,i[0]-0.1,5.2,"A",ha="right"); T(ax,o[0]+0.1,5.2,"$\\overline{A}$",ha="left")

ia,oa=nt(ax,3.2,5.6); ib,ob=nt(ax,3.2,4.4); T(ax,ia[0]-0.1,5.6,"A",ha="right"); T(ax,ib[0]-0.1,4.4,"B",ha="right")
ins,o=gn(ax,"NOR",7.6,5.0,n=2,w=0.9,lead=0.3)
L(ax,[oa,(6.4,oa[1]),(6.4,ins[0][1]),ins[0]]); L(ax,[ob,(6.2,ob[1]),(6.2,ins[1][1]),ins[1]])
T(ax,o[0]+0.1,5.0,"$AB$",ha="left")

ins,o=gn(ax,"NOR",5.2,1.6,n=2,w=0.9,lead=0.3); T(ax,ins[0][0]-0.1,ins[0][1],"A",ha="right"); T(ax,ins[1][0]-0.1,ins[1][1],"B",ha="right")
i2,o2=nt(ax,o[0]+1.0,1.6); L(ax,[o,i2]); T(ax,o2[0]+0.1,1.6,"$A+B$",ha="left")
```

Since NOT, AND and OR are available from either gate, any logic function can be realised with NAND gates alone or with NOR gates alone; hence both are universal gates (they are also cheaper in IC form).


@s 4
**Step 1 - K-map.** Enter 1 in each minterm cell, Gray-code ordered rows and columns so neighbouring cells differ in one variable.

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

kmap(ax,0.9,0.4,4,[1, 2, 4, 5, 6, 8, 10, 11, 13, 15],[],[([13, 15], '#d9534f'), ([11, 15], '#1d6fb8'), ([8, 10], '#2e8b57'), ([4, 6], '#b8860b'), ([2, 6], '#6a5acd'), ([1, 5], '#008b8b')],names='ABCD',cs=0.72,title='F')
```

**Step 2 - groups (largest possible, power of two).**

- Group 1 (loop colour red), cells 13, 15: variables that do not change survive, giving $ABD$.
- Group 2 (loop colour blue), cells 11, 15: variables that do not change survive, giving $ACD$.
- Group 3 (loop colour green), cells 8, 10: variables that do not change survive, giving $A\overline{B}\overline{D}$.
- Group 4 (loop colour gold), cells 4, 6: variables that do not change survive, giving $\overline{A}B\overline{D}$.
- Group 5 (loop colour violet), cells 2, 6: variables that do not change survive, giving $\overline{A}C\overline{D}$.
- Group 6 (loop colour teal), cells 1, 5: variables that do not change survive, giving $\overline{A}\overline{C}D$.

**Step 3 - minimised expression.**

$$\boxed{F(A,B,C,D) = ABD + ACD + A\overline{B}\overline{D} + \overline{A}B\overline{D} + \overline{A}C\overline{D} + \overline{A}\overline{C}D}$$

**Step 4 - realisation with logic gates (AND-OR, two-level).** The complemented inputs come from NOT gates.

```figure caption="AND-OR realisation of F = ABD + ACD + AB'D' + A'BD' + A'CD' + A'C'D"
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
fig,ax=ckt_canvas(5.9,7.51,xlim=(-0.5,8.8),ylim=(-9.7,1.8))

sopc(ax,[[(0, 1), (1, 1), (3, 1)], [(0, 1), (2, 1), (3, 1)], [(0, 1), (1, 0), (3, 0)], [(0, 0), (1, 1), (3, 0)], [(0, 0), (2, 1), (3, 0)], [(0, 0), (2, 0), (3, 1)]],['A', 'B', 'C', 'D'],out='F')
```

*Equivalent NAND-only form.* Replacing every AND and the OR by NAND gates (double inversion, De Morgan) gives the same function with 7 NAND gates (plus the input inverters).


@s 5
| Point | Encoder | Decoder |
|---|---|---|
| Function | Converts $2^n$ (or fewer) input lines into an $n$-bit binary code | Converts an $n$-bit binary code into one of $2^n$ output lines |
| Inputs / outputs | $2^n$ inputs, $n$ outputs | $n$ inputs, $2^n$ outputs |
| Active lines | Only one input is active at a time | Only one output is active for a given code |
| Built from | OR gates | AND (or NAND) gates |
| Example | Octal-to-binary (8:3), keyboard encoder | 3-to-8, BCD-to-7-segment decoder |
| Use | Keyboards, interrupt priority, data compression | Address decoding, memory chip select, display drivers |

**Octal-to-binary encoder (8-line to 3-line).** Eight inputs $D_0\dots D_7$ (only one high at a time) produce a 3-bit code $A_2A_1A_0$ equal to the number of the active input.

| D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 | A2 | A1 | A0 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |

From the table each output is the OR of the inputs whose code has a 1 in that position:

$$\begin{gathered}A_2 = D_4 + D_5 + D_6 + D_7 \\ A_1 = D_2 + D_3 + D_6 + D_7 \\ A_0 = D_1 + D_3 + D_5 + D_7\end{gathered}$$

$D_0$ needs no gate (the code is 000 when $D_0$ is active or when no input is active). Three 4-input OR gates give the encoder.

```figure caption="Octal-to-binary encoder: three 4-input OR gates."
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

fig,ax=ckt_canvas(5.9,3.4,xlim=(-1,11),ylim=(-0.6,7.4))
ys=[7.0-0.75*k for k in range(8)]   # D0..D7 top to bottom? place D7 at top
ys=[6.8-0.75*(7-i) for i in range(8)]
xs={}
for i,y in enumerate(ys):
    T(ax,0.0,y,"D%d"%i,ha="right",size=8.2)
    L(ax,[(0.1,y),(0.6+0.22*i,y)],lw=1.1,color="#4a5565")
for i,y in enumerate(ys): xs[i]=0.6+0.22*i
for i in range(8): L(ax,[(xs[i],ys[i]),(xs[i],-0.2)],lw=1.1,color="#4a5565")
outs=[("A2",[4,5,6,7],6.0),("A1",[2,3,6,7],3.3),("A0",[1,3,5,7],0.6)]
for nm,inp,yc in outs:
    ins,o=gn(ax,"OR",5.4,yc,n=4,w=1.1,lead=0.3)
    for (px,py),i in zip(ins,inp):
        L(ax,[(xs[i],py),(px,py)],lw=1.1); dot(ax,xs[i],py)
    L(ax,[o,(o[0]+0.4,o[1])]); T(ax,o[0]+0.5,o[1],nm,ha="left",size=9)
T(ax,8.0,7.1,"D0 has no gate: all outputs 0",size=7.6,color=MUTED)
```

*Limitation.* If two inputs are high together, the output is the OR of the two codes (wrong); a **priority encoder** removes this ambiguity.


@s 6
**Full subtractor.** It subtracts $A - B - B_{in}$ and gives the difference $D$ and borrow-out $B_{out}$.

| A | B | Bin | Diff | Bout |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 |

$$\begin{gathered}D = A\oplus B\oplus B_{in} \\ B_{out} = \overline{A}B + \overline{A}B_{in} + B\,B_{in}\end{gathered}$$

**Multiplexer implementation.** Take $A$ and $B$ as the select inputs of a 4:1 multiplexer ($S_1=A$, $S_0=B$) and express each output as a function of the remaining variable $B_{in}$ for each select combination (implementation table):

| AB (select) | Diff (data input) | Bout (data input) |
|---|---|---|
| 00 | Bin | Bin |
| 01 | $\overline{B_{in}}$ | 1 |
| 10 | $\overline{B_{in}}$ | 0 |
| 11 | Bin | Bin |

Check: for $AB=00$ the rows give $D=B_{in}$ and $B_{out}=B_{in}$; for $AB=01$, $D=\overline{B_{in}}$ and $B_{out}=1$; for $AB=10$, $D=\overline{B_{in}}$ and $B_{out}=0$; for $AB=11$, $D=B_{in}$, $B_{out}=B_{in}$. These agree with the 8 rows of the truth table.

```figure caption="Full subtractor with two 4:1 multiplexers (A = S1, B = S0; the data inputs are Bin, its complement, 0 or 1)."
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
m1=mux(ax,3.0,0.6,4,['B$_{in}$', '$\\overline{B_{in}}$', '$\\overline{B_{in}}$', 'B$_{in}$'],["A","B"],out="Diff",name="4:1 MUX (difference)")
m2=mux(ax,12.0,0.6,4,['B$_{in}$', '1', '0', 'B$_{in}$'],["A","B"],out="Bout",name="4:1 MUX (borrow)")
T(ax,7.5,-2.0,"select lines A (S1) and B (S0) are common to both multiplexers",size=7.6,color=MUTED)
```

Two 4:1 multiplexers and one NOT gate realise the full subtractor.


@s 7
**Latch vs flip-flop.**

| Point | Latch | Flip-flop |
|---|---|---|
| Triggering | Level sensitive: the output follows the input the whole time the enable is active | Edge triggered: the output can change only at the rising (or falling) edge of the clock |
| Clock | Enable / gate signal (no clock edge) | Clock with edge-detector (master-slave or edge circuit) |
| Race / transparency | Transparent while enabled, so a changing input appears at the output (race-around possible) | Not transparent; samples the input only at the edge |
| Circuit | Built from cross-coupled gates (NOR or NAND) plus steering gates | Built from two latches (master + slave) or latch + edge detector |
| Synchronisation | Asynchronous or gated, hard to synchronise | Synchronous, used in counters, registers and state machines |
| Example | SR latch, gated D latch (7475) | D, JK, T flip-flop (7474, 7476) |

**Modifying a D flip-flop into a JK flip-flop.** A JK flip-flop obeys the characteristic equation

$$Q^{+} = J\overline{Q} + \overline{K}\,Q$$

A D flip-flop obeys $Q^{+} = D$. Hence if the D input is driven by the combinational logic

$$\boxed{D = J\overline{Q} + \overline{K}Q}$$

the D flip-flop behaves exactly like a JK flip-flop. Check with the excitation table:

| J | K | Q | D = J Q' + K' Q | Q⁺ | Action |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | hold |
| 0 | 0 | 1 | 1 | 1 | hold |
| 0 | 1 | 0 | 0 | 0 | reset |
| 0 | 1 | 1 | 0 | 0 | reset |
| 1 | 0 | 0 | 1 | 1 | set |
| 1 | 0 | 1 | 1 | 1 | set |
| 1 | 1 | 0 | 1 | 1 | toggle |
| 1 | 1 | 1 | 0 | 0 | toggle |

Two AND gates, one OR gate and one inverter (the logic block below) are needed, with $Q$ and $\overline{Q}$ fed back.

```figure caption="JK flip-flop from a D flip-flop: D = J Q' + K' Q."
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

fig,ax=ckt_canvas(5.9,2.8,xlim=(-1.8,9.6),ylim=(-1.2,3.9))
P=ffb(ax,5.0,0.3,"D flip-flop","D",w=1.3,h=1.8,qn=True)
Dp=P["D"]; ck=P["CK"]
# gates: J.Q' and K'.Q then OR
ins1,o1=gn(ax,"AND",0.8,3.0,n=2,w=0.9,lead=0.3)
ins2,o2=gn(ax,"AND",0.8,1.4,n=2,w=0.9,lead=0.3)
ino,oo=gn(ax,"OR",3.1,2.2,n=2,w=0.9,lead=0.3)
L(ax,[o1,(2.7,o1[1]),(2.7,ino[0][1]),ino[0]]); L(ax,[o2,(2.7,o2[1]),(2.7,ino[1][1]),ino[1]])
L(ax,[oo,(4.2,oo[1]),(4.2,Dp[1]),Dp]) if False else L(ax,[oo,(4.4,oo[1]),(4.4,Dp[1]),Dp])
T(ax,ins1[0][0]-0.1,ins1[0][1],"J",ha="right"); T(ax,ins2[1][0]-0.1,ins2[1][1],"K",ha="right")
# K' into gate2 top input via inverter
iin,iout=inv(ax,-1.2,ins2[0][1],w=0.45,h=0.45,lead=0.1); L(ax,[iout,ins2[0]]); T(ax,iin[0]-0.1,iin[1],"K",ha="right")
L(ax,[(ins2[1][0],ins2[1][1]),(ins2[1][0]-0.3,ins2[1][1])]) 
T(ax,ins2[1][0]-0.1,ins2[1][1],"",ha="right")
# feedback Q' -> gate1 lower input, Q -> gate2 lower input
qn=P["QN"]; q=P["Q"]
L(ax,[qn,(qn[0]+0.4,qn[1]),(qn[0]+0.4,-0.9),(-0.2,-0.9),(-0.2,ins1[1][1]),ins1[1]])
L(ax,[q,(q[0]+0.8,q[1]),(q[0]+0.8,-0.6)]) if False else None
L(ax,[q,(q[0]+0.8,q[1])]); T(ax,q[0]+0.9,q[1],"Q",ha="left"); T(ax,qn[0]+0.5,qn[1]-0.1,"Q$'$",ha="left")
L(ax,[(q[0]+0.5,q[1]),(q[0]+0.5,-0.55),(0.1,-0.55),(0.1,ins2[1][1]),ins2[1]]); dot(ax,q[0]+0.5,q[1])
T(ax,ck[0]-0.1,ck[1],"CLK",ha="right")
```


@s 8
**4-bit SIPO (serial-in, parallel-out) shift register.** It consists of four D flip-flops with a common clock; the output $Q$ of each stage drives the $D$ input of the next, and the serial data enter the first stage. At every rising clock edge each flip-flop copies the previous stage, so the data move one place to the right. After $n=4$ clock pulses the 4 serial bits are present together at $Q_A\dots Q_D$ (parallel output); the parallel word can be read when the 4th pulse has ended.

```figure caption="4-bit SIPO shift register built from four D flip-flops (clock common to all stages)."
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

fig,ax=ckt_canvas(5.9,2.2,xlim=(-1.6,15),ylim=(-0.2,3.0))
Ps=[ffb(ax,0.2+3.6*i,0.6,"FF"+"ABCD"[i],"D",w=1.2,h=1.5,qn=False) for i in range(4)]
for i in range(3):
    L(ax,[Ps[i]["Q"],Ps[i+1]["D"]])
for i,P in enumerate(Ps):
    L(ax,[P["Q"],(P["Q"][0]+0.5,P["Q"][1])]) if i==3 else None
    L(ax,[(P["Q"][0]+0.55,P["Q"][1]),(P["Q"][0]+0.55,0.1)]) if False else None
    T(ax,P["Q"][0]+0.12,P["Q"][1]+0.28,"Q"+"ABCD"[i],size=8.2,ha="left")
    L(ax,[P["CK"],(P["CK"][0],0.25)]); dot(ax,P["CK"][0],0.25)
L(ax,[(Ps[0]["CK"][0],0.25),(Ps[3]["CK"][0],0.25)]); T(ax,Ps[0]["CK"][0]-0.1,0.25,"CLK",ha="right")
L(ax,[(Ps[0]["D"][0]-0.7,Ps[0]["D"][1]),Ps[0]["D"]]); T(ax,Ps[0]["D"][0]-0.75,Ps[0]["D"][1],"Serial in",ha="right")
L(ax,[Ps[3]["Q"],(Ps[3]["Q"][0]+0.5,Ps[3]["Q"][1])]);
```

**Working for the serial input 1010** (the first bit applied is 1, the last 0; the register is first cleared):

| Clock pulse | Serial in | QA | QB | QC | QD |
|---|---|---|---|---|---|
| initial | - | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 0 |
| 3 | 1 | 1 | 0 | 1 | 0 |
| 4 | 0 | 0 | 1 | 0 | 1 |

After the fourth pulse $Q_AQ_BQ_CQ_D = 0101$, i.e. $Q_DQ_CQ_BQ_A = 1010 = 1010$, the word applied serially, now available in parallel.

```figure caption="Timing diagram of the 4-bit SIPO register for the serial input 1010 (QA is the first stage, QD the last; the bits appear in QD..QA after four clock pulses)."
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
fig,ax=ckt_canvas(5.9,5.72,xlim=(-1.9,4.7),ylim=(-0.3,6.2))

clock(ax,0,4.1,4)
guides(ax,[0.0, 1.0, 2.0, 3.0],4.8,-0.1)
wave(ax,2.9499999999999997,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0)],4,'QA')
wave(ax,2.0,[(0.0, 0), (1.05, 1), (2.05, 0), (3.05, 1)],4,'QB')
wave(ax,1.05,[(0.0, 0), (2.05, 1), (3.05, 0)],4,'QC')
wave(ax,0.1,[(0.0, 0), (3.05, 1)],4,'QD')
wave(ax,5.3,[(0.0, 1), (1.0, 0), (2.0, 1), (3.0, 0)],4,'Din')
```


@s 9
**Asynchronous BCD (decade, mod-10) counter.** A 4-bit ripple counter naturally counts 0 to 15. To make it count only 0 to 9, the counter is **cleared as soon as the count 10 (1010) is reached**: the outputs $Q_3$ and $Q_1$ (the first two 1s of 1010) are NANDed, and the active-low NAND output is applied to the asynchronous clear (CLR) inputs of all four flip-flops.

```figure caption="Asynchronous BCD counter: 4-bit ripple counter (JK flip-flops with J = K = 1) with a NAND gate on Q3 and Q1 driving the clear inputs."
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

fig,ax=ckt_canvas(5.9,2.8,xlim=(-1.6,19.6),ylim=(-2.4,3.0))
Ps=[ffb(ax,0.4+4.2*i,0.6,"FF%d"%i,"JK",w=1.3,h=1.7,qn=True) for i in range(4)]
for i,P in enumerate(Ps):
    T(ax,P["J"][0]-0.1,P["J"][1],"1",ha="right",size=8.2); T(ax,P["K"][0]-0.1,P["K"][1],"1",ha="right",size=8.2)
    L(ax,[P["Q"],(P["Q"][0]+0.5,P["Q"][1])]); T(ax,P["Q"][0]+0.55,P["Q"][1],"Q%d"%i,ha="left",size=8.4)
for i in range(3):
    Pa,Pb=Ps[i],Ps[i+1]
    src=Pa["QN"]; L(ax,[src,(src[0]+0.6,src[1]),(src[0]+0.6,0.05),(Pb["CK"][0]-0.5,0.05),(Pb["CK"][0]-0.5,Pb["CK"][1]),Pb["CK"]])
L(ax,[(Ps[0]["CK"][0]-0.7,Ps[0]["CK"][1]),Ps[0]["CK"]]); T(ax,Ps[0]["CK"][0]-0.75,Ps[0]["CK"][1],"CLK",ha="right")
# NAND of Q3 and Q1 -> clear (all flip-flops)
ins,o=gn(ax,"NAND",9.0,-1.3,n=2,w=0.9,lead=0.3)
q3=Ps[3]["Q"]; q1=Ps[1]["Q"]
L(ax,[(q1[0]+0.25,q1[1]),(q1[0]+0.25,ins[1][1]),ins[1]]) if False else None
L(ax,[(Ps[1]["Q"][0]+0.3,Ps[1]["Q"][1]),(Ps[1]["Q"][0]+0.3,ins[1][1]),ins[1]]); dot(ax,Ps[1]["Q"][0]+0.3,Ps[1]["Q"][1])
L(ax,[(Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1]),(Ps[3]["Q"][0]+0.3,-2.2),(8.3,-2.2),(8.3,ins[0][1]),ins[0]]) if False else None
L(ax,[(Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1]),(Ps[3]["Q"][0]+0.3,-2.0),(7.7,-2.0),(7.7,ins[0][1]),ins[0]]); dot(ax,Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1])
T(ax,o[0]+0.15,o[1],"to CLR of\nall four FFs",ha="left",size=7.8)
T(ax,13.0,-1.3,"clear (active low) when Q3Q2Q1Q0 = 1010",size=7.8,color=MUTED)
```

**Operation.**

1. The clock drives $FF_0$; each following flip-flop is clocked by $\overline{Q}$ of the previous stage, so the outputs count in binary 0000, 0001, ..., 1001.
2. On the tenth pulse the counter tries to go to 1010; the moment $Q_3=Q_1=1$, the NAND output goes low, clears all flip-flops and the counter returns to 0000. The state 1010 exists only for about one propagation delay.
3. $Q_3$ is high only for counts 8 and 9, so it gives one pulse for every ten clock pulses: **frequency division by 10**.

| Clock pulse | Q3 | Q2 | Q1 | Q0 |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 |
| 2 | 0 | 0 | 1 | 0 |
| 3 | 0 | 0 | 1 | 1 |
| 4 | 0 | 1 | 0 | 0 |
| 5 | 0 | 1 | 0 | 1 |
| 6 | 0 | 1 | 1 | 0 |
| 7 | 0 | 1 | 1 | 1 |
| 8 | 1 | 0 | 0 | 0 |
| 9 | 1 | 0 | 0 | 1 |
| 10 (momentary) | 1 | 0 | 1 | 0 |
| 10 -> 0 | 0 | 0 | 0 | 0 |

```figure caption="Timing diagram of the asynchronous BCD counter: counts 0 to 9 and returns to 0 at the tenth pulse (the 1010 state lasts only a few nanoseconds, so it is not seen as a valid count)."
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
fig,ax=ckt_canvas(5.9,2.1,xlim=(-1.9,12.7),ylim=(-0.3,5.0))

clock(ax,0,4.1,12)
guides(ax,[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0],4.8,-0.1)
wave(ax,2.9499999999999997,[(0.0, 0), (7.26, 1), (9.26, 0)],12,'Q3')
wave(ax,2.0,[(0.0, 0), (3.19, 1), (7.19, 0)],12,'Q2')
wave(ax,1.05,[(0.0, 0), (1.12, 1), (3.12, 0), (5.12, 1), (7.12, 0), (11.12, 1)],12,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (5.05, 0), (6.05, 1), (7.05, 0), (8.05, 1), (9.05, 0), (10.05, 1), (11.05, 0)],12,'Q0')
```


@s 10
**Design of the synchronous mod-10 up counter with T flip-flops.**

*Step 1 - number of flip-flops.* $2^{3} < N \le 2^{4}$ needs $n=4$ flip-flops (T flip-flops), all clocked together (synchronous). The states are $Q3Q2Q1Q0$.

*Step 2 - excitation table of the T flip-flop.*

| Q | Q⁺ | T |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

*Step 3 - state / excitation table* (for each present state the next state, and the flip-flop inputs needed from the excitation table; X = don't care):

| Q3 | Q2 | Q1 | Q0 | Q3⁺ | Q2⁺ | Q1⁺ | Q0⁺ | T3 | T2 | T1 | T0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |

The unused states (1010 to 1111) never occur, so their next-state and input entries are don't-cares (X) in the K-maps.

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
fig,ax=ckt_canvas(5.33,4.96,xlim=(0,8.6),ylim=(-0.2,8.0))

kmap(ax,0.9,4.3,4,[7, 9],[10, 11, 12, 13, 14, 15],[([9, 11, 13, 15], '#d9534f'), ([7, 15], '#1d6fb8')],names='ABCD',cs=0.7,title='T3')
kmap(ax,5.0,4.3,4,[3, 7],[10, 11, 12, 13, 14, 15],[([3, 7, 11, 15], '#d9534f')],names='ABCD',cs=0.7,title='T2')
kmap(ax,0.9,0.4,4,[1, 3, 5, 7],[10, 11, 12, 13, 14, 15],[([1, 3, 5, 7], '#d9534f')],names='ABCD',cs=0.7,title='T1')
kmap(ax,5.0,0.4,4,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],[10, 11, 12, 13, 14, 15],[([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], '#d9534f')],names='ABCD',cs=0.7,title='T0')
```

The loops give

$$\begin{gathered} T_{3} = Q_3Q_0 + Q_2Q_1Q_0 \\ T_{2} = Q_1Q_0 \\ T_{1} = \overline{Q_3}Q_0 \\ T_{0} = 1 \end{gathered}$$
*Step 5 - logic diagram.*

```figure caption="Logic diagram of the synchronous mod-10 up counter with T flip-flops."
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
fig,ax=ckt_canvas(6.9,4.6,xlim=(-0.4,31.4),ylim=(-9.5,3.0))

seqcirc(ax,'T',['Q3', 'Q2', 'Q1', 'Q0'],[{'T': [[(0, 1), (3, 1)], [(1, 1), (2, 1), (3, 1)]]}, {'T': [[(2, 1), (3, 1)]]}, {'T': [[(0, 0), (3, 1)]]}, {'T': '1'}],zterms=None,extra=[])
```

```figure caption="Timing diagram of the synchronous mod-10 up counter: all outputs change together just after the rising clock edge; Q3 is high for counts 8 and 9 and the counter returns to 0000 on the tenth pulse (f/10 at Q3)."
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
fig,ax=ckt_canvas(5.9,2.1,xlim=(-1.9,12.7),ylim=(-0.3,5.0))

clock(ax,0,4.1,12)
guides(ax,[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0],4.8,-0.1)
wave(ax,2.9499999999999997,[(0.0, 0), (7.05, 1), (9.05, 0)],12,'Q3')
wave(ax,2.0,[(0.0, 0), (3.05, 1), (7.05, 0)],12,'Q2')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (3.05, 0), (5.05, 1), (7.05, 0), (11.05, 1)],12,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (5.05, 0), (6.05, 1), (7.05, 0), (8.05, 1), (9.05, 0), (10.05, 1), (11.05, 0)],12,'Q0')
```

All four flip-flops are clocked by the same pulse, so the outputs change together (no ripple delay) and the maximum clock frequency is limited only by one flip-flop delay plus the AND-gate delay.


@s 11
**Design of the sequence detector for 011 (Mealy machine, overlapping sequences allowed, T flip-flops).** One input $X$ (serial data), one output $Z$; $Z=1$ for the clock period in which the last bit of **011** arrives.

*Step 1 - state diagram.* States remember how much of the pattern has been matched:

- $S_0$: no part of the pattern seen yet (reset state)
- $S_1$: the last 1 input bit 0 seen
- $S_2$: the last 2 input bits 01 seen

Edge labels are $X/Z$. After a complete match the machine falls back to the longest prefix of the pattern that is also a suffix of what was received (overlap).

```figure caption="State diagram (Mealy) of the 011 detector; labels are X/Z."
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

statediag(ax,['S0', 'S1', 'S2'],[(0, 1, '0/0'), (0, 0, '1/0'), (1, 1, '0/0'), (1, 2, '1/0'), (2, 1, '0/0'), (2, 0, '1/1')])
```

*Step 2 - state table.*

| Present state | X = 0: next / Z | X = 1: next / Z |
|---|---|---|
| S0 | S1 / 0 | S0 / 0 |
| S1 | S1 / 0 | S2 / 0 |
| S2 | S1 / 0 | S0 / 1 |

*Step 3 - state assignment.* Three states need $n = 2$ flip-flops: $S_0=00$, $S_1=01$, $S_2=10$ ($Q_1Q_0$). The code 11 is unused (don't care).

*Step 4 - excitation table of the T flip-flop.*

| Q | Q⁺ | T |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

*Step 5 - state/excitation table* with $Q_1Q_0$ the present state and $X$ the input:

| Q1 | Q0 | X | Q1⁺ | Q0⁺ | Z | T1 | T0 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 |

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
fig,ax=ckt_canvas(6.6,1.43,xlim=(0,11.5),ylim=(-0.2,2.5))

kmap(ax,0.9,0.4,3,[3, 4, 5],[6, 7],[([4, 5, 6, 7], '#d9534f'), ([3, 7], '#1d6fb8')],names='ABC',cs=0.6,title='T1')
kmap(ax,4.6000000000000005,0.4,3,[0, 3, 4],[6, 7],[([3, 7], '#d9534f'), ([0, 4], '#1d6fb8')],names='ABC',cs=0.6,title='T0')
kmap(ax,8.3,0.4,3,[5],[6, 7],[([5, 7], '#d9534f')],names='ABC',cs=0.6,title='Z')
```

$$\begin{gathered} T_{1} = Q_1 + Q_0X \\ T_{0} = Q_0X + \overline{Q_0}\overline{X} \\ Z = Q_1X \end{gathered}$$
*Step 7 - logic diagram.*

```figure caption="Logic diagram of the 011 sequence detector (T flip-flops)."
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

seqcirc(ax,'T',['Q1', 'Q0'],[{'T': [[(0, 1)], [(1, 1), (2, 1)]]}, {'T': [[(1, 1), (2, 1)], [(1, 0), (2, 0)]]}],zterms=[[(0, 1), (2, 1)]],extra=['X'])
```

*Check with a test stream* $X = 0110110011$ (applied left to right): the states visited are S0, S1, S2, S0, S1, S2, S0, S1, S1, S2 and the output is $Z = 0010010001$, with a 1 exactly when the last three bits are 011 (including overlaps).

```figure caption="Timing diagram of the 011 detector for X = 0110110011: Z goes high in the period in which the last bit of 011 is applied (Mealy output, depends on X and the present state)."
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
wave(ax,2.95,[(0.0, 0), (0.55, 1), (2.55, 0), (3.55, 1), (5.55, 0), (7.55, 1)],10,'X')
wave(ax,2.0,[(0.0, 0), (1.55, 1), (2.55, 0), (4.55, 1), (5.55, 0), (8.55, 1)],10,'Z',color='#d9534f')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (2.05, 0), (4.05, 1), (5.05, 0), (8.05, 1), (9.05, 0)],10,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (3.05, 1), (4.05, 0), (6.05, 1), (8.05, 0)],10,'Q0')
```


@s 12
A **logic family** is a group of digital ICs that use the same circuit technology (and hence the same voltage levels, speed and power) so that they can be connected to each other directly. The main families are **RTL, DTL, TTL (bipolar transistor-transistor logic), ECL (emitter-coupled logic)** and **MOS/CMOS**. Their performance is compared by the following characteristics:

1. **Propagation delay** $t_{pd}$ - the time for a change at the input to appear at the output (average of $t_{pHL}$ and $t_{pLH}$, measured between the 50 % points); it sets the speed.
2. **Power dissipation** $P_D$ - the supply power per gate ($V_{CC}\times I_{CC}$). For CMOS it is mostly dynamic ($P = C V^2 f$) and tiny when static.
3. **Speed-power product** - $t_{pd}\times P_D$ in picojoules, the single figure of merit of a family.
4. **Fan-out** - the number of similar gate inputs one output can drive without leaving the valid logic levels.
5. **Fan-in** - the number of inputs a gate has.
6. **Noise margin** - the largest noise voltage that does not change the logic level: $NM_H = V_{OH(min)} - V_{IH(min)}$, $NM_L = V_{IL(max)} - V_{OL(max)}$.
7. **Logic levels** $V_{OH}, V_{OL}, V_{IH}, V_{IL}$, and the supply voltage range.
8. **Current-sourcing / sinking capacity** $I_{OH}, I_{OL}, I_{IH}, I_{IL}$, and **cost/packing density** (CMOS has the highest integration density).

| Parameter | Standard TTL (74) | CMOS (4000B / 74HC) | ECL (10K) |
|---|---|---|---|
| Supply | 5 V ± 5 % | 3 to 15 V (4000B), 2 to 6 V (74HC) | -5.2 V |
| Propagation delay (gate) | 10 ns | 50 ns (4000B), 8 ns (74HC) | 2 ns |
| Power per gate | 10 mW | ~ 0.01 mW static, rises with f | 25 mW |
| Speed-power product | 100 pJ | ~ 1 pJ at low f | 50 pJ |
| Fan-out | 10 | > 50 | 25 |
| Noise margin | 0.4 V | ~ 45 % of VDD | 0.2 V |
| $V_{OH}$ / $V_{OL}$ | 3.4 V / 0.2 V | ≈ VDD / ≈ 0 V | -0.9 V / -1.75 V |
| Notes | Very common, totem-pole output | Lowest power, high density, slow in older series | Fastest, non-saturating, high power |



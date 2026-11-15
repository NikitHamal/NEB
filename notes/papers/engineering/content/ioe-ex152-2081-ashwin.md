---
file: NEBians-IOE-Past-Paper-Digital-Logic-EX152-2081-Ashwin.pdf
subject: Digital Logic
level: BE · Year I / Part II
code: EX 152
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Mention merits and demerits of digital signal over analog signal. [[2]]

@q 2
Perform the following as indicated: [[2×1.5]]

a) $(6E.2C)_{16} = (?)_8$

b) $(10110110)_{Gray} = (?)_2$

@q 3
Design the simplest logic circuit for 'f' segment for the BCD-to-seven segment display decoder. [[4]]

@q 4
Implement $Y(A,B,C) = \sum m(0,2,3,5,7)$ using only a single 1:4 MUX. Design a circuit which can realize both the half-adder and the half-subtractor in a single circuit. [[3+7]]

@q 5
Design a mod-6 synchronous down counter using JK flip-flops. [[7]]

@q 6
Explain the operation of 4-bit serial-in parallel-out (SIPO) shift register with necessary circuit and timing diagram for input data of 1011. [[3+3]]

@q 7
Describe briefly the operation of 3 bit up/down asynchronous counter having negative edge triggering clock system with neat circuit diagram and timing diagram. [[4+3]]

@q 8
Design a sequential machine that consists of one input, X and one output, Z. The machine is required to give output high (Y=1), whenever it detects the serial sequence of 101 from its input data stream X. Implement only SR flip-flops for the designed circuit realization. [[10]]

@q 9
Draw the circuit diagram of two-input TTL NOR gate and explain its logic operation briefly and list the characteristics of CMOS logic family. [[5+2]]

@q 10
With the help of functional diagram explain the operation of frequency measurement. [[4]]

<!-- SOLUTIONS -->

@s 1
**Merits of digital signals over analog signals**

- Better noise immunity: only two levels, so small noise never changes a bit; regenerative repeaters restore the signal exactly.
- Easy storage in memory, easy processing/transmission by computers.
- Error detection and correction by coding (parity, CRC, Hamming).
- Easy encryption and compression, so secure and efficient communication is possible.
- Circuits are IC-friendly, cheap, small and low power; precision is fixed by the number of bits.
- Many signals (voice, data, video) can be time-multiplexed on a single channel.

**Demerits**

- Needs a larger bandwidth than analog for the same information (e.g. a voice channel needs 64 kb/s instead of 4 kHz).
- Needs A/D and D/A converters for real-world (analog) signals, adding cost and quantisation error.
- Needs accurate synchronisation between transmitter and receiver.
- Sampling below the Nyquist rate produces aliasing; quantisation always leaves some error.
- Digital circuits are slower to react than a simple analog circuit for tiny sub-problems and dissipate power when switching at high speed.


@s 2
**(a) $(6E.2C)_{16} = (?)_8$.** Convert each hex digit to 4 bits, regroup the bits in threes **from the radix point outwards**:

$$6E.2C = 0110\ 1110.\ 0010\ 1100 = 001\ 101\ 110.\ 001\ 011\ 000$$

Integer part: $001\,101\,110 = 1,5,6$; fractional part: $001\,011\,000 = 1,3,0$ (the last 0 is only padding). So

$$\boxed{(6E.2C)_{16} = (156.13)_8}$$

Check in decimal: $6E_{16} = 110$, $156_8 = 64+40+6 = 110$ ✓; $0.2C_{16} = 2/16 + 12/256 = 0.171875$ and $0.13_8 = 1/8 + 3/64 = 0.171875$ ✓.

**(b) $(10110110)_{Gray} = (?)_2$.** Rule: the MSB of the binary code equals the MSB of the Gray code; every other binary bit is $b_i = b_{i-1} \oplus g_i$.

- $b_1 = g_1 = 1$
- $b_2 = b_1 \oplus g_2 = 1 \oplus 0 = 1$
- $b_3 = b_2 \oplus g_3 = 1 \oplus 1 = 0$
- $b_4 = b_3 \oplus g_4 = 0 \oplus 1 = 1$
- $b_5 = b_4 \oplus g_5 = 1 \oplus 0 = 1$
- $b_6 = b_5 \oplus g_6 = 1 \oplus 1 = 0$
- $b_7 = b_6 \oplus g_7 = 0 \oplus 1 = 1$
- $b_8 = b_7 \oplus g_8 = 1 \oplus 0 = 1$

$$(10110110)_{Gray} = (11011011)_2$$


@s 3
**BCD-to-seven-segment decoder, segment f.** The seven segments are labelled a (top), b, c, d (bottom), e, f (upper left), g (middle). The BCD inputs are $A$ (MSB) $B\,C\,D$ (LSB); segment f must be lit for the digits whose shape has the upper-left vertical bar: **0, 4, 5, 6, 8, 9** (digit 7 is drawn without it; the codes 10 to 15 never occur, so they are don't cares).

| Digit | A | B | C | D | f |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 |
| 2 | 0 | 0 | 1 | 0 | 0 |
| 3 | 0 | 0 | 1 | 1 | 0 |
| 4 | 0 | 1 | 0 | 0 | 1 |
| 5 | 0 | 1 | 0 | 1 | 1 |
| 6 | 0 | 1 | 1 | 0 | 1 |
| 7 | 0 | 1 | 1 | 1 | 0 |
| 8 | 1 | 0 | 0 | 0 | 1 |
| 9 | 1 | 0 | 0 | 1 | 1 |
| 10 - 15 | X | X | X | X | X |

**Step 1 - K-map.** Enter 1 in each minterm cell and X (don't care) in each don't-care cell, Gray-code ordered rows and columns so neighbouring cells differ in one variable.

```figure caption="4-variable K-map of f with the prime-implicant loops (cell numbers are minterm numbers)."
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

kmap(ax,0.9,0.4,4,[0, 4, 5, 6, 8, 9],[10, 11, 12, 13, 14, 15],[([8, 9, 10, 11, 12, 13, 14, 15], '#d9534f'), ([4, 5, 12, 13], '#1d6fb8'), ([4, 6, 12, 14], '#2e8b57'), ([0, 4, 8, 12], '#b8860b')],names='ABCD',cs=0.72,title='f')
```

**Step 2 - groups (largest possible, power of two).**

- Group 1 (loop colour red), cells 8, 9, 10, 11, 12, 13, 14, 15: variables that do not change survive, giving $A$.
- Group 2 (loop colour blue), cells 4, 5, 12, 13: variables that do not change survive, giving $B\overline{C}$.
- Group 3 (loop colour green), cells 4, 6, 12, 14: variables that do not change survive, giving $B\overline{D}$.
- Group 4 (loop colour gold), cells 0, 4, 8, 12: variables that do not change survive, giving $\overline{C}\overline{D}$.

**Step 3 - minimised expression.**

$$\boxed{f(A,B,C,D) = A + B\overline{C} + B\overline{D} + \overline{C}\overline{D}}$$

**Step 4 - realisation with logic gates (AND-OR, two-level).** The complemented inputs come from NOT gates.

```figure caption="AND-OR realisation of f = A + BC' + BD' + C'D'"
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
fig,ax=ckt_canvas(5.9,4.59,xlim=(-0.5,8.8),ylim=(-5.35,1.8))

sopc(ax,[[(0, 1)], [(1, 1), (2, 0)], [(1, 1), (3, 0)], [(2, 0), (3, 0)]],['A', 'B', 'C', 'D'],out='f')
```

*Equivalent NAND-only form.* Replacing every AND and the OR by NAND gates (double inversion, De Morgan) gives the same function with 5 NAND gates (plus the input inverters).


@s 4
**(a) Implementation of $Y(A,B,C) = \sum m(0,2,3,5,7)$ with one 4:1 MUX.** Use $A$ and $B$ as select lines ($S_1=A$, $S_0=B$) and $C$ as data. For each $AB$ the pair of minterms $(C=0, C=1)$ gives the data input (implementation table):

| Select AB | Minterms (C = 0, C = 1) | Y for C = 0 / 1 | Data input |
|---|---|---|---|
| 00 | m0, m1 | 1 / 0 | $\overline{C}$ (I0) |
| 01 | m2, m3 | 1 / 1 | 1 (I1) |
| 10 | m4, m5 | 0 / 1 | C (I2) |
| 11 | m6, m7 | 0 / 1 | C (I3) |

$$Y = \overline{A}\,\overline{B}\,\overline{C} + \overline{A}B + AC$$

```figure caption="Y(A,B,C) = Σm(0,2,3,5,7) with a single 4:1 multiplexer (data inputs C', 1, C, C)."
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

fig,ax=ckt_canvas(5.9,2.8,xlim=(-3.0,9.0),ylim=(-1.8,3.6))
m=mux(ax,3.0,1.0,4,['$\\overline{C}$', '1', 'C', 'C'],["A","B"],out="Y",name="4:1 MUX")
```

**(b) One circuit for both the half adder and the half subtractor.**

Half adder: $S = A\oplus B$, $C = AB$. Half subtractor: $D = A\oplus B$, $B_o = \overline{A}B$. The sum and the difference are the same, only the second output differs; with a control input $M$ (0 = add, 1 = subtract):

$$\begin{gathered}\text{Sum/Difference} = A\oplus B \\ \text{Carry/Borrow} = (A\oplus M)\cdot B\end{gathered}$$

| M | A | B | Sum / Diff | Carry / Borrow = (A⊕M)B |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 0 | 0 |

For $M=0$: $(A\oplus0)B = AB$ (carry); for $M=1$: $(A\oplus1)B = \overline{A}B$ (borrow). Two XOR gates and one AND gate are enough:

```figure caption="Combined half adder / half subtractor with control input M (two XOR gates and an AND gate)."
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

fig,ax=ckt_canvas(5.9,3.0,xlim=(-1.8,13.0),ylim=(-0.6,6.2))
# S/D = A xor B ; C/Bo = (A xor M).B
ins,o=gate(ax,"XOR",3.0,5.0,w=1.2,h=0.9,lead=0.4)
T(ax,ins[0][0]-0.15,ins[0][1],"A",ha="right"); T(ax,ins[1][0]-0.15,ins[1][1],"B",ha="right")
T(ax,o[0]+0.15,o[1],"Sum / Difference",ha="left",size=8.4)
L(ax,[(ins[0][0]-0.15,ins[0][1]),(ins[0][0]-0.15,ins[0][1])])
ins2,o2=gate(ax,"XOR",3.0,2.8,w=1.2,h=0.9,lead=0.4)
T(ax,ins2[0][0]-0.15,ins2[0][1],"A",ha="right"); T(ax,ins2[1][0]-0.15,ins2[1][1],"M",ha="right")
ins3,o3=gn(ax,"AND",6.8,2.1,n=2,w=0.9,lead=0.4)
L(ax,[o2,(6.0,o2[1]),(6.0,ins3[0][1]),ins3[0]])
T(ax,ins3[1][0]-0.1,ins3[1][1],"B",ha="right")
T(ax,o3[0]+0.15,o3[1],"Carry / Borrow",ha="left",size=8.4)
T(ax,1.0,0.2,"M = 0: half adder     M = 1: half subtractor",size=8,color=MUTED,ha="left")
```


@s 5
**Design of the synchronous mod-6 down counter with JK flip-flops.**

*Step 1 - number of flip-flops.* $2^{2} < N \le 2^{3}$ needs $n=3$ flip-flops (JK flip-flops), all clocked together (synchronous). The states are $Q2Q1Q0$.

*Step 2 - excitation table of the JK flip-flop.*

| Q | Q⁺ | J | K |
|---|---|---|---|
| 0 | 0 | 0 | X |
| 0 | 1 | 1 | X |
| 1 | 0 | X | 1 |
| 1 | 1 | X | 0 |

*Step 3 - state / excitation table* (for each present state the next state, and the flip-flop inputs needed from the excitation table; X = don't care):

| Q2 | Q1 | Q0 | Q2⁺ | Q1⁺ | Q0⁺ | J2 | K2 | J1 | K1 | J0 | K0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 | 1 | 1 | X | 0 | X | 1 | X |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | X | 0 | X | X | 1 |
| 0 | 1 | 0 | 0 | 0 | 1 | 0 | X | X | 1 | 1 | X |
| 0 | 1 | 1 | 0 | 1 | 0 | 0 | X | X | 0 | X | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 | X | 1 | 1 | X | 1 | X |
| 1 | 0 | 1 | 1 | 0 | 0 | X | 0 | 0 | X | X | 1 |

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

kmap(ax,0.9,2.6,3,[0],[4, 5, 6, 7],[([0, 4], '#d9534f')],names='ABCD',cs=0.55,title='J2')
kmap(ax,4.4,2.6,3,[4],[0, 1, 2, 3, 6, 7],[([0, 2, 4, 6], '#d9534f')],names='ABCD',cs=0.55,title='K2')
kmap(ax,7.9,2.6,3,[4],[2, 3, 6, 7],[([4, 6], '#d9534f')],names='ABCD',cs=0.55,title='J1')
kmap(ax,0.9,0.4,3,[2],[0, 1, 4, 5, 6, 7],[([0, 2, 4, 6], '#d9534f')],names='ABCD',cs=0.55,title='K1')
kmap(ax,4.4,0.4,3,[0, 2, 4],[1, 3, 5, 6, 7],[([0, 1, 2, 3, 4, 5, 6, 7], '#d9534f')],names='ABCD',cs=0.55,title='J0')
kmap(ax,7.9,0.4,3,[1, 3, 5],[0, 2, 4, 6, 7],[([0, 1, 2, 3, 4, 5, 6, 7], '#d9534f')],names='ABCD',cs=0.55,title='K0')
```

The loops give

$$\begin{gathered} J_{2} = \overline{Q_1}\overline{Q_0} \\ K_{2} = \overline{Q_0} \\ J_{1} = Q_2\overline{Q_0} \\ K_{1} = \overline{Q_0} \\ J_{0} = 1 \\ K_{0} = 1 \end{gathered}$$
*Step 5 - logic diagram.*

```figure caption="Logic diagram of the synchronous mod-6 down counter with JK flip-flops."
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

seqcirc(ax,'JK',['Q2', 'Q1', 'Q0'],[{'J': [[(1, 0), (2, 0)]], 'K': [[(2, 0)]]}, {'J': [[(0, 1), (2, 0)]], 'K': [[(2, 0)]]}, {'J': '1', 'K': '1'}],zterms=None,extra=[])
```

```figure caption="Timing diagram of the mod-6 down counter: 101, 100, 011, 010, 001, 000, 101, ... Each output changes just after the rising clock edge."
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
wave(ax,2.0,[(0.0, 1), (1.05, 0), (5.05, 1), (7.05, 0)],8,'Q2')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (3.05, 0), (7.05, 1)],8,'Q1')
wave(ax,0.1,[(0.0, 1), (0.05, 0), (1.05, 1), (2.05, 0), (3.05, 1), (4.05, 0), (5.05, 1), (6.05, 0), (7.05, 1)],8,'Q0')
```


@s 6
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

**Working for the serial input 1011** (the first bit applied is 1, the last 1; the register is first cleared):

| Clock pulse | Serial in | QA | QB | QC | QD |
|---|---|---|---|---|---|
| initial | - | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 0 |
| 3 | 1 | 1 | 0 | 1 | 0 |
| 4 | 1 | 1 | 1 | 0 | 1 |

After the fourth pulse $Q_AQ_BQ_CQ_D = 1101$, i.e. $Q_DQ_CQ_BQ_A = 1011 = 1011$, the word applied serially, now available in parallel.

```figure caption="Timing diagram of the 4-bit SIPO register for the serial input 1011 (QA is the first stage, QD the last; the bits appear in QD..QA after four clock pulses)."
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
wave(ax,2.9499999999999997,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1)],4,'QA')
wave(ax,2.0,[(0.0, 0), (1.05, 1), (2.05, 0), (3.05, 1)],4,'QB')
wave(ax,1.05,[(0.0, 0), (2.05, 1), (3.05, 0)],4,'QC')
wave(ax,0.1,[(0.0, 0), (3.05, 1)],4,'QD')
wave(ax,5.3,[(0.0, 1), (1.0, 0), (2.0, 1)],4,'Din')
```


@s 7
**3-bit asynchronous up/down counter with negative-edge triggering.** Three T flip-flops (JK with $J=K=1$) that toggle on the **falling** edge of their clock input are cascaded. The first flip-flop gets the external clock. For the others the clock source depends on the mode input $M$:

- **Up counting ($M=0$):** the clock of $FF_{i+1}$ is $Q_i$. A falling edge of $Q_i$ means a 1→0 change, i.e. a carry, so the next bit toggles - exactly the ripple up counter.
- **Down counting ($M=1$):** the clock of $FF_{i+1}$ is $\overline{Q_i}$. $\overline{Q_i}$ falls when $Q_i$ rises (0→1), i.e. when the lower bit borrows from the higher one.

The selection is made by two AND gates and an OR gate per stage: $CLK_{i+1} = \overline{M}\,Q_i + M\,\overline{Q_i}$.

```figure caption="3-bit asynchronous up/down counter with falling-edge triggered T flip-flops; M selects Q (up) or Q' (down) as the clock of the next stage."
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

fig,ax=ckt_canvas(5.9,3.0,xlim=(-1.6,15.4),ylim=(-1.6,4.4))
Ps=[ffb(ax,0.6+4.6*i,0.6,"FF%d"%i,"T",w=1.3,h=1.6,qn=True,neg=True) for i in range(3)]
for i,P in enumerate(Ps):
    T(ax,P["T"][0]-0.1,P["T"][1],"1",ha="right",size=8.4)
    L(ax,[P["Q"],(P["Q"][0]+0.4,P["Q"][1])]) if i==2 else None
    T(ax,P["Q"][0]+0.45,P["Q"][1],"Q%d"%i,ha="left",size=8.4) if i==2 else None
# clock of stage i+1 selected by mode M: M=0 up (clock from Q), M=1 down (clock from Q')
for i in range(2):
    Pa,Pb=Ps[i],Ps[i+1]
    ia,oa=gn(ax,"AND",Pa["Q"][0]+1.0,3.5,n=2,w=0.8,lead=0.2)
    ib,ob=gn(ax,"AND",Pa["Q"][0]+1.0,2.3,n=2,w=0.8,lead=0.2)
    io,oo=gn(ax,"OR",Pa["Q"][0]+2.7,2.9,n=2,w=0.8,lead=0.2) if False else (None,None)
    L(ax,[Pa["Q"],(Pa["Q"][0]+0.3,Pa["Q"][1]),(Pa["Q"][0]+0.3,ia[0][1]),ia[0]]); dot(ax,Pa["Q"][0]+0.3,Pa["Q"][1])
    L(ax,[Pa["QN"],(Pa["QN"][0]+0.55,Pa["QN"][1]),(Pa["QN"][0]+0.55,ib[0][1]),ib[0]]); dot(ax,Pa["QN"][0]+0.55,Pa["QN"][1])
    T(ax,ia[1][0]-0.05,ia[1][1],"$\\overline{M}$",ha="right",size=7.6); T(ax,ib[1][0]-0.05,ib[1][1],"M",ha="right",size=7.6)
    ig,og=gn(ax,"OR",Pa["Q"][0]+2.55,2.9,n=2,w=0.8,lead=0.2)
    L(ax,[oa,(og[0]-1.35,oa[1]),(og[0]-1.35,ig[0][1]),ig[0]]) if False else L(ax,[oa,(ig[0][0]-0.2,oa[1]),(ig[0][0]-0.2,ig[0][1]),ig[0]])
    L(ax,[ob,(ig[1][0]-0.2,ob[1]),(ig[1][0]-0.2,ig[1][1]),ig[1]])
    L(ax,[og,(og[0]+0.2,og[1]),(og[0]+0.2,0.0),(Pb["CK"][0]-0.5,0.0),(Pb["CK"][0]-0.5,Pb["CK"][1]),Pb["CK"]])
L(ax,[(Ps[0]["CK"][0]-0.7,Ps[0]["CK"][1]),Ps[0]["CK"]]); T(ax,Ps[0]["CK"][0]-0.75,Ps[0]["CK"][1],"CLK",ha="right")
T(ax,-1.4,4.2,"M = 0 : up counting     M = 1 : down counting",size=8,ha="left",color=MUTED)
```

**Count sequences.**

| Pulse | Up: Q2 Q1 Q0 | Down: Q2 Q1 Q0 |
|---|---|---|
| 0 | 000 | 111 |
| 1 | 001 | 110 |
| 2 | 010 | 101 |
| 3 | 011 | 100 |
| 4 | 100 | 011 |
| 5 | 101 | 010 |
| 6 | 110 | 001 |
| 7 | 111 | 000 |
| 8 | 000 | 111 |

In the up mode the counter counts $000, 001, \dots, 111, 000$; in the down mode it counts $111, 110, \dots, 000, 111$.

```figure caption="Up mode (M = 0): Q0 toggles on every falling clock edge and each higher bit toggles on the falling edge of the previous Q."
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
guides(ax,[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5],3.8499999999999996,-0.1)
wave(ax,2.0,[(0.0, 0), (3.71, 1), (7.71, 0)],8,'Q2')
wave(ax,1.05,[(0.0, 0), (1.63, 1), (3.63, 0), (5.63, 1), (7.63, 0)],8,'Q1')
wave(ax,0.1,[(0.0, 0), (0.55, 1), (1.55, 0), (2.55, 1), (3.55, 0), (4.55, 1), (5.55, 0), (6.55, 1), (7.55, 0)],8,'Q0')
```
```figure caption="Down mode (M = 1): the clock of the next stage is taken from Q' of the previous stage, so the count falls 7, 6, ..., 0."
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
guides(ax,[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5],3.8499999999999996,-0.1)
wave(ax,2.0,[(0.0, 1), (3.71, 0), (7.71, 1)],8,'Q2')
wave(ax,1.05,[(0.0, 1), (1.63, 0), (3.63, 1), (5.63, 0), (7.63, 1)],8,'Q1')
wave(ax,0.1,[(0.0, 1), (0.55, 0), (1.55, 1), (2.55, 0), (3.55, 1), (4.55, 0), (5.55, 1), (6.55, 0), (7.55, 1)],8,'Q0')
```

Each stage adds a propagation delay, so the outputs ripple; the maximum clock frequency is $1/(3\,t_{pd}+t_{gate\ delays})$.


@s 8
**Design of the sequence detector for 101 (Mealy machine, overlapping sequences allowed, SR flip-flops).** One input $X$ (serial data), one output $Z$; $Z=1$ for the clock period in which the last bit of **101** arrives.

*Step 1 - state diagram.* States remember how much of the pattern has been matched:

- $S_0$: no part of the pattern seen yet (reset state)
- $S_1$: the last 1 input bit 1 seen
- $S_2$: the last 2 input bits 10 seen

Edge labels are $X/Z$. After a complete match the machine falls back to the longest prefix of the pattern that is also a suffix of what was received (overlap).

```figure caption="State diagram (Mealy) of the 101 detector; labels are X/Z."
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

statediag(ax,['S0', 'S1', 'S2'],[(0, 0, '0/0'), (0, 1, '1/0'), (1, 2, '0/0'), (1, 1, '1/0'), (2, 0, '0/0'), (2, 1, '1/1')])
```

*Step 2 - state table.*

| Present state | X = 0: next / Z | X = 1: next / Z |
|---|---|---|
| S0 | S0 / 0 | S1 / 0 |
| S1 | S2 / 0 | S1 / 0 |
| S2 | S0 / 0 | S1 / 1 |

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
| 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 | 1 | 0 | 0 | X | X | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | X |
| 1 | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 |

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

kmap(ax,0.9,2.6999999999999997,3,[2],[6, 7],[([2, 6], '#d9534f')],names='ABC',cs=0.6,title='S1')
kmap(ax,4.6000000000000005,2.6999999999999997,3,[4, 5],[0, 1, 3, 6, 7],[([0, 1, 4, 5], '#d9534f')],names='ABC',cs=0.6,title='R1')
kmap(ax,8.3,2.6999999999999997,3,[1, 5],[3, 6, 7],[([1, 3, 5, 7], '#d9534f')],names='ABC',cs=0.6,title='S0')
kmap(ax,0.9,0.4,3,[2],[0, 4, 6, 7],[([0, 2, 4, 6], '#d9534f')],names='ABC',cs=0.6,title='R0')
kmap(ax,4.6000000000000005,0.4,3,[5],[6, 7],[([5, 7], '#d9534f')],names='ABC',cs=0.6,title='Z')
```

$$\begin{gathered} S_{1} = Q_0\overline{X} \\ R_{1} = \overline{Q_0} \\ S_{0} = X \\ R_{0} = \overline{X} \\ Z = Q_1X \end{gathered}$$
*Step 7 - logic diagram.*

```figure caption="Logic diagram of the 101 sequence detector (SR flip-flops)."
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

seqcirc(ax,'SR',['Q1', 'Q0'],[{'S': [[(1, 1), (2, 0)]], 'R': [[(1, 0)]]}, {'S': [[(2, 1)]], 'R': [[(2, 0)]]}],zterms=[[(0, 1), (2, 1)]],extra=['X'])
```

*Check with a test stream* $X = 1010110101$ (applied left to right): the states visited are S0, S1, S2, S1, S2, S1, S1, S2, S1, S2 and the output is $Z = 0010100101$, with a 1 exactly when the last three bits are 101 (including overlaps).

```figure caption="Timing diagram of the 101 detector for X = 1010110101: Z goes high in the period in which the last bit of 101 is applied (Mealy output, depends on X and the present state)."
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
wave(ax,2.95,[(0.0, 1), (0.55, 0), (1.55, 1), (2.55, 0), (3.55, 1), (5.55, 0), (6.55, 1), (7.55, 0), (8.55, 1)],10,'X')
wave(ax,2.0,[(0.0, 0), (1.55, 1), (2.55, 0), (3.55, 1), (4.55, 0), (6.55, 1), (7.55, 0), (8.55, 1)],10,'Z',color='#d9534f')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (2.05, 0), (3.05, 1), (4.05, 0), (6.05, 1), (7.05, 0), (8.05, 1), (9.05, 0)],10,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (6.05, 0), (7.05, 1), (8.05, 0), (9.05, 1)],10,'Q0')
```


@s 9
**Two-input TTL NOR gate.** The circuit has three parts: (i) two **input transistors** $Q_{1A}$, $Q_{1B}$ with their own base resistors (4 kΩ), one for each input, (ii) two **phase-splitter transistors** $Q_{2A}$, $Q_{2B}$ connected **in parallel** (collectors tied, emitters tied) and (iii) the **totem-pole output stage** $Q_3$ (pull-up) and $Q_4$ (pull-down) with a diode and 130 Ω resistor.

```figure caption="Simplified circuit of a 2-input TTL NOR gate (each input has its own input transistor and phase splitter; the splitters are in parallel, then the totem-pole output)."
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

fig,ax=ckt_canvas(5.9,3.9,xlim=(-2.0,17.0),ylim=(-1.8,8.6))
T(ax,7.5,8.2,"+V$_{CC}$ (5 V)",size=8.6)
L(ax,[(0,7.8),(15,7.8)],lw=1.6)
# input stages
for k,(nm,x) in enumerate((("A",1.0),("B",5.0))):
    res(ax,(x,7.8),(x,5.8),"4 kΩ",side=1,body=0.9,off=1.0)
    box(ax,x-0.7,3.8,1.4,1.4,"Q1%s\n(input)"%nm,size=7.6)
    L(ax,[(x,5.8),(x,5.2)])
    L(ax,[(x-0.7,4.5),(x-1.3,4.5)]); T(ax,x-1.4,4.5,nm,ha="right",size=9)
    # collector to phase splitter
    L(ax,[(x,3.8),(x,3.2)]); box(ax,x-0.7,1.8,1.4,1.4,"Q2%s\n(splitter)"%nm,size=7.6)
    L(ax,[(x,1.8),(x,1.2)])
# common emitter node of splitters
L(ax,[(1.0,1.2),(5.0,1.2)]); dot(ax,3.0,1.2); res(ax,(3.0,1.2),(3.0,-0.6),"1 kΩ",side=1,body=0.8,off=1.0); gnd(ax,(3.0,-0.6))
# common collectors (tied via 1.6 k to Vcc) go to the totem-pole
L(ax,[(0.3,3.5),(0.3,6.6),(8.0,6.6)]) if False else None
res(ax,(8.0,7.8),(8.0,6.4),"1.6 kΩ",side=1,body=0.8,off=1.1)
L(ax,[(8.0,6.4),(8.0,5.6),(5.8,5.6),(5.8,2.5),(5.7,2.5)]) if False else None
L(ax,[(8.0,6.4),(8.0,2.5)]); L(ax,[(1.7,2.5),(8.0,2.5)]); dot(ax,8.0,2.5)
L(ax,[(1.7,2.5),(1.7,2.5)])
L(ax,[(5.7,2.5),(5.7,2.5)])
# totem pole
box(ax,9.4,5.4,1.6,1.0,"Q3",size=8.2); box(ax,9.4,1.8,1.6,1.0,"Q4",size=8.2)
res(ax,(10.2,7.8),(10.2,6.4),"130 Ω",side=1,body=0.7,off=1.0)
L(ax,[(10.2,5.4),(10.2,4.8)]); diode(ax,(10.2,4.8),(10.2,3.6),None,side=1) if True else None
L(ax,[(10.2,3.6),(10.2,2.8)]); dot(ax,10.2,4.2)
L(ax,[(8.0,5.9),(9.4,5.9)]) ; dot(ax,8.0,5.9)
L(ax,[(8.0,2.3),(9.4,2.3)]); 
L(ax,[(10.2,1.8),(10.2,-0.6)]); gnd(ax,(10.2,-0.6))
L(ax,[(11.0,3.6),(13.0,3.6)]) if False else None
L(ax,[(10.2,4.2),(13.0,4.2)]); T(ax,13.1,4.2,"Y = $\\overline{A+B}$",ha="left",size=8.8)
T(ax,13.2,1.0,"Q2A, Q2B in parallel:\nY = 0 if A or B is high",size=7.6,color=MUTED,ha="left")
```

**Logic operation.**

- **A = B = 0 (low):** both input transistors conduct through their emitters, which steals the base current of the splitters, so $Q_{2A}$ and $Q_{2B}$ are both OFF. The common collector node goes high: $Q_3$ conducts and $Q_4$ is off, so the output is high, $Y\approx 3.4$ V (logic 1).
- **A = 1, B = 0 (or A = 0, B = 1):** the input transistor of the high input is reverse biased and its collector current drives the base of its splitter; that splitter $Q_2$ saturates. Because the splitters are in parallel, one conducting transistor is enough to pull the collector node low and to drive $Q_4$ into saturation while $Q_3$ is off: $Y\approx0.2$ V (logic 0).
- **A = B = 1:** both splitters conduct, $Q_4$ saturates, $Y = 0$.

| A | B | Q2A | Q2B | Q3 | Q4 | Y = (A+B)' |
|---|---|---|---|---|---|---|
| 0 | 0 | off | off | on | off | 1 |
| 0 | 1 | off | on | off | on | 0 |
| 1 | 0 | on | off | off | on | 0 |
| 1 | 1 | on | on | off | on | 0 |

The output is low whenever *any* input is high, i.e. $Y = \overline{A+B}$ (NOR).

**Characteristics of the CMOS logic family.**

- **Basic structure:** complementary pair of enhancement MOSFETs (PMOS pull-up network, NMOS pull-down network) with the same inputs; only one network conducts in a steady state.
- **Supply voltage:** wide range, 3 to 15 V for the 4000B series (2 to 6 V for 74HC), so it can run from a battery.
- **Logic levels:** $V_{OH}\approx V_{DD}$ and $V_{OL}\approx 0$ V (full rail-to-rail swing); $V_{IL}\approx 0.3\,V_{DD}$, $V_{IH}\approx 0.7\,V_{DD}$.
- **Noise margin:** very high, about 45 % of $V_{DD}$ (≈ 2.25 V at 5 V, ≈ 4.5 V at 10 V).
- **Power dissipation:** extremely low static power (≈ 10 nW per gate); dynamic power $P = C_L V_{DD}^2 f$ grows with frequency.
- **Propagation delay:** about 50 ns for 4000B at 5 V (higher than TTL), 8 ns for 74HC.
- **Fan-out:** very high (> 50) because the MOS input draws almost no DC current (input resistance ≈ $10^{12}$ Ω); the limit is the capacitive load.
- **Packing density:** high, since the gates need no resistors, so CMOS is used for LSI/VLSI (microprocessors, memories).
- **Unused inputs** must never be left floating (static charge can damage the thin gate oxide and cause excess power): tie to $V_{DD}$ or ground; handle with anti-static care.
- **Speed-power product:** about 1 pJ at low frequency, the best of all families.


@s 10
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



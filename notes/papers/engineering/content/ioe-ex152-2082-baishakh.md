---
file: NEBians-IOE-Past-Paper-Digital-Logic-EX152-2082-Baishakh.pdf
subject: Digital Logic
level: BE · Year I / Part II
code: EX 152
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BCT, BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define an ASCII code. Use 2's complement method to perform the following addition $(-28 + 12)_{10}$ in 8-bit signed number representation. [[1+3]]

@q 2
Prove the following: [[2×2]]

a) $AB + \overline{A}C + BC = AB + \overline{A}C$

b) $AB + C(A\oplus B) = BC + A(B+C)$

@q 3
What is a decoder? Design an octal priority encoder with neat circuit diagram. [[2+6]]

@q 4
Realize the following Boolean function using a single 3×8 decoder. Also simplify the logic function implementing K-map method. [[3+3]]

$X(A,B,C,D) = \sum m(0,2,3,7,8,10,11,14,15)$

@q 5
Design a synchronous 2-bit up/down counter using T flip-flops. [[7]]

@q 6
Explain the operation of 4-bit parallel-in serial-out (PISO) shift register with necessary circuit and timing diagram for 1101 input data. [[3+2]]

@q 7
Sketch the circuit diagram of mod-12 asynchronous counter having positive-edge triggering clock system implementing JK flip-flops with neat timing diagram. [[3+3]]

@q 8
Design a sequential machine that consists of one input, X and one output, Z. The machine is required to give output high (Y=1), whenever it detects the serial sequence of 010 from its input data stream X. Implement only D flip-flops for the designed circuit realization. [[10]]

@q 9
Draw the circuit diagram of two-input CMOS NAND gate and explain its logic operation briefly and list the characteristics of TTL logic family. [[4+2]]

@q 10
With the help of functional diagram explain the operation of time measuring circuit. [[4]]

<!-- SOLUTIONS -->

@s 1
**ASCII** (American Standard Code for Information Interchange) is a 7-bit alphanumeric code that represents $2^7 = 128$ characters: 10 digits, 26 upper-case and 26 lower-case letters, punctuation, and 33 control characters. An 8th bit (parity or extended set) makes it a byte.

| Character | Decimal | 7-bit ASCII | Hex |
|---|---|---|---|
| 0 | 48 | 011 0000 | 30 |
| 9 | 57 | 011 1001 | 39 |
| A | 65 | 100 0001 | 41 |
| Z | 90 | 101 1010 | 5A |
| a | 97 | 110 0001 | 61 |
| Space | 32 | 010 0000 | 20 |
| CR (carriage return) | 13 | 000 1101 | 0D |

**Addition of $(-28)+12$ in 8-bit 2's complement.**

$+12 = 0000\,1100$. $28 = 0001\,1100$, so $-28$: invert $\to 1110\,0011$, add 1 $\to 1110\,0100$.

$$\begin{array}{r@{\;}l} & 1110\,0100 \quad(-28) \\ + & 0000\,1100 \quad(+12) \\ \hline & 1111\,0000 \end{array}$$

No carry out of the MSB position and the sign bit is 1, so the result is negative and is in 2's complement form. Magnitude: invert $1111\,0000 \to 0000\,1111$, add 1 $\to 0001\,0000 = 16$.

$$(-28) + 12 = -16 \quad\Rightarrow\quad \boxed{1111\,0000}_2 \ (\text{no overflow, since the operands have different signs})$$


@s 2
**(a) $AB + \overline{A}C + BC = AB + \overline{A}C$ (consensus theorem).**

Multiply the redundant term by $(A+\overline{A}) = 1$:

$$\begin{aligned} \text{LHS} &= AB + \overline{A}C + BC(A+\overline{A}) \\ &= AB + \overline{A}C + ABC + \overline{A}BC \\ &= AB(1 + C) + \overline{A}C(1 + B) \\ &= AB + \overline{A}C = \text{RHS} \end{aligned}$$

**(b) $AB + C(A\oplus B) = BC + A(B+C)$.**

Left side, using $A\oplus B = \overline{A}B + A\overline{B}$:

$$\begin{aligned} \text{LHS} &= AB + \overline{A}BC + A\overline{B}C \\ &= B(A + \overline{A}C) + A\overline{B}C \\ &= B(A + C) + A\overline{B}C \qquad (x + \overline{x}y = x + y) \\ &= AB + BC + A\overline{B}C \\ &= BC + A(B + \overline{B}C) = BC + A(B + C) = \text{RHS} \end{aligned}$$

Both sides equal $AB + BC + CA$ (the majority function, which is the carry of a full adder). **Truth-table check:**

| A | B | C | AB+A'C+BC | AB+A'C | AB+C(A⊕B) | BC+A(B+C) |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |

In every row the two columns of each pair are identical, so both identities hold.


@s 3
**Decoder.** A decoder is a combinational circuit that converts an $n$-bit binary input code into a 1-of-$2^n$ output: exactly one output line is active for each input combination (for a 3-to-8 decoder each output is a minterm of the inputs, built with AND/NAND gates, and an enable input switches the decoder on or off). Applications: address decoding, memory chip-select, demultiplexing, BCD-to-seven-segment driving.

**Octal priority encoder.** An ordinary encoder gives a wrong code if two inputs are active together. A priority encoder gives the code of the **highest-numbered active input** and ignores the lower ones (X = don't care). A valid output $V$ shows that at least one input is active.

| D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 | A2 | A1 | A0 | V |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | X | X | X | X | X | X | X | 1 | 1 | 1 | 1 |
| 0 | 1 | X | X | X | X | X | X | 1 | 1 | 0 | 1 |
| 0 | 0 | 1 | X | X | X | X | X | 1 | 0 | 1 | 1 |
| 0 | 0 | 0 | 1 | X | X | X | X | 1 | 0 | 0 | 1 |
| 0 | 0 | 0 | 0 | 1 | X | X | X | 0 | 1 | 1 | 1 |
| 0 | 0 | 0 | 0 | 0 | 1 | X | X | 0 | 1 | 0 | 1 |
| 0 | 0 | 0 | 0 | 0 | 0 | 1 | X | 0 | 0 | 1 | 1 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | X | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

From this table (the minimisation was done on a 7-variable K-map/Quine-McCluskey over $D_7\dots D_1$ and verified for all 128 input combinations; $D_0$ never changes the code):

$$\begin{aligned} A_2 &= D_7 + D_6 + D_5 + D_4 \\ A_1 &= D_7 + D_6 + \overline{D_5}\overline{D_4}D_3 + \overline{D_5}\overline{D_4}D_2 \\ A_0 &= D_7 + \overline{D_6}D_5 + \overline{D_6}\overline{D_4}D_3 + \overline{D_6}\overline{D_4}\overline{D_2}D_1 \\ V &= D_7 + D_6 + D_5 + D_4 + D_3 + D_2 + D_1 + D_0 \end{aligned}$$

**Logic diagram** (the three outputs; each product term is an AND gate and each output an OR gate; the complemented inputs come from NOT gates):

```figure caption="Priority encoder output A2 (inputs D7 ... D1)."
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
fig,ax=ckt_canvas(5.9,3.47,xlim=(-0.5,11.65),ylim=(-5.35,1.8))

sopc(ax,[[(0, 1)], [(1, 1)], [(2, 1)], [(3, 1)]],['D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1'],out='A2')
```
```figure caption="Priority encoder output A1 (inputs D7 ... D1)."
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
fig,ax=ckt_canvas(5.9,4.09,xlim=(-0.5,11.65),ylim=(-6.58,1.8))

sopc(ax,[[(0, 1)], [(1, 1)], [(2, 0), (3, 0), (4, 1)], [(2, 0), (3, 0), (5, 1)]],['D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1'],out='A1')
```
```figure caption="Priority encoder output A0 (inputs D7 ... D1)."
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
fig,ax=ckt_canvas(5.9,4.73,xlim=(-0.5,11.65),ylim=(-7.84,1.8))

sopc(ax,[[(0, 1)], [(1, 0), (2, 1)], [(1, 0), (3, 0), (4, 1)], [(1, 0), (3, 0), (5, 0), (6, 1)]],['D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1'],out='A0')
```

The valid output is a single 8-input OR gate on $D_0\dots D_7$.


@s 4
**Realisation with a single 3×8 decoder.** The function has four variables but the decoder has only three inputs. Apply $A, B, C$ to the decoder (outputs $y_0\dots y_7$ are the minterms of $ABC$, $y_k = 1$ when $ABC = k$) and handle $D$ with a few gates. For each value of $ABC$ look at the pair of minterms $m_{2k}$ ($D=0$) and $m_{2k+1}$ ($D=1$):

| ABC | D = 0 (m2k) | D = 1 (m2k+1) | X contains |
|---|---|---|---|
| 000 | 1 | 0 | $\overline{D}$ |
| 001 | 1 | 1 | 1 |
| 010 | 0 | 0 | 0 |
| 011 | 0 | 1 | $D$ |
| 100 | 1 | 0 | $\overline{D}$ |
| 101 | 1 | 1 | 1 |
| 110 | 0 | 0 | 0 |
| 111 | 1 | 1 | 1 |

So (using the decoder outputs $y_k$ and $D$):

$$X = y_0\overline{D} + y_1 + y_3 D + y_4\overline{D} + y_5 + y_7$$

(checked against all 16 input combinations). Three AND gates, one NOT gate and a 6-input OR gate, together with the 3×8 decoder, give the function.

```figure caption="X(A,B,C,D) = Σm(0,2,3,7,8,10,11,14,15) with one 3×8 decoder (A,B,C), three AND gates, an inverter for D and a 6-input OR gate."
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

fig,ax=ckt_canvas(5.9,4.2,xlim=(-1.4,15.4),ylim=(-1.2,7.2))
box(ax,1.4,0.0,2.6,6.0,"3 × 8\nDECODER",size=8.4)
for k,(nm) in enumerate(["A","B","C"]):
    yy=4.6-1.5*k; L(ax,[(0.6,yy),(1.4,yy)]); T(ax,0.5,yy,nm,ha="right",size=8.6); T(ax,1.55,yy,["I2","I1","I0"][k],ha="left",size=7.4,color=MUTED)
ys=[5.5-0.75*i for i in range(8)]
for i,y in enumerate(ys):
    L(ax,[(4.0,y),(4.6,y)]); T(ax,3.9,y,"y%d"%i,ha="right",size=7.6)
# AND gates for y0.D', y3.D, y4.D'
outs={}
gy={0:5.5,3:3.55,4:2.55}
for i,lab in ((0,"D'"),(3,"D"),(4,"D'")):
    ins,o=gn(ax,"AND",6.2,gy[i],n=2,w=0.9,lead=0.3)
    L(ax,[(4.6,ys[i]),(ins[0][0],ys[i]) if abs(ins[0][1]-ys[i])<1e-6 else (4.6,ys[i]),(5.5,ys[i]),(5.5,ins[0][1]),ins[0]])
    T(ax,ins[1][0]-0.08,ins[1][1],lab,ha="right",size=8.0); outs[i]=o
# OR gate: inputs from y1,y5,y7 directly and the three ANDs
src=[("y",ys[1]),("a",outs[0]),("a",outs[3]),("a",outs[4]),("y",ys[5]),("y",ys[7])]
ins,o=gn(ax,"OR",11.0,3.0,n=6,sp=0.62,w=1.1,lead=0.4)
order=[("y",1),("a",0),("a",3),("a",4),("y",5),("y",7)]
for (kind,i),(px,py) in zip(order,ins):
    if kind=="y":
        xm=8.6+0.2*i%1.0
        L(ax,[(4.6,ys[i]),(7.3+0.18*(i%3),ys[i]),(7.3+0.18*(i%3),py),(px,py)]) if False else L(ax,[(4.6,ys[i]),(5.0+0.0,ys[i]),(5.0,ys[i]),(5.0,ys[i])]) if False else None
        xa=9.2+0.15*(i%3)
        L(ax,[(4.6,ys[i]),(4.6,ys[i])]) if False else None
        L(ax,[(4.6,ys[i]),(xa,ys[i]) if False else (4.6,ys[i])]) if False else None
    else:
        pass
for (kind,i),(px,py) in zip(order,ins):
    if kind=="a":
        ox,oy=outs[i]; xa=ox+0.4
        L(ax,[(ox,oy),(xa,oy),(xa,py),(px,py)])
    else:
        # route above/below the gates
        yy=ys[i]; xa=9.3+0.25*[1,5,7].index(i)
        ytr=yy
        L(ax,[(4.6,yy),(4.6+0.0,yy)])
        L(ax,[(4.6,yy),(5.0,yy),(5.0,yy+(0.0)),(xa,yy)]) if False else None
        L(ax,[(4.6,yy),(xa,yy),(xa,py),(px,py)])
L(ax,[o,(o[0]+0.5,o[1])]); T(ax,o[0]+0.6,o[1],"X",ha="left",size=9)
T(ax,6.2,6.6,"D' from a NOT gate",size=7.6,color=MUTED,ha="left")
```

**Simplification by K-map.**

**Step 1 - K-map.** Enter 1 in each minterm cell, Gray-code ordered rows and columns so neighbouring cells differ in one variable.

```figure caption="4-variable K-map of X with the prime-implicant loops (cell numbers are minterm numbers)."
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

kmap(ax,0.9,0.4,4,[0, 2, 3, 7, 8, 10, 11, 14, 15],[],[([10, 11, 14, 15], '#d9534f'), ([3, 7, 11, 15], '#1d6fb8'), ([0, 2, 8, 10], '#2e8b57')],names='ABCD',cs=0.72,title='X')
```

**Step 2 - groups (largest possible, power of two).**

- Group 1 (loop colour red), cells 10, 11, 14, 15: variables that do not change survive, giving $AC$.
- Group 2 (loop colour blue), cells 3, 7, 11, 15: variables that do not change survive, giving $CD$.
- Group 3 (loop colour green), cells 0, 2, 8, 10: variables that do not change survive, giving $\overline{B}\overline{D}$.

**Step 3 - minimised expression.**

$$\boxed{X(A,B,C,D) = AC + CD + \overline{B}\overline{D}}$$

**Step 4 - realisation with logic gates (AND-OR, two-level).** The complemented inputs come from NOT gates.

```figure caption="AND-OR realisation of X = AC + CD + B'D'"
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

sopc(ax,[[(0, 1), (2, 1)], [(2, 1), (3, 1)], [(1, 0), (3, 0)]],['A', 'B', 'C', 'D'],out='X')
```

*Equivalent NAND-only form.* Replacing every AND and the OR by NAND gates (double inversion, De Morgan) gives the same function with 4 NAND gates (plus the input inverters).


@s 5
**Design of the synchronous 2-bit up/down counter with T flip-flops.**

*Step 1 - number of flip-flops.* $2^{1} < N \le 2^{2}$ needs $n=2$ flip-flops (T flip-flops), all clocked together (synchronous). The states are $Q1Q0$.

*Step 2 - excitation table of the T flip-flop.*

| Q | Q⁺ | T |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

*Step 3 - state / excitation table* (for each present state the next state, and the flip-flop inputs needed from the excitation table; X = don't care):

| Q1 | Q0 | M | Q1⁺ | Q0⁺ | T1 | T0 |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| 0 | 0 | 1 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 | 0 | 1 |

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
fig,ax=ckt_canvas(6.6,1.45,xlim=(0,10.9),ylim=(-0.2,2.4))

kmap(ax,0.9,0.4,3,[1, 2, 5, 6],[],[([2, 6], '#d9534f'), ([1, 5], '#1d6fb8')],names='ABCD',cs=0.55,title='T1')
kmap(ax,4.4,0.4,3,[0, 1, 2, 3, 4, 5, 6, 7],[],[([0, 1, 2, 3, 4, 5, 6, 7], '#d9534f')],names='ABCD',cs=0.55,title='T0')
```

The loops give

$$\begin{gathered} T_{1} = Q_0\overline{M} + \overline{Q_0}M \\ T_{0} = 1 \end{gathered}$$
*Step 5 - logic diagram.*

```figure caption="Logic diagram of the synchronous 2-bit up/down counter with T flip-flops."
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
fig,ax=ckt_canvas(6.9,4.6,xlim=(-0.4,19.2),ylim=(-9.5,3.0))

seqcirc(ax,'T',['Q1', 'Q0'],[{'T': [[(1, 1), (2, 0)], [(1, 0), (2, 1)]]}, {'T': '1'}],zterms=None,extra=['M'])
```

```figure caption="Timing diagram of the 2-bit up/down counter in the up mode (M = 0): 00, 01, 10, 11, 00, ... ; in the down mode (M = 1) the sequence is reversed: 00, 11, 10, 01, 00."
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
fig,ax=ckt_canvas(5.9,1.84,xlim=(-1.9,8.7),ylim=(-0.3,3.1))

clock(ax,0,2.1999999999999997,8)
guides(ax,[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],2.8999999999999995,-0.1)
wave(ax,1.05,[(0.0, 0), (1.05, 1), (3.05, 0), (5.05, 1), (7.05, 0)],8,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (5.05, 0), (6.05, 1), (7.05, 0)],8,'Q0')
```

Here $M = 0$ selects up counting and $M = 1$ selects down counting. Check: for $M=0$, $T_0 = 1$ and $T_1 = Q_0$ (the usual up counter); for $M=1$, $T_1 = \overline{Q_0}$ (down counter).


@s 6
**4-bit PISO (parallel-in, serial-out) shift register.** Each D input is fed by a 2-to-1 selector (two AND gates and an OR gate) controlled by the line $SH/\overline{LD}$. With $SH/\overline{LD}=0$ the parallel inputs $P_A\dots P_D$ are loaded into the four flip-flops at the next clock pulse; with $SH/\overline{LD}=1$ each stage takes the output of the previous stage (the first stage takes 0) and the data move towards $Q_D$, from where they leave serially, one bit per clock pulse.

```figure caption="4-bit PISO shift register: a 2:1 selector in front of each D input chooses between parallel load and shift."
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

fig,ax=ckt_canvas(5.9,3.2,xlim=(-2.2,15.6),ylim=(-1.2,4.4))
Ps=[ffb(ax,1.0+3.7*i,0.8,"FF"+"ABCD"[i],"D",w=1.2,h=1.5,qn=False) for i in range(4)]
for i in range(4):
    P=Ps[i]
    iy=3.4
    # 2:1 selection: AND(load.Pi) OR AND(shift.Q_prev)
    ins,o=gn(ax,"AND",P["D"][0]-1.45-1.0+0.2,2.95,n=2,w=0.7,lead=0.15) if False else (None,None)
    T(ax,P["D"][0]-0.25,P["D"][1]+0.27,"mux",size=7,color=MUTED) if False else None
    # data inputs
    mux(ax,P["D"][0]-1.6,2.62,2,[None,None],[],out="",sp=0.55,w=0.9,name="2:1") if False else None
# draw tiny 2:1 selectors as boxes
for i,P in enumerate(Ps):
    bx=P["D"][0]-0.95
    box(ax,bx,P["D"][1]-0.35,0.6,0.7,"2:1",size=7.4)
    L(ax,[(bx+0.6,P["D"][1]),P["D"]])
    L(ax,[(bx-0.0,P["D"][1]+0.17),(bx-0.2,P["D"][1]+0.17),(bx-0.2,3.3)]) ; T(ax,bx-0.2,3.55,"P"+"ABCD"[i],size=8.2)
    if i==0:
        L(ax,[(bx,P["D"][1]-0.17),(bx-0.45,P["D"][1]-0.17)]); T(ax,bx-0.5,P["D"][1]-0.17,"0",ha="right",size=8.2)
    else:
        q=Ps[i-1]["Q"]; L(ax,[q,(q[0]+0.2,q[1]),(q[0]+0.2,0.35),(bx-0.35,0.35),(bx-0.35,P["D"][1]-0.17),(bx,P["D"][1]-0.17)])
    L(ax,[(bx+0.3,P["D"][1]-0.35),(bx+0.3,-0.35)]); dot(ax,bx+0.3,-0.35) if False else None
    L(ax,[P["CK"],(P["CK"][0],-0.8)]); dot(ax,P["CK"][0],-0.8)
    T(ax,P["Q"][0]+0.12,P["Q"][1]+0.28,"Q"+"ABCD"[i],size=8.2,ha="left") if i<3 else None
for i,P in enumerate(Ps):
    L(ax,[(P["D"][0]-0.95+0.3,P["D"][1]-0.35),(P["D"][0]-0.95+0.3,-0.35)])
L(ax,[(Ps[0]["D"][0]-0.65,-0.35),(Ps[3]["D"][0]-0.65,-0.35)]); T(ax,Ps[0]["D"][0]-0.75,-0.35,"SH/$\\overline{LD}$",ha="right",size=8.2)
for i,P in enumerate(Ps): dot(ax,P["D"][0]-0.65,-0.35)
L(ax,[(Ps[0]["CK"][0],-0.8),(Ps[3]["CK"][0],-0.8)]); T(ax,Ps[0]["CK"][0]-0.1,-0.8,"CLK",ha="right",size=8.2)
L(ax,[Ps[3]["Q"],(Ps[3]["Q"][0]+0.6,Ps[3]["Q"][1])]); T(ax,Ps[3]["Q"][0]+0.7,Ps[3]["Q"][1],"Serial out",ha="left",size=8.4)
```

**Operation for the parallel word $P_AP_BP_CP_D = 1101$:**

| Clock pulse | QA | QB | QC | QD | Serial out (before the pulse) |
|---|---|---|---|---|---|
| load | 1 | 1 | 0 | 1 | - |
| 1 | 0 | 1 | 1 | 0 | 1 |
| 2 | 0 | 0 | 1 | 1 | 0 |
| 3 | 0 | 0 | 0 | 1 | 1 |
| 4 | 0 | 0 | 0 | 0 | 1 |

The serial output sequence read at $Q_D$ is 1, 0, 1, 1, that is the word 1101 sent out last bit first (D, C, B, A). Four clock pulses empty the register; the next pulse can load a new word.

```figure caption="Timing diagram of the 4-bit PISO register: parallel word 1101 loaded (SH/LD = 0) then shifted out serially (SH/LD = 1), LSB side (QD) first."
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
wave(ax,2.9499999999999997,[(0.0, 1), (0.05, 0)],4,'QA')
wave(ax,2.0,[(0.0, 1), (1.05, 0)],4,'QB')
wave(ax,1.05,[(0.0, 0), (0.05, 1), (2.05, 0)],4,'QC')
wave(ax,0.1,[(0.0, 1), (0.05, 0), (1.05, 1), (3.05, 0)],4,'QD')
wave(ax,5.3,[(0.0, 0), (0.5, 1)],4,'SH/LD')
```


@s 7
**Mod-12 asynchronous counter (JK flip-flops, positive-edge clock).** $2^4=16 > 12 > 2^3 = 8$, so four flip-flops are needed. The counter must skip the states 12 to 15, so it is reset when the count 12 ($1100$) is reached. The first state with $Q_3=Q_2=1$ is 1100, and no earlier count has both high, so a 2-input NAND of $Q_3$ and $Q_2$ detects it; the NAND output (active low) clears all the flip-flops.

All JK inputs are tied to 1 (toggle mode). The clock goes to $FF_0$, and since the flip-flops are positive-edge triggered, each later stage is clocked from $\overline{Q}$ of the previous one (so it toggles when the previous bit falls).

```figure caption="Mod-12 ripple counter with JK flip-flops: NAND of Q3 and Q2 clears the counter."
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
ins,o=gn(ax,"NAND",9.0,-1.3,n=2,w=0.9,lead=0.3)
L(ax,[(Ps[2]["Q"][0]+0.3,Ps[2]["Q"][1]),(Ps[2]["Q"][0]+0.3,ins[1][1]),ins[1]]); dot(ax,Ps[2]["Q"][0]+0.3,Ps[2]["Q"][1])
L(ax,[(Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1]),(Ps[3]["Q"][0]+0.3,-2.0),(7.7,-2.0),(7.7,ins[0][1]),ins[0]]); dot(ax,Ps[3]["Q"][0]+0.3,Ps[3]["Q"][1])
T(ax,o[0]+0.15,o[1],"to CLR of\nall four FFs",ha="left",size=7.8)
T(ax,13.0,-1.3,"clear (active low) when Q3Q2Q1Q0 = 1100",size=7.8,color=MUTED)
```

**Count sequence.**

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
| 10 | 1 | 0 | 1 | 0 |
| 11 | 1 | 0 | 1 | 1 |
| 12 (momentary) | 1 | 1 | 0 | 0 |
| 12 -> 0 | 0 | 0 | 0 | 0 |

```figure caption="Timing diagram of the mod-12 asynchronous counter (rising-edge clock): the state 1100 is momentary and clears the counter to 0000."
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
fig,ax=ckt_canvas(5.9,1.85,xlim=(-1.9,14.7),ylim=(-0.3,5.0))

clock(ax,0,4.1,14)
guides(ax,[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0],4.8,-0.1)
wave(ax,2.9499999999999997,[(0.0, 0), (7.26, 1), (11.26, 0)],14,'Q3')
wave(ax,2.0,[(0.0, 0), (3.19, 1), (7.19, 0)],14,'Q2')
wave(ax,1.05,[(0.0, 0), (1.12, 1), (3.12, 0), (5.12, 1), (7.12, 0), (9.12, 1), (11.12, 0), (13.12, 1)],14,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (5.05, 0), (6.05, 1), (7.05, 0), (8.05, 1), (9.05, 0), (10.05, 1), (11.05, 0), (12.05, 1), (13.05, 0)],14,'Q0')
```

$Q_3$ goes high for counts 8 to 11 only, so it is a square-ish wave at $f/12$ (high for 4 of 12 clock periods).


@s 8
**Design of the sequence detector for 010 (Mealy machine, overlapping sequences allowed, D flip-flops).** One input $X$ (serial data), one output $Z$; $Z=1$ for the clock period in which the last bit of **010** arrives.

*Step 1 - state diagram.* States remember how much of the pattern has been matched:

- $S_0$: no part of the pattern seen yet (reset state)
- $S_1$: the last 1 input bit 0 seen
- $S_2$: the last 2 input bits 01 seen

Edge labels are $X/Z$. After a complete match the machine falls back to the longest prefix of the pattern that is also a suffix of what was received (overlap).

```figure caption="State diagram (Mealy) of the 010 detector; labels are X/Z."
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

statediag(ax,['S0', 'S1', 'S2'],[(0, 1, '0/0'), (0, 0, '1/0'), (1, 1, '0/0'), (1, 2, '1/0'), (2, 1, '0/1'), (2, 0, '1/0')])
```

*Step 2 - state table.*

| Present state | X = 0: next / Z | X = 1: next / Z |
|---|---|---|
| S0 | S1 / 0 | S0 / 0 |
| S1 | S1 / 0 | S2 / 0 |
| S2 | S1 / 1 | S0 / 0 |

*Step 3 - state assignment.* Three states need $n = 2$ flip-flops: $S_0=00$, $S_1=01$, $S_2=10$ ($Q_1Q_0$). The code 11 is unused (don't care).

*Step 4 - excitation table of the D flip-flop.*

| Q | Q⁺ | D |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

*Step 5 - state/excitation table* with $Q_1Q_0$ the present state and $X$ the input:

| Q1 | Q0 | X | Q1⁺ | Q0⁺ | Z | D1 | D0 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |

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

kmap(ax,0.9,0.4,3,[3],[6, 7],[([3, 7], '#d9534f')],names='ABC',cs=0.6,title='D1')
kmap(ax,4.6000000000000005,0.4,3,[0, 2, 4],[6, 7],[([0, 2, 4, 6], '#d9534f')],names='ABC',cs=0.6,title='D0')
kmap(ax,8.3,0.4,3,[4],[6, 7],[([4, 6], '#d9534f')],names='ABC',cs=0.6,title='Z')
```

$$\begin{gathered} D_{1} = Q_0X \\ D_{0} = \overline{X} \\ Z = Q_1\overline{X} \end{gathered}$$
*Step 7 - logic diagram.*

```figure caption="Logic diagram of the 010 sequence detector (D flip-flops)."
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

seqcirc(ax,'D',['Q1', 'Q0'],[{'D': [[(1, 1), (2, 1)]]}, {'D': [[(2, 0)]]}],zterms=[[(0, 1), (2, 0)]],extra=['X'])
```

*Check with a test stream* $X = 0101010011$ (applied left to right): the states visited are S0, S1, S2, S1, S2, S1, S2, S1, S1, S2 and the output is $Z = 0010101000$, with a 1 exactly when the last three bits are 010 (including overlaps).

```figure caption="Timing diagram of the 010 detector for X = 0101010011: Z goes high in the period in which the last bit of 010 is applied (Mealy output, depends on X and the present state)."
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
wave(ax,2.95,[(0.0, 0), (0.55, 1), (1.55, 0), (2.55, 1), (3.55, 0), (4.55, 1), (5.55, 0), (7.55, 1)],10,'X')
wave(ax,2.0,[(0.0, 0), (1.55, 1), (2.55, 0), (3.55, 1), (4.55, 0), (5.55, 1), (6.55, 0)],10,'Z',color='#d9534f')
wave(ax,1.05,[(0.0, 0), (1.05, 1), (2.05, 0), (3.05, 1), (4.05, 0), (5.05, 1), (6.05, 0), (8.05, 1), (9.05, 0)],10,'Q1')
wave(ax,0.1,[(0.0, 0), (0.05, 1), (1.05, 0), (2.05, 1), (3.05, 0), (4.05, 1), (5.05, 0), (6.05, 1), (8.05, 0)],10,'Q0')
```


@s 9
**Two-input CMOS NAND gate.** Two PMOS transistors in **parallel** form the pull-up network (between $+V_{DD}$ and the output) and two NMOS transistors in **series** form the pull-down network (between the output and ground). Both inputs $A$ and $B$ drive one PMOS and one NMOS gate.

```figure caption="Circuit of a 2-input CMOS NAND gate (PMOS in parallel on top, NMOS in series below)."
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

fig,ax=ckt_canvas(5.9,4.2,xlim=(-2.2,9.0),ylim=(-5.0,6.0))
p1=mosfet(ax,0.8,3.0,kind="p"); p2=mosfet(ax,4.0,3.0,kind="p")
na=mosfet(ax,3.0,-1.0,kind="n"); nb=mosfet(ax,3.0,-3.2,kind="n")
# supply rail
L(ax,[(p1["D"][0],5.0),(p2["D"][0],5.0)]); L(ax,[p1["D"],(p1["D"][0],5.0)]); L(ax,[p2["D"],(p2["D"][0],5.0)]); T(ax,p2["D"][0]+0.15,5.35,"+V$_{DD}$",ha="left",size=8.6)
# output node
yo=1.0
L(ax,[(p1["S"][0],p1["S"][1]),(p1["S"][0],yo),(p2["S"][0],yo),(p2["S"][0],p2["S"][1])]); dot(ax,p2["S"][0],yo)
L(ax,[(p2["S"][0],yo),(8.0,yo)]); T(ax,8.1,yo,"Y",ha="left",size=9)
L(ax,[na["D"],(na["D"][0],yo)]); dot(ax,na["D"][0],yo)
L(ax,[nb["S"],(nb["S"][0],-4.5)]); L(ax,[(nb["S"][0]-0.4,-4.5),(nb["S"][0]+0.4,-4.5)]); L(ax,[(nb["S"][0]-0.25,-4.65),(nb["S"][0]+0.25,-4.65)]); L(ax,[(nb["S"][0]-0.1,-4.8),(nb["S"][0]+0.1,-4.8)])
# inputs
L(ax,[(-1.0,-1.0),(-1.0,3.0)]); dot(ax,-1.0,-1.0); L(ax,[(-1.0,3.0),p1["G"]]); L(ax,[(-1.0,-1.0),na["G"]]); T(ax,-1.1,-1.0,"A",ha="right",size=9)
L(ax,[(-1.8,-3.2),nb["G"]]); T(ax,-1.9,-3.2,"B",ha="right",size=9)
L(ax,[(2.0,-3.2),(2.0,3.0),p2["G"]]); dot(ax,2.0,-3.2)
T(ax,6.2,3.0,"PMOS pair\n(parallel pull-up)",size=7.8,color=MUTED,ha="left"); T(ax,5.4,-2.1,"NMOS pair\n(series pull-down)",size=7.8,color=MUTED,ha="left")
```

**Logic operation.**

| A | B | PMOS A | PMOS B | NMOS A | NMOS B | Output Y |
|---|---|---|---|---|---|---|
| 0 | 0 | on | on | off | off | 1 (pulled to VDD) |
| 0 | 1 | on | off | off | on | 1 |
| 1 | 0 | off | on | on | off | 1 |
| 1 | 1 | off | off | on | on | 0 (pulled to ground) |

If either input is low, at least one PMOS conducts and at least one NMOS of the series chain is open: $Y=1$. Only when $A=B=1$ do both NMOS conduct (path to ground) and both PMOS turn off: $Y=0$. So $Y = \overline{AB}$. In every steady state exactly one of the two networks is off, so there is no DC path from $V_{DD}$ to ground and the static power is almost zero.

**Characteristics of the TTL logic family** (standard 74 series):

- **Basic gate:** NAND, with a multi-emitter input transistor and a *totem-pole* output stage (two transistors, one pulls the output up, the other pulls it down); the supply is $V_{CC}= +5$ V ± 5 %.
- **Logic levels:** $V_{IH(min)} = 2$ V, $V_{IL(max)} = 0.8$ V, $V_{OH(min)} = 2.4$ V (typ. 3.4 V), $V_{OL(max)} = 0.4$ V (typ. 0.2 V).
- **Noise margin:** $NM_H = 2.4-2.0 = 0.4$ V, $NM_L = 0.8-0.4 = 0.4$ V.
- **Propagation delay:** about 10 ns per gate.
- **Power dissipation:** about 10 mW per gate (so the speed-power product is about 100 pJ).
- **Fan-out:** 10 standard loads ($I_{OL} = 16$ mA, $I_{IL}=1.6$ mA).
- **Unused inputs** float to logic 1 (high); they should still be tied to a defined level to avoid noise pick-up.
- **Variants:** Schottky (74S), low-power Schottky (74LS), advanced versions (74AS, 74ALS, 74F), with different speed/power trade-offs; open-collector and tri-state outputs for bus connection.


@s 10
**Time-interval (period) measurement.** A digital time-measuring instrument counts the number of pulses of a *known, accurate clock* that occur during the unknown interval.

```figure caption="Functional diagram of a digital time-interval meter."
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

fig,ax=ckt_canvas(5.9,2.5,xlim=(-1.6,17.0),ylim=(-1.2,4.6))
box(ax,0.0,2.4,3.0,1.2,"Input pulse\n(start/stop)",size=7.8)
box(ax,4.4,2.4,2.6,1.2,"Control\nflip-flop",size=7.8)
box(ax,0.0,0.2,3.0,1.2,"Crystal\noscillator",size=7.8)
box(ax,4.4,0.2,2.6,1.2,"Divider /\npulse shaper",size=7.8)
ins,o=gn(ax,"AND",8.4,2.0,n=2,w=0.9,lead=0.4)
box(ax,10.8,1.4,2.6,1.2,"Decade\ncounter",size=7.8); box(ax,14.0,1.4,2.2,1.2,"Display",size=7.8)
arr(ax,(3.0,3.0),(4.4,3.0)); arr(ax,(3.0,0.8),(4.4,0.8))
L(ax,[(7.0,3.0),(7.7,3.0),(7.7,ins[0][1]),ins[0]]); L(ax,[(7.0,0.8),(7.7,0.8),(7.7,ins[1][1]),ins[1]])
arr(ax,o,(10.8,2.0)); arr(ax,(13.4,2.0),(14.0,2.0))
T(ax,5.7,4.0,"gate: open for the interval T",size=7.8,color=MUTED); T(ax,5.7,-0.4,"clock pulses of period T$_c$",size=7.8,color=MUTED)
```

**Working.**

1. A crystal oscillator and divider produce clock pulses of known period $T_c$ (e.g. 1 MHz gives $T_c = 1\ \mu s$).
2. The start pulse (rising edge of the input) sets the control flip-flop, opening the AND gate; the stop pulse resets it and closes the gate. So the gate is open for exactly the unknown interval $T$.
3. While the gate is open the clock pulses pass to the decade counter, which counts $N$ pulses.
4. The display shows $T = N\,T_c$. The resolution is $\pm T_c$ (one count), so a faster clock gives better resolution, e.g. $N = 2347$ with $T_c = 1\ \mu s$ gives $T = 2.347$ ms.

The same arrangement gives the **period of a periodic signal** (gate open for one period of the input; use several periods and divide for small errors).



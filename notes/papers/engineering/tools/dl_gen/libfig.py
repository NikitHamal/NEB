PRE = r'''
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
'''

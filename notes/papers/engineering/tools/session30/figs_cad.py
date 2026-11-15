CPRE = r'''def dm(ax,p,q,t,off=(0,0.35),size=7,ha='center',color=INK):
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="<->",color=color,lw=0.8,shrinkA=0,shrinkB=0))
    ax.text((p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],t,ha=ha,va='center',fontsize=size,color=color)
def tx(ax,x,y,t,size=7,ha='center',color=INK,**k): ax.text(x,y,t,ha=ha,va='center',fontsize=size,color=color,**k)
def ld(ax,t,xy,xyt,size=7,ha='center'):
    ax.annotate(t,xy=xy,xytext=xyt,fontsize=size,ha=ha,va='center',arrowprops=dict(arrowstyle="-",lw=0.6,color=MUTED))
def hatch(ax,x0,x1,y,n=40,l=0.5):
    for x in np.linspace(x0,x1,n): ax.plot([x,x-l],[y,y-l],color=MUTED,lw=0.5)
'''

G = {}

G['c_canal_fill'] = r'''fig,ax=plt.subplots(figsize=(7.4,3.1)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-17,17); ax.set_ylim(-1.9,5.6)
emb=[(-13.5,0),(-7.5,3),(-4.5,3),(-1.5,1),(1.5,1),(4.5,3),(7.5,3),(13.5,0)]
ax.add_patch(plt.Polygon(emb,closed=True,fc="#eadfc9",ec=INK,lw=1.4))
ax.add_patch(plt.Polygon([(-1.5,1),(1.5,1),(3.75,2.5),(-3.75,2.5)],fc="#bcd7f2",ec="none"))
ax.plot([-4.5,4.5],[2.5,2.5],color="#1d6fb8",lw=1.1,ls="--")
ax.plot([-16,16],[0,0],color=INK,lw=1.0); hatch(ax,-15.5,15.5,0,n=52,l=0.6)
dm(ax,(-1.5,1.35),(1.5,1.35),"B = 3.0 m",off=(0,0.4),size=6.8)
ld(ax,"FSL (full supply level)",(3.2,2.5),(9.8,4.9),ha="left")
ld(ax,"canal bed (CBL)",(-1.4,1.0),(-9.0,0.55))
dm(ax,(6.2,1.0),(6.2,2.5),"D = 1.5 m",off=(0.15,0.0),size=6.8,ha="left")
dm(ax,(-6.0,2.5),(-6.0,3.0),"",off=(0,0))
ld(ax,"free board 0.5 m",(-6.0,2.75),(-10.6,4.5),ha="center")
dm(ax,(-7.5,3.5),(-4.5,3.5),"top width 3.0 m",off=(0,0.45),size=6.8)
dm(ax,(4.5,3.5),(7.5,3.5),"top width 3.0 m",off=(0,0.45),size=6.8)
tx(ax,3.9,1.15,"",size=6); ld(ax,"inner slope 1.5 H : 1 V",(3.0,2.0),(11.8,2.2),ha="left")
ld(ax,"outer slope 2 H : 1 V",(10.5,1.5),(14.2,3.1),ha="left")
tx(ax,2.0,0.45,"compacted embankment",size=6.6)
tx(ax,-16.5,-1.15,"natural ground level (NGL), top soil stripped; fill in 150-200 mm layers, 95 % MDD",size=6.4,ha="left")
ax.set_title("Typical canal section in complete fill (embankment)",fontsize=8)
'''

G['c_canal_cut'] = r'''fig,ax=plt.subplots(figsize=(7.4,2.9)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-14,14); ax.set_ylim(-3.4,2.4)
ax.add_patch(plt.Polygon([(-13,0),(-4.5,0),(-1.5,-2),(1.5,-2),(4.5,0),(13,0),(13,-3.0),(-13,-3.0)],closed=True,fc="#eadfc9",ec=INK,lw=1.4))
ax.add_patch(plt.Polygon([(-1.5,-2),(1.5,-2),(3.75,-0.5),(-3.75,-0.5)],fc="#bcd7f2",ec="none"))
ax.plot([-4.5,4.5],[-0.5,-0.5],color="#1d6fb8",lw=1.1,ls="--")
ax.plot([-4.5,4.5],[0,0],color=INK,lw=1.4); ax.plot([-13,13],[0,0],color=INK,lw=1.4)
dm(ax,(-1.5,-1.55),(1.5,-1.55),"B = 3.0 m",off=(0,0.0),size=6.6)
dm(ax,(5.4,-2.0),(5.4,-0.5),"D = 1.5 m",off=(0.2,0),size=6.8,ha="left")
dm(ax,(-8.0,-0.5),(-8.0,0),"",off=(0,0)); ld(ax,"free board 0.5 m",(-8.0,-0.25),(-9.5,1.2))
ld(ax,"FSL",(3.5,-0.5),(7.5,0.9)); ld(ax,"side slope 1.5 H : 1 V (in cut)",(3.0,-1.0),(8.8,-1.6),ha="left")
dm(ax,(4.5,0.5),(10.5,0.5),"inspection path / berm 3.0 m (min.)",off=(0,0.45),size=6.6)
dm(ax,(-10.5,0.5),(-4.5,0.5),"berm 3.0 m",off=(0,0.45),size=6.6)
ld(ax,"canal bed (CBL)",(0.0,-2.0),(0.0,-2.8)); tx(ax,-9.5,-2.4,"natural ground (cut in ordinary soil)",size=6.6)
ld(ax,"NGL = bank level",(10.5,0.0),(12.0,1.5),ha="center")
ax.set_title("Typical canal section in complete cut",fontsize=8)
'''

G['c_road_fill'] = r'''fig,ax=plt.subplots(figsize=(7.4,3.0)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-12,13); ax.set_ylim(-5.6,4.2)
xs=np.array([-11,11]); ax.plot(xs,-0.3*xs,color=INK,lw=1.0,ls="--")
yl=lambda x:-0.3*x
top=1.5; xl=-2.5; xr=2.5
# fill slopes 1.5:1 from platform edges down to ground
gl=(xl-1.5*0+0,top)
# uphill toe: solve ground y=-0.3x with slope from (xl,top) going left-down at 1.5H:1V
def toe(x0,y0,s):
    # point (x0+s*t, y0-t) on ground  -0.3(x0+s*t)=y0-t
    t=(y0+0.3*x0)/(0.3*s-1)*-1 if False else (-0.3*x0-y0)/(1-0.3*s)*-1
    return None
import numpy as _n
def solve(x0,y0,s):
    # s=+1.5 for downhill (right), -1.5 for left; ground y=-0.3x ; point=(x0+s*t, y0-t)
    t=(y0+0.3*x0)/(1-0.3*s)
    return (x0+s*t,y0-t)
L=solve(xl,top,-1.5); R=solve(xr,top,1.5)
ax.add_patch(plt.Polygon([L,(xl,top),(xr,top),R],closed=True,fc="#eadfc9",ec=INK,lw=1.4))
ax.plot([-11,L[0]],[yl(-11),L[1]],color=INK,lw=1.4); ax.plot([R[0],11],[R[1],yl(11)],color=INK,lw=1.4)
ax.plot([xl,xr],[top,top],color=INK,lw=2.2)
tx(ax,0,top-0.6,"compacted fill",size=7); 
dm(ax,(xl,top+0.45),(xr,top+0.45),"formation width 5.0 m",off=(0,0.5),size=6.6)
ld(ax,"side drain 0.6 m",(-2.3,top),(-6.0,3.3)); ld(ax,"fill slope 1.5 H : 1 V",(R[0]-1.2,R[1]+0.9),(8.8,1.5),ha="left")
ld(ax,"camber / crossfall 5 % (inward)",(0.5,top+0.04),(7.0,3.4),ha="left")
ld(ax,"toe wall / gabion (if fill > 2 m)",R,(9.8,-4.2),ha="center")
ld(ax,"catch drain",(L[0]-0.3,L[1]),(-9.0,-1.6)); ld(ax,"original ground (NGL)",(-9.0,2.7),(-9.5,3.9),ha="center")
ax.set_title("Typical hill-road section in complete fill",fontsize=8)
'''

G['c_road_cutfill'] = r'''fig,ax=plt.subplots(figsize=(7.4,3.1)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-12,13); ax.set_ylim(-5.0,5.0)
yl=lambda x:-0.3*x
xs=np.array([-11,11]); ax.plot(xs,yl(xs),color=INK,lw=1.0,ls="--")
xl=-2.5; xr=2.5; yp_l=0.0; yp_r=0.0+0.22
# cut face from (xl,0) going up-left at 0.5H:1V : point (xl-0.5t, t)
t=(-yl(xl)+0.0)  # placeholder
tc=(0-(-0.3)*(-xl))  # unused
# solve cut: ground y=-0.3x ; point (xl-0.5t, t): t=-0.3(xl-0.5t) -> t=-0.3xl+0.15t -> t=-0.3xl/0.85
tc=-0.3*xl/0.85; C=(xl-0.5*tc,tc)
# solve fill: (xr+1.5s, yp_r - s): yp_r-s=-0.3(xr+1.5s) -> yp_r-s=-0.3xr-0.45s -> s=(yp_r+0.3xr)/0.55
sf=(yp_r+0.3*xr)/0.55; Fp=(xr+1.5*sf,yp_r-sf)
ax.add_patch(plt.Polygon([(xl,yl(xl)),C,(xl,0)],closed=True,fc="#f3c9c4",ec="none"))
ax.add_patch(plt.Polygon([(xr,yl(xr)),(xr,yp_r),Fp],closed=True,fc="#d7e6c9",ec="none"))
prof=[(-11,yl(-11)),C,(xl,0),(-2.2,-0.38),(-1.9,0),(xr,yp_r),Fp,(11,yl(11))]
ax.plot([p[0] for p in prof],[p[1] for p in prof],color=INK,lw=1.6)
ax.plot([-1.9,xr],[0,yp_r],color=INK,lw=2.4)
tx(ax,C[0]+0.2,C[1]*0.35,"CUT",size=7,color="#b0413e"); tx(ax,3.2,-0.5,"FILL",size=7,color="#3d7a2e")
ld(ax,"catch drain (top of cut)",(C[0]-0.6,C[1]+0.05),(-9.0,3.6),ha="center")
ld(ax,"cut slope 0.5 H : 1 V (rock) / 1 H : 1 V (soil)",(-2.75,0.4),(-8.6,4.4),ha="left") if False else ld(ax,"cut slope 1 H : 2 V in hard soil / rock, 1 H : 1 V in ordinary soil",(C[0]+0.3,C[1]*0.55),(-3.0,4.5),ha="left")
ld(ax,"side drain 0.6 m",(-2.2,-0.38),(-7.2,-2.4)); ld(ax,"carriageway 3.0 m with 0.5 m shoulders, crossfall 5 %",(0.2,0.05),(4.0,3.0),ha="left")
ld(ax,"fill slope 1.5 H : 1 V",((xr+Fp[0])/2,(yp_r+Fp[1])/2),(8.4,1.2),ha="left"); ld(ax,"toe wall (dry stone / gabion)",Fp,(8.6,-3.9),ha="center")
dm(ax,(-2.5,-1.3),(2.5,-1.3),"formation width 5.0 m",off=(0,-0.4),size=6.6)
ld(ax,"original ground (NGL)",(-9.0,2.7),(-10.0,0.8),ha="center")
ax.set_title("Typical hill-road section in partial cut and fill (side-hill)",fontsize=8)
'''

G['c_retaining'] = r'''fig=plt.figure(figsize=(7.4,2.9))
def panel(i,title):
    a=fig.add_axes([0.01+i*0.335,0.04,0.32,0.84]); a.set_aspect('equal'); a.axis('off'); a.set_xlim(-0.8,5.2); a.set_ylim(-0.6,5.1); a.set_title(title,fontsize=7.4); return a
a=panel(0,"(a) gravity (stone masonry / PCC)")
a.add_patch(plt.Polygon([(2.4,0),(1.8,4),(4.9,4),(4.9,0)],fc="#eadfc9",ec="none")); hatch(a,2.0,4.8,3.9,n=12,l=0.5)
a.add_patch(plt.Polygon([(0,0),(2.4,0),(1.8,4),(1.1,4)],fc="#cfd4dc",ec=INK,lw=1.3)); a.plot([-0.5,0.0],[0.4,0.4],color=INK); a.plot([-0.5,-0.5],[0.4,0.4],color=INK)
a.plot([-0.7,0.0],[0.5,0.5],color=INK,lw=1.0); a.plot([0,0.2],[0.5,0.5],color=INK,lw=1.0)
tx(a,1.45,2.0,"masonry / PCC",size=6.4); tx(a,3.5,2.0,"backfill",size=6.6); dm(a,(0,-0.3),(2.4,-0.3),"B = 0.5–0.7 H",off=(0,-0.25),size=6.2); dm(a,(1.1,4.35),(1.8,4.35),"0.6 m",off=(0,0.25),size=6.2); a.plot([-0.7,5.1],[0,0],color=INK,lw=0.8)
tx(a,0.35,4.8,"H",size=7); a.annotate("",xy=(-0.35,4.0),xytext=(-0.35,0.5),arrowprops=dict(arrowstyle="<->",lw=0.7)); tx(a,-0.55,2.3,"H",size=7)
b=panel(1,"(b) cantilever RCC (inverted T)")
b.add_patch(plt.Polygon([(1.0,0.5),(0.85,4.0),(4.9,4.0),(4.9,0.5)],fc="#eadfc9",ec="none")); hatch(b,1.0,4.8,3.9,n=12,l=0.5)
b.add_patch(plt.Polygon([(0,0),(2.4,0),(2.4,0.5),(1.0,0.5),(0.85,4.0),(0.6,4.0),(0.6,0.5),(0,0.5)],fc="#cfd4dc",ec=INK,lw=1.3))
b.plot([-0.7,5.1],[0.5,0.5],color=INK,lw=0.8,ls="--"); tx(b,3.4,2.2,"backfill",size=6.6); tx(b,0.1,-0.35,"toe",size=6.2); tx(b,1.9,-0.35,"heel",size=6.2); dm(b,(0,-0.75),(2.4,-0.75),"B = 0.5–0.7 H",off=(0,-0.2),size=6.2)
tx(b,0.72,4.45,"stem",size=6.4); tx(b,1.3,0.25,"base slab",size=5.6)
c=panel(2,"(c) counterfort (section through a counterfort)")
c.add_patch(plt.Polygon([(1.0,0.5),(0.85,4.0),(4.9,4.0),(4.9,0.5)],fc="#eadfc9",ec="none"))
c.add_patch(plt.Polygon([(0,0),(2.4,0),(2.4,0.5),(1.0,0.5),(0.85,4.0),(0.6,4.0),(0.6,0.5),(0,0.5)],fc="#cfd4dc",ec=INK,lw=1.3))
c.add_patch(plt.Polygon([(0.85,4.0),(2.4,0.5),(1.0,0.5)],fc="#b9c2cf",ec=INK,lw=1.0,ls="--")); tx(c,1.45,1.55,"counterfort",size=5.8); tx(c,3.4,2.2,"backfill",size=6.6); c.plot([-0.7,5.1],[0.5,0.5],color=INK,lw=0.8,ls="--")
tx(c,2.6,-0.35,"used for H > 6 m, counterforts at 2.5-3.5 m c/c",size=5.6)
'''

G['c_cantilever4'] = r'''fig,ax=plt.subplots(figsize=(7.4,3.5)); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-2.2,7.4); ax.set_ylim(-1.4,5.2)
ax.add_patch(plt.Polygon([(1.0,0.5),(0.85,4.0),(5.6,4.0),(5.6,0.5)],fc="#eadfc9",ec="none")); hatch(ax,1.0,5.5,3.95,n=14,l=0.4)
ax.add_patch(plt.Polygon([(0,0),(2.4,0),(2.4,0.5),(1.0,0.5),(0.85,4.0),(0.6,4.0),(0.6,0.5),(0,0.5)],fc="#cfd4dc",ec=INK,lw=1.5))
ax.add_patch(plt.Rectangle((-0.1,-0.1),2.6,0.1,fc="#9a9a9a",ec=INK,lw=0.6)); ax.plot([-1.0,5.6],[0.5,0.5],color=INK,lw=0.9)
ax.add_patch(plt.Rectangle((1.2,-0.4),0.3,0.3,fc="#cfd4dc",ec=INK,lw=0.9))
ax.add_patch(plt.Rectangle((1.9,0.55),0.5,1.0,fc="#d9e6d2",ec="none")); tx(ax,4.0,2.0,"granular filter (drainage layer)",size=6.4)
ax.plot([0.6,0.6],[0.5,3.9],color=INK,lw=0.0); ax.plot([0.62,0.62],[0.62,3.9],color="#b0413e",lw=0.8,ls="--")
ax.plot([0.12,0.12,2.3],[0.5,0.12,0.12],color="#b0413e",lw=0.8,ls="--")
dm(ax,(-1.9,0.0),(-1.9,4.0),"H = 4.0 m",off=(-0.15,0),size=7,ha="right"); dm(ax,(-0.5,0.5),(-0.5,4.0),"stem 3.5 m",off=(-0.15,0),size=6.6,ha="right")
dm(ax,(0,-0.55),(0.6,-0.55),"0.60",off=(0,-0.3),size=6.2); dm(ax,(0.6,-0.55),(1.0,-0.55),"0.40",off=(0,-0.3),size=6.2); dm(ax,(1.0,-0.55),(2.4,-0.55),"1.40",off=(0,-0.3),size=6.2)
dm(ax,(0,-1.15),(2.4,-1.15),"B = 2.40 m (toe 0.60 + stem 0.40 + heel 1.40)",off=(1.6,0),size=6.4,ha="left")
dm(ax,(2.6,0.0),(2.6,0.5),"",off=(0,0)); tx(ax,2.7,0.12,"slab 0.50 m",size=6.2,ha="left")
dm(ax,(0.6,4.35),(0.85,4.35),"top 0.25",off=(0,0.3),size=6.2)
ld(ax,"weep holes 100 mm @ 2 m c/c",(0.95,1.0),(-1.6,1.8),ha="center") if False else ld(ax,"weep hole 100 mm dia. @ 2 m c/c (PVC)",(0.80,0.85),(4.6,0.95),ha="left")
ld(ax,"PCC 1:3:6 blinding, 100 mm",(2.0,-0.05),(4.8,-0.45),ha="center"); ld(ax,"shear key (optional)",(1.35,-0.25),(4.3,-1.0),ha="center") if False else None
ld(ax,"main bars at the earth face (tension)",(0.9,2.4),(5.9,2.6),ha="center") if False else tx(ax,4.6,3.0,"backfill (granular)",size=6.6)
ld(ax,"RCC M25, Fe500: main bars 16 @ 150 at back face,\ndistribution 10 @ 200, cover 50 mm (earth face)",(0.66,2.9),(4.4,4.7),ha="center")
ax.set_title("Typical section of a 4 m high cantilever retaining wall",fontsize=8)
'''

G['c_titleblock'] = r'''fig=plt.figure(figsize=(7.4,3.2))
a=fig.add_axes([0.0,0.02,0.40,0.92]); a.set_aspect('equal'); a.axis('off'); a.set_xlim(-2,44); a.set_ylim(-2,32)
a.add_patch(plt.Rectangle((0,0),42,29.7,fc="white",ec=INK,lw=1.2)); a.add_patch(plt.Rectangle((2.5,0.5),39,28.7,fc="none",ec=INK,lw=1.8))
a.add_patch(plt.Rectangle((23.5,0.5),18,8,fc="#e8eefb",ec=INK,lw=1.2)); tx(a,32.5,4.5,"title\nblock",size=7)
tx(a,13,18,"DRAWING AREA\n(border line 0.5 mm,\nmargin 25 mm left /\n5 mm others)",size=6.6); tx(a,21,31,"A3 sheet 420 × 297 mm",size=7)
b=fig.add_axes([0.42,0.02,0.57,0.92]); b.set_aspect('equal'); b.axis('off'); b.set_xlim(-0.5,18.5); b.set_ylim(-1.5,12.5)
b.add_patch(plt.Rectangle((0,0),18,10,fc="white",ec=INK,lw=1.6))
for y in (2,4,6,8): b.plot([0,18],[y,y],color=INK,lw=0.9)
b.plot([6,6],[8,10],color=INK,lw=0.9); b.plot([12,12],[4,6],color=INK,lw=0.9)
for x in (4.5,9,13.5): b.plot([x,x],[0,2],color=INK,lw=0.9)
for x in (4,8,12): b.plot([x,x],[2,4],color=INK,lw=0.9)
tx(b,3,9.0,"CONSULTANT\nname · address · logo",size=6.2); tx(b,12,9.0,"CLIENT / OWNER",size=6.4)
tx(b,9,7.0,"PROJECT:  name and location of the project",size=6.4); tx(b,6,5.0,"DRAWING TITLE (e.g. Typical canal section)",size=6.2); tx(b,15,5.0,"DRAWING No.",size=6.2)
for x,t in ((2,"SCALE\n1:100"),(6,"DATE\n2082/06/15"),(10,"SHEET\n3 of 12"),(15,"REVISION / STATUS")): tx(b,x,3.0,t,size=5.8)
for x,t in ((2.25,"DRAWN"),(6.75,"DESIGNED"),(11.25,"CHECKED"),(15.75,"APPROVED")): tx(b,x,1.0,t+"\n(sign / date)",size=5.6)
tx(b,9,11.2,"Typical title block (A3, 180 × 100 mm), drawn in the lower right corner",size=6.8)
dm(b,(0,-0.7),(18,-0.7),"180 mm",off=(0,-0.35),size=6.4)
'''

G['c_locsite'] = r'''fig=plt.figure(figsize=(7.4,3.2))
a=fig.add_axes([0.01,0.02,0.47,0.88]); a.set_xlim(0,10); a.set_ylim(0,8); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([]); a.set_title("Location map (1:5000, key to the site)",fontsize=7.4)
a.plot([0,10],[3.2,3.2],color=INK,lw=3); a.plot([6,6],[0,8],color=INK,lw=2); a.plot([0,6],[6.5,6.5],color=MUTED,lw=1.2)
xx=np.linspace(0,10,60); a.plot(xx,1.1+0.5*np.sin(xx*0.8),color="#1d6fb8",lw=3); tx(a,1.6,0.5,"river",size=6.4,color="#1d6fb8")
a.add_patch(plt.Rectangle((6.5,3.6),0.9,0.9,fc="#e5483f",ec=INK,lw=1)); ld(a,"SITE (plot no. 12)",(7.4,4.4),(8.0,6.0),size=6.6)
a.add_patch(plt.Rectangle((2.4,3.7),1.0,0.8,fc="#d9d9d9",ec=INK,lw=0.8)); tx(a,2.9,4.1,"school",size=5.8)
a.add_patch(plt.Rectangle((7.8,1.9),1.0,0.8,fc="#d9d9d9",ec=INK,lw=0.8)); tx(a,8.3,2.3,"temple",size=5.8)
tx(a,1.5,3.55,"Main road (12 m ROW)",size=5.8,ha="left"); tx(a,6.1,7.5,"Ring Road",size=5.8,ha="left",rotation=90)
a.annotate("N",xy=(9.2,7.5),xytext=(9.2,6.4),fontsize=8,ha="center",arrowprops=dict(arrowstyle="-|>",lw=1.2)); tx(a,1.2,7.4,"Scale 1:5000",size=6.4)
b=fig.add_axes([0.52,0.02,0.47,0.88]); b.set_xlim(0,14); b.set_ylim(0,11); b.set_aspect('equal'); b.set_xticks([]); b.set_yticks([]); b.set_title("Site plan (1:200)",fontsize=7.4)
b.add_patch(plt.Rectangle((0,0),14,2.2,fc="#e6e6e6",ec="none")); tx(b,7,1.1,"ROAD  (ROW 8 m)",size=6.6)
b.add_patch(plt.Polygon([(1,2.8),(13,2.8),(13,10.4),(1,10.4)],fc="none",ec=INK,lw=1.6,ls="-")); tx(b,7,10.75,"plot boundary 12.0 m × 7.6 m (boundary wall)",size=5.6)
b.add_patch(plt.Rectangle((2.8,4.8),6.4,4.2,fc="#cfd4dc",ec=INK,lw=1.4)); tx(b,6,7.3,"proposed\nbuilding",size=6.6)
dm(b,(1,3.4),(2.8,3.4),"",off=(0,0)); tx(b,1.9,3.65,"1.8",size=5.8)
dm(b,(9.2,3.4),(13,3.4),"",off=(0,0)); tx(b,11.1,3.65,"3.8",size=5.8)
dm(b,(5.4,2.8),(5.4,4.8),"front setback 2.0 m",off=(0.15,0),size=5.6,ha="left"); dm(b,(6.0,9.0),(6.0,10.4),"",off=(0,0)); tx(b,6.5,9.7,"rear 1.4",size=5.6,ha="left")
b.add_patch(plt.Rectangle((10.0,5.4),2.2,2.0,fc="#d9e6d2",ec=INK,lw=1)); tx(b,11.1,6.4,"septic\ntank",size=5.8)
b.plot([3.4,4.6],[2.8,2.8],color="#f4f4f4",lw=4); tx(b,4.0,3.15,"gate",size=5.4)
b.annotate("N",xy=(12.6,10.0),xytext=(12.6,8.9),fontsize=8,ha="center",arrowprops=dict(arrowstyle="-|>",lw=1.2))
'''

G['c_dtmflow'] = r'''fig=blockchain([("1  Survey data","P, E, N, Z, D (.txt/.csv)"),("2  Import points","PENZD, set units"),("3  Break lines","ridge, road edge, stream"),("4  Create DTM","triangulate, clip boundary"),("5  Contours","interval 1 m, major 5 m"),("6  Alignment","centre line (IPs, curves)"),("7  L-section","ground profile, scales 1:1000 / 1:100"),("8  Cross-sections","every 20 m, ±20 m"),("9  Export","DXF / DWG to AutoCAD, plot")],cols=3,figsize=(7.2,3.1))
'''

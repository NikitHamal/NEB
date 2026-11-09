# Figure code strings for the Electronic Device and Circuits papers (ENEX/EX 151).
# Each value is the body of a ```figure block (names from notes/pipeline/ckt.py are pre-injected).
F = {}

# ---------------------------------------------------------------- small-signal models
F['cb_ss'] = r'''
fig,ax=ckt_canvas(5.6,2.6,xlim=(-0.8,9.4),ylim=(-0.6,3.8))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.45,1.5),"v$_i$",size=9)
wire(ax,[(0,3),(1.6,3)]); wire(ax,[(0,0),(8.4,0)])
res(ax,(1.6,3),(1.6,0),"R$_E$",side=-1,off=0.55)
node(ax,(1.6,3)); wire(ax,[(1.6,3),(3.2,3)]); node(ax,(3.2,3))
res(ax,(3.2,3),(3.2,0),"r$_e$",side=-1,off=0.55)
wire(ax,[(3.2,3),(5.0,3)]); isrc(ax,(5.0,0),(5.0,3),None); label(ax,(5.6,1.5),"αi$_e$",ha="left",size=9)
wire(ax,[(5.0,3),(6.8,3)]); node(ax,(6.8,3)); res(ax,(6.8,3),(6.8,0),"R$_C$",side=1,off=0.55)
wire(ax,[(6.8,3),(8.4,3)]); terminal(ax,(8.4,3)); terminal(ax,(8.4,0)); label(ax,(8.9,1.5),"v$_o$",size=9)
node(ax,(1.6,0)); node(ax,(3.2,0)); node(ax,(5.0,0)); node(ax,(6.8,0))
arrow(ax,(2.0,3.45),(2.9,3.45),"i$_e$",off=0.25)
'''

F['ce_ss'] = r'''
fig,ax=ckt_canvas(6.0,3.2,xlim=(-0.9,9.8),ylim=(-0.6,4.7))
terminal(ax,(0,2.6)); terminal(ax,(0,0)); label(ax,(-0.5,1.3),"v$_i$",size=9)
wire(ax,[(0,2.6),(2.0,2.6)]); node(ax,(2.0,2.6)); res(ax,(2.0,2.6),(2.0,0),"R$_B$",side=-1,off=0.55)
wire(ax,[(2.0,2.6),(3.4,2.6)]); label(ax,(2.7,2.95),"B",size=8)
res(ax,(3.4,2.6),(3.4,1.4),"r$_π$",side=1,off=0.55,body=0.8)
wire(ax,[(3.4,1.4),(6.2,1.4)]); node(ax,(3.4,1.4)); label(ax,(3.1,1.7),"E",size=8,ha="right")
res(ax,(3.4,1.4),(3.4,0),"R$_E$",side=-1,off=0.55,body=0.9)
isrc(ax,(5.0,1.4),(5.0,4.0),None); label(ax,(5.5,2.7),"βi$_b$",ha="left",size=9)
node(ax,(5.0,1.4)); res(ax,(6.2,4.0),(6.2,1.4),"r$_o$",side=1,off=0.5,body=0.8)
wire(ax,[(5.0,4.0),(8.6,4.0)]); node(ax,(6.2,4.0)); node(ax,(7.6,4.0)); label(ax,(4.6,4.35),"C",size=8)
res(ax,(7.6,4.0),(7.6,0),"R$_C$",side=1,off=0.55)
wire(ax,[(0,0),(8.6,0)]); node(ax,(2.0,0)); node(ax,(3.4,0)); node(ax,(7.6,0))
terminal(ax,(8.6,4.0)); terminal(ax,(8.6,0)); label(ax,(9.1,2.0),"v$_o$",size=9)
arrow(ax,(1.0,2.95),(1.8,2.95),"i$_b$",off=0.25)
'''

F['cc_ss'] = r'''
fig,ax=ckt_canvas(5.6,2.8,xlim=(-0.9,9.2),ylim=(-0.6,4.0))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.5,1.5),"v$_i$",size=9)
wire(ax,[(0,3),(1.2,3)]); node(ax,(1.2,3)); res(ax,(1.2,3),(1.2,0),"R$_B$",side=-1,off=0.55)
wire(ax,[(1.2,3),(2.8,3)]); res(ax,(2.8,3),(2.8,1.5),"r$_π$",side=-1,off=0.55,body=0.8)
wire(ax,[(2.8,1.5),(7.0,1.5)]); node(ax,(2.8,1.5)); node(ax,(4.6,1.5))
isrc(ax,(4.6,0),(4.6,1.5),None); label(ax,(5.1,0.75),"βi$_b$",ha="left",size=9)
node(ax,(6.2,1.5)); res(ax,(6.2,1.5),(6.2,0),"R$_E$",side=1,off=0.5)
wire(ax,[(6.2,1.5),(7.6,1.5)]); terminal(ax,(7.6,1.5)); terminal(ax,(7.6,0)); label(ax,(8.1,0.75),"v$_o$",size=9)
wire(ax,[(0,0),(7.6,0)]); node(ax,(1.2,0)); node(ax,(4.6,0)); node(ax,(6.2,0))
label(ax,(5.6,2.5),"collector at a.c. ground",size=7.4,ha="left")
'''

# ---------------------------------------------------------------- BJT switch
F['bjt_switch'] = r'''
fig=plt.figure(figsize=(7.2,2.9))
ax=fig.add_axes([0.0,0.0,0.46,1.0]); ax.set_xlim(-1.2,6.2); ax.set_ylim(-0.8,5.2); ax.set_aspect('equal'); ax.axis('off')
ax.plot([3.4,3.4],[5.0,4.3],color=INK,lw=1.4); ax.text(3.4,5.05,"+V$_{CC}$",ha="center",fontsize=8.4)
res(ax,(3.4,4.3),(3.4,3.0),"R$_C$",side=1,off=0.45,body=0.8)
wire(ax,[(3.4,3.0),(3.4,2.5)])
bj=bjt(ax,2.4,1.5)
wire(ax,[(3.0,2.6),(3.4,2.6),(3.4,3.0)])
wire(ax,[bj["E"],(3.0,0.4),(3.0,0.0)]); gnd(ax,(3.0,0.0))
res(ax,(0.0,1.5),bj["B"],"R$_B$",side=1,off=0.5,body=0.9)
terminal(ax,(-0.4,1.5)); wire(ax,[(-0.4,1.5),(0,1.5)]); label(ax,(-0.4,1.95),"V$_i$",size=8.4,ha="center")
terminal(ax,(3.4,3.0)); label(ax,(4.2,3.0),"V$_o$",size=8.4,ha="left"); wire(ax,[(3.4,3.0),(3.8,3.0)])
bx=fig.add_axes([0.54,0.16,0.44,0.78])
vce=np.linspace(0,10,200)
for ib in (0,20,40,60,80):
    ic=np.minimum(ib*0.05*(1+0.01*vce),vce*3.2)*1.0; bx.plot(vce,ic,color="#8a8a8a" if ib==0 else INK,lw=0.9)
bx.plot([0,10],[4.2,0],color=ACCENT,lw=1.6)
bx.scatter([0.35,10],[3.95,0],color=ACCENT,zorder=5,s=22)
bx.text(0.7,4.45,"ON: saturation (switch closed)",fontsize=7.4,color=ACCENT)
bx.text(5.6,0.45,"OFF: cut-off (I$_B$ = 0)",fontsize=7.4,color=ACCENT)
bx.text(5.2,2.6,"d.c. load line",fontsize=7.4,color=ACCENT,rotation=-22)
bx.set_xlabel("V$_{CE}$ (V)",fontsize=8.4); bx.set_ylabel("I$_C$ (mA)",fontsize=8.4)
bx.set_xlim(0,10.5); bx.set_ylim(0,5.2)
for s in ("top","right"): bx.spines[s].set_visible(False)
'''

# ---------------------------------------------------------------- JFET / MOSFET structure and characteristics
F['jfet_char'] = r'''
fig=plt.figure(figsize=(7.4,2.7))
a=fig.add_axes([0.0,0.02,0.30,0.95]); a.set_xlim(0,10); a.set_ylim(0,9); a.axis('off')
a.add_patch(Rectangle((1,2.4),8,4.2,fc="#e4ecf7",ec=INK,lw=1.2))
a.add_patch(Polygon([(2.4,6.6),(7.6,6.6),(6.9,5.1),(3.1,5.1)],fc="#f7e3e3",ec=INK,lw=1))
a.add_patch(Polygon([(2.4,2.4),(7.6,2.4),(6.9,3.9),(3.1,3.9)],fc="#f7e3e3",ec=INK,lw=1))
a.add_patch(Rectangle((2.4,6.6),5.2,0.9,fc="#cfe0f5",ec=INK,lw=1.2)); a.add_patch(Rectangle((2.4,1.5),5.2,0.9,fc="#cfe0f5",ec=INK,lw=1.2))
a.text(5,7.05,"p (gate)",ha="center",va="center",fontsize=7.6); a.text(5,1.95,"p (gate)",ha="center",va="center",fontsize=7.6)
a.text(5,4.5,"n channel",ha="center",va="center",fontsize=8)
a.text(5,5.65,"depletion",ha="center",va="center",fontsize=6.4,color=ACCENT)
a.plot([1,1],[4.5,4.5]); a.text(0.6,4.5,"S",fontsize=9,ha="right",va="center"); a.text(9.4,4.5,"D",fontsize=9,va="center")
a.plot([5,5],[7.5,8.4],color=INK,lw=1.2); a.text(5,8.7,"G",ha="center",fontsize=9)
b=fig.add_axes([0.40,0.18,0.28,0.72]); VGS=[0,-1,-2,-3,-4]; vds=np.linspace(0,12,300); IDSS=8; VP=-4
for vg in VGS:
    ids=IDSS*(1-vg/VP)**2; vk=VP*0+ (vg-VP)
    i=np.where(vds<vk, ids*(2*vds/ max(vk,1e-6)-(vds/max(vk,1e-6))**2), ids) if vk>0 else np.zeros_like(vds)
    b.plot(vds,i,color=INK,lw=1.0); b.text(12.1,ids,f"{vg} V",fontsize=6.6,va="center")
xs=np.linspace(0,4,60); b.plot(xs,0.5*xs**2,color=ACCENT,lw=1.0,ls="--"); b.text(1.2,6.2,"pinch-off locus",fontsize=6.4,color=ACCENT,rotation=40)
b.set_xlabel("V$_{DS}$ (V)",fontsize=8); b.set_ylabel("I$_D$ (mA)",fontsize=8); b.set_xlim(0,14); b.set_ylim(0,9.5)
b.text(8.4,8.7,"V$_{GS}$ = 0",fontsize=7); b.set_title("drain characteristics",fontsize=8)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.77,0.18,0.22,0.72]); v=np.linspace(-4,0,100); c.plot(v,IDSS*(1-v/VP)**2,color=INK,lw=1.4)
c.scatter([-4,0],[0,8],color=ACCENT,zorder=5,s=16); c.text(-3.9,0.6,"V$_P$",fontsize=7.4,color=ACCENT); c.text(-1.7,8.3,"I$_{DSS}$",fontsize=7.4,color=ACCENT)
c.set_xlabel("V$_{GS}$ (V)",fontsize=8); c.set_ylabel("I$_D$ (mA)",fontsize=8); c.set_title("transfer curve",fontsize=8); c.set_ylim(0,9.5)
for s in ("top","right"): c.spines[s].set_visible(False)
'''

F['dmos_char'] = r'''
fig=plt.figure(figsize=(7.4,2.8))
a=fig.add_axes([0.0,0.02,0.32,0.95]); a.set_xlim(0,12); a.set_ylim(0,9); a.axis('off')
a.add_patch(Rectangle((1,1.0),10,3.6,fc="#efe9dc",ec=INK,lw=1.2)); a.text(6,1.8,"p-type substrate (SS)",ha="center",fontsize=7.4)
a.add_patch(Rectangle((1.8,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1)); a.add_patch(Rectangle((8.0,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1))
a.add_patch(Rectangle((4.0,3.4),4.0,0.55,fc="#9fc4ee",ec=INK,lw=0.8))
a.text(2.9,4.0,"n+",ha="center",va="center",fontsize=8); a.text(9.1,4.0,"n+",ha="center",va="center",fontsize=8)
a.text(6,3.68,"n channel (built-in)",ha="center",va="center",fontsize=6.2)
a.add_patch(Rectangle((4.0,4.0),4.0,0.35,fc="#d9d9d9",ec=INK,lw=0.8)); a.text(8.3,4.17,"SiO$_2$",fontsize=6.2,va="center")
a.add_patch(Rectangle((4.2,4.35),3.6,0.7,fc="#b9b9b9",ec=INK,lw=1)); a.text(6,4.7,"metal gate",ha="center",va="center",fontsize=6.4)
for x,t in ((2.9,"S"),(9.1,"D"),(6,"G")):
    a.plot([x,x],[5.1 if t=="G" else 4.6,6.6],color=INK,lw=1.2); a.text(x,7.0,t,ha="center",fontsize=9)
a.plot([11,11.6,11.6],[2.8,2.8,6.0],color=INK,lw=1.0); a.text(11.6,6.5,"SS",ha="center",fontsize=8)
b=fig.add_axes([0.40,0.18,0.25,0.72]); v=np.linspace(-6,2,200); IDSS=8; VP=-4
b.plot(v[v>=VP],IDSS*(1-v[v>=VP]/VP)**2,color=INK,lw=1.4)
b.axvline(0,color="#aaa",lw=0.6); b.axvline(VP,color=ACCENT,lw=0.8,ls=":")
b.scatter([-4,0],[0,8],color=ACCENT,zorder=5,s=16); b.text(-3.9,0.8,"V$_P$",fontsize=7.4,color=ACCENT); b.text(0.15,7.0,"I$_{DSS}$",fontsize=7.4,color=ACCENT)
b.text(-5.9,13,"depletion mode",fontsize=6.6,color=MUTED); b.text(0.4,16,"enhancement mode",fontsize=6.6,color=MUTED)
b.set_xlim(-6,2); b.set_ylim(0,19); b.set_xlabel("V$_{GS}$ (V)",fontsize=8); b.set_ylabel("I$_D$ (mA)",fontsize=8); b.set_title("transfer curve",fontsize=8)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.74,0.18,0.25,0.72]); vds=np.linspace(0,14,300)
for vg in (1,0,-1,-2,-3):
    ids=IDSS*(1-vg/VP)**2; vk=vg-VP
    c.plot(vds,np.where(vds<vk,ids*(2*vds/vk-(vds/vk)**2),ids),color=INK,lw=1.0); c.text(14.1,ids,f"{vg:+d} V" if vg else "0 V",fontsize=6.6,va="center")
c.plot(np.linspace(0,5,50),[0]*50,alpha=0)
c.set_xlim(0,16.5); c.set_ylim(0,16); c.set_xlabel("V$_{DS}$ (V)",fontsize=8); c.set_ylabel("I$_D$ (mA)",fontsize=8); c.set_title("drain characteristics",fontsize=8)
for s in ("top","right"): c.spines[s].set_visible(False)
'''

F['emos_char'] = r'''
fig=plt.figure(figsize=(7.4,2.8))
a=fig.add_axes([0.0,0.02,0.32,0.95]); a.set_xlim(0,12); a.set_ylim(0,9); a.axis('off')
a.add_patch(Rectangle((1,1.0),10,3.6,fc="#efe9dc",ec=INK,lw=1.2)); a.text(6,1.8,"p-type substrate",ha="center",fontsize=7.4)
a.add_patch(Rectangle((1.8,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1)); a.add_patch(Rectangle((8.0,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1))
a.text(2.9,4.0,"n+",ha="center",va="center",fontsize=8); a.text(9.1,4.0,"n+",ha="center",va="center",fontsize=8)
a.add_patch(Rectangle((4.0,4.0),4.0,0.35,fc="#d9d9d9",ec=INK,lw=0.8)); a.text(8.3,4.17,"SiO$_2$",fontsize=6.2,va="center")
a.add_patch(Rectangle((4.2,4.35),3.6,0.7,fc="#b9b9b9",ec=INK,lw=1)); a.text(6,4.7,"metal gate",ha="center",va="center",fontsize=6.4)
a.add_patch(Rectangle((4.0,3.45),4.0,0.5,fc="#9fc4ee",ec=INK,lw=0.6,ls="--")); a.text(6,3.7,"induced n channel (V$_{GS}$ > V$_T$)",ha="center",va="center",fontsize=5.6)
for x,t in ((2.9,"S"),(9.1,"D"),(6,"G")):
    a.plot([x,x],[5.1 if t=="G" else 4.6,6.6],color=INK,lw=1.2); a.text(x,7.0,t,ha="center",fontsize=9)
b=fig.add_axes([0.40,0.18,0.25,0.72]); VT=2; k=0.5; v=np.linspace(0,7,200)
b.plot(v[v>=VT],k*(v[v>=VT]-VT)**2,color=INK,lw=1.4); b.plot([0,VT],[0,0],color=INK,lw=1.4)
b.scatter([VT],[0],color=ACCENT,zorder=5,s=16); b.text(VT,0.9,"V$_T$",fontsize=7.4,color=ACCENT,ha="center")
b.text(3.0,10.5,"I$_D$ = k(V$_{GS}$ − V$_T$)$^2$",fontsize=7.2)
b.set_xlabel("V$_{GS}$ (V)",fontsize=8); b.set_ylabel("I$_D$ (mA)",fontsize=8); b.set_title("transfer curve",fontsize=8); b.set_ylim(0,13)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.74,0.18,0.25,0.72]); vds=np.linspace(0,12,300)
for vg in (3,4,5,6):
    ids=k*(vg-VT)**2; vk=vg-VT
    c.plot(vds,np.where(vds<vk,ids*(2*vds/vk-(vds/vk)**2),ids),color=INK,lw=1.0); c.text(12.1,ids,f"{vg} V",fontsize=6.6,va="center")
c.plot([0,12],[0,0],color=MUTED,lw=0.6); c.text(5,0.3,"V$_{GS}$ ≤ V$_T$: cut-off",fontsize=6.4,color=MUTED)
c.set_xlim(0,14); c.set_ylim(0,9); c.set_xlabel("V$_{DS}$ (V)",fontsize=8); c.set_ylabel("I$_D$ (mA)",fontsize=8); c.set_title("drain characteristics",fontsize=8)
for s in ("top","right"): c.spines[s].set_visible(False)
'''

# ---------------------------------------------------------------- problem circuits (FET bias)
def _fet_prob(VDD, R1, R2, RD, RS, kind, extra=""):
    return f'''
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"{VDD}",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"{R1}",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"{R2}",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
{kind}
res(ax,(5.0,6.6),(5.0,4.9),"{RD}",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"{RS}",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
{extra}
'''
F['prob_dmos'] = _fet_prob("+16 V","2.1 MΩ","270 kΩ","2.4 kΩ","1.5 kΩ",
    'm=mosfet(ax,2.0,3.2,kind="n",mode="dep")\nwire(ax,[m["D"],(4.0,4.3)])\nwire(ax,[m["S"],(4.0,2.1)])',
    'label(ax,(-1.1,7.3),"V$_P$ = −4 V,  I$_{DSS}$ = 8 mA",ha="left",size=8)')
F['prob_emos'] = _fet_prob("+10 V","11 MΩ","11 MΩ","6 kΩ","6 kΩ",
    'm=mosfet(ax,2.0,3.2,kind="n",mode="enh")\nwire(ax,[m["D"],(4.0,4.3)])\nwire(ax,[m["S"],(4.0,2.1)])',
    'label(ax,(-1.1,7.3),"V$_t$ = 1 V,  K = 0.48 mA/V$^2$",ha="left",size=8)')
def _jfet(VDD,R1,R2,RD,RS,note):
    return _fet_prob(VDD,R1,R2,RD,RS,
     'wire(ax,[(2.0,3.2),(2.9,3.2)]); ax.plot([2.9,2.9],[2.2,4.2],color=INK,lw=2.4)\nwire(ax,[(2.9,4.2),(4.0,4.2),(4.0,4.4)]); wire(ax,[(2.9,2.2),(4.0,2.2),(4.0,2.0)])\nax.annotate("",xy=(3.0,3.2),xytext=(2.45,3.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3,mutation_scale=9))',
     f'label(ax,(-1.1,7.3),"{note}",ha="left",size=8)')
F['prob_jfet1'] = _jfet("+20 V","910 kΩ","110 kΩ","2.2 kΩ","1.1 kΩ","I$_{DSS}$ = 10 mA,  V$_P$ = −3.5 V")
F['prob_jfet2'] = _jfet("V$_{DD}$ = 20 V","1.5 MΩ","330 kΩ","2 kΩ","1 kΩ","V$_P$ = −5.5 V,  I$_{DSS}$ = 10 mA")

F['prob_ce'] = r'''
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.8),ylim=(-1.0,7.6))
terminal(ax,(2.6,7.2)); label(ax,(3.1,7.2),"+20 V",ha="left",size=8.6)
wire(ax,[(1.2,6.6),(4.6,6.6)]); wire(ax,[(2.6,6.6),(2.6,7.2)]); node(ax,(2.6,6.6))
res(ax,(1.2,6.6),(1.2,4.0),"470 kΩ",side=-1,off=0.9)
res(ax,(4.6,6.6),(4.6,4.4),"2.2 kΩ",side=1,off=0.5,body=0.9)
bj=bjt(ax,2.6,3.0)
wire(ax,[(1.2,4.0),(1.2,3.0),bj["B"]]); node(ax,(1.2,3.0))
wire(ax,[bj["C"],(4.6,4.1),(4.6,4.4)])
cap(ax,(4.6,4.1),(6.4,4.1),"C$_2$",side=1); terminal(ax,(6.9,4.1)); wire(ax,[(6.4,4.1),(6.9,4.1)]); label(ax,(7.3,4.1),"v$_o$",ha="left",size=8.6)
cap(ax,(-0.6,3.0),(0.4,3.0),"C$_1$",side=1,gap=0.2); wire(ax,[(0.4,3.0),(1.2,3.0)]); terminal(ax,(-1.0,3.0)); wire(ax,[(-1.0,3.0),(-0.6,3.0)]); label(ax,(-1.0,3.45),"v$_{in}$",size=8.6)
wire(ax,[bj["E"],(3.2,1.7),(3.2,1.6)]); res(ax,(3.2,1.7),(3.2,0.2),"560 Ω",side=1,off=0.55,body=0.9); gnd(ax,(3.2,0.2))
label(ax,(4.4,2.2),"β = 120\nr$_o$ = 40 kΩ",ha="left",size=8)
'''

# ---------------------------------------------------------------- oscillators
F['wien'] = r'''
fig,ax=ckt_canvas(5.8,3.6,xlim=(-0.6,8.8),ylim=(-0.5,6.2))
o=opamp(ax,3.0,3.6)
wire(ax,[o["inv"],(2.2,4.2)]); node(ax,(2.2,4.2)); wire(ax,[(2.2,4.2),(0.2,4.2)]); res(ax,(0.2,4.2),(0.2,0.0),"R$_1$",side=-1,off=0.55)
wire(ax,[(2.2,4.2),(2.2,5.4),(3.2,5.4)]); res(ax,(3.2,5.4),(5.0,5.4),"R$_f$",side=1,off=0.45); wire(ax,[(5.0,5.4),(6.4,5.4),(6.4,3.6)])
wire(ax,[o["out"],(7.6,3.6)]); node(ax,(6.4,3.6)); terminal(ax,(7.6,3.6)); label(ax,(8.0,3.6),"v$_o$",ha="left",size=9)
wire(ax,[(6.4,3.6),(6.4,1.9)]); res(ax,(6.4,1.9),(4.8,1.9),"R",side=1,off=0.45,body=0.9); cap(ax,(4.8,1.9),(3.4,1.9),"C",side=1)
wire(ax,[(3.4,1.9),(2.2,1.9)]); node(ax,(2.2,1.9)); wire(ax,[(2.2,1.9),(2.2,3.0),o["non"]])
wire(ax,[(2.2,1.9),(1.2,1.9)]); res(ax,(2.2,1.9),(2.2,0.0),"R",side=-1,off=0.5,body=0.9); cap(ax,(1.2,1.9),(1.2,0.0),"C",side=1)
wire(ax,[(0.2,0.0),(2.2,0.0)]); node(ax,(1.2,0.0)); gnd(ax,(1.2,0.0))
label(ax,(4.2,2.55),"series R–C",size=7.4); label(ax,(1.7,0.95),"parallel\nR–C",size=7,ha="right")
'''


from figs2 import F2
F.update(F2)

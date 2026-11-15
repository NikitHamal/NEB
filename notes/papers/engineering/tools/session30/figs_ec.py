F = {}

F['q4ce'] = r'''fig,ax=ckt_canvas(5.6,4.0,xlim=(-2.0,10.0),ylim=(-0.9,8.2))
wire(ax,[(2.6,7.0),(6.2,7.0)]); terminal(ax,(6.2,7.0)); label(ax,(6.7,7.0),"V$_{CC}$ = +10 V",ha="left",size=8)
res(ax,(2.6,7.0),(2.6,4.8),"R$_1$ = 10 kΩ",side=-1,off=0.2); label(ax,(1.0,5.9),"",size=1)
wire(ax,[(2.6,4.8),(2.6,3.8)]); node(ax,(2.6,3.8)); wire(ax,[(2.6,3.8),(3.5,3.8)])
wire(ax,[(2.6,3.8),(2.6,2.8)]); res(ax,(2.6,2.8),(2.6,0.9),"R$_2$ = 10 kΩ",side=-1,off=0.2); gnd(ax,(2.6,0.9))
bj=bjt(ax,4.2,3.8)
wire(ax,[(4.8,7.0),(4.8,6.6)]); node(ax,(4.8,7.0)); res(ax,(4.8,7.0),(4.8,5.4),"R$_C$ = 2 kΩ",side=1,off=0.15); wire(ax,[(4.8,5.4),(4.8,4.9)])
node(ax,(4.8,5.15)); wire(ax,[(4.8,5.15),(6.0,5.15)]); cap(ax,(6.0,5.15),(6.8,5.15)); wire(ax,[(6.8,5.15),(8.4,5.15)]); node(ax,(8.4,5.15)); terminal(ax,(8.4,5.15))
wire(ax,[(8.4,5.15),(8.4,4.6)]); res(ax,(8.4,5.15),(8.4,3.1),"R$_L$ = 10 kΩ",side=1,off=0.15); gnd(ax,(8.4,3.1))
wire(ax,[(4.8,2.7),(4.8,2.3)]); node(ax,(4.8,2.3)); res(ax,(4.8,2.3),(4.8,0.9),"R$_E$ = 4.3 kΩ",side=1,off=0.15,body=0.8); gnd(ax,(4.8,0.9))
wire(ax,[(4.8,2.3),(7.6,2.3)]); cap(ax,(7.6,2.3),(7.6,0.9)); wire(ax,[(7.6,0.9),(4.8,0.9)])
label(ax,(8.1,1.6),"C$_E$",ha="left",size=8)
wire(ax,[(2.6,3.8),(1.9,3.8)]); cap(ax,(1.9,3.8),(1.1,3.8)); wire(ax,[(1.1,3.8),(0.4,3.8)]); res(ax,(0.4,3.8),(-1.2,3.8),"R$_s$ = 600 Ω",side=1,off=0.5)
wire(ax,[(-1.2,3.8),(-1.6,3.8),(-1.6,3.0)]); acsrc(ax,(-1.6,1.6),(-1.6,3.0),"v$_s$",side=-1,off=0.6); gnd(ax,(-1.6,1.6))
'''

F['q6mos'] = r'''fig,ax=ckt_canvas(4.4,3.9,xlim=(-1.2,7.0),ylim=(-0.8,8.0))
wire(ax,[(1.2,7.0),(5.2,7.0)]); terminal(ax,(5.2,7.0)); label(ax,(5.6,7.0),"+V$_{DD}$",ha="left",size=8.2)
res(ax,(1.2,7.0),(1.2,4.7),"R$_1$",side=-1,off=0.2); wire(ax,[(1.2,4.7),(1.2,3.5)]); node(ax,(1.2,3.5)); wire(ax,[(1.2,3.5),(2.3,3.5)])
wire(ax,[(1.2,3.5),(1.2,2.6)]); res(ax,(1.2,2.6),(1.2,0.7),"R$_2$",side=-1,off=0.2); gnd(ax,(1.2,0.7))
m=mosfet(ax,3.0,3.5,"n","enh")
wire(ax,[(4.0,7.0),(4.0,6.6)]); node(ax,(4.0,7.0)); res(ax,(4.0,7.0),(4.0,5.4),"R$_D$",side=1,off=0.2); wire(ax,[(4.0,5.4),(4.0,4.6)])
wire(ax,[(4.0,2.4),(4.0,2.0)]); res(ax,(4.0,2.0),(4.0,0.7),"R$_S$",side=1,off=0.2,body=0.8); gnd(ax,(4.0,0.7))
label(ax,(-0.5,7.5),"%s",ha="left",size=7.6)
'''

F['diodemodels'] = r'''fig,axs=plt.subplots(1,4,figsize=(7.6,2.3))
v=np.linspace(-0.3,1.0,400)
def real(v): return 1e-3*(np.exp((v-0.62)/0.052)-1)
for a,t in zip(axs,["(a) real diode","(b) ideal model","(c) constant-drop model","(d) piece-wise linear model"]):
    a.axhline(0,color=MUTED,lw=0.6); a.axvline(0,color=MUTED,lw=0.6); a.set_title(t,fontsize=7.2)
    a.set_xlim(-0.3,1.0); a.set_ylim(-0.1,1.1); a.set_xticks([]); a.set_yticks([])
    a.set_xlabel("v$_D$",fontsize=7.4); a.set_ylabel("i$_D$",fontsize=7.4)
    for s in ("top","right"): a.spines[s].set_visible(False)
axs[0].plot(v,np.clip(real(v),-0.1,1.1),color=INK,lw=1.4)
axs[1].plot([-0.3,0],[0,0],color=INK,lw=1.5); axs[1].plot([0,0],[0,1.0],color=INK,lw=1.5)
axs[2].plot([-0.3,0.7],[0,0],color=INK,lw=1.5); axs[2].plot([0.7,0.7],[0,1.0],color=INK,lw=1.5); axs[2].text(0.70,-0.07,"V$_D$ = 0.7 V",fontsize=6.4,ha="center")
axs[3].plot([-0.3,0.55],[0,0],color=INK,lw=1.5); axs[3].plot([0.55,0.9],[0,1.0],color=INK,lw=1.5); axs[3].text(0.55,-0.07,"V$_γ$",fontsize=6.8,ha="center"); axs[3].text(0.62,0.62,"slope = 1/r$_d$",fontsize=6.2,color=ACCENT)
axs[3].plot(v,np.clip(real(v),-0.1,1.1),color=MUTED,lw=0.9,ls="--")
fig.tight_layout()
'''

F['led'] = r'''fig=plt.figure(figsize=(7.2,2.6))
ax=fig.add_axes([0.0,0.0,0.52,1.0]); ax.set_xlim(-0.6,8.4); ax.set_ylim(-0.6,4.6); ax.set_aspect('equal'); ax.axis('off')
wire(ax,[(1.0,0.2),(1.0,0.8)]); batt(ax,(1.0,0.2),(1.0,3.0),"V$_S$",side=-1,off=0.7)
wire(ax,[(1.0,3.0),(1.0,4.0),(3.0,4.0)]); res(ax,(3.0,4.0),(5.0,4.0),"R$_S$",side=1,off=0.45)
wire(ax,[(5.0,4.0),(6.4,4.0),(6.4,3.3)]); diode(ax,(6.4,3.3),(6.4,1.1),"LED",side=1,off=0.9,body=0.7)
wire(ax,[(6.4,1.1),(6.4,0.2),(1.0,0.2)])
for dx in (0.0,0.45):
    ax.annotate("",xy=(7.7+dx*0.6,2.9+dx),xytext=(7.0+dx*0.6,2.2+dx),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.4,mutation_scale=9))
label(ax,(7.9,1.8),"light",ha="left",size=7.6,color=ACCENT)
b=fig.add_axes([0.60,0.2,0.38,0.7]); b.set_xlim(0,10); b.set_ylim(0,6); b.axis('off')
b.add_patch(Rectangle((0.5,0.8),3.6,3.6,fc="#cfe0f5",ec=INK,lw=1)); b.add_patch(Rectangle((5.9,0.8),3.6,3.6,fc="#f5d9d4",ec=INK,lw=1))
b.text(2.3,2.6,"n-region\n(electrons)",ha="center",va="center",fontsize=7); b.text(7.7,2.6,"p-region\n(holes)",ha="center",va="center",fontsize=7)
b.annotate("",xy=(5.9,3.3),xytext=(4.1,3.3),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2)); b.annotate("",xy=(4.1,1.8),xytext=(5.9,1.8),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2))
b.text(5.0,2.55,"recombination\n→ photon hν",ha="center",va="center",fontsize=6.4,color=ACCENT)
b.text(2.3,5.1,"n (cathode, −)",ha="center",fontsize=7.4); b.text(7.7,5.1,"p (anode, +)",ha="center",fontsize=7.4)
'''

F['ctfw'] = r'''fig=plt.figure(figsize=(7.4,2.9))
ax=fig.add_axes([0.0,0.0,0.56,1.0]); ax.set_xlim(-1.2,11.2); ax.set_ylim(-1.2,6.2); ax.set_aspect('equal'); ax.axis('off')
t=transformer(ax,1.0,0.6,w=1.8,h=3.4,turns=7)
acsrc(ax,(-0.6,1.2),(-0.6,3.2),"v$_i$",side=-1,off=0.6)
wire(ax,[(-0.6,3.2),(-0.6,t["p_top"][1]),t["p_top"]]); wire(ax,[(-0.6,1.2),(-0.6,t["p_bot"][1]),t["p_bot"]])
yt=t["s_top"][1]; yb=t["s_bot"][1]; ym=(yt+yb)/2; x0=t["s_top"][0]
diode(ax,(x0,yt),(x0+3.0,yt),"D$_1$",side=1,off=0.5); diode(ax,(x0,yb),(x0+3.0,yb),"D$_2$",side=-1,off=0.5)
xb=x0+4.0; wire(ax,[(x0+3.0,yt),(xb,yt),(xb,yb),(x0+3.0,yb)]); node(ax,(xb,ym))
wire(ax,[(xb,ym),(xb+1.6,ym)]); res(ax,(xb+1.6,ym),(xb+1.6,ym-2.2),"R$_L$",side=1,off=0.45); gnd(ax,(xb+1.6,ym-2.2))
wire(ax,[(x0,ym),(x0+0.5,ym)]); gnd(ax,(x0+0.5,ym)); label(ax,(x0+0.6,ym+0.4),"CT",size=7.4,ha="center")
b=fig.add_axes([0.66,0.55,0.32,0.38]); x=np.linspace(0,4*np.pi,400); b.plot(x,np.sin(x),color=INK,lw=1.2); b.set_xticks([]); b.set_yticks([]); b.set_title("secondary half v$_s$ (each half)",fontsize=7); b.axhline(0,color=MUTED,lw=0.6)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.66,0.08,0.32,0.38]); c.plot(x,np.abs(np.sin(x)),color=ACCENT,lw=1.4); c.set_xticks([]); c.set_yticks([]); c.set_title("load voltage v$_L$ (D$_1$, D$_2$ alternately)",fontsize=7)
for s in ("top","right"): c.spines[s].set_visible(False)
'''

F['bridge'] = r'''fig=plt.figure(figsize=(7.4,2.9))
ax=fig.add_axes([0.0,0.0,0.58,1.0]); ax.set_xlim(-2.2,11.4); ax.set_ylim(-1.8,5.4); ax.set_aspect('equal'); ax.axis('off')
L=(3.0,2.5);T=(5.0,4.5);R=(7.0,2.5);B=(5.0,0.5)
diode(ax,L,T,"D$_1$",side=-1,off=0.45); diode(ax,R,T,"D$_2$",side=1,off=0.45); diode(ax,B,L,"D$_3$",side=-1,off=0.45); diode(ax,B,R,"D$_4$",side=1,off=0.45)
node(ax,L); node(ax,R); node(ax,T); node(ax,B)
wire(ax,[(-0.6,1.6),(-0.6,3.0)]); acsrc(ax,(-0.6,1.0),(-0.6,2.5),"v$_i$",side=-1,off=0.6)
wire(ax,[(-0.6,2.5),L]); wire(ax,[(-0.6,1.0),(-0.6,-1.2),(8.2,-1.2),(8.2,2.5),R])
wire(ax,[T,(5.0,4.9),(9.4,4.9)]); wire(ax,[(9.4,4.9),(9.4,4.2)]); res(ax,(9.4,4.2),(9.4,1.2),"R$_L$",side=1,off=0.45); gnd(ax,(9.4,1.2))
wire(ax,[B,(5.0,-0.2)]); gnd(ax,(5.0,-0.2)); label(ax,(5.0,5.25),"+",size=9); label(ax,(5.6,0.0),"−",size=9,ha="left")
b=fig.add_axes([0.68,0.55,0.30,0.36]); x=np.linspace(0,4*np.pi,400); b.plot(x,np.sin(x),color=INK,lw=1.2); b.set_xticks([]); b.set_yticks([]); b.set_title("input v$_i$",fontsize=7); b.axhline(0,color=MUTED,lw=0.6)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.68,0.08,0.30,0.36]); c.plot(x,np.abs(np.sin(x)),color=ACCENT,lw=1.4); c.set_xticks([]); c.set_yticks([]); c.set_title("output v$_L$ (D$_1$D$_4$ then D$_2$D$_3$)",fontsize=7)
for s in ("top","right"): c.spines[s].set_visible(False)
'''

F['npn'] = r'''fig=plt.figure(figsize=(7.0,2.7))
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,14); ax.set_ylim(0,5.4); ax.axis('off')
ax.add_patch(Rectangle((1.2,1.5),3.4,2.2,fc="#cfe0f5",ec=INK,lw=1.2)); ax.add_patch(Rectangle((4.6,1.5),1.4,2.2,fc="#f5d9d4",ec=INK,lw=1.2)); ax.add_patch(Rectangle((6.0,1.5),3.4,2.2,fc="#cfe0f5",ec=INK,lw=1.2))
ax.text(2.9,2.6,"n  emitter\n(heavily doped)",ha="center",va="center",fontsize=7.4); ax.text(5.3,2.6,"p\nbase",ha="center",va="center",fontsize=7.4); ax.text(7.7,2.6,"n  collector",ha="center",va="center",fontsize=7.4)
ax.add_patch(Rectangle((4.6,1.5),0.0,2.2,fc="none")); ax.text(4.6,3.95,"E–B junction\nforward biased",ha="center",fontsize=6.6); ax.text(6.0,3.95,"C–B junction\nreverse biased",ha="center",fontsize=6.6)
ax.annotate("",xy=(5.0,2.9),xytext=(3.6,2.9),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6)); ax.annotate("",xy=(8.2,2.9),xytext=(5.6,2.9),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6))
ax.text(5.5,3.15,"I$_{nE}$ electrons",fontsize=6.4,color=ACCENT,ha="center")
ax.annotate("",xy=(4.8,1.3),xytext=(5.3,0.4),arrowprops=dict(arrowstyle="<|-",color=INK,lw=1.2)); ax.text(5.5,0.3,"I$_B$ (recombination + hole injection)",fontsize=6.6,va="center")
ax.plot([1.2,1.2,0.6],[2.6,2.6,2.6],color=INK); ax.text(0.4,2.6,"E",fontsize=9,ha="right",va="center"); ax.plot([9.4,10.0],[2.6,2.6],color=INK); ax.text(10.1,2.6,"C",fontsize=9,va="center")
ax.plot([5.3,5.3],[1.5,1.0],color=INK); ax.text(5.3,0.85,"",fontsize=1)
ax.text(11.3,4.6,"V$_{EB}$ ≈ +0.7 V forward",fontsize=7,ha="left"); ax.text(11.3,3.9,"V$_{CB}$ > 0 reverse",fontsize=7,ha="left")
ax.text(11.3,2.8,"I$_E$ = I$_B$ + I$_C$",fontsize=8,ha="left",color=ACCENT)
ax.text(11.3,2.0,"I$_C$ = αI$_E$ + I$_{CBO}$",fontsize=8,ha="left")
'''

F['depmos'] = r'''fig=plt.figure(figsize=(7.4,2.8))
a=fig.add_axes([0.0,0.02,0.32,0.95]); a.set_xlim(0,12); a.set_ylim(0,9); a.axis('off')
a.add_patch(Rectangle((1,1.0),10,3.6,fc="#efe9dc",ec=INK,lw=1.2)); a.text(6,1.8,"p-type substrate",ha="center",fontsize=7.4)
a.add_patch(Rectangle((1.8,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1)); a.add_patch(Rectangle((8.0,3.4),2.2,1.2,fc="#cfe0f5",ec=INK,lw=1))
a.text(2.9,4.0,"n+",ha="center",va="center",fontsize=8); a.text(9.1,4.0,"n+",ha="center",va="center",fontsize=8)
a.add_patch(Rectangle((4.0,3.4),4.0,1.2,fc="#9fc4ee",ec=INK,lw=0.6)); a.text(6,3.1,"built-in n channel",ha="center",va="center",fontsize=6.0)
a.add_patch(Rectangle((4.0,4.6),4.0,0.35,fc="#d9d9d9",ec=INK,lw=0.8)); a.text(8.3,4.78,"SiO$_2$",fontsize=6.2,va="center")
a.add_patch(Rectangle((4.2,4.95),3.6,0.7,fc="#b9b9b9",ec=INK,lw=1)); a.text(6,5.3,"metal gate",ha="center",va="center",fontsize=6.4)
for x,t in ((2.9,"S"),(9.1,"D"),(6,"G")):
    a.plot([x,x],[5.7 if t=="G" else 4.6,7.2],color=INK,lw=1.2); a.text(x,7.6,t,ha="center",fontsize=9)
b=fig.add_axes([0.40,0.18,0.25,0.72]); v=np.linspace(-5,2.0,200); b.plot(v,10*(1-v/(-4))**2*(v>=-4),color=INK,lw=1.4)
b.scatter([-4,0],[0,10],color=ACCENT,s=16,zorder=5); b.text(-3.9,0.8,"V$_P$",fontsize=7.4,color=ACCENT); b.text(0.1,8.6,"I$_{DSS}$",fontsize=7.4,color=ACCENT)
b.text(-4.6,12.6,"I$_D$ = I$_{DSS}$(1 − V$_{GS}$/V$_P$)$^2$",fontsize=6.8); b.axvline(0,color=MUTED,lw=0.6)
b.set_xlabel("V$_{GS}$ (V)",fontsize=8); b.set_ylabel("I$_D$ (mA)",fontsize=8); b.set_title("transfer curve",fontsize=8); b.set_ylim(0,15)
for s in ("top","right"): b.spines[s].set_visible(False)
c=fig.add_axes([0.74,0.18,0.25,0.72]); vds=np.linspace(0,12,300)
for vg,col in ((1,ACCENT),(0,INK),(-1,INK),(-2,INK),(-3,INK)):
    ids=10*(1+vg/4)**2; vk=vg+4
    c.plot(vds,np.where(vds<vk,ids*(2*vds/vk-(vds/vk)**2),ids),color=col,lw=1.0); c.text(12.1,ids,f"{vg} V",fontsize=6.4,va="center")
c.set_xlim(0,14); c.set_ylim(0,17); c.set_xlabel("V$_{DS}$ (V)",fontsize=8); c.set_ylabel("I$_D$ (mA)",fontsize=8); c.set_title("drain characteristics",fontsize=8)
c.text(5,15.6,"V$_{GS}$ > 0: enhancement mode",fontsize=6.0,color=ACCENT)
for s in ("top","right"): c.spines[s].set_visible(False)
'''

F['summer'] = r'''fig,ax=ckt_canvas(6.4,3.4,xlim=(-1.2,16.0),ylim=(-1.2,6.6))
# stage 1
o1=opamp(ax,3.6,3.6,2.2,2.0,"A$_1$")
for (y,t,lab) in ((5.4,"5 kΩ","V$_1$"),(4.6,"2 kΩ","V$_3$")):
    pass
wire(ax,[(-0.6,5.3),(0.6,5.3)]); terminal(ax,(-0.6,5.3)); label(ax,(-0.9,5.3),"V$_1$",ha="right",size=8.4)
res(ax,(0.6,5.3),(2.0,5.3),"5 kΩ",side=1,off=0.4,body=1.0)
wire(ax,[(-0.6,4.3),(0.6,4.3)]); terminal(ax,(-0.6,4.3)); label(ax,(-0.9,4.3),"V$_3$",ha="right",size=8.4)
res(ax,(0.6,4.3),(2.0,4.3),"2 kΩ",side=-1,off=0.4,body=1.0)
wire(ax,[(2.0,5.3),(2.6,5.3),(2.6,4.1)]); wire(ax,[(2.0,4.3),(2.6,4.3)]); node(ax,(2.6,4.3)); wire(ax,[(2.6,4.1),(3.6,4.1)])
wire(ax,[(3.6,3.1),(3.0,3.1),(3.0,2.2)]); gnd(ax,(3.0,2.2))
wire(ax,[(2.6,4.1),(2.6,6.0),(6.2,6.0),(6.2,3.6)]); res(ax,(2.6,6.0),(6.2,6.0),"R$_f$ = 10 kΩ",side=1,off=0.4,body=1.4) if False else None
wire(ax,[(2.6,4.3),(2.6,6.0),(3.4,6.0)]); res(ax,(3.4,6.0),(5.2,6.0),"R$_f$ = 10 kΩ",side=1,off=0.4,body=1.2); wire(ax,[(5.2,6.0),(6.2,6.0),(6.2,3.6)]); node(ax,(5.8,3.6))
wire(ax,[(5.8,3.6),(6.2,3.6)]); label(ax,(6.7,3.2),"V$_a$ = −(2V$_1$+5V$_3$)",ha="left",size=7.4)
# stage 2
wire(ax,[(6.2,3.6),(7.4,3.6)]); res(ax,(7.4,3.6),(8.8,3.6),"10 kΩ",side=1,off=0.4,body=1.0)
wire(ax,[(8.8,3.6),(9.6,3.6),(9.6,3.4)])
wire(ax,[(7.4,1.6),(8.2,1.6)]); terminal(ax,(7.4,1.6)); label(ax,(7.1,1.6),"V$_2$",ha="right",size=8.4)
res(ax,(8.2,1.6),(9.2,1.6),"",side=1,off=0.3,body=0.6) if False else None
wire(ax,[(7.4,1.6),(7.6,1.6)]); res(ax,(7.6,1.6),(9.0,1.6),"2.5 kΩ",side=-1,off=0.4,body=1.0); wire(ax,[(9.0,1.6),(9.6,1.6),(9.6,3.4)]); node(ax,(9.6,3.4))
o2=opamp(ax,9.6,3.0,2.2,2.0,"A$_2$")
wire(ax,[(9.6,3.4),(9.6,3.6+0.0)])
wire(ax,[(9.6,2.5),(9.0,2.5),(9.0,1.2)]) if False else None
wire(ax,[o2["non"],(9.2,o2["non"][1]),(9.2,0.2)]); gnd(ax,(9.2,0.2))
wire(ax,[o2["inv"],(9.2+0.0,o2["inv"][1])]) if False else None
wire(ax,[(9.6,3.4),(9.6,4.0)]) if False else None
wire(ax,[(9.6,3.6),(9.6,3.4)])
wire(ax,[(9.6,3.4),(9.6,6.0),(10.3,6.0)]) if False else None
wire(ax,[(9.6,3.6),(9.6,6.0),(10.2,6.0)]); res(ax,(10.2,6.0),(12.2,6.0),"R$_f$ = 10 kΩ",side=1,off=0.4,body=1.2); wire(ax,[(12.2,6.0),(12.8,6.0),(12.8,3.0)])
wire(ax,[o2["out"],(12.8,3.0)]); node(ax,(12.8,3.0)); wire(ax,[(12.8,3.0),(13.8,3.0)]); terminal(ax,(13.8,3.0)); label(ax,(14.1,3.0),"V$_o$",ha="left",size=8.4)
label(ax,(11.0,0.4),"V$_o$ = −(V$_a$ + 4V$_2$) = 2V$_1$ − 4V$_2$ + 5V$_3$",ha="center",size=7.6)
'''

F['wien'] = r'''fig,ax=ckt_canvas(5.6,3.7,xlim=(-1.0,11.2),ylim=(-0.8,7.6))
o=opamp(ax,4.0,4.6,2.4,2.4,"")
out=o["out"]; wire(ax,[out,(8.6,out[1])]); node(ax,(7.6,out[1])); terminal(ax,(8.6,out[1])); label(ax,(8.9,out[1]),"v$_o$",ha="left",size=8.4)
# feedback R1 and R2 on inverting side
inv=o["inv"]; wire(ax,[inv,(3.0,inv[1]),(3.0,6.6)]); node(ax,(3.0,inv[1]))
res(ax,(3.0,6.6),(3.0,5.9),"",side=1) if False else None
wire(ax,[(3.0,inv[1]),(3.0,6.8),(7.6,6.8),(7.6,out[1])]); res(ax,(3.4,6.8),(5.8,6.8),"R$_f$",side=1,off=0.35,body=1.2)
wire(ax,[(3.0,inv[1]),(3.0,3.4)]); res(ax,(3.0,5.4),(3.0,3.2),"R$_1$",side=-1,off=0.35,body=0.9) if False else None
wire(ax,[(3.0,inv[1]),(3.0,5.0)]); res(ax,(3.0,5.0),(3.0,3.0),"R$_1$",side=-1,off=0.35,body=1.0); gnd(ax,(3.0,3.0))
# positive feedback: series RC from output to non-inverting, parallel RC to ground
non=o["non"]; wire(ax,[non,(2.0,non[1])]); node(ax,(2.0,non[1]))
wire(ax,[(7.6,out[1]),(7.6,0.4),(-0.4,0.4),(-0.4,non[1]+0.0)]) if False else None
wire(ax,[(7.6,out[1]),(7.6,0.2),(0.2,0.2)]); res(ax,(0.2,0.2),(0.2,0.2),"") if False else None
res(ax,(7.6,0.2),(5.6,0.2),"R",side=-1,off=0.35,body=1.0) if False else None
wire(ax,[(7.6,0.2),(6.0,0.2)]); res(ax,(6.0,0.2),(4.4,0.2),"R",side=1,off=0.4,body=1.0); wire(ax,[(4.4,0.2),(3.8,0.2)]); cap(ax,(3.8,0.2),(3.0,0.2),"C",side=1,off=0.5)
wire(ax,[(3.0,0.2),(2.0,0.2),(2.0,non[1])]) if False else None
wire(ax,[(3.0,0.2),(2.0,0.2),(2.0,3.4)]); res(ax,(2.0,3.4),(2.0,1.6),"") if False else None
wire(ax,[(2.0,0.2),(2.0,1.0)]); node(ax,(2.0,0.2)) if False else None
label(ax,(5.4,0.8),"series R–C",size=7,color=MUTED)
wire(ax,[(2.0,non[1]),(2.0,2.2)]); res(ax,(2.0,2.2),(2.0,0.9),"",side=1) if False else None
'''

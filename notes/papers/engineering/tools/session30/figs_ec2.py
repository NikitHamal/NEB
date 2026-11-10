exec(open('/app/shots/figs_ec.py').read())

F['summer'] = r'''fig,ax=ckt_canvas(7.0,2.7,xlim=(-1.8,14.4),ylim=(0.6,6.4))
o1=opamp(ax,3.4,3.0,2.2,2.0,"A$_1$")
terminal(ax,(-0.5,4.6)); label(ax,(-0.8,4.6),"V$_1$",ha="right",size=8.4); wire(ax,[(-0.5,4.6),(0.4,4.6)]); res(ax,(0.4,4.6),(1.8,4.6),"5 kΩ",side=1,off=0.35)
terminal(ax,(-0.5,3.5)); label(ax,(-0.8,3.5),"V$_3$",ha="right",size=8.4); wire(ax,[(-0.5,3.5),(0.4,3.5)]); res(ax,(0.4,3.5),(1.8,3.5),"2 kΩ",side=-1,off=0.35)
wire(ax,[(1.8,4.6),(2.6,4.6),(2.6,3.5)]); wire(ax,[(1.8,3.5),(3.4,3.5)]); node(ax,(2.6,3.5))
wire(ax,[(2.6,4.6),(2.6,5.6),(3.2,5.6)]); res(ax,(3.2,5.6),(5.0,5.6),"10 kΩ",side=1,off=0.35); wire(ax,[(5.0,5.6),(6.2,5.6),(6.2,3.0)])
wire(ax,[(3.4,2.5),(3.0,2.5),(3.0,1.6)]); gnd(ax,(3.0,1.6))
wire(ax,[o1["out"],(6.2,3.0)]); node(ax,(6.2,3.0)); wire(ax,[(6.2,3.0),(6.8,3.0),(6.8,3.5)]); label(ax,(5.9,2.45),"V$_a$",size=8,ha="center")
res(ax,(6.8,3.5),(8.0,3.5),"10 kΩ",side=1,off=0.35,body=0.9); wire(ax,[(8.0,3.5),(9.4,3.5)]); node(ax,(8.6,3.5))
terminal(ax,(6.0,2.2)); label(ax,(5.7,2.2),"V$_2$",ha="right",size=8.4) if False else None
wire(ax,[(6.0,2.2),(6.8,2.2)]); res(ax,(6.8,2.2),(8.0,2.2),"2.5 kΩ",side=-1,off=0.35,body=0.9); wire(ax,[(8.0,2.2),(8.6,2.2),(8.6,3.5)])
label(ax,(6.0,1.8),"V$_2$",size=8.4)
wire(ax,[(8.6,3.5),(8.6,5.6),(9.2,5.6)]); res(ax,(9.2,5.6),(11.0,5.6),"10 kΩ",side=1,off=0.35); wire(ax,[(11.0,5.6),(12.2,5.6),(12.2,3.0)])
o2=opamp(ax,9.4,3.0,2.2,2.0,"A$_2$")
wire(ax,[(9.4,2.5),(9.0,2.5),(9.0,1.6)]); gnd(ax,(9.0,1.6))
wire(ax,[o2["out"],(12.2,3.0)]); node(ax,(12.2,3.0)); wire(ax,[(12.2,3.0),(13.2,3.0)]); terminal(ax,(13.2,3.0)); label(ax,(13.5,3.0),"V$_o$",ha="left",size=8.4)
'''

F['wien'] = r'''fig,ax=ckt_canvas(5.4,3.6,xlim=(-2.2,9.4),ylim=(0.3,6.2))
o=opamp(ax,4.0,3.6,2.4,2.4,"")
out=o["out"]; inv=o["inv"]; non=o["non"]
wire(ax,[out,(7.2,out[1])]); node(ax,(7.2,out[1])); wire(ax,[(7.2,out[1]),(8.2,out[1])]); terminal(ax,(8.2,out[1])); label(ax,(8.5,out[1]),"v$_o$",ha="left",size=8.4)
wire(ax,[inv,(2.8,inv[1])]); node(ax,(2.8,inv[1]))
wire(ax,[(7.2,out[1]),(7.2,5.4),(6.4,5.4)]); res(ax,(6.4,5.4),(4.2,5.4),"R$_f$",side=1,off=0.35,body=1.2); wire(ax,[(4.2,5.4),(2.8,5.4),(2.8,inv[1])])
wire(ax,[(2.8,inv[1]),(1.8,inv[1])]); res(ax,(1.8,inv[1]),(0.4,inv[1]),"R$_1$",side=1,off=0.35,body=0.9); gnd(ax,(0.4,inv[1]))
wire(ax,[non,(2.0,non[1])]); node(ax,(2.0,non[1]))
wire(ax,[(7.2,out[1]),(7.2,1.0),(6.4,1.0)]); res(ax,(6.4,1.0),(4.9,1.0),"R",side=1,off=0.35,body=1.0); wire(ax,[(4.9,1.0),(4.4,1.0)]); cap(ax,(4.4,1.0),(3.4,1.0),"C",side=1,off=0.5); wire(ax,[(3.4,1.0),(2.0,1.0),(2.0,non[1])])
wire(ax,[(2.0,non[1]),(0.6,non[1])]); node(ax,(0.6,non[1])); res(ax,(0.6,non[1]),(0.6,1.5),"R",side=-1,off=0.3,body=0.8); gnd(ax,(0.6,1.5))
wire(ax,[(0.6,non[1]),(-0.8,non[1])]); cap(ax,(-0.8,non[1]),(-0.8,1.5),"C",side=-1,off=0.5); gnd(ax,(-0.8,1.5))
label(ax,(5.6,0.55),"series R–C branch (Z$_s$)",size=7,color=MUTED); label(ax,(-0.1,0.9),"parallel R–C (Z$_p$)",size=7,color=MUTED,ha="center") if False else None
'''

F['classA_series'] = r'''fig=plt.figure(figsize=(7.2,2.9))
ax=fig.add_axes([0.0,0.0,0.46,1.0]); ax.set_xlim(-1.2,6.2); ax.set_ylim(-0.4,7.8); ax.set_aspect('equal'); ax.axis('off')
wire(ax,[(1.6,7.0),(3.8,7.0)]); terminal(ax,(5.0,7.0)); wire(ax,[(3.8,7.0),(5.0,7.0)]); label(ax,(5.0,7.45),"+V$_{CC}$",size=8)
res(ax,(1.6,7.0),(1.6,4.6),"R$_B$",side=-1,off=0.2); wire(ax,[(1.6,4.6),(1.6,3.8)]); node(ax,(1.6,3.8))
bj=bjt(ax,3.2,3.8); wire(ax,[(1.6,3.8),bj["B"]])
res(ax,(3.8,7.0),(3.8,5.4),"R$_L$ (load)",side=1,off=0.2); wire(ax,[(3.8,5.4),bj["C"]])
wire(ax,[bj["E"],(3.8,1.6)]); gnd(ax,(3.8,1.6))
wire(ax,[(1.6,3.8),(0.9,3.8)]); cap(ax,(0.9,3.8),(0.1,3.8)); wire(ax,[(0.1,3.8),(-0.5,3.8)]); terminal(ax,(-0.5,3.8)); label(ax,(-0.5,4.3),"v$_i$",size=8.4)
b=fig.add_axes([0.56,0.22,0.41,0.70]); vcc=1.0
b.plot([0,2*vcc],[2*0.5*1.0*1.0,0],color=INK,lw=1.4) if False else None
b.plot([0,vcc],[1.0,0],color=INK,lw=1.6); b.scatter([vcc/2],[0.5],color=ACCENT,zorder=5,s=22)
b.text(vcc/2+0.04,0.56,"Q",color=ACCENT,fontsize=8); b.plot([vcc/2,vcc/2],[0,0.5],color=ACCENT,lw=0.8,ls=":"); b.plot([0,vcc/2],[0.5,0.5],color=ACCENT,lw=0.8,ls=":")
b.set_xticks([0,vcc/2,vcc]); b.set_xticklabels(["0","V$_{CC}$/2","V$_{CC}$"],fontsize=8); b.set_yticks([0,0.5,1.0]); b.set_yticklabels(["0","I$_{CQ}$ = V$_{CC}$/2R$_L$","V$_{CC}$/R$_L$"],fontsize=7)
b.set_xlabel("v$_{CE}$",fontsize=8); b.set_ylabel("i$_C$",fontsize=8); b.set_title("d.c. = a.c. load line, Q at the centre",fontsize=7.6); b.set_xlim(0,1.08); b.set_ylim(0,1.12)
for s in ("top","right"): b.spines[s].set_visible(False)
'''

F['classA_tc'] = r'''fig=plt.figure(figsize=(7.4,2.9))
ax=fig.add_axes([0.0,0.0,0.52,1.0]); ax.set_xlim(-0.8,9.4); ax.set_ylim(-0.4,6.8); ax.set_aspect('equal'); ax.axis('off')
t=transformer(ax,5.4,2.4,w=1.6,h=3.0,turns=6)
bj=bjt(ax,3.8,1.7)
wire(ax,[bj["C"],(4.4,2.8),(t["p_bot"][0],t["p_bot"][1])]) if False else None
wire(ax,[bj["C"],(bj["C"][0],t["p_bot"][1]),t["p_bot"]])
wire(ax,[t["p_top"],(bj["C"][0],t["p_top"][1]),(bj["C"][0],6.0)]); terminal(ax,(bj["C"][0],6.0)); label(ax,(bj["C"][0],6.45),"+V$_{CC}$",size=8)
wire(ax,[(bj["C"][0],6.0),(1.8,6.0)]); res(ax,(1.8,6.0),(1.8,2.6),"R$_B$",side=-1,off=0.2); wire(ax,[(1.8,2.6),(1.8,1.7),bj["B"]]); node(ax,(1.8,1.7))
wire(ax,[(1.8,1.7),(1.0,1.7)]); cap(ax,(1.0,1.7),(0.2,1.7)); wire(ax,[(0.2,1.7),(-0.4,1.7)]); terminal(ax,(-0.4,1.7)); label(ax,(-0.4,2.2),"v$_i$",size=8.2)
wire(ax,[bj["E"],(bj["E"][0],0.2)]); gnd(ax,(bj["E"][0],0.2))
wire(ax,[t["s_top"],(8.2,t["s_top"][1])]); res(ax,(8.2,t["s_top"][1]),(8.2,t["s_bot"][1]),"R$_L$",side=1,off=0.5,body=0.9); wire(ax,[(8.2,t["s_bot"][1]),t["s_bot"]])
b=fig.add_axes([0.62,0.2,0.36,0.70])
b.plot([0,2],[1.0,1.0],alpha=0) ; b.plot([1,1],[0,2.0],color=INK,lw=1.4); b.plot([0,2],[2.0,0],color=ACCENT,lw=1.4)
b.scatter([1],[1.0],color=ACCENT,zorder=5,s=22); b.text(1.05,1.05,"Q",color=ACCENT,fontsize=8)
b.text(1.03,1.75,"d.c. load line\n(R$_{dc}$ ≈ 0, vertical)",fontsize=6.6); b.text(0.08,0.14,"a.c. load line, slope −1/R$_L'$",fontsize=6.6,color=ACCENT)
b.set_xticks([0,1,2]); b.set_xticklabels(["0","V$_{CC}$","2V$_{CC}$"],fontsize=8); b.set_yticks([1,2]); b.set_yticklabels(["I$_{CQ}$","2I$_{CQ}$"],fontsize=8)
b.set_xlabel("v$_{CE}$",fontsize=8); b.set_ylabel("i$_C$",fontsize=8); b.set_xlim(0,2.1); b.set_ylim(0,2.2)
for s in ("top","right"): b.spines[s].set_visible(False)
'''

F['seriesreg'] = r'''fig,ax=ckt_canvas(5.6,3.7,xlim=(-1.0,9.8),ylim=(-0.4,7.2))
terminal(ax,(0.0,6.4)); label(ax,(-0.3,6.4),"V$_{in}$",ha="right",size=8.4)
wire(ax,[(0.0,6.4),(4.2,6.4),(4.2,5.3)]); node(ax,(1.6,6.4))
q1=bjt(ax,3.6,4.2); label(ax,(5.5,4.7),"Q$_1$ (pass)",ha="left",size=7.6)
res(ax,(1.6,6.4),(1.6,4.8),"R",side=-1,off=0.2,body=0.9); wire(ax,[(1.6,4.8),(1.6,4.2),q1["B"]]); node(ax,(1.6,4.2))
wire(ax,[(1.6,4.2),(1.6,3.9)]); diode(ax,(1.6,1.0),(1.6,3.9),"D$_Z$",side=-1,off=0.5,zener=True); gnd(ax,(1.6,1.0))
wire(ax,[q1["E"],(4.2,2.6),(4.8,2.6)]); node(ax,(4.8,2.6)); res(ax,(4.8,2.6),(7.2,2.6),"R$_{sc}$",side=-1,off=0.5,body=1.4)
q2=bjt(ax,6.6,3.7); label(ax,(8.0,4.9),"Q$_2$ (limiter)",ha="left",size=7.6)
wire(ax,[(4.8,2.6),(4.8,3.7),q2["B"]]); wire(ax,[q2["E"],(7.2,2.6)]); node(ax,(7.2,2.6))
wire(ax,[q2["C"],(7.2,5.9),(2.4,5.9),(2.4,4.2)]); node(ax,(2.4,4.2))
wire(ax,[(7.2,2.6),(8.2,2.6)]); node(ax,(8.2,2.6)); wire(ax,[(8.2,2.6),(9.2,2.6)]); terminal(ax,(9.2,2.6)); label(ax,(9.2,3.1),"V$_o$",size=8.4)
wire(ax,[(8.2,2.6),(8.2,2.2)]); res(ax,(8.2,2.2),(8.2,0.6),"R$_L$",side=-1,off=0.5,body=0.9); gnd(ax,(8.2,0.6))
'''

F['shunt'] = r'''fig,ax=ckt_canvas(5.2,3.4,xlim=(-1.2,9.6),ylim=(-0.4,6.8))
terminal(ax,(0.0,5.6)); label(ax,(-0.3,5.6),"V$_{in}$",ha="right",size=8.4)
wire(ax,[(0.0,5.6),(0.4,5.6)]); res(ax,(0.4,5.6),(2.4,5.6),"R$_s$",side=1,off=0.4,body=1.4); wire(ax,[(2.4,5.6),(7.4,5.6)])
node(ax,(2.8,5.6)); wire(ax,[(2.8,5.6),(2.8,5.0)]); diode(ax,(2.8,3.4),(2.8,5.0),"D$_Z$",side=-1,off=0.5,zener=True,body=0.6)
bj=bjt(ax,4.6,3.2); wire(ax,[(2.8,3.4),(2.8,3.2),bj["B"]]); node(ax,(2.8,3.2))
wire(ax,[(2.8,3.2),(2.8,2.8)]); res(ax,(2.8,2.8),(2.8,0.9),"R$_B$",side=-1,off=0.3,body=0.8); gnd(ax,(2.8,0.9))
wire(ax,[bj["C"],(5.2,5.6)]); node(ax,(5.2,5.6)); label(ax,(5.6,4.5),"Q (shunt)",ha="left",size=7.6)
wire(ax,[bj["E"],(5.2,0.7)]); gnd(ax,(5.2,0.7))
node(ax,(7.4,5.6)); res(ax,(7.4,5.6),(7.4,1.0),"R$_L$",side=1,off=0.3,body=1.2); gnd(ax,(7.4,1.0))
wire(ax,[(7.4,5.6),(8.4,5.6)]); terminal(ax,(8.4,5.6)); label(ax,(8.4,6.1),"V$_o$",size=8.4)
'''

ZEN = r'''fig,ax=ckt_canvas(4.6,2.5,xlim=(-1.4,8.4),ylim=(-0.2,5.0))
wire(ax,[(0.0,0.6),(6.4,0.6)]); vsrc(ax,(0.0,0.6),(0.0,3.4),"V$_S$ = __VS__",side=-1,off=0.9); wire(ax,[(0.0,3.4),(0.0,4.2),(1.0,4.2)])
res(ax,(1.0,4.2),(3.0,4.2),"R$_S$ = __RS__",side=1,off=0.45,body=1.4); wire(ax,[(3.0,4.2),(6.4,4.2)])
node(ax,(4.2,4.2)); node(ax,(4.2,0.6)); diode(ax,(4.2,0.6),(4.2,4.2),"D$_Z$ (__VZ__)",side=1,off=0.5,zener=True,body=0.7)
node(ax,(6.4,4.2)); wire(ax,[(6.4,4.2),(6.4,3.9)]); res(ax,(6.4,3.9),(6.4,0.6),"R$_L$ = __RL__",side=1,off=0.2,body=1.4)
gnd(ax,(0.0,0.6))
'''

F['q3load'] = r'''fig=plt.figure(figsize=(7.2,2.9))
ax=fig.add_axes([0.0,0.0,0.46,1.0]); ax.set_xlim(-0.8,7.2); ax.set_ylim(-0.2,8.0); ax.set_aspect('equal'); ax.axis('off')
wire(ax,[(1.6,7.0),(5.6,7.0)]); terminal(ax,(5.6,7.0)); label(ax,(5.6,7.5),"V$_{CC}$ = 15 V",size=7.8)
res(ax,(1.6,7.0),(1.6,4.8),"R$_1$ = 10 kΩ",side=-1,off=0.15,body=1.2); wire(ax,[(1.6,4.8),(1.6,3.8)]); node(ax,(1.6,3.8))
bj=bjt(ax,3.2,3.8); wire(ax,[(1.6,3.8),bj["B"]]); wire(ax,[(1.6,3.8),(1.6,3.0)]); res(ax,(1.6,3.0),(1.6,0.9),"R$_2$ = 5 kΩ",side=-1,off=0.15,body=1.2); gnd(ax,(1.6,0.9))
node(ax,(3.8,7.0)); res(ax,(3.8,7.0),(3.8,5.4),"R$_C$ = 2 kΩ",side=1,off=0.15,body=1.2); wire(ax,[(3.8,5.4),bj["C"]])
wire(ax,[bj["E"],(3.8,2.3)]); res(ax,(3.8,2.3),(3.8,0.9),"R$_E$ = 1 kΩ",side=1,off=0.15,body=0.9); gnd(ax,(3.8,0.9))
b=fig.add_axes([0.56,0.22,0.41,0.70]); Vcc=15.0; b.plot([0,15],[5.0,0],color=INK,lw=1.5)
b.scatter([2.59],[4.12],color=ACCENT,zorder=5,s=24); b.text(3.2,4.3,"Q (2.59 V, 4.12 mA)",color=ACCENT,fontsize=7); b.plot([2.59,2.59],[0,4.12],color=ACCENT,lw=0.8,ls=":"); b.plot([0,2.59],[4.12,4.12],color=ACCENT,lw=0.8,ls=":")
b.text(6.0,2.6,"d.c. load line",fontsize=7.4,rotation=-19); b.text(0.3,5.15,"I$_{C(sat)}$ ≈ 5 mA",fontsize=7); b.text(10.2,0.25,"V$_{CE(cut-off)}$ = 15 V",fontsize=7)
b.set_xlabel("V$_{CE}$ (V)",fontsize=8); b.set_ylabel("I$_C$ (mA)",fontsize=8); b.set_xlim(0,16.5); b.set_ylim(0,5.8); b.set_title("d.c. load line and Q point",fontsize=7.6)
for s in ("top","right"): b.spines[s].set_visible(False)
'''

F['smallsig'] = r'''fig,ax=ckt_canvas(6.0,2.6,xlim=(-0.9,10.4),ylim=(-0.6,4.2))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.5,1.5),"v$_i$",size=9)
wire(ax,[(0,3),(1.2,3)]); node(ax,(1.2,3)); res(ax,(1.2,3),(1.2,0),"R$_B$",side=-1,off=0.55)
wire(ax,[(1.2,3),(2.8,3)]); res(ax,(2.8,3),(2.8,0),"r$_π$",side=-1,off=0.55,body=1.0)
wire(ax,[(2.8,3),(8.6,3)]); node(ax,(2.8,3)); node(ax,(4.6,3))
isrc(ax,(4.6,0),(4.6,3),None); label(ax,(5.1,1.5),"g$_m$v$_π$",ha="left",size=9)
node(ax,(6.4,3)); res(ax,(6.4,3),(6.4,0),"R$_C$",side=1,off=0.55)
node(ax,(7.8,3)); res(ax,(7.8,3),(7.8,0),"R$_L$",side=1,off=0.55)
wire(ax,[(8.6,3),(9.0,3)]); terminal(ax,(9.0,3)); terminal(ax,(9.0,0)); label(ax,(9.6,1.5),"v$_o$",size=9)
wire(ax,[(0,0),(9.0,0)]); node(ax,(1.2,0)); node(ax,(2.8,0)); node(ax,(4.6,0)); node(ax,(6.4,0)); node(ax,(7.8,0))
label(ax,(3.3,3.5),"v$_π$ across r$_π$",size=7,color=MUTED,ha="left")
'''

F['dynres'] = r'''fig=plt.figure(figsize=(7.0,2.5))
a=fig.add_axes([0.07,0.2,0.42,0.72]); v=np.linspace(0.3,0.78,300); I=lambda v:1e-3*(np.exp((v-0.62)/0.0259)-1)*1.0
a.plot(v,np.clip(I(v),0,12),color=INK,lw=1.5)
v0=0.66; i0=I(v0); g=i0/0.0259; vv=np.linspace(0.62,0.70,10); a.plot(vv,i0+g*(vv-v0),color=ACCENT,lw=1.0,ls="--")
a.scatter([v0],[i0],color=ACCENT,zorder=5,s=22); a.text(v0-0.045,i0+1.1,"Q (V$_D$, I$_D$)",fontsize=7.4,color=ACCENT)
a.plot([v0,v0+0.02],[i0,i0],color=MUTED,lw=0.8); a.plot([v0+0.02,v0+0.02],[i0,i0+g*0.02],color=MUTED,lw=0.8); a.text(v0+0.022,i0+0.4,"ΔI$_D$",fontsize=7); a.text(v0+0.003,i0-0.9,"ΔV$_D$",fontsize=7)
a.set_xlim(0.3,0.78); a.set_ylim(0,9); a.set_xlabel("v$_D$ (V)",fontsize=8); a.set_ylabel("i$_D$ (mA)",fontsize=8); a.set_title("slope at Q = 1/r$_d$ = I$_D$/(nV$_T$)",fontsize=7.6)
for s in ("top","right"): a.spines[s].set_visible(False)
b=fig.add_axes([0.55,0.0,0.44,1.0]); b.set_xlim(0,8); b.set_ylim(0,5); b.set_aspect('equal'); b.axis('off')
terminal(b,(0.6,3.0)); terminal(b,(7.0,3.0)); wire(b,[(0.6,3.0),(1.4,3.0)]); res(b,(1.4,3.0),(5.0,3.0),"r$_d$ = nV$_T$/I$_D$",side=1,off=0.5,body=2.4); wire(b,[(5.0,3.0),(7.0,3.0)])
arrow(b,(2.0,3.9),(3.6,3.9)); label(b,(2.8,4.3),"i$_d$",size=8)
label(b,(0.6,2.4),"anode",size=7,ha="center"); label(b,(7.0,2.4),"cathode",size=7,ha="center"); label(b,(3.7,1.2),"small-signal model of the forward-biased diode",size=7,color=MUTED)
'''

F['noninv'] = r'''fig,ax=ckt_canvas(4.6,3.0,xlim=(-1.0,8.6),ylim=(0.4,5.6))
o=opamp(ax,3.0,3.0,2.4,2.4,"")
wire(ax,[o["non"],(2.6,o["non"][1]),(2.6,1.2),(0.6,1.2)]); terminal(ax,(0.6,1.2)); label(ax,(0.3,1.2),"v$_i$",ha="right",size=8.4)
wire(ax,[o["inv"],(2.0,o["inv"][1])]); node(ax,(2.0,o["inv"][1])); res(ax,(2.0,o["inv"][1]),(2.0,2.4),"R$_1$",side=-1,off=0.3,body=0.7); gnd(ax,(2.0,2.4))
wire(ax,[(2.0,o["inv"][1]),(2.0,5.0),(2.8,5.0)]); res(ax,(2.8,5.0),(4.8,5.0),"R$_f$",side=1,off=0.35,body=1.2); wire(ax,[(4.8,5.0),(5.8,5.0),(5.8,3.0)])
wire(ax,[o["out"],(5.8,3.0)]); node(ax,(5.8,3.0)); wire(ax,[(5.8,3.0),(7.0,3.0)]); terminal(ax,(7.0,3.0)); label(ax,(7.3,3.0),"v$_o$",ha="left",size=8.4)
'''

F['q6mos2'] = F['q6mos'].replace('"R$_1$"','"__R1__"').replace('"R$_2$"','"__R2__"').replace('"R$_D$"','"__RD__"').replace('"R$_S$"','"__RS__"').replace('"+V$_{DD}$"','"__VDD__"')
'''
'''

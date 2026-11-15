F3 = {}

F3['f555'] = r'''
fig=plt.figure(figsize=(7.6,3.1))
ax=fig.add_axes([0.0,0.0,0.50,1.0]); ax.set_xlim(-0.2,9.4); ax.set_ylim(-0.4,7.4); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(Rectangle((3.0,1.0),4.0,4.0,fc="#eaf1ff",ec=INK,lw=1.4)); ax.text(5,3.0,"555",ha="center",va="center",fontsize=14,weight="bold")
for y,t in ((4.2,"7 DISCH"),(3.0,"6 THRES"),(2.0,"2 TRIG")):
    ax.text(3.15,y+0.0,t,fontsize=6.6,va="center"); ax.plot([3.0,1.2],[y,y],color=INK,lw=1.4)
ax.text(6.85,3.0,"OUT 3",fontsize=6.6,ha="right",va="center"); ax.plot([7.0,8.6],[3.0,3.0],color=INK,lw=1.4); ax.text(8.7,3.0,"v$_o$",fontsize=8.6,va="center")
ax.text(6.85,2.0,"CV 5",fontsize=6.6,ha="right",va="center"); ax.plot([7.0,7.6,7.6],[2.0,2.0,1.6],color=INK,lw=1.2); ax.text(7.9,1.45,"0.01 µF",fontsize=6.4,va="center")
ax.text(4.0,4.75,"8 V$_{CC}$",fontsize=6.6,ha="center",va="top"); ax.plot([4.0,4.0],[5.0,6.5],color=INK,lw=1.4)
ax.text(6.0,4.75,"4 RST",fontsize=6.6,ha="center",va="top"); ax.plot([6.0,6.0],[5.0,6.5],color=INK,lw=1.4)
ax.text(5.0,1.25,"1 GND",fontsize=6.6,ha="center",va="bottom"); ax.plot([5.0,5.0],[1.0,0.3],color=INK,lw=1.4)
ax.plot([1.2,6.0],[6.5,6.5],color=INK,lw=1.4); ax.text(6.2,6.5,"+V$_{CC}$",fontsize=8,va="center")
res(ax,(1.2,6.5),(1.2,4.2),"R$_A$",side=1,off=0.55,body=0.9); res(ax,(1.2,4.2),(1.2,3.0),"R$_B$",side=1,off=0.6,body=0.7)
ax.plot([1.2,1.2],[3.0,2.0],color=INK,lw=1.4); ax.scatter([1.2,1.2,1.2],[4.2,3.0,2.0],color=INK,s=10,zorder=5)
cap(ax,(1.2,2.0),(1.2,0.3),"C",side=1,gap=0.24,off=0.5); ax.plot([1.2,5.0],[0.3,0.3],color=INK,lw=1.4); gnd(ax,(3.0,0.3)); ax.scatter([3.0,5.0],[0.3,0.3],color=INK,s=10,zorder=5)
b=fig.add_axes([0.58,0.12,0.40,0.80]); t=np.linspace(0,4.2,900); Vcc=1.0; lo,hi=Vcc/3,2*Vcc/3
v=lo; state=1; dt=t[1]-t[0]; vc=[]; vo=[]
for _ in t:
    if state==1:
        v+=(Vcc-v)/1.0*dt
        if v>=hi: state=0
    else:
        v+=(0-v)/0.8*dt
        if v<=lo: state=1
    vc.append(v); vo.append(1.0 if state==1 else 0.0)
b.plot(t,np.array(vo)*0.9+1.3,color=INK,lw=1.5); b.plot(t,vc,color=ACCENT,lw=1.4)
for y,tx in ((hi,"2V$_{CC}$/3"),(lo,"V$_{CC}$/3")):
    b.axhline(y,color=MUTED,lw=0.7,ls="--"); b.text(4.25,y,tx,fontsize=6.8,va="center")
b.text(0.05,2.35,"v$_o$ (output)",fontsize=7.4); b.text(0.05,-0.02,"v$_C$ (capacitor)",fontsize=7.4,color=ACCENT,va="bottom")
b.set_xlim(0,5.3); b.set_ylim(-0.05,2.6); b.set_xlabel("t",fontsize=8); b.set_yticks([]); b.set_xticks([])
for s in ("top","right","left"): b.spines[s].set_visible(False)
'''

F3['widlar'] = r'''
fig,ax=ckt_canvas(4.6,3.8,xlim=(-0.6,9.0),ylim=(-0.8,9.0))
ax.plot([0.4,7.4],[8.4,8.4],color=INK,lw=1.5); label(ax,(7.7,8.4),"+V$_{CC}$",ha="left",size=8.6)
q1=bjt(ax,2.4,2.4); q2=bjt(ax,6.4,2.4)
wire(ax,[q1["B"],(1.0,2.4),(1.0,4.8),(5.0,4.8),(5.0,2.4),q2["B"]])
wire(ax,[q1["C"],(3.0,5.4)]); node(ax,(3.0,4.8))
res(ax,(3.0,8.4),(3.0,5.4),"R",side=-1,off=0.55,body=1.0); node(ax,(3.0,8.4))
wire(ax,[q1["E"],(3.0,0.0),(7.0,0.0)]); gnd(ax,(3.0,0.0)); node(ax,(3.0,0.0))
wire(ax,[q2["E"],(7.0,1.3)]); res(ax,(7.0,1.3),(7.0,0.0),"R$_E$",side=1,off=0.5,body=0.6)
wire(ax,[q2["C"],(7.0,6.6)]); arrow(ax,(7.0,5.8),(7.0,4.6),"I$_O$",off=0.9)
arrow(ax,(3.0,7.9),(3.0,6.9),"I$_{REF}$",off=-0.9)
label(ax,(2.3,4.1),"Q$_1$",size=8.4); label(ax,(6.2,4.1),"Q$_2$",size=8.4); label(ax,(7.2,7.0),"to load",size=7.6,ha="left")
'''

F3['classA_tc'] = r'''
fig=plt.figure(figsize=(7.4,2.9))
ax=fig.add_axes([0.0,0.0,0.50,1.0]); ax.set_xlim(-1.4,9.6); ax.set_ylim(-1.4,7.0); ax.set_aspect('equal'); ax.axis('off')
tr=transformer(ax,3.6,2.4,w=2.2,h=2.4,turns=6)
bj=bjt(ax,1.6,1.2)
wire(ax,[tr["p_top"],(3.0,tr["p_top"][1]),(3.0,5.8),(0.8,5.8)]); terminal(ax,(0.8,5.8)); label(ax,(0.4,5.8),"+V$_{CC}$",ha="right",size=8.4)
wire(ax,[tr["p_bot"],(2.2,tr["p_bot"][1]),bj["C"]])
wire(ax,[bj["E"],(2.2,-0.4)]); gnd(ax,(2.2,-0.4))
wire(ax,[bj["B"],(0.2,1.2)]); terminal(ax,(0.2,1.2)); label(ax,(-0.2,1.2),"v$_i$",ha="right",size=8.4)
x2=tr["s_top"][0]+1.0
wire(ax,[tr["s_top"],(x2,tr["s_top"][1])]); res(ax,(x2,tr["s_top"][1]),(x2,tr["s_bot"][1]),"R$_L$",side=1,off=0.5,body=0.8); wire(ax,[(x2,tr["s_bot"][1]),tr["s_bot"]])
b=fig.add_axes([0.60,0.17,0.38,0.74]); v=np.linspace(0,2.1,100)
for ib in (0.5,1.0,1.5,2.0,2.5): b.plot(v,ib*np.tanh(v*6)*0.9,color=MUTED,lw=0.7)
b.plot([0,2],[2.5,0],color=ACCENT,lw=1.6); b.scatter([1.0],[1.25],color=ACCENT,zorder=5,s=22); b.text(1.05,1.4,"Q",color=ACCENT,fontsize=8)
b.text(0.12,2.85,"a.c. load line, slope −1/R'$_L$",fontsize=6.8,color=ACCENT,va="top")
b.axvline(1.0,color=INK,lw=0.6,ls=":"); b.text(1.02,0.05,"V$_{CC}$",fontsize=7.2); b.text(2.0,0.05,"2V$_{CC}$",fontsize=7.2,ha="right")
b.set_xlim(0,2.1); b.set_ylim(0,3.0); b.set_xlabel("v$_{CE}$",fontsize=8.4); b.set_ylabel("i$_C$",fontsize=8.4); b.set_xticks([]); b.set_yticks([])
for s in ("top","right"): b.spines[s].set_visible(False)
'''

F3['classB_pp'] = r'''
fig=plt.figure(figsize=(7.4,2.9))
ax=fig.add_axes([0.0,0.0,0.58,1.0]); ax.set_xlim(-1.4,12.6); ax.set_ylim(-0.6,7.4); ax.set_aspect('equal'); ax.axis('off')
t1=transformer(ax,0.6,2.0,w=1.8,h=3.6,turns=7); t2=transformer(ax,8.0,2.0,w=1.8,h=3.6,turns=7)
terminal(ax,(-0.9,5.6)); terminal(ax,(-0.9,2.0)); label(ax,(-1.1,3.8),"v$_i$",ha="right",size=8.6)
wire(ax,[(-0.9,5.6),t1["p_top"]]); wire(ax,[(-0.9,2.0),t1["p_bot"]])
for (cx,cy,n) in ((5.0,5.2,"Q$_1$"),(5.0,2.4,"Q$_2$")):
    ax.add_patch(Circle((cx,cy),0.62,fc="white",ec=INK,lw=1.4,zorder=3)); ax.text(cx,cy,n,ha="center",va="center",fontsize=8.4,zorder=4)
wire(ax,[t1["s_top"],(3.0,t1["s_top"][1]),(3.0,5.2),(4.38,5.2)]); wire(ax,[t1["s_bot"],(3.0,t1["s_bot"][1]),(3.0,2.4),(4.38,2.4)])
ax.text(4.2,5.5,"B",fontsize=6.6); ax.text(4.2,2.7,"B",fontsize=6.6)
wire(ax,[(5.62,5.2),(6.9,5.2),(6.9,t2["p_top"][1]),t2["p_top"]]); wire(ax,[(5.62,2.4),(6.9,2.4),(6.9,t2["p_bot"][1]),t2["p_bot"]])
ax.text(5.8,5.5,"C",fontsize=6.6); ax.text(5.8,2.7,"C",fontsize=6.6)
wire(ax,[(5.0,4.58),(5.0,3.02)]); node(ax,(5.0,3.8)); wire(ax,[(5.0,3.8),(5.9,3.8)]); gnd(ax,(5.9,3.8)); label(ax,(5.0,3.8),"E",size=6.6,ha="right")
wire(ax,[(7.75,3.8),(7.2,3.8)]); terminal(ax,(7.2,3.8)); label(ax,(7.2,4.15),"+V$_{CC}$",size=7.4,ha="center")
x2=t2["s_top"][0]+1.0
wire(ax,[t2["s_top"],(x2,t2["s_top"][1])]); res(ax,(x2,t2["s_top"][1]),(x2,t2["s_bot"][1]),"R$_L$",side=1,off=0.5,body=0.9); wire(ax,[(x2,t2["s_bot"][1]),t2["s_bot"]])
b=fig.add_axes([0.68,0.18,0.30,0.72]); x=np.linspace(0,4*np.pi,400); v=np.sin(x)
b.plot(x,v,color=MUTED,lw=0.9,ls="--"); b.plot(x,np.where(v>0,v,0),color=INK,lw=1.4); b.plot(x,np.where(v<0,v,0),color=ACCENT,lw=1.4)
b.text(1.5,1.1,"Q$_1$",ha="center",fontsize=7.6); b.text(4.7,-1.35,"Q$_2$",ha="center",fontsize=7.6,color=ACCENT)
b.set_ylim(-1.7,1.5); b.set_xticks([]); b.set_yticks([]); b.set_xlabel("each transistor: 180° of the cycle",fontsize=7.4)
for s in ("top","right"): b.spines[s].set_visible(False)
'''

F3['series_prot'] = r'''
fig,ax=ckt_canvas(5.8,3.9,xlim=(-1.4,10.6),ylim=(-1.0,7.6))
terminal(ax,(0,6.2)); terminal(ax,(0,0)); label(ax,(-0.3,3.1),"V$_i$",ha="right",size=8.6)
wire(ax,[(0,6.2),(4.2,6.2)]); node(ax,(1.2,6.2)); node(ax,(4.2,6.2))
q1=bjt(ax,3.6,4.2); label(ax,(2.9,5.3),"Q$_1$ (pass)",size=7.4,ha="center")
wire(ax,[q1["C"],(4.2,6.2)])
res(ax,(1.2,6.2),(1.2,4.2),"R$_1$",side=-1,off=0.5,body=0.8); node(ax,(1.2,4.2)); wire(ax,[(1.2,4.2),q1["B"]])
wire(ax,[(1.2,4.2),(1.2,3.4)]); diode(ax,(1.2,0.0),(1.2,3.4),"D$_Z$",side=-1,zener=True,body=0.6,off=0.55)
wire(ax,[q1["E"],(4.2,3.0),(5.0,3.0)]); node(ax,(5.0,3.0))
res(ax,(5.0,3.0),(6.8,3.0),"R$_{SC}$",side=-1,off=0.5,body=0.8); node(ax,(6.8,3.0))
q2=bjt(ax,6.2,4.8); label(ax,(7.9,4.8),"Q$_2$ (limiter)",size=7.4,ha="left")
wire(ax,[q2["B"],(5.0,4.8),(5.0,3.0)]); wire(ax,[q2["E"],(6.8,3.7),(6.8,3.0)])
wire(ax,[q2["C"],(6.8,6.9),(0.6,6.9),(0.6,4.2),(1.2,4.2)])
wire(ax,[(6.8,3.0),(9.2,3.0)]); terminal(ax,(9.2,3.0)); terminal(ax,(9.2,0)); label(ax,(9.5,1.5),"V$_o$",ha="left",size=8.6)
res(ax,(8.2,3.0),(8.2,0.0),"R$_L$",side=1,off=0.5); node(ax,(8.2,3.0))
wire(ax,[(0,0),(9.2,0)]); node(ax,(1.2,0)); node(ax,(8.2,0))
'''

F3['lm317'] = r'''
fig,ax=ckt_canvas(5.4,3.2,xlim=(-0.8,10.6),ylim=(-0.8,5.8))
ax.add_patch(Rectangle((3.0,2.8),3.2,2.2,fc="#eaf1ff",ec=INK,lw=1.4)); label(ax,(4.6,4.0),"LM317",size=11)
label(ax,(3.15,4.35),"IN",size=7.4,ha="left"); label(ax,(6.05,4.35),"OUT",size=7.4,ha="right"); label(ax,(4.6,3.05),"ADJ",size=7.4,va="bottom")
terminal(ax,(0,4.2)); label(ax,(-0.3,4.2),"V$_{in}$",ha="right",size=8.6); wire(ax,[(0,4.2),(3.0,4.2)]); node(ax,(1.4,4.2))
cap(ax,(1.4,4.2),(1.4,0.0),"C$_1$ 0.1 µF",side=-1,off=1.0)
wire(ax,[(6.2,4.2),(9.4,4.2)]); terminal(ax,(9.4,4.2)); label(ax,(9.7,4.2),"V$_o$",ha="left",size=8.6)
node(ax,(7.4,4.2)); node(ax,(8.6,4.2))
res(ax,(7.4,4.2),(7.4,1.8),"R$_1$ = 240 Ω",side=1,off=0.5,body=1.0); node(ax,(7.4,1.8))
wire(ax,[(7.4,1.8),(4.6,1.8),(4.6,2.8)])
res(ax,(7.4,1.8),(7.4,0.0),"R$_2$",side=1,off=0.5,body=0.8)
cap(ax,(8.6,4.2),(8.6,0.0),"C$_2$ 1 µF",side=1,off=0.5)
wire(ax,[(1.4,0.0),(8.6,0.0)]); node(ax,(7.4,0.0)); gnd(ax,(4.6,0.0)); node(ax,(4.6,0.0))
'''

F3['tuned'] = r'''
fig=plt.figure(figsize=(7.2,3.0))
ax=fig.add_axes([0.0,0.0,0.46,1.0]); ax.set_xlim(-0.6,7.4); ax.set_ylim(-1.0,8.0); ax.set_aspect('equal'); ax.axis('off')
bj=bjt(ax,2.6,2.4)
wire(ax,[bj["C"],(3.2,4.6)]); node(ax,(3.2,4.6))
wire(ax,[(2.2,4.6),(4.2,4.6)]); wire(ax,[(2.2,6.2),(4.2,6.2)]); node(ax,(3.2,6.2))
ind(ax,(2.2,6.2),(2.2,4.6),"L",side=-1,body=1.1,off=0.45); cap(ax,(4.2,6.2),(4.2,4.6),"C",side=1,off=0.45)
wire(ax,[(3.2,6.2),(3.2,7.2)]); terminal(ax,(3.2,7.2)); label(ax,(3.2,7.6),"+V$_{CC}$",size=8)
wire(ax,[(4.2,4.6),(5.4,4.6)]); terminal(ax,(5.4,4.6)); label(ax,(5.9,4.6),"v$_o$",ha="left",size=8.6)
wire(ax,[bj["B"],(0.4,2.4)]); terminal(ax,(0.4,2.4)); label(ax,(0.0,2.4),"v$_i$",ha="right",size=8.4)
wire(ax,[bj["E"],(3.2,0.5)]); res(ax,(3.2,0.5),(3.2,-0.8),"R$_E$",side=1,off=0.5,body=0.5); gnd(ax,(3.2,-0.8))
b=fig.add_axes([0.56,0.2,0.42,0.7]); f=np.linspace(0.6,1.4,400); Q=8; A=1/np.sqrt(1+(Q*(f-1/f))**2)
b.plot(f,A,color=INK,lw=1.6); b.axhline(0.7071,color=ACCENT,lw=0.8,ls="--"); b.text(0.62,0.74,"A$_{max}$/√2 (−3 dB)",fontsize=7,color=ACCENT)
f1=(-1/(2*Q)+np.sqrt(1/(2*Q)**2+1)); f2=(1/(2*Q)+np.sqrt(1/(2*Q)**2+1))
b.plot([f1,f1],[0,0.7071],color=ACCENT,lw=0.8,ls=":"); b.plot([f2,f2],[0,0.7071],color=ACCENT,lw=0.8,ls=":")
b.annotate("",xy=(f1,0.3),xytext=(f2,0.3),arrowprops=dict(arrowstyle="<->",lw=0.9)); b.text(1.0,0.34,"BW = f$_2$ − f$_1$",ha="center",fontsize=7.4)
b.set_xticks([f1,1,f2]); b.set_xticklabels(["f$_1$","f$_o$","f$_2$"],fontsize=8); b.set_yticks([1]); b.set_yticklabels(["A$_{max}$"],fontsize=8); b.set_xlabel("frequency",fontsize=8); b.set_ylabel("voltage gain",fontsize=8)
for s in ("top","right"): b.spines[s].set_visible(False)
'''

F3['diffamp'] = r'''
fig,ax=ckt_canvas(5.4,4.2,xlim=(-1.0,11.0),ylim=(-1.4,9.6))
q1=bjt(ax,2.4,3.4); q2=bjt(ax,7.4,3.4)
terminal(ax,(0.4,3.4)); wire(ax,[(0.4,3.4),q1["B"]]); label(ax,(0.0,3.4),"v$_1$",ha="right",size=8.6)
wire(ax,[q2["B"],(5.9,3.4)]); terminal(ax,(5.9,3.4)); label(ax,(5.9,3.8),"v$_2$",size=8.6)
wire(ax,[q1["E"],(3.0,1.6),(8.0,1.6)]); wire(ax,[q2["E"],(8.0,1.6)]); node(ax,(5.5,1.6))
isrc(ax,(5.5,0.0),(5.5,1.6),None); label(ax,(6.0,0.8),"I$_{EE}$",ha="left",size=8.4)
wire(ax,[(5.5,0.0),(5.5,-0.6)]); terminal(ax,(5.5,-0.6)); label(ax,(6.0,-0.6),"−V$_{EE}$",ha="left",size=8)
wire(ax,[q1["C"],(3.0,6.0)]); wire(ax,[q2["C"],(8.0,6.0)])
ax.add_patch(Rectangle((2.4,6.0),6.2,1.4,fc="#fdf0e0",ec=INK,lw=1.3)); label(ax,(5.5,6.7),"active load: current mirror Q$_3$, Q$_4$",size=8)
wire(ax,[(5.5,7.4),(5.5,8.6)]); terminal(ax,(5.5,8.6)); label(ax,(6.0,8.6),"+V$_{CC}$",ha="left",size=8)
node(ax,(8.0,5.2)); wire(ax,[(8.0,5.2),(9.8,5.2)]); terminal(ax,(9.8,5.2)); label(ax,(10.1,5.2),"v$_o$",ha="left",size=8.6)
label(ax,(3.4,5.3),"Q$_1$",size=7.6,ha="left"); label(ax,(8.2,4.4),"Q$_2$",size=7.6,ha="left")
'''

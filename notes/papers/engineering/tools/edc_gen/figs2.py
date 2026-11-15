F2 = {}

F2['rcphase'] = r'''
fig,ax=ckt_canvas(6.2,3.2,xlim=(-0.4,10.6),ylim=(-0.9,6.2))
o=opamp(ax,5.0,3.6,w=2.2,h=2.0)
wire(ax,[o["inv"],(3.4,4.1)]); node(ax,(3.4,4.1))
wire(ax,[o["non"],(4.4,3.1),(4.4,2.3)]); gnd(ax,(4.4,2.3))
wire(ax,[(3.4,4.1),(3.4,5.4),(4.2,5.4)]); res(ax,(4.2,5.4),(6.2,5.4),"R$_f$",side=1,off=0.45)
wire(ax,[(6.2,5.4),(8.0,5.4),(8.0,3.6)]); wire(ax,[o["out"],(9.4,3.6)]); node(ax,(8.0,3.6)); terminal(ax,(9.4,3.6)); label(ax,(9.8,3.6),"v$_o$",ha="left",size=9)
wire(ax,[(8.0,3.6),(8.0,1.0)])
cap(ax,(8.0,1.0),(6.6,1.0),"C",side=1); node(ax,(6.6,1.0)); res(ax,(6.6,1.0),(6.6,-0.1),"R",side=1,off=0.4,body=0.6)
cap(ax,(6.6,1.0),(5.0,1.0),"C",side=1); node(ax,(5.0,1.0)); res(ax,(5.0,1.0),(5.0,-0.1),"R",side=1,off=0.4,body=0.6)
cap(ax,(5.0,1.0),(3.4,1.0),"C",side=1); res(ax,(3.4,1.0),(3.4,4.1),"R",side=-1,off=0.5,body=1.0)
wire(ax,[(3.4,-0.1),(6.6,-0.1)]); node(ax,(5.0,-0.1)); gnd(ax,(5.0,-0.1))
label(ax,(5.8,1.65),"three identical RC sections",size=7.6)
'''

def _tank(kind):
    top = {'hartley': 'ind(ax,(5.0,4.6),(3.2,4.6),"L$_1$",side=1,body=1.1); ind(ax,(3.2,4.6),(1.4,4.6),"L$_2$",side=1,body=1.1)\n'
                      'wire(ax,[(5.0,4.6),(5.0,5.7),(4.2,5.7)]); cap(ax,(4.2,5.7),(2.2,5.7),"C",side=1); wire(ax,[(2.2,5.7),(1.4,5.7),(1.4,4.6)])\n',
           'colpitts': 'cap(ax,(5.0,4.6),(3.2,4.6),"C$_1$",side=-1,gap=0.24); cap(ax,(3.2,4.6),(1.4,4.6),"C$_2$",side=-1,gap=0.24)\n'
                       'wire(ax,[(5.0,4.6),(5.0,5.7),(4.2,5.7)]); ind(ax,(4.2,5.7),(2.2,5.7),"L",side=1,body=1.2); wire(ax,[(2.2,5.7),(1.4,5.7),(1.4,4.6)])\n'}[kind]
    return r'''
fig,ax=ckt_canvas(5.2,3.6,xlim=(-0.6,8.6),ylim=(-1.2,7.6))
terminal(ax,(6.6,7.2)); label(ax,(7.0,7.2),"+V$_{CC}$",ha="left",size=8.6)
bj=bjt(ax,4.0,2.4)
node(ax,(5.0,4.6))
wire(ax,[(4.6,3.5),(4.6,4.6),(5.0,4.6)])
''' + top + r'''
wire(ax,[(1.4,4.6),(1.4,2.4),bj["B"]])
wire(ax,[(3.2,4.6),(3.2,3.9)]); node(ax,(3.2,4.6)); gnd(ax,(3.2,3.9))
wire(ax,[(5.0,4.6),(6.6,4.6)]); res(ax,(6.6,4.6),(6.6,6.6),"RFC",side=1,off=0.5,body=0.7); wire(ax,[(6.6,6.6),(6.6,7.2)])
wire(ax,[bj["E"],(4.6,0.7)]); res(ax,(4.6,0.7),(4.6,-0.4),"R$_E$",side=1,off=0.5,body=0.5); gnd(ax,(4.6,-0.4))
label(ax,(5.6,2.4),"f$_o$ = 1/(2π√(L$_{eq}$C$_{eq}$))",ha="left",size=7.4)
'''
F2['hartley'] = _tank('hartley').replace('node(ax,(5.0,4.6))','node(ax,(5.0,4.6))')
F2['colpitts'] = _tank('colpitts').replace('node(ax,(5.0,4.6))','node(ax,(5.0,4.6))')


F2['mirror_comp'] = r'''
fig,ax=ckt_canvas(5.0,4.2,xlim=(-0.6,9.0),ylim=(-0.8,10.0))
ax.plot([0.4,8.2],[9.3,9.3],color=INK,lw=1.5); label(ax,(8.5,9.3),"+V$_{CC}$",ha="left",size=8.6)
q1=bjt(ax,2.4,2.4); q2=bjt(ax,6.4,2.4); q3=bjt(ax,4.2,6.6)
wire(ax,[q1["B"],(1.0,2.4),(1.0,5.0),(4.8,5.0)]); wire(ax,[q2["B"],(5.0,2.4),(5.0,5.0),(4.8,5.0)]); node(ax,(5.0,5.0))
wire(ax,[q3["E"],(4.8,5.0)])
wire(ax,[q1["C"],(3.0,6.6),q3["B"]]); node(ax,(3.0,6.6)); 
res(ax,(3.0,9.3),(3.0,6.6),"R",side=-1,off=0.55,body=1.0); node(ax,(3.0,9.3))
wire(ax,[q3["C"],(4.8,9.3)]); node(ax,(4.8,9.3))
wire(ax,[q2["C"],(7.0,9.3)]); node(ax,(7.0,9.3)); wire(ax,[(7.0,3.5),(7.0,9.3)])
wire(ax,[q1["E"],(3.0,0.0),(7.0,0.0)]); wire(ax,[q2["E"],(7.0,0.0)]); gnd(ax,(5.0,0.0)); node(ax,(5.0,0.0))
arrow(ax,(3.0,8.7),(3.0,7.7),"I$_{REF}$",off=-0.9); arrow(ax,(7.0,8.2),(7.0,5.6),"I$_O$",off=0.9)
label(ax,(1.4,6.0),"Q$_3$ compensates\nthe base currents",size=7.4,ha="center")
label(ax,(2.3,4.3),"Q$_1$",size=8.4); label(ax,(6.3,4.3),"Q$_2$",size=8.4)
'''




F2['crossover'] = r'''
fig=plt.figure(figsize=(7.0,2.6))
x=np.linspace(0,4*np.pi,500); v=np.sin(x); d=0.6
a=fig.add_axes([0.04,0.2,0.28,0.65]); a.plot(x,v,color=MUTED,lw=0.8,ls="--"); y=np.where(v>d/1.2,v-d/1.2,np.where(v<-d/1.2,v+d/1.2,0)); a.plot(x,y,color=INK,lw=1.5)
a.set_title("class B: crossover distortion",fontsize=7.8); a.set_xticks([]); a.set_yticks([]); a.axhline(0,color=GRID,lw=0.5)
a.annotate("flat spot\n(|v$_{BE}$| < 0.7 V)",xy=(np.pi,0),xytext=(4.3,0.65),fontsize=6.4,arrowprops=dict(arrowstyle="->",lw=0.7))
b=fig.add_axes([0.38,0.2,0.28,0.65]); vi=np.linspace(-2,2,300)
b.plot(vi,np.where(vi>0.7,vi-0.7,np.where(vi<-0.7,vi+0.7,0)),color=INK,lw=1.4,label="class B"); b.plot(vi,np.where(vi>0.1,vi-0.1,np.where(vi<-0.1,vi+0.1,0)),color=ACCENT,lw=1.4,label="class AB")
b.set_title("transfer characteristic",fontsize=7.8); b.set_xlabel("v$_i$",fontsize=7.6); b.set_ylabel("v$_o$",fontsize=7.6); b.set_xticks([]); b.set_yticks([]); b.legend(fontsize=6.4,frameon=False,loc="upper left")
c=fig.add_axes([0.72,0.2,0.26,0.65]); y2=np.where(v>0.1,v-0.1,np.where(v<-0.1,v+0.1,0)); c.plot(x,v,color=MUTED,lw=0.8,ls="--"); c.plot(x,y2,color=ACCENT,lw=1.5)
c.set_title("class AB: practically linear",fontsize=7.8); c.set_xticks([]); c.set_yticks([]); c.axhline(0,color=GRID,lw=0.5)
for q in (a,b,c):
    for s in ("top","right"): q.spines[s].set_visible(False)
'''



from figs3 import F3
F2.update(F3)

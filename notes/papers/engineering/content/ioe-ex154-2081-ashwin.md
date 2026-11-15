---
file: NEBians-IOE-Past-Paper-Electronics-Circuit-EX154-2081-Ashwin.pdf
subject: Electronics Circuit
level: BE · Year I / Part II
code: EX 154
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
a) Explain the small signal model of PN junction diode and derive the expression for its dynamic resistance. [[4]]

b) Describe the operation of a full-wave bridge rectifier with necessary diagrams and waveforms. Also list its advantages over a half-wave rectifier. [[4]]

@q 2
Derive the expression for Z$_{in}$, Z$_{out}$, A$_v$ and A$_i$ in CE amplifier with bypass capacitor. [[6]]

@q 3
Draw the DC load line and determine the Q point of the voltage divider biased transistor circuit as shown in figure. Given: V$_{CC}$ = 15 V, R$_C$ = 2 kΩ, R$_E$ = 1 kΩ, R$_1$ = 10 kΩ, R$_2$ = 5 kΩ and β = 100. [[6]]

```figure caption="Question 3: voltage-divider bias, V$_{CC}$ = 15 V, R$_1$ = 10 kΩ, R$_2$ = 5 kΩ, R$_C$ = 2 kΩ, R$_E$ = 1 kΩ, β = 100."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig,ax=ckt_canvas(3.6,3.3); ax.set_xlim(-0.8,7.2); ax.set_ylim(-0.2,8.0); ax.set_aspect('equal'); ax.axis('off')
wire(ax,[(1.6,7.0),(5.6,7.0)]); terminal(ax,(5.6,7.0)); label(ax,(5.6,7.5),"V$_{CC}$ = 15 V",size=7.8)
res(ax,(1.6,7.0),(1.6,4.8),"R$_1$ = 10 kΩ",side=-1,off=0.15,body=1.2); wire(ax,[(1.6,4.8),(1.6,3.8)]); node(ax,(1.6,3.8))
bj=bjt(ax,3.2,3.8); wire(ax,[(1.6,3.8),bj["B"]]); wire(ax,[(1.6,3.8),(1.6,3.0)]); res(ax,(1.6,3.0),(1.6,0.9),"R$_2$ = 5 kΩ",side=-1,off=0.15,body=1.2); gnd(ax,(1.6,0.9))
node(ax,(3.8,7.0)); res(ax,(3.8,7.0),(3.8,5.4),"R$_C$ = 2 kΩ",side=1,off=0.15,body=1.2); wire(ax,[(3.8,5.4),bj["C"]])
wire(ax,[bj["E"],(3.8,2.3)]); res(ax,(3.8,2.3),(3.8,0.9),"R$_E$ = 1 kΩ",side=1,off=0.15,body=0.9); gnd(ax,(3.8,0.9))
```

@q 4
Explain the construction and working principle of EMOSFET with drain characteristic curve. [[6]]

@q 5
Find the drain current (I$_D$) and drain to source voltage (V$_{DS}$) for the following circuit. The given parameters are V$_t$ = 1 V and k = 0.5 mA/V$^2$. [[6]]

```figure caption="Question 5: enhancement MOSFET, V$_{DD}$ = +20 V, R$_1$ = 188 kΩ, R$_2$ = 47 kΩ, R$_D$ = 1.85 kΩ, R$_S$ = 1.65 kΩ."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig,ax=ckt_canvas(4.4,3.9,xlim=(-1.2,7.0),ylim=(-0.8,8.0))
wire(ax,[(1.2,7.0),(5.2,7.0)]); terminal(ax,(5.2,7.0)); label(ax,(5.6,7.0),"+20 V",ha="left",size=8.2)
res(ax,(1.2,7.0),(1.2,4.7),"R$_1$ = 188 kΩ",side=-1,off=0.2); wire(ax,[(1.2,4.7),(1.2,3.5)]); node(ax,(1.2,3.5)); wire(ax,[(1.2,3.5),(2.3,3.5)])
wire(ax,[(1.2,3.5),(1.2,2.6)]); res(ax,(1.2,2.6),(1.2,0.7),"R$_2$ = 47 kΩ",side=-1,off=0.2); gnd(ax,(1.2,0.7))
m=mosfet(ax,3.0,3.5,"n","enh")
wire(ax,[(4.0,7.0),(4.0,6.6)]); node(ax,(4.0,7.0)); res(ax,(4.0,7.0),(4.0,5.4),"R$_D$ = 1.85 kΩ",side=1,off=0.2); wire(ax,[(4.0,5.4),(4.0,4.6)])
wire(ax,[(4.0,2.4),(4.0,2.0)]); res(ax,(4.0,2.0),(4.0,0.7),"R$_S$ = 1.65 kΩ",side=1,off=0.2,body=0.8); gnd(ax,(4.0,0.7))
label(ax,(-0.5,7.5),"",ha="left",size=7.6)
```

@q 6
a) What is meant by Virtual Ground in Operational Amplifier? Write the criteria to maintain stability in Oscillation. [[2+2]]

b) Write any four properties of ideal Op-Amp. Derive voltage gain for a non-inverting amplifier using ideal Op-Amp. [[4]]

@q 7
Derive the maximum efficiency for Transformer coupled Class A power amplifier with circuit diagram and characteristics graph. [[6]]

@q 8
Draw the circuit diagram of the transformer coupled class B push-pull amplifier and show that the maximum efficiency is 25π %. [[6]]

@q 9
Explain how Transistor shunt voltage regulator works. [[4]]

@q 10
What is the main purpose of voltage regulator? Find the current flow through the zener diode (I$_Z$) in the given circuit, assuming V$_Z$ = 9 V. [[4]]

```figure caption="Question 10: Zener circuit, V$_S$ = 15 V, R$_S$ = 120 Ω, R$_L$ = 160 Ω, V$_Z$ = 9 V."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig,ax=ckt_canvas(4.6,2.5,xlim=(-1.4,8.4),ylim=(-0.2,5.0))
wire(ax,[(0.0,0.6),(6.4,0.6)]); vsrc(ax,(0.0,0.6),(0.0,3.4),"V$_S$ = 15 V",side=-1,off=0.9); wire(ax,[(0.0,3.4),(0.0,4.2),(1.0,4.2)])
res(ax,(1.0,4.2),(3.0,4.2),"R$_S$ = 120 Ω",side=1,off=0.45,body=1.4); wire(ax,[(3.0,4.2),(6.4,4.2)])
node(ax,(4.2,4.2)); node(ax,(4.2,0.6)); diode(ax,(4.2,0.6),(4.2,4.2),"D$_Z$ (9 V)",side=1,off=0.5,zener=True,body=0.7)
node(ax,(6.4,4.2)); wire(ax,[(6.4,4.2),(6.4,3.9)]); res(ax,(6.4,3.9),(6.4,0.6),"R$_L$ = 160 Ω",side=1,off=0.2,body=1.4)
gnd(ax,(0.0,0.6))
```
<!-- SOLUTIONS -->

@s 1
**(a) Small-signal model.** Let the diode be biased at a d.c. point Q (V$_D$, I$_D$) in forward conduction and let a small a.c. signal v$_d$ (much smaller than nV$_T$, i.e. below about 10 mV) be superimposed. Then v$_D$ = V$_D$ + v$_d$ and, from the Shockley equation i$_D$ = I$_S$(e$^{v_D/nV_T}$ − 1) with e$^{V_D/nV_T}$ ≫ 1,

$$\begin{gathered}i_D=I_Se^{V_D/nV_T}\,e^{v_d/nV_T}=I_D\,e^{v_d/nV_T} \\
\approx I_D\left(1+\frac{v_d}{nV_T}\right)=I_D+\frac{I_D}{nV_T}\,v_d
\end{gathered}$$

(only the first two terms of the series e$^x$ ≈ 1 + x are kept for |x| ≪ 1). The a.c. part of the current is therefore proportional to the a.c. voltage: i$_d$ = (I$_D$/nV$_T$)v$_d$, i.e. the diode behaves as a **linear resistor** called the **dynamic (incremental) resistance**

$$\boxed{\ r_d=\frac{v_d}{i_d}=\frac{dv_D}{di_D}\Big|_Q=\frac{nV_T}{I_D}\ \approx\ \frac{26\ \text{mV}}{I_D}\ (n=1,\ 300\ \text{K})\ }$$

```figure caption="The dynamic resistance is the reciprocal of the slope of the i-v curve at Q; the small-signal model is the resistor r$_d$."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig=plt.figure(figsize=(7.0,2.5))
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
```

*Example:* I$_D$ = 2 mA gives r$_d$ = 26/2 = 13 Ω; at I$_D$ = 0.1 mA, r$_d$ = 260 Ω. In reverse bias r$_d$ is very large (open circuit). At higher frequency the model also carries the junction (depletion) capacitance C$_j$ in reverse bias and the diffusion capacitance C$_d$ = τ$_T$I$_D$/(nV$_T$) in forward bias, in parallel with r$_d$.

**(b) Full-wave bridge rectifier.** Four diodes D$_1$ to D$_4$ are connected as a bridge across the secondary of the transformer (or directly across the a.c. line). During the **positive half cycle** the upper input terminal is positive: D$_1$ and D$_4$ are forward biased and conduct, D$_2$ and D$_3$ are reverse biased, and the current flows through R$_L$ from top to bottom. During the **negative half cycle** D$_2$ and D$_3$ conduct and D$_1$, D$_4$ are off; the current through R$_L$ again flows from top to bottom. Hence the load always sees the same polarity and the output frequency is 2f.

```figure caption="Bridge rectifier: D$_1$, D$_4$ conduct in the positive half cycle and D$_2$, D$_3$ in the negative half cycle."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig=plt.figure(figsize=(7.4,2.9))
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
```

With an ideal diode and secondary peak voltage V$_m$:

$$\begin{gathered}V_{dc}=\frac{2V_m}{\pi}\ \ (\text{with silicon diodes, }\tfrac{2}{\pi}(V_m-1.4\ \text{V})),\qquad V_{rms}=\frac{V_m}{\sqrt2} \\
r=0.482,\qquad \eta_{max}=81.2\ \text{percent},\qquad \text{PIV}=V_m
\end{gathered}$$

**Advantages over the half-wave rectifier:**

| Property | Half-wave | Bridge full-wave |
|---|---|---|
| V$_{dc}$ | V$_m$/π = 0.318V$_m$ | 2V$_m$/π = 0.636V$_m$ (double) |
| Ripple factor | 1.21 | 0.482 |
| Ripple frequency | f | 2f (easier to filter) |
| Maximum efficiency | 40.6 percent | 81.2 percent |
| Transformer utilisation | 0.287 | 0.812 (no d.c. saturation of the core) |

Compared with the centre-tapped full-wave circuit, the bridge needs no centre-tapped transformer and each diode must withstand only V$_m$ (the centre-tap circuit needs 2V$_m$), at the cost of two diode drops in series.

@s 2
The emitter resistor R$_E$ is bypassed by C$_E$, so the emitter is at a.c. ground. R$_B$ = R$_1$ ∥ R$_2$; r$_π$ = β/g$_m$ = βr$_e$ with g$_m$ = I$_C$/V$_T$; r$_o$ is the output resistance of the transistor.

```figure caption="Hybrid-π small-signal model of the CE amplifier with bypassed emitter."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig,ax=ckt_canvas(6.0,2.6,xlim=(-0.9,10.4),ylim=(-0.6,4.2))
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
```

**Input impedance.** Looking into the circuit from the source:

$$Z_{in}=R_B\parallel r_\pi=R_1\parallel R_2\parallel \beta r_e$$

**Output impedance.** Set v$_i$ = 0; then v$_π$ = 0 and the current source is dead, so only R$_C$ and r$_o$ remain (R$_L$ is the external load and is not counted):

$$Z_{out}=R_C\parallel r_o\approx R_C$$

**Voltage gain.** v$_π$ = v$_i$ and the current g$_m$v$_π$ flows in R$_C$ ∥ R$_L$ ∥ r$_o$ in the direction opposite to v$_o$:

$$A_v=\frac{v_o}{v_i}=-g_m\,(R_C\parallel R_L\parallel r_o)=-\frac{\beta\,(R_C\parallel R_L\parallel r_o)}{r_\pi}\approx-\frac{R_C\parallel R_L}{r_e}$$

**Current gain.** i$_i$ is the current delivered by the source into Z$_{in}$ and i$_o$ the current in R$_L$. By the current divider at the input, i$_b$ = i$_i$R$_B$/(R$_B$ + r$_π$) and at the output i$_o$ = −βi$_b$R$_C$/(R$_C$ + R$_L$) (r$_o$ neglected):

$$A_i=\frac{i_o}{i_i}=-\beta\,\frac{R_B}{R_B+r_\pi}\cdot\frac{R_C}{R_C+R_L}=A_v\frac{Z_{in}}{R_L}$$

All gains are negative: the CE stage gives a 180° phase shift, a medium input resistance, a high output resistance and large voltage and current gains. *Without* the bypass capacitor, R$_E$ appears in the base circuit as (β+1)R$_E$ and the gain falls to A$_v$ ≈ −R$_C$/(r$_e$ + R$_E$): this is why C$_E$ is used. *Example:* β = 100, I$_C$ = 1 mA (r$_e$ = 26 Ω), R$_B$ = 5 kΩ, R$_C$ = 2 kΩ, R$_L$ = 10 kΩ: Z$_{in}$ = 5 k ∥ 2.6 k = 1.71 kΩ, Z$_{out}$ = 2 kΩ, A$_v$ = −(1.667 k)/26 = −64, A$_i$ = −64 × 1.71 k/10 k = −11.

@s 3
**Thevenin equivalent of the base circuit.**

$$\begin{gathered}V_{TH}=V_{CC}\frac{R_2}{R_1+R_2}=15\times\frac{5}{15}=5\ \text{V} \\
R_{TH}=R_1\parallel R_2=\frac{10\times5}{15}=3.333\ \text{k}\Omega
\end{gathered}$$

**Base loop** (V$_{BE}$ = 0.7 V, I$_E$ = (β+1)I$_B$):

$$\begin{gathered}I_B=\frac{V_{TH}-V_{BE}}{R_{TH}+(\beta+1)R_E}=\frac{5-0.7}{3.333+101(1)}\ \text{mA}=41.2\ \mu\text{A} \\
I_C=\beta I_B=4.12\ \text{mA},\qquad I_E=(\beta+1)I_B=4.16\ \text{mA}
\end{gathered}$$

**Collector loop:**

$$V_{CE}=V_{CC}-I_CR_C-I_ER_E=15-4.12(2)-4.16(1)=\boxed{2.59\ \text{V}}$$

**Q point: (V$_{CEQ}$, I$_{CQ}$) = (2.59 V, 4.12 mA)** (I$_B$ = 41.2 µA). *Quick check with the approximate method (R$_{TH}$ neglected):* V$_E$ = 5 − 0.7 = 4.3 V, I$_E$ = 4.3 mA, I$_C$ ≈ 4.26 mA and V$_{CE}$ ≈ 15 − 4.26(2) − 4.3 = 2.19 V. The exact (Thevenin) result is used: the approximation overestimates I$_E$ by about 3 percent because I$_B$ drops 0.14 V across R$_{TH}$.

**DC load line.** The collector-loop equation V$_{CC}$ = I$_C$R$_C$ + V$_{CE}$ + I$_E$R$_E$ with I$_E$ ≈ I$_C$ gives the straight line

$$I_C=\frac{V_{CC}-V_{CE}}{R_C+R_E}=\frac{15-V_{CE}}{3\ \text{k}\Omega}$$

| Point | V$_{CE}$ | I$_C$ |
|---|---|---|
| Cut-off (I$_C$ = 0) | 15 V | 0 |
| Saturation (V$_{CE}$ ≈ 0) | 0 | 15/3 k = 5 mA |
| Q | 2.59 V | 4.12 mA |

```figure caption="DC load line and Q point of the voltage-divider biased stage."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig=plt.figure(figsize=(7.2,2.9))
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
```

The transistor is in the active region (V$_{CE}$ = 2.59 V > V$_{CE(sat)}$ ≈ 0.2 V and V$_{CB}$ = 1.89 V > 0). Since Q lies close to the saturation end of the load line the available output swing is small (about 2.4 V on the negative side): a larger R$_2$/R$_E$ or a smaller R$_C$ would centre Q better.

@s 4
**Construction.** The n-channel enhancement MOSFET (E-MOSFET) has a lightly doped **p-type substrate** with two heavily doped **n⁺ islands** (source and drain). A thin **SiO$_2$ layer** covers the surface between them and carries the metal **gate**. Unlike the depletion type there is **no built-in channel**: between the n⁺ regions lies p-type material (two back-to-back p-n junctions), so for V$_{GS}$ = 0 no current flows.


```figure caption="n-channel enhancement MOSFET: structure, transfer curve and drain characteristics."
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
```


**Working principle.**
1. *V$_{GS}$ = 0 (or below the threshold V$_T$):* the p-region separates source and drain; I$_D$ ≈ 0 (cut-off).
2. *V$_{GS}$ > 0:* the positive gate repels the holes of the p-substrate from the surface and attracts minority electrons, forming first a depletion layer. When V$_{GS}$ exceeds the **threshold voltage V$_T$** (about 1 to 4 V), a thin **inversion layer of electrons (induced n-channel)** connects source and drain. Increasing V$_{GS}$ further widens this channel and increases I$_D$ (the device is "enhanced").
3. *Effect of V$_{DS}$:* for small V$_{DS}$ the channel behaves as a resistor (ohmic or triode region). As V$_{DS}$ increases the channel at the drain end thins (the gate-to-channel voltage there is V$_{GD}$ = V$_{GS}$ − V$_{DS}$), and at V$_{DS}$ = V$_{GS}$ − V$_T$ the channel **pinches off** at the drain; for larger V$_{DS}$ the current saturates.

**Drain characteristic.** Plot of I$_D$ against V$_{DS}$ for V$_{GS}$ = V$_T$ + 1, + 2, ... V: each curve rises (ohmic region, the parabola) up to V$_{DS(sat)}$ = V$_{GS}$ − V$_T$, then is flat (saturation region, constant-current), and the locus of the pinch-off points is the parabola I$_D$ = k V$_{DS}^2$. For V$_{GS}$ ≤ V$_T$ the device is cut off.

**Mathematical expressions.**

$$\begin{gathered}
I_D=k\,(V_{GS}-V_T)^2\quad(\text{saturation, }V_{DS}\ge V_{GS}-V_T,\ V_{GS}>V_T) \\
I_D=2k\left[(V_{GS}-V_T)V_{DS}-\frac{V_{DS}^2}{2}\right]\quad(\text{triode, }V_{DS}<V_{GS}-V_T) \\
k=\frac{I_{D(on)}}{(V_{GS(on)}-V_T)^2}=\frac{1}{2}\mu_nC_{ox}\frac{W}{L},\qquad g_m=\frac{\partial I_D}{\partial V_{GS}}=2k(V_{GS}-V_T)
\end{gathered}$$


@s 5
The gate current is zero, so the gate voltage is given by the divider, and the source resistor gives the d.c. feedback:

$$\begin{gathered}V_G=V_{DD}\frac{R_2}{R_1+R_2}=20\times\frac{47}{188+47}=4.0\ \text{V} \\
V_{GS}=V_G-I_DR_S=4-1.65I_D\qquad(I_D\ \text{in mA}) \\
I_D=k(V_{GS}-V_t)^2=0.5(3-1.65I_D)^2
\end{gathered}$$

Expanding 0.5(9 − 9.9I$_D$ + 2.7225I$_D^2$) = I$_D$ gives the quadratic

$$1.36125I_D^2-5.95I_D+4.5=0\ \Rightarrow\ I_D=\frac{5.95\pm\sqrt{35.4025-24.5025}}{2.7225}=\frac{5.95\pm3.3015}{2.7225}=3.398\ \text{mA or }0.973\ \text{mA}$$

The root 3.398 mA gives V$_{GS}$ = 4 − 1.65(3.398) = −1.61 V, which is below V$_t$ (the device would be cut off), so it is rejected. For I$_D$ = 0.973 mA:

$$\begin{gathered}V_{GS}=4-1.65(0.973)=2.39\ \text{V}>V_t \\
V_{DS}=V_{DD}-I_D(R_D+R_S)=20-0.973(1.85+1.65)=16.6\ \text{V}
\end{gathered}$$

**Check:** V$_{GS}$ − V$_t$ = 1.39 V < V$_{DS}$ = 16.6 V, so the transistor is in saturation and the square law applies.

**Answer: I$_D$ = 0.973 mA ≈ 0.97 mA, V$_{DS}$ = 16.6 V** (V$_{GS}$ = 2.39 V).

@s 6
**(a) Virtual ground.** In an inverting amplifier (non-inverting input grounded) the open-loop gain A is very large, so the output is finite only if the differential input v$_d$ = v$_o$/A ≈ 0. Hence the inverting terminal is at the same potential as the grounded non-inverting terminal, v$_−$ ≈ v$_+$ = 0 V, although no wire connects it to ground. This is the **virtual ground** (a virtual short). No current flows into the input terminal (infinite input resistance), so the input current flows entirely through R$_f$: i = v$_i$/R$_1$ = −v$_o$/R$_f$ and the inverting gain is v$_o$/v$_i$ = −R$_f$/R$_1$. The input resistance seen by the source is R$_1$.

**Criteria for stable oscillation (Barkhausen criteria).** An amplifier of gain A with a positive-feedback network of factor β oscillates at a frequency f$_o$ if, around the loop, (i) the **magnitude** of the loop gain is unity, |Aβ| = 1, and (ii) the **phase shift** around the loop is 0° or 360° (so the feedback is positive), ∠Aβ = 0°. For the oscillation to **start**, |Aβ| must be slightly greater than 1 so that the noise builds up; the amplitude is then limited by the non-linearity of the active device (or an amplitude-stabilising lamp or diode network), which brings |Aβ| down to exactly 1. The criteria must be satisfied at one frequency only, which is fixed by the frequency-selective network (RC, LC or crystal).

**(b) Properties of an ideal op-amp** (any four): infinite open-loop gain; infinite input resistance (i$_+$ = i$_−$ = 0); zero output resistance; infinite bandwidth; infinite CMRR; zero offset voltage and drift; infinite slew rate.

**Non-inverting amplifier.** The input v$_i$ is applied to the non-inverting terminal; the output is fed back to the inverting terminal through the divider R$_f$, R$_1$.

```figure caption="Non-inverting amplifier."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig,ax=ckt_canvas(4.6,3.0,xlim=(-1.0,8.6),ylim=(0.4,5.6))
o=opamp(ax,3.0,3.0,2.4,2.4,"")
wire(ax,[o["non"],(2.6,o["non"][1]),(2.6,1.2),(0.6,1.2)]); terminal(ax,(0.6,1.2)); label(ax,(0.3,1.2),"v$_i$",ha="right",size=8.4)
wire(ax,[o["inv"],(2.0,o["inv"][1])]); node(ax,(2.0,o["inv"][1])); res(ax,(2.0,o["inv"][1]),(2.0,2.4),"R$_1$",side=-1,off=0.3,body=0.7); gnd(ax,(2.0,2.4))
wire(ax,[(2.0,o["inv"][1]),(2.0,5.0),(2.8,5.0)]); res(ax,(2.8,5.0),(4.8,5.0),"R$_f$",side=1,off=0.35,body=1.2); wire(ax,[(4.8,5.0),(5.8,5.0),(5.8,3.0)])
wire(ax,[o["out"],(5.8,3.0)]); node(ax,(5.8,3.0)); wire(ax,[(5.8,3.0),(7.0,3.0)]); terminal(ax,(7.0,3.0)); label(ax,(7.3,3.0),"v$_o$",ha="left",size=8.4)
```

Using the virtual short, v$_−$ = v$_+$ = v$_i$. No current enters the inverting terminal, so the same current flows in R$_1$ and R$_f$:

$$\begin{gathered}\frac{v_i}{R_1}=\frac{v_o-v_i}{R_f}\ \Rightarrow\ v_o=v_i\left(1+\frac{R_f}{R_1}\right) \\
\boxed{\ A_v=\frac{v_o}{v_i}=1+\frac{R_f}{R_1}\ }
\end{gathered}$$

The gain is positive (no phase inversion), is never less than 1, depends only on the resistor ratio, and the input resistance is ideally infinite. *Example:* R$_f$ = 9 kΩ, R$_1$ = 1 kΩ gives A$_v$ = 10. If R$_f$ = 0 and R$_1$ = ∞ the circuit becomes the voltage follower with A$_v$ = 1.

@s 7
**Circuit.** The collector load of the transformer-coupled class A stage is the **primary** of an output transformer whose secondary feeds R$_L$. The transformer reflects the load to the primary as R$_L'$ = (N$_1$/N$_2$)$^2$R$_L$ and has negligible d.c. resistance. The base is biased so that Q is at the centre of the a.c. load line.

```figure caption="Transformer-coupled class A amplifier: d.c. and a.c. load lines."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig=plt.figure(figsize=(7.4,2.9))
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
```

**Load lines.** Because the primary has no d.c. resistance, the **d.c. load line is vertical** at V$_{CE}$ = V$_{CC}$, and the Q point is (V$_{CC}$, I$_{CQ}$). The **a.c. load line** passes through Q with slope −1/R$_L'$. When the collector current falls to zero the collector voltage reaches 2V$_{CC}$ (the transformer's induced emf adds to V$_{CC}$), so

$$\begin{gathered}R_L'=\frac{V_{CC}}{I_{CQ}} \\ I_{C(max)}=2I_{CQ} \\ V_{CE(max)}=2V_{CC}\end{gathered}$$

**Power from the supply** (constant, independent of signal):

$$P_{dc}=V_{CC}I_{CQ}$$

**Maximum a.c. output power.** The largest undistorted swing is V$_{CE}$ from 0 to 2V$_{CC}$ and i$_C$ from 0 to 2I$_{CQ}$, so the peak values are V$_p$ = V$_{CC}$ and I$_p$ = I$_{CQ}$:

$$P_{ac(max)}=\frac{V_pI_p}{2}=\frac{V_{CC}I_{CQ}}{2}=\frac{V_{CC}^2}{2R_L'}$$

$$\boxed{\ \eta_{max}=\frac{P_{ac(max)}}{P_{dc}}=\frac{V_{CC}I_{CQ}/2}{V_{CC}I_{CQ}}=\frac12=50\ \text{percent}\ }$$

For any swing, η = (V$_p$/V$_{CC}$)$^2$/2 × 100 percent, i.e. in terms of the extreme values η = 50 × ((V$_{max}$ − V$_{min}$)/(V$_{max}$ + V$_{min}$))$^2$ percent. The efficiency is twice that of the series-fed (resistive-load) class A stage (25 percent) because no d.c. power is wasted in a load resistor. *Example:* V$_{CC}$ = 10 V and R$_L'$ = 20 Ω give I$_{CQ}$ = 0.5 A, P$_{dc}$ = 5 W, P$_{ac(max)}$ = 2.5 W, and the transistor dissipation is 5 W at no signal and 2.5 W at full signal.

@s 8
**Transformer-coupled class B push-pull amplifier.** Two identical transistors Q$_1$, Q$_2$ are biased at cut-off. The input transformer (centre-tapped secondary) feeds the two bases in anti-phase; each transistor conducts for 180° (one half cycle); the centre-tapped output transformer primary combines the two half cycles in the load.


```figure caption="Transformer-coupled class B push-pull amplifier; each transistor conducts for half a cycle."
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
```


**General efficiency.** Let the peak collector current be I$_p$ = V$_p$/R$_L'$ (V$_p$ = peak collector voltage swing, V$_p$ ≤ V$_{CC}$). Each transistor carries a half-sine pulse, so the average supply current is the sum of the two average currents:

$$\begin{gathered}
I_{dc}=2\cdot\frac{I_p}{\pi}=\frac{2V_p}{\pi R_L'},\qquad P_{dc}=V_{CC}I_{dc}=\frac{2V_{CC}V_p}{\pi R_L'} \\
P_{ac}=\frac{V_pI_p}{2}=\frac{V_p^2}{2R_L'} \\
\eta=\frac{P_{ac}}{P_{dc}}=\frac{V_p^2/(2R_L')}{2V_{CC}V_p/(\pi R_L')}=\frac{\pi}{4}\,\frac{V_p}{V_{CC}}\ \ (\times100\ \text{percent})
\end{gathered}$$

**Maximum efficiency** (V$_p$ = V$_{CC}$): η$_{max}$ = π/4 = **78.5 percent**, with P$_{ac(max)}$ = V$_{CC}^2$/(2R$_L'$) and P$_{dc}$ = 2V$_{CC}^2$/(πR$_L'$). The efficiency is **smallest (zero) at no signal** and increases linearly with V$_p$; no power is drawn from the supply when there is no signal.

**Power dissipation and the worst-case point.** P$_{D}$ (both transistors) = P$_{dc}$ − P$_{ac}$ = 2V$_{CC}$V$_p$/(πR$_L'$) − V$_p^2$/(2R$_L'$). Setting dP$_D$/dV$_p$ = 0: 2V$_{CC}$/(πR$_L'$) − V$_p$/R$_L'$ = 0, so the dissipation is **maximum at V$_p$ = 2V$_{CC}$/π ≈ 0.636V$_{CC}$**, where η = (π/4)(2/π) = 50 percent and

$$P_{D(max)}=\frac{2V_{CC}^2}{\pi^2R_L'}\ \ \text{(for both transistors; half in each)}$$

so each transistor must be rated for at least P$_{D(max)}$/2 = V$_{CC}^2$/(π²R$_L'$), which is about 0.2 P$_{ac(max)}$ (because P$_{ac(max)}$ = V$_{CC}^2$/(2R$_L'$)).

**Maximum efficiency in the form asked.** At V$_p$ = V$_{CC}$ the efficiency is

$$\eta_{max}=\frac{\pi}{4}=0.7854=\boxed{25\pi\ \text{percent}\ (=78.5\ \text{percent})}$$

which is much higher than the 50 percent of the transformer-coupled class A stage because in class B the transistors draw no quiescent current.

@s 9
**Circuit.** In a shunt regulator the **regulating element is connected in parallel with the load**, and a **series resistor R$_s$** between the unregulated supply V$_{in}$ and the output drops the excess voltage. Here the transistor Q is the shunt element; its base is driven from the output through the Zener D$_Z$ (reverse biased) and R$_B$.

```figure caption="Transistor shunt voltage regulator."
def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
fig,ax=ckt_canvas(5.2,3.4,xlim=(-1.2,9.6),ylim=(-0.4,6.8))
terminal(ax,(0.0,5.6)); label(ax,(-0.3,5.6),"V$_{in}$",ha="right",size=8.4)
wire(ax,[(0.0,5.6),(0.4,5.6)]); res(ax,(0.4,5.6),(2.4,5.6),"R$_s$",side=1,off=0.4,body=1.4); wire(ax,[(2.4,5.6),(7.4,5.6)])
node(ax,(2.8,5.6)); wire(ax,[(2.8,5.6),(2.8,5.0)]); diode(ax,(2.8,3.4),(2.8,5.0),"D$_Z$",side=-1,off=0.5,zener=True,body=0.6)
bj=bjt(ax,4.6,3.2); wire(ax,[(2.8,3.4),(2.8,3.2),bj["B"]]); node(ax,(2.8,3.2))
wire(ax,[(2.8,3.2),(2.8,2.8)]); res(ax,(2.8,2.8),(2.8,0.9),"R$_B$",side=-1,off=0.3,body=0.8); gnd(ax,(2.8,0.9))
wire(ax,[bj["C"],(5.2,5.6)]); node(ax,(5.2,5.6)); label(ax,(5.6,4.5),"Q (shunt)",ha="left",size=7.6)
wire(ax,[bj["E"],(5.2,0.7)]); gnd(ax,(5.2,0.7))
node(ax,(7.4,5.6)); res(ax,(7.4,5.6),(7.4,1.0),"R$_L$",side=1,off=0.3,body=1.2); gnd(ax,(7.4,1.0))
wire(ax,[(7.4,5.6),(8.4,5.6)]); terminal(ax,(8.4,5.6)); label(ax,(8.4,6.1),"V$_o$",size=8.4)
```

**Reference.** When the output voltage is above V$_Z$ + V$_{BE}$, the Zener is in breakdown and carries the base current of Q: the base voltage settles at V$_{BE}$ ≈ 0.7 V across R$_B$, so

$$V_o=V_Z+V_{BE}\approx V_Z+0.7\ \text{V}$$

**Action.** The series current is I$_S$ = (V$_{in}$ − V$_o$)/R$_s$ and it splits into I$_L$ (load) and I$_Q$ (through Q; the small Zener current is added to it): I$_S$ = I$_L$ + I$_Q$.

- If V$_{in}$ **increases** (or I$_L$ decreases), V$_o$ tends to rise; the base drive of Q increases, I$_Q$ rises, the extra current is drawn through R$_s$ and the extra drop in R$_s$ cancels the rise: V$_o$ stays constant.
- If V$_{in}$ **decreases** (or I$_L$ increases), V$_o$ tends to fall; the base drive and I$_Q$ fall, leaving more of I$_S$ for the load, and V$_o$ is restored.

Thus I$_S$ stays nearly constant and the output is regulated against line and load changes, with the transistor's current gain improving the regulation by a factor of about (β+1) compared with a plain Zener shunt. *Properties:* simple; the supply current is limited by R$_s$, so it is **short-circuit proof** (no extra current-limit circuit); but it is **inefficient** because I$_S$ flows all the time and the power V$_o$I$_Q$ is lost in Q even at light load, so it is used for low-power loads. The limit is I$_{L(max)}$ < (V$_{in(min)}$ − V$_o$)/R$_s$.

@s 10
**Purpose of a voltage regulator.** A rectifier-filter gives an output that changes with the **a.c. line voltage**, the **load current** and the **temperature**, and carries **ripple**. The regulator keeps the d.c. output voltage **constant** against these variations (and reduces the ripple), so that electronic circuits, which need a fixed supply, work correctly. Its quality is measured by the line regulation ΔV$_o$/ΔV$_{in}$, the load regulation (V$_{NL}$ − V$_{FL}$)/V$_{FL}$ and the output resistance.

**Zener current.** First find whether the Zener conducts. Remove it and compute the open-circuit load voltage:

$$V_L=V_S\frac{R_L}{R_S+R_L}=15\times\frac{160}{120+160}=8.57\ \text{V}<V_Z=9\ \text{V}$$

The voltage across the Zener is below its breakdown voltage, so the Zener is **not conducting**. (If it were assumed to be on, V$_o$ = 9 V would give I$_L$ = 9/160 = 56.25 mA, but the current available through R$_S$ is only (15 − 9)/120 = 50 mA, which would need I$_Z$ = 50 − 56.25 = −6.25 mA, impossible for a Zener, so that assumption fails.)

$$\boxed{\ I_Z\approx0\ \text{(only the negligible reverse leakage current flows)}\ }$$

The circuit then behaves as a plain divider: V$_o$ = 8.57 V (not regulated), I$_S$ = I$_L$ = 15/280 = 53.6 mA. The Zener would regulate only if V$_S$ were raised above V$_Z$(R$_S$ + R$_L$)/R$_L$ = 9 × 280/160 = 15.75 V.

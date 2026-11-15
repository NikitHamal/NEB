---
file: NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-EX151-2082-Baishakh.pdf
subject: Electronic Device and Circuits
level: BE · Year I / Part II
code: EX 151
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
Design a β-independent voltage divider bias circuit using the appropriate guidelines for the given parameters: V$_{CC}$ = 12 V, I$_E$ = 1 mA, and β = 100. [[4]]

@q 2
Determine input resistance, voltage gain and output resistance of given common emitter BJT Amplifier. β = 120 and r$_o$ = 40 kΩ. [[5]]

```figure caption="Question 2: common-emitter amplifier with fixed bias, V$_{CC}$ = +20 V, R$_B$ = 470 kΩ, R$_C$ = 2.2 kΩ, unbypassed R$_E$ = 0.56 kΩ."
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
```

@q 3
Explain the operation principle of a BJT as a switch with the necessary diagrams. [[4]]

@q 4
Describe the construction and working principle of n-channel depletion type MOSFET with the help of characteristics curve and mathematical expressions. [[7]]

@q 5
For the given JFET voltage divider configuration, determine I$_{DQ}$, V$_{GSQ}$, V$_{DS}$ and transconductance g$_m$. [[6]]

```figure caption="Question 5: JFET voltage-divider bias, V$_{DD}$ = 20 V, R$_1$ = 910 kΩ, R$_2$ = 110 kΩ, R$_D$ = 2.2 kΩ, R$_S$ = 1.1 kΩ, I$_{DSS}$ = 10 mA, V$_P$ = −3.5 V."
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"+20 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"910 kΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"110 kΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
wire(ax,[(2.0,3.2),(2.9,3.2)]); ax.plot([2.9,2.9],[2.2,4.2],color=INK,lw=2.4)
wire(ax,[(2.9,4.2),(4.0,4.2),(4.0,4.4)]); wire(ax,[(2.9,2.2),(4.0,2.2),(4.0,2.0)])
ax.annotate("",xy=(3.0,3.2),xytext=(2.45,3.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3,mutation_scale=9))
res(ax,(5.0,6.6),(5.0,4.9),"2.2 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"1.1 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"I$_{DSS}$ = 10 mA,  V$_P$ = −3.5 V",ha="left",size=8)
```

@q 6
Draw circuit diagram of LC Hartley oscillator. Derive its frequency of oscillation. [[4]]

@q 7
Derive the expression of bandwidth of class A tuned amplifier. [[4]]

@q 8
Show that the voltage gain of the differential amplifier with active load is twice with that with passive load. [[5]]

@q 9
Derive general efficiency of series fed class A amplifier. [[4]]

@q 10
For a class B amplifier using a supply of V$_{CC}$ = 30 V and driving a load of 16 Ω, determine the maximum input power, maximum output power and maximum power dissipation at transistors. [[5]]

@q 11
Derive frequency of oscillation of 555 timer Astable Multivibrator [[4]]

@q 12
Draw series voltage regulator with current limiting circuit and explain how this protection circuit works. Design a voltage regulator to give output voltage from 5 V to 15 V using LM317. [[4+4]]
<!-- SOLUTIONS -->

@s 1
**Design rules for a β-independent (stiff) voltage-divider bias.** Choose (i) V$_E$ = V$_{CC}$/10 so that V$_{BE}$ variations are small compared with V$_E$, (ii) V$_{CE}$ ≈ V$_{CC}$/2 for maximum undistorted swing, (iii) the divider current much larger than I$_B$, which is ensured by R$_2$ ≤ 0.1βR$_E$ (stiff divider; then V$_B$ is nearly independent of β).

Given: V$_{CC}$ = 12 V, I$_E$ ≈ I$_C$ = 1 mA, β = 100.

$$\begin{gathered}
V_E=\frac{V_{CC}}{10}=1.20\ \text{V}, \qquad R_E=\frac{V_E}{I_E}=\frac{1.20}{1\ \text{mA}}=1.20\ \text{k}\Omega \\
V_B=V_E+V_{BE}=1.20+0.7=1.90\ \text{V} \\
R_2\le 0.1\beta R_E=0.1(100)(1.20\ \text{k}\Omega)=12.00\ \text{k}\Omega\ \ \Rightarrow\ \ R_2=12.00\ \text{k}\Omega \\
\frac{R_2}{R_1+R_2}V_{CC}=V_B\ \Rightarrow\ R_1=R_2\left(\frac{V_{CC}}{V_B}-1\right)=63.79\ \text{k}\Omega \\
R_C=\frac{V_{CC}-V_E-V_{CE}}{I_C}=\frac{12-1.20-6.00}{0.990\ \text{mA}}=4.85\ \text{k}\Omega
\end{gathered}$$

Use the nearest standard values: R$_1$ ≈ 64 kΩ, R$_2$ ≈ 12 kΩ, R$_E$ ≈ 1.20 kΩ, R$_C$ ≈ 4.8 kΩ.

*Check of stiffness.* Thevenin resistance R$_B$ = R$_1$ ∥ R$_2$ = 10.10 kΩ, and I$_B$ = I$_C$/β = 9.9 µA. The voltage lost in R$_B$ is I$_B$R$_B$ = 0.10 V, only a small fraction of V$_B$; so I$_E$ = (V$_{BB}$ − V$_{BE}$)/(R$_E$ + R$_B$/(β+1)) changes by about 4.0 percent when β changes from β to 2β, i.e. the Q-point is practically β-independent. With I$_C$ = 0.990099 mA the quiescent voltages are V$_{CE}$ = 6.00 V and V$_C$ = 7.20 V (transistor in the active region).

@s 2
**d.c. analysis** (fixed bias with unbypassed R$_E$, V$_{BE}$ = 0.7 V):

$$I_B=\frac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}=\frac{20-0.7}{470\ \text{k}+121(0.56\ \text{k})}=\frac{19.3}{537.76\ \text{k}\Omega}=35.9\ \mu\text{A}$$

$$\begin{gathered}I_C=\beta I_B=4.307\ \text{mA} \\ I_E=(\beta+1)I_B=4.343\ \text{mA} \\ r_e=\frac{26\ \text{mV}}{I_E}=5.99\ \Omega\end{gathered}$$

$$V_{CE}=V_{CC}-I_CR_C-I_ER_E=20-9.476-2.432=8.09\ \text{V}\ \ (\text{active region})$$

**a.c. analysis.** The emitter is not bypassed, so R$_E$ appears in the small-signal model. Since r$_o$ = 40 kΩ ≥ 10(R$_C$ + R$_E$) = 27.6 kΩ, r$_o$ may be neglected in the approximate formulas (the exact values with r$_o$ are also given).


```figure caption="Hybrid-π small-signal model of the common-emitter amplifier (R$_E$ unbypassed; R$_E$ = 0 when bypassed)."
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
```


$$\begin{gathered}
Z_b=\beta(r_e+R_E)=120(5.99+560)=67.9\ \text{k}\Omega \\
\textbf{Input resistance:}\quad Z_i=R_B\parallel Z_b=\frac{470\times67.9}{470+67.9}=\mathbf{59.3\ k\Omega}\ \ (\text{exact with }r_o:\ 56.0\ \text{k}\Omega) \\
\textbf{Voltage gain:}\quad A_v=-\frac{\beta R_C}{Z_b}=-\frac{R_C}{r_e+R_E}=-\frac{2200}{565.99}=\mathbf{-3.89}\ \ (\text{exact:}\ -3.85) \\
\textbf{Output resistance:}\quad Z_o=R_C\parallel r_o=2.2\parallel40=\mathbf{2.09\ k\Omega}\ \ (\approx R_C=2.2\ \text{k}\Omega\ \text{if }r_o\text{ is neglected})
\end{gathered}$$

The negative sign shows the 180° phase shift; the gain is low because of the large unbypassed R$_E$ (a bypass capacitor across R$_E$ would raise it to −R$_C$/r$_e$ = −367).

@s 3
A BJT works as an electronic switch when it is driven between **cut-off** (switch OFF, open) and **saturation** (switch ON, closed); the active region is only passed through quickly.


```figure caption="BJT switch: circuit and load line with the two operating points."
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
```


- **Cut-off (OFF).** If the input is low (V$_i$ < 0.5 V, say 0 V) the base-emitter junction is not forward biased, I$_B$ = 0, I$_C$ ≈ I$_{CEO}$ ≈ 0, so V$_{CE}$ = V$_{CC}$ and V$_o$ ≈ V$_{CC}$: the collector-emitter path behaves as an **open switch** (high resistance).
- **Saturation (ON).** If the input is high (V$_i$ = V$_H$), a base current large enough to satisfy I$_B$ ≥ I$_{C(sat)}$/β drives both junctions forward, V$_{CE}$ falls to V$_{CE(sat)}$ ≈ 0.1 to 0.2 V and I$_C$ = I$_{C(sat)}$ = (V$_{CC}$ − V$_{CE(sat)}$)/R$_C$ ≈ V$_{CC}$/R$_C$: a **closed switch** (low resistance) with output V$_o$ ≈ 0.2 V. The base resistor is R$_B$ = (V$_H$ − 0.7)/I$_B$ with I$_B$ made about 2 to 5 times the minimum value to ensure hard saturation.
- The load line joins (V$_{CC}$, 0) and (0, V$_{CC}$/R$_C$); the two operating points are the ends of this line.

*Example.* V$_{CC}$ = 10 V, R$_C$ = 2.5 kΩ, β = 100, V$_H$ = 5 V: I$_{C(sat)}$ ≈ 4 mA, so I$_{B(min)}$ = 40 µA; take I$_B$ = 0.2 mA (5 times), R$_B$ = (5 − 0.7)/0.2 mA = 21.5 kΩ ≈ 22 kΩ.

The stage is also a **NOT gate (inverter)**: input high gives output low and vice versa. Switching speed is limited by the storage time and the delay, rise and fall times (t$_{on}$ = t$_d$ + t$_r$, t$_{off}$ = t$_s$ + t$_f$).

@s 4
**Construction.** The n-channel depletion-type MOSFET (D-MOSFET) is built on a lightly doped **p-type substrate** (SS) in which two heavily doped **n⁺ regions** are diffused for the source and the drain. A thin **n-type channel is physically built in** between them (by diffusion or implantation). A very thin layer of **SiO$_2$** (about 10 to 100 nm) covers the channel, and the metal **gate** is deposited on the oxide. Source and drain have metal contacts; the substrate is usually connected to the source. Because the gate is insulated by the oxide, the gate current is practically zero (input resistance about 10$^{10}$ to 10$^{15}$ Ω).


```figure caption="n-channel depletion MOSFET: structure, transfer curve and drain characteristics."
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
```


**Working principle.**
- **V$_{GS}$ = 0:** the built-in channel already exists, so for V$_{DS}$ > 0 the electrons flow from S to D and a drain current I$_{DSS}$ flows (at pinch-off).
- **V$_{GS}$ negative (depletion mode):** the negative gate charge repels the electrons of the channel, and the channel is depleted of carriers (narrower), so I$_D$ falls. At V$_{GS}$ = V$_P$ (negative, for example −4 V) the channel is fully depleted and I$_D$ = 0.
- **V$_{GS}$ positive (enhancement mode):** the positive gate attracts more electrons into the channel, enhancing it, and I$_D$ rises above I$_{DSS}$. The D-MOSFET can therefore be operated with either polarity of gate voltage (unlike the JFET).
- **Effect of V$_{DS}$:** as V$_{DS}$ is raised the channel narrows near the drain end and pinches off at V$_{DS}$ = V$_{GS}$ − V$_P$; beyond this I$_D$ is nearly constant (saturation).

**Characteristics.** The *transfer curve* is the Shockley parabola that extends from V$_P$ through I$_{DSS}$ (at V$_{GS}$ = 0) into positive V$_{GS}$; the *drain characteristics* have an ohmic (triode) region and a flat saturation region for each V$_{GS}$ (curves for V$_{GS}$ > 0, = 0 and < 0).

**Mathematical expressions.**

$$\begin{gathered}
I_D=I_{DSS}\left(1-\frac{V_{GS}}{V_P}\right)^2\quad(\text{saturation, }V_{DS}\ge V_{GS}-V_P) \\
I_D=\frac{2I_{DSS}}{V_P^2}\left[(V_{GS}-V_P)V_{DS}-\frac{V_{DS}^2}{2}\right]\quad(\text{triode, }V_{DS}<V_{GS}-V_P) \\
g_m=\frac{2I_{DSS}}{|V_P|}\left(1-\frac{V_{GS}}{V_P}\right)=\frac{2}{|V_P|}\sqrt{I_{DSS}I_D}
\end{gathered}$$

@s 5
The JFET is biased by a voltage divider with source resistor.


```figure caption="prob_jfet1"
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"+20 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"910 kΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"110 kΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
wire(ax,[(2.0,3.2),(2.9,3.2)]); ax.plot([2.9,2.9],[2.2,4.2],color=INK,lw=2.4)
wire(ax,[(2.9,4.2),(4.0,4.2),(4.0,4.4)]); wire(ax,[(2.9,2.2),(4.0,2.2),(4.0,2.0)])
ax.annotate("",xy=(3.0,3.2),xytext=(2.45,3.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3,mutation_scale=9))
res(ax,(5.0,6.6),(5.0,4.9),"2.2 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"1.1 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"I$_{DSS}$ = 10 mA,  V$_P$ = −3.5 V",ha="left",size=8)
```


**Solution** (R in kΩ, I in mA, V in V). The gate current is zero, so the divider fixes the gate voltage:

$$V_G=\frac{R_2}{R_1+R_2}V_{DD}=\frac{110}{910+110}(20)=2.1569\ \text{V}$$

The gate-source voltage is V$_{GS}$ = V$_G$ − I$_D$R$_S$ = 2.1569 − 1.1 I$_D$ and the device equation is I$_D$ = I$_{DSS}$(1 − V$_{GS}$/V$_P$)² = 10(1 − V$_{GS}$/(-3.5))². Substituting,

$$I_D=10\,(1.6162-0.3143\,I_D)^2\ \ \Rightarrow\ \ 0.9878\,I_D^2-11.1593\,I_D+26.1225=0$$

$$I_D=\frac{-B\pm\sqrt{B^2-4AC}}{2A}\ \ \Rightarrow\ \ I_D=3.312\ \text{mA}\ \ \text{or}\ \ 7.986\ \text{mA}$$

The root I$_D$ = 7.986 mA gives V$_{GS}$ = -6.63 V, which lies beyond cut-off (V$_{GS}$ < V$_P$ = -3.5 V), so it is rejected. Therefore

$$\begin{gathered}
I_D=3.312\ \text{mA}\\
V_{GS}=V_G-I_DR_S=2.1569-(3.312)(1.1)=-1.486\ \text{V}\ \ (>V_P)\\
V_{DS}=V_{DD}-I_D(R_D+R_S)=20-3.312(2.2+1.1)=9.072\ \text{V}
\end{gathered}$$

*Check of the region.* V$_{DS}$ = 9.072 V > V$_{GS}$ − V$_P$ = 2.014 V, so the transistor is in **saturation (pinch-off region)** and the Shockley equation is valid. Also g$_m$ = (2I$_{DSS}$/|V$_P$|)(1 − V$_{GS}$/V$_P$) = 3.288 mS.

**Answers:** I$_{DQ}$ = 3.31 mA, V$_{GSQ}$ = -1.486 V, V$_{DS}$ = 9.07 V, g$_m$ = 3.29 mS.

@s 6
**Hartley oscillator.** The tank circuit consists of a capacitor C in parallel with **two inductors L$_1$ and L$_2$ in series; the junction (tap) is at a.c. ground**. Feedback is taken from the inductor tap: the voltage across L$_2$ is applied to the base and, since the tap is grounded, it is 180° out of phase with the collector voltage across L$_1$. The CE amplifier gives another 180°, so the loop phase is 0°.


```figure caption="Hartley oscillator."
fig,ax=ckt_canvas(5.2,3.6,xlim=(-0.6,8.6),ylim=(-1.2,7.6))
terminal(ax,(6.6,7.2)); label(ax,(7.0,7.2),"+V$_{CC}$",ha="left",size=8.6)
bj=bjt(ax,4.0,2.4)
node(ax,(5.0,4.6))
wire(ax,[(4.6,3.5),(4.6,4.6),(5.0,4.6)])
ind(ax,(5.0,4.6),(3.2,4.6),"L$_1$",side=1,body=1.1); ind(ax,(3.2,4.6),(1.4,4.6),"L$_2$",side=1,body=1.1)
wire(ax,[(5.0,4.6),(5.0,5.7),(4.2,5.7)]); cap(ax,(4.2,5.7),(2.2,5.7),"C",side=1); wire(ax,[(2.2,5.7),(1.4,5.7),(1.4,4.6)])

wire(ax,[(1.4,4.6),(1.4,2.4),bj["B"]])
wire(ax,[(3.2,4.6),(3.2,3.9)]); node(ax,(3.2,4.6)); gnd(ax,(3.2,3.9))
wire(ax,[(5.0,4.6),(6.6,4.6)]); res(ax,(6.6,4.6),(6.6,6.6),"RFC",side=1,off=0.5,body=0.7); wire(ax,[(6.6,6.6),(6.6,7.2)])
wire(ax,[bj["E"],(4.6,0.7)]); res(ax,(4.6,0.7),(4.6,-0.4),"R$_E$",side=1,off=0.5,body=0.5); gnd(ax,(4.6,-0.4))
label(ax,(5.6,2.4),"f$_o$ = 1/(2π√(L$_{eq}$C$_{eq}$))",ha="left",size=7.4)
```


The tank resonates when the total reactance in the loop is zero: with mutual inductance M between the coils the equivalent inductance is L$_{eq}$ = L$_1$ + L$_2$ + 2M, so

$$\begin{gathered}f_o=\frac{1}{2\pi\sqrt{(L_1+L_2+2M)\,C}} \\ (\text{for no mutual coupling, }M=0:\ f_o=\frac{1}{2\pi\sqrt{(L_1+L_2)C}})\end{gathered}$$

Derivation (M = 0): in the tank the current circulates through C and L$_1$+L$_2$; resonance is when ωL$_{eq}$ = 1/(ωC), that is ω² = 1/(L$_{eq}$C). The feedback fraction is β = −L$_2$/L$_1$, and the amplifier gain magnitude is A = h$_{fe}$R$_C$/h$_{ie}$ (approximately), so oscillation needs

$$\begin{gathered}|A\beta|\ge1\ \ \Rightarrow\ \ h_{fe}\ge\frac{L_1}{L_2}\ (\text{BJT, light load}) \\ \left(\text{FET: }g_m r_d\ge \frac{L_1}{L_2}\right)\end{gathered}$$

Frequency is varied with a variable capacitor C. Used in radio receivers as local oscillator (about 1 MHz to 100 MHz). *Example:* L$_1$ = 1 mH, L$_2$ = 1 mH, C = 100 pF: f$_o$ = 1/(2π√(2×10⁻³ × 10⁻¹⁰)) = 356 kHz.

@s 7
**Class A tuned amplifier (single tuned).** A CE amplifier has a parallel LC tank (L with its series resistance, C) as the collector load. At resonance the tank impedance is a pure and large resistance, so the gain is maximum; away from resonance the tank impedance falls, so the amplifier is selective (used in radio and IF amplifiers).


```figure caption="Class A tuned amplifier and its frequency response."
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
```


Resonance frequency f$_o$ = 1/(2π√(LC)). Near resonance the tank impedance is

$$\begin{gathered}Z(f)=\frac{R_p}{1+jQ\left(\dfrac{f}{f_o}-\dfrac{f_o}{f}\right)} \\ Q=\frac{R_p}{\omega_oL}=\omega_oCR_p\end{gathered}$$

where R$_p$ is the equivalent parallel resistance (the coil loss resistance in parallel with r$_o$ and the load). With a transconductance g$_m$ the voltage gain is A$_v$ = −g$_m$Z, so

$$\begin{gathered}|A_v|=\frac{A_{max}}{\sqrt{1+Q^2\left(\dfrac{f}{f_o}-\dfrac{f_o}{f}\right)^2}} \\ A_{max}=g_mR_p\end{gathered}$$

**3 dB bandwidth.** The gain drops to A$_{max}$/√2 when Q(f/f$_o$ − f$_o$/f) = ±1. Solving the two quadratics f² ∓ (f$_o$/Q)f − f$_o^2$ = 0 for the positive roots:

$$\begin{gathered}f_{1,2}=f_o\left[\sqrt{1+\frac{1}{4Q^2}}\mp\frac{1}{2Q}\right]\ \Rightarrow\ f_2-f_1=\frac{f_o}{Q} \\ f_1f_2=f_o^2\end{gathered}$$

$$\boxed{\ BW=f_2-f_1=\frac{f_o}{Q}\ }$$

so a higher Q gives a narrower bandwidth and a sharper response (for Q > 10, f$_{1,2}$ ≈ f$_o$ ∓ BW/2). *Example:* f$_o$ = 1 MHz, Q = 50 gives BW = 20 kHz; with a heavy load, R$_p$ and hence Q fall and the bandwidth rises.

@s 8
**Differential amplifier with an active load.** Q$_1$, Q$_2$ form the differential pair biased by the tail current I$_{EE}$ (I$_{E1}$ = I$_{E2}$ = I$_{EE}$/2); both have the transconductance g$_m$ = I$_C$/V$_T$. In place of the resistors R$_C$, the collectors are loaded by a pnp **current mirror** (Q$_3$ diode-connected, Q$_4$ output). The output is taken from the collector of Q$_2$. Let v$_d$ = v$_1$ − v$_2$.


```figure caption="Differential amplifier with an active (current-mirror) load."
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
```


*(a) Passive (resistor) load, single-ended output.* By symmetry a differential input v$_d$ divides equally: the collector current of Q$_2$ changes by g$_m$(v$_d$/2) and that of Q$_1$ by −g$_m$(v$_d$/2). The output at one collector with the load R (the total resistance at the output node, e.g. R$_C$ ∥ r$_{o2}$):

$$v_o=-g_m\frac{v_d}{2}R\ \Rightarrow\ A_d(\text{passive})=\frac{v_o}{v_d}=\frac{g_mR}{2}$$

*(b) Active load.* The change of collector current of Q$_1$ is −g$_m$v$_d$/2 (it flows into the diode Q$_3$) and is **mirrored by Q$_4$ as an equal and opposite current, i.e. +g$_m$v$_d$/2 into the output node**, while Q$_2$ adds +g$_m$v$_d$/2 itself. Both halves of the differential signal therefore appear at the single output, and the output current is

$$i_o=\frac{g_mv_d}{2}+\frac{g_mv_d}{2}=g_mv_d$$

The resistance at the output node is R$_o$ = r$_{o2}$ ∥ r$_{o4}$ = R (the same resistance as in (a)). Hence

$$A_d(\text{active})=\frac{v_o}{v_d}=g_m\,(r_{o2}\parallel r_{o4})=g_mR$$

*Comparison for the same output resistance R:*

$$\frac{A_d(\text{active})}{A_d(\text{passive})}=\frac{g_mR}{g_mR/2}=2$$

So the single-ended gain with an active load is **twice** that with a passive load (the mirror recovers the half of the signal that the passive load wastes in the other collector). In addition the active load gives a very large R (r$_o$ ≈ 100 kΩ or more) so that gains of several thousand are possible with no large resistors and no large voltage drop.

@s 9
**Series-fed class A amplifier.** The load R$_C$ is connected in series with the collector from V$_{CC}$ and the transistor is biased (R$_B$) at the middle of the d.c. load line: I$_{CQ}$ = V$_{CC}$/(2R$_C$), V$_{CEQ}$ = V$_{CC}$/2. The same resistor R$_C$ (the load) carries the d.c. current.

$$\begin{gathered}
P_{dc}=V_{CC}I_{CQ}\quad(\text{input power from the supply}) \\
P_{ac}=\frac{V_{CE(p\text{-}p)}\,I_{C(p\text{-}p)}}{8}=\frac{I_{C(p\text{-}p)}^2R_C}{8}\ \ \left(\text{with }V_{CE(p\text{-}p)}=I_{C(p\text{-}p)}R_C\right)
\end{gathered}$$

$$\eta=\frac{P_{ac}}{P_{dc}}\times100=\frac{V_{CE(p\text{-}p)}I_{C(p\text{-}p)}/8}{V_{CC}I_{CQ}}\times100$$

For the maximum symmetrical swing: V$_{CE(p\text{-}p)}$ = V$_{CC}$ (V$_{CE}$ from 0 to V$_{CC}$) and I$_{C(p\text{-}p)}$ = 2I$_{CQ}$ = V$_{CC}$/R$_C$, so

$$P_{ac(max)}=\frac{V_{CC}\cdot 2I_{CQ}}{8}=\frac{V_{CC}I_{CQ}}{4}\ \ \Rightarrow\ \ \eta_{max}=\frac{V_{CC}I_{CQ}/4}{V_{CC}I_{CQ}}=\mathbf{25\ percent}$$

In general η = 25 (V$_{pp}$/V$_{CC}$)² percent, where V$_{pp}$ = V$_{CE(max)}$ − V$_{CE(min)}$. The poor efficiency is because the d.c. current flows through the load (a constant power V$_{CC}I_{CQ}$ is drawn even without a signal), so at most one quarter of it can be converted to a.c. power.

@s 10
Given V$_{CC}$ = 30 V and R$_L$ = 16 Ω. For the class B stage the largest swing is V$_p$ = V$_{CC}$, so

$$\begin{gathered}
I_{p(max)}=\frac{V_{CC}}{R_L}=\frac{30}{16}=1.875\ \text{A},\qquad I_{dc}=\frac{2I_p}{\pi}=1.194\ \text{A}\\
\textbf{Maximum input power:}\quad P_{in(max)}=V_{CC}I_{dc}=\frac{2V_{CC}^2}{\pi R_L}=\frac{2(30)^2}{\pi(16)}=\mathbf{35.81\ W}\\
\textbf{Maximum output power:}\quad P_{o(max)}=\frac{V_{CC}^2}{2R_L}=\frac{30^2}{2(16)}=\mathbf{28.125\ W}\\
\eta_{max}=\frac{P_o}{P_{in}}=\frac{\pi}{4}=78.5\ \text{percent}
\end{gathered}$$

**Maximum power dissipation in the transistors.** For any peak voltage V$_p$ the dissipation of the two transistors is P$_D$ = P$_{in}$ − P$_o$ = 2V$_{CC}$V$_p$/(πR$_L$) − V$_p^2$/(2R$_L$). Differentiating with respect to V$_p$ and equating to zero gives V$_p$ = 2V$_{CC}$/π = 19.10 V (I$_p$ = 1.194 A), at which

$$\begin{gathered}P_{D(max)}=\frac{2V_{CC}^2}{\pi^2R_L}=\frac{2(30)^2}{\pi^2(16)}=\mathbf{11.40\ W}\ \ \text{(both transistors)} \\ \text{i.e. }5.70\ \text{W per transistor}\end{gathered}$$

*(At the full-swing point V$_p$ = V$_{CC}$ the dissipation is P$_{in}$ − P$_o$ = 35.81 − 28.12 = 7.68 W, lower than P$_{D(max)}$.)* So each transistor must be rated for at least 5.7 W.

@s 11
**555 timer as an astable multivibrator.** Pins 2 (trigger) and 6 (threshold) are joined and connected to the capacitor C; R$_A$ goes from V$_{CC}$ to the discharge pin 7 and R$_B$ from pin 7 to C. Internally three equal 5 kΩ resistors fix the comparator levels V$_{CC}$/3 (lower trigger level) and 2V$_{CC}$/3 (upper threshold level).


```figure caption="555 timer astable multivibrator and its waveforms."
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
```


*Charging (output HIGH).* The discharge transistor is off and C charges through R$_A$ + R$_B$ toward V$_{CC}$ from V$_{CC}$/3 up to 2V$_{CC}$/3. With v$_C$(t) = V$_{CC}$ − (V$_{CC}$ − V$_{CC}$/3)e$^{-t/τ_1}$ and τ$_1$ = (R$_A$+R$_B$)C, set v$_C$ = 2V$_{CC}$/3:

$$\frac{2V_{CC}}{3}=V_{CC}-\frac{2V_{CC}}{3}e^{-T_H/\tau_1}\ \Rightarrow\ e^{-T_H/\tau_1}=\frac12\ \Rightarrow\ T_H=0.693\,(R_A+R_B)\,C$$

*Discharging (output LOW).* At 2V$_{CC}$/3 the upper comparator resets the flip-flop; the output goes low and pin 7 grounds, so C discharges through R$_B$ only: v$_C$(t) = (2V$_{CC}$/3)e$^{-t/τ_2}$ with τ$_2$ = R$_BC$ until v$_C$ = V$_{CC}$/3:

$$\frac{V_{CC}}{3}=\frac{2V_{CC}}{3}e^{-T_L/\tau_2}\ \Rightarrow\ T_L=0.693\,R_B\,C$$

*Period, frequency and duty cycle.*

$$\begin{gathered}
T=T_H+T_L=0.693\,(R_A+2R_B)\,C \\
f=\frac{1}{T}=\frac{1.44}{(R_A+2R_B)\,C} \\
D=\frac{T_H}{T}=\frac{R_A+R_B}{R_A+2R_B}\ (>50\ \text{percent})
\end{gathered}$$

The frequency is independent of V$_{CC}$ because both thresholds are proportional to V$_{CC}$. *Example:* R$_A$ = 1 kΩ, R$_B$ = 10 kΩ, C = 0.1 µF: f = 1.44/(21 kΩ × 0.1 µF) = 686 Hz, T$_H$ = 0.693 × 11 k × 0.1 µ = 0.762 ms, T$_L$ = 0.693 ms, D = 52.4 percent. A duty cycle of 50 percent or less needs a diode across R$_B$.

@s 12
**Short-circuit / overload (current-limit) protection.** A small sense resistor R$_{SC}$ is placed in series with the load and a second transistor Q$_2$ is connected with its base-emitter across R$_{SC}$ and its collector at the base of the pass transistor Q$_1$.


```figure caption="Series transistor regulator with a short-circuit (current-limiting) protection transistor Q$_2$."
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
```


*Normal load.* The load current I$_L$ flows through R$_{SC}$ and produces V$_{R_{SC}}$ = I$_LR_{SC}$ < 0.5 V, so Q$_2$ is off and the regulator works as above. *Overload or short circuit.* When I$_L$ rises until I$_LR_{SC}$ ≈ V$_{BE2}$ (≈ 0.6 to 0.7 V), Q$_2$ conducts and **diverts the base current of Q$_1$** (taking it from the R$_1$/Zener node), so the base drive of Q$_1$ falls and the output current is held at

$$I_{L(max)}=I_{SC}\approx\frac{V_{BE2}}{R_{SC}}=\frac{0.65\ \text{V}}{R_{SC}}$$

*Design:* for I$_{L(max)}$ = 1 A, R$_{SC}$ = 0.65 Ω (≈ 0.68 Ω, rated at least I²R = 0.7 W); the output voltage falls as the load resistance falls but the current cannot exceed I$_{SC}$, so the pass transistor does not burn out (its dissipation in a short is P$_D$ ≈ V$_i$I$_{SC}$, which the heat sink must withstand; foldback limiting reduces this). Practical designs also include R$_{SC}$ ≈ 0.5 Ω-class values and a fuse.

**Design with the LM317.** The LM317 keeps a constant reference of **V$_{ref}$ = 1.25 V** between its OUT and ADJ terminals, so the current through R$_1$ is fixed at 1.25/R$_1$ and the same current (plus the small adjust current I$_{ADJ}$ ≈ 50 µA) flows through R$_2$:

$$V_o=V_{ref}\left(1+\frac{R_2}{R_1}\right)+I_{ADJ}R_2\ \approx\ 1.25\left(1+\frac{R_2}{R_1}\right)$$


```figure caption="Adjustable regulator with the LM317."
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
```


*Choice of R$_1$.* The regulator needs a minimum load current of 3.5 to 10 mA, so R$_1$ = 1.25 V/5.2 mA ≈ **240 Ω** (standard value; 120 Ω to 240 Ω is the usual range).

*Value of R$_2$ for the two ends of the range* (R$_2$ = R$_1$(V$_o$/1.25 − 1)):

$$\begin{gathered}
V_{o(min)}=5\ \text{V}:\quad R_{2(min)}=240\left(\frac{5}{1.25}-1\right)=720\ \Omega \\
V_{o(max)}=15\ \text{V}:\quad R_{2(max)}=240\left(\frac{15}{1.25}-1\right)=2640\ \Omega
\end{gathered}$$

So R$_2$ must be variable from 720 Ω to 2640 Ω. Use a **fixed resistor of 720 Ω in series with a 2000 Ω potentiometer** (the fixed part sets the minimum voltage): R$_2$ varies from 720 Ω to 2720 Ω, giving V$_o$ from 1.25(1+720/240) = 5.00 V to 1.25(1+2720/240) = 15.42 V, which covers the required 5 to 15 V (the pot is trimmed to stop at 15 V).

*Other components.* C$_1$ = 0.1 µF at the input (when the regulator is far from the filter capacitor) and C$_2$ = 1 µF tantalum (or 10 µF) at the output for stability and transient response; a diode across the regulator protects against the discharge of C$_2$ into the output when the input is shorted. The unregulated input must satisfy V$_{in}$ ≥ V$_{o(max)}$ + 3 V (dropout), i.e. V$_{in}$ ≈ 18 V (up to the 40 V maximum differential), and the regulator delivers up to 1.5 A with a heat sink (P$_D$ = (V$_{in}$ − V$_o$)I$_o$). Line and load regulation are about 0.01 percent per volt and 0.1 percent.

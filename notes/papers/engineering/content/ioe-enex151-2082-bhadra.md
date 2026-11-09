---
file: NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-ENEX151-2082-Bhadra.pdf
subject: Electronic Device and Circuits
level: BE · Year I / Part II
code: ENEX 151
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
What is the significance of β-independency in a voltage divider biasing circuit? Design a β-independent voltage divider bias circuit for the given parameters: V$_{CC}$ = 15 V, I$_E$ = 1 mA and β = 100. [[1+5]]

@q 2
Explain the role of coupling capacitors in amplifier circuits. Draw the small signal equivalent circuit of a common emitter amplifier circuit and find its input impedance, output impedance and voltage gain. [[2+5]]

@q 3
Describe the construction and working principle of n-channel JFET with the help of characteristic curves and mathematical expressions. [[6]]

@q 4
Find I$_D$ and V$_{DS}$ for the circuit shown in the figure below. Given parameters are: V$_t$ = 1 V and K = 0.48 mA/V$^2$. [[7]]

```figure caption="Question 4: n-channel enhancement MOSFET, V$_{DD}$ = +10 V, R$_1$ = R$_2$ = 11 MΩ, R$_D$ = R$_S$ = 6 kΩ."
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"+10 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"11 MΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"11 MΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
m=mosfet(ax,2.0,3.2,kind="n",mode="enh")
wire(ax,[m["D"],(4.0,4.3)])
wire(ax,[m["S"],(4.0,2.1)])
res(ax,(5.0,6.6),(5.0,4.9),"6 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"6 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"V$_t$ = 1 V,  K = 0.48 mA/V$^2$",ha="left",size=8)
```

@q 5
State Barkhausen criteria for sinusoidal oscillation. Explain the working principle of RC phase shift oscillator with necessary expression and circuit diagram. [[6]]

@q 6
With a neat circuit diagram and necessary mathematical expressions, explain the operation of Widlar current source. What is the advantage of Widlar current source over simple current source? [[5+2]]

@q 7
Draw the circuit diagram of transformer coupled Class B amplifier. Determine the condition for minimum efficiency of Class B amplifier. [[6]]

@q 8
Define crossover distortion in a class B amplifier and explain how class AB operation can be used to eliminate it. [[6]]

@q 9
Explain the working principle of a series transistor voltage regulator, accompanied by short-circuit/overload protection. [[5]]

@q 10
Design a 10-25 V variable DC voltage regulator using LM317 IC. [[4]]
<!-- SOLUTIONS -->

@s 1
**Significance of β-independence.** The current gain β of a transistor is not a fixed number: it differs by a factor of 2 to 3 between two transistors of the same type, and it changes with temperature and with the collector current. If the Q-point (I$_C$, V$_{CE}$) depended on β, every replaced transistor or every temperature change would move the operating point towards saturation or cut-off, causing distortion and clipping. A **β-independent (stiff, voltage-divider) bias** makes I$_C$ ≈ (V$_B$ − V$_{BE}$)/R$_E$, which depends only on the stable resistors and the supply, so the Q-point is almost fixed, the stage is thermally stable (the emitter resistor gives d.c. negative feedback) and the gain, which depends on r$_e$ = 26 mV/I$_E$, is predictable. The stability factor S = ΔI$_C$/ΔI$_{CO}$ ≈ 1 + R$_B$/R$_E$ is small.

**Design rules for a β-independent (stiff) voltage-divider bias.** Choose (i) V$_E$ = V$_{CC}$/10 so that V$_{BE}$ variations are small compared with V$_E$, (ii) V$_{CE}$ ≈ V$_{CC}$/2 for maximum undistorted swing, (iii) the divider current much larger than I$_B$, which is ensured by R$_2$ ≤ 0.1βR$_E$ (stiff divider; then V$_B$ is nearly independent of β).

Given: V$_{CC}$ = 15 V, I$_E$ ≈ I$_C$ = 1 mA, β = 100.

$$\begin{gathered}
V_E=\frac{V_{CC}}{10}=1.50\ \text{V}, \qquad R_E=\frac{V_E}{I_E}=\frac{1.50}{1\ \text{mA}}=1.50\ \text{k}\Omega \\
V_B=V_E+V_{BE}=1.50+0.7=2.20\ \text{V} \\
R_2\le 0.1\beta R_E=0.1(100)(1.50\ \text{k}\Omega)=15.00\ \text{k}\Omega\ \ \Rightarrow\ \ R_2=15.00\ \text{k}\Omega \\
\frac{R_2}{R_1+R_2}V_{CC}=V_B\ \Rightarrow\ R_1=R_2\left(\frac{V_{CC}}{V_B}-1\right)=87.27\ \text{k}\Omega \\
R_C=\frac{V_{CC}-V_E-V_{CE}}{I_C}=\frac{15-1.50-7.50}{0.990\ \text{mA}}=6.06\ \text{k}\Omega
\end{gathered}$$

Use the nearest standard values: R$_1$ ≈ 87 kΩ, R$_2$ ≈ 15 kΩ, R$_E$ ≈ 1.50 kΩ, R$_C$ ≈ 6.1 kΩ.

*Check of stiffness.* Thevenin resistance R$_B$ = R$_1$ ∥ R$_2$ = 12.80 kΩ, and I$_B$ = I$_C$/β = 9.9 µA. The voltage lost in R$_B$ is I$_B$R$_B$ = 0.13 V, only a small fraction of V$_B$; so I$_E$ = (V$_{BB}$ − V$_{BE}$)/(R$_E$ + R$_B$/(β+1)) changes by about 4.0 percent when β changes from β to 2β, i.e. the Q-point is practically β-independent. With I$_C$ = 0.990099 mA the quiescent voltages are V$_{CE}$ = 7.50 V and V$_C$ = 9.00 V (transistor in the active region).

@s 2
**Role of the coupling capacitors.** A coupling capacitor (C$_1$ at the input, C$_2$ at the output) is connected in series with the signal path. Its reactance X$_C$ = 1/(2πfC) is small at the signal frequency so the **a.c. signal passes**, while it **blocks d.c.** Hence the d.c. bias point of the stage is not disturbed by the source or by the next stage (or load), and the stages can be cascaded. They are chosen so that X$_C$ ≤ 0.1 × (the resistance seen) at the lowest frequency; together with the resistances they set the **lower cut-off frequency** f$_L$ = 1/(2π R C).

**Small-signal equivalent of the common-emitter amplifier** (voltage-divider bias, emitter bypassed so that R$_E$ is short-circuited for a.c.; capacitors short, V$_{CC}$ at a.c. ground; R$_B$ = R$_1$∥R$_2$). In the hybrid-π model r$_π$ = β r$_e$ and the collector source is g$_m$v$_{be}$ = βi$_b$ in parallel with r$_o$:


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


(The figure includes an un-bypassed R$_E$; for a bypassed emitter R$_E$ = 0.) For the bypassed case:

$$\begin{gathered}
Z_i = R_B \parallel r_\pi = R_1\parallel R_2\parallel \beta r_e \\
Z_o = R_C \parallel r_o \approx R_C \\
v_o=-\beta i_b\,(r_o\parallel R_C\parallel R_L),\quad v_i=i_b r_\pi \ \Rightarrow\ A_v=-\frac{\beta (R_C\parallel R_L)}{\beta r_e}=-\frac{R_C\parallel R_L}{r_e}
\end{gathered}$$

The negative sign is the **180° phase shift** between v$_o$ and v$_i$. Without the bypass capacitor the gain falls to A$_v$ ≈ −(R$_C$∥R$_L$)/(r$_e$ + R$_E$) and Z$_i$ rises to R$_B$∥β(r$_e$+R$_E$). Example: for the design of Question 1 (I$_E$ = 1 mA, r$_e$ = 26 Ω, β = 100, R$_C$ = 6.2 kΩ, R$_B$ = 87 kΩ∥15 kΩ = 12.8 kΩ): Z$_i$ = 12.8 kΩ ∥ 2.6 kΩ ≈ 2.2 kΩ, Z$_o$ ≈ 6.2 kΩ and A$_v$ ≈ −6.2 kΩ/26 Ω ≈ −238.

@s 3
**Construction.** An n-channel JFET is a bar of n-type silicon with an ohmic contact at each end: the **source (S)** and the **drain (D)**. Two heavily doped p-type regions are diffused on both sides of the bar and joined together as the **gate (G)**. The n-region between the two p-n junctions is the **channel** through which the majority carriers (electrons) flow from S to D. The gate-channel junctions are always **reverse biased** in operation, so the gate current is practically zero (I$_G$ ≈ pA) and the input resistance is very high.


```figure caption="n-channel JFET: structure, drain characteristics and transfer curve."
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
```


**Working principle.**
1. *V$_{GS}$ = 0, small V$_{DS}$:* the channel is wide; the drain current rises linearly with V$_{DS}$ (the channel acts as an ohmic resistor).
2. *V$_{GS}$ = 0, V$_{DS}$ increasing:* the reverse bias across the gate junctions is larger near the drain, so the depletion regions widen unequally and the channel narrows toward the drain. At **V$_{DS}$ = V$_P$** (pinch-off voltage in magnitude) the two depletion regions almost touch. Beyond this the current stops increasing and stays at **I$_{DSS}$** (the saturation or pinch-off region); the channel is pinched but carriers still cross it, so I$_D$ is nearly independent of V$_{DS}$ and the JFET behaves as a constant-current source.
3. *V$_{GS}$ negative:* the additional reverse bias widens the depletion layers, narrows the channel, and the pinch-off occurs at the lower voltage V$_{DS(sat)}$ = V$_{GS}$ − V$_P$ (that is, V$_{DS}$ = V$_P$ − |V$_{GS}$|). I$_D$ decreases. At **V$_{GS}$ = V$_P$** (negative, for example −4 V) the channel is completely closed and I$_D$ = 0 (cut-off).

**Characteristics.** *Drain characteristics* (I$_D$ against V$_{DS}$ for steps of V$_{GS}$) have an ohmic region (V$_{DS}$ < V$_{GS}$ − V$_P$), a saturation (constant-current or pinch-off) region used for amplification, and a breakdown region at high V$_{DS}$. The *transfer characteristic* is a parabola from V$_P$ to 0.

**Mathematical expressions.**

$$\begin{gathered}
\text{Shockley equation (saturation):}\quad I_D=I_{DSS}\left(1-\frac{V_{GS}}{V_P}\right)^2,\qquad V_P\le V_{GS}\le 0 \\
\text{Ohmic region:}\quad I_D\approx\frac{2I_{DSS}}{V_P^2}\left[(V_{GS}-V_P)V_{DS}-\frac{V_{DS}^2}{2}\right]\ \ (V_{DS}<V_{GS}-V_P) \\
\text{Transconductance:}\quad g_m=\frac{\partial I_D}{\partial V_{GS}}=g_{m0}\left(1-\frac{V_{GS}}{V_P}\right),\qquad g_{m0}=\frac{2I_{DSS}}{|V_P|} \\
\text{Drain resistance:}\quad r_d=\frac{\Delta V_{DS}}{\Delta I_D}\bigg|_{V_{GS}},\qquad \text{amplification factor }\mu=g_m r_d
\end{gathered}$$

@s 4
The enhancement MOSFET is biased by the voltage divider (V$_{DD}$ = 10 V, R$_1$ = R$_2$ = 11 MΩ) with R$_D$ = R$_S$ = 6 kΩ.


```figure caption="prob_emos"
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"+10 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"11 MΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"11 MΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
m=mosfet(ax,2.0,3.2,kind="n",mode="enh")
wire(ax,[m["D"],(4.0,4.3)])
wire(ax,[m["S"],(4.0,2.1)])
res(ax,(5.0,6.6),(5.0,4.9),"6 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"6 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"V$_t$ = 1 V,  K = 0.48 mA/V$^2$",ha="left",size=8)
```


**Solution** (R in kΩ, I in mA, K in mA/V²). Gate current is zero, so

$$V_G=\frac{R_2}{R_1+R_2}V_{DD}=\frac{11000}{11000+11000}(10)=5.00\ \text{V}$$

For the enhancement MOSFET in saturation I$_D$ = K(V$_{GS}$ − V$_t$)² with V$_{GS}$ = V$_G$ − I$_D$R$_S$ = 5.00 − 6 I$_D$:

$$I_D=0.48\,(5.00-6\,I_D-1)^2=0.48\,(4.00-6\,I_D)^2$$

$$17.28\,I_D^2-24.0400\,I_D+7.6800=0\ \ \Rightarrow\ \ I_D=0.497\ \text{mA}\ \ \text{or}\ \ 0.894\ \text{mA}$$

The larger root gives V$_{GS}$ = 5.00 − 6(0.894) = -0.36 V, which is below V$_t$ (transistor cut off), so it is rejected. Hence

$$\begin{gathered}
I_D=0.497\ \text{mA}\ (\approx 497\ \mu\text{A})\\
V_{GS}=5.00-6(0.497)=2.018\ \text{V}\ (>V_t=1\ \text{V})\\
V_{DS}=V_{DD}-I_D(R_D+R_S)=10-0.497(6+6)=4.035\ \text{V}
\end{gathered}$$

*Check:* V$_{DS}$ = 4.035 V > V$_{GS}$ − V$_t$ = 1.018 V, so the device is in saturation and the square-law is valid.

@s 5
**Barkhausen criteria.** An amplifier with gain A and a feedback network with feedback factor β (positive feedback) sustains oscillation at a frequency f$_o$ if the loop gain Aβ satisfies

$$\begin{gathered}
|A\beta|=1 \quad(\text{magnitude condition: the loop gain is unity}) \\
\angle A\beta = 0^\circ\ \text{or}\ 360^\circ\quad(\text{phase condition: total phase shift around the loop is zero})
\end{gathered}$$

The closed-loop gain A$_f$ = A/(1 − Aβ) becomes infinite, so an output exists without any input. Oscillations start from noise when |Aβ| is slightly greater than 1 initially; the amplitude then limits (non-linearity or an amplitude-stabilising element) so that |Aβ| settles at 1.

**RC phase-shift oscillator.** An inverting amplifier (phase shift 180°) is followed by a feedback network of **three identical RC sections** which supplies a further 180° (60° per section) at one frequency, so the total phase around the loop is 360°.


```figure caption="RC phase-shift oscillator (three sections)."
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
```


For the three-section network (op-amp virtual ground at the end, the last R is the input resistor) the analysis of the loop equations gives the transfer function

$$\begin{gathered}\frac{v_f}{v_o}=\frac{1}{1-5\alpha^2-j(6\alpha-\alpha^3)} \\ \alpha=\frac{1}{\omega RC}\end{gathered}$$

The phase shift is 180° when the imaginary part is zero: 6α − α³ = 0, so α² = 6:

$$f_o=\frac{1}{2\pi RC\sqrt{6}}$$

At this frequency the real part is 1 − 5(6) = −29, so |β| = 1/29 and the amplifier must provide at least A$_v$ = 29 in magnitude (negative, inverting):

$$|A_v|=\frac{R_f}{R}\ \ge\ 29\ \ \Rightarrow\ \ R_f\ge 29R$$

(for a BJT version, h$_{fe}$ ≥ 29 + 23R$_C$/R + 4R/R$_C$ ≥ 44.5). Each section is loaded by the next, so the three sections are not independent. The circuit is simple and cheap and used for audio frequencies; its output is a good sine wave but its frequency is not easily varied (three components must be changed together). *Example:* R = 10 kΩ, C = 10 nF gives f$_o$ = 1/(2π × 10⁴ × 10⁻⁸ × 2.449) = 650 Hz, R$_f$ ≥ 290 kΩ.

@s 6
**Widlar current source.** It is a current mirror with a resistor R$_E$ added in the emitter of the output transistor Q$_2$; this allows **small output currents (µA) with modest resistors**.


```figure caption="Widlar current source."
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
```


*Relation between I$_O$ and I$_{REF}$.* Q$_1$ is diode-connected and the bases are common, so V$_{BE1}$ = V$_{BE2}$ + I$_{E2}$R$_E$. Using V$_{BE}$ = V$_T$ ln(I$_C$/I$_S$) for identical transistors:

$$\begin{gathered}V_{BE1}-V_{BE2}=V_T\ln\frac{I_{REF}}{I_O}=I_OR_E\ \ \Rightarrow\ \ R_E=\frac{V_T}{I_O}\ln\frac{I_{REF}}{I_O} \\ (\text{taking }I_{E2}\approx I_O)\end{gathered}$$

and I$_{REF}$ = (V$_{CC}$ − V$_{BE1}$)/R. *Example:* I$_{REF}$ = 1 mA, I$_O$ = 10 µA: R$_E$ = (25.85 mV/10 µA) ln(100) = 11.9 kΩ (a simple mirror would need a 100:1 ratio of device areas or resistors for the same current ratio).

*Output resistance.* Looking into the collector of Q$_2$ (small-signal model, with r$_o$ the transistor output resistance, g$_m$ = I$_O$/V$_T$, and r$_{π2}$ = β/g$_m$): the emitter resistance seen by Q$_2$ is R$_E$ in parallel with r$_{π}$ and the diode resistance 1/g$_{m1}$ of Q$_1$ (through the base node), i.e. R$_E$' = R$_E$ ∥ (r$_π$ + 1/g$_{m1}$ in the base branch) ≈ R$_E$ ∥ r$_π$ (since 1/g$_{m1}$ is small). A resistor R$_E$' in the emitter raises the output resistance (current-series feedback):

$$R_o=\frac{v_x}{i_x}\approx r_o\left[1+\frac{g_m R_E'}{1+R_E'/r_\pi}\right]\ \approx\ r_o\left[1+g_m\,(R_E\parallel r_\pi)\right]$$

For R$_E$ ≫ r$_π$ this tends to r$_o$(1 + β) — much larger than r$_o$ of the simple mirror (R$_o$ = r$_o$). Hence the Widlar source (i) gives small currents with small resistors (small chip area), (ii) has a high output resistance, so the output current is almost independent of the load voltage, and (iii) the output current is less sensitive to supply variations, but it has a temperature dependence proportional to T (I$_O$ is a PTAT-type current).

**Advantage over the simple current source.** To obtain a small output current such as 10 µA from I$_{REF}$ = 1 mA a simple mirror needs a 100:1 resistor ratio (or a very large R of about 1 MΩ, which takes a large area on a chip); the Widlar source needs only R$_E$ ≈ 12 kΩ. It also has a **much higher output resistance** (r$_o$[1 + g$_m$(R$_E$∥r$_π$)] instead of r$_o$), so the output current is independent of the load, and I$_O$ is less sensitive to supply voltage variations and to base-current error.

@s 7
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

@s 8
**Crossover distortion.** In a class B push-pull stage each transistor conducts only when its base-emitter voltage exceeds the cut-in voltage (about 0.5 to 0.7 V for silicon). Near the zero crossing of the input, when −0.7 V < v$_i$ < +0.7 V, **neither transistor conducts**, so the output stays at zero for that interval (a dead band). The output waveform is therefore distorted at the point where the output passes from one transistor to the other: this is called **crossover distortion**. It is most serious for small signals and gives odd harmonics.


```figure caption="Crossover distortion in class B and its removal in class AB."
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
```


**Class AB operation removes it.** The two transistors are given a small forward bias (V$_{BE}$ slightly above cut-in) from two series diodes or a V$_{BE}$-multiplier connected between the bases (the diodes track the transistors with temperature and avoid thermal runaway), so each device has a small quiescent current I$_{CQ}$ and conducts for slightly more than 180° (180° < θ < 360°). The two transfer characteristics then overlap around the origin, and the sum of the two collector currents is linear through zero. The price is a small quiescent power dissipation, so the efficiency is between class A (50 percent) and class B (78.5 percent). In an actual stage a resistor R$_E$ of about 0.5 Ω in each emitter limits the quiescent current.

@s 9
**Discrete series regulator.** A pass transistor Q$_1$ (emitter follower) is in series with the load. A Zener diode D$_Z$ fed through R$_1$ gives a constant reference voltage V$_Z$ at the base:

$$V_o=V_Z-V_{BE1}$$

*Regulation action:* if the input rises (or the load current falls) V$_o$ tends to rise, V$_{BE1}$ = V$_Z$ − V$_o$ falls, I$_{B1}$ and hence the collector current fall, V$_{CE1}$ rises and takes up the extra input voltage, so V$_o$ returns almost to its old value. The load current is supplied through the transistor, so the Zener only has to supply I$_{B1}$ = I$_L$/(β+1), and the Zener current is made nearly independent of the load.

**Stability factor (line regulation) S$_V$ = ΔV$_o$/ΔV$_i$** for a constant load. A change ΔV$_i$ divides between R$_1$ and the dynamic resistance r$_z$ of the Zener (the base-looking resistance (β+1)(r$_e$+R$_L$) is very large and is in parallel with r$_z$, so it is neglected):

$$\Delta V_Z=\Delta V_i\,\frac{r_z}{R_1+r_z}$$

The emitter follows the base with the gain A$_v$ = R$_L$/(R$_L$ + r$_e$) ≈ 1 (ΔV$_{BE}$ ≈ r$_e$ΔI$_E$ is small), so

$$\Delta V_o=\Delta V_Z\,\frac{R_L}{R_L+r_e}\ \Rightarrow\ \boxed{\ S_V=\frac{\Delta V_o}{\Delta V_i}=\frac{r_z}{R_1+r_z}\cdot\frac{R_L}{R_L+r_e}\ \approx\ \frac{r_z}{R_1+r_z}\ }$$

Since r$_z$ ≪ R$_1$, S$_V$ is small (for example r$_z$ = 10 Ω, R$_1$ = 500 Ω gives S$_V$ = 10/510 = 0.0196, i.e. a 10 V change at the input produces only 0.2 V at the output); the smaller the stability factor, the better the regulation. Similarly the output resistance R$_{out}$ = r$_e$ + r$_z$∥R$_1$/(β+1) is very small (about 1 Ω), which gives a good load regulation. The percent regulation can be improved further by using a Darlington pass transistor, a constant-current source in place of R$_1$ or an error amplifier (see the improved circuit).

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

@s 10
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
V_{o(min)}=10\ \text{V}:\quad R_{2(min)}=240\left(\frac{10}{1.25}-1\right)=1680\ \Omega \\
V_{o(max)}=25\ \text{V}:\quad R_{2(max)}=240\left(\frac{25}{1.25}-1\right)=4560\ \Omega
\end{gathered}$$

So R$_2$ must be variable from 1680 Ω to 4560 Ω. Use a **fixed resistor of 1680 Ω in series with a 3000 Ω potentiometer** (the fixed part sets the minimum voltage): R$_2$ varies from 1680 Ω to 4680 Ω, giving V$_o$ from 1.25(1+1680/240) = 10.00 V to 1.25(1+4680/240) = 25.62 V, which covers the required 10 to 25 V (the pot is trimmed to stop at 25 V).

*Other components.* C$_1$ = 0.1 µF at the input (when the regulator is far from the filter capacitor) and C$_2$ = 1 µF tantalum (or 10 µF) at the output for stability and transient response; a diode across the regulator protects against the discharge of C$_2$ into the output when the input is shorted. The unregulated input must satisfy V$_{in}$ ≥ V$_{o(max)}$ + 3 V (dropout), i.e. V$_{in}$ ≈ 28 V (up to the 40 V maximum differential), and the regulator delivers up to 1.5 A with a heat sink (P$_D$ = (V$_{in}$ − V$_o$)I$_o$). Line and load regulation are about 0.01 percent per volt and 0.1 percent.

---
file: NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-ENEX151-2083-Baishakh.pdf
subject: Electronic Device and Circuits
level: BE · Year I / Part II
code: ENEX 151
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
Why BJT is bipolar and FET is unipolar? Design β-independent type DC biased common collector amplifier. Given parameters are: V$_{CC}$ = 20 V, I$_C$ = 2 mA, and β = 100. Use firm biasing method. [[1+5]]

@q 2
Explain the role of bypass capacitor in amplifier circuits. Draw the small signal equivalent circuit of a common base amplifier circuit and find its input impedance, output impedance and voltage gain. [[2+5]]

@q 3
Describe the construction and working principle of N Channel D-MOSFET with the help of characteristic curves and mathematical expressions. [[6]]

@q 4
Find I$_D$ and V$_{DS}$ for the given circuit. Given parameters: V$_P$ = −4 V and I$_{DSS}$ = 8 mA. [[7]]

```figure caption="Question 4: n-channel depletion MOSFET with voltage-divider bias, V$_{DD}$ = +16 V, R$_1$ = 2.1 MΩ, R$_2$ = 270 kΩ, R$_D$ = 2.4 kΩ, R$_S$ = 1.5 kΩ."
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"+16 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"2.1 MΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"270 kΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
m=mosfet(ax,2.0,3.2,kind="n",mode="dep")
wire(ax,[m["D"],(4.0,4.3)])
wire(ax,[m["S"],(4.0,2.1)])
res(ax,(5.0,6.6),(5.0,4.9),"2.4 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"1.5 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"V$_P$ = −4 V,  I$_{DSS}$ = 8 mA",ha="left",size=8)
```

@q 5
What is the main difference between RC and LC oscillator circuits in terms of application? Explain the operation of Wien Bridge Oscillator circuit with the help of circuit diagram and necessary mathematical expressions. [[1+5]]

@q 6
Explain how a base current compensation circuit reduces the difference between I0 and IREF in a simple current mirror circuit. [[5+2]]

@q 7
For a class B amplifier providing a 20 V peak signal to a 16 Ω load (speaker) and a power supply of V$_{CC}$ = 30 V, determine the input power, output power, and circuit efficiency. [[6]]

@q 8
Draw the circuit diagram and the characteristic curve of a transformer-coupled class A amplifier and derive its general and maximum efficiency. [[7]]

@q 9
Derive the expression for stability factor of a discrete-transistor series regulator. [[4]]

@q 10
Design a variable DC voltage regulator using the LM317 to output (3-15) volts. [[4]]
<!-- SOLUTIONS -->

@s 1
**Why a BJT is bipolar and a FET is unipolar.** In a BJT (npn or pnp) the collector current is carried by **both types of charge carriers**: electrons are injected from the emitter into the p-type base (minority carriers), and at the same time holes flow from the base into the emitter (this forms the base current). Both electrons and holes take part in conduction across the two p-n junctions, hence *bi-polar*. In a FET the current flows through a single semiconductor **channel** (n-type in an n-channel device, p-type in a p-channel device) between source and drain, and is carried **only by the majority carriers** of that channel (electrons in n-channel, holes in p-channel); the gate voltage only changes the width of the channel through the electric field. Only one polarity of carrier conducts, hence *uni-polar*.

| BJT | FET |
|---|---|
| Bipolar: electrons and holes | Unipolar: majority carriers only |
| Current controlled device (I$_B$ controls I$_C$) | Voltage controlled device (V$_{GS}$ controls I$_D$) |
| Low input resistance (kΩ) | Very high input resistance (MΩ to TΩ) |
| More temperature dependent (minority carriers, thermal runaway) | Less noisy and more thermally stable |

**Design of the β-independent common-collector (emitter-follower) amplifier by firm (voltage-divider) biasing.** The collector is tied directly to V$_{CC}$ (a.c. ground); the load resistor R$_E$ is in the emitter. For the largest symmetrical output swing the emitter is biased at half the supply, V$_E$ = V$_{CC}$/2 (so V$_{CE}$ = V$_{CC}$/2).

Given V$_{CC}$ = 20 V, I$_C$ = 2 mA, β = 100, so I$_E$ = I$_C$(β+1)/β = 2.020 mA.

$$\begin{gathered}
V_E=\frac{V_{CC}}{2}=10.0\ \text{V}, \qquad R_E=\frac{V_E}{I_E}=\frac{10.0}{2.020\ \text{mA}}=4.95\ \text{k}\Omega\ \approx\ 5.0\ \text{k}\Omega \\
V_B=V_E+V_{BE}=10.0+0.7=10.7\ \text{V} \\
R_2\le 0.1\beta R_E=0.1(100)(4.95\ \text{k}\Omega)=49.5\ \text{k}\Omega\ \ (\text{take }R_2=50\ \text{k}\Omega) \\
R_1=R_2\left(\frac{V_{CC}}{V_B}-1\right)=43.0\ \text{k}\Omega\ \ (\text{use }43\ \text{k}\Omega)
\end{gathered}$$

Because R$_2$ ≤ 0.1βR$_E$ the divider is stiff: V$_B$ ≈ V$_{CC}$R$_2$/(R$_1$+R$_2$) = 10.75 V irrespective of β, so I$_E$ = (V$_B$ − 0.7)/R$_E$ is set by the resistors alone (β-independent). Small-signal check: r$_e$ = 26 mV/I$_E$ = 12.9 Ω, voltage gain A$_v$ = R$_E$/(R$_E$+r$_e$) ≈ 0.997 ≈ 1, input resistance Z$_i$ = R$_1$∥R$_2$∥(β+1)(r$_e$+R$_E$) ≈ 22.0 kΩ. Coupling capacitors C$_1$, C$_2$ (about 10 µF) and no bypass capacitor are used.


```figure caption="Designed common-collector amplifier with voltage-divider bias."
fig,ax=ckt_canvas(4.8,3.4,xlim=(-1.4,8.4),ylim=(-0.8,7.8))
terminal(ax,(3.2,7.3)); label(ax,(3.7,7.3),"+V$_{CC}$",ha="left",size=8.6); wire(ax,[(3.2,7.3),(3.2,6.6)])
wire(ax,[(1.2,6.6),(3.2,6.6)]); node(ax,(3.2,6.6))
res(ax,(1.2,6.6),(1.2,3.8),"R$_1$",side=-1,off=0.5,body=0.9); node(ax,(1.2,3.8)); res(ax,(1.2,3.8),(1.2,0.4),"R$_2$",side=-1,off=0.5,body=0.9)
bj=bjt(ax,2.6,3.8); wire(ax,[(1.2,3.8),bj["B"]]); wire(ax,[bj["C"],(3.2,6.6)])
cap(ax,(-0.9,3.8),(0.1,3.8),"C$_1$",side=1,gap=0.2); wire(ax,[(0.1,3.8),(1.2,3.8)]); terminal(ax,(-1.3,3.8)); wire(ax,[(-1.3,3.8),(-0.9,3.8)]); label(ax,(-1.3,4.25),"v$_i$",size=8.6)
wire(ax,[bj["E"],(3.2,2.0)]); node(ax,(3.2,2.0)); res(ax,(3.2,2.0),(3.2,0.4),"R$_E$",side=1,off=0.5,body=0.9)
wire(ax,[(3.2,2.0),(4.4,2.0)]); cap(ax,(4.4,2.0),(5.6,2.0),"C$_2$",side=1,gap=0.2); wire(ax,[(5.6,2.0),(6.2,2.0)]); terminal(ax,(6.2,2.0)); label(ax,(6.6,2.0),"v$_o$",ha="left",size=8.6)
wire(ax,[(1.2,0.4),(3.2,0.4)]); gnd(ax,(2.2,0.4)); node(ax,(2.2,0.4))
```


@s 2
**Role of the bypass capacitor.** A bypass capacitor (for example C$_E$ across R$_E$ in a CE stage) offers a very small reactance X$_C$ = 1/(2πfC) at the signal frequency, so it **short-circuits the a.c. signal to ground** around the resistor while it is an open circuit for d.c. Hence (i) the biasing resistor R$_E$ keeps the Q-point stable (d.c. negative feedback) and (ii) the signal sees no emitter degeneration, so the full gain is obtained (A$_v$ = −R$_C$/r$_e$ instead of −R$_C$/(r$_e$+R$_E$)). In the common-base amplifier the base capacitor C$_B$ is a bypass capacitor that holds the base at a.c. ground. It is chosen so that X$_C$ ≤ R/10 at the lowest signal frequency.

**Small-signal equivalent of the common-base amplifier.** With the base at a.c. ground, the emitter is the input and the collector the output. Using the r$_e$ model (r$_e$ = V$_T$/I$_E$ = 26 mV/I$_E$; the collector current is a source αi$_e$ in parallel with the large output resistance r$_o$, neglected):


```figure caption="Small-signal (r$_e$) model of the common-base amplifier."
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
```


$$\begin{gathered}
Z_i = R_E \parallel r_e \approx r_e \qquad (\text{a few ohms to tens of ohms}) \\
Z_o = R_C \parallel r_o \approx R_C \\
v_o=-\alpha i_e R_C,\ \ v_i=-i_e r_e\ \Rightarrow\ A_v=\frac{v_o}{v_i}=\frac{\alpha R_C}{r_e}\approx\frac{R_C}{r_e}
\end{gathered}$$

With a load R$_L$ the gain is A$_v$ ≈ (R$_C$∥R$_L$)/r$_e$. The gain is positive (no phase shift between input and output), the current gain A$_i$ = α ≈ 1, the input resistance is very low and the output resistance high, so the CB stage is used as a current buffer and at high frequencies (no Miller effect). Example: I$_E$ = 2 mA, r$_e$ = 13 Ω, R$_C$ = 4 kΩ gives A$_v$ ≈ 308 and Z$_i$ ≈ 13 Ω.

@s 3
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

@s 4
The n-channel D-MOSFET is biased by a voltage divider with source resistor (self-bias plus divider).


```figure caption="prob_dmos"
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"+16 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"2.1 MΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"270 kΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
m=mosfet(ax,2.0,3.2,kind="n",mode="dep")
wire(ax,[m["D"],(4.0,4.3)])
wire(ax,[m["S"],(4.0,2.1)])
res(ax,(5.0,6.6),(5.0,4.9),"2.4 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"1.5 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"V$_P$ = −4 V,  I$_{DSS}$ = 8 mA",ha="left",size=8)
```


**Solution** (R in kΩ, I in mA, V in V). The gate current is zero, so the divider fixes the gate voltage:

$$V_G=\frac{R_2}{R_1+R_2}V_{DD}=\frac{270}{2100+270}(16)=1.8228\ \text{V}$$

The gate-source voltage is V$_{GS}$ = V$_G$ − I$_D$R$_S$ = 1.8228 − 1.5 I$_D$ and the device equation is I$_D$ = I$_{DSS}$(1 − V$_{GS}$/V$_P$)² = 8(1 − V$_{GS}$/(-4))². Substituting,

$$I_D=8\,(1.4557-0.3750\,I_D)^2\ \ \Rightarrow\ \ 1.1250\,I_D^2-9.7342\,I_D+16.9524=0$$

$$I_D=\frac{-B\pm\sqrt{B^2-4AC}}{2A}\ \ \Rightarrow\ \ I_D=2.416\ \text{mA}\ \ \text{or}\ \ 6.236\ \text{mA}$$

The root I$_D$ = 6.236 mA gives V$_{GS}$ = -7.53 V, which lies beyond cut-off (V$_{GS}$ < V$_P$ = -4 V), so it is rejected. Therefore

$$\begin{gathered}
I_D=2.416\ \text{mA}\\
V_{GS}=V_G-I_DR_S=1.8228-(2.416)(1.5)=-1.802\ \text{V}\ \ (>V_P)\\
V_{DS}=V_{DD}-I_D(R_D+R_S)=16-2.416(2.4+1.5)=6.576\ \text{V}
\end{gathered}$$

*Check of the region.* V$_{DS}$ = 6.576 V > V$_{GS}$ − V$_P$ = 2.198 V, so the transistor is in **saturation (pinch-off region)** and the Shockley equation is valid. Also g$_m$ = (2I$_{DSS}$/|V$_P$|)(1 − V$_{GS}$/V$_P$) = 2.198 mS.

@s 5
| RC oscillators | LC oscillators |
|---|---|
| Frequency determined by resistors and capacitors, f = 1/(2πRC) (times a constant) | Frequency determined by an inductor-capacitor tank, f = 1/(2π√(LC)) |
| Used for **audio and low frequencies** (a few Hz up to about 1 MHz): function generators, audio signal sources | Used for **radio frequencies** (100 kHz to hundreds of MHz): RF carriers in transmitters, local oscillators in receivers |
| Inductors are not needed, so they are small, cheap and easy to integrate | Bulky inductors, but high Q and good frequency stability at RF |
| Phase-shift, Wien bridge | Hartley, Colpitts, Clapp (crystal for best stability) |

**Wien bridge oscillator.** A non-inverting op-amp amplifier (gain A$_v$ = 1 + R$_f$/R$_1$) is combined with a **lead-lag network** (series R–C in series arm, parallel R–C in shunt arm) which gives the positive feedback to the non-inverting input. The resistor divider R$_f$, R$_1$ gives the negative feedback that sets the gain.


```figure caption="Wien bridge oscillator."
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
```


Let Z$_s$ = R + 1/(jωC) and Z$_p$ = R/(1 + jωRC) (R∥C). The feedback factor of the lead-lag network is

$$\beta=\frac{Z_p}{Z_s+Z_p}=\frac{1}{3+j\left(\omega RC-\dfrac{1}{\omega RC}\right)}$$

The phase of β is zero when the imaginary part vanishes, ωRC = 1/(ωRC), that is at

$$\begin{gathered}\omega_o=\frac{1}{RC}\ \ \Rightarrow\ \ f_o=\frac{1}{2\pi RC} \\ |\beta|=\frac13\ \ \text{at}\ f_o\end{gathered}$$

The amplifier gives no phase shift, so the phase condition holds at f$_o$. The magnitude condition |Aβ| ≥ 1 requires

$$A_v=1+\frac{R_f}{R_1}\ \ge\ 3\ \ \Rightarrow\ \ R_f\ge 2R_1$$

In practice R$_f$ is made slightly larger than 2R$_1$ (or a lamp/thermistor/diode limiter is used in R$_f$) so that oscillation starts and the amplitude is then stabilised at A$_v$ = 3. *Example:* R = 10 kΩ, C = 16 nF gives f$_o$ = 1/(2π × 10 k × 16 n) = 995 Hz ≈ 1 kHz with R$_1$ = 10 kΩ, R$_f$ ≈ 20 kΩ+.

@s 6
**Simple current mirror.** Two identical transistors Q$_1$, Q$_2$ have the same V$_{BE}$, so their collector currents are equal: I$_{C2}$ = I$_{C1}$. The reference current, however, also supplies the two base currents:

$$I_{REF}=I_{C1}+2I_B=I_O\left(1+\frac{2}{\beta}\right)\ \Rightarrow\ I_O=\frac{I_{REF}}{1+2/\beta}$$

The difference between I$_O$ and I$_{REF}$ is the **base-current error** 2I$_B$ (for β = 100 it is 2 percent, and it is worse for low β).

**Base-current compensation.** An emitter-follower transistor Q$_3$ is added: its base is connected to the collector of Q$_1$, its emitter feeds the two bases (the node of Q$_1$, Q$_2$) and its collector goes to V$_{CC}$.


```figure caption="Current mirror with base-current compensation (Q$_3$)."
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
```


Now the two base currents are supplied by the emitter of Q$_3$, so Q$_3$'s base current is smaller by the factor (β+1) and only that much is taken from I$_{REF}$:

$$I_{B3}=\frac{2I_B}{\beta+1}=\frac{2I_O}{\beta(\beta+1)}$$

$$I_{REF}=I_{C1}+I_{B3}=I_O+\frac{2I_O}{\beta(\beta+1)}\ \Rightarrow\ I_O=\frac{I_{REF}}{1+\dfrac{2}{\beta(\beta+1)}}$$

For β = 100 the error is 2/(100 × 101) = 0.0198 percent (I$_O$ = 0.9998 I$_{REF}$) compared with 2 percent (I$_O$ = 0.9804 I$_{REF}$) for the simple mirror: the difference between I$_O$ and I$_{REF}$ is reduced by a factor of about (β+1), and it becomes almost β-independent. Q$_3$ must be a high-β transistor; it also needs V$_{CE3}$ > 0, so the minimum supply is 2V$_{BE}$ + V$_{CE(sat)}$ (slightly more than the simple mirror).

@s 7
Given V$_p$ = 20 V, R$_L$ = 16 Ω, V$_{CC}$ = 30 V. The two transistors of the push-pull class B stage conduct alternately, each for 180°.

$$\begin{gathered}
I_p=\frac{V_p}{R_L}=\frac{20}{16}=1.2500\ \text{A},\qquad I_{dc}=\frac{2I_p}{\pi}=\frac{2(1.2500)}{\pi}=0.7958\ \text{A} \\
\textbf{Input power:}\quad P_{in}=V_{CC}I_{dc}=30\times 0.7958=\mathbf{23.87\ W}\\
\textbf{Output power:}\quad P_o=\frac{V_p^2}{2R_L}=\frac{20^2}{2(16)}=\mathbf{12.50\ W}\\
\textbf{Efficiency:}\quad \eta=\frac{P_o}{P_{in}}\times100=\frac{12.50}{23.87}\times100=\mathbf{52.4\ percent}
\end{gathered}$$

*Check with the general formula:* η = (π/4)(V$_p$/V$_{CC}$) = 0.7854 × (20/30) = 52.4 percent. The power dissipated in the two transistors is P$_D$ = P$_{in}$ − P$_o$ = 23.87 − 12.50 = 11.37 W (5.69 W in each). The result is below the theoretical 78.5 percent maximum because V$_p$ is only 2/3 of V$_{CC}$.

@s 8
**Transformer-coupled class A amplifier.** The collector load is the primary of an output transformer whose secondary feeds the load R$_L$; the transistor is biased at a point Q in the middle of the active region so that it conducts for the full 360° of the input cycle. The transformer matches the load: the resistance seen in the collector is R$_L'$ = (N$_1$/N$_2$)²R$_L$. Because the d.c. resistance of the primary is almost zero, the **d.c. load line is vertical** (V$_{CE}$ = V$_{CC}$ for all I$_C$); the **a.c. load line** passes through Q with slope −1/R$_L'$ and swings between 0 and 2V$_{CC}$.


```figure caption="Transformer-coupled class A amplifier and its a.c. load line."
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
```


**General efficiency.** Let the collector-emitter voltage swing between V$_{CE(max)}$ and V$_{CE(min)}$ (peak-to-peak V$_{pp}$ = V$_{CE(max)}$ − V$_{CE(min)}$) and V$_{CEQ}$ = V$_{CC}$:

$$\begin{gathered}
P_{dc}=V_{CC}I_{CQ} \\
P_{ac}=\frac{V_{p}I_{p}}{2}=\frac{V_{pp}\,I_{pp}}{8}=\frac{(V_{CE(max)}-V_{CE(min)})(I_{C(max)}-I_{C(min)})}{8}
\end{gathered}$$

With V$_{CE(max)}$ + V$_{CE(min)}$ = 2V$_{CC}$ and I$_{CQ}$ = V$_{CC}$/R$_L'$: I$_{pp}$ = V$_{pp}$/R$_L'$, so P$_{ac}$ = V$_{pp}^2$/(8R$_L'$) and

$$\begin{gathered}\eta=\frac{P_{ac}}{P_{dc}}=\frac{V_{pp}^2/(8R_L')}{V_{CC}^2/R_L'}=\frac{1}{8}\left(\frac{V_{pp}}{V_{CC}}\right)^2=\frac{1}{2}\left(\frac{V_p}{V_{CC}}\right)^2 \\ \left(=50\left(\frac{V_{CE(max)}-V_{CE(min)}}{V_{CE(max)}+V_{CE(min)}}\right)^2\ \text{percent}\right)\end{gathered}$$

**Maximum efficiency.** The largest possible swing is V$_p$ = V$_{CC}$ (V$_{CE(min)}$ = 0, V$_{CE(max)}$ = 2V$_{CC}$): **η$_{max}$ = 50 percent**, compared with 25 percent for the series-fed (resistive-load) class A stage. The maximum output power is P$_{ac(max)}$ = V$_{CC}^2$/(2R$_L'$) = V$_{CC}I_{CQ}$/2, and the transistor dissipation is largest with no signal, P$_D$ = V$_{CC}I_{CQ}$ = 2P$_{ac(max)}$.

@s 9
**Discrete series regulator.** A pass transistor Q$_1$ (emitter follower) is in series with the load. A Zener diode D$_Z$ fed through R$_1$ gives a constant reference voltage V$_Z$ at the base:

$$V_o=V_Z-V_{BE1}$$

*Regulation action:* if the input rises (or the load current falls) V$_o$ tends to rise, V$_{BE1}$ = V$_Z$ − V$_o$ falls, I$_{B1}$ and hence the collector current fall, V$_{CE1}$ rises and takes up the extra input voltage, so V$_o$ returns almost to its old value. The load current is supplied through the transistor, so the Zener only has to supply I$_{B1}$ = I$_L$/(β+1), and the Zener current is made nearly independent of the load.

**Stability factor (line regulation) S$_V$ = ΔV$_o$/ΔV$_i$** for a constant load. A change ΔV$_i$ divides between R$_1$ and the dynamic resistance r$_z$ of the Zener (the base-looking resistance (β+1)(r$_e$+R$_L$) is very large and is in parallel with r$_z$, so it is neglected):

$$\Delta V_Z=\Delta V_i\,\frac{r_z}{R_1+r_z}$$

The emitter follows the base with the gain A$_v$ = R$_L$/(R$_L$ + r$_e$) ≈ 1 (ΔV$_{BE}$ ≈ r$_e$ΔI$_E$ is small), so

$$\Delta V_o=\Delta V_Z\,\frac{R_L}{R_L+r_e}\ \Rightarrow\ \boxed{\ S_V=\frac{\Delta V_o}{\Delta V_i}=\frac{r_z}{R_1+r_z}\cdot\frac{R_L}{R_L+r_e}\ \approx\ \frac{r_z}{R_1+r_z}\ }$$

Since r$_z$ ≪ R$_1$, S$_V$ is small (for example r$_z$ = 10 Ω, R$_1$ = 500 Ω gives S$_V$ = 10/510 = 0.0196, i.e. a 10 V change at the input produces only 0.2 V at the output); the smaller the stability factor, the better the regulation. Similarly the output resistance R$_{out}$ = r$_e$ + r$_z$∥R$_1$/(β+1) is very small (about 1 Ω), which gives a good load regulation. The percent regulation can be improved further by using a Darlington pass transistor, a constant-current source in place of R$_1$ or an error amplifier (see the improved circuit).

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
V_{o(min)}=3\ \text{V}:\quad R_{2(min)}=240\left(\frac{3}{1.25}-1\right)=336\ \Omega \\
V_{o(max)}=15\ \text{V}:\quad R_{2(max)}=240\left(\frac{15}{1.25}-1\right)=2640\ \Omega
\end{gathered}$$

So R$_2$ must be variable from 336 Ω to 2640 Ω. Use a **fixed resistor of 330 Ω in series with a 2500 Ω potentiometer** (the fixed part sets the minimum voltage): R$_2$ varies from 330 Ω to 2830 Ω, giving V$_o$ from 1.25(1+330/240) = 2.97 V to 1.25(1+2830/240) = 15.99 V, which covers the required 3 to 15 V (the pot is trimmed to stop at 15 V).

*Other components.* C$_1$ = 0.1 µF at the input (when the regulator is far from the filter capacitor) and C$_2$ = 1 µF tantalum (or 10 µF) at the output for stability and transient response; a diode across the regulator protects against the discharge of C$_2$ into the output when the input is shorted. The unregulated input must satisfy V$_{in}$ ≥ V$_{o(max)}$ + 3 V (dropout), i.e. V$_{in}$ ≈ 18 V (up to the 40 V maximum differential), and the regulator delivers up to 1.5 A with a heat sink (P$_D$ = (V$_{in}$ − V$_o$)I$_o$). Line and load regulation are about 0.01 percent per volt and 0.1 percent.

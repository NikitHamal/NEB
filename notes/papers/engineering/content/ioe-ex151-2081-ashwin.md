---
file: NEBians-IOE-Past-Paper-Electronic-Device-and-Circuits-EX151-2081-Ashwin.pdf
subject: Electronic Device and Circuits
level: BE · Year I / Part II
code: EX 151
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>


@q 1
Design β independent type dc biased common emitter amplifier. Given parameters V$_{CC}$ = 20 V, I$_C$ = 1.5 mA and β = 110. Use stiff biasing method. [[4]]

@q 2
Why is a common collector BJT amplifier also known as an emitter follower? Draw the small signal model of common collector amplifier circuit and derive expressions for input resistance, voltage gain, and current gain. [[1+4]]

@q 3
Derive trans-conductance of BJT. [[4]]

@q 4
Describe the construction and working principle of n channel enhancement-type MOSFET with the help of necessary diagrams and its drain characteristic curve. [[7]]

@q 5
Find I$_D$ and V$_{DS}$ for the following circuit. Given data are V$_P$ = −5.5 V, I$_{DSS}$ = 10 mA. Assume all the capacitors are ideal and check whether the transistor is operating in the Pinch off region or not. [[6]]

```figure caption="Question 5: JFET amplifier, V$_{DD}$ = 20 V, R$_1$ = 1.5 MΩ, R$_2$ = 330 kΩ, R$_D$ = 2 kΩ, R$_S$ = 1 kΩ (bypassed by C$_S$); C$_G$, C$_D$ coupling capacitors."
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"V$_{DD}$ = 20 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"1.5 MΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"330 kΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
wire(ax,[(2.0,3.2),(2.9,3.2)]); ax.plot([2.9,2.9],[2.2,4.2],color=INK,lw=2.4)
wire(ax,[(2.9,4.2),(4.0,4.2),(4.0,4.4)]); wire(ax,[(2.9,2.2),(4.0,2.2),(4.0,2.0)])
ax.annotate("",xy=(3.0,3.2),xytext=(2.45,3.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3,mutation_scale=9))
res(ax,(5.0,6.6),(5.0,4.9),"2 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"1 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"V$_P$ = −5.5 V,  I$_{DSS}$ = 10 mA",ha="left",size=8)
```

@q 6
State Barkhausen criterion for sinusoidal oscillation. Draw the circuit diagram of Colpitts oscillator and write its frequency of oscillation. [[4]]

@q 7
Derive frequency of oscillation of 555 timer Astable Multivibrator. [[4]]

@q 8
Draw a Widlar Current Source. Derive an expression for an output resistance of Widlar Current Source. [[5]]

@q 9
Calculate the efficiency of a transformer coupled Class A amplifier for a supply of 12 V DC and output of V$_P$ = 12 V and 6 V. [[4]]

@q 10
Draw the circuit diagram and the characteristic curve of a transformer coupled class B push-pull amplifier and derive its general efficiency. [[5]]

@q 11
Draw the circuit diagram of class A tuned amplifier with its frequency response. Derive its 3dB bandwidth. [[4]]

@q 12
Design variable DC voltage regulator using LM 317 to get (10-20) volts output. [[4]]

@q 13
Explain the working principle of a series transistor voltage regulator with improved performance and derive an expression for the voltage stability. [[2+2]]
<!-- SOLUTIONS -->

@s 1
**Design rules for a β-independent (stiff) voltage-divider bias.** Choose (i) V$_E$ = V$_{CC}$/10 so that V$_{BE}$ variations are small compared with V$_E$, (ii) V$_{CE}$ ≈ V$_{CC}$/2 for maximum undistorted swing, (iii) the divider current much larger than I$_B$, which is ensured by R$_2$ ≤ 0.1βR$_E$ (stiff divider; then V$_B$ is nearly independent of β).

Given: V$_{CC}$ = 20 V, I$_E$ ≈ I$_C$ = 1.51364 mA, β = 110.

$$\begin{gathered}
V_E=\frac{V_{CC}}{10}=2.00\ \text{V}, \qquad R_E=\frac{V_E}{I_E}=\frac{2.00}{1.51364\ \text{mA}}=1.32\ \text{k}\Omega \\
V_B=V_E+V_{BE}=2.00+0.7=2.70\ \text{V} \\
R_2\le 0.1\beta R_E=0.1(110)(1.32\ \text{k}\Omega)=14.53\ \text{k}\Omega\ \ \Rightarrow\ \ R_2=14.50\ \text{k}\Omega \\
\frac{R_2}{R_1+R_2}V_{CC}=V_B\ \Rightarrow\ R_1=R_2\left(\frac{V_{CC}}{V_B}-1\right)=93.13\ \text{k}\Omega \\
R_C=\frac{V_{CC}-V_E-V_{CE}}{I_C}=\frac{20-2.00-10.00}{1.500\ \text{mA}}=5.33\ \text{k}\Omega
\end{gathered}$$

Use the nearest standard values: R$_1$ ≈ 93 kΩ, R$_2$ ≈ 15 kΩ, R$_E$ ≈ 1.32 kΩ, R$_C$ ≈ 5.3 kΩ.

*Check of stiffness.* Thevenin resistance R$_B$ = R$_1$ ∥ R$_2$ = 12.57 kΩ, and I$_B$ = I$_C$/β = 13.6 µA. The voltage lost in R$_B$ is I$_B$R$_B$ = 0.17 V, only a small fraction of V$_B$; so I$_E$ = (V$_{BB}$ − V$_{BE}$)/(R$_E$ + R$_B$/(β+1)) changes by about 4.1 percent when β changes from β to 2β, i.e. the Q-point is practically β-independent. With I$_C$ = 1.5 mA the quiescent voltages are V$_{CE}$ = 10.00 V and V$_C$ = 12.00 V (transistor in the active region).

@s 2
**Why the common-collector amplifier is called an emitter follower.** The output is taken from the emitter and the emitter voltage **follows the input** in magnitude and phase: v$_o$ = v$_i$ − V$_{BE}$, so the voltage gain is close to 1 (slightly less) and there is no phase reversal. The emitter "follows" the base.

**Small-signal model** (collector at a.c. ground, r$_o$ neglected):


```figure caption="Small-signal model of the common-collector amplifier."
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
```


Input loop: v$_i$ = i$_b$r$_π$ + i$_e$R$_E$ with i$_e$ = (β+1)i$_b$ and r$_π$ = βr$_e$, so the resistance looking into the base is

$$\begin{gathered}Z_b=\frac{v_i}{i_b}=r_\pi+(\beta+1)R_E\approx\beta\,(r_e+R_E) \\ Z_i=R_B\parallel Z_b\end{gathered}$$

Voltage gain: v$_o$ = i$_e$R$_E$ = (β+1)i$_b$R$_E$, hence

$$A_v=\frac{v_o}{v_i}=\frac{(\beta+1)R_E}{r_\pi+(\beta+1)R_E}=\frac{R_E}{R_E+r_e}\ \lesssim\ 1$$

Current gain (load R$_L$ connected, R$_E$' = R$_E$∥R$_L$; i$_o$ is the current in R$_L$):

$$A_i=\frac{i_o}{i_i}=\frac{i_o}{i_b}\cdot\frac{i_b}{i_i}=(\beta+1)\frac{R_E}{R_E+R_L}\cdot\frac{R_B}{R_B+Z_b}\approx(\beta+1)\ \text{(large)}$$

Output resistance Z$_o$ = R$_E$ ∥ (r$_e$ + R$_s'$/(β+1)), where R$_s'$ = R$_s$∥R$_B$ is the source resistance seen by the base; it is **very low**. So the emitter follower has high input resistance, low output resistance, unity voltage gain and large current gain: it is a buffer used for impedance matching.

@s 3
**Transconductance** is the change of collector current per unit change of base-emitter voltage at a fixed V$_{CE}$:

$$g_m=\left.\frac{\partial i_C}{\partial v_{BE}}\right|_{V_{CE}}$$

The collector current of a forward-active BJT follows the Shockley (Ebers-Moll) relation

$$\begin{gathered}i_C=I_S\,e^{\,v_{BE}/V_T} \\ V_T=\frac{kT}{q}\approx 26\ \text{mV at }300\ \text{K}\end{gathered}$$

Differentiating with respect to v$_{BE}$ at the Q-point (I$_C$, V$_{BE}$):

$$g_m=\frac{d}{dv_{BE}}\left(I_S e^{v_{BE}/V_T}\right)=\frac{I_S e^{V_{BE}/V_T}}{V_T}=\frac{I_C}{V_T}\approx 40\,I_C$$

So g$_m$ is directly proportional to the d.c. collector current (about 40 mS per mA). Related quantities: r$_e$ = V$_T$/I$_E$ = α/g$_m$ ≈ 1/g$_m$, r$_π$ = β/g$_m$ = βr$_e$ and the small-signal collector current is i$_c$ = g$_m$v$_{be}$. Example: I$_C$ = 1.5 mA gives g$_m$ = 1.5 mA/26 mV = 57.7 mS and r$_e$ = 17.3 Ω.

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
The JFET is biased by a divider with a source resistor R$_S$ (bypassed by C$_S$ for a.c., so d.c. analysis uses R$_S$ = 1 kΩ).


```figure caption="prob_jfet2"
fig,ax=ckt_canvas(4.6,4.0,xlim=(-1.2,7.6),ylim=(-1.0,7.6))
terminal(ax,(2.8,7.2)); label(ax,(3.3,7.25),"V$_{DD}$ = 20 V",ha="left",size=8.6)
wire(ax,[(1.0,6.6),(5.0,6.6)]); wire(ax,[(2.8,6.6),(2.8,7.2)]); node(ax,(2.8,6.6))
wire(ax,[(1.0,6.6),(1.0,5.9)]); res(ax,(1.0,6.6),(1.0,3.2),"1.5 MΩ",side=-1,off=0.6)
res(ax,(1.0,3.2),(1.0,0.4),"330 kΩ",side=-1,off=0.6)
node(ax,(1.0,3.2)); wire(ax,[(1.0,3.2),(2.0,3.2)])
wire(ax,[(2.0,3.2),(2.9,3.2)]); ax.plot([2.9,2.9],[2.2,4.2],color=INK,lw=2.4)
wire(ax,[(2.9,4.2),(4.0,4.2),(4.0,4.4)]); wire(ax,[(2.9,2.2),(4.0,2.2),(4.0,2.0)])
ax.annotate("",xy=(3.0,3.2),xytext=(2.45,3.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3,mutation_scale=9))
res(ax,(5.0,6.6),(5.0,4.9),"2 kΩ",side=1,off=0.5,body=1.0)
wire(ax,[(5.0,4.9),(5.0,4.4),(4.0,4.4)])
wire(ax,[(5.0,2.0),(5.0,1.55)]); res(ax,(5.0,2.0),(5.0,0.4),"1 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(4.0,2.0),(5.0,2.0)])
wire(ax,[(1.0,0.4),(5.0,0.4)]); gnd(ax,(3.0,0.4)); node(ax,(3.0,0.4))
label(ax,(-1.1,7.3),"V$_P$ = −5.5 V,  I$_{DSS}$ = 10 mA",ha="left",size=8)
```


**Solution** (R in kΩ, I in mA, V in V). The gate current is zero, so the divider fixes the gate voltage:

$$V_G=\frac{R_2}{R_1+R_2}V_{DD}=\frac{330}{1500+330}(20)=3.6066\ \text{V}$$

The gate-source voltage is V$_{GS}$ = V$_G$ − I$_D$R$_S$ = 3.6066 − 1 I$_D$ and the device equation is I$_D$ = I$_{DSS}$(1 − V$_{GS}$/V$_P$)² = 10(1 − V$_{GS}$/(-5.5))². Substituting,

$$I_D=10\,(1.6557-0.1818\,I_D)^2\ \ \Rightarrow\ \ 0.3306\,I_D^2-7.0209\,I_D+27.4147=0$$

$$I_D=\frac{-B\pm\sqrt{B^2-4AC}}{2A}\ \ \Rightarrow\ \ I_D=5.157\ \text{mA}\ \ \text{or}\ \ 16.081\ \text{mA}$$

The root I$_D$ = 16.081 mA gives V$_{GS}$ = -12.47 V, which lies beyond cut-off (V$_{GS}$ < V$_P$ = -5.5 V), so it is rejected. Therefore

$$\begin{gathered}
I_D=5.157\ \text{mA}\\
V_{GS}=V_G-I_DR_S=3.6066-(5.157)(1)=-1.550\ \text{V}\ \ (>V_P)\\
V_{DS}=V_{DD}-I_D(R_D+R_S)=20-5.157(2+1)=4.529\ \text{V}
\end{gathered}$$

*Check of the region.* V$_{DS}$ = 4.529 V > V$_{GS}$ − V$_P$ = 3.950 V, so the transistor is in **saturation (pinch-off region)** and the Shockley equation is valid. Also g$_m$ = (2I$_{DSS}$/|V$_P$|)(1 − V$_{GS}$/V$_P$) = 2.611 mS.

**Answers:** I$_D$ = 5.157 mA, V$_{DS}$ = 4.53 V, and since V$_{DS}$ > V$_{GS}$ − V$_P$ the transistor operates in the pinch-off (saturation) region.

@s 6
**Barkhausen criteria.** An amplifier with gain A and a feedback network with feedback factor β (positive feedback) sustains oscillation at a frequency f$_o$ if the loop gain Aβ satisfies

$$\begin{gathered}
|A\beta|=1 \quad(\text{magnitude condition: the loop gain is unity}) \\
\angle A\beta = 0^\circ\ \text{or}\ 360^\circ\quad(\text{phase condition: total phase shift around the loop is zero})
\end{gathered}$$

The closed-loop gain A$_f$ = A/(1 − Aβ) becomes infinite, so an output exists without any input. Oscillations start from noise when |Aβ| is slightly greater than 1 initially; the amplitude then limits (non-linearity or an amplitude-stabilising element) so that |Aβ| settles at 1.

**Colpitts oscillator.** The tank is an inductor L in parallel with **two capacitors C$_1$ and C$_2$ in series; their junction is at a.c. ground**. The voltage across C$_2$ gives the feedback to the base; being referred to the grounded junction it is 180° out of phase with the collector voltage across C$_1$, which together with the 180° of the CE amplifier gives zero total phase shift.


```figure caption="Colpitts oscillator."
fig,ax=ckt_canvas(5.2,3.6,xlim=(-0.6,8.6),ylim=(-1.2,7.6))
terminal(ax,(6.6,7.2)); label(ax,(7.0,7.2),"+V$_{CC}$",ha="left",size=8.6)
bj=bjt(ax,4.0,2.4)
node(ax,(5.0,4.6))
wire(ax,[(4.6,3.5),(4.6,4.6),(5.0,4.6)])
cap(ax,(5.0,4.6),(3.2,4.6),"C$_1$",side=-1,gap=0.24); cap(ax,(3.2,4.6),(1.4,4.6),"C$_2$",side=-1,gap=0.24)
wire(ax,[(5.0,4.6),(5.0,5.7),(4.2,5.7)]); ind(ax,(4.2,5.7),(2.2,5.7),"L",side=1,body=1.2); wire(ax,[(2.2,5.7),(1.4,5.7),(1.4,4.6)])

wire(ax,[(1.4,4.6),(1.4,2.4),bj["B"]])
wire(ax,[(3.2,4.6),(3.2,3.9)]); node(ax,(3.2,4.6)); gnd(ax,(3.2,3.9))
wire(ax,[(5.0,4.6),(6.6,4.6)]); res(ax,(6.6,4.6),(6.6,6.6),"RFC",side=1,off=0.5,body=0.7); wire(ax,[(6.6,6.6),(6.6,7.2)])
wire(ax,[bj["E"],(4.6,0.7)]); res(ax,(4.6,0.7),(4.6,-0.4),"R$_E$",side=1,off=0.5,body=0.5); gnd(ax,(4.6,-0.4))
label(ax,(5.6,2.4),"f$_o$ = 1/(2π√(L$_{eq}$C$_{eq}$))",ha="left",size=7.4)
```


The two capacitors in series act as the tank capacitance

$$\begin{gathered}C_{eq}=\frac{C_1C_2}{C_1+C_2} \\ \Rightarrow \\ f_o=\frac{1}{2\pi\sqrt{L\,C_{eq}}}=\frac{1}{2\pi\sqrt{L\dfrac{C_1C_2}{C_1+C_2}}}\end{gathered}$$

The feedback factor is β = −C$_1$/C$_2$ and the amplifier gain is A ≈ h$_{fe}$R$_C$/h$_{ie}$, so the sustained-oscillation condition is

$$\begin{gathered}h_{fe}\ \ge\ \frac{C_2}{C_1} \\ (\text{FET: }g_m r_d\ge C_2/C_1)\end{gathered}$$

*Example:* L = 100 µH, C$_1$ = 1 nF, C$_2$ = 1 nF: C$_{eq}$ = 0.5 nF, f$_o$ = 1/(2π√(100×10⁻⁶ × 0.5×10⁻⁹)) = 711.8 kHz.

@s 7
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

@s 8
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

@s 9
For the transformer-coupled class A stage the Q-point is at V$_{CEQ}$ = V$_{CC}$ = 12 V and, because the d.c. resistance of the primary is zero, the collector voltage can swing from 0 to 2V$_{CC}$ = 24 V (peak value V$_p$ ≤ V$_{CC}$). With the a.c. load line of slope −1/R$_L'$ through Q (I$_{CQ}$ = V$_{CC}$/R$_L'$):

$$\begin{gathered}
P_{dc}=V_{CC}I_{CQ}=\frac{V_{CC}^2}{R_L'},\qquad P_{ac}=\frac{V_p^2}{2R_L'} \\
\eta=\frac{P_{ac}}{P_{dc}}=\frac{V_p^2/(2R_L')}{V_{CC}^2/R_L'}=\frac{1}{2}\left(\frac{V_p}{V_{CC}}\right)^2
\end{gathered}$$

| V$_p$ | η = ½(V$_p$/V$_{CC}$)² | Result |
|---|---|---|
| 12 V | ½(12/12)² = 0.5 | **50 percent** (the theoretical maximum) |
| 6 V | ½(6/12)² = 0.125 | **12.5 percent** |

(For a numerical check take R$_L'$ = 12 Ω: I$_{CQ}$ = 1 A, P$_{dc}$ = 12 W; V$_p$ = 12 V gives I$_p$ = 1 A and P$_{ac}$ = 6 W, η = 50 percent; V$_p$ = 6 V gives P$_{ac}$ = 1.5 W, η = 12.5 percent.) The efficiency falls as the square of the signal amplitude because P$_{dc}$ is constant, independent of the signal.

@s 10
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

@s 11
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

@s 12
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
V_{o(max)}=20\ \text{V}:\quad R_{2(max)}=240\left(\frac{20}{1.25}-1\right)=3600\ \Omega
\end{gathered}$$

So R$_2$ must be variable from 1680 Ω to 3600 Ω. Use a **fixed resistor of 1680 Ω in series with a 2000 Ω potentiometer** (the fixed part sets the minimum voltage): R$_2$ varies from 1680 Ω to 3680 Ω, giving V$_o$ from 1.25(1+1680/240) = 10.00 V to 1.25(1+3680/240) = 20.42 V, which covers the required 10 to 20 V (the pot is trimmed to stop at 20 V).

*Other components.* C$_1$ = 0.1 µF at the input (when the regulator is far from the filter capacitor) and C$_2$ = 1 µF tantalum (or 10 µF) at the output for stability and transient response; a diode across the regulator protects against the discharge of C$_2$ into the output when the input is shorted. The unregulated input must satisfy V$_{in}$ ≥ V$_{o(max)}$ + 3 V (dropout), i.e. V$_{in}$ ≈ 23 V (up to the 40 V maximum differential), and the regulator delivers up to 1.5 A with a heat sink (P$_D$ = (V$_{in}$ − V$_o$)I$_o$). Line and load regulation are about 0.01 percent per volt and 0.1 percent.

@s 13
**Series regulator with improved performance (error amplifier, closed-loop).** A Darlington pass element Q$_1$ is driven by a d.c. **error amplifier** Q$_2$. A sampling divider R$_3$, R$_4$ across the output gives the sample V$_s$ = V$_oR_4/(R_3+R_4)$, which is compared with a Zener reference V$_Z$ at the emitter of Q$_2$. The collector of Q$_2$ drives Q$_1$ (resistor R$_1$ from the input).

*Operation.* If V$_o$ increases, V$_s$ increases, V$_{BE2}$ = V$_s$ − V$_Z$ increases, Q$_2$ conducts more and takes more of the drive current from the base of Q$_1$; Q$_1$ conducts less and the output falls back. If V$_o$ falls, the action is reversed. The output voltage is set by

$$V_o=\frac{R_3+R_4}{R_4}\,(V_Z+V_{BE2})$$

and is adjustable with a potentiometer in the divider. **Why the performance improves:** the output is compared with a stable reference and the difference is amplified by the gain of Q$_2$ and of the pass transistor(s), so the regulation is much better than that of the simple Zener-follower, and the output resistance is smaller.

**Voltage stability factor.** Let the error amplifier gain be A$_e$ (≈ g$_{m2}$R$_{C2}$, R$_{C2}$ the load of Q$_2$ in parallel with the input resistance of Q$_1$), the pass stage gain A$_p$ ≈ 1 (emitter follower), and the sampling fraction β$_s$ = R$_4$/(R$_3$+R$_4$). A change ΔV$_i$ acts as a disturbance that enters through R$_1$ and, without feedback, changes the output by ΔV$_o$(open) = S$_0$ΔV$_i$ with S$_0$ ≈ 1/μ (μ is small-signal amplification of the pass stage; for the Zener-follower S$_0$ = r$_z$/(R$_1$+r$_z$)). With negative feedback, the loop gain is T = A$_eA_p\beta_s$ and

$$\Delta V_o=S_0\Delta V_i-T\,\Delta V_o\ \ \Rightarrow\ \ \boxed{\ S_V=\frac{\Delta V_o}{\Delta V_i}=\frac{S_0}{1+A_eA_p\beta_s}\ }$$

so the line regulation is improved by the factor (1 + A$_eA_p$β$_s$), typically 100 to 1000, giving S$_V$ of about 0.01 to 0.1 percent per volt. *Example:* S$_0$ = 0.02, A$_e$ = 200, A$_p$ = 1, β$_s$ = 0.5: S$_V$ = 0.02/101 = 1.98 × 10⁻⁴, i.e. 0.2 mV change at the output for a 1 V change at the input. The output resistance is similarly reduced from R$_o$ to R$_o$/(1+T), and the current-limit transistor of the previous question can be added.

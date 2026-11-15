---
file: NEBians-IOE-Past-Paper-Fundamental-of-Electrical-and-Electronics-Engineering-ENEX101-2081-Chaitra.pdf
subject: Fundamental of Electrical and Electronics Engineering
level: BE · Year I / Part I
code: ENEX 101
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEI, BCT, BME, BIE, BAM, BAS
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
In a given network, find the current flowing through the load resistance R$_L$ by using Thevenin's theorem. What should be the value of R$_L$ for maximum power to transfer? Also find the maximum power. [[6+2]]

```figure caption="Question 1: 12 V source across a 4 Ω resistor, 2 Ω series resistor, a 6 Ω resistor in series with a 10 V battery, and the load R$_L$ = 2 kΩ."
fig,ax=ckt_canvas(6.0,2.9,xlim=(-1.6,9.6),ylim=(-0.5,3.9))
batt(ax,(0,0.3),(0,2.7),"12 V",side=-1,off=0.9)
wire(ax,[(0,2.7),(0,3),(2,3)]); wire(ax,[(0,0.3),(0,0),(2,0)])
node(ax,(2,3)); node(ax,(2,0))
res(ax,(2,3),(2,0),"4 Ω",side=1,off=0.55)
res(ax,(2,3),(4.6,3),"2 Ω",side=1)
node(ax,(4.6,3)); node(ax,(4.6,0))
res(ax,(4.6,3),(4.6,1.9),"6 Ω",side=1,off=0.5,body=0.8)
batt(ax,(4.6,0),(4.6,1.9),"10 V",side=1,off=0.9)
wire(ax,[(2,0),(7,0)]); wire(ax,[(4.6,3),(7,3)])
res(ax,(7,3),(7,0),"R$_L$ = 2 kΩ",side=1,off=0.5)
```

@q 2
For the periodic signal given below, find the average and rms value. Assume T = 10 ms. [[2+3]]

```figure caption="Question 2: saw-tooth wave that rises linearly from 10 (point A, t = 0) to 20 (point B, t = T), falls back to 10 (point C) and repeats with period T. D is a point on the ramp at time t and E the point below it on the 10 level."
import numpy as _np
fig,ax=plt.subplots(figsize=(5.0,2.4))
for k in range(2):
    ax.plot([k,k+1],[10,20],color=INK,lw=1.8); ax.plot([k+1,k+1],[20,10],color=INK,lw=1.8)
ax.plot([2,2.5],[10,15],color=INK,lw=1.8)
ax.plot([0,2.6],[10,10],color=MUTED,lw=0.8,ls="--")
ax.plot([0.4,0.4],[0,14],color=MUTED,lw=0.8,ls=":")
for p,t,dx,dy in (((0,10),"A",-0.07,-1.6),((1,20),"B",0.0,0.9),((1,10),"C",0.06,-1.8),((0.4,14),"D",-0.08,0.8),((0.4,10),"E",0.06,-1.8)):
    ax.text(p[0]+dx,p[1]+dy,t,fontsize=8,fontweight="bold",ha="center")
ax.set_xticks([0.4,1,2]); ax.set_xticklabels(["t","T","2T"]); ax.set_yticks([10,20]); ax.set_ylim(0,24); ax.set_xlim(-0.1,2.7)
ax.set_xlabel("Time",fontsize=8); ax.set_ylabel("y",fontsize=8)
```

@q 3
What is the significance of the power factor? Calculate the total impedance, circuit current, power factor, and power consumed for the following circuit. [[1+6]]

```figure caption="Question 3: 3 Ω in series with j6 Ω, in series with the parallel combination of (4 Ω + j8 Ω) and (5 Ω − j8 Ω), supplied from 200 V, 50 Hz."
fig,ax=ckt_canvas(6.2,3.6,xlim=(-2.3,10.8),ylim=(-1.0,4.6))
acsrc(ax,(0,0),(0,3.0),None); label(ax,(-0.5,1.5),"200 V\n50 Hz",ha="right",size=8.2)
wire(ax,[(0,3.0),(0.5,3.0)])
res(ax,(0.5,3.0),(1.8,3.0),"3 Ω",side=1,body=0.9); ind(ax,(1.8,3.0),(3.2,3.0),"j6 Ω",side=1,body=1.1)
wire(ax,[(3.2,3.0),(4.0,3.0),(4.0,3.8),(5.0,3.8)])
res(ax,(5.0,3.8),(6.3,3.8),"4 Ω",side=1,body=0.9); ind(ax,(6.3,3.8),(7.7,3.8),"j8 Ω",side=1,body=1.1)
wire(ax,[(7.7,3.8),(8.6,3.8),(8.6,2.2),(7.7,2.2)])
wire(ax,[(4.0,3.0),(4.0,2.2),(5.0,2.2)])
res(ax,(5.0,2.2),(6.3,2.2),"5 Ω",side=-1,body=0.9); cap(ax,(6.3,2.2),(7.7,2.2),"−j8 Ω",side=-1)
wire(ax,[(8.6,3.0),(9.4,3.0),(9.4,0),(0,0)])
node(ax,(4.0,3.0)); node(ax,(8.6,3.0))
```

@q 4
Explain different methods of connection of three phase system with necessary diagrams. [[4]]

@q 5
What is a clamper circuit? Draw the output waveform of the circuit by applying the given input waveform. [[1+4]]

```figure caption="Question 5: square-wave input v$_{in}$ of ±6 V (left) applied to a resistor R, a Si diode and a 3 V battery (right); the output v$_o$ is taken across the diode-battery branch."
import numpy as _np
fig=plt.figure(figsize=(5.9,2.5))
bx=fig.add_axes([0.07,0.2,0.34,0.68])
bx.step([0,1,2,3,4,5,6],[6,-6,6,-6,6,-6,-6],where="post",color=ACCENT,lw=1.8)
bx.axhline(0,color=INK,lw=0.7); bx.set_yticks([-6,6]); bx.set_xticks([]); bx.set_ylim(-8,8); bx.set_xlim(0,6)
bx.set_ylabel("v$_{in}$ (V)",fontsize=8)
ax=fig.add_axes([0.46,0,0.54,1]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.0,5.6); ax.set_ylim(-0.7,3.6)
acsrc(ax,(0,0.2),(0,2.6),"v$_{in}$",side=-1)
wire(ax,[(0,2.6),(0,3.0),(0.6,3.0)]); res(ax,(0.6,3.0),(2.2,3.0),"R",side=1,body=1.0); wire(ax,[(2.2,3.0),(4.6,3.0)])
diode(ax,(3.4,3.0),(3.4,1.9),"Si",side=-1,body=0.5,off=0.45); batt(ax,(3.4,0.2),(3.4,1.9),"3 V",side=-1,off=0.6)
node(ax,(3.4,3.0)); node(ax,(3.4,0.2)); terminal(ax,(4.6,3.0)); terminal(ax,(4.6,0.2)); wire(ax,[(0,0.2),(4.6,0.2)]); label(ax,(5.1,1.6),"v$_o$",size=8.4)
```

@q 6
Explain the large signal model of a pn junction diode. [[4]]

@q 7
A load resistance of 1 kΩ is connected across a Zener voltage regulator with Zener diode of 10 V. Find the Zener current and power dissipated across the Zener diode. [[4]]

```figure caption="Question 7: Zener regulator with V$_S$ = 18 V, R$_S$ = 250 Ω, V$_Z$ = 10 V and R$_L$ = 1 kΩ."
fig,ax=ckt_canvas(5.2,2.6,xlim=(-1.8,8.2),ylim=(-0.5,3.7))
batt(ax,(0,0.3),(0,2.7),"V$_S$ = 18 V",side=-1,off=1.0)
wire(ax,[(0,2.7),(0,3),(0.6,3)]); res(ax,(0.6,3),(2.6,3),"R$_S$ = 250 Ω",side=1)
wire(ax,[(2.6,3),(5,3)]); diode(ax,(3.4,0),(3.4,3),"V$_Z$ = 10 V",side=1,zener=True,off=0.9)
res(ax,(5,3),(5,0),"R$_L$ = 1 kΩ",side=1,off=0.5)
wire(ax,[(0,0.3),(0,0),(5,0)]); node(ax,(3.4,3)); node(ax,(3.4,0))
```

@q 8
Draw the DC load line and determine the Q point of the voltage divider-biased transistor circuit having V$_{CC}$ = 20 V, R$_C$ = 2 K, R$_1$ = 20 K, R$_2$ = 10 K, R$_E$ = 4 K, and β = 100. [[5]]

@q 9
Draw a circuit diagram of BJT switch and explain its operation. [[3]]

@q 10
Explain the operation of n-channel depletion MOSFET with the necessary diagrams. [[6]]

@q 11
Derive the expression of summing amplifier using OP amp. [[4]]

@q 12
State Barkhausen Criteria for an oscillation. Draw a Wien bridge oscillator circuit and derive its frequency of oscillation. [[1+4]]

<!-- SOLUTIONS -->

@s 1
**Thevenin's theorem.** Any linear two-terminal network containing sources and resistors can be replaced, as seen from its terminals, by a single voltage source $V_{th}$ (the open-circuit voltage) in series with a resistance $R_{th}$ (the resistance seen from the terminals with all independent sources killed: voltage sources shorted, current sources opened).

*Reading of the circuit.* Both batteries are read with the long plate (+) at the top. The 12 V source is wired directly between the top and bottom rails, so the node *a* at the top of the 4 Ω resistor is held at exactly 12 V; the 4 Ω resistor is simply connected across an ideal source, and it affects neither $V_{th}$ nor $R_{th}$. The load $R_L$ is connected across node *b* (below the 2 Ω resistor) and the bottom rail.

**Step 1: open-circuit voltage.** Remove $R_L$. The only loop left is 12 V → 2 Ω → 6 Ω → 10 V battery, and the 10 V battery is opposed to the 12 V source:

$$I = \frac{12 - 10}{2 + 6} = 0.25\ \text{A}$$

$$V_{th} = V_b = 12 - 2(0.25) = 11.5\ \text{V}$$

(Check from the other side: $V_b = 10 + 6 \times 0.25$, which is again 11.5 V.)

**Step 2: Thevenin resistance.** Short the 12 V source and the 10 V battery. Node *a* becomes ground (the 4 Ω is shorted out), so looking into the terminals the 2 Ω and 6 Ω are in parallel:

$$R_{th} = 2 \parallel 6 = \frac{2 \times 6}{2 + 6} = 1.5\ \Omega$$

```figure caption="Thévenin equivalent of Question 1: V$_{th}$ = 11.5 V and R$_{th}$ = 1.5 Ω in series with the load R$_L$."
fig,ax=ckt_canvas(4.4,2.2,xlim=(-1.5,6.6),ylim=(-0.4,3.4))
batt(ax,(0,0.2),(0,2.6),"11.5 V",side=-1)
wire(ax,[(0,2.6),(0,3.0),(0.6,3.0)]); res(ax,(0.6,3.0),(2.6,3.0),"1.5 Ω",side=1)
wire(ax,[(2.6,3.0),(5.0,3.0)]); res(ax,(5.0,3.0),(5.0,0),"R$_L$",side=1,off=0.5)
wire(ax,[(0,0.2),(0,0),(5.0,0)])
```

**Step 3: current in the given load $R_L = 2\ \text{k}\Omega$.**

$$I_L = \frac{V_{th}}{R_{th} + R_L} = \frac{11.5}{1.5 + 2000} = 5.746 \times 10^{-3}\ \text{A} \approx \boxed{5.75\ \text{mA}}$$

**Step 4: value of $R_L$ for maximum power.** The load power is $P = I^2R_L = \dfrac{V_{th}^2R_L}{(R_{th}+R_L)^2}$. Setting $dP/dR_L = 0$ gives $R_{th} + R_L - 2R_L = 0$, so

$$\boxed{R_L = R_{th} = 1.5\ \Omega}$$

(maximum power transfer theorem).

**Step 5: maximum power.**

$$P_{max} = \frac{V_{th}^2}{4R_{th}} = \frac{(11.5)^2}{4 \times 1.5} = \boxed{22.04\ \text{W}}$$

(Here $I = 11.5/3 = 3.83$ A and $P = 3.83^2 \times 1.5 = 22.04$ W ✓; the efficiency is 50 %. With the actual $R_L = 2\ \text{k}\Omega$ the load only receives $(5.746\ \text{mA})^2 \times 2000 = 66\ \text{mW}$.)

@s 2
From the figure the signal over one period ($0 \le t \le T$) is a straight line from $A(0, 10)$ to $B(T, 20)$:

$$y(t) = 10 + \frac{20 - 10}{T}\,t = 10\left(1 + \frac{t}{T}\right)$$

**Average value.**

$$V_{av} = \frac{1}{T}\int_0^T y\,dt = \frac{1}{T}\left[10t + \frac{10t^2}{2T}\right]_0^T = \frac{1}{T}\,(10T + 5T) = \boxed{15\ \text{V (units of y)}}$$

(the mean of the two end values 10 and 20, as expected for a linear ramp).

**RMS value.**

$$V_{rms}^2 = \frac{1}{T}\int_0^T 100\left(1 + \frac{t}{T}\right)^2 dt = \frac{100}{T}\cdot\frac{T}{3}\left[\left(1 + \frac{t}{T}\right)^3\right]_0^T = \frac{100}{3}\,(8 - 1) = 233.33$$

$$\boxed{V_{rms} = \sqrt{233.33} = 15.28\ \text{(units of y)}}$$

*Check.* A ramp of peak-to-peak 10 has an ac rms of $10/\sqrt{12} = 2.887$, and $\sqrt{15^2 + 2.887^2} = 15.28$ ✓.

The period $T = 10$ ms does not enter the results (the average and rms of a periodic wave depend only on its shape). It would give the frequency $f = 1/T = 100$ Hz.

@s 3
**Significance of the power factor.** The power factor $\cos\varphi$ is the ratio of the real (useful) power to the apparent power, $\cos\varphi = P/S$, where $\varphi$ is the phase angle between the voltage and the current. It tells what fraction of the volt-amperes supplied is actually converted into useful work. For a given power $P$ and voltage $V$ the current is $I = P/(V\cos\varphi)$, so a **low power factor means a larger current**: bigger conductor size and copper loss ($I^2R$), poor voltage regulation, a larger rating of generators and transformers (kVA), and a penalty tariff from the supplier. Hence the power factor is kept near 1 (for example by connecting capacitors across inductive loads).

**Impedance of the parallel part.**

$$\begin{gathered}Z_1 = 4 + j8\ \Omega \\ Z_2 = 5 - j8\ \Omega\end{gathered}$$

$$Z_{AB} = \frac{Z_1Z_2}{Z_1 + Z_2} = \frac{(4 + j8)(5 - j8)}{9 + j0} = \frac{20 - j32 + j40 + 64}{9} = \frac{84 + j8}{9} = 9.333 + j0.889\ \Omega$$

**Total impedance.**

$$Z_T = (3 + j6) + (9.333 + j0.889) = 12.333 + j6.889 = \boxed{14.13\angle 29.19^\circ\ \Omega}$$

**Circuit current** (take $V = 200\angle0^\circ$ V):

$$I = \frac{200\angle 0^\circ}{14.13\angle 29.19^\circ} = \boxed{14.16\angle{-29.19^\circ}\ \text{A}}$$

**Power factor.**

$$\cos\varphi = \cos 29.19^\circ = \frac{R}{|Z|} = \frac{12.333}{14.127} = \boxed{0.873\ \text{lagging}}$$

(the circuit is inductive overall, so the current lags the voltage).

**Power consumed.**

$$P = VI\cos\varphi = 200 \times 14.16 \times 0.873 = \boxed{2472\ \text{W}}$$

The same value follows from $P = I^2R_T = 14.16^2 \times 12.333$ W.

$$\begin{gathered}Q = VI\sin\varphi = 200 \times 14.16 \times 0.488 = 1381\ \text{VAr (lagging)} \\ S = VI = 2831\ \text{VA}\end{gathered}$$

*Check by branches.* The voltage across the parallel part is $V_{AB} = I|Z_{AB}| = 132.7$ V, so $I_1 = 132.7/|4 + j8| = 14.84$ A and $I_2 = 132.7/|5 - j8| = 14.07$ A. Then the three resistor losses are $14.84^2 \times 4 = 881$ W, $14.07^2 \times 5 = 990$ W and $14.16^2 \times 3 = 601$ W, which add up to 2472 W ✓.

@s 4
A three-phase supply has three equal voltages displaced by $120^\circ$ in time phase ($R\!-\!Y\!-\!B$ sequence). The three windings of the source (and the three impedances of the load) can be connected in two ways, **star (Y)** or **delta (Δ)**.

```figure caption="Star connection (left), delta connection (centre) and the phasor relation V$_{RY}$ = V$_R$ − V$_Y$ of a star system (right): the line voltage is √3 times the phase voltage and leads V$_R$ by 30°."
import numpy as _np
fig,axs=plt.subplots(1,3,figsize=(6.2,2.3))
a=axs[0]; a.set_aspect("equal"); a.axis("off"); a.set_xlim(-1.7,1.7); a.set_ylim(-1.5,1.9)
for (x,y,t) in ((0,1.4,"R"),(-1.2,-0.9,"Y"),(1.2,-0.9,"B")):
    a.plot([0,x],[0,y],color=ACCENT,lw=2.4); a.plot([x,x*1.15],[y,y*1.15 if y>0 else y*1.12],color=INK,lw=1); a.text(x*1.28,(y*1.15 if y>0 else y*1.12)+(0.12 if y>0 else -0.22),t,ha="center",fontsize=9,fontweight="bold")
a.plot([0],[0],"o",color=INK,ms=5); a.text(0.18,0.05,"N",fontsize=8.5); a.set_title("Star (Y)",fontsize=8.5)
b=axs[1]; b.set_aspect("equal"); b.axis("off"); b.set_xlim(-1.7,1.7); b.set_ylim(-1.5,1.9)
P=[(0,1.3),(-1.3,-0.9),(1.3,-0.9)]
for i,(t) in enumerate("RYB"):
    x,y=P[i]; x2,y2=P[(i+1)%3]; b.plot([x,x2],[y,y2],color=ACCENT,lw=2.4); b.plot([x],[y],"o",color=INK,ms=5)
b.text(0,1.55,"R",ha="center",fontsize=9,fontweight="bold"); b.text(-1.55,-1.1,"Y",ha="center",fontsize=9,fontweight="bold"); b.text(1.55,-1.1,"B",ha="center",fontsize=9,fontweight="bold"); b.set_title("Delta (Δ)",fontsize=8.5)
c=axs[2]; c.set_aspect("equal"); c.axis("off"); c.set_xlim(-1.4,1.4); c.set_ylim(-1.1,1.6)
V={"V$_R$":(0,1.0),"V$_Y$":(_np.cos(-_np.pi/6),_np.sin(-_np.pi/6)),"V$_B$":(-_np.cos(_np.pi/6),-0.5)}
for k,(x,y) in V.items():
    c.annotate("",xy=(x,y),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.4)); c.text(x*1.2,y*1.2+(0.08 if y>0 else -0.1),k,ha="center",fontsize=8.5)
c.annotate("",xy=(0,1.0),xytext=(V["V$_Y$"][0],V["V$_Y$"][1]),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.8)); c.text(0.62,0.45,"V$_{RY}$",fontsize=8.5,color=ACCENT,ha="center")
c.set_title("Line voltage",fontsize=8.5)
```

**1. Star (wye) connection.** The three similar ends (say the finishing ends $R', Y', B'$) are joined at a common point, the **neutral N**, and the other three ends are brought out to the lines $R, Y, B$. A fourth (neutral) wire may be taken out (3-phase 4-wire system, used for 400 V/230 V distribution).

*Relations.* The line current is the same as the phase current. The line voltage is the phasor difference of two phase voltages, e.g. $V_{RY} = V_R - V_Y$. With $V_R = V_{ph}\angle0^\circ$, $V_Y = V_{ph}\angle{-120^\circ}$:

$$V_{RY} = V_{ph}\,[(1 + j0) - (-0.5 - j0.866)] = V_{ph}\,(1.5 + j0.866) = \sqrt{3}\,V_{ph}\angle 30^\circ$$

$$\boxed{V_L = \sqrt{3}\,V_{ph}, \qquad I_L = I_{ph}}$$

The line voltages lead the corresponding phase voltages by $30^\circ$.

**2. Delta (mesh) connection.** The finishing end of each winding is connected to the starting end of the next, forming a closed triangle; the lines are taken from the three junctions. There is no neutral (3-wire system).

*Relations.* The line voltage equals the phase voltage across the winding. At each junction KCL gives the line current as the phasor difference of two phase currents, e.g. $I_R = I_{RY} - I_{BR}$, whose magnitude (balanced load) is $\sqrt{3}$ times the phase current, lagging by $30^\circ$:

$$\boxed{V_L = V_{ph}, \qquad I_L = \sqrt{3}\,I_{ph}}$$

**Power (both connections, balanced load).**

$$\begin{gathered}P = 3V_{ph}I_{ph}\cos\varphi = \sqrt{3}\,V_LI_L\cos\varphi \\ Q = \sqrt{3}\,V_LI_L\sin\varphi \\ S = \sqrt{3}\,V_LI_L\end{gathered}$$

where $\varphi$ is the angle between phase voltage and phase current. The same expression holds for star and delta, but for the same line voltage a load connected in delta takes **three times** the power of the same load in star.

| | Star | Delta |
|---|---|---|
| Line voltage | $\sqrt{3}\,V_{ph}$ | $V_{ph}$ |
| Line current | $I_{ph}$ | $\sqrt{3}\,I_{ph}$ |
| Neutral | available (4-wire) | none (3-wire) |
| Typical use | distribution, alternators, small motors | transmission-side transformers, large motors |

*Source-load combinations* are Y–Y, Y–Δ, Δ–Y and Δ–Δ, each of which can be analysed phase by phase using these relations.

@s 5
**Clamper circuit.** A clamper (dc restorer) is a circuit built from a **capacitor, a diode and a resistor** (with an optional dc battery) that **shifts the entire input waveform up or down by a dc level without changing its shape**. The capacitor charges through the diode to the peak value and then acts as a battery in series with the source; the time constant $RC$ must be much larger than the half period of the signal.

*The circuit of this question* contains no capacitor: the Si diode and 3 V battery form a **biased shunt clipper** (a positive peak limiter). It is solved as drawn.

**Analysis** (Si diode, $V_\gamma = 0.7$ V). The diode anode is at the output node and its cathode is held at $+3$ V by the battery, so the diode conducts only when $v_o > 3 + 0.7 = 3.7$ V.

- **$v_{in} = +6$ V (positive half cycle).** The diode is forward biased, so $v_o = 3 + 0.7 = \mathbf{3.7\ V}$; the remaining $6 - 3.7 = 2.3$ V drops across $R$.
- **$v_{in} = -6$ V (negative half cycle).** The diode is reverse biased (anode at −6 V, cathode at +3 V), so it is open, no current flows, there is no drop across $R$ and $v_o = v_{in} = \mathbf{-6\ V}$ (output terminals open).

```figure caption="Input (dashed) and output (solid) of the circuit of Question 5: the +6 V peaks are clipped to +3.7 V and the −6 V peaks pass unchanged."
fig,ax=plt.subplots(figsize=(5.0,2.4))
t=[0,1,2,3,4,5,6]
ax.step(t,[6,-6,6,-6,6,-6,-6],where="post",color=MUTED,lw=1.2,ls="--",label="v$_{in}$")
ax.step(t,[3.7,-6,3.7,-6,3.7,-6,-6],where="post",color=ACCENT,lw=2.0,label="v$_o$")
ax.axhline(0,color=INK,lw=0.7); ax.axhline(3.7,color=SERIES[1],lw=0.7,ls=":")
ax.text(6.05,3.7,"3.7 V",fontsize=7.5,va="center",color=SERIES[1]); ax.text(6.05,-6,"−6 V",fontsize=7.5,va="center"); ax.text(6.05,6,"6 V",fontsize=7.5,va="center")
ax.set_xticks([]); ax.set_ylim(-8,8); ax.set_xlim(0,6.7); ax.set_ylabel("volts",fontsize=8); ax.legend(fontsize=7.5,loc="center right")
```

**A true clamper for the same input.** If the diode and 3 V battery are used with a series capacitor (capacitor in series with the source, diode with the battery across the output), the −6 V peak charges the capacitor and the output becomes the input shifted up by a constant: $v_o = v_{in} + 2.3\ \text{V}$, where the shift is $6 - 3 - 0.7$ volts. That is a swing from $-3.7$ V to $+8.3$ V: the waveform is *clamped* (the negative peak sits at $-3.7$ V) but its 12 V peak-to-peak shape is unchanged.

@s 6
**Large-signal model of a pn junction diode.** The real $i$–$v$ characteristic $i = I_S\,(e^{v/\eta V_T} - 1)$ is non-linear. For large signals (swings of volts, much larger than the thermal voltage $V_T = 26$ mV) it is replaced by a **piece-wise linear model** with one linear equivalent circuit for each region of operation.

```figure caption="Piece-wise linear (large-signal) model of a diode: ideal diode in series with the cut-in voltage V$_γ$ and the forward resistance r$_f$ (left); the real exponential characteristic (dashed) and its model (solid)."
import numpy as _np
fig=plt.figure(figsize=(5.9,2.5))
ax=fig.add_axes([0,0,0.5,1]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.6,7.0); ax.set_ylim(-0.4,2.4)
terminal(ax,(0,1.0)); wire(ax,[(0,1.0),(0.5,1.0)]); diode(ax,(0.5,1.0),(1.8,1.0),"ideal",side=1,body=0.5,off=0.5)
wire(ax,[(1.8,1.0),(2.1,1.0)]); batt(ax,(2.1,1.0),(3.3,1.0),"V$_γ$",side=1,off=0.5); wire(ax,[(3.3,1.0),(3.6,1.0)])
res(ax,(3.6,1.0),(5.4,1.0),"r$_f$",side=1,body=1.0); wire(ax,[(5.4,1.0),(6.2,1.0)]); terminal(ax,(6.2,1.0))
label(ax,(3.1,-0.1),"forward-bias equivalent: reverse bias = open circuit",size=7.2)
bx=fig.add_axes([0.6,0.2,0.37,0.7])
v=_np.linspace(-1,1.0,400); i=_np.where(v<0,-0.05,1e-3*(_np.exp(v/0.085)-1)); i=_np.clip(i,-0.05,10)
bx.plot(v,i,color=MUTED,ls="--",lw=1.2,label="real diode")
vm=_np.array([-1,0.7,0.7+1.0*0.0,1.0]); 
bx.plot([-1,0.7],[0,0],color=ACCENT,lw=2); bx.plot([0.7,1.0],[0,6],color=ACCENT,lw=2,label="model")
bx.axhline(0,color=INK,lw=0.6); bx.axvline(0,color=INK,lw=0.6); bx.set_ylim(-0.6,7); bx.set_xlim(-1,1.05)
bx.set_xticks([0,0.7]); bx.set_xticklabels(["0","V$_γ$"]); bx.set_yticks([]); bx.set_xlabel("v$_D$",fontsize=8); bx.set_ylabel("i$_D$",fontsize=8); bx.legend(fontsize=7,loc="upper left")
```

**Forward bias ($v_D > V_\gamma$).** The diode conducts. It is modelled by an **ideal diode (a short) in series with a battery $V_\gamma$ and the forward (dynamic) resistance $r_f$**:

$$\begin{gathered}i_D = \frac{v_D - V_\gamma}{r_f} \\ r_f = \frac{\Delta v_D}{\Delta i_D}\end{gathered}$$

Here $V_\gamma$ is the cut-in (offset) voltage, about 0.7 V for silicon and 0.3 V for germanium; $r_f$ is a few ohms to tens of ohms.

**Below cut-in ($0 < v_D < V_\gamma$) and in reverse bias.** The current is negligible: the diode is modelled as an **open circuit** ($i_D = 0$), plus (if needed) a very large reverse resistance $r_r$ (and the small leakage $I_S$).

**Simplifications** used in practice:

| Model | Forward equivalent | Used when |
|---|---|---|
| Ideal diode | short circuit ($V_\gamma = 0$, $r_f = 0$) | supply voltage ≫ 0.7 V |
| Constant-voltage drop (simplified) | ideal diode + $V_\gamma$ ($r_f = 0$) | most hand calculations |
| Piece-wise linear (large signal) | ideal diode + $V_\gamma$ + $r_f$ | accurate rectifier/clipper work |

*Example.* A Si diode with $V_\gamma = 0.7$ V and $r_f = 10\ \Omega$ in series with a 5 V source and $90\ \Omega$: $i = (5 - 0.7)/(90 + 10) = 43$ mA. (The *small-signal model*, in contrast, replaces the diode by the resistance $r_d = \eta V_T/I_D$ about a bias point and is used only for small ac variations.)

@s 7
**Check that the Zener is in breakdown.** If the Zener were removed, the load would receive $18 \times 1000/1250 = 14.4$ V, which is more than $V_Z = 10$ V. So the Zener conducts and holds the output at

$$V_L = V_Z = 10\ \text{V}$$

**Load current.**

$$I_L = \frac{V_Z}{R_L} = \frac{10}{1000} = 10\ \text{mA}$$

**Current through the series resistor** (the total current drawn from the source):

$$I_S = \frac{V_S - V_Z}{R_S} = \frac{18 - 10}{250} = 32\ \text{mA}$$

**Zener current** (KCL at the output node, $I_S = I_Z + I_L$):

$$\boxed{I_Z = I_S - I_L = 32 - 10 = 22\ \text{mA}}$$

**Power dissipated in the Zener.**

$$\boxed{P_Z = V_ZI_Z = 10 \times 22 \times 10^{-3} = 0.22\ \text{W}}$$

(so a 0.5 W Zener is adequate). For reference, the source delivers $18 \times 32\ \text{mA} = 0.576$ W: $P_{R_S} = 0.256$ W, $P_L = 0.1$ W, $P_Z = 0.22$ W, and these add to $0.576$ W ✓.

@s 8
**Step 1: Thevenin equivalent of the base divider.**

$$\begin{gathered}V_{TH} = V_{CC}\frac{R_2}{R_1 + R_2} = 20 \times \frac{10}{30} = 6.667\ \text{V} \\ R_{TH} = R_1 \parallel R_2 = \frac{20 \times 10}{30} = 6.667\ \text{k}\Omega\end{gathered}$$

```figure caption="Voltage-divider bias circuit of Question 8 (V$_{CC}$ = 20 V, R$_1$ = 20 kΩ, R$_2$ = 10 kΩ, R$_C$ = 2 kΩ, R$_E$ = 4 kΩ, β = 100)."
fig,ax=ckt_canvas(4.6,3.9,xlim=(-1.6,5.6),ylim=(-2.4,4.9))
bj=bjt(ax,2.4,1.0)
B,C,E=bj["B"],bj["C"],bj["E"]
wire(ax,[C,(C[0],2.5)]); res(ax,(C[0],3.9),(C[0],2.5),"R$_C$ = 2 kΩ",side=1,off=0.5,body=0.9)
wire(ax,[(C[0],3.9),(C[0],4.3)]); label(ax,(C[0],4.6),"V$_{CC}$ = +20 V",size=8.2)
wire(ax,[(C[0],4.3),(0.5,4.3)]); res(ax,(0.5,4.3),(0.5,2.6),"R$_1$",side=-1,off=0.5,body=0.9); wire(ax,[(0.5,2.6),(0.5,1.0),B]); node(ax,(0.5,1.0))
wire(ax,[(0.5,1.0),(0.5,0.6)]); res(ax,(0.5,0.6),(0.5,-1.0),"R$_2$",side=-1,off=0.5,body=0.9); gnd(ax,(0.5,-1.0))
wire(ax,[E,(E[0],-0.1)]); res(ax,(E[0],-0.1),(E[0],-1.6),"R$_E$ = 4 kΩ",side=1,off=0.5,body=0.9); gnd(ax,(E[0],-1.6))
```

**Step 2: base current** (input loop, $V_{BE} = 0.7$ V, $I_E = (\beta + 1)I_B$):

$$V_{TH} = I_BR_{TH} + V_{BE} + I_ER_E \ \Rightarrow\ I_B = \frac{V_{TH} - V_{BE}}{R_{TH} + (\beta + 1)R_E} = \frac{6.667 - 0.7}{6.667 + 101 \times 4}\ \text{mA} = \frac{5.967}{410.67}\ \text{mA}$$

$$I_B = 14.53\ \mu\text{A}$$

**Step 3: collector and emitter currents.**

$$\begin{gathered}I_C = \beta I_B = 100 \times 14.53\ \mu\text{A} = 1.453\ \text{mA} \\ I_E = (\beta + 1)I_B = 1.467\ \text{mA}\end{gathered}$$

**Step 4: collector-emitter voltage** (output loop):

$$V_{CE} = V_{CC} - I_CR_C - I_ER_E = 20 - 1.453 \times 2 - 1.467 \times 4 = 20 - 2.906 - 5.870 = 11.22\ \text{V}$$

$$\boxed{Q = (V_{CEQ},\ I_{CQ}) = (11.22\ \text{V},\ 1.45\ \text{mA})}$$

**DC load line.** Writing KVL round the collector loop with $I_E \approx I_C$: $V_{CE} = V_{CC} - I_C(R_C + R_E)$. The two end points are

- cut-off ($I_C = 0$): $V_{CE} = V_{CC} = 20$ V,
- saturation ($V_{CE} \approx 0$): $I_{C(sat)} = V_{CC}/(R_C + R_E)$, which is 3.33 mA.

```figure caption="DC load line of Question 8 from (V$_{CE}$ = 20 V, I$_C$ = 0) to (0, 3.33 mA) with the Q point at 11.22 V, 1.45 mA."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.8,2.8))
ax.plot([0,20],[3.333,0],color=ACCENT,lw=2)
ax.plot([11.22],[1.453],"o",color=SERIES[1],ms=7); ax.text(11.6,1.75,"Q (11.22 V, 1.45 mA)",fontsize=8,color=SERIES[1])
ax.plot([11.22,11.22],[0,1.453],color=MUTED,lw=0.8,ls=":"); ax.plot([0,11.22],[1.453,1.453],color=MUTED,lw=0.8,ls=":")
ax.text(0.4,3.1,"saturation: 3.33 mA",fontsize=7.6); ax.text(14.2,0.25,"cut-off: 20 V",fontsize=7.6)
ax.set_xlim(0,22); ax.set_ylim(0,3.8); ax.set_xlabel("V$_{CE}$ (V)",fontsize=8); ax.set_ylabel("I$_C$ (mA)",fontsize=8)
```

**Region of operation.** $I_B = 14.5\ \mu\text{A} > 0$ and $V_{CE} = 11.22\ \text{V} > V_{CE(sat)} \approx 0.2$ V (the Q point is in the middle of the load line, with $I_C = 1.45\ \text{mA} \ll I_{C(sat)}$), so the transistor operates in the **active region**, a good bias point for amplification. *Quick check (the divider is stiff since $\beta R_E = 400\ \text{k}\Omega \gg R_2 = 10\ \text{k}\Omega$):* $V_B \approx 6.67$ V, $V_E \approx 5.97$ V, $I_E \approx 1.49$ mA, $V_{CE} \approx 11.1$ V, which agrees.

@s 9
**BJT as a switch.** A transistor used only in its two extreme regions, **cut-off (switch OFF)** and **saturation (switch ON)**, acts as an electronically controlled switch between the collector and the emitter. It is the basic element of digital logic, relay/LED/motor drivers and the inverter (NOT gate).

```figure caption="NPN transistor switch: the input v$_{in}$ drives the base through R$_B$; the load (here R$_C$) is connected between V$_{CC}$ and the collector, and the output is taken at the collector."
fig,ax=ckt_canvas(4.4,3.3,xlim=(-1.8,5.6),ylim=(-1.2,4.9))
bj=bjt(ax,2.4,1.0)
B,C,E=bj["B"],bj["C"],bj["E"]
wire(ax,[C,(C[0],2.5)]); res(ax,(C[0],3.9),(C[0],2.5),"R$_C$",side=1,off=0.5,body=0.9)
wire(ax,[(C[0],3.9),(C[0],4.3)]); label(ax,(C[0],4.6),"+V$_{CC}$",size=8.4)
node(ax,(C[0],2.0)); wire(ax,[(C[0],2.0),(C[0]+1.2,2.0)]); terminal(ax,(C[0]+1.2,2.0)); label(ax,(C[0]+1.2,1.6),"v$_o$",size=8.4)
wire(ax,[(-0.8,B[1]),(0.0,B[1])]); res(ax,(0.0,B[1]),(B[0]-0.4,B[1]),"R$_B$",side=1,body=0.9); wire(ax,[(B[0]-0.4,B[1]),B])
terminal(ax,(-0.8,B[1])); label(ax,(-0.8,B[1]-0.4),"v$_{in}$",size=8.4)
wire(ax,[E,(E[0],-0.4)]); gnd(ax,(E[0],-0.4))
```

**Operation.**

| | OFF state (cut-off) | ON state (saturation) |
|---|---|---|
| Input | $v_{in} = 0$ (or $< 0.7$ V) | $v_{in} = V_{high}$ (e.g. 5 V) |
| Junctions | both reverse biased | both forward biased |
| Currents | $I_B = 0$, $I_C \approx I_{CEO} \approx 0$ | $I_B > I_{C(sat)}/\beta$, $I_C = I_{C(sat)} = (V_{CC} - V_{CE(sat)})/R_C$ |
| Collector–emitter | open switch | closed switch, $V_{CE(sat)} \approx 0.2$ V |
| Output $v_o$ | $\approx V_{CC}$ (HIGH) | $\approx 0.2$ V (LOW) |

1. **Input low.** With $v_{in} = 0$ the base-emitter junction is not forward biased ($V_{BE} < 0.5$–$0.7$ V), so $I_B = 0$ and $I_C = 0$. There is no drop across $R_C$, so $v_o = V_{CC}$ and the load current is zero.
2. **Input high.** The base current $I_B = (v_{in} - 0.7)/R_B$ must be large enough to **drive the transistor into saturation**: $I_B \ge I_{C(sat)}/\beta$ (in practice 2 to 5 times larger, the *overdrive factor*). Then $v_o = V_{CE(sat)} \approx 0.2$ V and the full $I_{C(sat)}$ flows through the load.

Because $v_o$ is high when $v_{in}$ is low and low when $v_{in}$ is high, the circuit also works as a **NOT gate (inverter)**.

*Numerical example.* $V_{CC} = 5$ V, $R_C = 1\ \text{k}\Omega$, $\beta = 100$, $v_{in} = 5$ V: $I_{C(sat)} = (5 - 0.2)/1\ \text{k}\Omega$, which is 4.8 mA, so the minimum base current is $48\ \mu\text{A}$. Choosing twice that, $I_B = 96\ \mu\text{A}$, gives $R_B = (5 - 0.7)/96\ \mu\text{A} = 44.8\ \text{k}\Omega$, so a standard $47\ \text{k}\Omega$ ($I_B = 91\ \mu\text{A} > 48\ \mu\text{A}$) is used. For an inductive load (relay) a free-wheeling diode across the load protects the transistor from the turn-off spike.

@s 10
**Construction.** The n-channel depletion MOSFET (D-MOSFET) is built on a lightly doped **p-type substrate**. Two heavily doped n⁺ regions, the **source (S)** and **drain (D)**, are diffused into it and are joined by a thin **n-type channel diffused (built in) during manufacture**. A thin layer of **SiO₂** insulator covers the channel and a **metal gate (G)** is deposited on the oxide. Source, drain and gate have metal contacts; the substrate is usually tied to the source. Since the gate is insulated from the channel, $I_G \approx 10^{-12}$ A (very high input resistance, about $10^{10}$ to $10^{14}\ \Omega$).

```figure caption="Cross-section of an n-channel depletion MOSFET. Unlike the enhancement type, a physical n-channel (blue strip) already joins the source and drain n$^+$ regions under the oxide."
import matplotlib.patches as mp, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.4,2.9)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.3,10.3); ax.set_ylim(-1.2,5.4)
ax.add_patch(mp.Rectangle((0,0),10,2.6,fc="#fbf1d2",ec=INK,lw=1.2)); ax.text(5,0.9,"p-type substrate (B)",ha="center",fontsize=8.5)
ax.add_patch(mp.Rectangle((0.9,1.7),2.0,0.9,fc="#bcd3f5",ec=INK,lw=1.1)); ax.text(1.9,2.15,"n$^+$",ha="center",va="center",fontsize=8.5)
ax.add_patch(mp.Rectangle((7.1,1.7),2.0,0.9,fc="#bcd3f5",ec=INK,lw=1.1)); ax.text(8.1,2.15,"n$^+$",ha="center",va="center",fontsize=8.5)
ax.add_patch(mp.Rectangle((2.9,2.1),4.2,0.5,fc="#9fc0f2",ec=INK,lw=1.0)); ax.text(5,2.35,"n-channel (built-in)",ha="center",va="center",fontsize=7.4)
ax.add_patch(mp.Rectangle((2.6,2.6),4.8,0.45,fc="#e6e6e6",ec=INK,lw=1.1)); ax.text(5,2.83,"SiO$_2$ (insulator)",ha="center",va="center",fontsize=7.4)
ax.add_patch(mp.Rectangle((3.0,3.05),4.0,0.7,fc="#c9ccd1",ec=INK,lw=1.1)); ax.text(5,3.4,"metal gate",ha="center",va="center",fontsize=8)
ax.add_patch(mp.Rectangle((1.3,2.6),1.1,1.15,fc="#c9ccd1",ec=INK,lw=1.1)); ax.add_patch(mp.Rectangle((7.6,2.6),1.1,1.15,fc="#c9ccd1",ec=INK,lw=1.1))
ax.add_patch(mp.Rectangle((0,-0.4),10,0.4,fc="#c9ccd1",ec=INK,lw=1.1))
for x,y,t in ((1.85,4.3,"S"),(8.15,4.3,"D"),(5,4.3,"G")):
    ax.plot([x,x],[3.75,4.05],color=INK,lw=1.3); ax.text(x,4.4,t,ha="center",fontsize=10,fontweight="bold")
ax.text(5,-0.9,"substrate contact (usually tied to S)",ha="center",fontsize=7.4,color=MUTED)
```

**Operation** (the drain is positive with respect to the source, $V_{DS} > 0$).

1. **$V_{GS} = 0$.** Electrons flow from the source along the existing channel to the drain, so a substantial drain current already exists: $I_D = I_{DSS}$ (the drain-source saturation current at zero bias). The device is *normally ON*.
2. **$V_{GS} < 0$ (depletion mode).** The negative gate repels electrons from the channel and attracts holes of the substrate towards the oxide. Channel electrons are recombined or pushed away (the channel is **depleted**), the channel narrows and $I_D$ falls. At the **pinch-off voltage** $V_{GS} = V_P$ (a negative value, e.g. −4 V) the channel is completely depleted and $I_D \approx 0$.
3. **$V_{GS} > 0$ (enhancement mode).** The positive gate attracts more electrons into the channel, widening it, so $I_D$ rises *above* $I_{DSS}$. This is what distinguishes the depletion MOSFET from a JFET (which cannot be forward biased at the gate) and the E-MOSFET (which needs $V_{GS} > V_T$ to conduct).
4. **Effect of $V_{DS}$.** For small $V_{DS}$ the channel behaves as a voltage-controlled resistor (ohmic/triode region). The drain end of the channel has a smaller gate-to-channel voltage $V_{GD} = V_{GS} - V_{DS}$, so the channel is narrower there; at $V_{DS} = V_{GS} - V_P$ the channel **pinches off** at the drain end and $I_D$ saturates (almost independent of $V_{DS}$).

**Characteristics.** In the saturation region the drain current obeys Shockley's equation, valid for both $V_{GS} < 0$ and $V_{GS} > 0$:

$$I_D = I_{DSS}\left(1 - \frac{V_{GS}}{V_P}\right)^2$$

```figure caption="Symbol of the n-channel depletion MOSFET (continuous channel line) and its transfer characteristic for I$_{DSS}$ = 8 mA, V$_P$ = −4 V: the curve passes through I$_{DSS}$ at V$_{GS}$ = 0 and continues in both depletion (V$_{GS}$ < 0) and enhancement (V$_{GS}$ > 0) modes."
import numpy as _np
fig=plt.figure(figsize=(5.9,2.6))
ax=fig.add_axes([0,0,0.36,1]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.4,3.6); ax.set_ylim(-0.4,3.4)
m=mosfet(ax,0.7,1.5,kind="n",mode="dep")
wire(ax,[m["D"],(m["D"][0],2.9)]); wire(ax,[m["S"],(m["S"][0],0.1)])
label(ax,(m["G"][0]-0.15,1.5),"G",size=9,ha="right"); label(ax,(m["D"][0]+0.3,2.9),"D",size=9,ha="left"); label(ax,(m["S"][0]+0.3,0.1),"S",size=9,ha="left")
bx=fig.add_axes([0.5,0.2,0.47,0.7])
vg=_np.linspace(-4,2,200); idd=8*(1-vg/(-4))**2
bx.plot(vg,idd,color=ACCENT,lw=2); bx.axhline(0,color=INK,lw=0.6); bx.axvline(0,color=INK,lw=0.6)
bx.plot([0],[8],"o",color=SERIES[1],ms=5); bx.text(0.15,6.2,"I$_{DSS}$ = 8 mA",fontsize=7.5,color=SERIES[1])
bx.text(-3.9,12,"depletion\nmode",fontsize=7.5,color=MUTED); bx.text(0.35,15.5,"enhancement\nmode",fontsize=7.5,color=MUTED)
bx.set_xticks([-4,-2,0,2]); bx.set_xticklabels(["V$_P$","−2","0","2"]); bx.set_xlabel("V$_{GS}$ (V)",fontsize=8); bx.set_ylabel("I$_D$ (mA)",fontsize=8); bx.set_ylim(-1,19)
```

```figure caption="Drain characteristics of the n-channel depletion MOSFET (I$_{DSS}$ = 8 mA, V$_P$ = −4 V): the ohmic region on the left (dashed boundary V$_{DS}$ = V$_{GS}$ − V$_P$) and the saturation (pinch-off) region on the right, for V$_{GS}$ = +1, 0, −1, −2, −3 V."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.8,2.8))
for k,vg in enumerate((1,0,-1,-2,-3)):
    c=SERIES[k%len(SERIES)]; vp=-4; vs=vg-vp; vd=_np.linspace(0,12,300)
    idd=_np.where(vd<vs,(2*8/vp**2)*((vg-vp)*vd-vd**2/2),8*(1-vg/vp)**2)
    ax.plot(vd,idd,color=c,lw=1.6); ax.text(12.2,idd[-1],"V$_{GS}$ = %+d V"%vg if vg else "V$_{GS}$ = 0 V",fontsize=7,va="center")
vv=_np.linspace(0,5,60); ax.plot(vv,0.5*vv**2,color=MUTED,lw=0.9,ls="--")
ax.set_xlim(0,16); ax.set_ylim(0,20); ax.set_xlabel("V$_{DS}$ (V)",fontsize=8); ax.set_ylabel("I$_D$ (mA)",fontsize=8)
```

**Symbol.** The continuous line between drain and source (compare the broken line of the enhancement type) shows that a channel exists at $V_{GS} = 0$; the arrow on the substrate terminal points **inwards** for an n-channel device. Applications: amplifiers with self-bias (no separate gate supply, because $V_{GS} = 0$ already conducts), dual-gate RF mixers, constant-current sources.

@s 11
**Summing amplifier (inverting adder).** Several input voltages $V_1, V_2, \dots, V_n$ are applied through resistors $R_1, R_2, \dots, R_n$ to the inverting input; the non-inverting input is grounded and the feedback resistor $R_f$ connects the output to the inverting input. The output is a weighted sum of the inputs.

```figure caption="Inverting summing amplifier with three inputs V$_1$, V$_2$, V$_3$: the inverting input is a virtual ground and the output is v$_o$ = −R$_f$(V$_1$/R$_1$ + V$_2$/R$_2$ + V$_3$/R$_3$)."
fig,ax=ckt_canvas(5.0,3.2,xlim=(-1.2,8.0),ylim=(-1.4,4.2))
op=opamp(ax,3.0,0.0)
for y,t,r in ((2.6,"V$_1$","R$_1$"),(1.7,"V$_2$","R$_2$"),(0.6,"V$_3$","R$_3$")):
    terminal(ax,(-0.4,y)); label(ax,(-0.8,y),t,size=8.6,ha="right"); wire(ax,[(-0.4,y),(0.2,y)]); res(ax,(0.2,y),(1.7,y),r,side=1,body=0.9); wire(ax,[(1.7,y),(2.2,y)])
wire(ax,[(2.2,2.6),(2.2,0.6),(3.0,0.6)]); node(ax,(2.2,1.7)); node(ax,(2.2,0.6))
wire(ax,[(2.2,2.6),(2.2,3.4),(3.4,3.4)]); res(ax,(3.4,3.4),(5.2,3.4),"R$_f$",side=1,body=1.0); wire(ax,[(5.2,3.4),(6.2,3.4),(6.2,0),(5.4,0)])
wire(ax,[(5.4,0),(7.0,0)]); node(ax,(6.2,0)); terminal(ax,(7.0,0)); label(ax,(7.0,-0.4),"v$_o$",size=8.6)
wire(ax,[(3.0,-0.6),(2.4,-0.6)]); gnd(ax,(2.4,-0.6)); label(ax,(2.0,0.25),"X",size=8)
```

*Derivation.* For an ideal op-amp, the open-loop gain is infinite, so $v_+ = v_-$; the + input is grounded, so $v_- = 0$ (**virtual ground** at the summing node X). The input current is zero, so no current enters the op-amp and all the input currents add up in $R_f$ (KCL at X):

$$I_1 + I_2 + I_3 = I_f$$

$$\frac{V_1 - 0}{R_1} + \frac{V_2 - 0}{R_2} + \frac{V_3 - 0}{R_3} = \frac{0 - v_o}{R_f}$$

$$\boxed{v_o = -R_f\left(\frac{V_1}{R_1} + \frac{V_2}{R_2} + \frac{V_3}{R_3}\right)}$$

For $n$ inputs, $v_o = -R_f\sum_{k=1}^{n}V_k/R_k$. The inputs do not interact with one another, because the summing node is a virtual ground (each input sees only its own resistor to ground).

**Special cases.**

- **Equal input resistors $R_1 = R_2 = R_3 = R$:** $v_o = -\dfrac{R_f}{R}(V_1 + V_2 + V_3)$.
- **Adder (unity weights), $R_f = R$:** $v_o = -(V_1 + V_2 + V_3)$. A following inverter restores the sign.
- **Averaging amplifier, $R_f = R/n$** ($n$ inputs): $v_o = -\dfrac{V_1 + V_2 + \dots + V_n}{n}$.
- **Scaling adder:** different $R_k$ give different weights $R_f/R_k$ (used as a D/A converter with binary-weighted resistors).

*Example.* $V_1 = 1$ V, $V_2 = 2$ V, $V_3 = 3$ V with $R_1 = R_2 = R_3 = R_f = 10\ \text{k}\Omega$: $v_o = -(1 + 2 + 3) = -6$ V.

@s 12
**Barkhausen criteria.** An amplifier of gain $A$ with a positive-feedback network of feedback factor $\beta$ produces sustained oscillations at a frequency $f_0$ if at that frequency

1. the magnitude of the loop gain is unity, $\ |A\beta| = 1$, and
2. the total phase shift around the loop is $0^\circ$ or an integer multiple of $360^\circ$ (the feedback is positive).

(If $|A\beta| < 1$ the oscillations die out; if $|A\beta| > 1$ they grow until the amplifier saturates, so for start-up $|A\beta|$ is made slightly greater than 1 and the amplitude is then limited by non-linearity.)

**Wien bridge oscillator.** It consists of a non-inverting op-amp amplifier of gain $A = 1 + R_f/R_1$, with a **lead-lag (Wien) network** as the positive feedback path: a series $RC$ arm ($Z_1$) from the output to the + input, and a parallel $RC$ arm ($Z_2$) from the + input to ground. The resistors $R_f$ and $R_1$ provide the negative feedback that sets the gain.

```figure caption="Wien bridge oscillator: the series R-C arm Z$_1$ and the parallel R-C arm Z$_2$ feed back positively to the + input; R$_f$ and R$_1$ set the amplifier gain 1 + R$_f$/R$_1$ (= 3 at the start-up limit)."
fig,ax=ckt_canvas(5.4,4.0,xlim=(-1.8,9.2),ylim=(-4.2,3.2))
op=opamp(ax,4.6,0.0)
wire(ax,[(7.0,0),(8.4,0)]); node(ax,(7.6,0)); terminal(ax,(8.4,0)); label(ax,(8.4,-0.4),"v$_o$",size=8.4)
wire(ax,[(7.6,0),(7.6,1.9),(6.3,1.9)]); res(ax,(6.3,1.9),(4.7,1.9),"R$_f$",side=1,body=1.0)
wire(ax,[(4.7,1.9),(4.0,1.9),(4.0,0.6),(4.6,0.6)]); node(ax,(4.0,0.6))
wire(ax,[(4.0,0.6),(3.4,0.6)]); res(ax,(3.4,0.6),(3.4,2.4),"R$_1$",side=-1,off=0.5,body=0.9); gnd(ax,(3.4,2.4),down=False)
wire(ax,[(4.6,-0.6),(2.4,-0.6),(2.4,-2.8)]); node(ax,(2.4,-1.7))
wire(ax,[(7.6,0),(7.6,-2.8),(5.6,-2.8)]); res(ax,(5.6,-2.8),(4.2,-2.8),"R",side=1,body=0.9); cap(ax,(4.2,-2.8),(2.4,-2.8),"C",side=1)
wire(ax,[(2.4,-1.7),(1.2,-1.7)]); node(ax,(1.2,-1.7))
res(ax,(1.2,-1.7),(1.2,-3.5),"R",side=-1,off=0.5,body=0.9)
wire(ax,[(1.2,-1.7),(0.2,-1.7)]); cap(ax,(0.2,-1.7),(0.2,-3.5),"C",side=-1,off=0.5)
wire(ax,[(0.2,-3.5),(1.2,-3.5)]); gnd(ax,(0.7,-3.5))
label(ax,(3.3,-3.4),"Z$_1$ (series RC)",size=7.6); label(ax,(-1.3,-2.6),"Z$_2$",size=8)
```

*Feedback factor.* With $Z_1 = R + \dfrac{1}{j\omega C}$ and $Z_2 = R\parallel\dfrac{1}{j\omega C} = \dfrac{R}{1 + j\omega RC}$, the fraction of the output fed back to the + input is

$$\beta = \frac{v_f}{v_o} = \frac{Z_2}{Z_1 + Z_2}$$

$$\beta = \frac{\dfrac{R}{1 + j\omega RC}}{R + \dfrac{1}{j\omega C} + \dfrac{R}{1 + j\omega RC}} = \frac{j\omega RC}{(1 + j\omega RC)^2 + j\omega RC} = \frac{j\omega RC}{1 - \omega^2R^2C^2 + 3j\omega RC}$$

Dividing numerator and denominator by $j\omega RC$:

$$\boxed{\beta = \frac{1}{3 + j\left(\omega RC - \dfrac{1}{\omega RC}\right)}}$$

*Frequency of oscillation.* The amplifier is non-inverting, so $A$ is real and has zero phase shift. The loop phase is zero only if $\beta$ is real, i.e. the imaginary part vanishes:

$$\omega RC - \frac{1}{\omega RC} = 0 \ \Rightarrow\ \omega_0 = \frac{1}{RC}$$

$$\boxed{f_0 = \frac{1}{2\pi RC}}$$

(With unequal elements, $R_1, C_1$ in series and $R_2, C_2$ in parallel, $f_0 = 1/(2\pi\sqrt{R_1R_2C_1C_2})$.)

*Condition for sustained oscillations.* At $\omega_0$, $\beta = 1/3$ with zero phase. The Barkhausen condition $|A\beta| = 1$ requires

$$A = 1 + \frac{R_f}{R_1} = 3 \ \Rightarrow\ \boxed{R_f = 2R_1}$$

In practice $R_f$ is made slightly larger than $2R_1$ so that oscillations start, and amplitude is stabilised automatically by replacing $R_f$ with a thermistor or lamp (whose resistance rises as the amplitude grows), or by anti-parallel diodes across part of $R_f$.

*Example.* $R = 10\ \text{k}\Omega$, $C = 0.01\ \mu\text{F}$: $f_0 = 1/(2\pi \times 10^4 \times 10^{-8})$, which is 1.59 kHz, with $R_1 = 10\ \text{k}\Omega$ and $R_f \gtrsim 20\ \text{k}\Omega$.

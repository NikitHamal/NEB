---
file: NEBians-IOE-Past-Paper-Fundamental-of-Electrical-and-Electronics-Engineering-EX101-2081-Baishakh.pdf
subject: Fundamental of Electrical and Electronics Engineering
level: BE · Year I / Part I
code: EX 101
year_bs: 2081 Baishakh
cal: BS
year_ad: 2024
stream: BEI, BCT, BME, BIE, BAM, BAS
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Explain superposition theorem with suitable example. Find the maximum power that can be delivered to the load resistor $R_L$ of the circuit shown in the figure below. [[2+4]]

```figure caption="Question 1: 20 V source, 5 Ω, 10 Ω shunt, 10 Ω series, 4 A current source (arrow up) and the variable load R$_L$."
fig,ax=ckt_canvas(5.8,2.9,xlim=(-1.4,9.2),ylim=(-0.5,3.9))
vsrc(ax,(0,0),(0,3),"20 V",side=-1)
wire(ax,[(0,3),(0.8,3)]); res(ax,(0.8,3),(2.8,3),"5 Ω",side=1)
wire(ax,[(2.8,3),(3.3,3)]); res(ax,(3.3,3),(5.3,3),"10 Ω",side=1)
wire(ax,[(5.3,3),(8,3)])
res(ax,(3.0,3),(3.0,0),"10 Ω",side=-1,off=0.55)
isrc(ax,(5.5,0),(5.5,3),"4 A",side=-1)
res(ax,(8,3),(8,0),"R$_L$",side=1,off=0.5)
wire(ax,[(0,0),(8,0)])
for p in ((3.0,3),(5.5,3),(5.5,0),(3.0,0)): node(ax,p)
```

@q 2
Define trans-conductance, trans-impedance and gain. [[3]]

@q 3
Define RMS and average value of ac signal. Find the RMS and average value of half wave rectified sinusoidal waveform $V = V_m\sin\omega t$. [[2+4]]

@q 4
What are the two ways of connecting a 3-phase system and mention their relation between phase and line quantities. Derive the expression for series connected RC with phasor diagram. [[2+4]]

@q 5
From the given circuit, find the branch current, total current, overall power factor, real power and reactive power. [[6]]

```figure caption="Question 5: Z$_C$ = 3 + j2.5 Ω in series with the parallel branches Z$_A$ = 2 + j1.5 Ω and Z$_B$ = 5 − j3.5 Ω, supplied from 200 V, 50 Hz."
fig,ax=ckt_canvas(6.2,3.6,xlim=(-2.3,10.8),ylim=(-1.0,4.6))
acsrc(ax,(0,0),(0,3.0),None); label(ax,(-0.5,1.5),"200 V\n50 Hz",ha="right",size=8.2)
wire(ax,[(0,3.0),(0.5,3.0)])
res(ax,(0.5,3.0),(1.8,3.0),"3 Ω",side=1,body=0.9); ind(ax,(1.8,3.0),(3.2,3.0),"j2.5 Ω",side=1,body=1.1)
wire(ax,[(3.2,3.0),(4.0,3.0),(4.0,3.8),(5.0,3.8)])
res(ax,(5.0,3.8),(6.3,3.8),"2 Ω",side=1,body=0.9); ind(ax,(6.3,3.8),(7.7,3.8),"j1.5 Ω",side=1,body=1.1)
wire(ax,[(7.7,3.8),(8.6,3.8),(8.6,2.2),(7.7,2.2)])
wire(ax,[(4.0,3.0),(4.0,2.2),(5.0,2.2)])
res(ax,(5.0,2.2),(6.3,2.2),"5 Ω",side=-1,body=0.9); cap(ax,(6.3,2.2),(7.7,2.2),"−j3.5 Ω",side=-1)
wire(ax,[(8.6,3.0),(9.4,3.0),(9.4,0),(0,0)])
node(ax,(4.0,3.0)); node(ax,(8.6,3.0))
label(ax,(3.7,3.3),"A"); label(ax,(8.95,3.3),"B"); label(ax,(6.35,3.25),"Z$_A$",size=8); label(ax,(6.35,2.75),"Z$_B$",size=8); label(ax,(2.0,2.3),"Z$_C$")
arrow(ax,(3.1,3.2),(3.9,3.2),None); label(ax,(3.5,3.55),"I$_C$",size=8)
```

@q 6
Explain the clipper and clamper circuits with suitable examples. [[2+2]]

@q 7
Draw the circuit diagram of half wave rectifier with its input output voltage waveforms and explain in brief. [[4]]

@q 8
Design a Zener diode voltage regulator that will maintain an output voltage of 20 V across 1-KΩ load with an input that will vary between 30 V and 50 V. Determine the proper value of $R_S$ and the maximum Zener current $I_{ZM}$. [[2+2]]

@q 9
Describe the input and output characteristics of Common Emitter BJT configuration with various region of operation. [[4]]

@q 10
For the given Emitter-bias BJT network, find Q point. Draw dc load line and find region of operation. [[2+1+1]]

```figure caption="Question 10: emitter-bias network (V$_{CC}$ = +20 V, R$_B$ = 430 kΩ, R$_C$ = 2 kΩ, R$_E$ = 1 kΩ with bypass capacitor C$_E$ = 40 μF, β = 50)."
fig,ax=ckt_canvas(5.0,3.9,xlim=(-1.8,6.4),ylim=(-2.6,4.8))
bj=bjt(ax,2.4,1.0)
B,C,E=bj["B"],bj["C"],bj["E"]
wire(ax,[C,(C[0],2.5)]); res(ax,(C[0],3.9),(C[0],2.5),"2 kΩ",side=1,body=0.9)
wire(ax,[(C[0],3.9),(C[0],4.3)]); label(ax,(C[0],4.6),"+20 V",size=8.4)
wire(ax,[(C[0],4.3),(0.5,4.3)]); res(ax,(0.5,4.3),(0.5,2.4),"430 kΩ",side=-1,off=0.65,body=1.2); wire(ax,[(0.5,2.4),(0.5,1.0),B]); node(ax,(0.5,1.0))
cap(ax,(-1.3,1.0),(0.5,1.0),"10 μF",side=1,off=0.5); terminal(ax,(-1.3,1.0)); label(ax,(-1.3,0.6),"v$_i$",size=8.4)
node(ax,(C[0],2.2)); cap(ax,(C[0],2.2),(5.7,2.2),"10 μF",side=1,off=0.5); terminal(ax,(5.7,2.2)); label(ax,(5.7,1.8),"v$_o$",size=8.4)
wire(ax,[E,(E[0],-0.5)]); node(ax,(E[0],-0.5))
res(ax,(E[0]-0.9,-0.5),(E[0]-0.9,-1.8),"1 kΩ",side=-1,off=0.65,body=0.9)
cap(ax,(E[0]+0.9,-0.5),(E[0]+0.9,-1.8),"C$_E$",side=1,off=0.5)
wire(ax,[(E[0]-0.9,-0.5),(E[0]+0.9,-0.5)]); wire(ax,[(E[0]-0.9,-1.8),(E[0]+0.9,-1.8)]); node(ax,(E[0],-1.8)); gnd(ax,(E[0],-1.8))
```

@q 11
Describe the construction and working principle of n-channel enhancement type MOSFET. [[4]]

@q 12
Derive voltage gain of closed loop non-inverting op-amp configuration. [[4]]

@q 13
State Barkhausen criteria. Draw and explain circuit diagram of Relaxation oscillator (square wave generator). Write its frequency of oscillation. [[1+3+1]]
<!-- SOLUTIONS -->

@s 1
**Superposition theorem.** In a *linear, bilateral* network containing more than one independent source, the response (current or voltage) in any element equals the **algebraic sum of the responses produced by each independent source acting alone**, with all the other independent sources replaced by their internal resistances: an ideal voltage source is **short-circuited** and an ideal current source is **open-circuited**. Dependent sources stay in the network. The theorem holds only for linear quantities (voltage, current), **not for power**, since $P = I^2R$ is quadratic.

*Example (the circuit of this question, open-circuit voltage $V_{oc}$ across the load terminals).*

- *20 V source alone* (4 A source opened, $R_L$ removed): no current flows in the right-hand 10 Ω, so $V_{oc}' = 20\times\dfrac{10}{5+10}$, which is $13.33$ V.
- *4 A source alone* (20 V shorted): the 4 A must return through the 10 Ω series resistor, then through $5\parallel10 = 3.333\ \Omega$: $V_{oc}''= 4\times(10+3.333)$, which is $53.33$ V.
- Both together: $V_{oc} = 13.33 + 53.33$, i.e. $66.67$ V, the same as by nodal analysis.

**Maximum power transfer.** Reduce the network to its Thévenin equivalent seen by $R_L$.

*Open-circuit voltage.* Without $R_L$ the 4 A source forces its current down through the series 10 Ω into node N (the junction of 5 Ω, 10 Ω shunt and 10 Ω series). KCL at N, with $V_N$ the node voltage:

$$\frac{20 - V_N}{5} + 4 = \frac{V_N}{10} \ \Rightarrow\ 8 = 0.3\,V_N \ \Rightarrow\ V_N = 26.67\ \text{V}$$

The output node is 4 A × 10 Ω above N:

$$V_{th} = V_{oc} = V_N + 4 \times 10 = 26.67 + 40 = 66.67\ \text{V}$$

*Thévenin resistance* (20 V shorted, 4 A opened):

$$R_{th} = (5 \parallel 10) + 10 = 3.333 + 10 = 13.33\ \Omega$$

```figure caption="Thévenin equivalent of Question 1: V$_{th}$ = 66.67 V, R$_{th}$ = 13.33 Ω, feeding the load R$_L$."
fig,ax=ckt_canvas(4.4,2.2,xlim=(-1.5,6.6),ylim=(-0.4,3.4))
batt(ax,(0,0.2),(0,2.6),"66.67 V",side=-1)
wire(ax,[(0,2.6),(0,3.0),(0.6,3.0)]); res(ax,(0.6,3.0),(2.6,3.0),"13.33 Ω",side=1)
wire(ax,[(2.6,3.0),(5.0,3.0)]); res(ax,(5.0,3.0),(5.0,0),"R$_L$",side=1,off=0.5)
wire(ax,[(0,0.2),(0,0),(5.0,0)])
```

**Condition.** The power in the load is $P_L = I^2R_L = \dfrac{V_{th}^2R_L}{(R_{th}+R_L)^2}$. Setting $dP_L/dR_L = 0$:

$$\frac{(R_{th}+R_L)^2 - 2R_L(R_{th}+R_L)}{(R_{th}+R_L)^4} = 0 \ \Rightarrow\ R_{th} - R_L = 0 \ \Rightarrow\ R_L = R_{th}$$

So the maximum power is delivered when $R_L = R_{th} = 13.33\ \Omega$, and then

$$\boxed{P_{max} = \frac{V_{th}^2}{4R_{th}} = \frac{(66.67)^2}{4 \times 13.33} = 83.33\ \text{W}}$$

(The efficiency at that point is only 50%: half the power is dissipated in $R_{th}$. The load current is $I = 66.67/26.67$, i.e. 2.5 A, so $P_L$ is $2.5^2 \times 13.33 = 83.3$ W ✓.)

@s 2
**Trans-conductance ($g_m$).** The ratio of the output *current* to the input *voltage* of a two-port device or amplifier (a voltage-controlled current source, VCCS). Its unit is the siemens (A/V):

$$g_m = \frac{I_{out}}{V_{in}}$$

For a BJT $g_m = \dfrac{\Delta I_C}{\Delta V_{BE}} = \dfrac{I_C}{V_T}$ (about 40 mS per mA at room temperature); for a FET $g_m = \dfrac{\Delta I_D}{\Delta V_{GS}}$.

**Trans-impedance ($r_m$ or $R_m$).** The ratio of the output *voltage* to the input *current* (a current-controlled voltage source, CCVS). Its unit is the ohm:

$$r_m = \frac{V_{out}}{I_{in}}$$

An op-amp transimpedance amplifier (photodiode amplifier) has $V_o = -I_{in}R_f$, i.e. $r_m = -R_f$.

**Gain.** The ratio of the output quantity to the input quantity of an amplifier, a measure of the amplification. A pure ratio with no unit (it may be quoted in decibels):

| Gain | Definition | In decibels |
|---|---|---|
| Voltage gain $A_v$ | $V_o/V_i$ | $20\log_{10}\lvert A_v\rvert$ |
| Current gain $A_i$ | $I_o/I_i$ | $20\log_{10}\lvert A_i\rvert$ |
| Power gain $A_p$ | $P_o/P_i = A_vA_i$ | $10\log_{10}A_p$ |

Voltage gain and current gain are *dimensionless*; trans-conductance and trans-impedance are the other two (mixed) ratios. Together they are the four gain parameters of the four amplifier models (voltage, current, transconductance and transresistance amplifiers).

@s 3
**RMS (effective) value.** The RMS value of an alternating quantity is the value of the *direct* current (or voltage) that produces the same heating effect (same power in a given resistor) as the alternating quantity does over one full period. It is the square **R**oot of the **M**ean of the **S**quare:

$$V_{rms} = \sqrt{\frac{1}{T}\int_0^T v^2(t)\,dt}$$

**Average value.** The arithmetic mean of all the instantaneous values over one period. For a symmetrical wave the mean over the full cycle is zero, so the average over a half cycle (or of the rectified wave) is taken:

$$V_{av} = \frac{1}{T}\int_0^T v(t)\,dt$$

For a pure sine wave $V_m\sin\omega t$: $V_{rms} = V_m/\sqrt2 = 0.707V_m$ and (half-cycle) $V_{av} = 2V_m/\pi = 0.637V_m$.

**Half-wave rectified sine.** $v = V_m\sin\omega t$ for $0 \le \omega t \le \pi$ and $v = 0$ for $\pi \le \omega t \le 2\pi$.

```figure caption="Half-wave rectified sinusoid V = V$_m$ sin ωt for 0 ≤ ωt ≤ π and zero for the next half cycle. The dashed lines mark the average V$_m$/π and the RMS value V$_m$/2."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,4*np.pi,800)
v=np.where(np.sin(t)>0,np.sin(t),0)
fig,ax=plt.subplots(figsize=(5.4,2.4))
ax.plot(t,v,color=ACCENT); ax.axhline(0,color=INK,lw=0.7)
ax.axhline(1/np.pi,color=SERIES[1],ls="--",lw=1); ax.axhline(0.5,color=SERIES[2],ls="--",lw=1)
ax.text(4*np.pi+0.1,1/np.pi-0.03,"V$_{av}$ = V$_m$/π",fontsize=7.2,color=SERIES[1],va="top")
ax.text(4*np.pi+0.1,0.52,"V$_{rms}$ = V$_m$/2",fontsize=7.2,color=SERIES[2],va="bottom")
ax.set_xticks([0,np.pi,2*np.pi,3*np.pi,4*np.pi]); ax.set_xticklabels(["0","π","2π","3π","4π"]); ax.set_yticks([0,1]); ax.set_yticklabels(["0","V$_m$"])
ax.set_xlabel("ωt"); ax.set_ylabel("v"); ax.set_xlim(0,4*np.pi+3.4)
```

*Average value.*

$$V_{av} = \frac{1}{2\pi}\int_0^{\pi}V_m\sin\theta\,d\theta = \frac{V_m}{2\pi}\Big[-\cos\theta\Big]_0^{\pi} = \frac{V_m}{2\pi}(1+1)$$

$$\boxed{V_{av} = \frac{V_m}{\pi} = 0.318\,V_m}$$

*RMS value.*

$$V_{rms}^2 = \frac{1}{2\pi}\int_0^{\pi}V_m^2\sin^2\theta\,d\theta = \frac{V_m^2}{2\pi}\int_0^{\pi}\frac{1-\cos2\theta}{2}\,d\theta = \frac{V_m^2}{4\pi}\Big[\theta - \frac{\sin2\theta}{2}\Big]_0^{\pi} = \frac{V_m^2}{4}$$

$$\boxed{V_{rms} = \frac{V_m}{2} = 0.5\,V_m}$$

*Form factor* $= V_{rms}/V_{av} = \pi/2 = 1.57$ and *peak factor* $= V_m/V_{rms} = 2$. For example, a half-wave rectified 10 V peak wave has $V_{av} = 3.18$ V and $V_{rms} = 5$ V.

@s 4
**Two ways of connecting a three-phase system:** the **star (Y)** connection and the **delta (Δ, mesh)** connection.

```figure caption="Star (left) and delta (right) connection of the three phase windings. In star the three similar ends are joined at the neutral N; in delta the windings form a closed triangle."
import numpy as np, matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(5.6,2.6))
ax=axs[0]; ax.axis("off"); ax.set_aspect("equal")
ends={"R":(-1.6,1.1),"Y":(1.6,1.1),"B":(0,-1.7)}
for k,(x,y) in ends.items():
    ax.plot([0,x],[0,y],color=ACCENT,lw=2.2); ax.text(x*1.18,y*1.18,k,ha="center",va="center",fontsize=9,fontweight="bold")
    ax.text(x*0.5+0.18*(1 if x>=0 else -1),y*0.5,"E$_{ph}$",fontsize=7,color=MUTED,ha="center")
ax.plot([0],[0],"o",color=INK,ms=5); ax.text(0.15,0.2,"N",fontsize=8.5)
ax.set_xlim(-2.4,2.4); ax.set_ylim(-2.3,1.9); ax.set_title("Star (Y)",fontsize=8.8)
ax=axs[1]; ax.axis("off"); ax.set_aspect("equal")
P=[(-1.6,-1.1),(1.6,-1.1),(0,1.6)]; nm=["Y","B","R"]
for i in range(3):
    a=P[i]; b=P[(i+1)%3]; ax.plot([a[0],b[0]],[a[1],b[1]],color=ACCENT,lw=2.2)
    ax.plot([a[0]],[a[1]],"o",color=INK,ms=5)
for p,n in zip(P,nm): ax.text(p[0]*1.22,p[1]*1.22+(0.1 if p[1]>0 else -0.05),n,ha="center",va="center",fontsize=9,fontweight="bold")
ax.set_xlim(-2.4,2.4); ax.set_ylim(-2.3,2.1); ax.set_title("Delta (Δ)",fontsize=8.8)
```

| Quantity | Star (Y) | Delta (Δ) |
|---|---|---|
| Line voltage $V_L$ | $V_L = \sqrt3\,V_{ph}$ (leads the phase voltage by $30^\circ$) | $V_L = V_{ph}$ |
| Line current $I_L$ | $I_L = I_{ph}$ | $I_L = \sqrt3\,I_{ph}$ (lags the phase current by $30^\circ$) |
| Neutral | available (3-phase 4-wire, two voltages) | not available |
| Power (balanced) | $P = \sqrt3\,V_LI_L\cos\varphi = 3V_{ph}I_{ph}\cos\varphi$ | same expression: $P = \sqrt3\,V_LI_L\cos\varphi$ |

*Proof for star.* $V_{RY} = V_R - V_Y = V_{ph}\angle0^\circ - V_{ph}\angle{-120^\circ} = \sqrt3\,V_{ph}\angle30^\circ$. *For delta*, $I_R = I_{RY} - I_{BR} = \sqrt3\,I_{ph}\angle{-30^\circ}$ by the same vector subtraction.

**Series RC circuit.** A resistor $R$ and a capacitor $C$ in series across $v = V_m\sin\omega t$ (rms voltage $V$, frequency $f$).

```figure caption="Series R–C circuit and its phasor diagram: V$_R$ is in phase with I, V$_C$ lags I by 90°, so the supply voltage V lags the current I by φ."
import numpy as _np
fig=plt.figure(figsize=(5.8,2.5))
ax=fig.add_axes([0,0,0.5,1]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1,5.2); ax.set_ylim(-1,3.2)
acsrc(ax,(0,0),(0,2.2),"V",side=-1)
wire(ax,[(0,2.2),(0.4,2.2)]); res(ax,(0.4,2.2),(2.0,2.2),"R",side=1); cap(ax,(2.0,2.2),(3.6,2.2),"C",side=1)
wire(ax,[(3.6,2.2),(4.4,2.2),(4.4,0),(0,0)])
arrow(ax,(0.55,2.75),(1.35,2.75),"I",off=0.2)
bx=fig.add_axes([0.52,0.05,0.46,0.9]); bx.set_aspect("equal"); bx.axis("off"); bx.set_xlim(-0.4,3.4); bx.set_ylim(-2.4,0.9)
bx.annotate("",xy=(3,0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.8)); bx.text(1.5,0.12,"V$_R$ = IR  (along I)",fontsize=7.3,color=ACCENT,ha="center")
bx.annotate("",xy=(3,-2.0),xytext=(3,0),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1.8)); bx.text(3.05,-1.0,"V$_C$ = IX$_C$",fontsize=7.3,color=SERIES[1],rotation=90,va="center",ha="left")
bx.annotate("",xy=(3,-2.0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.8)); bx.text(1.0,-1.35,"V",fontsize=9,ha="center",color=INK)
th=_np.linspace(0,-_np.arctan(2/3),30); bx.plot(0.9*_np.cos(th),0.9*_np.sin(th),color=INK,lw=1); bx.text(1.05,-0.35,"φ",fontsize=9)
bx.text(-0.35,0.12,"I (ref)",fontsize=7.3,color=MUTED)
```

Let the current be $I$ (taken as the reference phasor). The voltage across the resistor is in phase with $I$, and the voltage across the capacitor **lags** $I$ by $90^\circ$:

$$\begin{gathered} V_R = IR \angle 0^\circ \\ V_C = IX_C\angle{-90^\circ}, \qquad X_C = \frac{1}{\omega C} = \frac{1}{2\pi fC} \end{gathered}$$

By KVL the phasor sum is the supply voltage; from the right-angled voltage triangle:

$$V = \sqrt{V_R^2 + V_C^2} = I\sqrt{R^2 + X_C^2}$$

Hence the **impedance**, **current**, **phase angle** and **power factor**:

$$\begin{gathered} \boxed{Z = R - jX_C = \sqrt{R^2 + X_C^2}\ \angle{-\tan^{-1}\frac{X_C}{R}}} \\ I = \frac{V}{Z} = \frac{V}{\sqrt{R^2 + \left(\dfrac{1}{\omega C}\right)^2}} \\ \varphi = \tan^{-1}\frac{X_C}{R} \ \ (\text{current leads the voltage}), \qquad \cos\varphi = \frac{R}{Z} \end{gathered}$$

*Power:* $P = VI\cos\varphi = I^2R$ (W), reactive power $Q = VI\sin\varphi = I^2X_C$ (var, capacitive) and apparent power $S = VI = I^2Z$ (VA), with $S^2 = P^2 + Q^2$. In the time domain, $i = I_m\sin(\omega t + \varphi)$ when $v = V_m\sin\omega t$. The average power drawn by the capacitor itself is zero.

*Numerical illustration:* $R = 100\ \Omega$, $C = 31.8\ \mu$F, 230 V, 50 Hz give $X_C = 100\ \Omega$, $Z = 141.4\ \Omega$, $I = 1.63$ A, $\cos\varphi = 0.707$ leading, $P = 266$ W.

@s 5
Take the source as the reference, $\bar V = 200\angle0^\circ$ V. The branches are:

$$\begin{gathered} Z_A = 2 + j1.5 = 2.5\angle36.87^\circ\ \Omega \\ Z_B = 5 - j3.5 = 6.103\angle{-34.99^\circ}\ \Omega \\ Z_C = 3 + j2.5 = 3.905\angle39.81^\circ\ \Omega \end{gathered}$$

*Parallel combination of $Z_A$ and $Z_B$* (between A and B):

$$Z_{AB} = \frac{Z_AZ_B}{Z_A + Z_B} = \frac{2.5\angle36.87^\circ \times 6.103\angle{-34.99^\circ}}{7 - j2} = \frac{15.26\angle1.88^\circ}{7.28\angle{-15.95^\circ}} = 2.096\angle17.82^\circ = 1.995 + j0.642\ \Omega$$

*Total impedance:*

$$Z_T = Z_C + Z_{AB} = (3 + 1.995) + j(2.5 + 0.642) = 4.995 + j3.142 = 5.901\angle32.17^\circ\ \Omega$$

**Total current** (this is the current $I_C$ in the figure):

$$\boxed{I_C = \frac{200\angle0^\circ}{5.901\angle32.17^\circ} = 33.89\angle{-32.17^\circ}\ \text{A}}$$

**Voltage across the parallel part:**

$$V_{AB} = I_CZ_{AB} = 33.89 \times 2.096\angle(-32.17^\circ + 17.82^\circ) = 71.03\angle{-14.34^\circ}\ \text{V}$$

**Branch currents** (current divider or $V_{AB}/Z$):

$$\boxed{I_A = \frac{71.03\angle{-14.34^\circ}}{2.5\angle36.87^\circ} = 28.41\angle{-51.21^\circ}\ \text{A}}$$

$$\boxed{I_B = \frac{71.03\angle{-14.34^\circ}}{6.103\angle{-34.99^\circ}} = 11.64\angle20.65^\circ\ \text{A}}$$

*Check (KCL):* $I_A + I_B = (17.80 - j22.15) + (10.89 + j4.10)$, i.e. $28.69 - j18.05 = 33.89\angle{-32.2^\circ}$ A, equal to $I_C$ ✓.

**Overall power factor:**

$$\boxed{\cos\varphi = \cos32.17^\circ = \frac{R_T}{Z_T} = \frac{4.995}{5.901} = 0.847\ \text{lagging}}$$

**Real power and reactive power:**

$$\begin{gathered} P = VI\cos\varphi = 200 \times 33.89 \times 0.8465 = \mathbf{5738\ W} \\ Q = VI\sin\varphi = 200 \times 33.89 \times 0.5324 = \mathbf{3609\ var\ (lagging)} \\ S = VI = 6778\ \text{VA} \end{gathered}$$

*Check by branch losses:* the sum $I_C^2(3) + I_A^2(2) + I_B^2(5)$ is $3445.7 + 1614.6 + 677.4 = 5737.7$ W ✓. The reactive check: $I_C^2(2.5) + I_A^2(1.5) - I_B^2(3.5)$ is $2871.4 + 1211 - 474.2 = 3608$ var ✓.

@s 6
**Clipper (limiter).** A clipper is a diode-resistor network that **removes (clips) the part of an input waveform that lies above or below a chosen reference level** without altering the remaining part. It is used for wave shaping, for protecting circuits from voltage spikes, and in noise limiting and amplitude-modulation detectors. Types: *positive* (cuts the positive peaks) or *negative* clipper; *series* or *shunt* (diode in series or in parallel with the load); *unbiased* (clips at about ±0.7 V) or *biased* (a dc battery $V_R$ shifts the clipping level).

**Example: biased shunt positive clipper** (Si diode, $V_\gamma = 0.7$ V).

```figure caption="Biased positive clipper (left) and its waveforms for v$_i$ = 10 sin ωt, V$_R$ = 3 V: the output is clipped at V$_R$ + 0.7 = 3.7 V."
import numpy as _np
fig=plt.figure(figsize=(5.9,2.5))
ax=fig.add_axes([0,0,0.46,1]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.4,5.2); ax.set_ylim(-0.7,3.6)
acsrc(ax,(0,0.2),(0,2.6),"v$_i$",side=-1)
wire(ax,[(0,2.6),(0,3.0),(0.5,3.0)]); res(ax,(0.5,3.0),(2.0,3.0),"R",side=1,body=0.9); wire(ax,[(2.0,3.0),(4.3,3.0)])
diode(ax,(3.0,3.0),(3.0,1.9),"D",side=-1,body=0.5,off=0.4); batt(ax,(3.0,0.2),(3.0,1.9),"V$_R$",side=-1,off=0.55)
node(ax,(3.0,3.0)); terminal(ax,(4.3,3.0)); terminal(ax,(4.3,0.2)); label(ax,(4.75,1.6),"v$_o$",size=8.4)
wire(ax,[(0,0.2),(4.3,0.2)]); node(ax,(3.0,0.2))
bx=fig.add_axes([0.54,0.18,0.44,0.72])
t=_np.linspace(0,2*_np.pi*2,600); vi=10*_np.sin(t); vo=_np.minimum(vi,3.7)
bx.plot(t,vi,color=MUTED,lw=1,ls="--",label="v$_i$"); bx.plot(t,vo,color=ACCENT,lw=1.8,label="v$_o$")
bx.axhline(0,color=INK,lw=0.6); bx.axhline(3.7,color=SERIES[1],lw=0.8,ls=":"); bx.text(0.1,4.3,"3.7 V",fontsize=7,color=SERIES[1])
bx.set_xticks([]); bx.set_ylabel("volts",fontsize=7.5); bx.legend(fontsize=7,loc="lower right"); bx.set_ylim(-11.5,11.5)
```

*Action.* When $v_i < V_R + 0.7$ the diode is reverse biased (off), no current flows, and $v_o = v_i$. When $v_i > V_R + 0.7 = 3.7$ V the diode conducts and holds the output at $v_o = V_R + 0.7 = 3.7$ V; the extra voltage drops across $R$. Reversing the diode gives a negative clipper, and two such branches in opposite directions clip both peaks (a *double-ended* clipper).

**Clamper (dc restorer).** A clamper is a circuit built from a capacitor, a diode and a resistor (optionally a dc battery) that **shifts the whole input waveform up or down by a dc level** without changing its shape: the waveform is "clamped" so that a peak sits at a fixed level (0 V or a bias). Its time constant must be large, $RC \gg T/2$, so the capacitor holds its charge. It is used in TV receivers (dc restoration), voltage multipliers and level shifters.

**Example: positive clamper.** In the first negative half cycle the diode conducts (its anode is at ground, its cathode at the output) and charges $C$ to $V_m$ (less $V_\gamma$) with the polarity shown. Afterwards the diode stays off, the capacitor acts as a battery of $V_m$ in series with the source, and

$$v_o = v_i + V_m$$

so the output swings between $0$ and $2V_m$: the negative peak is clamped to $0$ V. If the diode is reversed, $v_o = v_i - V_m$ (negative clamper: positive peak at 0 V). A biasing battery moves the clamped level to $\pm V_R$.

```figure caption="Positive clamper (left) and waveforms for v$_i$ = ±5 V: the capacitor charges to V$_m$ and the output is the input shifted up by V$_m$, from 0 to 2V$_m$."
import numpy as _np
fig=plt.figure(figsize=(5.9,2.4))
ax=fig.add_axes([0,0,0.46,1]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.4,5.2); ax.set_ylim(-0.7,3.4)
acsrc(ax,(0,0.2),(0,2.6),"v$_i$",side=-1)
wire(ax,[(0,2.6),(0,3.0),(0.5,3.0)]); cap(ax,(0.5,3.0),(2.0,3.0),"C",side=1); wire(ax,[(2.0,3.0),(4.3,3.0)])
diode(ax,(3.0,0.2),(3.0,3.0),"D",side=-1,body=0.6,off=0.4); res(ax,(4.0,3.0),(4.0,0.2),"R",side=1,off=0.45,body=0.9)
node(ax,(3.0,3.0)); node(ax,(3.0,0.2)); node(ax,(4.0,3.0)); node(ax,(4.0,0.2)); terminal(ax,(4.9,3.0)); terminal(ax,(4.9,0.2)); wire(ax,[(4.0,3.0),(4.9,3.0)]); wire(ax,[(0,0.2),(4.9,0.2)])
bx=fig.add_axes([0.54,0.18,0.44,0.72])
t=_np.linspace(0,2*_np.pi*2,600); vi=5*_np.sin(t); vo=vi+5
bx.plot(t,vi,color=MUTED,lw=1,ls="--",label="v$_i$"); bx.plot(t,vo,color=ACCENT,lw=1.8,label="v$_o$ = v$_i$ + V$_m$")
bx.axhline(0,color=INK,lw=0.6); bx.set_xticks([]); bx.set_ylabel("volts",fontsize=7.5); bx.legend(fontsize=7,loc="upper right"); bx.set_ylim(-6.5,13.5)
```

@s 7
**Half-wave rectifier.** A single diode in series with the load converts the alternating input into a unidirectional (pulsating dc) output by allowing current only in one half cycle.

```figure caption="Half-wave rectifier: a transformer (or the ac source) feeds one diode D in series with the load R$_L$; v$_o$ appears across R$_L$."
fig,ax=ckt_canvas(4.6,2.5,xlim=(-1.5,6.4),ylim=(-0.5,3.5))
acsrc(ax,(0,0),(0,2.6),"v$_i$ = V$_m$ sin ωt",side=-1,off=1.1)
wire(ax,[(0,2.6),(0,3.0),(0.7,3.0)]); diode(ax,(0.7,3.0),(2.6,3.0),"D",side=1,body=0.8,off=0.45)
wire(ax,[(2.6,3.0),(5.0,3.0)]); res(ax,(5.0,3.0),(5.0,0),"R$_L$",side=1,off=0.5)
wire(ax,[(0,0),(5.0,0)]); arrow(ax,(1.2,2.35),(2.3,2.35),"i",off=0.22); terminal(ax,(5.0,3.0)); terminal(ax,(5.0,0)); label(ax,(3.7,1.5),"v$_o$",size=8.4)
```

*Operation.*

- **Positive half cycle** ($0 \to \pi$): the anode is positive with respect to the cathode, so the diode is forward biased and conducts. Neglecting its drop, $v_o = v_i$ and $i = \dfrac{V_m\sin\omega t}{R_L}$ (with a real diode $i = \dfrac{V_m\sin\omega t - V_\gamma}{R_L + r_f}$).
- **Negative half cycle** ($\pi \to 2\pi$): the diode is reverse biased, $i = 0$, $v_o = 0$ and the whole input voltage $V_m$ appears across the diode (peak inverse voltage $\text{PIV} = V_m$).

```figure caption="Input and output waveforms of the half-wave rectifier. The diode conducts only during the positive half cycles; its reverse voltage in the other half cycle reaches V$_m$ (the PIV)."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,4*np.pi,800)
fig,axs=plt.subplots(2,1,figsize=(5.2,3.2),sharex=True)
axs[0].plot(t,np.sin(t),color=MUTED); axs[0].axhline(0,color=INK,lw=0.6); axs[0].set_ylabel("v$_i$"); axs[0].set_yticks([-1,0,1]); axs[0].set_yticklabels(["−V$_m$","0","V$_m$"])
axs[1].plot(t,np.where(np.sin(t)>0,np.sin(t),0),color=ACCENT,lw=1.8); axs[1].axhline(0,color=INK,lw=0.6); axs[1].set_ylabel("v$_o$"); axs[1].set_yticks([0,1]); axs[1].set_yticklabels(["0","V$_m$"])
axs[1].set_xticks([0,np.pi,2*np.pi,3*np.pi,4*np.pi]); axs[1].set_xticklabels(["0","π","2π","3π","4π"]); axs[1].set_xlabel("ωt")
for a in axs: a.set_ylim(-1.25,1.25)
```

*Performance (ideal diode):*

| Quantity | Result |
|---|---|
| Average (dc) output | $V_{dc} = V_m/\pi = 0.318V_m$, $I_{dc} = I_m/\pi$ |
| RMS output | $V_{rms} = V_m/2$, $I_{rms} = I_m/2$ |
| Ripple factor | $\gamma = \sqrt{(V_{rms}/V_{dc})^2 - 1} = 1.21$ |
| Rectification efficiency | $\eta = P_{dc}/P_{ac} = \dfrac{(I_m/\pi)^2R_L}{(I_m/2)^2R_L} = \dfrac{4}{\pi^2} = 40.6\%$ |
| PIV of diode | $V_m$ |
| Transformer utilisation factor | $0.287$ |

The output has a large ripple at the *same* frequency as the input, so a filter (capacitor) is added to smooth it. A half-wave rectifier is simple and cheap but inefficient, so it is used only for low-power applications.

@s 8
Given: $V_o = V_Z = 20$ V, $R_L = 1\ \text{k}\Omega$, $V_{in} = 30$ V to $50$ V.

**Load current:** $$I_L = \frac{V_Z}{R_L} = \frac{20\ \text{V}}{1000\ \Omega} = 20\ \text{mA (constant)}$$

**Design conditions.** The series resistor current is $I_S = \dfrac{V_{in} - V_Z}{R_S} = I_Z + I_L$. To keep the Zener in breakdown at the *lowest* input, $I_Z \ge I_{Z,min}$; at the *highest* input the Zener current is largest and must not exceed $I_{ZM}$:

$$\begin{gathered} R_S = \frac{V_{in,min} - V_Z}{I_L + I_{Z,min}} \qquad (V_{in} = 30\ \text{V}) \\ I_{ZM} = \frac{V_{in,max} - V_Z}{R_S} - I_L \qquad (V_{in} = 50\ \text{V}) \end{gathered}$$

The question gives no $I_{Z,min}$, so use the usual design rule (the knee current is about 10% of the maximum rating), $I_{Z,min} = 0.1I_{ZM}$. Then

$$\begin{gathered}R_S(0.02 + 0.1I_{ZM}) = 10 \\ \text{and} \\ R_SI_{ZM} = 30 - 0.02R_S\end{gathered}$$

Substituting $R_SI_{ZM}$ into the first: $0.02R_S + 0.1(30 - 0.02R_S) = 10 \Rightarrow 0.018R_S = 7$:

$$\boxed{R_S = 388.9\ \Omega \approx 390\ \Omega\ (\text{standard value})}$$

$$\boxed{I_{ZM} = \frac{30}{388.9} - 0.02 = 0.0571\ \text{A} \approx 57\ \text{mA}}$$

*Check with $R_S = 390\ \Omega$:*

| $V_{in}$ | $I_S$ | $I_Z = I_S - I_L$ | $P_Z = V_ZI_Z$ |
|---|---|---|---|
| 30 V | $10/390 = 25.6$ mA | $5.6$ mA ($\approx 0.1I_{ZM}$, above the knee) | $0.11$ W |
| 50 V | $30/390 = 76.9$ mA | $56.9$ mA | $1.14$ W |

**Component ratings.** Zener: 20 V, power rating $\ge 20 \times 57\ \text{mA} = 1.14$ W, so choose a **20 V, 1.3 W (or 2 W)** Zener. Resistor: $P_{R_S,max}$ is $(50 - 20)^2/390 \approx 2.3$ W, so use a 5 W, 390 Ω resistor. If the load is disconnected, $I_Z = 76.9$ mA, which would exceed 57 mA, so the load must not be removed (or choose a larger Zener rating).

*Simpler assumption* ($I_{Z,min} \approx 0$): $R_S = 10/0.02 = 500\ \Omega$ and $I_{ZM} = 30/500 - 0.02 = 40$ mA. The first design keeps the Zener in a safe operating region and is preferred.

```figure caption="Zener regulator designed for Question 8: R$_S$ = 390 Ω, 20 V Zener, R$_L$ = 1 kΩ, V$_{in}$ = 30–50 V."
fig,ax=ckt_canvas(4.8,2.5,xlim=(-1.8,7.6),ylim=(-0.5,3.5))
batt(ax,(0,0.2),(0,2.2),"V$_{in}$ = 30–50 V",side=-1,off=1.0)
wire(ax,[(0,2.2),(0,3.0),(0.6,3.0)]); res(ax,(0.6,3.0),(3.0,3.0),"R$_S$ = 390 Ω",side=1,off=0.5); wire(ax,[(3.0,3.0),(6.0,3.0)])
diode(ax,(3.8,0),(3.8,3.0),"20 V Zener",side=-1,zener=True,body=0.6,off=0.95)
res(ax,(6.0,3.0),(6.0,0),"R$_L$ = 1 kΩ",side=1,off=0.5); node(ax,(3.8,3.0)); node(ax,(3.8,0))
wire(ax,[(0,0.2),(0,0),(6.0,0)])
```

@s 9
The **common-emitter (CE)** configuration has the emitter common to the input (base–emitter) and the output (collector–emitter) circuits of an n–p–n transistor. Its characteristics are plotted by varying the base and collector voltages.

```figure caption="Characteristics of the CE configuration. Left: input characteristics I$_B$ against V$_{BE}$ for two values of V$_{CE}$. Right: output characteristics I$_C$ against V$_{CE}$ for steps of I$_B$, with the cut-off, active and saturation regions marked."
import numpy as np, matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(5.9,2.7))
ax=axs[0]; v=np.linspace(0,0.85,300)
for vce,c,l,sh in ((0,SERIES[1],"V$_{CE}$ = 0",0.0),(5,ACCENT,"V$_{CE}$ ≥ 1 V",0.05)):
    ib=100*(np.exp(np.clip(v-0.62-sh,-5,None)/0.035)-np.exp(-0.62/0.035)*0.0)
    ib=np.where(v>0.45+sh,100*(np.exp((v-0.74-sh)/0.045)),0.0); ax.plot(v,np.clip(ib,0,160),color=c,label=l)
ax.set_xlabel("V$_{BE}$ (V)"); ax.set_ylabel("I$_B$ (μA)"); ax.legend(fontsize=7,loc="upper left"); ax.set_ylim(0,165); ax.set_xlim(0,0.9)
ax.text(0.04,45,"cut-in ≈ 0.7 V",fontsize=7,color=MUTED)
ax=axs[1]; vce=np.linspace(0,10,400)
for k,ib in enumerate((20,40,60,80,100)):
    ic=ib*0.1*(1-np.exp(-vce/0.35))*(1+vce/80)
    ax.plot(vce,ic,color=ACCENT,lw=1.3); ax.text(10.1,ic[-1],f"{ib} μA",fontsize=6.5,va="center")
ax.axhline(0.02,color=SERIES[1],lw=1.3); ax.text(5,0.25,"cut-off (I$_B$ = 0, I$_C$ = I$_{CEO}$)",fontsize=6.6,color=SERIES[1],ha="center",va="bottom")
ax.axvspan(0,0.5,color="#fdecea",alpha=0.9); ax.text(0.25,5.5,"sat.",fontsize=7,rotation=90,color=SERIES[1],ha="center",va="center")
ax.text(5.0,11.8,"active region",fontsize=7.2,color=MUTED,ha="center"); ax.set_xlim(0,12.6); ax.set_ylim(0,13.5)
ax.set_xlabel("V$_{CE}$ (V)"); ax.set_ylabel("I$_C$ (mA)")
fig.tight_layout()
```

**Input characteristics** ($I_B$ against $V_{BE}$ at constant $V_{CE}$). The curve is that of a forward-biased p–n junction (exponential), with a *cut-in* voltage of about 0.5 V and about 0.7 V (Si) in conduction. A larger $V_{CE}$ reduces the base width (Early effect) and shifts the curve slightly to the right, so the curves for $V_{CE} \ge 1$ V nearly coincide. *Dynamic input resistance:*

$$r_i = \left.\frac{\Delta V_{BE}}{\Delta I_B}\right|_{V_{CE}=\text{const}}\ \ (\text{about } 1\text{–}2\ \text{k}\Omega)$$

**Output characteristics** ($I_C$ against $V_{CE}$ at constant $I_B$): a family of curves, one for each value of $I_B$. The mid-portion is nearly flat, with a slight upward slope owing to the Early effect. *Dynamic output resistance* $r_o = \left.\dfrac{\Delta V_{CE}}{\Delta I_C}\right|_{I_B}$ (tens of kΩ), and the *current gain* $\beta_{ac} = \left.\dfrac{\Delta I_C}{\Delta I_B}\right|_{V_{CE}}$ and $\beta_{dc} = I_C/I_B$.

**Regions of operation:**

| Region | Junction bias | Features |
|---|---|---|
| **Active** | Emitter–base forward, collector–base reverse ($V_{CE} > V_{CE(sat)} \approx 0.2$ V) | $I_C = \beta I_B + (\beta+1)I_{CBO}$; the transistor works as a **linear amplifier** |
| **Cut-off** | Both junctions reverse ($I_B \approx 0$) | $I_C = I_{CEO} = (\beta+1)I_{CBO}$, almost zero; $V_{CE} \approx V_{CC}$; the **OFF switch** |
| **Saturation** | Both junctions forward ($V_{CE} \approx 0.2$ V, left of the knee) | $I_C$ is largest and no longer controlled by $I_B$; $I_C < \beta I_B$; the **ON switch** |
| **Breakdown** | Collector junction in avalanche at large $V_{CE}$ | $I_C$ rises sharply; the transistor can be destroyed (must be avoided) |

@s 10
Given: $V_{CC} = 20$ V, $R_B = 430\ \text{k}\Omega$, $R_C = 2\ \text{k}\Omega$, $R_E = 1\ \text{k}\Omega$, $\beta = 50$ (as printed on the figure), $V_{BE} = 0.7$ V (silicon). The 40 μF capacitor $C_E$ bypasses $R_E$ only for the ac signal, so for dc the emitter resistor stays in the circuit.

**Base–emitter loop (KVL).** $V_{CC} = I_BR_B + V_{BE} + I_ER_E$ with $I_E = (\beta+1)I_B$:

$$I_B = \frac{V_{CC} - V_{BE}}{R_B + (\beta+1)R_E} = \frac{20 - 0.7}{430\,\text{k} + 51 \times 1\,\text{k}} = \frac{19.3}{481\ \text{k}\Omega} = 40.1\ \mu\text{A}$$

$$\begin{gathered} I_C = \beta I_B = 50 \times 40.1\ \mu\text{A} = 2.006\ \text{mA} \\ I_E = (\beta + 1)I_B = 2.046\ \text{mA} \end{gathered}$$

**Collector–emitter loop:**

$$V_{CE} = V_{CC} - I_CR_C - I_ER_E = 20 - 2.006 \times 2 - 2.046 \times 1 = 13.94\ \text{V}$$

$$\boxed{Q\text{-point: } I_{CQ} = 2.01\ \text{mA},\quad V_{CEQ} = 13.94\ \text{V}\quad(I_{BQ} = 40.1\ \mu\text{A})}$$

**DC load line.** Applying KVL to the output loop, with $I_E \approx I_C$: $V_{CC} = V_{CE} + I_C(R_C + R_E)$.

- *Saturation point* ($V_{CE} = 0$): $I_{C(sat)} = \dfrac{V_{CC}}{R_C + R_E}$, so $I_{C(sat)} = 20/3\ \text{k}\Omega = 6.67$ mA.
- *Cut-off point* ($I_C = 0$): $V_{CE(cut\text{-}off)} = V_{CC} = 20$ V.

```figure caption="DC load line of Question 10 from (V$_{CE}$ = 20 V, I$_C$ = 0) to (0, 6.67 mA). The Q point (13.94 V, 2.01 mA) lies on the I$_B$ = 40 μA curve in the middle of the active region."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.2,3.0))
vce=np.linspace(0,20,300)
for ib in (20,40,60,80):
    ic=ib*0.05*(1-np.exp(-vce/0.4)); ax.plot(vce,ic,color="#9fb3d9",lw=1); ax.text(20.2,ic[-1],f"{ib} μA",fontsize=6.6,va="center",color=MUTED)
ax.plot([0,20],[6.67,0],color=ACCENT,lw=2); ax.plot([13.94],[2.01],"o",color=SERIES[1],ms=7,zorder=5)
ax.annotate("Q (13.94 V, 2.01 mA)",(13.94,2.01),xytext=(9.6,4.3),fontsize=7.6,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8))
ax.plot([13.94,13.94],[0,2.01],ls=":",color=INK,lw=0.8); ax.plot([0,13.94],[2.01,2.01],ls=":",color=INK,lw=0.8)
ax.text(0.3,6.85,"saturation  I$_{C(sat)}$ = 6.67 mA",fontsize=7.2); ax.text(19.8,0.3,"cut-off  V$_{CC}$ = 20 V",fontsize=7.2,ha="right")
ax.set_xlim(0,23.5); ax.set_ylim(0,7.8); ax.set_xlabel("V$_{CE}$ (V)"); ax.set_ylabel("I$_C$ (mA)")
```

**Region of operation.** $I_B = 40.1\ \mu\text{A} > 0$ (base junction forward biased) and $V_{CE} = 13.94\ \text{V} \gg V_{CE(sat)} \approx 0.2$ V, so the collector junction is reverse biased: $V_{CB} = 13.94 - 0.7 = 13.2$ V $> 0$. Also, $I_{B(sat)} \approx I_{C(sat)}/\beta$, which is $133\ \mu\text{A}$, larger than $40.1\ \mu\text{A}$. Therefore the transistor operates in the **active region**, which is suitable for linear amplification, and the Q point is conveniently placed near the middle of the load line (about 70% of $V_{CC}$).

@s 11
**Construction of the n-channel enhancement MOSFET (E-MOSFET).** It is built on a lightly doped **p-type silicon substrate** (body B). Two heavily doped **n⁺ regions**, the **source (S)** and **drain (D)**, are diffused into it a short distance ($L$, the channel length) apart. The surface between them is covered by a thin insulating layer of **silicon dioxide** (SiO₂, about 2–50 nm), and a **metal (or polysilicon) gate (G)** is deposited on the oxide. Metal contacts are made to the source, the drain, and the substrate (usually joined to the source). There is **no physical channel** between source and drain, and the gate is insulated from the semiconductor, so the gate current is practically zero (input resistance $\approx 10^{12}\ \Omega$).

```figure caption="Cross-section of an n-channel enhancement MOSFET. The dashed strip under the gate is the n-type inversion channel that is induced when V$_{GS}$ exceeds the threshold voltage V$_T$."
import matplotlib.patches as mp, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.4,2.9)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.3,10.3); ax.set_ylim(-1.2,5.4)
ax.add_patch(mp.Rectangle((0,0),10,2.6,fc="#fbf1d2",ec=INK,lw=1.2)); ax.text(5,0.9,"p-type substrate (B)",ha="center",fontsize=8.5)
ax.add_patch(mp.Rectangle((0.9,1.7),2.0,0.9,fc="#bcd3f5",ec=INK,lw=1.1)); ax.text(1.9,2.15,"n$^+$",ha="center",va="center",fontsize=8.5)
ax.add_patch(mp.Rectangle((7.1,1.7),2.0,0.9,fc="#bcd3f5",ec=INK,lw=1.1)); ax.text(8.1,2.15,"n$^+$",ha="center",va="center",fontsize=8.5)
ax.add_patch(mp.Rectangle((2.6,2.6),4.8,0.45,fc="#e6e6e6",ec=INK,lw=1.1)); ax.text(5,2.83,"SiO$_2$ (insulator)",ha="center",va="center",fontsize=7.4)
ax.add_patch(mp.Rectangle((3.0,3.05),4.0,0.7,fc="#c9ccd1",ec=INK,lw=1.1)); ax.text(5,3.4,"metal gate",ha="center",va="center",fontsize=8)
ax.add_patch(mp.Rectangle((1.3,2.6),1.1,1.15,fc="#c9ccd1",ec=INK,lw=1.1)); ax.add_patch(mp.Rectangle((7.6,2.6),1.1,1.15,fc="#c9ccd1",ec=INK,lw=1.1))
ax.add_patch(mp.Rectangle((0,-0.4),10,0.4,fc="#c9ccd1",ec=INK,lw=1.1))
ax.add_patch(mp.Rectangle((2.9,2.38),4.2,0.22,fc="#a9c8ff",ec=SERIES[1],lw=1,ls="--",alpha=0.9))
ax.annotate("induced n-channel",(5,2.45),xytext=(5,1.45),ha="center",fontsize=7.6,color=SERIES[1],arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1))
for x,y,t in ((1.85,4.3,"S"),(8.15,4.3,"D"),(5,4.3,"G")):
    ax.plot([x,x],[3.75 if t!="G" else 3.75,4.05],color=INK,lw=1.3); ax.text(x,4.4,t,ha="center",fontsize=10,fontweight="bold")
ax.text(5,-0.9,"substrate contact (usually tied to S)",ha="center",fontsize=7.4,color=MUTED)
ax.annotate("",xy=(7.1,2.15),xytext=(2.9,2.15),arrowprops=dict(arrowstyle="<->",color=MUTED,lw=0.8)); 
```

**Working principle.**

1. **$V_{GS} = 0$ (or $V_{GS} < V_T$).** The two n⁺–p junctions are back to back, so no current flows from drain to source even when $V_{DS} > 0$: the device is OFF, $I_D \approx 0$ (cut-off).
2. **$V_{GS} > 0$.** The positive gate attracts electrons (minority carriers of the p-substrate) toward the surface and repels holes. The gate–oxide–substrate acts as a capacitor. Initially a *depletion layer* of uncovered acceptor ions forms.
3. **$V_{GS} \ge V_T$ (threshold voltage, typically 1–2 V).** The surface is so heavily populated with electrons that it **inverts** into n-type: a thin **n-channel** connects source and drain. The channel is *enhanced* by increasing $V_{GS}$ (hence "enhancement" type); its conductivity (depth) rises with $V_{GS} - V_T$.
4. **Applying $V_{DS}$ with $V_{GS} > V_T$.** Electrons flow from the source through the channel to the drain; the conventional current $I_D$ flows drain to source.
   - *Triode (ohmic) region*, $V_{DS} < V_{GS} - V_T$: the channel acts as a voltage-controlled resistor, $I_D = k_n\left[(V_{GS} - V_T)V_{DS} - \tfrac12V_{DS}^2\right]$.
   - *Saturation (pinch-off) region*, $V_{DS} \ge V_{GS} - V_T$: the channel is pinched off at the drain end because the voltage between gate and drain falls below $V_T$ there. $I_D$ saturates, $I_D = \tfrac12k_n(V_{GS} - V_T)^2$ (square law), and the device acts as a voltage-controlled current source (an amplifier).

Here $k_n = \mu_nC_{ox}\dfrac{W}{L}$ is the transconductance parameter.

```figure caption="Drain characteristics of an n-channel E-MOSFET (V$_T$ = 2 V). The dashed parabola separates the triode region from the saturation region."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(5.0,2.7)); k=1.0; vt=2.0
for vgs in (3,4,5,6):
    vov=vgs-vt; vds=np.linspace(0,10,400)
    i=np.where(vds<vov,k*(vov*vds-vds**2/2),0.5*k*vov**2); ax.plot(vds,i,color=ACCENT,lw=1.4); ax.text(10.1,i[-1],f"V$_{{GS}}$ = {vgs} V",fontsize=6.8,va="center")
vp=np.linspace(0,4,50); ax.plot(vp,0.5*k*vp**2,color=SERIES[1],ls="--",lw=1)
ax.text(1.0,7.2,"triode",fontsize=7.4,color=MUTED); ax.text(6,9,"saturation",fontsize=7.4,color=MUTED); ax.text(1.5,0.4,"V$_{GS}$ < V$_T$: cut-off (I$_D$ = 0)",fontsize=7,color=MUTED)
ax.set_xlim(0,13.4); ax.set_ylim(0,9.6); ax.set_xlabel("V$_{DS}$ (V)"); ax.set_ylabel("I$_D$ (mA)")
```

*Transfer characteristic:* $I_D = 0$ for $V_{GS} < V_T$ and $I_D = \tfrac12k_n(V_{GS} - V_T)^2$ above it; $g_m = \dfrac{\partial I_D}{\partial V_{GS}} = k_n(V_{GS} - V_T)$. E-MOSFETs are the basic element of CMOS digital ICs, memories and microprocessors because of their small size, negligible gate current, and low power consumption.

@s 12
**Non-inverting amplifier.** The input signal $v_{in}$ is applied to the **non-inverting (+) terminal**, and a fraction of the output is fed back to the **inverting (−) terminal** through the divider $R_f$ and $R_1$ (negative feedback).

```figure caption="Closed-loop non-inverting amplifier: v$_{in}$ drives the + input; R$_f$ and R$_1$ feed a fraction R$_1$/(R$_1$ + R$_f$) of v$_o$ back to the − input."
fig,ax=ckt_canvas(4.8,2.8,xlim=(-0.4,8.0),ylim=(-1.5,3.2))
op=opamp(ax,3.0,0.0); 
wire(ax,[(5.4,0),(7.0,0)]); node(ax,(6.2,0)); terminal(ax,(7.0,0)); label(ax,(7.0,-0.4),"v$_o$",size=8.4)
wire(ax,[(6.2,0),(6.2,2.1),(5.2,2.1)]); res(ax,(5.2,2.1),(3.4,2.1),"R$_f$",side=1,body=1.0)
wire(ax,[(3.4,2.1),(2.2,2.1),(2.2,0.6),(3.0,0.6)]); node(ax,(2.2,0.6))
res(ax,(2.2,0.6),(0.8,0.6),"R$_1$",side=-1,body=0.9); gnd(ax,(0.8,0.6))
wire(ax,[(3.0,-0.6),(0.3,-0.6)]); terminal(ax,(0.3,-0.6)); label(ax,(0.3,-1.0),"v$_{in}$",size=8.4)
label(ax,(2.2,0.15),"v$_-$",size=7.8,ha="right")
```

*Derivation.* For an ideal op-amp the open-loop gain is infinite, so the differential input voltage is zero (**virtual short**, $v_- = v_+$), and the input current is zero ($i_+ = i_- = 0$).

1. The + input is connected to $v_{in}$, so $v_+ = v_{in}$ and therefore $v_- = v_{in}$.
2. No current enters the − terminal, so the same current flows through $R_f$ and $R_1$ (they form a voltage divider between $v_o$ and ground):

$$v_- = v_o\cdot\frac{R_1}{R_1 + R_f}$$

3. Equating $v_- = v_{in}$:

$$v_{in} = v_o\frac{R_1}{R_1 + R_f}$$

$$\boxed{A_{CL} = \frac{v_o}{v_{in}} = 1 + \frac{R_f}{R_1}}$$

*By KCL at the − node:* $\dfrac{0 - v_{in}}{R_1} = \dfrac{v_{in} - v_o}{R_f}$ gives $v_o = v_{in}\left(1 + \dfrac{R_f}{R_1}\right)$ as before.

*Properties.* The gain is positive (the output is **in phase** with the input), always $\ge 1$ and set only by the resistor ratio. The input resistance is very high ($R_{in} \to \infty$ in the ideal case, $R_{in}(1+A\beta)$ in a real one) and the output resistance is very low. If $R_f = 0$ (or $R_1 = \infty$), $A_{CL} = 1$: the **voltage follower** (buffer). *With a finite open-loop gain $A_{OL}$:* $A_{CL} = \dfrac{A_{OL}}{1 + A_{OL}\beta}$ with $\beta = \dfrac{R_1}{R_1 + R_f}$, which is nearly $1/\beta$ when $A_{OL}\beta \gg 1$. For example, $R_1 = 1\ \text{k}\Omega$ and $R_f = 9\ \text{k}\Omega$ give $A_{CL} = 10$.

@s 13
**Barkhausen criteria.** A feedback circuit (with amplifier gain $A$ and feedback factor $\beta$) sustains steady oscillations at frequency $f_o$ only if

1. the magnitude of the loop gain is unity, $|A\beta| = 1$, and
2. the total phase shift around the loop is $0^\circ$ or an integer multiple of $360^\circ$, $\angle A\beta = 2\pi n$ (positive feedback).

If $|A\beta| < 1$ the oscillations die out; if $|A\beta| > 1$ the amplitude grows until the amplifier saturates.

**Relaxation oscillator (op-amp astable multivibrator).** It produces a **square wave** with no input signal; the circuit does not follow the sinusoidal Barkhausen conditions but relies on the charging and discharging of a capacitor and on a regenerative comparator.

```figure caption="Op-amp relaxation oscillator (square-wave generator). R$_1$ and R$_2$ give positive feedback and set the thresholds; R and C give negative feedback with time delay."
fig,ax=ckt_canvas(5.0,3.2,xlim=(-0.4,8.2),ylim=(-3.0,3.2))
op=opamp(ax,3.0,0.0)
wire(ax,[(5.4,0),(7.0,0)]); node(ax,(6.2,0)); terminal(ax,(7.0,0)); label(ax,(7.0,-0.4),"v$_o$ = ±V$_{sat}$",size=8.2,ha="right")
wire(ax,[(6.2,0),(6.2,2.1),(5.2,2.1)]); res(ax,(5.2,2.1),(3.4,2.1),"R",side=1,body=1.0)
wire(ax,[(3.4,2.1),(2.2,2.1),(2.2,0.6),(3.0,0.6)]); node(ax,(2.2,0.6))
cap(ax,(2.2,0.6),(0.8,0.6),"C",side=1,off=0.5); gnd(ax,(0.8,0.6)); label(ax,(2.0,0.15),"v$_C$",size=7.8,ha="right")
wire(ax,[(6.2,0),(6.2,-1.5),(5.2,-1.5)]); res(ax,(5.2,-1.5),(3.4,-1.5),"R$_1$",side=-1,body=1.0)
wire(ax,[(3.4,-1.5),(2.2,-1.5),(2.2,-0.6),(3.0,-0.6)]); node(ax,(2.2,-1.5))
res(ax,(2.2,-1.5),(2.2,-2.6),"R$_2$",side=-1,body=0.7,off=0.45); gnd(ax,(2.2,-2.6))
```

*Operation.* The inverting input is the capacitor voltage $v_C$; the non-inverting input receives the fraction $\beta v_o$, where

$$\beta = \frac{R_2}{R_1 + R_2}$$

1. Suppose $v_o = +V_{sat}$. The non-inverting input is at the **upper threshold** $+\beta V_{sat}$, and $C$ charges toward $+V_{sat}$ through $R$.
2. When $v_C$ reaches $+\beta V_{sat}$ the comparator **switches** (regeneratively) to $v_o = -V_{sat}$, so the reference becomes the **lower threshold** $-\beta V_{sat}$ and $C$ now discharges, and charges toward $-V_{sat}$.
3. When $v_C$ falls to $-\beta V_{sat}$ the output flips back to $+V_{sat}$, and the cycle repeats.

```figure caption="Waveforms of the relaxation oscillator: the capacitor voltage v$_C$ (exponential segments between ±βV$_{sat}$) and the square-wave output v$_o$ = ±V$_{sat}$ (here β = 0.5)."
import numpy as np, matplotlib.pyplot as plt
vs=1.0; b=0.5; RC=1.0
T2=RC*np.log((1+b)/(1-b)); dt=0.002
t=[];vc=[];vo=[]; v=-b*vs; s=1.0; tt=0.0
while tt<5*T2:
    v+= (s*vs-v)/RC*dt; tt+=dt
    if s>0 and v>=b*vs: s=-1
    elif s<0 and v<=-b*vs: s=1
    t.append(tt); vc.append(v); vo.append(s*vs)
fig,ax=plt.subplots(figsize=(5.3,2.7))
ax.plot(t,vo,color=ACCENT,lw=1.6,label="v$_o$"); ax.plot(t,vc,color=SERIES[1],lw=1.4,label="v$_C$")
for y,tx in ((b,"+βV$_{sat}$"),(-b,"−βV$_{sat}$")): ax.axhline(y,color=MUTED,lw=0.7,ls=":"); ax.text(t[-1]+0.05,y,tx,fontsize=7,va="center",color=MUTED)
ax.axhline(0,color=INK,lw=0.6); ax.set_yticks([-1,0,1]); ax.set_yticklabels(["−V$_{sat}$","0","V$_{sat}$"]); ax.set_xlabel("time"); ax.legend(fontsize=7,loc="upper right",ncol=2); ax.set_ylim(-1.4,1.55); ax.set_xlim(0,t[-1]+1.2)
```

*Frequency.* During the discharge from $+\beta V_{sat}$ toward $-V_{sat}$, $v_C(t) = -V_{sat} + (V_{sat} + \beta V_{sat})e^{-t/RC}$, and the half period $T/2$ ends when $v_C = -\beta V_{sat}$:

$$-\beta V_{sat} = -V_{sat} + V_{sat}(1+\beta)e^{-T/2RC} \ \Rightarrow\ \frac{T}{2} = RC\ln\frac{1+\beta}{1-\beta}$$

$$T = 2RC\ln\frac{1+\beta}{1-\beta} = 2RC\ln\left(1 + \frac{2R_2}{R_1}\right)$$

$$\boxed{f_o = \frac{1}{T} = \frac{1}{2RC\ln\left(\dfrac{1+\beta}{1-\beta}\right)} = \frac{1}{2RC\ln\left(1 + \dfrac{2R_2}{R_1}\right)}}$$

For $R_1 = 1.16R_2$ (so $\beta = 0.463$) this gives $T = 2RC$, $f_o = \dfrac{1}{2RC}$. The output is a symmetric square wave of amplitude $\pm V_{sat}$ with 50% duty cycle. *Example:* $R_1 = R_2 = 10\ \text{k}\Omega$, $R = 10\ \text{k}\Omega$, $C = 0.1\ \mu$F: $\beta = 0.5$, $T = 2 \times 10^{-3}\ln3 = 2.2$ ms, $f_o = 455$ Hz.

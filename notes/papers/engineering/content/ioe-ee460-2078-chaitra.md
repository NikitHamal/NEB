---
file: NEBians-IOE-Past-Paper-Electric-Circuits-and-Machines-EE460-2078-Chaitra.pdf
subject: Electric Circuits and Machines
level: BE · Year I / Part II
code: EE 460
year_bs: 2078 Chaitra
cal: BS
year_ad: 2022
stream: BEI
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular. Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What do you mean by resonance in electric circuit? Derive the condition for series resonance. Also determine the expression of bandwidth. [[2+2+4]]

@q 2
For the circuit shown below, find currents and voltages across each elements at t = 0+. Also find the value of charge at t = 0+. [[8]]

```figure caption="Circuit of Question 2: 100 V source, 2 Ω with the switch (t = 0) across it, then a 3 Ω + 4 H branch and a 1 Ω + 2 F branch in parallel."
fig,ax=ckt_canvas(5.6,3.2,xlim=(-1.8,9.2),ylim=(-0.5,5.0))
vsrc(ax,(0,0),(0,3),"100 V",side=-1); wire(ax,[(0,3),(1.2,3)]); res(ax,(1.2,3),(3.6,3),"2 Ω",side=-1)
wire(ax,[(1.2,3),(1.2,4.2)]); switch(ax,(1.2,4.2),(3.6,4.2),"t = 0",side=1); wire(ax,[(3.6,4.2),(3.6,3)])
node(ax,(1.2,3)); node(ax,(3.6,3)); wire(ax,[(3.6,3),(8,3)]); node(ax,(5,3))
res(ax,(5,3),(5,1.6),"3 Ω",side=-1,body=0.9); ind(ax,(5,1.6),(5,0),"4 H",side=-1,body=1.0)
res(ax,(8,3),(8,1.6),"1 Ω",side=1,body=0.9); cap(ax,(8,1.6),(8,0),"2 F",side=1)
wire(ax,[(0,0),(8,0)])
```

@q 3
An exponential source V(t) = 20e$^{-3t}$ is suddenly applied at time t = 0 to a series RLC circuit comprising R = 4 ohms, L = 1 H and C = 1/3 F. Obtain the expression for the current i(t) in the circuit using Laplace Transform method. [[8]]

@q 4
For the two port network shown below, find h-parameter and T′ parameter. Also check for reciprocity of network. [[8]]

```figure caption="Two-port of Question 4: 5 Ω series arm, a voltage source 0.3 V1 in the top path, a current source 0.1 V2 across the middle node and a 4 Ω output shunt."
fig,ax=ckt_canvas(5.8,2.8,xlim=(-1.2,12.2),ylim=(-0.8,4.2))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.8,1.5),"V$_1$",size=9)
res(ax,(0,3),(2.8,3),"5 Ω",side=1); node(ax,(2.8,3))
vsrc(ax,(2.8,3),(6.4,3),"0.3 V$_1$",side=1)
wire(ax,[(6.4,3),(9,3)]); terminal(ax,(9,3)); terminal(ax,(9,0)); label(ax,(9.9,1.5),"V$_2$",size=9)
node(ax,(7.6,3)); res(ax,(7.6,3),(7.6,0),"4 Ω",side=1)
isrc(ax,(2.8,3),(2.8,0),"0.1 V$_2$",side=-1,off=0.9)
wire(ax,[(0,0),(9,0)]); node(ax,(2.8,0)); node(ax,(7.6,0))
```

@q 5
(a) Derive the equivalent Y-parameters of two number of two port network when connected in parallel. [[4]]
(b) Find the expression of inductor current for t > 0 using classical method. [[4]]

```figure caption="Circuit of Question 5(b): 20 A current source, switch (t = 0), 1/5 H inductor and 50 Ω resistor in parallel."
fig,ax=ckt_canvas(5.4,2.8,xlim=(-1.8,9.2),ylim=(-0.5,3.9))
isrc(ax,(0,0),(0,3),"20 A",side=-1); wire(ax,[(0,3),(8,3)]); wire(ax,[(0,0),(8,0)])
switch(ax,(2.6,3),(2.6,0),"t = 0",side=-1,off=0.8); node(ax,(2.6,3)); node(ax,(2.6,0))
ind(ax,(5,3),(5,0),"1/5 H",side=1); res(ax,(8,3),(8,0),"50 Ω",side=1); node(ax,(5,3)); node(ax,(5,0))
```

@q 6
An iron ring has mean length of 2 m and cross-sectional area of 0.01 m². It has a radial air gap of 4 mm. The ring is wound with 250 turns. What dc current would be needed in coil to produce a flux density of 0.5 Tesla in the core? (μ$_r$ = 4000) [[8]]

@q 7
Following results were obtained from test on a transformer of rating 8 kVA, 400/120 V, 50 Hz. [[8]]

| Test | Voltage | Current | Power |
|---|---|---|---|
| Open circuit test (LV side) | 120 V | 4 A | 75 W |
| Short circuit test (HV side) | 9.5 V | 20 A | 110 W |

Calculate equivalent circuit parameters referred to LV and HV side and draw equivalent circuit of same.

@q 8
Explain how rotating magnetic field is produced in central space of three phase induction motor. Show that magnitude of rotating magnetic field is 1.5 times maximum flux density. [[8]]

@q 9
A shunt generator delivers 50 kW at 250 V and 400 rpm. The armature resistance is 0.02 Ω and field resistance is 50 Ω. Calculate the induced emf by armature and electrical efficiency. [[8]]

@q 10
Derive the expression of torque developed in armature of Dc motor. How the direction of shunt motors can be reversed? [[4+4]]
<!-- SOLUTIONS -->

@s 1
**Resonance.** An electric circuit containing inductance and capacitance is in **resonance** when the supply voltage and the circuit current are in phase: the circuit is purely resistive and the power factor is unity (the net reactance of a series circuit, or the net susceptance of a parallel circuit, is zero).

**Condition for series resonance.** Series $R$–$L$–$C$ circuit, $Z = R + j\left(\omega L - \dfrac{1}{\omega C}\right)$. The imaginary part is zero when the inductive and capacitive reactances are equal:

$$X_L = X_C \;\Rightarrow\; \omega_0L = \frac{1}{\omega_0C}$$

$$\boxed{\,\omega_0 = \frac{1}{\sqrt{LC}},\qquad f_0 = \frac{1}{2\pi\sqrt{LC}}\,}$$

At resonance the impedance is minimum ($Z = R$), the current is maximum ($I_0 = V/R$), $V_L = V_C = QV$ with $Q = \dfrac{\omega_0L}{R} = \dfrac{1}{R}\sqrt{\dfrac{L}{C}}$.

**Bandwidth.** The band of frequencies between the half-power points $f_1, f_2$ where $I = I_0/\sqrt2$, i.e. $|Z| = \sqrt2R$ and the reactance equals $\pm R$:

$$\omega L - \frac{1}{\omega C} = \pm R \;\Rightarrow\; \omega^{2}LC \mp \omega RC - 1 = 0$$

$$\begin{gathered}\omega_{2} = \frac{R}{2L} + \sqrt{\left(\frac{R}{2L}\right)^{2} + \frac{1}{LC}} \\ \omega_{1} = -\frac{R}{2L} + \sqrt{\left(\frac{R}{2L}\right)^{2} + \frac{1}{LC}}\end{gathered}$$

$$\boxed{\,BW = \omega_2 - \omega_1 = \frac{R}{L}\ \text{rad/s} \quad\left(= \frac{R}{2\pi L}\ \text{Hz} = \frac{f_0}{Q}\right)\,}$$

with $\omega_0 = \sqrt{\omega_1\omega_2}$. A larger $Q$ means a narrower bandwidth and better selectivity.

```figure caption="Series RLC current response: the half-power points ω1 and ω2 bound the bandwidth BW = R/L."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.6,2.5)); w=_np.linspace(0.5,1.5,500); R=0.2
I=R/_np.sqrt(R**2+(w-1/w)**2); ax.plot(w,I,color=ACCENT,lw=1.8)
w1=-R/2+_np.sqrt(R**2/4+1); w2=R/2+_np.sqrt(R**2/4+1)
ax.axhline(1/_np.sqrt(2),color="#888",ls=":",lw=0.9); ax.axvline(w1,color="#888",ls=":",lw=0.9); ax.axvline(w2,color="#888",ls=":",lw=0.9)
ax.annotate("",xy=(w2,0.62),xytext=(w1,0.62),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.9)); ax.text(1.0,0.54,"BW = R/L",fontsize=8,ha="center")
ax.set_xticks([w1,1,w2]); ax.set_xticklabels(["$\\omega_1$","$\\omega_0$","$\\omega_2$"]); ax.set_yticks([1/_np.sqrt(2),1]); ax.set_yticklabels(["$I_0/\\sqrt{2}$","$I_0$"]); ax.tick_params(labelsize=8)
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
```

@s 2
The switch is drawn open across the 2 Ω resistor and marked $t = 0$: it **closes at $t = 0$**, short-circuiting the 2 Ω (the opening case is worked at the end).

*State before $t = 0$ (switch open, DC steady state).* The inductor is a short and the capacitor an open circuit, so the current flows through 2 Ω and 3 Ω only:

$$\begin{gathered}i_L(0^-) = \frac{100}{2 + 3} = 20\ \text{A} \\ i_C(0^-) = 0\end{gathered}$$

The node voltage is $3\times20 = 60$ V and, since the 1 Ω carries no current, $v_C(0^-) = 60$ V.

*At $t = 0^+$.* $i_L(0^+) = 20$ A and $v_C(0^+) = 60$ V (continuity). The closed switch applies the full 100 V to the node:

| Element | Current | Voltage |
|---|---|---|
| 2 Ω (shorted by the switch) | 0 A | 0 V |
| Switch | 60 A | 0 V |
| 3 Ω | 20 A | $3\times20 = 60$ V |
| 4 H | 20 A | $100 - 60 = 40$ V |
| 1 Ω | $\dfrac{100 - 60}{1} = 40$ A | 40 V |
| 2 F | 40 A | 60 V |
| 100 V source | $20 + 40 = 60$ A | 100 V |

$$\text{Charge at } 0^+:\quad q = Cv_C = 2\times60 = 120\ \text{C}$$

(KVL checks: 3 Ω branch $60 + 40 = 100$ V ✓, 1 Ω branch $40 + 60 = 100$ V ✓.) Also $\dfrac{di_L}{dt}\Big|_{0^+} = \dfrac{40}{4} = 10$ A/s and $\dfrac{dv_C}{dt}\Big|_{0^+} = \dfrac{40}{2} = 20$ V/s.

*If the switch were instead closed before $t = 0$ and opens at $t = 0$:* $i_L(0^-) = 100/3 = 33.33$ A, the capacitor charges to the full $v_C(0^-) = 100$ V ($q = 200$ C). At $0^+$ the inductor current stays 33.33 A, and KVL for the capacitor branch with the 2 Ω gives $i_{1Ω} = -\dfrac{2}{3}i_L = -22.22$ A, so the 2 Ω carries $33.33 - 22.22 = 11.11$ A (22.22 V), the 3 Ω 100 V, the 4 H $v_L = -22.22$ V, the 1 Ω $-22.22$ V and $q = 200$ C.

@s 3
$R = 4\ \Omega$, $L = 1$ H, $C = 1/3$ F, zero initial energy. $V(s) = \dfrac{20}{s + 3}$.

$$Z(s) = R + sL + \frac{1}{sC} = s + 4 + \frac{3}{s} = \frac{s^{2} + 4s + 3}{s} = \frac{(s + 1)(s + 3)}{s}$$

$$I(s) = \frac{V(s)}{Z(s)} = \frac{20}{s + 3}\cdot\frac{s}{(s + 1)(s + 3)} = \frac{20s}{(s + 1)(s + 3)^{2}}$$

*Partial fractions:* $I(s) = \dfrac{A}{s + 1} + \dfrac{B}{s + 3} + \dfrac{D}{(s + 3)^{2}}$.

$$\begin{gathered}A = \frac{20(-1)}{(2)^{2}} = -5 \\ D = \frac{20(-3)}{(-3 + 1)} = 30 \\ A + B = 0 \;\Rightarrow\; B = 5\end{gathered}$$

$$I(s) = -\frac{5}{s + 1} + \frac{5}{s + 3} + \frac{30}{(s + 3)^{2}}$$

$$\boxed{\,i(t) = -5e^{-t} + 5e^{-3t} + 30te^{-3t}\ \text{A}\,\quad (t \ge 0)}$$

*Check:* $i(0) = -5 + 5 = 0$ ✓ (zero initial current), and $\dfrac{di}{dt}\Big|_0 = 5 - 15 + 30 = 20$ A/s $= V(0)/L$ ✓. The roots $-1$ and $-3$ are real: over-damped; the source exponent $-3$ coincides with one natural frequency, which gives the $te^{-3t}$ term.

@s 4
**Equations of the network.** Let $I_1$ and $I_2$ both enter the network. Call A the middle node (after the 5 Ω) and B the output node. The dependent source in the top path has $+$ at the right: $V_2 = V_A + 0.3V_1$.

*Input loop:* $V_1 = 5I_1 + V_A = 5I_1 + V_2 - 0.3V_1$

$$1.3V_1 = 5I_1 + V_2 \;\Rightarrow\; V_1 = 3.846\,I_1 + 0.7692\,V_2$$

*Currents.* At node B the current in the dependent voltage source is $I_s = \dfrac{V_2}{4} - I_2$. At node A: $I_1 = 0.1V_2 + I_s = 0.1V_2 + 0.25V_2 - I_2$:

$$I_2 = -I_1 + 0.35\,V_2$$

**h-parameters** ($V_1 = h_{11}I_1 + h_{12}V_2$, $I_2 = h_{21}I_1 + h_{22}V_2$):

$$\boxed{h_{11} = 3.846\ \Omega,\quad h_{12} = 0.7692,\quad h_{21} = -1,\quad h_{22} = 0.35\ \text{S}}$$

**T′ (inverse transmission) parameters** ($V_2 = A'V_1 - B'I_1$, $I_2 = C'V_1 - D'I_1$). From the input equation, $V_2 = 1.3V_1 - 5I_1$, so $A' = 1.3$ and $B' = 5\ \Omega$. Substituting in the current equation: $I_2 = -I_1 + 0.35(1.3V_1 - 5I_1) = 0.455V_1 - 2.75I_1$:

$$\boxed{A' = 1.3,\quad B' = 5\ \Omega,\quad C' = 0.455\ \text{S},\quad D' = 2.75}$$

**Reciprocity.** A reciprocal network needs $h_{12} = -h_{21}$ (and $A'D' - B'C' = 1$). Here $h_{12} = 0.769 \neq -h_{21} = 1$, and $A'D' - B'C' = 1.3(2.75) - 5(0.455) = 3.575 - 2.275 = 1.3 \neq 1$. The network is therefore **not reciprocal**, as expected because it contains dependent (controlled) sources.

@s 5
**(a) Parallel connection of two-ports.**

Two two-port networks $N_a$ and $N_b$ are in parallel when their input ports are connected in parallel and their output ports are connected in parallel, with a common reference (each network keeps its port condition).

```figure caption="Two two-port networks N_a and N_b connected in parallel."
fig,ax=plt.subplots(figsize=(4.6,2.5)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2,12); ax.set_ylim(-1,7)
import matplotlib.patches as mp
for y0,t in ((4.0,"N$_a$  [Y$_a$]"),(0.4,"N$_b$  [Y$_b$]")):
    ax.add_patch(mp.Rectangle((3,y0),4,2,fill=False,ec=INK,lw=1.6)); ax.text(5,y0+1,t,ha="center",va="center",fontsize=9)
ax.plot([0,0],[1.4,5],color=INK,lw=1.3); ax.plot([0,3],[5,5],color=INK,lw=1.3); ax.plot([0,3],[1.4,1.4],color=INK,lw=1.3)
ax.plot([10,10],[1.4,5],color=INK,lw=1.3); ax.plot([7,10],[5,5],color=INK,lw=1.3); ax.plot([7,10],[1.4,1.4],color=INK,lw=1.3)
ax.plot([-1,0],[5.9,5.9],color=INK); ax.plot([0,0],[5,5.9],color=INK); ax.plot([-1,0],[0.5,0.5],color=INK); ax.plot([0,3],[2.4,2.4],color=INK,lw=1.3); ax.plot([0,3],[0.4+0.0,0.4],color=INK,lw=0)
ax.text(-1.6,3.2,"V$_1$",fontsize=9); ax.text(10.5,3.2,"V$_2$",fontsize=9)
```

Both networks see the same port voltages and the port currents add:

$$\begin{gathered}V_1 = V_{1a} = V_{1b} \\ V_2 = V_{2a} = V_{2b} \\ I_1 = I_{1a} + I_{1b} \\ I_2 = I_{2a} + I_{2b}\end{gathered}$$

For each network $\begin{bmatrix}I_{1k}\\ I_{2k}\end{bmatrix} = [Y_k]\begin{bmatrix}V_1\\ V_2\end{bmatrix}$, $k = a, b$. Adding the two:

$$\begin{bmatrix}I_1\\ I_2\end{bmatrix} = \left([Y_a] + [Y_b]\right)\begin{bmatrix}V_1\\ V_2\end{bmatrix}$$

$$\boxed{[Y] = [Y_a] + [Y_b]\ :\quad y_{11} = y_{11a} + y_{11b},\ y_{12} = y_{12a} + y_{12b},\ y_{21} = y_{21a} + y_{21b},\ y_{22} = y_{22a} + y_{22b}}$$

(This holds provided each network keeps its own port condition after connection, the Brune test; for an extra safety one uses an isolating ideal 1:1 transformer.)

**(b) Inductor current (classical method).**

$R = 50\ \Omega$, $L = 1/5$ H, $I_s = 20$ A, time constant $\tau = L/R = \dfrac{0.2}{50} = 4$ ms, $R/L = 250$ s$^{-1}$. The switch is in parallel with the inductor and resistor: it is drawn as the shorting branch next to the source, and the answer for both actions is given.

*Case 1: the switch opens at $t = 0$ (it short-circuits $L$ and $R$ before).* Before opening all the source current flows in the switch, so $i_L(0^-) = 0$. After opening, $I_s$ divides between $L$ and $R$:

$$I_s = i_L + \frac{L}{R}\frac{di_L}{dt} \;\Rightarrow\; i_L(t) = I_s + Ke^{-Rt/L},\quad i_L(0^+) = 0 \Rightarrow K = -20$$

$$\boxed{\,i_L(t) = 20\left(1 - e^{-250t}\right)\ \text{A}\,}$$

*Case 2: the switch closes at $t = 0$ (it was open).* Before closing, $L$ and $R$ carry the whole source current, in steady state the inductor is a short, $i_L(0^-) = 20$ A. After closing, the closed switch shorts the $L$–$R$ pair, so the stored energy decays through $R$:

$$i_L(t) = 20e^{-250t}\ \text{A}$$

In both cases the time constant is 4 ms; the inductor voltage is $v_L = L\,di_L/dt = 1000e^{-250t}$ V (switch opening) and $-1000e^{-250t}$ V (switch closing).

@s 6
*Data:* $l = 2$ m (mean length), $A = 0.01$ m², gap $l_g = 4$ mm $= 0.004$ m, $N = 250$, $\mu_r = 4000$, $B = 0.5$ T in the core (and in the gap, no fringing or leakage). The iron length is $l_i = 2 - 0.004 = 1.996$ m.

*Iron path:*

$$\begin{gathered}H_i = \frac{B}{\mu_0\mu_r} = \frac{0.5}{4\pi\times10^{-7}\times4000} = 99.47\ \text{A/m} \\ AT_i = H_il_i = 99.47\times1.996 = 198.5\ \text{AT}\end{gathered}$$

*Air gap:*

$$\begin{gathered}H_g = \frac{B}{\mu_0} = \frac{0.5}{4\pi\times10^{-7}} = 3.979\times10^{5}\ \text{A/m} \\ AT_g = H_gl_g = 3.979\times10^{5}\times0.004 = 1591.5\ \text{AT}\end{gathered}$$

*Total mmf and current:*

$$NI = AT_i + AT_g = 198.5 + 1591.5 = 1790\ \text{AT}$$

$$\boxed{I = \frac{1790}{250} = 7.16\ \text{A}}$$

(Flux $\phi = BA = 5$ mWb. Using $l_i = 2$ m gives 198.9 AT and $I = 7.16$ A, the same to three figures. The gap needs 89 percent of the mmf.)

@s 7
8 kVA, 400/120 V, 50 Hz. Rated currents: HV $= 8000/400 = 20$ A, LV $= 8000/120 = 66.7$ A. The S.C. test at 20 A is therefore at the rated HV current. Turns ratio $K = \dfrac{120}{400} = 0.3$ (LV to HV).

*O.C. test (LV side):*

$$\begin{gathered}\cos\phi_0 = \frac{75}{120\times4} = 0.15625\ (\phi_0 = 80.99^\circ) \\ I_w = 4(0.15625) = 0.625\ \text{A} \\ I_\mu = 4\sin\phi_0 = 3.951\ \text{A}\end{gathered}$$

$$\begin{gathered}R_0 = \frac{120}{0.625} = 192\ \Omega \\ X_0 = \frac{120}{3.951} = 30.37\ \Omega\quad(\text{referred to LV})\end{gathered}$$

*S.C. test (HV side):*

$$\begin{gathered}R_{eHV} = \frac{110}{20^{2}} = 0.275\ \Omega \\ Z_{eHV} = \frac{9.5}{20} = 0.475\ \Omega \\ X_{eHV} = \sqrt{0.475^{2} - 0.275^{2}} = 0.3873\ \Omega\end{gathered}$$

*Transfer between the windings* (factor $K^{2} = 0.09$ from HV to LV; divide by 0.09 for LV to HV):

| Parameter | Referred to LV | Referred to HV |
|---|---|---|
| $R_0$ | 192 Ω | $192/0.09 = 2133.3$ Ω |
| $X_0$ | 30.37 Ω | $30.37/0.09 = 337.5$ Ω |
| $R_e$ | $0.275\times0.09 = 0.02475$ Ω | 0.275 Ω |
| $X_e$ | $0.3873\times0.09 = 0.03486$ Ω | 0.3873 Ω |
| $Z_e$ | 0.04275 Ω | 0.475 Ω |

```figure caption="Approximate equivalent circuit referred to the LV side (left) and to the HV side (right)."
fig,ax=ckt_canvas(6.4,2.6,xlim=(-1.0,22.4),ylim=(-0.7,3.9))
label(ax,(5.4,3.65),"Referred to LV",size=8.5)
terminal(ax,(0,3)); terminal(ax,(0,0)); wire(ax,[(0,3),(1.4,3)]); res(ax,(1.4,3),(1.4,0),"192 Ω",side=1); wire(ax,[(1.4,3),(3.2,3)]); ind(ax,(3.2,3),(3.2,0),"j30.37 Ω",side=1)
node(ax,(1.4,3)); node(ax,(1.4,0)); node(ax,(3.2,3)); node(ax,(3.2,0))
wire(ax,[(3.2,3),(4.0,3)]); res(ax,(4.0,3),(6.2,3),"0.02475 Ω",side=1,body=0.9); ind(ax,(6.2,3),(8.4,3),"j0.0349 Ω",side=1,body=0.9); terminal(ax,(8.4,3)); terminal(ax,(8.4,0)); wire(ax,[(0,0),(8.4,0)])
label(ax,(16.6,3.65),"Referred to HV",size=8.5)
terminal(ax,(11,3)); terminal(ax,(11,0)); wire(ax,[(11,3),(12.0,3)]); res(ax,(12.0,3),(12.0,0),"2133 Ω",side=1); wire(ax,[(12.0,3),(14.0,3)]); ind(ax,(14.0,3),(14.0,0),"j337.5 Ω",side=1)
node(ax,(12.0,3)); node(ax,(12.0,0)); node(ax,(14.0,3)); node(ax,(14.0,0))
wire(ax,[(14.0,3),(14.8,3)]); res(ax,(14.8,3),(17.0,3),"0.275 Ω",side=1,body=0.9); ind(ax,(17.0,3),(19.2,3),"j0.387 Ω",side=1,body=0.9); terminal(ax,(19.2,3)); terminal(ax,(19.2,0)); wire(ax,[(11,0),(19.2,0)])
```

The exciting branch $R_0 \parallel X_0$ is placed at the supply side (approximate circuit); the series branch is $R_e + jX_e$.

@s 8
**Production of the rotating magnetic field.** The three stator windings are placed $120^\circ$ apart in space and are fed from a balanced three-phase supply whose currents are $120^\circ$ apart in time. Each winding produces a pulsating flux density along its own axis:

$$\begin{gathered}B_a = B_m\sin\omega t \\ B_b = B_m\sin(\omega t - 120^\circ) \\ B_c = B_m\sin(\omega t - 240^\circ)\end{gathered}$$

The axes lie at $0^\circ$, $120^\circ$ and $240^\circ$. Resolve into x and y components:

$$B_x = B_a + B_b\cos120^\circ + B_c\cos240^\circ = B_m\left[\sin\omega t - \tfrac12\sin(\omega t - 120^\circ) - \tfrac12\sin(\omega t - 240^\circ)\right] = 1.5B_m\sin\omega t$$

$$B_y = \frac{\sqrt3}{2}B_m\left[\sin(\omega t - 120^\circ) - \sin(\omega t - 240^\circ)\right] = -1.5B_m\cos\omega t$$

$$B_r = \sqrt{B_x^{2} + B_y^{2}} = \sqrt{(1.5B_m)^{2}(\sin^{2}\omega t + \cos^{2}\omega t)} = 1.5B_m$$

$$\begin{gathered}\boxed{B_r = 1.5\,B_m} \\ \text{and} \\ \tan\theta = \frac{B_y}{B_x} = -\cot\omega t\;\Rightarrow\;\theta = \omega t - 90^\circ\end{gathered}$$

The resultant flux density has **constant magnitude, 1.5 times the maximum flux density of one phase**, and its direction rotates with the angle $\omega t$, i.e. at the synchronous speed $N_s = \dfrac{120f}{P}$ rpm. The direction of rotation follows the phase sequence; interchanging any two supply lines reverses it. The figure shows the resultant at four instants.

```figure caption="Phase fluxes and the resultant at ωt = 0°, 60°, 120°, 180°: constant length 1.5 Bm, rotating."
import numpy as _np
from matplotlib.patches import Circle
fig=plt.figure(figsize=(6.2,2.5))
a=fig.add_axes([0.05,0.2,0.42,0.7]); th=_np.linspace(0,2*_np.pi,400)
for k,(c,l) in enumerate(zip(("#d9534f",ACCENT,"#2a9d4a"),("a","b","c"))): a.plot(_np.degrees(th),_np.sin(th-k*2*_np.pi/3),color=c,lw=1.5,label=l)
for d in (0,60,120,180): a.axvline(d,color="#aaa",ls=":",lw=0.8)
a.axhline(0,color=INK,lw=0.6); a.set_xticks([0,60,120,180,240,300,360]); a.tick_params(labelsize=6.5); a.set_yticks([]); a.set_xlabel("$\\omega t$ (degrees)",fontsize=8); a.legend(fontsize=7,ncol=3,loc="upper right",frameon=False)
for sp_ in ("top","right"): a.spines[sp_].set_visible(False)
for i,d in enumerate((0,60,120,180)):
    b=fig.add_axes([0.5+i*0.125,0.25,0.12,0.6]); b.set_aspect("equal"); b.axis("off"); b.set_xlim(-1.8,1.8); b.set_ylim(-1.8,1.8)
    w=_np.radians(d); fx=_np.sin(w); fy=-_np.cos(w)
    b.add_patch(Circle((0,0),1.5,fill=False,ec="#bbb",lw=0.7))
    b.annotate("",xy=(1.5*fx,1.5*fy),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); b.set_title("%d°"%d,fontsize=7.5)
```

@s 9
$I_L = \dfrac{50\,000}{250} = 200$ A, $I_{sh} = \dfrac{250}{50} = 5$ A.

$$I_a = I_L + I_{sh} = 205\ \text{A}$$

*Induced emf:*

$$E_g = V + I_aR_a = 250 + 205(0.02) = \boxed{254.1\ \text{V}}$$

*Electrical efficiency* $\eta_e$ = useful electrical output / electrical power developed in the armature:

$$P_{dev} = E_gI_a = 254.1\times205 = 52\,090.5\ \text{W}$$

$$\eta_e = \frac{50\,000}{52\,090.5}\times100 = \boxed{95.99\ \%}$$

*Check of losses:* armature copper $I_a^{2}R_a = 205^{2}(0.02) = 840.5$ W, field copper $VI_{sh} = 250\times5 = 1250$ W; $50\,000 + 840.5 + 1250 = 52\,090.5$ W ✓.

@s 10
**Torque of a DC motor armature.** Let $\phi$ be the flux per pole (Wb), $P$ the number of poles, $Z$ the number of armature conductors, $A$ the number of parallel paths, $I_a$ the armature current, $N$ the speed in rps.

*Force on one conductor:* $F = BlI_c$ with $I_c = \dfrac{I_a}{A}$. The torque of one conductor is $F\,r$ with $r$ the armature radius. The mean flux density under the poles is $B = \dfrac{P\phi}{2\pi rl}$ (flux per pole $\phi$ over the pole area $2\pi rl/P$).

$$T_{cond} = BlI_c\,r = \frac{P\phi}{2\pi rl}\,l\,\frac{I_a}{A}\,r = \frac{P\phi I_a}{2\pi A}$$

Total torque on all $Z$ conductors:

$$\boxed{\,T_a = \frac{ZP\phi}{2\pi A}\,I_a = 0.159\frac{ZP}{A}\phi I_a\ \text{N·m}\,}$$

so $T_a = k\phi I_a$ with $k = \dfrac{ZP}{2\pi A}$: the torque is proportional to flux and armature current (for a shunt motor with constant flux, $T \propto I_a$; for a series motor $T \propto I_a^{2}$ below saturation). It can also be derived from power: $E_bI_a = T_a\omega$, with $E_b = \dfrac{ZP\phi N}{A}$ and $\omega = 2\pi N$, giving the same result.

**Reversing the direction of a shunt motor.** The direction of the force, hence of rotation, is given by Fleming's left-hand rule and depends on the directions of the flux and of the armature current. Reversing **either** one reverses the torque:

1. Interchange the **armature terminals** (reverse the armature current) while keeping the field connections unchanged. This is the usual method: the field has a high inductance and a large emf appears on breaking its circuit, and reversing the field would pass through zero flux (a runaway danger).
2. Or interchange the **field terminals** (reverse the field current), keeping the armature connections unchanged.

Reversing both together (that is reversing the supply polarity) leaves the direction unchanged. In practice a reversing (double-pole double-throw) switch or contactors in the armature circuit are used.

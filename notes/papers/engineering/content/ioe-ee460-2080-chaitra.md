---
file: NEBians-IOE-Past-Paper-Electric-Circuits-and-Machines-EE460-2080-Chaitra.pdf
subject: Electric Circuits and Machines
level: BE · Year I / Part II
code: EE 460
year_bs: 2080 Chaitra
cal: BS
year_ad: 2024
stream: BEI
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular. Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) Define resonance condition of the network containing resistor, inductor and capacitor. Derive expression for the resonance frequency, bandwidth of series RLC circuit. [[8]]
(b) From the figure below, find the value of current and voltage across each element and di/dt at t = 0+. [[8]]

```figure caption="Circuit of Question 1(b): V0 = 10 V, R1 = 3 Ω with the switch (t = 0) across it, R = 2 Ω and L = 4 H, loop current i."
fig,ax=ckt_canvas(5.4,3.1,xlim=(-1.8,7.8),ylim=(-0.5,5.0))
vsrc(ax,(0,0),(0,3),"V$_0$ = 10 V",side=-1)
wire(ax,[(0,3),(1.2,3)]); res(ax,(1.2,3),(3.6,3),"R$_1$ = 3 Ω",side=-1)
wire(ax,[(1.2,3),(1.2,4.2)]); switch(ax,(1.2,4.2),(3.6,4.2),"t = 0",side=1); wire(ax,[(3.6,4.2),(3.6,3)])
node(ax,(1.2,3)); node(ax,(3.6,3))
res(ax,(3.6,3),(6,3),"R = 2 Ω",side=-1); ind(ax,(6,3),(6,0),"L = 4 H",side=1)
wire(ax,[(0,0),(6,0)]); mesh(ax,(3,1.5),0.6,"i")
```

@q 2
(a) Derive an expression of voltage in series RL circuit when excited by step voltage. Also define time constant of circuit and discuss its dependency on the circuit parameters. [[4+2+2]]
(b) In circuit shown in figure below, switch is changed from position 'a' to 'b' at t = 0. Find expression for loop currents i$_1$ and i$_2$ for t > 0, using classical approach, where v(t) = 30 sin(50t + 30°) volts, and the instantaneous polarity is as indicated in figure. Evaluate also value of 'v′' at 3 milliseconds. [[8]]

```figure caption="Circuit of Question 2(b): 50 V source (position a) and v(t) source (position b), 5 Ω, 2 H, shared 10 Ω, second 10 Ω and 2 H with voltage v′."
fig,ax=ckt_canvas(6.0,3.0,xlim=(-1.6,12.6),ylim=(-0.5,4.9))
vsrc(ax,(0,0),(0,3),"50 V",side=-1); vsrc(ax,(1.8,0),(1.8,3),"v(t)",side=1)
wire(ax,[(0,3),(0,4.1),(2.6,4.1)]); wire(ax,[(1.8,3),(2.6,3)])
node(ax,(2.6,4.1)); node(ax,(2.6,3)); label(ax,(2.35,4.45),"a"); label(ax,(2.35,2.65),"b")
ax.plot([3.6,2.7],[3,3],color=INK,lw=1.6); ax.plot([3.6,2.75],[3,4.0],color=INK,lw=1.0,ls=":"); label(ax,(3.15,3.55),"K",size=8)
res(ax,(3.6,3),(5.6,3),"5 Ω",side=1,body=0.9); ind(ax,(5.6,3),(7.6,3),"2 H",side=1,body=0.9)
node(ax,(7.6,3)); res(ax,(7.6,3),(7.6,0),"10 Ω",side=-1)
res(ax,(7.6,3),(10.2,3),"10 Ω",side=1,body=0.9); ind(ax,(10.2,3),(10.2,0),"2 H",side=1)
label(ax,(11.0,2.3),"+",size=10); label(ax,(11.0,0.7),"−",size=10); label(ax,(11.55,1.5),"v′",size=9)
wire(ax,[(0,0),(10.2,0)]); node(ax,(7.6,0))
mesh(ax,(4.6,1.5),0.6,"i$_1$"); mesh(ax,(9.0,1.5),0.6,"i$_2$")
```

@q 3
(a) What do you mean by two-port network and two-port parameters? Explain about Z, Y, T, T′, h and g parameters with related equations and signify the application of each parameter in context of electrical circuits. [[8]]
(b) In the circuit below find the i$_1$(t) and i$_2$(t) and the output voltage across 5 Ω when the switch is closed at t > 0 using Laplace method. [[6+2]]

```figure caption="Circuit of Question 3(b): 100 V source, switch S (t = 0), R = 10 Ω, L = 0.02 H and R = 5 Ω; mesh currents i1(t) and i2(t)."
fig,ax=ckt_canvas(5.4,3.0,xlim=(-1.6,8.6),ylim=(-0.5,4.0))
vsrc(ax,(0,0),(0,3),"100 V",side=-1)
switch(ax,(0,3),(2.0,3),"S (t = 0)",side=1)
res(ax,(2.0,3),(4.4,3),"10 Ω",side=1); node(ax,(4.4,3))
ind(ax,(4.4,3),(4.4,0),"L = 0.02 H",side=-1)
wire(ax,[(4.4,3),(7,3)]); res(ax,(7,3),(7,0),"5 Ω",side=1); wire(ax,[(0,0),(7,0)]); node(ax,(4.4,0))
mesh(ax,(2.2,1.5),0.6,"i$_1$"); mesh(ax,(5.7,1.5),0.6,"i$_2$")
```

@q 4
(a) Explain no load operation of a transformer and draw its electrical equivalent circuit. What do you mean by amp turn balance in loaded transformer? Write down the characteristics of ideal transformer. [[4+2+2]]
(b) An iron ring has a mean length of 1.5 m and cross-sectional area of 0.01 m². It has a radial air gap of 4 mm. The ring is wounded with 250 turns. What dc current would be needed in the coil to produce flux of 0.8 weber in the air gap? Assume that μ$_r$ = 400 and leakage factor is 25 %. [[8]]

@q 5
(a) Describe the T-S characteristics of 3-phase induction motor and find the condition for the maximum torque. Also, verify that maximum torque equation is independent of rotor resistance. [[4+2+2]]
(b) A 10 kVA, 200/400 V, 50 Hz single-phase transformer gives the following test results with the instruments connected on each side of the transformer. [[6+2]]

| Test | Voltage | Current | Power |
|---|---|---|---|
| Open Circuit Test (LV) | V$_{OC}$ = 200 V | I$_{OC}$ = 0.7 A | W$_{OC}$ = 70 W |
| Short Circuit Test (HV) | V$_{SC}$ = 15 V | I$_{SC}$ = 10 A | W$_{SC}$ = 85 W |

Draw the exact equivalent circuit of transformer with all necessary parameters refer to primary and secondary side.
<!-- SOLUTIONS -->

@s 1
**(a) Resonance in an RLC network; series RLC frequency and bandwidth.**

*Definition.* A network containing $R$, $L$ and $C$ is said to be in **resonance** when the applied voltage and the resulting current are in phase, i.e. the circuit behaves as a pure resistance (unity power factor): the net reactance (series circuit) or net susceptance (parallel circuit) is zero. In the series circuit this happens when the inductive reactance equals the capacitive reactance, $X_L = X_C$.

*Series RLC circuit.* Impedance $Z = R + j\left(\omega L - \dfrac{1}{\omega C}\right)$.

$$\begin{gathered}\text{Resonance: } \omega_0 L = \frac{1}{\omega_0 C} \;\Rightarrow\; \omega_0 = \frac{1}{\sqrt{LC}} \\ f_0 = \frac{1}{2\pi\sqrt{LC}}\end{gathered}$$

*At resonance:* $Z = R$ (minimum), $I_0 = V/R$ (maximum), $\cos\phi = 1$, $V_L = V_C = QV$ (voltage magnification) and $Q = \dfrac{\omega_0L}{R} = \dfrac{1}{\omega_0CR} = \dfrac{1}{R}\sqrt{\dfrac{L}{C}}$.

*Bandwidth.* The half-power (cut-off) frequencies $\omega_1$, $\omega_2$ are those at which $I = I_0/\sqrt2$, i.e. $|Z| = \sqrt2R$, so $\left|\omega L - \dfrac{1}{\omega C}\right| = R$.

$$\omega L - \frac{1}{\omega C} = \pm R \;\Rightarrow\; \omega^{2} \mp \frac{R}{L}\omega - \frac{1}{LC} = 0$$

$$\begin{gathered}\omega_{2} = \frac{R}{2L} + \sqrt{\left(\frac{R}{2L}\right)^{2} + \frac{1}{LC}} \\ \omega_{1} = -\frac{R}{2L} + \sqrt{\left(\frac{R}{2L}\right)^{2} + \frac{1}{LC}}\end{gathered}$$

$$\begin{gathered}BW = \omega_2 - \omega_1 = \frac{R}{L}\ \text{rad/s} \\ BW = \frac{R}{2\pi L}\ \text{Hz} = \frac{f_0}{Q}\end{gathered}$$

Also $\omega_0 = \sqrt{\omega_1\omega_2}$ (geometric mean). A higher $Q$ (smaller $R$) gives a narrower bandwidth and a sharper, more selective response.

```figure caption="Series RLC current response for three values of R: the smaller the R, the higher the Q and the narrower the bandwidth."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.8,2.6)); w=_np.linspace(0.4,1.6,500)
for R,c in ((0.1,"#d9534f"),(0.25,ACCENT),(0.6,"#2a9d4a")):
    I=1/_np.sqrt(R**2+(w-1/w)**2); ax.plot(w,I/ (1/R),color=c,lw=1.6,label="R = %.2f  (Q = %.0f)"%(R,1/R))
ax.axhline(1/_np.sqrt(2),color="#888",ls=":",lw=0.9); ax.text(0.42,0.73,"$I_0/\\sqrt{2}$",fontsize=8)
ax.set_xlabel("$\\omega/\\omega_0$",fontsize=8); ax.set_ylabel("$I/I_0$",fontsize=8); ax.tick_params(labelsize=7); ax.legend(fontsize=7,frameon=False)
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
```

**(b) Initial values at t = 0+.**

The figure shows the switch drawn open across $R_1$ and marked $t = 0$: it is a normally-open switch that **closes at $t = 0$** and short-circuits $R_1 = 3\ \Omega$ (an alternative reading, a switch that opens, is solved at the end).

*Before the switch acts ($t = 0^-$, DC steady state).* The inductor is a short, so $R_1$ and $R$ are in series with the source:

$$i(0^-) = \frac{V_0}{R_1 + R} = \frac{10}{3+2} = 2\ \text{A}$$

*At $t = 0^+$.* The inductor current cannot change: $i(0^+) = i(0^-) = 2$ A.

| Element | Voltage at $t = 0^+$ |
|---|---|
| $R_1$ (shorted by the closed switch) | $v_{R1} = 0$ V (switch current $= 2$ A) |
| $R = 2\ \Omega$ | $v_R = 2\times2 = 4$ V |
| $L = 4$ H | $v_L = V_0 - v_R = 10 - 4 = 6$ V |

KVL: $10 = 0 + 4 + 6$ ✓.

$$\frac{di}{dt}\Big|_{0^+} = \frac{v_L(0^+)}{L} = \frac{6}{4} = 1.5\ \text{A/s}$$

Final value: $i(\infty) = 10/2 = 5$ A with time constant $\tau = L/R = 2$ s, so $i(t) = 5 - 3e^{-t/2}$ A, whose slope at $0$ is $1.5$ A/s ✓.

*If the switch were instead initially closed and opens at $t = 0$:* $i(0^-) = 10/2 = 5$ A $= i(0^+)$; $v_{R1} = 3\times5 = 15$ V, $v_R = 10$ V, $v_L = 10 - 15 - 10 = -15$ V and $di/dt = -15/4 = -3.75$ A/s.

@s 2
**(a) Series RL circuit with step voltage.**

A DC step $V$ is applied at $t = 0$ to a series $R$–$L$ circuit with $i(0^-) = 0$. KVL for $t > 0$:

$$V = Ri + L\frac{di}{dt}$$

*Solution.* Complete response = forced + natural. Forced: $i_f = V/R$. Natural: $i_n = Ke^{-Rt/L}$. Using $i(0^+) = 0$: $K = -V/R$.

$$i(t) = \frac{V}{R}\left(1 - e^{-Rt/L}\right)$$

*Voltages:*

$$\begin{gathered}v_R(t) = Ri = V\left(1 - e^{-Rt/L}\right) \\ v_L(t) = L\frac{di}{dt} = Ve^{-Rt/L}\end{gathered}$$

At $t = 0^+$ the whole voltage appears across the inductor (it acts as an open circuit), at $t \to \infty$ it appears across $R$ (the inductor acts as a short).

*Time constant.* $\tau = \dfrac{L}{R}$ seconds is the time in which the current grows to $63.2$ percent of its final value $V/R$ (equivalently the time the current would take to reach its final value if it kept its initial rate of rise). The transient is practically over in $5\tau$ (99.3 percent).

*Dependency.* $\tau$ is directly proportional to the inductance $L$ and inversely proportional to the resistance $R$ (for several resistors, $R$ is the Thévenin resistance seen by the inductor). A large $L$ stores more energy and opposes change more, so the current rises slowly; a large $R$ makes the current settle quickly (smaller final value). $\tau$ is independent of the source voltage $V$ and of the initial current.

```figure caption="Series RL step response: i(t) rising to V/R and v_L(t) decaying; τ = L/R marks 63.2 percent."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.8,2.5)); x=_np.linspace(0,5,300)
ax.plot(x,1-_np.exp(-x),color=ACCENT,lw=1.8,label="i / (V/R)"); ax.plot(x,_np.exp(-x),color="#d9534f",lw=1.8,label="v$_L$ / V")
ax.plot([1,1],[0,0.632],ls=":",color="#888"); ax.plot([0,1],[0.632,0.632],ls=":",color="#888"); ax.text(1.05,0.2,"$\\tau$ = L/R",fontsize=8); ax.text(1.1,0.66,"63.2 %",fontsize=8)
ax.set_xlabel("t / $\\tau$",fontsize=8); ax.tick_params(labelsize=7); ax.legend(fontsize=7,frameon=False,loc="center right")
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
```

**(b) Loop currents (classical method).**

*Initial conditions (switch in 'a', 50 V, DC steady state for $t < 0$).* Both inductors are short circuits. Mesh 2: $10(i_2 - i_1) + 10i_2 = 0$ gives $i_2 = i_1/2$. Mesh 1: $50 = 5i_1 + 10(i_1 - i_2) = 5i_1 + 5i_1$:

$$\begin{gathered}i_1(0^+) = 5\ \text{A} \\ i_2(0^+) = 2.5\ \text{A}\end{gathered}$$

*Equations for $t > 0$ (switch in 'b', source $v(t)$):*

$$\begin{gathered}v(t) = 5i_1 + 2\frac{di_1}{dt} + 10(i_1 - i_2) \\ 0 = 10i_2 + 2\frac{di_2}{dt} + 10(i_2 - i_1)\end{gathered}$$

$$\begin{gathered}2i_1' + 15i_1 - 10i_2 = v(t) \\ 2i_2' - 10i_1 + 20i_2 = 0\end{gathered}$$

*Natural response.* The homogeneous system $\begin{bmatrix}i_1'\\ i_2'\end{bmatrix} = \begin{bmatrix}-7.5 & 5\\ 5 & -10\end{bmatrix}\begin{bmatrix}i_1\\ i_2\end{bmatrix}$ has the characteristic equation $(s+7.5)(s+10) - 25 = s^{2} + 17.5s + 50 = 0$:

$$s_{1,2} = \frac{-17.5 \pm \sqrt{17.5^{2} - 200}}{2} = -3.596,\ -13.904\ \text{s}^{-1}$$

with eigenvectors $(0.788,\ 0.615)$ and $(-0.615,\ 0.788)$.

*Forced (particular) response* by phasors, $\omega = 50$ rad/s, $V = 30\angle30^\circ$: the matrix $\begin{bmatrix}15 + j100 & -10\\ -10 & 20 + j100\end{bmatrix}\begin{bmatrix}I_1\\ I_2\end{bmatrix} = \begin{bmatrix}30\angle30^\circ\\ 0\end{bmatrix}$ gives

$$\begin{gathered}I_1 = 0.2940\angle-51.66^\circ\ \text{A} \\ I_2 = 0.02883\angle-130.35^\circ\ \text{A}\end{gathered}$$

*Complete response.* The constants follow from $i_1(0) = 5$, $i_2(0) = 2.5$ (the forced part at $t = 0$ is $-0.2306$ and $-0.0220$ A):

$$\boxed{\,i_1(t) = 4.473e^{-3.596t} + 0.758e^{-13.904t} + 0.2940\sin(50t - 51.66^\circ)\ \text{A}\,}$$

$$\boxed{\,i_2(t) = 3.492e^{-3.596t} - 0.970e^{-13.904t} + 0.02883\sin(50t - 130.35^\circ)\ \text{A}\,}$$

*Checks:* $i_1(0) = 4.473 + 0.758 - 0.2306 = 5.000$ A and $i_2(0) = 3.492 - 0.970 - 0.022 = 2.500$ A.

*Voltage at 3 ms.* The voltage $v'$ is across the right-hand 2 H inductor (polarity + on top), $v' = 2\,\dfrac{di_2}{dt}$:

$$\frac{di_2}{dt} = -12.558e^{-3.596t} + 13.491e^{-13.904t} + 1.4415\cos(50t - 130.35^\circ)$$

At $t = 3$ ms the three terms are $-12.424$, $+12.940$ and $-0.761$, so $di_2/dt = -0.242$ A/s (unrounded $-0.2418$), hence

$$\boxed{v'(3\ \text{ms}) = 2(-0.2418) \approx -0.484\ \text{V}}$$

(For reference the source voltage at that instant is $v(3\ \text{ms}) = 30\sin(0.15\ \text{rad} + 30^\circ) = 30\sin38.59^\circ = 18.7$ V.)

@s 3
**(a) Two-port networks and their parameters.**

A **two-port network** is a network with two pairs of terminals: an input port (1–1′) and an output port (2–2′). Each port has one voltage and one current, so of the four variables $V_1, I_1, V_2, I_2$ any two can be expressed in terms of the other two. The coefficients of these linear equations are the **two-port parameters**. The network is assumed linear and free of independent sources; $I_1$ and $I_2$ both flow *into* the network (except in the ABCD convention).

| Parameter | Equations | Found by | Used for |
|---|---|---|---|
| **Z** (open-circuit impedance) | $V_1 = z_{11}I_1 + z_{12}I_2$, $V_2 = z_{21}I_1 + z_{22}I_2$ | $z_{11} = V_1/I_1$, $z_{21} = V_2/I_1$ with $I_2 = 0$; $z_{12} = V_1/I_2$, $z_{22} = V_2/I_2$ with $I_1 = 0$ | series-series connection of networks, filter and impedance-matching design, analysis of T networks |
| **Y** (short-circuit admittance) | $I_1 = y_{11}V_1 + y_{12}V_2$, $I_2 = y_{21}V_1 + y_{22}V_2$ | $y_{11} = I_1/V_1$, $y_{21} = I_2/V_1$ with $V_2 = 0$; $y_{12} = I_1/V_2$, $y_{22} = I_2/V_2$ with $V_1 = 0$ | parallel-parallel connection, π networks, nodal analysis, FET and transmission-line models |
| **T** (ABCD, transmission) | $V_1 = AV_2 - BI_2$, $I_1 = CV_2 - DI_2$ | $A = V_1/V_2$, $B = -V_1/I_2$ ($V_2 = 0$ / $I_2 = 0$ as appropriate), $C = I_1/V_2$, $D = -I_1/I_2$ | **cascade** connection (matrix product), transmission lines, power-system lines and transformers |
| **T′** (inverse transmission) | $V_2 = A'V_1 - B'I_1$, $I_2 = C'V_1 - D'I_1$ | same idea with input and output interchanged | cascade analysed from the load toward the source, reverse transmission |
| **h** (hybrid) | $V_1 = h_{11}I_1 + h_{12}V_2$, $I_2 = h_{21}I_1 + h_{22}V_2$ | $h_{11} = V_1/I_1$ ($V_2 = 0$), $h_{21} = I_2/I_1$ ($V_2 = 0$), $h_{12} = V_1/V_2$ ($I_1 = 0$), $h_{22} = I_2/V_2$ ($I_1 = 0$) | **transistor** (BJT) small-signal models, series-parallel connection, feedback amplifiers |
| **g** (inverse hybrid) | $I_1 = g_{11}V_1 + g_{12}I_2$, $V_2 = g_{21}V_1 + g_{22}I_2$ | $g_{11} = I_1/V_1$ ($I_2 = 0$), $g_{21} = V_2/V_1$ ($I_2 = 0$), $g_{12} = I_1/I_2$ ($V_1 = 0$), $g_{22} = V_2/I_2$ ($V_1 = 0$) | parallel-series connection, voltage-controlled models, voltage amplifiers and regulators |

*Relations.* $[z] = [y]^{-1}$; $[g] = [h]^{-1}$. Conversion examples: $A = \dfrac{z_{11}}{z_{21}}$, $B = \dfrac{\Delta z}{z_{21}}$, $C = \dfrac{1}{z_{21}}$, $D = \dfrac{z_{22}}{z_{21}}$; $z_{11} = \dfrac{A}{C}$.

*Special properties.* Reciprocal network: $z_{12} = z_{21}$, $y_{12} = y_{21}$, $AD - BC = 1$, $h_{12} = -h_{21}$. Symmetrical network: additionally $z_{11} = z_{22}$, $A = D$. Which set is chosen depends on how networks are interconnected: series, parallel and cascade connections add $[z]$, add $[y]$ and multiply $[T]$ respectively.

**(b) Laplace transform solution.**

The inductor is initially de-energised ($i_L(0^-) = 0$). Transform the circuit: source $100/s$, resistor 10 Ω, inductor $sL = 0.02s$, resistor 5 Ω. Mesh currents $I_1(s)$ (source mesh) and $I_2(s)$ (right mesh through the 5 Ω):

$$\begin{gathered}\frac{100}{s} = 10I_1 + 0.02s(I_1 - I_2) \\ 0 = 5I_2 + 0.02s(I_2 - I_1)\end{gathered}$$

From the second equation $I_2 = \dfrac{0.02s}{5 + 0.02s}I_1 = \dfrac{s}{s + 250}I_1$. Substituting into the first:

$$\frac{100}{s} = I_1\left[10 + \frac{0.02s\cdot5}{5 + 0.02s}\right] = I_1\,\frac{50 + 0.2s + 0.1s}{5 + 0.02s} = I_1\,\frac{50 + 0.3s}{5 + 0.02s}$$

$$I_1(s) = \frac{100(5 + 0.02s)}{s(50 + 0.3s)}$$

Carrying out the partial fractions exactly:

$$\begin{gathered}I_1(s) = \frac{10}{s} - \frac{3.333}{s + 166.67} \\ I_2(s) = \frac{6.667}{s + 166.67} \\ V_o(s) = 5I_2(s) = \frac{33.33}{s + 166.67}\end{gathered}$$

The time constant of the circuit is $\tau = \dfrac{L}{R_{eq}} = \dfrac{0.02}{10\parallel5} = \dfrac{0.02}{3.333} = 6\ \text{ms}$, i.e. the pole at $s = -166.67$ s$^{-1}$.

*Inverse transform:*

$$\boxed{i_1(t) = 10 - 3.333e^{-166.67t}\ \text{A}}$$

$$\boxed{i_2(t) = 6.667e^{-166.67t}\ \text{A}}$$

$$\boxed{v_o(t) = 5i_2(t) = 33.33e^{-166.67t}\ \text{V}}$$

*Checks.* At $t = 0^+$ the inductor is an open circuit, so $i_1 = i_2 = 100/15 = 6.667$ A and $v_o = 33.3$ V ✓. At $t \to \infty$ the inductor is a short, so $i_1 = 100/10 = 10$ A, $i_2 = 0$, $v_o = 0$ ✓. The inductor current is $i_1 - i_2 = 10\left(1 - e^{-166.67t}\right)$ A.

@s 4
**(a) No-load operation of a transformer.**

With the secondary open and the rated voltage $V_1$ applied to the primary, the primary draws a small **no-load current** $I_0$ (2–5 % of the rated current). It has two components: the **magnetising component** $I_\mu$ (in phase with the flux, 90° behind $V_1$), which sets up the main flux $\phi_m$ in the core, and the **core-loss (working) component** $I_w$ (in phase with $V_1$), which supplies the hysteresis and eddy-current losses.

$$\begin{gathered}I_0 = \sqrt{I_\mu^{2} + I_w^{2}} \\ \cos\phi_0 = \frac{I_w}{I_0}\ (\text{about } 0.1\text{–}0.3\text{ lagging}) \\ W_0 = V_1I_0\cos\phi_0 = \text{iron loss}\end{gathered}$$

The alternating flux induces $E_1 = 4.44fN_1\phi_m$ in the primary (almost equal and opposite to $V_1$ since $I_0R_1$ and $I_0X_1$ are small) and $E_2 = 4.44fN_2\phi_m$ in the secondary, with $V_2 = E_2$ at no load. Hence $\dfrac{E_2}{E_1} = \dfrac{N_2}{N_1} = K$. The flux lags $V_1$ by about 90°.

```figure caption="No-load equivalent circuit: primary winding R1, X1 in series with the exciting branch R0 ∥ X0 (core loss and magnetising reactance); the secondary is open."
fig,ax=ckt_canvas(5.8,2.4,xlim=(-1.0,12.0),ylim=(-0.7,3.7))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.7,1.5),"V$_1$",size=9)
res(ax,(0,3),(2.4,3),"R$_1$",side=1,body=0.9); ind(ax,(2.4,3),(4.8,3),"X$_1$",side=1,body=0.9)
wire(ax,[(4.8,3),(7,3)]); res(ax,(7,3),(7,0),"R$_0$",side=1); wire(ax,[(7,3),(9.5,3)]); ind(ax,(9.5,3),(9.5,0),"X$_0$",side=1)
wire(ax,[(0,0),(9.5,0)]); node(ax,(7,3)); node(ax,(7,0))
arrow(ax,(0.5,3.5),(1.5,3.5),"I$_0$",off=0.2); arrow(ax,(7.8,2.0),(7.8,1.0),"I$_w$",off=0.35); arrow(ax,(10.3,2.0),(10.3,1.0),"I$_\\mu$",off=0.35)
```

**Ampere-turn balance in a loaded transformer.** When a load current $I_2$ flows, the secondary mmf $N_2I_2$ tends to demagnetise the core (Lenz's law). The primary draws an extra **load component** $I_2'$ so that its mmf cancels this effect and the net core flux stays practically constant (since $V_1 \approx E_1$ is fixed):

$$\begin{gathered}N_1I_1 - N_2I_2 = N_1I_0 \;\Rightarrow\; N_1I_2' = N_2I_2 \\ I_2' = \frac{N_2}{N_1}I_2 = KI_2\end{gathered}$$

$$\bar I_1 = \bar I_0 + \bar I_2'$$

For an ideal transformer $I_0 = 0$, so $N_1I_1 = N_2I_2$ exactly. This is the *ampere-turn balance*.

**Characteristics of an ideal transformer.**

- The windings have zero resistance (no copper loss) and the core has infinite permeability (no magnetising current), so no core loss ($I_0 = 0$).
- No leakage flux: all the flux links both windings (coupling coefficient $k = 1$).
- Efficiency $= 100$ %, voltage regulation $= 0$.
- $\dfrac{V_1}{V_2} = \dfrac{E_1}{E_2} = \dfrac{N_1}{N_2} = \dfrac{I_2}{I_1} = a$.
- Input power equals output power: $V_1I_1 = V_2I_2$, and the load impedance is reflected as $Z' = a^{2}Z_L$.

**(b) D.C. current for the ring with an air gap.**

*Data:* $l_i = 1.5$ m, $A = 0.01$ m², $l_g = 4$ mm $= 0.004$ m, $N = 250$, $\mu_r = 400$, $\phi_g = 0.8$ Wb (flux in the gap, the useful flux), leakage factor $\lambda = 1.25$ (total flux $= 1.25\times$ useful flux).

*Flux in the iron:* $\phi_i = \lambda\phi_g = 1.25\times0.8 = 1.0$ Wb (the leakage flux, 25 percent, bypasses the gap).

*Reluctances* ($\mu_0 = 4\pi\times10^{-7}$ H/m):

$$S_g = \frac{l_g}{\mu_0A} = \frac{0.004}{4\pi\times10^{-7}\times0.01} = 3.183\times10^{5}\ \text{AT/Wb}$$

$$S_i = \frac{l_i}{\mu_0\mu_rA} = \frac{1.5}{4\pi\times10^{-7}\times400\times0.01} = 2.984\times10^{5}\ \text{AT/Wb}$$

*Ampere-turns* (iron path carries the total flux, the gap carries the useful flux):

$$NI = \phi_gS_g + \phi_iS_i = 0.8(3.183\times10^{5}) + 1.0(2.984\times10^{5}) = 2.546\times10^{5} + 2.984\times10^{5} = 5.53\times10^{5}\ \text{AT}$$

$$\boxed{I = \frac{5.53\times10^{5}}{250} = 2212\ \text{A}}$$

*Note.* A gap flux of 0.8 Wb through 0.01 m² means $B_g = 80$ T, which no real core can reach; the numbers are those printed on the paper and the linear $\mu_r = 400$ model is used as asked. (If the gap length were subtracted from the iron length, $l_i = 1.496$ m, the answer changes by under 0.1 percent.)

@s 5
**(a) Torque–slip (T–S) characteristics of a 3-phase induction motor.**

*Torque equation.* With rotor resistance $R_2$ and standstill reactance $X_2$ per phase, standstill rotor emf $E_2$, slip $s$, synchronous angular speed $\omega_s$:

$$T = \frac{3}{\omega_s}\cdot\frac{sE_2^{2}R_2}{R_2^{2} + (sX_2)^{2}}$$

*Shape of the T–S curve.*

```figure caption="Torque–slip characteristics for three rotor resistances: the maximum torque is the same, only its slip changes."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.9,2.7)); s=_np.linspace(0.001,1,400); X2=0.4
for R2,c in ((0.1,"#d9534f"),(0.2,ACCENT),(0.4,"#2a9d4a")):
    T=s*R2/(R2**2+(s*X2)**2); ax.plot(s,T,color=c,lw=1.7,label="R$_2$ = %.1f"%R2)
    ax.plot([R2/X2],[1/(2*X2)],"o",color=c,ms=4)
ax.text(0.02,1.46,"T$_{max}$ for all R$_2$",fontsize=8); ax.axhline(1/(2*X2),color="#aaa",ls=":",lw=0.8)
ax.set_xlim(1,0); ax.set_xlabel("slip s  (1 = standstill, 0 = synchronous speed)",fontsize=8); ax.set_ylabel("torque T",fontsize=8); ax.set_yticks([]); ax.tick_params(labelsize=7); ax.legend(fontsize=7,frameon=False,loc="upper left")
for sp_ in ("top","right"): ax.spines[sp_].set_visible(False)
```

- At synchronous speed ($s = 0$) the torque is zero (no emf, no rotor current).
- For small slip (normal running, $s \le 0.05$) $sX_2 \ll R_2$, so $T \approx \dfrac{3sE_2^{2}}{\omega_sR_2} \propto s$: the curve is almost a straight line (stable region, speed falls slightly with load).
- The torque rises to a maximum (breakdown or pull-out torque) at $s_m$.
- For larger slip $sX_2 \gg R_2$, $T \approx \dfrac{3E_2^{2}R_2}{\omega_ssX_2^{2}} \propto \dfrac1s$: the torque falls as the slip increases (unstable region).
- At standstill ($s = 1$) the starting torque is $T_{st} = \dfrac{3E_2^{2}R_2}{\omega_s(R_2^{2} + X_2^{2})}$. Raising $R_2$ (slip-ring motors with external resistance) increases the starting torque, and it is greatest when $R_2 = X_2$ ($s_m = 1$).

*Condition for maximum torque.* Set $\dfrac{dT}{ds} = 0$. With $f(s) = \dfrac{sR_2}{R_2^{2} + s^{2}X_2^{2}}$:

$$\frac{(R_2^{2} + s^{2}X_2^{2})R_2 - sR_2(2sX_2^{2})}{(\cdots)^{2}} = 0 \;\Rightarrow\; R_2^{2} - s^{2}X_2^{2} = 0$$

$$\boxed{\,s_m = \frac{R_2}{X_2}\,}$$

Maximum torque occurs when the rotor resistance equals the slip-dependent rotor reactance, $R_2 = s_mX_2$.

*Verification that $T_{max}$ is independent of $R_2$.* Substituting $R_2 = s_mX_2$:

$$T_{max} = \frac{3}{\omega_s}\cdot\frac{s_mE_2^{2}R_2}{R_2^{2} + R_2^{2}} = \frac{3}{\omega_s}\cdot\frac{s_mE_2^{2}R_2}{2R_2^{2}} = \frac{3E_2^{2}}{2\omega_s}\cdot\frac{s_m}{R_2} = \frac{3E_2^{2}}{2\omega_s}\cdot\frac{1}{X_2}$$

$$\boxed{T_{max} = \frac{3E_2^{2}}{2\omega_sX_2}}$$

$R_2$ has cancelled: the maximum torque does not depend on the rotor resistance. Changing $R_2$ only changes the slip $s_m = R_2/X_2$ at which $T_{max}$ occurs (see the figure), which is why rotor-resistance control shifts the speed at which maximum torque is developed without changing its value.

**(b) Equivalent circuit from the test data.** 10 kVA, 200/400 V, 50 Hz. The O.C. test is on the LV side (200 V, i.e. the 200 V winding is called the primary here) and the S.C. test is on the HV side (400 V winding). Turns ratio $K = \dfrac{400}{200} = 2$.

*Open-circuit test (LV side, 200 V):*

$$\cos\phi_0 = \frac{W_{OC}}{V_{OC}I_{OC}} = \frac{70}{200\times0.7} = 0.5\ \ (\phi_0 = 60^\circ)$$

$$\begin{gathered}I_w = I_{OC}\cos\phi_0 = 0.35\ \text{A} \\ I_\mu = I_{OC}\sin\phi_0 = 0.606\ \text{A}\end{gathered}$$

$$\begin{gathered}R_0 = \frac{200}{0.35} = 571.4\ \Omega \\ X_0 = \frac{200}{0.606} = 329.9\ \Omega\quad(\text{referred to LV})\end{gathered}$$

*Short-circuit test (HV side, 10 A):*

$$\begin{gathered}R_{e2} = \frac{W_{SC}}{I_{SC}^{2}} = \frac{85}{100} = 0.85\ \Omega \\ Z_{e2} = \frac{15}{10} = 1.5\ \Omega \\ X_{e2} = \sqrt{1.5^{2} - 0.85^{2}} = 1.236\ \Omega\quad(\text{referred to HV})\end{gathered}$$

*Transfer between sides* (impedance scales by $K^{2} = 4$):

| Parameter | Referred to primary (LV, 200 V) | Referred to secondary (HV, 400 V) |
|---|---|---|
| $R_0$ | 571.4 Ω | $571.4\times4 = 2285.7$ Ω |
| $X_0$ | 329.9 Ω | $329.9\times4 = 1319.7$ Ω |
| $R_e$ | $0.85/4 = 0.2125$ Ω | 0.85 Ω |
| $X_e$ | $1.236/4 = 0.309$ Ω | 1.236 Ω |
| $Z_e$ | 0.375 Ω | 1.5 Ω |

*Exact (T-form) equivalent circuit.* The tests give only the total series values, so the usual assumption is made that the resistance and leakage reactance are shared equally between the two windings: $R_1 = R_2' = R_{e1}/2 = 0.106\ \Omega$ and $X_1 = X_2' = X_{e1}/2 = 0.155\ \Omega$ (referred to the primary); referred to the secondary: $R_1' = R_2 = 0.425\ \Omega$, $X_1' = X_2 = 0.618\ \Omega$. The exciting branch $R_0 \parallel X_0$ sits between the two series impedances. (The approximate circuit moves the exciting branch to the supply terminals and uses $R_e$, $X_e$ in one block.)

```figure caption="Exact equivalent circuit referred to the primary (LV, 200 V side): R1, X1 | R0 ∥ X0 | R2′, X2′."
fig,ax=ckt_canvas(6.2,2.6,xlim=(-1.0,14.4),ylim=(-0.7,3.8))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.7,1.5),"V$_1$",size=9)
res(ax,(0,3),(2.4,3),"0.106 Ω",side=1,body=0.9); ind(ax,(2.4,3),(4.8,3),"j0.155 Ω",side=1,body=0.9)
wire(ax,[(4.8,3),(5.6,3)]); res(ax,(5.6,3),(5.6,0),"571.4 Ω",side=-1); wire(ax,[(5.6,3),(8.0,3)]); ind(ax,(8.0,3),(8.0,0),"j329.9 Ω",side=1)
node(ax,(5.6,3)); node(ax,(5.6,0)); node(ax,(8.0,3)); node(ax,(8.0,0))
wire(ax,[(8.0,3),(8.6,3)]); res(ax,(8.6,3),(10.8,3),"0.106 Ω",side=1,body=0.9); ind(ax,(10.8,3),(13.0,3),"j0.155 Ω",side=1,body=0.9)
terminal(ax,(13.0,3)); terminal(ax,(13.0,0)); wire(ax,[(0,0),(13.0,0)]); label(ax,(13.8,1.5),"V$_2'$",size=9)
```

```figure caption="Exact equivalent circuit referred to the secondary (HV, 400 V side): R1′, X1′ | R0′ ∥ X0′ | R2, X2."
fig,ax=ckt_canvas(6.2,2.6,xlim=(-1.0,14.4),ylim=(-0.7,3.8))
terminal(ax,(0,3)); terminal(ax,(0,0)); label(ax,(-0.7,1.5),"V$_1'$",size=9)
res(ax,(0,3),(2.4,3),"0.425 Ω",side=1,body=0.9); ind(ax,(2.4,3),(4.8,3),"j0.618 Ω",side=1,body=0.9)
wire(ax,[(4.8,3),(5.6,3)]); res(ax,(5.6,3),(5.6,0),"2285.7 Ω",side=-1); wire(ax,[(5.6,3),(8.0,3)]); ind(ax,(8.0,3),(8.0,0),"j1319.7 Ω",side=1)
node(ax,(5.6,3)); node(ax,(5.6,0)); node(ax,(8.0,3)); node(ax,(8.0,0))
wire(ax,[(8.0,3),(8.6,3)]); res(ax,(8.6,3),(10.8,3),"0.425 Ω",side=1,body=0.9); ind(ax,(10.8,3),(13.0,3),"j0.618 Ω",side=1,body=0.9)
terminal(ax,(13.0,3)); terminal(ax,(13.0,0)); wire(ax,[(0,0),(13.0,0)]); label(ax,(13.8,1.5),"V$_2$",size=9)
```

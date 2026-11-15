---
file: NEBians-IOE-Past-Paper-Control-System-ENEE251-2082-Bhadra.pdf
subject: Control System
level: BE · Year II / Part II
code: ENEE 251
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) What is an open and a closed loop control system? Discuss along with their advantages and disadvantages. [[6]]

(b) Obtain the mathematical equations for the mechanical system shown in the figure. Also obtain the force-current analogy. (Figure: three masses in a vertical chain. $M_3$ hangs from the ceiling by damper $B_3$ and spring $K_3$ and has displacement $x_3$; below it $M_2$ (displacement $x_2$) is joined to $M_3$ by damper $B_2$ and spring $K_2$; $M_1$ (displacement $x_1$) is joined to $M_2$ by spring $K_1$ and carries the force $F(t)$.) [[6]]

@q 2
(a) Find the overall transfer function of the system shown below by the block diagram reduction technique. (Figure: three summing points with $R(s)$, $G_1$, then a parallel pair $G_2$ and $G_3$ into a last summing point giving $C(s)$; feedback $H_2$ and $H_1$ as drawn; unity feedback from $C(s)$ to the first summing point.) [[6]]

(b) Determine the block diagram and transfer function of an armature-controlled DC motor. [[6]]

@q 3
(a) Determine the value of $K$ and $H$ of the closed loop system so that the maximum overshoot in the unit step response is $25\%$ and the peak time is $2$ s. Assume $J = 1$ kg-m$^2$. (Figure: $R(s)$ → summing point → summing point → $\dfrac{K}{Js}$ → node → $\dfrac{1}{s}$ → $C(s)$; feedback $H$ from the node between $K/Js$ and $1/s$ to the second summing point; unity feedback from $C(s)$ to the first summing point.) [[6]]

(b) The open loop transfer function of a unity feedback system is given by $G(s) = \dfrac{K}{s(1 + 0.4s)(1 + 0.25s)}$. Using the Routh-Hurwitz criterion, (i) determine the range of $K$ so that the system is stable; (ii) calculate the frequency at which the system will exhibit sustained oscillation. [[6]]

@q 4
(a) Using the Nyquist criterion, determine the stability of the feedback system whose open loop transfer function is given by $G(s)H(s) = \dfrac{s + 5}{(s - 2)(s + 2)}$. Also find the gain margin. [[5]]

(b) Sketch the polar plot for the following open loop transfer function and, using the Nyquist criterion, determine whether the system is stable or not: $G(s)H(s) = \dfrac{60}{(s + 1)(s + 2)(s + 5)}$. [[6]]

@q 5
(a) Design a lead compensator for a system whose open loop transfer function is given by $G(s) = \dfrac{K}{s(1 + 0.1s)(1 + 0.001s)}$ to meet the following specifications: phase margin (P.M.) $\ge 45^\circ$ and velocity error constant $K_v = 1000\ \text{s}^{-1}$. [[9]]

(b) A system has the transfer function $\dfrac{Y(s)}{U(s)} = \dfrac{2}{s^3 + 6s^2 + 11s + 6}$. Find the state and output equations in matrix form. [[4]]

<!-- SOLUTIONS -->

@s 1
**(a) Open loop control system.** The control action is **independent of the output**: there is no measurement of the output and no feedback path. The output is determined only by the input and the calibration of the system.

**Closed loop (feedback) control system.** The output is measured, fed back and compared with the reference; the **error** $e = r - b$ drives the controller, so the control action depends on the output.

```figure caption="Open loop (top) and closed loop (bottom) control systems."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,(a,b)=plt.subplots(2,1,figsize=(6.6,3.7))
for z in (a,b): z.set_aspect("equal"); z.axis("off")
a.set_xlim(-0.3,11.3); a.set_ylim(-0.8,0.9); arr(a,[(0,0),(1.4,0)]); txt(a,0.1,0.4,"input r",ha="left",fs=7.5); box(a,2.4,0,"Controller",w=2.0,fc="#eaf3ff"); arr(a,[(3.4,0),(4.6,0)]); box(a,5.6,0,"Plant",w=2.0,fc="#fff4d6")
a.text(10.2,0.4,"output c",ha="right",fontsize=7.5); arr(a,[(6.6,0),(10.4,0)]); a.set_title("Open loop: no feedback",fontsize=8.5)
b.set_xlim(-0.3,11.3); b.set_ylim(-1.7,0.9); arr(b,[(0,0),(1.06,0)]); txt(b,0.1,0.4,"input r",ha="left",fs=7.5); sj(b,1.3,0,left="+",bottom="-"); arr(b,[(1.54,0),(2.35,0)]); box(b,3.3,0,"Controller",w=1.9,fc="#eaf3ff"); arr(b,[(4.25,0),(5.4,0)]); box(b,6.4,0,"Plant",w=2.0,fc="#fff4d6"); arr(b,[(7.4,0),(10.4,0)]); txt(b,10.4,0.4,"output c",ha="right",fs=7.5)
dot(b,8.8,0); line(b,[(8.8,0),(8.8,-1.2)]); arr(b,[(8.8,-1.2),(7.4,-1.2)]); box(b,6.4,-1.2,"Sensor",w=2.0,fc="#fff4d6"); line(b,[(5.4,-1.2),(1.3,-1.2)]); arr(b,[(1.3,-1.2),(1.3,-0.26)]); b.set_title("Closed loop: output fed back and compared",fontsize=8.5)
```

| Basis | Open loop | Closed loop |
|---|---|---|
| Feedback | none | present (output compared with input) |
| Accuracy | depends on calibration; poor | high, because the error is corrected |
| Effect of disturbances and parameter changes | large; cannot be corrected | greatly reduced (sensitivity $= 1/(1 + GH)$) |
| Stability | stable if the plant is stable (no stability problem from the controller) | can become unstable (oscillation) if the gain is too high |
| Bandwidth and speed | small bandwidth, sluggish | larger bandwidth, faster response |
| Complexity and cost | simple and cheap | complex, needs sensor and comparator, costlier |
| Overall gain | $G$ | $\dfrac{G}{1 + GH}$ (lower, but can be restored) |
| Examples | washing machine, traffic light on a timer, electric toaster, bread-maker | room thermostat/air conditioner, cruise control, servo motor, speed governor |

*Advantages of open loop:* simple, cheap, easy to maintain, no stability problem, convenient when the output is hard to measure or is not needed. *Disadvantages:* inaccurate, unable to compensate for disturbances or changes in the plant. *Advantages of closed loop:* accurate, rejects disturbances, reduces effect of parameter variation, improves transient response and bandwidth, can linearise a non-linear plant. *Disadvantages:* complex and expensive, reduced gain, possible instability, needs a sensor with its own noise.

**(b) Equations.** Let $x_1, x_2, x_3$ be the displacements of the masses, positive downward, from their equilibrium positions. Use the free-body diagram of each mass (force of a spring $= K\,\Delta x$, of a damper $= B\,\Delta\dot x$):

$$\begin{aligned} \text{Mass } M_3:&\ M_3\ddot x_3 + B_3\dot x_3 + K_3x_3 + B_2(\dot x_3 - \dot x_2) + K_2(x_3 - x_2) = 0 \\ \text{Mass } M_2:&\ M_2\ddot x_2 + B_2(\dot x_2 - \dot x_3) + K_2(x_2 - x_3) + K_1(x_2 - x_1) = 0 \\ \text{Mass } M_1:&\ M_1\ddot x_1 + K_1(x_1 - x_2) = F(t) \end{aligned}$$

In the Laplace domain:

$$\begin{aligned} \left[M_3s^2 + (B_2 + B_3)s + (K_2 + K_3)\right]X_3 - (B_2s + K_2)X_2 &= 0 \\ -(B_2s + K_2)X_3 + \left[M_2s^2 + B_2s + (K_1 + K_2)\right]X_2 - K_1X_1 &= 0 \\ -K_1X_2 + (M_1s^2 + K_1)X_1 &= F(s) \end{aligned}$$

**Force-current analogy** (force $\to$ current source, velocity $\to$ node voltage $v = \dot x$, mass $M \to$ capacitor $C = M$ to the reference node, damper $B \to$ resistor $R = 1/B$, spring $K \to$ inductor $L = 1/K$; elements fixed to the ceiling go to the reference (ground) node, elements joining two masses go between their nodes). The node equations are

$$\begin{aligned} M_3\frac{dv_3}{dt} + B_3v_3 + K_3\!\int v_3\,dt + B_2(v_3 - v_2) + K_2\!\int(v_3 - v_2)\,dt &= 0 \\ M_2\frac{dv_2}{dt} + B_2(v_2 - v_3) + K_2\!\int(v_2 - v_3)\,dt + K_1\!\int(v_2 - v_1)\,dt &= 0 \\ M_1\frac{dv_1}{dt} + K_1\!\int(v_1 - v_2)\,dt &= F(t) \end{aligned}$$

```figure caption="Force-current analogous circuit: node 3 has C = M3, R = 1/B3 and L = 1/K3 to the reference node; R = 1/B2 and L = 1/K2 in parallel join node 3 to node 2 (C = M2); L = 1/K1 joins node 2 to node 1 (C = M1, current source F)."
fig,ax=ckt_canvas(7.2,3.2,(-0.8,12.2),(-0.9,4.6))
cap(ax,(0.5,3),(0.5,0),"C = M3",side=-1); res(ax,(1.8,3),(1.8,0),"R = 1/B3",side=1); ind(ax,(3.1,3),(3.1,0),"L = 1/K3",side=1)
wire(ax,[(0.5,3),(3.7,3)]); wire(ax,[(3.7,2.2),(3.7,3.8)]); res(ax,(3.7,3.8),(6.0,3.8),"R = 1/B2",side=1); ind(ax,(3.7,2.2),(6.0,2.2),"L = 1/K2",side=-1); wire(ax,[(6.0,2.2),(6.0,3.8)])
wire(ax,[(6.0,3),(7.0,3)]); cap(ax,(7.0,3),(7.0,0),"C = M2",side=-1); ind(ax,(7.0,3),(9.4,3),"L = 1/K1",side=1); wire(ax,[(9.4,3),(11.4,3)])
cap(ax,(10.2,3),(10.2,0),"C = M1",side=-1); isrc(ax,(11.4,0),(11.4,3),"F",side=1); wire(ax,[(0.5,0),(11.4,0)]); gnd(ax,(5.4,0))
node(ax,(3.7,3)); node(ax,(6.0,3)); node(ax,(9.4,3)); label(ax,(2.4,3.3),"v3"); label(ax,(6.6,3.3),"v2"); label(ax,(10.8,3.3),"v1")
```

@s 2
**(a)** Redrawing the diagram (reading as: the first summing point forms $R - C$; the second subtracts the $H_1$ feedback; the third subtracts the $H_2$ feedback; the signal $X$ after the third summing point goes to the parallel pair $G_2$ and $G_3$ whose outputs add at the last summing point to give $C$; $H_1$ is fed from the output of $G_2$ and $H_2$ from $C$):

```figure caption="Block diagram of Question 2(a) as redrawn: unity feedback from C to the first summing point; H1 from the output of G2 to the second summing point; H2 from C to the third summing point; G2 and G3 in parallel."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,ax=canvas(7.2,3.2,(-0.3,14.4),(-3.8,2.0))
arr(ax,[(0,0),(1.16,0)]); txt(ax,0.2,0.3,"R(s)"); sj(ax,1.4,0,left="+",bottom="-"); arr(ax,[(1.64,0),(3.16,0)]); sj(ax,3.4,0,left="+",bottom="-"); arr(ax,[(3.64,0),(4.55,0)]); box(ax,5.2,0,"G1")
arr(ax,[(5.85,0),(6.76,0)]); sj(ax,7.0,0,left="+",bottom="-"); dot(ax,8.0,0); arr(ax,[(7.24,0),(9.35,0)]); box(ax,10.0,0,"G2"); arr(ax,[(10.65,0),(11.96,0)]); sj(ax,12.2,0,top="+",left="+")
arr(ax,[(12.44,0),(14.2,0)]); txt(ax,14.2,0.3,"C(s)",ha="right")
arr(ax,[(8.0,0),(8.0,1.3),(9.35,1.3)]); box(ax,10.0,1.3,"G3"); arr(ax,[(10.65,1.3),(12.2,1.3),(12.2,0.24)]); txt(ax,8.9,0.28,"X",fs=7.5)
dot(ax,11.2,0); line(ax,[(11.2,0),(11.2,-2.4)]); arr(ax,[(11.2,-2.4),(7.15,-2.4)]); box(ax,6.5,-2.4,"H1")
line(ax,[(5.85,-2.4),(3.4,-2.4)]); arr(ax,[(3.4,-2.4),(3.4,-0.24)])
dot(ax,13.3,0); line(ax,[(13.3,0),(13.3,-1.2)]); arr(ax,[(13.3,-1.2),(10.15,-1.2)]); box(ax,9.5,-1.2,"H2"); line(ax,[(8.85,-1.2),(7.0,-1.2)]); arr(ax,[(7.0,-1.2),(7.0,-0.24)])
line(ax,[(13.3,-1.2),(13.3,-3.4)]); line(ax,[(13.3,-3.4),(1.4,-3.4)]); arr(ax,[(1.4,-3.4),(1.4,-0.24)])
```

Writing the signals ($E$ = output of the first summing point, $W$ = output of the second, $X$ = output of the third, $Y = G_2X$):

$$\begin{gathered}E = R - C \\ W = E - H_1G_2X \\ X = G_1W - H_2C \\ C = (G_2 + G_3)X\end{gathered}$$

Eliminate $W$: $X = G_1(R - C) - G_1G_2H_1X - H_2C$, hence

$$X\left(1 + G_1G_2H_1\right) = G_1R - (G_1 + H_2)\,C$$

Substitute $X = \dfrac{C}{G_2 + G_3}$:

$$C\left(1 + G_1G_2H_1\right) = (G_2 + G_3)\left[G_1R - (G_1 + H_2)C\right]$$

$$C\left[1 + G_1G_2H_1 + (G_2 + G_3)(G_1 + H_2)\right] = G_1(G_2 + G_3)\,R$$

$$\boxed{\frac{C(s)}{R(s)} = \frac{G_1(G_2 + G_3)}{1 + G_1G_2H_1 + (G_2 + G_3)(G_1 + H_2)}}$$

Expanded denominator: $1 + G_1G_2 + G_1G_3 + G_1G_2H_1 + G_2H_2 + G_3H_2$. (Checked with sympy by solving the signal equations.) In block-reduction steps: (i) combine $G_2$ and $G_3$ in parallel as $G_2 + G_3$; (ii) move the $H_1$ pick-off from the output of $G_2$ to the output of $G_2 + G_3$ by multiplying $H_1$ by $\dfrac{G_2}{G_2 + G_3}$; (iii) reduce the inner loops; (iv) close the outer unity feedback.

**(b) Armature-controlled DC motor.** The field current is constant (constant flux $\phi$), the armature voltage $v_a$ is the input and the shaft angle $\theta$ the output.

Armature circuit: $v_a = R_ai_a + L_a\dfrac{di_a}{dt} + e_b$. Back emf: $e_b = K_b\dfrac{d\theta}{dt} = K_b\omega$. Torque: $T = K_ti_a$. Mechanical load: $T = J\dfrac{d\omega}{dt} + B\omega$. (J and B are the moment of inertia and viscous friction of the motor plus load.)

Laplace transforms:

$$V_a(s) - E_b(s) = (R_a + L_as)I_a(s), \quad E_b(s) = K_bs\theta(s), \quad T(s) = K_tI_a(s), \quad T(s) = (Js + B)\,s\,\theta(s)$$

```figure caption="Block diagram of an armature-controlled DC motor: the armature circuit 1/(Ra + La s), the torque constant Kt, the mechanical load 1/(Js + B), the integrator 1/s from speed to angle, and the back-emf feedback Kb."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,ax=canvas(7.2,2.5,(-0.3,15.6),(-2.3,1.6))
arr(ax,[(0,0),(0.76,0)]); txt(ax,0.0,0.35,"Va(s)",ha="left"); sj(ax,1.0,0,left="+",bottom="-"); arr(ax,[(1.24,0),(2.0,0)]); box(ax,3.1,0,"1 / (Ra + La s)",w=2.2,fc="#eaf3ff"); arr(ax,[(4.2,0),(5.3,0)]); txt(ax,4.75,0.3,"Ia",fs=7.5)
box(ax,6.1,0,"Kt",w=1.4,fc="#fff4d6"); arr(ax,[(6.8,0),(7.9,0)]); txt(ax,7.35,0.3,"T",fs=7.5); box(ax,9.0,0,"1 / (J s + B)",w=2.2,fc="#eaf3ff"); arr(ax,[(10.1,0),(11.8,0)]); txt(ax,11.0,0.3,"\u03c9(s)",fs=7.5)
dot(ax,11.2,0); box(ax,12.7,0,"1 / s",w=1.4,fc="#eaf3ff"); arr(ax,[(13.4,0),(15.4,0)]); txt(ax,15.4,0.35,"\u03b8(s)",ha="right")
line(ax,[(11.2,0),(11.2,-1.5)]); arr(ax,[(11.2,-1.5),(7.55,-1.5)]); box(ax,6.9,-1.5,"Kb",w=1.3,fc="#fff4d6"); line(ax,[(6.25,-1.5),(1.0,-1.5)]); arr(ax,[(1.0,-1.5),(1.0,-0.26)]); txt(ax,3.5,-1.2,"back emf Eb",fs=7.5,color=MUT)
```

Eliminating $I_a$ and $E_b$:

$$\frac{\theta(s)}{V_a(s)} = \frac{K_t}{s\left[(R_a + L_as)(Js + B) + K_tK_b\right]}$$

$$\boxed{\frac{\theta(s)}{V_a(s)} = \frac{K_t}{s\left[L_aJs^2 + (R_aJ + L_aB)s + (R_aB + K_tK_b)\right]}}$$

and the speed transfer function is $\dfrac{\omega(s)}{V_a(s)} = s\dfrac{\theta(s)}{V_a(s)}$. For small $L_a$ (usually neglected) this becomes

$$\begin{gathered}\frac{\theta(s)}{V_a(s)} = \frac{K_m}{s(\tau_ms + 1)} \\ K_m = \frac{K_t}{R_aB + K_tK_b}, \quad \tau_m = \frac{R_aJ}{R_aB + K_tK_b}\end{gathered}$$

The back-emf term $K_tK_b$ acts like extra viscous friction, increasing the damping of the motor.

@s 3
**(a)** Inner loop (forward $G_1 = K/Js$, feedback $H$):

$$\frac{G_1}{1 + G_1H} = \frac{K/Js}{1 + KH/Js} = \frac{K}{Js + KH}$$

Then multiplying by the integrator $\dfrac1s$, the forward path of the outer unity-feedback loop is $\dfrac{K}{s(Js + KH)}$:

$$\frac{C(s)}{R(s)} = \frac{\dfrac{K}{s(Js + KH)}}{1 + \dfrac{K}{s(Js + KH)}} = \frac{K}{Js^2 + KHs + K} = \frac{K/J}{s^2 + \dfrac{KH}{J}s + \dfrac{K}{J}}$$

Comparing with $s^2 + 2\zeta\omega_ns + \omega_n^2$ (with $J = 1$): $\omega_n^2 = K$ and $2\zeta\omega_n = KH$.

**From the specifications.**

$$M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = 0.25 \ \Rightarrow\ \zeta = \frac{-\ln0.25}{\sqrt{\pi^2 + \ln^2 0.25}} = \frac{1.3863}{\sqrt{9.8696 + 1.9218}} = 0.4037$$

$$t_p = \frac{\pi}{\omega_n\sqrt{1 - \zeta^2}} = 2 \ \Rightarrow\ \omega_n = \frac{\pi}{2\sqrt{1 - 0.4037^2}} = \frac{1.5708}{0.9149} = 1.717 \text{ rad/s}$$

$$\begin{gathered}K = J\omega_n^2 = (1.717)^2 = \boxed{2.95} \\ H = \frac{2\zeta\omega_n}{K} = \frac{2(0.4037)(1.717)}{2.948} = \boxed{0.470}\end{gathered}$$

Check: $K = 2.948$, $H = 0.4703$ give $s^2 + 1.386s + 2.948$, i.e. $\omega_n = 1.717$, $\zeta = 1.386/(2\times1.717) = 0.404$ ✓.

**(b)** $s(1 + 0.4s)(1 + 0.25s) = s(0.1s^2 + 0.65s + 1)$. The characteristic equation $1 + G(s) = 0$:

$$0.1s^3 + 0.65s^2 + s + K = 0 \quad\Longrightarrow\quad s^3 + 6.5s^2 + 10s + 10K = 0$$

Routh array:

| $s^3$ | 1 | 10 |
|---|---|---|
| $s^2$ | 6.5 | $10K$ |
| $s^1$ | $\dfrac{6.5(10) - 10K}{6.5} = \dfrac{65 - 10K}{6.5}$ | 0 |
| $s^0$ | $10K$ | |

**(i)** For stability: $65 - 10K > 0 \Rightarrow K < 6.5$ and $10K > 0 \Rightarrow K > 0$.

$$\boxed{0 < K < 6.5}$$

**(ii)** At the limit $K = 6.5$ the $s^1$ row is zero and the auxiliary equation from the $s^2$ row is $6.5s^2 + 10(6.5) = 0$, so $s^2 = -10$:

$$\begin{gathered}s = \pm j\sqrt{10} \\ \boxed{\omega = \sqrt{10} = 3.16 \text{ rad/s}} \ (f = 0.503 \text{ Hz})\end{gathered}$$

Sustained oscillation at 3.16 rad/s occurs when $K = 6.5$ (the third root is $s = -6.5$). Check: $(s^2 + 10)(s + 6.5) = s^3 + 6.5s^2 + 10s + 65$ ✓.

@s 4
**(a)** $G(s)H(s) = \dfrac{s + 5}{(s - 2)(s + 2)}$ has one open-loop pole in the right half plane ($s = 2$), so $P = 1$. Stability requires $N = +1$ counter-clockwise encirclement of $-1$ ($Z = P - N = 0$).

For $s = j\omega$:

$$\begin{gathered}G(j\omega)H(j\omega) = \frac{5 + j\omega}{-(\omega^2 + 4)}: \\ \mathrm{Re} = \frac{-5}{\omega^2 + 4}, \quad \mathrm{Im} = \frac{-\omega}{\omega^2 + 4}, \quad \angle GH = 180^\circ + \tan^{-1}\frac{\omega}{5}\end{gathered}$$

| $\omega$ (rad/s) | 0 | 1 | 2 | 5 | $\infty$ |
|---|---|---|---|---|---|
| $\mathrm{Re}$ | $-1.25$ | $-1.0$ | $-0.625$ | $-0.172$ | 0 |
| $\mathrm{Im}$ | 0 | $-0.2$ | $-0.25$ | $-0.172$ | 0 |

The plot starts at $-1.25$ (at $\omega = 0$, angle $180^\circ$), moves through the third quadrant and ends at the origin. The only negative-real-axis crossing is at $\omega = 0$. No poles lie on the $j\omega$ axis, so no indentation is needed.

```figure caption="Nyquist plot of (s+5)/((s−2)(s+2)): the closed loop through −1.25 and 0 encircles the critical point −1 once counter-clockwise."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,ax=plt.subplots(figsize=(5.0,3.3)); nyq_a(ax)
```

With the mirror image for $-\omega$ the contour is traversed counter-clockwise (from 0 along the upper half plane to $-1.25$ and back along the lower half plane to 0) and encloses $-1$ once: $N = 1$.

$$Z = P - N = 1 - 1 = 0 \quad\Rightarrow\quad \boxed{\text{the closed-loop system is stable}}$$

Check: $1 + GH = 0 \Rightarrow s^2 + s + 1 = 0$, roots $-0.5 \pm j0.866$ ✓.

**Gain margin.** The phase crossover frequency is $\omega_{pc} = 0$ with $|GH| = 1.25$:

$$\text{GM} = \frac{1}{1.25} = 0.8 = \boxed{-1.94 \text{ dB}}$$

A negative gain margin in dB shows that this system is stable only for gain $K > 0.8$ (conditionally stable): the characteristic equation with gain $K$ is $s^2 + Ks + (5K - 4) = 0$.

**(b)** $G(s)H(s) = \dfrac{60}{(s + 1)(s + 2)(s + 5)}$, all poles in the left half plane ($P = 0$).

**Polar form:**

$$\begin{gathered}|GH| = \frac{60}{\sqrt{1 + \omega^2}\sqrt{4 + \omega^2}\sqrt{25 + \omega^2}} \\ \angle GH = -\left[\tan^{-1}\omega + \tan^{-1}\frac{\omega}{2} + \tan^{-1}\frac{\omega}{5}\right]\end{gathered}$$

| $\omega$ | 0 | 1 | 2 | 2.84 | 4.12 | 10 | $\infty$ |
|---|---|---|---|---|---|---|---|
| $\lvert GH\rvert$ | 6 | 3.72 | 1.76 | 1.00 | 0.476 | 0.052 | 0 |
| $\angle GH$ | $0^\circ$ | $-82.9^\circ$ | $-130.2^\circ$ | $-155^\circ$ | $-180^\circ$ | $-226.4^\circ$ | $-270^\circ$ |

Start: $6\angle0^\circ$; end: $0\angle-270^\circ$ (three more poles than zeros).

**Phase crossover.** Denominator $(s+1)(s+2)(s+5) = s^3 + 8s^2 + 17s + 10$; at $s = j\omega$ it is $(10 - 8\omega^2) + j(17\omega - \omega^3)$. The imaginary part vanishes at $\omega_{pc}^2 = 17$, $\omega_{pc} = 4.123$ rad/s, where

$$GH(j\omega_{pc}) = \frac{60}{10 - 8(17)} = \frac{60}{-126} = -0.476$$

The plot cuts the negative real axis at $-0.476$, which is to the **right** of $-1$ (inside the unit circle). So the plot does not encircle $-1 + j0$: $N = 0$.

```figure caption="Polar (Nyquist, ω > 0) plot of 60/((s+1)(s+2)(s+5)): it starts at 6∠0°, crosses the unit circle at ω = 2.84 rad/s (phase margin 25°) and cuts the negative real axis at −0.476 (ω = 4.12 rad/s), so it does not encircle −1."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
w=np.logspace(-2,3,4000); g=60/((1j*w+1)*(1j*w+2)*(1j*w+5)); fig,ax=plt.subplots(figsize=(5.2,3.6))
ax.plot(g.real,g.imag,color=ACC,lw=1.8); ax.plot(g.real,-g.imag,color=ACC,lw=1.2,ls="--")
t=np.linspace(0,2*np.pi,200); ax.plot(np.cos(t),np.sin(t),color="#aab0ba",lw=0.9,ls=":")
ax.plot(-1,0,"x",color=RED,ms=9,mew=2); ax.text(-1.0,0.35,"−1",color=RED,ha="center"); ax.plot(-0.476,0,"o",color=INK,ms=4); ax.text(-0.476,0.35,"−0.476",ha="center",fontsize=8)
ax.plot(6,0,"o",color=INK,ms=4); ax.text(6,0.4,"ω = 0",ha="center",fontsize=8); ax.axhline(0,color="#aab0ba",lw=0.8); ax.axvline(0,color="#aab0ba",lw=0.8)
wg=2.836; gg=60/((1j*wg+1)*(1j*wg+2)*(1j*wg+5)); ax.plot(gg.real,gg.imag,"o",color=RED,ms=4); ax.text(gg.real-0.2,gg.imag-0.9,"|GH| = 1",fontsize=8,color=RED,ha="right")
ax.annotate("",xy=(3.4,-1.4),xytext=(4.2,-0.9),arrowprops=dict(arrowstyle="-|>",color=ACC)); ax.set_xlim(-2,7); ax.set_ylim(-4,4); ax.set_aspect("equal"); ax.set_xlabel("Re GH"); ax.set_ylabel("Im GH"); ax.grid(True)
```

By the Nyquist criterion, $Z = P - N = 0 - 0 = 0$: **the closed-loop system is stable**.

Margins: $\text{GM} = \dfrac{1}{0.476} = 2.1 = 6.44$ dB. The gain crossover ($|GH| = 1$) is at $\omega_{gc} = 2.84$ rad/s where $\angle GH = -155^\circ$, so $\text{PM} = 25^\circ$. The Routh criterion confirms: $s^3 + 8s^2 + 17s + 10 + 60$ has $8\times17 = 136 > 70$ ✓ (the limit is $K_{gain} = 126/60 = 2.1$ times the present gain).

@s 5
**(a)** $G(s) = \dfrac{K}{s(1 + 0.1s)(1 + 0.001s)}$; required $K_v = 1000\ \text{s}^{-1}$, PM $\ge 45^\circ$.

**Step 1: gain.** $K_v = \lim_{s\to0}sG(s) = K$, so $K = 1000$:

$$G(s) = \frac{1000}{s(1 + 0.1s)(1 + 0.001s)}$$

**Step 2: uncompensated phase margin.** At the gain crossover $|G| = 1$: $\omega\sqrt{1 + 0.01\omega^2}\sqrt{1 + 10^{-6}\omega^2} = 1000$, giving $\omega_{gc} \approx 99.5$ rad/s.

$$\angle G = -90^\circ - \tan^{-1}(0.1\times99.5) - \tan^{-1}(0.001\times99.5) = -90 - 84.26 - 5.68 = -179.9^\circ$$

$$PM_{old} \approx 0.06^\circ \quad(\text{practically marginally stable})$$

**Step 3: lead required.** The lead must supply $45^\circ$ plus a margin for the shift of the crossover to a higher frequency (where the plant phase is lower; here about $10^\circ$ because the plant phase falls steeply):

$$\phi_m = 45^\circ - 0.06^\circ + 10^\circ \approx 55^\circ$$

**Step 4: $\alpha$.**

$$\alpha = \frac{1 - \sin55^\circ}{1 + \sin55^\circ} = \frac{1 - 0.8192}{1 + 0.8192} = 0.0994 \approx 0.1$$

**Step 5: new crossover.** The lead network $\dfrac{1 + Ts}{1 + \alpha Ts}$ has gain $\dfrac{1}{\sqrt\alpha} = 3.17$ ($+10$ dB) at $\omega_m$. Place $\omega_m$ where the plant gain is $\sqrt\alpha = 0.315$ ($-10$ dB):

$$\frac{1000}{\omega\sqrt{1 + 0.01\omega^2}\sqrt{1 + 10^{-6}\omega^2}} = 0.315 \ \Rightarrow\ \omega_m \approx 176.6 \text{ rad/s}$$

**Step 6: corner frequencies.**

$$\begin{gathered}T = \frac{1}{\omega_m\sqrt\alpha} = \frac{1}{176.6(0.3153)} = 0.018 \text{ s} \\ \alpha T = 0.0018 \text{ s}\end{gathered}$$

(zero at $1/T = 55.7$ rad/s and pole at $1/\alpha T = 560$ rad/s.)

$$\begin{gathered}\boxed{G_c(s) = \frac{1 + 0.018s}{1 + 0.0018s}} \quad(\text{with } K = 1000) \\ G_cG = \frac{1000(1 + 0.018s)}{s(1 + 0.1s)(1 + 0.001s)(1 + 0.0018s)}\end{gathered}$$

**Step 7: verification.** At $\omega_m = 176.6$ rad/s:

$$\angle G = -90^\circ - \tan^{-1}(17.66) - \tan^{-1}(0.1766) = -90 - 86.76 - 10.01 = -186.8^\circ$$

$$\angle G_c = \tan^{-1}(0.018\times176.6) - \tan^{-1}(0.0018\times176.6) = 72.5 - 17.6 = 54.9^\circ$$

$$PM = 180^\circ - 186.8^\circ + 54.9^\circ = 48.1^\circ \ \ge 45^\circ \ \checkmark$$

and $K_v = \lim sG_cG = 1000$ ✓ (the compensator has unit dc gain, so the error constant is unchanged).

(A first trial with $\phi_m = 50^\circ$ gave only $44^\circ$, which is why the margin was increased to $55^\circ$.)

```figure caption="Bode diagram of the plant G(s) (grey) and the compensated Gc(s)G(s) (blue). The lead network raises the phase margin from about 0° to about 48° and moves the gain crossover from 99.5 to about 177 rad/s."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
Gf=lambda w:1000/(1j*w*(1+0.1j*w)*(1+0.001j*w)); Gc=lambda w:(1+0.018j*w)/(1+0.0018j*w)
print(bode_pm(Gf,Gc,5,5000))
```

**(b) State model.** $\dfrac{Y(s)}{U(s)} = \dfrac{2}{s^3 + 6s^2 + 11s + 6}$ means $\dddot y + 6\ddot y + 11\dot y + 6y = 2u$. Choose the phase variables $x_1 = y,\ x_2 = \dot y,\ x_3 = \ddot y$:

$$\begin{gathered}\dot x_1 = x_2 \\ \dot x_2 = x_3 \\ \dot x_3 = -6x_1 - 11x_2 - 6x_3 + 2u\end{gathered}$$

$$\boxed{\begin{bmatrix}\dot x_1 \\ \dot x_2 \\ \dot x_3\end{bmatrix} = \begin{bmatrix}0 & 1 & 0 \\ 0 & 0 & 1 \\ -6 & -11 & -6\end{bmatrix}\begin{bmatrix}x_1 \\ x_2 \\ x_3\end{bmatrix} + \begin{bmatrix}0 \\ 0 \\ 2\end{bmatrix}u, \qquad y = \begin{bmatrix}1 & 0 & 0\end{bmatrix}\begin{bmatrix}x_1 \\ x_2 \\ x_3\end{bmatrix}}$$

Equivalent form (controllable canonical form): $\dot{\mathbf x} = A\mathbf x + \begin{bmatrix}0 & 0 & 1\end{bmatrix}^T u$ with $y = \begin{bmatrix}2 & 0 & 0\end{bmatrix}\mathbf x$, the same matrix $A$. Check: $|sI - A| = s^3 + 6s^2 + 11s + 6 = (s + 1)(s + 2)(s + 3)$ and $C(sI - A)^{-1}B = \dfrac{2}{s^3 + 6s^2 + 11s + 6}$ ✓. The eigenvalues (poles) are $-1,\ -2,\ -3$, all in the left half plane, so the system is stable.

---
file: NEBians-IOE-Past-Paper-Control-System-ENEE251-2083-Baishakh.pdf
subject: Control System
level: BE · Year II / Part II
code: ENEE 251
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) What is a control system? Draw the block diagram of a closed loop control system and briefly explain the function of each block. [[4]]

(b) Derive the transfer function $X_1(s)/F(s)$ for the system shown below. Also draw the F-V and F-I analogy circuit of the system. (Figure: spring $K_1$ from the ceiling to mass $M_1$; damper $B_2$ from the ceiling to mass $M_2$; damper $B_1$ between $M_1$ and $M_2$; displacements $x_1(t)$ of $M_1$ and $x_2(t)$ of $M_2$; force $F(t)$ applied to $M_2$.) [[8]]

```figure caption="The mechanical system of Question 1(b), as printed: K1 and B2 are fixed to the ceiling, B1 joins the two masses, and the force F(t) acts on M2."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,ax=canvas(4.6,3.3,(-0.2,6.2),(-0.4,4.4))
ax.plot([0.5,5.6],[4.0,4.0],color=INK,lw=2.5); [ax.plot([x,x+0.2],[4.0,4.2],color=INK,lw=1) for x in np.arange(0.5,5.5,0.25)]
box(ax,2.0,2.4,"M1",w=1.6,h=0.55,fc="#d6e6f7"); box(ax,3.4,0.7,"M2",w=3.6,h=0.55,fc="#d6e6f7")
zz=lambda x,y0,y1,n=6: line(ax,[(x,y0)]+[(x+(0.15 if i%2==0 else -0.15),y0+(y1-y0)*(i+0.5)/n) for i in range(n)]+[(x,y1)])
line(ax,[(1.6,4.0),(1.6,3.8)]); zz(1.6,3.8,2.68); txt(ax,1.15,3.3,"K1")
line(ax,[(4.6,4.0),(4.6,3.2)]); line(ax,[(4.4,3.2),(4.8,3.2)])
line(ax,[(4.6,3.2),(4.6,2.9)]); line(ax,[(4.4,2.9),(4.8,2.9)]); line(ax,[(4.4,2.6),(4.8,2.6)]); line(ax,[(4.6,2.6),(4.6,0.98)]); txt(ax,5.1,2.75,"B2")
line(ax,[(2.2,2.12),(2.2,1.9)]); line(ax,[(2.05,1.9),(2.35,1.9)]); line(ax,[(2.05,1.7),(2.35,1.7)]); line(ax,[(2.2,1.7),(2.2,0.98)]); txt(ax,1.7,1.8,"B1")
arr(ax,[(3.4,0.42),(3.4,-0.3)],c=RED); txt(ax,3.75,-0.1,"F(t)",color=RED)
arr(ax,[(0.5,2.4),(0.5,1.7)],c=ACC); txt(ax,0.35,2.4,"x1(t)",ha="right"); arr(ax,[(0.5,0.7),(0.5,0.0)],c=ACC); txt(ax,0.35,0.7,"x2(t)",ha="right")
```

@q 2
(a) Obtain the overall transfer function $C(s)/R(s)$ using the block diagram reduction technique for the system represented by the block diagram shown in the figure. [[6]]

```figure caption="Block diagram of Question 2(a), redrawn from the paper: three forward blocks G1, G2, G3; a unity feed-forward path from V3 to the third summing point; feedback paths H1 and H2 taken from V4 and H3 taken from C(s)."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,ax=canvas(7.2,3.1,(-0.3,14.2),(-3.0,1.9))
arr(ax,[(0,0),(1.16,0)]); txt(ax,0.2,0.3,"R(s)"); sj(ax,1.4,0,top=None,left="+",bottom="-")
arr(ax,[(1.64,0),(2.55,0)]); txt(ax,2.0,0.3,"V1"); box(ax,3.2,0,"G1"); arr(ax,[(3.85,0),(4.76,0)]); txt(ax,4.3,0.3,"V2"); sj(ax,5.0,0,left="+",bottom="-")
arr(ax,[(5.24,0),(6.75,0)]); txt(ax,5.8,0.3,"V3"); box(ax,7.4,0,"G2"); arr(ax,[(8.05,0),(9.96,0)]); txt(ax,8.5,0.3,"V4"); sj(ax,10.2,0,top="+",left="+",bottom="-")
arr(ax,[(10.44,0),(11.35,0)]); txt(ax,10.9,0.3,"V5"); box(ax,12.0,0,"G3"); arr(ax,[(12.65,0),(14.1,0)]); txt(ax,13.9,0.3,"C(s)",ha="right")
dot(ax,6.0,0); arr(ax,[(6.0,0),(6.0,1.3),(10.2,1.3),(10.2,0.24)]); txt(ax,8.1,1.55,"unity feed-forward",fs=7.5,color=MUT)
dot(ax,9.0,0); line(ax,[(9.0,0),(9.0,-1.2)]); dot(ax,9.0,-1.2); arr(ax,[(9.0,-1.2),(8.05,-1.2)]); box(ax,7.4,-1.2,"H2"); line(ax,[(6.75,-1.2),(5.0,-1.2)]); arr(ax,[(5.0,-1.2),(5.0,-0.24)]); txt(ax,5.55,-0.95,"V7",fs=7.5)
line(ax,[(9.0,-1.2),(9.0,-2.4)]); arr(ax,[(9.0,-2.4),(3.85,-2.4)]); box(ax,3.2,-2.4,"H1"); line(ax,[(2.55,-2.4),(1.4,-2.4)]); arr(ax,[(1.4,-2.4),(1.4,-0.24)]); txt(ax,1.95,-2.15,"V6",fs=7.5)
dot(ax,13.0,0); line(ax,[(13.0,0),(13.0,-1.2)]); arr(ax,[(13.0,-1.2),(12.65,-1.2)]); box(ax,12.0,-1.2,"H3"); line(ax,[(11.35,-1.2),(10.2,-1.2)]); arr(ax,[(10.2,-1.2),(10.2,-0.24)]); txt(ax,10.75,-0.95,"V8",fs=7.5)
```

(b) A system having a forward path transfer function $G(s) = \dfrac{16}{s(s+1)}$ and unity feedback. Determine the value of undamped natural frequency and damping ratio. If tachometer feedback is introduced, the feedback path transfer function becomes $(1 + Ks)$. What should be the value of $K$ to obtain a damping ratio of $0.6$? Also calculate the percentage peak overshoot, first undershoot, peak time and settling time within 2% of the final value. [[6]]

@q 3
(a) The open loop transfer function of a unity feedback control system is given by $G(s) = \dfrac{K}{(s+2)(s+4)(s^2 + 6s + 25)}$. Using the RH criterion, determine the range of gain $K$ for the system to be stable. [[4]]

(b) Draw the root locus for a system whose open loop transfer function is given by $G(s)H(s) = \dfrac{K}{s(s+4)(s^2 + 5s + 20)}$. [[8]]

@q 4
(a) Using the Nyquist criterion, determine the stability of the feedback system whose open loop transfer function is given by $G(s)H(s) = \dfrac{s+5}{(s-2)(s+2)}$. Also find the gain margin. [[6]]

(b) For $G(s) = \dfrac{K}{s(s+2)(s+10)}$, determine the value of $K$ so that the system is stable with GM $= 6$ dB. [[6]]

@q 5
(a) The open-loop transfer function of a unity feedback control system is given by $G(s) = \dfrac{K}{s(1 + 0.2s)}$. Design a lead compensator such that the velocity error constant $K_v = 10$ and the phase margin $= 50^\circ$. [[8]]

(b) Determine the transfer function from the state space model given below: [[4]]

$$\dot{\mathbf x}(t) = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}\mathbf x(t) + \begin{bmatrix} 0 \\ 1 \end{bmatrix}u(t), \qquad y(t) = \begin{bmatrix} 1 & 0 \end{bmatrix}\mathbf x(t)$$

<!-- SOLUTIONS -->

@s 1
**(a) Control system.** A control system is an interconnection of components (a plant together with the devices that drive it) arranged so that the **output (controlled variable) is made to follow a desired input (reference)** automatically, with the required accuracy, speed and stability, in spite of disturbances. In a **closed-loop** system the output is measured and fed back to be compared with the reference, so the actuating error drives the correction.

```figure caption="Block diagram of a closed loop control system: the comparator forms the error e = r − b, the controller and actuator turn it into a drive signal for the plant (process), and the sensor feeds a measure of the output back."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,ax=canvas(7.0,2.5,(-0.3,12.2),(-2.3,1.5))
arr(ax,[(0,0),(1.06,0)]); txt(ax,0.0,0.35,"reference r(t)",ha="left",fs=7.5); sj(ax,1.3,0,left="+",bottom="-")
arr(ax,[(1.54,0),(2.65,0)]); txt(ax,2.05,0.3,"error e",fs=7.5); box(ax,3.6,0,"Controller",w=1.9,fc="#eaf3ff")
arr(ax,[(4.55,0),(5.25,0)]); box(ax,6.1,0,"Actuator",w=1.7,fc="#eaf3ff"); arr(ax,[(6.95,0),(7.65,0)]); box(ax,8.5,0,"Plant",w=1.7,fc="#fff4d6")
arr(ax,[(9.35,0),(11.9,0)]); txt(ax,11.9,0.35,"output c(t)",ha="right",fs=7.5); dot(ax,10.3,0); line(ax,[(10.3,0),(10.3,-1.6)])
arr(ax,[(10.3,-1.6),(7.2,-1.6)]); box(ax,6.1,-1.6,"Sensor",w=1.8,h=0.8,fc="#fff4d6"); line(ax,[(5.0,-1.6),(1.3,-1.6)]); arr(ax,[(1.3,-1.6),(1.3,-0.26)])
txt(ax,3.2,-1.35,"feedback signal b",fs=7.5,color=MUT); txt(ax,8.5,1.05,"disturbance",fs=7.5,color=RED); arr(ax,[(8.5,0.85),(8.5,0.42)],c=RED)
```

Function of each block:

| Block | Function |
|---|---|
| Reference input (command) | The desired value of the output, set by the operator (set-point). |
| Comparator (error detector, ⊗) | Subtracts the feedback signal from the reference, $e = r - b$, giving the actuating error. |
| Controller | Processes the error (amplifies, integrates, differentiates; P, PI, PID, compensators) to produce the control signal that gives the required accuracy and stability. |
| Actuator (final control element) | Converts the low-power control signal into the power needed to drive the plant (motor, valve, heater, amplifier). |
| Plant / process | The system whose output is to be controlled (a motor and load, furnace, aircraft). Disturbances also act here. |
| Sensor / feedback element | Measures the output and converts it to a signal compatible with the reference (tachometer, potentiometer, thermocouple). |

The closed-loop transfer function is $\dfrac{C}{R} = \dfrac{G}{1 + GH}$. Feedback reduces the sensitivity to parameter changes and disturbances, improves accuracy and speed, but can cause instability if badly designed.

**(b) Transfer function.** Take $x_1, x_2$ downward positive with the force $F$ on $M_2$. The mass $M_1$ is held by spring $K_1$ and damper $B_1$ (to $M_2$); $M_2$ is held by damper $B_2$ and pulled by $B_1$.

$$\begin{aligned} M_1\ddot x_1 + K_1x_1 + B_1(\dot x_1 - \dot x_2) &= 0 \\ M_2\ddot x_2 + B_2\dot x_2 + B_1(\dot x_2 - \dot x_1) &= F(t) \end{aligned}$$

Laplace transforms (zero initial conditions):

$$\begin{aligned} (M_1s^2 + B_1s + K_1)\,X_1 - B_1s\,X_2 &= 0 \quad\text{(1)} \\ -B_1s\,X_1 + \left[M_2s^2 + (B_1 + B_2)s\right]X_2 &= F \quad\text{(2)} \end{aligned}$$

From (1), $X_2 = \dfrac{(M_1s^2 + B_1s + K_1)}{B_1s}X_1$. Substituting in (2):

$$X_1\left\{\frac{(M_1s^2 + B_1s + K_1)\left[M_2s^2 + (B_1 + B_2)s\right]}{B_1s} - B_1s\right\} = F$$

$$\frac{X_1(s)}{F(s)} = \frac{B_1s}{(M_1s^2 + B_1s + K_1)\left[M_2s^2 + (B_1 + B_2)s\right] - B_1^2s^2}$$

Cancelling the common factor $s$ and expanding,

$$\boxed{\frac{X_1(s)}{F(s)} = \frac{B_1}{M_1M_2s^3 + \left[M_1(B_1 + B_2) + B_1M_2\right]s^2 + (B_1B_2 + K_1M_2)\,s + K_1(B_1 + B_2)}}$$

**Analogous circuits.**

| Mechanical | F-V (force = voltage) | F-I (force = current) |
|---|---|---|
| Force $F$ | voltage source $v$ | current source $i$ |
| Velocity $\dot x$ | mesh current | node voltage |
| Mass $M$ | inductance $L = M$ | capacitance $C = M$ |
| Damper $B$ | resistance $R = B$ | conductance $G = B$ ($R = 1/B$) |
| Spring $K$ | capacitance $C = 1/K$ | inductance $L = 1/K$ |
| Elements in parallel/series sharing a mass | same mesh (series) | same node (parallel) |
| Two masses joined by a damper | shared branch between two meshes | resistor between two nodes |

*F-V analogy (mesh equations).* With mesh currents $i_1 = \dot x_1$, $i_2 = \dot x_2$:

$$\begin{gathered}M_1\frac{di_1}{dt} + \frac{1}{C_1}\!\int i_1\,dt + B_1(i_1 - i_2) = 0 \\ M_2\frac{di_2}{dt} + B_2i_2 + B_1(i_2 - i_1) = F\end{gathered}$$

```figure caption="F-V (force-voltage) analogous circuit: mesh 1 contains L = M1 and C = 1/K1; mesh 2 contains L = M2, R = B2 and the source F; the resistor R = B1 is common to both meshes."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen"))
fig,ax=ckt_canvas(5.4,2.9,(-0.8,8.8),(-0.8,3.2))
ind(ax,(0,2.5),(2.4,2.5),"L = M1"); wire(ax,[(2.4,2.5),(2.6,2.5)]); ind(ax,(2.6,2.5),(5.2,2.5),"L = M2")
cap(ax,(0,2.5),(0,0),"C = 1/K1",side=-1); res(ax,(2.5,2.5),(2.5,0),"R = B1",side=1)
wire(ax,[(5.2,2.5),(7.2,2.5)]); vsrc(ax,(7.2,0),(7.2,2.5),"F",side=1); res(ax,(5.2,0),(2.5,0),"R = B2",side=-1,off=0.4); wire(ax,[(7.2,0),(5.2,0)]); wire(ax,[(2.5,0),(0,0)])
node(ax,(2.5,2.5)); node(ax,(2.5,0)); mesh(ax,(1.2,1.25),0.45,"i1"); mesh(ax,(4.9,1.25),0.45,"i2")
```

*F-I analogy (node equations).* With node voltages $v_1 = \dot x_1$, $v_2 = \dot x_2$ measured from the reference (ceiling) node:

$$\begin{gathered}C_1\frac{dv_1}{dt} + \frac{1}{L_1}\!\int v_1\,dt + G_1(v_1 - v_2) = 0 \\ C_2\frac{dv_2}{dt} + G_2v_2 + G_1(v_2 - v_1) = i_F\end{gathered}$$

```figure caption="F-I (force-current) analogous circuit: node 1 has C = M1 and L = 1/K1 to the reference node; node 2 has C = M2, R = 1/B2 and the current source F; R = 1/B1 joins node 1 to node 2."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen"))
fig,ax=ckt_canvas(5.6,3.0,(-0.8,9.2),(-0.9,3.4))
wire(ax,[(0.5,3),(2.5,3)]); res(ax,(2.5,3),(4.7,3),"R = 1/B1",side=1); wire(ax,[(4.7,3),(7.7,3)])
cap(ax,(0.5,3),(0.5,0),"C = M1",side=-1); ind(ax,(2.5,3),(2.5,0),"L = 1/K1",side=1)
cap(ax,(5.4,3),(5.4,0),"C = M2",side=-1); res(ax,(6.5,3),(6.5,0),"R = 1/B2",side=1); isrc(ax,(7.7,0),(7.7,3),"F",side=1)
wire(ax,[(0.5,0),(7.7,0)]); gnd(ax,(4.0,0)); node(ax,(2.5,3)); node(ax,(4.7,3)); label(ax,(1.5,3.35),"v1"); label(ax,(5.9,3.35),"v2")
```

@s 2
**(a)** Reading the diagram: $V_1 = R - V_6$; $V_2 = G_1V_1$; $V_3 = V_2 - V_7$; $V_4 = G_2V_3$; $V_5 = V_4 + V_3 - V_8$ (the unity feed-forward path adds $V_3$); $C = G_3V_5$; and the feedbacks $V_6 = H_1V_4$, $V_7 = H_2V_4$, $V_8 = H_3C$.

**Step 1: the inner loop (H1, H2) around G1 G2.** Write everything in terms of $V_3$:

$$V_3 = G_1(R - H_1G_2V_3) - H_2G_2V_3 \ \Rightarrow\ V_3\left(1 + G_1G_2H_1 + G_2H_2\right) = G_1R$$

$$\frac{V_3}{R} = \frac{G_1}{1 + G_2H_2 + G_1G_2H_1}$$

**Step 2: the output stage.** The two parallel paths $G_2$ and $1$ from $V_3$ to the summing point give $(1 + G_2)V_3$; then $G_3$ with feedback $H_3$:

$$C = G_3\left[(1 + G_2)V_3 - H_3C\right] \ \Rightarrow\ \frac{C}{V_3} = \frac{G_3(1 + G_2)}{1 + G_3H_3}$$

**Step 3: combine.**

$$\boxed{\frac{C(s)}{R(s)} = \frac{G_1G_3\,(1 + G_2)}{(1 + G_3H_3)\,(1 + G_2H_2 + G_1G_2H_1)}}$$

(Verified symbolically with sympy by solving the nine node equations.) Block-by-block, the reduction is: (i) move the $H_1$ take-off point to $V_4$ onto the loop of $H_2$, (ii) combine $H_1$ and $H_2$ into one loop $G_2(H_2 + G_1H_1)$ around $G_2$, (iii) add the parallel paths $G_2 + 1$, (iv) close the $H_3$ loop around $G_3$.

**(b)** *Unity feedback.* $\dfrac{C}{R} = \dfrac{16}{s^2 + s + 16}$. Comparing with $s^2 + 2\zeta\omega_ns + \omega_n^2$:

$$\begin{gathered}\omega_n^2 = 16 \Rightarrow \boxed{\omega_n = 4 \text{ rad/s}} \\ 2\zeta\omega_n = 1 \Rightarrow \boxed{\zeta = 0.125}\ (\text{very under-damped})\end{gathered}$$

*With tachometer feedback.* $H(s) = 1 + Ks$:

$$\frac{C}{R} = \frac{G}{1 + GH} = \frac{16}{s^2 + s + 16(1 + Ks)} = \frac{16}{s^2 + (1 + 16K)s + 16}$$

$\omega_n = 4$ is unchanged and $2\zeta\omega_n = 1 + 16K$. For $\zeta = 0.6$:

$$2(0.6)(4) = 4.8 = 1 + 16K \ \Rightarrow\ \boxed{K = 0.2375}$$

*Transient specifications* ($\zeta = 0.6$, $\omega_n = 4$, $\omega_d = \omega_n\sqrt{1 - \zeta^2} = 3.2$ rad/s):

$$M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}}\times100 = e^{-\pi(0.6)/0.8}\times100 = \boxed{9.48\%}$$

$$\text{First undershoot} = M_p^2 = (0.0948)^2 = 0.00898 \Rightarrow \boxed{0.90\%} \text{ (below the final value, at } t = 2t_p)$$

$$\begin{gathered}t_p = \frac{\pi}{\omega_d} = \frac{\pi}{3.2} = \boxed{0.982 \text{ s}} \\ t_s(2\%) = \frac{4}{\zeta\omega_n} = \frac{4}{0.6\times4} = \boxed{1.67 \text{ s}}\end{gathered}$$

The first undershoot occurs at $t = 2t_p = 1.96$ s.

@s 3
**(a)** The characteristic equation is $1 + G(s) = 0$, i.e. $(s + 2)(s + 4)(s^2 + 6s + 25) + K = 0$. First, $(s+2)(s+4) = s^2 + 6s + 8$, so

$$(s^2 + 6s + 8)(s^2 + 6s + 25) = s^4 + 12s^3 + 69s^2 + 198s + 200$$

$$s^4 + 12s^3 + 69s^2 + 198s + (200 + K) = 0$$

Routh array:

| $s^4$ | 1 | 69 | $200 + K$ |
|---|---|---|---|
| $s^3$ | 12 | 198 | 0 |
| $s^2$ | $\dfrac{12(69) - 198}{12} = 52.5$ | $200 + K$ | |
| $s^1$ | $\dfrac{52.5(198) - 12(200 + K)}{52.5} = \dfrac{7995 - 12K}{52.5}$ | 0 | |
| $s^0$ | $200 + K$ | | |

For stability all first-column terms must be positive: $7995 - 12K > 0 \Rightarrow K < 666.25$; and $200 + K > 0 \Rightarrow K > -200$. With $K \ge 0$ for a gain:

$$\boxed{0 < K < 666.25}$$

At $K = 666.25$ the $s^1$ row vanishes and the auxiliary equation $52.5s^2 + 866.25 = 0$ gives sustained oscillation at $\omega = \sqrt{16.5} = 4.06$ rad/s.

**(b)** $G(s)H(s) = \dfrac{K}{s(s + 4)(s^2 + 5s + 20)}$.

**Step 1: poles and zeros.** Poles at $s = 0$, $s = -4$, and $s = -2.5 \pm j3.708$ (from $s^2 + 5s + 20$: $\sqrt{20 - 6.25} = 3.708$). No finite zeros. $n = 4$ branches, all ending at infinity.

**Step 2: real-axis locus.** To the left of an odd number of poles/zeros: the segment $-4 \le s \le 0$.

**Step 3: asymptotes** ($n - m = 4$):

$$\begin{gathered}\theta_A = \frac{(2k + 1)180^\circ}{4} = \pm45^\circ,\ \pm135^\circ \\ \sigma_A = \frac{\sum\text{poles} - \sum\text{zeros}}{n - m} = \frac{0 - 4 - 2.5 - 2.5}{4} = -2.25\end{gathered}$$

**Step 4: breakaway point.** $K = -s(s + 4)(s^2 + 5s + 20) = -(s^4 + 9s^3 + 40s^2 + 80s)$ and $dK/ds = 0$:

$$4s^3 + 27s^2 + 80s + 80 = 0 \quad\Rightarrow\quad s = -1.807,\ -2.47 \pm j2.23$$

Only $s = -1.807$ lies on the locus (between $-4$ and $0$); the value of $K$ there is $K = 56.4$. So $\boxed{\sigma_b = -1.81}$ (breakaway from the real axis between the poles at 0 and $-4$).

**Step 5: angle of departure** from the complex pole $p = -2.5 + j3.708$:

$$\theta_d = 180^\circ - \left[\angle(p - 0) + \angle(p + 4) + \angle(p - p^*)\right] = 180^\circ - (123.99^\circ + 67.98^\circ + 90^\circ) = -101.97^\circ$$

so the complex branches leave at about $-102^\circ$ (and $+102^\circ$ from the conjugate pole), i.e. heading downward/upward and curving toward the asymptotes.

**Step 6: imaginary-axis crossing.** Characteristic equation $s^4 + 9s^3 + 40s^2 + 80s + K = 0$.

| $s^4$ | 1 | 40 | $K$ |
|---|---|---|---|
| $s^3$ | 9 | 80 | 0 |
| $s^2$ | $\dfrac{9(40) - 80}{9} = 31.11$ | $K$ | |
| $s^1$ | $\dfrac{31.11(80) - 9K}{31.11}$ | | |
| $s^0$ | $K$ | | |

The $s^1$ term vanishes at $K = \dfrac{31.11\times80}{9} = 276.5$. The auxiliary equation $31.11s^2 + 276.5 = 0$ gives $s = \pm j\sqrt{8.889} = \pm j2.98$.

$$\boxed{K_{max} = 276.5 \text{ (system is stable for } 0 < K < 276.5), \quad \omega_c = 2.98 \text{ rad/s}}$$

The other two roots at this gain are $-4.5 \pm j3.30$ (their sum with $\pm j2.98$ checks against $-9$: $2(-4.5) = -9$ ✓).

```figure caption="Root locus of G(s)H(s) = K / [s(s+4)(s²+5s+20)]: poles (×) at 0, −4 and −2.5 ± j3.71; asymptotes at ±45° and ±135° from σA = −2.25; breakaway at −1.81 (K = 56.4); imaginary-axis crossing at ±j2.98 (K = 276.5)."
D=np.array([1,9,40,80,0.]); Ks=np.concatenate([np.linspace(0,60,500),np.linspace(60,400,1200)])
R=np.array([np.roots(D+np.array([0,0,0,0,k])) for k in Ks])
fig,ax=plt.subplots(figsize=(5.8,4.0))
for i in range(4):
    ax.plot(R[:,i].real,R[:,i].imag,".",ms=1.6,color=ACCENT)
ax.plot([0,-4,-2.5,-2.5],[0,0,3.708,-3.708],"x",color=INK,ms=8,mew=2)
for a_ in (45,135,225,315):
    c,s=np.cos(np.radians(a_)),np.sin(np.radians(a_)); ax.plot([-2.25,-2.25+6*c],[0,6*s],"--",color="#aab0ba",lw=1)
ax.plot(-1.807,0,"o",color="#d9534f",ms=5); ax.text(-1.75,0.35,"breakaway\n−1.81",fontsize=7.5,color="#d9534f")
ax.plot([0,0],[2.98,-2.98],"s",color="#2e8b57",ms=5); ax.text(0.2,3.1,"K = 276.5, ω = 2.98",fontsize=7.5,color="#2e8b57")
ax.plot(-2.25,0,"+",color=INK); ax.text(-2.25,-0.45,"σA = −2.25",fontsize=7.5,ha="center")
ax.axhline(0,color="#8a93a0",lw=0.8); ax.axvline(0,color="#8a93a0",lw=0.8); ax.set_xlim(-7,2.5); ax.set_ylim(-5.5,5.5); ax.set_xlabel("real axis (σ)"); ax.set_ylabel("imaginary axis (jω)"); ax.grid(True)
```

@s 4
**(a)** $G(s)H(s) = \dfrac{s + 5}{(s - 2)(s + 2)}$ has one pole in the right half plane ($s = 2$), so $P = 1$. The system is stable if the Nyquist plot encircles $-1$ counter-clockwise $N = P = 1$ time ($Z = P - N = 0$).

**Frequency response.** $G(j\omega)H(j\omega) = \dfrac{5 + j\omega}{(j\omega)^2 - 4} = \dfrac{-(5 + j\omega)}{\omega^2 + 4}$, so

$$\begin{gathered}\mathrm{Re} = \frac{-5}{\omega^2 + 4} \\ \mathrm{Im} = \frac{-\omega}{\omega^2 + 4} \\ |GH| = \frac{\sqrt{25 + \omega^2}}{\omega^2 + 4} \\ \angle GH = 180^\circ + \tan^{-1}\frac{\omega}{5}\end{gathered}$$

| $\omega$ (rad/s) | 0 | 1 | 2 | 5 | $\infty$ |
|---|---|---|---|---|---|
| $\mathrm{Re}$ | $-1.25$ | $-1.0$ | $-0.625$ | $-0.172$ | 0 |
| $\mathrm{Im}$ | 0 | $-0.2$ | $-0.25$ | $-0.172$ | 0 |

The locus starts on the negative real axis at $-1.25$ (angle $180^\circ$), goes through the third quadrant for $\omega > 0$ and ends at the origin. The only crossing of the negative real axis is at $\omega = 0$, at $-1.25$. There are no poles on the $j\omega$ axis, so no indentation is needed. The mirror image ($\omega < 0$) closes the curve.

```figure caption="Nyquist plot of (s+5)/((s−2)(s+2)): a closed loop through −1.25 and 0 that encloses the critical point −1 once in the counter-clockwise direction."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
fig,ax=plt.subplots(figsize=(5.0,3.3)); nyq_a(ax)
```

**Encirclements.** The plot is traversed (with increasing $\omega$ from $-\infty$ to $+\infty$) from 0 through the upper half plane to $-1.25$ and back through the lower half plane to 0, which is **counter-clockwise**. The point $-1 + j0$ lies inside this loop (since $-1.25 < -1 < 0$), so $N = +1$ (counter-clockwise).

$$Z = P - N = 1 - 1 = 0 \quad\Rightarrow\quad \boxed{\text{the closed-loop system is stable}}$$

Check: the characteristic equation $1 + GH = 0$ gives $(s - 2)(s + 2) + (s + 5) = s^2 + s + 1 = 0$, whose roots $-0.5 \pm j0.866$ are in the left half plane ✓.

**Gain margin.** The phase crossover frequency (angle $= 180^\circ$) is $\omega_{pc} = 0$, where $|GH| = 1.25$:

$$\text{GM} = \frac{1}{|GH(j\omega_{pc})|} = \frac{1}{1.25} = 0.8 = 20\log(0.8) = \boxed{-1.94 \text{ dB}}$$

The negative (less than 1) gain margin means the system is **conditionally stable**: with a gain $K$ in front, the characteristic equation $s^2 + Ks + (5K - 4) = 0$ is stable only for $K > 0.8$. Reducing the gain by more than 20% would make the system unstable.

**(b)** $G(s) = \dfrac{K}{s(s + 2)(s + 10)}$. The phase is $\angle G(j\omega) = -90^\circ - \tan^{-1}\dfrac{\omega}{2} - \tan^{-1}\dfrac{\omega}{10}$.

**Phase crossover frequency.** From the denominator $s^3 + 12s^2 + 20s$ at $s = j\omega$: $-j\omega^3 - 12\omega^2 + j20\omega$, and the imaginary part vanishes at $\omega^2 = 20$:

$$\omega_{pc} = \sqrt{20} = 4.472 \text{ rad/s}$$

**Magnitude at $\omega_{pc}$:**

$$|G(j\omega_{pc})| = \frac{K}{\omega\sqrt{\omega^2 + 4}\sqrt{\omega^2 + 100}} = \frac{K}{4.472\times4.899\times10.954} = \frac{K}{240}$$

**Gain margin:** $\text{GM} = \dfrac{1}{|G(j\omega_{pc})|} = \dfrac{240}{K}$, so the limiting gain for stability is $K = 240$. For $\text{GM} = 6$ dB $= 10^{6/20} = 2$ (a factor of 2):

$$\frac{240}{K} = 2 \quad\Rightarrow\quad \boxed{K = 120}$$

Check: $20\log(240/120) = 6.02$ dB ✓. (Routh gives the same limit: $s^3 + 12s^2 + 20s + K$, stable for $K < 240$.)

@s 5
**(a) Lead compensator design.** $G(s) = \dfrac{K}{s(1 + 0.2s)}$. Required: $K_v = 10$, phase margin $\ge 50^\circ$.

**Step 1: gain K.** $K_v = \lim_{s\to0}sG(s) = K$, therefore $K = 10$ and the compensator must have unity dc gain:

$$G(s) = \frac{10}{s(1 + 0.2s)}$$

**Step 2: uncompensated margin.** At the gain crossover $|G(j\omega)| = 1$:

$$\frac{10}{\omega\sqrt{1 + 0.04\omega^2}} = 1 \ \Rightarrow\ 0.04\omega^4 + \omega^2 - 100 = 0 \ \Rightarrow\ \omega_{gc} = 6.25 \text{ rad/s}$$

$$PM_{old} = 180^\circ - 90^\circ - \tan^{-1}(0.2\times6.25) = 90^\circ - 51.3^\circ = 38.7^\circ$$

**Step 3: phase lead needed.** Add a safety margin of $5^\circ$ for the shift of the crossover:

$$\phi_m = 50^\circ - 38.7^\circ + 5^\circ = 16.3^\circ$$

**Step 4: lead parameter.**

$$\alpha = \frac{1 - \sin\phi_m}{1 + \sin\phi_m} = \frac{1 - 0.2808}{1 + 0.2808} = 0.561$$

The lead network $G_c(s) = \dfrac{1 + Ts}{1 + \alpha Ts}$ raises the gain at $\omega_m$ by $\dfrac{1}{\sqrt\alpha}$ (+2.51 dB). Choose the new gain crossover $\omega_m$ where the old magnitude is $-2.51$ dB $= \sqrt\alpha = 0.749$:

$$\frac{10}{\omega\sqrt{1 + 0.04\omega^2}} = 0.749 \ \Rightarrow\ \omega_m = 7.44 \text{ rad/s}$$

**Step 5: corner frequencies.**

$$\begin{gathered}T = \frac{1}{\omega_m\sqrt\alpha} = \frac{1}{7.44(0.749)} = 0.179 \text{ s} \\ \alpha T = 0.1006 \text{ s}\end{gathered}$$

(zero at $1/T = 5.58$ rad/s, pole at $1/\alpha T = 9.94$ rad/s.)

$$\begin{gathered}\boxed{G_c(s) = \frac{1 + 0.179s}{1 + 0.1006s}} \\ \text{(with } K = 10\text{)} \\ G_cG = \frac{10(1 + 0.179s)}{s(1 + 0.2s)(1 + 0.1006s)}\end{gathered}$$

**Step 6: verify.** At $\omega = 7.44$: the compensated gain is $|G_cG| = 1$ exactly (by design); the phase is

$$\angle G_cG = -90^\circ - \tan^{-1}(0.2\times7.44) + \tan^{-1}(0.179\times7.44) - \tan^{-1}(0.1006\times7.44) = -90 - 56.1 + 53.1 - 36.8 = -129.8^\circ$$

$$PM = 180^\circ - 129.8^\circ = 50.2^\circ \ \ge 50^\circ \ \checkmark$$

and $K_v = \lim sG_cG = 10$ ✓.

```figure caption="Bode diagram of the uncompensated G(s) (grey) and the lead-compensated Gc(s)G(s) (blue): the phase margin rises from 38.7° to 50.2° and the gain crossover moves from 6.25 to 7.44 rad/s."
import sys,os; sys.path.insert(0,os.path.join(os.getcwd(),"notes/papers/engineering/tools/cs_gen")); from bdlib import *
Gf=lambda w:10/(1j*w*(1+0.2j*w)); Gc=lambda w:(1+0.17935j*w)/(1+0.10062j*w)
res=bode_pm(Gf,Gc,0.5,100); print(res)
```

**(b) Transfer function from the state space model.** $A = \begin{bmatrix}0 & 1 \\ -2 & -3\end{bmatrix}$, $B = \begin{bmatrix}0 \\ 1\end{bmatrix}$, $C = \begin{bmatrix}1 & 0\end{bmatrix}$, $D = 0$. The transfer function is $G(s) = C(sI - A)^{-1}B + D$.

$$sI - A = \begin{bmatrix}s & -1 \\ 2 & s + 3\end{bmatrix}, \qquad |sI - A| = s(s + 3) + 2 = s^2 + 3s + 2$$

$$(sI - A)^{-1} = \frac{1}{s^2 + 3s + 2}\begin{bmatrix}s + 3 & 1 \\ -2 & s\end{bmatrix}$$

$$(sI - A)^{-1}B = \frac{1}{s^2 + 3s + 2}\begin{bmatrix}1 \\ s\end{bmatrix}, \qquad G(s) = C(sI - A)^{-1}B = \frac{1}{s^2 + 3s + 2}$$

$$\boxed{\frac{Y(s)}{U(s)} = \frac{1}{s^2 + 3s + 2} = \frac{1}{(s + 1)(s + 2)}}$$

The poles are the eigenvalues of $A$: $-1$ and $-2$ (stable).

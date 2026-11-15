---
file: NEBians-IOE-Past-Paper-Power-System-Analysis-II-ENEE252-2083-Baishakh.pdf
subject: Power System Analysis II
level: BE · Year II / Part II
code: ENEE 252
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electrical Engineering (BEL), Year II / Part II. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
a) Using appropriate mathematical derivations, the phase angle (power/loading angle) δ between E$_f$ and V$_t$ is due solely to the real power delivered by the synchronous generator. [[5]]

b) For the power system network shown below (three buses 1, 2, 3 joined by three lines), obtain the bus admittance matrix. The series impedance and shunt half-charging admittance of each line are 0.05 + j0.15 p.u. and j0.03 p.u. respectively. If a tap-changing transformer having turn ratio (t) = 1:1.05 is inserted mid-point between buses 1 and 2, find the modified bus admittance matrix. [[3+4]]

@q 2
a) What are the buses are considered in the Newton-Raphson load flow analysis method? Specify and elaborate the characteristics of the buses. [[2+3]]

b) The single line diagram of power system network is shown in the figure below (buses 1, 2, 3; lines 1-2 of 100 km, 1-3 of 200 km and 2-3 of 400 km). The Y bus of the system and bus data are shown in the table. (Use N-R method). [[4+3]]

$$Y_{bus} = \begin{bmatrix}-j12 & j6 & j6\\ j6 & -j12 & j6\\ j6 & j6 & -j12\end{bmatrix}$$

| Bus | Bus type | Injected P | Injected Q | Bus voltage magnitude | Voltage phase angle |
|---|---|---|---|---|---|
| 1 | Slack | - | - | 1 | 0 |
| 2 | PV | 0.6 | - | 1 | - |
| 3 | PQ | -0.5 | -0.4 | - | - |

(i) Form the Jacobian Matrix.

(ii) Find the unknown values after the first iteration.

@q 3
a) With suitable mathematical aid, show that in a delta connection, zero sequence components of current are absent in the line currents. [[5]]

b) The figure below shows a power system network (generators G1 and G2, each 100 MVA, 11 kV, 20 %, behind 100 MVA 11/132 kV, 5 % transformers; line L1: 100 km, 1.2 mH/phase/km between the two 132 kV buses; lines L2 and L3: 50 km, 1 mH/phase/km each, from the two buses to the fault point F). A three-phase fault occurs at point F in the system. Using the given system data: Determine the fault MVA at the point of fault and the corresponding fault current. [[4+3]]

@q 4
a) Show that for the two-conductor open circuit fault in a 3-phase system, the sequence networks are to be connected in series to simulate the fault. [[5]]

b) For the power system network shown below, if Line to Line fault occurs at point 'F' then find the fault current, take fault impedance Z$_f$ = 0.1 p.u. [[7]]

Network data: generator G1 25 MVA, 11 kV, neutral reactance X$_n$ = 0.1 p.u.; transformer T1 30 MVA, 10.8/121 kV (Δ-Y); line X$_1$ = X$_2$ = 100 Ω, X$_0$ = 250 Ω; transformer T2 30 MVA, 121/10.8 kV (Y-Δ); motors M1 15 MVA, 10 kV and M2 7.5 MVA, 10 kV (neutral reactance 0.036 p.u.) on the bus where the fault F occurs. For generator: X$_1$ = X$_2$ = 20 %, X$_0$ = 5 %. For both motors: X$_1$ = X$_2$ = 25 %, X$_0$ = 10 %. For both transformers: X$_1$ = X$_2$ = X$_0$ = 10 %. The neutral reactance of generator G$_1$ and motor M$_2$ are in p.u.

@q 5
a) Justify with appropriate expression that synchronizing power coefficient must be positive for a stable equilibrium power system operating condition. [[5]]

b) A 60 Hz synchronous generator has inertia constant H = 5 MJ/MVA and a direct axis transient reactance X$_d$' = 0.3 p.u. connected to an infinite bus V = 1∠0°. The generator has internal emf E' = 1.17∠26.387° p.u. and P$_e$ = 0.8 p.u. The reactance of transformer and both transmission line are in p.u. (X$_T$ = 0.2, each line X$_L$ = 0.3). A temporary 3-phase fault occurs at the sending end of the line at point 'F'. When the fault is cleared, both the lines is intact. Determine the critical clearing angle and the critical clearing time. [[4+3]]

<!-- SOLUTIONS -->

@s 1
**(a) The load angle depends only on the real power.** Consider a (cylindrical-rotor) generator with a synchronous reactance $X_s$ (resistance neglected) connected to a bus of voltage $V_t$. The phasor relation and the current are

$$\begin{gathered}\vec E_f = \vec V_t + jX_s\vec I \\ \vec I = \frac{E_f\angle\delta - V_t\angle0^\circ}{jX_s}\end{gathered}$$

The complex power delivered to the bus is $S = P + jQ = \vec V_t\vec I^*$:

$$\vec I^* = \frac{E_f\angle{-\delta} - V_t}{-jX_s} = \frac{j\,(E_f\cos\delta - jE_f\sin\delta - V_t)}{X_s} = \frac{E_f\sin\delta + j(E_f\cos\delta - V_t)}{X_s}$$

$$S = V_t\vec I^* = \frac{V_tE_f\sin\delta}{X_s} + j\,\frac{V_t(E_f\cos\delta - V_t)}{X_s}$$

so that

$$\begin{gathered}\boxed{P = \frac{E_fV_t}{X_s}\sin\delta} \\ \boxed{Q = \frac{V_t\,(E_f\cos\delta - V_t)}{X_s}}\end{gathered}$$

**Conclusion.** For a given terminal voltage and a fixed excitation, the real power $P$ is a function of the load angle $\delta$ only, through $\sin\delta$ (a rise of the turbine power input increases $\delta$ and the electrical power until $P = P_{mech}$). The angle $\delta$ is therefore due to the **real power**. The reactive power $Q$ depends mainly on the **magnitude difference** $E_f\cos\delta - V_t$, i.e. on the excitation: for a small $\delta$, $\cos\delta \approx 1$ and $Q \approx V_t(E_f - V_t)/X_s$, nearly independent of the angle. Hence $P$ is controlled by the angle (governor, turbine), and $Q$ by the voltage magnitude (excitation), which is the basis of the P-δ, Q-V decoupling used in the fast-decoupled load flow.

**(b) Bus admittance matrix.** Series admittance of each line $y = \dfrac{1}{0.05 + j0.15} = 2 - j6$ pu; the half-line charging admittance $y_{sh}/2 = j0.03$ at each end.

Diagonal terms (two lines meet at every bus):

$$\begin{gathered}Y_{ii} = 2\left[(2 - j6) + j0.03\right] = 4 - j11.94\ \text{pu} \\ Y_{ij} = -(2 - j6) = -2 + j6\ \text{pu}\end{gathered}$$

$$Y_{bus} = \begin{bmatrix}4 - j11.94 & -2 + j6 & -2 + j6\\ -2 + j6 & 4 - j11.94 & -2 + j6\\ -2 + j6 & -2 + j6 & 4 - j11.94\end{bmatrix}$$

**Tap-changing transformer in line 1-2.** The line series branch becomes a series element with an off-nominal tap ratio. Assuming the tap on the bus-1 side, $t = 1.05$, the transformer impedance is merged with the line impedance (the same $y$), the shunt halves stay at the ends. The terms of the 1-2 branch change to

$$\begin{gathered}Y_{11}' = Y_{11} - y + \frac{y}{t^2},\qquad Y_{12}' = Y_{21}' = -\frac{y}{t},\qquad Y_{22}' = Y_{22}\\ \frac{y}{t^2} = \frac{2 - j6}{1.1025} = 1.814 - j5.442,\qquad \frac{y}{t} = \frac{2 - j6}{1.05} = 1.905 - j5.714\end{gathered}$$

$$Y_{11}' = (4 - j11.94) - (2 - j6) + (1.814 - j5.442) = 3.814 - j11.382$$

$$Y_{bus}' = \begin{bmatrix}3.814 - j11.382 & -1.905 + j5.714 & -2 + j6\\ -1.905 + j5.714 & 4 - j11.94 & -2 + j6\\ -2 + j6 & -2 + j6 & 4 - j11.94\end{bmatrix}\ \text{pu}$$

The matrix remains symmetric (a real tap ratio, no phase shift); the row sums are no longer equal to the shunt charging only, because the transformer gives a different effective admittance at the two ends.

@s 2
**(a) Buses in the Newton-Raphson load flow.** At each bus four variables are involved: $|V|$, $\delta$, $P$ and $Q$. Two are specified and two are unknown, which gives three classes of bus:

| Bus type | Specified | Unknown (to be found) | Typical bus |
|---|---|---|---|
| **Slack (swing / reference) bus** | $|V|$ and $\delta$ (usually $1\angle0^\circ$) | $P$ and $Q$ | One large generator; takes up the system losses and the mismatch |
| **PV (generator / voltage-controlled) bus** | $P$ and $|V|$ | $Q$ and $\delta$ ($Q$ limits checked) | Generators with AVR, synchronous condensers, SVC |
| **PQ (load) bus** | $P$ and $Q$ | $|V|$ and $\delta$ | Load centres, substations |

**Characteristics.** The **slack bus** is a mathematical necessity: the system losses are not known beforehand, so one generator must supply the balance, and its angle fixes the reference of all the other angles; there is exactly one in a system. At a **PV bus** the reactive power is varied (within $Q_{min} \le Q \le Q_{max}$) by the excitation to hold $|V|$; if the limit is reached it is converted to a PQ bus. At a **PQ bus** the demand is fixed, and the voltage varies. For a system of $n$ buses with $n_{PV}$ voltage-controlled buses, the N-R method solves $2(n - 1) - n_{PV}$ equations: the $P$ equations for all non-slack buses and the $Q$ equations for the PQ buses.

**(b)(i) Jacobian.** Unknowns $x = [\delta_2,\ \delta_3,\ |V_3|]^T$; equations $P_2$, $P_3$, $Q_3$:

$$\begin{bmatrix}\Delta P_2\\ \Delta P_3\\ \Delta Q_3\end{bmatrix} = \begin{bmatrix}\partial P_2/\partial\delta_2 & \partial P_2/\partial\delta_3 & \partial P_2/\partial|V_3|\\ \partial P_3/\partial\delta_2 & \partial P_3/\partial\delta_3 & \partial P_3/\partial|V_3|\\ \partial Q_3/\partial\delta_2 & \partial Q_3/\partial\delta_3 & \partial Q_3/\partial|V_3|\end{bmatrix}\begin{bmatrix}\Delta\delta_2\\ \Delta\delta_3\\ \Delta|V_3|\end{bmatrix}$$

With $G_{ik} = 0$ and $B_{12} = B_{13} = B_{23} = 6$, $B_{ii} = -12$, the power equations are

$$\begin{gathered}P_i = \sum_k|V_i||V_k|B_{ik}\sin(\delta_i - \delta_k)\ \ (\text{G} = 0) \\ Q_i = -\sum_k|V_i||V_k|B_{ik}\cos(\delta_i - \delta_k)\end{gathered}$$

so for example $P_2 = 6|V_1||V_2|\sin(\delta_2 - \delta_1) + 6|V_2||V_3|\sin(\delta_2 - \delta_3)$. At the flat start $V = [1, 1, 1]\angle0^\circ$ the elements are

$$\begin{gathered}\frac{\partial P_2}{\partial\delta_2} = 6\cos0 + 6\cos0 = 12,\qquad \frac{\partial P_2}{\partial\delta_3} = -6,\qquad \frac{\partial P_2}{\partial|V_3|} = 6\sin0 = 0\\ \frac{\partial P_3}{\partial\delta_2} = -6,\qquad \frac{\partial P_3}{\partial\delta_3} = 6 + 6 = 12,\qquad \frac{\partial P_3}{\partial|V_3|} = 0\\ \frac{\partial Q_3}{\partial\delta_2} = \frac{\partial Q_3}{\partial\delta_3} = 0,\qquad \frac{\partial Q_3}{\partial|V_3|} = 24|V_3| - 12 = 12\end{gathered}$$

$$\boxed{J^{(0)} = \begin{bmatrix}12 & -6 & 0\\ -6 & 12 & 0\\ 0 & 0 & 12\end{bmatrix}}$$

**(ii) First iteration.** Calculated powers at the flat start are all zero ($P_2 = P_3 = Q_3 = 0$), so the mismatches are

$$\begin{gathered}\Delta P_2 = 0.6 - 0 = 0.6 \\ \Delta P_3 = -0.5 - 0 = -0.5 \\ \Delta Q_3 = -0.4 - 0 = -0.4\end{gathered}$$

Solving $J\,\Delta x = \Delta$:

$$\begin{gathered}12\Delta\delta_2 - 6\Delta\delta_3 = 0.6,\qquad -6\Delta\delta_2 + 12\Delta\delta_3 = -0.5\\ \Delta\delta_2 = \frac{12(0.6) - 6(0.5)}{108} = 0.03889\ \text{rad},\qquad \Delta\delta_3 = \frac{12(-0.5) + 6(0.6)}{108} = -0.02222\ \text{rad}\\ \Delta|V_3| = \frac{-0.4}{12} = -0.03333\end{gathered}$$

$$\boxed{\delta_2^{(1)} = 0.03889\ \text{rad} = 2.228^\circ,\quad \delta_3^{(1)} = -0.02222\ \text{rad} = -1.273^\circ,\quad |V_3|^{(1)} = 0.9667\ \text{pu}}$$

With these values the first-iteration powers are $P_2 = 0.5875$, $Q_2 = 0.2154$, $P_1 = -0.1044$, $Q_1 = 0.2060$ pu. Further iterations converge in 3 to 4 steps to $\delta_2 = 2.256^\circ$, $\delta_3 = -1.349^\circ$, $|V_3| = 0.9643$ pu; then $P_2 = 0.6$, $P_3 = -0.5$, $Q_3 = -0.4$, and the slack bus absorbs $S_1 = -0.100 + j0.220$ pu ($P_1 = 0.6 - 0.5 = +0.1$ surplus returned, $Q_2 = 0.230$ pu supplied by the PV generator).

@s 3
**(a) Zero-sequence current in a delta connection.** Let the line currents be $I_a, I_b, I_c$ and the phase (winding) currents $I_{ab}, I_{bc}, I_{ca}$ in the delta. By Kirchhoff's current law at the three corners:

$$\begin{gathered}I_a = I_{ab} - I_{ca} \\ I_b = I_{bc} - I_{ab} \\ I_c = I_{ca} - I_{bc}\end{gathered}$$

**Method 1 (sum of line currents).** Adding the three equations:

$$I_a + I_b + I_c = 0$$

and the zero-sequence component of a set of three phasors is $I_{a0} = \tfrac13(I_a + I_b + I_c)$, so

$$I_{a0} = 0$$

**Method 2 (sequence components).** Resolve each current into symmetrical components; the zero-sequence components of the three winding currents are equal ($I_{ab0} = I_{bc0} = I_{ca0}$, may circulate in the closed delta). Then, taking the zero-sequence part of $I_a = I_{ab} - I_{ca}$:

$$I_{a0} = I_{ab0} - I_{ca0} = 0$$

Hence, in a delta (or in an ungrounded star with no neutral path), **no zero-sequence current can flow in the lines**, only positive and negative sequence components. A zero-sequence current can circulate **inside the delta winding** if there is a source of zero-sequence voltage ($V_{ab0} = I_{ab0}Z_0$), but it does not leave the delta; that is why a delta winding of a transformer provides a path for the zero-sequence only inside, and blocks it on the line side (the zero-sequence network is open to the line, shorted to the reference at the transformer: $Z_0$ of the delta is connected to the reference bus).

**(b) Fault MVA at F.** Base: $S_b = 100$ MVA, $V_b = 11$ kV on the generator sides and 132 kV on the lines; $Z_b = 132^2/100 = 174.24\ \Omega$. Frequency 50 Hz is assumed.

| Element | Reactance (pu) |
|---|---|
| G1, G2 (100 MVA, 20 %) | $0.20$ |
| T1, T2 (100 MVA, 5 %) | $0.05$ |
| L1: $X = 2\pi\times50\times1.2\times10^{-3}\times100 = 37.70\ \Omega$ | $37.70/174.24 = 0.2164$ |
| L2, L3: $X = 2\pi\times50\times1\times10^{-3}\times50 = 15.71\ \Omega$ | $15.71/174.24 = 0.0902$ |

Each source branch is $X_G + X_T = 0.20 + 0.05 = 0.25$ pu. The two generators have the same emf (1 pu), so during the fault the two ends of L1 are at the same potential: **no current flows in L1** (and it can be removed). The Thevenin reactance seen from F is the two identical branches in parallel:

$$X_{th} = \frac{0.25 + 0.0902}{2} = 0.1701\ \text{pu}\quad(\text{exact network solution: } 0.17008)$$

$$\boxed{\text{Fault MVA} = \frac{S_b}{X_{th}} = \frac{100}{0.1701} \approx 588\ \text{MVA}}$$

$$\begin{gathered}I_f = \frac{1}{X_{th}} = 5.88\ \text{pu} \\ I_b = \frac{100\times10^6}{\sqrt3\times132\times10^3} = 437.4\ \text{A}\end{gathered}$$

$$\boxed{I_f = 5.88\times437.4 \approx 2572\ \text{A}\ (2.57\ \text{kA at 132 kV})}$$

Each generator supplies half of the fault current, 1.29 kA at 132 kV (2.94 pu, 15.4 kA at 11 kV).

@s 4
**(a) Two-conductor open fault (conductors b and c open, a closed).** Let the open section be between the points $a\,a'$, $b\,b'$, $c\,c'$, and let $V_{aa'}, V_{bb'}, V_{cc'}$ be the voltage drops across the break and $I_a, I_b, I_c$ the line currents.

*Conditions for conductors b and c open and a intact:*

$$\begin{gathered}I_b = 0 \\ I_c = 0 \\ V_{aa'} = 0\end{gathered}$$

*Current:* the symmetrical components of the current are

$$\begin{bmatrix}I_{a0}\\ I_{a1}\\ I_{a2}\end{bmatrix} = \frac13\begin{bmatrix}1&1&1\\ 1&a&a^2\\ 1&a^2&a\end{bmatrix}\begin{bmatrix}I_a\\ 0\\ 0\end{bmatrix} = \frac{I_a}{3}\begin{bmatrix}1\\ 1\\ 1\end{bmatrix}\ \Rightarrow\ \boxed{I_{a0} = I_{a1} = I_{a2}}$$

*Voltage:* $V_{aa'} = V_{aa'0} + V_{aa'1} + V_{aa'2} = 0$.

These two conditions (equal sequence currents and the voltage drops across the break adding up to zero) are exactly those that are met by **connecting the three sequence networks in series**, each with its Thevenin impedance seen at the break, $Z_1$, $Z_2$ and $Z_0$, and the pre-fault drop $E$ (the positive-sequence emf $E_{a} = $ the voltage across the break before the fault) acting in the positive-sequence network only:

$$\begin{gathered}V_{aa'1} = E - I_{a1}Z_1 \\ V_{aa'2} = -I_{a2}Z_2 \\ V_{aa'0} = -I_{a0}Z_0\end{gathered}$$

$$\sum V_{aa'} = E - I(Z_1 + Z_2 + Z_0) = 0 \ \Rightarrow\ I_{a1} = I_{a2} = I_{a0} = \frac{E}{Z_1 + Z_2 + Z_0}$$

Thus the positive, negative and zero-sequence networks are connected **in series** through the break, with the sequence current common to all (the same connection as for a single line-to-ground fault, its dual). The line current is $I_a = 3I_{a1}$ and the open phase voltages follow from $V_{aa'}$ of $V_{bb'}, V_{cc'}$.

```figure caption="Question 4(a): sequence networks in series for the two-conductor open fault."
fig,ax=plt.subplots(figsize=(6.2,2.6)); ax.axis('off'); ax.set_xlim(-0.3,12); ax.set_ylim(-0.3,4.2)
vsrc(ax,(0,0.3),(0,3.3),'E',side=-1,off=0.8)
wire(ax,[(0,3.3),(0.7,3.3)]); res(ax,(0.7,3.3),(2.7,3.3),'$Z_1$',side=1,body=1.0); wire(ax,[(2.7,3.3),(3.4,3.3)]); res(ax,(3.4,3.3),(5.4,3.3),'$Z_2$',side=1,body=1.0)
wire(ax,[(5.4,3.3),(6.1,3.3)]); res(ax,(6.1,3.3),(8.1,3.3),'$Z_0$',side=1,body=1.0); wire(ax,[(8.1,3.3),(9.0,3.3),(9.0,0.3),(0,0.3)])
arrow(ax,(1.0,3.95),(2.2,3.95),'$I_{a1}=I_{a2}=I_{a0}$',off=0.2)
ax.text(10.1,1.8,'$V_{aa^\\prime}=0$',fontsize=9)
```

**(b) Line-to-line fault.** A line-to-line fault involves only the positive- and negative-sequence networks, so the zero-sequence data (and the neutral reactances) are not needed.

**Base:** $S_b = 30$ MVA, $V_b = 10.8$ kV at the generator and motor sides, $121$ kV on the line ($Z_b = 121^2/30 = 488.03\ \Omega$). Convert the reactances to this base:

| Element | Calculation | pu |
|---|---|---|
| G1 | $0.20\times\dfrac{30}{25}\left(\dfrac{11}{10.8}\right)^2$ | 0.2490 |
| T1, T2 | $0.10$ each (30 MVA, 10.8 kV) | 0.1000 |
| Line | $100/488.03$ | 0.2049 |
| M1 | $0.25\times\dfrac{30}{15}\left(\dfrac{10}{10.8}\right)^2$ | 0.4287 |
| M2 | $0.25\times\dfrac{30}{7.5}\left(\dfrac{10}{10.8}\right)^2$ | 0.8573 |

**Positive-sequence (= negative-sequence) reactance seen from F:**

$$\begin{gathered}X_{gen\ branch} = 0.2490 + 0.10 + 0.2049 + 0.10 = 0.6539\\ X_{motors} = \frac{0.4287\times0.8573}{0.4287 + 0.8573} = 0.2858\\ X_1 = X_2 = \frac{0.6539\times0.2858}{0.6539 + 0.2858} = 0.1989\ \text{pu}\end{gathered}$$

**Fault current.** The pre-fault voltage is $E = 1$ pu and the fault impedance $Z_f = 0.1$ pu is connected between the two faulted phases; it is treated as a reactance, $Z_f = j0.1$ pu, like the other data (the same unit as the network reactances):

$$I_{a1} = -I_{a2} = \frac{E}{j(X_1 + X_2) + Z_f} = \frac{1}{j(0.1989 + 0.1989 + 0.1)} = -j2.009\ \text{pu}$$

The fault-phase currents are $I_a = 0$ and

$$I_b = -I_c = (a^2 - a)I_{a1} = -j\sqrt3\,I_{a1}\ \Rightarrow\ |I_b| = \sqrt3\times2.009 = 3.480\ \text{pu}$$

$$I_{base} = \frac{30\times10^6}{\sqrt3\times10.8\times10^3} = 1603.8\ \text{A}$$

$$\boxed{I_f = |I_b| = |I_c| = 3.480\times1603.8 \approx 5581\ \text{A}\ (\approx 5.58\ \text{kA at 10.8 kV})}$$

If $Z_f$ were instead a pure resistance of 0.1 pu, then $|I_{a1}| = 1/\sqrt{0.3978^2 + 0.1^2} = 2.438$ pu, and $I_f = \sqrt3\times2.438 = 4.22$ pu $= 6.77$ kA.

*Contributions (positive-sequence, $Z_f = j0.1$):* the generator branch supplies $2.009\times0.2858/0.9397 = 0.611$ pu and the motors $1.398$ pu of the positive-sequence current; the fault is fed 70 % by the motors (the motor reactance is much lower than the generator branch).

@s 5
**(a) Synchronising power coefficient.** For a generator connected to an infinite bus, the electrical power is $P_e = P_{max}\sin\delta$. Let the machine run in equilibrium at $\delta_0$ with $P_m = P_{e0} = P_{max}\sin\delta_0$. After a small disturbance $\Delta\delta$ the swing equation (small angle, linearised) is

$$\frac{2H}{\omega_s}\frac{d^2\delta}{dt^2} = P_m - P_{max}\sin\delta\ \ \Rightarrow\ \ \frac{2H}{\omega_s}\frac{d^2(\Delta\delta)}{dt^2} + \left(\frac{dP_e}{d\delta}\right)_{\delta_0}\Delta\delta = 0$$

$$\boxed{P_s = \left.\frac{dP_e}{d\delta}\right|_{\delta_0} = P_{max}\cos\delta_0}\quad\text{(the synchronising power coefficient, pu MW/rad)}$$

The characteristic equation is $\dfrac{2H}{\omega_s}s^2 + P_s = 0$, so $s = \pm\sqrt{-P_s\omega_s/2H}$:

- **$P_s > 0$** ($\delta_0 < 90^\circ$): $s = \pm j\omega_n$, $\omega_n = \sqrt{\dfrac{\omega_sP_s}{2H}}$. The rotor **oscillates** about $\delta_0$ and (with damping) returns to it. The restoring (synchronising) torque opposes the displacement, so the equilibrium is **stable**.
- **$P_s < 0$** ($\delta_0 > 90^\circ$): the roots are real, one positive, so $\Delta\delta$ **grows exponentially** and the machine loses synchronism; the equilibrium is unstable.
- **$P_s = 0$** ($\delta_0 = 90^\circ$): the limit of steady-state stability, $P_{max} = E V/X$.

So for stable equilibrium the synchronising power coefficient must be positive: a positive $P_s$ means a rise of $\delta$ raises the electrical output, which slows the rotor down and restores equilibrium. The natural frequency in Hz is $f_n = \dfrac{1}{2\pi}\sqrt{\dfrac{\pi fP_s}{H}}$.

**(b) Critical clearing angle and time.**

*Pre-fault* (both lines in): $X_{pre} = X_d' + X_T + \dfrac{X_L}{2} = 0.3 + 0.2 + 0.15 = 0.65$ pu

$$\begin{gathered}P_{max,1} = \frac{E'V}{X_{pre}} = \frac{1.17\times1}{0.65} = 1.80\ \text{pu} \\ \sin\delta_0 = \frac{P_m}{P_{max,1}} = \frac{0.8}{1.8}\ \Rightarrow\ \delta_0 = 26.39^\circ = 0.4606\ \text{rad}\end{gathered}$$

*During the fault:* the three-phase fault is at the **sending end of the line** (the generator-transformer bus), which holds the bus voltage at zero, so no power can be transferred: $P_{max,2} = 0$ (the generator accelerates with $P_e = 0$).

*Post-fault* (fault cleared, both lines intact): the same network as pre-fault, $P_{max,3} = 1.80$ pu.

**Equal-area criterion.** $\delta_{max} = 180^\circ - \delta_0 = 153.61^\circ = 2.6810$ rad. The accelerating area (during the fault) equals the decelerating area after clearing at $\delta_c$:

$$\int_{\delta_0}^{\delta_c}P_m\,d\delta = \int_{\delta_c}^{\delta_{max}}(P_{max,3}\sin\delta - P_m)\,d\delta$$

$$\cos\delta_c = \frac{P_m(\delta_{max} - \delta_0) + P_{max,3}\cos\delta_{max} - P_{max,2}\cos\delta_0}{P_{max,3} - P_{max,2}}$$

$$\cos\delta_c = \frac{0.8(2.6810 - 0.4606) + 1.8\cos153.61^\circ - 0}{1.8 - 0} = \frac{1.7763 - 1.6100}{1.8} = 0.0924$$

$$\boxed{\delta_c = 84.77^\circ = 1.4796\ \text{rad}}$$

**Critical clearing time.** With $P_e = 0$ during the fault, the swing equation gives a constant acceleration:

$$\frac{d^2\delta}{dt^2} = \frac{\pi f}{H}P_m = \frac{\pi\times60}{5}(0.8) = 30.16\ \text{rad/s}^2$$

$$\delta_c - \delta_0 = \frac12\left(30.16\right)t_c^2\ \Rightarrow\ t_c = \sqrt{\frac{2H(\delta_c - \delta_0)}{\pi fP_m}} = \sqrt{\frac{2\times5\times(1.4796 - 0.4606)}{\pi\times60\times0.8}}$$

$$\boxed{t_c = \sqrt{0.06757} = 0.260\ \text{s}\ (\approx 15.6\ \text{cycles at 60 Hz})}$$

The fault must be cleared in less than **0.26 s** (the angle must not exceed $84.8^\circ$) for the generator to stay in synchronism.

```figure caption="Question 5(b): equal-area criterion: pre/post-fault curve (P_max = 1.8 pu), fault curve (P = 0), P_m = 0.8 pu, clearing angle 84.8 degrees."
fig,ax=plt.subplots(figsize=(5.8,3.4))
d=np.linspace(0,180,400); ax.plot(d,1.8*np.sin(np.radians(d)),color=INK,lw=1.8,label='pre- and post-fault  $P_{max}=1.8$')
ax.plot([0,180],[0,0],color=ACCENT,lw=1.6,label='during fault  $P_e=0$'); ax.axhline(0.8,color=SERIES[2],lw=1.3,label='$P_m=0.8$')
d0,dc,dm=26.39,84.77,153.61
x1=np.linspace(d0,dc,50); ax.fill_between(x1,0,0.8,color='#fecaca',alpha=0.8); ax.text(52,0.33,'$A_1$\naccelerating',fontsize=7.5,ha='center')
x2=np.linspace(dc,dm,100); ax.fill_between(x2,0.8,1.8*np.sin(np.radians(x2)),color='#bbf7d0',alpha=0.9); ax.text(118,0.95,'$A_2$ decelerating',fontsize=7.5,ha='center')
for x,l in ((d0,'$\\delta_0$'),(dc,'$\\delta_c$'),(dm,'$\\delta_{max}$')): ax.axvline(x,color=GRID,ls=':'); ax.text(x,-0.17,l,ha='center',fontsize=8)
ax.set_xlim(0,180); ax.set_ylim(-0.25,2.0); ax.set_xlabel('rotor angle $\\delta$ (degrees)'); ax.set_ylabel('power (pu)'); ax.legend(fontsize=6.8,loc='upper right')
```

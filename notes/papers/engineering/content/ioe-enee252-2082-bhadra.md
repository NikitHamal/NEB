---
file: NEBians-IOE-Past-Paper-Power-System-Analysis-II-ENEE252-2082-Bhadra.pdf
subject: Power System Analysis II
level: BE · Year II / Part II
code: ENEE 252
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE Electrical Engineering (BEL), Year II / Part II. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
a) Explain the consequences of real power on frequency and reactive power on voltage problems in a power system. Also, illustrate the basic control mechanisms in brief to address these are in the real power system. [[3+2]]

b) Consider a 3-bus power system network (generators at buses 1 and 2, three lines joining the three buses, load at bus 3). The series impedance and shunt admittance of each line are 0.026 + j 0.11 pu and j 0.04 pu respectively. Find: [[3+4]]

(i) the bus admittance matrix.

(ii) the modified bus admittance matrix if a tap changing transformer inserted in mid-point between bus 2 and 3 having turn ration t = e$^{j30°}$.

@q 2
a) Why load flow analysis is need in power system? Point out the significance of the slack bus. [[2+3]]

b) Using G-S load flow analysis, compute the voltage at bus 2 of figure shown below if V$_1$ = 1∠0° pu. Find also power flow between bus 1 and 2. (all values are in pu). [[4+3]]

Figure: bus 1 (V$_1$, load S$_{d1}$) joined to bus 2 by a line of Z = j0.75; at bus 2 a shunt source S$_2$ = j1.0 (capacitor) and the load S$_{d2}$ = 0.5 + j1.0.

@q 3
a) Explain the significance of symmetrical components in power system analysis. Also derive the expression for phasor voltages in terms of the symmetrical components of voltages. [[2+3]]

b) An alternator is connected to a synchronous motor through a transmission line and two transformers as shown in the figure below. The rated MVA, voltage rating and percentage reactance of the components are depicted in the figure. The transmission line reactance is also shown in the figure in Ω. Compute the fault current, if a 3-phase bolted fault occurs at the terminal of the generator. Consider the pre fault voltage as 1 p.u. Also determine the fault MVA at the generator terminal. [[3+4]]

Figure data: generator 50 MVA, 11 kV, 10 %; T1 100 MVA, 11/132 kV, 5 %; line j25 Ω; T2 50 MVA, 132/6.6 kV, 4 %; motor 50 MVA, 6.6 kV, 6 %.

@q 4
a) Obtain the sequence network for double line to ground fault (bolted fault) at alternator terminal. [[5]]

b) A 50 MVA, 12 kV, three-phase alternator were subjected to different types of faults. The fault currents were: [[7]]

(i) 1870 A for three-phase fault

(ii) 2590 A for L-L fault

(iii) 4130 A for L-G fault.

The alternator neutral is solidly grounded. Find the three-sequence reactance of the alternator in per unit.

@q 5
a) Define steady state and transient stability of power system. Point out the methods of improving transient stability of a power system. [[3+2]]

b) Starting from the single machine swing equation, derive the expression for equivalent swing equation for multiple generators swinging together. Three generators in a power plant of 50 MVA, 100 MVA & 200 MVA have inertia constant of 6 MJ/MVA each. Compute the equivalent inertia constant at a base of 100 MVA if all units swing together. [[4+3]]

<!-- SOLUTIONS -->

@s 1
**(a) Real power and frequency, reactive power and voltage.**

**Real power balance and frequency.** In a synchronous system the speed of all the generators, and so the frequency, is set by the balance between the mechanical power input and the electrical power demand. The kinetic energy $\tfrac12J\omega^2$ stored in the rotating masses is the buffer:

$$\frac{2H}{f_0}\frac{d\Delta f}{dt} = \Delta P_m - \Delta P_L$$

- If the real-power demand exceeds the generation ($\Delta P_L > \Delta P_m$), the rotors decelerate and the **frequency falls**; a surplus raises it.
- Consequences of off-nominal frequency: motors and clocks run off-speed, the turbine blades suffer resonance and fatigue, the transformers saturate (V/f), the protection and load shedding operate, and a large deficit collapses the system (a frequency collapse, black-out).

**Reactive power and voltage.** The voltage at a bus depends mainly on the reactive power flow, since $\Delta V \approx \dfrac{R\,\Delta P + X\,\Delta Q}{V}$ and $X \gg R$ in transmission:

- A **reactive-power deficit** (inductive loads, long loaded lines, motors starting) makes the **voltage fall** and the current rise (higher losses); an excess (lightly loaded lines, the Ferranti effect, capacitors) makes the **voltage rise**.
- Consequences: low voltage reduces the motor torque and lamp output, causes overheating and tripping, and can lead to a **voltage collapse**; a high voltage stresses the insulation and saturates the transformers.

Reactive power cannot be transmitted over long distances without loss, so it is produced **locally**, whereas the frequency is a **global** quantity. This is why $P$-$f$ and $Q$-$V$ are controlled separately (almost decoupled).

**Control mechanisms**

| Problem | Controller | Action |
|---|---|---|
| Frequency (real power) | **Primary control:** the turbine **governor** (droop $R$, typically 4 to 5 %) | Changes the valve/gate opening with $\Delta f$ within seconds |
| | **Secondary control:** **automatic generation control (AGC / load frequency control)** | Resets the speed changer using the frequency and tie-line deviation (area control error) to restore 50 Hz and the scheduled interchange |
| | Tertiary control: economic dispatch, spinning reserve, under-frequency **load shedding** | Reschedules the units; sheds load in an emergency |
| Voltage (reactive power) | **AVR with excitation system** of the generator | Changes the field current to hold the terminal voltage |
| | **Shunt capacitors / reactors, synchronous condensers, SVC, STATCOM** | Inject or absorb vars at the load bus |
| | **On-load tap-changing transformers**, series capacitors, voltage regulators | Change the turns ratio or the line reactance to adjust the voltage profile |

```figure caption="Question 1(a): the two basic control loops of a generator: the frequency (governor) loop for real power and the voltage (AVR) loop for reactive power."
fig,ax=plt.subplots(figsize=(6.8,3.3)); ax.axis('off'); ax.set_xlim(0,15); ax.set_ylim(0,7)
def bx(x,y,w,h,t,fc='#e0f2fe'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=7)
bx(0.2,4.6,2.4,1.4,'Governor\nspeed changer\n(AGC set-point)','#fde68a'); bx(3.4,4.6,2.2,1.4,'Turbine\nvalve / gate'); bx(6.4,3.0,2.6,2.4,'Generator\n(synchronous)','#dbeafe'); bx(10.0,4.6,2.0,1.4,'Power system\nload'); bx(12.6,4.6,2.2,1.4,'Frequency f\nsensor','#dcfce7')
bx(0.2,0.7,2.4,1.4,'Voltage\nreference','#fde68a'); bx(3.4,0.7,2.2,1.4,'AVR'); bx(6.4,0.7,2.6,1.4,'Exciter\n(field current)'); bx(10.0,0.7,2.0,1.4,'Terminal\nvoltage V','#dcfce7')
for a,b in (((2.6,5.3),(3.4,5.3)),((5.6,5.3),(6.4,5.0)),((9.0,4.2),(10.0,5.0)),((12.0,5.3),(12.6,5.3)),((2.6,1.4),(3.4,1.4)),((5.6,1.4),(6.4,1.4)),((7.7,2.1),(7.7,3.0)),((9.0,3.3),(10.0,1.5))): arrow(ax,a,b,None,color=INK)
ax.plot([13.7,13.7,1.4,1.4],[4.6,6.6,6.6,6.0],color=ACCENT,lw=1.2); arrow(ax,(1.4,6.3),(1.4,6.0),None,color=ACCENT); ax.text(7.5,6.75,'frequency error  $\\Delta f$  (P - f loop)',fontsize=7,ha='center',color=ACCENT)
ax.plot([11.0,11.0,4.5,4.5],[0.7,0.2,0.2,0.7],color=SERIES[3],lw=1.2); ax.text(7.7,0.3,'voltage error  $\\Delta V$  (Q - V loop)',fontsize=7,ha='center',color=SERIES[3])
```

**(b)(i) Bus admittance matrix.** Series admittance of each line:

$$y = \frac{1}{0.026 + j0.11} = \frac{0.026 - j0.11}{0.026^2 + 0.11^2} = 2.0351 - j8.6099\ \text{pu}$$

The shunt (charging) admittance of each line is $j0.04$ pu in total, i.e. $j0.02$ pu at each end ($\pi$ model). Every bus has two lines connected:

$$\begin{gathered}Y_{ii} = 2\left(y + j0.02\right) = 4.0701 - j17.1798\ \text{pu}\\ Y_{12} = Y_{13} = Y_{23} = -y = -2.0351 + j8.6099\ \text{pu}\end{gathered}$$

$$Y_{bus} = \begin{bmatrix}4.0701 - j17.1798 & -2.0351 + j8.6099 & -2.0351 + j8.6099\\ -2.0351 + j8.6099 & 4.0701 - j17.1798 & -2.0351 + j8.6099\\ -2.0351 + j8.6099 & -2.0351 + j8.6099 & 4.0701 - j17.1798\end{bmatrix}\ \text{pu}$$

(If $j0.04$ is read as the charging at each end, replace $-j17.1798$ by $-j17.1398$ in every diagonal element.)

**(ii) Phase-shifting (tap-changing) transformer in line 2-3, $t = e^{j30^\circ}$** ($|t| = 1$: a pure phase shift). The transformer is in series with the line, on the bus-2 side, and carries the series admittance $y$. For a branch between $p$ (tap side) and $q$ with a complex ratio $t$:

$$\begin{gathered}Y_{pp} \mathrel{+}= \frac{y}{|t|^2} \\ Y_{pq} = -\frac{y}{t^*} \\ Y_{qp} = -\frac{y}{t} \\ Y_{qq} \mathrel{+}= y\end{gathered}$$

With $|t| = 1$ the diagonal elements do not change; only the 2-3 off-diagonals do:

$$Y_{23}' = -\frac{y}{t^*} = -y\,e^{j30^\circ} = -(2.0351 - j8.6099)(0.8660 + j0.5) = -6.0675 + j6.4389$$

$$Y_{32}' = -\frac{y}{t} = -y\,e^{-j30^\circ} = 2.5425 + j8.4737$$

$$Y_{bus}' = \begin{bmatrix}4.0701 - j17.1798 & -2.0351 + j8.6099 & -2.0351 + j8.6099\\ -2.0351 + j8.6099 & 4.0701 - j17.1798 & -6.0675 + j6.4389\\ -2.0351 + j8.6099 & 2.5425 + j8.4737 & 4.0701 - j17.1798\end{bmatrix}\ \text{pu}$$

The modified matrix is **no longer symmetric** ($Y_{23}' \ne Y_{32}'$) because of the phase shift; this is a general property of a phase-shifting transformer.

@s 2
**(a) Need for load flow (power flow) analysis.** It gives the steady-state operating condition of the network: the voltage magnitude and angle at every bus, the real and reactive power flow in every line and transformer, and the losses, for a specified generation and load. It is needed for:

1. **Planning** (new generators, lines, substations, capacitors) and the study of the future expansion;
2. **Operation:** checking the voltage profile and the line loadings (thermal limits), economic dispatch, and optimal power flow;
3. **Contingency (N-1) analysis:** the effect of the loss of a line or generator, the security assessment;
4. The initial condition for **stability** and **short-circuit** studies, and the loss calculation, tap and reactive-power compensation settings.

**Significance of the slack bus.**

- The system losses are not known until the load flow is solved, so one bus has to take the unknown **mismatch** of real and reactive power; this bus, the **slack (swing) bus**, supplies $P_{slack} = \sum P_{load} + P_{loss} - \sum P_{other\ gen}$.
- It has the specified $|V|$ and $\delta = 0$, which provides the **voltage and angle reference** for all other buses (only angle differences are physically meaningful).
- It is normally the **largest, most flexible generator**; it keeps the power balance, which is not possible if the $P$ and $Q$ of every bus were specified.
- There is only one slack bus in the system studied (exceptions: distributed slack).

**(b) Gauss-Seidel load flow.** $Y_{22} = 1/Z = 1/(j0.75) = -j1.3333$ pu, $Y_{21} = -Y_{22} = +j1.3333$ pu.

The net scheduled power injection at bus 2 is the capacitor generation minus the load:

$$S_2 = j1.0 - (0.5 + j1.0) = -0.5 + j0\ \text{pu}\quad\Rightarrow\ P_2 = -0.5,\ Q_2 = 0$$

The Gauss-Seidel update (bus 2 is the only unknown) is

$$V_2^{(k+1)} = \frac{1}{Y_{22}}\left[\frac{P_2 - jQ_2}{V_2^{(k)*}} - Y_{21}V_1\right] = 1 + \frac{-0.5}{(-j1.3333)\,V_2^{(k)*}} = 1 - \frac{j0.375}{V_2^{(k)*}}$$

Starting with $V_2^{(0)} = 1\angle0^\circ$:

| Iteration | $V_2$ (pu) | magnitude | angle |
|---|---|---|---|
| 1 | $1 - j0.375$ | 1.0680 | $-20.56^\circ$ |
| 2 | $0.8767 - j0.3288$ | 0.9363 | $-20.56^\circ$ |
| 3 | $0.8590 - j0.3772$ | 0.9376 | $-23.58^\circ$ |
| 4 | | 0.9165 | $-23.58^\circ$ |
| 5 | | 0.9166 | $-24.15^\circ$ |
| 6 | | 0.9125 | $-24.15^\circ$ |
| 7 | | 0.9125 | $-24.27^\circ$ |
| 10 | | 0.9115 | $-24.29^\circ$ |
| 20 | | 0.91144 | $-24.295^\circ$ |

The iterations converge slowly. The converged solution can be checked in closed form. With no net reactive power at bus 2, the line carries $P = \dfrac{V_1V_2\sin\delta}{X} = 0.5$ and $Q_{21} = 0 = \dfrac{V_2(V_1\cos\delta - V_2)}{X}$:

$$V_2 = \cos\delta\ \ \Rightarrow\ \ \sin\delta\cos\delta = \frac{0.5\times0.75}{1} = 0.375\ \Rightarrow\ \sin2\delta = 0.75,\ \ \delta = 24.295^\circ$$

$$\boxed{V_2 = 0.9114\angle{-24.30^\circ}\ \text{pu}}$$

(the other mathematical root, $\delta = 65.7^\circ$, $V_2 = 0.41$ pu, is the low-voltage, unstable solution).

**Power flow between buses 1 and 2.**

$$I_{12} = \frac{V_1 - V_2}{j0.75} = \frac{1 - (0.8307 - j0.3751)}{j0.75} = 0.5001 - j0.2257\ \text{pu}$$

$$\begin{gathered}S_{12} = V_1I_{12}^* = 0.5 + j0.2257\ \text{pu}\\ S_{21} = V_2I_{21}^* = -0.5 + j0.0\ \text{pu}\\ S_{loss} = S_{12} + S_{21} = j0.2257\ \text{pu}\end{gathered}$$

So **0.5 pu of real power and 0.226 pu of reactive power leave bus 1** towards bus 2; bus 2 receives 0.5 pu (all absorbed by the load) and no net reactive power (the capacitor supplies exactly the 1.0 pu of reactive load), and the line consumes $I^2X = 0.226$ pu of reactive power (it has no resistance, so no real loss). Real power flow is $0.5$ pu from 1 to 2.

@s 3
**(a) Significance of symmetrical components.** An unbalanced three-phase system of phasors (as in a fault, an open phase, or unbalanced loading) is hard to analyse directly because the mutual coupling between the phases makes the phase impedance matrix full. **Fortescue's theorem** says that any unbalanced set of three phasors can be resolved into three balanced sets:

- **positive sequence** (three equal phasors, $120^\circ$ apart, the same phase sequence abc),
- **negative sequence** (three equal phasors, $120^\circ$ apart, the opposite sequence acb),
- **zero sequence** (three equal phasors in phase).

For a balanced network the three sequence networks are **independent** (decoupled), each is a simple single-phase equivalent solved with its own impedance $Z_1$, $Z_2$, $Z_0$. Fault analysis (L-G, L-L, L-L-G, open conductors), the relay setting (negative and zero-sequence relays), the design of grounding, the transformer connections, and the effect of unbalance on the machines (negative-sequence heating) all use them.

**Derivation of the phasor voltages.** Let $a = 1\angle120^\circ = -\tfrac12 + j\tfrac{\sqrt3}{2}$ so that $a^2 = 1\angle240^\circ$, $a^3 = 1$, and $1 + a + a^2 = 0$. With the reference phase $a$:

$$\begin{gathered}V_a = V_{a0} + V_{a1} + V_{a2}\\ V_b = V_{b0} + V_{b1} + V_{b2} = V_{a0} + a^2V_{a1} + aV_{a2}\\ V_c = V_{c0} + V_{c1} + V_{c2} = V_{a0} + aV_{a1} + a^2V_{a2}\end{gathered}$$

because in the positive sequence $V_{b1} = a^2V_{a1}$, $V_{c1} = aV_{a1}$, in the negative sequence $V_{b2} = aV_{a2}$, $V_{c2} = a^2V_{a2}$, and in the zero sequence all three are equal. In matrix form:

$$\begin{bmatrix}V_a\\ V_b\\ V_c\end{bmatrix} = \begin{bmatrix}1&1&1\\ 1&a^2&a\\ 1&a&a^2\end{bmatrix}\begin{bmatrix}V_{a0}\\ V_{a1}\\ V_{a2}\end{bmatrix} = [A]\,\begin{bmatrix}V_{a0}\\ V_{a1}\\ V_{a2}\end{bmatrix}$$

The inverse transformation, found with $[A]^{-1} = \tfrac13[A]^*$ (using $1 + a + a^2 = 0$), gives the components:

$$\begin{gathered}V_{a0} = \tfrac13(V_a + V_b + V_c) \\ V_{a1} = \tfrac13(V_a + aV_b + a^2V_c) \\ V_{a2} = \tfrac13(V_a + a^2V_b + aV_c)\end{gathered}$$

**(b) Three-phase fault at the generator terminals.** Base: $S_b = 50$ MVA; $V_b = 11$ kV (generator), 132 kV (line), 6.6 kV (motor). $Z_{b,line} = 132^2/50 = 348.48\ \Omega$.

| Element | Per-unit reactance on the common base |
|---|---|
| Generator | $0.10$ (50 MVA, 11 kV, same base) |
| T1 (100 MVA) | $0.05\times\dfrac{50}{100} = 0.025$ |
| Line j25 Ω | $\dfrac{25}{348.48} = 0.0717$ |
| T2 (50 MVA, 132/6.6 kV) | $0.04$ |
| Motor (50 MVA, 6.6 kV) | $0.06$ |

The motor branch seen from the generator terminal (through T2, line, T1):

$$X_{m} = 0.06 + 0.04 + 0.0717 + 0.025 = 0.1967\ \text{pu}$$

The Thevenin reactance at the generator terminals is the generator in parallel with the motor branch (both are sources of emf $= 1$ pu):

$$X_{th} = \frac{0.10\times0.1967}{0.10 + 0.1967} = 0.0663\ \text{pu}$$

$$\begin{gathered}I_f = \frac{V_f}{X_{th}} = \frac{1}{0.0663} = 15.08\ \text{pu} \\ I_{base} = \frac{50\times10^6}{\sqrt3\times11\times10^3} = 2624.3\ \text{A}\end{gathered}$$

$$\boxed{I_f = 15.08\times2624.3 \approx 39.58\ \text{kA}}$$

$$\boxed{\text{Fault MVA} = S_b\times\frac{1}{X_{th}} = 50\times15.08 \approx 754\ \text{MVA}}$$

*Contributions:* generator $1/0.10 = 10$ pu = 26.2 kA; motor $1/0.1967 = 5.08$ pu = 13.3 kA at 11 kV (the motor feeds the fault through T2, the line and T1).

@s 4
**(a) Double line-to-ground (L-L-G) fault at the alternator terminals.** Phases b and c are short-circuited and connected to ground, phase a is open. With a bolted fault ($Z_f = 0$):

$$\begin{gathered}I_a = 0 \\ V_b = V_c = 0\end{gathered}$$

*Voltages:* $V_{a0} = \tfrac13(V_a + V_b + V_c) = \tfrac13V_a$; $V_{a1} = \tfrac13(V_a + aV_b + a^2V_c) = \tfrac13V_a$; $V_{a2} = \tfrac13(V_a + a^2V_b + aV_c) = \tfrac13V_a$:

$$\boxed{V_{a0} = V_{a1} = V_{a2}}$$

*Currents:* $I_{a0} + I_{a1} + I_{a2} = I_a = 0$.

The generator sequence relations are $V_{a1} = E_a - I_{a1}Z_1$, $V_{a2} = -I_{a2}Z_2$, $V_{a0} = -I_{a0}Z_0$. The three conditions ($V_{a0} = V_{a1} = V_{a2}$ and $\sum I = 0$) are satisfied by **connecting the three sequence networks in parallel**:

$$\boxed{I_{a1} = \frac{E_a}{Z_1 + \dfrac{Z_2Z_0}{Z_2 + Z_0}}}$$

$$\begin{gathered}I_{a2} = -I_{a1}\frac{Z_0}{Z_2 + Z_0} \\ I_{a0} = -I_{a1}\frac{Z_2}{Z_2 + Z_0} \\ V_{a1} = V_{a2} = V_{a0} = E_a - I_{a1}Z_1\end{gathered}$$

The current flowing into the ground is $I_g = I_b + I_c = 3I_{a0}$ and the fault phase currents are $I_b = I_{a0} + a^2I_{a1} + aI_{a2}$, $I_c = I_{a0} + aI_{a1} + a^2I_{a2}$. (With a fault impedance $Z_f$ to ground, add $3Z_f$ in series with $Z_0$.)

```figure caption="Question 4(a): sequence networks for the double line-to-ground fault: positive network in series with the parallel combination of the negative and zero networks."
fig,ax=plt.subplots(figsize=(6.2,3.0)); ax.axis('off'); ax.set_xlim(-0.3,12); ax.set_ylim(-0.3,5.2)
vsrc(ax,(0,0.3),(0,3.7),'$E_a$',side=-1,off=0.8)
wire(ax,[(0,3.7),(0.7,3.7)]); res(ax,(0.7,3.7),(2.9,3.7),'$Z_1$',side=1,body=1.0); wire(ax,[(2.9,3.7),(4.6,3.7)]); node(ax,(4.6,3.7))
wire(ax,[(4.6,3.7),(4.6,3.3)]); res(ax,(4.6,3.3),(4.6,1.3),'$Z_2$',side=1,body=1.0); wire(ax,[(4.6,1.3),(4.6,0.3)])
wire(ax,[(4.6,3.7),(7.6,3.7)]); wire(ax,[(7.6,3.7),(7.6,3.3)]); res(ax,(7.6,3.3),(7.6,1.3),'$Z_0$',side=1,body=1.0); wire(ax,[(7.6,1.3),(7.6,0.3)]); node(ax,(7.6,3.7))
wire(ax,[(0,0.3),(7.6,0.3)]); node(ax,(4.6,0.3))
arrow(ax,(1.0,4.35),(2.3,4.35),'$I_{a1}$',off=0.2); arrow(ax,(5.0,2.9),(5.0,2.2),'$I_{a2}$',off=0.3); arrow(ax,(8.0,2.9),(8.0,2.2),'$I_{a0}$',off=0.3)
ax.text(9.0,2.3,'$V_{a1}=V_{a2}=V_{a0}$',fontsize=8.5)
```

**(b) Sequence reactances of the alternator.** Base: 50 MVA, 12 kV: $I_{base} = \dfrac{50\times10^6}{\sqrt3\times12\times10^3} = 2405.6$ A; $Z_{base} = 12^2/50 = 2.88\ \Omega$. The pre-fault emf is $E = 1$ pu, resistance neglected, bolted faults, solidly grounded neutral ($Z_n = 0$).

**(i) Three-phase fault:** only the positive sequence is involved: $I_f = E/X_1$.

$$I_f = \frac{1870}{2405.6} = 0.7774\ \text{pu}\ \Rightarrow\ X_1 = \frac{1}{0.7774} = \mathbf{1.2864\ pu}\ (3.705\ \Omega)$$

**(ii) L-L fault:** $I_f = \dfrac{\sqrt3E}{X_1 + X_2}$.

$$I_f = \frac{2590}{2405.6} = 1.0767\ \text{pu}\ \Rightarrow\ X_1 + X_2 = \frac{\sqrt3}{1.0767} = 1.6086\ \text{pu}$$

$$X_2 = 1.6086 - 1.2864 = \mathbf{0.3223\ pu}\ (0.928\ \Omega)$$

**(iii) L-G fault:** $I_f = 3I_{a1} = \dfrac{3E}{X_1 + X_2 + X_0}$.

$$I_f = \frac{4130}{2405.6} = 1.7168\ \text{pu}\ \Rightarrow\ X_1 + X_2 + X_0 = \frac{3}{1.7168} = 1.7474\ \text{pu}$$

$$X_0 = 1.7474 - 1.6086 = \mathbf{0.1387\ pu}\ (0.399\ \Omega)$$

$$\boxed{X_1 = 1.286\ \text{pu},\qquad X_2 = 0.322\ \text{pu},\qquad X_0 = 0.139\ \text{pu}}$$

*Check:* L-L: $\sqrt3/(1.2864 + 0.3223) = 1.0767$ pu = 2590 A ✓; L-G: $3/(1.2864 + 0.3223 + 0.1387) = 1.7168$ pu = 4130 A ✓. (The ordering $X_1 > X_2 > X_0$ is typical of the machine with the synchronous or transient reactance as the positive sequence reactance; if the three-phase fault current were the sub-transient value, it would give a smaller $X_1$ than $X_2$.)

@s 5
**(a) Stability definitions**

- **Steady-state stability:** the ability of the power system to **remain in synchronism** after **small, gradual disturbances** (slow load changes or small variations in excitation or the generator output), the operating point moving slowly. It is studied with the linearised swing equation; the limit is $P_{max} = \dfrac{EV}{X}$ at $\delta = 90^\circ$ ($P_s = dP/d\delta > 0$).
- **Transient stability:** the ability of the system to **remain in synchronism after a large, sudden disturbance** (a short circuit, loss of a generator or a heavily loaded line, sudden load change or switching) during the first swing (about 1 s). It needs the non-linear swing equation (equal-area criterion, step-by-step numerical solution).

**Methods of improving transient stability**

1. **Fast fault clearing:** high-speed relays and circuit breakers (2 to 3 cycles), which reduces the accelerating area.
2. **Auto-reclosing** (single-pole) of the circuit breakers on transient faults.
3. **Reducing the transfer reactance:** parallel lines (double circuit), series compensation (capacitors), and a lower transformer and generator reactance.
4. **High-speed, high-gain excitation system and AVR** (and power-system stabiliser), which raises the internal emf during the fault.
5. **Fast valving / turbine fast-closing** and a lower mechanical input during the disturbance; **dynamic (braking) resistors** which add the electrical load during the swing.
6. A larger inertia constant $H$ (heavier rotor), generator tripping or load shedding, **HVDC / FACTS** (TCSC, SVC, STATCOM), and a higher transmission voltage.

**(b) Equivalent swing equation for coherent machines.** For one machine on its own base $S_i$, with $H_i = $ (stored kinetic energy at rated speed)/$S_i$:

$$\frac{2H_i}{\omega_s}\frac{d^2\delta_i}{dt^2} = P_{mi} - P_{ei}\quad\text{(pu on } S_i)$$

Multiply by $S_i$ to get the equation in MW:

$$\frac{2H_iS_i}{\omega_s}\frac{d^2\delta_i}{dt^2} = P_{mi}' - P_{ei}'\quad(\text{MW})$$

If all machines swing together (coherent: $\delta_1 = \delta_2 = \dots = \delta_n = \delta$) add the equations:

$$\frac{2}{\omega_s}\left(\sum_{i=1}^nH_iS_i\right)\frac{d^2\delta}{dt^2} = \sum_i P_{mi}' - \sum_i P_{ei}' = P_m' - P_e'$$

Dividing by a common base $S_B$:

$$\begin{gathered}\frac{2H_{eq}}{\omega_s}\frac{d^2\delta}{dt^2} = P_m - P_e\quad(\text{pu on } S_B) \\ \boxed{H_{eq} = \frac{\sum_iH_iS_i}{S_B} = H_1\frac{S_1}{S_B} + H_2\frac{S_2}{S_B} + \dots}\end{gathered}$$

The group behaves as a single machine of rating $S_B$ with inertia constant $H_{eq}$.

**Numerical.**

$$\begin{gathered}H_1S_1 = 6\times50 = 300\ \text{MJ},\quad H_2S_2 = 6\times100 = 600\ \text{MJ},\quad H_3S_3 = 6\times200 = 1200\ \text{MJ}\\ \sum H_iS_i = 2100\ \text{MJ}\end{gathered}$$

$$\boxed{H_{eq} = \frac{2100}{100} = 21\ \text{MJ/MVA (on a 100 MVA base)}}$$

(Equivalently the combined rating is 350 MVA with $H = 6$ MJ/MVA, so on a 100 MVA base $H_{eq} = 6\times350/100 = 21$ MJ/MVA.)

---
file: NEBians-IOE-Past-Paper-Electrical-Machine-I-ENEE202-2082-Kartik.pdf
subject: Electrical Machine I
level: BE · Year II / Part I
code: ENEE 202
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
A cast steel magnetic structure made of a bar of section 2 cm × 2 cm is shown in figure. Determine the current that the 500 turns magnetizing coil on the left limb should carry so that a flux of 2 mWb is produced in the right limb. Take $\mu_r = 600$ and neglect leakage. [[6]]

Figure: a two-window core. The coil (500 turns) is on the left limb; the centre limb B (window height 15 cm) is shared by both windows; the right limb is C. Each window is 25 cm wide and 15 cm high (mean path lengths); the fluxes are Φ (left limb), Φ$_1$ (centre limb) and Φ$_2$ (right limb).

@q 2
During open circuit and short circuit test of a 2200/110 V, 40 kVA transformer, following results were obtained. The meters for open circuit test were placed on LV side and for short circuit test on HV side. [[6]]

Open circuit: P = 320 W, I = 8.4 A, V = 110 V. Short circuit: P = 650 W, I = 18.2 A, V = 85 V. Determine:

(i) R$_0$ and X$_0$

(ii) The efficiency at full load with pf 0.85 lag

(iii) The approx. voltage regulation

@q 3
Why do we need to connect transformers in parallel? Also explain the conditions that need to be fulfilled for parallel operation of transformers with detailed explanation for operation. [[2+4]]

@q 4
Explain the principle of Sumpner's test. Why is it necessary to use two identical transformer in Sumpner's test? [[3+3]]

@q 5
Why DC shunt generator shall not be started at load? Explain the voltage build-up process of a DC shunt generator. [[2+4]]

@q 6
The armature and field resistances of a 200 V DC shunt motor are 0.12 Ω and 250 Ω respectively. The rotational loss of the motor is 250 W. The full load line current is 10 A and motor rpm is 1500. Determine; [[6]]

(i) The mechanical power developed.

(ii) The power output

(iii) The load torque

(iv) The full load efficiency

@q 7
Explain the need of starter in a DC motor and describe the working principle of 4 point starter with a neat sketch. [[6]]

@q 8
Explain the construction and working principle of 3-phase induction motor. [[6]]

@q 9
A 4 pole, 3 phase, 50 Hz, 1440 rpm induction motor is drawing 35 kW. The stator and friction losses are 1 kW and 1.5 kW respectively. Find, [[6]]

(i) rotor copper losses

(ii) efficiency of motor

@q 10
Explain why do we need a starter to start an induction motor? Also explain different methods of induction motor starting. [[6]]

<!-- SOLUTIONS -->

@s 1
**Magnetic circuit.** Cross-section $A = 2 \times 2 = 4\ \text{cm}^2 = 4\times10^{-4}\ \text{m}^2$, $\mu = \mu_0\mu_r = 4\pi\times10^{-7}\times600 = 7.54\times10^{-4}$ H/m. The coil on the left limb sets up flux $\Phi$ which divides at the top junction into the centre limb ($\Phi_1$) and the right limb ($\Phi_2$): the centre limb and the right path are in **parallel**, and this parallel combination is in series with the left limb.

*Mean lengths* (from the dashed paths of the figure): centre limb $l_B = 15$ cm; right path $l_C = 25 + 15 + 25 = 65$ cm; left path $l_L = 25 + 15 + 25 = 65$ cm.

*Right limb* ($\Phi_2 = 2$ mWb):

$$\begin{gathered}B_2 = \frac{2\times10^{-3}}{4\times10^{-4}} = 5.0\ \text{T} \\ H_2 = \frac{B_2}{\mu} = \frac{5.0}{7.54\times10^{-4}} = 6631\ \text{A/m}\end{gathered}$$

$$\text{mmf drop across the right path} = H_2 l_C = 6631 \times 0.65 = 4310\ \text{AT}$$

*Centre limb* (same mmf drop, since it is in parallel between the same two nodes):

$$\begin{gathered}H_B = \frac{4310}{0.15} = 28\,736\ \text{A/m} \\ B_B = \mu H_B = 21.67\ \text{T} \\ \Phi_1 = B_BA = 8.667\ \text{mWb}\end{gathered}$$

*Total flux in the left limb:*

$$\begin{gathered}\Phi = \Phi_1 + \Phi_2 = 8.667 + 2 = 10.667\ \text{mWb} \\ B_L = \frac{10.667\times10^{-3}}{4\times10^{-4}} = 26.67\ \text{T}\end{gathered}$$

$$\begin{gathered}H_L = \frac{26.67}{7.54\times10^{-4}} = 35\,368\ \text{A/m} \\ \text{mmf}_L = H_Ll_L = 35\,368\times0.65 = 22\,989\ \text{AT}\end{gathered}$$

*Total mmf and current:*

$$NI = 22\,989 + 4\,310 = 27\,299\ \text{AT} \quad\Rightarrow\quad I = \frac{27\,299}{500} = \mathbf{54.6\ A}$$

*Reluctance check:* $S = l/(\mu A)$: $S_L = S_C = 2.155\times10^6$, $S_B = 0.497\times10^6$ AT/Wb; $S_{B\parallel C} = 0.404\times10^6$; $\Phi = NI/(S_L + S_{B\parallel C}) = 27\,299/2.56\times10^6 = 10.67$ mWb, the same.

(The flux densities are far above the saturation of cast steel (about 1.5 to 2 T); the question explicitly gives a constant $\mu_r = 600$, so the linear result is the expected answer. A real B-H curve would need an even larger current.)

```figure caption="Question 1: magnetic equivalent circuit: the mmf NI drives the left limb reluctance S_L in series with the parallel pair S_B (centre limb) and S_C (right limb)."
fig,ax=ckt_canvas(6.2,3.0)
vsrc(ax,(0,0),(0,2.6),"NI",side=-1,off=0.9)
wire(ax,[(0,2.6),(0.7,2.6)]); res(ax,(0.7,2.6),(2.7,2.6),"S$_L$",side=1,body=1.0); wire(ax,[(2.7,2.6),(7.2,2.6)])
node(ax,(4.2,2.6)); node(ax,(6.6,2.6))
res(ax,(4.2,2.6),(4.2,0),"S$_B$",side=1,body=1.2); res(ax,(6.6,2.6),(6.6,0),"S$_C$",side=1,body=1.2)
wire(ax,[(0,0),(6.6,0)])
arrow(ax,(1.2,3.25),(2.2,3.25),"$\\Phi$"); arrow(ax,(4.6,1.6),(4.6,0.8),"$\\Phi_1$",off=0.3); arrow(ax,(7.0,1.6),(7.0,0.8),"$\\Phi_2$",off=0.3)
```

@s 2
**Transformer 2200/110 V, 40 kVA** (turns ratio $a = 20$); rated HV current $I_1 = 40\,000/2200 = 18.18$ A.

**(i) $R_0$ and $X_0$** (open-circuit test on the LV side, so these are LV-side values):

$$\begin{gathered}\cos\varphi_0 = \frac{P_0}{V_0I_0} = \frac{320}{110\times8.4} = 0.3463 \\ \varphi_0 = 69.74^\circ\end{gathered}$$

$$\begin{gathered}I_c = I_0\cos\varphi_0 = \frac{320}{110} = 2.909\ \text{A} \\ I_m = I_0\sin\varphi_0 = \sqrt{8.4^2 - 2.909^2} = 7.880\ \text{A}\end{gathered}$$

$$\begin{gathered}R_0 = \frac{V_0}{I_c} = \frac{110}{2.909} = \mathbf{37.8\ \Omega} \\ X_0 = \frac{V_0}{I_m} = \frac{110}{7.880} = \mathbf{13.96\ \Omega}\quad\text{(LV side)}\end{gathered}$$

Referred to the HV side (multiply by $a^2 = 400$): $R_0' = 15.1\ \text{k}\Omega$, $X_0' = 5.58\ \text{k}\Omega$.

*Short-circuit test (HV side):* $I_{sc} = 18.2\ \text{A}$ (almost exactly the rated 18.18 A), so $650$ W is the full-load copper loss.

$$\begin{gathered}R_{e1} = \frac{W_{sc}}{I_{sc}^2} = \frac{650}{18.2^2} = 1.962\ \Omega \\ Z_{e1} = \frac{V_{sc}}{I_{sc}} = \frac{85}{18.2} = 4.670\ \Omega \\ X_{e1} = \sqrt{Z_{e1}^2 - R_{e1}^2} = 4.238\ \Omega\end{gathered}$$

**(ii) Efficiency at full load, 0.85 pf lagging:**

$$\begin{gathered}\text{Output} = 40\,000 \times 0.85 = 34\,000\ \text{W} \\ P_i = 320\ \text{W} \\ P_{cu} = 650\ \text{W}\end{gathered}$$

$$\eta = \frac{34\,000}{34\,000 + 320 + 650} = \frac{34\,000}{34\,970} = 0.9723 = \mathbf{97.2\,\%}$$

(Maximum efficiency occurs at $\sqrt{320/650} = 0.70$ of full load, i.e. at 28.1 kVA.)

**(iii) Approximate voltage regulation** (HV side, lagging pf: $\cos\varphi = 0.85$, $\sin\varphi = 0.527$):

$$\%\text{VR} \approx \frac{I_1\left(R_{e1}\cos\varphi + X_{e1}\sin\varphi\right)}{V_1}\times100 = \frac{18.18\,(1.962\times0.85 + 4.238\times0.527)}{2200}\times100$$

$$= \frac{18.18 \times 3.901}{2200}\times100 = \mathbf{3.22\,\%}$$

@s 3
**Why transformers are operated in parallel.**

1. **Load growth:** when the load exceeds the rating of the existing transformer, a second unit is added instead of replacing it.
2. **Reliability and continuity:** if one unit fails or is taken off for maintenance, the other continues to supply (at least the essential load).
3. **Efficiency:** at light load one unit is switched off, so the other runs near its full-load (maximum-efficiency) point.
4. **Standardisation, transport and spare:** a station with several smaller units is cheaper to transport and to keep spares for.

**Conditions for satisfactory parallel operation.**

| Condition | Explanation | Consequence if not satisfied |
|---|---|---|
| 1. Same **polarity** | Terminals of the same instantaneous polarity are joined (primary to primary, secondary to secondary) | Short circuit through the secondaries when joined |
| 2. Same **voltage ratio** (and rated voltages) | Open-circuit secondary emfs equal | A circulating current $I_c = (E_{2A} - E_{2B})/(Z_A + Z_B)$ flows even at no load, causing loss and heating |
| 3. Same **per-unit (percentage) impedance** | Load sharing is $S_A/S_B = (S_{rA}/S_{rB})\times(z_B/z_A)$, so the one with the smaller p.u. impedance takes the larger share relative to its rating | One transformer overloads while the other is under-loaded |
| 4. Same **ratio of $X/R$** (same impedance angle) | Currents of the two transformers are then in phase | The two currents are out of phase, the total is less than the arithmetic sum, so the capacity is wasted and the power factors at which they work differ |
| 5. Same **phase sequence** (3-phase) | Secondary phase rotation $a$-$b$-$c$ identical | Phase-to-phase short circuit |
| 6. Same **phase displacement** (vector group, e.g. Dy11 with Dy11, not with Yy0) | Secondary line voltages in phase | Large circulating current, as in condition 2 |

*Operation.* The primaries are connected to the same bus; the secondaries are connected to the same load bus through their circuit breakers, after checking polarity and phase (for example with a voltmeter or synchroscope across the open switch, which must read zero). On load, the two transformers share the common terminal voltage; their currents satisfy $I_AZ_A = I_BZ_B$ with $I_A + I_B = I_L$, so

$$\begin{gathered}I_A = I_L\frac{Z_B}{Z_A + Z_B} \\ I_B = I_L\frac{Z_A}{Z_A + Z_B}\end{gathered}$$

The loads add vectorially, and the combined rating is the sum of the ratings only if the p.u. impedances are equal.

@s 4
**Principle of Sumpner's (back-to-back) test.** It is a heat-run test on two *identical* transformers which gives the **full-load temperature rise and the iron and copper losses** at the same time while the supply has to give only the losses (not the full load power).

*Connections.* The primaries of the two transformers are connected in parallel across the rated supply voltage $V_1$: the cores are magnetised at rated flux, so the wattmeter $W_1$ reads the sum of the two iron losses $2P_i$. The secondaries are connected in **series opposition**, so that the net emf round the closed secondary loop is zero (check with a voltmeter before closing it, which should read zero; otherwise reverse one secondary). A second, low-voltage supply $V_2$ (through a regulating transformer) is injected in the secondary loop and adjusted so that rated current $I_2$ circulates; the wattmeter $W_2$ reads the sum of the two full-load copper losses $2P_{cu}$. Hence

$$\begin{gathered}W_1 = 2P_i \\ W_2 = 2P_{cu} \\ \Rightarrow \\ \text{total loss at full load} = W_1 + W_2\end{gathered}$$

and the transformers are in the same thermal state as under full load, although the line supply provides only $W_1 + W_2$, a small fraction of the rating.

```figure caption="Question 4: Sumpner's test. The primaries are in parallel on the rated supply V1 (W1 reads 2 x iron loss); the secondaries are in series opposition and carry the rated current from the injected voltage V2 (W2 reads 2 x full-load copper loss)."
fig,ax=plt.subplots(figsize=(6.2,3.2))
def box(x,y,w,h,t): ax.add_patch(Rectangle((x,y),w,h,fc="#eaf1fb",ec=ACCENT,lw=1.4,zorder=2)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=9,zorder=3)
def L(xs,ys): ax.plot(xs,ys,color=INK,lw=1.4,zorder=1)
def meter(x,y,t,c): ax.add_patch(Circle((x,y),0.28,fc="white",ec=c,lw=1.4,zorder=3)); ax.text(x,y,t,ha="center",va="center",fontsize=8,zorder=4)
box(2.2,2.1,1.4,0.9,"T$_1$"); box(2.2,0.4,1.4,0.9,"T$_2$")
L([1.1,1.1,2.2],[1.95,2.8,2.8]); L([1.1,1.1,2.2],[1.95,1.1,1.1])
L([1.6,1.6,2.2],[0.2,2.3,2.3]); L([1.6,2.2],[0.6,0.6])
L([0.35,0.35,1.1],[1.4,1.95,1.95]); L([0.35,0.35,1.6],[0.8,0.2,0.2])
meter(0.35,1.1,"V$_1$",ACCENT); meter(0.75,1.95,"W$_1$",SERIES[1])
L([3.6,5.4,5.4,3.6],[2.8,2.8,1.1,1.1]); L([3.6,4.3,4.3,3.6],[2.3,2.3,0.6,0.6])
meter(5.4,2.3,"W$_2$",SERIES[1]); meter(5.4,1.55,"V$_2$",ACCENT)
ax.text(0.35,0.4,"rated\nsupply",ha="center",fontsize=8,color=INK)
ax.text(5.75,2.0,"series opposition\n(net emf = 0),\nI$_2$ = rated",fontsize=8,color=MUTED)
ax.set_xlim(-0.2,7.6); ax.set_ylim(0.0,3.2); ax.set_aspect("equal"); ax.axis("off")
```

*Why two identical transformers are needed.*

1. The secondaries are connected in series **opposition** and the test needs the emfs to cancel exactly: only transformers of the **same ratio, polarity and rating** make the loop emf zero, so that a small injected voltage circulates the full-load current.
2. The two units carry equal iron loss and equal copper loss, so each loss is exactly half of the wattmeter reading ($W_1/2$ and $W_2/2$). With different transformers the readings could not be split correctly and the circulating current would flow at no load.
3. Identical units reach the same temperature, so the heat-run result is meaningful for each of them.

Advantages: only the losses are supplied from the line, the temperature rise is obtained under practically full-load conditions, and the efficiency at any load can be computed from the separate loss values.

@s 5
**Why a DC shunt generator should not be started on load.** The generator builds up its own voltage from the residual flux, through its field current $I_f = V/R_f$ taken from its own terminals. If a load is connected during the build-up:

1. The load (and armature) current produces an armature-resistance drop and armature reaction, which lower the terminal voltage, so the field current, and hence the flux, cannot rise: the voltage **fails to build up** (or settles at a very low value).
2. With a heavy load of low resistance across the terminals, the voltage at which the field and load share the generated emf collapses; the machine may also overheat because of the heavy current with a small emf.

Therefore the generator is started with the load switch open (and the field regulator rheostat short-circuited to give maximum field current), the voltage is built up to the rated value, and then the load is applied.

**Voltage build-up process.**

1. Because of **residual magnetism** in the poles, the armature, when driven at rated speed, generates a small emf $E_r$ (about 2 to 5 % of rated), which appears across the field winding.
2. This voltage drives a small field current $I_f$ through the field circuit. If the field winding is connected so that this current **aids** the residual flux, the flux, and so $E_g = k\Phi\omega$, increases.
3. The larger emf drives more field current, which gives more flux and still more emf: the voltage rises cumulatively along the open-circuit characteristic (OCC).
4. The build-up stops at the point of intersection of the OCC with the **field-resistance line** $V = I_fR_f$ (a straight line through the origin of slope $R_f$), because there the emf generated is exactly the voltage needed to drive the field current; this is the no-load terminal voltage.

*Conditions for build-up:* (a) residual flux must be present (otherwise flash the field from a battery), (b) the field connections must be such that the field current strengthens the residual flux (otherwise reverse the field terminals or the direction of rotation), (c) the field circuit resistance must be **less than the critical resistance** (the slope of the tangent to the initial straight part of the OCC), and (d) the speed must be above the critical speed. If $R_f$ exceeds the critical value, the line intersects the OCC near the origin and the voltage hardly builds up.

```figure caption="Question 5: build-up of the voltage of a DC shunt generator: the generated emf follows the open-circuit characteristic (OCC) until it meets the field-resistance line; for a field resistance above the critical value the line meets the OCC close to the origin."
fig,ax=plt.subplots(figsize=(5.4,3.0))
i=np.linspace(0,2.6,300); E=8+250*np.tanh(i/1.0)*(0.92)
ax.plot(i,E,color=ACCENT,lw=2,label="OCC (with residual emf)")
ax.plot(i,115*i,color=SERIES[2],lw=1.6,label="R$_f$ < critical")
ax.plot(i,np.minimum(230*i,260),color=SERIES[3],lw=1.6,ls="--",label="R$_f$ = critical")
ax.plot(i,np.minimum(330*i,260),color=SERIES[1],lw=1.6,label="R$_f$ > critical")
ax.plot([0],[8],"o",color=INK,ms=4); ax.text(0.05,22,"residual emf",fontsize=7.5)
ax.annotate("no-load voltage",xy=(1.55,178),xytext=(1.7,60),fontsize=8,arrowprops=dict(arrowstyle="->",color=MUTED))
ax.set_xlim(0,2.6); ax.set_ylim(0,260); ax.set_xlabel("field current I$_f$ (A)",fontsize=8.5); ax.set_ylabel("E$_g$ , V (V)",fontsize=8.5); ax.legend(fontsize=7.5,loc="lower right"); ax.tick_params(labelsize=8); ax.grid(color=GRID,lw=0.6)
```

@s 6
**200 V DC shunt motor.** $R_a = 0.12\ \Omega$, $R_f = 250\ \Omega$, rotational loss $250$ W, $I_L = 10$ A, $N = 1500$ rpm.

$$\begin{gathered}I_f = \frac{200}{250} = 0.8\ \text{A} \\ I_a = I_L - I_f = 10 - 0.8 = 9.2\ \text{A}\end{gathered}$$

$$E_b = V - I_aR_a = 200 - 9.2\times0.12 = 198.90\ \text{V}$$

**(i) Mechanical power developed** (armature power):

$$P_m = E_bI_a = 198.90 \times 9.2 = \mathbf{1829.8\ W}$$

**(ii) Power output** (shaft power = developed power minus rotational loss):

$$P_{out} = 1829.8 - 250 = \mathbf{1579.8\ W} = 2.12\ \text{hp}$$

**(iii) Load (shaft) torque:**

$$\begin{gathered}\omega = \frac{2\pi \times 1500}{60} = 157.08\ \text{rad/s} \\ T_{load} = \frac{P_{out}}{\omega} = \frac{1579.8}{157.08} = \mathbf{10.06\ N\,m}\end{gathered}$$

(the gross developed torque is $P_m/\omega = 11.65$ N m).

**(iv) Full-load efficiency:**

$$\begin{gathered}P_{in} = VI_L = 200 \times 10 = 2000\ \text{W} \\ \eta = \frac{1579.8}{2000} = 0.790 = \mathbf{79.0\,\%}\end{gathered}$$

Check of losses: field $200 \times 0.8 = 160$ W, armature copper $9.2^2\times0.12 = 10.16$ W, rotational $250$ W; $2000 - 160 - 10.16 - 250 = 1579.8$ W. ✓

@s 7
**Need of a starter.** At the instant of starting the speed is zero, so the back emf $E_b = k\Phi\omega = 0$ and the armature current is limited only by $R_a$:

$$I_{a,start} = \frac{V}{R_a}$$

Since $R_a$ is very small (for example 0.12 Ω at 200 V gives 1667 A, or about 180 times the full-load current), this would burn the armature and commutator, produce a very large torque and shock, and cause a heavy voltage dip on the supply. A **starter** inserts an external resistance in series with the armature at starting, limiting the current to 1.5 to 2 times the rated current, and cuts it out in steps as the motor speeds up and $E_b$ builds up. It also provides **no-voltage** and **overload** protection.

**Four-point starter.** The starter has four terminals: **L** (line), **A** (armature), **F** (field) and a fourth terminal for the no-volt coil. The starting resistance is divided into sections connected to studs, and the handle (arm) carries a soft-iron piece and a return spring.

*Working.*

1. With the arm at the OFF position, the main switch is closed. The arm is slowly moved to the first stud: the line current flows through the arm and the **whole starting resistance** into the armature, while the shunt field gets its **full line voltage** (through the brass arc, not through the starting resistance, which is why the field current is not weakened as the arm moves: the main advantage over the 3-point starter).
2. The no-volt release coil (NVC) is connected in series with a protective resistance across the line (through the fourth terminal, independent of the field current) and magnetises. When the arm reaches the ON (last) stud, it is held there by the electromagnet pulling the soft-iron piece of the arm.
3. As the motor speeds up, the back emf rises, and the arm is moved step by step, cutting out the resistance, until all of it is out and the armature is at full voltage.
4. **No-volt protection:** if the supply fails, the NVC is demagnetised and the spring returns the arm to OFF; the motor cannot restart with all the resistance cut out. Because the NVC current does not depend on the field current, the coil does not release if the field is weakened or lost, either (a defect of the 3-point starter).
5. **Overload protection:** an overload release (an electromagnet in the line) lifts a short-circuiting bar across the NVC when the current exceeds a set value, so the NVC loses its hold and the arm returns to OFF.

```figure caption="Question 7: schematic of a DC shunt motor four-point starter. The field branch (F) and the no-volt coil branch (NVC with its protective resistor) are connected across the line independently of the starting resistance R_st, which is in series with the armature only."
fig,ax=ckt_canvas(6.4,3.0)
wire(ax,[(0.2,3.2),(9.4,3.2)]); wire(ax,[(0.2,0),(9.4,0)])
label(ax,(-0.2,3.2),"L+",size=8.5); label(ax,(-0.2,0),"L$-$",size=8.5)
node(ax,(2.0,3.2)); node(ax,(3.0,3.2))
ind(ax,(2.0,3.2),(2.0,0),"F (field)",side=-1,body=1.6,off=0.75)
ind(ax,(3.0,3.2),(3.0,1.7),"NVC",side=1,body=0.9,off=0.55); res(ax,(3.0,1.7),(3.0,0),"R$_p$",side=1,body=0.9,off=0.45)
res(ax,(3.6,3.2),(5.6,3.2),"R$_{st}$",side=1,body=1.4)
ax.add_patch(Circle((7.4,1.6),0.5,fc="white",ec=INK,lw=1.5)); label(ax,(7.4,1.6),"M",size=9)
wire(ax,[(5.6,3.2),(7.4,3.2),(7.4,2.1)]); wire(ax,[(7.4,1.1),(7.4,0)])
node(ax,(2.0,0)); node(ax,(3.0,0)); label(ax,(7.4,2.65),"A",size=8); label(ax,(6.5,2.0),"armature",size=7.5,color="#5b6472")
label(ax,(1.1,3.7),"handle / arm",size=7.5,color="#5b6472")
```

@s 8
**Construction of a 3-phase induction motor.**

*Stator:* the stationary part has (i) a **frame** (cast iron or steel, with end-shields and bearings), (ii) a **core** of laminated silicon steel punched with slots on the inner periphery (to reduce eddy-current loss), and (iii) a **three-phase winding** (distributed, double layer, wound for $p$ poles, placed in the slots and displaced $120^\circ$ electrical).

*Rotor:* separated from the stator by a small air gap (0.3 to 1 mm); a laminated cylindrical core with slots, in one of two types:

| Squirrel-cage rotor | Wound (slip-ring) rotor |
|---|---|
| Aluminium or copper bars in the slots, short-circuited by end-rings (a cage) | A 3-phase winding (star) with the ends joined to three slip rings on the shaft |
| Rugged, cheap, no brushes; slots skewed to reduce noise and cogging | External resistance can be inserted through brushes, giving high starting torque, low starting current and speed control |

*Working principle.*

1. The three-phase stator current produces a **rotating magnetic field** of constant magnitude $1.5\,\Phi_m$ rotating at the synchronous speed $N_s = 120f/p$ (1500 rpm for 4 poles at 50 Hz).
2. The rotating field cuts the stationary rotor conductors and, by Faraday's law, **induces emf** in them; since the rotor circuit is closed (cage or external resistance), a current flows.
3. By Lenz's law the rotor current opposes the cause, that is, the *relative speed* between the rotating field and the rotor, and the force $F = BIl$ on the rotor conductors produces a **torque** in the direction of the field, so the rotor starts to rotate.
4. The rotor can never reach $N_s$: at $N = N_s$ there would be no relative speed, no emf and no torque. It therefore runs at $N < N_s$, and the fractional difference is the **slip**

$$s = \frac{N_s - N}{N_s}$$

5. The rotor emf and current have the frequency $sf$, the rotor induced emf is $sE_{20}$, and the electromagnetic torque is $T = \dfrac{3}{\omega_s}\dfrac{I_2^2R_2}{s}$. It acts as a motor for $0 < s < 1$ (a full-load slip of 2 to 5 %); no electrical connection to the rotor is needed (hence "induction", a transformer with a short-circuited moving secondary).

@s 9
**4-pole, 50 Hz, 1440 rpm induction motor** (input $P_{in} = 35$ kW; stator loss $= 1$ kW; friction and windage loss $= 1.5$ kW).

$$\begin{gathered}N_s = \frac{120f}{p} = \frac{120 \times 50}{4} = 1500\ \text{rpm} \\ s = \frac{1500 - 1440}{1500} = 0.04\end{gathered}$$

*Power flow:*

$$\text{Rotor input (air-gap power)} = P_{in} - P_{stator} = 35 - 1 = 34\ \text{kW}$$

**(i) Rotor copper loss:**

$$P_{cu2} = s \times P_{ag} = 0.04 \times 34 = \mathbf{1.36\ kW}$$

**(ii) Efficiency:** the gross mechanical power is $P_m = P_{ag} - P_{cu2} = 34 - 1.36 = 32.64$ kW; the shaft output is

$$P_{out} = P_m - P_{fw} = 32.64 - 1.5 = 31.14\ \text{kW} \;(= 41.7\ \text{hp})$$

$$\eta = \frac{P_{out}}{P_{in}} = \frac{31.14}{35} = 0.8897 = \mathbf{89.0\,\%}$$

@s 10
**Why a starter is needed.** At standstill the slip is $s = 1$ and the induction motor behaves like a short-circuited transformer: with the rated voltage across the stator the rotor emf is at its maximum and the **starting current is 5 to 8 times the full-load current**, with a poor power factor (0.3). This causes a large voltage dip on the supply (flicker, disturbance to other consumers), heating of the windings and mechanical stress. A starter reduces the voltage across the motor (or increases the rotor resistance) during starting to limit this current, and is removed as the speed rises. (Small motors, below 3 to 5 kW, may be started direct.)

**Methods of starting a squirrel-cage motor** (reduced-voltage starters; torque varies as $V^2$):

| Method | Principle | Starting current (of DOL) | Starting torque (of DOL) |
|---|---|---|---|
| **Direct-on-line (DOL)** | Full voltage through a contactor and overload relay | 100 % | 100 % |
| **Stator resistance (or reactor)** | Series resistor in each stator lead, short-circuited after speed-up | $x$ | $x^2$ |
| **Auto-transformer (compensator)** | Reduced voltage $xV$ from taps (50, 65, 80 %); the line current is $x^2$ of DOL | $x^2$ | $x^2$ |
| **Star-delta** | Stator is started in Y (phase voltage $V/\sqrt3$), then switched to Δ by a TPDT switch or contactors; needs six terminals | 1/3 | 1/3 |
| **Soft starter** | Thyristors (phase-angle control) ramp the voltage up | adjustable | adjustable |
| **Variable frequency drive (VFD)** | Voltage and frequency ramped together, constant $V/f$ | about 1 to 1.5 $I_{FL}$ | up to 1.5 $T_{FL}$ or more |

**Slip-ring (wound-rotor) motor:** a **rotor-resistance starter** (a 3-phase variable resistor connected through the slip rings) is used. It reduces the starting current because $I_2 = sE_{20}/\sqrt{R_2^2 + (sX_2)^2}$ falls as $R_2$ rises, and it **increases** the starting torque (maximum starting torque when $R_2 = X_2$), and the resistance is cut out step by step.

*Example (star-delta):* in the star connection each phase gets $V_L/\sqrt3$, so the phase current and starting line current are $1/\sqrt3$ and $1/3$ of those in delta, and the starting torque is also reduced to one third. It is therefore used only for light-load starts (fans, pumps, machine tools); heavy-load starts use the auto-transformer or slip-ring methods.

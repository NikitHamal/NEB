---
file: NEBians-IOE-Past-Paper-Electrical-Machine-I-ENEE202-2081-Chaitra.pdf
subject: Electrical Machine I
level: BE · Year II / Part I
code: ENEE 202
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course, 2080 batch), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
A circular ring of magnetic material has a mean length of 0.8 m, cross sectional area of 120 cm$^2$ and an air gap of 5 mm. Calculate the magnetizing current required to produce a flux of 1 mWb in the air gap if the ring is wound uniformly with a coil of 220 turns. Take relative permeability of the ring material = 500 and neglect leakage and fringing. [[6]]

@q 2
Define referred quantities in transformer. Derive the expression for the referred quantities (voltage, current, impedance) in a transformer. [[1+5]]

@q 3
Daily loading of a 150 kVA transformer having iron loss of 400 W and full load copper loss of 1700 W is given below. Determine the all-day efficiency of the transformer. [[6]]

| Time | Load (kW) | Power factor |
|---|---|---|
| 6:00 – 10:00 | 50 | 0.9 |
| 10:00 – 17:00 | 60 | 0.85 |
| 17:00 – 21:00 | 70 | 0.8 |
| 21:00 – 6:00 | 10 | 0.95 |

@q 4
A single phase, 100 kVA, 2000/200 V, 50 Hz transformer has an impedance drop of 10% and resistance drop of 5%. Calculate; [[3+3]]

(a) The regulation at full load 0.8 power factor lagging.

(b) The value of power factor at which regulation is zero.

@q 5
Define armature reaction in DC machine. Explain its effects on the operation of DC machine. What measures can be taken to reduce its effect? [[2+2+2]]

@q 6
A 220 V DC series motor draws full-load line current of 38 A at the rated speed of 600 rpm. The motor has armature resistance of 0.4 Ω and the series field resistance is 0.2 Ω. The brush voltage drop irrespective of load is 3.0 volts, find: [[3+3]]

(a) The speed of the motor when the load current drops to 19 A.

(b) The speed on removal of load when the motor takes only 1 A from the supply.

@q 7
Explain the necessity of testing in DC machines. Explain how is the retardation test different from the Swinburne's test? [[3+3]]

@q 8
Mention the basic difference between slip ring and squirrel cage induction motor. Discuss their application and its characteristics. [[4+2]]

@q 9
A 440 V 3-phase 50 Hz, 4-pole Y-connected Induction motor has a full load 1425 rpm. The rotor has an Impedance of (0.4 + j 4) Ω per phase and rotor/ stator turn ratio is 0.8. Calculate; [[2+2+2]]

(i) Full-load torque

(ii) Rotor current and

(iii) Full-load rotor Cu loss.

@q 10
Explain the operation of three phase induction motor as induction generator in isolated mode. Explain the role of induction machines in renewable energy applications. [[4+2]]

<!-- SOLUTIONS -->

@s 1
**Magnetic circuit with an air gap** (iron ring in series with the gap). Cross-section $A = 120\ \text{cm}^2 = 1.2\times10^{-2}\ \text{m}^2$, $\mu_r = 500$, $l_g = 5$ mm, mean length $0.8$ m (so the iron length is $l_i = 0.8 - 0.005 = 0.795$ m), $N = 220$.

Flux density (the same in iron and gap, no leakage or fringing):

$$B = \frac{\Phi}{A} = \frac{1\times10^{-3}}{1.2\times10^{-2}} = 0.08333\ \text{T}$$

$$\text{mmf of the iron} = \frac{B\,l_i}{\mu_0\mu_r} = \frac{0.08333 \times 0.795}{4\pi\times10^{-7}\times500} = 105.4\ \text{AT}$$

$$\text{mmf of the air gap} = \frac{B\,l_g}{\mu_0} = \frac{0.08333 \times 0.005}{4\pi\times10^{-7}} = 331.6\ \text{AT}$$

$$NI = 105.4 + 331.6 = 437.0\ \text{AT} \quad\Rightarrow\quad I = \frac{437.0}{220} = \mathbf{1.99\ A}$$

(If the whole 0.8 m is taken as the iron length, $I = 1.989$ A: the same to three figures.) The air gap, only 0.6 % of the length, needs about 76 % of the mmf, which shows why gaps dominate the magnetising current.

@s 2
**Referred quantities.** The primary and secondary of a transformer have different voltages and currents. To analyse the circuit as one network, all quantities are expressed on one side (primary or secondary): the *referred* (or "transferred") value of a voltage, current or impedance is its equivalent value on the other side, found with the turns ratio $K = N_2/N_1 = E_2/E_1 = I_1/I_2$, so that the **power and the stored energy are unchanged**.

**Derivation.**

*Voltage:* the secondary voltage referred to the primary is the voltage that would exist in the primary if the secondary turns were $N_1$:

$$\begin{gathered}V_2' = \frac{V_2}{K} \\ \text{and referred to the secondary:}\quad V_1' = KV_1\end{gathered}$$

*Current:* the ampere-turns are equal ($I_1N_1 = I_2N_2$), so

$$\begin{gathered}I_2' = KI_2 \\ I_1' = \frac{I_1}{K}\end{gathered}$$

so that $V_2'I_2' = V_2I_2$: the apparent power is invariant.

*Impedance:* an impedance $Z_2$ in the secondary dissipates $I_2^2R_2$; the same power in the primary side needs $I_2'^2R_2' = I_2^2R_2$:

$$R_2' = R_2\left(\frac{I_2}{I_2'}\right)^2 = \frac{R_2}{K^2}$$

and similarly for the reactance and impedance ($Z_2 = V_2/I_2$ gives $Z_2' = V_2'/I_2' = (V_2/K)/(KI_2)$):

$$\begin{gathered}X_2' = \frac{X_2}{K^2} \\ Z_2' = \frac{Z_2}{K^2} \\ Z_L' = \frac{Z_L}{K^2}\end{gathered}$$

and, referred to the secondary, $R_1' = K^2R_1$, $X_1' = K^2X_1$.

*Equivalent resistance, reactance and impedance referred to the primary:*

$$\begin{gathered}R_{01} = R_1 + R_2' = R_1 + \frac{R_2}{K^2} \\ X_{01} = X_1 + X_2' = X_1 + \frac{X_2}{K^2} \\ Z_{01} = \sqrt{R_{01}^2 + X_{01}^2}\end{gathered}$$

and referred to the secondary: $R_{02} = R_2 + K^2R_1$, $X_{02} = X_2 + K^2X_1$. The referred impedances are related by $Z_{02} = K^2Z_{01}$, and the $I^2R$ loss in the equivalent resistance equals the total copper loss.

```figure caption="Question 2: equivalent circuit of a transformer with every quantity referred to the primary (R_0 and X_0 are the core-loss and magnetising branch; R_01 = R_1 + R_2/K^2 and X_01 = X_1 + X_2/K^2)."
fig,ax=ckt_canvas(6.4,2.8)
wire(ax,[(0.0,2.4),(0.7,2.4)]); res(ax,(0.7,2.4),(2.3,2.4),"R$_{01}$",side=1,body=1.0); ind(ax,(2.3,2.4),(3.9,2.4),"X$_{01}$",side=1,body=1.0); wire(ax,[(3.9,2.4),(7.2,2.4)])
node(ax,(4.6,2.4)); res(ax,(4.6,2.4),(4.6,0),"R$_0$",side=-1,body=0.9); node(ax,(5.8,2.4)); ind(ax,(5.8,2.4),(5.8,0),"X$_0$",side=1,body=0.9)
wire(ax,[(0.0,0),(5.8,0)]); res(ax,(7.2,2.4),(7.2,0),"Z$_L$' = Z$_L$/K$^2$",side=1,body=1.0,off=1.0); wire(ax,[(5.8,0),(7.2,0)])
label(ax,(0.0,1.2),"V$_1$",size=9); label(ax,(6.7,1.2),"V$_2$'",size=9)
```

@s 3
**All-day (energy) efficiency.** $\displaystyle \eta_{all\ day} = \frac{\text{kWh output in 24 h}}{\text{kWh output} + \text{iron-loss kWh} + \text{copper-loss kWh}}$.

The iron loss is constant: $0.4\ \text{kW} \times 24\ \text{h} = 9.6$ kWh. The copper loss varies with the square of the load: $P_{cu} = 1700\,(S/150)^2$, with $S = P/\cos\varphi$.

| Period | Hours | Load (kW) | pf | kVA | $P_{cu}$ (W) | Output (kWh) | Cu loss (kWh) |
|---|---|---|---|---|---|---|---|
| 6:00 – 10:00 | 4 | 50 | 0.90 | 55.56 | 233.2 | 200 | 0.933 |
| 10:00 – 17:00 | 7 | 60 | 0.85 | 70.59 | 376.5 | 420 | 2.635 |
| 17:00 – 21:00 | 4 | 70 | 0.80 | 87.50 | 578.5 | 280 | 2.314 |
| 21:00 – 6:00 | 9 | 10 | 0.95 | 10.53 | 8.4 | 90 | 0.075 |
| **Total** | 24 | | | | | **990** | **5.957** |

$$\eta_{all\ day} = \frac{990}{990 + 9.6 + 5.957} = \frac{990}{1005.56} = 0.9845 = \mathbf{98.45\,\%}$$

@s 4
**100 kVA, 2000/200 V transformer:** per-unit impedance drop $= 0.10$, resistance drop $v_r = 0.05$, so the reactance drop is

$$v_x = \sqrt{0.10^2 - 0.05^2} = 0.0866\ \text{p.u.} \;(8.66\,\%)$$

**(a) Regulation at full load, 0.8 pf lagging** ($\cos\varphi = 0.8$, $\sin\varphi = 0.6$):

$$\%\text{VR} \approx \left(v_r\cos\varphi + v_x\sin\varphi\right)\times100 = (0.05\times0.8 + 0.0866\times0.6)\times100 = \mathbf{9.20\,\%}$$

(Exact value: $\sqrt{(0.8 + 0.05)^2 + (0.6 + 0.0866)^2} - 1 = 0.0927 = 9.27\,\%$.)

**(b) Power factor for zero regulation.** Regulation is zero only for a **leading** power factor. Setting $v_r\cos\varphi - v_x\sin\varphi = 0$ (approximate condition):

$$\tan\varphi = \frac{v_r}{v_x} = \frac{0.05}{0.0866} = 0.5774 \quad\Rightarrow\quad \varphi = 30^\circ$$

$$\boxed{\cos\varphi = 0.866\ \text{leading}}$$

(The exact condition $\sqrt{(\cos\varphi + v_r)^2 + (v_x - \sin\varphi)^2} = 1$ gives $\cos\varphi = 0.840$ leading; at that load the secondary voltage is the same as at no-load.) The maximum (most negative) regulation for a given load occurs at leading $\cos\varphi = 0.866$ and the maximum positive at lagging $\cos\varphi = v_r/z = 0.5$.

@s 5
**Armature reaction.** The armature current of a DC machine produces its own magnetic field (armature mmf) which acts on the main field of the poles. The effect of the armature mmf on the distribution and magnitude of the main flux is called **armature reaction**.

*Effects on the operation:*

1. **Cross-magnetising effect (distortion):** with the brushes at the geometric neutral axis (GNA), the armature mmf is along the brush axis, 90° to the main field. It strengthens the flux under one pole tip (the trailing tip in a generator) and weakens it at the other, so the flux distribution is distorted.
2. **Shift of the magnetic neutral axis (MNA):** the MNA moves forward (generator) or backward (motor) by an angle $\theta$, so the brushes at the GNA are no longer on the commutating zone; sparking results.
3. **Demagnetising effect:** because of magnetic saturation, the pole tip that gets strengthened gains less flux than the other loses, so the **total flux per pole decreases**; the generated emf (and the generator voltage) falls, and a motor tends to speed up.
4. When the brushes are shifted (ahead of the GNA in a generator), the armature mmf has a direct **demagnetising component** (conductors between $\pm\theta$ of the brush axis) and a cross-magnetising component.
5. Increased sparking at the brushes, higher stress between segments (flashover), noise and poor commutation.

```figure caption="Question 5: flux density in the air gap under one pole: at no load (flat), with the cross-magnetising armature field alone (triangular), and the net distribution on load (distorted and reduced because of saturation at the strengthened tip)."
fig,ax=plt.subplots(figsize=(5.6,2.7))
x=np.linspace(-1,1,400); pole=1/(1+np.exp((np.abs(x)-0.72)/0.04))
B0=pole; Ba=0.55*x*pole; Bl=np.minimum(B0+Ba,1.12)*pole
ax.plot(x,B0,color=INK,lw=1.6,label="no load"); ax.plot(x,Ba,color=SERIES[3],lw=1.2,ls="--",label="armature field")
ax.plot(x,Bl,color=SERIES[1],lw=1.8,label="on load (net)")
ax.fill_between(x,Bl,B0,where=(Bl<B0),color=SERIES[1],alpha=0.15)
ax.axvline(0,color=MUTED,lw=0.8,ls=":"); ax.text(0.02,-0.52,"GNA",fontsize=8,color=MUTED)
ax.text(-0.95,1.18,"leading pole tip\n(weakened)",fontsize=7.5); ax.text(0.45,1.22,"trailing tip\n(strengthened)",fontsize=7.5)
ax.set_ylim(-0.6,1.5); ax.set_xlabel("position under pole (pole centre = 0)",fontsize=8.5); ax.set_ylabel("B (relative)",fontsize=8.5); ax.legend(fontsize=7.5,loc="lower center",ncol=3); ax.tick_params(labelsize=8)
```

*Measures to reduce armature reaction:*

1. **Interpoles (commutating poles)** in the neutral zone, in series with the armature, whose mmf opposes the armature mmf there (also gives good commutation).
2. **Compensating winding** in slots in the pole faces, in series with the armature and carrying the current in the opposite direction to that in the armature conductors under the poles: it neutralises the cross-magnetising mmf (used in large machines and with fast load changes).
3. **Pole-face design:** increased air-gap length, slotted or chamfered pole tips, high-reluctance pole tips (laminations with slots) to raise the reluctance in the cross-axis.
4. **Brush shifting** (backward lead in a motor, forward in a generator) in small machines without interpoles, which needs to be repeated as the load changes.
5. Operating the machine at lower flux density (avoid saturation) and a small armature loading ($A/m$).

@s 6
**220 V DC series motor.** Total series resistance $R = R_a + R_{se} = 0.4 + 0.2 = 0.6\ \Omega$, brush drop $V_b = 3$ V.

*Full load* ($I_1 = 38$ A, $N_1 = 600$ rpm):

$$E_{b1} = V - I_1R - V_b = 220 - 38\times0.6 - 3 = 194.2\ \text{V}$$

For a series motor the flux is (below saturation) proportional to the current, $\Phi \propto I$, and $E_b \propto \Phi N$, so

$$\frac{N_2}{N_1} = \frac{E_{b2}}{E_{b1}}\cdot\frac{\Phi_1}{\Phi_2} = \frac{E_{b2}}{E_{b1}}\cdot\frac{I_1}{I_2}$$

**(a) At $I_2 = 19$ A:**

$$E_{b2} = 220 - 19\times0.6 - 3 = 205.6\ \text{V}$$

$$N_2 = 600 \times \frac{205.6}{194.2} \times \frac{38}{19} = \mathbf{1270\ rpm}$$

**(b) At $I_3 = 1$ A (no load):**

$$E_{b3} = 220 - 1\times0.6 - 3 = 216.4\ \text{V}$$

$$N_3 = 600 \times \frac{216.4}{194.2} \times \frac{38}{1} = \mathbf{25\,400\ rpm\ (about\ 2.5\times10^4\ rpm)}$$

Such a speed is only the result of the linear assumption $\Phi \propto I$; in reality the flux does not fall below the residual value, but it is still **dangerously high**: a series motor must never be run without load (the armature would be thrown apart), and it is always coupled directly or by gears, never by a belt.

@s 7
**Necessity of testing DC machines.** Testing is needed to (i) determine the **efficiency** at any load without loading the machine fully (a large machine cannot easily be given a full load), (ii) separate the **constant losses** (iron, friction, windage) from the variable losses, (iii) find the temperature rise, the characteristics (OCC, load, speed-torque) and the commutation performance, (iv) check the performance against the guaranteed values and the standards before delivery, and (v) find the moment of inertia and the losses for design and troubleshooting.

**Retardation test.** The machine is run as a motor at a speed a little above the rated speed and the supply is switched off. The machine slows down because the kinetic energy of the rotating parts supplies the stray losses (friction, windage and iron loss), and the loss is

$$\begin{gathered}W_s = -\frac{d}{dt}\left(\tfrac12 J\omega^2\right) = -J\omega\frac{d\omega}{dt} \\ (\text{with the field excited, so iron loss is included})\end{gathered}$$

The speed-time curve is recorded (tachometer and stopwatch) and the slope $d\omega/dt$ at the rated speed is found by a tangent. To eliminate the unknown moment of inertia $J$, a second retardation run is made with the armature connected across a known resistance $R$ (field unchanged): the additional loss is $W_e = E_b^2/R$ ($= V_aI_a$ as measured), so

$$\begin{gathered}W_s = J\omega\left|\frac{d\omega}{dt}\right|_1 \\ W_s + W_e = J\omega\left|\frac{d\omega}{dt}\right|_2 \quad\Rightarrow\quad W_s = \frac{W_e}{\dfrac{(d\omega/dt)_2}{(d\omega/dt)_1} - 1}\end{gathered}$$

```figure caption="Question 7: retardation test. The speed decays after switching off: the slope of the tangent at the rated speed gives the stray loss; the second curve (armature across a known resistor) falls faster because of the added electrical loss."
fig,ax=plt.subplots(figsize=(5.2,2.6))
t=np.linspace(0,60,200); ax.plot(t,1050*np.exp(-t/55),color=ACCENT,lw=2,label="run 1: field on, armature open")
ax.plot(t,1050*np.exp(-t/22),color=SERIES[1],lw=2,label="run 2: armature across R")
t0=0; ax.plot([0,25],[1000,1000-1050/55*25],color=MUTED,ls="--",lw=1); ax.plot([0,10],[1000,1000-1050/22*10],color=MUTED,ls="--",lw=1)
ax.axhline(1000,color=GRID,lw=0.8); ax.text(40,1010,"rated speed",fontsize=7.5,color=MUTED)
ax.set_xlabel("time (s)",fontsize=8.5); ax.set_ylabel("speed (rpm)",fontsize=8.5); ax.legend(fontsize=7.5,loc="center right"); ax.tick_params(labelsize=8); ax.grid(color=GRID,lw=0.6)
```

**Retardation test versus Swinburne's test.**

| Point | Swinburne's test | Retardation test |
|---|---|---|
| Machine running | As a motor on no-load, with the supply connected | Supply is **disconnected**; the machine coasts down |
| What is measured | Input power at no-load $= $ constant losses (iron + friction + windage + no-load armature copper loss) | The rate of fall of speed (a speed-time curve) |
| Constant losses by | $VI_0 - I_{a0}^2R_a$ | $-J\omega\,d\omega/dt$ (needs $J$ or a second run) |
| Applicable to | Shunt and compound machines running at constant speed and flux (not to series motors, which would run away) | Any machine that can be run up and left to coast, including series; large machines and generators |
| Assumption | The constant losses are the same at no load and at full load (flux and speed assumed constant), so armature reaction effect is not shown | Losses are found at each speed over the whole range, so the variation of loss with speed is obtained |
| Cost / equipment | Only a supply and meters | Needs a tachometer and stopwatch, or a speed-time recorder |
| Accuracy | Good for small and medium machines | Good for large machines with big inertia, but depends on accuracy of the tangent |

@s 8
**Slip-ring versus squirrel-cage induction motor.**

| Point | Squirrel-cage motor | Slip-ring (wound-rotor) motor |
|---|---|---|
| Rotor | Bars of aluminium or copper short-circuited by end-rings; no external connection | 3-phase star-connected winding brought out to 3 slip rings with brushes |
| Rotor resistance | Fixed, low; cannot be changed | External resistance can be added (also removed) |
| Starting torque | Low to moderate (1 to 2 $T_{FL}$ depending on design class) | High (up to the maximum torque, by adding rotor resistance) |
| Starting current | High (5 to 8 $I_{FL}$), reduced only by a stator-side starter | Low (about 1.5 to 2.5 $I_{FL}$) with the rotor resistance |
| Speed control | Only by frequency (VFD), voltage, pole changing | Rotor resistance, slip power recovery (Scherbius), cascade |
| Construction and cost | Simple, rugged, no brushes, cheap, little maintenance | Complex, more costly, brushes and slip rings need maintenance |
| Efficiency, power factor | Higher efficiency (no external loss) | Slightly lower with the resistance in the circuit |

**Characteristics.** The torque-slip characteristic is $T = \dfrac{3}{\omega_s}\dfrac{sE_2^2R_2}{R_2^2 + (sX_2)^2}$: the maximum (breakdown) torque occurs at $s_m = R_2/X_2$ and is independent of the rotor resistance. Adding resistance in a slip-ring motor moves the peak towards $s = 1$ (starting), keeping the same maximum torque; the squirrel-cage motor has a steep, nearly constant-speed characteristic (a 'shunt' type; slip 2 to 5 % at full load).

```figure caption="Question 8: torque-slip characteristics. A squirrel-cage motor has a fixed low R_2 (steep curve, low starting torque). In a slip-ring motor, added rotor resistance moves the peak to the left (to s = 1), giving the maximum torque at starting; the peak value stays the same."
fig,ax=plt.subplots(figsize=(5.4,2.8))
s=np.linspace(0.001,1,400); X2=1.0
for R2,c,l in ((0.15,ACCENT,"squirrel cage, R$_2$ = 0.15"),(0.4,SERIES[2],"slip ring, R$_2$ + R$_{ext}$ = 0.4"),(1.0,SERIES[1],"slip ring, R$_2$ + R$_{ext}$ = 1.0 (= X$_2$)")):
    T=s*R2/(R2**2+(s*X2)**2); ax.plot(s,T/0.5,color=c,lw=1.8,label=l)
ax.set_xlabel("slip s  (1 = standstill)",fontsize=8.5); ax.set_ylabel("T / T$_{max}$",fontsize=8.5); ax.legend(fontsize=7.5,loc="center right"); ax.invert_xaxis(); ax.tick_params(labelsize=8); ax.grid(color=GRID,lw=0.6)
```

**Applications.** *Squirrel-cage:* fans, pumps, compressors, lathes, conveyors, blowers and water-supply motors (constant-speed, light or medium starting duty); with VFDs also variable-speed drives. *Slip-ring:* cranes and hoists, lifts, rolling mills, ball and crushing mills, compressors started under load, and any drive with a high starting inertia or a limited supply (needs a high starting torque with a low starting current).

@s 9
**440 V, 50 Hz, 4-pole, Y-connected induction motor**, $N = 1425$ rpm, $R_2 = 0.4\ \Omega$, $X_2 = 4\ \Omega$ (standstill values, per phase), rotor-to-stator turns ratio $0.8$. The stator impedance drop is neglected.

$$\begin{gathered}N_s = \frac{120\times50}{4} = 1500\ \text{rpm} \\ s = \frac{1500 - 1425}{1500} = 0.05\end{gathered}$$

$$\begin{gathered}E_1 = \frac{440}{\sqrt3} = 254.0\ \text{V (stator phase)} \\ E_{20} = 0.8\times254.0 = 203.2\ \text{V (rotor, standstill, per phase)}\end{gathered}$$

**(ii) Rotor current at full load:**

$$I_2 = \frac{sE_{20}}{\sqrt{R_2^2 + (sX_2)^2}} = \frac{0.05\times203.2}{\sqrt{0.4^2 + (0.05\times4)^2}} = \frac{10.16}{0.4472} = \mathbf{22.72\ A\ per\ phase}$$

($\cos\varphi_2 = R_2/\sqrt{R_2^2 + (sX_2)^2} = 0.894$, $\varphi_2 = 26.6^\circ$.)

**(iii) Full-load rotor copper loss:**

$$P_{cu2} = 3I_2^2R_2 = 3\times22.72^2\times0.4 = \mathbf{619.5\ W}$$

**(i) Full-load torque.** Air-gap power $P_{ag} = P_{cu2}/s = 619.5/0.05 = 12\,390$ W; $\omega_s = 2\pi\times1500/60 = 157.08$ rad/s:

$$T = \frac{P_{ag}}{\omega_s} = \frac{12\,390}{157.08} = \mathbf{78.9\ N\,m}$$

(the mechanical power developed is $P_m = (1-s)P_{ag} = 11\,771$ W, and $P_m/\omega_r = 11\,771/149.2 = 78.9$ N m, the same torque).

@s 10
**Induction generator in isolated mode (self-excited induction generator, SEIG).** An induction machine delivers power to a load when driven by a prime mover **above the synchronous speed** ($s < 0$, negative slip): the rotor leads the rotating field, the rotor current reverses and the electromagnetic torque opposes the prime mover, so mechanical power is converted to electrical power. A cage machine takes its **magnetising current from the grid** (it has no field winding); in an **isolated** (stand-alone) system with no grid, the reactive power must be supplied by a **capacitor bank** connected across the stator terminals.

*Operation (self-excitation).*

1. A capacitor bank $C$ (per phase, delta or star) is connected across the stator terminals. The rotor is driven at the speed $N > N_s$.
2. The **residual magnetism** in the rotor core induces a small emf in the stator; this emf drives a small leading current through the capacitors, and that current acts as the magnetising current, which reinforces the flux.
3. The voltage and capacitor current rise together (as in a DC shunt generator) until the capacitor line $V = I_m X_C = I_m/(2\pi fC)$ meets the **magnetisation (no-load saturation) curve** of the machine. The operating point is the intersection, which sets the no-load voltage. Needs $C > C_{min}$, a capacitor line less steep than the tangent to the initial part of the magnetisation curve.
4. A load is connected to the terminals; the frequency is determined by the speed and the load (it is not fixed by a grid), and voltage and frequency droop with load unless more capacitance and speed control (or a controller such as an electronic load controller and a STATCOM) are provided.
5. The required capacitance is about $C = I_m/(2\pi fV)$ per phase for the magnetising current at rated voltage; for a load of lagging power factor, more capacitance is needed.

```figure caption="Question 10: self-excitation of an induction generator: the generated voltage builds up along the magnetisation curve until it meets the capacitor line V = I x X_C (small C: line too steep, no build-up)."
fig,ax=plt.subplots(figsize=(5.2,2.8))
i=np.linspace(0,1.6,300); V=1.05*np.tanh(i/0.8)*1.0+0.03
ax.plot(i,V,color=ACCENT,lw=2,label="magnetisation curve (residual + saturation)")
ax.plot(i,0.95*i,color=SERIES[2],lw=1.6,label="C large enough (build-up to the crossing)")
ax.plot(i,1.9*i,color=SERIES[1],lw=1.6,label="C too small (no build-up)")
ax.plot([0.97],[0.92],"o",color=INK,ms=5); ax.text(1.0,0.78,"operating point",fontsize=8)
ax.set_xlim(0,1.6); ax.set_ylim(0,1.3); ax.set_xlabel("magnetising current I$_m$ (p.u.)",fontsize=8.5); ax.set_ylabel("stator voltage (p.u.)",fontsize=8.5); ax.legend(fontsize=7.2,loc="lower right"); ax.tick_params(labelsize=8); ax.grid(color=GRID,lw=0.6)
```

*Advantages:* simple, rugged, no brushes or DC excitation, no synchronising equipment, self-protecting against short circuit (the voltage collapses), low cost and maintenance. *Drawbacks:* poor voltage and frequency regulation, needs capacitor bank and control, limited to small plants.

**Role of induction machines in renewable energy applications.**

1. **Wind turbines:** squirrel-cage induction generators (fixed-speed, grid-connected, through a gearbox, with capacitor banks for power factor correction) and the **doubly-fed induction generator (DFIG)**, a slip-ring machine whose rotor is fed through a back-to-back converter of about 30 % of the rating, which allows a variable speed range of $\pm30\,\%$ and independent control of real and reactive power; widely used in 1.5 to 6 MW wind turbines.
2. **Micro and pico hydro (very relevant to Nepal):** self-excited cage induction generators with capacitors and an electronic load controller (ballast load) supply remote villages at 3 to 50 kW, because they need no exciter or governor and are cheap.
3. **Biogas, biomass and small engine-driven generators**, and waste-heat and tidal / wave plants where the speed varies.
4. **Solar-pump and storage systems:** cage induction motors with VFDs for pumping from PV; induction motors in pumped storage and flywheel systems, and induction machines for regenerative braking in electric vehicles.

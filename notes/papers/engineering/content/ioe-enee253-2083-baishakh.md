---
file: NEBians-IOE-Past-Paper-Electrical-Machine-II-ENEE253-2083-Baishakh.pdf
subject: Electrical Machine II
level: BE · Year II / Part II
code: ENEE 253
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electrical Engineering (BEL), Year II / Part II. Full marks 30, pass marks 12. All questions carry equal marks (3 each).
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
With neat sketch, explain about constructional features of synchronous machine. Discuss different types of rotor and their applications. [[3]]

@q 2
Define pitch factor and distribution factor, derive the EMF equation of an alternator. [[3]]

@q 3
A 3 phase, star connected alternator with R = 0.4 Ω and x = 6 Ω per phase delivers 300 A at power factor 0.8 to constant frequency 10 kV busbars. If the steam supply is unchanged, find the percentage change in the induced emf necessary to raise the power factor to unity. Ignore the change in losses. [[3]]

@q 4
Explain the power capability curve of a synchronous machine. What are its main components? [[3]]

@q 5
A 300 V, 1.5 MW, 3 phase synchronous motor has X$_d$ = 4 Ω/phase and X$_q$ = 3 Ω/phase, neglecting all losses, calculate the excitation emf when motor supplies rated load at unity power factor. Calculate the maximum mechanical power which the motor would develop for this field excitation. [[3]]

@q 6
What is hunting in synchronous machines? Explain in details and how they reduced. [[3]]

@q 7
Illustrate the concept of d axis and q axis in synchronous machine. Why dq0 plane in synchronous machine is needed? [[3]]

@q 8
A 250 W, 230 V, 50 Hz capacitor start motor has following impedances at standstill. Z$_m$ = 7 + j5 Ω and Z$_a$ = 11.5 + j5 Ω. Find the value of the capacitor to be connected in series with the auxiliary winding to give a quadrant phase displacement between the currents in two windings. Draw the circuit and phasor diagram for motor. [[3]]

@q 9
Derive the torque equation of permanent magnet BLDC motor. And also explain torque-speed characteristics of the same motor. [[3]]

@q 10
Discuss the construction and working principle of switched reluctance motor. [[3]]

<!-- SOLUTIONS -->

@s 1
**Constructional features.** A synchronous machine has two main members: a **stator (armature)** that carries the three-phase winding and a **rotor (field)** that carries the d.c.-excited poles.

- **Stator frame:** cast-iron or fabricated steel yoke; it supports the core, gives mechanical strength and carries the cooling-air or hydrogen ducts.
- **Stator core:** stack of 0.35 to 0.5 mm silicon-steel laminations, insulated from one another (varnish or oxide) to cut eddy-current loss; radial ventilation ducts every 6 to 8 cm.
- **Armature winding:** three-phase, double-layer, lap or wave, short-pitched coils placed in open or semi-closed slots, star connected with the neutral brought out for grounding.
- **Rotor and field winding:** d.c. excited through two **slip rings and carbon brushes** (or a brushless exciter with rotating diodes on large units).
- **Exciter:** a small d.c. generator (or static / brushless rectifier) on the same shaft that supplies the field current, typically 0.5 to 2 % of the rating.
- **Damper (amortisseur) winding:** copper or brass bars short-circuited by end rings in the pole faces; it damps hunting and lets a synchronous motor self-start.
- **Shaft, bearings and cooling system:** air-cooled up to about 50 MVA, hydrogen or water cooled for large turbo-alternators.

The speed is rigidly tied to the frequency: $N_s = \dfrac{120f}{P}$ rpm.

**Types of rotor**

| | **Salient-pole rotor** | **Cylindrical (non-salient, round) rotor** |
|---|---|---|
| Shape | Projecting poles bolted or dovetailed to a spider; large diameter, short axial length | Smooth solid forged-steel cylinder with slots milled along 2/3 of the surface; small diameter, long axial length |
| Poles | Many (4 to 60 or more) | 2 or 4 |
| Speed | Low, 100 to 1500 rpm | High, 1500 or 3000 rpm |
| Air gap | Non-uniform ($X_d \ne X_q$) | Uniform ($X_d = X_q = X_s$) |
| Winding | Concentrated field coils on each pole; damper bars in pole faces | Distributed field winding in slots held by steel wedges and retaining rings |
| Strength | Poor at high speed (windage, centrifugal stress) | Very strong, balanced, quiet |
| Use | Hydro-electric and diesel-engine generators (Kaligandaki, Marsyangdi), synchronous condensers, large slow motors | Steam and gas turbine alternators (thermal plants), high-speed motors |

```figure caption="Question 1: cross-sections of the two rotor types (stator shown as the outer ring)."
fig,axs=plt.subplots(1,2,figsize=(6.8,3.0))
for ax in axs:
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.35,1.35); ax.set_ylim(-1.35,1.35)
    ax.add_patch(Circle((0,0),1.25,fc='none',ec=INK,lw=1.2)); ax.add_patch(Circle((0,0),1.05,fc='none',ec=INK,lw=1.0))
a=axs[0]; a.set_title('Salient pole (4 poles)',fontsize=8.5)
for k in range(4):
    th=k*np.pi/2; c,s=np.cos(th),np.sin(th)
    a.add_patch(Polygon([(0.30*c-0.12*s,0.30*s+0.12*c),(0.82*c-0.12*s,0.82*s+0.12*c),(0.95*c-0.24*s,0.95*s+0.24*c),(0.95*c+0.24*s,0.95*s-0.24*c),(0.82*c+0.12*s,0.82*s-0.12*c),(0.30*c+0.12*s,0.30*s-0.12*c)],fc='#cbd5e1',ec=INK,lw=1))
    a.add_patch(Rectangle((0.42,-0.20),0.04,0.4,angle=0,fc=ACCENT,ec='none',alpha=0.0))
a.add_patch(Circle((0,0),0.30,fc='#94a3b8',ec=INK)); a.text(0,0,'shaft',fontsize=6.5,ha='center',va='center')
a.text(0,-1.3,'damper bars in pole faces',fontsize=7,ha='center',va='top',color=MUTED)
b=axs[1]; b.set_title('Cylindrical rotor (2 poles)',fontsize=8.5)
b.add_patch(Circle((0,0),0.95,fc='#cbd5e1',ec=INK,lw=1))
for x in (-0.55,-0.35,-0.15,0.15,0.35,0.55):
    for sgn in (1,-1):
        b.add_patch(Rectangle((x-0.04,sgn*0.55-0.13 if sgn>0 else -0.55-0.13+0.0),0.08,0.26,fc='white',ec=INK,lw=0.7))
b.text(0,0,'N',fontsize=11,ha='center',va='center',color=INK); b.text(0,-1.3,'distributed slotted winding',fontsize=7,ha='center',va='top',color=MUTED)
```

@s 2
**Pitch (coil-span) factor $K_p$.** A coil is short-pitched by an electrical angle $\alpha$ (coil span $= 180^\circ - \alpha$). The emfs in its two sides are no longer in phase opposition, so the coil emf is the phasor sum, not the arithmetic sum:

$$K_p = \frac{\text{emf with short-pitched coil}}{\text{emf with full-pitched coil}} = \frac{2E\cos(\alpha/2)}{2E} = \cos\frac{\alpha}{2}$$

(e.g. $5/6$ pitch: $\alpha = 30^\circ$, $K_p = \cos 15^\circ = 0.966$.)

**Distribution (breadth) factor $K_d$.** The $m$ coils of a phase group lie in adjacent slots displaced by the slot angle $\gamma$, so their emfs differ in phase:

$$K_d = \frac{\text{phasor sum of the } m \text{ coil emfs}}{\text{arithmetic sum}} = \frac{\sin(m\gamma/2)}{m\sin(\gamma/2)}$$

(e.g. 3 slots per pole per phase, $\gamma = 20^\circ$: $K_d = \sin 30^\circ/(3\sin 10^\circ) = 0.960$.)

**EMF equation.** Let $\Phi$ = flux per pole (Wb), $P$ = number of poles, $N$ = speed in rpm, $f = PN/120$, $T_{ph}$ = series turns per phase ($Z_{ph}/2$).

In one revolution a conductor cuts $P\Phi$ weber in $60/N$ seconds, so

$$e_{avg,\ conductor} = \frac{P\Phi}{60/N} = \frac{P N\Phi}{60} = 2f\Phi \ \text{V}$$

A turn has two conductors: $e_{avg,\ turn} = 4f\Phi$. For a sinusoidal flux distribution the form factor is $\pi/(2\sqrt2) = 1.11$, so the r.m.s. emf per turn is $1.11\times4f\Phi = 4.44f\Phi$. For $T_{ph}$ turns in series:

$$\boxed{E_{ph} = 4.44\,K_pK_d\,f\,\Phi\,T_{ph}\ \text{V}}$$

For a star connection the line emf is $\sqrt3E_{ph}$. $K_p$ and $K_d$ are both less than 1, but they suppress the harmonics (especially the 5th and 7th) far more than the fundamental, which gives a nearly sinusoidal terminal voltage.

@s 3
**Data (taken as lagging).** Line voltage $V_L = 10$ kV, so the phase voltage is

$$\begin{gathered}V = \frac{10\,000}{\sqrt3} = 5773.5\ \text{V} \\ Z_s = 0.4 + j6\ \Omega\ (|Z_s| = 6.013\ \Omega)\end{gathered}$$

**Case 1: 300 A at 0.8 pf lagging.** Taking $V$ as reference, $\vec I_1 = 300\angle{-36.87^\circ} = 240 - j180$ A:

$$\begin{gathered}\vec E_1 = \vec V + \vec I_1Z_s = 5773.5 + (240 - j180)(0.4 + j6) \\ = 5773.5 + (96 + 1080) + j(1440 - 72) = 6949.5 + j1368 \\ E_1 = 7082.9\ \text{V/phase}\ (\angle 11.14^\circ),\ \ \sqrt3E_1 = 12.27\ \text{kV}\end{gathered}$$

**Case 2: unity pf, steam supply unchanged.** The steam (prime-mover) input is constant and the change in losses is ignored, so the real power delivered is unchanged:

$$\sqrt3V_LI_1\cos\varphi_1 = \sqrt3V_LI_2\cos\varphi_2 \ \Rightarrow\ I_2 = 300\times0.8 = 240\ \text{A (in phase with } V)$$

$$\vec E_2 = 5773.5 + 240(0.4 + j6) = 5869.5 + j1440 \ \Rightarrow\ E_2 = 6043.6\ \text{V/phase}\ (\angle 13.78^\circ)$$

**Percentage change in induced emf:**

$$\frac{E_2 - E_1}{E_1}\times100 = \frac{6043.6 - 7082.9}{7082.9}\times100 = \mathbf{-14.67\ \%}$$

The excitation must be **reduced by about 14.7 %** (line emf from 12.27 kV to 10.47 kV). Because a lagging machine is over-excited relative to a unity-pf machine at the same real power, raising pf to unity needs less field current.

@s 4
**Power capability curve (reactive capability chart, D-curve).** It is the plot of the real power $P$ against the reactive power $Q$ that a generator can deliver at its rated terminal voltage without exceeding any thermal or stability limit. With $V = 1$ pu and synchronous reactance $X_s$, the complex power at the terminals is

$$\begin{gathered}S = P + jQ \\ P^2 + \left(Q + \frac{V^2}{X_s}\right)^2 = \left(\frac{VE_f}{X_s}\right)^2 \\ P^2 + Q^2 = (VI_a)^2\end{gathered}$$

**Main components (boundaries) of the curve:**

1. **Armature-current (stator heating) limit:** a circle about the origin of radius $VI_{a,rated}$ (the rated MVA). It governs the region from rated pf to leading-pf operation.
2. **Field-current (rotor heating) limit:** a circle with centre $(0, -V^2/X_s)$ and radius $VE_{f,max}/X_s$. It governs the lagging, over-excited region. The two circles intersect at the **rated power-factor point** (e.g. 0.85 lag).
3. **Prime-mover (turbine) limit:** a horizontal line $P = P_{max,turbine}$.
4. **Steady-state stability limit:** the load angle $\delta = 90^\circ$ boundary, a vertical line at $Q = -V^2/X_s$ (for a cylindrical machine); a practical limit with 10 to 20 % margin is drawn inside it.
5. **Minimum-excitation / end-region heating limit:** a sloping line in the under-excited zone, limiting the leakage flux that heats the stator end iron and clamping plates when the machine absorbs vars.

Operation is allowed only inside the area bounded by all of these limits. It tells the operator how many MVAr the machine can supply or absorb for a given MW dispatch.

```figure caption="Question 4: power capability curve (per unit on rated MVA, V = 1, X_s = 1.2, rated pf 0.85 lag)."
th=np.linspace(0,np.pi,400)
fig,ax=plt.subplots(figsize=(6.2,3.9))
ax.plot(np.cos(np.linspace(0,np.pi/2,100)),np.sin(np.linspace(0,np.pi/2,100)),color=INK,lw=1.6)
ar=np.linspace(-np.pi/2-0.35,np.arctan2(0.527+0.833,0.85),200)
R=1.604
phi=np.linspace(np.arccos(0.85/R)*0+np.arctan2(0.527+0.833,0.85),np.pi/2,100)
ax.plot(R*np.cos(phi),-0.833+R*np.sin(phi),color=ACCENT,lw=1.6)
ax.plot(np.cos(np.linspace(-0.62,0,50)),np.sin(np.linspace(-0.62,0,50)),color=INK,lw=1.6)
ax.plot([0.85,0.85],[-0.53,0.527],color=SERIES[2],lw=1.6)
ax.plot([0,0.85],[-0.55,-0.55],color=SERIES[3],lw=1.6)
ax.plot([0,0.85],[0,0],color=GRID,lw=0.8); ax.axvline(0,color=GRID,lw=0.8)
ax.fill([0,0.85,0.85,0.7,0],[0,0,0.527,0.72,1],color='#e0f2fe',alpha=0.5,lw=0)
ax.set_xlim(-0.05,1.15); ax.set_ylim(-0.75,1.15); ax.set_aspect('equal')
ax.set_xlabel('P  (pu, MW)'); ax.set_ylabel('Q  (pu, MVAr)')
ax.text(0.45,0.92,'armature current limit',fontsize=7,color=INK,rotation=-27)
ax.text(0.28,0.82,'field current\nlimit',fontsize=7,color=ACCENT,ha='center')
ax.text(0.86,0.05,'turbine\nlimit',fontsize=7,color=SERIES[2]); ax.text(0.05,-0.50,'under-excited stability / end-region limit',fontsize=7,color=SERIES[3])
ax.plot([0.85],[0.527],'o',color=INK,ms=4); ax.text(0.88,0.56,'rated pf 0.85 lag',fontsize=7)
ax.text(0.1,0.3,'allowed\nregion',fontsize=8,color=MUTED)
```

@s 5
**Data.** Star connected, so $V_{ph} = 300/\sqrt3 = 173.2$ V; $X_d = 4\ \Omega$, $X_q = 3\ \Omega$; losses neglected. Rated current at unity pf:

$$I = \frac{1.5\times10^6}{\sqrt3\times300} = 2886.8\ \text{A}$$

**Step 1: load angle (motor, unity pf).** For a salient-pole motor, $\vec V = \vec E + jX_d\vec I_d + jX_q\vec I_q$. The quantity $\vec E' = \vec V - jX_q\vec I$ lies on the q-axis:

$$\begin{gathered}\vec E' = 173.2 - j(3)(2886.8) = 173.2 - j8660.3 \\ |E'| = 8662.0\ \text{V},\quad \delta = \tan^{-1}\frac{8660.3}{173.2} = 88.85^\circ\end{gathered}$$

**Step 2: components of current** (angle between $I$ and the q-axis is $\psi = \delta$):

$$\begin{gathered}I_d = I\sin\delta = 2886.2\ \text{A} \quad(\text{magnetising, leading with respect to } E) \\ I_q = I\cos\delta = 57.7\ \text{A}\end{gathered}$$

Check on the q-axis: $V\sin\delta = X_qI_q$: $173.2\times0.9998 = 173.2 = 3\times57.7$ ✓.

**Step 3: excitation emf** (d-axis equation, $V\cos\delta = E + X_dI_d$ with $I_d$ taken negative):

$$E = V\cos\delta + X_dI_d = 173.2(0.0201) + 4(2886.2) = 3.5 + 11\,544.7 \approx 11\,548\ \text{V/phase}$$

$$\boxed{E \approx 11.55\ \text{kV per phase}\ (\approx 20.0\ \text{kV line})}$$

**Step 4: maximum mechanical power for this excitation.** With losses neglected, the power developed per phase is

$$P_\phi = \frac{EV}{X_d}\sin\delta + \frac{V^2}{2}\left(\frac{1}{X_q} - \frac{1}{X_d}\right)\sin2\delta$$

$$\begin{gathered}\frac{EV}{X_d} = \frac{11\,548\times173.2}{4} = 500\,040\ \text{W} \\ \frac{V^2}{2}\left(\frac13 - \frac14\right) = \frac{173.2^2}{2}(0.08333) = 1250\ \text{W}\end{gathered}$$

Set $dP/d\delta = 0$: $500\,040\cos\delta + 2500\cos2\delta = 0 \Rightarrow \delta_{max} = 89.71^\circ$.

$$P_{max} = 3\left[500\,040\sin89.71^\circ + 1250\sin179.4^\circ\right] \approx 1.5002\times10^6\ \text{W}$$

$$\boxed{P_{max} \approx 1.50\ \text{MW}}$$

Rated load is 1.5 MW, so at this field current the motor is operating essentially **at its pull-out limit** ($\delta = 88.9^\circ$ against $\delta_{max} = 89.7^\circ$). The printed data have a synchronous-reactance drop $X_dI$ (11.5 kV) far larger than the terminal voltage (173 V), which is why the excitation is so large; the working is exactly as the data give.

@s 6
**Hunting.** When a synchronous machine is running synchronously, the rotor holds a fixed load angle $\delta$ with respect to the stator rotating field. A sudden change of load or of prime-mover torque makes the rotor swing about its new equilibrium position: it overshoots, the synchronising torque pulls it back, it overshoots the other way, and so on. This **periodic oscillation of the rotor about the synchronous speed** is called hunting (phase swinging).

**Mechanism (swing equation).**

$$J\frac{d^2\delta}{dt^2} + D\frac{d\delta}{dt} + P_s\,\delta = \Delta T$$

where the synchronising-power coefficient is

$$P_s = \frac{dP}{d\delta} = \frac{EV}{X_s}\cos\delta$$

 The natural frequency is $f_n = \dfrac{1}{2\pi}\sqrt{\dfrac{P_s}{J}}$, typically 0.5 to 2 Hz. Without damping ($D = 0$) the oscillation is sustained.

**Causes:** sudden changes in load; a prime mover with a periodic (cyclic) torque, for example a reciprocating engine; faults and switching; a large armature resistance; parallel machines with unequal governor characteristics; resonance when the pulsating torque frequency equals $f_n$.

**Harmful effects:** the current and power oscillate, so lamps flicker and bus voltage varies; the rotor and shaft suffer fatigue and cyclic stress; extra losses and heating; the machine may **fall out of step** if the swing exceeds the stability limit.

**Methods of reducing or preventing hunting:**

1. **Damper (amortisseur) windings** in the pole faces. When the rotor oscillates it moves relative to the field, and the induced currents in the bars produce a torque that opposes the relative motion (the $D$ term). This is the main remedy.
2. A suitable **flywheel** on the prime-mover shaft raises $J$ and so lowers $f_n$ away from the exciting frequency.
3. Using a prime mover with a uniform torque and a well-designed governor (no hunting of the governor itself).
4. Designing the machine with a low $X_s$ and a large air-gap (a high short-circuit ratio) to keep $P_s$ in a suitable range.
5. Laminating the pole faces and keeping the armature resistance low avoids the negative damping that large $R_a$ can give; the power-system stabiliser (PSS) in the AVR adds damping in large generators.

@s 7
**d-axis and q-axis.** The salient-pole rotor is magnetically asymmetric. The axis of the rotor field pole is the **direct axis (d-axis)**, where the air gap is smallest and the reluctance is least. The axis **90 electrical degrees** from it, along the interpolar space, is the **quadrature axis (q-axis)**, where the reluctance is largest. In the usual convention the q-axis leads the d-axis by 90° and the emf $E_f$ lies on the q-axis.

Blondel's **two-reaction theory** splits the armature current (and its mmf) into two components:

$$\begin{gathered}I_d = I\sin\psi\ \text{(along the d-axis)} \\ I_q = I\cos\psi\ \text{(along the q-axis)}\end{gathered}$$

Each component produces its own reaction flux through a different reluctance, hence two reactances:

$$\begin{gathered}X_d = X_{ad} + X_l \\ X_q = X_{aq} + X_l \\ X_d > X_q\end{gathered}$$

Phasor equation of a generator: $\vec E_f = \vec V + R_a\vec I + jX_d\vec I_d + jX_q\vec I_q$.

```figure caption="Question 7: d-axis and q-axis of a salient-pole synchronous machine and the resolution of the armature current."
fig,ax=plt.subplots(figsize=(4.6,3.3)); ax.axis('off'); ax.set_xlim(-0.4,2.2); ax.set_ylim(-0.2,2.1); ax.set_aspect('equal')
arrow(ax,(0,0),(2.0,0),'d-axis (field pole axis)',off=-0.18)
arrow(ax,(0,0),(0,1.9),'q-axis',off=-0.25)
arrow(ax,(0,0),(1.3,1.2),'$I$',color=ACCENT,off=0.15)
arrow(ax,(0,0),(1.3,0),'$I_d$',color=SERIES[2],off=0.15); arrow(ax,(0,0),(0,1.2),'$I_q$',color=SERIES[3],off=0.15)
ax.plot([1.3,1.3],[0,1.2],ls=':',color=MUTED); ax.plot([0,1.3],[1.2,1.2],ls=':',color=MUTED)
ax.add_patch(Arc((0,0),0.9,0.9,theta1=0,theta2=42.7,color=INK)); ax.text(0.55,0.16,'$\\theta=90^\\circ-\\psi$',fontsize=7.5)
```

**Why the dq0 reference frame is needed.**

1. In the a-b-c frame the stator-rotor mutual and self inductances of a salient-pole machine vary with the rotor angle $\theta$ (terms in $\cos\theta$, $\cos2\theta$), so the voltage equations are **time-varying differential equations** that cannot be solved easily.
2. Park's transformation refers all stator quantities to axes fixed to the **rotor**. In the dq frame the inductances become **constants** and sinusoidal steady state becomes d.c. quantities, which makes transient analysis, stability studies, control (field-oriented control) and simulation straightforward.
3. Balanced three-phase currents appear as two d.c. quantities $i_d, i_q$; the third axis, **zero-sequence ($0$)**, carries the unbalanced (zero-sequence) part, so the transformation also handles unbalanced faults. It is power invariant if scaled by $\sqrt{2/3}$.

$$\begin{bmatrix}f_d\\f_q\\f_0\end{bmatrix} = \frac23\begin{bmatrix}\cos\theta & \cos(\theta-120^\circ) & \cos(\theta+120^\circ)\\ -\sin\theta & -\sin(\theta-120^\circ) & -\sin(\theta+120^\circ)\\ \tfrac12 & \tfrac12 & \tfrac12\end{bmatrix}\begin{bmatrix}f_a\\f_b\\f_c\end{bmatrix}$$

The dq voltage equations $v_d = Ri_d + \dot\lambda_d - \omega\lambda_q$, $v_q = Ri_q + \dot\lambda_q + \omega\lambda_d$ and torque $T = \tfrac32\tfrac P2(\lambda_di_q - \lambda_qi_d)$ then have constant coefficients.

@s 8
**Data.** $V = 230\angle0^\circ$ V, 50 Hz; $Z_m = 7 + j5 = 8.60\angle35.54^\circ\ \Omega$; $Z_a = 11.5 + j5\ \Omega$; capacitor $X_c$ in series with the auxiliary winding.

**Currents.** $\vec I_m = \dfrac{230}{7 + j5} = 26.74\angle{-35.54^\circ}$ A (lagging $V$ by $\theta_m = 35.54^\circ$).

For quadrature the auxiliary current must lead $I_m$ by $90^\circ$, i.e. $\vec I_a$ at $-35.54^\circ + 90^\circ = +54.46^\circ$, a **leading** current of angle $\theta_a = 54.46^\circ$:

$$\begin{gathered}\vec I_a = \frac{230}{11.5 + j(5 - X_c)} \\ \tan\theta_a = \frac{X_c - 5}{11.5}\end{gathered}$$

$$\begin{gathered}\frac{X_c - 5}{11.5} = \tan54.46^\circ = 1.4000 \\ X_c = 5 + 11.5\times1.4 = 21.1\ \Omega\end{gathered}$$

$$\boxed{C = \frac{1}{2\pi fX_c} = \frac{1}{2\pi\times50\times21.1} = 1.509\times10^{-4}\ \text{F} \approx 151\ \mu\text{F}}$$

**Check:** $Z_a' = 11.5 - j16.1 = 19.78\angle{-54.46^\circ}$, $\vec I_a = 11.62\angle54.46^\circ$ A; phase difference with $I_m$ is $54.46 + 35.54 = 90.0^\circ$ ✓. Line current $\vec I_m + \vec I_a = 29.15\angle{-12.0^\circ}$ A.

```figure caption="Question 8: capacitor-start motor circuit (left) and phasor diagram (right) with I_a leading I_m by 90 degrees."
fig,axs=plt.subplots(1,2,figsize=(6.8,3.0),gridspec_kw={'width_ratios':[1.15,1]})
ax=axs[0]; ax.axis('off'); ax.set_xlim(-1.0,6.2); ax.set_ylim(-0.3,3.6)
vsrc(ax,(0,0.2),(0,3.0),'230 V, 50 Hz',side=-1,off=0.95)
wire(ax,[(0,3.0),(0.8,3.0)]); res(ax,(0.8,3.0),(2.9,3.0),'main winding $Z_m$',side=1,body=1.2); wire(ax,[(2.9,3.0),(5.0,3.0),(5.0,0.2)])
wire(ax,[(0.8,3.0),(0.8,1.6)]); node(ax,(0.8,3.0)); wire(ax,[(0.8,1.6),(1.1,1.6)])
cap(ax,(1.1,1.6),(1.8,1.6),'C',side=1,gap=0.12); res(ax,(1.8,1.6),(3.2,1.6),'aux. winding $Z_a$',side=-1,body=1.0)
switch(ax,(3.2,1.6),(4.1,1.6),'centrifugal switch',side=1,off=0.5); wire(ax,[(4.1,1.6),(5.0,1.6)]); node(ax,(5.0,1.6))
wire(ax,[(0,0.2),(5.0,0.2)])
ax=axs[1]; ax.axis('off'); ax.set_xlim(-0.5,2.6); ax.set_ylim(-1.3,2.4); ax.set_aspect('equal')
r=np.radians
arrow(ax,(0,0),(2.1,0),'$V$',off=0.12)
arrow(ax,(0,0),(1.9*np.cos(r(-35.54)),1.9*np.sin(r(-35.54))),'$I_m$',color=ACCENT,off=0.15)
arrow(ax,(0,0),(1.2*np.cos(r(54.46)),1.2*np.sin(r(54.46))),'$I_a$',color=SERIES[2],off=0.15)
ax.add_patch(Arc((0,0),0.8,0.8,theta1=-35.5,theta2=54.5,color=INK)); ax.text(0.5,0.05,'$90^\\circ$',fontsize=8)
arrow(ax,(0,0),(1.9*np.cos(r(-35.54))+1.2*np.cos(r(54.46)),1.9*np.sin(r(-35.54))+1.2*np.sin(r(54.46))),'$I_{line}$',color=SERIES[3],off=0.15)
ax.text(1.5,-1.15,'$I_m$ lags $V$ by $35.5^\\circ$,  $I_a$ leads $V$ by $54.5^\\circ$',fontsize=7,ha='center')
```

@s 9
**BLDC (permanent-magnet brushless d.c.) motor.** The rotor carries permanent magnets; the stator has a three-phase concentrated winding with a **trapezoidal back-emf** (flat-top 120° electrical). The phases are switched by an inverter using Hall-sensor rotor-position signals so that, at any instant, **two phases conduct** (120° conduction) and the third is off.

**Back-emf constant.** For a rotor of radius $r$, stack length $l$, air-gap flux density $B$, $N_{ph}$ turns per phase (full-pitch, flat-top): the emf of one phase during its flat top is

$$\begin{gathered}E = 2N_{ph}Blr\,\omega_m = k_e\,\omega_m\quad(\text{V per phase}) \\ k_e = 2N_{ph}Blr\end{gathered}$$

**Torque.** Neglecting losses, the electromagnetic power is the sum of the products of back-emf and current in each phase:

$$P_e = e_ai_a + e_bi_b + e_ci_c$$

In the 120° conduction interval with phases A and B on: $e_a = +E,\ i_a = +I;\ e_b = -E,\ i_b = -I;\ i_c = 0$:

$$P_e = EI + EI = 2EI = 2k_e\omega_mI$$

$$T_e = \frac{P_e}{\omega_m}\ \Rightarrow\ \boxed{T_e = 2k_eI = 4N_{ph}BlrI = k_tI}$$

The torque is proportional to the current, like a d.c. motor, with torque constant $k_t = 2k_e$ (N m/A); it is nearly ripple-free because every 60° the next pair of phases takes over at the flat top of the emf.

**Voltage equation (two phases in series across the d.c. link $V_{dc}$):**

$$V_{dc} = 2E + 2RI = 2k_e\omega_m + 2RI$$

**Torque-speed characteristic.** Eliminating $I = T/(2k_e)$:

$$\boxed{\omega_m = \frac{V_{dc}}{2k_e} - \frac{R}{2k_e^2}\,T_e}$$

This is a **straight line** (as in a separately excited d.c. motor).

- No-load speed: $\omega_0 = V_{dc}/(2k_e)$ (at $T = 0$).
- Stall (starting) torque: $T_s = k_eV_{dc}/R$ (at $\omega_m = 0$, $I_s = V_{dc}/2R$).
- Speed regulation is small, speed is controlled by $V_{dc}$ (PWM), and the line shifts parallel to itself for different $V_{dc}$.
- The practical operating region is limited by the **continuous (rated) torque** (thermal limit of the winding) and the **peak (intermittent) torque** (set by the inverter current limit and magnet demagnetisation); above the base speed the supply voltage limit applies unless field weakening (phase advance) is used.

```figure caption="Question 9: BLDC torque-speed characteristic for several d.c. link voltages, with continuous and peak torque limits."
fig,ax=plt.subplots(figsize=(5.4,3.2))
for v,c in zip((1.0,0.75,0.5),SERIES[:3]):
    ax.plot([0,1.0],[v,0],color=c,lw=1.7,label='$V_{dc}$ = %.2f $V_{rated}$'%v)
ax.axvline(0.55,color=ACCENT,ls='--',lw=1); ax.text(0.56,0.05,'continuous torque limit',fontsize=7,color=ACCENT,rotation=90)
ax.axvline(0.85,color=SERIES[3],ls=':',lw=1); ax.text(0.86,0.05,'peak torque limit',fontsize=7,color=SERIES[3],rotation=90)
ax.set_xlabel('torque  $T_e$  (pu of stall torque)'); ax.set_ylabel('speed  (pu of no-load speed)'); ax.set_xlim(0,1.05); ax.set_ylim(0,1.1); ax.legend(loc='upper right',fontsize=7)
```

@s 10
**Switched reluctance motor (SRM).** A **doubly-salient** machine with **no winding and no magnet on the rotor**; torque comes only from the tendency of the rotor to move to the position of minimum reluctance (maximum inductance) with respect to the energised stator pole pair.

**Construction**

- **Stator:** laminated silicon-steel core with salient poles; a concentrated coil on each pole, diametrically opposite coils connected in series (or parallel) to form one **phase**. Common arrangements: 6/4 (3-phase, 6 stator poles, 4 rotor poles) and 8/6 (4-phase).
- **Rotor:** a laminated stack with salient poles only, no conductors, no brushes, no slip rings; it is simple, light, cheap and robust and has a low inertia.
- **Rotor position sensor** (optical encoder, Hall or resolver; or sensorless estimation) gives the position for commutation.
- **Power converter:** asymmetric half-bridge per phase (two switches and two diodes) that applies $+V_{dc}$, zero volts or $-V_{dc}$ to the phase.

**Working principle**

1. When a stator phase is excited, flux flows through the stator poles and the nearest rotor poles. The rotor feels a force that tries to align the rotor poles with the energised stator poles (minimum reluctance, **maximum inductance $L_{max}$**).
2. The torque per phase is

$$T = \tfrac12\,i^2\,\frac{dL(\theta)}{d\theta}$$

The sign of the torque depends only on the sign of $dL/d\theta$, **not on the direction of current**, so unipolar current pulses suffice.
3. A phase is switched ON (at turn-on angle $\theta_{on}$) while the rotor pole is approaching the stator pole, where $dL/d\theta > 0$, giving **motoring torque**. It is switched OFF (at $\theta_{off}$) before alignment so that the current decays before $dL/d\theta$ becomes negative (generating or braking torque).
4. The phases are excited in sequence (A, B, C, A, ...); the overlap of successive pulses gives a continuous rotation. Reversal is obtained by reversing the phase sequence. The step angle is $\varepsilon = \dfrac{360^\circ}{m\,N_r}$ ($15^\circ$ for 3-phase 6/4).
5. Speed is controlled by the d.c. link voltage, by the turn-on/off angles, and by chopping the current (hysteresis or PWM) at low speed.

**Features:** simple robust rotor, fault-tolerant (phases are independent), high starting torque, high speed and efficiency, a wide constant-power range; drawbacks are the **torque ripple, acoustic noise and vibration**, the need for a position sensor and a special converter. **Applications:** electric vehicles, fans and compressors, washing machines and vacuum cleaners, aircraft starter-generators, textile and mining drives.

```figure caption="Question 10: phase inductance against rotor angle; positive torque (motoring) is produced while the inductance rises."
fig,ax=plt.subplots(figsize=(5.6,2.9))
th=np.linspace(0,90,400); L=np.where(th<20,0.2,np.where(th<45,0.2+0.8*(th-20)/25,np.where(th<65,1.0,np.where(th<90,1.0-0.8*(th-65)/25,0.2))))
ax.plot(th,L,color=INK,lw=1.8,label='$L(\\theta)$')
ax.axvspan(20,45,color='#dcfce7',alpha=0.8); ax.axvspan(65,90,color='#fee2e2',alpha=0.8)
ax.text(32,0.1,'$dL/d\\theta>0$\nmotoring',fontsize=7.5,ha='center'); ax.text(77,0.1,'$dL/d\\theta<0$\nbraking',fontsize=7.5,ha='center')
ax.axvline(25,color=ACCENT,ls='--',lw=1); ax.text(25.5,1.08,'$\\theta_{on}$',fontsize=8,color=ACCENT); ax.axvline(42,color=ACCENT,ls='--',lw=1); ax.text(42.5,1.08,'$\\theta_{off}$',fontsize=8,color=ACCENT)
ax.text(8,0.28,'unaligned\n$L_{min}$',fontsize=7); ax.text(51,1.04,'aligned $L_{max}$',fontsize=7)
ax.set_xlabel('rotor angle  $\\theta$  (degrees)'); ax.set_ylabel('inductance (pu)'); ax.set_ylim(0,1.25)
```

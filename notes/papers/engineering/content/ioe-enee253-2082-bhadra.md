---
file: NEBians-IOE-Past-Paper-Electrical-Machine-II-ENEE253-2082-Bhadra.pdf
subject: Electrical Machine II
level: BE · Year II / Part II
code: ENEE 253
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE Electrical Engineering (BEL), Year II / Part II. Full marks 30, pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
Describe the constructional details of 3φ synchronous machine. [[3]]

@q 2
What do mean by armature reaction? How does armature reaction vary in a synchronous generator when supplying loads at different power factors? [[3]]

@q 3
Two station generators A and B operate in parallel. Station capacity of A is 50 MW and that of B is 25 MW. Full load speed regulation of station A is 3% and B is 3.5%. Calculate the load sharing if the connected load is 50 MW, no load frequency is 50 Hz. Comment on the answer. [[3]]

@q 4
With the help of relevant curves and diagram, explain the Potier method for determining the voltage regulation of a synchronous generator. [[4]]

@q 5
Define excitation system in synchronous motor. Explain briefly with neat phasor diagram about the effect of changing excitation with constant load in synchronous motor. [[3]]

@q 6
A 3 phase, 100 hp, 440 V, star connected synchronous motor has a synchronous impedance per phase of 0.1 + j1 Ω. The excitation and torque losses are 4 kW and may be assumed constant. Calculate the current, power factor and efficiency when operating at full load with an excitation equivalent to 400 line volts. [[3]]

@q 7
Write 3 advantages of abc to dq0 transformation. Prove that I$_{abc}$ = [T] i$_{dq0}$ [[3]]

@q 8
At starting, the windings of a 230 V, 50 Hz, split-phase induction motor have the following parameters: [[3]]

Main winding: R = 4 Ω; X$_1$ = 7.5 Ω. Starting winding: R = 7.5 Ω; X$_1$ = 4 Ω. Find

a) Current in the main winding

b) Current in the starting winding

c) Phase angle between I$_s$ and I$_m$

d) Line current and

e) Power factor of the motor.

@q 9
Describe operating principle and characteristics of shaded pole single phase motor with necessary diagrams. [[2]]

@q 10
What are the constructional features of brushless DC motor? How is it different from induction motor? State two applications of BLDC motor. [[3]]

<!-- SOLUTIONS -->

@s 1
**Three-phase synchronous machine: constructional details.**

**1. Stator (armature)**

- *Frame:* welded steel or cast iron; carries the core, provides ventilation passages and mechanical protection.
- *Core:* stacked 0.35 to 0.5 mm silicon-steel laminations, insulated by varnish, with radial cooling ducts; low hysteresis and eddy-current loss.
- *Slots and winding:* open or semi-closed slots hold a three-phase double-layer, short-pitched, distributed winding. Phases are normally star connected with the neutral grounded (directly or through impedance).

**2. Rotor (field)** carries the d.c.-excited field winding, supplied through two slip rings and brushes (or a brushless exciter). Two forms are used:

- **Salient pole:** projecting laminated poles with concentrated field coils and pole-face damper bars; large diameter, short length; low speed (hydro, diesel sets).
- **Cylindrical (round) rotor:** solid forged-steel cylinder with slots for a distributed field winding, held by steel wedges and retaining rings; small diameter, long length; high speed, 2 or 4 poles (turbo-alternators).

**3. Auxiliaries:** the exciter (d.c. generator or static rectifier, 0.5 to 2 % of the rating), bearings, shaft, cooling system (air, hydrogen or water) and the damper (amortisseur) winding for stability and for self-starting as a motor.

The speed of the machine is $N_s = 120f/P$ rpm, rigidly tied to the supply frequency.

@s 2
**Armature reaction.** The effect of the **armature (stator) mmf on the main field flux** is called armature reaction. A loaded alternator has a current-carrying armature winding that sets up a rotating mmf $F_a$ which rotates at synchronous speed, so it is stationary with respect to the field mmf $F_f$. The resultant air-gap flux is the phasor sum of the two, so its magnitude, distribution and position change with the load current and the power factor.

The effect depends on the phase angle $\psi$ between the load current and the induced emf $E_f$ (which itself is $90^\circ$ behind the flux $\Phi_f$):

| Load power factor | Angle between $I$ and $E_f$ | Armature reaction | Effect on terminal voltage |
|---|---|---|---|
| Unity pf | $0^\circ$ ($I$ in phase with $E_f$) | **Cross-magnetising**: $F_a$ is $90^\circ$ to the field axis; it distorts the flux (strengthens one pole tip, weakens the other); net flux nearly unchanged but slightly reduced by saturation | Small drop, caused mainly by $R_a$ and the distortion |
| Zero pf lagging (inductive load) | $90^\circ$ lag | **Demagnetising**: $F_a$ directly opposes $F_f$, so the flux is reduced | Large fall in terminal voltage (poor regulation) |
| Zero pf leading (capacitive load) | $90^\circ$ lead | **Magnetising**: $F_a$ aids $F_f$, flux strengthened | Terminal voltage **rises** (Ferranti-type effect; negative regulation) |
| Intermediate lagging pf | $0 < \psi < 90^\circ$ lag | Partly demagnetising + partly cross-magnetising | Drop, increasing as the pf falls |
| Intermediate leading pf | $0 < \psi < 90^\circ$ lead | Partly magnetising + cross-magnetising | Smaller drop or a rise |

The reaction is represented by an equivalent reactance, the armature-reaction reactance $X_a$ in series with the leakage reactance $X_l$ to give the synchronous reactance $X_s = X_a + X_l$, and $\vec E_f = \vec V + \vec I(R_a + jX_s)$.

```figure caption="Question 2: phasor diagrams of a generator at (a) lagging, (b) unity and (c) leading power factor; E_f = V + I(R_a + jX_s)."
fig,axs=plt.subplots(1,3,figsize=(6.8,2.5))
r=np.radians
for ax,(phi,t) in zip(axs,((-36.9,'(a) lagging pf'),(0,'(b) unity pf'),(36.9,'(c) leading pf'))):
    ax.axis('off'); ax.set_xlim(-0.2,2.0); ax.set_ylim(-0.9,1.6); ax.set_aspect('equal'); ax.set_title(t,fontsize=8)
    V=1.0; I=0.55*np.exp(1j*r(phi)); Z=0.1+0.7j
    E=V+I*Z*1.5
    arrow(ax,(0,0),(V,0),'$V$',off=-0.15)
    arrow(ax,(0,0),(I.real*1.0,I.imag*1.0),'$I$',color=SERIES[2],off=0.1)
    A=V+I*0.1*1.5; arrow(ax,(V,0),(A.real,A.imag),None,color=MUTED)
    arrow(ax,(A.real,A.imag),(E.real,E.imag),None,color=SERIES[3])
    arrow(ax,(0,0),(E.real,E.imag),'$E_f$',color=ACCENT,off=0.12)
    ax.text(0.5*(V+E.real),0.5*E.imag+0.2 if phi<=0 else 0.5*E.imag-0.25,'$IR_a$, $jIX_s$',fontsize=6.5,color=MUTED)
```

@s 3
**Droop characteristics** (frequency falls linearly from the no-load value $f_0 = 50$ Hz to full-load frequency):

$$\begin{gathered}\text{Station A: } \Delta f_{FL} = 0.03\times50 = 1.5\ \text{Hz over } 50\ \text{MW} \ \Rightarrow\ R_A = 0.03\ \text{Hz/MW} \\ \text{Station B: } \Delta f_{FL} = 0.035\times50 = 1.75\ \text{Hz over } 25\ \text{MW} \ \Rightarrow\ R_B = 0.07\ \text{Hz/MW}\end{gathered}$$

Both machines run at the same system frequency, so

$$\begin{gathered}f = 50 - R_AP_A = 50 - R_BP_B \\ P_A + P_B = 50\ \text{MW}\end{gathered}$$

$$\begin{gathered}0.03P_A = 0.07(50 - P_A) \ \Rightarrow\ 0.10P_A = 3.5 \\ \boxed{P_A = 35\ \text{MW},\qquad P_B = 15\ \text{MW}}\end{gathered}$$

$$f = 50 - 0.03\times35 = \mathbf{48.95\ Hz}\quad(\text{check: } 50 - 0.07\times15 = 48.95)$$

**Comment.** Station A (50 MW) supplies 35 MW, i.e. **70 %** of its rating, while B (25 MW) supplies 15 MW, i.e. **60 %**. The set with the smaller regulation (steeper-flatter characteristic, A) takes the larger fraction of its rating; neither is overloaded, and the system frequency falls to 48.95 Hz, which is below the normal band of about 49.5 Hz (a 2.1 % drop), so a secondary control action (raising the governor speed-changer settings) is required to restore 50 Hz. The loads are not shared strictly in proportion to the ratings because the regulations differ (3 % against 3.5 %); equal percentage regulation would give an exactly proportional share (33.3 MW and 16.7 MW).

@s 4
**Potier method** is the most accurate of the indirect (synthetic) methods of finding the regulation of a cylindrical-rotor alternator. It separates the armature leakage-reactance drop from the armature-reaction mmf, and it takes the saturation of the magnetic circuit into account (the emf method does not, so it is pessimistic).

**Data needed from tests**

1. **Open-circuit characteristic (OCC):** the generated emf against the field current $I_f$ at rated speed.
2. **Zero-power-factor-lagging (ZPF) characteristic at full-load current:** the terminal voltage against $I_f$ with the machine delivering rated armature current into a purely inductive load (or over-excited synchronous motor), at rated speed. It has the shape of the OCC shifted to the right and down.
3. The armature resistance $R_a$ (d.c. test).

**Construction of the Potier triangle**

1. Draw the OCC and the ZPF curve on the same axes.
2. Through the point $A$ on the ZPF where the terminal voltage is rated, draw a **horizontal** line $AB$ (parallel to the $I_f$ axis) whose length equals the field current $I_{f,sc}$ that circulates full-load current on a short circuit (the point where the ZPF curve meets the $V = 0$ axis).
3. From $B$ draw $BC$ parallel to the initial straight part (the air-gap line) of the OCC, to meet the OCC at $C$. Drop the perpendicular $CD$ onto $AB$.
4. $\triangle ACD$ (or $BCD$) is the **Potier triangle**: $CD$ (vertical) gives the **leakage-reactance drop $IX_p$** (the *Potier reactance* $X_p \approx X_l$ in volts per phase) and $BD$ (horizontal) gives the **armature-reaction field current $I_{fa}$** (the field current that balances the armature-reaction mmf at full load). Thus

$$\begin{gathered}X_p = \frac{CD}{I_{rated}}\ \ (\text{per phase}) \\ I_{fa} = BD\end{gathered}$$

**Finding the regulation at any load (rated current, pf $\cos\varphi$ lagging)**

1. Compute the voltage behind the leakage reactance: $\vec E_1 = \vec V + \vec I(R_a + jX_p)$.
2. From the OCC read the field current $I_{f1}$ that produces $E_1$ (the field current needed for the air-gap flux).
3. Add the armature-reaction field current $I_{fa}$ **at the correct angle**: $I_{fa}$ is drawn at an angle $(90^\circ + \psi)$ ahead of $I_{f1}$, where $\psi$ is the angle between $I$ and $E_1$. Since $I_{f1}$ leads $E_1$ by $90^\circ$ and $I_{fa}$ is in phase with $I$:

$$\vec I_{f} = \vec I_{f1} + \vec I_{fa}\quad\text{(phasor sum)}$$

4. The resultant field current $I_f$ gives, on the OCC, the **no-load emf $E_0$** corresponding to the load that has been removed (field current unchanged).
5. **Voltage regulation:**

$$\text{Regulation} = \frac{E_0 - V}{V}\times100\ \%$$

**Why it is accurate:** the leakage reactance and the armature reaction are separated, and the saturation is accounted for through the OCC at the actual air-gap flux. The result is usually within a few per cent of the actual value for cylindrical-rotor machines (for salient-pole machines the two-reaction method is preferred).

```figure caption="Question 4: OCC and full-load ZPF characteristic with the Potier triangle BCD (schematic)."
fig,ax=plt.subplots(figsize=(5.8,3.8))
occ=lambda x:1.68*np.tanh(x/6.2)
x=np.linspace(0,10,300)
ax.plot(x,occ(x),color=INK,lw=1.8,label='OCC')
sh=(1.2,-0.217)
xz=x[x>=sh[0]]; ax.plot(xz,occ(xz-sh[0])+sh[1],color=ACCENT,lw=1.8,label='ZPF at full-load current')
ax.plot([0,6],[0,0.271*6],color=MUTED,ls='--',lw=1,label='air-gap line')
V=1.0; xc=6.2*np.arctanh((V+0.217)/1.68); xb=xc-0.8; xa=xb+2.0
ax.axhline(V,color=GRID,lw=0.8); ax.text(0.1,V+0.03,'rated V',fontsize=7)
ax.plot([xb,xa],[V,V],color=SERIES[3],lw=2.0)
ax.plot([xc,xc],[V,V+0.217],color=SERIES[2],lw=2.2)
ax.plot([xb,xc],[V,V+0.217],color=MUTED,lw=1.0)
ax.plot([xa,xb,xc,xc],[V,V,V+0.217,V],'o',color=INK,ms=3)
ax.text(xa+0.1,V-0.09,'A',fontsize=8); ax.text(xb-0.3,V-0.09,'B',fontsize=8); ax.text(xc-0.15,V+0.25,'C',fontsize=8); ax.text(xc+0.05,V-0.1,'D',fontsize=8)
ax.text(xc+0.12,V+0.07,'$CD=IX_p$',fontsize=7,color=SERIES[2]); ax.text(xb-1.0,V-0.2,'$BD=I_{fa}$',fontsize=7,color=SERIES[3]); ax.text(xb+0.6,V-0.28,'$AB$ = field current for full-load short circuit',fontsize=6.5,color=SERIES[3],ha='left')
ax.set_xlabel('field current  $I_f$  (A)'); ax.set_ylabel('terminal voltage / emf (pu)'); ax.set_xlim(0,10); ax.set_ylim(0,1.5); ax.legend(loc='lower right',fontsize=7)
```

@s 5
**Excitation system.** The **excitation system** of a synchronous machine is the equipment that supplies the d.c. field current to the rotor: a main exciter (a d.c. generator on the shaft, or a static/brushless a.c. exciter with rectifier), the field rheostat or automatic voltage regulator (AVR) controlling the field current, the slip rings and brushes (or rotating diodes), and the field-suppression and protection equipment. In a synchronous motor it also supplies the d.c. field for pull-in and runs the motor as an **adjustable power-factor machine**.

**Effect of changing excitation at constant load (constant $P$, constant $V$, constant $f$).** The input power is fixed, so $P = 3VI\cos\varphi = $ const, i.e. the active component $I\cos\varphi$ is constant, and, since $P = \dfrac{3EV}{X_s}\sin\delta$ is constant, $E\sin\delta$ is constant. The tip of $\vec E$ therefore moves along a **horizontal line** and the tip of $\vec I$ along a **vertical line** as the field current is changed:

- **Normal excitation:** $E\cos\delta = V$ (about); $I$ is a minimum and the pf is **unity**.
- **Under-excited** ($E$ smaller): the motor needs reactive power from the supply; $I$ is larger and **lagging** (inductive load, like an inductor or resistor-inductor).
- **Over-excited** ($E$ larger): the motor delivers reactive power to the supply; $I$ is larger and **leading** (like a capacitor). The motor then acts as a power-factor corrector or synchronous condenser.

The plot of $I_a$ against $I_f$ is the **V-curve** (minimum at unity pf); the plot of pf against $I_f$ is the inverted V-curve. The stability limit ($\delta = 90^\circ$) is reached when excitation is reduced too far.

```figure caption="Question 5: synchronous motor phasors at constant load for three excitation levels: the locus of E is a horizontal line (E sin(delta) constant) and the active part of I is constant."
fig,ax=plt.subplots(figsize=(5.8,3.4)); ax.axis('off'); ax.set_xlim(-0.6,4.0); ax.set_ylim(-1.5,1.3); ax.set_aspect('equal')
v=2.0; Xs=1.0; Ip=0.9
arrow(ax,(0,0),(v,0),'$V$',off=0.14)
for Iq,c,l in ((-0.8,SERIES[3],'under-excited, lagging I'),(0.0,SERIES[2],'normal, unity pf'),(0.8,ACCENT,'over-excited, leading I')):
    I=Ip+1j*Iq; E=v-1j*Xs*I
    arrow(ax,(0,0),(I.real,I.imag),None,color=c,lw=1.0)
    arrow(ax,(0,0),(E.real,E.imag),None,color=c,lw=1.5)
    arrow(ax,(E.real,E.imag),(v,0),None,color=c,lw=1.0)
    ax.text(E.real,E.imag-0.16,'$E$: '+l,fontsize=6.6,color=c,ha='center')
ax.axhline(-Xs*Ip,color=GRID,ls=':',lw=0.8); ax.text(3.9,-Xs*Ip+0.05,'locus of $E$',fontsize=6.5,ha='right',color=MUTED)
ax.axvline(Ip,color=GRID,ls=':',lw=0.8); ax.text(Ip+0.04,1.1,'locus of $I$',fontsize=6.5,color=MUTED)
```

@s 6
**Data.** Star-connected: $V_{ph} = 440/\sqrt3 = 254.03$ V; $E_{ph} = 400/\sqrt3 = 230.94$ V; $Z_s = 0.1 + j1\ \Omega$ ($Z_s = 1.005\ \Omega$, $\theta_z = 84.29^\circ$). Output $= 100\ \text{hp} = 100\times746 = 74.6$ kW. The excitation and torque (windage, friction, core) losses of 4 kW are constant and are taken as the part of the developed power that does not reach the shaft:

$$\begin{gathered}P_{dev} = 74.6 + 4 = 78.6\ \text{kW} \\ P_{dev,\ per\ phase} = 26.2\ \text{kW}\end{gathered}$$

**Load angle.** For a motor $\vec I = \dfrac{\vec V - \vec E}{Z_s}$, with $\vec E = E\angle{-\delta}$, so the power developed per phase is

$$P_{dev} = \frac{EV}{Z_s}\cos(\theta_z - \delta) - \frac{E^2}{Z_s}\cos\theta_z$$

$$\begin{gathered}\frac{E^2}{Z_s}\cos\theta_z = \frac{230.94^2}{1.005}(0.0995) = 5280\ \text{W} \\ \frac{EV}{Z_s} = \frac{230.94\times254.03}{1.005} = 58\,375\ \text{W}\end{gathered}$$

$$\begin{gathered}58\,375\cos(84.29^\circ - \delta) = 26\,200 + 5280 = 31\,480 \\ 84.29^\circ - \delta = 57.37^\circ \ \Rightarrow\ \delta = 26.92^\circ\end{gathered}$$

**Armature current.**

$$\begin{gathered}\vec E = 230.94\angle{-26.92^\circ} = 205.99 - j104.54\ \text{V} \\ \vec V - \vec E = 48.04 + j104.54 = 115.05\angle65.3^\circ\ \text{V}\end{gathered}$$

$$\vec I = \frac{115.05\angle65.3^\circ}{1.005\angle84.29^\circ} = 114.5\angle{-19.0^\circ}\ \text{A}$$

$$\boxed{I = 114.5\ \text{A (line = phase)},\qquad \cos\varphi = \cos19.0^\circ = 0.9455\ \text{lagging}}$$

(The motor is under-excited, since $E < V$, so it draws a lagging current.)

**Efficiency.**

$$\begin{gathered}\text{Armature copper loss} = 3I^2R_a = 3(114.5)^2(0.1) = 3936\ \text{W} \\ \text{Input} = 74\,600 + 4000 + 3936 = 82\,536\ \text{W}\end{gathered}$$

$$\text{Check: } \sqrt3\times440\times114.5\times0.9455 = 82.5\ \text{kW}\ \checkmark$$

$$\boxed{\eta = \frac{74.6}{82.54}\times100 = 90.4\ \%}$$

@s 7
**Three advantages of the abc to dq0 (Park) transformation**

1. It converts the **time-varying** inductances of a salient-pole machine (which depend on $\theta$) into **constants**, so the machine equations become ordinary linear differential equations with constant coefficients.
2. Balanced sinusoidal a.c. quantities become **d.c. quantities** ($i_d$, $i_q$), so PI controllers can be used (vector / field-oriented control) and the steady state is an equilibrium point instead of an oscillation.
3. The three-phase system is reduced to **decoupled axes**: $d$ and $q$ (flux and torque producing parts) and the zero-sequence axis ($0$) for unbalance, which simplifies fault, stability and transient studies; the transformation (power-invariant form) preserves power, $p = v_di_d + v_qi_q + v_0i_0$.

**Proof of $\mathbf{I_{abc} = [T]\,I_{dq0}}$.** Let the d-axis be at angle $\theta$ from the a-axis, with the phase axes at $\theta$, $\theta-120^\circ$ and $\theta+120^\circ$ electrical from the d-axis. The Park (forward) transformation, with $k = 2/3$, is

$$[T_{dq0}] = \frac23\begin{bmatrix}\cos\theta & \cos(\theta-120^\circ) & \cos(\theta+120^\circ)\\ -\sin\theta & -\sin(\theta-120^\circ) & -\sin(\theta+120^\circ)\\ \tfrac12 & \tfrac12 & \tfrac12\end{bmatrix},\qquad I_{dq0} = [T_{dq0}]\,I_{abc}$$

We show that it has the inverse

$$[T] = \begin{bmatrix}\cos\theta & -\sin\theta & 1\\ \cos(\theta-120^\circ) & -\sin(\theta-120^\circ) & 1\\ \cos(\theta+120^\circ) & -\sin(\theta+120^\circ) & 1\end{bmatrix}$$

*Physical derivation.* The phase current $i_a$ is the sum of the projections of the rotating-axis components on the a-axis plus the zero-sequence current, because the d- and q-axes are at angles $\theta$ and $\theta + 90^\circ$ from a:

$$i_a = i_d\cos\theta - i_q\sin\theta + i_0$$

Similarly for b and c, with $\theta$ replaced by $\theta - 120^\circ$ and $\theta + 120^\circ$. In matrix form this is exactly $I_{abc} = [T]\,I_{dq0}$.

*Check by multiplication:* $[T_{dq0}][T] = [U]$. Using $\cos^2\theta + \cos^2(\theta-120^\circ) + \cos^2(\theta+120^\circ) = \tfrac32$, $\sin\theta\cos\theta + \dots = 0$ and $\cos\theta + \cos(\theta-120^\circ) + \cos(\theta+120^\circ) = 0$:

$$\begin{gathered}(1,1):\ \tfrac23\left(\tfrac32\right) = 1 \quad(1,2):\ \tfrac23\left(-\sum\cos\theta_k\sin\theta_k\right) = 0 \quad(1,3):\ \tfrac23\sum\cos\theta_k = 0 \\ (3,3):\ \tfrac23\cdot\tfrac12\cdot3 = 1\end{gathered}$$

and all off-diagonal terms vanish, so $[T_{dq0}][T] = [U]$, i.e. $[T] = [T_{dq0}]^{-1}$ and therefore

$$\boxed{I_{abc} = [T]\,I_{dq0}}$$

@s 8
**Data.** $V = 230\angle0^\circ$ V at starting (both windings are across the supply).

Main winding: $Z_m = 4 + j7.5 = 8.5\angle61.93^\circ\ \Omega$. Starting winding: $Z_s = 7.5 + j4 = 8.5\angle28.07^\circ\ \Omega$.

**(a) Current in the main winding**

$$\vec I_m = \frac{230}{8.5\angle61.93^\circ} = 27.06\angle{-61.93^\circ}\ \text{A}$$

**(b) Current in the starting winding**

$$\vec I_s = \frac{230}{8.5\angle28.07^\circ} = 27.06\angle{-28.07^\circ}\ \text{A}$$

**(c) Phase angle between $I_s$ and $I_m$**

$$\alpha = 61.93^\circ - 28.07^\circ = \mathbf{33.86^\circ}\quad(I_s\ \text{leads}\ I_m)$$

**(d) Line current**

$$\begin{gathered}\vec I_L = \vec I_m + \vec I_s = (12.72 - j23.89) + (23.88 - j12.74) \\ = 36.60 - j36.63 = \mathbf{51.77\angle{-45.0^\circ}\ A}\end{gathered}$$

Check with the magnitude formula for two equal currents displaced by $\alpha$:

$$I_L = 2I\cos\frac{\alpha}{2} = 2(27.06)\cos16.93^\circ = 51.77\ \text{A}\ \checkmark$$

**(e) Power factor**

$$\cos\varphi = \cos45.0^\circ = \mathbf{0.707\ lagging}$$

Because the two currents are only $33.9^\circ$ apart, the starting torque $T_{st} \propto I_mI_s\sin\alpha$ is small compared with that of a capacitor-start motor, which can reach $90^\circ$.

@s 9
**Shaded-pole single-phase motor.**

**Construction:** a salient-pole stator with a concentrated single-phase coil; a **shading coil** (one short-circuited copper ring or band) embraces about one third of each pole face. The rotor is a squirrel-cage rotor.

**Principle.** The alternating main flux $\Phi_m$ is divided into $\Phi_u$ (unshaded part) and $\Phi_s$ (shaded part). The flux through the shaded part induces an emf $E_s$ in the shading ring, which is $90^\circ$ behind $\Phi_s$. The short-circuit current $I_s$ it drives lags $E_s$ by the ring's impedance angle and produces its own flux, so the net shaded-part flux $\Phi_s$ **lags** the unshaded flux $\Phi_u$ by a small angle $\gamma$ (about $30^\circ$). Two fluxes that are displaced in space (the unshaded and the shaded part of the pole) and in time create a weak **rotating field** which moves **from the unshaded towards the shaded side of the pole**; the rotor is dragged in that direction and starts.

```figure caption="Question 9: shaded-pole motor: pole with shading ring (left), flux phasors (centre) and typical torque-speed characteristic (right)."
fig,axs=plt.subplots(1,3,figsize=(6.8,2.5),gridspec_kw={'width_ratios':[1,1,1.1]})
ax=axs[0]; ax.axis('off'); ax.set_xlim(0,4); ax.set_ylim(0,3); ax.set_aspect('equal')
ax.add_patch(Rectangle((0.3,2.2),3.4,0.5,fc='#cbd5e1',ec=INK)); ax.add_patch(Rectangle((1.3,1.2),1.4,1.0,fc='#cbd5e1',ec=INK))
ax.add_patch(Rectangle((1.9,0.4),1.8,0.8,fc='#cbd5e1',ec=INK)); ax.add_patch(Rectangle((0.3,0.4),1.4,0.8,fc='#cbd5e1',ec=INK))
ax.add_patch(Rectangle((2.2,0.35),0.4,0.9,fc='none',ec=ACCENT,lw=2))
ax.text(2.4,0.05,'shading ring',fontsize=7,ha='center',color=ACCENT); ax.text(1.0,0.02,'unshaded',fontsize=7,ha='center')
ax.add_patch(Rectangle((1.45,1.45),0.5,0.5,fc='white',ec=INK,lw=0.8)); ax.text(1.7,1.7,'coil',fontsize=7,ha='center',va='center')
arrow(ax,(1.0,0.2),(2.8,0.2),None,color=MUTED); ax.text(2.0,2.9,'torque direction: unshaded to shaded',fontsize=6.5,ha='center')
ax=axs[1]; ax.axis('off'); ax.set_xlim(-0.3,2.2); ax.set_ylim(-1.3,1.3); ax.set_aspect('equal')
arrow(ax,(0,0),(1.8,0),'$\\Phi_u$',off=0.12); arrow(ax,(0,0),(1.5*np.cos(np.radians(-30)),1.5*np.sin(np.radians(-30))),'$\\Phi_s$',color=ACCENT,off=0.12)
arrow(ax,(0,0),(1.0*np.cos(np.radians(-120)),1.0*np.sin(np.radians(-120))),'$E_s$',color=SERIES[2],off=0.1)
arrow(ax,(0,0),(0.8*np.cos(np.radians(-150)),0.8*np.sin(np.radians(-150))),'$I_s$',color=SERIES[3],off=0.1)
ax.add_patch(Arc((0,0),0.8,0.8,theta1=-30,theta2=0,color=INK)); ax.text(0.55,-0.14,'$\\gamma$',fontsize=8)
ax=axs[2]; w=np.linspace(0,1,100); T=(0.45+1.1*w*(1-w))*(1-w**8)
ax.plot(w,T,color=INK,lw=1.8)
ax.set_xlabel('speed (pu of $N_s$)',fontsize=8); ax.set_ylabel('torque (pu)',fontsize=8); ax.set_ylim(0,1.0); ax.text(0.04,0.3,'low starting\ntorque',fontsize=7)
```

**Characteristics.**

- **Low starting torque** (about 0.5 to 0.8 of full-load torque or less) and a drooping torque-speed curve (a large slip at full load, 8 to 15 %).
- **Low efficiency** (5 to 35 %) and a low power factor, because of the continuous loss in the shading ring; rating up to about 1/20 hp (fractional).
- **Direction of rotation is fixed** (unshaded to shaded); it cannot be reversed electrically (the stator would have to be turned around). Speed can be changed by voltage control.
- Very simple, rugged, no centrifugal switch, no brushes, cheap.

**Applications:** table and exhaust fans, hair dryers, record players, small blowers, projectors, photocopiers, toys.

@s 10
**Constructional features of a BLDC motor**

- **Stator:** laminated silicon-steel core with a three-phase (sometimes two- or four-phase) concentrated winding in the slots, star connected, designed for a trapezoidal (or sinusoidal) back-emf.
- **Rotor:** a laminated steel core carrying **permanent magnets** (ferrite, or NdFeB / SmCo for a high power density) that are surface-mounted or buried (interior), with 2 to 8 poles. No windings, no slip rings, no commutator, no brushes.
- **Rotor-position sensors:** three Hall-effect sensors $120^\circ$ apart (or an optical encoder or resolver, or a sensorless back-emf method) give the commutation sequence.
- **Electronic commutator:** a three-phase voltage-source inverter (six switches: MOSFET or IGBT) with a controller, which excites two phases at a time for $120^\circ$ electrical conduction.

**Difference from an induction motor**

| | **BLDC motor** | **Induction motor** |
|---|---|---|
| Rotor | Permanent magnets | Squirrel cage or wound rotor with induced currents |
| Rotor excitation | By the magnet (no rotor loss) | Magnetising current from the stator; rotor $I^2R$ loss |
| Speed | **Synchronous**, with no slip | Below synchronous speed (slip 2 to 6 %) |
| Control | Needs an inverter and a position sensor | Can run directly on the mains |
| Efficiency, power factor | Higher efficiency (85 to 95 %), better pf | Lower |
| Torque density | Higher, smaller for the same torque | Lower |
| Torque-speed | Linear, like a d.c. motor, high starting torque | Non-linear, with breakdown torque |
| Cost, robustness | Magnet cost, magnets can demagnetise | Cheaper, very rugged |

**Applications of BLDC motor:** electric vehicles and e-bikes, drones, computer cooling fans and hard-disc drives, air-conditioner compressors, robotics and servo drives, medical equipment, washing machines.

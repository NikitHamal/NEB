---
file: NEBians-Past-Paper-Grade-12-Physics-2082-General.pdf
subject: Physics
grade: 12
year_bs: 2082
year_ad: 2025
stream: General Stream
code: 1021 'H'
time: 3 hrs
marks: 75
students: For the regular and partial general stream students whose first two digits of registration number start from 78, 79, 80 and 81
category: Board Exam
---
## Group 'A'
<small>Multiple choice questions · rewrite the correct option of each question in your answer sheet · [11×1=11]</small>

@mcq 1
What is the difference between the moment of inertia of a rod about an axis passing through its one end and through its centre, perpendicular to its length?
@opts $\dfrac{ML^2}{3}$ | $\dfrac{ML^2}{4}$ | $\dfrac{ML^2}{6}$ | $\dfrac{ML^2}{12}$

@mcq 2
For an oscillating object, the displacement versus time curve is shown in the figure. What is the velocity of the object in the mean position?

```figure caption="Displacement–time curve for question 2."
fig, ax = plt.subplots(figsize=(4.2,2.2))
t = np.linspace(0, 3.6, 500); x = 0.2*np.cos(np.pi*t)
ax.plot(t, x, color=INK, lw=1.5)
ax.axhline(0, color=INK, lw=.8)
for s in (0.5, 1.5, 2.5): ax.plot([s],[0], 'o', color=ACCENT, ms=4)
ax.set_xticks([1,2,3]); ax.set_yticks([0.2]); ax.set_xlabel('t (s)'); ax.set_ylabel('x (m)')
ax.spines[['top','right']].set_visible(False)
ax.spines['bottom'].set_position('zero'); ax.set_ylim(-0.26, 0.26)
```

@opts $0.2\pi$ m/s | $0.4\pi$ m/s | $2\pi$ m/s | $4\pi$ m/s

@mcq 3
Two spherical rain drops of equal size are falling vertically downward with a terminal velocity of 0.15 m/s. What would be the terminal velocity if these drops were combined to form a larger drop?
@opts 0.15 m/s | 0.24 m/s | 0.31 m/s | 0.48 m/s

@mcq 4
What happens in an adiabatic process?
@opts-col Volume remains constant | Pressure remains constant | Temperature remains constant | The system is insulated from the surroundings

@mcq 5
The efficiency of a Carnot engine operating between the steam point and the ice point is
@opts 26.8% | 50% | 73.2% | 100%

@mcq 6
Which of the following is an example of a transverse wave?
@opts-col Sound wave in air | Waves inside the water | Wave produced in the stem of a vibrating tuning fork | Wave produced in a stretched string

@mcq 7
Which one of the following phenomena is not explained by Huygens' construction of wavefront?
@opts Refraction | Reflection | Polarization | Diffraction

@mcq 8
The magnetic field intensity at the centre of a circular coil of radius $R$ carrying current $I$ is
@opts $\dfrac{\mu_0 I}{R}$ | $\dfrac{\mu_0 I}{2R}$ | $\dfrac{\mu_0 I}{2\pi R}$ | $\dfrac{2\mu_0 I}{R}$

@mcq 9
If $\chi$ is the magnetic susceptibility of a material, then its relative permeability $\mu_r$ is
@opts $\chi + 1$ | $\chi - 1$ | $\dfrac{1}{\chi}$ | $1+\chi^2$

@mcq 10
A square coil of area $10^{-2}\ \text{m}^2$ is placed perpendicular to a uniform magnetic field of intensity $10^{3}$ T. What is the magnetic flux through the coil?
@opts 100 Weber | 10 Weber | $10^{-3}$ Weber | $10^{-5}$ Weber

@mcq 11
What is the point where seismic waves start called?
@opts Epicenter | Metacenter | Hypocenter | Seismic center

## Group 'B'
<small>Short answer questions · [8×5=40]</small>

@q 12
(a) A ballet dancer sometimes stretches and sometimes folds her arms during her performance. Why? Justify. [[2]]
(b) Establish a relation between torque and moment of inertia for a rigid body. [[2]]
(c) Why do we prefer a wrench of longer arm over a wrench of shorter arm? [[1]]
@or
(a) Show that the total energy of a particle executing SHM is constant. [[3]]
(b) Draw a graph showing the variation of potential energy of a particle in SHM with displacement. [[1]]
(c) The time period of a simple pendulum on the surface of the earth is $T$. What will be its time period on the Moon's surface? [[1]]

@q 13
(a) Define laminar flow and turbulent flow of a liquid. [[2]]
(b) Water flows steadily through a horizontal pipe of non-uniform cross-section. If the pressure of water is $4\times10^{4}\ \text{N m}^{-2}$ at a point where the velocity of flow is 2 m/s and the cross-section is $200\ \text{cm}^2$, calculate the pressure at a point where the cross-section reduces to $50\ \text{cm}^2$. (Density of water = $1000\ \text{kg/m}^3$) [[3]]

@q 14
(a) A Carnot engine has 25% efficiency with a sink at $9^{\circ}$C. By how many degrees should the temperature of the source be increased in order to raise the efficiency to 50%? [[3]]
(b) State the first law of thermodynamics. Does it follow the principle of conservation of energy? Explain. [[2]]

@q 15
(a) Discuss the effect of temperature and pressure on the velocity of sound in a gas. [[2]]
(b) A train is approaching a cliff at 10 m/s. The driver sounds a whistle of frequency 600 Hz. What will be the frequency of the echo as heard by the driver? (Velocity of sound in air = $340\ \text{m s}^{-1}$) [[3]]

@q 16
(a) State the two Kirchhoff's laws of an electrical circuit. [[2]]
(b) Obtain an expression for the balanced condition of a Wheatstone bridge using Kirchhoff's laws. [[3]]

@q 17
(a) State Lenz's law. [[1]]
(b) Plot a graph to show the variation of induced emf in a coil rotating in a uniform magnetic field with time. [[1]]
(c) Derive an expression for the energy stored in an inductor. [[3]]

@q 18
(a) Write the symbol and truth table of a NAND gate. [[2]]
(b) Explain full wave rectification using two P-N junction diodes. [[3]]

@q 19
(a) An oil drop of mass $3\times10^{-11}$ g and of radius $2\times10^{-4}$ cm carries 10 excess electrons. What is its terminal velocity when
(i) falling in a region in which there is no electric field? [[1]]
(ii) falling in an electric field of $3\times10^{5}\ \text{V m}^{-1}$ directed downward? [[1]]
(Viscosity of air = $1.8\times10^{-5}\ \text{N s m}^{-2}$)
(b) In Thomson's method for determining the specific charge of an electron, why is the electric field kept perpendicular to the magnetic field? Justify. [[2]]
(c) What is the use of X-rays in Millikan's oil drop experiment? [[1]]
@or
(a) Define decay constant and half-life. [[2]]
(b) Derive the equation $N = N_0 e^{-\lambda t}$ for a radioactive process, where the symbols have their usual meanings. [[3]]

## Group 'C'
<small>Long answer questions · [3×8=24]</small>

@q 20
(a) What are stationary waves? Prove that the distance between two consecutive nodes in it is equal to half of the wavelength. [[3]]
(b) A guitar string of length 1.5 m is made of steel of density $7800\ \text{kg/m}^3$ and Young's modulus $2\times10^{11}\ \text{N/m}^2$. It produces an elastic strain of 1% in the string. Calculate [[3]]
(i) the stress developed in the string.
(ii) the frequency of the second mode of vibration.
(c) The given figure shows a standing wave formed in an open organ pipe.

```figure caption="Standing wave in an open organ pipe (question 20 c)."
fig, ax = plt.subplots(figsize=(4.4,1.7))
x = np.linspace(0, 1, 400); y = np.cos(2*np.pi*x)
ax.plot(x, y, color=INK, lw=1.3); ax.plot(x, -y, color=INK, lw=1.3)
ax.plot([0,1],[1.12,1.12], color=INK, lw=1.6); ax.plot([0,1],[-1.12,-1.12], color=INK, lw=1.6)
ax.set_xlim(-.03,1.03); ax.set_ylim(-1.3,1.3); ax.axis('off')
```

(i) Which mode of vibration is shown? [[1]]
(ii) Obtain the frequency of vibration for this mode. [[1]]
@or
(a) Prove that bright and dark fringes are equally spaced in Young's double slit experiment. [[3]]
(b) A parallel beam of monochromatic light is incident on a diffraction grating having 500 lines/mm to get second order maxima at $30^{\circ}$. Calculate the wavelength of light used. [[3]]
(c) State and prove Brewster's law. [[2]]

@q 21
(a) The figure below shows a series LCR circuit.

```figure caption="Series LCR circuit (question 21 a)."
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.8,2.3))
def w(xs, ys): ax.plot(xs, ys, color=INK, lw=1.3, solid_capstyle='round')
w([0,0,1.2],[0,1.4,1.4]); w([1.9,2.6],[1.4,1.4]); w([2.8,3.2],[1.4,1.4]); w([4.6,5],[1.4,1.4]); w([5,5,0.0],[1.4,0,0])
w([0,2.0],[0,0]); w([3.0,5],[0,0])
th = np.linspace(0, 4*np.pi, 100)
ax.plot(1.2+0.7*th/(4*np.pi)*1.0, 1.4+0.18*np.abs(np.sin(th))*np.sign(np.sin(th)), color=INK, lw=1.3)
ax.plot([2.6,2.6],[1.15,1.65], color=INK, lw=1.8); ax.plot([2.8,2.8],[1.15,1.65], color=INK, lw=1.8)
zx = np.linspace(3.2,4.6,9); zy = 1.4+0.16*np.array([0,1,-1,1,-1,1,-1,1,0])
ax.plot(zx, zy, color=INK, lw=1.3)
ax.add_patch(Circle((2.5,0),0.5,fc='white',ec=INK,lw=1.3,zorder=3))
ax.text(2.5,0,'~',ha='center',va='center',fontsize=14,zorder=4)
ax.text(1.55,1.85,'L = 100 mH',ha='center',fontsize=8); ax.text(2.7,1.85,'C = 2 μF',ha='center',fontsize=8); ax.text(3.9,1.85,'R = 400 Ω',ha='center',fontsize=8)
ax.text(2.5,-0.75,'V, f',ha='center',fontsize=8)
ax.set_xlim(-0.3,5.3); ax.set_ylim(-1,2.2); ax.set_aspect('equal'); ax.axis('off')
```

If the frequency of the ac source is $\dfrac{500}{\pi}$ Hz, then
(i) calculate the phase angle between current and voltage. [[2]]
(ii) which one leads in phase, current or voltage? Justify. [[1]]
(b) What is meant by impedance of an ac circuit? [[1]]
(c) Two parallel wires P and Q carrying currents $I_1$ and $I_2$ are placed in air at a distance $r$ apart as shown in the figure.

```figure caption="Parallel current-carrying wires (question 21 c)."
fig, ax = plt.subplots(figsize=(3.0,2.0))
for x, lab in ((0,'P'),(2,'Q')):
    ax.annotate('', xy=(x,1.5), xytext=(x,0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4))
    ax.text(x, 1.65, lab, ha='center', fontsize=9)
ax.text(-0.18,0.8,'$I_1$',ha='right',fontsize=9); ax.text(2.18,0.8,'$I_2$',ha='left',fontsize=9)
ax.annotate('', xy=(0.02,-0.25), xytext=(1.98,-0.25), arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1))
ax.text(1,-0.55,'r',ha='center',fontsize=9)
ax.set_xlim(-0.6,2.6); ax.set_ylim(-0.8,1.9); ax.axis('off')
```

(i) Obtain an expression for the magnitude of force per unit length between them. [[2]]
(ii) What is the nature of the force in this case? [[1]]
(iii) What will be the force per unit length between the two wires if the distance between the wires is halved, keeping all other quantities constant? [[1]]
@or
(a) Explain the variation of thermoelectric emf with the temperature of the hot junction of a thermocouple. [[3]]
(b) A potentiometer circuit is shown in the figure. If the total length of the potentiometer wire is 4 m and has resistance $10\ \Omega$ and the balance point is obtained at a length of 240 cm, calculate the value of the unknown emf $E$. [[3]]

```figure caption="Potentiometer circuit (question 21 b, alternative)."
fig, ax = plt.subplots(figsize=(4.8,2.5))
def w(xs, ys, **k): ax.plot(xs, ys, color=INK, lw=1.3, **k)
w([0,0,1.3],[0,2,2]); ax.plot([1.3,1.3],[1.8,2.2],color=INK,lw=2.2); ax.plot([1.5,1.5],[1.65,2.35],color=INK,lw=1.2)
w([1.5,2.6],[2,2]); ax.add_patch(plt.Rectangle((2.6,1.85),1.1,0.3,fc='white',ec=INK,lw=1.2)); ax.text(3.15,2.0,'R.B',ha='center',va='center',fontsize=7)
ax.text(3.15,1.6,'R = 290 Ω',ha='center',fontsize=7); ax.text(1.4,2.45,'3 V',ha='center',fontsize=8)
w([3.7,5,5],[2,2,1]); w([0,0],[0,1]); ax.plot([0,5],[1,1],color=INK,lw=2)
ax.text(-0.2,1,'A',ha='right',va='center',fontsize=8); ax.text(5.2,1,'B',va='center',fontsize=8)
ax.annotate('', xy=(0,1.25), xytext=(3.0,1.25), arrowprops=dict(arrowstyle='<|-|>',color=INK,lw=0.9)); ax.text(1.5,1.35,'240 cm',ha='center',fontsize=8)
ax.annotate('', xy=(3.0,1.02), xytext=(3.0,0.5), arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.1))
w([3.0,3.0,4.6],[0.5,0.2,0.2]); ax.add_patch(plt.Circle((4.2,0.2),0.18,fc='white',ec=INK,lw=1.2)); ax.text(4.2,0.2,'G',ha='center',va='center',fontsize=7)
w([0,0],[1,0.2]); w([0,0.5],[0.2,0.2]); ax.plot([0.5,0.5],[0.05,0.35],color=INK,lw=2.0); ax.plot([0.7,0.7],[0.12,0.28],color=INK,lw=1.2)
w([0.7,2.2],[0.2,0.2]); ax.add_patch(plt.Circle((2.4,0.2),0.12,fc='white',ec=INK,lw=1.2)); w([2.52,3.0],[0.2,0.2]); ax.text(0.6,-0.1,'E',ha='center',fontsize=8); ax.text(2.4,-0.1,'K',ha='center',fontsize=8)
ax.set_xlim(-0.5,5.5); ax.set_ylim(-0.3,2.7); ax.set_aspect('equal'); ax.axis('off')
```

(c) Use Ampere's circuital law to find the magnetic field due to a straight current carrying conductor. [[2]]

@q 22
(a) Define threshold wavelength. [[1]]
(b) A metal has a work function of 2 eV. Calculate the maximum speed of the emitted photoelectrons when it is illuminated by radiation of wavelength 150 nm. What is the least frequency of the radiation for which electrons are emitted? (Given: Planck's constant $h = 6.62\times10^{-34}$ J s, $m = 9.1\times10^{-31}$ kg, $e = 1.6\times10^{-19}$ C) [[3]]
(c) State Heisenberg's uncertainty principle. [[1]]
(d) Obtain an expression for the velocity of an electron in the $n^{\text{th}}$ orbit of the hydrogen atom. [[3]]

<!-- SOLUTIONS -->
### Group A — answer key

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ans | B | A | B | D | A | D | C | B | A | B | C |

**1. B.** $I_{end} - I_{centre} = \dfrac{ML^2}{3} - \dfrac{ML^2}{12} = \dfrac{ML^2}{4}$.

**2. A.** Amplitude $A = 0.20$ m. Successive zero crossings are 1 s apart, so $T = 2$ s and $\omega = \pi$ rad/s. Speed at the mean position is maximum: $v = A\omega = 0.2\pi$ m/s.

**3. B.** Combining two drops: $\tfrac43\pi R^3 = 2\cdot\tfrac43\pi r^3$, so $R = 2^{1/3}r$. Terminal velocity $v_t \propto r^2$, so $v' = 0.15 \times 2^{2/3} = 0.15\times1.587 \approx 0.24$ m/s.

**4. D.** In an adiabatic process no heat is exchanged: $\Delta Q = 0$, the system is thermally insulated.

**5. A.** $\eta = 1 - \dfrac{273}{373} = 0.268 = 26.8\%$.

**6. D.** Particles of a stretched string vibrate perpendicular to the direction of propagation. Sound in air, waves inside water and the waves in a tuning-fork stem are longitudinal.

**7. C.** Huygens' construction explains reflection, refraction and diffraction. Polarization needs the transverse nature of light, which the wavefront construction does not account for.

**8. B.** $B = \dfrac{\mu_0 I}{2R}$ at the centre of a circular coil of one turn.

**9. A.** $\mu_r = 1 + \chi$.

**10. B.** $\Phi = BA\cos0^{\circ} = 10^{3}\times10^{-2} = 10$ Wb.

**11. C.** Seismic waves start at the focus, called the hypocenter. The epicenter is the point on the surface directly above it.

### Group B

@s 12
**(a)** When she stretches her arms, her moment of inertia $I$ increases. With no external torque, angular momentum $L = I\omega$ is conserved, so $\omega$ decreases and she rotates slowly. When she folds her arms, $I$ decreases and $\omega$ increases, so she spins faster.

**(b)** Consider a rigid body rotating about a fixed axis with angular acceleration $\alpha$. A particle of mass $m_i$ at distance $r_i$ has tangential acceleration $a_i = r_i\alpha$, so the tangential force on it is $F_i = m_i r_i\alpha$. Its torque is $\tau_i = F_i r_i = m_i r_i^2\alpha$. Summing over all particles,
$$\tau = \sum m_i r_i^2\,\alpha = I\alpha$$
where $I = \sum m_i r_i^2$. Hence torque = moment of inertia × angular acceleration.

**(c)** Torque $\tau = F\times d$. For a given torque needed to loosen a nut, a longer arm $d$ requires a smaller force $F$, so the nut turns with less effort.

**Or (a)** For SHM, $x = A\sin\omega t$, $v = A\omega\cos\omega t$. Kinetic energy $K = \tfrac12 m v^2 = \tfrac12 m\omega^2A^2\cos^2\omega t$. Potential energy $U = \tfrac12 kx^2 = \tfrac12 m\omega^2A^2\sin^2\omega t$ (as $k = m\omega^2$). Total
$$E = K + U = \tfrac12 m\omega^2A^2(\cos^2\omega t + \sin^2\omega t) = \tfrac12 m\omega^2A^2,$$
which does not depend on time, so the total energy is constant.

**(b)** $U = \tfrac12 kx^2$ is a parabola with its minimum at $x=0$ and value $\tfrac12kA^2$ at $x = \pm A$.

```figure caption="Potential energy of a particle in SHM against displacement."
fig, ax = plt.subplots(figsize=(3.8,2.3))
x = np.linspace(-1,1,200); ax.plot(x, x**2, color=ACCENT, lw=1.8)
ax.axhline(1, color=GRID, ls='--', lw=1); ax.set_xticks([-1,0,1]); ax.set_xticklabels(['−A','0','A']); ax.set_yticks([0,1]); ax.set_yticklabels(['0',r'$\frac{1}{2}kA^2$'])
ax.set_xlabel('displacement x'); ax.set_ylabel('U'); ax.spines[['top','right']].set_visible(False)
```

**(c)** $T = 2\pi\sqrt{l/g}$ and $g_{moon}\approx g/6$, so $T' = 2\pi\sqrt{\dfrac{l}{g/6}} = \sqrt{6}\,T \approx 2.45\,T$.

@s 13
**(a)** *Laminar flow:* the flow of a liquid in which every particle follows the same path as the particle ahead of it (streamline flow), with velocity below the critical velocity. *Turbulent flow:* irregular, zig-zag flow with eddies, occurring when the velocity exceeds the critical velocity (Reynolds number above about 3000).

**(b)** Continuity: $A_1v_1 = A_2v_2 \Rightarrow v_2 = \dfrac{200\times2}{50} = 8$ m/s.
Bernoulli (horizontal pipe): $P_1 + \tfrac12\rho v_1^2 = P_2 + \tfrac12\rho v_2^2$
$$P_2 = 4\times10^{4} + \tfrac12(1000)(2^2 - 8^2) = 40000 - 30000 = 1\times10^{4}\ \text{N m}^{-2}.$$

@s 14
**(a)** $\eta = 1 - \dfrac{T_2}{T_1}$, with $T_2 = 9 + 273 = 282$ K.
For $\eta = 0.25$: $T_1 = \dfrac{282}{0.75} = 376$ K. For $\eta = 0.50$: $T_1' = \dfrac{282}{0.50} = 564$ K.
Increase in source temperature $= 564 - 376 = 188$ K (188 °C).

**(b)** The heat supplied to a system equals the increase in its internal energy plus the work done by the system: $\Delta Q = \Delta U + \Delta W$. Yes, it follows the principle of conservation of energy: it states that heat energy supplied is neither created nor destroyed but converted into internal energy and external work, so the total energy is conserved.

@s 15
**(a)** *Temperature:* $v = \sqrt{\gamma P/\rho}\propto\sqrt{T}$, so velocity increases with absolute temperature ($v_t \approx v_0 + 0.61t$ m/s in air). *Pressure:* at constant temperature $P/\rho$ is constant (Boyle's law), so the velocity of sound is independent of pressure.

**(b)** The cliff (stationary observer) receives the whistle from the approaching train:
$$f_1 = \frac{v}{v - v_s}f = \frac{340}{340-10}\times600 = 618.2\ \text{Hz}.$$
The cliff reflects this as a stationary source; the driver moves towards it:
$$f_2 = \frac{v + v_o}{v}f_1 = \frac{340+10}{340}\times618.2 \approx 636\ \text{Hz}.$$
The echo is heard at about **636 Hz**.

@s 16
**(a)** *Junction (current) law:* the algebraic sum of the currents meeting at a junction is zero, $\sum I = 0$. *Loop (voltage) law:* the algebraic sum of the emfs and the potential drops $IR$ around any closed loop is zero, $\sum E + \sum IR = 0$.

**(b)** Let the bridge have arms $P$ (A to B), $Q$ (B to C), $R$ (A to D) and $S$ (D to C), a galvanometer between B and D, and a cell between A and C. Let the current $I_1$ flow in $P$ and $Q$ and $I_2$ in $R$ and $S$ when the galvanometer shows no deflection ($I_g = 0$, so B and D are at the same potential).
Loop law for loop ABDA: $I_1P - I_2R = 0 \Rightarrow I_1P = I_2R$ … (1)
Loop law for loop BCDB: $I_1Q - I_2S = 0 \Rightarrow I_1Q = I_2S$ … (2)
Dividing (1) by (2):
$$\frac{P}{Q} = \frac{R}{S}$$
which is the balanced condition of the Wheatstone bridge.

@s 17
**(a)** The direction of the induced current is such that it opposes the change (cause) that produces it.

**(b)** $e = e_0\sin\omega t$, a sine curve of period $T$ and peak value $e_0 = NBA\omega$.

```figure caption="Induced emf in a rotating coil against time."
fig, ax = plt.subplots(figsize=(4.2,2.2))
t = np.linspace(0,2,300); ax.plot(t, np.sin(2*np.pi*t), color=ACCENT, lw=1.8); ax.axhline(0,color=INK,lw=.8)
ax.set_xticks([0,0.5,1,1.5,2]); ax.set_xticklabels(['0','T/2','T','3T/2','2T']); ax.set_yticks([-1,0,1]); ax.set_yticklabels(['−e₀','0','e₀'])
ax.set_xlabel('time t'); ax.set_ylabel('emf e'); ax.spines[['top','right']].set_visible(False); ax.spines['bottom'].set_position('zero')
```

**(c)** When the current in an inductor of self-inductance $L$ grows by $dI$ in time $dt$, the back emf is $e = L\,\dfrac{dI}{dt}$. Work done against it: $dW = e\,I\,dt = LI\,dI$. To raise the current from 0 to $I$:
$$W = \int_0^I LI\,dI = \tfrac12 LI^2,\qquad\text{so}\qquad U = \tfrac12 LI^2.$$

@s 18
**(a)** NAND is an AND gate followed by a NOT gate: $Y = \overline{A\cdot B}$. Symbol: the AND-gate shape with a small circle at the output.

| A | B | Y |
|---|---|---|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**(b)** Two diodes $D_1$, $D_2$ are connected to the ends of the secondary of a centre-tapped transformer; the load $R_L$ is connected between the centre tap and the joined cathodes. During the positive half-cycle the upper end is positive, so $D_1$ conducts and $D_2$ is reverse biased; current flows through $R_L$ in one direction. During the negative half-cycle the lower end is positive, so $D_2$ conducts and $D_1$ is blocked; current flows through $R_L$ in the *same* direction. The output across $R_L$ is therefore a pulsating dc of frequency twice the input frequency, using both half-cycles.

@s 19
**(a)** $m = 3\times10^{-11}$ g $= 3\times10^{-14}$ kg, $r = 2\times10^{-4}$ cm $= 2\times10^{-6}$ m, $q = 10e = 1.6\times10^{-18}$ C. Weight $mg = 3\times10^{-14}\times9.8 = 2.94\times10^{-13}$ N. Neglecting buoyancy of air:
(i) At terminal velocity $mg = 6\pi\eta r v$:
$$v = \frac{mg}{6\pi\eta r} = \frac{2.94\times10^{-13}}{6\pi(1.8\times10^{-5})(2\times10^{-6})} \approx 4.3\times10^{-4}\ \text{m s}^{-1}\ (\text{downward}).$$
(ii) Electric force $qE = 1.6\times10^{-18}\times3\times10^{5} = 4.8\times10^{-13}$ N. The electrons make the drop negative, so for a downward field the electric force acts upward and exceeds the weight. The net upward force is $4.8\times10^{-13} - 2.94\times10^{-13} = 1.86\times10^{-13}$ N, so the drop actually moves **upward** with
$$v = \frac{qE - mg}{6\pi\eta r} = \frac{1.86\times10^{-13}}{6.79\times10^{-10}} \approx 2.7\times10^{-4}\ \text{m s}^{-1}.$$

**(b)** The electron beam is undeflected only when the electric force $eE$ and the magnetic force $evB$ are equal and opposite, which is possible only if the fields are perpendicular to each other (and to the beam). Then $eE = evB$, giving $v = E/B$, and the specific charge follows from the deflection with only $B$ switched on: $\dfrac{e}{m} = \dfrac{v}{Br}$.

**(c)** X-rays ionise the air between the plates, producing charges that attach to the oil drop and change the charge on it by one or more electrons, which allows the drop's charge to be observed in steps of $e$.

**Or (a)** *Decay constant:* the ratio of the number of atoms disintegrating per unit time to the total number of atoms present; the fraction decaying per second. *Half-life:* the time in which half of the radioactive nuclei present decay, $T_{1/2} = \dfrac{0.693}{\lambda}$.

**(b)** The rate of decay is proportional to the number of undecayed nuclei: $\dfrac{dN}{dt} = -\lambda N$. Separating variables, $\dfrac{dN}{N} = -\lambda\,dt$. Integrating from $N_0$ at $t=0$ to $N$ at time $t$:
$$\ln\frac{N}{N_0} = -\lambda t\quad\Rightarrow\quad N = N_0e^{-\lambda t}.$$

### Group C

@s 20
**(a)** Stationary (standing) waves are formed by the superposition of two identical progressive waves travelling in opposite directions along the same line; they show fixed nodes and antinodes and transport no energy.
Let $y_1 = a\sin(\omega t - kx)$ and $y_2 = a\sin(\omega t + kx)$ (reflected). Then
$$y = y_1+y_2 = 2a\cos kx\,\sin\omega t.$$
The amplitude is $2a\cos kx$. At nodes $\cos kx = 0$, so $kx = (2n+1)\dfrac{\pi}{2}$, i.e. $x = (2n+1)\dfrac{\lambda}{4}$ (since $k = 2\pi/\lambda$). The consecutive nodes are at $x_n = (2n+1)\lambda/4$ and $x_{n+1} = (2n+3)\lambda/4$, so
$$x_{n+1} - x_n = \frac{\lambda}{2}.$$

**(b)** (i) Stress $= Y\times$ strain $= 2\times10^{11}\times0.01 = 2\times10^{9}\ \text{N m}^{-2}$.
(ii) The wave speed on the string is $v = \sqrt{T/\mu} = \sqrt{\text{stress}/\rho} = \sqrt{\dfrac{2\times10^{9}}{7800}} \approx 506\ \text{m s}^{-1}$. A string fixed at both ends has $f_n = \dfrac{nv}{2L}$, so the second mode ($n=2$) is
$$f_2 = \frac{v}{L} = \frac{506}{1.5} \approx 3.4\times10^{2}\ \text{Hz}\ (\approx 338\ \text{Hz}).$$

**(c)** (i) Antinodes at both ends and two nodes in between: the **second harmonic (first overtone)**, with $L = \lambda$.
(ii) $f = \dfrac{v}{\lambda} = \dfrac{v}{L} = \dfrac{2v}{2L}$, that is, $f = 2f_1$ where $f_1 = v/2L$ is the fundamental frequency.

**Or (a)** Two coherent sources $S_1$, $S_2$ separated by $d$ illuminate a screen at distance $D$. For a point $P$ at height $y$ from the centre, the path difference is $\Delta = \dfrac{yd}{D}$. *Bright fringes:* $\Delta = n\lambda \Rightarrow y_n = \dfrac{n\lambda D}{d}$. Spacing: $y_{n+1} - y_n = \dfrac{\lambda D}{d}$. *Dark fringes:* $\Delta = (2n+1)\dfrac{\lambda}{2} \Rightarrow y_n' = (2n+1)\dfrac{\lambda D}{2d}$; spacing $y'_{n+1} - y'_n = \dfrac{\lambda D}{d}$. Both spacings equal $\beta = \dfrac{\lambda D}{d}$, independent of $n$, so the fringes are equally spaced.

**(b)** $N = 500$ lines/mm $= 5\times10^{5}$ lines/m, so $d = \dfrac{1}{N} = 2\times10^{-6}$ m. From $d\sin\theta = n\lambda$ with $n=2$, $\theta = 30^{\circ}$:
$$\lambda = \frac{d\sin\theta}{n} = \frac{2\times10^{-6}\times0.5}{2} = 5\times10^{-7}\ \text{m} = 500\ \text{nm}.$$

**(c)** *Brewster's law:* when unpolarised light is incident at the polarising angle $i_p$ on a transparent surface, the reflected light is completely plane polarised and $\tan i_p = \mu$.
*Proof:* at $i_p$ the reflected and refracted rays are perpendicular, so $i_p + r = 90^{\circ}$, i.e. $r = 90^{\circ} - i_p$. By Snell's law $\mu = \dfrac{\sin i_p}{\sin r} = \dfrac{\sin i_p}{\sin(90^{\circ}-i_p)} = \dfrac{\sin i_p}{\cos i_p} = \tan i_p$.

@s 21
**(a)** $\omega = 2\pi f = 2\pi\times\dfrac{500}{\pi} = 1000$ rad/s. $X_L = \omega L = 1000\times0.1 = 100\ \Omega$. $X_C = \dfrac{1}{\omega C} = \dfrac{1}{1000\times2\times10^{-6}} = 500\ \Omega$.
(i) $\tan\phi = \dfrac{X_L - X_C}{R} = \dfrac{100-500}{400} = -1$, so $|\phi| = 45^{\circ}$.
(ii) $X_C > X_L$: the circuit is capacitive, so the **current leads the voltage** (by $45^{\circ}$).

**(b)** Impedance $Z = \sqrt{R^2 + (X_L - X_C)^2}$ is the total opposition offered by an ac circuit to the flow of current; $Z = V_{rms}/I_{rms}$, measured in ohm.

**(c)** (i) The field of P at Q is $B_1 = \dfrac{\mu_0I_1}{2\pi r}$. The force on a length $l$ of Q is $F = B_1I_2l$, so
$$\frac{F}{l} = \frac{\mu_0I_1I_2}{2\pi r}.$$
(ii) The currents are in the same direction, so the force is **attractive**.
(iii) $F/l\propto 1/r$, so halving $r$ **doubles** the force per unit length: $\dfrac{F'}{l} = \dfrac{\mu_0I_1I_2}{\pi r}$.

**Or (a)** In a thermocouple, with the cold junction at $0^{\circ}$C, the emf varies with the hot-junction temperature $\theta$ as $e = a\theta + \tfrac12b\theta^{2}$, a parabola. The emf rises to a maximum at the *neutral temperature* $\theta_n = -a/b$, then decreases, becomes zero at the *temperature of inversion* $\theta_i = 2\theta_n$ (for the cold junction at $0^{\circ}$C) and reverses sign beyond it.

```figure caption="Thermoelectric emf against hot-junction temperature."
fig, ax = plt.subplots(figsize=(4.0,2.3))
t = np.linspace(0, 2, 200); e = 1 - (t-1)**2
ax.plot(t, e, color=ACCENT, lw=1.8); ax.axhline(0, color=INK, lw=.8)
ax.set_xticks([1,2]); ax.set_xticklabels([r'$\theta_n$', r'$\theta_i$']); ax.set_yticks([])
ax.set_xlabel('temperature of hot junction'); ax.set_ylabel('thermo emf'); ax.spines[['top','right']].set_visible(False)
```

**(b)** Current in the wire: $I = \dfrac{3}{290+10} = 0.01$ A. Potential gradient: $k = \dfrac{IR_{AB}}{L} = \dfrac{0.01\times10}{4} = 0.025\ \text{V m}^{-1}$. At balance, $E = k\,l = 0.025\times2.4 = 0.06$ V.

**(c)** Take a circular Amperian loop of radius $r$ around a long straight wire carrying current $I$. By symmetry $B$ is tangential and constant on the loop, so $\oint\vec B\cdot d\vec l = B(2\pi r) = \mu_0I$, giving
$$B = \frac{\mu_0I}{2\pi r}.$$

@s 22
**(a)** The threshold wavelength $\lambda_0$ is the maximum wavelength of incident light for which photoelectric emission occurs, $\lambda_0 = hc/\phi$.

**(b)** Energy of a photon: $E = \dfrac{hc}{\lambda} = \dfrac{6.62\times10^{-34}\times3\times10^{8}}{150\times10^{-9}} = 1.324\times10^{-18}$ J $= 8.28$ eV. Work function $\phi = 2$ eV $= 3.2\times10^{-19}$ J. Maximum kinetic energy $K = E - \phi = 1.324\times10^{-18} - 3.2\times10^{-19} = 1.004\times10^{-18}$ J. Then
$$v_{max} = \sqrt{\frac{2K}{m}} = \sqrt{\frac{2\times1.004\times10^{-18}}{9.1\times10^{-31}}} \approx 1.49\times10^{6}\ \text{m s}^{-1}.$$
Least (threshold) frequency: $f_0 = \dfrac{\phi}{h} = \dfrac{3.2\times10^{-19}}{6.62\times10^{-34}} \approx 4.8\times10^{14}\ \text{Hz}$.

**(c)** It is impossible to determine simultaneously and exactly both the position and the momentum of a particle: $\Delta x\,\Delta p \ge \dfrac{h}{4\pi}$.

**(d)** For an electron in the $n^{th}$ orbit (radius $r_n$), the Coulomb force supplies the centripetal force: $\dfrac{mv^2}{r} = \dfrac{1}{4\pi\epsilon_0}\dfrac{e^2}{r^2}$, so $mv^2r = \dfrac{e^2}{4\pi\epsilon_0}$ … (1). Bohr's quantisation: $mvr = \dfrac{nh}{2\pi}$ … (2). Dividing (1) by (2):
$$v_n = \frac{e^2}{4\pi\epsilon_0}\cdot\frac{2\pi}{nh} = \frac{e^2}{2\epsilon_0 nh}.$$
For $n=1$ this gives $v_1\approx2.19\times10^{6}$ m/s.

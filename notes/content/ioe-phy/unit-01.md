---
subject: Physics
grade: IOE
unit: 1
title: Mechanics
hours: 8
area: Physics
---

Mechanics is about **a third of the Physics paper**. The official syllabus lists seven sub-areas: kinematics and vectors, Newton's laws and friction, work-energy, circular motion with gravitation and SHM, rotation, elasticity, and fluids. The Section B questions combine two ideas, typically energy with circular motion, momentum with energy loss, or continuity with Bernoulli.

::: key What the paper asks from this chapter
- Dimensions of work, power, pressure, surface tension, viscosity, and dimensional checking.
- Projectile formulas: $T=\frac{2u\sin\theta}{g}$, $H=\frac{u^2\sin^2\theta}{2g}$, $R=\frac{u^2\sin2\theta}{g}$.
- Newton's second law on inclines and with friction; $\mu=\tan\theta$ at the angle of repose.
- Momentum conservation and collisions; kinetic energy lost in a perfectly inelastic collision.
- Circular motion: $a=v^2/r$, banking $\tan\theta=\frac{v^2}{rg}$, vertical circle ($v_{\text{bottom}}\ge\sqrt{5gr}$).
- Gravitation: $g'=g\big(\frac{R}{R+h}\big)^2$, escape speed $\sqrt{2gR}=11.2$ km/s, orbital speed, $T^2\propto r^3$.
- SHM: $T=2\pi\sqrt{m/k}$, $2\pi\sqrt{l/g}$, $v_{\max}=A\omega$, energy $\frac{1}{2}kA^2$.
- Rotation: $I$ of standard bodies, $\tau=I\alpha$, $L=I\omega$ conserved.
- Elasticity: $Y=\frac{FL}{A\Delta L}$, energy density $\frac{1}{2}\times$ stress $\times$ strain, Poisson's ratio.
- Fluids: Archimedes, surface tension and capillary rise, Stokes' law, continuity $A_1v_1=A_2v_2$, Bernoulli.
:::

## 1.1 Physical quantities, vectors and kinematics

**Dimensions.** $[\text{force}]=\text{MLT}^{-2}$, $[\text{work, energy}]=\text{ML}^2\text{T}^{-2}$, $[\text{power}]=\text{ML}^2\text{T}^{-3}$, $[\text{pressure, stress, }Y]=\text{ML}^{-1}\text{T}^{-2}$, $[\text{surface tension}]=\text{MT}^{-2}$, $[\text{viscosity }\eta]=\text{ML}^{-1}\text{T}^{-1}$, $[G]=\text{M}^{-1}\text{L}^3\text{T}^{-2}$, $[h]=\text{ML}^2\text{T}^{-1}$. Only quantities of the same dimensions can be added; dimensional analysis checks a formula but cannot fix numerical constants.

**Vectors.** Resultant of $\vec A,\vec B$ at angle $\theta$: $R=\sqrt{A^2+B^2+2AB\cos\theta}$, direction $\tan\alpha=\frac{B\sin\theta}{A+B\cos\theta}$. Two equal forces $F$ at $120^\circ$ give $F$. Polygon law: vectors drawn head to tail close the polygon when the sum is zero. Resolution: $A_x=A\cos\theta$, $A_y=A\sin\theta$. Dot product (work, projection), cross product (torque, magnetic force).

**Equations of uniformly accelerated motion:** $v=u+at$, $s=ut+\frac{1}{2}at^2$, $v^2=u^2+2as$, $s_n=u+\frac{a}{2}(2n-1)$. Free fall uses $a=g=9.8\ \text{m s}^{-2}$. Area under the $v$–$t$ graph is displacement; slope of the $x$–$t$ graph is velocity.

**Projectile** (speed $u$, angle $\theta$): $T=\dfrac{2u\sin\theta}{g}$, $H=\dfrac{u^2\sin^2\theta}{2g}$, $R=\dfrac{u^2\sin2\theta}{g}$ (maximum at $45^\circ$, equal for $\theta$ and $90^\circ-\theta$), $\tan\theta=\frac{4H}{R}$. Trajectory $y=x\tan\theta-\frac{gx^2}{2u^2\cos^2\theta}$ is a parabola. Horizontal launch from height $h$: $t=\sqrt{2h/g}$.

**Relative motion:** $\vec v_{AB}=\vec v_A-\vec v_B$. River crossing: shortest time when heading perpendicular to the bank (time $d/v_b$); shortest path when $\sin\theta=v_r/v_b$ (needs $v_b>v_r$). Rain appears to fall at $\tan\alpha=v_{\text{man}}/v_{\text{rain}}$ from the vertical.

## 1.2 Newton's laws of motion and friction

**Laws:** (1) inertia; (2) $\vec F=\frac{d\vec p}{dt}=m\vec a$; (3) action–reaction on different bodies. **Impulse** $=F\Delta t=\Delta p$ (area under the $F$–$t$ graph). **Momentum conservation** holds when no external force acts: $m_1u_1+m_2u_2=m_1v_1+m_2v_2$; a gun recoils with $v_{\text{gun}}=\frac{m_{\text{bullet}}}{M}v$.

Equilibrium: $\sum\vec F=0$ (e.g. Lami's theorem for three concurrent forces). Inclined plane (angle $\theta$, frictionless): $a=g\sin\theta$. Atwood machine: $a=\dfrac{(m_1-m_2)g}{m_1+m_2}$, $T=\dfrac{2m_1m_2g}{m_1+m_2}$. Lift accelerating up at $a$: apparent weight $m(g+a)$; down: $m(g-a)$; free fall: zero.

**Solid friction.** Static $f_s\le\mu_sN$; kinetic $f_k=\mu_kN$ ($\mu_k<\mu_s$). Laws (verified with an inclined plane): independent of the area of contact, proportional to normal reaction, independent of speed. **Angle of friction** $\lambda$: $\tan\lambda=\mu$; **angle of repose** $\alpha$ (a block just slips): $\tan\alpha=\mu$. On a rough incline $a=g(\sin\theta-\mu\cos\theta)$. Horizontal push $P$ on a block: $a=\dfrac{P-\mu mg}{m}$.

## 1.3 Work, energy and power

$W=\vec F\cdot\vec s=Fs\cos\theta$; area under the $F$–$x$ graph; spring work $\frac{1}{2}kx^2$. **Work–energy theorem:** $W_{\text{net}}=\Delta K=\frac{1}{2}mv^2-\frac{1}{2}mu^2$. $K=\frac{p}{2m}\cdot p=\frac{p^2}{2m}$. Gravitational PE $=mgh$; elastic PE $=\frac{1}{2}kx^2$. Mechanical energy is conserved under **conservative forces** (gravity, spring, electrostatic: work independent of path, zero over a closed loop); friction and drag are non-conservative. **Power** $P=\frac{W}{t}=\vec F\cdot\vec v$; 1 hp = 746 W; kWh = $3.6\times10^6$ J.

**Collisions.** Momentum is always conserved. *Elastic:* kinetic energy also conserved, $e=1$; for equal masses the velocities exchange; for $m_1$ on a stationary $m_2$: $v_1=\frac{m_1-m_2}{m_1+m_2}u$, $v_2=\frac{2m_1}{m_1+m_2}u$. *Perfectly inelastic:* bodies stick, $v=\frac{m_1u_1+m_2u_2}{m_1+m_2}$ and the maximum kinetic energy is lost. Coefficient of restitution $e=\frac{v_2-v_1}{u_1-u_2}$; a ball dropped from $h$ rebounds to $e^2h$.

## 1.4 Circular motion, gravitation and SHM

**Circular motion.** $\omega=\frac{2\pi}{T}=2\pi f$, $v=\omega r$, $a_c=\frac{v^2}{r}=\omega^2r$ toward the centre, $F_c=\frac{mv^2}{r}$ (supplied by tension, friction, gravity, normal reaction — not a separate force). *Conical pendulum:* $T\cos\theta=mg$, $T\sin\theta=\frac{mv^2}{r}$, period $2\pi\sqrt{\frac{L\cos\theta}{g}}$. *Level turn:* $v_{\max}=\sqrt{\mu rg}$. *Banking* (no friction): $\tan\theta=\frac{v^2}{rg}$. *Vertical circle:* $T_{\text{top}}=\frac{mv_t^2}{r}-mg$; $v_{\text{top,min}}=\sqrt{gr}$, $v_{\text{bottom,min}}=\sqrt{5gr}$. Over a convex bridge the apparent weight is $m(g-\frac{v^2}{r})$.

**Gravitation.** $F=\dfrac{Gm_1m_2}{r^2}$, $G=6.67\times10^{-11}$. $g=\dfrac{GM}{R^2}$; at height $h$: $g'=g\big(\frac{R}{R+h}\big)^2$ ($=\frac{g}{4}$ at $h=R$); at depth $d$: $g'=g\big(1-\frac{d}{R}\big)$; with latitude $\lambda$: $g'=g-\omega^2R\cos^2\lambda$ (zero effect at the poles). Gravitational potential $V=-\frac{GM}{r}$, PE $=-\frac{GMm}{r}$. **Escape speed** $v_e=\sqrt{\frac{2GM}{R}}=\sqrt{2gR}=11.2$ km/s; $v_{\text{orbit}}=\sqrt{\frac{GM}{r}}$ (near Earth $\sqrt{gR}=7.9$ km/s), so $v_e=\sqrt{2}v_o$. **Kepler:** $T^2\propto r^3$; $T=2\pi\sqrt{\frac{r^3}{GM}}$. Orbital energy: $K=\frac{GMm}{2r}$, $E=-\frac{GMm}{2r}$. A **geostationary** satellite has $T=24$ h, orbit radius $\approx42{,}400$ km (height $\approx36{,}000$ km), moves west to east above the equator. Weightlessness in orbit: free fall. Rocket: thrust $=v_{\text{rel}}\frac{dm}{dt}$; multi-stage design sheds dead mass to reach the required speed.

**SHM.** $a=-\omega^2x$, $x=A\sin(\omega t+\phi)$, $v=\omega\sqrt{A^2-x^2}$, $v_{\max}=A\omega$, $a_{\max}=A\omega^2$. Spring–mass $T=2\pi\sqrt{\frac{m}{k}}$ (series springs $k=\frac{k_1k_2}{k_1+k_2}$, parallel $k_1+k_2$); simple pendulum $T=2\pi\sqrt{\frac{l}{g}}$ (a seconds pendulum has $T=2$ s, $l\approx0.994$ m). Energy $E=\frac{1}{2}kA^2=\frac{1}{2}m\omega^2A^2$; $K=\frac{1}{2}k(A^2-x^2)$, $U=\frac{1}{2}kx^2$; both oscillate at twice the frequency; $K=U$ at $x=\frac{A}{\sqrt{2}}$. Damped oscillations lose amplitude to friction; **forced oscillations** have the driver's frequency and the amplitude peaks at **resonance** ($f_{\text{driver}}=f_0$).

## 1.5 Rotational dynamics

$I=\sum mr^2$; $K_{\text{rot}}=\frac{1}{2}I\omega^2$; $\tau=I\alpha=\vec r\times\vec F$; $L=I\omega$; $\tau=\frac{dL}{dt}$; $P=\tau\omega$. Radius of gyration $k=\sqrt{I/M}$.

| Body (axis) | $I$ |
|---|---|
| ring / hollow cylinder (central axis) | $MR^2$ |
| disc / solid cylinder (central axis) | $\frac{1}{2}MR^2$ |
| solid sphere (diameter) | $\frac{2}{5}MR^2$ |
| hollow sphere (diameter) | $\frac{2}{3}MR^2$ |
| thin rod (centre, perpendicular) / (end) | $\frac{ML^2}{12}$ / $\frac{ML^2}{3}$ |

Parallel-axis theorem $I=I_{cm}+Md^2$; perpendicular-axis (planar) $I_z=I_x+I_y$. Rolling without slipping: $K=\frac{1}{2}Mv^2\big(1+\frac{k^2}{R^2}\big)$; down an incline $a=\frac{g\sin\theta}{1+k^2/R^2}$. **Conservation of angular momentum:** $I_1\omega_1=I_2\omega_2$ (a skater pulling arms in spins faster). Centre of mass $\frac{\sum m\vec r}{\sum m}$; for uniform gravity the centre of gravity coincides with it. A body is in equilibrium when $\sum F=0$ and $\sum\tau=0$.

## 1.6 Elasticity

Stress $=\frac{F}{A}$, strain $=\frac{\Delta L}{L}$. **Hooke's law:** stress $\propto$ strain within the elastic limit. $Y=\dfrac{FL}{A\,\Delta L}$; bulk modulus $K=-\dfrac{\Delta P}{\Delta V/V}$ (compressibility $1/K$); rigidity $\eta=\dfrac{F/A}{\theta}$. **Poisson's ratio** $\sigma=\frac{\text{lateral strain}}{\text{longitudinal strain}}$, between $-1$ and $0.5$. Energy stored $=\frac{1}{2}F\Delta L$ per unit volume $\frac{1}{2}\times\text{stress}\times\text{strain}=\frac{\text{stress}^2}{2Y}$. Extension $\propto\frac{L}{r^2}$ for the same material and force. Relations: $Y=3K(1-2\sigma)=2\eta(1+\sigma)$. Steel has a higher $Y$ than rubber (it is *more* elastic in the physics sense). Elastic after-effect, fatigue, yield point, breaking stress are read from the stress–strain graph. Pressure at depth $h$ in the sea decreases the volume of a ball by $\frac{\rho gh}{K}$ (fraction).

## 1.7 Fluid mechanics

**Pressure** $P=P_0+\rho gh$; Pascal's law (hydraulic press, force ratio = area ratio). **Archimedes:** buoyant force $=\rho_{\text{fluid}}Vg$; a body floats when its weight equals the buoyancy; ice (900 kg m⁻³) floats with $\frac{9}{10}$ submerged; apparent weight in a liquid $=W-F_B$.

**Surface tension** $T=\frac{F}{l}$ (N m⁻¹) $=\frac{\text{energy}}{\text{area}}$. Excess pressure: bubble with one surface $\frac{2T}{r}$, soap bubble (two surfaces) $\frac{4T}{r}$. Work to blow a soap bubble of radius $r$: $8\pi r^2T$. **Capillary rise** $h=\dfrac{2T\cos\theta}{r\rho g}$ ($h\propto1/r$; mercury, with $\theta>90^\circ$, is depressed). Surface tension falls with temperature and with detergent.

**Viscosity.** $F=\eta A\frac{dv}{dx}$ (Newton). **Stokes' law** $F=6\pi\eta rv$; **terminal velocity** $v_t=\dfrac{2r^2(\rho-\sigma)g}{9\eta}$ ($\propto r^2$). **Poiseuille** $\dfrac{dV}{dt}=\dfrac{\pi Pr^4}{8\eta l}$ ($\propto r^4$). **Reynold number** $R_e=\dfrac{\rho vD}{\eta}$; below about 2000 the flow is streamline (laminar), above about 3000 turbulent.

**Continuity** $A_1v_1=A_2v_2$ (incompressible). **Bernoulli** $P+\frac{1}{2}\rho v^2+\rho gh=\text{constant}$ — conservation of energy along a streamline. Uses: Venturi meter, aerofoil lift, atomiser, speed of efflux $v=\sqrt{2gh}$ (Torricelli).

::: caution Traps in mechanics
- Centripetal force is not an extra force on a free-body diagram.
- A satellite in orbit is *not* beyond gravity; it is in free fall.
- In an inelastic collision momentum is conserved, kinetic energy is not.
- Banking-angle questions give $v$ in km/h: convert first.
- Capillary height is *inversely* proportional to radius; Poiseuille flow goes as $r^4$.
:::

```photogrid label="1.1" cols="2" ratio="1.2" caption="Pascal's law at work. (a) A workshop trolley jack: a small piston pushed by hand and a large piston under the car share one oil-filled space, so the pressure is the same in both. (b) The numbers for a jack with a 2 cm small piston and an 8 cm large piston, computed here. The force is multiplied by the area ratio, but the small piston must travel the same ratio further, so the work done is unchanged: a machine gives force, never energy."
@ photo id="ioephy/jack" cap="A hydraulic jack: one pressure, two piston areas"
fit 1.2
focus 0.5 0.5
@ svg cap="Force gain 16x, distance loss 16x, same work"
import math
d1, d2, F1 = 0.02, 0.08, 100.0
A1, A2 = math.pi * (d1 / 2) ** 2, math.pi * (d2 / 2) ** 2
P = F1 / A1; F2 = P * A2; ratio = A2 / A1
s2 = 0.01; s1 = s2 * ratio
assert abs(ratio - 16) < 1e-9 and abs(F2 - 1600) < 1e-6 and abs(F1 * s1 - F2 * s2) < 1e-9
W = 1000 * 9.8; need = W / ratio
f = Fig(300, 236)
f.box(30, 70, 50, 70, "", fill=BLUE, stroke=NAVY, r=2); f.box(30, 52, 50, 14, "", fill=NAVY, stroke=NAVY, r=2)
f.box(200, 70, 80, 70, "", fill=BLUE, stroke=NAVY, r=2); f.box(200, 52, 80, 14, "", fill=NAVY, stroke=NAVY, r=2)
f.box(30, 140, 250, 18, "", fill=BLUE, stroke=NAVY, r=2)
f.arrow([(55, 14), (55, 48)], color=RED, label="F1 = %d N" % F1, lpos=(100, 24), lsize=10.5)
f.arrow([(240, 14), (240, 48)], color=TEAL, label="F2 = %s N" % format(round(F2), ","), lpos=(240, 8), lsize=10.5)
f.text(55, 112, "A1", size=10.5, color=NAVY, bold=True); f.text(240, 112, "A2", size=10.5, color=NAVY, bold=True)
f.text(150, 178, "P = F1/A1 = %s Pa in both" % format(round(P), ","), size=10.5, color=NAVY, bold=True)
f.text(150, 196, "A2/A1 = %d,  s1 = %d cm for s2 = 1 cm" % (round(ratio), round(s1 * 100)), size=10.5, color=SLATE)
f.text(150, 214, "work: %d J in = %d J out" % (round(F1 * s1), round(F2 * s2)), size=10.5, color=TEAL, bold=True)
f.text(150, 230, "lifting 1,000 kg needs only %d N" % round(need), size=10.5, color=AMBER, bold=True)
```

## Formula and fact sheet

| Quantity | Formula |
|---|---|
| range, max height | $\frac{u^2\sin2\theta}{g}$, $\frac{u^2\sin^2\theta}{2g}$ |
| friction | $\mu=\tan\alpha$ (repose) |
| inelastic KE loss | $\frac{1}{2}\frac{m_1m_2}{m_1+m_2}(u_1-u_2)^2$ |
| banking | $\tan\theta=\frac{v^2}{rg}$ |
| $v_e$, $v_o$ | $\sqrt{2gR}$, $\sqrt{gR}$ |
| SHM | $T=2\pi\sqrt{m/k}$, $2\pi\sqrt{l/g}$ |
| rolling ratio | $K_{tr}:K_{rot}=1:\frac{k^2}{R^2}$ |
| $Y$ | $\frac{FL}{A\Delta L}$ |
| capillary | $h=\frac{2T\cos\theta}{r\rho g}$ |
| terminal speed | $\frac{2r^2(\rho-\sigma)g}{9\eta}$ |
| Poiseuille | $\frac{\pi Pr^4}{8\eta l}$ |

## Chapter summary

- Check units by dimensions; use $\sin2\theta$ for range, $\sin^2\theta$ for height.
- Momentum is conserved in every collision; kinetic energy only in elastic ones.
- For circular and orbital motion identify what supplies the centripetal force.
- SHM periods depend only on the system constants ($m,k$ or $l,g$), not on amplitude.
- Angular momentum conservation changes $\omega$ when $I$ changes.
- Elastic energy density is $\frac{1}{2}\times$ stress $\times$ strain.
- Fluids: continuity first for speeds, then Bernoulli for pressure.

## Practice questions

**Set A — Recall (14 questions)**

1. The dimensional formula of work is
   (a) $[MLT^{-2}]$ (b) $[ML^2T^{-2}]$ (c) $[ML^2T^{-3}]$ (d) $[ML^{-1}T^{-2}]$
2. A projectile is launched at $45^\circ$ with a speed of 20 m s⁻¹ ($g=10$ m s⁻²). Its range is
   (a) 20 m (b) 80 m (c) 40 m (d) 10 m
3. A force of 10 N acts for 3 s on a 5 kg body initially at rest. Its final speed is
   (a) 6 m s⁻¹ (b) 2 m s⁻¹ (c) 15 m s⁻¹ (d) 50 m s⁻¹
4. The kinetic energy of a 2 kg body moving at 3 m s⁻¹ is
   (a) 6 J (b) 18 J (c) 12 J (d) 9 J
5. The power needed to lift a 100 kg load through 10 m in 10 s ($g=10$) is
   (a) 100 W (b) 1000 W (c) 10000 W (d) 10 W
6. A body moves at 10 m s⁻¹ on a circle of radius 5 m. Its centripetal acceleration is
   (a) 2 m s⁻² (b) 50 m s⁻² (c) 20 m s⁻² (d) 10 m s⁻²
7. The escape speed from the Earth's surface is nearly
   (a) 7.9 km s⁻¹ (b) 9.8 km s⁻¹ (c) 8 km s⁻¹ (d) 11.2 km s⁻¹
8. If the length of a simple pendulum is made four times, its time period
   (a) halves (b) doubles (c) quadruples (d) is unchanged
9. The moment of inertia of a solid sphere about a diameter is
   (a) $\frac{1}{2}MR^2$ (b) $\frac{2}{3}MR^2$ (c) $\frac{2}{5}MR^2$ (d) $MR^2$
10. The maximum theoretical value of Poisson's ratio is
    (a) 0.5 (b) 1 (c) 0.25 (d) 0.33
11. Ice of density 900 kg m⁻³ floats in water with the fraction submerged equal to
    (a) $1/10$ (b) $1/2$ (c) $3/4$ (d) $9/10$
12. Bernoulli's theorem expresses the conservation of
    (a) energy (b) momentum (c) mass (d) angular momentum
13. The SI unit of surface tension is
    (a) N m (b) N m⁻² (c) N m⁻¹ (d) J m⁻³
14. A block just starts to slide when a plane is tilted to $30^\circ$. The coefficient of static friction is
    (a) 0.866 (b) 0.5 (c) 1.73 (d) 0.577

::: note Answers and explanations — Set A
**1.** (b) — force × distance. (a) is force.
**2.** (c) — $R=\frac{u^2\sin90^\circ}{g}=\frac{400}{10}=40$ m.
**3.** (a) — impulse: $v=\frac{Ft}{m}=\frac{30}{5}=6$.
**4.** (d) — $\frac{1}{2}\cdot2\cdot9=9$ J.
**5.** (b) — $\frac{mgh}{t}=\frac{100\cdot10\cdot10}{10}=1000$ W.
**6.** (c) — $v^2/r=100/5=20$.
**7.** (d) — $\sqrt{2gR}=11.2$ km s⁻¹; 7.9 km s⁻¹ is the orbital speed near the surface.
**8.** (b) — $T\propto\sqrt{l}$.
**9.** (c) — $\frac{2}{5}MR^2$; (b) is the hollow sphere.
**10.** (a) — theory limits: $-1<\sigma<0.5$.
**11.** (d) — $\rho_{ice}/\rho_{water}=0.9$.
**12.** (a) — it is the work–energy theorem for a flowing fluid.
**13.** (c) — force per unit length.
**14.** (d) — $\mu=\tan30^\circ=0.577$.
:::

**Set B — Understanding (10 questions)**

1. A ball is thrown at $60^\circ$ to the horizontal with speed 20 m s⁻¹ ($g=10$). Its maximum height is
   (a) 10 m (b) 15 m (c) 20 m (d) 30 m
2. Two forces of 10 N each act at $120^\circ$ to each other. Their resultant is
   (a) 20 N (b) $10\sqrt{3}$ N (c) 10 N (d) 0
3. A 2 kg block on a rough floor ($\mu=0.2$, $g=10$) is pushed by a 10 N horizontal force. Its acceleration is
   (a) 5 m s⁻² (b) 3 m s⁻² (c) 4 m s⁻² (d) 2 m s⁻²
4. A 2 kg body moving at 4 m s⁻¹ collides and sticks to a stationary 2 kg body. The kinetic energy lost is
   (a) 4 J (b) 16 J (c) 0 (d) 8 J
5. A frictionless banked road must let a car take a bend of radius 10 m at 10 m s⁻¹ ($g=10$). The banking angle is
   (a) $45^\circ$ (b) $30^\circ$ (c) $60^\circ$ (d) $37^\circ$
6. A particle moves as $x=0.1\sin(10t)$ (SI). Its maximum speed is
   (a) 0.1 m s⁻¹ (b) 10 m s⁻¹ (c) 1 m s⁻¹ (d) 100 m s⁻¹
7. A 2 kg mass hangs on a spring of constant 200 N m⁻¹. The period of its oscillation is
   (a) $0.2\pi$ s (b) $2\pi$ s (c) $0.02\pi$ s (d) $\pi$ s
8. The time period of a geostationary satellite is
   (a) 12 h (b) 90 min (c) 6 h (d) 24 h
9. A disc of mass 2 kg and radius 0.5 m is acted on by a torque of 0.5 N m about its axis. Its angular acceleration is
   (a) 2 rad s⁻² (b) 1 rad s⁻² (c) 0.5 rad s⁻² (d) 4 rad s⁻²
10. A wire has twice the length and twice the radius of another of the same material. Under the same force its extension is
    (a) 2 times (b) $\frac{1}{2}$ times (c) $\frac{1}{4}$ times (d) the same

::: note Answers and explanations — Set B
**1.** (b) — $H=\frac{u^2\sin^2\theta}{2g}=\frac{400\cdot0.75}{20}=15$.
**2.** (c) — equal vectors at $120^\circ$ give a resultant equal to each.
**3.** (b) — $a=\frac{10-0.2\cdot2\cdot10}{2}=3$.
**4.** (d) — $v=2$ m s⁻¹; $K_i=16$ J, $K_f=\frac{1}{2}\cdot4\cdot4=8$ J; loss 8 J.
**5.** (a) — $\tan\theta=\frac{v^2}{rg}=1$.
**6.** (c) — $v_{\max}=A\omega=0.1\times10$.
**7.** (a) — $T=2\pi\sqrt{2/200}=0.2\pi$ s $\approx0.63$ s.
**8.** (d) — it must match the Earth's rotation.
**9.** (a) — $I=\frac{1}{2}MR^2=0.25$; $\alpha=\frac{0.5}{0.25}=2$.
**10.** (b) — $\Delta L\propto\frac{L}{r^2}=\frac{2}{4}$.
:::

**Set C — Application (8 questions)**

1. A stone is thrown horizontally at 10 m s⁻¹ from a 20 m high tower ($g=10$). It lands at a horizontal distance of
   (a) 10 m (b) 14 m (c) 40 m (d) 20 m
2. A 1000 kg car moving at 20 m s⁻¹ is stopped by brakes in 40 m. The average braking force is
   (a) 5000 N (b) 10000 N (c) 2500 N (d) 500 N
3. At a height equal to the Earth's radius, the acceleration due to gravity is ($g=9.8$ at the surface)
   (a) 4.9 m s⁻² (b) 3.27 m s⁻² (c) 2.45 m s⁻² (d) 1.1 m s⁻²
4. A stone on a 0.5 m string is whirled in a vertical circle. The minimum speed at the bottom to complete the circle is ($g=10$)
   (a) 5 m s⁻¹ (b) 2.5 m s⁻¹ (c) 7.07 m s⁻¹ (d) 10 m s⁻¹
5. A skater spinning at 2 rad s⁻¹ with $I=4$ kg m² pulls in her arms so that $I=1$ kg m². Her new angular speed is
   (a) 0.5 rad s⁻¹ (b) 4 rad s⁻¹ (c) 8 rad s⁻¹ (d) 16 rad s⁻¹
6. Water ($\rho=1000$) flows at 2 m s⁻¹ in a pipe of area 4 cm² that narrows to 1 cm². The pressure drop in the narrow part is
   (a) 28 kPa (b) 30 kPa (c) 32 kPa (d) 60 kPa
7. Water rises 3 cm in a capillary tube. In a tube of half the radius it rises
   (a) 6 cm (b) 3 cm (c) 12 cm (d) 1.5 cm
8. Two identical spheres fall through the same liquid; one has twice the radius. Ratio of terminal speeds (larger : smaller) is
   (a) 2 (b) 8 (c) 16 (d) 4

::: note Answers and explanations — Set C
**1.** (d) — $t=\sqrt{2h/g}=2$ s; $x=10\cdot2=20$ m.
**2.** (a) — $F=\frac{\frac{1}{2}mv^2}{d}=\frac{200000}{40}$.
**3.** (c) — $g'=g\big(\frac{R}{2R}\big)^2=\frac{g}{4}=2.45$.
**4.** (a) — $v=\sqrt{5gr}=\sqrt{25}$.
**5.** (c) — $L=I\omega$: $4\times2=1\times\omega$.
**6.** (b) — $v_2=8$ m s⁻¹ by continuity; $\Delta P=\frac{1}{2}\cdot1000\,(64-4)=30000$ Pa.
**7.** (a) — $h\propto\frac{1}{r}$: halving the radius doubles the rise.
**8.** (d) — $v_t\propto r^2$, ratio 4.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Derive the time of flight, maximum height and range of a projectile and solve a numerical. <span class="marks">[10]</span>
2. Explain motion in a horizontal circle, a banked road and a vertical circle, with the condition for completing the loop. <span class="marks">[10]</span>
3. State and prove the equation of continuity and Bernoulli's principle; give four applications and a numerical. <span class="marks">[10]</span>

```photogrid label="1.H" cols="4" ratio="1.25" caption="Mechanics in practice. (a) A hydraulic jack multiplies force by Pascal's law. (b) A kite is held by the balance of tension, weight and wind force. (c) A beam balance compares masses by balancing torques. (d) A vernier caliper reads lengths to 0.1 mm."
@ photo id="ioephy/jack" cap="(a) Hydraulic jack"
fit 1.25
focus 0.5 0.5
@ photo id="phy11/kite" cap="(b) Kite"
fit 1.25
focus 0.5 0.5
@ photo id="phy11/balance" cap="(c) Beam balance"
fit 1.25
focus 0.5 0.5
@ photo id="phy11/vernier" cap="(d) Vernier caliper"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Projectile motion (10 marks)

**Introduction.** A **projectile** is a body thrown into the air that then moves only under gravity (air resistance neglected). The path is a **parabola**, because the horizontal and vertical motions are independent.

**Derivation.** Let the body be thrown with speed $u$ at angle $\theta$ above the horizontal.

1. **Components:** $u_x = u\cos\theta$ (constant) and $u_y = u\sin\theta$ (changing by $-g$ each second).
2. **Time of flight:** the vertical displacement is zero at landing, so $0 = u\sin\theta\,T - \frac{1}{2}gT^2$ and
$$T=\frac{2u\sin\theta}{g}.$$
3. **Maximum height:** at the top $v_y = 0$, so $0 = u^2\sin^2\theta - 2gH$ and
$$H=\frac{u^2\sin^2\theta}{2g}.$$
4. **Range:** $R = u\cos\theta \times T = \frac{2u^2\sin\theta\cos\theta}{g}$, so
$$R=\frac{u^2\sin 2\theta}{g}.$$
5. **Maximum range** is at $\theta=45^\circ$, where $R_{\max}=u^2/g$. Angles $\theta$ and $(90^\circ-\theta)$ give the same range.
6. **Equation of path:** eliminating $t$ gives $y = x\tan\theta - \frac{gx^2}{2u^2\cos^2\theta}$, which is a parabola.

**Numerical.** A ball is thrown at $40\ \text{m s}^{-1}$ at $30^\circ$ ($g=10\ \text{m s}^{-2}$).

| Quantity | Working | Answer |
|---|---|---|
| Time of flight | $2\times40\times0.5/10$ | $4\ \text{s}$ |
| Maximum height | $1600\times0.25/20$ | $20\ \text{m}$ |
| Range | $1600\times0.866/10$ | $138.6\ \text{m}$ |
| Speed at the top | $40\cos30^\circ$ | $34.6\ \text{m s}^{-1}$ |

**Conclusion.** The horizontal speed never changes, and the height and time depend only on the vertical component, so a $45^\circ$ throw gives the longest range.

### Model answer D2: Circular motion (10 marks)

**Introduction.** A body in uniform circular motion has constant speed but changing direction, so it has a **centripetal acceleration** $a = \frac{v^2}{r} = \omega^2 r$ towards the centre, and needs a force $F = \frac{mv^2}{r}$.

**1. Horizontal circle.** A stone whirled on a string has tension as the centripetal force. A car on a flat road uses **friction**: $\mu mg \ge \frac{mv^2}{r}$, so the safe speed is $v \le \sqrt{\mu r g}$.

**2. Banked road.** For a road banked at angle $\theta$ the normal reaction has a horizontal part $N\sin\theta = \frac{mv^2}{r}$ and a vertical part $N\cos\theta = mg$. Dividing:
$$\tan\theta=\frac{v^2}{rg}.$$
For $v = 20\ \text{m s}^{-1}$ and $r = 100\ \text{m}$: $\tan\theta = 400/(100\times10) = 0.4$, so $\theta \approx 21.8^\circ$.

**3. Vertical circle** (mass $m$ on a string of length $r$).

1. At the **top**: $T + mg = \frac{mv_{t}^2}{r}$. The least speed is when $T = 0$, so $v_{t} = \sqrt{gr}$.
2. At the **bottom**: $T - mg = \frac{mv_b^2}{r}$.
3. By conservation of energy, $\frac{1}{2}mv_b^2 = \frac{1}{2}mv_t^2 + mg(2r)$, so $v_b^2 = v_t^2 + 4gr$.
4. For the minimum case $v_b = \sqrt{5gr}$.
5. The tension difference between the bottom and top is $6mg$.

**Numerical.** For $r = 0.9\ \text{m}$ and $g = 10$: $v_{t} = \sqrt{9} = 3\ \text{m s}^{-1}$ and $v_b = \sqrt{45} = 6.7\ \text{m s}^{-1}$.

| Case | Centripetal force from | Condition |
|---|---|---|
| Stone on string | Tension | $T = mv^2/r$ |
| Flat road | Friction | $v \le \sqrt{\mu rg}$ |
| Banked road | Component of $N$ | $\tan\theta = v^2/rg$ |
| Vertical loop | Tension + weight | $v_b \ge \sqrt{5gr}$ |
| Satellite | Gravity | $v = \sqrt{GM/r}$ |

**Conclusion.** Every circular motion needs a net inward force, and for the vertical loop the string must stay taut at the top.

### Model answer D3: Equation of continuity and Bernoulli's principle (10 marks)

**Introduction.** For an ideal fluid (incompressible, non-viscous, steady flow) two laws describe the flow: conservation of mass and conservation of energy.

**Equation of continuity.** The mass entering a pipe per second equals the mass leaving, so $A_1v_1 = A_2v_2$. The fluid speeds up where the pipe narrows.

**Bernoulli's principle.** Along a streamline
$$P + \frac{1}{2}\rho v^2 + \rho gh = \text{constant}.$$
**Proof (outline).** The work done by the pressure difference on a small volume $V$ is $(P_1 - P_2)V$. This equals the gain in kinetic energy, $\frac{1}{2}\rho V(v_2^2 - v_1^2)$, plus the gain in potential energy, $\rho V g(h_2 - h_1)$. Dividing by $V$ gives the result.

**Applications.**

1. **Torricelli's theorem:** the speed of efflux from a hole at depth $h$ is $v = \sqrt{2gh}$.
2. **Venturi meter:** measures flow speed from the pressure drop in a narrow throat.
3. **Aerofoil lift:** faster air over the curved top gives lower pressure than below.
4. **Atomiser and spray gun:** fast air over a tube lowers the pressure and draws liquid up.

**Numerical.** In a pipe $A_1 = 20\ \text{cm}^2$, $v_1 = 2\ \text{m s}^{-1}$ and $A_2 = 5\ \text{cm}^2$. Then $v_2 = 20\times2/5 = 8\ \text{m s}^{-1}$, and (horizontal pipe, water) $P_1 - P_2 = \frac{1}{2}\times1000\times(64 - 4) = 30{,}000\ \text{Pa}$. For a tank with a hole at $1.8\ \text{m}$ depth, $v = \sqrt{2\times10\times1.8} = 6\ \text{m s}^{-1}$.

| Law | Conserves | Equation |
|---|---|---|
| Continuity | Mass | $Av = \text{constant}$ |
| Bernoulli | Energy | $P + \frac{1}{2}\rho v^2 + \rho gh = \text{constant}$ |
| Pascal | Pressure transmission | $F_1/A_1 = F_2/A_2$ (hydraulic jack) |

**Conclusion.** Where a fluid moves faster its pressure is lower, which explains the flight of aeroplanes and the working of sprays and flow meters.

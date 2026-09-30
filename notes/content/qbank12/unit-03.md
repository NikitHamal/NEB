---
subject: Question Bank
grade: 12
unit: 3
title: "Physics: Unit-wise Subjective Question Bank"
hours: 0
area: Physics
---

Group B (eight questions of 5 marks) and Group C (three questions of 8 marks) carry
sixty-four of the seventy-five written marks in NEB Grade 12 Physics. This chapter
takes the twenty-five CDC units in syllabus order, and in every unit it gives a set of
short-answer questions (the shape of a Group B question, often split $1+2+2$ or
$2+3$), a set of long-answer questions (the shape of a Group C question, split
$2+2+2+2$, $3+3+2$ or $5+3$), and a complete model answer to each, written at the
length and in the order a full-mark script would follow.

::: key How to use a section
Attempt each question on paper *before* opening the model answer. Mark yourself
part by part against the answer, because the examiner awards marks part by part too:
a derivation earns its marks for the **starting law**, the **steps** and the
**boxed result**; a numerical earns them for the **formula**, the **substitution with
units** and the **answer**. Read the Examiner's note at the end of each section last —
it lists what the marker looks for and the mistakes that cost marks in real papers.
:::

::: caution What a year tag means here
**(NEB 2081)** is printed only on a question that we saw in that year's board paper;
**(NEB 2079 model)** marks the official NEB model question for 2079, which we
downloaded and read. A tag covers the *question as set*; where the printed question
depended on a figure we could not reproduce, the data in the stem have been rebuilt
and the question is given without a tag. The 2078 paper circulates under two labels
(board and model); it is tagged **(NEB 2078)** and its label is treated as disputed.
Untagged questions are original practice questions of the same pattern, not
leaked papers.
:::

## 3.1 Rotational dynamics

CDC allots **7 teaching hours**. The unit produces a Group B question almost every
year: the moment of inertia of a rod, a conservation-of-angular-momentum argument
(the ballet dancer, the rotating platform, the Earth), or a torque–energy numerical
on a flywheel. It supplies the opening part of longer questions too.

**Short answer questions [5 marks each]**

1. (a) Define moment of inertia. [1] (b) Derive the moment of inertia of a uniform rod about an axis through one end and perpendicular to its length. [2] (c) A flywheel of moment of inertia $0.32\ \text{kg m}^{2}$ rotates at $120\ \text{rad s}^{-1}$, driven by a motor of power $50\ \text{W}$. Find its kinetic energy and the frictional couple. [2] <span class="marks">[5]</span> (NEB 2081)
2. (a) Define radius of gyration. [1] (b) Find the moment of inertia of a thin uniform rod about a perpendicular axis through its centre. [2] (c) A teacher sitting on a rotating platform with her arms outstretched turns at $1.5\ \text{rad s}^{-1}$; she pulls her arms in and the speed becomes $5.0\ \text{rad s}^{-1}$. Find the ratio of her final to initial kinetic energy. [2] <span class="marks">[5]</span> (NEB 2080)
3. (a) Why does a ballet dancer spin faster when she folds her arms? [2] (b) Establish the relation between torque and moment of inertia. [2] (c) Why is a wrench with a longer handle easier to use? [1] <span class="marks">[5]</span> (NEB 2082)
4. (a) Why does the angular velocity of the Earth about the Sun increase when it is nearer the Sun? [2] (b) If the Earth suddenly shrank without loss of mass, what would happen to the length of the day? [2] (c) State the law you used in both parts. [1] <span class="marks">[5]</span> (NEB 2078)
5. (a) Write the equations of angular motion and deduce the relations between linear and angular quantities. [3] (b) A wheel turning at $120\ \text{rev min}^{-1}$ is brought uniformly to rest in $20\ \text{s}$. Find the angular retardation and the number of revolutions it makes. [2] <span class="marks">[5]</span>
6. (a) Show that the kinetic energy of a rotating rigid body is $\tfrac12I\omega^{2}$. [3] (b) A solid body has $I = 0.8\ \text{kg m}^{2}$ and $K = 160\ \text{J}$; find its angular momentum. [2] <span class="marks">[5]</span>

::: note Model answers — short (1–3)
**1.** (a) The **moment of inertia** of a body about an axis is the sum $\sum mr^{2}$ of the products of the mass of each particle and the square of its perpendicular distance from the axis. It is the rotational analogue of mass: it measures the body's resistance to a change in its rotation. Unit: $\text{kg m}^{2}$.

(b) For a uniform rod of mass $M$ and length $l$, take an element of length $dx$ at distance $x$ from the end; its mass is $dm = (M/l)\,dx$.
$$ I_{end} = \int_0^{l}x^{2}\,\frac{M}{l}\,dx = \frac{M}{l}\cdot\frac{l^{3}}{3} = \frac{Ml^{2}}{3} $$

(c) Kinetic energy and frictional couple:
$$ K = \tfrac12I\omega^{2} = \tfrac12(0.32)(120)^{2} = 2304\ \text{J} $$
At a steady speed the motor's power is used entirely against friction, $P = \tau\omega$:
$$ \tau = \frac{P}{\omega} = \frac{50}{120} = 0.42\ \text{N m} $$

**2.** (a) The **radius of gyration** $k$ is the distance from the axis at which the whole mass of the body could be concentrated without changing its moment of inertia: $I = Mk^{2}$, so $k = \sqrt{I/M}$.

(b) Integrate from the centre outwards, $x$ from $-l/2$ to $+l/2$:
$$ I_{cm} = \int_{-l/2}^{l/2}x^{2}\,\frac{M}{l}\,dx = \frac{M}{l}\left[\frac{x^{3}}{3}\right]_{-l/2}^{l/2} = \frac{Ml^{2}}{12} $$

(c) There is no external torque on the platform, so the angular momentum is conserved, $I_1\omega_1 = I_2\omega_2$. Since $K = \tfrac12I\omega^{2} = \tfrac12L\omega$ and $L$ is constant,
$$ \frac{K_2}{K_1} = \frac{\omega_2}{\omega_1} = \frac{5.0}{1.5} = 3.3 $$
The kinetic energy rises $3.3$ times; the extra energy is the work her muscles do pulling her arms in against the outward tendency of the mass.

**3.** (a) With no external torque on her, her angular momentum $L = I\omega$ stays constant. Folding her arms brings the mass close to the axis, so $I$ decreases; to keep $L$ constant her angular velocity $\omega$ must increase. Extending them again increases $I$ and slows her.

(b) A particle of mass $m$ at distance $r$ from the axis, acted on by a tangential force $F$, has tangential acceleration $a = r\alpha$, so $F = mr\alpha$. Its torque about the axis is $\tau = Fr = mr^{2}\alpha$. For the whole rigid body, all particles share the same $\alpha$:
$$ \tau = \Big(\sum mr^{2}\Big)\alpha = I\alpha $$

(c) The torque is $\tau = Fr$; a longer handle increases the perpendicular distance $r$, so a smaller force $F$ gives the same torque.
:::

::: note Model answers — short (4–6)
**4.** (a) The Earth is subject only to the Sun's gravitational pull, which acts along the line joining them and so has **zero torque** about the Sun. Its orbital angular momentum $L = mr^{2}\omega$ is therefore conserved. When $r$ decreases, $\omega$ must increase — equivalently the radius vector sweeps equal areas in equal times (Kepler's second law).

(b) The Earth's spin angular momentum $L = I\omega$ is conserved, since no external torque acts. Shrinking decreases $I$ (for a sphere $I\propto R^{2}$), so $\omega$ increases and the **day becomes shorter**. For example, if $R$ fell to half, $I$ would fall to a quarter and the day would be $24/4 = 6\ \text{h}$.

(c) The **law of conservation of angular momentum**: if the resultant external torque on a system is zero, its total angular momentum remains constant.

**5.** (a) For constant angular acceleration $\alpha$, starting with angular velocity $\omega_0$:
$$ \omega = \omega_0+\alpha t $$
$$ \theta = \omega_0t+\tfrac12\alpha t^{2} $$
$$ \omega^{2} = \omega_0^{2}+2\alpha\theta $$
A point at distance $r$ from the axis moves along an arc $s = r\theta$, so $v = r\omega$ and the tangential acceleration is $a = r\alpha$.

(b) $\omega_0 = 120\times2\pi/60 = 12.57\ \text{rad s}^{-1}$, $\omega = 0$, $t = 20\ \text{s}$.
$$ \alpha = \frac{\omega-\omega_0}{t} = \frac{0-12.57}{20} = -0.63\ \text{rad s}^{-2} $$
$$ \theta = \frac{\omega_0+\omega}{2}\,t = \frac{12.57}{2}\times20 = 125.7\ \text{rad} $$
Number of revolutions $= 125.7/2\pi = 20$.

**6.** (a) A rigid body is made of particles $m_1, m_2,\dots$ at distances $r_1, r_2,\dots$ from the axis, all turning at the same $\omega$. Particle $i$ moves with speed $v_i = r_i\omega$, so its kinetic energy is $\tfrac12m_ir_i^{2}\omega^{2}$. Summing over all particles,
$$ K = \tfrac12\Big(\sum m_ir_i^{2}\Big)\omega^{2} = \tfrac12I\omega^{2} $$

(b) $K = L^{2}/2I$, so
$$ L = \sqrt{2IK} = \sqrt{2\times0.8\times160} = \sqrt{256} = 16\ \text{kg m}^{2}\text{s}^{-1} $$
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Define moment of inertia and radius of gyration. [2] (b) Derive the moment of inertia of a uniform rod about a perpendicular axis through its centre and, using the parallel-axis theorem, about one end. [4] (c) A uniform rod of mass $1.2\ \text{kg}$ and length $0.60\ \text{m}$ is pivoted at one end and released from the horizontal. Find the angular acceleration at release. [2] <span class="marks">[8]</span>
2. (a) Derive $\tau = I\alpha$ for a rigid body. [2] (b) Deduce the expressions for work and power in rotational motion. [3] (c) A flywheel of moment of inertia $2.5\ \text{kg m}^{2}$ is acted on by a constant torque of $10\ \text{N m}$ for $5.0\ \text{s}$, starting from rest. Find its final angular velocity, the work done, the final kinetic energy and the instantaneous power at $5.0\ \text{s}$. [3] <span class="marks">[8]</span>
3. (a) State the law of conservation of angular momentum. [1] (b) A horizontal disc of moment of inertia $0.50\ \text{kg m}^{2}$ rotates freely at $4.0\ \text{rad s}^{-1}$. A small lump of putty of mass $0.10\ \text{kg}$ dropped on it sticks at a distance $0.40\ \text{m}$ from the axis. Find the new angular velocity and the loss of kinetic energy, and explain where the energy has gone. [4] (c) Explain why a diver tucks into a ball during a somersault. [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Moment of inertia** $I = \sum mr^{2}$ is the rotational analogue of mass. **Radius of gyration** $k = \sqrt{I/M}$ is the distance from the axis at which the whole mass would give the same $I$.

(b) Let the rod have mass $M$ and length $l$; a length $dx$ at distance $x$ from the centre has mass $(M/l)dx$.
$$ I_{cm} = \int_{-l/2}^{l/2}\frac{M}{l}x^{2}\,dx = \frac{M}{l}\cdot\frac{2}{3}\left(\frac{l}{2}\right)^{3} = \frac{Ml^{2}}{12} $$
The **parallel-axis theorem** states $I = I_{cm}+Md^{2}$, where $d$ is the distance between the parallel axes. For the end of the rod $d = l/2$:
$$ I_{end} = \frac{Ml^{2}}{12}+M\left(\frac{l}{2}\right)^{2} = \frac{Ml^{2}}{12}+\frac{Ml^{2}}{4} = \frac{Ml^{2}}{3} $$
which agrees with the direct integration from one end.

(c) At release the weight $Mg$ acts at the centre, distance $l/2$ from the pivot, so
$$ \tau = Mg\,\frac{l}{2},\qquad I = \frac{Ml^{2}}{3} $$
$$ \alpha = \frac{\tau}{I} = \frac{Mgl/2}{Ml^{2}/3} = \frac{3g}{2l} = \frac{3\times9.8}{2\times0.60} = 24.5\ \text{rad s}^{-2} $$
The mass cancels: a heavier rod of the same length falls at the same rate.

**2.** (a) Consider particle $i$ of mass $m_i$ at distance $r_i$ with tangential force $F_i$. Its tangential acceleration is $r_i\alpha$, so $F_i = m_ir_i\alpha$ and its torque is $F_ir_i = m_ir_i^{2}\alpha$. Summing over all particles, since $\alpha$ is common to all,
$$ \tau = \alpha\sum m_ir_i^{2} = I\alpha $$

(b) A torque $\tau$ turning a body through a small angle $d\theta$ does work $dW = F\,ds = F\,r\,d\theta = \tau\,d\theta$. For a constant torque through angle $\theta$:
$$ W = \tau\theta $$
Dividing by the time taken:
$$ P = \frac{dW}{dt} = \tau\frac{d\theta}{dt} = \tau\omega $$

(c) $\alpha = \tau/I = 10/2.5 = 4.0\ \text{rad s}^{-2}$.
$$ \omega = \alpha t = 4.0\times5.0 = 20\ \text{rad s}^{-1} $$
$$ \theta = \tfrac12\alpha t^{2} = \tfrac12(4.0)(25) = 50\ \text{rad} $$
$$ W = \tau\theta = 10\times50 = 500\ \text{J} $$
$$ K = \tfrac12I\omega^{2} = \tfrac12(2.5)(20)^{2} = 500\ \text{J} $$
The two agree, as they must when no energy is lost. The instantaneous power is
$$ P = \tau\omega = 10\times20 = 200\ \text{W} $$
(the *average* power is $W/t = 100\ \text{W}$; the power grows linearly because $\omega$ does).

**3.** (a) If the resultant external torque on a system is zero, its total angular momentum is constant.

(b) The putty adds a moment of inertia $mr^{2} = 0.10\times(0.40)^{2} = 0.016\ \text{kg m}^{2}$, so $I_2 = 0.516\ \text{kg m}^{2}$. No external torque acts on the disc-and-putty system:
$$ I_1\omega_1 = I_2\omega_2\ \Rightarrow\ \omega_2 = \frac{0.50\times4.0}{0.516} = 3.88\ \text{rad s}^{-1} $$
$$ K_1 = \tfrac12(0.50)(4.0)^{2} = 4.00\ \text{J},\qquad K_2 = \tfrac12(0.516)(3.88)^{2} = 3.88\ \text{J} $$
$$ \Delta K = 4.00-3.88 = 0.12\ \text{J} $$
The lost energy has gone to heat and sound in the inelastic sticking of the putty, exactly as in a linear perfectly inelastic collision: momentum (here angular momentum) is conserved, kinetic energy is not.

(c) In the air there is no external torque about the centre of mass, so $L = I\omega$ is fixed. Tucking reduces $I$, so the diver rotates faster and completes the somersault; opening out before entry raises $I$ and slows the rotation for a clean entry.
:::

::: tip Examiner's note — Rotational dynamics
Quote the **starting principle** before the algebra — "no external torque, so $L$ is conserved" — because that sentence alone is worth a mark in every angular-momentum question. For the rod, always state the **limits** of the integral and the **element** $dm = (M/l)dx$; writing only the final $Ml^{2}/12$ earns one mark out of two. In flywheel numericals, check that the units of power and torque agree ($\text{W} = \text{N m s}^{-1}$), and do not confuse the energy $\tfrac12I\omega^{2}$ with the work $\tau\theta$ — they are equal only if no energy is lost to friction. Convert $\text{rev min}^{-1}$ to $\text{rad s}^{-1}$ first.
:::

## 3.2 Periodic motion

CDC allots **6 teaching hours**. Expect the vertical-spring derivation, an energy argument for SHM (often with a graph), a simple-pendulum item and, in recent papers, a build-your-own-SHM argument from a restoring force such as the earthquake question of 2078.

**Short answer questions [5 marks each]**

1. (a) Define simple harmonic motion. [1] (b) Derive an expression for the time period of a mass $m$ attached to a vertical spring of force constant $k$. [3] (c) What would the time period be inside an orbiting satellite? [1] <span class="marks">[5]</span> (NEB 2079 model)
2. (a) A particle moves as $y = r\sin\omega t$. Define amplitude and calculate the acceleration. [1+2] (b) A uniform spring is cut into two equal halves. What happens to the force constant and to the frequency of a given mass on one half? [1+1] <span class="marks">[5]</span> (NEB 2080)
3. (a) Show that the total energy in SHM is constant. [3] (b) Sketch the potential energy against displacement. [1] (c) What is the time period of a simple pendulum on the Moon, compared with that on Earth? [1] <span class="marks">[5]</span> (NEB 2082)
4. A spring of force constant $18\ \text{N m}^{-1}$ carries a mass $0.15\ \text{kg}$ and is pulled $4\ \text{cm}$ down and released. (a) Define SHM. [1] (b) Find the maximum acceleration and the time period. [2] (c) Write the expression for the total energy and draw the kinetic and potential energy graphs. [2] <span class="marks">[5]</span> (NEB 2081)
5. (a) Distinguish between free, damped and forced oscillations. [3] (b) What is resonance? Give two examples. [2] <span class="marks">[5]</span>
6. (a) Derive the time period of a simple pendulum. [3] (b) How can the $l$–$T^{2}$ graph be used to find $g$? [2] <span class="marks">[5]</span>

::: note Model answers — short (1–3)
**1.** (a) **Simple harmonic motion** is the periodic motion of a particle whose acceleration is directly proportional to its displacement from a fixed point (the mean position) and is always directed towards that point: $a = -\omega^{2}x$.

(b) At equilibrium the spring is stretched by $e$ so that $ke = mg$. If the mass is pulled a further distance $y$ down, the net restoring force is
$$ F = mg-k(e+y) = -ky $$
Newton's second law gives $ma = -ky$, so
$$ a = -\frac{k}{m}\,y = -\omega^{2}y,\qquad \omega^{2} = \frac{k}{m} $$
This is the defining equation of SHM, and
$$ T = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{m}{k}} $$

(c) The time period is **unchanged**. The expression for $T$ contains only $m$ and $k$, not $g$. In the satellite the mass and the spring are both "weightless", but the spring still exerts $-ky$ on the mass and its inertia is unchanged, so it oscillates with the same $T$. (A *simple pendulum* would not oscillate at all, since its restoring force is the weight.)

**2.** (a) **Amplitude** $r$ is the maximum displacement from the mean position. With $y = r\sin\omega t$,
$$ v = \frac{dy}{dt} = r\omega\cos\omega t,\qquad a = \frac{dv}{dt} = -r\omega^{2}\sin\omega t = -\omega^{2}y $$
The acceleration is proportional to the displacement, opposite in direction, with maximum value $r\omega^{2}$.

(b) A spring of half the length is twice as stiff, because the same force now stretches each of only half as many coils: **the force constant doubles** ($k' = 2k$). The frequency $f = \dfrac{1}{2\pi}\sqrt{k/m}$ therefore increases by the factor $\sqrt{2}$: $f' = \sqrt{2}\,f$.

**3.** (a) At displacement $x$ the speed is $v = \omega\sqrt{A^{2}-x^{2}}$, so
$$ K = \tfrac12mv^{2} = \tfrac12m\omega^{2}(A^{2}-x^{2}) = \tfrac12k(A^{2}-x^{2}) $$
The restoring force $F = -kx$ does work $-\int F\,dx$ in displacing the particle, stored as
$$ U = \tfrac12kx^{2} $$
$$ E = K+U = \tfrac12k(A^{2}-x^{2})+\tfrac12kx^{2} = \tfrac12kA^{2} $$
which does not depend on $x$ or $t$: the energy is constant.

(b) $U = \tfrac12kx^{2}$ is a parabola with its minimum ($U = 0$) at $x = 0$, rising to $\tfrac12kA^{2}$ at $x = \pm A$ (see the figure below).

(c) $T = 2\pi\sqrt{l/g}$ and $g_{Moon}\approx g/6$, so
$$ \frac{T_{Moon}}{T_{Earth}} = \sqrt{\frac{g}{g_{Moon}}} = \sqrt{6} = 2.45 $$
The pendulum swings $2.45$ times more slowly on the Moon.
:::

::: note Model answers — short (4–6)
**4.** (a) SHM is motion in which the acceleration is proportional to the displacement from the mean position and directed towards it.

(b) $\omega = \sqrt{k/m} = \sqrt{18/0.15} = \sqrt{120} = 10.95\ \text{rad s}^{-1}$, amplitude $A = 0.04\ \text{m}$.
$$ a_{max} = \omega^{2}A = 120\times0.04 = 4.8\ \text{m s}^{-2} $$
$$ T = \frac{2\pi}{\omega} = \frac{2\pi}{10.95} = 0.57\ \text{s} $$

(c) The total energy is
$$ E = \tfrac12kA^{2} = \tfrac12(18)(0.04)^{2} = 1.44\times10^{-2}\ \text{J} $$
The kinetic energy $\tfrac12k(A^{2}-x^{2})$ is an inverted parabola, maximum at $x = 0$; the potential energy $\tfrac12kx^{2}$ is an upright parabola. They add to a horizontal line at $E$ (the figure below).

**5.** (a) **Free oscillation:** the system oscillates at its natural frequency with constant amplitude, with no resistive force and no external driving (an ideal case). **Damped oscillation:** a resistive force (air drag, friction) removes energy each cycle, so the amplitude decays with time; the frequency is slightly lower than the natural value. **Forced oscillation:** a periodic external force of frequency $f_d$ drives the system; after a transient it oscillates at $f_d$, not at its natural frequency, with an amplitude that depends on how close $f_d$ is to the natural frequency.

(b) **Resonance** occurs when the frequency of the driving force equals the natural frequency of the system; the amplitude of the forced oscillation is then a maximum (limited only by damping). Examples: a child's swing pushed in time with its motion; the shattering of a glass by a singer of the right pitch; radio tuning; bridges swaying under marching soldiers.

**6.** (a) The bob of mass $m$ on a string of length $l$ is displaced by a small angle $\theta$. The component of weight along the arc is the restoring force $F = -mg\sin\theta\approx-mg\theta$ for small $\theta$ (in radians). The displacement along the arc is $x = l\theta$, so
$$ F = -\frac{mg}{l}\,x $$
This has the form $F = -kx$ with $k = mg/l$, so the motion is SHM and
$$ T = 2\pi\sqrt{\frac{m}{k}} = 2\pi\sqrt{\frac{l}{g}} $$

(b) Squaring, $T^{2} = \dfrac{4\pi^{2}}{g}\,l$. A graph of $T^{2}$ (vertical) against $l$ (horizontal) is a straight line through the origin of slope $4\pi^{2}/g$; hence $g = 4\pi^{2}/\text{slope}$. Using the whole line averages out reading errors.
:::

```figure caption="Energy in SHM. The potential energy ½kx² (blue) is a parabola, the kinetic energy ½k(A² − x²) (orange) is an inverted parabola, and their sum E = ½kA² (dashed) is constant."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.5,2.9))
A = 1.0
x = np.linspace(-A, A, 300)
U = 0.5*x**2
K = 0.5*(A**2 - x**2)
ax.plot(x, U, color=ACCENT, lw=1.8)
ax.plot(x, K, color=SERIES[1], lw=1.8)
ax.axhline(0.5, color=INK, lw=1.1, ls='--')
ax.text(-0.98, 0.535, '$E = \\frac{1}{2}kA^{2}$', fontsize=9, color=INK, va='bottom')
ax.text(0.55, 0.06, 'PE', color=ACCENT, fontsize=9)
ax.text(0.04, 0.42, 'KE', color=SERIES[1], fontsize=9, ha='left')
ax.set_xticks([-A, 0, A]); ax.set_xticklabels(['−A', '0', '+A'])
ax.set_yticks([0, 0.5]); ax.set_yticklabels(['0', '$E$'])
ax.set_xlabel('displacement  $x$', fontsize=9)
ax.set_ylabel('energy', fontsize=9)
ax.set_ylim(0, 0.65)
ax.spines[['top','right']].set_visible(False)
ax.grid(color=GRID, lw=0.5)
```

**Long answer / numerical questions [8 marks each]**

1. During an earthquake a building is displaced from equilibrium and feels a restoring force $F = -Ax$, where $A$ is a constant and $x$ the displacement. (a) Prove that the motion is simple harmonic. [2] (b) Show that the speed is $v = \pm\omega\sqrt{A_0^{2}-x^{2}}$, where $A_0$ is the amplitude. [2] (c) Find the maximum speed of a building shaken by $21\ \text{Hz}$ waves with amplitude $0.05\ \text{m}$. [2] (d) Why are tall buildings more susceptible to low-frequency waves? [2] <span class="marks">[8]</span> (NEB 2078)
2. (a) Derive the time period of a mass suspended from a vertical coiled spring. [3] (b) Show that the total energy of the oscillating mass is $\tfrac12kA^{2}$ and sketch the energy graphs. [3] (c) A $0.50\ \text{kg}$ mass on a spring oscillates with amplitude $0.10\ \text{m}$ and period $0.63\ \text{s}$. Find $k$, the total energy and the speed when $x = 0.06\ \text{m}$. [2] <span class="marks">[8]</span>
3. (a) Define angular SHM and derive the time period of a torsional pendulum. [3] (b) Derive the period of a simple pendulum from the torque on the bob. [3] (c) A second's pendulum has period $2.0\ \text{s}$. Find its length and its period on the Moon ($g_{Moon} = 1.63\ \text{m s}^{-2}$). [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) In SHM the acceleration is proportional to the displacement and opposite in direction. Here, with mass $m$,
$$ a = \frac{F}{m} = -\frac{A}{m}\,x = -\omega^{2}x,\qquad \omega^{2} = \frac{A}{m} $$
which is the defining equation of SHM, so the motion is SHM with $T = 2\pi\sqrt{m/A}$.

(b) Let the displacement be $x = A_0\sin\omega t$. Then $v = A_0\omega\cos\omega t$, and
$$ v^{2} = A_0^{2}\omega^{2}\cos^{2}\omega t = \omega^{2}A_0^{2}(1-\sin^{2}\omega t) = \omega^{2}(A_0^{2}-x^{2}) $$
$$ v = \pm\omega\sqrt{A_0^{2}-x^{2}} $$

(c) The maximum speed is at $x = 0$:
$$ v_{max} = \omega A_0 = 2\pi fA_0 = 2\pi\times21\times0.05 = 6.6\ \text{m s}^{-1} $$

(d) A building has its own **natural frequency**, and it is lower for a taller structure (a longer, more flexible "cantilever"). A low-frequency wave is therefore more likely to match the natural frequency of a tall building, producing **resonance**: the amplitude of the building's oscillation grows large and it may collapse. Short, stiff buildings have high natural frequencies and are driven far from resonance by such waves.

**2.** (a) See the derivation for the vertical spring in short answer 1(b): $F = -ky$, so
$$ T = 2\pi\sqrt{\frac{m}{k}} $$
The weight only changes the equilibrium position; the oscillation is about the new equilibrium and $T$ does not contain $g$.

(b) $K+U = \tfrac12kA^{2}$ as in short answer 3(a); the figure shows the energy graphs: $U$ and $K$ are parabolas that exchange energy twice per cycle, their sum constant.

(c) $\omega = 2\pi/T = 2\pi/0.63 = 9.97\ \text{rad s}^{-1}$.
$$ k = m\omega^{2} = 0.50\times(9.97)^{2} = 49.7\ \text{N m}^{-1} $$
$$ E = \tfrac12kA^{2} = \tfrac12(49.7)(0.10)^{2} = 0.25\ \text{J} $$
$$ v = \omega\sqrt{A^{2}-x^{2}} = 9.97\sqrt{0.10^{2}-0.06^{2}} = 9.97\times0.08 = 0.80\ \text{m s}^{-1} $$

**3.** (a) **Angular SHM** is oscillation in which the restoring torque is proportional to the angular displacement, $\tau = -C\theta$, where $C$ is the torsional constant. By $\tau = I\alpha$:
$$ I\alpha = -C\theta\ \Rightarrow\ \alpha = -\frac{C}{I}\,\theta = -\omega^{2}\theta,\qquad \omega^{2} = \frac{C}{I} $$
$$ T = 2\pi\sqrt{\frac{I}{C}} $$

(b) For a bob of mass $m$ on a light string of length $l$ displaced by a small angle $\theta$, the torque of the weight about the pivot is $\tau = -mgl\sin\theta\approx-mgl\theta$, and the moment of inertia is $I = ml^{2}$. Then
$$ ml^{2}\alpha = -mgl\,\theta\ \Rightarrow\ \alpha = -\frac{g}{l}\,\theta,\qquad T = 2\pi\sqrt{\frac{l}{g}} $$
This is the torsional result with $C = mgl$.

(c) $l = \dfrac{gT^{2}}{4\pi^{2}} = \dfrac{9.8\times4.0}{39.5} = 0.99\ \text{m}$. On the Moon,
$$ T_{M} = 2\pi\sqrt{\frac{0.993}{1.63}} = 4.9\ \text{s} $$
:::

::: tip Examiner's note — Periodic motion
The defining equation comes first: for any "prove it is SHM" question, reduce the force or torque to the form $a = -(\text{constant})\,x$ and *say* that this is SHM. In the vertical-spring derivation, state that $ke = mg$ at equilibrium and that the weight cancels; omitting it loses a mark. Note that $T$ for a spring–mass system does **not** depend on $g$ — the satellite and Moon questions test exactly this. In energy questions give $E = \tfrac12kA^{2}$ **and** label the graph axes; in numericals check that you used radians and $\omega$ in $\text{rad s}^{-1}$.
:::

## 3.3 Fluid statics

CDC allots **9 teaching hours** — one of the heaviest units, covering pressure and buoyancy, surface tension, capillarity, viscosity and the two principles of fluid flow. Every recent paper has one Group B item on each of surface tension, viscosity/Stokes' law and Bernoulli's equation.

**Short answer questions [5 marks each]**

1. (a) Define surface tension. [1] (b) Establish the relation between surface tension and surface energy. [2] (c) Two equal raindrops falling at terminal velocity $v_1$ coalesce into one. Find the new terminal velocity. [2] <span class="marks">[5]</span> (NEB 2078, 2081)
2. (a) State Stokes' law and define the coefficient of viscosity. [1+1] (b) Describe how $\eta$ of a liquid may be determined by Stokes' method. [1] (c) Water flows along a horizontal pipe of cross-section $25\ \text{cm}^{2}$ at $3\ \text{m s}^{-1}$ into a section of $15\ \text{cm}^{2}$. Find the change in pressure. [2] <span class="marks">[5]</span> (NEB 2080)
3. (a) Distinguish between laminar (streamline) and turbulent flow. [2] (b) Water at pressure $4\times10^{4}\ \text{N m}^{-2}$ flows at $2\ \text{m s}^{-1}$ through a pipe of area $200\ \text{cm}^{2}$, which narrows to $50\ \text{cm}^{2}$. Find the pressure in the narrow part. [3] <span class="marks">[5]</span> (NEB 2082)
4. (a) State Bernoulli's principle. [1] (b) A liquid of density $1200\ \text{kg m}^{-3}$ flows steadily through a tube of varying cross-section, $1.0\ \text{cm}^{2}$ at A and $20\ \text{mm}^{2}$ at B, at the same level. The speed at A is $10\ \text{cm s}^{-1}$. Find the speed at B [2] and the pressure difference between A and B. [2] <span class="marks">[5]</span> (NEB 2079 model)
5. (a) Derive Bernoulli's equation. [2] (b) Why does water squirt further when a thumb partly covers the end of a hose? [2] (c) State the equation of continuity. [1] <span class="marks">[5]</span> (NEB 2078)
6. (a) Define angle of contact and explain why mercury is depressed in a glass tube while water rises. [3] (b) Find the rise of water ($T = 0.072\ \text{N m}^{-1}$, angle of contact $0^{\circ}$) in a tube of radius $0.50\ \text{mm}$. [2] <span class="marks">[5]</span>
7. (a) State Poiseuille's formula and name each symbol. [2] (b) If the radius of a blood vessel is reduced by $10\%$ at constant pressure difference, by what fraction does the flow fall? [3] <span class="marks">[5]</span>
8. (a) Derive the expression for pressure at depth $h$ in a liquid. [2] (b) State Archimedes' principle and find the fraction of an iceberg ($917\ \text{kg m}^{-3}$) above sea water ($1025\ \text{kg m}^{-3}$). [3] <span class="marks">[5]</span>

::: note Model answers — short (1–4)
**1.** (a) **Surface tension** is the force acting per unit length on an imaginary line drawn in the surface of a liquid, perpendicular to the line and tangential to the surface: $T = F/l$, unit $\text{N m}^{-1}$.

(b) Let a wire frame with a sliding bar of length $l$ hold a soap film of *one* surface. The surface pulls the bar with force $F = Tl$. If the bar is moved a distance $dx$, the work done against surface tension is
$$ dW = F\,dx = T\,l\,dx = T\,\Delta A $$
where $\Delta A = l\,dx$ is the increase in surface area. This work is stored as surface energy, so the **surface energy per unit area equals the surface tension**: $E/A = T$, in $\text{J m}^{-2}$ which is identical to $\text{N m}^{-1}$.

(c) The terminal velocity is $v_t = \dfrac{2r^{2}(\rho-\sigma)g}{9\eta}\propto r^{2}$. Volume is conserved when two drops of radius $r$ coalesce: $\tfrac43\pi R^{3} = 2\times\tfrac43\pi r^{3}$, so $R = 2^{1/3}r$. Then
$$ v_2 = v_1\left(\frac{R}{r}\right)^{2} = 2^{2/3}v_1 = 1.59\,v_1 $$
For $N$ drops $v_2 = N^{2/3}v_1$; with $N = 2$ and $v_1 = 0.4\ \text{m s}^{-1}$ this gives $v_2 = 0.63\ \text{m s}^{-1}$.

**2.** (a) **Stokes' law:** the viscous drag on a small sphere of radius $r$ moving with speed $v$ through a fluid of viscosity $\eta$ is $F = 6\pi\eta rv$. The **coefficient of viscosity** is the tangential force per unit area needed to maintain unit velocity gradient between layers: $F = \eta A\,dv/dx$; unit $\text{Pa s}$.

(b) Drop a small steel ball of known radius and density into a tall jar of the liquid; time its fall between two marks once it reaches **terminal velocity**, where weight $=$ buoyancy $+$ drag. Then
$$ \eta = \frac{2r^{2}(\rho-\sigma)g}{9v_t} $$

(c) Continuity: $A_1v_1 = A_2v_2$, so $v_2 = 25\times3/15 = 5\ \text{m s}^{-1}$. For water, $\rho = 1000\ \text{kg m}^{-3}$ and Bernoulli's equation for a horizontal pipe gives
$$ P_1-P_2 = \tfrac12\rho(v_2^{2}-v_1^{2}) = \tfrac12(1000)(25-9) = 8.0\times10^{3}\ \text{Pa} $$
The pressure **falls** by $8.0\ \text{kPa}$ in the narrow section.

**3.** (a) In **laminar flow** every particle follows the same smooth path as the ones ahead of it, layers slide over each other without mixing, and the velocity at any point is constant; it occurs at low speeds (Reynolds number below about $2000$). In **turbulent flow** the motion is irregular, with eddies and mixing, and the velocity at a point changes randomly; it occurs at high speed or in narrow constrictions.

(b) $v_2 = 200\times2/50 = 8\ \text{m s}^{-1}$. With $\rho = 1000\ \text{kg m}^{-3}$:
$$ P_2 = P_1+\tfrac12\rho(v_1^{2}-v_2^{2}) = 4\times10^{4}+\tfrac12(1000)(4-64) $$
$$ P_2 = 4\times10^{4}-3\times10^{4} = 1.0\times10^{4}\ \text{N m}^{-2} $$

**4.** (a) **Bernoulli's principle:** for the steady, non-viscous, incompressible flow of a fluid, the sum of the pressure, the kinetic energy per unit volume and the potential energy per unit volume is constant along a streamline: where the speed is high, the pressure is low.

(b) $A_A = 1.0\ \text{cm}^{2} = 100\ \text{mm}^{2}$ and $A_B = 20\ \text{mm}^{2}$, so
$$ v_B = v_A\frac{A_A}{A_B} = 10\times\frac{100}{20} = 50\ \text{cm s}^{-1} = 0.50\ \text{m s}^{-1} $$
$$ P_A-P_B = \tfrac12\rho(v_B^{2}-v_A^{2}) = \tfrac12(1200)(0.50^{2}-0.10^{2}) = 600\times0.24 = 144\ \text{Pa} $$
:::

::: note Model answers — short (5–8)
**5.** (a) Consider a steady flow through a pipe: at the lower end (height $h_1$, area $A_1$, speed $v_1$, pressure $P_1$) and the upper end ($h_2, A_2, v_2, P_2$). In a short time $\Delta t$ a volume $\Delta V = A_1v_1\Delta t = A_2v_2\Delta t$ enters and leaves. Work done on the fluid by the pressures: $(P_1-P_2)\Delta V$. Change in energy: kinetic $\tfrac12\rho\Delta V(v_2^{2}-v_1^{2})$ plus potential $\rho\Delta V g(h_2-h_1)$. By the work–energy theorem,
$$ P_1-P_2 = \tfrac12\rho(v_2^{2}-v_1^{2})+\rho g(h_2-h_1) $$
$$ P+\tfrac12\rho v^{2}+\rho gh = \text{constant} $$

(b) The water leaves through a smaller area. By the equation of continuity its speed rises, and the range of a horizontal jet is proportional to its exit speed, so it goes further. (The flow rate hardly changes; the same volume per second is squeezed through a smaller opening.)

(c) For the steady flow of an incompressible fluid, the volume passing per second is the same at every cross-section: $A_1v_1 = A_2v_2$.

**6.** (a) The **angle of contact** is the angle between the tangent to the liquid surface at the point of contact and the solid surface, measured *inside the liquid*. For water on clean glass the adhesive force between water and glass exceeds the cohesive force between water molecules, the surface curves upward and $\theta<90^{\circ}$, so water is pulled up the tube. For mercury the cohesion is stronger, $\theta\approx140^{\circ}>90^{\circ}$, the meniscus is convex and the mercury is depressed.

(b)
$$ h = \frac{2T\cos\theta}{r\rho g} = \frac{2\times0.072\times1}{5.0\times10^{-4}\times1000\times9.8} = 2.9\times10^{-2}\ \text{m} $$
The water rises $2.9\ \text{cm}$.

**7.** (a) The volume of liquid flowing per second through a horizontal capillary tube is
$$ \frac{V}{t} = \frac{\pi Pr^{4}}{8\eta l} $$
where $P$ is the pressure difference across the ends, $r$ the radius, $l$ the length and $\eta$ the coefficient of viscosity.

(b) $V/t\propto r^{4}$. With the radius reduced by $10\%$, $r' = 0.9r$:
$$ \frac{V'}{V} = (0.9)^{4} = 0.656 $$
The flow falls by $34\%$ — which is why narrowed arteries force the heart to raise the pressure sharply.

**8.** (a) A liquid column of height $h$ and cross-section $A$ has weight $\rho Ahg$, and this is carried by the pressure difference acting on the area $A$:
$$ P = P_0+\frac{\rho Ahg}{A} = P_0+\rho gh $$
(b) **Archimedes' principle:** a body wholly or partly immersed in a fluid experiences an upthrust equal to the weight of the fluid displaced. A floating iceberg has weight $=$ upthrust, so the submerged fraction is $917/1025 = 0.895$; the fraction above the surface is $1-0.895 = 0.105$, about $10\%$.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) State Stokes' law. [1] (b) Derive the expression for the terminal velocity of a small sphere falling through a viscous fluid. [4] (c) A steel ball of radius $1.0\ \text{mm}$ and density $7800\ \text{kg m}^{-3}$ falls in glycerine ($\rho = 1260\ \text{kg m}^{-3}$, $\eta = 0.83\ \text{Pa s}$); find its terminal velocity. [2] (d) Why do raindrops not accelerate indefinitely? [1] <span class="marks">[8]</span>
2. (a) Derive Bernoulli's equation and state the assumptions made. [4] (b) Explain the working of a Venturi meter and derive the speed of flow from the two pressures. [3] (c) Why does an aeroplane wing experience lift? [1] <span class="marks">[8]</span>
3. (a) Derive the expression for the rise of a liquid in a capillary tube. [4] (b) Give two applications of capillarity. [2] (c) Eight drops of water, each of radius $1.0\ \text{mm}$, combine into a single drop. Find the change in surface energy ($T = 0.072\ \text{N m}^{-1}$). [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) The viscous drag on a small sphere of radius $r$ moving at speed $v$ in a fluid of viscosity $\eta$ is $F = 6\pi\eta rv$.

(b) A sphere of density $\rho$ falls in a fluid of density $\sigma$. Three forces act: the weight downward, $W = \tfrac43\pi r^{3}\rho g$; the upthrust upward, $U = \tfrac43\pi r^{3}\sigma g$; and the viscous drag upward, $F = 6\pi\eta rv$, which grows as $v$ grows. The sphere accelerates until the net force is zero; that speed is the **terminal velocity** $v_t$:
$$ \tfrac43\pi r^{3}\rho g = \tfrac43\pi r^{3}\sigma g+6\pi\eta rv_t $$
$$ 6\pi\eta rv_t = \tfrac43\pi r^{3}(\rho-\sigma)g $$
$$ v_t = \frac{2r^{2}(\rho-\sigma)g}{9\eta} $$
The speed is proportional to $r^{2}$ and inversely proportional to $\eta$.

(c)
$$ v_t = \frac{2(1.0\times10^{-3})^{2}(7800-1260)(9.8)}{9\times0.83} = \frac{0.1282}{7.47} = 1.7\times10^{-2}\ \text{m s}^{-1} $$

(d) As a drop speeds up the drag $6\pi\eta rv$ increases until it (plus upthrust) balances the weight; the net force then vanishes and the drop falls at constant terminal velocity. (For real raindrops, the drag law itself changes at larger speeds, but the conclusion is the same.)

**2.** (a) See short answer 5(a) for the derivation from the work–energy theorem,
$$ P+\tfrac12\rho v^{2}+\rho gh = \text{constant} $$
**Assumptions:** the fluid is incompressible (constant density), non-viscous (no internal friction), and its flow is steady and streamline (laminar), and the equation is applied along a single streamline.

(b) A **Venturi meter** is a horizontal tube with a narrow throat, with vertical manometer tubes at the wide part (area $A_1$, pressure $P_1$) and throat ($A_2$, $P_2$). By continuity $v_2 = v_1A_1/A_2$. By Bernoulli (same level),
$$ P_1-P_2 = \tfrac12\rho(v_2^{2}-v_1^{2}) = \tfrac12\rho v_1^{2}\left(\frac{A_1^{2}}{A_2^{2}}-1\right) $$
$$ v_1 = \sqrt{\frac{2(P_1-P_2)}{\rho\left(\dfrac{A_1^{2}}{A_2^{2}}-1\right)}} $$
The measured height difference $h$ in the manometers gives $P_1-P_2 = \rho_{l}gh$.

(c) The wing's shape and tilt make air travel faster over the top than below. By Bernoulli's principle the pressure above is lower, so the net upward pressure force on the wing is the lift.

**3.** (a) Water of surface tension $T$ rises in a tube of radius $r$ with contact angle $\theta$. The surface tension acts along the line of contact of length $2\pi r$, at angle $\theta$ to the wall; the vertical component of the pull is
$$ F = T\cos\theta\times2\pi r $$
This lifts a column of height $h$, whose weight is $\pi r^{2}h\rho g$. At equilibrium,
$$ 2\pi rT\cos\theta = \pi r^{2}h\rho g $$
$$ h = \frac{2T\cos\theta}{r\rho g} $$
$h\propto1/r$: narrower tubes give higher rises. For $\theta>90^{\circ}$ (mercury) $h$ is negative — a depression.

(b) **Applications:** (i) the rise of oil in the wick of a lamp, or of water in a blotting paper or a towel; (ii) the rise of sap and water from roots in fine vessels of plants; (iii) the supply of water to soil by fine pores.

(c) Volume is conserved: $8\times\tfrac43\pi r^{3} = \tfrac43\pi R^{3}$, so $R = 2r = 2.0\ \text{mm}$.
$$ A_{initial} = 8\times4\pi r^{2} = 32\pi r^{2},\qquad A_{final} = 4\pi(2r)^{2} = 16\pi r^{2} $$
$$ \Delta E = T(A_{final}-A_{initial}) = -T\times16\pi r^{2} = -0.072\times16\pi\times(1.0\times10^{-3})^{2} $$
$$ \Delta E = -3.6\times10^{-6}\ \text{J} $$
The surface energy **decreases** by $3.6\ \mu\text{J}$; the released energy appears as a small rise in temperature.
:::

::: tip Examiner's note — Fluid statics
State **which law** is used at each step: continuity first, then Bernoulli. In the coalescing-drop question the marks are for "volume is conserved, so $R = 2^{1/3}r$" and "$v\propto r^{2}$" — not for the final number alone. For Bernoulli numericals assume the fluid is water unless told otherwise, and convert areas to $\text{m}^{2}$ only when they are not cancelled in a ratio. Do not write that surface tension is "energy": it is force per unit length, *numerically equal* to the surface energy per unit area.
:::

## 3.4 First Law of Thermodynamics

CDC allots **6 teaching hours**. The first law, $C_P-C_V = R$ and the isothermal and adiabatic processes are all standard Group B items; the $p$–$V$ diagram is also used for graph-reading questions in Group A.

**Short answer questions [5 marks each]**

1. (a) State the first law of thermodynamics. [1] (b) Derive $C_P-C_V = R$ for an ideal gas. [2] (c) Define the efficiency of a heat engine. [2] <span class="marks">[5]</span> (NEB 2080)
2. (a) What is an indicator diagram? [1] (b) Show that the work done by a gas in a volume change is the area under its $p$–$V$ curve. [2] (c) A gas expands at a constant pressure of $2.0\times10^{5}\ \text{Pa}$ from $1.0\ \text{L}$ to $4.0\ \text{L}$ and absorbs $900\ \text{J}$. Find the work done and the change in internal energy. [2] <span class="marks">[5]</span> (NEB 2081)
3. (a) Explain how the first law expresses the conservation of energy. [2] (b) Write what the law reduces to in (i) an isothermal, (ii) an adiabatic, (iii) an isochoric and (iv) an isobaric process. [3] <span class="marks">[5]</span> (NEB 2082)
4. (a) Derive the work done by an ideal gas in an isothermal expansion. [3] (b) Find the heat absorbed when $2.0\ \text{mol}$ of gas expand isothermally at $300\ \text{K}$ to three times the volume. [2] <span class="marks">[5]</span>
5. (a) Show that $PV^{\gamma}$ is constant in an adiabatic process. [3] (b) One mole of a monatomic gas at $300\ \text{K}$ expands adiabatically to twice its volume. Find the final temperature. [2] <span class="marks">[5]</span>
6. $2.0\ \text{mol}$ of a monatomic ideal gas are heated at constant pressure from $300\ \text{K}$ to $400\ \text{K}$. Find $Q$, $\Delta U$ and $W$ ($R = 8.314\ \text{J mol}^{-1}\text{K}^{-1}$). [5]
7. (a) What is meant by a thermodynamic system, and how are open, closed and isolated systems different? [3] (b) Why is internal energy called a state function while heat and work are not? [2] <span class="marks">[5]</span>

::: note Model answers — short (1–4)
**1.** (a) The **first law:** the heat supplied to a system equals the increase in its internal energy plus the work done by the system: $Q = \Delta U + W$.

(b) At constant volume, $W = 0$ so all heat raises the internal energy: $Q_V = nC_V\Delta T = \Delta U$. Since $U$ of an ideal gas depends on $T$ alone, $\Delta U = nC_V\Delta T$ in *every* process. At constant pressure,
$$ Q_P = \Delta U+P\Delta V = nC_V\Delta T+P\Delta V $$
From $PV = nRT$ at constant $P$, $P\Delta V = nR\Delta T$. Therefore
$$ nC_P\Delta T = nC_V\Delta T+nR\Delta T $$
$$ C_P-C_V = R $$
(Mayer's relation). The extra heat at constant pressure pays for the expansion work.

(c) The **efficiency** of a heat engine is the fraction of the heat absorbed from the source that is converted to useful work:
$$ \eta = \frac{W}{Q_1} = \frac{Q_1-Q_2}{Q_1} = 1-\frac{Q_2}{Q_1} $$

**2.** (a) An **indicator diagram** is a graph of pressure against volume ($p$–$V$ diagram) for a system or an engine cycle.

(b) For a small expansion $dV$ at pressure $P$ against a piston of area $A$, $dW = F\,dx = PA\,dx = P\,dV$. Between $V_1$ and $V_2$,
$$ W = \int_{V_1}^{V_2}P\,dV $$
which is the area under the curve. For a closed cycle the net work is the area enclosed.

(c) 
$$ W = P\Delta V = 2.0\times10^{5}\times(4.0-1.0)\times10^{-3} = 600\ \text{J} $$
$$ \Delta U = Q-W = 900-600 = 300\ \text{J} $$

**3.** (a) Energy can be neither created nor destroyed. Heat $Q$ is energy supplied to the system; it either raises the internal (molecular) energy, $\Delta U$, or leaves the system as work, $W$ done on the surroundings. Nothing is lost, so the accounts balance: $Q = \Delta U+W$.

(b) 

| Process | Condition | First law becomes |
|---|---|---|
| Isothermal | $\Delta T = 0$, so $\Delta U = 0$ | $Q = W$ |
| Adiabatic | $Q = 0$ | $W = -\Delta U$ (gas cools when it expands) |
| Isochoric | $\Delta V = 0$, so $W = 0$ | $Q = \Delta U$ |
| Isobaric | $P$ constant | $Q = \Delta U+P\Delta V$ |

**4.** (a) For $n$ moles at constant temperature $T$, $P = nRT/V$:
$$ W = \int_{V_1}^{V_2}\frac{nRT}{V}\,dV = nRT\ln\frac{V_2}{V_1} $$
Since $\Delta U = 0$, this equals the heat absorbed.

(b) 
$$ Q = W = 2.0\times8.314\times300\times\ln3 = 4988\times1.0986 = 5.5\times10^{3}\ \text{J} $$
:::

::: note Model answers — short (5–7)
**5.** (a) In an adiabatic change $dQ = 0$, so $dU+P\,dV = 0$, i.e. $nC_V\,dT = -P\,dV$. Differentiating $PV = nRT$: $P\,dV+V\,dP = nR\,dT$. Eliminate $dT$:
$$ C_V(P\,dV+V\,dP) = -R\,P\,dV = -(C_P-C_V)P\,dV $$
$$ C_V V\,dP+C_PP\,dV = 0\ \Rightarrow\ \frac{dP}{P}+\gamma\frac{dV}{V} = 0 $$
Integrating, $\ln P+\gamma\ln V = \text{constant}$, so
$$ PV^{\gamma} = \text{constant} $$

(b) Using $TV^{\gamma-1}$ constant with $\gamma = \tfrac53$:
$$ T_2 = T_1\left(\frac{V_1}{V_2}\right)^{\gamma-1} = 300\times\left(\tfrac12\right)^{2/3} = 300\times0.630 = 189\ \text{K} $$

**6.** For a monatomic gas $C_V = \tfrac32R$ and $C_P = \tfrac52R$.
$$ Q = nC_P\Delta T = 2.0\times\tfrac52(8.314)\times100 = 4157\ \text{J} $$
$$ \Delta U = nC_V\Delta T = 2.0\times\tfrac32(8.314)\times100 = 2494\ \text{J} $$
$$ W = Q-\Delta U = 1663\ \text{J}\quad(= nR\Delta T = 2.0\times8.314\times100\ \checkmark) $$

**7.** (a) A **thermodynamic system** is the part of the universe (a quantity of gas in a cylinder, say) chosen for study; everything else is the **surroundings**. An **open** system exchanges both matter and energy with its surroundings (a boiling kettle); a **closed** system exchanges energy only (gas in a sealed cylinder with a piston); an **isolated** system exchanges neither (an ideal thermos).

(b) The internal energy depends only on the present state ($P$, $V$, $T$) of the system, not on how it arrived there, so $\Delta U$ between two states is fixed. Heat and work depend on the **path** taken between the states (for example, the area under different $p$–$V$ curves joining the same two points differs), so they are not properties of a state.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Define the two principal heat capacities of an ideal gas. [2] (b) Derive the relation between them. [3] (c) Show that $\gamma = 1+R/C_V$ and find $C_V$ and $C_P$ for a diatomic gas. [3] <span class="marks">[8]</span>
2. (a) Describe the isothermal and adiabatic processes of an ideal gas and sketch both on one $p$–$V$ diagram. [3] (b) Derive the work done in an adiabatic expansion from $(P_1, V_1)$ to $(P_2, V_2)$. [3] (c) One mole of monatomic gas at $300\ \text{K}$ expands adiabatically to twice its volume; find the work done. [2] <span class="marks">[8]</span>
3. (a) Apply the first law to the four thermodynamic processes, giving $Q$, $\Delta U$, $W$ for each. [4] (b) A gas is taken from $A$ to $B$ by an isobaric expansion at $1.0\times10^{5}\ \text{Pa}$ from $2\ \text{L}$ to $6\ \text{L}$, then from $B$ to $C$ at constant volume until it reaches the isotherm through $A$. Find the pressure at $C$, the work done by the gas in $A\to B\to C$ and the heat absorbed. [4] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) The **molar heat capacity at constant volume**, $C_V$, is the heat needed to raise the temperature of one mole by one kelvin with the volume held fixed; $C_P$ is the corresponding heat at constant pressure. Units: $\text{J mol}^{-1}\text{K}^{-1}$.

(b) See short answer 1(b): $C_P-C_V = R$. The extra heat at constant pressure does the expansion work $P\Delta V = R\Delta T$ per mole.

(c) Dividing by $C_V$: $\gamma = C_P/C_V = 1+R/C_V$. For a diatomic gas with five degrees of freedom (translation and rotation), $C_V = \tfrac52R = 20.8\ \text{J mol}^{-1}\text{K}^{-1}$, $C_P = \tfrac72R = 29.1\ \text{J mol}^{-1}\text{K}^{-1}$ and $\gamma = 7/5 = 1.4$.

**2.** (a) **Isothermal:** the temperature is fixed (slow change, good thermal contact with a reservoir); $PV = \text{constant}$ and $\Delta U = 0$. **Adiabatic:** no heat flows (rapid change or perfect insulation); $PV^{\gamma} = \text{constant}$ with $\gamma>1$, so the adiabatic curve is **steeper** than the isotherm through the same point (see the figure below).

(b) $W = \int_{V_1}^{V_2}P\,dV$ with $P = KV^{-\gamma}$, where $K = P_1V_1^{\gamma} = P_2V_2^{\gamma}$:
$$ W = K\int_{V_1}^{V_2}V^{-\gamma}\,dV = \frac{K}{1-\gamma}\left(V_2^{1-\gamma}-V_1^{1-\gamma}\right) $$
$$ W = \frac{P_2V_2-P_1V_1}{1-\gamma} = \frac{P_1V_1-P_2V_2}{\gamma-1} = \frac{nR(T_1-T_2)}{\gamma-1} $$

(c) $T_2 = 189\ \text{K}$ (short answer 5(b)), $\gamma-1 = \tfrac23$:
$$ W = \frac{1\times8.314\times(300-189)}{2/3} = 1.38\times10^{3}\ \text{J} $$
Check: $W = nC_V(T_1-T_2) = 12.47\times111 = 1.38\times10^{3}\ \text{J}$.

**3.** (a)

| Process | $Q$ | $\Delta U$ | $W$ |
|---|---|---|---|
| Isothermal | $nRT\ln(V_2/V_1)$ | $0$ | $nRT\ln(V_2/V_1)$ |
| Adiabatic | $0$ | $nC_V\Delta T$ | $-nC_V\Delta T$ |
| Isochoric | $nC_V\Delta T$ | $nC_V\Delta T$ | $0$ |
| Isobaric | $nC_P\Delta T$ | $nC_V\Delta T$ | $P\Delta V = nR\Delta T$ |

(b) $C$ lies on the isotherm through $A$, so $P_CV_C = P_AV_A$ with $V_C = V_B = 6\ \text{L}$:
$$ P_C = \frac{P_AV_A}{V_C} = \frac{1.0\times10^{5}\times2}{6} = 3.3\times10^{4}\ \text{Pa} $$
In $A\to B$, $W_{AB} = P\Delta V = 1.0\times10^{5}\times(6-2)\times10^{-3} = 400\ \text{J}$. In $B\to C$ the volume is constant, so $W_{BC} = 0$. Total $W = 400\ \text{J}$. Because $A$ and $C$ are at the same temperature, $\Delta U = 0$ over the whole path, so
$$ Q = \Delta U+W = 0+400 = 400\ \text{J} $$
absorbed. (If the gas is monatomic, $A\to B$ absorbs $Q_{AB} = \tfrac52P\Delta V = 1000\ \text{J}$ and $B\to C$ rejects $Q_{BC} = \Delta U_{BC} = -600\ \text{J}$; the net heat absorbed is $1000-600 = 400\ \text{J}$, as found.)
:::

```figure caption="Isothermal (blue) and adiabatic (orange) expansions of an ideal gas from the same state A. The adiabat falls more steeply because the gas also cools as it does work; the area under each curve is the work done."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.0))
V = np.linspace(1.0, 2.6, 200)
P0 = 1.0
ax.plot(V, P0/V, color=ACCENT, lw=1.9)
ax.plot(V, P0/V**(5/3), color=SERIES[1], lw=1.9)
ax.plot([1.0],[1.0],'o',color=INK,ms=4)
ax.annotate('A', (1.0, 1.0), xytext=(1.04, 1.05), fontsize=9, color=INK)
ax.annotate('isotherm  $PV$ = constant', (2.6, 1/2.6), xytext=(1.75, 0.66), fontsize=8.5, color=ACCENT)
ax.annotate('adiabat  $PV^{\\gamma}$ = constant', (2.6, 2.6**(-5/3)), xytext=(1.55, 0.12), fontsize=8.5, color=SERIES[1])
ax.set_xlabel('volume  $V$', fontsize=9); ax.set_ylabel('pressure  $P$', fontsize=9)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(0.9, 2.75); ax.set_ylim(0, 1.25)
ax.spines[['top','right']].set_visible(False)
```

::: tip Examiner's note — First Law of Thermodynamics
Write the sign convention once, at the top: $Q$ positive when heat enters, $W$ positive when the gas does work. The derivation of $C_P-C_V = R$ earns its marks for "$\Delta U = nC_V\Delta T$ in every process" and "$P\Delta V = nR\Delta T$"; both must appear. In a numerical, use kelvin for $T$ and $\text{m}^{3}$ for $V$ (litres $\times10^{-3}$). For the adiabatic questions quote $\gamma$ for the gas (monatomic $\tfrac53$, diatomic $\tfrac75$) and check that the adiabat is steeper than the isotherm.
:::

## 3.5 Second Law of Thermodynamics

CDC allots **6 teaching hours**. Expect the statement of the second law, a heat-engine or refrigerator item (often with the efficiency expression), the petrol-engine cycle against the diesel cycle, and a Carnot numerical.

**Short answer questions [5 marks each]**

1. (a) State the second law of thermodynamics. [1] (b) Does a refrigerator violate it? Explain. [2] (c) A heat engine takes $Q_1$ from a source at $T_1$ and rejects $Q_2$ to a sink at $T_2$. Write its efficiency [1] and say when the efficiency would be zero. [1] <span class="marks">[5]</span> (NEB 2078)
2. (a) A Carnot engine has an efficiency of $25\%$ with its sink at $9\ ^{\circ}\text{C}$. By how much must the source temperature rise to make the efficiency $50\%$? [3] (b) How does the first law express conservation of energy? [2] <span class="marks">[5]</span> (NEB 2082)
3. (a) Draw the $p$–$V$ diagram of a petrol engine and explain its working. [3] (b) Compare the efficiency of a petrol engine with that of a diesel engine in terms of compression ratio. [2] <span class="marks">[5]</span> (NEB 2079 model)
4. (a) Describe the four steps of the Carnot cycle. [3] (b) Write the efficiency and state why no engine can exceed it. [2] <span class="marks">[5]</span>
5. (a) Define the coefficient of performance of a refrigerator and derive it in terms of $T_1$ and $T_2$ for an ideal one. [3] (b) An ideal refrigerator works between $273\ \text{K}$ and $300\ \text{K}$; find its coefficient of performance and the work needed to remove $1000\ \text{J}$. [2] <span class="marks">[5]</span>
6. (a) Give the Kelvin–Planck and Clausius statements and show they express the same law. [3] (b) What is entropy, and what does it tell about the direction of natural processes? [2] <span class="marks">[5]</span>
7. A Carnot engine works between $500\ \text{K}$ and $300\ \text{K}$ and takes $2000\ \text{J}$ from the source per cycle. Find its efficiency, the work done and the heat rejected. [5]

::: note Model answers — short (1–4)
**1.** (a) **Kelvin–Planck statement:** it is impossible to construct an engine, working in a cycle, whose sole effect is to take heat from a single reservoir and convert it completely into work. **Clausius statement:** heat cannot flow from a colder body to a hotter body by itself, with no other change.

(b) No. A refrigerator does take heat from a cold body and give more heat to a hot one, but only because **work is done on it** by an external agent (the compressor motor). The Clausius statement forbids transfer *by itself*; here the transfer is not the sole effect, since electrical work is consumed and also appears as heat in the room.

(c)
$$ \eta = \frac{Q_1-Q_2}{Q_1} = 1-\frac{Q_2}{Q_1} = 1-\frac{T_2}{T_1} $$
(the last form only for a reversible engine, since $Q_2/Q_1 = T_2/T_1$). The efficiency is **zero when $T_2 = T_1$** (equivalently $Q_2 = Q_1$): with no temperature difference no work can be extracted.

**2.** (a) $T_2 = 9+273 = 282\ \text{K}$.
$$ \eta = 1-\frac{T_2}{T_1}\ \Rightarrow\ 0.25 = 1-\frac{282}{T_1}\ \Rightarrow\ T_1 = \frac{282}{0.75} = 376\ \text{K} $$
For $\eta = 0.50$:
$$ T_1' = \frac{282}{0.50} = 564\ \text{K} $$
$$ \Delta T_1 = 564-376 = 188\ \text{K} $$

(b) The first law, $Q = \Delta U+W$, says that the heat supplied to a system is exactly accounted for by the gain in its internal energy and the work it does: energy changes form but the total is conserved. In an engine cycle $\Delta U = 0$, so $W = Q_1-Q_2$: the work output is the net heat input.

**3.** (a) The **Otto cycle** (figure below) models a petrol engine: $1\to2$ adiabatic compression of the fuel–air mixture from $V_1$ to $V_2$; $2\to3$ heating at constant volume when the spark ignites the mixture (heat $Q_1$ absorbed); $3\to4$ adiabatic expansion (the power stroke, which delivers the work); $4\to1$ cooling at constant volume when the exhaust valve opens (heat $Q_2$ rejected). The net work is the enclosed area.

(b) For the Otto cycle, with compression ratio $r = V_1/V_2$,
$$ \eta_{petrol} = 1-\frac{1}{r^{\gamma-1}} $$
For the diesel cycle the compression ratio is much higher ($15$ to $22$, against $6$ to $10$ for petrol) because only air is compressed, so there is no pre-ignition. A higher $r$ gives a larger $\eta$: with $\gamma = 1.4$, $r = 8$ gives $56\%$ while $r = 16$ gives $67\%$ for the ideal Otto formula. The diesel cycle's efficiency also depends on the cut-off ratio $\rho$ at which fuel injection stops: $\eta_{diesel} = 1-\dfrac{1}{r^{\gamma-1}}\,\dfrac{\rho^{\gamma}-1}{\gamma(\rho-1)}$. At the same compression ratio the Otto cycle is the more efficient; but a real diesel engine runs at a far higher $r$, so it is more efficient in practice.

**4.** (a) Working substance: an ideal gas in a cylinder, between a source at $T_1$ and a sink at $T_2$.
(i) **Isothermal expansion** at $T_1$: heat $Q_1$ absorbed from the source, work done by the gas. (ii) **Adiabatic expansion:** the gas cools from $T_1$ to $T_2$ with no heat exchange. (iii) **Isothermal compression** at $T_2$: heat $Q_2$ rejected to the sink. (iv) **Adiabatic compression:** the gas warms from $T_2$ back to $T_1$, completing the cycle.

(b) $\eta = 1-T_2/T_1$, with temperatures in kelvin. **Carnot's theorem:** no engine working between two given temperatures can be more efficient than a reversible engine between the same temperatures — otherwise it could be coupled with a reversed Carnot engine to transfer heat from cold to hot with no net work, violating the Clausius statement. $\eta = 1$ would need $T_2 = 0\ \text{K}$, which cannot be reached.
:::

::: note Model answers — short (5–7)
**5.** (a) The **coefficient of performance** of a refrigerator is the ratio of the heat removed from the cold space to the work supplied:
$$ \text{COP} = \frac{Q_2}{W} = \frac{Q_2}{Q_1-Q_2} $$
For a reversible refrigerator $Q_1/Q_2 = T_1/T_2$, so
$$ \text{COP} = \frac{T_2}{T_1-T_2} $$

(b) $T_2 = 273\ \text{K}$, $T_1 = 300\ \text{K}$:
$$ \text{COP} = \frac{273}{300-273} = 10.1 $$
$$ W = \frac{Q_2}{\text{COP}} = \frac{1000}{10.1} = 99\ \text{J} $$

**6.** (a) Kelvin–Planck and Clausius statements are given in short answer 1(a). Suppose the Kelvin–Planck statement were false, so that an engine $X$ converts heat $Q$ from a cold reservoir entirely into work. Use that work to drive a refrigerator that takes $Q_c$ from the same cold reservoir and gives $Q_c+Q$ to a hot one: the combined result is a transfer of heat from cold to hot with no outside work, violating Clausius. So a violation of one is a violation of the other: they are two forms of the same law.

(b) **Entropy** $S$ is a state function that measures the disorder of a system; for heat $\Delta Q$ absorbed reversibly at temperature $T$, $\Delta S = \Delta Q/T$. The second law in terms of entropy: in any spontaneous (irreversible) process in an isolated system the entropy increases; it stays constant only in a reversible one. This gives time a direction — a hot cup cools, a gas expands into a vacuum, and neither reverses by itself.

**7.** $T_1 = 500\ \text{K}$, $T_2 = 300\ \text{K}$, $Q_1 = 2000\ \text{J}$.
$$ \eta = 1-\frac{300}{500} = 0.40 $$
$$ W = \eta Q_1 = 0.40\times2000 = 800\ \text{J} $$
$$ Q_2 = Q_1-W = 1200\ \text{J} $$
Check: $Q_2/Q_1 = 1200/2000 = 0.6 = T_2/T_1$.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Describe the Carnot cycle with a labelled $p$–$V$ diagram. [3] (b) Derive the efficiency $\eta = 1-T_2/T_1$. [4] (c) What is the efficiency between the steam point and the ice point? [1] <span class="marks">[8]</span>
2. (a) Draw and explain the Otto and the Diesel cycles. [4] (b) Derive the efficiency of the Otto cycle. [3] (c) Calculate it for $r = 8$, $\gamma = 1.4$. [1] <span class="marks">[8]</span>
3. (a) Explain how a refrigerator works, with a block diagram. [2] (b) A refrigerator removes $500\ \text{J}$ per cycle from the food compartment at $-3\ ^{\circ}\text{C}$ and rejects heat to a room at $27\ ^{\circ}\text{C}$. Find the minimum work per cycle and the heat rejected. [3] (c) A real engine works between $600\ \text{K}$ and $300\ \text{K}$ with $90\%$ of the Carnot efficiency and delivers $8\ \text{kW}$. Find the rate at which it absorbs heat and the rate at which it rejects heat. [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) The cycle (figure below) consists of four reversible steps on an ideal gas: $A\to B$ isothermal expansion at $T_1$; $B\to C$ adiabatic expansion to $T_2$; $C\to D$ isothermal compression at $T_2$; $D\to A$ adiabatic compression to $T_1$.

(b) For the isothermal expansion $A\to B$ (volumes $V_A\to V_B$): heat absorbed
$$ Q_1 = nRT_1\ln\frac{V_B}{V_A} $$
For the isothermal compression $C\to D$: heat rejected
$$ Q_2 = nRT_2\ln\frac{V_C}{V_D} $$
For the adiabats $B\to C$ and $D\to A$, using $TV^{\gamma-1}$ constant:
$$ T_1V_B^{\gamma-1} = T_2V_C^{\gamma-1},\qquad T_1V_A^{\gamma-1} = T_2V_D^{\gamma-1} $$
Dividing these gives $V_B/V_A = V_C/V_D$, so the logarithms are equal and
$$ \frac{Q_2}{Q_1} = \frac{T_2}{T_1} $$
$$ \eta = 1-\frac{Q_2}{Q_1} = 1-\frac{T_2}{T_1} $$

(c) $T_1 = 373\ \text{K}$, $T_2 = 273\ \text{K}$: $\eta = 1-273/373 = 0.268$, about $27\%$.

**2.** (a) **Otto cycle** (petrol): two adiabats and two isochores, as explained in section 3.5 short answer 3(a). **Diesel cycle:** $1\to2$ adiabatic compression of air alone to a high ratio; $2\to3$ fuel injected and burns at **constant pressure** (heat $Q_1$ in, gas expands to $V_3$); $3\to4$ adiabatic expansion; $4\to1$ cooling at constant volume ($Q_2$ out). The diesel engine ignites the fuel by the heat of compression, so there is no spark plug.

(b) In the Otto cycle, heat is absorbed at constant volume $2\to3$ and rejected at constant volume $4\to1$:
$$ Q_1 = nC_V(T_3-T_2),\qquad Q_2 = nC_V(T_4-T_1) $$
$$ \eta = 1-\frac{T_4-T_1}{T_3-T_2} $$
For the adiabats, $T_1V_1^{\gamma-1} = T_2V_2^{\gamma-1}$ and $T_4V_1^{\gamma-1} = T_3V_2^{\gamma-1}$, so $T_2 = T_1r^{\gamma-1}$ and $T_3 = T_4r^{\gamma-1}$ with $r = V_1/V_2$. Then $T_3-T_2 = r^{\gamma-1}(T_4-T_1)$ and
$$ \eta = 1-\frac{1}{r^{\gamma-1}} $$

(c) $\eta = 1-8^{-0.4} = 1-0.435 = 0.565$: $56\%$ (an ideal upper limit; real engines reach about $25$–$30\%$).

**3.** (a) A refrigerator is a heat engine run backwards. A compressor (driven by a motor, work $W$) compresses a refrigerant vapour, which gives up heat $Q_1$ in the condenser outside; the refrigerant then expands through a valve, cools and absorbs heat $Q_2$ in the evaporator inside the compartment; the cycle repeats. By energy conservation $Q_1 = Q_2+W$.

(b) $T_2 = 270\ \text{K}$, $T_1 = 300\ \text{K}$:
$$ \text{COP} = \frac{T_2}{T_1-T_2} = \frac{270}{30} = 9 $$
$$ W = \frac{Q_2}{\text{COP}} = \frac{500}{9} = 56\ \text{J} $$
$$ Q_1 = Q_2+W = 500+56 = 556\ \text{J} $$

(c) The Carnot (ideal) efficiency is $1-300/600 = 0.50$, so the engine's efficiency is $\eta = 0.90\times0.50 = 0.45$.
$$ \text{rate of absorption} = \frac{P_{out}}{\eta} = \frac{8.0}{0.45} = 17.8\ \text{kW} $$
$$ \text{rate of rejection} = 17.8-8.0 = 9.8\ \text{kW} $$
:::

```figure caption="Left: the Otto cycle of a petrol engine (1→2 adiabatic compression, 2→3 heating at constant volume, 3→4 adiabatic expansion, 4→1 cooling at constant volume). Right: the Carnot cycle (A→B and C→D isothermal, B→C and D→A adiabatic)."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
g = 1.4
V1, V2 = 5.0, 1.0
P1 = 1.0
Va = np.linspace(V2, V1, 80)
P12 = P1*(V1/Va)**g
P2 = P1*(V1/V2)**g
P3 = 2.4*P2
Vb = np.linspace(V2, V1, 80)
P34 = P3*(V2/Vb)**g
P4 = P3*(V2/V1)**g
a1.plot(Va, P12, color=ACCENT, lw=1.7)
a1.plot([V2, V2], [P2, P3], color=SERIES[1], lw=1.7)
a1.plot(Vb, P34, color=ACCENT, lw=1.7)
a1.plot([V1, V1], [P4, P1], color=SERIES[1], lw=1.7)
for lab, (x, y), off in [('1', (V1, P1), (0.15, -0.6)), ('2', (V2, P2), (-0.65, 0.0)), ('3', (V2, P3), (-0.65, 0.0)), ('4', (V1, P4), (0.15, 0.1))]:
    a1.plot([x], [y], 'o', color=INK, ms=3)
    a1.text(x+off[0], y+off[1], lab, fontsize=8.5, color=INK)
a1.set_xlabel('V', fontsize=8.5); a1.set_ylabel('P', fontsize=8.5)
a1.set_xticks([]); a1.set_yticks([])
a1.set_xlim(0, 6); a1.set_ylim(0, P3*1.1)
a1.set_title('Otto cycle', fontsize=9, color=INK)
T1, T2 = 2.0, 1.0
VA, VB = 1.0, 2.0
VC = VB*(T1/T2)**(1/(g-1)); VD = VA*(T1/T2)**(1/(g-1))
VAB = np.linspace(VA, VB, 60); VBC = np.linspace(VB, VC, 60)
VCD = np.linspace(VC, VD, 60); VDA = np.linspace(VD, VA, 60)
a2.plot(VAB, T1/VAB, color=SERIES[1], lw=1.7)
pB = T1/VB
a2.plot(VBC, pB*(VB/VBC)**g, color=ACCENT, lw=1.7)
a2.plot(VCD, T2/VCD, color=SERIES[1], lw=1.7)
pA = T1/VA
a2.plot(VDA, pA*(VA/VDA)**g, color=ACCENT, lw=1.7)
for lab, (x, y), off in [('A', (VA, pA), (-0.35, 0.0)), ('B', (VB, pB), (0.1, 0.1)), ('C', (VC, pB*(VB/VC)**g), (0.1, 0.05)), ('D', (VD, T2/VD), (-0.35, -0.12))]:
    a2.plot([x], [y], 'o', color=INK, ms=3)
    a2.text(x+off[0], y+off[1], lab, fontsize=8.5, color=INK)
a2.text(1.35, 1.72, '$T_1$', fontsize=8.5, color=SERIES[1])
a2.text(3.2, 0.42, '$T_2$', fontsize=8.5, color=SERIES[1])
a2.set_xlabel('V', fontsize=8.5)
a2.set_xticks([]); a2.set_yticks([])
a2.set_xlim(0.4, VC+1.0); a2.set_ylim(0, pA*1.12)
a2.set_title('Carnot cycle', fontsize=9, color=INK)
for a in (a1, a2):
    a.spines[['top','right']].set_visible(False)
fig.tight_layout()
```

::: tip Examiner's note — Second Law of Thermodynamics
Always convert to **kelvin** before using $1-T_2/T_1$. In the Carnot derivation, the marks are for the two isothermal heat expressions, the two adiabatic relations and the step "$V_B/V_A = V_C/V_D$"; skipping that step is the usual reason for losing a mark. Distinguish *efficiency* (engine, $W/Q_1$, always below $1$) from *coefficient of performance* (refrigerator, $Q_2/W$, often above $1$). When comparing petrol and diesel engines, say clearly that it is the **compression ratio** that differs and that the diesel compresses air only.
:::

## 3.6 Wave motion

CDC allots only **2 teaching hours**, but progressive and stationary waves underpin units 7 to 9, and the node-spacing proof appeared in a Group C question in 2082.

**Short answer questions [5 marks each]**

1. (a) Define a progressive wave and a stationary wave. [2] (b) Write the equation of a plane progressive wave and explain every symbol. [3] <span class="marks">[5]</span>
2. (a) Explain how a stationary wave is formed. [2] (b) Prove that the distance between two consecutive nodes is $\lambda/2$. [3] <span class="marks">[5]</span> (NEB 2082)
3. A wave is described by $y = 0.05\sin(40t-2x)$ in SI units. Find the amplitude, frequency, wavelength and speed, and the phase difference between two points $0.50\ \text{m}$ apart. [5]
4. Distinguish between progressive and stationary waves in a table (five points). [5]
5. (a) State the principle of superposition. [1] (b) Two pulses of heights $+2\ \text{cm}$ and $+3\ \text{cm}$ travel towards each other on a string; describe what you see as they meet and after. [2] (c) Repeat with $+3\ \text{cm}$ and $-3\ \text{cm}$. [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) A **progressive wave** is a disturbance that travels through a medium, transferring energy from one place to another without transferring the medium itself. A **stationary (standing) wave** is formed by the superposition of two identical progressive waves travelling in opposite directions; the pattern stays in place and no energy is transferred along the medium.

(b) A wave travelling in the $+x$ direction:
$$ y = A\sin(\omega t-kx) $$
Here $y$ is the displacement of the particle at position $x$ at time $t$, $A$ the **amplitude**, $\omega = 2\pi f$ the **angular frequency** (rad $\text{s}^{-1}$), and $k = 2\pi/\lambda$ the **angular wave number** (rad $\text{m}^{-1}$). The wave speed is $v = f\lambda = \omega/k$. For a wave travelling in the $-x$ direction, use $\sin(\omega t+kx)$.

**2.** (a) A wave travelling along a string is reflected at the fixed end with a phase change of $\pi$. The incident and reflected waves, of the same frequency and amplitude, travel in opposite directions and superpose. At some points they always cancel (**nodes**); at others they always reinforce (**antinodes**). The pattern does not move, hence "stationary".

(b) Let the incident wave be $y_1 = A\sin(\omega t-kx)$ and the reflected wave $y_2 = A\sin(\omega t+kx)$. The resultant is
$$ y = y_1+y_2 = 2A\cos kx\,\sin\omega t $$
The amplitude at $x$ is $2A\cos kx$. Nodes are where $\cos kx = 0$:
$$ kx = \left(n+\tfrac12\right)\pi\ \Rightarrow\ x_n = \left(n+\tfrac12\right)\frac{\lambda}{2} $$
Consecutive nodes ($n$ and $n+1$) are at
$$ x_{n+1}-x_n = \frac{\lambda}{2} $$
(Antinodes, where $|\cos kx| = 1$, are also $\lambda/2$ apart and lie midway between nodes, $\lambda/4$ from each.)

**3.** Compare with $y = A\sin(\omega t-kx)$: $A = 0.05\ \text{m}$, $\omega = 40\ \text{rad s}^{-1}$, $k = 2\ \text{rad m}^{-1}$.
$$ f = \frac{\omega}{2\pi} = \frac{40}{2\pi} = 6.4\ \text{Hz} $$
$$ \lambda = \frac{2\pi}{k} = \pi = 3.14\ \text{m} $$
$$ v = \frac{\omega}{k} = \frac{40}{2} = 20\ \text{m s}^{-1} $$
$$ \Delta\phi = k\,\Delta x = 2\times0.50 = 1.0\ \text{rad} $$

**4.**

| Progressive wave | Stationary wave |
|---|---|
| The disturbance travels forward | The pattern stays in place |
| Energy is transferred along the medium | No net energy is transferred |
| All particles have the same amplitude | Amplitude varies from zero (node) to maximum (antinode) |
| Phase differs from particle to particle | All particles between two nodes are in the same phase |
| No nodes or antinodes | Nodes and antinodes, $\lambda/2$ apart |

**5.** (a) **Superposition:** when two or more waves overlap, the resultant displacement at any point is the algebraic sum of the displacements that each wave would produce alone.

(b) As the pulses overlap, the string at the centre has height $2+3 = 5\ \text{cm}$ at the instant they coincide. They then pass through each other and emerge with their original shapes and sizes (waves do not collide like particles).

(c) The displacements $+3$ and $-3\ \text{cm}$ cancel: at the instant of complete overlap the string is flat everywhere there, and the energy is momentarily all kinetic; the pulses then continue unchanged.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Derive the equation of a stationary wave formed on a string fixed at both ends. [3] (b) Find the positions of nodes and antinodes. [3] (c) Show that the distance between consecutive nodes is $\lambda/2$. [2] <span class="marks">[8]</span> (NEB 2082)
2. (a) Derive the equation $y = A\sin(\omega t-kx)$ for a progressive wave. [3] (b) Find the phase difference between two particles $x_1$ and $x_2$ apart. [2] (c) A progressive wave on a string is $y = 4.0\sin(50t-0.25x)$ (cm, s, cm). Find the wavelength, speed, the maximum particle velocity and the phase difference between particles $10\ \text{cm}$ apart. [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) Let the incident wave be $y_1 = A\sin(\omega t-kx)$. At the fixed end the reflected wave is $y_2 = -A\sin(\omega t+kx)$ for a reflection with a phase change of $\pi$ (taking the end at $x = 0$). Adding,
$$ y = A\sin(\omega t-kx)-A\sin(\omega t+kx) $$
Using $\sin C-\sin D = 2\cos\frac{C+D}{2}\sin\frac{C-D}{2}$:
$$ y = -2A\sin kx\,\cos\omega t $$
The amplitude $2A\sin kx$ depends on position, and every particle vibrates in SHM of frequency $f$ with its own amplitude.

(b) **Nodes** have zero amplitude, $\sin kx = 0$:
$$ kx = n\pi\ \Rightarrow\ x = \frac{n\lambda}{2},\quad n = 0, 1, 2,\dots $$
**Antinodes** have maximum amplitude, $|\sin kx| = 1$:
$$ kx = \left(n+\tfrac12\right)\pi\ \Rightarrow\ x = \left(n+\tfrac12\right)\frac{\lambda}{2} = (2n+1)\frac{\lambda}{4} $$

(c) Consecutive nodes: $x_{n+1}-x_n = \dfrac{(n+1)\lambda}{2}-\dfrac{n\lambda}{2} = \dfrac{\lambda}{2}$. For a string fixed at both ends of length $L$, both ends are nodes, which quantizes $L = n\lambda/2$ and leads to the harmonics $f_n = nv/2L$ (section 3.8).

**2.** (a) A source at $x = 0$ vibrates as $y = A\sin\omega t$. The disturbance travels at speed $v$, so a point at distance $x$ copies the source motion a time $x/v$ later:
$$ y = A\sin\omega\left(t-\frac{x}{v}\right) = A\sin(\omega t-kx),\qquad k = \frac{\omega}{v} = \frac{2\pi}{\lambda} $$

(b) The phase at $x$ is $\omega t-kx$. For two points $\Delta x = x_2-x_1$ apart at the same time,
$$ \Delta\phi = k\,\Delta x = \frac{2\pi}{\lambda}\,\Delta x $$
One wavelength corresponds to $2\pi$.

(c) $A = 4.0\ \text{cm}$, $\omega = 50\ \text{rad s}^{-1}$, $k = 0.25\ \text{cm}^{-1}$.
$$ \lambda = \frac{2\pi}{k} = \frac{2\pi}{0.25} = 25\ \text{cm} $$
$$ v = \frac{\omega}{k} = \frac{50}{0.25} = 200\ \text{cm s}^{-1} = 2.0\ \text{m s}^{-1} $$
$$ v_{particle,max} = A\omega = 4.0\times50 = 200\ \text{cm s}^{-1} $$
$$ \Delta\phi = k\,\Delta x = 0.25\times10 = 2.5\ \text{rad} $$
:::

::: tip Examiner's note — Wave motion
Mark-earners are the **two component waves written out**, the use of the sum-to-product identity, and the clear statement that amplitude depends on position. State the reflection phase change ($\pi$ at a fixed end, $0$ at a free end) because it decides whether there is a node or an antinode at the end. In numericals, take $\omega$ and $k$ straight from the equation and check units: $v = \omega/k$ needs the *same* length unit in $k$ as in the answer.
:::

## 3.7 Mechanical waves

CDC allots **4 teaching hours**. The Newton–Laplace story has been asked in 2080 and 2081, and it is the single most predictable Group B item in Waves; the effect of temperature and pressure (asked in 2082) follows from the same formula.

**Short answer questions [5 marks each]**

1. (a) State Newton's formula for the speed of sound in air and its discrepancy with experiment. [2] (b) State Laplace's correction. [2] (c) Why are sound waves in a gas called pressure waves? [1] <span class="marks">[5]</span> (NEB 2080)
2. (a) State Laplace's correction and write the corrected formula. [3] (b) Find the wavelength in air at $25\ ^{\circ}\text{C}$ of a note of $256\ \text{Hz}$, given that the speed at $0\ ^{\circ}\text{C}$ is $330\ \text{m s}^{-1}$. [2] <span class="marks">[5]</span> (NEB 2081)
3. (a) How do temperature and pressure affect the speed of sound in a gas? [2] (b) How does humidity affect it? [1] (c) Find the speed of sound in air at $27\ ^{\circ}\text{C}$ if it is $332\ \text{m s}^{-1}$ at $0\ ^{\circ}\text{C}$. [2] <span class="marks">[5]</span> (NEB 2082)
4. (a) Write the expressions for the speed of a longitudinal wave in a solid and in a liquid. [2] (b) Find the speed in steel ($Y = 2.0\times10^{11}\ \text{Pa}$, $\rho = 7800\ \text{kg m}^{-3}$) and in water ($K = 2.2\times10^{9}\ \text{Pa}$, $\rho = 1000\ \text{kg m}^{-3}$). [3] <span class="marks">[5]</span>
5. Show that the speed of sound in an ideal gas is proportional to $\sqrt{T}$ and calculate the speed in air at $300\ \text{K}$ if it is $331\ \text{m s}^{-1}$ at $273\ \text{K}$. [5]

::: note Model answers — short
**1.** (a) **Newton:** sound passes through air so slowly that the compressions and rarefactions are **isothermal**, and the speed is
$$ v = \sqrt{\frac{P}{\rho}} $$
At $0\ ^{\circ}\text{C}$, $P = 1.01\times10^{5}\ \text{Pa}$ and $\rho = 1.29\ \text{kg m}^{-3}$ give $280\ \text{m s}^{-1}$, whereas the measured value is about $332\ \text{m s}^{-1}$: a discrepancy of about $16\%$.

(b) **Laplace:** the compressions and rarefactions in a sound wave occur so rapidly that heat has no time to flow between layers, and the changes are **adiabatic**, so the bulk modulus is $\gamma P$, not $P$:
$$ v = \sqrt{\frac{\gamma P}{\rho}} $$
With $\gamma = 1.4$ the speed is $\sqrt{1.4}\times280 = 331\ \text{m s}^{-1}$, agreeing with experiment.

(c) Sound in a gas is a series of compressions (pressure above the mean) and rarefactions (pressure below the mean) travelling outwards; the pressure at each point varies about the atmospheric value, and it is this pressure variation that the ear detects.

**2.** (a) **Laplace's correction:** the changes of pressure and volume in a sound wave are adiabatic, not isothermal, so in Newton's formula $P$ must be replaced by $\gamma P$ (because the adiabatic bulk modulus of an ideal gas is $\gamma P$):
$$ v = \sqrt{\frac{\gamma P}{\rho}},\qquad \gamma = \frac{C_P}{C_V} = 1.40\ \text{for air} $$
(b) The speed varies with temperature as $v_t\approx v_0+0.61\,t$ ($t$ in $^{\circ}\text{C}$), so
$$ v_{25} = 330+0.61\times25 = 345\ \text{m s}^{-1} $$
$$ \lambda = \frac{v}{f} = \frac{345}{256} = 1.35\ \text{m} $$
(Using $v\propto\sqrt{T}$: $330\sqrt{298/273} = 345\ \text{m s}^{-1}$, the same.)

**3.** (a) For an ideal gas $P/\rho = RT/M$, so $v = \sqrt{\gamma RT/M}\propto\sqrt{T}$: **the speed rises with temperature**, about $0.61\ \text{m s}^{-1}$ per $^{\circ}\text{C}$ near room temperature. At constant temperature a change of **pressure has no effect**, because $\rho\propto P$ and the ratio $P/\rho$ stays constant.

(b) **Humidity:** moist air is less dense than dry air at the same $P$ and $T$ (water vapour, molar mass $18$, replaces $\text{N}_2$ and $\text{O}_2$), so sound travels slightly faster in damp air.

(c) 
$$ v_{27} = 332+0.61\times27 = 348\ \text{m s}^{-1} $$

**4.** (a) **Solid:** $v = \sqrt{Y/\rho}$, where $Y$ is Young's modulus. **Liquid:** $v = \sqrt{K/\rho}$, where $K$ is the bulk modulus. (A solid also carries transverse waves at $\sqrt{\eta/\rho}$, with $\eta$ the rigidity modulus.)

(b) 
$$ v_{steel} = \sqrt{\frac{2.0\times10^{11}}{7800}} = 5.06\times10^{3}\ \text{m s}^{-1} $$
$$ v_{water} = \sqrt{\frac{2.2\times10^{9}}{1000}} = 1.48\times10^{3}\ \text{m s}^{-1} $$

**5.** From Laplace's formula with $P = \rho RT/M$ for an ideal gas ($M$ the molar mass),
$$ v = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\frac{\gamma RT}{M}}\propto\sqrt{T} $$
$$ \frac{v_{300}}{v_{273}} = \sqrt{\frac{300}{273}} = 1.048 $$
$$ v_{300} = 331\times1.048 = 347\ \text{m s}^{-1} $$
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Derive the expression for the speed of a longitudinal pulse in a fluid in terms of its bulk modulus and density. [4] (b) Hence state Newton's formula and Laplace's correction. [2] (c) Calculate the speed of sound in air at $0\ ^{\circ}\text{C}$ from Laplace's formula ($\gamma = 1.40$, $P = 1.013\times10^{5}\ \text{Pa}$, $\rho = 1.293\ \text{kg m}^{-3}$). [2] <span class="marks">[8]</span>
2. (a) Explain the effect of (i) temperature, (ii) pressure and (iii) humidity on the speed of sound. [3] (b) A bat emits a pulse and hears the echo from a wall $0.50\ \text{s}$ later at an air temperature of $20\ ^{\circ}\text{C}$ ($v_0 = 332\ \text{m s}^{-1}$). How far is the wall? [2] (c) A sound wave in air has a pressure amplitude of $3.0\times10^{-2}\ \text{Pa}$ and frequency $1000\ \text{Hz}$. Using $B = 1.42\times10^{5}\ \text{Pa}$ and $v = 344\ \text{m s}^{-1}$, find the displacement amplitude. [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) Let a piston in a long tube of fluid (cross-section $A$, density $\rho$, bulk modulus $B$) suddenly move with speed $u$ for a time $\Delta t$. A compression pulse travels ahead at speed $v$, so in $\Delta t$ it covers $v\Delta t$ of fluid, which has mass $\rho Av\Delta t$ and is brought from rest to speed $u$. The piston moves a distance $u\Delta t$, so the volume of the compressed part shrinks by $Au\Delta t$ from $Av\Delta t$: the fractional change is $\Delta V/V = -u/v$.
The excess pressure needed is, by the definition of the bulk modulus,
$$ \Delta P = -B\,\frac{\Delta V}{V} = B\,\frac{u}{v} $$
Newton's second law (impulse = change of momentum) applied to the pulse:
$$ \Delta P\,A\,\Delta t = (\rho Av\Delta t)\,u $$
$$ \Delta P = \rho v u $$
Equating the two expressions for $\Delta P$:
$$ B\frac{u}{v} = \rho vu\ \Rightarrow\ v = \sqrt{\frac{B}{\rho}} $$

(b) For a gas held at constant temperature (isothermal) $B = P$, giving **Newton's formula** $v = \sqrt{P/\rho}$. Laplace showed that the changes are adiabatic, for which $B = \gamma P$, giving $v = \sqrt{\gamma P/\rho}$.

(c) 
$$ v = \sqrt{\frac{1.40\times1.013\times10^{5}}{1.293}} = \sqrt{1.097\times10^{5}} = 331\ \text{m s}^{-1} $$

**2.** (a) (i) **Temperature:** $v\propto\sqrt{T}$, so heating air makes sound faster, by about $0.61\ \text{m s}^{-1}$ per degree. (ii) **Pressure:** no effect if $T$ is constant, because $P/\rho$ is constant. (iii) **Humidity:** moist air is less dense, so the speed is higher.

(b) $v_{20} = 332+0.61\times20 = 344\ \text{m s}^{-1}$. The echo covers the distance to the wall and back in $0.50\ \text{s}$:
$$ d = \frac{vt}{2} = \frac{344\times0.50}{2} = 86\ \text{m} $$

(c) The pressure and displacement amplitudes are related by $p_{max} = Bk\,s_{max}$, with $k = 2\pi f/v$:
$$ k = \frac{2\pi\times1000}{344} = 18.3\ \text{m}^{-1} $$
$$ s_{max} = \frac{p_{max}}{Bk} = \frac{3.0\times10^{-2}}{1.42\times10^{5}\times18.3} = 1.2\times10^{-8}\ \text{m} $$
:::

::: tip Examiner's note — Mechanical waves
Both stories must be told: **what Newton assumed** (isothermal, $B = P$), **the number that shows it fails** ($280$ against $332\ \text{m s}^{-1}$), and **what Laplace changed** (adiabatic, $B = \gamma P$). Mention that the changes are too fast for heat to flow — that is the reason, and it is what the marker looks for. In the temperature numericals, be consistent: either $v_t = v_0+0.61t$ or $v\propto\sqrt{T}$ with kelvin — do not mix them inside one calculation.
:::

## 3.8 Wave in pipes and strings

CDC allots **4 teaching hours**. Stationary waves in pipes and strings are examined every year (2080 Group B, 2081 and 2082 Group C); the sonometer beat problem of the 2079 model and the $v = \sqrt{T/\mu}$ scaling arguments are the most repeated numerical forms.

**Short answer questions [5 marks each]**

1. (a) A sonometer wire $75\ \text{cm}$ long is in resonance with a tuning fork. Shortening the wire by $0.50\ \text{cm}$ gives $3$ beats per second with the fork. Find the frequency of the fork. [3] (b) A vibrator of $120\ \text{Hz}$ sets up a stationary wave with $3$ loops on a string $1.2\ \text{m}$ long; find the speed of the progressive wave. [2] <span class="marks">[5]</span> (NEB 2079 model, part (a))
2. (a) Define harmonic and overtone. [1] (b) A string $0.80\ \text{m}$ long, under tension $64\ \text{N}$, has mass per unit length $4.0\times10^{-3}\ \text{kg m}^{-1}$: find the frequency of its first overtone. [2] (c) What is the new frequency if the tension is made four times as large? [2] <span class="marks">[5]</span>
3. (a) A flute $30\ \text{cm}$ long, open at both ends, sounds its first harmonic; find the frequency ($v = 330\ \text{m s}^{-1}$). [2] (b) Define harmonic in music. [1] (c) Why does the pitch of a bus horn seem to drop as it passes you? [2] <span class="marks">[5]</span> (NEB 2078)
4. (a) What is end correction? [1] (b) In a resonance-tube experiment with a fork of $512\ \text{Hz}$, resonance occurs at $16.0\ \text{cm}$ and $50.5\ \text{cm}$. Find the speed of sound and the end correction. [4] <span class="marks">[5]</span>
5. (a) State the laws of transverse vibration of a fixed string. [3] (b) A string vibrates at $200\ \text{Hz}$; find the frequency if its length is halved and its tension is quadrupled. [2] <span class="marks">[5]</span>
6. Compare the harmonics of an open pipe and a closed pipe of the same length in a table (fundamental, allowed harmonics, ratio of the first three). [5]

::: note Model answers — short (1–3)
**1.** (a) A sonometer wire has $f\propto1/L$. Let the fork's frequency be $f$; at resonance the $75\ \text{cm}$ wire also vibrates at $f$. The shortened wire ($74.5\ \text{cm}$) vibrates faster:
$$ f' = f\,\frac{75}{74.5} $$
$$ f'-f = 3 = f\left(\frac{75}{74.5}-1\right) = f\times\frac{0.5}{74.5} $$
$$ f = \frac{3\times74.5}{0.5} = 447\ \text{Hz} $$
(b) With $3$ loops, $L = 3\lambda/2$, so $\lambda = 2L/3 = 0.80\ \text{m}$ and
$$ v = f\lambda = 120\times0.80 = 96\ \text{m s}^{-1} $$

**2.** (a) The lowest frequency of a vibrating system is the **fundamental** (first harmonic). Higher frequencies that are integer multiples of it are **harmonics** (second, third, …). An **overtone** is any mode above the fundamental: the first overtone is the second harmonic (for an open pipe or a string), the second overtone is the third harmonic, and so on.

(b) 
$$ v = \sqrt{\frac{T}{\mu}} = \sqrt{\frac{64}{4.0\times10^{-3}}} = 126\ \text{m s}^{-1} $$
$$ f_1 = \frac{v}{2L} = \frac{126}{2\times0.80} = 79\ \text{Hz} $$
The first overtone is the second harmonic, $f_2 = 2f_1 = 158\ \text{Hz}$.

(c) $f\propto\sqrt{T}$, so quadrupling the tension doubles every frequency: the first overtone becomes $2\times158 = 316\ \text{Hz}$.

**3.** (a) An open pipe has antinodes at both ends and $L = \lambda/2$ for the fundamental:
$$ f_1 = \frac{v}{2L} = \frac{330}{2\times0.30} = 550\ \text{Hz} $$
(b) In music a **harmonic** is a component of a note whose frequency is an integer multiple of the fundamental; the mix of harmonics determines the quality (timbre) of the note.

(c) By the Doppler effect: while the bus approaches, each successive sound crest is emitted closer to you and arrives more often, so the frequency is higher; after it passes, successive crests start farther away, so the frequency is lower. The horn's actual frequency does not change.
:::

::: note Model answers — short (4–6)
**4.** (a) At an open end the antinode is not exactly at the mouth of the pipe but a little outside it, at a distance $e\approx0.6\,r$ (for a pipe of radius $r$); this extra length is the **end correction**. The effective length is $L+e$.

(b) For a closed pipe, the first resonance is at $L_1+e = \lambda/4$ and the second at $L_2+e = 3\lambda/4$. Subtracting,
$$ L_2-L_1 = \frac{\lambda}{2}\ \Rightarrow\ \lambda = 2(0.505-0.160) = 0.690\ \text{m} $$
$$ v = f\lambda = 512\times0.690 = 353\ \text{m s}^{-1} $$
$$ e = \frac{L_2-3L_1}{2} = \frac{50.5-48.0}{2} = 1.3\ \text{cm} $$
(Using the first resonance, $e = \lambda/4-L_1 = 17.25-16.0 = 1.25\ \text{cm}$.)

**5.** (a) For a string of length $L$, tension $T$ and mass per unit length $\mu$ vibrating in a given mode: **Law of length** — $f\propto1/L$ (at fixed $T$ and $\mu$). **Law of tension** — $f\propto\sqrt{T}$ (at fixed $L$ and $\mu$). **Law of mass** — $f\propto1/\sqrt{\mu}$ (at fixed $L$ and $T$). These combine in $f = \dfrac{1}{2L}\sqrt{T/\mu}$.

(b) 
$$ \frac{f'}{f} = \frac{L}{L/2}\sqrt{\frac{4T}{T}} = 2\times2 = 4 $$
$$ f' = 4\times200 = 800\ \text{Hz} $$

**6.**

| | Open pipe | Closed pipe (one end closed) |
|---|---|---|
| Ends | antinode at both | node at closed end, antinode at open end |
| Fundamental | $v/2L$ | $v/4L$ |
| Harmonics present | all: $1, 2, 3, \dots$ | only odd: $1, 3, 5, \dots$ |
| First three | $f, 2f, 3f$ | $f, 3f, 5f$ |
| Ratio | $1:2:3$ | $1:3:5$ |
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Describe the stationary waves in an open and in a closed organ pipe, drawing the first three modes of each. [3] (b) Derive the frequencies of the harmonics for both. [3] (c) An open pipe and a closed pipe each have fundamental $264\ \text{Hz}$; find the lengths ($v = 340\ \text{m s}^{-1}$) and the frequency of the first overtone of each. [2] <span class="marks">[8]</span>
2. (a) Derive $f_n = \dfrac{n}{2L}\sqrt{T/\mu}$ for a string fixed at both ends. [3] (b) A guitar string of length $1.5\ \text{m}$ is made of steel of density $7800\ \text{kg m}^{-3}$ and Young's modulus $2\times10^{11}\ \text{N m}^{-2}$, stretched by $1\%$. Find the stress and the frequency of the second mode. [3] (c) What happens to the speed of a transverse wave if the radius of the string is doubled at constant tension? [2] <span class="marks">[8]</span> (NEB 2081 and 2082, parts)
3. (a) State the laws of vibration of a fixed string and describe the sonometer experiment that verifies the law of length. [4] (b) Two wires of the same material, radii in the ratio $1:2$, are stretched with equal tension and have equal lengths; compare their fundamental frequencies. [2] (c) A $0.60\ \text{m}$ wire of mass $4.8\ \text{g}$ is under a tension of $120\ \text{N}$; find its fundamental and third harmonic. [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Open pipe:** both ends are antinodes of displacement (pressure nodes). The three simplest modes have $L = \lambda/2,\ \lambda,\ 3\lambda/2$ (figure below, left). **Closed pipe:** the closed end is a node, the open end an antinode; the modes have $L = \lambda/4,\ 3\lambda/4,\ 5\lambda/4$ (figure below, right).

(b) *Open pipe:* $L = n\lambda_n/2$, so $\lambda_n = 2L/n$ and
$$ f_n = \frac{v}{\lambda_n} = \frac{nv}{2L},\quad n = 1, 2, 3,\dots $$
*Closed pipe:* $L = (2n-1)\lambda_n/4$, so $\lambda_n = 4L/(2n-1)$ and
$$ f_n = \frac{(2n-1)v}{4L} = (2n-1)f_1,\quad n = 1, 2, 3,\dots $$

(c) Open pipe: $L = \dfrac{v}{2f_1} = \dfrac{340}{2\times264} = 0.64\ \text{m}$; first overtone $= 2f_1 = 528\ \text{Hz}$. Closed pipe: $L = \dfrac{v}{4f_1} = \dfrac{340}{4\times264} = 0.32\ \text{m}$; first overtone $= 3f_1 = 792\ \text{Hz}$.

**2.** (a) A transverse wave on a string travels at $v = \sqrt{T/\mu}$. For a string fixed at both ends of length $L$, both ends are nodes, so the stationary wave must fit an integral number of half-wavelengths: $L = n\lambda_n/2$, $\lambda_n = 2L/n$. Then
$$ f_n = \frac{v}{\lambda_n} = \frac{n}{2L}\sqrt{\frac{T}{\mu}},\quad n = 1, 2, 3,\dots $$
(b) Stress $=$ Young's modulus $\times$ strain:
$$ \sigma = Y\times\text{strain} = 2\times10^{11}\times0.01 = 2\times10^{9}\ \text{N m}^{-2} $$
With $T = \sigma A$ and $\mu = \rho A$, the area cancels in $v = \sqrt{T/\mu} = \sqrt{\sigma/\rho}$:
$$ v = \sqrt{\frac{2\times10^{9}}{7800}} = 506\ \text{m s}^{-1} $$
The second mode ($n = 2$) has $f_2 = \dfrac{2v}{2L} = \dfrac{v}{L} = \dfrac{506}{1.5} = 338\ \text{Hz}$.

(c) $\mu = \rho\pi r^{2}$ increases four times when $r$ doubles, so $v = \sqrt{T/\mu}$ falls to **half**.

**3.** (a) The laws are stated in short answer 5(a). **Sonometer experiment:** a wire is stretched over two bridges on a wooden box and kept under a fixed tension by a hanging load. A tuning fork of known frequency is sounded and a light paper rider is placed on the wire; the movable bridge is adjusted until the rider is thrown off, which shows resonance, and the vibrating length $L$ is measured. Repeating with forks of several frequencies, one finds $f\times L$ is constant, i.e. $f\propto1/L$.

(b) $\mu = \rho\pi r^{2}$, so for equal $T$ and $L$, $f\propto1/\sqrt{\mu}\propto1/r$. With $r_1:r_2 = 1:2$, $f_1:f_2 = 2:1$: the thinner wire vibrates twice as fast.

(c) $\mu = \dfrac{4.8\times10^{-3}}{0.60} = 8.0\times10^{-3}\ \text{kg m}^{-1}$.
$$ v = \sqrt{\frac{120}{8.0\times10^{-3}}} = 122\ \text{m s}^{-1} $$
$$ f_1 = \frac{v}{2L} = \frac{122}{1.2} = 102\ \text{Hz},\qquad f_3 = 3f_1 = 306\ \text{Hz} $$
:::

```figure caption="Stationary waves in pipes (displacement envelope). Left: open pipe, fundamental and first two overtones. Right: closed pipe (node at the closed end on the left), fundamental and first two overtones."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.9))
x = np.linspace(0, 1, 200)
def draw(ax, shapes, labels, closed):
    for i, (y, lab) in enumerate(zip(shapes, labels)):
        off = -i*1.0
        ax.plot(x, y+off, color=ACCENT, lw=1.6)
        ax.plot(x, -y+off, color=ACCENT, lw=1.6)
        ax.text(1.05, off, lab, fontsize=8, va='center', color=INK)
    top = 0.55; bot = -2.55
    ax.plot([0, 1], [top, top], color=INK, lw=1.2)
    ax.plot([0, 1], [bot, bot], color=INK, lw=1.2)
    if closed:
        ax.plot([0, 0], [bot, top], color=INK, lw=3)
    ax.set_xlim(-0.08, 1.5); ax.set_ylim(bot-0.1, top+0.1)
    ax.axis('off')
draw(a1, [0.4*np.abs(np.cos(n*np.pi*x)) for n in (1, 2, 3)],
     ['$f_1$', '$2f_1$', '$3f_1$'], False)
draw(a2, [0.4*np.abs(np.sin(m*np.pi*x/2)) for m in (1, 3, 5)],
     ['$f_1$', '$3f_1$', '$5f_1$'], True)
a1.set_title('open pipe', fontsize=9, color=INK)
a2.set_title('closed pipe', fontsize=9, color=INK)
fig.tight_layout()
```

::: tip Examiner's note — Wave in pipes and strings
In pipe questions **draw the pattern first**: one sketch tells you where the nodes and antinodes are and gives $L$ in terms of $\lambda$. Do not write "$f = v/4L$" for an open pipe — a classic slip that costs the whole numerical. For strings, prefer the combined formula $f = (n/2L)\sqrt{T/\mu}$ and substitute ratios rather than absolute values when the question says "if the tension is quadrupled". In the sonometer beat problem, say clearly that *shortening raises the frequency*; choosing the wrong sign gives a different answer.
:::

## 3.9 Acoustic phenomena

CDC allots **5 teaching hours**. Doppler numericals have appeared in 2078, 2079 model, 2081 and 2082; intensity, pressure amplitude and the characteristics of sound make up the rest.

**Short answer questions [5 marks each]**

1. (a) A train travelling at $30\ \text{m s}^{-1}$ in still air sounds a whistle of $262\ \text{Hz}$. A passenger on another train moving at $18\ \text{m s}^{-1}$ in the opposite direction hears it. Find the frequency heard (i) while the trains approach and (ii) after they have passed, taking $v = 340\ \text{m s}^{-1}$. [2+2] (b) How does the intensity of sound change if the distance from the source increases four times? [1] <span class="marks">[5]</span> (NEB 2079 model)
2. A car horn of $400\ \text{Hz}$ is heard by a stationary listener with a frequency difference of $60\ \text{Hz}$ between approach and recession. Find the speed of the car ($v = 340\ \text{m s}^{-1}$). [5] <span class="marks">[5]</span> (NEB 2081, data)
3. A train moving at $10\ \text{m s}^{-1}$ towards a cliff sounds a horn of $600\ \text{Hz}$. Find the frequency of the echo heard by the driver [3] and explain why it is higher than $600\ \text{Hz}$. [2] <span class="marks">[5]</span> (NEB 2082, data)
4. In a sound wave the maximum pressure variation is $3.0\times10^{-2}\ \text{Pa}$ at $1000\ \text{Hz}$ in air ($v = 344\ \text{m s}^{-1}$, bulk modulus $1.42\times10^{5}\ \text{Pa}$). Find the maximum displacement [3] and say why it is so small. [2] <span class="marks">[5]</span> (NEB 2079 model)
5. Distinguish between intensity, loudness, pitch and quality of a sound. [5]
6. (a) Define intensity level in decibels. [2] (b) The intensity of a sound is $1.0\times10^{-5}\ \text{W m}^{-2}$; find its level ($I_0 = 10^{-12}\ \text{W m}^{-2}$). [1] (c) By how much does the level rise if the intensity is doubled? [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** The passenger (observer) moves at $u_o = 18\ \text{m s}^{-1}$ and the source at $u_s = 30\ \text{m s}^{-1}$.
(i) *Approaching:*
$$ f' = f\,\frac{v+u_o}{v-u_s} = 262\times\frac{340+18}{340-30} = 262\times\frac{358}{310} = 303\ \text{Hz} $$
(ii) *Receding:*
$$ f' = f\,\frac{v-u_o}{v+u_s} = 262\times\frac{340-18}{340+30} = 262\times\frac{322}{370} = 228\ \text{Hz} $$
(b) The intensity varies as $1/r^{2}$, so at four times the distance it is $1/16$ of its value.

**2.** For a source moving at speed $u$ past a stationary listener, the frequency on approach is $f_1 = \dfrac{fv}{v-u}$ and on recession $f_2 = \dfrac{fv}{v+u}$.
$$ f_1-f_2 = fv\left(\frac{1}{v-u}-\frac{1}{v+u}\right) = \frac{2fvu}{v^{2}-u^{2}} = 60 $$
With $f = 400$, $v = 340$: $272000\,u = 60\,(115600-u^{2})$, which gives $u^{2}+4533\,u-115600 = 0$, so
$$ u = \frac{-4533+\sqrt{4533^{2}+4\times115600}}{2} = 25\ \text{m s}^{-1} $$
As a check, since $u\ll v$, $\Delta f\approx2fu/v$ gives $u = 60\times340/800 = 25.5\ \text{m s}^{-1}$. The car moves at about $25\ \text{m s}^{-1}$, i.e. $90\ \text{km h}^{-1}$.

**3.** The cliff first acts as a stationary **observer** receiving $f_1$ from the moving source, and then as a stationary **source** emitting $f_1$ to the moving driver:
$$ f_1 = \frac{fv}{v-10},\qquad f_2 = f_1\,\frac{v+10}{v} = f\,\frac{v+10}{v-10} $$
$$ f_2 = 600\times\frac{340+10}{340-10} = 600\times\frac{350}{330} = 636\ \text{Hz} $$
It is higher because the train approaches the cliff twice over, in effect: the crests are compressed at the source (shorter wavelength) and the driver moves towards the returning crests, so both effects raise the frequency.

**4.** The relation $p_{max} = Bk\,s_{max}$ with $k = 2\pi f/v$:
$$ k = \frac{2\pi\times1000}{344} = 18.3\ \text{m}^{-1} $$
$$ s_{max} = \frac{3.0\times10^{-2}}{1.42\times10^{5}\times18.3} = 1.2\times10^{-8}\ \text{m} $$
The displacement is tiny because a pressure variation of only $3\times10^{-2}\ \text{Pa}$ (out of $10^{5}\ \text{Pa}$) corresponds to a fractional volume change of about $2\times10^{-7}$, so each particle moves only about $10^{-8}\ \text{m}$; yet the ear detects it.

**5.**

| Term | Meaning | Depends on |
|---|---|---|
| **Intensity** | energy flowing per second through unit area normal to the wave, $\text{W m}^{-2}$; objective | amplitude$^{2}$, frequency$^{2}$, distance |
| **Loudness** | the sensation of how strong a sound is; subjective | intensity and the ear's sensitivity (frequency) |
| **Pitch** | sensation of how high or low the note is | frequency |
| **Quality** (timbre) | what distinguishes two notes of the same pitch and loudness | number and strengths of harmonics (waveform) |

**6.** (a) The **intensity level** is $\beta = 10\log_{10}(I/I_0)$ decibels, where $I_0 = 10^{-12}\ \text{W m}^{-2}$ is the threshold of hearing.

(b) 
$$ \beta = 10\log_{10}\frac{10^{-5}}{10^{-12}} = 10\times7 = 70\ \text{dB} $$
(c) $\Delta\beta = 10\log_{10}2 = 3.0\ \text{dB}$, independent of the starting level.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) What is the Doppler effect? [1] (b) Derive the apparent frequency when a source moves towards a stationary observer and when an observer moves towards a stationary source. [4] (c) A source of $500\ \text{Hz}$ moves away at $34\ \text{m s}^{-1}$ from an observer moving towards it at $17\ \text{m s}^{-1}$; find the frequency heard ($v = 340\ \text{m s}^{-1}$). [3] <span class="marks">[8]</span>
2. (a) Explain the characteristics of sound. [3] (b) Derive the relation between displacement amplitude and pressure amplitude, $p_{max} = Bks_{max}$. [3] (c) The intensity of a sound is $10^{-6}\ \text{W m}^{-2}$ at $2\ \text{m}$; find the intensity and the level at $8\ \text{m}$. [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) The **Doppler effect** is the apparent change in the frequency of a wave heard by an observer when there is relative motion between the source and the observer.

(b) Let the speed of sound be $v$, the source frequency $f$ and its wavelength $\lambda = v/f$.
*Source moving at $u_s$ towards a stationary observer.* In one period $T = 1/f$ the source moves $u_sT$, so the wavelength in front is shortened:
$$ \lambda' = \lambda-u_sT = \frac{v-u_s}{f} $$
$$ f' = \frac{v}{\lambda'} = f\,\frac{v}{v-u_s} $$
*Observer moving at $u_o$ towards a stationary source.* The wavelength is unchanged, but the speed of the waves relative to the observer is $v+u_o$:
$$ f' = \frac{v+u_o}{\lambda} = f\,\frac{v+u_o}{v} $$
Combined (positive direction from observer to source):
$$ f' = f\,\frac{v+u_o}{v-u_s} $$
Change the sign of $u_s$ or $u_o$ for motion away.

(c) The source recedes ($+u_s$ in the denominator) while the observer approaches ($+u_o$ in the numerator):
$$ f' = 500\times\frac{340+17}{340+34} = 500\times\frac{357}{374} = 477\ \text{Hz} $$

**2.** (a) See short answer 5: intensity (objective), loudness (subjective, depends on intensity and frequency), pitch (frequency) and quality (harmonic content).

(b) For a wave $s = s_{max}\sin(\omega t-kx)$ in a fluid of bulk modulus $B$, the fractional volume change is $\Delta V/V = \partial s/\partial x = -ks_{max}\cos(\omega t-kx)$. The pressure change is
$$ \Delta P = -B\frac{\Delta V}{V} = Bks_{max}\cos(\omega t-kx) $$
so the pressure amplitude is
$$ p_{max} = Bk\,s_{max} $$
The pressure variation is $\pi/2$ out of phase with the displacement: pressure is greatest where the displacement is zero.

(c) Intensity obeys the inverse square law, $I\propto1/r^{2}$:
$$ I_8 = 10^{-6}\times\left(\frac{2}{8}\right)^{2} = 6.3\times10^{-8}\ \text{W m}^{-2} $$
$$ \beta_8 = 10\log_{10}\frac{6.3\times10^{-8}}{10^{-12}} = 10\times4.80 = 48\ \text{dB} $$
At $2\ \text{m}$ the level was $60\ \text{dB}$; quadrupling the distance lowers it by $12\ \text{dB}$.
:::

::: tip Examiner's note — Acoustic phenomena
Write the Doppler formula in its **general** form and then put in signs deliberately: toward $= +$ in the numerator for the observer, toward $= -$ in the denominator for the source. The most common mistake is to apply the observer formula when the *source* is moving (or the reverse). In echo problems there are **two** Doppler shifts — the wall is first an observer, then a source. Convert decibels carefully: $10\log_{10}$ of an *intensity* ratio (not amplitude).
:::

## 3.10 Nature and propagation of light

CDC allots **3 teaching hours**. Huygens' principle and the wave-theory derivations of reflection and refraction are "prove" questions; 2081 asked for a plane wavefront becoming spherical, and 2082 asked which phenomenon Huygens' construction does not explain.

**Short answer questions [5 marks each]**

1. (a) State Huygens' principle. [1] (b) Use it to show how a plane wavefront passing through a small aperture becomes spherical. [2] (c) What is a wavefront, and what is its shape for a point source and for a distant source? [2] <span class="marks">[5]</span> (NEB 2081, part)
2. Prove the law of reflection using Huygens' wave theory. [5]
3. (a) Prove Snell's law using Huygens' construction. [3] (b) Light of wavelength $600\ \text{nm}$ in air passes into glass of refractive index $1.5$; find its speed, wavelength and frequency in glass. [2] <span class="marks">[5]</span>
4. (a) Name two phenomena explained by the wave theory and one that is not. [3] (b) What did Foucault's experiment settle? [2] <span class="marks">[5]</span> (NEB 2082, part)
5. (a) Define refractive index in terms of the speeds of light. [1] (b) A ray goes from water ($n = 1.33$) into glass ($n = 1.50$); find the ratio of the speeds and of the wavelengths. [2] (c) Why does the frequency not change? [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) **Huygens' principle:** every point on a wavefront acts as a source of secondary wavelets, which spread out in all directions with the speed of the wave; the new wavefront after a time $t$ is the forward envelope (common tangent surface) of these wavelets.

(b) When a plane wavefront reaches a small aperture (of size comparable with the wavelength), only a few points on it can send wavelets through. With so few sources the envelope is part of a sphere: the wavefront beyond the aperture is **spherical**, centred on the aperture, and the light spreads out (diffraction).

(c) A **wavefront** is the locus of all points of a wave that are in the same phase at a given instant. It is a sphere for a point source, a plane for a very distant source, and a cylinder for a line source. Rays are normal to wavefronts.

**2.** Let a plane wavefront $AB$ fall obliquely on a plane mirror, with $A$ touching the mirror first; let $i$ be the angle of incidence. While the wavelet from $B$ travels the distance $BC = vt$ to the mirror, the wavelet from $A$ travels the same distance $AD = vt$ in the same medium. The reflected wavefront is the tangent $CD$ from $C$ to the wavelet centred at $A$.
In the right-angled triangles $ABC$ and $ADC$ the side $AC$ is common and $BC = AD = vt$. They are therefore congruent, and
$$ \angle BAC = \angle DCA\ \Rightarrow\ i = r $$
The incident ray, the reflected ray and the normal lie in one plane. This proves the **law of reflection**.

**3.** (a) A plane wavefront $AB$ is incident on the boundary between medium 1 (speed $v_1$) and medium 2 ($v_2$), at angle of incidence $i$. While the wavelet from $B$ reaches the boundary at $C$ in time $t$ ($BC = v_1t$), the wavelet from $A$ travels $AD = v_2t$ in medium 2. The refracted wavefront is $CD$, making angle $r$ with the boundary. From the two triangles with the common hypotenuse $AC$:
$$ \sin i = \frac{BC}{AC} = \frac{v_1t}{AC},\qquad \sin r = \frac{AD}{AC} = \frac{v_2t}{AC} $$
$$ \frac{\sin i}{\sin r} = \frac{v_1}{v_2} = \text{constant} $$
This is **Snell's law**; with $n = c/v$ it reads $n_1\sin i = n_2\sin r$.

(b) 
$$ v = \frac{c}{n} = \frac{3.0\times10^{8}}{1.5} = 2.0\times10^{8}\ \text{m s}^{-1} $$
$$ \lambda_g = \frac{\lambda_{air}}{n} = \frac{600}{1.5} = 400\ \text{nm} $$
The frequency is unchanged: $f = c/\lambda = 3.0\times10^{8}/(600\times10^{-9}) = 5.0\times10^{14}\ \text{Hz}$.

**4.** (a) Explained by the wave theory: **reflection and refraction** (Huygens' construction), **interference and diffraction** (superposition, bending) and **polarization** (transverse waves). Not explained: the **photoelectric effect**, which needs energy in quanta (photons).

(b) Foucault measured the speed of light in water and found it **less** than in air. The wave theory predicts $v = c/n<c$; Newton's corpuscular theory predicted a **greater** speed in a denser medium. The result ruled out the simple corpuscular theory.

**5.** (a) The **refractive index** of a medium is the ratio of the speed of light in vacuum to its speed in the medium: $n = c/v$.

(b) $\dfrac{v_w}{v_g} = \dfrac{n_g}{n_w} = \dfrac{1.50}{1.33} = 1.13$. Since $f$ is the same, $\dfrac{\lambda_w}{\lambda_g} = \dfrac{v_w}{v_g} = 1.13$.

(c) Wavefronts arriving at the boundary must leave it at the same rate, or they would pile up or be created at the boundary. The number of wavefronts per second — the frequency — is therefore the same in both media.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) State Huygens' principle. [1] (b) Using it, derive the laws of reflection and refraction of a plane wave. [5] (c) A ray goes from air into glass with $i = 60^{\circ}$ and $r = 35^{\circ}$; find the refractive index and the speed of light in the glass. [2] <span class="marks">[8]</span>
2. (a) Explain, using Huygens' principle, why light bends towards the normal on entering a denser medium. [2] (b) Derive the critical angle in terms of the speeds of light in the two media and find it for glass–air ($n = 1.5$). [3] (c) Explain how Huygens' principle accounts for the spread of light after a narrow slit. [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) See short answer 1(a).

(b) The constructions and the congruent and similar triangles are given in short answers 2 and 3(a); the results are $i = r$ for reflection and $\sin i/\sin r = v_1/v_2$ for refraction, with both rays and the normal in one plane.

(c) 
$$ n = \frac{\sin i}{\sin r} = \frac{\sin60^{\circ}}{\sin35^{\circ}} = \frac{0.866}{0.574} = 1.51 $$
$$ v = \frac{c}{n} = \frac{3.0\times10^{8}}{1.51} = 2.0\times10^{8}\ \text{m s}^{-1} $$

**2.** (a) On entering a denser medium the end of the wavefront that arrives first slows down, while the other end is still moving at the higher speed. The wavefront therefore swings round, so its normal (the ray) turns towards the normal to the surface: $r<i$.

(b) For light going from a denser medium 1 ($v_1$) to a rarer medium 2 ($v_2>v_1$), $\sin i/\sin r = v_1/v_2$. The **critical angle** $i_c$ is the angle of incidence for which $r = 90^{\circ}$:
$$ \sin i_c = \frac{v_1}{v_2} = \frac{n_2}{n_1} $$
For glass–air, $\sin i_c = 1/1.5$, so $i_c = 41.8^{\circ}$. For $i>i_c$ the refracted wavefront cannot be constructed: total internal reflection occurs.

(c) Every point of the wavefront in the slit acts as a secondary source. When the slit width is comparable with the wavelength there are few such sources and the envelope of their wavelets spreads well beyond the geometrical shadow edges: the wave **diffracts**. A wide slit leaves a large flat central part of wavefront, and the light bends only at the edges.
:::

::: tip Examiner's note — Nature and propagation of light
For the wave-theory proofs, **draw the construction**: wavefront $AB$, the boundary, the two distances $BC = v_1t$ and $AD = v_2t$, and the two triangles. A labelled diagram is worth about half the marks. Always state that the *frequency* is unchanged on refraction and that it is the wavelength and speed that change. When asked what Huygens cannot explain, answer *photoelectric effect* (not interference or diffraction).
:::

## 3.11 Interference

CDC allots **2 teaching hours**. Young's double slit is asked almost every year, often with a fringe-width numerical and the effect of immersing the apparatus in a liquid (2080), or the equal spacing of bright and dark fringes (2082 Group C).

**Short answer questions [5 marks each]**

1. (a) Define interference of light. [1] (b) What are coherent sources and how are they obtained in practice? [2] (c) Why are two separate light bulbs not coherent? [2] <span class="marks">[5]</span>
2. Show that the bright and dark fringes in Young's double-slit experiment are equally spaced, and derive the fringe width $\beta = \lambda D/d$. [5]
3. (a) Two waves of equal intensity $I$ superpose; find the resultant intensity for constructive and destructive interference. [3] (b) Write the general expression for the resultant intensity at phase difference $\phi$. [2] <span class="marks">[5]</span> (NEB 2081, part)
4. A double slit of separation $0.50\ \text{mm}$ is illuminated by green light of wavelength $546\ \text{nm}$; the screen is $0.80\ \text{m}$ away. Find the fringe width and the width of ten fringes. [5] (NEB 2079 model, data)
5. (a) What happens to the fringe width if the whole double-slit apparatus is immersed in water of refractive index $1.33$? [2] (b) Describe the pattern when white light is used. [3] <span class="marks">[5]</span> (NEB 2080, part)

::: note Model answers — short
**1.** (a) **Interference** is the redistribution of energy produced when two or more coherent light waves overlap: bright fringes where they reinforce and dark fringes where they cancel.

(b) **Coherent sources** emit waves of the same frequency with a constant phase difference. In practice they are obtained by **dividing a single wavefront** (Young's two slits) or a single beam by amplitude (thin films), so that any random change in the source phase appears equally in both.

(c) Two bulbs emit light in independent bursts of about $10^{-8}\ \text{s}$ with random phases; the phase difference between them changes randomly and faster than the eye can follow, so the pattern averages to uniform brightness.

**2.** Slits $S_1$ and $S_2$ are a distance $d$ apart, and the screen is a distance $D\gg d$ away. For a point $P$ at height $y$ above the central point $O$, the path difference is
$$ \Delta = S_2P-S_1P\approx\frac{yd}{D} $$
*Bright:* $\Delta = n\lambda$, so $y_n = \dfrac{n\lambda D}{d}$, $n = 0, 1, 2,\dots$ *Dark:* $\Delta = (n+\tfrac12)\lambda$, so $y_n' = \left(n+\tfrac12\right)\dfrac{\lambda D}{d}$.
The separation of consecutive bright fringes is
$$ \beta = y_{n+1}-y_n = \frac{\lambda D}{d} $$
and that of consecutive dark fringes is the same, $\dfrac{\lambda D}{d}$, independent of $n$. The fringes are **equally spaced**, with a dark fringe midway between successive bright ones.

**3.** (a) Two waves of amplitude $a$ superpose with phase difference $\phi$: the resultant amplitude is $R = 2a\cos(\phi/2)$, so $I\propto R^{2} = 4a^{2}\cos^{2}(\phi/2)$, i.e. $I_R = 4I\cos^{2}(\phi/2)$.
*Constructive* ($\phi = 0, 2\pi,\dots$): $I_{max} = 4I$. *Destructive* ($\phi = \pi, 3\pi,\dots$): $I_{min} = 0$.

(b) 
$$ I_R = I_1+I_2+2\sqrt{I_1I_2}\cos\phi $$
For $I_1 = I_2 = I$ this becomes $2I(1+\cos\phi) = 4I\cos^{2}(\phi/2)$. The average intensity is $2I$: energy is redistributed, not created.

**4.** 
$$ \beta = \frac{\lambda D}{d} = \frac{546\times10^{-9}\times0.80}{0.50\times10^{-3}} = 8.7\times10^{-4}\ \text{m} = 0.87\ \text{mm} $$
Ten fringes: $10\beta = 8.7\ \text{mm}$.

**5.** (a) In a medium of refractive index $\mu$ the wavelength becomes $\lambda' = \lambda/\mu$, so
$$ \beta' = \frac{\lambda'D}{d} = \frac{\beta}{\mu} = \frac{\beta}{1.33} = 0.75\,\beta $$
The fringes become narrower (closer together).

(b) With white light the **central fringe ($n = 0$) is white**, since all colours have zero path difference there. On either side are a few coloured fringes: in each order, blue (small $\lambda$, small $\beta$) is nearest the centre and red farthest. After a few orders the colours overlap and the pattern fades to uniform white.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Define interference and state the conditions for a sustained pattern. [2] (b) Derive the fringe width in Young's double-slit experiment. [3] (c) In such an experiment with $d = 0.30\ \text{mm}$ and $D = 1.5\ \text{m}$ the fringe width is $2.0\ \text{mm}$. Find $\lambda$, and the fringe width when the apparatus is immersed in a liquid of refractive index $1.25$. [3] <span class="marks">[8]</span>
2. (a) Derive the expression for the resultant intensity in two-beam interference. [3] (b) Show that the average intensity equals the sum of the two separate intensities. [2] (c) A thin transparent sheet of thickness $t$ and refractive index $\mu$ is placed over one slit; by how many fringes does the pattern shift? [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Interference** is the superposition of two coherent waves to give a stable pattern of maxima and minima of intensity. **Conditions:** the sources must be coherent; the amplitudes should be nearly equal for good contrast; the slit separation must be small compared with the distance to the screen; and the light should be nearly monochromatic.

(b) See short answer 2: $\beta = \lambda D/d$.

(c) 
$$ \lambda = \frac{\beta d}{D} = \frac{2.0\times10^{-3}\times0.30\times10^{-3}}{1.5} = 4.0\times10^{-7}\ \text{m} = 400\ \text{nm} $$
$$ \beta' = \frac{\beta}{\mu} = \frac{2.0}{1.25} = 1.6\ \text{mm} $$

**2.** (a) Let the two waves at $P$ be $y_1 = a_1\sin\omega t$ and $y_2 = a_2\sin(\omega t+\phi)$. Their sum is $R\sin(\omega t+\delta)$ with
$$ R^{2} = a_1^{2}+a_2^{2}+2a_1a_2\cos\phi $$
(from the phasor triangle). Intensity is proportional to the amplitude squared, so
$$ I = I_1+I_2+2\sqrt{I_1I_2}\cos\phi $$
For $I_1 = I_2 = I_0$: $I = 2I_0(1+\cos\phi) = 4I_0\cos^{2}(\phi/2)$.

(b) The average of $\cos\phi$ over the pattern is zero, so $\bar{I} = I_1+I_2$ ($= 2I_0$): energy is redistributed from the dark to the bright regions, not created or destroyed.

(c) The sheet adds an extra optical path $(\mu-1)t$ to that slit. The central bright fringe, where the total path difference is zero, moves towards the covered slit to the point where the geometrical path difference cancels the extra path. The shift, in fringes, is
$$ \text{number of fringes shifted} = \frac{(\mu-1)t}{\lambda} $$
:::

::: tip Examiner's note — Interference
In the fringe-width derivation the marks are for **path difference $\approx yd/D$**, the **bright and dark conditions**, and the statement that the spacing is **independent of $n$**; the last of these answers "show the fringes are equally spaced". Give both the $I = 4I_0\cos^{2}(\phi/2)$ form and the limiting values $4I_0$ and $0$. Do not say that energy is destroyed at dark fringes.
:::

## 3.12 Diffraction

CDC allots **3 teaching hours**. A grating numerical appears in almost every paper (2079 model, 2080, 2081, 2082); single-slit theory and resolving power are the usual other parts.

**Short answer questions [5 marks each]**

1. (a) A diffraction grating has $6000$ lines per cm. Find the angle of the second-order maximum for light of wavelength $5890\ \text{Å}$. [2] (b) Is a third-order maximum possible? [1] (c) Define diffraction. [2] <span class="marks">[5]</span> (NEB 2081)
2. A grating of $500$ lines per mm gives the second-order maximum at $30^{\circ}$. Find the wavelength of the light. [3] (b) Why do the maxima of a grating appear sharper than the fringes of a double slit? [2] <span class="marks">[5]</span> (NEB 2082)
3. Green light of wavelength $546\ \text{nm}$ falls on a grating of $3000$ lines per cm. (a) Find the angle of the second-order maximum. [2] (b) Which gives a more accurate measurement of wavelength, a double slit of $0.50\ \text{mm}$ or this grating, and why? [2] (c) State the condition for the highest order. [1] <span class="marks">[5]</span> (NEB 2079 model, part)
4. (a) Explain diffraction at a single slit and derive the condition for the minima. [3] (b) Find the width of the central maximum on a screen $1.0\ \text{m}$ away for a slit of $0.20\ \text{mm}$ and light of $600\ \text{nm}$. [2] <span class="marks">[5]</span>
5. (a) State the Rayleigh criterion for the resolution of two point sources. [2] (b) Find the minimum angular separation resolved by a telescope objective of diameter $10\ \text{cm}$ for $550\ \text{nm}$ light. [2] (c) How can the resolving power be increased? [1] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) The grating spacing is $d = \dfrac{1}{6000}\ \text{cm} = 1.667\times10^{-6}\ \text{m}$ and $\lambda = 5890\ \text{Å} = 5.89\times10^{-7}\ \text{m}$. For the $n$th maximum $d\sin\theta = n\lambda$:
$$ \sin\theta_2 = \frac{2\lambda}{d} = \frac{2\times5.89\times10^{-7}}{1.667\times10^{-6}} = 0.707\ \Rightarrow\ \theta_2 = 45^{\circ} $$
(b) For $n = 3$, $\sin\theta_3 = 3\lambda/d = 1.06>1$, which is impossible: **the third order cannot be observed**. The highest order satisfies $n<d/\lambda = 2.8$, i.e. $n = 2$.

(c) **Diffraction** is the bending of light around the edges of an obstacle or through a narrow aperture, spreading it into the geometrical shadow and producing a pattern of bright and dark fringes; it is marked when the size of the obstacle or aperture is comparable with the wavelength.

**2.** (a) $d = \dfrac{1}{500}\ \text{mm} = 2.0\times10^{-6}\ \text{m}$; $n = 2$, $\theta = 30^{\circ}$:
$$ \lambda = \frac{d\sin\theta}{n} = \frac{2.0\times10^{-6}\times0.5}{2} = 5.0\times10^{-7}\ \text{m} = 500\ \text{nm} $$
(b) A grating has a very large number $N$ of slits. For a direction slightly away from a principal maximum the waves from the $N$ slits have phases spread right round the cycle and cancel almost exactly, so each principal maximum is narrow and bright; a double slit has only two sources, so its fringes are broad and of gradually varying intensity.

**3.** (a) $d = \dfrac{1}{3000}\ \text{cm} = 3.33\times10^{-6}\ \text{m}$:
$$ \sin\theta_2 = \frac{2\times546\times10^{-9}}{3.33\times10^{-6}} = 0.328\ \Rightarrow\ \theta_2 = 19.1^{\circ} $$
(b) The **grating**. The maxima are far apart (angles measured to a fraction of a degree, not fringes of $0.9\ \text{mm}$ read with a ruler), sharp and bright, and $\lambda = d\sin\theta/n$ involves directly measured angles. In the double slit, $\beta = 0.87\ \text{mm}$ is small and has a fractional reading error several times larger.

(c) The highest order obeys $n<d/\lambda$ because $\sin\theta\leq 1$.

**4.** (a) A single slit of width $a$ is lit by a plane wavefront. Each point in the slit is a source of secondary wavelets. In a direction $\theta$ the paths from the two edges differ by $a\sin\theta$. If $a\sin\theta = \lambda$, divide the slit into two halves: for every point in the top half there is a point in the bottom half $a/2$ away whose wavelet is half a wavelength out of phase, so they cancel in pairs. The same holds for $a\sin\theta = n\lambda$:
$$ a\sin\theta = n\lambda,\quad n = 1, 2, 3,\dots\ \text{(minima)} $$
The central maximum lies between the first minima at $\theta = \pm\lambda/a$.

(b) Width of the central maximum $= 2\lambda D/a = \dfrac{2\times600\times10^{-9}\times1.0}{0.20\times10^{-3}} = 6.0\times10^{-3}\ \text{m} = 6.0\ \text{mm}$.

**5.** (a) **Rayleigh criterion:** two point sources are just resolved when the central maximum of the diffraction pattern of one falls on the first minimum of the pattern of the other; for a circular aperture of diameter $D$ the minimum angular separation is $\theta_{min} = 1.22\,\lambda/D$.

(b) 
$$ \theta_{min} = \frac{1.22\times550\times10^{-9}}{0.10} = 6.7\times10^{-6}\ \text{rad} $$
(c) Increase the diameter $D$ of the objective, or use light of shorter wavelength (as in the electron microscope, where $\lambda$ is about $10^{-11}\ \text{m}$).
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Describe and explain the diffraction pattern of a single slit, giving the intensity distribution qualitatively. [3] (b) Derive the condition for the first minimum and for the secondary maxima (approximately). [3] (c) A slit of width $0.10\ \text{mm}$ is lit by $500\ \text{nm}$ light; find the angular width of the central maximum. [2] <span class="marks">[8]</span>
2. (a) Explain the action of a plane transmission diffraction grating and derive $(a+b)\sin\theta = n\lambda$. [4] (b) A grating has $5000$ lines per cm. Find the angular positions of the first and second order for $600\ \text{nm}$ and the maximum order. [3] (c) What is seen if white light is used? [1] <span class="marks">[8]</span> (NEB 2080, data)

::: note Model answers — long
**1.** (a) Light from a narrow slit, instead of forming a sharp image, spreads out into a **broad bright central maximum** flanked by much weaker, narrower secondary maxima, separated by dark minima. The central band is twice as wide as each secondary one, and most of the energy is in it. The narrower the slit, the wider the pattern.

(b) The path difference between the edge rays is $a\sin\theta$. For the **first minimum**, $a\sin\theta = \lambda$: the slit divides into two halves whose wavelets cancel in pairs. The general minima are $a\sin\theta = n\lambda$. Secondary maxima lie approximately midway between successive minima, at
$$ a\sin\theta\approx\left(n+\tfrac12\right)\lambda,\quad n = 1, 2,\dots $$
and are of rapidly decreasing intensity ($4.5\%$, $1.6\%$, … of the central one).

(c) First minimum: $\sin\theta = \lambda/a = 5.0\times10^{-7}/1.0\times10^{-4} = 5.0\times10^{-3}$, so $\theta = 5.0\times10^{-3}\ \text{rad}$. The angular width of the central maximum is
$$ 2\theta = 1.0\times10^{-2}\ \text{rad} = 0.57^{\circ} $$

**2.** (a) A **plane transmission grating** is a glass plate ruled with a great many parallel, equally spaced opaque lines: the width of each transparent slit is $a$, of each opaque line $b$, so the grating spacing is $d = a+b$. A parallel beam falls normally on it. In a direction $\theta$ the rays from corresponding points of adjacent slits differ in path by $(a+b)\sin\theta$. They reinforce in every slit of the grating when this equals a whole number of wavelengths:
$$ (a+b)\sin\theta = n\lambda,\quad n = 0, 1, 2,\dots $$
These are the principal maxima; $n = 0$ is the undeviated central image.

(b) $d = \dfrac{1}{5000}\ \text{cm} = 2.0\times10^{-6}\ \text{m}$.
$$ \sin\theta_1 = \frac{600\times10^{-9}}{2.0\times10^{-6}} = 0.30\ \Rightarrow\ \theta_1 = 17.5^{\circ} $$
$$ \sin\theta_2 = 0.60\ \Rightarrow\ \theta_2 = 36.9^{\circ} $$
The maximum order: $n<d/\lambda = 3.3$, so $n_{max} = 3$ (at $\sin\theta_3 = 0.90$, $\theta_3 = 64.2^{\circ}$).

(c) White light gives a white central image ($n = 0$) and on either side a series of spectra in which violet is nearest the centre and red farthest (because $\sin\theta\propto\lambda$); higher orders overlap.
:::

::: tip Examiner's note — Diffraction
In grating numericals the first step is **$d = 1/N$ in metres** ($N$ in lines per metre): $6000\ \text{lines/cm} = 6\times10^{5}\ \text{lines/m}$. Always test whether the order asked for is possible: if $n\lambda/d>1$ the order does not exist, and the question "is the third order possible?" is worth a mark on its own. For single-slit work, remember that the given formula $a\sin\theta = n\lambda$ is for **minima**, not maxima — the classic confusion with the double slit and grating.
:::

## 3.13 Polarization

CDC allots **3 teaching hours**. Brewster's law has been asked with proof (2082) and as a numerical for water (2079 model); the sunglasses question of 2079 is a typical application.

**Short answer questions [5 marks each]**

1. (a) What is polarization of light? [1] (b) How can you tell a polaroid sunglass from an ordinary tinted one? [1] (c) What does polarization prove about the nature of light? [1] (d) Name two uses of polaroids. [2] <span class="marks">[5]</span> (NEB 2079 model, part)
2. (a) State Brewster's law. [1] (b) Find the angle of incidence at which light reflected from water ($\mu = 1.3$) is completely plane polarized. [2] (c) What is the angle of refraction then? [2] <span class="marks">[5]</span> (NEB 2079 model, part)
3. State and prove Brewster's law. [5] (NEB 2082)
4. (a) State Malus' law. [1] (b) Unpolarized light of intensity $I_0$ falls on two polaroids whose axes are at $60^{\circ}$; find the final intensity. [2] (c) What happens when the axes are crossed? [2] <span class="marks">[5]</span>
5. (a) Explain, with a diagram, how the transverse nature of light is shown by two tourmaline crystals. [3] (b) Why can sound waves not be polarized? [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) **Polarization** is the restriction of the vibrations of the electric vector of a transverse wave to a single plane (plane of vibration), perpendicular to the direction of travel.

(b) Look at glare (reflection from water or a road) through one lens and rotate the lens, or hold one pair of glasses in front of another and rotate it: polaroid lenses darken to almost black at $90^{\circ}$; ordinary tinted glass shows no change in transmitted light.

(c) Only transverse waves can be polarized, so the phenomenon shows that light is a **transverse** wave.

(d) Polaroid sunglasses (cut glare), camera filters, liquid-crystal displays, 3-D cinema glasses, stress analysis of transparent models.

**2.** (a) **Brewster's law:** the tangent of the polarizing angle $i_p$ of a transparent medium is equal to its refractive index: $\tan i_p = \mu$.

(b) 
$$ i_p = \tan^{-1}(1.3) = 52.4^{\circ} $$
(c) At $i_p$, reflected and refracted rays are perpendicular, so $r = 90^{\circ}-i_p = 37.6^{\circ}$. Check: $\sin52.4^{\circ}/\sin37.6^{\circ} = 0.792/0.610 = 1.30$.

**3.** **Brewster's law:** $\tan i_p = \mu$. **Proof:** at the polarizing angle the reflected ray is completely polarized and is perpendicular to the refracted ray, so
$$ i_p+r = 90^{\circ} $$
Snell's law: $\mu = \dfrac{\sin i_p}{\sin r}$. With $r = 90^{\circ}-i_p$, $\sin r = \cos i_p$, so
$$ \mu = \frac{\sin i_p}{\cos i_p} = \tan i_p $$
**Why the rays are perpendicular:** the reflected light is re-radiated by electrons in the glass that are set vibrating by the refracted wave. For the component with its electric vector in the plane of incidence, these electrons vibrate perpendicular to the refracted ray. If the reflected ray were *along* that direction of vibration (which happens exactly when the reflected and refracted rays are perpendicular), no light could be radiated that way, because an oscillating charge does not radiate along its own axis. Only the component vibrating perpendicular to the plane of incidence is reflected, so the reflected light is completely plane polarized.

**4.** (a) **Malus' law:** the intensity of plane-polarized light transmitted by an analyser is $I = I_0\cos^{2}\theta$, where $\theta$ is the angle between the polarization direction of the light and the axis of the analyser.

(b) The first polaroid passes half: $I_1 = I_0/2$. The second, at $60^{\circ}$: 
$$ I_2 = I_1\cos^{2}60^{\circ} = \frac{I_0}{2}\times\frac14 = \frac{I_0}{8} $$
(c) With crossed axes, $\theta = 90^{\circ}$ and $I = 0$: no light gets through.

**5.** (a) Light from a source passes through a tourmaline crystal $T_1$ (the polarizer) and then a second crystal $T_2$ (the analyser), with their axes initially parallel: light emerges from both. When $T_2$ is rotated about the beam, the emergent light dims, becoming zero when the axes are at $90^{\circ}$, and brightens again at $180^{\circ}$. This behaviour is possible only if the vibrations are perpendicular to the direction of travel — if light were longitudinal, rotation about the beam's axis would not matter by symmetry.

(b) Sound in air is **longitudinal**: the particles vibrate along the direction of propagation, so every direction perpendicular to it is equivalent, and there is no plane of vibration that could be selected.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Distinguish unpolarized, plane polarized and partially polarized light. [2] (b) State and prove Brewster's law. [3] (c) Find the polarizing angle for glass of refractive index $1.52$ and the angle of refraction. [2] (d) What is seen on looking at the reflected light through a rotating polaroid? [1] <span class="marks">[8]</span>
2. (a) Explain polarization by a polaroid and state Malus' law. [3] (b) Unpolarized light of intensity $I_0$ passes through a polarizer and then an analyser at $45^{\circ}$; find the emergent intensity. [2] (c) A third polaroid is inserted between two crossed polaroids at $45^{\circ}$ to each; find the transmitted fraction of the original unpolarized intensity. [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Unpolarized** light has vibrations in all directions perpendicular to the ray (ordinary sunlight). **Plane polarized** light has vibrations in one plane only. **Partially polarized** light has a preference for one plane but with some vibrations in other planes (light reflected at any angle other than $i_p$).

(b) See short answer 3: $\tan i_p = \mu$ follows from $i_p+r = 90^{\circ}$ and Snell's law.

(c) 
$$ i_p = \tan^{-1}(1.52) = 56.7^{\circ},\qquad r = 90^{\circ}-56.7^{\circ} = 33.3^{\circ} $$
(d) At $i_p$ the reflected light is completely plane polarized: through the rotating polaroid it goes from bright to extinction twice per full turn.

**2.** (a) A **polaroid** is a sheet containing long molecular chains aligned in one direction (for example iodoquinine sulfate crystals or stretched polyvinyl alcohol doped with iodine); the chains absorb light whose electric vector is along the chain and transmit the component perpendicular to it. Unpolarized light is thus turned into plane polarized light with half the intensity. **Malus' law:** $I = I_0\cos^{2}\theta$ (defined in short answer 4).

(b) After the polarizer, $I_1 = I_0/2$. After the analyser at $45^{\circ}$,
$$ I_2 = \frac{I_0}{2}\cos^{2}45^{\circ} = \frac{I_0}{4} $$
(c) After the first polaroid: $I_0/2$. After the middle polaroid at $45^{\circ}$ to the first: $\frac{I_0}{2}\cos^{2}45^{\circ} = I_0/4$. The third is at $45^{\circ}$ to the second: $\frac{I_0}{4}\cos^{2}45^{\circ} = I_0/8$. The transmitted fraction is $1/8 = 12.5\%$ — whereas with *no* middle polaroid the two crossed polaroids transmit nothing.
:::

::: tip Examiner's note — Polarization
In the proof of Brewster's law, **state the perpendicularity of the reflected and refracted rays** as the starting point: the marks are for this condition, the use of Snell's law and $\sin r = \cos i_p$. For Malus' law, remember the first polaroid always halves *unpolarized* light; only afterwards does $\cos^{2}\theta$ apply. A sketch of the two tourmaline crystals or the reflecting surface with the two perpendicular rays gives the diagram mark.
:::

## 3.14 Electrical circuits

CDC allots **6 teaching hours**. The Wheatstone bridge and meter bridge (2079 model), the potentiometer (2078, 2079 model, 2081, 2082) and the conversion of a galvanometer to an ammeter or voltmeter (2081) make this one of the most reliably examined units in Electricity.

**Short answer questions [5 marks each]**

1. (a) State Kirchhoff's two laws. [2] (b) Using them, derive the balance condition of a Wheatstone bridge. [3] <span class="marks">[5]</span> (NEB 2082)
2. (a) State the principle of the potentiometer and explain why it is called a voltmeter of infinite resistance. [1+1] (b) In a meter bridge the balance point is at $20\ \text{cm}$. The two resistances are doubled and then interchanged; where is the new balance point? [2] (c) If the galvanometer and the battery are interchanged, how is the balance point affected? [1] <span class="marks">[5]</span> (NEB 2079 model)
3. In a meter bridge the null point is at $60.0\ \text{cm}$ from end $A$ with $R$ in the left gap and $S$ in the right. When $5\ \Omega$ is connected in series with $S$, the null point moves to $50.0\ \text{cm}$. Find $R$ and $S$. [5] (NEB 2079 model)
4. (a) Derive the expression for the internal resistance of a cell using a potentiometer. [3] (b) A cell balances at $75\ \text{cm}$ on open circuit and at $60\ \text{cm}$ when a $10\ \Omega$ resistor is connected across it; find its internal resistance. [2] <span class="marks">[5]</span> (NEB 2081)
5. (a) How is a moving-coil galvanometer converted into an ammeter? [2] (b) A galvanometer of resistance $50\ \Omega$ gives full-scale deflection for $5\ \text{mA}$; find the shunt to read $1\ \text{A}$. [3] <span class="marks">[5]</span> (NEB 2081, part)
6. (a) How is a galvanometer converted into a voltmeter? [2] (b) Find the series resistance needed to make a $10\ \text{V}$ voltmeter from a galvanometer of $100\ \Omega$ and $1\ \text{mA}$. [3] <span class="marks">[5]</span>
7. (a) State Joule's law of heating. [1] (b) What are superconductors, and how do they differ from perfect conductors? [2] (c) Describe an ohmmeter briefly. [2] <span class="marks">[5]</span>
8. A standard cell of $1.50\ \text{V}$ is balanced at $37.5\ \text{cm}$ on a potentiometer wire and a test cell at $25.0\ \text{cm}$. (a) Find the e.m.f. of the test cell. [2] (b) Why is the potentiometer more precise than an ordinary voltmeter? [2] (c) Why is the wire made of manganin? [1] <span class="marks">[5]</span> (NEB 2078, part)

::: note Model answers — short (1–4)
**1.** (a) **Junction (current) law:** the algebraic sum of the currents at a junction is zero, $\sum I = 0$ — charge does not accumulate (conservation of charge). **Loop (voltage) law:** the algebraic sum of the e.m.f.s in any closed loop equals the sum of the products $IR$ round it, $\sum\mathcal{E} = \sum IR$, i.e. the net change of potential round a closed loop is zero (conservation of energy).

(b) In the Wheatstone bridge four resistors $P, Q, R, S$ form a quadrilateral $ABCD$ with the battery across $A$–$C$ and the galvanometer across $B$–$D$. At balance the galvanometer current is zero, so the same current $I_1$ flows in $P$ and $Q$, and $I_2$ in $R$ and $S$. The loop law for $ABDA$ (potential of $B$ equals that of $D$) gives
$$ I_1P = I_2R $$
and for $BCDB$
$$ I_1Q = I_2S $$
Dividing,
$$ \frac{P}{Q} = \frac{R}{S} $$

**2.** (a) **Principle:** when a steady current flows through a wire of uniform cross-section, the potential difference between two points is proportional to the length of wire between them. A potentiometer compares or measures voltages by balancing them against this known fall along the wire. **Voltmeter of infinite resistance:** at the balance point no current flows in the cell (or circuit) being measured, so its terminal voltage equals its e.m.f. — unlike a voltmeter, which draws some current and reads less than the e.m.f.

(b) At balance $\dfrac{R}{X} = \dfrac{l}{100-l} = \dfrac{20}{80} = \dfrac14$. Doubling both keeps the ratio $\tfrac14$, so the balance point does not move. Interchanging them inverts the ratio:
$$ \frac{l'}{100-l'} = 4\ \Rightarrow\ l' = 80\ \text{cm} $$
(c) The balance point is **unaffected**: the Wheatstone bridge condition $P/Q = R/S$ is symmetric with respect to the battery and galvanometer positions. (It is more sensitive with the more convenient arrangement, but the null point is the same.)

**3.** Let the ratio of resistances be in proportion to the wire lengths: $R/S = l/(100-l)$.
$$ \frac{R}{S} = \frac{60}{40} = 1.5\ \Rightarrow\ R = 1.5S $$
After adding $5\ \Omega$ to $S$:
$$ \frac{R}{S+5} = \frac{50}{50} = 1\ \Rightarrow\ R = S+5 $$
Equating, $1.5S = S+5$, so $S = 10\ \Omega$ and $R = 15\ \Omega$.

**4.** (a) A cell of e.m.f. $E$ and internal resistance $r$ is balanced on the potentiometer wire: on open circuit at length $l_1$, so $E = kl_1$ ($k$ is the potential gradient). Then a resistance $R$ is connected across the cell. A current $I = E/(R+r)$ flows and the terminal voltage $V = IR$ balances at length $l_2$: $V = kl_2$. Dividing,
$$ \frac{E}{V} = \frac{l_1}{l_2} = \frac{R+r}{R} $$
$$ r = R\left(\frac{l_1-l_2}{l_2}\right) $$
(b) 
$$ r = 10\times\frac{75-60}{60} = 2.5\ \Omega $$

:::

::: note Model answers — short (5–8)
**5.** (a) A low-resistance **shunt** $S$ is connected in **parallel** with the galvanometer. Most of the current bypasses the coil and only the fraction it can stand flows through it; the scale is recalibrated. The combined resistance is very small, so the ammeter disturbs the circuit very little.

(b) The galvanometer carries $I_g = 5\ \text{mA}$ and the shunt $I-I_g = 1-0.005 = 0.995\ \text{A}$ at the same potential difference:
$$ I_gG = (I-I_g)S\ \Rightarrow\ S = \frac{I_gG}{I-I_g} = \frac{0.005\times50}{0.995} = 0.25\ \Omega $$

**6.** (a) A high resistance $R$ is connected in **series** with the galvanometer. The current stays within $I_g$ up to the maximum voltage $V$, and the scale is calibrated in volts. The high resistance means the voltmeter draws little current from the circuit.

(b) 
$$ V = I_g(G+R)\ \Rightarrow\ R = \frac{V}{I_g}-G = \frac{10}{1.0\times10^{-3}}-100 = 9900\ \Omega $$

**7.** (a) **Joule's law:** the heat produced in a conductor in time $t$ is $H = I^{2}Rt$ — proportional to the square of the current, to the resistance and to the time.

(b) A **superconductor** is a material whose resistance drops to exactly zero below a critical temperature $T_c$ (for example mercury at $4.2\ \text{K}$). Unlike a *perfect conductor* (only zero resistance), it also expels magnetic field from its interior, the Meissner effect, and this persists if the field is applied before or after cooling. Uses: powerful electromagnets in MRI, maglev trains, lossless transmission.

(c) An **ohmmeter** has a galvanometer in series with a cell and a variable resistor. With the terminals shorted the galvanometer gives full-scale deflection (marked $0\ \Omega$) after adjusting the resistor; with the terminals open there is no deflection ($\infty$). An unknown resistance joined between the terminals reduces the current in proportion, so the scale can be marked in ohms; it is non-linear and crowded at the high end.

**8.** (a) $E_1/E_2 = l_1/l_2$, so
$$ E_2 = E_1\frac{l_2}{l_1} = 1.50\times\frac{25.0}{37.5} = 1.00\ \text{V} $$
(b) At the balance point **no current** is drawn from the cell, so the reading is the true e.m.f. and is independent of the cell's internal resistance; a voltmeter draws current and reads less. The reading is obtained as a ratio of *lengths*, which can be measured very precisely, and needs no calibrated meter scale.

(c) Manganin has a **high resistivity** (so a long, thin wire fits in a short length) and a **very small temperature coefficient of resistance**, so the potential gradient stays steady as the wire warms.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Describe the meter bridge and derive the expression for an unknown resistance. [4] (b) Why is it best to have the balance point near the middle? [1] (c) A $4.0\ \Omega$ resistor is in the left gap and the null point is at $40.0\ \text{cm}$; find the unknown resistance in the right gap, and the new null point if the two resistors are interchanged. [3] <span class="marks">[8]</span>
2. (a) Explain with a circuit diagram how a potentiometer is used to compare the e.m.f.s of two cells. [4] (b) Derive the ratio. [2] (c) A potentiometer wire $10\ \text{m}$ long carries a steady $0.20\ \text{A}$ and has resistance $20\ \Omega$; what is the potential gradient? [2] <span class="marks">[8]</span>
3. (a) Explain how a moving-coil galvanometer is converted into (i) an ammeter and (ii) a voltmeter. [4] (b) A galvanometer of $30\ \Omega$ gives full-scale deflection at $10\ \text{mA}$. Find the shunt for a $0$–$3\ \text{A}$ range and the series resistor for a $0$–$30\ \text{V}$ range. [4] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) The **meter bridge** is a practical Wheatstone bridge: a uniform wire $AC$ of length $100\ \text{cm}$ is stretched along a metre scale, with a known resistance $R$ in the left gap and the unknown $X$ in the right gap of a copper strip; a battery is across $AC$ and a galvanometer connected between the junction $B$ of $R$ and $X$ and a sliding jockey $J$ on the wire. The jockey is moved until the galvanometer shows no deflection, at distance $l$ from $A$. The resistances of the wire lengths are proportional to lengths, so
$$ \frac{R}{X} = \frac{l}{100-l}\ \Rightarrow\ X = R\,\frac{100-l}{l} $$
(b) Near the middle the bridge is most sensitive and the percentage error in $(100-l)/l$ from a fixed error in reading $l$ is smallest.

(c) $X = 4.0\times\dfrac{100-40}{40} = 6.0\ \Omega$. After interchanging, the left gap holds $6.0\ \Omega$ and the right $4.0\ \Omega$:
$$ \frac{l'}{100-l'} = \frac{6.0}{4.0} = 1.5\ \Rightarrow\ l' = 60\ \text{cm} $$

**2.** (a) A potentiometer wire $AB$ of uniform cross-section is connected in series with a driver cell (steady current) and a key. The positive terminals of the two cells $E_1, E_2$ are joined to $A$; their negative terminals go through a galvanometer and a two-way switch to a sliding jockey $J$ (circuit in the figure below). With $E_1$ connected, slide $J$ until the galvanometer shows zero deflection; note the length $l_1$. Repeat with $E_2$ to get $l_2$.

(b) With potential gradient $k$ (volts per unit length) along the wire,
$$ E_1 = kl_1,\qquad E_2 = kl_2\ \Rightarrow\ \frac{E_1}{E_2} = \frac{l_1}{l_2} $$
The driver e.m.f. must exceed both cell e.m.f.s and the current must stay constant.

(c) The potential difference across the wire is $V = IR = 0.20\times20 = 4.0\ \text{V}$; the gradient is
$$ k = \frac{V}{L} = \frac{4.0}{10} = 0.40\ \text{V m}^{-1} $$

**3.** (a) (i) **Ammeter:** a small shunt resistance $S$ in parallel with the galvanometer of resistance $G$ diverts the excess current, so that only $I_g$ goes through the coil when the total current is $I$: $S = I_gG/(I-I_g)$. The resulting resistance $GS/(G+S)$ is smaller than $S$. (ii) **Voltmeter:** a large resistance $R$ in series limits the current to $I_g$ at the full-scale voltage $V$: $R = V/I_g-G$. The resulting resistance $G+R$ is very large.

(b) Shunt: $S = \dfrac{I_gG}{I-I_g} = \dfrac{0.010\times30}{3.0-0.010} = 0.10\ \Omega$. Series resistor: $R = \dfrac{V}{I_g}-G = \dfrac{30}{0.010}-30 = 2970\ \Omega$.
:::

```figure caption="Potentiometer circuit for comparing e.m.f.s. The driver cell sends a steady current through wire AB. Cell E₁ or E₂ (chosen by a two-way switch, shown as one cell) is joined, through the galvanometer G, to the jockey J, which is slid along AB until G reads zero."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis('off')
ax.plot([1.0, 9.0], [3.9, 3.9], color=INK, lw=3.2)
ax.text(0.85, 4.05, 'A', fontsize=9, ha='right', va='bottom', color=INK)
ax.text(9.15, 4.05, 'B', fontsize=9, ha='left', va='bottom', color=INK)
ax.plot([1.0, 1.0, 4.3], [3.9, 5.5, 5.5], color=INK, lw=1.2)
ax.plot([5.0, 9.0, 9.0], [5.5, 5.5, 3.9], color=INK, lw=1.2)
ax.plot([4.3, 4.3], [5.25, 5.75], color=INK, lw=2.4)
ax.plot([5.0, 5.0], [5.38, 5.62], color=INK, lw=1.2)
ax.text(4.65, 5.95, 'driver cell', fontsize=8, ha='center', color=MUTED)
ax.plot([1.0, 1.0, 2.6], [3.9, 1.3, 1.3], color=INK, lw=1.2)
ax.plot([3.2, 5.3], [1.3, 1.3], color=INK, lw=1.2)
ax.plot([2.6, 2.6], [1.05, 1.55], color=INK, lw=2.4)
ax.plot([3.2, 3.2], [1.18, 1.42], color=INK, lw=1.2)
ax.text(2.9, 0.55, '$E_1$ or $E_2$', fontsize=8.5, ha='center', color=INK)
ax.add_patch(Circle((5.7, 1.3), 0.4, fc='white', ec=INK, lw=1.3))
ax.text(5.7, 1.3, 'G', fontsize=9, ha='center', va='center', color=INK)
ax.plot([6.1, 7.3, 7.3], [1.3, 1.3, 3.0], color=INK, lw=1.2)
ax.annotate('', xy=(7.3, 3.85), xytext=(7.3, 3.0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0))
ax.text(7.5, 3.3, 'J', fontsize=9, color=INK)
```

::: tip Examiner's note — Electrical circuits
For the Wheatstone bridge, **apply the loop law to two loops** and divide: that is the proof the examiner wants, not a quoted formula. In meter-bridge numericals, always write $X = R(100-l)/l$ with **$l$ measured from the end where $R$ is**. For a potentiometer the two marks are "no current at balance" and "ratio of lengths". In the conversion of a galvanometer, remember the ammeter *shunt is in parallel and small*, the voltmeter *resistor is in series and large*; and always state the full-scale current $I_g$ being used.
:::

## 3.15 Thermoelectric effects

CDC allots **3 teaching hours**. The neutral and inversion temperatures are examined in a Group A item nearly every year, and a full Group B question (2080) and a Group C alternative (2082) have asked for the $e$–$\theta$ graph.

**Short answer questions [5 marks each]**

1. (a) What is the thermoelectric effect? [1] (b) Define neutral temperature and inversion temperature. [2] (c) What happens to the inversion temperature if the cold junction is moved from $0\ ^{\circ}\text{C}$ to $-10\ ^{\circ}\text{C}$? [1] (d) Give one application of a thermocouple. [1] <span class="marks">[5]</span> (NEB 2080)
2. (a) Sketch and explain the variation of thermo-e.m.f. with the temperature of the hot junction. [3] (b) Write the empirical equation and deduce the neutral temperature. [2] <span class="marks">[5]</span> (NEB 2082, part)
3. A thermocouple has a neutral temperature of $500\ ^{\circ}\text{C}$ with its cold junction at $0\ ^{\circ}\text{C}$. By what percentage does the inversion temperature change when the cold junction is raised to $20\ ^{\circ}\text{C}$? [5] <span class="marks">[5]</span> (NEB 2079 model)
4. A thermocouple has an inversion temperature of $600\ ^{\circ}\text{C}$ and a neutral temperature of $310\ ^{\circ}\text{C}$. (a) Find the temperature of the cold junction. [2] (b) What is the temperature of the cold junction if the neutral temperature is $320\ ^{\circ}\text{C}$ for the same inversion temperature? [1] (c) Explain why the neutral temperature is independent of the cold junction. [2] <span class="marks">[5]</span> (NEB 2081, 2082 model)
5. (a) Explain the Peltier effect. [2] (b) How does it differ from Joule heating? [2] (c) Name one use. [1] <span class="marks">[5]</span>
6. (a) What is a thermopile? [2] (b) Why is it more sensitive than a single thermocouple? [1] (c) For $e = 16\theta-0.04\theta^{2}\ \mu\text{V}$ find the neutral temperature and the maximum e.m.f. [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) The **thermoelectric (Seebeck) effect:** when the two junctions of a closed circuit of two different metals are kept at different temperatures, an e.m.f. (and a current) appears in the circuit.

(b) The **neutral temperature** $\theta_n$ is the temperature of the hot junction at which the thermo-e.m.f. is a maximum (the graph of $e$ against $\theta$ has zero slope there). The **inversion temperature** $\theta_i$ is the hot-junction temperature at which the thermo-e.m.f. falls back to zero and then reverses.

(c) $\theta_i = 2\theta_n-\theta_c$, and $\theta_n$ is fixed. Lowering $\theta_c$ by $10\ ^{\circ}\text{C}$ **raises $\theta_i$ by $10\ ^{\circ}\text{C}$**.

(d) Measuring temperatures (a thermocouple thermometer in furnaces, engines and laboratories), or detecting radiation in a thermopile; also thermoelectric generators.

**2.** (a) With the cold junction at $0\ ^{\circ}\text{C}$, the thermo-e.m.f. first rises as the hot-junction temperature rises, reaches a **maximum** at $\theta_n$, then falls, reaching zero at $\theta_i$ and reversing beyond it. The curve is a **parabola** with its peak at $\theta_n$ and intercept at $\theta_i = 2\theta_n$ (figure below).

(b) $e = a\theta+\tfrac12b\theta^{2}$ ($a>0$, $b<0$). At the maximum $de/d\theta = 0$: $a+b\theta_n = 0$, so
$$ \theta_n = -\frac{a}{b} $$
and $e = 0$ again at $\theta_i = -2a/b = 2\theta_n$ (for $\theta_c = 0$).

**3.** With $\theta_c = 0$: $\theta_i = 2\theta_n-0 = 1000\ ^{\circ}\text{C}$. With $\theta_c = 20\ ^{\circ}\text{C}$, $\theta_n$ is unchanged: $\theta_i' = 2(500)-20 = 980\ ^{\circ}\text{C}$.
$$ \text{change} = \frac{1000-980}{1000}\times100 = 2\% $$
(a decrease of $2\%$).

**4.** (a) $\theta_i = 2\theta_n-\theta_c$ so
$$ \theta_c = 2\theta_n-\theta_i = 2(310)-600 = 20\ ^{\circ}\text{C} $$
(b) $\theta_c = 2(320)-600 = 40\ ^{\circ}\text{C}$.

(c) The e.m.f. for a pair of metals is a function $e = a(\theta_h-\theta_c)+\tfrac12b(\theta_h^{2}-\theta_c^{2})$. Its maximum with respect to $\theta_h$ is where $a+b\theta_h = 0$ — which does not contain $\theta_c$. Changing the cold junction changes the *size* of the e.m.f. but not the hot-junction temperature at which it peaks.

**5.** (a) The **Peltier effect:** when a current flows across a junction of two different metals, heat is absorbed at the junction for one direction of the current and evolved for the other; this is because the electrons carry different energy in the two metals.

(b) Joule heating $I^{2}R$ is **irreversible** (the heat is always evolved) and proportional to $I^{2}$; the Peltier heat is proportional to $I$ and **reversible**: reversing the current turns the heating at a junction into cooling.

(c) Small thermoelectric coolers for portable refrigerators and for cooling electronic detectors.

**6.** (a) A **thermopile** is a number of thermocouples connected in series, with all the "hot" junctions on one face and all the "cold" junctions on another; it is used to detect and measure radiant heat.

(b) The e.m.f.s of the individual junction pairs add, so a given small rise of temperature gives several times the e.m.f. of a single couple, increasing sensitivity.

(c) $de/d\theta = 16-0.08\theta = 0$ gives $\theta_n = 200\ ^{\circ}\text{C}$, and
$$ e_{max} = 16(200)-0.04(200)^{2} = 3200-1600 = 1600\ \mu\text{V} $$
The inversion temperature is $400\ ^{\circ}\text{C}$.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Describe the Seebeck effect with a labelled diagram and name the factors on which the thermo-e.m.f. depends. [3] (b) Explain the graph of thermo-e.m.f. against hot-junction temperature and define $\theta_n$ and $\theta_i$. [3] (c) For a copper–iron couple the neutral temperature is $270\ ^{\circ}\text{C}$; find the inversion temperature when the cold junction is at $15\ ^{\circ}\text{C}$. [2] <span class="marks">[8]</span>
2. (a) Explain the Peltier effect and show that Peltier heat is reversible. [3] (b) Describe how a thermopile works and one use. [3] (c) A thermocouple has $e = 12\theta-0.03\theta^{2}\ \mu\text{V}$ ($\theta$ in $^{\circ}\text{C}$, cold junction at $0\ ^{\circ}\text{C}$). Find $\theta_n$, $\theta_i$ and the e.m.f. at $100\ ^{\circ}\text{C}$. [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) Two different metals, say copper and iron, are joined at two junctions to form a closed loop; one junction (hot) is kept at a higher temperature $\theta_h$ than the other (cold) $\theta_c$. A galvanometer in the circuit shows a current. The e.m.f. depends on (i) the **pair of metals** (their positions in the thermoelectric series — the farther apart, the larger the e.m.f.), (ii) the **temperatures of the two junctions**, and to first order on their difference.

(b) With $\theta_c = 0\ ^{\circ}\text{C}$, raising $\theta_h$ increases $e$ roughly linearly at first; the rise slows, $e$ reaches a maximum at the neutral temperature $\theta_n$, then decreases, reaching zero at $\theta_i$, and reverses in sign above it. The parabola $e = a\theta+\tfrac12b\theta^{2}$ is symmetric about $\theta_n$. $\theta_n$ depends only on the metals; $\theta_i = 2\theta_n-\theta_c$ depends on $\theta_c$ too.

(c) $\theta_i = 2(270)-15 = 525\ ^{\circ}\text{C}$.

**2.** (a) See short answer 5. When current $I$ passes through a junction, the heat $\Pi I$ per second is absorbed or evolved, where $\Pi$ is the Peltier coefficient of the pair. Reversing $I$ changes the sign of $\Pi I$: heat absorbed becomes heat evolved. By contrast $I^{2}R$ does not change sign.

(b) See short answer 6(a). When radiation falls on the blackened hot junctions, they warm relative to the cold junctions; the summed e.m.f. is measured with a galvanometer and is proportional to the radiation received. Used to measure the intensity of infrared and heat radiation, e.g. in radiometers and some infrared thermometers.

(c) $\theta_n = -a/b = 12/0.06 = 200\ ^{\circ}\text{C}$ (from $12-0.06\theta = 0$), $\theta_i = 400\ ^{\circ}\text{C}$, and
$$ e(100) = 12(100)-0.03(100)^{2} = 1200-300 = 900\ \mu\text{V} $$
:::

```figure caption="Thermo-e.m.f. of a thermocouple against the hot-junction temperature (cold junction at 0 °C). The e.m.f. peaks at the neutral temperature θn and falls to zero again at the inversion temperature θi = 2θn."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.8))
th = np.linspace(0, 440, 300)
e = 16*th - 0.04*th**2
ax.plot(th, e, color=ACCENT, lw=1.9)
ax.axhline(0, color=INK, lw=0.9)
ax.plot([200, 200], [0, 1600], color=MUTED, lw=1.0, ls='--')
ax.plot([200], [1600], 'o', color=INK, ms=4)
ax.annotate('maximum e.m.f.', (200, 1600), xytext=(215, 1560), fontsize=8.5, color=INK, va='center')
ax.text(200, -330, '$\\theta_n$', ha='center', fontsize=9.5, color=INK)
ax.text(400, -330, '$\\theta_i$', ha='center', fontsize=9.5, color=INK)
ax.plot([400], [0], 'o', color=INK, ms=4)
ax.set_xlabel('hot-junction temperature  $\\theta$ (°C)', fontsize=9)
ax.set_ylabel('thermo-e.m.f.  $e$ (μV)', fontsize=9)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(0, 450); ax.set_ylim(-520, 1900)
ax.spines[['top','right']].set_visible(False)
```

::: tip Examiner's note — Thermoelectric effects
Do not define the neutral temperature as "the temperature at which the e.m.f. is zero" — that is the **inversion** temperature. The two formulae to have ready are $\theta_n = -a/b$ and $\theta_i = 2\theta_n-\theta_c$; nearly every numerical uses the second. Draw the parabola with the maximum at $\theta_n$ and the zero crossing at $\theta_i$. For the cold-junction question say explicitly that *only the inversion temperature shifts*.
:::

## 3.16 Magnetic field

CDC allots **9 teaching hours** — the largest unit in Electricity and Magnetism. Biot–Savart and Ampère's law, the galvanometer, the Hall effect and the force between parallel currents account for a Group B or Group C question in every paper (2078, 2079 model, 2080, 2081, 2082).

**Short answer questions [5 marks each]**

1. (a) State the Biot–Savart law. [1] (b) Derive the magnetic field at the centre of a circular current-carrying coil. [3] (c) State the direction rule. [1] <span class="marks">[5]</span> (NEB 2080)
2. (a) Use Ampère's circuital law to find the magnetic field at a distance $r$ from a long straight conductor carrying current $I$. [3] (b) A wire $0.5\ \text{m}$ long carries $2\ \text{A}$ in a field of $0.4\ \text{T}$; find the maximum and minimum force on it. [2] <span class="marks">[5]</span> (NEB 2081)
3. (a) Define the voltage sensitivity of a moving-coil galvanometer and state the factors on which it depends. [2] (b) Why is a radial magnetic field used? [1] (c) Coil data: $N = 100$, $A = 4.0\times10^{-4}\ \text{m}^{2}$, $B = 0.25\ \text{T}$, torsional constant $5.0\times10^{-5}\ \text{N m rad}^{-1}$, resistance $50\ \Omega$. Find the current and voltage sensitivity. [2] <span class="marks">[5]</span> (NEB 2081, part)
4. (a) Explain the Hall effect. [2] (b) An indium antimonide slice of thickness $2.5\ \text{mm}$ carries $150\ \text{mA}$ in a field of $0.5\ \text{T}$ and the Hall voltage is $8.75\ \text{mV}$. Find the carrier density. [3] <span class="marks">[5]</span> (NEB 2081)
5. (a) Derive the force per unit length between two long parallel conductors. [3] (b) Define the ampere. [2] <span class="marks">[5]</span> (NEB 2081, 2079 model)
6. (a) Find the force on a charge moving in a magnetic field and show the path is a circle. [3] (b) A proton of speed $2.0\times10^{6}\ \text{m s}^{-1}$ moves perpendicular to a field of $0.50\ \text{T}$; find the radius ($m = 1.67\times10^{-27}\ \text{kg}$). [2] <span class="marks">[5]</span>
7. (a) Use Ampère's law to find the field inside a long solenoid and a toroid. [3] (b) A solenoid has $2000$ turns per metre and carries $5.0\ \text{A}$; find $B$ inside. [2] <span class="marks">[5]</span>
8. (a) What is meant by magnetic field lines and magnetic flux? [2] (b) Describe Oersted's experiment and what it showed. [2] (c) Why do the field lines never cross? [1] <span class="marks">[5]</span>

::: note Model answers — short (1–4)
**1.** (a) The **Biot–Savart law:** the magnetic field $d\vec B$ due to a current element $I\,d\vec l$ at a point with position vector $\vec r$ from the element is
$$ dB = \frac{\mu_0}{4\pi}\,\frac{I\,dl\,\sin\theta}{r^{2}} $$
where $\theta$ is the angle between $d\vec l$ and $\vec r$; its direction is perpendicular to both $d\vec l$ and $\vec r$.

(b) Take a coil of $N$ turns and radius $R$, carrying $I$. Every element $dl$ of the circle is perpendicular to the line $\vec r$ to the centre, so $\theta = 90^{\circ}$, $\sin\theta = 1$ and $r = R$, and all the $d\vec B$ at the centre point the same way (along the axis). Adding,
$$ B = \sum dB = \frac{\mu_0}{4\pi}\,\frac{I}{R^{2}}\sum dl = \frac{\mu_0}{4\pi}\,\frac{I}{R^{2}}\,(2\pi R) $$
$$ B = \frac{\mu_0I}{2R}\qquad\text{for one turn},\qquad B = \frac{\mu_0NI}{2R}\ \text{for }N\text{ turns} $$
(c) **Right-hand rule:** curl the fingers of the right hand in the direction of the current in the coil; the thumb points along $\vec B$ at the centre.

**2.** (a) Draw a circle of radius $r$ around the wire, with the wire at its centre and perpendicular to its plane. By symmetry $B$ is tangential and constant in magnitude round the circle. **Ampère's circuital law:** $\oint\vec B\cdot d\vec l = \mu_0I_{enclosed}$.
$$ B(2\pi r) = \mu_0I\ \Rightarrow\ B = \frac{\mu_0I}{2\pi r} $$
(b) $F = BIl\sin\theta$. Maximum at $\theta = 90^{\circ}$: $F = 0.4\times2\times0.5 = 0.40\ \text{N}$. Minimum at $\theta = 0^{\circ}$ (wire along the field): $F = 0$.

**3.** (a) **Voltage sensitivity** is the deflection produced per unit voltage across the galvanometer: $\dfrac{\phi}{V} = \dfrac{NBA}{CR}$; it depends on the number of turns $N$, the field $B$, the coil area $A$, the torsional constant $C$ (smaller is more sensitive) and the coil resistance $R$. Current sensitivity is $\phi/I = NBA/C$.

(b) A **radial field** (concave pole pieces with a soft-iron core) keeps the plane of the coil always parallel to $\vec B$, so the deflecting torque $NIAB$ is the same at every angle and the deflection is proportional to the current — a **linear scale**.

(c) 
$$ \frac{\phi}{I} = \frac{NBA}{C} = \frac{100\times0.25\times4.0\times10^{-4}}{5.0\times10^{-5}} = 200\ \text{rad A}^{-1} = 0.20\ \text{rad mA}^{-1} $$
$$ \frac{\phi}{V} = \frac{\phi/I}{R} = \frac{200}{50} = 4.0\ \text{rad V}^{-1} $$

**4.** (a) When a current-carrying conductor is placed in a magnetic field perpendicular to the current, the moving charge carriers are pushed sideways by the force $qvB$. Charge accumulates on one face, and a transverse electric field (Hall field) builds up until its force balances the magnetic force. The resulting transverse potential difference is the **Hall voltage** $V_H$. Its sign tells whether the carriers are electrons or holes.

(b) At balance $eE_H = evB$ and $V_H = E_Hw$; with $I = nevwt$ (where $w$ is the width and $t$ the thickness in the direction of $\vec B$), $V_H = \dfrac{BI}{net}$:
$$ n = \frac{BI}{eV_Ht} = \frac{0.5\times0.150}{1.6\times10^{-19}\times8.75\times10^{-3}\times2.5\times10^{-3}} = 2.1\times10^{22}\ \text{m}^{-3} $$
:::

::: note Model answers — short (5–8)
**5.** (a) Two long parallel wires a distance $r$ apart carry currents $I_1$ and $I_2$ in the same direction. Wire 1 produces at wire 2 a field
$$ B_1 = \frac{\mu_0I_1}{2\pi r} $$
directed perpendicular to the plane of the wires. Wire 2 (length $l$) carries $I_2$ perpendicular to this field, so the force on it is $F = B_1I_2l$:
$$ \frac{F}{l} = \frac{\mu_0I_1I_2}{2\pi r} $$
For currents in the same direction the force is **attractive**; for opposite currents, repulsive.

(b) The **ampere** is that constant current which, if maintained in two straight parallel conductors of infinite length and negligible cross-section, placed one metre apart in vacuum, produces between them a force of $2\times10^{-7}\ \text{newton per metre}$ of length. (From $\mu_0/2\pi = 2\times10^{-7}\ \text{N A}^{-2}$ with $I_1 = I_2 = 1\ \text{A}$, $r = 1\ \text{m}$.)

**6.** (a) A charge $q$ with velocity $\vec v$ in a field $\vec B$ experiences $\vec F = q\vec v\times\vec B$, of magnitude $qvB\sin\theta$ and perpendicular to both $\vec v$ and $\vec B$. For $\vec v\perp\vec B$ the force is always perpendicular to the velocity: it changes the direction of motion but not the speed, and provides the centripetal force:
$$ qvB = \frac{mv^{2}}{r}\ \Rightarrow\ r = \frac{mv}{qB} $$
a constant radius: the path is a circle.

(b) 
$$ r = \frac{mv}{qB} = \frac{1.67\times10^{-27}\times2.0\times10^{6}}{1.6\times10^{-19}\times0.50} = 4.2\times10^{-2}\ \text{m} $$

**7.** (a) *Solenoid:* take a rectangular Amperian loop with one side of length $l$ inside the solenoid and parallel to its axis, the other outside where $B\approx0$. The enclosed current is $nlI$ (with $n$ turns per metre), and $\oint\vec B\cdot d\vec l = Bl$, so
$$ B = \mu_0nI $$
*Toroid:* a circle of radius $r$ inside the ring encloses $N$ turns, each carrying $I$; with $B$ tangential and constant,
$$ B(2\pi r) = \mu_0NI\ \Rightarrow\ B = \frac{\mu_0NI}{2\pi r} $$
Outside the toroid the enclosed current is zero, so $B = 0$.

(b) 
$$ B = \mu_0nI = 4\pi\times10^{-7}\times2000\times5.0 = 1.3\times10^{-2}\ \text{T} $$
**8.** (a) A **magnetic field line** is a curve whose tangent at every point gives the direction of $\vec B$, and whose density shows its strength. **Magnetic flux** through a surface is $\Phi = BA\cos\theta$, the number of lines crossing it, in weber.

(b) **Oersted's experiment (1820):** a compass needle held parallel to a straight wire deflects when a current is passed and reverses when the current is reversed. It showed that an electric current produces a magnetic field circulating round the wire — the first link between electricity and magnetism.

(c) At every point $\vec B$ has a single direction, so a field line has a single tangent there; two lines crossing would give two directions at one point.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) State the Biot–Savart law and use it to find the magnetic field at the centre of a circular coil. [3] (b) A thin slice of indium antimonide, thickness $2.5\ \text{mm}$, carries $150\ \text{mA}$ in a field of $0.5\ \text{T}$ with Hall voltage $8.75\ \text{mV}$; find the carrier density. [2] (c) Derive the force per unit length between two parallel conductors and define the ampere. [3] <span class="marks">[8]</span> (NEB 2081)
2. (a) Derive the torque on a rectangular current-carrying coil in a uniform magnetic field. [3] (b) Describe the construction and working of a moving-coil galvanometer. [3] (c) A coil of $50$ turns, $3.0\ \text{cm}\times4.0\ \text{cm}$, carries $0.20\ \text{A}$ in a field of $0.80\ \text{T}$ at $30^{\circ}$ between the normal and the field; find the torque. [2] <span class="marks">[8]</span>
3. (a) Define one ampere in terms of the force between two parallel conductors. [1] (b) Explain why a solenoid contracts when a current passes through it. [2] (c) A conductor of linear mass density $0.2\ \text{g m}^{-1}$ hangs horizontally between two flexible wires in a horizontal magnetic field of $1\ \text{T}$ at right angles to it. The tension in the wires is zero; find the current [3], and then the torque on a $100$-turn coil of area $100\ \text{cm}^{2}$ carrying this current with its plane parallel to a field of $10\ \text{T}$. [2] <span class="marks">[8]</span> (NEB 2079 model)

::: note Model answers — long
**1.** (a) The Biot–Savart law and the derivation of $B = \mu_0NI/2R$ are given in short answer 1.

(b) $n = 2.1\times10^{22}\ \text{m}^{-3}$ as in short answer 4(b).

(c) As in short answer 5: $F/l = \mu_0I_1I_2/2\pi r$, attractive for parallel currents; the ampere is defined through $F/l = 2\times10^{-7}\ \text{N m}^{-1}$ for $1\ \text{A}$ at $1\ \text{m}$.

**2.** (a) Let a rectangular coil of sides $a$ (vertical) and $b$ (horizontal) carry $I$ in a uniform field $\vec B$, with the normal making an angle $\theta$ with $\vec B$. The forces on the two vertical sides are equal and opposite, $F = BIa$ each, forming a couple with arm $b\sin\theta$. The forces on the horizontal sides are equal, opposite and collinear, so they do not produce torque. The torque is
$$ \tau = F\,b\sin\theta = BIab\sin\theta = BIA\sin\theta $$
and for $N$ turns
$$ \tau = NBIA\sin\theta = mB\sin\theta,\qquad m = NIA $$
where $m$ is the magnetic moment of the coil.

(b) **Moving-coil galvanometer:** a rectangular coil of many turns on a soft-iron core is suspended between the concave poles of a permanent magnet by a phosphor-bronze strip, which supplies the restoring torque $C\phi$. The field is radial. A current $I$ gives a torque $NBAI$ and the coil turns through $\phi$ until $NBAI = C\phi$:
$$ \phi = \frac{NBA}{C}\,I\propto I $$
The deflection, read by a lamp-and-scale or pointer, is proportional to the current.

(c) 
$$ A = 0.030\times0.040 = 1.2\times10^{-3}\ \text{m}^{2} $$
$$ \tau = NBIA\sin\theta = 50\times0.80\times0.20\times1.2\times10^{-3}\times\sin30^{\circ} = 4.8\times10^{-3}\ \text{N m} $$
Here $\theta$ is the angle between the normal to the coil and the field, as in the derivation.

**3.** (a) One **ampere** is the constant current which, flowing in each of two infinitely long straight parallel conductors one metre apart in vacuum, produces a force of $2\times10^{-7}\ \text{N}$ per metre of length between them.

(b) Adjacent turns of the solenoid carry current in the **same direction**, so, like parallel currents, they attract one another. The mutual attraction of all the turns compresses the coil along its axis, and the solenoid contracts (it would return to its length when the current is stopped).

(c) With zero tension in the supporting wires the upward magnetic force on the conductor just balances its weight. For a length $l$ of conductor with linear density $\mu = 0.2\ \text{g m}^{-1} = 2.0\times10^{-4}\ \text{kg m}^{-1}$:
$$ BIl = \mu lg\ \Rightarrow\ I = \frac{\mu g}{B} = \frac{2.0\times10^{-4}\times9.8}{1} = 1.96\times10^{-3}\ \text{A}\approx2.0\ \text{mA} $$
For the coil, with its plane *parallel* to the field the normal is perpendicular to $\vec B$, so $\sin\theta = 1$ and the torque is maximum:
$$ \tau = NBIA = 100\times10\times1.96\times10^{-3}\times1.0\times10^{-2} = 1.96\times10^{-2}\ \text{N m} $$
(with $A = 100\ \text{cm}^{2} = 1.0\times10^{-2}\ \text{m}^{2}$).
:::

::: tip Examiner's note — Magnetic field
For Biot–Savart derivations, say why $\sin\theta = 1$ (every element is perpendicular to the radius) and why the contributions add (all along the axis). For Ampère's law, **name the Amperian loop** and use symmetry to pull $B$ outside the integral. Distinguish $B$ at the centre of a coil ($\mu_0NI/2R$) from $B$ of a straight wire ($\mu_0I/2\pi r$) — the most common slip. In torque numericals, check whether the angle given is between the *field and the normal* (use $\sin\theta$) or between the *field and the plane* (use $\cos$). Convert $\text{cm}^{2}$ to $\text{m}^{2}$ before multiplying.
:::

## 3.17 Magnetic properties of materials

CDC allots **5 teaching hours**. It supplies a very predictable Group B question:
define $\mu_r$, $\chi_m$ and their relation, compare dia-, para- and ferromagnetic
materials in a table, and explain the hysteresis loop and the choice of material
for a transformer core or a permanent magnet.

**Short answer questions [5 marks each]**

1. (a) Define magnetic permeability, relative permeability and magnetic susceptibility. [3] (b) Show that $\mu_r = 1+\chi_m$. [2] <span class="marks">[5]</span> (NEB 2080)
2. (a) Distinguish between diamagnetic, paramagnetic and ferromagnetic materials in a table, with one example of each. [4] (b) Which of them is repelled by a magnet? [1] <span class="marks">[5]</span> (NEB 2082)
3. (a) What is hysteresis? Draw a labelled hysteresis loop. [3] (b) Define retentivity and coercivity from the loop. [2] <span class="marks">[5]</span> (NEB 2081)
4. (a) Explain why the area of the hysteresis loop represents energy lost per cycle per unit volume. [3] (b) State which material you would use for (i) a transformer core and (ii) a permanent magnet, giving a reason for each. [2] <span class="marks">[5]</span> (NEB 2079 model)
5. (a) Define magnetising field $H$, magnetisation $I$ and flux density $B$, and write the relation connecting them. [3] (b) A material of relative permeability $500$ is placed in a magnetising field of $2000\ \text{A m}^{-1}$; find $B$ and $\chi_m$. [2] <span class="marks">[5]</span>
6. (a) Explain the domain theory of ferromagnetism. [3] (b) What is the Curie temperature and what happens above it? [2] <span class="marks">[5]</span>
7. (a) Why is soft iron used for electromagnets and steel for permanent magnets? [3] (b) Why is the core of a transformer laminated? [2] <span class="marks">[5]</span>
8. (a) Define magnetic flux and state Gauss's law for magnetism. [3] (b) Why do magnetic field lines always form closed loops, unlike electric field lines? [2] <span class="marks">[5]</span>

::: note Model answers — short (1–4)
**1.** (a) **Magnetic permeability** $\mu$ of a medium is the ratio of the magnetic flux density produced in it to the magnetising field: $\mu = B/H$, unit $\text{T m A}^{-1}$ (or $\text{H m}^{-1}$). It measures how readily the medium allows magnetic flux to be set up in it.
**Relative permeability** $\mu_r$ is the ratio of the permeability of the medium to that of free space:
$$ \mu_r = \frac{\mu}{\mu_0} = \frac{B}{B_0} $$
It is a pure number, equal to the factor by which the material multiplies the flux density.
**Magnetic susceptibility** $\chi_m$ is the ratio of the magnetisation produced to the magnetising field: $\chi_m = I/H$, also a pure number. It measures how easily the material becomes magnetised.

(b) The total flux density inside a magnetised material is the sum of the part due to the magnetising field and the part due to the magnetisation of the material itself:
$$ B = \mu_0(H+I) $$
Divide throughout by $\mu_0 H$:
$$ \frac{B}{\mu_0H} = 1+\frac{I}{H} $$
Now $B/H = \mu$, so the left side is $\mu/\mu_0 = \mu_r$, and $I/H = \chi_m$:
$$ \mu_r = 1+\chi_m $$

**2.** (a)

| Property | Diamagnetic | Paramagnetic | Ferromagnetic |
|---|---|---|---|
| Behaviour in a field | Feebly **repelled** | Feebly attracted | Strongly attracted |
| $\chi_m$ | Small and **negative** ($\approx-10^{-5}$) | Small and positive ($\approx10^{-5}$) | Very large and positive ($10^{3}$–$10^{5}$) |
| $\mu_r$ | Slightly less than $1$ | Slightly greater than $1$ | Very much greater than $1$ |
| Atomic magnetic moment | Zero (paired electrons) | Non-zero but randomly oriented | Non-zero, aligned in domains |
| Effect of temperature | Independent | $\chi_m \propto 1/T$ (Curie's law) | Becomes paramagnetic above $T_c$ |
| In a non-uniform field | Moves to the **weaker** part | Moves to the stronger part | Moves strongly to the stronger part |
| Examples | Bismuth, copper, water, gold | Aluminium, platinum, oxygen | Iron, cobalt, nickel, steel |

(b) **Diamagnetic** materials. Their induced magnetisation opposes the applied field (a consequence of Lenz's law at the atomic level), so a rod of bismuth suspended in a field sets itself **across** the field and is pushed towards the weaker region.

**3.** (a) **Hysteresis** is the lagging of the magnetisation (or flux density $B$) behind the magnetising field $H$ when a ferromagnetic specimen is taken through a complete cycle of magnetisation. Because of this lag, $B$ does not return along the original curve when $H$ is reduced, and the $B$–$H$ graph traces a closed loop (Figure 17).
Starting from an unmagnetised specimen, $B$ rises along $OA$ to **saturation**. As $H$ is reduced to zero, $B$ falls only to $OB_r$, not to zero. Reversing $H$ to $-OH_c$ brings $B$ to zero; further reversal saturates the specimen the other way, and the return path closes the loop.

(b) **Retentivity (remanence)** $B_r$ is the flux density that **remains** in the material when the magnetising field is reduced to zero — the intercept on the $B$ axis. It measures how much magnetism the material retains.
**Coercivity** $H_c$ is the reverse magnetising field needed to reduce that residual flux density to **zero** — the intercept on the $H$ axis. It measures how hard the material is to demagnetise.

**4.** (a) When a ferromagnetic specimen is carried round one complete cycle of magnetisation, work must be done by the magnetising source to turn the domains against the internal friction that opposes their rotation and wall motion. This work is not recovered when $H$ returns to zero, because the magnetisation lags behind: the material comes back to its starting point having absorbed net energy, which appears as **heat**.
Quantitatively, the work done per unit volume in changing the flux density by $dB$ is $H\,dB$, so over the whole cycle
$$ W = \oint H\,dB $$
and this integral is exactly the **area enclosed by the $B$–$H$ loop**. A wide loop therefore means a large energy loss per cycle; the power wasted is (area) × (volume) × (frequency).

(b) (i) **Transformer core — soft iron.** Its hysteresis loop is tall but very **narrow**, so the area, and hence the energy lost per cycle, is small; this matters because the core is taken round the loop $50$ times a second. Soft iron also has a very high permeability and low retentivity and coercivity, so it magnetises and demagnetises easily.
(ii) **Permanent magnet — steel (or alnico).** Its loop is **wide**, with high retentivity (so it keeps its magnetism) and high coercivity (so stray fields and rough handling cannot demagnetise it). The large loop area does not matter because the magnet is not cycled.
:::

::: note Model answers — short (5–8)
**5.** (a) **Magnetising field (magnetic field intensity)** $H$ is the field produced by the free current alone, independent of the medium; for a solenoid $H = nI$, unit $\text{A m}^{-1}$. **Magnetisation (intensity of magnetisation)** $I$ is the magnetic moment developed per unit volume of the material, $I = M/V$, also in $\text{A m}^{-1}$. **Flux density** $B$ is the total field inside the material, unit tesla. They are related by
$$ B = \mu_0(H+I) = \mu_0\mu_r H = \mu H $$

(b)
$$ B = \mu_0\mu_rH = 4\pi\times10^{-7}\times500\times2000 = 1.26\ \text{T} $$
$$ \chi_m = \mu_r-1 = 500-1 = 499 $$

**6.** (a) In a ferromagnetic material the atomic magnetic moments are not independent: a strong quantum-mechanical **exchange interaction** locks neighbouring atomic moments parallel to one another over small regions called **domains**, typically $10^{-6}$ to $10^{-4}\ \text{m}$ across and containing about $10^{17}$ atoms. Each domain is therefore magnetised to saturation even with no external field. In an unmagnetised specimen the domains point in random directions, so their moments cancel and the specimen shows no net magnetism.
When an external field is applied, two things happen: at low fields the **domain walls move**, so domains already pointing near the field direction grow at the expense of the others; at high fields the remaining domains **rotate** bodily into the field direction. When all domains are aligned, the specimen is **saturated** and no further increase is possible. Domain-wall motion is not perfectly reversible — walls get stuck at impurities and grain boundaries — and this is the microscopic origin of hysteresis.

(b) The **Curie temperature** $T_c$ is the temperature above which a ferromagnetic material loses its ferromagnetism and becomes merely **paramagnetic** ($770\ ^{\circ}\text{C}$ for iron, $358\ ^{\circ}\text{C}$ for nickel, $1131\ ^{\circ}\text{C}$ for cobalt). Above $T_c$ the thermal energy of the atoms exceeds the exchange energy holding the moments parallel, so the domain structure is destroyed; the susceptibility falls sharply and thereafter obeys the Curie-Weiss law $\chi_m = C/(T-T_c)$. On cooling below $T_c$ the domains reform and ferromagnetism returns.

**7.** (a) **Soft iron for electromagnets:** it has very high permeability, so a modest current gives a very strong field; very low retentivity, so the magnetism disappears almost completely the moment the current is switched off — essential for a crane magnet or a relay; and low coercivity with a narrow loop, so little energy is wasted if the field is reversed repeatedly.
**Steel for permanent magnets:** it has high retentivity, so it keeps almost all its magnetisation after the magnetising field is removed, and high coercivity, so it is not demagnetised by stray fields, mechanical shock or moderate heating. Its wide loop means large hysteresis loss, but a permanent magnet is never cycled, so that is irrelevant.

(b) A changing magnetic flux in a solid iron core induces circulating **eddy currents** in the core itself, and these dissipate energy as heat ($I^{2}R$) and heat the transformer. Laminating the core — building it from thin sheets insulated from one another by varnish or oxide, with their planes parallel to the flux — breaks the conducting paths available to those currents. The induced e.m.f. in each thin lamination is small and its resistance is high, so the eddy currents, and the power lost (which varies as the square of the lamination thickness), are greatly reduced.

**8.** (a) **Magnetic flux** through a surface is $\Phi = \vec{B}\cdot\vec{A} = BA\cos\theta$, the total number of field lines crossing it, measured in weber. **Gauss's law for magnetism:** the total magnetic flux through any **closed** surface is zero,
$$ \oint\vec{B}\cdot d\vec{A} = 0 $$
Every line that enters a closed surface must leave it again.

(b) Because **magnetic monopoles do not exist**. Electric field lines begin on positive charges and end on negative ones, so a closed surface round a single charge has a net outward flux — that is Gauss's law for electricity. But the smallest unit of magnetism is the **dipole**: cut a bar magnet in half and you get two complete magnets, each with its own north and south pole, never an isolated pole. With no sources or sinks for $\vec{B}$ to start or stop on, every field line must close on itself, running from N to S outside the magnet and from S to N inside it. The mathematical statement of this is $\oint\vec{B}\cdot d\vec{A} = 0$.
:::

```figure caption="Hysteresis loop of a ferromagnetic material. Retentivity B_r is the flux density left when H falls to zero; coercivity H_c is the reverse field needed to remove it. The enclosed area is the energy lost per cycle per unit volume."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7,3.2))
Hs = 3.0
def branch(H, sgn):
    return 1.35*np.tanh(0.95*(H + sgn*0.85))
H1 = np.linspace(-Hs, Hs, 400)
H2 = np.linspace(Hs, -Hs, 400)
ax.plot(H1, branch(H1, +1), color=ACCENT, lw=1.7)
ax.plot(H2, branch(H2, -1), color=ACCENT, lw=1.7)
Hi = np.linspace(0, Hs, 200)
ax.plot(Hi, 1.35*np.tanh(0.95*Hi)*0.5 + 0.5*branch(Hi, +1), color=MUTED,
        lw=1.2, ls='--')
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
Br = branch(0.0, -1)
Hc = -0.85
ax.plot([0],[Br],'o',color='#A8271F',ms=5)
ax.plot([Hc],[0],'o',color='#0B6A62',ms=5)
ax.annotate('$B_r$ (retentivity)', (0.12, Br+0.05), fontsize=8.4,
            color='#A8271F', ha='left', va='bottom')
ax.annotate('$H_c$ (coercivity)', (Hc-0.12, -0.16), fontsize=8.4,
            color='#0B6A62', ha='right', va='top')
ax.annotate('saturation', (Hs-0.08, 1.38), fontsize=8.4, color=MUTED,
            ha='right', va='bottom')
ax.annotate('initial\ncurve', (1.12, 0.32), fontsize=8.2, color=MUTED,
            ha='left', va='top')
ax.annotate('area = energy lost\nper cycle per $\\mathrm{m^3}$', (-2.90, -1.28),
            fontsize=8.2, color=INK, ha='left', va='center')
ax.set_xlabel('magnetising field  $H$  (A m$^{-1}$)', fontsize=9)
ax.set_ylabel('flux density  $B$  (T)', fontsize=9)
ax.set_xlim(-3.25, 3.25); ax.set_ylim(-1.85, 1.85)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
```
**Long answer / numerical questions [8 marks each]**

1. (a) Define $\mu$, $\mu_r$, $\chi_m$ and $I$, and derive $\mu_r = 1+\chi_m$. [4] (b) Compare dia-, para- and ferromagnetic materials in a table. [3] (c) A material of $\mu_r = 500$ is placed in a field of $H = 2000\ \text{A m}^{-1}$; find $B$, $\chi_m$ and the magnetisation $I$. [1] <span class="marks">[8]</span>
2. (a) Explain hysteresis and draw a fully labelled loop. [3] (b) Show that the area of the loop gives the energy lost per cycle per unit volume, and explain the microscopic origin of the loss. [3] (c) State with reasons which material suits a transformer core, an electromagnet and a permanent magnet. [2] <span class="marks">[8]</span> (NEB 2081)
3. (a) Explain the domain theory of ferromagnetism and use it to account for saturation and for hysteresis. [4] (b) What is the Curie temperature? [1] (c) Explain eddy currents, state two uses and two disadvantages, and explain how lamination reduces them. [3] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Permeability** $\mu = B/H$ measures how readily a medium carries magnetic flux. **Relative permeability** $\mu_r = \mu/\mu_0$ is the pure number by which the medium multiplies the flux density that the same magnetising field would produce in vacuum. **Magnetisation** $I$ is the magnetic moment per unit volume of the material. **Susceptibility** $\chi_m = I/H$ measures how readily the material becomes magnetised.
Inside a magnetised material the total flux density is the sum of the contribution of the magnetising field and that of the aligned atomic dipoles:
$$ B = \mu_0 H + \mu_0 I = \mu_0(H+I) $$
Divide both sides by $\mu_0H$:
$$ \frac{B}{\mu_0H} = \frac{H}{H}+\frac{I}{H} = 1+\chi_m $$
On the left, $B/H = \mu$, so $B/\mu_0H = \mu/\mu_0 = \mu_r$. Therefore
$$ \mu_r = 1+\chi_m $$
This single relation classifies all materials: $\chi_m$ slightly negative gives $\mu_r < 1$ (diamagnetic); $\chi_m$ small positive gives $\mu_r$ just above $1$ (paramagnetic); $\chi_m$ very large gives $\mu_r \gg 1$ (ferromagnetic).

(b) See the table in short answer 2 above: the comparison runs over the sign and size of $\chi_m$, the value of $\mu_r$, the atomic origin, the behaviour in a non-uniform field, the temperature dependence, and examples.

(c)
$$ B = \mu_0\mu_rH = 4\pi\times10^{-7}\times500\times2000 = 1.26\ \text{T} $$
$$ \chi_m = \mu_r-1 = 499 $$
$$ I = \chi_mH = 499\times2000 = 9.98\times10^{5}\ \text{A m}^{-1} $$

**2.** (a) **Hysteresis** is the lag of $B$ behind $H$ through a complete cycle of magnetisation. Figure 17 shows the loop: $OA$ is the initial magnetisation curve rising to saturation; $AB_r$ is the fall to the **retentivity** $B_r$ as $H$ returns to zero; $B_rH_c$ is the reverse field to the **coercivity** $H_c$ at which $B = 0$; then saturation in the reverse sense and the symmetrical return path, closing the loop.

(b) Consider unit volume of the material. When the flux density changes by $dB$ under a magnetising field $H$, the source must supply work $dW = H\,dB$ per unit volume. Over one complete cycle,
$$ W = \oint H\,dB $$
which is, by definition of an integral round a closed curve in the $H$–$B$ plane, the **area enclosed by the loop**. Since the loop is traversed once per cycle, the power dissipated in a core of volume $V$ at frequency $f$ is
$$ P = (\text{loop area})\times V\times f $$
**Microscopic origin.** The magnetisation changes by domain-wall motion and domain rotation. Walls do not move smoothly: they are pinned at impurities, dislocations and grain boundaries, and break free in sudden jumps (the Barkhausen effect). Each jump dissipates energy irreversibly as lattice vibrations, i.e. as heat. That is why the return path does not retrace the outward one and why the loop has area at all.

(c) **Transformer core — soft iron (or silicon steel):** narrow loop, so small area and small hysteresis loss at $50\ \text{Hz}$; also high $\mu_r$ so the flux linkage is large. **Electromagnet — soft iron:** high permeability for a strong field, but very low retentivity so the magnetism collapses when the current stops, which is the whole point of a lifting magnet or a relay. **Permanent magnet — steel, alnico or a rare-earth alloy:** high retentivity so it stays magnetised, and high coercivity so it resists demagnetisation; the large loop area is irrelevant because it is not cycled.

**3.** (a) A ferromagnetic material is divided into **domains** — small regions, about $10^{-6}$ to $10^{-4}\ \text{m}$ across, within which an exchange interaction holds all the atomic magnetic moments rigidly parallel, so each domain is spontaneously magnetised to saturation. In an unmagnetised specimen the domains point in random directions and their moments cancel, giving no net magnetism.
**Magnetisation and saturation.** Applying a weak field makes the domain **walls move**, so those domains already lying near the field direction grow at the expense of their neighbours; this stage is largely reversible. In stronger fields the remaining domains **rotate** bodily into line with the field. Once every domain is aligned, no further alignment is possible and $B$ increases only as fast as it would in vacuum: the specimen has reached **saturation**.
**Hysteresis.** Domain-wall motion is impeded by impurities, grain boundaries and internal strains, which pin the walls. Freeing a wall requires energy and happens in abrupt jumps, so the process is **irreversible**. When $H$ is reduced, the walls do not return to their original positions, and some alignment survives at $H = 0$ — the retentivity. A reverse field must be applied to unpin them and restore $B = 0$ — the coercivity. The energy lost in these irreversible jumps is the area of the loop.

(b) The **Curie temperature** is the temperature above which thermal agitation destroys the domain structure and the material ceases to be ferromagnetic, becoming ordinarily paramagnetic. For iron it is $770\ ^{\circ}\text{C}$. Above $T_c$ the susceptibility follows $\chi_m = C/(T-T_c)$.

(c) **Eddy currents** are circulating currents induced in the body of a conductor when the magnetic flux through it changes; by Lenz's law they flow so as to oppose the change, and they dissipate energy as heat.
**Uses:** (i) **induction furnaces**, where a high-frequency field melts a metal charge by the heat of its own eddy currents; (ii) **electromagnetic damping** in moving-coil galvanometers, balances and induction-type energy meters, making them dead-beat; (iii) **eddy-current brakes** in trains and in exercise machines, which are smooth and wear-free; (iv) induction cooking hobs and metal detectors.
**Disadvantages:** (i) they waste energy as heat in transformer and motor cores, lowering efficiency; (ii) the heating can damage insulation and demands cooling.
**Lamination.** The core is built of thin sheets insulated from one another, their planes **parallel to the flux**. Each lamination has a small cross-section, so the flux through it and hence the induced e.m.f. is small, while its resistance to the circulating path is large. Since eddy-current power varies as the square of the lamination thickness, using sheets $0.3\ \text{mm}$ thick instead of a solid core cuts the loss by orders of magnitude. (Hysteresis loss is unaffected by lamination; that is reduced by choosing silicon steel.)
:::

::: tip Examiner's note — Magnetic properties of materials
The three-way table is the fastest four marks in the paper — learn the **sign and
size of $\chi_m$** for each class, because that single row implies all the others.
In the $\mu_r = 1+\chi_m$ proof, start from $B = \mu_0(H+I)$ and divide by
$\mu_0H$; do not simply assert the result. Label the hysteresis loop fully: axes
$H$ and $B$ (not $I$), saturation, $B_r$ on the $B$ axis and $H_c$ on the $H$ axis.
And keep the two loss mechanisms separate — **hysteresis** loss is reduced by
choosing soft magnetic material, **eddy-current** loss by laminating.
:::

## 3.18 Electromagnetic Induction

CDC allots **6 teaching hours**. Faraday's and Lenz's laws, motional e.m.f., the
a.c. generator, self and mutual inductance, the energy stored in an inductor and
the transformer are all examinable, and this unit appeared in Group C in 2080 and
2082.

**Short answer questions [5 marks each]**

1. (a) State Faraday's laws of electromagnetic induction. [2] (b) State Lenz's law and show that it is a consequence of the conservation of energy. [3] <span class="marks">[5]</span> (NEB 2080)
2. (a) Derive the expression for the motional e.m.f. induced in a rod moving in a magnetic field. [3] (b) A rod $20\ \text{cm}$ long moves at $10\ \text{m s}^{-1}$ perpendicular to a field of $0.50\ \text{T}$; find the e.m.f. [2] <span class="marks">[5]</span>
3. (a) Describe the construction and working of an a.c. generator. [3] (b) Show that the e.m.f. produced is $e = NBA\omega\sin\omega t$. [2] <span class="marks">[5]</span> (NEB 2082)
4. (a) Define self-inductance and write its unit. [2] (b) Derive the self-inductance of a long solenoid. [3] <span class="marks">[5]</span>
5. (a) Derive the energy stored in an inductor. [3] (b) A coil of inductance $2.0\ \text{H}$ carries $3.0\ \text{A}$; find the stored energy and the e.m.f. induced if the current falls to zero in $0.50\ \text{s}$. [2] <span class="marks">[5]</span> (NEB 2081)
6. (a) Define mutual inductance and state four factors on which it depends. [3] (b) Two coils have $M = 0.20\ \text{H}$; find the e.m.f. induced in the second when the current in the first changes from $2.0\ \text{A}$ to $6.0\ \text{A}$ in $0.10\ \text{s}$. [2] <span class="marks">[5]</span>
7. (a) Explain the principle and working of a transformer and derive the turns-ratio relation. [3] (b) A transformer has $1200$ turns in the primary and $50$ in the secondary; if the primary is fed at $240\ \text{V}$, find the secondary voltage. [2] <span class="marks">[5]</span> (NEB 2082 model)
8. (a) List four energy losses in a transformer and state how each is reduced. [4] (b) Why is a transformer useless on d.c.? [1] <span class="marks">[5]</span>
9. (a) What are eddy currents? [1] (b) Give two uses and two disadvantages. [2] (c) A coil of $200$ turns experiences a flux change from $0.010\ \text{Wb}$ to $0.050\ \text{Wb}$ in $0.20\ \text{s}$; find the induced e.m.f. [2] <span class="marks">[5]</span>

::: note Model answers — short (1–5)
**1.** (a) **First law:** whenever the magnetic flux linked with a circuit changes, an e.m.f. is induced in it, and it lasts only as long as the change lasts. **Second law:** the magnitude of the induced e.m.f. is directly proportional to the rate of change of magnetic flux linkage:
$$ e = -N\frac{d\Phi}{dt} $$

(b) **Lenz's law:** the induced current always flows in such a direction as to **oppose** the change producing it; this is the meaning of the minus sign in Faraday's law.
**Energy argument.** Suppose the north pole of a magnet is pushed towards a coil. By Lenz's law the induced current makes the near face of the coil a north pole, which repels the magnet, so the experimenter must do **work** to continue pushing. That work is exactly the source of the electrical energy that appears in the coil. Now suppose the law were the other way round: the induced current would make the near face a south pole, which would **attract** the magnet, pulling it in faster, increasing the flux change, increasing the current, and so on without limit. We should get unlimited electrical energy and unlimited kinetic energy from nothing, which violates the conservation of energy. Lenz's law is therefore the statement of energy conservation for induced currents.

**2.** (a) Let a conducting rod $PQ$ of length $l$ slide with velocity $v$ on a pair of rails in a uniform field $B$ directed into the plane, the velocity being perpendicular to both the rod and the field. In a time $dt$ the rod sweeps out an area $l\,v\,dt$, so the flux through the circuit changes by
$$ d\Phi = B\,l\,v\,dt $$
By Faraday's law the magnitude of the induced e.m.f. is
$$ e = \frac{d\Phi}{dt} = Blv $$
(Equivalently: each free electron in the rod feels a force $evB$ along the rod, which drives charge to one end until the electrostatic field $E = V/l$ balances it, giving $V = Blv$.) If $\vec{v}$ makes an angle $\theta$ with $\vec{B}$, then $e = Blv\sin\theta$.

(b)
$$ e = Blv = 0.50\times0.20\times10 = 1.0\ \text{V} $$

**3.** (a) **Construction.** An **armature** — a rectangular coil of $N$ turns of insulated copper wire wound on a laminated soft-iron core — is mounted on an axle between the poles of a strong permanent magnet or electromagnet, so that it can be rotated in the field. The two ends of the coil are joined to two separate **slip rings** fixed on the axle, and two carbon **brushes** press against the rings and lead the current to the external circuit.
**Working.** As the coil is rotated, the flux linked with it changes continuously, so by Faraday's law an e.m.f. is induced. The sides of the coil cut the field lines in opposite senses, and each side reverses its sense of cutting twice per revolution, so the induced e.m.f. and current **alternate** in direction with the same frequency as the rotation. The slip rings keep each end of the coil permanently connected to its own brush, so the alternation is passed on to the external circuit unchanged.

(b) Let the coil of $N$ turns and area $A$ rotate with uniform angular velocity $\omega$ in a field $B$, and let $\theta = \omega t$ be the angle between the normal to the coil and $\vec{B}$, measured from the position where the coil's plane is perpendicular to the field. The flux linkage is
$$ N\Phi = NBA\cos\omega t $$
By Faraday's law,
$$ e = -\frac{d}{dt}(NBA\cos\omega t) = NBA\omega\sin\omega t $$
So $e = e_0\sin\omega t$ with peak value $e_0 = NBA\omega = 2\pi fNBA$.

**4.** (a) **Self-inductance** $L$ of a coil is the property by which it opposes any change of current through itself, by inducing a back e.m.f. Numerically it is the flux linkage per unit current, or the back e.m.f. per unit rate of change of current:
$$ L = \frac{N\Phi}{I} = \frac{-e}{dI/dt} $$
Its SI unit is the **henry (H)**: a coil has an inductance of one henry if a current changing at $1\ \text{A s}^{-1}$ induces a back e.m.f. of $1\ \text{V}$.

(b) Let a long solenoid of length $l$, cross-sectional area $A$ and $N$ turns (so $n = N/l$ per metre) carry a current $I$. The field inside is
$$ B = \mu_0nI = \frac{\mu_0NI}{l} $$
The flux through one turn is $\Phi = BA$, so the total flux linkage is
$$ N\Phi = NBA = \frac{\mu_0N^{2}IA}{l} $$
Hence
$$ L = \frac{N\Phi}{I} = \frac{\mu_0N^{2}A}{l} = \mu_0n^{2}Al = \mu_0n^{2}V $$
where $V = Al$ is the volume. With a core of relative permeability $\mu_r$, multiply by $\mu_r$.

**5.** (a) See the derivation box below. Summary: while the current is being built up from $0$ to $I$, the source must work against the back e.m.f. $L\,dI/dt$; the total work is
$$ W = \int_0^{I}LI'\,dI' = \tfrac12LI^{2} $$
and this is stored in the magnetic field of the coil.

(b)
$$ U = \tfrac12LI^{2} = \tfrac12\times2.0\times(3.0)^{2} = 9.0\ \text{J} $$
$$ |e| = L\frac{dI}{dt} = 2.0\times\frac{3.0}{0.50} = 12\ \text{V} $$
:::

::: note Model answers — short (6–9)
**6.** (a) **Mutual inductance** $M$ of a pair of coils is the flux linkage produced in the second coil per unit current in the first:
$$ M = \frac{N_2\Phi_2}{I_1} = \frac{-e_2}{dI_1/dt} $$
It is measured in henry, and $M_{12} = M_{21}$.
**Factors:** (i) the **number of turns** of each coil; (ii) the **area of cross-section** and the size of the coils; (iii) the **distance and orientation** between them — $M$ is greatest when they are close and coaxial, and zero when their axes are perpendicular; (iv) the **permeability of the medium or core** between them — a common soft-iron core greatly increases $M$.

(b)
$$ |e_2| = M\frac{dI_1}{dt} = 0.20\times\frac{6.0-2.0}{0.10} = 0.20\times40 = 8.0\ \text{V} $$

**7.** (a) A **transformer** changes an alternating voltage from one value to another. It works on the principle of **mutual induction**: an alternating current in one coil produces a changing flux, which links a second coil and induces an alternating e.m.f. in it. Two coils, the primary of $N_p$ turns and the secondary of $N_s$ turns, are wound on a common closed core of laminated soft iron, which carries virtually all the flux from one coil to the other.
Since the same flux $\Phi$ links every turn of both coils,
$$ e_p = -N_p\frac{d\Phi}{dt}, \qquad e_s = -N_s\frac{d\Phi}{dt} $$
Dividing one by the other, $d\Phi/dt$ cancels:
$$ \frac{e_s}{e_p} = \frac{N_s}{N_p} = k $$
If $k > 1$ it is a step-up transformer; if $k < 1$, step-down. For an ideal (loss-free) transformer the power is conserved, $V_pI_p = V_sI_s$, so
$$ \frac{V_s}{V_p} = \frac{N_s}{N_p} = \frac{I_p}{I_s} $$
— voltage is raised only at the cost of current.

(b)
$$ V_s = V_p\frac{N_s}{N_p} = 240\times\frac{50}{1200} = 10\ \text{V} $$
(a step-down transformer).

**8.** (a) (i) **Copper (I²R) loss** — heat in the resistance of the windings; reduced by using thick copper wire of low resistance. (ii) **Iron (eddy-current) loss** — currents circulating in the core; reduced by **laminating** the core with insulated sheets. (iii) **Hysteresis loss** — energy spent taking the core round its $B$–$H$ loop $50$ times a second; reduced by making the core of soft magnetic material with a narrow loop, such as silicon steel. (iv) **Flux leakage** — some flux from the primary does not link the secondary; reduced by winding the two coils on the same limb, one over the other, and by using a closed core of high permeability. (Humming due to magnetostriction is a fifth, small loss, reduced by clamping the laminations tightly.)

(b) Because a transformer depends entirely on a **changing** flux. A steady direct current produces a steady flux, so $d\Phi/dt = 0$ and no e.m.f. at all is induced in the secondary. Worse, the primary of a transformer has very low resistance and, with d.c., no back e.m.f. or inductive reactance to limit the current, so a large current flows and the primary winding burns out.

**9.** (a) **Eddy currents** are the circulating currents induced in the body of a solid conductor when the magnetic flux through it changes; they flow in closed loops in planes perpendicular to the flux and, by Lenz's law, oppose the change.

(b) **Uses:** induction furnaces for melting metals; electromagnetic damping in galvanometers and balances (dead-beat instruments); eddy-current brakes in trains; induction motors, induction cookers and metal detectors. **Disadvantages:** wasted energy as heat in the cores of transformers, motors and dynamos, reducing efficiency; the heat produced can damage the insulation and requires cooling arrangements.

(c)
$$ e = N\frac{d\Phi}{dt} = 200\times\frac{0.050-0.010}{0.20} = 200\times0.20 = 40\ \text{V} $$
:::

**Long answer / numerical questions [8 marks each]**

1. (a) State and explain Faraday's laws and Lenz's law. [3] (b) Describe an a.c. generator and derive $e = NBA\omega\sin\omega t$. [3] (c) A coil of $100$ turns and area $200\ \text{cm}^{2}$ rotates at $50\ \text{Hz}$ in a field of $0.50\ \text{T}$; find the peak and the r.m.s. e.m.f. [2] <span class="marks">[8]</span> (NEB 2082)
2. (a) Define self-inductance and derive the inductance of a long solenoid. [3] (b) Derive the energy stored in an inductor and explain where it resides. [3] (c) A solenoid of $1000$ turns per metre, area $10\ \text{cm}^{2}$ and length $0.50\ \text{m}$ carries $4.0\ \text{A}$. Find $L$ and the stored energy. [2] <span class="marks">[8]</span> (NEB 2081)
3. (a) Explain the principle, construction and working of a transformer, and derive the turns-ratio relation. [4] (b) Discuss its energy losses and how each is minimised. [2] (c) An ideal transformer steps $240\ \text{V}$ down to $10\ \text{V}$ with $1200$ primary turns. Find the number of secondary turns, and the primary current when the secondary delivers $2.0\ \text{A}$. [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Faraday's first law:** an e.m.f. is induced in a circuit whenever the magnetic flux linked with it changes, and it lasts only while the change lasts. **Second law:** the induced e.m.f. equals the rate of change of flux linkage, $e = -N\,d\Phi/dt$. The flux can be changed by moving the magnet, moving the coil, changing the area, rotating the coil, or changing the current in a neighbouring coil.
**Lenz's law:** the induced current always opposes the change that causes it. Pushing a north pole towards a coil makes the near face a north pole, which pushes back; pulling it away makes the near face a south pole, which pulls back. The law fixes the **direction** of the current and supplies the minus sign in Faraday's law. It is required by the conservation of energy: the mechanical work done against the opposing force is exactly the electrical energy generated. If the current helped the motion instead, the system would accelerate itself and produce energy from nothing.

(b) **Construction and working:** see short answer 3(a) above — armature coil, field magnet, slip rings and brushes; rotation changes the flux linkage continuously and produces an alternating e.m.f.
**Derivation.** Let the coil have $N$ turns of area $A$ and rotate with angular velocity $\omega$ about an axis perpendicular to a uniform field $B$. At time $t$ let the normal to the coil make an angle $\theta = \omega t$ with $\vec{B}$. The flux through one turn is
$$ \Phi = BA\cos\theta = BA\cos\omega t $$
so the flux linkage is $N\Phi = NBA\cos\omega t$. By Faraday's law,
$$ e = -\frac{d(N\Phi)}{dt} = -NBA\frac{d}{dt}(\cos\omega t) $$
$$ e = -NBA(-\omega\sin\omega t) = NBA\omega\sin\omega t $$
The e.m.f. is therefore sinusoidal, with peak value $e_0 = NBA\omega$, reached when $\omega t = 90^{\circ}$ — that is, when the plane of the coil is **parallel** to the field and its sides are cutting the lines of force fastest. The e.m.f. is zero when the plane is perpendicular to the field, even though the flux is then greatest.

(c)
$$ \omega = 2\pi f = 2\pi\times50 = 314.2\ \text{rad s}^{-1} $$
$$ e_0 = NBA\omega = 100\times0.50\times200\times10^{-4}\times314.2 = 314\ \text{V} $$
$$ e_{rms} = \frac{e_0}{\sqrt{2}} = \frac{314}{1.414} = 222\ \text{V} $$

**2.** (a) **Self-inductance** $L$ is the flux linkage per unit current, $L = N\Phi/I$, equivalently the back e.m.f. induced per unit rate of change of current, $e = -L\,dI/dt$; unit the henry.
**Solenoid.** For a long solenoid of length $l$, area $A$ and $N$ turns carrying $I$, the internal field is uniform:
$$ B = \mu_0nI = \frac{\mu_0NI}{l} $$
The flux through each turn is $BA$, and there are $N$ turns, so the flux linkage is
$$ N\Phi = \frac{\mu_0N^{2}AI}{l} $$
Dividing by $I$,
$$ L = \frac{\mu_0N^{2}A}{l} = \mu_0n^{2}Al $$
So $L$ depends only on the geometry of the coil and the core material — never on the current.

(b) See the derivation box below. In building the current from $0$ to $I$ the source does work
$$ W = \int_0^{I}LI'\,dI' = \tfrac12LI^{2} $$
**Where it resides:** in the **magnetic field** in the space inside the solenoid. Substituting $L = \mu_0n^{2}Al$ and $I = B/\mu_0n$,
$$ U = \tfrac12\mu_0n^{2}Al\left(\frac{B}{\mu_0n}\right)^{2} = \frac{B^{2}}{2\mu_0}(Al) $$
so the energy per unit volume is $u = B^{2}/2\mu_0$ — an expression containing only the field itself. The field is the store, exactly as an electric field stores $\tfrac12\varepsilon_0E^{2}$ per unit volume.

(c)
$$ L = \mu_0n^{2}Al = 4\pi\times10^{-7}\times(1000)^{2}\times10\times10^{-4}\times0.50 $$
$$ L = 4\pi\times10^{-7}\times10^{6}\times5.0\times10^{-4} = 6.28\times10^{-4}\ \text{H} $$
$$ U = \tfrac12LI^{2} = \tfrac12\times6.28\times10^{-4}\times(4.0)^{2} = 5.03\times10^{-3}\ \text{J} $$

**3.** (a) **Principle: mutual induction.** A changing current in one coil sets up a changing flux which, linking a second coil, induces an e.m.f. in it.
**Construction.** Two coils — the **primary** of $N_p$ turns, fed from the a.c. supply, and the **secondary** of $N_s$ turns, feeding the load — are wound on a **closed, laminated soft-iron core**, usually one over the other on the same limb so that almost all the flux is shared. The laminations are insulated from each other and the core metal is silicon steel.
**Working.** The alternating primary current produces an alternating flux in the core. The core guides essentially the whole of this flux through the secondary, so the same $d\Phi/dt$ acts on every turn of both coils:
$$ e_p = -N_p\frac{d\Phi}{dt}, \qquad e_s = -N_s\frac{d\Phi}{dt} $$
Dividing the second by the first cancels $d\Phi/dt$:
$$ \frac{e_s}{e_p} = \frac{N_s}{N_p} $$
For an ideal transformer there are no losses, so the power in equals the power out:
$$ V_pI_p = V_sI_s \;\Rightarrow\; \frac{I_p}{I_s} = \frac{V_s}{V_p} = \frac{N_s}{N_p} $$
A step-up transformer raises the voltage but lowers the current in exactly the same ratio; it cannot create power. This is why electrical energy is transmitted at very high voltage — the current, and so the $I^{2}R$ loss in the line, is small.

(b) **Copper loss** ($I^{2}R$ in the windings) — use thick, low-resistance copper conductors, and oil-cool large transformers. **Eddy-current loss** — laminate the core, insulating the sheets from one another. **Hysteresis loss** — use a magnetically soft core (silicon steel) with a narrow $B$–$H$ loop. **Flux leakage** — use a closed core of high permeability and interleave the primary and secondary windings on the same limb. With these measures a large power transformer reaches an efficiency of $98$–$99\%$.

(c)
$$ N_s = N_p\frac{V_s}{V_p} = 1200\times\frac{10}{240} = 50\ \text{turns} $$
For an ideal transformer, $V_pI_p = V_sI_s$:
$$ I_p = \frac{V_sI_s}{V_p} = \frac{10\times2.0}{240} = 0.083\ \text{A} = 83\ \text{mA} $$
**Check:** output power $= 10\times2.0 = 20\ \text{W}$; input power $= 240\times0.083 = 20\ \text{W}$. ✓
:::

::: derivation Energy stored in an inductor
We start from the back e.m.f. that opposes a growing current and reach the stored
energy $U = \tfrac12LI^{2}$, then show that the energy actually sits in the magnetic
field.

**Setting up.** A coil of self-inductance $L$ is connected to a source, and the
current in it grows from zero to a final steady value $I$. While the current is
changing, the coil induces a back e.m.f. that opposes the growth, so the source
must do work against it. That work is what we want to find. Take the resistance of
the coil to be zero, so that none of the work is wasted as heat.

**Step 1 — write the back e.m.f. at the moment when the current is $i$.** By
Faraday's and Lenz's laws,

$$ e = -L\frac{di}{dt} $$

**Step 2 — write the voltage the source must supply.** To keep the current growing,
the source must exactly overcome this back e.m.f.:

$$ V = L\frac{di}{dt} $$

**Step 3 — write the power the source delivers.** Power is voltage times current:

$$ P = Vi = Li\frac{di}{dt} $$

**Step 4 — write the work done in a short time $dt$.** Work is power times time:

$$ dW = P\,dt = Li\frac{di}{dt}dt $$

**Step 5 — cancel $dt$.** The $dt$ in the numerator and denominator cancel, leaving
an expression in $di$ alone:

$$ dW = Li\,di $$

**Step 6 — add up all these small contributions.** Integrate as the current grows
from $0$ to its final value $I$:

$$ W = \int_0^{I} Li\,di $$

**Step 7 — take the constant $L$ outside and integrate.** The integral of $i\,di$ is
$i^{2}/2$:

$$ W = L\left[\frac{i^{2}}{2}\right]_0^{I} $$

**Step 8 — put in the limits.**

$$ W = \frac{1}{2}LI^{2} - 0 = \frac{1}{2}LI^{2} $$

**Step 9 — find where the energy is kept.** Take a solenoid, for which
$L = \mu_0n^{2}Al$ and $B = \mu_0nI$, so $I = B/\mu_0n$. Substitute both:

$$ U = \frac{1}{2}\left(\mu_0n^{2}Al\right)\left(\frac{B}{\mu_0n}\right)^{2} $$

**Step 10 — simplify.** The $n^{2}$ cancels and one $\mu_0$ survives in the
denominator:

$$ U = \frac{B^{2}}{2\mu_0}\left(Al\right) $$

**Step 11 — divide by the volume $Al$ to get the energy density.**

$$ u = \frac{B^{2}}{2\mu_0} $$

**Result.**

$$ U = \frac{1}{2}LI^{2}, \qquad u = \frac{B^{2}}{2\mu_0} $$

**What it means.** The energy is not stored "in the wire" — the final expression
contains only $B$ and $\mu_0$, so it is stored in the **magnetic field** filling the
space inside the coil, at a density $B^{2}/2\mu_0$ joule per cubic metre. This
mirrors the electric case, where a capacitor stores $\tfrac12CV^{2}$ at a density
$\tfrac12\varepsilon_0E^{2}$. Because the energy must be returned when the current
is switched off, breaking the circuit of a large inductor produces a violent spark
at the switch: the energy has nowhere else to go. That is also why the ignition coil
of a petrol engine can make a spark of thousands of volts from a $12\ \text{V}$
battery.

**Conditions.** The coil must have no resistance for the whole of $W$ to be stored
(with resistance, the extra $I^{2}R$ work becomes heat and is *not* recoverable),
and $L$ must be constant — which fails for an iron-cored coil near saturation,
where $L$ falls as the current rises.
:::

::: tip Examiner's note — Electromagnetic Induction
Keep the two directions straight: Faraday's law gives the **size** of the e.m.f.,
Lenz's law gives its **direction** and supplies the minus sign. When asked to
"justify Lenz's law", the expected answer is the **energy** argument — describe the
repulsion, the work done, and the absurdity of the alternative. In the generator
derivation, start from $\Phi = BA\cos\omega t$ (not $\sin$): the flux is greatest
when the e.m.f. is zero, and getting this the wrong way round costs a mark.
For the inductor energy, show the integral $\int Li\,di$; quoting $\tfrac12LI^{2}$
alone earns only one of three marks. In transformer numericals, use the
turns ratio for voltage but remember the current ratio is **inverted**.
:::

## 3.19 Alternating Currents

CDC allots **6 teaching hours**. Peak and r.m.s. values, the behaviour of $R$, $L$
and $C$ separately, the series LCR circuit with its phasor diagram, resonance,
power factor and wattless current are the standard questions; the series LCR
circuit is a very frequent Group C question and appeared in 2079 model and 2081.

**Short answer questions [5 marks each]**

1. (a) Define peak value, r.m.s. value and mean value of an alternating current. [3] (b) Show that $I_{rms} = I_0/\sqrt{2}$. [2] <span class="marks">[5]</span> (NEB 2080)
2. (a) An a.c. of peak value $5.0\ \text{A}$ flows in a circuit. Find its r.m.s. value and its mean value over half a cycle. [2] (b) The mains supply is quoted as $220\ \text{V}$; what is its peak value? [1] (c) Why is the r.m.s. value, not the peak value, quoted? [2] <span class="marks">[5]</span>
3. (a) Show that the current lags the voltage by $90^{\circ}$ in a purely inductive circuit, and define inductive reactance. [3] (b) Find $X_L$ for $L = 0.50\ \text{H}$ at $50\ \text{Hz}$. [2] <span class="marks">[5]</span> (NEB 2082)
4. (a) Show that the current leads the voltage by $90^{\circ}$ in a purely capacitive circuit, and define capacitive reactance. [3] (b) Find $X_C$ for $C = 100\ \mu\text{F}$ at $50\ \text{Hz}$. [2] <span class="marks">[5]</span>
5. (a) Draw the phasor diagram for a series LCR circuit and write the expression for its impedance. [3] (b) Find $Z$ for $R = 30\ \Omega$, $X_L = 70\ \Omega$, $X_C = 30\ \Omega$. [2] <span class="marks">[5]</span> (NEB 2081)
6. (a) What is resonance in a series LCR circuit? Derive the resonant frequency. [3] (b) Find $f_0$ for $L = 1.0\ \text{H}$ and $C = 10\ \mu\text{F}$. [2] <span class="marks">[5]</span> (NEB 2079 model)
7. (a) Define power factor and wattless current. [2] (b) Show that the average power in an a.c. circuit is $P = V_{rms}I_{rms}\cos\phi$, and explain why a pure inductor consumes no power. [3] <span class="marks">[5]</span> (NEB 2082 model)
8. (a) Distinguish between resistance, reactance and impedance. [3] (b) Why does a capacitor block d.c. but pass a.c.? [2] <span class="marks">[5]</span>
9. (a) What is the quality factor of a series resonant circuit and what does a high value mean? [3] (b) For $L = 1.0\ \text{H}$, $C = 10\ \mu\text{F}$ and $R = 20\ \Omega$, find $Q$. [2] <span class="marks">[5]</span>

::: note Model answers — short (1–5)
**1.** (a) The **peak (maximum) value** $I_0$ is the largest value the alternating current reaches in either direction during a cycle. The **r.m.s. (root-mean-square, or virtual) value** is that steady direct current which would produce the same heating effect in a given resistance in the same time — it is the square root of the mean of the squares of the instantaneous values over one complete cycle. The **mean value** over a complete cycle is **zero**, because the positive and negative halves cancel; the useful mean is therefore taken over **half** a cycle, and equals $2I_0/\pi = 0.637I_0$.

(b) Let $I = I_0\sin\omega t$. The heat produced in a resistance $R$ in time $dt$ is $I^{2}R\,dt$, so the mean of $I^{2}$ over one period $T$ is
$$ \overline{I^{2}} = \frac{1}{T}\int_0^{T}I_0^{2}\sin^{2}\omega t\,dt $$
Using $\sin^{2}\omega t = \tfrac12(1-\cos2\omega t)$, the mean of $\cos2\omega t$ over a whole number of cycles is zero, so the mean of $\sin^{2}\omega t$ is $\tfrac12$:
$$ \overline{I^{2}} = \frac{I_0^{2}}{2} \;\Rightarrow\; I_{rms} = \sqrt{\overline{I^{2}}} = \frac{I_0}{\sqrt{2}} = 0.707I_0 $$

**2.** (a)
$$ I_{rms} = \frac{I_0}{\sqrt{2}} = \frac{5.0}{1.414} = 3.54\ \text{A} $$
$$ I_{mean(\text{half cycle})} = \frac{2I_0}{\pi} = \frac{2\times5.0}{3.142} = 3.18\ \text{A} $$

(b)
$$ V_0 = \sqrt{2}\,V_{rms} = 1.414\times220 = 311\ \text{V} $$

(c) Because the **r.m.s. value is the one that determines the heating and the power**: an a.c. of r.m.s. value $220\ \text{V}$ delivers exactly the same power to a heater as a steady $220\ \text{V}$ d.c. supply, so all the d.c. formulae $P = V^{2}/R = I^{2}R$ can be used unchanged. Ordinary a.c. ammeters and voltmeters (hot-wire and moving-iron types) respond to the mean square of the current and so read r.m.s. directly. The mean value over a full cycle would be useless, since it is zero. (The **peak** value still matters for insulation design, which must withstand $311\ \text{V}$, not $220\ \text{V}$.)

**3.** (a) Let $V = V_0\sin\omega t$ be applied to a pure inductance $L$ of zero resistance. The back e.m.f. balances the applied voltage:
$$ V_0\sin\omega t = L\frac{dI}{dt} \;\Rightarrow\; dI = \frac{V_0}{L}\sin\omega t\,dt $$
Integrating,
$$ I = -\frac{V_0}{\omega L}\cos\omega t = \frac{V_0}{\omega L}\sin\!\left(\omega t-\frac{\pi}{2}\right) $$
So the current has the same frequency but its phase is $\pi/2$ **behind** the voltage: the current **lags** the voltage by $90^{\circ}$. Physically, the self-induced e.m.f. opposes the growth of the current, so the current cannot rise until after the voltage has.
Comparing with $I = I_0\sin(\omega t-\pi/2)$ gives $I_0 = V_0/\omega L$, so the quantity $\omega L$ plays the part of resistance. **Inductive reactance** $X_L = \omega L = 2\pi fL$, measured in ohms, is the opposition offered by an inductor to alternating current. It is proportional to frequency: an inductor passes d.c. ($f=0$, $X_L=0$) freely but chokes high frequencies.

(b)
$$ X_L = 2\pi fL = 2\times3.142\times50\times0.50 = 157\ \Omega $$

**4.** (a) Let $V = V_0\sin\omega t$ be applied to a pure capacitance $C$. The charge is
$$ q = CV = CV_0\sin\omega t $$
and the current is the rate of flow of charge:
$$ I = \frac{dq}{dt} = \omega CV_0\cos\omega t = \omega CV_0\sin\!\left(\omega t+\frac{\pi}{2}\right) $$
The current is $\pi/2$ **ahead** of the voltage: the current **leads** by $90^{\circ}$. Physically, the current is largest when the capacitor is empty and the voltage across it is zero, and falls to zero when the capacitor is fully charged and the voltage is greatest.
Comparing with $I = I_0\sin(\omega t+\pi/2)$ gives $I_0 = V_0/(1/\omega C)$, so **capacitive reactance** is
$$ X_C = \frac{1}{\omega C} = \frac{1}{2\pi fC} $$
in ohms. It is inversely proportional to frequency: infinite at $f = 0$, so d.c. is blocked completely, and small at high frequency, so a capacitor passes a.c. easily.

(b)
$$ X_C = \frac{1}{2\pi fC} = \frac{1}{2\times3.142\times50\times100\times10^{-6}} = 31.8\ \Omega $$

**5.** (a) In a **series** circuit the same current flows through all three elements, so the current phasor $I$ is drawn as the reference along the positive $x$-axis. Then $V_R = IR$ is in phase with $I$ (drawn along $I$); $V_L = IX_L$ leads $I$ by $90^{\circ}$ (drawn upwards); $V_C = IX_C$ lags $I$ by $90^{\circ}$ (drawn downwards). See Figure 18.
$V_L$ and $V_C$ are opposite, so they combine to a single phasor of magnitude $|V_L-V_C|$. The applied voltage is the resultant of this and $V_R$, at right angles:
$$ V = \sqrt{V_R^{2}+(V_L-V_C)^{2}} = I\sqrt{R^{2}+(X_L-X_C)^{2}} $$
$$ Z = \frac{V}{I} = \sqrt{R^{2}+(X_L-X_C)^{2}}, \qquad \tan\phi = \frac{X_L-X_C}{R} $$

(b)
$$ Z = \sqrt{30^{2}+(70-30)^{2}} = \sqrt{900+1600} = \sqrt{2500} = 50\ \Omega $$
:::

::: note Model answers — short (6–9)
**6.** (a) **Resonance** is the condition in which the inductive and capacitive reactances of a series LCR circuit become equal and cancel, so that the impedance falls to its minimum value $R$, the current rises to its maximum $V/R$, and the current is exactly **in phase** with the applied voltage (power factor $= 1$). It occurs at one particular frequency, the **resonant frequency**.
At resonance $X_L = X_C$:
$$ \omega_0L = \frac{1}{\omega_0C} \;\Rightarrow\; \omega_0^{2} = \frac{1}{LC} $$
$$ \omega_0 = \frac{1}{\sqrt{LC}} \;\Rightarrow\; f_0 = \frac{1}{2\pi\sqrt{LC}} $$
Because the current is greatest there, the series resonant circuit is called an **acceptor** circuit; it is used to tune a radio receiver to one station.

(b)
$$ f_0 = \frac{1}{2\pi\sqrt{LC}} = \frac{1}{2\pi\sqrt{1.0\times10\times10^{-6}}} $$
$$ f_0 = \frac{1}{2\pi\times3.162\times10^{-3}} = 50.3\ \text{Hz} $$

**7.** (a) **Power factor** is the cosine of the phase angle between the applied voltage and the current, $\cos\phi = R/Z$. It is the fraction of the apparent power $V_{rms}I_{rms}$ that is actually consumed. **Wattless (idle) current** is the component of the current at $90^{\circ}$ to the voltage, $I\sin\phi$; it flows in the circuit but consumes **no** average power.

(b) Let $V = V_0\sin\omega t$ and $I = I_0\sin(\omega t-\phi)$. The instantaneous power is
$$ P = VI = V_0I_0\sin\omega t\,\sin(\omega t-\phi) $$
Using $2\sin A\sin B = \cos(A-B)-\cos(A+B)$,
$$ P = \frac{V_0I_0}{2}\left[\cos\phi-\cos(2\omega t-\phi)\right] $$
Averaged over a complete cycle the term $\cos(2\omega t-\phi)$ gives zero, so
$$ P_{av} = \frac{V_0I_0}{2}\cos\phi = \frac{V_0}{\sqrt{2}}\cdot\frac{I_0}{\sqrt{2}}\cos\phi $$
$$ P_{av} = V_{rms}I_{rms}\cos\phi $$
**A pure inductor** has $R = 0$, so $\phi = 90^{\circ}$ and $\cos\phi = 0$, giving $P_{av} = 0$. Energy is not destroyed but exchanged: during a quarter cycle the inductor draws energy from the source and stores it in its magnetic field, and during the next quarter cycle it returns all of it. The average over a full cycle is exactly zero. The same is true of a pure capacitor, which stores and returns energy in its electric field.

**8.** (a) **Resistance** $R$ is the opposition of a resistor; it is independent of frequency, the current and voltage are in phase, and it **dissipates** energy as heat. **Reactance** ($X_L = \omega L$ or $X_C = 1/\omega C$) is the opposition of an inductor or capacitor; it depends on frequency, produces a $90^{\circ}$ phase difference, and dissipates **no** energy — it only stores and returns it. **Impedance** $Z$ is the total opposition of a circuit containing both, $Z = \sqrt{R^{2}+(X_L-X_C)^{2}}$, with a phase angle between $0$ and $90^{\circ}$. All three are measured in ohms.

(b) The dielectric of a capacitor is an insulator, so no charge ever crosses the gap. With **d.c.**, current flows only for the brief instant of charging; once the capacitor is charged to the supply voltage the current stops, so the capacitor **blocks** d.c. — consistent with $X_C = 1/2\pi fC \to \infty$ as $f \to 0$. With **a.c.** the supply voltage reverses continually, so the capacitor charges, discharges, charges the other way and discharges again, $50$ times a second. Charge surges back and forth in the leads, and this counts as a current in the external circuit even though no charge crosses the dielectric. The higher the frequency, the more often this happens and the larger the current, so $X_C$ falls as $f$ rises.

**9.** (a) The **quality factor** $Q$ measures the sharpness of resonance. It is the ratio of the voltage developed across the inductor (or the capacitor) at resonance to the applied voltage:
$$ Q = \frac{\omega_0L}{R} = \frac{1}{\omega_0CR} = \frac{1}{R}\sqrt{\frac{L}{C}} $$
Equivalently $Q = f_0/\Delta f$, where $\Delta f$ is the width of the resonance curve at $1/\sqrt{2}$ of the maximum current. A **high $Q$** means a small $R$, a tall and very narrow resonance peak, and large voltage magnification across $L$ and $C$ — so the circuit is highly **selective**, accepting one frequency and rejecting its neighbours. This is exactly what a radio tuner needs.

(b)
$$ Q = \frac{1}{R}\sqrt{\frac{L}{C}} = \frac{1}{20}\sqrt{\frac{1.0}{10\times10^{-6}}} = \frac{1}{20}\times316.2 = 15.8 $$
:::

```figure caption="Left: phasor diagram for a series LCR circuit, with the current I as reference. Right: the resonance curve — current is a maximum at f0, and a smaller R gives a sharper peak."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2,2.9))

# --- phasor diagram ---
a1.annotate('', xy=(1.0,0), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6))
a1.text(1.04, -0.05, '$V_R = IR$', fontsize=8.2, color=INK, ha='left', va='top')
a1.annotate('', xy=(0,1.0), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.6))
a1.text(-0.05, 1.02, '$V_L$', fontsize=8.2, color=ACCENT, ha='right', va='bottom')
a1.annotate('', xy=(0,-0.45), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.6))
a1.text(-0.05, -0.47, '$V_C$', fontsize=8.2, color='#0B6A62', ha='right', va='top')
a1.annotate('', xy=(1.0,0.55), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.9))
a1.text(1.02, 0.60, '$V$', fontsize=8.6, color='#A8271F', ha='left', va='bottom')
a1.plot([1.0,1.0],[0,0.55], color=MUTED, lw=0.9, ls=':')
a1.plot([0,1.0],[0.55,0.55], color=MUTED, lw=0.9, ls=':')
a1.text(1.06, 0.28, '$V_L - V_C$', fontsize=7.8, color=MUTED,
        ha='left', va='center')
th = np.linspace(0, np.arctan2(0.55,1.0), 40)
a1.plot(0.34*np.cos(th), 0.34*np.sin(th), color=MUTED, lw=0.9)
a1.text(0.40, 0.10, r'$\phi$', fontsize=9, color=MUTED)
a1.text(0.50, -0.72, 'current $I$ is the reference', fontsize=7.8,
        color=MUTED, ha='center')
a1.set_xlim(-0.40, 1.70); a1.set_ylim(-0.95, 1.25)
a1.set_aspect('equal'); a1.axis('off')

# --- resonance curve ---
L, C, V = 1.0, 10e-6, 200.0
f0 = 1/(2*np.pi*np.sqrt(L*C))
f = np.linspace(0.5*f0, 1.8*f0, 900)
w = 2*np.pi*f
for R, ls, lab in ((10.0,'-','small $R$ (high $Q$)'), (40.0,'--','large $R$ (low $Q$)')):
    Z = np.sqrt(R**2 + (w*L - 1/(w*C))**2)
    a2.plot(f, V/Z, ls=ls, lw=1.6, label=lab)
a2.axvline(f0, color=MUTED, lw=0.9, ls=':')
a2.text(f0+1.2, 17.0, '$f_0$', fontsize=9, color=MUTED, ha='left')
a2.set_xlabel('frequency  $f$  (Hz)', fontsize=9)
a2.set_ylabel('current  $I$  (A)', fontsize=9)
a2.legend(fontsize=7.2, frameon=False, loc='upper right')
a2.set_ylim(0, 23)
a2.grid(True, color=GRID, lw=0.5)
a2.spines[['top','right']].set_visible(False)
fig.subplots_adjust(wspace=0.35)
```
**Long answer / numerical questions [8 marks each]**

1. (a) Draw the phasor diagram of a series LCR circuit and derive $Z = \sqrt{R^{2}+(X_L-X_C)^{2}}$ and $\tan\phi = (X_L-X_C)/R$. [4] (b) A series circuit has $R = 30\ \Omega$, $X_L = 70\ \Omega$ and $X_C = 30\ \Omega$ across a $200\ \text{V}$ a.c. supply. Find the impedance, the current, the phase angle, the power factor and the power consumed. [4] <span class="marks">[8]</span> (NEB 2081)
2. (a) What is resonance in a series LCR circuit? Derive $f_0 = 1/2\pi\sqrt{LC}$ and sketch the resonance curve. [4] (b) Define the quality factor and explain its significance. [2] (c) For $L = 1.0\ \text{H}$, $C = 10\ \mu\text{F}$, $R = 20\ \Omega$ and $V = 200\ \text{V}$, find $f_0$, the current at resonance, the voltage across $L$ at resonance, and $Q$. [2] <span class="marks">[8]</span> (NEB 2079 model)
3. (a) Obtain the phase relation between current and voltage separately for a pure resistor, a pure inductor and a pure capacitor, and define reactance in each case. [4] (b) Derive $P = V_{rms}I_{rms}\cos\phi$ and explain "wattless current". [3] (c) Why must the power factor of an industrial installation be kept close to $1$? [1] <span class="marks">[8]</span> (NEB 2082 model)

::: note Model answers — long
**1.** (a) See the derivation box below for the full argument. In outline: the same current $I = I_0\sin\omega t$ flows through $R$, $L$ and $C$, so $I$ is the reference phasor. $V_R = IR$ is in phase with $I$; $V_L = IX_L$ leads by $90^{\circ}$; $V_C = IX_C$ lags by $90^{\circ}$ (Figure 18). Since $V_L$ and $V_C$ are anti-parallel, their resultant is $(V_L - V_C)$ along the $V_L$ direction, perpendicular to $V_R$. By Pythagoras,
$$ V = \sqrt{V_R^{2}+(V_L-V_C)^{2}} = I\sqrt{R^{2}+(X_L-X_C)^{2}} $$
$$ Z = \frac{V}{I} = \sqrt{R^{2}+(X_L-X_C)^{2}}, \qquad \tan\phi = \frac{V_L-V_C}{V_R} = \frac{X_L-X_C}{R} $$
If $X_L > X_C$ the circuit is inductive and the current lags; if $X_C > X_L$ it is capacitive and the current leads; if they are equal the circuit is purely resistive and in resonance.

(b)
$$ Z = \sqrt{R^{2}+(X_L-X_C)^{2}} = \sqrt{30^{2}+40^{2}} = 50\ \Omega $$
$$ I = \frac{V}{Z} = \frac{200}{50} = 4.0\ \text{A} $$
$$ \tan\phi = \frac{X_L-X_C}{R} = \frac{40}{30} = 1.333 \;\Rightarrow\; \phi = 53.1^{\circ} $$
Since $X_L > X_C$, the current **lags** the voltage by $53.1^{\circ}$.
$$ \cos\phi = \frac{R}{Z} = \frac{30}{50} = 0.60 $$
$$ P = VI\cos\phi = 200\times4.0\times0.60 = 480\ \text{W} $$
**Check** by the other route: $P = I^{2}R = (4.0)^{2}\times30 = 480\ \text{W}$. ✓ All the power is dissipated in $R$; $L$ and $C$ dissipate none.

**2.** (a) **Resonance** is the state of a series LCR circuit in which $X_L = X_C$, so the two reactances cancel completely. Then $Z$ has its least possible value $R$, the current its greatest value $V/R$, and $\tan\phi = 0$, so the current is exactly in phase with the applied voltage and the power factor is $1$. Physically, the energy pumped into the magnetic field of $L$ during one quarter cycle is exactly what the electric field of $C$ gives back, so the source has only to supply the $I^{2}R$ heat.
$$ X_L = X_C \;\Rightarrow\; \omega_0 L = \frac{1}{\omega_0C} \;\Rightarrow\; \omega_0^{2}LC = 1 $$
$$ \omega_0 = \frac{1}{\sqrt{LC}} \;\Rightarrow\; f_0 = \frac{1}{2\pi\sqrt{LC}} $$
The resonance curve (Figure 18, right) is a plot of $I$ against $f$: it rises to a sharp maximum at $f_0$ and falls away on both sides. A smaller $R$ gives a taller, narrower peak.

(b) The **quality factor** $Q = \omega_0L/R = (1/R)\sqrt{L/C}$ is the voltage magnification across $L$ or $C$ at resonance, and equals $f_0/\Delta f$, where $\Delta f$ is the bandwidth at $1/\sqrt{2}$ of the peak current. **Significance:** a high $Q$ means a sharp, selective response — the circuit accepts a narrow band of frequencies and rejects all others, which is how a radio set picks out one station from many. It also means large voltages appear across $L$ and $C$ individually, which may greatly exceed the supply voltage and must be allowed for in the insulation.

(c)
$$ f_0 = \frac{1}{2\pi\sqrt{LC}} = \frac{1}{2\pi\sqrt{1.0\times10^{-5}}} = 50.3\ \text{Hz} $$
At resonance $Z = R = 20\ \Omega$, so
$$ I = \frac{V}{R} = \frac{200}{20} = 10\ \text{A} $$
$$ X_L = 2\pi f_0L = 2\pi\times50.3\times1.0 = 316\ \Omega $$
$$ V_L = IX_L = 10\times316 = 3.16\times10^{3}\ \text{V} $$
$$ Q = \frac{1}{R}\sqrt{\frac{L}{C}} = \frac{1}{20}\sqrt{\frac{1.0}{10^{-5}}} = 15.8 $$
**Check:** $Q = V_L/V = 3160/200 = 15.8$. ✓ Note that $V_L$ is nearly $16$ times the supply voltage, and $V_C$ is equal and opposite to it, so the two cancel in the series sum.

**3.** (a) **Pure resistor.** With $V = V_0\sin\omega t$, Ohm's law gives $I = (V_0/R)\sin\omega t$ at every instant: the current is **in phase** with the voltage, $\phi = 0$. The opposition is the resistance $R$, independent of frequency.
**Pure inductor.** $V_0\sin\omega t = L\,dI/dt$, so integrating,
$$ I = \frac{V_0}{\omega L}\sin\!\left(\omega t-\frac{\pi}{2}\right) $$
The current **lags** the voltage by $90^{\circ}$, and the opposition is the **inductive reactance** $X_L = \omega L = 2\pi fL$, which grows with frequency.
**Pure capacitor.** $q = CV_0\sin\omega t$, so
$$ I = \frac{dq}{dt} = \omega CV_0\sin\!\left(\omega t+\frac{\pi}{2}\right) $$
The current **leads** the voltage by $90^{\circ}$, and the opposition is the **capacitive reactance** $X_C = 1/\omega C = 1/2\pi fC$, which falls as frequency rises.

(b) With $V = V_0\sin\omega t$ and $I = I_0\sin(\omega t-\phi)$, the instantaneous power is
$$ P = V_0I_0\sin\omega t\sin(\omega t-\phi) $$
$$ P = \frac{V_0I_0}{2}\left[\cos\phi-\cos(2\omega t-\phi)\right] $$
Over a complete cycle the mean of $\cos(2\omega t-\phi)$ is zero, so
$$ P_{av} = \frac{V_0I_0}{2}\cos\phi = V_{rms}I_{rms}\cos\phi $$
**Wattless current.** Resolve $I$ into a component $I\cos\phi$ along $V$ and a component $I\sin\phi$ perpendicular to it. Only the first contributes to $P_{av}$; the perpendicular component $I\sin\phi$ flows in the wires, heats them, and loads the generator, but contributes **zero** average power. It is therefore called the wattless or idle current. In a pure inductor or capacitor $\phi = 90^{\circ}$ and the whole current is wattless.

(c) The supply must carry the full current $I = P/(V\cos\phi)$, so a low power factor means a **larger current for the same useful power**. That larger current causes greater $I^{2}R$ heating in the cables and transformers, a larger voltage drop along the line, and requires thicker conductors and bigger switchgear — all wasted cost. Industrial loads are largely inductive (motors), so capacitor banks are connected in parallel to bring $\cos\phi$ back close to $1$; electricity boards fine consumers whose power factor falls too low.
:::

::: derivation Impedance of a series LCR circuit from the phasor diagram
We want a single number $Z$ that replaces $R$ in Ohm's law when a resistor, an
inductor and a capacitor are joined in series across an a.c. supply.

**Setting up.** $R$, $L$ and $C$ are in series across $V = V_0\sin\omega t$. Because
they are in series, the **same** current flows through all three at every instant, so
the current is the natural reference. Each element has its own voltage, and these
voltages do not peak at the same moment, so they cannot simply be added as numbers.
We represent each by a rotating arrow (a phasor) whose length is the peak voltage
and whose angle shows the phase, and add the arrows.

**Step 1 — draw the current phasor.** Take $I$ along the positive $x$-axis. Every
phase angle below is measured from this line.

**Step 2 — place the voltage across the resistor.** For a resistor the current and
voltage rise and fall together, so $V_R$ points **along** $I$:

$$ V_R = IR $$

**Step 3 — place the voltage across the inductor.** In an inductor the current lags
the voltage by $90^{\circ}$, so the voltage **leads** the current by $90^{\circ}$;
draw $V_L$ straight **up** from the origin:

$$ V_L = IX_L, \qquad X_L = \omega L $$

**Step 4 — place the voltage across the capacitor.** In a capacitor the current
leads the voltage by $90^{\circ}$, so the voltage **lags** by $90^{\circ}$; draw
$V_C$ straight **down**:

$$ V_C = IX_C, \qquad X_C = \frac{1}{\omega C} $$

**Step 5 — combine the two vertical phasors.** $V_L$ points up and $V_C$ points
down along the same line, so they subtract directly:

$$ V_{LC} = V_L - V_C = I(X_L-X_C) $$

**Step 6 — add this to the horizontal phasor.** $V_{LC}$ is vertical and $V_R$ is
horizontal, so they are at right angles and the supply voltage is the hypotenuse:

$$ V^{2} = V_R^{2} + (V_L-V_C)^{2} $$

**Step 7 — substitute the three expressions for the voltages.**

$$ V^{2} = (IR)^{2} + \left[I(X_L-X_C)\right]^{2} $$

**Step 8 — take the common factor $I^{2}$ outside and square-root.**

$$ V = I\sqrt{R^{2}+(X_L-X_C)^{2}} $$

**Step 9 — divide both sides by $I$ to get the opposition.**

$$ Z = \frac{V}{I} = \sqrt{R^{2}+(X_L-X_C)^{2}} $$

**Step 10 — read the phase angle from the same triangle.** The angle between $V$ and
$I$ has the vertical side over the horizontal side as its tangent:

$$ \tan\phi = \frac{V_L-V_C}{V_R} = \frac{X_L-X_C}{R} $$

**Result.**

$$ Z = \sqrt{R^{2}+\left(\omega L-\frac{1}{\omega C}\right)^{2}} $$
$$ \tan\phi = \frac{\omega L-\dfrac{1}{\omega C}}{R}, \qquad \cos\phi = \frac{R}{Z} $$

**What it means.** The circuit behaves like a single resistor of value $Z$ as far as
the size of the current is concerned, but with a phase shift $\phi$ added. If
$X_L > X_C$, $\phi$ is positive and the current lags; if $X_C > X_L$, $\phi$ is
negative and the current leads. If $X_L = X_C$, the bracket vanishes, $Z$ falls to
its smallest possible value $R$, the current is a maximum and is in phase with the
voltage — this is **resonance**, at $f_0 = 1/2\pi\sqrt{LC}$. Note also that only $R$
appears in $\cos\phi$: the reactances shift the phase and limit the current but
never consume power.

**Conditions.** The supply must be sinusoidal and of a single frequency; $R$, $L$
and $C$ must be constant (not varying with current); the elements must be in
**series**, so that the current, not the voltage, is common; and the inductor is
assumed to have no resistance of its own — if it has, add that resistance to $R$.
:::

::: tip Examiner's note — Alternating Currents
Draw the phasor diagram with $I$ along the reference line — candidates who start
from $V$ get the lead and lag the wrong way round and lose the whole question.
Remember the mnemonic used everywhere in Nepal: in an inductor the voltage leads,
in a capacitor the current leads. Watch the units in reactance formulae:
$C$ in microfarad must become $10^{-6}\ \text{F}$ before use. When a numerical asks
for power, quote $P = VI\cos\phi$ and then **check** it against $I^{2}R$; the two
must agree, and showing the check often earns the last mark. Finally, at resonance
the voltages across $L$ and $C$ can each be many times the supply voltage — this is
a favourite "surprising" part (c) and is not an error in your arithmetic.
:::

## 3.20 Electrons

CDC allots **4 teaching hours**. The examinable core is the motion of an electron
in electric and magnetic fields, Thomson's measurement of $e/m$, Millikan's oil-drop
experiment and the definition of the electronvolt.

**Short answer questions [5 marks each]**

1. (a) Describe the motion of an electron entering a uniform electric field (i) parallel and (ii) perpendicular to the field. [3] (b) Show that the perpendicular path is a parabola. [2] <span class="marks">[5]</span> (NEB 2080)
2. (a) An electron is accelerated through a potential difference $V$. Show that its final speed is $v = \sqrt{2eV/m}$. [3] (b) Find $v$ for $V = 200\ \text{V}$. [2] <span class="marks">[5]</span> (NEB 2082)
3. (a) Show that an electron entering a uniform magnetic field at right angles moves in a circle of radius $r = mv/eB$. [3] (b) Find $r$ for $v = 8.4\times10^{6}\ \text{m s}^{-1}$ and $B = 1.0\times10^{-3}\ \text{T}$. [2] <span class="marks">[5]</span>
4. (a) Describe Thomson's experiment for the specific charge of an electron, with a labelled sketch. [3] (b) Write the expression used and state why crossed fields are needed. [2] <span class="marks">[5]</span> (NEB 2081)
5. (a) Define electronvolt and convert $1\ \text{eV}$ to joule. [2] (b) Find the kinetic energy, in joule and in eV, of an electron accelerated through $200\ \text{V}$. [3] <span class="marks">[5]</span>
6. (a) Describe Millikan's oil-drop experiment and state its conclusion. [3] (b) Write the condition for a drop to remain stationary between the plates. [2] <span class="marks">[5]</span> (NEB 2079 model)
7. (a) What is a velocity selector? Derive the condition $v = E/B$. [3] (b) Why are crossed electric and magnetic fields used in a mass spectrometer? [2] <span class="marks">[5]</span>
8. (a) Explain how an electron beam is produced and controlled in a cathode-ray oscilloscope. [3] (b) State two of its uses. [2] <span class="marks">[5]</span>

::: note Model answers — short (1–4)
**1.** (a) **(i) Parallel entry.** The force $eE$ is along the line of motion, so the electron moves in a **straight line** with uniform acceleration $a = eE/m$. If it enters against the field it decelerates uniformly, stops and returns. The speed changes but the direction does not.
**(ii) Perpendicular entry.** The force is always at right angles to the initial velocity, so the horizontal component of velocity stays constant while the vertical component grows uniformly. This is exactly the situation of a **projectile** under gravity, and the path is a **parabola**. Once the electron leaves the field region it continues in a straight line along the tangent.

(b) Let the electron enter along $x$ with speed $v$, and let the field $E$ be along $-y$, so the force on the electron (charge $-e$) is $eE$ along $+y$. The acceleration is $a = eE/m$, constant.
Horizontally, $x = vt$, so $t = x/v$.
Vertically, starting from rest in that direction,
$$ y = \frac{1}{2}at^{2} = \frac{1}{2}\cdot\frac{eE}{m}\cdot\frac{x^{2}}{v^{2}} $$
$$ y = \left(\frac{eE}{2mv^{2}}\right)x^{2} $$
Everything in the bracket is constant, so $y \propto x^{2}$, which is the equation of a **parabola** with its vertex at the point of entry.

**2.** (a) An electron of charge $e$ starting from rest and falling through a potential difference $V$ has work $eV$ done on it by the field. Since no other force acts, by the work-energy theorem all of this appears as kinetic energy:
$$ eV = \frac{1}{2}mv^{2} $$
$$ v^{2} = \frac{2eV}{m} \;\Rightarrow\; v = \sqrt{\frac{2eV}{m}} $$

(b)
$$ v = \sqrt{\frac{2\times1.6\times10^{-19}\times200}{9.1\times10^{-31}}} $$
$$ v = \sqrt{7.03\times10^{13}} = 8.4\times10^{6}\ \text{m s}^{-1} $$
(About $2.8\%$ of the speed of light, so the non-relativistic formula is safe.)

**3.** (a) A charge $e$ moving with velocity $v$ at right angles to a field $B$ feels a force
$$ F = evB $$
By Fleming's left-hand rule (or $\vec{F} = q\vec{v}\times\vec{B}$) this force is perpendicular to $\vec{v}$. A force always perpendicular to the velocity can never change the **speed** — it does no work — it only changes the direction. A constant-magnitude force always at right angles to the motion is exactly a **centripetal** force, so the path is a circle. Equating the magnetic force to the required centripetal force:
$$ evB = \frac{mv^{2}}{r} $$
$$ r = \frac{mv}{eB} $$
The period $T = 2\pi m/eB$ is independent of the speed — the principle of the cyclotron.

(b)
$$ r = \frac{9.1\times10^{-31}\times8.4\times10^{6}}{1.6\times10^{-19}\times1.0\times10^{-3}} $$
$$ r = \frac{7.64\times10^{-24}}{1.6\times10^{-22}} = 4.8\times10^{-2}\ \text{m} = 4.8\ \text{cm} $$

**4.** (a) **Thomson's apparatus.** Electrons from a hot cathode are accelerated through a potential difference $V$ towards an anode with a fine hole, which selects a narrow beam. The beam then passes between a pair of parallel plates that provide a uniform **electric** field $E$ (vertical), and through the same region a **magnetic** field $B$ is applied at right angles both to $E$ and to the beam. The beam finally strikes a fluorescent screen, where its deflection is measured.
**Procedure.** With the magnetic field off, the electric field deflects the spot. The magnetic field is then switched on and adjusted until the spot returns **exactly to its undeflected position**. At that setting the two forces balance:
$$ eE = evB \;\Rightarrow\; v = \frac{E}{B} $$
Combining this with the energy equation for the accelerating stage, $eV = \tfrac12mv^{2}$,
$$ \frac{e}{m} = \frac{v^{2}}{2V} = \frac{E^{2}}{2VB^{2}} $$
Thomson found $e/m \approx 1.76\times10^{11}\ \text{C kg}^{-1}$, the same for every gas and every cathode material — which is how he concluded that the electron is a universal constituent of all matter.

(b) See the boxed expression above. **Crossed fields are needed** because a single deflection measurement contains **two** unknowns, the speed $v$ and the ratio $e/m$, and one equation cannot give both. Balancing an electric deflection against a magnetic one removes the deflection from the problem entirely and yields $v = E/B$ by itself; only then can $e/m$ be extracted. It also makes the result independent of the length of the plates and of the exact geometry of the screen.
:::

::: note Model answers — short (5–8)
**5.** (a) One **electronvolt** is the kinetic energy gained by an electron when it is accelerated through a potential difference of one volt.
$$ 1\ \text{eV} = e\times1\ \text{V} = 1.6\times10^{-19}\ \text{J} $$
It is a convenient unit because atomic and nuclear energies are absurdly small in joules; ionisation energies are a few eV, X-ray photons a few keV, and nuclear binding energies a few MeV.

(b)
$$ KE = eV = 1.6\times10^{-19}\times200 = 3.2\times10^{-17}\ \text{J} $$
$$ KE = 200\ \text{eV} $$
(The second answer needs no calculation: an electron falling through $V$ volts gains exactly $V$ electronvolts — that is the whole point of the unit.)

**6.** (a) **Millikan's oil-drop experiment.** A fine spray of oil is blown above a pair of horizontal parallel plates; a few droplets fall through a small hole into the space between them. The droplets acquire charge by friction during spraying, or by ionisation of the air with X-rays. A single droplet is watched through a travelling microscope.
With the plates **uncharged**, the droplet falls and quickly reaches a terminal velocity $v$, at which the viscous drag balances the weight; Stokes' law then gives the radius, and hence the mass, of the droplet:
$$ 6\pi\eta rv = \frac{4}{3}\pi r^{3}(\rho-\sigma)g $$
A potential difference is then applied so that the electric force lifts the droplet, and $V$ is adjusted until the droplet hangs **stationary**.
**Conclusion.** Repeating this for hundreds of droplets, Millikan found that the charge on every droplet was a whole-number multiple of one basic amount, $1.6\times10^{-19}\ \text{C}$. Charge is therefore **quantised**, $q = ne$, and $e$ is the smallest free charge in nature. Combined with Thomson's $e/m$, this also gives the mass of the electron.

(b) For a stationary drop the upward electric force balances the weight less the upthrust of the air:
$$ \frac{qV}{d} = mg - \text{(upthrust)} = \frac{4}{3}\pi r^{3}(\rho-\sigma)g $$
where $d$ is the plate separation, $\rho$ the density of the oil and $\sigma$ that of air. In the simplified school version the upthrust is neglected and the condition is $qV/d = mg$.

**7.** (a) A **velocity selector** is an arrangement of mutually perpendicular electric and magnetic fields that allows only particles of one particular speed to pass straight through, whatever their charge or mass. A charged particle moving with speed $v$ perpendicular to both fields feels an electric force $qE$ one way and a magnetic force $qvB$ the other. It passes undeflected only if these are equal:
$$ qE = qvB \;\Rightarrow\; v = \frac{E}{B} $$
The charge $q$ cancels, so the selected speed depends only on the ratio of the field strengths. Faster particles are pushed aside by the magnetic force, slower ones by the electric force, and both are stopped by a slit.

(b) In a **mass spectrometer** the ions produced by the source emerge with a wide spread of speeds. If they were sent straight into the analysing magnetic field, the radius $r = mv/qB$ would depend on both $m$ and $v$, and ions of the same mass would arrive spread out over the detector while ions of different mass overlapped. The crossed-field velocity selector removes the speed spread first, so that every ion entering the analyser has the same $v$; then $r \propto m/q$ alone and each isotope gives a sharp, well-separated line.

**8.** (a) In a **cathode-ray oscilloscope** the electron beam is produced by an **electron gun**: a heated cathode emits electrons by thermionic emission, a cylindrical grid at a negative potential controls how many get through (this sets the **brightness**), and two anodes at high positive potential accelerate the beam and, acting as an electrostatic lens, focus it to a sharp spot (the **focus** control). The beam then passes between two pairs of deflecting plates at right angles to each other: the **Y-plates** deflect it vertically in proportion to the signal voltage applied to them, while the **X-plates** receive a sawtooth "time-base" voltage that sweeps the spot across the screen at a steady rate and flies it back. The combination traces the graph of the signal against time on a fluorescent screen, which glows where the electrons strike it. A conducting coating returns the charge and prevents the screen charging up.

(b) **Uses:** (i) to display and measure the waveform, amplitude, frequency and period of a varying voltage; (ii) to compare the phase or frequency of two signals (Lissajous figures); (iii) as a very high-resistance voltmeter that does not load the circuit; (iv) in medicine and radar, for example to display an electrocardiogram or an echo trace.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) Describe Thomson's experiment to determine the specific charge of an electron, with a labelled diagram, and derive $e/m = E^{2}/2VB^{2}$. [5] (b) Why must the electric and magnetic fields be crossed? [1] (c) In such an experiment $V = 200\ \text{V}$, the deflecting plates are $2.0\ \text{cm}$ apart with $168\ \text{V}$ across them, and a magnetic field of $1.0\times10^{-3}\ \text{T}$ just restores the undeflected spot. Find the speed of the electrons and $e/m$. [2] <span class="marks">[8]</span> (NEB 2081)
2. (a) Describe the motion of an electron entering a uniform electric field perpendicular to its velocity, and show that the path is a parabola. [3] (b) Show that an electron entering a uniform magnetic field at right angles moves in a circle of radius $r = mv/eB$, and that its period is independent of its speed. [3] (c) An electron is accelerated through $200\ \text{V}$ and then enters a field of $1.0\times10^{-3}\ \text{T}$ at right angles. Find its speed and the radius of its path, taking $e/m = 1.76\times10^{11}\ \text{C kg}^{-1}$. [2] <span class="marks">[8]</span> (NEB 2082)
3. (a) Describe Millikan's oil-drop experiment and explain how it shows that charge is quantised. [4] (b) What is a velocity selector? Derive $v = E/B$ and state one use. [2] (c) Define the electronvolt, convert it to joule, and find the kinetic energy in joule and in eV of an electron accelerated through $200\ \text{V}$. [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Apparatus.** Electrons emitted thermionically from a hot cathode are accelerated towards a perforated anode by a potential difference $V$; the hole selects a narrow beam. The beam passes between two horizontal parallel plates that provide a uniform **electric field** $E = V_p/d$, and a pair of coils provides a uniform **magnetic field** $B$ over the same region, at right angles both to $E$ and to the beam. The beam finally strikes a fluorescent screen, where the position of the spot is read off a scale. The whole tube is highly evacuated.
**Derivation.** In the accelerating stage all the work done on the electron becomes kinetic energy:
$$ eV = \frac{1}{2}mv^{2} $$
In the deflecting region the electric force is $eE$ and the magnetic force is $evB$, and they are arranged to act in opposite directions. The magnetic field is adjusted until the spot returns **exactly** to its undeflected position, at which setting
$$ eE = evB $$
The charge $e$ cancels from both sides, so
$$ v = \frac{E}{B} $$
Returning to the energy equation and dividing both sides by $mV$,
$$ \frac{e}{m} = \frac{v^{2}}{2V} $$
Substituting $v = E/B$,
$$ \frac{e}{m} = \frac{E^{2}}{2VB^{2}} \approx 1.76\times10^{11}\ \text{C kg}^{-1} $$
Thomson found the same value whatever gas filled the tube and whatever metal formed the cathode — proof that this particle is a constituent of **all** matter.

(b) Because one deflection measurement contains **two** unknowns, $v$ and $e/m$, and a single equation cannot determine both. Balancing an electric deflection against a magnetic one removes the deflection from the problem altogether and gives $v = E/B$ on its own; only then can $e/m$ be found. The null method is also far more accurate than measuring a deflection, and it makes the answer independent of the exact length of the plates and of the distance to the screen.

(c)
$$ E = \frac{V_p}{d} = \frac{168}{2.0\times10^{-2}} = 8.4\times10^{3}\ \text{V m}^{-1} $$
$$ v = \frac{E}{B} = \frac{8.4\times10^{3}}{1.0\times10^{-3}} = 8.4\times10^{6}\ \text{m s}^{-1} $$
$$ \frac{e}{m} = \frac{v^{2}}{2V} = \frac{(8.4\times10^{6})^{2}}{2\times200} = \frac{7.056\times10^{13}}{400} $$
$$ \frac{e}{m} = 1.76\times10^{11}\ \text{C kg}^{-1} $$
**Check:** this agrees with the accepted value, and $v/c = 0.028$, so the non-relativistic treatment is justified. ✓

**2.** (a) Let the electron enter along the $x$-axis with speed $v$, and let a uniform field $E$ act at right angles to it. The force $eE$ is constant in size and direction and acts only along $y$, so the motion splits into two independent parts: **uniform velocity** along $x$ and **uniform acceleration** $a = eE/m$ along $y$. This is exactly the situation of a projectile.
Along $x$: $\quad x = vt \;\Rightarrow\; t = x/v$.
Along $y$, starting from rest in that direction:
$$ y = \frac{1}{2}at^{2} = \frac{1}{2}\cdot\frac{eE}{m}\cdot\frac{x^{2}}{v^{2}} $$
$$ y = \left(\frac{eE}{2mv^{2}}\right)x^{2} $$
The bracket is a constant, so $y \propto x^{2}$ — a **parabola**, with its vertex at the point of entry. Once the electron leaves the plates no force acts, so it travels on in a straight line along the tangent to the parabola at the exit point. Note that the **speed changes**, because the electric force does work on the electron.

(b) In a magnetic field the force on a charge moving at right angles to $\vec{B}$ is
$$ F = evB $$
and, by $\vec{F} = q\vec{v}\times\vec{B}$, it is always perpendicular to $\vec{v}$. A force perpendicular to the velocity does **no work**, so the speed never changes; it only turns the velocity. A force of constant magnitude always perpendicular to the motion is precisely a centripetal force, so the path is a **circle**. Equating:
$$ evB = \frac{mv^{2}}{r} \;\Rightarrow\; r = \frac{mv}{eB} $$
The period is the circumference divided by the speed:
$$ T = \frac{2\pi r}{v} = \frac{2\pi}{v}\cdot\frac{mv}{eB} = \frac{2\pi m}{eB} $$
The $v$ cancels, so $T$ is **independent of the speed** (and of the radius): a faster electron simply travels round a proportionately larger circle in the same time. This is the principle on which the cyclotron works, since a fixed-frequency accelerating voltage stays in step with the particles as they gain energy.

(c)
$$ v = \sqrt{2\left(\frac{e}{m}\right)V} = \sqrt{2\times1.76\times10^{11}\times200} $$
$$ v = \sqrt{7.04\times10^{13}} = 8.4\times10^{6}\ \text{m s}^{-1} $$
$$ r = \frac{mv}{eB} = \frac{v}{(e/m)B} = \frac{8.4\times10^{6}}{1.76\times10^{11}\times1.0\times10^{-3}} $$
$$ r = \frac{8.4\times10^{6}}{1.76\times10^{8}} = 4.8\times10^{-2}\ \text{m} = 4.8\ \text{cm} $$

**3.** (a) **Millikan's oil-drop experiment.** Oil is sprayed as a fine mist above two horizontal parallel metal plates; a few droplets drift through a small hole into the space between them. The spraying, or a beam of X-rays, leaves each droplet with a small charge. One droplet is watched through a travelling microscope with a calibrated eyepiece scale, and the space is illuminated from the side and kept at constant temperature.
**Stage 1 — find the mass.** With the plates **uncharged**, the droplet falls and quickly reaches a terminal velocity $v$, at which the viscous drag given by Stokes' law balances the weight less the upthrust:
$$ 6\pi\eta rv = \frac{4}{3}\pi r^{3}(\rho-\sigma)g $$
Measuring $v$ gives the radius $r$ and hence the mass of the droplet.
**Stage 2 — balance it.** A potential difference $V$ is now applied so that the electric force is upward, and $V$ is adjusted until the droplet hangs **stationary**:
$$ \frac{qV}{d} = \frac{4}{3}\pi r^{3}(\rho-\sigma)g $$
from which the charge $q$ is calculated.
**Conclusion.** Repeating this for hundreds of droplets, and changing the charge on a droplet by irradiating it, Millikan found that **every** value of $q$ was a whole-number multiple of one basic quantity:
$$ q = ne, \qquad e = 1.6\times10^{-19}\ \text{C} $$
No droplet ever carried a fraction of it. Electric charge is therefore **quantised**, and $e$ is its indivisible unit. Combined with Thomson's $e/m$, this gives the mass of the electron, $9.1\times10^{-31}\ \text{kg}$.

(b) A **velocity selector** is a region of mutually perpendicular electric and magnetic fields through which only particles of one particular speed can pass undeflected. A particle of charge $q$ and speed $v$ moving perpendicular to both fields feels an electric force $qE$ and a magnetic force $qvB$ in opposite directions; it goes straight only if
$$ qE = qvB \;\Rightarrow\; v = \frac{E}{B} $$
The charge and the mass both cancel, so the selected speed depends only on the ratio of the field strengths. **Use:** it is placed in front of the analysing magnet of a **mass spectrometer**, so that all the ions entering the analyser have the same speed; then the radius $r = mv/qB$ depends on $m/q$ alone and each isotope gives a sharp, separate line.

(c) One **electronvolt** is the kinetic energy acquired by an electron in falling freely through a potential difference of one volt:
$$ 1\ \text{eV} = 1.6\times10^{-19}\ \text{C}\times1\ \text{V} = 1.6\times10^{-19}\ \text{J} $$
For an electron accelerated through $200\ \text{V}$:
$$ KE = eV = 1.6\times10^{-19}\times200 = 3.2\times10^{-17}\ \text{J} $$
$$ KE = 200\ \text{eV} $$
:::

::: derivation Thomson's measurement of the specific charge $e/m$
We want the ratio of the charge of an electron to its mass, measured without
knowing either separately.

**Setting up.** Electrons leave a hot cathode with negligible speed and are
accelerated through a potential difference $V$ to form a narrow beam. The beam then
crosses a region in which an electric field $E$ (from parallel plates) and a
magnetic field $B$ act at right angles to each other and to the beam. The beam
finally hits a fluorescent screen, where the position of the spot is observed.

**Step 1 — write the energy gained in the accelerating stage.** The work done by the
field on a charge $e$ falling through $V$ becomes kinetic energy:

$$ eV = \frac{1}{2}mv^{2} $$

**Step 2 — write the electric force in the deflecting region.** The plates produce a
uniform field $E$, so the force on the electron is

$$ F_E = eE $$

**Step 3 — write the magnetic force.** The electron moves at right angles to $B$, so

$$ F_B = evB $$

**Step 4 — adjust $B$ until the spot returns to its undeflected position.** When the
spot is back where it started, the two forces must be equal and opposite:

$$ eE = evB $$

**Step 5 — cancel $e$ from both sides and solve for the speed.** The charge appears
on both sides, so it cancels completely:

$$ v = \frac{E}{B} $$

This is the key measurement: the speed of the electrons is now known from two
laboratory quantities alone.

**Step 6 — return to the energy equation and make $e/m$ the subject.** Divide both
sides of Step 1 by $mV$:

$$ \frac{e}{m} = \frac{v^{2}}{2V} $$

**Step 7 — substitute the speed found in Step 5.**

$$ \frac{e}{m} = \frac{1}{2V}\left(\frac{E}{B}\right)^{2} $$

**Result.**

$$ \frac{e}{m} = \frac{E^{2}}{2VB^{2}} \approx 1.76\times10^{11}\ \text{C kg}^{-1} $$

**What it means.** Every quantity on the right — the plate voltage that fixes $E$,
the current in the coils that fixes $B$, and the accelerating voltage $V$ — is
measurable on the bench, so $e/m$ is obtained without ever isolating a single
electron. Thomson's crucial finding was that the **same** value came out whatever
gas filled the tube and whatever metal the cathode was made of. That universality
showed that these particles are a common constituent of all atoms, and since $e/m$
is about $1836$ times larger than that of a hydrogen ion, the particle is either
very light or very highly charged. Millikan's later measurement of $e$ settled the
question in favour of a very small mass, $m = 9.1\times10^{-31}\ \text{kg}$.

**Conditions.** The electrons must start effectively from rest, so that all their
energy comes from $V$; the fields must be uniform and confined to the same region;
the speed must be well below the speed of light, or the relativistic increase of
mass makes the measured $e/m$ come out too small; and the tube must be highly
evacuated so that the beam is not scattered by gas molecules.
:::

::: tip Examiner's note — Electrons
The two "$\sqrt{\ }$ formulae" — $v = \sqrt{2eV/m}$ from energy and $r = mv/eB$
from circular motion — between them solve almost every numerical in this unit;
memorise where each comes from, not just its form. When you write Thomson's method,
the marks are for the **balancing** step: say explicitly that $B$ is adjusted until
the spot returns to its original place, then that $e$ cancels to give $v = E/B$.
Do not confuse electric deflection (parabolic path, speed changes) with magnetic
deflection (circular path, speed constant) — a common and expensive error. And keep
the electronvolt straight: an electron through $500\ \text{V}$ gains
$500\ \text{eV}$, full stop.
:::

## 3.21 Photons

CDC allots **3 teaching hours**. Small but very reliable: Einstein's photoelectric
equation, the laws of photoelectric emission, threshold frequency, stopping
potential and the energy and momentum of a photon.

**Short answer questions [5 marks each]**

1. (a) What is a photon? State four of its properties. [3] (b) Find the energy of a photon of wavelength $400\ \text{nm}$ in joule and in eV. [2] <span class="marks">[5]</span> (NEB 2080)
2. (a) State the laws of photoelectric emission. [3] (b) Which of them cannot be explained by the wave theory of light, and why? [2] <span class="marks">[5]</span> (NEB 2082)
3. (a) Write Einstein's photoelectric equation and explain each term. [3] (b) Define work function, threshold frequency and threshold wavelength. [2] <span class="marks">[5]</span> (NEB 2081)
4. (a) Define stopping potential and show that $eV_s = h\nu - W$. [3] (b) Light of wavelength $400\ \text{nm}$ falls on a metal of work function $2.0\ \text{eV}$; find the stopping potential. [2] <span class="marks">[5]</span> (NEB 2079 model)
5. (a) Sketch the graph of stopping potential against frequency and explain how $h$ and $W$ are obtained from it. [3] (b) What does the intercept on the frequency axis represent? [2] <span class="marks">[5]</span>
6. (a) Find the threshold wavelength of a metal whose work function is $2.0\ \text{eV}$. [2] (b) Will red light of wavelength $700\ \text{nm}$ eject electrons from it? Justify. [3] <span class="marks">[5]</span>
7. (a) Show that the momentum of a photon is $h/\lambda$. [2] (b) How many photons of wavelength $500\ \text{nm}$ does a $1.0\ \text{W}$ lamp emit per second, assuming all the energy goes into light? [3] <span class="marks">[5]</span>
8. (a) Explain how the photoelectric effect demonstrates the particle nature of light. [3] (b) Give two practical applications of photoelectric cells. [2] <span class="marks">[5]</span>

::: note Model answers — short (1–4)
**1.** (a) A **photon** is the quantum, or smallest indivisible packet, of electromagnetic radiation: light of frequency $\nu$ can be emitted or absorbed only in whole units of energy $h\nu$.
**Properties:** (i) its energy is $E = h\nu = hc/\lambda$, fixed entirely by the frequency and independent of the intensity; (ii) it has **zero rest mass** and always travels at $c$ in vacuum; (iii) it carries momentum $p = E/c = h/\lambda$ even though it has no rest mass; (iv) it is **electrically neutral**, so it is undeflected by electric and magnetic fields; (v) the intensity of a beam is the **number** of photons crossing unit area per second, not the energy of each; (vi) in an interaction with an electron, the photon is absorbed **whole** — it cannot give up part of itself.

(b)
$$ E = \frac{hc}{\lambda} = \frac{6.63\times10^{-34}\times3\times10^{8}}{400\times10^{-9}} $$
$$ E = 4.97\times10^{-19}\ \text{J} $$
$$ E = \frac{4.97\times10^{-19}}{1.6\times10^{-19}} = 3.11\ \text{eV} $$

**2.** (a) **Laws of photoelectric emission.** (i) For a given metal and a given frequency, the number of photoelectrons emitted per second (the photoelectric current) is directly proportional to the **intensity** of the incident light. (ii) For every metal there is a minimum frequency, the **threshold frequency** $\nu_0$, below which no emission occurs however intense the light or however long it shines. (iii) The **maximum kinetic energy** of the emitted electrons depends only on the **frequency** of the light and on the metal, and is completely independent of the intensity. (iv) Emission is **instantaneous** — within about $10^{-9}\ \text{s}$ of the light arriving — even for very feeble light.

(b) Laws **(ii), (iii) and (iv)** defeat the wave theory.
On the wave picture, light energy arrives spread continuously over the whole surface, and an electron absorbs it gradually. Then: **(ii)** any frequency should eventually work, provided the light is intense enough or is left on long enough, so there should be no threshold at all; **(iii)** a more intense wave carries a larger electric field, so it should shake the electrons harder and eject them with more energy — the maximum kinetic energy should depend on intensity, and should not depend on colour; **(iv)** with very weak light an electron would need minutes or hours to collect enough energy from the spread-out wave, so emission should be delayed, not instantaneous.
Experiment contradicts all three. Einstein's resolution is that light arrives as **individual photons** of energy $h\nu$, and one electron absorbs one whole photon in a single event.

**3.** (a) **Einstein's photoelectric equation:**
$$ h\nu = W + \frac{1}{2}mv_{max}^{2} $$
$h\nu$ is the energy of the single incident photon, which is absorbed completely by one electron. $W$ is the **work function** of the metal, the least energy needed to free an electron from the surface. $\tfrac12mv_{max}^{2}$ is the maximum kinetic energy with which the electron emerges — it is a *maximum* because electrons that come from below the surface lose extra energy in collisions on the way out. Using $W = h\nu_0$, the equation may be written
$$ \frac{1}{2}mv_{max}^{2} = h(\nu-\nu_0) $$
which shows at once why no emission is possible for $\nu < \nu_0$: the kinetic energy would have to be negative.

(b) **Work function** $W$ is the minimum energy required to remove an electron from the surface of a metal, usually quoted in eV. **Threshold frequency** $\nu_0 = W/h$ is the lowest frequency of light that can just cause emission, with the electron leaving with zero speed. **Threshold wavelength** $\lambda_0 = hc/W = c/\nu_0$ is the corresponding longest wavelength; light of wavelength greater than $\lambda_0$ can never eject electrons from that metal.

**4.** (a) The **stopping potential** $V_s$ is the least negative potential that must be applied to the collecting anode to stop even the fastest photoelectron from reaching it, so that the photoelectric current falls to exactly zero.
An electron of charge $e$ moving against a retarding potential $V_s$ loses kinetic energy $eV_s$. The fastest electron is just stopped when
$$ eV_s = \frac{1}{2}mv_{max}^{2} $$
Substituting this into Einstein's equation $h\nu = W + \tfrac12mv_{max}^{2}$,
$$ h\nu = W + eV_s \;\Rightarrow\; eV_s = h\nu - W $$
$$ V_s = \frac{h}{e}\nu - \frac{W}{e} $$

(b) Photon energy at $400\ \text{nm}$ is $3.11\ \text{eV}$ (from question 1), so
$$ eV_s = h\nu - W = 3.11 - 2.0 = 1.11\ \text{eV} $$
$$ V_s = 1.11\ \text{V} $$
:::

::: note Model answers — short (5–8)
**5.** (a) From $V_s = (h/e)\nu - W/e$, a graph of stopping potential against frequency is a **straight line**. It does not pass through the origin: it meets the $\nu$-axis at $\nu_0$ and, if extended backwards, meets the $V_s$-axis at $-W/e$.
- The **slope** is $h/e$. Measuring the slope and multiplying by the known $e$ gives **Planck's constant**: $h = e\times\text{slope}$. This is how Millikan measured $h$ in 1916, and it agreed with the value from black-body radiation.
- The **intercept on the $V_s$-axis** is $-W/e$, so $W = e\times|\text{intercept}|$.
A striking feature is that the line has the **same slope for every metal**; changing the metal only shifts the line sideways. That universality is strong evidence that $h$ is a constant of nature, not a property of the material.

(b) The intercept on the frequency axis is the **threshold frequency** $\nu_0$ of that metal — the frequency at which the stopping potential is zero, meaning the electrons just barely escape with no kinetic energy. It is related to the work function by $W = h\nu_0$.

**6.** (a)
$$ \lambda_0 = \frac{hc}{W} = \frac{6.63\times10^{-34}\times3\times10^{8}}{2.0\times1.6\times10^{-19}} $$
$$ \lambda_0 = \frac{1.989\times10^{-25}}{3.2\times10^{-19}} = 6.2\times10^{-7}\ \text{m} = 622\ \text{nm} $$

(b) **No.** The incident wavelength $700\ \text{nm}$ is **greater** than the threshold wavelength $622\ \text{nm}$, so its frequency is below $\nu_0$. Checking directly, the photon energy is
$$ E = \frac{hc}{\lambda} = \frac{1.989\times10^{-25}}{700\times10^{-9}} = 2.84\times10^{-19}\ \text{J} = 1.78\ \text{eV} $$
which is less than the work function $2.0\ \text{eV}$. A single photon cannot free an electron, and since an electron absorbs only one photon at a time, no amount of extra intensity and no length of exposure will help — increasing the intensity merely sends more photons, each still too weak.

**7.** (a) A photon has zero rest mass, so the relativistic energy-momentum relation $E^{2} = p^{2}c^{2}+m_0^{2}c^{4}$ reduces to $E = pc$. Hence
$$ p = \frac{E}{c} = \frac{h\nu}{c} = \frac{h}{\lambda} $$
(Equivalently, using the equivalent mass $m = E/c^{2} = h\nu/c^{2}$ and $p = mc$ gives the same result.) The existence of this momentum is confirmed by radiation pressure, by the Compton effect and by the tails of comets, which are pushed away from the Sun.

(b) Energy of one photon:
$$ E = \frac{hc}{\lambda} = \frac{1.989\times10^{-25}}{500\times10^{-9}} = 3.98\times10^{-19}\ \text{J} $$
Number emitted per second:
$$ n = \frac{P}{E} = \frac{1.0}{3.98\times10^{-19}} = 2.5\times10^{18}\ \text{s}^{-1} $$
The number is enormous, which is exactly why the graininess of light is never noticed in everyday life.

**8.** (a) The photoelectric effect shows three things a wave cannot do. **(i) The threshold.** If the energy of a wave were spread out, faint red light shining for long enough would accumulate enough energy to free an electron; in fact red light never works on a metal whose threshold lies in the green, however bright. This is only sensible if the energy comes in indivisible lumps of size $h\nu$, and a single lump must be big enough by itself. **(ii) Energy depends on colour, not brightness.** Doubling the intensity doubles the **number** of electrons but leaves their maximum energy exactly unchanged; changing the colour changes the energy. So each electron deals with one photon, and the photon's energy is fixed by $\nu$. **(iii) No time delay.** Even at intensities so low that classical theory predicts an hour's wait, the first electrons appear within nanoseconds — because the energy is delivered in a single concentrated event, not gathered gradually.
Together these force the picture of light as a stream of **particles**, each carrying energy $h\nu$ and momentum $h/\lambda$. (Interference and diffraction equally force the wave picture, and both are true: this is wave-particle duality.)

(b) **Applications:** (i) in **photocells** used for automatic street lighting, burglar alarms, automatic doors and counting devices on production lines; (ii) in **light meters** for photography and in solar cells for electrical power; (iii) in the **sound track** of film projectors, where the varying light through the track becomes a varying current; (iv) in **photomultiplier tubes** for detecting very faint light in astronomy and in nuclear particle detectors; (v) in television camera tubes and image intensifiers for night vision.
:::

**Long answer / numerical questions [8 marks each]**

1. (a) State the laws of photoelectric emission and explain which of them the wave theory fails to account for. [4] (b) Derive Einstein's photoelectric equation and define work function and threshold frequency. [2] (c) Light of wavelength $400\ \text{nm}$ falls on a metal of work function $2.0\ \text{eV}$. Find the photon energy in eV, the maximum kinetic energy of the photoelectrons, the stopping potential and the threshold wavelength. [2] <span class="marks">[8]</span> (NEB 2081)
2. (a) Define stopping potential and show that $V_s = (h/e)\nu - W/e$. [3] (b) Sketch $V_s$ against $\nu$ for two different metals and explain how $h$ and $W$ are found from the graph. [3] (c) A metal has $\nu_0 = 5.0\times10^{14}\ \text{Hz}$; find its work function in eV. [2] <span class="marks">[8]</span> (NEB 2079 model)
3. (a) What is a photon? Derive expressions for its energy, equivalent mass and momentum. [4] (b) Explain wave-particle duality and state de Broglie's hypothesis. [2] (c) A $1.0\ \text{W}$ source emits light of wavelength $500\ \text{nm}$. Find the photon energy and the number of photons emitted per second. [2] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) The four laws are as stated in short answer 2(a): current proportional to intensity; a threshold frequency below which nothing happens; maximum kinetic energy determined by frequency alone; and instantaneous emission.
**The wave theory explains only the first.** It fails on the other three. A wave delivers energy continuously and over the whole illuminated area, so (i) there should be no threshold — low-frequency light, made intense enough or left on long enough, should always work; (ii) a more intense wave has a larger amplitude and therefore a larger electric field, so it should give the ejected electrons **more** kinetic energy, whereas experiment shows the maximum energy is completely independent of intensity and rises only with frequency; (iii) with a very feeble beam an electron would have to collect energy for minutes, so there should be a measurable delay, but none is found.

(b) **Derivation.** Einstein assumed that light of frequency $\nu$ consists of photons of energy $h\nu$, and that a photoelectron absorbs **one whole photon** in a single act. The energy so received is spent in two ways: a minimum amount $W$ must be spent in freeing the electron from the attraction of the metal surface, and whatever remains appears as kinetic energy. For an electron that happens to be right at the surface and loses nothing on the way out, the remainder is a maximum:
$$ h\nu = W + \frac{1}{2}mv_{max}^{2} $$
**Work function** $W$ is the minimum energy needed to liberate an electron from the metal surface. **Threshold frequency** $\nu_0$ is the frequency for which $h\nu_0 = W$ exactly, so the electron just escapes with zero kinetic energy; with $W = h\nu_0$,
$$ \frac{1}{2}mv_{max}^{2} = h(\nu-\nu_0) $$
For $\nu < \nu_0$ the right-hand side is negative, which is impossible — hence no emission at all, at any intensity.

(c)
$$ E = \frac{hc}{\lambda} = \frac{6.63\times10^{-34}\times3\times10^{8}}{400\times10^{-9}} = 4.97\times10^{-19}\ \text{J} $$
$$ E = \frac{4.97\times10^{-19}}{1.6\times10^{-19}} = 3.11\ \text{eV} $$
$$ KE_{max} = E - W = 3.11-2.0 = 1.11\ \text{eV} = 1.77\times10^{-19}\ \text{J} $$
$$ V_s = \frac{KE_{max}}{e} = 1.11\ \text{V} $$
$$ \lambda_0 = \frac{hc}{W} = \frac{1.989\times10^{-25}}{3.2\times10^{-19}} = 6.2\times10^{-7}\ \text{m} = 622\ \text{nm} $$
**Check:** $622\ \text{nm} > 400\ \text{nm}$, so the incident light is indeed energetic enough — consistent with a positive $KE_{max}$. ✓

**2.** (a) The **stopping potential** $V_s$ is the smallest retarding potential difference applied to the anode that reduces the photoelectric current to zero, by turning back even the fastest electron. As an electron of charge $e$ climbs through a retarding potential $V_s$ it loses energy $eV_s$; the fastest electron is just brought to rest when
$$ eV_s = \frac{1}{2}mv_{max}^{2} $$
Einstein's equation is
$$ h\nu = W + \frac{1}{2}mv_{max}^{2} = W + eV_s $$
Rearranging for $V_s$ and dividing throughout by $e$:
$$ V_s = \frac{h}{e}\nu - \frac{W}{e} $$

(b) This is of the form $y = mx+c$, so the graph of $V_s$ against $\nu$ is a straight line of **slope $h/e$** and **intercept $-W/e$** on the $V_s$-axis, cutting the $\nu$-axis at $\nu_0 = W/h$. For two metals $A$ and $B$ with $W_A < W_B$, the lines are **parallel** (same slope $h/e$), with $B$'s line displaced to the right and its threshold frequency larger.
- **To find $h$:** measure the slope of either line and multiply by $e$; $h = e\times\text{slope}$.
- **To find $W$:** read the intercept on the $V_s$ axis and multiply by $e$, $W = e\times|{-W/e}|$; or read $\nu_0$ from the $\nu$-axis and use $W = h\nu_0$.
The fact that both lines have the same slope, whatever the metal, is direct experimental proof that $h$ is a universal constant.

(c)
$$ W = h\nu_0 = 6.63\times10^{-34}\times5.0\times10^{14} = 3.32\times10^{-19}\ \text{J} $$
$$ W = \frac{3.32\times10^{-19}}{1.6\times10^{-19}} = 2.07\ \text{eV} $$

**3.** (a) A **photon** is the quantum of electromagnetic radiation — the smallest indivisible packet in which light of a given frequency can be emitted or absorbed.
**Energy.** Planck's hypothesis, which Einstein extended to free radiation, gives
$$ E = h\nu = \frac{hc}{\lambda} $$
**Equivalent mass.** A photon has **zero rest mass**, but it carries energy, and by Einstein's mass-energy relation $E = mc^{2}$ this energy is equivalent to a mass
$$ m = \frac{E}{c^{2}} = \frac{h\nu}{c^{2}} = \frac{h}{\lambda c} $$
This is the mass that makes light bend in a gravitational field.
**Momentum.** Since the photon travels at $c$,
$$ p = mc = \frac{h\nu}{c^{2}}\cdot c = \frac{h\nu}{c} = \frac{h}{\lambda} $$
The same result follows from the relativistic relation $E = pc$ for a massless particle. Photon momentum is real and measurable: it produces radiation pressure, drives comet tails away from the Sun, and shows up quantitatively in the Compton effect.

(b) **Wave-particle duality** is the principle that radiation and matter both show wave behaviour in some experiments and particle behaviour in others, and that neither picture alone is complete. Light diffracts and interferes (Young's slits, gratings, thin films) — purely wave behaviour; yet it shows a photoelectric threshold and Compton scattering — purely particle behaviour. The two never appear in the same measurement, so there is no contradiction; which face shows depends on what you ask of the light.
**de Broglie's hypothesis** extends the symmetry to matter: every moving particle has an associated wave of wavelength
$$ \lambda = \frac{h}{p} = \frac{h}{mv} $$
For everyday objects $\lambda$ is unimaginably small ($10^{-34}\ \text{m}$ for a cricket ball) and no wave effect is seen, but for an electron accelerated through $100\ \text{V}$ it is about $1.2\times10^{-10}\ \text{m}$ — comparable with atomic spacings, which is why electrons are diffracted by crystals (Davisson and Germer) and why the electron microscope works.

(c)
$$ E = \frac{hc}{\lambda} = \frac{6.63\times10^{-34}\times3\times10^{8}}{500\times10^{-9}} = 3.98\times10^{-19}\ \text{J} $$
$$ E = 2.49\ \text{eV} $$
$$ n = \frac{P}{E} = \frac{1.0}{3.98\times10^{-19}} = 2.5\times10^{18}\ \text{photons per second} $$
:::

::: derivation Einstein's photoelectric equation
We want a relation between the colour of the light, the metal, and the speed of the
fastest electron that comes off.

**Setting up.** Light of frequency $\nu$ falls on a clean metal surface in a vacuum.
Einstein made two assumptions: that the light arrives as separate photons, each
carrying energy $h\nu$; and that one photoelectron absorbs **one complete photon**,
never a part of one and never two at once.

**Step 1 — write the energy the electron receives.** The whole photon is absorbed,
so the electron gains

$$ E_{in} = h\nu $$

**Step 2 — subtract the price of escaping.** An electron inside the metal is held
there by the attraction of the positive ions. The least energy that any electron
must pay to get out through the surface is the work function $W$. So the energy left
over is

$$ E_{left} = h\nu - W $$

**Step 3 — recognise that most electrons pay more than the minimum.** An electron
starting below the surface loses extra energy in collisions on its way out, so it
emerges with less than $E_{left}$. Only an electron right at the surface, losing
nothing on the way, keeps all of it. That electron is the fastest one:

$$ \frac{1}{2}mv_{max}^{2} = h\nu - W $$

**Step 4 — write it in the standard form.** Move $W$ to the other side:

$$ h\nu = W + \frac{1}{2}mv_{max}^{2} $$

**Step 5 — express the work function as a frequency.** Define the threshold
frequency $\nu_0$ as the frequency of the photon whose energy is exactly $W$:

$$ W = h\nu_0 $$

**Step 6 — substitute this into Step 3.**

$$ \frac{1}{2}mv_{max}^{2} = h\nu - h\nu_0 = h(\nu-\nu_0) $$

**Step 7 — connect to the stopping potential.** The fastest electron is just turned
back by a retarding potential $V_s$ when the work done against it equals that
kinetic energy:

$$ eV_s = h\nu - W $$

**Step 8 — divide by $e$ to get a straight-line form.**

$$ V_s = \frac{h}{e}\nu - \frac{W}{e} $$

**Result.**

$$ h\nu = W + \frac{1}{2}mv_{max}^{2}, \qquad V_s = \frac{h}{e}\nu - \frac{W}{e} $$

**What it means.** Every puzzling feature of photoelectric emission drops out of this
one line. If $\nu < \nu_0$ the right-hand side of Step 6 is negative, which is
impossible for a kinetic energy, so **no electrons come off at all** — that is the
threshold. Making the light brighter sends **more** photons, so more electrons are
released and the current grows, but each photon still carries the same $h\nu$, so
the maximum kinetic energy does not change. The energy arrives in one concentrated
event rather than being gathered slowly, so emission is **instantaneous**. And the
graph of $V_s$ against $\nu$ must be a straight line of slope $h/e$, the same for
every metal — which is how Planck's constant was measured from a photocell.

**Conditions.** The surface must be clean and in a vacuum, since a layer of oxide or
grease changes $W$; the equation is non-relativistic, so it fails for very energetic
photons; and it assumes single-photon absorption, which breaks down only at laser
intensities, where two-photon processes become possible.
:::

::: tip Examiner's note — Photons
Convert to electronvolts early and stay there: $E(\text{eV}) = 1242/\lambda(\text{nm})$
is worth memorising as a check, and it makes $KE_{max} = E - W$ a one-line
subtraction. Always say that **one electron absorbs one whole photon** — that single
sentence is what makes the threshold and the instantaneous emission intelligible,
and examiners look for it. Keep the three "independent of intensity" facts
separate from the one fact that *is* proportional to intensity (the current).
In graph questions, label the slope $h/e$ and the intercepts $-W/e$ and $\nu_0$,
and remember that lines for different metals are **parallel**.
:::

## 3.22 Semiconductor devices

CDC allots **6 teaching hours**. Intrinsic and extrinsic semiconductors, the p-n
junction and its biasing, half-wave and full-wave rectification, the transistor and
its characteristics and gain, and the basic logic gates are all examinable; this
unit supplies a Group C question most years.

**Short answer questions [5 marks each]**

1. (a) Distinguish between conductors, semiconductors and insulators using energy-band diagrams. [3] (b) Why does the resistance of a semiconductor fall as temperature rises? [2] <span class="marks">[5]</span> (NEB 2080)
2. (a) Distinguish between intrinsic and extrinsic semiconductors. [2] (b) Explain n-type and p-type doping with examples, and state the majority and minority carriers in each. [3] <span class="marks">[5]</span> (NEB 2082)
3. (a) Explain the formation of the depletion layer and the potential barrier in a p-n junction. [3] (b) Compare the width of the depletion layer under forward and reverse bias. [2] <span class="marks">[5]</span> (NEB 2081)
4. (a) Draw the V-I characteristic of a p-n junction diode in forward and reverse bias. [3] (b) Define knee voltage and breakdown voltage. [2] <span class="marks">[5]</span>
5. (a) Explain half-wave rectification with a circuit diagram and output waveform. [3] (b) Why is full-wave rectification preferred? [2] <span class="marks">[5]</span> (NEB 2079 model)
6. (a) Explain full-wave rectification using a centre-tapped transformer. [3] (b) If the input frequency is $50\ \text{Hz}$, what is the ripple frequency for half-wave and for full-wave rectification? [2] <span class="marks">[5]</span>
7. (a) Describe the structure of an n-p-n transistor and explain why the base is thin and lightly doped. [3] (b) Write the relation between $I_E$, $I_B$ and $I_C$. [2] <span class="marks">[5]</span> (NEB 2082 model)
8. (a) Define $\alpha$ and $\beta$ for a transistor and show that $\beta = \alpha/(1-\alpha)$. [3] (b) A transistor has $\beta = 100$ and $I_B = 50\ \mu\text{A}$; find $I_C$, $I_E$ and $\alpha$. [2] <span class="marks">[5]</span>
9. (a) Draw the symbols and truth tables of the OR, AND and NOT gates. [3] (b) Show that a NAND gate followed by a NOT gate gives an AND gate. [2] <span class="marks">[5]</span>

::: note Model answers — short (1–5)
**1.** (a) In a solid the allowed electron energies form **bands**. The highest band that is full at absolute zero is the **valence band**; the next empty one is the **conduction band**; the gap between them is the **forbidden energy gap** $E_g$.
- **Conductor:** the valence and conduction bands **overlap** (or the valence band is only half full), so $E_g = 0$. Electrons can move into unoccupied levels under the smallest field, and conductivity is very high. Example: copper.
- **Semiconductor:** the bands are separated by a **small** gap, about $1.1\ \text{eV}$ in silicon and $0.72\ \text{eV}$ in germanium. At $0\ \text{K}$ it is an insulator, but at room temperature thermal energy lifts a few electrons across, leaving holes behind, so it conducts feebly.
- **Insulator:** the gap is **large**, $5\ \text{eV}$ or more (diamond $\approx6\ \text{eV}$). Thermal energy at room temperature ($\approx0.026\ \text{eV}$) cannot lift electrons across, so the conduction band stays empty and no current flows.

(b) A metal has a fixed number of free electrons; heating it only increases the lattice vibrations, which scatter the electrons more, so its resistance **rises**. A semiconductor is different: at higher temperature many more electron-hole pairs are created by thermal excitation across the small gap, so the number of charge carriers $n$ increases **exponentially**. This gain in carrier number far outweighs the loss in mobility due to increased scattering, so the conductivity rises and the resistance falls. Semiconductors therefore have a **negative temperature coefficient** of resistance — the basis of the thermistor.

**2.** (a) An **intrinsic** semiconductor is a pure specimen — pure silicon or germanium with no added impurity. Its conduction is due entirely to thermally generated electron-hole pairs, so $n_e = n_h$, and its conductivity is small and depends only on temperature. An **extrinsic** semiconductor has a controlled impurity deliberately added ("doping"), typically one atom in $10^{6}$–$10^{8}$. Its conductivity is far higher, is dominated by one type of carrier, and can be set by the doping level.

(b) **n-type:** a **pentavalent** impurity (arsenic, antimony, phosphorus) is added to tetravalent silicon. Four of its five valence electrons form covalent bonds with neighbours; the **fifth is left over**, only loosely bound, and is freed by a tiny amount of energy ($\approx0.01\ \text{eV}$). The impurity is called a **donor**. Majority carriers: **electrons**; minority carriers: **holes**.
**p-type:** a **trivalent** impurity (boron, indium, gallium, aluminium) is added. It can form only three covalent bonds, so one bond is left incomplete — a **hole**, which readily accepts an electron from a neighbouring bond, so the hole moves. The impurity is called an **acceptor**. Majority carriers: **holes**; minority carriers: **electrons**.
Both types remain **electrically neutral** overall: an n-type crystal has extra free electrons but an equal number of fixed positive donor ions.

**3.** (a) When p-type and n-type materials are joined, there is a very large concentration difference across the junction: many electrons on the n-side and many holes on the p-side. So electrons **diffuse** from n to p and holes from p to n, and they recombine near the junction. Each electron that leaves the n-side exposes a fixed **positive donor ion**, and each hole that leaves the p-side exposes a fixed **negative acceptor ion**. A narrow region on either side of the junction is thus stripped of mobile carriers and contains only these immobile charged ions; this is the **depletion layer**, about $10^{-6}\ \text{m}$ wide.
The exposed ions set up an electric field pointing from the n-side to the p-side, which **opposes** further diffusion. Equilibrium is reached when this field just stops the net diffusion. The potential difference across the layer is the **potential barrier**, about $0.3\ \text{V}$ for germanium and $0.7\ \text{V}$ for silicon. No external current flows, because the barrier blocks it.

(b) **Forward bias** (p to $+$, n to $-$): the applied field opposes the internal field, so majority carriers are pushed towards the junction, they neutralise some of the exposed ions, and the depletion layer becomes **narrower** and the barrier lower. Beyond the knee voltage the barrier is essentially cancelled and a large current flows; the resistance is low (a few ohms).
**Reverse bias** (p to $-$, n to $+$): the applied field adds to the internal field, majority carriers are pulled **away** from the junction, more ions are exposed, and the depletion layer becomes **wider** and the barrier higher. Only a tiny leakage current due to minority carriers (a few $\mu\text{A}$) flows; the resistance is very high (megohms).

**4.** (a) The characteristic is plotted with $V$ on the $x$-axis and $I$ on the $y$-axis, with reverse values in the third quadrant.
**Forward branch (first quadrant):** almost no current until the applied voltage reaches the **knee voltage** ($0.7\ \text{V}$ for Si, $0.3\ \text{V}$ for Ge), after which the current rises very steeply and almost vertically; the graph is markedly **non-linear**, so the diode does not obey Ohm's law.
**Reverse branch (third quadrant):** a very small, almost constant reverse saturation current of a few microamperes, independent of voltage, until at the **breakdown voltage** the reverse current suddenly becomes very large.

(b) **Knee (cut-in or threshold) voltage** is the forward voltage at which the diode current begins to increase rapidly, because the applied voltage has just overcome the potential barrier. **Breakdown voltage** is the reverse voltage at which the reverse current increases abruptly and without limit, because the strong field either tears electrons out of covalent bonds (Zener breakdown) or accelerates minority carriers enough to ionise atoms in a chain reaction (avalanche breakdown). An ordinary diode is destroyed if the current is not limited; a Zener diode is designed to work there and is used as a voltage regulator.

**5.** (a) In **half-wave rectification** a single diode is joined in series with the load resistance $R_L$ across the secondary of a transformer. During the half cycle in which the secondary makes the diode's p-side positive, the diode is **forward biased**, its resistance is low, and current flows through $R_L$, giving an output voltage that follows the input. During the next half cycle the polarity reverses, the diode is **reverse biased**, its resistance is enormous, and virtually no current flows, so the output is zero. The output is therefore a series of unidirectional pulses with gaps between them — direct current, but only for half the time (see Figure 19, top).

(b) **Full-wave rectification is preferred** because: (i) it uses **both** halves of the input, so its efficiency is about $81\%$ against $40.6\%$ for half-wave; (ii) the output has no gaps, so the **ripple factor** is much lower ($0.48$ against $1.21$ for half-wave), so the output is far easier to smooth with a filter; (iii) the ripple frequency is **doubled** ($100\ \text{Hz}$ from a $50\ \text{Hz}$ mains), and a higher ripple frequency is easier to filter out; (iv) the d.c. output voltage is twice as large for the same peak.
:::

::: note Model answers — short (6–9)
**6.** (a) In the centre-tapped arrangement, the secondary of the transformer has a tapping at its mid-point, which is earthed and joined to one end of the load. The two ends of the secondary are connected to the p-sides of two diodes $D_1$ and $D_2$, and their n-sides are joined together to the other end of the load. Because the tapping is at the centre, the two halves of the secondary are always of **opposite** polarity relative to it.
During the first half cycle, end $A$ is positive with respect to the tap, so $D_1$ is forward biased and conducts while $D_2$ is reverse biased and blocks; current flows through $R_L$ in one direction. During the second half cycle, end $B$ is positive, so $D_2$ conducts and $D_1$ blocks; the current again flows through $R_L$ **in the same direction**, because the two diodes feed the load from the same side. Both halves of the input therefore give output, and the waveform is a continuous train of humps (Figure 19, bottom).

(b) In **half-wave** rectification, the output has one pulse per input cycle, so the ripple frequency equals the input frequency:
$$ f_{ripple} = 50\ \text{Hz} $$
In **full-wave** rectification, both halves of each input cycle produce a pulse, so there are two pulses per cycle:
$$ f_{ripple} = 2\times50 = 100\ \text{Hz} $$

**7.** (a) An **n-p-n transistor** is a single crystal with three doped regions. The **emitter** is heavily doped and of moderate size; it emits the majority carriers (electrons) into the device. The **base** is the thin middle p-region, **very thin** ($10^{-6}\ \text{m}$) and **lightly doped**; it controls the flow. The **collector** is an n-region, moderately doped but physically the largest, and it collects the carriers. In normal operation the emitter-base junction is **forward biased** and the base-collector junction **reverse biased**.
**Why the base is thin and lightly doped:** electrons injected from the emitter into the base are minority carriers there and would be lost by recombination with holes. If the base were thick or heavily doped, most of them would recombine and never reach the collector, so the transistor would not amplify. Because it is thin and lightly doped, only about $2$–$5\%$ of the electrons recombine (giving the small base current $I_B$) and $95$–$98\%$ diffuse right across and are swept into the collector by its reverse-biased field. It is this near-total transfer that gives a large current gain.

(b) The emitter current divides between the base and the collector, so by conservation of charge at the transistor:
$$ I_E = I_B + I_C $$
with $I_B$ only a few per cent of $I_E$, so $I_C \approx I_E$.

**8.** (a) **Common-base current gain** $\alpha$ is the ratio of the collector current to the emitter current:
$$ \alpha = \frac{I_C}{I_E} $$
It is a little less than $1$, typically $0.95$–$0.99$. **Common-emitter current gain** $\beta$ is the ratio of the collector current to the base current:
$$ \beta = \frac{I_C}{I_B} $$
and is large, typically $20$–$500$.
**Relation.** Start from $I_E = I_B+I_C$, and divide every term by $I_C$:
$$ \frac{I_E}{I_C} = \frac{I_B}{I_C}+1 $$
$$ \frac{1}{\alpha} = \frac{1}{\beta}+1 = \frac{1+\beta}{\beta} $$
Inverting, $\alpha = \beta/(1+\beta)$. Solving instead for $\beta$: $\beta\alpha = \beta - \alpha\beta$... more directly, from $\alpha(1+\beta) = \beta$ we get $\alpha = \beta-\alpha\beta$, so $\alpha = \beta(1-\alpha)$ and
$$ \beta = \frac{\alpha}{1-\alpha} $$

(b)
$$ I_C = \beta I_B = 100\times50\times10^{-6} = 5.0\times10^{-3}\ \text{A} = 5.0\ \text{mA} $$
$$ I_E = I_B+I_C = 0.05+5.0 = 5.05\ \text{mA} $$
$$ \alpha = \frac{I_C}{I_E} = \frac{5.00}{5.05} = 0.990 $$
**Check:** $\beta = \alpha/(1-\alpha) = 0.990/0.0099 = 100$. ✓

**9.** (a)

| Gate | Symbol | Boolean | Truth table ($A,B \to Y$) |
|---|---|---|---|
| **OR** | flat back, curved front, two inputs | $Y = A+B$ | $00\to0$; $01\to1$; $10\to1$; $11\to1$ |
| **AND** | flat back, D-shaped front | $Y = A\cdot B$ | $00\to0$; $01\to0$; $10\to0$; $11\to1$ |
| **NOT** | triangle with a small circle at the tip | $Y = \bar{A}$ | $0\to1$; $1\to0$ |

The OR gate gives output $1$ if **any** input is $1$; the AND gate only if **all** inputs are $1$; the NOT gate (inverter) reverses whatever it is given.

(b) A **NAND** gate gives $Y_1 = \overline{A\cdot B}$ — the AND output inverted. Feeding this into a **NOT** gate inverts it once more:
$$ Y = \overline{Y_1} = \overline{\overline{A\cdot B}} = A\cdot B $$
because inverting twice restores the original (involution law). The truth table confirms it: for $A,B = 0,0$, NAND gives $1$ and NOT gives $0$; for $0,1$ and $1,0$, NAND gives $1$ and NOT gives $0$; for $1,1$, NAND gives $0$ and NOT gives $1$. Output is $1$ only when both inputs are $1$ — an **AND** gate. (Since a NOT gate can itself be made by tying the two inputs of a NAND together, the NAND gate is a **universal gate**.)
:::

```figure caption="Rectification. Top: half-wave — only the positive halves appear across the load. Bottom: full-wave — the negative halves are inverted and used too, so the ripple frequency is doubled."
import numpy as np, matplotlib.pyplot as plt
t = np.linspace(0, 2.0, 1200)
v = np.sin(2*np.pi*t)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(4.9,3.4), sharex=True)
for ax in (a1, a2):
    ax.plot(t, v, color=MUTED, lw=0.9, ls='--')
    ax.axhline(0, color=INK, lw=0.9)
    ax.set_yticks([-1,0,1])
    ax.set_ylim(-1.45, 1.6)
    ax.grid(True, color=GRID, lw=0.5)
    ax.spines[['top','right']].set_visible(False)
a1.plot(t, np.clip(v, 0, None), color=ACCENT, lw=1.8)
a1.text(0.02, 1.22, 'half-wave:  output for half of each cycle', fontsize=8.2,
        color=INK, ha='left', va='center')
a1.text(1.52, -1.10, 'ripple 50 Hz', fontsize=7.8, color=MUTED, ha='center')
a2.plot(t, np.abs(v), color=ACCENT, lw=1.8)
a2.text(0.02, 1.22, 'full-wave:  both halves used', fontsize=8.2,
        color=INK, ha='left', va='center')
a2.text(1.52, -1.10, 'ripple 100 Hz', fontsize=7.8, color=MUTED, ha='center')
a2.set_xlabel('time  (in units of the input period)', fontsize=9)
a1.set_ylabel('$V_{out}$', fontsize=9)
a2.set_ylabel('$V_{out}$', fontsize=9)
fig.subplots_adjust(hspace=0.22)
```
**Long answer / numerical questions [8 marks each]**

1. (a) Explain, with energy-band diagrams, the difference between a conductor, a semiconductor and an insulator. [3] (b) Explain n-type and p-type doping and the formation of the depletion layer and potential barrier in a p-n junction. [3] (c) Draw the forward and reverse V-I characteristics of a diode and mark the knee and breakdown voltages. [2] <span class="marks">[8]</span> (NEB 2080)
2. (a) Explain half-wave and full-wave rectification with circuit diagrams and output waveforms. [4] (b) Compare them in efficiency, ripple factor and ripple frequency. [2] (c) For a $50\ \text{Hz}$ input, state the ripple frequency in each case, and explain why a capacitor is connected across the load. [2] <span class="marks">[8]</span> (NEB 2081)
3. (a) Describe the construction and working of an n-p-n transistor, explaining why the base is thin and lightly doped. [3] (b) Define $\alpha$ and $\beta$ and derive the relation between them. [3] (c) A transistor with $\beta = 100$ has a base current of $50\ \mu\text{A}$. Find $I_C$, $I_E$ and $\alpha$, and the voltage gain if the input resistance is $1.0\ \text{k}\Omega$ and the load is $5.0\ \text{k}\Omega$. [2] <span class="marks">[8]</span> (NEB 2082)

::: note Model answers — long
**1.** (a) In a crystal the allowed energies form bands separated by forbidden gaps. The band filled at $0\ \text{K}$ is the **valence band**, the empty one above it the **conduction band**, and their separation is the **energy gap** $E_g$. Conduction requires electrons with empty levels close above them to move into.
**Conductor:** the two bands **overlap**, $E_g = 0$; countless empty levels lie immediately above the occupied ones, so even a very weak field produces a large current. Resistivity $10^{-8}$–$10^{-6}\ \Omega\,\text{m}$; resistance **increases** with temperature.
**Semiconductor:** $E_g$ is small, $1.1\ \text{eV}$ (Si) or $0.72\ \text{eV}$ (Ge). At $0\ \text{K}$ the conduction band is empty and the crystal is an insulator, but at $300\ \text{K}$ thermal energy promotes a few electrons across, each leaving a **hole** behind; both carry current. Resistivity $10^{-5}$–$10^{4}\ \Omega\,\text{m}$; resistance **decreases** with temperature.
**Insulator:** $E_g$ is large, $5$–$10\ \text{eV}$. Room-temperature thermal energy is only about $0.026\ \text{eV}$, hopelessly small, so the conduction band stays empty. Resistivity $10^{11}$–$10^{19}\ \Omega\,\text{m}$.

(b) **Doping.** Adding a **pentavalent** atom (As, Sb, P) to silicon gives one spare electron per impurity atom, loosely bound and easily freed: an **n-type** crystal, majority carriers electrons, impurity called a donor. Adding a **trivalent** atom (B, In, Ga) leaves one covalent bond incomplete, a **hole** that can accept an electron: a **p-type** crystal, majority carriers holes, impurity called an acceptor. Both remain electrically neutral overall.
**Depletion layer.** Joining the two, electrons diffuse from n to p and holes from p to n, driven by the concentration difference, and recombine near the boundary. This leaves behind **immobile** positive donor ions on the n-side and negative acceptor ions on the p-side, in a narrow region with almost no mobile carriers — the **depletion layer**, roughly $1\ \mu\text{m}$ wide. These fixed ions create an internal field from n to p, which opposes further diffusion, and the associated potential difference is the **potential barrier** ($0.7\ \text{V}$ for Si, $0.3\ \text{V}$ for Ge). At equilibrium diffusion stops and no net current flows.

(c) **Forward characteristic (first quadrant):** current is negligible up to the **knee voltage** ($0.7\ \text{V}$ for Si), then rises almost vertically; the curve is non-linear, so the diode disobeys Ohm's law and its dynamic resistance falls with current. **Reverse characteristic (third quadrant):** only a tiny reverse saturation current of a few $\mu\text{A}$, nearly independent of voltage, until at the **breakdown voltage** the current increases abruptly. Both points must be labelled on the sketch.

**2.** (a) **Half-wave.** A single diode is in series with $R_L$ across the transformer secondary. On the half cycle that forward-biases the diode, current flows and the output follows the input; on the other half the diode blocks and the output is zero. The output is a train of pulses separated by gaps (Figure 19, top).
**Full-wave (centre-tapped).** The secondary has an earthed centre tap joined to one end of the load; the two ends feed diodes $D_1$ and $D_2$, whose other terminals join at the far end of the load. The two halves of the secondary are always of opposite polarity with respect to the tap, so on the first half cycle $D_1$ conducts and $D_2$ blocks, and on the second half cycle $D_2$ conducts and $D_1$ blocks. In **both** cases the current passes through $R_L$ in the **same** direction, so the negative halves are effectively flipped up and the output is a continuous series of humps (Figure 19, bottom). (A bridge of four diodes does the same job without a centre tap.)

(b)

| | Half-wave | Full-wave |
|---|---|---|
| Diodes | 1 | 2 (centre-tap) or 4 (bridge) |
| Fraction of input used | half | all |
| Maximum efficiency | $40.6\%$ | $81.2\%$ |
| Ripple factor | $1.21$ | $0.48$ |
| Ripple frequency (for $f$ input) | $f$ | $2f$ |
| D.C. output | $V_0/\pi$ | $2V_0/\pi$ |

(c) For a $50\ \text{Hz}$ supply, the half-wave ripple frequency is **$50\ \text{Hz}$** (one pulse per cycle) and the full-wave ripple frequency is **$100\ \text{Hz}$** (two pulses per cycle).
**Why a capacitor is connected across the load.** The rectified output is unidirectional but far from steady; the fluctuation is the ripple. A large capacitor in parallel with $R_L$ acts as a **reservoir**: it charges up almost to the peak voltage while the output is rising, and then, while the rectified voltage falls towards zero, it discharges slowly through $R_L$ (time constant $CR_L$ made much longer than the ripple period). The output therefore sags only a little between peaks, and the ripple is greatly reduced. Its reactance $X_C = 1/2\pi fC$ is small for the a.c. ripple component, which it short-circuits, but infinite for the d.c. component, which it passes on to the load — so it is a simple low-pass filter. This works better in the full-wave case because the gaps are shorter and the ripple frequency twice as high.

**3.** (a) An **n-p-n transistor** consists of a thin p-type **base** sandwiched between a heavily doped n-type **emitter** and a moderately doped, physically larger n-type **collector**. In normal amplifying operation the **emitter-base junction is forward biased** and the **base-collector junction is reverse biased**.
**Working.** The forward bias on the emitter junction is easily overcome, so the heavily doped emitter injects a large stream of electrons into the base. In the base these electrons are minority carriers and could recombine with holes, but the base is very thin and lightly doped, so only about $2$–$5\%$ of them do; these constitute the small base current $I_B$. The remaining $95$–$98\%$ diffuse right across the base and reach the edge of the reverse-biased collector junction, where the strong field there sweeps them straight into the collector, giving $I_C$. Thus $I_E = I_B+I_C$ with $I_C \approx I_E$.
**Why the base is thin and lightly doped:** to keep recombination small so that nearly all the emitted carriers reach the collector. A thick or heavily doped base would lose most of them, $\alpha$ would fall well below $1$, and $\beta = \alpha/(1-\alpha)$ would collapse — there would be no useful amplification. The **amplification** itself comes from transferring a current from a low-resistance input circuit (forward-biased junction) to a high-resistance output circuit (reverse-biased junction) at nearly the same size, so that the voltage and power are greatly increased. ("Transistor" = transfer + resistor.)

(b) $\alpha = I_C/I_E$ (common base), $\beta = I_C/I_B$ (common emitter). From $I_E = I_B + I_C$, divide by $I_C$:
$$ \frac{I_E}{I_C} = \frac{I_B}{I_C} + 1 $$
$$ \frac{1}{\alpha} = \frac{1}{\beta} + 1 = \frac{1+\beta}{\beta} $$
$$ \alpha = \frac{\beta}{1+\beta} $$
Rearranging this for $\beta$: $\alpha(1+\beta) = \beta$, so $\alpha = \beta(1-\alpha)$ and
$$ \beta = \frac{\alpha}{1-\alpha} $$
Since $\alpha$ is just below $1$, the denominator $1-\alpha$ is tiny and $\beta$ is large — that is why a $1\%$ change in $\alpha$ makes an enormous difference to the gain.

(c)
$$ I_C = \beta I_B = 100\times50\ \mu\text{A} = 5.0\ \text{mA} $$
$$ I_E = I_B+I_C = 0.05+5.0 = 5.05\ \text{mA} $$
$$ \alpha = \frac{I_C}{I_E} = \frac{5.00}{5.05} = 0.990 $$
$$ A_V = \beta\times\frac{R_{out}}{R_{in}} = 100\times\frac{5.0\times10^{3}}{1.0\times10^{3}} = 500 $$
**Check:** $\beta = \alpha/(1-\alpha) = 0.990/0.010 = 100$. ✓ A voltage gain of $500$ from a current gain of $100$ shows how the resistance ratio does the rest of the work.
:::

::: tip Examiner's note — Semiconductor devices
Band diagrams must show three things: the valence band, the conduction band and the
**size** of the gap — and the gap values $1.1\ \text{eV}$ (Si) and $0.72\ \text{eV}$
(Ge) are worth quoting. Never say a doped crystal is charged: n-type has extra free
electrons but an equal number of fixed positive ions, so it is **neutral**.
In rectifier questions the waveform sketch carries marks of its own — draw the
input and output on the same time axis and label the ripple frequency. For the
$\alpha$–$\beta$ derivation, start from $I_E = I_B+I_C$ and divide by $I_C$; that is
the whole proof. And in transistor numericals, remember that $I_B$ is in
**microamperes** while $I_C$ is in milliamperes — mixing them up is the single most
common error in this unit.
:::

## 3.23 Quantization of energy

CDC allots **8 teaching hours** — the largest single unit in the Grade 12 course.
Bohr's theory of the hydrogen atom, the radius and energy of the orbits, the
spectral series, energy-level diagrams, excitation and ionisation, de Broglie waves
and the production and properties of X-rays are all examinable, and something from
this unit appears in Group C almost every year.

**Short answer questions [5 marks each]**

1. (a) State the postulates of Bohr's theory of the hydrogen atom. [3] (b) Which classical difficulty of Rutherford's model does each postulate remove? [2] <span class="marks">[5]</span> (NEB 2080)
2. (a) Derive an expression for the radius of the $n$th Bohr orbit. [3] (b) Show that $r_n \propto n^{2}$ and find the radius of the second orbit given $r_1 = 0.53\ \text{Å}$. [2] <span class="marks">[5]</span> (NEB 2082)
3. (a) Derive the total energy of an electron in the $n$th Bohr orbit. [3] (b) Why is the total energy negative, and what does that mean physically? [2] <span class="marks">[5]</span> (NEB 2081)
4. (a) Draw the energy-level diagram of hydrogen and mark the Lyman, Balmer and Paschen series. [3] (b) In which region of the spectrum does each lie? [2] <span class="marks">[5]</span>
5. (a) Define excitation energy, excitation potential, ionisation energy and ionisation potential. [3] (b) Find the ionisation energy of hydrogen from the ground state and the first excitation energy. [2] <span class="marks">[5]</span> (NEB 2079 model)
6. (a) Calculate the wavelength of the first line of the Balmer series ($n = 3$ to $n = 2$) taking $R = 1.097\times10^{7}\ \text{m}^{-1}$. [3] (b) State the region of the spectrum in which it lies and its colour. [2] <span class="marks">[5]</span>
7. (a) State de Broglie's hypothesis and write the expression for the wavelength. [2] (b) Show that Bohr's quantisation condition follows from fitting a whole number of de Broglie waves into an orbit. [3] <span class="marks">[5]</span> (NEB 2082 model)
8. (a) Describe the production of X-rays in a Coolidge tube. [3] (b) Show that the minimum wavelength emitted is $\lambda_{min} = hc/eV$, and find it for $V = 50\ \text{kV}$. [2] <span class="marks">[5]</span>
9. (a) Distinguish between continuous and characteristic X-ray spectra. [3] (b) State three properties and two uses of X-rays. [2] <span class="marks">[5]</span>
10. (a) State three limitations of Bohr's theory. [3] (b) Why can it not be applied to the helium atom? [2] <span class="marks">[5]</span>

::: note Model answers — short (1–5)
**1.** (a) **Postulate 1 (stationary orbits).** The electron revolves round the nucleus only in certain allowed circular orbits, called stationary orbits, in which the necessary centripetal force is supplied by the electrostatic attraction of the nucleus.
**Postulate 2 (quantisation of angular momentum).** Only those orbits are allowed for which the angular momentum of the electron is an integral multiple of $h/2\pi$:
$$ mvr = \frac{nh}{2\pi}, \qquad n = 1,2,3,\ldots $$
**Postulate 3 (no radiation in a stationary orbit).** While the electron remains in such an orbit it does **not** radiate energy, however fast it accelerates.
**Postulate 4 (frequency condition).** Radiation is emitted or absorbed only when the electron jumps between two allowed orbits, and the photon frequency is fixed by the energy difference:
$$ h\nu = E_2 - E_1 $$

(b) Rutherford's model had two fatal defects. **(i) Instability.** A circling electron is accelerating, and classical electromagnetism says an accelerating charge must radiate; it would lose energy continuously, spiral inwards and hit the nucleus in about $10^{-8}\ \text{s}$. Every atom would collapse. **Postulate 3** removes this by simply forbidding radiation from an allowed orbit; **postulates 1 and 2** provide a smallest orbit ($n = 1$) below which the electron cannot fall. **(ii) Continuous spectrum.** As the electron spiralled in, its frequency of revolution would change continuously, so the atom would emit a continuous band of all frequencies. In fact hydrogen emits a **line** spectrum of sharp, definite wavelengths. **Postulate 4** explains this: only certain energy differences exist, so only certain photon frequencies can be emitted.

**2.** (a) Let an electron of mass $m$ and charge $e$ move with speed $v$ in a circular orbit of radius $r$ about a nucleus of charge $+e$ (hydrogen). The electrostatic attraction supplies the centripetal force:
$$ \frac{1}{4\pi\varepsilon_0}\frac{e^{2}}{r^{2}} = \frac{mv^{2}}{r} $$
$$ mv^{2} = \frac{e^{2}}{4\pi\varepsilon_0 r} $$
Bohr's quantisation condition gives $mvr = nh/2\pi$, so $v = nh/2\pi mr$. Substituting,
$$ m\left(\frac{nh}{2\pi mr}\right)^{2} = \frac{e^{2}}{4\pi\varepsilon_0 r} $$
$$ \frac{n^{2}h^{2}}{4\pi^{2}mr^{2}} = \frac{e^{2}}{4\pi\varepsilon_0 r} $$
Multiplying both sides by $r^{2}$ and rearranging,
$$ r_n = \frac{\varepsilon_0n^{2}h^{2}}{\pi me^{2}} $$

(b) Everything in that expression except $n$ is a constant of nature, so
$$ r_n \propto n^{2} $$
The orbits are not equally spaced: they get rapidly further apart. With $r_1 = 0.53\ \text{Å}$,
$$ r_2 = 2^{2}\times0.53 = 2.12\ \text{Å} = 2.12\times10^{-10}\ \text{m} $$

**3.** (a) The electron has both kinetic and potential energy.
**Kinetic energy.** From the force equation $mv^{2} = e^{2}/4\pi\varepsilon_0r$,
$$ KE = \frac{1}{2}mv^{2} = \frac{e^{2}}{8\pi\varepsilon_0 r} $$
**Potential energy.** For charges $+e$ and $-e$ a distance $r$ apart, taking the zero at infinity,
$$ PE = -\frac{e^{2}}{4\pi\varepsilon_0 r} $$
**Total energy.**
$$ E = KE+PE = \frac{e^{2}}{8\pi\varepsilon_0r}-\frac{e^{2}}{4\pi\varepsilon_0r} = -\frac{e^{2}}{8\pi\varepsilon_0r} $$
Substituting $r_n = \varepsilon_0n^{2}h^{2}/\pi me^{2}$,
$$ E_n = -\frac{me^{4}}{8\varepsilon_0^{2}h^{2}n^{2}} = -\frac{13.6}{n^{2}}\ \text{eV} $$

(b) The energy is negative because the zero of potential energy is fixed at **infinite separation**, where the electron is free and at rest. A **bound** electron has less energy than that, so its total energy must be below zero. Physically the negative sign means the electron is **trapped**: an amount of energy $+13.6/n^{2}\ \text{eV}$ must be supplied from outside to pull it away from the nucleus altogether. Note also that $|PE| = 2\times KE$, and $E = -KE$, which is the virial theorem for an inverse-square force.

**4.** (a) The levels are drawn as horizontal lines at $E_n = -13.6/n^{2}\ \text{eV}$: $-13.6$ for $n=1$, $-3.40$ for $n=2$, $-1.51$ for $n=3$, $-0.85$ for $n=4$, $-0.54$ for $n=5$, and $0$ for $n = \infty$. The lines crowd together as $n$ increases (Figure 20). Downward arrows show the emission series:
- **Lyman series:** all transitions ending on $n = 1$.
- **Balmer series:** all transitions ending on $n = 2$.
- **Paschen series:** all transitions ending on $n = 3$.
(Brackett ends on $n=4$ and Pfund on $n=5$.)

(b) The Lyman transitions have the largest energy differences (up to $13.6\ \text{eV}$), so they lie in the **ultraviolet**. The Balmer transitions lie in the **visible** region (and the near ultraviolet at the series limit) — these are the four lines actually seen in a hydrogen discharge tube, red $656\ \text{nm}$, blue-green $486\ \text{nm}$, violet $434\ \text{nm}$ and $410\ \text{nm}$. Paschen, Brackett and Pfund lie in the **infrared**, progressively further into it.

**5.** (a) **Excitation energy** is the energy that must be supplied to lift an electron from the ground state to a higher (excited) level; the first excitation energy of hydrogen is $E_2-E_1$. **Excitation potential** is the accelerating potential difference in volts through which an electron must fall to acquire that energy — numerically equal to the excitation energy in eV. **Ionisation energy** is the energy needed to remove the electron completely from the atom, that is to raise it from the ground state to $n = \infty$. **Ionisation potential** is the corresponding potential difference in volts.

(b)
$$ E_{ion} = E_\infty - E_1 = 0-(-13.6) = 13.6\ \text{eV} $$
so the ionisation potential is $13.6\ \text{V}$.
$$ E_{exc,1} = E_2-E_1 = -3.40-(-13.6) = 10.2\ \text{eV} $$
so the first excitation potential is $10.2\ \text{V}$. (These are the numbers confirmed directly by the Franck-Hertz experiment.)
:::

::: note Model answers — short (6–10)
**6.** (a) The Balmer series ends on $n_f = 2$, and the **first** line is the transition from $n_i = 3$. Rydberg's formula gives
$$ \frac{1}{\lambda} = R\left(\frac{1}{n_f^{2}}-\frac{1}{n_i^{2}}\right) = R\left(\frac{1}{4}-\frac{1}{9}\right) $$
$$ \frac{1}{\lambda} = 1.097\times10^{7}\times\frac{5}{36} = 1.524\times10^{6}\ \text{m}^{-1} $$
$$ \lambda = \frac{1}{1.524\times10^{6}} = 6.56\times10^{-7}\ \text{m} = 656\ \text{nm} $$

(b) It lies in the **visible** region, at the red end; it is the bright **red** line known as $H_\alpha$, the most conspicuous line in the hydrogen spectrum and a familiar feature of the spectra of stars and nebulae.
**Check by energy:** $E_3-E_2 = -1.51-(-3.40) = 1.89\ \text{eV}$, and $\lambda = 1242/1.89 = 657\ \text{nm}$. ✓

**7.** (a) **de Broglie's hypothesis:** just as light, long regarded as a wave, behaves in some experiments as a stream of particles, so every moving **material particle** has a wave associated with it. The wavelength is
$$ \lambda = \frac{h}{p} = \frac{h}{mv} $$
For a $1\ \text{kg}$ body moving at $1\ \text{m s}^{-1}$ this is $6.6\times10^{-34}\ \text{m}$ — undetectable. For an electron accelerated through $100\ \text{V}$ it is $1.2\times10^{-10}\ \text{m}$, comparable with the spacing of atoms in a crystal, which is why electrons are diffracted by crystals.

(b) De Broglie argued that a stationary orbit is one in which the electron wave joins smoothly onto itself after going once round — a **standing wave** on a circle. If it did not, successive circuits would interfere destructively and the wave would cancel itself out. The condition for the wave to close up is that the circumference contains a whole number of wavelengths:
$$ 2\pi r = n\lambda $$
Substituting $\lambda = h/mv$,
$$ 2\pi r = \frac{nh}{mv} $$
$$ mvr = \frac{nh}{2\pi} $$
which is exactly Bohr's quantisation condition. What Bohr had to **assume**, de Broglie **explained**: the integer $n$ is simply the number of wavelengths that fit round the orbit.

**8.** (a) In a **Coolidge tube**, a tungsten filament in a highly evacuated tube is heated by a low-voltage supply and emits electrons by **thermionic emission**; the filament current controls how many, and hence the **intensity** of the X-rays. These electrons are accelerated through a very high potential difference (tens of kilovolts) towards a **target** of a high-melting-point, high-atomic-number metal such as tungsten or molybdenum, set at an angle in a massive copper anode. On striking the target the electrons are suddenly stopped; less than $1\%$ of their kinetic energy is converted into **X-rays** and the rest into heat, so the anode must be cooled by circulating oil or water or by rotating it. The **quality** (penetrating power) of the X-rays is controlled by the accelerating voltage, the **intensity** by the filament current.

(b) An electron accelerated through $V$ arrives with kinetic energy $eV$. In the most extreme possible event, the electron is brought to rest in a **single** collision and **all** of its energy goes into one photon. That photon has the greatest possible energy, and so the shortest possible wavelength:
$$ eV = h\nu_{max} = \frac{hc}{\lambda_{min}} \;\Rightarrow\; \lambda_{min} = \frac{hc}{eV} $$
$$ \lambda_{min} = \frac{6.63\times10^{-34}\times3\times10^{8}}{1.6\times10^{-19}\times50\times10^{3}} = 2.49\times10^{-11}\ \text{m} $$
This is the **Duane-Hunt limit**; note it depends only on $V$, not on the target material.

**9.** (a) The **continuous** spectrum (bremsstrahlung, or braking radiation) arises from electrons that are decelerated in the field of the target nuclei, losing an arbitrary fraction of their energy in each event. It is therefore a smooth, continuous distribution of all wavelengths above a **sharp minimum** $\lambda_{min} = hc/eV$, and it depends **only on the accelerating voltage**, not on the target material.
The **characteristic** spectrum is a set of sharp, intense **lines** (the K, L, M series) superposed on the continuous background. It arises when an incident electron knocks an electron out of an **inner shell** of a target atom; an electron from a higher shell then falls into the vacancy and emits a photon whose energy is the difference between two well-defined atomic levels. These wavelengths depend **only on the target material**, not on the voltage — though the voltage must exceed a threshold before the lines appear at all. (Moseley's law relates their frequencies to the atomic number, which is how $Z$ was first measured.)

(b) **Properties:** (i) they are electromagnetic waves of very short wavelength ($10^{-8}$ to $10^{-13}\ \text{m}$), travelling at $c$; (ii) they are uncharged, so they are undeflected by electric and magnetic fields; (iii) they are highly **penetrating**, passing through flesh, wood and thin metal, and absorption increases sharply with the atomic number and thickness of the absorber; (iv) they **ionise** gases, affect photographic plates, cause fluorescence, and can be diffracted by crystals, which proves they are waves; (v) they damage living tissue.
**Uses:** medical radiography of bones and teeth; radiotherapy for cancer; detection of flaws and cracks in castings and welds; airport and customs security scanning; X-ray crystallography, which determines the structure of crystals and of molecules such as DNA.

**10.** (a) **Limitations of Bohr's theory.** (i) It works **only for hydrogen and hydrogen-like one-electron ions** ($\text{He}^{+}$, $\text{Li}^{2+}$); it fails completely for any atom with two or more electrons, because it cannot handle the repulsion between them. (ii) It cannot explain the **fine structure** of spectral lines — lines that a good spectrometer resolves into two or more closely spaced components. (iii) It cannot explain the **relative intensities** of lines, or why some transitions are much more probable than others. (iv) It cannot explain the **Zeeman and Stark effects**, the splitting of lines in magnetic and electric fields. (v) It is a hybrid: it uses classical mechanics for the orbit but arbitrarily forbids classical radiation, without saying why. (vi) It assumes a definite orbit of definite radius and speed, which violates the **Heisenberg uncertainty principle**.

(b) Because helium has **two** electrons. Bohr's calculation is built on a single electron moving under a single inverse-square force from the nucleus, and the whole derivation of $r_n$ and $E_n$ depends on that one force. In helium each electron is attracted by the nucleus **and repelled by the other electron**, whose position is itself changing. This is a three-body problem with no exact solution, and the repulsion term cannot be written in a form that allows a simple quantisation condition. The predicted energy levels come out badly wrong. The correct treatment came only with the wave mechanics of Schrödinger, in which the electron is described by a probability cloud rather than an orbit.
:::

```figure caption="Energy levels of the hydrogen atom, E_n = -13.6/n^2 eV. Downward arrows show the first transition of each series; the levels crowd together towards the ionisation limit at 0 eV."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.6))
ns = range(1, 7)
for n in ns:
    E = -13.6/n**2
    ax.plot([0.10, 0.92], [E, E], color=INK, lw=1.3)
    ax.text(0.94, E, 'n = %d' % n, fontsize=8.0, color=INK, va='center')
    ax.text(0.07, E, '%.2f' % E, fontsize=7.6, color=MUTED, va='center',
            ha='right')
ax.plot([0.10, 0.92], [0, 0], color=MUTED, lw=1.3, ls='--')
ax.text(0.94, 0.0, r'n = $\infty$', fontsize=8.0, color=MUTED, va='center')
ax.text(0.07, 0.0, '0.00', fontsize=7.6, color=MUTED, va='center', ha='right')
arrows = [(2, 1, 0.24, 'Lyman\n(UV)', '#A8271F'),
          (3, 2, 0.46, 'Balmer\n(visible)', ACCENT),
          (4, 3, 0.70, 'Paschen\n(IR)', '#0B6A62')]
for ni, nf, x, lab, col in arrows:
    Ei, Ef = -13.6/ni**2, -13.6/nf**2
    ax.annotate('', xy=(x, Ef), xytext=(x, Ei),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.5))
    ax.text(x+0.025, (Ei+Ef)/2, lab, fontsize=7.6, color=col, va='center')
ax.set_ylabel('energy  $E_n$  (eV)', fontsize=9)
ax.set_xlim(-0.06, 1.22); ax.set_ylim(-15.4, 1.9)
ax.set_xticks([])
ax.spines[['top','right','bottom']].set_visible(False)
```
**Long answer / numerical questions [8 marks each]**

1. (a) State Bohr's postulates. [2] (b) Derive expressions for the radius and the total energy of the $n$th orbit of the hydrogen atom. [4] (c) Find the radius of the second orbit and the energy of the third level, given $r_1 = 0.53\ \text{Å}$ and $E_1 = -13.6\ \text{eV}$. [2] <span class="marks">[8]</span> (NEB 2081)
2. (a) Draw and explain the energy-level diagram of hydrogen and account for the Lyman, Balmer and Paschen series. [3] (b) Define excitation and ionisation energies and find both for hydrogen. [2] (c) Calculate the wavelength of the first line of the Balmer series and of the series limit of the Lyman series, taking $R = 1.097\times10^{7}\ \text{m}^{-1}$. [3] <span class="marks">[8]</span> (NEB 2082)
3. (a) Describe the production of X-rays in a Coolidge tube and explain how the intensity and the quality are controlled. [3] (b) Distinguish between continuous and characteristic X-ray spectra, and derive $\lambda_{min} = hc/eV$. [3] (c) Find $\lambda_{min}$ for accelerating voltages of $20\ \text{kV}$ and $50\ \text{kV}$, and comment. [2] <span class="marks">[8]</span> (NEB 2080)

::: note Model answers — long
**1.** (a) The four postulates are as listed in short answer 1(a): circular stationary orbits held by electrostatic attraction; angular momentum quantised as $mvr = nh/2\pi$; no radiation while in a stationary orbit; and radiation only on a jump, with $h\nu = E_2-E_1$.

(b) See the derivation box below for the step-by-step argument. The results are
$$ r_n = \frac{\varepsilon_0n^{2}h^{2}}{\pi me^{2}} = 0.53\,n^{2}\ \text{Å} $$
$$ E_n = -\frac{me^{4}}{8\varepsilon_0^{2}h^{2}n^{2}} = -\frac{13.6}{n^{2}}\ \text{eV} $$
Both follow from just two equations — the force equation
$e^{2}/4\pi\varepsilon_0r^{2} = mv^{2}/r$ and the quantisation condition
$mvr = nh/2\pi$ — solved simultaneously for $r$ and then for $E = KE+PE$.

(c)
$$ r_2 = n^{2}r_1 = 4\times0.53 = 2.12\ \text{Å} = 2.12\times10^{-10}\ \text{m} $$
$$ E_3 = \frac{E_1}{n^{2}} = \frac{-13.6}{9} = -1.51\ \text{eV} $$
**Check:** the energy needed to ionise an atom already in the third level is only $1.51\ \text{eV}$, far less than the $13.6\ \text{eV}$ from the ground state — excited atoms are much easier to ionise, as they must be. ✓

**2.** (a) The allowed energies are $E_n = -13.6/n^{2}\ \text{eV}$, so the levels are drawn as horizontal lines at $-13.6$, $-3.40$, $-1.51$, $-0.85$, $-0.54\ \text{eV}$ and so on up to $0$ at $n = \infty$ (Figure 20). Because $E_n$ goes as $1/n^{2}$, the spacing shrinks rapidly and the levels **crowd together** as they approach the ionisation limit. Every emission line corresponds to a downward jump between two of these levels, with $h\nu = E_i - E_f$; because the levels are discrete, only certain photon energies are possible, which is why the spectrum consists of **sharp lines**.
Grouping the transitions by their **final** level explains the series at once:
- transitions ending on $n = 1$ have the largest energy gaps (from $10.2$ up to $13.6\ \text{eV}$) and form the **Lyman** series in the ultraviolet;
- transitions ending on $n = 2$ have gaps of $1.89$ to $3.40\ \text{eV}$, corresponding to $656$ down to $365\ \text{nm}$, so they form the **Balmer** series in the visible;
- transitions ending on $n = 3$ have still smaller gaps and form the **Paschen** series in the infrared, with Brackett ($n=4$) and Pfund ($n=5$) further into the infrared.
In general $1/\lambda = R\left(1/n_f^{2}-1/n_i^{2}\right)$.

(b) **Excitation energy** is the energy needed to raise the electron from the ground state to a specified higher level; **ionisation energy** is the energy needed to remove it entirely, to $n = \infty$.
$$ E_{exc,1} = E_2-E_1 = -3.40+13.6 = 10.2\ \text{eV} $$
$$ E_{exc,2} = E_3-E_1 = -1.51+13.6 = 12.1\ \text{eV} $$
$$ E_{ion} = 0-(-13.6) = 13.6\ \text{eV} $$
so the first excitation potential is $10.2\ \text{V}$ and the ionisation potential $13.6\ \text{V}$.

(c) **First Balmer line** ($n_i = 3 \to n_f = 2$):
$$ \frac{1}{\lambda} = R\left(\frac{1}{4}-\frac{1}{9}\right) = 1.097\times10^{7}\times0.1389 = 1.524\times10^{6}\ \text{m}^{-1} $$
$$ \lambda = 6.56\times10^{-7}\ \text{m} = 656\ \text{nm} \quad(\text{red, visible}) $$
**Lyman series limit** ($n_i = \infty \to n_f = 1$):
$$ \frac{1}{\lambda} = R\left(\frac{1}{1}-0\right) = 1.097\times10^{7}\ \text{m}^{-1} $$
$$ \lambda = 9.12\times10^{-8}\ \text{m} = 91.2\ \text{nm} \quad(\text{far ultraviolet}) $$
**Check:** the Lyman limit corresponds to $1242/91.2 = 13.6\ \text{eV}$, exactly the ionisation energy — as it must, since the series limit is the transition from a just-free electron to the ground state. ✓

**3.** (a) **Coolidge tube.** A tungsten filament, heated by a separate low-voltage supply inside a highly evacuated glass tube, emits electrons thermionically. These are focused by a molybdenum cup and accelerated through a potential difference of $10$–$100\ \text{kV}$ onto a target of tungsten (high melting point, high atomic number) embedded at about $45^{\circ}$ in a massive copper anode. The abrupt stopping of the electrons produces X-rays, which leave through a thin window. Over $99\%$ of the electron energy becomes heat, so the anode is cooled by circulating water or oil, or is rotated.
**Intensity** (the number of X-ray photons per second) is controlled by the **filament current**, since that fixes how many electrons per second strike the target. **Quality** (the penetrating power, i.e. how short the wavelengths are) is controlled by the **accelerating voltage**: a higher voltage gives more energetic electrons, a shorter $\lambda_{min}$, and therefore "harder", more penetrating X-rays. The two controls are independent, which is exactly what a radiographer needs.

(b) **Continuous spectrum:** produced when incident electrons are **decelerated** in the electric field of the target nuclei, each losing an arbitrary part of its energy. Since the fraction lost can be anything from nearly zero up to everything, all wavelengths **above a sharp minimum** are produced, in a smooth distribution. It depends only on the **accelerating voltage**.
**Characteristic spectrum:** produced when an incident electron ejects an electron from an **inner (K or L) shell** of a target atom. An outer electron drops into the vacancy and emits a photon of energy equal to the difference between two sharply defined atomic levels, giving intense **discrete lines** ($K_\alpha$, $K_\beta$, $L_\alpha$, …) superposed on the continuous background. These depend only on the **target material** and are its fingerprint.
**Derivation of the limit.** An electron accelerated through $V$ has kinetic energy
$$ KE = eV $$
In the most extreme collision, the electron is stopped **completely in one step** and all of its energy goes into a single photon. That is the largest photon energy possible, hence the highest frequency and shortest wavelength:
$$ eV = h\nu_{max} = \frac{hc}{\lambda_{min}} $$
$$ \lambda_{min} = \frac{hc}{eV} $$

(c) For $V = 20\ \text{kV}$:
$$ \lambda_{min} = \frac{6.63\times10^{-34}\times3\times10^{8}}{1.6\times10^{-19}\times2.0\times10^{4}} = 6.22\times10^{-11}\ \text{m} $$
For $V = 50\ \text{kV}$:
$$ \lambda_{min} = \frac{1.989\times10^{-25}}{1.6\times10^{-19}\times5.0\times10^{4}} = 2.49\times10^{-11}\ \text{m} $$
**Comment.** Raising the voltage by a factor of $2.5$ shortens $\lambda_{min}$ by the same factor $2.5$, since $\lambda_{min} \propto 1/V$. The shorter the wavelength, the more penetrating ("harder") the radiation — $50\ \text{kV}$ X-rays will pass through thicker tissue and denser bone than $20\ \text{kV}$ ones. Note also that this limit is independent of the target metal; only the characteristic lines depend on that.
:::

::: derivation Radius and energy of the $n$th Bohr orbit
We want the size of the allowed orbits of the hydrogen atom and the energy of the
electron in each, starting from only two facts: the electrostatic force holds the
electron in its circle, and the angular momentum can take only certain values.

**Setting up.** A hydrogen atom has one electron, of mass $m$ and charge $-e$,
moving in a circle of radius $r$ with speed $v$ about a nucleus of charge $+e$. Take
the nucleus to be fixed, since it is about $1836$ times heavier. The potential
energy is measured from zero at infinite separation.

**Step 1 — write the force that holds the electron in the circle.** The only force
is the electrostatic attraction, and it must supply exactly the centripetal force:

$$ \frac{1}{4\pi\varepsilon_0}\frac{e^{2}}{r^{2}} = \frac{mv^{2}}{r} $$

**Step 2 — multiply both sides by $r$.** This gives a useful expression for
$mv^{2}$, which we will need twice:

$$ mv^{2} = \frac{e^{2}}{4\pi\varepsilon_0 r} $$

**Step 3 — write Bohr's quantisation condition.** Only orbits with angular momentum
an integer multiple of $h/2\pi$ are allowed:

$$ mvr = \frac{nh}{2\pi} $$

**Step 4 — make $v$ the subject.** Divide both sides by $mr$:

$$ v = \frac{nh}{2\pi mr} $$

**Step 5 — substitute this $v$ into the result of Step 2.**

$$ m\left(\frac{nh}{2\pi mr}\right)^{2} = \frac{e^{2}}{4\pi\varepsilon_0 r} $$

**Step 6 — square the bracket and cancel one $m$.**

$$ \frac{n^{2}h^{2}}{4\pi^{2}mr^{2}} = \frac{e^{2}}{4\pi\varepsilon_0 r} $$

**Step 7 — multiply both sides by $r^{2}$ and solve for $r$.** One power of $r$
survives on the right:

$$ r_n = \frac{\varepsilon_0 n^{2}h^{2}}{\pi m e^{2}} $$

**Step 8 — write the kinetic energy.** Halve the result of Step 2:

$$ KE = \frac{1}{2}mv^{2} = \frac{e^{2}}{8\pi\varepsilon_0 r} $$

**Step 9 — write the potential energy.** For charges $+e$ and $-e$ separated by $r$,
with zero at infinity, the potential energy is negative:

$$ PE = -\frac{e^{2}}{4\pi\varepsilon_0 r} $$

**Step 10 — add them to get the total energy.**

$$ E = \frac{e^{2}}{8\pi\varepsilon_0 r}-\frac{e^{2}}{4\pi\varepsilon_0 r} = -\frac{e^{2}}{8\pi\varepsilon_0 r} $$

**Step 11 — put in the value of $r$ from Step 7.**

$$ E_n = -\frac{e^{2}}{8\pi\varepsilon_0}\cdot\frac{\pi me^{2}}{\varepsilon_0n^{2}h^{2}} $$

**Step 12 — collect the constants.** The $\pi$ cancels and the two $e^{2}$ terms
combine:

$$ E_n = -\frac{me^{4}}{8\varepsilon_0^{2}h^{2}n^{2}} $$

**Result.**

$$ r_n = \frac{\varepsilon_0 n^{2}h^{2}}{\pi m e^{2}} = 0.53\,n^{2}\ \text{Å} $$
$$ E_n = -\frac{me^{4}}{8\varepsilon_0^{2}h^{2}}\cdot\frac{1}{n^{2}} = -\frac{13.6}{n^{2}}\ \text{eV} $$

**What it means.** The radius grows as $n^{2}$, so the orbits get rapidly further
apart: $0.53$, $2.12$, $4.77\ \text{Å}$ and so on. The smallest orbit, $n = 1$, is
the **Bohr radius**, and it sets the size of the hydrogen atom — the atom cannot
collapse because there is no orbit below it. The energy is **negative**, meaning the
electron is bound; it rises towards zero as $n$ increases, and the levels **crowd
together** near the top. Taking the difference of two levels and using
$h\nu = E_i-E_f$ gives
$1/\lambda = R\left(1/n_f^{2}-1/n_i^{2}\right)$ with
$R = me^{4}/8\varepsilon_0^{2}h^{3}c$, and the value of $R$ calculated from these
constants alone agrees with the measured Rydberg constant
$1.097\times10^{7}\ \text{m}^{-1}$. That agreement, from a theory with no adjustable
parameter, is why Bohr's model was accepted at once.

**Conditions.** The atom must have only **one** electron (hydrogen, $\text{He}^{+}$,
$\text{Li}^{2+}$, for which $e^{2}$ becomes $Ze^{2}$ and $E_n = -13.6Z^{2}/n^{2}$);
the nucleus is assumed infinitely heavy, and allowing for its motion changes the
result by about $1$ part in $2000$; the speeds are taken as non-relativistic; and
the whole picture of a definite orbit is, strictly, inconsistent with the
uncertainty principle — it happens to give the right energies for one-electron
atoms and fails for everything else.
:::

::: tip Examiner's note — Quantization of energy
Almost every question here starts from the same two lines — the force equation and
$mvr = nh/2\pi$ — so write them both down even if the question seems to ask for
something else. Keep the two proportionalities straight: $r \propto n^{2}$ but
$E \propto -1/n^{2}$. When you use Rydberg's formula, the **smaller** quantum number
is always $n_f$ and goes first inside the bracket; getting them the wrong way round
gives a negative wavelength. The shortcut $\lambda(\text{nm}) = 1242/E(\text{eV})$
converts between the two halves of this unit in one step and makes checking easy.
For X-rays, remember that $\lambda_{min}$ depends only on the **voltage** while the
characteristic lines depend only on the **target**; questions frequently test
exactly that distinction.
:::

## 3.24 Radioactivity and nuclear reaction

CDC allots **6 teaching hours**. The properties of $\alpha$, $\beta$ and $\gamma$
radiations, the laws of radioactive disintegration and the exponential decay law,
half-life, mean life and decay constant, the Geiger-Müller tube, carbon dating and
the medical uses and hazards of radiation are the examinable core.

**Short answer questions [5 marks each]**

1. (a) Compare $\alpha$-particles, $\beta$-particles and $\gamma$-rays in charge, mass, penetrating power and ionising power. [4] (b) Which is deflected most in a magnetic field and why? [1] <span class="marks">[5]</span> (NEB 2080)
2. (a) State the laws of radioactive disintegration. [2] (b) Write the displacement laws for $\alpha$ and $\beta$ emission and give one example of each. [3] <span class="marks">[5]</span> (NEB 2082)
3. (a) Derive the law of radioactive decay $N = N_0e^{-\lambda t}$. [4] (b) Define the decay constant from your result. [1] <span class="marks">[5]</span> (NEB 2081)
4. (a) Define half-life and mean life and derive the relation $T_{1/2} = 0.693/\lambda$. [3] (b) Show that mean life $\tau = 1/\lambda = T_{1/2}/0.693$. [2] <span class="marks">[5]</span> (NEB 2079 model)
5. (a) A radioactive sample falls to $1/16$ of its initial activity in $80$ minutes. Find the half-life and the decay constant. [3] (b) What fraction remains after a further $40$ minutes? [2] <span class="marks">[5]</span>
6. (a) Define activity and state its units. [2] (b) A source contains $1.0\times10^{18}$ atoms of a nuclide of half-life $20$ minutes; find its activity in becquerel. [3] <span class="marks">[5]</span>
7. (a) Describe the construction and working of a Geiger-Müller tube. [4] (b) What is meant by its dead time? [1] <span class="marks">[5]</span> (NEB 2082 model)
8. (a) Explain the principle of carbon dating. [3] (b) A wooden sample has $25\%$ of the $^{14}\text{C}$ activity of living wood; find its age, given $T_{1/2} = 5730\ \text{years}$. [2] <span class="marks">[5]</span>
9. (a) Define mass defect and binding energy per nucleon. [2] (b) Find the binding energy of $^{4}_{2}\text{He}$ given a mass defect of $0.0304\ \text{u}$ and $1\ \text{u} = 931.5\ \text{MeV}$. [3] <span class="marks">[5]</span>
10. (a) State three medical uses of nuclear radiation. [3] (b) State two health hazards and two safety precautions. [2] <span class="marks">[5]</span> (NEB 2080)

::: note Model answers — short (1–5)
**1.** (a)

| Property | $\alpha$-particle | $\beta$-particle | $\gamma$-ray |
|---|---|---|---|
| Nature | Helium nucleus $^{4}_{2}\text{He}$ | Fast electron | Electromagnetic wave (photon) |
| Charge | $+2e$ | $-e$ | Zero |
| Mass | $4\ \text{u}$ | $1/1836\ \text{u}$ | Zero rest mass |
| Speed | $\approx0.05c$ | up to $0.99c$ | $c$ |
| Penetrating power | Least — stopped by paper or a few cm of air | Moderate — stopped by a few mm of aluminium | Greatest — needs several cm of lead |
| Ionising power | Greatest ($\approx10^{4}$ ion pairs per mm) | Moderate ($\approx10^{2}$) | Least ($\approx1$) |
| Deflection in fields | Small, opposite to $\beta$ | Large | None |

Penetrating power and ionising power always run **opposite** to each other: a heavily ionising particle spends its energy quickly and so does not get far.

(b) The **$\beta$-particle**, by a very large margin. The radius of the path is $r = mv/qB$, so the deflection is greatest for the smallest $m/q$. A $\beta$-particle has a mass about $7300$ times smaller than an $\alpha$-particle and half the charge magnitude, so its $m/q$ is smaller by a factor of about $3670$ and it curves far more sharply. The $\gamma$-ray, being uncharged, is not deflected at all.

**2.** (a) **Laws of radioactive disintegration.** (i) Radioactivity is a **spontaneous nuclear** process, unaffected by temperature, pressure, chemical combination or any other physical condition — it is a property of the nucleus alone. (ii) The disintegration of a particular nucleus is entirely **random**; it is impossible to say which nucleus will decay next or when a given one will decay, and the process obeys only statistical laws. (iii) The **rate of disintegration at any instant is directly proportional to the number of undecayed nuclei present** at that instant:
$$ -\frac{dN}{dt} \propto N \;\Rightarrow\; -\frac{dN}{dt} = \lambda N $$
(iv) In each disintegration one $\alpha$ or one $\beta$ particle is emitted, never both together, and $\gamma$-radiation accompanies them when the daughter nucleus is left excited.

(b) **$\alpha$-decay (Soddy-Fajans displacement law):** the mass number falls by $4$ and the atomic number by $2$, so the daughter is **two places to the left** in the periodic table:
$$ ^{A}_{Z}X \longrightarrow\ ^{A-4}_{Z-2}Y + ^{4}_{2}\text{He} $$
Example: $^{238}_{92}\text{U} \longrightarrow\ ^{234}_{90}\text{Th} + ^{4}_{2}\text{He}$.
**$\beta^{-}$-decay:** a neutron in the nucleus turns into a proton and an electron, which is ejected; the mass number is unchanged and the atomic number **increases by one**, so the daughter is one place to the right:
$$ ^{A}_{Z}X \longrightarrow\ ^{A}_{Z+1}Y + ^{0}_{-1}e $$
Example: $^{234}_{90}\text{Th} \longrightarrow\ ^{234}_{91}\text{Pa} + ^{0}_{-1}e$.
**$\gamma$-emission** changes neither $A$ nor $Z$; it only removes excess excitation energy.

**3.** (a) See the derivation box below. In outline: the third law of disintegration gives $-dN/dt = \lambda N$; separating the variables gives $dN/N = -\lambda\,dt$; integrating from $N_0$ at $t = 0$ to $N$ at time $t$ gives $\ln(N/N_0) = -\lambda t$; and taking exponentials,
$$ N = N_0e^{-\lambda t} $$

(b) The **decay constant** $\lambda$ is the constant of proportionality in $-dN/dt = \lambda N$: it is the fraction of the undecayed nuclei that decay per unit time, or equivalently the probability per unit time that any one nucleus will decay. Its unit is $\text{s}^{-1}$. A large $\lambda$ means a rapidly decaying (short-lived) nuclide. From the exponential law, $\lambda$ is also the reciprocal of the time in which the number falls to $1/e$ of its value.

**4.** (a) **Half-life** $T_{1/2}$ is the time in which half the nuclei originally present have decayed, so that $N = N_0/2$. **Mean life** $\tau$ is the average lifetime of all the nuclei in the sample, from formation to decay.
Putting $N = N_0/2$ at $t = T_{1/2}$ in $N = N_0e^{-\lambda t}$:
$$ \frac{N_0}{2} = N_0e^{-\lambda T_{1/2}} \;\Rightarrow\; e^{-\lambda T_{1/2}} = \frac{1}{2} $$
Taking natural logarithms of both sides,
$$ -\lambda T_{1/2} = \ln\frac{1}{2} = -\ln2 $$
$$ T_{1/2} = \frac{\ln 2}{\lambda} = \frac{0.693}{\lambda} $$

(b) The mean life is the total lifetime of all the nuclei divided by their number. A nucleus that decays between $t$ and $t+dt$ has lived a time $t$, and the number doing so is $\lambda N_0e^{-\lambda t}dt$. Hence
$$ \tau = \frac{1}{N_0}\int_0^{\infty}t\,\lambda N_0e^{-\lambda t}dt = \lambda\int_0^{\infty}te^{-\lambda t}dt $$
The standard integral $\int_0^{\infty}te^{-\lambda t}dt = 1/\lambda^{2}$, so
$$ \tau = \lambda\cdot\frac{1}{\lambda^{2}} = \frac{1}{\lambda} $$
Combining with $T_{1/2} = 0.693/\lambda$,
$$ \tau = \frac{1}{\lambda} = \frac{T_{1/2}}{0.693} = 1.44\,T_{1/2} $$
The mean life is always **longer** than the half-life, because the few very long-lived nuclei pull the average up.

**5.** (a) Activity is proportional to $N$, so the sample falls to $1/16$ of its number.
$$ \frac{1}{16} = \left(\frac{1}{2}\right)^{n} \;\Rightarrow\; n = 4 \text{ half-lives} $$
$$ T_{1/2} = \frac{80}{4} = 20\ \text{minutes} $$
$$ \lambda = \frac{0.693}{T_{1/2}} = \frac{0.693}{20\times60} = 5.78\times10^{-4}\ \text{s}^{-1} $$

(b) A further $40$ minutes is **two** more half-lives, so the fraction remaining falls by a further factor of $2^{2} = 4$:
$$ \frac{N}{N_0} = \frac{1}{16}\times\frac{1}{4} = \frac{1}{64} $$
(equivalently, $6$ half-lives in total in $120$ minutes, and $(1/2)^{6} = 1/64$).
:::

::: note Model answers — short (6–10)
**6.** (a) **Activity** $A$ is the number of disintegrations occurring per second in a sample:
$$ A = -\frac{dN}{dt} = \lambda N = A_0e^{-\lambda t} $$
Its SI unit is the **becquerel (Bq)**, one disintegration per second. The older unit is the **curie (Ci)**, $1\ \text{Ci} = 3.7\times10^{10}\ \text{Bq}$, originally the activity of one gram of radium. The rutherford ($10^{6}\ \text{Bq}$) is also occasionally met.

(b)
$$ \lambda = \frac{0.693}{T_{1/2}} = \frac{0.693}{20\times60} = 5.78\times10^{-4}\ \text{s}^{-1} $$
$$ A = \lambda N = 5.78\times10^{-4}\times1.0\times10^{18} $$
$$ A = 5.8\times10^{14}\ \text{Bq} $$

**7.** (a) **Construction.** A **Geiger-Müller tube** is a hollow metal cylinder, or a glass tube with a conducting inner coating, which serves as the **cathode**. Along its axis runs a fine tungsten wire, the **anode**, insulated from the cylinder and ending in a small bead to avoid a point discharge. The tube is filled with an inert gas such as argon at low pressure (about $10\ \text{cm}$ of mercury) together with a small amount of a **quenching** vapour such as bromine or ethyl alcohol. One end is closed by a thin mica window through which $\alpha$ and $\beta$ particles can enter. A potential difference of about $400\ \text{V}$ is applied between the wire and the cylinder through a high resistance $R$ of a few megohms.
**Working.** The applied voltage is set just below the value at which the gas would break down on its own. When an ionising particle enters, it produces a few ion pairs. The strong radial field near the thin wire accelerates the freed electrons so violently that they ionise further atoms, and those ionise still more: an **avalanche** spreads along the whole length of the wire. A large pulse of current flows momentarily, producing a voltage pulse across $R$, which is amplified and fed to a scaler or ratemeter and counted. The quenching vapour absorbs the ultraviolet photons and neutralises the positive ions before they can strike the cathode and start a spurious second discharge, so the tube recovers and is ready for the next particle.

(b) The **dead time** is the short interval, typically $100$–$200\ \mu\text{s}$, immediately after a count, during which the slow positive-ion sheath around the wire has reduced the field so much that a second particle entering the tube cannot produce a countable avalanche. Any particle arriving during this time is **missed**, so at high count rates the observed rate is lower than the true rate and a dead-time correction must be applied.

**8.** (a) **Carbon dating.** Cosmic-ray neutrons striking nitrogen in the upper atmosphere continuously produce the radioactive isotope $^{14}_{6}\text{C}$, which mixes with ordinary carbon as carbon dioxide. Because production and decay have been in balance for a long time, the ratio of $^{14}\text{C}$ to $^{12}\text{C}$ in the atmosphere is essentially constant. A **living** plant or animal constantly exchanges carbon with its surroundings, so it carries this same ratio and shows a constant $^{14}\text{C}$ activity of about $15$ disintegrations per minute per gram of carbon.
The moment the organism **dies**, the exchange stops. No new $^{14}\text{C}$ enters, and the $^{14}\text{C}$ already there decays with a half-life of $5730$ years. Measuring the residual activity per gram of carbon and comparing it with that of living material gives the number of half-lives that have passed, and hence the age, from $A = A_0e^{-\lambda t}$. The method is reliable for objects between about $500$ and $50\,000$ years old — beyond that too little $^{14}\text{C}$ remains to measure. It is used to date wood, charcoal, bone, cloth and manuscripts.

(b) $25\% = 1/4 = (1/2)^{2}$, so exactly **two** half-lives have elapsed:
$$ t = 2\times5730 = 11\,460\ \text{years} $$
**Check** with the formula: $\lambda = 0.693/5730 = 1.21\times10^{-4}\ \text{yr}^{-1}$, and $t = \ln(4)/\lambda = 1.386/1.21\times10^{-4} = 1.15\times10^{4}$ years. ✓

**9.** (a) **Mass defect** $\Delta m$ is the difference between the sum of the masses of the free, separate nucleons and the actual mass of the nucleus they form:
$$ \Delta m = \left[Zm_p + (A-Z)m_n\right] - M_{nucleus} $$
The missing mass has been converted into the energy released when the nucleus was assembled. **Binding energy** is the corresponding energy, $BE = \Delta m\,c^{2}$ — the energy that would have to be supplied to pull the nucleus completely apart into free nucleons. **Binding energy per nucleon** is $BE/A$; it measures the **stability** of the nucleus and peaks at about $8.8\ \text{MeV}$ near iron ($A \approx 56$), which is why heavy nuclei release energy by fission and light ones by fusion.

(b)
$$ BE = \Delta m\times931.5 = 0.0304\times931.5 = 28.3\ \text{MeV} $$
$$ \frac{BE}{A} = \frac{28.3}{4} = 7.08\ \text{MeV per nucleon} $$
This is unusually high for such a light nucleus, which is why the $\alpha$-particle is exceptionally stable and why heavy nuclei emit it whole rather than emitting separate nucleons.

**10.** (a) **Medical uses.** (i) **Diagnosis with tracers:** a small quantity of a short-lived isotope is given to the patient and its progress followed with a detector — $^{131}\text{I}$ for the thyroid, $^{99m}\text{Tc}$ for bone, kidney and heart scans, $^{24}\text{Na}$ to trace blood circulation and find clots. (ii) **Radiotherapy:** a beam of $\gamma$-rays from a $^{60}\text{Co}$ source, or an implanted source, is directed at a tumour to destroy the rapidly dividing cancer cells, which are more sensitive to radiation than normal tissue. (iii) **Sterilisation:** $\gamma$-radiation sterilises syringes, dressings, sutures and surgical instruments in their sealed packets, without heat. (iv) Radiography with X-rays, and the preservation of food from spoilage.

(b) **Hazards.** (i) **Somatic damage** — radiation ionises the molecules of living cells; large doses cause radiation sickness, burns, loss of hair, damage to the blood-forming tissue and, after long exposure, leukaemia and other cancers. (ii) **Genetic damage** — ionisation in the reproductive cells alters the DNA, and the resulting mutations are passed to later generations. Damage is cumulative, and there is no dose so small that it is certainly harmless.
**Precautions.** (i) Keep the source at the greatest possible distance and handle it with long tongs, never with bare hands, since the dose falls as the inverse square of the distance. (ii) Store sources in thick **lead** containers and work behind lead or concrete shielding, with lead aprons for staff. (iii) Minimise the **time** of exposure and wear a **film badge or dosimeter** so that the accumulated dose is monitored against the permitted limit. (iv) Use the shortest-lived isotope that will do the job, and dispose of radioactive waste properly.
:::

```figure caption="Radioactive decay. The number of undecayed nuclei falls exponentially, halving in each successive half-life: 100%, 50%, 25%, 12.5%, ... and never quite reaching zero."
import numpy as np, matplotlib.pyplot as plt
T = 20.0
t = np.linspace(0, 5*T, 500)
N = 100*0.5**(t/T)
fig, ax = plt.subplots(figsize=(4.8,3.0))
ax.plot(t, N, color=ACCENT, lw=1.8)
for k in range(1, 5):
    tk, Nk = k*T, 100*0.5**k
    ax.plot([tk, tk], [0, Nk], color=MUTED, lw=0.8, ls=':')
    ax.plot([0, tk], [Nk, Nk], color=MUTED, lw=0.8, ls=':')
    ax.plot([tk], [Nk], 'o', color='#A8271F', ms=4.2)
    ax.text(tk+1.5, Nk+3.0, '%.1f%%' % Nk, fontsize=7.6, color='#A8271F')
ax.set_xticks([0, T, 2*T, 3*T, 4*T, 5*T])
ax.set_xticklabels(['0', '$T$', '$2T$', '$3T$', '$4T$', '$5T$'])
ax.set_xlabel('time  (in half-lives $T$)', fontsize=9)
ax.set_ylabel('undecayed nuclei  (% of $N_0$)', fontsize=9)
ax.set_ylim(0, 108); ax.set_xlim(0, 5*T)
ax.grid(True, color=GRID, lw=0.5)
ax.spines[['top','right']].set_visible(False)
```
**Long answer / numerical questions [8 marks each]**

1. (a) State the laws of radioactive disintegration and derive $N = N_0e^{-\lambda t}$. [4] (b) Define half-life and mean life and derive $T_{1/2} = 0.693/\lambda$ and $\tau = 1/\lambda$. [2] (c) A sample falls to $1/16$ of its activity in $80$ minutes. Find the half-life, the decay constant, and the fraction left after $120$ minutes. [2] <span class="marks">[8]</span> (NEB 2081)
2. (a) Compare $\alpha$, $\beta$ and $\gamma$ radiations and state the displacement laws for $\alpha$ and $\beta$ decay with one example of each. [4] (b) Describe the construction and working of a Geiger-Müller tube. [3] (c) What is dead time? [1] <span class="marks">[8]</span> (NEB 2082)
3. (a) Explain the principle of carbon dating and state its range and limitations. [3] (b) Define activity, mass defect and binding energy per nucleon. [2] (c) A wooden relic shows $25\%$ of the $^{14}\text{C}$ activity of living wood ($T_{1/2} = 5730\ \text{yr}$); find its age. A source of $1.0\times10^{18}$ atoms has $T_{1/2} = 20\ \text{min}$; find its activity. [3] <span class="marks">[8]</span> (NEB 2080)

::: note Model answers — long
**1.** (a) **Laws:** radioactivity is a spontaneous nuclear process unaffected by physical or chemical conditions; the decay of an individual nucleus is completely random; and the rate of decay at any instant is proportional to the number of undecayed nuclei present. The derivation from the third law is in the box below; the result is
$$ N = N_0e^{-\lambda t} $$

(b) **Half-life** $T_{1/2}$ is the time for half the nuclei present to decay; **mean life** $\tau$ is the average life of all the nuclei.
Setting $N = N_0/2$ at $t = T_{1/2}$:
$$ \frac{1}{2} = e^{-\lambda T_{1/2}} \;\Rightarrow\; \ln\frac{1}{2} = -\lambda T_{1/2} $$
$$ T_{1/2} = \frac{0.693}{\lambda} $$
For the mean life, the number decaying between $t$ and $t+dt$ is $\lambda N_0e^{-\lambda t}dt$ and each such nucleus lived a time $t$, so
$$ \tau = \frac{1}{N_0}\int_0^{\infty}\lambda N_0te^{-\lambda t}dt = \lambda\cdot\frac{1}{\lambda^{2}} = \frac{1}{\lambda} $$
Hence $\tau = T_{1/2}/0.693 = 1.44\,T_{1/2}$: the mean life exceeds the half-life.

(c)
$$ \frac{1}{16} = \left(\frac12\right)^{4} \;\Rightarrow\; 4\ \text{half-lives in }80\ \text{min} \;\Rightarrow\; T_{1/2} = 20\ \text{min} $$
$$ \lambda = \frac{0.693}{20\times60} = 5.78\times10^{-4}\ \text{s}^{-1} $$
In $120$ minutes there are $120/20 = 6$ half-lives, so
$$ \frac{N}{N_0} = \left(\frac12\right)^{6} = \frac{1}{64} = 1.56\% $$

**2.** (a) The comparison table is in short answer 1(a): $\alpha$ is a helium nucleus, charge $+2e$, mass $4\ \text{u}$, least penetrating but most ionising; $\beta$ is a fast electron, charge $-e$, tiny mass, moderately penetrating and moderately ionising; $\gamma$ is an uncharged, massless photon, most penetrating and least ionising. In a magnetic field $\alpha$ and $\beta$ bend in **opposite** directions ($\beta$ far more sharply, because of its very small $m/q$) while $\gamma$ goes straight through.
**Displacement laws.**
$$ ^{A}_{Z}X \longrightarrow\ ^{A-4}_{Z-2}Y + ^{4}_{2}\text{He} \quad (\alpha) $$
Example: $^{226}_{88}\text{Ra} \longrightarrow\ ^{222}_{86}\text{Rn} + ^{4}_{2}\text{He}$.
$$ ^{A}_{Z}X \longrightarrow\ ^{A}_{Z+1}Y + ^{0}_{-1}e \quad (\beta^{-}) $$
Example: $^{14}_{6}\text{C} \longrightarrow\ ^{14}_{7}\text{N} + ^{0}_{-1}e$.
In $\alpha$-decay the element moves **two** places left in the periodic table; in $\beta$-decay, **one** place right. $\gamma$-emission changes neither $A$ nor $Z$ and simply carries away excitation energy from the daughter nucleus.

(b) **Construction and working:** as described in short answer 7(a). Metal cylinder (cathode) with a fine axial tungsten wire (anode), inert gas at low pressure with a quenching vapour, thin mica window, about $400\ \text{V}$ applied through a few megohms. An entering ionising particle produces a few ion pairs; the intense radial field near the thin wire accelerates the electrons enough to cause a self-sustaining **avalanche**; the resulting current pulse develops a voltage across the resistor, which is amplified and counted. The quenching vapour stops the discharge so the tube is ready for the next particle.

(c) **Dead time** is the interval of $100$–$200\ \mu\text{s}$ after each count during which the sluggish positive-ion sheath near the wire suppresses the field, so a second particle produces no countable pulse. Counts arriving in this interval are lost, and at high rates a correction must be made to obtain the true count rate.

**3.** (a) **Carbon dating.** $^{14}\text{C}$ is produced continuously in the upper atmosphere by cosmic-ray neutrons acting on nitrogen, and it decays with a half-life of $5730$ years, so its proportion in atmospheric carbon dioxide has remained nearly constant. Living things exchange carbon with their surroundings and therefore carry the same $^{14}\text{C}:{^{12}\text{C}}$ ratio, giving an activity of about $15$ counts per minute per gram of carbon. At **death** the exchange stops and the $^{14}\text{C}$ decays without replacement, so the activity falls exponentially. Measuring the present activity per gram and comparing it with the living value gives $t$ from $A = A_0e^{-\lambda t}$.
**Range and limitations:** usable from about $500$ to about $50\,000$ years — after roughly $10$ half-lives too little $^{14}\text{C}$ is left to measure reliably. It works only on **once-living** material (wood, charcoal, bone, cloth, seeds), not on stone or metal. It assumes the atmospheric $^{14}\text{C}$ level has been constant, which is not exactly true (it has been disturbed by volcanic activity, by the burning of fossil fuel and by nuclear weapons testing), so calibration curves from tree rings are used. Contamination of the sample by modern carbon makes it appear too young.

(b) **Activity** $A = \lambda N$ is the number of disintegrations per second; unit the becquerel. **Mass defect** $\Delta m = [Zm_p+(A-Z)m_n] - M_{nucleus}$ is the mass that disappears when free nucleons combine. **Binding energy per nucleon** $= \Delta m\,c^{2}/A$ is the energy needed per nucleon to break the nucleus into its separate parts; it is a direct measure of stability and is greatest ($\approx8.8\ \text{MeV}$) for nuclei near iron.

(c) **Age of the relic.** $25\%$ is $(1/2)^{2}$, so two half-lives:
$$ t = 2\times5730 = 1.15\times10^{4}\ \text{years} $$
**Activity of the source.**
$$ \lambda = \frac{0.693}{20\times60} = 5.78\times10^{-4}\ \text{s}^{-1} $$
$$ A = \lambda N = 5.78\times10^{-4}\times1.0\times10^{18} = 5.8\times10^{14}\ \text{Bq} $$
(That is about $1.6\times10^{4}$ curie — a ferociously hot source, which is why short-lived tracers are used in only microgram quantities.)
:::

::: derivation The law of radioactive decay, $N = N_0e^{-\lambda t}$
We start from the single experimental fact that the decay rate is proportional to
how much undecayed material is left, and reach the exponential law and the half-life.

**Setting up.** A sample contains $N_0$ undecayed nuclei at time $t = 0$ and $N$ at a
later time $t$. Each nucleus decays independently and at random, but the **chance**
that any one nucleus decays in the next second is a fixed number $\lambda$,
characteristic of the nuclide and unaffected by temperature, pressure or chemical
state.

**Step 1 — write the number expected to decay in a short time $dt$.** If each of the
$N$ nuclei has a probability $\lambda\,dt$ of decaying, the expected number of
decays is $N\lambda\,dt$. Since $N$ is falling, the change $dN$ is negative:

$$ -dN = \lambda N\,dt $$

**Step 2 — write it as a rate.** Divide both sides by $dt$:

$$ -\frac{dN}{dt} = \lambda N $$

**Step 3 — separate the variables.** Put everything containing $N$ on one side and
everything containing $t$ on the other. Divide both sides by $N$ and multiply by
$dt$:

$$ \frac{dN}{N} = -\lambda\,dt $$

**Step 4 — integrate both sides between the corresponding limits.** At $t = 0$ the
number is $N_0$; at time $t$ it is $N$:

$$ \int_{N_0}^{N}\frac{dN}{N} = -\lambda\int_0^{t}dt $$

**Step 5 — carry out the two integrations.** The integral of $1/N$ is $\ln N$, and
the integral of $dt$ is $t$:

$$ \left[\ln N\right]_{N_0}^{N} = -\lambda\left[t\right]_0^{t} $$

**Step 6 — put in the limits.**

$$ \ln N - \ln N_0 = -\lambda t $$

**Step 7 — combine the two logarithms.** The difference of two logarithms is the
logarithm of the quotient:

$$ \ln\frac{N}{N_0} = -\lambda t $$

**Step 8 — undo the logarithm.** Raise $e$ to the power of each side:

$$ \frac{N}{N_0} = e^{-\lambda t} $$

**Step 9 — multiply through by $N_0$.**

$$ N = N_0e^{-\lambda t} $$

**Step 10 — find the half-life.** By definition $N = N_0/2$ when $t = T_{1/2}$:

$$ \frac{1}{2} = e^{-\lambda T_{1/2}} $$

**Step 11 — take logarithms of both sides.**

$$ -\ln 2 = -\lambda T_{1/2} $$

**Result.**

$$ N = N_0e^{-\lambda t}, \qquad A = \lambda N = A_0e^{-\lambda t} $$
$$ T_{1/2} = \frac{\ln 2}{\lambda} = \frac{0.693}{\lambda}, \qquad \tau = \frac{1}{\lambda} $$

**What it means.** The number left falls by the **same factor** in every equal
interval of time — a half in every half-life, giving $100\%$, $50\%$, $25\%$,
$12.5\%$ and so on (Figure 21). It never reaches zero exactly, which is why we speak
of a half-life rather than a "total life". Because the activity $A = \lambda N$ is
proportional to $N$, activity obeys exactly the same exponential law, which is what
makes the law testable: one counts clicks, not atoms. Taking logarithms of the
result gives $\ln N = \ln N_0 - \lambda t$, so a graph of $\ln A$ against $t$ is a
**straight line of slope $-\lambda$** — the standard laboratory method of measuring
a half-life. Note that $\lambda$ is fixed by the nucleus alone: an old nucleus is no
more likely to decay than a newly formed one, so radioactive nuclei do not "age".

**Conditions.** The sample must contain a large number of nuclei, since the law is
statistical and fluctuates badly when only a few are left; the daughter product must
be stable, or its own decay must be treated separately; and $\lambda$ must be
constant, which is true to extremely high accuracy because the process is nuclear
and the nucleus is shielded from all chemical and thermal influence.
:::

::: tip Examiner's note — Radioactivity and nuclear reaction
Most numericals here need no calculator at all: express the surviving fraction as a
power of $\tfrac12$, count the half-lives, and stop. Use
$\lambda = 0.693/T_{1/2}$ only when the question asks for $\lambda$ or the activity,
and keep $T_{1/2}$ in **seconds** when a becquerel answer is wanted — forgetting the
$\times60$ is the commonest slip in this unit. In the decay-law derivation, show the
separation of variables and both limits of integration; jumping straight to the
exponential loses half the marks. Learn the displacement laws as movements in the
periodic table ($\alpha$: two places left; $\beta$: one place right), and remember
that penetrating power and ionising power always run in **opposite** order.
:::

## 3.25 Recent trends in physics

CDC allots **6 teaching hours**. This unit is descriptive, so the marks are easy —
seismic waves and the Gorkha earthquake of 2015, gravitational waves,
nanotechnology and the Higgs boson. Learn the definitions and the two or three key
numbers for each topic and the questions answer themselves.

**Short answer questions [5 marks each]**

1. (a) Distinguish between body waves and surface waves in an earthquake. [2] (b) Compare P-waves and S-waves in nature, speed and the media through which they travel. [3] <span class="marks">[5]</span> (NEB 2080)
2. (a) Describe Rayleigh waves and Love waves. [3] (b) Why do surface waves cause most of the damage in an earthquake although they arrive last? [2] <span class="marks">[5]</span> (NEB 2082)
3. (a) Explain how the epicentre of an earthquake is located from the arrival times of P and S waves. [3] (b) If P-waves travel at $8.0\ \text{km s}^{-1}$ and S-waves at $4.0\ \text{km s}^{-1}$ and the S-wave arrives $60\ \text{s}$ after the P-wave, find the distance to the epicentre. [2] <span class="marks">[5]</span>
4. (a) Give an account of the Gorkha earthquake of 2015 — date, magnitude, epicentre and cause. [3] (b) What does the fact that S-waves do not pass through the outer core tell us about it? [2] <span class="marks">[5]</span> (NEB 2081)
5. (a) What are gravitational waves? State two of their properties. [3] (b) How were they first detected, and when? [2] <span class="marks">[5]</span> (NEB 2079 model)
6. (a) Describe the principle of the LIGO detector. [3] (b) Why is the detection of gravitational waves so difficult? [2] <span class="marks">[5]</span>
7. (a) What is nanotechnology? Define the nanometre and the nanoscale. [2] (b) Why do materials behave differently at the nanoscale? [3] <span class="marks">[5]</span> (NEB 2082 model)
8. (a) State four applications of nanotechnology. [3] (b) Mention two possible risks. [2] <span class="marks">[5]</span>
9. (a) What is the Higgs boson and what is the Higgs field supposed to do? [3] (b) Where, when and how was it discovered? [2] <span class="marks">[5]</span> (NEB 2080)

::: note Model answers — short (1–5)
**1.** (a) **Body waves** travel through the **interior** of the Earth, spreading out in three dimensions from the focus; they are the P- and S-waves, they are the **fastest** and arrive first at a seismograph, and their amplitude falls off quickly with distance. **Surface waves** travel along or near the Earth's **surface**, like ripples on water; they are the Rayleigh and Love waves, they are **slower** and arrive last, but they have much larger amplitudes and decay more slowly with distance, so they do most of the damage.

(b)

| | P-wave (primary) | S-wave (secondary) |
|---|---|---|
| Nature | **Longitudinal** — particles vibrate along the direction of travel (compressions and rarefactions) | **Transverse** — particles vibrate at right angles to the direction of travel |
| Speed in crust | $6$–$8\ \text{km s}^{-1}$ — the fastest, so recorded first | $3.5$–$4.5\ \text{km s}^{-1}$, about $0.6$ times the P-speed |
| Media | Travels through **solids, liquids and gases** | Travels through **solids only** |
| Damage | Small | Larger than P |

The reason for the difference in media is that a transverse wave needs a **shear** restoring force, and liquids and gases have no rigidity, so they cannot support shear.

**2.** (a) **Rayleigh waves** travel along the free surface of the ground and make each particle move in a **vertical ellipse**, rolling backwards relative to the direction of propagation — the motion is like that of a water wave, a combination of longitudinal and vertical transverse displacement. They are the slowest seismic waves (about $0.9$ times the S-speed) and usually have the largest amplitude of all; the visible "rolling" of the ground in a strong earthquake is a Rayleigh wave.
**Love waves** are surface waves in which the particles move **horizontally**, side to side, at right angles to the direction of travel and parallel to the surface, with no vertical motion at all. They exist only when a low-velocity surface layer overlies a faster substratum, in which the shear waves are trapped and guided. They travel slightly faster than Rayleigh waves and are particularly destructive to the foundations of buildings, which resist vertical loads well but horizontal shaking badly.

(b) Three reasons. **(i) Amplitude.** Surface waves are confined to a thin layer near the surface, so their energy is spread over an area rather than a volume; their amplitude therefore falls off only as $1/\sqrt{r}$ instead of the $1/r$ of body waves, and they arrive still large at great distances. **(ii) Low frequency and long duration.** They have longer periods and go on shaking for many cycles, so they can drive tall buildings into **resonance** — a building with a natural period matching the wave suffers enormous amplitudes. **(iii) Horizontal motion.** Love waves shake the ground sideways, and ordinary buildings are far weaker against horizontal forces than vertical ones. Arriving last is no protection, because the damage is done by the **amplitude**, not the arrival order.

**3.** (a) P-waves travel faster than S-waves, so the gap between their arrivals grows steadily with distance from the epicentre — the further away the station, the bigger the **S-P time difference**. Each seismograph station measures this difference and converts it into a distance $d$ using the known speeds (or a standard travel-time curve):
$$ \frac{d}{v_s}-\frac{d}{v_p} = \Delta t \;\Rightarrow\; d = \frac{\Delta t}{\dfrac{1}{v_s}-\dfrac{1}{v_p}} $$
This gives the distance but not the direction, so the station can only say that the epicentre lies somewhere on a **circle** of radius $d$ drawn round it on the map. Repeating the measurement at a second station gives a second circle, which cuts the first at two points, and a **third** station resolves the ambiguity: the single point where all three circles intersect is the epicentre. This method is called **triangulation**.

(b)
$$ d = \frac{\Delta t}{\dfrac{1}{v_s}-\dfrac{1}{v_p}} = \frac{60}{\dfrac{1}{4.0}-\dfrac{1}{8.0}} = \frac{60}{0.125} $$
$$ d = 480\ \text{km} $$
**Check:** $t_P = 480/8.0 = 60\ \text{s}$ and $t_S = 480/4.0 = 120\ \text{s}$, a difference of exactly $60\ \text{s}$. ✓

**4.** (a) The **Gorkha earthquake** struck on **25 April 2015** at about $11{:}56$ local time. Its **moment magnitude was $7.8$**, and its epicentre was near **Barpak in Gorkha district**, roughly $80\ \text{km}$ north-west of Kathmandu, at a shallow focal depth of about $15\ \text{km}$. A major aftershock of magnitude $7.3$ followed on **12 May 2015** near Dolakha, and thousands of smaller aftershocks continued for months. Nearly $9000$ people died, about $22\,000$ were injured, and huge numbers of houses and many historic monuments in the Kathmandu valley were destroyed.
**Cause.** Nepal lies on the collision boundary where the **Indian plate is being driven northward beneath the Eurasian plate** at about $45\ \text{mm}$ per year. Friction locks the two plates along the Main Frontal Thrust, strain energy accumulates in the rock for centuries, and when the stress exceeds the strength of the rock the fault slips suddenly, releasing the stored elastic energy as seismic waves. In 2015 a section of the fault about $120\ \text{km}$ long slipped by several metres. The shallow focus and the soft sediments of the Kathmandu valley, which amplified the long-period surface waves, made the shaking especially destructive.

(b) It tells us that the outer core is **liquid**. S-waves are transverse, and a transverse wave needs a shear (rigidity) restoring force. Liquids have no rigidity — they flow rather than resist a shearing stress — so they cannot transmit an S-wave. The observation that no S-waves at all arrive in the **shadow zone** beyond about $103^{\circ}$ from the epicentre, while P-waves do arrive (refracted, and delayed), is the classic evidence that the outer core is molten. The later discovery that P-waves are refracted again at a deeper boundary showed that the inner core is solid.

**5.** (a) **Gravitational waves** are ripples in the curvature of space-time itself, predicted by Einstein's general theory of relativity in 1916 and produced whenever mass is accelerated **unsymmetrically** — for example by two neutron stars or black holes spiralling round each other, or by an asymmetric supernova.
**Properties:** (i) they travel at the **speed of light**; (ii) they are **transverse** — they stretch space in one direction while squeezing it in the perpendicular direction, alternately, as they pass; (iii) they interact with matter extraordinarily weakly, so they pass through the Earth almost undisturbed and can bring information from regions that light cannot escape; (iv) their amplitude falls off as $1/r$, and the strain they produce at the Earth is of order $10^{-21}$; (v) they carry energy away from the source, which is why a binary pulsar's orbit slowly shrinks — the indirect evidence for which Hulse and Taylor won the Nobel Prize in 1993.

(b) They were first detected **directly on 14 September 2015** by the two **LIGO** (Laser Interferometer Gravitational-Wave Observatory) detectors at Hanford and Livingston in the United States; the discovery was announced on 11 February 2016 and the event is named **GW150914**. The signal came from the merger of two **black holes** of about $36$ and $29$ solar masses, about $1.3$ billion light years away, which combined into a single black hole of about $62$ solar masses — roughly **three solar masses** of material being converted into the energy of gravitational waves in a fraction of a second. The Nobel Prize in Physics for 2017 went to Weiss, Barish and Thorne for this work.

:::

::: note Model answers — short (6–9)
**6.** (a) **LIGO** is a giant **Michelson interferometer**. A powerful laser beam is split by a half-silvered mirror into two beams that travel down two evacuated arms set at right angles, each $4\ \text{km}$ long, reflect from mirrors at the far ends (in practice bouncing back and forth hundreds of times in optical cavities to lengthen the effective path), and return to recombine at the detector. The arms are adjusted so that the two returning beams normally interfere **destructively** and the detector sees darkness.
A passing gravitational wave is transverse: it stretches one arm while shrinking the other, then reverses. The two light paths are therefore no longer equal, the path difference changes, and the interference pattern shifts, so a flicker of light appears at the previously dark output. The pattern of that flicker with time is a direct recording of the wave. Two detectors thousands of kilometres apart are used, so that a real signal must appear at both with the correct light-travel delay; local disturbances affect only one.

(b) Because the effect is unimaginably small. A strong astronomical source produces a strain of only about $h \approx 10^{-21}$, so in a $4\ \text{km}$ arm the change in length is
$$ \Delta L = hL \approx 10^{-21}\times4\times10^{3} = 4\times10^{-18}\ \text{m} $$
which is about one **thousandth of the diameter of a proton**. Measuring this requires the mirrors to be suspended in a near-perfect vacuum on elaborate multi-stage isolation systems, cooled and shielded, and protected from seismic tremors, passing traffic, ocean waves, thermal vibration of the mirror atoms and even the random arrival of individual photons. Gravity is by far the weakest of the four fundamental interactions, which is exactly why gravitational waves are so penetrating and so hard to catch.

**7.** (a) **Nanotechnology** is the study, design, production and application of structures, devices and systems by controlling the shape and size of matter at the scale of a few **nanometres**. A **nanometre** is $10^{-9}\ \text{m}$, about the length of ten hydrogen atoms in a row. The **nanoscale** is conventionally the range **$1$ to $100\ \text{nm}$** — big enough to contain hundreds or thousands of atoms, small enough that the ordinary bulk properties of the material no longer apply.

(b) Two effects take over at this size. **(i) The surface-to-volume ratio becomes enormous.** For a cube of side $a$ this ratio is $6/a$, so shrinking the cube from $1\ \text{cm}$ to $1\ \text{nm}$ increases it ten million times. A very large fraction of the atoms are then **surface** atoms, with unsatisfied bonds, so the material becomes far more chemically reactive, a far better catalyst, and melts at a much lower temperature than the bulk. **(ii) Quantum confinement.** When a particle is smaller than the natural wavelength of its electrons, the electron energy levels are no longer continuous bands but become **discrete**, and their spacing depends on the size of the particle. So the optical and electrical properties can be tuned by size alone: cadmium selenide quantum dots of different diameters, made of exactly the same substance, fluoresce in different colours. Gold, which is yellow and inert in bulk, is red in $10\ \text{nm}$ particles and is an excellent catalyst.

**8.** (a) **Applications.** (i) **Medicine:** targeted drug delivery, in which a drug is carried in a nanoparticle that releases it only at a tumour, reducing side effects; nanoparticle contrast agents for imaging; and nanoscale biosensors for early diagnosis. (ii) **Electronics:** transistors with features a few nanometres across, giving faster and denser integrated circuits; memory devices; carbon nanotubes and graphene for flexible, transparent conductors. (iii) **Materials:** carbon-nanotube composites that are exceptionally strong and light for sports equipment and aircraft; scratch-resistant, self-cleaning and water-repellent coatings; stain-resistant fabrics; nano-silver antibacterial coatings. (iv) **Energy and environment:** more efficient solar cells, better battery and fuel-cell electrodes, nano-catalysts, and membranes and nano-filters for purifying water. (v) **Cosmetics:** zinc oxide and titanium dioxide nanoparticles in sunscreens, which block ultraviolet but are transparent.

(b) **Risks.** (i) **Health.** Nanoparticles are small enough to pass through the lungs into the bloodstream and even to cross the blood-brain barrier, and their large reactive surface may damage cells; the long-term effects of inhaling them are not yet known, and some nanotubes behave in the lungs somewhat like asbestos fibres. (ii) **Environment.** They are difficult to detect, filter or clean up once released, and may accumulate in soil, water and living organisms; nano-silver released from fabrics can harm useful bacteria in sewage treatment. (iii) Other concerns are the misuse of invisible nano-sensors for surveillance, possible military applications, and the economic disruption caused if nano-materials replace natural raw materials on which poor countries depend.

**9.** (a) The **Higgs boson** is a fundamental particle of the Standard Model — the quantum, or particle-like excitation, of the **Higgs field**. The Higgs field is supposed to fill all of space uniformly, even in a perfect vacuum. Particles that interact with this field are slowed by it, and this resistance to acceleration is exactly what we call **mass**: the more strongly a particle couples to the Higgs field, the more massive it is, while the photon, which does not couple at all, remains massless. The mechanism (proposed independently in 1964 by Higgs, by Englert and Brout, and by others) is what allows the W and Z bosons to be heavy while the photon is massless, even though the electromagnetic and weak interactions are otherwise unified. Without it the Standard Model would predict that electrons and quarks have no mass, and atoms could not exist. Its mass is about $125\ \text{GeV}/c^{2}$, some $133$ times that of a proton; it has zero charge and **zero spin**, the only known fundamental scalar particle, and it decays almost instantly.

(b) It was discovered at **CERN**, near Geneva, at the **Large Hadron Collider**, and announced on **4 July 2012** by the two independent experiments **ATLAS** and **CMS**. Protons were accelerated in opposite directions round the $27\ \text{km}$ ring and made to collide at very high energy; occasionally a collision produced a Higgs boson, which decayed at once into particles such as two photons or four leptons. The Higgs itself was never seen — it was inferred from a small statistical **excess** of such decay events at a common reconstructed mass of about $125\ \text{GeV}$, which rose above the background as more and more collisions were recorded. Peter Higgs and François Englert received the Nobel Prize in Physics in **2013**.
:::

```figure caption="Seismic waves. P-waves are longitudinal and travel fastest, S-waves are transverse and travel through solids only, and the slower surface waves arrive last but have the largest amplitude."
import numpy as np, matplotlib.pyplot as plt
t = np.linspace(0, 10, 2200)
def burst(t, t0, f, amp, width):
    return amp*np.exp(-((t-t0)/width)**2)*np.sin(2*np.pi*f*(t-t0))
trace = (burst(t, 2.0, 3.0, 0.30, 0.45)
         + burst(t, 4.4, 2.0, 0.55, 0.65)
         + burst(t, 7.0, 0.9, 1.00, 1.40))
fig, ax = plt.subplots(figsize=(5.0,2.9))
ax.plot(t, trace, color=INK, lw=1.0)
ax.axhline(0, color=MUTED, lw=0.7)
marks = [(2.0, 'P\nlongitudinal\nfastest', '#A8271F'),
         (4.4, 'S\ntransverse\nsolids only', ACCENT),
         (7.0, 'surface\n(Rayleigh, Love)\nlargest', '#0B6A62')]
for x, lab, col in marks:
    ax.axvline(x, color=col, lw=0.9, ls=':')
    ax.text(x, 1.52, lab, fontsize=7.4, color=col, ha='center', va='bottom')
ax.set_xlabel('time after the earthquake  (arbitrary units)', fontsize=9)
ax.set_ylabel('ground displacement', fontsize=9)
ax.set_ylim(-1.35, 2.75); ax.set_xlim(0, 10)
ax.set_yticks([])
ax.spines[['top','right','left']].set_visible(False)
```
**Long answer / numerical questions [8 marks each]**

1. (a) Classify seismic waves and compare P-, S-, Rayleigh and Love waves in nature, speed, medium and destructiveness. [4] (b) Explain how the epicentre of an earthquake is located, and what the shadow zone tells us about the Earth's core. [2] (c) The S-wave arrives $60\ \text{s}$ after the P-wave at a station; taking $v_P = 8.0$ and $v_S = 4.0\ \text{km s}^{-1}$, find the distance to the epicentre. [2] <span class="marks">[8]</span> (NEB 2081)
2. (a) What are gravitational waves? State their properties and explain how LIGO detects them. [4] (b) Why is the measurement so difficult? Estimate the arm-length change for a strain of $10^{-21}$ in a $4\ \text{km}$ arm. [2] (c) Give an account of the first detection and its significance. [2] <span class="marks">[8]</span> (NEB 2082)
3. (a) Define nanotechnology and the nanoscale, and explain why matter behaves differently there. [3] (b) State four applications and two risks. [3] (c) What is the Higgs boson, what does the Higgs field do, and how was the particle discovered? [2] <span class="marks">[8]</span> (NEB 2080)

::: note Model answers — long
**1.** (a)

| Wave | Type | Speed | Medium | Damage |
|---|---|---|---|---|
| **P (primary)** | Body, **longitudinal** | $6$–$8\ \text{km s}^{-1}$, fastest | Solid, liquid and gas | Least |
| **S (secondary)** | Body, **transverse** | $3.5$–$4.5\ \text{km s}^{-1}$ | **Solids only** | Moderate |
| **Love** | Surface, transverse but **horizontal** | Slower than S | Needs a surface layer over a faster one | Severe — sideways shaking |
| **Rayleigh** | Surface, **elliptical rolling** motion | Slowest of all | Along the free surface | Greatest amplitude |

The order of arrival at a seismograph is therefore P, then S, then the surface waves (Figure 22). Body waves spread through a volume, so their amplitude falls as $1/r$; surface waves are confined to a thin layer and fall only as $1/\sqrt{r}$, which is why they still dominate the record at great distances and cause most of the destruction.

(b) **Locating the epicentre.** Since P is faster than S, the S-P arrival-time difference grows with distance. Each station converts its measured $\Delta t$ into a distance,
$$ d = \frac{\Delta t}{\dfrac{1}{v_S}-\dfrac{1}{v_P}} $$
and draws a circle of that radius round itself on the map. One station gives a circle, two give two intersection points, and a **third** station picks out the single common point — the epicentre. This is **triangulation**.
**The shadow zone.** Beyond about $103^{\circ}$ of arc from the epicentre, **no S-waves** are received anywhere, and between about $103^{\circ}$ and $142^{\circ}$ no direct P-waves arrive either. The complete absence of S-waves shows that they have met a layer with **no rigidity**, so the outer core must be **liquid**; the refraction and delay of the P-waves that do get through gives the depth of that boundary ($2900\ \text{km}$), and a further refraction inside it reveals a **solid inner core**. Nearly everything we know about the deep interior of the Earth comes from such observations, since no borehole reaches even through the crust.

(c)
$$ d = \frac{\Delta t}{\dfrac{1}{v_S}-\dfrac{1}{v_P}} = \frac{60}{\dfrac{1}{4.0}-\dfrac{1}{8.0}} = \frac{60}{0.250-0.125} $$
$$ d = \frac{60}{0.125} = 480\ \text{km} $$
**Check:** $t_P = 480/8.0 = 60\ \text{s}$, $t_S = 480/4.0 = 120\ \text{s}$, difference $60\ \text{s}$. ✓

**2.** (a) **Gravitational waves** are ripples in the fabric of space-time, predicted by Einstein in 1916, radiated whenever mass undergoes unsymmetrical acceleration. **Properties:** they travel at the speed of light; they are **transverse**, stretching space along one axis while compressing it along the perpendicular axis and then reversing; they interact with matter extremely weakly, so they pass through the Earth essentially unchanged and carry information out of regions from which no light can escape; their amplitude falls as $1/r$; and they carry energy away from their source, gradually shrinking the orbits of binary stars.
**How LIGO detects them.** LIGO is a Michelson interferometer with two evacuated arms $4\ \text{km}$ long at right angles. Laser light is split between the arms, reflected from mirrors at the far ends (many times, in resonant cavities, to increase the effective path length) and recombined. The instrument is set so that the recombined beams normally cancel and the output is dark. A passing gravitational wave lengthens one arm and shortens the other, changing the path difference; the interference is upset and light appears at the output, its variation with time tracing the waveform. Two widely separated detectors must record the same signal, with the right light-travel delay between them, before it is accepted.

(b) The difficulty is the size of the effect. With a strain $h = 10^{-21}$ and $L = 4\ \text{km}$,
$$ \Delta L = hL = 10^{-21}\times4\times10^{3} = 4\times10^{-18}\ \text{m} $$
which is about $1/1000$ of the diameter of a proton, and roughly $10^{-13}$ of the wavelength of the laser light used to measure it. Everything conspires against the measurement: ground tremors, traffic, ocean waves, thermal jiggling of the atoms in the mirrors, residual gas molecules in the tube and the statistical noise of the photons themselves are all far larger. LIGO therefore uses multi-stage pendulum suspensions, an ultra-high vacuum, very high laser power, mirrors of exceptional quality, and coincidence between two detectors $3000\ \text{km}$ apart. Gravity is about $10^{36}$ times weaker than the electromagnetic force, which is both why the waves are so penetrating and why they are so nearly undetectable.

(c) The first direct detection, **GW150914**, was made on **14 September 2015** by both LIGO detectors and announced on 11 February 2016. The source was the merger of two **black holes** of about $36$ and $29$ solar masses at a distance of about $1.3$ billion light years; the final black hole had about $62$ solar masses, so roughly **three solar masses** were radiated away as gravitational waves in a few tenths of a second — briefly outshining, in this form of energy, all the stars in the observable universe.
**Significance:** it was the first direct confirmation of a prediction Einstein made a century earlier; the first direct observation of black holes and of a black-hole merger; and the opening of **gravitational-wave astronomy**, an entirely new way of observing the universe that does not depend on light and can therefore probe the dark and the very early universe. The 2017 Nobel Prize in Physics was awarded for it.

**3.** (a) **Nanotechnology** is the deliberate design, production and use of materials and devices whose structure is controlled at the scale of a few nanometres, where matter behaves differently from the bulk. A **nanometre** is $10^{-9}\ \text{m}$; the **nanoscale** is from $1$ to $100\ \text{nm}$.
**Why matter behaves differently.** Two reasons dominate. **(i) Surface-to-volume ratio.** For a cube of side $a$ the ratio of surface area to volume is $6a^{2}/a^{3} = 6/a$, which is inversely proportional to size. Going from $a = 1\ \text{cm}$ to $a = 1\ \text{nm}$ raises it from $600\ \text{m}^{-1}$ to $6\times10^{9}\ \text{m}^{-1}$ — ten million times greater. An enormous fraction of the atoms are then at the surface with unsatisfied bonds, so nanoparticles are far more reactive, are superb catalysts, and melt far below the bulk melting point. **(ii) Quantum confinement.** When the particle is comparable with the electron's de Broglie wavelength, the electrons are boxed in and their energy levels become **discrete** and size-dependent instead of forming continuous bands. The optical and electrical properties can then be tuned by changing the size alone — quantum dots of the same chemical substance fluoresce red, green or blue according to their diameter.

(b) **Applications:** targeted drug delivery and nanomedicine; nanoscale transistors, memory and graphene electronics; strong light composites and self-cleaning, scratch-resistant coatings; and efficient solar cells, better batteries and nano-membranes for water purification. (Others: sunscreens, antibacterial silver coatings, nano-sensors.)
**Risks:** (i) **health** — particles small enough to enter the bloodstream through the lungs and to cross the blood-brain barrier, with unknown long-term effects and an asbestos-like hazard from some nanotubes; (ii) **environment** — they are hard to detect or remove once released, may accumulate in water, soil and living things, and may disturb useful micro-organisms.

(c) The **Higgs boson** is the quantum of the **Higgs field**, a field believed to fill the whole of space. Particles acquire **mass** by interacting with this field: the stronger the coupling, the greater the resistance to acceleration, and therefore the greater the mass; the photon does not couple and stays massless. This mechanism completes the Standard Model by explaining how the W and Z bosons of the weak interaction can be heavy while the photon is not. The particle has a mass of about $125\ \text{GeV}/c^{2}$ (about $133$ proton masses), zero charge and zero spin.
**Discovery:** at **CERN's Large Hadron Collider** near Geneva, announced on **4 July 2012** by the ATLAS and CMS experiments independently. Protons collided head-on at very high energy; a Higgs boson produced in a rare collision decayed immediately, and its existence was inferred from a statistical **excess** of decay products (two photons, or four leptons) clustering at a common mass near $125\ \text{GeV}$. Higgs and Englert shared the 2013 Nobel Prize.
:::

::: tip Examiner's note — Recent trends in physics
This unit rewards **specific facts**, not vague description. Fix in your memory:
P longitudinal and fastest, S transverse and blocked by liquids (hence the liquid
outer core), Rayleigh rolling and Love horizontal; Gorkha, **25 April 2015**,
magnitude **7.8**, epicentre **Barpak**; LIGO, **14 September 2015**, two black
holes, strain $10^{-21}$; nanoscale **$1$–$100\ \text{nm}$**, with surface-to-volume
ratio and quantum confinement as the two reasons for the new behaviour; Higgs boson,
**CERN, 4 July 2012**, about $125\ \text{GeV}/c^{2}$. One well-placed number is worth
a paragraph of generalities. The only numerical that appears here is the S-P
distance formula, so make sure you can rearrange it quickly.
:::

## Chapter summary

- **Sixty-four of the seventy-five marks are subjective.** Group B carries
  $8\times5 = 40$ and Group C $3\times8 = 24$; the eleven multiple-choice marks of
  Group A cannot rescue a candidate who cannot write. Every question in this chapter
  is built to the real mark splits — $1+2+2$, $2+3$, $1+1+3$ and $1+4$ for the
  five-mark questions, and $2+2+2+2$, $3+3+2$ and $5+3$ for the eight-mark ones.
- **The chapter covers all twenty-five CDC units in spine order**, from Rotational
  dynamics to Recent trends in physics, with at least five short and two long
  questions in each, every one followed by a complete model answer written at the
  length an examiner expects to see in the answer book.
- **Every examinable derivation is worked step by step**, either in a derivation box
  (energy in an inductor, the LCR impedance, Thomson's $e/m$, Einstein's photoelectric
  equation, the Bohr orbit) or inside the model answer itself: the moment of inertia of a
  rod, the vertical spring, Bernoulli's equation, Stokes' law, $C_P-C_V = R$, Carnot
  efficiency, the speed of a pulse in a fluid, pipes and strings, Doppler, fringe width,
  Brewster, the Wheatstone balance, the circular coil, Ampère's law and parallel
  conductors. Each gives one algebraic move per line, so the proof can be reproduced
  under examination pressure rather than recited.
- **Every numerical was recomputed before it was printed**, and the answers are
  written out with units at each step. Where a result can be checked a second way —
  $P = VI\cos\phi$ against $I^{2}R$, $\beta$ against $\alpha/(1-\alpha)$, a Bohr
  energy against a Rydberg wavelength — the check is shown, because writing it earns
  marks and catches slips.
- **A year tag such as (NEB 2081) marks a question that has actually been asked**, in
  that year or in that model set. Untagged questions are new, but are built to the
  same pattern. Where several years carry the same tag, the topic is one that the
  board returns to almost every session and should be prepared first.
- **Twelve figures** carry the parts of the answer that words cannot: the energy graphs
  of SHM, the isotherm and adiabat, the Otto and Carnot cycles, the stationary-wave
  patterns in pipes, the potentiometer circuit, the thermocouple curve, the hysteresis
  loop, the LCR phasor and resonance curve and the rectifier waveforms, with the
  remaining diagrams of the modern-physics units. In the examination, a clear labelled
  diagram is often worth two of the five marks on its own.
- **The units are not equally weighted.** Magnetic field ($9$ h), Quantization of
  energy ($8$ h) and Fluid statics ($9$ h) are the largest, while Wave motion,
  Interference and Photons run to only two or three hours each — but the short units
  supply the opening parts of longer questions, so none can be skipped.
- **Read each Examiner's note.** They record the mistakes that cost marks year after
  year: kelvin inside a square root, $I$ as the reference phasor, the base current in
  microamperes, the smaller quantum number first in Rydberg's formula, and the habit
  of writing down the assumption before the algebra.

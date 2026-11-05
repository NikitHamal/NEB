---
subject: Physics
grade: CEE
unit: 6
title: Gravitation
hours: 1
area: Mechanics
---

Gravitation is the one force that never switches off: it holds the Moon in its
orbit, keeps your feet on the ground in Kathmandu and makes a dropped stone fall
the same way everywhere on Earth. Of the **10 Mechanics questions** in the Physics
paper (official weightage), we estimate about **1** comes from this chapter. It is
almost always a comparison rather than a calculation: $g$ at a height against $g$
at a depth, escape speed against orbital speed, or a "which statement is true"
about the energy of a satellite. Learn the two variation formulas and the sign of
the energy, and the mark is quick.

::: key What the paper asks from this chapter
- $F = Gm_1m_2/r^2$ and $g = GM/R^2$; $G = 6.67\times10^{-11}$ N m² kg⁻².
- Height: $g_h = g\left(\frac{R}{R+h}\right)^2$; depth: $g_d = g\left(1-\frac{d}{R}\right)$ — linear, not inverse-square.
- Latitude: $g_\lambda = g - R\omega^2\cos^2\lambda$; least at the equator, greatest at the poles.
- Field strength $GM/r^2$ (N kg⁻¹); potential $-GM/r$ (J kg⁻¹); potential energy $-GMm/r$.
- Orbital speed $v = \sqrt{GM/r}$; period $T = 2\pi\sqrt{r^3/GM}$, so $T^2 \propto r^3$.
- Satellite energy: $K = GMm/2r$, $U = -GMm/r$, $E = -GMm/2r$ — the total is **negative**.
- Escape speed $v_e = \sqrt{2GM/R} = \sqrt{2gR} = 11.2$ km s⁻¹, and $v_e = \sqrt{2}\,v_{orbital}$.
- Geostationary orbit: period 24 h, above the equator, west to east, height about 36,000 km.
:::

## 6.1 Newton's law of gravitation; acceleration due to gravity and its variation

### The inverse-square law

::: definition Newton's law of gravitation
Every particle of matter attracts every other particle with a force proportional to
the product of their masses and inversely proportional to the square of the distance
between them. The force acts along the line joining the particles.
:::

$$ F = \frac{Gm_1m_2}{r^2} $$

Here $m_1$ and $m_2$ are the masses, $r$ the distance between their centres, and $G$
the **universal gravitational constant**:

$$ G = 6.67\times10^{-11}\ \text{N m}^2\text{kg}^{-2} $$

In vector form, the force on $m_1$ due to $m_2$ is
$\vec F_{12} = -\frac{Gm_1m_2}{r^2}\hat r$, where $\hat r$ points from $m_1$ to
$m_2$; the minus sign is what makes the force **attractive**.

| Property | Meaning |
|---|---|
| Universal | The same value of $G$ everywhere, for every pair of masses |
| Always attractive | There is no gravitational repulsion |
| Mutual | The two forces are an action–reaction pair, equal and opposite, on **different** bodies |
| Central | Acts along the line joining the centres |
| Conservative | Work done depends only on the end points, so a potential energy exists |
| Independent of the medium | No medium is needed; it is not weakened by a vacuum |
| Long range, weakest | Infinite range, but about $10^{36}$ times weaker than the electrostatic force between two protons |

The law was stated for **point masses**. It also holds, exactly, for two uniform
spheres with $r$ measured between their centres — a result Newton proved with the
shell theorem. That is why we may treat the whole Earth as a point at its centre.

### g at the surface of a planet

For a body of mass $m$ on the surface of a planet of mass $M$ and radius $R$, the
gravitational force is its weight:

$$ mg = \frac{GMm}{R^2} \quad\Longrightarrow\quad g = \frac{GM}{R^2} $$

So $g$ is fixed by the planet, not by the falling body: a feather and a hammer have
the same $g$ (they fall differently only because of air resistance). With
$M = \frac{4}{3}\pi R^3\rho$,

$$ g = \frac{4}{3}\pi G\rho R $$

Two planets of the same density have surface gravities proportional to their radii.

| Body | $g$ (m s⁻²) |
|---|---|
| Earth (mean) | 9.8 |
| Moon | 1.62 |
| Mars | 3.7 |
| Jupiter | 24.8 |
| Sun | 274 |

On the Moon $g$ is about one-sixth of the Earth's, so a 60 kg astronaut weighs
about 590 N on Earth but only 97 N on the Moon — the **mass** is 60 kg in both
places.

### Variation with altitude

At a height $h$ above the surface the distance from the centre is $R+h$, so

$$ g_h = \frac{GM}{(R+h)^2} = g\left(\frac{R}{R+h}\right)^2 $$

For $h \ll R$ we may expand:

$$ g_h \approx g\left(1 - \frac{2h}{R}\right) $$

so a small height lowers $g$ by the fraction $2h/R$. The exact formula must be used
when $h$ is comparable with $R$.

| Height | $g_h$ |
|---|---|
| $h = R$ | $g/4$ |
| $h = 2R$ | $g/9$ |
| $h = 3R$ | $g/16$ |
| $h \to \infty$ | 0 |

### Variation with depth — and the mistake almost everyone makes

At a depth $d$ below the surface the body is at distance $R-d$ from the centre. The
temptation is to write $g_d = GM/(R-d)^2$, which would make $g$ **increase** with
depth. That is wrong: the matter outside radius $R-d$ does not pull on the body at
all, so the mass that matters is smaller too.

**Shell theorem.** A uniform spherical shell exerts **no net gravitational force on
a particle anywhere inside it**. So at depth $d$ only the sphere of radius $R-d$
matters; the shell of thickness $d$ outside that radius pulls equally in all
directions and cancels.

```figure caption="Why $g$ falls linearly with depth. At $P$ only the shaded inner sphere of radius $R-d$ pulls; the shell outside that radius pulls equally in every direction, so its forces cancel."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.3))
ax.set_aspect('equal'); ax.axis('off')
R, d = 1.0, 0.32
r = R - d
ax.add_patch(plt.Circle((0,0), R, fc='none', ec=INK, lw=1.5))
ax.add_patch(plt.Circle((0,0), r, fc=ACCENT, alpha=0.16, ec=ACCENT, lw=1.1, ls='--'))
ax.plot([-r,R],[0,0], color=MUTED, lw=0.9)
ax.plot([0,0],[0,R], color=MUTED, lw=0.9, ls=':')
ax.plot([0],[0],'o',color=INK,ms=3.5)
ax.plot([0],[r],'o',color='#A8271F',ms=5,zorder=6)
ax.text(0.06,-0.12,'O',fontsize=9,color=INK)
ax.text(0.09,r+0.02,'P',fontsize=9.5,color='#A8271F')
ax.text(0.52,0.07,'R',fontsize=9,color=MUTED)
ax.text(-0.36,0.08,'R − d',fontsize=9,color=ACCENT,ha='center',va='bottom')
ax.text(0,-0.42,'only this mass\npulls P',fontsize=8.2,color=ACCENT,ha='center',va='center')
ax.annotate('outer shell:\nforces cancel', xy=(-0.70,0.70), xytext=(-1.38,0.98),
            fontsize=8.2, color=MUTED, ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.7,
                            mutation_scale=7, shrinkA=1, shrinkB=0))
ax.set_xlim(-1.42,1.22); ax.set_ylim(-1.18,1.22)
```

Assuming the Earth has uniform density $\rho$,

$$ M' = \frac{4}{3}\pi (R-d)^3\rho = M\frac{(R-d)^3}{R^3} $$

$$ g_d = \frac{GM'}{(R-d)^2} = \frac{GM(R-d)}{R^3} = g\left(1 - \frac{d}{R}\right) $$

The variation with depth is **linear**: $g$ falls steadily from $g$ at the surface to
**zero at the centre**.

| Depth | $g_d$ |
|---|---|
| $d = R/4$ | $3g/4$ |
| $d = R/2$ | $g/2$ |
| $d = 3R/4$ | $g/4$ |
| $d = R$ | 0 |

```figure caption="How $g$ changes with distance from the Earth's centre. Inside the Earth (shaded) $g$ rises linearly from zero at the centre; outside it falls as $1/r^2$. At the surface the two branches meet at $g$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
rin = np.linspace(0,1,100); rout = np.linspace(1,4,300)
ax.fill_between(rin, 0, rin, color=ACCENT, alpha=0.10, lw=0)
ax.plot(rin, rin, color=ACCENT, lw=2.0)
ax.plot(rout, 1/rout**2, color='#A8271F', lw=2.0)
ax.axvline(1, color=MUTED, lw=0.8, ls=':')
ax.plot([0.5],[0.5],'o',color=INK,ms=4)
ax.plot([2.0],[0.25],'o',color=INK,ms=4)
ax.annotate('d = R/2:  g/2', xy=(0.5,0.5), xytext=(0.08,0.92),
            fontsize=8.2, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.annotate('h = R:  g/4', xy=(2.0,0.25), xytext=(2.35,0.47),
            fontsize=8.2, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.text(0.34, 0.20, 'g ∝ r', fontsize=8.5, color=ACCENT)
ax.text(2.25, 0.10, 'g ∝ 1/r²', fontsize=8.5, color='#A8271F')
ax.annotate('surface', xy=(1.02,0.98), xytext=(1.20,0.93), fontsize=8.2,
            color=MUTED, ha='left', va='bottom',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.set_xticks([0,1,2,3,4]); ax.set_xticklabels(['0','R','2R','3R','4R'])
ax.set_yticks([0,0.25,0.5,0.75,1.0]); ax.set_yticklabels(['0','g/4','g/2','3g/4','g'])
ax.set_xlabel('distance from the centre  r'); ax.set_ylabel('g at that distance')
ax.set_xlim(0,4); ax.set_ylim(0,1.08)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

::: caution The depth formula is linear — and it is not the height formula
At a height $h$ the whole Earth still pulls, so $g$ falls as $(R/(R+h))^2$. At a
depth $d$ the outer shell stops pulling, so $g$ falls as $(R-d)/R$. A 1 % drop needs
$d = 0.01R \approx 64$ km but only $h \approx 0.005R \approx 32$ km. Any option that
uses $(R-d)^2$ in the denominator is a distractor built on exactly this error.
:::

::: caution The formula assumes uniform density
The real Earth is denser at the core, so $g$ actually stays close to 9.8 and even
rises slightly down to the core–mantle boundary before falling to zero. The linear
law $g_d = g(1-d/R)$ is the one the syllabus and the paper use, and it is exact only
for a uniform sphere.
:::

### Variation with latitude and the shape of the Earth

A body at latitude $\lambda$ is not at rest in an inertial frame: it goes round the
Earth's axis once a day in a circle of radius $R\cos\lambda$, with angular speed
$\omega = 2\pi/(24\times3600) = 7.27\times10^{-5}$ rad s⁻¹. Part of gravity must
supply this centripetal acceleration, which points towards the axis. Resolving along
the local vertical gives the **effective** value:

$$ g_\lambda = g - R\omega^2\cos^2\lambda $$

- At the **poles** ($\lambda = 90^{\circ}$): $\cos\lambda = 0$, so $g$ is unchanged — **maximum**.
- At the **equator** ($\lambda = 0^{\circ}$): the reduction is greatest,
  $R\omega^2 \approx 0.034$ m s⁻².

The Earth is also slightly **oblate** — the equatorial radius (6378 km) is larger
than the polar radius (6357 km) — which lowers $g$ at the equator further. The two
effects together give about 9.78 m s⁻² at the equator and 9.83 m s⁻² at the poles.
A body taken from the equator to a pole therefore **loses** a little weight but
keeps its mass.

::: example Worked example 6.1 — height against depth
**Problem.** Taking $R = 6400$ km, at what depth and at what height is $g$ less than
its surface value by 1 %?

**Solution.** Depth: $g_d = g(1-d/R)$, so $d/R = 0.01$ and
$d = 0.01\times6400 = 64$ km.

Height: $g_h = g(R/(R+h))^2$. For a 1 % drop,
$R/(R+h) = \sqrt{0.99} = 0.995$, so $h = 6400(1/0.995 - 1) = 32.2$ km. The
approximation $2h/R = 0.01$ gives the same 32 km.

The height needed is **half** the depth: near the surface the inverse-square fall is
twice as fast as the linear one.
:::

::: example Worked example 6.2 — the equator–pole weight difference
**Problem.** A student of mass 70 kg is weighed at the equator and at a pole. Taking
$R = 6.4\times10^6$ m and the rotation period as 24 h, find the difference in weight
caused by the Earth's rotation alone.

**Solution.** $\omega = 2\pi/T = 2\pi/86400 = 7.27\times10^{-5}$ rad s⁻¹.

At the equator the reduction is
$R\omega^2 = (6.4\times10^6)(7.27\times10^{-5})^2 = 0.034$ m s⁻².

So $\Delta W = m\Delta g = 70\times0.034 = 2.4$ N. The weight at the pole is about
686 N, so rotation changes it by only 0.35 % — a real effect, but a small one. The
rest of the pole–equator difference comes from the Earth's flattening.
:::

::: memory Three formulas, three behaviours
Height: **square** in the denominator — falls fast, $g/4$ at $h = R$.
Depth: **linear** — falls slowly, zero at the centre.
Latitude: **cosine squared** — no effect at the poles, largest at the equator.
:::

## 6.2 Gravitational field strength, potential and potential energy

### Field strength

The **gravitational field strength** at a point is the gravitational force per unit
mass placed there:

$$ \vec E_g = \frac{\vec F}{m} = -\frac{GM}{r^2}\hat r $$

Its magnitude is $GM/r^2$ and its SI unit is **N kg⁻¹**, which is identical to
m s⁻² — the field strength *is* the local acceleration of free fall. Near the
Earth's surface it is 9.8 N kg⁻¹ downwards.

Field lines point towards the mass, radially. Their **density** shows the strength:
close to the Earth the lines are crowded, far away they are spread out. Field lines
never cross (a point cannot have two directions of force), and they are
perpendicular to the equipotential surfaces.

::: caution Field is a vector; potential is a scalar
"Do not confuse $GM/r^2$ with $GM/r$." The field is force per unit mass (N kg⁻¹) and
falls as $1/r^2$; the potential is energy per unit mass (J kg⁻¹) and falls as $1/r$.
At the surface, $E_g = g = 9.8$ N kg⁻¹ while $V = -gR = -6.3\times10^7$ J kg⁻¹.
:::

### Potential

::: definition Gravitational potential
The gravitational potential at a point is the work done **per unit mass** by an
external agent in bringing a small test mass from infinity to that point, without
acceleration.
:::

$$ V = -\frac{GM}{r} $$

The zero is chosen at infinity. Because gravity attracts, the agent does **negative**
work as the mass comes in from infinity, so $V$ is **negative** everywhere at a
finite distance and rises towards zero at infinity.

| Quantity | Expression | Unit | Sign |
|---|---|---|---|
| Field strength | $GM/r^2$ | N kg⁻¹ | magnitude, direction towards $M$ |
| Potential | $-GM/r$ | J kg⁻¹ | always negative |
| Potential energy of $m$ | $-GMm/r$ | J | always negative |

The field is the negative gradient of the potential:

$$ E_g = -\frac{dV}{dr} $$

so on a graph of $V$ against $r$ the field is minus the slope. Moving **along** an
equipotential surface requires **zero** work, because the displacement is
perpendicular to the force.

### Potential energy

$$ U = -\frac{GMm}{r} $$

The change in potential energy when a mass moves from $r_1$ to $r_2$ is

$$ \Delta U = GMm\left(\frac{1}{r_1} - \frac{1}{r_2}\right) $$

Moving **away** from the Earth ($r_2 > r_1$) makes $\Delta U$ positive: the external
agent must do work. Moving **towards** the Earth makes it negative: gravity does the
work.

For a small height $h$ above the surface, put $r_1 = R$ and $r_2 = R+h$:

$$ \Delta U = \frac{GMmh}{R(R+h)} \approx \frac{GMmh}{R^2} = mgh $$

So the familiar $mgh$ is only the **near-surface approximation** of $-GMm/r$. It
fails when $h$ is a large fraction of $R$.

::: caution Sign conventions that decide the answer
- $U = 0$ at infinity, and $U$ is negative at every finite distance.
- A **bound** body (a satellite, the Moon) has **negative total energy**.
- "Increases" always means *becomes less negative* when a body moves outward.
- The work done **by gravity** is $-\Delta U$; the work done **by an external agent**
  is $+\Delta U$. The paper often asks for one and offers the other.
:::

### Field and potential inside a sphere

| Region | Field | Potential |
|---|---|---|
| Inside a thin shell | 0 | constant, $-GM/R$ (same as the surface) |
| Inside a uniform solid sphere, radius $r$ | $GMr/R^3$ | $-\frac{GM}{2R^3}(3R^2 - r^2)$ |
| At the centre of a solid sphere | 0 | $-3GM/2R$ (minimum) |

Inside a shell the field is zero but the potential is **not** zero: no force is
needed to move about inside, yet work was needed to bring the mass from infinity to
the shell. This distinction is a favourite "which statement is true" question.

| Distance from the centre | $E_g$ (N kg⁻¹) | $V$ (J kg⁻¹) |
|---|---|---|
| $R$ (surface) | 9.8 | $-6.3\times10^7$ |
| $2R$ | 2.45 | $-3.1\times10^7$ |
| $3R$ | 1.09 | $-2.1\times10^7$ |
| $\infty$ | 0 | 0 |

Doubling the distance quarters the field but only halves the magnitude of the
potential — the $1/r^2$ against $1/r$ difference again.

```figure caption="The gravitational potential well of a mass $M$. The potential $U=-GMm/r$ rises towards zero at infinity. A body with total energy $E<0$ is trapped between the two turning points (shaded); with $E \ge 0$ it escapes."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
x = np.linspace(0.9,6,500)
U = -1/x
ax.plot(x, U, color=ACCENT, lw=2.0)
ax.axhline(0, color=INK, lw=0.9)
x0 = 2.0; E = -1/(2*x0); x1 = 2*x0
ax.axhline(E, color='#A8271F', lw=1.3, ls='--')
xf = np.linspace(x0, x1, 120)
ax.fill_between(xf, E, -1/xf, color='#A8271F', alpha=0.15, lw=0)
ax.plot([x0,x1],[E,E],'o',color='#A8271F',ms=3.5)
ax.text(2.55, E+0.055, 'total energy  E = −GMm/2r', fontsize=8.3, color='#A8271F')
ax.text(2.55, -0.86, 'U = −GMm/r', fontsize=8.5, color=ACCENT)
ax.text(4.35, 0.05, 'E = 0: escape', fontsize=8.2, color=MUTED)
ax.annotate('allowed region', xy=(2.6,-0.42), xytext=(3.0,-0.62), fontsize=8.2,
            color='#A8271F',
            arrowprops=dict(arrowstyle='-', color='#A8271F', lw=0.7))
ax.set_xlabel('distance from the centre  r'); ax.set_ylabel('energy')
ax.set_xlim(0.9,6); ax.set_ylim(-1.05,0.16)
ax.set_yticks([-1,-0.5,0]); ax.set_yticklabels(['−GMm/R','','0'])
ax.set_xticks([])
ax.spines[['top','right']].set_visible(False)
```

::: example Worked example 6.3 — potential, field and the work to climb
**Problem.** A body of mass 5 kg is on the Earth's surface ($R = 6400$ km,
$g = 9.8$ m s⁻²). Find (i) the potential and field at a distance $2R$ from the
centre, and (ii) the work needed to take the body from the surface to that point.

**Solution.** With $GM = gR^2$:

(i) $V = -GM/(2R) = -gR/2 = -(9.8)(6.4\times10^6)/2 = -3.1\times10^7$ J kg⁻¹.
$E_g = GM/(2R)^2 = g/4 = 2.45$ N kg⁻¹, towards the Earth.

(ii) $U_1 = -GMm/R = -mgR = -(5)(9.8)(6.4\times10^6) = -3.14\times10^8$ J.
$U_2 = -GMm/2R = -1.57\times10^8$ J. Work by the agent
$= U_2 - U_1 = 1.57\times10^8$ J.

Note that $mgh$ would give $5\times9.8\times6.4\times10^6 = 3.14\times10^8$ J —
twice the true answer, because $h = R$ is not small.
:::

## 6.3 Satellites: orbital velocity, period, energy, escape velocity, geostationary orbit

A satellite stays in a circular orbit because gravity supplies exactly the
centripetal force it needs. There is no "centrifugal force" pushing it out; the
single force is the pull of the Earth, directed to the centre.

### Orbital velocity

For a satellite of mass $m$ in a circular orbit of radius $r$ (measured from the
Earth's centre) at speed $v$:

$$ \frac{GMm}{r^2} = \frac{mv^2}{r} \quad\Longrightarrow\quad v = \sqrt{\frac{GM}{r}} $$

The mass of the satellite cancels: a 1 kg CubeSat and a 400-tonne space station at
the same radius move at the same speed. Near the surface ($r \approx R$),

$$ v_{orb} = \sqrt{gR} = \sqrt{(9.8)(6.4\times10^6)} = 7.9\ \text{km s}^{-1} $$

Higher orbits are **slower**: $v \propto 1/\sqrt{r}$.

**Newton's cannonball.** Fire a ball horizontally from a very high mountain. It
lands a short way off; fired faster, it lands farther; at 7.9 km s⁻¹ the ground
curves away as quickly as the ball falls and it never lands. An orbit is not a place
where gravity is absent — it is a fall that never reaches the ground.

### Period

The satellite covers $2\pi r$ in one period $T$, so $v = 2\pi r/T$:

$$ T = \frac{2\pi r}{v} = 2\pi\sqrt{\frac{r^3}{GM}} $$

Squaring, $T^2 = \frac{4\pi^2}{GM}r^3$, so

$$ T^2 \propto r^3 $$

which is Kepler's third law. For a satellite skimming the surface,
$T = 2\pi\sqrt{R/g} = 84.6$ min — the lowest possible orbital period around the
Earth.

| Orbit | Radius | Period |
|---|---|---|
| Surface-skimming | $R$ | 84.6 min |
| 400 km (ISS) | $1.06R$ | about 1.5 h |
| GPS | $26\,600$ km | about 12 h |
| Geostationary | $42\,200$ km | 24 h |
| Moon | $3.84\times10^8$ m | 27.3 days |

```figure caption="Orbital period against orbital radius for Earth satellites. The curve is $T=2\pi\sqrt{r^3/GM}$; doubling the radius multiplies the period by $2\sqrt{2}=2.83$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
GM = 4.0e14
r = np.linspace(6.5e6, 4.6e7, 400)
T = 2*np.pi*np.sqrt(r**3/GM)/3600
ax.plot(r/1e6, T, color=ACCENT, lw=2.0)
pts = [(6.8,'ISS  1.5 h', 9.5, 5.0), (26.6,'GPS  12 h', 17.0, 14.5),
       (42.3,'geostationary  24 h', 28.0, 27.6)]
for rr, lab, tx, ty in pts:
    tt = 2*np.pi*np.sqrt((rr*1e6)**3/GM)/3600
    ax.plot([rr],[tt],'o',color='#A8271F',ms=4.5,zorder=5)
    ax.annotate(lab, xy=(rr,tt), xytext=(tx,ty), fontsize=8.2, color=INK, ha='left',
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.set_xlabel('orbital radius  r  (10⁶ m)'); ax.set_ylabel('period  T  (hours)')
ax.set_xlim(5,47); ax.set_ylim(0,31)
ax.set_yticks([0,5,10,15,20,25])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

### Energy of a satellite

$$ K = \frac{1}{2}mv^2 = \frac{GMm}{2r}, \qquad U = -\frac{GMm}{r} $$

$$ E = K + U = -\frac{GMm}{2r} $$

Three relations follow at once, and the paper uses all three:

$$ E = -K, \qquad U = 2E, \qquad U = -2K $$

- The total energy is **negative**: the satellite is bound.
- The **binding energy** — the energy needed to remove it to infinity — is $+GMm/2r$.
- As $r$ increases, $K$ and the magnitude of $U$ both decrease, but $E$ becomes
  **less negative**, that is, it **increases**. Moving a satellite to a higher orbit
  costs energy even though it ends up moving more slowly.

::: caution "Higher orbit" means slower but more energetic
Students remember "higher is slower" and then conclude "higher has less energy". Both
statements are true but about different quantities: $K$ decreases, $E$ increases.
To lift a satellite from $r_1$ to $r_2$ the rocket must supply
$\frac{GMm}{2}\left(\frac{1}{r_1}-\frac{1}{r_2}\right)$.
:::

### Escape velocity

The **escape velocity** is the minimum speed at the surface needed to just reach
infinity. At infinity both $K$ and $U$ are zero, so the total energy at launch must
be at least zero:

$$ \frac{1}{2}mv_e^2 - \frac{GMm}{R} = 0 $$

$$ v_e = \sqrt{\frac{2GM}{R}} = \sqrt{2gR} $$

For the Earth, $v_e = \sqrt{2(9.8)(6.4\times10^6)} = 1.12\times10^4$ m s⁻¹
$= 11.2$ km s⁻¹.

| Feature | Orbital speed | Escape speed |
|---|---|---|
| Formula | $\sqrt{GM/r}$ | $\sqrt{2GM/R}$ |
| Earth value | 7.9 km s⁻¹ | 11.2 km s⁻¹ |
| Depends on | radius of the orbit | mass and radius of the planet |
| Depends on satellite mass | no | no |
| Direction | along the orbit | any direction (ignoring air and rotation) |

Since $v_e = \sqrt{2}\,\sqrt{GM/R} = \sqrt{2}\,v_{orb}$ at the surface, the escape
speed is $1.414$ times the orbital speed. That ratio $\sqrt{2}$ is one of the most
reliable one-mark questions in the chapter.

Escape speed does **not** depend on the mass of the escaping body, and (in the
idealised problem) not on the direction of projection — a stone thrown horizontally
at 11.2 km s⁻¹ escapes just as a vertical one does, though the ground gets in the
way.

### Geostationary orbit

A **geostationary** satellite stays above the same point of the Earth. For that it
must satisfy three conditions:

1. **Period 24 h** — actually one sidereal day, 23 h 56 min 4 s, the time for one
   rotation relative to the stars.
2. **Above the equator** — an orbit over any other latitude would drift north and
   south.
3. **West to east**, the same sense as the Earth's rotation.

Putting $T = 86400$ s into $r = (GMT^2/4\pi^2)^{1/3}$ gives
$r = 4.22\times10^7$ m, so the height above the surface is

$$ h = 4.22\times10^7 - 6.4\times10^6 \approx 3.6\times10^7\ \text{m} = 36\,000\ \text{km} $$

There is only **one** geostationary radius, so all such satellites share a single
ring — the geostationary belt. Their orbital speed is about 3.1 km s⁻¹. They are used
for television, telephone and weather satellites, because a dish on the ground can
be fixed pointing at one spot.

| | Geostationary | Polar (sun-synchronous) |
|---|---|---|
| Orbit | equatorial, circular | passes over the poles |
| Period | 24 h | about 90–100 min |
| Height | 36,000 km | 600–1000 km |
| Ground track | fixed point | whole Earth as it turns |
| Used for | communication, weather | remote sensing, mapping, spy satellites |

### Why launches go east, and from low latitudes

A point on the equator is already moving east at $R\omega = 465$ m s⁻¹ because of the
Earth's rotation (check: $6.4\times10^6 \times 7.27\times10^{-5}$). A rocket launched **eastward** from
near the equator starts with that speed for free, so it needs less fuel to reach
7.9 km s⁻¹. A launch from a higher latitude gets less help (the speed is
$465\cos\lambda$ m s⁻¹), and a **polar** launch gets none at all. This is why space
agencies build launch sites as close to the equator as they can, and why almost all
communication satellites are launched eastward.

### Weightlessness in orbit

An astronaut in the International Space Station is **not** outside gravity: at
400 km, $g = 9.8(6400/6800)^2 = 8.7$ m s⁻², only 11 % less than on the ground. The
station and the astronaut are both falling freely with the same acceleration, so
the floor never pushes on them. The **normal reaction is zero**, and that is what
"weightlessness" means. The same thing happens for a few seconds in a lift whose
cable snaps.

::: example Worked example 6.4 — a satellite at height 2R
**Problem.** A satellite orbits at a height $2R$ above the Earth's surface
($R = 6400$ km, $g = 9.8$ m s⁻²). Find its orbital speed and period.

**Solution.** Here $r = 3R$, so
$v = \sqrt{GM/3R} = \sqrt{gR/3} = 7.9/\sqrt{3} = 4.6$ km s⁻¹.

$T = 2\pi\sqrt{(3R)^3/GM} = 2\pi\sqrt{27R/g} = 84.6\sqrt{27}$ min
$= 84.6\times5.20 = 440$ min $\approx 7.3$ h.

Check with Kepler: the surface-skimming period is 84.6 min at $r = R$; at $r = 3R$
the period is $3^{3/2} = 5.2$ times larger.
:::

::: example Worked example 6.5 — escape speed of another planet
**Problem.** A planet has twice the mass and half the radius of the Earth. Find its
escape speed in terms of the Earth's 11.2 km s⁻¹.

**Solution.** $v_e \propto \sqrt{M/R}$, so

$$ \frac{v_e'}{v_e} = \sqrt{\frac{2M}{M}\cdot\frac{R}{R/2}} = \sqrt{4} = 2 $$

The escape speed is $2\times11.2 = 22.4$ km s⁻¹. A smaller radius more than makes up
for the larger mass, because the body starts deeper in the potential well.
:::

```photogrid label="6.1" cols="2" ratio="1.2" caption="Why astronauts float. (a) The International Space Station orbits at about 420 km. (b) Setting gravity equal to the centripetal force gives the orbital speed v = sqrt(G M / r). With G M = 3.986 x 10^14 m^3/s^2 and r = 6,371 + 420 = 6,791 km, v = 7.66 km/s and the period is T = 2 pi r / v = 92.8 minutes, or 15.6 orbits a day. Gravity at that height is still g = G M / r^2 = 8.64 m/s^2, which is 88 per cent of its surface value of 9.82 m/s^2, so astronauts are not beyond gravity: they and the station fall together, and the escape speed from there would be sqrt(2) times larger, 10.83 km/s."
@ photo id="sci10/iss" cap="The International Space Station: a body in free fall around the Earth"
fit 1.2
focus 0.5 0.5
@ svg cap="Orbit of the ISS to scale, with g at three heights"
import math
GM = 3.986e14; R = 6.371e6; r = R + 4.2e5
v = math.sqrt(GM / r); T = 2 * math.pi * r / v / 60
g0, gi, gg = GM / R ** 2, GM / r ** 2, GM / (R + 35.786e6) ** 2
assert abs(v - 7661) < 5 and abs(T - 92.9) < 0.2 and abs(gi / g0 - 0.880) < 0.002 and abs(gg - 0.2243) < 0.005
ve = math.sqrt(2) * v
facts = dict(r="{:,.0f}".format(r / 1000), v="%.2f" % (v / 1000), T="%.1f" % T, n="%.1f" % (1440 / T), gi="%.2f" % gi, pct="%.0f" % (gi / g0 * 100), g0="%.2f" % g0, ve="%.2f" % (ve / 1000))
f = Fig(300, 236)
f.text(150, 14, "Earth radius 6,371 km; orbit radius %s km" % "{:,.0f}".format(r / 1000), size=10.5, color=NAVY, bold=True)
cx, cy = 90, 100; Rp = 58; rp = Rp * r / R
f.circle(cx, cy, rp, fill="#ffffff", stroke=AMBER, sw=1.6); f.circle(cx, cy, Rp, fill=BLUE, stroke=NAVY, sw=1.6)
f.circle(cx + rp, cy, 4, fill=RED, stroke=RED); f.arrow([(cx + rp, cy), (cx + rp, cy - 30)], color=RED, sw=2); f.arrow([(cx + rp, cy), (cx + rp - 28, cy)], color=TEAL, sw=2)
f.text(cx + rp + 8, cy - 26, "v", size=11, color=RED, bold=True, anchor="start"); f.text(cx + rp - 14, cy + 14, "g", size=11, color=TEAL, bold=True)
f.text(cx, cy + 4, "Earth", size=10.5, color=NAVY, bold=True)
vals = [("surface", g0, NAVY), ("ISS 420 km", gi, AMBER), ("GEO 35,786 km", gg, TEAL)]
for i, (nm, gv, col) in enumerate(vals):
    y = 38 + i * 36
    f.text(190, y, nm, size=10.5, color=col, bold=True, anchor="start"); f.box(190, y + 6, max(gv * 9, 2), 12, "", fill=SOFT, stroke=col, r=2); f.text(190 + max(gv * 9, 2) + 4, y + 12, "%.2f" % gv, size=10.5, color=col, bold=True, anchor="start", vmid=True)
f.text(150, 188, "g in m/s^2; the bars are to one scale", size=10.5, color=SLATE)
f.text(150, 204, "v = %.2f km/s, T = %.1f min, %.1f orbits/day" % (v / 1000, T, 1440 / T), size=10.5, color=NAVY, bold=True)
f.text(150, 220, "weightless = free fall, not zero gravity", size=10.5, color=TEAL, bold=True)
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Newton's law | $F = Gm_1m_2/r^2$, attractive, along the joining line |
| Gravitational constant | $G = 6.67\times10^{-11}$ N m² kg⁻²; $[M^{-1}L^3T^{-2}]$ |
| Surface gravity | $g = GM/R^2 = \frac{4}{3}\pi G\rho R$ |
| Height | $g_h = g(R/(R+h))^2 \approx g(1-2h/R)$; $h=R \Rightarrow g/4$ |
| Depth | $g_d = g(1-d/R)$; $d=R \Rightarrow 0$; $d=R/2 \Rightarrow g/2$ |
| Latitude | $g_\lambda = g - R\omega^2\cos^2\lambda$; equator least, poles greatest |
| Field strength | $E_g = GM/r^2$, N kg⁻¹; $E_g = -dV/dr$ |
| Potential | $V = -GM/r$, J kg⁻¹; zero at infinity; $-gR$ at the surface |
| Potential energy | $U = -GMm/r$; $\Delta U = GMm(1/r_1 - 1/r_2)$; $mgh$ if $h \ll R$ |
| Inside a shell | $E_g = 0$, $V = -GM/R$ (constant) |
| Inside a solid sphere | $E_g = GMr/R^3$; $V = -\frac{GM}{2R^3}(3R^2-r^2)$ |
| Orbital speed | $v = \sqrt{GM/r} = \sqrt{gR^2/r}$; 7.9 km s⁻¹ at the surface |
| Period | $T = 2\pi\sqrt{r^3/GM}$; $T^2 \propto r^3$; 84.6 min at the surface |
| Satellite energy | $K = GMm/2r$, $U = -GMm/r$, $E = -GMm/2r = -K$ |
| Binding energy | $GMm/2r$ |
| Escape speed | $v_e = \sqrt{2GM/R} = \sqrt{2gR}$; 11.2 km s⁻¹; $v_e = \sqrt{2}v_{orb}$ |
| Geostationary | $T = 24$ h, equatorial, west→east, $h \approx 36{,}000$ km, $v \approx 3.1$ km s⁻¹ |
| Useful numbers | $R = 6.4\times10^6$ m; $M = 6\times10^{24}$ kg; $GM = gR^2 = 4.0\times10^{14}$ m³ s⁻² |

## Chapter summary

- Every mass attracts every other with $F = Gm_1m_2/r^2$; the force is always
  attractive, mutual, central and conservative.
- Surface gravity is $g = GM/R^2$; it belongs to the planet, not to the falling body.
- With height $g_h = g(R/(R+h))^2$ (inverse square); with depth
  $g_d = g(1-d/R)$ (linear, because the outer shell pulls equally all round). $g$ is
  zero at the centre.
- Rotation reduces $g$ most at the equator: $g_\lambda = g - R\omega^2\cos^2\lambda$;
  the poles have the largest $g$ and the equator the smallest.
- Field strength $GM/r^2$ is a vector in N kg⁻¹; potential $-GM/r$ is a scalar in
  J kg⁻¹, zero at infinity and negative everywhere else.
- Potential energy is $-GMm/r$; $mgh$ is only its near-surface approximation. The
  work by an external agent is $+\Delta U$.
- Orbital speed $\sqrt{GM/r}$ and period $2\pi\sqrt{r^3/GM}$: higher orbits are
  slower, and $T^2 \propto r^3$.
- Satellite energy: $K = GMm/2r$, $U = -GMm/r$, $E = -GMm/2r$. The total is negative
  and equals $-K$; raising the orbit increases $E$ but decreases $K$.
- Escape speed $\sqrt{2GM/R} = 11.2$ km s⁻¹ is $\sqrt{2}$ times the surface orbital
  speed and is independent of the body's mass.
- A geostationary satellite needs 24 h, the equatorial plane and west-to-east
  motion; its height is about 36,000 km.

## Practice questions

**Set A — Recall (20 questions)**

1. The SI unit of gravitational potential is
   (a) J kg⁻¹ (b) N kg⁻¹ (c) J kg (d) N m² kg⁻²
2. The value of the universal gravitational constant in SI units is
   (a) 9.8 N m² kg⁻² (b) 6.67 × 10⁻¹¹ N kg⁻¹ (c) 6.02 × 10²³ N m² kg⁻² (d) 6.67 × 10⁻¹¹ N m² kg⁻²
3. At the centre of the Earth, the value of the acceleration due to gravity is
   (a) maximum (b) equal to its surface value (c) zero (d) infinite
4. At a depth $d$ below the Earth's surface, the acceleration due to gravity is
   (a) $g(1-2d/R)$ (b) $g(R/(R-d))^2$ (c) $g\sqrt{1-d/R}$ (d) $g(1-d/R)$
5. The gravitational potential at infinity is taken to be
   (a) zero (b) $-GM/R$ (c) infinite (d) $+GM/R$
6. The escape velocity from the Earth's surface is about
   (a) 7.9 km s⁻¹ (b) 11.2 km s⁻¹ (c) 2.4 km s⁻¹ (d) 3.0 × 10⁸ m s⁻¹
7. For a satellite in a circular orbit close to the Earth's surface, the ratio of escape speed to orbital speed is
   (a) 1 (b) 2 (c) √2 (d) 1/√2
8. The period of a geostationary satellite is
   (a) 12 h (b) 24 h (c) 1 h (d) 365 days
9. The height of a geostationary satellite above the Earth's surface is about
   (a) 3600 km (b) 36,000 km (c) 360 km (d) 3,60,000 km
10. The total energy of a satellite of mass m in a circular orbit of radius r is
   (a) $GMm/2r$ (b) $-GMm/2r$ (c) $-GMm/r$ (d) $GMm/r$
11. Which of the following forces is conservative?
   (a) friction (b) air resistance (c) gravitational force (d) thrust of a rocket
12. The SI unit of gravitational field strength is
   (a) N kg⁻¹ (b) J kg⁻¹ (c) N m² kg⁻² (d) kg N⁻¹
13. If M is the mass and R the radius of the Earth, the acceleration due to gravity at its surface is
   (a) $GM/R$ (b) $GM/R^2$ (c) $GM^2/R$ (d) $GMR^2$
14. Compared with its value at the poles, the value of g at the equator is
   (a) greater (b) the same (c) smaller (d) zero
15. Kepler's third law for satellites states that
   (a) $T^2 \propto r^3$ (b) $T \propto r$ (c) $T^2 \propto r$ (d) $T^3 \propto r^2$
16. The gravitational potential energy of two point masses separated by a distance r is
   (a) $-Gm_1m_2/r$ (b) $+Gm_1m_2/r$ (c) $-Gm_1m_2/r^2$ (d) $Gm_1m_2r$
17. The work done in moving a mass along an equipotential surface is
   (a) $mgh$ (b) infinite (c) equal to the potential (d) zero
18. For a satellite in a circular orbit, the potential energy U and kinetic energy K are related by
   (a) $U = K$ (b) $U = 2K$ (c) $U = -2K$ (d) $U = -K/2$
19. The escape velocity of a body from the Earth depends on
   (a) its mass (b) the direction of projection (c) the mass and radius of the Earth (d) its mass and direction of projection
20. The value of g at a height equal to the Earth's radius is
   (a) $g/2$ (b) $g/4$ (c) $g/8$ (d) $g/9$

::: note Answers and explanations — Set A
**1.** (a) — potential is work per unit mass, J kg⁻¹. N kg⁻¹ is field strength, and N m² kg⁻² is G.
**2.** (d) — $G = 6.67\times10^{-11}$ N m² kg⁻². The value 9.8 is $g$ (a local acceleration), and option (b) carries the wrong units for $G$.
**3.** (c) — at the centre the mass inside the body's radius is zero, so by the shell theorem the pull is zero.
**4.** (d) — only the sphere of radius $R-d$ pulls, giving $g(R-d)/R = g(1-d/R)$. Option (b) is the common error of applying the height formula downwards.
**5.** (a) — the zero of potential is chosen at infinity; at every finite distance it is negative.
**6.** (b) — $\sqrt{2gR} = \sqrt{2(9.8)(6.4\times10^6)} = 11.2$ km s⁻¹. 7.9 km s⁻¹ is the orbital speed.
**7.** (c) — $v_e/v_{orb} = \sqrt{2GM/R}\div\sqrt{GM/R} = \sqrt{2}$.
**8.** (b) — geostationary means "fixed relative to the ground", which needs one rotation per day, 24 h.
**9.** (b) — the orbital radius is 42,200 km, so the height above the 6400 km radius is about 36,000 km.
**10.** (b) — $E = K + U = GMm/2r - GMm/r = -GMm/2r$.
**11.** (c) — gravity depends only on position, so the work it does is path-independent. Friction, drag and rocket thrust are not.
**12.** (a) — field strength is force per unit mass, N kg⁻¹, numerically equal to m s⁻².
**13.** (b) — weight $mg = GMm/R^2$ gives $g = GM/R^2$.
**14.** (c) — rotation supplies part of the centripetal acceleration at the equator, and the equatorial radius is larger; both reduce $g$ there.
**15.** (a) — $T^2 = (4\pi^2/GM)r^3$ for every satellite about the same central mass.
**16.** (a) — with zero at infinity the energy is $-Gm_1m_2/r$; the positive sign would mean repulsion.
**17.** (d) — the displacement is perpendicular to the field, so $\vec F\cdot\vec s = 0$ everywhere along the path.
**18.** (c) — $U = -GMm/r$ and $K = GMm/2r$, so $U = -2K$. Equivalently $E = -K$.
**19.** (c) — $v_e = \sqrt{2GM/R}$ contains only the planet's mass and radius; the body's mass cancels and the direction does not enter.
**20.** (b) — $g_h = g(R/(R+R))^2 = g/4$.
:::

**Set B — Understanding (13 questions)**

1. At a height equal to the Earth's radius g is $g/4$. At a depth equal to the Earth's radius it is
   (a) zero (b) $g/4$ (c) $g/2$ (d) infinite
2. Two satellites of different masses move in the same circular orbit. They have the same
   (a) kinetic energy and the same speed (b) kinetic energy but different speeds (c) period and different speeds (d) speed but different kinetic energies
3. Which statement about a satellite in a circular orbit is TRUE?
   (a) its kinetic energy is negative (b) its total energy is negative (c) its potential energy is positive (d) its total energy is zero
4. As a satellite moves from a lower circular orbit to a higher one, its
   (a) speed and total energy both increase (b) speed increases and total energy decreases (c) speed and total energy both decrease (d) speed decreases and total energy increases
5. The weightlessness felt by an astronaut in an orbiting spacecraft is because
   (a) g is zero in space (b) there is no gravity beyond the atmosphere (c) the spacecraft moves at the escape speed (d) the spacecraft and the astronaut fall together with the same acceleration
6. If the Earth shrank to half its present radius with no change in mass, g at its new surface would be
   (a) 4g (b) 2g (c) g/2 (d) unchanged
7. At what depth below the Earth's surface is g half its surface value?
   (a) R/4 (b) R/√2 (c) R/2 (d) R
8. At what height above the surface is g half its surface value? (R = Earth's radius)
   (a) R/2 (b) (√2 − 1)R (c) 2R (d) R
9. At the centre of a uniform solid sphere the gravitational field is zero, but the gravitational potential there is
   (a) zero (b) minimum (c) maximum (d) infinite
10. The escape velocity from the Moon is much smaller than from the Earth mainly because the Moon has
   (a) no atmosphere (b) a longer day (c) smaller mass and radius (d) a smaller orbital speed
11. If the radius of a satellite's circular orbit is doubled, its period becomes
   (a) 2 times (b) √2 times (c) 4 times (d) 2√2 times
12. The gravitational potential at a point inside a thin spherical shell is
   (a) zero (b) inversely proportional to the distance from the centre (c) constant and equal to its value at the surface (d) directly proportional to the distance from the centre
13. A body is projected vertically upward with a speed equal to half the escape velocity. The maximum height reached is (R = Earth's radius)
   (a) R/3 (b) R/4 (c) R/2 (d) R

::: note Answers and explanations — Set B
**1.** (a) — the depth formula is $g(1-d/R)$; at $d = R$ it gives zero. The height case keeps the whole Earth pulling, so it only falls to $g/4$.
**2.** (d) — $v = \sqrt{GM/r}$ has no mass in it, so the speeds are equal; $K = GMm/2r$ is proportional to the satellite's mass, so the kinetic energies differ.
**3.** (b) — $E = -GMm/2r$ is negative for every bound orbit. $K$ is positive and $U$ is negative, so (a) and (c) are impossible.
**4.** (d) — $v \propto 1/\sqrt{r}$ falls, while $E = -GMm/2r$ becomes less negative, that is, it rises.
**5.** (d) — g at 400 km is still 8.7 m s⁻²; the astronaut floats because both craft and astronaut are in free fall, so the normal reaction vanishes.
**6.** (a) — $g = GM/R^2$; halving $R$ multiplies $g$ by $1/(1/2)^2 = 4$.
**7.** (c) — $1-d/R = 1/2$ gives $d = R/2$. The linear law makes this exact.
**8.** (b) — $R/(R+h) = 1/\sqrt{2}$ gives $R+h = R\sqrt{2}$, so $h = (\sqrt{2}-1)R$.
**9.** (b) — $V = -3GM/2R$ at the centre, more negative than the surface value $-GM/R$; the potential is least (most negative) there.
**10.** (c) — $v_e = \sqrt{2GM/R}$; the Moon's $M$ is 1/81 and $R$ about 1/3.7 of the Earth's, so $v_e$ falls to 2.4 km s⁻¹. The absence of an atmosphere is a *consequence*, not the cause.
**11.** (d) — $T \propto r^{3/2}$, so doubling $r$ multiplies $T$ by $2^{3/2} = 2\sqrt{2}$.
**12.** (c) — inside a shell the field is zero, so the potential does not change with position; it keeps the surface value $-GM/R$.
**13.** (a) — energy: $\frac{1}{2}(v_e/2)^2 = \frac{1}{4}\frac{GM}{R}$. Then $\frac{GM}{R}-\frac{GM}{R+h} = \frac{GM}{4R}$, giving $R+h = 4R/3$ and $h = R/3$.
:::

**Set C — Application (10 questions)**

1. Taking R = 6400 km, the value of g at a height of 1600 km is about
   (a) 7.8 m s⁻² (b) 4.9 m s⁻² (c) 6.3 m s⁻² (d) 8.7 m s⁻²
2. Taking R = 6400 km, at what depth is g 1 % less than at the surface?
   (a) 32 km (b) 128 km (c) 640 km (d) 64 km
3. Taking R = 6400 km, at what height is g approximately 1 % less than at the surface?
   (a) 64 km (b) 32 km (c) 128 km (d) 640 km
4. A planet has four times the mass and four times the radius of the Earth. Its escape velocity is
   (a) 11.2 km s⁻¹ (b) 5.6 km s⁻¹ (c) 22.4 km s⁻¹ (d) 44.8 km s⁻¹
5. The orbital speed of a satellite at a height equal to half the Earth's radius (R = 6400 km, g = 9.8 m s⁻²) is about
   (a) 5.6 km s⁻¹ (b) 7.9 km s⁻¹ (c) 6.5 km s⁻¹ (d) 9.8 km s⁻¹
6. A satellite orbits at a height equal to the Earth's radius. Its period is about
   (a) 2 h (b) 4 h (c) 8 h (d) 24 h
7. The energy needed to lift a 100 kg body from the Earth's surface to a height equal to the Earth's radius is about (R = 6400 km, g = 9.8 m s⁻²)
   (a) 6.3 × 10⁹ J (b) 1.6 × 10⁹ J (c) 6.3 × 10⁸ J (d) 3.1 × 10⁹ J
8. The escape velocity from the Moon (M = 7.35 × 10²² kg, R = 1.74 × 10⁶ m, G = 6.67 × 10⁻¹¹ N m² kg⁻²) is about
   (a) 1.2 km s⁻¹ (b) 2.4 km s⁻¹ (c) 4.8 km s⁻¹ (d) 11.2 km s⁻¹
9. Taking GM = 4.0 × 10¹⁴ m³ s⁻², the radius of a geostationary orbit is about
   (a) 4.2 × 10⁷ m (b) 3.6 × 10⁷ m (c) 6.4 × 10⁶ m (d) 1.4 × 10⁸ m
10. A 500 kg satellite orbits at a distance 2R from the Earth's centre (R = 6400 km, g = 9.8 m s⁻²). Its total energy is
   (a) +7.8 × 10⁹ J (b) −1.6 × 10¹⁰ J (c) −7.8 × 10⁹ J (d) −3.9 × 10⁹ J

::: note Answers and explanations — Set C
**1.** (c) — $r = 6400+1600 = 8000$ km, so $g_h = 9.8(6400/8000)^2 = 9.8(0.64) = 6.3$ m s⁻². This is $g/1.5625$, not $g/2$.
**2.** (d) — $d = 0.01R = 64$ km. The linear depth law puts the 1 % point twice as deep as the height law does.
**3.** (b) — $2h/R = 0.01$ gives $h = 32$ km (exactly 32.2 km). Option (a) is the depth answer — the classic swap.
**4.** (a) — $v_e \propto \sqrt{M/R}$; both $M$ and $R$ are multiplied by 4, so the ratio is $\sqrt{4/4} = 1$ and $v_e$ is unchanged at 11.2 km s⁻¹.
**5.** (c) — $r = 1.5R$, so $v = \sqrt{gR^2/1.5R} = \sqrt{gR/1.5} = 7.9/1.225 = 6.5$ km s⁻¹.
**6.** (b) — $T = 84.6\sqrt{2^3} = 84.6\times2.83 = 239$ min $= 4.0$ h.
**7.** (d) — $\Delta U = GMm(1/R - 1/2R) = mgR/2 = 100(9.8)(3.2\times10^6) = 3.1\times10^9$ J. Using $mgh$ with $h = R$ would double it.
**8.** (b) — $v_e = \sqrt{2GM/R} = \sqrt{2(6.67\times10^{-11})(7.35\times10^{22})/1.74\times10^6} = \sqrt{5.6\times10^6} = 2.4$ km s⁻¹.
**9.** (a) — $r = (GMT^2/4\pi^2)^{1/3} = (4.0\times10^{14}(86400)^2/39.5)^{1/3} = 4.2\times10^7$ m. Option (b) is the height above the surface, not the radius.
**10.** (c) — $E = -GMm/2r = -mgR^2/(2)(2R) = -mgR/4 = -(500)(9.8)(6.4\times10^6)/4 = -7.8\times10^9$ J.
:::

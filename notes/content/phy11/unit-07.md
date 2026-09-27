---
subject: Physics
grade: 11
unit: 7
title: Gravitation
hours: 10
area: Mechanics
---

Gravitation is the weakest of the four fundamental interactions, yet it shapes
the largest structures in the universe, because it is always attractive and never
cancels out. One equation written by Newton in 1687 explains a falling apple in
Lumbini, the orbit of the Moon, the tides, the period of a communication
satellite over the equator and the reading on a GPS receiver in Kathmandu. This
unit builds that equation, measures the Earth with it, and then flies satellites.

::: key What this unit is really about
Two families of formulas, and knowing which family a question belongs to.
The **field** family ($F$, $g$) is about forces and varies as $1/r^{2}$. The
**energy** family ($V$, $U$) is about work and varies as $1/r$, and is always
negative. Escape velocity, orbital energy and binding energy all come from the
second family.
:::

## 7.1 Newton's law of gravitation

::: definition Newton's law of universal gravitation
Every particle in the universe attracts every other particle with a force that is
directly proportional to the product of their masses and inversely proportional
to the square of the distance between them. The force acts along the line joining
them.

$$ F = \frac{Gm_1m_2}{r^{2}} $$
:::

$G$ is the **universal gravitational constant**. Its value, first measured by
Henry Cavendish in 1798 with a torsion balance, is

$$ G = 6.67 \times 10^{-11}\ \text{N m}^{2}\text{ kg}^{-2} $$

with dimensions $[M^{-1}L^{3}T^{-2}]$. It is "universal" because it is the same
everywhere, for every pair of masses, at every temperature.

```figure caption="Left: the two forces are equal, opposite and along the line of centres. Right: the inverse-square fall-off — doubling $r$ quarters the force."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, (a1,a2) = plt.subplots(1,2, figsize=(5.2,2.5))
a1.add_patch(Circle((0.9,1.0),0.30,fc=ACCENT,ec=INK,lw=1.1,alpha=.85))
a1.add_patch(Circle((3.6,1.0),0.46,fc='#2e8b57',ec=INK,lw=1.1,alpha=.85))
a1.annotate('$m_1$',(0.9,1.0),ha='center',va='center',color='white',fontsize=9)
a1.annotate('$m_2$',(3.6,1.0),ha='center',va='center',color='white',fontsize=9)
a1.annotate('',xy=(1.95,1.0),xytext=(1.25,1.0),
            arrowprops=dict(arrowstyle='-|>',color='#d9534f',lw=1.8,mutation_scale=12))
a1.annotate('',xy=(2.55,1.0),xytext=(3.2,1.0),
            arrowprops=dict(arrowstyle='-|>',color='#d9534f',lw=1.8,mutation_scale=12))
a1.annotate('$F$',(1.6,1.0),textcoords='offset points',xytext=(0,7),color='#d9534f',fontsize=9.5)
a1.annotate('$F$',(2.9,1.0),textcoords='offset points',xytext=(0,7),color='#d9534f',fontsize=9.5)
a1.annotate('',xy=(3.6,0.35),xytext=(0.9,0.35),
            arrowprops=dict(arrowstyle='<|-|>',color=MUTED,lw=1.0,mutation_scale=9))
a1.annotate('$r$',(2.25,0.35),textcoords='offset points',xytext=(0,-13),color=MUTED,fontsize=9.5)
a1.set_xlim(0,4.6); a1.set_ylim(0,2.0); a1.set_aspect('equal'); a1.axis('off')
r = np.linspace(1,4,300)
a2.plot(r, 1/r**2, color=ACCENT, lw=2.0)
for rr in (1,2,3):
    a2.plot([rr,rr],[0,1/rr**2], color=MUTED, lw=0.8, ls=':')
    a2.plot([0,rr],[1/rr**2,1/rr**2], color=MUTED, lw=0.8, ls=':')
a2.plot([1,2,3],[1,0.25,1/9.],'o',color='#d9534f',ms=4.5)
a2.set_xlim(0,4.2); a2.set_ylim(0,1.15)
a2.set_xticks([1,2,3]); a2.set_xticklabels(['$r$','$2r$','$3r$'])
a2.set_yticks([1,0.25,1/9.]); a2.set_yticklabels(['$F$','$F/4$','$F/9$'])
a2.set_xlabel('separation'); a2.set_ylabel('force')
a2.spines[['top','right']].set_visible(False)
fig.tight_layout()
```

Three points that carry marks:

1. The forces form a **Newton's third law pair** — equal in magnitude, opposite
   in direction — even when the masses are wildly different. The Earth pulls an
   apple with the same force with which the apple pulls the Earth.
2. The law is stated for **point masses**. For a uniform solid sphere it still
   holds exactly, with $r$ measured from the **centre** — Newton proved this.
3. Gravitational force is **independent of the medium** between the bodies and of
   the presence of other masses. Forces from several masses simply add as vectors
   (the principle of superposition).

::: example Worked example 7.1
**Problem.** Taking $g = 9.8\ \text{m s}^{-2}$ at the Earth's surface and
$R = 6.4 \times 10^{6}\ \text{m}$, calculate the mass and the mean density of the
Earth. ($G = 6.67 \times 10^{-11}\ \text{N m}^{2}\text{ kg}^{-2}$.)

**Solution.** For a body of mass $m$ on the surface, its weight *is* the
gravitational pull:

$$ mg = \frac{GMm}{R^{2}} \qquad \Longrightarrow \qquad M = \frac{gR^{2}}{G} $$

$$ M = \frac{9.8 \times (6.4\times10^{6})^{2}}{6.67\times10^{-11}}
= \frac{4.01\times10^{14}}{6.67\times10^{-11}} = 6.0 \times 10^{24}\ \text{kg} $$

Mean density:

$$ \rho = \frac{M}{\frac{4}{3}\pi R^{3}} = \frac{6.0\times10^{24}}{\frac{4}{3}\pi(6.4\times10^{6})^{3}}
= \frac{6.0\times10^{24}}{1.10\times10^{21}} = 5.5 \times 10^{3}\ \text{kg m}^{-3} $$

This is about twice the density of surface rock, which is the first clue that the
Earth has a dense iron core. Cavendish called this "weighing the Earth".
:::

## 7.2 Gravitational field strength

A mass changes the space around it so that any other mass placed there feels a
force. That region is the **gravitational field**.

::: definition Gravitational field strength
The gravitational field strength (or gravitational intensity) at a point is the
force per unit mass experienced by a small test mass placed at that point:

$$ \vec{E} = \frac{\vec{F}}{m} $$

It is a **vector**, measured in N kg⁻¹ (or m s⁻², the same thing), directed
towards the attracting mass.
:::

For a point mass (or outside a uniform sphere) of mass $M$, at distance $r$,

$$ E = \frac{GM/r^{2} \cdot m}{m} = \frac{GM}{r^{2}} $$

At the surface of the Earth $r = R$ and the field strength is exactly what we
call $g$:

$$ g = \frac{GM}{R^{2}} $$

So **$g$ is not a property of the falling body — it is a property of the Earth
and of where you stand.** Field lines point radially inwards; their crowding near
the surface shows where the field is strong.

::: caution Weight and mass are different
Mass (kg) is the amount of matter and is the same everywhere. Weight (N) is the
gravitational force $mg$ and changes with location. A 60 kg student has mass
60 kg on the Moon too, but weighs only about $60 \times 1.62 = 97\ \text{N}$
there instead of $588\ \text{N}$.
:::

## 7.3 Gravitational potential; gravitational potential energy

Gravity is a conservative force, so a potential energy can be defined. The
natural zero is at **infinite separation**, where the force vanishes.

::: derivation Gravitational potential energy $U = -GMm/r$ and potential $V = -GM/r$
We start from the definition of potential energy as the work needed to bring a mass
in from infinity, and reach the $-GMm/r$ formula and the potential that follows from
it.

**Setting up.** A mass $M$ sits at the origin. We bring a small mass $m$ from infinity
(where we agree $U = 0$) slowly in to a distance $r$. "Slowly" means the body has no
kinetic energy at either end, so all the work done shows up as stored energy.

**Step 1 — the force at a general distance $x$.** By Newton's law of gravitation the
attraction on $m$ when it is a distance $x$ from $M$ has magnitude

$$ F_{grav} = \frac{GMm}{x^{2}} $$

and it points inwards, towards $M$.

**Step 2 — fix a sign convention.** Measure $x$ outwards from $M$, so "outwards" is
positive. Gravity pulls **inwards**, i.e. in the direction of decreasing $x$, so as a
signed quantity the gravitational force is

$$ F = -\frac{GMm}{x^{2}} $$

**Step 3 — work done by gravity over a tiny displacement $dx$.** Work is force times
displacement:

$$ dW = F\,dx = -\frac{GMm}{x^{2}}\,dx $$

**Step 4 — add up all the tiny bits from $x = \infty$ to $x = r$:**

$$ W = \int_{\infty}^{r} -\frac{GMm}{x^{2}}\,dx $$

**Step 5 — take the constants outside the integral.** $G$, $M$ and $m$ do not change
during the journey:

$$ W = -GMm\int_{\infty}^{r} \frac{dx}{x^{2}} $$

**Step 6 — integrate $x^{-2}$.** Using
$\int x^{-2}dx = -x^{-1}$:

$$ W = -GMm\left[-\frac{1}{x}\right]_{\infty}^{r} $$

**Step 7 — the two minus signs cancel:**

$$ W = GMm\left[\frac{1}{x}\right]_{\infty}^{r} $$

**Step 8 — put in the limits** (value at the top limit minus value at the bottom
limit):

$$ W = GMm\left(\frac{1}{r} - \frac{1}{\infty}\right) $$

**Step 9 — use $1/\infty = 0$:**

$$ W = \frac{GMm}{r} $$

This is the work done **by gravity** as the mass falls in from infinity, and it is
positive — gravity helped, as you would expect.

**Step 10 — convert that into potential energy.** Whenever a conservative force does
work $W$, the potential energy falls by the same amount:

$$ U(r) - U(\infty) = -W $$

**Step 11 — put in $U(\infty) = 0$ (our chosen zero) and $W = GMm/r$:**

$$ U(r) - 0 = -\frac{GMm}{r} $$

so

$$ U = -\frac{GMm}{r} $$

**Step 12 — get the potential.** The gravitational potential $V$ is defined as the
potential energy **per unit mass**, so divide by $m$:

$$ V = \frac{U}{m} = -\frac{GM}{r} $$

**Result.**

$$ U = -\frac{GMm}{r} \ \ (\text{joule}), \qquad V = -\frac{GM}{r}
\ \ (\text{J kg}^{-1}) $$

Both are **scalars** — there is no direction to worry about, which is what makes
potential so much easier to work with than field.

**What it means.** The sign is not a mistake. We chose $U = 0$ at infinity, and gravity
is always attractive, so every real point is a place you would have to do work to
climb *out* of. Hence $U$ is negative everywhere, deepest (most negative) close in and
rising towards zero far away — a "potential well".

**Conditions used.** $M$ is treated as a point mass (or a uniform sphere, for which
this is exactly true outside it), the mass is moved **slowly** so no kinetic energy is
involved, and the zero of potential is taken at infinity. $U$ belongs to the *pair* of
masses, not to either one alone.
:::

::: tip The examiner is looking for
(i) The statement that $U = 0$ at infinity — write it down; (ii) $F = GMm/x^{2}$ at a
general distance $x$; (iii) the integral with limits $\infty$ to $r$; (iv) the
integration of $1/x^{2}$ shown properly; (v) the negative sign explained in words;
(vi) $V = U/m$ with the unit J kg⁻¹. The explanation of the minus sign is worth a
mark on its own and is almost always missing.
:::

::: key Why the potential is negative
Zero potential is at infinity. Since gravity is always attractive, work must be
done *against* it to take a mass out to infinity, so every finite point is at a
lower energy than infinity, i.e. negative. The potential is most negative at the
centre of the well and rises towards zero as $r \to \infty$.
:::

Field and potential are linked by

$$ E = -\frac{dV}{dr} $$

— the field is the negative gradient (steepness) of the potential.

Near the surface, over heights small compared with $R$, the difference
$U_2 - U_1$ reduces to the familiar $mgh$:

$$ \Delta U = GMm\left(\frac{1}{R} - \frac{1}{R+h}\right) = \frac{GMmh}{R(R+h)}
\approx \frac{GMm}{R^{2}}h = mgh \qquad (h \ll R) $$

So $U = mgh$ is not a different formula — it is the $1/r$ formula in disguise,
valid only close to the ground.

## 7.4 Variation in the value of $g$ due to altitude and depth

::: derivation Variation of $g$ with altitude (height above the surface)
We start from $g = GM/R^{2}$ at the surface and reach a formula for $g$ at a height
$h$ above it.

**Step 1 — $g$ at the surface.** A mass $m$ on the surface is a distance $R$ from the
centre of the Earth, so its weight is $GMm/R^{2}$. But weight is also $mg$, so:

$$ mg = \frac{GMm}{R^{2}} \;\Longrightarrow\; g = \frac{GM}{R^{2}} $$

**Step 2 — $g$ at a height $h$.** At height $h$ the body is a distance $R+h$ from the
centre. The *only* change is the distance, so

$$ g_h = \frac{GM}{(R+h)^{2}} $$

**Step 3 — form the ratio $g_h/g$.** Divide Step 2 by Step 1. The $GM$ cancels:

$$ \frac{g_h}{g} = \frac{1/(R+h)^{2}}{1/R^{2}} = \frac{R^{2}}{(R+h)^{2}} $$

**Step 4 — write it as a single squared bracket:**

$$ g_h = g\left(\frac{R}{R+h}\right)^{2} $$

**Step 5 — divide the top and bottom inside the bracket by $R$.** Dividing top and
bottom by the same thing does not change a fraction:

$$ g_h = g\left(\frac{1}{1 + \dfrac{h}{R}}\right)^{2} $$

**Step 6 — write the reciprocal as a negative power:**

$$ g_h = g\left(1 + \frac{h}{R}\right)^{-2} $$

This formula is **exact**. The next two steps only simplify it for small heights.

**Step 7 — use the binomial expansion.** For small $x$,
$(1+x)^{n} \approx 1 + nx$. Here $x = h/R$ and $n = -2$:

$$ g_h \approx g\left(1 + (-2)\frac{h}{R}\right) $$

**Step 8 — tidy up:**

$$ g_h \approx g\left(1 - \frac{2h}{R}\right) $$

**Result.**

$$ g_h = g\left(1 + \frac{h}{R}\right)^{-2} \quad(\text{exact}), \qquad
g_h \approx g\left(1 - \frac{2h}{R}\right) \quad (h \ll R) $$

**What it means.** $g$ gets smaller as you climb, and for small heights the fractional
drop is $2h/R$ — twice the fraction of the Earth's radius you have climbed. At the top
of Sagarmatha ($h \approx 8.8$ km) this is about $0.28\%$, so $g$ falls from
$9.800$ to about $9.77$ m s⁻². $g$ only becomes zero at infinity.

**Conditions used.** The Earth is treated as a uniform sphere so that it acts like a
point mass at its centre; rotation is ignored. Step 7 needs $h \ll R$ — for a satellite
at $h = R$ you must use the exact form, which gives $g/4$, not $g(1-2) = -g$.
:::

::: derivation Variation of $g$ with depth (below the surface)
We start from the shell theorem and reach a formula for $g$ at a depth $d$ below the
surface — and show that $g$ becomes zero at the centre.

**Setting up.** Treat the Earth as a uniform sphere of radius $R$ and density $\rho$. A
body at depth $d$ is at a distance $(R - d)$ from the centre.

**Step 1 — the shell theorem.** A uniform spherical shell exerts **no net gravitational
force** on anything inside it: the pulls from all sides cancel exactly. So the outer
shell, of thickness $d$, can be ignored, and only the inner sphere of radius $(R-d)$
attracts the body.

**Step 2 — the mass of that inner sphere.** Mass $=$ density $\times$ volume, and the
volume of a sphere is $\frac{4}{3}\pi(\text{radius})^{3}$:

$$ M' = \frac{4}{3}\pi(R-d)^{3}\rho $$

**Step 3 — the field at the body's position.** The inner sphere behaves like a point
mass $M'$ at the centre, a distance $(R-d)$ away:

$$ g_d = \frac{GM'}{(R-d)^{2}} $$

**Step 4 — substitute $M'$ from Step 2:**

$$ g_d = \frac{G}{(R-d)^{2}}\cdot\frac{4}{3}\pi(R-d)^{3}\rho $$

**Step 5 — cancel $(R-d)^{2}$ against two of the three factors in $(R-d)^{3}$,
leaving one:**

$$ g_d = \frac{4}{3}\pi G\rho\,(R-d) $$

**Step 6 — do the same thing at the surface.** Putting $d = 0$ in Step 5 gives the
surface value:

$$ g = \frac{4}{3}\pi G\rho\,R $$

**Step 7 — divide Step 5 by Step 6.** All the constants $\frac{4}{3}\pi G\rho$ cancel:

$$ \frac{g_d}{g} = \frac{R - d}{R} $$

**Step 8 — split the fraction on the right:**

$$ \frac{g_d}{g} = \frac{R}{R} - \frac{d}{R} = 1 - \frac{d}{R} $$

**Step 9 — multiply both sides by $g$:**

$$ g_d = g\left(1 - \frac{d}{R}\right) $$

**Step 10 — put $d = R$ (the centre of the Earth):**

$$ g_{centre} = g(1 - 1) = 0 $$

**Result.**

$$ g_d = g\left(1 - \frac{d}{R}\right), \qquad g = 0 \ \text{at the centre} $$

**What it means.** Unlike the altitude case, $g$ falls **linearly** with depth — and it
reaches exactly zero at the centre, where a body would be weightless because the pulls
from all directions cancel. Notice also that going *up* a small distance $h$ costs
$2h/R$ of $g$, while going *down* the same distance costs only $d/R$ — twice as much is
lost by climbing as by digging.

**Conditions used.** The Earth is assumed to be of **uniform density**, which is the
only way Step 2 works. (In reality the core is far denser, so $g$ actually rises
slightly for the first 3000 km before falling.) Rotation and the non-spherical shape
are ignored.
:::

::: tip The examiner is looking for
For the depth derivation: (i) the shell-theorem statement — "the shell above exerts no
force" — in words; (ii) $M' = \frac{4}{3}\pi(R-d)^{3}\rho$; (iii) the cancellation in
Step 5; (iv) the surface value with $d=0$; (v) the ratio, giving
$g_d = g(1 - d/R)$; (vi) the substitution $d = R$ to show $g = 0$ at the centre. State
the uniform-density assumption — it is frequently a listed mark.
:::

Three consequences follow:

- $g$ decreases **linearly** with depth and reaches **zero at the centre**
  ($d = R$). A body at the centre of the Earth is weightless.
- $g$ decreases with altitude as $1/(R+h)^{2}$, reaching zero only at infinity.
- Near the surface a given small distance costs *twice* as much $g$ going up as
  going down ($2h/R$ against $d/R$).

```figure caption="Left: $g$ inside the Earth rises linearly from zero at the centre, peaks at the surface, then falls as $1/r^2$. Right: the potential well $V = -GM/r$, flat-bottomed inside the Earth and rising towards zero at large $r$."
import numpy as np, matplotlib.pyplot as plt
fig, (a1,a2) = plt.subplots(1,2, figsize=(5.2,2.6))
ri = np.linspace(0,1,120); ro = np.linspace(1,3.4,260)
a1.plot(ri, ri, color='#d9534f', lw=2.0)
a1.plot(ro, 1/ro**2, color=ACCENT, lw=2.0)
a1.axvline(1, color=MUTED, lw=0.9, ls=':')
a1.annotate('surface',(1,1.02),textcoords='offset points',xytext=(4,4),
            color=MUTED,fontsize=8.5)
a1.annotate('depth',(0.52,0.17),ha='center',va='center',
            color='#d9534f',fontsize=8.5)
a1.annotate('altitude',(1.8,1/1.8**2),textcoords='offset points',xytext=(2,12),
            color=ACCENT,fontsize=9)
a1.set_xlim(0,3.4); a1.set_ylim(0,1.25)
a1.set_xticks([0,1,2,3]); a1.set_xticklabels(['0','$R$','$2R$','$3R$'])
a1.set_yticks([0,1]); a1.set_yticklabels(['0','$g$'])
a1.set_xlabel('distance from centre $r$'); a1.set_ylabel('field strength')
ri2 = np.linspace(0,1,120); ro2 = np.linspace(1,3.4,260)
a2.plot(ri2, -(3-ri2**2)/2, color='#d9534f', lw=2.0)
a2.plot(ro2, -1/ro2, color=ACCENT, lw=2.0)
a2.axvline(1, color=MUTED, lw=0.9, ls=':')
a2.axhline(0, color=MUTED, lw=0.9)
a2.set_xlim(0,3.4); a2.set_ylim(-1.7,0.35)
a2.set_xticks([0,1,2,3]); a2.set_xticklabels(['0','$R$','$2R$','$3R$'])
a2.set_yticks([-1.5,-1,0]); a2.set_yticklabels([r'$-\frac{3GM}{2R}$',r'$-\frac{GM}{R}$','0'])
a2.set_xlabel('distance from centre $r$'); a2.set_ylabel('potential $V$')
for a in (a1,a2):
    a.spines[['top','right']].set_visible(False); a.grid(True, alpha=.4)
fig.tight_layout()
```

Two further effects change $g$ over the Earth's surface, both worth a mark:

| Cause | Effect on $g$ |
|---|---|
| Shape: the Earth bulges at the equator ($R_{eq} > R_{pole}$) | $g$ is greatest at the poles ($9.83$), least at the equator ($9.78$) |
| Rotation: $g' = g - R\omega^{2}\cos^{2}\lambda$ at latitude $\lambda$ | reduces $g$ most at the equator, no effect at the poles |

::: example Worked example 7.2
**Problem.** Take $g = 9.8\ \text{m s}^{-2}$ and $R = 6.4\times10^{6}\ \text{m}$.
Find $g$ (a) at the summit of Sagarmatha (Mt. Everest), height $8849\ \text{m}$,
(b) at a height equal to the Earth's radius, and (c) at a depth of $R/2$.

**Solution.**

(a) Here $h = 8849\ \text{m} \ll R$, so use the approximation:

$$ g_h = g\left(1 - \frac{2h}{R}\right) = 9.8\left(1 - \frac{2 \times 8849}{6.4\times10^{6}}\right)
= 9.8(1 - 0.002765) = 9.77\ \text{m s}^{-2} $$

Climbing the highest mountain on Earth reduces your weight by only about $0.28\%$.

(b) Here $h = R$ is not small, so use the exact form:

$$ g_h = g\left(\frac{R}{R+R}\right)^{2} = \frac{g}{4} = 2.45\ \text{m s}^{-2} $$

(c) $g_d = g\left(1 - \dfrac{d}{R}\right) = 9.8\left(1 - \dfrac{1}{2}\right)
= 4.9\ \text{m s}^{-2}$.
:::

::: caution Do not use the binomial form when $h$ is large
$g_h = g(1-2h/R)$ is a first-order approximation. At $h = R$ it would give
$g_h = -9.8\ \text{m s}^{-2}$, which is nonsense. Use it only when
$h$ is a few per cent of $R$ at most; otherwise use $g(R/(R+h))^{2}$.
:::

## 7.5 Centre of mass and centre of gravity

::: definition Centre of mass and centre of gravity
The **centre of mass** of a system is the point at which the whole mass may be
considered concentrated for the purpose of describing translational motion:

$$ x_{cm} = \frac{\sum m_i x_i}{\sum m_i}, \qquad y_{cm} = \frac{\sum m_i y_i}{\sum m_i} $$

The **centre of gravity** is the point through which the resultant weight of the
body acts.
:::

In a **uniform** gravitational field the two points coincide, because each mass
element is weighted by the same $g$. They separate only when the body is so tall
that $g$ differs measurably across it — for a mountain or a long satellite, the
centre of gravity lies slightly *below* the centre of mass, because the lower
parts are pulled harder. For anything of laboratory size the distinction is
academic, but NEB asks for it.

| | Centre of mass | Centre of gravity |
|---|---|---|
| Depends on | mass distribution only | mass distribution **and** the field |
| Exists in zero gravity? | Yes | No |
| Position for a uniform field | same point | same point |
| Position for a very large body | fixed | slightly towards the stronger field |

```figure caption="Locating the centre of gravity of an irregular lamina. When the body hangs freely, G lies on the vertical through the point of suspension; repeating with a second point fixes G at the intersection."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, (a1,a2) = plt.subplots(1,2, figsize=(5.2,2.8))
P = np.array([[0.4,0.5],[2.6,0.15],[3.8,1.6],[3.1,3.3],[1.5,3.6],[0.15,2.3]])
x, y = P[:,0], P[:,1]; xs, ys = np.roll(x,-1), np.roll(y,-1)
cr = x*ys - xs*y; A = cr.sum()/2.0
G = np.array([((x+xs)*cr).sum()/(6*A), ((y+ys)*cr).sum()/(6*A)])
iA, iB = 4, 2          # two suspension vertices
def draw(ax, i, show_other, other):
    v = P[i] - G
    rot = np.pi/2 - np.arctan2(v[1], v[0])
    c, s = np.cos(rot), np.sin(rot)
    M = np.array([[c,-s],[s,c]])
    Q = (P - G) @ M.T
    ax.add_patch(Polygon(Q, closed=True, fc='#e7ebf1', ec=INK, lw=1.3))
    top = Q[i]
    ax.plot([top[0]-0.55, top[0]+0.55],[top[1]+0.30]*2, color=INK, lw=1.6)
    ax.plot([top[0],top[0]],[top[1]+0.30, top[1]], color=MUTED, lw=1.0)
    ax.plot([top[0],top[0]],[top[1], -2.5], color='#d9534f', lw=1.2, ls='--')
    ax.plot([top[0]],[top[1]],'o',color=INK,ms=4.5)
    ax.annotate('A' if i==iA else 'B', top, textcoords='offset points',
                xytext=(7,2), color=INK, fontsize=9.5)
    if show_other:
        w = Q[other]
        d = w - np.array([0,0])
        d = d/np.hypot(*d)
        ax.plot([-d[0]*2.6, d[0]*2.6], [-d[1]*2.6, d[1]*2.6],
                color='#2e8b57', lw=1.2, ls=':')
        end = np.array([-d[0]*2.45, -d[1]*2.45])
        if end[0] > 0:
            end = -end
        ax.annotate('line found\nfrom A', end, textcoords='offset points',
                    xytext=(-4,-6), ha='right', va='top',
                    color='#2e8b57', fontsize=8.2)
    ax.plot([0],[0],'o',color='#d9534f',ms=6)
    ax.annotate('G',(0,0),textcoords='offset points',xytext=(8,-10),
                color='#d9534f',fontsize=11)
    ax.set_xlim(-2.9,2.9); ax.set_ylim(-2.7,2.9)
    ax.set_aspect('equal'); ax.axis('off')
draw(a1, iA, False, iB)
draw(a2, iB, True, iA)
a1.set_title('suspended at A', fontsize=9, color=MUTED)
a2.set_title('suspended at B', fontsize=9, color=MUTED)
fig.tight_layout()
```

::: example Worked example 7.3
**Problem.** Three particles of masses $1\ \text{kg}$, $2\ \text{kg}$ and
$3\ \text{kg}$ are placed at the points $(0,0)$, $(6,0)$ and $(0,6)$ metres.
Locate their centre of mass.

**Solution.** Total mass $M = 1+2+3 = 6\ \text{kg}$.

$$ x_{cm} = \frac{1(0) + 2(6) + 3(0)}{6} = \frac{12}{6} = 2\ \text{m} $$
$$ y_{cm} = \frac{1(0) + 2(0) + 3(6)}{6} = \frac{18}{6} = 3\ \text{m} $$

The centre of mass is at $(2, 3)\ \text{m}$. Note it lies nearer the heavier
masses, and it need not be at the position of any actual particle.
:::

## 7.6 Motion of a satellite: orbital velocity and time period

A satellite in a circular orbit of radius $r$ around a planet of mass $M$ is held
there because the gravitational attraction plays the part of the centripetal
force.

::: derivation Orbital velocity and time period of a satellite
We start from the single physical idea that gravity *is* the centripetal force for a
satellite, and reach expressions for its orbital speed and its period — and Kepler's
third law as a bonus.

**Setting up.** A satellite of mass $m$ moves in a circle of radius $r = R + h$ about a
planet of mass $M$ and radius $R$, at a height $h$ above the surface, with orbital
speed $v_o$.

**Step 1 — the gravitational force on the satellite.** By Newton's law of gravitation,
at a distance $r$ from the centre:

$$ F_{grav} = \frac{GMm}{r^{2}} $$

**Step 2 — the centripetal force it needs.** To move in a circle of radius $r$ at speed
$v_o$, a mass $m$ needs an inward force

$$ F_{cent} = \frac{mv_o^{2}}{r} $$

**Step 3 — equate them.** Gravity is the *only* force acting, so it must be exactly the
force required — no more and no less:

$$ \frac{GMm}{r^{2}} = \frac{mv_o^{2}}{r} $$

**Step 4 — cancel $m$ from both sides.** It appears once on each side, so the answer
will not depend on the satellite's mass:

$$ \frac{GM}{r^{2}} = \frac{v_o^{2}}{r} $$

**Step 5 — multiply both sides by $r$:**

$$ \frac{GM}{r} = v_o^{2} $$

**Step 6 — take the square root:**

$$ v_o = \sqrt{\frac{GM}{r}} = \sqrt{\frac{GM}{R+h}} $$

**Step 7 — rewrite using surface quantities.** At the surface $g = GM/R^{2}$, so
$GM = gR^{2}$. Substitute:

$$ v_o = \sqrt{\frac{gR^{2}}{R+h}} $$

**Step 8 — take $R^{2}$ out of the root as $R$:**

$$ v_o = R\sqrt{\frac{g}{R+h}} $$

**Step 9 — the period.** The satellite travels one circumference $2\pi r$ in one period
$T$ at steady speed $v_o$, so time $=$ distance $\div$ speed:

$$ T = \frac{2\pi r}{v_o} $$

**Step 10 — substitute $v_o$ from Step 6:**

$$ T = \frac{2\pi r}{\sqrt{\dfrac{GM}{r}}} $$

**Step 11 — dividing by $\sqrt{GM/r}$ is the same as multiplying by
$\sqrt{r/GM}$:**

$$ T = 2\pi r\sqrt{\frac{r}{GM}} $$

**Step 12 — bring the $r$ outside the root inside it, where it becomes $r^{2}$:**

$$ T = 2\pi\sqrt{\frac{r^{2}\cdot r}{GM}} = 2\pi\sqrt{\frac{r^{3}}{GM}} $$

**Step 13 — square both sides:**

$$ T^{2} = 4\pi^{2}\,\frac{r^{3}}{GM} $$

**Step 14 — group the constants.** $4\pi^{2}$, $G$ and $M$ are all fixed for a given
planet:

$$ T^{2} = \left(\frac{4\pi^{2}}{GM}\right)r^{3} \;\Longrightarrow\; T^{2} \propto r^{3} $$

**Result.**

$$ v_o = \sqrt{\frac{GM}{R+h}} = R\sqrt{\frac{g}{R+h}}, \qquad
T = 2\pi\sqrt{\frac{r^{3}}{GM}}, \qquad T^{2} \propto r^{3} $$

That last line is **Kepler's third law** — here *derived* from Newton's laws rather
than assumed from observation.

**What it means.** The satellite's mass cancelled in Step 4, so a tiny cubesat and a
space station at the same height orbit at the same speed and with the same period. A
higher orbit is a *slower* orbit ($v_o \propto 1/\sqrt{r}$) with a longer period — which
is why a geostationary satellite has to sit 36 000 km up. For a satellite skimming the
surface, $h \approx 0$ and $v_o = \sqrt{gR} \approx 7.9$ km s⁻¹.

**Conditions used.** The orbit is **circular** (for an ellipse, $r$ becomes the mean
distance), there is no air resistance, the planet is a uniform sphere, and the
satellite's mass is far smaller than the planet's so the planet does not move.
:::

::: tip The examiner is looking for
(i) The sentence "the gravitational force provides the centripetal force";
(ii) both force expressions written out; (iii) the cancellation of $m$, and a comment
that the speed is therefore independent of the satellite's mass; (iv) the substitution
$GM = gR^{2}$ if the question gives $g$ and $R$ rather than $G$ and $M$; (v) $T = 2\pi
r/v_o$ and the final $T^{2} \propto r^{3}$ named as Kepler's third law.
:::

```figure caption="Newton's thought experiment. Fired slowly, the projectile falls back; at $v_o = \sqrt{GM/r}$ the fall exactly matches the curvature of the Earth and it orbits; beyond $v_e = \sqrt{2GM/r}$ it never returns."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.6,3.2))
ax.add_patch(Circle((0,0),1.0,fc='#dce6f0',ec=INK,lw=1.2))
r0 = 1.45
vc = np.sqrt(1.0/r0); ve = np.sqrt(2.0/r0)
def orbit(v):
    p = (r0*v)**2; e = abs(r0*v**2 - 1.0); peri = (r0*v**2 >= 1.0)
    th = np.linspace(0, 2*np.pi, 1400)
    den = 1 + e*np.cos(th) if peri else 1 - e*np.cos(th)
    rr = np.where(np.abs(den) < 1e-3, np.nan, p/np.where(np.abs(den)<1e-3, 1, den))
    bad = ~np.isfinite(rr) | (rr < 1.0) | (rr > 6.0) | (den <= 0)
    cut = np.argmax(bad) if bad.any() else len(th)
    return rr[:cut], th[:cut]
for v, c in [(0.55*vc,'#8a8f99'), (0.80*vc,'#b8860b'), (vc,'#d9534f'),
             (1.20*vc,ACCENT), (1.04*ve,'#2e8b57')]:
    rr, th = orbit(v)
    ax.plot(rr*np.cos(th), rr*np.sin(th), color=c, lw=1.6)
ax.plot([r0],[0],'o',color=INK,ms=5)
ax.annotate('cannon on\na high peak',(r0,0),textcoords='offset points',xytext=(7,-20),
            color=INK,fontsize=8.4)
ax.annotate('falls back',(1.30,0.92),color='#8a8f99',fontsize=8.4,
            ha='left',textcoords='offset points',xytext=(10,-2))
ax.annotate('longer fall',(0.86,1.48),color='#b8860b',fontsize=8.4,
            ha='left',textcoords='offset points',xytext=(10,2))
ax.annotate('circular orbit',(-3.4,0.9),color='#d9534f',fontsize=8.4)
ax.annotate('ellipse',(-3.6,-0.55),color=ACCENT,fontsize=8.4)
ax.annotate('escapes',(-1.25,2.85),color='#2e8b57',fontsize=8.4)
ax.set_xlim(-4.1,3.9); ax.set_ylim(-2.9,3.3); ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 7.4
**Problem.** A satellite orbits the Earth at a height of $300\ \text{km}$. Taking
$g = 9.8\ \text{m s}^{-2}$ and $R = 6.4\times10^{6}\ \text{m}$, find its orbital
speed and period.

**Solution.** Orbital radius $r = R+h = 6.4\times10^{6} + 0.3\times10^{6}
= 6.7\times10^{6}\ \text{m}$, and $GM = gR^{2} = 9.8 \times 4.096\times10^{13}
= 4.01\times10^{14}\ \text{m}^{3}\text{s}^{-2}$.

$$ v_o = \sqrt{\frac{GM}{r}} = \sqrt{\frac{4.01\times10^{14}}{6.7\times10^{6}}}
= \sqrt{5.99\times10^{7}} = 7.74\times10^{3}\ \text{m s}^{-1} $$

$$ T = \frac{2\pi r}{v_o} = \frac{2\pi \times 6.7\times10^{6}}{7.74\times10^{3}}
= 5.44\times10^{3}\ \text{s} = 90.6\ \text{minutes} $$

A low-Earth-orbit satellite therefore circles the planet about 16 times a day.
:::

## 7.7 Escape velocity

::: definition Escape velocity
The escape velocity is the minimum speed with which a body must be projected from
the surface of a planet so that it escapes the planet's gravitational field and
never returns — that is, it just reaches infinity with zero speed.
:::

::: derivation Escape velocity $v_e = \sqrt{2gR}$
We start from conservation of energy between the planet's surface and infinity, and
reach the minimum launch speed needed to get away and never come back.

**Setting up.** A body of mass $m$ is fired straight up from the surface of a planet of
mass $M$ and radius $R$ with speed $v_e$. Take the gravitational potential energy to be
zero at infinity, as usual.

**Step 1 — energy at the surface.** The body has kinetic energy $\frac{1}{2}mv_e^{2}$
and potential energy $-GMm/R$ (using $U = -GMm/r$ with $r = R$). The total is

$$ E_{surface} = \tfrac{1}{2}mv_e^{2} - \frac{GMm}{R} $$

**Step 2 — energy at infinity.** "Just escapes" means it arrives at infinity with no
speed left over, so its kinetic energy there is zero. Its potential energy there is
also zero, by our choice of zero level. So:

$$ E_{\infty} = 0 + 0 = 0 $$

**Step 3 — apply conservation of energy.** Gravity is a conservative force and we
neglect air resistance, so the total energy does not change:

$$ \tfrac{1}{2}mv_e^{2} - \frac{GMm}{R} = 0 $$

**Step 4 — move the second term to the right:**

$$ \tfrac{1}{2}mv_e^{2} = \frac{GMm}{R} $$

**Step 5 — cancel $m$ from both sides.** It appears once on each side, so the answer
does not depend on the body's mass:

$$ \tfrac{1}{2}v_e^{2} = \frac{GM}{R} $$

**Step 6 — multiply both sides by 2:**

$$ v_e^{2} = \frac{2GM}{R} $$

**Step 7 — take the square root:**

$$ v_e = \sqrt{\frac{2GM}{R}} $$

**Step 8 — rewrite in terms of $g$.** At the surface $g = GM/R^{2}$, so $GM = gR^{2}$:

$$ v_e = \sqrt{\frac{2gR^{2}}{R}} $$

**Step 9 — cancel one $R$:**

$$ v_e = \sqrt{2gR} $$

**Step 10 — a third form, in terms of density.** The planet's mass is
$M = \frac{4}{3}\pi R^{3}\rho$. Putting this into Step 7:

$$ v_e = \sqrt{\frac{2G}{R}\cdot\frac{4}{3}\pi R^{3}\rho}
= R\sqrt{\frac{8}{3}\pi G\rho} $$

**Result.**

$$ v_e = \sqrt{\frac{2GM}{R}} = \sqrt{2gR} = R\sqrt{\frac{8}{3}\pi G\rho} $$

For the Earth, $v_e = \sqrt{2 \times 9.8 \times 6.4\times10^{6}} = 11.2$ km s⁻¹.

**What it means.** $m$ cancelled, so a pebble and a rocket need the same escape speed.
There is also no angle in the answer — energy depends only on distance, so the
*direction* of projection does not matter either. Escape speed depends only on the
planet: its mass (or density) and its radius.

**Conditions used.** Air resistance is neglected (a real rocket needs more), the body is
given all its speed at once at the surface (not continuously pushed), the planet does
not rotate, and there are no other bodies pulling on it.
:::

::: derivation Escape velocity is $\sqrt{2}$ times the orbital velocity
We start from the two results just obtained and reach the ratio between them.

**Step 1 — orbital speed for an orbit close to the surface.** Put $h = 0$, i.e.
$r = R$, into $v_o = \sqrt{GM/r}$:

$$ v_o = \sqrt{\frac{GM}{R}} = \sqrt{gR} $$

**Step 2 — write down the escape speed:**

$$ v_e = \sqrt{2gR} $$

**Step 3 — split the root.** Since $\sqrt{ab} = \sqrt{a}\sqrt{b}$:

$$ v_e = \sqrt{2}\cdot\sqrt{gR} $$

**Step 4 — recognise the second factor as $v_o$ from Step 1:**

$$ v_e = \sqrt{2}\,v_o $$

**Result.** $v_e = \sqrt{2}\,v_o \approx 1.41\,v_o$.

**What it means.** A satellite in low orbit is already travelling at 7.9 km s⁻¹; only
41 % more speed would let it leave the Earth altogether. In energy terms, escaping needs
exactly **twice** the kinetic energy of orbiting, because $v_e^{2} = 2v_o^{2}$.

**Condition used.** The orbit must be close to the surface ($h \ll R$), so that the same
$R$ appears in both formulas.
:::

For the Earth, $v_e = \sqrt{2 \times 9.8 \times 6.4\times10^{6}}
= \sqrt{1.254\times10^{8}} = 11.2\ \text{km s}^{-1}$.

| Body | $g$ (m s⁻²) | $R$ (km) | $v_e$ (km s⁻¹) |
|---|---|---|---|
| Moon | 1.62 | 1738 | 2.4 |
| Earth | 9.8 | 6400 | 11.2 |
| Mars | 3.7 | 3390 | 5.0 |
| Jupiter | 24.8 | 71 500 | 59.5 |
| Sun | 274 | 696 000 | 618 |

::: key Why the Moon has no atmosphere
The escape velocity of the Moon ($2.4\ \text{km s}^{-1}$) is comparable to the
root-mean-square speed of ordinary gas molecules at its daytime temperature, so
over geological time the gas molecules have all escaped. The Earth's
$11.2\ \text{km s}^{-1}$ is far above molecular speeds, so our atmosphere stays —
except for hydrogen and helium, the lightest and fastest, which do leak away.
:::

::: caution Escape velocity does not depend on the direction of projection
$v_e$ contains no angle, because the derivation uses only energy, and potential
energy depends only on $r$. Nor does it depend on the mass of the projectile.
It *does* depend on the mass and radius of the planet.
:::

## 7.8 Potential and kinetic energy of the satellite

For a satellite of mass $m$ in a circular orbit of radius $r$, the orbital
condition $GMm/r^{2} = mv_o^{2}/r$ gives $mv_o^{2} = GMm/r$, so

$$ K = \tfrac{1}{2}mv_o^{2} = +\frac{GMm}{2r}, \qquad
U = -\frac{GMm}{r}, \qquad
E = K + U = -\frac{GMm}{2r} $$

Three facts to remember:

- $U = -2K$, and $E = -K = U/2$. The total energy is **negative**, which is the
  signature of a **bound** orbit. If $E$ were zero or positive the satellite
  would escape.
- The **binding energy** — the extra energy needed to send the satellite from its
  orbit to infinity — is $|E| = GMm/2r$.
- A satellite in a *lower* orbit has a *more negative* total energy but a
  *higher* speed. Losing energy to atmospheric drag makes a satellite spiral down
  and **speed up**, which is why decaying satellites burn up.

```figure caption="Energies of a satellite against orbital radius, in units of $GMm/R$. $K$ is positive, $U$ negative, and the total $E = -K$ is always negative for a bound orbit."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7,2.9))
r = np.linspace(1,5,400)
ax.plot(r, 1/(2*r), color='#d9534f', lw=1.9, label='kinetic energy $K = GMm/2r$')
ax.plot(r, -1/r, color=ACCENT, lw=1.9, label='potential energy $U = -GMm/r$')
ax.plot(r, -1/(2*r), color='#2e8b57', lw=2.0, ls='--', label='total energy $E = -GMm/2r$')
ax.axhline(0, color=MUTED, lw=0.9)
ax.set_xlim(1,5); ax.set_ylim(-1.15,0.75)
ax.set_xticks([1,2,3,4,5]); ax.set_xticklabels(['$R$','$2R$','$3R$','$4R$','$5R$'])
ax.set_xlabel('orbital radius $r$'); ax.set_ylabel('energy')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
ax.legend(loc='lower right', fontsize=7.8)
```

::: example Worked example 7.5
**Problem.** A satellite of mass $200\ \text{kg}$ orbits the Earth at a height
equal to the Earth's radius. Find its orbital speed, kinetic energy, potential
energy, total energy and binding energy.
($g = 9.8\ \text{m s}^{-2}$, $R = 6.4\times10^{6}\ \text{m}$.)

**Solution.** Orbital radius $r = 2R = 1.28\times10^{7}\ \text{m}$ and
$GM = gR^{2} = 4.01\times10^{14}\ \text{m}^{3}\text{s}^{-2}$.

$$ v_o = \sqrt{\frac{GM}{r}} = \sqrt{\frac{4.01\times10^{14}}{1.28\times10^{7}}}
= \sqrt{3.14\times10^{7}} = 5.6\times10^{3}\ \text{m s}^{-1} $$

$$ K = \frac{GMm}{2r} = \frac{4.01\times10^{14}\times200}{2\times1.28\times10^{7}}
= 3.14\times10^{9}\ \text{J} $$

$$ U = -\frac{GMm}{r} = -6.27\times10^{9}\ \text{J},
\qquad E = K+U = -3.14\times10^{9}\ \text{J} $$

The binding energy is $|E| = 3.14\times10^{9}\ \text{J}$ — the energy that must be
supplied to free the satellite completely.
:::

## 7.9 Geostationary satellite

::: definition Geostationary satellite
A geostationary satellite is one that appears permanently fixed above one point
on the Earth's equator, because it revolves in the same sense as the Earth with a
period exactly equal to the Earth's period of rotation, $24\ \text{hours}$.
:::

Four conditions must all be met:

1. Its period must be $24\ \text{h}$ ($86400\ \text{s}$).
2. Its orbit must lie in the **equatorial plane**.
3. It must revolve **west to east**, the same sense as the Earth's spin.
4. The orbit must be **circular**, so that the angular speed is constant.

The height follows from the period. From $T^{2} = 4\pi^{2}r^{3}/GM$,

$$ r = \left(\frac{GMT^{2}}{4\pi^{2}}\right)^{1/3}
= \left(\frac{4.01\times10^{14}\times(86400)^{2}}{4\pi^{2}}\right)^{1/3}
= 4.23\times10^{7}\ \text{m} $$

so the height above the surface is

$$ h = r - R = 4.23\times10^{7} - 0.64\times10^{7} = 3.59\times10^{7}\ \text{m}
\approx 36\,000\ \text{km} $$

and the orbital speed is $v = 2\pi r/T = 3.08\ \text{km s}^{-1}$.

Geostationary satellites carry television broadcasts, telephone relays and
weather imaging. Three of them, $120^{\circ}$ apart, cover almost the whole globe
except the polar caps. Nepal's own communications satellite slot, at
$123.3^{\circ}\text{E}$, is a geostationary slot of exactly this kind; the
INSAT and FengYun weather images used by the Department of Hydrology and
Meteorology come from the same ring.

::: caution A geostationary satellite is not stationary
It moves at over $3\ \text{km s}^{-1}$. It only *appears* stationary because the
ground beneath it moves with the same angular velocity. Also, it cannot be placed
over Kathmandu — the centre of any orbit must be the centre of the Earth, so a
fixed-overhead satellite is only possible above the equator.
:::

## 7.10 GPS

The **Global Positioning System** is a constellation of at least 24 satellites in
six orbital planes at a height of about $20\,200\ \text{km}$, each with a period
of $11\ \text{h}\ 58\ \text{min}$ — half a sidereal day, so each satellite traces
the same ground track twice daily. From anywhere on Earth at least four are above
the horizon.

Each satellite continuously broadcasts its own position and the exact time of
transmission, kept by an atomic clock. The receiver measures the delay $\Delta t$
and computes the distance

$$ d = c\,\Delta t $$

where $c = 3\times10^{8}\ \text{m s}^{-1}$. One distance places the receiver on a
sphere around that satellite; two spheres intersect in a circle; three fix it to
two points, one of which is absurd (far out in space). This is
**trilateration**. A **fourth** satellite is needed because the receiver's own
cheap quartz clock has an unknown offset — four measurements solve for four
unknowns ($x$, $y$, $z$ and the clock error).

```figure caption="Trilateration. Each measured range puts the receiver on a sphere; three ranges intersect at the receiver R. A fourth satellite is needed to correct the receiver clock."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
R = np.array([4.0,1.0])
sats = [np.array([0.6,7.2]), np.array([7.4,6.6]), np.array([4.0,8.6])]
cols = [ACCENT,'#d9534f','#2e8b57']
labs = ['$S_1$','$S_2$','$S_3$']
# label anchors picked by hand so no text sits on an arc or a range line
soff = [(-7,7,'right'), (-7,8,'right'), (7,4,'left')]
dpos = [(3.00,4.48), (5.02,4.22), (4.55,5.60)]
t = np.linspace(0,2*np.pi,400)
for S,c,lab,off,dp in zip(sats,cols,labs,soff,dpos):
    d = np.hypot(*(R-S))
    ax.plot(S[0]+d*np.cos(t), S[1]+d*np.sin(t), color=c, lw=1.1, alpha=.75)
    ax.plot([S[0],R[0]],[S[1],R[1]], color=c, lw=0.9, ls='--', alpha=.9)
    ax.plot([S[0]],[S[1]],'^',color=c,ms=9,mec=INK,mew=0.6)
    ax.annotate(lab,S,textcoords='offset points',xytext=(off[0],off[1]),
                ha=off[2],color=c,fontsize=9.5)
    ax.annotate('$d$',dp,ha='center',va='center',color=c,fontsize=9)
ax.plot([R[0]],[R[1]],'o',color=INK,ms=7)
gy = -1.05
ax.annotate('R (receiver)', xy=(R[0],R[1]-0.16), xytext=(R[0],-0.30),
            ha='center', va='top', color=INK, fontsize=9.5,
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8, shrinkA=1, shrinkB=2))
ax.plot([-3.5,11.5],[gy,gy],color=MUTED,lw=1.2)
ax.annotate('ground',(-3.3,gy),textcoords='offset points',xytext=(0,-12),
            color=MUTED,fontsize=8.6)
ax.set_xlim(-4.2,12.2); ax.set_ylim(-2.0,9.6); ax.set_aspect('equal'); ax.axis('off')
```
Two corrections matter. Because the satellites move fast, special relativity
makes their clocks run slow by about $7\ \mu\text{s}$ per day; because they are
high in a weaker gravitational field, general relativity makes them run fast by
about $45\ \mu\text{s}$ per day. The net $38\ \mu\text{s}$ per day is corrected
in the satellite clocks — without it, positions would drift by about
$11\ \text{km}$ every day.

GPS is used in Nepal for land surveying and cadastral mapping, for tracking
aircraft and trekking routes, for monitoring the slow northward creep of the
Indian plate (about $2\ \text{cm}$ per year) that builds the Himalaya and causes
earthquakes, and it was used in the 2019–2020 survey in which Nepal and China
jointly re-measured the height of Sagarmatha as $8848.86\ \text{m}$.

## Chapter summary

- Newton's law: $F = Gm_1m_2/r^{2}$ with
  $G = 6.67\times10^{-11}\ \text{N m}^{2}\text{ kg}^{-2}$; forces are an
  action–reaction pair, independent of the medium.
- Field strength $E = GM/r^{2}$ (a vector, N kg⁻¹); at the surface $g = GM/R^{2}$,
  from which $M = gR^{2}/G$.
- Potential $V = -GM/r$ (a scalar, J kg⁻¹) and potential energy $U = -GMm/r$;
  $E = -dV/dr$, and $\Delta U \approx mgh$ near the surface.
- Altitude: $g_h = g(R/(R+h))^{2} \approx g(1-2h/R)$. Depth:
  $g_d = g(1-d/R)$, zero at the centre.
- Centre of mass $x_{cm} = \sum m_ix_i/\sum m_i$; it coincides with the centre of
  gravity only in a uniform field.
- Orbit: $v_o = \sqrt{GM/r}$, $T = 2\pi\sqrt{r^{3}/GM}$, hence
  $T^{2} \propto r^{3}$ (Kepler's third law).
- Escape velocity $v_e = \sqrt{2GM/R} = \sqrt{2gR} = \sqrt{2}\,v_o
  = 11.2\ \text{km s}^{-1}$ for the Earth; independent of mass and direction.
- Satellite energies: $K = GMm/2r$, $U = -GMm/r$, $E = -GMm/2r = -K$; binding
  energy $= GMm/2r$.
- Geostationary orbit: $T = 24\ \text{h}$, equatorial, west to east, circular,
  at $r = 4.23\times10^{7}\ \text{m}$, i.e. about $36\,000\ \text{km}$ up.
- GPS: 24+ satellites at $20\,200\ \text{km}$, period $11\ \text{h}\ 58\ \text{min}$;
  range $d = c\Delta t$; four satellites fix position and receiver clock error.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The dimensional formula of the universal gravitational constant $G$
   is <span class="marks">[1]</span>
   (a) $[ML^{2}T^{-2}]$ (b) $[M^{-1}L^{3}T^{-2}]$ (c) $[ML^{-3}T^{2}]$ (d) $[M^{-1}L^{2}T^{-1}]$
2. The value of $g$ at the centre of the Earth is <span class="marks">[1]</span>
   (a) maximum (b) equal to the surface value (c) zero (d) infinite
3. The gravitational potential at a distance $r$ from a mass $M$
   is <span class="marks">[1]</span>
   (a) $GM/r^{2}$ (b) $-GM/r$ (c) $-GM/r^{2}$ (d) $GMm/r$
4. The escape velocity from the Earth's surface does **not** depend
   on <span class="marks">[1]</span>
   (a) the mass of the Earth (b) the radius of the Earth (c) the mass of the body (d) the value of $g$
5. The total energy of a satellite in a circular orbit of radius $r$
   is <span class="marks">[1]</span>
   (a) $GMm/r$ (b) $-GMm/r$ (c) $-GMm/2r$ (d) $+GMm/2r$
6. A GPS receiver needs a minimum of how many satellites to fix its position and
   time? <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 6

::: note Answers to Group A
**1.** (b) — from $G = Fr^2/m_1m_2$, $[MLT^{-2}][L^2]/[M^2] = [M^{-1}L^3T^{-2}]$.
**2.** (c) — $g_d = g(1-d/R)$ gives zero at $d = R$; there is no mass below you.
**3.** (b) — potential is work per unit mass to bring the mass from infinity, and is negative.
**4.** (c) — $v_e = \sqrt{2gR}$ contains no term for the mass of the escaping body.
**5.** (c) — $K = GMm/2r$ and $U = -GMm/r$, so $E = -GMm/2r$.
**6.** (c) — three for the three spatial coordinates, a fourth for the receiver clock error.
:::

**Group B — Short answer (5 marks each)**

1. State Newton's law of gravitation. Define $G$ and give its SI unit and
   dimensional formula. <span class="marks">[5]</span>
2. Define gravitational potential and gravitational potential energy. Show that
   the gravitational potential at a distance $r$ from a mass $M$ is
   $V = -GM/r$. <span class="marks">[5]</span>
3. Derive an expression for the variation of $g$ with depth below the Earth's
   surface, and hence show that $g$ is zero at the centre. <span class="marks">[5]</span>
4. Distinguish between centre of mass and centre of gravity. Under what
   circumstances do they not coincide? <span class="marks">[5]</span>
5. Calculate the height and orbital speed of a geostationary satellite.
   ($g = 9.8\ \text{m s}^{-2}$, $R = 6.4\times10^{6}\ \text{m}$.) <span class="marks">[5]</span>
6. Two spheres, each of mass $100\ \text{kg}$, have their centres $1.0\ \text{m}$
   apart. Find the gravitational force between them and comment on its
   size. <span class="marks">[5]</span>

::: note Answers to Group B
**5.** $GM = gR^{2} = 4.01\times10^{14}$. With $T = 86400\ \text{s}$,
$r = \left(GMT^{2}/4\pi^{2}\right)^{1/3} = \left(7.59\times10^{22}\right)^{1/3}
= 4.23\times10^{7}\ \text{m}$. Height $h = r - R = 3.59\times10^{7}\ \text{m}
\approx 36\,000\ \text{km}$; speed $v = 2\pi r/T = 3.08\times10^{3}\ \text{m s}^{-1}$.

**6.** $F = \dfrac{Gm_1m_2}{r^{2}} = \dfrac{6.67\times10^{-11}\times100\times100}{1.0^{2}}
= 6.67\times10^{-7}\ \text{N}$ — about the weight of a grain of dust. Gravity is
negligible between everyday objects and matters only when one mass is
astronomically large.

**1., 2., 3., 4.** See §7.1, §7.3, the depth derivation in §7.4 and §7.5.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define escape velocity and derive the expression $v_e = \sqrt{2gR}$.
   <span class="marks">[4]</span>
   (b) Show that the escape velocity is $\sqrt{2}$ times the orbital velocity of
   a satellite close to the planet's surface. <span class="marks">[2]</span>
   (c) Calculate the escape velocity from the Moon, for which
   $g_m = 1.62\ \text{m s}^{-2}$ and $R_m = 1.74\times10^{6}\ \text{m}$, and use
   your answer to explain why the Moon has no atmosphere. <span class="marks">[2]</span>
2. (a) Derive expressions for the orbital velocity and the time period of a
   satellite revolving at a height $h$ above the Earth's surface, and hence
   obtain Kepler's third law. <span class="marks">[5]</span>
   (b) What is a geostationary satellite? State the conditions it must
   satisfy. <span class="marks">[3]</span>
3. (a) Obtain expressions for the kinetic energy, potential energy and total
   energy of a satellite in a circular orbit of radius $r$, and explain the
   significance of the negative sign of the total energy. <span class="marks">[5]</span>
   (b) A satellite of mass $500\ \text{kg}$ orbits at a height of
   $3.6\times10^{6}\ \text{m}$. Find its binding energy.
   ($g = 9.8\ \text{m s}^{-2}$, $R = 6.4\times10^{6}\ \text{m}$.) <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (c) $v_e = \sqrt{2g_mR_m} = \sqrt{2\times1.62\times1.74\times10^{6}}
= \sqrt{5.64\times10^{6}} = 2.37\times10^{3}\ \text{m s}^{-1} = 2.37\ \text{km s}^{-1}$.
This is of the same order as the speeds of gas molecules at lunar surface
temperatures, so over time all the gas has escaped.

**2.** See the derivation box in §7.6 and the four conditions listed in §7.9.

**3.** (b) $r = R+h = 6.4\times10^{6} + 3.6\times10^{6} = 1.0\times10^{7}\ \text{m}$,
$GM = gR^{2} = 4.01\times10^{14}$. Binding energy
$= \dfrac{GMm}{2r} = \dfrac{4.01\times10^{14}\times500}{2\times1.0\times10^{7}}
= 1.0\times10^{10}\ \text{J}$.
:::

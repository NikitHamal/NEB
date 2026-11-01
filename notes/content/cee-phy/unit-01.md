---
subject: Physics
grade: CEE
unit: 1
title: Physical Quantities, Vectors and Kinematics
hours: 2
area: Mechanics
---

This chapter is the toolkit of the whole Physics paper: units and dimensions,
significant figures and errors, vectors, and the description of straight-line and
projectile motion. The Mechanics area carries **10 of the 50 Physics questions**
(official MEC weightage); we estimate about **2** of them come from this chapter.
They are usually quick marks — a dimensional formula, a significant-figure count,
an angle between two vectors, a reading from a velocity–time graph, or a projectile
range — and the same skills are needed silently in every later chapter.

::: key What the paper asks from this chapter
- Dimensional formulae of common quantities, and which pairs share dimensions.
- Using dimensions: checking an equation, converting units, finding the dimensions of a constant.
- Counting significant figures; rounding a sum or product correctly; percentage error of $A^pB^q/C^r$.
- Resultant of two vectors, $R^2 = A^2 + B^2 + 2AB\cos\theta$, and its special cases (0°, 90°, 120°, 180°).
- Dot and cross products: angle between vectors, perpendicular and parallel tests, area of a parallelogram.
- Equations of motion, the distance in the $n$th second, and reading slopes and areas of motion graphs.
- Projectile formulas $T$, $H$, $R$; complementary angles; horizontal projection; what air resistance changes.
:::

## 1.1 Precision, accuracy, significant figures and dimensional analysis

### Units and base quantities

A **physical quantity** is anything that can be measured; it is written as a
number times a unit. The SI system has seven **base (fundamental) quantities**;
every other quantity is **derived** from them.

```photo id="phy11/vernier" caption="A vernier calliper. The jaws on the left grip the object; the sliding vernier scale beside the fixed main scale gives the fractional millimetre." width="80"
```


| Base quantity | SI unit | Symbol | Dimension |
|---|---|---|---|
| Length | metre | m | [L] |
| Mass | kilogram | kg | [M] |
| Time | second | s | [T] |
| Electric current | ampere | A | [A] (or [I]) |
| Thermodynamic temperature | kelvin | K | [K] (or [Θ]) |
| Amount of substance | mole | mol | [mol] (or [N]) |
| Luminous intensity | candela | cd | [cd] (or [J]) |

Plane angle (radian) and solid angle (steradian) are dimensionless.

### Accuracy, precision and errors

::: definition Accuracy and precision
**Accuracy** is how close a measured value is to the **true value**.
**Precision** is how close repeated measurements are to **one another** (and, for an
instrument, how fine its smallest reading — its least count — is).
:::

A set of readings can be precise but inaccurate (tightly grouped around the wrong
value — typical of a **systematic error** such as a zero error), or accurate on
average but imprecise (scattered around the true value — typical of **random
errors**).

| Error type | Cause | Reduced by |
|---|---|---|
| Systematic | zero error, faulty calibration, a fixed habit of the observer, ignored air drag | correcting the instrument or the method; *not* by repeating |
| Random | unpredictable small fluctuations | taking many readings and averaging |
| Gross (blunder) | misreading, wrong recording | care; rejecting the odd reading |

For readings $a_1, a_2, \dots, a_n$ with mean $\bar a$: the **absolute error** of a
reading is $|\bar a - a_i|$; the **mean absolute error** $\Delta a$ is the mean of
these; **relative error** $= \Delta a/\bar a$; **percentage error**
$= (\Delta a/\bar a)\times 100\,\%$.

```photo id="phy11/micrometer" caption="A micrometer screw gauge. The object is held between the anvil and the spindle; the thimble (circular scale) is turned until the ratchet clicks." width="70"
```


**Least count** (the smallest reading an instrument can make):
vernier calliper LC = 1 MSD − 1 VSD $=$ (value of 1 MSD)/(number of vernier
divisions), when $n$ VSD coincide with $(n-1)$ MSD; screw gauge LC $=$ pitch /
number of circular-scale divisions. A metre rule has LC 1 mm, a typical vernier
0.1 mm, a typical screw gauge 0.01 mm.

### Combining errors

| Result | Maximum error |
|---|---|
| $Z = A + B$ or $Z = A - B$ | $\Delta Z = \Delta A + \Delta B$ (absolute errors add) |
| $Z = AB$ or $Z = A/B$ | $\frac{\Delta Z}{Z} = \frac{\Delta A}{A} + \frac{\Delta B}{B}$ (relative errors add) |
| $Z = A^n$ | $\frac{\Delta Z}{Z} = n\frac{\Delta A}{A}$ |
| $Z = \frac{A^pB^q}{C^r}$ | $\%Z = p(\%A) + q(\%B) + r(\%C)$ |

::: caution Errors never subtract
Even when a quantity is *divided* or appears with a negative power, its
percentage error is **added**. In $Z = A^2/B^3$ the percentage error is
$2(\%A) + 3(\%B)$, not $2(\%A) - 3(\%B)$. And a subtraction $A - B$ of two nearly
equal numbers has a large *percentage* error even if each reading is good.
:::

::: example Worked example 1.1 — error in g from a pendulum
**Problem.** In $g = 4\pi^2 l/T^2$ the length $l$ is measured with an error of 2 %
and the period $T$ with an error of 1 %. Find the maximum percentage error in $g$.

**Solution.** $4\pi^2$ is exact. $\%g = 1\times(\%l) + 2\times(\%T) = 2 + 2(1) = 4\,\%$.
The power of $T$ doubles its share — measure $T$ (time many oscillations) most
carefully.
:::

### Significant figures

The **significant figures** (SF) of a measured value are the reliably known digits
plus the first uncertain one.

| Rule | Example | SF |
|---|---|---|
| All non-zero digits count | 4.256 | 4 |
| Zeros *between* non-zero digits count | 4.005 | 4 |
| *Leading* zeros never count (they only fix the decimal point) | 0.00420 | 3 |
| *Trailing* zeros after a decimal point count | 4.200 | 4 |
| Trailing zeros of a whole number without a decimal point are ambiguous | 4200 | 2, 3 or 4 |
| The power of ten does not count | 6.02 × 10²³ | 3 |

Write 4200 as 4.2 × 10³ (2 SF) or 4.200 × 10³ (4 SF) to remove the doubt.
**Changing units does not change the number of significant figures**:
2.30 m = 230 cm = 2.30 × 10⁻³ km — always 3 SF (230 cm is better written
2.30 × 10² cm).

**Arithmetic.**

- *Addition and subtraction:* keep as many **decimal places** as the number with the
  fewest decimal places. 12.1 + 0.25 + 1.256 = 13.606 → **13.6**.
- *Multiplication and division:* keep as many **significant figures** as the
  factor with the fewest SF. 2.5 × 1.25 = 3.125 → **3.1**.
- *Rounding:* drop a digit below 5 (2.743 → 2.74); raise the previous digit if the
  dropped digit is above 5 (2.746 → 2.75). When the dropped digit is exactly 5,
  the common convention keeps the previous digit if it is even and raises it if it
  is odd (2.745 → 2.74, 2.735 → 2.74).

### Dimensions and dimensional analysis

The **dimensions** of a quantity are the powers to which the base quantities must
be raised to represent it; the expression is its **dimensional formula**. Force
$= ma$ has $[M][LT^{-2}] = [MLT^{-2}]$.

| Quantity | From | Dimensional formula | SI unit |
|---|---|---|---|
| Force | $ma$ | $[MLT^{-2}]$ | N |
| Work, energy, torque | $Fs$, $rF$ | $[ML^2T^{-2}]$ | J, N m |
| Power | $W/t$ | $[ML^2T^{-3}]$ | W |
| Momentum, impulse | $mv$, $Ft$ | $[MLT^{-1}]$ | kg m s⁻¹, N s |
| Pressure, stress, elastic modulus, energy density | $F/A$ | $[ML^{-1}T^{-2}]$ | Pa |
| Surface tension, spring constant | $F/l$, $F/x$ | $[MT^{-2}]$ | N m⁻¹ |
| Coefficient of viscosity | $F/(A\,dv/dx)$ | $[ML^{-1}T^{-1}]$ | Pa s |
| Gravitational constant $G$ | $Fr^2/(m_1m_2)$ | $[M^{-1}L^3T^{-2}]$ | N m² kg⁻² |
| Planck's constant, angular momentum | $E/f$, $mvr$ | $[ML^2T^{-1}]$ | J s |
| Moment of inertia | $mr^2$ | $[ML^2]$ | kg m² |
| Frequency, angular velocity, velocity gradient | $1/T$, $\theta/t$ | $[T^{-1}]$ | Hz, rad s⁻¹ |
| Specific heat capacity | $Q/(m\Delta T)$ | $[L^2T^{-2}K^{-1}]$ | J kg⁻¹ K⁻¹ |
| Latent heat | $Q/m$ | $[L^2T^{-2}]$ | J kg⁻¹ |
| Stefan's constant $\sigma$ | $P/(AT^4)$ | $[MT^{-3}K^{-4}]$ | W m⁻² K⁻⁴ |
| Charge | $It$ | $[AT]$ | C |
| Potential difference | $W/q$ | $[ML^2T^{-3}A^{-1}]$ | V |
| Resistance | $V/I$ | $[ML^2T^{-3}A^{-2}]$ | Ω |
| Magnetic field $B$ | $F/(qv)$ | $[MT^{-2}A^{-1}]$ | T |

**Dimensionless quantities:** strain, angle, refractive index, relative density,
coefficient of friction, Poisson's ratio, Reynolds number. (Angle has a unit, the
radian, but no dimensions.)

::: definition Principle of homogeneity
Every term on both sides of a correct physical equation has the **same
dimensions**. Only quantities of the same dimensions can be added, subtracted or
equated, and the argument of $\sin$, $\cos$, $e^x$ or $\log$ must be dimensionless.
:::

**Uses.**

1. *Checking an equation:* $s = ut + \frac{1}{2}at^2$ — each term is $[L]$, so it is
   dimensionally correct (correctness of the $\frac{1}{2}$ is not tested).
2. *Dimensions of a constant:* in $v = at + \frac{b}{t+c}$, $c$ is added to $t$ so
   $c = [T]$; $b/t$ is a velocity, so $b = [LT^{-1}][T] = [L]$.
3. *Converting units:* a quantity with dimensions $[M^aL^bT^c]$ has numerical values
   related by $n_2 = n_1\left(\frac{M_1}{M_2}\right)^a\left(\frac{L_1}{L_2}\right)^b\left(\frac{T_1}{T_2}\right)^c$.
   For example 1 J $= 1\times(10^3\ \text{g/g})(10^2\ \text{cm/cm})^2 = 10^7$ erg.
4. *Deriving a relation* when a quantity is a product of powers of others.

::: example Worked example 1.2 — deriving a formula
**Problem.** The speed $v$ of a transverse wave on a string depends on the tension
$F$ and the mass per unit length $\mu$. Find the form of the relation.

**Solution.** Put $v = kF^x\mu^y$: $[LT^{-1}] = [MLT^{-2}]^x[ML^{-1}]^y$.
Matching powers: M: $0 = x + y$; L: $1 = x - y$; T: $-1 = -2x$. So $x = \frac{1}{2}$,
$y = -\frac{1}{2}$ and $v = k\sqrt{F/\mu}$ (experiment gives $k = 1$).
:::

**Limitations.** Dimensional analysis cannot find dimensionless constants ($\frac{1}{2}$,
$2\pi$); cannot handle relations containing sums of different terms, or
trigonometric, exponential and logarithmic functions; cannot, in mechanics, find a
relation with more than three unknown powers (only three equations, from M, L, T);
and cannot tell apart quantities with the same dimensions (work and torque).

::: tip Fast dimension work in the paper
Memorise five anchors — force $[MLT^{-2}]$, energy $[ML^2T^{-2}]$, pressure
$[ML^{-1}T^{-2}]$, charge $[AT]$, voltage $[ML^2T^{-3}A^{-1}]$ — and build the rest
by one division or multiplication. To compare options, check one base quantity at
a time (often the power of T alone eliminates three options).
:::

## 1.2 Scalars and vectors: laws of addition, resolution, scalar and vector products

A **scalar** has magnitude only (mass, time, work, energy, power, pressure,
temperature, charge, electric current, potential). A **vector** has magnitude and
direction **and obeys the laws of vector addition** (displacement, velocity,
acceleration, force, momentum, impulse, torque, electric field). Electric
current has a direction but adds algebraically at a junction, so it is a
**scalar**; finite rotations do not add like vectors either.

### Addition of vectors

- **Triangle law:** place $\vec B$ with its tail at the head of $\vec A$; the
  resultant runs from the tail of $\vec A$ to the head of $\vec B$.
- **Parallelogram law:** if $\vec A$ and $\vec B$ are the adjacent sides from one
  point, the diagonal from that point is $\vec R = \vec A + \vec B$.
- **Polygon law:** for many vectors joined head to tail, the closing side (tail of
  the first to head of the last) is the resultant. If they form a closed polygon,
  the resultant is zero.

For two vectors at angle $\theta$, the resultant's magnitude and its angle $\alpha$
with $\vec A$ are

$$ R = \sqrt{A^2 + B^2 + 2AB\cos\theta}, \qquad \tan\alpha = \frac{B\sin\theta}{A + B\cos\theta} $$

| Angle $\theta$ | Resultant $R$ |
|---|---|
| 0° (parallel) | $A + B$ (maximum) |
| 90° | $\sqrt{A^2+B^2}$ |
| 180° (antiparallel) | $|A - B|$ (minimum) |
| any $\theta$, with $A = B$ | $2A\cos(\theta/2)$ |
| 120°, with $A = B$ | $A$ |

So $|A - B| \le R \le A + B$: forces of 3 N and 5 N can give any resultant from
2 N to 8 N, but not 1 N or 9 N. **Subtraction** is adding the reverse vector:
$|\vec A - \vec B| = \sqrt{A^2 + B^2 - 2AB\cos\theta}$. Vector addition is
commutative and associative.

::: example Worked example 1.3 — resultant of two forces
**Problem.** Forces of 3 N and 4 N act at a point with 60° between them. Find the
resultant.

**Solution.** $R = \sqrt{9 + 16 + 2(3)(4)\cos 60^{\circ}} = \sqrt{37} = 6.1\ \text{N}$.
Check against the limits: it must lie between 1 N and 7 N, and above
5 N (the 90° value) because the angle is less than 90°.
:::

::: caution Zero resultant
Two vectors give zero only if they are equal and opposite. Three coplanar vectors
can give zero (they close a triangle) — e.g. 3 N, 4 N, 5 N — but 2 N, 3 N and 6 N
cannot, because 6 > 2 + 3. Three vectors that are not in one plane can never add
to zero; at least four are needed.
:::

### Resolution and unit vectors

A vector $\vec A$ at angle $\theta$ to the $x$-axis has rectangular components
$A_x = A\cos\theta$ and $A_y = A\sin\theta$, so $A = \sqrt{A_x^2 + A_y^2}$ and
$\tan\theta = A_y/A_x$. In three dimensions,
$\vec A = A_x\hat i + A_y\hat j + A_z\hat k$ and
$|\vec A| = \sqrt{A_x^2 + A_y^2 + A_z^2}$. The **unit vector** along $\vec A$ is
$\hat A = \vec A/|\vec A|$. The direction cosines satisfy
$\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1$. A component can be zero but never
larger than the vector itself.

### Scalar (dot) and vector (cross) products

| | Scalar product $\vec A\cdot\vec B$ | Vector product $\vec A\times\vec B$ |
|---|---|---|
| Definition | $AB\cos\theta$ (a scalar) | $AB\sin\theta\,\hat n$, $\hat n$ by the right-hand rule |
| In components | $A_xB_x + A_yB_y + A_zB_z$ | $(A_yB_z - A_zB_y)\hat i + (A_zB_x - A_xB_z)\hat j + (A_xB_y - A_yB_x)\hat k$ |
| Order | commutative: $\vec A\cdot\vec B = \vec B\cdot\vec A$ | anticommutative: $\vec A\times\vec B = -\vec B\times\vec A$ |
| Unit vectors | $\hat i\cdot\hat i = 1$, $\hat i\cdot\hat j = 0$ | $\hat i\times\hat j = \hat k$, $\hat j\times\hat k = \hat i$, $\hat k\times\hat i = \hat j$, $\hat i\times\hat i = 0$ |
| Zero when | $\theta = 90^{\circ}$ (perpendicular) | $\theta = 0^{\circ}$ or $180^{\circ}$ (parallel) |
| Physics | $W = \vec F\cdot\vec s$, $P = \vec F\cdot\vec v$, flux $= \vec B\cdot\vec A$ | $\vec\tau = \vec r\times\vec F$, $\vec L = \vec r\times\vec p$, $\vec F = q\vec v\times\vec B$ |
| Geometry | projection of $\vec A$ on $\vec B$ $= \vec A\cdot\vec B/B$ | area of parallelogram $= |\vec A\times\vec B|$; triangle $= \frac{1}{2}|\vec A\times\vec B|$ |

The angle between two vectors: $\cos\theta = \frac{\vec A\cdot\vec B}{AB}$.
$\vec A\times\vec B$ is perpendicular to both $\vec A$ and $\vec B$.

::: example Worked example 1.4 — angle between two vectors
**Problem.** Find the angle between $\vec A = \hat i + \hat j$ and $\vec B = \hat j + \hat k$.

**Solution.** $\vec A\cdot\vec B = (1)(0) + (1)(1) + (0)(1) = 1$ and
$A = B = \sqrt{2}$. So $\cos\theta = 1/2$ and $\theta = 60^{\circ}$.
:::

::: tip Three one-line tests
$|\vec A + \vec B| = |\vec A - \vec B|$ means $\vec A\perp\vec B$.
$\vec A\cdot\vec B = |\vec A\times\vec B|$ means $\theta = 45^{\circ}$.
$\vec A\cdot\vec B = 0$ means perpendicular; $\vec A\times\vec B = 0$ means parallel
(for components, $A_x/B_x = A_y/B_y = A_z/B_z$).
:::

## 1.3 Linear motion: equations of motion and their graphical treatment

**Distance** (path length, scalar) is never less than the magnitude of
**displacement** (vector, straight line from start to end). Average speed = total
distance / total time; average velocity = total displacement / total time.
Instantaneous velocity $v = dx/dt$; acceleration $a = dv/dt = d^2x/dt^2 = v\,dv/dx$.

### Equations of uniformly accelerated motion

For constant acceleration $a$, initial velocity $u$, final velocity $v$,
displacement $s$ in time $t$:

$$ v = u + at, \qquad s = ut + \frac{1}{2}at^2, \qquad v^2 = u^2 + 2as $$

$$ s = \frac{(u+v)}{2}\,t, \qquad s_n = u + \frac{a}{2}(2n - 1) $$

$s_n$ is the displacement **in the $n$th second** (its unit is metre; the "per
second" is hidden in the 1 s interval). They hold only if $a$ is constant.

| Fast fact (from rest, uniform $a$) | Ratio |
|---|---|
| Distances in successive equal intervals (1st, 2nd, 3rd second) | 1 : 3 : 5 : 7 (Galileo's odd numbers) |
| Total distances after 1, 2, 3 s | 1 : 4 : 9 ($s\propto t^2$) |
| Velocities after 1, 2, 3 s | 1 : 2 : 3 |
| Stopping distance for the same braking | $s \propto u^2$ — double the speed, four times the distance |

**Average speed for two halves.** Equal *distances* at $v_1$ and $v_2$:
$\bar v = \frac{2v_1v_2}{v_1+v_2}$ (harmonic mean). Equal *times*:
$\bar v = \frac{v_1+v_2}{2}$.

**Free fall** (air resistance neglected) is uniform acceleration $g$ downward.
Dropped from rest: $h = \frac{1}{2}gt^2$, $v = \sqrt{2gh}$. Thrown up at $u$: maximum
height $H = u^2/2g$, time up $= u/g$ = time down, total time $2u/g$, and it returns
with the same speed $u$. All bodies fall with the same $g$ in vacuum, whatever their
mass.

**Relative velocity on a line:** $v_{AB} = v_A - v_B$. Cars moving the same way at
60 and 40 km h⁻¹ close at 20 km h⁻¹; moving towards each other, at 100 km h⁻¹.

### Motion graphs

| Graph | Slope gives | Area under it gives |
|---|---|---|
| Position–time ($x$–$t$) | velocity | — |
| Velocity–time ($v$–$t$) | acceleration | displacement (area above axis +, below −); total area ignoring sign = distance |
| Acceleration–time ($a$–$t$) | rate of change of acceleration | change in velocity |

| Motion | $x$–$t$ graph | $v$–$t$ graph |
|---|---|---|
| At rest | horizontal line | on the time axis |
| Uniform velocity | straight sloping line | horizontal line |
| Uniform acceleration | parabola, curving upward | straight line, positive slope |
| Uniform retardation | parabola, curving downward | straight line, negative slope |
| Ball thrown up and caught (up positive) | inverted parabola | straight line of slope $-g$ crossing the axis at the top |

A $v$–$t$ graph can never be vertical (infinite acceleration) and an $x$–$t$ graph
can never turn back in time (a body cannot be at two places at once).

```figure caption="A velocity–time graph. Slopes are accelerations; the shaded areas are displacements — positive above the axis, negative below. Displacement = 16 + 48 + 16 − 4 = 76 m; distance = 84 m."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
t = [0,4,10,14,16]; v = [0,8,8,0,-4]
ax.fill_between([0,4,10,14], [0,8,8,0], color=ACCENT, alpha=0.16, lw=0)
ax.fill_between([14,16], [0,-4], color='#A8271F', alpha=0.20, lw=0)
ax.axhline(0, color=INK, lw=0.8)
ax.plot(t, v, color=ACCENT, lw=2.0, zorder=3)
ax.text(2.95, 1.6, '16 m', ha='center', fontsize=9, color=INK)
ax.text(7.0, 3.8, '48 m', ha='center', fontsize=9, color=INK)
ax.text(11.05, 1.6, '16 m', ha='center', fontsize=9, color=INK)
ax.annotate('−4 m', xy=(15.2,-1.0), xytext=(12.2,-3.6), fontsize=9, color='#A8271F',
            ha='center', va='center',
            arrowprops=dict(arrowstyle='-', color='#A8271F', lw=0.8))
ax.annotate('slope = +2 m s⁻²', xy=(2.2,4.4), xytext=(0.2,10.0), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.annotate('slope = −2 m s⁻²', xy=(12.6,2.8), xytext=(11.3,10.0), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8, mutation_scale=8))
ax.set_xlabel('time  t  (s)'); ax.set_ylabel('velocity  v  (m s⁻¹)')
ax.set_xlim(0,16.6); ax.set_ylim(-5.2,11.6)
ax.set_xticks([0,4,8,10,12,14,16])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

::: example Worked example 1.5 — the last-second trick
**Problem.** A stone dropped from rest covers 25 m in the last second of its fall
($g = 10\ \text{m s}^{-2}$). From what height was it dropped?

**Solution.** In the $n$th second, $s_n = \frac{g}{2}(2n-1) = 5(2n-1) = 25$, so
$n = 3$: the fall lasts 3 s. Height $h = \frac{1}{2} g t^2 = \frac{1}{2}(10)(9) = 45\ \text{m}$.
:::

::: caution Signs in vertical motion
Choose one direction as positive and keep it. With "up" positive, $a = -g$ on the
way up **and** on the way down; at the top $v = 0$ but $a = -g$ still. A body thrown
down from a height and one thrown up with the same speed reach the ground with the
**same speed** (energy), but at different times.
:::

## 1.4 Projectile motion, with and without a resistive force

A **projectile** is a body thrown into the air and then acted on by gravity alone
(no air resistance). Its motion is two independent motions: **uniform velocity**
horizontally ($a_x = 0$) and **free fall** vertically ($a_y = -g$).

For launch speed $u$ at angle $\theta$ above the horizontal on level ground:
$u_x = u\cos\theta$ (constant throughout), $u_y = u\sin\theta$.

| Quantity | Formula |
|---|---|
| Time of flight | $T = \frac{2u\sin\theta}{g}$ |
| Maximum height | $H = \frac{u^2\sin^2\theta}{2g}$ |
| Horizontal range | $R = \frac{u^2\sin2\theta}{g}$, maximum $R_{max} = \frac{u^2}{g}$ at $\theta = 45^{\circ}$ |
| Path (trajectory) | $y = x\tan\theta - \frac{gx^2}{2u^2\cos^2\theta} = x\tan\theta\left(1 - \frac{x}{R}\right)$ — a parabola |
| Velocity at time $t$ | $v_x = u\cos\theta$, $v_y = u\sin\theta - gt$, $v = \sqrt{v_x^2 + v_y^2}$ |
| At the highest point | $v = u\cos\theta$ (horizontal), $a = g$ downward, KE $= K\cos^2\theta$ |
| Range and height | $R = 4H\cot\theta$, so $\tan\theta = 4H/R$; at 45°, $H = R/4$ |
| Change in momentum, launch to landing | $2mu\sin\theta$, vertically downward |

**Complementary angles.** $\theta$ and $90^{\circ} - \theta$ give the **same range**
(15° and 75°, 30° and 60°), but different heights and times; for them
$H_1 + H_2 = u^2/2g$, $T_1T_2 = 2R/g$ and $R = 4\sqrt{H_1H_2}$.

```figure caption="Trajectories for the same launch speed (20 m s⁻¹, g = 10 m s⁻²). 15° and 75° land at the same point; 45° goes farthest."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.7))
u, g = 20.0, 10.0
for th, c in [(15, SERIES[1]), (45, ACCENT), (75, SERIES[2])]:
    r = np.radians(th); T = 2*u*np.sin(r)/g
    tt = np.linspace(0, T, 200)
    ax.plot(u*np.cos(r)*tt, u*np.sin(r)*tt - 0.5*g*tt**2, color=c, lw=1.9)
ax.text(10.0, 19.6, '75°:  H = 18.7 m', color=SERIES[2], fontsize=8.5, ha='left', va='bottom')
ax.text(21.5, 10.6, '45°:  H = 10 m', color=ACCENT, fontsize=8.5, ha='left', va='bottom')
ax.text(5.0, 2.4, '15°:  H = 1.3 m', color=SERIES[1], fontsize=8.5, ha='left', va='bottom')
ax.plot([20,40],[0,0],'o', color=INK, ms=4, zorder=5)
ax.annotate('R = 20 m\n(15° and 75°)', xy=(20,0), xytext=(24.5,4.2), fontsize=8.5, color=INK,
            ha='left', va='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('R = 40 m', xy=(40,0), xytext=(38.0,8.2), fontsize=8.5, color=INK,
            ha='center', va='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.set_xlim(0,42); ax.set_ylim(0,23.5)
ax.set_xlabel('horizontal distance  x  (m)'); ax.set_ylabel('height  y  (m)')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

::: example Worked example 1.6 — oblique projection
**Problem.** A ball is kicked at 20 m s⁻¹ at 30° above the horizontal
($g = 10\ \text{m s}^{-2}$). Find $T$, $H$ and $R$.

**Solution.** $u_y = 10\ \text{m s}^{-1}$, $u_x = 10\sqrt{3} = 17.3\ \text{m s}^{-1}$.
$T = 2u_y/g = 2\ \text{s}$; $H = u_y^2/2g = 100/20 = 5\ \text{m}$;
$R = u_xT = 34.6\ \text{m}$ (or $u^2\sin60^{\circ}/g = 20\sqrt{3}$).
:::

### Horizontal projection

A body thrown horizontally at speed $u$ from height $h$: $u_y = 0$, so the time to
fall $t = \sqrt{2h/g}$ is **the same as for a body simply dropped** from that height.
Horizontal distance $x = u\sqrt{2h/g}$; path $y = \frac{gx^2}{2u^2}$ (measured
downward); striking speed $v = \sqrt{u^2 + 2gh}$, at angle $\tan\phi = \sqrt{2gh}/u$
below the horizontal.

::: example Worked example 1.7 — relief drop
**Problem.** A helicopter flying horizontally at 50 m s⁻¹, 490 m above flat ground
near Jumla, releases a relief packet ($g = 9.8\ \text{m s}^{-2}$, no air
resistance). How far ahead of the release point does it land?

**Solution.** $t = \sqrt{2(490)/9.8} = \sqrt{100} = 10\ \text{s}$;
$x = 50\times10 = 500\ \text{m}$. The packet stays vertically below the helicopter
all the way down — both have the same horizontal velocity.
:::

### With a resistive force (air drag)

Real air exerts a drag force opposite to the velocity, roughly $F = kv$ at low
speeds and $F \propto v^2$ at high speeds. This changes the results above:

| Without air resistance | With air resistance |
|---|---|
| Horizontal velocity constant | Horizontal velocity keeps decreasing |
| Path a symmetric parabola | Path not a parabola; the descending branch is steeper than the rising one |
| Time up = time down | Time up **less than** time down (drag adds to $g$ on the way up and subtracts from it on the way down) |
| Lands with the launch speed | Lands with a smaller speed (energy lost to the air) |
| Maximum range at 45° | Range and height both reduced; maximum range at an angle **below 45°** |

```figure caption="A ball launched at 30 m s⁻¹ and 45°: the ideal parabola and the path with linear air drag. With drag the path is lower, shorter and lopsided — it comes down more steeply than it went up."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.7))
u, g, th = 30.0, 9.8, np.radians(45)
ux, uy = u*np.cos(th), u*np.sin(th)
T0 = 2*uy/g; t = np.linspace(0, T0, 300)
ax.plot(ux*t, uy*t - 0.5*g*t**2, color=MUTED, lw=1.7, ls='--', label='no air resistance (parabola)')
b = 0.12
t = np.linspace(0, 4.2, 3000)
x = ux/b*(1-np.exp(-b*t)); y = (uy + g/b)/b*(1-np.exp(-b*t)) - g*t/b
m = y >= 0
ax.plot(x[m], y[m], color='#A8271F', lw=2.0, label='with air resistance')
ax.text(83, 21.0, 'H = 23.0 m\nR = 91.8 m', fontsize=8.5, color=MUTED, ha='center', va='center')
ax.text(30, 13.5, 'H = 19.6 m\nR = 67.5 m', fontsize=8.5, color='#A8271F', ha='center', va='center')
ax.set_xlim(0,95); ax.set_ylim(0,29)
ax.set_xlabel('horizontal distance  x  (m)'); ax.set_ylabel('height  y  (m)')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
ax.legend(loc='upper left', fontsize=8, frameon=False)
```

**Terminal velocity.** A body falling through a fluid speeds up until the drag
(plus buoyancy) equals its weight; then the net force is zero and it falls at a
constant **terminal velocity**. For drag $kv$, $mg = kv_t$ gives $v_t = mg/k$, and
the velocity grows as $v = v_t(1 - e^{-kt/m})$, reaching about 63 % of $v_t$ after
one time constant $m/k$. Raindrops and parachutists fall at terminal velocity;
Stokes' law for a sphere in a viscous fluid (Chapter 4) is the same idea.

::: caution What does not change at the top
At the highest point the *vertical* velocity is zero, but the speed is
$u\cos\theta$, not zero, and the acceleration is still $g$ downward. Only a body
thrown straight up ($\theta = 90^{\circ}$) is momentarily at rest at the top.
:::


::: example Worked example — killing wrong options with dimensions
A formula is offered for the period of a pendulum in four forms: T = 2π√(l/g), T = 2π√(g/l), T = 2π√(ml/g), T = 2π(l/g). Which survive a dimension check?

- Dimensions: [l] = L, [g] = LT⁻², so l/g has dimensions T² and **√(l/g) has dimension T** ✓.
- √(g/l) has dimension T⁻¹ ✗ (that is a frequency).
- √(ml/g) contains M½T ✗ — a period cannot depend on mass this way.
- (l/g) alone has dimension T² ✗.

Only T = 2π√(l/g) can be correct — and you never needed the derivation. Note the limit of the method: it cannot verify dimensionless constants (the 2π) and cannot distinguish quantities with identical dimensions, like torque and energy.
:::

::: caution Trap — significant figures in multiplication
2.4 × 1.35 = 3.24 on a calculator, but the answer may carry only **two** significant figures (that of 2.4): **3.2**. The rule: multiplication/division follows the **fewest significant figures**; addition/subtraction follows the **fewest decimal places**. Examiners place 3.24 and 3.2 side by side precisely to catch this.
:::

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Least count | vernier: 1 MSD − 1 VSD; screw gauge: pitch / circular divisions |
| Errors | $Z = A\pm B$: $\Delta Z = \Delta A + \Delta B$; $Z = A^pB^q/C^r$: $\%Z = p\%A + q\%B + r\%C$ |
| SF in $+$ / $-$ | fewest decimal places |
| SF in $\times$ / $\div$ | fewest significant figures |
| Unit conversion | $n_2 = n_1(M_1/M_2)^a(L_1/L_2)^b(T_1/T_2)^c$ |
| Same dimensions | work = energy = torque $[ML^2T^{-2}]$; momentum = impulse $[MLT^{-1}]$; pressure = stress = modulus = energy density $[ML^{-1}T^{-2}]$; $h$ = angular momentum $[ML^2T^{-1}]$; surface tension = spring constant $[MT^{-2}]$ |
| Resultant | $R^2 = A^2 + B^2 + 2AB\cos\theta$; $\tan\alpha = B\sin\theta/(A + B\cos\theta)$; equal vectors: $R = 2A\cos(\theta/2)$ |
| Dot product | $AB\cos\theta = A_xB_x + A_yB_y + A_zB_z$; zero for perpendicular |
| Cross product | $AB\sin\theta$; zero for parallel; $\hat i\times\hat j = \hat k$; area of parallelogram $= |\vec A\times\vec B|$ |
| Equations of motion | $v = u + at$; $s = ut + \frac{1}{2}at^2$; $v^2 = u^2 + 2as$; $s_n = u + \frac{a}{2}(2n-1)$ |
| Free fall | $v = \sqrt{2gh}$; thrown up: $H = u^2/2g$, $T = 2u/g$ |
| Average speed, equal distances | $2v_1v_2/(v_1+v_2)$ |
| Projectile | $T = 2u\sin\theta/g$; $H = u^2\sin^2\theta/2g$; $R = u^2\sin2\theta/g$; $R_{max} = u^2/g$ |
| Projectile extras | $R = 4H\cot\theta$; $\theta$ and $90^{\circ} - \theta$ same $R$; KE at top $= K\cos^2\theta$ |
| Horizontal projection | $t = \sqrt{2h/g}$; $x = u\sqrt{2h/g}$; $v = \sqrt{u^2 + 2gh}$ |
| Linear drag | $v_t = mg/k$; with drag, time up < time down, range smaller, best angle < 45° |

## Chapter summary

- Accuracy is closeness to the true value; precision is closeness of repeated
  readings. Systematic errors spoil accuracy and are not removed by repeating.
- Leading zeros never count as significant; trailing zeros after a decimal point
  do. Sums keep the fewest decimal places, products the fewest significant figures.
- Percentage errors always add, each multiplied by its power:
  $\%(A^pB^q/C^r) = p\%A + q\%B + r\%C$.
- Every term in a correct equation has the same dimensions; dimensions convert units
  and derive power-law relations, but cannot give numerical constants or tell work
  from torque.
- $R^2 = A^2 + B^2 + 2AB\cos\theta$; $|A - B| \le R \le A + B$; two equal vectors at
  120° have a resultant equal to either.
- $\vec A\cdot\vec B = AB\cos\theta$ (zero when perpendicular),
  $|\vec A\times\vec B| = AB\sin\theta$ (zero when parallel, equals the parallelogram area).
- $v = u + at$, $s = ut + \frac{1}{2}at^2$, $v^2 = u^2 + 2as$, $s_n = u + \frac{a}{2}(2n-1)$;
  slope of $v$–$t$ = acceleration, area = displacement.
- Projectile: $T = 2u\sin\theta/g$, $H = u^2\sin^2\theta/2g$, $R = u^2\sin2\theta/g$;
  maximum range at 45°; complementary angles give equal ranges.
- Air resistance lowers and shortens the path, makes the fall slower than the rise,
  and moves the best angle below 45°; a falling body reaches terminal velocity when
  drag balances weight.

## Practice questions

**Set A — Recall (20 questions)**

1. The dimensional formula of Planck's constant is
   (a) [ML²T⁻²] (b) [ML²T⁻¹] (c) [MLT⁻¹] (d) [ML²T⁻³]
2. The number of significant figures in 0.003060 is
   (a) 2 (b) 3 (c) 4 (d) 7
3. Which pair of quantities has the same dimensions?
   (a) torque and work (b) work and power (c) force and momentum (d) stress and strain
4. A set of measurements is called precise when
   (a) its mean equals the true value (b) it is free of systematic error (c) it is made with a calibrated instrument (d) the repeated readings agree closely with one another
5. In a vernier calliper, 10 vernier divisions coincide with 9 main-scale divisions of 1 mm each. Its least count is
   (a) 0.01 mm (b) 0.1 mm (c) 0.9 mm (d) 1 mm
6. Which of the following is NOT a vector quantity?
   (a) impulse (b) torque (c) electric current (d) displacement
7. Two forces of 3 N and 4 N act on a body. Their resultant is greatest when the angle between them is
   (a) 0° (b) 45° (c) 90° (d) 180°
8. For the unit vectors along the coordinate axes, $\hat{j}\times\hat{i}$ equals
   (a) $\hat{k}$ (b) 1 (c) 0 (d) $-\hat{k}$
9. The scalar product of two non-zero vectors is zero when the angle between them is
   (a) 0° (b) 45° (c) 90° (d) 180°
10. The slope of a velocity–time graph gives
   (a) displacement (b) acceleration (c) distance (d) average speed
11. The area under an acceleration–time graph over an interval equals the
   (a) displacement (b) average acceleration (c) distance covered (d) change in velocity
12. A body starts from rest with uniform acceleration. The distances it covers in the 1st, 2nd and 3rd seconds are in the ratio
   (a) 1 : 3 : 5 (b) 1 : 2 : 3 (c) 1 : 4 : 9 (d) 1 : 2 : 4
13. At the highest point of its path, a body projected obliquely (no air resistance) has
   (a) zero velocity and zero acceleration (b) a horizontal velocity and acceleration g downward (c) zero velocity and acceleration g downward (d) a horizontal velocity and zero acceleration
14. For a fixed speed of projection and no air resistance, the horizontal range on level ground is greatest when the angle of projection is
   (a) 15° (b) 30° (c) 45° (d) 60°
15. Neglecting air resistance, the path of a body projected obliquely near the Earth's surface is a
   (a) parabola (b) circle (c) hyperbola (d) straight line
16. The dimensional formula of the universal gravitational constant G is
   (a) [ML²T⁻²] (b) [M⁻¹L²T⁻²] (c) [M⁻²L³T⁻²] (d) [M⁻¹L³T⁻²]
17. Which of the following is a dimensionless quantity?
   (a) stress (b) surface tension (c) strain (d) angular velocity
18. Dimensional analysis CANNOT be used to
   (a) find the value of a dimensionless constant in a formula (b) check the consistency of an equation (c) convert a quantity from one system of units to another (d) find how a quantity depends on others in a product-of-powers relation
19. A raindrop falling through air has reached its terminal velocity. Its acceleration is now
   (a) g, downward (b) zero (c) g/2, downward (d) g, upward
20. If $Z = A^{2}B$, the maximum percentage error in Z is
   (a) %A + %B (b) 2(%A) − %B (c) (%A)² + %B (d) 2(%A) + %B

::: note Answers and explanations — Set A
**1.** (b) — $E = hf$, so $h = E/f = [ML^2T^{-2}]/[T^{-1}] = [ML^2T^{-1}]$, the same as angular momentum. (a) is energy and (d) is power.
**2.** (c) — leading zeros do not count; the digits 3, 0, 6 and the final 0 (after the decimal point) do: 4 significant figures.
**3.** (a) — torque ($rF$) and work ($Fs$) are both [ML²T⁻²], though torque is a vector and work a scalar. Power has an extra T⁻¹; strain is dimensionless.
**4.** (d) — precision is the closeness of repeated readings to each other; closeness to the true value is accuracy.
**5.** (b) — 1 VSD = 9/10 mm = 0.9 mm, so LC = 1 MSD − 1 VSD = 1 − 0.9 = 0.1 mm.
**6.** (c) — current has a sense of flow but adds algebraically at a junction; it does not obey vector addition, so it is a scalar.
**7.** (a) — $R^2 = A^2 + B^2 + 2AB\cos\theta$ is greatest at $\cos\theta = 1$: R = 7 N. At 90° it is 5 N, at 180° only 1 N.
**8.** (d) — $\hat i\times\hat j = \hat k$ in cyclic order; reversing the order reverses the sign, so $\hat j\times\hat i = -\hat k$. A cross product is a vector, so 1 is impossible.
**9.** (c) — $\vec A\cdot\vec B = AB\cos\theta = 0$ only for $\theta = 90^{\circ}$. At 180° it is $-AB$, not zero.
**10.** (b) — $a = dv/dt$ is the slope; the area under a $v$–$t$ graph is the displacement.
**11.** (d) — $\int a\,dt = \Delta v$. Displacement is the area under the $v$–$t$ graph, not the $a$–$t$ graph.
**12.** (a) — $s_n = \frac{a}{2}(2n - 1)$ gives $\frac{a}{2}$, $\frac{3a}{2}$, $\frac{5a}{2}$: 1 : 3 : 5. The ratio 1 : 4 : 9 is for the *total* distances after 1, 2, 3 s.
**13.** (b) — only the vertical component vanishes at the top; $u\cos\theta$ remains, and gravity still gives g downward.
**14.** (c) — $R = u^2\sin2\theta/g$ is largest when $\sin 2\theta = 1$, i.e. $\theta = 45^{\circ}$.
**15.** (a) — uniform horizontal velocity plus uniform vertical acceleration gives $y = x\tan\theta - gx^2/(2u^2\cos^2\theta)$, a parabola.
**16.** (d) — $G = Fr^2/(m_1m_2) = [MLT^{-2}][L^2]/[M^2] = [M^{-1}L^3T^{-2}]$.
**17.** (c) — strain is change in length / original length, a ratio of two lengths. Stress is [ML⁻¹T⁻²], surface tension [MT⁻²], angular velocity [T⁻¹].
**18.** (a) — pure numbers such as $\frac{1}{2}$ or $2\pi$ have no dimensions, so they cannot be found; the other three are standard uses.
**19.** (b) — at terminal velocity the drag (with buoyancy) balances the weight, the net force is zero and the velocity is constant.
**20.** (d) — relative errors add, each multiplied by its power: $\%Z = 2(\%A) + 1(\%B)$. Errors never subtract.
:::

**Set B — Understanding (13 questions)**

1. Two vectors of equal magnitude P have a resultant that is also of magnitude P. The angle between them is
   (a) 60° (b) 90° (c) 120° (d) 180°
2. For two non-zero vectors, $|\vec{A}+\vec{B}| = |\vec{A}-\vec{B}|$. The angle between them is
   (a) 90° (b) 60° (c) 45° (d) 0°
3. A ball is thrown vertically upward and caught at the same height. Taking upward as positive and ignoring air resistance, its velocity–time graph is
   (a) a parabola opening downward (b) a horizontal line (c) a V-shaped pair of lines (d) a straight line of negative slope crossing the time axis
4. A ball is thrown vertically upward in air. Because of air resistance, the time it takes to fall back, compared with the time it takes to rise, is
   (a) shorter (b) longer (c) the same (d) shorter for a heavy ball and longer for a light one
5. Two stones are projected with the same speed at 30° and at 60° to the horizontal. The ratio of their maximum heights, $H_{30}:H_{60}$, is
   (a) 1 : 3 (b) 1 : 1 (c) 3 : 1 (d) 1 : √3
6. A car moving at speed v stops in a distance d under a constant braking force. Moving at 2v, under the same force, it stops in
   (a) √2 d (b) 2d (c) 4d (d) 8d
7. An athlete runs exactly one lap of a 400 m circular track in 80 s. His average speed and the magnitude of his average velocity are
   (a) 5 m s⁻¹ and 5 m s⁻¹ (b) 0 and 5 m s⁻¹ (c) 5 m s⁻¹ and 2.5 m s⁻¹ (d) 5 m s⁻¹ and 0
8. In the relation $v = at + \frac{b}{t+c}$, where v is a velocity and t a time, the dimensions of b are
   (a) [LT⁻¹] (b) [L] (c) [LT⁻²] (d) [T]
9. A rod exactly 10.00 cm long is measured five times with a vernier calliper that has a zero error: 10.21, 10.20, 10.22, 10.21 and 10.21 cm. These readings are
   (a) precise but not accurate (b) accurate but not precise (c) both accurate and precise (d) neither accurate nor precise
10. The momentum of a body of exactly known mass is measured with an error of 2 %. The percentage error in its kinetic energy is
   (a) 1 % (b) 2 % (c) 3 % (d) 4 %
11. A stone is projected at 60° to the horizontal with kinetic energy K. Neglecting air resistance, its kinetic energy at the highest point is
   (a) zero (b) K/4 (c) K/2 (d) 3K/4
12. The product 2.5 × 1.25, written to the correct number of significant figures, is
   (a) 3.125 (b) 3.13 (c) 3.1 (d) 3
13. When air resistance is taken into account, the angle of projection that gives the maximum horizontal range is
   (a) exactly 45° (b) greater than 45° (c) less than 45° (d) 90°

::: note Answers and explanations — Set B
**1.** (c) — for equal vectors $R = 2P\cos(\theta/2)$; $R = P$ needs $\cos(\theta/2) = \frac{1}{2}$, so $\theta/2 = 60^{\circ}$ and $\theta = 120^{\circ}$.
**2.** (a) — squaring both sides: $A^2 + B^2 + 2\vec A\cdot\vec B = A^2 + B^2 - 2\vec A\cdot\vec B$, so $\vec A\cdot\vec B = 0$: perpendicular.
**3.** (d) — $v = u - gt$ is linear in $t$ with slope $-g$; $v$ passes through zero at the top and becomes negative on the way down. The V shape (c) is the *speed*–time graph.
**4.** (b) — going up, drag and gravity both act downward (deceleration greater than g); coming down, drag opposes gravity (acceleration less than g). The ball comes back slower, so the fall takes longer — for every mass.
**5.** (a) — $H \propto \sin^2\theta$: $\sin^2 30^{\circ} : \sin^2 60^{\circ} = \frac{1}{4} : \frac{3}{4} = 1 : 3$. The *ranges* are equal (complementary angles) — that is the trap in (b).
**6.** (c) — $v^2 = 2ad$ with the same $a$, so $d \propto v^2$: doubling the speed gives four times the distance.
**7.** (d) — the distance is 400 m, so average speed = 400/80 = 5 m s⁻¹; he ends where he started, so displacement and average velocity are zero.
**8.** (b) — $c$ is added to $t$, so $c$ is a time; $b/t$ must be a velocity, so $b = [LT^{-1}][T] = [L]$.
**9.** (a) — the readings agree within 0.01 cm (precise), but their mean 10.21 cm is off the true 10.00 cm because of the zero error (not accurate).
**10.** (d) — $K = p^2/2m$; with $m$ exact, $\Delta K/K = 2\,\Delta p/p = 2\times2\,\% = 4\,\%$.
**11.** (b) — at the top only $u\cos60^{\circ} = u/2$ remains; KE $\propto v^2$, so KE $= K/4$.
**12.** (c) — in multiplication the answer keeps the fewest significant figures of the factors; 2.5 has two, so 3.125 → 3.1.
**13.** (c) — drag reduces the horizontal velocity throughout the flight, which penalises long, high flights; the best compromise is a flatter launch, below 45°.
:::

**Set C — Application (10 questions)**

1. A ball is thrown vertically upward at 19.6 m s⁻¹ (g = 9.8 m s⁻²). Its maximum height and total time of flight are
   (a) 9.8 m, 2 s (b) 19.6 m, 2 s (c) 39.2 m, 4 s (d) 19.6 m, 4 s
2. A body starting from rest with uniform acceleration covers 10 m in the third second of its motion. Its acceleration is
   (a) 2.2 m s⁻² (b) 4 m s⁻² (c) 5 m s⁻² (d) 6.7 m s⁻²
3. A stone is projected at 20 m s⁻¹ at 30° above the horizontal (g = 10 m s⁻²). Its horizontal range on level ground is
   (a) 34.6 m (b) 20.0 m (c) 40.0 m (d) 17.3 m
4. G is 6.67 × 10⁻¹¹ N m² kg⁻² in SI units. Its value in CGS units (dyn cm² g⁻²) is
   (a) 6.67 × 10⁻⁵ (b) 6.67 × 10⁻¹⁴ (c) 6.67 × 10⁻⁸ (d) 6.67 × 10⁻⁹
5. A bus covers the first half of the distance from Kathmandu to Dhulikhel at 40 km h⁻¹ and the second half at 60 km h⁻¹. Its average speed for the whole journey is
   (a) 50 km h⁻¹ (b) 48 km h⁻¹ (c) 45 km h⁻¹ (d) 52 km h⁻¹
6. A ball rolls off the edge of a horizontal table 1.25 m high at 3 m s⁻¹ (g = 10 m s⁻²). How far from the foot of the table does it land?
   (a) 0.75 m (b) 3.0 m (c) 1.25 m (d) 1.5 m
7. The adjacent sides of a parallelogram are $\vec{A} = \hat{i}+2\hat{j}$ and $\vec{B} = 2\hat{i}+\hat{j}$ (in metres). Its area is
   (a) 4 m² (b) 5 m² (c) 3 m² (d) 1.5 m²
8. The position of a particle moving along the x-axis is $x = 2t^{3} - 3t^{2} + 4$ (x in m, t in s). Its acceleration at t = 2 s is
   (a) 18 m s⁻² (b) 12 m s⁻² (c) 24 m s⁻² (d) 8 m s⁻²
9. The period T of a simple pendulum depends only on its length l and on g. Dimensional analysis gives T proportional to
   (a) $\sqrt{g/l}$ (b) $\sqrt{l/g}$ (c) $l/g$ (d) $\sqrt{lg}$
10. A ball projected at 20 m s⁻¹ lands 20 m away on level ground (g = 10 m s⁻²). The possible angles of projection are
   (a) 30° and 60° (b) 45° only (c) 20° and 70° (d) 15° and 75°

::: note Answers and explanations — Set C
**1.** (d) — $H = u^2/2g = (19.6)^2/19.6 = 19.6$ m; total time $2u/g = 2(19.6)/9.8 = 4$ s. (b) gives only the time to rise.
**2.** (b) — from rest, $s_3 = \frac{a}{2}(2\times3 - 1) = \frac{5a}{2} = 10$ m, so $a = 4$ m s⁻². (a) wrongly treats 10 m as the distance covered in 3 s.
**3.** (a) — $R = u^2\sin2\theta/g = 400\sin60^{\circ}/10 = 20\sqrt{3} = 34.6$ m. 40 m would need 45°.
**4.** (c) — $[M^{-1}L^3T^{-2}]$: $n_2 = 6.67\times10^{-11}\times(1000)^{-1}\times(100)^3 = 6.67\times10^{-8}$.
**5.** (b) — equal distances: $\bar v = 2v_1v_2/(v_1+v_2) = 2(40)(60)/100 = 48$ km h⁻¹. The 50 km h⁻¹ of (a) would be right only for equal *times*.
**6.** (d) — $t = \sqrt{2h/g} = \sqrt{2(1.25)/10} = 0.5$ s; $x = ut = 3\times0.5 = 1.5$ m.
**7.** (c) — $\vec A\times\vec B = (1\cdot1 - 2\cdot2)\hat k = -3\hat k$, so area $= 3$ m². 4 is $\vec A\cdot\vec B$, 5 is $AB$, 1.5 the triangle.
**8.** (a) — $v = 6t^2 - 6t$, $a = 12t - 6 = 18$ m s⁻² at $t = 2$ s. 12 m s⁻¹ is the velocity and 8 m the position at that instant.
**9.** (b) — $T = kl^xg^y$: $[T] = [L]^x[LT^{-2}]^y$ gives $x + y = 0$ and $-2y = 1$, so $y = -\frac{1}{2}$, $x = \frac{1}{2}$: $T \propto \sqrt{l/g}$.
**10.** (d) — $\sin2\theta = Rg/u^2 = 200/400 = 0.5$, so $2\theta = 30^{\circ}$ or $150^{\circ}$: $\theta = 15^{\circ}$ or $75^{\circ}$ (complementary, as expected).
:::

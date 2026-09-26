---
subject: Physics
grade: 11
unit: 1
title: Physical Quantities
hours: 3
area: Mechanics
---

Physics is an experimental science: every law in this book began as a number
read off an instrument. That number is never exact. This unit is about how much
of a measured number you are entitled to believe — the language of precision,
error and significant figures — and about the hidden structure that every
physical quantity carries with it, its **dimensions**. Dimensions let you check
an unfamiliar equation in ten seconds, convert a constant between unit systems,
and sometimes guess a formula you were never taught.

::: key What the examiner is testing
Group A nearly always carries one mark on significant figures or on the
dimensional formula of a named quantity. Group B regularly asks you to *check*
an equation dimensionally, to *derive* one, or to combine percentage errors.
These are the cheapest marks in the paper if the rules are automatic.
:::

## 1.1 Precision and significant figures

### Measurement, units and standards

A **physical quantity** is any property of matter or of a phenomenon that can be
measured. Measuring it means comparing it with a standard, so every measurement
is a numerical value multiplied by a unit:

$$ Q = n \times u $$

For a given quantity the product $nu$ is fixed, so a smaller unit always gives a
larger number. This one relation is the whole of unit conversion:

$$ n_1 u_1 = n_2 u_2 $$

Quantities that are independent of one another are called **fundamental** (base)
quantities; everything else is **derived** from them. The SI system takes seven
base quantities.

| Base quantity | SI unit | Symbol | Dimension |
|---|---|---|---|
| Length | metre | m | $[L]$ |
| Mass | kilogram | kg | $[M]$ |
| Time | second | s | $[T]$ |
| Electric current | ampere | A | $[I]$ |
| Thermodynamic temperature | kelvin | K | $[K]$ |
| Amount of substance | mole | mol | $[N]$ |
| Luminous intensity | candela | cd | $[J]$ |

Plane angle (radian) and solid angle (steradian) are **supplementary** units;
both are ratios of two lengths or two areas and are therefore dimensionless.

### Accuracy, precision and least count

::: definition Accuracy and precision
**Accuracy** is how close a measured value lies to the true or accepted value.
**Precision** is how close repeated measurements lie to one another, and how
finely the instrument can resolve a reading. A set of readings can be precise
without being accurate, and accurate on average without being precise.
:::

```figure caption="Accuracy is closeness to the true value (the bullseye); precision is closeness of the readings to each other. They are independent."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, axes = plt.subplots(2, 2, figsize=(4.4, 3.4))
tight = np.array([[0.10,0.16],[-0.14,0.05],[0.04,-0.15],[0.17,-0.04],[-0.06,-0.09]])
loose = np.array([[0.46,0.50],[-0.52,0.18],[0.10,-0.56],[0.58,-0.20],[-0.30,-0.34]])
panels = [(np.array([0.0,0.0]), tight, 'accurate and precise'),
          (np.array([0.50,0.34]), tight, 'precise, not accurate'),
          (np.array([0.0,0.0]), loose, 'accurate, not precise'),
          (np.array([0.40,0.28]), loose, 'neither')]
for ax, (ctr, off, title) in zip(axes.ravel(), panels):
    for r in (1.0, 0.66, 0.33):
        ax.add_patch(Circle((0, 0), r, fill=False, edgecolor=GRID, lw=1.0, zorder=1))
    ax.add_patch(Circle((0, 0), 0.09, facecolor=MUTED, edgecolor='none', zorder=2))
    p = ctr + off
    ax.plot(p[:, 0], p[:, 1], 'o', color=ACCENT, ms=4.2, zorder=3)
    ax.set_xlim(-1.18, 1.18); ax.set_ylim(-1.18, 1.18)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title, fontsize=7.8, color=INK, pad=3)
fig.tight_layout(pad=0.4)
```

Precision is capped by the **least count** of the instrument — the smallest
change it can display.

| Instrument | Least count |
|---|---|
| Metre rule | 1 mm = 0.1 cm |
| Vernier callipers (10 divisions) | 0.1 mm = 0.01 cm |
| Screw gauge (pitch 1 mm, 100 divisions) | 0.01 mm |
| Spherometer | 0.01 mm |
| Mechanical stop-watch | 0.1 s |
| Laboratory thermometer | 1 °C |

For a vernier scale, the least count is the difference between one main-scale
division (MSD) and one vernier-scale division (VSD):

$$ \text{L.C.} = 1\ \text{MSD} - 1\ \text{VSD} = \frac{\text{smallest main scale division}}{\text{number of vernier divisions}} $$

For a screw gauge, L.C. = pitch ÷ number of circular-scale divisions.

```figure caption="Vernier callipers. Ten vernier divisions span nine millimetres, so the least count is 0.1 mm. Here the vernier zero lies past 13 mm and its 4th division coincides, giving 13 + 4(0.1) = 13.4 mm."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.4))
ax.plot([0, 30], [0, 0], color=INK, lw=1.3)
for mm in range(31):
    h = 0.58 if mm % 10 == 0 else (0.42 if mm % 5 == 0 else 0.27)
    ax.plot([mm, mm], [0, h], color=INK, lw=0.9)
for cm in range(4):
    ax.annotate(str(cm), (10 * cm, 0.70), ha='center', fontsize=8.6, color=INK)
ax.annotate('main scale (cm)', (0.0, 1.50), fontsize=8.4, color=MUTED)
v0 = 13.4
ax.plot([v0 - 1.0, v0 + 10.0], [-0.14, -0.14], color=ACCENT, lw=1.3)
for k in range(11):
    x = v0 + 0.9 * k
    ax.plot([x, x], [-0.14, -0.66], color=ACCENT, lw=0.9)
    if k in (0, 4, 10):
        ax.annotate(str(k), (x, -1.02), ha='center', fontsize=8.2, color=ACCENT)
ax.annotate('vernier scale', (v0 - 1.0, -1.42), fontsize=8.4, color=ACCENT)
ax.plot([17, 17], [-0.66, 0.27], color='#d9534f', lw=1.6, zorder=4)
ax.annotate('4th division coincides', xy=(17.0, 0.34), xytext=(18.6, 1.50),
            ha='left', va='center', fontsize=8.2, color='#d9534f',
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0,
                            mutation_scale=9, shrinkB=0,
                            connectionstyle='angle,angleA=180,angleB=90,rad=0'))
ax.plot([v0, v0], [-0.14, 0.94], color='#2e8b57', lw=1.0, ls='--')
ax.annotate('zero of vernier', (v0, 1.06), ha='right', fontsize=8.2, color='#2e8b57')
ax.set_xlim(-1.5, 31.5); ax.set_ylim(-1.8, 1.9); ax.axis('off')
```
### Errors in measurement

| | Systematic error | Random error |
|---|---|---|
| Cause | faulty instrument, zero error, wrong technique, personal bias | unpredictable fluctuations: judgement, draughts, supply ripple |
| Sign | always in the same direction | equally likely either way |
| Effect | spoils **accuracy** | spoils **precision** |
| Remedy | calibrate, correct for zero error, change method | repeat and take the mean |

If a quantity is measured $n$ times giving $a_1, a_2, \dots, a_n$, the best
estimate is the arithmetic mean $\bar{a}$. Then

$$ \Delta a_i = |\bar{a} - a_i|, \qquad
\Delta a_{mean} = \frac{1}{n}\sum_{i=1}^{n} \Delta a_i $$

$$ \text{relative error} = \frac{\Delta a_{mean}}{\bar{a}}, \qquad
\text{percentage error} = \frac{\Delta a_{mean}}{\bar{a}} \times 100 $$

The result is quoted as $a = \bar{a} \pm \Delta a_{mean}$.

### Significant figures

::: definition Significant figures
The significant figures of a measured value are all the digits known with
certainty together with the first digit that is uncertain. They record the
precision of the measurement, not its size.
:::

| Rule | Example | Count |
|---|---|---|
| All non-zero digits count | 2345 | 4 |
| Zeros **between** non-zero digits count | 2.005 | 4 |
| **Leading** zeros never count | 0.0025 | 2 |
| **Trailing** zeros after a decimal point count | 2.500 | 4 |
| Trailing zeros in a whole number are ambiguous — use standard form | 4700 → $4.70\times10^{3}$ | 3 |
| Changing the unit never changes the count | 2.50 cm = 25.0 mm = 0.0250 m | 3 |
| Exact (counted) numbers and pure numbers such as $\pi$ | 12 eggs, $2\pi$ | infinite |

::: caution Zeros are the trap
Leading zeros are only place-holders: $0.0025$ has **two** significant figures,
not four. But the zero in $2.50$ was actually measured, so it counts. Never drop
a trailing zero from a result — $2.5$ cm and $2.50$ cm are different claims.
:::

**Rounding off.** If the digit to be dropped is greater than 5, raise the
preceding digit by one; if it is less than 5, leave the preceding digit
unchanged; if it is exactly 5 with nothing after it, round so that the preceding
digit becomes even ($4.25 \to 4.2$, $4.35 \to 4.4$).

**Arithmetic.** Two different rules, and mixing them up is the commonest error:

- **Addition and subtraction** — the answer keeps as many *decimal places* as
  the term with the fewest decimal places.
- **Multiplication and division** — the answer keeps as many *significant
  figures* as the factor with the fewest significant figures.

::: example Worked example 1.1
**Problem.** (a) A rectangular plate measures $4.234\ \text{cm}$ by
$1.005\ \text{cm}$. Find its area to the correct number of significant figures.
(b) Add $3.14\ \text{m}$, $2.7\ \text{m}$ and $0.586\ \text{m}$.

**Solution.**

(a) $A = 4.234 \times 1.005 = 4.25517\ \text{cm}^{2}$. The factors have 4 and 4
significant figures, so the answer keeps **4**:

$$ A = 4.255\ \text{cm}^{2} $$

(b) $3.14 + 2.7 + 0.586 = 6.426\ \text{m}$. The fewest decimal places is one (in
$2.7$), so the sum is rounded to one decimal place:

$$ \text{sum} = 6.4\ \text{m} $$

Notice that (b) is *not* rounded to two significant figures — the decimal-place
rule, not the significant-figure rule, governs addition.
:::

### Combining uncertainties

Let $\Delta A$ and $\Delta B$ be the absolute errors in $A$ and $B$. For the
**maximum possible** error in a result $Z$:

| Operation | Rule |
|---|---|
| $Z = A + B$ or $Z = A - B$ | $\Delta Z = \Delta A + \Delta B$ (absolute errors **add**) |
| $Z = AB$ or $Z = A/B$ | $\dfrac{\Delta Z}{Z} = \dfrac{\Delta A}{A} + \dfrac{\Delta B}{B}$ |
| $Z = A^{p}B^{q}/C^{r}$ | $\dfrac{\Delta Z}{Z} = p\dfrac{\Delta A}{A} + q\dfrac{\Delta B}{B} + r\dfrac{\Delta C}{C}$ |

::: derivation Where the error-combination rules come from
We start from only one idea — a measured value may be anywhere between
$A - \Delta A$ and $A + \Delta A$ — and we finish with every rule in the table
above. The trick each time is the same: push both measurements to the worst
possible end of their range.

**(a) Sum.** Let $Z = A + B$. The largest value $Z$ can take is reached when both
measurements are as large as they can be:

$$ Z_{\max} = (A + \Delta A) + (B + \Delta B) $$

Group the true parts together and the error parts together. This is just
rearranging the sum, so nothing has changed:

$$ Z_{\max} = (A + B) + (\Delta A + \Delta B) $$

But $A + B$ is the answer $Z$ itself, so whatever is left over is the error in $Z$:

$$ \Delta Z = \Delta A + \Delta B $$

**(b) Difference.** Let $Z = A - B$. Now $Z$ is largest when $A$ is at its top and
$B$ at its **bottom**, because we are subtracting $B$:

$$ Z_{\max} = (A + \Delta A) - (B - \Delta B) $$

Open the bracket. The two minus signs on $\Delta B$ make a plus:

$$ Z_{\max} = (A - B) + (\Delta A + \Delta B) $$

So again

$$ \Delta Z = \Delta A + \Delta B $$

Absolute errors **always add**, even for a subtraction. Errors never cancel,
because we do not know which way each one went.

**(c) Product.** Let $Z = AB$. Take both measurements at their top end:

$$ Z + \Delta Z = (A + \Delta A)(B + \Delta B) $$

Multiply out the two brackets, term by term:

$$ Z + \Delta Z = AB + A\,\Delta B + B\,\Delta A + \Delta A\,\Delta B $$

Now drop the last term. $\Delta A$ and $\Delta B$ are both small, so their
product is *very* small — for 1 % errors it is $0.01 \times 0.01 = 0.0001$ of the
answer, which no instrument could ever show:

$$ Z + \Delta Z \approx AB + A\,\Delta B + B\,\Delta A $$

Since $Z = AB$, subtract $AB$ from both sides:

$$ \Delta Z = A\,\Delta B + B\,\Delta A $$

Divide every term by $Z = AB$. Dividing both sides of an equation by the same
quantity is always allowed:

$$ \frac{\Delta Z}{AB} = \frac{A\,\Delta B}{AB} + \frac{B\,\Delta A}{AB} $$

Cancel $A$ in the first term on the right and $B$ in the second:

$$ \frac{\Delta Z}{Z} = \frac{\Delta A}{A} + \frac{\Delta B}{B} $$

**(d) Quotient.** Let $Z = A/B$. Here $Z$ is largest when the top is largest and
the bottom smallest:

$$ Z + \Delta Z = \frac{A + \Delta A}{B - \Delta B} $$

Pull $A$ out of the top and $B$ out of the bottom, so that only ratios are left
inside the brackets:

$$ Z + \Delta Z = \frac{A}{B}\cdot\frac{1 + \dfrac{\Delta A}{A}}{1 - \dfrac{\Delta B}{B}} $$

For any small number $x$, $\dfrac{1}{1-x} \approx 1 + x$ (try $x = 0.01$:
$1/0.99 = 1.0101$, and $1 + x = 1.01$). Use this on the denominator:

$$ Z + \Delta Z \approx \frac{A}{B}\left(1 + \frac{\Delta A}{A}\right)\left(1 + \frac{\Delta B}{B}\right) $$

Multiply the two brackets and again throw away the product of the two small
terms:

$$ Z + \Delta Z \approx \frac{A}{B}\left(1 + \frac{\Delta A}{A} + \frac{\Delta B}{B}\right) $$

Since $Z = A/B$, the bracket's "1" reproduces $Z$ and the rest is $\Delta Z$:

$$ \frac{\Delta Z}{Z} = \frac{\Delta A}{A} + \frac{\Delta B}{B} $$

The same rule as for a product — division does not help you.

**(e) Power.** Let $Z = A^{p}$. Take $A$ at its top end and pull out $A^{p}$:

$$ Z + \Delta Z = (A + \Delta A)^{p} = A^{p}\left(1 + \frac{\Delta A}{A}\right)^{p} $$

For small $x$, $(1+x)^{p} \approx 1 + px$ — this is the binomial expansion with
only the first two terms kept, and the rest are negligible because $x$ is small:

$$ Z + \Delta Z \approx A^{p}\left(1 + p\,\frac{\Delta A}{A}\right) $$

Since $Z = A^{p}$,

$$ \frac{\Delta Z}{Z} = p\,\frac{\Delta A}{A} $$

**Result.** For $Z = A^{p}B^{q}/C^{r}$ the three contributions simply add:

$$ \frac{\Delta Z}{Z} = p\,\frac{\Delta A}{A} + q\,\frac{\Delta B}{B} + r\,\frac{\Delta C}{C} $$

**What it means.** Absolute errors add for $+$ and $-$; *relative* errors add for
$\times$ and $\div$, each weighted by its power. So the measurement carrying the
biggest power deserves the most care.

**Condition used.** Every step after (b) assumed the errors are **small** compared
with the measurements ($\Delta A/A \ll 1$), so that products of two errors and
higher binomial terms can be dropped. The rules give the *maximum* error, not the
most likely one.
:::

::: tip The examiner is looking for
For "derive the expression for the maximum error in a product": (i) write
$Z + \Delta Z = (A+\Delta A)(B+\Delta B)$; (ii) expand fully; (iii) *say in words*
that $\Delta A\,\Delta B$ is neglected because it is second order; (iv) divide
through by $Z = AB$; (v) quote the final result with a box. Steps (iii) and (iv)
are where marks are most often lost.
:::

::: tip The power rule bites hardest
A power multiplies the percentage error by that power, and it does so even for a
quantity in the denominator. Measure the radius of a sphere to 1 % and the
volume is only good to 3 %. So in the laboratory, measure most carefully the
quantity that carries the highest power.
:::

::: example Worked example 1.2
**Problem.** The radius of a sphere is measured as $r = 7.20 \pm 0.05\ \text{cm}$.
Find its volume and the percentage error in the volume.

**Solution.** $V = \frac{4}{3}\pi r^{3} = \frac{4}{3}(3.1416)(7.20)^{3}$.

Since $(7.20)^{3} = 373.248\ \text{cm}^{3}$,

$$ V = 4.1888 \times 373.248 = 1563.5\ \text{cm}^{3} $$

Because $V \propto r^{3}$, the fractional errors combine as

$$ \frac{\Delta V}{V} = 3\,\frac{\Delta r}{r} = 3 \times \frac{0.05}{7.20} = 0.0208 $$

so the percentage error is **2.08 %**, and
$\Delta V = 0.0208 \times 1563.5 = 32.6\ \text{cm}^{3}$.

The uncertainty is in the tens, so the answer is quoted as

$$ V = (1.56 \pm 0.03) \times 10^{3}\ \text{cm}^{3} $$
:::

## 1.2 Dimensions and uses of dimensional analysis

::: definition Dimensions of a physical quantity
The dimensions of a physical quantity are the powers to which the base
quantities must be raised in order to represent it. The expression
$[M^{a}L^{b}T^{c}]$ is its **dimensional formula**, and an equation stating that
a quantity equals its dimensional formula is a **dimensional equation**.
:::

For example, force $=$ mass $\times$ acceleration, so

$$ [F] = [M][LT^{-2}] = [MLT^{-2}] $$

| Quantity | Defining relation | Dimensional formula | SI unit |
|---|---|---|---|
| Velocity | displacement/time | $[LT^{-1}]$ | m s⁻¹ |
| Acceleration | velocity/time | $[LT^{-2}]$ | m s⁻² |
| Force | mass × acceleration | $[MLT^{-2}]$ | N |
| Momentum, impulse | mass × velocity | $[MLT^{-1}]$ | kg m s⁻¹ |
| Work, energy, torque | force × distance | $[ML^{2}T^{-2}]$ | J |
| Power | work/time | $[ML^{2}T^{-3}]$ | W |
| Pressure, stress, modulus | force/area | $[ML^{-1}T^{-2}]$ | Pa |
| Density | mass/volume | $[ML^{-3}]$ | kg m⁻³ |
| Frequency | 1/period | $[T^{-1}]$ | Hz |
| Gravitational constant $G$ | $Fr^{2}/m_1m_2$ | $[M^{-1}L^{3}T^{-2}]$ | N m² kg⁻² |
| Surface tension | force/length | $[MT^{-2}]$ | N m⁻¹ |
| Coefficient of viscosity | $F/(A\,dv/dx)$ | $[ML^{-1}T^{-1}]$ | Pa s |
| Strain, angle, refractive index | ratio | $[M^{0}L^{0}T^{0}]$ | none |

::: key Principle of homogeneity of dimensions
Only quantities of the same dimensions may be added, subtracted or equated.
Therefore every term on both sides of a correct physical equation must have the
same dimensional formula.
:::

### Use 1 — checking an equation

Test $v^{2} = u^{2} + 2as$. Left side $[LT^{-1}]^{2} = [L^{2}T^{-2}]$. First term
on the right $[L^{2}T^{-2}]$; second term $[LT^{-2}][L] = [L^{2}T^{-2}]$. All
three agree, so the equation is dimensionally correct. Note that the pure number
2 is invisible to this test — dimensional analysis can prove an equation *wrong*
but never fully *right*.

::: example Worked example 1.3
**Problem.** Find the dimensional formula of (a) Planck's constant $h$, defined
by $E = h\nu$, and (b) the universal gas constant $R$, defined by $PV = nRT$.

**Solution.**

(a) $h = E/\nu$. Energy has $[ML^{2}T^{-2}]$ and frequency has $[T^{-1}]$, so

$$ [h] = \frac{[ML^{2}T^{-2}]}{[T^{-1}]} = [ML^{2}T^{-1}] $$

(This is the dimension of angular momentum — a useful check, since $h$ is indeed
measured in J s.)

(b) $R = PV/(nT)$. Pressure has $[ML^{-1}T^{-2}]$ and volume $[L^{3}]$, so
$PV = [ML^{2}T^{-2}]$. Dividing by amount of substance $[N]$ and temperature
$[K]$,

$$ [R] = [ML^{2}T^{-2}K^{-1}N^{-1}] $$

with SI unit J K⁻¹ mol⁻¹.
:::

### Use 2 — converting between systems of units

::: derivation The conversion formula for a quantity of dimensions $[M^{a}L^{b}T^{c}]$
We start from the fact that a physical quantity does not change when we change
the units we describe it in, and we reach a formula that converts its *number*
from one system to another.

Let the quantity be measured as $n_1$ units of size $u_1$ in the first system and
$n_2$ units of size $u_2$ in the second. The quantity itself is the same object,
so the two descriptions must be equal:

$$ n_1 u_1 = n_2 u_2 $$

Make $n_2$ the subject by dividing both sides by $u_2$:

$$ n_2 = n_1\,\frac{u_1}{u_2} $$

Now we need $u_1/u_2$. A unit of a quantity with dimensions $[M^{a}L^{b}T^{c}]$ is
built out of that system's own mass, length and time units:

$$ u_1 = M_1^{a}L_1^{b}T_1^{c}, \qquad u_2 = M_2^{a}L_2^{b}T_2^{c} $$

Divide one by the other and collect the same base quantity together, using
$x^{a}/y^{a} = (x/y)^{a}$:

$$ \frac{u_1}{u_2} = \frac{M_1^{a}L_1^{b}T_1^{c}}{M_2^{a}L_2^{b}T_2^{c}}
= \left(\frac{M_1}{M_2}\right)^{a}\left(\frac{L_1}{L_2}\right)^{b}\left(\frac{T_1}{T_2}\right)^{c} $$

Put this back into $n_2 = n_1(u_1/u_2)$:

$$ n_2 = n_1 \left(\frac{M_1}{M_2}\right)^{a}\left(\frac{L_1}{L_2}\right)^{b}\left(\frac{T_1}{T_2}\right)^{c} $$

**What it means.** Bigger units give smaller numbers. That is why the number of
ergs in a joule is huge ($10^{7}$): the erg is a tiny unit.

**Condition used.** The quantity must have a pure power-law dimensional formula in
M, L and T only. It fails for anything whose definition hides an extra base
quantity (temperature, current, amount of substance) unless you include that
base too.
:::

::: example Worked example 1.4
**Problem.** Convert 1 joule into erg (the CGS unit of energy).

**Solution.** Energy has $[ML^{2}T^{-2}]$, so $a = 1$, $b = 2$, $c = -2$. Going
from SI to CGS, $M_1/M_2 = 1\ \text{kg}/1\ \text{g} = 10^{3}$,
$L_1/L_2 = 1\ \text{m}/1\ \text{cm} = 10^{2}$, and $T_1/T_2 = 1$.

$$ n_2 = 1 \times (10^{3})^{1}(10^{2})^{2}(1)^{-2} = 10^{3} \times 10^{4} = 10^{7} $$

Hence $1\ \text{J} = 10^{7}\ \text{erg}$.
:::

### Use 3 — deriving a relation

If a quantity is known to depend on at most three others, assume a product of
powers and match dimensions on both sides.

::: example Worked example 1.5
**Problem.** The period $T$ of a simple pendulum may depend on its mass $m$,
length $l$ and the acceleration due to gravity $g$. Derive the relation.

**Solution.** Assume $T = k\,m^{a}l^{b}g^{c}$, where $k$ is a dimensionless
constant. Writing dimensions,

$$ [T] = [M]^{a}[L]^{b}[LT^{-2}]^{c} = [M^{a}L^{b+c}T^{-2c}] $$

Comparing powers of $M$, $L$ and $T$ on the two sides:

$$ a = 0, \qquad b + c = 0, \qquad -2c = 1 $$

So $c = -\tfrac{1}{2}$, $b = +\tfrac{1}{2}$ and $a = 0$. Therefore

$$ T = k\,l^{1/2}g^{-1/2} = k\sqrt{\frac{l}{g}} $$

The period does **not** depend on the mass of the bob — a real physical
prediction from pure bookkeeping. Experiment (or a full derivation) supplies
$k = 2\pi$.
:::

```figure caption="Testing the dimensional prediction $T \propto \sqrt{l}$ for a simple pendulum. The $T^2$ against $l$ graph is a straight line through the origin of slope $4\pi^2/g$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.6))
g = 9.8
L = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
T = 2 * np.pi * np.sqrt(L / g)
Ls = np.linspace(0, 1.05, 200)
axes[0].plot(Ls, 2 * np.pi * np.sqrt(Ls / g), color=MUTED, lw=1.2)
axes[0].plot(L, T, 'o', color=ACCENT, ms=5)
axes[0].set_xlabel('length  $l$  (m)'); axes[0].set_ylabel('period  $T$  (s)')
axes[0].set_title('$T$ against $l$', fontsize=9)
axes[1].plot(Ls, (2 * np.pi) ** 2 * Ls / g, color=MUTED, lw=1.2)
axes[1].plot(L, T ** 2, 'o', color=ACCENT, ms=5)
axes[1].set_xlabel('length  $l$  (m)'); axes[1].set_ylabel('$T^2$  (s$^2$)')
axes[1].set_title('$T^2$ against $l$', fontsize=9)
for ax in axes:
    ax.set_xlim(0, 1.05); ax.set_ylim(0, None)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(True, alpha=0.5)
fig.tight_layout(pad=0.5)
```

### Limitations of dimensional analysis

1. It cannot supply **dimensionless constants**. The $2\pi$ in
   $T = 2\pi\sqrt{l/g}$, and the $\tfrac{1}{2}$ in $\tfrac{1}{2}mv^{2}$, must
   come from theory or experiment.
2. It fails if the quantity depends on **more than three** base quantities,
   because M, L and T give only three equations.
3. It cannot handle equations that are a **sum of terms**, such as
   $s = ut + \tfrac{1}{2}at^{2}$ — it can only check them, not build them.
4. It cannot deal with **trigonometric, exponential or logarithmic** functions,
   though it does tell you their arguments must be dimensionless.
5. It cannot distinguish quantities with the same dimensions (work and torque,
   both $[ML^{2}T^{-2}]$), and cannot tell a scalar from a vector.

## Chapter summary

- A measurement is $Q = nu$, and $n_1u_1 = n_2u_2$; SI has seven base quantities.
- **Accuracy** = closeness to the true value; **precision** = closeness of
  repeated readings, limited by the least count.
- Vernier L.C. $= 1\ \text{MSD} - 1\ \text{VSD}$; screw-gauge L.C. = pitch ÷ number of circular divisions.
- Systematic errors spoil accuracy and are removed by calibration; random errors
  spoil precision and are reduced by averaging. Quote results as $\bar{a} \pm \Delta a_{mean}$.
- Significant figures = certain digits + first uncertain digit. Addition keeps
  the least **decimal places**; multiplication keeps the least **significant figures**.
- Errors combine as $\Delta Z = \Delta A + \Delta B$ for sums, and
  $\Delta Z/Z = p\,\Delta A/A + q\,\Delta B/B$ for products and powers.
- The **principle of homogeneity** says every term of a physical equation has the
  same dimensions. Dimensional analysis checks equations, converts units via
  $n_2 = n_1 (M_1/M_2)^{a}(L_1/L_2)^{b}(T_1/T_2)^{c}$, and derives simple relations.
- It cannot give dimensionless constants, handle more than three variables, build
  equations with several terms, or separate work from torque.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The number of significant figures in $0.00250\ \text{m}$ is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 5 (d) 6
2. Which pair has the same dimensional formula? <span class="marks">[1]</span>
   (a) work and power (b) force and momentum (c) work and torque (d) pressure and force
3. The dimensional formula of the universal gravitational constant is <span class="marks">[1]</span>
   (a) $[M^{-1}L^{3}T^{-2}]$ (b) $[ML^{3}T^{-2}]$ (c) $[M^{-1}L^{2}T^{-2}]$ (d) $[ML^{2}T^{-1}]$
4. The radius of a sphere is measured with an error of 2 %. The error in its volume is <span class="marks">[1]</span>
   (a) 2 % (b) 4 % (c) 6 % (d) 8 %
5. A vernier callipers has 10 vernier divisions matching 9 main-scale divisions of 1 mm each. Its least count is <span class="marks">[1]</span>
   (a) 1 mm (b) 0.5 mm (c) 0.1 mm (d) 0.01 mm
6. Which of the following is dimensionless? <span class="marks">[1]</span>
   (a) stress (b) strain (c) surface tension (d) force constant

::: note Answers to Group A
**1.** (b) — leading zeros are place-holders; the 2, 5 and the trailing 0 count.
**2.** (c) — both are force × distance, $[ML^{2}T^{-2}]$.
**3.** (a) — $G = Fr^{2}/m_1m_2 = [MLT^{-2}][L^{2}]/[M^{2}]$.
**4.** (c) — $V \propto r^{3}$, so the percentage error is tripled.
**5.** (c) — L.C. $= 1 - 0.9 = 0.1$ mm, i.e. 1 mm ÷ 10.
**6.** (b) — strain is a ratio of two lengths.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between accuracy and precision, giving one example of each. State
   what limits the precision of an instrument. <span class="marks">[5]</span>
2. State the rules for counting significant figures. Hence give the number of
   significant figures in (i) $0.00602$, (ii) $6.023\times10^{23}$, (iii) $4.700\ \text{m}$. <span class="marks">[5]</span>
3. The length, breadth and thickness of a metal block are $5.12\ \text{cm}$,
   $2.34\ \text{cm}$ and $1.05\ \text{cm}$. Calculate its volume to the correct
   number of significant figures. <span class="marks">[5]</span>
4. Check the correctness of the equation $T = 2\pi\sqrt{l/g}$ by the method of
   dimensions, and explain why the test cannot confirm the factor $2\pi$. <span class="marks">[5]</span>
5. A physical quantity is given by $P = a^{3}b^{2}/(\sqrt{c}\,d)$. If the
   percentage errors in $a$, $b$, $c$ and $d$ are 1 %, 2 %, 3 % and 4 %
   respectively, find the maximum percentage error in $P$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: accuracy = closeness to the true value (a zero-error instrument is
inaccurate); precision = closeness of repeated readings, set by the least count.

**2.** (i) 3 — leading zeros do not count. (ii) 4 — only the mantissa $6.023$ counts.
(iii) 4 — the trailing zeros follow a decimal point.

**3.** $V = 5.12 \times 2.34 \times 1.05 = 12.57984\ \text{cm}^{3}$. The fewest
significant figures among the factors is 3 (in $1.05$), so
$V = 12.6\ \text{cm}^{3}$.

**4.** LHS $= [T]$. RHS $= \sqrt{[L]/[LT^{-2}]} = \sqrt{[T^{2}]} = [T]$. The two
sides agree, so the equation is dimensionally correct. $2\pi$ is a pure number
with dimensions $[M^{0}L^{0}T^{0}]$, so replacing it by any other number leaves
the check unchanged — dimensional analysis cannot detect it.

**5.** $\dfrac{\Delta P}{P}\times100 = 3(1) + 2(2) + \tfrac{1}{2}(3) + 1(4)
= 3 + 4 + 1.5 + 4 = 12.5\ \%$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define absolute error, mean absolute error, relative error and percentage
   error. <span class="marks">[3]</span>
   (b) In an experiment the mass of a body is found to be
   $20.00 \pm 0.05\ \text{g}$ and its volume $5.00 \pm 0.02\ \text{cm}^{3}$.
   Calculate its density, the percentage error and the absolute error, and quote
   the result properly. <span class="marks">[5]</span>
2. (a) State the principle of homogeneity of dimensions and describe three uses
   of dimensional analysis. <span class="marks">[4]</span>
   (b) The value of the gravitational constant is
   $G = 6.67\times10^{-11}\ \text{N m}^{2}\ \text{kg}^{-2}$ in SI units. Convert
   it into the CGS system. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) See the definitions in §1.1.

**1.** (b) $\rho = m/V = 20.00/5.00 = 4.00\ \text{g cm}^{-3}$.

$$ \frac{\Delta\rho}{\rho} = \frac{0.05}{20.00} + \frac{0.02}{5.00} = 0.0025 + 0.0040 = 0.0065 $$

so the percentage error is $0.65\ \%$ and
$\Delta\rho = 0.0065 \times 4.00 = 0.026 \approx 0.03\ \text{g cm}^{-3}$.
The result is $\rho = 4.00 \pm 0.03\ \text{g cm}^{-3}$.

**2.** (a) Outline: state homogeneity, then the three uses — checking equations,
converting units, deriving relations.

**2.** (b) $[G] = [M^{-1}L^{3}T^{-2}]$, so $a = -1$, $b = 3$, $c = -2$ with
$M_1/M_2 = 10^{3}$, $L_1/L_2 = 10^{2}$, $T_1/T_2 = 1$:

$$ n_2 = 6.67\times10^{-11}\,(10^{3})^{-1}(10^{2})^{3} = 6.67\times10^{-11}\times10^{-3}\times10^{6} $$

giving $G = 6.67\times10^{-8}\ \text{dyne cm}^{2}\ \text{g}^{-2}$.
:::

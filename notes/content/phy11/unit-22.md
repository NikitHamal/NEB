---
subject: Physics
grade: 11
unit: 22
title: Capacitor
hours: 7
area: Electricity and Magnetism
---

A capacitor is the simplest device that stores electrical energy in a field
rather than in a chemical reaction. Two conductors, a thin insulating gap, and
you have something that can hold charge, smooth a power supply, time a circuit,
or deliver the huge pulse that fires a camera flash. This is the longest unit in
the electricity section, and it rewards careful work: the derivations are short,
the network problems are routine once you know the two combination rules, and
almost every NEB paper carries a capacitor numerical.

::: key Three formulas do most of the work
$C = Q/V$ defines capacitance, $C = \varepsilon_0 A/d$ describes the standard
parallel-plate capacitor, and $U = \frac{1}{2}CV^{2}$ gives the stored energy.
Everything else in this unit is an application of one of these three.
:::

## 22.1 Capacitance and capacitor

Give an isolated conductor a charge $Q$ and its potential rises to $V$.
Experiment shows the two are proportional, $Q \propto V$, so the ratio is a
constant of the conductor:

::: definition Capacitance
The capacitance of a conductor is the charge required to raise its potential by
one unit:
$$ C = \frac{Q}{V} $$
Its SI unit is the **farad** (F), where $1\ \text{F} = 1\ \text{C V}^{-1}$.
:::

The farad is enormous, so practical values are given in microfarad
($1\ \mu\text{F} = 10^{-6}\ \text{F}$), nanofarad ($10^{-9}\ \text{F}$) or
picofarad ($10^{-12}\ \text{F}$).

For an isolated sphere of radius $R$ we already know $V = kQ/R$, so

$$ C = \frac{Q}{V} = \frac{Q}{kQ/R} = 4\pi\varepsilon_0 R $$

Capacitance therefore depends only on **geometry and the surrounding medium**,
never on how much charge you happen to have put on. (As a scale check, the whole
Earth, $R = 6.4\times10^{6}\ \text{m}$, has $C = 6.4\times10^{6}/9\times10^{9}
= 711\ \mu\text{F}$ — smaller than a capacitor you can buy in Kathmandu for a
few rupees.)

::: definition Capacitor
A capacitor is an arrangement of two conductors separated by an insulator,
designed to store charge and electrical energy. The conductors carry equal and
opposite charges $+Q$ and $-Q$, and $Q$ means the magnitude on **one** plate.
:::

Bringing an earthed conductor close to a charged plate lowers its potential
without changing its charge, and so **raises** its capacitance. That is the
whole idea of a practical capacitor: two plates close together hold far more
charge per volt than either plate alone.

## 22.2 Parallel plate capacitor

Two flat metal plates of area $A$ a distance $d$ apart, with $d$ small compared
with the size of the plates, form the standard capacitor.

```figure caption="Parallel plate capacitor. The field between the plates is uniform, $E = \sigma/\varepsilon_0$, and the potential difference is $V = Ed$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.9))
d = 2.0
ax.plot([0, 0], [-1.05, 1.05], color='#d9534f', lw=4.0, solid_capstyle='butt')
ax.plot([d, d], [-1.05, 1.05], color=ACCENT, lw=4.0, solid_capstyle='butt')
for y in np.linspace(-0.85, 0.85, 7):
    ax.text(-0.17, y, '+', color='#d9534f', fontsize=9, ha='center', va='center')
    ax.text(d + 0.17, y, '-', color=ACCENT, fontsize=11, ha='center', va='center')
for y in np.linspace(-0.75, 0.75, 4):
    ax.annotate('', xy=(d - 0.09, y), xytext=(0.09, y),
                arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
ax.text(d/2, 0.0, r'$\vec{E}$', color='#2e8b57', fontsize=10, ha='center',
        va='center', bbox=dict(facecolor='white', edgecolor='none', pad=1.0))
ax.annotate('', xy=(d, -1.45), xytext=(0, -1.45),
            arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9,
                            shrinkA=0, shrinkB=0, mutation_scale=8))
ax.text(d/2, -1.40, '$d$', color=INK, fontsize=10, ha='center')
ax.text(0.0, 1.22, 'plate area $A$, charge $+Q$', color='#d9534f',
        fontsize=8.6, ha='left')
ax.text(d + 0.30, -1.25, 'charge $-Q$', color=ACCENT, fontsize=8.6, ha='right')
ax.set_xlim(-1.1, d + 1.1); ax.set_ylim(-1.85, 1.55)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Capacitance of a parallel plate capacitor, $C = \dfrac{\varepsilon_0 A}{d}$
We start from the field of a charged sheet and reach a formula for the
capacitance in terms of the plate area and the separation only.

**Setting up.** Two flat metal plates, each of area $A$, face each other a
distance $d$ apart with air (or vacuum) between them. One carries charge $+Q$,
the other $-Q$. The plates are large and $d$ is small, so we may treat the field
between them as uniform and ignore the bulging of the field at the edges.

**Step 1 — express the charge as a surface charge density.** Spreading $Q$
evenly over the area $A$ gives

$$ \sigma = \frac{Q}{A} $$

**Step 2 — write the field of one plate alone.** From Gauss's law, a thin sheet
with charge density $\sigma$ produces a field on each side of

$$ E_{one} = \frac{\sigma}{2\varepsilon_0} $$

**Step 3 — add the two fields in the region between the plates.** The positive
plate pushes a test charge away from itself, and the negative plate pulls it
towards itself. Between the plates both effects point the same way, from $+$ to
$-$, so the two fields add:

$$ E = \frac{\sigma}{2\varepsilon_0} + \frac{\sigma}{2\varepsilon_0} $$

(Outside the plates the same two fields point in opposite directions and cancel,
which is why a capacitor keeps its field neatly inside itself.)

**Step 4 — add the fractions.**

$$ E = \frac{\sigma}{\varepsilon_0} $$

**Step 5 — put back $\sigma = Q/A$ from Step 1.**

$$ E = \frac{Q}{\varepsilon_0 A} $$

**Step 6 — convert the field into a potential difference.** The field is
uniform, so the potential gradient $E = V/d$ from Unit 21 applies, and

$$ V = Ed $$

**Step 7 — substitute the field found in Step 5.**

$$ V = \frac{Qd}{\varepsilon_0 A} $$

**Step 8 — use the definition of capacitance, $C = Q/V$.**

$$ C = \frac{Q}{\dfrac{Qd}{\varepsilon_0 A}} $$

**Step 9 — dividing by a fraction is multiplying by its reciprocal.**

$$ C = Q \times \frac{\varepsilon_0 A}{Qd} $$

**Step 10 — cancel $Q$ from top and bottom.**

$$ C = \frac{\varepsilon_0 A}{d} $$

**Result.** The capacitance of a parallel plate air capacitor is
$C = \varepsilon_0 A/d$.

**What it means.** The charge $Q$ cancelled, so capacitance is a property of the
*shape and size* of the capacitor, not of how much charge you happen to put on
it. Bigger plates or a smaller gap store more charge per volt.

**Conditions used.** Uniform field (large plates, small separation, edge effects
ignored) and vacuum or air between the plates.
:::

So capacitance rises if you **increase the plate area** or **decrease the
separation**, and it does not depend on $Q$ or $V$. Filling the gap with an
insulating material of relative permittivity $\varepsilon_r$ multiplies it:

$$ C = \frac{\varepsilon_0\varepsilon_r A}{d} $$

::: derivation Capacitance with a dielectric slab of thickness $t$ in the gap
We start from the same two plates and reach the capacitance when a slab of
dielectric of thickness $t$ (with $t < d$) fills only part of the gap.

**Setting up.** The gap of width $d$ now contains a slab of thickness $t$ and
dielectric constant $\varepsilon_r$; the remaining thickness $d - t$ is still
air. Let $E_0 = \sigma/\varepsilon_0$ be the field in the air part, which is the
same as before because the charge on the plates is unchanged.

**Step 1 — write the field inside the slab.** The polarised molecules of the
dielectric set up their own opposing field, which weakens the original field by
the factor $\varepsilon_r$:

$$ E_{slab} = \frac{E_0}{\varepsilon_r} $$

**Step 2 — the total potential difference is the sum of the drops across the
two regions.** Potential drop equals field $\times$ distance in each uniform
region, so

$$ V = E_0(d - t) + E_{slab}\,t $$

**Step 3 — substitute the slab field from Step 1.**

$$ V = E_0(d - t) + \frac{E_0}{\varepsilon_r}t $$

**Step 4 — take $E_0$ out as a common factor.**

$$ V = E_0\left(d - t + \frac{t}{\varepsilon_r}\right) $$

**Step 5 — replace $E_0$ by $Q/\varepsilon_0 A$, using Step 5 of the previous
derivation.**

$$ V = \frac{Q}{\varepsilon_0 A}\left(d - t + \frac{t}{\varepsilon_r}\right) $$

**Step 6 — apply $C = Q/V$ and cancel $Q$.**

$$ C = \frac{\varepsilon_0 A}{d - t + \dfrac{t}{\varepsilon_r}} $$

**Result.** With a partly filling slab,

$$ C = \frac{\varepsilon_0 A}{d - t + \dfrac{t}{\varepsilon_r}} $$

**What it means.** The bracket in the denominator is smaller than $d$, because
$t/\varepsilon_r < t$. A smaller denominator means a larger $C$, so inserting a
dielectric always raises the capacitance. Two checks: putting $t = 0$ gives back
$\varepsilon_0 A/d$, and putting $t = d$ gives $\varepsilon_0\varepsilon_r A/d$,
exactly as expected.

**Conditions used.** The slab lies parallel to the plates and fills the whole
area $A$; the charge $Q$ on the plates is unchanged; edge effects ignored.
:::

::: tip The examiner is looking for
1. $\sigma = Q/A$ and the field of a single sheet, $\sigma/2\varepsilon_0$.
2. The reason the two fields **add** between the plates (and cancel outside).
3. $V = Ed$, with a statement that the field is uniform.
4. The definition $C = Q/V$ and the cancellation of $Q$ — this is the step that
   shows capacitance is independent of charge.
5. For the slab: the potential difference written as a **sum of two drops**,
   $V = E_0(d-t) + (E_0/\varepsilon_r)t$.
:::

::: example Worked example 22.1
**Problem.** A parallel plate capacitor has plates of area $100\ \text{cm}^{2}$
separated by $1\ \text{mm}$ of air. Find (a) its capacitance, (b) the charge
stored at $100\ \text{V}$, (c) the field between the plates, and (d) the new
capacitance if the gap is filled with mica of $\varepsilon_r = 6$.

**Solution.** $A = 100\ \text{cm}^{2} = 1.0\times10^{-2}\ \text{m}^{2}$ and
$d = 1.0\times10^{-3}\ \text{m}$.

(a) $C = \dfrac{\varepsilon_0 A}{d}
= \dfrac{8.85\times10^{-12}\times1.0\times10^{-2}}{1.0\times10^{-3}}
= 8.85\times10^{-11}\ \text{F} = 88.5\ \text{pF}$.

(b) $Q = CV = 8.85\times10^{-11}\times100 = 8.85\times10^{-9}\ \text{C} = 8.85\ \text{nC}$.

(c) $E = \dfrac{V}{d} = \dfrac{100}{1.0\times10^{-3}} = 1.0\times10^{5}\ \text{V m}^{-1}$.

(d) $C' = \varepsilon_r C = 6\times88.5 = 531\ \text{pF}$.
:::

## 22.3 Combination of capacitors

```figure caption="Capacitors in series carry the same charge $Q$ and share the applied p.d.; in parallel they have the same p.d. $V$ and share the charge."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.5))
G, PH = 0.085, 0.30          # half-gap and half-plate-length

def cap_h(ax, x, y, lab, above=True):
    ax.plot([x - G, x - G], [y - PH, y + PH], color=INK, lw=2.2)
    ax.plot([x + G, x + G], [y - PH, y + PH], color=ACCENT, lw=2.2)
    ax.text(x, y + PH + 0.12, lab, color=INK, fontsize=8.6, ha='center')

def cap_v(ax, x, y, lab):
    ax.plot([x - PH, x + PH], [y + G, y + G], color=INK, lw=2.2)
    ax.plot([x - PH, x + PH], [y - G, y - G], color=ACCENT, lw=2.2)
    ax.text(x - 0.11, y + G + 0.22, lab, color=INK, fontsize=8.6, ha='right')

def battery(ax, x, y, lab):
    ax.plot([x - 0.30, x + 0.30], [y + 0.09, y + 0.09], color=INK, lw=1.5)
    ax.plot([x - 0.15, x + 0.15], [y - 0.09, y - 0.09], color=INK, lw=3.0)
    ax.text(x - 0.42, y, lab, color=INK, fontsize=9, ha='right', va='center')

# ---------------- series ----------------
ax = axes[0]
W, H, yb = 3.1, 1.5, 0.75
xs = [0.75, 1.60, 2.45]
ax.plot([0, 0], [0, yb - 0.09], color=INK, lw=1.3)
ax.plot([0, 0], [yb + 0.09, H], color=INK, lw=1.3)
ax.plot([0, W], [0, 0], color=INK, lw=1.3)
ax.plot([W, W], [0, H], color=INK, lw=1.3)
edges = [0] + [v for x in xs for v in (x - G, x + G)] + [W]
for a, b in zip(edges[0::2], edges[1::2]):
    ax.plot([a, b], [H, H], color=INK, lw=1.3)
for x, lab in zip(xs, ['$C_1$', '$C_2$', '$C_3$']):
    cap_h(ax, x, H, lab)
battery(ax, 0, yb, '$V$')
ax.set_title('series', fontsize=9.5, color=INK)
ax.set_xlim(-1.0, W + 0.3); ax.set_ylim(-0.4, H + 0.8)
ax.set_aspect('equal'); ax.axis('off')

# ---------------- parallel ----------------
ax = axes[1]
W, H, yb = 3.0, 1.7, 0.85
xs = [0.85, 1.75, 2.65]
ax.plot([0, 0], [0, yb - 0.09], color=INK, lw=1.3)
ax.plot([0, 0], [yb + 0.09, H], color=INK, lw=1.3)
ax.plot([0, W], [0, 0], color=INK, lw=1.3)
ax.plot([0, W], [H, H], color=INK, lw=1.3)
for x, lab in zip(xs, ['$C_1$', '$C_2$', '$C_3$']):
    ax.plot([x, x], [0, H/2 - G], color=INK, lw=1.3)
    ax.plot([x, x], [H/2 + G, H], color=INK, lw=1.3)
    cap_v(ax, x, H/2, lab)
battery(ax, 0, yb, '$V$')
ax.set_title('parallel', fontsize=9.5, color=INK)
ax.set_xlim(-1.0, W + 0.3); ax.set_ylim(-0.4, H + 0.8)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Equivalent capacitance in series, $\dfrac{1}{C_{eq}} = \sum\dfrac{1}{C_i}$
We start from the two facts that fix a series chain — same charge, shared
voltage — and reach the rule for the single capacitor that could replace them.

**Setting up.** Three capacitors $C_1$, $C_2$, $C_3$ are joined end to end
across a supply of potential difference $V$. Let the p.d. across them be $V_1$,
$V_2$ and $V_3$.

**Step 1 — state why the charge is the same on all three.** The battery puts
$+Q$ on the first plate. Charge cannot jump across the insulating gap, so the
facing plate gains $-Q$ by induction, its partner on the next capacitor gains
$+Q$, and so on down the chain. Hence every capacitor carries the same charge:

$$ Q_1 = Q_2 = Q_3 = Q $$

**Step 2 — state why the voltages add.** Going from one end of the chain to the
other, the total drop in potential is the sum of the individual drops:

$$ V = V_1 + V_2 + V_3 $$

**Step 3 — write each voltage using $C = Q/V$, rearranged as $V = Q/C$.**

$$ V_1 = \frac{Q}{C_1},\qquad V_2 = \frac{Q}{C_2},\qquad V_3 = \frac{Q}{C_3} $$

**Step 4 — substitute these into Step 2.**

$$ V = \frac{Q}{C_1} + \frac{Q}{C_2} + \frac{Q}{C_3} $$

**Step 5 — write the same total voltage for the single equivalent capacitor.**
By definition $C_{eq}$ is the one capacitor that would take the same charge $Q$
at the same total voltage $V$:

$$ V = \frac{Q}{C_{eq}} $$

**Step 6 — set the two expressions for $V$ equal.**

$$ \frac{Q}{C_{eq}} = \frac{Q}{C_1} + \frac{Q}{C_2} + \frac{Q}{C_3} $$

**Step 7 — divide every term by $Q$.** The charge is the same everywhere
(Step 1), so this one division clears it from the whole equation:

$$ \frac{1}{C_{eq}} = \frac{1}{C_1} + \frac{1}{C_2} + \frac{1}{C_3} $$

**Result.** For capacitors in series the *reciprocals* add:
$1/C_{eq} = 1/C_1 + 1/C_2 + 1/C_3$.

**What it means.** Adding another capacitor in series adds another positive term
to the right-hand side, so $1/C_{eq}$ grows and $C_{eq}$ shrinks. A series
combination is therefore always smaller than the smallest capacitor in it — use
it when you need the chain to withstand a high voltage, not to store more charge.

**Conditions used.** Step 1 needs the capacitors to be genuinely in series, with
nothing else connected to the junctions between them, so that no charge can leak
away sideways.
:::

::: derivation Equivalent capacitance in parallel, $C_{eq} = \sum C_i$
We start from the two facts that fix a parallel group — same voltage, shared
charge — and reach the rule for the single replacement capacitor.

**Setting up.** Three capacitors $C_1$, $C_2$, $C_3$ have all their left plates
joined to one terminal and all their right plates joined to the other. Let them
carry charges $Q_1$, $Q_2$, $Q_3$.

**Step 1 — state why the voltage is the same across all three.** Each capacitor
has its two plates connected directly to the two terminals of the supply, so
each one feels the full supply voltage:

$$ V_1 = V_2 = V_3 = V $$

**Step 2 — state why the charges add.** The total charge the supply pushes out
is shared among the three capacitors:

$$ Q = Q_1 + Q_2 + Q_3 $$

**Step 3 — write each charge using $C = Q/V$, rearranged as $Q = CV$.**

$$ Q_1 = C_1V,\qquad Q_2 = C_2V,\qquad Q_3 = C_3V $$

**Step 4 — substitute these into Step 2.**

$$ Q = C_1V + C_2V + C_3V $$

**Step 5 — write the same total charge for the single equivalent capacitor.**

$$ Q = C_{eq}V $$

**Step 6 — set the two expressions for $Q$ equal.**

$$ C_{eq}V = C_1V + C_2V + C_3V $$

**Step 7 — divide every term by $V$.** The voltage is the same everywhere
(Step 1), so it cancels right through:

$$ C_{eq} = C_1 + C_2 + C_3 $$

**Result.** For capacitors in parallel the capacitances simply add,
$C_{eq} = C_1 + C_2 + C_3$.

**What it means.** Connecting capacitors in parallel is the same as building one
capacitor with a bigger plate area, and $C = \varepsilon_0 A/d$ says bigger area
means bigger capacitance. The total is always larger than the largest member.

**Conditions used.** All the capacitors must share the same pair of nodes, and
each must be able to withstand the full supply voltage.
:::

::: tip The examiner is looking for
1. A clear statement, **with a reason**, of what is common: same $Q$ in series
   (induction, charge cannot cross the gap), same $V$ in parallel (both plates
   on the terminals).
2. The matching sum: $V = V_1+V_2+V_3$ in series, $Q = Q_1+Q_2+Q_3$ in parallel.
3. Substituting $V = Q/C$ or $Q = CV$ for each capacitor.
4. The definition of $C_{eq}$ as the single capacitor that behaves the same way.
5. The final division by $Q$ (series) or $V$ (parallel).
:::

| | Series | Parallel |
|---|---|---|
| Same for all | charge $Q$ | potential difference $V$ |
| Shared | potential difference | charge |
| Rule | $1/C_{eq} = \sum 1/C_i$ | $C_{eq} = \sum C_i$ |
| Result | **less** than the smallest | **more** than the largest |
| Used to | withstand a higher voltage | obtain a larger capacitance |

::: caution Series and parallel are opposite to resistors
For resistors the *series* rule is the simple sum; for capacitors it is the
*parallel* rule. Students who learn DC circuits first regularly swap them. Check
your answer: a series combination must always come out smaller than the smallest
capacitor in it.
:::

::: example Worked example 22.2
**Problem.** A $6\ \mu\text{F}$ capacitor is joined in series with a parallel
pair of $3\ \mu\text{F}$ capacitors, and the combination is connected across
$60\ \text{V}$. Find the equivalent capacitance, the charge on each capacitor
and the p.d. across each.

**Solution.** The parallel pair first:
$C_p = 3 + 3 = 6\ \mu\text{F}$.

In series with the $6\ \mu\text{F}$:

$$ \frac{1}{C_{eq}} = \frac{1}{6} + \frac{1}{6} = \frac{1}{3}
\Longrightarrow C_{eq} = 3\ \mu\text{F} $$

Total charge: $Q = C_{eq}V = 3\times10^{-6}\times60 = 180\ \mu\text{C}$.

This whole charge sits on the series $6\ \mu\text{F}$, so its p.d. is
$V_1 = 180/6 = 30\ \text{V}$. The remaining $60 - 30 = 30\ \text{V}$ appears
across the parallel pair, and each $3\ \mu\text{F}$ there carries

$$ Q = CV = 3\times10^{-6}\times30 = 90\ \mu\text{C} $$

As a check, $90 + 90 = 180\ \mu\text{C}$, matching the series charge.
:::

## 22.4 Energy of charged capacitor

Charging a capacitor is not free: each extra bit of charge must be pushed onto a
plate that is already charged and repelling it.

::: derivation Energy stored in a charged capacitor, $U = \frac{1}{2}CV^{2}$
We start from the work needed to move one more small piece of charge onto a
partly charged capacitor, and we reach the total energy stored.

**Setting up.** The capacitor starts completely uncharged. The battery moves
charge from one plate to the other a little at a time until the final charge is
$Q$ and the final p.d. is $V$.

**Step 1 — write the p.d. at a moment when the charge so far is $q$.** From the
definition $C = q/v$:

$$ v = \frac{q}{C} $$

Notice that $v$ **grows** as $q$ grows. Each extra bit of charge is harder to
push on than the one before, so we cannot just write "work = $QV$".

**Step 2 — write the work needed for one extra small charge $dq$.** Work equals
charge moved times the p.d. it is moved through, and $dq$ is small enough that
$v$ does not change during it:

$$ dW = v\,dq $$

**Step 3 — substitute $v$ from Step 1.**

$$ dW = \frac{q}{C}\,dq $$

**Step 4 — add up all these small amounts of work, from empty to full.** The
charge on the plates runs from $0$ to $Q$:

$$ W = \int_{0}^{Q}\frac{q}{C}\,dq $$

**Step 5 — take the constant $C$ outside the integral.** The capacitance does
not change while the capacitor charges:

$$ W = \frac{1}{C}\int_{0}^{Q} q\,dq $$

**Step 6 — integrate $q$.**

$$ W = \frac{1}{C}\left[\frac{q^{2}}{2}\right]_{0}^{Q} $$

**Step 7 — substitute the limits, upper minus lower.**

$$ W = \frac{1}{C}\left(\frac{Q^{2}}{2} - \frac{0^{2}}{2}\right) $$

**Step 8 — the second term is zero.**

$$ W = \frac{Q^{2}}{2C} $$

**Step 9 — this work is not lost; it is stored in the field between the
plates.** So the energy stored is

$$ U = \frac{Q^{2}}{2C} $$

**Step 10 — get the second form.** Replace one of the two $Q$ factors using
$Q = CV$:

$$ U = \frac{Q \times Q}{2C} = \frac{Q \times CV}{2C} $$

**Step 11 — cancel $C$.**

$$ U = \frac{1}{2}QV $$

**Step 12 — get the third form.** Replace $Q$ by $CV$ once more:

$$ U = \frac{1}{2}(CV)V = \frac{1}{2}CV^{2} $$

**Result.** The energy stored in a charged capacitor is

$$ U = \frac{Q^{2}}{2C} = \frac{1}{2}QV = \frac{1}{2}CV^{2} $$

**What it means.** The three forms are the same energy; pick the one whose two
quantities you already know. The factor $\frac{1}{2}$ appears because the
average p.d. during charging is only half the final value — the first charge is
moved across almost no p.d., the last across the full $V$.

**Conditions used.** The capacitance $C$ is constant during charging (no
dielectric is moved, no plate separation changed), and none of the energy
counted here includes the heat lost in the connecting wires and the battery.
:::

The factor $\frac{1}{2}$ is not arbitrary. On a graph of $Q$ against $V$ the
energy is the **area under the line**, and the line is straight through the
origin, so the area is a triangle.

```figure caption="Charge against potential difference for a capacitor. The gradient is $C$ and the shaded area $\frac{1}{2}QV$ is the stored energy."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.7))
V = np.linspace(0, 5, 100)
Q = 0.8*V
ax.plot(V, Q, color=ACCENT, lw=2.1)
ax.fill_between(V, 0, Q, color=ACCENT, alpha=0.12)
ax.hlines(0.8*5, 0, 5, color=MUTED, lw=0.9, ls=':')
ax.vlines(5, 0, 0.8*5, color=MUTED, lw=0.9, ls=':')
ax.annotate('slope $= C$', (3.0, 2.4), textcoords='offset points',
            xytext=(-56, 20), color='#d9534f', fontsize=9.2,
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.1,
                            mutation_scale=10))
ax.text(3.1, 0.85, r'area $=\frac{1}{2}QV$', color=INK, fontsize=9.5, ha='center')
ax.set_xlabel('potential difference  $V$')
ax.set_ylabel('charge  $Q$')
ax.set_xticks([0, 5]); ax.set_xticklabels(['$0$', '$V$'])
ax.set_yticks([4.0]); ax.set_yticklabels(['$Q$'])
ax.set_xlim(0, 5.9); ax.set_ylim(0, 4.9)
ax.spines[['top', 'right']].set_visible(False)
```

### Energy density

Where is the energy? In the **field**. For a parallel plate capacitor, put
$C = \varepsilon_0A/d$ and $V = Ed$ into $U = \frac{1}{2}CV^{2}$:

$$ U = \frac{1}{2}\cdot\frac{\varepsilon_0 A}{d}\cdot(Ed)^{2}
= \frac{1}{2}\varepsilon_0E^{2}(Ad) $$

Since $Ad$ is the volume between the plates, the energy stored per unit volume is

$$ u = \frac{1}{2}\varepsilon_0E^{2} $$

This turns out to be true of *any* electrostatic field, not just this one.

### Energy lost in sharing charge

Connect a capacitor $C_1$ at $V_1$ to a capacitor $C_2$ at $V_2$. Charge is
conserved, so the common final potential is

$$ V = \frac{C_1V_1 + C_2V_2}{C_1 + C_2} $$

Comparing the energy before and after gives a loss of

$$ \Delta U = \frac{C_1C_2(V_1 - V_2)^{2}}{2(C_1 + C_2)} $$

which is always positive. The "missing" energy is dissipated as heat in the
connecting wires and as a small amount of electromagnetic radiation — it is
never recovered.

::: example Worked example 22.3
**Problem.** A $10\ \mu\text{F}$ capacitor is charged to $200\ \text{V}$ and then
disconnected from the supply and joined to an uncharged $10\ \mu\text{F}$
capacitor. Find the common potential difference, the energy before and after,
and the energy lost.

**Solution.** Initial charge: $Q = 10\times10^{-6}\times200 = 2.0\times10^{-3}\ \text{C}$.

Common p.d.:
$$ V = \frac{Q}{C_1 + C_2} = \frac{2.0\times10^{-3}}{20\times10^{-6}} = 100\ \text{V} $$

Energy before: $U_i = \tfrac{1}{2}(10\times10^{-6})(200)^{2} = 0.20\ \text{J}$.

Energy after: $U_f = \tfrac{1}{2}(20\times10^{-6})(100)^{2} = 0.10\ \text{J}$.

Loss $= 0.10\ \text{J}$, i.e. **half** the original energy. The formula agrees:

$$ \Delta U = \frac{(10\times10^{-6})(10\times10^{-6})(200)^{2}}{2(20\times10^{-6})}
= \frac{1.0\times10^{-10}\times4\times10^{4}}{4.0\times10^{-5}} = 0.10\ \text{J} $$
:::

## 22.5 Effect of a dielectric: Polarization and displacement

A **dielectric** is an insulator placed between the plates. It has no free
electrons, but its molecules respond to the field.

- **Non-polar** molecules (H₂, O₂, CO₂) have no permanent dipole. The field pulls
  the electron cloud one way and the nucleus the other, **inducing** a dipole.
- **Polar** molecules (H₂O, HCl) already possess a dipole moment. The field
  simply turns them so that they line up with it, against the randomising effect
  of thermal motion.

Either way the slab acquires a net dipole moment per unit volume. This is called
the **polarization** $\vec{P}$. Inside the bulk, neighbouring dipoles cancel, but
on the two faces uncancelled **bound charges** appear — negative on the face
towards the positive plate and positive on the other. Their surface density
equals the polarization, $\sigma_p = P$.

```figure caption="A dielectric slab polarized between charged plates. The bound surface charges set up a field $E_p$ opposing $E_0$, so the net field falls to $E_0/\varepsilon_r$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.9))
d = 3.0
ax.plot([0, 0], [-1.0, 1.0], color='#d9534f', lw=4.0, solid_capstyle='butt')
ax.plot([d, d], [-1.0, 1.0], color=ACCENT, lw=4.0, solid_capstyle='butt')
for y in np.linspace(-0.8, 0.8, 5):
    ax.text(-0.16, y, '+', color='#d9534f', fontsize=9, ha='center', va='center')
    ax.text(d + 0.16, y, '-', color=ACCENT, fontsize=11, ha='center', va='center')
ax.add_patch(plt.Rectangle((0.75, -0.95), 1.5, 1.9, facecolor='#eef2f7',
                           edgecolor=MUTED, lw=0.9, zorder=1))
for y in (-0.55, 0.0, 0.55):
    for x in (1.28, 1.76):
        ax.annotate('', xy=(x + 0.075, y), xytext=(x - 0.075, y),
                    arrowprops=dict(arrowstyle='-', color=MUTED, lw=1.0,
                                    shrinkA=0, shrinkB=0), zorder=2)
        ax.text(x - 0.16, y, '-', color=ACCENT, fontsize=8.5, ha='center',
                va='center', zorder=3)
        ax.text(x + 0.175, y, '+', color='#d9534f', fontsize=7, ha='center',
                va='center', zorder=3)
for y in np.linspace(-0.72, 0.72, 4):
    ax.text(0.90, y, '-', color=ACCENT, fontsize=11, ha='center', va='center', zorder=4)
    ax.text(2.10, y, '+', color='#d9534f', fontsize=9, ha='center', va='center', zorder=4)
ax.annotate('', xy=(0.60, 1.30), xytext=(0.12, 1.30),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.5,
                            shrinkA=0, shrinkB=0, mutation_scale=11))
ax.text(0.36, 1.40, '$E_0$', color='#2e8b57', fontsize=9.5, ha='center')
ax.annotate('', xy=(1.15, 1.30), xytext=(1.85, 1.30),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.5,
                            shrinkA=0, shrinkB=0, mutation_scale=11))
ax.text(1.50, 1.40, '$E_p$', color='#d9534f', fontsize=9.5, ha='center')
ax.text(1.5, -1.35, 'dielectric, $\\varepsilon_r$', color=INK, fontsize=8.8, ha='center')
ax.set_xlim(-0.6, d + 0.6); ax.set_ylim(-1.75, 1.85)
ax.set_aspect('equal'); ax.axis('off')
```

The bound charges produce their own field $E_p$ **opposing** the original field
$E_0$, so the net field inside the dielectric is reduced:

$$ E = E_0 - E_p = \frac{E_0}{\varepsilon_r} $$

The number $\varepsilon_r$ (also written $K$) is the **dielectric constant** or
relative permittivity. Since $V = Ed$ falls by the same factor while $Q$ is
unchanged, the capacitance rises:

$$ \varepsilon_r = \frac{E_0}{E} = \frac{V_0}{V} = \frac{C}{C_0} $$

| Material | $\varepsilon_r$ | Material | $\varepsilon_r$ |
|---|---|---|---|
| Vacuum | 1 (exactly) | Mica | 6 |
| Air | 1.0006 | Glass | 5–10 |
| Paper | 3.7 | Water | 80 |

### Electric displacement

Inside a dielectric two kinds of charge exist: **free** charge on the plates and
**bound** charge on the dielectric faces. It is convenient to define a vector
that responds only to the free charge, the **electric displacement**:

$$ \vec{D} = \varepsilon_0\vec{E} + \vec{P} = \varepsilon_0\varepsilon_r\vec{E} $$

Its magnitude equals the free surface charge density, $D = \sigma_{free}$, and
its unit is C m⁻². Gauss's law then takes the compact form

$$ \oint \vec{D}\cdot d\vec{A} = q_{free} $$

so the bound charges never have to be counted explicitly.

Every dielectric also has a **dielectric strength** — the largest field it can
withstand before it ionises and conducts. For air this is about
$3\times10^{6}\ \text{V m}^{-1}$, which is why a capacitor is rated for a maximum
working voltage as well as a capacitance.

::: tip Battery connected, or battery removed?
The effect of inserting a dielectric depends entirely on what is held fixed.

| Quantity | Battery still connected ($V$ fixed) | Battery removed ($Q$ fixed) |
|---|---|---|
| $C$ | $\times\varepsilon_r$ | $\times\varepsilon_r$ |
| $Q$ | $\times\varepsilon_r$ | unchanged |
| $V$ | unchanged | $\div\varepsilon_r$ |
| $E$ | unchanged | $\div\varepsilon_r$ |
| $U$ | $\times\varepsilon_r$ | $\div\varepsilon_r$ |

Decide which column applies **before** you start the arithmetic.
:::

::: example Worked example 22.4
**Problem.** A parallel plate capacitor has plates of area $100\ \text{cm}^{2}$
separated by $5\ \text{mm}$. A slab of thickness $3\ \text{mm}$ and dielectric
constant $3$ is inserted between the plates. Find the capacitance before and
after insertion.

**Solution.** $A = 1.0\times10^{-2}\ \text{m}^{2}$, $d = 5.0\times10^{-3}\ \text{m}$.

Before:
$$ C_0 = \frac{\varepsilon_0 A}{d}
= \frac{8.85\times10^{-12}\times1.0\times10^{-2}}{5.0\times10^{-3}}
= 1.77\times10^{-11}\ \text{F} = 17.7\ \text{pF} $$

After, with $t = 3.0\times10^{-3}\ \text{m}$ and $\varepsilon_r = 3$, the
effective separation is

$$ d - t + \frac{t}{\varepsilon_r} = 5.0 - 3.0 + 1.0 = 3.0\ \text{mm} $$

$$ C = \frac{8.85\times10^{-12}\times1.0\times10^{-2}}{3.0\times10^{-3}}
= 2.95\times10^{-11}\ \text{F} = 29.5\ \text{pF} $$

The slab raises the capacitance by a factor of $5/3$, not by $\varepsilon_r = 3$,
because it fills only part of the gap.
:::

## Chapter summary

- $C = Q/V$, unit farad (C V⁻¹); capacitance depends on geometry and medium only.
- Isolated sphere: $C = 4\pi\varepsilon_0R$.
- Parallel plate capacitor: $E = \sigma/\varepsilon_0$, $V = Ed$, and
  $C = \varepsilon_0\varepsilon_r A/d$. With a partial slab,
  $C = \varepsilon_0A/(d - t + t/\varepsilon_r)$.
- Series: same $Q$, $1/C_{eq} = \sum 1/C_i$, result smaller than the smallest.
  Parallel: same $V$, $C_{eq} = \sum C_i$, result larger than the largest.
- Stored energy $U = \frac{Q^{2}}{2C} = \frac{1}{2}QV = \frac{1}{2}CV^{2}$; it is
  the area under the $Q$–$V$ line.
- Energy per unit volume of any electric field: $u = \frac{1}{2}\varepsilon_0E^{2}$.
- Sharing charge always wastes energy:
  $\Delta U = C_1C_2(V_1-V_2)^{2}/2(C_1+C_2)$.
- A dielectric polarizes, producing bound surface charge $\sigma_p = P$ which
  reduces the field to $E_0/\varepsilon_r$ and multiplies $C$ by $\varepsilon_r$.
  Displacement $\vec{D} = \varepsilon_0\vec{E} + \vec{P}$ responds to free charge
  only.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of capacitance, the farad, is equivalent to <span class="marks">[1]</span>
   (a) $\text{C V}$ (b) $\text{C V}^{-1}$ (c) $\text{V C}^{-1}$ (d) $\text{J C}^{-1}$
2. Three capacitors each of $3\ \mu\text{F}$ are connected in series. The
   equivalent capacitance is <span class="marks">[1]</span>
   (a) $9\ \mu\text{F}$ (b) $3\ \mu\text{F}$ (c) $1\ \mu\text{F}$ (d) $0.33\ \mu\text{F}$
3. The energy stored in a capacitor of capacitance $C$ at a p.d. $V$ is <span class="marks">[1]</span>
   (a) $CV$ (b) $CV^{2}$ (c) $\frac{1}{2}CV^{2}$ (d) $\frac{1}{2}C^{2}V$
4. A charged capacitor is disconnected from the battery and a dielectric of
   constant $K$ is inserted. The potential difference <span class="marks">[1]</span>
   (a) becomes $K$ times (b) becomes $1/K$ times (c) is unchanged (d) becomes zero
5. The capacitance of a parallel plate capacitor does **not** depend on <span class="marks">[1]</span>
   (a) plate area (b) plate separation (c) the dielectric (d) the charge on the plates

::: note Answers to Group A
**1.** (b) — from $C = Q/V$, coulomb per volt.
**2.** (c) — $1/C = 3/3 = 1$, so $C = 1\ \mu\text{F}$.
**3.** (c) — the area of the triangle under the $Q$–$V$ line.
**4.** (b) — $Q$ is fixed, $C$ becomes $KC$, so $V = Q/C$ falls by $K$.
**5.** (d) — $C$ is fixed by geometry and medium alone.
:::

**Group B — Short answer (5 marks each)**

1. Define capacitance and the farad. Derive an expression for the capacitance of
   a parallel plate capacitor with air between the plates. <span class="marks">[5]</span>
2. Derive expressions for the equivalent capacitance of three capacitors
   connected (a) in series and (b) in parallel. <span class="marks">[5]</span>
3. Show that the energy stored in a capacitor is $\frac{1}{2}CV^{2}$, and hence
   obtain the energy density of an electric field. <span class="marks">[5]</span>
4. Capacitors of $2\ \mu\text{F}$, $3\ \mu\text{F}$ and $6\ \mu\text{F}$ are
   joined in series across a $100\ \text{V}$ supply. Find the equivalent
   capacitance, the charge on each and the p.d. across each. <span class="marks">[5]</span>
5. A $2\ \mu\text{F}$ capacitor charged to $100\ \text{V}$ is connected across an
   uncharged $3\ \mu\text{F}$ capacitor. Find the common potential and the energy
   lost. <span class="marks">[5]</span>

::: note Answers to Group B
**4.** $\dfrac{1}{C} = \dfrac{1}{2} + \dfrac{1}{3} + \dfrac{1}{6} = 1$, so
$C_{eq} = 1\ \mu\text{F}$. The charge is the same on each:
$Q = 1\times10^{-6}\times100 = 100\ \mu\text{C}$. The potential differences are
$V = Q/C$: $100/2 = 50\ \text{V}$, $100/3 = 33.3\ \text{V}$ and
$100/6 = 16.7\ \text{V}$, which add to $100\ \text{V}$ as required.

**5.** Charge is conserved:
$V = \dfrac{C_1V_1}{C_1+C_2} = \dfrac{2\times100}{5} = 40\ \text{V}$.
$U_i = \frac12(2\times10^{-6})(100)^{2} = 1.0\times10^{-2}\ \text{J}$;
$U_f = \frac12(5\times10^{-6})(40)^{2} = 4.0\times10^{-3}\ \text{J}$.
Energy lost $= 6.0\times10^{-3}\ \text{J}$, which agrees with
$C_1C_2(V_1-V_2)^{2}/2(C_1+C_2)$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive an expression for the capacitance of a parallel plate capacitor and
   show that inserting a dielectric slab of thickness $t$ and dielectric constant
   $K$ changes it to $C = \varepsilon_0A/(d - t + t/K)$. <span class="marks">[5]</span>
   (b) Explain, in terms of polarization, why a dielectric increases the
   capacitance. <span class="marks">[3]</span>
2. (a) Derive an expression for the energy stored in a charged capacitor. <span class="marks">[3]</span>
   (b) A $2\ \mu\text{F}$ and a $3\ \mu\text{F}$ capacitor are connected in
   parallel, and this combination is joined in series with a $5\ \mu\text{F}$
   capacitor across a $50\ \text{V}$ supply. Find the equivalent capacitance, the
   charge on each capacitor, and the total energy stored. <span class="marks">[5]</span>

::: note Answer to Group C question 2
(a) With charge $q$ on the plates the p.d. is $q/C$, so $dW = (q/C)dq$ and
$W = \int_0^Q (q/C)\,dq = Q^{2}/2C = \frac12 CV^{2}$.

(b) Parallel section: $C_p = 2 + 3 = 5\ \mu\text{F}$. In series with
$5\ \mu\text{F}$: $1/C_{eq} = 1/5 + 1/5 = 2/5$, so $C_{eq} = 2.5\ \mu\text{F}$.

Total charge $Q = 2.5\times10^{-6}\times50 = 125\ \mu\text{C}$, which is the
charge on the $5\ \mu\text{F}$ capacitor. Its p.d. is $125/5 = 25\ \text{V}$, so
the parallel pair also has $25\ \text{V}$ across it. Hence
$Q_1 = 2\times25 = 50\ \mu\text{C}$ and $Q_2 = 3\times25 = 75\ \mu\text{C}$
(and $50 + 75 = 125\ \mu\text{C}$, as it must).

Total energy $U = \frac12 C_{eq}V^{2} = \frac12(2.5\times10^{-6})(50)^{2}
= 3.125\times10^{-3}\ \text{J} = 3.125\ \text{mJ}$.
:::

---
subject: Physics
grade: 12
unit: 15
title: Thermoelectric effects
hours: 3
area: Electricity and Magnetism
---

Heat and electricity are usually separate chapters, but at the junction of two
different metals they are directly linked: a temperature difference produces an
e.m.f., and a current produces a temperature difference. These are the Seebeck
and Peltier effects. They are the basis of the thermocouple thermometer used in
every industrial furnace, of the thermopile that detects heat radiation, and of
the solid-state coolers in portable fridges.

::: key What the exam wants from this unit
Three things, every year: the direction of the thermoelectric current (Seebeck
series), the parabola $E = \alpha\theta + \frac{1}{2}\beta\theta^{2}$ with its
neutral and inversion temperatures, and the table of differences between Peltier
and Joule heating. The numericals are almost always about $\theta_n$ and
$\theta_i$.
:::

## 15.1 Seebeck effect; Thermocouples

::: definition Seebeck effect
When two wires of **different** metals are joined to form a closed circuit and
the two junctions are kept at **different temperatures**, an e.m.f. is set up in
the circuit and a current flows round it. The effect is called the Seebeck or
thermoelectric effect, the e.m.f. is the **thermo-e.m.f.**, and the pair of
metals with its two junctions is a **thermocouple**.
:::

Thomas Seebeck discovered it in 1821. The thermo-e.m.f. is small — of the order
of tens of microvolts per degree — and it depends on only two things:

1. the **nature of the two metals**, and
2. the **temperature difference** between the two junctions.

It does not depend on the thickness of the wires, the length of the wires, or the
shape of the junctions.

```figure caption="A copper–iron thermocouple. The current flows from iron to copper through the cold junction, and from copper to iron through the hot junction."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.8))
CU, FE = '#b5651d', '#3f4a5a'
A = np.array([0.70, 0.0]); B = np.array([6.30, 0.0])
top = [A, (2.20,1.05), (4.80,1.05), B]
bot = [A, (2.20,-1.05), (4.80,-1.05), B]
ax.plot([p[0] for p in top], [p[1] for p in top], color=CU, lw=2.6,
        solid_capstyle='round', zorder=3)
ax.plot([p[0] for p in bot], [p[1] for p in bot], color=FE, lw=2.6,
        solid_capstyle='round', zorder=3)
ax.annotate('copper', (4.10,1.30), ha='center', fontsize=9.0, color=CU)
ax.annotate('iron', (3.10,-1.34), ha='center', fontsize=9.0, color=FE)
ax.add_patch(Circle((4.10,-1.05), 0.38, fc='white', ec=INK, lw=1.3, zorder=4))
ax.annotate('G', (4.10,-1.05), ha='center', va='center', fontsize=9.6, zorder=5)
ax.add_patch(FancyBboxPatch((0.16,-0.44), 1.08, 0.88, boxstyle='round,pad=0.06',
             fc='#f6d9d4', ec='#A8271F', lw=1.1, zorder=1))
ax.add_patch(FancyBboxPatch((5.76,-0.44), 1.08, 0.88, boxstyle='round,pad=0.06',
             fc='#dbe8f6', ec=ACCENT, lw=1.1, zorder=1))
ax.annotate('hot junction\nat $\\theta$', (0.70,-1.35), ha='center', va='center',
            fontsize=8.6, color='#A8271F')
ax.annotate('cold junction\nat $0\\,^{\\circ}$C', (6.30,-1.35), ha='center',
            va='center', fontsize=8.6, color=ACCENT)
for p in (A, B):
    ax.plot([p[0]],[p[1]],'o', color=INK, ms=6, zorder=5)
# Cu -> Fe through the hot junction: top wire carries the current towards A
ax.annotate('', xy=(2.75,1.05), xytext=(3.55,1.05),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.7, mutation_scale=12))
ax.annotate('', xy=(3.40,-1.05), xytext=(2.60,-1.05),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.7, mutation_scale=12))
ax.annotate('$I$', (3.15,1.26), ha='center', color='#0B6A62', fontsize=9.4)
ax.annotate('$I$', (3.00,-0.82), ha='center', color='#0B6A62', fontsize=9.4)
ax.set_xlim(-0.35,7.35); ax.set_ylim(-1.95,1.75); ax.set_aspect('equal'); ax.axis('off')
```
### Direction of the thermoelectric current: the thermoelectric series

Arrange metals in the **Seebeck (thermoelectric) series**:

> **Sb, Fe, Cd, Zn, Ag, Au, Cr, Sn, Pb, Hg, Mn, Cu, Pt, Co, Ni, Bi**

Two rules follow:

- **Direction.** In the thermocouple the current flows through the **cold
  junction** from the metal that comes *earlier* in the series to the metal that
  comes *later*. (Through the hot junction it therefore flows the other way.)
- **Magnitude.** The further apart the two metals are in the series, the larger
  the thermo-e.m.f. Antimony and bismuth stand at the two ends, so an Sb–Bi
  couple gives the biggest e.m.f. of all — which is why thermopiles are built
  from it.

::: memory Two mnemonics worth memorising
**"A–B–C"** — **A**ntimony to **B**ismuth through the **C**old junction.
**"hot coffee"** — **Co**pper to **Fe** (iron) through the **hot** junction,
and therefore iron to copper through the cold junction.
:::

**Why it happens.** The free-electron concentration is different in the two
metals. Where they touch, electrons diffuse from the metal of higher
concentration to the metal of lower concentration until a **contact potential
difference** stops the flow. This contact p.d. depends on temperature. If both
junctions are at the same temperature the two contact p.d.s are equal and
opposite and cancel round the loop; if the junctions are at different
temperatures they no longer cancel, and the difference is the thermo-e.m.f.

### Thermocouple thermometers

To use a thermocouple as a thermometer, keep the cold junction in melting ice
(a fixed $0\,^{\circ}\text{C}$ reference) and put the hot junction where the
temperature is wanted. The galvanometer or potentiometer reading is converted to
temperature from a calibration curve.

| Thermocouple | Useful range |
|---|---|
| Copper–constantan | $-200\,^{\circ}$C to $400\,^{\circ}$C |
| Iron–constantan | $-200\,^{\circ}$C to $750\,^{\circ}$C |
| Chromel–alumel | $-200\,^{\circ}$C to $1100\,^{\circ}$C |
| Platinum–platinum/rhodium | $0\,^{\circ}$C to $1600\,^{\circ}$C |

**Advantages:** very wide range; the junction is tiny, so its heat capacity is
small and it responds in a fraction of a second; it measures the temperature at a
*point*; the reading can be taken hundreds of metres away, which is why the
kilns of a brick factory or a cement plant in Hetauda are monitored this way.

**Disadvantages:** the e.m.f. is small, so a sensitive instrument is needed; the
calibration is **not linear**; a reference junction must be maintained.

::: caution A thermocouple with both junctions in the same bath reads nothing
The Seebeck e.m.f. depends on the *difference* of junction temperatures. If the
"cold" junction is allowed to drift to the temperature of the hot one, the e.m.f.
falls to zero even though the furnace is white hot. Always check the reference
junction first.
:::

## 15.2 Peltier effect: Variation of thermoelectric e.m.f. with temperature; Thermopile

### The Peltier effect

::: definition Peltier effect
When an electric current is passed through the junction of two dissimilar
metals, heat is **evolved** at one junction and **absorbed** at the other. If the
direction of the current is reversed, the two junctions exchange roles. This is
the converse of the Seebeck effect.
:::

```figure caption="Peltier effect. An external cell drives the current; where it passes from copper to iron the junction cools, where it passes from iron to copper the junction warms."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,2.9))
CU, FE = '#b5651d', '#3f4a5a'
A = np.array([0.70, 0.0]); B = np.array([6.30, 0.0])
top = [A, (2.20,1.05), (4.80,1.05), B]
bot = [A, (2.20,-1.05), (4.80,-1.05), B]
ax.plot([p[0] for p in top], [p[1] for p in top], color=CU, lw=2.6,
        solid_capstyle='round', zorder=3)
ax.plot([p[0] for p in bot], [p[1] for p in bot], color=FE, lw=2.6,
        solid_capstyle='round', zorder=3)
ax.annotate('copper', (4.30,1.30), ha='center', fontsize=9.0, color=CU)
ax.annotate('iron', (3.50,-1.32), ha='center', fontsize=9.0, color=FE)
# external cell inserted in the copper wire
ax.plot([3.30,3.62],[1.05,1.05], color='white', lw=3.4, zorder=4)
ax.plot([3.40,3.40],[0.72,1.38], color=INK, lw=1.4, zorder=5)
ax.plot([3.72,3.72],[0.88,1.22], color=INK, lw=3.6, zorder=5)
ax.annotate('external cell', (3.56,1.62), ha='center', fontsize=8.6)
# clockwise current: to the right on top, to the left underneath
ax.annotate('', xy=(2.95,1.05), xytext=(2.45,1.05),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.7, mutation_scale=12))
ax.annotate('', xy=(2.55,-1.05), xytext=(3.05,-1.05),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.7, mutation_scale=12))
ax.annotate('$I$', (2.70,1.26), ha='center', color='#0B6A62', fontsize=9.4)
ax.annotate('$I$', (2.80,-0.82), ha='center', color='#0B6A62', fontsize=9.4)
ax.add_patch(FancyBboxPatch((0.16,-0.44), 1.08, 0.88, boxstyle='round,pad=0.06',
             fc='#f6d9d4', ec='#A8271F', lw=1.1, zorder=1))
ax.add_patch(FancyBboxPatch((5.76,-0.44), 1.08, 0.88, boxstyle='round,pad=0.06',
             fc='#dbe8f6', ec=ACCENT, lw=1.1, zorder=1))
ax.annotate('Fe $\\rightarrow$ Cu\nheat evolved\n(warms)',
            (0.70,-1.55), ha='center', va='center', fontsize=8.4, color='#A8271F')
ax.annotate('Cu $\\rightarrow$ Fe\nheat absorbed\n(cools)',
            (6.30,-1.55), ha='center', va='center', fontsize=8.4, color=ACCENT)
for p in (A, B):
    ax.plot([p[0]],[p[1]],'o', color=INK, ms=6, zorder=5)
ax.set_xlim(-0.50,7.50); ax.set_ylim(-2.30,1.95); ax.set_aspect('equal'); ax.axis('off')
```
The **Peltier coefficient** $\pi$ of a junction is the heat absorbed or evolved
when unit charge crosses it. Since a current $I$ carries a charge $q = It$ in
time $t$,

$$ H = \pi q = \pi I t $$

so $\pi$ is measured in joule per coulomb, i.e. **volts**; for metal junctions it
is of the order of millivolts.

::: key Peltier heating is not Joule heating
| Peltier heat | Joule heat |
|---|---|
| Only at a **junction** of two different metals | In **any** conductor |
| $H = \pi I t$ — proportional to $I$ | $H = I^{2}Rt$ — proportional to $I^{2}$ |
| **Reversible**: reversing $I$ turns evolution into absorption | **Irreversible**: heat is evolved whichever way $I$ flows |
| Can cool a junction below room temperature | Always warms the conductor |
:::

A junction that absorbs Peltier heat is one at which the current flows in the
direction it would take through the **hot** junction of a Seebeck circuit of the
same pair — for copper and iron, from copper to iron. The reason is simply that a
working thermocouple is a heat engine: it takes in heat at the hot junction and
rejects it at the cold one.

> **Thomson effect (for completeness).** Heat is also absorbed or evolved when a
> current flows along a *single* conductor whose two ends are at different
> temperatures. It is positive for copper, silver and zinc, negative for iron,
> cobalt and nickel, and zero for lead — which is why lead is taken as the
> reference metal.

### Variation of thermo-e.m.f. with temperature

Keep the cold junction at $0\,^{\circ}\text{C}$ and raise the hot junction to
$\theta$. Experiment shows that the thermo-e.m.f. is not proportional to
$\theta$; it follows a parabola:

$$ E = \alpha\theta + \tfrac{1}{2}\beta\theta^{2} $$

where $\alpha$ and $\beta$ are constants of the pair of metals. For most couples
$\alpha$ is positive and $\beta$ is small and **negative**, so the curve rises,
turns over and comes back down.

```figure caption="Left: thermo-e.m.f. against hot-junction temperature for $\\alpha = 25\\ \\mu$V/$^{\\circ}$C, $\\beta = -0.1\\ \\mu$V/$^{\\circ}$C$^2$. Right: the thermoelectric power $dE/d\\theta$ falls linearly and changes sign at $\\theta_n$."

import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(5.2,2.6))
a, b = 25.0, -0.1
th = np.linspace(0, 600, 500)
E = a*th + 0.5*b*th**2
tn, ti = 250.0, 500.0
Em = a*tn + 0.5*b*tn**2

ax = axs[0]
ax.plot(th, E, color=ACCENT, lw=2.0)
ax.axhline(0, color=INK, lw=0.9)
ax.plot([tn,tn],[0,Em], color=MUTED, lw=0.9, ls=':')
ax.plot([tn],[Em],'o', color='#A8271F', ms=5, zorder=5)
ax.plot([ti],[0],'o', color='#0B6A62', ms=5, zorder=5)
ax.annotate('$\\theta_n$', (tn,0), textcoords='offset points', xytext=(-17,-14),
            ha='right', color=MUTED, fontsize=9.6)
ax.annotate('$\\theta_i$', (ti,0), textcoords='offset points', xytext=(13,-4),
            ha='center', color='#0B6A62', fontsize=9.6)
ax.annotate('$E_{max}$', (tn,Em), textcoords='offset points', xytext=(5,3),
            color='#A8271F', fontsize=9.0)
ax.annotate('e.m.f. reverses\nbeyond $\\theta_i$', (330,-1330), ha='center',
            fontsize=7.8, color=MUTED)
ax.set_xlabel('$\\theta$  ($^{\\circ}$C)'); ax.set_ylabel('$E$  ($\\mu$V)')
ax.set_xlim(0,600); ax.set_ylim(-1800,3900)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)

ax = axs[1]
ax.plot(th, a + b*th, color='#A8271F', lw=2.0)
ax.axhline(0, color=INK, lw=0.9)
ax.plot([tn],[0],'o', color='#A8271F', ms=5, zorder=5)
ax.annotate('$\\theta_n$', (tn,0), textcoords='offset points', xytext=(-3,-17),
            ha='center', color=MUTED, fontsize=9.6)
ax.set_xlabel('$\\theta$  ($^{\\circ}$C)')
ax.set_ylabel('$dE/d\\theta$  ($\\mu$V/$^{\\circ}$C)')
ax.set_xlim(0,600); ax.set_ylim(-40,30)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
fig.tight_layout()
```
::: derivation Neutral temperature and temperature of inversion
**Thermoelectric power.** Differentiating $E = \alpha\theta + \frac{1}{2}\beta\theta^{2}$,

$$ S = \frac{dE}{d\theta} = \alpha + \beta\theta $$

This is the **thermoelectric power** (or Seebeck coefficient) — the e.m.f. per
degree. It falls linearly as $\theta$ rises.

**Neutral temperature $\theta_n$.** The e.m.f. is a maximum where
$dE/d\theta = 0$:

$$ \alpha + \beta\theta_n = 0 \;\Longrightarrow\;
\boxed{\theta_n = -\frac{\alpha}{\beta}} $$

$\theta_n$ contains only $\alpha$ and $\beta$, so it depends **only on the pair
of metals** — not on the temperature of the cold junction. The maximum e.m.f. is
$E_{max} = -\alpha^{2}/2\beta$.

**Temperature of inversion $\theta_i$.** Beyond $\theta_n$ the e.m.f. falls, and
at some higher temperature it becomes zero and then **reverses** direction.
Putting $E = 0$ with the cold junction at $0\,^{\circ}\text{C}$:

$$ \theta\left(\alpha + \tfrac{1}{2}\beta\theta\right) = 0
\;\Longrightarrow\; \theta_i = -\frac{2\alpha}{\beta} = 2\theta_n $$

If the cold junction is at $\theta_c$ instead of $0\,^{\circ}\text{C}$, the
neutral temperature stays put but the inversion temperature shifts, because
$\theta_n$ always lies **midway** between $\theta_c$ and $\theta_i$:

$$ \boxed{\theta_i = 2\theta_n - \theta_c} $$
:::

::: caution $\theta_n$ is fixed, $\theta_i$ is not
A very common error is to say that both temperatures depend on the cold junction.
Only $\theta_i$ does. Raise the cold junction by $10\,^{\circ}\text{C}$ and
$\theta_i$ falls by $10\,^{\circ}\text{C}$, while $\theta_n$ does not move at
all.
:::

::: example Worked example 15.1
**Problem.** For a thermocouple with its cold junction at $0\,^{\circ}\text{C}$,
the thermo-e.m.f. in microvolts is $E = 25\theta - 0.05\theta^{2}$. Find
(a) $\alpha$ and $\beta$, (b) the neutral temperature, (c) the temperature of
inversion, (d) the maximum e.m.f., (e) the thermoelectric power at
$100\,^{\circ}\text{C}$, and (f) the two hot-junction temperatures at which
$E = 3000\ \mu\text{V}$.

**Solution.**

(a) Comparing with $E = \alpha\theta + \frac{1}{2}\beta\theta^{2}$:
$\alpha = 25\ \mu\text{V}\,^{\circ}\text{C}^{-1}$ and
$\frac{1}{2}\beta = -0.05$, so $\beta = -0.1\ \mu\text{V}\,^{\circ}\text{C}^{-2}$.

(b) $\theta_n = -\alpha/\beta = -25/(-0.1) = 250\,^{\circ}\text{C}$.

(c) $\theta_i = 2\theta_n - \theta_c = 2(250) - 0 = 500\,^{\circ}\text{C}$.

(d) $E_{max} = 25(250) - 0.05(250)^{2} = 6250 - 3125 = 3125\ \mu\text{V}
= 3.125\ \text{mV}$.

(e) $S = \alpha + \beta\theta = 25 - 0.1(100) = 15\ \mu\text{V}\,^{\circ}\text{C}^{-1}$.

(f) $25\theta - 0.05\theta^{2} = 3000 \Rightarrow \theta^{2} - 500\theta + 60000 = 0$,

$$ \theta = \frac{500 \pm \sqrt{250000 - 240000}}{2} = \frac{500 \pm 100}{2} $$

so $\theta = 200\,^{\circ}\text{C}$ or $300\,^{\circ}\text{C}$ — one on each side
of $\theta_n$, as the parabola requires.
:::

::: example Worked example 15.2
**Problem.** The neutral temperature of a copper–iron thermocouple is
$270\,^{\circ}\text{C}$. Find its temperature of inversion when the cold junction
is kept at (a) $0\,^{\circ}\text{C}$ and (b) $20\,^{\circ}\text{C}$. If
$\alpha = 13.5\ \mu\text{V}\,^{\circ}\text{C}^{-1}$, find $\beta$ and the
e.m.f. at $\theta = 100\,^{\circ}\text{C}$ with the cold junction at
$0\,^{\circ}\text{C}$.

**Solution.**

(a) $\theta_i = 2\theta_n - \theta_c = 540 - 0 = 540\,^{\circ}\text{C}$.

(b) $\theta_i = 540 - 20 = 520\,^{\circ}\text{C}$.

From $\theta_n = -\alpha/\beta$:
$$ \beta = -\frac{\alpha}{\theta_n} = -\frac{13.5}{270}
= -0.05\ \mu\text{V}\,^{\circ}\text{C}^{-2} $$

$$ E = 13.5(100) + \tfrac{1}{2}(-0.05)(100)^{2} = 1350 - 250 = 1100\ \mu\text{V}
= 1.10\ \text{mV} $$
:::

::: example Worked example 15.3
**Problem.** The Peltier coefficient of a junction is $12\ \text{mV}$ and its
resistance is $0.50\ \Omega$. A current of $2.0\ \text{A}$ is passed for
$5.0\ \text{minutes}$. Find (a) the Peltier heat and (b) the Joule heat, and
comment.

**Solution.** $t = 5.0 \times 60 = 300\ \text{s}$.

(a) $H_P = \pi It = (12\times10^{-3})(2.0)(300) = 7.2\ \text{J}$

(b) $H_J = I^{2}Rt = (2.0)^{2}(0.50)(300) = 600\ \text{J}$

The Joule heat is about 83 times larger, and it is *always* evolved. Reversing
the current leaves the $600\ \text{J}$ of Joule heating unchanged but turns the
$7.2\ \text{J}$ from evolved to absorbed. This is why practical Peltier coolers
use semiconductor pellets, whose Peltier coefficient is hundreds of times larger
than that of a metal junction while their resistance stays small.
:::

### The thermopile

A single thermocouple gives only microvolts. A **thermopile** is a large number
of thermocouples — usually antimony–bismuth, because that pair gives the largest
e.m.f. — joined **in series**, so that their e.m.f.s add.

```figure caption="A thermopile: antimony and bismuth bars in series. The front junctions are blackened and face the radiation; the back junctions are shielded and stay cool."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.0,3.1))
SB, BI = '#1d6fb8', '#A8271F'
F  = [(0.0, 0.0), (0.0, 0.95), (0.0, 1.90)]
Bk = [(2.60, 0.475), (2.60, 1.425), (2.60, 2.375)]
ax.add_patch(Rectangle((2.42, 0.10), 0.52, 2.70, fc='#e3e6ec', ec=MUTED,
                       lw=1.0, zorder=1))
ax.annotate('shielded\ncold junctions', (2.68, 3.32), ha='center',
            fontsize=8.0, color=MUTED)
for p, q, c in [(F[0],Bk[0],SB), (Bk[0],F[1],BI), (F[1],Bk[1],SB),
                (Bk[1],F[2],BI), (F[2],Bk[2],SB)]:
    ax.plot([p[0],q[0]], [p[1],q[1]], color=c, lw=3.0,
            solid_capstyle='round', zorder=3)
for p in F:
    ax.add_patch(Rectangle((p[0]-0.15, p[1]-0.15), 0.30, 0.30, fc='#14181f',
                           ec='#14181f', zorder=4))
for p in Bk:
    ax.plot([p[0]],[p[1]],'o', color=INK, ms=5.5, zorder=4)
ax.annotate('blackened\nhot junctions', (-0.05, 2.70), ha='center',
            fontsize=8.0, color=INK)
for y in (0.0, 0.95, 1.90):
    ax.annotate('', xy=(-0.34,y), xytext=(-1.90,y),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.5,
                                mutation_scale=11))
ax.annotate('heat\nradiation', (-2.00, 0.95), ha='right', va='center',
            fontsize=8.6, color='#d9534f')
ax.plot([0.0,0.0],[0.0,-1.05], color=INK, lw=1.3)
ax.plot([0.0,4.30],[-1.05,-1.05], color=INK, lw=1.3)
ax.plot([4.30,4.30],[-1.05,2.375], color=INK, lw=1.3)
ax.plot([4.30,2.60],[2.375,2.375], color=INK, lw=1.3)
ax.add_patch(Circle((2.30,-1.05), 0.36, fc='white', ec=INK, lw=1.3, zorder=4))
ax.annotate('G', (2.30,-1.05), ha='center', va='center', fontsize=9.6, zorder=5)
ax.plot([-3.05,-2.72],[-0.80,-0.80], color=SB, lw=3.0)
ax.annotate('antimony', (-2.62,-0.80), ha='left', va='center', fontsize=8.4, color=SB)
ax.plot([-3.05,-2.72],[-1.28,-1.28], color=BI, lw=3.0)
ax.annotate('bismuth', (-2.62,-1.28), ha='left', va='center', fontsize=8.4, color=BI)
ax.set_xlim(-3.25,5.05); ax.set_ylim(-1.90,3.75); ax.set_aspect('equal'); ax.axis('off')
```
Alternate junctions are **blackened** and exposed at the front of a polished
metal cone; the other set is shielded inside the case and stays at room
temperature. Radiation falling on the cone is absorbed by the black faces, raises
their temperature, and the series e.m.f. drives a current through a sensitive
galvanometer.

A thermopile is astonishingly sensitive: it will register the heat of a person
standing a few metres away, or of the Moon. Its uses include measuring radiant
heat and comparing the heating effects of different sources, radiation
pyrometers for furnaces, infrared detectors and burglar alarms, and — running
the Peltier effect backwards — portable thermoelectric refrigerators and the
radioisotope thermoelectric generators that power deep-space probes.

::: example Worked example 15.4
**Problem.** A copper–constantan thermocouple has a thermoelectric power of
$42\ \mu\text{V}\,^{\circ}\text{C}^{-1}$ near room temperature. The galvanometer
used with it can just detect $2.1\ \mu\text{V}$. What is the smallest temperature
difference it can measure? What e.m.f. would a thermopile of 40 such couples in
series give for a temperature difference of $0.50\,^{\circ}\text{C}$?

**Solution.** Smallest detectable difference:
$$ \Delta\theta = \frac{\Delta E}{S} = \frac{2.1\ \mu\text{V}}
{42\ \mu\text{V}\,^{\circ}\text{C}^{-1}} = 0.050\,^{\circ}\text{C} $$

For 40 couples in series the e.m.f.s add:
$$ E = N S\,\Delta\theta = 40 \times 42 \times 0.50 = 840\ \mu\text{V}
= 0.84\ \text{mV} $$
— comfortably measurable, which is exactly the point of a thermopile.
:::

```photogrid label="15.P" cols="2" ratio="1.2" caption="A thermometer made from two metals. (a) A K-type thermocouple is a pair of wires, nickel-chromium and nickel-aluminium, joined at the hot end; the other ends go to a plug. (b) The cell uses the standard table of thermo e.m.f. with the cold junction at 0 degrees C: 4.096 mV at 100 degrees, 8.138 mV at 200 degrees, 20.644 mV at 500 degrees and 41.276 mV at 1000 degrees. Dividing by temperature gives a nearly constant Seebeck coefficient, 41.0 microvolt per degree at 100 degrees and 41.3 at 1000 degrees. Because the e.m.f. rises almost linearly over such a wide range, the thermocouple is the standard sensor for furnaces, kilns and engines where a mercury thermometer would fail."
@ photo id="phy12b/thermocouple" cap="A K-type thermocouple wire with its plug"
fit 1.2
focus 0.5 0.5
@ svg cap="Thermo e.m.f. of a nickel-chromium / nickel-aluminium couple"
tab = [(100, 4.096), (200, 8.138), (500, 20.644), (1000, 41.276)]
rows = [("%d C" % t, e) for t, e in tab]
sens = [e / t * 1000 for t, e in tab]
assert round(sens[3], 1) == 41.3
f = Fig(300, 236)
f.text(150, 12, "e.m.f. with cold junction at 0 C, mV", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=45, fmt="%.3f", x0=56, y0=30, bw=160, gap=30)
f.text(150, 158, "mean sensitivity e / T in microvolt per C:", size=10, color=SLATE, bold=True)
f.text(150, 178, "%.1f, %.1f, %.1f, %.1f" % tuple(sens), size=10.5, color=NAVY, bold=True)
f.text(150, 198, "nearly constant, so e = a t is a good", size=10, color=SLATE, bold=True)
f.text(150, 214, "approximation up to 1000 deg C", size=10, color=SLATE, bold=True)
facts = dict(s=sens[0], s5=sens[2], s10=sens[3], e5=tab[2][1])
```

## Chapter summary

- **Seebeck effect:** two dissimilar metals, two junctions at different
  temperatures, an e.m.f. appears. It depends only on the metals and on the
  temperature difference.
- Seebeck series Sb, Fe, Cd, Zn, Ag, Au, Cr, Sn, Pb, Hg, Mn, Cu, Pt, Co, Ni, Bi:
  the current flows from the earlier metal to the later one through the **cold**
  junction, and the further apart the metals, the greater the e.m.f.
- **Peltier effect:** a current through a junction evolves heat at one junction
  and absorbs it at the other; $H = \pi It$, proportional to $I$ and
  **reversible**, unlike Joule heat $I^{2}Rt$.
- $E = \alpha\theta + \frac{1}{2}\beta\theta^{2}$ with the cold junction at
  $0\,^{\circ}\text{C}$; thermoelectric power $S = dE/d\theta = \alpha + \beta\theta$.
- Neutral temperature $\theta_n = -\alpha/\beta$ (where $E$ is maximum, fixed by
  the metals alone); temperature of inversion $\theta_i = 2\theta_n - \theta_c$
  (where $E$ returns to zero and reverses).
- $E_{max} = -\alpha^{2}/2\beta$, reached at $\theta_n$.
- A **thermopile** is many Sb–Bi couples in series, alternate junctions
  blackened, used to detect and measure heat radiation.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The Seebeck effect converts <span class="marks">[1]</span>
   (a) electrical energy into heat (b) heat into electrical energy
   (c) chemical energy into heat (d) magnetic energy into heat
2. The neutral temperature of a thermocouple depends on <span class="marks">[1]</span>
   (a) the temperature of the cold junction (b) the nature of the two metals only
   (c) the current in the circuit (d) the length of the wires
3. The Peltier heat developed at a junction is proportional to <span class="marks">[1]</span>
   (a) $I^{2}$ (b) $I$ (c) $\sqrt{I}$ (d) $1/I$
4. The neutral temperature of a thermocouple is $270\,^{\circ}$C. With the cold junction at $10\,^{\circ}$C the temperature of inversion is <span class="marks">[1]</span>
   (a) $260\,^{\circ}$C (b) $280\,^{\circ}$C (c) $530\,^{\circ}$C (d) $550\,^{\circ}$C
5. In a thermopile the thermocouples are joined <span class="marks">[1]</span>
   (a) in parallel (b) in series (c) in a bridge (d) back to back
6. Antimony and bismuth are chosen for a thermopile because <span class="marks">[1]</span>
   (a) they are cheap (b) they melt at a high temperature
   (c) they lie at opposite ends of the thermoelectric series (d) they are black

::: note Answers to Group A
**1.** (b) — a temperature difference produces an e.m.f.
**2.** (b) — $\theta_n = -\alpha/\beta$ contains only constants of the metal pair.
**3.** (b) — $H = \pi It$; the $I^{2}$ law belongs to Joule heating.
**4.** (c) — $\theta_i = 2\theta_n - \theta_c = 540 - 10 = 530\,^{\circ}$C.
**5.** (b) — in series so that the small e.m.f.s add.
**6.** (c) — the widest separation in the series gives the largest thermo-e.m.f.
:::

**Group B — Short answer (5 marks each)**

1. State the Seebeck effect. What is the thermoelectric series, and how is it used
   to find the direction of the thermoelectric current? State the direction in a
   copper–iron thermocouple. <span class="marks">[5]</span>
2. Starting from $E = \alpha\theta + \frac{1}{2}\beta\theta^{2}$, define the
   thermoelectric power, and obtain expressions for the neutral temperature and
   the temperature of inversion. <span class="marks">[5]</span>
3. For a thermocouple with its cold junction at $0\,^{\circ}$C the thermo-e.m.f.
   in microvolts is $E = 16\theta - 0.02\theta^{2}$. Find $\alpha$, $\beta$, the
   neutral temperature, the temperature of inversion, the maximum e.m.f. and the
   thermoelectric power at $100\,^{\circ}$C. <span class="marks">[5]</span>
4. Distinguish between Peltier heating and Joule heating on four counts. A
   junction of Peltier coefficient $10\ \text{mV}$ carries $3.0\ \text{A}$ for
   $200\ \text{s}$; find the Peltier heat. <span class="marks">[5]</span>
5. Give four advantages and two disadvantages of a thermocouple thermometer over
   a mercury-in-glass thermometer. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** See §15.1. Series: Sb, Fe, Cd, Zn, Ag, Au, Cr, Sn, Pb, Hg, Mn, Cu, Pt, Co,
Ni, Bi. Current flows from the earlier metal to the later one through the cold
junction; since Fe comes before Cu, the current flows **from iron to copper
through the cold junction** and from copper to iron through the hot junction.

**3.** $\alpha = 16\ \mu\text{V}\,^{\circ}\text{C}^{-1}$;
$\frac{1}{2}\beta = -0.02$ so $\beta = -0.04\ \mu\text{V}\,^{\circ}\text{C}^{-2}$.
$\theta_n = -\alpha/\beta = 16/0.04 = 400\,^{\circ}$C;
$\theta_i = 2\theta_n - 0 = 800\,^{\circ}$C;
$E_{max} = 16(400) - 0.02(400)^{2} = 6400 - 3200 = 3200\ \mu\text{V} = 3.2\ \text{mV}$;
$S = 16 - 0.04(100) = 12\ \mu\text{V}\,^{\circ}\text{C}^{-1}$.

**4.** Table in §15.2. $H = \pi It = (10\times10^{-3})(3.0)(200) = 6.0\ \text{J}$.

**5.** Advantages: very wide range; small heat capacity so fast response;
measures temperature at a point; reading can be taken remotely (and recorded
electrically). Disadvantages: the e.m.f. is very small and needs a sensitive
instrument; the calibration is non-linear and a reference junction must be
maintained.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe the Seebeck effect and sketch the variation of thermo-e.m.f. with
   the temperature of the hot junction. Define and locate the neutral temperature
   and the temperature of inversion on your graph. <span class="marks">[4]</span>
   (b) A copper–iron thermocouple has
   $\alpha = 13.5\ \mu\text{V}\,^{\circ}\text{C}^{-1}$ and
   $\beta = -0.05\ \mu\text{V}\,^{\circ}\text{C}^{-2}$ with the cold junction at
   $0\,^{\circ}$C. Find the neutral temperature, the temperature of inversion,
   the maximum e.m.f., and the e.m.f. when the hot junction is at
   $200\,^{\circ}$C. <span class="marks">[4]</span>
2. (a) State the Peltier effect and explain, with a diagram, how it differs from
   Joule heating. <span class="marks">[4]</span>
   (b) Describe the construction and working of a thermopile and give two of its
   uses. A thermopile of $50$ antimony–bismuth couples, each of thermoelectric
   power $100\ \mu\text{V}\,^{\circ}\text{C}^{-1}$, is connected to a
   galvanometer of total circuit resistance $25\ \Omega$. Find the current when
   the junctions differ by $0.40\,^{\circ}$C. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (b) $\theta_n = -\alpha/\beta = 13.5/0.05 = 270\,^{\circ}$C;
$\theta_i = 2(270) - 0 = 540\,^{\circ}$C;
$$ E_{max} = 13.5(270) - 0.025(270)^{2} = 3645 - 1822.5 = 1822.5\ \mu\text{V}
\approx 1.82\ \text{mV} $$
$$ E(200) = 13.5(200) - 0.025(200)^{2} = 2700 - 1000 = 1700\ \mu\text{V} = 1.70\ \text{mV} $$

**2.** (b) Total e.m.f.
$E = NS\,\Delta\theta = 50 \times 100 \times 0.40 = 2000\ \mu\text{V}
= 2.0\times10^{-3}\ \text{V}$. Hence
$$ I = \frac{E}{R} = \frac{2.0\times10^{-3}}{25} = 8.0\times10^{-5}\ \text{A}
= 80\ \mu\text{A} $$
which a sensitive galvanometer reads easily.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. What is the Seebeck effect? Explain the thermoelectric series, the neutral and inversion temperatures, and calculate the e.m.f. of a thermocouple. <span class="marks">[10]</span>
2. Describe the Peltier and Thomson effects, and distinguish the Peltier effect from Joule heating. <span class="marks">[10]</span>
3. What is a thermopile? Describe how thermocouples and thermopiles are used, and give eight applications of thermoelectric effects. <span class="marks">[10]</span>

### Model answer D1: Seebeck effect, neutral and inversion temperatures (10 marks)

**Introduction.** In 1821 T. J. Seebeck found that if the two junctions of a circuit made from two different metals are kept at different temperatures, an **e.m.f. (thermo-e.m.f.) appears and a current flows**. This is the **Seebeck effect**, and the circuit is a **thermocouple**.

**Explanation.** Free-electron densities differ in the two metals. At the hot junction, electrons diffuse more rapidly across the interface than at the cold junction, so a net potential difference is set up around the circuit. Its direction is reversed if the hot and cold ends are exchanged.

**Thermoelectric series.** The metals are arranged in a list such as **Bi, Ni, Co, Pt, Hg, Al, Pb, Sn, Cu, Au, Ag, Zn, Fe, Sb**. At the hot junction the current flows from the metal earlier in the list to the metal later in the list (for a Cu-Fe couple, from copper to iron). The farther apart the metals are in the series, the larger the e.m.f. (the bismuth-antimony pair gives the largest).

**Variation of e.m.f. with temperature.** If the cold junction is at $0^{\circ}$C and the hot junction is at $\theta$, the e.m.f. is found by experiment to be a parabola:

$$ e = a\theta + \tfrac{1}{2}b\theta^{2} $$

where $a$ and $b$ are constants of the pair of metals. The thermoelectric power (Seebeck coefficient) is

$$ S = \frac{de}{d\theta} = a + b\theta $$

1. **Neutral temperature $\theta_{n}$:** the temperature of the hot junction at which the e.m.f. is a **maximum**, so $de/d\theta = 0$, giving $\theta_{n} = -a/b$.
2. **Inversion temperature $\theta_{i}$:** the temperature at which the e.m.f. falls back to **zero** and then reverses; setting $e = 0$ gives $\theta_{i} = -2a/b = 2\theta_{n}$.
3. $\theta_{n}$ is independent of the cold-junction temperature, but $\theta_{i}$ depends on it: it is as far above $\theta_{n}$ as the cold junction is below it, $\theta_{i} = 2\theta_{n} - \theta_{c}$.

**Numerical.** For a Cu-Fe couple take $a = 14\ \mu\text{V}\,{}^{\circ}\text{C}^{-1}$ and $b = -0.035\ \mu\text{V}\,{}^{\circ}\text{C}^{-2}$, with the cold junction at $0^{\circ}$C.

- Neutral temperature: $\theta_{n} = -14/(-0.035) = 400^{\circ}$C.
- Inversion temperature: $\theta_{i} = 2\times400 = 800^{\circ}$C.
- E.m.f. at $200^{\circ}$C: $e = 14(200) + \tfrac{1}{2}(-0.035)(200)^{2} = 2800 - 700 = 2100\ \mu\text{V}$.
- Maximum e.m.f. at $400^{\circ}$C: $5600 - 2800 = 2800\ \mu\text{V}$.
- Seebeck coefficient at $200^{\circ}$C: $14 - 0.035\times200 = 7\ \mu\text{V}\,{}^{\circ}\text{C}^{-1}$.

| Hot junction ($^{\circ}$C) | E.m.f. ($\mu$V) | Remark |
|---|---|---|
| 100 | 1225 | Rising |
| 200 | 2100 | Rising |
| 400 | 2800 | Maximum, $\theta_{n}$ |
| 800 | 0 | Inversion, $\theta_{i}$ |

**Conclusion.** The thermo-e.m.f. is a parabolic function of temperature. For a precise thermometer one uses the range below the neutral temperature, where the e.m.f. rises steadily.

### Model answer D2: Peltier and Thomson effects (10 marks)

**Introduction.** The Seebeck effect converts heat into electricity. Its **reverse** was found by Peltier (1834): a current through a junction of two different metals produces **heating or cooling** at the junction.

**Peltier effect.** When a current $I$ is passed through a junction of two different metals, heat is **absorbed** at one junction and **liberated** at the other. Reversing the current reverses the effect. The heat exchanged in time $t$ is $Q = \Pi I t$, where $\Pi$ is the **Peltier coefficient**: the heat absorbed or evolved per unit charge, in J/C (volt). The Peltier and Seebeck coefficients are linked by $\Pi = ST$, where $T$ is the absolute temperature of the junction.

**Explanation.** When electrons pass from a metal where their mean energy is low into one where it is high they absorb energy (**cooling**), and when they move the other way they give the energy up (**heating**).

**Numerical.** For a junction with $S = 7\ \mu\text{V K}^{-1}$ at $T = 300\ \text{K}$: $\Pi = 7\times10^{-6}\times300 = 2.1\times10^{-3}\ \text{V}$. With $I = 2\ \text{A}$ for $10$ minutes the heat exchanged is $Q = \Pi I t = 2.1\times10^{-3}\times2\times600 = 2.52\ \text{J}$.

**Thomson effect (1851).** When a current flows along a **single metal** wire that has a temperature gradient, heat is absorbed or liberated along the wire in addition to Joule heating. The heat per unit charge per unit temperature difference is the **Thomson coefficient** $\sigma$. In copper, the heat is **absorbed** when the current flows from cold to hot; in iron it is the reverse. Thomson also linked all three effects with $\sigma = T\,dS/dT$.

**Comparison of Peltier and Joule heating.**

| Feature | Peltier effect | Joule heating |
|---|---|---|
| Occurs at | Junction of two different metals | Whole of the conductor |
| Depends on | $I$ (first power) | $I^{2}$ |
| Reversible? | Yes, heating or cooling | No, always heating |
| Formula | $Q = \Pi I t$ | $Q = I^{2}Rt$ |
| Use | Cooling, heat pumps | Heaters, fuses |

**Applications of the Peltier effect.** Small **Peltier coolers** (thermoelectric modules) with no moving parts cool CPUs, portable refrigerators, car cup-holders, and small vaccine boxes. Because the heat is moved by electric current, there is no noise or gas refrigerant.

**Conclusion.** The Seebeck, Peltier and Thomson effects are three aspects of the same coupling between heat and charge flow, and they are connected by the Kelvin relations. The Peltier effect is reversible and linear in the current, unlike Joule heating.

### Model answer D3: thermocouple, thermopile and applications (10 marks)

**Introduction.** A single thermocouple gives only a few millivolts, so in a practical instrument several are combined. A **thermopile** consists of a large number of thermocouples connected in series, with alternate junctions at the hot and cold ends. It gives the sum of the e.m.f.s and is much more sensitive.

**Thermopile.** Antimony and bismuth bars are soldered alternately in a compact box. All the odd junctions are blackened and exposed to the radiation, and all the even ones are shielded. If one couple gives $e$, a pile of $n$ couples gives $E = ne$. A pile of 40 Cu-Fe couples, each giving $1.225\ \text{mV}$ for a $100^{\circ}$C difference, gives $40\times1.225 = 49\ \text{mV}$. Joined to a sensitive galvanometer, it can detect a rise of one-thousandth of a degree.

**Thermocouple thermometer.** One junction is kept at a known temperature (ice) and the other is placed where the temperature is required. The e.m.f. is read on a millivoltmeter calibrated in degrees. Its advantages are a **wide range** (-200 to 1600 degrees C), small size, quick response and remote reading.

**Eight applications of thermoelectric effects.**

1. **Furnace and kiln thermometry:** a Pt-Rh thermocouple measures the temperature of brick kilns in Bhaktapur and of cement furnaces.
2. **Measurement of radiant heat:** a thermopile detects infrared radiation from the Sun and from stars.
3. **Thermoelectric generators:** spacecraft such as Voyager use the heat of decaying plutonium in a thermopile to make electricity.
4. **Peltier cooling:** compact refrigerators for medicines and vaccines in remote health posts.
5. **Fire safety:** the pilot flame of a gas heater heats a thermocouple, whose e.m.f. holds the gas valve open and shuts it if the flame goes out.
6. **Temperature control:** thermocouples in ovens, incubators and industrial boilers.
7. **Power from waste heat:** modules on the exhaust pipe or on cooking stoves that charge a mobile phone in villages without electricity.
8. **Medical and scientific use:** tiny thermocouples measure the temperature inside tissues and in the laboratory.

**Limitations.** The e.m.f. is small and not perfectly linear; the efficiency of the thermoelectric generators is low (around 5-8%), and the junctions need regular calibration.

**Conclusion.** The thermopile is a sensitive heat detector, and the thermocouple is a robust thermometer. With the Peltier effect they find uses from the kitchen to space.

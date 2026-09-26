---
subject: Physics
grade: 11
unit: 10
title: Thermal Expansion
hours: 4
area: Heat and Thermodynamics
---

Heat a solid and its molecules vibrate through wider swings about their lattice
positions, so their average separation grows and the body gets bigger. That one
sentence explains the gaps left between rails on the Janakpur railway, the
rollers under a bridge girder, the sag designed into transmission lines, and the
fact that a mercury thermometer works at all. In this unit we put numbers on the
effect: one coefficient for length, one for area, one for volume, and a special
treatment for liquids, which cannot be heated without a container that expands
too.

::: key The three coefficients are not independent
$\alpha$, $\beta$ and $\gamma$ describe expansion in one, two and three
dimensions, and for an isotropic solid they are in the ratio $1:2:3$. Learn the
derivation of $\beta = 2\alpha$ and $\gamma = 3\alpha$ — it is a standard Group B
question — and learn why a liquid has *two* expansivities.
:::

## 10.1 Linear expansion and its measurement

When a rod of length $l_1$ at temperature $\theta_1$ is heated to $\theta_2$, its
length becomes $l_2$. Experiment shows the increase is proportional to the
original length and to the temperature rise.

::: definition Coefficient of linear expansion
The coefficient of linear expansion (linear expansivity) $\alpha$ of a material
is the increase in length per unit original length per unit rise in temperature:

$$ \alpha = \frac{l_2 - l_1}{l_1(\theta_2 - \theta_1)}
\qquad \Longrightarrow \qquad l_2 = l_1\left[1 + \alpha(\theta_2-\theta_1)\right] $$

Its SI unit is K⁻¹ (numerically the same as °C⁻¹) and it has no dimensions of
length: $[\alpha] = [K^{-1}]$.
:::

Strictly $l_1$ should be the length at $0\ ^{\circ}\text{C}$, but because
$\alpha$ is of order $10^{-5}$ the difference between "length at $0\ ^{\circ}$C"
and "length at room temperature" changes the answer only in the fifth decimal
place, so any convenient starting length is used.

| Material | $\alpha$ ($\times 10^{-6}$ K⁻¹) | Material | $\alpha$ ($\times 10^{-6}$ K⁻¹) |
|---|---|---|---|
| Invar | 1.2 | Copper | 17 |
| Pyrex glass | 3.2 | Brass | 19 |
| Ordinary glass | 9 | Aluminium | 23 |
| Steel / iron / concrete | 12 | Lead | 29 |

Invar (an iron–nickel alloy) expands so little that it is used for pendulum rods
and survey tapes. Steel and concrete happen to have almost the same $\alpha$ —
which is the reason reinforced concrete does not tear itself apart in the
Terai summer.

### Measurement: Pullinger's apparatus

```figure caption="Pullinger's apparatus. The rod expands inside a steam jacket and the expansion is read on a micrometer screw whose contact with the rod completes the bell circuit."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.8,3.4))
# steam jacket and rod
ax.add_patch(Rectangle((1.6,0.55),1.9,4.00, fill=False, ec=INK, lw=1.4))
ax.add_patch(Rectangle((2.35,0.75),0.40,3.95, facecolor=GRID, ec=INK, lw=1.2))
ax.text(2.55,2.5,'rod', rotation=90, ha='center', va='center', fontsize=8.4, color=INK)
# rigid base with hatching
ax.add_patch(Rectangle((1.30,0.42),2.5,0.33, facecolor='none', ec=INK, lw=1.1))
for x0 in np.arange(1.32,3.64,0.20):
    ax.plot([x0,x0+0.16],[0.42,0.75],color=MUTED,lw=0.7)
# steam in / out
ax.annotate('', xy=(1.6,1.15), xytext=(0.25,1.15),
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.4,mutation_scale=11))
ax.text(0.18,1.34,'steam in',ha='left',fontsize=8.2,color=ACCENT)
ax.annotate('', xy=(4.35,4.15), xytext=(3.5,4.15),
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.4,mutation_scale=11))
ax.text(4.52,4.10,'steam out',ha='left',fontsize=8.2,color=ACCENT)
# thermometer
ax.plot([3.25,3.25],[2.10,4.88],color=INK,lw=1.2)
ax.add_patch(Circle((3.25,2.02),0.11,facecolor=SERIES[1],ec=INK,lw=0.8))
ax.text(3.42,4.82,'thermometer',fontsize=8.2,color=MUTED)
# micrometer
ax.add_patch(Rectangle((1.95,4.95),1.20,0.45, fill=False, ec=INK, lw=1.3))
ax.plot([2.55,2.55],[4.95,4.72],color=INK,lw=2.0)
ax.text(1.90,5.52,'micrometer screw',fontsize=8.2,color=INK,ha='left')
# length marker
ax.annotate('', xy=(2.05,4.70), xytext=(2.05,0.75),
            arrowprops=dict(arrowstyle='<|-|>',color=MUTED,lw=1.0,mutation_scale=8))
ax.text(1.98,2.7,'$l_1$',ha='right',fontsize=9.5,color=MUTED)
# circuit: micrometer -> bell -> battery -> base
ax.plot([3.15,6.45,6.45],[5.18,5.18,3.95],color=INK,lw=1.0)
ax.add_patch(Circle((6.45,3.62),0.30,fill=False,ec=INK,lw=1.2))
ax.text(6.88,3.55,'bell',fontsize=8.2,color=MUTED)
ax.plot([6.45,6.45],[3.32,2.70],color=INK,lw=1.0)
for y0,hw in [(2.70,0.28),(2.50,0.16)]:
    ax.plot([6.45-hw,6.45+hw],[y0,y0],color=INK,lw=1.4)
ax.text(6.88,2.50,'battery',fontsize=8.2,color=MUTED)
ax.plot([6.45,6.45,3.80],[2.50,0.58,0.58],color=INK,lw=1.0)
ax.set_xlim(-0.1,8.3); ax.set_ylim(0.0,5.9)
ax.set_aspect('equal'); ax.axis('off')
```

The rod under test stands on a fixed base inside a hollow **steam jacket**. Its
upper end is just below the tip of a **micrometer screw** carried on a rigid
frame. The screw, the rod and a battery with an electric bell are connected in
series, so the bell rings the instant the screw touches the rod.

1. With the rod at room temperature $\theta_1$ (read on the thermometer in the
   jacket), turn the screw down until the bell just rings; record the reading
   $a_1$. Measure the length $l_1$ of the rod with a metre rule.
2. Raise the screw well clear of the rod.
3. Pass steam through the jacket until the thermometer is steady at $\theta_2$.
   The rod has now expanded.
4. Turn the screw down again until the bell just rings; record $a_2$.

The expansion is $\delta l = a_1 - a_2$ (the screw has less distance to travel),
so

$$ \alpha = \frac{\delta l}{l_1(\theta_2-\theta_1)} $$

::: example Worked example 10.1
**Problem.** A steel railway rail is $30.0\ \text{m}$ long at $10\ ^{\circ}\text{C}$.
What gap must be left at each joint if the rail temperature can rise to
$45\ ^{\circ}\text{C}$? Take $\alpha_{\text{steel}} = 1.2\times10^{-5}\ \text{K}^{-1}$.

**Solution.** Temperature rise $\Delta\theta = 45 - 10 = 35\ \text{K}$.

$$ \delta l = l_1\alpha\Delta\theta = 30.0 \times 1.2\times10^{-5}\times 35
= 1.26\times10^{-2}\ \text{m} $$

So a gap of about $12.6\ \text{mm}$ is needed. (A gap smaller than this and the
rails push against each other and buckle in hot weather.)
:::

::: example Worked example 10.2
**Problem.** A pendulum clock with a steel pendulum keeps correct time at
$15\ ^{\circ}\text{C}$. How much time does it lose per day when the temperature
rises to $35\ ^{\circ}\text{C}$? Take $\alpha = 1.2\times10^{-5}\ \text{K}^{-1}$.

**Solution.** For a simple pendulum $T = 2\pi\sqrt{l/g}$, so $T \propto \sqrt{l}$.
With $l' = l(1+\alpha\Delta\theta)$,

$$ \frac{T'}{T} = \sqrt{1+\alpha\Delta\theta} \approx 1 + \tfrac{1}{2}\alpha\Delta\theta $$

The fractional gain in the period is $\frac{1}{2}\alpha\Delta\theta$, so in one
day of $86400\ \text{s}$ the clock loses

$$ \Delta t = \tfrac{1}{2}\alpha\Delta\theta \times 86400
= 0.5\times1.2\times10^{-5}\times20\times86400 = 10.4\ \text{s} $$

A longer pendulum swings more slowly, so the clock runs **slow** in hot weather.
:::

## 10.2 Cubical expansion, superficial expansion and relation with linear expansion

::: definition Superficial and cubical expansivity
**Superficial expansivity** $\beta$ is the increase in area per unit original
area per unit rise in temperature: $A_2 = A_1(1+\beta\Delta\theta)$.

**Cubical (volume) expansivity** $\gamma$ is the increase in volume per unit
original volume per unit rise in temperature: $V_2 = V_1(1+\gamma\Delta\theta)$.

Both have the unit K⁻¹.
:::

```figure caption="A square of side $l$ heated through $\Delta\theta$. The two shaded strips have total area $2l\,\delta l$; the corner square $(\delta l)^2$ is far smaller and is neglected, giving $\beta = 2\alpha$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.6))
ax = axes[0]
L, d = 1.0, 0.26
ax.add_patch(Rectangle((0,0),L,L, facecolor=GRID, ec=INK, lw=1.3))
ax.add_patch(Rectangle((L,0),d,L, facecolor=ACCENT, alpha=0.35, ec='none'))
ax.add_patch(Rectangle((0,L),L,d, facecolor=ACCENT, alpha=0.35, ec='none'))
ax.add_patch(Rectangle((L,L),d,d, facecolor=SERIES[1], alpha=0.55, ec='none'))
ax.add_patch(Rectangle((0,0),L+d,L+d, fill=False, ec=SERIES[1], lw=1.2, ls='--'))
ax.text(L/2, L/2, '$l^2$', ha='center', va='center', fontsize=10, color=INK)
ax.text(L+d/2, L/2, r'$l\,\delta l$', ha='center', va='center', fontsize=8.4,
        color=INK, rotation=90)
ax.text(L/2, L+d/2, r'$l\,\delta l$', ha='center', va='center', fontsize=8.4, color=INK)
ax.annotate(r'$(\delta l)^2$', (L+d/2, L+d/2), textcoords='offset points',
            xytext=(16,12), fontsize=8.4, color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=0.9, mutation_scale=9))
ax.annotate('', xy=(L,-0.14), xytext=(0,-0.14),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=8))
ax.text(L/2,-0.30,'$l$',ha='center',fontsize=9.5,color=MUTED)
ax.set_xlim(-0.2,1.75); ax.set_ylim(-0.42,1.60)
ax.set_title('(a) area', fontsize=9, color=INK)

ax = axes[1]
def cube(o, s, ec, ls, lw):
    x,y = o; k = 0.42*s
    pts = [((x,y),(x+s,y)),((x+s,y),(x+s,y+s)),((x+s,y+s),(x,y+s)),((x,y+s),(x,y)),
           ((x+s,y),(x+s+k,y+k)),((x+s,y+s),(x+s+k,y+s+k)),((x,y+s),(x+k,y+s+k)),
           ((x+s+k,y+k),(x+s+k,y+s+k)),((x+s+k,y+s+k),(x+k,y+s+k)),
           ((x+k,y+s+k),(x+k,y+k)),((x+k,y+k),(x+s+k,y+k))]
    for (p,q) in pts:
        ax.plot([p[0],q[0]],[p[1],q[1]], color=ec, ls=ls, lw=lw)
cube((0,0), 1.0, INK, '-', 1.3)
cube((0,0), 1.24, SERIES[1], '--', 1.1)
ax.text(0.5,0.22,'$V=l^3$',ha='center',fontsize=9.5,color=INK)
ax.text(1.05,2.12,r'$V(1+\gamma\Delta\theta)$',ha='center',fontsize=8.6,color=SERIES[1])
ax.set_xlim(-0.2,2.35); ax.set_ylim(-0.30,2.35)
ax.set_title('(b) volume', fontsize=9, color=INK)
for ax in axes:
    ax.set_aspect('equal'); ax.axis('off')
```

::: derivation The relations $\beta = 2\alpha$ and $\gamma = 3\alpha$
We start from the definition of linear expansivity applied to every edge of a body, and
reach the two relations connecting the three expansivities.

**Setting up.** Everything rests on one fact: when the temperature rises by
$\Delta\theta$, *every* length in the body grows by the same fraction, so a length $l$
becomes $l(1 + \alpha\Delta\theta)$.

**Part (a): $\beta = 2\alpha$**

**Step 1 — start with a square plate.** Let it have side $l$, so its area at the start is

$$ A_1 = l^{2} $$

**Step 2 — find the new side.** Each side is a length, so it grows by the fraction
$\alpha\Delta\theta$:

$$ l' = l(1 + \alpha\Delta\theta) $$

**Step 3 — square it to get the new area:**

$$ A_2 = l'^{2} = l^{2}(1 + \alpha\Delta\theta)^{2} $$

**Step 4 — expand the bracket.** Using $(1+x)^{2} = 1 + 2x + x^{2}$:

$$ A_2 = l^{2}\left(1 + 2\alpha\Delta\theta + \alpha^{2}\Delta\theta^{2}\right) $$

**Step 5 — throw away the tiny term.** For solids $\alpha$ is about
$10^{-5}\ \text{K}^{-1}$, so $\alpha^{2}$ is about $10^{-10}$ — ten thousand times
smaller than $\alpha$ itself. Dropping it changes nothing we could measure:

$$ A_2 \approx l^{2}(1 + 2\alpha\Delta\theta) $$

**Step 6 — put $A_1$ back in,** since $l^{2} = A_1$:

$$ A_2 \approx A_1(1 + 2\alpha\Delta\theta) $$

**Step 7 — compare with the definition of $\beta$,** which says
$A_2 = A_1(1 + \beta\Delta\theta)$. The two right-hand sides must agree for every
$\Delta\theta$, so the coefficients of $\Delta\theta$ must match:

$$ \beta = 2\alpha $$

---

**Part (b): $\gamma = 3\alpha$**

**Step 8 — start with a cube of side $l$,** so its volume at the start is

$$ V_1 = l^{3} $$

**Step 9 — cube the new side** $l(1+\alpha\Delta\theta)$ from Step 2:

$$ V_2 = l^{3}(1 + \alpha\Delta\theta)^{3} $$

**Step 10 — expand,** using $(1+x)^{3} = 1 + 3x + 3x^{2} + x^{3}$:

$$ V_2 = l^{3}\left(1 + 3\alpha\Delta\theta + 3\alpha^{2}\Delta\theta^{2}
+ \alpha^{3}\Delta\theta^{3}\right) $$

**Step 11 — drop the $\alpha^{2}$ and $\alpha^{3}$ terms** for the same reason as in
Step 5:

$$ V_2 \approx l^{3}(1 + 3\alpha\Delta\theta) = V_1(1 + 3\alpha\Delta\theta) $$

**Step 12 — compare with $V_2 = V_1(1 + \gamma\Delta\theta)$:**

$$ \gamma = 3\alpha $$

**Result.**

$$ \beta = 2\alpha, \qquad \gamma = 3\alpha, \qquad
\alpha : \beta : \gamma = 1 : 2 : 3, \qquad
\frac{\alpha}{1} = \frac{\beta}{2} = \frac{\gamma}{3} $$

**What it means.** The numbers $1, 2, 3$ are simply the number of directions involved: a
line stretches in one direction, an area in two, a volume in three. So you never need to
look up $\beta$ or $\gamma$ in a table — one number per material is enough.

**Conditions used.** $\alpha\Delta\theta \ll 1$, so that the squared and cubed terms can
be neglected; and $\alpha$ is the same in all directions (true for metals and glass, not
for wood or crystals like calcite). The shape does not matter: any body can be imagined as
built from small cubes, each expanding this way, so the result holds equally for a sphere,
a rod or an irregular casting.
:::

::: tip The examiner is looking for
1. "Each side becomes $l(1+\alpha\Delta\theta)$" — stated, not assumed silently.
2. The binomial expansion written out in full.
3. An explicit sentence saying *why* the $\alpha^{2}$ term is dropped (because
   $\alpha \approx 10^{-5}$), not just a quiet disappearance.
4. The comparison with the defining equation for $\beta$ or $\gamma$.
5. The assumption that expansion is the same in all directions.
:::

::: caution A hole expands, it does not close up
Students often expect a hole in a heated metal plate to get smaller. It does
not. Imagine the disc of metal that was cut out to make the hole: on heating,
that disc would grow by $\gamma\Delta\theta$ per unit volume, and the hole must
grow with it so that the disc would still fit. **A cavity expands exactly as if
it were filled with the material of the body.** This is why a tight metal lid
loosens when held under hot water.
:::

::: example Worked example 10.3
**Problem.** A brass plate has a circular hole of diameter $5.000\ \text{cm}$ at
$20\ ^{\circ}\text{C}$. Find the diameter of the hole and the area of the hole at
$220\ ^{\circ}\text{C}$. Take $\alpha_{\text{brass}} = 1.9\times10^{-5}\ \text{K}^{-1}$.

**Solution.** The hole expands like the metal, with $\Delta\theta = 200\ \text{K}$.

$$ d_2 = d_1(1+\alpha\Delta\theta) = 5.000\left(1 + 1.9\times10^{-5}\times200\right)
= 5.000(1+3.8\times10^{-3}) = 5.019\ \text{cm} $$

Original area $A_1 = \pi d_1^{2}/4 = \pi(5.000)^{2}/4 = 19.635\ \text{cm}^{2}$.
Using $\beta = 2\alpha = 3.8\times10^{-5}\ \text{K}^{-1}$,

$$ A_2 = A_1(1+\beta\Delta\theta) = 19.635\left(1+3.8\times10^{-5}\times200\right)
= 19.635\times1.0076 = 19.784\ \text{cm}^{2} $$
:::

## 10.3 Liquid Expansion: Absolute and apparent

A liquid has no shape of its own, so only its **volume** expansion is defined —
there is no $\alpha$ or $\beta$ for a liquid. But a liquid must be held in a
vessel, and when the vessel is heated it expands too. The level in the vessel
therefore rises by *less* than the liquid's true expansion. Two coefficients are
needed.

::: definition Real and apparent expansivity
**Real (absolute) expansivity** $\gamma_r$ is the true increase in volume of the
liquid per unit volume per unit rise in temperature.

**Apparent expansivity** $\gamma_a$ is the *observed* increase in volume per unit
volume per unit rise in temperature, measured relative to the vessel.
:::

::: derivation Real, apparent and vessel expansivity: $\gamma_r = \gamma_a + \gamma_g$
We start from the fact that the vessel expands too, and reach the correction that must be
added to every measured value.

**Setting up.** A vessel of volume $V$ is filled to the brim with liquid at temperature
$\theta_1$. Both are heated to $\theta_2$, a rise of $\Delta\theta$. Let $\gamma_r$ be the
real expansivity of the liquid and $\gamma_g$ the cubical expansivity of the vessel's
material.

**Step 1 — the true new volume of the liquid.** By the definition of $\gamma_r$:

$$ V_{liquid} = V(1 + \gamma_r\Delta\theta) $$

**Step 2 — the new volume of the vessel.** The vessel is made of a solid, and its inside
volume expands by its own cubical expansivity:

$$ V_{vessel} = V(1 + \gamma_g\Delta\theta) $$

**Step 3 — only the difference can escape.** The liquid that will not fit inside the
enlarged vessel spills out over the top:

$$ \text{overflow} = V_{liquid} - V_{vessel}
= V(1 + \gamma_r\Delta\theta) - V(1 + \gamma_g\Delta\theta) $$

**Step 4 — take out the common factor $V$ and remove the brackets.** The two $1$'s cancel:

$$ \text{overflow} = V\left(\gamma_r\Delta\theta - \gamma_g\Delta\theta\right) $$

**Step 5 — take out $\Delta\theta$ as well:**

$$ \text{overflow} = V(\gamma_r - \gamma_g)\Delta\theta $$

**Step 6 — say what we actually observe.** All an experimenter sees is the spilt liquid,
and that overflow is exactly what the *apparent* expansivity is defined by:

$$ \text{overflow} = V\gamma_a\Delta\theta $$

**Step 7 — set Step 5 equal to Step 6.** Both describe the same spilt liquid:

$$ V\gamma_a\Delta\theta = V(\gamma_r - \gamma_g)\Delta\theta $$

**Step 8 — cancel $V$ and $\Delta\theta$,** which appear on both sides:

$$ \gamma_a = \gamma_r - \gamma_g $$

**Step 9 — rearrange for the real expansivity:**

$$ \gamma_r = \gamma_a + \gamma_g $$

**Step 10 — express the vessel's part through $\alpha$,** since tables list the linear
expansivity $\alpha_g$ of glass, and $\gamma = 3\alpha$:

$$ \gamma_r = \gamma_a + 3\alpha_g $$

**Result.**

$$ \gamma_r = \gamma_a + \gamma_g = \gamma_a + 3\alpha_g $$

**What it means.** The measured (apparent) expansion is always *smaller* than the real
one, because the container quietly makes room for part of the liquid's growth. So the
correction is always an **addition**. If the vessel could somehow not expand
($\gamma_g = 0$), apparent and real expansion would be the same.

**Conditions used.** The vessel is full to the brim at the start, nothing evaporates, and
the liquid and vessel reach the same temperature.
:::

In the **weight-thermometer** (specific-gravity bottle) method the bulb is filled
with liquid of mass $M$ at $\theta_1$, heated to $\theta_2$, and the mass $m$
expelled is weighed. Since apparent expansion is measured by the liquid that
leaves,

$$ \gamma_a = \frac{m}{(M-m)\,\Delta\theta} $$

where $M-m$ is the mass still filling the bulb at the higher temperature. Adding
$3\alpha_g$ for the glass then gives the real expansivity.

| Liquid | $\gamma_r$ (K⁻¹) |
|---|---|
| Mercury | $1.8\times10^{-4}$ |
| Water (near 20 °C) | $2.1\times10^{-4}$ |
| Glycerine | $5.3\times10^{-4}$ |
| Ethanol | $1.1\times10^{-3}$ |

Because $\gamma_{\text{glass}} = 3\times(9\times10^{-6}) = 2.7\times10^{-5}\ \text{K}^{-1}$
is small compared with these, the apparent expansivity is usually only a little
less than the real one — but the difference is easily measurable and must never
be ignored in a calculation.

```figure caption="Anomalous expansion of water. Between $0\ ^\circ$C and $4\ ^\circ$C water contracts on heating, so its density is greatest at $4\ ^\circ$C."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
T = np.array([0,1,2,3,4,5,6,7,8,9,10])
rho = np.array([999.840,999.899,999.940,999.964,999.972,999.964,
                999.940,999.901,999.848,999.781,999.699])
ax.plot(T, rho, color=ACCENT, lw=2.0, marker='o', ms=3.4)
ax.plot([4],[999.972],'o',color=SERIES[1],ms=6,zorder=4)
ax.annotate('maximum density\nat $4\\ ^\\circ$C', (4,999.972),
            xytext=(0.9,999.760), ha='left', va='center',
            fontsize=8.6, color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0,
                            mutation_scale=10, shrinkB=4))
ax.set_xlabel(r'temperature  ($^\circ$C)')
ax.set_ylabel(r'density  (kg m$^{-3}$)')
ax.set_xlim(-0.4,10.4); ax.set_ylim(999.66,1000.00)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
```

Water is the famous exception. From $0\ ^{\circ}$C to $4\ ^{\circ}$C it
*contracts* on heating, and only above $4\ ^{\circ}$C does it expand normally.
Its density is therefore a maximum at $4\ ^{\circ}$C. This **anomalous
expansion** is why ice floats, and why a lake such as Rara freezes from the
surface downwards in winter, leaving water at $4\ ^{\circ}$C at the bottom in
which fish survive.

::: example Worked example 10.4
**Problem.** A glass flask of volume $1000\ \text{cm}^{3}$ is filled completely
with mercury at $0\ ^{\circ}\text{C}$ and heated to $100\ ^{\circ}\text{C}$. Given
$\gamma_{\text{Hg}} = 1.8\times10^{-4}\ \text{K}^{-1}$ and
$\alpha_{\text{glass}} = 9\times10^{-6}\ \text{K}^{-1}$, find the volume of
mercury that overflows.

**Solution.** Cubical expansivity of glass:

$$ \gamma_g = 3\alpha_g = 3\times9\times10^{-6} = 2.7\times10^{-5}\ \text{K}^{-1} $$

$$ \gamma_a = \gamma_r - \gamma_g = 1.8\times10^{-4} - 0.27\times10^{-4}
= 1.53\times10^{-4}\ \text{K}^{-1} $$

$$ \text{overflow} = V\gamma_a\Delta\theta = 1000\times1.53\times10^{-4}\times100
= 15.3\ \text{cm}^{3} $$

Had we forgotten the flask, we would have said $18.0\ \text{cm}^{3}$ — an error
of almost $18\ \%$.
:::

## 10.4 Dulong and Petit method of determining expansivity of liquid

Every method that uses a vessel gives the *apparent* expansivity first, and the
real value only after the vessel's own expansion is known. Dulong and Petit
(1817) found a way to measure the **real** expansivity directly, using the fact
that pressure, not volume, is what balances in a connected liquid.

```figure caption="Dulong and Petit's apparatus. The two limbs of liquid balance at the base, so $h_0\rho_0 = h_\theta\rho_\theta$ and the expansion of the glass never enters the result."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,3.0))
h0, ht = 3.00, 3.45
def limb(x, h):
    ax.add_patch(Rectangle((x-0.20,0.30), 0.40, h, fill=False, ec=INK, lw=1.3))
    ax.add_patch(Rectangle((x-0.18,0.32), 0.36, h-0.02, facecolor=SERIES[1],
                           alpha=0.75, ec='none'))
ax.add_patch(Rectangle((1.4,0.10),4.2,0.40, fill=False, ec=INK, lw=1.3))
ax.add_patch(Rectangle((1.42,0.12),4.16,0.36, facecolor=SERIES[1], alpha=0.75, ec='none'))
limb(1.6, h0); limb(5.4, ht)
ax.add_patch(Rectangle((0.95,0.55),1.30,h0-0.20, fill=False, ec=ACCENT, lw=1.1, ls='--'))
ax.add_patch(Rectangle((4.75,0.55),1.30,ht-0.20, fill=False, ec=SERIES[1], lw=1.1, ls='--'))
ax.text(1.60,h0+0.55,'melting ice\n$0\\ ^\\circ$C', ha='center', fontsize=8.4, color=ACCENT)
ax.text(5.40,ht+0.55,'steam\n$\\theta\\ ^\\circ$C', ha='center', fontsize=8.4, color=SERIES[1])
for x, h, lab, c in [(0.72, h0, '$h_0$', ACCENT), (6.30, ht, r'$h_\theta$', SERIES[1])]:
    ax.annotate('', xy=(x,0.30+h), xytext=(x,0.30),
                arrowprops=dict(arrowstyle='<|-|>', color=c, lw=1.1, mutation_scale=9))
    ax.text(x-0.12 if x < 3 else x+0.12, 0.30+h/2, lab,
            ha='right' if x < 3 else 'left', fontsize=9.5, color=c)
ax.plot([0.9,6.2],[0.30,0.30], color=MUTED, lw=0.9, ls=':')
ax.text(3.50,-0.32,'common base level', ha='center', fontsize=8.2, color=MUTED)
ax.set_xlim(0.2,7.2); ax.set_ylim(-0.65,5.0)
ax.set_aspect('equal'); ax.axis('off')
```

**Apparatus.** The liquid fills a U-shaped glass tube whose two vertical limbs
are joined by a narrow horizontal tube at the bottom. One limb is surrounded by a
jacket of melting ice at $0\ ^{\circ}\text{C}$; the other is surrounded by a
steam jacket at $\theta\ ^{\circ}\text{C}$. The heights of the two columns above
the common horizontal base are measured with a travelling microscope, so nothing
touches the liquid.

::: derivation The Dulong and Petit formula, $\gamma = \dfrac{h_\theta - h_0}{h_0\theta}$
We start from the balance of pressures in the two columns and reach a formula for the real
expansivity in terms of two measured heights.

**Setting up.** The two vertical columns of the same liquid are joined at the bottom by a
horizontal tube. One column is kept at $0\ ^{\circ}$C and stands at height $h_0$; the
other is kept at $\theta\ ^{\circ}$C and stands at height $h_\theta$. Let $\rho_0$ and
$\rho_\theta$ be the densities at those two temperatures.

**Step 1 — the liquid is at rest.** Nothing flows through the horizontal tube, so the two
columns must push on it equally hard. Pressure of a column of height $h$ and density
$\rho$ is $h\rho g$:

$$ h_0\rho_0 g = h_\theta\rho_\theta g $$

**Step 2 — cancel $g$,** which is the same on both sides:

$$ h_0\rho_0 = h_\theta\rho_\theta $$

**Step 3 — now find $\rho_\theta$.** Take a fixed mass $M$ of the liquid. At
$0\ ^{\circ}$C it occupies $V_0$, so

$$ \rho_0 = \frac{M}{V_0} $$

**Step 4 — the same mass at $\theta$ occupies a bigger volume.** By the definition of
cubical expansivity, the volume becomes $V_0(1 + \gamma\theta)$:

$$ \rho_\theta = \frac{M}{V_0(1 + \gamma\theta)} $$

**Step 5 — replace $M/V_0$ by $\rho_0$** using Step 3. This is the "density falls because
the same mass spreads out" step:

$$ \rho_\theta = \frac{\rho_0}{1 + \gamma\theta} $$

**Step 6 — substitute this into Step 2:**

$$ h_0\rho_0 = h_\theta \cdot \frac{\rho_0}{1 + \gamma\theta} $$

**Step 7 — cancel $\rho_0$ from both sides:**

$$ h_0 = \frac{h_\theta}{1 + \gamma\theta} $$

**Step 8 — multiply both sides by $(1 + \gamma\theta)$:**

$$ h_0(1 + \gamma\theta) = h_\theta $$

**Step 9 — expand the left side:**

$$ h_0 + h_0\gamma\theta = h_\theta $$

**Step 10 — move $h_0$ across:**

$$ h_0\gamma\theta = h_\theta - h_0 $$

**Step 11 — divide both sides by $h_0\theta$:**

$$ \gamma = \frac{h_\theta - h_0}{h_0\,\theta} $$

**Result.**

$$ \boxed{\gamma = \frac{h_\theta - h_0}{h_0\,\theta}} $$

**What it means.** Only two heights and one temperature are needed — no masses, no
volumes, no weighing. The hot column stands *taller* because the same mass has become less
dense and so needs more height to produce the same pressure.

**Conditions used.** The liquid is in equilibrium (not flowing), the two columns are at
steady, uniform temperatures, and the heights are measured from the level of the
horizontal joining tube.
:::

::: tip The examiner is looking for
1. The pressure-balance equation $h_0\rho_0 g = h_\theta\rho_\theta g$ with a reason.
2. $\rho_\theta = \rho_0/(1+\gamma\theta)$, derived from a **fixed mass**.
3. The substitution and the cancellation of $\rho_0$.
4. The final rearrangement to $\gamma = (h_\theta - h_0)/h_0\theta$.
5. The explanation of why **no vessel correction** is needed.
:::

::: key Why this gives the *real* expansivity
The result contains only heights, temperatures and the liquid's own densities.
The glass tube does expand, but its expansion changes neither the density of the
liquid nor the measured heights, which are read from outside with a microscope
against a fixed scale. So Dulong and Petit's method needs no correction for the
vessel and gives $\gamma_r$ directly — its great advantage over the
weight-thermometer method.
:::

::: example Worked example 10.5
**Problem.** In a Dulong and Petit experiment the cold column of mercury stands
$75.00\ \text{cm}$ high at $0\ ^{\circ}\text{C}$ while the hot column stands
$76.35\ \text{cm}$ high at $100\ ^{\circ}\text{C}$. Find the real expansivity of
mercury. If the tube is glass with
$\alpha = 9\times10^{-6}\ \text{K}^{-1}$, what apparent expansivity would a
glass-vessel experiment have given?

**Solution.**

$$ \gamma_r = \frac{h_\theta - h_0}{h_0\theta} = \frac{76.35 - 75.00}{75.00\times100}
= \frac{1.35}{7500} = 1.8\times10^{-4}\ \text{K}^{-1} $$

For glass, $\gamma_g = 3\alpha = 2.7\times10^{-5}\ \text{K}^{-1}$, so

$$ \gamma_a = \gamma_r - \gamma_g = 1.8\times10^{-4} - 0.27\times10^{-4}
= 1.53\times10^{-4}\ \text{K}^{-1} $$
:::

## Chapter summary

- Linear expansivity $\alpha = \dfrac{l_2-l_1}{l_1\Delta\theta}$, so
  $l_2 = l_1(1+\alpha\Delta\theta)$; unit K⁻¹.
- Pullinger's apparatus measures $\alpha$: rod in a steam jacket, expansion read
  on a micrometer screw that completes a bell circuit;
  $\alpha = \delta l / (l_1\Delta\theta)$.
- $A_2 = A_1(1+\beta\Delta\theta)$ and $V_2 = V_1(1+\gamma\Delta\theta)$, with
  $\beta = 2\alpha$, $\gamma = 3\alpha$ and $\alpha:\beta:\gamma = 1:2:3$.
- A cavity or hole expands exactly as if it were filled with the surrounding
  material.
- A liquid has two expansivities: real $\gamma_r$ and apparent $\gamma_a$, with
  $\gamma_r = \gamma_a + \gamma_g$ where $\gamma_g = 3\alpha_g$ for the vessel.
  By the weight thermometer, $\gamma_a = m/[(M-m)\Delta\theta]$.
- Water expands anomalously: it contracts from $0$ to $4\ ^{\circ}$C and has
  maximum density at $4\ ^{\circ}$C.
- Dulong and Petit: balancing columns give $h_\theta = h_0(1+\gamma\theta)$, so
  $\gamma_r = (h_\theta-h_0)/(h_0\theta)$, with no correction for the vessel.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. For an isotropic solid the ratio $\alpha : \beta : \gamma$ is <span class="marks">[1]</span>
   (a) $1:2:3$ (b) $3:2:1$ (c) $1:3:2$ (d) $2:3:1$
2. When a metal plate with a hole in it is heated, the hole <span class="marks">[1]</span>
   (a) gets smaller (b) gets larger (c) stays the same (d) first shrinks, then grows
3. The SI unit of the coefficient of linear expansion is <span class="marks">[1]</span>
   (a) m (b) K⁻¹ (c) m K⁻¹ (d) it has no unit
4. The real expansivity of a liquid equals its apparent expansivity plus the <span class="marks">[1]</span>
   (a) linear expansivity of the vessel (b) cubical expansivity of the vessel
   (c) superficial expansivity of the vessel (d) nothing
5. Dulong and Petit's method directly determines the <span class="marks">[1]</span>
   (a) apparent expansivity (b) real expansivity (c) linear expansivity (d) superficial expansivity

::: note Answers to Group A
**1.** (a) — from $(1+\alpha\Delta\theta)^n$ for $n = 1,2,3$.
**2.** (b) — a cavity expands like the material that would fill it.
**3.** (b) — it is a fractional length change per kelvin, so only K⁻¹ is left.
**4.** (b) — $\gamma_r = \gamma_a + \gamma_g$, where $\gamma_g = 3\alpha_g$.
**5.** (b) — it balances pressures, so the vessel's expansion cancels out.
:::

**Group B — Short answer (5 marks each)**

1. Define the coefficient of linear expansion and show that $\gamma = 3\alpha$
   for an isotropic solid. <span class="marks">[5]</span>
2. With a labelled diagram, describe how the linear expansivity of a metal rod is
   determined using Pullinger's apparatus. <span class="marks">[5]</span>
3. Distinguish between the real and apparent expansivity of a liquid and show
   that $\gamma_r = \gamma_a + \gamma_g$. <span class="marks">[5]</span>
4. A glass flask of volume $500\ \text{cm}^{3}$ is completely filled with mercury
   at $0\ ^{\circ}\text{C}$. On heating to $80\ ^{\circ}\text{C}$,
   $6.0\ \text{cm}^{3}$ of mercury overflows. If
   $\gamma_{\text{Hg}} = 1.8\times10^{-4}\ \text{K}^{-1}$, find the coefficient
   of linear expansion of the glass. <span class="marks">[5]</span>
5. A brass scale is correct at $15\ ^{\circ}\text{C}$. It is used at
   $35\ ^{\circ}\text{C}$ and reads a length of $50.00\ \text{cm}$. What is the
   true length? Take $\alpha_{\text{brass}} = 1.9\times10^{-5}\ \text{K}^{-1}$.
   <span class="marks">[5]</span>

::: note Answers to Group B
**4.** $\gamma_a = \dfrac{6.0}{500\times80} = 1.5\times10^{-4}\ \text{K}^{-1}$.
Then $\gamma_g = \gamma_r - \gamma_a = 1.8\times10^{-4} - 1.5\times10^{-4}
= 3.0\times10^{-5}\ \text{K}^{-1}$, so
$\alpha_g = \gamma_g/3 = 1.0\times10^{-5}\ \text{K}^{-1}$.

**5.** At $35\ ^{\circ}$C each scale division has grown, so every division now
measures more than it claims. True length
$= 50.00\left(1 + 1.9\times10^{-5}\times20\right) = 50.00(1+3.8\times10^{-4})
= 50.019\ \text{cm}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the relations $\beta = 2\alpha$ and $\gamma = 3\alpha$, stating
   clearly the approximation used. <span class="marks">[4]</span>
   (b) Describe Dulong and Petit's method for the absolute expansivity of a
   liquid and derive $\gamma = \dfrac{h_\theta - h_0}{h_0\theta}$. Explain why no
   correction for the expansion of the glass is needed.
   <span class="marks">[4]</span>
2. (a) An iron rim of diameter $79.80\ \text{cm}$ at $20\ ^{\circ}\text{C}$ is to
   be fitted on a wooden cart wheel of diameter $80.00\ \text{cm}$. To what
   temperature must the rim be heated? Take
   $\alpha_{\text{iron}} = 1.2\times10^{-5}\ \text{K}^{-1}$.
   <span class="marks">[4]</span>
   (b) In a Dulong and Petit experiment on a liquid, the column at
   $0\ ^{\circ}\text{C}$ is $60.00\ \text{cm}$ high and the column at
   $100\ ^{\circ}\text{C}$ is $61.20\ \text{cm}$ high. Find the real expansivity
   of the liquid, and its apparent expansivity when it is kept in a glass vessel
   with $\alpha = 9\times10^{-6}\ \text{K}^{-1}$. <span class="marks">[4]</span>

::: note Answers to Group C
**2.** (a) The rim must expand from $79.80$ to $80.00\ \text{cm}$, so
$\Delta d = 0.20\ \text{cm}$ and

$$ \Delta\theta = \frac{\Delta d}{d_1\alpha}
= \frac{0.20}{79.80\times1.2\times10^{-5}} = 208.9\ \text{K} $$

The rim must be heated to $20 + 208.9 \approx 229\ ^{\circ}\text{C}$. On cooling
it grips the wheel tightly — the standard way a wheelwright fits a tyre.

(b) $\gamma_r = \dfrac{61.20-60.00}{60.00\times100} = \dfrac{1.20}{6000}
= 2.0\times10^{-4}\ \text{K}^{-1}$.

$\gamma_g = 3\times9\times10^{-6} = 2.7\times10^{-5}\ \text{K}^{-1}$, so
$\gamma_a = 2.0\times10^{-4} - 0.27\times10^{-4} = 1.73\times10^{-4}\ \text{K}^{-1}$.
:::

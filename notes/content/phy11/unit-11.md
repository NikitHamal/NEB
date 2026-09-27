---
subject: Physics
grade: 11
unit: 11
title: Quantity of Heat
hours: 6
area: Heat and Thermodynamics
---

Heat is energy that flows from a hotter body to a colder one because of the
temperature difference between them. This unit is about *counting* that energy:
how much heat a body must absorb to warm up, how much more it needs to melt or
boil, and how quickly a hot body loses heat to the air around it. The unit of
every quantity here is the joule, and almost every numerical problem is solved
with one sentence — **heat lost by the hot bodies equals heat gained by the cold
bodies**, provided nothing leaks to the surroundings.

::: key The three equations this unit is built on
Warming without a phase change: $Q = mc\,\Delta\theta$.
Phase change at constant temperature: $Q = mL$.
Heat capacity of a body: $C = mc$, measured in J K⁻¹.

The **water equivalent** $W$ of a calorimeter is the mass of water that would
need the same heat for the same temperature rise: $W = mc/c_w$. Adding the
calorimeter's water equivalent to the water already inside turns a two-body
problem into a one-body problem.
:::

## 11.1 Newton's law of cooling

Leave a cup of tea on the table in Kathmandu in winter and it cools fast at
first, then more and more slowly, finally settling at room temperature. Newton
described this behaviour in a law that works well for moderate temperature
differences.

::: definition Newton's law of cooling
The rate at which a body loses heat is directly proportional to the excess of
its temperature over that of its surroundings, provided the excess is small and
the physical conditions (surface area, nature of surface, movement of the
surrounding air) remain unchanged.
:::

If the body is at $\theta$ and the surroundings at $\theta_0$,

$$ \frac{dQ}{dt} = -K(\theta - \theta_0) $$

where $K$ depends on the surface area and on the nature of the surface. Since
$Q = mc\theta$ for a body of mass $m$ and specific heat capacity $c$, we may
write $dQ/dt = mc\,(d\theta/dt)$, so

$$ \frac{d\theta}{dt} = -k(\theta - \theta_0), \qquad k = \frac{K}{mc} $$

The **rate of fall of temperature** is therefore also proportional to the excess
temperature. Note carefully that $dQ/dt$ and $d\theta/dt$ are different things:
the first is a power in watts, the second a cooling rate in K s⁻¹.

::: derivation A cooling body falls in temperature exponentially
We start from Newton's law of cooling written as a rate equation, and reach a formula that
gives the temperature at any later time.

**Setting up.** Let $\theta$ be the body's temperature at time $t$, $\theta_0$ the
temperature of the surroundings, and $\theta_1$ the body's temperature at $t = 0$. Newton's
law says the rate of cooling is proportional to the excess temperature:

$$ \frac{d\theta}{dt} = -k(\theta - \theta_0) $$

The minus sign is there because $\theta$ is *falling*, so $d\theta/dt$ is negative while
$k$ and the excess temperature are both positive.

**Step 1 — separate the variables.** We want all the $\theta$'s on one side and all the
$t$'s on the other, so divide both sides by $(\theta - \theta_0)$ and multiply by $dt$:

$$ \frac{d\theta}{\theta - \theta_0} = -k\,dt $$

**Step 2 — integrate both sides.** The left side is of the standard form
$\int \frac{dx}{x} = \ln x$, with $x = \theta - \theta_0$ (note $\theta_0$ is a constant,
so $d(\theta-\theta_0) = d\theta$):

$$ \ln(\theta - \theta_0) = -kt + C $$

**Step 3 — find the constant $C$ from the starting condition.** At $t = 0$ the temperature
is $\theta_1$:

$$ \ln(\theta_1 - \theta_0) = -k(0) + C = C $$

**Step 4 — put this value of $C$ back:**

$$ \ln(\theta - \theta_0) = -kt + \ln(\theta_1 - \theta_0) $$

**Step 5 — collect the two logarithms on the left:**

$$ \ln(\theta - \theta_0) - \ln(\theta_1 - \theta_0) = -kt $$

**Step 6 — combine them into one,** using $\ln A - \ln B = \ln(A/B)$:

$$ \ln\frac{\theta - \theta_0}{\theta_1 - \theta_0} = -kt $$

**Step 7 — undo the logarithm** by taking $e$ to the power of each side:

$$ \frac{\theta - \theta_0}{\theta_1 - \theta_0} = e^{-kt} $$

**Step 8 — multiply both sides by $(\theta_1 - \theta_0)$:**

$$ \theta - \theta_0 = (\theta_1 - \theta_0)e^{-kt} $$

**Step 9 — add $\theta_0$ to both sides:**

$$ \theta = \theta_0 + (\theta_1 - \theta_0)e^{-kt} $$

**Result.**

$$ \theta = \theta_0 + (\theta_1 - \theta_0)e^{-kt} $$

**What it means.** The *excess* temperature $(\theta - \theta_0)$ dies away
**exponentially**, halving in equal intervals of time. The body never quite reaches
$\theta_0$ in theory — it only gets closer and closer, which is why cooling looks fast at
first and very slow at the end. Step 6 also gives the experimental test: a graph of
$\ln(\theta - \theta_0)$ against $t$ is a **straight line of slope $-k$**.

**Conditions used.** The excess temperature must be small (roughly under
$30\ ^{\circ}\text{C}$), cooling must be by natural convection in a draught-free room, and
the surroundings must stay at a steady $\theta_0$.
:::

::: tip The examiner is looking for
1. Newton's law written as $d\theta/dt = -k(\theta - \theta_0)$, with the minus sign
   explained.
2. The separation of variables.
3. The integration giving a logarithm, **with a constant of integration**.
4. Using $t = 0$, $\theta = \theta_1$ to evaluate that constant.
5. Taking exponentials to reach $\theta = \theta_0 + (\theta_1-\theta_0)e^{-kt}$.
6. The remark that $\ln(\theta-\theta_0)$ against $t$ is a straight line of slope $-k$.
:::

```figure caption="Left: a body at $80^\circ$C cooling in surroundings at $20^\circ$C. Right: the same data plotted as $\ln(\theta-\theta_0)$ against $t$ gives a straight line of slope $-k$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.5))
t = np.linspace(0, 40, 300)
th0, th1, k = 20.0, 80.0, 0.055
th = th0 + (th1-th0)*np.exp(-k*t)
a = axes[0]
a.plot(t, th, color=ACCENT, lw=1.9)
a.axhline(th0, color=MUTED, lw=1.0, ls='--')
a.annotate('surroundings  $\\theta_0$', (39, th0), textcoords='offset points',
           xytext=(0, -7), ha='right', va='top', color=MUTED, fontsize=8.2)
a.set_xlabel('time  $t$  (min)'); a.set_ylabel('temperature  ($^\\circ$C)')
a.set_xlim(0, 40); a.set_ylim(0, 90)
a.spines[['top','right']].set_visible(False); a.grid(True, alpha=.5)
b = axes[1]
b.plot(t, np.log(th-th0), color='#d9534f', lw=1.9)
b.set_xlabel('time  $t$  (min)'); b.set_ylabel('$\\ln(\\theta-\\theta_0)$')
b.set_xlim(0, 40)
b.spines[['top','right']].set_visible(False); b.grid(True, alpha=.5)
fig.tight_layout()
```

For examination work the differential form is usually replaced by an
**average form**. If a body cools from $\theta_1$ to $\theta_2$ in time $t$, and
the fall is not too large, we may take the mean temperature during the interval
as $(\theta_1+\theta_2)/2$:

$$ \frac{\theta_1 - \theta_2}{t} = k\left(\frac{\theta_1+\theta_2}{2} - \theta_0\right) $$

::: example Worked example 11.1
**Problem.** A body cools from $60\ ^\circ$C to $50\ ^\circ$C in 10 minutes. The
temperature of the surroundings is $25\ ^\circ$C. What will its temperature be
after the next 10 minutes?

**Solution.** Using the average form for the first interval,

$$ \frac{60-50}{10} = k\left(\frac{60+50}{2} - 25\right) = k(55-25) = 30k $$

so $1 = 30k$, giving $k = 1/30$ per minute.

For the second interval, let the final temperature be $\theta$:

$$ \frac{50-\theta}{10} = \frac{1}{30}\left(\frac{50+\theta}{2} - 25\right) $$

Multiplying through by 30: $3(50-\theta) = \frac{50+\theta}{2} - 25$, i.e.
$150 - 3\theta = \theta/2$. Hence $150 = 3.5\theta$ and

$$ \theta = \frac{150}{3.5} = 42.9\ ^\circ\text{C} $$

The body fell $10\ ^\circ$C in the first ten minutes but only about
$7.1\ ^\circ$C in the second — cooling slows as the excess temperature drops.
:::

::: caution Newton's law is not universal
The law holds only for a **small** excess temperature (in practice up to about
$30\ ^\circ$C) and for a body losing heat mainly by convection in a draught or
by forced air flow. For a red-hot body radiation dominates, the loss goes as
$T^4$ (Unit 12), and Newton's law fails badly.
:::

## 11.2 Measurement of specific heat capacity of solids and liquids

::: definition Specific heat capacity
The specific heat capacity $c$ of a substance is the heat required to raise the
temperature of **unit mass** of it by **one kelvin**:
$c = Q/(m\,\Delta\theta)$, in J kg⁻¹ K⁻¹.
:::

Water has an unusually large specific heat capacity,
$c_w = 4200\ \text{J kg}^{-1}\text{K}^{-1}$, which is why lakes such as Phewa
Tal change temperature far more slowly than the land around them.

| Substance | $c$ / J kg⁻¹ K⁻¹ | Substance | $c$ / J kg⁻¹ K⁻¹ |
|---|---|---|---|
| Water | 4200 | Copper | 400 |
| Ice | 2100 | Aluminium | 900 |
| Steam | 2010 | Iron | 470 |
| Kerosene | 2100 | Brass | 380 |

### Method of mixtures (for a solid)

A known mass $m_s$ of the solid is heated in a steam jacket to a steady
temperature $\theta_s$ and then dropped quickly into water of mass $m_w$ in a
calorimeter of mass $m_c$ and specific heat capacity $c_c$, initially at
$\theta_1$. The mixture is stirred and the highest steady temperature
$\theta_2$ is recorded. Then

$$ m_s c_s (\theta_s - \theta_2) = (m_w c_w + m_c c_c)(\theta_2 - \theta_1) $$

$$ c_s = \frac{(m_w c_w + m_c c_c)(\theta_2-\theta_1)}{m_s(\theta_s-\theta_2)} $$

```figure caption="Calorimeter for the method of mixtures. Lagging and the polished outer vessel cut down heat exchange with the room."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.4, 3.2))
# outer vessel
ax.add_patch(Rectangle((0.6, 0.4), 5.6, 3.4, fill=False, ec=INK, lw=1.4))
# lagging
ax.add_patch(Rectangle((0.6, 0.4), 5.6, 3.4, facecolor='#efe6d5', ec='none', zorder=0))
# calorimeter
ax.add_patch(Rectangle((1.7, 0.95), 3.4, 2.5, facecolor='#f6d9b0', ec=INK, lw=1.5, zorder=2))
# water
ax.add_patch(Rectangle((1.78, 1.02), 3.24, 1.75, facecolor='#bcd9ef', ec='none', zorder=3))
# specimen
ax.add_patch(Rectangle((2.9, 1.08), 0.75, 0.5, facecolor=MUTED, ec=INK, lw=1.0, zorder=4))
# thermometer
ax.plot([2.3, 2.3], [1.3, 4.35], color=INK, lw=1.6, zorder=5)
ax.plot([2.3], [1.3], marker='o', color='#d9534f', ms=5, zorder=6)
# stirrer
ax.plot([4.4, 4.4], [1.35, 4.15], color=INK, lw=1.3, zorder=5)
ax.plot([4.1, 4.7], [1.35, 1.35], color=INK, lw=1.3, zorder=5)
ax.annotate('thermometer', (2.3, 4.5), textcoords='offset points', xytext=(-30, 2),
            fontsize=8.4, color=INK, ha='right', zorder=7)
ax.annotate('stirrer', (4.4, 4.3), textcoords='offset points', xytext=(4, 0),
            fontsize=8.4, color=INK, ha='left', zorder=7)
ax.text(3.40, 2.20, 'water', ha='center', va='center', fontsize=8.4,
        color=INK, zorder=7)
# the three parts of the vessel are called out from the clear space on the right
lead = dict(arrowstyle='-', color=INK, lw=0.8, shrinkA=2, shrinkB=1)
ax.annotate('lid', xy=(5.60, 3.80), xytext=(6.45, 4.05), ha='left', va='center',
            fontsize=8.4, color=INK, zorder=7, arrowprops=lead)
ax.annotate('calorimeter', xy=(5.10, 2.95), xytext=(6.45, 2.95), ha='left',
            va='center', fontsize=8.4, color=INK, zorder=7, arrowprops=lead)
ax.annotate('lagging', xy=(5.65, 1.95), xytext=(6.45, 1.95), ha='left',
            va='center', fontsize=8.4, color=INK, zorder=7, arrowprops=lead)
ax.annotate('hot specimen', xy=(3.30, 1.08), xytext=(3.40, 0.62), ha='center',
            va='center', fontsize=8.4, color=INK, zorder=7, arrowprops=lead)
ax.set_xlim(0.1, 8.3); ax.set_ylim(0.1, 4.9); ax.axis('off')
```
### Method of mixtures (for a liquid)

The same equation is used the other way round. A solid of *known* specific heat
capacity is heated and dropped into the unknown liquid; $c_s$ is now known and
$c_{\text{liquid}}$ is the unknown. The liquid must not attack the calorimeter
and must not boil.

### Electrical method

For a liquid it is often easier to supply a measured amount of electrical
energy. A heating coil carrying current $I$ at potential difference $V$ for
time $t$ delivers $Q = VIt$ joules, so

$$ VIt = (m_l c_l + m_c c_c)(\theta_2 - \theta_1) $$

The advantage is that the heat supplied is known directly from electrical
measurements; the disadvantage is that heat losses over a long run can be large,
so a **cooling correction** based on Newton's law of cooling is applied.

::: example Worked example 11.2
**Problem.** A copper calorimeter of mass 150 g contains 200 g of water at
$20\ ^\circ$C. A metal block of mass 100 g at $100\ ^\circ$C is dropped in and the
final steady temperature is $25\ ^\circ$C. Find the specific heat capacity of the
metal. Take $c_w = 4200$ and $c_{Cu} = 400\ \text{J kg}^{-1}\text{K}^{-1}$.

**Solution.** Heat gained by water and calorimeter:

$$ Q = (0.200\times4200 + 0.150\times400)(25-20) = (840+60)\times 5 = 4500\ \text{J} $$

Heat lost by the metal block:

$$ Q = 0.100 \times c \times (100-25) = 7.5\,c $$

Equating, $7.5\,c = 4500$, so

$$ c = 600\ \text{J kg}^{-1}\text{K}^{-1} $$
:::

## 11.3 Change of phases: Latent heat

Supply heat steadily to a block of ice taken from a deep freeze and record the
temperature. The graph is not a straight line: it has two flat steps.

```figure caption="Heating curve for 1 kg of water substance from $-20^\circ$C ice to $120^\circ$C steam. The temperature stands still while a phase change is in progress."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ci, cw, cs = 2100.0, 4200.0, 2010.0
Lf, Lv = 3.34e5, 2.26e6
q1 = ci*20; q2 = q1+Lf; q3 = q2+cw*100; q4 = q3+Lv; q5 = q4+cs*20
Q = [0, q1, q2, q3, q4, q5]
T = [-20, 0, 0, 100, 100, 120]
Qk = [q/1000 for q in Q]
ax.plot(Qk, T, color=ACCENT, lw=2.1)
bands = [(Qk[0], Qk[1], 'ice', '#6a5acd'), (Qk[1], Qk[2], 'melting', '#2e8b57'),
         (Qk[2], Qk[3], 'water', '#1d6fb8'), (Qk[3], Qk[4], 'boiling', '#d9534f'),
         (Qk[4], Qk[5], 'steam', '#b8860b')]
for x0, x1, s, col in bands:
    ax.axvspan(x0, x1, color=col, alpha=0.07)
# the ice and steam bands are too narrow to hold a label, so they are named
# on a second row where nothing can collide
for x0, x1, s, col in bands[1:4]:
    ax.annotate(s, ((x0+x1)/2, 132), fontsize=8.0, color=col, ha='center')
ax.annotate('ice', (Qk[0]+10, 158), fontsize=8.0, color='#6a5acd', ha='left')
ax.annotate('steam', (Qk[5], 158), fontsize=8.0, color='#b8860b', ha='right')
ax.set_xlabel('heat supplied  (kJ per kg)'); ax.set_ylabel('temperature  ($^\circ$C)')
ax.set_xlim(0, Qk[-1]*1.02); ax.set_ylim(-40, 180)
ax.set_yticks([-20, 0, 50, 100, 120])
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45, axis='y')
```
Along the sloping parts the heat raises the kinetic energy of the molecules and
the temperature rises. Along the flat parts the heat does something else: it
breaks the bonds holding the molecules in place, increasing their potential
energy. The temperature does not change at all. Heat absorbed in this way is
called **latent** — Latin for *hidden* — because a thermometer cannot see it.

::: definition Latent heat
Latent heat is the heat absorbed or given out by a substance during a change of
phase at constant temperature and constant pressure.
:::

| Change of phase | Name | Heat |
|---|---|---|
| solid → liquid | fusion (melting) | absorbed |
| liquid → solid | freezing | given out |
| liquid → gas | vaporisation (boiling) | absorbed |
| gas → liquid | condensation | given out |
| solid → gas | sublimation | absorbed |

::: caution "Heat always raises temperature" is false
During melting and boiling the substance absorbs a great deal of heat with **no
temperature change at all**. A mistake in the reverse direction is just as
common: students forget that condensing steam *gives out* its latent heat, which
is why a steam burn is far worse than a burn from boiling water.
:::

## 11.4 Specific latent heat of fusion and vaporization

::: definition Specific latent heat
The specific latent heat $L$ of a substance is the heat required to change the
phase of **unit mass** of it at constant temperature: $Q = mL$, with $L$ in
J kg⁻¹.
:::

Two values matter for the NEB paper, both for water at normal atmospheric
pressure:

| Quantity | Symbol | Value | Temperature |
|---|---|---|---|
| Specific latent heat of fusion of ice | $L_f$ | $3.34\times10^{5}$ J kg⁻¹ | 0 °C |
| Specific latent heat of vaporisation of water | $L_v$ | $2.26\times10^{6}$ J kg⁻¹ | 100 °C |

$L_v$ is nearly seven times $L_f$. Melting only loosens the molecules so that
they can slide past one another; boiling has to separate them completely
against the attractive forces *and* push back the atmosphere while the vapour
expands. Both jobs need much more energy than simply unlocking the lattice.

::: example Worked example 11.3
**Problem.** How much heat is needed to convert 50 g of ice at $-10\ ^\circ$C
completely into steam at $100\ ^\circ$C? Take $c_{ice}=2100$, $c_w=4200$,
$c_{steam}=2010\ \text{J kg}^{-1}\text{K}^{-1}$, $L_f = 3.34\times10^5$ and
$L_v = 2.26\times10^6\ \text{J kg}^{-1}$.

**Solution.** Work through the stages one by one with $m = 0.050$ kg.

Warming ice from $-10\ ^\circ$C to $0\ ^\circ$C:

$$ Q_1 = mc_{ice}\Delta\theta = 0.050\times2100\times10 = 1050\ \text{J} $$

Melting the ice at $0\ ^\circ$C:

$$ Q_2 = mL_f = 0.050\times 3.34\times10^{5} = 16\,700\ \text{J} $$

Warming the water from $0\ ^\circ$C to $100\ ^\circ$C:

$$ Q_3 = mc_w\Delta\theta = 0.050\times4200\times100 = 21\,000\ \text{J} $$

Boiling the water at $100\ ^\circ$C:

$$ Q_4 = mL_v = 0.050\times2.26\times10^{6} = 113\,000\ \text{J} $$

Total heat required:

$$ Q = 1050+16\,700+21\,000+113\,000 = 1.52\times10^{5}\ \text{J} $$

Almost three quarters of it goes into the last step alone.
:::

## 11.5 Measurement of specific latent heat of fusion and vaporization

Both measurements use the method of mixtures, with one extra precaution in each
case.

### Latent heat of fusion of ice

Small pieces of ice at $0\ ^\circ$C are dried on blotting paper — **wet ice
carries water at $0\ ^\circ$C and makes $L_f$ come out too small** — and added
to warm water in a calorimeter. The water is started a few degrees above room
temperature and finishes a few degrees below it, so that the heat gained from
the room in the second half roughly cancels the heat lost in the first half.

If $m_i$ is the mass of ice, $W$ the water equivalent of the calorimeter,
$\theta_1$ the initial and $\theta_2$ the final temperature:

$$ (m_w + W)c_w(\theta_1-\theta_2) = m_i L_f + m_i c_w(\theta_2 - 0) $$

$$ L_f = \frac{(m_w+W)c_w(\theta_1-\theta_2)}{m_i} - c_w\theta_2 $$

### Latent heat of vaporisation of water

Dry steam at $100\ ^\circ$C is passed into cold water in a calorimeter. A **steam
trap** between the boiler and the calorimeter catches the water droplets carried
over with the steam; without it the measured $L_v$ is too small. The mass $m_s$
of steam condensed is found by reweighing the calorimeter at the end. With
$\theta_1$ and $\theta_2$ the initial and final temperatures,

$$ m_s L_v + m_s c_w(100-\theta_2) = (m_w+W)c_w(\theta_2-\theta_1) $$

$$ L_v = \frac{(m_w+W)c_w(\theta_2-\theta_1)}{m_s} - c_w(100-\theta_2) $$

::: example Worked example 11.4
**Problem.** A calorimeter of water equivalent 20 g contains 180 g of water at
$35.0\ ^\circ$C. When 23.4 g of dry ice at $0\ ^\circ$C is stirred in, the steady
temperature becomes $23.0\ ^\circ$C. Find the specific latent heat of fusion of
ice. ($c_w = 4200\ \text{J kg}^{-1}\text{K}^{-1}$.)

**Solution.** The calorimeter behaves like an extra 20 g of water, so the
cooling mass is $180+20 = 200$ g $= 0.200$ kg.

Heat given out by the water and calorimeter:

$$ Q = 0.200\times4200\times(35.0-23.0) = 840\times12 = 10\,080\ \text{J} $$

Heat taken by the ice, in two stages — melting, then warming the melt water from
$0\ ^\circ$C to $23.0\ ^\circ$C:

$$ Q = m_iL_f + m_ic_w\theta_2 = 0.0234\,L_f + 0.0234\times4200\times23.0 $$

The second term is $0.0234\times96\,600 = 2260\ \text{J}$. Therefore

$$ 0.0234\,L_f = 10\,080 - 2260 = 7820\ \text{J} $$

$$ L_f = \frac{7820}{0.0234} = 3.34\times10^{5}\ \text{J kg}^{-1} $$
:::

::: tip Where the marks are in a calorimetry question
Write the heat-lost side and the heat-gained side as two separate labelled
expressions before you equate them. Examiners give method marks for the correct
energy balance even when the arithmetic goes wrong, and they cannot give them if
they cannot see which term is which.
:::

## 11.6 Triple point

The temperature at which a substance melts and the temperature at which it boils
both depend on pressure. Plotting pressure against temperature gives the
**phase diagram**, whose three curves meet at a single point.

```figure caption="Phase diagram of water (pressure on a logarithmic scale). The fusion curve leans backwards, so extra pressure lowers the melting point of ice."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.0))
Tt, Pt = 273.16, 611.657
# vaporisation curve through triple, normal boiling, critical points
Ta = np.array([Tt, 373.15, 647.0]); Pa = np.array([Pt, 1.01325e5, 2.21e7])
co = np.polyfit(1/Ta, np.log(Pa), 2)
Tv = np.linspace(Tt, 647.0, 250)
Pv = np.exp(np.polyval(co, 1/Tv))
ax.plot(Tv, Pv, color='#d9534f', lw=2.0)
# sublimation curve
Ts = np.linspace(205.0, Tt, 200)
Ps = Pt*np.exp(6127.0*(1/Tt - 1/Ts))
ax.plot(Ts, Ps, color='#6a5acd', lw=2.0)
# fusion curve (leans left)
Pf = np.logspace(np.log10(Pt), 8.7, 120)
Tf = Tt - 22.0*(np.log10(Pf) - np.log10(Pt))/(8.7 - np.log10(Pt))
ax.plot(Tf, Pf, color='#2e8b57', lw=2.0)
ax.plot([Tt], [Pt], 'o', color=INK, ms=6, zorder=5)
ax.plot([647.0], [2.21e7], 'o', color=INK, ms=5, zorder=5)
ax.annotate('triple point\n273.16 K, 611 Pa', (Tt, Pt), textcoords='offset points',
            xytext=(10, -26), fontsize=8.1, color=INK)
ax.annotate('critical point', (647.0, 2.21e7), textcoords='offset points',
            xytext=(-16, 10), fontsize=8.1, color=INK, ha='right')
ax.annotate('SOLID', (230, 1e5), fontsize=8.6, color='#2e8b57', ha='center',
            va='center', rotation=90)
ax.annotate('LIQUID', (400, 3e6), fontsize=8.6, color='#1d6fb8', ha='center')
ax.annotate('VAPOUR', (500, 30), fontsize=8.6, color='#d9534f', ha='center')
ax.set_yscale('log')
ax.set_xlabel('temperature  $T$  (K)'); ax.set_ylabel('pressure  $p$  (Pa)')
ax.set_xlim(205, 700); ax.set_ylim(1e-1, 1e9)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
```

The three curves divide the diagram into solid, liquid and vapour regions. The
**fusion curve** separates solid from liquid, the **vaporisation curve**
separates liquid from vapour and ends at the critical point, and the
**sublimation curve** separates solid from vapour. They meet at one point only.

::: definition Triple point
The triple point of a substance is the single pressure and temperature at which
its solid, liquid and vapour phases can coexist in thermal equilibrium.
:::

For water the triple point is at

$$ T = 273.16\ \text{K} = 0.01\ ^\circ\text{C}, \qquad p = 611.66\ \text{Pa} $$

which is about 0.006 atmosphere. Below that pressure liquid water cannot exist
at all: ice warmed at low pressure sublimes straight to vapour. That is exactly
how freeze-drying works.

Because the triple point is fixed by nature and can be reproduced in a sealed
glass *triple-point cell* to better than a thousandth of a kelvin, it was chosen
as the single fixed point of the Kelvin scale. From 1954 to 2019 the kelvin was
**defined** as $1/273.16$ of the thermodynamic temperature of the triple point
of water. Since the SI revision of 2019 the kelvin is instead fixed by giving
the Boltzmann constant the exact value
$1.380649\times10^{-23}\ \text{J K}^{-1}$, and $273.16$ K has become a very
accurately *measured* quantity rather than a defined one.

::: caution The triple point is not the melting point
Ice melts at $0\ ^\circ$C under **1 atmosphere** of pressure. The triple point is
at $0.01\ ^\circ$C under only 611 Pa. The two differ because dissolved air and the
much higher pressure of the atmosphere each lower the melting point slightly.
:::

## Chapter summary

- Heat to change temperature: $Q = mc\Delta\theta$; heat capacity $C = mc$;
  water equivalent $W = mc/c_w$.
- Newton's law of cooling: $dQ/dt = -K(\theta-\theta_0)$, hence
  $\theta = \theta_0 + (\theta_1-\theta_0)e^{-kt}$. Valid only for small excess
  temperature and unchanged surroundings.
- Working form for problems:
  $(\theta_1-\theta_2)/t = k[(\theta_1+\theta_2)/2 - \theta_0]$.
- Specific heat capacity is measured by the method of mixtures,
  $m_sc_s(\theta_s-\theta_2) = (m_wc_w+m_cc_c)(\theta_2-\theta_1)$, or
  electrically, $VIt = (m_lc_l+m_cc_c)\Delta\theta$.
- Latent heat is absorbed at constant temperature during a phase change:
  $Q = mL$. For water $L_f = 3.34\times10^5$ and
  $L_v = 2.26\times10^6\ \text{J kg}^{-1}$.
- $L_f$ is measured with dried ice and $L_v$ with dry steam from a steam trap;
  both use the same energy balance.
- The triple point is the unique $(p,T)$ at which solid, liquid and vapour
  coexist. For water: 273.16 K and 611.66 Pa.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of specific latent heat is <span class="marks">[1]</span>
   (a) J kg⁻¹ K⁻¹ (b) J kg⁻¹ (c) J K⁻¹ (d) J
2. While a solid is melting, the heat supplied to it <span class="marks">[1]</span>
   (a) raises its temperature (b) raises its kinetic energy only
   (c) increases the potential energy of its molecules (d) is destroyed
3. Newton's law of cooling is best obeyed when <span class="marks">[1]</span>
   (a) the excess temperature is small (b) the body is red hot
   (c) the body is in vacuum (d) the surroundings are heated
4. The triple point of water occurs at <span class="marks">[1]</span>
   (a) 273.15 K and 1 atm (b) 273.16 K and 611 Pa
   (c) 373.15 K and 1 atm (d) 273.16 K and 1 atm
5. The water equivalent of a calorimeter of mass $m$ and specific heat capacity
   $c$ is <span class="marks">[1]</span>
   (a) $mc$ (b) $mc_w$ (c) $mc/c_w$ (d) $c_w/mc$

::: note Answers to Group A
**1.** (b) — $L = Q/m$, so joule per kilogram; there is no temperature change, hence no K in the unit.
**2.** (c) — the bonds are broken, so molecular potential energy rises while the temperature stays fixed.
**3.** (a) — the law is a linear approximation valid only for a small excess temperature.
**4.** (b) — 0.01 °C and 611.66 Pa.
**5.** (c) — the mass of water having the same heat capacity: $mc = Wc_w$.
:::

**Group B — Short answer (5 marks each)**

1. State Newton's law of cooling and show that the temperature of a cooling body
   falls exponentially towards that of its surroundings. <span class="marks">[5]</span>
2. A block of copper of mass 0.4 kg at $100\ ^\circ$C is dropped into 0.2 kg of
   water at $20\ ^\circ$C in a container of negligible heat capacity. Find the
   final temperature. ($c_{Cu}=400$, $c_w=4200\ \text{J kg}^{-1}\text{K}^{-1}$.) <span class="marks">[5]</span>
3. Define specific latent heat of fusion and of vaporisation, and explain why
   $L_v$ is much larger than $L_f$ for the same substance. <span class="marks">[5]</span>
4. Steam at $100\ ^\circ$C is passed into 0.5 kg of water at $20\ ^\circ$C in a
   calorimeter of water equivalent 0.02 kg until the temperature reaches
   $60\ ^\circ$C. Find the mass of steam condensed.
   ($L_v = 2.26\times10^6$, $c_w = 4200\ \text{J kg}^{-1}\text{K}^{-1}$.) <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: state the law; write $dQ/dt = -K(\theta-\theta_0)$; put
$dQ = mc\,d\theta$ to get $d\theta/dt = -k(\theta-\theta_0)$; separate variables
and integrate to $\ln(\theta-\theta_0) = -kt + C$; apply $\theta=\theta_1$ at
$t=0$ to obtain $\theta = \theta_0 + (\theta_1-\theta_0)e^{-kt}$.

**2.** Heat lost $= 0.4\times400\times(100-\theta) = 160(100-\theta)$; heat gained
$= 0.2\times4200\times(\theta-20) = 840(\theta-20)$. So
$16\,000-160\theta = 840\theta-16\,800$, giving $1000\theta = 32\,800$ and
$\theta = 32.8\ ^\circ$C.

**3.** Definitions as in §11.4. $L_v > L_f$ because melting only has to loosen
the lattice enough for molecules to slide, whereas vaporisation must separate
the molecules completely against their mutual attraction and, in addition, do
work pushing back the atmosphere as the vapour expands.

**4.** Heat gained $= (0.5+0.02)\times4200\times(60-20) = 2184\times40 = 87\,360$ J.
Heat given out by mass $m$ of steam $= m[2.26\times10^6 + 4200\times40]
= m(2.428\times10^6)$. Hence $m = 87\,360/2.428\times10^{6} = 0.036$ kg $= 36$ g.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define specific latent heat of vaporisation. <span class="marks">[2]</span>
   (b) Describe, with the necessary theory and two precautions, how the specific
   latent heat of vaporisation of water is measured by the method of mixtures. <span class="marks">[6]</span>
2. 100 g of ice at $0\ ^\circ$C is dropped into 300 g of water at $50\ ^\circ$C
   contained in a calorimeter of water equivalent 25 g.
   (a) Show that all the ice melts. <span class="marks">[3]</span>
   (b) Find the final temperature of the mixture. <span class="marks">[5]</span>
   ($L_f = 3.34\times10^5$, $c_w = 4200\ \text{J kg}^{-1}\text{K}^{-1}$.)

::: note Answers to Group C
**1.** (a) The heat needed to change unit mass of a liquid into vapour at its
boiling point without any change of temperature. (b) Steam from a boiler passes
through a steam trap into a weighed calorimeter holding a known mass of cold
water; record $\theta_1$, pass steam until the rise is about $20\ ^\circ$C,
record $\theta_2$, reweigh to get $m_s$. Theory:
$m_sL_v + m_sc_w(100-\theta_2) = (m_w+W)c_w(\theta_2-\theta_1)$.
Precautions: use a steam trap so that only **dry** steam enters; start below and
finish above room temperature so the heat exchange with the room cancels; stir
continuously; lag the calorimeter.

**2.** (a) Heat available from the water and calorimeter as they cool to
$0\ ^\circ$C is $(0.300+0.025)\times4200\times50 = 0.325\times4200\times50
= 68\,250$ J. The heat needed to melt all the ice is
$0.100\times3.34\times10^5 = 33\,400$ J. Since $68\,250 > 33\,400$, all the ice
melts and some heat is left over.

(b) Surplus heat $= 68\,250 - 33\,400 = 34\,850$ J. This warms the whole
mixture — 300 g of original water, 100 g of melt water and the 25 g water
equivalent, i.e. 0.425 kg — from $0\ ^\circ$C:

$\theta = 34\,850/(0.425\times4200) = 34\,850/1785 = 19.5\ ^\circ$C.
:::

---
subject: Physics
grade: 11
unit: 12
title: Rate of heat flow
hours: 5
area: Heat and Thermodynamics
---

Unit 11 asked *how much* heat. This unit asks *how fast*. Heat travels from a
hot place to a cold one by three mechanisms — conduction, convection and
radiation — and each has its own law. Conduction passes energy along without
moving the material, convection carries it bodily in a moving fluid, and
radiation sends it across empty space as electromagnetic waves. A thermos flask
is the standard exam object because it is designed to defeat all three at once.

::: key Three mechanisms, three signatures
| Mechanism | Needs matter? | Matter moves? | Governing law |
|---|---|---|---|
| Conduction | yes | no | $H = kA\,\Delta\theta/L$ |
| Convection | yes (fluid only) | yes | $H \propto \Delta\theta$ (Newton) |
| Radiation | no | no | $H = e\sigma A T^{4}$ (Stefan) |
:::

## 12.1 Conduction: Thermal conductivity and measurement

Hold one end of an iron rod in a fire and the other end soon becomes too hot to
hold. The atoms at the hot end vibrate more violently, collide with their
neighbours and pass the energy along the lattice; in a metal the free electrons
carry most of it, which is why metals conduct far better than non-metals. No
part of the rod moves as a whole.

::: derivation The conduction equation $H = \dfrac{kA(\theta_1-\theta_2)}{L}$
We start from three facts that experiment gives us, and reach the single equation that
governs all steady conduction.

**Setting up.** A slab has cross-sectional area $A$ and thickness $L$. Its two faces are
held at steady temperatures $\theta_1$ and $\theta_2$, with $\theta_1 > \theta_2$. Let
$H = dQ/dt$ be the heat current — the joules crossing the slab each second. We wait until
the **steady state**: every cross-section then carries the same $H$, because no part of the
slab is still warming up.

**Step 1 — $H$ depends on the area.** Two identical slabs side by side conduct twice as
much as one, and they are the same thing as one slab of double the area. So

$$ H \propto A $$

**Step 2 — $H$ depends on the temperature difference.** Nothing flows when the two faces
are equally hot, and experiment shows the flow doubles when the difference doubles:

$$ H \propto (\theta_1 - \theta_2) $$

**Step 3 — $H$ depends inversely on the thickness.** A thicker slab is a longer journey for
the heat. Two slabs one behind the other (thickness $2L$) carry half the current of one:

$$ H \propto \frac{1}{L} $$

**Step 4 — combine the three proportionalities.** When a quantity is separately
proportional to several others, it is proportional to their product:

$$ H \propto \frac{A(\theta_1 - \theta_2)}{L} $$

**Step 5 — replace "$\propto$" by an equals sign and a constant.** Call that constant $k$;
it depends only on the material:

$$ H = \frac{kA(\theta_1 - \theta_2)}{L} $$

**Step 6 — the differential form.** In the steady state the temperature falls evenly across
the slab, so $(\theta_1 - \theta_2)/L$ is just the size of the **temperature gradient**
$d\theta/dx$. Writing the gradient with its own sign:

$$ H = -kA\frac{d\theta}{dx} $$

**Result.**

$$ H = \frac{kA(\theta_1 - \theta_2)}{L} = -kA\frac{d\theta}{dx} $$

**What it means.** The minus sign in the last form says heat flows *down* the temperature
gradient — from hot to cold, never the other way. The constant $k$ is the **thermal
conductivity**: a large $k$ (copper) means a big heat current for a small temperature
difference, a small $k$ (wood, still air) means a good insulator.

**Conditions used.** The steady state has been reached (temperatures no longer changing);
the flow is one-dimensional, i.e. no heat escapes from the sides, which is why rods are
**lagged**; and the slab is made of one uniform material.
:::

::: definition Thermal conductivity
The thermal conductivity of a material is the rate of flow of heat per unit area
per unit temperature gradient, in the steady state. Its SI unit is
W m⁻¹ K⁻¹, and its dimensional formula is $[MLT^{-3}\Theta^{-1}]$.
:::

```figure caption="Steady conduction through a slab. In the steady state the temperature falls uniformly from $\theta_1$ to $\theta_2$ across the thickness $L$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.add_patch(Rectangle((2.0, 0.6), 2.4, 3.2, facecolor='#e3e8ef', ec=INK, lw=1.4))
ax.add_patch(Rectangle((1.88, 0.6), 0.12, 3.2, facecolor='#d9534f', ec='none'))
ax.add_patch(Rectangle((4.4, 0.6), 0.12, 3.2, facecolor='#1d6fb8', ec='none'))
for y in (1.2, 2.2, 3.2):
    ax.annotate('', xy=(4.35, y), xytext=(2.05, y),
                arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.5, mutation_scale=11))
ax.annotate('$\\theta_1$', (1.94, 3.95), ha='center', fontsize=10, color='#d9534f')
ax.annotate('$\\theta_2$', (4.46, 3.95), ha='center', fontsize=10, color='#1d6fb8')
ax.annotate('heat current $H$', (3.2, 2.55), ha='center', fontsize=8.6, color='#b8860b')
# thickness measured below the slab, face area called out on the cold face
ax.annotate('', xy=(4.4, 0.40), xytext=(2.0, 0.40),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=8))
ax.annotate('$L$', (3.2, 0.30), ha='center', va='top', fontsize=9.5, color=MUTED)
ax.annotate('area $A$', xy=(4.52, 1.70), xytext=(5.15, 1.35), ha='left', va='center',
            fontsize=9, color=INK,
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8, shrinkA=2, shrinkB=2))
tx = np.linspace(2.0, 4.4, 50)
ax.plot(tx, 5.15 - 0.70*(tx-2.0)/2.4, color='#2e8b57', lw=1.6, ls='--')
ax.annotate('temperature\nprofile', (4.70, 4.55), fontsize=8.4, va='center',
            color='#2e8b57')
ax.set_xlim(1.0, 6.8); ax.set_ylim(0.0, 5.6); ax.axis('off')
```
It is often convenient to write the law like Ohm's law. Defining the
**thermal resistance** $R = L/(kA)$,

$$ H = \frac{\theta_1-\theta_2}{R} $$

so that temperature difference plays the part of potential difference and heat
current the part of electric current. Slabs one behind the other are in
**series**, and their thermal resistances simply add:
$R = R_1 + R_2 + \cdots$. This single idea handles every composite-wall problem.

| Material | $k$ / W m⁻¹ K⁻¹ | Material | $k$ / W m⁻¹ K⁻¹ |
|---|---|---|---|
| Silver | 420 | Glass | 0.8 |
| Copper | 390 | Brick | 0.6 |
| Aluminium | 240 | Water | 0.6 |
| Brass | 110 | Wood | 0.15 |
| Steel | 50 | Air (still) | 0.024 |

### Measuring $k$ of a good conductor: Searle's method

A thick lagged bar of the metal is heated at one end by a steam chest and cooled
at the other by water flowing steadily through a spiral. Two thermometers
$\theta_1$ and $\theta_2$ sit in holes a measured distance $x$ apart along the
bar; two more read the inlet and outlet temperatures $\theta_3$ and $\theta_4$
of the water.

::: derivation The working formula of Searle's method
We start from the fact that in the steady state the water carries away exactly the heat the
bar delivers, and reach a formula for $k$ in terms of things we can measure.

**Setting up.** $A$ is the cross-sectional area of the bar, $x$ the distance between the two
thermometers in it, $c_w$ the specific heat capacity of water, and $m$ the mass of water
collected in time $t$.

**Step 1 — the heat conducted along the bar between the two thermometers.** Apply the
conduction equation to the length $x$ of bar between them:

$$ H_{conducted} = \frac{kA(\theta_1 - \theta_2)}{x} $$

**Step 2 — the heat gained by the water.** A mass $m$ of water rises in temperature from
$\theta_3$ to $\theta_4$, so it absorbs heat $Q = mc_w(\theta_4 - \theta_3)$. Dividing by
the time $t$ gives the rate:

$$ H_{absorbed} = \frac{mc_w(\theta_4 - \theta_3)}{t} $$

**Step 3 — set them equal.** In the steady state nothing in the bar is getting hotter, so
none of the heat stays behind, and the lagging stops any escaping sideways. Everything
conducted in is carried out by the water:

$$ \frac{kA(\theta_1 - \theta_2)}{x} = \frac{mc_w(\theta_4 - \theta_3)}{t} $$

**Step 4 — multiply both sides by $x$:**

$$ kA(\theta_1 - \theta_2) = \frac{mc_w(\theta_4 - \theta_3)\,x}{t} $$

**Step 5 — divide both sides by $A(\theta_1 - \theta_2)$:**

$$ k = \frac{mc_w(\theta_4 - \theta_3)\,x}{A(\theta_1 - \theta_2)\,t} $$

**Result.**

$$ k = \frac{mc_w(\theta_4 - \theta_3)\,x}{A(\theta_1 - \theta_2)\,t} $$

**What it means.** Every symbol on the right can be measured in the laboratory: $m$ by
weighing the collected water, $t$ by a stopwatch, the four temperatures by thermometers, and
$x$ and $A$ by a ruler and a micrometer. Note which temperature difference goes where —
$(\theta_1-\theta_2)$ belongs to the **bar**, $(\theta_4-\theta_3)$ to the **water**.

**Conditions used.** A true steady state (all four thermometer readings constant), perfect
lagging so no heat leaks from the sides, and a steady flow of water.
:::

```figure caption="Searle's apparatus. The heat conducted between the two thermometers in the bar is collected by the flowing water."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 2.6))
ax.add_patch(Rectangle((1.4, 1.5), 7.0, 0.85, facecolor='#f6d9b0', ec=INK, lw=1.3))
# lagging covers only the exposed middle of the bar, not the chest or the jacket
ax.add_patch(Rectangle((2.4, 2.35), 4.9, 0.3, facecolor='#efe6d5', ec='none'))
ax.add_patch(Rectangle((2.4, 1.2), 4.9, 0.3, facecolor='#efe6d5', ec='none'))
ax.add_patch(Rectangle((1.2, 1.15), 1.2, 1.6, facecolor='#f3c7c4', ec=INK, lw=1.2))
ax.add_patch(Rectangle((7.3, 1.15), 1.4, 1.6, facecolor='#bcd9ef', ec=INK, lw=1.2))
for x, lab, col in [(3.6, '$\\theta_1$', '#d9534f'), (6.2, '$\\theta_2$', '#d9534f'),
                    (7.6, '$\\theta_3$', '#1d6fb8'), (8.4, '$\\theta_4$', '#1d6fb8')]:
    ax.plot([x, x], [1.9 if col == '#d9534f' else 2.0, 3.5], color=INK, lw=1.2)
    ax.annotate(lab, (x, 3.6), ha='center', fontsize=9, color=col)
ax.annotate('', xy=(6.2, 1.05), xytext=(3.6, 1.05),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=8))
ax.annotate('$x$', (4.9, 0.95), ha='center', va='top', fontsize=9.5, color=MUTED)
ax.annotate('steam\nchest', (1.8, 0.85), ha='center', va='top', fontsize=8.2, color=INK)
ax.annotate('metal bar, area $A$', (4.9, 1.85), ha='center', va='center',
            fontsize=8.4, color=INK)
# the water labels sit beyond the ends of their own arrows, clear of the vessel
ax.annotate('', xy=(8.75, 1.40), xytext=(9.85, 1.40),
            arrowprops=dict(arrowstyle='-|>', color='#1d6fb8', lw=1.3, mutation_scale=10))
ax.annotate('water in', (9.95, 1.40), ha='left', va='center', fontsize=8.2,
            color='#1d6fb8')
ax.annotate('', xy=(9.85, 2.55), xytext=(8.75, 2.55),
            arrowprops=dict(arrowstyle='-|>', color='#1d6fb8', lw=1.3, mutation_scale=10))
ax.annotate('water out', (9.95, 2.55), ha='left', va='center', fontsize=8.2,
            color='#1d6fb8')
ax.annotate('lagging', xy=(6.9, 1.34), xytext=(6.9, 0.72), ha='center', va='center',
            fontsize=8.2, color=MUTED,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8, shrinkA=2, shrinkB=1))
ax.set_xlim(0.8, 11.8); ax.set_ylim(0.3, 4.1); ax.axis('off')
```
For a **bad** conductor such as glass, cardboard or rubber, Searle's bar is
useless: the flow would be far too small to measure. **Lee's disc method** is
used instead. The specimen is made a thin disc of large area sandwiched between
a steam chamber and a thick brass disc, so that the heat flows through a short
distance and a wide area.

::: caution Lagging is not decoration
The derivation of $H = kA\Delta\theta/L$ assumes that **all** the heat entering
one face leaves the other. If the bar is not lagged, heat escapes sideways, the
temperature gradient stops being uniform, and $k$ comes out too small. In every
diagram you draw, show the lagging and say what it is for.
:::

::: example Worked example 12.1
**Problem.** A glass window measures $1.5\ \text{m}\times1.0\ \text{m}$ and is
4.0 mm thick. The inner surface is at $25\ ^\circ$C and the outer at
$5\ ^\circ$C. Taking $k_{glass}=0.80\ \text{W m}^{-1}\text{K}^{-1}$, find the rate
of heat loss.

**Solution.** $A = 1.5\times1.0 = 1.5\ \text{m}^2$, $L = 4.0\times10^{-3}$ m and
$\Delta\theta = 20$ K.

$$ H = \frac{kA\,\Delta\theta}{L}
= \frac{0.80\times1.5\times20}{4.0\times10^{-3}} = \frac{24}{4.0\times10^{-3}}
= 6.0\times10^{3}\ \text{W} $$

Six kilowatts through one window is absurdly large, and it tells us the
assumption is wrong: the glass surfaces are *not* at room and outdoor
temperature. Thin films of still air on each side, with $k$ only 0.024, provide
nearly all the real thermal resistance.
:::

::: example Worked example 12.2
**Problem.** A copper rod ($k = 390$) and a brass rod ($k = 110\ \text{W m}^{-1}
\text{K}^{-1}$) of equal length and equal cross-section are joined end to end.
The free end of the copper is kept at $100\ ^\circ$C and the free end of the
brass at $0\ ^\circ$C. Find the steady temperature of the junction. The sides are
perfectly lagged.

**Solution.** In the steady state the same heat current passes through both
rods. With equal $A$ and equal $L$, and junction temperature $\theta$:

$$ \frac{k_1A(100-\theta)}{L} = \frac{k_2A(\theta-0)}{L}
\;\Longrightarrow\; 390(100-\theta) = 110\theta $$

$$ 39\,000 = 500\theta \;\Longrightarrow\; \theta = 78\ ^\circ\text{C} $$

In general $\theta = (k_1\theta_1+k_2\theta_2)/(k_1+k_2)$ for equal rods: the
junction sits closer to the temperature of the **better** conductor.
:::

## 12.2 Convection

::: definition Convection
Convection is the transfer of heat through a fluid by the bulk movement of the
heated fluid itself.
:::

Warm a fluid from below and it expands, becomes less dense, and is pushed up by
the denser cold fluid around it, which then takes its place and is warmed in
turn. The resulting circulation is a **convection current**. Because the
material itself has to move, convection is impossible in solids and impossible
in a vacuum.

| | Natural convection | Forced convection |
|---|---|---|
| Cause of motion | density difference and gravity | pump, fan or blower |
| Speed | slow | fast |
| Example | air above a heater, boiling water | radiator fan, hair dryer, blood circulation |

The rate of convective loss from a surface is roughly proportional to the excess
temperature, $H = hA(\theta-\theta_0)$, where $h$ is the convection coefficient.
This is precisely Newton's law of cooling from Unit 11 — Newton's law is a law
of convection, which is why it fails when radiation takes over at high
temperature.

```figure caption="Daytime valley wind. The sunlit slope heats the air against it, which rises, and cooler air flows up the valley to replace it."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
fig, ax = plt.subplots(figsize=(4.9, 2.6))
ax.add_patch(Polygon([[0.0,0.0],[2.6,0.0],[0.6,3.0]], closed=True, facecolor='#cdbfa6', ec=INK, lw=1.1))
ax.add_patch(Polygon([[4.4,0.0],[8.0,0.0],[7.6,3.2]], closed=True, facecolor='#b9ab92', ec=INK, lw=1.1))
ax.add_patch(Polygon([[2.6,0.0],[4.4,0.0],[4.4,0.25],[2.6,0.25]], closed=True,
                     facecolor='#9fb98a', ec='none'))
ax.add_patch(Circle((7.0, 3.9), 0.36, facecolor='#e8b53a', ec='none'))
ax.annotate('sun', (7.0, 4.45), ha='center', fontsize=8.2, color='#b8860b')
for a, b in [((6.3,3.5),(5.6,2.6)), ((6.7,3.1),(6.1,2.3))]:
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color='#e8b53a',
                lw=1.2, mutation_scale=9))
for x0, y0, x1, y1 in [(5.1,0.5,6.6,2.6), (5.6,0.3,7.0,2.2)]:
    ax.annotate('', xy=(x1,y1), xytext=(x0,y0),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.6,
                                connectionstyle='arc3,rad=-0.25', mutation_scale=11))
ax.annotate('', xy=(4.6,1.0), xytext=(2.1,1.0),
            arrowprops=dict(arrowstyle='-|>', color='#1d6fb8', lw=1.6, mutation_scale=11))
ax.annotate('warm air rises\nalong sunlit slope', (4.9, 2.60), fontsize=8.2,
            ha='right', va='center', color='#d9534f')
ax.annotate('cool air drawn in', (3.35, 1.25), fontsize=8.2, color='#1d6fb8', ha='center')
ax.annotate('valley floor', (3.5, -0.35), fontsize=8.2, color=MUTED, ha='center')
ax.set_xlim(-0.3, 9.6); ax.set_ylim(-0.7, 5.0); ax.axis('off')
```

Convection explains a long list of everyday things: the up-valley wind that
blows through Pokhara and Kathmandu on a sunny afternoon and reverses at night;
land and sea breezes; the draught up a chimney; the circulation of water in a
solar water heater on a rooftop, which needs no pump because hot water rises on
its own; why a room heater is placed low and an air conditioner high; and why
the trapped air in a woollen sweater keeps you warm — the wool stops the air
from convecting away.

## 12.3 Radiation: Ideal radiator

The Earth receives energy from the Sun across 150 million kilometres of vacuum,
so there must be a third mechanism that needs no matter at all.

::: definition Thermal radiation
Thermal radiation is energy emitted by every body on account of its temperature,
carried by electromagnetic waves — mainly infrared for bodies near room
temperature.
:::

Radiation travels at $3\times10^{8}\ \text{m s}^{-1}$, obeys the inverse-square
law, and can be reflected and refracted like light. **Prevost's theory of heat
exchange** states that every body above absolute zero radiates continuously,
whatever its surroundings; a body appears to cool only because it emits more
than it absorbs, and at thermal equilibrium the two rates are equal.

When radiation falls on a body, part is absorbed, part reflected and part
transmitted. Writing each as a fraction of the incident energy,

$$ a + r + t = 1 $$

::: definition Perfect black body (ideal radiator)
A perfect black body is one that absorbs **all** the radiation of every
wavelength falling on it, so that $a = 1$ and $r = t = 0$. At a given
temperature it is also the best possible emitter at every wavelength.
:::

That the best absorber is also the best emitter is **Kirchhoff's law**: at a
given temperature and wavelength, the ratio of emissive power to absorptive
power is the same for all bodies and equals the emissive power of a black body.
The everyday proof is a glazed white cup with a coloured pattern: heat it in a
furnace and the pattern, which absorbs best, glows brightest.

No real surface is perfectly black — lamp black absorbs about 96 %. A practical
black body is made instead as a cavity: **Ferry's black body** is a
double-walled copper sphere, blackened with lamp black inside, with a small hole
and a conical projection opposite it. Radiation entering the hole is reflected
many times inside and absorbed almost completely before it can find its way out,
so the hole behaves as a black surface. Heat the sphere and the same hole
becomes an ideal radiator.

The **emissivity** $e$ of a real surface is the ratio of its emissive power to
that of a black body at the same temperature, so $0 \le e \le 1$, with $e = 1$
for a black body. By Kirchhoff's law $e = a$.

## 12.4 Black-body radiation

A black body does not radiate at one wavelength only. Measuring how the emitted
power is distributed over wavelength gives the **black-body spectrum**, first
measured accurately by Lummer and Pringsheim.

```figure caption="Black-body spectra at three temperatures. As $T$ rises the peak grows, the total area grows much faster, and $\lambda_m$ moves to shorter wavelengths."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 2.9))
h, c, kB = 6.626e-34, 3.0e8, 1.381e-23
lam = np.linspace(0.12e-6, 3.0e-6, 700)
for T, col in [(3000, '#1d6fb8'), (4000, '#2e8b57'), (5000, '#d9534f')]:
    E = (2*np.pi*h*c**2/lam**5)/(np.exp(h*c/(lam*kB*T)) - 1.0)
    ax.plot(lam*1e6, E/1e13, color=col, lw=1.8, label=f'{T} K')
    lm = 2.898e-3/T
    Em = (2*np.pi*h*c**2/lm**5)/(np.exp(h*c/(lm*kB*T)) - 1.0)
    ax.plot([lm*1e6], [Em/1e13], 'o', color=col, ms=4.5)
Tg = np.linspace(2600, 5200, 60)
lg = 2.898e-3/Tg
Eg = (2*np.pi*h*c**2/lg**5)/(np.exp(h*c/(lg*kB*Tg)) - 1.0)
ax.plot(lg*1e6, Eg/1e13, color=MUTED, lw=1.0, ls='--')
# the label is lifted clear of the 5000 K curve and tied to the dashed locus
ax.annotate('$\\lambda_m T = $ constant', xy=(0.575, 4.16), xytext=(0.74, 4.28),
            ha='left', va='bottom', fontsize=8.3, color=MUTED,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7, shrinkA=2, shrinkB=2))
ax.set_xlabel('wavelength  $\\lambda$  ($\\mu$m)')
ax.set_ylabel('$E_\\lambda$  ($10^{13}$ W m$^{-3}$)')
ax.set_xlim(0, 3.0); ax.set_ylim(0, 4.6)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
ax.legend(title='temperature', fontsize=8.2, title_fontsize=8.2, loc='upper right')
```

Four features of these curves must be quoted:

1. The spectrum is **continuous**: energy is emitted at every wavelength.
2. Each curve rises to a single maximum at a wavelength $\lambda_m$ and falls
   away on both sides; the emission is very small at very short and very long
   wavelengths.
3. As the temperature rises, $\lambda_m$ shifts towards **shorter** wavelengths.
   This is **Wien's displacement law**:

$$ \lambda_m T = b = 2.898\times10^{-3}\ \text{m K} $$

4. The **area** under a curve is the total power radiated per unit area, and it
   increases very rapidly with temperature — as $T^4$, which is the next
   section.

Wien's law is why a heated iron bar glows dull red, then orange, then white as
it gets hotter, and why the blue star Rigel is hotter than the red star
Betelgeuse. Classical physics could not reproduce these curves at all; it
predicted that the emission should grow without limit at short wavelengths (the
*ultraviolet catastrophe*). Planck fixed it in 1900 by assuming that energy is
emitted in discrete quanta $E = h\nu$ — the beginning of quantum theory.

::: example Worked example 12.3
**Problem.** The Sun radiates most strongly at $\lambda_m = 500$ nm. Treating it
as a black body, find (a) its surface temperature and (b) the power radiated per
square metre of its surface. Take $b = 2.898\times10^{-3}\ \text{m K}$ and
$\sigma = 5.67\times10^{-8}\ \text{W m}^{-2}\text{K}^{-4}$.

**Solution.** (a) From Wien's displacement law,

$$ T = \frac{b}{\lambda_m} = \frac{2.898\times10^{-3}}{500\times10^{-9}}
= 5.80\times10^{3}\ \text{K} $$

(b) From Stefan's law, with $T = 5796$ K,

$$ E = \sigma T^{4} = 5.67\times10^{-8}\times(5796)^{4}
= 5.67\times10^{-8}\times1.129\times10^{15} $$

$$ E = 6.4\times10^{7}\ \text{W m}^{-2} $$
:::

## 12.5 Stefan-Boltzmann law

::: definition Stefan-Boltzmann law
The total energy radiated per second per unit area by a perfect black body is
directly proportional to the fourth power of its absolute temperature:
$$ E = \sigma T^{4} $$
where $\sigma = 5.67\times10^{-8}\ \text{W m}^{-2}\text{K}^{-4}$ is the
Stefan-Boltzmann constant.
:::

For a body of surface area $A$ and emissivity $e$ the total power radiated is
$P = e\sigma AT^{4}$. But the body is also absorbing from its surroundings at
$T_0$, at a rate $e\sigma AT_0^{4}$ by Prevost's theory. The **net** rate of
loss is therefore

$$ P_{net} = e\sigma A\left(T^{4} - T_0^{4}\right) $$

::: caution Kelvin, always kelvin
$T$ in Stefan's law is the **absolute** temperature. Putting degrees Celsius
into $T^4$ is the single commonest error in this unit — and because of the
fourth power, the answer is not slightly wrong, it is wrong by orders of
magnitude. Convert first, every time.
:::

::: derivation Newton's law of cooling follows from Stefan's law
We start from the net rate of radiation loss and reach Newton's law of cooling, valid when
the body is only a little hotter than its surroundings.

**Step 1 — write the body's temperature as surroundings plus a small excess.** Let
$\Delta T = T - T_0$ be that excess:

$$ T = T_0 + \Delta T $$

**Step 2 — put this into the net-loss formula:**

$$ P_{net} = e\sigma A\left[(T_0 + \Delta T)^{4} - T_0^{4}\right] $$

**Step 3 — take $T_0$ outside the first bracket** so we can use the binomial expansion:

$$ P_{net} = e\sigma A T_0^{4}\left[\left(1 + \frac{\Delta T}{T_0}\right)^{4} - 1\right] $$

**Step 4 — expand by the binomial theorem.** Since $\Delta T/T_0$ is small, we keep only
the first power of it:

$$ \left(1 + \frac{\Delta T}{T_0}\right)^{4} \approx 1 + 4\,\frac{\Delta T}{T_0} $$

**Step 5 — substitute that back.** The two $1$'s cancel:

$$ P_{net} \approx e\sigma A T_0^{4}\cdot 4\,\frac{\Delta T}{T_0} $$

**Step 6 — cancel one factor of $T_0$:**

$$ P_{net} \approx 4e\sigma A T_0^{3}\,\Delta T $$

**Step 7 — recognise that everything except $\Delta T$ is constant.** $e$, $\sigma$, $A$
and $T_0$ all stay fixed while the body cools, so

$$ P_{net} \propto \Delta T = (T - T_0) $$

**Result.** The rate of heat loss, and therefore the rate of fall of temperature, is
proportional to the excess temperature — which is exactly **Newton's law of cooling**, with
$k$ identified as $4e\sigma A T_0^{3}/(mc)$.

**What it means.** Newton's law is not a separate law of nature; it is Stefan's $T^{4}$ law
seen through a narrow window of small temperature differences.

**Condition used.** $\Delta T \ll T_0$ — this is the only reason we were allowed to stop the
binomial expansion after the first term. For a large excess temperature the $T^{4}$ law must
be used in full, and Newton's law fails.
:::

::: example Worked example 12.4
**Problem.** A blackened metal sphere of radius 5.0 cm is maintained at
$327\ ^\circ$C in a room at $27\ ^\circ$C. Taking it as a perfect black body,
find the net rate at which it loses energy by radiation.

**Solution.** Convert to kelvin: $T = 327+273 = 600$ K and $T_0 = 27+273 = 300$ K.

Surface area of the sphere:

$$ A = 4\pi r^{2} = 4\pi(0.050)^{2} = 3.14\times10^{-2}\ \text{m}^{2} $$

Fourth powers: $T^4 = (600)^4 = 1.296\times10^{11}$ and
$T_0^4 = (300)^4 = 8.10\times10^{9}$, so
$T^4 - T_0^4 = 1.215\times10^{11}\ \text{K}^4$.

$$ P_{net} = \sigma A(T^{4}-T_0^{4})
= 5.67\times10^{-8}\times3.14\times10^{-2}\times1.215\times10^{11} $$

$$ P_{net} = 216\ \text{W} $$

Note that doubling the absolute temperature multiplied the emission by
$2^4 = 16$: the surroundings contribute only about 6 % of what the sphere emits.
:::

A vacuum flask now makes complete sense. The double wall with the space
evacuated stops conduction and convection; the silvered surfaces have a very low
emissivity and so radiate and absorb very little; and the narrow insulating
stopper blocks the only remaining conduction path.

## Chapter summary

- Steady conduction: $H = kA(\theta_1-\theta_2)/L = -kA\,d\theta/dx$; thermal
  conductivity $k$ is in W m⁻¹ K⁻¹.
- Thermal resistance $R = L/(kA)$; resistances of slabs in series add, and
  $H = \Delta\theta/R$.
- Searle's method measures $k$ for good conductors:
  $k = mc_w(\theta_4-\theta_3)x/[A(\theta_1-\theta_2)t]$; Lee's disc is used for
  bad conductors.
- Convection needs a moving fluid; natural convection is driven by density
  differences, forced convection by a fan or pump. Newton's law of cooling is a
  convection law.
- Radiation needs no medium. $a+r+t=1$; a perfect black body has $a = e = 1$;
  Kirchhoff's law says good absorbers are good emitters; Prevost's theory says
  emission never stops.
- Black-body curves are continuous with one maximum; Wien's displacement law
  gives $\lambda_m T = 2.898\times10^{-3}$ m K.
- Stefan-Boltzmann law: $E = \sigma T^4$ with
  $\sigma = 5.67\times10^{-8}\ \text{W m}^{-2}\text{K}^{-4}$; net loss
  $P = e\sigma A(T^4-T_0^4)$, with $T$ in kelvin.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of thermal conductivity is <span class="marks">[1]</span>
   (a) W m⁻¹ K⁻¹ (b) W m⁻² K⁻⁴ (c) J kg⁻¹ K⁻¹ (d) W m K
2. If the absolute temperature of a black body is doubled, the energy it radiates
   per second becomes <span class="marks">[1]</span>
   (a) 2 times (b) 4 times (c) 8 times (d) 16 times
3. A good absorber of radiation is also a good emitter. This is <span class="marks">[1]</span>
   (a) Stefan's law (b) Wien's law (c) Kirchhoff's law (d) Prevost's theory
4. Heat transfer by convection cannot take place in <span class="marks">[1]</span>
   (a) water (b) air (c) a solid (d) any fluid
5. The wavelength of maximum emission from a black body at 2000 K is about
   1450 nm. At 4000 K it will be about <span class="marks">[1]</span>
   (a) 5800 nm (b) 2900 nm (c) 725 nm (d) 1450 nm

::: note Answers to Group A
**1.** (a) — from $H = kA\Delta\theta/L$, $k$ has units W m⁻¹ K⁻¹.
**2.** (d) — $E \propto T^4$, and $2^4 = 16$.
**3.** (c) — Kirchhoff's law, $e = a$.
**4.** (c) — convection needs the material itself to move, which a solid cannot do.
**5.** (c) — $\lambda_m \propto 1/T$, so doubling $T$ halves $\lambda_m$.
:::

**Group B — Short answer (5 marks each)**

1. Define thermal conductivity and derive $H = kA(\theta_1-\theta_2)/L$ for
   steady conduction through a slab. Why must the slab be lagged? <span class="marks">[5]</span>
2. A wall of area $10\ \text{m}^2$ is made of 12 cm of brick
   ($k = 0.60\ \text{W m}^{-1}\text{K}^{-1}$) covered on the outside with 4.0 cm
   of insulating board ($k = 0.050\ \text{W m}^{-1}\text{K}^{-1}$). The inside
   surface is at $25\ ^\circ$C and the outside surface at $5\ ^\circ$C. Find the
   rate of heat flow and the temperature of the junction. <span class="marks">[5]</span>
3. Distinguish between natural and forced convection, and explain why a thermos
   flask has a vacuum between its walls and silvered surfaces. <span class="marks">[5]</span>
4. A black body of surface area $20\ \text{cm}^2$ is kept at $527\ ^\circ$C in
   surroundings at $27\ ^\circ$C. Find the net rate of loss of heat by radiation. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: define $k$ as in §12.1; state $H \propto A$ and
$H \propto \Delta\theta/L$ in the steady state; combine to
$H = kA\Delta\theta/L$. Lagging ensures no heat escapes through the sides, so
the heat current is the same at every cross-section and the gradient is uniform.

**2.** $R_1 = L_1/(k_1A) = 0.12/(0.60\times10) = 0.020\ \text{K W}^{-1}$ and
$R_2 = 0.040/(0.050\times10) = 0.080\ \text{K W}^{-1}$, so
$R = 0.100\ \text{K W}^{-1}$. Then $H = \Delta\theta/R = 20/0.100 = 200$ W.
Junction temperature $\theta = 25 - HR_1 = 25 - 200\times0.020 = 21\ ^\circ$C.
(Check: $(21-5)/0.080 = 200$ W.)

**3.** Natural convection is driven by the density change of the fluid itself in
a gravitational field; forced convection is driven by an external pump or fan
and is much faster. In a flask the vacuum removes the matter that conduction and
convection need, and the silvering gives a very low emissivity so that little is
radiated or absorbed.

**4.** $A = 20\times10^{-4} = 2.0\times10^{-3}\ \text{m}^2$, $T = 800$ K,
$T_0 = 300$ K. $T^4 - T_0^4 = 4.096\times10^{11} - 8.1\times10^{9}
= 4.015\times10^{11}$. So
$P = 5.67\times10^{-8}\times2.0\times10^{-3}\times4.015\times10^{11} = 45.5$ W.
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe Searle's method for determining the thermal conductivity of a
   good conductor, with a labelled diagram, and derive the working formula. <span class="marks">[6]</span>
   (b) State two reasons why the method is unsuitable for glass. <span class="marks">[2]</span>
2. (a) Draw the energy distribution curves of black-body radiation for three
   temperatures and state the conclusions drawn from them. <span class="marks">[4]</span>
   (b) A star radiates most strongly at 350 nm and has a radius of
   $7.0\times10^{8}$ m. Find its surface temperature and its total power output,
   treating it as a black body. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) Diagram and theory as in §12.1; the working formula is
$k = mc_w(\theta_4-\theta_3)x/[A(\theta_1-\theta_2)t]$, obtained by equating the
heat conducted between the two bar thermometers to the heat carried away by the
water. (b) Glass has a very small $k$, so the heat collected by the water in a
reasonable time would be too small to measure, and the temperature difference
$\theta_4-\theta_3$ would be lost in the experimental error; also, a long thin
glass bar would lose most of the heat sideways despite lagging.

**2.** (a) Curves as in Figure 4, with the four conclusions of §12.4. (b)
$T = b/\lambda_m = 2.898\times10^{-3}/(350\times10^{-9}) = 8280$ K. Surface area
$A = 4\pi R^2 = 4\pi(7.0\times10^{8})^2 = 6.16\times10^{18}\ \text{m}^2$. With
$T^4 = (8280)^4 = 4.70\times10^{15}$,
$P = \sigma AT^4 = 5.67\times10^{-8}\times6.16\times10^{18}\times4.70\times10^{15}
= 1.6\times10^{27}\ \text{W}$.
:::

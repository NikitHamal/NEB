---
subject: Physics
grade: CEE
unit: 4
title: Fluid Statics and Dynamics
hours: 1
area: Mechanics
---

Fluids — liquids and gases — carry the blood in our arteries, the water in our
pipes and the air over an aeroplane wing. Of the **10 Mechanics questions**
(official weightage), we estimate about **1** comes from this chapter. It is a
formula-rich chapter, so the question is usually a quick ratio: how a capillary rise,
a terminal velocity or a flow rate changes when a radius changes, an excess pressure
inside a bubble, or a speed or pressure from the continuity and Bernoulli equations.

::: key What the paper asks from this chapter
- $P = P_0 + h\rho g$; Pascal's law and the hydraulic lift; floating and Archimedes' principle.
- Surface tension $T = F/l$ and surface energy (same number, J m⁻² = N m⁻¹); effect of temperature and impurities.
- Excess pressure $2T/r$ in a drop or an air bubble, $4T/r$ in a soap bubble; work to make a film counts both surfaces.
- Capillary rise $h = 2T\cos\theta/(r\rho g)$: $h \propto 1/r$; angle of contact; mercury is depressed.
- Viscosity: $F = \eta A\,dv/dx$; Stokes' law $6\pi\eta rv$; terminal velocity $\propto r^2$; Poiseuille $Q \propto r^4$.
- Continuity $A_1v_1 = A_2v_2$; Bernoulli $P + \frac{1}{2}\rho v^2 + \rho gh$ = constant; Torricelli $v = \sqrt{2gh}$; lift, venturi, atomiser.
:::

## 4.1 Pressure in a fluid; surface tension, surface energy and capillary action

### Pressure in a fluid at rest

**Pressure** is the normal force per unit area: $P = F/A$. It is a scalar; SI unit
pascal (1 Pa = 1 N m⁻²), dimensions $[ML^{-1}T^{-2}]$. Other units:
1 atm = 1.013 × 10⁵ Pa = 76 cm of mercury = 760 torr; 1 bar = 10⁵ Pa;
1 mm Hg ≈ 133 Pa (blood pressure of 120 mm Hg is about 16 kPa above atmospheric).

In a fluid at rest:

1. pressure at a point acts **equally in all directions**;
2. pressure is the **same at all points at the same level** in a connected body of the
   same liquid;
3. pressure increases with depth: at depth $h$ below the free surface
   $P = P_0 + h\rho g$, where $P_0$ is the atmospheric pressure. $h\rho g$ alone is the
   **gauge pressure**; $P$ is the **absolute pressure**;
4. pressure at the bottom does **not** depend on the shape or the cross-section of the
   vessel, only on the depth (the *hydrostatic paradox*).

The atmosphere supports a column of 76 cm of mercury, or about 10.3 m of water.

::: definition Pascal's law
A pressure applied to an enclosed fluid is transmitted undiminished to every part of
the fluid and to the walls of the container.
:::

In a **hydraulic lift, press or brake**, a small force $F_1$ on a small piston $A_1$
gives a large force $F_2 = F_1A_2/A_1$ on a large piston — but the large piston moves
a correspondingly smaller distance, so no work is gained.

**Archimedes' principle:** a body wholly or partly immersed in a fluid feels an
upward **buoyant force (upthrust)** equal to the weight of the fluid it displaces.
A floating body displaces its own weight of fluid, so the fraction of its volume
submerged is $\rho_{body}/\rho_{fluid}$ (ice, 917 kg m⁻³, floats about nine-tenths
submerged in fresh water). Relative density = weight in air / loss of weight in
water.

::: example Worked example 4.1 — a diver and a hydraulic lift
**Problem.** (a) Find the absolute pressure on a diver 10 m below the surface of
Phewa Lake ($P_0 = 1.01\times10^5$ Pa, $\rho = 1000$ kg m⁻³, $g = 9.8$ m s⁻²).
(b) The pistons of a car-service lift have areas 10 cm² and 1000 cm². What force
on the small piston lifts a 2000 kg car?

**Solution.** (a) $P = 1.01\times10^5 + 1000(9.8)(10) = 1.99\times10^5$ Pa — about
2 atm: every 10 m of water adds roughly one atmosphere.
(b) $F_1 = F_2A_1/A_2 = 2000(9.8)/100 = 196$ N.
:::

### Surface tension

Molecules attract one another over a very short **molecular range** (about
10⁻⁹ m). A molecule deep in a liquid is pulled equally on all sides; a molecule in the
surface is pulled **inward** only. The surface therefore behaves like a stretched
elastic membrane and tends to **contract to the least area** — which is why free
drops and bubbles are spherical (a sphere has the least surface for a given volume),
why a greased needle can float on water, and why wet hairs of a paint brush cling
together.

Attraction between like molecules is **cohesion**; between unlike molecules (liquid
and solid), **adhesion**.

::: definition Surface tension
The **surface tension** $T$ of a liquid is the force per unit length acting on an
imaginary line drawn in the liquid surface, perpendicular to the line and tangential
to the surface: $T = F/l$. SI unit N m⁻¹; dimensions $[MT^{-2}]$.
:::

**Surface energy.** To increase the area of a surface, molecules must be brought up
from the interior against the inward pull, so work is needed. The work done per unit
increase in surface area (at constant temperature) is the **surface energy**, and it
is numerically equal to the surface tension: $W = T\,\Delta A$ (1 J m⁻² = 1 N m⁻¹).

| Situation | Change of area to use in $W = T\Delta A$ |
|---|---|
| Liquid drop of radius $r$ (one surface) | $4\pi r^2$ |
| Soap bubble of radius $r$ (two surfaces, inside and outside) | $2\times4\pi r^2 = 8\pi r^2$ |
| Soap film on a frame, area increased by $\Delta A$ | $2\Delta A$ |
| Drop of radius $R$ split into $n$ equal droplets | $4\pi R^2(n^{1/3} - 1)$ — energy must be supplied |

When small drops merge into one big drop the total area falls and energy is
**released** (the big drop is slightly warmer).

**Excess pressure** inside a curved surface (the inside of the curve is at the higher
pressure):

| Surface | Excess pressure |
|---|---|
| Liquid drop, or air bubble inside a liquid (one surface) | $\Delta P = \frac{2T}{r}$ |
| Soap bubble in air (two surfaces) | $\Delta P = \frac{4T}{r}$ |

The **smaller** the bubble, the **larger** the excess pressure. Two soap bubbles of
different sizes joined by a tube: air flows from the smaller into the larger, so the
small one shrinks and the large one grows.

**What changes surface tension.**

| Factor | Effect on $T$ |
|---|---|
| Rise in temperature | decreases (almost linearly); zero at the critical temperature |
| Highly soluble impurity (common salt in water) | increases slightly |
| Sparingly soluble or surface-active impurity (soap, detergent, phenol) | decreases strongly |
| Oil or grease film on water | decreases (oil spread on ponds kills mosquito larvae, which can no longer hang from the surface) |

Detergents lower the surface tension of water so that it spreads into and wets the
fine gaps of cloth; hot soapy water washes better than cold, plain water.

### Angle of contact and capillary action

::: definition Angle of contact
The **angle of contact** is the angle between the tangent to the liquid surface at
the point of contact and the solid surface, measured **inside the liquid**.
:::

| | Pure water and clean glass | Mercury and glass |
|---|---|---|
| Angle of contact | acute, nearly 0° (often quoted as about 8°) | obtuse, about 140° |
| Adhesion vs cohesion | adhesion > cohesion | cohesion > adhesion |
| Wets the glass? | yes | no |
| Meniscus | concave (curves up at the walls) | convex (curves down at the walls) |
| In a capillary tube | **rises** | is **depressed** |

At exactly 90° (water on silver) there is neither rise nor fall.

**Capillarity** is the rise or fall of a liquid in a tube of very fine bore. Balancing
the upward surface-tension pull around the rim, $2\pi rT\cos\theta$, against the weight
of the raised column, $\pi r^2h\rho g$ (Jurin's law):

$$ h = \frac{2T\cos\theta}{r\rho g} $$

So $h \propto 1/r$ ($hr$ = constant for a given liquid): halve the bore and the
liquid rises twice as high. For $\theta > 90^{\circ}$, $\cos\theta < 0$ and $h$ is
negative (depression).

```figure caption="Capillary action. Water wets glass ($\theta < 90^{\circ}$): concave meniscus, the column rises by h. Mercury does not ($\theta > 90^{\circ}$): convex meniscus, the column is pushed down."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,3.2))
def panel(x0, col, inner, convex, title):
    lev = 1.5; xc = x0 + 2.0; w = 0.22
    ax.add_patch(Rectangle((x0+0.3, 0), 3.4, lev, color=col, alpha=0.45, lw=0, zorder=1))
    xs = np.linspace(xc-w, xc+w, 50)
    s = ((xs-xc)/w)**2
    men = inner + (0.16 - 0.16*s if convex else -0.16 + 0.16*s)
    ax.add_patch(Rectangle((xc-w, 0.55), 2*w, max(lev, inner+0.3)-0.55, color='white', lw=0, zorder=2))
    ax.fill_between(xs, 0.55, men, color=col, alpha=0.45, lw=0, zorder=3)
    for xx in (xc-w, xc+w):
        ax.plot([xx, xx], [0.55, 3.6], color=INK, lw=1.2, zorder=4)
    ax.plot([x0+0.3, x0+0.3, x0+3.7, x0+3.7], [2.3, 0, 0, 2.3], color=INK, lw=1.2, zorder=4)
    ax.plot(xs, men, color=INK, lw=1.0, zorder=4)
    ax.plot([x0+0.3, xc-w], [lev, lev], color=INK, lw=0.6, zorder=4)
    ax.plot([xc+w, x0+3.7], [lev, lev], color=INK, lw=0.6, zorder=4)
    top = inner + (0 if convex else -0.16) if not convex else inner + 0.16
    xa = xc + 0.75
    ax.plot([xc+w+0.05, xa+0.15], [top, top], color=MUTED, lw=0.7, ls=':', zorder=4)
    ax.annotate('', xy=(xa, top), xytext=(xa, lev), arrowprops=dict(arrowstyle='<->', color='#A8271F', lw=1.0, shrinkA=0, shrinkB=0), zorder=5)
    ax.text(xa+0.12, (top+lev)/2, 'h', color='#A8271F', fontsize=10, va='center')
    ax.text(xc, 3.95, title, ha='center', va='bottom', fontsize=8.5, color=INK)
panel(0.0, ACCENT, 2.95, False, 'water: concave, rises')
panel(4.6, MUTED, 0.95, True, 'mercury: convex, depressed')
ax.set_xlim(-0.1, 8.9); ax.set_ylim(-0.1, 4.4); ax.set_aspect('equal'); ax.axis('off')
```

**Applications.** Oil rises in a lamp wick; ink in blotting paper; water in a towel
and in the soil (ploughing breaks the fine soil capillaries and keeps moisture from
reaching the surface and evaporating); surface tension and capillarity help move
water in the xylem of plants.

::: caution A capillary tube never overflows
If the tube above the water is shorter than $h$, the water rises to the top and
stops — it does **not** spill over like a fountain. The meniscus flattens instead:
its radius of curvature $R$ grows so that $hR$ stays constant. In a freely falling
lift ($g_{eff} = 0$) water rises to fill the whole length of any capillary.
:::

::: example Worked example 4.2 — capillary rise and bubbles
**Problem.** (a) Water ($T = 0.07$ N m⁻¹, $\theta = 0^{\circ}$) stands in a glass
capillary of internal diameter 0.5 mm. Find the rise ($g = 9.8$ m s⁻²). (b) Find the
excess pressure inside a soap bubble of radius 2 cm, and the work done in blowing a
bubble of radius 1 cm, for a soap solution with $T = 0.03$ N m⁻¹.

**Solution.** (a) $r = 0.25$ mm:
$h = \frac{2(0.07)}{(0.25\times10^{-3})(1000)(9.8)} = 0.057$ m $= 5.7$ cm.
(b) $\Delta P = 4T/r = 4(0.03)/0.02 = 6$ Pa. Work $= T\times8\pi r^2 = 0.03\times8\pi\times10^{-4} = 7.5\times10^{-5}$ J.
:::

## 4.2 Viscosity: Newton's law of viscous flow, Stokes' law and terminal velocity, Poiseuille's formula

### Viscosity and Newton's law

In **streamline (laminar)** flow a liquid moves in layers that slide over one another:
the layer touching a fixed surface is at rest, and the speed increases layer by layer
away from it. **Viscosity** is the property of a fluid by which it opposes the
relative motion between its adjacent layers — internal friction of the fluid.

::: definition Newton's law of viscous flow
The tangential viscous force between two layers is proportional to the area $A$ of
the layers and to the **velocity gradient** $dv/dx$ (rate of change of velocity with
distance perpendicular to the flow): $F = \eta A\frac{dv}{dx}$. The constant $\eta$ is
the **coefficient of viscosity**. SI unit N s m⁻² = Pa s (sometimes called the
decapoise); CGS unit the poise; 1 Pa s = 10 poise. Dimensions $[ML^{-1}T^{-1}]$.
:::

| | Liquids | Gases |
|---|---|---|
| Origin of viscosity | cohesive forces between molecules | transfer of momentum by molecules moving between layers |
| On heating | viscosity **decreases** (honey and engine oil run more freely) | viscosity **increases** |

Viscosity is different from density: honey is far more viscous than mercury, though
much less dense. Blood is about three to four times as viscous as water.

**Reynolds number** $R_e = \rho vD/\eta$ (dimensionless) decides the type of flow in a
pipe of diameter $D$: small values (below about 2000) mean laminar flow, large values
turbulent flow. The speed at which laminar flow breaks down is the **critical
velocity** $v_c = R_e\eta/(\rho D)$ — high for thick, viscous liquids in narrow tubes.

### Stokes' law and terminal velocity

::: definition Stokes' law
A small sphere of radius $r$ moving slowly with speed $v$ through a viscous fluid of
viscosity $\eta$ feels a viscous drag $F = 6\pi\eta rv$.
:::

It holds for a small, smooth, rigid sphere, moving slowly (streamline flow) through a
uniform fluid of large extent. Dimensional check: $[ML^{-1}T^{-1}][L][LT^{-1}] = [MLT^{-2}]$.

A sphere of density $\rho$ dropped in a fluid of density $\sigma$ accelerates until the
drag plus the upthrust balance its weight. Then it falls at a constant **terminal
velocity**:

$$ \frac{4}{3}\pi r^3\rho g = \frac{4}{3}\pi r^3\sigma g + 6\pi\eta rv_t \quad\Rightarrow\quad v_t = \frac{2r^2(\rho - \sigma)g}{9\eta} $$

- $v_t \propto r^2$: double the radius, four times the terminal velocity.
- If $\sigma > \rho$ (an air bubble in water), $v_t$ is negative: the body rises at a
  steady speed.
- Tiny water droplets in clouds and fog have very small $v_t$, so they seem to float;
  a parachute has a small terminal velocity because its drag is large.
- Uses: Millikan's oil-drop experiment (Chapter 18); measuring the viscosity of
  oils; settling (sedimentation) of particles. In medicine, the **erythrocyte
  sedimentation rate (ESR)** is the rate at which red cells settle in a column of
  blood — clumped cells behave as larger spheres and settle faster.

```figure caption="Speed of a small sphere dropped into a viscous liquid. It accelerates at first, but the drag $6\pi\eta rv$ grows with speed until the net force is zero; after that it falls at the terminal velocity $v_t$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.6))
t = np.linspace(0, 5, 300); vt = 1.0
v = vt*(1 - np.exp(-t/0.8))
ax.plot(t, v, color=ACCENT, lw=2.0)
ax.axhline(vt, color='#A8271F', lw=1.0, ls=(0, (4, 2)))
ax.text(4.9, vt + 0.04, 'terminal velocity  $v_t$', color='#A8271F', fontsize=8.5, ha='right', va='bottom')
ax.plot([0, 0.8], [0, 1.0], color=MUTED, lw=0.9, ls=':')
ax.annotate('initial slope = g(1 − σ/ρ)', xy=(0.45, 0.55), xytext=(1.25, 0.32), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.text(3.2, 0.62, 'weight = upthrust + drag', fontsize=8.5, color=MUTED, ha='center')
ax.set_xlim(0, 5); ax.set_ylim(0, 1.3)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel('time  t'); ax.set_ylabel('speed  v')
ax.spines[['top','right']].set_visible(False)
```

::: example Worked example 4.3 — why clouds float
**Problem.** Find the terminal velocity of a cloud droplet of radius 10 μm falling
through air ($\eta = 1.8\times10^{-5}$ Pa s, density of water 1000 kg m⁻³; neglect the
density of air; $g = 9.8$ m s⁻²). How fast would a droplet of radius 30 μm fall?

**Solution.** $v_t = \frac{2(10^{-5})^2(1000)(9.8)}{9(1.8\times10^{-5})} = 1.2\times10^{-2}$ m s⁻¹
— about 1 cm per second, so air currents easily hold it up. Three times the radius
gives $3^2 = 9$ times the speed: about 11 cm s⁻¹.
:::

### Poiseuille's formula

For steady laminar flow of a liquid through a narrow horizontal tube of radius $r$ and
length $l$, with a pressure difference $P$ between its ends, the **volume of liquid
flowing per second** is

$$ Q = \frac{\pi Pr^4}{8\eta l} $$

The formula can be checked (apart from the $\pi/8$) by dimensions. The key is the
**fourth power** of the radius: halve the radius and the flow drops to $\frac{1}{16}$.
Writing $Q = P/R$, the tube has a **fluid resistance** $R = \frac{8\eta l}{\pi r^4}$;
tubes in series add resistances and tubes in parallel add flows, exactly like
electrical resistors.

::: example Worked example 4.4 — a narrowed artery
**Problem.** Fatty deposits reduce the radius of an artery by 20 %. For the same
pressure difference, by what factor does the blood flow fall? By what factor must the
pressure difference rise to restore the flow?

**Solution.** $Q \propto r^4$: $0.8^4 = 0.41$, so the flow falls to 41 % of normal. To
restore it, $P$ must rise by $1/0.41 \approx 2.4$ times — one reason narrowed
arteries raise blood pressure and load the heart.
:::

## 4.3 Equation of continuity and Bernoulli's principle with applications

An **ideal fluid** is incompressible and non-viscous, and its flow is steady and
irrotational. In **steady (streamline) flow** the velocity at each point does not
change with time; the path of a fluid particle is a **streamline**, the tangent to it
gives the velocity there, and two streamlines never cross. Crowded streamlines mean
fast flow.

### Equation of continuity

For an incompressible fluid flowing steadily through a tube, the mass (and volume)
entering one end per second equals that leaving the other:

$$ A_1v_1 = A_2v_2 = Q \ \ \text{(constant)} $$

$Q$ is the volume flow rate (m³ s⁻¹). Where the tube is **narrow, the flow is fast**:
water speeds up through the rapids of a gorge and out of a nozzle; a thumb over the
end of a hose makes the jet fly farther. It is the law of **conservation of mass**.
In the body, the total cross-section of all the capillaries is far larger than that
of the aorta, so blood moves much more **slowly** in the capillaries — giving time for
exchange with the tissues.

### Bernoulli's principle

::: definition Bernoulli's theorem
For the steady flow of an ideal fluid, the sum of the pressure, the kinetic energy per
unit volume and the potential energy per unit volume is the same at every point of a
streamline:
$P + \frac{1}{2}\rho v^2 + \rho gh = $ constant.
:::

Dividing by $\rho g$: $\frac{P}{\rho g} + \frac{v^2}{2g} + h$ = constant — the sum of the
**pressure head**, **velocity head** and **gravitational head**. Bernoulli's theorem
is the law of **conservation of energy** for a moving fluid. In a horizontal pipe it
says: **where the speed is high, the pressure is low.**

```figure caption="A venturi tube. The flow is faster in the narrow throat (continuity), so the pressure there is lower (Bernoulli) — the liquid in the middle pressure tube stands lower."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
x = np.linspace(0, 10, 400)
half = 1.0 - 0.55*np.exp(-((x-5.0)/1.1)**2)
ax.fill_between(x, -half, half, color=ACCENT, alpha=0.14, lw=0)
ax.plot(x, half, color=INK, lw=1.3); ax.plot(x, -half, color=INK, lw=1.3)
for xp, hgt in [(1.8, 2.1), (5.0, 0.9), (8.2, 1.85)]:
    top = 1.0 - 0.55*np.exp(-((xp-5.0)/1.1)**2)
    ax.plot([xp-0.15, xp-0.15], [top, 3.4], color=INK, lw=1.0)
    ax.plot([xp+0.15, xp+0.15], [top, 3.4], color=INK, lw=1.0)
    ax.fill_between([xp-0.15, xp+0.15], top, top+hgt, color=ACCENT, alpha=0.45, lw=0)
for yy in (0.35, -0.35):
    ax.annotate('', xy=(3.2, yy), xytext=(0.4, yy), arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.annotate('', xy=(6.4, 0.0), xytext=(4.0, 0.0), arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.6, mutation_scale=11))
ax.text(1.8, -1.35, 'wide: A₁, v₁ slow,\nP₁ high', fontsize=8.5, ha='center', va='top', color=INK)
ax.text(5.0, -1.35, 'throat: A₂, v₂ fast,\nP₂ low', fontsize=8.5, ha='center', va='top', color='#A8271F')
ax.text(8.2, -1.35, 'wide again:\nP nearly recovers', fontsize=8.5, ha='center', va='top', color=INK)
ax.set_xlim(-0.2, 10.2); ax.set_ylim(-2.4, 3.6); ax.axis('off')
```

**Applications.**

| Device or effect | How Bernoulli and continuity explain it |
|---|---|
| **Venturimeter** | the pressure drop between the wide part and the throat gives the flow speed: $P_1 - P_2 = \frac{1}{2}\rho(v_2^2 - v_1^2)$ with $A_1v_1 = A_2v_2$ |
| **Torricelli's theorem** | liquid leaves a hole at depth $h$ below the free surface of a wide open tank with speed $v = \sqrt{2gh}$ — the speed of a free fall from that height |
| **Lift on an aeroplane wing** (aerofoil) | air flows faster over the curved upper surface, so the pressure above is lower than below |
| Roofs lifted off in a storm | fast wind over the roof lowers the pressure above it; the still air inside pushes up |
| Two boats or trains moving side by side | fast flow in the narrow gap lowers the pressure there; they are pushed together |
| Atomiser, sprayer, Bunsen burner, carburettor | a fast jet past the top of a tube lowers the pressure there and draws the liquid (or air) in |
| Swing of a spinning ball (Magnus effect) | the spin makes the air faster on one side; the ball is pushed toward the low-pressure side |

Jet from a hole: for a tank filled to height $H$ with a hole at depth $h$ below the
surface, the jet lands at a horizontal distance $R = 2\sqrt{h(H - h)}$ from the foot of
the tank — greatest ($R = H$) for a hole halfway down, and the same for holes at
depths $h$ and $H - h$.

::: example Worked example 4.5 — venturi and Torricelli
**Problem.** (a) Water flows through a horizontal pipe whose cross-section narrows
from 4 cm² to 1 cm². The speed in the wide part is 1 m s⁻¹. Find the speed in the
narrow part and the pressure difference. (b) Water stands 5 m above a small hole in
the side of a large open tank. Find the speed of efflux ($g = 10$ m s⁻²).

**Solution.** (a) $v_2 = A_1v_1/A_2 = 4$ m s⁻¹;
$P_1 - P_2 = \frac{1}{2}(1000)(4^2 - 1^2) = 7500$ Pa (a water column of about 0.77 m).
(b) $v = \sqrt{2gh} = \sqrt{100} = 10$ m s⁻¹.
:::

::: caution Continuity uses area, area uses the square of the diameter
A pipe narrowing from 4 cm to 2 cm **diameter** has one quarter of the area, so the
speed becomes **four** times, not two. And in Bernoulli's equation use $v^2$: doubling
the speed quadruples the kinetic-energy term.
:::

::: tip Ratio problems in this chapter
Learn the power of $r$ in each formula and most questions are one line:
capillary rise $h \propto r^{-1}$; excess pressure $\propto r^{-1}$; Stokes' drag
$\propto r$; terminal velocity $\propto r^2$; Poiseuille flow $\propto r^4$;
speed in a pipe $\propto r^{-2}$ (continuity).
:::

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Pressure | $P = F/A$; $P = P_0 + h\rho g$; 1 atm = 1.013 × 10⁵ Pa = 76 cm Hg |
| Pascal's law | $F_2/F_1 = A_2/A_1$ (hydraulic lift, brakes) |
| Archimedes | upthrust = weight of fluid displaced; floating: fraction submerged $= \rho_{body}/\rho_{fluid}$ |
| Surface tension | $T = F/l$ (N m⁻¹, $[MT^{-2}]$) = surface energy per unit area (J m⁻²) |
| Work on surfaces | drop $T\cdot4\pi r^2$; soap bubble $T\cdot8\pi r^2$; splitting into $n$ drops $4\pi R^2T(n^{1/3} - 1)$ |
| Excess pressure | drop or air bubble in liquid $2T/r$; soap bubble $4T/r$ |
| Capillary rise | $h = 2T\cos\theta/(r\rho g)$; $hr$ constant; mercury ($\theta \approx 140^{\circ}$) depressed |
| Effect of temperature | $T$ falls; viscosity of liquids falls, of gases rises |
| Newton's law of viscosity | $F = \eta A\,dv/dx$; $\eta$ in Pa s ($[ML^{-1}T^{-1}]$); 1 Pa s = 10 poise |
| Stokes' law | $F = 6\pi\eta rv$ |
| Terminal velocity | $v_t = 2r^2(\rho - \sigma)g/9\eta$; $\propto r^2$ |
| Poiseuille | $Q = \pi Pr^4/(8\eta l)$; $\propto r^4$; resistance $8\eta l/\pi r^4$ |
| Reynolds number | $R_e = \rho vD/\eta$; low → laminar, high → turbulent |
| Continuity | $A_1v_1 = A_2v_2$ (mass conservation) |
| Bernoulli | $P + \frac{1}{2}\rho v^2 + \rho gh$ = constant (energy conservation) |
| Torricelli | $v = \sqrt{2gh}$; jet range $2\sqrt{h(H - h)}$, maximum $H$ at $h = H/2$ |
| Venturi | $P_1 - P_2 = \frac{1}{2}\rho(v_2^2 - v_1^2)$ |

## Chapter summary

- Pressure in a liquid is $P_0 + h\rho g$, the same at one level, independent of the
  vessel's shape; Pascal's law multiplies force in a hydraulic lift; upthrust equals
  the weight of fluid displaced.
- Surface tension (N m⁻¹) equals surface energy per unit area (J m⁻²); it falls with
  temperature and with soap or detergent; a soap film has two surfaces.
- Excess pressure is $2T/r$ in a drop and $4T/r$ in a soap bubble — the smaller the
  bubble, the higher the pressure.
- Capillary rise $h = 2T\cos\theta/(r\rho g)$: liquids that wet glass (acute angle,
  concave meniscus) rise; mercury (obtuse, convex) is depressed; a short tube never
  overflows.
- Viscous force $F = \eta A\,dv/dx$; viscosity of liquids falls and of gases rises on
  heating; SI unit Pa s.
- Stokes' drag $6\pi\eta rv$ leads to the terminal velocity $2r^2(\rho - \sigma)g/9\eta$,
  proportional to $r^2$.
- Poiseuille's flow $Q = \pi Pr^4/8\eta l$ depends on the fourth power of the radius.
- Continuity $A_1v_1 = A_2v_2$ and Bernoulli $P + \frac{1}{2}\rho v^2 + \rho gh$ =
  constant: faster flow means lower pressure — venturimeter, Torricelli's
  $\sqrt{2gh}$, wing lift, atomisers.

## Practice questions

**Set A — Recall (21 questions)**

1. The SI unit of pressure, the pascal, is equal to
   (a) N m (b) N m⁻² (c) N m⁻¹ (d) N m²
2. The pressure at a depth h in a liquid of density ρ, whose surface is open to an atmospheric pressure $P_0$, is
   (a) $h\rho g$ (b) $P_0 - h\rho g$ (c) $P_0 + h\rho g$ (d) $P_0/h\rho g$
3. A hydraulic lift works on the principle of
   (a) Bernoulli's theorem (b) Archimedes' principle (c) Stokes' law (d) Pascal's law
4. The dimensional formula of surface tension is
   (a) [MT⁻²] (b) [MLT⁻²] (c) [ML⁻¹T⁻²] (d) [ML²T⁻²]
5. When the temperature of a liquid rises, its surface tension
   (a) increases (b) decreases (c) stays the same (d) first increases and then decreases
6. The excess pressure inside a soap bubble of radius r made from a solution of surface tension T is
   (a) $2T/r$ (b) $T/r$ (c) $4T/r$ (d) $8T/r$
7. The angle of contact between mercury and clean glass is
   (a) zero (b) acute (c) exactly 90° (d) obtuse
8. A liquid rises in a glass capillary tube when the angle of contact is
   (a) acute (b) obtuse (c) 90° (d) 180°
9. For a given liquid, the height of capillary rise h and the radius r of the tube are related by
   (a) $h \propto r$ (b) $h \propto r^{2}$ (c) $h \propto 1/r^{2}$ (d) $h \propto 1/r$
10. The SI unit of the coefficient of viscosity is
   (a) poise (b) Pa s (c) N s m (d) N m⁻² s⁻¹
11. According to Stokes' law, the viscous drag on a sphere of radius r moving with speed v through a fluid of viscosity η is
   (a) $6\pi\eta rv$ (b) $6\pi\eta r^{2}v$ (c) $4\pi\eta rv$ (d) $6\pi\eta v/r$
12. The terminal velocity of a small sphere falling through a viscous liquid is proportional to
   (a) r (b) $r^{3}$ (c) $r^{2}$ (d) 1/r
13. According to Poiseuille's formula, the volume of liquid flowing per second through a narrow tube is proportional to
   (a) $r^{4}$ (b) $r^{2}$ (c) $r^{3}$ (d) r
14. When a gas is heated, its viscosity
   (a) decreases (b) increases (c) does not change (d) becomes zero
15. The equation of continuity for fluid flow follows from the conservation of
   (a) energy (b) momentum (c) mass (d) angular momentum
16. Bernoulli's theorem is a statement of the conservation of
   (a) energy (b) mass (c) momentum (d) volume
17. Liquid flows out of a small hole at depth h below the free surface of a large open tank with a speed of
   (a) $gh$ (b) $\sqrt{gh}$ (c) $2gh$ (d) $\sqrt{2gh}$
18. A venturimeter is used to measure
   (a) the surface tension of a liquid (b) the rate of flow of a liquid in a pipe (c) the viscosity of a liquid (d) atmospheric pressure
19. The surface energy per unit area of a liquid surface is numerically equal to its
   (a) viscosity (b) surface tension (c) density (d) vapour pressure
20. The dimensional formula of the coefficient of viscosity is
   (a) [MLT⁻¹] (b) [ML⁻¹T⁻²] (c) [ML⁻¹T⁻¹] (d) [ML²T⁻¹]
21. Small free drops of a liquid are spherical because of
   (a) viscosity (b) gravity (c) buoyancy (d) surface tension

::: note Answers and explanations — Set A
**1.** (b) — pressure is force per unit area: 1 Pa = 1 N m⁻². N m⁻¹ is the unit of surface tension.
**2.** (c) — the atmosphere presses on the surface and the liquid column adds $h\rho g$; $h\rho g$ alone is the gauge pressure.
**3.** (d) — the pressure applied at the small piston is transmitted undiminished to the large one, so $F_2 = F_1A_2/A_1$.
**4.** (a) — $T = F/l$: $[MLT^{-2}]/[L] = [MT^{-2}]$. (c) is pressure.
**5.** (b) — surface tension falls (almost linearly) with temperature and vanishes at the critical temperature.
**6.** (c) — a soap bubble has two surfaces, so the excess pressure is $2\times2T/r = 4T/r$. $2T/r$ is for a drop or an air bubble inside a liquid.
**7.** (d) — about 140°: mercury does not wet glass, its meniscus is convex and it is depressed in a capillary.
**8.** (a) — with $\theta < 90^{\circ}$, $\cos\theta > 0$ and $h = 2T\cos\theta/(r\rho g)$ is positive.
**9.** (d) — Jurin's law: $h = 2T\cos\theta/(r\rho g)$, so $hr$ is constant.
**10.** (b) — $\eta = F/(A\,dv/dx)$ has unit N s m⁻² = Pa s. The poise is the CGS unit (1 Pa s = 10 poise).
**11.** (a) — Stokes' law, $F = 6\pi\eta rv$, valid for small spheres in slow (streamline) motion.
**12.** (c) — $v_t = 2r^2(\rho - \sigma)g/9\eta$: weight and upthrust go as $r^3$, drag as $rv$, so $v \propto r^2$.
**13.** (a) — $Q = \pi Pr^4/(8\eta l)$; the fourth power is the point examiners test.
**14.** (b) — gas viscosity comes from molecules carrying momentum between layers; faster molecules at higher temperature carry more. Liquids behave oppositely.
**15.** (c) — what enters a tube per second must leave it: $\rho A_1v_1 = \rho A_2v_2$.
**16.** (a) — $P$, $\frac{1}{2}\rho v^2$ and $\rho gh$ are energies per unit volume; their sum stays constant.
**17.** (d) — Torricelli's theorem: the efflux speed equals the speed of free fall through the height $h$.
**18.** (b) — the pressure difference between its wide part and its throat gives the flow speed and hence the rate of flow.
**19.** (b) — surface energy (J m⁻²) and surface tension (N m⁻¹) have the same dimensions and the same numerical value.
**20.** (c) — $\eta = F/(A\,dv/dx)$: $[MLT^{-2}]/([L^2][T^{-1}]) = [ML^{-1}T^{-1}]$.
**21.** (d) — surface tension makes the surface contract to the least area, and a sphere has the least area for its volume.
:::

**Set B — Understanding (14 questions)**

1. Water rises 6 cm in a capillary tube, but only 4 cm of the tube is above the water surface. The water
   (a) overflows from the top in a fountain (b) rises to 4 cm and its meniscus becomes flatter (c) does not rise at all (d) rises to 4 cm and its meniscus becomes more curved
2. A capillary tube stands in water inside a freely falling lift. The water in the tube
   (a) does not rise at all (b) rises to the same height as on the ground (c) rises to half the usual height (d) rises to fill the whole length of the tube
3. Two soap bubbles of radii 1 cm and 2 cm are joined by a narrow tube. Air then flows
   (a) from the smaller bubble into the larger (b) from the larger bubble into the smaller (c) in neither direction (d) back and forth until the sizes are equal
4. The radius of a capillary tube is halved. The height to which water rises in it becomes
   (a) half (b) one quarter (c) twice (d) four times
5. The radius of a narrow tube is halved while the pressure difference and length stay the same. The rate of flow of water through it becomes
   (a) one half (b) one quarter (c) one eighth (d) one sixteenth
6. Water flows through a horizontal pipe from a wide section into a narrow section. In the narrow section
   (a) the speed is higher and the pressure is lower (b) the speed and the pressure are both higher (c) the speed is lower and the pressure is higher (d) the speed and the pressure are both lower
7. Many tiny mercury droplets merge to form one big drop. In this process
   (a) energy is absorbed and the drop cools (b) energy is released and the drop warms slightly (c) no energy change takes place (d) the surface area increases
8. Soap or detergent helps water to clean greasy clothes mainly because it
   (a) increases the surface tension of water (b) increases the viscosity of water (c) lowers the surface tension of water (d) raises the boiling point of water
9. A small steel ball falls through glycerine with terminal velocity v. A ball of the same steel with twice the radius would have a terminal velocity of
   (a) 2v (b) v/2 (c) 8v (d) 4v
10. During a storm, the roof of a house is lifted off. This happens because
   (a) the fast wind above the roof lowers the pressure there (b) the wind raises the pressure above the roof (c) the air inside the house heats up (d) the roof becomes lighter when wet
11. Honey flows much more easily when it is warmed because
   (a) its density increases (b) its surface tension increases (c) its viscosity decreases (d) its viscosity increases
12. Blood flows more slowly in the capillaries than in the aorta because
   (a) the capillaries are narrower than the aorta (b) the total cross-sectional area of all the capillaries is much larger than that of the aorta (c) blood is more viscous in the capillaries (d) the pressure in the capillaries is higher
13. Ice of density 900 kg m⁻³ floats in water of density 1000 kg m⁻³. The fraction of its volume above the water surface is
   (a) 9/10 (b) 1/9 (c) 1/10 (d) 1/2
14. An air bubble released at the bottom of a pond of water rises
   (a) with constant acceleration g (b) with ever-increasing speed (c) only if the water is hot (d) at a terminal velocity, since its density is less than that of water

::: note Answers and explanations — Set B
**1.** (b) — a capillary never overflows; the water stops at the top and the meniscus radius grows ($hR$ constant), so the meniscus becomes flatter.
**2.** (d) — in free fall the effective $g$ is zero, so nothing pulls the column down: $h = 2T\cos\theta/(r\rho g)$ grows without limit and the water fills the tube.
**3.** (a) — excess pressure $4T/r$ is greater in the smaller bubble, so air is pushed into the larger one; the small bubble shrinks further.
**4.** (c) — $h \propto 1/r$: half the radius gives twice the rise.
**5.** (d) — Poiseuille: $Q \propto r^4$; $(1/2)^4 = 1/16$.
**6.** (a) — continuity: smaller area, higher speed; Bernoulli (horizontal pipe): higher speed, lower pressure.
**7.** (b) — the total surface area decreases, so surface energy is released as heat and the drop warms slightly.
**8.** (c) — lowering the surface tension lets water spread into and wet the fine gaps of the cloth and lift off the grease.
**9.** (d) — $v_t \propto r^2$: twice the radius, four times the terminal velocity. (c) uses $r^3$ (the weight alone).
**10.** (a) — Bernoulli: fast-moving air above has lower pressure than the still air inside, so there is a net upward force on the roof.
**11.** (c) — the viscosity of a liquid falls quickly with rising temperature; density hardly changes.
**12.** (b) — continuity applies to the total flow: $A_{total}v$ is the same, and the capillaries together have a far larger cross-section, so $v$ is smaller. A single narrow tube (a) would give faster flow.
**13.** (c) — fraction submerged $= 900/1000 = 9/10$, so one-tenth is above the surface. (a) is the submerged fraction.
**14.** (d) — Stokes' law gives a terminal velocity with $\rho - \sigma$ negative, so the bubble moves **up** at a steady speed once the drag balances the net upthrust.
:::

**Set C — Application (12 questions)**

1. The absolute pressure 10 m below the surface of a lake is ($P_0 = 1.01 \times 10^{5}$ Pa, $\rho$ = 1000 kg m⁻³, g = 9.8 m s⁻²)
   (a) 0.98 × 10⁵ Pa (b) 1.99 × 10⁵ Pa (c) 1.01 × 10⁵ Pa (d) 2.98 × 10⁵ Pa
2. The pistons of a hydraulic lift have areas of 10 cm² and 1000 cm². The force on the small piston needed to lift a 2000 kg car (g = 9.8 m s⁻²) is
   (a) 196 N (b) 19.6 N (c) 1960 N (d) 1.96 × 10⁶ N
3. Water (surface tension 0.072 N m⁻¹, angle of contact 0°) rises in a glass capillary of radius 0.1 mm. The height of rise is about (g = 9.8 m s⁻²)
   (a) 1.5 cm (b) 7.3 cm (c) 29 cm (d) 14.7 cm
4. The excess pressure inside a soap bubble of radius 2 cm, if the surface tension of the solution is 0.03 N m⁻¹, is
   (a) 3 Pa (b) 1.5 Pa (c) 6 Pa (d) 12 Pa
5. The work done in blowing a soap bubble of radius 1 cm with a soap solution of surface tension 0.03 N m⁻¹ is about
   (a) 3.8 × 10⁻⁵ J (b) 7.5 × 10⁻⁵ J (c) 1.5 × 10⁻⁴ J (d) 1.9 × 10⁻⁵ J
6. A drop of water of radius 1 mm splits into 1000 identical droplets. Compared with the surface energy of the drop, the total surface energy of the droplets is
   (a) the same (b) 100 times (c) 1000 times (d) 10 times
7. Water flows at 2 m s⁻¹ in a pipe of diameter 4 cm. The pipe narrows to a diameter of 2 cm. The speed in the narrow part is
   (a) 4 m s⁻¹ (b) 1 m s⁻¹ (c) 8 m s⁻¹ (d) 16 m s⁻¹
8. In a horizontal pipe, water moves at 2 m s⁻¹ in one section and at 4 m s⁻¹ in another. The pressure difference between the sections is
   (a) 6000 Pa (b) 2000 Pa (c) 1000 Pa (d) 12000 Pa
9. A small hole is made in the side of a large open water tank, 5 m below the water surface. The speed of the emerging water is (g = 10 m s⁻²)
   (a) 5 m s⁻¹ (b) 7.1 m s⁻¹ (c) 50 m s⁻¹ (d) 10 m s⁻¹
10. Water flows through a narrow tube at 60 cm³ s⁻¹. If the tube is replaced by one of half the radius, with the same length and pressure difference, the flow becomes
   (a) 30 cm³ s⁻¹ (b) 15 cm³ s⁻¹ (c) 3.75 cm³ s⁻¹ (d) 7.5 cm³ s⁻¹
11. A plate of area 0.1 m² moves at 0.2 m s⁻¹ over a fixed parallel plate, separated by an oil film 1 mm thick of viscosity 0.5 Pa s. The force needed to keep it moving is
   (a) 0.01 N (b) 10 N (c) 1 N (d) 100 N
12. A cloud droplet of radius 10 μm falls through air of viscosity 1.8 × 10⁻⁵ Pa s (water density 1000 kg m⁻³; neglect air density; g = 9.8 m s⁻²). Its terminal velocity is about
   (a) 1.2 cm s⁻¹ (b) 1.2 m s⁻¹ (c) 0.12 cm s⁻¹ (d) 12 cm s⁻¹

::: note Answers and explanations — Set C
**1.** (b) — $P = P_0 + h\rho g = 1.01\times10^5 + 1000(9.8)(10) = 1.99\times10^5$ Pa. (a) is the gauge pressure alone.
**2.** (a) — $F_1 = F_2A_1/A_2 = 2000(9.8)(10/1000) = 196$ N.
**3.** (d) — $h = 2T/(r\rho g) = 2(0.072)/(10^{-4}\times1000\times9.8) = 0.147$ m = 14.7 cm. (b) forgets the factor 2.
**4.** (c) — two surfaces: $\Delta P = 4T/r = 4(0.03)/0.02 = 6$ Pa. (a) is $2T/r$, the value for a single surface.
**5.** (b) — two surfaces: $W = T\times2\times4\pi r^2 = 0.03\times8\pi\times10^{-4} = 7.5\times10^{-5}$ J. (a) counts only one surface.
**6.** (d) — volume conserved: $1000r^3 = R^3$, so $r = R/10$; total area $= 1000\times4\pi(R/10)^2 = 10\times4\pi R^2$. Energy is proportional to area: 10 times.
**7.** (c) — $v \propto 1/A \propto 1/d^2$: half the diameter, one quarter of the area, four times the speed: 8 m s⁻¹. (a) uses the diameter instead of the area.
**8.** (a) — $\Delta P = \frac{1}{2}\rho(v_2^2 - v_1^2) = 500(16 - 4) = 6000$ Pa; the pressure is lower where the water is faster. (b) squares the difference of the speeds; (c) forgets to square them.
**9.** (d) — $v = \sqrt{2gh} = \sqrt{2(10)(5)} = 10$ m s⁻¹.
**10.** (c) — $Q \propto r^4$: $60/16 = 3.75$ cm³ s⁻¹.
**11.** (b) — $F = \eta A\,v/d = 0.5(0.1)(0.2)/0.001 = 10$ N.
**12.** (a) — $v_t = \frac{2r^2\rho g}{9\eta} = \frac{2(10^{-5})^2(1000)(9.8)}{9(1.8\times10^{-5})} = 0.012$ m s⁻¹ = 1.2 cm s⁻¹; so small a speed that rising air holds clouds up.
:::

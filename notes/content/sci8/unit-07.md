---
subject: Science and Technology
grade: 8
unit: 7
title: Energy in Daily Life
hours: 0
area: Science and Technology
---

Every day in Nepal begins with energy: wood or gas under a pot, an electric
light switched on, a bus burning diesel, a water mill turning. Energy is the
capacity to do work, and it is never created or destroyed — it only changes
from one form to another. This unit takes two forms of energy that matter most
in daily life, **heat** and **light**, and ends with the sources we use and the
need to use them wisely.

::: key What this unit asks of you
You should be able to distinguish heat from temperature, describe the thermal
expansion of solids, liquids and gases with examples, explain conduction,
convection and radiation with examples of each, state the laws of reflection
and refraction, draw ray diagrams for a plane mirror and a convex lens, explain
dispersion of light and the working of the human eye, and classify energy
sources as renewable or non-renewable.
:::

## 7.1 Heat

**Heat** is a form of energy that flows from a hotter body to a colder one.
**Temperature** tells how hot or cold a body is; it is measured with a
thermometer in degrees Celsius (°C), and its SI unit is the kelvin (K).

Heat and temperature are not the same thing. A bucket of warm water at 40 °C
contains far more heat than a burning match at several hundred degrees, because
it has a much greater mass. Heat is energy; temperature is a measure of how hot.

| Scale | Ice point | Steam point | Body temperature |
|---|---|---|---|
| Celsius | 0 °C | 100 °C | 37 °C |
| Kelvin | 273 K | 373 K | 310 K |

**Relation:** $T(\text{K})=t(°\text{C})+273$.

### 7.1.1 Thermal expansion

Most substances expand when heated and contract when cooled, because the
particles vibrate faster and move slightly further apart.

| State | Expansion | Useful or harmful effect |
|---|---|---|
| Solid | small | railway lines and bridges are laid with a gap; the iron rim of a cart wheel is heated to fit it tightly; a tight metal lid loosens when held under hot water |
| Liquid | larger than solids | the liquid in a thermometer rises; a bottle filled to the top with oil overflows in the sun |
| Gas | largest of all | a balloon swells in the sun; a football left in the sun becomes harder |

::: caution Water is the exception
Almost every liquid contracts as it cools, but water behaves oddly between
0 °C and 4 °C: it contracts when warmed from 0 °C to 4 °C and expands when
cooled from 4 °C to 0 °C. This is why ice floats on water and why a pond freezes
at the surface while fish survive below.
:::

### 7.1.2 Transfer of heat

Heat moves in three ways.

| Method | How it moves | Needs a medium? | Example |
|---|---|---|---|
| Conduction | particle to particle, without the particles travelling | yes, and best in solids | a metal spoon in hot tea; the handle of a pan |
| Convection | the hot fluid itself rises and the cold fluid sinks | yes, in liquids and gases | water boiling; a room heater warming a room; the land and sea breeze |
| Radiation | as electromagnetic waves; needs no medium | no | the heat of the sun reaching the earth through space; a fire warming your face |

Metals are good conductors of heat because they have free electrons that carry
energy quickly; wood, plastic, wool, air and paper are poor conductors
(insulators). That is why a pan is metal but its handle is plastic, and why
woollen clothes keep us warm in winter: wool traps air, and trapped air is a
poor conductor, so the heat of the body stays in.

```figure caption="The three ways heat travels. Conduction passes energy along a solid, convection carries it in a moving fluid, and radiation crosses empty space."
fig, ax = plt.subplots(figsize=(5.0, 2.7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.text(1.6, 5.4, "Conduction", ha="center", fontsize=7.4, color=ACCENT)
ax.add_patch(plt.Rectangle((0.3, 4.2), 2.6, 0.5, fc=SERIES[2], alpha=0.5, ec=INK, lw=1.0))
for x in (0.7, 1.3, 1.9, 2.5):
    ax.add_patch(plt.Circle((x, 4.45), 0.11, color=SERIES[1], alpha=0.85))
ax.annotate("", xy=(3.1, 4.45), xytext=(1.0, 4.45),
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.text(2.0, 3.75, "spoon in tea: energy\\npasses particle to particle", ha="center",
        fontsize=6.0, color=INK)
ax.text(5.0, 5.4, "Convection", ha="center", fontsize=7.4, color=SERIES[1])
ax.add_patch(plt.Rectangle((3.9, 2.6), 2.2, 1.6, fill=False, ec=INK, lw=1.1))
for (x, y, dy) in [(4.6, 3.0, 1.0), (5.4, 4.0, -1.0)]:
    ax.annotate("", xy=(x, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.1))
ax.text(5.0, 1.9, "hot water rises,\\ncold water sinks", ha="center", fontsize=6.0, color=INK)
ax.text(8.0, 5.4, "Radiation", ha="center", fontsize=7.4, color=SERIES[2])
ax.add_patch(plt.Circle((6.7, 3.9), 0.45, fc="#f2b134", ec="none"))
ax.text(6.7, 3.9, "sun", ha="center", va="center", fontsize=5.8, color=INK)
for dy in (-0.5, 0, 0.5):
    ax.annotate("", xy=(9.6, 3.4 + dy), xytext=(7.2, 3.4 + dy),
                arrowprops=dict(arrowstyle="->", color=SERIES[2], lw=1.0))
ax.text(8.4, 2.5, "through empty space,\\nno medium needed", ha="center",
        fontsize=6.0, color=INK)
fig.tight_layout()
```

::: example Using $Q=mc\Delta\theta$
**Problem.** How much heat is needed to raise the temperature of 2 kg of water
from 20 °C to 70 °C? (Specific heat capacity of water
$=4200$ J kg⁻¹ °C⁻¹.)

**Solution.** The rise in temperature is
$\Delta\theta=70-20=50$ °C.

$$Q=mc\Delta\theta=2\times4200\times50=420\,000\ \text{J}=420\ \text{kJ}$$

**Answer.** 420 kJ.

**Check.** 1 kg of water needs 4200 J for each degree, so 2 kg needs 8400 J per
degree, and 50 degrees needs $8400\times50=420\,000$ J. Agrees.

**What it means.** Water has an unusually large specific heat capacity, which
is why it is used in radiators and hot-water bags and why a coastal place has a
milder climate than a desert.
:::

**Specific heat capacity** $c$ is the heat needed to raise the temperature of
1 kg of a substance by 1 °C. The heat taken in or given out is

$$Q=mc\Delta\theta$$

```photo id="sci10/solar-nepal" caption="A solar array in Nepal. Sunlight is the renewable source most easily used where the grid has not reached." width="70"
```

## 7.2 Light

**Light** is the form of energy that makes things visible. It travels in
straight lines called rays, at about $3\times10^8$ m/s in a vacuum.

### 7.2.1 Reflection

When light falls on a surface, part of it bounces back. This is **reflection**.

**Laws of reflection.** (1) The angle of incidence equals the angle of
reflection. (2) The incident ray, the reflected ray and the normal lie in the
same plane.

| Kind of reflection | Surface | What you see |
|---|---|---|
| Regular | smooth, such as a mirror or still water | a clear image |
| Irregular (diffuse) | rough, such as a wall or paper | no image; the light is scattered, which is why you can see the wall at all |

In a plane mirror the image is **virtual, erect, of the same size as the
object, and as far behind the mirror as the object is in front**. It is also
laterally inverted: your right hand appears as the image's left.

### 7.2.2 Refraction

When light passes from one transparent medium into another, its speed changes
and its path bends at the boundary. This bending is **refraction**.

| From | To | Speed | Bends |
|---|---|---|---|
| Air | glass or water | slower | towards the normal |
| Glass or water | air | faster | away from the normal |

**Laws of refraction.** (1) The incident ray, the refracted ray and the normal
are in the same plane. (2) For a given pair of media,
$\frac{\sin i}{\sin r}$ is a constant, called the refractive index.

Refraction explains why a stick half in water looks bent, why a coin in a bowl
of water seems to rise, why a pool looks shallower than it is, and why a
diamond sparkles.

### 7.2.3 Lenses

A **lens** is a piece of transparent material with one or two curved surfaces.

| | Convex lens | Concave lens |
|---|---|---|
| Shape | thicker at the middle | thinner at the middle |
| Effect on parallel rays | brings them together (converging) | spreads them out (diverging) |
| Images it can form | real and inverted, or virtual and erect | always virtual, erect and smaller |
| Use | magnifying glass, camera, human eye, spectacles for long sight | spectacles for short sight, peephole |

```figure caption="Refraction through a glass slab and a convex lens. Light entering glass slows down and bends towards the normal; a convex lens bends the rays so that they meet at the focus."
from matplotlib.patches import Ellipse
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.add_patch(plt.Rectangle((0.6, 1.6), 3.4, 2.6, fc=ACCENT, alpha=0.16, ec=ACCENT, lw=1.1))
ax.text(2.3, 4.5, "glass slab", ha="center", fontsize=6.6, color=ACCENT)
ax.plot([0.1, 1.3, 2.7, 4.5], [4.9, 3.4, 3.4, 2.0], color=INK, lw=1.3)
ax.plot([1.3, 1.3], [1.4, 5.2], color=GRID, lw=0.9, ls="--")
ax.plot([2.7, 2.7], [1.4, 5.2], color=GRID, lw=0.9, ls="--")
ax.text(1.1, 5.0, "i", fontsize=6.6, color=INK)
ax.text(2.9, 3.6, "r", fontsize=6.6, color=INK)
ax.text(2.3, 0.9, "ray bends towards the normal, then away again", ha="center",
        fontsize=6.0, color=MUTED)
cx, cy = 7.4, 3.4
ax.add_patch(Ellipse((cx, cy), 0.9, 3.0, fc=ACCENT, alpha=0.22, ec=ACCENT, lw=1.2))
for dy in (0.9, 0.0, -0.9):
    ys = cy + dy
    ye = cy + dy * 0.12
    ax.plot([5.3, 7.0, 8.6], [ys, ye, 3.4 if dy else 3.4], color=INK, lw=1.1)
ax.plot([5.3, 8.6], [3.4, 3.4], color=GRID, lw=0.9, ls="--")
ax.plot([8.6], [3.4], "o", color=SERIES[1], ms=4)
ax.text(8.75, 3.4, "F", ha="left", va="center", fontsize=6.8, color=SERIES[1])
ax.text(7.4, 5.2, "convex lens", ha="center", fontsize=6.6, color=ACCENT)
ax.text(7.4, 0.9, "parallel rays meet at the focus", ha="center", fontsize=6.0,
        color=MUTED)
fig.tight_layout()
```

::: caution Use the real ray rules, not a sketch
In a lens diagram, rays parallel to the principal axis must pass through the
focus after refraction, and a ray through the optical centre must go straight.
Rays drawn bending at the wrong place, or a "focus" that is not where the
parallel rays actually meet, lose the diagram marks even if the labels are
correct.
:::

### 7.2.4 Dispersion of light

White light is a mixture of colours. When it passes through a glass prism, the
different colours bend by different amounts and separate into a band of seven
colours — red, orange, yellow, green, blue, indigo and violet. This splitting
is **dispersion**, and the band is a **spectrum**. Red bends least and violet
bends most. A rainbow is formed when sunlight is refracted and reflected inside
droplets of rain.

### 7.2.5 The human eye

| Part | Function |
|---|---|
| Cornea | the transparent front surface; does most of the bending of light |
| Iris | the coloured ring that controls the size of the pupil |
| Pupil | the opening that lets light in |
| Lens | fine-tunes the focus by changing its shape |
| Retina | the screen at the back, where the image forms and light-sensitive cells detect it |
| Optic nerve | carries the signal to the brain |

The image formed on the retina is real and inverted; the brain interprets it the
right way up. Two common defects: in **short sight** (myopia) a distant object
focuses in front of the retina, corrected by a concave lens; in **long sight**
(hypermetropia) a near object focuses behind the retina, corrected by a convex
lens.

### 7.2.6 Optical instruments

- **Magnifying glass** — a convex lens held inside its focal length, giving a
  virtual, erect, enlarged image.
- **Camera** — a convex lens forms a real, inverted image on a sensor; the
  aperture and shutter control the light.
- **Microscope** — two convex lenses, giving a very large magnification of tiny
  objects.
- **Telescope** — a large convex lens (or mirror) collects light from far
  objects and a second lens magnifies the image.
- **Periscope** — two plane mirrors at 45°, letting you see over an obstacle.

```photo id="sci10/biogas" caption="A household biogas plant. Dung and kitchen waste become a smokeless cooking gas and a good manure." width="66"
```

## 7.3 Energy sources and conservation

| Source | Renewable? | Notes |
|---|---|---|
| Sunlight | renewable | solar panels and solar cookers; abundant in Nepal |
| Wind | renewable | wind turbines where the wind is steady, as in Mustang |
| Water | renewable | micro-hydro and large hydro plants |
| Biogas and biomass | renewable | cattle dung and plant waste; saves firewood |
| Geothermal | renewable | hot springs such as Tatopani |
| Fossil fuels (coal, petroleum, natural gas) | non-renewable | formed over millions of years; burning them causes pollution |
| Nuclear fuel | non-renewable | not used in Nepal |

**Law of conservation of energy.** Energy can neither be created nor destroyed;
it can only be changed from one form into another. A hydroelectric plant changes
the potential energy of stored water into kinetic energy, then into electrical
energy, then into light, sound and heat in your home.

| Device | Energy change |
|---|---|
| Electric bulb | electrical → light + heat |
| Electric fan | electrical → kinetic + sound |
| Dry cell | chemical → electrical |
| Solar panel | light → electrical |
| Microphone | sound → electrical |
| Generator | kinetic → electrical |
| Burning firewood | chemical → heat + light |

::: tip Five habits that save energy at home
**(1)** Switch off lights and fans when you leave a room. **(2)** Use LED bulbs,
which give the same light for about a fifth of the power. **(3)** Pressure-cook
dal and rice: it saves both fuel and time. **(4)** Dry clothes in the sun instead
of in a machine. **(5)** Do not leave the television or charger on stand-by; a
plug that is warm is a plug that is using energy.
:::

::: example Worked reasoning: why the pressure cooker saves fuel
**Observation.** Dal takes about an hour in an open pot on a kerosene stove,
but about twenty minutes in a pressure cooker.

**Reasoning.** Water boils at 100 °C in an open pot and cannot get hotter, no
matter how large the flame, because the extra heat only turns water into steam.
In a closed pressure cooker the steam cannot escape, so the pressure inside
rises and water boils at about 121 °C. The higher temperature cooks the dal
faster, and since the lid is closed, little heat escapes with the steam.

**Conclusion.** The pressure cooker does not add energy; it uses the same energy
more usefully. The saving comes from a higher cooking temperature and from
stopping the heat from leaving with the steam.
:::

## 7.5 Energy arithmetic for daily life

| Quantity | Formula | Unit |
|---|---|---|
| Energy used | $E = P \times t$ | kWh (unit) |
| Cost | units × rate | rupees |
| Efficiency | $\frac{\text{useful output}}{\text{total input}} \times 100$ | per cent |
| Potential energy | $PE = mgh$ | joule (J) |
| Kinetic energy | $KE = \frac{1}{2}mv^2$ | joule (J) |

::: example Comparing two cooking fuels
**Question.** A family cooks for 2 hours a day. An induction cooker of
1,500 W costs Rs 12 per unit; a gas cylinder of 14.2 kg costs Rs 1,900 and
lasts 30 such days. Which is cheaper per month of 30 days?

**Answer.** Induction: $1.5$ kW × 2 h $= 3$ units a day; 30 days $= 90$
units; cost $= 90 \times 12 = $ **Rs 1,080**.
Gas: **Rs 1,900** for the same 30 days.
The **induction cooker is cheaper by Rs 820 a month**, and it also avoids
indoor smoke — though it needs a reliable supply.
:::

::: example Energy of falling water
**Question.** Find the potential energy of 500 kg of water held 20 m above a
turbine ($g = 10$ m/s²).

**Answer.** $PE = mgh = 500 \times 10 \times 20 = \textbf{100{,}000 J}$
(100 kJ). In a hydropower plant this potential energy becomes kinetic energy
as the water falls, and then electrical energy in the generator.
:::

::: note Activity — the household energy audit
List every electrical appliance at home with its wattage (printed on the
rating plate) and the hours it runs each day. Work out the daily units and
the monthly bill, and rank the appliances from the most to the least
expensive. Then propose three changes and estimate the saving.
:::

## Chapter summary

- **Heat** is energy in transfer; **temperature** measures how hot a body is;
  $T(\text{K})=t(°\text{C})+273$.
- Substances expand on heating — gases most, liquids next, solids least; water
  is the exception between 0 °C and 4 °C.
- Heat travels by **conduction** (solids), **convection** (fluids) and
  **radiation** (no medium needed).
- $Q=mc\Delta\theta$, where $c$ is the specific heat capacity.
- **Laws of reflection**: angle of incidence = angle of reflection, and the
  three lines are coplanar. A plane mirror gives a virtual, erect, same-size
  image, laterally inverted.
- **Refraction** is the bending of light as its speed changes between media;
  $\frac{\sin i}{\sin r}$ is a constant.
- A convex lens converges light and can give a real inverted image; a concave
  lens diverges and always gives a virtual, erect, diminished image.
- **Dispersion** splits white light into seven colours, red bending least.
- The eye focuses light on the retina; myopia is corrected by a concave lens and
  hypermetropia by a convex lens.
- Energy is conserved: it only changes form. Sources are renewable (sun, wind,
  water, biogas) or non-renewable (fossil fuels, nuclear).

## Practice questions

**Group A — Objective (1 mark each)**

1. The SI unit of temperature is the <span class="marks">[1]</span>
   (a) degree Celsius (b) kelvin (c) joule (d) calorie
2. Heat transfer in liquids and gases takes place mainly by
   <span class="marks">[1]</span>
   (a) conduction (b) convection (c) radiation (d) reflection
3. The angle of incidence is always equal to the
   <span class="marks">[1]</span>
   (a) angle of refraction (b) angle of reflection (c) critical angle
   (d) angle of deviation
4. Which lens is used to correct short sight? <span class="marks">[1]</span>
   (a) convex (b) concave (c) cylindrical (d) plane
5. The band of seven colours obtained from white light is called the
   <span class="marks">[1]</span>
   (a) spectrum (b) refraction (c) reflection (d) focus
6. Which of these is a non-renewable source of energy?
   <span class="marks">[1]</span>
   (a) sunlight (b) wind (c) coal (d) biogas

::: note Answers to Group A
**1.** (b) — the kelvin is the SI unit.
**2.** (b) — the fluid itself moves, carrying the heat.
**3.** (b) — that is the second law of reflection.
**4.** (b) — a concave lens pushes the image back to the retina.
**5.** (a) — the spectrum.
**6.** (c) — coal took millions of years to form and cannot be replaced.
:::

**Group B — Short answer (2 marks each)**

1. Distinguish between heat and temperature.
   <span class="marks">[2]</span>
2. Give one example each of conduction, convection and radiation from daily
   life. <span class="marks">[2]</span>
3. State the two laws of reflection of light.
   <span class="marks">[2]</span>
4. Write two differences between a convex lens and a concave lens.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Heat is a form of energy that flows from a hot body to a cold one, and it
is measured in joules; temperature is a measure of how hot or cold a body is,
measured in degrees Celsius or kelvin. A bucket of warm water contains more
heat than a burning match, though the match has a far higher temperature.
**2.** Conduction — a metal spoon left in hot tea becomes hot at the handle.
Convection — water heated in a pot circulates and warms evenly, and a room
heater warms a room. Radiation — the heat of the sun reaches the earth through
space, and you feel the warmth of a fire on your face.
**3.** (i) The angle of incidence is equal to the angle of reflection.
(ii) The incident ray, the reflected ray and the normal at the point of
incidence all lie in the same plane.
**4.** A convex lens is thicker at the middle and converges parallel rays to a
focus; a concave lens is thinner at the middle and diverges them. A convex lens
can form a real, inverted image; a concave lens always forms a virtual, erect,
diminished image.
:::

**Group C — Long answer (4 marks each)**

1. How much heat is needed to raise the temperature of 500 g of water from
   25 °C to 85 °C? Take $c=4200$ J kg⁻¹ °C⁻¹. Explain what specific heat
   capacity means and why water is used in a hot-water bag.
   <span class="marks">[4]</span>
2. Draw a labelled ray diagram showing refraction through a convex lens of
   parallel rays, and explain with it how a convex lens forms a real, inverted
   image. State two uses of a convex lens. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $m=500$ g $=0.5$ kg, $\Delta\theta=85-25=60$ °C, so
$Q=mc\Delta\theta=0.5\times4200\times60=126\,000$ J $=126$ kJ.
**Specific heat capacity** is the quantity of heat needed to raise the
temperature of 1 kg of a substance by 1 °C. For water it is
4200 J kg⁻¹ °C⁻¹, which is high compared with most substances. Water is used in
a hot-water bag because this high value means a given mass of water stores a
great deal of heat while its own temperature rises only a little; it therefore
gives out warmth slowly and steadily for a long time, which is exactly what a
hot-water bag is for.
**2.** **Diagram.** Draw a convex lens with the principal axis through it; mark
the optical centre and a focal point F on each side. Three rays from the top of
the object: one parallel to the axis, which passes through F after the lens;
one through the optical centre, which goes straight; one through the far focal
point, which emerges parallel. All three meet at the same point, which is the
top of the image. **Explanation.** The rays from each point of the object are
brought together again on the other side of the lens, so a real image is formed
where they actually meet; because the rays cross, the image is inverted, and
because it is formed on the far side where light really arrives, it is real.
**Two uses.** A magnifying glass and a camera lens (also a microscope objective
lens, a projector lens, and spectacles for long sight).
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The main constituent of biogas is
   (a) carbon dioxide (b) methane (c) hydrogen (d) butane
**2.** A 2,000 W heater used for 3 hours consumes
   (a) 0.6 unit (b) 6 units (c) 60 units (d) 600 units
**3.** In a hydropower plant the energy chain is
   (a) electrical → kinetic → potential (b) potential → kinetic → electrical (c) chemical → heat → electrical (d) heat → kinetic → chemical
**4.** Which source is non-renewable?
   (a) solar (b) wind (c) coal (d) biogas
**5.** The potential energy of a 10 kg body at a height of 5 m ($g = 10$ m/s²) is
   (a) 50 J (b) 200 J (c) 500 J (d) 5000 J

::: note Objective practice — answers
**1.** (b) — methane. **2.** (b) — $2 \text{ kW} \times 3 \text{ h} = 6$ kWh. **3.** (b) — stored water → flowing water → generator. **4.** (c) — coal is a fossil fuel. **5.** (c) — $mgh = 10 \times 10 \times 5 = 500$ J.
:::

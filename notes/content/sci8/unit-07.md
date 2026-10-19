---
subject: Science and Technology
grade: 8
unit: 7
title: Energy in Daily Life
hours: 0
area: Science and Technology
---

We read, write, carry loads and work in the fields with the energy from our food.
Vehicles run on petrol or diesel, and electrical appliances run on electricity.
**Energy is the capacity to do work.** Its SI unit is the **joule (J)**; the
calorie is an older unit, and **1 calorie ≈ 4.2 J**. Energy exists in many forms —
mechanical, heat, light, sound, magnetic, electrical, chemical and nuclear — and
changes from one form to another. This unit, following the CDC textbook, studies
heat and its transfer, light and spherical mirrors, and sound, together with the
other topics of the syllabus (thermometers, expansion, specific heat capacity,
refraction, lenses and energy sources).

::: key What this unit asks of you
Explain conduction, convection and radiation with examples and applications; tell
mechanical from electromagnetic waves; describe a thermos flask and the greenhouse
effect; define the terms of spherical mirrors, give the rules of reflection and the
images formed by a concave mirror; define frequency, wavelength, period and
amplitude, use $v=f\lambda$ and $I=\frac{P}{A}$; classify sound as infrasonic,
audible or ultrasonic; and explain the causes, effects and control of noise pollution.
:::

## 7.1 Heat and temperature; thermometers and their scales

**Heat** is a form of energy that gives us the feeling of warmth. It always flows
from a body at a **higher temperature** to a body at a **lower temperature**. When we
touch hot water, heat flows into our skin and we feel hot; when we touch ice, heat
flows out of our skin and we feel cold.

**Temperature** is the degree of hotness or coldness of a body. It is measured with
a **thermometer**. Heat is energy (joule); temperature is a measure of how hot a body
is (°C, °F or kelvin). A bucket of warm water has much more heat than a red-hot pin,
although the pin's temperature is higher.

| Scale | Ice point | Steam point | Normal body temperature |
|---|---|---|---|
| Celsius (°C) | 0 °C | 100 °C | 37 °C |
| Fahrenheit (°F) | 32 °F | 212 °F | 98.6 °F |
| Kelvin (K), SI | 273 K | 373 K | 310 K |

Conversions: $F=\frac{9}{5}C+32$ and $K=C+273$. A **clinical thermometer** reads
35–42 °C and has a kink that stops the mercury falling back; a **laboratory
thermometer** reads about −10 °C to 110 °C.

::: example Changing temperature scales
**Problem.** Convert 37 °C into °F and K.

**Solution.** $F=\frac{9}{5}\times37+32=66.6+32=98.6$ °F. $K=37+273=310$ K.
:::

## 7.2 Thermal expansion of solids, liquids and gases

Most substances **expand** when heated and **contract** when cooled, because their
particles vibrate faster and move a little farther apart. Gases expand most,
liquids less, solids least.

| State | Examples of expansion |
|---|---|
| Solid | gaps are left between rails and in bridges; electric wires sag in summer; a tight metal lid is loosened by putting it in hot water |
| Liquid | mercury or alcohol rises in a thermometer; a bottle filled to the brim with oil overflows in the sun |
| Gas | a balloon or football left in the sun becomes tight; tyres are not pumped too hard in summer |

::: caution Water is unusual
Water contracts when warmed from 0 °C to 4 °C and expands when cooled from 4 °C to
0 °C, so it is densest at 4 °C. That is why ice floats and a pond freezes only at the
top, leaving water below in which fish survive.
:::

## 7.3 Transfer of heat: conduction, convection and radiation

The process by which heat moves from one place or body to another is called the
**transmission (transfer) of heat**. It happens in three ways.

### 7.3.1 Conduction

In Activity 7.1, pins stuck with wax on a metal rod fall one after another, starting
from the heated end. The particles of the solid do not move from their places; each
one **vibrates** more and passes heat to its neighbour, like students passing a brick
along a line.

::: definition Conduction
**Conduction** is the transfer of heat through a solid from particle to particle
**without the actual movement of the particles**.
:::

**Good conductors** let heat pass easily: iron, copper, aluminium, silver, gold.
**Insulators** (bad conductors) do not: wood, plastic, rubber, cotton, wool, air,
porcelain. Most metals are good conductors; diamond and graphite are unusual
non-metals that conduct heat well.

**Applications of conduction and insulation**

- Cooking pots and kettles are made of metal to pass heat to the food quickly, while
  their **handles** are made of wood or plastic, which are insulators.
- **Woollen clothes and blankets** keep us warm: wool and the air trapped between its
  fibres are poor conductors, so body heat does not escape.
- Tea cups are made of **porcelain**, a poor conductor, so the tea stays hot and the
  cup can be held.
- **Mud houses** are cool in summer and warm in winter because mud is a poor conductor.
- Birds fluff up their feathers on cold days to trap a layer of insulating air.

### 7.3.2 Convection

Drop a little colour into a beaker of water and heat it from below (Activity 7.3).
The coloured warm water rises, and cold water from the top comes down to take its
place. Heated water becomes **less dense** and rises; denser cold water sinks. This
circular flow is a **convection current**.

::: definition Convection
**Convection** is the transfer of heat in liquids and gases by the **actual movement
of the heated particles** from one place to another.
:::

**Wind** is caused by convection: the ground heated by the sun warms the air above it;
the warm, light air rises; cooler air from nearby moves in to take its place.

**Sea breeze and land breeze.** Water has a higher specific heat capacity than land, so
land heats and cools faster than the sea.

| Sea breeze | Land breeze |
|---|---|
| blows in the **daytime** | blows at **night** |
| land is hotter than the sea; air over land rises (low pressure) | land cools faster; the sea is warmer; air over the sea rises |
| cool air flows **from sea to land** | cool air flows **from land to sea** |

```figure caption="Sea breeze by day and land breeze by night. Air rises over the warmer surface and cooler air flows in to replace it."
fig, axs = plt.subplots(1, 2, figsize=(5.1, 2.4))
for ax, title, hot in zip(axs, ["Day: sea breeze", "Night: land breeze"], ["land", "sea"]):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.add_patch(plt.Rectangle((0, 0), 5, 1.0, fc="#bcd6ee", ec="none"))
    ax.add_patch(plt.Rectangle((5, 0), 5, 1.0, fc="#d9c7a3", ec="none"))
    ax.text(2.5, 0.5, "sea", ha="center", va="center", fontsize=8, color=INK)
    ax.text(7.5, 0.5, "land", ha="center", va="center", fontsize=8, color=INK)
    up = 7.5 if hot == "land" else 2.5
    dn = 2.5 if hot == "land" else 7.5
    ax.annotate("", xy=(up, 4.3), xytext=(up, 1.4), arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.6))
    ax.annotate("", xy=(dn, 1.4), xytext=(dn, 4.3), arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.6))
    ax.annotate("", xy=(up - 1.0 if up > dn else up + 1.0, 1.7), xytext=(dn + 1.0 if up > dn else dn - 1.0, 1.7),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.6))
    ax.annotate("", xy=(dn + 1.0 if up > dn else dn - 1.0, 4.6), xytext=(up - 1.0 if up > dn else up + 1.0, 4.6),
                arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.6))
    ax.text(5, 2.15, "cool air", ha="center", fontsize=7.4, color=ACCENT)
    ax.text(5, 5.05, "warm air returns", ha="center", fontsize=7.4, color=SERIES[1])
    ax.set_title(title, fontsize=8.2, color=INK)
fig.tight_layout()
```

**Natural (free) convection** happens by itself because of density differences: boiling
water, sea and land breezes, cloud formation and rain. **Forced convection** uses
outside energy such as a fan or pump: electric fans, water heaters (geysers), air
conditioners. Convection also helps to carry heat in the blood of warm-blooded animals,
works in refrigerators and room heaters, and causes clouds, thunderstorms and lightning.
Ventilators are made in the **upper part** of walls because warm, used air rises and
goes out, while fresh cool air comes in through doors and windows.

### 7.3.3 Radiation

Space between the sun and the earth has no medium, so the sun's heat cannot come by
conduction or convection. It comes by **radiation**.

::: definition Radiation
**Radiation** is the transfer of heat in the form of (electromagnetic) waves **without
any material medium**. It can take place even through a vacuum, at the speed of light.
:::

**Colour and radiation (Activity 7.6).** Three boxes — black, white and golden — kept in
the sun with thermometers: the black box becomes hottest. **Dark, dull surfaces are good
absorbers and good emitters** of heat radiation; white and shiny surfaces are poor
absorbers and emitters. So white clothes are worn in summer, houses in the Terai are
painted white, and the inside of a solar cooker and the bottom of cooking pots are black.

**Applications:** we feel warm near a fire; the sun heats the earth; the black grill at
the back of a refrigerator radiates heat into the room; hot tea cools by radiating heat.

### 7.3.4 Waves: mechanical and electromagnetic

A stone thrown into a pond makes **ripples** that spread out while the water particles
only move up and down. A wave carries **energy** from one place to another without
carrying the medium with it.

| Mechanical wave | Electromagnetic wave |
|---|---|
| needs a material medium | needs no medium; travels through a vacuum |
| cannot travel through a vacuum | travels at $3\times10^8$ m/s in a vacuum |
| loses energy in the medium; travels limited distance | travels very long distances |
| e.g. sound, water waves, waves on a rope | e.g. light, radio waves, X-rays, infrared, gamma rays |

Speed of sound: about 332 m/s in air, 1481 m/s in water and 5120 m/s in iron. Light from
the sun takes about **8 minutes 20 seconds** to reach the earth. Heat radiation is carried
mainly by **infrared** waves, which our eyes cannot see.

### 7.3.5 The thermos flask

A **thermos (vacuum) flask** keeps hot liquids hot and cold liquids cold for a long time,
because it stops all three ways of heat transfer.

```figure caption="Section of a thermos flask. The vacuum stops conduction and convection; the silvered walls stop radiation; the cork stopper and pad stop conduction."
fig, ax = plt.subplots(figsize=(4.4, 3.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")
ax.add_patch(plt.Rectangle((2.0, 0.4), 3.6, 6.4, fc="#e6e6e6", ec=INK, lw=1.4))
ax.add_patch(plt.Rectangle((2.45, 0.9), 2.7, 5.2, fc="white", ec=MUTED, lw=2.4))
ax.add_patch(plt.Rectangle((2.75, 1.2), 2.1, 4.9, fc="#d4e3f3", ec=MUTED, lw=2.4))
ax.add_patch(plt.Rectangle((2.6, 0.45), 2.4, 0.42, fc=SERIES[3], ec=INK, lw=0.8))
ax.add_patch(plt.Rectangle((2.9, 6.1), 1.8, 0.9, fc=SERIES[3], ec=INK, lw=0.8))
ax.add_patch(plt.Rectangle((1.8, 7.0), 4.0, 0.6, fc="#bdbdbd", ec=INK, lw=1))
def tag(x, y, ty, s):
    ax.plot([x, 6.4], [y, ty], color=MUTED, lw=0.7)
    ax.text(6.5, ty, s, ha="left", va="center", fontsize=7.6, color=INK)
tag(5.0, 7.3, 7.5, "cap / cup")
tag(4.4, 6.5, 6.5, "cork stopper (insulator)")
tag(5.15, 4.8, 5.4, "vacuum between walls")
tag(4.85, 3.8, 4.3, "silvered double glass wall")
tag(4.0, 3.0, 3.2, "hot or cold liquid")
tag(5.6, 2.0, 2.1, "outer metal / plastic case")
tag(4.8, 0.65, 0.9, "insulating cork pad")
fig.tight_layout()
```

| Part | How it reduces heat transfer |
|---|---|
| double glass wall with **vacuum** between | vacuum has no particles, so no conduction or convection |
| **silvered** surfaces facing the vacuum | shiny surfaces reflect radiation back |
| **cork stopper** and **cork pad** | poor conductors; stopper also stops convection out of the mouth |
| outer case | protects the fragile glass |

### 7.3.6 The greenhouse and the greenhouse effect

An **artificial greenhouse** (plastic tunnel) is a house of glass or transparent
plastic on a frame. It is used to grow off-season vegetables and nursery plants. The
glass lets in the sun's **short-wave** radiation, but the soil and plants give out
**long-wave** (infrared) radiation, which cannot pass out easily. The trapped heat keeps
the inside warm. The roof is sloping so that more sunlight enters.

The **earth's atmosphere** acts in the same way. Gases such as **carbon dioxide, methane,
water vapour, nitrous oxide and CFCs** (greenhouse gases) absorb the heat radiated by the
earth and send part of it back. This warming of the earth is the **greenhouse effect**.

::: definition Greenhouse effect
The **greenhouse effect** is the warming of the earth's surface because greenhouse gases
in the atmosphere trap part of the heat radiated by the earth instead of letting it
escape into space.
:::

Without it, the earth's average temperature would be about **−18 °C** instead of about
**15 °C (59 °F)**, and life would hardly be possible. But factories, vehicles and
deforestation are adding more greenhouse gases, which trap extra heat and cause **global
warming**.

**Harmful effects of an increased greenhouse effect:** rise in average temperature;
changes in rainfall and the water cycle; health problems; lower farm production; melting
of Himalayan snow and danger of **glacial lake outburst floods (GLOF)**; sea-level rise
that may drown low coastal land; loss of biodiversity; desertification; imbalance of
ecosystems.

**Uses:** the natural greenhouse effect keeps the earth warm enough for life; artificial
greenhouses let farmers grow off-season vegetables and protect plants from cold.

::: tip Why a cloudy night feels warmer
Clouds (water vapour) absorb the heat radiated by the ground and send it back, so the
ground cools less than on a clear night.
:::

## 7.4 Specific heat capacity and its daily applications

Different substances need different amounts of heat to warm up by the same amount.

::: definition Specific heat capacity
The **specific heat capacity** of a substance is the amount of heat needed to raise the
temperature of 1 kg of it by 1 °C (or 1 K). Its SI unit is J/kg °C. The heat needed is
$Q=m\,s\,\Delta t$, where $m$ is mass, $s$ specific heat capacity and $\Delta t$ the rise in
temperature.
:::

| Substance | Specific heat capacity (J/kg °C, approximate) |
|---|---|
| Water | 4200 |
| Ice | 2100 |
| Aluminium | 900 |
| Iron | 460 |
| Copper | 390 |

Water has a very high specific heat capacity, so it heats and cools slowly. This is why
the sea is cooler than land by day and warmer by night (sea and land breezes), why hot
water bags are filled with water, and why water is used in car radiators.

::: example Heat needed to warm water
**Problem.** How much heat is needed to raise the temperature of 2 kg of water from
20 °C to 70 °C? ($s=4200$ J/kg °C)

**Solution.** $\Delta t=70-20=50$ °C.
$Q=m\,s\,\Delta t=2\times4200\times50=420\,000$ J $=420$ kJ.
:::

## 7.5 Light: reflection by plane and spherical mirrors, and refraction

**Light** is a form of energy that gives us the sensation of vision. When light falls on
an object, part of it is absorbed, part is reflected and part may pass through.

::: definition Reflection of light
**Reflection of light** is the returning of light into the same medium after it strikes
a surface. Smooth, polished surfaces reflect most of the light and look shiny; rough
surfaces scatter light and look dull.
:::

A **mirror** reflects light and forms an image. Mirrors are **plane** or **spherical**.
A spherical mirror is part of a hollow glass sphere.

### 7.5.1 Concave and convex mirrors

Look into a steel spoon: the inner side is **concave** (depressed in the middle), the back
is **convex** (bulging out in the middle).

| Concave mirror | Convex mirror |
|---|---|
| reflecting surface curved inward (caved in) | reflecting surface bulging outward |
| **converging** mirror: brings parallel rays together | **diverging** mirror: spreads parallel rays out |
| focus is real, in front of the mirror | focus is virtual, behind the mirror |
| forms real, inverted images (and a virtual, magnified image when the object is very close) | always forms a virtual, erect, diminished image |
| torch, headlight, shaving mirror, solar cooker | rear-view mirror of vehicles, street lamps |

**Terms of a spherical mirror**

| Term | Meaning |
|---|---|
| Pole (P) | the centre of the reflecting surface; distances are measured from it |
| Centre of curvature (C) | centre of the sphere of which the mirror is a part |
| Radius of curvature (R) | distance from P to C |
| Principal axis | the straight line through P and C |
| Principal focus (F) | the point where rays parallel to the principal axis meet (concave) or seem to come from (convex) after reflection; F is midway between P and C |
| Focal length (f) | distance from P to F; $f=\frac{R}{2}$ |

**Rules for drawing ray diagrams (concave mirror)**

1. A ray **parallel** to the principal axis passes **through F** after reflection.
2. A ray **through F** becomes **parallel** to the principal axis after reflection.
3. A ray **through C** is reflected **back along the same path**.

For a convex mirror: a parallel ray seems to come from F behind the mirror; a ray
directed towards F becomes parallel; a ray directed towards C returns along its path.

```figure caption="Ray diagram for a concave mirror with the object AB beyond C. The image A′B′ is between F and C: real, inverted and diminished."
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0.8, 9.0)
ax.set_ylim(-2.4, 1.9)
ax.axis("off")
th = np.linspace(-0.62, 0.62, 80)
ax.plot(4 + 4 * np.cos(th), 4 * np.sin(th), color=INK, lw=2)
for t in np.linspace(-0.6, 0.6, 14):
    x, y = 4 + 4 * np.cos(t), 4 * np.sin(t)
    ax.plot([x, x + 0.18], [y, y + 0.1], color=MUTED, lw=0.7)
ax.plot([0.9, 8.2], [0, 0], color=MUTED, lw=0.8)
for x, l in [(4, "C"), (6, "F"), (8, "P")]:
    ax.plot(x, 0, "o", color=INK, ms=3)
    ax.text(x - (0.25 if l == "P" else 0), -0.3, l, ha="center", fontsize=8, color=INK)
ax.annotate("", xy=(2.5, 0.8), xytext=(2.5, 0), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.6))
ax.text(2.5, 0.95, "A", ha="center", fontsize=8, color=ACCENT); ax.text(2.5, -0.3, "B", ha="center", fontsize=8, color=ACCENT)
xi = 8 - 1 / (0.5 - 1 / 5.5)
yi = -0.8 * (8 - xi) / 5.5
ax.annotate("", xy=(xi, yi), xytext=(xi, 0), arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.6))
ax.text(xi + 0.05, yi - 0.3, "A′", ha="center", fontsize=8, color=SERIES[1]); ax.text(xi, 0.15, "B′", ha="center", fontsize=8, color=SERIES[1])
xm = 4 + (16 - 0.64) ** 0.5
ax.plot([2.5, xm], [0.8, 0.8], color=SERIES[2], lw=1)
ax.plot([xm, xi], [0.8, yi], color=SERIES[2], lw=1)
s = -0.8 / 1.5
xs_ = np.linspace(2.5, 8.0, 2000)
ys_ = 0.8 + s * (xs_ - 2.5)
xc = xs_[np.argmin(np.abs((xs_ - 4) ** 2 + ys_ ** 2 - 16))]
ax.plot([2.5, xc], [0.8, 0.8 + s * (xc - 2.5)], color=SERIES[3], lw=1)
ax.text(5.0, 1.25, "parallel ray → through F", fontsize=7.4, color=SERIES[2])
ax.text(1.0, -1.9, "ray through C returns along itself", fontsize=7.4, color=SERIES[3])
fig.tight_layout()
```

**Images formed by a concave mirror**

| Position of object | Position of image | Nature and size of image |
|---|---|---|
| at infinity | at F | real, inverted, highly diminished (point) |
| beyond C | between F and C | real, inverted, diminished |
| at C | at C | real, inverted, same size |
| between C and F | beyond C | real, inverted, magnified |
| at F | at infinity | real, inverted, highly magnified |
| between F and P | behind the mirror | **virtual, erect, magnified** |

A **convex mirror** always forms a virtual, erect and diminished image behind the mirror,
between P and F; for an object at infinity the image is a point at F.

| Real image | Virtual image |
|---|---|
| formed where reflected rays actually meet | formed where reflected rays only appear to meet |
| can be obtained on a screen | cannot be obtained on a screen |
| formed in front of the mirror | formed behind the mirror |
| always inverted | always erect |

**Uses of a concave mirror:** reflector in torches, searchlights and vehicle headlights
(the bulb is at F so the reflected beam is parallel and goes far); doctors' mirror for
ear, nose and throat; shaving and make-up mirror (enlarged erect image when the face is
within F); astronomical telescopes; solar cookers (it converges the sun's rays).
**Uses of a convex mirror:** rear-view (side) mirror of vehicles, because it gives an
erect, diminished image and a **wide field of view**; reflector in street lamps to spread
light over a wide area.

::: note Activity 7.11 — focal length of a concave mirror
Point a concave mirror at a distant window and move a white card in front of it until a
sharp, inverted image of the window forms. The distance from mirror to card is roughly
the focal length (about 20–30 cm for a school mirror). Try the same with a convex or plane
mirror: no image forms on the card, because their images are virtual.
:::

### 7.5.2 Refraction of light

**Refraction** is the bending of light when it passes obliquely from one transparent
medium to another, because its speed changes. Light going from air into water or glass
(a denser medium) bends **towards** the normal; from water to air it bends **away** from
the normal. That is why a pencil in water looks bent and a pond looks shallower than it is.

## 7.6 Lenses and images; dispersion; the eye and optical instruments

A **lens** is a piece of transparent glass bounded by curved surfaces. A **convex
(converging) lens** is thicker in the middle and brings parallel rays to a real focus; it
can form real inverted images or (for a near object) a magnified virtual image — a
magnifying glass. A **concave (diverging) lens** is thinner in the middle, spreads light
out and always forms a virtual, erect, diminished image.

**Dispersion.** When white light passes through a glass prism it splits into seven colours
— **violet, indigo, blue, green, yellow, orange, red (VIBGYOR)** — because each colour bends
by a different amount. A rainbow forms in the same way in raindrops.

**The human eye** works like a camera: the **cornea** and **lens** form a real, inverted
image on the **retina**, the **iris** controls the size of the **pupil**, and the **optic
nerve** carries the message to the brain. **Optical instruments** — magnifying glass,
microscope, telescope, camera and spectacles — use lenses (and mirrors) to see small or
distant objects clearly.

## 7.7 Sound

Sound is produced by **vibrating** objects. Strike a tuning fork on a rubber pad and touch
it: it vibrates and hums. The particles of the medium vibrate back and forth **in the
direction in which the sound travels**, so sound is a **longitudinal** and **mechanical**
wave: it needs a medium (solid, liquid or gas) and **cannot travel through a vacuum**.

### 7.7.1 Characteristics of a wave

| Quantity | Meaning | Unit |
|---|---|---|
| Frequency (f) | number of waves produced in **one second** | hertz (Hz); kHz, MHz |
| Time period (T) | time taken to make one complete wave; $T=\frac{1}{f}$ | second (s) |
| Wavelength (λ) | distance between two successive crests (or compressions) | metre (m) |
| Amplitude (A) | maximum displacement of a particle from its mean position | metre (m) |

```figure caption="A wave drawn as a curve. Wavelength λ is the distance from one crest to the next; amplitude A is the height of a crest above the mean position."
fig, ax = plt.subplots(figsize=(5.0, 2.4))
x = np.linspace(0, 3, 400)
ax.plot(x, np.sin(2 * np.pi * x), color=ACCENT, lw=1.6)
ax.axhline(0, color=MUTED, lw=0.8, ls="--")
ax.annotate("", xy=(1.25, 1.35), xytext=(0.25, 1.35), arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
ax.text(0.75, 1.5, "wavelength λ", ha="center", fontsize=8, color=INK)
for xx in (0.25, 1.25):
    ax.plot([xx, xx], [1.02, 1.3], color=MUTED, lw=0.6, ls=":")
ax.annotate("", xy=(2.25, 1.0), xytext=(2.25, 0), arrowprops=dict(arrowstyle="<->", color=SERIES[1], lw=1))
ax.text(2.25, 1.2, "amplitude A", fontsize=8, color=SERIES[1], ha="center")
ax.text(1.37, 0.98, "crest", ha="left", fontsize=7.6, color=MUTED)
ax.text(0.75, -1.12, "trough", ha="center", fontsize=7.6, color=MUTED, va="top")
ax.set_ylim(-1.6, 1.8)
ax.axis("off")
fig.tight_layout()
```

::: definition Speed of sound
The distance travelled by sound in one second is its **speed**:
$v=f\lambda$ (speed = frequency × wavelength), in m/s. In a given medium the speed is
constant, so a higher frequency means a shorter wavelength.
:::

::: example Speed and wavelength of sound (textbook examples)
**Problem (a).** Find the speed of a sound of frequency 66 Hz and wavelength 5 m.
**Solution.** $v=f\lambda=66\times5=330$ m/s.

**Problem (b).** The speed of sound at 0 °C is 332 m/s and its frequency is 40 Hz. Find
the wavelength.
**Solution.** $\lambda=\frac{v}{f}=\frac{332}{40}=8.3$ m.
:::

### 7.7.2 Infrasonic, audible and ultrasonic sound

Human ears can hear frequencies from **20 Hz to 20 000 Hz (20 kHz)**. Children's and
women's voices have a higher frequency (sharper) than men's.

| Type | Frequency | Examples |
|---|---|---|
| Infrasonic (infrasound) | below 20 Hz | earthquakes, volcanoes; produced by elephants, rhinos, whales |
| Audible | 20 Hz – 20 kHz | speech, songs, musical instruments |
| Ultrasonic (ultrasound) | above 20 kHz | produced and heard by bats, dolphins, some insects; dogs can hear it |

**Uses of ultrasound:** ultrasonography (USG) to see a baby in the womb and to find
tumours and stones; bloodless operations; killing bacteria; **SONAR** to measure the depth
of the sea (depth $=\frac{\text{speed}\times\text{time}}{2}$, because the sound goes down and comes back).

### 7.7.3 Intensity of sound

The **intensity** of sound is the sound energy passing per second through unit area
perpendicular to its direction: $I=\frac{P}{A}$, unit **W/m²**. The **loudness** we hear is
measured in **decibels (dB)**.

| Sound | Typical level |
|---|---|
| whisper | about 20–30 dB |
| quiet library | about 30–40 dB |
| normal conversation | about 50–60 dB |
| busy traffic | about 70–90 dB |
| threshold of pain | about 120–140 dB |

According to the textbook, a person who cannot hear sounds of 45–60 dB has partial hearing
loss, and one who cannot hear even 80 dB is **deaf**.

**Factors affecting intensity:** **amplitude** ($I\propto A^2$); **distance** from the source
(intensity falls as you move away, which is why a sound gets fainter); **density** of the
medium (greater in denser, cold air); **area** of the vibrating body (a big temple bell or
drum is louder); **frequency** (shriller sounds have more intensity).

::: example Intensity and energy of sound
**Problem (a).** Children whistle with a sound power of $2\times10^{-4}$ W spread over 5 m².
Find the intensity.
**Solution.** $I=\frac{P}{A}=\frac{2\times10^{-4}}{5}=4\times10^{-5}$ W/m².

**Problem (b).** Sound of intensity $2\times10^{-5}$ W/m² falls on 6 m² for 1 s. Find the
energy carried.
**Solution.** Power $P=I\times A=2\times10^{-5}\times6=1.2\times10^{-4}$ W; energy $=P\times t=1.2\times10^{-4}$ J.
:::

### 7.7.4 Sound (noise) pollution

**Noise** is unwanted, unpleasant or too loud sound; **sound pollution** is excessive noise
that harms people, animals and the environment.

**Causes:** heavy traffic and horns, factories and machines, construction, loudspeakers,
loud television and music, crowded markets.
**Effects:** weakening or loss of hearing, rupture of the eardrum, high blood pressure,
digestive problems, stress and poor sleep, difficulty in concentrating on study and work.
**Control:** plant trees along roads and around industries; use silencers in vehicles and
avoid unnecessary horns; keep TV and music low; build industries away from settlements;
run public awareness programmes.

## 7.8 Energy sources, transformation and conservation

Sources from which we get energy are **energy sources**.

| Renewable sources | Non-renewable sources |
|---|---|
| are replaced naturally and do not run out | cannot be replaced quickly once used up |
| sun, wind, flowing water (hydropower), tides, biogas, firewood (if forests are replanted) | coal, petroleum (petrol, diesel, kerosene, LPG), natural gas, nuclear fuel |
| mostly clean | cause pollution and greenhouse gases (except nuclear) |

Energy changes from one form to another: a hydropower plant changes the kinetic energy of
water into electrical energy; a bulb changes electrical energy into light and heat; our
body changes the chemical energy of food into mechanical energy and heat. The **law of
conservation of energy** states that energy can neither be created nor destroyed; it only
changes from one form to another. Nepal's rivers make **hydroelectricity** its main clean
energy source; solar panels and biogas plants are common in villages.

```photo id="sci10/solar-nepal" caption="Solar panels in Nepal change light energy into electrical energy — a renewable source useful where the grid has not reached." width="66"
```

## Chapter summary

- Energy is the capacity to do work (J); 1 calorie ≈ 4.2 J.
- Heat flows from higher to lower temperature. $F=\frac{9}{5}C+32$, $K=C+273$.
- **Conduction** (solids, no movement of particles), **convection** (liquids and gases,
  movement of particles), **radiation** (no medium, electromagnetic waves).
- Dark surfaces absorb and emit radiation well; white and shiny surfaces do not.
- Thermos flask: vacuum (no conduction/convection), silvering (no radiation), cork.
- Greenhouse effect: greenhouse gases trap heat; more gases → global warming.
- $Q=ms\Delta t$; water has a high specific heat capacity (4200 J/kg °C).
- Concave mirror converges (real images, except object within F); convex mirror diverges
  (virtual, erect, diminished image). $f=\frac{R}{2}$.
- Sound is a longitudinal mechanical wave; $v=f\lambda$, $T=\frac{1}{f}$; audible range
  20 Hz – 20 kHz; $I=\frac{P}{A}$ (W/m²), loudness in dB.

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Textbook exercises.)*

1. Transfer of heat by the actual movement of particles is <span class="marks">[1]</span>
   (a) conduction (b) convection (c) radiation (d) temperature
2. Heat travels in liquids and gases by <span class="marks">[1]</span>
   (a) conduction (b) convection (c) radiation (d) evaporation
3. Heat travels through a vacuum by <span class="marks">[1]</span>
   (a) conduction (b) convection (c) radiation (d) transpiration
4. In which case is heat transferred by radiation? <span class="marks">[1]</span>
   (a) a spoon kept in sunlight gets hot (b) a spoon in hot tea gets hot (c) a spoon held above a spirit lamp gets hot (d) cold water warms when a hot iron rod is put in it
5. The average temperature of the earth's surface is about <span class="marks">[1]</span>
   (a) 70 °F (b) 59 °F (c) 40 °F (d) 125 °F
6. Which is a mechanical wave? <span class="marks">[1]</span>
   (a) radio wave (b) gamma ray (c) sound wave (d) X-ray
7. Which mirror do we use daily to look at our face? <span class="marks">[1]</span>
   (a) plane (b) concave (c) convex (d) spherical
8. Which mirror can form a real image? <span class="marks">[1]</span>
   (a) plane (b) concave (c) convex (d) none
9. A real image is one that <span class="marks">[1]</span>
   (a) cannot be obtained on a screen (b) can be obtained on a screen (c) is always erect (d) is always magnified
10. A concave mirror is also called a <span class="marks">[1]</span>
   (a) plane mirror (b) diverging mirror (c) converging mirror (d) simple mirror
11. A ray through the centre of curvature of a concave mirror <span class="marks">[1]</span>
   (a) passes through F (b) is reflected back along the same path (c) becomes parallel to the axis (d) diverges
12. Frequency is the number of waves produced in <span class="marks">[1]</span>
   (a) 1 second (b) 2 seconds (c) 3 seconds (d) 4 seconds
13. The frequency range of audible sound is <span class="marks">[1]</span>
   (a) 2 Hz – 20 Hz (b) 20 Hz – 20 kHz (c) 20 kHz – 200 kHz (d) 2 Hz – 200 Hz
14. A sound with greater amplitude has <span class="marks">[1]</span>
   (a) more intensity (b) less intensity (c) the same intensity (d) no intensity
15. According to the textbook, a person who cannot hear even this level is deaf: <span class="marks">[1]</span>
   (a) 90 dB (b) 80 dB (c) 60 dB (d) 55 dB
16. Which animal can produce and hear ultrasound? <span class="marks">[1]</span>
   (a) elephant (b) bat (c) crocodile (d) rhino

::: note Answers to Group A
**1.** (b). **2.** (b). **3.** (c). **4.** (a) — the sun's heat crosses empty space. **5.** (b) — about 15 °C. **6.** (c). **7.** (a). **8.** (b). **9.** (b). **10.** (c). **11.** (b). **12.** (a). **13.** (b). **14.** (a) — $I\propto A^2$. **15.** (b). **16.** (b).
:::

**Group B — Short answer (2 marks each)**

1. Differentiate: (a) conductor and insulator of heat (b) mechanical and electromagnetic waves (c) sea breeze and land breeze. <span class="marks">[3]</span>
2. Give reasons: (a) Mud houses are cool in summer and warm in winter. (b) Tea cups are made of porcelain. (c) Light-coloured clothes are worn in summer. (d) Ventilators are made in the upper part of walls. (e) Transparent plastic covers an artificial greenhouse. <span class="marks">[5]</span>
3. What is convection? How does wind blow? Write two applications of convection. <span class="marks">[2]</span>
4. What is radiation? Write two applications. What is an electromagnetic wave? Give three examples. <span class="marks">[3]</span>
5. Draw a labelled diagram of a thermos flask and explain how it works. <span class="marks">[3]</span>
6. What is the greenhouse effect? Write its importance and two harmful effects. <span class="marks">[3]</span>
7. Differentiate: (a) concave and convex mirror (b) real and virtual image. Define principal axis, focus, centre of curvature and focal length. <span class="marks">[4]</span>
8. Give reasons: (a) A concave mirror is used in a solar cooker. (b) A convex mirror is used as a rear-view mirror. (c) Convex and plane mirrors cannot form real images. (d) A concave mirror is used for shaving. <span class="marks">[4]</span>
9. Differentiate: (a) wavelength and amplitude (b) infrasound and ultrasound. Write three uses of ultrasound. <span class="marks">[3]</span>
10. Why does the speed of sound stay the same when frequency changes? Why does sound become fainter as we move away from the source? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** (a) A conductor lets heat pass easily (copper, iron); an insulator does not (wood, plastic, wool). (b) See the table in 7.3.4. (c) See the table in 7.3.2.
**2.** (a) Mud is a poor conductor, so heat does not easily pass in or out through the walls. (b) Porcelain is a poor conductor, so the tea stays hot and the cup is safe to hold. (c) Light colours absorb less heat radiation. (d) Warm used air is lighter and rises; it goes out through the upper ventilator while fresh air enters below (convection). (e) It lets the sun's short-wave radiation in but traps the long-wave heat given out by the soil and plants.
**3.** Transfer of heat in liquids and gases by the movement of heated particles. Wind: the sun heats the ground; the air above becomes warm and light and rises; cooler air from nearby flows in to take its place — this moving air is wind. Applications: boiling water, sea and land breezes, fans and air conditioners, refrigerators.
**4.** Transfer of heat without a medium in the form of waves. Applications: sun heats the earth; warming near a fire; white clothes in summer; black solar cookers. An electromagnetic wave needs no medium and travels at $3\times10^8$ m/s in a vacuum: light, radio waves, X-rays (also infrared, gamma rays).
**5.** Draw as in the figure in 7.3.5. Vacuum between the double walls stops conduction and convection; silvered surfaces reflect heat radiation; cork stopper and pad are poor conductors. So heat neither enters nor leaves easily, and the liquid stays hot or cold.
**6.** The warming of the earth because greenhouse gases trap the heat radiated by it. Importance: keeps the average temperature about 15 °C instead of −18 °C so life can exist; greenhouses grow off-season vegetables. Harmful effects of its increase: global warming, melting glaciers and GLOF, sea-level rise, changed rainfall, lower crop yield.
**7.** See the tables in 7.5.1. Principal axis: the line through the pole and centre of curvature. Focus: the point on the axis where parallel rays meet (or seem to come from) after reflection. Centre of curvature: the centre of the sphere of which the mirror is part. Focal length: the distance from the pole to the focus.
**8.** (a) It is a converging mirror; it collects the sun's rays at its focus and produces great heat. (b) It always gives an erect, diminished image and a wide field of view of the traffic behind. (c) Their reflected rays never actually meet; they only appear to meet behind the mirror. (d) When the face is within F, a concave mirror gives an erect, enlarged image.
**9.** (a) Wavelength is the distance between two successive crests; amplitude is the maximum displacement of a particle from the mean position. (b) Infrasound is below 20 Hz (earthquakes, elephants); ultrasound is above 20 kHz (bats). Uses of ultrasound: USG of the womb, SONAR, killing bacteria, bloodless operations.
**10.** The speed depends only on the medium; since $v=f\lambda$ is fixed, a higher frequency gives a proportionally shorter wavelength. The energy spreads over a larger area and part is absorbed by the air, so intensity falls with distance.
:::

**Group C — Numerical and long answer (4 marks each)**

1. The speed of sound in air is 332 m/s and its frequency is 10 Hz. Find the wavelength. <span class="marks">[2]</span>
2. A sound has a wavelength of 22 m and frequency 10 Hz. Find its speed. <span class="marks">[2]</span>
3. If the speed of sound in air is 332 m/s, find the wavelengths of the shortest and longest sound waves that humans can hear. <span class="marks">[3]</span>
4. Sound of intensity $2\times10^{-5}$ W/m² spreads over 6 m² in 1 s. Find the energy carried. <span class="marks">[2]</span>
5. Draw ray diagrams for a concave mirror when the object is (i) beyond C (ii) at infinity (iii) between C and F, and write the nature of each image. <span class="marks">[4]</span>
6. How much heat is needed to raise 500 g of water from 25 °C to 85 °C? ($s=4200$ J/kg °C) <span class="marks">[2]</span>
7. Write the causes, two effects and two ways to control sound pollution. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $\lambda=\frac{v}{f}=\frac{332}{10}=33.2$ m. *(The textbook prints 33.3 m; the exact value is 33.2 m.)*
**2.** $v=f\lambda=10\times22=220$ m/s. *(The textbook's printed answer, 330 m/s, does not match the data; with 22 m and 10 Hz the speed is 220 m/s.)*
**3.** Shortest wavelength at the highest audible frequency, 20 000 Hz: $\lambda=\frac{332}{20000}=0.0166$ m. Longest at 20 Hz: $\lambda=\frac{332}{20}=16.6$ m.
**4.** $E=I\times A\times t=2\times10^{-5}\times6\times1=1.2\times10^{-4}$ J.
**5.** Use the three rules of 7.5.1. (i) Beyond C: image between F and C, real, inverted, diminished (figure in 7.5.1). (ii) At infinity: parallel rays meet at F — image at F, real, inverted, point-sized. (iii) Between C and F: image beyond C, real, inverted, magnified.
**6.** $m=500$ g $=0.5$ kg, $\Delta t=85-25=60$ °C. $Q=0.5\times4200\times60=126\,000$ J $=126$ kJ.
**7.** Causes: traffic and horns, factories, construction, loudspeakers and loud music. Effects: hearing loss and eardrum damage; high blood pressure, stress and sleeplessness; loss of concentration. Control: trees along roads, silencers and fewer horns, low-volume music and TV, industries away from settlements, awareness programmes.
:::

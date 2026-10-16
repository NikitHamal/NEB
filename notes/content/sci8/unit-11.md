---
subject: Science and Technology
grade: 8
unit: 11
title: The Earth and Universe
hours: 0
area: Science and Technology
---

The ground you stand on is a thin skin of rock over a ball of hot metal 6,400 km
across. Beyond it lies a star, eight planets, moons, asteroids and comets, and
beyond those, a hundred billion suns in our galaxy. This unit starts at your
feet — minerals, rocks and the inside of the earth — and travels outward to the
solar system, the stars and the space missions that Nepal has now joined.

::: key What this unit asks of you
You should be able to name the main metallic and non-metallic minerals and their
uses, classify rocks into three types with an example of each, describe the
internal structure of the earth, state the accepted age and the modern idea of
how the earth and the solar system formed, describe the solar system with the
planets in order and distinguish a planet, a satellite, an asteroid and a
comet, define a star, a constellation, a galaxy and a light year, and describe
what artificial satellites are used for.
:::

## 11.1 Minerals

A **mineral** is a naturally occurring solid substance with a definite chemical
composition and a regular internal structure. Minerals are the building blocks
of rocks. A mineral from which a metal can be extracted profitably is an
**ore**.

| | Metallic minerals | Non-metallic minerals |
|---|---|---|
| What they contain | a metal, often combined with oxygen or sulphur | no metal; salts, silicates, carbonates, fuels |
| Examples | iron ore (magnetite, haematite), copper ore, zinc blende, bauxite (aluminium), gold, silver | limestone, dolomite, mica, quartz, talc, graphite, salt, coal, petroleum |
| Used for | iron and steel, wire, machines, coins, ornaments | cement, glass, paint, lubricants, fertiliser, fuel |
| Where found in Nepal | iron in Ramechhap, Tanahun and the Kathmandu valley; copper in Ilam, Dhading and Bhojpur; zinc and lead in Ganesh Himal and Sindhupalchok | limestone in Chobhar, Surkhet and Dhading; talc in Darchula, Baitadi and Bajhang; mica in Taplejung, Nuwakot and Sankhuwasabha; magnesite in Dolakha |

::: caution Mining has two sides
A mine gives work and raw material, but it also removes the soil and the forest
above it, leaves a pit, and can pollute the river below with waste. In Nepal
much of the mineral wealth lies in fragile mountain ground, so mining is
allowed only with a plan for restoring the land. A mineral taken out of a
mountain cannot be put back.
:::

## 11.2 Rocks and the structure of the earth

A **rock** is a natural aggregate of one or more minerals. Rocks are grouped
into three types by how they were formed.

| Type | How it forms | Texture and example |
|---|---|---|
| Igneous | magma or lava cools and solidifies | crystals; granite (slow cooling, under ground), basalt (fast cooling, on the surface) |
| Sedimentary | layers of sand, mud, shells or gravel are compacted and cemented over a long time | layers and often fossils; sandstone, limestone, shale, conglomerate |
| Metamorphic | an existing rock is changed by great heat and pressure | banded or foliated; marble (from limestone), slate (from shale), gneiss (from granite), quartzite (from sandstone) |

```figure caption="The rock cycle. Any rock can become any other kind: heat and pressure make a metamorphic rock, melting and cooling make an igneous rock, and weathering, transport and cementing make a sedimentary rock."
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")
pos = {"Igneous": (5.0, 5.0), "Sedimentary": (8.4, 2.4), "Metamorphic": (1.6, 2.4)}
for name, (x, y) in pos.items():
    ax.text(x, y, name, ha="center", va="center", fontsize=7.4, color=INK,
            bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=ACCENT, lw=1.1))
edges = [("Igneous", "Sedimentary", "weathering, transport, cementing"),
         ("Sedimentary", "Metamorphic", "heat and pressure"),
         ("Metamorphic", "Igneous", "melting and cooling"),
         ("Sedimentary", "Igneous", "melting and cooling"),
         ("Metamorphic", "Sedimentary", "weathering, transport, cementing")]
for a, b, label in edges[:3]:
    xa, ya = pos[a]
    xb, yb = pos[b]
    ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1,
                                shrinkA=30, shrinkB=30,
                                connectionstyle="arc3,rad=0.18"))
ax.text(7.4, 4.1, "weathering,\\ntransport", ha="center", fontsize=6.0, color=MUTED)
ax.text(4.3, 2.0, "heat and pressure", ha="center", fontsize=6.0, color=MUTED)
ax.text(2.2, 4.1, "melting and\\ncooling", ha="center", fontsize=6.0, color=MUTED)
ax.text(5.0, 0.4, "the cycle has no beginning and no end", ha="center", fontsize=6.4,
        color=MUTED)
fig.tight_layout()
```

### 11.2.1 Inside the earth

```figure caption="A slice through the earth. The crust is thinner under the ocean than under a mountain range, and the temperature rises all the way to the core."
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.add_patch(plt.Circle((5.0, 3.0), 2.75, fc="#cfe0ea", ec=INK, lw=1.2))
ax.add_patch(plt.Circle((5.0, 3.0), 2.05, fc="#e6c9a8", ec=INK, lw=1.0))
ax.add_patch(plt.Circle((5.0, 3.0), 1.25, fc="#e8a03c", ec=INK, lw=1.0))
ax.add_patch(plt.Circle((5.0, 3.0), 0.6, fc="#f2d24b", ec=INK, lw=1.0))
ax.text(5.0, 3.0, "inner core", ha="center", va="center", fontsize=6.4, color=INK)
ax.text(5.0, 1.95, "outer core", ha="center", va="center", fontsize=6.6, color=INK)
ax.text(5.0, 1.05, "mantle", ha="center", va="center", fontsize=7.0, color=INK)
ax.text(5.0, 5.55, "crust", ha="center", va="center", fontsize=7.0, color=INK)
ax.annotate("", xy=(5.0, 5.4), xytext=(5.0, 5.85),
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
ax.text(0.35, 5.5, "thickness:", ha="left", fontsize=6.4, color=MUTED)
ax.text(0.35, 4.95, "crust 5-70 km", ha="left", fontsize=6.2, color=MUTED)
ax.text(0.35, 4.4, "mantle to 2900 km", ha="left", fontsize=6.2, color=MUTED)
ax.text(0.35, 3.85, "core to 6371 km", ha="left", fontsize=6.2, color=MUTED)
fig.tight_layout()
```

| Layer | Thickness | State and main composition |
|---|---|---|
| Crust | about 5 km under the ocean to about 70 km under mountains | solid rock; silicon, aluminium, oxygen |
| Mantle | down to about 2,900 km | mostly solid rock that flows very slowly; iron and magnesium silicates |
| Outer core | to about 5,150 km | liquid iron and nickel |
| Inner core | to the centre, 6,371 km | solid iron and nickel, about 5,500 °C |

The movement of the liquid outer core gives the earth its magnetic field. The
slow movement of the mantle moves the crustal plates, and where plates meet
there are earthquakes, volcanoes and mountain building — which is why the
Himalaya is still rising by a few millimetres a year.

```photo id="sci10/solar-system" caption="The planets of the solar system, in order from the Sun." width="74"
```

## 11.3 Origin and age of the earth

The earth is about **4.6 billion years (4,600 million years)** old. The age is
found by measuring the decay of radioactive elements in the oldest rocks and
meteorites.

The accepted explanation is the **nebular hypothesis**: a large cloud of gas and
dust began to contract under its own gravity; most of it collected in the
centre to form the sun, while the rest flattened into a spinning disc. In the
disc, dust and rock stuck together into larger and larger bodies, and these
**planetesimals** grew into the planets by collision. The young earth was
molten, and as it cooled the heavier materials sank to form the core while
lighter rock floated up to form the crust. The atmosphere and the oceans formed
later, from gases released from the interior and from water brought by comets
and icy bodies.

## 11.4 The solar system

The **solar system** consists of the sun, eight planets, their moons, dwarf
planets, asteroids, comets, meteoroids and dust. The sun contains more than
99 % of all the mass in the system.

| Order | Planet | Type | One fact |
|---|---|---|---|
| 1 | Mercury | terrestrial | smallest planet; no atmosphere worth speaking of |
| 2 | Venus | terrestrial | hottest planet, about 465 °C, because of its carbon dioxide atmosphere |
| 3 | Earth | terrestrial | the only planet known to have liquid water on the surface and life |
| 4 | Mars | terrestrial | the "red planet"; has the tallest volcano in the solar system |
| 5 | Jupiter | gas giant | the largest planet; has a great red spot storm |
| 6 | Saturn | gas giant | famous for its bright ring system |
| 7 | Uranus | ice giant | rotates on its side |
| 8 | Neptune | ice giant | farthest planet; strongest winds |

The four inner planets are small, rocky and close together. The four outer
planets are large, made mostly of gas and ice, and far apart. Between Mars and
Jupiter lies the **asteroid belt**.

| Body | What it is |
|---|---|
| Planet | a large body that orbits the sun, is nearly round and has cleared its orbit |
| Dwarf planet | round and orbits the sun, but has not cleared its orbit — Pluto, Ceres |
| Satellite (moon) | a natural body orbiting a planet; the earth has one |
| Asteroid | a small rocky body, most of them in the belt between Mars and Jupiter |
| Comet | a body of ice, dust and rock that develops a bright tail when it comes near the sun |
| Meteoroid | a small piece of rock or dust in space |
| Meteor | a meteoroid burning up in the atmosphere — a "shooting star" |
| Meteorite | a meteoroid that reaches the ground |

::: caution The moon does not shine
The moon has no light of its own; it reflects sunlight. That is why its phase
changes: as it goes round the earth we see different fractions of its lit half.
The phases repeat in about 29.5 days, which is the basis of the lunar calendar
used for Dashain, Tihar and other Nepali festivals.
:::

```photo id="sci8/sun-and-planets" caption="Stars compared in size. The Sun is an ordinary star; many others are far larger." width="68"
```

## 11.5 Stars, constellations and galaxies

A **star** is a huge ball of gas, mostly hydrogen, that gives out its own light
because nuclear reactions in its core release energy. The sun is the nearest
star, about 150 million km away. The next nearest star is about 4.2 light years
away.

A **light year** is the distance light travels in one year:
about $9.46\times10^{12}$ km. It is a unit of distance, not of time.

Stars are not all the same: they differ in mass, size, colour and temperature.
Blue-white stars are the hottest (over 25,000 °C at the surface), yellow stars
such as the sun are about 5,500 °C, and red stars are the coolest. A star is
born from a cloud of gas and dust, spends most of its life converting hydrogen
into helium, and ends as a white dwarf, a neutron star or a black hole,
depending on its mass.

Groupings of stars seen from the earth are **constellations**. The familiar ones
are the Great Bear (Saptarishi), Orion, and the Pole Star, which lies almost
above the north pole and is used to find direction at night.

::: photo id="sci8/sun-and-planets" caption="Relative sizes of the sun, the planets and some nearby stars. The sun is a hundred times wider than the earth, and the stars shown here make the sun look small." width="90"
key 1 The sun, a yellow star of average size
key 2 The planets, drawn to the same scale as the stars
key 3 Giant stars, hundreds of times wider than the sun
:::

A **galaxy** is a very large system of stars, gas and dust held together by
gravity. Our galaxy is the **Milky Way**, which contains about a hundred billion
stars, and the sun lies about two-thirds of the way out from its centre. There
are billions of galaxies; one of the nearest large ones, Andromeda, is about
2.5 million light years away.

## 11.6 Space exploration and artificial satellites

An **artificial satellite** is a machine put into orbit round the earth or
another body, with a rocket. The first was Sputnik 1, launched by the Soviet
Union in 1957; the first person in space was Yuri Gagarin in 1961; and people
first walked on the moon in 1969.

| Use of artificial satellites | What it does |
|---|---|
| Communication | carries telephone, internet and television signals between continents |
| Weather | photographs cloud systems and tracks cyclones so that warnings can be issued |
| Navigation | GPS tells a device its exact position, used in mapping and trekking |
| Remote sensing | maps land use, forests, glaciers, floods and crops |
| Scientific research | telescopes in orbit see the sky without the blurring of the atmosphere |
| Defence and disaster | monitors borders and helps in search and rescue |

Nepal joined this work in 2019 with **NepaliSat-1**, a small satellite built by
Nepali students and engineers with support from the Kyushu Institute of
Technology in Japan, launched on 18 April 2019. It carried a camera and a
magnetometer, and it put Nepal among the countries with a satellite of its own.
Satellite data is now used in Nepal for glacier monitoring, flood early warning
and mapping.

::: example Worked reasoning: how far is a light year?
**Problem.** Light travels at $3\times10^8$ m/s. Find the distance of one light
year in kilometres, and state the distance to a star 4.2 light years away.

**Solution.** Seconds in a year:
$60\times60\times24\times365=31\,536\,000$ s, about $3.15\times10^7$ s.

Distance in one year:

$$3\times10^8\times3.15\times10^7=9.45\times10^{15}\ \text{m}
=9.45\times10^{12}\ \text{km}$$

So one light year is about $9.46\times10^{12}$ km, roughly 9.5 million million
kilometres. A star 4.2 light years away is

$$4.2\times9.46\times10^{12}\approx4.0\times10^{13}\ \text{km}$$

**What it shows.** Even the nearest star is about 40 million million kilometres
away. This is why astronomers use the light year instead of the kilometre, and
why, when you look at a star, you are seeing it as it was years ago.
:::

::: example Worked reasoning: why the moon has phases
**Problem.** The moon goes round the earth in about 27.3 days, but the cycle of
phases takes about 29.5 days. Explain.

**Solution.** The moon shines only by reflected sunlight, so half of it is lit at
all times. As it moves round the earth, we see different fractions of the lit
half: new moon when it lies between the earth and the sun (lit side away from
us), full moon when the earth lies between (lit side towards us), and the
crescent and gibbous shapes in between.

The phases take longer than one orbit because the earth is also moving round the
sun. By the time the moon has completed one orbit round the earth, the earth has
moved on, so the moon must travel a little further to return to the same
position relative to the sun. That extra travel takes about 2.2 days, giving
29.5 days.

**Conclusion.** 27.3 days is the moon's orbital period; 29.5 days is the period
of the phases, which is what we actually watch.
:::

## Chapter summary

- A **mineral** is a natural solid with a definite composition; an **ore** is a
  mineral from which a metal can be extracted profitably.
- Metallic minerals in Nepal include iron, copper, zinc and lead; non-metallic
  ones include limestone, talc, mica, magnesite and graphite.
- Rocks are **igneous** (cooled magma or lava), **sedimentary** (compacted
  layers) or **metamorphic** (changed by heat and pressure); the rock cycle
  connects all three.
- The earth has a thin **crust**, a thick **mantle**, a liquid **outer core** and
  a solid **inner core**; the outer core gives the magnetic field.
- The earth is about **4.6 billion years** old; the nebular hypothesis explains
  the formation of the sun and the planets from a contracting cloud of gas and
  dust.
- The solar system has eight planets — Mercury, Venus, Earth, Mars, Jupiter,
  Saturn, Uranus, Neptune — with the asteroid belt between Mars and Jupiter.
- Planets orbit the sun; satellites orbit planets; asteroids are rocky; comets
  are icy and grow a tail near the sun; a meteor is a meteoroid burning in the
  atmosphere.
- A **star** makes its own light; a **constellation** is a pattern of stars as
  seen from the earth; a **galaxy** is a system of billions of stars; a **light
  year** is a distance of about 9.46 × 10¹² km.
- Artificial satellites serve communication, weather, navigation, remote
  sensing and research; Nepal launched **NepaliSat-1** in 2019.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these is a metamorphic rock? <span class="marks">[1]</span>
   (a) granite (b) sandstone (c) marble (d) basalt
2. The innermost layer of the earth is the <span class="marks">[1]</span>
   (a) crust (b) mantle (c) outer core (d) inner core
3. The accepted age of the earth is about <span class="marks">[1]</span>
   (a) 4.6 million years (b) 4.6 billion years (c) 46 million years
   (d) 460 million years
4. The largest planet in the solar system is <span class="marks">[1]</span>
   (a) Saturn (b) Jupiter (c) Neptune (d) Earth
5. A light year is a unit of <span class="marks">[1]</span>
   (a) time (b) distance (c) brightness (d) speed
6. Nepal's first satellite was <span class="marks">[1]</span>
   (a) Sputnik-1 (b) NepaliSat-1 (c) Gaganyaan (d) Chandrayaan

::: note Answers to Group A
**1.** (c) — marble is limestone changed by heat and pressure.
**2.** (d) — the solid iron-nickel inner core.
**3.** (b) — about 4,600 million, that is 4.6 billion, years.
**4.** (b) — Jupiter.
**5.** (b) — distance: the distance light travels in one year.
**6.** (b) — NepaliSat-1, launched on 18 April 2019.
:::

**Group B — Short answer (2 marks each)**

1. Distinguish between a mineral and an ore, and give one example of each.
   <span class="marks">[2]</span>
2. Write the three types of rock with one example of each.
   <span class="marks">[2]</span>
3. Distinguish between a planet and a satellite, and between an asteroid and a
   comet. <span class="marks">[2]</span>
4. Write any four uses of artificial satellites.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A mineral is a naturally occurring solid with a definite chemical
composition and a regular internal structure — for example quartz. An ore is a
mineral from which a metal can be extracted profitably — for example magnetite,
from which iron is extracted.
**2.** Igneous — granite (or basalt). Sedimentary — sandstone (or limestone,
shale). Metamorphic — marble (or slate, gneiss, quartzite).
**3.** A planet is a large, nearly round body that orbits the sun directly and
has cleared its orbit, such as the earth; a satellite is a body that orbits a
planet, such as the moon (or an artificial satellite launched by people). An
asteroid is a small rocky body, most of them in the belt between Mars and
Jupiter; a comet is a body of ice, dust and rock that develops a bright tail
when it comes near the sun.
**4.** Any four of: communication — carrying telephone, internet and television
signals; weather forecasting and cyclone warning; navigation, as with GPS;
remote sensing for mapping forests, glaciers, crops and floods; scientific
research; border monitoring and disaster search and rescue.
:::

**Group C — Long answer (4 marks each)**

1. Describe the internal structure of the earth with a diagram, giving the
   thickness and the state of each layer. State two effects of the movement
   inside the earth. <span class="marks">[4]</span>
2. What is the solar system? Write the eight planets in order from the sun and
   state one fact about any four of them. Distinguish between a meteor, a
   meteorite and a meteoroid. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Diagram.** A circle divided into four concentric parts, labelled from
the outside in. **Layers.** *Crust* — about 5 km thick under the ocean to about
70 km under mountain ranges; solid rock, mainly silicates of silicon,
aluminium and oxygen. *Mantle* — extends to about 2,900 km depth; hot rock that
is mostly solid but flows extremely slowly; iron and magnesium silicates.
*Outer core* — from about 2,900 km to about 5,150 km; liquid iron and nickel.
*Inner core* — from about 5,150 km to the centre at 6,371 km; solid iron and
nickel at about 5,500 °C. **Two effects.** (i) The movement of the liquid outer
core produces the earth's magnetic field, which protects us from much of the
solar wind and makes the compass work. (ii) The slow movement of the mantle
moves the crustal plates, so where plates meet we get earthquakes, volcanoes and
the rising of mountain ranges such as the Himalaya.
**2.** **The solar system** is the sun together with everything held by its
gravity — eight planets, their moons, dwarf planets, asteroids, comets,
meteoroids and dust. **Planets in order:** Mercury, Venus, Earth, Mars,
Jupiter, Saturn, Uranus, Neptune. **Facts (any four).** Venus is the hottest
planet because its carbon dioxide atmosphere traps heat. Earth is the only
planet known to have liquid water on its surface and life. Jupiter is the
largest planet and has a giant storm called the Great Red Spot. Saturn is
famous for its bright rings. Mars is called the red planet and has the tallest
volcano in the solar system. Uranus rotates on its side. Neptune is the farthest
planet and has the strongest winds. Mercury is the smallest planet and has
almost no atmosphere. **Meteor, meteorite, meteoroid.** A *meteoroid* is a small
piece of rock or dust travelling in space. A *meteor* is a meteoroid that enters
the earth's atmosphere and burns up, appearing as a streak of light or
"shooting star". A *meteorite* is a meteoroid that survives the passage through
the atmosphere and lands on the ground.
:::

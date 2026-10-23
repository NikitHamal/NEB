---
subject: Science and Technology
grade: 8
unit: 11
title: The Earth and Universe
hours: 0
area: Science and Technology
---

The earth is one small part of the **universe**, which contains nebulas, stars,
planets, asteroids, comets and meteors. The most accepted scientific explanation of
the origin of the universe is the **Big Bang theory**. In the beginning the earth was
too hot for life; it slowly cooled, its surface of rock, soil, minerals and water and
its atmosphere formed, and simple living beings appeared and evolved into today's
biodiversity. This unit, following the CDC textbook, studies minerals, the structure
and origin of the earth, the history of life on it, and the bodies of the universe —
asteroids, comets, meteors, galaxies and constellations — together with the solar
system and space exploration.

::: key What this unit asks of you
Define mineral and classify minerals (metallic, non-metallic, energy) with examples,
properties, uses and places in Nepal; explain the hypotheses of the origin of the earth;
describe the geological eras and the life of each; explain the Big Bang theory; and
describe asteroids, comets (with their parts), meteoroids–meteors–meteorites, galaxies
and constellations.
:::

## 11.1 Minerals: metallic and non-metallic, and their uses

The earth's crust is made of rocks, soil, sand and water, and all of these are made of
elements and compounds.

::: definition Mineral
In geology, a **mineral** is a naturally formed, solid, pure (homogeneous) substance with
a definite chemical composition. In daily use the word also means any useful substance
obtained from mines, such as coal, petroleum, limestone, marble, diamond, granite and
clay. The study of minerals is **mineralogy**.
:::

**Types of minerals**

| Type | Features | Sub-types and examples |
|---|---|---|
| **Metallic** (ores) | hard, lustrous, dense, good conductors of heat and electricity; metals are extracted from them | *ferrous* (contain iron): haematite, magnetite, limonite, siderite, pyrite; *non-ferrous*: ores of copper, lead, tin, aluminium, zinc; *precious*: gold, silver, platinum |
| **Non-metallic** | not lustrous, poor conductors, light, found in the upper crust | *gems*: diamond, emerald, sapphire, topaz, garnet; *non-gems*: silica (quartz), feldspar, mica, sulphur, graphite, gypsum, talc |
| **Energy minerals** | fuels from mines; non-renewable | coal (peat → lignite → bituminous → anthracite), petroleum, natural gas, radioactive uranium |

```figure caption="Classification of minerals."
fig, ax = plt.subplots(figsize=(5.1, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.2); ax.axis("off")
def box(x, y, t, c=ACCENT):
    ax.text(x, y, t, ha="center", va="center", fontsize=7.6, color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=c, lw=1.0))
box(5.0, 4.7, "Minerals", INK)
for x, t in [(1.7, "Metallic"), (5.0, "Non-metallic"), (8.3, "Energy")]:
    ax.plot([5.0, x], [4.45, 3.75], color=MUTED, lw=0.8)
    box(x, 3.5, t)
for x, t, px in [(0.6, "ferrous", 1.7), (1.7, "non-\nferrous", 1.7), (2.8, "precious", 1.7),
                 (4.3, "gems", 5.0), (5.7, "non-gems", 5.0)]:
    ax.plot([px, x], [3.25, 2.25], color=MUTED, lw=0.8)
    box(x, 1.95, t, SERIES[2])
for x, t in [(7.15, "coal"), (8.3, "oil, gas"), (9.5, "uranium")]:
    ax.plot([8.3, x], [3.25, 2.25], color=MUTED, lw=0.8)
    box(x, 1.95, t, SERIES[3])
for x, t in [(0.6, "haematite"), (1.7, "copper ore"), (2.8, "gold"), (4.3, "diamond"), (5.7, "mica")]:
    ax.text(x, 0.85, t, ha="center", fontsize=7.2, color=MUTED, style="italic")
fig.tight_layout()
```

**Properties of minerals:** they have various colours (iron ores black or reddish-brown,
gold and copper ores yellowish or red, muscovite colourless); most are **crystalline**
with fixed shapes (pyrite cubic, tourmaline prismatic), a few are amorphous (opal); they
are usually hard and lustrous; metallic minerals conduct heat and electricity, non-metallic
ones do not; they are homogeneous solids with a definite chemical composition — that is
why a mineral is called a pure chemical substance.

**Uses of minerals**

| Sector | Minerals and uses |
|---|---|
| Agriculture | nitrogen, phosphorus, potash, gypsum and sulphur give fertilisers, pesticides and micronutrients for crops |
| Industry | limestone (cement — e.g. Udayapur and Hetauda cement factories), silica (glass), mica, gypsum, magnesite; metals for cables, rods, tools and machines |
| Construction | stone, sand, gravel, gypsum; slate for roofs; marble and granite for floors, idols and inscriptions |
| Energy | coal (brick kilns, cement factories), petroleum (vehicles), graphite, zinc, lithium, manganese and lead in cells and batteries |

**Minerals in Nepal.** More than 60 kinds of minerals have been identified in Nepal. Iron,
copper and coal have been mined since ancient times (iron of Ramechhap, coal of Dang).
Effective exploration and sustainable commercial mining have not yet been done, mainly for
lack of research, technology, capital and roads.

| Mineral | Places (as given in the textbook) |
|---|---|
| Iron | Phulchoki (Lalitpur), Thoshe (Ramechhap) |
| Copper | more than 100 places |
| Zinc and lead | Ganesh Himal area |
| Gold | sand of the Kaligandaki, Sunkoshi, Rapti and Bishnumati rivers |
| Limestone | Udayapur, Makwanpur, Chobhar (Kathmandu) |
| Magnesite | Dolakha, Udayapur, Palpa |
| Phosphorite | Dang, Pyuthan, Baitadi |
| Marble and granite | Godawari (Lalitpur), Sindhuli |
| Slate | Dhankuta, Achham, Gorkha, Benighat (Dhading) |
| Coal | Dang, Palpa, Pyuthan |
| Rock salt | Mustang, Dolpa |
| Uranium | Upper Mustang |

## 11.2 Rocks and the structure of the earth

Minerals combine to form **rocks**. **Igneous rocks** (granite, basalt) form when hot molten
magma cools; **sedimentary rocks** (sandstone, limestone, shale) form when layers of
sediment are pressed together, and may contain fossils; **metamorphic rocks** (marble from
limestone, slate from shale) form when other rocks are changed by great heat and pressure.

```figure caption="Layers of the earth. Heavy iron and nickel sank to the core; lighter silicates make the mantle and crust."
fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_xlim(-3.4, 6.4); ax.set_ylim(-3.2, 3.2); ax.set_aspect("equal"); ax.axis("off")
for r, c in [(3.0, "#a7c4a0"), (2.8, "#e0a96d"), (1.6, "#e8743b"), (0.8, "#f4d03f")]:
    ax.add_patch(plt.Circle((0, 0), r, fc=c, ec=INK, lw=0.6))
for r0, y, t in [(2.95, 2.4, "crust (rock, 5–70 km)"), (2.2, 1.2, "mantle (hot rock)"),
                 (1.2, 0.0, "outer core (liquid iron, nickel)"), (0.4, -1.2, "inner core (solid)")]:
    ax.plot([r0 * 0.8, 3.4], [r0 * 0.5, y], color=INK, lw=0.6)
    ax.text(3.5, y, t, fontsize=7.4, color=INK, va="center")
fig.tight_layout()
```

## 11.3 Origin and age of the earth; history of life

From the age of rocks and fossils, the earth is estimated to be about **4.6 billion years**
old. Several hypotheses try to explain how it formed.

| Hypothesis | Proposed by | Main idea |
|---|---|---|
| **Nebular hypothesis** | Immanuel Kant (1755), modified by Pierre-Simon Laplace (1796) | a huge, flat, slowly spinning cloud of gas and dust (nebula) contracted by gravity; its centre became very hot and dense and formed the sun; the outer flattened part broke into rings or lumps that formed the planets, and smaller lumps formed satellites, asteroids and comets |
| **Collision (comet) hypothesis** — called the *planetesimal hypothesis* in the textbook | Georges Buffon (about 1745–1749) | a giant comet struck the sun at a low angle and splashed out matter; the pieces revolved round the sun and cooled into planets |
| **Passing-star (planetesimal) hypothesis** — called the *binary hypothesis* in the textbook | T. C. Chamberlin and F. R. Moulton (1905) | a star came close to the sun and pulled out matter, which formed small solid bodies (planetesimals) that joined into planets |
| **Tidal hypothesis** | James Jeans and Harold Jeffreys (around 1917–1919) | a giant star passing close to the sun pulled out a cigar-shaped tide of hot matter; small planets formed at its thin ends and big ones (Jupiter, Saturn) in the thick middle |

**Specialities of the nebular hypothesis:** it explains why all planets revolve round the
sun in nearly the same plane and the same direction, because they formed from one flattened,
spinning disc. It is the basis of the modern explanation. **Criticism of the passing-star
and binary ideas:** no partner star of the sun has ever been found, and such close passes of
stars are extremely rare.

### 11.3.1 History of the evolution of life (geological time scale)

The young earth was hot and unstable. Heavy metals (iron, nickel) sank to the core and
light ones (silicon, magnesium, aluminium) rose to the surface. Gases released from rocks —
water vapour, carbon dioxide, nitrogen, ammonia, methane — formed the atmosphere. Water
vapour condensed into heavy rain that filled the lowlands as oceans. Reactions among
hydrogen, oxygen, nitrogen and carbon formed biomolecules (proteins, nucleic acids), and the
first simple **prokaryotes** appeared in water. All present life evolved from them.

The earth's history is divided into **eons**, **eras** and periods.

```figure caption="Geological time scale (approximate ages in million years ago, as used in the textbook). The Cryptozoic eon covers about 88 % of the earth's history."
fig, ax = plt.subplots(figsize=(5.1, 2.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off")
segs = [("Cryptozoic\n(Precambrian)", 0.2, 6.4, "#cfcfcf", "4600–570"),
        ("Palaeozoic", 6.4, 8.0, SERIES[2], "570–240"),
        ("Mesozoic", 8.0, 9.1, SERIES[3], "240–65"),
        ("Cenozoic", 9.1, 9.8, SERIES[1], "65–now")]
for name, a, b, c, age in segs:
    ax.add_patch(plt.Rectangle((a, 2.0), b - a, 0.9, fc=c, ec="white", lw=1, alpha=0.85))
    ax.text((a + b) / 2, 1.6, age, ha="center", va="top", fontsize=7.2, color=INK)
ax.text(3.3, 2.45, "Cryptozoic eon (Precambrian)", ha="center", va="center", fontsize=7.8, color=INK)
for x, t, y in [(7.2, "Palaeozoic", 3.4), (8.55, "Mesozoic", 3.85), (9.45, "Cenozoic", 3.4)]:
    ax.plot([x, x], [2.9, y - 0.15], color=MUTED, lw=0.6)
    ax.text(x, y, t, ha="center", fontsize=7.6, color=INK)
ax.text(8.1, 0.65, "Phanerozoic eon", ha="center", fontsize=7.8, color=INK)
ax.plot([6.4, 9.8], [0.95, 0.95], color=MUTED, lw=0.8)
fig.tight_layout()
```

| Eon / era | Time (approx.) | Main events and life |
|---|---|---|
| **Cryptozoic eon** (Precambrian; "hidden life"): Archaeozoic, Proterozoic, Eozoic eras | 4600 to 570 million years ago | atmosphere, oceans and land formed; first unicellular life in water; later soft-bodied animals and algae |
| **Palaeozoic era** (Phanerozoic eon) | 570 to 240 million years ago | many invertebrates (trilobites, molluscs, corals, jellyfish), fishes including lung-fishes, amphibians (frogs) and early reptiles; algae, mosses, ferns and tree-fern forests; ended with mass extinction |
| **Mesozoic era** — "era of reptiles", "era of conifers" (gymnosperms) | 240 to 65 million years ago | dinosaurs evolved (Triassic), dominated (Jurassic) and died out at the end of the Cretaceous after meteor impacts and volcanic eruptions; pines and cycads; toothed birds, mosquitoes, small mammals, first flowering plants |
| **Cenozoic era** — "era of mammals", "era of flowering plants" | 65 million years ago to now | continents separated; Himalaya rose; elephants, horses, rhinos, whales, primates, entelodont (giant boar), woolly mammoths; monocot and dicot plants; humans |

The first human-like ancestors appeared about 6 million years ago and walked upright about
4 million years ago. Modern humans (*Homo sapiens*) appeared roughly 300 000 years ago, and
farming, settled villages and organised society began only about 10 000–12 000 years ago
(the Holocene epoch). (Ages of the eras are approximate; newer measurements give about
541 and 252 million years for the start of the Palaeozoic and Mesozoic.)

::: example How long was the Cryptozoic eon?
**Problem.** The earth formed about 4600 million years ago and the Cryptozoic eon ended about
570 million years ago. What percentage of the earth's history does it cover?
**Solution.** Duration $=4600-570=4030$ million years.
Percentage $=\frac{4030}{4600}\times100\%\approx87.6\%$, i.e. about **88 %**, so the
Phanerozoic eon is only about 12 %.
:::

The **Cryptozoic eon** was unsuitable for complex life because the earth was still hot, the
atmosphere had little oxygen and there was no ozone layer to block ultraviolet rays, so only
simple life could exist, and only in water.

## 11.4 The solar system: planets, satellites, asteroids, comets and meteors

The **solar system** is the sun with all the bodies that revolve round it: **eight planets**
— Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune — their **satellites**
(moons), dwarf planets such as Pluto, asteroids, comets and meteoroids. Mercury, Venus,
Earth and Mars are small rocky planets; Jupiter, Saturn, Uranus and Neptune are giant
planets made mostly of gas. The earth has one natural satellite, the Moon.

```photo id="sci10/solar-system" caption="The planets of the solar system in order from the Sun: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune." width="72"
```

### 11.4.1 Asteroids

**Asteroids** (minor planets) are small, irregular masses of rock and metal that revolve
round the sun. Most lie in the **asteroid belt** between Mars and Jupiter; many icy bodies
lie beyond Neptune in the **Kuiper belt**, where the dwarf planet Pluto also lies.
**Trojans** share the orbit of Jupiter (or Mars). **Near-earth asteroids** cross the earth's
orbit and may hit it, causing great destruction. Asteroids are from about 1 km to about
1000 km across; **Ceres**, the largest, is nearly round, about 940 km across; Eros is
elongated, about 17 km. Their gravity is too weak to pull them into a round shape.

### 11.4.2 Comets

**Comets** are small bodies of **ice, dust, rock fragments and gases** that move round the sun
in **highly elliptical orbits**. Near the sun they grow long, bright tails.

```figure caption="Parts of a comet. The tails always point away from the sun, pushed by the solar wind."
fig, ax = plt.subplots(figsize=(5.0, 2.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off")
ax.add_patch(plt.Circle((0.6, 2.2), 0.45, fc="#ffd54f", ec="none"))
ax.text(0.6, 1.4, "sun", ha="center", fontsize=7.6, color=INK)
ax.annotate("", xy=(2.3, 2.2), xytext=(1.2, 2.2), arrowprops=dict(arrowstyle="->", color=MUTED))
ax.text(1.75, 2.45, "solar wind", ha="center", fontsize=7.2, color=MUTED)
ax.add_patch(plt.Circle((3.2, 2.2), 0.5, fc="#dfe9f5", ec=ACCENT, lw=0.8))
ax.add_patch(plt.Circle((3.2, 2.2), 0.12, fc=INK))
ax.add_patch(plt.Polygon([[3.5, 2.55], [9.4, 3.9], [9.6, 3.0], [3.6, 2.3]], fc="#f2f2f2", ec=MUTED, lw=0.6))
ax.add_patch(plt.Polygon([[3.6, 2.1], [9.6, 1.6], [9.6, 1.3], [3.55, 1.95]], fc="#cfe0f5", ec=ACCENT, lw=0.6))
ax.text(7.4, 4.25, "dust tail (white, broad)", ha="center", fontsize=7.4, color=INK)
ax.text(6.8, 1.15, "ion (gas) tail (bluish, straight)", ha="center", fontsize=7.4, color=ACCENT)
ax.plot([3.2, 3.0], [2.08, 0.75], color=MUTED, lw=0.6); ax.text(3.0, 0.5, "nucleus (ice and dust)", ha="center", fontsize=7.4, color=INK)
ax.plot([3.4, 4.2], [2.65, 3.95], color=MUTED, lw=0.6); ax.text(4.25, 4.05, "coma (glowing cloud)", fontsize=7.4, color=INK)
fig.tight_layout()
```

**Parts:** the solid icy **nucleus** in the centre; the **coma**, a bright cloud of evaporated
gas and dust round the nucleus when it comes near the sun; and the **tails** — a thick, white
**dust tail** and a thin, bluish **ion (plasma) tail** — which always point **away from the
sun** because the solar wind pushes them. The tail grows as the comet approaches the sun and
shrinks and disappears as it moves away.

Comets take from about 2 to hundreds of thousands of years to go round the sun:
**Encke** about 3.3 years, **Halley** about 76 years (it will next be seen in 2061),
**Hyakutake** (seen in 1996) tens of thousands of years. **Endocomets** stay within the
Kuiper belt; **exocomets** come from beyond the solar system. Comet **Shoemaker–Levy 9**
crashed into **Jupiter in 1994**. Each time a comet passes the sun it loses some ice and gas;
after many rounds it has lost all its volatile matter and becomes a rocky **extinct comet**,
like an asteroid.

| Asteroid | Comet |
|---|---|
| rock and metal | ice, dust, rock and gas |
| nearly circular orbits, mostly between Mars and Jupiter | highly elliptical orbits reaching the Kuiper belt and beyond |
| no tail | develops a coma and tails near the sun |

### 11.4.3 Meteoroids, meteors and meteorites

**Meteoroids** are small pieces of rock and metal wandering in the solar system, from dust
grains to small asteroids. When one enters the earth's atmosphere at a very high speed (about
11–72 km/s), friction with the air (in the mesosphere) makes it burn and leave a bright streak
of light — a **meteor** ("shooting star"). Meteors are seen only at night because sunlight
hides them by day. Most burn up completely; a piece that reaches the ground is a
**meteorite**. When many meteors fall in one region at one time it is a **meteor shower**.
Craters on the Moon were made by meteorites, because the Moon has no atmosphere to burn them.

| Meteor | Meteorite |
|---|---|
| streak of light made by a burning meteoroid in the air | remains of a meteoroid that reach the earth's surface |
| burns up completely | does not burn completely; may make a crater |

## 11.5 The universe, stars, constellations and galaxies

The endless region around us is **space**; the visible part of it above us is the **sky**.
The **universe** is the total of all space, time, matter and energy. The part we can observe
with the most powerful telescopes is the **observable universe**, about **93 billion
light years** across (about 46 billion light years in every direction from us). A **light
year** is the distance light travels in a vacuum in one year, about **9.46 × 10¹² km**. The
study of the universe is **astronomy**.

::: example Distances in light years
**Problem (a).** The star Proxima Centauri is about 4.2 light years away. Express this in km.
**Solution.** $4.2\times9.46\times10^{12}=39.7\times10^{12}\approx4.0\times10^{13}$ km.

**Problem (b).** Sunlight takes about 8 minutes 20 seconds to reach the earth. Taking the speed
of light as $3\times10^5$ km/s, find the distance of the sun.
**Solution.** $t=8\times60+20=500$ s. Distance $=3\times10^5\times500=1.5\times10^8$ km
(150 million km).
:::

::: example When will a comet return?
**Problem.** Halley's comet was last seen from the earth in 1986. Its period is about 75–76 years.
When will it be seen again?
**Solution.** $1986+75=2061$. It is expected in **2061**.
:::

### 11.5.1 The Big Bang theory

In the 1920s **Edwin Hubble** observed that distant galaxies are moving away from us, and in
**1927** the Belgian scientist **Georges Lemaître** explained that the universe is
**expanding**. If the expansion is run backwards, all matter and energy come together into
one extremely hot, dense point (Lemaître's "primeval atom"). About **13.8 billion years
ago** this exploded and began expanding — the **Big Bang**. As it expanded and cooled,
subatomic particles formed, then atoms and molecules, and from them, over time, galaxies,
nebulas, stars and planets. Stephen Hawking explained the beginning mathematically in his book
*A Brief History of Time*.

### 11.5.2 Stars and galaxies

A **star** is a huge ball of hot gas that produces its own heat and light by nuclear fusion.
The sun is an ordinary, medium-sized star; many stars are far larger.

```photo id="sci8/sun-and-planets" caption="Planets and stars compared in size. Panels 1–2: the planets (Earth is small beside Jupiter). Panel 3: the Sun dwarfs Jupiter but is small beside the star Sirius. Panels 4–6: giant stars such as Arcturus, Aldebaran, Betelgeuse and VY Canis Majoris are far larger still." width="84"
```

A **galaxy** is a huge collection of millions to billions of stars, together with nebulas
(clouds of gas and dust), planetary systems and dark matter, held together by gravity. Galaxies
may be spiral, elliptical, lens-shaped, ring-shaped or irregular. Our solar system is in the
**Milky Way**, a spiral galaxy of roughly **100–400 billion stars**; the sun is one of them.
Other galaxies: Andromeda, Whirlpool, Sombrero. There are hundreds of billions of galaxies in
the observable universe, and many have a black hole at the centre.

### 11.5.3 Constellations

A **constellation** is a group of stars that forms a pattern in the sky, imagined as an
animal, a person or an object. Astronomers recognise **88 constellations**. The 12 that lie
along the **ecliptic** (the sun's apparent yearly path) are the **zodiac**: Aries, Taurus,
Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius and Pisces.
Others: **Ursa Major** (the Great Bear; its seven bright stars are the *Saptarishi*), Orion,
Cassiopeia (five bright stars in a W shape), Ursa Minor (containing the Pole Star), Draco.
**Crux** is the smallest and **Hydra** the largest. Before watches and compasses, people used
constellations to tell the time, the season and the direction.

| Galaxy | Constellation |
|---|---|
| a real system of billions of stars bound by gravity | a pattern of stars as seen from the earth; the stars may be very far apart |
| looks like a faint patch of light | stars seen individually with the naked eye |
| e.g. Milky Way, Andromeda | e.g. Ursa Major, Orion |

## 11.6 Space exploration and artificial satellites; Nepal in space science

An **artificial satellite** is a human-made object placed in orbit round the earth or another
body. The first was **Sputnik 1** (USSR, 1957). Humans first landed on the Moon on **Apollo
11** in **1969**. The **International Space Station** has been occupied continuously since
2000. Satellites are used for communication (TV, telephone, internet), weather forecasting,
navigation (GPS), mapping and disaster monitoring, and telescopes in space (such as Hubble)
study distant galaxies.

**Nepal in space science.** Nepal's first satellite, **NepaliSat-1**, a small cube-shaped
satellite built by Nepali engineers at Kyushu Institute of Technology, Japan, under the BIRDS
project, was launched in **2019** and placed in orbit from the International Space Station. It
took photographs of Nepal and collected data for mapping. Nepal also uses satellites for weather
forecasting, television and communication.

## Chapter summary

- Mineral: natural, solid, homogeneous substance of definite composition; types —
  metallic (ferrous, non-ferrous, precious), non-metallic (gems, non-gems), energy minerals.
- Nepal has more than 60 kinds of minerals; e.g. iron at Phulchoki, limestone at Udayapur,
  magnesite at Dolakha, uranium in Upper Mustang.
- Earth's layers: crust, mantle, outer core (liquid), inner core (solid). Rocks: igneous,
  sedimentary, metamorphic.
- Earth is about 4.6 billion years old. Hypotheses: nebular (Kant, Laplace), collision
  (Buffon), passing-star / planetesimal (Chamberlin–Moulton), tidal (Jeans–Jeffreys).
- Eras: Cryptozoic (simple life), Palaeozoic (invertebrates, fish, amphibians, ferns),
  Mesozoic (reptiles, dinosaurs, conifers), Cenozoic (mammals, flowering plants, humans).
- Big Bang: about 13.8 billion years ago; the universe is expanding (Hubble, Lemaître).
- Asteroids: rocky, between Mars and Jupiter. Comets: icy, nucleus + coma + tails pointing
  away from the sun. Meteor = burning meteoroid; meteorite = piece that reaches the ground.
- Galaxy: billions of stars (Milky Way); constellation: star pattern (88; 12 zodiac).
- 1 light year ≈ 9.46 × 10¹² km. Nepal's first satellite NepaliSat-1 (2019).

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Textbook exercises.)*

1. The branch of science that studies minerals is <span class="marks">[1]</span>
   (a) geology (b) palaeontology (c) mineralogy (d) archaeology
2. Which mineral is necessary for the proper growth of plants? <span class="marks">[1]</span>
   (a) nitrogen (b) dolomite (c) uranium (d) granite
3. Which statement describes the tidal hypothesis? <span class="marks">[1]</span>
   (a) the earth formed from matter splashed out when two stars collided (b) the earth formed from a hot lump pulled from the sun by a giant star passing close by (c) the earth formed from nebular dust (d) the earth formed from the explosion of a heavenly body
4. Dinosaurs evolved and became extinct in the <span class="marks">[1]</span>
   (a) Precambrian (b) Palaeozoic (c) Mesozoic (d) Cenozoic
5. Who put forward the idea of the expanding universe? <span class="marks">[1]</span>
   (a) Einstein (b) Lemaître (c) Halley (d) Pythagoras
6. Which comet crashed into Jupiter? <span class="marks">[1]</span>
   (a) Shoemaker–Levy 9 (b) Bennett (c) Tempel–Tuttle (d) Halley
7. Trojans are asteroids that <span class="marks">[1]</span>
   (a) lie in the Kuiper belt (b) move along the orbit of Jupiter or Mars (c) burn in the atmosphere (d) have a long bright tail
8. The nucleus of a comet is made of <span class="marks">[1]</span>
   (a) rock, metal and dust (b) ice, gas and dust (c) stars and dark matter (d) stars and nebular clouds

::: note Answers to Group A
**1.** (c). **2.** (a). **3.** (b). **4.** (c). **5.** (b). **6.** (a) — in 1994. **7.** (b). **8.** (b).
:::

**Group B — Short answer (2 marks each)**

1. Differentiate: (a) metallic and non-metallic minerals (b) Palaeozoic and Cenozoic era. <span class="marks">[2]</span>
2. Give reasons: (a) Minerals are called pure chemical substances. (b) The Mesozoic era is called the era of conifers. (c) Living beings appeared only a very long time after the earth formed. <span class="marks">[3]</span>
3. What is a mineral? Give examples. Draw a flowchart of the types of minerals. <span class="marks">[2]</span>
4. Explain the importance of minerals for Nepal. List five minerals with their places and uses. <span class="marks">[3]</span>
5. Which era was unsuitable for the evolution of complex life, and why? <span class="marks">[2]</span>
6. When did mammoths with long tusks and lung-fishes evolve? Name the era of: tree-fern, entelodont boar, dinosaur, frog, monocot plants, bacteria, mosquito, trilobite, jellyfish. <span class="marks">[3]</span>
7. Differentiate: (a) meteor and meteorite (b) galaxy and constellation (c) asteroid and comet. <span class="marks">[3]</span>
8. Give reasons: (a) Near-earth asteroids are dangerous. (b) Comets gradually lose their material. (c) Most meteors are destroyed before reaching the ground. (d) Galaxies are important for studying the universe. <span class="marks">[4]</span>
9. Explain "meteor shower" and "observable universe". <span class="marks">[2]</span>
10. Why are Nepal's minerals not yet mined sustainably? Which minerals are mined traditionally, and what should be done? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** (a) Metallic minerals are hard, lustrous, dense ores that conduct heat and electricity and give metals (haematite, copper ore, gold); non-metallic minerals are not lustrous, are poor conductors and light (mica, gypsum, diamond). (b) Palaeozoic (570–240 million years ago): invertebrates, fish, amphibians, ferns; Cenozoic (65 million years ago to now): mammals, flowering plants and humans.
**2.** (a) A mineral is homogeneous with a definite chemical composition, like a pure compound or element. (b) Large gymnosperms (conifers) such as pines and cycads covered almost all moist land then. (c) The early earth was very hot and unstable, without oceans or a suitable atmosphere; these took hundreds of millions of years to form.
**3.** See the definition and the figure in 11.1 (metallic: ferrous, non-ferrous, precious; non-metallic: gems, non-gems; energy: coal, petroleum and gas, radioactive).
**4.** Minerals give raw materials for industries (cement, glass, metals), fertilisers for farming, building materials and energy; mining can create jobs and income and reduce imports. Examples: iron — Phulchoki — tools and rods; limestone — Udayapur — cement; magnesite — Dolakha — heat-resistant bricks; slate — Dhankuta — roofing; coal — Dang — fuel for kilns.
**5.** The Cryptozoic (Precambrian) eon: the earth was hot, the atmosphere had little oxygen and no ozone layer, so only simple unicellular life could exist in water.
**6.** In the Cenozoic era (mammoths) and the Palaeozoic era (lung-fishes). Tree-fern — Palaeozoic; entelodont — Cenozoic; dinosaur — Mesozoic; frog — Palaeozoic; monocots — Cenozoic; bacteria — Cryptozoic (Precambrian); mosquito — Mesozoic; trilobite — Palaeozoic; jellyfish — Palaeozoic (soft-bodied ancestors appeared at the end of the Precambrian).
**7.** See the tables in 11.4.2, 11.4.3 and 11.5.3.
**8.** (a) Their orbits cross the earth's orbit, so one may hit the earth and cause great destruction, as at the end of the Mesozoic. (b) Each time they pass close to the sun, its heat evaporates some of their ice and gas, which the solar wind blows away as tails. (c) They enter the atmosphere at very high speed, and friction with air heats and burns them up. (d) Galaxies are the basic large units of the universe; studying them tells us about its structure, expansion and age.
**9.** A meteor shower is the fall of many meteors in one region of the sky at one time. The observable universe is the part of the universe that can be seen with our most powerful telescopes, about 93 billion light years across.
**10.** Lack of research, modern technology, capital, skilled people and roads, and weak policy. Traditionally mined: iron, copper, coal, gold (from river sand), slate, limestone. To use them sustainably: survey and research, use modern and safe methods, protect the environment and local people, and add value inside the country.
:::

**Group C — Long answer (4 marks each)**

1. What are the hypotheses about the origin of the earth? Explain the nebular hypothesis. <span class="marks">[4]</span>
2. Describe the Mesozoic era. Why did dinosaurs become extinct, and what would happen to the biological balance if they were still alive? <span class="marks">[4]</span>
3. Describe the Big Bang theory in brief. <span class="marks">[4]</span>
4. What is a comet? Explain its parts with a diagram. <span class="marks">[4]</span>
5. What are asteroids? Write their characteristics. What are meteoroids and how do they become meteors? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Nebular (Kant 1755, Laplace 1796), collision (Buffon), passing-star / planetesimal (Chamberlin and Moulton, 1905) and tidal (Jeans and Jeffreys). *Nebular:* a huge, flat, slowly spinning nebula of gas and dust contracted under its own gravity; its centre grew hot and dense and became the sun; as it spun faster, the outer part flattened and broke into rings or lumps that collected matter and became planets; smaller lumps became satellites, and leftover matter formed asteroids and comets. It explains why the planets revolve in one plane and one direction.
**2.** 240–65 million years ago (textbook values); climate became drier with seasons; conifer forests; reptiles, especially dinosaurs, dominated land, water and air; toothed birds, small mammals and the first flowering plants appeared. Dinosaurs died out at the end of the Cretaceous, probably because of huge meteorite impacts and volcanic eruptions that filled the air with fire, dust and poisonous gases. If they were alive, large dinosaurs would compete with or prey on mammals, including humans, and the present food webs could not exist in their present form.
**3.** Hubble found that distant galaxies are moving away; Lemaître (1927) explained that the universe is expanding. Reversing the expansion, all matter and energy were once in one extremely hot, dense point (primeval atom). About 13.8 billion years ago it exploded — the Big Bang — and expanded rapidly; as it cooled, subatomic particles, then atoms and molecules, and finally galaxies, stars and planets formed. The universe is still expanding.
**4.** A small body of ice, dust, rock and gas moving round the sun in a highly elliptical orbit. Parts (figure in 11.4.2): nucleus — solid icy centre; coma — glowing cloud of gas and dust round the nucleus near the sun; tails — a white dust tail and a bluish ion tail, pointing away from the sun because of the solar wind.
**5.** Asteroids are small, irregular rocky and metallic bodies revolving round the sun, mostly between Mars and Jupiter. Characteristics: irregular shape (weak gravity), size about 1–1000 km (Ceres about 940 km), made of rock, metal and clay, orbits slightly irregular so they collide; some are Trojans, some near-earth asteroids. Meteoroids are small pieces of rock and metal in the solar system; when one enters the atmosphere at high speed, friction with the air makes it glow and burn, giving a streak of light — a meteor.
:::

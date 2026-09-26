---
subject: Chemistry
grade: 12
unit: 19
title: Cement
hours: 4
area: Applied Chemistry
---

Cement is the powder that turns sand, gravel and water into rock. Nepal alone
consumes several million tonnes of it every year — in the pillars of a Kathmandu
apartment, in a Karnali suspension-bridge anchor block, in every canal and
culvert. Chemically it is a mixture of **calcium silicates and aluminates** made
by roasting limestone with clay, and its usefulness comes from one property:
mixed with water it sets and hardens *hydraulically*, that is, even under water.

::: key What the examiner wants from this unit
Four repeat questions: the **raw materials** and the oxide each supplies; the
**three stages** of manufacture with the rotary-kiln temperature zones and the
reactions in each; the **role of gypsum**; and a comparison of **OPC with PPC**.
A flow-sheet diagram is worth full marks on its own — practise drawing it.
:::

## 19.1 Introduction

::: definition Cement
Portland cement is a finely ground hydraulic binder made by burning a
proportioned mixture of calcareous (lime-bearing) and argillaceous (clay-bearing)
materials at about 1400–1500 °C and grinding the resulting clinker with a little
gypsum. Mixed with water it sets and hardens by **hydration**, and does so under
water as well as in air.
:::

Joseph Aspdin patented it in Leeds in **1824** and called it *Portland* cement
because the set product resembled the building stone quarried on the Isle of
Portland. Cement with sand and water gives **mortar**; with sand, aggregate and
water it gives **concrete**; with steel bars embedded, **reinforced concrete
(RCC)**.

| Oxide | Symbol | Percentage in OPC | Supplied by |
|---|---|---|---|
| Calcium oxide (lime) | CaO | 60–67 % | limestone |
| Silica | SiO₂ | 17–25 % | clay, shale, sand |
| Alumina | Al₂O₃ | 3–8 % | clay, bauxite |
| Ferric oxide | Fe₂O₃ | 0.5–6 % | clay, iron ore |
| Magnesia | MgO | 0.1–4 % | dolomitic limestone |
| Sulphur trioxide | SO₃ | 1–3 % | added gypsum |

Two ratios control the quality of the raw mix:

$$ \text{hydraulic modulus} = \frac{\%\,\mathrm{CaO}}{\%\,\mathrm{SiO_2} + \%\,\mathrm{Al_2O_3} + \%\,\mathrm{Fe_2O_3}} \approx 2 $$

$$ \text{silica modulus} = \frac{\%\,\mathrm{SiO_2}}{\%\,\mathrm{Al_2O_3} + \%\,\mathrm{Fe_2O_3}} = 2.5\ \text{to}\ 4 $$

Too much lime leaves **free lime** in the clinker, which slakes slowly in the
hardened concrete and cracks it — the cement is *unsound*. Too little lime gives a
weak, quick-setting cement.

## 19.2 Raw materials for cement production

| Class | Material | Oxide supplied |
|---|---|---|
| **Calcareous** | limestone, chalk, marl, sea shells | CaO |
| **Argillaceous** | clay, shale, slate | SiO₂, Al₂O₃, Fe₂O₃ |
| **Corrective** | sand or quartzite; bauxite or laterite; iron ore or pyrite cinder | SiO₂; Al₂O₃; Fe₂O₃ |
| **Retarder** | gypsum, CaSO₄·2H₂O (2–5 %, added at the end) | SO₃ |
| **Fuel** | coal, petroleum coke, furnace oil | — |
| **Pozzolana** (for PPC only) | fly ash, volcanic ash, calcined clay | reactive SiO₂ |

Roughly **1.5 tonnes of limestone** and 0.4 tonne of clay are needed per tonne of
cement, which is why every cement plant sits on top of a limestone deposit rather
than near its customers.

## 19.3 Main steps in cement production

**(a) Crushing, grinding and mixing.** Quarried limestone is crushed to about
25 mm, blended with clay in the correct proportion and ground fine. Two routes
exist:

| | Wet process | Dry process |
|---|---|---|
| Raw mix prepared as | slurry with 35–50 % water | dry powder ("raw meal") |
| Mixing quality | excellent, easy to correct | needs careful blending silos |
| Fuel needed | high (water must be boiled off) | low — about 40 % less |
| Used today | old or very wet deposits | almost all modern plants, with preheaters |

**(b) Strong heating (burning) in the rotary kiln.** The raw mix is fed into the
upper end of a steel cylinder 60–150 m long and 3–8 m across, lined with
refractory brick, inclined about 1 in 30 and rotating at 1–2 revolutions per
minute. Pulverised coal and hot air are blown in at the lower end, so the charge
slides down *against* the rising flame and gets hotter as it travels.

```figure caption="Rotary kiln with its temperature zones. The charge enters cold at the upper end and travels down against the flame, leaving the lower end as red-hot clinker nodules."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2,3.3))
ax.set_xlim(0, 13.2); ax.set_ylim(0.2, 10.8); ax.axis('off')

P0 = np.array([2.3, 7.6]); P1 = np.array([9.9, 5.8]); th = 0.58
ang = np.degrees(np.arctan2(P1[1]-P0[1], P1[0]-P0[0])) * 0.78
zones = [(0.00, 0.22, '#eef2f7', 'drying',     '≤ 400 °C',      4.2),
         (0.22, 0.56, '#dbe8f6', 'calcination','900–1000 °C',   4.2),
         (0.56, 0.86, '#f7d5c8', 'clinkering', '1400–1500 °C',  4.2),
         (0.86, 1.00, '#e2efe2', 'cooling',    '≈ 1000 °C',     3.55)]
for a, b, c, name, temp, ty in zones:
    A = P0 + (P1-P0)*a; B = P0 + (P1-P0)*b
    ax.add_patch(Polygon([[A[0], A[1]+th], [B[0], B[1]+th],
                          [B[0], B[1]-th], [A[0], A[1]-th]],
                         closed=True, fc=c, ec=INK, lw=1.1))
    M = (A+B)/2
    ax.text(M[0], M[1], name, ha='center', va='center', fontsize=6.8,
            color=INK, rotation=ang, rotation_mode='anchor')
    ax.annotate(temp, xy=(M[0], M[1]-th), xytext=(M[0], ty),
                ha='center', va='top', fontsize=7.4, color=INK,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))

ax.annotate('raw meal feed in', xy=(2.32, 7.85), xytext=(0.05, 8.75),
            fontsize=7.6, color=SERIES[0], ha='left', va='center',
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.3,
                            mutation_scale=11))
ax.annotate('', xy=(2.0, 9.8), xytext=(2.75, 8.2),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2,
                            mutation_scale=10))
ax.text(2.15, 10.0, 'hot flue gas  →  dust precipitator', fontsize=7.4,
        color=MUTED, ha='left', va='center')
ax.annotate('pulverised coal\n+ hot air', xy=(10.05, 6.05), xytext=(13.15, 8.1),
            fontsize=7.6, color='#A8271F', ha='right', va='center',
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.3,
                            mutation_scale=11))

ax.add_patch(FancyBboxPatch((9.1, 1.85), 2.6, 1.05,
                            boxstyle='round,pad=0.08', fc='#f2f4f7',
                            ec=INK, lw=1.0))
ax.text(10.4, 2.38, 'grate cooler', fontsize=7.6, ha='center', va='center',
        color=INK)
ax.annotate('', xy=(10.5, 2.95), xytext=(10.0, 5.2),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.3,
                            mutation_scale=11))
ax.text(10.65, 4.75, 'clinker', fontsize=7.4, color=INK, ha='left')
ax.text(5.6, 0.75, 'kiln 60–150 m long, 3–8 m across, inclined 1 in 30, 1–2 rpm',
        ha='center', fontsize=7.4, color=MUTED)
```

The chemistry happens zone by zone:

| Zone | Temperature | What happens |
|---|---|---|
| Drying | up to 400 °C | free and combined water driven off |
| Calcination | 900–1000 °C | CaCO₃ --Δ--> CaO + CO₂↑; clay decomposes to its oxides |
| Clinkering (burning) | 1400–1500 °C | lime combines with SiO₂, Al₂O₃ and Fe₂O₃; about a quarter of the charge melts and binds the rest into nodules |
| Cooling | 1000 °C → 100 °C | rapid cooling in a grate cooler fixes the crystal forms |

2CaO + SiO₂ → Ca₂SiO₄  (dicalcium silicate, **C₂S**)

3CaO + SiO₂ → Ca₃SiO₅  (tricalcium silicate, **C₃S**)

3CaO + Al₂O₃ → Ca₃Al₂O₆  (tricalcium aluminate, **C₃A**)

4CaO + Al₂O₃ + Fe₂O₃ → Ca₄Al₂Fe₂O₁₀  (tetracalcium aluminoferrite, **C₄AF**)

The greenish-black nodules that leave the kiln, 5–25 mm across, are **clinker**.

**(c) Final grinding.** Cooled clinker is ground in a ball mill with **2–5 %
gypsum** to a powder so fine that most of it passes a 90 μm sieve
(specific surface about 300–350 m² kg⁻¹), and bagged in 50 kg sacks.

::: caution Gypsum is not a filler — it is the brake
Without gypsum, C₃A hydrates within minutes and the cement undergoes a **flash
set**: it stiffens before it can be placed, and is then useless. Gypsum reacts
with C₃A to form a coating of ettringite on each grain, which slows the reaction
and gives a working time of about 30 minutes to 10 hours:

Ca₃Al₂O₆ + 3CaSO₄·2H₂O + 26H₂O → Ca₆Al₂(SO₄)₃(OH)₁₂·26H₂O
:::

### Bogue compounds and the setting reactions

The four compounds formed in the clinker were first identified by R. H. Bogue, and
the properties of a cement follow directly from how much of each it contains.

```figure caption="Typical composition of ordinary Portland cement and the heat of hydration of each Bogue compound. C₃S gives early strength, C₂S later strength, and C₃A most of the heat."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
names = ['C₃S\nalite', 'C₂S\nbelite', 'C₃A\ncelite', 'C₄AF\nfelite', 'gypsum\n+ minor']
pct   = [50, 25, 10, 8, 7]
heat  = [500, 260, 865, 420, None]
cols  = [SERIES[1], SERIES[0], SERIES[3], SERIES[2], MUTED]
ax.bar(names, pct, color=cols, width=0.62)
for n, p, h in zip(names, pct, heat):
    lab = f'{p} %' + (f'\n{h} J g⁻¹' if h else '')
    ax.text(n, p+1.4, lab, ha='center', fontsize=7.4, color=INK)
ax.set_ylabel('percentage of cement by mass')
ax.set_ylim(0, 62)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.45)
```

| Compound | Formula | % in OPC | Rate of hydration | Contribution |
|---|---|---|---|---|
| C₃S, alite | 3CaO·SiO₂ | 45–55 | fast (hours to days) | **early strength**, first 7 days; 500 J g⁻¹ |
| C₂S, belite | 2CaO·SiO₂ | 20–30 | slow (weeks to a year) | **later strength**, after 28 days; 260 J g⁻¹ |
| C₃A, celite | 3CaO·Al₂O₃ | 8–12 | immediate (minutes) | flash set; little strength; 865 J g⁻¹; poor sulphate resistance |
| C₄AF, felite | 4CaO·Al₂O₃·Fe₂O₃ | 6–10 | fast | grey colour, little strength; 420 J g⁻¹ |

**Setting and hardening** are hydration reactions. Both silicates give the same
binding gel — calcium silicate hydrate, called tobermorite gel — plus calcium
hydroxide:

2Ca₃SiO₅ + 6H₂O → Ca₃Si₂O₇·3H₂O + 3Ca(OH)₂

2Ca₂SiO₄ + 4H₂O → Ca₃Si₂O₇·3H₂O + Ca(OH)₂

Ca₃Al₂O₆ + 6H₂O → Ca₃Al₂(OH)₁₂

The interlocking needles of gel are what hold the concrete together, and because
the reaction is hydration rather than drying, fresh concrete must be **cured**
(kept wet) for at least a week.

::: example Worked example 19.1 — limestone and carbon dioxide
**Problem.** A kiln produces 1.00 tonne of clinker containing 65 % CaO. The
limestone used is 95 % CaCO₃ by mass. Calculate (a) the mass of limestone
required and (b) the mass of CO₂ released. (Ca = 40, C = 12, O = 16)

**Solution.**

CaO needed = 0.65 × 1000 = 650 kg.

CaCO₃ --Δ--> CaO + CO₂↑, so 100 kg CaCO₃ gives 56 kg CaO and 44 kg CO₂.

(a) Pure CaCO₃ required = 650 × 100/56 = 1160.7 kg.
Limestone (95 % pure) = 1160.7 / 0.95 = **1222 kg ≈ 1.22 tonne**.

(b) CO₂ released = 650 × 44/56 = **510.7 kg**, i.e. about half a tonne of CO₂ per
tonne of clinker *before* counting the coal burnt. This is why cement
manufacture is one of the largest industrial sources of carbon dioxide.
:::

::: example Worked example 19.2 — checking a raw mix
**Problem.** A raw mix analyses as CaO 64 %, SiO₂ 21 %, Al₂O₃ 6 %, Fe₂O₃ 3 %.
Find the hydraulic modulus and the silica modulus and comment.

**Solution.**

$$ \text{hydraulic modulus} = \frac{64}{21+6+3} = \frac{64}{30} = 2.13 $$

$$ \text{silica modulus} = \frac{21}{6+3} = \frac{21}{9} = 2.33 $$

The hydraulic modulus is close to the required value of about 2, so the lime
content is acceptable — a little high, so free lime must be watched. The silica
modulus, 2.33, is **below** the usual range 2.5–4.0: the mix carries rather much
alumina and iron oxide, which will raise the C₃A content, make the cement set
faster and lower its sulphate resistance. Adding sand would correct it.
:::

## 19.4 Types of cement: OPC and PPC

| | Ordinary Portland Cement (OPC) | Portland Pozzolana Cement (PPC) |
|---|---|---|
| Made by grinding | clinker + 2–5 % gypsum | clinker + gypsum + **15–35 % pozzolana** (fly ash, volcanic ash, calcined clay) |
| Early strength | high — good for precast work and cold weather | lower at 7 days |
| Strength at 28–90 days | high | equal or **higher** |
| Heat of hydration | high; risks thermal cracking in thick pours | **low** — suited to dams and raft foundations |
| Durability | free lime left in the paste can be leached | pozzolana consumes the free lime, giving denser, less permeable concrete, better resistance to sulphates and chlorides |
| Cost and CO₂ | higher (more clinker) | lower; the pozzolana is often a waste product |
| Grades sold in Nepal | OPC 33, 43, 53 (28-day strength in N mm⁻²) | PPC (most bagged cement sold for house building) |

The pozzolana has no cementing power by itself. It works by reacting with the
calcium hydroxide that the silicates release:

Ca(OH)₂ + SiO₂ (reactive) + H₂O → calcium silicate hydrate gel

So the weakest and most soluble product of ordinary hydration is converted into
more of the strong binding gel.

::: example Worked example 19.3 — heat of hydration of a cement
**Problem.** A cement contains 50 % C₃S, 25 % C₂S, 10 % C₃A and 8 % C₄AF. Using
the heats of hydration 500, 260, 865 and 420 J g⁻¹, estimate the heat evolved by
1 kg of this cement. What is the figure if 30 % of the cement is replaced by fly
ash, which evolves no heat?

**Solution.** Heat per gram of cement is the sum of (fraction × heat):

$$ q = 0.50(500) + 0.25(260) + 0.10(865) + 0.08(420) $$
$$ q = 250 + 65 + 86.5 + 33.6 = 435.1\ \mathrm{J\ g^{-1}} $$

For 1 kg, heat evolved = 435.1 × 1000 = **4.35 × 10⁵ J ≈ 435 kJ**.

With 30 % replacement by inert fly ash, only 0.70 kg of cement is present, so

q = 0.70 × 435 = **305 kJ per kg of blended cement**, a fall of 30 %.

That reduction is exactly why PPC is specified for massive pours such as a dam or
a large raft foundation, where trapped heat would crack the concrete as it cools.
:::

## 19.5 Portland cement process with flow-sheet diagram

```figure caption="Flow sheet for the manufacture of Portland cement by the dry process."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,4.4))
ax.set_xlim(0, 10.8); ax.set_ylim(0, 20.6); ax.axis('off')
X, W, CX = 0.5, 5.9, 3.45

def box(y, txt, fc='#f2f5f9', h=1.7, fs=8.0, bold=False):
    ax.add_patch(FancyBboxPatch((X, y), W, h, boxstyle='round,pad=0.12',
                                fc=fc, ec=INK, lw=1.0))
    ax.text(CX, y+h/2, txt, ha='center', va='center', fontsize=fs,
            color=INK, fontweight='bold' if bold else 'normal')

def down(y1, y2):
    ax.annotate('', xy=(CX, y2), xytext=(CX, y1),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.3,
                                mutation_scale=11))

def feed(y, txt, c=SERIES[2]):
    ax.annotate(txt, xy=(X+W+0.05, y), xytext=(X+W+0.75, y), fontsize=7.2,
                color=c, ha='left', va='center',
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.0, mutation_scale=9))

def out(y, txt, c=MUTED):
    ax.annotate('', xy=(X+W+0.7, y), xytext=(X+W+0.05, y),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.0, mutation_scale=9))
    ax.text(X+W+0.8, y, txt, fontsize=7.2, color=c, ha='left', va='center')

box(18.6, 'limestone quarry  +  clay', fc='#e8eff8', bold=True)
down(18.6, 17.3)
box(15.6, 'crushing  (to ≈ 25 mm)')
down(15.6, 14.3)
box(12.6, 'proportioning, grinding\nand blending  →  raw meal')
down(12.6, 11.3)
box(9.6, 'rotary kiln, 1400–1500 °C\ncalcination + clinkering', fc='#f7ded4')
feed(10.7, 'coal + hot air', c='#A8271F')
out(9.9, 'CO₂, flue gas')
down(9.6, 8.3)
box(6.6, 'grate cooler  →  clinker')
down(6.6, 5.3)
box(3.6, 'ball mill:\nclinker + gypsum', fc='#e8f2ea')
feed(4.45, 'gypsum 2–5 %')
down(3.6, 2.3)
box(0.6, 'Portland cement  →  bags', fc='#e8eff8', bold=True)
```

In the **wet process** the first two boxes are replaced by wet grinding to a
slurry, which is fed straight into a longer kiln; everything after the kiln is
identical. The dry process has displaced it almost everywhere because evaporating
the slurry water wastes about 40 % more fuel.

## 19.6 Cement industry in Nepal

Nepal is well supplied with the main raw material: thick limestone beds run
through the Mahabharat range and the inner Terai, in Udayapur, Makwanpur,
Dhading, Palpa, Arghakhanchi, Dang and Surkhet districts. Coal, gypsum and iron
ore, however, are almost entirely imported, mainly from India.

| Plant | Place | Note |
|---|---|---|
| Himal Cement Company | Chobhar, Kathmandu | Nepal's first cement plant, built with German aid; in production from 1975, closed in 2002 after protests over dust and air pollution |
| Hetauda Cement Industry | Lamsure, Makwanpur | state-owned, established 2033 B.S. (1976), commercial production from December 1985, about 260,000 t yr⁻¹ |
| Udayapur Cement Industry | Jaljale, Udayapur | state-owned, established 2044 B.S. (1987), Japanese-built, brand "Gaida", about 800 t of clinker per day |
| Hongshi–Shivam Cement | Dhading | Nepal–China joint venture; the country's largest plant, about 2.4 million t yr⁻¹ |
| Shivam, CG, Arghakhanchi, Ghorahi, Sarbottam and others | Makwanpur, Palpa, Dang, Arghakhanchi | the private plants that now supply most of the market |

Around fifty cement factories operate in the country, with a combined grinding
capacity of roughly 22–25 million tonnes a year, although only about twenty of
them run their own kilns; the rest grind imported or domestic clinker. Nepal
became self-sufficient in cement at the start of this decade and has since begun
exporting small quantities to India. Per-capita consumption is about 250 kg a
year.

The industry's problems are equally clear: plants run far below capacity, imported
coal makes energy costly, limestone quarrying scars the Chure and Mahabharat
hills, and kiln dust and CO₂ remain an environmental burden — the reason modern
plants fit electrostatic precipitators and increasingly sell PPC, which needs less
clinker per bag.

## Chapter summary

- Cement is a hydraulic binder of calcium silicates and aluminates; Aspdin
  patented Portland cement in 1824.
- Composition of OPC: CaO 60–67 %, SiO₂ 17–25 %, Al₂O₃ 3–8 %, Fe₂O₃ 0.5–6 %.
  Hydraulic modulus ≈ 2; silica modulus 2.5–4. Excess lime makes cement unsound.
- Raw materials: calcareous (limestone), argillaceous (clay), correctives (sand,
  bauxite, iron ore) and 2–5 % gypsum added after burning.
- Three stages: crushing/grinding (wet or dry process) → burning in a rotary kiln
  → final grinding with gypsum.
- Kiln zones: drying (to 400 °C), calcination 900–1000 °C
  (CaCO₃ → CaO + CO₂↑), clinkering 1400–1500 °C (formation of C₃S, C₂S, C₃A,
  C₄AF), then rapid cooling.
- Bogue compounds: C₃S gives early strength, C₂S later strength, C₃A causes flash
  set and most of the heat, C₄AF gives the grey colour. Gypsum retards C₃A by
  forming ettringite.
- Setting: 2Ca₃SiO₅ + 6H₂O → Ca₃Si₂O₇·3H₂O + 3Ca(OH)₂ and
  2Ca₂SiO₄ + 4H₂O → Ca₃Si₂O₇·3H₂O + Ca(OH)₂; the gel binds the aggregate, so
  concrete must be cured wet.
- OPC = clinker + gypsum; PPC = clinker + gypsum + 15–35 % pozzolana, which
  consumes free Ca(OH)₂, lowers the heat of hydration and improves durability.
- Nepal has abundant limestone; about fifty plants, roughly 22–25 Mt yr⁻¹ grinding
  capacity, self-sufficient since about 2020, with Hongshi–Shivam in Dhading the
  largest and Hetauda and Udayapur the state-owned plants.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The approximate percentage of lime (CaO) in ordinary Portland cement is <span class="marks">[1]</span>
   (a) 20–25 % (b) 40–45 % (c) 60–67 % (d) 80–85 %
2. Gypsum is added to cement clinker to <span class="marks">[1]</span>
   (a) increase strength (b) retard the setting time
   (c) give colour (d) reduce the cost
3. The temperature of the clinkering zone of a rotary kiln is about <span class="marks">[1]</span>
   (a) 500 °C (b) 900 °C (c) 1450 °C (d) 2000 °C
4. Which Bogue compound is mainly responsible for early strength? <span class="marks">[1]</span>
   (a) C₂S (b) C₃S (c) C₃A (d) C₄AF
5. PPC differs from OPC in containing <span class="marks">[1]</span>
   (a) more gypsum (b) no lime (c) 15–35 % pozzolana (d) iron oxide
6. Nepal's largest cement plant is located in <span class="marks">[1]</span>
   (a) Dhading (b) Chobhar (c) Jaljale, Udayapur (d) Biratnagar

::: note Answers to Group A
**1.** (c) — lime is the largest single oxide.
**2.** (b) — it stops the flash set caused by C₃A.
**3.** (c) — 1400–1500 °C, where partial fusion forms clinker.
**4.** (b) — C₃S hydrates in hours to days.
**5.** (c) — fly ash or another reactive silica.
**6.** (a) — the Hongshi–Shivam plant in Dhading, about 2.4 Mt yr⁻¹.
:::

**Group B — Short answer (5 marks each)**

1. What is cement? Give the average composition of OPC and state the two moduli
   that control the raw mix. <span class="marks">[5]</span>
2. Name the raw materials used in cement manufacture and state the oxide each
   supplies. <span class="marks">[5]</span>
3. Describe the zones of a rotary kiln with their temperatures and the chemical
   changes in each. <span class="marks">[5]</span>
4. What are Bogue compounds? Give their formulae and the property each controls.
   Why is gypsum added? <span class="marks">[5]</span>
5. Distinguish between OPC and PPC, and explain the chemistry by which a pozzolana
   improves durability. <span class="marks">[5]</span>
6. 2.0 tonnes of limestone containing 90 % CaCO₃ is decomposed in a kiln.
   Calculate the mass of CaO formed and the mass of CO₂ released. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** See §19.1: a hydraulic binder of calcium silicates and aluminates made by
burning limestone with clay at 1400–1500 °C and grinding the clinker with gypsum.
CaO 60–67 %, SiO₂ 17–25 %, Al₂O₃ 3–8 %, Fe₂O₃ 0.5–6 %. Hydraulic modulus
CaO/(SiO₂+Al₂O₃+Fe₂O₃) ≈ 2 and silica modulus SiO₂/(Al₂O₃+Fe₂O₃) = 2.5–4.

**2.** Calcareous — limestone, chalk, marl (CaO); argillaceous — clay, shale
(SiO₂, Al₂O₃, Fe₂O₃); correctives — sand (SiO₂), bauxite (Al₂O₃), iron ore
(Fe₂O₃); gypsum (SO₃) added at the grinding stage.

**3.** Drying zone up to 400 °C, water removed; calcination zone 900–1000 °C,
CaCO₃ → CaO + CO₂↑ and the clay breaks down; clinkering zone 1400–1500 °C, where
2CaO + SiO₂ → Ca₂SiO₄, 3CaO + SiO₂ → Ca₃SiO₅, 3CaO + Al₂O₃ → Ca₃Al₂O₆ and
4CaO + Al₂O₃ + Fe₂O₃ → Ca₄Al₂Fe₂O₁₀; then rapid cooling to about 100 °C.

**4.** C₃S (3CaO·SiO₂) early strength; C₂S (2CaO·SiO₂) later strength; C₃A
(3CaO·Al₂O₃) flash set, most heat, poor sulphate resistance; C₄AF
(4CaO·Al₂O₃·Fe₂O₃) grey colour, little strength. Gypsum reacts with C₃A to form
ettringite, coating the grains and giving a workable setting time.

**5.** See the table in §19.4. Pozzolana reacts with the Ca(OH)₂ set free during
hydration: Ca(OH)₂ + SiO₂ + H₂O → calcium silicate hydrate gel. Removing the
soluble calcium hydroxide and adding more gel makes the concrete denser, less
permeable and more resistant to sulphate and chloride attack, while lowering the
heat of hydration.

**6.** Mass of CaCO₃ = 0.90 × 2000 = 1800 kg. From CaCO₃ → CaO + CO₂,
100 kg gives 56 kg CaO and 44 kg CO₂.
CaO = 1800 × 56/100 = **1008 kg**; CO₂ = 1800 × 44/100 = **792 kg**.
:::

**Group C — Long answer (8 marks each)**

1. Describe the manufacture of Portland cement by the dry process, with a
   flow-sheet diagram, the reactions in the kiln and the role of gypsum. <span class="marks">[8]</span>
2. (a) What are the setting and hardening reactions of cement? Write the equations
   for C₃S and C₂S. <span class="marks">[4]</span>
   (b) A cement contains 45 % C₃S, 30 % C₂S, 12 % C₃A and 8 % C₄AF. Taking heats
   of hydration of 500, 260, 865 and 420 J g⁻¹, calculate the heat evolved per
   kilogram, and say whether this cement is suitable for a thick dam wall. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Quarried limestone and clay are crushed to about 25 mm, proportioned,
ground and blended to a dry raw meal; the meal is burnt in a rotary kiln
(60–150 m, inclined 1 in 30, 1–2 rpm) fired with pulverised coal, passing through
drying, calcination (900–1000 °C, CaCO₃ → CaO + CO₂↑) and clinkering
(1400–1500 °C, forming C₃S, C₂S, C₃A and C₄AF) zones; the clinker is cooled in a
grate cooler and ground with 2–5 % gypsum, which prevents the flash set caused by
C₃A, and the cement is bagged. The flow sheet is the one drawn in §19.5.

**2.** (a) Setting and hardening are hydration reactions producing tobermorite
(calcium silicate hydrate) gel and calcium hydroxide:
2Ca₃SiO₅ + 6H₂O → Ca₃Si₂O₇·3H₂O + 3Ca(OH)₂ (fast, early strength) and
2Ca₂SiO₄ + 4H₂O → Ca₃Si₂O₇·3H₂O + Ca(OH)₂ (slow, later strength). The interlocking
gel needles bind the aggregate, so the concrete must be kept wet while curing.
(b) q = 0.45(500) + 0.30(260) + 0.12(865) + 0.08(420)
= 225 + 78 + 103.8 + 33.6 = 440.4 J g⁻¹, so **440 kJ per kg**. This is *higher*
than an ordinary cement (≈435 kJ kg⁻¹) because of its large C₃A content, so it is
**not** suitable for a thick dam wall; a low-heat PPC should be used instead.
:::

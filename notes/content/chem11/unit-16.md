---
subject: Chemistry
grade: 11
unit: 16
title: Fundamentals of Applied Chemistry
hours: 4
area: Applied Chemistry
---

Everything in the first fifteen units happened in a test tube. This unit asks a
different question: how do you take a reaction that works on 5 g in a laboratory
and make it work on 500 tonnes a day, profitably, safely, and without poisoning
the river next door? **Applied chemistry** — also called chemical technology or
chemical engineering science — is the study of that scale-up. It is the bridge
between the balanced equation and the bag of urea a farmer in Chitwan actually
buys.

::: key What the examiner wants from this unit
This is a descriptive unit with no derivations, so marks are won on *organised
lists*. Learn: the stages of new-product development in order; the difference
between fixed and variable cost and the shape of the cash-flow curve; the
batch-versus-continuous comparison table; and four or five named environmental
impacts with the chemistry behind each. Unit 17 then applies all of it.
:::

## 16.1 Chemical industry and its importance

::: definition Chemical industry
The **chemical industry** is the branch of manufacturing that converts raw
materials — minerals, air, water, petroleum, biomass — into chemical products by
deliberately changing their chemical composition on a commercial scale.
:::

Chemical manufacture is divided by scale and value:

| Class | Tonnage | Value | Examples |
|---|---|---|---|
| Heavy (bulk) chemicals | millions of tonnes/year | low per kg | H₂SO₄, NH₃, NaOH, Na₂CO₃, cement, urea |
| Fine chemicals | hundreds to thousands of tonnes/year | high per kg | dyes, flavours, pesticide actives, reagents |
| Speciality chemicals | small, made to a specification | sold on performance | paints, adhesives, catalysts, detergents |
| Pharmaceuticals | kg to tonnes | very high per kg | paracetamol, antibiotics, vaccines |

Why the industry matters:

1. **Food.** Nitrogen fertilizers made from atmospheric nitrogen feed roughly
   half the world's population. Nepal has no fertilizer factory of its own and
   imports **100%** of its chemical fertilizer, at a cost of more than
   Rs 40 billion a year.
2. **Health.** Medicines, disinfectants, chlorine for drinking water, oxygen for
   hospitals, and the plastics that syringes and IV sets are made from.
3. **Infrastructure.** Cement, steel, glass, paints and bitumen. Nepal has 13
   integrated and 16 grinding cement plants with a combined capacity of about
   12.3 million tonnes a year, including the state-owned Hetauda Cement (using
   limestone from Bhaise, Majhuwa and Jogmara in Makawanpur) and Udayapur Cement.
4. **Energy.** Refining, battery chemicals, and the electrolysis of water for
   hydrogen.
5. **Economy.** The output of one chemical plant is the raw material of the next,
   so a single plant creates a chain of downstream industry and employment.

The industry's signature is that a **single cheap raw material tree** feeds
everything. Air gives N₂ and O₂; brine gives Cl₂, NaOH and Na₂CO₃; sulphur or
pyrites give H₂SO₄; hydrocarbons and water give H₂ and synthesis gas. Almost
every product in Unit 17 grows from one of these four roots.

## 16.2 Stages in producing a new product

A new chemical product is not invented and then built. It passes through a fixed
sequence of stages, each of which can kill the project. The later a project is
abandoned, the more money is lost — so each stage is designed to answer one
question as cheaply as possible.

```figure caption="The stages in bringing a new chemical product to market. Cost per stage rises roughly tenfold each time, so every stage ends in a go / no-go decision."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,4.3))

stages = [
    ('1  Market research\n& idea', 'Is there a demand?\nWhat price?'),
    ('2  Laboratory\n(bench) synthesis', 'Does the reaction work?\nYield, purity, route'),
    ('3  Pilot plant', 'kg-scale trial run:\nheat, mixing, corrosion'),
    ('4  Process & plant\ndesign', 'Flow sheet, reactor size,\nmaterials, safety study'),
    ('5  Construction &\ncommissioning', 'Build, test, start up\non specification'),
    ('6  Full-scale\nproduction', 'Steady operation,\nquality control'),
    ('7  Marketing, sales\n& review', 'Sell, monitor cost,\nimprove the process'),
]
y, h = 7.40, 0.86
for i, (name, note) in enumerate(stages):
    hi = i in (1, 2, 3)
    ax.add_patch(FancyBboxPatch((0.55, y-h), 2.55, h,
                                boxstyle='round,pad=0.02,rounding_size=0.10',
                                fc='#eef3f9' if hi else '#f4f6f9',
                                ec=ACCENT if hi else INK, lw=1.3))
    ax.text(1.825, y-h/2, name, fontsize=7.6, color=INK, ha='center', va='center',
            linespacing=1.35)
    ax.text(3.30, y-h/2, note, fontsize=7.0, color=MUTED, ha='left', va='center',
            linespacing=1.35)
    if i < len(stages)-1:
        ax.annotate('', xy=(1.825, y-h-0.28), xytext=(1.825, y-h-0.02),
                    arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.3, mutation_scale=11))
    y -= (h + 0.30)

ax.annotate('', xy=(0.50, 5.81), xytext=(0.50, 0.01),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.2,
                            connectionstyle='arc3,rad=-0.17', mutation_scale=11))
ax.text(-0.92, 2.95, 'feedback: re-design, re-cost', fontsize=7.0, color='#d9534f',
        ha='center', va='center', rotation=90)
ax.set_xlim(-1.25, 6.40); ax.set_ylim(-0.60, 7.60); ax.axis('off')
```

Two stages deserve extra attention.

- The **pilot plant** (stage 3) exists because chemistry does not scale linearly.
  Doubling the size of a reactor multiplies its volume by 8 but its surface area
  only by 4, so a reaction that was easy to cool in a 250 cm³ flask can run away
  in a 25 m³ vessel. Mixing, heat transfer, corrosion, catalyst life and the
  handling of solids can only be measured, not predicted.
- **Process design** (stage 4) fixes the flow sheet: which units, in what order,
  at what temperature and pressure, with what recycle streams. Every later cost
  is locked in here.

## 16.3 Economics of production; cash flow in the production cycle

A plant is built only if it will make money. The money involved falls into two
capital sums and two running costs.

| Term | Meaning | Examples |
|---|---|---|
| **Fixed capital** | one-off spending to build the plant | land, reactors, pipework, instruments |
| **Working capital** | money tied up to keep it running | stock of raw material, product in store, unpaid bills |
| **Fixed costs** | paid whether or not anything is produced | depreciation, interest on loans, salaries, insurance, rates |
| **Variable costs** | proportional to output | raw materials, catalyst, electricity, steam, packaging |

For a selling price $S$ per kilogram, a variable cost $V$ per kilogram and fixed
costs $F$ per year, the profit on $n$ kilograms a year is

$$ P = n(S - V) - F $$

The quantity $(S-V)$ is the **contribution** per kilogram. Setting $P=0$ gives
the **break-even point** — the output at which the plant stops losing money:

$$ n_{\text{BE}} = \frac{F}{S - V} $$

Because $F$ is spread over every kilogram, the cost per kilogram falls as output
rises. This is the **economy of scale**, and it is the single strongest reason
that bulk chemical plants are enormous.

```figure caption="Cumulative cash flow over the life of a project. Cash is negative through research and construction, reaches its lowest point at start-up, and the payback period ends where the curve crosses zero."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))

t = np.array([0.0, 1.0, 2.0, 3.0, 3.6, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0])
c = np.array([0.0,-0.4,-1.0,-4.2,-6.6,-7.4,-5.6,-3.4,-1.1, 1.3, 3.7, 6.1, 8.3, 10.1])
ax.plot(t, c, color=ACCENT, lw=2.0, zorder=3)
ax.axhline(0, color=INK, lw=1.0)
ax.fill_between(t, c, 0, where=(c<0), color='#d9534f', alpha=0.13)
ax.fill_between(t, c, 0, where=(c>0), color='#2e8b57', alpha=0.13)

ax.annotate('research &\ndesign', (1.4,-0.7), textcoords='offset points', xytext=(-6,16),
            fontsize=7.4, color=MUTED, ha='center', linespacing=1.3)
ax.annotate('construction', (3.0,-4.2), textcoords='offset points', xytext=(-2,-20),
            fontsize=7.4, color=MUTED, ha='center')
ax.plot([4.0],[-7.4],'o',color='#d9534f',ms=5, zorder=4)
ax.annotate('start-up:\nmaximum cash outflow', (4.0,-7.4), textcoords='offset points',
            xytext=(15,-1), fontsize=7.4, color='#d9534f', va='center', ha='left',
            linespacing=1.3)
ax.plot([7.56],[0.0],'o',color='#2e8b57',ms=5, zorder=4)
ax.annotate('break-even', (7.56,0.0), textcoords='offset points', xytext=(-4,12),
            fontsize=7.4, color='#2e8b57', ha='center')
ax.annotate('', xy=(0.0,-9.9), xytext=(7.56,-9.9),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(2.60,-9.62,'payback period', fontsize=7.4, color=INK, ha='center')
ax.text(10.4, 7.4, 'profit', fontsize=7.6, color='#2e8b57', ha='center')

ax.set_xlabel('years from start of project')
ax.set_ylabel('cumulative cash flow')
ax.set_xlim(0,12.4); ax.set_ylim(-11.0,11.4)
ax.set_yticks([])
ax.spines[['top','right','left']].set_visible(False)
ax.grid(True, axis='x', alpha=.45)
```

The curve above is the **cash-flow diagram** of the production cycle. Read it
left to right: money flows *out* during research, design and construction; the
outflow is worst at commissioning, when the plant is complete but selling
nothing; then sales begin and the curve climbs. Where it crosses zero, the
project has returned exactly what was spent — that time is the **payback
period**. Nothing after that point is profit until the plant is shut down and
its working capital recovered.

::: example Worked example 16.1
**Problem.** A plant making a solvent has fixed costs of Rs 120 million per year.
The variable cost is Rs 45 per kg and the product sells for Rs 75 per kg.
(a) Find the break-even output. (b) Find the annual profit at an output of
7,000 tonnes. (c) If the plant cost Rs 900 million to build, find the payback
period at that output, ignoring interest.

**Solution.**

(a) Contribution $= S - V = 75 - 45 = $ Rs 30 per kg.

$$ n_{\text{BE}} = \frac{F}{S-V} = \frac{120 \times 10^{6}}{30} = 4.0\times10^{6}\ \text{kg} = 4000\ \text{tonnes per year} $$

(b) At $n = 7000\ \text{t} = 7.0\times10^{6}$ kg,

$$ P = 7.0\times10^{6}(30) - 120\times10^{6} = 210\times10^{6} - 120\times10^{6} = \text{Rs}\ 90\ \text{million per year} $$

(c) Payback $= 900/90 = \mathbf{10}$ **years**. A payback longer than about eight
years would normally make the project unattractive, so the company would look for
a cheaper design or a higher output.
:::

## 16.4 Running a chemical plant; designing a chemical plant

### Designing a plant

Design begins with the **flow sheet** — a block diagram naming every unit and
every stream. Once the flow sheet is fixed, the designer works through:

1. **Choice of route.** Of the reactions that give the product, pick the one with
   the cheapest raw materials, the highest atom economy and the fewest steps.
2. **Reaction conditions.** Temperature, pressure and catalyst are chosen by
   balancing *equilibrium yield* against *rate* and *cost* — the compromise that
   dominates Unit 17.
3. **Plant location.** Near the raw material if the raw material is bulky
   (cement near limestone); near the market if the product is bulky or dangerous
   (sulphuric acid); always near water, power, transport and labour, and away
   from dense settlement.
4. **Materials of construction.** Stainless steel, lead lining, glass lining or
   titanium, chosen against corrosion at the operating temperature.
5. **Energy integration.** Exothermic reactions raise steam that drives the next
   stage. In a contact-process plant almost all the process heat comes from the
   reaction itself.
6. **Safety and effluent.** Pressure-relief systems, interlocks, and treatment
   for every waste stream, decided at the design stage — not afterwards.

### Running a plant

| Task | What it involves |
|---|---|
| Raw-material supply | continuous, of guaranteed purity; catalyst poisons excluded |
| Process control | automatic control of temperature, pressure, flow, pH, level |
| Quality control | sampling and analysis of product against a written specification |
| Maintenance | planned shutdowns; corrosion and catalyst-activity monitoring |
| Safety | training, protective equipment, leak detection, emergency plans |
| Waste management | scrubbing of gases, effluent treatment, solid-waste disposal |

::: tip Why catalysts get "poisoned" in exam answers
A catalyst is expensive and must last for years. Impurities that adsorb on its
surface and block the active sites are called **poisons** — arsenic oxide for the
V₂O₅ of the contact process, sulphur compounds and CO for the iron of the Haber
process. This is why every flow sheet in Unit 17 has a purification stage *before*
the catalyst chamber. Naming the poison earns the mark.
:::

## 16.5 Continuous and batch processing

::: definition Batch and continuous processing
In a **batch process** a measured charge of reactants is put into a vessel, made
to react, and the whole product is removed before the next charge is loaded.
In a **continuous process** reactants flow into the reactor and products flow out
without interruption, so the plant runs at a steady state for months at a time.
:::

```figure caption="Left: a batch reactor is charged, reacted and emptied in a repeating cycle, so output arrives in steps. Right: a continuous reactor holds a steady state and delivers product at a constant rate."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.1,3.0))

def mini(ax, t, cum, col):
    ax.annotate('', xy=(4.80,-0.62), xytext=(0.50,-0.62),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
    ax.annotate('', xy=(0.50,1.15), xytext=(0.50,-0.72),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
    ax.plot(0.58+t*1.00, -0.62+cum*0.40, color=col, lw=1.7)
    ax.text(2.65,-1.08,'time', fontsize=7.2, color=MUTED, ha='center')
    ax.text(0.20,0.28,'total product made', fontsize=7.0, color=MUTED,
            rotation=90, va='center', ha='center')

# ---- batch ----
a1.add_patch(Rectangle((1.15,2.00),1.85,1.45, fc='#eef3f9', ec=INK, lw=1.5))
a1.add_patch(Rectangle((1.20,2.05),1.75,0.80, fc=ACCENT, alpha=0.20, ec='none'))
a1.plot([2.075,2.075],[2.25,3.80], color=INK, lw=1.6)
a1.plot([1.75,2.40],[2.25,2.25], color=INK, lw=2.2)
a1.annotate('', xy=(1.70,3.62), xytext=(0.45,3.62),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.5, mutation_scale=11))
a1.text(0.42,3.80,'charge', fontsize=7.2, color='#2e8b57', ha='left')
a1.annotate('', xy=(3.95,1.62), xytext=(2.85,1.94),
            arrowprops=dict(arrowstyle='-|>', color='#8a6d1f', lw=1.5, mutation_scale=11))
a1.text(3.35,1.34,'discharge', fontsize=7.2, color='#8a6d1f', ha='center')
a1.text(2.075,4.22,'BATCH', fontsize=8.8, color=INK, ha='center', fontweight='bold')
tb = np.linspace(0, 4, 800)
cum_b = np.floor(tb) + np.clip((tb % 1.0 - 0.25)/0.50, 0, 1)
cum_b = np.where(tb >= 4.0, 4.0, cum_b)
mini(a1, tb, cum_b, ACCENT)
a1.set_xlim(-0.05,5.15); a1.set_ylim(-1.35,4.55); a1.axis('off')

# ---- continuous ----
a2.add_patch(Rectangle((1.30,2.12),2.15,1.20, fc='#eef3f9', ec=INK, lw=1.5))
for xx in (1.78, 2.38, 2.98):
    a2.add_patch(Circle((xx,2.72), 0.19, fc='none', ec=MUTED, lw=0.9))
a2.text(2.38,3.55,'catalyst bed', fontsize=7.2, color=MUTED, ha='center')
a2.annotate('', xy=(1.25,2.72), xytext=(0.20,2.72),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.6, mutation_scale=11))
a2.text(0.18,2.94,'feed in', fontsize=7.2, color='#2e8b57', ha='left')
a2.annotate('', xy=(5.05,2.72), xytext=(3.50,2.72),
            arrowprops=dict(arrowstyle='-|>', color='#8a6d1f', lw=1.6, mutation_scale=11))
a2.text(5.08,2.94,'product out', fontsize=7.2, color='#8a6d1f', ha='right')
a2.text(2.38,4.22,'CONTINUOUS', fontsize=8.8, color=INK, ha='center', fontweight='bold')
tc = np.linspace(0, 4, 200)
mini(a2, tc, tc, '#2e8b57')
a2.set_xlim(-0.05,5.60); a2.set_ylim(-1.35,4.55); a2.axis('off')
```

| Feature | Batch | Continuous |
|---|---|---|
| Scale suited to | small, up to a few thousand t/yr | very large, bulk chemicals |
| Equipment | one general-purpose vessel, many products | dedicated plant, one product |
| Capital cost | low | high |
| Labour per tonne | high | low |
| Product uniformity | varies from batch to batch | very uniform at steady state |
| Traceability | excellent — each batch numbered | harder; needs continuous sampling |
| Down-time | large (charge, clean, discharge) | small; runs months between shutdowns |
| Control | manual or semi-automatic | fully automatic |
| Typical products | medicines, dyes, paints, cosmetics | H₂SO₄, NH₃, urea, NaOH, cement, petrol |

::: example Worked example 16.2
**Problem.** A batch reactor makes 2.5 tonnes of product per batch. Each cycle is
6 hours of reaction plus 2 hours for charging, discharging and cleaning. A
continuous plant for the same product makes 0.40 tonnes per hour. Both operate
330 days a year. Compare the annual outputs.

**Solution.** Operating time per year $= 330 \times 24 = 7920$ h.

*Batch:* cycle time $= 6 + 2 = 8$ h, so the number of batches is
$7920/8 = 990$ batches, and

$$ \text{output} = 990 \times 2.5 = 2475\ \text{tonnes per year} $$

*Continuous:* $\ 0.40 \times 7920 = 3168$ tonnes per year.

The continuous plant makes **693 tonnes (28%) more** from the same operating
time, because it loses no time to charging and cleaning. Note also that the batch
plant is idle for $990 \times 2 = 1980$ h, a quarter of the year.
:::

::: caution "Continuous is always better" is wrong
Continuous plant is only cheaper *per tonne at high output*. Its high fixed
capital means a low break-even point is impossible, and it can make only one
product. A pharmaceutical company making 40 different drugs in small quantities,
each needing a traceable batch number, uses batch reactors for very good reasons.
:::

## 16.6 Environmental impact of the chemical industry

Every kilogram of product leaves the plant with some mass of waste attached to
it. The standard measure is the **E-factor**: kilograms of waste per kilogram of
product. It rises steeply as tonnage falls and chemistry gets more complicated.

```figure caption="Typical E-factor (kg waste per kg product) by sector. Bulk chemicals make the most waste in total tonnage; pharmaceuticals make by far the most per kilogram of product. Note the logarithmic scale."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.7))
sectors = ['Oil\nrefining', 'Bulk\nchemicals', 'Fine\nchemicals', 'Pharma-\nceuticals']
lo = np.array([0.02, 1.0, 5.0, 25.0])
hi = np.array([0.10, 5.0, 50.0, 100.0])
ypos = np.arange(len(sectors))
for i in range(len(sectors)):
    ax.barh(ypos[i], hi[i]-lo[i], left=lo[i], height=0.52,
            color=SERIES[i], alpha=0.80, edgecolor='none')
    ax.text(hi[i]*1.25, ypos[i], f'{lo[i]:g}–{hi[i]:g}', fontsize=7.6,
            color=INK, va='center')
ax.set_xscale('log')
ax.set_yticks(ypos); ax.set_yticklabels(sectors, fontsize=7.8)
ax.invert_yaxis()
ax.set_xlabel('E-factor  (kg waste per kg product)')
ax.set_xlim(0.01, 600)
ax.spines[['top','right','left']].set_visible(False)
ax.grid(True, axis='x', alpha=.5)
```

**The main impacts, with the chemistry behind each**

| Impact | Chemistry | Control measure |
|---|---|---|
| Acid rain | SO₂ and NOₓ escaping to air: SO₂ + H₂O → H₂SO₃; 2SO₂ + O₂ → 2SO₃ → H₂SO₄ | scrubbing flue gas with lime slurry; double absorption in the contact process |
| Global warming | CO₂ from fuel, from reforming and from CaCO₃ → CaO + CO₂ in cement kilns | energy integration, alternative fuels, carbon capture |
| Ozone depletion | CFCs release Cl atoms: Cl + O₃ → ClO + O₂ | Montreal Protocol; replacement by HFCs and hydrocarbons |
| Water pollution | acidic or alkaline effluent, heavy-metal ions (Hg²⁺, Cr⁶⁺, Pb²⁺), organic load | neutralisation, precipitation as hydroxide or sulphide, biological treatment |
| Solid waste | CaCl₂ from the Solvay process, phosphogypsum, spent catalyst, fly ash | re-use in road building and cement; metal recovery from spent catalyst |
| Air-borne dust | cement, lime and fertilizer dust causing respiratory disease | bag filters, electrostatic precipitators, wet spraying |
| Thermal pollution | warm cooling water lowers the dissolved oxygen of a river | cooling towers before discharge |
| Major accidents | the Bhopal disaster of December 1984, in which methyl isocyanate leaked from a pesticide plant and killed thousands | inventory reduction, containment, interlocks, emergency planning |

The modern answer to all of this is **green chemistry**: design the waste out
rather than treat it afterwards. The most useful single number is the **atom
economy**, which measures how much of the mass of the reactants ends up in the
wanted product:

$$ \text{Atom economy} = \frac{\text{molar mass of desired product}}{\text{total molar mass of all reactants}} \times 100\% $$

Unlike percentage yield, atom economy is fixed by the *equation* — a reaction
with a poor atom economy is wasteful even at 100% yield.

::: example Worked example 16.3
**Problem.** Ethanol can be made by two routes:

Route A: C₂H₄ + H₂O → C₂H₅OH
Route B: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂

Calculate the atom economy of each and comment. ($M$: C₂H₄ = 28, H₂O = 18,
C₂H₅OH = 46, C₆H₁₂O₆ = 180.)

**Solution.**

*Route A.* Total reactant mass $= 28 + 18 = 46$; desired product $= 46$.

$$ \text{Atom economy} = \frac{46}{46}\times 100\% = 100\% $$

*Route B.* Total reactant mass $= 180$; desired product $= 2\times46 = 92$.

$$ \text{Atom economy} = \frac{92}{180}\times 100\% = 51.1\% $$

Route A is an **addition** reaction, so nothing is wasted — every addition
reaction has 100% atom economy. Route B throws away 88 g of CO₂ for every 92 g of
ethanol. Route B is still used because its raw material (molasses, a sugar-mill
by-product) is renewable and cheap, while route A needs ethene from petroleum.
Atom economy is one factor in the choice of route, not the only one.
:::

::: caution Atom economy is not percentage yield
Percentage yield compares the mass you *actually got* with the mass the equation
*promised*. Atom economy compares the mass the equation promises with the mass
you *put in*. A reaction can have 95% yield and 40% atom economy, or 100% atom
economy and 5% yield. Examiners set this distinction almost every year.
:::

## Chapter summary

- The chemical industry converts cheap raw materials — air, brine, water,
  sulphur, limestone, hydrocarbons — into heavy, fine, speciality and
  pharmaceutical chemicals. Nepal imports 100% of its chemical fertilizer.
- New products pass through seven stages: market research → laboratory synthesis
  → pilot plant → process and plant design → construction and commissioning →
  full production → marketing and review, with a go/no-go decision at each.
- Costs are fixed capital and working capital, fixed costs and variable costs.
  Profit $P = n(S-V) - F$ and the break-even output is $n_{\text{BE}} = F/(S-V)$.
- The cash-flow curve is negative through research and construction, reaches its
  minimum at start-up, and crosses zero at the end of the payback period.
- Plant design fixes the route, the conditions, the location, the materials of
  construction, energy integration and effluent treatment. Purification comes
  before every catalyst bed because catalysts are poisoned.
- Batch = one charge at a time, cheap, flexible, traceable, small scale.
  Continuous = steady state, high capital, low labour, uniform product, bulk scale.
- Environmental damage includes acid rain (SO₂, NOₓ), CO₂ emission, ozone
  depletion, effluent and heavy metals, dust and solid waste.
- Atom economy $= (M_{\text{product}}/\sum M_{\text{reactants}})\times 100\%$ is a
  property of the equation, not of the operator; percentage yield is not.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is a *fixed* cost of a chemical plant? <span class="marks">[1]</span>
   (a) raw materials (b) packaging (c) depreciation (d) electricity
2. The stage at which a reaction is first tested on the kilogram scale is the <span class="marks">[1]</span>
   (a) bench synthesis (b) pilot plant (c) commissioning (d) market survey
3. Which process would normally be operated **batchwise**? <span class="marks">[1]</span>
   (a) manufacture of sulphuric acid (b) manufacture of ammonia
   (c) manufacture of a tablet coating (d) manufacture of cement
4. The atom economy of the addition reaction C₂H₄ + Br₂ → C₂H₄Br₂ is <span class="marks">[1]</span>
   (a) 50% (b) 75% (c) 100% (d) impossible to calculate
5. The lowest point of the cumulative cash-flow curve of a project occurs at <span class="marks">[1]</span>
   (a) the end of research (b) start-up of the plant
   (c) the break-even point (d) the end of the plant's life

::: note Answers to Group A
**1.** (c) — depreciation is paid whether or not the plant produces anything.
**2.** (b) — the pilot plant is the kg-scale trial between bench and full plant.
**3.** (c) — small tonnage, many different specifications, batch traceability needed.
**4.** (c) — in an addition reaction all reactant atoms appear in the product.
**5.** (b) — the plant is fully paid for but has not yet sold anything.
:::

**Group B — Short answer (5 marks each)**

1. Define the chemical industry. Classify chemical products into four groups with
   one example of each. <span class="marks">[5]</span>
2. List, in order, the stages in producing a new chemical product, and state why a
   pilot plant is needed even when the bench reaction works perfectly. <span class="marks">[5]</span>
3. Distinguish between batch and continuous processing under any five headings. <span class="marks">[5]</span>
4. A plant has fixed costs of Rs 60 million per year. The variable cost is
   Rs 28 per kg and the selling price is Rs 40 per kg. Find (a) the break-even
   output in tonnes and (b) the profit at an output of 8,000 tonnes per year. <span class="marks">[5]</span>
5. State four environmental impacts of the chemical industry, giving one chemical
   equation or species responsible for each and one method of control. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** Market research → bench synthesis → pilot plant → process and plant design
→ construction and commissioning → full production → marketing and review. The
pilot plant is needed because heat transfer, mixing, corrosion, catalyst life and
solids handling do not scale with volume: the surface-to-volume ratio falls as
size rises, so a reaction that is easy to cool in a flask can run away in a large
reactor.

**4.** Contribution $= 40 - 28 =$ Rs 12 per kg.
(a) $n_{\text{BE}} = 60\times10^{6}/12 = 5.0\times10^{6}$ kg $= 5000$ tonnes per year.
(b) $P = 8.0\times10^{6}(12) - 60\times10^{6} = 96\times10^{6} - 60\times10^{6} =$ Rs 36 million per year.

**5.** Any four from the impact table — e.g. acid rain (SO₂ + H₂O → H₂SO₃;
controlled by lime scrubbing), global warming (CaCO₃ → CaO + CO₂ in cement kilns;
controlled by energy integration), water pollution (Cr⁶⁺, Pb²⁺ in effluent;
controlled by precipitation and neutralisation), dust (cement dust; controlled by
electrostatic precipitators).
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw and explain the cash-flow diagram for the production cycle of a new
   chemical product, marking the research, construction, start-up, break-even and
   profit regions. <span class="marks">[4]</span>
   (b) Explain the factors that must be considered when choosing the site and
   designing a new chemical plant. <span class="marks">[4]</span>
2. (a) Define atom economy and percentage yield and distinguish between them. <span class="marks">[3]</span>
   (b) Ethanoic acid can be made by CH₃OH + CO → CH₃COOH or by
   CH₃CH₂OH + O₂ → CH₃COOH + H₂O. Calculate the atom economy of each route.
   ($M$: CH₃OH = 32, CO = 28, CH₃COOH = 60, CH₃CH₂OH = 46, O₂ = 32, H₂O = 18.) <span class="marks">[3]</span>
   (c) State which route a manufacturer would prefer on environmental grounds and
   why. <span class="marks">[2]</span>

::: note Answer to Group C question 2
(a) *Atom economy* is the fraction of the total mass of the reactants that appears
in the desired product, $(M_{\text{product}}/\sum M_{\text{reactants}})\times100\%$;
it is fixed by the balanced equation. *Percentage yield* is
(actual mass obtained / theoretical mass from the equation) $\times 100\%$; it
depends on how well the reaction and the separation are carried out. A reaction
can have a high yield and a poor atom economy, or the reverse.

(b) Route 1: reactants $32 + 28 = 60$; product $60$; atom economy
$= (60/60)\times100\% = 100\%$.
Route 2: reactants $46 + 32 = 78$; product $60$; atom economy
$= (60/78)\times100\% = 76.9\%$.

(c) Route 1 — the carbonylation of methanol — is preferred: every atom of the
reactants ends up in the product, so there is no by-product to separate, treat or
dispose of, and no raw material is bought only to be thrown away. Route 2 wastes
18 g of water per 60 g of acid, and the dilute water must be removed by
distillation, which costs energy.
:::

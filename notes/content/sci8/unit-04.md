---
subject: Science and Technology
grade: 8
unit: 4
title: Biodiversity and Environment
hours: 0
area: Science and Technology
---

Nepal is a small country with an extraordinary variety of life. Within about
147,000 square kilometres it holds the low, hot plains of the Terai, the middle
hills and the high Himalaya, from about 60 m above sea level to the summit of
Sagarmatha at 8,848.8 m. That range of height, rainfall and temperature is the
reason Nepal has more kinds of birds than the whole of Europe. This unit is
about that variety, why it matters, what is destroying it, and what
sustainable development means for a country that has to use its forests, its
soil and its rivers without finishing them.

::: key What this unit asks of you
You should be able to define biodiversity and name its three levels with a
Nepali example of each, explain why biodiversity matters, describe the main
threats to it and the ways of conserving it, draw a simple food chain and food
web, and explain the meaning and principles of sustainable development.
:::

## 4.1 Biodiversity

**Biodiversity**, or biological diversity, is the variety of living beings found
in a place — every plant, animal, fungus and microorganism, together with the
variety within each kind and the variety of the places they live in.

Biodiversity is studied at three levels.

```figure caption="The three levels of biodiversity. A forest is rich at all three levels at once: many species, many varieties inside each species, and many different habitats packed into one landscape."
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.text(5.0, 5.5, "Biodiversity", ha="center", fontsize=8.4, color=INK,
        bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=INK, lw=1.2))
levels = [("Genetic diversity", "varieties within one species —\\n2300 kinds of rice, 3 kinds of yak",
           1.7, ACCENT),
          ("Species diversity", "different kinds of living being —\\nspiny babbler, one-horned rhino, sal tree",
           5.0, SERIES[1]),
          ("Ecosystem diversity", "different habitats —\\nforest, grassland, wetland, river, alpine",
           8.3, SERIES[2])]
for name, note, x, c in levels:
    ax.plot([5.0, x], [5.0, 4.15], color=GRID, lw=1.0)
    ax.text(x, 3.7, name, ha="center", fontsize=7.2, color=c,
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=c, lw=1.0))
    ax.text(x, 2.4, note, ha="center", va="center", fontsize=6.1, color=INK)
ax.text(5.0, 0.7, "Losing any one level weakens the other two.", ha="center",
        fontsize=6.8, color=MUTED)
fig.tight_layout()
```

::: definition Biodiversity
**Biodiversity** is the variety and variability of living organisms at all
levels — the variety of genes within a species, the variety of species in a
community, and the variety of ecosystems in a region.
:::

### 4.1.1 Why biodiversity matters

- **Food and medicine.** Every crop and every medicine comes from some living
  thing. Rice, maize, millet, buckwheat and 2,300 varieties of rice in Nepal
  alone give farmers something to fall back on when a disease attacks one
  variety.
- **Clean air and water.** Plants take in carbon dioxide and give out oxygen;
  forests hold the soil and recharge the springs that villages drink from.
- **Soil and fertility.** Earthworms, insects, fungi and bacteria break down
  dead matter into humus. Without them the soil would be dead.
- **Protection from disaster.** A forest on a slope slows rainwater and
  prevents landslides and floods; mangroves and riverbank forest reduce flood
  damage.
- **Income.** Tourism, trekking, honey, *yarsagumba*, herbs and timber all rest
  on living things.
- **Beauty and culture.** Many Nepali festivals, songs and beliefs are tied to
  particular trees, birds and rivers.

```photo id="sci8/chitwan-forest" caption="Sal forest in Chitwan National Park. A forest is a habitat, a water store, a soil holder and a food store at the same time — which is why clearing it costs far more than the timber is worth." width="88"
key 1 Sal trees, the dominant tree of the Terai forest
key 2 Understorey shrubs and grass, food for deer and rhino
key 3 Leaf litter, which becomes humus
```
### 4.1.2 The ecosystem, food chain and food web

An **ecosystem** is a community of living beings together with the non-living
surroundings they depend on — the soil, water, air and sunlight of a place.

In every ecosystem, food passes from one living thing to another in a
**food chain**. The chain always begins with a green plant, because only green
plants can make their own food.

**Grass → grasshopper → frog → snake → eagle**

| Position in the chain | Name | Example |
|---|---|---|
| Makes its own food | producer | grass, paddy, sal tree |
| Eats plants | primary consumer (herbivore) | grasshopper, deer, goat |
| Eats plant eaters | secondary consumer | frog, jackal |
| Eats other animals | tertiary consumer | snake, tiger, eagle |
| Breaks down dead matter | decomposer | bacteria, fungi, earthworm |

In a real forest the chains are joined together, because one animal eats
several kinds of food and is eaten by several others. This network is a **food
web**.

```figure caption="A food web from the Terai. Follow any single line and you have a food chain; look at the whole picture and you see why one lost species affects many others."
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")
nodes = {"grass": (1.2, 1.2), "paddy": (1.2, 3.0), "deer": (4.0, 2.1),
         "grasshopper": (4.0, 0.9), "frog": (6.6, 0.9), "jackal": (6.6, 3.4),
         "tiger": (9.0, 2.6), "snake": (6.6, 1.9)}
for name, (x, y) in nodes.items():
    ax.text(x, y, name, ha="center", va="center", fontsize=6.8, color=INK,
            bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=ACCENT, lw=0.9))
for a, b in [("grass", "deer"), ("grass", "grasshopper"), ("paddy", "deer"),
             ("grasshopper", "frog"), ("deer", "jackal"), ("frog", "snake"),
             ("jackal", "tiger"), ("snake", "tiger")]:
    xa, ya = nodes[a]
    xb, yb = nodes[b]
    ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9,
                                shrinkA=16, shrinkB=16))
ax.text(5.0, 5.5, "green plants are the start of every chain", ha="center",
        fontsize=6.8, color=MUTED)
ax.text(5.0, 4.4, "an arrow means \"is eaten by\"", ha="center", fontsize=6.8,
        color=MUTED)
fig.tight_layout()
```

::: caution The arrow direction
An arrow in a food chain means **"is eaten by"**, not "eats". So
grass → grasshopper is right, and grasshopper → grass means the arrow has been
drawn backwards. Marks are lost for this every year.
:::

### 4.1.3 Threats to biodiversity

| Threat | What happens |
|---|---|
| Deforestation | habitats disappear; soil erodes; springs dry up |
| Habitat fragmentation | roads and settlements cut a forest into pieces too small for tigers or elephants |
| Poaching and illegal trade | rhino horn, tiger bone, musk, *yarsagumba* collected beyond limit |
| Pollution | pesticides kill bees and fish; plastic chokes rivers |
| Invasive species | *Mikania*, *Lantana* and water hyacinth crowd out native plants |
| Climate change | snow lines rise, glaciers shrink, rainfall becomes irregular |
| Over-use | overgrazing, over-fishing, and cutting firewood faster than the forest grows |
| Forest fire | kills seedlings and small animals; occurs more often in dry years |

### 4.1.4 Conservation

**In-situ conservation** protects a species where it already lives.

- **National parks and reserves** — Chitwan, Bardia, Sagarmatha, Langtang,
  Rara, Shey-Phoksundo and others; more than a fifth of Nepal's land is under
  some form of protection.
- **Community forests** — forest handed to a user group to manage. Nepal is
  famous for this: forest cover has grown since the 1990s largely because
  communities were given responsibility.
- **Buffer zones** — a belt around a park where local people may collect
  firewood and fodder in a controlled way, so that they have a reason to
  protect the park.
- **Laws and agreements** — the National Parks and Wildlife Conservation Act,
  the CITES agreement that bans trade in endangered species, and the
  Ramsar Convention that protects wetlands such as Koshi Tappu.

**Ex-situ conservation** protects a species outside its habitat: botanical
gardens (Godavari), zoological parks (Central Zoo, Jawalakhel), seed banks and
tissue culture laboratories.

::: tip Four things a student can actually do
**(1)** Plant and look after a tree — watering it for the first two years
matters more than planting it. **(2)** Refuse plastic bags and carry a cloth
bag. **(3)** Never buy or eat wild meat, and never collect orchids, *yarsagumba*
seedlings or birds' eggs. **(4)** Join or start an eco-club: a school that
composts its waste and plants on its own ground teaches the whole village.
:::

## 4.2 Sustainable development

**Sustainable development** means meeting the needs of people today without
destroying the ability of people in the future to meet their own needs.

The idea is often drawn as three overlapping circles: the environment, society
and the economy. A plan is sustainable only when all three are satisfied at
once.

```figure caption="The three circles of sustainable development. Cutting a forest gives the economy a gain today and takes it away from the environment and from the people who depended on it — the overlap is what has to be designed."
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis("off")
ax.add_patch(plt.Circle((4.0, 3.6), 2.02, fc=ACCENT, alpha=0.20, ec=ACCENT, lw=1.2))
ax.add_patch(plt.Circle((6.0, 3.6), 2.02, fc=SERIES[1], alpha=0.20, ec=SERIES[1], lw=1.2))
ax.add_patch(plt.Circle((5.0, 2.0), 2.02, fc=SERIES[2], alpha=0.20, ec=SERIES[2], lw=1.2))
ax.text(3.0, 5.0, "Environment", ha="center", fontsize=7.0, color=ACCENT)
ax.text(7.0, 5.0, "Society", ha="center", fontsize=7.0, color=SERIES[1])
ax.text(5.0, 0.55, "Economy", ha="center", fontsize=7.0, color=SERIES[2])
ax.text(5.0, 3.15, "sustainable", ha="center", fontsize=7.2, color=INK)
ax.text(5.0, 2.55, "development", ha="center", fontsize=7.2, color=INK)
fig.tight_layout()
```

### 4.2.1 The principles

1. **Use renewable resources no faster than they renew.** Cut a tree only as
   fast as a new one grows; catch fish only as fast as they breed.
2. **Use non-renewable resources sparingly.** Petroleum, coal and minerals
   cannot be replaced, so use them efficiently and look for alternatives.
3. **Keep waste within what nature can absorb.** Compost degradable waste,
   recycle what can be recycled, and refuse what is not needed.
4. **Protect biodiversity**, because a species once lost is lost for ever.
5. **Include people.** A conservation rule that leaves local people hungry will
   not survive; a rule that gives them a share will.
6. **Think of the long term.** Ask what a decision costs in twenty years, not
   what it earns this year.

### 4.2.2 Sustainable development in Nepal

| Practice | Why it is sustainable |
|---|---|
| Community forestry | the forest is cut and replanted by the people who use it |
| Micro-hydro and solar power | uses a river or the sun without depleting it |
| Organic farming and composting | keeps the soil fertile without poisoning water |
| Biogas plants | turns cattle dung into cooking gas and saves firewood |
| Homestay tourism | income stays in the village and the forest stays standing |
| Rainwater harvesting | stores the monsoon for the dry months |
| Electric buses and safa tempos | less smoke in the valley |

::: example Worked reasoning: the brick kiln and the school
**Situation.** A village near a forest has a chance to lease 20 hectares of
community forest to a brick kiln for five years. The lease would pay Rs 3,00,000
a year and give work to 40 people.

**Reasoning.**
1. **Economy.** Rs 3,00,000 a year and 40 jobs is a real gain, and the money
   could build a school building.
2. **Environment.** The kiln needs firewood and clay. Cutting 20 hectares
   removes the trees that hold the soil, so the slope above the village is more
   likely to landslide. The kiln smoke adds to the dust in the valley.
3. **Society.** The 40 jobs last five years; the landslide and the dried spring
   last much longer. Families that collect firewood and fodder from that forest
   lose their source and must walk further.

**Conclusion.** This lease is **not** sustainable as it stands. A sustainable
version would lease a smaller, flatter, already-degraded piece; require a
replanting plan and a deposit for it; require a cleaner kiln technology
(zig-zag or improved fixed-chimney); and pay a share into a village fund that
uses the money for tree planting and for the families that lose access.
:::

## 4.5 Conservation in Nepal: what is actually done

| Measure | What it is | Example |
|---|---|---|
| Protected areas | parks, reserves and conservation areas under law | 12 national parks, 6 conservation areas, 1 wildlife reserve, 1 hunting reserve |
| Buffer zones | the belt round a park, managed with local users | Chitwan and Bardiya buffer zones |
| Community forestry | forest handed to a user group to manage and use | nearly 23,000 user groups |
| Species programmes | plans for a single threatened species | tiger, rhinoceros, snow leopard, vulture |
| Anti-poaching | patrols, informer networks, prosecution | zero-poaching years for the rhinoceros |
| Benefit sharing | part of park income returned to communities | buffer-zone schools, biogas, compensation |

```figure caption="Why community forestry worked: when the forest belongs to the people who use it, protection becomes self-interest rather than policing."
fig, ax = cycle(["User group\nformed", "Rules and\nharvest plan",
                 "Forest recovers", "Income and\nfuel for members"],
                centre="Community\nforestry")
```

::: example A four-mark answer on biodiversity loss
**Question.** Explain four causes of biodiversity loss in Nepal and one
measure against each.

**Answer.** (i) **Habitat loss** — forest cleared for settlement, roads and
farming; the answer is land-use planning and protected corridors.
(ii) **Poaching and illegal trade** — rhinoceros horn, pangolin scales and
timber; the answer is patrolling, prosecution and community informers.
(iii) **Pollution and over-extraction** — river sand mining, pesticides and
untreated waste; the answer is regulation of mining and waste treatment.
(iv) **Invasive species** — *Mikania* and water hyacinth smothering native
plants; the answer is early removal and planting of native species.
(Climate change, with forest and wetland protection, is the fifth.)
:::

## Chapter summary

- **Biodiversity** is the variety of living beings at three levels: genetic,
  species and ecosystem.
- It matters for food, medicine, clean air and water, fertile soil, protection
  from landslides, income and culture.
- An **ecosystem** is the living community plus its non-living surroundings.
- A **food chain** starts with a green plant and its arrow means "is eaten by";
  joined chains make a **food web**.
- Main threats: deforestation, habitat fragmentation, poaching, pollution,
  invasive species, climate change, over-use and forest fire.
- Conservation is **in-situ** (national parks, community forests, buffer zones,
  Ramsar wetlands) or **ex-situ** (botanical gardens, zoos, seed banks).
- **Sustainable development** meets present needs without harming the ability of
  future generations to meet theirs; it needs the environment, society and the
  economy to be satisfied together.

## Practice questions

**Group A — Objective (1 mark each)**

1. The variety of living beings in a place is called
   <span class="marks">[1]</span>
   (a) ecosystem (b) biodiversity (c) habitat (d) population
2. In a food chain, an arrow means <span class="marks">[1]</span>
   (a) eats (b) lives with (c) is eaten by (d) is bigger than
3. A green plant in a food chain is a <span class="marks">[1]</span>
   (a) producer (b) primary consumer (c) decomposer (d) tertiary consumer
4. Keeping a national park to protect a species where it lives is
   <span class="marks">[1]</span>
   (a) ex-situ conservation (b) in-situ conservation (c) tissue culture
   (d) a seed bank
5. Sustainable development means <span class="marks">[1]</span>
   (a) using all resources now (b) stopping all development
   (c) meeting present needs without harming future needs
   (d) developing only the cities
6. Which of these is a decomposer? <span class="marks">[1]</span>
   (a) grass (b) earthworm (c) grasshopper (d) eagle

::: note Answers to Group A
**1.** (b) — biodiversity is the variety of life.
**2.** (c) — the arrow points from the eaten to the eater.
**3.** (a) — only green plants make their own food.
**4.** (b) — protection in the natural habitat is in-situ.
**5.** (c) — the needs of the future count as much as those of today.
**6.** (b) — the earthworm breaks down dead plant matter into humus.
:::

**Group B — Short answer (2 marks each)**

1. Write the three levels of biodiversity with one example of each.
   <span class="marks">[2]</span>
2. What is an ecosystem? Name any two ecosystems found in Nepal.
   <span class="marks">[2]</span>
3. Write any four threats to biodiversity in Nepal.
   <span class="marks">[2]</span>
4. Give two examples of ex-situ conservation and say why it is needed in
   addition to national parks. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Genetic diversity — many varieties within one species, such as the
thousands of rice varieties grown in Nepal. Species diversity — many different
kinds of living being, such as the spiny babbler, the one-horned rhinoceros and
the sal tree in one park. Ecosystem diversity — different habitats, such as
forest, grassland, wetland and alpine meadow.
**2.** An ecosystem is a community of living beings together with the non-living
surroundings — soil, water, air and sunlight — that they depend on. Two Nepali
examples: the Terai sal forest ecosystem, and the high-altitude lake ecosystem
of Rara.
**3.** Any four of: deforestation; habitat fragmentation by roads and
settlements; poaching and illegal trade in horn, bone, musk and *yarsagumba*;
pollution from pesticides and plastic; invasive species such as *Mikania* and
water hyacinth; climate change; overgrazing and over-collection of firewood;
forest fire.
**4.** Botanical gardens such as the National Botanical Garden at Godavari, and
zoological parks such as the Central Zoo at Jawalakhel (also seed banks and
tissue culture). They are needed because a small population left in one park
can be wiped out by a single disease, fire or flood; keeping the species alive
outside its habitat is a second copy, and it also lets scientists study and
breed the species.
:::

**Group C — Long answer (4 marks each)**

1. Draw a food web with at least four living things from a Nepali forest, and
   explain what would happen to the web if all the frogs died.
   <span class="marks">[4]</span>
2. What is sustainable development? Explain its three circles and give two
   Nepali examples of a sustainable practice and one example of an
   unsustainable one. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Food web.** Grass and paddy (producers) → grasshopper and deer
(primary consumers) → frog and jackal (secondary consumers) → snake and tiger
(tertiary consumers); bacteria and earthworms as decomposers, shown separately
below. Arrows point from the eaten to the eater. **If all the frogs died:** the
grasshoppers they ate would multiply and eat more of the paddy, so the crop
yield would fall; the snakes that fed on frogs would lose a food source and
either eat more of something else — which would then decline — or die; and the
decomposers would receive the bodies of the starved animals, which changes the
amount of humus returning to the soil. A food web is a set of balances, so one
removed link pushes every other link.
**2.** **Sustainable development** is development that meets the needs of the
present generation without destroying the ability of future generations to meet
their needs. **Three circles: environment** — resources must be used no faster
than they renew and waste must stay within what nature can absorb;
**society** — people must have their needs met and must be part of the decision,
otherwise the rule is not followed; **economy** — the activity must be worth
doing and must pay for its own upkeep. A plan is sustainable only where all
three overlap. **Two sustainable examples.** Community forestry, in which the
user group cuts and replants so the forest keeps producing; and biogas plants,
which turn cattle dung into cooking gas, saving firewood and keeping the
village clean. **One unsustainable example.** Selling a whole slope of community
forest to a brick kiln for five years: the money is short-term while the
landslide, the dried spring and the lost firewood last for decades.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** In a food chain, green plants are
   (a) consumers (b) producers (c) decomposers (d) parasites
**2.** About what share of energy passes to the next trophic level?
   (a) 1 % (b) 10 % (c) 50 % (d) 90 %
**3.** Which is an abiotic component?
   (a) earthworm (b) fungus (c) sunlight (d) grass
**4.** *Mikania* (lahare banmara) spreading in Nepal's forests is an example of
   (a) an endemic species (b) an invasive species (c) a keystone species (d) a producer at risk
**5.** The one-horned rhinoceros is best conserved in
   (a) Chitwan National Park (b) Shey Phoksundo (c) Sagarmatha (d) Rara

::: note Objective practice — answers
**1.** (b) — they make food by photosynthesis. **2.** (b) — roughly 10 %. **3.** (c) — sunlight is non-living. **4.** (b) — an introduced species spreading at the cost of native ones. **5.** (a) — Chitwan holds the largest population.
:::

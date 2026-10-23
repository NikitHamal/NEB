---
subject: Science and Technology
grade: 8
title: Life Process
unit: 5
hours: 0
area: Science and Technology
---

Every organism can produce young ones of its own kind. Flowering plants form
seeds in their flowers, and the seeds grow into new plants. Many plants also grow
directly from a root, stem or leaf. Lower plants and fungi form special units
called spores. In higher animals, males and females form gametes, and the joining
of the gametes starts a new life that is born from the mother or hatched from an
egg. Without reproduction a species would die out. This unit studies asexual and
sexual reproduction, pollination and fertilisation, the seed and its germination,
and the basic life processes of nutrition, respiration and growth.

::: key What this unit asks of you
Define reproduction and give its importance; describe fission, budding,
fragmentation, regeneration, sporulation and parthenogenesis; explain natural and
artificial vegetative propagation (cutting, layering, gootee, grafting, tissue
culture); label a flower; explain self- and cross-pollination and double
fertilisation; compare internal and external fertilisation; describe the parts of
a seed, its dispersal and germination and the factors needed for germination.
:::

## 5.1 Reproduction: asexual and sexual

::: definition Reproduction
**Reproduction** is the biological process by which organisms give birth to young
ones of their own kind.
:::

**Importance of reproduction:** (a) it continues the generation and prevents
extinction; (b) it balances the death rate by new births; (c) it is the basis of
new generations; (d) it keeps the biodiversity of the ecosystem in balance.

There are two kinds of reproduction. In **sexual reproduction** a male gamete and
a female gamete fuse. In **asexual reproduction** a new organism forms from a
single parent **without the fusion of gametes**.

### 5.1.1 Types of asexual reproduction

| Type | What happens | Examples |
|---|---|---|
| **Fission** | the parent cell splits; the parent no longer exists. *Binary fission:* into two (lengthwise or crosswise). *Multiple fission:* into many | binary: amoeba, paramecium, euglena, bacteria; multiple: *Plasmodium*, *Chlamydomonas* |
| **Budding** | a small bud grows on the body, develops into a complete organism and separates | yeast, hydra, corals, jellyfish |
| **Fragmentation** | the body breaks into pieces and each piece grows into a new organism | *Spirogyra*, *Marchantia*, lichens, *Mucor* |
| **Regeneration** | a cut piece of the body grows into a whole organism; the parent also regrows the lost part | hydra, planaria, starfish |
| **Sporulation** | single-celled **spores** form inside a **sporangium**, are spread by wind and grow into new plants in moist places | fern, moss, mushroom, *Mucor* |
| **Parthenogenesis** | a new individual develops from an **unfertilised egg** | drone (male) honey bees, aphids, some ants |

In some plants such as banana, pineapple and some cucumbers, the ovary grows into
a fruit **without fertilisation**, giving seedless fruit. This is called
*parthenocarpy*.

```figure caption="Two common kinds of asexual reproduction: binary fission in amoeba (top) and budding in hydra (bottom)."
from matplotlib.patches import Ellipse, Circle
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
def amoeba(x, y, w=1.1, h=0.8, nuc=1):
    ax.add_patch(Ellipse((x, y), w, h, fc="#dfe9f5", ec=ACCENT, lw=1.1))
    for i in range(nuc):
        ax.add_patch(Circle((x + (i - (nuc - 1) / 2) * 0.35, y), 0.11, fc=INK))
amoeba(1.0, 4.6)
amoeba(3.5, 4.6, w=1.6, h=0.75, nuc=2)
ax.add_patch(Ellipse((6.0, 4.6), 0.75, 0.75, fc="#dfe9f5", ec=ACCENT, lw=1.1))
ax.add_patch(Ellipse((6.65, 4.6), 0.75, 0.75, fc="#dfe9f5", ec=ACCENT, lw=1.1))
ax.add_patch(Circle((6.0, 4.6), 0.1, fc=INK)); ax.add_patch(Circle((6.65, 4.6), 0.1, fc=INK))
amoeba(8.4, 4.9, w=0.9, h=0.7); amoeba(9.3, 4.3, w=0.9, h=0.7)
for x in (1.9, 4.6, 7.3):
    ax.annotate("", xy=(x + 0.5, 4.6), xytext=(x, 4.6), arrowprops=dict(arrowstyle="->", color=MUTED))
for x, t in [(1.0, "parent cell"), (3.5, "nucleus divides"), (6.3, "cell splits"), (8.85, "two daughters")]:
    ax.text(x, 3.75, t, ha="center", fontsize=7.4, color=INK)
# hydra budding
def hydra(x, bud=0):
    ax.add_patch(Ellipse((x, 1.4), 0.5, 1.8, fc="#e4efd9", ec=SERIES[2], lw=1.1))
    for dx in (-0.25, -0.08, 0.08, 0.25):
        ax.plot([x + dx, x + dx * 3], [2.25, 2.85], color=SERIES[2], lw=1)
    if bud:
        ax.add_patch(Ellipse((x + 0.35 + 0.1 * bud, 1.2 + 0.1 * bud), 0.25 + 0.15 * bud, 0.45 + 0.25 * bud,
                             angle=-50, fc="#e4efd9", ec=SERIES[2], lw=1.1))
hydra(1.2); hydra(4.0, 1); hydra(6.8, 2)
ax.add_patch(Ellipse((9.0, 1.3), 0.35, 1.2, fc="#e4efd9", ec=SERIES[2], lw=1.1))
for x in (2.0, 4.9, 7.8):
    ax.annotate("", xy=(x + 0.5, 1.4), xytext=(x, 1.4), arrowprops=dict(arrowstyle="->", color=MUTED))
ax.text(4.4, 0.05, "bud appears", ha="center", fontsize=7.4, color=INK)
ax.text(7.3, 0.05, "bud grows", ha="center", fontsize=7.4, color=INK)
ax.text(9.0, 0.05, "new hydra", ha="center", fontsize=7.4, color=INK)
ax.text(1.2, 0.05, "parent hydra", ha="center", fontsize=7.4, color=INK)
fig.tight_layout()
```

**Features of asexual reproduction:** no gametes are formed or fused; there is no
male or female; it can start from any vegetative (body) cell; and the offspring are
**genetically identical** to the parent (clones).

### 5.1.2 Vegetative propagation

The flower is the reproductive part of a plant; the root, stem and leaf are
**vegetative parts**. Asexual reproduction from a vegetative part is called
**vegetative propagation**.

**Natural vegetative propagation**

| Part | How it gives a new plant | Examples |
|---|---|---|
| Root | buds on roots, or food-storing roots, give new shoots | sweet potato, dahlia, asparagus, guava, sissoo |
| Underground stem: sucker | shoots grow from the base of the main stem | banana, bamboo, mint |
| Underground stem: rhizome | flat, food-storing stem with buds | ginger, turmeric, *bojho* |
| Underground stem: corm | swollen base of the shoot with a few buds | *pindalu* (colocasia), gladiolus |
| Underground stem: bulb | round stem with fleshy leaves and buds | onion, garlic, tulip |
| Underground stem: tuber | swollen stem with **eyes** (buds) | potato, yam |
| Aerial stem | buds at the nodes grow roots and shoots | sugarcane, *dubo* grass |
| Bulbils | small buds that drop and grow | agave (*ketuke*), lily, pineapple |
| Leaf | buds in the notches of the leaf margin | *Bryophyllum* (*pattharchatta*), begonia, snake plant |

**Artificial vegetative propagation** is producing new plants asexually with tools
and techniques to improve the quality and quantity of crops.

1. **Cutting** — pieces of stem, root or leaf are planted; a stem cutting should be
   from a one-year-old twig and have at least **two nodes**. *Rose, sugarcane, lemon.*
2. **Layering** — a low, soft branch (the *layer*) has 2–3 cm of bark removed, is
   bent and buried in moist soil; when roots form it is cut off and planted. *Jasmine,
   grape.*
3. **Gootee (air layering)** — a ring of 2–3 cm of bark is removed from a branch
   at least a year old, covered with moist soil (with manure or hormone) and wrapped
   in plastic; after one to two months roots form and the branch is cut and planted.
   *Litchi, mango, guava, orange, pomelo.*
4. **Grafting** — two closely related plants are joined. The rooted lower part is the
   **stock** (a year-old seedling cut 20–30 cm above the ground); the shoot of a
   high-quality plant is the **scion**. Their cut surfaces are fitted, bound with
   grafting tape and wax so no air enters, and kept in shade. The new plant gives
   fruit of the scion's quality. The Nepal Agricultural Research Council (NARC)
   produces many grafted fruit plants.
5. **Tissue culture** — a tiny piece of the parent plant (**explant**) is grown in a
   nutrient medium (**culture medium**) with hormones in a sterile laboratory; it
   forms a mass of cells called **callus**, which grows into thousands of
   disease-free plantlets. It is the most advanced method.

**Advantages of artificial propagation:** the variety can be chosen; plants bear
fruit early; many identical plants are produced quickly; plants without viable
seeds (banana, sugarcane) can be multiplied.

| Layering | Grafting |
|---|---|
| a branch roots while still attached to the parent | two parts of different plants are joined |
| only one plant is involved | stock and scion from two related plants |
| gives a copy of the same plant | combines a strong root with a good-quality shoot |

## 5.2 Sexual reproduction in plants: flower, pollination and fertilisation

**Sexual reproduction** is reproduction by the fusion of male and female gametes
of the same species. The fused cell is the **zygote**, which grows into the new
organism. Organisms with only male or only female organs are **unisexual**; those
with both (e.g. the mustard flower, earthworm) are **bisexual** (hermaphrodite).

**Features:** gametes form and fuse; male and female organs exist; offspring show
**variation**, are more adaptable to a changing environment and make evolution
possible.

### 5.2.1 The flower

The flower is the reproductive part of a flowering plant.

```figure caption="Parts of a bisexual flower in section. The stamen (anther + filament) is the male part; the pistil (stigma + style + ovary) is the female part."
from matplotlib.patches import Ellipse, Polygon
fig, ax = plt.subplots(figsize=(5.0, 3.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")
ax.plot([5, 5], [0.2, 1.6], color=SERIES[2], lw=3)
ax.add_patch(Ellipse((5, 1.75), 1.8, 0.6, fc="#cfe3c4", ec=SERIES[2]))
ax.add_patch(Polygon([[4.2, 1.9], [2.6, 2.9], [3.9, 2.3]], fc="#9cc98a", ec=SERIES[2]))
ax.add_patch(Polygon([[5.8, 1.9], [7.4, 2.9], [6.1, 2.3]], fc="#9cc98a", ec=SERIES[2]))
ax.add_patch(Polygon([[4.3, 2.1], [2.2, 5.6], [3.2, 5.8], [4.6, 2.4]], fc="#f6cdd6", ec=SERIES[1]))
ax.add_patch(Polygon([[5.7, 2.1], [7.8, 5.6], [6.8, 5.8], [5.4, 2.4]], fc="#f6cdd6", ec=SERIES[1]))
ax.add_patch(Ellipse((5, 2.6), 1.1, 1.1, fc="#f3e3b5", ec=INK))
for dy in (-0.2, 0.2):
    ax.add_patch(Ellipse((5 + dy, 2.6), 0.22, 0.32, fc="white", ec=INK, lw=0.8))
ax.plot([5, 5], [3.15, 4.9], color=INK, lw=2)
ax.add_patch(Ellipse((5, 5.0), 0.6, 0.25, fc=SERIES[3], ec=INK))
for x0, x1 in [(4.5, 3.9), (5.5, 6.1)]:
    ax.plot([x0, x1], [2.3, 4.3], color=MUTED, lw=1.4)
    ax.add_patch(Ellipse((x1, 4.45), 0.3, 0.45, fc="#e6b84a", ec=INK))
lab = dict(fontsize=7.6, color=INK, va="center")
def tag(x, y, tx, ty, s, ha="left"):
    ha = "left" if tx > x else "right"
    ax.plot([x, tx - 0.1 if ha == "left" else tx + 0.1], [y, ty], color=MUTED, lw=0.7)
    ax.text(tx, ty, s, ha=ha, **lab)
tag(5.15, 5.05, 7.6, 6.6, "stigma")
tag(5.05, 4.0, 8.2, 4.6, "style")
tag(5.5, 2.75, 8.2, 3.3, "ovary")
tag(5.2, 2.6, 8.2, 2.3, "ovule")
tag(6.25, 4.5, 8.2, 5.6, "anther")
tag(4.2, 3.4, 1.9, 3.9, "filament")
tag(2.7, 5.2, 1.9, 5.0, "petal")
tag(3.0, 2.75, 1.9, 2.9, "sepal")
tag(4.4, 1.7, 1.9, 1.5, "receptacle")
tag(5.0, 0.8, 7.0, 0.6, "pedicel (stalk)")
fig.tight_layout()
```

| Whorl | Part | Function |
|---|---|---|
| Calyx (sepals) | green outer leaves | protects the flower in the bud |
| Corolla (petals) | coloured leaves | attracts insects and birds |
| Androecium (stamens) | **filament** and **anther**; pollen grains form in the anther | male part |
| Gynoecium (pistil) | **stigma**, **style**, **ovary** with **ovules** | female part |

### 5.2.2 Pollination

::: definition Pollination
**Pollination** is the transfer of pollen grains from the anther to the stigma of
the same flower or of another flower of the same species.
:::

A pollen grain is a single, microscopic cell with a double wall; its sticky or
rough outer wall helps it stick to the stigma.

**Self-pollination** is the transfer of pollen to the stigma of the same flower
(**autogamy**) or of another flower on the **same plant** (**geitonogamy**). It
occurs in small, dull flowers without nectar or scent. *Paddy, wheat, groundnut,
pea.*
*Advantages:* good parental characters are kept; seed formation is almost sure; no
agent needed. *Disadvantages:* no new characters; reproductive vigour slowly falls;
bad characters cannot be removed.

**Cross-pollination** is the transfer of pollen to the stigma of a flower on a
**different plant of the same species**. It occurs in colourful, scented flowers
with nectar, or where anther and stigma ripen at different times. It needs agents:

| Agent | Name | Examples |
|---|---|---|
| wind | anemophily | maize, pine, mango |
| water | hydrophily | *Vallisneria*, some water plants |
| insects (bee, butterfly, fly) | entomophily | mustard, sunflower, pumpkin |
| birds (sunbird, tailorbird) | ornithophily | bottle-brush, silk cotton |

*Advantages:* new and better varieties; offspring adapt better; seeds germinate
well. *Disadvantages:* depends on agents; good characters may not be preserved;
unwanted characters may come in.

```photo id="sci8/bee-pollination" caption="A honey bee visiting a flower for nectar. Pollen sticks to its hairy body and is carried to the next flower — entomophily." width="80"
key 1 Anthers, which shed the pollen
key 2 Pollen sticking to the bee's body hairs
key 3 Petals
```

### 5.2.3 Fertilisation and double fertilisation

::: definition Fertilisation
**Fertilisation** is the fusion of a male gamete with a female gamete (egg) of the
same species to form a **zygote**.
:::

In a flowering plant: (1) a pollen grain on the stigma absorbs water and sugar from
the stigma fluid and grows a **pollen tube**; (2) the tube grows down through the
style into the ovary and enters an **ovule**; (3) on the way its nucleus divides to
form **two male gametes**; (4) one male gamete fuses with the **egg** → **zygote**
(becomes the embryo); (5) the other fuses with the **secondary nucleus** (the two
fused polar nuclei) → **endosperm nucleus** (becomes food store). Because two
fusions happen, this is **double fertilisation**; it is found only in flowering plants.

After fertilisation, the **ovule becomes the seed** and the **ovary becomes the
fruit**; the petals, stamens, style and stigma usually wither.

| Pollination | Fertilisation |
|---|---|
| transfer of pollen from anther to stigma | fusion of male gamete and egg |
| happens on the stigma, outside the ovary | happens inside the ovule (in the ovary) |
| needs agents in cross-pollination | needs a pollen tube |
| comes first | follows pollination |

## 5.3 Sexual reproduction in animals: internal and external fertilisation

In most animals males and females are separate. The male's **testes** produce
**sperms**; the female's **ovaries** produce **ova** (eggs). Forming gametes is
called **gametogenesis**. A sperm has an oval head, a middle piece and a long tail
for swimming; an ovum is much larger and round, with stored food. Millions of
sperms are made, but in a woman usually only one ovum is released in a month.

During fertilisation only **one sperm** enters the ovum, and their nuclei fuse to
form the **zygote** — the first cell of the new individual. The zygote divides to
form an **embryo**, which grows into a baby. The time from fertilisation to birth or
hatching is the embryonic (gestation) period.

**Male → sperm, female → ovum → (fertilisation) → zygote → embryo → young one**

| Internal fertilisation | External fertilisation |
|---|---|
| sperm and ovum fuse **inside the female's body** (in humans, in the fallopian tube) | sperm and ova fuse **outside**, in water |
| mating is needed | the female lays many eggs; the male sheds sperms over them |
| fewer eggs, well protected | very many eggs, many are eaten or lost |
| insects, reptiles, birds, mammals (human, cow, bat, whale, pigeon, tortoise, butterfly) | fish and most amphibians (frog) |

Internal fertilisation is safer because the gametes and embryo are protected from
drying, temperature change and predators inside the female's body.

::: example Classify the fertilisation
**Question.** Name the type of fertilisation: human, pigeon, tortoise, butterfly,
fish, bat, frog, cow, dragonfly, whale.

**Answer.** *Internal:* human, pigeon, tortoise, butterfly, bat, cow, dragonfly,
whale. *External:* fish, frog.
:::

## 5.4 The seed: structure, germination and dispersal

After fertilisation the zygote in the ovule develops into an **embryo**, and the
ovule becomes a **seed** that can grow into a new plant under suitable conditions.

### 5.4.1 Structure of a seed

1. **Seed coat** — outer covering of two layers: thick outer **testa** and thin
   inner **tegmen**. It protects the seed and keeps it dormant in bad conditions.
2. **Embryo** — the living baby plant: **radicle** (becomes the root),
   **plumule** (becomes the shoot) and **cotyledons** (seed leaves). Cotyledons
   protect the radicle and plumule, store food in dicots, and in many plants come
   above the soil as the first green leaves. Monocots have **one** cotyledon,
   dicots **two**.
3. **Endosperm** — stored food (starch, protein) used by the embryo until the
   seedling can make its own food. All monocot seeds (maize, rice) have it; most
   dicot seeds (bean, pea, gram) store food in the cotyledons instead.

```figure caption="A bean seed (dicot) opened by separating the two cotyledons."
from matplotlib.patches import Ellipse
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")
ax.add_patch(Ellipse((4.2, 2.8), 6.0, 4.0, fc="#efe2c4", ec=INK, lw=2.4))
ax.add_patch(Ellipse((4.2, 2.8), 5.5, 3.5, fc="#f7efd9", ec=MUTED, lw=0.8))
ax.plot([6.2, 5.7, 5.3], [2.7, 2.55, 2.2], color=SERIES[3], lw=4, solid_capstyle="round")
ax.plot([6.2, 6.3], [2.7, 3.2], color=SERIES[2], lw=3)
ax.add_patch(Ellipse((6.38, 3.38), 0.42, 0.22, angle=40, fc=SERIES[2], ec="none"))
lab = dict(fontsize=7.8, color=INK, va="center")
def tag(x, y, tx, ty, s):
    ax.plot([x, tx - 0.1], [y, ty], color=MUTED, lw=0.7)
    ax.text(tx, ty, s, ha="left", **lab)
tag(6.45, 3.45, 7.8, 4.7, "plumule")
tag(5.4, 2.25, 7.8, 1.4, "radicle")
tag(4.2, 1.6, 7.8, 0.35, "cotyledon")
ax.plot([1.35, 1.0], [4.0, 4.95], color=MUTED, lw=0.7)
ax.text(1.0, 5.2, "seed coat", ha="center", **lab)
fig.tight_layout()
```

### 5.4.2 Dispersal of seeds

**Dispersal** is the carrying of seeds away from the parent plant by an agent. It
reduces crowding and competition and lets the plant reach new places.

| Agent | Features of seed/fruit | Examples |
|---|---|---|
| Wind | small, light, with hairs, wings or air sacs (lower density, so they float in air) | silk cotton (*simal*), *aak*, *kans* and *khar* grass, dandelion, maple |
| Water | light, waterproof, can float | lotus, coconut, mangrove |
| Animals | edible fleshy fruits (seeds swallowed and passed out, or thrown away); hooks and spines that stick to fur | *jamun*, *kafal*, guava, *harro*, *amala*; *kuro* (cobbler's pegs), *bhede kuro* |
| Gravity | heavy fruits fall below the plant | mango, apple, coconut |
| Bursting of pods | dry pods burst and throw seeds out | mustard, pea, bean, sesame, gram, *dhaturo* |

### 5.4.3 Germination

::: definition Germination and dormancy
**Germination** is the development of the root and shoot of a new plant from a seed.
**Dormancy** is the resting state in which a dry seed stays alive without growing;
it preserves the life and germinating power of the seed until conditions are suitable.
:::

When a seed gets water, air and warmth, it swells and its enzymes become active.
The **radicle** comes out first and grows down into the root; then the **plumule**
grows up into the shoot; the cotyledons may become the first green leaves.

```photo id="sci8/bean-germination" caption="A bean seed germinating, stage by stage. The radicle comes out first and grows downwards; the plumule follows and grows upwards." width="80"
key 1 Seed coat splitting as the seed swells
key 2 Radicle, the first root
key 3 Plumule with the first true leaves
```

**Factors needed for germination**

| Factor | Why it is needed |
|---|---|
| Water | softens the seed coat, breaks dormancy, starts metabolism (seeds are soaked about 24 hours before sowing) |
| Air (oxygen) | for respiration in mitochondria, which releases energy for growth |
| Suitable temperature | about 16–24 °C for most seeds; very high or low temperature stops it |
| Light | not needed by most seeds to sprout, but the seedling needs it to photosynthesise |

::: example Germination percentage
**Problem.** A farmer tests 50 wheat seeds on moist cotton; 42 germinate. Find the
germination percentage. Is the seed good for sowing if at least 80 % is needed?
**Solution.** Germination % $=\frac{42}{50}\times100\%=84\%$. Yes — 84 % is more than 80 %.
:::

::: note Activity 5.13 — three seeds on one stick
Tie three similar seeds on a stick — one at the top, one in the middle and one at the
bottom — and stand it in a beaker so that the bottom seed is under water, the middle
one half in water and the top one in air. After 2–3 days only the **middle** seed
germinates: the top seed has air but no water, the bottom seed has water but too
little air. **Conclusion:** both water and air are needed.
:::

**Importance of germination:** continues the plant's generation; good germination
increases farm yield; germinated seeds (sprouts) are more nutritious; germination
of grass and tree seeds conserves forests and pastures.

::: example The case of Suryanarayan's wheat field
**Situation.** Suryanarayan sowed wheat and dug the field again to bury the seeds.
Seedlings were good in the moist part but poor in the dry part.

**Answers.** (i) He dug again to cover the seeds with soil so that they get moisture
and warmth and are not eaten by birds. (ii) In the dry part there was not enough
water to break dormancy. (iii) Irrigate the field evenly (or sow after rain), use
good seeds, and sow at the right depth and season.
:::

## 5.5 Growth, nutrition and respiration in living beings

**Nutrition** is taking in and using food. Green plants are **autotrophs**: they make
their own food by **photosynthesis** in chloroplasts:

carbon dioxide + water --(sunlight, chlorophyll)--> glucose + oxygen

Animals, fungi and most bacteria are **heterotrophs**: they depend on food made by
others, either by eating it (holozoic, e.g. cow, human), absorbing it from dead
matter (saprophytic, e.g. mushroom) or living on a host (parasitic, e.g. tapeworm).

**Respiration** is the breakdown of food (glucose) in the cells to release energy.
It happens in the **mitochondria** of all living cells, day and night:

glucose + oxygen → carbon dioxide + water + energy

Without oxygen (anaerobic respiration), yeast makes alcohol and carbon dioxide, and
tired muscles make lactic acid; much less energy is released.

**Growth** is the permanent increase in the size and mass of an organism, caused by
cell division and enlargement. It uses the food from nutrition and the energy from
respiration. Plants grow throughout life at their tips (meristems); animals grow
until adulthood.

| Process | Experiment that shows it | Result |
|---|---|---|
| Photosynthesis needs light | destarch a plant, cover part of a leaf, test with iodine | covered part stays brown; the rest turns blue-black |
| Photosynthesis releases oxygen | *Hydrilla* under a funnel and test tube in water, in sunlight | gas relights a glowing splint |
| Respiration releases CO₂ | breathe through lime water | lime water turns milky |
| Germinating seeds respire | seeds in a flask with lime water | lime water turns milky |

## Chapter summary

- **Reproduction** gives birth to one's own kind; it is asexual (no gametes) or
  sexual (fusion of gametes).
- Asexual types: fission, budding, fragmentation, regeneration, sporulation,
  parthenogenesis. Offspring are identical to the parent.
- Vegetative propagation: natural (root, sucker, rhizome, corm, bulb, tuber, aerial
  stem, bulbil, leaf) and artificial (cutting, layering, gootee, grafting, tissue culture).
- Flower: sepals, petals, stamens (anther + filament), pistil (stigma + style + ovary).
- **Pollination**: self (autogamy, geitonogamy) and cross (wind, water, insects, birds).
- **Double fertilisation**: male gamete + egg → zygote; male gamete + secondary
  nucleus → endosperm. Ovule → seed; ovary → fruit.
- Animals: internal fertilisation (insects, reptiles, birds, mammals) and external
  (fish, frog).
- Seed = seed coat + embryo (radicle, plumule, cotyledons) + endosperm; dispersed by
  wind, water, animals, gravity and bursting; germinates with water, air and warmth.

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Textbook exercises.)*

1. How are new organisms formed during regeneration? <span class="marks">[1]</span>
   (a) new life grows from a fresh fragment (b) the separated part regenerates into a whole body (c) the part fragments again (d) the body develops directly
2. What must be followed in propagation by cutting? <span class="marks">[1]</span>
   (a) a few leaves on the piece (b) new buds on the piece (c) the piece from the top of the stem (d) a few nodes on the piece
3. Which represents the meaning of reproduction? <span class="marks">[1]</span>
   (a) birth and death (b) giving birth at maturity (c) biological process of giving birth to one's own kind (d) forming seeds and laying eggs
4. Tissue culture is related to which statement? <span class="marks">[1]</span>
   (a) only a small piece of the parent plant is taken (b) the whole plant is taken (c) pieces of plants and animals are used (d) it works only in non-flowering plants
5. Where does fertilisation take place in flowering plants? <span class="marks">[1]</span>
   (a) stigma (b) ovary wall (c) ovule (d) style
6. Pollination carried out by flies is <span class="marks">[1]</span>
   (a) self-pollination (b) pollen germination (c) hydrophily (d) entomophily
7. Which animal has internal fertilisation? <span class="marks">[1]</span>
   (a) lizard (b) frog (c) rohu fish (d) toad
8. Which sequence of events is correct? <span class="marks">[1]</span>
   (a) anther, stigma, pollen grain, pollen tube (b) anther, pollen grain, stigma, germination (c) pollen tube, pollen grain, style, anther (d) pollen grain, anther, pollen tube, stigma
9. *Khar* (thatch grass) disperses its seeds through <span class="marks">[1]</span>
   (a) air (b) water (c) bursting pods (d) birds
10. The main function of a seed is <span class="marks">[1]</span>
   (a) to form fruit (b) to produce a new plant (c) to store nutrients (d) to protect the embryo
11. Which event occurs during germination? <span class="marks">[1]</span>
   (a) plumule and radicle make the cotyledon (b) endosperm becomes the root (c) the stem grows from the seed coat (d) cotyledons become the first (embryonic) leaves
12. Seeds are not stored in moist places mainly <span class="marks">[1]</span>
   (a) to keep them warm (b) to make them heavy (c) to protect them from light (d) to prevent germination (and rotting)
13. Dormancy <span class="marks">[1]</span>
   (a) preserves the life and germinating power of seeds (b) adds nutrients (c) keeps out air and water (d) carries out germination reactions
14. Wings and air sacs on wind-dispersed seeds help because they <span class="marks">[1]</span>
   (a) protect seeds from strong wind (b) make the seeds burst (c) push seeds out of fruits (d) lower the density so seeds float in air

::: note Answers to Group A
**1.** (b). **2.** (d) — at least two nodes. **3.** (c). **4.** (a) — a small explant. **5.** (c) — inside the ovule, which lies in the ovary. **6.** (d). **7.** (a) — reptiles fertilise internally. **8.** (b). **9.** (a). **10.** (b). **11.** (d). **12.** (d) — moisture breaks dormancy and also lets fungi rot the seeds. **13.** (a). **14.** (d).
:::

**Group B — Short answer (2 marks each)**

1. Differentiate: (a) fission and budding (b) bulbil and rhizome (c) natural and artificial vegetative propagation. <span class="marks">[3]</span>
2. Give reasons: (a) Asexual reproduction has no concept of male and female. (b) Growing potatoes from tubers is vegetative propagation. (c) Farmers benefit from grafting. (d) Tissue culture is the most advanced method of vegetative propagation. <span class="marks">[4]</span>
3. Name the method of asexual reproduction: yeast, paramecium, pineapple, banana, planaria, begonia, ginger, onion, sugarcane, *Mucor*, sweet potato, *Spirogyra*. <span class="marks">[3]</span>
4. What are stock and scion? Write two advantages of grafting. <span class="marks">[2]</span>
5. Differentiate: (a) gamete and zygote (b) anther and pollen grain (c) autogamy and geitonogamy. <span class="marks">[3]</span>
6. Give reasons: (a) Pollinating agents play a great role in pollination. (b) Both male and female are needed for sexual reproduction. (c) Internal fertilisation is safer than external fertilisation. <span class="marks">[3]</span>
7. What is gametogenesis? Where does it occur in plants and animals? <span class="marks">[2]</span>
8. Differentiate: (a) dispersal and germination of seeds (b) plumule and radicle (c) dispersal of mustard seeds and of *kafal* seeds. <span class="marks">[3]</span>
9. Give reasons: (a) Seeds germinate if soaked in water. (b) Silk cotton seeds are dispersed far. (c) Eating sprouted seeds is more beneficial than dry seeds. <span class="marks">[3]</span>

::: note Answers to Group B
**1.** (a) In fission the parent splits and disappears (amoeba); in budding a bud grows on the parent and separates, and the parent remains (yeast, hydra). (b) A bulbil is a small bud that falls and grows (agave, lily); a rhizome is a thick underground stem with buds lying flat under the soil (ginger). (c) Natural propagation happens by itself through roots, stems or leaves (potato, *Bryophyllum*); artificial propagation is done by people with tools (cutting, layering, grafting, tissue culture) to improve crops.
**2.** (a) There is no formation or fusion of gametes; only one parent is involved. (b) The tuber is a stem (a vegetative part) and its eyes are buds that grow into new plants. (c) Grafted plants bear fruit early and have the high quality of the scion, so yield and income increase. (d) Thousands of disease-free, identical plantlets are produced from a tiny piece in a short time in any season.
**3.** Yeast — budding; paramecium — binary fission; pineapple — bulbils (and suckers); banana — sucker; planaria — regeneration; begonia — leaf; ginger — rhizome; onion — bulb; sugarcane — stem cutting (aerial stem); *Mucor* — sporulation (and fragmentation); sweet potato — root; *Spirogyra* — fragmentation.
**4.** The stock is the lower rooted part (a young seedling); the scion is the twig of a good-quality plant joined on it. Advantages: early fruiting; fruit of the desired quality; combines a hardy root with a productive shoot.
**5.** (a) A gamete is a single reproductive cell (sperm or ovum); a zygote is the cell formed by fusion of two gametes. (b) The anther is the part of the stamen that makes pollen; a pollen grain is the tiny cell formed in it that carries the male gametes. (c) Autogamy: pollen to the stigma of the same flower; geitonogamy: pollen to another flower of the same plant.
**6.** (a) In cross-pollination pollen cannot move by itself; wind, water, insects and birds carry it. (b) The male gives the sperm and the female the ovum; only their fusion forms the zygote. (c) The gametes and embryo stay inside the female's body, protected from drying, cold and predators.
**7.** Gametogenesis is the formation of gametes. In plants it occurs in the anther (pollen, male gametes) and ovule (egg); in animals in the testes (sperms) and ovaries (ova).
**8.** (a) Dispersal is carrying seeds away from the parent; germination is the growth of a seed into a seedling. (b) The plumule grows upward into the shoot; the radicle grows downward into the root. (c) Mustard seeds are thrown out when dry pods burst; *kafal* seeds are swallowed by birds and animals with the fruit and passed out elsewhere.
**9.** (a) Water softens the coat, breaks dormancy and starts enzyme action. (b) They are light and covered with silky hairs, so the wind carries them. (c) Sprouting changes stored food into simpler forms and increases vitamins, so sprouts are easier to digest and more nutritious.
:::

**Group C — Long answer (4 marks each)**

1. What are the types of asexual reproduction? Describe budding in hydra with a diagram. <span class="marks">[4]</span>
2. Compare self-pollination and cross-pollination with their advantages and disadvantages. <span class="marks">[4]</span>
3. What is double fertilisation? Describe the process. <span class="marks">[4]</span>
4. Write the methods of seed dispersal and explain any one with examples. Name the method for mango, chestnut, maple, gram, cobbler's pegs, sesame, pumpkin, coconut and pear. <span class="marks">[4]</span>
5. Explain the germination of a seed with a diagram, and the role of air in germination. <span class="marks">[4]</span>
6. "If there is no pollination, fertilisation is nearly impossible." Justify. What happens if the style of a flower is removed? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Fission, budding, fragmentation, regeneration, sporulation, parthenogenesis. *Budding in hydra:* when food is plenty, a small bulge (bud) appears on the side of the body; it grows, develops a mouth and tentacles, and finally separates as a new hydra. Draw the stages as in the figure in 5.1.1.
**2.** Self: pollen to the same flower or same plant; small dull flowers; no agent needed; seed setting is sure and parent characters are kept, but no new variety and vigour falls. Cross: pollen to another plant of the same species; bright, scented flowers with nectar; needs agents; gives new, stronger and better-adapted varieties, but depends on agents and may bring unwanted characters.
**3.** Two fusions in the ovule of a flowering plant. The pollen grain forms a pollen tube that grows through the style to the ovule; its nucleus forms two male gametes; one fuses with the egg to form the zygote (→ embryo) and the other fuses with the secondary nucleus to form the endosperm nucleus (→ endosperm). Then the ovule becomes the seed and the ovary the fruit.
**4.** Wind, water, animals, gravity and bursting of pods (table in 5.4.2). Mango — gravity (and animals); chestnut — bursting/gravity; maple — wind; gram — bursting of pods; cobbler's pegs — animals (sticking); sesame — bursting of pods; pumpkin — animals/people; coconut — water; pear — animals.
**5.** The seed absorbs water and swells, the coat softens, enzymes change stored food into simple sugar, the radicle emerges and grows down, then the plumule grows up and the cotyledons open as the first leaves (draw a bean seedling with seed coat, radicle, plumule and cotyledons). Air gives oxygen for respiration, which releases the energy needed for cell division and growth; seeds in waterlogged soil fail for lack of oxygen.
**6.** Fertilisation needs the male gametes, which reach the ovule only in a pollen tube that grows from pollen lying on the stigma; without pollination no pollen reaches the stigma, so no pollen tube, no male gamete and no fertilisation (except in parthenocarpic fruits, which have no seeds). If the style is removed, the stigma is also lost and the pollen tube has no path to the ovary, so fertilisation and seed formation cannot occur.
:::

---
subject: Science and Technology
grade: 8
title: Life Process
unit: 5
hours: 0
area: Science and Technology
---

A living being does certain things that a stone never does: it takes in food, it
breathes, it grows, it gets rid of waste, it responds, and it produces new
individuals like itself. These activities together are called **life
processes**. Nutrition, respiration, excretion and growth are covered in the
earlier grades; this unit gives its main attention to **reproduction** — how a
new individual is made, in a plant, in an animal and from a single seed.

::: key What this unit asks of you
You should be able to distinguish asexual from sexual reproduction and give
examples of each, name the parts of a flower and state the function of each,
explain pollination, fertilisation and the formation of the fruit and seed,
compare internal with external fertilisation, and describe the structure and
germination of a seed with the conditions it needs.
:::

## 5.1 Reproduction

**Reproduction** is the process by which a living being produces a new
individual of its own kind. It is what keeps a species from dying out — an
individual can live without reproducing, but a species cannot.

Reproduction happens in two ways.

| | Asexual reproduction | Sexual reproduction |
|---|---|---|
| How many parents | one | two (usually) |
| Sex cells (gametes) | none | male and female gametes join |
| New individual is | almost an exact copy of the parent | a mixture of both parents |
| Speed and numbers | fast; often many at once | slower; usually fewer |
| Variation | very little | much more |
| Examples | binary fission in Amoeba, budding in yeast and Hydra, vegetative propagation in potato and sugarcane | flowering plants, fish, frog, cow, human |

### 5.1.1 Asexual reproduction

- **Binary fission.** The parent cell divides into two equal daughter cells.
  Amoeba, Paramecium and bacteria do this. In good conditions an Amoeba can
  divide every few hours.
- **Budding.** A small outgrowth (a bud) grows on the parent's body, and when
  it is large enough it separates. Yeast and Hydra do this.
- **Fragmentation.** The body breaks into pieces, and each piece grows into a
  new individual. Spirogyra and some flatworms do this.
- **Spore formation.** The parent makes a large number of microscopic spores,
  each able to grow into a new individual. *Rhizopus*, the bread mould, does
  this.
- **Vegetative propagation.** A part of a plant — a root, stem, leaf or bud —
  grows into a new plant. This is the method farmers use most.

| Vegetative part | Example |
|---|---|
| Tuber (swollen underground stem) | potato |
| Bulb | onion, garlic |
| Rhizome | ginger, turmeric |
| Stem cutting | sugarcane, rose, *dhalne phool* |
| Sucker | banana, pineapple |
| Leaf | *Bryophyllum* |
| Root | sweet potato, dahlia |
| Layering and grafting | mango, orange, guava |

::: tip Why farmers prefer vegetative propagation
The new plant is a copy of the parent, so a farmer who has one exceptionally
good mango tree can raise many trees that give the same fruit. There is also no
waiting for a seed to grow: a grafted sapling bears fruit years earlier than a
seedling. The disadvantage is that all the copies share the same weakness, so
one disease can destroy the whole orchard.
:::

## 5.2 Sexual reproduction in plants

The flower is the reproductive organ of a flowering plant. Its parts are
arranged in four rings.

```figure caption="A flower cut open. The male parts make pollen, the female part holds the egg, and the colourful petals exist only to bring the pollinator in."
from matplotlib.patches import Ellipse
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.6)
ax.axis("off")
ax.plot([5.0, 5.0], [1.2, 4.2], color=INK, lw=2.0)
ax.add_patch(plt.Circle((5.0, 4.35), 0.28, fc=SERIES[2], alpha=0.85))
ax.text(5.0, 4.95, "stigma", ha="center", fontsize=6.6, color=SERIES[2])
ax.text(5.35, 3.5, "style", ha="left", fontsize=6.6, color=INK)
ax.add_patch(plt.Circle((5.0, 1.25), 0.45, fc=SERIES[2], alpha=0.5))
ax.text(5.0, 0.6, "ovary (holds ovules)", ha="center", fontsize=6.6, color=SERIES[2])
for x0 in (3.3, 6.7):
    ax.plot([x0, x0], [1.6, 4.0], color=ACCENT, lw=1.4)
    ax.add_patch(plt.Circle((x0, 4.15), 0.22, fc=ACCENT, alpha=0.85))
ax.text(2.0, 4.5, "anther (pollen)", ha="center", fontsize=6.6, color=ACCENT)
ax.text(8.1, 3.4, "filament", ha="center", fontsize=6.6, color=ACCENT)
for x0 in (2.2, 7.8):
    ax.add_patch(Ellipse((x0, 2.8), 1.5, 2.4, fc=SERIES[1], alpha=0.28,
                             ec=SERIES[1], lw=1.0))
ax.text(1.4, 1.2, "petal", ha="center", fontsize=6.6, color=SERIES[1])
ax.add_patch(Ellipse((5.0, 1.15), 6.4, 1.5, fc="#cfe3c8", alpha=0.55,
                         ec="#5d8a4a", lw=1.0))
ax.text(1.3, 0.25, "sepal", ha="left", fontsize=6.4, color="#4a6b3a")
ax.text(9.6, 5.6, "male: androecium", ha="right", fontsize=6.8, color=ACCENT)
ax.text(9.6, 5.05, "female: gynoecium", ha="right", fontsize=6.8, color=SERIES[2])
fig.tight_layout()
```

| Part | Function |
|---|---|
| Sepal | protects the flower while it is a bud |
| Petal | bright colour and scent attract insects and birds |
| Stamen (anther + filament) | the male part; the anther makes pollen grains |
| Carpel (stigma + style + ovary) | the female part; the ovary holds the ovules (eggs) |

### 5.2.1 Pollination

**Pollination** is the transfer of pollen from the anther of a flower to the
stigma of a flower. If it happens in the same flower or in another flower of
the same plant it is **self-pollination**; if the pollen goes to a flower of a
different plant of the same kind it is **cross-pollination**.

| Agent | How it carries pollen | Example plant |
|---|---|---|
| Insect or bird | pollen sticks to the body while drinking nectar | mustard, orange, sunflower |
| Wind | light, dry pollen blows in the air; stigmas are feathery | maize, wheat, pine |
| Water | pollen floats to the female flower | lotus, water hyacinth |
| Animal | fur carries pollen from flower to flower | *Rhododendron* visited by birds |

```photo id="sci8/bee-pollination" caption="A honey bee drinking nectar. Pollen from the flower's anthers sticks to the hairs on the bee's body and is carried to the next flower — the bee is paid in nectar, and the plant is paid in pollination." width="86"
key 1 Anthers, which shed the pollen
key 2 Pollen sticking to the bee's body hairs
key 3 Petals, the landing place and the advertisement
```
### 5.2.2 Fertilisation and the fruit

After pollination the pollen grain grows a tube down through the style into the
ovary. The male gamete inside the pollen travels down the tube and joins the
female gamete (the egg) inside the ovule. This joining is **fertilisation**.

| After fertilisation | Becomes |
|---|---|
| Ovule | seed |
| Ovary | fruit |
| Zygote (the fertilised egg) | embryo inside the seed |
| Petals, stamens, sepals | dry up and fall off |

So the fruit you eat — a mango, a tomato, a pea pod — is a grown-up ovary, and
the seeds inside it are grown-up ovules. That is why a fruit that has not been
pollinated has no seeds, and often does not form at all.

### 5.2.3 Sexual reproduction in animals

Animals also produce male and female gametes, but they differ in where the
joining takes place.

| | External fertilisation | Internal fertilisation |
|---|---|---|
| Where the gametes join | outside the body, in water | inside the female's body |
| Animals | most fish, frog, toad | reptiles, birds, mammals |
| Eggs laid | very many, in water | few, protected |
| Care of the young | usually none; most eggs and young are eaten | often some care, from guarding eggs to feeding milk |

In frogs, the female lays a mass of eggs in water and the male releases his
gametes over them. In birds and reptiles the egg is fertilised inside the
female and laid with a shell; in mammals the young develops inside the mother
and is fed with milk after birth.

::: caution The egg we eat is not a baby bird
A hen's egg that you buy in the market has not been fertilised, because there
is no male bird with the flock. It contains one female gamete plus food and a
shell, and it would never hatch. This is also why hens lay eggs almost every
day: the egg is produced whether or not fertilisation happens.
:::

## 5.3 The seed

A seed contains a baby plant (the embryo) with a store of food, wrapped in a
protective coat. A **monocotyledonous** seed, such as maize or rice, has one
cotyledon; a **dicotyledonous** seed, such as bean or pea, has two.

| Part of a bean seed | Function |
|---|---|
| Seed coat (testa) | protects the embryo from damage and drying |
| Cotyledon (two) | stores food for the seedling until it can make its own |
| Embryo | the young plant: plumule (future shoot) and radicle (future root) |
| Micropyle | the small pore through which water enters |

```photo id="sci8/bean-germination" caption="A bean seed germinating, stage by stage. The radicle comes out first and grows downwards; the plumule follows and grows upwards. Growth never waits for the food store to run out." width="84"
key 1 Seed coat splitting as the seed swells
key 2 Radicle, the first root
key 3 Plumule with the first true leaves
```
### 5.3.1 Germination and the conditions it needs

**Germination** is the growth of the embryo out of the seed into a seedling.

| Condition | Why it is needed |
|---|---|
| Water | softens the seed coat, activates the enzymes and dissolves the stored food |
| Air (oxygen) | for respiration, which releases the energy for growth |
| Suitable temperature | warmth speeds up the enzymes; too much heat kills the embryo |
| (Light) | not needed for most seeds to germinate, but needed soon after for the seedling to make food |

A simple proof: soak three lots of bean seeds — one kept dry, one kept in
boiled water covered with oil (no oxygen), one kept wet at room temperature.
Only the third lot germinates. Each other lot is missing exactly one condition.

### 5.3.2 Dispersal of seeds

If all the seeds fell under the parent plant they would compete with the parent
and with each other for light, water and minerals. Seeds are therefore carried
away.

| Agent | How | Example |
|---|---|---|
| Wind | light seeds with hairs or wings | *Bhimal*, dandelion, pine |
| Water | light, waterproof seed coat | coconut, lotus |
| Animal | hooks stick to fur; fruit is eaten and the seed dropped | *Bichu ghas*, guava, tomato |
| Explosion | the dry fruit bursts and throws the seeds | pea, bean, *Sisoo* |
| Human being | seed carried deliberately for farming | paddy, maize, vegetables |

::: example Worked reasoning: why paddy is transplanted
**Observation.** A farmer sows paddy seed thickly in one small nursery bed, and
after about three weeks pulls up the seedlings and plants them in the main field
with a gap between each.

**Reasoning.** (1) In a nursery the seeds can be watered, weeded and protected
from birds on a small area, which is cheaper than guarding the whole field.
(2) If the seedlings stayed crowded, they would compete for light, water and
minerals and most would die or stay small. Transplanting gives each plant its
own space, so each produces more grain. (3) Transplanting also lets the farmer
use the main field for another crop for those three weeks.

**Conclusion.** Transplanting is a way of giving each seedling the conditions
for germination first, and the space for growth afterwards — the same two
requirements, separated in time.
:::

## Chapter summary

- **Reproduction** keeps a species alive; it is asexual (one parent, no
  gametes) or sexual (two parents, gametes join).
- Asexual examples: binary fission (Amoeba), budding (yeast, Hydra),
  fragmentation (Spirogyra), spore formation (*Rhizopus*), vegetative
  propagation (potato, sugarcane, banana, *Bryophyllum*).
- Flower parts: sepals protect, petals attract, stamens make pollen, the carpel
  holds the ovules.
- **Pollination** is the transfer of pollen to the stigma; **fertilisation** is
  the joining of the male and female gametes inside the ovule.
- After fertilisation the ovule becomes the seed and the ovary becomes the
  fruit.
- External fertilisation (fish, frog) needs water and wastes many eggs; internal
  fertilisation (reptile, bird, mammal) protects the young.
- A seed has a coat, a food store (one or two cotyledons) and an embryo with
  plumule and radicle.
- Germination needs water, air and a suitable temperature; dispersal avoids
  competition between the seedling and its parent.

## Practice questions

**Group A — Objective (1 mark each)**

1. Binary fission is seen in <span class="marks">[1]</span>
   (a) Amoeba (b) Hydra (c) potato (d) maize
2. The male part of a flower is the <span class="marks">[1]</span>
   (a) sepal (b) petal (c) stamen (d) carpel
3. After fertilisation, the ovary of a flower becomes the
   <span class="marks">[1]</span>
   (a) seed (b) fruit (c) leaf (d) root
4. Transfer of pollen from the anther to the stigma is called
   <span class="marks">[1]</span>
   (a) fertilisation (b) germination (c) pollination (d) dispersal
5. Which is a dicotyledonous seed? <span class="marks">[1]</span>
   (a) maize (b) rice (c) bean (d) wheat
6. A seed will not germinate if it has no <span class="marks">[1]</span>
   (a) light (b) water and air (c) soil (d) fertiliser

::: note Answers to Group A
**1.** (a) — the parent cell divides into two.
**2.** (c) — the stamen is the male part.
**3.** (b) — the ovary becomes the fruit and the ovules inside become the seeds.
**4.** (c) — pollination is the transfer, fertilisation is the joining.
**5.** (c) — the bean has two cotyledons.
**6.** (b) — water and oxygen are the two that must be present; light is not
needed for germination.
:::

**Group B — Short answer (2 marks each)**

1. Give two differences between asexual and sexual reproduction.
   <span class="marks">[2]</span>
2. Write the function of the anther, the stigma, the petal and the sepal.
   <span class="marks">[2]</span>
3. What is vegetative propagation? Give two examples with the part used.
   <span class="marks">[2]</span>
4. Write the four conditions needed for the germination of a seed and say why
   the seed needs each. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Asexual reproduction needs only one parent and no gametes, and the young
one is nearly a copy of the parent; sexual reproduction needs two parents and
the joining of male and female gametes, and the young one is a mixture of both.
Asexual reproduction is faster and produces more young ones; sexual
reproduction produces far more variation.
**2.** Anther — produces and stores pollen grains. Stigma — receives the pollen
grain and lets it grow a tube. Petal — its colour and scent attract insects and
birds. Sepal — protects the flower while it is still a bud.
**3.** Vegetative propagation is the growth of a new plant from a part of the
parent plant without any seed or gamete. Potato — a tuber, which is a swollen
underground stem with buds ("eyes"). Sugarcane — a stem cutting with a node.
(Also acceptable: banana by sucker, ginger by rhizome, *Bryophyllum* by leaf,
onion by bulb.)
**4.** Water — softens the seed coat and lets the stored food dissolve. Air
(oxygen) — needed for respiration, which supplies energy for growth. Suitable
temperature — warmth speeds up the enzymes that break down the stored food.
(For most seeds, light is not needed for germination itself, though the seedling
needs it soon after.)
:::

**Group C — Long answer (4 marks each)**

1. Draw a labelled diagram of the vertical section of a flower and describe
   what happens from pollination to the formation of a fruit.
   <span class="marks">[4]</span>
2. What is meant by a monocotyledonous and a dicotyledonous seed? Draw a
   labelled diagram of a bean seed and explain what happens in the first week
   of its germination. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Diagram.** The vertical section must show the pedicel, sepals, petals,
stamens (anther and filament) and the carpel (stigma, style and ovary with
ovules inside), each with a labelled line. **From pollination to fruit.**
(i) Pollen from the anther lands on the stigma — pollination. It may arrive by
insect, wind or water. (ii) The pollen grain grows a tube down through the
style into the ovary. (iii) The male gamete travels down the tube and joins the
egg inside the ovule — fertilisation. (iv) The zygote develops into an embryo,
the ovule becomes the seed and the ovary swells and becomes the fruit, whose
wall protects the seeds and helps in their dispersal. (v) The petals, stamens
and sepals dry up and fall off.
**2.** A **monocotyledonous** seed has a single cotyledon (one seed leaf) — maize
and rice. A **dicotyledonous** seed has two cotyledons — bean and pea.
**Diagram.** The bean seed must show the seed coat, the two cotyledons, the
embryo with plumule and radicle, and the micropyle. **First week.** The seed
absorbs water and swells; the seed coat splits; the enzymes become active and
break down the stored food in the cotyledons; the radicle emerges first and
grows downwards to absorb water and anchor the seedling; then the plumule grows
upwards, carrying the two cotyledons above the ground; the cotyledons shrivel
as their food is used; the first green leaves open and photosynthesis begins, so
the seedling now makes its own food.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The raw materials of photosynthesis are
   (a) glucose and oxygen (b) carbon dioxide and water (c) oxygen and water (d) glucose and carbon dioxide
**2.** Most absorption of digested food takes place in the
   (a) stomach (b) small intestine (c) large intestine (d) oesophagus
**3.** Bile is produced by the
   (a) pancreas (b) liver (c) gall bladder (d) stomach
**4.** Anaerobic respiration in yeast produces carbon dioxide and
   (a) lactic acid (b) ethanol (c) glucose (d) water only
**5.** Transpiration takes place mainly through
   (a) lenticels (b) stomata (c) roots (d) veins

::: note Objective practice — answers
**1.** (b) — glucose and oxygen are the products. **2.** (b) — the villi of the small intestine. **3.** (b) — the liver makes it; the gall bladder stores it. **4.** (b) — ethanol (fermentation). **5.** (b) — stomata.
:::

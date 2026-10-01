---
subject: Science and Technology
grade: 10
unit: 3
title: Honey Bee
hours: 0
area: Science and Technology
---

A honey bee colony works like a small, well-run town. One queen lays the eggs, thousands of workers collect food, build the nest and guard the door, and a few males wait to mate. Bees give us honey, wax and royal jelly, and, more important, they pollinate our crops: apple, mustard, buckwheat, cucumber and many more depend on them. Bee keeping is also a low-cost source of income for many farmers in the hills and the terai of Nepal. In this unit you learn the types of bees, their life cycle, how the colony is organised, and how bees are kept and their products used.

::: key What the SEE paper expects from this unit
Typical questions: name the types of honey bees (1 mark); the members of a colony and their functions (2 or 4 marks); the life cycle of the honey bee with a diagram (4 marks); the products of bees and their uses (2 marks); the equipment and care in bee keeping (2 or 4 marks). Learn the number of days in each stage.
:::

## 3.1 Types of bees

Honey bees belong to the genus *Apis*, in the phylum **Arthropoda**, class **Insecta**, order **Hymenoptera** (the order of bees, wasps and ants). The body of a bee has three parts: the **head** (with a pair of compound eyes, three simple eyes, a pair of antennae and mouth parts for chewing and sucking), the **thorax** (with three pairs of legs and two pairs of wings) and the **abdomen** (with the wax glands, the sting in the female workers and the digestive and reproductive organs).

### Species of honey bee

Four species of *Apis* are important in Nepal.

| Species | Common name | Nest | Habit | Remarks |
|---|---|---|---|---|
| *Apis dorsata* | Giant rock bee ("Bhir mauri") | One huge open comb hung from a cliff or branch | Wild, migratory, fierce | Cannot be kept in a box; large honey yield (30–40 kg per comb) |
| *Apis laboriosa* | Himalayan cliff bee | One huge comb on high cliffs, 1,200–4,000 m | Wild | Largest honey bee in the world; the cliff honey of Lamjung, Kaski and Dolakha |
| *Apis cerana* | Eastern (Asian) hive bee ("Mauri") | Several parallel combs in a dark cavity | Domesticated in hives | Native of Nepal; gentle; yield 5–15 kg per hive per year |
| *Apis florea* | Little (dwarf) bee | Single small comb on a bush branch | Wild | Smallest; yield 0.5–1 kg |
| *Apis mellifera* | European (Italian) bee | Several combs in cavity | Domesticated | Introduced to Nepal; yield 25–40 kg per hive per year; more aggressive |

Besides these, there are **stingless bees** (*Trigona*) that make small amounts of honey and cannot sting.

::: tip In the exam
Only *Apis cerana* and *Apis mellifera* are kept in boxes (domesticated hive bees). *A. dorsata*, *A. laboriosa* and *A. florea* are wild.
:::

### Castes (members) of a colony

A colony has three kinds of individuals, called **castes**: the queen, the workers and the drones.

| Feature | Queen | Worker | Drone |
|---|---|---|---|
| Sex | Fertile female | Sterile female | Male |
| Number in a colony | 1 | 20,000–60,000 | 100–500 or more (in season) |
| Size | Longest abdomen | Smallest | Largest body, stout |
| Sting | Present (rarely used) | Present | Absent |
| Origin | Fertilised egg fed on royal jelly | Fertilised egg fed on bee-bread | Unfertilised egg |
| Life span | 2–5 years | 6 weeks (summer), up to 6 months (winter) | About 2–3 months |
| Main job | Lays eggs | All the work of the colony | Mates with the queen |

```photo id="sci10/bee-worker" caption="The queen (marked with a red dot) among her workers. The queen is longer than the workers and is the only egg-laying female." width="66"
```

## 3.2 Life cycle

The honey bee shows **complete metamorphosis**: **egg → larva → pupa → adult**. The four stages look entirely different.

### Mating

A young virgin queen leaves the hive on a **nuptial flight** high in the air and mates with several drones (often 10–20). The drones die after mating. The queen stores the sperm in a small sac, the **spermatheca**, and uses it for the rest of her life, often for two to three years or more. She returns and begins to lay eggs.

### Stages

1. **Egg.** The queen lays one egg in each cell of the comb, standing upright, small, white and about 1.5 mm long. It hatches after **3 days**.
2. **Larva.** A white, legless, worm-like grub comes out. It is fed by nurse workers and grows rapidly, shedding its skin several times. All larvae first get royal jelly for 2–3 days; worker and drone larvae then get bee-bread (pollen and honey); the queen larva keeps getting royal jelly.
3. **Pupa.** When fully grown, the larva is sealed in its cell by a wax capping. Inside, it changes into a pupa and the adult organs (legs, wings, eyes) form. It does not feed.
4. **Adult.** The adult bites open the capping and comes out.

| Caste | Egg | Larva | Pupa | Total (egg → adult) |
|---|---|---|---|---|
| Queen | 3 days | 5½ days | 7½ days | **16 days** |
| Worker | 3 days | 6 days | 12 days | **21 days** |
| Drone | 3 days | 6½ days | 14½ days | **24 days** |

::: memory 16 – 21 – 24
Queen 16, Worker 21, Drone 24: the order of days is Queen, Worker, Drone. The queen is the quickest to develop; the drone the slowest.
:::

```figure caption="Days taken in each stage of development of the queen, the worker and the drone."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.6))
castes=["Queen","Worker","Drone"]
egg=[3,3,3]; lar=[5.5,6,6.5]; pup=[7.5,12,14.5]
y=np.arange(3)
ax.barh(y,egg,color=SERIES[0],label="Egg")
ax.barh(y,lar,left=egg,color=SERIES[1],label="Larva")
ax.barh(y,pup,left=np.array(egg)+np.array(lar),color=SERIES[2],label="Pupa")
for i,t in enumerate([16,21,24]):
    ax.text(t+0.4,i,str(t)+" days",va='center',fontsize=8,color=INK)
ax.set_yticks(y); ax.set_yticklabels(castes); ax.invert_yaxis()
ax.set_xlim(0,29); ax.set_xlabel("Days from egg laid", color=INK)
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower right',ncol=3,fontsize=7.5,bbox_to_anchor=(1.0,-0.45))
```

::: example Worked example 3.1 (date of emergence)
**Problem.** A queen lays an egg in a worker cell on 1 April and in a drone cell on the same day. On which dates will the worker and the drone emerge as adults? (April has 30 days.)

**Solution.** Worker: egg to adult = 21 days. 1 April + 21 days = **22 April**.

Drone: egg to adult = 24 days. 1 April + 24 days = **25 April**.

If the same egg had been placed in a queen cell, the queen would emerge on 1 + 16 = **17 April**.
:::

### Parthenogenesis and caste determination

- The queen can lay both **fertilised** and **unfertilised** eggs.
- A **fertilised egg** (with a set of chromosomes from both parents, 32 in all) can become a worker or a queen. A larva that is fed **royal jelly** for its whole larval life, in a large queen cell, develops into a queen. A larva fed royal jelly only for 2–3 days, and then bee-bread, becomes a worker.
- An **unfertilised egg** (16 chromosomes) develops into a **drone**. Development of an egg without fertilisation is called **parthenogenesis**.

So the difference between queen and worker is only a matter of feeding, not of heredity.

```photo id="sci10/drone-pupae" caption="Developing honey bees taken from their cells: larvae (white, left) and pupae (right) show the stages between egg and adult." width="76"
```

## 3.3 Colony and division of labour

A **colony** is the whole family of bees living together in one nest. Wild bees build their combs in the open or in cavities; domesticated bees live in hives.

### The comb

The **comb** is a wall of wax cells, built by the workers from the wax secreted by the glands under their abdomen. Cells are **hexagonal** (six-sided) and back-to-back on both faces of the comb. A hexagon uses the least wax for the most storage space and leaves no gaps. Cells are of different kinds:

| Cell | Use |
|---|---|
| Worker cells (small) | Rearing workers; storing honey and pollen |
| Drone cells (larger) | Rearing drones |
| Queen cells (peanut-shaped, hang down) | Rearing new queens |
| Honey cells (at the top) | Honey storage, sealed with wax when ripe |

The centre of the comb is the **brood area**, where eggs, larvae and pupae lie; pollen is stored in a ring around it, and honey at the top and edges.

```photo id="sci10/bee-brood" caption="A frame of comb. The pale capped cells in the middle hold developing brood; workers crowd over the comb." width="90"
```

### Division of labour

In a colony the work is shared among the castes, and a worker changes her job as she ages. This is called **division of labour**; it makes the colony efficient.

**The queen** is the only fully developed female. She is the mother of all bees in the hive and lays **1,000–2,000 eggs a day** in the busy season. She releases a chemical called **queen substance (pheromone)** that keeps the colony together and stops the workers from developing ovaries. If the queen dies, the workers feed some larvae with royal jelly to make a new one.

**The drones** are the males. They do no work for the colony; they mate with a virgin queen, and die as they do so. In autumn or when food is short, the workers drive the remaining drones out of the hive to starve.

**The workers** are sterile females. They do all the work, in the order of their age:

| Age of worker (days) | Job |
|---|---|
| 1–3 | **Cleaner**: clean cells, remove dirt |
| 3–10 | **Nurse**: feed larvae with royal jelly and bee-bread; feed the queen |
| 10–18 | **House bee**: build comb with wax, store pollen and nectar, ripen honey by fanning, receive food from foragers |
| 18–21 | **Guard**: stand at the entrance and drive away enemies (wasps, robber bees) |
| After 21 | **Forager**: fly out to collect nectar, pollen, water and propolis |

### Communication: bee dances

When a forager finds a good source of nectar, she returns and tells the others by dancing on the comb, as shown by **Karl von Frisch** (Nobel Prize 1973).

- **Round dance:** the bee runs in small circles. It tells that food is near (within about 50–100 m); it gives no direction.
- **Waggle dance:** the bee runs in a straight line, waggling her abdomen, then turns in a half circle and repeats. The angle of the straight run with the vertical shows the direction of the food relative to the sun, and the length of the run shows how far away it is.

### Swarming and absconding

When a colony becomes too crowded, the old queen with about half of the workers leaves the hive and clusters on a branch; this is **swarming**. It is the natural way in which a new colony starts. Beekeepers catch the swarm in a box. **Absconding** means the whole colony leaves the nest, due to shortage of food, disease, smoke, ants or wax moths.

::: example Worked example 3.2 (queen's egg laying)
**Problem.** In the spring a queen lays 1,200 eggs per day. How many eggs does she lay in the 30 days of April? Of these, 5% do not hatch. How many larvae hatch?

**Solution.** Eggs laid = 1,200 × 30 = 36,000.

Eggs that do not hatch = 5% of 36,000 = 1,800.

Larvae that hatch = 36,000 − 1,800 = **34,200**.
:::

::: example Worked example 3.3 (worker strength)
**Problem.** A hive contains 24,000 workers. The nurse bees, house bees and guards together make up 60% of them and the rest are foragers. If each forager makes 10 trips a day and carries 30 mg of nectar per trip, find the mass of nectar brought home in one day.

**Solution.** Foragers = 40% of 24,000 = 9,600.

Nectar per forager per day = 10 × 30 mg = 300 mg.

Total nectar = 9,600 × 300 mg = 2,880,000 mg = 2,880 g = **2.88 kg**.

(Nectar is mostly water; about 4–5 kg of nectar is needed to make 1 kg of honey, so this colony can make roughly 0.6 kg of honey a day in a good flow.)
:::

::: caution Common mistake
The queen does not "rule" or give orders to the colony; she is the egg-layer. Also, drones have no sting and do not collect food. Do not write that workers are males; all workers are sterile females.
:::

## 3.4 Bee keeping and products

**Bee keeping (apiculture)** is the care and management of honey bees in artificial hives to get honey and other products. A place with many hives is an **apiary**.

### Why keep bees?

- It gives honey, wax and other valuable products.
- Bees **pollinate** flowers, which raises the yield of crops; some farmers keep hives in orchards and mustard fields for this reason.
- It needs little land, little money and little time, and is good work for women, youth and landless families.
- It does not harm the environment.

### Requirements

| Item | Use |
|---|---|
| **Hive box** (movable-frame hive, e.g. Langstroth or Newton type) | The home of the colony; has a bottom board, brood chamber, super (honey chamber), inner cover and roof |
| **Frames** with wax foundation sheet | Bees build combs on them; they can be lifted out without harming the combs |
| **Queen excluder** | A grid between the brood chamber and super; workers pass through but the larger queen cannot, so the honey is free of brood |
| **Smoker** | Gives cool smoke that calms the bees |
| **Bee veil, gloves, apron** | Protect from stings |
| **Hive tool** | For prising apart frames and scraping wax |
| **Bee brush** | To sweep bees off combs |
| **Honey extractor** | A drum that spins the frame; centrifugal force throws out honey without breaking the comb |
| **Uncapping knife** | To cut off the wax caps of the honey cells |

### Management

1. **Site:** a dry, sunny, quiet place near flowers and clean water, protected from strong wind, with the entrance facing east or south-east.
2. **Starting a colony:** catch a swarm or buy a colony of *Apis cerana* or *Apis mellifera*.
3. **Inspection:** open the hive once a week in the morning, gently; check the queen, brood, food, disease.
4. **Feeding:** give sugar syrup (1 : 1 sugar and water) in the lean season when there are no flowers.
5. **Control of pests and diseases:** pests include wax moth, wasps, ants and mites (*Varroa*); diseases include foulbrood and Thai sacbrood virus. Keep hives clean and strong, remove old combs and reduce the entrance in the lean season.
6. **Swarm control:** give more space (extra super), or remove queen cells.
7. **Migration:** move hives to places where flowers are in bloom (for example, mustard in the terai in winter, and hill flowers in spring and summer).
8. **Harvest:** take the honey from sealed combs only, in the flow season, leaving enough for the bees.

```photo id="sci10/beekeeper" caption="A beekeeper lifting a frame out of a hive to inspect the comb." width="76"
```

### Products of bee keeping

| Product | What it is | Uses |
|---|---|---|
| **Honey** | Nectar changed by bees with enzymes and ripened by fanning off water | Food and energy, medicine for cough and sore throat, wound healing, sweetener |
| **Beeswax** | Secreted by worker's wax glands | Candles, polish, cosmetics, ointments, comb foundation |
| **Royal jelly** | A milky protein-rich secretion of nurse bees' glands | Food of queen; health tonic and cosmetics |
| **Propolis** (bee glue) | Resin collected from tree buds | Used by bees to seal cracks; antiseptic medicine |
| **Pollen** | Collected from flowers; "bee bread" | Protein food for the colony; health food |
| **Bee venom** | Poison from the sting | Medicine for arthritis (used under expert control) |

**Honey** is about 80% sugar (mainly fructose and glucose) and 17–18% water, plus small amounts of enzymes, minerals and vitamins. Good honey has a moisture below 20%, does not ferment and does not spoil because its high sugar content stops microbes from growing.

::: example Worked example 3.4 (income from bee keeping)
**Problem.** A farmer keeps 20 hives of *Apis cerana*, each producing 12 kg of honey a year. The honey is sold at Rs 900 per kg. The yearly cost of the apiary (feeding, equipment wear, labour and transport) is Rs 60,000. Find the farmer's yearly profit and profit percentage.

**Solution.** Total honey = 20 × 12 = 240 kg.

Income = 240 × 900 = Rs 2,16,000.

Profit = 2,16,000 − 60,000 = **Rs 1,56,000**.

Profit % = (profit / cost) × 100 = (1,56,000 / 60,000) × 100 = **260%**.
:::

### Honey hunting and conservation

In the hills of Nepal, the Gurung and Rai people traditionally collect honey of the cliff bee (*Apis laboriosa*) by climbing rope ladders. This is dangerous and, done carelessly, destroys the colony. Sustainable honey hunting, where the brood part of the comb is left, protects the bees. Pesticides and loss of flowering plants are the main threats to bees everywhere, so we should plant flowers, avoid spraying during flowering, and protect natural habitats.

## Chapter summary

- Honey bees belong to genus *Apis*, class Insecta, order Hymenoptera. Wild species: *A. dorsata*, *A. laboriosa*, *A. florea*; domesticated: *A. cerana*, *A. mellifera*.
- The colony has three castes: one queen (fertile female), thousands of workers (sterile females) and drones (males).
- Life cycle: egg → larva → pupa → adult (complete metamorphosis). Egg-to-adult time: queen 16 days, worker 21 days, drone 24 days.
- Fertilised eggs give queens and workers (diet decides which); unfertilised eggs give drones (parthenogenesis).
- Division of labour among workers by age: cleaner, nurse, house bee (comb builder), guard, forager. Bees communicate by round and waggle dances.
- The comb is made of hexagonal wax cells; the brood is at the centre, pollen around it and honey above.
- Bee-keeping tools: movable-frame hive, queen excluder, smoker, veil, hive tool, honey extractor.
- Products: honey, beeswax, royal jelly, propolis, pollen and bee venom. Bees also pollinate crops.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. Which honey bee species is domesticated in Nepal? <span class="marks">[1]</span>
   (a) *Apis dorsata* (b) *Apis florea* (c) *Apis cerana* (d) *Apis laboriosa*
2. A worker bee develops from egg to adult in <span class="marks">[1]</span>
   (a) 16 days (b) 21 days (c) 24 days (d) 30 days
3. Drones develop from <span class="marks">[1]</span>
   (a) fertilised eggs (b) unfertilised eggs (c) pupae of workers (d) larvae fed royal jelly
4. The device that stops the queen entering the honey chamber is the <span class="marks">[1]</span>
   (a) smoker (b) queen excluder (c) extractor (d) hive tool
5. The shape of the cells in a honey comb is <span class="marks">[1]</span>
   (a) circular (b) square (c) hexagonal (d) triangular
6. The food that makes a larva grow into a queen is <span class="marks">[1]</span>
   (a) honey (b) bee-bread (c) royal jelly (d) propolis

::: note Answers to Group A
**1.** (c) — *Apis cerana* (and *A. mellifera*, introduced) are kept in hives.
**2.** (b) — workers take 21 days.
**3.** (b) — drones are haploid, from unfertilised eggs.
**4.** (b) — the queen is too large to pass the excluder.
**5.** (c) — hexagons need the least wax and leave no gaps.
**6.** (c) — royal jelly throughout the larval stage makes a queen.
:::

**Group B — Short answer (2 marks each)**

1. Name the three castes of honey bees. <span class="marks">[2]</span>
2. What is the function of the queen in the colony? <span class="marks">[2]</span>
3. What is the difference between swarming and absconding? <span class="marks">[2]</span>
4. Give any four uses of honey bee products. <span class="marks">[2]</span>
5. Why are the cells of the comb hexagonal? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Queen, workers and drones.
**2.** The queen lays eggs (1,000–2,000 per day) to keep up the population; she also releases pheromone that holds the colony together.
**3.** In swarming, the old queen and part of the workers leave to form a new colony because the hive is crowded. In absconding, the whole colony leaves the hive because of shortage of food, pests or disturbance.
**4.** Honey as food and medicine; beeswax for candles and cosmetics; royal jelly as a tonic; propolis as an antiseptic; pollination of crops.
**5.** A hexagon fits with others without a gap and gives the largest storage space for the least wax.
:::

**Group C — Long answer (4 marks each)**

1. Describe the life cycle of the honey bee with a labelled diagram. <span class="marks">[4]</span>
2. Explain the division of labour among the members of a bee colony. <span class="marks">[4]</span>
3. A queen lays 1,500 eggs a day for 20 days; 4% of the eggs fail to hatch. How many larvae hatch? On what date would a worker emerge from an egg laid on 10 May? <span class="marks">[4]</span>
4. Write the equipment required for modern bee keeping and mention how bee keeping benefits farmers. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Egg (3 days, laid by the queen in a cell) → larva (6 days, fed by nurse bees) → pupa (12 days, sealed in wax) → adult worker (emerges on the 21st day). The diagram shows the four stages in a cycle with the days. The queen takes 16 days and the drone 24 days.
**2.** The queen lays eggs; drones mate with the queen; workers do all the other work, by age: cleaning, nursing, comb building and honey storing, guarding the entrance, and foraging for nectar, pollen and water. Division of labour gives an efficient colony.
**3.** Eggs = 1,500 × 20 = 30,000. Failed = 4% × 30,000 = 1,200. Hatched = 28,800. Worker emerges 21 days after 10 May = 31 May.
**4.** Movable-frame hive with frames and foundation, queen excluder, smoker, veil and gloves, hive tool, bee brush, uncapping knife and honey extractor. Benefits: income from honey, wax and other products; higher crop yield from pollination; low cost, small space; suitable for women and landless people.
:::

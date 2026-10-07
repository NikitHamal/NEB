---
subject: Science and Technology
grade: 8
unit: 4
title: Biodiversity and Environment
hours: 0
area: Science and Technology
---

A forest, riverbank, grassland or garden is home to many kinds of life. The variety of living things in a place is called **biodiversity**. Plants, animals, fungi and tiny organisms are connected to one another and to the non-living environment—air, water, soil, light and temperature. These connections provide food and shelter, recycle materials and help ecosystems recover from change. People depend on healthy ecosystems, so understanding local biodiversity is also a way to care for our communities.

::: key Follow the flow of energy
Green plants capture energy from sunlight. Animals get energy by eating plants or other animals, and decomposers break down dead material. In a food-chain arrow, point **from the food to the organism that eats it**. नेपालीमा: **ऊर्जाको दिशा देखाउन तीर खानाबाट खाने जीवतर्फ कोर्नुहोस्।**
:::

## 4.1 Biodiversity and habitats

**Biodiversity** means the variety of living things. We can notice differences among species (a rhododendron, a butterfly and a bird are different species), among individuals of one species, and among habitats such as forests, wetlands and mountain grasslands. A **habitat** is the place where an organism lives and finds the conditions it needs.

Each organism has needs: food, water, shelter, space and suitable conditions. A **population** is a group of the same species living in an area; a **community** is all the populations living and interacting there. The **ecosystem** includes the community and the non-living parts of its surroundings. These terms describe different levels, so do not use “habitat,” “community” and “ecosystem” as if they mean the same thing.

Nepal's different heights, climates and landforms support many habitats. A species suited to a cool mountain forest may not thrive in a hot lowland. An organism's **adaptations**—such as body shape, behaviour or timing of activity—help it survive in its own conditions. A snow leopard's thick fur helps in cold mountain environments; a fish's gills take oxygen from water. Adaptations develop over generations; an individual animal does not grow a new feature simply because it needs one.

```photo id="sci10/rhino" caption="The greater one-horned rhinoceros is a large herbivore protected in parts of Nepal. Habitat protection benefits many other species that share the same landscape." width="76"
```

## 4.2 Food chains, food webs and balance

A **producer** makes its own food, usually by photosynthesis. Green plants and algae are producers. A **consumer** gets food by eating other organisms. A **decomposer**, such as many fungi and bacteria, breaks down dead material and returns nutrients to the environment.

A food chain shows one route by which energy moves. For example:

**grass → grasshopper → frog → snake**

The arrow starts at the food and points to the eater. A frog does not pass energy to the grasshopper; it receives energy by eating it. In real habitats, most animals eat more than one kind of food, so chains connect to make a **food web**.

```figure caption="A simplified food web. Arrows point from food to eater; several routes connect plants, insects and animals."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.1))
ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
points={"Grass":(1.2,4.7),"Seeds":(1.2,1.4),"Grasshopper":(3.7,5.9),"Mouse":(3.7,3.4),"Bird":(3.7,0.9),"Frog":(6.2,5.9),"Snake":(6.2,3.4),"Owl":(6.2,0.9),"Hawk":(8.9,3.4)}
edges=[((1.65,4.75),(3.08,5.82)),((1.65,4.5),(3.08,3.45)),((1.65,1.65),(3.08,3.35)),((1.65,1.4),(3.08,0.95)),((4.35,5.9),(5.58,5.9)),((4.35,3.4),(5.58,3.4)),((4.15,3.0),(5.72,1.3)),((6.2,5.45),(6.2,3.85)),((4.25,1.1),(8.28,3.2)),((6.85,3.4),(8.28,3.4))]
for a,b in edges:
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=MUTED,lw=0.85,shrinkA=0,shrinkB=0))
for label,(x,y) in points.items():
    color="#e8f3df" if label in ("Grass","Seeds") else "#eef3fb"
    ax.text(x,y,label,ha="center",va="center",fontsize=7.5,color=INK,
            bbox=dict(boxstyle="round,pad=0.32",fc=color,ec=ACCENT if color=="#eef3fb" else SERIES[2],lw=0.9))
fig.tight_layout()
```

A change in one population can affect others. If a pesticide harms many insects, insect-eating birds may have less food. If a predator disappears, the animals it hunted may increase and consume more plants. Ecosystems can change naturally, but rapid changes caused by pollution, habitat loss or over-hunting can make it difficult for species to survive.

::: example Read a food-chain arrow
**Problem.** In the chain rice plant → mouse → owl, what does the arrow from mouse to owl mean? What might happen if many mice are removed?

**Solution.** The arrow means that the owl can obtain food and energy by eating the mouse. If many mice are removed, owls may have less food and their numbers or breeding success could fall. The rice plant may face less feeding by mice. Other food sources and conditions also matter, so these are possible effects, not a guaranteed result.
:::

## 4.3 How people depend on ecosystems

Ecosystems provide useful **services**. Forests help hold soil and slow surface runoff; wetlands store water and provide habitat; insects pollinate many crops; decomposers return nutrients; plants provide food, fibre, medicine and shade. These benefits can be easy to overlook until a habitat is damaged.

A river is an ecosystem with flowing water, plants, fish, insects, microorganisms and the land around it. Dumping rubbish or untreated wastewater can harm aquatic life and people who rely on the water. Burning mixed waste releases smoke and can leave toxic material behind. Good waste management starts by reducing unnecessary waste, reusing safe items, sorting recyclable material and disposing of hazardous waste correctly.

```photo id="sci10/bagmati-waste" caption="Rubbish beside the Bagmati River illustrates how waste can damage a shared habitat. Preventing litter and managing wastewater protect both wildlife and people." width="78"
```

::: caution Pollution does not stay in one place
A plastic bag thrown beside a road can block a drain, travel downstream and reach a river. Smoke can move with the wind. Prevent pollution at its source rather than assuming it affects only the place where it began.
:::

## 4.4 Threats and conservation

**Conservation** is the wise protection and use of nature so that species and habitats can continue into the future. Major threats include:

- **Habitat loss and fragmentation:** forests or wetlands are cleared, or a continuous habitat is divided by roads and buildings.
- **Pollution:** harmful substances enter air, water or soil.
- **Overuse:** organisms are hunted, collected or harvested faster than populations recover.
- **Invasive species:** an introduced organism spreads and harms native species or habitats.
- **Climate change:** long-term shifts in temperature and rainfall change the conditions organisms depend on.

Conservation can include protecting habitats, planting native species, preventing illegal hunting, reducing waste, restoring damaged land and using resources carefully. Local knowledge matters: residents can identify seasonal changes and places where wildlife lives. A school project can map trees or birds without disturbing nests, removing plants or sharing the location of a rare species publicly.

::: example Plan a safe biodiversity survey
**Problem.** A class wants to compare the number of kinds of plants in a school garden and a nearby paved area. Give a fair, safe method.

**Solution.** Mark equal-sized sample areas in each place and observe them for the same length of time. Record each plant kind seen, using a guide or teacher's help to identify it; do not pull plants out. Repeat the survey at several spots and at a similar time of day. The class can compare the number of kinds observed, while noting that a short survey may miss plants hidden or out of season.
:::

## 4.5 Take action without harming nature

Small actions are most useful when they address a real local problem. Keep waste out of drains, separate recyclable items where collection exists, save water, plant suitable native species and avoid disturbing wildlife. Before sharing a conservation claim online, check the source and date. Do not handle an unknown animal, touch a nest or drink water from a stream because it looks clean.

A simple observation log can make a local issue visible: record date, place, weather, what was seen and how many times. Use the same method on each visit. A rise in bird sightings may relate to season, food or observation time; a log records a pattern but does not by itself prove its cause. Share results with the school or local environment group so that others can check and act on them.

::: example Choose a conservation response
**Problem.** Students find plastic wrappers beside a small stream near school. Name two actions that reduce harm and one observation that would help them evaluate the result.

**Solution.** They can first inform a teacher or local authority and organise safe litter prevention or a supervised clean-up using gloves and proper disposal. They can also place clear waste bins at suitable points and ask the community to use them. Record the number of wrappers in the same marked area each week; compare counts after the action. Do not enter deep or fast water or handle sharp or medical waste.
:::

## Chapter summary

- Biodiversity is the variety of living things. A habitat is where an organism lives; an ecosystem includes the community and its non-living surroundings.
- Producers, consumers and decomposers connect through food chains and food webs; arrows point from food to eater.
- Ecosystems support people through food, clean water, soil protection, pollination and other services.
- Habitat loss, pollution, overuse, invasive species and climate change threaten biodiversity.
- Conservation protects habitats and uses resources responsibly. Observe safely, record evidence and avoid disturbing wildlife.

## Practice questions

1. What is a habitat? (a) a group of different ecosystems (b) the place where an organism lives (c) a food chain (d) a non-living object
2. In a food-chain arrow, which direction does the arrow point?
3. Name one producer and one decomposer.
4. Give one way pollution can travel from land to a river.

::: note Answers to questions 1–4
**1.** (b) — a habitat is the place where an organism lives and finds suitable conditions.
**2.** From the food organism to the organism that eats it.
**3.** Producer: green plant or algae. Decomposer: many fungi or bacteria.
**4.** Rain can wash litter or chemicals into drains and carry them downstream.
:::

5. Make a food chain using grass, grasshopper, frog and snake. Explain what the arrows mean.
6. Distinguish population, community and ecosystem.
7. State two threats to biodiversity and one practical response to either threat.
8. Suggest a safe method for observing birds near a school without disturbing them.

::: note Answers to questions 5–8
**5.** Grass → grasshopper → frog → snake. Each arrow points from food to eater and shows one route of energy transfer.
**6.** A population is one species in an area; a community is the interacting populations; an ecosystem includes the community and non-living surroundings.
**7.** Examples: habitat loss—protect or restore native habitat; pollution—prevent waste entering water; overuse—enforce sustainable harvesting; invasive species—seek local expert advice before removal.
**8.** Observe from a distance at a fixed time and place, record sightings without approaching nests or feeding birds, and repeat under similar conditions.
:::

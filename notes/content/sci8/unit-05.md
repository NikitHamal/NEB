---
subject: Science and Technology
grade: 8
unit: 5
title: Life Process
hours: 0
area: Science and Technology
---

Living organisms need materials and energy to grow, repair their bodies and respond to their surroundings. Nutrition, respiration, transport and excretion are connected processes, not separate tricks. Plants and animals carry out these life processes in different ways, while growth, reproduction and response help living things continue through changing conditions.

::: key Respiration is not the same as breathing
Breathing moves air into and out of the lungs. **Cellular respiration** releases usable energy from food inside cells. Oxygen is needed for aerobic respiration, but not all respiration uses oxygen; breathing and respiration are different processes.
:::

## 5.1 Nutrition, respiration, transport and excretion

**Nutrition** is obtaining and using food. Green plants make glucose by photosynthesis using light, water and carbon dioxide; oxygen is released. Animals obtain food by eating plants or other animals and digest it into substances that can be absorbed. A balanced diet includes suitable amounts of energy-giving foods, body-building foods, protective foods, water and fibre. Needs vary with age, activity and health, so one menu is not ideal for everyone.

**Respiration** releases energy from glucose. In many cells, aerobic respiration uses oxygen and produces carbon dioxide and water. The lungs bring oxygen into the body and remove much of the carbon dioxide, but respiration itself happens in cells. During activity, breathing and pulse rate may rise because working muscles need more oxygen and faster transport of materials.

The **transport system** moves materials to where they are needed. In humans, blood transports oxygen, digested nutrients and waste around the body; the heart pumps it through blood vessels. In plants, xylem carries water and minerals from roots toward leaves, while phloem moves dissolved food from sources such as leaves to other parts. **Excretion** removes metabolic wastes made by the body. In humans, kidneys help remove urea and excess water in urine; lungs remove carbon dioxide. Egestion of undigested food is different from excretion.

```figure caption="Food and oxygen enter the blood and reach cells; kidneys remove some wastes from the blood."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
labels=[("Food",(0.35,4.1)),("Digestion",(2.75,4.1)),("Blood",(5.2,4.1)),("Cells",(7.7,4.1)),("Lungs",(2.75,1.0)),("Kidneys",(6.0,1.0))]
for label,(x,y) in labels:
    ax.add_patch(FancyBboxPatch((x,y),1.9,0.9,boxstyle="round,pad=0.06",fc="#eef5e8",ec=SERIES[2],lw=1.0))
    ax.text(x+0.95,y+0.45,label,ha="center",va="center",fontsize=7.5,color=INK)
for a,b in [((2.3,4.55),(2.65,4.55)),((4.7,4.55),(5.1,4.55)),((7.15,4.55),(7.65,4.55))]:
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.0))
ax.annotate("",xy=(5.45,4.0),xytext=(4.05,1.95),arrowprops=dict(arrowstyle="->",color=SERIES[4],lw=1.0,connectionstyle="arc3,rad=-0.12"))
ax.text(4.15,3.05,"oxygen to blood",ha="center",fontsize=6.8,color=SERIES[4])
ax.annotate("",xy=(6.95,1.95),xytext=(8.65,4.0),arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.0,connectionstyle="arc3,rad=-0.12"))
ax.text(8.5,2.9,"wastes",ha="center",fontsize=6.8,color=MUTED)
fig.tight_layout()
```

::: example Calculate a simple pulse rate
**Problem.** A student's pulse is counted as 18 beats in 15 seconds after resting. What is the rate in beats per minute?

**Solution.** One minute has 60 seconds, which is four groups of 15 seconds. Rate = $18 \times 4 = 72$ beats per minute. This is a classroom calculation, not a medical diagnosis; pulse varies among people and with activity.
:::

## 5.2 Growth, reproduction and response

**Growth** is a lasting increase in size or dry mass as an organism develops. It results from cells increasing in number or size and from materials being built into the body. **Reproduction** produces new individuals of the same kind. It may be sexual, involving reproductive cells from two parents, or asexual, involving one parent and no fusion of reproductive cells. Reproduction is important to the continuation of a species, but an individual does not need to reproduce to be alive.

A **stimulus** is a change that can be detected; a **response** is the reaction. Animals may move away from a loud sound or toward food. Plants respond too: a shoot generally grows toward light, and roots tend to grow downward and toward water. These responses develop over time and should be distinguished from a plant making a quick voluntary movement.

In flowering plants, pollen must reach a stigma for fertilisation to occur; after fertilisation, a seed develops from the ovule. Seeds can be dispersed by wind, water, animals or other means. In animals, reproduction and development vary widely, but young organisms need suitable conditions to survive.

```figure caption="A young plant's shoot can grow toward light while roots grow into the soil."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(4.5, 3.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")
ax.add_patch(Rectangle((0.5,3.0),9.0,0.45,fc="#9b6a42",ec="none",alpha=0.45))
ax.plot([5,5],[1.2,4.2],color=SERIES[2],lw=2.2)
ax.plot([5,5.5,5.7],[3.4,2.3,1.0],color="#8b6d50",lw=1.4)
ax.plot([5,4.5,4.2],[3.4,2.4,1.2],color="#8b6d50",lw=1.4)
ax.add_patch(FancyArrowPatch((1.2,6.9),(4.2,6.9),arrowstyle="->",mutation_scale=12,color=ACCENT,lw=1.5))
ax.text(1.1,7.25,"light",fontsize=8,color=ACCENT)
ax.annotate("shoot",xy=(5.1,4.0),xytext=(6.6,5.0),fontsize=8,color=INK,arrowprops=dict(arrowstyle="->",color=MUTED))
ax.annotate("roots",xy=(5.0,1.4),xytext=(6.6,1.2),fontsize=8,color=INK,arrowprops=dict(arrowstyle="->",color=MUTED))
ax.text(2.0,2.5,"soil",fontsize=8,color=MUTED)
fig.tight_layout()
```

::: example Follow food through the body
**Problem.** A student eats rice. Describe one route by which its digested nutrient can reach a leg muscle and be used.

**Solution.** Digestion breaks starch into glucose, which is absorbed through the small intestine into the blood. The heart pumps blood through vessels to the leg muscle. Muscle cells take in glucose and oxygen; cellular respiration releases usable energy. The blood also carries some wastes away. The exact route passes through many vessels, so this is a simplified description.
:::

::: example Interpret a plant response
**Problem.** A potted seedling near a window bends toward the light. Name the stimulus and response, and suggest a fair observation.

**Solution.** The light direction is the stimulus; the shoot's change in growth direction is the response. A class can place similar seedlings in the same soil and water conditions, orient the light from one side, and record shoot direction over several days. Do not pull or repeatedly turn the plants during the observation.
:::

## 5.3 Healthy habits and life processes

Food, water, sleep, hygiene and physical activity support normal body processes. Eat a varied diet rather than relying on one food group. Safe drinking water and handwashing lower the spread of many infections. Regular activity strengthens the body, while rest allows recovery. Avoid tobacco, alcohol and unknown drugs; seek help from a trusted adult or health worker for health concerns instead of relying on unverified online advice.

Plants also need suitable light, water, air, minerals and space. Overwatering can reduce air in soil around roots; too little water can cause wilting. Healthy growth depends on several conditions together, so changing one factor at a time helps identify what matters. Never taste a plant or unknown substance as part of a classroom test.

::: caution Do not confuse processes
Breathing is air movement; respiration releases energy in cells. Egestion removes undigested food from the digestive tract; excretion removes metabolic waste. Keep these meanings distinct in diagrams and written answers.
:::

## Chapter summary

- Nutrition provides materials and energy; green plants photosynthesise and animals obtain food by feeding.
- Cellular respiration releases energy from glucose; breathing exchanges gases with the environment.
- Blood transports materials in animals; xylem and phloem transport materials in plants.
- Excretion removes metabolic wastes; it is different from egestion of undigested food.
- Growth, reproduction and response are important life processes; plants and animals respond to stimuli.
- Safe water, varied food, hygiene, rest and activity support health; plants need suitable growing conditions.

## Practice questions

1. Which process releases energy from food inside cells? (a) digestion (b) respiration (c) excretion (d) reproduction
2. Which plant tissue carries water from roots toward leaves?
3. Name one stimulus to which a plant can respond.
4. What is one difference between excretion and egestion?

::: note Answers to questions 1–4
**1.** (b) — cellular respiration releases usable energy from food.
**2.** Xylem.
**3.** Light, gravity, water or touch may act as a stimulus, depending on the example.
**4.** Excretion removes metabolic wastes; egestion removes undigested food from the digestive tract.
:::

5. Describe how oxygen can travel from the air to a working muscle cell.
6. Explain why a plant shoot growing toward a window is a response.
7. Give two habits that support health and explain how one helps.
8. A plant wilts in a dry classroom. Suggest one suitable observation and one action that may help it.

::: note Answers to questions 5–8
**5.** Oxygen enters the lungs during breathing, passes into the blood and is transported by vessels to the muscle cells.
**6.** The shoot changes its growth direction in response to light, an environmental stimulus.
**7.** Examples: handwashing, safe water, varied diet, sleep, activity. Handwashing removes many germs from hands and can reduce their spread.
**8.** Record the soil moisture and leaf condition; if the soil is dry, water appropriately and observe whether the plant recovers. Check light and drainage too.
:::

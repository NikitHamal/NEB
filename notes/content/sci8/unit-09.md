---
subject: Science and Technology
grade: 8
unit: 9
title: Matter
hours: 0
area: Science and Technology
---

Everything around us that has mass and occupies space is called matter. Matter can be solid, liquid or gas, and its properties can be explained using a simple particle model. Substances may be elements, compounds or mixtures. Learning how they differ helps us choose a suitable method to separate materials and describe changes accurately.

::: key Classify what is present
An **element** contains one kind of atom; a **compound** contains different elements chemically joined in a fixed proportion; a **mixture** contains substances together without being chemically joined. A mixture can often be separated by physical methods.
:::

## 9.1 States and particle model of matter

In the particle model, matter is made of tiny particles. In a **solid**, particles are close together and vibrate around fixed positions; the solid keeps its shape and volume. In a **liquid**, particles remain close but can move past one another, so a liquid flows and takes the shape of its container while keeping a nearly fixed volume. In a **gas**, particles are far apart and move freely, so a gas spreads to fill its container and can be compressed more easily.

Heating usually increases particle motion. When a solid melts, particles gain enough energy to move out of their fixed arrangement. When a liquid evaporates or boils, particles enter the gas state. Cooling can condense a gas to liquid or freeze a liquid to solid. During a change of state, the substance remains the same chemical substance; for example, liquid water and water vapour are both H₂O.

```figure caption="The particle model compares spacing and movement in solids, liquids and gases."
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1,3,figsize=(5.0,2.6))
labels=["Solid","Liquid","Gas"]
points=[[(x,y) for x in [0.25,0.5,0.75] for y in [0.25,0.5,0.75]],[(0.2,0.25),(0.45,0.28),(0.7,0.22),(0.3,0.52),(0.58,0.5),(0.8,0.56),(0.22,0.78),(0.51,0.76),(0.75,0.82)],[(0.15,0.2),(0.78,0.23),(0.42,0.42),(0.22,0.72),(0.83,0.8),(0.62,0.62)]]
for ax,label,coords in zip(axes,labels,points):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect("equal"); ax.set_title(label,fontsize=8,color=INK)
    ax.set_xticks([]); ax.set_yticks([]); ax.spines[["top","right","left","bottom"]].set_color(MUTED)
    for x,y in coords:
        ax.add_patch(plt.Circle((x,y),0.045,color=ACCENT))
fig.tight_layout()
```

::: example Identify a change of state
**Problem.** Water droplets form on the outside of a cold bottle on a warm day. Did water pass through the bottle wall?

**Solution.** Usually no. Water vapour in the surrounding air cooled near the bottle and condensed into liquid droplets on its outside surface. The change is gas to liquid; the bottle can remain sealed.
:::

## 9.2 Elements, compounds and mixtures

An **atom** is a tiny particle that forms an element. Each element has a name and symbol; examples include oxygen (O), iron (Fe) and carbon (C). A **molecule** is two or more atoms joined together. Oxygen gas is O₂, while water is H₂O. The chemical formula shows which atoms are present, but a formula does not by itself show the complete shape of a molecule.

A **compound** forms when atoms of different elements combine chemically. Water is a compound of hydrogen and oxygen in a fixed ratio. Its properties differ from those of hydrogen and oxygen. A **mixture** may contain two or more elements or compounds physically combined in any proportion. Air is a mixture of gases; salt water is a mixture of salt and water. The substances in a mixture keep their own properties and can often be separated physically.

| Type | What it contains | Example | Can it be separated by ordinary physical methods? |
|---|---|---|---|
| Element | One kind of atom | Copper, oxygen gas | No; it is not a mixture |
| Compound | Elements chemically joined in a fixed ratio | Water, carbon dioxide | No; a chemical change is needed |
| Mixture | Substances together but not chemically joined | Air, salt water | Often yes |

::: example Classify three materials
**Problem.** Classify oxygen gas, pure water and air as element, compound or mixture.

**Solution.** Oxygen gas is an **element** because it contains only oxygen atoms, commonly in O₂ molecules. Pure water is a **compound** because hydrogen and oxygen are chemically joined in a fixed ratio. Air is a **mixture** of gases such as nitrogen and oxygen, with amounts that can vary.
:::

## 9.3 Physical and chemical changes; separation methods

A **physical change** changes a material's form or state without making a new substance. Cutting paper, melting ice and dissolving sugar in water are physical changes. A **chemical change** forms one or more new substances. Rusting iron, burning wood and cooking an egg are chemical changes. Colour or temperature change can be a clue, but no single clue alone proves that a chemical reaction occurred.

Mixtures can be separated by taking advantage of differences in particle size, solubility, boiling point or magnetic behaviour. **Sieving** separates solids of different sizes. **Filtration** separates an insoluble solid from a liquid. **Evaporation** can recover a dissolved solid from a solution, while **distillation** boils and condenses a liquid to collect it separately. A magnet can remove magnetic material from a non-magnetic mixture. Choose a method that matches the substances and the goal.

```figure caption="A filter can separate an insoluble solid from a liquid mixture."
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
fig, ax = plt.subplots(figsize=(4.5, 2.9))
ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis("off")
ax.add_patch(Polygon([[2,5.8],[8,5.8],[5.7,3.5],[4.3,3.5]],closed=True,fill=False,ec=ACCENT,lw=1.4))
ax.plot([2.3,7.7],[5.6,5.6],color=SERIES[2],lw=1.1)
ax.add_patch(Polygon([[4.3,3.5],[5.7,3.5],[5.0,2.8]],closed=False,fill=False,ec=MUTED,lw=1.1))
ax.plot([5,5],[2.8,1.5],color=ACCENT,lw=1.2)
ax.add_patch(Polygon([[3.5,1.5],[6.5,1.5],[6.1,0.6],[3.9,0.6]],closed=True,fill=False,ec=INK,lw=1.2))
ax.add_patch(Circle((5,1.0),0.12,fc="#9dc7e8",ec="none"))
ax.text(1.2,6.2,"mixture",fontsize=7,color=INK); ax.text(2.0,4.2,"filter paper",fontsize=7,color=MUTED)
ax.text(5.4,2.3,"liquid",fontsize=7,color=ACCENT); ax.text(6.6,1.0,"filtrate",fontsize=7,color=INK)
fig.tight_layout()
```

::: example Separate sand and salt
**Problem.** A dry mixture contains sand and salt. Describe how to obtain the sand and the salt separately.

**Solution.** Add water and stir so that the salt dissolves. Filter the mixture: sand remains as residue on the filter. Evaporate the water from the filtrate to recover salt crystals. Use a teacher-approved heat source and eye protection; do not heat a solution to dryness over an open flame without supervision.
:::

::: example Decide whether a change is physical or chemical
**Problem.** A piece of iron left outside forms a reddish-brown coating. Is this evidence of a physical or chemical change?

**Solution.** Rust is a new substance formed when iron reacts with oxygen and water, so rusting is a **chemical change**. The coating's colour is an observation; identifying rust as a new substance explains why it is chemical.
:::

::: caution Bubbles do not always mean a new substance
Boiling water forms bubbles of water vapour, but the substance is still water. To identify a chemical change, consider whether new substances form and use more than one piece of evidence.
:::

## Chapter summary

- Matter has mass and occupies space; solids, liquids and gases differ in particle arrangement and movement.
- Heating and cooling can change a substance's state without changing its chemical identity.
- Elements contain one kind of atom; compounds contain elements chemically joined in fixed ratios.
- Mixtures contain substances physically combined and can often be separated by physical methods.
- Physical changes do not make new substances; chemical changes produce new substances.
- Sieving, filtration, evaporation, distillation and magnets separate mixtures using different properties.

## Practice questions

1. Which state has particles far apart and moving freely? (a) solid (b) liquid (c) gas (d) crystal only
2. Is air an element, compound or mixture?
3. Which method separates an insoluble solid from a liquid? (a) filtration (b) melting (c) freezing (d) magnetising
4. Is rusting iron a physical or chemical change?

::: note Answers to questions 1–4
**1.** (c) — gas particles are far apart and move freely.
**2.** A mixture of gases.
**3.** (a) — the insoluble solid is retained by the filter.
**4.** Chemical — rust is a new substance formed from iron and substances in the environment.
:::

5. Explain one difference between a compound and a mixture.
6. Describe how dissolved salt can be recovered from salt water.
7. A puddle dries in sunlight. Is this a chemical change? Explain.
8. Suggest a method for removing iron filings from sand.

::: note Answers to questions 5–8
**5.** A compound has elements chemically joined in fixed proportions; a mixture contains substances physically combined in variable proportions.
**6.** Evaporate the water using a safe, teacher-approved method; salt remains as crystals. Distillation is used if the water also needs to be collected.
**7.** No. Water evaporates from liquid to gas; it remains water and no new substance is formed.
**8.** Move a magnet through the mixture, preferably wrapped in paper or plastic so filings can be removed from it safely.
:::

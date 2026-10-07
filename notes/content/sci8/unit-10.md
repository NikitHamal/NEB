---
subject: Science and Technology
grade: 8
unit: 10
title: Materials Used in Daily Life
hours: 0
area: Science and Technology
---

People choose materials for buildings, clothes, tools, packaging and energy. A material is useful because of its properties, but no single material is best for every job. Comparing strength, flexibility, conductivity, cost, availability and environmental impact helps us make safer and more responsible choices.

::: key Choose a material for the job
Start with the purpose and conditions: Will it carry a load, touch food, face heat or get wet? Then compare the properties and risks of possible materials. A low price alone does not make a material suitable.
:::

## 10.1 Common natural and manufactured materials

A **natural material** comes from plants, animals or the Earth with limited processing. Examples include wood, cotton, wool, stone, clay and metals obtained from ores. A **manufactured material** is made by processing raw materials; examples include paper, glass, concrete, steel, ceramics and many plastics. Processing can change a material's properties and usually uses energy and resources.

Important properties include hardness, strength, toughness, flexibility, density, water resistance, heat resistance, electrical conductivity and ability to be shaped. **Hardness** describes resistance to scratching or indentation; **strength** describes how much force a material can withstand without breaking. A material can be hard but brittle. **Ductility** is the ability to be drawn into a wire, while **malleability** is the ability to be shaped into sheets.

| Material | Useful properties | Common uses | Points to consider |
|---|---|---|---|
| Wood | Can be strong, shaped and insulating | Furniture, doors, building parts | Needs suitable treatment and responsible sourcing |
| Glass | Transparent, hard and fairly chemically resistant | Windows, bottles | Can break into sharp pieces |
| Steel | Strong and shapeable; many types are magnetic | Tools, frames, vehicles | Can corrode unless protected; production uses resources |
| Plastic | Light, shapeable and often water-resistant | Containers, insulation, equipment | Some types persist in the environment and are hard to recycle |
| Cotton | Soft, flexible natural fibre | Clothing, cloth | Growing and processing use water and land |
| Clay ceramic | Hard and heat-resistant | Tiles, dishes, pots | Can be brittle and break |

```figure caption="A safe material choice checks the task, properties, cost and environmental effects."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
steps=[("Define the\njob",0.2),("Compare\nproperties",2.65),("Check safety\nand cost",5.1),("Consider\nenvironment",7.55)]
for label,x in steps:
    ax.add_patch(FancyBboxPatch((x,2.0),2.1,1.1,boxstyle="round,pad=0.07",fc="#eef3fb",ec=ACCENT,lw=1.0))
    ax.text(x+1.05,2.55,label,ha="center",va="center",fontsize=7.4,color=INK)
for (_,x1),(_,x2) in zip(steps,steps[1:]):
    ax.annotate("",xy=(x2-0.08,2.55),xytext=(x1+2.14,2.55),arrowprops=dict(arrowstyle="->",color=MUTED,lw=1.0))
ax.text(5,1.1,"Choose a material that suits the use and can be handled responsibly.",ha="center",fontsize=7,color=MUTED)
fig.tight_layout()
```

::: example Select a handle for a cooking pot
**Problem.** A pot becomes hot on a stove. Why is a handle made from a suitable plastic or wood often safer than a bare metal handle?

**Solution.** Many plastics and dry wood conduct heat less readily than metal, so the handle may remain cooler for longer. The material must also withstand the expected temperature and be firmly attached. No handle is guaranteed to stay cool; use a dry cloth or mitt and follow the appliance instructions.
:::

## 10.2 Metals, non-metals, plastics, fibres, fuels and household substances

Metals are commonly shiny when freshly cut, can often be shaped and usually conduct heat and electricity well. Iron, aluminium and copper are examples. Non-metals such as sulphur, oxygen and carbon often have different properties, but there are exceptions: graphite, a form of carbon, conducts electricity. Do not rely on appearance alone to identify a substance.

Plastics are a broad family of manufactured polymers. They can be light, moulded into many shapes and resistant to water, which makes them useful for containers and insulation. Different plastics behave differently when heated or exposed to chemicals. Never burn plastic as a disposal method; fumes can be harmful. Fibres are thin strands used to make yarn and cloth. Cotton and wool are natural fibres; nylon and polyester are manufactured fibres. Their comfort, strength, absorbency and environmental effects vary.

Fuels store chemical energy. Wood, biogas, liquefied petroleum gas (LPG) and petroleum products are used for cooking or transport in different places. Burning a fuel can release heat, but incomplete burning may produce harmful smoke or carbon monoxide. Household substances such as cleaners, paints, batteries and medicines must be stored and used according to their labels. Never mix cleaning products or taste an unknown substance.

::: example Compare two fibres
**Problem.** A student needs a cloth that absorbs sweat. What properties should be compared when choosing between cotton and polyester?

**Solution.** Compare absorbency, comfort, drying time, strength, care instructions and source. Cotton commonly absorbs more water than polyester, while polyester often dries faster. The exact performance depends on the fabric weave and blend, so check the garment label rather than assuming every cloth behaves identically.
:::

::: example Read a material property
**Problem.** A metal spoon and a wooden spoon are left in warm soup. Which handle is likely to warm more slowly, and why?

**Solution.** A dry wooden spoon handle is likely to warm more slowly because wood is a poorer conductor of heat than most metals. The metal spoon transfers heat more readily. This is a general comparison; the result also depends on the spoon's thickness, starting temperature and how long it stays in the soup.
:::

## 10.3 Safe use, reuse, recycling and environmental impact

Use a material according to its purpose and instructions. Keep fuels away from flames and store them only in approved containers. Do not pour oil, paint, medicines or chemicals into a drain or onto soil. Batteries and electronic devices may contain substances that need special collection; ask the local authority or school about safe disposal. Broken glass should be handled by an adult with suitable tools, not picked up with bare hands.

The waste hierarchy begins with **reduce**—avoid unnecessary material—then **reuse** items safely, repair where possible and **recycle** suitable materials through an available collection system. Recycling can save some raw materials and energy, but it requires sorting, transport and processing; it does not make unlimited consumption harmless. Compostable material should only go into a suitable composting system. Litter can harm animals, block drains and enter rivers.

```figure caption="A material can move through use, reuse and recycling; design and local collection affect what happens next."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8, 2.7))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
steps=[("Raw\nmaterials",(0.5,3.9)),("Make",(3.0,3.9)),("Use",(5.5,3.9)),("Reuse or\nrepair",(5.5,1.1)),("Recycle or\nsafe disposal",(0.5,1.1))]
for label,(x,y) in steps:
    ax.add_patch(FancyBboxPatch((x,y),2.0,0.9,boxstyle="round,pad=0.06",fc="#eef5e8",ec=SERIES[2],lw=1.0))
    ax.text(x+1,y+0.45,label,ha="center",va="center",fontsize=7.2,color=INK)
for a,b in [((2.6,4.35),(2.9,4.35)),((5.1,4.35),(5.4,4.35)),((6.5,3.8),(6.5,2.1)),((5.4,1.55),(2.6,1.55)),((1.5,2.05),(1.5,3.75))]:
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.0))
ax.text(4.0,0.35,"Reduce unnecessary use at every stage",ha="center",fontsize=7,color=MUTED)
fig.tight_layout()
```

::: example Make a safer disposal plan
**Problem.** A student finds an old battery and an empty glass jar at home. Suggest a responsible next step for each.

**Solution.** Keep the battery away from children and heat, and ask an adult or local authority where battery collection is available; do not burn it or open it. If the jar is clean and unbroken, it may be reused or placed in the appropriate glass-recycling collection. If it is broken, tell an adult and avoid touching the pieces.
:::

::: caution “Natural” does not always mean harmless
Some natural substances can be poisonous, flammable or irritating, and some manufactured materials are designed for safe use. Identify a substance from its label and use it according to instructions; never taste or mix unknown materials.
:::

## Chapter summary

- Natural materials come from plants, animals or Earth; manufactured materials are processed into useful forms.
- Hardness, strength, flexibility, conductivity and heat resistance help determine a material's uses.
- Metals, non-metals, plastics, fibres and fuels have different properties, with exceptions within each group.
- Store fuels and household substances safely; never mix cleaners or burn plastic waste.
- Reduce unnecessary use, reuse and repair items safely, and recycle through an available collection system.
- Material production, transport, use and disposal all affect the environment.

## Practice questions

1. Which material is usually a good electrical conductor? (a) copper (b) dry wood (c) rubber (d) paper
2. Name one natural fibre.
3. Why should plastic not be burned as a way to dispose of it?
4. What should be done before using a household cleaner?

::: note Answers to questions 1–4
**1.** (a) — copper is a metal that conducts electricity well.
**2.** Cotton or wool.
**3.** Burning plastic can release harmful fumes and pollute the air.
**4.** Read and follow its label; do not mix it with other cleaners and keep it away from children.
:::

5. Give two properties that make glass useful for a window and one risk of using it.
6. Explain why a steel tool can be strong but still need protection from rust.
7. State the waste hierarchy in a useful order and give one example of reuse.
8. Why should a student ask an adult about disposing of an old battery?

::: note Answers to questions 5–8
**5.** Glass is transparent and weather-resistant; it can break into sharp pieces.
**6.** Steel can withstand large forces, but iron in it may react with oxygen and water to form rust. A suitable coating can slow corrosion.
**7.** Reduce, reuse or repair, then recycle or dispose safely. Example: use a clean jar again for storage.
**8.** Batteries may contain materials requiring special collection; adults can identify a safe local disposal route.
:::

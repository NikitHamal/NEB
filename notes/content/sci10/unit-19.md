---
subject: Science and Technology
grade: 10
unit: 19
title: Chemicals used in Daily Life
hours: 0
area: Science and Technology
---

From the moment you wash your face with soap in the morning to the moment you switch off a light in a glass bulb at night, you use chemicals made in factories. Farmers spread fertilisers on terraces to grow more rice and maize; builders mix cement with sand to raise houses; and plastic bags, bottles and pipes are everywhere. This chapter explains what these materials are, how they are made, how they work, and what harm they can do when we are careless with them.

::: key What the SEE paper asks from this chapter
Expect: the cleaning action of soap and the difference between soap and detergent (2 to 4 marks); the names, formulae and uses of chemical fertilisers and a percentage-of-nitrogen numerical (2 to 4 marks); the raw materials and uses of cement and glass (2 marks); the difference between thermoplastics and thermosetting plastics and the problems of plastic waste (2 to 4 marks).
:::

## 19.1 Soaps and detergents

### Soap

**Soap** is the sodium or potassium salt of a long-chain fatty acid (such as stearic, palmitic or oleic acid). A typical soap is sodium stearate, C₁₇H₃₅COONa.

```photo id="sci10/soap" caption="Bars of soap. Soap is made by boiling a fat or oil with an alkali such as sodium hydroxide." width="60"
```

**Making soap: saponification.** Vegetable oil or animal fat (a compound of glycerol and fatty acids, called an ester) is boiled with a strong alkali (caustic soda, NaOH). The change is called **saponification**.

Fat or oil + NaOH → Soap + Glycerol

Steps in the factory:

1. **Boiling.** Oil or fat is boiled with NaOH solution in a large kettle.
2. **Salting out.** Common salt (NaCl) is added. Soap is less soluble in salt water, so it rises as a curd on top, and the glycerol with salt water stays beneath.
3. **Purification and finishing.** The soap is washed, perfume, colour and sometimes a germicide are added, and it is moulded into cakes.

Using KOH instead of NaOH gives **soft soap** (shaving cream, liquid soap). NaOH gives **hard soap** (bathing and washing bars).

Glycerol, the by-product, is valuable. It is used in cosmetics, medicines and explosives (nitroglycerine).

### How soap cleans

A soap molecule has two ends.

- A **hydrophilic** (water-loving) head: the –COO⁻Na⁺ part, which dissolves in water.
- A **hydrophobic** (water-hating) tail: the long hydrocarbon chain, which dissolves in oil and grease but not in water.

When soap is added to dirty cloth in water, the tails stick into the grease and the heads stay in the water. The grease is pulled off the cloth and broken into tiny droplets surrounded by soap molecules. These clusters are called **micelles**. Micelles stay dispersed in water and are rinsed away with the dirt.

```figure caption="Cleaning action of soap. Tails dissolve in the grease droplet; the charged heads point into water, forming a micelle that is washed away."
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.0,2.8))
ax.set_aspect('equal')
ang = np.linspace(0, 2*np.pi, 16, endpoint=False)
ax.add_patch(Circle((2.2,1.5), 0.85, fc='#f6e3a3', ec=INK, lw=1))
ax.text(2.2,1.5,'grease', ha='center', va='center', fontsize=7.5, color=INK)
for a in ang:
    x0,y0 = 2.2+0.85*np.cos(a), 1.5+0.85*np.sin(a)
    x1,y1 = 2.2+1.45*np.cos(a), 1.5+1.45*np.sin(a)
    ax.plot([x0,x1],[y0,y1], color=SERIES[1], lw=1.4)
    ax.add_patch(Circle((x1,y1), 0.1, fc=ACCENT, ec=INK, lw=0.5, zorder=3))
ax.text(2.2,-0.25,'micelle in water', ha='center', fontsize=7.5, color=INK)
ax.plot([5.2,6.4],[2.2,2.2], color=SERIES[1], lw=2); ax.add_patch(Circle((6.4,2.2), 0.12, fc=ACCENT, ec=INK, lw=0.5))
ax.text(6.7,2.2,'one soap molecule', fontsize=7.5, color=INK, va='center')
ax.text(5.2,1.75,'tail: hydrophobic (in grease)', fontsize=7, color=SERIES[1], va='center')
ax.text(5.2,1.3,'head: hydrophilic (in water)', fontsize=7, color=ACCENT, va='center')
ax.text(5.2,0.6,'C₁₇H₃₅–COO⁻Na⁺', fontsize=8, color=INK, va='center')
ax.set_xlim(0, 9.5); ax.set_ylim(-0.6, 3.3); ax.axis('off')
```

### Hard water and soap

Water containing calcium and magnesium salts is **hard water**. Soap reacts with these salts to form an insoluble, sticky **scum**:

2C₁₇H₃₅COONa + CaCl₂ → (C₁₇H₃₅COO)₂Ca ↓ + 2NaCl

Much soap is wasted before any lather forms. Hard water is softened by boiling (for temporary hardness) or by adding washing soda (Na₂CO₃).

### Detergents

A **detergent** is a cleaning agent made from **synthetic** chemicals, usually the sodium salt of a sulphonic acid or an alkyl sulphate, for example sodium lauryl sulphate, C₁₂H₂₅OSO₃Na. Detergents are made from petroleum products.

| Soap | Detergent |
|---|---|
| Sodium or potassium salt of a fatty acid | Sodium salt of a sulphonic acid or alkyl sulphate |
| Made from natural oils and fats | Made from petrochemicals |
| Forms scum in hard water | Does **not** form scum; works in hard water |
| Biodegradable | Some (those with branched chains) are non-biodegradable |
| Less effective in acidic water | Effective in acidic and hard water |
| Gentle on skin and clothes | Can be harsh |

### Environmental effect

Detergents with branched chains are not broken down by bacteria. They remain in rivers and lakes and form foam. The phosphates added to detergents act as a fertiliser for algae, which grow rapidly and use up the oxygen of the water, killing fish. This is **eutrophication**. Using **biodegradable detergents** (straight-chain) and using less detergent reduces the harm.

## 19.2 Fertilisers

Plants need nutrients for growth. The three main nutrients are **nitrogen (N), phosphorus (P) and potassium (K)**. Crops remove them from the soil, so they must be returned as **fertilisers**.

A **fertiliser** is a natural or synthetic substance added to the soil to supply the nutrients that plants need.

| Nutrient | Role in the plant | Sign of shortage |
|---|---|---|
| Nitrogen | leaf and stem growth, makes protein and chlorophyll | yellow leaves, stunted growth |
| Phosphorus | root growth, flowering and seeds | purple leaves, weak roots |
| Potassium | disease resistance, fruit quality | brown leaf edges |

### Organic and chemical fertilisers

| Organic (natural) fertilisers | Chemical (artificial) fertilisers |
|---|---|
| Farmyard manure, compost, green manure, bio-slurry | Urea, DAP, MOP, ammonium sulphate |
| Release nutrients slowly | Give nutrients quickly |
| Improve soil structure and water holding | Do not add humus |
| Cheap, locally available | Cost money; imported into Nepal |
| Safe for soil life | Overuse harms the soil and water |

### Common chemical fertilisers

| Fertiliser | Formula | Nutrient | Content |
|---|---|---|---|
| Urea | CO(NH₂)₂ | N | 46 % N (highest among solid N fertilisers) |
| Ammonium sulphate | (NH₄)₂SO₄ | N | 21 % N |
| Ammonium nitrate | NH₄NO₃ | N | 35 % N |
| Single superphosphate | Ca(H₂PO₄)₂ + CaSO₄ | P | about 16 % P₂O₅ |
| Muriate of potash (MOP) | KCl | K | about 60 % K₂O |
| DAP (diammonium phosphate) | (NH₄)₂HPO₄ | N and P | 18 % N, 46 % P₂O₅ |
| NPK complex | mixture | N, P, K | e.g. 15-15-15 |

```photo id="sci10/urea" caption="A tractor spreading chemical fertiliser, such as urea, over a field." width="66"
```

**Urea** is made from ammonia and carbon dioxide at high pressure:

2NH₃ + CO₂ → CO(NH₂)₂ + H₂O

**Ammonia** is made by the Haber process: N₂ + 3H₂ ⇌ 2NH₃ (iron catalyst, about 450 °C and 200 atm). Hydrogen and nitrogen are the raw materials.

::: example Percentage of nitrogen in urea
**Problem.** Calculate the percentage of nitrogen in urea, CO(NH₂)₂. (C = 12, O = 16, N = 14, H = 1.)

**Solution.** Molar mass = 12 + 16 + 2 × (14 + 2 × 1) = 28 + 2 × 16 = 28 + 32 = **60**. Nitrogen present = 2 × 14 = 28. % N = (28 / 60) × 100 = **46.7 %**.
:::

::: example Which fertiliser is richer in nitrogen?
**Problem.** Compare the nitrogen content of ammonium nitrate (NH₄NO₃) with ammonium sulphate ((NH₄)₂SO₄). (N = 14, H = 1, O = 16, S = 32.)

**Solution.** NH₄NO₃: M = 14 + 4 + 14 + 48 = 80; N = 28; % N = 28/80 × 100 = **35 %**. (NH₄)₂SO₄: M = 2 × 18 + 32 + 64 = 36 + 96 = 132; N = 28; % N = 28/132 × 100 = **21.2 %**. Ammonium nitrate is richer in nitrogen.
:::

::: example Amount of fertiliser needed
**Problem.** A field needs 23 kg of nitrogen. How much urea (46 % N) is needed?

**Solution.** Mass of urea = 23 / 0.46 = **50 kg**.
:::

### Problems of excess use of chemical fertilisers

- Soil becomes hard, acidic and less fertile; useful soil organisms die.
- Runoff pollutes rivers and ponds and causes **eutrophication**.
- Nitrate in drinking water is harmful, especially to infants ("blue baby" disease).
- Plants may be burnt by an overdose.

::: caution Do not say chemical fertilisers are always bad
Fertilisers are not the enemy; **excess** and **wrong** use is. Nepali farmers face a real shortage of fertiliser at planting time, and the right approach is balanced use: organic manure as the base, with chemical fertiliser topped up according to soil tests.
:::

## 19.3 Cement

**Cement** is a fine grey powder which, when mixed with water, sets into a hard, stone-like mass. The type commonly used is **Portland cement**, invented by Joseph Aspdin in 1824, so called because the hardened cement looked like Portland stone. Nepal has several cement factories (for example at Hetauda, Udayapur and Butwal), using limestone found in the country.

```photo id="sci10/cement" caption="Bags of Portland cement, each holding 25 kg. Cement is mixed with sand and water to make mortar and concrete." width="60"
```

### Raw materials

- **Limestone** (CaCO₃) — source of lime (about 75 %)
- **Clay or shale** (silica SiO₂, alumina Al₂O₃, iron oxide) — about 25 %
- **Gypsum** (CaSO₄·2H₂O) — 2 to 3 %, added at the end to **slow the setting**

### Approximate composition

| Oxide | Percentage |
|---|---|
| Lime (CaO) | 60 to 67 |
| Silica (SiO₂) | 17 to 25 |
| Alumina (Al₂O₃) | 3 to 8 |
| Iron oxide (Fe₂O₃) | 0.5 to 6 |
| Magnesia (MgO) | 0.1 to 4 |

### Manufacture

1. The limestone and clay are **crushed and ground** to a fine powder and mixed in the correct proportion with water (wet process) or dry (dry process) to form a **slurry** or raw meal.
2. The mixture is heated in a long, slightly tilted rotating **kiln** at about **1400 to 1500 °C**. Limestone decomposes (CaCO₃ → CaO + CO₂) and the materials fuse into small lumps called **clinker**.
3. The hot clinker is cooled and **ground** to a fine powder with **2 to 3 % gypsum**.
4. The cement is packed in bags (50 kg bags are standard).

### Setting and hardening

When water is added, the compounds in cement react with water (they **hydrate**), forming a rigid gel and crystals that bind the sand and gravel. This is **setting**, which takes a few hours; the **hardening** continues for weeks. Cement needs water to be kept on the surface for 7 to 28 days (**curing**). Without gypsum, cement would set almost at once, before it could be placed.

### Mortar and concrete

| Material | Composition | Use |
|---|---|---|
| Mortar | cement + sand + water (1 : 4 or 1 : 6) | laying bricks, plastering |
| Concrete | cement + sand + gravel (aggregate) + water (1 : 2 : 4) | floors, slabs, roads |
| Reinforced cement concrete (RCC) | concrete with steel bars | beams, columns, bridges, earthquake-resistant buildings |

::: tip Why steel in RCC?
Concrete is strong when it is pressed (compression) but weak when it is pulled (tension). Steel bars take the pulling force, and steel and concrete expand by almost the same amount on heating, so they do not tear apart.
:::

::: example Quantity of materials
**Problem.** A concrete mix is 1 : 2 : 4 (cement : sand : gravel) by volume. If 7 parts of dry mix are needed in all, how much of each is needed for 3.5 m³ of dry mix?

**Solution.** Total parts = 1 + 2 + 4 = 7. Cement = (1/7) × 3.5 = **0.5 m³**. Sand = (2/7) × 3.5 = **1.0 m³**. Gravel = (4/7) × 3.5 = **2.0 m³**.
:::

## 19.4 Glass

**Glass** is a hard, transparent, brittle, **amorphous** solid (it has no regular crystal arrangement). It is sometimes called a super-cooled liquid. Glass is made by fusing sand with other chemicals.

```photo id="sci10/glass-recycling" caption="Containers for collecting glass for recycling. Used glass can be melted again and made into new bottles." width="60"
```

### Raw materials

| Raw material | Chemical | Role |
|---|---|---|
| Sand | SiO₂ | main ingredient (about 70 %) |
| Soda ash | Na₂CO₃ | lowers the melting point |
| Limestone | CaCO₃ | makes glass hard and durable |
| Cullet | broken glass | recycled, saves energy |

### Manufacture of ordinary soda-lime glass

1. The raw materials are mixed and fed into a **furnace** at about **1500 °C** where they melt.
2. Na₂CO₃ + SiO₂ → Na₂SiO₃ + CO₂ ↑ and CaCO₃ + SiO₂ → CaSiO₃ + CO₂ ↑. The molten mixture of sodium silicate, calcium silicate and extra silica is soda-lime glass.
3. The molten glass is shaped by blowing, pressing, or floating on molten tin (flat sheets).
4. **Annealing:** the shaped glass is cooled very slowly in an oven. Rapid cooling would leave stress that makes the glass break easily.

### Kinds of glass

| Type | Special ingredients | Properties and use |
|---|---|---|
| Soda-lime (soft) glass | Na₂CO₃, CaCO₃, SiO₂ | windows, bottles, tumblers |
| Pyrex (borosilicate) | B₂O₃ in place of part of the silica | does not crack on heating; laboratory apparatus, oven dishes |
| Lead (flint) glass | PbO | bright, high refractive index; lenses, cut glass, decorations |
| Coloured glass | metal oxides | cobalt oxide gives blue, copper oxide green, iron oxide brown, gold chloride ruby red |
| Safety glass | plastic layer between sheets | does not shatter; car windscreen |
| Optical glass | special composition | lenses, spectacles, microscopes |

::: caution Glass is not a crystalline solid
Many students say glass is a crystal because it is clear. Its particles have no regular order, so it is **amorphous**. It has no sharp melting point; it softens gradually.
:::

## 19.5 Plastics and polymers

### Polymers

A **polymer** is a very large molecule (macromolecule) formed by joining thousands of small molecules called **monomers**. The process is **polymerisation**.

n CH₂=CH₂ → –(CH₂–CH₂)ₙ–

Here ethene (the monomer) forms polythene (the polymer).

Polymers are **natural** (cellulose, starch, protein, rubber, DNA) or **synthetic** (polythene, PVC, nylon, polyester).

### Plastics

**Plastics** are synthetic polymers that can be moulded into any shape by heat and pressure. They are light, cheap, strong, waterproof, corrosion-resistant and poor conductors of heat and electricity.

```photo id="sci10/pet-bottles" caption="Plastic (PET) bottles collected for recycling. Plastics are polymers." width="60"
```

| Type | Behaviour on heating | Examples and uses |
|---|---|---|
| **Thermoplastic** | softens on heating and hardens on cooling; can be re-moulded again and again | polythene (bags, bottles), PVC (pipes, raincoats), polystyrene (thermocol), nylon (ropes, fibres) |
| **Thermosetting plastic** | sets permanently on the first heating; cannot be softened again | Bakelite (switches, plugs, handles), melamine (plates, tabletops) |

### Common plastics

| Polymer | Monomer | Properties | Uses |
|---|---|---|---|
| Polythene (polyethylene) | ethene | soft, flexible, waterproof | bags, bottles, films, pipes |
| PVC (polyvinyl chloride) | vinyl chloride, CH₂=CHCl | tough, long-lasting | water pipes, wire insulation, rainwear |
| Polystyrene | styrene | light, foam | thermocol packing, cups |
| Teflon (PTFE) | tetrafluoroethene | non-stick, heat resistant | non-stick pans |
| Nylon | adipic acid + hexamethylenediamine | strong, elastic | ropes, fishing nets, clothes |
| Bakelite | phenol + formaldehyde | hard, heat-resistant | switches, handles |

```figure caption="Classification of polymers and plastics."
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.0))
def box(x,y,w,h,s,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.1',fc=fc,ec=INK,lw=0.9))
    ax.text(x+w/2,y+h/2,s,ha='center',va='center',fontsize=7,color=INK)
def link(x1,y1,x2,y2): ax.plot([x1,x2],[y1,y2],color=INK,lw=0.9)
box(3.6,5.0,2.8,0.7,'POLYMERS','#dbe7f7')
box(0.6,3.6,3.2,0.8,'Natural\n(starch, protein, rubber)','#e6f2e0')
box(6.2,3.6,3.2,0.8,'Synthetic\n(plastics, nylon, polyester)','#fbe9d3')
link(5.0,5.0,5.0,4.7); link(2.2,4.7,7.8,4.7); link(2.2,4.7,2.2,4.4); link(7.8,4.7,7.8,4.4)
box(4.7,2.0,2.6,0.8,'Thermoplastic\npolythene, PVC','#fbe9d3')
box(7.8,2.0,2.6,0.8,'Thermosetting\nBakelite, melamine','#fbe9d3')
link(7.8,3.6,7.8,3.3); link(6.0,3.3,9.1,3.3); link(6.0,3.3,6.0,2.8); link(9.1,3.3,9.1,2.8)
box(4.7,0.6,2.6,0.8,'soften on heating,\nreusable','#ffffff'); box(7.8,0.6,2.6,0.8,'set once,\nnot reusable','#ffffff')
link(6.0,2.0,6.0,1.4); link(9.1,2.0,9.1,1.4)
ax.set_xlim(0,10.6); ax.set_ylim(0.3,6.0); ax.axis('off')
```

### Other synthetic polymers

- **Synthetic rubber** (neoprene, Buna-S) is more resistant to oil and heat than natural rubber and is used in tyres.
- **Synthetic fibres** such as nylon and polyester (terylene) are strong, wrinkle-resistant and quick to dry.
- **Rayon** is made from cellulose of wood pulp and is called artificial silk.

### Problems of plastics and their management

| Problem | Explanation |
|---|---|
| **Non-biodegradable** | Bacteria cannot break down most plastics, so they remain in the soil for hundreds of years. |
| Blocks drains and rivers | Plastic bags jam drains in Kathmandu and increase flooding. |
| Harms animals | Cows and other animals die after eating plastic bags. |
| Burning is toxic | Burning plastic, particularly PVC, releases poisonous gases (dioxins, HCl, CO). |
| Soil pollution | Plastic stops water and air from entering the soil. |
| Microplastics | Small fragments enter water, fish and food chains. |

Management follows the **4 Rs**: **Reduce** the use of plastic bags (carry a cloth bag); **Reuse** containers; **Recycle** plastics (thermoplastics can be melted and remoulded); **Refuse** single-use plastic. Nepal has banned very thin plastic bags (below 40 microns), and many municipalities encourage jute and paper bags.

::: example Molecular mass of a polymer
**Problem.** Polythene is made of ethene units (C₂H₄). If the average polymer has 1000 monomer units, find its relative molecular mass. (C = 12, H = 1.)

**Solution.** Mass of C₂H₄ = 24 + 4 = 28. Mass of polymer = 28 × 1000 = **28 000**.
:::

## Chapter summary

- **Soap** is the sodium or potassium salt of a fatty acid, made by saponification of oil or fat with alkali; glycerol is a by-product. It cleans by forming micelles around grease.
- Soap forms scum with hard water; **detergents** (synthetic) do not, but non-biodegradable ones pollute water.
- Fertilisers supply N, P and K. Urea has 46 % N. Excess use causes soil damage and eutrophication.
- **Cement** is made by heating limestone and clay at 1400 to 1500 °C and grinding the clinker with 2 to 3 % gypsum; mortar, concrete and RCC are its main products.
- **Glass** is an amorphous solid made by fusing sand (SiO₂), soda ash (Na₂CO₃) and limestone (CaCO₃) at about 1500 °C; it is annealed by slow cooling.
- **Polymers** are formed from monomers; thermoplastics soften on heating, thermosetting plastics do not.
- Plastics are non-biodegradable, so reduce, reuse, recycle and refuse.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. The process of making soap from fat and alkali is called <span class="marks">[1]</span>
   (a) hydrogenation (b) saponification (c) polymerisation (d) fermentation
2. The percentage of nitrogen in urea is about <span class="marks">[1]</span>
   (a) 21 % (b) 35 % (c) 46 % (d) 82 %
3. Gypsum is added to cement to <span class="marks">[1]</span>
   (a) make it grey (b) slow down the setting (c) harden it (d) reduce the cost only
4. Which of the following is a thermosetting plastic? <span class="marks">[1]</span>
   (a) polythene (b) PVC (c) Bakelite (d) nylon
5. The raw material for glass is <span class="marks">[1]</span>
   (a) sand (b) clay (c) gypsum (d) coal
6. Detergents are better than soap in <span class="marks">[1]</span>
   (a) soft water (b) hard water (c) distilled water (d) rain water

::: note Answers to Group A
**1.** (b) — saponification.
**2.** (c) — 28/60 = 46.7 %.
**3.** (b) — otherwise cement sets too quickly.
**4.** (c) — Bakelite sets permanently.
**5.** (a) — silica (SiO₂) in sand.
**6.** (b) — detergents do not form scum with Ca²⁺ and Mg²⁺.
:::

**Group B — Short answer (2 marks each)**

1. What is a fertiliser? Name the three primary nutrients. <span class="marks">[2]</span>
2. Why is annealing done in glass making? <span class="marks">[2]</span>
3. Differentiate between thermoplastic and thermosetting plastic. <span class="marks">[2]</span>
4. Why does soap not lather well in hard water? <span class="marks">[2]</span>
5. Write two problems caused by the excess use of plastics. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A substance added to soil to supply nutrients to plants. Nitrogen, phosphorus, potassium.
**2.** The glass is cooled slowly to remove internal stress, so that it does not break easily.
**3.** A thermoplastic softens on heating and can be re-moulded (polythene); a thermosetting plastic sets permanently after heating once (Bakelite).
**4.** Ca²⁺ and Mg²⁺ ions react with soap to form insoluble scum, so soap is wasted before it can lather.
**5.** Plastics are non-biodegradable and pollute soil; they block drains and harm animals; burning releases toxic gases.
:::

**Group C — Long answer (4 marks each)**

1. Describe the manufacture of soap. Explain the cleaning action of soap. <span class="marks">[4]</span>
2. Describe how Portland cement is made, stating the raw materials and the role of gypsum. <span class="marks">[4]</span>
3. A farmer needs 92 kg of nitrogen. How much (a) urea (46 % N) and (b) ammonium nitrate (35 % N) would be needed? <span class="marks">[4]</span>
4. What is a polymer? Explain the types of plastics with two examples each and suggest four ways to manage plastic waste. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Saponification: boil oil or fat with NaOH; add salt to separate soap (salting out); wash, add perfume and mould. Cleaning: tails dissolve in grease, heads stay in water, grease is broken into micelles and rinsed away.
**2.** Limestone and clay are ground, mixed and heated at 1400 to 1500 °C in a rotary kiln to form clinker; clinker is ground with 2 to 3 % gypsum. Gypsum slows the setting.
**3.** (a) Urea = 92 / 0.46 = **200 kg**. (b) Ammonium nitrate = 92 / 0.35 = **262.9 kg** (about 263 kg).
**4.** A polymer is a large molecule formed from many monomers. Thermoplastics (polythene, PVC) soften on heating; thermosetting plastics (Bakelite, melamine) do not. Management: reduce, reuse, recycle, refuse; ban thin bags; use jute or paper bags.
:::

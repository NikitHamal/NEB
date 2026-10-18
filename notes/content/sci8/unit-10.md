---
subject: Science and Technology
grade: 8
unit: 10
title: Materials Used in Daily Life
hours: 0
area: Science and Technology
---

A Nepali kitchen holds cement in the wall, glass in the window, plastic in the
bucket, soap at the tap, fertiliser in the shed and kerosene or LPG in the
stove. Each of these materials is used because of a property that somebody
chose deliberately. This unit looks at what they are, how they behave, what
they do for us and what they cost the environment — beginning with water, which
is the material we cannot do without for a single day.

::: key What this unit asks of you
You should be able to describe the sources of water and distinguish hard from
soft water, describe four methods of purifying water, name the main
water-borne diseases and how to prevent them, state the uses of cement, glass
and plastics and the harm plastics cause, explain how soap removes dirt, name
the three plant nutrients supplied by fertiliser, and explain the conditions
needed for combustion and the safety rules for LPG.
:::

## 10.1 Water

### 10.1.1 Sources and the water cycle

Fresh water reaches us from rain, and the rain that does not run off or
evaporate soaks into the ground and is stored in the pores and cracks of rock as
**groundwater**. A spring, a *kuwa*, a *dhara*, a tube well and a river are all
ways of reaching stored or flowing water.

| Source | Usually safer? | Why |
|---|---|---|
| Rain water | yes | it is distilled water by nature; the risk comes from the roof and the tank |
| Spring water | often | filtered through rock, but open springs are easily contaminated |
| Tube-well water | usually | drawn from below the surface, but arsenic and iron can be present |
| River and pond water | no | open to sewage, washing, animals and runoff |
| *Kuwa* (open well) | depends | safe if the wall is raised, the floor is sealed and water is drawn with a pump |

### 10.1.2 Hard and soft water

**Soft water** lathers easily with soap. **Hard water** does not, because it
contains dissolved salts of calcium and magnesium.

| | Temporary hardness | Permanent hardness |
|---|---|---|
| Caused by | calcium and magnesium bicarbonates | sulphates and chlorides of calcium and magnesium |
| Removed by | boiling | not by boiling; needs washing soda, ion exchange or distillation |
| Effect | more soap needed; scale in kettles | same, and it cannot be cured by heating |

Hard water is not harmful to drink — it may even supply calcium — but it wastes
soap and forms scale inside kettles and boilers.

### 10.1.3 Purification of water

| Method | How it works | Removes |
|---|---|---|
| Boiling | heat kills microorganisms | germs (not dissolved salts) |
| Filtration | water passes through sand, gravel and cloth or a ceramic filter | suspended particles and many germs |
| Chlorination | chlorine or bleaching powder is added | germs |
| Distillation | water is boiled and the vapour condensed | salts and germs — gives pure water |
| Sedimentation with alum | alum makes fine particles clump and settle | mud and turbidity |
| SODIS | clear plastic bottles filled with water are left in the sun for six hours; the ultraviolet light and the heat kill germs | germs, where fuel is scarce |

```figure caption="A household water-purification train. Each stage removes what the previous one could not; boiling is the last defence against germs, not a substitute for filtration."
fig, ax = plt.subplots(figsize=(5.1, 2.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")
stages = [("Settle", 0.9, "heavy mud\\nsinks"), ("Filter", 3.1, "sand, gravel,\\ncloth"),
          ("Boil", 5.3, "kills germs"), ("Store", 7.5, "covered pot with\\na tap or a lid"),
          ("Drink", 9.5, "safe water")]
for name, x, note in stages:
    ax.text(x, 3.9, name, ha="center", va="center", fontsize=7.0, color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ACCENT, lw=1.0))
    ax.text(x, 2.85, note, ha="center", va="center", fontsize=6.0, color=MUTED)
for i in range(4):
    x0 = 0.9 + i * 2.1
    ax.annotate("", xy=(x0 + 1.15, 3.9), xytext=(x0 + 0.62, 3.9),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
ax.text(5.0, 1.7, "do not dip a glass into the pot — it puts the germs back in",
        ha="center", fontsize=6.5, color=SERIES[1])
ax.text(5.0, 1.05, "and keep the storage pot above the floor, never beside the toilet",
        ha="center", fontsize=6.5, color=MUTED)
fig.tight_layout()
```

### 10.1.4 Water-borne disease and water pollution

| Disease | Caused by | Spread |
|---|---|---|
| Cholera | bacterium | contaminated water and food |
| Typhoid | bacterium | contaminated water and food |
| Dysentery (amoebic and bacillary) | protozoan or bacterium | contaminated water, dirty hands |
| Jaundice (hepatitis A) | virus | contaminated water and food |
| Diarrhoea and worms | many germs | unsafe water, open defecation |

**Prevention** is always the same four steps: drink boiled or filtered water;
wash hands with soap before eating and after the toilet; use a toilet and keep
the water source away from it; keep the storage pot covered.

**Sources of pollution:** untreated sewage, waste from industries, chemical
fertiliser and pesticide runoff, bathing and washing animals in the river,
solid waste and plastic dumped in the river, and open defecation. Control means
treating sewage before release, planting trees along the banks, banning the
dumping of waste in rivers, and — the cheapest of all — not letting the
pollution enter the water in the first place.

## 10.2 Cement, glass and ceramics

| Material | Made from | Property that makes it useful |
|---|---|---|
| Cement | limestone and clay, heated in a kiln and ground with gypsum | sets hard when mixed with water; binds sand and gravel into concrete |
| Concrete | cement + sand + gravel + water | strong in compression; used for foundations and pillars |
| Glass | sand (silica), soda ash and limestone, melted at high temperature | transparent, hard, does not corrode, can be moulded |
| Ceramics (clay pots, bricks, tiles) | clay, baked in a kiln | cheap, heat resistant, does not react with food |
| Plaster of Paris | gypsum heated to about 120 °C | sets quickly when mixed with water; used for casts and mouldings |

::: caution Cement setting is a chemical change
Mortar does not dry like mud; the cement reacts with water and forms new
compounds. That is why a set cement bag can never be softened back into cement,
and why a mortar that dries out too fast during setting becomes weak. Keeping
the concrete wet for a few days is not optional — it is part of what makes it
strong.
:::

```photo id="sci10/rust" caption="Rust on iron. Rusting needs both oxygen and moisture, which is why a painted or oiled surface is protected." width="64"
```

## 10.3 Plastics and polymers

A **polymer** is a very large molecule built by joining many small units.
Plastics are synthetic polymers, made mainly from petroleum.

| | Thermoplastic | Thermosetting plastic |
|---|---|---|
| On heating | softens and can be reshaped again and again | sets permanently; cannot be reshaped |
| Examples | polythene, PVC, polypropylene, nylon | bakelite, melamine |
| Uses | bags, buckets, pipes, bottles, electric wire covering | switches, plugs, handles of cookware, melamine plates |

**Harm caused by plastic.**

- It does not rot. A polythene bag stays in the soil for decades and in the
  river for longer.
- Animals and cattle swallow bags along with food and die.
- It chokes drains, which is one cause of the waterlogging in Kathmandu.
- Burning plastic releases poisonous gases; it is never safe to burn.
- Much of it ends in the ocean as microplastics, which then enter fish and so
  enter people.

**What to do:** carry a cloth or *jhola* bag; refuse the plastic bag; separate
degradable from non-degradable waste; compost the degradable part; reuse
containers; and recycle bottles and hard plastic.

## 10.4 Soap, detergent and fertiliser

### 10.4.1 How soap works

Soap is made by boiling oil or fat with an alkali. Its molecule has a long
**hydrocarbon tail** that attaches to grease and dirt and a **head** that
attaches to water. The tails bury themselves in the grease, the heads face the
water, and the dirt is lifted off the cloth and carried away in the rinse water.
This is why washing works only with rubbing and rinsing: the soap has to get
between the dirt and the cloth, and then be carried off.

| | Soap | Synthetic detergent |
|---|---|---|
| Made from | oil or fat and an alkali | petroleum products |
| In hard water | forms scum, so it does not clean well | works well; no scum |
| On the skin | milder | can be harsh |
| In water bodies | biodegrades fast | some foams are slow to biodegrade |

### 10.4.2 Fertiliser

Plants need nitrogen (N) for leaf growth, phosphorus (P) for roots, flowers and
seeds, and potassium (K) for overall strength and disease resistance. Chemical
fertilisers such as urea, DAP and potash supply these in concentrated form;
**compost** and **farmyard manure** supply them slowly along with humus.

Fertiliser increases the yield, but too much of it is carried by rain into
rivers and lakes, where it makes algae grow uncontrollably. The algae die, their
decay uses up the oxygen in the water, and fish are suffocated. Chemical
fertiliser is therefore used together with compost, in the amount the crop
actually needs.

```photo id="sci10/pet-bottles" caption="Collected plastic bottles. Most plastics are non-biodegradable, so segregation and recycling are the only real answers." width="68"
```

## 10.5 Fibre

| Natural fibre | Source | Property |
|---|---|---|
| Cotton | cotton plant | absorbs sweat, comfortable in summer |
| Jute | jute plant stem | strong, cheap; sacks and rope |
| Silk | cocoon of the silkworm | soft, lustrous, expensive |
| Wool | fleece of sheep | traps air, warm |

| Synthetic fibre | Made from | Property |
|---|---|---|
| Nylon | petroleum | strong, elastic, dries fast |
| Polyester | petroleum | wrinkle resistant, quick drying |
| Rayon | wood pulp, chemically treated | silk-like; called semi-synthetic |

Synthetic fibres are strong and cheap but do not absorb sweat, catch fire
readily and do not decompose. Mixing a natural fibre with a synthetic one — as
in terry-cot — gives comfort with strength.

## 10.6 Fuel and combustion

A **fuel** is a substance that burns in air to give heat and light. Wood,
kerosene, LPG, petrol, diesel, coal, biogas and cow-dung cakes are the fuels
used in Nepali homes.

**Combustion** needs three things at once — fuel, oxygen and heat. They are
drawn as the **fire triangle**. Removing any one of the three puts the fire out,
which is exactly what every fire-fighting method does.

```figure caption="The fire triangle. Water removes heat, a blanket or sand removes oxygen, and breaking the fuel line removes the fuel; every extinguisher is one of these three ideas."
fig, ax = plt.subplots(figsize=(4.9, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")
ax.add_patch(plt.Polygon([[5.0, 5.4], [1.4, 0.9], [8.6, 0.9]], fill=False,
                         ec=ACCENT, lw=1.8))
ax.text(5.0, 4.55, "fuel", ha="center", fontsize=8.0, color=INK,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
ax.text(2.3, 1.55, "oxygen", ha="center", fontsize=8.0, color=INK,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
ax.text(7.7, 1.55, "heat", ha="center", fontsize=8.0, color=INK,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
ax.text(5.0, 3.0, "remove any one", ha="center", fontsize=6.6, color=SERIES[1])
ax.text(5.0, 2.45, "and the fire stops", ha="center", fontsize=6.6, color=SERIES[1])
ax.text(5.0, 0.25, "every fire rule in this unit is one side of this triangle",
        ha="center", fontsize=6.3, color=MUTED)
fig.tight_layout()
```

| Kind of combustion | What happens | Example |
|---|---|---|
| Rapid | heat and light given out quickly | burning kerosene, LPG |
| Spontaneous | starts by itself at ordinary temperature | phosphorus in air; wet hay in a stack |
| Explosive | very fast, with a large volume of gas | firecrackers, a leaking LPG cylinder |

**Fire safety, in one list.**

1. Never leave a burning stove or *chulo* unattended.
2. Turn the LPG regulator off at the cylinder, not only at the burner, and keep
   the cylinder upright in a ventilated place.
3. If you smell gas, do not switch on a light or strike a match; open the doors
   and windows and turn the cylinder off.
4. Keep water and a bucket of sand near the kitchen; do not pour water on an
   electrical fire or on burning oil.
5. Never store kerosene or petrol near a fire or in a soft-drink bottle.
6. In case of a fire, get out first; call for help; never go back inside.

::: example Worked reasoning: why a wet cloth stops a chip-pan fire
**Situation.** Oil in a pan catches fire. A wet cloth is thrown over it and the
fire goes out.

**Reasoning.** The burning oil needs oxygen from the air. The wet cloth covers
the surface and cuts the oil off from the air, so the oxygen side of the fire
triangle is removed. The water in the cloth also removes heat as it turns to
steam and takes energy away, which works on the heat side as well.

**Why not water poured directly?** Water is denser than oil and sinks below it;
the water turns to steam suddenly under the hot oil and throws burning oil up
into the air, spreading the fire. Burning oil is never put out with a jet of
water: cover it, or use sand or a fire blanket.
:::

## 10.5 Waste, recycling and the three Rs

| Waste | Time to break down | Better practice |
|---|---|---|
| Vegetable peel | 2–4 weeks | compost at home or in school |
| Paper | 2–6 weeks | collect and recycle |
| Cotton cloth | 2–5 months | reuse, then use as a cleaning rag |
| Tin can | 50–100 years | wash and sell to a scrap dealer |
| Plastic bottle | 400–1,000 years | refuse single use; refill or recycle |
| Glass | effectively never | return, reuse, recycle |

**The order matters:** **refuse and reduce** first (do not take the bag at
all), then **reuse**, and only then **recycle** — recycling still costs
energy and water, which is why it is the third choice, not the first.

```figure caption="How long common waste stays in the soil. The numbers explain why a plastic bottle used for ten minutes is a poor bargain."
fig, ax = barh_ranked(["Glass (effectively never)", "Plastic bottle",
                       "Tin can", "Cotton cloth", "Paper", "Vegetable peel"],
                      [1000, 700, 75, 4, 1, 0.5], unit=" years",
                      highlight={"Plastic bottle"})
```

::: example A four-mark answer on plastic
**Question.** Why is plastic waste a serious problem, and what can a school
do about it?

**Answer.** **Problem:** most plastics are non-biodegradable and last for
centuries; burning them releases poisonous gases; discarded bags block
drains and cause local flooding; animals swallow them and die, and
microplastic enters the food chain. **What a school can do:** (i) ban
single-use bottles and bags on the premises and provide drinking water
points; (ii) separate waste into kitchen, paper-plastic and other, with
labelled bins in every corridor; (iii) compost the kitchen waste for the
school garden and sell the recyclables; (iv) run a monthly clean-up and a
"refuse the bag" campaign with the shops nearby.
:::

## Chapter summary

- Fresh water comes from rain and is stored as groundwater; springs, wells,
  tube wells and rivers are the ways we reach it.
- **Soft water** lathers easily; **hard water** contains calcium and magnesium
  salts. Temporary hardness is removed by boiling, permanent hardness is not.
- Water is purified by sedimentation, filtration, boiling, chlorination,
  distillation and solar disinfection (SODIS).
- Cholera, typhoid, dysentery and jaundice spread through contaminated water;
  boiled water, soap, toilets and covered storage prevent them.
- Cement, glass and ceramics are made from cheap minerals and are chosen for
  setting, transparency and heat resistance; cement sets by a chemical reaction.
- Plastics are synthetic polymers; thermoplastics can be reshaped and
  thermosetting plastics cannot. They do not rot, choke drains and kill
  animals when eaten, so reduce, reuse and recycle.
- Soap molecules have a grease-loving tail and a water-loving head; soap fails
  in hard water, detergent does not.
- Fertiliser supplies nitrogen, phosphorus and potassium; excess fertiliser
  pollutes water, so it is used with compost.
- Natural fibres come from plants and animals, synthetic fibres from petroleum;
  mixtures combine comfort with strength.
- Combustion needs fuel, oxygen and heat — the fire triangle. Removing any one
  puts the fire out.

## Practice questions

**Group A — Objective (1 mark each)**

1. Hard water does not lather well because it contains salts of
   <span class="marks">[1]</span>
   (a) sodium and potassium (b) calcium and magnesium (c) iron and copper
   (d) chlorine and sulphur
2. Temporary hardness of water is removed by <span class="marks">[1]</span>
   (a) filtering (b) boiling (c) decanting (d) adding sand
3. Which of these is a thermosetting plastic? <span class="marks">[1]</span>
   (a) polythene (b) PVC (c) bakelite (d) nylon
4. Which disease spreads through contaminated water?
   <span class="marks">[1]</span>
   (a) malaria (b) cholera (c) tuberculosis (d) ringworm
5. Combustion needs fuel, heat and <span class="marks">[1]</span>
   (a) nitrogen (b) oxygen (c) carbon dioxide (d) water
6. Which nutrient in fertiliser helps leaf growth? <span class="marks">[1]</span>
   (a) nitrogen (b) phosphorus (c) potassium (d) calcium

::: note Answers to Group A
**1.** (b) — the bicarbonates, sulphates and chlorides of calcium and magnesium.
**2.** (b) — boiling drives off the carbon dioxide and precipitates the
bicarbonates.
**3.** (c) — bakelite sets permanently and cannot be reshaped.
**4.** (b) — cholera is water-borne; malaria comes from a mosquito.
**5.** (b) — oxygen, from the air.
**6.** (a) — nitrogen is needed for leaves and stems.
:::

**Group B — Short answer (2 marks each)**

1. Distinguish between hard water and soft water, and give one way of removing
   each kind of hardness. <span class="marks">[2]</span>
2. Write any four methods of purifying water at home and say what each removes.
   <span class="marks">[2]</span>
3. Why is jute used for sacks and cotton for summer clothes? Answer in terms of
   the properties of the fibres. <span class="marks">[2]</span>
4. Write four fire-safety rules for a kitchen that uses LPG.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Soft water lathers easily with soap; hard water does not, because it
contains dissolved calcium and magnesium salts. Temporary hardness, caused by
bicarbonates, is removed by boiling. Permanent hardness, caused by sulphates and
chlorides, is not removed by boiling; it needs washing soda, ion exchange or
distillation.
**2.** Boiling — kills microorganisms, but not dissolved salts. Filtration
through sand, gravel and cloth or a ceramic candle — removes suspended
particles and many germs. Chlorination with bleaching powder — kills germs.
Sedimentation with alum — makes fine mud settle. Distillation — removes salts as
well as germs. SODIS, leaving a clear bottle in the sun — kills germs where fuel
is scarce.
**3.** Jute fibre is strong and cheap, and sacks have to carry heavy loads
without tearing. Cotton absorbs sweat and lets air through, which keeps the body
cool in summer; synthetic fibre would trap the sweat and feel uncomfortable.
**4.** Any four of: turn off the regulator at the cylinder as well as the burner;
keep the cylinder upright in a ventilated place; if you smell gas, do not strike
a match or switch on a light — open the windows and turn the cylinder off; never
leave a stove burning unattended; keep a bucket of water and some sand nearby;
never pour water on burning oil; never store kerosene or petrol near the stove.
:::

**Group C — Long answer (4 marks each)**

1. What are the sources of water pollution in your locality? Describe any four
   methods of purifying water for drinking and explain what each one removes.
   <span class="marks">[4]</span>
2. Explain how soap removes dirt from cloth. Describe one harmful effect each of
   plastics, chemical fertilisers and the burning of fuel, and give one habit
   that reduces each harm. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Sources.** Untreated household sewage; waste water from workshops and
industries; fertiliser and pesticide washed off the fields by rain; bathing,
washing clothes and animals in the river or pond; solid waste and plastic
dumped in or beside the water; open defecation near a source; and drawing water
with a dirty vessel. **Purification.** (i) *Sedimentation with alum* — alum
makes the fine mud particles clump together and settle, so the water becomes
clear. (ii) *Filtration* through a sand-and-gravel bed or a ceramic filter —
traps suspended particles and many bacteria; it does not remove dissolved salts
or all viruses. (iii) *Boiling* for at least three minutes — kills bacteria,
viruses and other microorganisms; it does not remove dissolved salts, and the
water must be stored covered afterwards. (iv) *Chlorination*, adding bleaching
powder in the correct amount — kills the remaining germs and protects the water
during storage. Distillation would remove salts as well, but it costs fuel.
**2.** **How soap works.** A soap molecule has a long hydrocarbon tail that
dissolves in grease and a head that dissolves in water. When soap is rubbed on
dirty cloth, the tails bury themselves in the grease and the heads face
outwards into the water, so the grease is surrounded, lifted off the cloth and
carried away with the rinse water. **Harm and remedy.** *Plastics* — they do not
decompose and cattle that swallow bags die, and they choke drains; remedy: carry
a cloth bag and refuse plastic bags, separate and recycle waste. *Chemical
fertiliser* — excess is washed into rivers, where it makes algae bloom, the
algae decay and use up the oxygen, and the fish suffocate; remedy: use compost
along with a measured amount of fertiliser. *Burning fuel* — smoke and gases
cause respiratory disease and contribute to global warming; remedy: use
improved stoves, biogas or electricity where possible, and never leave an engine
or a stove burning unnecessarily.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** Brass is an alloy of copper and
   (a) tin (b) zinc (c) nickel (d) carbon
**2.** Rusting of iron requires
   (a) oxygen only (b) moisture only (c) both oxygen and moisture (d) carbon dioxide only
**3.** Coating iron with zinc is called
   (a) galvanising (b) tinning (c) annealing (d) tempering
**4.** Stainless steel resists rusting because of
   (a) carbon (b) chromium (c) lead (d) zinc
**5.** Detergent cleans greasy cloth because its molecule has
   (a) only a water-loving end (b) only an oil-loving end (c) both a water-loving and an oil-loving end (d) neither

::: note Objective practice — answers
**1.** (b) — copper and zinc. **2.** (c) — both are needed. **3.** (a) — galvanising. **4.** (b) — chromium forms a protective oxide film. **5.** (c) — one end holds water, the other grease.
:::

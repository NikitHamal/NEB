---
subject: Science and Technology
grade: 8
unit: 10
title: Materials Used in Daily Life
hours: 0
area: Science and Technology
---

Fruits, vegetables, soaps, shampoos, sanitisers and cleaning agents all contain
acids, bases or salts. The water we drink may be soft or hard, and the vessels and
tools we use are often made of alloys rather than pure metals. This unit studies the
materials of daily life: water (its hardness, purification and pollution, including
acid rain), building and household materials (cement, glass, plastics, soap,
fertiliser, fibres and fuels), and — the main lessons of the CDC textbook — **acids,
bases and salts**, **acid rain**, **hardness of water** and **alloys**.

::: key What this unit asks of you
Define acid, base, alkali and salt; tell organic from inorganic and strong from weak
acids; give the colours of litmus, methyl orange and phenolphthalein; write the
reactions of acids with metals, carbonates and bases, and of bases with ammonium
salts; classify salts as neutral, acidic or basic; explain the causes, effects and
prevention of acid rain; define hard and soft water and the methods of removing
temporary and permanent hardness; and state the composition and uses of steel,
stainless steel, brass and bronze.
:::

## 10.1 Water: sources, hardness, purification and water-borne disease

Our water comes from rain, springs, rivers, lakes, wells (*kuwa*), stone spouts
(*dhara*) and tube wells. Surface water (rain, rivers) is usually **soft**; groundwater
(wells, tube wells) is often **hard**, because it dissolves salts from rocks.

### 10.1.1 Soft and hard water

Add two drops of liquid soap to water samples from different sources and stir
(Activity 10.13): some give plenty of lather, some very little.

::: definition Soft and hard water
**Soft water** is water that contains no dissolved salts of calcium and magnesium; it
lathers easily with soap (rain water, boiled water, most river water).
**Hard water** contains dissolved salts (bicarbonates, sulphates, chlorides) of
**calcium and magnesium**; it gives little lather with soap. **Hardness of water** is the
property of water by which it does not form lather easily with soap, because of these
dissolved salts.
:::

**Problems of hard water:** much soap is wasted; clothes washed in it become dull and
greyish because the soap forms a sticky scum; a white **scale** collects in kettles,
pipes and boilers, wasting fuel and blocking pipes.

| Temporary hardness | Permanent hardness |
|---|---|
| caused by **bicarbonates** of calcium and magnesium — Ca(HCO₃)₂, Mg(HCO₃)₂ | caused by **sulphates and chlorides** of calcium and magnesium — CaSO₄, MgCl₂ |
| removed by **boiling** or by **Clark's method** (adding lime, Ca(OH)₂) | not removed by boiling; removed by **washing soda** or the **permutit (zeolite) method** |

**Removing temporary hardness**

- *Boiling:* the soluble bicarbonate changes into insoluble carbonate, which settles:
  Ca(HCO₃)₂ --heat--> CaCO₃↓ + H₂O + CO₂↑
- *Clark's method:* a calculated amount of slaked lime is added; the insoluble carbonate
  is filtered off: Ca(HCO₃)₂ + Ca(OH)₂ → 2CaCO₃↓ + 2H₂O

**Removing permanent hardness**

- *Washing soda (sodium carbonate):* CaSO₄ + Na₂CO₃ → CaCO₃↓ + Na₂SO₄ (the precipitate
  is filtered off).
- *Permutit method:* hard water is passed through a column of **sodium zeolite** (sodium
  aluminium silicate) packed between layers of sand and gravel. The calcium and magnesium
  ions are held by the zeolite and sodium ions go into the water, which comes out soft:
  Na₂Z + CaSO₄ → CaZ + Na₂SO₄. The used zeolite is renewed by washing it with strong salt
  solution.

```figure caption="Permutit (zeolite) method: hard water enters at the top, calcium and magnesium are exchanged for sodium in the zeolite layer, and soft water flows out at the bottom."
fig, ax = plt.subplots(figsize=(4.6, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 7.4); ax.axis("off")
ax.add_patch(plt.Rectangle((2.0, 0.9), 3.0, 5.6, fc="white", ec=INK, lw=1.4))
layers = [(0.9, 1.0, "#9e9e9e", "gravel"), (1.9, 1.0, "#e3cf9b", "sand"),
          (2.9, 1.8, "#c9dfc0", "sodium zeolite"), (4.7, 1.0, "#e3cf9b", "sand")]
for y, h, c, name in layers:
    ax.add_patch(plt.Rectangle((2.0, y), 3.0, h, fc=c, ec=MUTED, lw=0.6))
    ax.plot([5.0, 5.6], [y + h / 2, y + h / 2], color=MUTED, lw=0.7)
    ax.text(5.7, y + h / 2, name, va="center", fontsize=7.8, color=INK)
ax.annotate("", xy=(3.5, 6.0), xytext=(3.5, 7.2), arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.5))
ax.text(3.9, 6.95, "hard water in", fontsize=7.8, color=SERIES[1])
ax.plot([3.5, 3.5], [0.9, 0.5], color=INK, lw=2)
ax.annotate("", xy=(5.6, 0.35), xytext=(3.5, 0.35), arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5))
ax.text(5.7, 0.35, "soft water out", va="center", fontsize=7.8, color=ACCENT)
fig.tight_layout()
```

::: example Advice for Roshan and Riya (textbook questions)
**Roshan** gets little lather with well water. *Advice:* boil the water first (removes
temporary hardness) or add a little washing soda, and let the precipitate settle;
alternatively use rain water or a detergent, which works even in hard water.

**Riya's** white clothes turn dull with tube-well water. *Reason:* the calcium and
magnesium salts form an insoluble scum with soap that sticks to the cloth. *Advice:* soften
the water with washing soda (or boiling), or use detergent, and rinse well.
:::

### 10.1.2 Purification of water

| Method | What it removes |
|---|---|
| sedimentation (with alum) and decantation | mud and suspended particles |
| filtration (sand, ceramic candle filter, cloth) | suspended dirt and many germs |
| boiling for several minutes | germs (not dissolved salts) |
| chlorination (bleaching powder, chlorine tablets) | germs |
| SODIS — clear bottles in strong sun for about six hours | germs, where fuel is scarce |
| distillation | dissolved salts and germs — gives pure water |

### 10.1.3 Water-borne diseases

**Cholera, typhoid, diarrhoea, dysentery, jaundice (hepatitis A)** and worm infections
spread through water and food contaminated by faeces. *Prevention:* drink boiled or
filtered water; wash hands with soap before eating and after using the toilet; use
toilets and keep water sources away from them; cover stored water.

## 10.2 Water pollution and its control; acid rain

**Sources of water pollution:** untreated sewage, industrial waste, chemical fertilisers
and pesticides washed from fields, dumping of solid waste and plastic in rivers, washing
clothes and animals in rivers, and acid rain. Excess fertiliser makes algae grow fast; when
the algae die and decay they use up the dissolved oxygen and fish die.
**Control:** treat sewage and factory waste before release; never dump waste in rivers; use
fertilisers and pesticides carefully; plant trees along river banks; build toilets.

### 10.2.1 Acid rain

::: definition Acid rain
**Acid rain** is rain that has become acidic because acids formed in the atmosphere
(mainly **sulphuric acid** and **nitric acid**) have mixed with it.
:::

Normal rain is slightly acidic (about pH 5.6–6) because carbon dioxide dissolves in it to
form weak **carbonic acid**; this is not very harmful. Rain with strong acids has a lower
pH and is harmful.

**How the acids form.** *Natural sources:* volcanic eruptions and decay of plants and
animals give oxides of sulphur and nitrogen. *Human sources (the main cause):* burning
coal, petrol and diesel in vehicles, factories and brick kilns. These oxides react with
water vapour in the air: sulphur dioxide → sulphuric acid; nitrogen oxides → nitric acid.

```figure caption="How acid rain forms."
fig, ax = flow([("Fuel burnt", "vehicles,\nfactories"),
                ("SO₂, NOₓ", "go into\nthe air"),
                ("Acids form", "H₂SO₄,\nHNO₃"),
                ("Acid rain", "falls on land\nand water")],
               figsize=(5.1, 2.3))
```

**Effects:** rivers, lakes and ponds become acidic, harming fish and water life; leaves are
damaged and soil fertility falls, so crop production declines; forests may be destroyed;
temples, monuments and statues of marble and metal corrode (the Taj Mahal in India is a
famous example of marble damage).
**Prevention:** use less fossil fuel; use renewable energy (hydroelectricity, solar);
control vehicle and factory smoke; set up industries away from settlements.
**For farmland already affected:** add lime or wood ash (both are bases) to neutralise the
soil acidity, use compost, and grow crops that tolerate acidic soil.

## 10.3 Cement, glass and ceramics

| Material | Raw materials | Useful property and use |
|---|---|---|
| Cement | limestone and clay heated in a kiln, ground with a little gypsum | sets hard with water (a chemical change); binds sand and gravel into concrete for buildings, bridges, dams |
| Glass | sand (silica), soda ash and limestone melted together | transparent, hard, does not rust; windows, bottles, lenses |
| Ceramics | clay shaped and baked in a kiln | hard, heat resistant, does not react with food; bricks, tiles, pottery, cups |

::: caution Curing concrete
Cement does not simply dry; it reacts with water. Fresh concrete is kept wet (cured) for
several days — if it dries too quickly it becomes weak.
:::

## 10.4 Plastics and polymers: uses and environmental harm

A **polymer** is a giant molecule made by joining many small units. **Plastics** are
synthetic polymers made mainly from petroleum. **Thermoplastics** (polythene, PVC, nylon)
soften on heating and can be reshaped; **thermosetting plastics** (bakelite, melamine) set
permanently and are used for switches and pan handles.
**Harm:** plastics are **non-biodegradable** — they stay in soil and water for many years;
they block drains, choke animals that swallow them, form microplastics in rivers, and give
poisonous gases when burnt. **What to do:** reduce (use cloth bags), reuse, recycle, and
separate waste at home.

```photo id="sci10/pet-bottles" caption="Collected plastic bottles. Most plastics are non-biodegradable, so reducing, reusing and recycling are the only real answers." width="62"
```

## 10.5 Soap, detergent and fertiliser

**Soap** is made by boiling oil or fat with an alkali (sodium hydroxide). A soap molecule has
a long tail that holds grease and a head that holds water, so it lifts oily dirt off cloth.
**Detergents** are made from petroleum products; they work well even in **hard water**, but
some are slow to break down in rivers.

**Fertilisers** supply nitrogen (N, for leaves), phosphorus (P, for roots, flowers, seeds)
and potassium (K, for strength). Chemical fertilisers (urea, DAP, potash) act quickly;
**compost** and farmyard manure release nutrients slowly and improve the soil. Overuse of
chemical fertiliser harms soil and pollutes water.

## 10.6 Fibre: natural and synthetic

| Natural fibres | Synthetic fibres |
|---|---|
| from plants or animals: cotton, jute, *allo* (Himalayan nettle), silk, wool | made from petroleum chemicals: nylon, polyester, acrylic |
| absorb sweat, comfortable | strong, cheap, quick drying, do not absorb sweat |
| biodegradable | non-biodegradable; melt and stick to skin in fire |

## 10.7 Fuel and combustion; fire safety

A **fuel** burns in air to give heat (wood, kerosene, LPG, petrol, diesel, coal, biogas).
**Combustion** needs three things together — **fuel, oxygen and heat** (the fire triangle).
Removing any one puts out the fire: water removes heat; sand, a fire blanket or a damp
cloth cuts off oxygen; closing the gas valve removes the fuel.
**Fire safety:** never leave a stove burning unattended; turn off the LPG regulator at the
cylinder; if gas leaks, do not light a match or switch on a light — open doors and windows;
never pour water on burning oil or an electrical fire; keep a bucket of sand near the kitchen.
Fire extinguishers often use **sodium bicarbonate**, which releases carbon dioxide.

## 10.8 Acids, bases and salts in daily life

### 10.8.1 Acids

::: definition Acid
An **acid** is a substance that gives **hydrogen ions (H⁺)** when dissolved in water.
HCl → H⁺ + Cl⁻
:::

| Organic acids | Inorganic (mineral) acids |
|---|---|
| found naturally in plants and animals | prepared in the laboratory from minerals |
| usually **weak** and many are edible | usually **strong**, corrosive, not edible |
| citric acid (lemon), acetic acid (vinegar), lactic acid (curd, milk), oxalic acid (tomato), tartaric acid (tamarind, grapes), formic acid (ant sting, nettle) | hydrochloric acid (HCl), sulphuric acid (H₂SO₄), nitric acid (HNO₃), carbonic acid |

A **strong acid** gives many H⁺ ions in water (HCl, H₂SO₄, HNO₃); a **weak acid** gives few
(citric, acetic). That is why sulphuric acid burns cloth but lemon juice does not. The
hydrochloric acid in our stomach is an inorganic acid, though it is made by the body.

**Physical properties:** sour taste; soluble in water; turn **blue litmus red** (red litmus
stays red); turn **methyl orange red**; **phenolphthalein stays colourless**.

**Chemical properties**

1. *With metals* — give a salt and **hydrogen** (the gas burns with a 'pop'):
   Mg + 2HCl → MgCl₂ + H₂↑ (zinc also gives bubbles of hydrogen in dilute acid).
2. *With metal carbonates* — give a salt, water and **carbon dioxide** (turns lime water milky):
   CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂↑
3. *With bases* — give a salt and water (**neutralisation**):
   HCl + NaOH → NaCl + H₂O; H₂SO₄ + 2KOH → K₂SO₄ + 2H₂O

| Acid | Uses |
|---|---|
| citric acid | preserving food, giving a sour taste |
| ascorbic acid | vitamin C in medicines |
| acetic acid (vinegar) | pickles (Activity 10.7: radish in vinegar stays fresh) |
| tartaric acid | baking powder |
| hydrochloric acid | digestion in the stomach; cleaning toilets; making PVC |
| nitric acid | nitrogen fertilisers, explosives |
| sulphuric acid | car batteries, fertilisers, dyes, detergents, artificial silk |

### 10.8.2 Bases and alkalis

::: definition Base and alkali
A **base** is a metal oxide or hydroxide (Na₂O, NaOH, KOH, MgO, Ca(OH)₂). A base that
**dissolves in water** is an **alkali**; alkalis give **hydroxide ions (OH⁻)** in water:
NaOH → Na⁺ + OH⁻.
:::

All alkalis are bases, but not all bases are alkalis (e.g. copper oxide does not dissolve).
**Strong bases** (NaOH, KOH) give many OH⁻ ions; **weak bases** (ammonium hydroxide) give few.

**Physical properties** (Activity 10.8 with ash water): bitter taste; soapy, slippery feel;
turn **red litmus blue**; turn **methyl orange yellow**; turn **phenolphthalein pink**.

**Chemical properties:** with acids they form salt and water (neutralisation); with ammonium
salts they give **ammonia** gas (which turns moist red litmus blue):
(NH₄)₂SO₄ + 2NaOH → Na₂SO₄ + 2NH₃↑ + 2H₂O

| Base | Uses |
|---|---|
| calcium hydroxide (slaked lime) | whitewashing, bleaching powder, reducing soil acidity |
| magnesium hydroxide | antacid (milk of magnesia) for hyperacidity (gastritis) |
| sodium hydroxide (caustic soda) | soap, paper, cloth, refining petroleum |
| ammonium hydroxide | laboratory reagent, fertilisers, rayon, plastics, dyes |

Ash contains alkaline compounds of potassium and calcium, so farmers spread ash to reduce
soil acidity. A gastritis patient takes magnesium hydroxide because this base neutralises
the excess hydrochloric acid in the stomach.

### 10.8.3 Salts

::: definition Salt
A **salt** is the compound formed, together with water, when an acid reacts with a base.
:::

| Type | Formed from | Example |
|---|---|---|
| Neutral salt | strong acid + strong base (or weak + weak) | sodium chloride, NaCl |
| Acidic salt | strong acid + weak base | ammonium chloride, NH₄Cl (from HCl + NH₄OH) |
| Basic salt | strong base + weak acid | sodium carbonate, Na₂CO₃ (from NaOH + H₂CO₃) |

**Properties:** most are tasteless (table salt is salty, some are bitter); most dissolve in
water; white or colourless, some coloured (copper sulphate is blue); high melting and boiling
points; neutral salts do not change indicators. In water they split into ions:
NaCl → Na⁺ + Cl⁻.

**Reactions:** with acids — H₂SO₄ + 2NaCl → Na₂SO₄ + 2HCl; with bases —
2NH₄Cl + Ca(OH)₂ → CaCl₂ + 2NH₃ + 2H₂O; **displacement** — a more reactive metal pushes a less
reactive metal out of its salt (Activity 10.11: iron in blue copper sulphate solution turns
reddish-brown with copper, and the solution turns pale green):
Fe + CuSO₄ → FeSO₄ + Cu

| Salt | Uses |
|---|---|
| sodium chloride (common salt) | flavouring and preserving food; making NaOH, washing soda, soap |
| sodium carbonate (washing soda) | removing permanent hardness; making glass, paper, soap |
| sodium bicarbonate (baking soda) | baking powder, antacid, fire extinguishers |

| Indicator | Acid | Base | Neutral salt solution |
|---|---|---|---|
| blue litmus | red | blue | no change |
| red litmus | red | blue | no change |
| methyl orange | red | yellow | orange (no change) |
| phenolphthalein | colourless | pink | colourless |

::: example Identifying three unknown liquids
**Problem.** Three colourless liquids P, Q and R are tested. P turns blue litmus red and
gives bubbles with a marble chip (CaCO₃). Q turns phenolphthalein pink. R changes neither
litmus paper. Identify each and write the reaction of P with the marble chip if P is
dilute hydrochloric acid.

**Solution.** P is an **acid** (blue litmus → red; carbonate gives CO₂). Q is a **base
(alkali)** (phenolphthalein pink). R is **neutral** — water or a neutral salt solution such
as common salt.
CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂↑ (the gas turns lime water milky).
:::

::: example Which hardness, and how to remove it?
**Problem.** Sample X lathers well after boiling. Sample Y still does not lather after
boiling, but lathers after washing soda is added. Name the hardness in each.

**Solution.** X has **temporary hardness** (calcium/magnesium bicarbonates), removed by
boiling: Ca(HCO₃)₂ → CaCO₃ + H₂O + CO₂. Y has **permanent hardness** (sulphates or
chlorides), not removed by boiling but removed by washing soda:
CaSO₄ + Na₂CO₃ → CaCO₃ + Na₂SO₄.
:::

## 10.9 Alloys

Ramila's mother wanted a 24-carat gold bangle, but the goldsmith advised 22 carat for daily
wear. **24-carat gold is pure** and soft; **22-carat gold** is mixed with a little copper or
silver, which makes it harder, so it does not bend or wear away easily.

::: definition Alloy
An **alloy** is a homogeneous mixture made by melting a metal with other metals or with a
non-metal, to improve its properties.
:::

**Properties of alloys:** harder and stronger than the pure metal, but less malleable and
ductile; resist rusting and corrosion better; have a different melting point and colour
from their metals; generally have better properties for use. *Example:* aluminium is light
but soft; **duralumin** (aluminium with copper, manganese and magnesium) is light and strong
and is used for aircraft bodies.

| Alloy | Composition | Uses |
|---|---|---|
| Steel | iron + a little carbon | buildings, bridges, railings, tools — much harder and stronger than iron |
| Stainless steel | iron + chromium + nickel (+ a little carbon) | kitchen utensils, surgical instruments — does not rust |
| Brass | copper + zinc | *puja* items, *gagri*, idols, nuts and bolts, plumbing fittings |
| Bronze | copper + tin | plates, bowls, tumblers, medals, coins, statues, bells |

Steel and stainless steel are preferred to pure iron for kitchen utensils because pure iron
is soft and rusts, while stainless steel is hard, shiny and rust-free.

## Chapter summary

- Hard water has Ca and Mg salts. Temporary (bicarbonates): boiling, Clark's method.
  Permanent (sulphates, chlorides): washing soda, permutit.
- Water is purified by sedimentation, filtration, boiling, chlorination, SODIS, distillation.
- Acid rain: SO₂ and NOₓ from burning fuels form H₂SO₄ and HNO₃; harms water life, crops,
  forests and monuments.
- Acid gives H⁺ (sour, blue litmus → red, methyl orange red, phenolphthalein colourless).
  Base/alkali gives OH⁻ (bitter, soapy, red litmus → blue, methyl orange yellow,
  phenolphthalein pink).
- Acid + metal → salt + H₂; acid + carbonate → salt + H₂O + CO₂; acid + base → salt + water.
- Salts are neutral (NaCl), acidic (NH₄Cl) or basic (Na₂CO₃).
- Alloys: steel (Fe + C), stainless steel (Fe + Cr + Ni), brass (Cu + Zn), bronze (Cu + Sn).

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Textbook exercises.)*

1. A property of an acid is <span class="marks">[1]</span>
   (a) bitter (b) slippery (c) sour (d) colourless
2. Which turns red litmus blue? <span class="marks">[1]</span>
   (a) curd (b) tomato (c) cola drink (d) soapy shampoo
3. Bubbles come out as soon as zinc is put in a liquid. The liquid is <span class="marks">[1]</span>
   (a) water (b) an acid (c) a base (d) a salt solution
4. Ash is used to reduce soil acidity because ash is <span class="marks">[1]</span>
   (a) cheap (b) found at home (c) alkaline (d) a salt
5. Which salt is used in fire extinguishers? <span class="marks">[1]</span>
   (a) sodium carbonate (b) potassium carbonate (c) sodium bicarbonate (d) potassium sulphate
6. Hard water contains <span class="marks">[1]</span>
   (a) magnesium sulphate (b) magnesium oxide (c) magnesium nitrate (d) magnesium sulphide
7. Permanent hardness is removed by <span class="marks">[1]</span>
   (a) boiling (b) Clark's method (c) the permutit method (d) calcium hydroxide
8. Which water has the least hardness? <span class="marks">[1]</span>
   (a) rain water (b) well water (c) tube-well water (d) river water
9. Alloys are used more than pure metals because <span class="marks">[1]</span>
   (a) they are cheaper (b) their properties are improved (c) they are easily available (d) they are good for health
10. Brass is made by mixing <span class="marks">[1]</span>
   (a) copper and zinc (b) copper and tin (c) copper and carbon (d) copper and nickel
11. Adding a little carbon to iron to make steel makes it <span class="marks">[1]</span>
   (a) softer (b) harder and stronger (c) liquid (d) non-magnetic
12. Copper mixed with tin forms <span class="marks">[1]</span>
   (a) steel (b) stainless steel (c) brass (d) bronze
13. Which statement is true? <span class="marks">[1]</span>
   (a) an alloy is harder than its metal (b) an alloy is more flexible (c) an alloy is duller (d) an alloy is more ductile

::: note Answers to Group A
**1.** (c). **2.** (d) — soap-based shampoo is basic; the others are acidic. **3.** (b) — the gas is hydrogen. **4.** (c). **5.** (c) — it gives CO₂. **6.** (a). **7.** (c). **8.** (a). **9.** (b). **10.** (a). **11.** (b). **12.** (d). **13.** (a).
:::

**Group B — Short answer (2 marks each)**

1. Differentiate: (a) organic and inorganic acid (b) strong and weak acid (c) base and alkali. <span class="marks">[3]</span>
2. Give reasons: (a) Rain water is generally acidic. (b) Ammonium chloride is an acidic salt. (c) Sulphuric acid corrodes cloth but lemon juice does not. (d) Gastritis patients are relieved by magnesium hydroxide. <span class="marks">[4]</span>
3. Show in a table the action of acids, bases and salts on litmus, methyl orange and phenolphthalein. <span class="marks">[3]</span>
4. Sample A gives red with methyl orange, red with litmus and colour X with phenolphthalein; sample B gives colour Y with methyl orange, blue with litmus and pink with phenolphthalein. (i) Name X and Y. (ii) Which sample gives CO₂ with calcium carbonate? <span class="marks">[2]</span>
5. Differentiate: (a) soft and hard water (b) temporary and permanent hardness (c) Clark's method and permutit method (d) pure metal and alloy (e) steel and stainless steel. <span class="marks">[5]</span>
6. Give reasons: (a) Steel is used more than iron for kitchen utensils. (b) Rain water gives more lather with soap. (c) Well water is hard. (d) The use of alloys is increasing. <span class="marks">[4]</span>
7. Rama won a bronze medal. Which metals is it made of? Name the metals in steel, stainless steel and brass. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** (a) See the table in 10.8.1. (b) A strong acid gives many H⁺ ions in water (HCl); a weak acid gives few (acetic acid). (c) A base is any metal oxide or hydroxide; an alkali is a base that dissolves in water and gives OH⁻ ions (NaOH). All alkalis are bases, not all bases are alkalis.
**2.** (a) Carbon dioxide in the air dissolves in rain to form weak carbonic acid. (b) It is formed from a strong acid (HCl) and a weak base (NH₄OH). (c) Sulphuric acid is a strong acid giving many H⁺ ions; citric acid in lemon is a weak organic acid. (d) Mg(OH)₂ is a mild base that neutralises excess stomach acid.
**3.** See the indicator table in 10.8.3.
**4.** (i) X = colourless (A is an acid); Y = yellow (B is a base). (ii) A, the acid.
**5.** (a) Soft water has no Ca/Mg salts and lathers easily; hard water has them and lathers poorly. (b) See the table in 10.1.1. (c) Clark's method adds lime to remove temporary hardness by precipitating carbonate; the permutit method passes water through sodium zeolite to remove permanent hardness by exchanging Ca/Mg for Na. (d) A pure metal has one kind of atom and is usually softer; an alloy is a mixture with improved hardness and resistance to corrosion. (e) Steel is iron + carbon and can rust; stainless steel also has chromium and nickel and does not rust.
**6.** (a) Steel (stainless) is harder, stronger and does not rust, while iron is soft and rusts. (b) It contains no calcium or magnesium salts. (c) Underground water dissolves calcium and magnesium salts from rocks. (d) Alloys are harder, stronger, more corrosion-resistant and can be made for special uses.
**7.** Bronze: copper and tin. Steel: iron and carbon; stainless steel: iron, chromium and nickel; brass: copper and zinc.
:::

**Group C — Long answer (4 marks each)**

1. What is an acid? Write three chemical properties of acids with balanced equations. <span class="marks">[4]</span>
2. Define base. Write two properties of bases and the uses of three bases. <span class="marks">[4]</span>
3. What is a salt? Explain neutral, acidic and basic salts with examples, and write the displacement reaction of iron with copper sulphate. <span class="marks">[4]</span>
4. List the causes of acid rain. How is it harmful? How can it be prevented? Suggest how farmers can improve crop production in soil damaged by acid rain. <span class="marks">[4]</span>
5. Define hardness of water and give its causes. Describe the permutit method with a diagram. <span class="marks">[4]</span>
6. What is an alloy? Why are alloys becoming popular? Write the composition and two uses of four alloys. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** A substance that gives H⁺ ions in water. Mg + 2HCl → MgCl₂ + H₂; CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂; HCl + NaOH → NaCl + H₂O.
**2.** A metal oxide or hydroxide; soluble bases (alkalis) give OH⁻ ions. Properties: turn red litmus blue and phenolphthalein pink; react with acids to give salt and water; with ammonium salts give ammonia. Uses: Ca(OH)₂ — whitewash and reducing soil acidity; Mg(OH)₂ — antacid; NaOH — soap and paper.
**3.** A compound formed with water when an acid reacts with a base. Neutral: NaCl (HCl + NaOH); acidic: NH₄Cl (HCl + NH₄OH); basic: Na₂CO₃ (NaOH + H₂CO₃). Fe + CuSO₄ → FeSO₄ + Cu — iron is more reactive and displaces copper.
**4.** Causes: oxides of sulphur and nitrogen from burning fossil fuels in vehicles, factories and kilns (and volcanoes) form sulphuric and nitric acids in the air. Harm: acidic rivers and lakes kill fish; leaves and soil are damaged and crops fall; forests die; monuments and statues corrode. Prevention: less fossil fuel, renewable energy, smoke control, industries away from settlements. For farmers: add lime or ash to neutralise soil acidity, add compost, test soil pH, grow acid-tolerant crops.
**5.** The property of water of not lathering easily with soap, due to dissolved salts of calcium and magnesium (bicarbonates for temporary, sulphates and chlorides for permanent hardness). Permutit method: see the figure and text in 10.1.1 — hard water flows through sodium zeolite; Na₂Z + CaSO₄ → CaZ + Na₂SO₄; soft water comes out.
**6.** A homogeneous mixture of a metal with other metals or a non-metal. Popular because they are harder, stronger, resist rust and can be made for special purposes. Steel (Fe + C): buildings, bridges. Stainless steel (Fe + Cr + Ni): utensils, surgical tools. Brass (Cu + Zn): *gagri*, idols, fittings. Bronze (Cu + Sn): plates, medals, statues.
:::

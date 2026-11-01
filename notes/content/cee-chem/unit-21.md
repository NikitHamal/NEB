---
subject: Chemistry
grade: CEE
unit: 21
title: Applied Chemistry and Chemistry in Service to Mankind
hours: 3
area: Applied Chemistry
---

Applied chemistry asks what happens when a balanced equation has to survive a factory, a
market and the environment. This **3-question** chapter is a rapid tour with a common logic:
raw materials are prepared, converted, separated, finished and checked; the best process is
not merely the one with the prettiest equation but the one giving safe, pure product at a
defensible cost in energy, materials and pollution. The same thinking explains familiar
materials — cement, paper, plastics, dyes, medicines and fertilizers — and the quiet
chemistry of colloids, osmosis and buffers in daily life.

::: key What the paper asks from this chapter
- A chemical plant runs: raw-material preparation → reaction/conversion → separation and purification → finishing/formulation → packaging, with quality control, utilities, recycle and waste treatment wrapped around every stage.
- **Batch processing** (charge–react–discharge–clean) is flexible and traceable, suited to small-volume/many-product work such as pharmaceuticals. **Continuous processing** is steady, automated and economical at huge volume (ammonia, sulfuric acid, cement), but capital-heavy and inflexible.
- Profit and sustainability turn on feedstock/energy price, yield and selectivity, catalyst life, recycle of unconverted reactants, co-product value, location, maintenance and pollution control. Green chemistry prefers prevention, atom economy, catalysis, safer solvents and energy efficiency over end-of-pipe cleanup.
- Cement: limestone + clay are calcined and clinkered near 1450 °C; alite (C₃S) gives early strength, belite (C₂S) later strength. A little gypsum in grinding retards setting. Calcination itself releases CO₂: 1000 kg CaCO₃ → 440 kg CO₂.
- Paper: fibres are liberated by mechanical pulping (high yield, lignin remains, paper yellows) or kraft chemical pulping (NaOH + Na₂S; strong fibres; black liquor is burned to recover energy/chemicals), then washed, bleached, formed on a wire, pressed and dried.
- Heavy chemicals in one line each: **Haber** NH₃ (Fe catalyst, recycle); **Ostwald** HNO₃ (Pt–Rh gauze oxidizes NH₃); **Contact** H₂SO₄ (V₂O₅; SO₃ absorbed into oleum); **chlor-alkali** NaOH/Cl₂/H₂ (diaphragm historically, membrane cells now preferred); **Solvay** Na₂CO₃ (precipitate NaHCO₃, calcine); **urea** from NH₃ + CO₂ through ammonium carbamate (46% N).
- Addition polymers grow by chain addition with no small by-product (polythene, PVC, polystyrene, Teflon). Condensation polymers eliminate a small molecule (nylon-6,6, PET, Bakelite). Thermoplastics soften reversibly; cross-linked thermosets do not. Vulcanization cross-links rubber with sulfur.
- A dye needs a **chromophore** (for example –N=N– in azo dyes) and usually an **auxochrome** (–OH, –NH₂, –SO₃H) for solubility/fibre binding. Drugs are classified by action (analgesic, antibiotic, antacid…); antibiotics act on bacteria, not viruses, and misuse selects resistance.
- Fertilizer labels give N–P₂O₅–K₂O percentages: urea 46-0-0, DAP about 18-46-0, muriate of potash about 0-0-60. Persistent fat-soluble pesticides such as DDT biomagnify; integrated pest management reduces chemical load.
- Colloids (roughly 1–1000 nm dispersed particles) show Tyndall scattering and Brownian motion: milk (emulsion), fog (aerosol), jelly (gel), blood (sol). Alum coagulates colloidal clay in water treatment.
- Osmotic pressure follows $\pi = iCRT$. About 0.9% NaCl is isotonic with blood; reverse osmosis applies pressure greater than π to desalinate water. The blood buffer is chiefly H₂CO₃/HCO₃⁻, holding pH near 7.4.
- Radioisotopes: Tc-99m and F-18 for diagnostic imaging; I-131 for thyroid therapy; Co-60 for radiotherapy/sterilization and industrial radiography; Am-241 in smoke detectors. Protection is time, distance and shielding (ALARA).
:::

## 21.1 The chemical industry: stages of production, economics and plant management, batch and continuous processing, environmental effects and their control

### From flask to flowsheet

A commercial process is usually drawn as a chain of **unit operations and unit processes**:

1. **Feed preparation** — crushing, dissolving, filtering, drying, preheating and purifying raw
   materials so the reactor receives a predictable diet.
2. **Conversion** — the chemical reaction(s), controlled for temperature, pressure, residence
   time and catalyst contact. Conversion per pass may deliberately be modest (Haber) if
   unreacted feed can be recycled cheaply.
3. **Separation and purification** — distillation, absorption, extraction, crystallization,
   filtration and drying. In many plants this block costs more energy than the reactor.
4. **Finishing** — blending, granulation/prilling, polymerization shaping, tableting or
   dilution to specification.
5. **Packaging, storage and dispatch**, with batch/lot traceability.

Around the chain sit utilities (steam, cooling water, compressed air, refrigeration),
analytical quality control, recycle loops, flare/relief systems and effluent treatment.
Scale-up is not just a bigger flask: surface area per volume falls, hot spots grow, mixing
and heat removal become limiting, so pilot-plant data and hazard studies (for example HAZOP)
precede a full plant.

```figure caption="The skeleton of a continuous chemical plant. Recycle returns unconverted feed instead of demanding impossible one-pass conversion; separation and waste treatment are core production stages, not afterthoughts."
fig, ax = plt.subplots(figsize=(5.2,2.8))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6)
boxes = [(0.3,3.2,1.7,1.1,'raw material\npreparation'),(2.5,3.2,1.6,1.1,'reactor\n(catalyst)'),(4.6,3.2,1.8,1.1,'separation &\npurification'),(6.9,3.2,1.5,1.1,'finishing &\npackaging'),(8.8,3.2,1.0,1.1,'product')]
for x,y,w,h,lab in boxes:
    ax.fill([x,x+w,x+w,x],[y,y,y+h,y+h], color='#BFD7EA', ec=INK, lw=1.0, zorder=2)
    ax.text(x+w/2,y+h/2,lab,ha='center',va='center',fontsize=7.2,zorder=3)
for x1,x2 in [(2.0,2.5),(4.1,4.6),(6.4,6.9),(8.4,8.8)]:
    ax.annotate('',xy=(x2,3.75),xytext=(x1,3.75),arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.2))
ax.annotate('',xy=(3.3,4.85),xytext=(5.5,4.85),arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.4))
ax.plot([5.5,5.5,3.3],[4.3,4.85,4.85],color=ACCENT,lw=1.4)
ax.plot([3.3,3.3],[4.85,4.3],color=ACCENT,lw=1.4)
ax.text(4.4,5.08,'recycle unconverted feed',ha='center',fontsize=8,color=ACCENT)
ax.annotate('',xy=(5.5,1.75),xytext=(5.5,3.2),arrowprops=dict(arrowstyle='-|>',color='#A8271F',lw=1.2))
ax.fill([3.8,7.2,7.2,3.8],[0.75,0.75,1.75,1.75], color='#F3C98B', ec=INK, lw=1.0)
ax.text(5.5,1.25,'waste treatment\n& recovery',ha='center',va='center',fontsize=7.6)
ax.text(1.1,1.25,'utilities + QC\nat every stage',ha='center',va='center',fontsize=8,color=MUTED)
```

### Batch versus continuous, and what the manager optimizes

| Feature | Batch | Continuous |
|---|---|---|
| Operation | Load, react, unload, clean; one lot at a time | Feed and product flow steadily |
| Best for | Low volume, many grades, strict lot identity (medicines, dyes, speciality chemicals) | Very large tonnage of one specification (NH₃, H₂SO₄, cement, refining) |
| Strengths | Flexible scheduling/equipment, easier containment of a bad lot | Labour/energy efficiency, steady quality, heat integration, automation |
| Weaknesses | Downtime, cleaning waste, batch-to-batch variation | High capital cost, difficult start-up/shutdown, poor flexibility |

Plant economics is applied stoichiometry with prices attached. **Yield** and **selectivity**
decide how much feed becomes saleable product rather than by-product; catalyst life and
energy integration decide operating cost; capital is repaid over years, so utilization
matters. A valuable co-product can rescue a process (acetone in the cumene route to phenol,
Ch. 18), while a waste with no outlet can kill it (CaCl₂ brine from Solvay plants). Site
choice balances raw material, water/energy, labour, market transport and environmental
capacity. Good plant management is therefore chemistry plus preventive maintenance,
instrumentation, inventory control, safety culture and documented quality systems.

### Environmental effects and control

Typical burdens are acid gases (SO₂/NOₓ), particulates, volatile organic compounds and
greenhouse gases to air; oxygen-demanding, acidic, saline or metal-bearing effluent to
water; and sludges/ash/spent catalyst as solids. Control follows a hierarchy:

- **Prevent/substitute:** choose catalytic, atom-economical routes; replace mercury cells by
  membrane cells; design out persistent products.
- **Recover/recycle:** recycle unconverted reactants and solvents, burn pulping black liquor
  for energy and chemical recovery, use waste heat.
- **Treat at the boundary:** electrostatic precipitators/bag filters for dust, lime scrubbers
  for SO₂, selective catalytic reduction for NOₓ, neutralization and biological oxidation for
  effluent, secure disposal of hazardous residues.
- **Monitor and account:** continuous emission monitoring, environmental impact assessment
  before construction, and increasingly carbon capture or low-carbon hydrogen for the
  hardest sectors (cement, ammonia, steel).

::: example Worked example 21.1 — the CO₂ locked inside limestone
**Problem.** A cement kiln calcines 1000 kg of pure CaCO₃. What mass of process CO₂ is
released before any fuel is counted? (CaCO₃ = 100 g mol⁻¹, CO₂ = 44 g mol⁻¹.)

**Solution.** CaCO₃ → CaO + CO₂ is 1:1 in moles. Mass of CO₂ = 1000 × 44/100 = **440 kg**.
That is why cement decarbonization cannot be solved by clean fuel alone: nearly half a
tonne of CO₂ per tonne of limestone is chemistry, so clinker substitution and carbon
capture matter as much as kiln fuel.
:::


```figure caption="The contact process in four frames: sulphur burns to sulphur dioxide, the vanadium pentoxide catalyst oxidises it to the trioxide at 450 degrees, the trioxide dissolves into concentrated acid as oleum, and careful dilution of the oleum delivers the strong acid without mist."
flow([("burn S", "S + O2 -> SO2"),
      ("oxidise", "2SO2+O2 V2O5\n450 C"),
      ("absorb", "SO3 into H2SO4\nmakes oleum"),
      ("dilute", "oleum + water\nconc. acid")], figsize=(5.2, 2.15))
```

::: example Urea's nitrogen, by the label
**Problem.** Fertiliser sacks proclaim urea CO(NH₂)₂ as 46 % nitrogen.
Verify the claim from the formula (C 12, O 16, N 14, H 1), and state why
urea outranks ammonium sulphate as a nitrogen source.
**Solution.** Molar mass = 12 + 16 + 2 × (14 + 2) = **60 g/mol**; the two
nitrogens weigh **28 g**, so the mass fraction is 28/60 = 0.4667, i.e.
**46.7 %**, labelled 46 % — the richest solid nitrogen fertiliser in
common use, against ammonium sulphate's 21 %, and it leaves no acid
residue in the soil the way the sulphate does.
:::
## 21.2 Cement, paper and pulp; the six heavy-chemical processes

### Portland cement

The raw mix is mainly **limestone** (CaCO₃) with **clay/shale** supplying SiO₂, Al₂O₃ and
Fe₂O₃, corrected with sand or iron ore where needed. In the modern dry process the ground,
homogenized meal passes through preheaters, calcines near 900 °C and enters a rotary kiln at
about **1450 °C**, emerging as marble-sized **clinker**. Its strength minerals are alite
(3CaO·SiO₂, “C₃S”, early strength), belite (2CaO·SiO₂, “C₂S”, later strength), tricalcium
aluminate (C₃A, rapid early reaction/heat) and ferrite (C₄AF). The clinker is ground with
about 3–5% **gypsum**, which retards the otherwise flash-setting hydration of C₃A.

```photo id="chem12/kiln" caption="The rotary kiln of a cement works: a long steel cylinder, slightly inclined, that turns slowly while the charge moves down through the hot zone." width="75"
```


Ordinary Portland cement (OPC) is essentially clinker + gypsum. Portland pozzolana cement
(PPC) intergrinds reactive material such as fly ash; the pozzolan later consumes Ca(OH)₂
from hydration to make more binding calcium-silicate-hydrate, often improving durability
and lowering clinker-related CO₂. Setting and hardening are hydration, not “drying”:
silicates form C–S–H gel plus Ca(OH)₂ exothermically, which is why fresh concrete is cured
wet and why the alkaline pore solution passivates reinforcing steel.

### Pulp and paper

Paper is a felted web of cellulose fibres. The industrial problem is freeing those fibres
from lignin, the aromatic glue of wood. **Mechanical pulping** grinds or refines wood with
high yield, but lignin remains, so newsprint is weaker and yellows in light. **Kraft
(chemical) pulping** cooks chips in NaOH + Na₂S (“white liquor”), dissolving lignin to give
strong fibres; the spent **black liquor** is concentrated and burned, recovering both energy
and inorganic cooking chemicals. Pulp is washed, screened and bleached — modern sequences
use oxygen, chlorine dioxide (elemental-chlorine-free) or peroxide rather than elemental
chlorine, reducing chlorinated pollutants.

Stock is then diluted, mixed with fillers (CaCO₃/kaolin for opacity and smoothness) and
sizing agents (to resist ink spreading), spread on a moving wire (Fourdrinier machine),
pressed, dried on heated cylinders and calendered. Paper quality is specified by grammage
(g m⁻²), tensile/burst/tear strength, brightness, opacity and moisture. Recovered paper is
repulped and de-inked, though fibres shorten a little each cycle. Bamboo, bagasse, straw and
sabai grass are regionally important non-wood fibres, including in South Asian mills.

### Six processes the syllabus names

| Product | Heart of the process | Non-negotiable examination point |
|---|---|---|
| **Ammonia — Haber** | N₂ + 3H₂ over promoted Fe, about 450 °C and 200 atm, NH₃ liquefied out and unreacted gas recycled | Exothermic equilibrium compromise; catalyst changes rate, not equilibrium |
| **Nitric acid — Ostwald** | 4NH₃ + 5O₂ →(Pt–Rh gauze, about 900 °C) 4NO + 6H₂O; 2NO + O₂ → 2NO₂; 3NO₂ + H₂O → 2HNO₃ + NO (recycled) | The NO by-product is not waste; it re-enters oxidation/absorption |
| **Sulfuric acid — Contact** | S or sulfide ore → SO₂; 2SO₂ + O₂ ⇌ 2SO₃ over V₂O₅ near 450 °C; SO₃ absorbed in conc. H₂SO₄ to oleum, then diluted | Directly dissolving SO₃ in water makes a corrosive acid mist |
| **Caustic soda — chlor-alkali** | Electrolysis of brine: anode Cl₂, cathode H₂ + NaOH. A porous diaphragm limits Cl₂/OH⁻ mixing but gives salt-contaminated liquor | Modern membrane cells give purer NaOH and avoid asbestos diaphragms/mercury cells |
| **Sodium carbonate — Solvay** | NH₃/CO₂ into brine precipitates NaHCO₃; calcining gives Na₂CO₃; lime recovers NH₃ | Overall waste stream is mainly CaCl₂; KHCO₃ is too soluble for a potassium version (Ch. 14) |
| **Urea** | 2NH₃ + CO₂ under pressure → ammonium carbamate → CO(NH₂)₂ + H₂O; solution is concentrated and prilled/granulated | 46% N — the most concentrated common solid nitrogen fertilizer; excess heat forms undesirable biuret |


::: example Worked example — why industry picks a compromise temperature (Haber process)
Ammonia synthesis, N₂ + 3H₂ ⇌ 2NH₃, is exothermic. Reason through the plant conditions as an examiner does:

1. **Yield at equilibrium** (Le Chatelier): low temperature and high pressure favour NH₃ (4 gas moles → 2).
2. **Rate**: low temperature is uselessly slow; a catalyst (finely divided iron) speeds the *approach* to equilibrium but cannot change its position.
3. **Economics**: very high pressures need expensive plant.

So the operating point is a **compromise: about 450 °C, about 200 atm, iron catalyst**, with the ammonia liquefied out and unreacted gases recycled. The same three-line argument (yield ↔ rate ↔ cost) answers the equivalent Contact-process question (about 450 °C, 1–2 atm, V₂O₅ catalyst).
:::

::: caution Trap — batch vs continuous, and what a catalyst cannot do
**Continuous** processes suit bulk chemicals made on a huge scale (ammonia, sulphuric acid, cement); **batch** processing suits small-scale, high-value products (many drugs and dyes). And the perennial trap: a catalyst lowers activation energy and shortens the time to equilibrium — it never **increases the percentage yield at equilibrium**.
:::

## 21.3 Uses of common non-metals, metals, inorganic and organic compounds

Use follows property. A compact, high-yield map is:

| Material | Major uses | Property being cashed in |
|---|---|---|
| O₂ | Steel converters, welding, medical oxygen | Supports rapid oxidation/respiration |
| N₂ | Haber feedstock; inert blanketing and food packaging | Very unreactive triple bond |
| H₂ | Ammonia, refining, hydrogenation of oils, emerging low-carbon fuel/reductant | Light, combustible, reducing |
| Cl₂ and hypochlorites | Water disinfection, PVC and chlorinated intermediates | Oxidizing, microbicidal |
| Sulfur | Sulfuric acid, vulcanizing rubber, fungicides | Accessible S–S/redox chemistry |
| Phosphorus compounds | Fertilizers, detergents (restricted), flame retardants | Phosphate is an essential nutrient |
| Graphite/diamond | Electrodes, lubricant, pencils / cutting tools and abrasives | Layered slipperiness / extreme hardness |
| Fe/steel | Construction, machines, vehicles | Strength, abundance, alloy tuning |
| Al | Aircraft, cables, packaging, utensils | Low density + protective oxide film |
| Cu | Electrical wiring, motors, heat exchangers | Conductivity second only to Ag, ductility |
| Zn | Galvanizing, brass, dry cells | Sacrificial corrosion (Ch. 10) |
| Ti and alloys | Aircraft, implants, chemical plant | Strength-to-density and corrosion resistance |
| Li compounds | Rechargeable batteries, lubricating greases, mood-stabilizing drug salts | Lightest metal, high electrode potential |
| Na₂CO₃ / NaHCO₃ | Glass, detergents, water softening / baking and antacid use | Alkalinity at two strengths |
| CaO / Ca(OH)₂ / CaOCl₂ | Cement and steel flux / mortar and liming / bleaching powder disinfectant | Basicity and available chlorine |
| Alum, KAl(SO₄)₂·12H₂O | Water clarification, mordant | Al³⁺ hydrolyses and coagulates colloids |
| Methane / LPG | Domestic and industrial fuel, H₂ manufacture | High H:C ratio, clean-er combustion than coal |
| Ethene | Polythene, PVC via chloroethene, ethanol/ethylene oxide chains | Reactive π bond — a platform molecule |
| Ethanol | Solvent, antiseptic, fuel blending, tinctures | Miscibility, volatility, microbicidal action |
| Ethanoic acid | Vinegar, acetate esters/fibres | Weak-acid food safety + acylation chemistry |
| Glycerol | Cosmetics, pharmaceuticals, nitroglycerin | Hygroscopic triol, non-volatile |
| Benzene/toluene | Feedstocks for styrene, phenol, dyes and drugs | Reformable aromatic platform (with strict exposure control) |

## 21.4 Polymers, dyes, drugs, pesticides and fertilizers; colloids, osmotic pressure and buffers; radioisotopes

### Polymers

A polymer is a macromolecule built from repeating monomer units. **Addition polymers** form
when π bonds open in a chain reaction and no small molecule is lost: ethene → polythene,
chloroethene → PVC, styrene → polystyrene, tetrafluoroethene → PTFE (Teflon). **Condensation
polymers** grow stepwise with loss of H₂O or another small molecule: hexamethylenediamine +
adipic acid → nylon-6,6; ethylene glycol + terephthalic acid → PET polyester; phenol +
formaldehyde → Bakelite. Natural rubber is cis-polyisoprene; heating it with sulfur
(**vulcanization**) introduces cross-links that convert a sticky gum into a resilient
elastomer. Linear/branched **thermoplastics** soften on heating and can be remoulded;
cross-linked **thermosets** char rather than melt. Fibres (nylon, polyester) are drawn into
oriented chains for tensile strength. The current materials challenge is circular: design
for sorting/recycling, reduce microplastic shedding and reserve biodegradable polymers such
as PLA for settings where their required composting conditions actually exist.

### Dyes

Colour requires conjugated unsaturation. The group chiefly responsible is the
**chromophore** — azo –N=N–, carbonyl/anthraquinone systems, phthalocyanine rings — while an
**auxochrome** such as –NH₂, –OH or –SO₃H deepens colour and helps the dye dissolve or bind.
Azo dyes are made by diazotizing a primary aromatic amine and coupling it with phenol/
β-naphthol (Ch. 20). By application, dyes may be direct (hydrogen-bond to cotton), acid
(anionic, for wool/nylon), basic (cationic), reactive (covalent bond to fibre — excellent
wash fastness), vat (indigo; applied in reduced soluble form, then oxidized in the fibre) or
disperse (tiny particles for polyester). Some azo dyes can be metabolically cleaved to
regulated aromatic amines, so dye chemistry is also toxicology.

### Drugs

A drug is a substance used to diagnose, prevent or treat disease. Examples by action:
**analgesics/antipyretics** (paracetamol; aspirin is also anti-inflammatory and antiplatelet),
**antibiotics** (penicillins and others act on bacterial targets and are useless against
viral colds; incomplete or unnecessary courses select resistant bacteria), **antacids**
(Mg(OH)₂/Al(OH)₃ mixtures neutralize excess gastric HCl), **antihistamines** (allergy),
**antimalarials** (chloroquine historically, artemisinin combinations now central), and
**anaesthetics**. An **antiseptic** is applied to living tissue (chloroxylenol/Dettol-type
preparations, iodine tincture); a **disinfectant** is for surfaces (phenolics, hypochlorite)
and is generally more cytotoxic. Dose, formulation and pharmacokinetics turn a molecule into
a medicine — the bridge to pharmacology in the health-science degrees CEE opens.

### Pesticides and fertilizers

Pesticides are named by target: insecticides, herbicides, fungicides, rodenticides.
Organochlorines such as DDT are persistent and fat-soluble, so they **biomagnify** through
food chains and are heavily restricted. Organophosphates/carbamates inhibit
acetylcholinesterase and can be acutely poisonous to handlers. Pyrethroids mimic natural
pyrethrins; biopesticides include *Bacillus thuringiensis* preparations and neem
(azadirachtin). Copper-based Bordeaux mixture remains a classic fungicide.
**Integrated pest management** — resistant varieties, crop rotation, biological control,
monitoring and targeted spraying — keeps chemical use as the last, measured resort.

Plants need N for protein/chlorophyll, P for ATP/nucleic acids/roots and K for enzyme and
water regulation. Fertilizer grades quote **N–P₂O₅–K₂O**: urea 46-0-0, ammonium sulfate
21-0-0 (plus sulfur), single/triple superphosphate about 16/46% P₂O₅, DAP about 18-46-0 and
muriate of potash (KCl) about 0-0-60. In soil, urease hydrolyses urea to ammonium, nitrifying
bacteria form nitrate, and excess nitrate/phosphate leaches or runs off to cause
eutrophication. Manures and composts are dilute and slow but add carbon and improve soil
structure; the modern answer is soil testing and the right dose at the right time, not
“chemical versus organic” slogans.

### Colloids, osmosis and buffers around us

A colloid disperses particles of roughly 1–1000 nm through a continuous medium. Named by
the pair of phases, examples include **sols** (paint, blood plasma proteins), **gels**
(jelly, silica gel), **emulsions** (milk, mayonnaise: liquid in liquid), **foams** (whipped
cream, shaving foam) and **aerosols** (fog, smoke). Colloids scatter a light beam
(**Tyndall effect**), jitter under molecular bombardment (**Brownian motion**) and often
carry surface charge, so electrolytes coagulate them — multivalent ions being most effective
(Hardy–Schulze pattern). Alum clarifies turbid water by coagulating negatively charged clay
and humic colloids; gelatin and casein act as protective colloids in foods and inks.

**Osmosis** is net solvent movement through a semipermeable membrane toward the side of
higher solute concentration; osmotic pressure is $\pi=iCRT$. A 0.9% (9 g L⁻¹) NaCl solution
is about 0.154 mol L⁻¹ in NaCl and, with i≈2, close to blood osmolality — hence “normal
saline” neither swells nor shrivels red cells. Salt and sugar preserve food by drawing water
from microbes; wilted vegetables crisp again in water; and **reverse osmosis** applies
pressure exceeding π to force fresh water out of seawater/brackish supplies. Oral rehydration
(also Ch. 15) is osmosis harnessed by coupled Na⁺–glucose absorption.

A **buffer** is a conjugate acid–base pair that absorbs added H⁺ or OH⁻ with little pH change.
Blood is held near pH 7.4 chiefly by H₂CO₃/HCO₃⁻, assisted by phosphate and proteins including
haemoglobin; acetate and phosphate buffers stabilize laboratory reagents, eye drops,
injections and fermentation media. The chemistry is Ch. 7's equilibrium doing daily work.

### Medical and industrial uses of radioisotopes

Unstable nuclei are useful because their radiation can be detected at tracer mass or focused
for damage. **Tc-99m** (metastable, 6 h half-life, clean γ) is the workhorse of diagnostic
scans of bone, heart and thyroid; **F-18** in fluorodeoxyglucose lights up glucose-hungry
tissue in PET imaging. **I-131** is concentrated by the thyroid, where its β emission treats
hyperthyroidism and thyroid cancer; **P-32** has been used for excess red-cell production;
**Co-60** γ beams treat tumours and sterilize medical supplies; **Ir-192** seeds deliver
brachytherapy; and targeted agents such as **Lu-177** combine a tumour-seeking molecule
with a β emitter (“theranostics” when paired with an imaging isotope).

Industry uses Co-60/Ir-192 γ radiography to inspect welds and castings, β/γ gauges to measure
sheet thickness and tank levels without contact, tracer isotopes to find pipeline leaks and
follow groundwater, Am-241 ionization in smoke detectors, food irradiation to delay sprouting
and kill insects/microbes, and sterile-insect releases against pests. In research, ³H, ¹⁴C,
³²P and ³⁵S labels trace metabolic pathways, while ¹⁴C dating reads archaeological time
(Ch. 12). Every benefit is paired with ALARA discipline — minimize **time**, maximize
**distance**, use appropriate **shielding**, and manage decaying waste by half-life.



```figure caption="Four radioisotopes in public service: cobalt-60 gamma rays treat tumours and sterilise food, iodine-131 scans and treats the thyroid that greedily absorbs it, carbon-14 dates what once lived, and technetium-99m images organs from within."
cards([
    ("Cobalt-60", "gamma radiotherapy\nfood irradiation\nsterile equipment"),
    ("Iodine-131", "thyroid uptake\nscan and therapy\nthe gland absorbs it"),
    ("Carbon-14", "radiocarbon dating\nfossils and relics\nhalf-life 5730 y"),
    ("Technetium-99m", "gamma imaging\nshort half-life\norgan scans"),
], cols=2, figsize=(6.2, 3.0))
```

::: caution
Five distinctions the paper probes: **the catalyst speeds the Haber
reaction while the promoters keep the iron porous and active** — not the
same job; **oleum is SO₃ dissolved in sulphuric acid, not in water**,
because water makes an acid mist; **the diaphragm separates products,
not electrodes from solution** — without it Cl₂ and NaOH marry into
hypochlorite; **gypsum retards cement's setting rather than strengthening
it**; and **isotonic saline matches blood's osmotic pressure at 0.9 %**,
while distilled water in a vein would burst the cells.
:::

## Formula and fact sheet

| Topic | Must-know |
|---|---|
| Plant logic | Prepare → react → separate → finish → pack; recycle + QC + waste treatment throughout |
| Batch vs continuous | Batch = flexible/small lots; continuous = steady/large tonnage |
| Cement | Limestone + clay; 1450 °C clinker; gypsum retards set; 1 t CaCO₃ → 0.44 t process CO₂ |
| Paper | Kraft liquor NaOH + Na₂S; black liquor recovery; mechanical pulp keeps lignin and yellows |
| Six processes | Haber Fe; Ostwald Pt–Rh; Contact V₂O₅/oleum; chlor-alkali H₂+Cl₂+NaOH; Solvay NaHCO₃ ppt; urea via carbamate, 46% N |
| Polymers | Addition: PE/PVC/PS/PTFE. Condensation: nylon-6,6/PET/Bakelite. Thermoset = cross-linked |
| Dyes/drugs | Chromophore colours, auxochrome binds/dissolves; antibiotics ≠ antivirals; antiseptic = tissue, disinfectant = surface |
| Agrochemicals | DDT biomagnifies; N–P₂O₅–K₂O labels; urea 46-0-0, DAP 18-46-0, MOP 0-0-60 |
| Daily physical chemistry | Tyndall for colloids; π=iCRT; 0.9% saline isotonic; blood buffer H₂CO₃/HCO₃⁻ |
| Isotopes | Tc-99m/F-18 imaging; I-131 thyroid; Co-60 therapy/sterilization/radiography; Am-241 smoke alarm |

### Rapid-revision tables and high-yield facts

| Item | Value |
|---|---|
| Haber ΔH | −92 kJ/mol, exothermic |
| Oleum | H₂S₂O₇ |
| Solvay by-product | CaCl₂ |
| Urea nitrogen | 46 % |
| Saline isotonic | 0.9 % NaCl |
| Blood pH | 7.4, bicarbonate buffer |
| Aspirin | acetylsalicylic acid |
| Vulcanising agent | sulphur |
| Co-60 | therapy, irradiation |
| C-14 | radiocarbon dating |

## Chapter summary

- A viable process joins reaction chemistry to separation, recycle, energy, quality and waste systems; batch suits variety, continuous suits volume.
- Cement clinker minerals and gypsum explain strength and setting, while limestone calcination makes process CO₂ unavoidable without substitution/capture.
- Kraft pulping's chemical-recovery loop is why a paper mill can be both a fibre factory and a power station.
- Haber, Ostwald, Contact, chlor-alkali, Solvay and urea each compress to one catalyst/reagent, one equilibrium trick and one product-separation trick.
- Uses of common substances are predictable from properties such as conductivity, oxide passivation, alkalinity, π reactivity and hydrogen bonding.
- Addition versus condensation polymerization, chromophore/auxochrome design and drug action classes organize the consumer-chemical world.
- Fertilizer value is printed as N–P₂O₅–K₂O; pesticide persistence and nutrient runoff are the environmental price of careless dosage.
- Tyndall scattering identifies colloids, iCRT prices osmosis from saline drips to desalination, and bicarbonate keeps blood near pH 7.4.
- Radioisotopes image, treat, sterilize, inspect and trace — always under time–distance–shielding discipline.

## Practice questions

**Set A — Recall (25 questions)**

1. In a typical chemical plant, separation and purification normally come immediately after the
   (a) packaging stage (b) mining of ore only (c) marketing stage (d) reaction/conversion stage
2. Continuous processing is most suitable for
   (a) very large tonnage at steady specification (b) one-off laboratory samples (c) changing recipes hourly (d) handmade products only
3. The fraction of feed converted to the desired product (rather than by-products) is closely described by
   (a) viscosity (b) humidity (c) selectivity (d) colour
4. A lime scrubber in a power/chemical plant is used mainly to remove
   (a) CO₂ only (b) SO₂ from flue gas (c) sand from water (d) nitrogen from air
5. The principal raw materials of Portland cement are limestone and
   (a) clay/shale (b) common salt (c) bauxite only (d) phosphate rock
6. Gypsum is ground with cement clinker mainly to
   (a) colour it white (b) remove iron (c) supply nitrogen (d) retard setting
7. Cement clinker is formed in a rotary kiln at about
   (a) 450 °C (b) 1450 °C (c) 250 °C (d) 100 °C
8. Kraft pulping uses a cooking liquor containing NaOH and
   (a) NaCl (b) NaNO₃ (c) Na₂S (d) NaHCO₃ only
9. The catalyst in the Haber process is promoted
   (a) platinum (b) iron (c) V₂O₅ (d) nickel oxide only
10. The catalyst gauze in the Ostwald process is
   (a) Pt–Rh (b) Fe/Mo (c) CuCl (d) MnO₂
11. The catalyst for oxidizing SO₂ to SO₃ in the Contact process is
   (a) Fe₂O₃ (b) ZnO (c) Pt only in all plants (d) V₂O₅
12. Electrolysis of brine in a chlor-alkali cell gives NaOH together with H₂ and
   (a) O₂ (b) CO₂ (c) Cl₂ (d) NH₃
13. The solid filtered off in the Solvay process before calcination is
   (a) NaHCO₃ (b) Na₂CO₃ (c) NH₄Cl (d) CaCO₃
14. Urea contains approximately what percentage of nitrogen?
   (a) 21% (b) 60% (c) 46% (d) 82%
15. Aluminium is preferred for overhead cables and aircraft largely because it is light and protected by a surface film of
   (a) AlCl₃ (b) Al₂O₃ (c) AlH₃ (d) Al₂S₃
16. PVC is the addition polymer of
   (a) ethene (b) tetrafluoroethene (c) styrene (d) chloroethene (vinyl chloride)
17. Nylon-6,6 is an example of a
   (a) addition polymer (b) natural protein (c) condensation polymer (d) thermoset resin only
18. Bakelite is a
   (a) thermoplastic (b) thermosetting polymer (c) natural fibre (d) silicone oil
19. The –N=N– group in an azo dye acts as the
   (a) chromophore (b) auxochrome (c) mordant (d) solvent
20. Antibiotics are effective primarily against
   (a) viruses (b) genetic diseases (c) all cancers (d) bacteria
21. DDT belongs to the persistent pesticide class called
   (a) pyrethroids (b) organochlorines (c) carbamates (d) biopesticides
22. A fertilizer labelled 18-46-0 is commonly
   (a) urea (b) lime (c) muriate of potash (d) DAP (diammonium phosphate)
23. A colloidal dispersion can be recognized by scattering of light, the
   (a) Raman effect only (b) photoelectric effect (c) Tyndall effect (d) Doppler effect
24. The principal buffer keeping blood near pH 7.4 is
   (a) carbonic acid/bicarbonate (b) acetic acid/acetate (c) HCl/NaCl (d) ammonia/ammonium chloride
25. The radioisotope most widely used for diagnostic gamma imaging is
   (a) C-14 (b) U-235 (c) Tc-99m (d) Ra-226

::: note Answers and explanations — Set A
**1.** (d) — reactors rarely give a pure, saleable stream; separation is the next core block.
**2.** (a) — steady operation amortizes automation and heat-integration over huge throughput.
**3.** (c) — yield = conversion × selectivity in process language.
**4.** (b) — wet limestone/lime scrubbing converts SO₂ to sulfite/sulfate (gypsum) salts.
**5.** (a) — clay supplies silica, alumina and iron oxide.
**6.** (d) — sulfate controls C₃A hydration and prevents flash set.
**7.** (b) — partial melting at clinkering temperature forms alite.
**8.** (c) — sulfide improves lignin cleavage and pulp strength in kraft cooking.
**9.** (b) — iron with structural/electronic promoters.
**10.** (a) — platinum–rhodium gauze oxidizes NH₃ selectively to NO at short contact time.
**11.** (d) — vanadium(V) oxide (supported, alkali-promoted) in modern converters.
**12.** (c) — three co-products in fixed electrochemical proportion.
**13.** (a) — sodium bicarbonate is the sparingly soluble pivot of Solvay chemistry (Ch. 14).
**14.** (c) — CO(NH₂)₂ has molar mass 60, of which 28 is N (46.7%).
**15.** (b) — a thin adherent oxide passivates the reactive metal.
**16.** (d) — poly(vinyl chloride) is the systematic name behind the initials.
**17.** (c) — each amide link forms with loss of water.
**18.** (b) — the phenol–formaldehyde network is permanently cross-linked.
**19.** (a) — the conjugated azo unit absorbs visible light.
**20.** (d) — most hit bacterial walls, ribosomes or enzymes; they do not treat viral infections.
**21.** (b) — C–Cl persistence plus lipid solubility drives environmental accumulation.
**22.** (d) — read fertilizer labels as N–P₂O₅–K₂O.
**23.** (c) — particles are large enough to scatter but too small to settle quickly.
**24.** (a) — breathing removes CO₂ and makes this an open, exceptionally effective buffer.
**25.** (c) — its 6-hour half-life and 140 keV γ suit imaging and rapid clearance.
:::

**Set B — Understanding (15 questions)**

1. A pharmaceutical maker producing many small, strictly traceable lots usually prefers batch processing mainly because it offers
   (a) the highest tonnage (b) no cleaning ever (c) flexibility and lot identity (d) continuous flow
2. Recycling unreacted N₂/H₂ in the Haber loop is essential because conversion per pass at the compromise temperature is
   (a) exactly 100% (b) endothermic (c) zero without recycle (d) limited (equilibrium), so one pass wastes feed
3. Even a cement kiln fired by carbon-free fuel would emit large CO₂ because limestone itself undergoes
   (a) calcination to CaO + CO₂ (b) hydration (c) polymerization (d) electrolysis
4. Replacing part of clinker by fly ash in PPC generally lowers process emissions and improves later durability because the pozzolan reacts with hydration-produced
   (a) NaCl (b) Ca(OH)₂ (c) CO₂ gas only (d) gypsum only
5. Mechanically pulped newsprint yellows with age/light mainly because most of the wood's coloured, oxidizable polymer remains in the sheet:
   (a) cellulose (b) keratin (c) starch (d) lignin
6. SO₃ is absorbed into concentrated H₂SO₄ (oleum) rather than water mainly to avoid forming a persistent
   (a) solid (b) acid mist (c) explosive gas (d) blue solution
7. Membrane chlor-alkali cells are preferred to old diaphragm/mercury cells because they give purer NaOH with lower energy and avoid asbestos and
   (a) chlorine (b) electricity (c) mercury pollution (d) brine
8. Urea becomes plant-available nitrogen in soil after urease hydrolyses it first toward
   (a) ammonium/ammonia (b) nitrate directly (c) N₂ gas only (d) protein
9. A thermoplastic can be remelted and reshaped because its chains are held to one another only by
   (a) covalent cross-links (b) intermolecular forces (c) ionic bonds (d) metallic bonds
10. Vulcanization improves rubber mainly by introducing sulfur
   (a) cross-links between chains (b) plasticizers (c) crystals (d) fillers only
11. A reactive dye is exceptionally wash-fast on cotton because it forms a covalent bond with the
   (a) water (b) air (c) detergent (d) fibre
12. Antibiotic resistance spreads fastest when antibiotics are overused because susceptible bacteria are killed while resistant variants are
   (a) converted to viruses (b) dissolved (c) selected to survive and multiply (d) made sterile
13. DDT concentration rises toward top predators because DDT is persistent and stored in body
   (a) fat (b) water (c) bone mineral only (d) blood plasma only
14. Intravenous fluid is made about 0.9% in NaCl so that it is isotonic and red cells neither swell nor shrink by net
   (a) diffusion of Na⁺ (b) sedimentation (c) boiling (d) osmosis of water
15. Bicarbonate buffer resists a fall in blood pH because HCO₃⁻ reacts with added H⁺ to form carbonic acid/CO₂, which can be removed by
   (a) the skin (b) breathing (c) bone growth (d) digestion only

::: note Answers and explanations — Set B
**1.** (c) — campaign manufacture and unambiguous lot genealogy outweigh throughput in regulated medicines.
**2.** (d) — the plant accepts modest per-pass conversion and separates/recycles rather than chasing a slow low-temperature equilibrium.
**3.** (a) — Worked example 21.1 quantified the unavoidable 440 kg per tonne of CaCO₃.
**4.** (b) — pozzolanic reaction turns portlandite into additional C–S–H binding gel.
**5.** (d) — lignin chromophores oxidize; chemical pulps remove most lignin before bleaching.
**6.** (b) — fine H₂SO₄ aerosol escapes ordinary absorption and corrodes plant and lungs.
**7.** (c) — technology substitution removed two legacy hazards at once.
**8.** (a) — nitrification to nitrate follows; surface-applied urea can lose NH₃ if not incorporated/watered.
**9.** (b) — heating overcomes dispersion/H-bond forces without breaking the backbone.
**10.** (a) — a sparse sulfur network lets chains stretch without flowing past one another permanently.
**11.** (d) — covalent attachment beats adsorption when the garment is washed.
**12.** (c) — resistance is evolution observed at clinical speed; the drug selects, it does not create the need.
**13.** (a) — each trophic level retains much of the dose while respiring away most food energy.
**14.** (d) — cell membranes pass water far more readily than NaCl, so osmolality must match.
**15.** (b) — coupling the buffer to ventilation is why blood pH control is respiratory as well as chemical.
:::

**Set C — Application (10 questions)**

1. The process CO₂ released by calcining 2500 kg of pure CaCO₃ is
   (a) 440 kg (b) 1100 kg (c) 2500 kg (d) 560 kg
2. A plant must make about 2000 tonnes of ammonia per day, every day, to one specification. The natural operating mode is
   (a) batch (b) manual (c) continuous (d) seasonal only
3. Hexamethylenediamine + adipic acid polymerize to give
   (a) nylon-6,6 (b) PET (c) Bakelite (d) polythene
4. A benzenediazonium salt coupled with phenol in alkali is the standard preparation of an
   (a) ester (b) antibiotic (c) organochlorine (d) azo dye
5. A farmer needs a fertilizer supplying both nitrogen and phosphorus but no potassium. The bag to choose is labelled
   (a) 46-0-0 (b) 0-0-60 (c) 18-46-0 (d) 0-46-0
6. Milk is best classified as a colloid of the type
   (a) emulsion (b) aerosol (c) gel only (d) foam
7. In reverse osmosis desalination, the applied pressure on seawater must exceed the
   (a) vapour pressure (b) surface tension (c) atmospheric pressure only once (d) osmotic pressure
8. The positron-emitting isotope in FDG used for PET scans is
   (a) I-131 (b) F-18 (c) Co-60 (d) Am-241
9. Hidden cracks in a steel weld are inspected non-destructively using gamma radiography, commonly with
   (a) Ir-192 (or Co-60) (b) H-3 (c) C-14 paper (d) P-32 paint
10. Long-term heavy use of ammonium-based fertilizer tends to make many soils more
   (a) alkaline (b) acidic (nitrification releases H⁺) (c) saline in one day (d) sterile of all microbes

::: note Answers and explanations — Set C
**1.** (b) — 2500 × 44/100 = 1100 kg, scaling Worked example 21.1.
**2.** (c) — commodity scale and a single product are exactly the continuous-process niche.
**3.** (a) — both monomers contribute six carbons to the repeat-unit name.
**4.** (d) — coupling installs the –N=N– chromophore between two aromatic systems.
**5.** (c) — DAP's grade is 18% N and 46% P₂O₅ with no K₂O.
**6.** (a) — fat droplets dispersed in an aqueous continuous phase (with protein colloids as stabilizers).
**7.** (d) — only then does solvent flow run from the concentrated side to the dilute product side.
**8.** (b) — F-18 labelled fluorodeoxyglucose reports glucose metabolism.
**9.** (a) — penetrating γ rays shadow internal voids/cracks onto a detector, under strict radiological control.
**10.** (b) — NH₄⁺ + 2O₂ → NO₃⁻ + 2H⁺ + H₂O in nitrification, so liming plans accompany ammonium fertilizers.
:::

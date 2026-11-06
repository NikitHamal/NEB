---
subject: Botany
grade: CEE
unit: 15
title: Applied Botany
hours: 3
area: Developmental and Applied Botany
---

The closing chapter of the Botany book — **3 of the 40 Botany questions**
— turns everything before it into technology: **plant tissue culture**
(the technique that regenerates whole plants from single cells via
totipotency), **genetic engineering** (recombinant DNA, vectors, PCR,
GMOs and Nepal's biosafety rules), and the field-level applied botany
of **biofertilizers, green manures and plant breeding**, rounded off by
**bio-engineering, food safety and food security**. It is a vocabulary
chapter: the marks live in the exact terms, the named examples and one
or two multiplication sums.

::: key What the paper asks from this chapter
- **Tissue culture** — totipotency (Haberlandt 1902; Steward 1957 carrot); MS medium (Murashige and Skoog 1962); explant → sterilise → inoculate → callus → organogenesis → hardening; auxin : cytokinin ratio (high auxin roots, high cytokinin shoots).
- **Culture types** — callus, suspension, meristem (virus-free), anther (haploids → colchicine doubling → pure lines), embryo rescue, protoplast fusion (pomato), cryopreservation −196 °C; somaclonal variation.
- **Genetic engineering tools** — restriction endonucleases (scissors, sticky ends), DNA ligase (glue), vectors (pBR322; Ti plasmid of *Agrobacterium tumefaciens*, T-DNA), selectable markers; transfer: CaCl₂/heat shock, electroporation, microinjection, gene gun, Agrobacterium; PCR (Kary Mullis), gel electrophoresis.
- **GMOs** — humulin (1982), Flavr Savr tomato (1994, antisense polygalacturonase), Bt cotton and brinjal (*cry* genes), Golden Rice (β-carotene), Roundup Ready soybean; transgenic ≠ hybrid; Cartagena Protocol; **no GM crop registered for cultivation in Nepal**.
- **Plant breeding** — germplasm → evaluation → selection (mass, pure-line, clonal) → hybridisation → testing/release; heterosis vs inbreeding depression; mutation and polyploidy breeding; Borlaug and IR8; backcross; vertical vs horizontal resistance; biofortification.
- **Biofertilizers and green manures** — *Rhizobium*, *Frankia* (utis), *Azolla–Anabaena*, *Azotobacter*, *Azospirillum*, blue-green algae, phosphate solubilisers, mycorrhiza (phosphorus); dhaincha (*Sesbania*), sunhemp ploughed in green.
- **Bio-engineering and food** — bioreactor/fermenter, biogas (≈60% methane), bioremediation (*Pseudomonas* superbug), bioleaching; food safety (hazards, HACCP, Codex, DFTQC) vs food security (availability, access, utilisation, stability — FAO).
:::

## 15.1 Plant tissue culture: concept, types and applications

::: definition Plant tissue culture
The growth of plant cells, tissues or organs on a **sterile, chemically
defined nutrient medium** under controlled temperature, light and
humidity — *in vitro*, "in glass". It rests on **totipotency**: the
ability of a single living plant cell to divide and regenerate a
complete plant.
:::

Totipotency was proposed by **Haberlandt (1902)** and proved by
**F. C. Steward (1957)**, who grew whole carrot plants from single
phloem cells in coconut water. The standard medium is **MS medium
(Murashige and Skoog, 1962)**: macro- and micronutrient salts, **2–3%
sucrose** as the carbon source (young cultures barely photosynthesise),
vitamins, glycine, 0.8% agar to gel it — and, decisively, the growth
regulators **auxin and cytokinin**, whose ratio steers development
(Skoog and Miller 1957, Unit 13): high auxin → **roots**, high cytokinin
→ **shoots**, balanced → an unorganised **callus**.

```photo id="cee-bot/tissue-culture" caption="A cucumber plantlet regenerated from a shoot-tip explant on Murashige-Skoog medium with 1 mg/L of the cytokinin benzylaminopurine - tissue culture in a single image. The scale bar is 2000 μm." width="70"
call 0.15 0.92 0.14 0.68 "Cotyledon"
call 0.60 0.92 0.50 0.72 "Shoot apex with new leaves"
call 0.84 0.14 0.88 0.52 "Cotyledon"
```


The routine runs in steps, and the paper asks for them in order:

1. **Explant** — a small piece (shoot tip, node, leaf disc, anther) from
   a healthy mother plant.
2. **Surface sterilisation** — 70% ethanol, then 0.1% mercuric chloride
   or about 1% sodium hypochlorite, then sterile-water rinses.
3. **Inoculation** — aseptic transfer to medium in a laminar-flow
   cabinet.
4. **Callus and multiplication** — about 25 °C, 16-hour photoperiod,
   subculturing every 3–4 weeks.
5. **Organogenesis** — cytokinin-rich medium for shoots, then
   auxin-rich for roots.
6. **Hardening (acclimatisation)** — plantlets weaned from saturated
   humidity to greenhouse and field conditions.

```figure caption="The tissue-culture pipeline. The two hormone shifts do the steering: balanced regulators keep a callus multiplying, cytokinin raises shoots, auxin roots them, and hardening teaches the glasshouse-raised plantlet to live outdoors."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.0))
steps = [('1. EXPLANT', 'shoot tip or node\nfrom mother plant', '#1d6fb8'),
         ('2. STERILISE', 'ethanol, then\nhypochlorite', '#6a5acd'),
         ('3. CALLUS', 'balanced auxin\nand cytokinin', '#b8860b'),
         ('4. SHOOTS', 'high cytokinin', '#2e8b57'),
         ('5. ROOTS', 'high auxin', '#2e8b57'),
         ('6. HARDENING', 'humidity lowered,\nthen field', '#c0392b')]
for i, (t, s, c) in enumerate(steps):
    row = i // 3
    col = i % 3 if row == 0 else 2 - (i % 3)
    x = 0.3 + col*3.6; y = 3.4 - row*2.6
    ax.add_patch(Rectangle((x, y), 3.1, 1.9, fc='white', ec=c, lw=1.4))
    ax.text(x + 1.55, y + 1.45, t, fontsize=6.9, ha='center', va='center', color=c)
    ax.text(x + 1.55, y + 0.62, s, fontsize=6.3, ha='center', va='center', color=INK)
    if i in (0, 1):
        ax.annotate('', xy=(x + 3.42, y + 0.95), xytext=(x + 3.14, y + 0.95),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=10))
    if i in (3, 4):
        ax.annotate('', xy=(x - 0.46, y + 0.95), xytext=(x - 0.04, y + 0.95),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=10))
ax.annotate('', xy=(7.5 + 1.55, 3.4 - 2.6 + 1.95), xytext=(7.5 + 1.55, 3.4),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=10))
ax.set_xlim(0, 11.2); ax.set_ylim(0.3, 5.7); ax.axis('off')
```

**Kinds of culture, and what each is for:**

| Culture | What is grown | Chief use |
|---|---|---|
| Callus culture | unorganised cells on solid medium | regeneration starting point; somaclonal variation |
| Suspension culture | free cells in shaken liquid | industrial secondary metabolites (alkaloids, dyes) |
| **Meristem (shoot-tip) culture** | the 0.2–0.5 mm apical dome | **virus-free plants** — viruses lag behind the growing tip |
| **Anther/pollen culture** | microspores | **haploid plants**; colchicine doubling gives instantly homozygous lines |
| Embryo culture | young hybrid embryo | **embryo rescue** of wide crosses that would abort |
| Protoplast culture | wall-less cells (cellulase + pectinase) | **somatic hybridisation**, e.g. the potato + tomato "pomato" |

**Applications.** **Micropropagation** — thousands of genetically uniform
plants of banana, orchid, potato, sugarcane and strawberry from one bud,
produced commercially in Kathmandu and Chitwan as elsewhere; **virus-free
seed potato** from meristem culture; haploid breeding shortcuts;
production of alkaloids and other **secondary metabolites** in
suspensions; **cryopreservation** of germplasm in liquid nitrogen at
−196 °C; and — crucially — tissue culture is the **obligatory final step
of every plant genetic-engineering project**, when the transformed cell
must be grown back into a plant. Its limits: cost, the need for absolute
asepsis and skilled hands, batch-destroying contamination, and unwanted
**somaclonal variation** (culture-induced genetic changes — usually a
nuisance, occasionally a source of useful new variation).

::: example Worked example — how fast does micropropagation multiply?
**Problem.** One nodal explant of potato is subcultured every 5 weeks and
each subculture multiplies the shoots five-fold. (a) How many shoots
after 25 weeks? (b) If 10% are lost in hardening, how many plants reach
the field?

**Solution.** (a) $25 / 5 = 5$ subcultures:

$$ N = 5^{5} = 3125\ \text{shoots} $$

(b) $3125 \times 0.90 = 2812.5$, so about **2812 plants** from a single
node in just over five months — exponential multiplication no field
method can match.
:::


::: example Worked example — why somaclones can save a crop
A virus has infected a farmer's entire stock of an elite banana variety, which is propagated only by suckers. Reason out the tissue-culture rescue:

1. The shoot **apical meristem** is virtually virus-free (the virus moves through vascular tissue and lags behind the rapidly dividing tip).
2. Excise the meristem tip, surface-sterilise it, and grow it on sterile nutrient medium (e.g. MS medium with auxin/cytokinin balance set for shoot multiplication).
3. Root the shoots, harden the plantlets, and test them for the virus — the resulting **somaclones are genetically identical** to the elite variety but freed of the pathogen.

The same logic explains why meristem culture is used for potato, sugarcane and orchids — and why ordinary cuttings would simply clone the disease.
:::

::: caution Trap — totipotency is not pluripotency, and a callus is not an organ
A mature plant cell placed in culture first **dedifferentiates** into an unorganised **callus**, then **redifferentiates** into shoots/roots depending on the auxin:cytokinin ratio (cytokinin-rich → shoots; auxin-rich → roots) — that inherent capacity is **totipotency**. Options saying the callus is "organised embryonic tissue" are wrong; organisation appears only after redifferentiation.
:::


```figure caption="Micropropagation in four moves: a sterilised explant initiates a callus, cytokinin-rich medium multiplies shoot clusters, auxin-rich medium roots them, and hardening acclimatises the plantlets to soil and open air."
flow([("initiate", "explant cleaned,\ncallus induced"),
      ("multiply", "cytokinin pushes\nshoot clusters"),
      ("root", "auxin induces\nroots on shoots"),
      ("harden", "plantlets moved\nto soil and air")], figsize=(5.2, 2.15))
```

::: example Doubling maths of the culture room
**Problem.** A micropropagation lab multiplies shoots at a rate of five per
shoot each cycle and runs four cycles from a single explant. How many
plantlets stand at the end? Separately, an anther-culture haploid of a
species with 2n = 28 is doubled with colchicine: how many chromosomes does
the doubled haploid carry?
**Solution.** Multiplication is geometric: 5⁴ = 5 × 5 × 5 × 5 = **625
plantlets** from one explant — the arithmetic behind "a forest from a
leaf". The haploid carries n = 28 ÷ 2 = 14 chromosomes; colchicine doubles
the set without cell division, giving a fully homozygous line of **28
chromosomes** in two generations instead of the six or more that repeated
selfing would need.
:::
```photogrid label="15.1" cols="2" ratio="1.2" caption="Micropropagation multiplies a plant very fast. (a) Plantlets growing in culture on a nutrient medium. (b) If one explant gives 5 shoots at each 4-week subculture and every shoot is subcultured, the number is 5 to the power n: 5, 25, 125, 625, 3,125 and 15,625 after 1 to 6 cycles. One piece of tissue thus gives 15,625 plantlets within 24 weeks, all genetically identical and free of disease if the explant was a meristem. Banana, orchids and potato seed tubers are multiplied this way, and ginger and cardamom are also under study in Nepal."
@ photo id="cee-bot/tissue-culture" cap="Plantlets in tissue culture"
fit 1.2
focus 0.5 0.5
@ svg cap="Plantlets after n subcultures (5 shoots each, log scale)"
N = [5 ** n for n in range(1, 7)]
assert N[-1] == 15625 and N[2] == 125
facts = {"a%d" % (i + 1): "{:,}".format(v) for i, v in enumerate(N)}
f = Fig(300, 236)
f.text(150, 12, "log10 (plantlets) against cycles", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 34, 232, 140, (0, 6), (0, 5))
ax.grid(1, 1).axes("n", "log N")
ax.curve(lambda n: n * math.log10(5), 0, 6, color=TEAL)
for n, v in enumerate(N, 1):
    ax.pt(n, math.log10(v), "{:,}".format(v) if n in (1, 3, 6) else "", dx=-6, dy=-9, anchor="end", r=3.4)
f.text(150, 206, "24 weeks (6 cycles): 15,625 plantlets", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "slope = log10 5 = 0.699 per cycle", size=10.5, color=SLATE, bold=True)
```

## 15.2 Genetic engineering: concept and applications

**Genetic engineering (recombinant DNA technology)** isolates a gene,
joins it to carrier DNA, and delivers it into a host where it replicates
and expresses. The toolkit:

```photo id="bio12/gel-uv" caption="A real agarose gel under ultraviolet light. DNA is negatively charged, so it runs from the cathode (wells, top) towards the anode (bottom); small fragments travel furthest. The ladder lane is a mixture of fragments of known size used to read off the others." width="52"
mark 0.55 0.82 "1"
mark 0.14 0.60 "2"
mark 0.64 0.50 "3"
mark 0.82 0.36 "4"
arrow 0.94 0.90 0.94 0.30
key 1 Wells where the DNA samples were loaded (cathode end)
key 2 Ladder lane — marker fragments of known sizes
key 3 A band: fragments of one size, stained with a fluorescent dye
key 4 Loading-dye front, running ahead of the smallest DNA
```


- **Restriction endonucleases — the molecular scissors.** Bacterial
  enzymes that cut DNA at specific sequences, usually leaving
  complementary **sticky ends**.
- **DNA ligase — the molecular glue**, sealing the sugar–phosphate
  backbone between joined fragments.
- **Vectors — the carriers.** A vector needs an **origin of
  replication**, unique restriction sites, and a **selectable marker**
  (often antibiotic resistance). Typical vectors are bacterial
  **plasmids** (the classic **pBR322**, with ampᴿ and tetᴿ markers),
  bacteriophages and — for plants — the **Ti plasmid of *Agrobacterium
  tumefaciens***, nature's own genetic engineer, whose **T-DNA** it
  transfers into the plant genome (the cause of crown-gall tumours).
- **Hosts** — *E. coli*, yeast, or plant cells.

**The steps:** isolate the gene (or amplify it by **PCR**) → cut gene
and vector with the **same restriction enzyme** so the sticky ends match
→ **ligate** to form **recombinant DNA** → transfer into the host —
**CaCl₂ treatment with heat shock** or **electroporation** for bacteria,
**microinjection** for animal cells, the **gene gun (biolistics)** for
monocots, ***Agrobacterium*** for most dicots → **select** the rare
transformed cells on the marker (in pBR322, recombinants have lost tetᴿ
but keep ampᴿ; modern vectors use blue–white *lacZ* screening) → grow
and exploit the clone. Two supporting techniques are asked by name:
**PCR (Kary Mullis)** — repeated cycles of **denaturation (≈94 °C),
primer annealing (≈55 °C) and extension at 72 °C** by heat-stable *Taq*
polymerase, doubling DNA each cycle — and **gel electrophoresis**,
separating DNA fragments by size in an electric field.

```figure caption="Recombinant DNA in five moves. Cutting gene and vector with the same restriction enzyme is the step that makes the ends compatible; the marker gene is what makes the rare successful cell findable."
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.0))
steps = [('1. CUT', 'gene and plasmid\nsame restriction\nenzyme', '#1d6fb8'),
         ('2. JOIN', 'sticky ends pair;\nligase seals\n(recombinant DNA)', '#6a5acd'),
         ('3. TRANSFER', 'heat shock,\ngene gun or\nAgrobacterium', '#b8860b'),
         ('4. SELECT', 'marker gene\nfinds transformed\ncells', '#2e8b57'),
         ('5. GROW', 'clone copies\ngene and makes\nits product', '#c0392b')]
for i, (t, s, c) in enumerate(steps):
    row = i // 3
    col = i % 3 if row == 0 else 2 - (i % 3)
    x = 0.3 + col*3.6; y = 3.3 - row*2.7
    ax.add_patch(Rectangle((x, y), 3.1, 2.0, fc='white', ec=c, lw=1.4))
    ax.text(x + 1.55, y + 1.55, t, fontsize=6.9, ha='center', va='center', color=c)
    ax.text(x + 1.55, y + 0.70, s, fontsize=6.2, ha='center', va='center', color=INK)
    if i in (0, 1):
        ax.annotate('', xy=(x + 3.42, y + 1.0), xytext=(x + 3.14, y + 1.0),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=10))
    if i == 3:
        ax.annotate('', xy=(x - 0.46, y + 1.0), xytext=(x - 0.04, y + 1.0),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=10))
ax.annotate('', xy=(7.5 + 1.55, 3.3 - 2.7 + 2.05), xytext=(7.5 + 1.55, 3.3),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=10))
ax.set_xlim(0, 11.2); ax.set_ylim(0.1, 5.7); ax.axis('off')
```

A **GMO** is an organism whose genome has been deliberately altered by
these methods; if the inserted gene comes from another species it is
**transgenic** — not to be confused with a **hybrid**, which is an
ordinary sexual cross. Landmark products:

| GMO | Inserted gene | Result |
|---|---|---|
| *E. coli* making **Humulin** (1982) | human insulin genes | cheap, non-allergenic insulin |
| **Flavr Savr tomato** (1994, first GM food) | antisense polygalacturonase | slow softening, long shelf life |
| **Bt cotton / Bt brinjal / Bt maize** | *cry* genes of *Bacillus thuringiensis* | built-in caterpillar resistance |
| **Golden Rice** | *psy* + *crtI* | grain accumulates β-carotene (provitamin A) |
| Roundup Ready soybean | bacterial EPSPS | glyphosate herbicide tolerance |

**Benefits:** yield with less pesticide, stress tolerance, longer shelf
life, biofortified food, and cheap medicines (insulin, hepatitis B
vaccine, growth hormone). **Concerns:** new allergens, marker-gene
spread, gene flow to wild relatives ("superweeds"), non-target insects,
erosion of landraces and farmer dependence on patented seed. Nepal
signed the **Cartagena Protocol on Biosafety** framework (National
Biosafety Framework 2006; a Supreme Court interim order in 2014 halted
GM seed import), and **no GM crop is registered for cultivation in
Nepal** — border seed samples are PCR-tested.

```photogrid label="15.2" cols="2" ratio="1.2" caption="Biological nitrogen fixation in money and kilograms. (a) A section of a legume root nodule: the dark-stained cells are packed with Rhizobium bacteria that fix nitrogen. (b) A good legume crop fixes about 100 kg of nitrogen per hectare in a year (a typical figure). To supply the same nitrogen by fertilizer a farmer would apply 217 kg of urea (46 per cent N), 476 kg of ammonium sulphate (21 per cent N) or 556 kg of diammonium phosphate (18 per cent N). Seed inoculated with Rhizobium biofertilizer, and green manure of legumes such as dhaincha, therefore save fertilizer that Nepal must import."
@ photo id="ceebot/rhizobium" cap="Section of a legume root nodule"
fit 1.2
focus 0.5 0.5
@ svg cap="Fertilizer needed to equal 100 kg of fixed nitrogen (kg)"
need = 100.0
fert = (("Urea (46% N)", 46), ("Ammonium sulphate (21% N)", 21), ("DAP (18% N)", 18))
amt = [need / p * 100 for _, p in fert]
assert round(amt[0]) == 217 and round(amt[1]) == 476 and round(amt[2]) == 556
facts = dict(urea="%.0f" % amt[0], **{"as": "%.0f" % amt[1]}, dap="%.0f" % amt[2])
f = Fig(300, 236)
f.text(150, 12, "Product needed for 100 kg N per hectare", size=10.5, color=NAVY, bold=True)
for i, ((lab, p), a) in enumerate(zip(fert, amt)):
    y = 30 + i * 46
    f.text(10, y, lab, size=10.5, color=SLATE, anchor="start")
    w = a / 556 * 200
    f.box(10, y + 8, w, 20, fill=SAND if i else MINT, stroke=AMBER if i else TEAL, r=2)
    f.text(10 + w + 6, y + 18, "%.0f kg" % a, size=10.5, color=AMBER if i else TEAL, bold=True, anchor="start", vmid=True)
f.text(150, 186, "kg product = 100 / (per cent N) x 100", size=10.5, color=NAVY, bold=True)
f.text(150, 204, "legume crop: about 100 kg N per ha a year", size=10.5, color=SLATE, bold=True)
```

## 15.3 Biofertilizers, green manures, plant breeding, bio-engineering, food safety and security

### Plant breeding

**Plant breeding** is the directed improvement of crops for yield,
quality, resistance and adaptation. A programme runs: **collect
germplasm** (varieties, landraces, wild relatives — the raw variation) →
**evaluate and select parents** → **hybridise** → **select and test**
the progeny over years and places → **release and multiply seed**. The
methods: **introduction** (importing a proven variety), **selection**
(**mass selection**, **pure-line selection** — Johannsen's progeny of one
selfed plant — and clonal selection), **hybridisation** (intervarietal,
interspecific, intergeneric), **mutation breeding** (gamma rays, EMS)
and **polyploidy breeding** (Unit 09). Crosses harness **heterosis
(hybrid vigour)** — the F₁ outperforming both parents — while continued
selfing gives the opposite, **inbreeding depression**. A single wanted
gene (say disease resistance) is usually moved by the **backcross
method**, repeatedly crossing back to the good parent while retaining
the gene. Resistance itself may be **vertical** (one major gene, total
but race-specific, liable to break down) or **horizontal** (many small
genes, partial but durable). The Green Revolution — **Norman Borlaug's**
semi-dwarf wheats and IRRI's **IR8 rice** — stands behind Nepal's own
releases such as Sabitri and Khumal-4 rice; its newest heir is
**biofortification**, breeding in iron, zinc and provitamin A.

```photo id="cee-bot/root-nodules" caption="Root nodules on a legume (clover, Fabaceae). Each pale swelling is packed with *Rhizobium* bacteria that fix atmospheric nitrogen; the plant supplies sugars and the red leghaemoglobin that keeps the nodule interior nearly oxygen-free." width="52"
call 0.58 0.92 0.40 0.66 "Root nodules"
call 0.64 0.40 0.45 0.40 "Main root"
```


### Biofertilizers and green manures

A **biofertilizer** is a preparation of living microbes that enriches
the soil's nutrients:

| Group | Organism | What it does |
|---|---|---|
| Symbiotic N-fixers | *Rhizobium* (legume nodules); *Frankia* (in *Alnus nepalensis*, utis); *Anabaena azollae* inside the fern *Azolla* | fix atmospheric N₂ for the plant |
| Free-living/associative | *Azotobacter*, *Clostridium*, *Azospirillum*, free blue-green algae (*Nostoc*, *Aulosira*) | fix N₂ in soil and flooded paddy |
| Phosphate solubilisers | *Bacillus megaterium*, *Pseudomonas striata*, *Aspergillus* | release locked-up phosphate |
| Mycorrhiza | VAM fungi such as *Glomus* | extend the root's reach for **phosphorus** and water |

A **green manure** is a fast-growing (usually leguminous) crop —
**dhaincha (*Sesbania*)**, sunhemp (*Crotalaria*) — grown and **ploughed
into the soil while still green**, donating biologically fixed nitrogen
and organic matter to the following rice or wheat crop. The distinction
the paper likes: a biofertilizer is **living inoculant added in small
amount**; a green manure is **a whole crop sacrificed to the soil**.

```photo id="cee-bot/azolla" caption="*Azolla*, a floating water fern, turns red-brown in strong light. Each tiny two-lobed frond has a cavity housing the nitrogen-fixing cyanobacterium *Anabaena azollae*; a dried Azolla mat in a paddy field works as a green manure." width="60"
label 0.50 0.06 "A dense mat of Azolla fronds"
```


### Bio-engineering

**Bio-engineering (biochemical engineering)** scales biology up: the
**bioreactor/fermenter** — a sterilised, stirred vessel with automatic
temperature, pH and oxygen control — produces penicillin, citric acid
and enzymes; **immobilised enzymes** are reused industrially;
**biogas** (about 60% methane from dung, some 450,000 household plants
in Nepal since 1992) and liquid biofuels turn biomass into energy;
**bioremediation** deploys microbes such as oil-eating ***Pseudomonas
putida*** (the "superbug") and **phytoremediation** uses plants to lift
heavy metals from soil; **bioleaching** bacteria free copper from poor
ores; **single-cell protein** (*Spirulina*) converts waste into food.

### Food safety and food security

Two terms, one mark each, constantly confused. **Food safety** is about
**quality**: freedom from **biological hazards** (*Salmonella*, *Vibrio
cholerae*, and **aflatoxin** from *Aspergillus flavus* on damp maize and
groundnut), **chemical hazards** (pesticide residues, heavy metals,
adulterants, illegal ripening chemicals) and **physical hazards**
(glass, stones). It is managed by clean production, proper drying and
storage, pasteurisation and refrigeration, the **HACCP** system of
monitoring critical control points, and **Codex Alimentarius**
standards — in Nepal enforced under the Food Act by the **Department of
Food Technology and Quality Control (DFTQC)**.

**Food security** (FAO, 1996) is about **access**: "all people, at all
times, have physical, social and economic access to sufficient, safe and
nutritious food." Its four pillars are **availability, access,
utilisation and stability** — a country can grow enough (availability)
and still have hungry citizens (access). Nepal's Constitution (Article
36) and the **Right to Food and Food Sovereignty Act, 2075 (2018)** make
food a legal right. Biotechnology serves both goals: higher, stabler
yields and biofortified crops for security; Bt crops cutting pesticide
residues and insect-bored, mould-friendly grain for safety.



```figure caption="The four biofertilizer guilds the paper names: symbiotic Rhizobium in legume nodules, free-living Azotobacter in soil, the Azolla fern hosting Anabaena in paddy water, and mycorrhizal Glomus mining phosphorus for roots."
cards([
    ("Rhizobium", "symbiotic with legumes\nnodules fix nitrogen\nleghemoglobin pink"),
    ("Azotobacter", "free-living aerobic\nfixes N in soil\nno host needed"),
    ("Azolla–Anabaena", "fern–cyanobacteria\ndual crop in paddy\nN leaks to rice"),
    ("Mycorrhiza", "Glomus on roots\nmines phosphorus\nwider water reach"),
], cols=2, figsize=(6.2, 3.0))
```

::: caution
Six swaps the paper sets: **anther culture gives haploids, not sterile
plants** — haploids are fertile after doubling; **a somatic hybrid (protoplast
fusion of two whole genomes) is not a transgenic GM plant** (one or few
defined genes); **green manure is a live crop ploughed in**, not a composted
heap (that is farmyard manure or compost); **the Ti plasmid belongs to
*Agrobacterium*, pBR322 to *E. coli***; **meristem culture is virus-free
because the meristem lacks the virus**, not because the medium kills it;
and **Bt toxin is insect-specific**, activated only in the alkaline
lepidopteran gut — it is not a general poison.
:::

```photogrid label="15.3" cols="2" ratio="1.2" caption="Azolla, the green manure of rice fields. (a) Azolla carries the nitrogen-fixing cyanobacterium Anabaena in cavities of its leaves. (b) If its biomass doubles every 3 days under good conditions, 100 g gives 100 x 2^(t/3) g: 3.2 kg after 15 days and 102.4 kg after 30 days, until space or phosphorus runs out. A mat ploughed into the paddy before rice transplanting releases its nitrogen as it decays; Azolla is also used as feed for ducks, fish and cattle. The calculation is an upper limit, since a real mat stops growing once it covers the water."
@ photo id="cee-bot/azolla" cap="Azolla mat on water"
fit 1.2
focus 0.5 0.5
@ svg cap="Azolla biomass if it doubles every 3 days (start 100 g)"
B = lambda t: 0.1 * 2 ** (t / 3)
assert abs(B(15) - 3.2) < 1e-9 and abs(B(30) - 102.4) < 1e-9
facts = dict(d15="%.1f" % B(15), d30="%.1f" % B(30))
f = Fig(300, 236)
f.text(150, 12, "Biomass (kg) against days", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 34, 232, 140, (0, 30), (0, 110))
ax.grid(5, 25).axes("day", "kg")
ax.curve(B, 0, 30, color=TEAL)
ax.pt(15, B(15), "3.2 kg", dx=0, dy=-10, anchor="middle")
ax.pt(30, B(30), "102.4 kg", dx=-8, dy=16, anchor="end")
f.text(150, 206, "doubling every 3 days: x 1,024 in 30 days", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "upper limit; real mats stop at full cover", size=10.5, color=SLATE, bold=True)
```

## Formula and fact sheet

- **Tissue culture**: totipotency (Haberlandt 1902, Steward 1957 carrot); MS medium + sucrose + agar; steps explant→sterilise→inoculate→callus→organogenesis→hardening.
- **Culture types**: meristem = virus-free; anther = haploids (double with colchicine); embryo rescue; protoplast fusion = pomato; suspension = metabolites; cryopreservation −196 °C.
- **rDNA tools**: restriction enzymes (scissors/sticky ends), ligase (glue), vectors pBR322 and Ti plasmid/T-DNA (*Agrobacterium*), selectable markers, same-enzyme cutting.
- **Transfer**: CaCl₂ + heat shock; electroporation; microinjection; gene gun; *Agrobacterium*. PCR: 94 °C denature, ~55 °C anneal, 72 °C extend (*Taq*); Kary Mullis.
- **GMOs**: Humulin 1982; Flavr Savr 1994 (antisense PG); Bt *cry* crops; Golden Rice β-carotene; transgenic ≠ hybrid; Cartagena Protocol; no GM cultivation registered in Nepal.
- **Breeding**: collection→evaluation→hybridisation→selection/testing→release; pure line (Johannsen); heterosis vs inbreeding depression; backcross for single genes; vertical (breaks down) vs horizontal (durable) resistance; Borlaug, IR8.
- **Biofertilizers**: *Rhizobium*, *Frankia*, *Azolla–Anabaena*, *Azotobacter*, *Azospirillum*, BGA, PSB, VAM (*Glomus*) for phosphorus. **Green manure**: dhaincha/sunhemp ploughed in green.
- **Bio-engineering**: bioreactor, biogas ~60% CH₄, *Pseudomonas* superbug, bioleaching (*Thiobacillus*). **Food**: safety = hazard-free (HACCP, Codex, DFTQC; aflatoxin); security = availability + access + utilisation + stability (FAO 1996).

### Rapid-revision tables and high-yield facts

| Item | Value |
|---|---|
| Totipotency | Haberlandt's concept; Steward's carrot proof |
| MS medium | Murashige & Skoog, 1962 |
| Hormone dial | high cytokinin → shoots; high auxin → roots |
| Virus-free stock | meristem (shoot-tip) culture, Morel & Martin |
| Haploids | anther culture, Guha & Maheshwari (*Datura*) |
| Somatic hybrid | protoplast fusion (pomato) |
| Scissors and glue | restriction endonuclease; DNA ligase |
| Plant vector | Ti plasmid T-DNA, *Agrobacterium tumefaciens* |
| First GM food | Flavr Savr tomato, 1994 |
| Recombinant insulin | Humulin, 1982 |
| Bt activation | alkaline insect midgut only |
| Green manure N | sunhemp/dhaincha, ~60–120 kg N ha⁻¹ |
| Green Revolution | Borlaug wheat, Nobel 1970; IR8 rice |
| Seed vault | Svalbard 2008; Nepal gene bank, NARC Khumaltar |

## Chapter summary

- Tissue culture milks totipotency on MS medium: sterilised explants pass through callus to shoots (cytokinin) and roots (auxin), then hardening — the engine of micropropagation and the finishing step of all plant genetic engineering.
- Specialised cultures earn their keep: meristems for virus-free stock, anthers for haploids and instant pure lines, rescued embryos for wide crosses, fused protoplasts for somatic hybrids, liquid nitrogen for germplasm.
- Genetic engineering cuts with restriction enzymes, glues with ligase, ferries genes on plasmid or Ti vectors, selects on markers, and amplifies DNA with PCR; its products range from Humulin and Flavr Savr to Bt crops and Golden Rice, under Cartagena-style biosafety rules (and no registered GM cultivation in Nepal).
- Plant breeding improves crops by introduction, selection, hybridisation, mutation and polyploidy — trading variation for uniformity carefully, using backcrosses for single resistance genes and heterosis for yield.
- Biofertilizers inoculate the soil with nitrogen fixers, phosphate solubilisers and mycorrhiza; green manures sacrifice a legume crop to feed the next one.
- Bio-engineering runs biology at industrial scale — fermenters, biogas, bioremediation — while food safety (hazard control: HACCP, DFTQC) and food security (FAO's four pillars of access) frame why all of it matters.

## Practice questions

**Set A — Recall (25 questions)**

1. Plant tissue culture is based on the cellular property of
   (a) totipotency (b) pluripotency of animals (c) fermentation (d) hybridisation
2. The concept of totipotency of plant cells was proposed by
   (a) Haberlandt (b) Skoog (c) Murashige (d) Steward
3. The most commonly used nutrient medium for plant tissue culture is
   (a) White's medium (b) MS (Murashige and Skoog) medium (c) Knop's solution (d) Hoagland solution
4. The small piece of plant tissue used to initiate a culture is called an
   (a) inoculum of bacteria (b) explant (c) callus (d) clone
5. The unorganised mass of dividing cells formed in tissue culture is the
   (a) protoplast (b) suspension (c) meristem (d) callus
6. Virus-free plants are best obtained by
   (a) meristem (shoot-tip) culture (b) seed culture (c) leaf culture (d) root culture
7. Haploid plants can be raised by
   (a) embryo culture (b) protoplast fusion (c) grafting (d) anther (pollen) culture
8. Somatic hybridisation, as in the "pomato", is achieved through
   (a) seed crossing (b) layering (c) anther culture (d) protoplast culture and fusion
9. Restriction endonucleases are commonly called molecular
   (a) glue (b) scissors (c) carriers (d) pumps
10. The enzyme that joins cut DNA fragments by sealing the backbone is
   (a) DNA ligase (b) DNA polymerase (c) nuclease (d) helicase
11. The classic plasmid cloning vector, with ampᴿ and tetᴿ marker genes, is
   (a) λ phage (b) pBR322 (c) Ti plasmid only (d) YAC
12. The Ti plasmid used as a plant vector comes from
   (a) *Escherichia coli* (b) *Bacillus thuringiensis* (c) yeast (d) *Agrobacterium tumefaciens*
13. The biolistic method of gene transfer is also known as the
   (a) heat-shock method (b) microinjection (c) gene gun method (d) electroporation
14. The polymerase chain reaction (PCR) was developed by
   (a) Watson (b) Sanger (c) Kary Mullis (d) Nirenberg
15. The first genetically modified food to reach the market was the
   (a) Bt cotton (b) Golden Rice (c) Roundup Ready soybean (d) Flavr Savr tomato
16. The insecticidal *cry* genes of Bt crops were obtained from
   (a) *Agrobacterium* (b) *Rhizobium* (c) *Bacillus thuringiensis* (d) *Escherichia coli*
17. Golden Rice was engineered to accumulate in its grain
   (a) β-carotene (provitamin A) (b) iron only (c) insulin (d) extra starch only
18. The symbiotic nitrogen-fixing bacterium of legume root nodules is
   (a) *Azotobacter* (b) *Rhizobium* (c) *Nitrosomonas* (d) *Clostridium*
19. The water fern *Azolla*, used as a biofertilizer in paddy, hosts the nitrogen-fixing cyanobacterium
   (a) *Anabaena azollae* (b) *Nostoc* only (c) *Frankia* (d) *Azospirillum*
20. Vesicular-arbuscular mycorrhiza (VAM, *Glomus*) as a biofertilizer mainly improves uptake of
   (a) nitrogen gas (b) carbon dioxide (c) phosphorus (d) oxygen
21. Dhaincha (*Sesbania*) is commonly grown and ploughed into paddy fields as a
   (a) bio-pesticide (b) fodder only (c) green manure (d) cash crop
22. The superiority of an F₁ hybrid over both its parents is called
   (a) inbreeding depression (b) mutation (c) apomixis (d) heterosis
23. The "father of the Green Revolution" was
   (a) M. S. Swaminathan (b) Norman Borlaug (c) Gregor Johann Mendel (d) Barbara McClintock
24. The international agreement regulating the safe transfer and use of GMOs is the
   (a) Kyoto Protocol (b) Montreal Protocol (c) Cartagena Protocol on Biosafety (d) Ramsar Convention
25. The four pillars of food security (FAO) are availability, access,
   (a) export and import (b) utilisation and stability (c) price and profit (d) storage and transport

::: note Answers and explanations — Set A
**1.** (a) — One living cell can regenerate the whole plant; Steward demonstrated it with carrot in 1957.
**2.** (a) — Haberlandt proposed it in 1902, decades before technique caught up.
**3.** (b) — MS medium (1962), its high salt strength suiting most cultures.
**4.** (b) — The explant is sterilised, then inoculated aseptically onto the medium.
**5.** (d) — Balanced auxin and cytokinin keep cells dividing without organising.
**6.** (a) — Viruses spread cell to cell more slowly than the apex grows, so the dome is usually virus-free.
**7.** (d) — Microspores diverted into embryos give haploids; colchicine doubling follows.
**8.** (d) — Fusing wall-less protoplasts merges genomes that sex cannot.
**9.** (b) — They cut at specific sequences, leaving the sticky ends that make joining possible.
**10.** (a) — Ligase restores the phosphodiester bonds between annealed sticky ends.
**11.** (b) — Inserting DNA into its tetᴿ gene gives a neat ampˢ/tet selection scheme.
**12.** (d) — The crown-gall bacterium's Ti plasmid naturally inserts T-DNA into plant chromosomes.
**13.** (c) — DNA-coated gold or tungsten microprojectiles are shot into cells — vital for monocots.
**14.** (c) — Kary Mullis (Nobel 1993); *Taq* polymerase survives the 94 °C denaturation step.
**15.** (d) — Calgene's 1994 antisense tomato preceded Bt cotton (1996) and Golden Rice (2000s).
**16.** (c) — The soil bacterium's crystal-protein genes poison caterpillar guts.
**17.** (a) — Two introduced genes (*psy*, *crtI*) complete the carotenoid pathway in the endosperm.
**18.** (b) — *Rhizobium*–legume symbiosis is the classic biofertilizer; *Nitrosomonas* nitrifies instead.
**19.** (a) — The fern–cyanobacterium partnership has manured Asian paddies for centuries.
**20.** (c) — The fungal network scours soil volume far beyond the root's own reach for phosphate.
**21.** (c) — The legume's biomass and fixed nitrogen are buried for the next crop.
**22.** (d) — Hybrid vigour; its mirror image is inbreeding depression on selfing.
**23.** (b) — Borlaug's semi-dwarf wheats (Nobel Peace Prize 1970); Swaminathan led India's programme.
**24.** (c) — The Cartagena Protocol (2000) governs transboundary movement of living modified organisms; Nepal follows it.
**25.** (b) — Availability, access, utilisation, stability (FAO, World Food Summit 1996).
:::

**Set B — Understanding (15 questions)**

1. Meristem culture can free a plant from viral infection because
   (a) viruses generally do not invade the rapidly dividing apical dome (b) meristems produce antibiotics (c) the culture medium kills viruses (d) viruses need soil
2. Somaclonal variation arising in tissue culture is valuable to breeders because it
   (a) removes all variation (b) makes plants sterile (c) can generate useful new variants to select from (d) stops cell division
3. The donor gene and the vector are cut with the same restriction enzyme so that
   (a) their sticky ends are complementary and can anneal (b) the DNA becomes circular (c) ligase is not needed (d) both are destroyed
4. A selectable marker gene is included in a vector in order to
   (a) make the DNA invisible (b) identify and select the few cells that have taken up the vector (c) increase mutation (d) colour the colony blue-green naturally
5. The Flavr Savr tomato softens slowly because an antisense gene blocks production of
   (a) cellulose (b) ethylene gas itself (c) chlorophyll (d) the wall-softening enzyme polygalacturonase
6. A transgenic plant differs from a conventional hybrid in that the transgenic carries a gene
   (a) from its own parents only (b) inserted in the laboratory, often from an unrelated organism (c) with no DNA (d) only in its seeds
7. Doubling the chromosomes of an anther-culture haploid is so useful because it instantly gives a
   (a) triploid hybrid (b) sterile plant (c) mutant (d) completely homozygous (pure) line
8. A breeder uses repeated backcrossing chiefly to
   (a) increase chromosome number (b) make polyploids (c) transfer one desired gene into an otherwise excellent variety (d) create maximum variation
9. Vertical (race-specific) disease resistance often "breaks down" in a few years because
   (a) a new pathogen race evolves that the single gene cannot stop (b) the plant forgets the gene (c) fertiliser removes it (d) rain washes it off
10. A biofertilizer differs from a green manure in that a biofertilizer is a
   (a) chemical fertiliser (b) small inoculum of living microbes, not a whole crop ploughed in (c) type of compost (d) pesticide
11. *Azolla* enriches paddy fields with nitrogen because
   (a) its cyanobacterial partner *Anabaena* fixes atmospheric nitrogen (b) it absorbs urea (c) it kills weeds (d) its roots reach groundwater
12. The HACCP system keeps food safe by
   (a) testing only the finished product (b) monitoring hazards at critical control points in production (c) banning all additives (d) freezing everything
13. A country may produce enough food for all its people and still be food-insecure because food security also requires
   (a) exports (b) big farms (c) more factories (d) that every person can actually access and utilise the food at all times
14. Drying grain thoroughly before storage prevents aflatoxin contamination chiefly by stopping growth of the fungus
   (a) *Rhizopus* (b) *Penicillium* (c) *Saccharomyces* (d) *Aspergillus flavus*
15. Germplasm is cryopreserved in liquid nitrogen at −196 °C because at this temperature
   (a) DNA multiplies (b) seeds germinate (c) metabolism is virtually arrested, giving almost unlimited storage (d) ice improves genes

::: note Answers and explanations — Set B
**1.** (a) — The dome outgrows viral spread and lacks differentiated vascular connections.
**2.** (c) — Culture-induced variation occasionally yields disease-resistant or higher-yielding clones (Larkin's somaclones).
**3.** (a) — Identical cuts leave matching overhangs that base-pair and invite ligase.
**4.** (b) — Without selection (e.g. antibiotic resistance) the one transformed cell in a million is unfindable.
**5.** (d) — Antisense RNA silences the softening enzyme, so fruit can vine-ripen yet ship firm.
**6.** (b) — A bacterial *cry* gene in cotton makes it transgenic; a maize inbred cross is merely hybrid.
**7.** (d) — Every locus becomes homozygous in one step, saving years of selfing.
**8.** (c) — Each backcross halves the donor genome while selection keeps the target gene.
**9.** (a) — Strong single-gene resistance selects hard for virulent races; horizontal resistance lasts longer.
**10.** (b) — Grams of carrier-based inoculant versus tonnes of legume biomass.
**11.** (a) — The fern shelters and feeds the fixer in its leaf cavities; ploughing in releases the nitrogen.
**12.** (b) — Hazard Analysis and Critical Control Points: prevention designed into the process.
**13.** (d) — Availability is only one pillar; access, utilisation and stability complete the FAO definition.
**14.** (d) — *A. flavus* moulds damp maize and groundnut; its aflatoxins are among the most potent natural carcinogens.
**15.** (c) — Ultra-low temperature freezes biochemistry in place for germplasm banks.
:::

**Set C — Application (10 questions)**

1. One shoot explant multiplying five-fold at each subculture gives, after five subcultures,
   (a) 25 shoots (b) 625 shoots (c) 3125 shoots (d) 125 shoots
2. A potato farmer in Jumla wants planting material free of the viruses reducing her yield. The laboratory should supply plants raised by
   (a) meristem culture (b) anther culture (c) seed sowing (d) grafting
3. Cotton badly damaged by bollworm caterpillars can be protected by a variety carrying which transgene?
   (a) *psy* (b) *cry1Ac* (c) antisense PG (d) EPSPS
4. At a border quarantine post, a seed consignment suspected of being GM is best screened by
   (a) weighing it (b) tasting it (c) microscopy (d) PCR testing for transgene sequences
5. A callus is transferred to a medium with high auxin and very low cytokinin. It will most likely form
   (a) shoots (b) flowers (c) roots (d) seeds
6. The "pomato" (potato + tomato) somatic hybrid was produced by
   (a) cross-pollination (b) protoplast fusion (c) embryo rescue (d) mutation breeding
7. Which of the following is an example of a biofortified crop aimed at hidden hunger?
   (a) Bt maize (b) Golden Rice (c) Flavr Savr tomato (d) Roundup Ready soybean
8. The main combustible component of biogas from a household dung digester is
   (a) hydrogen (b) carbon monoxide (c) butane (d) methane
9. The engineered "superbug" used to clean up oil spills is a strain of
   (a) *Pseudomonas putida* (b) *Rhizobium* (c) *Azotobacter* (d) *Bacillus subtilis*
10. A breeder needs completely homozygous lines in the shortest possible time. The fastest route is
   (a) mass selection (b) eight generations of selfing (c) anther culture followed by colchicine doubling (d) introduction

::: note Answers and explanations — Set C
**1.** (c) — $5^5 = 3125$ shoots (before hardening losses).
**2.** (a) — Meristem-tip culture, indexed for viruses, is how clean seed-potato stocks are produced.
**3.** (b) — The *cry1Ac* endotoxin gene of *Bacillus thuringiensis* is the Bt-cotton transgene.
**4.** (d) — PCR primers for common transgene elements (e.g. CaMV 35S promoter) detect GM presence sensitively.
**5.** (c) — Skoog–Miller: auxin dominance specifies root organogenesis; cytokinin dominance would give shoots.
**6.** (b) — Wall-less protoplasts of the two species are fused and the hybrid cell regenerated.
**7.** (b) — Provitamin-A rice targets vitamin-A deficiency; the others address pests, shelf life or herbicides.
**8.** (d) — Methanogen digestion yields roughly 60% CH₄, the burnable fraction.
**9.** (a) — Chakrabarty's multi-plasmid *Pseudomonas putida* degrades several crude-oil components.
**10.** (c) — Doubled haploids are homozygous at every locus in a single generation.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe plant tissue culture: techniques, totipotency, stages and applications. <span class="marks">[10]</span>
2. Describe plant breeding, biofertilisers and the use of genetic engineering in agriculture (Bt cotton, golden rice). <span class="marks">[10]</span>

```photogrid label="15.H" cols="3" ratio="1.25" caption="Applied botany. (a) Plantlets growing from explants in a tissue culture vessel. (b) A callus, an undifferentiated mass of cells grown on nutrient medium. (c) Root nodules of a legume hold Rhizobium bacteria that fix atmospheric nitrogen."
@ photo id="cee-bot/tissue-culture" cap="(a) Micropropagation"
fit 1.25
focus 0.5 0.5
@ photo id="qbank/plant-callus" cap="(b) Callus"
fit 1.25
focus 0.5 0.5
@ photo id="cee-bot/root-nodules" cap="(c) Root nodules"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: plant tissue culture (10 marks)

**Introduction.** **Plant tissue culture** is the growth of plant cells, tissues or organs on a sterile nutrient medium under controlled conditions. It rests on **totipotency**: the ability of a single living plant cell to form a whole plant (Haberlandt, Steward).

**Technique.**

1. **Explant:** a small piece of tissue (shoot tip, leaf, node) is taken from a healthy plant and **surface-sterilised** (with sodium hypochlorite or mercuric chloride).
2. **Medium:** **Murashige and Skoog (MS) medium** with macro- and micro-nutrients, sucrose (the carbon source), vitamins, agar (the solidifying agent) and **plant growth regulators**.
3. **Aseptic conditions:** a laminar-air-flow cabinet, autoclaved ($121^{\circ}\text{C}$, $15$ psi) medium and instruments, and a culture room at $25^{\circ}\text{C}$ with a light cycle.
4. **Callus induction:** with auxin (2,4-D) to form an undifferentiated mass.
5. **Differentiation:** the ratio of **auxin to cytokinin** determines the result (high ratio for roots, low ratio for shoots).
6. **Hardening** of the plantlets and transfer to soil.

**Applications.**

| Application | Description | Example |
|---|---|---|
| **Micropropagation** | mass cloning | banana, orchids, potato, sugarcane |
| **Virus-free plants** | **meristem culture** (meristem is virus-free) | potato, sugarcane |
| **Haploid production** | **anther culture** | pure lines in rice |
| **Somaclonal variation** | useful variants | disease-resistant lines |
| **Protoplast fusion** | **somatic hybrids** | **pomato** (potato and tomato) |
| **Secondary metabolites** | cell suspension culture | shikonin, taxol, vincristine |
| **Embryo rescue** | grows hybrid embryos | wide crosses |
| **Germplasm storage** | cryopreservation in liquid nitrogen | rare species |
| **Production of synthetic seeds** | encapsulated somatic embryos | elite clones |

Orchids and the medicinal plants of Nepal, such as the Himalayan yew, can be propagated by tissue culture, which helps to conserve them.

**Numerical.** If one explant gives $5$ shoots each $4$ weeks, after four cycles one gets $5^4 = 625$ plantlets, and after five cycles $3125$ from a single explant in about $20$ weeks. A medium made at $30\ \text{g L}^{-1}$ sucrose needs $15\ \text{g}$ for $500\ \text{mL}$.

**Conclusion.** Because of totipotency, one cell or explant can be grown into a complete plant, so tissue culture produces large numbers of disease-free clones quickly.

### Model answer D2: plant breeding, biofertilisers and genetic engineering (10 marks)

**Introduction.** Crop production has to meet the needs of a growing population, and the strategies include conventional breeding, biofertilisers and biotechnology.

**Plant breeding.**

1. **Steps:** collection of variability (germplasm), evaluation and selection of parents, cross-hybridisation, selection and testing of the recombinants, and release of the new variety.
2. **Methods:** selection, hybridisation, mutation breeding (gamma rays), polyploidy breeding (colchicine) and **heterosis** (hybrid vigour in maize).
3. **The Green Revolution:** high-yielding dwarf wheat (Norman Borlaug) and rice (IR8) increased food production but needed fertiliser and water.
4. **Biofortification** improves nutrition, for example **iron-rich rice** and **provitamin A**-rich maize.

**Biofertilisers.** Living organisms that enrich the soil with nutrients.

| Biofertiliser | Organism | Function |
|---|---|---|
| Rhizobium | symbiotic bacteria in legume roots | fixes nitrogen |
| Azotobacter, Azospirillum | free-living bacteria | fix nitrogen |
| Anabaena with Azolla | cyanobacterium in fern | fixes nitrogen in rice fields |
| Mycorrhiza | fungi | take up phosphorus |
| Phosphate-solubilising bacteria | Pseudomonas | release phosphate |

They reduce the use of chemical fertilisers, cost less and are eco-friendly.

**Genetic engineering and GM crops.**

1. **Bt cotton:** the gene *cry* from *Bacillus thuringiensis* produces a protein toxin that kills the bollworm, so less pesticide is needed.
2. **Golden rice:** carries genes for **$\beta$-carotene** (provitamin A) to tackle vitamin A deficiency.
3. **Herbicide-resistant** soyabean, **Flavr Savr** tomato (slow ripening), and **virus-resistant** papaya.
4. **Tools:** a **vector** (the *Ti plasmid* of *Agrobacterium tumefaciens*) or a gene gun carries the gene into the plant cell, which is then regenerated by tissue culture.
5. **Concerns:** biosafety, allergy, effect on non-target insects, gene flow and the patent rights.

**Other topics.** **Single-cell protein** (*Spirulina*), biopesticides, **biogas** and the biodegradation of waste.

**Numerical.** If a field of $10$ hectares fixes $40\ \text{kg N ha}^{-1}$ with *Rhizobium* in a legume crop, the saving is $400\ \text{kg}$ of nitrogen, which is the same as $400/0.46 = 870\ \text{kg}$ of urea. A GM crop that cuts $6$ pesticide sprays to $2$, for a $4$-spray saving, reduces the cost by $4\times1500 = 6000$ rupees per hectare (if each spray costs Rs. 1500).

**Conclusion.** Breeding, biofertilisers and genetic engineering together help to raise yield, cut chemical use and improve the nutritional value of crops.

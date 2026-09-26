---
subject: Chemistry
grade: 12
unit: 18
title: Chemistry in the service of mankind
hours: 4
area: Applied Chemistry
---

This unit is a survey of the four families of manufactured chemicals that changed
ordinary life: polymers, dyes, drugs and pesticides. Nothing here is hard, but
there is a great deal to *know* — monomers, linkages, classes, examples — and the
examiner asks for exactly those names and examples. Read it as a set of tables to
be learned rather than as theory to be derived.

::: key What the examiner wants from this unit
Almost every question is one of four kinds: distinguish **addition from
condensation** polymerisation with examples; give the **monomer, type and use** of
a named polymer; classify **dyes** by structure or by method of application; or
classify **drugs** and explain antiseptic versus disinfectant. Learn the tables.
:::

## 18.1 Polymers: addition and condensation; elastomers and fibres; natural and synthetic

::: definition Polymer and monomer
A **polymer** is a very large molecule built by joining many small repeating
units. Each small unit is a **monomer**, and the process is **polymerisation**.
The number of monomer units in one chain is the **degree of polymerisation**, n.
:::

```figure caption="Addition polymerisation joins unsaturated monomers with nothing left over; condensation polymerisation joins bifunctional monomers and expels a small molecule such as water at every link."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(5.1,2.9))
ax.set_xlim(0,11); ax.set_ylim(0,6.4); ax.axis('off')

# --- addition ---
ax.text(0.0, 5.9, 'Addition', fontsize=9.0, color=INK, fontweight='bold')
for i in range(3):
    x = 0.55 + i*1.25
    ax.add_patch(Circle((x, 4.75), 0.42, fc='#dbe7f4', ec=SERIES[0], lw=1.2))
    ax.text(x, 4.75, 'M', fontsize=8.0, ha='center', va='center', color=INK)
ax.annotate('', xy=(5.55, 4.75), xytext=(4.45, 4.75),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.3, mutation_scale=11))
for i in range(3):
    x = 6.1 + i*0.92
    ax.add_patch(Circle((x, 4.75), 0.42, fc='#dbe7f4', ec=SERIES[0], lw=1.2))
    ax.text(x, 4.75, 'M', fontsize=8.0, ha='center', va='center', color=INK)
    if i < 2:
        ax.plot([x+0.42, x+0.50], [4.75, 4.75], color=INK, lw=1.4)
ax.text(5.0, 5.25, 'nothing lost', fontsize=7.4, color=MUTED, ha='center')
ax.text(0.0, 3.85, 'n CH₂=CH₂  →  –(CH₂–CH₂)ₙ–   polythene',
        fontsize=8.0, color=MUTED)

# --- condensation ---
ax.text(0.0, 2.95, 'Condensation', fontsize=9.0, color=INK, fontweight='bold')
for i in range(3):
    x = 0.4 + i*1.30
    c = '#dff0e6' if i % 2 == 0 else '#fbe9e4'
    e = SERIES[2] if i % 2 == 0 else SERIES[1]
    ax.add_patch(Rectangle((x, 1.42), 0.86, 0.80, fc=c, ec=e, lw=1.2))
    ax.text(x+0.43, 1.82, 'A' if i % 2 == 0 else 'B', fontsize=8.0,
            ha='center', va='center', color=INK)
ax.annotate('', xy=(5.55, 1.82), xytext=(4.45, 1.82),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.3, mutation_scale=11))
for i in range(3):
    x = 6.0 + i*0.95
    c = '#dff0e6' if i % 2 == 0 else '#fbe9e4'
    e = SERIES[2] if i % 2 == 0 else SERIES[1]
    ax.add_patch(Rectangle((x, 1.42), 0.86, 0.80, fc=c, ec=e, lw=1.2))
    ax.text(x+0.43, 1.82, 'A' if i % 2 == 0 else 'B', fontsize=8.0,
            ha='center', va='center', color=INK)
    if i < 2:
        ax.plot([x+0.86, x+0.95], [1.82, 1.82], color=INK, lw=1.4)
        ax.text(x+0.90, 2.62, 'H₂O', fontsize=7.2, color=SERIES[1], ha='center')
        ax.annotate('', xy=(x+0.90, 2.45), xytext=(x+0.90, 2.05),
                    arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0,
                                    mutation_scale=8))
ax.text(0.0, 0.55, 'n HOOC(CH₂)₄COOH + n H₂N(CH₂)₆NH₂  →  nylon-6,6 + 2n H₂O',
        fontsize=8.0, color=MUTED)
```

| | Addition polymerisation | Condensation polymerisation |
|---|---|---|
| Monomer | one unsaturated monomer (C=C) | two bifunctional monomers (or one with two different groups) |
| Small molecule lost | **none** | H₂O, HCl or NH₃ at every link |
| Empirical formula | same as the monomer | different from the monomers |
| Mechanism | chain (free radical, ionic or coordination) | step growth |
| Examples | polythene, PVC, Teflon, polystyrene, polypropene | nylon-6,6, terylene, bakelite, silicones |

Polymers are also classified by **behaviour**:

| Class | Intermolecular force | Behaviour | Examples |
|---|---|---|---|
| Elastomers | weakest; coiled chains, few cross-links | stretch several times their length and snap back | natural rubber, buna-S, neoprene |
| Fibres | strongest; hydrogen bonding, close packing | thread-like, high tensile strength, sharp melting point | nylon-6,6, terylene, silk |
| Thermoplastics | intermediate; linear or lightly branched | soften on heating, can be remoulded again and again | polythene, PVC, polystyrene |
| Thermosetting | three-dimensional cross-links | set permanently on moulding; char rather than melt | bakelite, melamine, urea–formaldehyde |

and by **origin**: **natural** (starch, cellulose, proteins, natural rubber, DNA),
**semi-synthetic** (rayon, cellulose acetate, vulcanised rubber) and **synthetic**
(polythene, PVC, nylon, bakelite).

::: example Worked example 18.1 — degree of polymerisation
**Problem.** A sample of PVC has an average molar mass of 93,750 g mol⁻¹.
Calculate its degree of polymerisation. (C = 12, H = 1, Cl = 35.5)

**Solution.** The monomer is chloroethene, CH₂=CHCl:

M(monomer) = 2(12) + 3(1) + 35.5 = 62.5 g mol⁻¹

In addition polymerisation nothing is lost, so the polymer mass is simply n times
the monomer mass:

$$ n = \frac{M_{\text{polymer}}}{M_{\text{monomer}}} = \frac{93750}{62.5} = 1500 $$

The chain contains **1500** chloroethene units.
:::

## 18.2 Synthetic polymers: polythene, PVC, Teflon, polystyrene, nylon and bakelite

| Polymer | Monomer(s) | Type | Conditions | Uses |
|---|---|---|---|---|
| **Polythene (LDPE)** | ethene, CH₂=CH₂ | addition | 1000–2000 atm, 350–570 K, trace O₂ | branched and flexible: carrier bags, squeeze bottles, cable insulation |
| **Polythene (HDPE)** | ethene | addition | Ziegler–Natta catalyst TiCl₄ + Al(C₂H₅)₃, 6–7 atm, 333–343 K | linear and tough: buckets, pipes, the black rooftop water tanks of Kathmandu |
| **PVC** | chloroethene, CH₂=CHCl | addition | free-radical initiator, 350 K | pipes, raincoats, floor tiles, wire insulation |
| **Teflon (PTFE)** | tetrafluoroethene, CF₂=CF₂ | addition | persulphate catalyst, high pressure | non-stick cookware, gaskets, plumbers' tape; inert and heat-resistant |
| **Polystyrene** | styrene, C₆H₅CH=CH₂ | addition | free-radical initiator | thermocol packing, disposable cups, insulation |
| **Nylon-6,6** | hexamethylenediamine + adipic acid | condensation | ~553 K, high pressure | ropes, fishing nets, parachutes, tyre cord, textiles |
| **Bakelite** | phenol + methanal (HCHO) | condensation | acid or alkali catalyst, heat | electrical switches, plugs, saucepan handles — a thermoset |

Repeat units, written out:

- Polythene: –(CH₂–CH₂)ₙ–
- PVC: –(CH₂–CHCl)ₙ–
- Teflon: –(CF₂–CF₂)ₙ–
- Polystyrene: –(CH₂–CH(C₆H₅))ₙ–
- Nylon-6,6: –[NH–(CH₂)₆–NH–CO–(CH₂)₄–CO]ₙ–  (an **amide** linkage)

n H₂N(CH₂)₆NH₂ + n HOOC(CH₂)₄COOH → –[NH(CH₂)₆NHCO(CH₂)₄CO]ₙ– + 2n H₂O

::: caution "Nylon-6,6" is not a random name
The two 6s are the numbers of **carbon atoms in each monomer**: six in
hexamethylenediamine and six in adipic acid. Nylon-6 is made from a single
monomer, caprolactam, which also has six carbons. Do not write nylon-6,6 as an
addition polymer — it loses water at every link, so it is a condensation polymer.
:::

::: example Worked example 18.2 — mass of nylon from its monomers
**Problem.** 14.6 g of adipic acid reacts completely with hexamethylenediamine to
give nylon-6,6. Calculate the mass of polymer and the mass of water formed.
(Adipic acid M = 146, hexamethylenediamine M = 116)

**Solution.** Moles of adipic acid = 14.6 / 146 = 0.100 mol, and the two monomers
react 1 : 1, so 0.100 mol of the diamine (11.6 g) is used.

Each link expels **two** molecules of water, so each repeat unit has mass

M(repeat unit) = 146 + 116 − 2(18) = 226 g mol⁻¹

Mass of nylon = 0.100 × 226 = **22.6 g**

Mass of water = 0.200 × 18 = **3.6 g**

Check: 14.6 + 11.6 = 26.2 g in, and 22.6 + 3.6 = 26.2 g out. Mass is conserved.
:::

## 18.3 Dyes

::: definition Dye
A dye is a coloured organic compound that can be fixed firmly to a fabric and
keeps its colour on exposure to light, washing and mild acids or alkalis.
:::

According to **Witt's theory**, a dye molecule needs two kinds of group:

- A **chromophore** — the colour-bearing group, always unsaturated:
  –N=N– (azo), –NO₂, –NO, >C=O, –C=C– or a quinonoid ring.
- An **auxochrome** — a group such as –OH, –NH₂, –NHR, –NR₂, –SO₃H or –COOH that
  deepens the colour and, more importantly, **binds the dye to the fibre**.

A compound with a chromophore but no auxochrome is merely coloured (a *chromogen*),
not a dye: azobenzene is orange but washes straight out of cloth.

```figure caption="Methyl orange. The azo group –N=N– is the chromophore; the dimethylamino and sulphonate groups are auxochromes, which deepen the colour and anchor the dye to the fibre."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Circle
fig, ax = plt.subplots(figsize=(5.1,2.4))
ax.set_xlim(-1.5, 8.2); ax.set_ylim(-1.5, 1.6); ax.axis('off')

def ring(cx, cy, r=0.62):
    ax.add_patch(RegularPolygon((cx, cy), 6, radius=r, orientation=np.pi/6,
                                fc='none', ec=INK, lw=1.4))
    ax.add_patch(Circle((cx, cy), r*0.55, fc='none', ec=MUTED, lw=1.0))
    return r

r = 0.62
ring(0.9, 0.0); ring(4.9, 0.0)
def line(x1, x2, y=0.0, n=1, c=INK):
    for o in ([0] if n == 1 else [0.07, -0.07]):
        ax.plot([x1, x2], [y+o, y+o], color=c, lw=1.4, solid_capstyle='round')
line(-0.28, 0.9-r)                      # NMe2 to ring
line(0.9+r, 2.28)                       # ring to first N
line(3.32, 4.9-r)                       # second N to ring
line(2.72, 3.08, n=2, c='#A8271F')      # N=N double bond
line(4.9+r, 6.1)                        # ring to sulphonate
ax.text(-0.45, 0.0, '(CH₃)₂N', fontsize=9.5, ha='right', va='center', color=SERIES[0])
ax.text(2.50, 0.0, 'N', fontsize=10.5, ha='center', va='center', color='#A8271F')
ax.text(3.30, 0.0, 'N', fontsize=10.5, ha='center', va='center', color='#A8271F')
ax.text(6.2, 0.0, 'SO₃Na', fontsize=9.5, ha='left', va='center', color=SERIES[2])
ax.annotate('chromophore  –N=N–', xy=(2.9, 0.20), xytext=(2.9, 1.25),
            ha='center', fontsize=8.0, color='#A8271F',
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.1, mutation_scale=9))
ax.annotate('auxochrome', xy=(-0.55, -0.20), xytext=(-0.2, -1.2),
            ha='center', fontsize=8.0, color=SERIES[0],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.1, mutation_scale=9))
ax.annotate('auxochrome', xy=(6.4, -0.20), xytext=(6.2, -1.2),
            ha='center', fontsize=8.0, color=SERIES[2],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.1, mutation_scale=9))
```

**Classification by structure**

| Structural class | Chromophore | Examples |
|---|---|---|
| Azo dyes | –N=N– | methyl orange, congo red, aniline yellow |
| Triphenylmethane dyes | quinonoid ring | malachite green, magenta (rosaniline) |
| Indigoid dyes | >C=O with C=C | indigo, tyrian purple |
| Anthraquinone dyes | two >C=O on a fused ring | alizarin |
| Nitro and nitroso dyes | –NO₂, –NO | picric acid, naphthol yellow S |
| Phthalein dyes | quinonoid | phenolphthalein, fluorescein |

**Classification by method of application**

| Application class | How it is fixed | Fibres | Example |
|---|---|---|---|
| Acid dyes | sodium salts of sulphonic acids; dyed from an acid bath | wool, silk, nylon | methyl orange, orange II |
| Basic dyes | coloured cation binds acidic sites in the fibre | wool, silk, mordanted cotton | malachite green, aniline yellow |
| Direct dyes | applied straight from a hot neutral bath | cotton, rayon | congo red |
| Vat dyes | reduced to a soluble colourless *leuco* form, absorbed, then re-oxidised in the fibre by air | cotton | **indigo** (the blue of denim) |
| Mordant dyes | a metal salt (alum, chrome) is fixed first and the dye forms a coloured complex with it | cotton, wool | alizarin — red with Al³⁺, violet with Fe³⁺ |
| Disperse dyes | fine insoluble particles dissolve into the fibre | polyester, nylon, acetate | disperse red |
| Reactive dyes | form a **covalent** bond with –OH of cellulose | cotton | procion dyes |
| Ingrain (azoic) dyes | the dye is synthesised inside the fibre by coupling | cotton | para red |

Indigo (*nīl*) was one of the oldest trade dyes of the Terai and the north Indian
plains, and is still the vat dye that colours denim.

## 18.4 Drugs

::: definition Drug
A drug is a chemical substance, natural or synthetic, of low molecular mass that
interacts with a biological target to give a therapeutic effect — the diagnosis,
prevention, relief or cure of disease. Treatment of disease with chemicals is
**chemotherapy**.
:::

**Characteristics of a good drug**

- It should be **effective at a small dose** against the specific disease.
- It should show **selective toxicity**: destroy the pathogen without harming the
  patient's own cells.
- It should have minimum side effects and **should not be habit-forming**.
- It should be stable on storage, cheap, and easy to administer and absorb.
- Its products should be excreted, not stored in the body.

**Natural and synthetic drugs**

| Natural drug | Source | Synthetic drug | Made from |
|---|---|---|---|
| Quinine | bark of *Cinchona* | Chloroquine | synthetic antimalarial |
| Morphine, codeine | opium poppy latex | Aspirin | salicylic acid + ethanoic anhydride |
| Penicillin | mould *Penicillium notatum* | Paracetamol | p-aminophenol |
| Reserpine | *Rauwolfia serpentina* (sarpagandha, grown in the Nepali Terai) | Sulphadiazine | sulphanilic acid derivatives |

**Classification of common drugs**

| Class | Action | Examples |
|---|---|---|
| Analgesic | relieves pain | aspirin, paracetamol, ibuprofen, morphine (narcotic) |
| Antipyretic | brings down fever | paracetamol, aspirin |
| Antibiotic | produced by micro-organisms; kills or inhibits other micro-organisms | penicillin, amoxicillin, streptomycin, chloramphenicol |
| Antiseptic | kills microbes on **living** tissue | dettol (chloroxylenol), tincture of iodine, boric acid |
| Disinfectant | kills microbes on **non-living** surfaces | 1 % phenol, bleaching powder, formalin |
| Tranquilliser / sedative | relieves anxiety, induces calm or sleep | diazepam, chlordiazepoxide, barbiturates |
| Antacid | neutralises excess acid in the stomach | Mg(OH)₂, Al(OH)₃, NaHCO₃, omeprazole |
| Antihistamine | suppresses allergy | cetirizine, chlorpheniramine |
| Antimalarial | kills the malaria parasite | chloroquine, quinine, artemisinin |
| Anaesthetic | causes loss of sensation | general: diethyl ether, halothane, N₂O; local: lignocaine |

::: caution Antiseptic and disinfectant are the *same* chemicals at different strengths
Phenol is an **antiseptic** at about 0.2 % and a **disinfectant** at 1 %. The
difference is not the compound but where and how strongly it is used: antiseptics
go on living tissue, disinfectants on floors, drains and instruments. Writing
"phenol is a disinfectant" without the concentration loses the mark.
:::

**Habit-forming drugs and drug addiction.** Some drugs act on the central nervous
system and produce **dependence**: the user needs ever-larger doses (tolerance),
and stopping causes withdrawal symptoms.

| Type | Effect | Examples |
|---|---|---|
| Stimulants | excite the nervous system | caffeine, nicotine, amphetamine, cocaine |
| Depressants / sedatives | slow the nervous system | alcohol, barbiturates, diazepam |
| Narcotic analgesics | kill pain and induce sleep and euphoria | opium, morphine, heroin ("brown sugar"), codeine |
| Hallucinogens | distort perception | cannabis (*gānjā*, charas), LSD |

Addiction damages the liver, brain, kidneys and heart; injecting drugs spreads HIV
and hepatitis B through shared needles. In Nepal the **Narcotic Drugs (Control)
Act, 2033 B.S. (1976)** prohibits the cultivation, production, sale, trafficking
and consumption of cannabis, opium and coca products, and makes addiction itself
punishable; treatment is through counselling, rehabilitation centres and community
support.

## 18.5 Pesticides: insecticides, herbicides and fungicides

A **pesticide** is any chemical used to kill or control organisms that damage
crops, stored food or health. The three groups examined are named after their
target.

| Group | Target | Examples | Notes |
|---|---|---|---|
| **Insecticides** | insects | DDT, BHC/lindane (organochlorines); malathion, parathion, chlorpyrifos (organophosphates); carbaryl (carbamate); pyrethrins and neem oil (natural) | organochlorines persist for years; organophosphates break down faster but are acutely toxic nerve poisons |
| **Herbicides** (weedicides) | weeds | 2,4-D, glyphosate, atrazine, sodium chlorate, paraquat | 2,4-D kills broad-leaved weeds and leaves cereals standing |
| **Fungicides** | fungi, moulds, blights | Bordeaux mixture (CuSO₄ + Ca(OH)₂), copper oxychloride, sulphur dust, mancozeb | Bordeaux mixture is still sprayed on potato and tomato blight in the hills |

**Why they are regulated.** DDT does not break down; it dissolves in fat and is
passed up the food chain, so its concentration multiplies at every step —
**biomagnification**.

```figure caption="Biomagnification of DDT through an estuary food chain (classic Long Island survey). The concentration rises by a factor of about ten million from water to fish-eating birds."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.8))
levels = ['water', 'plankton', 'small fish', 'large fish', 'fish-eating birds']
ppm    = [0.000003, 0.04, 0.5, 2.0, 25.0]
cols   = [MUTED, SERIES[2], SERIES[0], SERIES[3], SERIES[1]]
ax.barh(levels, ppm, color=cols, height=0.6)
ax.set_xscale('log'); ax.set_xlim(1e-6, 1e3)
ax.set_xlabel('DDT concentration (ppm, log scale)')
for lv, v in zip(levels, ppm):
    ax.text(v*1.8, lv, f'{v:g}', va='center', fontsize=7.8, color=INK)
ax.invert_yaxis()
ax.spines[['top','right','left']].set_visible(False)
ax.grid(True, axis='x', alpha=.45)
```

Pesticide residues on vegetables, poisoning of the farmers who spray without
protection, death of bees and fish, and the growth of resistant pests are the
other costs. In Nepal, pesticides are registered and controlled by the **Plant
Quarantine and Pesticide Management Centre** under the Pesticide Act, 2048 B.S.
(1991). More than twenty pesticides are banned outright — among them DDT, aldrin,
dieldrin, endrin, BHC, methyl parathion and endosulfan — and paraquat, chlorpyrifos
and phorate were added in recent years. Rapid residue-testing laboratories, such
as the one at the Kalimati fruit and vegetable market in Kathmandu, screen
incoming produce before it reaches the retail stalls.

::: example Worked example 18.3 — sorting a medicine cabinet
**Problem.** Classify each of the following and, in one line, say what it does:
paracetamol, amoxicillin, tincture of iodine, magnesium hydroxide, diazepam,
2,4-D, indigo, Teflon.

**Solution.**

| Substance | Class | Action |
|---|---|---|
| Paracetamol | analgesic and antipyretic | relieves pain and lowers fever |
| Amoxicillin | antibiotic | kills bacteria; made from a penicillin nucleus |
| Tincture of iodine | antiseptic | kills microbes on a cut, i.e. on living tissue |
| Magnesium hydroxide | antacid | neutralises excess HCl in the stomach: Mg(OH)₂ + 2HCl → MgCl₂ + 2H₂O |
| Diazepam | tranquilliser | relieves anxiety; habit-forming, so prescription-only |
| 2,4-D | herbicide | kills broad-leaved weeds in a cereal field |
| Indigo | vat dye | the blue of denim; applied as its soluble leuco form |
| Teflon | addition polymer (PTFE) | non-stick, chemically inert coating |
:::

## Chapter summary

- A polymer is many monomers joined; n is the degree of polymerisation and
  M(polymer) = n × M(monomer) for an addition polymer.
- Addition polymerisation needs an unsaturated monomer and loses nothing;
  condensation polymerisation needs bifunctional monomers and expels H₂O, HCl or
  NH₃ at each link.
- Elastomers stretch and recover (rubber), fibres are strong and thread-like
  (nylon), thermoplastics remould on heating (polythene), thermosets do not
  (bakelite).
- Key polymers: polythene (ethene), PVC (chloroethene), Teflon (tetrafluoroethene),
  polystyrene (styrene) — all addition; nylon-6,6 (hexamethylenediamine + adipic
  acid) and bakelite (phenol + methanal) — both condensation.
- A dye needs a **chromophore** (–N=N–, –NO₂, >C=O, quinonoid) for colour and an
  **auxochrome** (–OH, –NH₂, –SO₃H) to deepen it and fix it to the fibre.
- Dyes by structure: azo, triphenylmethane, indigoid, anthraquinone, nitro,
  phthalein. By application: acid, basic, direct, vat, mordant, disperse, reactive
  and ingrain.
- A good drug is effective at low dose, selectively toxic, non habit-forming and
  excretable. Classes: analgesic, antipyretic, antibiotic, antiseptic,
  disinfectant, tranquilliser, antacid, antihistamine, antimalarial, anaesthetic.
- Antiseptics act on living tissue, disinfectants on non-living surfaces — often
  the same compound at different concentrations (phenol 0.2 % vs 1 %).
- Habit-forming drugs: stimulants, depressants, narcotic analgesics and
  hallucinogens; controlled in Nepal by the Narcotic Drugs (Control) Act, 2033.
- Pesticides are insecticides, herbicides or fungicides. Persistent
  organochlorines such as DDT biomagnify up the food chain and are banned in Nepal.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is a condensation polymer? <span class="marks">[1]</span>
   (a) polythene (b) PVC (c) nylon-6,6 (d) Teflon
2. The monomer of Teflon is <span class="marks">[1]</span>
   (a) CH₂=CHCl (b) CF₂=CF₂ (c) CH₂=CH₂ (d) C₆H₅CH=CH₂
3. In Witt's theory, –N=N– is a <span class="marks">[1]</span>
   (a) auxochrome (b) chromophore (c) mordant (d) leuco group
4. Indigo is applied to cotton as a <span class="marks">[1]</span>
   (a) acid dye (b) basic dye (c) vat dye (d) disperse dye
5. Which is used as an antacid? <span class="marks">[1]</span>
   (a) aspirin (b) diazepam (c) Mg(OH)₂ (d) chloroquine
6. 2,4-D is a <span class="marks">[1]</span>
   (a) fungicide (b) herbicide (c) insecticide (d) rodenticide

::: note Answers to Group A
**1.** (c) — water is eliminated at every amide link.
**2.** (b) — tetrafluoroethene gives –(CF₂–CF₂)ₙ–.
**3.** (b) — the azo group carries the colour.
**4.** (c) — it is reduced to the soluble leuco form, absorbed, then air-oxidised
inside the fibre.
**5.** (c) — Mg(OH)₂ + 2HCl → MgCl₂ + 2H₂O.
**6.** (b) — 2,4-dichlorophenoxyacetic acid kills broad-leaved weeds.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between addition and condensation polymerisation, with two examples
   of each. <span class="marks">[5]</span>
2. Give the monomer, type of polymerisation and one use of polythene, PVC,
   polystyrene and bakelite. <span class="marks">[5]</span>
3. What is a dye? Explain Witt's theory with methyl orange as the example, and
   classify dyes on the basis of their method of application. <span class="marks">[5]</span>
4. Define a drug. State four characteristics of a good drug and distinguish
   between an antiseptic and a disinfectant with examples. <span class="marks">[5]</span>
5. A sample of polythene has an average molar mass of 42,000 g mol⁻¹. Find its
   degree of polymerisation. <span class="marks">[5]</span>
6. What are habit-forming drugs? Name the four types with one example each and
   state two harmful effects of drug addiction. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** See the table in §18.1. Addition: unsaturated monomer, nothing eliminated,
same empirical formula (polythene, PVC). Condensation: bifunctional monomers, a
small molecule such as H₂O eliminated, different empirical formula (nylon-6,6,
bakelite).

**2.** Polythene — ethene, addition, carrier bags and water tanks. PVC —
chloroethene, addition, pipes and raincoats. Polystyrene — styrene, addition,
thermocol packing. Bakelite — phenol + methanal, condensation, electrical switches.

**3.** A dye is a coloured compound that can be fixed to a fabric and resists light
and washing. Witt: a **chromophore** gives colour and an **auxochrome** deepens it
and binds the dye to the fibre. In methyl orange the chromophore is –N=N– and the
auxochromes are –N(CH₃)₂ and –SO₃Na. By application: acid, basic, direct, vat,
mordant, disperse, reactive and ingrain dyes (one example each, as in §18.3).

**4.** A drug is a low-molecular-mass chemical that acts on a biological target to
diagnose, prevent or cure disease. Good drug: effective at a small dose,
selectively toxic, few side effects, not habit-forming (also stable, cheap,
excretable). An **antiseptic** (dettol, tincture of iodine) is applied to living
tissue; a **disinfectant** (1 % phenol, bleaching powder) to floors, drains and
instruments. Phenol is an antiseptic at 0.2 % and a disinfectant at 1 %.

**5.** Monomer is ethene, M = 28 g mol⁻¹. $n = 42000/28 = \mathbf{1500}$ units.

**6.** Habit-forming (addictive) drugs act on the central nervous system and cause
tolerance and dependence. Stimulants — amphetamine; depressants — barbiturates;
narcotic analgesics — morphine; hallucinogens — cannabis. Harmful effects: damage
to liver, brain and kidneys; spread of HIV and hepatitis B through shared needles;
loss of study, work and family life. Controlled in Nepal by the Narcotic Drugs
(Control) Act, 2033.
:::

**Group C — Long answer (8 marks each)**

1. (a) Classify polymers on the basis of the mode of polymerisation, of physical
   properties and of origin, giving two examples of each class. <span class="marks">[5]</span>
   (b) Write the equation for the formation of nylon-6,6 and calculate the mass of
   nylon obtained from 29.2 g of adipic acid with excess diamine. <span class="marks">[3]</span>
2. (a) Classify dyes on the basis of structure, with an example of each. <span class="marks">[4]</span>
   (b) What are pesticides? Distinguish between insecticides, herbicides and
   fungicides with two examples each, and give two harmful effects of using
   persistent pesticides such as DDT. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) By mode: addition (polythene, PVC) and condensation (nylon-6,6,
bakelite). By physical property: elastomers (natural rubber, buna-S), fibres
(nylon-6,6, terylene), thermoplastics (polythene, polystyrene), thermosets
(bakelite, melamine). By origin: natural (starch, cellulose), semi-synthetic
(rayon, cellulose acetate) and synthetic (nylon, PVC).
(b) n H₂N(CH₂)₆NH₂ + n HOOC(CH₂)₄COOH → –[NH(CH₂)₆NHCO(CH₂)₄CO]ₙ– + 2n H₂O.
Moles of adipic acid = 29.2 / 146 = 0.200 mol; repeat-unit mass = 146 + 116 − 36
= 226 g mol⁻¹; mass of nylon = 0.200 × 226 = **45.2 g** (with 0.400 × 18 = 7.2 g of
water).

**2.** (a) Azo (methyl orange), triphenylmethane (malachite green), indigoid
(indigo), anthraquinone (alizarin), nitro (picric acid), phthalein
(phenolphthalein).
(b) A pesticide is a chemical used to kill or control pests. Insecticides kill
insects (DDT, malathion); herbicides kill weeds (2,4-D, glyphosate); fungicides
kill fungi (Bordeaux mixture, sulphur dust). Harmful effects of DDT-type
pesticides: they persist for years and **biomagnify** up the food chain, poisoning
fish and birds at the top; residues remain on food and cause chronic poisoning of
farmers; pests also develop resistance. DDT is banned in Nepal for this reason.
:::

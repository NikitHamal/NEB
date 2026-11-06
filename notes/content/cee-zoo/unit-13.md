---
subject: Zoology
grade: CEE
unit: 13
title: Medical Technology and Applied Biology
hours: 2
area: Applied Zoology
---

This unit is rated at **2 questions** in this book's estimate of the
40-question Zoology paper. It is definition-heavy, but the best questions are
procedural: why grafts are rejected, which infertility problem IVF or ICSI
bypasses, what amniocentesis actually samples, and which microorganism performs
each useful fermentation or stage of waste treatment.

::: key What the paper asks from this chapter
- Grafts: **auto-** self, **iso-** genetically identical, **allo-** same species but genetically different, **xeno-** different species. HLA mismatch drives rejection.
- IVF fertilises an oocyte outside the body; **ICSI** injects one sperm into an oocyte and is used especially for severe male-factor infertility.
- Amniocentesis samples **amniotic fluid and fetal cells**, usually for diagnostic karyotyping/genetic testing—not for routine sex selection.
- A transgenic animal carries an intentionally introduced, heritable gene; “pharming” makes useful proteins in milk or another accessible product.
- Dairy lactic-acid bacteria convert **lactose → lactic acid**; *Saccharomyces* converts sugars to ethanol + CO₂ in beverages and CO₂ for raising dough.
- Sewage treatment: primary = physical settling; secondary = microbial oxidation in activated sludge/biofilms; sludge digestion is anaerobic and yields methane.
- BOD is the oxygen microorganisms need to oxidise biodegradable organic matter; *E. coli* is an indicator of faecal contamination of drinking water.
- *Bacillus thuringiensis* Cry protoxins are activated in susceptible insect midguts; *Trichoderma* antagonises plant-pathogenic fungi.
:::

## 13.1 Tissue and organ transplantation, IVF, amniocentesis and transgenic animals

### Transplantation and graft rejection

**Transplantation** replaces a diseased cell population, tissue or organ—such
as haematopoietic stem cells, skin, cornea, kidney, liver, heart or lung—with
a healthy graft. Grafts are named by genetic relationship:

| Graft | Donor → recipient | Immunological expectation |
|---|---|---|
| **Autograft** | one site to another in same person | no foreign-HLA rejection |
| **Isograft/syngeneic graft** | genetically identical individual (identical twin) | normally accepted |
| **Allograft** | genetically different member of same species | rejection unless matched/immunosuppressed |
| **Xenograft** | different species | strongest incompatibility; pig-to-human use remains specialised/research territory |

The major barrier is recognition of donor **human leukocyte antigens (HLA)**,
the human MHC molecules, as non-self. **Hyperacute rejection** occurs within
minutes/hours when preformed antibodies attack graft vessels. **Acute
rejection** over days to months is commonly T-cell-mediated and/or antibody-
mediated. **Chronic rejection** slowly scars and narrows graft vessels/tissue.
ABO compatibility, HLA matching and a donor–recipient crossmatch reduce risk,
and immunosuppressive drugs suppress lymphocyte activation. Their necessary
trade-off is vulnerability to infection and some cancers.

The cornea is relatively **immune-privileged** and avascular, so corneal grafts
often succeed with less systemic immunosuppression. Bone-marrow/
haematopoietic stem-cell transplantation is exceptional in the opposite way:
donor immune cells may attack the recipient in **graft-versus-host disease**.

Ethical transplantation also requires valid consent, fair allocation and a
strict prohibition of organ trafficking/coercion. Medical technology does not
remove those constraints; it makes them more important.

### In-vitro fertilisation (IVF)

**IVF** is fertilisation in laboratory culture rather than in a uterine tube.
A typical cycle includes controlled ovarian stimulation and ultrasound/hormone
monitoring, a maturation trigger, ultrasound-guided oocyte retrieval, sperm
preparation, fertilisation, embryo culture and transfer of an embryo to the
uterus. Suitable extra embryos may be cryopreserved.

```figure caption="The IVF sequence. The laboratory replaces the blocked or non-functioning meeting place of sperm and oocyte; development after transfer must still occur in the uterus."
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.2, 3.0))
ax.set_xlim(0,10.6); ax.set_ylim(0,6.6); ax.axis('off')

def box(x,y,w,h,txt,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.07,rounding_size=0.12',fc=fc,ec=MUTED,lw=0.9,zorder=3))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=6.4,color=INK,zorder=4,linespacing=1.25)
def arr(p,q):
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=9,lw=1.15,color=MUTED,zorder=2))
box(0.25,4.35,3.05,1.30,'1. Ovarian stimulation\nand monitoring','#eaf1f8')
box(3.85,4.35,3.05,1.30,'2. Oocyte retrieval\n+ sperm preparation','#f3e9fb')
box(7.45,4.35,2.90,1.30,'3. Fertilisation\nIVF or ICSI','#fff1d6')
box(7.45,1.25,2.90,1.30,'4. Embryo culture\n(day 3–5)','#e8f5e9')
box(3.85,1.25,3.05,1.30,'5. Embryo transfer\nto uterus','#fdeeed')
box(0.25,1.25,3.05,1.30,'6. Pregnancy test\n± embryo freezing','#eef0f3')
arr((3.32,5.00),(3.82,5.00)); arr((6.92,5.00),(7.42,5.00))
arr((8.90,4.32),(8.90,2.58)); arr((7.42,1.90),(6.93,1.90)); arr((3.82,1.90),(3.33,1.90))
```

IVF is especially useful for bilateral tubal blockage, severe endometriosis,
some ovulatory/unexplained infertility and cases requiring donor gametes or
pre-implantation genetic testing. In **intracytoplasmic sperm injection
(ICSI)**, an embryologist injects a single selected sperm into a mature
oocyte; it can bypass very low sperm count, poor motility or previous failed
fertilisation. IVF is not a guarantee of a baby: maternal age and embryo
chromosome normality strongly influence success, and risks include ovarian
hyperstimulation syndrome, multiple pregnancy when more than one embryo
implants, procedural complications and cost.

### Amniocentesis

In **amniocentesis**, usually after about 15 weeks of pregnancy, a fine needle
is guided by ultrasound through the abdominal/uterine wall to withdraw a small
sample of amniotic fluid. The fluid contains fetal cells whose chromosomes/DNA
can be used for karyotyping, chromosomal microarray or selected single-gene
tests; biochemical measurements may assess some fetal conditions.

It is a **diagnostic** test rather than a screening test. Non-invasive prenatal
testing of cell-free DNA in maternal blood can screen risk with no needle into
the uterus, but abnormal screening generally requires a diagnostic procedure
such as amniocentesis or chorionic-villus sampling for confirmation.
Amniocentesis carries a small risk of leakage, infection or pregnancy loss and
may require anti-D protection for an Rh-negative patient. Its purpose is
diagnosis and informed care; misuse for non-medical sex selection is ethically
and legally unacceptable.

### Transgenic animals

A **transgenic animal** has a deliberately introduced gene (transgene) stably
integrated into its genome and potentially transmitted to offspring. Methods
include pronuclear microinjection into a zygote, engineered embryonic stem
cells, viral vectors and targeted genome editing. “Transgenic” is not a synonym
for clone: a clone copies a nuclear genome, whereas transgenesis changes the
genetic content.

Uses include:

- **Disease models:** mice carrying human disease-related genes or targeted
  knockouts reveal mechanisms and test treatments.
- **Pharming:** mammary-specific promoters make goats/cows secrete a human
  therapeutic protein in milk, from which it can be purified.
- **Improved production/research traits:** growth, milk composition, disease
  resistance or biomaterials have all been investigated.
- **Xenotransplantation research:** pigs are edited to remove pig antigens and
  add human regulatory genes, aiming to reduce hyperacute rejection.

Risks and safeguards include insertion-site effects, animal welfare,
escape/gene flow, food/environmental safety assessment, containment and
traceability. A scientifically successful founder animal is not automatically
a socially or legally approved product.


::: example Worked example — matching the technique to the medical problem
A question describes three couples: (i) the woman's fallopian tubes are blocked; (ii) the man produces very few, weakly motile sperms; (iii) the man produces **no** sperms in the semen because of a blocked vas deferens. Choose the assisted-reproduction route for each.

- **(i) Blocked tubes:** fertilisation cannot occur in the body, so use **IVF** — ova are collected, fertilised in the laboratory, and the embryo is transferred to the uterus. **GIFT** would be wrong here: it places gametes *into the tube*, which is the blocked segment.
- **(ii) Very few, weak sperms:** ordinary IVF may fail because a sperm must still penetrate the ovum. Use **ICSI** — a single sperm is injected directly into the ovum.
- **(iii) No sperms in semen but testes normal:** sperms are retrieved surgically from the testis/epididymis and then used for **ICSI**.

The method is always chosen by asking *which step of natural conception is failing* — meeting of gametes, penetration of the ovum, or delivery of sperms.
:::

::: caution Trap — the three speeds of graft rejection
**Hyperacute** rejection (minutes) is caused by **pre-formed antibodies** in the recipient; **acute** rejection (days–weeks) is mainly **T-cell mediated**; **chronic** rejection (months–years) is slow vascular damage. MCQs swap these. Adjacent traps: an **isograft** (identical twin) is not rejected; graft compatibility is decided by **HLA (MHC)** matching; **cyclosporine** protects grafts by suppressing T-cells.
:::


```figure caption="Secondary sewage treatment in one line of work: screened and settled sewage is aerated so activated-sludge flocs of bacteria and fungi oxidise the dissolved organic matter, the sludge then settles out, and disinfection finishes the water before discharge — while the drawn-off sludge digests anaerobically into biogas."
flow([("primary", "screens,\nsediment"),
      ("aeration", "sludge flocs\neat organics"),
      ("settling", "sludge out,\nwater on"),
      ("disinfect", "chlorine\nor UV"),
      ("digester", "methanogens\n→ biogas")], figsize=(5.2, 2.15))
```

::: example BOD arithmetic, exactly as the paper computes it
**Problem.** A river-water sample's dissolved oxygen reads 7.5 mg/L; after
five days at 20 °C it reads 2.5 mg/L. What is the BOD? A sewage sample must
be diluted 1 : 10 before the same test, and shows the same 5 mg/L drop. What
is its true BOD?
**Solution.** Undiluted: BOD = 7.5 − 2.5 = **5 mg/L** — moderately clean
water. Diluted: the drop must be multiplied by the dilution factor:
5 × 10 = **50 mg/L** — heavily polluted, which is precisely why it needed
diluting: the microbes consumed all the oxygen the bottle could hold.
:::
## 13.2 Applied microbiology: dairy and beverage microbes, sewage and drinking-water treatment, bio-control agents

### Dairy and beverage fermentation

In curd/yoghurt, **lactic-acid bacteria** ferment lactose mainly to lactic
acid. As pH approaches about 4.6, casein micelles lose stability and form a
gel. Classic yoghurt cultures are *Streptococcus thermophilus* and
*Lactobacillus delbrueckii* subsp. *bulgaricus*; many curds use mixed
*Lactococcus/Lactobacillus* cultures. Acidification also suppresses many
spoilage organisms and creates flavour compounds. In cheese, starter acid and
rennet form curd; ripening organisms then create texture/flavour.
*Propionibacterium* produces CO₂ “eyes” in Swiss-type cheese, while
*Penicillium roqueforti* and *P. camemberti* ripen blue and soft cheeses.

The beverage and bread yeast ***Saccharomyces cerevisiae*** carries out
alcoholic fermentation:

$$\mathrm{C_6H_{12}O_6 \rightarrow 2C_2H_5OH + 2CO_2}$$

In bread, CO₂ raises the dough and most ethanol evaporates during baking. In
beer/wine, sugars come from malted grain or fruit and ethanol remains.
Distillation—not yeast—then concentrates ethanol in spirits. *Acetobacter*
can oxidise ethanol aerobically to acetic acid in vinegar production.

### Sewage treatment

Sewage treatment uses physical separation first and then harnesses microbial
food webs.

| Stage | Process | What is removed/changed |
|---|---|---|
| **Preliminary/primary** | screens, grit chambers, sedimentation | rags, grit and settleable solids (**primary sludge**) |
| **Secondary biological** | activated-sludge aeration or biofilm systems such as trickling filters | aerobic bacteria/fungi/protozoa consume dissolved/colloidal organic matter; BOD falls greatly |
| **Secondary clarification** | flocs settle | part is returned as activated sludge to maintain biomass; excess goes to sludge treatment |
| **Tertiary/disinfection where required** | nutrient removal, filtration, chlorine/UV/ozone | nitrogen/phosphorus and pathogens reduced further |
| **Sludge treatment** | thickening and anaerobic digestion | methanogenic archaea produce CH₄-rich biogas; volume and pathogen load fall, though safe disposal rules still apply |

```figure caption="Conventional sewage treatment. Physical settling prepares the water; aerobic microbial flocs perform most organic removal; anaerobic archaea turn sludge into biogas."
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.2, 3.1))
ax.set_xlim(0,10.8); ax.set_ylim(0,6.4); ax.axis('off')

def box(x,y,w,h,title,body,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.07,rounding_size=0.12',fc=fc,ec=MUTED,lw=0.9,zorder=3))
    ax.text(x+w/2,y+h/2+0.28,title,ha='center',va='center',fontsize=6.5,color=INK,fontweight='bold',zorder=4)
    ax.text(x+w/2,y+h/2-0.34,body,ha='center',va='center',fontsize=6.1,color=INK,zorder=4,linespacing=1.2)
def arr(p,q,c=MUTED):
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=9,lw=1.15,color=c,zorder=2))
box(0.20,3.95,2.35,1.45,'PRIMARY','screens + settling','#eaf1f8')
box(3.05,3.95,2.45,1.45,'SECONDARY','aerated flocs\nconsume organics','#e8f5e9')
box(6.00,3.95,2.15,1.45,'CLARIFIER','flocs settle','#fff1d6')
box(8.65,3.95,1.95,1.45,'DISINFECT','treated\neffluent','#f3e9fb')
box(4.45,0.85,3.20,1.35,'SLUDGE DIGESTER','anaerobic archaea → biogas','#fdeeed')
arr((2.57,4.68),(3.02,4.68)); arr((5.52,4.68),(5.97,4.68)); arr((8.17,4.68),(8.62,4.68))
arr((7.05,3.92),(6.85,2.24))
arr((5.95,4.20),(5.52,4.20),SERIES[2])
ax.text(5.73,3.48,'returned activated sludge',fontsize=6.1,color=SERIES[2],ha='center')
ax.text(1.35,5.82,'sewage in',fontsize=6.4,color=MUTED,ha='center')
arr((1.35,5.62),(1.35,5.43))
```

**Biochemical oxygen demand (BOD)** is the dissolved oxygen used by
microorganisms to oxidise biodegradable matter under standard test conditions
(usually 5 days at 20 °C). Raw sewage has high BOD; if discharged untreated,
microbial respiration can deoxygenate a river and kill fish. A good treatment
plant transfers that oxidation into an engineered aeration tank, so BOD in the
effluent is much lower.

::: example BOD load removed by a treatment plant
A plant treats $2.0\times10^6$ L day⁻¹ of sewage with BOD 300 mg L⁻¹ and removes
90% of that load. Incoming BOD load is

$$300\ \text{mg L}^{-1}\times2.0\times10^6\ \text{L day}^{-1}=6.0\times10^8\ \text{mg day}^{-1}=600\ \text{kg day}^{-1}$$

Ninety percent removal is $0.90\times600=540$ kg day⁻¹ of oxygen-demanding
load prevented from reaching the receiving river.
:::

### Drinking-water treatment

Safe drinking water uses multiple barriers rather than one chemical step:
source protection; **coagulation/flocculation** to aggregate fine particles;
sedimentation; rapid or slow sand **filtration** (the latter includes a
biologically active surface layer); and **disinfection** by chlorine, UV light
or ozone. Chlorine has the advantage of a residual that helps protect water in
pipes, while UV leaves no residual. Boiling is an effective household barrier
when fuel and safe storage permit.

Laboratories usually test for ***Escherichia coli*** as an indicator organism.
Its presence does not prove that every pathogen is present; it signals recent
faecal contamination and hence a pathway by which typhoid, cholera and viral
enteric pathogens could enter. Safe water should contain no *E. coli* in a
100 mL sample.

### Biological control agents

**Biocontrol** uses a pest's natural enemies or microbial products to suppress
it below an economic/medical threshold.

| Agent | Target/mode |
|---|---|
| ***Bacillus thuringiensis* (Bt)** | spores/Cry protoxins are eaten by insect larvae; alkaline midgut and gut receptors activate pore-forming toxin, causing gut paralysis/death |
| **Baculoviruses (NPVs)** | highly host-specific viruses infect and kill particular caterpillar pests |
| ***Trichoderma* spp.** | fungi that parasitise/antagonise soil-borne plant-pathogenic fungi and compete in the rhizosphere |
| **Parasitoid wasps, ladybirds, spiders** | parasitism/predation of insect pests |
| ***Bacillus thuringiensis israelensis*** | larvicide for mosquito/blackfly larvae in suitable water bodies |

Compared with broad-spectrum chemical pesticides, biocontrol can be specific,
leave fewer toxic residues and fit integrated pest management. It may act more
slowly, require correct timing/storage and be sensitive to ultraviolet light or
weather. Resistance to Bt can evolve, so refuges of non-Bt host plants and
rotation/monitoring are part of responsible deployment.


::: caution Trap — BOD runs "backwards"
A **high BOD** (biochemical oxygen demand) means **heavily polluted** water: microbes need much oxygen to decompose the large organic load. Clean river water has a *low* BOD. Two linked traps: **primary** sewage treatment is only physical (screening, sedimentation); the **secondary** stage is the biological one (aerobic microbes in activated sludge), and in the anaerobic digester **methanogen** bacteria produce biogas.
:::



```figure caption="Applied microbiology in four shelves: the fermenters that feed us, the yeast that brews and leavens, the microbial engineers of sewage and drinking water, and the living pesticides of biocontrol. Every shelf is a species doing its ordinary chemistry at our service."
cards([
    ("Dairy", "Lactobacillus: curd, yoghurt\nlactose → lactic acid\ncheese: rennet + Penicillium"),
    ("Brewing and baking", "Saccharomyces cerevisiae\nsugar → ethanol + CO₂\nCO₂ leavens the bread"),
    ("Water and sewage", "activated sludge: BOD down\nmethanogens: biogas\nalum, sand, chlorine"),
    ("Biocontrol", "Bt: Cry toxin for caterpillars\nTrichoderma, ladybirds\nbaculoviruses: one pest"),
], cols=2, figsize=(6.2, 3.0))
```

::: caution
Three pairs the paper swaps: **Dolly = clone, Rosie = transgenic** (cloning
copies a genome, transgenesis adds a gene); **ZIFT transfers the zygote to
the oviduct, IVF-ET the embryo to the uterus**; **secondary sewage treatment
is biological, primary is physical** — 'secondary' sounds lesser and is in
fact the heart of the plant.
:::

```photogrid label="13.1" cols="2" ratio="1.2" caption="Cleaning sewage in two stages. (a) An aeration tank of an activated-sludge plant, where bubbled air feeds the bacteria that digest the waste. (b) Biochemical oxygen demand (BOD) measures the organic load as the oxygen that microbes need. Raw sewage of 250 mg/L loses 35 per cent in primary settling (to 162.5 mg/L) and 90 per cent of the rest in the aeration tank and clarifier (to 16.25 mg/L), an overall removal of 93.5 per cent. A town sending 1 million litres a day would otherwise release 250 kg of BOD daily; after treatment only 16.2 kg. Water fit for discharge must usually stay below about 30 mg/L."
@ photo id="bio12/aeration-tank" cap="Aeration tank of a sewage plant"
fit 1.2
focus 0.5 0.5
@ svg cap="BOD at each stage (mg/L)"
b0 = 250.0
b1 = b0 * (1 - 0.35)
b2 = b1 * (1 - 0.90)
tot = 100 * (b0 - b2) / b0
assert abs(b1 - 162.5) < 1e-9 and abs(b2 - 16.25) < 1e-9 and abs(tot - 93.5) < 1e-9
facts = dict(b1="%.1f" % b1, b2="%.2f" % b2, tot="%.1f" % tot, in_="%.0f" % (b0 * 1e6 / 1e6), out="%.1f" % (b2 * 1e6 / 1e6))
f = Fig(300, 236)
f.text(150, 12, "Raw sewage to effluent", size=10.5, color=NAVY, bold=True)
for i, (lab, v, c, fl) in enumerate((("raw sewage", b0, RED, ROSE), ("after primary settling (-35%)", b1, AMBER, SAND), ("after activated sludge (-90%)", b2, TEAL, MINT))):
    y = 30 + i * 46
    f.text(10, y, lab, size=10.5, color=SLATE, anchor="start")
    w = v / 250 * 210
    f.box(10, y + 8, w, 22, fill=fl, stroke=c, r=2)
    f.text(10 + w + 6, y + 19, "%.4g" % v, size=10.5, color=c, bold=True, anchor="start", vmid=True)
f.text(150, 186, "overall removal = 93.5 per cent", size=10.5, color=NAVY, bold=True)
f.text(150, 204, "1 ML/day: 250 kg BOD in, 16.3 kg out", size=10.5, color=SLATE, bold=True)
```

## Formula and fact sheet

- Autograft = self; isograft = identical genotype; allograft = same species,
  different genotype; xenograft = different species.
- Rejection is driven mainly by HLA/MHC and, in hyperacute cases, preformed antibodies.
- IVF = oocyte retrieval + laboratory fertilisation + embryo culture/transfer.
- ICSI = one sperm injected into one mature oocyte; strongest use is severe male factor.
- Amniocentesis = ultrasound-guided sample of amniotic fluid/fetal cells for diagnosis.
- Transgenic = heritable inserted gene; pharming = pharmaceutical protein from a transgenic animal.
- Lactic fermentation: lactose → lactic acid → casein gel in curd/yoghurt.
- Alcoholic fermentation: $\mathrm{C_6H_{12}O_6\to2C_2H_5OH+2CO_2}$.
- Sewage: primary physical → secondary aerobic biological → clarification →
  disinfection; sludge anaerobic digestion gives methane.
- BOD falls when treatment succeeds. Drinking-water *E. coli* = faecal indicator.
- Bt protoxin requires ingestion and susceptible insect-midgut activation.

### Rapid-revision tables and high-yield facts

| Quantity | Value |
|---|---|
| Graft types | auto (self), iso (twin), allo (human), xeno (species) |
| Rejection / drug | T cells vs foreign MHC / cyclosporine |
| IVF milestones | Louise Brown 1978; ICSI 1992 |
| Amniocentesis window | 15–20 weeks; karyotype, sex-selection banned |
| Down syndrome / Klinefelter / Turner | 47,+21 / 47,XXY / 45,X |
| Fermentation | sugar → ethanol + CO₂ (yeast); lactose → lactic acid (Lactobacillus) |
| BOD test | DO drop over 5 days at 20 °C; × dilution factor |
| Biogas | methane 50–70 %, CO₂; methanogens, anaerobic |
| Water standard | no E. coli; chlorine/UV/ozone disinfection |
| Bt | Cry toxin, alkaline-gut specific to caterpillars |

## Chapter summary

- Transplant compatibility is an immunological problem centred on HLA
  recognition; immunosuppression prevents rejection at the cost of infection risk.
- IVF moves fertilisation to the laboratory, while ICSI additionally bypasses
  failures of sperm number, movement or oocyte penetration.
- Amniocentesis provides fetal cells for definitive chromosome/DNA diagnosis,
  but as an invasive test it follows careful counselling and screening.
- Transgenic animals produce disease models and valuable proteins, yet require
  welfare, containment and biosafety oversight.
- Dairy and beverage industries are controlled fermentations whose acids,
  gases and ethanol explain product texture, preservation and flavour.
- Sewage treatment relocates microbial oxidation from rivers to engineered
  aeration systems and extracts energy from sludge by anaerobic digestion.
- Drinking-water safety is a multi-barrier process monitored with faecal
  indicator organisms.
- Biocontrol uses ecological specificity—especially Bt, baculoviruses and
  *Trichoderma*—as an alternative or complement to chemical pesticides.

## Practice questions

**Set A — Recall (25 questions)**

1. A graft between genetically identical individuals is called an
   (a) autograft (b) isograft (c) allograft (d) xenograft
2. A kidney transferred between unrelated humans is an
   (a) autograft (b) isograft (c) allograft (d) xenograft
3. The main molecular barrier to organ transplantation is incompatibility of
   (a) HLA/MHC antigens (b) blood plasma volume (c) mitochondrial DNA only (d) donor age
4. Immunosuppressive treatment after transplantation mainly reduces
   (a) lymphocyte-mediated rejection (b) oxygen transport (c) urine production (d) bone growth
5. Corneal grafts often need less systemic immunosuppression because the cornea is
   (a) heavily vascularised (b) relatively immune-privileged and avascular (c) made of cartilage (d) replaced every day
6. In IVF, fertilisation occurs
   (a) in the uterus (b) in the ovary (c) outside the body in culture (d) in the cervix
7. ICSI involves injection of
   (a) an embryo into a sperm (b) many sperm into the uterus (c) a nucleus into an egg (d) one sperm into a mature oocyte
8. A day-5 embryo commonly transferred in IVF is at the
   (a) blastocyst stage (b) zygote stage only (c) gastrula stage (d) fetal stage
9. Amniocentesis samples fetal cells from the
   (a) maternal blood only (b) placenta surface (c) umbilical artery (d) amniotic fluid
10. Karyotyping of cells obtained by amniocentesis can diagnose
   (a) maternal anaemia (b) fetal chromosomal abnormalities (c) adult hypertension (d) paternal infertility
11. A transgenic animal is one carrying a
   (a) temporary vaccine only (b) hybrid nucleus from mating (c) stably integrated introduced gene (d) cloned mitochondrion only
12. Production of a human therapeutic protein in transgenic goat milk is called
   (a) pasteurisation (b) hybridisation (c) gene silencing (d) pharming
13. Lactic-acid bacteria in curd ferment mainly
   (a) cellulose to methane (b) ethanol to acetic acid (c) lactose to lactic acid (d) casein to lactose
14. The classic paired yoghurt cultures are *Streptococcus thermophilus* and
   (a) *Bacillus thuringiensis* (b) *Saccharomyces cerevisiae* (c) *Lactobacillus delbrueckii* (d) *Escherichia coli*
15. Alcoholic fermentation by yeast produces ethanol and
   (a) lactic acid (b) carbon dioxide (c) methane (d) oxygen
16. The gas holes in Swiss-type cheese are produced mainly by
   (a) methanogens (b) *Penicillium* spores (c) nitrogen-fixing bacteria (d) *Propionibacterium*
17. Primary sewage treatment is principally a
   (a) viral process (b) physical settling process (c) photosynthetic process (d) distillation process
18. Activated sludge treatment depends on microbial flocs that are mainly
   (a) obligate anaerobes in sealed tanks (b) photosynthetic algae only (c) human epithelial cells (d) aerobic bacteria and associated organisms
19. BOD measures the oxygen required by microorganisms to oxidise
   (a) biodegradable organic matter (b) sand and grit (c) dissolved nitrogen gas (d) glass particles
20. Anaerobic digestion of sewage sludge yields a gas rich in
   (a) oxygen (b) chlorine (c) nitrogen (d) methane
21. Which is a common drinking-water disinfectant leaving a protective residual?
   (a) ethanol (b) chlorine (c) lactic acid (d) methane
22. *E. coli* in drinking water is used primarily as an indicator of
   (a) hardness (b) excess dissolved oxygen (c) faecal contamination (d) fluoride deficiency
23. Bt toxin kills susceptible insect larvae after activation in the
   (a) insect midgut (b) human stomach only (c) plant xylem (d) soil water
24. *Trichoderma* species are used in biocontrol chiefly against
   (a) influenza viruses (b) soil-borne fungal plant pathogens (c) mosquito adults (d) tapeworms
25. Methane-producing organisms in biogas digesters belong mainly to the
   (a) Archaea (b) fungi (c) protozoa (d) viruses

::: note Answers and explanations — Set A
**1.** (b) — An isograft is between genetically identical donor and recipient.
**2.** (c) — Same-species but genetically different transplantation is allogeneic.
**3.** (a) — Recipient immunity recognises foreign HLA/MHC molecules.
**4.** (a) — Immunosuppression limits T-cell and antibody-mediated graft attack.
**5.** (b) — Corneal avascularity and immune privilege reduce rejection risk.
**6.** (c) — “In vitro” means fertilisation is performed in laboratory culture.
**7.** (d) — ICSI injects one sperm directly into the oocyte cytoplasm.
**8.** (a) — Extended culture to about day 5 produces a blastocyst.
**9.** (d) — Amniotic fluid contains shed fetal cells.
**10.** (b) — Chromosome number/structure can be examined in fetal cells.
**11.** (c) — A transgene is integrated into the genome and can be inherited.
**12.** (d) — Pharming harvests pharmaceuticals from transgenic animals.
**13.** (c) — Lactose fermentation yields acid that gels casein.
**14.** (c) — *L. delbrueckii* subsp. *bulgaricus* partners *S. thermophilus* in yoghurt.
**15.** (b) — Glucose fermentation gives two ethanol and two CO₂ per glucose.
**16.** (d) — Propionibacteria release CO₂ that forms cheese eyes.
**17.** (b) — Screening and sedimentation physically remove solids.
**18.** (d) — Aerated flocs contain bacteria and grazers that oxidise organics.
**19.** (a) — BOD quantifies microbial oxygen demand from biodegradable pollution.
**20.** (d) — Methanogenic archaea produce methane-rich biogas.
**21.** (b) — Chlorine disinfects and can leave a distribution residual.
**22.** (c) — *E. coli* indicates a faecal contamination pathway.
**23.** (a) — Bt protoxin is solubilised/activated in susceptible larval midguts.
**24.** (b) — *Trichoderma* antagonises fungal pathogens in soil/root zones.
**25.** (a) — Methanogens are anaerobic archaea, not bacteria.
:::

**Set B — Understanding (15 questions)**

1. An allograft is rejected mainly because recipient T cells and antibodies recognise donor tissue as
   (a) non-self through HLA differences (b) too large to vascularise (c) lacking mitochondria (d) always infected
2. Long-term immunosuppression creates a clinical trade-off because suppressing rejection also increases susceptibility to
   (a) infection and some cancers (b) chromosomal trisomy (c) lactose intolerance (d) excessive antibody memory
3. IVF can treat bilateral fallopian-tube blockage because oocytes are retrieved and fertilised
   (a) inside the blocked tube (b) in the laboratory before uterine transfer (c) by amniocentesis (d) after natural implantation
4. ICSI is preferred over conventional IVF in severe male-factor infertility because it bypasses requirements for sperm
   (a) number, motility and oocyte penetration (b) DNA and mitochondria (c) production in the testis (d) ABO compatibility
5. Amniocentesis is diagnostic rather than merely screening because it obtains
   (a) a maternal risk score (b) fetal cells for direct chromosome/DNA analysis (c) an ultrasound picture only (d) adult blood cells
6. A clone and a transgenic animal differ because transgenesis specifically involves
   (a) asexual reproduction only (b) transfer into a uterus (c) deliberate introduction or editing of a gene (d) identical twins
7. Transgenic mice are valuable disease models because a defined human-related gene or mutation can be
   (a) removed from all food (b) studied in a whole living mammal (c) made invisible to immunity (d) converted into milk
8. Milk sets into curd when lactic acid lowers pH so that casein micelles
   (a) lose stability and form a gel (b) become lactose (c) begin photosynthesis (d) dissolve completely
9. The same yeast can raise bread and make beer because fermentation produces both ethanol and CO₂, but in bread the valued product is mainly
   (a) lactic acid (b) methane (c) carbon dioxide (d) acetic acid
10. Returning settled activated sludge to an aeration tank maintains a high concentration of
   (a) chlorine (b) grit (c) sterile water (d) pollutant-consuming microorganisms
11. Untreated high-BOD sewage can kill fish mainly by causing microbial respiration to deplete
   (a) sunlight (b) calcium carbonate (c) nitrogen gas (d) dissolved oxygen
12. Coagulation and flocculation improve drinking-water treatment by aggregating fine particles so they can be removed by
   (a) boiling only (b) chlorination alone (c) sedimentation and filtration (d) anaerobic digestion
13. Bt preparations are relatively selective because the Cry protoxin must be ingested and activated by conditions/receptors in the
   (a) human lung (b) susceptible insect midgut (c) roots of every plant (d) blood of mammals
14. A major advantage of biocontrol in integrated pest management is that it can suppress pests with greater target specificity and fewer
   (a) chromosomes (b) pollinators (c) nutrients (d) persistent chemical residues
15. In anaerobic digestion, methane formation is the final stage after hydrolysis, acid formation and acetate/H₂ production by
   (a) photosynthetic algae (b) the recipient's T cells (c) yeast distillation (d) interacting bacteria and methanogenic archaea

::: note Answers and explanations — Set B
**1.** (a) — Alloimmunity is directed at genetically different donor antigens, especially HLA.
**2.** (a) — The same immune suppression that protects a graft weakens defence against microbes/tumours.
**3.** (b) — Laboratory fertilisation bypasses the anatomical tubal meeting site.
**4.** (a) — Direct injection compensates for too few, poorly motile or non-penetrating sperm.
**5.** (b) — Direct fetal-cell analysis can establish a diagnosis rather than estimate risk.
**6.** (c) — Cloning copies; transgenesis alters genetic content.
**7.** (b) — Whole-animal models expose gene effects across interacting tissues and systems.
**8.** (a) — Near its isoelectric pH, casein precipitates/gels.
**9.** (c) — CO₂ inflates dough; most ethanol is lost in baking.
**10.** (d) — Returned sludge seeds and maintains the working microbial biomass.
**11.** (d) — Decomposition consumes dissolved oxygen faster than it is replaced.
**12.** (c) — Larger flocs settle and filter much more effectively than colloids.
**13.** (b) — Alkaline pH, proteases and specific receptors make activation host-selective.
**14.** (d) — Specific biological agents can reduce broad chemical exposure and residues.
**15.** (d) — Anaerobic digestion is a microbial food chain ending in methanogenesis.
:::

**Set C — Application (10 questions)**

1. Ignoring recombination, the probability that two full siblings are HLA-identical is about
   (a) 100% (b) 50% (c) 75% (d) 25%
2. An amniocentesis karyotype reported as 47,XY,+21 indicates a male fetus with
   (a) Turner syndrome (b) Klinefelter syndrome (c) Down syndrome (d) cri-du-chat syndrome
3. A couple has normal gametes but both uterine tubes are irreversibly blocked. The most direct assisted-reproduction method is
   (a) amniocentesis (b) artificial insemination only (c) chorionic-villus sampling (d) IVF with embryo transfer
4. A semen sample contains very few weakly motile sperm. The IVF modification most appropriate is
   (a) embryo freezing (b) donor insemination only (c) ICSI (d) tubal surgery
5. Sewage with BOD 250 mg L⁻¹ undergoes 92% BOD removal. The approximate effluent BOD is
   (a) 250 mg L⁻¹ (b) 20 mg L⁻¹ (c) 92 mg L⁻¹ (d) 230 mg L⁻¹
6. Complete fermentation of 90 kg glucose has a theoretical ethanol yield of about
   (a) 23 kg (b) 46 kg (c) 90 kg (d) 180 kg
7. A transgenic goat secretes purified human antithrombin in its milk. This application is best called
   (a) pharming (b) amniocentesis (c) xenografting (d) pasteurisation
8. A kidney-transplant recipient on immunosuppressants develops invasive fungal infection mainly because treatment reduces
   (a) red-cell production only (b) cell-mediated immune surveillance (c) stomach acidity permanently (d) donor HLA expression to zero
9. *E. coli* is detected in a village drinking-water sample. The most justified interpretation is
   (a) faecal contamination and possible enteric-pathogen risk (b) proof that cholera toxin is present (c) water is safe if clear (d) excessive water hardness
10. A Bt spray kills a caterpillar pest but does not poison a farmer in the same direct way chiefly because the protoxin requires
   (a) activation/receptor conditions of the insect midgut (b) sunlight inside human blood (c) fertilisation in plant ovules (d) anaerobic sewage sludge

::: note Answers and explanations — Set C
**1.** (d) — Siblings inherit the same two parental HLA haplotypes in about one-quarter of cases.
**2.** (c) — 47 chromosomes with XY and an extra chromosome 21 is male trisomy 21.
**3.** (d) — IVF replaces tubal fertilisation/transport and returns the embryo to the uterus.
**4.** (c) — ICSI allows one viable sperm to be injected into each mature oocyte.
**5.** (b) — Remaining BOD is $250\times0.08=20$ mg L⁻¹.
**6.** (b) — 180 kg glucose yields $2\times46=92$ kg ethanol, so 90 kg yields 46 kg.
**7.** (a) — Pharmaceutical production in a transgenic animal is pharming.
**8.** (b) — Suppressed T-cell immunity predisposes to opportunistic fungal disease.
**9.** (a) — The indicator reveals a contamination route, not the identity of every pathogen.
**10.** (a) — Bt specificity depends on ingestion, gut pH/proteases and epithelial receptors.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe tissue and organ transplantation, in-vitro fertilisation, amniocentesis and transgenic animals. <span class="marks">[10]</span>
2. Describe the role of microbes in dairy and beverages, sewage and drinking-water treatment and biological control. <span class="marks">[10]</span>

```photogrid label="13.H" cols="4" ratio="1.25" caption="Biotechnology at work. (a) PCR amplifies a tiny sample of DNA. (b) A DNA gel under UV light shows bands used in identification. (c) An aeration tank of a sewage plant holds the activated sludge. (d) Plant tissue culture produces many identical plantlets."
@ photo id="bio12/pcr" cap="(a) PCR"
fit 1.25
focus 0.5 0.5
@ photo id="bio12/gel-uv" cap="(b) Gel under UV"
fit 1.25
focus 0.5 0.5
@ photo id="bio12/aeration-tank" cap="(c) Aeration tank"
fit 1.25
focus 0.5 0.5
@ photo id="cee-bot/tissue-culture" cap="(d) Tissue culture"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Medical technology (10 marks)

**Introduction.** Modern medicine uses transplantation, assisted reproduction, prenatal diagnosis and genetic engineering to treat disease and help families.

**1. Tissue and organ transplantation.** An organ or tissue of a **donor** replaces a failed one in the **recipient**.

| Type | Meaning |
|---|---|
| Autograft | From one part of the body to another (skin graft) |
| Isograft | Between identical twins |
| Allograft | Between two unrelated persons of one species (kidney) |
| Xenograft | Between species (pig heart valve) |

The immune system may cause **rejection**, so doctors match **HLA and blood group** and use **immunosuppressants** such as cyclosporin. Kidney transplants are done in Nepal; the organs can come from a living relative or a brain-dead donor.

**2. In-vitro fertilisation (IVF) — "test-tube baby".** Steps:

1. The woman receives hormones to produce several eggs.
2. Eggs are collected from the ovary and sperm from the male.
3. They are mixed in a dish (fertilisation outside the body).
4. The zygote divides to an 8-celled embryo.
5. The embryo is placed in the uterus (**embryo transfer**) for implantation.

Louise Brown (1978, UK) was the first IVF baby. **ZIFT and GIFT** place a zygote or the gametes in the oviduct.

**3. Amniocentesis.** At 15–18 weeks a needle takes a little **amniotic fluid** from the womb under ultrasound. The foetal cells are cultured and checked for chromosomal disorders such as **Down syndrome** (trisomy 21), and for metabolic diseases. Using it to find the sex of the baby for abortion is **illegal** in Nepal.

**4. Transgenic animals.** An animal that carries a foreign gene in its genome. Examples: mice for cancer research, **Rosie** the cow whose milk had human α-lactalbumin, sheep making human α-1-antitrypsin, and fish that grow faster. Uses: drug production, disease models, and safety testing of vaccines.

**Conclusion.** These technologies save lives and treat infertility, but they raise ethical issues that need laws and careful use.

### Model answer D2: Applied microbiology (10 marks)

**Introduction.** Microbes are used to make food, to clean water and to protect crops.

**1. Dairy and beverages.**

1. **Curd:** *Lactobacillus* (lactic acid bacteria) changes lactose to lactic acid, which coagulates milk protein and also gives vitamin B12.
2. **Cheese:** *Streptococcus lactis* ripens it; the holes in **Swiss cheese** come from CO₂ made by *Propionibacterium*.
3. **Alcoholic drinks:** yeast (*Saccharomyces cerevisiae*) ferments sugar into ethanol and CO₂: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂. Nepali **jaand** and raksi use this in a traditional way with *murcha* starter.
4. **Bread and idli:** yeast gas makes the dough rise.

**2. Sewage treatment.**

| Stage | Process |
|---|---|
| Primary | Screening, grit removal, sedimentation; solids settle as sludge |
| Secondary | Effluent goes to the **aeration tank**; air and **activated sludge** microbes digest organic matter, lowering the **BOD** (biological oxygen demand) |
| Tertiary | Chlorination or UV removes germs before discharge into a river |

The sludge is digested anaerobically in a digester to make **biogas** (methane), which is widely used in Nepali homes.

**3. Drinking-water treatment.** Sedimentation → **coagulation** with alum (flocs trap particles) → **filtration** through sand → **disinfection** by chlorine (0.2–0.5 mg/L) or boiling or the SODIS method.

**4. Biological control.** Pests are controlled by living organisms.

1. ***Bacillus thuringiensis* (Bt)** toxin kills caterpillars.
2. **Baculovirus** controls insect pests.
3. ***Trichoderma*** fungus protects plants from soil fungi.
4. **Ladybird beetles** eat aphids, and ***Gambusia*** fish eat mosquito larvae.

**Advantages.** No chemical residue, safe for man and soil, and cheaper for farmers who practise organic farming in Nepal.

**Conclusion.** Microbes provide food, clean water and natural pest control, which makes them very important to human welfare.

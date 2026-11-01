---
subject: Zoology
grade: CEE
unit: 4
title: Plasmodium, Earthworm and Frog
hours: 6
area: Study of Selected Animals
---

Study of Selected Animals carries **6 of the 40 Zoology questions** — more
than any other single chapter outside Human Biology. Three type animals are
named: the malarial parasite *Plasmodium* (habitat, structure, life cycle and
the types of malaria), the earthworm *Pheretima posthuma* (morphology, body
systems, physiology and economic importance) and the frog *Rana tigrina*
(morphology, body systems and physiology). Expect about two questions on each,
almost all of them **numbers and names**: which segment, which stage, which
host, which species, which chamber.

::: key What the paper asks from this chapter
- *Plasmodium*: **female *Anopheles*** is the **definitive host** (sexual phase), **man the intermediate host** (asexual schizogony); **sporozoite** infects man, **gametocytes** infect the mosquito.
- The stages in order — liver schizogony → **erythrocytic (Golgi) cycle** → gametocytes → gametes in the mosquito stomach → zygote (the only diploid stage) → ookinete → **oocyst** on the stomach wall → sporozoites → **salivary glands**.
- The four classic species with their fever intervals: ***P. vivax*** benign tertian (48 h, relapses from hypnozoites), ***P. falciparum*** malignant tertian (cerebral malaria), ***P. malariae*** quartan (72 h), ***P. ovale*** ovale tertian.
- Earthworm segment numbers: **clitellum 14–16**, female pore **14**, male pores **18**, genital papillae **17 and 19**, spermathecal pores **5/6–8/9**, testes **10–11**, ovaries **13**, gizzard **8–9**, stomach **9–14**, caeca **26**, hearts **7, 9, 12, 13**.
- Earthworm physiology: **haemoglobin dissolved in plasma**, closed circulation, **cutaneous** respiration, three kinds of **nephridia**, protandrous hermaphrodite with **cross-fertilisation in the cocoon**.
- Frog: three ways of breathing, **buccal force pump**, **three-chambered heart** with **sinus venosus** (pacemaker) and **spiral valve**, nucleated RBCs, mesonephric kidneys, **urinogenital duct** in the male, **10 pairs of cranial nerves**, external fertilisation and **thyroxine-controlled metamorphosis**.
:::

## 4.1 Plasmodium: habitat, structure, life cycle and types of malaria

### Systematic position and habitat

| Rank | Taxon |
|---|---|
| Kingdom | Protista |
| Phylum | Protozoa (Apicomplexa) |
| Class | **Sporozoa** — no locomotory organelles, all parasitic, spore-forming |
| Genus | ***Plasmodium*** |

*Plasmodium* is an **intracellular, digenetic** (two-host) parasite.

| Host | Status | Where the parasite lives | Phase |
|---|---|---|---|
| **Man** | **intermediate (secondary) host** | **liver cells** (hepatocytes) and **red blood cells** | **asexual** — schizogony; gametocytes formed |
| **Female *Anopheles*** mosquito | **definitive (primary) host** and vector | **stomach (midgut) wall**, haemocoel and **salivary glands** | **sexual** — gamogony, fertilisation, sporogony |

Only the **female** *Anopheles* transmits malaria: the male feeds on plant
juices, while the female needs a blood meal to mature her eggs.

### Structure of the stages

| Stage | Structure | Where |
|---|---|---|
| **Sporozoite** | slender, **sickle- (spindle-) shaped**, about 10–15 μm; one central nucleus; pellicle with microtubules; **apical complex** (polar ring, rhoptries, micronemes) for entering cells; glides, no cilia or flagella | salivary glands of mosquito → injected into man; **the infective stage for man** |
| **Cryptozoite / schizont** | large multinucleate body formed in a liver cell | liver |
| **Merozoite** | small, oval, uninucleate; invades a fresh RBC | liver and blood |
| **Trophozoite** | feeding stage in the RBC; first a **signet-ring** (ring stage, a large vacuole with the nucleus at one side), then amoeboid; digests haemoglobin, leaving the brown pigment **haemozoin** | RBC |
| **Erythrocytic schizont** | multinucleate stage that divides into merozoites | RBC |
| **Gametocytes** | **microgametocyte** (male, smaller) and **macrogametocyte** (female, larger); round in *P. vivax*, **crescent-shaped** in *P. falciparum* | RBC; **the infective stage for the mosquito** |
| **Microgametes / macrogamete** | 4–8 slender flagellated microgametes from one microgametocyte (**exflagellation**); one macrogamete from each macrogametocyte | mosquito stomach |
| **Zygote → ookinete** | diploid zygote becomes a motile, worm-like **ookinete** | mosquito stomach |
| **Oocyst** | rounded cyst on the outer surface of the stomach wall | mosquito stomach wall |

### The life cycle

```figure caption="Life cycle of *Plasmodium vivax*. The asexual phase (schizogony) runs in man, the intermediate host; gamete formation, fertilisation and sporogony run in the female *Anopheles*, the definitive host. Each bite carries the parasite across."
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.2, 4.5))
ax.set_xlim(0, 10); ax.set_ylim(0.2, 9.0); ax.axis("off")
MAN, MOS = "#e7eff7", "#f6e7d8"
def box(xc, yc, text, fc, ec, w=3.75, h=1.5):
    ax.add_patch(FancyBboxPatch((xc - w / 2, yc - h / 2), w, h,
                 boxstyle="round,pad=0.03,rounding_size=0.18", fc=fc, ec=ec, lw=0.9))
    ax.text(xc, yc, text, ha="center", va="center", fontsize=6.7, color=INK,
            linespacing=1.3)
def arrow(p, q, c=INK, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9, lw=1.1,
                 color=c, connectionstyle=f"arc3,rad={rad}"))
L, R = 2.0, 8.0
ax.text(L, 8.75, "IN MAN — asexual phase", ha="center", fontsize=7.2,
        color=SERIES[0], fontweight="bold")
ax.text(L, 8.35, "(intermediate host)", ha="center", fontsize=6.6, color=SERIES[0])
ax.text(R, 8.75, "IN FEMALE MOSQUITO — sexual phase", ha="center", fontsize=7.2,
        color=SERIES[1], fontweight="bold")
ax.text(R, 8.35, "(definitive host)", ha="center", fontsize=6.6, color=SERIES[1])
box(L, 7.25, "Liver cell: sporozoite →\nschizont → thousands of\nmerozoites; hypnozoites\nmay lie dormant (relapse)", MAN, SERIES[0])
box(L, 5.05, "RBC (Golgi cycle): ring\ntrophozoite → schizont →\n12–24 merozoites; RBCs\nburst every 48 h → fever", MAN, SERIES[0])
box(L, 2.85, "Some merozoites form\nmicro- and macro-\ngametocytes in RBCs;\nno further growth in man", MAN, SERIES[0])
box(R, 2.85, "Stomach: microgametocyte\n→ 4–8 flagellated\nmicrogametes; macro-\ngametocyte → 1 macrogamete", MOS, SERIES[1])
box(R, 5.05, "Fertilisation → zygote\n(2n, the only diploid\nstage) → motile ookinete\nbores into stomach wall", MOS, SERIES[1])
box(R, 7.25, "Oocyst on stomach wall:\nmeiosis, then thousands\nof sporozoites (sporogony)\n→ salivary glands", MOS, SERIES[1])
arrow((L, 6.48), (L, 5.82), SERIES[0])
arrow((L, 4.28), (L, 3.62), SERIES[0])
arrow((R, 3.62), (R, 4.28), SERIES[1])
arrow((R, 5.82), (R, 6.48), SERIES[1])
arrow((L + 1.9, 4.7), (L + 1.9, 5.4), SERIES[0], rad=1.3)
arrow((R - 1.9, 7.25), (L + 1.9, 7.25), INK)
ax.text(5.0, 7.55, "bite injects", ha="center", fontsize=6.6, color=INK)
ax.text(5.0, 6.8, "sporozoites", ha="center", fontsize=6.6, color=INK)
arrow((L + 1.9, 2.85), (R - 1.9, 2.85), INK)
ax.text(5.0, 3.15, "bite takes up", ha="center", fontsize=6.6, color=INK)
ax.text(5.0, 2.4, "gametocytes", ha="center", fontsize=6.6, color=INK)
ax.text(4.62, 5.05, "repeats", ha="left", va="center", fontsize=6.6, color=SERIES[0])
ax.text(L, 1.6, "schizogony in liver and RBCs", ha="center", fontsize=6.6, color=MUTED)
ax.text(R, 1.6, "gamogony + sporogony (Ross cycle)", ha="center", fontsize=6.6, color=MUTED)
ax.text(5.0, 0.75, "all stages haploid except zygote and ookinete", ha="center",
        fontsize=6.6, color=MUTED)
```

**A. In man — asexual phase (schizogony)**

1. **Infection.** A female *Anopheles* injects **sporozoites** with her saliva. Within about half an hour they leave the blood and enter **liver cells**.
2. **Pre-erythrocytic schizogony** (liver). Each sporozoite grows into a **schizont** that divides into thousands of **merozoites (cryptomerozoites)**; the liver cell bursts and they enter the blood. In *P. vivax* and *P. ovale* some sporozoites become dormant **hypnozoites**, which wake weeks or months later and cause **relapses**. (Older books describe a secondary liver cycle, the **exo-erythrocytic schizogony**; relapses are now explained by the hypnozoites.)
3. **Erythrocytic schizogony — the Golgi cycle.** A merozoite enters an RBC → **ring trophozoite** → amoeboid trophozoite, eating haemoglobin → **schizont** → **12–24 merozoites** (*P. vivax*). The RBCs burst **together**, releasing merozoites, cell debris and **haemozoin** into the plasma; this causes the **paroxysm of fever**. The merozoites attack fresh RBCs and the cycle repeats every **48 h** in *P. vivax*.
4. **Gametogony.** After several cycles some merozoites develop into **gametocytes** inside RBCs. They do not divide further in man; they wait to be sucked up by a mosquito.

The time from the bite to the first parasites in the blood is the **prepatent
period**; to the first fever, the **incubation period** — usually about two
weeks (12–17 days) for *P. vivax*.

**B. In the female Anopheles — sexual phase**

1. **Gamogony** (in the stomach, within minutes of the blood meal): the **microgametocyte** throws out **4–8 flagellated microgametes** (exflagellation); the **macrogametocyte** matures into one **macrogamete**. All other blood stages are digested.
2. **Fertilisation** (anisogamy) gives a **zygote** (synkaryon) — the **only diploid stage** — which becomes the motile, vermiform **ookinete**.
3. The ookinete bores through the stomach wall and rounds up beneath its outer lining as an **oocyst**.
4. **Sporogony**: the first division in the oocyst is **meiosis**, so all later stages are haploid; repeated divisions give thousands of **sporozoites**. The oocyst bursts, sporozoites drift through the haemocoel and collect in the **salivary glands**, ready for the next bite. Sporogony takes about **10–14 days** and stops in cold weather — one reason malaria is a disease of the warm Terai and not of the high hills.

::: caution Hosts and phases — the commonest reversal
The **definitive host** is the one in which **sexual reproduction**
(fertilisation) happens — the **mosquito**. Man, in whom only asexual
multiplication occurs, is the **intermediate host**, however much he suffers.
And the mosquito does **not** catch the infection from sporozoites: it needs
**gametocytes** in the blood it sucks.
:::

### The malarial fever

The **paroxysm** has three stages: a **cold stage** (shivering, 15–60 min), a
**hot stage** (fever up to 40–41 °C, 2–6 h) and a **sweating stage** (2–4 h), after
which the patient feels well until the next batch of RBCs bursts. Repeated
destruction of RBCs causes **anaemia** and an **enlarged spleen**
(splenomegaly). The fever is caused by **haemozoin** and other toxins released
when the RBCs rupture.

### Types of malaria

| Species | Malaria | Erythrocytic cycle (fever) | Distinctive points |
|---|---|---|---|
| ***P. vivax*** | **benign tertian** | **48 h** — fever every third day | commonest in Nepal and South Asia; infected RBCs enlarged with **Schüffner's dots**; **hypnozoites → relapse** |
| ***P. falciparum*** | **malignant tertian** (subtertian, pernicious) | **36–48 h**, irregular | **most dangerous**; invades RBCs of all ages, so parasite counts soar; **crescent-shaped gametocytes**; sticky infected RBCs block brain capillaries → **cerebral malaria**; **blackwater fever** (haemoglobin in urine); no hypnozoites |
| ***P. malariae*** | **quartan** | **72 h** — fever every fourth day | mild but long-lasting; band-shaped trophozoites |
| ***P. ovale*** | **ovale (mild) tertian** | **48 h** | rare, mainly tropical Africa; oval infected RBCs; hypnozoites → relapse |
| *P. knowlesi* | quotidian | 24 h | monkey malaria of South-East Asia that can infect man |

**Discovery.** **Charles Laveran (1880)** saw the parasite in human blood;
**Camillo Golgi** described the cycle in RBCs; **Ronald Ross (1897)** found the
oocysts in the stomach wall of *Anopheles* and proved transmission by the
mosquito (Nobel Prize 1902); **Grassi (1898)** completed the human cycle in
*Anopheles*; **Shortt and Garnham (1948)** found the liver stage.

**Diagnosis, treatment and control.** Thick and thin **blood smears** stained by
Giemsa or Leishman, or rapid antigen tests. Drugs: **quinine** (from *Cinchona*
bark), **chloroquine**, **primaquine** (kills hypnozoites and gametocytes — the
"radical cure" of vivax), and **artemisinin-based combination therapy (ACT)**
for falciparum (artemisinin from *Artemisia annua*). Control: insecticide-treated
**bed nets**, indoor residual spraying, draining stagnant water, the larvivorous
fish ***Gambusia***, and the new vaccines (RTS,S and R21). In Nepal most
remaining cases are *P. vivax* in the Terai or imported, and the country is
close to eliminating the disease.

**Sickle-cell trait.** Heterozygotes (HbA HbS) resist falciparum malaria: an
infected RBC sickles and is removed by the spleen before the parasite completes
its cycle — the classic example of **balanced polymorphism**.

| Feature | ***Anopheles*** (malaria) | ***Culex*** (filaria, Japanese encephalitis) |
|---|---|---|
| Resting posture | body at an angle (about 45°) to the surface | body parallel to the surface, "hunch-backed" |
| Palps of the female | as long as the proboscis | much shorter than the proboscis |
| Eggs | laid singly, each with lateral **floats** | laid in **rafts** |
| Larva | lies **parallel** to the water surface; no siphon | hangs at an angle; breathes by a **siphon** |
| Wings | spotted | unspotted |

::: example How fast does a vivax infection grow?
**Problem.** A single infected RBC releases 16 merozoites at the end of each 48-hour cycle, and every merozoite infects a new RBC. Ignoring losses, how many RBCs are infected after three complete cycles?

**Solution.** The number multiplies by 16 each cycle: $16^3 = 4096$ infected RBCs in 6 days. After six cycles (12 days) it would be $16^6 \approx 1.7 \times 10^7$ — which is why symptoms appear about two weeks after a bite.
:::

## 4.2 Earthworm (Pheretima): morphology, body systems, physiology and economic importance

### Position, habit and habitat

***Pheretima posthuma*** (phylum **Annelida**, class **Oligochaeta**) is the
common earthworm of Nepal's plains and valleys. It lives in **burrows in moist
soil rich in humus**, is **nocturnal**, **fossorial** and feeds on decaying
leaves and organic matter swallowed with soil. It comes out after heavy rain
because water floods the burrows and it cannot breathe through a drowned skin.

### Morphology

- Body long, cylindrical, about **150 mm** long and 3–5 mm thick, divided into about **100–120 segments** (metameres); dark brown dorsally from the pigment **porphyrin**; a dark **mid-dorsal line** marks the dorsal blood vessel.
- The **prostomium** — a fleshy lobe overhanging the mouth — is **not a segment**; it probes the soil. The first segment, bearing the mouth, is the **peristomium**.
- Segments **14, 15 and 16** form the glandular **clitellum** (girdle). The body is thus **pre-clitellar (1–13)**, **clitellar (14–16)** and **post-clitellar (17 onwards)**.
- **Setae**: S-shaped chitinous bristles in a ring round the middle of every segment (**perichaetine**), **absent from the first segment, the last segment and the clitellum**; they grip the soil in locomotion.

| Aperture | Number | Position |
|---|---|---|
| **Mouth** | 1 | peristomium (segment 1) |
| **Anus** | 1 | last segment |
| **Spermathecal pores** | **4 pairs** | ventro-lateral, in the grooves **5/6, 6/7, 7/8, 8/9** |
| **Female genital pore** | **1** | mid-ventral, **segment 14** |
| **Male genital pores** | **1 pair** | ventro-lateral, **segment 18** |
| **Genital papillae** | **2 pairs** | **segments 17 and 19** |
| **Dorsal pores** | 1 per groove | mid-dorsal, from groove **12/13** backwards; release coelomic fluid to keep the skin moist |
| **Nephridiopores** | very many | all over the body except the first two segments |

```figure caption="Ventral view of the front end of *Pheretima posthuma*, segments 1–21. The genital apertures are the commonest source of segment-number questions."
from matplotlib.patches import Rectangle, Polygon, Circle
import numpy as np
fig, ax = plt.subplots(figsize=(5.2, 2.75))
ax.set_xlim(-0.9, 10.6); ax.set_ylim(-2.75, 2.75); ax.axis("off")
x0, w = 0.35, 0.46
def sx(n):
    return x0 + (n - 1) * w
hw = 0.72
ax.add_patch(Polygon([[x0, hw * 0.75], [x0 - 0.55, 0.25], [x0 - 0.55, -0.25],
                      [x0, -hw * 0.75]], closed=True, fc="#f0d9c4", ec="#8a5a33", lw=0.9))
for n in range(1, 22):
    h = hw * (0.75 + 0.25 * min(n, 4) / 4)
    fc = "#d98c6a" if 14 <= n <= 16 else "#f0d9c4"
    ax.add_patch(Rectangle((sx(n), -h), w, 2 * h, fc=fc, ec="#8a5a33", lw=0.7))
ax.plot([x0 - 0.38, x0 - 0.12], [0, 0], color="#5a3a1a", lw=1.6)
for g in (6, 7, 8, 9):
    for s in (1, -1):
        ax.add_patch(Circle((sx(g), s * 0.45), 0.07, fc=SERIES[0], ec="none", zorder=5))
ax.add_patch(Circle((sx(14) + w / 2, 0), 0.08, fc=SERIES[1], ec="none", zorder=5))
for s in (1, -1):
    ax.add_patch(Circle((sx(18) + w / 2, s * 0.42), 0.09, fc="#7a3e8e", ec="none", zorder=5))
    for n in (17, 19):
        ax.add_patch(Circle((sx(n) + w / 2, s * 0.25), 0.07, fc="none", ec=INK, lw=0.9, zorder=5))
fs = 6.8
def lab(t, xy, xyt, ha="center", c=INK):
    up = xyt[1] > xy[1]
    nl = t.count("\n") + 1
    yend = xyt[1] - (0.13 * nl if up else -0.13 * nl)
    ax.plot([xy[0], xyt[0]], [xy[1], yend], color=MUTED, lw=0.7, zorder=8)
    ax.text(xyt[0], xyt[1], t, fontsize=fs, color=c, ha=ha, va="center", zorder=8,
            linespacing=1.2)
lab("prostomium", (x0 - 0.45, 0.2), (-0.3, 1.75))
lab("mouth", (x0 - 0.25, 0.0), (-0.35, -1.7))
lab("spermathecal pores\n(grooves 5/6–8/9)", (sx(7.5), 0.5), (sx(7.5), 2.05), c=SERIES[0])
lab("clitellum (14–16)", (sx(15.5), 0.72), (sx(15.5), 1.95))
lab("female pore (14)", (sx(14) + w / 2, -0.05), (sx(12.5), -1.95), c=SERIES[1])
lab("male pores (18)", (sx(18) + w / 2, 0.47), (sx(20.6), 1.95), c="#7a3e8e")
lab("genital papillae\n(17, 19)", (sx(19) + w / 2, -0.32), (sx(19.6), -1.95))
for n in (1, 5, 10, 16, 18, 21):
    ax.text(sx(n) + w / 2, -0.98, str(n), ha="center", va="top", fontsize=6.6, color=MUTED)
```

### Body wall, coelom and locomotion

Body wall (outside in): **cuticle** → **epidermis** (columnar cells with gland
cells) → **circular muscles** → **longitudinal muscles** → **parietal
peritoneum**. The **coelom** is a true **schizocoel**, divided by
**intersegmental septa** and filled with milky, alkaline **coelomic fluid** with
coelomocytes. The fluid is the **hydrostatic skeleton**: circular muscles
contract to make the front segments long and thin and push them forward; setae
anchor them; longitudinal muscles then shorten the body and pull the rear up.
**Chloragogen cells** on the gut and blood vessels store glycogen and fat and
remove nitrogenous waste (compared with the vertebrate liver).

### Digestive system

| Region | Segments | Notes |
|---|---|---|
| Mouth, buccal cavity | **1–3** | eversible |
| **Pharynx** | **4** | muscular, sucking; **pharyngeal (salivary) glands** secrete mucus and a protease |
| Oesophagus | **5–7** | narrow tube |
| **Gizzard** | **8–9** | thick, muscular, cuticle-lined; **grinds** soil and leaves |
| **Stomach** | **9–14** | glandular; **calciferous glands** secrete CaCO₃ that **neutralises the humic acid** of the humus |
| **Intestine** | **15 to the last** | digestion and absorption; a pair of short conical **intestinal caeca** at **segment 26**; the **typhlosole**, a mid-dorsal fold, runs from segment **26** to all but the last 23–25 segments and **increases the absorptive surface** |
| Anus | last | worm castings leave here |

Digestion is **extracellular**; the gut makes protease, amylase and lipase,
and cellulose is broken down largely with the help of gut microbes.

### Blood vascular system

- **Closed** system; the blood is red because **haemoglobin is dissolved in the plasma**; the corpuscles are colourless, nucleated amoeboid cells.
- **Dorsal vessel**: above the gut, contractile, with valves; blood flows **forwards** — the chief **collecting** vessel.
- **Ventral vessel**: below the gut; blood flows **backwards** — the chief **distributing** vessel.
- **Four pairs of hearts**: **lateral hearts** in segments **7 and 9** and **latero-oesophageal hearts** in segments **12 and 13**, with valves, pumping from the dorsal to the ventral vessel.
- **Blood glands** in segments **4, 5 and 6** make blood corpuscles and haemoglobin.

### Respiration

There are **no respiratory organs**. Respiration is **cutaneous**: O₂ dissolves
in the moist film of mucus and coelomic fluid on the skin and diffuses into a
dense capillary network beneath the cuticle. A dry skin means death by
suffocation.

### Excretion

The excretory organs are coiled tubules, the **nephridia** — three kinds in
*Pheretima*.

| Nephridia | Position | Opening | Nephrostome |
|---|---|---|---|
| **Septal** | both faces of each septum from **segment 15** to the last | into the **intestine** (enteronephric) | present |
| **Integumentary** | inner surface of the body wall from **segment 3** to the last; very many on the clitellum | **outside** by nephridiopores (exonephric) | absent |
| **Pharyngeal** | three paired tufts in segments **4, 5 and 6** | into the **buccal cavity and pharynx** (enteronephric) | absent |

The worm excretes **ammonia** in wet soil and more **urea** when dry
(ammonotelic → ureotelic). Enteronephric nephridia send the urine into the gut,
where water is reabsorbed — a water-saving adaptation.

### Nervous system and sense organs

A pair of **cerebral (supra-pharyngeal) ganglia** — the "brain" — lies above
the pharynx in **segment 3**; **circum-pharyngeal connectives** join them to the
**sub-pharyngeal ganglia** in segment **4**, forming a **nerve ring**; from
these the **ventral nerve cord** — double but fused, **solid**, with a
**ganglion in every segment** — runs to the hind end. There are **no eyes**:
**photoreceptor cells** (mostly on the prostomium and dorsal surface) sense
light, and epidermal receptors sense touch and chemicals; chemoreceptors in the
buccal cavity taste food.

### Reproduction and development

The earthworm is **hermaphrodite (monoecious)** but **protandrous** — the testes
mature before the ovaries — so **cross-fertilisation** is the rule.

| Male organs | Segments | Female organs | Segments |
|---|---|---|---|
| **2 pairs of testes** in testis sacs | **10 and 11** | **1 pair of ovaries** (on septum 12/13) | **13** |
| 2 pairs of seminal vesicles | 11 and 12 | ovarian funnels and oviducts | 13–14 |
| vasa deferentia | 10 to 18 | **single female genital pore** | **14** |
| 1 pair of large **prostate glands** | about 16/17 to 20/21 | **4 pairs of spermathecae** | **6, 7, 8, 9** |
| male genital pores | **18** | | |
| 2 pairs of accessory glands (open on the genital papillae) | **17 and 19** | | |

**Copulation** (on damp nights): two worms join ventral surfaces head-to-tail
and exchange sperm, which are stored in each other's **spermathecae**. Later the
**clitellum secretes a cocoon**; as the worm wriggles backwards out of it, the
cocoon collects **ova at segment 14** and **sperm from the spermathecae at
segments 6–9**. **Fertilisation therefore takes place in the cocoon, outside the
body (external)**. The cocoon is left in the soil; after about three weeks it
releases 2–20 young worms (on average about four). **Development is direct — no larva.** Earthworms
also **regenerate** lost parts.

::: caution Two marks that are regularly lost
(1) Hermaphrodite does **not** mean self-fertilising — *Pheretima* is
protandrous and **cross-fertilising**. (2) Sperm pass from worm to worm, but
fertilisation is **external**, inside the cocoon. And remember the single
female pore (14) lies **in front of** the paired male pores (18).
:::

### Economic importance

- **Farmer's friend**: burrows **aerate and drain** the soil and let roots penetrate; worms bring subsoil up and bury organic matter (Darwin, *The Formation of Vegetable Mould through the Action of Worms*, 1881).
- **Castings** are rich in nitrogen, phosphorus, potassium, calcium and humus.
- **Vermicomposting** (vermiculture) turns farm and kitchen waste into manure; *Eisenia fetida* (red wiggler) and *Perionyx excavatus* are the usual species.
- Worms are fish bait, a protein-rich feed for poultry and fish, and are used in traditional medicine.
- Harmful: casts spoil lawns and seedbeds; earthworms are intermediate hosts of the poultry gapeworm *Syngamus* and the lungworm of pigs; they host the gregarine *Monocystis* in their seminal vesicles.

::: memory Earthworm segment numbers
**"3-4 brain, 4 pharynx, 5-7 gullet, 8-9 gizzard, 9-14 stomach"**; then the
reproductive run **"6-9 spermathecae, 10-11 testes, 13 ovaries, 14 female, 17
and 19 papillae, 18 male"**; hearts **7, 9, 12, 13**; caeca and typhlosole from
**26**.
:::

## 4.3 Frog (Rana): morphology, body systems and physiology

### Position, habit and habitat

***Rana tigrina*** (now *Hoplobatrachus tigerinus*, the Indian bullfrog;
Chordata → Vertebrata → **Amphibia** → order **Anura**) lives in and near ponds,
ditches and paddy fields of the Terai and valleys. It is **amphibious**,
**carnivorous** (insects, worms, snails) and **poikilothermic** (cold-blooded):
it escapes winter cold by **hibernation** (winter sleep) and summer heat and
drought by **aestivation** (summer sleep), buried in mud and breathing through
its skin. It changes skin colour with its surroundings by means of
**chromatophores** (camouflage).

### Morphology

- Body of **head and trunk**; **no neck and no tail** in the adult.
- Skin **smooth, moist, slimy, scaleless**, loosely attached, rich in mucous glands and capillaries. The frog **never drinks water** — it absorbs water through the skin.
- Head: wide mouth, a pair of **external nares**, bulging **eyes** with a fixed upper lid, a movable lower lid and a transparent **nictitating membrane** that protects the eye under water; behind each eye a circular **tympanum** (ear drum) — there is **no external ear**.
- **Forelimbs** short, with **4 digits**; **hindlimbs** long and muscular, with **5 webbed toes** for leaping and swimming.
- A single **cloacal aperture** at the hind end passes faeces, urine and gametes.
- **Sexual dimorphism**: the male has a pair of **vocal sacs** (croaking) and a **nuptial (copulatory) pad** on the **first digit of each forelimb**; the female has neither.

### Skeleton (the facts that are asked)

| Part | Feature |
|---|---|
| Skull | **dicondylic** (two occipital condyles); teeth on the upper jaw (**maxillary**) and palate (**vomerine**); lower jaw toothless |
| Vertebral column | only **9 vertebrae + a rod-like urostyle**; the first (atlas) has no transverse processes |
| Ribs | **absent** |
| Limb bones | **radio-ulna** and **tibio-fibula** fused; long ankle (tarsal) bones for leaping |
| Calcified cartilage | suprascapula |

### Digestive system

**Mouth** → **buccal cavity** with **maxillary** and **vomerine teeth** (they
grip prey, they do not chew; teeth homodont, acrodont and replaced throughout
life) and a sticky **bilobed tongue attached in front and free behind**, flicked
out to catch insects → **pharynx** → short **oesophagus** → **stomach**
(cardiac and pyloric parts; HCl and pepsin) → **duodenum** → coiled **ileum**
with villi (digestion completed, absorption) → **rectum** → **cloaca**. The
**liver** (three lobes) secretes bile, stored in the **gall bladder**; the
**pancreas** lies between stomach and duodenum; the bile duct and pancreatic
duct join to form the **common bile duct**, opening into the **duodenum**. The
adult's gut is **short** (carnivore); the herbivorous tadpole's is long and coiled.

### Respiration

The frog breathes in three ways:

| Mode | Organ | When |
|---|---|---|
| **Cutaneous** | moist, thin, vascular **skin** | always — in water, on land and the **only** route during **hibernation and aestivation**; gets rid of most of the CO₂ |
| **Buccopharyngeal** | moist lining of the buccal cavity | at rest on land, mouth shut (the throat flutters) |
| **Pulmonary** | a pair of thin, elastic, sac-like **lungs** with internal septa forming alveoli | when active on land |

**Pathway of air**: external nares → nasal chambers → internal nares → buccal
cavity → **glottis** → laryngo-tracheal chamber → lungs. With **no diaphragm and
no ribs**, the frog fills its lungs by a **buccal force pump** (positive
pressure): with the glottis shut it lowers the buccal floor and draws air in
through the nostrils; it then closes the nostrils, opens the glottis and
**raises the buccal floor**, forcing the air into the lungs. Expiration is by
elastic recoil and pressure of the body wall. The tadpole breathes by **gills**.

### Blood vascular system

- **Closed**, with a **three-chambered heart** — **two atria (auricles) and one ventricle** — in a pericardium, plus two accessory chambers.
- **Sinus venosus** (dorsal, thin-walled) receives deoxygenated blood from **two precavals and one postcaval** and opens into the **right atrium**; it is the **pacemaker** — the heartbeat starts here.
- **Pulmonary veins** bring oxygenated blood from the lungs into the **left atrium**.
- Both atria empty into the single **ventricle**, whose spongy wall (trabeculae) limits mixing.
- **Truncus (conus) arteriosus** leaves the ventricle on the ventral side; its **spiral valve** directs the most deoxygenated blood into the **pulmocutaneous arch** (lungs and skin), mixed blood into the **systemic arch** (body) and the best-oxygenated blood into the **carotid arch** (head).
- Circulation is **double but incomplete** (some mixing). **Hepatic portal** and **renal portal** systems are present; the lymphatic system has **lymph hearts**.
- Blood: plasma with **nucleated, oval, biconvex RBCs**, WBCs and spindle-shaped thrombocytes.

```figure caption="Blood flow through the heart of the frog. Two atria share one ventricle; the spiral valve in the truncus arteriosus sorts the blood into three pairs of arches, so the circulation is double but incomplete."
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.2, 2.9))
ax.set_xlim(0, 10.4); ax.set_ylim(0, 5.8); ax.axis("off")
BLUE, RED, MIX = "#dbe7f3", "#f6d9d5", "#eadcf0"
def box(x, y, w, h, t, fc, ec=MUTED, fs=6.8, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc=fc, ec=ec, lw=0.9))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, color=INK,
            linespacing=1.25, fontweight="bold" if bold else "normal")
def arr(p, q):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=8, lw=1.0, color=INK))
box(0.1, 4.45, 2.6, 0.95, "body: 2 precavals\n+ 1 postcaval", BLUE)
box(0.1, 2.85, 2.6, 0.95, "sinus venosus\n(pacemaker)", BLUE, bold=True)
box(0.1, 1.25, 2.6, 0.95, "right atrium", BLUE, bold=True)
box(3.25, 4.45, 2.4, 0.95, "lungs → pulmonary\nveins", RED)
box(3.25, 2.85, 2.4, 0.95, "left atrium", RED, bold=True)
box(3.25, 0.15, 2.4, 0.95, "ventricle (single)", MIX, bold=True)
box(6.2, 0.15, 1.75, 2.1, "truncus\narteriosus\n(spiral\nvalve)", MIX, bold=True)
box(8.35, 4.25, 1.95, 1.15, "carotid arch\n→ head\n(best O₂)", RED)
box(8.35, 2.6, 1.95, 1.15, "systemic arch\n→ body\n(mixed)", MIX)
box(8.35, 0.95, 1.95, 1.15, "pulmocutaneous\n→ lungs, skin\n(least O₂)", BLUE)
arr((1.4, 4.45), (1.4, 3.8))
arr((1.4, 2.85), (1.4, 2.2))
arr((1.4, 1.25), (3.25, 0.62))
arr((4.45, 4.45), (4.45, 3.8))
arr((4.45, 2.85), (4.45, 1.1))
arr((5.65, 0.62), (6.2, 0.62))
for y in (4.82, 3.17, 1.52):
    arr((7.95, 1.2 + (y - 1.52) * 0.25), (8.35, y))
```

### Excretion and osmoregulation

A pair of dark-red **mesonephric kidneys** lies against the dorsal body wall,
each with a yellow **adrenal gland** on its ventral face. **Ureters** open into
the **cloaca**; in the **male** the ureter also carries sperm and is called the
**urinogenital duct**, while in the **female** the ureter and oviduct open
separately into the cloaca. The thin-walled, bilobed **urinary bladder** opens
**ventrally into the cloaca**, not into the ureters, and lets water be reabsorbed
on land. The adult is **ureotelic** (urea); the aquatic tadpole is
**ammonotelic** (ammonia).

### Nervous system, sense organs and endocrine glands

**CNS**: brain in the cranium and spinal cord in the neural canal, wrapped in
meninges. **PNS**: **10 pairs of cranial nerves** and **10 pairs of spinal
nerves**; an autonomic system as well.

| Brain region | Parts | Job |
|---|---|---|
| **Forebrain** | a pair of **olfactory lobes**, a pair of **cerebral hemispheres**, the **diencephalon** with the pineal body above and the optic chiasma, infundibulum and **pituitary** below | smell, voluntary activity, hormone control |
| **Midbrain** | a pair of large **optic lobes** | vision |
| **Hindbrain** | a small **cerebellum** and the **medulla oblongata** | balance; breathing, heartbeat and other reflex centres |

**Sense organs**: eyes (with nictitating membrane), ears (tympanum, a middle ear
with one ossicle, the **columella**, and an internal ear for hearing and
balance), nasal epithelium (smell), taste buds and skin papillae (touch). The
tadpole has a **lateral line system**, lost at metamorphosis.

**Endocrine glands**: pituitary, **thyroid**, parathyroid, thymus, pineal,
pancreatic islets, adrenals and gonads. **Thyroxine** from the thyroid controls
**metamorphosis**.

### Reproduction and development

The frog is **dioecious**; **fertilisation is external**; **development is
indirect** through a tadpole larva.

| Male | Female |
|---|---|
| a pair of yellowish oval **testes**, attached to the kidneys and body wall by the **mesorchium** | a pair of lobed **ovaries** near the kidneys, attached by the **mesovarium**, **not connected to the kidneys** |
| **10–12 vasa efferentia** carry sperm into the kidney → **Bidder's canal** → **urinogenital duct** (ureter) → a dilated **seminal vesicle** → cloaca | ova are shed into the coelom and enter the funnel-shaped **ostium** of the long coiled **oviduct**; its hind end, the **ovisac**, opens into the cloaca |
| finger-like **fat bodies** store food for the breeding season | lays **2500–3000 eggs** at a time in jelly-coated masses |

**Breeding** follows the first monsoon rains. In **amplexus** the male clasps the
female with the nuptial pads; she sheds eggs into the water and he sheds sperm
over them at once. **Amplexus is not copulation — fertilisation is external.**
The egg hatches into a **tadpole**: aquatic, herbivorous, with horny jaws, a
long coiled gut, a tail with fins, external then internal **gills**, a
**two-chambered heart**, a lateral line, no limbs, and ammonotelic.

**Metamorphosis**, controlled by **thyroxine** (which needs iodine), turns the
tadpole into a frog. *Progressive* changes: **hindlimbs appear first, then
forelimbs**; lungs develop; heart becomes three-chambered; eyelids and tympanum
form; the gut shortens; excretion becomes ureotelic. *Retrogressive* changes:
the **tail is resorbed** (by lysosomal enzymes), gills, horny jaws and lateral
line disappear. Tadpoles given thyroxine metamorphose early into tiny frogs;
tadpoles deprived of thyroid hormone or iodine stay as giant tadpoles.

::: caution Frog traps
- The heartbeat starts in the **sinus venosus**, not in the SA node (the frog has none).
- The frog's RBCs are **nucleated** and oval, unlike the mammal's.
- The male's ureter carries urine **and** sperm; the female's oviduct is separate from the ureter.
- The urinary bladder opens into the **cloaca**, not into the ureters.
- Only the **upper jaw** carries teeth; the **lower jaw is toothless**.
:::

::: tip Three columns for every frog question
Most frog questions are answered by placing the fact in one of three columns:
**tadpole** (gills, two-chambered heart, ammonia, herbivore, lateral line) →
**metamorphosis** (thyroxine) → **adult** (lungs and skin, three-chambered heart,
urea, carnivore).
:::

::: example Timing erythrocytic schizogony and fever paroxysms in malaria
**Problem.** A patient presents with classic paroxysms of chill, high fever, and sweating recurring every 48 hours, and peripheral blood smear shows enlarged, stippled RBCs with Schüffner's dots. Identify the *Plasmodium* species and explain why the fever recurs every 48 hours.

**Solution.** A 48-hour benign tertian cycle with enlarged host RBCs bearing **Schüffner's dots** identifies ***Plasmodium vivax***. Fever spikes when **erythrocytic schizonts rupture synchronously** every 48 hours, releasing merozoites and the pyrogenic toxin **haemozoin** into the plasma.
:::

::: example Segmental landmarks of Pheretima posthuma
**Problem.** Give the exact segment numbers in *Pheretima posthuma* for (a) the gizzard, (b) the clitellum, (c) the single female genital pore, (d) the paired male genital pores, and (e) the four pairs of spermathecal apertures.

**Solution.** (a) Gizzard: **8 (or 8–9)**; (b) clitellum: **14, 15, and 16**; (c) female pore: mid-ventral on **14**; (d) male pores: ventro-lateral on **18**; (e) spermathecal pores: intersegmental grooves **5/6, 6/7, 7/8, and 8/9**.
:::

## Formula and fact sheet

**Plasmodium**

| Item | Fact |
|---|---|
| Class | Sporozoa (Apicomplexa) |
| Definitive / intermediate host | female *Anopheles* / man |
| Infective stage to man / to mosquito | sporozoite / gametocytes |
| Human sites | liver cells, RBCs |
| Mosquito sites | stomach wall (oocyst), salivary glands (sporozoites) |
| Golgi cycle | erythrocytic schizogony |
| Ross cycle | sporogony in the mosquito |
| Only diploid stage | zygote (and ookinete) |
| Malarial pigment / toxin | haemozoin |
| Relapse | hypnozoites of *P. vivax* and *P. ovale* |
| Microgametes per microgametocyte | 4–8 (exflagellation) |
| *P. vivax* / *P. falciparum* / *P. malariae* / *P. ovale* | benign tertian 48 h / malignant tertian 36–48 h / quartan 72 h / ovale tertian 48 h |
| Cerebral malaria, blackwater fever, crescent gametocytes | *P. falciparum* |
| Schüffner's dots, enlarged RBCs | *P. vivax* |
| Laveran / Ross / Golgi / Grassi | parasite in blood 1880 / oocyst in *Anopheles* 1897 / RBC cycle / cycle in *Anopheles* |
| Drugs | quinine, chloroquine, primaquine (hypnozoites), artemisinin (ACT) |
| Larvivorous fish | *Gambusia* |

**Earthworm (*Pheretima posthuma*)**

| Item | Segment(s) / fact |
|---|---|
| Length, segments | about 150 mm; 100–120 segments |
| Prostomium / peristomium | not a segment / segment 1 (mouth) |
| Clitellum | 14–16 |
| Setae absent from | segment 1, last segment, clitellum |
| Spermathecal pores / spermathecae | grooves 5/6–8/9 / segments 6–9 |
| Female pore / ovaries | 14 / 13 |
| Male pores / testes / seminal vesicles | 18 / 10–11 / 11–12 |
| Genital papillae | 17 and 19 |
| Dorsal pores begin | groove 12/13 |
| Pharynx / oesophagus / gizzard / stomach | 4 / 5–7 / 8–9 / 9–14 |
| Intestine / caeca / typhlosole begins | 15 onwards / 26 / 26 |
| Hearts | 4 pairs: 7, 9 (lateral), 12, 13 (latero-oesophageal) |
| Blood glands | 4, 5, 6 |
| Pharyngeal / septal / integumentary nephridia | 4–6 / 15 onwards / 3 onwards |
| Brain (cerebral ganglia) / sub-pharyngeal ganglia | 3 / 4 |
| Respiratory pigment | haemoglobin dissolved in plasma |
| Respiration | cutaneous |
| Excretion | ammonotelic and ureotelic |
| Calciferous glands | neutralise humic acid |
| Sex | protandrous hermaphrodite, cross-fertilisation, external fertilisation in the cocoon, direct development |

**Frog (*Rana tigrina*)**

| Item | Fact |
|---|---|
| Digits | forelimb 4, hindlimb 5 (webbed) |
| Male-only features | vocal sacs, nuptial pad on first digit of forelimb |
| Teeth | maxillary + vomerine; lower jaw toothless |
| Vertebrae | 9 + urostyle; no ribs |
| Breathing | skin, buccopharynx, lungs; buccal force pump |
| Heart | 2 atria + 1 ventricle; sinus venosus (pacemaker); truncus arteriosus with spiral valve |
| Arches | carotid, systemic, pulmocutaneous |
| Portal systems | hepatic portal, renal portal |
| RBCs | nucleated, oval, biconvex |
| Kidneys | mesonephric; adult ureotelic, tadpole ammonotelic |
| Male duct | ureter = urinogenital duct; Bidder's canal; 10–12 vasa efferentia |
| Nerves | 10 pairs cranial, 10 pairs spinal |
| Ear ossicle | columella |
| Eggs | 2500–3000 at a time |
| Metamorphosis | thyroxine; hindlimbs before forelimbs; tail resorbed |

## Chapter summary

- *Plasmodium* (Sporozoa) is a digenetic intracellular parasite: **asexual schizogony in man** (intermediate host) — liver cells, then the 48-hour **Golgi cycle** in RBCs — and **sexual phase in the female *Anopheles*** (definitive host) — gametes, zygote, ookinete, oocyst, sporozoites in the salivary glands.
- The **sporozoite** infects man and the **gametocyte** infects the mosquito; the zygote is the only diploid stage; the fever follows the synchronous bursting of RBCs and the release of **haemozoin**.
- ***P. vivax*** (benign tertian, relapses from hypnozoites, commonest in Nepal), ***P. falciparum*** (malignant tertian, cerebral malaria), ***P. malariae*** (quartan, 72 h) and ***P. ovale*** (ovale tertian).
- ***Pheretima posthuma***: about 100–120 segments; prostomium; clitellum 14–16; perichaetine setae; female pore 14, male pores 18, papillae 17 and 19, spermathecal pores 5/6–8/9.
- Earthworm gut: pharynx 4, gizzard 8–9, stomach 9–14 with **calciferous glands**, caeca and **typhlosole** from 26; **closed circulation** with Hb in plasma and four pairs of hearts (7, 9, 12, 13); **cutaneous respiration**; **septal, integumentary and pharyngeal nephridia**.
- The earthworm is a **protandrous hermaphrodite**: testes 10–11, ovaries 13, spermathecae 6–9; cross-fertilisation, fertilisation in the cocoon, direct development; it is the **farmer's friend** and the basis of vermicomposting.
- The frog (*Rana tigrina*) breathes by **skin, buccopharynx and lungs** (buccal force pump); its **three-chambered heart** with **sinus venosus** and **spiral valve** gives a double but incomplete circulation; RBCs are nucleated.
- The frog is **ureotelic** with mesonephric kidneys; the male's ureter is a **urinogenital duct**; it has **10 pairs of cranial nerves**, 9 vertebrae and a urostyle; fertilisation is **external** after amplexus, and **thyroxine** drives metamorphosis of the tadpole.

## Practice questions

**Set A — Recall (30 questions)**

1. The definitive host of *Plasmodium* is
   (a) man (b) the male *Anopheles* (c) the female *Anopheles* (d) the female *Culex*
2. The stage of *Plasmodium* that infects man is the
   (a) sporozoite (b) merozoite (c) gametocyte (d) ookinete
3. The erythrocytic schizogony of *Plasmodium* in man is also called the
   (a) Ross cycle (b) Krebs cycle (c) Cori cycle (d) Golgi cycle
4. The toxic pigment released when infected red blood cells burst is
   (a) haemocyanin (b) haemozoin (c) bilirubin (d) melanin
5. Benign tertian malaria is caused by
   (a) *P. falciparum* (b) *P. malariae* (c) *P. vivax* (d) *P. knowlesi*
6. Malarial fever recurring every 72 hours is caused by
   (a) *P. malariae* (b) *P. vivax* (c) *P. ovale* (d) *P. falciparum*
7. Cerebral malaria and blackwater fever are complications of infection with
   (a) *P. vivax* (b) *P. ovale* (c) *P. malariae* (d) *P. falciparum*
8. The oocysts of *Plasmodium* are formed on the
   (a) salivary glands of the mosquito (b) stomach wall of the mosquito (c) liver cells of man (d) red blood cells of man
9. The malarial parasite was first seen in human blood in 1880 by
   (a) Ronald Ross (b) Camillo Golgi (c) Charles Laveran (d) Battista Grassi
10. In the life cycle of *Plasmodium* the diploid stage is the
   (a) zygote (b) sporozoite (c) merozoite (d) gametocyte
11. In *Pheretima posthuma* the clitellum occupies segments
   (a) 10–12 (b) 12–14 (c) 15–17 (d) 14–16
12. The female genital pore of *Pheretima* lies on segment
   (a) 13 (b) 14 (c) 18 (d) 16
13. The male genital pores of *Pheretima* lie on segment
   (a) 18 (b) 14 (c) 17 (d) 19
14. The spermathecal pores of *Pheretima* are
   (a) 2 pairs, on segments 10 and 11 (b) 1 pair, on segment 18 (c) 4 pairs, in grooves 5/6 to 8/9 (d) 2 pairs, on segments 17 and 19
15. The gizzard of the earthworm lies in segments
   (a) 4 (b) 5–7 (c) 9–14 (d) 8–9
16. The calciferous glands of the earthworm neutralise
   (a) hydrochloric acid (b) humic acid (c) uric acid (d) lactic acid
17. The typhlosole of the earthworm intestine
   (a) increases the absorptive surface (b) grinds food (c) secretes calcium carbonate (d) stores sperm
18. The respiratory pigment of the earthworm is
   (a) haemocyanin in the plasma (b) haemoglobin in red cells (c) haemoglobin dissolved in the plasma (d) myoglobin in the muscles
19. The pharyngeal nephridia of the earthworm lie in segments
   (a) 15 to the last (b) 3 to the last (c) 1 to 3 (d) 4, 5 and 6
20. The testes of *Pheretima* are
   (a) 1 pair, in segment 13 (b) 2 pairs, in segments 10 and 11 (c) 2 pairs, in segments 11 and 12 (d) 4 pairs, in segments 6–9
21. The heartbeat of the frog is initiated in the
   (a) sinus venosus (b) right atrium (c) ventricle (d) truncus arteriosus
22. The spiral valve of the frog is found in the
   (a) sinus venosus (b) ventricle (c) truncus arteriosus (d) left atrium
23. The number of cranial nerves in the frog is
   (a) 12 pairs (b) 8 pairs (c) 11 pairs (d) 10 pairs
24. The chief nitrogenous waste of the adult frog is
   (a) ammonia (b) urea (c) uric acid (d) creatinine
25. In the male frog the ureter is also called the
   (a) urinogenital duct (b) Bidder's canal (c) vas efferens (d) oviduct
26. The nuptial (copulatory) pad of the frog is found on the
   (a) hindlimb of the female (b) first toe of the male's hindlimb (c) first digit of the male's forelimb (d) throat of the male
27. The vertebral column of the frog consists of
   (a) 7 vertebrae and a sacrum (b) 12 vertebrae and a coccyx (c) 10 vertebrae and no urostyle (d) 9 vertebrae and a urostyle
28. Metamorphosis of the frog tadpole is controlled by
   (a) insulin (b) thyroxine (c) adrenaline (d) prolactin
29. In the frog, teeth are present on
   (a) the upper jaw and vomers only (b) both jaws (c) the lower jaw only (d) the tongue
30. The midbrain of the frog bears a pair of
   (a) olfactory lobes (b) cerebellar lobes (c) optic lobes (d) cerebral hemispheres

::: note Answers and explanations — Set A
**1.** (c) — fertilisation (the sexual phase) occurs in the female *Anopheles*, so she is the definitive host; man is intermediate.
**2.** (a) — sporozoites from the mosquito's salivary glands are injected with saliva. Gametocytes infect the mosquito, not man.
**3.** (d) — Golgi described the cycle in RBCs; the Ross cycle is the sporogony in the mosquito.
**4.** (b) — haemozoin, the residue of digested haemoglobin; haemocyanin is the copper pigment of molluscs.
**5.** (c) — *P. vivax*, 48-hour cycle, rarely fatal; *P. falciparum* causes the malignant form.
**6.** (a) — the 72-hour erythrocytic cycle of *P. malariae* gives quartan fever (every fourth day).
**7.** (d) — sticky falciparum-infected RBCs block brain capillaries, and massive haemolysis darkens the urine.
**8.** (b) — the ookinete crosses the stomach wall and encysts on its outer surface; sporozoites later move to the salivary glands.
**9.** (c) — Laveran (1880); Ross (1897) found the oocysts in the mosquito.
**10.** (a) — the zygote (with the ookinete it becomes) is diploid; meiosis in the oocyst makes every later stage haploid.
**11.** (d) — segments 14, 15 and 16 form the glandular clitellum, which has no setae.
**12.** (b) — a single mid-ventral female pore on segment 14, in front of the male pores.
**13.** (a) — one pair of male pores on segment 18, with genital papillae on 17 and 19.
**14.** (c) — four pairs, ventro-lateral, in the grooves between segments 5/6, 6/7, 7/8 and 8/9.
**15.** (d) — the muscular grinding gizzard is in segments 8–9; the stomach follows in 9–14.
**16.** (b) — the CaCO₃ they secrete neutralises the humic acid of decaying leaves in the soil.
**17.** (a) — the typhlosole is a mid-dorsal infolding of the intestine that adds absorptive surface.
**18.** (c) — earthworm haemoglobin is dissolved in the plasma; its corpuscles are colourless.
**19.** (d) — three paired tufts in segments 4, 5 and 6, opening into the buccal cavity and pharynx.
**20.** (b) — two pairs of testes in segments 10 and 11; the seminal vesicles are in 11 and 12.
**21.** (a) — the sinus venosus acts as the pacemaker in the frog; mammals have an SA node instead.
**22.** (c) — the spiral valve of the truncus arteriosus sorts blood into the three arches.
**23.** (d) — the frog has 10 pairs of cranial nerves; man has 12.
**24.** (b) — the adult frog is ureotelic; its aquatic tadpole is ammonotelic.
**25.** (a) — in the male the ureter carries both urine and sperm; Bidder's canal lies inside the kidney.
**26.** (c) — the male grips the female in amplexus with nuptial pads on the first digit of each forelimb.
**27.** (d) — only nine vertebrae and a rod-like urostyle; the frog has no ribs.
**28.** (b) — thyroxine (thyroid hormone) triggers metamorphosis.
**29.** (a) — maxillary teeth on the upper jaw and vomerine teeth on the palate; the lower jaw is toothless.
**30.** (c) — the optic lobes are the midbrain's visual centres; olfactory lobes belong to the forebrain.
:::

**Set B — Understanding (21 questions)**

1. Only the female *Anopheles* transmits malaria because
   (a) males lack salivary glands (b) only females feed on blood (c) males are immune to *Plasmodium* (d) males live only in water
2. A patient treated for vivax malaria has a fresh attack eight months later without a new bite. The attack comes from
   (a) gametocytes in the blood (b) sporozoites in the spleen (c) merozoites in bone marrow (d) dormant hypnozoites in liver cells
3. The 48-hour periodicity of fever in vivax malaria reflects the duration of
   (a) erythrocytic schizogony (b) sporogony in the mosquito (c) the life of an RBC (d) the journey of sporozoites to the liver
4. Gametocytes of *Plasmodium* do not develop further in the human body because
   (a) they are diploid (b) they lack nuclei (c) they need the conditions of the mosquito's stomach (d) human antibodies kill them at once
5. Which stage of *Plasmodium* is NEVER seen in a human blood smear?
   (a) ring-shaped trophozoite (b) oocyst (c) gametocyte (d) schizont
6. In vivax malaria primaquine is given after chloroquine in order to
   (a) kill sporozoites in the mosquito (b) reduce the fever quickly (c) prevent mosquito bites (d) destroy hypnozoites and gametocytes
7. People with sickle-cell trait resist falciparum malaria because
   (a) they have no red cells (b) their RBCs lack haemoglobin (c) infected RBCs sickle and are removed early (d) they have antibodies against *Anopheles*
8. The earthworm is hermaphrodite, yet cross-fertilisation occurs because
   (a) its testes mature before its ovaries (b) it has no ovaries (c) its sperm cannot swim (d) male and female pores lie on one segment
9. In the earthworm, fertilisation takes place in the
   (a) spermathecae (b) cocoon (c) coelom (d) seminal vesicles
10. Earthworms come out of the soil after heavy rain mainly
   (a) to feed (b) to mate (c) to lay cocoons (d) to avoid suffocating in flooded burrows
11. Blood in the dorsal vessel of the earthworm flows
   (a) backwards, as the distributing vessel (b) forwards, as the distributing vessel (c) forwards, as the collecting vessel (d) backwards, as the collecting vessel
12. The septal nephridia of *Pheretima* open into the intestine. This is an adaptation for
   (a) conserving water (b) faster locomotion (c) digesting cellulose (d) storing sperm
13. The earthworm is called the "farmer's friend" because it
   (a) eats insect pests (b) aerates the soil and enriches it with its castings (c) pollinates crops (d) fixes atmospheric nitrogen
14. Locomotion in the earthworm depends on
   (a) parapodia and cilia (b) a bony endoskeleton (c) jointed legs (d) setae, two muscle layers and the coelomic fluid
15. The frog does not need to drink water because it
   (a) makes water from fat (b) never loses water (c) absorbs water through its skin (d) gets all its water from food
16. During hibernation the frog respires
   (a) through its skin (b) through its lungs (c) through gills (d) through the buccopharyngeal lining only
17. Air is forced into the lungs of a frog by
   (a) movements of the diaphragm (b) raising the floor of the buccal cavity (c) movements of the ribs (d) contraction of the lungs
18. Although the frog has a single ventricle, mixing of blood is reduced by
   (a) the sinus venosus (b) the renal portal system (c) the lymph hearts (d) the spiral valve and folds of the ventricle wall
19. Bidder's canal is found in the
   (a) ovary of the female (b) liver (c) kidney of the male (d) brain
20. A tadpole excretes ammonia but an adult frog excretes urea. The change is linked to
   (a) the change from aquatic to land life (b) loss of the tail (c) the growth of teeth (d) the appearance of vocal sacs
21. The nictitating membrane of the frog
   (a) helps in hearing (b) protects the eye under water (c) secretes tears (d) produces sound

::: note Answers and explanations — Set B
**1.** (b) — the female needs a blood meal to mature her eggs; the male feeds on nectar and plant juices.
**2.** (d) — hypnozoites of *P. vivax* lie dormant in hepatocytes and later restart the cycle (relapse).
**3.** (a) — merozoites are released in a synchronised batch at the end of each 48-hour erythrocytic cycle.
**4.** (c) — gametes form only after the drop in temperature and the chemical cues of the mosquito's stomach.
**5.** (b) — the oocyst forms only on the mosquito's stomach wall; rings, schizonts and gametocytes are all seen in human blood.
**6.** (d) — primaquine kills the liver hypnozoites (preventing relapse) and the gametocytes (stopping transmission).
**7.** (c) — the parasite lowers the oxygen in its RBC, which then sickles and is removed by the spleen before the cycle finishes.
**8.** (a) — protandry: sperm ripen first, so a worm cannot fertilise its own eggs.
**9.** (b) — the cocoon picks up ova at segment 14 and sperm at segments 6–9; fertilisation is external, inside it.
**10.** (d) — water fills the burrows and its cutaneous respiration fails; the worm surfaces to breathe.
**11.** (c) — the dorsal vessel collects blood from the segments and pumps it forwards to the hearts.
**12.** (a) — urine entering the gut gives the intestine a chance to reabsorb its water.
**13.** (b) — burrows aerate and drain the soil; castings are rich in N, P, K and humus. Earthworms do not fix nitrogen (d).
**14.** (d) — circular and longitudinal muscles act on the incompressible coelomic fluid (hydrostatic skeleton) while setae anchor the body.
**15.** (c) — the permeable skin takes in water directly.
**16.** (a) — buried in mud and inactive, the frog relies on cutaneous respiration alone.
**17.** (b) — the buccal force pump: nostrils closed, glottis open, buccal floor raised. The frog has no diaphragm and no ribs.
**18.** (d) — the spiral valve and ventricular trabeculae keep the streams partly separate; the circulation is still incomplete.
**19.** (c) — vasa efferentia enter the kidney and join Bidder's canal on the way to the urinogenital duct.
**20.** (a) — ammonia needs much water to flush away; urea is less toxic and suits life on land.
**21.** (b) — the transparent third eyelid covers the eye when the frog is under water.
:::

**Set C — Application (12 questions)**

1. A patient has fever every 48 hours; the smear shows enlarged RBCs with Schüffner's dots, and the disease relapses months later. The parasite is
   (a) *P. falciparum* (b) *P. vivax* (c) *P. malariae* (d) *P. knowlesi*
2. A vivax malaria patient's fever begins on Monday at 10 a.m. The next paroxysm is expected on
   (a) Tuesday at 10 a.m. (b) Thursday at 10 a.m. (c) Friday at 10 a.m. (d) Wednesday at 10 a.m.
3. A smear shows only ring forms and crescent-shaped gametocytes, and the patient becomes unconscious. The parasite is
   (a) *P. falciparum* (b) *P. vivax* (c) *P. ovale* (d) *P. malariae*
4. Each infected RBC releases 16 merozoites every 48 hours and each merozoite infects a new RBC. Starting from one infected RBC, how many RBCs are infected after three complete cycles?
   (a) 48 (b) 256 (c) 4096 (d) 65 536
5. An earthworm has 120 segments. Setae are absent from the first segment, the clitellum and the last segment. How many segments bear setae?
   (a) 116 (b) 115 (c) 117 (d) 113
6. An earthworm is cut transversely between segments 9 and 10. The front piece contains the
   (a) testes and ovaries (b) clitellum and female pore (c) intestinal caeca (d) gizzard and spermathecae
7. An earthworm placed on dry filter paper soon dies because
   (a) gas exchange through its dry skin stops (b) its gills collapse (c) its lungs are damaged (d) its tracheae close
8. Earthworms in acidic, humus-rich soil rely most on which structure to keep their gut contents from becoming too acidic?
   (a) typhlosole (b) gizzard (c) calciferous glands (d) chloragogen cells
9. A frog's heart beats 40 times a minute, pumping 0.25 mL each beat, and its blood volume is 6 mL. How long does the whole blood volume take to pass once through the heart?
   (a) 24 s (b) 36 s (c) 60 s (d) 15 s
10. Tadpoles reared in iodine-free water fail to metamorphose because they
   (a) cannot absorb oxygen through their gills (b) cannot digest plants (c) cannot develop lungs without air (d) cannot make enough thyroxine
11. In the frog, which vessel receives the least oxygenated blood leaving the heart?
   (a) pulmocutaneous arch (b) carotid arch (c) systemic arch (d) pulmonary vein
12. In a dissected frog the duct leaving each kidney carries both urine and sperm. The frog is
   (a) a female (b) a tadpole (c) a male (d) a hermaphrodite

::: note Answers and explanations — Set C
**1.** (b) — a 48-hour cycle, Schüffner's dots in enlarged RBCs and relapses from hypnozoites mark *P. vivax*.
**2.** (d) — 48 hours after Monday 10 a.m. is Wednesday 10 a.m. (fever "every third day", counting Monday as day 1). Thursday (b) would be quartan.
**3.** (a) — crescent gametocytes, only ring stages in peripheral blood (schizonts hide in deep capillaries) and cerebral malaria: *P. falciparum*.
**4.** (c) — the count multiplies by 16 each cycle: 16³ = 4096. (b) is 16² (two cycles).
**5.** (b) — 120 − 1 (first) − 3 (clitellum 14–16) − 1 (last) = 115.
**6.** (d) — segments 1–9 hold the gizzard (8–9) and spermathecae (6–9); testes (10–11), ovaries (13), clitellum (14–16) and caeca (26) are behind the cut.
**7.** (a) — earthworm respiration is cutaneous and needs a moist skin; it has no gills, lungs or tracheae.
**8.** (c) — calciferous glands in the stomach wall secrete CaCO₃ that neutralises humic acid.
**9.** (b) — output = 0.25 mL × 40 min⁻¹ = 10 mL min⁻¹; time = 6 mL ÷ 10 mL min⁻¹ = 0.6 min = 36 s.
**10.** (d) — thyroxine contains iodine; without it the thyroid cannot trigger metamorphosis and the larvae grow into giant tadpoles.
**11.** (a) — the spiral valve sends the most deoxygenated blood to the lungs and skin through the pulmocutaneous arch; the pulmonary vein brings blood *to* the heart.
**12.** (c) — only the male's ureter is a urinogenital duct; in the female the oviduct is separate.
:::

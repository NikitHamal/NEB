---
subject: Zoology
grade: CEE
unit: 2
title: Animal Diversity and Classification
hours: 4
area: Evolution and Diversity
---

Animal Diversity and Classification carries **4 of the 40 Zoology questions**,
all from one syllabus line: the diagnostic features and classification of
animals from Protozoa to Chordata. The questions are of three kinds — "which
phylum or class has this feature" (flame cells, choanocytes, water vascular
system, placoid scales), "which animal is this" (the scientific name behind a
common name), and "which statement is true of this group" (coelom, symmetry,
excretory organ, heart). Learn the tables in this chapter column by column.

::: key What the paper asks from this chapter
- The five **bases of classification**: level of organisation, symmetry, germ layers, coelom (acoelomate, pseudocoelomate, schizocoelous, enterocoelous) and segmentation — and which phylum shows which.
- One **unique feature per phylum**: choanocytes (Porifera), cnidoblasts (Cnidaria), flame cells (Platyhelminthes), pseudocoel (Aschelminthes), metameres with setae (Annelida), jointed legs (Arthropoda), mantle and radula (Mollusca), water vascular system (Echinodermata), notochord (Chordata).
- The **classes** with their examples: Protozoa by locomotory organelle; Hydrozoa/Scyphozoa/Anthozoa; Turbellaria/Trematoda/Cestoda; Polychaeta/Oligochaeta/Hirudinea; Crustacea, Myriapoda, Insecta, Arachnida; the seven classes of Mollusca; five of Echinodermata.
- **Excretory and respiratory organs**: flame cells, renette cells, nephridia, Malpighian tubules, green glands, organ of Bojanus, kidneys; gills, book lungs, book gills, tracheae.
- **Chordate characters** and the three subphyla; the seven vertebrate classes compared on skin, skeleton, heart, temperature, excretion and egg.
- **Common-name traps**: silverfish, starfish, jellyfish, cuttlefish and crayfish are not fishes; the sea horse is.
- Parasites and vectors with their diseases (*Leishmania*, *Trypanosoma*, *Taenia*, *Wuchereria*, *Ancylostoma*).
:::

## 2.1 Diagnostic features and classification of animals from Protozoa to Chordata

### The bases of classification

| Basis | States | Found in |
|---|---|---|
| **Level of organisation** | protoplasmic (one cell does everything) | Protozoa |
| | cellular (cells with division of labour, no true tissues) | Porifera |
| | tissue | Coelenterata, Ctenophora |
| | organ | Platyhelminthes |
| | organ-system | Aschelminthes to Chordata |
| **Symmetry** | asymmetrical | most sponges; adult snails (after torsion) |
| | radial (any plane through the oral–aboral axis halves the body) | Coelenterata; adult Echinodermata (pentaradial) |
| | biradial | Ctenophora, sea anemones |
| | bilateral (one plane only) | Platyhelminthes to Chordata; echinoderm larvae |
| **Germ layers** | diploblastic (ectoderm + endoderm, non-cellular mesogloea between) | Coelenterata, Ctenophora (Porifera are usually grouped here) |
| | triploblastic (mesoderm added) | Platyhelminthes onwards |
| **Coelom** | acoelomate (space packed with mesodermal parenchyma) | Platyhelminthes |
| | pseudocoelomate (cavity not fully lined by mesoderm — a blastocoel remnant) | Aschelminthes |
| | eucoelomate, **schizocoelous** (mesoderm splits) | Annelida, Arthropoda, Mollusca |
| | eucoelomate, **enterocoelous** (pouches from the gut) | Echinodermata, Hemichordata, Chordata |
| **Segmentation** | metameric (true, repeated organs) | Annelida, Arthropoda, Chordata |
| | pseudometamerism (proglottids budded off) | tapeworms |
| **Embryo** | **protostome**: blastopore → mouth; spiral, determinate cleavage | Annelida, Arthropoda, Mollusca |
| | **deuterostome**: blastopore → anus; radial, indeterminate cleavage | Echinodermata, Hemichordata, Chordata |
| **Notochord** | absent (non-chordates) / present (chordates) | — |

The **true coelom** is a cavity lined on both sides by mesoderm: the outer
**parietal (somatic)** layer on the body wall and the inner **visceral
(splanchnic)** layer on the gut. In Arthropoda and Mollusca the coelom is
reduced and the main body cavity is a blood-filled **haemocoel**.

```figure caption="The three body plans in transverse section. Acoelomate: mesoderm fills the space between body wall and gut. Pseudocoelomate: a cavity lies between the mesoderm of the body wall and the endoderm of the gut, which has no mesoderm of its own. Coelomate: mesoderm lines both the body wall and the gut, and the coelom lies within it."
fig, axs = plt.subplots(1, 3, figsize=(7.0, 3.5))
EC, ME, EN, GU = "#bcd3ec", "#f2c4bd", "#f5e3c0", "#ffffff"
def ring(ax, r0, r1, fc):
    ax.add_patch(matplotlib.patches.Wedge((0, 0), r1, 0, 360, width=r1 - r0, fc=fc, ec="#6b7686", lw=0.9))
plans = [("Acoelomate", "(Platyhelminthes)", None), ("Pseudocoelomate", "(Aschelminthes)", "pseudocoel"), ("Coelomate", "(Annelida to Chordata)", "coelom")]
for ax, (nm, ex, cav) in zip(axs, plans):
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-2.35, 1.5); ax.set_aspect("equal"); ax.axis("off")
    ring(ax, 0.92, 1.0, EC)
    if cav is None:
        ring(ax, 0.34, 0.92, ME)
    elif cav == "pseudocoel":
        ring(ax, 0.80, 0.92, ME); ring(ax, 0.34, 0.80, GU)
    else:
        ring(ax, 0.80, 0.92, ME); ring(ax, 0.58, 0.80, GU); ring(ax, 0.46, 0.58, ME); ring(ax, 0.34, 0.46, ME)
    ring(ax, 0.16, 0.34, EN); ring(ax, 0.0, 0.16, GU)
    if cav:
        ax.annotate(cav, xy=(0.0, -0.69 if cav == "coelom" else -0.57), xytext=(0.0, -1.45), ha="center", fontsize=8, color="#b0472c", arrowprops=dict(arrowstyle="-", color="#b0472c", lw=0.9))
        ax.text(0, -1.78, nm, ha="center", fontsize=9, fontweight="bold"); ax.text(0, -2.1, ex, ha="center", fontsize=7.8, color=MUTED)
    else:
        ax.text(0, -1.5, nm, ha="center", fontsize=9, fontweight="bold"); ax.text(0, -1.82, ex, ha="center", fontsize=7.8, color=MUTED)
        ax.text(0, -2.15, "no body cavity: mesoderm is solid", ha="center", fontsize=7.4, color=MUTED)
for i, (c, n) in enumerate(((EC, "ectoderm"), (ME, "mesoderm"), (EN, "endoderm (gut wall)"))):
    pass
fig.legend(handles=[matplotlib.patches.Patch(fc=EC, ec="#6b7686", label="ectoderm"), matplotlib.patches.Patch(fc=ME, ec="#6b7686", label="mesoderm"), matplotlib.patches.Patch(fc=EN, ec="#6b7686", label="endoderm (gut wall)")], loc="lower center", ncol=3, fontsize=8, frameon=False)
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.1, wspace=0.02)
```

```figure caption="The classification tree of the animal phyla. Each fork is one basis of classification; read a phylum's characters off its path from the root."
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.2, 4.3))
ax.set_xlim(-0.3, 10.6); ax.set_ylim(-0.6, 9.6); ax.axis("off")
leaves = ["Porifera (sponges)", "Coelenterata (jellyfish, corals)",
          "Platyhelminthes (flatworms)", "Aschelminthes (roundworms)",
          "Annelida (segmented worms)", "Arthropoda (jointed legs)",
          "Mollusca (mantle, shell)", "Echinodermata (spiny skin)",
          "Hemichordata (acorn worms)", "Chordata (notochord)"]
Y = [9 - i for i in range(10)]
LX = 6.7
for n, y in zip(leaves, Y):
    ax.add_patch(FancyBboxPatch((LX, y - 0.32), 3.8, 0.64,
                 boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc="#eef3f8", ec=SERIES[0], lw=0.8))
    ax.text(LX + 0.12, y, n, fontsize=6.9, color=INK, va="center")
def fork(x, y_parent, kids):
    for y_kid, x_end in kids:
        ax.plot([x, x, x_end], [y_parent, y_kid, y_kid], color=MUTED, lw=1.0)
xr, xe, xb, xc, xp = 0.15, 1.0, 2.6, 3.95, 5.6
yP = (Y[4] + Y[5] + Y[6]) / 3
yD = (Y[7] + Y[8] + Y[9]) / 3
fork(xp, yP, [(Y[4], LX), (Y[5], LX), (Y[6], LX)])
fork(xp, yD, [(Y[7], LX), (Y[8], LX), (Y[9], LX)])
yc = (yP + yD) / 2
fork(xc, yc, [(yP, xp), (yD, xp)])
yb = (Y[2] + Y[3] + yc) / 3
fork(xb, yb, [(Y[2], LX), (Y[3], LX), (yc, xc)])
ye = (Y[1] + yb) / 2
fork(xe, ye, [(Y[1], LX), (yb, xb)])
yr = (Y[0] + ye) / 2
fork(xr, yr, [(Y[0], LX), (ye, xe)])
ax.text(xr - 0.08, yr, "Animalia", rotation=90, ha="right", va="center",
        fontsize=7.0, color=INK)
fs = 6.6
up = dict(fontsize=fs, color=SERIES[1], va="bottom")
dn = dict(fontsize=fs, color=SERIES[1], va="top")
ax.text(xr + 0.12, Y[0] + 0.06, "cellular level", **up)
ax.text(xe + 0.12, Y[1] + 0.06, "tissue level, radial, diploblastic", **up)
ax.text(xb + 0.12, Y[2] + 0.06, "acoelomate", **up)
ax.text(xb + 0.12, Y[3] + 0.06, "pseudocoelomate", **up)
ax.text(xe + 0.10, yb + 0.06, "bilateral,", **up)
ax.text(xe + 0.10, yb - 0.08, "triploblastic", **dn)
ax.text(xb + 0.10, yc + 0.06, "coelomate", **up)
ax.text(xc + 0.08, yP + 0.06, "protostomes", **up)
ax.text(xc + 0.08, yP - 0.08, "(schizocoel)", **dn)
ax.text(xc + 0.08, yD + 0.06, "deuterostomes", **up)
ax.text(xc + 0.08, yD - 0.08, "(enterocoel)", **dn)
```

### The phyla at a glance

| Phylum | Level | Symmetry | Coelom | Gut | Circulation | Respiration | Excretion | Nervous system |
|---|---|---|---|---|---|---|---|---|
| Protozoa | protoplasmic | various | — | food vacuoles | — | diffusion | contractile vacuole, diffusion | — |
| Porifera | cellular | asymmetrical / radial | none | none (canal system) | none | diffusion | diffusion | none |
| Coelenterata | tissue | radial | none (coelenteron) | blind sac, one opening | none | diffusion | diffusion | **nerve net** |
| Platyhelminthes | organ | bilateral | acoelomate | incomplete (no anus) or absent | none | diffusion | **flame cells** | ladder-like |
| Aschelminthes | organ-system | bilateral | **pseudocoel** | complete | none | diffusion | **renette cells** / canals | circum-pharyngeal ring + cords |
| Annelida | organ-system | bilateral | schizocoel | complete | **closed** | skin, gills | **nephridia** | ventral, double, ganglionated |
| Arthropoda | organ-system | bilateral | **haemocoel** | complete | **open**, dorsal heart | gills, tracheae, book lungs | **Malpighian tubules**, green glands | ventral, double, ganglionated |
| Mollusca | organ-system | bilateral (snails asymmetrical) | reduced (pericardial) | complete, **radula** | open (closed in cephalopods) | gills (ctenidia), pulmonary sac | kidneys / **organ of Bojanus** | ganglia |
| Echinodermata | organ-system | pentaradial adult, bilateral larva | enterocoel | complete | haemal system | tube feet, dermal branchiae | none | nerve ring, no brain |
| Chordata | organ-system | bilateral | enterocoel | complete | closed, **ventral heart** | gills or lungs | kidneys | **dorsal, hollow** |

### Protozoa (kingdom Protista)

In the five-kingdom system the protozoans are the **animal-like protists**; the
syllabus begins animal classification with them.

```photo id="bio11/amoeba" caption="*Amoeba proteus* under differential interference contrast: a single cell that moves by extending blunt pseudopodia (compare with ciliary movement in *Paramecium*)." width="84"
```


- Unicellular **eukaryotes** at the protoplasmic level; free-living or parasitic.
- No cell wall; body covered by plasma membrane or a firm **pellicle**.
- Nutrition holozoic, holophytic (*Euglena*), saprozoic or parasitic.
- Locomotion by **pseudopodia, flagella or cilia**; Sporozoa have none.
- Osmoregulation by **contractile vacuoles** in fresh-water forms; respiration and excretion by diffusion.
- Asexual reproduction by binary or multiple fission; sexual by syngamy or **conjugation**; **cysts** survive bad conditions.

| Class | Locomotion | Examples (and diseases) |
|---|---|---|
| **Rhizopoda (Sarcodina)** | **pseudopodia** | *Amoeba proteus*; ***Entamoeba histolytica*** (amoebic dysentery); *E. gingivalis* (in the gums); *Elphidium* (*Polystomella*, a foraminiferan) |
| **Mastigophora (Flagellata)** | **flagella** | *Euglena viridis*; ***Trypanosoma gambiense*** (African sleeping sickness, by the tsetse fly *Glossina*); ***Leishmania donovani*** (**kala-azar**, by the sandfly *Phlebotomus* — endemic in Nepal's Terai); *Giardia intestinalis* (diarrhoea); *Trichomonas vaginalis*; *Noctiluca* (sea luminescence); *Trichonympha* (digests cellulose in termites) |
| **Sporozoa (Apicomplexa)** | **none** in the adult; all parasites; form spores | ***Plasmodium*** (malaria, by female *Anopheles*); *Monocystis* (seminal vesicles of earthworm); *Eimeria* (coccidiosis of poultry); *Toxoplasma* |
| **Ciliata** | **cilia**; two kinds of nuclei (macronucleus, micronucleus) | *Paramecium caudatum* (slipper animalcule); *Vorticella* (bell animalcule); ***Balantidium coli*** (the only ciliate parasite of man, dysentery); *Nyctotherus* (rectum of frog) |

### Phylum Porifera — sponges

- Aquatic, mostly **marine**, sessile; asymmetrical or radial; **cellular level**.
- Body perforated by many small pores, the **ostia** (incurrent), and one large **osculum** (excurrent); the body cavity is the **spongocoel**.
- **Canal (water-current) system** — ostia → canals → spongocoel → osculum — brings food and O₂ and removes waste. Types: **ascon** (*Leucosolenia*), **sycon** (*Sycon*), **leucon** (*Spongilla*, *Euspongia*).
- **Choanocytes (collar cells)** line the spongocoel or chambers and drive the current; digestion is **intracellular**.
- Skeleton of **spicules** (calcareous or siliceous) and/or **spongin** fibres.
- No mouth, gut, muscles, nerves or organs. Hermaphrodite; fertilisation internal; larva **amphiblastula** or parenchymula. Asexual by budding, fragmentation and **gemmules** (internal buds of fresh-water sponges). Great power of regeneration.

| Class | Skeleton | Examples |
|---|---|---|
| **Calcarea** (Calcispongiae) | calcareous (CaCO₃) spicules | *Sycon* (*Scypha*), *Leucosolenia*, *Grantia* |
| **Hexactinellida** (Hyalospongiae) — glass sponges | **six-rayed siliceous** spicules | ***Euplectella*** (**Venus' flower basket**), *Hyalonema* (glass-rope sponge) |
| **Demospongiae** | **spongin** fibres with or without siliceous spicules | ***Euspongia*** (**bath sponge**), ***Spongilla*** (**fresh-water sponge**), *Cliona* (boring sponge), *Chalina* (dead man's fingers) |

### Phylum Coelenterata (Cnidaria)

- Aquatic, mostly marine (*Hydra* is fresh-water); solitary or colonial; **radial symmetry**; **tissue level**; **diploblastic** with a non-cellular **mesogloea**.
- One cavity, the **coelenteron (gastrovascular cavity)**, opening by the **mouth** on a raised **hypostome**; no anus. Digestion extracellular, then intracellular.
- **Cnidoblasts (cnidocytes)** with **nematocysts** (stinging capsules) on the tentacles — the diagnostic feature; for prey capture, defence and anchorage.
- Two body forms: the sessile, cylindrical **polyp** (asexual) and the free-swimming, umbrella-shaped **medusa** (sexual). Their alternation is **metagenesis** (*Obelia*). **Polymorphism**: different zooids in one colony (*Physalia*).
- **Nerve net**, no brain; no respiratory, circulatory or excretory organs. Larva **planula**. Corals secrete a CaCO₃ skeleton and build reefs.

| Class | Dominant form | Examples |
|---|---|---|
| **Hydrozoa** | polyp, medusa or both; medusa with a velum | ***Hydra*** (polyp only), ***Obelia*** (sea fur, metagenesis), ***Physalia*** (**Portuguese man-of-war**), *Velella* |
| **Scyphozoa** | **medusa** dominant (true jellyfish) | ***Aurelia*** (moon jelly), *Rhizostoma*, *Cyanea* |
| **Anthozoa** (Actinozoa) | **polyp only**, no medusa | sea anemones ***Metridium***, ***Adamsia*** (on the hermit crab's shell); corals ***Corallium*** (red coral), *Madrepora*, *Meandrina* (brain coral), *Fungia* (mushroom coral); ***Gorgonia*** (sea fan), ***Pennatula*** (sea pen) |

**Ctenophora (comb jellies)** are a small marine phylum close to the Cnidaria:
biradial, diploblastic, with **eight rows of comb plates (ctenes)** of fused cilia for
swimming, **colloblasts (lasso cells)** instead of nematocysts, and strong
**bioluminescence**: *Pleurobrachia* (sea gooseberry), *Ctenoplana*.

```photo id="bio11/hydra" caption="A living *Hydra*: a slender column attached by its basal disc, with tentacles around the mouth (hypostome) at the free end. Its green colour comes from symbiotic algae." width="68"
```


### Phylum Platyhelminthes — flatworms

- **Dorsoventrally flattened**; **bilateral**, **triploblastic**, **acoelomate** (parenchyma fills the body); organ level; head present.
- Mostly **endoparasites** with **hooks and suckers**; thick tegument resists host enzymes.
- Gut **incomplete** (mouth, no anus) or **absent** (tapeworms absorb food through the body surface).
- Excretion and osmoregulation by **flame cells** (protonephridia).
- Mostly **hermaphrodite**; internal fertilisation; complicated life cycles with one or two hosts. *Planaria* regenerates whole worms from small pieces.

| Class | Features | Examples (and diseases) |
|---|---|---|
| **Turbellaria** | free-living, ciliated epidermis | *Dugesia* (*Planaria*) |
| **Trematoda** (flukes) | parasitic, suckers, branched gut | ***Fasciola hepatica*** (**liver fluke** of sheep; snail *Lymnaea* is the intermediate host; larvae miracidium → sporocyst → redia → cercaria); ***Schistosoma*** (blood fluke, schistosomiasis) |
| **Cestoda** (tapeworms) | ribbon-like; **scolex** with suckers (± hooks); chain of **proglottids**; no gut | ***Taenia solium*** (**pork tapeworm**: scolex armed with hooks; pig is the intermediate host; its larva in man's brain causes **neurocysticercosis**); ***T. saginata*** (beef tapeworm, scolex without hooks); ***Echinococcus granulosus*** (dog tapeworm; **hydatid cyst** in man) |

### Phylum Aschelminthes (Nemathelminthes, Nematoda) — roundworms

- **Cylindrical, unsegmented**, tapering at both ends; tough **cuticle**; bilateral, triploblastic, organ-system level.
- **Pseudocoelomate** — the first body cavity.
- **Complete gut** (mouth and anus) with a muscular pharynx — the first "tube within a tube".
- Only longitudinal muscles in the body wall (whip-like movement). No circulatory or respiratory organs; excretion by **excretory canals / renette cells**.
- **Sexes separate (dioecious)** with **sexual dimorphism**: the male is smaller with a curved tail bearing penial spicules. No cilia anywhere.

| Worm | Common name | Disease / note |
|---|---|---|
| ***Ascaris lumbricoides*** | common roundworm | ascariasis (small intestine) |
| ***Enterobius vermicularis*** | **pinworm** (seat worm) | children; anal itching |
| ***Ancylostoma duodenale*** | **hookworm** | larvae enter through the skin of bare feet; blood-sucking → **anaemia** |
| ***Wuchereria bancrofti*** | filarial worm | **filariasis (elephantiasis)**; vector *Culex* mosquito |
| ***Dracunculus medinensis*** | guinea worm | intermediate host *Cyclops* (in drinking water) |
| *Trichinella spiralis* | trichina worm | trichinosis from undercooked pork |
| *Loa loa* | eye worm | under the skin and over the eye |
| *Caenorhabditis elegans* | — | free-living model organism of genetics |

### Phylum Annelida — segmented worms

- Elongated, **metamerically segmented** — the first true segmentation; bilateral, triploblastic, **coelomate** (schizocoelous).
- Thin moist **cuticle**; locomotion by **setae (chaetae)**, **parapodia** or suckers, with circular and longitudinal muscles working on the coelomic fluid (hydrostatic skeleton).
- **Closed circulatory system**; **haemoglobin dissolved in the plasma**.
- Excretion by **nephridia**; respiration through the moist skin (gills in some polychaetes).
- Ventral, double, ganglionated nerve cord with a nerve ring.
- Hermaphrodite (earthworm, leech) or dioecious (*Nereis*); polychaetes have a **trochophore** larva.

| Class | Diagnostic | Examples |
|---|---|---|
| **Polychaeta** | marine; **parapodia** with many setae; no clitellum; dioecious; trochophore | ***Nereis*** (sandworm, clam worm), ***Aphrodite*** (**sea mouse**), *Chaetopterus*, *Arenicola* (lugworm) |
| **Oligochaeta** | few setae, no parapodia; **clitellum**; hermaphrodite; direct development | ***Pheretima posthuma*** (Indian earthworm), *Lumbricus terrestris*, *Tubifex* |
| **Hirudinea** (leeches) | no setae or parapodia; fixed number of segments (about 33); **anterior and posterior suckers**; hermaphrodite; coelom filled by botryoidal tissue | ***Hirudinaria granulosa*** (cattle leech), ***Hirudo medicinalis*** (medicinal leech — saliva has the anticoagulant **hirudin**), *Haemadipsa* (land leech of the monsoon hills) |

### Phylum Arthropoda — jointed-legged animals

The **largest phylum**: more than two-thirds of all named animal species.

- **Jointed appendages**; **chitinous exoskeleton** shed by **moulting (ecdysis)**.
- Body segmented and grouped into **head, thorax and abdomen** or **cephalothorax and abdomen**.
- Coelom reduced; body cavity a blood-filled **haemocoel**; **open circulation** with a dorsal heart.
- Respiration by **gills**, **book gills** (*Limulus*), **book lungs** (scorpions, spiders), **tracheae** (insects, myriapods) or the body surface.
- Excretion by **Malpighian tubules** (insects, myriapods, arachnids), **green (antennal) glands** (crustaceans) or **coxal glands** (arachnids).
- **Compound eyes**; ventral double nerve cord; sexes usually separate; fertilisation internal; often metamorphosis.

| Class | Body | Antennae | Legs | Respiration / excretion | Examples |
|---|---|---|---|---|---|
| **Crustacea** | cephalothorax (with carapace) + abdomen | **2 pairs** | many, biramous | **gills** / **green glands**; nauplius larva | ***Palaemon*** (prawn), *Astacus* (crayfish), *Cancer* (crab), *Daphnia* (water flea), ***Cyclops***, *Balanus* (barnacle), *Sacculina* (parasite of crabs), *Eupagurus* (hermit crab) |
| **Chilopoda** (Myriapoda) — centipedes | head + many trunk segments | 1 pair | **1 pair per segment**; first pair are poison claws | tracheae / Malpighian tubules | ***Scolopendra*** |
| **Diplopoda** (Myriapoda) — millipedes | head + many trunk segments | 1 pair | **2 pairs per segment** | tracheae / Malpighian tubules | ***Julus***, *Spirostreptus* |
| **Insecta** (Hexapoda) | **head, thorax, abdomen** | 1 pair | **3 pairs**; usually 2 pairs of wings | **tracheae** / **Malpighian tubules** | ***Periplaneta americana*** (cockroach), *Musca domestica*, *Anopheles*, *Aedes*, *Culex*, *Apis* (honey bee), ***Bombyx mori*** (silk moth), ***Laccifer (Kerria) lacca*** (lac insect), *Locusta*, *Pediculus* (louse), *Cimex* (bed bug), *Xenopsylla* (rat flea, plague), ***Lepisma*** (silverfish, wingless) |
| **Arachnida** | cephalothorax + abdomen | **none** | **4 pairs**; chelicerae and pedipalps | **book lungs** or tracheae / Malpighian tubules, coxal glands | *Palamnaeus* and *Buthus* (scorpions), *Aranea* (spider), ***Sarcoptes scabiei*** (itch mite, scabies), ticks |
| **Merostomata** | cephalothorax with horseshoe carapace + abdomen | none | 5 pairs + book gills | **book gills** | ***Limulus*** (**king crab**, a living fossil — not a true crab) |
| **Onychophora** | worm-like, soft cuticle | 1 pair | unjointed stumpy legs | tracheae / nephridia | ***Peripatus*** (Annelida–Arthropoda link) |

| Insect vector | Disease it spreads |
|---|---|
| female *Anopheles* | malaria |
| *Aedes aegypti* | dengue, chikungunya, yellow fever |
| *Culex* | filariasis, Japanese encephalitis |
| *Phlebotomus* (sandfly) | kala-azar |
| *Glossina* (tsetse fly) | sleeping sickness |
| *Xenopsylla cheopis* (rat flea) | plague |
| *Musca domestica* (housefly) | mechanical carrier of typhoid, cholera, dysentery |

### Phylum Mollusca — soft-bodied animals

The **second largest** phylum.

- Soft, **unsegmented** body (except *Neopilina*) of **head, muscular foot and visceral hump**; bilateral, but snails become asymmetrical by **torsion** (180° twisting of the visceral mass).
- The **mantle (pallium)** covers the hump and secretes the calcareous **shell**; the **mantle cavity** holds the gills (**ctenidia**).
- **Radula** — a rasping, file-like tongue with chitinous teeth (absent in bivalves).
- Coelom reduced to the pericardial cavity and gonad cavities; **open circulation** (closed in cephalopods); respiratory pigment **haemocyanin** (copper).
- Excretion by kidneys (the **organ of Bojanus** in bivalves such as *Lamellidens*); **osphradium** tests the water entering the mantle cavity.
- Sexes usually separate; larvae **trochophore** and **veliger**.

| Class | Diagnostic | Examples |
|---|---|---|
| **Monoplacophora** | single cap-like shell; serially repeated gills and nephridia | ***Neopilina*** (living fossil; Annelida–Mollusca link) |
| **Polyplacophora** (Amphineura) | **8 dorsal shell plates** | ***Chiton*** |
| **Aplacophora** | worm-like, no shell, spicules in the skin | *Neomenia*, *Chaetoderma* |
| **Scaphopoda** | **tusk-shaped tubular shell open at both ends** | ***Dentalium*** (tusk shell) |
| **Gastropoda** | **torsion**; coiled shell (or none); distinct head with tentacles | ***Pila globosa*** (apple snail), *Helix* (land snail), ***Limax*** (slug, no shell), *Aplysia* (sea hare), *Doris* (sea lemon), *Patella* (limpet), *Lymnaea* (pond snail) |
| **Pelecypoda** (Bivalvia, Lamellibranchiata) | **two hinged valves**; **no head, no radula**; filter feeders | ***Lamellidens*** and *Unio* (fresh-water mussels), *Mytilus* (sea mussel), ***Ostrea*** (edible oyster), ***Pinctada*** (**pearl oyster**), ***Teredo*** (shipworm, bores wood), *Pecten* (scallop) |
| **Cephalopoda** | foot modified into **arms/tentacles around the head**; **closed circulation**; large eyes; ink gland; shell internal or absent (external only in *Nautilus*) | ***Sepia*** (**cuttlefish**), ***Loligo*** (**squid**), ***Octopus*** (**devil fish**), ***Nautilus***, *Architeuthis* (giant squid, among the largest invertebrates) |

### Phylum Echinodermata — spiny-skinned animals

- **All marine**; adults **pentaradial**, larvae **bilateral**; triploblastic, **enterocoelous** deuterostomes.
- **Endoskeleton** of calcareous **ossicles** with spines (from mesoderm) — hence "spiny skin".
- **Water vascular (ambulacral) system** — sea water enters by the **madreporite** and works the **tube feet (podia)** for locomotion, food capture and respiration — the diagnostic feature.
- No head, no brain, **no excretory organs**; open haemal system; **pedicellariae** clean the surface.
- Sexes separate; external fertilisation; many free-swimming larvae; great **regeneration** (starfish).

| Class | Diagnostic | Larva | Examples |
|---|---|---|---|
| **Asteroidea** (starfishes) | star-shaped; arms not sharply marked off from the disc; tube feet with suckers in open ambulacral grooves | **bipinnaria**, brachiolaria | ***Asterias***, *Pentaceros* (*Oreaster*) |
| **Ophiuroidea** (brittle stars) | long slender arms **sharply set off** from a round disc | ophiopluteus | ***Ophiura***, *Ophiothrix* |
| **Echinoidea** (sea urchins, sand dollars) | globular or flat; no arms; movable spines; chewing **Aristotle's lantern** | echinopluteus | ***Echinus***, *Clypeaster* (sand dollar), *Echinocardium* (heart urchin) |
| **Holothuroidea** (sea cucumbers) | elongated, leathery; ossicles microscopic; **respiratory trees**; evisceration | auricularia | ***Cucumaria***, *Holothuria* |
| **Crinoidea** (sea lilies, feather stars) | cup-shaped, feathery arms; stalked or free; mouth faces up | doliolaria | ***Antedon*** (**feather star**), *Metacrinus* (sea lily) |

### Hemichordata

Worm-like marine burrowers with a body of **proboscis, collar and trunk**,
pharyngeal **gill slits** and a dorsal nerve cord in the collar. Their
**stomochord** (buccal diverticulum) was once taken for a notochord, so older
books made them a subphylum of Chordata; today they are a separate
non-chordate phylum. The **tornaria** larva resembles echinoderm larvae.
Examples: ***Balanoglossus*** (acorn worm), *Saccoglossus*.

```photo id="bio11/asterias" caption="The starfish *Asterias*: a pentamerous body of five arms around a central disc with the spiny, studded upper surface visible." width="60"
```


```photo id="bio11/cockroach" caption="The American cockroach *Periplaneta americana*: a flattened body in head, thorax and abdomen, with long antennae, wings and three pairs of jointed legs." width="60"
crop 0.0 0.13 1 1
```


```photo id="bio11/earthworm-ext" caption="A living earthworm on moist ground: elongated, cylindrical and segmented, with no limbs." width="70"
crop 0.3 0.25 0.9 0.8
```


```photo id="bio11/ascaris-jar" caption="Preserved *Ascaris lumbricoides* in a jar: long, cylindrical, unsegmented, tapering at both ends." width="34"
```


```photo id="bio11/planaria" caption="*Planaria*, a free-living flatworm: leaf-shaped, flattened from top to bottom and unsegmented, with a smooth ciliated surface." width="70"
```


```photo id="bio11/paramecium" caption="*Paramecium caudatum* cells in a culture, light microscopy. The scale bar is 50 μm; the cells are slipper-shaped with a blunt front end and a tapering rear end." width="84"
```


### Phylum Chordata

Four **fundamental characters**, present at least in the embryo:

1. a **notochord** — a flexible rod of vacuolated cells dorsal to the gut;
2. a **dorsal, hollow, single nerve cord**;
3. paired **pharyngeal gill slits**;
4. a **post-anal tail**.

| Character | Non-chordates | Chordates |
|---|---|---|
| Notochord | absent | present (at least in the embryo) |
| Nerve cord | **ventral, solid, double**, ganglionated | **dorsal, hollow, single** |
| Pharyngeal gill slits | absent | present |
| Heart | dorsal (if present) | **ventral** |
| Post-anal tail | absent | present |
| Blastopore | usually becomes mouth (protostomes) | becomes **anus** (deuterostomes) |

| Subphylum | Notochord | Features | Examples |
|---|---|---|---|
| **Urochordata** (Tunicata) | **only in the larval tail** | marine, sessile adult in a **tunic** of tunicin; free-swimming tadpole larva; **retrogressive metamorphosis** | ***Herdmania***, *Ascidia* (sea squirt), *Salpa*, *Doliolum* |
| **Cephalochordata** | **from head to tail, throughout life** | small, fish-like, burrowing filter feeders; no head, no paired fins | ***Branchiostoma*** (**Amphioxus**, the lancelet) |
| **Vertebrata** (Craniata) | replaced by the **vertebral column** in the adult | cranium round the brain; paired appendages; muscular ventral heart with chambers; kidneys | fishes to mammals |

Urochordata and Cephalochordata together are the **protochordates**. Every
vertebrate is a chordate, but not every chordate is a vertebrate.

```photo id="bio11/rohu" caption="The rohu, *Labeo rohita*, a common freshwater carp: streamlined body, overlapping scales, paired and median fins and a forked tail." width="72"
```


Vertebrata divides into **Agnatha** (jawless — class Cyclostomata) and
**Gnathostomata** (jawed — super-class Pisces with the two fish classes, and
super-class Tetrapoda with four-limbed Amphibia, Reptilia, Aves and Mammalia).

```photo id="bio11/rana-tigrina" caption="The Indian bullfrog *Hoplobatrachus tigerinus* (the frog historically called *Rana tigrina*). It has smooth moist skin, large eyes, a broad head and webbed hind feet." width="76"
```


| Class | Skin / exoskeleton | Skeleton | Heart | Respiration | Body temperature | Excretion | Reproduction | Examples |
|---|---|---|---|---|---|---|---|---|
| **Cyclostomata** | soft, **no scales** | cartilaginous; notochord persists | 2-chambered | 6–15 pairs of gill slits | cold-blooded | ammonia | migrate to fresh water to spawn (lamprey); larva ammocoete | ***Petromyzon*** (lamprey, ectoparasite of fish), ***Myxine*** (hagfish) |
| **Chondrichthyes** (cartilaginous fish) | **placoid scales** | **cartilaginous** | 2-chambered | 5–7 pairs of **separate gill slits, no operculum**; **no air bladder** | cold-blooded | urea | **claspers** in males; internal fertilisation; many viviparous; heterocercal tail; **ventral mouth** | ***Scoliodon*** (dogfish), ***Pristis*** (sawfish), ***Torpedo*** (electric ray), ***Trygon*** (stingray), *Carcharodon* (great white shark) |
| **Osteichthyes** (bony fish) | **cycloid or ctenoid scales** | **bony** | 2-chambered (venous) | 4 pairs of gills under an **operculum**; **air (swim) bladder** | cold-blooded | ammonia | mostly oviparous, external fertilisation; terminal mouth; homocercal tail | ***Labeo rohita*** (rohu), *Catla catla*, *Clarias* (magur), ***Hippocampus*** (sea horse), ***Exocoetus*** (flying fish), ***Anabas*** (climbing perch), *Pterophyllum* (angel fish), *Betta* (fighting fish), *Protopterus* (lungfish) |
| **Amphibia** | **moist, glandular, no scales** | bony | **3-chambered** (2 atria + 1 ventricle) | gills (larva), lungs, **skin**, buccopharynx | cold-blooded | urea (adult) | **cloaca**; external fertilisation in water; tadpole larva, metamorphosis; tympanum | ***Rana*** (frog), ***Bufo*** (toad), ***Hyla*** (tree frog), *Salamandra*, ***Ichthyophis*** (**limbless**), *Necturus* |
| **Reptilia** | **dry, cornified, epidermal scales** or scutes | bony | **3-chambered; 4 in crocodiles** | lungs | cold-blooded | **uric acid** | internal fertilisation; **cleidoic (shelled, amniotic) eggs**; direct development; snakes and lizards moult | ***Chelone*** (turtle), *Testudo* (tortoise), ***Calotes*** (garden lizard), *Hemidactylus* (wall lizard), *Chamaeleo*, *Draco* (flying lizard), ***Crocodylus***, *Alligator*, ***Gavialis*** (gharial), ***Naja*** (cobra), *Bungarus* (krait), *Vipera* (viper), *Python* |
| **Aves** | **feathers**; scales on legs; only the oil (preen) gland | bony, **pneumatic** (air-filled) | **4-chambered** | lungs + **air sacs** | **warm-blooded** | uric acid | beak without teeth; crop and gizzard; **syrinx**; oviparous; **right** aortic arch | *Columba livia* (pigeon), *Corvus* (crow), *Psittacula* (parrot), ***Struthio*** (ostrich), ***Pavo cristatus*** (peafowl), ***Aptenodytes*** (penguin), *Neophron* (vulture), ***Lophophorus impejanus*** (**Danfe**, national bird of Nepal) |
| **Mammalia** | **hair**; sweat and sebaceous glands; **mammary glands** | bony; 7 neck vertebrae | **4-chambered** | lungs; **diaphragm** | **warm-blooded** | urea | external ear (pinna); teeth heterodont and replaced once; viviparous (except monotremes); **left** aortic arch; RBCs without nuclei | see below |

| Mammal sub-class | Diagnostic | Examples |
|---|---|---|
| **Prototheria** (monotremes) | **lay eggs**; cloaca; no nipples | ***Ornithorhynchus*** (duck-billed platypus), ***Tachyglossus*** (spiny anteater, *Echidna*) |
| **Metatheria** (marsupials) | young born very early and reared in a **pouch** (marsupium) | ***Macropus*** (kangaroo), *Didelphis* (opossum), *Phascolarctos* (koala) |
| **Eutheria** (placentals) | true placenta | *Homo*, *Rattus*, *Canis*, *Felis*, *Elephas*, ***Pteropus*** (flying fox), ***Balaenoptera*** (blue whale, largest animal), *Delphinus* (dolphin), *Panthera tigris* (tiger), ***Rhinoceros unicornis*** (one-horned rhinoceros), ***Ailurus fulgens*** (red panda) |

::: caution Fish or not? — the favourite trap
**Jellyfish** (Coelenterata), **starfish** (Echinodermata), **cuttlefish**
(Mollusca), **crayfish** (Crustacea), **silverfish** (*Lepisma*, an insect) and
**devil fish** (*Octopus*, Mollusca) are **not** fishes. The **sea horse**
(*Hippocampus*), the **flying fish** (*Exocoetus*) and the **lungfish** are true
bony fishes. Likewise the **sea anemone** is a cnidarian, the **sea mouse** a
polychaete, the **sea cucumber** and **sea lily** echinoderms, and the **king
crab** (*Limulus*) is not a crab.
:::

::: caution Exceptions examiners love
- Not every coelenterate has a medusa (*Hydra*, sea anemones, corals) — and *Hydra* lives in fresh water.
- Not every mollusc has a shell (*Limax*, *Octopus*) or a radula (bivalves); *Nautilus* is the only cephalopod with an external shell.
- The heart of the **crocodile** is four-chambered although it is a reptile.
- Monotremes are mammals that **lay eggs**; bats are mammals that **fly**; whales and dolphins are mammals that **swim**.
- *Ichthyophis* is a **limbless amphibian**, not a snake.
- Tapeworm proglottids are **not** true segments (pseudometamerism).
:::

::: memory The order of the phyla
**"Please Come Play And Act As My Elder Cousin"** — Porifera, Coelenterata,
Platyhelminthes, Aschelminthes, Annelida, Arthropoda, Mollusca, Echinodermata,
Chordata. Each step adds one feature: tissues → mesoderm → body cavity → true
coelom → segmentation → deuterostome plan → notochord.
:::

::: example Diagnosing a phylum from body cavity, symmetry and excretory organ
**Problem.** A bilateral, triploblastic, unsegmented endoparasite possesses a pseudocoelom, a complete digestive tract with a muscular pharynx, a syncytial epidermis, and H-shaped excretory canals lacking flame cells or cilia. Name the phylum and a human parasite belonging to it.

**Solution.** Pseudocoelom + syncytial epidermis + H-shaped renette excretory system + complete gut uniquely define **Aschelminthes (Nematoda)**, exemplified by *Ascaris lumbricoides* or *Wuchereria bancrofti*.
:::

::: example Tracing water flow through Porifera canal systems
**Problem.** Write the exact sequence of chambers water traverses in a syconoid sponge (*Sycon*) from the outside sea water to the exit opening, and name the flagellated cells that drive the current.

**Solution.** Dermal ostia $\rightarrow$ **incurrent canal** $\rightarrow$ **prosopyle** $\rightarrow$ **radial (flagellated) canal** $\rightarrow$ **apopyle** $\rightarrow$ **spongocoel** $\rightarrow$ **osculum**. The current is driven by **choanocytes (collar cells)** lining the radial canals.
:::

::: example Separating cartilaginous and bony fishes in one table read
**Problem.** A marine fish has a ventral mouth, placoid scales, 5 pairs of uncovered gill slits, a heterocercal caudal fin, lacks an air bladder, and excretes urea (ureotelic). Assign its class and contrast it with *Labeo rohita*.

**Solution.** The marine specimen belongs to **Chondrichthyes** (e.g., *Scoliodon*). *Labeo rohita* (Osteichthyes) has a terminal mouth, cycloid scales, 4 pairs of gills covered by an **operculum**, a homocercal tail, a swim bladder, and is ammonotelic.
:::

```photogrid label="2.1" cols="2" ratio="1.2" caption="Why large animals need organ systems. (a) Paramecium, a single cell about 200 micrometres long, exchanges gases and food through its surface. (b) For a sphere the surface-to-volume ratio is 3/r and for a cylinder 2/r. A bacterium (r = 1 micrometre) has 3,000,000 per metre, Paramecium 30,000, an earthworm 1,000, a frog 120 and a human 13; the ratio falls a million-fold, so diffusion through the skin cannot feed a large body. Lungs, gills, intestinal villi and capillaries are folded surfaces that bring the ratio back up, and the flat body of a flatworm is the same trick."
@ photo id="bio11/paramecium" cap="Paramecium caudatum"
fit 1.2
focus 0.5 0.5
@ svg cap="Surface-to-volume ratio (per metre, log scale)"
it = (("Bacterium, sphere r = 1 um", 3, 1e-6), ("Paramecium, sphere r = 100 um", 3, 100e-6), ("Earthworm, cylinder r = 2 mm", 2, 2e-3), ("Frog, sphere r = 2.5 cm", 3, 0.025), ("Human, cylinder r = 15 cm", 2, 0.15))
sv = [k / r for _, k, r in it]
assert round(sv[0]) == 3000000 and round(sv[1]) == 30000 and round(sv[2]) == 1000 and round(sv[3]) == 120 and abs(sv[4] - 13.33) < 0.01
facts = dict(a="{:,.0f}".format(sv[0]), b="{:,.0f}".format(sv[1]), c="{:,.0f}".format(sv[2]), d="{:,.0f}".format(sv[3]), e="%.0f" % sv[4])
f = Fig(300, 236)
f.text(150, 12, "SA/V falls as the body gets bigger", size=10.5, color=NAVY, bold=True)
for i, ((n, k, r), v) in enumerate(zip(it, sv)):
    y = 28 + i * 37
    f.text(10, y + 2, n, size=10.5, color=SLATE, anchor="start")
    w = 31 * math.log10(v)
    f.box(10, y + 9, w, 18, fill=MINT, stroke=TEAL, r=2)
    f.text(10 + w + 6, y + 18, "{:,.0f}".format(v), size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(150, 224, "sphere 3/r, cylinder 2/r (r in metres)", size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

**One feature, one group**

| Feature | Group |
|---|---|
| Choanocytes, ostia, osculum, spicules, gemmules | Porifera |
| Cnidoblasts / nematocysts, mesogloea, polyp and medusa | Coelenterata |
| Comb plates, colloblasts | Ctenophora |
| Flame cells, hooks and suckers, proglottids | Platyhelminthes |
| Pseudocoel, cuticle, renette cells, sexual dimorphism | Aschelminthes |
| Metameric segmentation, setae, parapodia, nephridia, clitellum | Annelida |
| Jointed legs, chitin, haemocoel, Malpighian tubules, tracheae | Arthropoda |
| Mantle, shell, radula, ctenidia, osphradium, organ of Bojanus | Mollusca |
| Water vascular system, tube feet, madreporite, Aristotle's lantern | Echinodermata |
| Notochord, dorsal hollow nerve cord, gill slits, post-anal tail | Chordata |
| Placoid scales, claspers | Chondrichthyes |
| Operculum, air bladder | Osteichthyes |
| Feathers, pneumatic bones, air sacs, syrinx | Aves |
| Hair, mammary glands, diaphragm, pinna | Mammalia |

**Common name → scientific name**

| Common name | Animal (group) |
|---|---|
| Venus' flower basket / bath sponge / fresh-water sponge | *Euplectella* / *Euspongia* / *Spongilla* (Porifera) |
| Portuguese man-of-war / sea fur / moon jelly | *Physalia* / *Obelia* / *Aurelia* (Coelenterata) |
| Sea anemone / sea fan / sea pen / red coral | *Metridium*, *Adamsia* / *Gorgonia* / *Pennatula* / *Corallium* |
| Liver fluke / pork tapeworm / dog tapeworm | *Fasciola* / *Taenia solium* / *Echinococcus* |
| Roundworm / pinworm / hookworm / filarial worm / guinea worm | *Ascaris* / *Enterobius* / *Ancylostoma* / *Wuchereria* / *Dracunculus* |
| Sea mouse / sandworm / earthworm / cattle leech | *Aphrodite* / *Nereis* / *Pheretima* / *Hirudinaria* |
| Prawn / crayfish / water flea / barnacle | *Palaemon* / *Astacus* / *Daphnia* / *Balanus* |
| Centipede / millipede / silverfish / king crab | *Scolopendra* / *Julus* / *Lepisma* / *Limulus* |
| Apple snail / slug / tusk shell / chiton | *Pila* / *Limax* / *Dentalium* / *Chiton* |
| Pearl oyster / shipworm / cuttlefish / squid / devil fish | *Pinctada* / *Teredo* / *Sepia* / *Loligo* / *Octopus* |
| Starfish / brittle star / sea urchin / sea cucumber / feather star | *Asterias* / *Ophiura* / *Echinus* / *Cucumaria* / *Antedon* |
| Acorn worm / sea squirt / lancelet | *Balanoglossus* / *Herdmania*, *Ascidia* / *Branchiostoma* |
| Lamprey / hagfish / dogfish / sawfish / electric ray / stingray | *Petromyzon* / *Myxine* / *Scoliodon* / *Pristis* / *Torpedo* / *Trygon* |
| Rohu / sea horse / flying fish / climbing perch | *Labeo rohita* / *Hippocampus* / *Exocoetus* / *Anabas* |
| Toad / tree frog / limbless amphibian | *Bufo* / *Hyla* / *Ichthyophis* |
| Garden lizard / wall lizard / turtle / cobra / gharial | *Calotes* / *Hemidactylus* / *Chelone* / *Naja* / *Gavialis* |
| Pigeon / ostrich / penguin / Danfe | *Columba* / *Struthio* / *Aptenodytes* / *Lophophorus impejanus* |
| Platypus / spiny anteater / kangaroo / flying fox / blue whale | *Ornithorhynchus* / *Tachyglossus* / *Macropus* / *Pteropus* / *Balaenoptera* |

**Larvae**

| Larva | Group |
|---|---|
| Amphiblastula | sponges (*Sycon*) |
| Planula | Coelenterata |
| Miracidium, sporocyst, redia, cercaria | liver fluke |
| Cysticercus (bladder worm) | *Taenia* |
| Trochophore | Polychaeta, Mollusca |
| Veliger | Mollusca |
| Nauplius | Crustacea |
| Bipinnaria / echinopluteus / auricularia | starfish / sea urchin / sea cucumber |
| Tornaria | *Balanoglossus* |
| Tadpole | ascidians, frogs |
| Ammocoete | lamprey |

## Chapter summary

- Animals are classified by **level of organisation**, **symmetry**, **germ layers**, **coelom** and **segmentation**: cellular → Porifera; tissue, radial, diploblastic → Coelenterata; acoelomate → Platyhelminthes; pseudocoelomate → Aschelminthes; schizocoelous protostomes → Annelida, Arthropoda, Mollusca; enterocoelous deuterostomes → Echinodermata, Hemichordata, Chordata.
- **Protozoa** are grouped by locomotion: pseudopodia (*Amoeba*, *Entamoeba*), flagella (*Euglena*, *Trypanosoma*, *Leishmania*), none (Sporozoa: *Plasmodium*), cilia (*Paramecium*, *Balantidium*).
- **Porifera**: ostia, osculum, canal system, choanocytes, spicules or spongin, gemmules; Calcarea, Hexactinellida (*Euplectella*), Demospongiae (*Euspongia*, *Spongilla*).
- **Coelenterata**: radial, diploblastic, coelenteron, **nematocysts**, polyp and medusa, metagenesis in *Obelia*; Hydrozoa, Scyphozoa, Anthozoa.
- **Platyhelminthes** (flame cells; *Fasciola*, *Taenia*) and **Aschelminthes** (pseudocoel, complete gut, separate sexes; *Ascaris*, *Wuchereria*, *Ancylostoma*, *Enterobius*).
- **Annelida**: metameres, setae/parapodia, closed circulation, nephridia; Polychaeta (*Nereis*), Oligochaeta (*Pheretima*), Hirudinea (*Hirudinaria*).
- **Arthropoda**, the largest phylum: jointed legs, chitin, haemocoel, open circulation; Crustacea (2 pairs of antennae, gills, green glands), Myriapoda, Insecta (3 pairs of legs, tracheae, Malpighian tubules), Arachnida (4 pairs of legs, book lungs, no antennae).
- **Mollusca**: mantle, shell, radula, ctenidia; seven classes from *Neopilina* to *Sepia*; **Echinodermata**: pentaradial adults, water vascular system, tube feet; Asteroidea to Crinoidea.
- **Chordata**: notochord, dorsal hollow nerve cord, gill slits, post-anal tail; Urochordata (larval notochord), Cephalochordata (*Branchiostoma*), Vertebrata — Cyclostomata, Chondrichthyes, Osteichthyes, Amphibia, Reptilia, Aves, Mammalia, each with its skin, heart, temperature and egg in the table.

## Practice questions

**Set A — Recall (30 questions)**

1. Choanocytes (collar cells) are characteristic of the phylum
   (a) Coelenterata (b) Porifera (c) Platyhelminthes (d) Ctenophora
2. Venus' flower basket is the common name of
   (a) *Euspongia* (b) *Spongilla* (c) *Euplectella* (d) *Hyalonema*
3. Nematocysts are found in
   (a) Coelenterata (b) Porifera (c) Ctenophora (d) Echinodermata
4. The Portuguese man-of-war is
   (a) *Aurelia* (b) *Adamsia* (c) *Pennatula* (d) *Physalia*
5. Alternation of a polyp generation with a medusa generation (metagenesis) is seen in
   (a) *Hydra* (b) *Obelia* (c) *Metridium* (d) *Pleurobrachia*
6. Flame cells are the excretory structures of
   (a) Mollusca (b) Annelida (c) Platyhelminthes (d) Arthropoda
7. The tapeworm whose scolex bears both hooks and suckers, and whose intermediate host is the pig, is
   (a) *Taenia solium* (b) *Taenia saginata* (c) *Echinococcus granulosus* (d) *Fasciola hepatica*
8. Elephantiasis is caused by
   (a) *Ancylostoma duodenale* (b) *Enterobius vermicularis* (c) *Ascaris lumbricoides* (d) *Wuchereria bancrofti*
9. A pseudocoelom is the body cavity of
   (a) Platyhelminthes (b) Aschelminthes (c) Annelida (d) Mollusca
10. Parapodia are the locomotory organs of
   (a) *Pheretima* (b) *Hirudinaria* (c) *Nereis* (d) *Tubifex*
11. Kala-azar, endemic in the Terai of Nepal, is caused by
   (a) *Leishmania donovani* (b) *Trypanosoma gambiense* (c) *Giardia intestinalis* (d) *Entamoeba histolytica*
12. The only ciliate known to parasitise man is
   (a) *Paramecium caudatum* (b) *Vorticella* (c) *Nyctotherus* (d) *Balantidium coli*
13. The largest phylum of the animal kingdom is
   (a) Mollusca (b) Arthropoda (c) Chordata (d) Annelida
14. Green glands are the excretory organs of
   (a) cockroach (b) scorpion (c) prawn (d) centipede
15. Book lungs are the respiratory organs of
   (a) scorpion (b) cockroach (c) prawn (d) millipede
16. Two pairs of legs on each trunk segment are found in
   (a) *Scolopendra* (b) *Periplaneta* (c) *Palaemon* (d) *Julus*
17. A radula is found in most members of
   (a) Echinodermata (b) Annelida (c) Mollusca (d) Arthropoda
18. The pearl oyster is
   (a) *Ostrea* (b) *Pinctada* (c) *Unio* (d) *Teredo*
19. The cuttlefish is
   (a) *Sepia* (b) *Loligo* (c) *Octopus* (d) *Nautilus*
20. A water vascular system with tube feet is the diagnostic feature of
   (a) Porifera (b) Coelenterata (c) Mollusca (d) Echinodermata
21. Aristotle's lantern is the chewing apparatus of
   (a) starfish (b) brittle star (c) sea urchin (d) sea cucumber
22. The feather star is
   (a) *Asterias* (b) *Antedon* (c) *Ophiura* (d) *Cucumaria*
23. Retrogressive metamorphosis is shown by
   (a) *Herdmania* (b) *Branchiostoma* (c) *Petromyzon* (d) *Balanoglossus*
24. Placoid scales are found in
   (a) *Labeo* (b) *Hippocampus* (c) *Catla* (d) *Scoliodon*
25. Among reptiles a four-chambered heart is found in
   (a) *Naja* (b) *Calotes* (c) *Crocodylus* (d) *Chelone*
26. Pneumatic bones and air sacs are features of
   (a) Reptilia (b) Aves (c) Mammalia (d) Amphibia
27. An egg-laying mammal is
   (a) *Ornithorhynchus* (b) *Macropus* (c) *Pteropus* (d) *Didelphis*
28. A muscular diaphragm separating the thorax from the abdomen is found only in
   (a) Aves (b) Reptilia (c) Amphibia (d) Mammalia
29. The Danfe, the national bird of Nepal, is
   (a) *Pavo cristatus* (b) *Columba livia* (c) *Lophophorus impejanus* (d) *Psittacula krameri*
30. The limbless amphibian among the following is
   (a) *Hyla* (b) *Ichthyophis* (c) *Salamandra* (d) *Bufo*

::: note Answers and explanations — Set A
**1.** (b) — collar cells with a flagellum line the spongocoel of sponges and drive the water current. Ctenophores have colloblasts, not choanocytes.
**2.** (c) — *Euplectella*, a glass sponge with six-rayed siliceous spicules; *Hyalonema* is the glass-rope sponge.
**3.** (a) — nematocysts in cnidoblasts are the diagnostic feature of Cnidaria; Ctenophora have adhesive colloblasts instead.
**4.** (d) — *Physalia* is a polymorphic floating hydrozoan colony; *Aurelia* is the moon jelly, *Adamsia* a sea anemone.
**5.** (b) — *Obelia* alternates an asexual colonial polyp with a sexual medusa. *Hydra* and *Metridium* have no medusa; *Pleurobrachia* is a ctenophore.
**6.** (c) — flame cells (protonephridia) of flatworms; Annelida have nephridia, Arthropoda Malpighian tubules or green glands, Mollusca kidneys.
**7.** (a) — *T. solium*, the pork tapeworm, has an armed scolex; *T. saginata* (beef) has suckers only.
**8.** (d) — the filarial worm *Wuchereria*, carried by *Culex*, blocks lymph vessels.
**9.** (b) — the roundworm cavity is not lined by mesoderm on the gut side: a pseudocoel. Flatworms are acoelomate.
**10.** (c) — *Nereis*, a polychaete, has paired lateral parapodia with many setae; earthworms have only setae, leeches suckers.
**11.** (a) — *Leishmania donovani*, a flagellate spread by the sandfly *Phlebotomus*. *Trypanosoma* causes sleeping sickness.
**12.** (d) — *Balantidium coli* causes balantidial dysentery; *Nyctotherus* lives in the frog's rectum.
**13.** (b) — arthropods make up more than two-thirds of all named animal species.
**14.** (c) — crustaceans excrete by antennal (green) glands; cockroach, scorpion and centipede have Malpighian tubules.
**15.** (a) — scorpions and spiders breathe by book lungs; insects and millipedes by tracheae, prawns by gills.
**16.** (d) — *Julus*, a millipede (Diplopoda), has two pairs per segment; *Scolopendra*, a centipede, has one.
**17.** (c) — the radula is the molluscan rasping tongue; bivalves lack it.
**18.** (b) — *Pinctada*; *Ostrea* is the edible oyster, *Teredo* the shipworm.
**19.** (a) — *Sepia*; *Loligo* is the squid, *Octopus* the devil fish.
**20.** (d) — the ambulacral system works the tube feet of echinoderms.
**21.** (c) — Aristotle's lantern is the five-jawed feeding apparatus of sea urchins (Echinoidea).
**22.** (b) — *Antedon* is a crinoid; *Asterias* starfish, *Ophiura* brittle star, *Cucumaria* sea cucumber.
**23.** (a) — the tadpole larva of *Herdmania* loses its tail, notochord and most of its nerve cord when it settles: a step backwards in organisation.
**24.** (d) — *Scoliodon*, a cartilaginous fish; the bony fishes have cycloid or ctenoid scales.
**25.** (c) — the crocodile's ventricle is fully divided; other reptiles have an incompletely divided ventricle.
**26.** (b) — hollow, air-filled bones and air sacs lighten birds and supply the lungs.
**27.** (a) — the platypus is a monotreme; *Macropus* and *Didelphis* are marsupials, *Pteropus* a placental bat.
**28.** (d) — only mammals have a muscular diaphragm.
**29.** (c) — *Lophophorus impejanus*, the Himalayan monal; *Pavo cristatus* is the peafowl.
**30.** (b) — *Ichthyophis* is a caecilian, a burrowing limbless amphibian.
:::

**Set B — Understanding (18 questions)**

1. Which of the following is a true fish?
   (a) jellyfish (b) silverfish (c) sea horse (d) cuttlefish
2. The silverfish (*Lepisma*) belongs to the class
   (a) Insecta (b) Osteichthyes (c) Crustacea (d) Arachnida
3. An enterocoelous coelom is found in
   (a) Annelida (b) Arthropoda (c) Mollusca (d) Echinodermata
4. In which pair of phyla does the blastopore become the anus?
   (a) Annelida and Arthropoda (b) Echinodermata and Chordata (c) Mollusca and Annelida (d) Platyhelminthes and Aschelminthes
5. True metameric segmentation is NOT found in
   (a) *Pheretima* (b) *Periplaneta* (c) *Taenia* (d) *Nereis*
6. Which of the following is NOT a fundamental character of chordates?
   (a) notochord (b) dorsal hollow nerve cord (c) pharyngeal gill slits (d) ventral solid double nerve cord
7. In Urochordata the notochord is present
   (a) only in the tail of the larva (b) from head to tail throughout life (c) as a vertebral column in the adult (d) as a stomochord in the proboscis
8. Which of the following is NOT a mollusc?
   (a) *Dentalium* (b) *Limulus* (c) *Chiton* (d) *Teredo*
9. The mesogloea of *Hydra* is
   (a) a cellular mesoderm (b) the body cavity (c) a non-cellular jelly between ectoderm and endoderm (d) a layer of spicules
10. The body cavity of a cockroach is called a haemocoel because it
   (a) is filled with blood from an open circulatory system (b) is lined by mesoderm on both sides (c) contains coelomic fluid but no blood (d) is absent, the body being solid
11. Among molluscs a closed circulatory system is found in
   (a) *Pila* (b) *Unio* (c) *Dentalium* (d) *Octopus*
12. The shelled (cleidoic) egg of reptiles and birds is an adaptation for
   (a) external fertilisation in water (b) development on land without free water (c) larval metamorphosis (d) faster hatching in ponds
13. Which pair of animals has neither a circulatory nor a respiratory system?
   (a) earthworm and leech (b) cockroach and prawn (c) *Hydra* and *Taenia* (d) frog and toad
14. Which group excretes mainly uric acid?
   (a) birds and reptiles (b) bony fishes and tadpoles (c) mammals and adult frogs (d) sharks and rays
15. The duck-billed platypus is placed among mammals because it
   (a) lays eggs (b) has a cloaca (c) has a beak (d) has hair and mammary glands
16. Which pair is correctly matched?
   (a) *Fasciola* — tapeworm (b) *Enterobius* — pinworm (c) *Taenia* — liver fluke (d) *Ascaris* — filarial worm
17. Sponges are said to be at the cellular level of organisation because their cells
   (a) live singly (b) form true tissues and organs (c) divide labour but form no true tissues (d) lack nuclei
18. Which feature separates Osteichthyes from Chondrichthyes?
   (a) an operculum covering the gills (b) paired fins (c) a two-chambered heart (d) jaws

::: note Answers and explanations — Set B
**1.** (c) — *Hippocampus* is a bony fish with gills, fins and an operculum; the others are a cnidarian, an insect and a mollusc.
**2.** (a) — *Lepisma* is a primitive wingless insect (three pairs of legs, one pair of antennae).
**3.** (d) — echinoderms (with hemichordates and chordates) form the coelom from gut pouches; the other three are schizocoelous.
**4.** (b) — they are deuterostomes; in annelids, arthropods and molluscs (protostomes) the blastopore becomes the mouth.
**5.** (c) — the proglottids of *Taenia* are budded off from the neck and do not repeat organs in a true metameric way: pseudometamerism.
**6.** (d) — a ventral, solid, double nerve cord is the non-chordate (annelid, arthropod) pattern.
**7.** (a) — "uro" = tail: the notochord lies in the larval tail and is lost at metamorphosis. (b) is Cephalochordata, (d) Hemichordata.
**8.** (b) — *Limulus*, the king crab, is an arthropod (Merostomata); the others are a tusk shell, a chiton and the shipworm.
**9.** (c) — Cnidaria are diploblastic; the mesogloea is jelly, not a germ layer.
**10.** (a) — arthropod blood leaves the vessels and bathes the organs in the body cavity; the true coelom is reduced.
**11.** (d) — cephalopods are active predators with a closed system and accessory branchial hearts.
**12.** (b) — the shell and the amnion keep the embryo in its own pond, so reptiles and birds can breed away from water.
**13.** (c) — cnidarians and flatworms exchange gases and wastes by diffusion through the body surface.
**14.** (a) — uric acid saves water (uricotely); fishes and tadpoles are ammonotelic, mammals and adult frogs ureotelic, sharks retain urea.
**15.** (d) — hair and milk glands define mammals; egg-laying and a cloaca are reptilian features it retains.
**16.** (b) — *Enterobius vermicularis* is the pinworm; *Fasciola* is a liver fluke, *Taenia* a tapeworm, *Ascaris* the roundworm.
**17.** (c) — sponge cells specialise (pinacocytes, choanocytes, amoebocytes) but never form true tissues.
**18.** (a) — bony fishes have an operculum (and air bladder); paired fins, a two-chambered heart and jaws are common to both.
:::

**Set C — Application (12 questions)**

1. An animal has jointed legs, two pairs of antennae, a cephalothorax covered by a carapace and breathes by gills. It belongs to
   (a) Insecta (b) Crustacea (c) Arachnida (d) Myriapoda
2. An animal has four pairs of walking legs, no antennae and breathes by book lungs. It belongs to
   (a) Insecta (b) Crustacea (c) Chilopoda (d) Arachnida
3. A specimen is radially symmetrical with tentacles bearing stinging cells round the only opening of its gut. It belongs to
   (a) Coelenterata (b) Porifera (c) Echinodermata (d) Ctenophora
4. A worm is cylindrical and unsegmented, with a complete gut, a body cavity not lined by mesoderm on the gut side, and separate sexes. It belongs to
   (a) Platyhelminthes (b) Annelida (c) Aschelminthes (d) Hirudinea
5. A student collects *Hydra*, *Fasciola*, *Ascaris*, *Nereis*, *Pila* and *Asterias*. How many of them are triploblastic and truly coelomate?
   (a) 3 (b) 2 (c) 4 (d) 5
6. Which of these animals would you expect to have a closed circulatory system?
   (a) cockroach (b) earthworm (c) *Pila* (d) prawn
7. A pond organism has a pellicle, a flagellum, an eyespot and chloroplasts, and feeds saprophytically in the dark. It is
   (a) *Paramecium* (b) *Amoeba* (c) *Plasmodium* (d) *Euglena*
8. A vertebrate has moist glandular skin without scales, a three-chambered heart, external fertilisation and a larva with gills. Its class is
   (a) Reptilia (b) Osteichthyes (c) Amphibia (d) Cyclostomata
9. An animal has dry skin with epidermal scales, a four-chambered heart, lays shelled eggs and is cold-blooded. It is
   (a) *Crocodylus* (b) *Columba* (c) *Ornithorhynchus* (d) *Naja*
10. A marine animal has a sessile adult enclosed in a tunic; its free-swimming larva has a notochord only in its tail. It belongs to
   (a) Cephalochordata (b) Urochordata (c) Hemichordata (d) Cyclostomata
11. A fish has a ventral mouth, five pairs of uncovered gill slits, placoid scales and claspers, and no air bladder. It is
   (a) *Labeo rohita* (b) *Hippocampus* (c) *Exocoetus* (d) *Scoliodon*
12. A spiny-skinned animal with tube feet, no head and a pentaradial body has a bipinnaria larva. It is
   (a) *Echinus* (b) *Holothuria* (c) *Asterias* (d) *Antedon*

::: note Answers and explanations — Set C
**1.** (b) — two pairs of antennae, carapace and gills mark a crustacean such as the prawn; insects have one pair of antennae, arachnids none.
**2.** (d) — four pairs of legs, no antennae and book lungs: a scorpion or spider.
**3.** (a) — radial symmetry, cnidoblasts and a blind-sac coelenteron: a cnidarian such as *Hydra*. Ctenophores lack stinging cells.
**4.** (c) — a pseudocoel, complete gut and separate sexes describe a nematode such as *Ascaris*.
**5.** (a) — *Nereis* (annelid), *Pila* (mollusc) and *Asterias* (echinoderm). *Hydra* is diploblastic, *Fasciola* acoelomate, *Ascaris* pseudocoelomate.
**6.** (b) — the earthworm's blood stays in vessels (closed system); cockroach, *Pila* and prawn have open systems.
**7.** (d) — *Euglena*, a flagellate that photosynthesises in light and absorbs organic food in the dark.
**8.** (c) — moist naked skin, three chambers and an aquatic gilled tadpole mark an amphibian.
**9.** (a) — the crocodile is the reptile with a four-chambered heart; *Columba* is warm-blooded, *Naja* has three chambers, *Ornithorhynchus* has hair.
**10.** (b) — a tunic and a larval tail notochord are the marks of a tunicate such as *Herdmania*.
**11.** (d) — all are features of a cartilaginous fish; *Scoliodon* is the dogfish. The other three are bony fishes with an operculum.
**12.** (c) — the bipinnaria is the starfish larva; *Echinus* has an echinopluteus, *Holothuria* an auricularia, *Antedon* a doliolaria.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe the diagnostic features of the phyla Porifera, Cnidaria, Platyhelminthes and Aschelminthes, with examples. <span class="marks">[10]</span>
2. Describe the features of the phyla Annelida, Arthropoda, Mollusca and Echinodermata, with examples. <span class="marks">[10]</span>
3. Classify the phylum Chordata up to classes, giving the main features and examples of each. <span class="marks">[10]</span>

```photogrid label="2.H" cols="5" ratio="1.1" caption="Animal diversity in the laboratory and in Nepal. (a) Sycon, a sponge. (b) Hydra, a cnidarian. (c) Planaria, a flatworm. (d) Earthworm, an annelid. (e) Rohu, a bony fish common in Nepali ponds."
@ photo id="bio11/sycon-photo" cap="(a) Sycon"
fit 1.1
focus 0.5 0.5
@ photo id="bio11/hydra" cap="(b) Hydra"
fit 1.1
focus 0.5 0.5
@ photo id="bio11/planaria" cap="(c) Planaria"
fit 1.1
focus 0.5 0.5
@ photo id="bio11/earthworm-ext" cap="(d) Earthworm"
fit 1.1
focus 0.5 0.5
@ photo id="bio11/rohu" cap="(e) Rohu"
fit 1.1
focus 0.5 0.5
```

### Model answer D1: Porifera to Aschelminthes (10 marks)

**Introduction.** Animals are multicellular, heterotrophic eukaryotes without cell walls. The simplest non-chordate phyla show how the body plan becomes more complex from cell level to organ level.

1. **Porifera (sponges).** Body with many pores (**ostia**), a large opening (**osculum**) and a central cavity (spongocoel). **Collar cells (choanocytes)** create the water current. Cellular grade of organisation, skeleton of spicules or spongin. Mostly marine. *Sycon, Spongilla* (fresh water), *Euspongia* (bath sponge).
2. **Cnidaria (Coelenterata).** Radial symmetry, tissue grade, **diploblastic** with a gastro-vascular cavity and a single opening. Stinging cells (**cnidoblasts**) hold nematocysts. Polyp and medusa forms. *Hydra, Obelia, Aurelia* (jellyfish), *Physalia*, sea anemone and corals.
3. **Platyhelminthes (flatworms).** Bilateral symmetry, dorso-ventrally flattened, **triploblastic and acoelomate**, organ grade, incomplete gut or none, **flame cells** for excretion. Many are parasites. *Planaria* (free-living), *Fasciola hepatica* (liver fluke), *Taenia solium* (pork tapeworm).
4. **Aschelminthes (Nematoda).** Round, unsegmented, **pseudocoelomate**, complete alimentary canal, separate sexes, cuticle outside. *Ascaris lumbricoides*, *Ancylostoma* (hookworm), *Wuchereria bancrofti* (filaria).

| Phylum | Symmetry | Germ layers | Body cavity | Special feature |
|---|---|---|---|---|
| Porifera | Asymmetric or radial | None (cellular) | Spongocoel | Choanocytes |
| Cnidaria | Radial | Two | Gastro-vascular | Cnidoblasts |
| Platyhelminthes | Bilateral | Three | Acoelomate | Flame cells |
| Aschelminthes | Bilateral | Three | Pseudocoelomate | Cuticle, complete gut |

**Importance.** Bath sponges and coral reefs are useful, while the liver fluke, tapeworm, hookworm and *Ascaris* cause disease in Nepali villages where sanitation is poor.

**Conclusion.** From sponges to roundworms there is a trend from cellular to organ-system organisation, from radial to bilateral symmetry and from no gut to a complete gut.

### Model answer D2: Annelida, Arthropoda, Mollusca and Echinodermata (10 marks)

**Introduction.** These four phyla are **coelomate** (or haemocoelic) and have complete digestive systems and well-developed organ systems.

1. **Annelida.** **Metamerically segmented** body, true coelom, closed circulation, ventral nerve cord, **nephridia** for excretion, setae for movement. *Pheretima* (earthworm), *Nereis* (sandworm), *Hirudinaria* (leech).
2. **Arthropoda.** The largest phylum. **Jointed appendages**, chitinous exoskeleton, moulting (ecdysis), **haemocoel** with open circulation, compound eyes. Classes: Insecta (*Periplaneta*, honeybee), Crustacea (prawn, crab), Arachnida (spider, scorpion), Myriapoda (centipede).
3. **Mollusca.** Soft unsegmented body in a **mantle** that often secretes a calcareous shell, a muscular **foot**, a **radula** for scraping food, open circulation. *Pila* (apple snail), *Unio* (mussel), *Octopus*, *Sepia*.
4. **Echinodermata.** Spiny skin, **pentamerous radial symmetry** in the adult (bilateral larva), **water vascular system** with tube feet, entirely marine, no head. *Asterias* (starfish), sea urchin, sea cucumber, brittle star.

| Phylum | Symmetry | Skeleton | Locomotion | Example |
|---|---|---|---|---|
| Annelida | Bilateral, segmented | Hydrostatic | Setae, muscles | Earthworm |
| Arthropoda | Bilateral, segmented | Chitin | Jointed legs, wings | Cockroach |
| Mollusca | Bilateral | Shell | Foot | Pila |
| Echinodermata | Radial (adult) | Calcareous ossicles | Tube feet | Starfish |

**Importance.** Earthworms improve soil (vermicompost), honeybees and silkworms give honey and silk (important in Nepal), insects such as *Anopheles* spread malaria, and pearl oysters give pearls.

**Conclusion.** Annelids introduced segmentation, arthropods added jointed limbs, molluscs the shell and echinoderms the water vascular system.

### Model answer D3: Classification of Chordata (10 marks)

**Introduction.** Chordates have a **notochord**, a **dorsal hollow nerve cord**, **pharyngeal gill slits** and a post-anal tail at some stage of life. The phylum has two groups: **Protochordata** (Urochordata, Cephalochordata) and **Vertebrata**.

**Protochordata.** *Herdmania* (Urochordata, notochord only in the larval tail) and *Branchiostoma* (Cephalochordata, notochord all through life).

**Vertebrata** (backbone replaces the notochord, brain in a skull).

1. **Agnatha (cyclostomes):** jawless, round sucking mouth, no paired fins. *Petromyzon* (lamprey), *Myxine*.
2. **Pisces:** fins, gills, scales, two-chambered heart. Chondrichthyes (cartilage; *Scoliodon*) and Osteichthyes (bone; *Rohu, Labeo*).
3. **Amphibia:** moist skin, tadpole with gills, adult with lungs, three-chambered heart. *Rana tigrina*, *Bufo*, *Salamandra*.
4. **Reptilia:** dry scaly skin, lungs, shelled eggs on land, mostly three-chambered heart (crocodile four). *Lizard, snake, tortoise, gharial*.
5. **Aves:** feathers, wings, beak, hollow bones, **four-chambered heart**, warm-blooded. *Pigeon, vulture, Himalayan monal* (Danphe).
6. **Mammalia:** hair, **mammary glands**, diaphragm, four-chambered heart, warm-blooded, external ear (pinna). *Man, tiger, rhino, bat, whale, platypus*.

| Class | Skin cover | Respiration | Heart | Body temperature |
|---|---|---|---|---|
| Pisces | Scales | Gills | 2 chambers | Cold-blooded |
| Amphibia | Moist skin | Skin, lungs | 3 chambers | Cold-blooded |
| Reptilia | Dry scales | Lungs | 3 (4 in crocodile) | Cold-blooded |
| Aves | Feathers | Lungs and air sacs | 4 chambers | Warm-blooded |
| Mammalia | Hair | Lungs | 4 chambers | Warm-blooded |

**Conclusion.** Chordates show a progress from gills to lungs and from a two- to a four-chambered heart, which is the basis of adaptation to land life.

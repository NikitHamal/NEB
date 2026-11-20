---
subject: Science and Technology
grade: 10
unit: 2
title: Classification of Living Beings
hours: 0
area: Science and Technology
---

Nepal alone has more than 6,000 kinds of flowering plants, about 880 kinds of birds and thousands of insects. The whole Earth has millions of kinds of living things. To study such variety, scientists sort living things into groups according to their likeness. This sorting is called classification. In this unit you learn why we classify, how every organism gets a two-part scientific name, and the five great kingdoms into which all living things are placed.

::: key What the SEE paper expects from this unit
Questions are usually: define taxonomy / binomial nomenclature (2 marks); differences between prokaryotic and eukaryotic cells or between plant and animal kingdoms (2 or 4 marks); give examples of each kingdom (1 mark); the characteristics of one kingdom (4 marks). Learn the table of five kingdoms and the examples.
:::

## 2.1 Taxonomy and classification

### Why classify?

**Classification** is the arrangement of living things into groups and subgroups on the basis of their similarities and differences. We classify because it:

- makes the study of millions of organisms easy;
- shows how organisms are related to one another;
- gives each organism a name known to scientists everywhere;
- helps us to identify an unknown organism;
- helps in the study of evolution.

::: definition Taxonomy
**Taxonomy** is the branch of biology that deals with the identification, naming and classification of organisms.
:::

### Early classification

The Greek scientist **Aristotle** (384–322 BC) first grouped organisms as plants and animals, and plants as herbs, shrubs and trees. **Carolus Linnaeus** (1707–1778), a Swedish botanist, is called the **father of taxonomy**. He introduced the system of naming organisms with two names and arranged them in ranks. **R. H. Whittaker** (1969) proposed the five-kingdom system that this unit follows.

### Taxonomic hierarchy

The ranks in classification, from the largest group to the smallest, are called the **taxonomic hierarchy**. Each step down holds fewer organisms that are more alike.

::: memory Order of ranks
**K**ing **P**hilip **C**ame **O**ver **F**or **G**ood **S**oup: Kingdom → Phylum (Division in plants) → Class → Order → Family → Genus → Species.
:::

The **species** is the basic unit of classification. A species is a group of organisms that look alike, can breed with each other and produce fertile offspring.

```figure caption="Taxonomic hierarchy of the human being. The number of organisms in each rank decreases from top to bottom, but their similarity increases."
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.6,3.3))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,7.4)
ranks = [("Kingdom","Animalia"),("Phylum","Chordata"),("Class","Mammalia"),("Order","Primates"),("Family","Hominidae"),("Genus","Homo"),("Species","Homo sapiens")]
for i,(r,n) in enumerate(ranks):
    y = 7.0-i*1.0
    w = 4.6-i*0.5
    ax.add_patch(Polygon([(2.8-w/2+0.0,y-0.45),(2.8+w/2,y-0.45),(2.8+w/2,y+0.45),(2.8-w/2,y+0.45)],fc="#eaf1ff",ec=ACCENT,lw=1))
    ax.text(2.8,y,r,ha='center',va='center',fontsize=8,color=INK,fontweight='bold')
    ax.text(5.6,y,n,ha='left',va='center',fontsize=8.5,color=INK,style='italic')
ax.annotate("",xy=(9.6,0.4),xytext=(9.6,7.0),arrowprops=dict(arrowstyle="->",color=MUTED))
ax.text(9.0,3.7,"fewer\norganisms,\nmore alike",fontsize=7,color=MUTED,ha='center',rotation=0)
```

### Binomial nomenclature

Common names change from place to place. A mango is *aamba* in Nepali, *mango* in English and *aam* in Hindi, and the same common name can mean different plants in different places. To avoid confusion, Linnaeus gave each organism a two-word **scientific name**.

::: definition Binomial nomenclature
**Binomial nomenclature** is the system of naming an organism with two words: the first is the **genus** name and the second is the **species** name.
:::

Rules for writing a scientific name:

1. The name is in Latin and is written in *italics* (when handwritten, each word is underlined separately).
2. The **genus** name begins with a **capital** letter; the **species** name begins with a **small** letter.
3. The first word is the genus and the second the species: *Homo sapiens*, not *sapiens Homo*.

| Organism | Scientific name |
|---|---|
| Human being | *Homo sapiens* |
| Mango | *Mangifera indica* |
| Rice | *Oryza sativa* |
| Pea | *Pisum sativum* |
| Cat | *Felis catus* |
| Dog | *Canis familiaris* |
| Tiger | *Panthera tigris* |
| Rhododendron (national flower of Nepal) | *Rhododendron arboreum* |

::: example Worked example 2.1 (reading a scientific name)
**Problem.** For *Panthera tigris* (tiger) and *Panthera leo* (lion), state the genus and species of each and say how closely they are related.

**Solution.** The genus of both is *Panthera* (capital P); the species are *tigris* and *leo* (small letters). They share the same genus, so they are closely related members of one group of big cats, but they are different species because they do not normally breed in nature to produce fertile young.
:::

::: caution Common mistake
Do not write the scientific name as *homo Sapiens* or *Homo Sapiens*. Only the genus name takes the capital letter. Also, the whole name must be in italics or underlined.
:::

## 2.2 Five kingdoms

Earlier, all organisms were placed in two kingdoms, plants and animals. This did not suit bacteria, fungi or organisms like *Euglena* (which has green colour but also moves). In 1969 R. H. Whittaker therefore proposed **five kingdoms**, based on four main points:

1. type of cell: prokaryotic or eukaryotic;
2. number of cells: unicellular or multicellular;
3. mode of nutrition: autotrophic or heterotrophic;
4. body organisation and way of reproduction.

### Prokaryotic and eukaryotic cells

| Prokaryotic cell | Eukaryotic cell |
|---|---|
| No true nucleus; genetic material lies free in the cytoplasm | Has a true nucleus bounded by a nuclear membrane |
| Membrane-bound organelles absent | Membrane-bound organelles (mitochondria etc.) present |
| Very small (1–10 μm) | Larger (10–100 μm) |
| Found in bacteria | Found in protists, fungi, plants and animals |

### The five kingdoms

The five kingdoms are **Monera, Protista, Fungi, Plantae and Animalia**.

```figure caption="The five-kingdom classification (Whittaker). Monera is prokaryotic; the other four kingdoms are eukaryotic."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.2))
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,7)
def box(x,y,w,h,t,fc="#eaf1ff",fs=8):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.04",fc=fc,ec=ACCENT,lw=1.1))
    ax.text(x,y,t,ha='center',va='center',fontsize=fs,color=INK)
box(5,6.3,4.4,0.8,"Living organisms",fc="#dbe8ff",fs=9)
box(1.8,4.5,3.2,0.9,"Prokaryotes\n(no true nucleus)")
box(7.2,4.5,3.8,0.9,"Eukaryotes\n(true nucleus)")
ax.plot([5,5],[5.9,5.4],color=INK,lw=1); ax.plot([1.8,7.2],[5.4,5.4],color=INK,lw=1)
ax.plot([1.8,1.8],[5.4,4.95],color=INK,lw=1); ax.plot([7.2,7.2],[5.4,4.95],color=INK,lw=1)
box(1.8,2.4,2.8,1.0,"Kingdom\nMONERA\nbacteria",fs=7.5)
xs=[4.3,6.3,8.3]
ax.plot([7.2,7.2],[4.05,3.6],color=INK,lw=1); ax.plot([4.8,9.2],[3.6,3.6],color=INK,lw=1)
for x,t in zip([4.8,6.45,8.1,9.4],["PROTISTA\namoeba","FUNGI\nyeast","PLANTAE\nmango","ANIMALIA\ncow"]):
    pass
names=["PROTISTA\namoeba","FUNGI\nmushroom","PLANTAE\nmango","ANIMALIA\ncow"]
px=[3.9,5.6,7.3,9.0]
ax.plot([3.9,9.0],[3.6,3.6],color=INK,lw=1)
ax.plot([7.2,7.2],[4.05,3.6],color=INK,lw=1)
for x,t in zip(px,names):
    ax.plot([x,x],[3.6,3.15],color=INK,lw=1)
    box(x,2.6,1.6,1.0,t,fs=6.8)
ax.plot([1.8,1.8],[4.05,2.9],color=INK,lw=1)
```

| Kingdom | Cell type | Body | Nutrition | Examples |
|---|---|---|---|---|
| Monera | Prokaryotic | Unicellular | Autotrophic or heterotrophic | Bacteria, cyanobacteria (*Nostoc*) |
| Protista | Eukaryotic | Mostly unicellular | Autotrophic or heterotrophic | *Amoeba*, *Paramecium*, *Euglena* |
| Fungi | Eukaryotic | Mostly multicellular (yeast is unicellular) | Heterotrophic (absorptive) | Yeast, mushroom, *Rhizopus*, *Penicillium* |
| Plantae | Eukaryotic, cell wall of cellulose | Multicellular | Autotrophic (photosynthesis) | Moss, fern, pine, mango, rice |
| Animalia | Eukaryotic, no cell wall | Multicellular | Heterotrophic (ingestion) | Hydra, earthworm, fish, human |

## 2.3 Characteristics of Monera, Protista, Fungi, Plantae and Animalia

### Kingdom Monera

Monera includes the simplest and oldest living things, the **bacteria** and the **blue-green algae (cyanobacteria)**.

- Microscopic, **unicellular**, **prokaryotic**: the DNA lies free in the cytoplasm without a nuclear membrane.
- The cell has a cell wall (of peptidoglycan in bacteria), a cell membrane, cytoplasm and ribosomes. Mitochondria and chloroplasts are absent.
- Nutrition may be **autotrophic** (cyanobacteria carry out photosynthesis) or **heterotrophic** (most bacteria absorb food from dead matter or living hosts).
- Reproduce mostly by **binary fission**: one cell divides into two. They can multiply very fast, as quickly as once every 20 minutes in good conditions.
- Found everywhere: soil, water, air, inside our bodies.

Bacteria are classified by shape into **cocci** (spherical), **bacilli** (rod-shaped), **spirilla** (spiral) and **vibrios** (comma-shaped).

```photo id="sci10/ecoli" caption="Bacteria seen under a scanning electron microscope: these are rod-shaped bacilli (Escherichia coli). Cocci are round and spirilla are spiral." width="70"
scale 0.05 0.04 0.2 "2 μm"
```

**Importance.** *Lactobacillus* turns milk into curd; *Rhizobium* fixes nitrogen in the root nodules of legumes; bacteria decompose dead bodies. Harmful bacteria cause cholera (*Vibrio cholerae*), typhoid, tuberculosis and tetanus.

### Kingdom Protista

- Mostly **unicellular**, **eukaryotic** organisms with a true nucleus and organelles.
- Most live in water or moist places.
- Nutrition: **autotrophic** (*Euglena*, diatoms), **heterotrophic** (*Amoeba*, *Paramecium*) or both (*Euglena*).
- Locomotion by pseudopodia (*Amoeba*), cilia (*Paramecium*) or flagella (*Euglena*).
- Reproduction mainly by binary fission; sexual reproduction (conjugation) also occurs in some.
- Some are harmful: *Plasmodium* causes malaria, *Entamoeba histolytica* causes amoebic dysentery, *Giardia* causes giardiasis.

Protista is often called the "kingdom of leftovers", because it contains eukaryotes that are neither plants, animals nor fungi.

```photo id="sci10/paramecium" caption="Paramecium, a ciliate protist, seen through a microscope. It swims with the help of the cilia that cover its body." width="70"
```

| Protist | Locomotion | Nutrition |
|---|---|---|
| *Amoeba* | Pseudopodia | Heterotrophic |
| *Paramecium* | Cilia | Heterotrophic |
| *Euglena* | Flagellum | Autotrophic and heterotrophic |
| *Plasmodium* | None (parasite) | Heterotrophic |

```photo id="sci10/euglena" caption="Euglena and other pond-water protists under the microscope. Euglena has a whip-like flagellum for swimming and chloroplasts for photosynthesis." width="70"
```

```photo id="sci10/amoeba" caption="Amoeba, a protist, seen through a microscope. It moves by extending temporary false feet (pseudopodia)." width="70"
```

### Kingdom Fungi

- Mostly **multicellular** (yeast is unicellular), **eukaryotic**.
- The body is made of thread-like **hyphae**, which together form a **mycelium**.
- The cell wall is made of **chitin** (not cellulose).
- **No chlorophyll**, so no photosynthesis. Fungi are **heterotrophic**: **saprophytes** feed on dead matter (mushroom, bread mould), **parasites** on living hosts (the rust fungus on wheat).
- They secrete enzymes outside the body to digest food and then absorb the digested food (**absorptive nutrition**).
- Reproduce by **spores**, by budding (yeast) and by fragmentation.
- Store food as glycogen, as animals do.

**Importance.** Yeast is used in making bread and alcohol; *Penicillium* gives the antibiotic penicillin; some mushrooms are food (*Agaricus*, the button mushroom); other fungi cause athlete's foot, ringworm and food spoilage. Fungi, along with bacteria, are **decomposers**.

```photo id="sci10/penicillium" caption="Penicillium growing on an orange: the green powder is the mass of spores. Penicillium is the fungus that gave us the antibiotic penicillin." width="56"
```

```photo id="sci10/mushroom" caption="A mushroom (fly agaric), the fruiting body of a fungus. The cap sits on a stalk and the body of the fungus lies in the soil." width="70"
```

### Kingdom Plantae (Algae, Bryophyta and Tracheophyta)

- **Multicellular**, **eukaryotic** organisms with a rigid **cell wall made of cellulose**.
- Contain **chlorophyll** inside plastids (chloroplasts) and prepare their own food by **photosynthesis** (**autotrophic** producers).
- Reserve food is stored mainly as **starch**.
- In the official CDC Grade 10 curriculum, **Kingdom Plantae** is classified into **three main divisions**: **Algae**, **Bryophyta** and **Tracheophyta** (vascular plants), and Division **Tracheophyta** is further divided into **three sub-divisions**: **Pteridophyta**, **Gymnosperms** and **Angiosperms**.

| Division / Sub-division | Key identifying characteristics | Examples |
|---|---|---|
| **1. Division: Algae** | Thalloid plant body (not differentiated into root, stem and leaf); no vascular tissue (xylem/phloem); mostly aquatic (freshwater or marine); unicellular (*Chlamydomonas*), colonial (*Volvox*) or filamentous (*Spirogyra*, *Ulothrix*); cell wall of cellulose; reproduce asexually (fragmentation/spores) and sexually. | *Spirogyra*, *Ulothrix*, *Volvox*, *Chlamydomonas*, *Fucus* |
| **2. Division: Bryophyta** | Called **"amphibians of the plant kingdom"** because they grow on moist shady land/walls but require water for fertilisation; plant body is thalloid (*Marchantia*, *Riccia*) or differentiated into stem-like and leaf-like structures with unicellular/multicellular **rhizoids** instead of true roots (*Funaria*/moss); **non-vascular** (xylem and phloem absent); show distinct **alternation of generations** where the haploid **gametophyte** is dominant and the diploid **sporophyte** depends on it. | Moss (*Funaria*), Liverwort (*Marchantia*, *Riccia*) |
| **3. Division: Tracheophyta** | **Vascular plants** possessing well-developed **xylem** (for water conduction) and **phloem** (for food translocation), with true roots, stems and leaves; dominant diploid **sporophyte** generation. Divided into three sub-divisions below: | Ferns, Pine, Mustard, Paddy |
| **3a. Sub-division: Pteridophyta** | Seedless vascular plants (**vascular cryptogams**) growing in cool, damp, shady habitats; plant body has true roots, an underground rhizome (stem) and feather-like compound leaves (**fronds**); underside of mature leaves bears brown spore-producing clusters called **sori**; spores germinate into a heart-shaped gametophyte (**prothallus**); no flowers, fruits or seeds. | Fern (*Dryopteris*, *Pteris*), Horsetail (*Equisetum*), Club moss (*Lycopodium*, *Selaginella*) |
| **3b. Sub-division: Gymnosperms** | **Naked-seeded vascular plants** (*gymnos* = naked, *sperma* = seed) in which ovules and seeds are **not enclosed inside a fruit** (no ovary); bear unisexual male and female **cones** instead of true flowers; perennial woody trees or shrubs with needle-like or scale-like leaves and xerophytic adaptations; pollination occurs by wind (**anemophily**). | Pine (*Pinus*/Salla), *Cycas*, Fir (*Abies*), Juniper (*Juniperus*), *Thuja* |
| **3c. Sub-division: Angiosperms** | **Flowering vascular plants** (*angio* = enclosed, *sperma* = seed) with well-developed flowers containing ovary, style and stigma; ovules develop into **seeds enclosed inside a fruit**; show **double fertilisation**; divided into two classes: **Monocotyledonae** and **Dicotyledonae**. | Rice, Maize, Banana, Mango, Mustard, Pea, Rose |

Angiosperms are further divided into two classes — **Monocotyledonae (monocots)** and **Dicotyledonae (dicots)**:

```photo id="sci10/hibiscus" caption="Flower of a hibiscus plant. Angiosperms bear flowers, and their seeds are enclosed in fruits." width="56"
```

| Monocotyledon | Dicotyledon |
|---|---|
| One cotyledon in the seed | Two cotyledons |
| Parallel venation | Reticulate (net) venation |
| Fibrous roots | Tap root |
| Flower parts in threes | Flower parts in fours or fives |

```photo id="sci10/moss" caption="Moss with its spore capsules (sporophytes) on thin stalks. Mosses are bryophytes: small plants of moist places that have no true roots." width="70"
```

```photo id="sci10/fern-sori" caption="Underside of a fern frond, showing the brown clusters of spore-producing sori. Ferns reproduce by spores, not seeds." width="70"
```

### Kingdom Animalia

- **Multicellular**, **eukaryotic**, cells without cell wall.
- **Heterotrophic**: they take food in (**ingestion**) and digest it inside the body.
- Most can **move** from place to place at some stage of life.
- Have nervous system and sense organs (except in the simplest ones), so they respond quickly to stimuli.
- Reproduce mostly sexually; store food as glycogen and fat.

Animals are classified into **nine major phyla**: the first eight are **invertebrates (non-chordates)** lacking a vertebral column, and the ninth is **Phylum Chordata** (which includes **Sub-phylum Vertebrata**).

| Phylum | Body organisation, symmetry & key diagnostic features | Examples |
|---|---|---|
| **1. Porifera** (Pore-bearing) | **Cellular level** of organisation (no tissues or organs); diploblastic, asymmetrical; sessile (attached to rocks); body perforated by numerous minute pores called **ostia** (water enters) and a single large opening at the top called **osculum** (water leaves) forming a **canal system**; internal cavity (**spongocoel**) lined by flagellated **choanocytes (collar cells)** for intracellular digestion; skeleton of calcareous/siliceous **spicules** or **spongin** fibres; hermaphrodite. | *Sycon*, *Spongilla* (freshwater sponge), *Euspongia* (bath sponge) |
| **2. Coelenterata (Cnidaria)** | **Tissue level** of organisation; **diploblastic** and **radially symmetrical**; hollow central gastrovascular cavity (**coelenteron**) with a single opening (mouth/hypostome) surrounded by **tentacles**; tentacles bear stinging cells called **cnidoblasts (nematocysts)** for offence, defence and food capture; show **polyp** (sessile, e.g. *Hydra*) and **medusa** (free-swimming, e.g. Jellyfish) forms. | *Hydra*, Jellyfish (*Aurelia*), Sea anemone, Coral |
| **3. Platyhelminthes** (Flatworms) | **Organ-system level**, **triploblastic**, **bilaterally symmetrical** and **acoelomate** (no body cavity); body dorsoventrally flattened like a ribbon or leaf; parasitic forms possess **hooks and suckers** for attachment; digestive tract incomplete (mouth present, anus absent) or absent in tapeworms; excretion by **flame cells (protonephridia)**; mostly **hermaphrodite (bisexual)**. | Liver fluke (*Fasciola hepatica*), Tapeworm (*Taenia solium*), *Planaria* |
| **4. Nemathelminthes / Aschelminthes (Nematoda)** | **Roundworms**: cylindrical, unsegmented body tapering at both ends; **triploblastic**, **bilaterally symmetrical** and **pseudocoelomate** (false body cavity); **complete digestive tract** with distinct mouth and anus; body covered by a tough protective **cuticle**; **unisexual (dioecious)** with sexual dimorphism (female longer than male); mostly endoparasites. | Roundworm (*Ascaris lumbricoides*), Hookworm (*Ancylostoma*), Pinworm (*Enterobius*), Filarial worm (*Wuchereria*) |
| **5. Annelida** (Segmented worms) | Elongated cylindrical body divided into ring-like **metameric segments (annuli)**; **triploblastic**, **bilaterally symmetrical** and **true coelomate**; locomotion by chitinous bristles (**setae** in earthworm), **parapodia** (in *Nereis*) or suckers (in leech); **closed blood circulatory system** with haemoglobin dissolved in plasma; excretion by coiled **nephridia**; respiration through moist skin (cuticle); hermaphrodite or unisexual. | Earthworm (*Pheretima*), Leech (*Hirudinaria*), Sandworm (*Nereis*) |
| **6. Arthropoda** (Jointed-legged) | **Largest phylum** in Animalia; body covered by a hard **chitinous exoskeleton** (shed periodically by **moulting/ecdysis**) and divided into **head, thorax and abdomen** (or **cephalothorax and abdomen** in crustaceans/arachnids); **jointed appendages**; **open circulatory system** with blood-filled body cavity (**haemocoel**); compound eyes and antennae; respiration by **trachea**, **gills** or **book lungs**; excretion by **Malpighian tubules** or green glands; unisexual. | Honey bee, Butterfly, Cockroach, Mosquito, Spider, Scorpion, Crab, Prawn, Centipede, Millipede |
| **7. Mollusca** (Soft-bodied) | Soft, unsegmented body usually protected by a hard **calcareous ($CaCO_3$) shell**; body divisible into **head** (with tentacles and eyes), **visceral mass**, **muscular foot** (for locomotion) and a soft fold of skin called the **mantle** (which secretes the shell); rasping organ **radula** in the mouth; open blood system (except octopus/squid); respiration by **gills (ctenidia)** or pulmonary sac; unisexual or hermaphrodite. | Snail (*Pila*, garden snail), Octopus, Cuttlefish (*Sepia*), Slug (*Limax*), Freshwater mussel (*Unio*) |
| **8. Echinodermata** (Spiny-skinned) | **Exclusively marine** animals with spiny skin formed by calcareous ossicles/plates; **triploblastic** and **coelomate**; **radially symmetrical** (pentamerous) in adults and bilaterally symmetrical in larvae; possess a unique **water vascular (ambulacral) system** with **tube feet (podia)** for locomotion, food capture and respiration; no distinct head; high power of **regeneration**; unisexual. | Starfish (*Asterias*), Sea urchin (*Echinus*), Sea cucumber (*Holothuria*), Brittle star |
| **9. Chordata** | Possess four fundamental chordate characters at some stage of life: (i) rod-like supporting **notochord**, (ii) **dorsal tubular nerve cord**, (iii) **pharyngeal gill slits**, and (iv) **post-anal tail**; closed circulatory system with a ventral heart. In **Sub-phylum Vertebrata**, the embryonic notochord is replaced by a bony or cartilaginous **vertebral column (backbone)**. | Fish, Frog, Lizard, Bird, Human |

```photo id="sci10/earthworm" caption="An earthworm (phylum Annelida): the body is divided into many ring-like segments." width="60"
```

```photo id="sci10/cockroach" caption="A cockroach (phylum Arthropoda): jointed legs, three pairs, and a hard outer skeleton." width="60"
```

**Sub-phylum Vertebrata (Craniata)** is divided into **five classes**:

| Class | Body covering & limbs | Respiration | Heart chambers & thermal regulation | Reproduction & examples |
|---|---|---|---|---|
| **1. Pisces** (Fishes) | Streamlined body covered with waterproof **scales**; paired and unpaired **fins** for swimming; swim bladder (air sac) in bony fishes. | **Gills** (covered by operculum in bony fishes) | **2-chambered heart** (1 auricle, 1 ventricle); **cold-blooded (poikilothermic)**. | Oviparous; external fertilisation. Examples: *Rohu* (*Labeo*), Shark, Sea horse (*Hippocampus*), Catla |
| **2. Amphibia** | Smooth, **moist glandular skin** without scales; body divided into head and trunk; two pairs of pentadactyl limbs. | **Gills** in aquatic tadpole larva; **lungs and moist skin** (cutaneous) in adults | **3-chambered heart** (2 auricles, 1 ventricle); **cold-blooded (poikilothermic)**. | Oviparous; external fertilisation in water ("amphibians of Animalia"). Examples: Frog (*Rana tigrina*), Toad (*Bufo*), Salamander, Tree frog (*Hyla*) |
| **3. Reptilia** | Dry, cornified skin covered with **horny epidermal scales** or scutes; crawl on land with two pairs of limbs (absent in snakes). | **Lungs** throughout life | **3-chambered heart** (2 auricles, incompletely divided ventricle; **4-chambered in crocodile**); **cold-blooded (poikilothermic)**. | Oviparous; internal fertilisation; leathery-shelled eggs laid on land. Examples: Wall lizard, Snake, Turtle, Tortoise, Crocodile |
| **4. Aves** (Birds) | Streamlined body covered with **feathers**; forelimbs modified into **wings** for flight; jaws modified into a toothless horny **beak**; light hollow (**pneumatic**) bones; air sacs connected to lungs. | **Lungs** (assisted by air sacs) | **4-chambered heart** (2 auricles, 2 ventricles); **warm-blooded (homeothermic)**. | Oviparous; internal fertilisation; hard calcareous-shelled eggs. Examples: Pigeon, Danphe (*Lophophorus*), Crow, Ostrich, Penguin |
| **5. Mammalia** | Body covered with **hair or fur**; possess milk-producing **mammary glands** to nourish young ones, external ears (**pinna**), and a muscular **diaphragm** separating thorax and abdomen. | **Lungs** | **4-chambered heart** (2 auricles, 2 ventricles); **warm-blooded (homeothermic)**. | **Viviparous** (give birth to young ones; exception: egg-laying Platypus & Echidna). Examples: Human, Cow, Tiger, Bat (flying mammal), Whale & Dolphin (aquatic mammals) |

## 2.4 Relationship between classification and evolution

**Classification** and **organic evolution** are closely interconnected:

1. **Simple to complex body organisation:** Both plant and animal classifications follow the order of evolutionary development from primitive, simple organisms to advanced, complex ones.
   - In **Kingdom Plantae**, evolution progressed from aquatic thalloid **Algae** $\rightarrow$ land-dwelling non-vascular **Bryophyta** $\rightarrow$ spore-bearing vascular **Pteridophyta** $\rightarrow$ naked-seeded **Gymnosperms** $\rightarrow$ fruit-bearing flowering **Angiosperms**.
   - In **Kingdom Animalia**, invertebrates evolved from cellular-level **Porifera** $\rightarrow$ tissue-level diploblastic **Coelenterata** $\rightarrow$ triploblastic acoelomate **Platyhelminthes** $\rightarrow$ pseudocoelomate **Nemathelminthes** $\rightarrow$ true coelomate segmented **Annelida** $\rightarrow$ **Arthropoda**, **Mollusca** and **Echinodermata** $\rightarrow$ **Chordata**.
   - Among **Vertebrates**, aquatic **Pisces** (2-chambered heart, gills) evolved into **Amphibia** (3-chambered heart, water-to-land transition) $\rightarrow$ **Reptilia** (fully terrestrial, shelled eggs) $\rightarrow$ warm-blooded **Aves** and **Mammalia** (4-chambered heart).
2. **Common ancestry:** Organisms placed in the same taxonomic group share more homologous structures and DNA similarities because they diverged from a **recent common ancestor**. For example, Porifera, Annelida and Chordata represent sequential milestones along the animal evolutionary tree.

```photo id="sci10/rohu" caption="Rohu, a fish (class Pisces): the body is covered with scales and it breathes with gills." width="60"
```

```photo id="sci10/frog" caption="A frog (class Amphibia): moist skin, and it lives both in water and on land." width="56"
```

```photo id="sci10/pigeon" caption="A pigeon (class Aves): a bird has feathers, wings and a beak and is warm-blooded." width="56"
```

::: tip Mammals
Mammals are the only animals with milk-producing glands (mammary glands) and external ears (pinna). Most give birth to young ones; the platypus lays eggs.
:::

::: example Worked example 2.2 (placing an organism)
**Problem.** An organism is unicellular, has a true nucleus, lives in pond water, moves with cilia and takes in food through a mouth-like groove. In which kingdom does it belong? Name a likely example.

**Solution.** Unicellular + true nucleus means it is eukaryotic and unicellular, which rules out Monera, Fungi (no cilia, cell wall of chitin), Plantae and Animalia (multicellular). So it belongs to **Protista**. The example is *Paramecium*.
:::

::: example Worked example 2.3 (using a key)
**Problem.** Place these organisms in their kingdoms: *Nostoc*, mushroom, *Hydra*, fern, *Euglena*.

**Solution.** *Nostoc* — a cyanobacterium, prokaryotic: **Monera**. Mushroom — has hyphae and chitin, heterotrophic: **Fungi**. *Hydra* — multicellular, heterotrophic, no cell wall: **Animalia**. Fern — multicellular, has chlorophyll, cellulose wall: **Plantae**. *Euglena* — unicellular, eukaryotic, with a flagellum: **Protista**.
:::

::: caution Common mistake
Do not place yeast in Plantae or bacteria in Plantae. Yeast is a (unicellular) fungus; bacteria are Monera. Also, viruses are not placed in any of the five kingdoms because they are not cellular and show life only inside a host cell.
:::

### Comparison: plants and animals

| Plantae | Animalia |
|---|---|
| Cell wall present | Cell wall absent |
| Autotrophic | Heterotrophic |
| Chlorophyll present | Chlorophyll absent |
| Do not move from place to place | Move from place to place |
| Grow throughout life at tips | Growth stops after maturity |
| Store food as starch | Store food as glycogen and fat |

## Chapter summary

- Taxonomy is the identification, naming and classification of organisms. Linnaeus is the father of taxonomy; Whittaker proposed five kingdoms in 1969.
- The hierarchy is Kingdom → Phylum → Class → Order → Family → Genus → Species; the species is the basic unit.
- Binomial nomenclature: two Latin names, genus (capital) then species (small letter), in italics or underlined.
- Monera: prokaryotic, unicellular (bacteria, cyanobacteria); binary fission.
- Protista: unicellular eukaryotes (*Amoeba*, *Paramecium*, *Euglena*).
- Fungi: chitin cell wall, hyphae, saprophytic or parasitic, spores (yeast, mushroom).
- Plantae: multicellular, cellulose wall, photosynthesis; algae, bryophytes, pteridophytes, gymnosperms, angiosperms.
- Animalia: multicellular, heterotrophic, no cell wall; invertebrate phyla and five classes of vertebrates (fish, amphibians, reptiles, birds, mammals).

## Practice questions

**Group A — Objective questions (1 mark each)**

1. Who is called the father of taxonomy? <span class="marks">[1]</span>
   (a) Aristotle (b) Linnaeus (c) Whittaker (d) Darwin
2. Which of the following is a prokaryote? <span class="marks">[1]</span>
   (a) Yeast (b) *Amoeba* (c) Bacteria (d) *Euglena*
3. The cell wall of fungi is made of <span class="marks">[1]</span>
   (a) cellulose (b) chitin (c) peptidoglycan (d) protein
4. The correct way of writing the scientific name of man is <span class="marks">[1]</span>
   (a) *homo sapiens* (b) *Homo Sapiens* (c) *Homo sapiens* (d) *Sapiens homo*
5. Which kingdom includes *Paramecium*? <span class="marks">[1]</span>
   (a) Monera (b) Protista (c) Fungi (d) Animalia
6. Which group of plants bears naked seeds? <span class="marks">[1]</span>
   (a) Pteridophytes (b) Bryophytes (c) Gymnosperms (d) Angiosperms

::: note Answers to Group A
**1.** (b) — Linnaeus introduced binomial nomenclature and the ranks.
**2.** (c) — bacteria have no true nucleus.
**3.** (b) — chitin, a tough carbohydrate.
**4.** (c) — genus capital, species small, in italics.
**5.** (b) — *Paramecium* is a ciliated unicellular eukaryote.
**6.** (c) — gymnosperm means "naked seed".
:::

**Group B — Short answer (2 marks each)**

1. Define taxonomy and binomial nomenclature. <span class="marks">[2]</span>
2. Write any two differences between prokaryotic and eukaryotic cells. <span class="marks">[2]</span>
3. Why is Whittaker's five-kingdom system better than the older two-kingdom system? <span class="marks">[2]</span>
4. Name the four shapes of bacteria with one example each. <span class="marks">[2]</span>
5. List any two characteristics of fungi. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Taxonomy is the branch of biology that identifies, names and classifies organisms. Binomial nomenclature is the system of naming an organism with two words, the genus and the species.
**2.** Prokaryotic cells have no true nucleus and no membrane-bound organelles; eukaryotic cells have a true nucleus and membrane-bound organelles.
**3.** It uses cell type, number of cells, mode of nutrition and body organisation; so bacteria, fungi and unicellular organisms like *Euglena* get proper places which they did not have in the plant-animal system.
**4.** Cocci (*Streptococcus*), bacilli (*Bacillus*), spirilla (*Spirillum*), vibrios (*Vibrio cholerae*).
**5.** They have a chitin cell wall and no chlorophyll; they feed by absorption; they reproduce by spores.
:::

**Group C — Long answer (4 marks each)**

1. Describe the characteristics of the kingdom Monera and Protista. <span class="marks">[4]</span>
2. Differentiate between plants and animals on the basis of four points. <span class="marks">[4]</span>
3. Write the taxonomic hierarchy with a suitable example and state the rules for writing scientific names. <span class="marks">[4]</span>
4. Classify the vertebrates into classes with two characteristics and an example of each. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Monera: prokaryotic and unicellular; cell wall present; no mitochondria or chloroplast; nutrition autotrophic or heterotrophic; binary fission; examples bacteria and cyanobacteria. Protista: unicellular eukaryotes with a true nucleus; live in water or moist places; locomotion by pseudopodia, cilia or flagella; nutrition autotrophic or heterotrophic; binary fission; examples *Amoeba*, *Paramecium*, *Euglena*.
**2.** Plants have a cell wall, animals do not; plants are autotrophic, animals heterotrophic; plants have chlorophyll, animals do not; plants do not move from place to place, most animals do; plants store starch, animals glycogen.
**3.** Kingdom Animalia → Phylum Chordata → Class Mammalia → Order Primates → Family Hominidae → Genus *Homo* → Species *Homo sapiens*. Rules: Latin; italics (or underlined); genus name begins with a capital letter and species with a small letter; genus first, then species.
**4.** Pisces: scales and gills, rohu. Amphibia: moist skin, lungs and skin in adult, frog. Reptilia: dry scaly skin, lungs, lizard. Aves: feathers, warm-blooded, pigeon. Mammalia: hair, mammary glands, warm-blooded, human.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe the five-kingdom system of classification with the main characteristics and examples of each kingdom. <span class="marks">[10]</span>
2. Classify the plant kingdom into its main divisions and differentiate between monocot and dicot plants. <span class="marks">[10]</span>

```photogrid label="2.H" cols="5" ratio="1.0" caption="One organism from each kingdom. (a) Bacteria (Monera) have no nucleus. (b) Paramecium (Protista) is one cell with a nucleus. (c) A mushroom (Fungi) absorbs food from dead matter. (d) A hibiscus (Plantae) makes food with chlorophyll. (e) A frog (Animalia) eats other organisms. Notice that size does not decide the kingdom; cell type and feeding do."
@ photo id="sci10/bacteria-shapes" cap="(a) Bacteria, Monera"
@ photo id="sci10/paramecium" cap="(b) Paramecium, Protista"
@ photo id="sci10/mushroom" cap="(c) Mushroom, Fungi"
@ photo id="sci10/hibiscus" cap="(d) Hibiscus, Plantae"
@ photo id="sci10/frog" cap="(e) Frog, Animalia"
```

### Model answer D1: five-kingdom classification (10 marks)

**Introduction.** There are millions of kinds of living things, so scientists put them into groups. **R. H. Whittaker (1969)** divided all living beings into **five kingdoms** on the basis of the type of cell (without or with a nucleus), the number of cells, the way of getting food and the body organisation. The system is easy to use and is the one taught in school.

**1. Kingdom Monera.** These are **single-celled organisms without a true nucleus** (prokaryotes). They have a cell wall but no nuclear membrane. Examples: *Escherichia coli*, *Bacillus*, *Nostoc* and blue-green algae. Some cause diseases such as typhoid and cholera, while others make curd from milk.

**2. Kingdom Protista.** These are mostly **single-celled organisms with a true nucleus**, living in water or damp places. Some make food by photosynthesis (*Euglena*), others eat food (*Amoeba*, *Paramecium*). *Plasmodium* is a protist that causes malaria.

**3. Kingdom Fungi.** Fungi have **cell walls but no chlorophyll**, so they cannot make their own food. They feed on dead or living matter (saprophytes or parasites) by absorbing it. Examples: mushroom, yeast, *Penicillium* (the source of penicillin) and bread mould.

**4. Kingdom Plantae.** Plants are many-celled organisms with **cell walls of cellulose and chlorophyll**. They make food by photosynthesis, so they are **autotrophs**. Examples: moss, fern, pine, rice, hibiscus.

**5. Kingdom Animalia.** Animals are many-celled organisms with **no cell wall and no chlorophyll**. They depend on other living things for food (**heterotrophs**) and most can move. Examples: earthworm, cockroach, rohu, frog, pigeon, human beings.

**Comparison table.**

| Kingdom | Cell type | Number of cells | Cell wall | Nutrition | Example |
|---|---|---|---|---|---|
| Monera | Prokaryotic | One | Present | Autotroph or heterotroph | Bacteria |
| Protista | Eukaryotic | Mostly one | Some | Autotroph or heterotroph | Amoeba |
| Fungi | Eukaryotic | Mostly many | Present (not cellulose) | Absorb dead matter | Mushroom |
| Plantae | Eukaryotic | Many | Cellulose | Autotroph | Hibiscus |
| Animalia | Eukaryotic | Many | Absent | Heterotroph | Frog |

**Conclusion.** The five-kingdom system arranges living things from simple to complex and helps us to identify, study and protect the biodiversity of Nepal.

### Model answer D2: divisions of the plant kingdom and monocot versus dicot (10 marks)

**Introduction.** Kingdom Plantae is divided into groups by the presence of **true roots, stems and leaves**, **vascular tissue** (xylem and phloem for carrying water and food) and **seeds**.

**Divisions of the plant kingdom.**

| Division | Body | Vascular tissue | Seeds / flowers | Examples |
|---|---|---|---|---|
| Thallophyta (algae) | Thallus, no root, stem or leaf | Absent | None | *Spirogyra*, *Ulothrix* |
| Bryophyta | Small, leaf-like, with rhizoids | Absent | None; spores | Moss, liverwort |
| Pteridophyta | True root, stem and leaves | Present | None; spores in sori | Fern, horsetail |
| Gymnosperms | Trees and shrubs | Present | Naked seeds in cones | Pine, cycas |
| Angiosperms | Herbs, shrubs, trees | Present | Seeds in fruits; flowers | Rice, mango, hibiscus |

**Key points.**

- **Thallophyta** are simple plants of ponds and streams.
- **Bryophytes** need water for fertilisation and grow on damp rocks and walls, as moss does in the hills of Nepal.
- **Pteridophytes** show the first vascular tissue and carry spores under the leaf in small brown spots called **sori**.
- **Gymnosperms** have "naked seeds" because the seeds are not enclosed in a fruit.
- **Angiosperms** are the largest group. They are divided into **monocots** (one seed leaf) and **dicots** (two seed leaves).

**Monocot versus dicot.**

| Feature | Monocot | Dicot |
|---|---|---|
| Seed leaf (cotyledon) | One | Two |
| Root | Fibrous | Tap root |
| Leaf veins | Parallel | Net-like |
| Flower parts | In threes | In fours or fives |
| Vascular bundles in stem | Scattered | In a ring |
| Examples | Maize, rice, wheat | Pea, mango, hibiscus |

**Importance.** Plants supply food, oxygen, timber, medicine (such as *timur* and *jatamansi* from the Himalayas) and fuel. They also prevent soil erosion on the steep hills of Nepal.

**Conclusion.** Plant classification moves from simple thallus plants to seed-bearing flowering plants, and the monocot-dicot difference is the most useful in practical identification.

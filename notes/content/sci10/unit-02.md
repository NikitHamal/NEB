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

```figure caption="Four shapes of bacteria, drawn schematically, with examples."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,2.5))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,5.5)
for cx,cy in [(1.3,3.5),(2.1,3.5),(1.7,2.8),(1.0,2.8)]:
    ax.add_patch(Circle((cx,cy),0.35,fc="#cfe0ff",ec=ACCENT))
ax.text(1.6,2.0,"Cocci\n(sphere)\nStreptococcus",ha='center',va='top',fontsize=7.5,color=INK)
for cx,cy,a in [(4.5,3.4,10),(5.3,3.0,-20),(4.6,2.6,5)]:
    ax.add_patch(FancyBboxPatch((cx-0.6,cy-0.2),1.2,0.4,boxstyle="round,pad=0.1",fc="#cfe0ff",ec=ACCENT,transform=matplotlib.transforms.Affine2D().rotate_deg_around(cx,cy,a)+ax.transData))
ax.text(4.9,2.0,"Bacilli\n(rod)\nBacillus",ha='center',va='top',fontsize=7.5,color=INK)
t=np.linspace(0,4*np.pi,200)
ax.plot(7.2+0.35*np.sin(t)*0+0.3*np.sin(t)+0.0, 2.2+ t/(4*np.pi)*2.4, color=ACCENT, lw=3)
ax.text(7.2,2.0,"Spirilla\n(spiral)\nSpirillum",ha='center',va='top',fontsize=7.5,color=INK)
tt=np.linspace(-0.9,0.9,50)
ax.plot(10+tt*1.0, 3.6-1.0*tt**2+0.0, color=ACCENT, lw=5, solid_capstyle='round')
ax.text(10,2.0,"Vibrios\n(comma)\nVibrio cholerae",ha='center',va='top',fontsize=7.5,color=INK)
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

| Protist | Locomotion | Nutrition |
|---|---|---|
| *Amoeba* | Pseudopodia | Heterotrophic |
| *Paramecium* | Cilia | Heterotrophic |
| *Euglena* | Flagellum | Autotrophic and heterotrophic |
| *Plasmodium* | None (parasite) | Heterotrophic |

### Kingdom Fungi

- Mostly **multicellular** (yeast is unicellular), **eukaryotic**.
- The body is made of thread-like **hyphae**, which together form a **mycelium**.
- The cell wall is made of **chitin** (not cellulose).
- **No chlorophyll**, so no photosynthesis. Fungi are **heterotrophic**: **saprophytes** feed on dead matter (mushroom, bread mould), **parasites** on living hosts (the rust fungus on wheat).
- They secrete enzymes outside the body to digest food and then absorb the digested food (**absorptive nutrition**).
- Reproduce by **spores**, by budding (yeast) and by fragmentation.
- Store food as glycogen, as animals do.

**Importance.** Yeast is used in making bread and alcohol; *Penicillium* gives the antibiotic penicillin; some mushrooms are food (*Agaricus*, the button mushroom); other fungi cause athlete's foot, ringworm and food spoilage. Fungi, along with bacteria, are **decomposers**.

### Kingdom Plantae

- **Multicellular**, **eukaryotic**, with a **cell wall of cellulose**.
- Contain **chlorophyll** in chloroplasts and make food by **photosynthesis**, so they are **autotrophic** (producers).
- Mostly fixed in one place; they do not move from place to place.
- Reproduction is vegetative, asexual (spores) or sexual (seeds).
- Store food as starch.

Plants are divided into five groups:

| Group | Main features | Examples |
|---|---|---|
| Algae (Thallophyta) | No true root, stem or leaf; mostly aquatic | *Spirogyra*, *Ulothrix* |
| Bryophyta | Small, grow in moist places, no vascular tissue, root-like rhizoids | Moss (*Funaria*), liverwort (*Marchantia*) |
| Pteridophyta | Have root, stem, leaves and vascular tissue; no flowers or seeds; reproduce by spores | Ferns (*Nephrolepis*), horsetail |
| Gymnosperms | Seeds are naked (no fruit), cones present | Pine (*Pinus*), cycas |
| Angiosperms | Flowering plants; seeds enclosed in fruits | Mango, rice, pea |

Angiosperms are further divided into **monocots** (one seed leaf, parallel leaf veins, fibrous roots: maize, rice, wheat) and **dicots** (two seed leaves, net-like veins, tap root: pea, mustard, mango).

| Monocotyledon | Dicotyledon |
|---|---|
| One cotyledon in the seed | Two cotyledons |
| Parallel venation | Reticulate (net) venation |
| Fibrous roots | Tap root |
| Flower parts in threes | Flower parts in fours or fives |

### Kingdom Animalia

- **Multicellular**, **eukaryotic**, cells without cell wall.
- **Heterotrophic**: they take food in (**ingestion**) and digest it inside the body.
- Most can **move** from place to place at some stage of life.
- Have nervous system and sense organs (except in the simplest ones), so they respond quickly to stimuli.
- Reproduce mostly sexually; store food as glycogen and fat.

Animals are divided into **invertebrates** (no backbone) and **vertebrates** (backbone present).

| Phylum | Main features | Examples |
|---|---|---|
| Porifera | Pores on the body, sessile, no organs | Sponge |
| Coelenterata (Cnidaria) | Tentacles with stinging cells; sac-like body | *Hydra*, jellyfish |
| Platyhelminthes | Flat body, no body cavity | Tapeworm, liver fluke |
| Aschelminthes (Nematoda) | Round, unsegmented worm | *Ascaris* |
| Annelida | Body divided into segments | Earthworm, leech |
| Arthropoda | Jointed legs, hard outer skeleton; the largest phylum | Honey bee, spider, prawn |
| Mollusca | Soft body, usually a shell | Snail, octopus |
| Echinodermata | Spiny skin | Starfish |
| Chordata | Notochord; vertebrates are included | Fish, frog, lizard, bird, human |

Vertebrates are placed in five classes:

| Class | Body covering | Respiration | Body temperature | Examples |
|---|---|---|---|---|
| Pisces (fish) | Scales | Gills | Cold-blooded | Rohu, shark |
| Amphibia | Moist skin | Gills (larva), lungs and skin (adult) | Cold-blooded | Frog, toad |
| Reptilia | Dry scales | Lungs | Cold-blooded | Lizard, snake, crocodile |
| Aves (birds) | Feathers | Lungs | Warm-blooded | Pigeon, Himalayan monal (Danphe) |
| Mammalia | Hair or fur | Lungs | Warm-blooded | Cow, tiger, human |

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

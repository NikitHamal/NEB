---
subject: Zoology
grade: CEE
unit: 1
title: Evolutionary Biology
hours: 3
area: Evolution and Diversity
---

Evolutionary Biology carries **3 of the 40 Zoology questions**. The paper draws
them from four places: the origin of life (Oparin–Haldane and Miller–Urey), the
evidences of evolution (homologous, analogous and vestigial organs, connecting
links, fossils, embryos and molecules), the theories (Lamarck, Darwin and the
modern synthesis) and the line of human ancestry from *Ramapithecus* to modern
man. Almost every question is a name, a date, an example or an exception — this
chapter puts them in tables.

::: key What the paper asks from this chapter
- The **reducing primitive atmosphere** — CH₄, NH₃, H₂ and water vapour, **no free O₂** — and the order monomers → polymers → coacervates/microspheres → protocell.
- **Miller–Urey (1953)**: electric spark through CH₄, NH₃, H₂ (2 : 2 : 1) and steam for one week gave **amino acids** (glycine, alanine), not life.
- **Homologous** organs = same origin, different function = **divergent** evolution; **analogous** = different origin, same function = **convergent** evolution; vestigial organs and atavism.
- **Connecting links** (*Peripatus*, *Neopilina*, *Balanoglossus*, lungfish, *Archaeopteryx*, platypus) and the **horse series** *Eohippus* → *Equus*.
- **Haeckel's biogenetic law**, Nuttall's **precipitin test**, the universal genetic code and cytochrome c.
- **Lamarck** (use and disuse, inheritance of acquired characters; Weismann's reply), **Darwin** (overproduction, struggle, variation, natural selection), **de Vries** (mutation, *Oenothera*) and the **modern synthesis** with Hardy–Weinberg and industrial melanism.
- The hominid sequence with **places, discoverers, cranial capacities and "firsts"** — *Ramapithecus* at **Tinau Khola, Butwal**; *H. habilis* the first tool-maker; *H. erectus* the first user of fire; Neanderthals the first to bury their dead; Cro-Magnon the cave painters.
:::

## 1.1 Origin of life: the Oparin–Haldane theory and the Miller–Urey experiment

The Earth is about **4.6 billion years** old. The oldest undisputed fossils —
**stromatolites**, layered mats built by cyanobacteria — are about **3.5 billion
years** old, so life arose within the first billion years.

### Theories before chemical evolution

| Theory | Claim | Who / evidence | Verdict |
|---|---|---|---|
| Special creation | all species created at once, unchanged since | religious texts | untestable; contradicted by fossils |
| Spontaneous generation (**abiogenesis**) | life arises repeatedly from non-living matter (maggots from meat, mice from grain) | Aristotle, van Helmont | disproved |
| Disproof 1 | meat in sealed or gauze-covered jars got no maggots | **Francesco Redi (1668)** | maggots come from fly eggs |
| Disproof 2 | boiled broth in sealed flasks stayed sterile | **Lazzaro Spallanzani (1767)** | microbes come from the air |
| Disproof 3 | broth in a **swan-necked flask** stayed sterile; broke the neck → microbes grew | **Louis Pasteur (1860s)** | **biogenesis**: *omne vivum ex vivo* |
| Cosmozoic / panspermia | life came from space as spores | Richter (1865), Arrhenius (1908) | only moves the problem elsewhere |
| **Chemical evolution** | life arose from non-living chemicals *once*, under conditions that no longer exist | **Oparin (1924), Haldane (1929)** | accepted model |

### The Oparin–Haldane theory

**A. I. Oparin** (Russian biochemist, 1924) and **J. B. S. Haldane** (British
geneticist, 1929) proposed independently that life arose by slow chemical
evolution. The theory is also called the **naturalistic** or
**physico-chemical** theory.

**Conditions on the primitive Earth**

- Atmosphere **reducing**: methane (CH₄), ammonia (NH₃), hydrogen (H₂) and water vapour, with some CO₂, N₂ and HCN — **no free oxygen**.
- No ozone layer, so strong **ultraviolet radiation** reached the surface.
- Energy from UV light, **lightning (electric discharge)**, volcanic heat, radioactivity and cosmic rays.
- A cooling crust, condensing rain and warm shallow seas.

**The steps**

1. **Atoms → simple inorganic molecules** (H₂O, CH₄, NH₃, CO₂, HCN).
2. **Simple organic monomers**: amino acids, simple sugars, nitrogen bases, fatty acids, glycerol. They accumulated in the sea — Haldane's **"hot dilute soup"** (prebiotic soup).
3. **Polymers**: proteins, polysaccharides, fats and nucleic acids, condensing on warm clay or in drying pools.
4. **Protobionts** — membrane-bounded aggregates that keep an internal chemistry: Oparin's **coacervates** and Fox's **microspheres** (table below).
5. **First cell (protocell / eobiont)**: a self-replicating nucleic acid enclosed in a membrane. RNA probably came first (**RNA world**: RNA both stores information and catalyses, as **ribozymes** do).
6. The first organisms were **prokaryotic, anaerobic heterotrophs** living on the soup. As the soup ran out, **chemoautotrophs** and then **photoautotrophs** (cyanobacteria) evolved.
7. Photosynthesis released **O₂**; the atmosphere became **oxidising**, the **ozone layer** formed, and chemical evolution stopped for ever. O₂ allowed **aerobic** respiration and, later, eukaryotes.

| Protobiont | Proposed by | How formed | Features |
|---|---|---|---|
| **Coacervate** | **Oparin** | colloidal droplets of proteins, polysaccharides etc. separating out of water | absorb materials, grow, divide; no lipid membrane |
| **Microsphere** (proteinoid microsphere) | **Sidney Fox** | heating dry amino acids gives **proteinoids**; in water they form spheres | double-layered boundary, osmotic swelling, budding |

::: caution Why life cannot arise this way today
Free **O₂** in today's air oxidises organic molecules as fast as they form, and
any that survive are eaten by existing microbes. "Chemical evolution is going on
in the oceans now" is a standard wrong option.
:::

### The Miller–Urey experiment (1953)

**Stanley L. Miller**, a student of **Harold C. Urey** at the University of
Chicago, tested steps 1–2 in a closed glass apparatus.

```figure caption="The Miller–Urey apparatus. Steam from the boiling flask carries water vapour into the spark flask filled with CH₄, NH₃ and H₂; the spark plays the part of lightning, the condenser the part of rain, and the U-trap collects the products and returns them to the flask. After a week the water held amino acids."
import numpy as np
from matplotlib.patches import Circle, Rectangle, Polygon
fig, ax = plt.subplots(figsize=(5.2, 3.9))
ax.set_xlim(0, 10.4); ax.set_ylim(0, 7.9); ax.set_aspect("equal"); ax.axis("off")
GLASS = "#5b6b7a"; WATER = "#cfe3f3"; PROD = "#d9b98a"
def tube(xs, ys, lw=3.2):
    ax.plot(xs, ys, color=GLASS, lw=lw, solid_capstyle="round", zorder=2)
    ax.plot(xs, ys, color="white", lw=lw - 2.0, solid_capstyle="round", zorder=3)
# boiling flask with water
bx, by, br = 2.0, 1.7, 0.85
th = np.linspace(0, 2 * np.pi, 300)
lvl = by + 0.05
cx, cy = bx + br * np.cos(th), by + br * np.sin(th)
m = cy <= lvl
pts = np.c_[cx[m], cy[m]]
pts = pts[np.argsort(np.arctan2(pts[:, 1] - by, pts[:, 0] - bx))]
ax.add_patch(Polygon(pts, closed=True, fc=WATER, ec="none", zorder=4))
ax.add_patch(Circle((bx, by), br, fc="none", ec=GLASS, lw=1.6, zorder=5))
# flame
ax.add_patch(Polygon([[1.75, 0.15], [2.25, 0.15], [2.0, 0.72]], closed=True,
                     fc="#f2a541", ec="#c0392b", lw=0.8, zorder=4))
# vapour tube up and across to the spark flask
tube([bx, bx, 5.25], [by + br, 6.1, 6.1])
ax.annotate("", xy=(bx, 5.3), xytext=(bx, 4.1),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[0], lw=1.2), zorder=6)
# spark flask
sx, sy, sr = 6.45, 6.0, 1.2
ax.add_patch(Circle((sx, sy), sr, fc="#f4f4f8", ec=GLASS, lw=1.6, zorder=4))
for x0, x1 in [(5.55, 6.18), (7.35, 6.72)]:
    ax.plot([x0, x1], [7.75, 6.25], color=INK, lw=1.6, zorder=6)
zx = np.linspace(6.18, 6.72, 7)
zy = 6.25 + np.array([0, .12, -.12, .12, -.12, .12, 0])
ax.plot(zx, zy, color="#e67e22", lw=1.3, zorder=7)
ax.text(sx, 5.35, "CH$_4$  NH$_3$\nH$_2$  H$_2$O", ha="center", va="center",
        fontsize=7.2, color=INK, zorder=8, linespacing=1.3)
# outlet, condenser, U-trap back to the boiling flask
tube([sx, sx, sx], [sy - sr, 4.2, 2.3])
ax.add_patch(Rectangle((sx - 0.32, 2.55), 0.64, 1.55, fc="#e3f0f7", ec=GLASS,
                       lw=1.2, zorder=4))
tube([sx, sx], [4.15, 2.5])
tube([sx + 0.32, sx + 0.75], [2.75, 2.75], lw=2.4)
tube([sx + 0.32, sx + 0.75], [3.9, 3.9], lw=2.4)
tt = np.linspace(0, np.pi, 40)
ux, uy = 5.95 + 0.5 * np.cos(tt), 1.0 - 0.5 * np.sin(tt)
tube([sx, sx], [2.5, 1.0])
tube(list(ux), list(uy))
tube([5.45, 5.45, bx + br - 0.02], [1.0, by, by])
ax.add_patch(Circle((5.95, 0.62), 0.16, fc=PROD, ec="none", zorder=4))
tube([5.95, 5.95], [0.5, 0.18], lw=2.4)
ax.add_patch(Rectangle((5.80, 0.22), 0.30, 0.12, fc=GLASS, ec="none", zorder=6))
# labels
fs = 7.0
def lab(t, xy, xyt, ha="left"):
    ax.annotate(t, xy=xy, xytext=xyt, fontsize=fs, color=INK, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=9)
lab("boiling water\n(the primitive sea)", (1.45, 1.45), (0.05, 3.25))
ax.text(2.0, -0.12, "heat", ha="center", va="top", fontsize=fs, color=INK)
ax.text(1.55, 4.7, "water\nvapour", ha="right", va="center", fontsize=fs, color=SERIES[0])
lab("tungsten electrodes:\nspark = lightning", (7.2, 7.5), (8.0, 7.45))
lab("5-litre flask of\nreducing gases", (7.55, 5.5), (8.0, 5.55))
lab("condenser: cooling\nwater = rain", (6.8, 3.35), (8.0, 3.35))
lab("U-trap: products\nreturn to the flask", (6.15, 0.7), (7.35, 1.2))
ax.text(5.55, 0.25, "sample", ha="right", va="center", fontsize=fs, color=MUTED)
```

| Item | Detail |
|---|---|
| Gases in the spark flask | **CH₄, NH₃, H₂** — Miller's paper gives 20 cm, 20 cm and 10 cm of mercury, i.e. **CH₄ : NH₃ : H₂ = 2 : 2 : 1** — + water vapour; **no O₂** (some coaching books print 2 : 1 : 2; follow the original) |
| Energy source | **electric spark** between tungsten electrodes (= lightning); the water was boiled to circulate steam (many textbooks quote "about 800 °C" for the hot zone) |
| Cooling | condenser (= rain) |
| Duration | **one week**, run continuously |
| Analysis | paper chromatography of the solution that collected in the trap and boiling flask |
| Products | **amino acids** — **glycine** and **alanine** most abundant, also aspartic acid; urea, HCN, aldehydes, simple acids. Later work gave sugars and nitrogen bases |
| Conclusion | **organic monomers can form abiotically** from the reducing gases → supports Oparin–Haldane |

::: caution Miller did not make life — nor proteins
He made **monomers** (amino acids), not polypeptides, nucleic acids or cells. No
sulphur gas was used, so cysteine and methionine are not among the original
products. Options such as "living cells", "enzymes" or "DNA appeared in the trap"
are wrong.
:::

## 1.2 Evidences of evolution: morphological, anatomical, palaeontological, embryological and biochemical

### Morphological and anatomical evidence

| Feature | **Homologous organs** | **Analogous organs** |
|---|---|---|
| Origin and basic plan | same | different |
| Function | different | same |
| Shows | common ancestry — **divergent evolution** (adaptive radiation) | adaptation to the same need — **convergent evolution** |
| Animal examples | forelimbs of man, whale (flipper), bat (wing), horse, cheetah; hearts and brains of vertebrates; mouthparts of cockroach, honeybee, mosquito and butterfly | wings of insect and of bird or bat; eye of octopus and of mammal; flippers of penguin and dolphin; gills of fish and of prawn |
| Plant examples | thorn of *Bougainvillea* and tendril of *Cucurbita* (both stem) | sweet potato (root) and potato (stem tuber) |

**Vestigial organs** are reduced, functionless remnants of organs that were
useful in an ancestor. In man: **vermiform appendix** (a large caecum in
herbivores), **coccyx** (fused tail vertebrae), **nictitating membrane** (plica
semilunaris), **auricular (ear) muscles**, **wisdom teeth** (third molars), body
hair and the skin muscle (panniculus). Others: the **pelvic girdle and hind-limb
remnants of python and whale**, the wings of the kiwi and ostrich, the splint
bones of the horse.

```photo id="bio11/homology" caption="Analogous wings in three vertebrates: a pterodactyl (a reptile), a bat (a mammal) and a bird. The wing of each is built on the same forelimb skeleton, but the flight surface is different: a skin membrane on one long finger, a membrane stretched over four fingers, and feathers." width="50"
```


**Atavism** is the sudden reappearance of an ancestral character: a short tail in
a newborn, dense body hair, extra nipples, long canines.

**Connecting links** are living or fossil organisms with characters of two
groups — evidence that one group arose from the other.

```photo id="bio11/haeckel" caption="Comparative embryology: Haeckel's plate of eight vertebrates (fish, salamander, tortoise, chick, hog, calf, rabbit, human) at three stages. In row I the embryos are nearly alike, all with pharyngeal gill slits and a post-anal tail; species characters appear only in rows II and III. Haeckel overstated the similarity of the earliest stage; the lesson is von Baer's law, not recapitulation." width="90"
```


| Connecting link | Between | Characters of the first group | Characters of the second group |
|---|---|---|---|
| *Euglena* | plants and animals | chloroplasts, photosynthesis | no cell wall (pellicle), flagellum; heterotrophic in the dark |
| *Proterospongia* | Protozoa and Porifera | colonial flagellates | collar cells like choanocytes |
| ***Peripatus*** | **Annelida and Arthropoda** | segmentation, nephridia, unjointed legs, thin cuticle | tracheae, claws, open circulation (haemocoel) |
| ***Neopilina*** | Annelida and Mollusca | serially repeated gills and nephridia | shell, foot, radula |
| ***Balanoglossus*** | non-chordates and chordates | tornaria larva like an echinoderm larva | pharyngeal gill slits, dorsal nerve cord |
| **Lungfishes** (*Protopterus*, *Lepidosiren*, *Neoceratodus*) | fishes and amphibians | fins, gills, scales | lungs, three-chambered heart |
| *Seymouria* (fossil) | amphibians and reptiles | amphibian skull | reptilian skeleton |
| ***Archaeopteryx*** (fossil) | **reptiles and birds** | **teeth**, long bony **tail**, clawed fingers, weak sternum | **feathers**, wings, beak, wishbone (furcula) |
| **Duck-billed platypus** (*Ornithorhynchus*), spiny anteater (*Tachyglossus*) | reptiles and mammals | **lay eggs**, cloaca | **hair**, **mammary glands** |

::: caution Connecting link versus living fossil
A **living fossil** is a living species almost unchanged from long-extinct
relatives: ***Limulus*** (king crab), ***Latimeria*** (coelacanth), ***Sphenodon***
(tuatara), *Peripatus*, *Ginkgo*. *Peripatus* is both; *Limulus* is only a living
fossil — it is the favourite distractor for "connecting link between Annelida
and Arthropoda".
:::

### Palaeontological evidence (fossils)

A **fossil** is any preserved remain or trace of a past organism (petrified
bone, mould, cast, amber insect, frozen mammoth, footprint, coprolite). Fossils
show that life changed in order — simple forms in old rocks, complex forms in
young rocks — and they supply the **missing links**. Rocks are dated by
radioactive decay: **¹⁴C** (half-life **5730 years**, for remains under about
50,000 years), potassium–argon and uranium–lead for older rocks.

| Era | Period / epoch | Began (Mya) | Hallmark |
|---|---|---|---|
| Palaeozoic | Cambrian | 541 | "explosion" of invertebrates, trilobites |
| | Ordovician | 485 | first vertebrates — jawless fish |
| | Silurian | 443 | first land plants, first jawed fish |
| | Devonian | 419 | **Age of Fishes**; first amphibians at the end |
| | Carboniferous | 359 | **Age of Amphibians**; coal forests; first reptiles |
| | Permian | 299 | reptiles spread; the largest mass extinction ends it |
| Mesozoic (**Age of Reptiles**) | Triassic | 252 | first dinosaurs, **first mammals** |
| | Jurassic | 201 | dinosaurs dominant; **first birds** (*Archaeopteryx*) |
| | Cretaceous | 145 | flowering plants spread; dinosaurs extinct at 66 Mya |
| Cenozoic (**Age of Mammals**) | Palaeocene–Eocene | 66 | mammals radiate; *Eohippus* |
| | Oligocene–Miocene | 34 | apes; *Dryopithecus*, *Ramapithecus* |
| | Pliocene | 5.3 | *Australopithecus* |
| | Pleistocene (Quaternary) | 2.6 | ice ages; *Homo*; **Age of Man** |
| | Holocene | 0.012 | modern man, agriculture |

**Evolution of the horse** — the best fossil series, worked out in **North
America** — shows increasing size, longer face and legs, **loss of toes** and
**high-crowned grinding teeth** as the forest browser became a grassland grazer.

| Genus | Epoch | Toes (fore / hind) | Notes |
|---|---|---|---|
| ***Eohippus*** (*Hyracotherium*) | Eocene | 4 / 3 | fox-sized (about 30 cm), browser, "dawn horse" |
| ***Mesohippus*** | Oligocene | 3 / 3 | larger, middle toe larger |
| ***Merychippus*** | Miocene | 3 / 3, only the middle toe on the ground | first grazer, high-crowned teeth |
| ***Pliohippus*** | Pliocene | **1 / 1** | **first one-toed horse**; side toes as splints |
| ***Equus*** | Pleistocene–Recent | 1 / 1 (hoof) | modern horse, about 1.5 m |

***Archaeopteryx*** (Jurassic, about 150 Mya) was found in the **Solnhofen
limestone of Bavaria, Germany (1861)**. It had feathers and wings like a bird but
teeth, a long tail of free vertebrae and three clawed fingers like a reptile.

### Embryological evidence

Early embryos of all vertebrates look alike: all have **pharyngeal gill slits
(pouches)**, a **notochord**, a post-anal tail and a **two-chambered heart**.
The human embryo shows gill pouches and a fish-like two-chambered heart in its
first weeks; the frog's tadpole is a "fish" with gills, a tail and a lateral line.

- **Biogenetic law / recapitulation theory** — **Ernst Haeckel (1866)**: *"ontogeny recapitulates phylogeny"* — an individual's development repeats the evolutionary history of its race.
- **Von Baer's law (1828)** — embryos of higher animals resemble the **embryos**, not the adults, of lower animals. This is the form accepted today.
- Larvae show relationships: the **trochophore** larva links annelids with molluscs; the **tornaria** of *Balanoglossus* resembles the **bipinnaria** of starfish, linking echinoderms with chordates; the **tadpole larva** of an ascidian has a notochord, proving it a chordate.

::: caution The human embryo never becomes a fish
It develops gill **pouches**, never functional gills, and it passes through
stages like the **embryo** of a fish, not the adult fish. Haeckel's literal
"adult stages" wording is the trap.
:::

### Biochemical evidence

- All organisms use **DNA/RNA**, the **same genetic code**, **ATP**, similar enzymes and the same 20 amino acids.
- **Cytochrome c** (a respiratory protein of 104 amino acids): human and chimpanzee are identical; human and rhesus monkey differ at 1 position; the number of differences rises with evolutionary distance.
- **Serum precipitin test** — **G. H. F. Nuttall (1904)**: rabbit anti-human serum precipitates human serum most strongly, then chimpanzee and gorilla, then orang-utan, then monkeys — the same order as the anatomical tree.
- Hormones work across species (pig and cattle insulin treated diabetics for decades); DNA–DNA hybridisation puts human and chimpanzee DNA about 98–99 % alike.

```photogrid label="1.1" cols="2" ratio="1.2" caption="Dating fossils needs the right clock. (a) The Berlin specimen of Archaeopteryx, a feathered reptile-like bird about 150 million years old, a classic palaeontological evidence for evolution. (b) Radiocarbon decays with a half-life of 5,730 years, so the fraction left is 0.5 to the power (t/5,730): 50 per cent after 1 half-life, 25 per cent after 2 and 12.5 per cent after 3, i.e. 17,190 years. Beyond about 50,000 years only 0.24 per cent is left, too little to measure, so rocks as old as Archaeopteryx are dated with uranium-238 (half-life 4.47 billion years), of which 97.7 per cent would still remain after 150 million years."
@ photo id="ceezoo/archaeopteryx" cap="Archaeopteryx, Berlin specimen"
fit 1.2
focus 0.5 0.45
@ svg cap="Fraction of carbon-14 left against age"
H = 5730.0
fr = lambda t: 100 * 0.5 ** (t / H)
assert abs(fr(3 * H) - 12.5) < 1e-9 and round(3 * H) == 17190
c50 = fr(50000); u150 = 100 * 0.5 ** (150e6 / 4.468e9)
assert abs(c50 - 0.24) < 0.01 and abs(u150 - 97.7) < 0.1
facts = dict(f1="%.0f" % fr(H), age="{:,}".format(round(3 * H)), c50="%.2f" % c50, u150="%.1f" % u150)
f = Fig(300, 236)
f.text(150, 12, "Carbon-14 remaining (%) against years", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 34, 232, 140, (0, 30000), (0, 100))
ax.grid(10000, 25, xfmt=lambda v: "%dk" % (v // 1000)).axes("yr", "%")
ax.curve(fr, 0, 30000, color=RED)
for k in (1, 2, 3):
    ax.pt(k * H, fr(k * H), "%g%%" % fr(k * H), dx=8, dy=-8, r=3.6)
f.text(150, 206, "12.5 per cent left = 3 half-lives = 17,190 yr", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "useful to about 50,000 yr only (0.24%)", size=10.5, color=SLATE, bold=True)
```

## 1.3 Lamarckism, Darwinism and Neo-Darwinism

### Lamarckism — inheritance of acquired characters

**Jean-Baptiste de Lamarck** (French, 1744–1829) set out the first full theory
of evolution in ***Philosophie Zoologique* (1809)**. He also popularised the word
*biology*.

```photo id="bio11/finches-gould" caption="Beaks of four Galápagos finches (Gould's plate for Darwin): 1 *Geospiza magnirostris*, the large ground finch with a heavy crushing beak; 2 *G. fortis*; 3 *G. parvula*; 4 *Certhidea olivacea*, the warbler finch with a thin probing beak." width="76"
```


1. **Internal vital force** — organisms tend to increase in size.
2. **Effect of environment and new needs** — a changed environment creates new needs and new habits.
3. **Use and disuse of organs** — an organ used more grows stronger; one not used weakens and disappears.
4. **Inheritance of acquired characters** — changes acquired in a lifetime pass to the offspring.

| Lamarck's example | His explanation |
|---|---|
| Long neck and forelimbs of the **giraffe** | ancestors stretched to browse high leaves; each generation inherited the stretch |
| Limbless **snakes** | ancestors stopped using legs while creeping through narrow places |
| Webbed feet of ducks | skin between the toes stretched by swimming |
| Flightless birds, blind cave animals | wings and eyes lost by disuse |

**Refutation.** **August Weismann** cut off the tails of mice for **22
generations**; every newborn had a normal tail. His **germplasm theory (1892)**:
only changes in the germ cells (germplasm) are inherited; changes in body cells
(somatoplasm) are not. Pierced ears and noses, bound feet and the strong arms of
a blacksmith are never inherited.

### Darwinism — natural selection

**Charles Darwin** (English, 1809–1882) sailed round the world on **HMS
*Beagle* (1831–1836)**; the finches and tortoises of the **Galápagos Islands**
impressed him most. He drew on **Lyell's** *Principles of Geology* (slow change
over long time) and **Malthus's** *Essay on the Principle of Population* (1798:
populations grow geometrically, food arithmetically). **Alfred Russel Wallace**,
working in the Malay Archipelago, reached the same idea; their joint papers were
read at the Linnean Society in **1858**, and ***On the Origin of Species by Means
of Natural Selection*** appeared on **24 November 1859**.

```photo id="bio11/biston" caption="Two forms of the peppered moth on one birch trunk: the pale form blends with the lichen-covered bark, while the dark form shows up clearly against it." width="76"
```


| Postulate | Content |
|---|---|
| 1. Overproduction (prodigality) | every species produces far more young than can survive — even the slow-breeding elephant would leave about 19 million descendants from one pair in 750 years |
| 2. Limited food and space | so numbers stay roughly constant |
| 3. **Struggle for existence** | intraspecific (most intense — same needs), interspecific, and environmental |
| 4. **Variation** | no two individuals are alike; some variations are heritable |
| 5. **Natural selection** — "**survival of the fittest**" (phrase of **Herbert Spencer**) | individuals with favourable variations survive and reproduce more |
| 6. Inheritance of useful variations | they accumulate generation after generation |
| 7. Origin of new species | accumulated differences make a new species |

**Weaknesses of Darwinism.** It could not explain **how variations arise or are
inherited** (Mendel's work of 1866 was unknown; Darwin's own **pangenesis**
theory of "gemmules" was wrong); it did not separate heritable from
non-heritable variation; it explains the *survival* of the fittest, not the
*arrival* of the fittest; and it could not explain vestigial organs or
over-specialised structures such as the giant antlers of the Irish elk.

**Mutation theory.** **Hugo de Vries** (Dutch botanist, 1901) found new,
true-breeding forms appearing suddenly in the evening primrose ***Oenothera
lamarckiana*** and proposed that species arise by large sudden jumps
(**saltation**). He coined the term **mutation**.

### Neo-Darwinism — the modern synthetic theory

Neo-Darwinism joins natural selection to **Mendelian and population genetics**.
Its builders: **R. A. Fisher, J. B. S. Haldane and Sewall Wright** (population
genetics), **T. Dobzhansky** (*Genetics and the Origin of Species*, 1937),
**Julian Huxley** (*Evolution: the Modern Synthesis*, 1942), **Ernst Mayr**,
**G. G. Simpson** and **G. L. Stebbins**.

| Factor | Role |
|---|---|
| **Gene mutation** | the ultimate source of new alleles |
| **Chromosomal mutation** | deletions, duplications, inversions, translocations; polyploidy |
| **Genetic recombination** | crossing over, independent assortment and fertilisation reshuffle alleles — the main source of variation in each generation |
| **Natural selection** | **differential reproduction**: genotypes leaving more fertile offspring increase |
| **Reproductive isolation** | stops gene flow between diverging populations, so they become new species |
| Accessory: gene flow, **genetic drift** (Sewall Wright effect; founder effect, bottleneck), hybridisation | change allele frequencies, most strongly in small populations |

In neo-Darwinism the **population** — not the individual — evolves, and evolution
is a change in **allele frequencies**.

**Hardy–Weinberg principle (1908).** In a large, randomly mating population with
no mutation, migration, selection or drift, allele and genotype frequencies stay
constant. For alleles A (frequency p) and a (frequency q):

$$ p + q = 1, \qquad p^2 + 2pq + q^2 = 1 $$

where $p^2$ = AA, $2pq$ = Aa (carriers) and $q^2$ = aa. Any departure shows that
evolution is happening.

::: example Carrier frequency from a recessive trait
**Problem.** In a population 16 % of people show a recessive trait. What fraction are heterozygous carriers?

**Solution.** $q^2 = 0.16$, so $q = 0.4$ and $p = 0.6$. Carriers $= 2pq = 2 \times 0.6 \times 0.4 = 0.48$, i.e. **48 %**. Shortcut: always take the square root of the *recessive phenotype* frequency first.
:::

**Types of natural selection**

| Type | Favours | Example |
|---|---|---|
| **Stabilising** | the average; removes both extremes | human birth weight (about 3–3.5 kg survives best) |
| **Directional** | one extreme; the mean shifts | **industrial melanism**, DDT-resistant mosquitoes, antibiotic-resistant bacteria |
| **Disruptive** | both extremes; the mean is removed | two beak sizes in some finch populations; can split a population in two |

**Industrial melanism** — the peppered moth ***Biston betularia*** in England.
Before the Industrial Revolution the light form, camouflaged on lichen-covered
bark, was common; after soot blackened the trees, birds ate the conspicuous
light moths and the dark (melanic) form rose to about 98 % near Manchester.
**H. B. D. Kettlewell** confirmed this by release–recapture in the 1950s, and
after the Clean Air Acts the light form returned. Selection did not *create* the
dark allele; it already existed and was selected.

**Isolation and speciation.** Pre-zygotic barriers (geographical, habitat,
seasonal, behavioural, mechanical, gametic) stop mating; post-zygotic barriers
act after it — hybrid inviability, **hybrid sterility** (the **mule**, horse ×
donkey) and hybrid breakdown. **Allopatric** speciation follows geographical
separation; **sympatric** speciation (common in plants by **polyploidy**) happens
in one place. **Adaptive radiation** — one ancestor giving many forms for many
niches — is shown by **Darwin's finches** and the Australian marsupials.

| | Lamarckism | Darwinism | Neo-Darwinism |
|---|---|---|---|
| Source of variation | needs and use/disuse | not explained | mutation and recombination |
| Inheritance | acquired characters inherited | not explained (pangenesis) | Mendelian genes; acquired characters **not** inherited |
| Mechanism | individuals change in response to need | natural selection of individuals | selection of genotypes; drift, gene flow, isolation |
| Unit that evolves | individual | individual | **population** (gene pool) |
| Giraffe's neck | stretching, inherited | long-necked variants survived droughts better | alleles for long necks increased in frequency |

## 1.4 Human evolution from Ramapithecus to modern man

**Classification of man**: Animalia → Chordata → Vertebrata → Mammalia →
order **Primates** → family **Hominidae** → *Homo* → *Homo sapiens*. Man and the
modern apes share a common ancestor; man did not descend from the chimpanzee.

**Trends in human evolution**: habitual **bipedal** walking with an S-shaped
spine, broad pelvis and arched foot; forward shift of the **foramen magnum**;
rising **cranial capacity**; reduction of brow ridges, jaws and **canines**;
appearance of the **chin** and a vertical forehead; a fully **opposable thumb**
and precision grip; loss of body hair; speech, tools, fire, culture.

```figure caption="Cranial capacity of the hominid stages (ranges as quoted in Nepali and Indian textbooks). Bipedalism (*Australopithecus*) came long before the big brain; capacity peaked in the Neanderthals and Cro-Magnon and is a little lower in modern man. *Ramapithecus* is known only from jaws and teeth."
import numpy as np
fig, ax = plt.subplots(figsize=(5.2, 2.9))
rows = [("$\\it{Australopithecus}$", "4–2 Mya", 400, 500),
        ("$\\it{Homo\\ habilis}$", "2.4–1.5 Mya", 650, 800),
        ("$\\it{Homo\\ erectus}$", "1.9–0.3 Mya", 800, 1100),
        ("Neanderthal man", "0.4–0.04 Mya", 1300, 1600),
        ("Cro-Magnon man", "40 000–10 000 y", 1550, 1650),
        ("modern man", "today", 1350, 1450)]
for i, (n, t, lo, hi) in enumerate(rows):
    y = len(rows) - 1 - i
    c = SERIES[0] if i < 3 else SERIES[1]
    ax.plot([lo, hi], [y, y], color=c, lw=9, solid_capstyle="butt")
    ax.text(hi + 25, y, f"{lo}–{hi} cm³   ({t})", va="center", fontsize=7.2, color=INK)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=7.6)
ax.set_xlim(300, 2350)
ax.set_xticks([400, 800, 1200, 1600])
ax.set_xlabel("cranial capacity (cm³)", fontsize=7.6)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color=GRID, lw=0.6)
ax.set_axisbelow(True)
```

| Stage | Time | Fossil site and discoverer | Cranial capacity | Diagnostic points |
|---|---|---|---|---|
| ***Dryopithecus*** ("oak ape") | Miocene, about 25–10 Mya | Africa, Europe, Asia | small, ape-sized | common ancestor of apes and man; knuckle-walker |
| ***Ramapithecus*** ("Rama's ape") | Miocene, about 14–9 Mya | **Siwalik Hills, India — G. E. Lewis (1932)**; in Nepal at **Tinau Khola near Butwal (Palpa), 1980**, a jaw fragment and teeth dated to about 9–11 Mya | not known (jaws and teeth only) | small canines, thick-enamelled molars; long called the **first hominid**; now referred to *Sivapithecus*, on the orang-utan line |
| ***Australopithecus*** ("southern ape", **ape-man**) | Pliocene, about 4–2 Mya | **Taung child, South Africa — Raymond Dart (1924)**; **"Lucy"** (*A. afarensis*), Hadar, Ethiopia — D. Johanson (1974) | **400–500 cm³** | **first clearly bipedal** hominid; ape-sized brain; used stones but made no tools; ate fruit |
| ***Homo habilis*** ("handy man") | 2.4–1.5 Mya | **Olduvai Gorge, Tanzania — Louis and Mary Leakey (1960)** | **650–800 cm³** | **first maker of stone tools** (Oldowan pebble choppers); first species of *Homo* |
| ***Homo erectus*** ("upright man") | 1.9 Mya – about 0.3 Mya | **Java man** (*Pithecanthropus erectus*) — **Eugène Dubois (1891)**; **Peking man** (*Sinanthropus pekinensis*), Zhoukoudian, China (1920s) | **800–1100 cm³** (Java ≈ 900) | **first to use fire**; hand axes; hunted, ate meat; first to leave Africa; heavy brow ridge, no chin |
| ***Homo neanderthalensis*** (Neanderthal man) | 0.4 Mya – 40 000 years ago | **Neander valley, near Düsseldorf, Germany (1856)**; Europe, Near East, Central Asia | **1300–1600 cm³** (≈ 1450) | **first to bury the dead**; wore hides; Mousterian flake tools; heavy brow ridge, weak chin; extinct side branch |
| ***Cro-Magnon man*** (*Homo sapiens fossilis*) | 40 000–10 000 years ago | **Cro-Magnon rock shelter, France (1868)** | **≈ 1600–1650 cm³** | tall, vertical forehead, prominent chin; **cave paintings** (Altamira, Lascaux); bone and blade tools; the most recent ancestor |
| ***Homo sapiens sapiens*** (modern man) | from about 0.3 Mya in Africa | worldwide | **1350–1450 cm³** | high rounded skull, chin, small teeth; language, **agriculture from about 10 000 years ago** |

::: memory The order of the hominids
**"Really Angry Hens Eat Nuts Calmly, Sapiently"** — *Ramapithecus* →
*Australopithecus* → *H. habilis* → *H. erectus* → Neanderthal → Cro-Magnon →
*H. sapiens sapiens*. Pair each with its "first": bipedal — tools — fire —
burial — paintings — agriculture.
:::

::: caution Three favourite traps
(1) **Fire** belongs to *H. erectus*, **tools** to *H. habilis* — not the
reverse. (2) The **Neanderthal** brain (≈ 1450 cm³) was *not smaller* than ours;
size alone is not intelligence. (3) *Ramapithecus* is no longer regarded as our
ancestor, but the paper still calls it the "first hominid" in standard palaeoanthropology
— answer in that language when the stem uses it.
:::

::: example Ordering cranial capacities along the hominin lineage
**Problem.** Arrange *Australopithecus africanus*, *Homo habilis*, *Homo erectus*, and *Homo neanderthalensis* in ascending order of average cranial capacity and identify which stage first used fire.

**Solution.** Cranial capacities rise steadily: *Australopithecus* ($\approx 450\text{–}500\text{ cm}^3$) $<$ *Homo habilis* ($\approx 650\text{–}800\text{ cm}^3$, first tool-maker) $<$ *Homo erectus* ($\approx 900\text{ cm}^3$, **first regular user of fire**) $<$ *Homo neanderthalensis* ($\approx 1{,}400\text{–}1{,}450\text{ cm}^3$).
:::

::: example Distinguishing homologous vs analogous organs in vertebrates
**Problem.** Classify (a) the forelimb of a bat and the flipper of a whale, and (b) the wing of a bat and the wing of a butterfly, stating the type of evolution each pair demonstrates.

**Solution.** (a) Bat forelimb and whale flipper share the pentadactyl bone plan (humerus, radius, ulna, carpals, metacarpals, phalanges) adapted to flight vs swimming: **homologous organs** showing **divergent evolution**. (b) Bat wing (skin fold over tetrapod bones) and butterfly wing (chitinous cuticular outgrowth) share function without common structural origin: **analogous organs** showing **convergent evolution**.
:::

```photogrid label="1.2" cols="2" ratio="1.2" caption="The human brain trebled in size. (a) A display of fossil hominid skulls: the faces shorten and the braincase grows from the australopithecines to Homo. (b) Typical brain volumes are about 450 cm3 for Australopithecus afarensis, 650 for Homo habilis, 900 for H. erectus, 1,450 for Neanderthals and 1,350 for modern H. sapiens (ranges overlap, so these are round averages). Modern man has 3 times the volume of A. afarensis; the Neanderthal brain was slightly larger than ours, so size alone does not measure intelligence. Ramapithecus is not on the line: it is now regarded as an ape, not a hominid."
@ photo id="ceezoo/hominid" cap="Fossil hominid skulls on display"
fit 1.2
focus 0.5 0.4
@ svg cap="Typical cranial capacity (cm3)"
sp = (("A. afarensis", 450, "3.5 Myr"), ("H. habilis", 650, "2 Myr"), ("H. erectus", 900, "1.5 Myr"), ("H. neanderthalensis", 1450, "0.1 Myr"), ("H. sapiens", 1350, "now"))
x = sp[-1][1] / sp[0][1]
assert abs(x - 3.0) < 1e-9
facts = dict(x="%.0f" % x)
f = Fig(300, 236)
f.text(150, 12, "Cranial capacity of five hominids", size=10.5, color=NAVY, bold=True)
for i, (n, v, t) in enumerate(sp):
    y = 28 + i * 37
    f.text(10, y + 2, "%s (%s)" % (n, t), size=10.5, color=SLATE, anchor="start")
    w = v / 1450 * 205
    f.box(10, y + 9, w, 18, fill=MINT if i != 4 else BLUE, stroke=TEAL if i != 4 else NAVY, r=2)
    f.text(10 + w + 6, y + 18, "%d" % v, size=10.5, color=TEAL if i != 4 else NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 224, "1,350 / 450 = 3 times", size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

**Origin of life**

| Fact | Value |
|---|---|
| Age of the Earth | ≈ 4.6 billion years |
| Oldest fossils | stromatolites (cyanobacteria), ≈ 3.5 billion years |
| Oparin / Haldane | 1924 (Russian) / 1929 (British); "hot dilute soup" = Haldane; coacervates = Oparin |
| Microspheres | Sidney Fox (proteinoids from heated amino acids) |
| Primitive atmosphere | CH₄, NH₃, H₂, H₂O (+ CO₂, N₂, HCN); reducing; **no O₂**, no ozone |
| First organisms | prokaryotic, anaerobic heterotrophs |
| Miller–Urey | 1953; CH₄ : NH₃ : H₂ = 2 : 2 : 1 (20, 20, 10 cm Hg) + steam; spark; 1 week; glycine, alanine, aspartic acid |
| Disproved spontaneous generation | Redi (1668), Spallanzani, Pasteur (swan-neck flask) |

**Evidences**

| Term | Key example |
|---|---|
| Homologous (divergent) | forelimbs of man, whale, bat, horse; *Bougainvillea* thorn and *Cucurbita* tendril |
| Analogous (convergent) | wings of insect and bird; eyes of octopus and man; sweet potato and potato |
| Vestigial in man | appendix, coccyx, nictitating membrane, ear muscles, wisdom teeth, body hair |
| Atavism | tail, dense hair, extra nipples, long canines in a baby |
| Connecting links | *Peripatus* (Annelida–Arthropoda), *Neopilina* (Annelida–Mollusca), *Balanoglossus* (non-chordate–chordate), lungfish (fish–amphibian), *Archaeopteryx* (reptile–bird), platypus and *Tachyglossus* (reptile–mammal), *Euglena* (plant–animal) |
| Living fossils | *Limulus*, *Latimeria*, *Sphenodon*, *Peripatus*, *Ginkgo* |
| Horse series | *Eohippus* (Eocene, 4/3 toes) → *Mesohippus* (3) → *Merychippus* (3, grazer) → *Pliohippus* (1, first one-toed) → *Equus*; North America |
| ¹⁴C half-life | 5730 years |
| Biogenetic law | Haeckel (1866), "ontogeny recapitulates phylogeny" |
| Precipitin test | Nuttall (1904) |

**Theories**

| Name | Fact |
|---|---|
| Lamarck | *Philosophie Zoologique* (1809); use and disuse; inheritance of acquired characters; giraffe |
| Weismann | tails of mice cut for 22 generations; germplasm theory (1892) |
| Darwin | HMS *Beagle* 1831–36; Galápagos finches; *Origin of Species* 24 Nov 1859; pangenesis |
| Wallace | Malay Archipelago; joint paper 1858 |
| Malthus / Lyell | population essay (1798) / *Principles of Geology* |
| Herbert Spencer | "survival of the fittest" |
| Hugo de Vries | mutation theory (1901), *Oenothera lamarckiana*, saltation |
| Modern synthesis | Fisher, Haldane, Wright, Dobzhansky (1937), Huxley (1942), Mayr, Simpson, Stebbins |
| Hardy–Weinberg | $p + q = 1$; $p^2 + 2pq + q^2 = 1$; large population, random mating, no mutation, migration, selection or drift |
| Industrial melanism | *Biston betularia*; directional selection; Kettlewell |
| Mule | hybrid sterility (post-zygotic isolation) |

**Human evolution**

| Hominid | Remember |
|---|---|
| *Ramapithecus* | Siwaliks (Lewis, 1932); Nepal: Tinau Khola, Butwal (1980) |
| *Australopithecus* | Dart (1924, Taung); "Lucy" (1974); bipedal; 400–500 cm³ |
| *H. habilis* | Leakeys, Olduvai (1960); first tools; 650–800 cm³ |
| *H. erectus* | Java man (Dubois, 1891), Peking man; first fire; 800–1100 cm³ |
| Neanderthal | Germany (1856); burial; 1300–1600 cm³ |
| Cro-Magnon | France (1868); cave art; ≈ 1650 cm³ |
| Modern man | 1350–1450 cm³; agriculture ≈ 10 000 years ago |

## Chapter summary

- Life arose by **chemical evolution** (Oparin 1924, Haldane 1929) in a **reducing** atmosphere of CH₄, NH₃, H₂ and water vapour with **no free O₂**, energised by UV and lightning: monomers → polymers → coacervates/microspheres → protocell → anaerobic heterotroph.
- **Miller–Urey (1953)** sparked CH₄, NH₃, H₂ (2 : 2 : 1) and steam for a week and obtained **amino acids** (glycine, alanine) — monomers, not life.
- **Homologous** organs (same origin, different use) show **divergent** evolution; **analogous** organs (different origin, same use) show **convergent** evolution; vestigial organs and atavism point to ancestors.
- **Connecting links** — *Peripatus*, *Neopilina*, *Balanoglossus*, lungfish, *Archaeopteryx*, platypus — and the **horse series** (*Eohippus* → *Equus*, toes 4 → 1) are the classic fossil and living evidence.
- **Haeckel's** biogenetic law (embryos), Nuttall's **precipitin test**, cytochrome c and the universal genetic code (biochemistry) complete the evidence.
- **Lamarck** (1809): use and disuse + inheritance of acquired characters — refuted by **Weismann** (22 generations of tailed mice; germplasm theory).
- **Darwin** (1859): overproduction, struggle, variation, **natural selection** ("survival of the fittest", Spencer); weakness — no theory of variation or heredity. **De Vries**: mutation, *Oenothera*.
- **Neo-Darwinism**: mutation + recombination + selection + isolation (+ drift, gene flow); the population evolves; Hardy–Weinberg $p^2 + 2pq + q^2 = 1$; *Biston betularia* is directional selection.
- Hominids: *Ramapithecus* (Tinau Khola, Butwal) → *Australopithecus* (bipedal, 400–500 cm³) → *H. habilis* (tools) → *H. erectus* (fire) → Neanderthal (burial) → Cro-Magnon (cave art) → *H. sapiens sapiens* (1350–1450 cm³).

## Practice questions

**Set A — Recall (25 questions)**

1. The phrase "hot dilute soup" for the primitive sea in which life began was used by
   (a) A. I. Oparin (b) J. B. S. Haldane (c) Stanley Miller (d) Sidney Fox
2. Which gas was absent from the primitive atmosphere according to the Oparin–Haldane theory?
   (a) methane (b) ammonia (c) hydrogen (d) free oxygen
3. Colloidal droplets of proteins and polysaccharides that Oparin regarded as forerunners of cells are called
   (a) coacervates (b) microspheres (c) liposomes (d) ribozymes
4. In the Miller–Urey apparatus the electric spark between the electrodes stood for
   (a) ultraviolet light (b) volcanic heat (c) rain (d) lightning
5. The two amino acids found in greatest amount in Miller's original experiment were
   (a) cysteine and methionine (b) tryptophan and tyrosine (c) glycine and alanine (d) lysine and histidine
6. The swan-necked flask experiment that finally disproved spontaneous generation was performed by
   (a) Francesco Redi (b) Lazzaro Spallanzani (c) J. B. S. Haldane (d) Louis Pasteur
7. The first living organisms on Earth were most probably
   (a) aerobic autotrophs (b) anaerobic heterotrophs (c) aerobic heterotrophs (d) photosynthetic eukaryotes
8. Which pair consists of analogous organs?
   (a) flipper of whale and wing of bat (b) wing of butterfly and wing of sparrow (c) thorn of *Bougainvillea* and tendril of *Cucurbita* (d) forelimb of horse and arm of man
9. Which of the following is a vestigial organ in man?
   (a) epiglottis (b) patella (c) vermiform appendix (d) uvula
10. The connecting link between Annelida and Arthropoda is
   (a) *Neopilina* (b) *Limulus* (c) *Balanoglossus* (d) *Peripatus*
11. *Archaeopteryx* is regarded as a connecting link between
   (a) reptiles and birds (b) amphibians and reptiles (c) reptiles and mammals (d) fishes and amphibians
12. The first one-toed horse in the evolutionary series of the horse was
   (a) *Eohippus* (b) *Mesohippus* (c) *Pliohippus* (d) *Merychippus*
13. "Ontogeny recapitulates phylogeny" was stated by
   (a) Karl von Baer (b) August Weismann (c) Hugo de Vries (d) Ernst Haeckel
14. The serum precipitin test used to show relationships between animals was introduced by
   (a) Nuttall (b) Kettlewell (c) Dobzhansky (d) Lyell
15. Lamarck published his theory of evolution in
   (a) *Origin of Species* (b) *Principles of Geology* (c) *Philosophie Zoologique* (d) *Das Keimplasma*
16. The phrase "survival of the fittest" was coined by
   (a) Charles Darwin (b) Herbert Spencer (c) Thomas Malthus (d) Alfred Russel Wallace
17. Hugo de Vries based his mutation theory on observations of
   (a) *Pisum sativum* (b) *Drosophila melanogaster* (c) *Oenothera lamarckiana* (d) *Biston betularia*
18. Weismann cut off the tails of mice for 22 generations to disprove
   (a) inheritance of acquired characters (b) natural selection (c) mutation theory (d) the biogenetic law
19. In Nepal a fossil jaw of *Ramapithecus* was found at
   (a) Kali Gandaki, Mustang (b) Karnali, Chisapani (c) Tinau Khola near Butwal (d) Arun valley, Sankhuwasabha
20. The first hominid to make stone tools was
   (a) *Homo habilis* (b) *Australopithecus* (c) *Homo erectus* (d) *Ramapithecus*
21. Fire was first used by
   (a) *Australopithecus* (b) *Homo habilis* (c) Cro-Magnon man (d) *Homo erectus*
22. The first hominids known to bury their dead were
   (a) Java men (b) Neanderthal men (c) Peking men (d) Australopithecines
23. The cave paintings of Altamira and Lascaux were made by
   (a) Neanderthal man (b) *Homo erectus* (c) Cro-Magnon man (d) *Homo habilis*
24. The cranial capacity of modern man is about
   (a) 1350–1450 cm³ (b) 650–800 cm³ (c) 900–1100 cm³ (d) 1800–2000 cm³
25. "Lucy", a 3.2-million-year-old skeleton from Ethiopia, belongs to
   (a) *Homo habilis* (b) *Australopithecus afarensis* (c) *Homo erectus* (d) *Ramapithecus*

::: note Answers and explanations — Set A
**1.** (b) — Haldane (1929) called the primitive ocean a "hot dilute soup" of organic molecules; Oparin's word was *coacervate*.
**2.** (d) — the primitive atmosphere was reducing: CH₄, NH₃, H₂ and water vapour. Free O₂ came later, from photosynthesis.
**3.** (a) — coacervates are Oparin's; microspheres (option b) are Sidney Fox's proteinoid spheres.
**4.** (d) — the spark supplied the energy of lightning; the boiling water stood for the sea and the condenser for rain. (The gases were CH₄ : NH₃ : H₂ = 2 : 2 : 1 by pressure.)
**5.** (c) — glycine and alanine were the most abundant. No sulphur gas was used, so cysteine and methionine (a) could not form.
**6.** (d) — Pasteur's swan-necked flask let air in but trapped dust and microbes in the bend; the broth stayed sterile.
**7.** (b) — with no O₂ and a "soup" of organic food, the first cells were anaerobic heterotrophs; autotrophs came later.
**8.** (b) — a butterfly wing is a fold of cuticle, a sparrow wing a feathered forelimb: same function, different origin. The others are homologous.
**9.** (c) — the vermiform appendix is the vestige of a large herbivore caecum. Epiglottis, patella and uvula all work.
**10.** (d) — *Peripatus* has nephridia and unjointed legs (annelid) with tracheae and a haemocoel (arthropod). *Limulus* is a living fossil, not this link.
**11.** (a) — feathers and wings of a bird with teeth, a long bony tail and clawed fingers of a reptile.
**12.** (c) — *Pliohippus* (Pliocene) was the first one-toed horse; *Merychippus* still had three toes.
**13.** (d) — Haeckel's biogenetic law (1866). Von Baer said embryos resemble ancestral *embryos*, not adults.
**14.** (a) — G. H. F. Nuttall (1904) showed anti-human serum reacts most strongly with ape sera.
**15.** (c) — *Philosophie Zoologique*, 1809. *Das Keimplasma* is Weismann's.
**16.** (b) — Herbert Spencer coined it; Darwin adopted it in later editions of the *Origin*.
**17.** (c) — the evening primrose *Oenothera lamarckiana*; its sudden new forms suggested evolution by jumps.
**18.** (a) — the mice kept being born with normal tails: a mutilation acquired in life is not inherited.
**19.** (c) — Tinau Khola near Butwal (Palpa) — jaw and teeth found in 1980 and dated to roughly 9–11 million years.
**20.** (a) — *H. habilis*, "handy man", made the Oldowan pebble tools. *Australopithecus* used stones but did not shape them.
**21.** (d) — *H. erectus* (Peking man's hearths) first used fire.
**22.** (b) — Neanderthals buried their dead with flowers and tools — the first evidence of ritual.
**23.** (c) — Cro-Magnon man, *Homo sapiens fossilis*, painted the caves.
**24.** (a) — 1350–1450 cm³; 650–800 is *H. habilis*, 900–1100 is *H. erectus*.
**25.** (b) — Lucy (Hadar, Ethiopia, 1974) was a bipedal *Australopithecus afarensis* with an ape-sized brain.
:::

**Set B — Understanding (15 questions)**

1. Chemical evolution of life cannot occur on Earth today mainly because
   (a) the Earth's temperature is too low (b) free O₂ and microbes destroy organic molecules as fast as they form (c) lightning no longer occurs (d) the oceans are too salty
2. The Miller–Urey experiment demonstrated that
   (a) living cells can arise from inorganic matter (b) proteins form spontaneously in water (c) amino acids can form from simple gases under primitive-Earth conditions (d) oxygen is essential for the synthesis of amino acids
3. The thorn of *Bougainvillea* and the tendril of *Cucurbita* are homologous because both are
   (a) modified leaves (b) modified stems (c) used for climbing (d) modified roots
4. The eye of an octopus and the eye of a mammal are an example of
   (a) convergent evolution (b) divergent evolution (c) homology (d) atavism
5. Pharyngeal gill pouches in the human embryo are best interpreted as evidence that
   (a) the human embryo passes through an adult fish stage (b) the human embryo breathes through gills (c) man evolved from modern fishes (d) man and fishes share a common ancestor
6. Which explanation of the long neck of the giraffe is Darwinian?
   (a) longer-necked variants already existed and left more offspring (b) giraffes stretched their necks and passed the stretch on (c) a single mutation suddenly produced a long neck (d) an internal vital force lengthened the neck
7. The chief weakness of Darwin's theory was that it
   (a) ignored the struggle for existence (b) could not explain the origin and inheritance of variations (c) rejected natural selection (d) assumed the Earth was young
8. Neo-Darwinism differs from Darwinism chiefly in
   (a) rejecting natural selection (b) accepting the inheritance of acquired characters (c) explaining variation by mutation and recombination in populations (d) proposing that species are fixed
9. During industrialisation in England the dark form of *Biston betularia* increased because
   (a) soot darkened the moths' wings directly (b) the dark moths were less visible to birds on blackened bark (c) light moths mutated into dark ones (d) dark moths needed less food
10. Which of the following does NOT disturb Hardy–Weinberg equilibrium?
   (a) gene flow (b) genetic drift (c) random mating (d) natural selection
11. The mule is sterile. This is an example of
   (a) post-zygotic isolation (b) geographical isolation (c) behavioural isolation (d) mechanical isolation
12. *Ramapithecus* is no longer placed on the direct human line because
   (a) its fossils proved to be fakes (b) it lived after *Homo erectus* (c) it was merged with *Sivapithecus* of the orang-utan line (d) it had a larger brain than man
13. Which trend is NOT part of human evolution?
   (a) increase in cranial capacity (b) reduction of brow ridges (c) development of a chin (d) enlargement of the canine teeth
14. Arrange in the order of evolution: 1 *Homo erectus*, 2 *Australopithecus*, 3 *Homo sapiens*, 4 *Homo habilis*.
   (a) 2, 4, 1, 3 (b) 4, 2, 1, 3 (c) 2, 1, 4, 3 (d) 1, 4, 2, 3
15. The trochophore larva shared by annelids and molluscs is an evidence of evolution from
   (a) palaeontology (b) embryology (c) biochemistry (d) biogeography

::: note Answers and explanations — Set B
**1.** (b) — O₂ oxidises organic molecules and microbes eat them; lightning (c) still occurs, so that is not the reason.
**2.** (c) — Miller made monomers (amino acids) from CH₄, NH₃, H₂ and steam under primitive-Earth conditions. No cells or proteins appeared, and O₂ was deliberately absent.
**3.** (b) — both are modified axillary branches of the stem, though one defends and the other climbs.
**4.** (a) — they arose independently in molluscs and vertebrates (the octopus retina has no blind spot): analogous organs, convergent evolution.
**5.** (d) — embryos resemble ancestral *embryos*; the pouches never become working gills (option a is Haeckel's overstatement).
**6.** (a) — Darwin: the variation exists first and selection keeps it. (b) is Lamarck, (c) de Vries.
**7.** (b) — Darwin knew nothing of genes; his pangenesis guess was wrong.
**8.** (c) — the modern synthesis adds genetics: mutation and recombination supply the variation, and evolution is a change of allele frequencies in a population.
**9.** (b) — birds ate the conspicuous light moths; the dark allele already existed and was selected (directional selection). Soot does not change genes (a).
**10.** (c) — random mating is one of the *conditions* of equilibrium; gene flow, drift and selection all change allele frequencies.
**11.** (a) — the hybrid zygote forms and grows but is sterile: a post-zygotic barrier.
**12.** (c) — the Pakistani *Sivapithecus* face (1980s) matched the orang-utan; *Ramapithecus* was merged with it.
**13.** (d) — canines became smaller in the human line; the other three are true trends.
**14.** (a) — *Australopithecus* (ape-man) → *H. habilis* (tools) → *H. erectus* (fire) → *H. sapiens*.
**15.** (b) — similar larvae in different phyla are embryological evidence of common ancestry.
:::

**Set C — Application (10 questions)**

1. In a population in Hardy–Weinberg equilibrium, 9 % of individuals show a recessive phenotype. The percentage of heterozygous carriers is
   (a) 21 % (b) 49 % (c) 42 % (d) 30 %
2. In a village of 1000 people in equilibrium, 160 show an autosomal recessive trait. How many are expected to be heterozygous?
   (a) 480 (b) 360 (c) 240 (d) 640
3. A fossil bone contains one-eighth of the ¹⁴C found in living bone. Taking the half-life of ¹⁴C as 5730 years, its age is about
   (a) 11 460 years (b) 45 840 years (c) 22 920 years (d) 17 190 years
4. A fossil skull with a cranial capacity of about 700 cm³ is found in East Africa beside crude pebble choppers. It most probably belongs to
   (a) *Homo erectus* (b) *Homo habilis* (c) *Australopithecus* (d) Neanderthal man
5. A newly discovered animal has a segmented body, nephridia and unjointed legs, but also breathes by tracheae and has a haemocoel. It would be regarded as a link between
   (a) Annelida and Mollusca (b) Mollusca and Arthropoda (c) Annelida and Arthropoda (d) Arthropoda and Echinodermata
6. A bacterium becomes resistant after an antibiotic is used widely. In neo-Darwinian terms the best explanation is that
   (a) resistant mutants already present survived and multiplied (b) bacteria became resistant because they needed to (c) the antibiotic caused every bacterium to change (d) resistance acquired by use was inherited
7. In a hospital record, babies of very low and very high birth weight had the highest death rates. This shows
   (a) directional selection (b) disruptive selection (c) genetic drift (d) stabilising selection
8. Comparing one protein, species P differs from man at 1 amino acid, Q at 12 and R at 44. The correct conclusion is that
   (a) P is most distantly related to man (b) R is most distantly related to man (c) Q is most closely related to man (d) all three are equally related to man
9. Whales have small pelvic bones buried in the body wall. This is best explained by
   (a) use and disuse in the lifetime of each whale (b) recent independent origin of the pelvis (c) descent from four-legged land ancestors (d) convergent evolution with fishes
10. Blind fish living in dark caves are explained by a student as "they stopped using their eyes, so their young were born blind". The student is applying
   (a) Darwinism (b) mutation theory (c) the biogenetic law (d) Lamarckism

::: note Answers and explanations — Set C
**1.** (c) — $q^2 = 0.09$, $q = 0.3$, $p = 0.7$; $2pq = 2 \times 0.7 \times 0.3 = 0.42$ = 42 %. Option (b) is $p^2$.
**2.** (a) — $q^2 = 0.16$, $q = 0.4$, $p = 0.6$; $2pq = 0.48$; 0.48 × 1000 = 480. (b) 360 is $p^2$ × 1000.
**3.** (d) — 1/8 = (1/2)³, three half-lives: 3 × 5730 = 17 190 years. (a) is two half-lives.
**4.** (b) — 650–800 cm³ with Oldowan pebble tools is *H. habilis*; *Australopithecus* had 400–500 cm³ and made no tools.
**5.** (c) — exactly the mix seen in *Peripatus*, the Annelida–Arthropoda link.
**6.** (a) — mutations for resistance arise at random, before exposure (Lederberg's replica plating); the antibiotic only selects them. (b) and (d) are Lamarckian.
**7.** (d) — the intermediate weight is favoured and both extremes removed: stabilising selection.
**8.** (b) — the more amino-acid differences, the longer ago the lines separated; R (44) is most distant, P (1) closest.
**9.** (c) — vestigial pelvic bones are the remains of hind limbs of land-living ancestors; use and disuse in one lifetime (a) is not inherited.
**10.** (d) — "lost by disuse and inherited" is Lamarck's use-and-disuse with inheritance of acquired characters.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe the Oparin–Haldane theory of the origin of life and the Miller–Urey experiment that supports it. <span class="marks">[10]</span>
2. Describe the evidences of organic evolution (morphological, anatomical, palaeontological, embryological and biochemical). <span class="marks">[10]</span>
3. Compare Lamarckism, Darwinism and Neo-Darwinism and explain how natural selection works. <span class="marks">[10]</span>

```photogrid label="1.H" cols="4" ratio="1.25" caption="Evidence for evolution. (a) Darwin's finches show adaptive radiation of beak shape. (b) Horse fossils show a steady change from a small many-toed animal to the one-toed Equus. (c) Archaeopteryx is a connecting link between reptiles and birds. (d) The skulls of hominids show a growing brain case."
@ photo id="bio11/finches-gould" cap="(a) Finches"
fit 1.25
focus 0.5 0.5
@ photo id="bio11/horse-evo" cap="(b) Horse series"
fit 1.25
focus 0.5 0.5
@ photo id="ceezoo/archaeopteryx" cap="(c) Archaeopteryx"
fit 1.25
focus 0.5 0.5
@ photo id="ceezoo/hominid" cap="(d) Hominid skulls"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Oparin–Haldane theory and the Miller–Urey experiment (10 marks)

**Introduction.** Earth is about 4.6 billion years old and the first cells appeared about 3.5 billion years ago. Early ideas such as special creation, spontaneous generation (disproved by Redi and Pasteur) and panspermia (life arrived from space, Arrhenius) did not explain how life began. The **chemical evolution theory** of A. I. Oparin (1924) and J. B. S. Haldane (1929) says that life arose slowly from non-living matter under the conditions of the young Earth.

**Steps of the Oparin–Haldane theory.**

1. **Primitive atmosphere:** it was **reducing**, with methane (CH₄), ammonia (NH₃), hydrogen (H₂) and water vapour, but no free oxygen.
2. **Energy sources:** ultraviolet rays, lightning, volcanic heat and cosmic rays drove chemical reactions.
3. **Simple organic molecules:** the gases reacted to form amino acids, simple sugars, fatty acids and nitrogen bases.
4. **Hot dilute soup:** rain carried these molecules into the oceans, which became a "primordial soup".
5. **Macromolecules:** monomers joined to form proteins, polysaccharides and nucleic acids.
6. **Coacervates (protobionts):** droplets of macromolecules with a membrane-like boundary could take in material and divide. Sidney Fox made similar **proteinoid microspheres**.
7. **First cell:** a heterotrophic, anaerobic prokaryote that fed on the soup.
8. **Autotrophs and oxygen:** when food ran short, photosynthetic cells evolved, released oxygen, and later gave rise to aerobic life.

**Miller–Urey experiment (1953).** Stanley Miller and Harold Urey built a closed glass apparatus. One flask held water that was boiled to make vapour. A second flask held the gases CH₄, NH₃ and H₂ in which **high-voltage electric sparks** imitated lightning. A condenser cooled the gas, and the liquid collected in a trap and was returned to the boiling flask, so the cycle ran continuously for about a week. The water turned brown-red, and chromatography showed **amino acids** such as glycine, alanine, aspartic acid and glutamic acid, with urea and simple acids.

| Part of apparatus | Imitates | Result |
|---|---|---|
| Boiling flask | Ocean and evaporation | Water vapour to the gas flask |
| Gas flask with sparks | Atmosphere with lightning | Organic molecules formed |
| Condenser and trap | Rain into the sea | Amino acids collected |

**Importance and limits.** The experiment gave the first laboratory proof that organic molecules form from inorganic ones. Later work (Oro, 1960) made adenine from hydrogen cyanide. Today many scientists think the early air held more CO₂ and N₂, but similar molecules still form near volcanoes and deep-sea vents.

**Conclusion.** Chemical evolution, supported by the Miller–Urey experiment, is the most accepted explanation of how life began on Earth.

### Model answer D2: Evidences of organic evolution (10 marks)

**Introduction.** **Organic evolution** is the gradual change of living things over many generations. Its proof comes from several branches of biology.

**1. Morphological and anatomical evidence.**

1. **Homologous organs** have the same basic structure but different functions: the forelimb of a human, cat, whale and bat has the same bones (humerus, radius, ulna, carpals, metacarpals, phalanges). They show **divergent evolution** from a common ancestor.
2. **Analogous organs** have different structure but the same function, such as the wing of a bird and of an insect. They show **convergent evolution**.
3. **Vestigial organs** are reduced and almost useless: the appendix, wisdom teeth, coccyx and ear muscles of man.
4. **Connecting links:** *Archaeopteryx* (reptile and bird), *Peripatus* (annelid and arthropod), the lungfish and the duck-billed platypus.

**2. Palaeontological evidence.** **Fossils** in rock layers show that older strata hold simpler forms. The age is found by **radiocarbon dating** (half-life of C-14 = 5,730 years). A fossil with ⅛ of the C-14 of a living organism has passed through three half-lives, so its age is 3 × 5,730 = **17,190 years**. The **horse** series (Eohippus → Mesohippus → Merychippus → Pliohippus → Equus) shows growth in size, reduction of toes from four to one, and longer, stronger teeth.

**3. Embryological evidence.** Embryos of fish, tortoise, chick and man look alike in early stages and have **gill slits** and a tail. Von Baer said that general features appear before special ones. Haeckel's **biogenetic law** ("ontogeny repeats phylogeny") is true only in a loose way.

**4. Biochemical evidence.** All organisms use DNA, the same genetic code, ATP and the same 20 amino acids. The amino-acid sequence of **cytochrome c** differs by only a few residues between man and chimpanzee but by many between man and yeast, so the smaller the difference, the closer the relationship.

**5. Biogeographical evidence.** Darwin's finches on the Galápagos have different beaks for different foods, though they came from one ancestor.

| Evidence | Example | What it shows |
|---|---|---|
| Homology | Forelimbs of vertebrates | Common ancestry |
| Fossils | Horse, Archaeopteryx | Gradual change |
| Embryology | Gill slits in all embryos | Shared ancestors |
| Biochemistry | Cytochrome c | Degree of relationship |

**Conclusion.** Evidence from anatomy, fossils, embryos and molecules all points to descent with modification from common ancestors.

### Model answer D3: Lamarckism, Darwinism and Neo-Darwinism (10 marks)

**Introduction.** Three major theories try to explain **how** evolution happens.

**Lamarckism (1809).** In *Philosophie Zoologique* Lamarck proposed (a) the internal urge to grow, (b) **use and disuse** of organs and (c) **inheritance of acquired characters**. Example: the giraffe stretched its neck to reach high leaves, and its offspring inherited the longer neck. **Criticism:** Weismann cut the tails of mice for 22 generations and the young still had normal tails. Acquired changes of body cells are not passed on, as only the germ cells carry heredity.

**Darwinism (1859).** In *The Origin of Species* Darwin (with Wallace) gave five ideas:

1. **Overproduction:** more young are born than can survive.
2. **Struggle for existence:** they compete for food, space and mates.
3. **Variation:** no two individuals are exactly alike.
4. **Natural selection:** the fittest survive and breed.
5. **Inheritance and speciation:** useful variations pass on, and over many generations new species arise.

Example: in the industrial areas of England the dark form of the peppered moth *Biston betularia* became common because birds ate the pale moths on sooty trees. **Limits:** Darwin could not explain how variations arise or are inherited.

**Neo-Darwinism (modern synthetic theory).** Dobzhansky, Huxley, Mayr and Simpson joined Darwin's idea with genetics. It says that variation arises by **mutation** and **recombination**, and that evolution is a change in gene frequency caused by mutation, gene flow, genetic drift, natural selection and reproductive isolation. By the Hardy–Weinberg law, p² + 2pq + q² = 1. If q² = 0.04 then q = 0.2, p = 0.8, and carriers (2pq) = 2 × 0.8 × 0.2 = **0.32**.

| Point | Lamarckism | Darwinism | Neo-Darwinism |
|---|---|---|---|
| Cause of change | Use and disuse | Natural selection | Mutation, selection, drift, isolation |
| Acquired traits | Inherited | Not discussed | Not inherited |
| Source of variation | Environment | Unexplained | Mutation and recombination |
| Basis | Organs | Individuals | Gene frequency |

**Conclusion.** Lamarck started the idea of gradual change, Darwin explained it through natural selection, and Neo-Darwinism completed it with genetics.

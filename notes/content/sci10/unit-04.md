---
subject: Science and Technology
grade: 10
unit: 4
title: Heredity
hours: 0
area: Science and Technology
---

Why do you have your mother's eyes or your father's curly hair? Why do two children of the same parents look alike, but not exactly the same? The passing of characters from parents to their children is called **heredity**, and the study of heredity and variation is called **genetics**. Genetics began in a monastery garden with an Austrian monk who grew peas. This unit explains his experiments and laws, how chromosomes and genes carry the characters, how the sex of a child is decided, and some diseases that run in families.

::: key What the SEE paper expects from this unit
Most marks come from crosses: a monohybrid cross with the 3 : 1 phenotypic ratio and a dihybrid cross with the 9 : 3 : 3 : 1 ratio, drawn with a Punnett square (4 marks). Also expect definitions (heredity, gene, allele, dominant, recessive, genotype, phenotype), the XX-XY mechanism of sex determination, and the cause of Down's syndrome, haemophilia and colour blindness.
:::

## 4.1 Mendel's experiments and laws

### Heredity and variation

::: definition Heredity
**Heredity** is the transmission of characters (traits) from parents to offspring through genes.
:::

**Variation** is the difference between individuals of the same species, even between brothers and sisters. Variation arises because the offspring receive a mixture of genes from two parents and because of changes in genes called mutations. Variation helps a species to survive when the environment changes.

### Gregor Johann Mendel

**Gregor Johann Mendel** (1822–1884) was an Austrian monk. Between 1856 and 1863 he did experiments on the garden pea (*Pisum sativum*) in the garden of his monastery in Brno (now in the Czech Republic) and published them in 1866. His work was not noticed until 1900, when three scientists (de Vries, Correns, Tschermak) found his results independently. Mendel is called the **father of genetics**.

**Why did Mendel choose the pea plant?**

- It has clear, contrasting characters (tall or dwarf, round or wrinkled seed).
- It is self-pollinating, so pure lines (true-breeding plants) are easy to get, but it can also be cross-pollinated by hand.
- Its life cycle is short and it produces many seeds.
- It is easy to grow and the flowers are large enough to handle.

Mendel studied **seven pairs of contrasting characters**:

| Character | Dominant form | Recessive form |
|---|---|---|
| Height of stem | Tall | Dwarf |
| Seed shape | Round | Wrinkled |
| Seed colour | Yellow | Green |
| Pod shape | Inflated (full) | Constricted |
| Pod colour | Green | Yellow |
| Flower colour | Violet (purple) | White |
| Flower position | Axial (along the stem) | Terminal (at the tip) |

### Terms used in genetics

| Term | Meaning |
|---|---|
| Character / trait | A feature that can be inherited, e.g. height |
| Gene | A segment of DNA on a chromosome that controls a character |
| Allele | One of the alternative forms of a gene (T for tall and t for dwarf) |
| Dominant | An allele that shows its effect even when only one copy is present (capital letter) |
| Recessive | An allele that shows its effect only when two copies are present (small letter) |
| Homozygous (pure) | Two identical alleles: TT or tt |
| Heterozygous (hybrid) | Two different alleles: Tt |
| Genotype | The genetic make-up of an organism (TT, Tt, tt) |
| Phenotype | The visible character (tall, dwarf) |
| Hybrid | Offspring of parents that differ in one or more characters |
| P generation | Parental generation |
| F₁ and F₂ | First and second filial generation (children and grandchildren) |

### Monohybrid cross

A **monohybrid cross** studies the inheritance of **one** pair of contrasting characters.

Mendel crossed a pure **tall** plant (TT) with a pure **dwarf** plant (tt).

- The **F₁** generation: all plants were **tall**. The dwarf character seemed to have disappeared.
- He then let the F₁ plants self-pollinate. The **F₂** generation had both **tall and dwarf** plants in the ratio **3 : 1**: about 787 tall and 277 dwarf in his counts.

So the dwarf character was not lost; it was hidden in F₁.

Explanation: A pure tall plant (TT) makes only T gametes; a pure dwarf (tt) makes only t gametes. Every F₁ plant is Tt, and shows tall because T is dominant. Tt plants make two kinds of gametes, T and t, in equal numbers. They combine at random:

| Gametes | T | t |
|---|---|---|
| **T** | TT (tall) | Tt (tall) |
| **t** | Tt (tall) | tt (dwarf) |

- **Phenotypic ratio** F₂: 3 tall : 1 dwarf.
- **Genotypic ratio** F₂: 1 TT : 2 Tt : 1 tt.

```figure caption="Monohybrid cross between pure tall (TT) and pure dwarf (tt) pea plants, giving the F1 and F2 generations."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(4.8,4.0))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,10)
def bx(x,y,t,w=3.4,fc="#eaf1ff",fs=8):
    ax.add_patch(FancyBboxPatch((x-w/2,y-0.4),w,0.8,boxstyle="round,pad=0.04",fc=fc,ec=ACCENT,lw=1))
    ax.text(x,y,t,ha='center',va='center',fontsize=fs,color=INK)
def ar(x1,y1,x2,y2):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color=INK,lw=1))
bx(3,9.3,"P: TT (tall)"); bx(9,9.3,"P: tt (dwarf)")
bx(3,8.0,"Gametes: T  T",w=2.8,fc="white"); bx(9,8.0,"Gametes: t  t",w=2.8,fc="white")
ar(3,8.9,3,8.45); ar(9,8.9,9,8.45)
ar(3,7.55,5.2,6.95); ar(9,7.55,6.8,6.95)
bx(6,6.5,"F1: all Tt (tall)",w=4.0,fc="#dbe8ff")
ax.text(9.6,5.7,"self-pollination",fontsize=7.5,color=MUTED,ha='center',va='center')
ar(6,6.05,6,5.45)
bx(6,5.0,"Gametes of F1:  T  or  t",w=4.6,fc="white")
ar(6,4.55,6,3.95)
cells=[("TT","tall"),("Tt","tall"),("Tt","tall"),("tt","dwarf")]
for i,(g,p) in enumerate(cells):
    x=1.9+i*2.7
    bx(x,3.4,g+"\n"+p,w=2.3,fc="#dbe8ff" if p=="tall" else "#ffe8d6",fs=8)
ax.text(6,2.0,"F2 phenotypes: 3 tall : 1 dwarf",ha='center',fontsize=8.5,color=INK,fontweight='bold')
ax.text(6,1.2,"F2 genotypes: 1 TT : 2 Tt : 1 tt",ha='center',fontsize=8.5,color=INK)
```

::: example Worked example 4.1 (monohybrid cross with round and wrinkled seeds)
**Problem.** A pea plant heterozygous for round seeds (Rr) is self-pollinated, and 400 seeds are produced. Round (R) is dominant over wrinkled (r). How many seeds are expected to be round and how many wrinkled?

**Solution.** Gametes of Rr: R and r. Punnett square: RR, Rr, Rr, rr.

Phenotypic ratio = 3 round : 1 wrinkled.

Round seeds = 3/4 × 400 = **300**. Wrinkled seeds = 1/4 × 400 = **100**.

Genotypes: 100 RR, 200 Rr, 100 rr.
:::

### Test cross

A tall plant may be TT or Tt. To find its genotype, it is crossed with a recessive (dwarf, tt) plant. This is the **test cross**.

- If **all** offspring are tall, the plant tested was **TT** (homozygous).
- If **half tall and half dwarf** (1 : 1), the plant was **Tt** (heterozygous).

### Dihybrid cross

A **dihybrid cross** studies the inheritance of **two** pairs of contrasting characters at the same time.

Mendel crossed a pure plant with **round yellow** seeds (RRYY) with a pure plant with **wrinkled green** seeds (rryy).

- **F₁:** all plants had round yellow seeds (RrYy).
- **F₂** (by self-pollination of F₁): four kinds of seeds in the ratio **9 : 3 : 3 : 1**.

Each F₁ plant (RrYy) makes four kinds of gametes in equal numbers: **RY, Ry, rY, ry**. The 16 combinations are shown in the Punnett square:

| | RY | Ry | rY | ry |
|---|---|---|---|---|
| **RY** | RRYY | RRYy | RrYY | RrYy |
| **Ry** | RRYy | RRyy | RrYy | Rryy |
| **rY** | RrYY | RrYy | rrYY | rrYy |
| **ry** | RrYy | Rryy | rrYy | rryy |

Counting the phenotypes:

| Phenotype | Number of boxes |
|---|---|
| Round yellow | 9 |
| Round green | 3 |
| Wrinkled yellow | 3 |
| Wrinkled green | 1 |

Two **new combinations** (round green and wrinkled yellow) appeared that were not in either parent. This shows that the two characters are inherited independently.

```figure caption="Dihybrid F2 ratio 9 : 3 : 3 : 1. Each square is one of the 16 boxes in the Punnett square, coloured by phenotype."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,3.0))
ax.set_aspect('equal'); ax.axis('off')
g=["RY","Ry","rY","ry"]
shade={(True,True):"#f3c34b",(True,False):"#8fcf7a",(False,True):"#f7e08a",(False,False):"#b9d98a"}
for i,a in enumerate(g):
    ax.text(i+0.5,4.3,a,ha='center',va='center',fontsize=8,color=INK)
    ax.text(-0.35,3.5-i,a,ha='center',va='center',fontsize=8,color=INK)
    for j,b in enumerate(g):
        r = a[0]=="R" or b[0]=="R"
        y = a[1]=="Y" or b[1]=="Y"
        ax.add_patch(Rectangle((i,3-j),1,1,fc=shade[(r,y)],ec="white",lw=1.5))
        s = "".join(sorted([a[0],b[0]],key=lambda c:c.islower())) + "".join(sorted([a[1],b[1]],key=lambda c:c.islower()))
        ax.text(i+0.5,3-j+0.5,s,ha='center',va='center',fontsize=6.5,color=INK)
ax.set_xlim(-0.8,9.2); ax.set_ylim(-0.4,4.8)
labs=[("#f3c34b","Round yellow: 9"),("#8fcf7a","Round green: 3"),("#f7e08a","Wrinkled yellow: 3"),("#b9d98a","Wrinkled green: 1")]
for k,(c,t) in enumerate(labs):
    ax.add_patch(Rectangle((4.8,3.1-k*0.8),0.5,0.5,fc=c,ec="white"))
    ax.text(5.5,3.35-k*0.8,t,va='center',fontsize=8,color=INK)
```

::: example Worked example 4.2 (dihybrid cross numbers)
**Problem.** In a dihybrid cross RrYy × RrYy, 1,600 seeds are produced. How many are expected to be (a) round yellow, (b) wrinkled green, (c) round green?

**Solution.** Ratio 9 : 3 : 3 : 1, total 16 parts. One part = 1,600 / 16 = 100 seeds.

(a) Round yellow = 9 × 100 = **900**.

(b) Wrinkled green = 1 × 100 = **100**.

(c) Round green = 3 × 100 = **300**.

Check: 900 + 300 + 300 + 100 = 1,600.
:::

### Mendel's laws of inheritance

1. **Law of dominance.** When two pure parents with contrasting characters are crossed, only one character, the **dominant** one, appears in F₁. The other, the **recessive**, is hidden.
2. **Law of segregation (law of purity of gametes).** The two alleles of a gene separate (segregate) from each other during the formation of gametes, so each gamete carries only **one** allele of each gene.
3. **Law of independent assortment.** When two or more pairs of characters are inherited together, the alleles of each pair separate **independently** of those of the other pair. This gives new combinations such as round green and wrinkled yellow.

::: caution Common mistake
The 3 : 1 ratio is the phenotypic ratio; the genotypic ratio is 1 : 2 : 1. Many students write the wrong one. Also, dominant does not mean "more common" or "stronger"; it only means that the character shows when the allele is present with a recessive one.
:::

### Incomplete dominance

Sometimes neither allele is fully dominant. In the **four o'clock plant** (*Mirabilis jalapa*), a cross between red (RR) and white (rr) flowers gives **pink** (Rr) flowers in F₁. In F₂ the ratio is **1 red : 2 pink : 1 white**. This is **incomplete dominance**, and here the phenotypic and genotypic ratios are the same.

## 4.2 Chromosomes and genes

### Where are genes found?

Every cell of a living thing has a **nucleus**. In the nucleus there are thread-like structures called **chromosomes**. They are visible as thick rods only when the cell is dividing. A chromosome is made of **DNA** (deoxyribonucleic acid) wound round proteins. A **gene** is a small section of DNA that has the instruction for making one protein, and so controls one character.

Hierarchy: **cell → nucleus → chromosome → DNA → gene**.

### Chromosome number

Each species has a fixed number of chromosomes. They occur in pairs (one from each parent), called **homologous chromosomes**.

| Organism | Number of chromosomes in body cell (2n) |
|---|---|
| Human | 46 (23 pairs) |
| Pea | 14 |
| Maize | 20 |
| Rice | 24 |
| Housefly | 12 |
| Dog | 78 |
| Chimpanzee | 48 |

The number of chromosomes does not show the complexity of an organism.

Body cells have **two sets** of chromosomes (**diploid**, 2n). Gametes (sperm and egg) have **one set** (**haploid**, n). In humans, 2n = 46 and n = 23. When a sperm (n = 23) fuses with an egg (n = 23), the zygote has 2n = 46 again.

In human beings, the 46 chromosomes are 22 pairs of **autosomes** (control body characters) and one pair of **sex chromosomes** (XX in female, XY in male).

### Chromosomal basis of Mendel's laws

Mendel's "factors" are the genes on chromosomes. The segregation of alleles is explained by the separation of the homologous chromosomes in **meiosis**, the cell division that makes gametes. The independent assortment of two characters is explained by the random way different pairs of chromosomes line up and separate. Walter Sutton and Theodor Boveri (1902) put forward this **chromosome theory of inheritance**.

### Cell divisions: mitosis and meiosis

| Mitosis | Meiosis |
|---|---|
| In body (somatic) cells | In reproductive organs, to make gametes |
| One division | Two divisions |
| 2 daughter cells | 4 daughter cells |
| Chromosome number stays the same (2n → 2n) | Number is halved (2n → n) |
| Daughter cells identical to the parent | Daughter cells differ (variation) |
| For growth and repair | For sexual reproduction |

### DNA

DNA was described as a **double helix** by **James Watson and Francis Crick** in 1953, using the X-ray pictures of Rosalind Franklin and Maurice Wilkins. It looks like a twisted ladder.

- The **sides** of the ladder are made of alternate **sugar (deoxyribose)** and **phosphate**.
- The **rungs** are pairs of nitrogen **bases**: **adenine (A) pairs with thymine (T)**, and **cytosine (C) pairs with guanine (G)**.
- The order of bases along DNA is the genetic code.

DNA can make an exact copy of itself (**replication**), so the same instructions pass to new cells. **RNA** carries the message from DNA to make proteins.

```figure caption="Levels of organisation of heredity: from nucleus to chromosome to the DNA double helix with base pairs."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
fig, ax = plt.subplots(figsize=(4.8,2.8))
ax.axis('off'); ax.set_xlim(0,12); ax.set_ylim(0,7)
ax.add_patch(Circle((1.6,4.3),1.5,fc="#f4f7ff",ec=ACCENT,lw=1.3))
ax.add_patch(Circle((1.6,4.3),0.65,fc="#dbe8ff",ec=ACCENT,lw=1.1))
ax.text(1.6,2.4,"Cell with\nnucleus",ha='center',fontsize=7.5,color=INK,va='top')
ax.add_patch(Ellipse((4.9,4.3),0.35,2.2,fc="#e57373",ec=INK,lw=0.8))
ax.add_patch(Ellipse((5.5,4.3),0.35,2.2,fc="#64b5f6",ec=INK,lw=0.8))
ax.text(5.2,2.4,"Chromosome\n(a pair)",ha='center',fontsize=7.5,color=INK,va='top')
y=np.linspace(0.8,6.2,200)
ax.plot(9.5+0.8*np.sin(y*2.4),y,color=SERIES[0],lw=2)
ax.plot(9.5-0.8*np.sin(y*2.4),y,color=SERIES[1],lw=2)
for yy in np.arange(1.0,6.1,0.45):
    a=0.8*np.sin(yy*2.4)
    ax.plot([9.5-a,9.5+a],[yy,yy],color=MUTED,lw=0.9)
ax.text(9.5,0.4,"DNA double helix\n(A-T and C-G pairs)",ha='center',fontsize=7.5,color=INK,va='top')
ax.annotate("",xy=(3.9,4.3),xytext=(3.2,4.3),arrowprops=dict(arrowstyle="->",color=INK))
ax.annotate("",xy=(7.7,4.3),xytext=(6.6,4.3),arrowprops=dict(arrowstyle="->",color=INK))
```

## 4.3 Sex determination

The sex of a child is decided at the moment of fertilisation by the **sex chromosomes**.

- A **female** has two **X** chromosomes (XX). All her egg cells carry one X: she makes only one kind of gamete.
- A **male** has one **X** and one **Y** chromosome (XY). Half of the sperm carry X and half carry Y: he makes two kinds of gametes.

At fertilisation:

- an X-sperm + X-egg gives **XX = a girl**;
- a Y-sperm + X-egg gives **XY = a boy**.

| Egg (from mother) | X-sperm | Y-sperm |
|---|---|---|
| **X** | XX (girl) | XY (boy) |
| **X** | XX (girl) | XY (boy) |

The chance of a boy or a girl is **50 : 50 (1 : 1)** each time, whatever the sex of the earlier children.

```figure caption="Sex determination in human beings. The sex of the baby is decided by the sperm, not by the egg."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.8,3.1))
ax.axis('off'); ax.set_xlim(0,12.8); ax.set_ylim(0,8)
def bx(x,y,t,w=3.2,fc="#eaf1ff",fs=8):
    ax.add_patch(FancyBboxPatch((x-w/2,y-0.4),w,0.8,boxstyle="round,pad=0.04",fc=fc,ec=ACCENT,lw=1))
    ax.text(x,y,t,ha='center',va='center',fontsize=fs,color=INK)
def ar(x1,y1,x2,y2):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color=INK,lw=1))
bx(2.6,7.2,"Mother: 44 + XX",fc="#ffe8f0"); bx(9.2,7.2,"Father: 44 + XY",fc="#dbe8ff")
ar(2.6,6.8,2.6,6.05); ar(8.6,6.8,7.6,6.05); ar(9.8,6.8,10.6,6.05)
bx(2.6,5.65,"Egg: 22 + X",w=2.8,fc="white")
bx(7.3,5.65,"Sperm: 22 + X",w=2.8,fc="white"); bx(10.7,5.65,"Sperm: 22 + Y",w=2.8,fc="white")
ar(7.3,5.2,5.9,3.0); ar(10.7,5.2,10.0,3.0)
ar(2.6,5.2,4.9,3.0); ar(2.6,5.2,8.2,3.2)
bx(5.4,2.5,"44 + XX\nGirl",w=2.6,fc="#ffe8f0"); bx(9.6,2.5,"44 + XY\nBoy",w=2.6,fc="#dbe8ff")
ax.text(6,0.7,"Probability: girl 1/2, boy 1/2",ha='center',fontsize=8.5,color=INK,fontweight='bold')
```

::: example Worked example 4.3 (sex of children)
**Problem.** A couple already have three daughters. What is the probability that the fourth child will be a son? Who decides the sex of a child, the father or the mother?

**Solution.** Each fertilisation is independent. The sperm that reaches the egg is X or Y with equal chance, so the probability of a son (XY) is **1/2 = 50%**, whatever the sex of the earlier children.

All eggs carry X, but sperm carry X or Y, so the **father's** sperm decides the sex of the child. A mother cannot be blamed for having only daughters.
:::

### Sex determination in other animals

In birds, butterflies and some reptiles the male has two similar chromosomes (ZZ) and the female has two different ones (ZW), so the **female** decides the sex. In bees, fertilised eggs give females and unfertilised eggs give males (see Unit 3). In some reptiles (turtles, crocodiles) the incubation temperature of the egg decides the sex.

### Sex-linked inheritance

Genes on the X chromosome are said to be **sex-linked**. The Y chromosome is much smaller and carries few of these genes. A man has only one X, so a recessive gene on it shows (there is no second X to hide it). A woman needs two copies of the recessive allele to show the trait. So these traits are **more common in men**. A woman with one copy is a **carrier**: she is normal but can pass the allele to her children.

## 4.4 Genetic disorders

A **genetic disorder** is a disease or condition caused by a change in a gene or chromosome and passed on in families. Some are caused by faulty genes; others by a wrong number of chromosomes.

### Gene disorders

**Colour blindness.** The person cannot tell red from green. The gene is recessive and lies on the **X chromosome**. It is more common in boys (about 8% of men and 0.5% of women).

**Haemophilia ("bleeder's disease").** The blood does not clot well, so a small cut can bleed for a long time. It is caused by a recessive gene on the X chromosome. Queen Victoria was a carrier and passed it to many royal families in Europe.

In writing the genotypes, X with the letter C stands for the normal allele and X with the letter c for the colour-blind allele:

| Genotype | Phenotype |
|---|---|
| X^C Y | Normal man |
| X^c Y | Colour-blind man |
| X^C X^C | Normal woman |
| X^C X^c | Normal woman (carrier) |
| X^c X^c | Colour-blind woman |

**Albinism.** The person lacks the pigment melanin, and so has very light skin, hair and eyes. It is caused by a recessive gene on an autosome (aa); both parents may be normal carriers (Aa).

**Sickle cell anaemia.** A recessive autosomal disorder in which haemoglobin is abnormal and red blood cells take a sickle shape, blocking small blood vessels. Common in some parts of Africa and India.

**Thalassaemia.** An inherited disorder of haemoglobin that causes severe anaemia; it occurs in South Asia, including Nepal, and the main way to prevent it is screening before marriage and genetic counselling.

::: example Worked example 4.4 (carrier mother)
**Problem.** A normal woman who is a carrier for colour blindness (X^C X^c) marries a normal man (X^C Y). What are the chances of colour-blind children?

**Solution.** Gametes of the mother: X^C and X^c. Gametes of the father: X^C and Y.

| | X^C | Y |
|---|---|---|
| **X^C** | X^C X^C (normal girl) | X^C Y (normal boy) |
| **X^c** | X^C X^c (carrier girl) | X^c Y (colour-blind boy) |

- All daughters are phenotypically normal; **half** of them are carriers.
- **Half of the sons** (1 in 4 of all children) are colour-blind.
- Overall: 1/4 normal girl, 1/4 carrier girl, 1/4 normal boy, 1/4 colour-blind boy.
:::

### Chromosomal disorders

These are due to a change in the number of chromosomes, usually from a mistake in meiosis (non-disjunction), when a pair of chromosomes fails to separate.

| Disorder | Chromosomes | Features |
|---|---|---|
| **Down's syndrome** | 47: an extra chromosome 21 (**trisomy 21**) | Short height, flat face, slanting eyes, mental retardation; the risk increases with the age of the mother |
| **Turner's syndrome** | 45: one X only (**XO**), female | Short, no ovaries, infertile |
| **Klinefelter's syndrome** | 47: **XXY**, male | Tall, small testes, infertile, some breast growth |

```figure caption="Number of chromosomes in normal and abnormal human conditions. The dashed line marks the normal count of 46."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.6))
names=["Normal\nwoman\n(XX)","Normal\nman\n(XY)","Down's\n(trisomy 21)","Turner's\n(XO)","Klinefelter's\n(XXY)"]
vals=[46,46,47,45,47]
cols=[SERIES[0],SERIES[0],SERIES[1],SERIES[2],SERIES[3]]
ax.bar(range(5),vals,color=cols,width=0.6)
ax.axhline(46,color=INK,ls='--',lw=0.9)
for i,v in enumerate(vals):
    ax.text(i,v+0.12,str(v),ha='center',fontsize=8,color=INK)
ax.set_ylim(43,48.2); ax.set_xticks(range(5)); ax.set_xticklabels(names,fontsize=7)
ax.set_ylabel("Chromosomes in a body cell", color=INK, fontsize=8)
ax.spines[['top','right']].set_visible(False)
```

### Prevention and management

- **Genetic counselling** for families with a history of disorders.
- **Avoid marriage between close relatives**, since both partners may carry the same harmful recessive gene.
- **Medical tests** before and during pregnancy (blood test, ultrasound, amniocentesis) to find disorders early.
- Healthy living; avoiding smoking, alcohol and radiation during pregnancy reduces some risks.
- Many genetic disorders cannot be cured, but some can be managed (e.g. giving blood factor to haemophilia patients).

### Importance of genetics

- **Agriculture:** improved crop varieties (high-yielding rice, maize) and cattle breeds by selecting parents.
- **Medicine:** diagnosis, gene therapy and making insulin by genetic engineering.
- **Forensics:** DNA fingerprinting to identify criminals and the parents of a child.
- **Conservation:** studying the genetic variety of endangered species such as the tiger and rhino.

## Chapter summary

- Heredity is the passing of characters from parents to offspring through genes. Mendel, the father of genetics, worked with pea plants and discovered the laws of inheritance.
- Monohybrid cross Tt × Tt gives phenotypic ratio 3 : 1 and genotypic ratio 1 : 2 : 1; a test cross with the recessive parent shows whether a dominant plant is pure.
- Dihybrid cross RrYy × RrYy gives 9 : 3 : 3 : 1.
- Laws: dominance, segregation (purity of gametes), independent assortment.
- Cell → nucleus → chromosome → DNA → gene. Humans have 46 chromosomes (22 pairs autosomes + XX or XY). DNA is a double helix with A–T and C–G pairing.
- Sex is decided by the father's sperm: X-sperm gives a girl, Y-sperm gives a boy; chance 50 : 50.
- Sex-linked recessive disorders (colour blindness, haemophilia) are commoner in males.
- Chromosomal disorders: Down's (47, trisomy 21), Turner's (XO, 45), Klinefelter's (XXY, 47). Genetic counselling helps prevention.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. Who is called the father of genetics? <span class="marks">[1]</span>
   (a) Darwin (b) Mendel (c) Watson (d) Lamarck
2. The genotypic ratio in the F₂ generation of a monohybrid cross is <span class="marks">[1]</span>
   (a) 3 : 1 (b) 9 : 3 : 3 : 1 (c) 1 : 2 : 1 (d) 1 : 1
3. The sex of a human baby is decided by <span class="marks">[1]</span>
   (a) the egg (b) the sperm (c) the mother's age (d) the food
4. Down's syndrome is caused by <span class="marks">[1]</span>
   (a) a missing X chromosome (b) an extra chromosome 21 (c) an extra Y chromosome (d) a gene on the X chromosome
5. A plant with the genotype Tt is called <span class="marks">[1]</span>
   (a) homozygous (b) heterozygous (c) recessive (d) pure
6. The base that pairs with adenine in DNA is <span class="marks">[1]</span>
   (a) cytosine (b) guanine (c) thymine (d) uracil

::: note Answers to Group A
**1.** (b) — Mendel.
**2.** (c) — 1 TT : 2 Tt : 1 tt.
**3.** (b) — the sperm carries X or Y.
**4.** (b) — trisomy 21, giving 47 chromosomes.
**5.** (b) — two different alleles.
**6.** (c) — A pairs with T (uracil is in RNA).
:::

**Group B — Short answer (2 marks each)**

1. Define gene and allele. <span class="marks">[2]</span>
2. Differentiate between genotype and phenotype. <span class="marks">[2]</span>
3. State Mendel's law of segregation. <span class="marks">[2]</span>
4. Why is colour blindness more common in males than in females? <span class="marks">[2]</span>
5. What is a test cross? What is its use? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A gene is a section of DNA on a chromosome that controls a character. An allele is one of the alternative forms of a gene.
**2.** Genotype is the genetic make-up (e.g. Tt); phenotype is the visible character (e.g. tall).
**3.** The two alleles of a gene separate during gamete formation, so each gamete gets only one allele.
**4.** The gene is recessive and on the X chromosome. A male has one X, so one copy of the allele shows; a female needs two copies.
**5.** A test cross is the cross of an individual with the dominant character with a homozygous recessive individual. It is used to find out whether the individual is homozygous or heterozygous.
:::

**Group C — Long answer (4 marks each)**

1. Explain Mendel's monohybrid cross between pure tall and pure dwarf pea plants up to the F₂ generation with a Punnett square. <span class="marks">[4]</span>
2. In a dihybrid cross of RrYy × RrYy, find the phenotypic ratio. If there are 800 offspring, how many are wrinkled green? <span class="marks">[4]</span>
3. A colour-blind man marries a normal woman who is not a carrier. Find the genotypes and phenotypes of their children. <span class="marks">[4]</span>
4. Explain how the sex of a child is determined in human beings, with a diagram. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** P: TT × tt. Gametes T and t. F₁: all Tt (tall). F₁ self: gametes T, t from each parent; Punnett square gives TT, Tt, Tt, tt. F₂: 3 tall : 1 dwarf, genotypic ratio 1 : 2 : 1.
**2.** 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green. Wrinkled green = 1/16 × 800 = 50.
**3.** Man X^c Y, woman X^C X^C. Gametes: X^c, Y and X^C. Children: X^C X^c (carrier girls, normal sight) and X^C Y (normal boys). All children have normal sight; the daughters are carriers.
**4.** Female XX makes eggs with X only. Male XY makes sperms of X and Y in equal numbers. X-sperm + egg = XX girl; Y-sperm + egg = XY boy. The chance is 50 : 50. The father's sperm decides.
:::

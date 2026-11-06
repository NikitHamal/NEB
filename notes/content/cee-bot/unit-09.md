---
subject: Botany
grade: CEE
unit: 9
title: Inheritance, Linkage, Mutation and Genetic Disorders
hours: 4
area: Genetics
---

This is the biggest chapter of the Genetics unit — about **4 of the 40
Botany questions** — and the most "solvable": almost every question is a
small cross, a ratio or a karyotype that can be worked in the margin. It
covers Mendel's terminology and laws with their two great modifications,
**linkage and crossing over**, **sex-linked inheritance** in humans and
*Drosophila*, **mutation and polyploidy**, and the six human disorders the
syllabus names. Learn the standard ratios by heart, learn to read a test
cross as a direct printout of gametes, and the four marks are among the
cheapest in the paper.

::: key What the paper asks from this chapter
- **Mendel** — *Pisum sativum*, seven characters, pure lines, counting; father of genetics; rediscovered 1900 by de Vries, Correns and Tschermak.
- **The words** — gene, allele, locus, dominant/recessive, homo-/heterozygous, genotype/phenotype, back cross vs test cross.
- **The ratios** — monohybrid F₂ 3 : 1 (genotypic 1 : 2 : 1); dihybrid F₂ 9 : 3 : 3 : 1; test crosses 1 : 1 and 1 : 1 : 1 : 1; incomplete dominance 1 : 2 : 1.
- **The laws** — dominance; segregation (purity of gametes, cytological basis anaphase I); independent assortment.
- **Incomplete dominance** (*Mirabilis* pink) vs **co-dominance** (AB blood group, roan cattle); multiple alleles (ABO: I^A^, I^B^, i).
- **Linkage** — Bateson and Punnett (sweet pea); Morgan's explanation; complete vs incomplete; linkage groups = haploid number; crossing over between non-sister chromatids; 1 cM = 1% recombination.
- **Sex linkage** — hemizygous males; criss-cross inheritance; colour blindness and haemophilia (X-recessive); Morgan's white-eyed *Drosophila*.
- **Mutation** — de Vries; point (substitution, frameshift) vs chromosomal (structural and numerical); mutagens; non-disjunction → aneuploidy.
- **Polyploidy** — colchicine; autopolyploid (banana, potato) vs allopolyploid (bread wheat, *Triticale*, *Raphanobrassica*); triploid sterility.
- **Disorders** — Down (trisomy 21), Edwards (trisomy 18), Turner (45, XO), Klinefelter (47, XXY), albinism (autosomal recessive, no tyrosinase), haemophilia (X-recessive, factor VIII).
:::

## 9.1 Mendelian terminology and laws; incomplete dominance and co-dominance

**Gregor Johann Mendel** (1822–1884), an Austrian monk, worked on the
garden pea ***Pisum sativum*** from 1856 to 1863 and published in 1866; the
work was ignored until **de Vries, Correns and Tschermak rediscovered it
in 1900**. He succeeded because he studied **one pair of contrasting
characters at a time**, started from **pure (true-breeding) lines**,
**counted** large numbers of offspring, and followed crosses through
several generations. The pea helped: naturally self-pollinating, easily
crossed by hand after emasculation, short-lived, and offering seven
clear-cut character pairs — tall/dwarf stem, axial/terminal flowers,
violet/white flowers, inflated/constricted pods, green/yellow pods,
round/wrinkled seeds, yellow/green cotyledons.

::: definition The words you must use correctly
**Gene** — a unit of inheritance, a DNA segment at a fixed **locus** on a
chromosome. **Allele** — one of the alternative forms of a gene (T and t).
**Dominant** — the allele expressed in the heterozygote; **recessive** —
the one masked in it. **Homozygous** (TT, tt) — both alleles alike;
**heterozygous** (Tt) — alleles different. **Genotype** — the genetic
constitution; **phenotype** — the visible character. **Monohybrid cross**
— follows one character; **dihybrid** — two. **Back cross** — F₁ crossed
with either parent; **test cross** — F₁ (or any dominant-looking
individual) crossed with the **homozygous recessive**.
:::

Crossing pure tall (TT) with pure dwarf (tt) gave an F₁ of all tall
plants (Tt). Selfing the F₁ gave an F₂ of **3 tall : 1 dwarf** (genotypes
**1 TT : 2 Tt : 1 tt**). The dwarf allele had survived the F₁ unchanged —
only hidden. From this, Mendel's first two laws:

::: definition Law of dominance and law of segregation
**Dominance.** When two contrasting alleles meet in a hybrid, only the
dominant one is expressed; the recessive remains unexpressed but
unchanged.

**Segregation (purity of gametes).** The two alleles of a pair separate
during gamete formation, so every gamete carries only one of them — a
gamete is never hybrid. Its cytological basis is **anaphase I of
meiosis**, when homologues part.
:::

A tall plant may be TT or Tt — indistinguishable by eye. A **test cross**
with a dwarf (tt) reveals it: TT gives all tall offspring, Tt gives
**1 tall : 1 dwarf**. The test cross works because the recessive parent
contributes only recessive alleles, so the offspring ratio is a direct
copy of the **gamete ratio** of the plant being tested. That one idea —
*test-cross progeny display the gametes of the heterozygous parent* —
drives every linkage calculation later in this chapter.

With two characters at once (round/wrinkled seeds × yellow/green
cotyledons) the F₂ gave **9 : 3 : 3 : 1** — the two 3 : 1 ratios combined
freely. Hence the **law of independent assortment**: alleles of
*different* genes separate into gametes independently of one another
(because different chromosome pairs orient independently at metaphase I).
A dihybrid test cross accordingly gives **1 : 1 : 1 : 1**.

```figure caption="The dihybrid F2 Punnett square (RrYy x RrYy). Each parent makes four gamete types in equal numbers; colouring the sixteen boxes by phenotype gives the famous 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.9, 3.4))
gams = ['RY', 'Ry', 'rY', 'ry']
cols = {(0,0):'#bfe3b4'}
def pheno(g1, g2):
    R = 'R' in (g1[0] + g2[0]); Y = 'Y' in (g1[1] + g2[1])
    if R and Y: return '#bfe3b4'
    if R: return '#fdf0b3'
    if Y: return '#cfe0f2'
    return '#f6cfc9'
def geno(g1, g2):
    a = ''.join(sorted(g1[0] + g2[0], key=lambda ch: ch.islower()))
    b = ''.join(sorted(g1[1] + g2[1], key=lambda ch: ch.islower()))
    return a + b
for i, gr in enumerate(gams):
    for j, gc in enumerate(gams):
        ax.add_patch(Rectangle((j, 3-i), 1, 1, fc=pheno(gr, gc), ec=INK, lw=0.7))
        ax.text(j+0.5, 3-i+0.5, geno(gr, gc), fontsize=6.3, ha='center', va='center', color=INK)
    ax.text(-0.14, 3-i+0.5, gr, fontsize=6.8, ha='right', va='center', color=INK)
    ax.text(i+0.5, 4.12, gams[i], fontsize=6.8, ha='center', va='bottom', color=INK)
ax.text(2.0, -0.55, '9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green',
        fontsize=6.6, ha='center', color=MUTED)
ax.text(2.0, 4.62, 'F1 gametes from each parent', fontsize=6.6, ha='center', color=MUTED)
ax.set_xlim(-0.85, 4.15); ax.set_ylim(-0.85, 4.95); ax.set_aspect('equal'); ax.axis('off')
```

### Incomplete dominance and co-dominance

Mendel's peas happened to show complete dominance; many genes do not.

**Incomplete dominance** — neither allele fully dominates, so the
heterozygote is **intermediate**. In *Mirabilis jalapa* (four-o'clock) and
*Antirrhinum* (snapdragon), red (RR) × white (rr) gives **pink** (Rr) F₁;
selfing gives **1 red : 2 pink : 1 white** — the phenotypic ratio equals
the genotypic ratio. Note that red and white reappear pure in F₂: the
alleles never blended, they merely dosed the pigment.

**Co-dominance** — both alleles express themselves **side by side** in
the heterozygote, not as a blend. The human AB blood group carries
**both** A and B antigens; roan cattle have red and white hairs mixed,
not pink hairs.

**Multiple alleles** — a gene may have more than two alleles in the
population (though any one person carries only two). The ABO system is
controlled by gene *I* with three alleles **I^A^, I^B^ and i**: I^A^ and
I^B^ are co-dominant with each other and both dominant over i, giving four
blood groups (A, B, AB, O) from six genotypes.


```figure caption="The monohybrid logic in four moves: true-breeding parents give a uniform heterozygous F₁, selfing the F₁ sorts the alleles 3 : 1 in phenotype and 1 : 2 : 1 in genotype, and a test cross against the recessive reads an unknown genotype straight off a 1 : 1 or uniform progeny."
flow([("P cross", "TT × tt\nall Tt"),
      ("F₁ self", "Tt × Tt\ngametes T, t"),
      ("F₂ ratios", "3 : 1 phenotype\n1 : 2 : 1 genes"),
      ("test cross", "Tt × tt\n1 : 1 reveals")], figsize=(5.2, 2.15))
```

::: example Recombination mapping and pedigree probability
**Problem.** A dihybrid test cross yields 850 offspring, of which 170 are
recombinant. How far apart are the two genes? Separately: a carrier mother
(X^H X^h) and a normal father (X^H Y) plan a family — what is the chance a
son has haemophilia, and the chance that any child is an affected son? A
colour-blind man marries a homozygous normal woman — what are their
daughters?
**Solution.** 170 ÷ 850 = 20 % recombination = **20 map units** apart.
Sons receive the mother's X: half of them get X^h → **1/2 of sons affected**;
an affected son is one of four equally likely child types → **1/4 of all
children**. Every daughter receives the father's only X, which carries the
colour-blindness allele, plus a normal X from mother: **all daughters
carriers, none affected** — and every son normal, taking the Y.
:::
```photogrid label="9.1" cols="2" ratio="1.2" caption="Testing Mendel's 9:3:3:1 with a chi-square. (a) Mendel's seven pea characters, each with a dominant and a recessive form. (b) In his dihybrid cross (round yellow x wrinkled green) he counted 315, 101, 108 and 32 seeds, 556 in all. A 9:3:3:1 ratio would give 312.75, 104.25, 104.25 and 34.75. Chi-square = sum of (O - E)^2/E = 0.47; with 3 degrees of freedom the 5 per cent critical value is 7.81, so the data fit the ratio very well (if anything, suspiciously well, as later statisticians noted)."
@ photo id="ceebot/mendel-chars" cap="Mendel's seven pea characters"
fit 1.2
focus 0.5 0.4
@ svg cap="Observed against expected seed counts"
obs = (315, 101, 108, 32)
n = sum(obs)
exp = [n * r / 16 for r in (9, 3, 3, 1)]
chi = sum((o - e) ** 2 / e for o, e in zip(obs, exp))
assert n == 556 and abs(chi - 0.470) < 0.001
facts = dict(e1="%.2f" % exp[0], e2="%.2f" % exp[1], e3="%.2f" % exp[2], e4="%.2f" % exp[3], chi="%.2f" % chi)
f = Fig(300, 236)
f.text(150, 12, "Seeds counted (navy) and expected (amber)", size=10.5, color=NAVY, bold=True)
labs = ("round yellow", "round green", "wrinkled yellow", "wrinkled green")
base = 170
for i, (o, e) in enumerate(zip(obs, exp)):
    x = 22 + i * 68
    f.box(x, base - o / 315 * 120, 22, o / 315 * 120, fill=BLUE, stroke=NAVY, r=1)
    f.box(x + 24, base - e / 315 * 120, 22, e / 315 * 120, fill=SAND, stroke=AMBER, r=1)
    f.text(x + 11, base - o / 315 * 120 - 6, str(o), size=10.5, color=NAVY, bold=True)
    f.text(x + 35, base - e / 315 * 120 - 6 if i else base - e / 315 * 120 - 20, "%.0f" % e, size=10.5, color=AMBER, bold=True)
    f.text(x + 23, base + 14, labs[i].split()[0], size=10.5, color=SLATE)
    f.text(x + 23, base + 27, labs[i].split()[1], size=10.5, color=SLATE)
f.line(14, base, 290, base, color=SLATE)
f.text(150, 224, "chi-square = %.2f (critical 7.81)" % chi, size=10.5, color=NAVY, bold=True)
```

## 9.2 Linkage (complete and incomplete) and crossing over

Independent assortment fails for genes that sit on the **same
chromosome**: they tend to travel together into gametes. This is
**linkage**. **Bateson and Punnett (1906)** first saw it in sweet pea,
where parental combinations in a dihybrid test cross far outnumbered new
ones; they spoke of **coupling** (dominant alleles entering together on
one chromosome, the *cis* arrangement AB/ab) and **repulsion** (entering
apart, *trans*, Ab/aB). **T. H. Morgan (1910)**, using *Drosophila*, showed
coupling and repulsion are just two arrangements of linked genes, and
that the **strength of linkage depends on the distance between the genes**
— the closer, the stronger. All the genes on one chromosome form a
**linkage group**, so the number of linkage groups equals the **haploid
chromosome number** (4 in *Drosophila*, 23 in humans).

- **Complete linkage** — genes so close (or in an organism/sex with no
  crossing over, such as **male *Drosophila*** and female silkworm) that
  only parental gametes form; a test cross gives just the two parental
  classes, 1 : 1.
- **Incomplete linkage** — the usual case: crossing over in some meioses
  produces a minority of **recombinant** gametes; a test cross gives two
  large parental classes and two small recombinant classes.

**Crossing over** is the exchange of corresponding segments between
**non-sister chromatids** of homologues at **pachytene** of prophase I,
visible later as chiasmata. Its frequency between two genes rises with
the distance between them and is also affected by sex, age, temperature,
radiation and nearness to the centromere (where it is suppressed). Because
the recombinant classes in a test cross reveal recombinant gametes
directly,

$$ \text{recombination frequency} = \frac{\text{recombinant offspring}}{\text{total offspring}} \times 100\% $$

and **Sturtevant (1913)** turned this into a map: **1% recombination =
1 map unit = 1 centimorgan (cM)**. Frequencies never exceed 50% — at 50%
the genes assort as if unlinked (they may be far apart on one chromosome
or on different chromosomes).

```figure caption="Incomplete linkage in a coupling-phase heterozygote AB/ab. Most gametes keep the parental combinations; a crossover between the two loci in some meioses swaps the ends and creates the two recombinant gamete types."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 3.0))
ax.plot([0.3, 3.1], [5.2, 5.2], color='#1d6fb8', lw=3.0, solid_capstyle='round')
ax.plot([0.3, 3.1], [4.4, 4.4], color='#d9534f', lw=3.0, solid_capstyle='round')
for x, t, c in [(1.0, 'A', '#1d6fb8'), (2.5, 'B', '#1d6fb8')]:
    ax.text(x, 5.55, t, fontsize=7.4, ha='center', color=c)
for x, t, c in [(1.0, 'a', '#d9534f'), (2.5, 'b', '#d9534f')]:
    ax.text(x, 3.95, t, fontsize=7.4, ha='center', color=c)
ax.text(1.7, 6.15, 'coupled homologues AB / ab', fontsize=6.6, ha='center', color=INK)
ax.plot([1.75, 1.75], [5.35, 4.25], color=MUTED, lw=0.8, ls='--')
ax.text(1.75, 3.35, 'crossover here\nin some meioses', fontsize=6.3, ha='center', color=MUTED)
def gamete(x, parts, label, lab2):
    xs = x
    for (col, letter) in parts:
        ax.plot([xs, xs+0.62], [1.7, 1.7], color=col, lw=3.0, solid_capstyle='round')
        ax.text(xs+0.31, 2.05, letter, fontsize=7.0, ha='center', color=col)
        xs += 0.68
    ax.text(x+0.66, 1.05, label, fontsize=6.5, ha='center', color=INK)
    ax.text(x+0.66, 0.55, lab2, fontsize=6.3, ha='center', color=MUTED)
B, R = '#1d6fb8', '#d9534f'
gamete(4.3, [(B,'A'), (B,'B')], 'AB', 'parental')
gamete(6.1, [(R,'a'), (R,'b')], 'ab', 'parental')
gamete(7.9, [(B,'A'), (R,'b')], 'Ab', 'recombinant')
gamete(9.7, [(R,'a'), (B,'B')], 'aB', 'recombinant')
ax.text(5.85, 2.75, 'majority of gametes', fontsize=6.5, ha='center', color=INK)
ax.text(9.45, 2.75, 'minority', fontsize=6.5, ha='center', color=INK)
ax.set_xlim(0, 11.4); ax.set_ylim(0, 6.6); ax.axis('off')
```

::: example Worked example — mapping two genes from a test cross
**Problem.** A dihybrid plant AaBb (in coupling phase) is test-crossed
with aabb. The progeny are: AaBb 415, aabb 405, Aabb 92, aaBb 88. Are the
genes linked? If so, how far apart are they?

**Solution.** In a test cross the progeny phenotypes display the gametes
of the heterozygous parent. Two classes are large (415, 405) and two
small (92, 88), instead of the 1 : 1 : 1 : 1 expected for unlinked genes
— so the genes are **linked**. The small classes are the recombinants:

$$ \text{RF} = \frac{92 + 88}{415 + 405 + 92 + 88} \times 100 = \frac{180}{1000} \times 100 = 18\% $$

The genes are **18 map units (18 cM)** apart. Identify recombinants by
**frequency** (the two smallest classes), never by whether they "look"
parental.
:::

## 9.3 Sex-linked inheritance: colour blindness in humans, eye colour in Drosophila

Genes on the X chromosome (outside the small region shared with Y) have
**no partner allele in the male**. A male is therefore **hemizygous**: a
single recessive allele on his one X expresses itself. That is why
**red–green colour blindness** and **haemophilia** are far commoner in
men: a woman needs the allele on **both** X chromosomes to be affected,
whereas one copy makes her a phenotypically normal **carrier**.

The transmission pattern is **criss-cross inheritance**: an affected
father passes his X (and the allele) to **all his daughters** (carriers)
and to **none of his sons** (they get his Y); a carrier mother passes the
allele to **half her sons**, who are affected, and half her daughters,
who become carriers. The character thus hops from grandfather, through
carrier daughters, to grandsons.

**Eye colour in *Drosophila*.** Morgan (1910) found a white-eyed male in
his red-eyed cultures. White proved **recessive and X-linked**: red-eyed
female × white-eyed male gave all red F₁, and the F₂ showed 3 red : 1
white with **all the whites male**; the reciprocal cross (white female ×
red male) gave red daughters and white sons in F₁ itself — the textbook
criss-cross, and the first gene ever assigned to a chromosome. Remember
the logic of reciprocal crosses: **if the two reciprocal crosses give
different results, the gene is sex-linked** (autosomal genes give
identical reciprocal results).

(Y-linked or **holandric** genes — e.g. the SRY sex-determining region —
pass only from father to son; **sex-influenced** genes such as human
pattern baldness are autosomal but dominant in one sex and recessive in
the other.)

```photogrid label="9.2" cols="2" ratio="1.2" caption="Eye colour in Drosophila follows the X chromosome. (a) A white-eyed fruit fly, the mutant Thomas Hunt Morgan used in 1910 to show that a gene sits on a chromosome. The white allele is recessive and X-linked. (b) A heterozygous red-eyed female (XW Xw) crossed with a red-eyed male (XW Y) gives 4 equally likely zygotes: 2 of them are red-eyed females (half carriers) and the male offspring split 1 red to 1 white. So 25 per cent of all progeny, and 50 per cent of the sons, are white-eyed, while no daughter is. The same pattern explains colour blindness and haemophilia in humans."
@ photo id="ceebot/drosophila-white" cap="A white-eyed Drosophila beside a scale"
fit 1.2
focus 0.5 0.5
@ svg cap="Punnett square: XW Xw female x XW Y male"
mother, father = ("XW", "Xw"), ("XW", "Y")
kids = [(m, fa) for m in mother for fa in father]
def pheno(m, fa):
    if fa == "Y":
        return "white male" if m == "Xw" else "red male"
    return "carrier female" if "Xw" in (m, fa) else "red female"
ph = [pheno(*k) for k in kids]
sons = [p for p in ph if "male" in p and "fe" not in p]
assert ph.count("white male") == 1 and len(sons) == 2 and ph.count("carrier female") == 1
facts = dict(nk=len(kids), fr=ph.count("red female") + ph.count("carrier female"), wm="%.0f" % (100 * ph.count("white male") / 4), wsons="%.0f" % (100 * ph.count("white male") / len(sons)))
f = Fig(300, 236)
f.text(150, 12, "Mother gametes (rows), father gametes (columns)", size=10.5, color=NAVY, bold=True)
col = {"white male": (ROSE, RED), "carrier female": (SAND, AMBER), "red female": (MINT, TEAL), "red male": (MINT, TEAL)}
for j, g in enumerate(father):
    f.text(100 + j * 100 + 44, 40, g, size=11, color=NAVY, bold=True)
for i, g in enumerate(mother):
    f.text(40, 86 + i * 62, g, size=11, color=NAVY, bold=True, vmid=True)
for k, (m, fa) in enumerate(kids):
    i, j = divmod(k, 2)
    fl, st = col[ph[k]]
    f.box(100 + j * 100 - 0, 52 + i * 62, 90, 56, fill=fl, stroke=st, r=4, sw=1.6)
    f.text(145 + j * 100, 72 + i * 62, "%s %s" % (m, fa), size=11, color=st, bold=True)
    f.text(145 + j * 100, 92 + i * 62, ph[k], size=10.5, color=st, bold=True)
f.text(150, 192, "white-eyed: 1 in 4 of all, 1 in 2 of sons", size=10.5, color=RED, bold=True)
f.text(150, 210, "no white-eyed daughters in this cross", size=10.5, color=SLATE, bold=True)
```

```photogrid label="9.3" cols="2" ratio="1.2" caption="Colour blindness in a population. (a) Ishihara plates hide a number in dots of two colours that a person with red-green colour blindness cannot separate. (b) The gene is X-linked, so men (one X) show the recessive allele whenever they carry it: if 8 per cent of men are affected, q = 0.08 and p = 0.92. Women need two copies, so the Hardy-Weinberg law gives 0.64 per cent affected (q squared), 14.72 per cent carriers (2pq) and 84.64 per cent unaffected non-carriers (p squared). Colour blindness is therefore about 12.5 times commoner in men than in women."
@ photo id="ceebot/ishihara" cap="Ishihara plates used to test colour vision"
fit 1.2
focus 0.5 0.5
@ svg cap="Share of men and women by genotype (q = 0.08)"
q = 0.08
p = 1 - q
qq, car, nn = q * q * 100, 2 * p * q * 100, p * p * 100
assert abs(qq + car + nn - 100) < 1e-9 and abs(qq - 0.64) < 1e-9 and abs(car - 14.72) < 1e-9 and abs(nn - 84.64) < 1e-9
facts = dict(qq="%.2f" % qq, car="%.2f" % car, nn="%.2f" % nn, ratio="%.1f" % (q * 100 / qq))
f = Fig(300, 236)
f.text(150, 12, "Per cent of the population (X-linked recessive)", size=10.5, color=NAVY, bold=True)
rows = (("Men affected (XwY)", q * 100, RED, ROSE), ("Women affected (XwXw)", qq, RED, ROSE), ("Women carriers (XWXw)", car, AMBER, SAND), ("Women unaffected (XWXW)", nn, TEAL, MINT))
for i, (lab, v, c, fl) in enumerate(rows):
    y = 28 + i * 44
    f.text(10, y + 4, lab, size=10.5, color=SLATE, anchor="start")
    w = max(v * 2.1, 3)
    f.box(10, y + 12, w, 18, fill=fl, stroke=c, r=2)
    f.text(10 + w + 6, y + 21, "%.2f%%" % v, size=10.5, color=c, bold=True, anchor="start", vmid=True)
f.text(150, 214, "men: 8.00 / women: 0.64 = 12.5 times", size=10.5, color=NAVY, bold=True)
```

## 9.4 Gene and chromosomal mutations; polyploidy

A **mutation** is a sudden, heritable change in the genetic material (the
term is **Hugo de Vries'**, from his work on *Oenothera*). Mutations may be
**spontaneous** (replication errors) or **induced** by **mutagens** —
physical (X-rays, gamma rays, UV), chemical (nitrous acid, EMS, mustard
gas, base analogues such as 5-bromouracil, acridine dyes, colchicine) or
biological (transposons, some viruses). **Somatic** mutations are not
inherited (unless the plant is propagated vegetatively); **gametic**
mutations pass to offspring.

**Gene (point) mutations** change one or a few base pairs:

- **Substitution** — one base pair replaced: a *transition* (purine ↔
  purine) or *transversion* (purine ↔ pyrimidine). Effects range from
  none (silent, thanks to degeneracy) through a changed amino acid
  (missense — sickle-cell anaemia, one base) to a premature stop
  (nonsense).
- **Frameshift** — insertion or deletion of bases in a number that is
  **not a multiple of three** shifts the reading frame, garbling every
  codon downstream; usually the most damaging point mutation.

**Chromosomal mutations** change structure or number. Structural:
**deletion** (lost segment), **duplication** (repeated segment),
**inversion** (segment reversed 180°) and **translocation** (segment
moved to another chromosome). Numerical: **euploidy** changes whole sets
(n, 3n, 4n — polyploidy below), while **aneuploidy** adds or loses
individual chromosomes (2n + 1 trisomy, 2n − 1 monosomy, 2n + 2
tetrasomy, 2n − 2 nullisomy). Aneuploidy arises by **non-disjunction** —
homologues (meiosis I) or sister chromatids (meiosis II) failing to
separate, producing n + 1 and n − 1 gametes.

**Polyploidy** — more than two complete chromosome sets — is a major
engine of plant evolution and breeding. It is induced artificially with
**colchicine** (an alkaloid from *Colchicum*), which blocks spindle
formation so a replicated nucleus does not divide and the chromosome
number doubles.

| | Autopolyploidy | Allopolyploidy (amphidiploidy) |
|---|---|---|
| Sets come from | one species, multiplied (AAAA) | two species, then doubled (AABB) |
| Examples | potato, banana (3n), seedless watermelon (3n) | bread wheat (6n), *Triticale*, *Raphanobrassica* |
| Notes | larger cells and organs (gigas); odd ploidies sterile | doubling restores fertility to sterile hybrids by giving every chromosome a partner |

A **triploid (3n)** is sterile because three sets cannot pair evenly in
meiosis — exactly why seedless bananas and watermelons are seedless.
Karpechenko's ***Raphanobrassica*** (radish × cabbage, 1928) and the
man-made cereal ***Triticale*** (wheat × rye) are the classic
allopolyploids; bread wheat *Triticum aestivum* is a natural
allohexaploid (6n = 42).

## 9.5 Down's, Turner's, Edwards' and Klinefelter's syndromes; albinism; haemophilia

| Disorder | Karyotype / gene | Sex and key features |
|---|---|---|
| **Down syndrome** | **trisomy 21** (47, +21), maternal non-disjunction | either sex; short stature, round face, epicanthal fold, single palmar (simian) crease, intellectual disability; risk rises steeply with mother's age |
| **Edwards syndrome** | **trisomy 18** (47, +18) | either sex, mostly female survivors; clenched overlapping fingers, rocker-bottom feet, severe heart defects; usually fatal in infancy |
| **Turner syndrome** | **45, XO** — monosomy of X | female; short, webbed neck, underdeveloped ovaries (streak gonads), sterile, no Barr body |
| **Klinefelter syndrome** | **47, XXY** | male (Y decides sex); tall, long limbs, small testes, sterile, some breast development (gynaecomastia), one Barr body |
| **Albinism** | **autosomal recessive** — no functional **tyrosinase**, so tyrosine is not converted to melanin | either sex equally; white skin and hair, pink eyes, photophobia; normal parents can have albino children (both carriers) |
| **Haemophilia** | **X-linked recessive** — deficient clotting **factor VIII** (type A; factor IX in type B) | almost always males; wounds bleed long, bleeding into joints; "royal disease" of Queen Victoria's descendants |

Three exam habits with this table: (1) count chromosomes — 45, 46 or 47
sorts Turner from normal from the trisomies/XXY at a glance; (2) the
**Y chromosome decides maleness**, so XXY is male and XO is female; (3)
autosomal recessive disorders (albinism) strike **both sexes equally**
and skip generations through carriers, while X-linked recessives
(haemophilia, colour blindness) strike **mostly males** and never pass
father-to-son.

::: example Worked example — a haemophilia risk
**Problem.** A woman whose father was haemophilic marries a normal man.
What is the probability that (a) her son is haemophilic, (b) her daughter
is a carrier, (c) a child of hers is haemophilic?

**Solution.** Her father was X^h^Y; every daughter receives his only X,
so the woman is an **obligate carrier** X^H^X^h^ (she got X^H^ from her
mother and is herself normal). Her husband is X^H^Y.

| | X^H^ (father) | Y (father) |
|---|---|---|
| **X^H^** | X^H^X^H^ normal girl | X^H^Y normal boy |
| **X^h^** | X^H^X^h^ carrier girl | X^h^Y haemophilic boy |

(a) Of her sons, half receive X^h^: **1/2 (50%)**. (b) Of her daughters,
half receive X^h^: **1/2** carriers (none haemophilic). (c) One of the
four equally likely children is haemophilic: **1/4 (25%)**. Always state
whether the probability is *among sons*, *among daughters* or *among all
children* — the paper tests exactly that distinction.
:::



```figure caption="Inheritance in four drawers: Mendel's two laws and their ratios, the two exceptions where both alleles show, linkage and its map-unit arithmetic, and the chromosomal disorders the paper names by karyotype."
cards([
    ("Mendel's laws", "segregation: allele pairs part\nindependent assortment:\nunlinked genes shuffle 9:3:3:1"),
    ("Exceptions", "incomplete dominance 1 : 2 : 1\nco-dominance: AB blood\nboth alleles visible"),
    ("Linkage", "same chromosome travels together\ncrossing over makes recombinants\n1 % recombination = 1 map unit"),
    ("Disorders", "Down 47,+21; Turner 45,X\nKlinefelter 47,XXY\nhaemophilia, colour-blind: X-linked"),
], cols=2, figsize=(6.2, 3.0))
```

::: caution
Four pairs the paper swaps: **incomplete dominance blends the phenotype
(pink), co-dominance shows both (AB)** — both give 1 : 2 : 1 F₂, so the
example, not the ratio, names them; **linkage defeats independent
assortment**, and crossing over defeats linkage; **Turner is 45,X and
female, Klinefelter 47,XXY and male** — the Y, not the X count, decides sex;
and **translocation moves segments between non-homologues**, while crossing
over exchanges between homologues.
:::

## Formula and fact sheet

- **Mendel**: *Pisum sativum*, 1856–63, published 1866, rediscovered 1900 (de Vries, Correns, Tschermak); seven characters, pure lines, counted F₂.
- **Ratios**: monohybrid F₂ 3 : 1 (1 : 2 : 1 genotypic); dihybrid F₂ 9 : 3 : 3 : 1; monohybrid test cross 1 : 1; dihybrid test cross 1 : 1 : 1 : 1; incomplete dominance 1 : 2 : 1.
- **Laws**: dominance; segregation = purity of gametes (anaphase I); independent assortment (metaphase I orientation) — fails for linked genes.
- **Incomplete dominance**: *Mirabilis*/*Antirrhinum* pink; **co-dominance**: AB blood, roan; **multiple alleles**: I^A^, I^B^, i → 4 phenotypes, 6 genotypes.
- **Linkage**: Bateson and Punnett (sweet pea, 1906); Morgan's chromosomal explanation; linkage groups = haploid number; *cis* = coupling, *trans* = repulsion.
- **Crossing over**: non-sister chromatids, pachytene; RF = recombinants ÷ total × 100; 1% = 1 cM; RF caps at 50%; absent in male *Drosophila* (complete linkage).
- **Sex linkage**: males hemizygous; criss-cross (father → daughters → grandsons); reciprocal crosses differ; white eye in *Drosophila* (Morgan, 1910).
- **Mutation**: de Vries; substitution (transition/transversion) vs frameshift (not a multiple of 3); structural: deletion, duplication, inversion, translocation; numerical: euploidy vs aneuploidy; non-disjunction.
- **Mutagens**: X-rays, UV, nitrous acid, EMS, 5-bromouracil, acridines (frameshifts), colchicine (ploidy, anti-spindle).
- **Polyploidy**: autopolyploid — banana, potato, seedless watermelon (3n sterile); allopolyploid — bread wheat 6n = 42, *Triticale*, *Raphanobrassica*; colchicine doubles sets.
- **Disorders**: Down 47,+21; Edwards 47,+18; Turner 45,XO (female); Klinefelter 47,XXY (male); albinism autosomal recessive (no tyrosinase → no melanin); haemophilia X-recessive (factor VIII).

### Rapid-revision tables and high-yield facts

| Quantity | Value |
|---|---|
| Monohybrid F₂ | 3 : 1 phenotype, 1 : 2 : 1 genotype |
| Dihybrid F₂ / test cross | 9 : 3 : 3 : 1 / 1 : 1 : 1 : 1 |
| Incomplete dominance F₂ | 1 : 2 : 1 |
| Map distance | recombinants ÷ total × 100 (cM) |
| Sex-linked pattern | mother → son (criss-cross); never father → son |
| Down / Edwards | trisomy 21 / trisomy 18 |
| Turner / Klinefelter | 45,X / 47,XXY |
| Albinism / haemophilia | autosomal recessive / X-linked recessive |
| Frameshift | indel not a multiple of 3 |
| Polyploidy agent | colchicine (spindle poison) |

## Chapter summary

- Mendel's pea crosses gave genetics its language (allele, dominant, genotype) and its first two laws: dominance, and segregation — alleles part into gametes unaltered, which meiosis I explains physically.
- The signature ratios flow from gamete combinations: 3 : 1 and 9 : 3 : 3 : 1 in F₂, and test-cross ratios that print out the gametes of the heterozygote directly.
- Incomplete dominance (pink *Mirabilis*, 1 : 2 : 1) and co-dominance (AB blood group) modify expression, never segregation — pure types reappear in F₂.
- Genes on one chromosome are linked; their recombination frequency (test-cross minority classes) measures distance in centimorgans, capped at 50%.
- Sex-linked recessives (colour blindness, haemophilia, white eye in *Drosophila*) hit hemizygous males, travel criss-cross through carrier females, and betray themselves by unequal reciprocal crosses.
- Mutations change bases (substitutions, frameshifts), chromosome structure, or chromosome number; non-disjunction produces the aneuploid syndromes.
- Polyploidy multiplies whole sets: triploids are sterile (seedless fruit), doubled hybrids are fertile new species (bread wheat, *Triticale*).
- Count the karyotype to name the syndrome: 45,XO Turner (female), 47,XXY Klinefelter (male), +21 Down, +18 Edwards; albinism is autosomal recessive (no tyrosinase), haemophilia X-linked recessive (no factor VIII).

## Practice questions

**Set A — Recall (25 questions)**

1. The father of genetics is
   (a) Hugo de Vries (b) T. H. Morgan (c) Charles Darwin (d) Gregor Johann Mendel
2. Mendel performed his hybridisation experiments on
   (a) *Drosophila melanogaster* (b) *Pisum sativum* (c) *Mirabilis jalapa* (d) *Oenothera lamarckiana*
3. The alternative forms of a gene are called
   (a) loci (b) phenotypes (c) alleles (d) genomes
4. The phenotypic ratio in the F₂ of a monohybrid cross is
   (a) 1 : 2 : 1 (b) 3 : 1 (c) 1 : 1 (d) 9 : 3 : 3 : 1
5. The F₂ phenotypic ratio of a dihybrid cross with unlinked genes is
   (a) 3 : 1 (b) 9 : 3 : 3 : 1 (c) 1 : 1 : 1 : 1 (d) 1 : 2 : 1
6. A test cross is a cross between the individual to be tested and a
   (a) homozygous dominant (b) heterozygous (c) pure tall parent (d) homozygous recessive
7. The law of segregation is also called the law of
   (a) purity of gametes (b) independent assortment (c) dominance (d) linkage
8. The classic example of incomplete dominance is flower colour in
   (a) garden pea (b) *Mirabilis jalapa* (c) maize (d) sweet pea
9. In incomplete dominance the F₂ ratio of phenotypes is
   (a) 3 : 1 (b) 1 : 1 (c) 1 : 2 : 1 (d) 9 : 7
10. The AB blood group, in which both antigens appear together, is an example of
   (a) incomplete dominance (b) co-dominance (c) recessiveness (d) epistasis
11. Genes located on the same chromosome and inherited together are called
   (a) linked genes (b) alleles (c) multiple alleles (d) lethal genes
12. Linkage was first observed by Bateson and Punnett in
   (a) sweet pea (*Lathyrus*) (b) *Drosophila* (c) maize (d) garden pea
13. The concept of linkage and the chromosome theory of linkage were developed by
   (a) Hugo de Vries (b) T. H. Morgan (c) Sturtevant (d) Karpechenko
14. The number of linkage groups in an organism equals its
   (a) diploid chromosome number (b) total gene number (c) genome size (d) haploid chromosome number
15. Crossing over takes place between
   (a) sister chromatids of one chromosome (b) non-homologous chromosomes (c) non-sister chromatids of homologues (d) a chromatid and the centromere
16. One centimorgan (map unit) equals
   (a) 10% recombination (b) 1% recombination (c) 50% recombination (d) 0.1% recombination
17. White eye colour in *Drosophila*, studied by Morgan, is
   (a) autosomal dominant (b) Y-linked (c) autosomal recessive (d) X-linked recessive
18. Colour blindness is much commoner in men than in women because men are, for X-linked genes,
   (a) hemizygous (b) homozygous (c) heterozygous (d) triploid
19. The term "mutation" was introduced by
   (a) Hugo de Vries (b) Mendel (c) Morgan (d) Bateson
20. Insertion of a single extra base into a gene produces a
   (a) silent mutation (b) substitution (c) transition (d) frameshift mutation
21. Which of the following is a chemical mutagen?
   (a) nitrous acid (b) visible light (c) water (d) carbon dioxide
22. Colchicine induces polyploidy by
   (a) breaking chromosomes (b) stopping DNA replication (c) preventing spindle formation (d) dissolving the cell wall
23. Down syndrome is caused by
   (a) trisomy of chromosome 18 (b) monosomy of X (c) an extra Y chromosome (d) trisomy of chromosome 21
24. Turner syndrome has the karyotype
   (a) 47, XXY (b) 47, +21 (c) 45, XO (d) 46, XX
25. Haemophilia results from a deficiency of blood-clotting
   (a) factor II (b) fibrinogen (c) factor VIII (d) vitamin K

::: note Answers and explanations — Set A
**1.** (d) — Mendel's 1866 pea experiments founded genetics; de Vries was one of its rediscoverers in 1900.
**2.** (b) — *Pisum sativum* (garden pea), 1856–63, seven pairs of contrasting characters.
**3.** (c) — Alleles occupy the same locus on homologous chromosomes.
**4.** (b) — TT and Tt look alike, so 1 TT : 2 Tt : 1 tt appears as 3 tall : 1 dwarf.
**5.** (b) — Two independent 3 : 1 ratios combine as (3 : 1)² = 9 : 3 : 3 : 1.
**6.** (d) — Only the homozygous recessive partner lets the tested parent's gametes show directly in the progeny.
**7.** (a) — Each gamete carries just one allele of a pair, uncontaminated by the other.
**8.** (b) — Red × white *Mirabilis* gives pink F₁ (also *Antirrhinum*).
**9.** (c) — 1 red : 2 pink : 1 white; phenotype matches genotype because the heterozygote looks distinct.
**10.** (b) — Both I^A^ and I^B^ express fully side by side; nothing is blended.
**11.** (a) — Linked genes sit on one chromosome and tend to enter gametes together.
**12.** (a) — Bateson and Punnett (1906), sweet pea flower colour and pollen shape; they called it coupling and repulsion.
**13.** (b) — T. H. Morgan (1910) explained linkage chromosomally using *Drosophila*; Hugo de Vries was his student.
**14.** (d) — One linkage group per chromosome type: *Drosophila* 4, humans 23.
**15.** (c) — Exchange is between non-sister chromatids of the two homologues at pachytene.
**16.** (b) — Sturtevant's map unit: 1% recombinant offspring in a test cross.
**17.** (d) — Morgan, 1910: white eye is recessive and carried on the X — the first gene placed on a chromosome.
**18.** (a) — With only one X, a single recessive allele is enough to express the trait in males.
**19.** (a) — Hugo de Vries coined it for sudden variations in *Oenothera* (worked example of history questions).
**20.** (d) — Adding one base shifts every downstream codon: a frameshift.
**21.** (a) — Nitrous acid (also EMS, mustard gas, 5-bromouracil) chemically alters bases.
**22.** (c) — Colchicine blocks spindle microtubules, so the replicated chromosomes stay in one nucleus and the sets double.
**23.** (d) — An extra chromosome 21 (usually from maternal non-disjunction), karyotype 47, +21.
**24.** (c) — A single X and no second sex chromosome: 45, XO, a sterile female.
**25.** (c) — Haemophilia A, the common type, lacks factor VIII; type B lacks factor IX.
:::

**Set B — Understanding (15 questions)**

1. The reappearance of dwarf plants in the F₂, after an all-tall F₁, shows that the recessive allele
   (a) was created anew in F₂ (b) had mutated back (c) survived unchanged in the heterozygote (d) had blended with the dominant
2. A test-cross ratio tells us the genotype of the tested parent because the offspring phenotypes copy its
   (a) gamete types and their frequencies (b) chromosome number (c) somatic mutations (d) parent's phenotype
3. Incomplete dominance does not contradict Mendel because in the F₂
   (a) the pink plants breed true (b) no white plants appear (c) dominance returns (d) the pure parental types reappear and the ratio is 1 : 2 : 1
4. A blood-group A father and B mother can have an O child only if both parents are
   (a) homozygous for their alleles (b) blood group AB (c) younger than 30 (d) heterozygous, carrying the i allele
5. In complete linkage, a dihybrid test cross gives
   (a) a 9 : 3 : 3 : 1 ratio (b) only the two parental combinations in equal numbers (c) four combinations equally (d) only recombinant offspring
6. The strength of linkage between two genes increases as
   (a) the distance between them increases (b) crossing over increases (c) the distance between them decreases (d) the chromosome shortens
7. Male *Drosophila* show complete linkage for genes on the same chromosome because
   (a) they are haploid (b) crossing over does not occur in males (c) they have no X chromosome (d) their chromosomes do not pair
8. Inheritance is called criss-cross when an X-linked character passes from
   (a) father to daughters and through them to grandsons (b) father directly to sons (c) mother to daughters only (d) grandfather to grandfather
9. A carrier woman for haemophilia is herself normal because
   (a) the gene is on the Y chromosome (b) haemophilia needs two X chromosomes (c) her normal allele on the other X is dominant (d) the allele is deleted in women
10. Trisomy in a child is most directly explained by
   (a) crossing over in the father (b) non-disjunction during meiosis in a parent (c) polyploidy in the zygote (d) a frameshift mutation
11. An allopolyploid differs from an autopolyploid in that its chromosome sets come from
   (a) two different species (b) one species only (c) bacteria (d) the same parent cell twice
12. A frameshift mutation is usually more harmful than a substitution because it
   (a) changes the chromosome number (b) affects only one amino acid (c) changes every codon after the mutation site (d) deletes a whole chromosome
13. Triploid (3n) bananas are seedless because in meiosis the three chromosome sets
   (a) fail to replicate (b) cannot pair and separate evenly, so gametes are unbalanced (c) are all recessive (d) fuse into one set
14. Two normally pigmented parents have an albino child. Albinism must be inherited as an
   (a) autosomal dominant (b) X-linked dominant (c) Y-linked trait (d) autosomal recessive, both parents being carriers
15. A person with karyotype 47, XXY is male because sex in humans is determined by the
   (a) presence of a Y chromosome (b) number of X chromosomes (c) number of autosomes (d) mother

::: note Answers and explanations — Set B
**1.** (c) — Segregation: the t allele was masked in Tt plants, not altered, and sorts cleanly into gametes.
**2.** (a) — The recessive tester contributes only recessive alleles, so each offspring's phenotype displays one gamete from the tested parent.
**3.** (d) — Red and white return pure in a 1 : 2 : 1 F₂: alleles segregated exactly as Mendel required; only dominance is incomplete.
**4.** (d) — An O child is ii, so each parent must carry i: I^A^i × I^B^i.
**5.** (b) — No crossing over means only parental gametes (AB and ab), giving two progeny classes equally.
**6.** (c) — Nearer genes are less often separated by a crossover, so linkage is stronger.
**7.** (b) — Crossing over is absent in male *Drosophila* (and in female silkworms), a favourite named exception.
**8.** (a) — The father's X goes to his daughters, who pass it to their sons: grandfather → daughter → grandson.
**9.** (c) — X^H^X^h^ makes enough factor VIII from the normal allele; only X^h^X^h^ females are haemophilic.
**10.** (b) — Failure of homologues or chromatids to part gives an n + 1 gamete; fertilisation yields 2n + 1.
**11.** (a) — Amphidiploids combine whole genomes of two species and then double; autopolyploids multiply one genome.
**12.** (c) — The reading frame shifts, so the entire downstream amino-acid sequence — and usually a premature stop — follows.
**13.** (b) — Three homologues cannot split 1 : 1; near all gametes are aneuploid and inviable, so no seeds form.
**14.** (d) — Affected child from unaffected parents is the signature of recessive inheritance; both parents are Aa.
**15.** (a) — The Y (SRY region) imposes maleness whatever the X count: XXY male, XO female.
:::

**Set C — Application (10 questions)**

1. A monohybrid cross Tt × Tt produces 640 F₂ plants. The expected number of dwarf plants is
   (a) 480 (b) 320 (c) 160 (d) 64
2. A dihybrid F₂ (RrYy × RrYy) contains 1600 seeds. The expected number of wrinkled green (double recessive) seeds is
   (a) 300 (b) 100 (c) 900 (d) 400
3. A test cross gives 800 progeny, of which 85 + 75 are of the two recombinant types. The distance between the genes is
   (a) 10 cM (b) 16 cM (c) 20 cM (d) 40 cM
4. Selfing pink *Mirabilis* gives 200 offspring. The expected number of pink-flowered plants is
   (a) 50 (b) 150 (c) 100 (d) 200
5. A carrier woman (X^C^X^c^) marries a normal man. The probability that her son is colour blind is
   (a) 50% (b) 25% (c) 100% (d) 0%
6. Both parents are carriers (Aa) for albinism. Their normally pigmented child has what probability of being a carrier?
   (a) 1/4 (b) 1/2 (c) 1/3 (d) 2/3
7. A man of genotype I^A^i marries a woman of genotype I^B^i. The probability of an AB child is
   (a) 1/2 (b) 1/4 (c) 3/4 (d) 0
8. A carrier woman for haemophilia marries a haemophilic man. The probability that a daughter is haemophilic is
   (a) 0% (b) 25% (c) 100% (d) 50%
9. In the cross Tt × Tt, the probability that an offspring is both tall and heterozygous is
   (a) 1/2 (b) 1/4 (c) 3/4 (d) 2/3
10. In a dihybrid test cross the parental combinations together make 83% of the progeny. The genes are separated by
   (a) 17 cM (b) 83 cM (c) 34 cM (d) 8.5 cM

::: note Answers and explanations — Set C
**1.** (c) — Dwarfs are 1/4 of the F₂: $640 \times \tfrac{1}{4} = 160$.
**2.** (b) — The double recessive is 1/16 of a 9 : 3 : 3 : 1 F₂: $1600/16 = 100$.
**3.** (c) — RF $= (85 + 75)/800 \times 100 = 20\%$, so 20 cM.
**4.** (c) — Incomplete dominance gives 1 red : 2 pink : 1 white; half of 200 = 100 pink.
**5.** (a) — Sons get their X from their mother, who passes X^c^ to half of them.
**6.** (d) — Normal children of Aa × Aa are 1 AA : 2 Aa, so 2 out of 3 normals are carriers.
**7.** (b) — AB needs I^A^ from father (1/2) and I^B^ from mother (1/2): $1/2 \times 1/2 = 1/4$.
**8.** (d) — Daughters all receive X^h^ from their haemophilic father; half also receive X^h^ from their carrier mother and are X^h^X^h^.
**9.** (a) — Tt genotypes are 2/4 of the progeny, and all of them are tall: 1/2.
**10.** (a) — Recombinants $= 100 - 83 = 17\%$, which is the map distance, 17 cM.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. State and explain Mendel's laws with monohybrid and dihybrid crosses and the test cross. <span class="marks">[10]</span>
2. Explain linkage, sex-linked inheritance, mutation and any two genetic disorders. <span class="marks">[10]</span>

```photogrid label="9.H" cols="3" ratio="1.25" caption="Inheritance in plants and people. (a) Mendel's pea characters, such as round or wrinkled seed and tall or dwarf plant. (b) An Ishihara plate for testing red-green colour blindness, an X-linked recessive trait. (c) White-eyed Drosophila, an X-linked mutant found by Morgan."
@ photo id="ceebot/mendel-chars" cap="(a) Mendel's pea characters"
fit 1.25
focus 0.5 0.5
@ photo id="ceebot/ishihara" cap="(b) Ishihara colour test"
fit 1.25
focus 0.5 0.5
@ photo id="ceebot/drosophila-white" cap="(c) White-eyed Drosophila"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Mendel's laws (10 marks)

**Introduction.** **Gregor Johann Mendel** (1822-1884) worked on garden pea (*Pisum sativum*) for eight years, and published in 1866. The pea was a good choice because of its distinct contrasting characters, self-pollination, a short life cycle and many offspring.

**Terms.** Gene, allele, dominant, recessive, homozygous, heterozygous, **genotype** (genetic make-up) and **phenotype** (appearance), $\text{P}$, $\text{F}_1$ and $\text{F}_2$.

**Law of dominance.** When two contrasting alleles are present, only one (the dominant) is expressed in the $\text{F}_1$.

**Law of segregation (purity of gametes).** The two alleles of a gene separate during gamete formation, so each gamete gets only one. **Monohybrid cross:** $\text{TT}$ (tall) $\times$ $\text{tt}$ (dwarf) gives $\text{F}_1$ $\text{Tt}$ (all tall). Selfing gives $\text{F}_2$ with the **phenotypic ratio $3:1$** and the **genotypic ratio $1:2:1$** ($\text{TT} : \text{Tt} : \text{tt}$).

**Law of independent assortment.** The alleles of different genes assort independently into gametes. **Dihybrid cross:** $\text{RRYY}$ (round yellow) $\times$ $\text{rryy}$ (wrinkled green) gives $\text{F}_1$ $\text{RrYy}$. The $\text{F}_2$ phenotypic ratio is $9:3:3:1$ (round yellow : round green : wrinkled yellow : wrinkled green), with $16$ combinations from $4$ types of gamete ($\text{RY}$, $\text{Ry}$, $\text{rY}$, $\text{ry}$).

| Cross | Phenotypic ratio | Genotypic ratio |
|---|---|---|
| Monohybrid | $3:1$ | $1:2:1$ |
| Dihybrid | $9:3:3:1$ | $1:2:1:2:4:2:1:2:1$ |
| Test cross (with a recessive) | $1:1$ if heterozygous | $1:1$ |
| Incomplete dominance (*Mirabilis*) | $1:2:1$ | $1:2:1$ |
| Codominance (ABO blood groups) | | |

**Test cross.** Crossing an individual of dominant phenotype with a **homozygous recessive** to find its genotype. All dominant offspring means that the parent was homozygous, and a $1:1$ ratio means that it was heterozygous. A **back cross** is a cross of the $\text{F}_1$ with either parent.

**Extensions.** **Incomplete dominance:** the $\text{F}_1$ is intermediate (pink in snapdragon). **Codominance:** both alleles are expressed ($\text{I}^\text{A}\text{I}^\text{B}$ gives blood group AB). **Multiple alleles:** ABO has three alleles ($\text{I}^\text{A}$, $\text{I}^\text{B}$ and $i$). **Pleiotropy:** one gene affects several characters.

**Numerical.** For the cross $\text{AaBb} \times \text{AaBb}$, the probability of $\text{aabb}$ is $\dfrac14\times\dfrac14 = \dfrac1{16}$ and of the dominant for both characters $\dfrac34\times\dfrac34 = \dfrac9{16}$. With $\text{F}_2$ of $1600$ plants, the number of tall plants is $1200$ and dwarf $400$. The cross $\text{Aa} \times \text{aa}$ gives $50\%$ $\text{Aa}$.

**Conclusion.** Mendel's laws of dominance, segregation and independent assortment explain the transmission of characters through the gametes.

### Model answer D2: linkage, sex linkage and mutation (10 marks)

**Introduction.** Mendel's independent assortment applies only to genes on different chromosomes. Genes on the same chromosome tend to be inherited together.

**Linkage and crossing over.** **Morgan** showed **linkage** in *Drosophila*. The strength of linkage depends on the distance between genes. Crossing over in prophase I gives **recombinants**. The **recombination frequency** $= \dfrac{\text{recombinants}}{\text{total offspring}}\times100$, and $1\%$ recombination equals one **map unit** (centimorgan). Sturtevant made the first genetic map.

**Sex determination.** In humans, females are $\text{XX}$ and males $\text{XY}$ (male heterogametic). In birds the female is $\text{ZW}$. In grasshoppers it is $\text{XO}$. The sex of the child is decided by the sperm.

**Sex-linked inheritance.** Genes on the X chromosome. A recessive X-linked trait shows more often in males, because the male has only one X (hemizygous), and **skips a generation** through carrier females. Examples: **red-green colour blindness**, **haemophilia** and white eye in *Drosophila*. A carrier mother ($\text{X}^\text{C}\text{X}^\text{c}$) and a normal father ($\text{X}^\text{C}\text{Y}$) have sons with a $50\%$ chance of colour blindness and no affected daughters (half the daughters are carriers).

**Mutation.** A sudden, heritable change in the genetic material.

1. **Gene (point) mutation:** substitution (sickle-cell anaemia: GAG changed to GUG, so glutamic acid is replaced by valine), insertion or deletion (**frame shift**).
2. **Chromosomal mutation:** deletion, duplication, inversion and translocation.
3. **Genome mutation (ploidy):** aneuploidy and polyploidy.
4. **Mutagens:** X-rays, UV, chemicals (mustard gas) and colchicine, which induces polyploidy.

**Genetic disorders.**

| Disorder | Cause | Features |
|---|---|---|
| Down syndrome | trisomy $21$ ($47$ chromosomes) | mental retardation, short stature |
| Turner syndrome | $44 + \text{XO}$ | sterile female |
| Klinefelter syndrome | $44 + \text{XXY}$ | sterile male |
| Sickle-cell anaemia | recessive point mutation | abnormal haemoglobin, **autosomal** |
| Haemophilia | X-linked recessive | blood does not clot |
| Phenylketonuria | autosomal recessive, enzyme missing | brain damage |

**Numerical.** If $12$ recombinants occur among $100$ offspring, the genes are $12$ map units apart. For a colour-blind man ($\text{X}^\text{c}\text{Y}$) and a normal homozygous woman, all children are phenotypically normal, but all daughters are carriers. The chance that a carrier woman has a colour-blind **child** is $\tfrac14$.

**Conclusion.** Linked genes are inherited together unless separated by crossing over, and mutations cause variation and genetic disorders.

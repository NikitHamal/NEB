---
subject: Zoology
grade: CEE
unit: 11
title: Reproductive System
hours: 2
area: Human Biology and Physiology
---

The reproductive system is rated at **2 questions** on the 40-question Zoology paper. The questions are usually anatomical or
sequence-based: where sperms form and mature, which cells make testosterone or
nourish gametes, why one primary oocyte gives one ovum while one primary
spermatocyte gives four sperms, and how FSH, LH, oestrogen and progesterone
order the menstrual cycle.

::: key What the paper asks from this chapter
- Male route: **seminiferous tubule → rete testis → epididymis → vas deferens → ejaculatory duct → urethra**. Sertoli cells nourish developing sperms; Leydig cells make testosterone.
- The scrotum holds the testes about **2–2.5 °C below core temperature**, as required for normal spermatogenesis.
- Female route: **ovary → fimbriae/infundibulum → ampulla → isthmus → uterus → cervix → vagina**. Fertilisation is normally in the **ampulla**.
- One primary spermatocyte forms **four sperms**; one primary oocyte forms **one ovum plus polar bodies** because cytokinesis is unequal.
- The cell ovulated is a **secondary oocyte** arrested in metaphase II; it completes meiosis only after sperm entry.
- Cycle logic: FSH grows a follicle → oestrogen rebuilds endometrium → high oestrogen triggers the **LH surge** → ovulation → corpus luteum secretes progesterone.
- **hCG** from the early embryo/placenta rescues the corpus luteum in pregnancy and is detected by pregnancy tests.
:::

## 11.1 Male and female reproductive organs

Human reproduction is sexual, with internal fertilisation and development of
the embryo inside the uterus (**viviparity**). The gonads have two inseparable
roles: they produce haploid gametes and secrete sex hormones.

### Male reproductive system

The **testes** are paired oval gonads suspended in the **scrotum**. Dartos and
cremaster muscles alter scrotal position and surface area, keeping the testes
cooler than the abdomen. Each testis contains many coiled
**seminiferous tubules**, where sperm are produced. Within their walls:

```photo id="bio12/male-repro-nci" caption="The human reproductive systems. (a) Male, sectional side view." width="66"
```


- spermatogenic cells undergo mitosis/meiosis to form sperm;
- **Sertoli cells** support, nourish and protect developing germ cells, form
  the blood–testis barrier, and secrete inhibin and androgen-binding protein;
- between tubules, **Leydig (interstitial) cells** secrete testosterone when
  stimulated by LH.

Sperm leave through the rete testis and vasa efferentia to the
**epididymis**, a long, tightly coiled duct where they mature, gain motility
and are stored. During ejaculation, each **vas deferens** propels sperm to an
ejaculatory duct and then the urethra. Thus a vasectomy, which cuts/seals the
vas deferens, prevents sperm reaching semen but does not normally remove the
testes' testosterone secretion into blood.

Accessory glands produce most of the volume of **semen**:

| Gland | Contribution/function |
|---|---|
| **Seminal vesicles** | fructose-rich fluid providing an energy substrate; prostaglandins and clotting factors |
| **Prostate gland** | thin secretion with enzymes/citrate/zinc; helps semen liquefaction and sperm function |
| **Bulbourethral (Cowper's) glands** | clear mucus lubrication and neutralisation of residual urinary acidity |

The penis delivers semen into the vagina. Its urethra is a common passage for
urine and semen, though sphincter coordination prevents normal simultaneous
flow during ejaculation.

### Structure of a sperm

A sperm is a stripped-down delivery vehicle for a haploid nucleus. Its
**acrosome** is a lysosome-like cap containing enzymes for penetrating the
oocyte investments. Behind it, the head is mostly compact nucleus. The
**middle piece** contains helically arranged mitochondria supplying ATP to the
flagellar axoneme of the **tail**. Almost all cytoplasm is discarded during
maturation—one reason the ovum supplies nearly all cytoplasm and mitochondria
to the zygote.

```figure caption="A human sperm. The acrosome and nucleus form the head; mitochondria of the middle piece power the flagellar tail."
from matplotlib.patches import Ellipse, Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.2, 2.8))
# tail
x = np.linspace(4.05, 9.55, 400)
y = 0.34*np.sin(2.0*(x-4.05))*np.exp(-0.08*(x-4.05))
ax.plot(x, y, color='#7a5b23', lw=2.2, solid_capstyle='round', zorder=2)
# middle piece and neck
ax.add_patch(Rectangle((2.82,-0.31),1.25,0.62,fc='#f6d9a8',ec='#8a6a20',lw=1.0,zorder=3))
for xx in np.linspace(3.02,3.86,5):
    ax.add_patch(Circle((xx,0),0.13,fc='#d88c3a',ec='#8a4f18',lw=0.5,zorder=4))
ax.add_patch(Rectangle((2.55,-0.22),0.27,0.44,fc='#d8d2c4',ec=MUTED,lw=0.8,zorder=3))
# head: nucleus and acrosome cap
ax.add_patch(Ellipse((1.70,0),1.95,1.22,fc='#dbeafe',ec='#315f9f',lw=1.2,zorder=4))
ax.add_patch(Ellipse((1.98,0),1.05,0.78,fc='#648dc4',ec='#315f9f',lw=0.7,zorder=5))
ax.add_patch(Ellipse((1.03,0),0.78,1.02,fc='#f2c14e',ec='#9a7114',lw=0.9,zorder=6))
labels=[('acrosome\n(enzymes)',(0.35,1.62),(0.98,0.42)),
        ('nucleus (n = 23)',(2.08,1.18),(1.98,0.42)),
        ('middle piece\n(mitochondria)',(4.35,1.62),(3.55,0.34)),
        ('neck / centrioles',(2.75,-1.55),(2.68,-0.26)),
        ('tail (flagellum)',(8.25,-1.58),(8.20,-0.10))]
for txt,(tx,ty),(px,py) in labels:
    ax.text(tx,ty,txt,fontsize=6.5,color=INK,ha='center',va='center',zorder=10)
    sy=ty-0.34 if py<ty else ty+0.34
    ax.plot([tx,px],[sy,py],color=MUTED,lw=0.65,zorder=9)
ax.set_xlim(-0.25,9.85); ax.set_ylim(-1.95,1.95)
ax.set_aspect('equal'); ax.axis('off')
```

### Female reproductive system

The **ovaries** lie in the pelvic cavity. Each contains follicles at different
stages. A mature follicle ruptures at ovulation and then transforms into an
endocrine corpus luteum; most follicles instead undergo atresia.

```photo id="bio12/female-repro" caption="(b) Female, front view of the pelvic organs." width="66"
```


Each **uterine (fallopian) tube** has:

1. **Infundibulum** with fimbriae that sweep over the ovary and capture the
   released secondary oocyte.
2. **Ampulla**, the wider middle region and normal site of fertilisation.
3. **Isthmus**, the narrower portion joining the uterus.

Cilia and smooth-muscle contractions move the oocyte/early embryo toward the
uterus. A blocked tube can therefore cause infertility even when ovulation is
normal, or permit a dangerous tubal (ectopic) implantation.

The **uterus** has a fundus, body and cervix. Its wall comprises the outer
perimetrium, thick smooth-muscle **myometrium** and inner **endometrium**.
The endometrial functional layer proliferates, becomes secretory, supports
implantation or is shed in menstruation. The cervix opens into the
**vagina**, which receives the penis/semen, forms part of the birth canal and
conducts menstrual flow. External genitalia are collectively the vulva.

At puberty, gonadotropins activate gonadal hormone production. Testosterone
promotes male secondary sexual characters—growth of reproductive organs,
facial/body hair, voice deepening and increased muscle mass. Oestrogens promote
female reproductive-tract development, breast development and characteristic
fat distribution; progesterone principally prepares the uterus and mammary
glands for pregnancy/lactation.


```figure caption="Spermatogenesis in four stages: mitosis keeps the spermatogonium stock diploid, meiosis I halves the chromosome number into two secondary spermatocytes, meiosis II gives four haploid spermatids, and spermiogenesis dresses each spermatid as a swimming spermatozoon — four fertile cells from every starter."
flow([("mitosis", "spermatogonium 2n\n→ primary 2n"),
      ("meiosis I", "primary 2n →\n2 secondary n"),
      ("meiosis II", "2 secondary n →\n4 spermatids n"),
      ("spermiogenesis", "spermatids →\nspermatozoa")])
```

::: caution
Two site-questions the paper repeats: **fertilisation happens in the
oviduct (ampulla), not the uterus**, and **implantation happens in the
endometrium of the uterus, not the oviduct** — an ectopic pregnancy is
precisely implantation in the wrong place. And sperm **mature in the
epididymis**, not in the tubules where they are made.
:::
## 11.2 Gametogenesis

**Gametogenesis** is gamete formation. It combines proliferation by mitosis,
reduction by meiosis and differentiation. Meiosis halves chromosome number
from 46 to 23 and creates genetic variation through crossing over and
independent assortment.

### Spermatogenesis

Spermatogenesis begins at puberty and normally continues throughout adult
life in the seminiferous tubules. Spermatogonia (2n) divide mitotically; some
become **primary spermatocytes (2n)**. Meiosis I forms two
**secondary spermatocytes (n, duplicated chromosomes)**, and meiosis II forms
four **spermatids (n)**. During **spermiogenesis** (not another division),
each spermatid loses cytoplasm, forms an acrosome and flagellum and becomes a
spermatozoon. The complete production process takes roughly two to three
months, followed by epididymal maturation.

LH stimulates Leydig cells to secrete testosterone. FSH and high local
testosterone act through Sertoli cells to sustain spermatogenesis. Inhibin
from Sertoli cells selectively suppresses FSH secretion.

### Oogenesis

Oogenesis begins before birth. Fetal oogonia produce **primary oocytes** that
enter meiosis I and arrest in prophase I within primordial follicles. A female
is therefore born with a finite oocyte pool—commonly estimated at roughly
1–2 million at birth, falling by atresia to a few hundred thousand by puberty.
Only around 400–500 are normally ovulated in a lifetime.

After puberty, a cohort of follicles develops in each cycle. Usually one
dominant follicle completes meiosis I just before ovulation, producing:

- a large **secondary oocyte**, retaining nearly all cytoplasm; and
- a small **first polar body**.

The secondary oocyte begins meiosis II but arrests at metaphase II and is the
cell ovulated. Only if a sperm penetrates it does it complete meiosis II,
forming the mature ovum and second polar body. The first polar body may also
divide, so one primary oocyte can yield one ovum and up to three polar bodies.

| Feature | Spermatogenesis | Oogenesis |
|---|---|---|
| Site | seminiferous tubules | ovarian follicles |
| Starts | puberty | fetal life |
| Pattern | continuous, enormous numbers | cyclic, usually one dominant oocyte per cycle |
| Cytokinesis | essentially equal | highly unequal |
| Meiotic products | 4 spermatids → 4 sperm | 1 ovum + polar bodies |
| Meiotic arrests | none prolonged | prophase I for years; metaphase II until fertilisation |
| Ends | declines with age, no abrupt universal endpoint | menopause when follicle pool/function is exhausted |

### Fertilisation, implantation and gestation

Sperm deposited in the vagina must traverse the cervix and uterus into a
uterine tube and undergo **capacitation**, a final functional maturation in
the female tract. At the oocyte, sperm pass through the corona radiata; the
acrosome reaction helps penetration of the zona pellucida. Fusion of one sperm
triggers cortical-granule release and zona changes that block
**polyspermy**. The secondary oocyte completes meiosis II; male and female
pronuclei combine to restore diploidy in the **zygote**.

Cleavage produces a morula and then a fluid-filled **blastocyst**. Around
6–7 days after fertilisation, the blastocyst begins **implantation** in the
secretory endometrium. Trophoblast and maternal tissues form the
**placenta**, across which gases, nutrients and wastes exchange by diffusion
and transport. Maternal and fetal blood normally remain separate. The placenta
also secretes hCG initially and later large amounts of oestrogen and
progesterone.

A typical pregnancy lasts about **40 weeks (280 days) from the first day of
the last menstrual period**, equivalent to about 38 weeks from fertilisation.
At parturition, uterine contractions are strengthened by oxytocin in a
positive-feedback loop. After birth, prolactin supports milk production and
oxytocin causes milk ejection; early **colostrum** is especially rich in
protective antibodies.


::: example Worked example — counting gametes from meiotic products
How many functional gametes are produced from **50 primary spermatocytes** and from **50 primary oocytes**?

- Each primary spermatocyte completes both meiotic divisions equally, giving **4 spermatids → 4 sperms**. Total = 50 × 4 = **200 sperms**.
- In oogenesis the divisions are unequal: each primary oocyte gives only **1 functional ovum** (the rest of the material goes to polar bodies). Total = 50 × 1 = **50 ova** (plus polar bodies, which degenerate).

Now the variations become one-step: 25 *secondary* spermatocytes → 25 × 2 = 50 sperms; and "how many polar bodies from 10 primary oocytes" — up to 3 per oocyte (one from meiosis I, which may itself divide, and one from meiosis II), so a maximum of **30**.
:::

::: caution Trap — place and cell mix-ups in reproduction
Fertilisation occurs in the **ampulla of the fallopian (uterine) tube**, not in the uterus. Sperms are **produced** in the seminiferous tubules but **mature and are stored** in the **epididymis**. **Sertoli** cells nourish the developing sperms and secrete inhibin; **Leydig (interstitial)** cells secrete testosterone — MCQs routinely exchange these two.
:::

```photogrid label="11.1" cols="2" ratio="1.2" caption="Counting the cells made by meiosis. (a) A diagram of a human spermatozoon: head with acrosome, middle piece of mitochondria, and a tail. (b) Start with 100 primary germ cells (2n = 46). In the male each primary spermatocyte gives 2 secondary spermatocytes and then 4 spermatids, so 100 give 400 sperm, all functional. In the female each primary oocyte gives 1 ovum and 3 polar bodies, because the cytoplasm is shared unequally, so 100 give 100 ova and 300 polar bodies that die. The female stores the food for the zygote; the male makes many small mobile cells."
@ photo id="bio12/sperm" cap="Human spermatozoon (diagram)"
fit 1.2
focus 0.5 0.5
@ svg cap="Cells after each division from 100 germ cells"
n0 = 100
male = [n0, n0 * 2, n0 * 4]
female_func = [n0, n0, n0]
polar = [0, n0, n0 * 3]
assert male[-1] == 400 and polar[-1] == 300
facts = dict(s=male[-1], o=female_func[-1], pb=polar[-1])
f = Fig(300, 236)
f.text(150, 12, "Spermatogenesis and oogenesis", size=10.5, color=NAVY, bold=True)
heads = ("2n = 46", "meiosis I", "meiosis II")
fem = ("100 oocytes", "100 second.\noocytes", "100 ova")
for j, h in enumerate(heads):
    f.text(90 + j * 82, 30, h, size=10.5, color=SLATE, bold=True)
f.text(4, 70, "male", size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(4, 140, "female", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
for j in range(3):
    x = 54 + j * 82
    f.box(x, 44, 72, 40, fill=MINT, stroke=TEAL, r=3, label="%d\n%s" % (male[j], "cells" if j == 0 else "n = 23"), size=10.5, bold=True)
    f.box(x, 112, 72, 36, fill=ROSE, stroke=RED, r=3, label=fem[j], size=10.5, bold=True)
    if polar[j]:
        f.box(x, 154, 72, 26, fill="#f1f5f9", stroke=SLATE, r=3, label="%d polar" % polar[j], size=10.5, bold=True, dash=True)
f.text(150, 206, "100 spermatocytes -> 400 sperm", size=10.5, color=TEAL, bold=True)
f.text(150, 222, "100 oocytes -> 100 ova + 300 polar bodies", size=10.5, color=RED, bold=True)
```

## 11.3 The ovarian and menstrual cycles

The ovarian cycle (follicle growth, ovulation and corpus luteum) and uterine/
menstrual cycle (endometrial change) are two views of one hormonal sequence.
Day 1 is defined as the first day of menstrual bleeding. A 28-day cycle is a
teaching average; healthy adult cycles commonly vary, and much of the
variation lies in the pre-ovulatory follicular phase.

```figure caption="The hormonal and uterine pattern of an idealised 28-day cycle. The mid-cycle LH surge triggers ovulation; progesterone dominates the secretory phase."
fig, axs = plt.subplots(2, 1, figsize=(5.2, 3.3), sharex=True,
                        gridspec_kw=dict(height_ratios=[1.25, 0.70], hspace=0.16))
t = np.linspace(0, 28, 601)
def bump(c,w,h): return h*np.exp(-0.5*((t-c)/w)**2)
FSH=24+bump(3.5,3.0,24)+bump(13.6,1.0,26)
LH=15+bump(13.8,0.72,94)
OES=13+bump(12.6,2.1,76)+bump(21.5,4.0,30)
PRO=5+bump(21.5,4.2,80)
ax=axs[0]
ax.plot(t,FSH,color=SERIES[0],lw=1.6)
ax.plot(t,LH,color=SERIES[1],lw=1.8)
ax.plot(t,OES,color=SERIES[2],lw=1.6,ls='--')
ax.plot(t,PRO,color=SERIES[3],lw=1.6,ls='--')
for x in (5,14,28): ax.axvline(x,color=GRID,lw=0.8,zorder=0)
ax.set_ylim(0,125); ax.set_yticks([])
ax.set_ylabel('hormone level\n(relative)',fontsize=6.5)
ax.text(2.0,58,'FSH',fontsize=6.5,color=SERIES[0],fontweight='bold')
ax.text(10.2,99,'oestrogen',fontsize=6.5,color=SERIES[2],ha='right')
ax.text(15.2,112,'LH surge',fontsize=6.5,color=SERIES[1],ha='left',fontweight='bold')
ax.text(23.5,94,'progesterone',fontsize=6.5,color=SERIES[3],ha='center')
ax.spines[['top','right']].set_visible(False); ax.tick_params(left=False)
ax=axs[1]
anchors_t=np.array([0,5,9,14,20,25,28]); anchors_y=np.array([3.2,0.7,2.0,4.2,5.5,5.1,3.1])
END=np.interp(t,anchors_t,anchors_y)
kernel=np.exp(-0.5*(np.arange(-25,26)/8)**2); kernel/=kernel.sum()
END=np.convolve(np.pad(END,25,mode='edge'),kernel,mode='valid')
ax.fill_between(t,0,END,color='#f0d3d3',zorder=2)
ax.plot(t,END,color='#b07878',lw=1.3,zorder=3)
for x in (5,14,28): ax.axvline(x,color=GRID,lw=0.8,zorder=1)
ax.set_ylim(0,6.8); ax.set_yticks([])
ax.set_ylabel('uterine\nlining',fontsize=6.5)
ax.set_xlabel('day of cycle')
ax.set_xlim(0,28); ax.set_xticks([1,5,10,14,20,28])
ax.text(2.5,1.7,'menses',fontsize=6.3,color='#a3302c',ha='center')
ax.text(9.4,0.85,'proliferative',fontsize=6.3,color=MUTED,ha='center')
ax.text(20.5,1.25,'secretory',fontsize=6.3,color=MUTED,ha='center')
ax.spines[['top','right','left']].set_visible(False); ax.tick_params(left=False)
```

### Phases of an idealised 28-day cycle

| Phase | Typical days | Ovary/hormones | Uterine event |
|---|---:|---|---|
| **Menstrual** | 1–5 | corpus luteum has regressed; oestrogen/progesterone low | functional endometrium sheds |
| **Follicular/proliferative** | about 6–13 | FSH recruits follicles; dominant follicle secretes rising oestrogen | endometrium regrows and thickens |
| **Ovulatory** | about 14 | sustained high oestrogen switches to positive feedback; **LH surge** (with smaller FSH rise) | follicle ruptures; secondary oocyte released |
| **Luteal/secretory** | about 15–28 | corpus luteum secretes progesterone plus oestrogen | glands secrete, vessels coil; lining prepared for implantation |

If pregnancy does not occur, the corpus luteum regresses to a corpus albicans.
Progesterone/oestrogen withdrawal causes endometrial breakdown and releases
the hypothalamus/pituitary from negative feedback, allowing FSH to rise for a
new cycle. If implantation occurs, trophoblast **hCG** maintains the corpus
luteum until the placenta can produce enough steroid hormones.

The released oocyte is fertilisable for roughly a day, while sperm may survive
in the female tract for up to about five days. The biologically fertile window
therefore spans several days ending soon after ovulation. Cycle-day estimates
are averages, not precise individual predictions.

::: example Estimating ovulation in a 32-day cycle
The luteal phase is often about 14 days and is usually less variable than the
follicular phase. For a regular 32-day cycle, ovulation is estimated at

$$32-14\approx\text{day }18$$

not automatically day 14. With sperm survival up to five days and oocyte
survival about one day, the approximate fertile interval would be days 13–19.
This calculation teaches the physiology; it is not a guarantee for an
individual cycle.
:::

**Menarche** is the first menstruation, marking pubertal activation of the
hypothalamo-pituitary-ovarian axis. **Menopause** is permanent cessation of
menstruation after ovarian follicular activity is lost, commonly around the
late forties to early fifties. As ovarian oestrogen and inhibin fall, loss of
negative feedback allows FSH (and LH) to become persistently high.


::: example Worked example — predicting the day of ovulation
The **luteal (post-ovulatory) phase is nearly constant at about 14 days**; it is the follicular phase that varies. So ovulation day ≈ cycle length − 14.

- 28-day cycle → ovulation about day **14**.
- 35-day cycle → ovulation about day **21**.
- 24-day cycle → ovulation about day **10**.

Notice the trap in the second case: answering "day 14" for every cycle length ignores that the extra days lengthen the *follicular* phase, not the luteal phase.
:::



```figure caption="The cycle's hormone curves and its two fixed events. FSH lifts a follicle whose oestrogen rebuilds the womb; the mid-cycle LH surge (day 14) bursts it; the corpus luteum then pours progesterone to hold the lining — and when the corpus luteum dies unfertilised, both hormones fall and menstruation begins. The luteal half is the constant: 14 days."
fig, ax = plt.subplots(figsize=(5.0, 3.0))
d = np.linspace(1, 28, 280)
lh = 8 + 60 * np.exp(-((d - 14) ** 2) / 1.6)
est = 20 + 55 * np.exp(-((d - 12) ** 2) / 9) + 25 * np.exp(-((d - 21) ** 2) / 18)
prog = 6 + 62 * np.exp(-((d - 21.5) ** 2) / 14)
ax.plot(d, lh, color=SERIES[0], lw=1.8)
ax.plot(d, est, color=SERIES[1], lw=1.5)
ax.plot(d, prog, color=SERIES[2], lw=1.5)
ax.axvspan(1, 5, color=MUTED, alpha=0.16)
ax.axvline(14, color=MUTED, lw=0.9, ls=":")
ax.text(3, 92, "menstruation", ha="center", fontsize=6.6, color=INK)
ax.text(14.6, 92, "ovulation", ha="left", fontsize=6.6, color=INK)
ax.text(22, 92, "luteal phase", ha="center", fontsize=6.6, color=INK)
ax.text(15.3, 52, "LH", fontsize=6.6, color=SERIES[0])
ax.text(7.6, 60, "oestrogen", fontsize=6.6, color=SERIES[1])
ax.text(24, 60, "progesterone", fontsize=6.6, color=SERIES[2])
ax.set_xlabel("day of cycle", fontsize=7.5); ax.set_ylabel("relative level", fontsize=7.5)
ax.set_xlim(1, 28); ax.set_ylim(0, 100); ax.set_xticks([1, 7, 14, 21, 28])
ax.spines[["top", "right"]].set_visible(False); ax.grid(color=GRID, lw=0.6)
ax.tick_params(labelsize=7.5)
```

::: example Ovulation day from cycle length, exactly as the paper asks
**Problem.** One woman's cycles run 32 days, another's 26. On which day does
each ovulate?
**Solution.** The luteal phase is the fixed half at ~14 days, so ovulation
falls 14 days **before the next period**: 32 − 14 = **day 18**, and
26 − 14 = **day 12**. Counting 14 from the *start* is the classic error —
only a 28-day cycle ovulates on day 14.
:::

::: memory
**FSH grows the follicle; oestrogen builds the lining; LH bursts the follicle
on day 14; progesterone holds the lining; the fall of both menstruates it.**
Five verbs, one cycle.
:::

::: tip
Cycle questions collapse to one identity: **ovulation = cycle length − 14**.
And gametogenesis questions collapse to two numbers: **4 sperm per
spermatogonium, 1 ovum (+3 polar bodies) per oogonium**.
:::

## Formula and fact sheet

- Sperm pathway: seminiferous tubule → rete testis → epididymis → vas deferens
  → ejaculatory duct → urethra.
- Sertoli = support/nurse/inhibin; Leydig = testosterone; LH acts on Leydig cells.
- Scrotal testes are about 2–2.5 °C cooler than the body core.
- Sperm head = acrosome + haploid nucleus; midpiece = mitochondria; tail = motility.
- Fertilisation: ampulla. Implantation: endometrium. Muscular uterine coat: myometrium.
- One primary spermatocyte → 4 sperm. One primary oocyte → 1 ovum + up to 3 polar bodies.
- Ovulated cell = secondary oocyte arrested in metaphase II.
- FSH grows follicles; oestrogen proliferates endometrium; LH surge ovulates;
  progesterone makes endometrium secretory.
- hCG maintains the corpus luteum in early pregnancy.
- Gestation ≈ 280 days from last menstrual period.
- Prolactin = milk production; oxytocin = milk ejection and uterine contraction.

### Rapid-revision tables and high-yield facts

| Quantity | Value |
|---|---|
| Scrotal temperature | ~2–3 °C below core |
| Spermatogenesis time / output | ~64 days / 4 sperm per spermatogonium |
| Ejaculate | 3–5 mL, 200–300 million sperm, pH ~7.2–7.8 |
| Oogenesis output | 1 ovum + 3 polar bodies per oogonium |
| Ovulations per lifetime | ~400–450 |
| Ovulation day | cycle length − 14 (day 14 if 28-day) |
| Fertilisation site / implantation site | oviduct ampulla / uterine endometrium |
| Egg viable / sperm viable | ~12–24 h / ~3–5 days |
| Pregnancy hormone (test) | hCG from the embryo |
| Menopause | ~45–50 years |

## Chapter summary

- The testes produce sperm in seminiferous tubules under FSH, testosterone and
  Sertoli-cell support; Leydig cells supply testosterone.
- Sperm mature and are stored in the epididymis, then travel through the vas
  deferens and urethra in semen produced mainly by accessory glands.
- The ovaries produce oocytes and steroid hormones; uterine tubes capture the
  oocyte and normally host fertilisation in the ampulla.
- Spermatogenesis is continuous and quantitatively equal, whereas oogenesis
  begins before birth, is interrupted twice and conserves cytoplasm in one ovum.
- Fertilisation restores diploidy, blocks polyspermy and initiates cleavage;
  the blastocyst implants in a progesterone-prepared endometrium.
- The menstrual cycle is driven by changing feedback among GnRH, FSH/LH,
  oestrogen and progesterone.
- Ovulation follows the LH surge, and the corpus luteum either regresses—
  causing menstruation—or is rescued by hCG in pregnancy.

## Practice questions

**Set A — Recall (25 questions)**

1. The primary male reproductive organs are the
   (a) testes (b) seminal vesicles (c) prostate glands (d) epididymides
2. Spermatozoa are produced in the
   (a) vas deferens (b) seminiferous tubules (c) epididymis (d) urethra
3. Developing germ cells are nourished and supported by
   (a) Leydig cells (b) spermatogonia (c) Sertoli cells (d) acrosomal cells
4. Testosterone is secreted by the
   (a) Sertoli cells (b) epididymis (c) prostate gland (d) Leydig cells
5. Spermatozoa mature and are stored mainly in the
   (a) seminiferous tubule (b) epididymis (c) seminal vesicle (d) urethra
6. Most fructose in human semen is supplied by the
   (a) prostate gland (b) testes (c) bulbourethral glands (d) seminal vesicles
7. Enzymes that help a sperm penetrate oocyte coverings are stored in the
   (a) midpiece (b) acrosome (c) tail (d) centriole
8. Mitochondria supplying ATP for sperm movement are concentrated in the
   (a) head (b) acrosome (c) neck only (d) middle piece
9. The female gonads are the
   (a) uterine tubes (b) uterus and cervix (c) ovaries (d) mammary glands
10. Fertilisation in humans normally occurs in the
   (a) ovary (b) uterus (c) vagina (d) ampulla of uterine tube
11. The blastocyst normally implants in the
   (a) myometrium (b) perimetrium (c) endometrium (d) cervix
12. The thick muscular layer of the uterus is the
   (a) myometrium (b) endometrium (c) perimetrium (d) mesometrium
13. Spermatogenesis normally begins at
   (a) birth (b) puberty (c) fertilisation (d) old age
14. One primary spermatocyte ultimately produces
   (a) four spermatozoa (b) two spermatozoa (c) one spermatozoon (d) eight spermatozoa
15. Oogenesis begins during
   (a) fetal life (b) puberty (c) pregnancy (d) menopause
16. The cell released at ovulation is a
   (a) primary oocyte (b) mature ovum (c) secondary oocyte (d) polar body
17. Complete oogenesis from one primary oocyte gives
   (a) one ovum and polar bodies (b) four equal ova (c) two ova only (d) eight ova
18. Day 1 of the menstrual cycle is the first day of
   (a) ovulation (b) menstrual bleeding (c) fertilisation (d) implantation
19. Ovulation is triggered most directly by a surge of
   (a) progesterone (b) LH (c) prolactin (d) inhibin
20. The corpus luteum secretes large amounts of
   (a) testosterone (b) FSH (c) progesterone (d) hCG
21. The proliferative rebuilding of endometrium is stimulated mainly by
   (a) oestrogen (b) progesterone (c) prolactin (d) oxytocin
22. The hormone detected by most early pregnancy tests is
   (a) LH (b) FSH (c) prolactin (d) hCG
23. Permanent cessation of menstrual cycles is called
   (a) menarche (b) puberty (c) menopause (d) implantation
24. A normal human sperm contains how many chromosomes?
   (a) 46 (b) 23 (c) 22 (d) 44
25. Exchange between maternal and fetal circulations occurs across the
   (a) amnion only (b) cervix (c) corpus luteum (d) placenta

::: note Answers and explanations — Set A
**1.** (a) — Testes are the male gonads producing sperm and testosterone.
**2.** (b) — Spermatogenesis occurs in seminiferous tubules.
**3.** (c) — Sertoli cells are the nurse/support cells of the tubule.
**4.** (d) — Interstitial Leydig cells secrete testosterone under LH.
**5.** (b) — The epididymis is the main site of sperm maturation and storage.
**6.** (d) — Seminal-vesicle fluid is rich in fructose.
**7.** (b) — The acrosome contains enzymes used in the acrosome reaction.
**8.** (d) — Middle-piece mitochondria power the flagellum.
**9.** (c) — Ovaries produce oocytes and female sex steroids.
**10.** (d) — The ampulla of the uterine tube is the normal fertilisation site.
**11.** (c) — Implantation occurs in the secretory endometrium.
**12.** (a) — Myometrium is the smooth-muscle coat of the uterus.
**13.** (b) — Continuous spermatogenesis starts with pubertal gonadotropin activation.
**14.** (a) — Two meiotic divisions and spermiogenesis yield four sperm.
**15.** (a) — Primary oocytes form and arrest before birth.
**16.** (c) — A secondary oocyte arrested in metaphase II is ovulated.
**17.** (a) — Unequal cytokinesis gives one large ovum and small polar bodies.
**18.** (b) — Menstrual-cycle dating begins with the first day of bleeding.
**19.** (b) — The mid-cycle LH surge ruptures the dominant follicle.
**20.** (c) — Corpus-luteum progesterone dominates the luteal phase.
**21.** (a) — Follicular oestrogen rebuilds the endometrium after menstruation.
**22.** (d) — hCG from trophoblast tissue enters maternal blood and urine.
**23.** (c) — Menopause is permanent loss of ovarian cyclic activity.
**24.** (b) — Meiosis makes sperm haploid with 23 chromosomes.
**25.** (d) — Placental villi provide the exchange surface without normally mixing blood.
:::

**Set B — Understanding (15 questions)**

1. The testes are held in the scrotum because spermatogenesis requires a temperature
   (a) equal to core temperature (b) below core body temperature (c) above fever temperature (d) independent of blood flow
2. Unequal division in oogenesis is advantageous because it preserves in one cell most of the
   (a) cytoplasm and stored resources (b) paternal chromosomes (c) sperm mitochondria (d) follicular fluid
3. Millions of sperm are ejaculated although only one fertilises because
   (a) every sperm must enter the ovum (b) meiosis occurs in the uterus (c) most are lost or fail during transport (d) the ovum contains millions of nuclei
4. Calling the ovulated cell a mature ovum is inaccurate because it has not yet completed
   (a) mitosis in the follicle (b) its first meiotic division (c) meiosis II (d) implantation
5. Early in the follicular phase, FSH primarily causes
   (a) menstruation (b) corpus-luteum formation (c) milk secretion (d) follicle growth and oestrogen production
6. A sustained high oestrogen level just before ovulation triggers the LH surge by
   (a) positive feedback on the pituitary/hypothalamus (b) destroying GnRH receptors (c) converting FSH into progesterone (d) blocking all gonadotropins
7. Regression of the corpus luteum initiates menstruation mainly through withdrawal of
   (a) hCG (b) testosterone (c) prolactin (d) progesterone and oestrogen
8. hCG is useful in pregnancy testing because it is produced by early trophoblast and appears in maternal
   (a) blood and urine (b) semen only (c) cerebrospinal fluid only (d) menstrual fluid only
9. Seminal fructose and mildly alkaline fluid respectively help sperm by providing
   (a) chromosomes and enzymes (b) energy substrate and protection from acidity (c) oxygen and mitochondria (d) hormones and antibodies
10. After vasectomy, masculine characters usually remain normal because the testes still
   (a) release sperm into blood (b) secrete testosterone into blood (c) store semen in the bladder (d) produce oestrogen only
11. Bilateral blockage of uterine tubes can cause infertility despite normal ovulation because
   (a) eggs become diploid (b) the uterus stops contracting (c) sperm and oocyte cannot meet normally (d) FSH cannot enter blood
12. Which pairing correctly distinguishes milk production from milk ejection?
   (a) oxytocin produces; prolactin ejects (b) ADH produces; oxytocin ejects (c) prolactin produces; insulin ejects (d) prolactin produces; oxytocin ejects
13. Maternal and fetal materials exchange in the placenta without wholesale mixing because transfer occurs across
   (a) placental barrier surfaces by diffusion/transport (b) open holes between arteries (c) the fetal digestive tract (d) the maternal spinal cord
14. FSH is typically high after menopause because falling ovarian hormones reduce
   (a) hypothalamic blood flow (b) sperm production (c) negative feedback on the pituitary (d) the number of chromosomes
15. During the secretory phase, progesterone makes the endometrium
   (a) shed immediately (b) glandular, vascular and receptive to implantation (c) convert into myometrium (d) insensitive to all hormones

::: note Answers and explanations — Set B
**1.** (b) — Scrotal positioning/thermoregulation keeps testes cooler than the abdomen.
**2.** (a) — The ovum retains cytoplasm, organelles and reserves needed before implantation.
**3.** (c) — Attrition in the female tract is enormous; numbers compensate for loss and transport barriers.
**4.** (c) — The ovulated secondary oocyte is arrested in metaphase II.
**5.** (d) — FSH recruits/grows follicles and stimulates granulosa-cell oestrogen synthesis.
**6.** (a) — Sustained high oestrogen switches from negative to positive feedback at mid-cycle.
**7.** (d) — Loss of luteal steroids destabilises and sheds the functional endometrium.
**8.** (a) — Implanting trophoblast secretes hCG that reaches blood and is excreted in urine.
**9.** (b) — Fructose fuels sperm; seminal fluid buffers the acidic vaginal environment.
**10.** (b) — Vasectomy blocks the duct path, not endocrine release from Leydig cells.
**11.** (c) — Tubal transport is necessary for fertilisation and embryo passage to the uterus.
**12.** (d) — Prolactin supports synthesis; oxytocin contracts myoepithelial cells for ejection.
**13.** (a) — Exchange occurs across fetal capillary/trophoblast surfaces bathed by maternal blood.
**14.** (c) — Low oestrogen/inhibin after menopause removes feedback restraint on FSH.
**15.** (b) — Progesterone converts the proliferated lining into a secretory, implantation-ready tissue.
:::

**Set C — Application (10 questions)**

1. A semen sample has volume 3.0 mL and concentration 80 million sperm/mL. The total sperm number is
   (a) 80 million (b) 240 million (c) 27 million (d) 800 million
2. How many spermatozoa can form from 25 primary spermatocytes, assuming all divisions succeed?
   (a) 25 (b) 50 (c) 75 (d) 100
3. Ten primary oocytes complete oogenesis after fertilisation. The maximum yield is
   (a) 40 ova and no polar bodies (b) 20 ova and 20 polar bodies (c) 10 ova and 30 polar bodies (d) 10 ova and 10 polar bodies
4. In a regular 35-day cycle with an approximately 14-day luteal phase, ovulation is expected near day
   (a) 14 (b) 21 (c) 28 (d) 35
5. If the first day of the last menstrual period is 1 January 2026, the 280-day estimated due date is
   (a) 28 September 2026 (b) 1 October 2026 (c) 15 October 2026 (d) 8 October 2026
6. A man has no sperm in semen after an operation, but testosterone and libido remain normal. The operation most likely blocked the
   (a) vas deferens (b) seminiferous tubule blood supply (c) pituitary portal vessels (d) Leydig-cell ducts
7. An embryo implants and begins growing inside a uterine tube. This is an
   (a) ectopic pregnancy (b) normal implantation (c) corpus albicans (d) menarche event
8. Blood sampled immediately before ovulation should show the pattern
   (a) low oestrogen, low LH, high progesterone (b) high oestrogen, rapidly rising LH, low progesterone (c) high progesterone and low FSH/LH (d) high hCG before implantation
9. Surgical loss of the corpus luteum very early in pregnancy, before placental steroid production is adequate, threatens pregnancy chiefly through loss of
   (a) sperm capacitation (b) fetal testosterone (c) prolactin only (d) progesterone support of endometrium
10. If about 400 follicles ovulate from a pubertal pool of 400,000, the percentage ovulated is
   (a) 1.0% (b) 0.01% (c) 0.1% (d) 10%

::: note Answers and explanations — Set C
**1.** (b) — Total sperm = $3.0\times80=240$ million.
**2.** (d) — Each primary spermatocyte yields four sperm: $25\times4=100$.
**3.** (c) — Each primary oocyte yields one ovum and up to three polar bodies.
**4.** (b) — Ovulation is approximately $35-14=21$ days after cycle day 1.
**5.** (d) — 1 January plus 280 days in non-leap year 2026 is 8 October.
**6.** (a) — A vasectomy interrupts sperm transport while testicular endocrine function continues.
**7.** (a) — Implantation outside the uterine cavity, most often tubal, is ectopic pregnancy.
**8.** (b) — The LH surge follows sustained high follicular oestrogen while progesterone has not yet risen substantially.
**9.** (d) — Early pregnancy depends on luteal progesterone before the luteoplacental shift.
**10.** (c) — $(400/400000)\times100=0.1\%$; most follicles undergo atresia.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe the male and female reproductive systems of man. <span class="marks">[10]</span>
2. Describe spermatogenesis and oogenesis and compare them. <span class="marks">[10]</span>
3. Describe the ovarian and menstrual cycles and their hormonal control. <span class="marks">[10]</span>

```photogrid label="11.H" cols="3" ratio="1.25" caption="Human reproduction. (a) The male reproductive system. (b) The female reproductive system. (c) Human sperm cells, each with an acrosome, a middle piece and a tail."
@ photo id="bio12/male-repro" cap="(a) Male system"
fit 1.25
focus 0.5 0.5
@ photo id="bio12/female-repro" cap="(b) Female system"
fit 1.25
focus 0.5 0.5
@ photo id="bio12/sperm" cap="(c) Sperm"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: Male and female reproductive systems (10 marks)

**Introduction.** Humans are **sexually reproducing, viviparous** animals with internal fertilisation.

**Male system.**

1. **Testes:** a pair in the **scrotum**, which keeps them 2–3 °C below body temperature. Seminiferous tubules make sperms and **Leydig (interstitial) cells** make testosterone; Sertoli cells nourish the sperm.
2. **Duct system:** epididymis (stores sperm) → vas deferens → ejaculatory duct → urethra inside the penis.
3. **Accessory glands:** **seminal vesicles** (fructose, 60% of semen), **prostate** (alkaline fluid) and **Cowper's glands** (lubricating mucus). Sperm and secretions form **semen** (about 3 mL, with 60–100 million sperm per mL).

**Female system.**

1. **Ovaries:** a pair in the lower abdomen that produce eggs and oestrogen and progesterone.
2. **Fallopian tubes (oviducts):** with the funnel-shaped **infundibulum** and ciliated lining; the site of **fertilisation**.
3. **Uterus (womb):** a pear-shaped muscular organ; the wall has perimetrium, **myometrium** and **endometrium** where the embryo implants.
4. **Cervix and vagina:** the cervix is the neck of the uterus; the vagina is the birth canal.
5. **External genitalia and mammary glands:** the vulva; the breasts produce milk under prolactin and oxytocin.

| Organ | Male | Female |
|---|---|---|
| Gonad | Testis | Ovary |
| Gamete | Sperm | Ovum |
| Hormones | Testosterone | Oestrogen, progesterone |
| Gamete number | Millions | One (usually) a month |
| Fertilisation site | – | Ampulla of the oviduct |

**Conclusion.** Each organ has a clear role in forming gametes, bringing them together and nourishing the embryo.

### Model answer D2: Gametogenesis (10 marks)

**Introduction.** **Gametogenesis** is the formation of haploid gametes from diploid germ cells in the gonads. It has multiplication, growth and maturation phases.

**Spermatogenesis (in the seminiferous tubules, starts at puberty).**

1. **Multiplication:** spermatogonia (2n = 46) divide by mitosis.
2. **Growth:** some grow into **primary spermatocytes** (2n).
3. **Maturation:** meiosis I gives two **secondary spermatocytes** (n = 23), and meiosis II gives four **spermatids** (n).
4. **Spermiogenesis:** spermatids change into **spermatozoa** (no division). Each has a **head** (nucleus with the **acrosome** that has enzymes), a **middle piece** (mitochondria for energy) and a **tail** for swimming.

**Oogenesis (in the ovary).**

1. **Multiplication:** in the foetus oogonia divide by mitosis.
2. **Growth:** they become **primary oocytes** that start meiosis I, but stop at prophase I until puberty. A girl is born with about 2 million primary oocytes, and only about 400 ovulate.
3. **Maturation:** at each cycle meiosis I is completed, giving a large **secondary oocyte** and a small **first polar body**. The secondary oocyte stops at metaphase II and is released at ovulation.
4. Only if a sperm enters does meiosis II finish, giving the **ovum** and a second polar body.

| Feature | Spermatogenesis | Oogenesis |
|---|---|---|
| Starts | Puberty | Foetal life (stops, resumes at puberty) |
| Time | Continues through life | Stops at menopause (about 50) |
| Product of one cell | 4 sperms | 1 ovum + 3 polar bodies |
| Size | Small, motile | Large, non-motile |
| Number | Millions | About 400 |

**Fertilisation.** A sperm releases acrosomal enzymes (hyaluronidase) to pass through the egg coat. The nuclei fuse to form a **zygote** (2n = 46).

**Conclusion.** Spermatogenesis is continuous and produces many small gametes, but oogenesis is limited and gives one large, food-rich egg.

### Model answer D3: Ovarian and menstrual cycles (10 marks)

**Introduction.** In women the cycle repeats about every **28 days** from puberty (menarche, 12–14 years) to menopause (about 45–50 years). It is controlled by the hypothalamus, pituitary and ovarian hormones.

**Phases.**

1. **Menstrual phase (days 1–5):** the endometrium breaks down and about 50–100 mL of blood and tissue is discharged because the levels of oestrogen and progesterone have dropped.
2. **Follicular (proliferative) phase (days 6–13):** **FSH** from the pituitary matures a Graafian follicle, which makes **oestrogen**. Oestrogen rebuilds the endometrium.
3. **Ovulation (day 14):** a surge of **LH** (with FSH) bursts the follicle and releases the secondary oocyte.
4. **Luteal (secretory) phase (days 15–28):** the ruptured follicle becomes the **corpus luteum**, which secretes **progesterone** (and oestrogen). The endometrium becomes thick, glandular and ready for implantation.
5. **If fertilisation does not occur,** the corpus luteum degenerates after about 10 days, hormone levels fall and menstruation begins. **If it occurs,** the embryo makes **hCG**, which keeps the corpus luteum active, and menstruation stops (pregnancy).

| Hormone | Source | Main action |
|---|---|---|
| FSH | Anterior pituitary | Follicle growth |
| LH | Anterior pituitary | Ovulation, corpus luteum |
| Oestrogen | Follicle | Builds endometrium; LH surge |
| Progesterone | Corpus luteum | Maintains endometrium |

**Numerical.** If the last period began on day 1 and the cycle is 28 days, ovulation is on day 14 and the fertile days are about days 12–16. For a 30-day cycle, ovulation is about day 16.

**Conclusion.** The two cycles run together, so the uterus is ready exactly when the egg arrives in the oviduct.

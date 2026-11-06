---
subject: Zoology
grade: CEE
unit: 10
title: Endocrine System
hours: 2
area: Human Biology and Physiology
---

The endocrine system is rated at **2 questions** in this book's estimate of
the 40-question Zoology paper. This is a matching-and-direction chapter:
gland → hormone → target → effect, then hyper- and hyposecretion. The highest
yield chains are **hypothalamus → pituitary → target gland**,
**insulin versus glucagon**, **PTH versus calcitonin**, and the contrast
between an underactive and overactive thyroid or adrenal cortex.

::: key What the paper asks from this chapter
- Endocrine glands are **ductless** and release hormones into blood; only cells with suitable receptors respond.
- The **hypothalamus** controls the anterior pituitary through releasing/inhibiting hormones in portal blood; the posterior pituitary **stores** ADH and oxytocin made in the hypothalamus.
- Anterior pituitary hormones: **GH, TSH, ACTH, FSH, LH and prolactin**.
- Thyroid hormones raise metabolic rate and need iodine; **calcitonin lowers Ca²⁺**, whereas **parathormone raises Ca²⁺**.
- Adrenal cortex: **aldosterone** for Na⁺/water and blood pressure, **cortisol** for glucose and stress; adrenal medulla: adrenaline/noradrenaline for emergency action.
- **Insulin lowers** blood glucose; **glucagon raises** it.
- Disorder anchors: gigantism/acromegaly (GH excess), cretinism/myxoedema and Graves' disease (thyroid), tetany (low PTH/calcium), Addison's/Cushing's/Conn's (adrenal cortex), diabetes mellitus (insulin lack/resistance), diabetes insipidus (ADH failure).
:::

## 10.1 Endocrine glands and their hormones

An **endocrine gland** releases its secretion directly into extracellular
fluid and blood rather than through a duct. The secretion is a **hormone**, a
chemical messenger effective at very low concentration. Although blood carries
a hormone throughout the body, only **target cells** bearing its receptor can
respond. Endocrine control is usually slower than nervous control but broader
and longer lasting, coordinating growth, metabolism, reproduction, fluid
balance and stress responses.

### Chemical classes and modes of action

| Class | Examples | Typical receptor/mechanism |
|---|---|---|
| **Peptides and proteins** | insulin, glucagon, GH, TSH, ADH, oxytocin | water-soluble; bind cell-surface receptors and use second messengers or enzyme cascades |
| **Steroids** | cortisol, aldosterone, testosterone, oestrogen, progesterone | made from cholesterol; lipid-soluble; mainly bind intracellular receptors that alter gene transcription |
| **Amino-acid derivatives** | T₃/T₄, adrenaline, noradrenaline, melatonin | catecholamines usually act at surface receptors; thyroid hormones act mainly on nuclear receptors |

Water-soluble hormones travel largely free in plasma and often have short
half-lives. Many steroid and thyroid hormones travel bound to carrier
proteins, which prolongs their action. Hormone secretion is regulated chiefly
by **negative feedback**: a rising product inhibits the glands or releasing
centres that stimulated its production. Positive feedback is uncommon in
healthy endocrinology; oxytocin during labour is the standard example.

### Hypothalamus and pituitary: the command axis

The pea-sized **pituitary gland (hypophysis)** lies in the sella turcica of the
sphenoid bone and is joined to the hypothalamus by the infundibulum. Its two
lobes differ in origin and should never be confused.

The **anterior pituitary (adenohypophysis)** is glandular tissue. Hypothalamic
releasing and inhibiting hormones reach it through the
**hypothalamo-hypophyseal portal system**. It synthesises and releases:

| Hormone | Principal target/action |
|---|---|
| **Growth hormone (GH/somatotropin)** | growth of bone and soft tissues; protein synthesis, fat mobilisation, antagonises insulin |
| **Thyroid-stimulating hormone (TSH)** | thyroid growth and T₃/T₄ secretion |
| **Adrenocorticotropic hormone (ACTH)** | adrenal cortex, especially cortisol secretion |
| **Follicle-stimulating hormone (FSH)** | ovarian follicle development; spermatogenesis through Sertoli cells |
| **Luteinising hormone (LH/ICSH)** | ovulation and corpus luteum; testosterone secretion by Leydig cells |
| **Prolactin** | development of mammary tissue and milk production |

The **posterior pituitary (neurohypophysis)** is nervous tissue. It does not
manufacture its two hormones. **Antidiuretic hormone (ADH/vasopressin)** and
**oxytocin** are synthesised in hypothalamic neuron cell bodies, transported
down axons and released from posterior-lobe terminals. ADH increases water
reabsorption in connecting tubules/collecting ducts; oxytocin contracts the
uterus in labour and causes milk ejection.

```figure caption="Negative feedback in the hypothalamus–pituitary–thyroid axis. Rising T₃/T₄ suppress both TRH and TSH, stabilising metabolic rate."
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 3.6))

def box(y, txt, fc):
    ax.add_patch(FancyBboxPatch((-1.45, y-0.34), 2.9, 0.68,
                                boxstyle='round,pad=0.06,rounding_size=0.10',
                                fc=fc, ec=MUTED, lw=0.9, zorder=3))
    ax.text(0, y, txt, fontsize=6.7, color=INK, ha='center', va='center', zorder=4)

box(2.35, 'HYPOTHALAMUS\nreleases TRH', '#e9f1fb')
box(0.95, 'ANTERIOR PITUITARY\nreleases TSH', '#f3e9fb')
box(-0.45, 'THYROID GLAND\nreleases T₃ and T₄', '#fff1d6')
box(-1.85, 'BODY CELLS\nmetabolic rate rises', '#e8f5e9')
for y0, y1 in [(2.00, 1.32), (0.60, -0.08), (-0.80, -1.48)]:
    ax.add_patch(FancyArrowPatch((0, y0), (0, y1), arrowstyle='-|>',
                                 mutation_scale=9, color=MUTED, lw=1.2, zorder=2))
    ax.text(0.16, (y0+y1)/2, 'stimulates (+)', fontsize=6.2, color=MUTED, va='center')
# feedback arrows on the left
for yt in (0.95, 2.35):
    ax.add_patch(FancyArrowPatch((-2.15, -0.45), (-2.15, yt), arrowstyle='-|>',
                                 mutation_scale=8, color=SERIES[1], lw=1.1, zorder=2))
    ax.plot([-1.50, -2.15], [-0.45, -0.45], color=SERIES[1], lw=1.1)
    ax.plot([-2.15, -1.50], [yt, yt], color=SERIES[1], lw=1.1)
ax.text(-2.48, 0.65, 'negative feedback (−)', fontsize=6.4, color=SERIES[1],
        ha='center', va='center', rotation=90)
ax.set_xlim(-3.05, 2.65); ax.set_ylim(-2.45, 2.85)
ax.axis('off')
```

The phrase “master gland” for the pituitary is convenient but incomplete: the
hypothalamus itself receives neural and blood-borne information and directs
both pituitary lobes.

### Thyroid and parathyroid glands

The **thyroid**, situated below the larynx around the upper trachea, is
traditionally described as the largest purely endocrine gland. Follicular
cells use iodide to produce **thyroxine (T₄)** and **triiodothyronine (T₃)**.
These increase basal metabolic rate, oxygen consumption and heat production
and are indispensable for fetal and childhood brain and skeletal development.
T₃ is the more potent hormone; much T₄ is converted to T₃ in target tissues.

Parafollicular **C cells** secrete **calcitonin**, which tends to lower blood
Ca²⁺ by reducing osteoclast activity and promoting calcium deposition in bone.
Four **parathyroid glands** on the posterior thyroid secrete **parathormone
(PTH)**, the dominant minute-to-minute raiser of blood Ca²⁺. PTH releases Ca²⁺
from bone, increases renal Ca²⁺ reabsorption and activates vitamin D, which
increases intestinal absorption. Thus the school-level pair is:

**PTH ↑ blood Ca²⁺; calcitonin ↓ blood Ca²⁺.**

### Adrenal glands: two glands in one

Each adrenal gland caps a kidney and contains an outer **cortex** and inner
**medulla** of different embryological origin.

| Region/zone | Hormone | Main action |
|---|---|---|
| Cortex — zona glomerulosa | **Aldosterone** (mineralocorticoid) | renal Na⁺ and water retention, K⁺/H⁺ excretion; maintains blood volume and pressure |
| Cortex — zona fasciculata | **Cortisol** (glucocorticoid) | gluconeogenesis, mobilisation of protein/fat, stress adaptation; anti-inflammatory/immunosuppressive at high levels |
| Cortex — zona reticularis | adrenal androgens | contribute to pubic/axillary hair and libido, especially in females |
| Medulla | **Adrenaline and noradrenaline** | rapid emergency response: cardiac output and blood pressure rise, bronchioles/pupils dilate, glycogenolysis increases |

The adrenal cortex is essential for life because salt, water and glucose
control fail without it. The medulla is a modified sympathetic ganglion; its
hormones reinforce sympathetic nerves but are not absolutely essential.

### Endocrine pancreas and blood-glucose control

The **islets of Langerhans** are ductless endocrine clusters scattered through
the exocrine pancreas. Their β cells secrete **insulin**, α cells secrete
**glucagon**, and δ cells secrete somatostatin.

Insulin is released when blood glucose rises. It increases glucose uptake by
muscle and adipose tissue, stimulates glycogen, fat and protein synthesis and
suppresses hepatic glucose output. Glucagon is released when glucose falls and
acts mainly on the liver to stimulate glycogenolysis and gluconeogenesis.
Adrenaline, cortisol and GH also tend to raise glucose; insulin is the only
major hormone whose dominant systemic action lowers it.

```figure caption="Schematic blood-glucose and insulin pattern after a carbohydrate-containing meal. The insulin rise follows glucose absorption and returns glucose toward the fasting range."
fig, ax = plt.subplots(figsize=(5.2, 3.1))
t = np.linspace(0, 180, 500)
glucose = 90 + 66*(t/45)**2*np.exp(2*(1-t/45))
insulin = 8 + 74*(t/58)**2*np.exp(2*(1-t/58))
ax.plot(t, glucose, color=SERIES[0], lw=2.0, label='blood glucose')
ax.set_xlabel('time after meal (min)')
ax.set_ylabel('blood glucose (mg dL⁻¹)', color=SERIES[0])
ax.set_xlim(0, 180); ax.set_ylim(65, 175)
ax.tick_params(axis='y', colors=SERIES[0])
ax2 = ax.twinx()
ax2.plot(t, insulin, color=SERIES[1], lw=2.0, label='insulin')
ax2.set_ylabel('plasma insulin (relative units)', color=SERIES[1])
ax2.set_ylim(0, 105)
ax2.tick_params(axis='y', colors=SERIES[1])
ax.axhline(90, color=GRID, lw=0.8, ls='--')
ax.text(124, 94, 'fasting level', fontsize=6.2, color=MUTED)
ax.text(38, 163, 'glucose', fontsize=6.8, color=SERIES[0], ha='center')
ax2.text(66, 89, 'insulin', fontsize=6.8, color=SERIES[1], ha='center')
ax.axvline(0, color=MUTED, lw=0.8)
ax.text(2, 169, 'meal', fontsize=6.2, color=MUTED)
ax.spines[['top']].set_visible(False)
ax2.spines[['top']].set_visible(False)
```

::: example How much glucose is in the blood?
A fasting glucose of 90 mg dL⁻¹ means 90 mg in 100 mL, or 0.9 g L⁻¹. In about
5 L of blood, this is only

$$0.9\ \text{g L}^{-1}\times5\ \text{L}=4.5\ \text{g}$$

Yet a meal may supply many tens of grams. The point of insulin is therefore
easy to see: absorbed glucose must rapidly enter tissues and storage forms,
while hepatic glucose output is switched down.
:::

### Gonads, pineal, thymus and diffuse endocrine tissues

- **Testes:** Leydig cells secrete **testosterone**, required for
  spermatogenesis and male secondary sexual characters. Sertoli cells secrete
  inhibin, which suppresses FSH.
- **Ovaries:** developing follicles secrete **oestrogens**; the corpus luteum
  secretes mainly **progesterone**, which prepares/maintains the endometrium.
- **Pineal gland:** secretes **melatonin** mainly at night, helping organise
  circadian rhythms.
- **Thymus:** thymosins support T-lymphocyte maturation; the gland is most
  prominent in childhood.
- **Kidney:** erythropoietin stimulates red-cell production and calcitriol is
  the active form of vitamin D. The heart releases ANP, adipose tissue releases
  leptin, the placenta releases hCG, and the gut releases gastrin, secretin,
  cholecystokinin and motilin.


```figure caption="The thyroid axis as a closed loop with its brake. Hypothalamus releases TRH, pituitary answers with TSH, thyroid secretes T3 and T4, and the body's cells run their metabolism faster — while the rising T3/T4 feed back and quiet the two glands above, holding the whole axis steady."
cycle(["hypothalamus\nTRH", "pituitary\nTSH", "thyroid\nT3, T4", "body cells\nmetabolism"],
      centre="negative\nfeedback", figsize=(4.4, 3.4))
```

::: caution
Two ownership traps the paper sets every few years: **ADH and oxytocin are
made in the hypothalamus and merely released by the posterior pituitary** —
an option saying the posterior lobe synthesises them is wrong. And
**calcitonin (thyroid) lowers blood calcium while PTH (parathyroid) raises
it** — swapped in half of all wrong options.
:::
## 10.2 Hormonal disorders

An endocrine disorder may result from hormone **deficiency**, **excess**, or
target-cell **resistance**. In an axis, the relationship between a pituitary
tropic hormone and target-gland hormone locates the fault. For example, low
T₄ with high TSH points to primary thyroid failure: the pituitary is correctly
“shouting louder”. Low T₄ with low or inappropriately normal TSH points to a
pituitary/hypothalamic fault.

### Pituitary and posterior-lobe disorders

| Disorder | Hormonal fault | Diagnostic pattern |
|---|---|---|
| **Pituitary dwarfism** | GH deficiency in childhood | short, normally proportioned growth; intelligence usually normal |
| **Gigantism** | GH excess before epiphyseal plates close | generalised excessive linear growth |
| **Acromegaly** | GH excess after epiphyseal closure | enlarged jaw, hands, feet and soft tissues; little increase in height |
| **Diabetes insipidus** | too little ADH or renal response to ADH | very large volumes of dilute urine, intense thirst, blood glucose normal |
| **Hypopituitarism** | loss of several anterior pituitary hormones | combined thyroid, adrenal and gonadal underactivity |

### Thyroid and parathyroid disorders

**Hypothyroidism** means insufficient thyroid hormone action. In infancy and
early childhood, untreated deficiency causes **cretinism**: severely impaired
growth and brain development. In adults, **myxoedema** presents with fatigue,
cold intolerance, weight gain, dry skin, puffy face, constipation and slow
pulse. Iodine deficiency reduces T₄ synthesis; persistent TSH stimulation then
enlarges the gland as **simple/endemic goitre**.

**Hyperthyroidism** increases metabolic rate. **Graves' disease**, an
autoimmune stimulation of the TSH receptor, causes weight loss despite
appetite, heat intolerance, tremor, rapid pulse, anxiety and often exophthalmos
(protruding eyes). The presence of a goitre alone does not distinguish under-
from overactivity.

Low PTH or severe hypocalcaemia increases neuromuscular excitability and can
cause **tetany**—painful sustained muscle spasms, including laryngeal spasm.
Excess PTH produces hypercalcaemia, bone resorption and pain, kidney stones,
excess urination and abdominal/neuropsychiatric symptoms. The traditional
memory is “stones, bones, groans and moans”.

### Adrenal disorders

| Disorder | Fault | Key features |
|---|---|---|
| **Addison's disease** | adrenal cortex insufficiency (low cortisol and aldosterone) | weakness, weight loss, low blood pressure, low Na⁺, high K⁺, increased skin pigmentation in primary disease |
| **Cushing's syndrome** | cortisol excess | moon face, central obesity, thin limbs/skin, hypertension, hyperglycaemia, muscle wasting |
| **Conn's syndrome** | aldosterone excess | Na⁺/water retention, hypertension, K⁺ loss and muscle weakness |
| **Phaeochromocytoma** | adrenal-medulla tumour secreting catecholamines | episodic severe hypertension, palpitations, headache and sweating |

An adrenal crisis in untreated cortical insufficiency is dangerous because
aldosterone deficiency collapses extracellular-fluid volume while cortisol
deficiency impairs the response to stress.

### Diabetes mellitus and hypoglycaemia

**Diabetes mellitus** is chronic hyperglycaemia from deficient insulin
secretion, deficient insulin action, or both. It must not be confused with
diabetes insipidus.

| Feature | Type 1 diabetes | Type 2 diabetes |
|---|---|---|
| Main mechanism | autoimmune destruction of β cells | insulin resistance with progressive β-cell dysfunction |
| Usual onset | childhood/young adult, often abrupt | adult, gradual; increasingly seen in younger people with obesity |
| Endogenous insulin | very low or absent | present early but insufficient for demand |
| Ketosis tendency | high without insulin | less likely except under severe stress/illness |
| Essential treatment principle | insulin replacement | lifestyle measures and glucose-lowering medicines; insulin may later be needed |

When blood glucose exceeds the renal threshold, glucose appears in urine and
osmotically increases urine volume. The classical symptoms are **polyuria,
polydipsia and polyphagia**, with weight loss in marked insulin deficiency.
Long-term hyperglycaemia injures retinal, renal, nerve and cardiovascular
tissues. Modern laboratory diagnosis uses standardised fasting plasma glucose,
oral glucose tolerance or HbA1c criteria; a single casual number out of context
is not a complete diagnosis.

Conversely, too much insulin or too little food after insulin can produce
**hypoglycaemia**: sweating, tremor, palpitations, hunger, confusion and, if
severe, seizures or coma. The brain's heavy dependence on a continuous glucose
supply makes this an emergency.

::: caution Mellitus vs insipidus
Both can produce excess urine and thirst. In **mellitus**, urine is
glucose-rich because blood glucose is high. In **insipidus**, urine is very
dilute and glucose is normal because ADH signalling fails. The shared word
“diabetes” refers to passing large volumes, not to the same hormone.
:::



```figure caption="The glucose see-saw as a cycle: rising glucose summons insulin from the beta cells, cells and liver take the glucose in and the level falls; falling glucose summons glucagon from the alpha cells, the liver pours glucose back, and the level rises again. The middle band, 80-110 mg/dL, is what the two hormones defend."
cycle(["glucose\nrises", "beta cells:\ninsulin", "cells and liver\ntake glucose in",
       "glucose\nfalls", "alpha cells:\nglucagon", "liver pours\nglucose out"],
      centre="blood glucose\n80–110 mg/dL", figsize=(5.0, 3.9))
```

::: example Glucose units, exactly as the lab reports them
**Problem.** A fasting plasma glucose reads 7.0 mmol/L. Convert to mg/dL
and classify. A second patient reads 99 mg/dL; convert to mmol/L.
**Solution.** mg/dL = mmol/L × 18: 7.0 × 18 = **126 mg/dL** — the diabetic
fasting threshold, so the first patient is diabetic. 99 ÷ 18 =
**5.5 mmol/L** — comfortably normal (the ×18 factor is glucose's molecular
weight, 180 g/mol, divided by 10).
:::

::: memory
**Grow: GH. Heat: thyroid. Stress: cortisol and adrenaline. Salt:
aldosterone. Sugar: insulin and glucagon. Water: ADH. Calcium: PTH up,
calcitonin down. Clock: melatonin. Soldiers: thymosin.** Nine hooks hang the
whole table.
:::

::: tip
Sort the three 'diabetes' names once and for all: **mellitus type 1 = no
insulin**, **type 2 = insulin ignored**, **insipidus = no ADH** (urine
dilute and sweet-free). And sort the growth trio by age: **child lack =
dwarf, child excess = giant, adult excess = acromegaly**.
:::

::: example Diagnosing primary vs secondary hypothyroidism from TSH and T₄
**Problem.** Patient X has low serum free $\text{T}_4$, elevated serum $\text{TSH}$, and a diffuse goitre; Patient Y has low free $\text{T}_4$ and low $\text{TSH}$ without goitre. Localise the lesion in each patient.

**Solution.** In **Patient X (primary thyroid failure / endemic iodine-deficiency goitre)**, low $\text{T}_4$ removes negative feedback on the anterior pituitary, driving high $\text{TSH}$ which hypertrophies the gland into a goitre. In **Patient Y (secondary / pituitary hypothyroidism)**, the anterior pituitary itself fails to secrete $\text{TSH}$.
:::

```photogrid label="10.1" cols="2" ratio="1.2" caption="Iodine, the thyroid and salt. (a) The endocrine glands of the head and trunk, including the thyroid in the neck that makes thyroxine from iodine. (b) An adult needs about 150 micrograms of iodine a day. Salt carrying 30 mg of iodine per kg gives 60 micrograms in 2 g, 150 in 5 g and 300 in 10 g of salt, so 100 per cent of the need is met by 5 g, the amount usually eaten. A shortage enlarges the thyroid (simple goitre) and in a pregnant woman damages the baby's brain (cretinism), which is why Nepal promotes iodised salt in the hills where soil iodine is low."
@ photo id="bio12/endocrine-glands" cap="Endocrine glands of the human body"
fit 1.2
focus 0.5 0.5
@ svg cap="Iodine from salt against the daily need of 150 micrograms"
conc = 30.0
need = 150.0
got = {g: conc * g / 1000 * 1000 for g in (2, 5, 10)}
assert got[2] == 60 and got[5] == 150 and got[10] == 300
facts = dict(a2="%.0f" % got[2], a5="%.0f" % got[5], a10="%.0f" % got[10], a5pc="%.0f" % (got[5] / need * 100))
f = Fig(300, 236)
f.text(150, 12, "Iodine (micrograms) in 30 mg/kg salt", size=10.5, color=NAVY, bold=True)
for i, g in enumerate((2, 5, 10)):
    y = 34 + i * 46
    f.text(10, y, "%d g of salt" % g, size=10.5, color=SLATE, anchor="start")
    w = got[g] / 300 * 200
    c, fl = (AMBER, SAND) if got[g] < need else (TEAL, MINT)
    f.box(10, y + 8, w, 22, fill=fl, stroke=c, r=2)
    f.text(10 + w + 6, y + 19, "%.0f ug = %.0f%%" % (got[g], got[g] / need * 100), size=10.5, color=c, bold=True, anchor="start", vmid=True)
f.line(10 + 100, 28, 10 + 100, 176, color=RED, dash=True)
f.text(112, 186, "need 150", size=10.5, color=RED, bold=True, anchor="start")
f.text(150, 214, "5 g of iodised salt meets the daily need", size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

- Anterior pituitary: **GH, TSH, ACTH, FSH, LH, prolactin**.
- Posterior pituitary stores hypothalamic **ADH** and **oxytocin**.
- Thyroid: T₃/T₄ ↑ BMR; C-cell calcitonin ↓ blood Ca²⁺.
- Parathyroid: PTH ↑ blood Ca²⁺ from bone, kidney and activated vitamin D/gut.
- Adrenal cortex: aldosterone = salt/water; cortisol = glucose/stress.
- Adrenal medulla: adrenaline/noradrenaline = emergency sympathetic hormone.
- Pancreatic β cells → insulin ↓ glucose; α cells → glucagon ↑ glucose.
- Leydig cells → testosterone; corpus luteum → progesterone; pineal → melatonin.
- Low target hormone + high pituitary tropic hormone = primary target-gland failure.
- GH excess: childhood = gigantism; adult = acromegaly.
- Low thyroid hormone: child = cretinism; adult = myxoedema. Excess = Graves' pattern.
- Addison's = low cortical hormones; Cushing's = cortisol excess; Conn's = aldosterone excess.

### Rapid-revision tables and high-yield facts

| Quantity | Value |
|---|---|
| Blood glucose normal / diabetic fasting | 80–110 mg/dL / ≥ 126 mg/dL (≥ 7.0 mmol/L) |
| mg/dL → mmol/L | divide by 18 (glucose 180 g/mol) |
| HbA1c window / diagnostic | ~3 months (RBC lifespan) / ≥ 6.5 % |
| Anterior pituitary | GH, TSH, ACTH, FSH, LH, prolactin |
| Posterior pituitary | ADH, oxytocin (made in hypothalamus) |
| Ca²⁺ control | PTH raises, calcitonin lowers |
| Adrenal | cortex: aldosterone, cortisol; medulla: adrenaline |
| Islets | β insulin (lowers glucose), α glucagon (raises) |

## Chapter summary

- Hormones are blood-borne messengers whose effects depend on receptors,
  chemical class, transport and feedback regulation.
- The hypothalamus controls the anterior pituitary through portal blood and
  supplies the posterior pituitary with ADH and oxytocin.
- Pituitary tropic hormones organise thyroid, adrenal-cortical and gonadal
  activity; GH and prolactin act more directly on non-endocrine tissues.
- Thyroid hormones set metabolic rate and are essential to development;
  PTH and calcitonin act in opposite directions on blood calcium.
- The adrenal cortex preserves salt, water and glucose during stress, whereas
  the medulla supplies a rapid catecholamine emergency response.
- Insulin and glucagon form an antagonistic pair around blood glucose.
- Endocrine diagnosis rests on direction and feedback: identify what is high,
  what is low and whether the controller is responding appropriately.
- The major named disorders follow mechanically from hormone function, so
  symptoms can be derived rather than memorised in isolation.

## Practice questions

**Set A — Recall (25 questions)**

1. Endocrine glands release their secretions directly into the
   (a) intestinal lumen (b) ducts (c) blood (d) skin surface
2. The gland traditionally called the master gland is the
   (a) pituitary gland (b) thyroid gland (c) adrenal gland (d) pineal gland
3. ADH and oxytocin are synthesised in the
   (a) anterior pituitary (b) hypothalamus (c) posterior pituitary (d) pineal gland
4. Growth hormone is secreted by the
   (a) thyroid (b) adrenal cortex (c) pancreatic islets (d) anterior pituitary
5. Milk production by mammary glands is stimulated mainly by
   (a) oxytocin (b) ADH (c) oestrogen (d) prolactin
6. The hormone that increases water reabsorption in collecting ducts is
   (a) ADH (b) aldosterone (c) calcitonin (d) glucagon
7. Uterine contraction during labour and milk ejection are promoted by
   (a) oxytocin (b) prolactin (c) progesterone (d) LH
8. Iodine is essential for synthesis of
   (a) insulin (b) thyroxine (c) adrenaline (d) cortisol
9. Blood calcium is lowered by
   (a) parathormone (b) calcitonin (c) ADH (d) aldosterone
10. Parathormone is secreted by the
   (a) thyroid follicles (b) adrenal medulla (c) parathyroid glands (d) pancreatic acini
11. Aldosterone is produced mainly by the
   (a) adrenal medulla (b) zona reticularis (c) zona glomerulosa (d) anterior pituitary
12. The principal glucocorticoid of humans is
   (a) aldosterone (b) adrenaline (c) testosterone (d) cortisol
13. Adrenaline is secreted by the
   (a) adrenal cortex (b) adrenal medulla (c) thyroid gland (d) pituitary gland
14. Insulin is secreted by which islet cells?
   (a) α cells (b) δ cells (c) β cells (d) acinar cells
15. Glucagon increases blood glucose mainly by acting on the
   (a) kidney (b) skin (c) thyroid (d) liver
16. Testosterone is produced in the testis by
   (a) Leydig cells (b) Sertoli cells (c) spermatogonia (d) seminiferous fluid
17. Progesterone is secreted in large amount by the
   (a) Graafian follicle before ovulation (b) corpus luteum (c) pituitary gland (d) placenta only
18. Melatonin is secreted by the
   (a) thymus (b) thyroid (c) adrenal cortex (d) pineal gland
19. Maturation of T lymphocytes is promoted by hormones of the
   (a) thymus (b) pineal gland (c) parathyroid (d) adrenal medulla
20. Erythropoietin, which stimulates red-cell production, comes mainly from the
   (a) kidney (b) spleen (c) thyroid (d) pituitary
21. The largest purely endocrine gland in the human body is traditionally the
   (a) pituitary (b) adrenal (c) thyroid (d) thymus
22. Steroid hormones are chemically derived from
   (a) glucose (b) amino acids (c) nucleotides (d) cholesterol
23. A water-soluble peptide hormone usually binds first to a receptor on the
   (a) nuclear membrane (b) ribosome (c) cell surface (d) chromosome
24. Secretin, a gastrointestinal hormone, chiefly stimulates pancreatic secretion rich in
   (a) hydrochloric acid (b) bicarbonate (c) bile salts (d) insulin
25. FSH in females primarily promotes
   (a) ovarian follicle development (b) milk ejection (c) uterine contraction (d) thyroid secretion

::: note Answers and explanations — Set A
**1.** (c) — Endocrine glands are ductless and deliver hormones to blood.
**2.** (a) — The pituitary controls several other endocrine glands, although the hypothalamus controls it.
**3.** (b) — Hypothalamic neurons make ADH and oxytocin; the posterior pituitary stores/releases them.
**4.** (d) — Somatotroph cells of the anterior pituitary secrete growth hormone.
**5.** (d) — Prolactin stimulates milk production; oxytocin causes milk ejection.
**6.** (a) — ADH inserts water channels and increases collecting-duct water reabsorption.
**7.** (a) — Oxytocin contracts uterine and mammary myoepithelial smooth muscle.
**8.** (b) — Thyroxine/T₄ contains four iodine atoms and requires dietary iodide.
**9.** (b) — Calcitonin from thyroid C cells lowers blood calcium.
**10.** (c) — The four parathyroid glands secrete PTH.
**11.** (c) — Aldosterone is the mineralocorticoid of the zona glomerulosa.
**12.** (d) — Cortisol is the main human glucocorticoid.
**13.** (b) — Chromaffin cells of the adrenal medulla secrete adrenaline and noradrenaline.
**14.** (c) — Pancreatic β cells secrete insulin.
**15.** (d) — Glucagon stimulates hepatic glycogenolysis and gluconeogenesis.
**16.** (a) — Interstitial Leydig cells produce testosterone under LH stimulation.
**17.** (b) — After ovulation, the corpus luteum is the main progesterone source.
**18.** (d) — The pineal gland secretes melatonin with a night-time peak.
**19.** (a) — Thymic hormones support T-cell development.
**20.** (a) — The kidney senses oxygen delivery and releases erythropoietin.
**21.** (c) — The thyroid is the largest gland devoted solely to endocrine secretion.
**22.** (d) — All steroid hormones are synthesised from cholesterol.
**23.** (c) — Peptide hormones generally cannot cross the lipid membrane and use surface receptors.
**24.** (b) — Secretin stimulates watery bicarbonate-rich pancreatic secretion to neutralise acid chyme.
**25.** (a) — FSH supports growth and maturation of ovarian follicles.
:::

**Set B — Understanding (15 questions)**

1. A hormone carried to nearly every tissue affects only some cells because only those cells possess
   (a) specific receptors for it (b) a nucleus (c) direct nerve supply (d) endocrine ducts
2. In the thyroid axis, a sustained rise in T₄ normally causes
   (a) reduced TRH and TSH secretion (b) increased TRH and TSH secretion (c) destruction of pituitary cells (d) conversion of TSH to T₃
3. The posterior pituitary differs from the anterior pituitary because it mainly
   (a) makes six tropic hormones (b) is controlled by portal blood (c) develops from mouth roof (d) stores hypothalamic hormones
4. Steroid hormones can influence gene transcription directly because they are
   (a) stored in synaptic vesicles (b) rapidly destroyed by enzymes (c) carried only by nerves (d) lipid-soluble and enter target cells
5. During fasting, maintenance of blood glucose depends especially on
   (a) increased insulin and glycogenesis (b) calcitonin release from thyroid (c) glucagon-stimulated hepatic glucose output (d) ADH-stimulated glucose reabsorption
6. Aldosterone raises arterial pressure mainly by increasing renal retention of
   (a) sodium and water (b) potassium and hydrogen ions (c) glucose and amino acids (d) calcium and phosphate
7. Which statement correctly contrasts PTH and calcitonin?
   (a) Both raise blood calcium (b) PTH raises and calcitonin lowers blood calcium (c) Both lower blood calcium (d) PTH lowers and calcitonin raises blood calcium
8. GH excess produces gigantism in a child but acromegaly in an adult because adults have
   (a) no pituitary receptors (b) stopped secreting TSH (c) closed epiphyseal growth plates (d) no long bones remaining
9. Iodine deficiency can enlarge the thyroid because low T₄ removes feedback inhibition of
   (a) insulin (b) calcitonin (c) TSH (d) prolactin
10. Adrenal medullary hormones reinforce sympathetic nerves but their effects last longer because they
   (a) are stored permanently in bone (b) travel only inside axons (c) block all receptors (d) circulate throughout the blood
11. On a hot day with little water intake, increased ADH produces urine that is
   (a) large in volume and dilute (b) small in volume and concentrated (c) rich in glucose (d) alkaline and protein-rich
12. Cortisol helps maintain glucose during prolonged stress chiefly by promoting
   (a) glycogen storage only (b) insulin secretion (c) urinary glucose loss (d) gluconeogenesis in the liver
13. Insulin is given by injection rather than as an ordinary swallowed protein because it would be
   (a) converted to glucagon in blood (b) digested by gastrointestinal proteases (c) stored in thyroid colloid (d) unable to enter any cell
14. Calling the pituitary the master gland is incomplete because its anterior lobe is directed by
   (a) the spinal cord (b) adrenal medulla (c) hypothalamic releasing hormones (d) pancreatic enzymes
15. Accidental removal of parathyroid tissue may cause tetany because low blood calcium increases
   (a) neuromuscular excitability (b) insulin resistance (c) red-cell production (d) thyroid hormone storage

::: note Answers and explanations — Set B
**1.** (a) — Hormonal specificity is determined by receptor distribution.
**2.** (a) — T₃/T₄ exert negative feedback on hypothalamic TRH and pituitary TSH.
**3.** (d) — The posterior lobe is a release site for hormones synthesised in hypothalamic neurons.
**4.** (d) — Lipid-soluble steroids cross membranes and bind intracellular receptors.
**5.** (c) — Glucagon mobilises hepatic glycogen and supports gluconeogenesis during fasting.
**6.** (a) — Sodium retention osmotically retains water, expanding extracellular-fluid volume.
**7.** (b) — PTH and calcitonin have opposite school-level effects on plasma calcium.
**8.** (c) — After growth-plate fusion, long bones cannot lengthen, so mainly acral/soft tissues enlarge.
**9.** (c) — Low T₄ leaves TSH high, chronically stimulating thyroid growth.
**10.** (d) — Blood-borne catecholamines reach widespread targets and are cleared more slowly than synaptic signals.
**11.** (b) — ADH-mediated water reabsorption lowers urine volume and raises concentration.
**12.** (d) — Cortisol mobilises substrates and stimulates hepatic glucose production.
**13.** (b) — Insulin is a protein and would be hydrolysed in the gastrointestinal tract.
**14.** (c) — Hypothalamic factors delivered by portal blood regulate anterior-pituitary secretion.
**15.** (a) — Hypocalcaemia makes excitable membranes unstable, causing spasms.
:::

**Set C — Application (10 questions)**

1. Laboratory tests show low free T₄ together with markedly high TSH. The primary fault is most likely in the
   (a) hypothalamus (b) anterior pituitary (c) adrenal cortex (d) thyroid gland
2. At a blood glucose concentration of 126 mg dL⁻¹, the mass of glucose in 5.0 L of blood is about
   (a) 0.63 g (b) 1.26 g (c) 6.3 g (d) 63 g
3. An adult develops an enlarging jaw, hands and feet without increased height. The likely disorder is
   (a) gigantism (b) cretinism (c) myxoedema (d) acromegaly
4. A patient passes 15 L/day of very dilute urine but has normal blood glucose. The deficient signal is most likely
   (a) ADH action (b) insulin action (c) glucagon action (d) aldosterone action
5. Low blood pressure, low Na⁺, high K⁺, weakness and skin pigmentation suggest
   (a) Cushing's syndrome (b) Addison's disease (c) Graves' disease (d) Conn's syndrome
6. Moon face, central obesity, hypertension and hyperglycaemia are most consistent with excess
   (a) calcitonin (b) cortisol (c) insulin (d) melatonin
7. A diabetic student who injected insulin but missed lunch becomes sweaty, tremulous and confused from
   (a) hyperglycaemia (b) hypercalcaemia (c) hypothyroidism (d) hypoglycaemia
8. Recurrent kidney stones, bone pain and high blood calcium most strongly suggest excess
   (a) parathormone (b) calcitonin (c) oxytocin (d) thymosin
9. Persistent hypertension with sodium retention and low blood potassium suggests excess
   (a) ADH (b) glucagon (c) aldosterone (d) prolactin
10. A newborn with untreated severe thyroid-hormone deficiency is at greatest risk of
   (a) impaired brain and skeletal development (b) excessive linear growth (c) diabetes insipidus (d) adrenal crisis

::: note Answers and explanations — Set C
**1.** (d) — High TSH shows the pituitary responding appropriately to a failing thyroid: primary hypothyroidism.
**2.** (c) — 126 mg dL⁻¹ = 1.26 g L⁻¹; in 5.0 L the mass is $1.26\times5.0=6.3$ g.
**3.** (d) — Adult GH excess after epiphyseal closure causes acromegaly.
**4.** (a) — Failure of ADH secretion or renal response produces diabetes insipidus.
**5.** (b) — Combined cortisol/aldosterone deficiency causes Addison's disease; pigmentation reflects high ACTH in primary disease.
**6.** (b) — Chronic cortisol excess causes Cushing's syndrome.
**7.** (d) — Insulin without sufficient carbohydrate lowers glucose below the brain's safe supply.
**8.** (a) — Excess PTH raises calcium, resorbs bone and promotes urinary stone formation.
**9.** (c) — Aldosterone excess expands Na⁺/water volume while wasting K⁺.
**10.** (a) — Thyroid hormone is critical for early brain maturation and skeletal growth; untreated deficiency causes cretinism.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe the endocrine glands of man, their hormones and functions. <span class="marks">[10]</span>
2. Describe the common disorders caused by hormone imbalance and the feedback control of hormones. <span class="marks">[10]</span>

```photogrid label="10.H" cols="2" ratio="1.5" caption="The endocrine system. (a) The position of the endocrine glands in the human body. (b) The pituitary and hypothalamus on a sagittal section of the brain, the control centre of the system."
@ photo id="bio12/endocrine-glands" cap="(a) Endocrine glands"
fit 1.5
focus 0.5 0.5
@ photo id="bio12/brain-sagittal" cap="(b) Hypothalamus and pituitary"
fit 1.5
focus 0.5 0.5
```

### Model answer D1: Endocrine glands and hormones (10 marks)

**Introduction.** **Endocrine glands** are ductless glands that release **hormones** directly into the blood. A hormone is a chemical messenger that affects a target organ in very small amounts.

| Gland | Hormone | Main function |
|---|---|---|
| **Hypothalamus** | Releasing and inhibiting hormones | Controls the pituitary |
| **Anterior pituitary** (master gland) | GH, TSH, ACTH, FSH, LH, prolactin | Growth, controls other glands, milk |
| **Posterior pituitary** | ADH, oxytocin | Water balance; labour and milk ejection |
| **Thyroid** | Thyroxine (T₃, T₄), calcitonin | Metabolic rate; lowers blood calcium |
| **Parathyroid** | Parathormone | Raises blood calcium |
| **Adrenal cortex** | Cortisol, aldosterone | Stress, glucose; salt balance |
| **Adrenal medulla** | Adrenaline, noradrenaline | Emergency ("fight or flight") |
| **Pancreas** (islets of Langerhans) | Insulin (β cells), glucagon (α cells) | Lowers and raises blood glucose |
| **Testis** | Testosterone | Male characters, sperm |
| **Ovary** | Oestrogen, progesterone | Female characters, cycle, pregnancy |
| **Pineal** | Melatonin | Sleep and body clock |
| **Thymus** | Thymosin | T-cell development |

**Points to explain.**

1. The **pituitary** is the size of a pea, lies under the hypothalamus and controls many glands, yet the hypothalamus controls it.
2. **Thyroxine** needs iodine; **iodised salt** is used in Nepal to prevent goitre.
3. **Insulin and glucagon** work against each other to keep fasting blood glucose at about 70–100 mg/dL.
4. **Adrenaline** raises heart rate, blood glucose and blood flow to muscles.
5. **Calcitonin and parathormone** keep blood calcium steady.
6. **Oxytocin** causes uterine contractions and milk release.

**Conclusion.** Hormones work together as a slow but long-lasting control system that adjusts growth, metabolism and reproduction.

### Model answer D2: Hormonal disorders and feedback control (10 marks)

**Introduction.** Too much (hyper-) or too little (hypo-) secretion of a hormone causes disease.

| Gland | Hormone problem | Disorder and symptoms |
|---|---|---|
| Pituitary | Less GH in childhood | **Dwarfism**: small body, normal mind |
| Pituitary | More GH in childhood | **Gigantism** |
| Pituitary | More GH in adults | **Acromegaly**: large jaw, hands, feet |
| Pituitary (post.) | Less ADH | **Diabetes insipidus**: large volumes of dilute urine |
| Thyroid | Lack of iodine | **Simple goitre**: neck swelling |
| Thyroid | Hypothyroid, infant | **Cretinism**: stunted body and mind |
| Thyroid | Hypothyroid, adult | **Myxoedema**: slow, weight gain |
| Thyroid | Hyperthyroid | **Graves' disease**: weight loss, protruding eyes |
| Parathyroid | Less parathormone | **Tetany**: muscle spasm |
| Adrenal cortex | Less cortisol | **Addison's disease**: weakness, low BP |
| Adrenal cortex | More cortisol | **Cushing's syndrome**: moon face, high BP |
| Pancreas | Less insulin | **Diabetes mellitus**: high blood glucose |

**Diabetes mellitus.** In **type 1** the β-cells are destroyed and insulin must be injected. In **type 2** the cells respond poorly to insulin; diet, exercise and tablets help. Signs: thirst, frequent urination, weight loss. A fasting glucose above 126 mg/dL indicates diabetes.

**Feedback control.** Most hormones work by **negative feedback**. For example: low thyroxine → the hypothalamus releases TRH → the pituitary releases TSH → the thyroid releases more thyroxine → a high level of thyroxine inhibits TRH and TSH. Similarly, a rise in blood glucose triggers insulin, which lowers glucose, which stops the insulin release. In **positive feedback** the effect strengthens the cause, as when oxytocin increases contractions during childbirth.

**Prevention in Nepal.** Iodised salt, regular checks of blood sugar and screening of newborns for hypothyroidism.

**Conclusion.** Hormone levels are held within narrow limits by feedback, and a failure of this control produces the disorders listed above.

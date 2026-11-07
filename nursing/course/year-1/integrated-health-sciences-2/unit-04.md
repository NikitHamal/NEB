---
subject: Integrated Health Sciences II
grade: BSc Nursing Year 1
unit: 4
title: Reproductive System, Menstrual Cycle and Early Pregnancy
hours: 30
area: BSN 2-3 · Integrated Health Sciences II · Unit 4
---

Every Nepali nurse counsels on menstruation, family planning and pregnancy, and the dates and hormones in this unit are the base of the later Midwifery books. We cover the male and female organs with real histology, the hypothalamic-pituitary-ovarian axis and the menstrual cycle, calculation of the expected date of delivery and gestational age, fertilisation to placenta, and the main family planning methods offered free through the MoHP, with the Safe Motherhood (Aama) programme in view.

::: key What this unit gives you
- A real ovary micrograph with a hormone-curve schematic, and a real testis micrograph with a sperm pathway diagram.
- The menstrual cycle in days, the ovulation date for 28- and 32-day cycles and the fertile window.
- Naegele's rule, the 280-day count, gestational age and fundal height, Ganzoni iron deficit and the Pearl Index, all worked step by step.
- The path from fertilisation to implantation as a timeline.
- Eight points of family planning counselling and model answers with a care plan for anaemia in pregnancy.
:::

## 4.1 Male reproductive system

The two **testes** hang in the scrotum, 2-3 °C below body temperature, which is needed for sperm production. Each testis holds about 250 lobules packed with **seminiferous tubules**, where **spermatogenesis** takes about 74 days: spermatogonia divide, become spermatocytes, spermatids and finally sperm with a head (nucleus and acrosome), midpiece (mitochondria) and tail. **Sertoli cells** nourish them and **Leydig cells** between the tubules make **testosterone** under LH. Sperm mature in the epididymis, pass through the vas deferens, and are mixed with fluid from the seminal vesicles, prostate and bulbourethral glands to form semen (normal count about 16 million per mL or more, WHO 2021). Undescended testis (cryptorchidism) needs surgery before 2 years, and a **vasectomy**, one of the permanent methods offered in Nepal, cuts the vas.

```photogrid label="4.1" cols="2" ratio="1.1" caption="The testis. (a) A real micrograph of a seminiferous tubule (H and E): cells in the wall at different stages of sperm development, with the lumen to the side. (b) The pathway of sperm from testis to urethra and the glands that add fluid."
@ photo id="nur2/seminif" cap="Seminiferous tubule, H and E"
fit 1.1
focus 0.5 0.5
mark 0.30 0.62 "1"
mark 0.68 0.25 "2"
key 1 (a) Layers of spermatogenic cells with dark round nuclei, the youngest at the outer edge
key 2 (a) Lumen of the tubule where finished sperm are released
@ svg cap="Sperm pathway"
f = Fig(380, 320)
st = [("Seminiferous tubules\nsperm made (74 days)", BLUE, NAVY), ("Epididymis\nsperm mature, stored", MINT, TEAL), ("Vas deferens\n(cut in vasectomy)", SAND, AMBER), ("Ejaculatory duct:\nseminal vesicle +\nprostate fluid", MINT, TEAL), ("Urethra: semen\nleaves the body", ROSE, RED)]
for i, (t_, fc, sc) in enumerate(st):
    y = 6 + i * 62; f.box(60, y, 260, 48, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    if i < 4: f.arrow([(190, y + 48), (190, y + 62)], color=SLATE, sw=2)
```

## 4.2 Female reproductive system

The **ovaries** (each about 3 cm) hold follicles and make oestrogen and progesterone. At birth there are about 1-2 million primordial follicles and about 400 will ovulate in a lifetime. The **fallopian tubes** (10 cm) catch the ovum, and fertilisation takes place in the **ampulla**. The **uterus** has three layers, **perimetrium**, **myometrium** and **endometrium**, and its cervix opens into the vagina; the **ectopic pregnancy** (most often in the tube) is a surgical emergency. The breast is a gland of 15-20 lobes that make milk under prolactin and release it under oxytocin.

```photogrid label="4.2" cols="2" ratio="1.15" caption="The ovary and the menstrual cycle. (a) A real section of an ovary (low power): follicles lie in the cortex around the central medulla. (b) Hormone curves across a 28-day cycle: FSH grows a follicle, the LH surge at day 14 triggers ovulation, progesterone prepares the endometrium."
@ photo id="nur2/ovary" cap="Ovary, low-power section"
fit 1.15
focus 0.5 0.5
mark 0.50 0.55 "1"
mark 0.28 0.80 "2"
key 1 (a) Central medulla: vessels and connective tissue
key 2 (a) Outer cortex: follicles at different stages of growth
@ svg cap="Cycle hormones"
import math
f = Fig(420, 330)
f.line(40, 20, 40, 230, color=SLATE, sw=1.6); f.line(40, 230, 400, 230, color=SLATE, sw=1.6)
for d in (1, 7, 14, 21, 28): f.line(40 + d * 12.5, 228, 40 + d * 12.5, 234, color=SLATE, sw=1.4); f.text(40 + d * 12.5, 246, str(d), size=10, color=SLATE)
g = lambda d, c, w: math.exp(-((d - c) / w) ** 2)
def curve(fn, col):
    pts = [(40 + d * 12.5, 225 - 190 * fn(d)) for d in [i * 0.5 for i in range(2, 57)]]
    for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=col, sw=2.6)
curve(lambda d: 0.25 + 0.15 * g(d, 5, 5) + 0.3 * g(d, 14, 1.5), AMBER)
curve(lambda d: 0.12 + 0.55 * g(d, 13, 3) + 0.3 * g(d, 21, 3.5), TEAL)
curve(lambda d: 0.04 + 0.7 * g(d, 22, 4.5), RED)
f.text(60, 12, "FSH/LH", size=10, color=AMBER, bold=True, anchor="start"); f.text(130, 12, "Oestrogen", size=10, color=TEAL, bold=True, anchor="start"); f.text(215, 12, "Progesterone", size=10, color=RED, bold=True, anchor="start")
f.box(40, 262, 150, 28, "Menses 1-5", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(195, 262, 100, 28, "Ovulation 14", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(300, 262, 100, 28, "Luteal 15-28", fill=MINT, stroke=TEAL, size=10, bold=True)
f.text(220, 312, "Day of cycle", size=10.5, color=SLATE, bold=True)
```

## 4.3 The menstrual cycle, ovulation and dates in pregnancy

The cycle is run by the **hypothalamus (GnRH)**, **anterior pituitary (FSH, LH)** and **ovary (oestrogen, progesterone)**. In the **follicular phase** (days 1-14) FSH grows a follicle whose oestrogen rebuilds the endometrium (proliferative phase); rising oestrogen causes the **LH surge** and ovulation about 36 hours later. After ovulation the follicle becomes the **corpus luteum**, which makes progesterone for the **secretory phase** (days 15-28). If there is no pregnancy it degenerates and the endometrium is shed as menses. The **luteal phase is nearly constant at 14 days**, so ovulation occurs 14 days before the next period: day 14 in a 28-day cycle and day 18 in a 32-day cycle. The **fertile window** is the 5 days before ovulation plus the day of ovulation (sperm survive 5 days, the egg about 24 hours).

```python
from datetime import date, timedelta
lmp = date(2025, 6, 1)
edd = lmp + timedelta(days=280)
today = date(2025, 10, 12)
days = (today - lmp).days
print("EDD:", edd.strftime("%d %b %Y"))
print("Gestational age:", days // 7, "weeks", days % 7, "days")
print("Ovulation day (32-day cycle):", 32 - 14)
print("Fundal height at 28 weeks ~", 28, "cm")
```

```text
EDD: 08 Mar 2026
Gestational age: 19 weeks 0 days
Ovulation day (32-day cycle): 18
Fundal height at 28 weeks ~ 28 cm
```

**Naegele's rule** adds 7 days to the first day of the last menstrual period (LMP) and 9 months (or subtracts 3 months and adds 1 year). For an LMP of 1 June 2025 it gives **8 March 2026**, the same as counting 280 days (40 weeks), as the block shows. On 12 October 2025 the gestational age is 19 weeks. After 20 weeks the **fundal height** in cm roughly equals the weeks of gestation (± 2 cm): at 28 weeks the fundus is near 28 cm, and a lag of more than 3 cm suggests growth restriction or wrong dates. Pregnancy is divided into trimesters: first to 13 weeks, second 14-27, third 28-40.

## 4.4 Fertilisation, implantation and the placenta

Fertilisation in the ampulla makes a **zygote** that divides while travelling for about 3-4 days to the uterus. The **blastocyst** implants in the endometrium 6-7 days after fertilisation, and the trophoblast makes **hCG**, which keeps the corpus luteum making progesterone and is the hormone detected by the urine pregnancy test. The **placenta** (formed by 12 weeks) exchanges gases, nutrients and wastes, makes hormones (hCG, progesterone, oestrogen, hPL) and blocks most but not all germs and drugs: rubella, syphilis, HIV and many drugs (warfarin, isotretinoin) cross it. The umbilical cord has two arteries and one vein.

```svgfig label="4.1" caption="From fertilisation to implantation. Days are counted from fertilisation. The urine pregnancy test turns positive soon after implantation because hCG appears in the mother's blood."
f = Fig(760, 190)
st = [("Day 0\nFertilisation in\nampulla: zygote", ROSE, RED), ("Day 1-3\nCleavage: 2, 4, 8\ncells, morula", SAND, AMBER), ("Day 4-5\nBlastocyst enters\nuterus", BLUE, NAVY), ("Day 6-7\nImplants in the\nendometrium", MINT, TEAL), ("Week 3+\nhCG detectable,\nembryo forms", MINT, TEAL)]
for i, (t_, fc, sc) in enumerate(st):
    x = 8 + i * 150; f.box(x, 40, 130, 70, t_, fill=fc, stroke=sc, size=10, bold=True)
    if i < 4: f.arrow([(x + 130, 75), (x + 150, 75)], color=SLATE, sw=2)
f.text(380, 20, "Timeline of early development", size=11, color=SLATE, bold=True)
f.text(380, 140, "Folic acid 400 µg daily before conception and in the first 12 weeks prevents neural tube defects", size=10.5, color=RED, bold=True)
f.text(380, 160, "Nepal gives 180 iron-folic acid tablets in pregnancy; 4 antenatal visits (months 4, 6, 8, 9)", size=10.5, color=TEAL, bold=True)
```

## 4.5 Family planning in Nepal

Nepal offers free family planning through health posts and FPAN clinics. The national total fertility rate has fallen to about 2.1 children per woman (NDHS 2022). Methods are **short-acting** (condom, pills, injectable DMPA every 3 months), **long-acting** (Jadelle implant 5 years, copper T 380A IUCD 10 years, hormonal IUS) and **permanent** (vasectomy, minilaparotomy tubal ligation); **emergency contraception** (levonorgestrel 1.5 mg within 72 hours, best within 24 hours) is for unprotected sex. Effectiveness is measured by the **Pearl Index**: pregnancies per 100 woman-years = pregnancies × 1200 ÷ total months of use. If 3 pregnancies occur among 500 women followed for 12 months, the Pearl Index is 3 × 1200 ÷ 6000 = **0.6**, a very effective method.

## 4.6 Family planning counselling: eight points

Counselling by a nurse follows the **GATHER** steps (Greet, Ask, Tell, Help, Explain, Return) and the principle of free, informed choice protected by the Nepal Nursing Council Code of Ethics. These eight points should be covered with every client.

1. **Greet and build trust in private.** Welcome the client, use simple Nepali, ensure privacy and promise confidentiality. Many women fear family disapproval and need reassurance. Include the husband when the client wishes.
2. **Ask about needs and history.** Ask about age, number of children, desire for more children, breastfeeding, periods, illness and previous methods. Use the medical eligibility checklist to find conditions that rule out a method. Check blood pressure and exclude pregnancy.
3. **Explain every method simply.** Describe condoms, pills, DMPA, Jadelle, IUCD and permanent methods with their effectiveness, duration and return to fertility. Show samples and use a method chart. Let the client choose, not the nurse.
4. **Explain how the chosen method is used.** Teach pills at the same time every day, DMPA every 13 weeks (grace 4 weeks), condom for every act and IUCD string checks monthly after periods. Give a written date for the next visit. Ask the client to repeat the instructions.
5. **Describe common side effects.** DMPA often causes irregular bleeding or amenorrhoea, implants cause spotting, pills cause nausea in the first month and IUCD may increase menstrual flow. Reassure that these usually settle and are not harmful. Say that a client may return for removal or change at any time.
6. **Teach danger signs.** Pills: severe leg pain, chest pain, severe headache or yellow eyes. IUCD: lower abdominal pain, fever, foul discharge or missed period. Any of these needs urgent attendance at the health facility.
7. **Protect against infection.** Only the condom protects against HIV and STIs, so recommend dual protection for those at risk. Promote safer sex after migration and return of workers from abroad. Offer HIV and STI testing.
8. **Arrange follow-up and record.** Fix the next appointment, record the method in the register and HMIS/DHIS2 and give the card. Post-partum and post-abortion clients should leave with a method. Provide emergency contraception information to every client.

## Formula and fact sheet

- Ovulation is 14 days before the next menses: day 14 (28-day cycle), day 18 (32-day cycle). Fertile window = 5 days before ovulation + ovulation day.
- Naegele's rule: LMP + 7 days + 9 months. 280 days = 40 weeks. LMP 1 June 2025 gives 08 Mar 2026.
- Gestational age = days since LMP ÷ 7 (weeks) with remainder days: 19 weeks at 133 days. Fundal height (cm) ≈ weeks after 20 weeks.
- Pearl Index = pregnancies × 1200 ÷ woman-months = 0.6 in the example.
- Ganzoni iron deficit (mg) = weight × (target Hb − actual Hb) × 2.4 + 500 (iron stores). For 55 kg, Hb 9.5 to 11 it is **698 mg**.

## Chapter summary

- The testis makes sperm in 74 days and testosterone from Leydig cells; the ovary makes oestrogen and progesterone.
- The cycle is run by GnRH, FSH, LH, and ovulation comes 14 days before the next period.
- Naegele's rule and the 280-day count give the EDD; gestational age is counted from the LMP.
- hCG from the implanting embryo keeps the corpus luteum active and is the basis of the pregnancy test.
- Nepal offers free short-, long- and permanent family planning methods, and counselling follows GATHER.

## Practice

**MCQs (with reasons)**

1. Ovulation in a 32-day cycle occurs on about day: (a) 12 (b) 14 (c) 18 (d) 22.
2. The hormone detected by the urine pregnancy test is: (a) FSH (b) LH (c) progesterone (d) hCG.
3. LMP 1 June 2025: the EDD by Naegele's rule is: (a) 8 March 2026 (b) 1 April 2026 (c) 8 February 2026 (d) 15 March 2026.
4. Fertilisation normally occurs in the: (a) uterine cavity (b) ampulla of the fallopian tube (c) cervix (d) ovary.
5. The Jadelle implant protects for: (a) 3 months (b) 1 year (c) 5 years (d) 10 years.

::: note Answers and rationales
**1. (c).** The luteal phase is fixed at about 14 days, so ovulation is on day 32 − 14 = 18. Day 14 applies only to a 28-day cycle.
**2. (d).** hCG comes from the trophoblast soon after implantation. FSH and LH peak at ovulation and progesterone is not used in the strip test.
**3. (a).** Adding 7 days (8 June) and 9 months gives 8 March 2026, the same as 280 days.
**4. (b).** The egg is fertilised in the ampulla, the widest part of the tube, and the embryo then travels to the uterus.
**5. (c).** Jadelle (two rods of levonorgestrel) is licensed for 5 years; the copper T 380A lasts 10 years and DMPA 3 months.
:::

**Short answer (3 marks): Menstrual cycle phases.** The cycle averages 28 days. The follicular (proliferative) phase lasts to day 14: FSH grows the follicle, oestrogen rebuilds the endometrium and its peak causes the LH surge. Ovulation follows about 36 hours later. The luteal (secretory) phase is a fixed 14 days in which the corpus luteum makes progesterone; if there is no pregnancy it degenerates and menses start. Ovulation is therefore on day 14 in a 28-day cycle and day 18 in a 32-day cycle.

**Medium answer (5 marks): Describe the hormonal control of the menstrual cycle (Figure 4.2).** The **hypothalamus** releases GnRH in pulses, so the **anterior pituitary** releases **FSH and LH**. FSH grows 10-20 follicles and one becomes dominant; the granulosa cells make **oestrogen**, which thickens the endometrium (proliferative phase) and exerts negative feedback on FSH. When oestrogen stays high for about 2 days it gives **positive feedback**, causing the **LH surge** and ovulation at about day 14. After ovulation the **corpus luteum** makes **progesterone** and oestrogen, which prepare a secretory endometrium and raise the body temperature by 0.3-0.5 °C. Without fertilisation the corpus luteum fails after 14 days, the hormones fall and menses begin. If fertilisation occurs, hCG rescues the corpus luteum. Combined pills work by keeping the hormones steady so that the LH surge never occurs.

**Long answer (10 marks): Sunita Tamang, 22, a primigravida, attends the antenatal clinic of a district hospital on 12 October 2025. Her LMP was 1 June 2025. She is tired and dizzy; weight 55 kg, BP 110/70 mmHg, fundal height 19 cm, Hb 9.5 g/dL, conjunctival pallor. Calculate her dates and discuss her condition with a nursing care plan.**

*Dates.* The EDD by Naegele's rule is 1 June + 7 days + 9 months = **08 Mar 2026**, matching 280 days. The gestational age is 19 weeks 0 days, so she is in the second trimester, and the fundal height of 19 cm agrees with 19 weeks. The remaining time to term is 280 − 133 = **147 days**, so the 180 iron-folic acid tablets issued by the MoHP are enough until delivery.

*Condition.* **Moderate anaemia in pregnancy** (WHO: Hb below 11 g/dL; 10.0-10.9 mild, 7.0-9.9 moderate, below 7.0 severe). The plasma volume rises by 40-50% and the red cell mass by about 20%, so physiological dilution lowers Hb, and poor diet, worms and malaria add to it. The iron deficit by Ganzoni is 55 × (11 − 9.5) × 2.4 + 500 = **698 mg**. The risks are preterm birth, low birth weight, postpartum haemorrhage and heart failure. Management: oral iron 60 mg elemental iron with folic acid 400 µg daily, vitamin C food, deworming with albendazole 400 mg in the second trimester, treat malaria, and check Hb again in 4 weeks (rise of 1 g/dL expected). If she cannot tolerate oral iron or Hb falls, intravenous iron sucrose is used and delivery is planned at a facility with blood.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I feel tired and dizzy." **O:** Hb 9.5, pallor, pulse 96, BP 110/70. | **Fatigue** related to decreased haemoglobin and increased metabolic demand, as evidenced by tiredness and dizziness. | **Energy conservation:** reports less fatigue and Hb at least 10.5 g/dL in 4 weeks. | 1. Give iron-folic acid daily with water or citrus, not tea; *tannin blocks absorption.* 2. Rest on the left side for 2 hours in the afternoon; *improves placental blood flow.* 3. Teach slow position changes; *prevents dizziness.* 4. Repeat Hb at 4 weeks; *shows response.* | Hb and symptoms reviewed at next visit. |
| **S:** diet is mostly rice and dal, tea with meals. **O:** BMI 21, no meat. | **Imbalanced nutrition: less than body requirements** related to inadequate iron intake, as evidenced by pallor and low Hb. | **Nutritional status:** eats iron-rich food daily and gains 0.4 kg/week in the second trimester. | 1. Teach green leafy vegetables, liver, egg, soybean and jaggery with lemon; *haem and vitamin C raise absorption.* 2. Avoid tea and coffee for 2 hours around meals; *less iron blocked.* 3. Weigh each visit; *tracks weight gain.* | Food recall and weight gain checked. |
| **O:** primigravida, has not attended earlier, lives far from the hospital. | **Risk for ineffective childbearing process** related to anaemia and limited access, as evidenced by late booking. | **Maternal-foetal health:** completes four ANC visits and plans a facility birth. | 1. Explain the four ANC visits (months 4, 6, 8, 9) and the Aama incentive; *encourages attendance.* 2. Teach danger signs: bleeding, severe headache, blurred vision, reduced movement; *early referral.* 3. Prepare a birth plan with transport and blood donor; *prevents delay.* | ANC card shows visits; birth plan written. |
| **S:** "Will the tablets harm my baby?" **O:** missed 2 weeks of tablets due to constipation. | **Deficient knowledge** about iron therapy, as evidenced by non-adherence. | **Knowledge: medication:** states dose, side effects and how to reduce them within 1 visit. | 1. Teach that dark stool is normal; *reduces fear.* 2. Advise fibre, water and fruit for constipation; *lessens side effect.* 3. Return demonstration of pill-taking schedule; *confirms understanding.* | Patient repeats instructions and takes tablets daily. |

*Prevention and education.* Deworm, eat iron-rich food, delay first pregnancy until after 20 years, and attend ANC. *Conclusion.* Early detection by Hb and fundal height lets the nurse prevent anaemia-related complications at delivery.

::: tip Exam tip
In any pregnancy question first write the EDD and gestational age with the working. Quote the WHO Hb cut-offs and the MoHP iron-folic schedule, since both are asked in the viva.
:::

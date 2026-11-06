---
subject: Midwifery I
grade: BSc Nursing Year 3
unit: 5
title: The Normal Newborn, Immediate Care and APGAR, the Puerperium, Postnatal Visits and Lactation
hours: 20
area: BSN 17-18 · Midwifery I · Units 8-10
---

Mina Gurung, 25, is on day 3 after her first birth in a Pokhara hospital. Her baby boy weighed 3,200 g at birth and 2,950 g today. Her breasts are hard and tender, her left nipple is cracked, and her mother-in-law has told her to give honey water "because the milk has not come". The nurse has three jobs at the same bedside: **protect the newborn** (warmth, feeding, infection), **check the mother's recovery** (uterus, bleeding, perineum, mood) and **support breastfeeding** so the family does not stop at the first difficulty. This unit covers the **immediate care of the newborn**, the **APGAR score**, the **normal newborn and its examination**, the **puerperium** and **postnatal visits**, and **lactation**.

::: key What this unit gives you
- Real images: a **newborn seconds after birth**, a **nurse weighing a baby**, **skin-to-skin contact with breastfeeding**, **kangaroo mother care**, the **APGAR chart** and the **Helping Babies Breathe** action plan; with numbered marks.
- SVG figures: the **newborn resuscitation algorithm** (the golden minute), **involution of the uterus and lochia**, and the **lactation reflex loop** (prolactin and oxytocin).
- **Eight danger signs of the newborn** and an **eight-point postnatal check**, each in 3-4 plain sentences, anchored in IMNCI Nepal, the NIP, the Aama programme and WHO.
- Verified maths: **APGAR**, **weight loss percentage**, **fluid volume per feed**, **vitamin A and IFA counts**; MCQs, short, medium and long answers and a 5-column NANDA-I plan for a postnatal mother.
:::

## 5.1 Immediate care of the newborn: the golden minute

Of 1,000 live births in Nepal, **21 die within the first 28 days** (NDHS 2022), most of them in the first 48 hours, from **birth asphyxia, prematurity and infection**, and the rate has not fallen since 2016. The first minutes decide survival. WHO and the MoHP's **Helping Babies Breathe (HBB)** programme teach a **"golden minute"**: within the first 60 seconds the baby must be **dried, stimulated, checked for breathing and, if needed, ventilated** (Figure 5.1).

```svgfig label="5.1" caption="The newborn resuscitation algorithm (golden minute), based on Helping Babies Breathe. Every birth needs a ready table, a clean warm cloth, a suction bulb and a bag and mask of the right size (size 1 for term, size 0 for small babies). Dry and stimulate; if the baby is breathing well or crying, give skin-to-skin care; if not breathing after 30 seconds, clamp and cut the cord, clear the airway and give bag-and-mask ventilation at 40-60 breaths a minute. If the heart rate is below 100 or breathing is poor after ventilation, improve ventilation and call for help; if there is no response after 10 minutes of effective ventilation, discuss stopping with the team."
f = Fig(760, 340)
f.box(280, 8, 200, 44, "BIRTH: ask 'Is the baby breathing\nor crying? Good tone?'", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.arrow([(280, 40), (170, 80)], color=TEAL, sw=2, label="yes", lpos=(210, 55))
f.arrow([(480, 40), (590, 80)], color=RED, sw=2, label="no", lpos=(550, 55))
f.box(40, 80, 260, 70, "ROUTINE CARE\ndry, skin-to-skin, cover with cap and cloth\ndelayed cord clamp 1-3 min, breastfeed in 1 h", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(460, 80, 280, 70, "THE GOLDEN MINUTE\ndry thoroughly, remove wet cloth,\nstimulate by rubbing the back, position head", fill=SAND, stroke=AMBER, size=10, bold=True)
f.arrow([(600, 150), (600, 175)], color=RED, sw=2, label="not breathing after 30 s", lpos=(655, 165))
f.box(460, 175, 280, 70, "CLAMP AND CUT THE CORD, clear the airway\nBAG-AND-MASK 40-60 breaths/min\nwatch the chest rise; check heart rate", fill=ROSE, stroke=RED, size=10, bold=True)
f.arrow([(600, 245), (600, 270)], color=RED, sw=2)
f.box(460, 270, 280, 55, "HR under 100 or no breathing: improve\nventilation, call for help, refer to NICU", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(40, 175, 260, 70, "KEEP WARM (36.5-37.5 C)\ncap, dry cloth, skin-to-skin, closed room\nNO bath for the first 24 hours", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(40, 270, 260, 55, "Chlorhexidine 7.1% to the stump,\nvitamin K 1 mg IM, eye care, BCG per NIP", fill=SOFT, stroke=SLATE, size=10, bold=True)
```

**Routine care in the first hour.** (1) Dry the baby with a warm cloth, cover the head and place him skin to skin on his mother (this keeps him warm and begins breastfeeding). (2) Clamp the cord at 1-3 minutes. (3) Apply **chlorhexidine 7.1% gel** to the stump (Nepal's programme reduces cord infection and mortality). (4) Give **vitamin K 1 mg IM** (prevents bleeding disease) and eye care as per hospital protocol. (5) Weigh and measure after the first feed. (6) Start breastfeeding **within one hour**. (7) Give **BCG** at birth according to the NIP. (8) Delay bathing for 24 hours; keep the baby with the mother (rooming-in).

### The APGAR score

Dr Virginia Apgar (1952) devised a score at **1 and 5 minutes** (and every 5 minutes up to 20 if low) to show how well the baby has adapted. Five signs are scored 0, 1 or 2 (Plate 5.2): **A**ppearance (colour), **P**ulse (heart rate), **G**rimace (reflex), **A**ctivity (tone) and **R**espiration. **7-10** is normal, **4-6** moderately depressed and **0-3** severely depressed. **APGAR does not decide when to start resuscitation:** the midwife starts as soon as the baby is not breathing, without waiting for one minute.

```python
sign = {"Heart rate over 100": 2, "Respiration good, crying": 2, "Muscle tone active motion": 2, "Reflex grimace": 1, "Colour body pink, hands blue": 1}   # 1 minute
apgar1 = sum(sign.values())
apgar5 = 2 + 2 + 2 + 1 + 2                       # 5 minutes
band = lambda s: "normal" if s >= 7 else "moderately depressed" if s >= 4 else "severely depressed"
low = {"HR below 100": 1, "slow irregular": 1, "some flexion": 1, "grimace": 1, "blue pale": 0}
apgar_low = sum(low.values())
bw, d3 = 3000, 2790                              # birth weight and day-3 weight, g
loss = (bw - d3) / bw * 100
fluid_day3 = 100 * d3 / 1000                     # 100 mL/kg/day on day 3
per_feed = fluid_day3 / 8
print(f"APGAR 1 min = {apgar1} ({band(apgar1)}); 5 min = {apgar5} ({band(apgar5)}); depressed baby = {apgar_low} ({band(apgar_low)})")
print(f"Weight {bw} -> {d3} g = {loss:.1f}% loss (acceptable up to 10%); day-3 fluid {fluid_day3:.0f} mL/day = {per_feed:.1f} mL per feed in 8 feeds")
```

```text
APGAR 1 min = 8 (normal); 5 min = 9 (normal); depressed baby = 4 (moderately depressed)
Weight 3000 -> 2790 g = 7.0% loss (acceptable up to 10%); day-3 fluid 279 mL/day = 34.9 mL per feed in 8 feeds
```

The baby scores **8** at 1 minute (normal) and **9** at 5 minutes. A baby with a heart rate below 100, slow irregular breathing, some flexion, grimace and a pale blue colour scores **4** (moderately depressed) and needs stimulation and possibly ventilation. A baby of 3,000 g who weighs 2,790 g on day 3 has lost **7.0%** (physiological, up to 10%, regained by 10-14 days) and needs about **279 mL a day** (100 mL/kg), which is **34.9 mL per feed** in 8 feeds.

```photogrid label="5.1" cols="4" ratio="1.0" caption="The newborn in real images. (a) A baby seconds after birth, wet, crying and still attached to the cord: crying and good tone mean routine care. (b) A nurse recording the weight on a digital baby scale (normal 2.5-4 kg). (c) Skin-to-skin contact and the first breastfeed: the baby in a cap lies on the mother's chest. (d) Kangaroo mother care: a small baby is carried skin to skin against the mother's chest, warm and breastfeeding."
@ photo id="nur11/newborn" cap="Baby just born"
fit 1.0
focus 0.35 0.5
mark 0.27 0.62 "1"
mark 0.62 0.30 "2"
key 1 (a) Face: wide open mouth, crying (breathing well)
key 2 (a) Umbilical cord, still unclamped, cut after 1-3 minutes
@ photo id="nur11/babywt" cap="Baby weighed on a scale"
fit 1.0
focus 0.58 0.5
mark 0.62 0.30 "3"
mark 0.30 0.52 "4"
key 3 (b) Baby on a digital scale with a warm cover underneath
key 4 (b) Nurse records the weight on the chart
@ photo id="nur11/skin" cap="Skin-to-skin and first feed"
fit 1.0
focus 0.5 0.5
mark 0.50 0.32 "5"
mark 0.50 0.82 "6"
key 5 (c) Baby in a warm cap, chest to chest with the mother
key 6 (c) Mother looks at the baby: bonding and oxytocin release
@ photo id="nur11/kmc" cap="Kangaroo mother care"
fit 1.0
focus 0.55 0.5
mark 0.58 0.62 "7"
key 7 (d) Baby wrapped and held against the mother's skin (KMC)
```

```photogrid label="5.2" cols="2" ratio="1.5" caption="Two tools for the first minutes. (a) The APGAR chart: five signs (heart rate, respiratory effort, muscle tone, reflex irritability, colour), each scored 0, 1 or 2; a total of 7-10 is normal, 4-6 moderately depressed and 0-3 severely depressed. (b) The top of the Helping Babies Breathe action plan: prepare for birth, dry thoroughly, check crying or breathing, keep warm, and ventilate in the golden minute."
@ photo id="nur11/apgar" cap="APGAR evaluation chart"
fit 1.5
focus 0.5 0.5
mark 0.55 0.73 "1"
key 1 (a) Heart rate row: over 100 scores 2, below 100 scores 1, absent 0
@ photo id="nur11/hbb" cap="HBB action plan (upper part)"
fit 1.5
focus 0.5 0.86
```

## 5.2 The normal newborn

A **term newborn** (37-41 weeks) has these normal values: **weight 2.5-4 kg** (mean 3 kg), **length 48-52 cm**, **head circumference 33-35 cm** (about 2 cm more than the chest), **temperature 36.5-37.5 °C**, **heart rate 120-160**, **respiratory rate 40-60** (periodic breathing normal), and **urine within 24 hours and meconium within 48 hours**. **Low birth weight** is under 2.5 kg and **very low** under 1.5 kg; babies under 2 kg or under 35 weeks need special care or KMC in Nepal's guidelines.

| Examination | Normal findings | Report if |
|---|---|---|
| **Head** | Moulding or caput that fades in 2-3 days; anterior fontanelle 3-4 cm, flat | Bulging or sunken fontanelle; cephalhaematoma growing |
| **Skin** | Pink; vernix; **Mongolian spots**, milia, erythema toxicum | Pallor, blue lips, jaundice in the first 24 hours |
| **Eyes, mouth** | Clear eyes; intact palate; Epstein pearls | Pus from eyes; cleft palate; white patches (thrush) |
| **Chest and heart** | Symmetrical; grunt-free breathing; no murmur or soft murmur | Fast breathing 60 or more, chest indrawing, grunting |
| **Abdomen and cord** | Soft; two arteries and one vein in cord; dry stump | Distension; pus, redness around the cord; bleeding |
| **Genitalia, anus** | Girls: vaginal discharge and pseudo-menses; boys: testes descended | No anal opening; hypospadias; no urine for 24 hours |
| **Limbs and hips** | Full movement; ten fingers and toes; hips stable (Barlow and Ortolani) | Club foot; click or unstable hip; extra digits |
| **Reflexes** | **Moro** (startle, to 4-6 months), **rooting and sucking**, **palmar grasp**, **stepping** | Absent or asymmetric reflexes |

## 5.3 Eight danger signs of the newborn (IMNCI Nepal)

Nepal's IMNCI for the sick young infant (birth to 2 months) classifies the baby as having **possible serious bacterial infection (PSBI)** if **any one** of these signs is present. The FCHV and the mother must know them, because neonatal sepsis can kill in hours.

1. **Not feeding well.** The baby who sucked well and now refuses, or sucks weakly, may be getting sick. Feeding is the baby's "daily exam". Ask the mother how many feeds in 24 hours; fewer than 8 is a warning.
2. **Convulsions.** Rhythmic jerking, staring or stiffness may be caused by sepsis, meningitis, low blood sugar or birth asphyxia. Protect the baby, check temperature and sugar, and refer urgently. Never ignore "fits" in a newborn.
3. **Fast breathing.** Count the respiratory rate for one full minute while the baby is calm: **60 per minute or more** is fast. It suggests pneumonia or sepsis. Repeat the count if the first is high.
4. **Severe chest indrawing.** The lower chest wall goes in with each breath, which shows hard work of breathing. Mild indrawing is normal in the newborn, but severe indrawing is not. Keep the baby warm and refer.
5. **Fever or low temperature.** A temperature of **37.5 °C or more**, or **below 35.5 °C**, is dangerous. Cold babies are hypoglycaemic and sick. Rewarm by skin-to-skin contact and a cap and refer.
6. **Movement only when stimulated or no movement.** A floppy, sleepy baby who does not wake to touch is seriously ill. Check blood sugar and temperature. Refer at once.
7. **Central cyanosis or pallor.** Blue lips and tongue indicate poor oxygenation (heart or lung disease); severe pallor suggests blood loss or haemolysis. Give oxygen if available and refer. Hands and feet may be blue in the first hours and this is normal.
8. **Jaundice in the first 24 hours, yellow palms and soles, or pus from the umbilicus.** Jaundice in the first day is always pathological (haemolysis, Rh or ABO incompatibility); yellow palms and soles show severe jaundice; pus and redness around the stump show omphalitis. Treat the infection and refer for phototherapy.

## 5.4 The puerperium: physiology and postnatal visits

The **puerperium** is the period from the delivery of the placenta until **6 weeks (42 days)**, when the reproductive organs return to the non-pregnant state. The main change is **involution of the uterus**: it weighs about **1,000 g** at birth (fundus at or just below the umbilicus), **500 g** at one week, about **350 g** at two weeks and **60 g** at six weeks, and the fundus descends about **1 cm a day** until it is no longer palpable above the pubis at about 10-14 days. Contraction of the muscle fibres (the "living ligatures") closes the placental site; **after-pains** from oxytocin are stronger in multiparae and breastfeeding mothers. The **endometrium** regenerates in 3 weeks, except at the placental site (6 weeks), and the **cervix** closes to 1 cm in a week. **Lochia** is the uterine discharge (Figure 5.2).

```svgfig label="5.2" caption="Involution and lochia in the puerperium. Lochia rubra (blood, decidua) lasts for the first 3-4 days; lochia serosa (pink-brown, serum and white cells) from day 4 to day 10; lochia alba (cream-yellow, mucus and white cells) from about day 10 to 6 weeks. The uterus shrinks from about 1,000 g to 60 g and the fundus descends about one finger-breadth a day. Heavy red bleeding after day 4, a foul smell, fever, or a uterus that is soft and high are signs of retained products, infection or secondary PPH."
f = Fig(760, 300)
f.text(20, 24, "Lochia (days after birth)", size=11, color=NAVY, bold=True, anchor="start")
f.box(20, 36, 120, 44, "RUBRA\nday 1-4: red", fill="#fee2e2", stroke=RED, size=10.5, bold=True)
f.box(140, 36, 240, 44, "SEROSA\nday 4-10: pink-brown", fill="#fed7aa", stroke=AMBER, size=10.5, bold=True)
f.box(380, 36, 360, 44, "ALBA\nday 10 to 6 weeks: cream-yellow, scanty", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.text(20, 112, "Uterus weight and fundal level", size=11, color=NAVY, bold=True, anchor="start")
for i, (a, b) in enumerate([("BIRTH", "1,000 g\nfundus at navel"), ("1 WEEK", "500 g\nfundus 7-8 cm\nabove pubis"), ("2 WEEKS", "350 g\nnot palpable\nabdominally"), ("6 WEEKS", "60 g\nnormal size")]):
    x = 20 + i * 185
    f.box(x, 124, 165, 70, a + "\n" + b, fill=BLUE, stroke=NAVY, size=10.5, bold=True)
    if i < 3: f.arrow([(x + 165, 159), (x + 185, 159)], color=SLATE, sw=2)
f.box(20, 215, 355, 70, "NORMAL: uterus firm, midline, descending\nlochia matching the day, no fever, pulse 60-90,\nvoids freely, passes stool by day 3", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(395, 215, 345, 70, "REFER: soft, high, tender uterus; foul or heavy\nred lochia after day 4; fever 38 C or more;\ncalf pain; severe headache or fits", fill=ROSE, stroke=RED, size=10.5, bold=True)
```

**Other changes.** **Diuresis** in the first 2-5 days clears the extra fluid; the **blood volume** returns to normal in about 6 weeks and the **clotting factors** stay raised for 2 weeks (a risk for thrombosis). **Weight** falls by 5-6 kg at birth and another 2-3 kg in the first weeks. **Menstruation** returns at about 6-8 weeks in a non-breastfeeding mother and later in an exclusively breastfeeding mother. **Psychologically** the mother passes through **taking-in** (day 1-2, passive, talkative), **taking-hold** (day 3-10, active but anxious) and **letting-go** (weeks later). **Baby blues** (day 3-10) are normal; **postnatal depression** (low mood over 2 weeks, no interest in the baby) needs referral and support (Psychiatric Nursing).

**Postnatal care in Nepal.** The **mother and baby stay in the facility for at least 24 hours** after normal birth, and the Safe Motherhood protocol schedules postnatal visits at **24 hours, day 3, day 7-14 and 6 weeks**; check the current MoHP circular because the number counted for Aama incentives is three. NDHS 2022 found that **70%** of mothers and newborns had a postnatal check within 2 days, so one in three goes home without it. The mother receives **vitamin A 200,000 IU (one capsule)** within 6 weeks, **IFA tablets for 45 days** after delivery, counselling on **family planning** (LAM, implants, IUCD, pills, injectable; postpartum IUCD within 48 hours is possible), and the baby gets **BCG**, and the NIP schedule starts at 6 weeks (Child Health Nursing).

## 5.5 Eight-point postnatal check (the "BUBBLE-HEE" examination)

The nurse examines the mother from the breasts to the legs, in the same order each time, with privacy and consent.

1. **Breasts.** Look for fullness, hardness, red wedge-shaped areas, cracked nipples and the baby's feeding position. Engorgement peaks on day 3-5 and is relieved by frequent feeding. A hot, red, painful area with fever suggests mastitis. Teach hand expression.
2. **Uterus.** With the bladder empty, rub up the fundus gently if soft and check height, firmness and tenderness. It should be firm, round and descend about 1 cm a day. A soft, high or tender uterus suggests retained products or infection.
3. **Bladder.** Ask when she last passed urine and how much. She should pass urine within 6 hours; a full bladder displaces the uterus and increases bleeding. Burning or frequency suggests urinary infection.
4. **Bowels.** Ask about stool and fear of pain from stitches. She should pass stool by day 2-3. Give fluids, fibre and a gentle laxative if needed; piles are common.
5. **Lochia.** Check the amount (pad count), colour and smell against the expected stage (Figure 5.2). A saturated pad within an hour, clots larger than a plum or a foul smell are danger signs. Record on the postnatal card.
6. **Episiotomy and perineum.** Inspect the wound for swelling, redness, discharge or breakdown. Teach washing with clean water after each toilet use, patting dry, front to back, and changing pads often. Sitz baths with warm water help comfort and healing.
7. **Homan's sign, legs and vital signs.** Check calves for pain, redness or swelling (DVT) and take temperature, pulse and BP. Fever 38 °C or more after 24 hours suggests puerperal sepsis. High BP in the first 6 weeks may be postpartum pre-eclampsia.
8. **Emotions, bonding and advice.** Ask about sleep, appetite, mood and support at home, and watch how she holds and speaks to the baby. Teach rest, food (extra 500 kcal a day while breastfeeding), danger signs, hygiene, family planning and the next visit. Respect traditions such as *sutkeri* diets and 11-day rest, correct only harmful ones.

## 5.6 Lactation and breastfeeding

During pregnancy **oestrogen and progesterone** grow the ducts and alveoli but **block milk production**; after the placenta leaves, their level falls and **prolactin** can act. Milk production is controlled by the **prolactin reflex** (suckling signals the hypothalamus and anterior pituitary, releasing prolactin, which makes milk in the alveoli) and milk release by the **oxytocin reflex** (suckling releases oxytocin from the posterior pituitary, which contracts the cells around the alveoli, the "let-down") (Figure 5.3). **The more the baby suckles, the more milk is made; anxiety and pain block the oxytocin reflex.**

```svgfig label="5.3" caption="Lactation reflexes. Suckling stimulates nerves in the nipple. The hypothalamus signals the anterior pituitary to release prolactin, which makes milk (the milk-making reflex, strongest at night). It also signals the posterior pituitary to release oxytocin, which squeezes milk out of the alveoli (the let-down or milk-ejection reflex). Pain, fear and embarrassment block the let-down; thoughts of the baby, the sight and cry of the baby and a calm place help it. Frequent feeding and emptying the breast keep production high."
f = Fig(760, 300)
f.box(20, 120, 150, 60, "SUCKLING\nnerves in the nipple", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.arrow([(170, 140), (250, 80)], color=SLATE, sw=2); f.arrow([(170, 160), (250, 220)], color=SLATE, sw=2)
f.box(250, 50, 190, 60, "ANTERIOR PITUITARY\nPROLACTIN", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(250, 190, 190, 60, "POSTERIOR PITUITARY\nOXYTOCIN", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(440, 80), (520, 80)], color=NAVY, sw=2); f.arrow([(440, 220), (520, 220)], color=TEAL, sw=2)
f.box(520, 50, 220, 60, "ALVEOLI MAKE MILK\n(more suckling = more milk)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(520, 190, 220, 60, "LET-DOWN: cells squeeze\nmilk into the ducts; uterus contracts", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(250, 130, 190, 40, "Pain, fear, stress BLOCK let-down", fill=ROSE, stroke=RED, size=10, bold=True)
```

**Colostrum** (first 2-3 days) is thick, yellow and rich in IgA, protein and white cells, a natural first vaccine, and it is **never** to be thrown away or replaced by honey water, *ghee* or animal milk. **Mature milk** comes at day 3-5 (the "milk comes in"). **Exclusive breastfeeding for 6 months** (WHO, MoHP), on demand, **8-12 times in 24 hours**, then continued with complementary foods to 2 years or more. Benefits: protects against diarrhoea, pneumonia and sepsis, lowers infant deaths, supports brain growth, helps the uterus involute, lowers maternal bleeding and some cancers, delays pregnancy (LAM) and costs nothing.

**Good attachment** shows four signs: **the chin touches the breast, the mouth is wide open, the lower lip is turned out, and more areola is seen above than below the mouth**. A good **position** has the baby's body in a straight line, facing the breast, held close and supported (cradle, cross-cradle, football or side-lying). **Common problems:** *engorgement* (feed often, express, warm before and cold after); *sore or cracked nipples* (correct attachment, apply hind milk, do not stop feeding); *blocked duct and mastitis* (continue feeding from that breast, rest, fluids, antibiotics if fever); *low supply perceived* (feed more often, skin contact); and *HIV* (mothers on ART should breastfeed exclusively for 6 months per WHO and Nepal guidance). **LAM** is more than 98% effective when the baby is under 6 months, the mother is fully or nearly fully breastfeeding and her periods have not returned.

```python
from datetime import date, timedelta
birth_day = date(2026, 3, 10)
visits = [birth_day + timedelta(days=d) for d in (1, 3, 7, 42)]   # 24 h, day 3, day 7, day 42
bw3, w3 = 3200, 2950                                              # Mina's baby: birth and day-3 weight
loss = (bw3 - w3) / bw3 * 100
fluid = 100 * w3 / 1000                                           # 100 mL/kg/day on day 3
feed = fluid / 8
vit_a = 1                                                         # one capsule of 200,000 IU
ifa_45 = 45
print("Visits: " + ", ".join(f"{v:%d %b}" for v in visits))
print(f"Weight loss {loss:.1f}% (limit 10%); day-3 fluid {fluid:.0f} mL/day = {feed:.1f} mL per feed; vitamin A {vit_a} capsule; IFA {ifa_45} tablets")
```

```text
Visits: 11 Mar, 13 Mar, 17 Mar, 21 Apr
Weight loss 7.8% (limit 10%); day-3 fluid 295 mL/day = 36.9 mL per feed; vitamin A 1 capsule; IFA 45 tablets
```

With birth on 10 March the four postnatal visits fall on **11 March, 13 March, 17 March and 21 April**. Mina's baby has lost **7.8%** of his birth weight (within 10%), needs **295 mL** a day on day 3, which is **36.9 mL** per feed in 8 feeds, and she receives **one** vitamin A capsule and **45** IFA tablets.

## Formula and fact sheet

- **APGAR** (1 and 5 min): appearance, pulse, grimace, activity, respiration; 7-10 normal, 4-6 moderate, 0-3 severe. Start resuscitation without waiting for the score. Bag-and-mask 40-60 breaths per minute.
- **Newborn:** weight 2.5-4 kg; HR 120-160; RR 40-60 (60 or more is fast); temperature 36.5-37.5 °C; weight loss up to 10%, regained by 10-14 days; fluid 60 mL/kg on day 1 rising to 150 mL/kg by day 5-7.
- **Routine newborn care:** dry, skin to skin, cord clamp 1-3 min, chlorhexidine 7.1%, vitamin K 1 mg IM, BCG, breastfeed within 1 hour, no bath for 24 hours.
- **Puerperium:** 6 weeks; uterus 1,000 g to 60 g; fundus falls 1 cm a day; lochia rubra 1-4 days, serosa 4-10 days, alba to 6 weeks; PNC at 24 hours, day 3, day 7-14, week 6; vitamin A 200,000 IU, IFA 45 days.
- **Breastfeeding:** exclusive for 6 months, 8-12 feeds a day; four signs of good attachment; LAM over 98% if under 6 months, fully breastfeeding and amenorrhoeic.

## Chapter summary

- The first minute decides survival: dry, stimulate, check breathing, ventilate within the golden minute, and keep the baby warm and skin to skin.
- APGAR describes adaptation at 1 and 5 minutes but does not delay resuscitation; the normal newborn loses up to 10% of weight and regains it in 10-14 days.
- Any one of the eight IMNCI signs (poor feeding, fits, fast breathing, indrawing, fever or cold, no movement, central cyanosis, early jaundice or pus) means refer urgently.
- In the puerperium the uterus involutes (1,000 g to 60 g) and lochia changes from red to white; the BUBBLE-HEE check finds retained products, sepsis, DVT and depression early.
- Breastfeeding works through the prolactin and oxytocin reflexes; good attachment, early and frequent feeds and exclusive breastfeeding for 6 months protect the baby, and LAM spaces births.

## Practice

```python
from datetime import date, timedelta
m1 = date(2026, 3, 10) + timedelta(days=7)               # MCQ1 postnatal visit on day 7
m2 = (3500 - 3200) / 3500 * 100                          # MCQ2 weight loss, %
apgar = 2 + 1 + 1 + 1 + 0                                # MCQ4 HR over 100, slow breathing, some flexion, grimace, blue
mina_loss = (3200 - 2950) / 3200 * 100
mina_fluid = 100 * 2.95
mina_feed = mina_fluid / 8
print(f"MCQ1 = {m1:%d %b}; MCQ2 = {m2:.1f}%; MCQ4 = {apgar}")
print(f"Mina's baby: loss {mina_loss:.1f}%; fluid {mina_fluid:.0f} mL/day; {mina_feed:.1f} mL per feed; weight at day 3 = {2950} g")
```

```text
MCQ1 = 17 Mar; MCQ2 = 8.6%; MCQ4 = 5
Mina's baby: loss 7.8%; fluid 295 mL/day; 36.9 mL per feed; weight at day 3 = 2950 g
```

**MCQs (with reasons)**

1. A mother gave birth on 10 March. Her postnatal visit on day 7 falls on: (a) 14 March (b) 16 March (c) 17 March (d) 21 April.
2. A baby born at 3,500 g weighs 3,200 g on day 3. The weight loss is about: (a) 3% (b) 6% (c) 8.6% (d) 12%.
3. Lochia serosa is: (a) red, day 1-4 (b) pink-brown, day 4-10 (c) cream, day 10-42 (d) clear, week 8.
4. A baby has heart rate over 100, slow irregular breathing, some flexion, grimace and a blue colour. The APGAR score is: (a) 3 (b) 4 (c) 5 (d) 6.
5. A 10-day-old baby breathes 64 times a minute with a calm chest. The correct classification is: (a) normal (b) fast breathing: possible serious bacterial infection (c) mild cough only (d) transient tachypnoea needing no action.

::: note Answers and rationales
**1. (c).** 10 March + 7 days = 17 March; (a) is day 4, and (d) is the 6-week visit.
**2. (c).** (3,500 - 3,200) ÷ 3,500 × 100 = 8.6%, within the acceptable 10%; 12% would need feeding assessment.
**3. (b).** Serosa is pink-brown from day 4 to 10; red is rubra and cream is alba.
**4. (c).** Heart rate over 100 = 2, slow breathing = 1, some flexion = 1, grimace = 1, blue colour = 0, so 2 + 1 + 1 + 1 + 0 = 5 (moderately depressed); 4 or 6 come from mis-scoring one sign.
**5. (b).** 60 or more per minute in a young infant is fast breathing and a PSBI sign in IMNCI; the baby must be referred, not watched at home.
:::

**Short answer (3 marks): Write the APGAR score.** APGAR is scored at 1 and 5 minutes on five signs, each 0, 1 or 2: **A**ppearance (colour), **P**ulse (heart rate over 100 scores 2), **G**rimace (reflex response), **A**ctivity (muscle tone) and **R**espiration. A total of **7-10** is normal, **4-6** moderate depression (stimulate, oxygen) and **0-3** severe depression (resuscitate). The score is recorded but resuscitation must begin at once if the baby is not breathing.

**Medium answer (5 marks): Describe involution of the uterus and lochia (Figure 5.2).** Involution is the return of the uterus to its non-pregnant size in 6 weeks. The uterus weighs 1,000 g at birth with the fundus at the umbilicus, 500 g at one week, 350 g at two weeks and about 60 g at six weeks; the fundus falls about 1 cm a day and is not palpable abdominally by day 10-14. Contraction of the muscle fibres closes the vessels at the placental site, and the endometrium heals by about 3 weeks (the placental site by 6 weeks). Breastfeeding speeds involution through oxytocin. **Lochia** is the vaginal discharge: **rubra** (red, blood and decidua) for days 1-4, **serosa** (pink-brown) from day 4 to 10, and **alba** (cream-yellow) from day 10 to about 6 weeks. Normal lochia has a fleshy smell; a foul smell, heavy red bleeding after day 4, a soft or high tender uterus or fever suggests infection or retained products. Nursing care includes fundal checks, pad count, perineal hygiene, early ambulation, fluids and teaching danger signs.

**Long answer (10 marks): Mina Gurung, 25, P1, is on day 3 after a normal birth (baby boy 3,200 g, today 2,950 g). Her breasts are engorged, her left nipple is cracked and she gave honey water because "the milk had not come". Temperature is 37.2 °C, pulse 78, fundus firm 3 cm below the umbilicus, lochia rubra, perineal stitches clean. Calculate the baby's weight loss and fluid need and write the care plan.**

*Calculations.* The baby has lost 250 g, which is **7.8%** of his birth weight (within the 10% limit and expected to return to 3,200 g by 10-14 days). On day 3 he needs about 100 mL/kg, which is **295 mL a day** or **36.9 mL per feed** in 8 feeds; this is easily met by breast milk, so **no honey water or animal milk** is needed. Mina needs one vitamin A capsule (200,000 IU) and **45 IFA tablets** after delivery, and the baby's next checks are on day 7 and at 6 weeks.

*Care.* The nurse praises her for starting breastfeeding, and corrects the belief about honey water gently, by explaining that colostrum is the baby's first vaccine and that honey water can carry infection and reduce suckling. She watches a feed and corrects the **attachment** (chin touching, wide mouth, lower lip out, more areola above), shows the **cross-cradle** hold, and teaches **hand expression** and warm compresses before and cold afterward to relieve engorgement; she applies expressed milk to the cracked nipple and advises feeding from the less sore side first. She teaches 8-12 feeds a day, and checks the baby for urine 6 times a day and stool, jaundice, temperature, cord and breathing, teaching the eight danger signs. She examines Mina (BUBBLE-HEE), teaches perineal hygiene, fluids and rest, explains LAM and offers a family planning method, and arranges follow-up with the FCHV.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "My breasts are rock hard and it hurts." **O:** bilateral engorgement, left nipple cracked. | **Acute pain** related to breast engorgement and nipple trauma. | **Pain level:** 3 or less in 24 hours. | Feed 8-12 times and express (empties the breast); warm before, cold after (let-down, swelling); apply hind milk to cracks (heals). | Pain 2/10; engorgement eased. |
| **S:** "The baby will not stay on the nipple." **O:** shallow latch, chin away from breast. | **Ineffective breastfeeding** related to poor attachment and maternal knowledge deficit. | **Breastfeeding establishment:** baby latched well and swallowing within 48 hours. | Teach the four signs of attachment and positions (good latch stops damage); observe a full feed; stop honey water (protects supply and the gut). | Latch good; audible swallowing. |
| **O:** episiotomy wound, lochia rubra, 3 days postpartum. | **Risk for infection** related to perineal wound and breast trauma. | **Infection status:** afebrile and wound healing through 6 weeks. | Perineal care, pad changes, hand hygiene, fluids (prevent wound infection); temperature daily; report fever or foul lochia (early sepsis). | Temperature normal; wound clean. |
| **S:** "Is it normal that he is losing weight?" **O:** 7.8% weight loss. | **Deficient knowledge** about newborn care and danger signs. | **Knowledge:** names 5 newborn danger signs and the feeding schedule before discharge. | Explain physiological weight loss and 8-12 feeds (reassures); teach IMNCI danger signs and cord care with chlorhexidine; give the card. | Repeats danger signs correctly. |
| **S:** "I slept two hours last night." **O:** tired, tearful at times. | **Disturbed sleep pattern** and risk for postpartum low mood related to newborn care. | **Rest and mood:** sleeps 6 hours in 24 and reports good mood by day 10. | Cluster care and rest when the baby sleeps (restores energy); involve husband and mother-in-law; screen mood at each visit (finds depression early). | Rests; mood stable. |

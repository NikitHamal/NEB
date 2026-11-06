---
subject: Geriatric Nursing
grade: BSc Nursing Year 2
unit: 1
title: Ageing, Nepal's Older Population and Comprehensive Geriatric Assessment
hours: 8
area: BSN 11 · Geriatric Nursing · Unit 1
---

Nepal is getting older. The 2021 census counted about **2.97 million people aged 60 and above, 10.2% of 29.16 million Nepalis**, up from 8.1% in 2011, and the older group grows about four times faster than the whole population. The **Senior Citizens Act 2063 (2006)** defines a senior citizen as a person of **60 years or more**, the **Senior Citizens Regulations 2065 (2008)** put it into practice, and the **WHO Decade of Healthy Ageing 2021-2030** gives the global frame. Most older Nepalis live in rural hill and mountain homes, many still work in farming, many cannot read, and many have hypertension, diabetes, COPD, cataract or dementia without a diagnosis. Geriatric nursing is the care that keeps these people **independent, safe and dignified for as long as possible**. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of an older Nepali woman, a hand-grip dynamometer, a mature cataract and a behind-the-ear hearing aid, plus SVG figures on functional decline and the assessment domains.
- Ageing theories, eight systems of normal age-related change, comprehensive geriatric assessment (CGA), Katz and Barthel scores, gait speed, timed up-and-go and the Fried frailty phenotype.
- Eight points each on healthy-ageing teaching and communication with an older person.
- Model answers and a NANDA-I care plan for an older woman with weight loss and sensory loss.
:::

## 1.1 Who is "old", and why do we age?

Ageing is a **normal, gradual, universal loss of reserve** in every organ, not a disease. Gerontology (the study of ageing) separates the **young-old (60-74 years), old-old (75-84)** and **oldest-old (85+)**. Chronological age is a poor guide, so geriatric nurses think in terms of **function and frailty**. **Biological theories:** *programmed* (cells divide a limited number of times, the Hayflick limit, because telomeres shorten) and *damage* theories (free radicals, glycation of proteins, accumulated DNA errors). **Psychosocial theories:** *disengagement* (older people withdraw from roles), *activity* (staying active gives life satisfaction) and *continuity* (people keep their lifelong habits and roles). Erikson's last stage is **integrity versus despair**: looking back on life with acceptance or regret. Nepali families often fit the activity and continuity ideas, since grandparents still farm, mind children and keep ritual roles.

```python
import math
total, old, old2011 = 29.16, 2.97, 2.154       # millions: 2021 census, 60+ in 2021, 60+ in 2011
share = old / total * 100                       # % of the population aged 60+
rise = (old - old2011) / old2011 * 100          # rise in the number of older people over 10 years
r_old, r_all = 3.29, 0.92                       # % growth per year, 2011-2021 (60+ and all ages)
double = 70 / r_old                             # rule of 70: doubling time of the older group
t14 = math.log(14 / share) / math.log((1 + r_old / 100) / (1 + r_all / 100))
print(f"Share aged 60+ = {old} / {total} x 100 = {share:.1f}%")
print(f"Rise in the number aged 60+ over 10 years = {rise:.1f}%")
print(f"Doubling time at {r_old}% a year = 70 / {r_old} = {double:.1f} years")
print(f"Years until the share reaches 14% (aged society) at these two growth rates = {t14:.1f}")
```

```text
Share aged 60+ = 2.97 / 29.16 x 100 = 10.2%
Rise in the number aged 60+ over 10 years = 37.9%
Doubling time at 3.29% a year = 70 / 3.29 = 21.3 years
Years until the share reaches 14% (aged society) at these two growth rates = 13.7
```

The share of older people is **10.2%**, and the number of people aged 60+ rose **37.9%** in ten years. At 3.29% a year the older group would double in about **21.3 years** (rule of 70). If today's two growth rates simply continued, the share would reach 14% (an "aged society") in about **13.7 years**; official projections are later (about 2054) because growth slows, which shows why a straight-line forecast over-states the change and why planners use models.

```svgfig label="1.1" caption="Normal ageing is a slow loss of reserve, not a sudden failure. Illustrative curves from standard formulas, each shown as a percentage of its value at age 30: maximum heart rate (208 - 0.7 x age), creatinine clearance by the Cockcroft-Gault age term (140 - age) and FEV1 (about 20 mL lost per year from 3.5 L in a healthy non-smoker). A healthy older adult still functions at rest but has little reserve for illness, dehydration or a new drug."
f = Fig(760, 250)
f.line(60, 20, 60, 210, color=SLATE, sw=1.4); f.line(60, 210, 730, 210, color=SLATE, sw=1.4)
def X(a): return 60 + (a - 30) / 60 * 650
def Y(p): return 210 - (p - 40) / 60 * 190
for p in (50, 60, 70, 80, 90, 100):
    f.line(60, Y(p), 730, Y(p), color="#cbd5e1", sw=0.6); f.text(52, Y(p), str(p) + "%", size=10, anchor="end", vmid=True)
for a in (30, 40, 50, 60, 70, 80, 90):
    f.text(X(a), 226, str(a), size=10); f.line(X(a), 210, X(a), 214)
f.text(395, 244, "Age (years)", size=11, bold=True)
series = [("Max heart rate", lambda a: (208 - 0.7 * a) / (208 - 0.7 * 30) * 100, RED, 52),
          ("Creatinine clearance", lambda a: (140 - a) / 110 * 100, NAVY, 44),
          ("FEV1", lambda a: (3.5 - 0.02 * (a - 30)) / 3.5 * 100, TEAL, 38)]
for name, fn, col, ly in series:
    pts = [(X(a), Y(fn(a))) for a in range(30, 91, 5)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]): f.line(x1, y1, x2, y2, color=col, sw=2.6)
    f.text(X(90) - 4, Y(fn(90)) - 8, name, size=10.5, color=col, bold=True, anchor="end")
f.box(80, 28, 300, 36, "Reserve falls, resting function is kept", fill=SAND, stroke=AMBER, size=11, bold=True)
```

### Eight systems: normal age-related change and what the nurse does

1. **Cardiovascular.** Arteries stiffen, so systolic BP rises and the maximum heart rate falls. The heart fills more slowly and depends on a good atrial kick, so **atrial fibrillation** is poorly tolerated. Baroreceptors react slowly, which causes **orthostatic hypotension** and falls. Measure BP lying and after standing for 1-3 minutes.
2. **Respiratory.** The chest wall stiffens, alveoli lose elastic recoil and the cough is weaker, so vital capacity falls and the residual volume rises. The older person is at higher risk of **pneumonia**. Teach deep breathing, upright posture, vaccination and a smoke-free kitchen.
3. **Gastrointestinal.** Saliva, taste, gastric acid and gut movement decrease and teeth are lost. This causes poor appetite, constipation and poor absorption of iron and vitamin B12. Give small frequent meals, check dentures and keep fibre and fluids up.
4. **Renal and urinary.** Nephrons and renal blood flow fall, so the glomerular filtration rate drops about 1 mL/min a year after 40 even when serum creatinine looks normal. The bladder holds less, and the prostate enlarges in men. Drugs must be dosed by creatinine clearance, and nocturia needs a plan for safe night toileting.
5. **Neurological and sensory.** Reaction time slows, deep sleep shortens and the lens clouds (**cataract**), accommodation fails (**presbyopia**), high-pitch hearing is lost (**presbycusis**) and taste and smell dull. These changes cause isolation and accidents. Give good light, speak low and clearly, and treat cataract and wax.
6. **Musculoskeletal.** Muscle mass falls (**sarcopenia**), bone density falls, cartilage thins and posture stoops. Falls and fractures follow. Encourage weight-bearing exercise, protein, calcium and vitamin D.
7. **Skin.** The skin is thin, dry, wrinkled and slow to heal, with less fat and sweat. Bruises, tears and pressure injury come easily, and cold or heat is badly sensed. Moisturise, avoid hot water and friction, and inspect the skin daily.
8. **Endocrine, immune and thermoregulation.** Glucose tolerance falls, T-cell response weakens and fever may be absent in a serious infection. Hypothermia occurs in cold Himalayan winters. Look for confusion, a fall or poor appetite as the "atypical" signs of infection.

```photogrid label="1.2" cols="4" ratio="1.0" caption="Ageing in real people. (a) An older woman in a doorway in Bandipur: thin, dry, wrinkled skin and layered clothing against cold. (b) A real hand-grip dynamometer: grip strength is a quick test of sarcopenia and frailty. (c) A real mature cataract: the lens is milky, so the pupil is grey-white instead of black. (d) A real behind-the-ear hearing aid worn in the ear canal for presbycusis."
@ photo id="nur7/nep1" cap="Older woman, Bandipur"
fit 1.0
focus 0.5 0.0
mark 0.40 0.80 "1"
mark 0.50 0.35 "2"
key 1 (a) Face: thin, dry, lined skin; check hydration and sun damage
key 2 (a) Layered shawl: older people feel the cold late and lose heat quickly
@ photo id="nur7/grip" cap="Grip dynamometer"
fit 1.0
focus 0.5 0.3
mark 0.46 0.85 "3"
mark 0.30 0.47 "4"
key 3 (b) Dial: reads grip force in kg; best of three tries on the stronger hand
key 4 (b) Hand: elbow bent 90 degrees, arm unsupported; low grip means sarcopenia
@ photo id="nur7/cataract" cap="Mature cataract"
fit 1.0
focus 0.5 0.5
mark 0.50 0.45 "5"
mark 0.50 0.80 "6"
key 5 (c) Milky lens opacity: light cannot reach the retina, vision blurs and glare increases
key 6 (c) Iris: normally the pupil inside it is black; surgery with a lens implant restores sight
@ photo id="nur7/hearing" cap="Behind-the-ear hearing aid"
fit 1.0
focus 0.5 0.5
mark 0.70 0.55 "7"
mark 0.62 0.40 "8"
key 7 (d) Aid body and tube lie behind the ear: clean daily, switch off and remove at night
key 8 (d) Ear canal: remove wax first, since wax is a common reversible cause of deafness
```

## 1.2 Comprehensive geriatric assessment (CGA)

A **CGA** is a team assessment (doctor, nurse, physiotherapist, nutritionist, social worker) of the **medical, functional, cognitive, psychological, nutritional, social, environmental and medication** domains, ending in one written care plan. It is better than a routine check because older people hide problems, fear being called "weak" and put symptoms down to "age". In Nepal a nurse can run a basic CGA at a PHC, a geriatric ward, a senior citizens' home or a home visit by the ward FCHV and health post. Use a **tool for each domain** (Figure 1.3) and record the scores so that the next visit can be compared.

```svgfig label="1.3" caption="The domains of a comprehensive geriatric assessment, each with a simple bedside tool. Scores guide the plan; they do not replace listening to the patient and the family."
f = Fig(760, 250)
f.box(290, 100, 180, 50, "COMPREHENSIVE\nGERIATRIC\nASSESSMENT", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
cells = [(10, 14, "FUNCTION\nKatz ADL, Lawton IADL, Barthel", BLUE, NAVY), (260, 14, "MOBILITY AND FALLS\nTUG, gait speed, Morse", MINT, TEAL), (510, 14, "COGNITION\nMini-Cog, MoCA, CAM", SAND, AMBER),
         (10, 100, "MOOD\nGDS-15 (5 or more)", ROSE, RED), (510, 100, "NUTRITION\nMNA-SF, BMI, weight loss", MINT, TEAL),
         (10, 186, "MEDICINES\nBeers, STOPP/START, CrCl", BLUE, NAVY), (260, 186, "SOCIAL AND HOME\nCaregiver, money, safety", SAND, AMBER), (510, 186, "SENSES AND SKIN\nVision, hearing, Braden", ROSE, RED)]
for x, y, t, fl, st in cells:
    f.box(x, y, 240, 52, t, fill=fl, stroke=st, size=11, bold=True)
for x, y in [(250, 40), (510, 40)]: pass
f.arrow([(250, 125), (290, 125)], color=SLATE); f.arrow([(510, 125), (470, 125)], color=SLATE)
f.arrow([(130, 66), (130, 98)], color=SLATE); f.arrow([(130, 184), (130, 154)], color=SLATE)
f.arrow([(630, 66), (630, 98)], color=SLATE); f.arrow([(630, 184), (630, 154)], color=SLATE)
f.arrow([(380, 66), (380, 98)], color=SLATE); f.arrow([(380, 184), (380, 152)], color=SLATE)
```

**Function** is the single best predictor of an older person's future. The **Katz Index** scores six basic activities (bathing, dressing, toileting, transferring, continence, feeding), 1 point for each done independently: 6 is full function, 4 moderate impairment and 2 or less severe impairment. The **Barthel Index** (0-100) scores ten items, with 91-99 slight, 61-90 moderate, 21-60 severe and 0-20 total dependence. **Gait speed** over 4 metres below 0.8 m/s, a **timed up-and-go (TUG) of 12 seconds or more** and a weak grip all mark frailty and fall risk. The **Fried frailty phenotype** is present when 3 or more of 5 are found: unintentional weight loss, exhaustion, weakness (grip), slow gait and low activity (1-2 is pre-frail).

```python
katz = {"bathing": 0, "dressing": 1, "toileting": 1, "transferring": 1, "continence": 0, "feeding": 1}
barthel = [10, 0, 5, 5, 10, 5, 10, 10, 10, 5]   # feeding, bathing, grooming, dressing, bowels, bladder, toilet, transfer, mobility, stairs
dist, secs, tug = 4.0, 6.0, 14                  # 4-metre walk time, timed up-and-go (seconds)
speed = dist / secs
fried = {"weight loss": 0, "exhaustion": 1, "weak grip": 1, "slow gait": 1, "low activity": 1}
print(f"Katz = {sum(katz.values())} / 6 (moderate impairment is 3-4)")
print(f"Barthel = {sum(barthel)} / 100 (61-90 moderate dependence)")
print(f"Gait speed = {dist:.0f} m / {secs:.0f} s = {speed:.2f} m/s (below 0.8 is slow)")
print(f"TUG = {tug} s ({'at or above' if tug >= 12 else 'below'} the 12 s fall-risk cut-off)")
print(f"Fried criteria met = {sum(fried.values())} of 5 -> {'frail' if sum(fried.values()) >= 3 else 'pre-frail'}")
```

```text
Katz = 4 / 6 (moderate impairment is 3-4)
Barthel = 70 / 100 (61-90 moderate dependence)
Gait speed = 4 m / 6 s = 0.67 m/s (below 0.8 is slow)
TUG = 14 s (at or above the 12 s fall-risk cut-off)
Fried criteria met = 4 of 5 -> frail
```

Mr Ram Bahadur, 74 years, scores **Katz 4/6** (needs help with bathing and continence), **Barthel 70/100**, walks 4 m in 6 s (**0.67 m/s**, slow), has a **TUG of 14 s** and meets **4 of 5** Fried criteria, so he is **frail**. A frail patient needs a falls, nutrition and medicine review, not just a prescription.

### Healthy ageing: eight points of health education

1. **Eat enough protein and energy.** Older people need as much protein as the young, about 1.0-1.2 g/kg a day, but they eat less. Give dal, eggs, milk, curd, soya, fish and *dhindo* with gundruk in small frequent meals. Weigh the person monthly, because weight loss is the earliest sign of trouble.
2. **Keep moving every day.** Walking 30 minutes on most days, simple strength exercise with a water bottle and balance practice such as standing on one leg near a wall lower the risk of falls and keep muscle. Even sitting exercises help a person who cannot walk far. Exercise also lifts mood and sleep.
3. **Take vaccines and screening.** Influenza and pneumococcal vaccines are advised for older adults and for those with chronic disease (not part of the routine NIP child schedule, so ask the health facility). Tetanus (Td) after a wound, BP and blood sugar checks through the **PEN programme**, and VIA for cervical cancer in women are important screening steps.
4. **Check eyes, ears and teeth every year.** Cataract surgery at eye hospitals (Tilganga, Lumbini and others) restores sight, ear wax can be removed in minutes, and a hearing aid ends isolation. Good teeth or well-fitting dentures allow proper food. Do not accept "it is just age".
5. **Manage medicines safely.** Keep a single list of all drugs, including Ayurvedic and shop-bought ones, use a pill box, and never share medicines. Report dizziness, confusion or constipation, because these are common drug effects. Return to the doctor before stopping a drug.
6. **Stay connected.** Loneliness is as harmful as smoking. Encourage temple, mothers' group, senior citizen club and family meals, and phone calls from migrant children. Social contact protects the memory.
7. **Make the home safe.** Add light, remove loose rugs and thresholds, fit a grab bar and a firm stool in the bathroom, use non-slip footwear and keep the path to the toilet clear at night. Smoke from open fires harms the lungs, so use an improved stove or a chimney.
8. **Plan for the future.** Talk about who will give care, the Senior Citizens Act rights, the old-age allowance (about Rs 4,000 a month from age 70, and from 60 for Dalit citizens and those in the former Karnali districts; check the current rate with the ward office), wishes about treatment and a will. These talks reduce fear and conflict in the family.

### Communicating with an older person: eight points

1. **Greet and address with respect.** Use *Buwa*, *Aama*, *Baje*, *Bajai* or the title the person likes, never "dear" or the first name without permission. Introduce yourself and explain your role.
2. **Reduce noise and face the person.** Switch off the radio, sit at eye level and keep your face in the light so that lips can be read. Avoid shouting; a lower, slower voice carries better than a high loud one.
3. **Check the senses first.** Make sure glasses and hearing aids are on and clean. A confused answer may only mean the person did not hear.
4. **Use short sentences and one question at a time.** Pause for the answer, since the response takes longer. Do not finish the sentence for the person.
5. **Use the mother tongue.** Use an interpreter or a family member for Nepali, Newari, Gurung, Maithili and other languages, but keep the person at the centre. Do not talk about the patient as if absent.
6. **Touch with permission.** A hand on the forearm calms many people, but ask first, and respect norms about touch from the opposite sex.
7. **Give time and written reminders.** Write large-print notes and a picture medicine chart for those who read little. Use teach-back: "Please show me how you will take the tablet."
8. **Listen to the life story.** Reminiscence builds integrity, reveals fears about money, loneliness or death and often reveals abuse or neglect. Allow time and privacy.

## Formula and fact sheet

- Share aged 60+ = old ÷ total × 100 (2021 census: 2.97 ÷ 29.16 = 10.2%); doubling time = 70 ÷ growth rate (%).
- Katz 6 = independent, 4 = moderate, 2 or less = severe; Barthel 91-99 slight, 61-90 moderate, 21-60 severe, 0-20 total dependence.
- Gait speed = distance ÷ time (below 0.8 m/s slow); TUG 12 s or more = fall risk; Fried 3 or more of 5 = frail.
- Cockcroft-Gault: (140 − age) × weight ÷ (72 × creatinine), × 0.85 for women. Energy about 30 kcal/kg and protein 1.0-1.2 g/kg for the frail.

## Chapter summary

- Nepal is ageing fast (10.2% aged 60+); the Senior Citizens Act 2063 defines 60 years as senior.
- Normal ageing lowers reserve in every system; illness shows in atypical ways, such as a fall, confusion or poor appetite.
- CGA covers function, mobility, cognition, mood, nutrition, medicines, social and sensory domains, each with a bedside tool.
- Good communication, sensory aids, nutrition, activity and a safe home are the heart of geriatric nursing.

## Practice

```python
total, old = 29.16, 2.97
m1 = old / total * 100
m2 = 4 / 8                                     # 4 m in 8 s
m3 = (140 - 80) * 60 / (72 * 1.2)              # man, 80 y, 60 kg, creatinine 1.2
w0, w1, ht = 52, 46, 1.50                      # Mrs Maya: weight 6 months ago, now, height (m)
c_loss = (w0 - w1) / w0 * 100
c_bmi = w1 / ht ** 2
c_crcl = (140 - 78) * w1 / (72 * 1.1) * 0.85
c_gait = 4 / 7
c_kcal, c_prot = 30 * w1, 1.2 * w1
print(f"MCQ1 share = {m1:.1f}%; MCQ2 gait speed = {m2:.2f} m/s; MCQ3 CrCl = {m3:.1f} mL/min")
print(f"Mrs Maya: weight loss = {w0 - w1} kg = {c_loss:.1f}% in 6 months; BMI = {c_bmi:.1f}")
print(f"Mrs Maya: CrCl = (140 - 78) x {w1} / (72 x 1.1) x 0.85 = {c_crcl:.1f} mL/min; gait speed = {c_gait:.2f} m/s")
print(f"Mrs Maya: energy 30 kcal/kg = {c_kcal:,} kcal; protein 1.2 g/kg = {c_prot:.0f} g")
```

```text
MCQ1 share = 10.2%; MCQ2 gait speed = 0.50 m/s; MCQ3 CrCl = 41.7 mL/min
Mrs Maya: weight loss = 6 kg = 11.5% in 6 months; BMI = 20.4
Mrs Maya: CrCl = (140 - 78) x 46 / (72 x 1.1) x 0.85 = 30.6 mL/min; gait speed = 0.57 m/s
Mrs Maya: energy 30 kcal/kg = 1,380 kcal; protein 1.2 g/kg = 55 g
```

**MCQs (with reasons)**

1. In the 2021 census Nepal had 2.97 million people aged 60+ among 29.16 million. The share of older people is: (a) 1.0% (b) 10.2% (c) 20.4% (d) 102%.
2. A patient takes 8 seconds to walk 4 metres. Her gait speed is: (a) 0.25 m/s (b) 0.50 m/s (c) 2.0 m/s (d) 32 m/s.
3. An 80-year-old man weighs 60 kg and has a serum creatinine of 1.2 mg/dL. His Cockcroft-Gault creatinine clearance is about: (a) 0.7 (b) 41.7 (c) 60 (d) 100 mL/min.
4. The best single predictor of an older person's future independence is: (a) chronological age (b) function (c) serum cholesterol (d) number of children.
5. An 82-year-old woman is newly confused and refuses food, with no fever. The most likely explanation to exclude first is: (a) normal ageing (b) infection, such as urinary tract infection or pneumonia, with an atypical presentation (c) laziness (d) vitamin C excess.

::: note Answers and rationales
**1. (b).** 2.97 ÷ 29.16 × 100 = 10.2%; 1.0% is a decimal slip and 20.4% doubles it.
**2. (b).** 4 ÷ 8 = 0.50 m/s, below the 0.8 cut-off; 0.25 inverts the division and 2.0 multiplies the numbers wrongly.
**3. (b).** (140 − 80) × 60 ÷ (72 × 1.2) = 41.7 mL/min; 0.7 leaves out the weight and 100 ignores age.
**4. (b).** Function (ADL, gait speed, grip) predicts disability, hospital stay and death better than age alone; the other options have no direct link.
**5. (b).** New confusion is delirium until proved otherwise, and infection often has no fever in the old; normal ageing never causes sudden confusion.
:::

**Short answer (3 marks): Comprehensive geriatric assessment.** CGA is a multidimensional, team-based assessment of an older person's medical, functional, cognitive, psychological, nutritional, social, environmental and medication status, which ends in one coordinated care plan. It uses standard tools: Katz and Barthel for function, TUG and gait speed for mobility, Mini-Cog for cognition, GDS-15 for mood and MNA-SF for nutrition. It reduces hospital admission and improves independence compared with usual care.

**Medium answer (5 marks): Describe the assessment of frailty (Figure 1.3).** *Meaning:* frailty is a state of lost reserve that makes a small stressor (infection, a new drug, a fall) lead to disability. *Fried phenotype:* three or more of unintentional weight loss, exhaustion, weak grip, slow gait (under 0.8 m/s) and low activity. *Measures:* grip dynamometer, 4-metre gait speed, TUG (12 s or more) and the Clinical Frailty Scale. *Nurse's role:* weigh the patient, observe walking, ask about tiredness and activity, review medicines and nutrition, check mood and cognition and involve the family. *Management:* resistance exercise, protein 1.0-1.2 g/kg, treat reversible causes (anaemia, thyroid disease, depression), review polypharmacy and plan care at home.

**Long answer (10 marks): Mrs Maya Devi Gurung, 78 years, a widow from Bandipur living alone, is brought by a neighbour to the geriatric outpatient clinic of a district hospital. She has lost weight from 52 kg to 46 kg in 6 months (height 150 cm), eats one meal a day and feels tired. Both eyes are blurred (cataract), she mishears questions, her TUG is 16 seconds and she walked 4 m in 7 seconds. Serum creatinine is 1.1 mg/dL. Her daughter works abroad. Calculate and write the nursing care plan.**

*Calculations.* Weight loss is 6 kg ÷ 52 × 100 = **11.5%** in 6 months (over 5% is significant). BMI is 46 ÷ 1.5² = **20.4 kg/m²**. Her Cockcroft-Gault clearance is **30.6 mL/min**, although the creatinine of 1.1 looks normal, because her muscle mass is small; so drug doses must be reduced. Gait speed is 4 ÷ 7 = **0.57 m/s** (slow) and TUG 16 s (over 12 s) shows a high fall risk. Her energy need is 30 × 46 = **1,380 kcal** and protein 1.2 × 46 = **55 g** a day. She meets Fried criteria for weight loss, exhaustion, slow gait and probably weak grip, so she is **frail**.

*Care.* Do a full CGA with the team. Check for reversible causes of weight loss: depression (GDS-15), dental problems, anaemia, thyroid disease, TB (cough, fever, sputum for AFB at the DOTS centre), diabetes and cancer. Weigh monthly and give three meals and two snacks with protein at each, using locally available foods (dal, eggs, milk, soya, green leaves); offer a fortified flour such as *sarbottam pitho* or lito. Refer her for cataract surgery and ear wax removal, and for a hearing assessment. Teach the use of a stick or frame, remove home hazards and begin a chair-stand and balance programme with a physiotherapist. Link her with the ward office for the old-age allowance, a health post FCHV home visit, a neighbour as a daily contact and a phone call arrangement with her daughter. Review in 2 weeks and then monthly.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I eat one meal a day, I feel weak." **O:** 52 → 46 kg, BMI 20.4, loss 11.5% in 6 months. | **Imbalanced nutrition: less than body requirements** related to living alone, poor vision and low appetite, as evidenced by weight loss and BMI 20.4. | **Nutritional status:** weight gain of 1 kg in 4 weeks; eats 3 meals and 2 snacks daily. | Nutrition counselling and food diary (finds the gaps); 1,380 kcal and 55 g protein plan (meets needs); weekly weight; treat dental or mood causes; link with neighbour for meals (shared meals raise intake). | Weight 47 kg at 4 weeks; eats three meals; BMI rising. |
| **S:** "I cannot see the steps well." **O:** TUG 16 s, gait 0.57 m/s, cataract. | **Risk for falls** related to impaired vision, slow gait and weak muscles. | **Fall prevention behaviour:** no falls over 3 months; TUG under 12 s. | Home hazard check and lighting (the commonest causes); stick or frame teaching; chair-stand and balance exercise (builds strength); cataract surgery referral (restores vision); footwear advice. | No falls; TUG 12 s at 3 months; surgery done. |
| **S:** "People mumble, I cannot follow." **O:** hears poorly; blurred vision. | **Disturbed sensory perception (visual and auditory)** related to cataract and presbycusis. | **Sensory function:** can answer questions correctly; vision and hearing improved. | Remove ear wax and test hearing (reversible cause); face the patient and speak slowly (improves understanding); refer for cataract surgery and hearing aid (restores function); large-print medicine chart. | Hears questions at normal voice; surgery done. |
| **S:** "My daughter is abroad; I am alone." **O:** lives alone, no visitors. | **Social isolation** related to bereavement, distance from family and sensory loss. | **Social involvement:** takes part in a group activity twice a week. | Link with the senior citizens' group and temple (company protects mood); weekly FCHV visit (early detection); regular calls with her daughter (family bond); screen mood with GDS-15 (finds depression). | Attends group; GDS under 5. |

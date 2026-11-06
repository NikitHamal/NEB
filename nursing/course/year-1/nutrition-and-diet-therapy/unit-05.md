---
subject: Nutrition and Diet Therapy
grade: BSc Nursing Year 1
unit: 5
title: Enteral and Parenteral Nutrition, Refeeding, Food Safety and Nutrition Education
hours: 12
area: BSN 8 · Nutrition and Diet Therapy · Unit 5
---

When a patient cannot eat enough by mouth, the nurse becomes the one who delivers the nutrition: through a tube into the gut (**enteral nutrition**) or directly into a vein (**parenteral nutrition**). Stroke, head injury, oesophageal cancer, burns, coma, severe malnutrition and bowel surgery fill the wards of Bir, TUTH, Patan and BPKIHS with patients in this group. The rule is a short one: **"if the gut works, use it."** Enteral feeding is safer, cheaper, preserves the gut barrier and is the first choice; the vein is used only when the gut cannot be used. This unit gives the indications, volumes, rates and nursing safety checks, then ends with refeeding syndrome, food safety and nutrition education, with all arithmetic checked by program.

::: key What this unit gives you
- Real photographs of an enteral feeding pump, an open-system feeding set with its tubing, and a parenteral nutrition bag, plus a route-selection algorithm.
- Enteral formula, rate and free-water arithmetic; the NG tube steps and placement checks; the eight complications.
- Parenteral composition from energy, protein and lipid, the glucose infusion rate, osmolarity and nitrogen balance.
- Refeeding syndrome, food safety and nutrition education in Nepal, and eight points on the nurse's role, with model answers and a care plan for an NG-fed stroke patient.
:::

## 5.1 Enteral nutrition: feeding through the gut

**Indications:** a working gut but inadequate oral intake: stroke or swallowing disorder (dysphagia), unconsciousness, head and neck cancer, severe burns, severe malnutrition, anorexia in chronic illness and after upper-gut surgery. **Contraindications** are intestinal obstruction, ileus, severe haemorrhage, high-output fistula, severe vomiting not controlled and shock. The **route** is chosen by the expected time and the risk of aspiration: a **nasogastric (NG) tube** for under 4-6 weeks, a **nasojejunal tube** if gastric emptying is poor or aspiration risk is high, and a **gastrostomy (PEG)** or jejunostomy for longer. **Formulas** are **polymeric** (whole protein, standard 1 kcal/mL, about 40 g protein per litre), **energy-dense** (1.5-2 kcal/mL), **elemental** (amino acids, for malabsorption) and in Nepal often **blenderised home-made feeds** of rice, dal, milk, egg, oil and vegetables sieved to pass the tube, given the same day and kept clean. **Methods** are bolus, intermittent and continuous pump feeding.

**Inserting and checking an NG tube.** Wash hands, explain, sit the patient up. Measure **NEX** (the distance from the tip of the **N**ose to the **E**ar lobe and then to the **X**iphoid process) and mark it. Lubricate, pass along the floor of the nose, ask the patient to swallow sips of water and advance to the mark. **Never trust the sound of air** to prove placement. The accepted checks are **aspirate with a pH of 5.5 or less** with pH paper (or X-ray where the aspirate is not clear), and the mark at the nostril unchanged. Tape the tube, keep the head of the bed **raised 30-45°** during and for one hour after feeding. **Flush with 30 mL water** before and after each feed and each medicine, give drugs separately in liquid form and never crush slow-release tablets.

```python
kcal_goal, w = 1800, 60               # target kcal/day, kg
vol = kcal_goal / 1.0                 # formula 1 kcal/mL
print(f"Volume = {kcal_goal} kcal / 1 kcal per mL = {vol:.0f} mL/day")
print(f"Continuous 24 h = {vol/24:.0f} mL/h; over 20 h = {vol/20:.0f} mL/h; bolus 6 feeds = {vol/6:.0f} mL per feed")
protein = vol / 1000 * 40
print(f"Protein at 40 g/L = {protein:.0f} g/day = {protein/w:.1f} g/kg")
free = vol * 0.85
need = 30 * w
print(f"Free water in formula (85%) = {free:.0f} mL; need 30 mL/kg = {need} mL; flush = {need - free:.0f} mL/day")
print(f"Start 25 mL/h and raise 25 mL/h every 8 h: 25, 50, 75 mL/h reached at hour {2*8}")
print(f"Energy-dense 1.5 kcal/mL: {kcal_goal/1.5:.0f} mL/day = {kcal_goal/1.5/24:.0f} mL/h")
```

```text
Volume = 1800 kcal / 1 kcal per mL = 1800 mL/day
Continuous 24 h = 75 mL/h; over 20 h = 90 mL/h; bolus 6 feeds = 300 mL per feed
Protein at 40 g/L = 72 g/day = 1.2 g/kg
Free water in formula (85%) = 1530 mL; need 30 mL/kg = 1800 mL; flush = 270 mL/day
Start 25 mL/h and raise 25 mL/h every 8 h: 25, 50, 75 mL/h reached at hour 16
Energy-dense 1.5 kcal/mL: 1200 mL/day = 50 mL/h
```

A 60-kg patient with a target of 1,800 kcal needs **1,800 mL a day of a 1 kcal/mL formula**, which is **75 mL/h** for 24 hours (or 90 mL/h over 20 hours, or 300 mL in each of six bolus feeds). The formula supplies **72 g protein (1.2 g/kg)** and 1,530 mL of water, so the patient also needs **270 mL** of free water each day as flushes. Feeding is started at 25 mL/h and increased by 25 mL/h every 8 hours, reaching the goal rate in 16 hours. The 1.5 kcal/mL formula gives the same energy in 1,200 mL.

```photogrid label="5.1" cols="4" ratio="1.0" caption="Tube-feeding equipment. (a) A real enteral feeding pump with its display: the nurse sets the rate in mL/h and the pump alarms for a blocked tube. (b) The same set seen as an open-system feeding bag with its tubing coiled beside the pump. (c) A real parenteral nutrition bag: a multi-chamber bag in its protective overwrap, with the chambers that are mixed before use. (d) The route-selection algorithm."
@ photo id="nur4/pumps" cap="Enteral feeding pump"
fit 1.0
focus 0.5 0.45
mark 0.50 0.45 "1"
mark 0.50 0.78 "2"
key 1 (a) The pump display: rate (mL/h) and volume to be infused (VTBI)
key 2 (a) The pump housing: the feeding-set cassette clips here
@ photo id="nur4/openent" cap="Open-system set"
fit 1.0
focus 0.5 0.45
mark 0.28 0.45 "3"
mark 0.72 0.45 "4"
key 3 (b) The feed bag and its giving set: hang it, prime the line, label it with time
key 4 (b) The pump and the purple tube connectors: connect only to an enteral port
@ photo id="nur4/pn" cap="Parenteral nutrition bag"
fit 1.0
focus 0.5 0.5
mark 0.45 0.25 "5"
mark 0.60 0.80 "6"
key 5 (c) The bag chambers (dextrose, amino acids, lipid) are mixed by breaking the seals
key 6 (c) The port and hanger area of the bag
@ svg cap="Which route?"
f = Fig(300, 300)
f.box(60, 6, 180, 46, "Can he eat?", fill=BLUE, stroke=NAVY, size=16, bold=True)
f.box(6, 84, 138, 52, "Yes: oral diet", fill=MINT, stroke=TEAL, size=14, bold=True)
f.box(156, 84, 138, 52, "No: gut works?", fill=SAND, stroke=AMBER, size=14, bold=True)
f.box(6, 176, 138, 70, "Yes: enteral\nNG or PEG", fill=MINT, stroke=TEAL, size=14, bold=True)
f.box(156, 176, 138, 70, "No: parenteral\ncentral line", fill=ROSE, stroke=RED, size=14, bold=True)
f.arrow([(110, 52), (75, 84)], sw=1.8); f.arrow([(190, 52), (225, 84)], sw=1.8)
f.arrow([(200, 136), (75, 176)], sw=1.8, color=TEAL); f.arrow([(250, 136), (225, 176)], sw=1.8, color=RED)
f.text(150, 276, "If the gut works, use it", size=14, color=NAVY, bold=True)
```

**Complications of tube feeding** and the nurse's action: (1) **aspiration pneumonia** (keep head up 30-45°, stop if cough or vomit, check placement); (2) **tube blockage** (flush with warm water, never use a wire); (3) **diarrhoea** (check formula contamination, rate and antibiotics; do not stop feeding without advice); (4) **nausea and distension** (slow the rate); (5) **tube displacement** (mark and tape; recheck before each use); (6) **nasal and skin injury** (change the side and clean daily); (7) **dehydration and electrolyte imbalance** (flush, weigh, record fluids); (8) **refeeding syndrome** (see 5.3).

## 5.2 Parenteral nutrition: feeding through a vein

**Parenteral nutrition (PN)** gives all nutrients intravenously when the gut cannot be used for more than 5-7 days: intestinal obstruction, short bowel, severe pancreatitis, high-output fistula, major bowel surgery or severe malabsorption. **Peripheral PN** uses a vein in the arm and solutions of osmolarity **up to about 900 mOsm/L** for under 2 weeks. **Central PN** uses a catheter whose tip lies in the superior vena cava, for stronger solutions. Energy values are **dextrose 3.4 kcal/g, amino acids 4 kcal/g and 20% lipid emulsion 2 kcal/mL**. A 3-in-1 bag holds all three, with electrolytes, vitamins and trace elements added by pharmacy.

```python
w = 60
energy = 25 * w
prot_g = 1.2 * w
prot_kcal = prot_g * 4
lip_kcal = 0.30 * energy
lip_ml = lip_kcal / 2
dex_kcal = energy - prot_kcal - lip_kcal
dex_g = dex_kcal / 3.4
print(f"Energy {energy} kcal: protein {prot_g:.0f} g = {prot_kcal:.0f} kcal; lipid 30% = {lip_kcal:.0f} kcal = {lip_ml:.0f} mL of 20%; dextrose = {dex_kcal:.0f} kcal = {dex_g:.0f} g")
gir = dex_g * 1000 / w / 1440
print(f"Glucose infusion rate = {gir:.2f} mg/kg/min (keep below 4-5)")
osm = (dex_g * 5 + prot_g * 10) / 1.5
print(f"Osmolarity of 1.5 L (without lipid) = {osm:,.0f} mOsm/L: central vein needed")
print(f"Rate over 24 h = {1500/24:.1f} mL/h")
nin = prot_g / 6.25
nout = 10 + 4
print(f"Nitrogen in = {prot_g:.0f}/6.25 = {nin:.2f} g; out = 10 + 4 = {nout} g; balance = {nin - nout:.2f} g")
print(f"Refeeding start 10 kcal/kg for 40 kg = {10*40} kcal; extreme risk 5 kcal/kg = {5*40} kcal")
```

```text
Energy 1500 kcal: protein 72 g = 288 kcal; lipid 30% = 450 kcal = 225 mL of 20%; dextrose = 762 kcal = 224 g
Glucose infusion rate = 2.59 mg/kg/min (keep below 4-5)
Osmolarity of 1.5 L (without lipid) = 1,227 mOsm/L: central vein needed
Rate over 24 h = 62.5 mL/h
Nitrogen in = 72/6.25 = 11.52 g; out = 10 + 4 = 14 g; balance = -2.48 g
Refeeding start 10 kcal/kg for 40 kg = 400 kcal; extreme risk 5 kcal/kg = 200 kcal
```

For a 60-kg patient, the PN is made from 25 kcal/kg (**1,500 kcal**): protein 1.2 g/kg gives **72 g (288 kcal)**, lipid 30% gives **225 mL of 20% emulsion**, and the rest, **224 g of dextrose**, supplies the balance. The **glucose infusion rate** is 2.59 mg/kg/min, within the safe limit. The osmolarity of the 1.5-L bag without lipid is about **1,227 mOsm/L**, far above the peripheral limit, so a central line is needed. The 24-hour rate is **62.5 mL/h**. **Nitrogen balance** = protein ÷ 6.25 minus (urinary urea nitrogen + 4 g for skin and stool losses): with 72 g protein and a urinary urea nitrogen of 10 g, 11.52 − 14 = **-2.48 g**, a negative balance that tells the team to review the protein and energy supply.

```svgfig label="5.1" caption="Composition of a 1,500-kcal parenteral nutrition regimen for a 60-kg adult. Dextrose supplies about half the energy, lipid 30% and amino acids 19%, with electrolytes, vitamins and trace elements added; the three-in-one bag is given by pump through a central line over 24 hours."
f = Fig(760, 200)
tot = 1500
parts = [("Dextrose 762 kcal\n224 g", 762, BLUE, NAVY), ("Lipid 450 kcal\n225 mL 20%", 450, SAND, AMBER), ("Amino acids\n288 kcal, 72 g", 288, MINT, TEAL)]
x = 20
for t_, k_, fc, sc in parts:
    wd = 720 * k_ / tot
    f.box(x, 40, wd, 70, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    x += wd
f.text(380, 24, "Energy 1,500 kcal = 25 kcal/kg x 60 kg", size=12, color=NAVY, bold=True)
f.text(20, 138, "Added: Na, K, Mg, PO4, Ca, vitamins, trace elements", size=11, color=SLATE, bold=True, anchor="start")
f.text(20, 160, "Central line, aseptic technique, 24-hour hang time, pump rate 62.5 mL/h", size=11, color=TEAL, bold=True, anchor="start")
f.text(20, 182, "Check glucose every 6 h at start; do not stop abruptly (rebound hypoglycaemia)", size=11, color=RED, bold=True, anchor="start")
```

**Complications of PN** and care: (1) **catheter-related bloodstream infection** (aseptic dressing and hub care, a dedicated lumen, nothing else through it); (2) **hyperglycaemia** (glucose checks, insulin as ordered); (3) **hypoglycaemia** on sudden stopping (taper, or run 10% dextrose); (4) **refeeding syndrome**; (5) **fluid overload and electrolyte disturbance** (daily weight, intake-output, daily then weekly blood tests); (6) **pneumothorax, air embolism and thrombosis** from the central line (X-ray before use, clamp and head-down position if the line is open); (7) **liver dysfunction and gall stones** (use the gut when possible, cycle the feed); (8) **bag contamination or precipitation** (inspect for cloudiness, label, 24-hour hang time, lipid line changed in 24 hours).

## 5.3 Refeeding syndrome

When a starved patient is fed fast, insulin rises, and **phosphate, potassium and magnesium move into the cells** and the thiamine requirement jumps. The result is **hypophosphataemia, hypokalaemia, hypomagnesaemia, fluid retention, arrhythmia, heart failure, seizures and confusion** within days. **High-risk patients** have a BMI below 16, a weight loss above 15% in 3-6 months, little or no intake for over 10 days, or low electrolytes before feeding; many of them are the older, alcohol-using, cancer, malnourished and post-operative patients on a Nepali ward. The NICE guideline advises: **start at 10 kcal/kg/day (5 kcal/kg in extreme cases)**, increase over 4-7 days, **give thiamine and a vitamin mix before and during the first 10 days**, correct electrolytes and monitor phosphate, potassium and magnesium daily at first. A 40-kg patient starts at **400 kcal** (or 200 kcal in extreme risk).

## 5.4 Food safety, adulteration and nutrition education in Nepal

**Food safety.** Food-borne illness (diarrhoea, typhoid, hepatitis A, cholera) follows contaminated food and water. The WHO **Five Keys to Safer Food** are: **keep clean** (wash hands and surfaces), **separate raw and cooked**, **cook thoroughly** (to 70 °C), **keep food at safe temperature** (below 5 °C or above 60 °C; not more than 2 hours in the danger zone) and **use safe water and raw materials**. In Nepal the Food Act 2023 BS (1966) and the Department of Food Technology and Quality Control (DFTQC) regulate quality and **adulteration** (water in milk, colour in turmeric, lead chromate, artificial colours in sweets and pickles, unsafe pesticide residues on vegetables). Consumers should wash and peel vegetables, boil milk, buy packed iodised salt, read dates and avoid street food in poor hygiene.

**Nutrition education** is planned by the same steps as any health education: assess need, set one clear message, choose the method (demonstration, flip chart, plate model, home-garden, FCHV talk, radio), involve the community and evaluate by what people do. Nepal's national nutrition programmes include **MSNP-III (2023-2030)**, **IMAM** for acute malnutrition, **Baal Vita** for children 6-23 months, **vitamin A**, **IFA** and **calcium** for mothers, **universal salt iodisation** and **school meal and weekly iron programmes**, all reported through HMIS and DHIS2.

## 5.5 The nurse's role in enteral and parenteral nutrition: eight points

1. **Assess the need and the risk.** Know why the patient is fed by tube or vein, the expected duration and the risk of aspiration or refeeding. Check weight, BMI and electrolytes before the start. Report high-risk patients so that the doctor starts slowly and gives thiamine.
2. **Insert and check the tube safely.** Measure NEX, insert gently and confirm the position by pH 5.5 or less or X-ray before the first feed, and recheck before each use. Never rely on listening to air. A wrongly placed tube in the lung can kill.
3. **Position the patient and prevent aspiration.** Raise the head of the bed 30-45° during feeding and for one hour after. Stop the feed for coughing, vomiting, distension or breathlessness and tell the doctor. Keep the oral care routine, since bacteria in the mouth are aspirated too.
4. **Prepare and give feeds hygienically.** Wash hands, check formula name, date and expiry, label open feeds, and discard after 4 hours (hang time) for open home-made feeds and 24 hours for closed sets. Flush with 30 mL water before and after. Contaminated feeds cause diarrhoea and infection.
5. **Run the pump and calculate the rate.** Use the correct formula and rate in mL/h, begin slowly and increase as ordered. Check the pump alarm and the volume infused every shift. Record the volume actually given, not only the volume ordered.
6. **Care for the central line.** Use full aseptic technique, a dedicated lumen, a transparent dressing changed on schedule, and a new set every 24 hours for lipid. Look for redness, fever and swelling. Never take blood or give drugs through the PN lumen.
7. **Monitor and record.** Weigh, measure intake and output, check glucose (PN every 6 hours at first), and follow electrolytes, phosphate and liver tests. Record bowel and stool, residual volumes if ordered and tolerance. Early signs of trouble are better caught on the chart than at the bedside.
8. **Teach and plan for discharge.** Teach the family tube care, feed preparation from kitchen foods, flushing, positioning and warning signs, with return demonstration. Link them to the nearest health facility for tube changes and weight checks. A trained family keeps the patient out of hospital.

## Formula and fact sheet

- NEX = nose to ear to xiphoid. Placement: aspirate pH 5.5 or less or X-ray; head up 30-45°; flush 30 mL.
- Enteral volume = kcal ÷ kcal per mL; rate = volume ÷ hours; free water = need − 85% of formula volume.
- PN: dextrose 3.4, amino acids 4 kcal/g, 20% lipid 2 kcal/mL; GIR = g × 1000 ÷ kg ÷ 1440; peripheral limit about 900 mOsm/L.
- Nitrogen balance = protein ÷ 6.25 − (UUN + 4). Refeeding: 10 kcal/kg start (5 in extreme), thiamine first.
- Five keys to safer food; MSNP-III 2023-2030; IMAM; Baal Vita; DFTQC.

## Chapter summary

- If the gut works use it: NG tube for under 4-6 weeks, PEG for longer; the vein only if the gut cannot be used.
- Rate, volume and free water are calculated from energy and weight; placement is checked by pH or X-ray.
- PN is built from energy, protein and lipid, is given centrally if the osmolarity is high, and needs strict asepsis and monitoring.
- Refeeding syndrome is prevented by a slow start and thiamine; food safety and nutrition education complete the nurse's role.

## Practice

**MCQs (with reasons)**

1. A patient needs 2,000 kcal from a 1 kcal/mL formula over 20 hours; the rate is: (a) 80 mL/h (b) 83 mL/h (c) 100 mL/h (d) 120 mL/h.
2. 250 mL of 20% lipid emulsion supplies: (a) 250 kcal (b) 500 kcal (c) 1,000 kcal (d) 2,250 kcal.
3. 200 g of dextrose supplies: (a) 200 kcal (b) 400 kcal (c) 680 kcal (d) 1,800 kcal.
4. A 50-kg patient at high risk of refeeding syndrome should begin at about: (a) 10 kcal/kg = 500 kcal (b) 25 kcal/kg = 1,250 kcal (c) 35 kcal/kg = 1,750 kcal (d) full feeds.
5. The most reliable bedside check of NG tube position is: (a) listening for air over the stomach (b) aspirate pH 5.5 or less (c) water flowing in easily (d) the patient being able to talk.

::: note Answers and rationales
**1. (c).** 2,000 mL ÷ 20 h = 100 mL/h; 83 mL/h is 2,000 over 24 hours, an error that under-delivers.
**2. (b).** 20% emulsion gives 2 kcal/mL, so 250 × 2 = 500 kcal; the 20% figure is the concentration, not the calories.
**3. (c).** Dextrose gives 3.4 kcal/g: 200 × 3.4 = 680 kcal, not 4 kcal/g.
**4. (a).** Refeeding risk requires 10 kcal/kg (or less), so 50 × 10 = 500 kcal at first, with thiamine; full feeding may cause fatal hypophosphataemia.
**5. (b).** A gastric aspirate pH of 5.5 or less (or X-ray) is the accepted check; sound of air and ease of flushing can occur with the tube in the lung.
:::

**Short answer (3 marks): Refeeding syndrome.** It is a set of fluid and electrolyte shifts after feeding a starved person: insulin drives phosphate, potassium and magnesium into cells and the thiamine need rises. It causes hypophosphataemia, hypokalaemia, arrhythmia, heart failure, oedema and seizures. It is prevented by starting at 10 kcal/kg a day, giving thiamine before feeding and checking electrolytes daily.

**Medium answer (5 marks): Describe the nursing care of a patient on NG tube feeding (Figure 5.1d).** Choose the tube route only when the gut works. Before use confirm placement by aspirate pH of 5.5 or less or X-ray, and check the mark at the nostril every shift. Sit the patient up 30-45° during and for an hour after feeding, give the correct formula at the ordered rate, flush with 30 mL water before and after each feed and each drug, and discard open feeds after the hang time. Give oral and nasal care daily and fix the tube. Record the volume, tolerance, weight, bowel and fluid balance and watch for aspiration, diarrhoea and blockage. Teach the family for home care.

**Long answer (10 marks): Mr Dhan Bahadur Gurung, 68 years, 60 kg, is admitted with a left-sided stroke. He is drowsy (GCS 10), cannot swallow safely and an NG tube is passed. The doctor orders 1,800 kcal a day by continuous feed with a 1 kcal/mL formula. Plan the feed and the nursing care.**

*Calculations.* Volume = 1,800 ÷ 1 = **1,800 mL a day**, so the goal rate is 1,800 ÷ 24 = **75 mL/h**. Start at 25 mL/h and raise 25 mL/h every 8 hours (25, 50, 75), so on the first day he receives 25 × 8 + 50 × 8 + 75 × 8 = **1,200 mL (1,200 kcal)**, then the full 1,800 mL from day 2. The formula gives 72 g protein (1.2 g/kg), and free water of 30 mL/kg × 60 kg = 1,800 mL less 1,530 mL in the formula leaves **270 mL** to be given as flushes (about 30 mL every 2 hours plus the drug flushes).

*Care.* Check placement by pH of 5.5 or less before the first feed, tape the tube at the nostril and mark the exit point. Keep the head of the bed at 30-45°, stop the feed and call the doctor for coughing, vomiting or breathlessness. Give mouth care four times a day, change the nostril and tape daily, wash hands and label the feed with time. Record the volume, weigh twice a week, observe stools and give drugs separately in liquid form with flushes. A speech and swallow assessment is arranged as he recovers and oral trials begin only after it. Teach the daughter to prepare a blended home-made feed (rice, dal, milk, egg, oil) in clean utensils, to flush and position, and to bring him back if the tube moves.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** GCS 10, impaired swallow, NG tube in place. | **Risk for aspiration** related to impaired swallowing and reduced consciousness. | **Aspiration control:** no cough, vomiting or chest signs during feeding. | 1. Head of bed 30-45°; *gravity reduces reflux.* 2. Check tube position before use; *a displaced tube can cause lung feeding.* 3. Stop for vomiting or cough; *prevents pneumonia.* | No aspiration during the stay; chest clear. |
| **O:** no oral intake for 2 days, 60 kg. | **Imbalanced nutrition: less than body requirements** related to inability to swallow, as evidenced by no oral intake. | **Nutritional status:** 1,800 mL feed and 75 mL/h reached by day 2. | 1. Start at 25 mL/h and raise 25 mL/h every 8 h; *gradual increase prevents intolerance.* 2. Flush with 270 mL water daily; *meets free-water needs.* 3. Weigh twice a week; *monitors response.* | Full feed by day 2; weight within 1 kg at week 1. |
| **S:** daughter: "I do not know how to feed him." | **Deficient knowledge (caregiver)** related to lack of exposure to tube feeding. | **Knowledge: caregiver:** performs tube feeding correctly with return demonstration before discharge. | 1. Demonstrate blended feed, flush and positioning; *return demonstration confirms skill.* 2. Give a written list of danger signs in Nepali; *quick help.* 3. Arrange follow-up at the health post; *continuity.* | Correct demonstration on the day of discharge. |

::: tip Exam tip
For a tube-feeding case write the volume and rate calculation, the free-water flush, the placement check and the head-up position, then three NANDA-I diagnoses starting with aspiration risk.
:::

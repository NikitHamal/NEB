---
subject: Integrated Health Sciences I
grade: BSc Nursing Year 1
unit: 5
title: Digestion, Metabolism and Energy
hours: 30
area: BSN 1 · Integrated Health Sciences I · Unit 5
---

Food becomes energy, growth and repair through digestion, absorption and metabolism. This unit follows a plate of dal-bhat from mouth to cell: the structure and secretions of the gut, the work of the liver and pancreas, energy and the basal metabolic rate, glucose, and the physiology behind oral rehydration salts, which have saved millions of Nepali children from diarrhoea.

::: key What this unit gives you
- The wall of the gut, the stomach, the small-intestinal villus and the liver, shown in real micrographs.
- A table of enzymes, sites and end products for carbohydrate, protein and fat.
- BMR, total energy expenditure, the energy value of a Nepali meal and glucose unit conversions, all computed.
- Why ORS works: sodium-glucose co-transport, the WHO osmolarity and the zinc course.
- Eight points on nursing care of a patient with a nasogastric tube, and model answers with a full care plan for peptic ulcer disease.
:::

## 5.1 Organisation of the gastrointestinal tract

The alimentary canal runs from the mouth to the anus (about 9 m) and is helped by the **salivary glands, liver, gallbladder and pancreas**. Its wall has four layers from inside out: **mucosa** (epithelium, absorption and secretion), **submucosa** (vessels and the Meissner nerve plexus), **muscularis** (circular and longitudinal muscle with the Auerbach plexus, which gives peristalsis) and **serosa** (the peritoneum). The gut is controlled by the enteric nervous system, the vagus (parasympathetic, which increases motility and secretion) and hormones: **gastrin** (stomach acid), **secretin** (pancreatic bicarbonate), **cholecystokinin (CCK)** (gallbladder contraction and pancreatic enzymes) and **motilin**. Each day about **7000 mL** of secretions enter the gut (saliva 1500, gastric juice 2000, bile 500, pancreatic juice 1500, intestinal juice 1500), and nearly all is reabsorbed, which is why severe diarrhoea or vomiting drains the body so fast.

```svgfig label="5.1" caption="Stations of digestion. Each organ adds its secretion and enzyme; most absorption takes place in the small intestine and water is recovered in the colon."
f = Fig(760, 250)
st = [("Mouth\nsalivary amylase\nchewing", AMBER), ("Oesophagus\nperistalsis\n(no digestion)", SLATE), ("Stomach\nHCl, pepsin\nchyme, pH 1.5-3.5", RED), ("Small intestine\n6 m: bile, lipase,\ntrypsin, absorption", TEAL), ("Large intestine\nwater, electrolytes,\nflora, faeces", NAVY)]
for i, (t_, c) in enumerate(st):
    x = 8 + i * 150; f.box(x, 40, 134, 76, t_, fill="#ffffff", stroke=c, size=10.5, color=c, bold=True)
    if i < 4: f.arrow([(x + 134, 78), (x + 150, 78)], color=SLATE, sw=2)
f.box(210, 150, 160, 50, "Liver and gallbladder\nbile: emulsifies fat", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(400, 150, 160, 50, "Pancreas\nenzymes + bicarbonate", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(290, 150), (440, 116)], color=AMBER, sw=1.8); f.arrow([(480, 150), (470, 116)], color=TEAL, sw=1.8)
f.text(380, 228, "Both pour into the duodenum through the ampulla of Vater", size=11, color=SLATE, bold=True)
```

## 5.2 The stomach and the small intestine

The stomach stores food (capacity about 1.5 L), churns it and begins protein digestion. **Parietal cells** secrete HCl (pH 1.5-3.5, kills microbes, activates pepsinogen to **pepsin**) and **intrinsic factor** (needed for vitamin B12; a lack causes pernicious anaemia); **chief cells** secrete pepsinogen; **mucous cells** make a protective bicarbonate-rich mucus. Damage to this barrier by *Helicobacter pylori* (very common in Nepal) or NSAIDs causes **peptic ulcer**. The small intestine has three parts (duodenum, jejunum, ileum). Its **circular folds, villi and microvilli** multiply the surface area to about 200 m², and each villus holds a capillary network and a lacteal (for fat).

```photogrid label="5.1" cols="2" ratio="1.25" caption="Stomach and intestine. (a) Normal gastric (fundic) mucosa in section: the surface epithelium on top and long straight glands below; the inset shows parietal cells with round central nuclei and pink granular cytoplasm. (b) The intestinal wall: plan of a villus with its capillary and lacteal, and below it micrographs of villi in section."
@ photo id="nur1/fundic" cap="Fundic (gastric) mucosa, H&E"
fit 1.25
focus 0.5 0.5
mark 0.50 0.92 "1"
mark 0.45 0.45 "2"
mark 0.88 0.20 "3"
key 1 (a) Surface mucous cells with deep pits
key 2 (a) Gastric glands going down to the muscularis mucosae
key 3 (a) Inset: parietal cells (acid and intrinsic factor)
@ photo id="nur1/villi" cap="Small intestine villus"
fit 1.25
focus 0.5 0.5
mark 0.50 0.62 "1"
mark 0.52 0.10 "2"
key 1 (b) Villus: absorptive cells, capillary and central lacteal
key 2 (b) Micrograph of villi cut lengthwise
```

| Nutrient | Enzyme (source) | Site | End product |
|---|---|---|---|
| Starch | Salivary and pancreatic amylase | Mouth, duodenum | Maltose, then glucose by brush-border maltase |
| Protein | Pepsin (stomach); trypsin, chymotrypsin (pancreas); peptidases | Stomach, duodenum, brush border | Amino acids, di- and tripeptides |
| Fat | Pancreatic lipase with bile salts | Duodenum | Fatty acids and monoglycerides, absorbed into lacteals as chylomicrons |
| Lactose | Lactase (brush border) | Small intestine | Glucose and galactose (lactase deficiency causes bloating and diarrhoea) |
| Nucleic acids | Nucleases | Duodenum | Nucleotides |

Glucose and galactose are absorbed by the **sodium-glucose co-transporter (SGLT1)** and fructose by facilitated diffusion; amino acids use sodium-linked carriers; fat-soluble vitamins (A, D, E, K) go with fat; **iron is absorbed in the duodenum** and B12 in the terminal ileum, so ileal resection causes B12 deficiency.

## 5.3 Liver, bile, pancreas and jaundice

The liver (about 1.5 kg, the largest gland) has hexagonal lobules of **hepatocytes** arranged around a central vein, with portal triads (portal vein, hepatic artery and bile duct) at the corners. It makes bile, albumin and clotting factors, stores glycogen and vitamins, converts ammonia to urea and detoxifies drugs, which is why drug dose is reduced in liver disease. The **gallbladder** concentrates and stores bile. **Bilirubin**, from the breakdown of red cells, is carried to the liver, conjugated and excreted in bile; a total bilirubin above about 2.5 mg/dL appears as **jaundice**. If total bilirubin is 3.0 mg/dL and the direct (conjugated) part is 0.8 mg/dL, the indirect part is 3.0 − 0.8 = **2.2 mg/dL**, so the main problem is before the liver (haemolysis) or in uptake, not an obstruction. Hepatitis A and E (waterborne, with outbreaks in Nepal) are common causes of acute jaundice; hepatitis B is prevented by the NIP pentavalent vaccine.

```photogrid label="5.2" cols="2" ratio="1.1" caption="The liver cell. (a) Hepatocytes at high magnification: large polygonal cells with a round central nucleus and a prominent nucleolus. (b) Plan of the hepatic lobule and the route of blood and bile."
@ photo id="nur1/liver" cap="Hepatocytes (H&E)"
fit 1.1
focus 0.5 0.5
mark 0.31 0.41 "1"
mark 0.75 0.80 "2"
key 1 (a) Hepatocyte nucleus with a dark nucleolus
key 2 (a) Pale space (sinusoid) between plates of liver cells
@ svg cap="Hepatic lobule"
f = Fig(330, 300)
f.circle(165, 150, 118, fill="#fff7ed", stroke=AMBER, sw=2.5)
f.circle(165, 150, 22, fill="#bfdbfe", stroke=NAVY, sw=2)
for k in range(6):
    import math
    a = k * math.pi / 3 + 0.5; x = 165 + 118 * math.cos(a) * 0.95; y = 150 + 118 * math.sin(a) * 0.95
    f.circle(x, y, 9, fill="#fecaca", stroke=RED, sw=1.5)
    f.arrow([(x - (x - 165) * 0.12, y - (y - 150) * 0.12), (165 + (x - 165) * 0.25, 150 + (y - 150) * 0.25)], color=RED, sw=1.2)
f.text(165, 150, "Central\nvein", size=9, color=NAVY, bold=True)
f.text(165, 14, "Portal triad at each corner: portal vein, hepatic artery, bile duct", size=9.5, color=RED, bold=True)
f.text(165, 285, "Blood flows to the centre along sinusoids; bile flows outward", size=9.5, color=AMBER, bold=True)
```

## 5.4 Metabolism and energy

**Metabolism** is all the chemical reactions of the body: *catabolism* breaks molecules down to release energy (glycolysis in the cytoplasm gives 2 ATP from one glucose; the Krebs cycle and the electron transport chain in mitochondria give about 30-32 more) and *anabolism* builds tissue. The fed state is under **insulin** (glucose goes into cells and glycogen), the fasting state under **glucagon, cortisol and adrenaline** (glycogenolysis, then gluconeogenesis and ketone production). The energy values are **4 kcal/g for carbohydrate and protein, 9 kcal/g for fat** (7 for alcohol). A plate of dal-bhat with 300 g of carbohydrate, 70 g of protein and 60 g of fat gives 300 × 4 + 70 × 4 + 60 × 9 = **2020 kcal**, which is 59% carbohydrate, 14% protein and 27% fat by energy.

```photogrid label="5.3" cols="2" ratio="1.3" caption="A Nepali meal. (a) Dal-bhat-tarkari thali: rice (carbohydrate), lentil soup (protein, iron, folate), green saag (vitamins, iron, fibre) and curd (protein, calcium). (b) The same meal as energy shares of 2,020 kcal."
@ photo id="nur1/dalbhat" cap="Dal-bhat thali"
fit 1.3
focus 0.5 0.5
mark 0.57 0.26 "1"
mark 0.28 0.56 "2"
mark 0.365 0.29 "3"
mark 0.72 0.63 "4"
key 1 (a) Rice: starch, about 4 kcal/g
key 2 (a) Dal: protein, iron, folate
key 3 (a) Green saag: vitamins A, C, K and iron
key 4 (a) Curd: protein and calcium
@ svg cap="Energy shares of the meal"
f = Fig(330, 250)
f.box(15, 50, 178, 46, "Carbohydrate\n59%", fill="#fde68a", stroke=AMBER, size=10.5, bold=True, r=0)
f.box(193, 50, 42, 46, "Pro\n14%", fill="#bbf7d0", stroke=TEAL, size=9.5, bold=True, r=0)
f.box(235, 50, 80, 46, "Fat 27%", fill="#fecaca", stroke=RED, size=10.5, bold=True, r=0)
f.text(165, 30, "2,020 kcal per day", size=12, color=NAVY, bold=True)
f.text(104, 120, "1200 kcal", size=10.5, color=AMBER, bold=True); f.text(214, 120, "280", size=10.5, color=TEAL, bold=True); f.text(275, 120, "540 kcal", size=10.5, color=RED, bold=True)
f.box(15, 150, 300, 80, "", fill=SOFT, stroke="#cbd5e1", r=8)
f.text(165, 170, "Energy per gram", size=11, color=NAVY, bold=True)
f.text(165, 192, "Carbohydrate 4   Protein 4   Fat 9   Alcohol 7", size=10.5, color=SLATE, bold=True)
f.text(165, 214, "Acceptable range: 55-65% / 10-15% / 20-30%", size=10, color=SLATE)
```

**Basal metabolic rate (BMR)** is the energy used at complete rest. The Harris-Benedict equation for a woman is 655.1 + 9.563 × weight (kg) + 1.850 × height (cm) − 4.676 × age. For 54 kg, 158 cm and 20 years: **1370 kcal/day**. The Mifflin-St Jeor equation (10 × weight + 6.25 × height − 5 × age − 161) gives **1266 kcal/day** for the same woman. The **total energy expenditure** is BMR × an activity factor, 1.2 for bed rest, 1.55 for moderate activity: 1266 × 1.55 = **1963 kcal/day**. Fever raises the BMR by about 10-13% for each degree Celsius, and so do burns and sepsis.

**Glucose units.** Laboratories in Nepal report mg/dL; dividing by 18.016 gives mmol/L. A fasting plasma glucose of 100 mg/dL is **5.6 mmol/L** (impaired fasting glucose starts here) and 126 mg/dL is **7.0 mmol/L**, the diabetes cut-off. Nepal's PEN programme screens adults over 40 for blood glucose with a glucometer at the health post.

## 5.5 Why oral rehydration salts work

In diarrhoea the gut loses water and salt, but the **sodium-glucose co-transporter (SGLT1) stays intact**: each glucose carries a sodium ion into the cell and water follows by osmosis, so a drink of salt plus sugar rehydrates even while stools are passing. The **WHO low-osmolarity ORS** (introduced 2002 and used in Nepal's national programme) has 75 mmol/L sodium, 65 chloride, 75 glucose, 20 potassium and 10 citrate, so its osmolarity is 75 + 65 + 75 + 20 + 10 = **245 mOsm/L**. One litre has 13.5 g of anhydrous glucose = 13.5 ÷ 180.16 × 1000 = **75 mmol/L**. A child with *some dehydration* receives 75 mL/kg over 4 hours, so a 4 kg infant needs 75 × 4 = **300 mL** (Plan B of IMNCI Nepal), and **zinc 20 mg daily for 10 days** (10 mg for infants below 6 months, total 20 × 10 = **200 mg** in the older child) is given to shorten the illness and prevent recurrence.

```python
hb = 655.1 + 9.563 * 54 + 1.850 * 158 - 4.676 * 20
mif = 10 * 54 + 6.25 * 158 - 5 * 20 - 161
tee = mif * 1.55
kcal = 300 * 4 + 70 * 4 + 60 * 9
ors = 75 + 65 + 75 + 20 + 10
glu = 13.5 / 180.16 * 1000
print("Harris-Benedict BMR", f"{hb:.0f}")
print("Mifflin BMR", f"{mif:.0f}")
print("TEE", f"{tee:.0f}")
print("Meal kcal", kcal)
print("ORS mOsm/L", ors)
print("ORS glucose mmol/L", f"{glu:.0f}")
print("FPG 100 mg/dL in mmol/L", f"{100 / 18.016:.1f}")
```

```text
Harris-Benedict BMR 1370
Mifflin BMR 1266
TEE 1963
Meal kcal 2020
ORS mOsm/L 245
ORS glucose mmol/L 75
FPG 100 mg/dL in mmol/L 5.6
```

## 5.6 Nursing care of a patient with a nasogastric (NG) tube: eight points

An NG tube is passed through the nose into the stomach to feed, give drugs, aspirate or decompress. It is ordered for unconscious, post-stroke or dysphagic patients, in intestinal obstruction and in poisoning.

1. **Explain and prepare.** Tell the patient what will happen, sit them upright (Fowler's), and gather the tube (size 12-14 Fr for adults), lubricant, tape, syringe, pH paper, stethoscope and a kidney dish. Wash hands and wear gloves. Good explanation reduces gagging and fear.
2. **Measure the length (NEX).** Measure from the nose tip to the earlobe and then to the xiphisternum, and mark the tube. This puts the tip in the stomach and not in the oesophagus. Record the mark at the nostril.
3. **Insert correctly.** Lubricate the tip, pass it along the floor of the nose, ask the patient to flex the neck and sip water while you advance it. Stop and withdraw if there is coughing, cyanosis or breathlessness, as the tube may be in the airway. Never force against resistance.
4. **Confirm position before every use.** Aspirate gastric fluid and test the pH: a value of 5.5 or less is safe for feeding. If in doubt, an X-ray is needed. Air-bubble listening alone is unreliable and a misplaced tube feed into the lung can be fatal.
5. **Secure and mark.** Tape the tube to the nose and cheek without pressure on the nostril, and note the external length each shift. Rotate the tape site to avoid pressure injury. A dislodged tube is a common cause of aspiration.
6. **Feed safely.** Keep the head of the bed at 30-45 degrees during and for an hour after feeds. Give the feed at room temperature, slowly by gravity or pump, and flush with 30 mL of water before and after each feed and drug. Crush only the tablets allowed and give each drug separately.
7. **Watch for complications.** Check for aspiration (cough, fever, breathlessness), diarrhoea, vomiting, abdominal distension, blocked tube and nasal skin injury. Stop the feed and call the doctor if aspiration is suspected. Weigh and record intake and output.
8. **Care of mouth, nose and records.** Give mouth care every 4 hours since the mouth dries when not eating, clean the nostril and change the tape daily. Record the tube size, mark, pH, feed type, volume and response. Teach relatives to keep the head up and never to put in food or medicine themselves.

## Formula and fact sheet

- Energy: carbohydrate 4, protein 4, fat 9, alcohol 7 kcal/g. Example meal 2020 kcal (59% / 14% / 27%).
- Mifflin-St Jeor (woman) = 10 W + 6.25 H − 5 A − 161 (1266 kcal). Harris-Benedict gives 1370. TEE = BMR × activity factor (1963 kcal at 1.55).
- Glucose mmol/L = mg/dL ÷ 18.016 (100 mg/dL = 5.6; 126 mg/dL = 7.0 mmol/L).
- WHO ORS = 245 mOsm/L; 75 mL/kg over 4 h for some dehydration; zinc 20 mg × 10 days = 200 mg.
- Indirect bilirubin = total − direct. Daily GI secretions about 7000 mL, nearly all reabsorbed.

## Chapter summary

- The gut wall has four layers; vagus, enteric plexuses and hormones (gastrin, secretin, CCK) control it.
- Stomach acid and pepsin start protein digestion; the small intestine, with bile and pancreatic enzymes, completes digestion and absorbs nearly everything through villi.
- The liver makes bile and proteins, handles bilirubin and detoxifies; jaundice appears above about 2.5 mg/dL.
- Energy comes from glucose, fat and protein; BMR times an activity factor gives daily need.
- ORS works because glucose carries sodium and water into the cell; zinc shortens diarrhoea.
- NG-tube safety depends on measuring, pH-checking, positioning and flushing.

## Practice

**MCQs (with reasons)**

1. Intrinsic factor, needed for vitamin B12 absorption, is secreted by: (a) chief cells (b) parietal cells (c) mucous cells (d) G cells.
2. A meal with 300 g carbohydrate, 70 g protein and 60 g fat supplies: (a) 1,540 kcal (b) 2,020 kcal (c) 2,500 kcal (d) 3,300 kcal.
3. The osmolarity of WHO low-osmolarity ORS is: (a) 150 (b) 245 (c) 311 (d) 400 mOsm/L.
4. A fasting plasma glucose of 126 mg/dL equals about: (a) 5.6 (b) 6.1 (c) 7.0 (d) 11.1 mmol/L.
5. The best test to confirm NG tube position before feeding is: (a) air insufflation (b) gastric aspirate pH 5.5 or less (c) patient says it is comfortable (d) tube length alone.

::: note Answers and rationales
**1. (b).** Parietal cells make HCl and intrinsic factor; chief cells make pepsinogen and mucous cells make mucus.
**2. (b).** 1,200 + 280 + 540 = 2020 kcal. Option (d) forgets the energy conversion factors.
**3. (b).** 75 + 65 + 75 + 20 + 10 = 245 mOsm/L, lower than the older 311 formula and better for reducing stool output.
**4. (c).** 126 ÷ 18.016 = 7.0 mmol/L, the diagnostic threshold; 5.6 is the fasting value of 100 mg/dL.
**5. (b).** An acid aspirate (pH 5.5 or less) shows the tip is in the stomach; air listening misses lung placement.
:::

**Short answer (3 marks): Functions of the liver.** The liver makes bile for fat digestion, albumin and clotting factors, and stores glycogen, iron and vitamins A, D, B12. It converts ammonia to urea, breaks down hormones and drugs, and removes bilirubin from the blood. It also performs gluconeogenesis in fasting. Liver failure therefore causes jaundice, oedema, bleeding, hypoglycaemia and confusion (ammonia), and drug doses are reduced.

**Medium answer (5 marks): Describe digestion and absorption in the small intestine (Figure 5.1).** Acid chyme from the stomach reaches the duodenum, which releases secretin and CCK; the pancreas pours in bicarbonate that neutralises the acid and enzymes that digest each food class. Amylase splits starch to maltose, trypsin and chymotrypsin split proteins to peptides, and lipase with bile salts splits emulsified fat to fatty acids and monoglycerides. The brush border completes the job with maltase, lactase and peptidases. The surface is multiplied about 600 times by circular folds, villi and microvilli (about 200 m²). Glucose and galactose enter by the sodium-linked SGLT1, amino acids by carriers, and fat as micelles into the lacteal as chylomicrons. Iron is absorbed in the duodenum and vitamin B12 with intrinsic factor in the ileum. Water follows by osmosis, and about 9 L of fluid are absorbed every day.

**Long answer (10 marks): Mr Krishna Prasad Adhikari, 48, a farmer who takes diclofenac for back pain, comes to the emergency of a district hospital with burning epigastric pain that wakes him at night and eases with food, and black tarry stool this morning. He is dizzy and pale. Pulse 108/min, BP 98/60 mmHg. Discuss the condition and prepare a nursing care plan.**

*Introduction.* This is a bleeding duodenal ulcer: *H. pylori* infection and NSAID use damage the mucus-bicarbonate barrier, acid and pepsin digest the mucosa, and an eroded artery bleeds, giving melaena. His shock index is 108 ÷ 98 = **1.10**, above 0.9, and the MAP is (98 + 120) ÷ 3 = **72.7 mmHg**, so he is in early haemorrhagic shock and needs urgent resuscitation. Priorities: two large-bore IV lines, crystalloid then blood by cross-match, nil by mouth, oxygen, a PPI by IV (omeprazole or pantoprazole 80 mg then infusion or 40 mg twice daily), endoscopy within 24 hours, stop diclofenac, and test for *H. pylori* (stool antigen or biopsy). After healing, eradication therapy of a PPI, amoxicillin and clarithromycin twice daily for 14 days (28 doses of PPI in all, as per national guideline) prevents recurrence. Surgery or radiological embolisation is required if bleeding continues.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I feel dizzy." **O:** melaena, P 108, BP 98/60, shock index 1.10, pale. | **Risk for deficient fluid volume** (shock) related to active gastrointestinal bleeding. | **Fluid balance:** SBP at least 100, pulse below 100, urine at least 0.5 mL/kg/h in 6 h. | 1. Establish two large IV lines, give fluids and blood as ordered; *restores volume and oxygen carriage.* 2. Vitals every 15 min, hourly urine, record stool; *detects ongoing loss.* 3. Keep nil by mouth; *rests the gut.* 4. Lie flat with legs raised; *improves venous return.* | Pulse, BP, urine and haemoglobin tracked; goal met when stable for 6 h. |
| **S:** "Burning pain in the stomach." **O:** epigastric tenderness, pain score 7/10. | **Acute pain** related to acid erosion of the mucosa, as evidenced by self-report and guarding. | **Pain level:** score 3 or lower within 2 h. | 1. Give IV PPI on schedule; *reduces acid and allows clotting.* 2. Assess pain with a numeric scale; *guides treatment.* 3. Avoid NSAIDs and aspirin; *they cause ulcer.* 4. Comfortable position and calm environment; *reduces stress acid.* | Pain scored every hour; relief within the target. |
| **S:** "I take diclofenac every day." **O:** no knowledge of ulcer causes. | **Deficient knowledge** about ulcer prevention and treatment. | **Knowledge: treatment regimen:** states 3 triggers and the full antibiotic course before discharge. | 1. Teach to avoid NSAIDs, smoking, alcohol and irregular meals; *removes causes.* 2. Teach to take all 14 days of antibiotics with the PPI; *eradicates H. pylori.* 3. Teach black stool, vomiting blood and dizziness as signs to return; *early detection.* | Teach-back before discharge; follow-up at 4 weeks. |

::: tip Exam tip
Always link the cause (H. pylori, NSAID) to the mechanism, quote the shock index and MAP when bleeding is described, and finish with eradication therapy and health education. That sequence is the structure examiners mark.
:::

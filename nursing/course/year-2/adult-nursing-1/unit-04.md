---
subject: Adult Nursing I
grade: BSc Nursing Year 2
unit: 4
title: Gastrointestinal and Hepatobiliary Nursing: Ulcer, Bleeding, Acute Abdomen, Stoma and Liver Disease
hours: 22
area: BSN 9 · Adult Nursing I · Unit 4
---

Abdominal pain, vomiting, black stools and a swollen belly bring many adults to the emergency room and medical wards of Nepal's hospitals. **Gastritis and peptic ulcer** are common in a country where *Helicobacter pylori* infection is widespread and spicy, irregular meals, tobacco and NSAID tablets are daily habits; **cirrhosis from alcohol (raksi) and hepatitis B and C** fills the liver wards; and **hepatitis A and E** spread through contaminated water in the monsoon season. The nurse must recognise **gastrointestinal bleeding**, **an acute abdomen** and **hepatic encephalopathy** early, because each is a medical emergency. All arithmetic is checked by program.

::: key What this unit gives you
- Real photographs of jaundice, an *H. pylori* rapid-test cassette, an abdominal X-ray with dilated bowel and air-fluid levels, and an illustration of colostomy versus ileostomy, with three SVG figures.
- Assessment, peptic ulcer and *H. pylori* therapy, GI bleeding classes, shock index and the Alvarado score.
- Acute abdomen and intestinal obstruction, stoma care, viral hepatitis, cirrhosis with the Child-Pugh score, paracentesis and eight points on each of ulcer care, stoma care and cirrhosis care.
- Model answers and a NANDA-I care plan for a patient with cirrhosis and ascites.
:::

## 4.1 Assessment of the gastrointestinal patient

Ask about **appetite, nausea, vomiting (colour: coffee-ground or bright red), pain (site, timing with meals, radiation), bowel habit (diarrhoea, constipation, black tarry stool or melaena), weight loss, alcohol, tobacco, drugs (NSAIDs, steroids) and jaundice**. Inspect for jaundice, pallor, distension, scars, visible veins and the abdomen's movement; **auscultate before palpating** (bowel sounds 5-30 per minute; absent in ileus, high-pitched in obstruction); percuss for fluid; palpate gently for tenderness, guarding, rebound and masses. Tests: **haemoglobin, liver function tests, amylase or lipase, stool occult blood, abdominal ultrasound, plain X-ray, endoscopy and *H. pylori* test**.

```photogrid label="4.1" cols="4" ratio="1.0" caption="Gastrointestinal and liver findings. (a) A real photograph of a patient with jaundice: the whites of the eyes (sclerae) are yellow because bilirubin is raised. (b) A real rapid antigen test cassette for Helicobacter pylori: a control line and a test line show the result. (c) A real plain abdominal X-ray with dilated bowel loops and air-fluid levels: intestinal obstruction. (d) A teaching illustration of the two common stomas, colostomy (large bowel, solid stool) and ileostomy (small bowel, liquid stool)."
@ photo id="nur5/icterus" cap="Jaundice"
fit 1.0
focus 0.45 0.5
mark 0.68 0.72 "1"
key 1 (a) Yellow sclera: visible when bilirubin is above about 2.5 mg/dL (40 micromol/L)
@ photo id="nur5/hpylori" cap="H. pylori rapid test"
fit 1.0
focus 0.5 0.5
mark 0.41 0.50 "2"
key 2 (b) Result window: a coloured line at C only is negative; lines at both C and T are positive
@ photo id="nur5/sbo" cap="Bowel obstruction X-ray"
fit 1.0
focus 0.5 0.5
mark 0.30 0.36 "3"
mark 0.70 0.52 "4"
key 3 (c) Gas-filled dilated bowel loop: the bowel above the block fills with air and fluid
key 4 (c) Air-fluid level: a horizontal line seen on an erect or decubitus film
@ photo id="nur5/ostomy" cap="Colostomy and ileostomy"
fit 1.0
```

## 4.2 Gastritis, peptic ulcer and *H. pylori*

**Peptic ulcer** is a break in the lining of the stomach (gastric) or duodenum (duodenal), caused by acid and pepsin when the defence of mucus is weakened by ***H. pylori*** (about 70-90% of duodenal and 60-70% of gastric ulcers) or **NSAIDs**. Duodenal ulcer pain is **burning epigastric pain that comes 2-3 hours after meals or at night and is relieved by food**; gastric ulcer pain is **worse soon after eating** and with weight loss. **Complications** are bleeding (haematemesis, melaena), perforation (sudden severe pain with a rigid abdomen), gastric outlet obstruction and cancer. **Treatment** is acid suppression with a proton pump inhibitor (omeprazole 20-40 mg daily), stopping NSAIDs, and **eradication of *H. pylori*** by **triple therapy for 14 days: PPI + amoxicillin 1 g twice daily + clarithromycin 500 mg twice daily**; bismuth quadruple therapy is used where clarithromycin resistance is high or the first course fails. Confirm cure by a breath or stool antigen test 4 weeks after treatment.

```svgfig label="4.2" caption="Peptic ulcer pathway and treatment. Imbalance between aggressive factors (acid, pepsin, H. pylori, NSAIDs, smoking) and defensive factors (mucus, bicarbonate, blood flow) produces the ulcer. Treatment removes the cause, reduces acid, protects the mucosa and eradicates H. pylori."
f = Fig(760, 210)
f.box(10, 20, 220, 70, "Aggressive factors\nAcid, pepsin, H. pylori,\nNSAIDs, smoking", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(10, 120, 220, 70, "Defensive factors\nMucus, bicarbonate,\nmucosal blood flow", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.poly([(255, 65), (330, 105), (255, 145)], fill=SAND, stroke=AMBER, label="Imbalance", lx=290, ly=105, size=9.5)
f.box(350, 70, 170, 70, "ULCER\nPain, bleeding,\nperforation", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(545, 20, 205, 50, "PPI + stop NSAIDs\nand smoking", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(545, 80, 205, 50, "Eradicate H. pylori: PPI +\namoxicillin + clarithromycin, 14 days", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(545, 140, 205, 50, "Diet: regular small meals,\nno alcohol, no spicy food", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.arrow([(230, 55), (258, 85)], sw=1.8); f.arrow([(230, 155), (258, 125)], sw=1.8); f.arrow([(330, 105), (350, 105)], sw=1.8)
```

### Peptic ulcer: eight points of nursing care and teaching

1. **Relieve pain.** Give the antacid, PPI or other drugs as ordered and note when pain occurs in relation to meals. Pain that suddenly becomes severe and constant, with a rigid abdomen, may mean perforation. Report it at once and keep the patient fasting.
2. **Give drugs correctly.** Give the PPI 30 minutes before breakfast, antacids 1 hour after meals and at bedtime, and finish the full 14 days of *H. pylori* therapy. Warn about the metallic taste and loose stools from clarithromycin. Stopping early leads to resistant bacteria.
3. **Teach about diet.** Advise regular, small, unhurried meals and avoid foods that cause pain for that person, such as very spicy food, strong tea and coffee. Milk helps for a short time but then increases acid. There is no need for a bland diet beyond this.
4. **Stop tobacco and alcohol.** Smoking delays ulcer healing and raises the chance of recurrence; alcohol irritates the stomach. Offer a plan to quit. Both are major causes of ulcer failure.
5. **Avoid NSAIDs.** Tell the patient not to take ibuprofen, diclofenac or aspirin tablets for pain without advice, and to use paracetamol instead. Steroid use also needs care. Many ulcers in Nepal start with pain-killers bought over the counter.
6. **Watch for bleeding.** Look for vomiting of coffee-ground material, black tarry stool, dizziness and a fast pulse. Measure the pulse and BP and keep a stool chart. Report any change quickly.
7. **Manage stress and sleep.** Anxiety can worsen symptoms, so teach relaxation, regular sleep and meal times. Offer counselling when needed. A calm routine also helps taking drugs regularly.
8. **Follow up.** Stress that an ulcer in the stomach needs endoscopy to exclude cancer and a repeat test for cure. Teach to return for dark stool, vomiting blood, severe pain or weight loss. Explain that the ulcer heals in 4-8 weeks with proper treatment.

## 4.3 Gastrointestinal bleeding and the numbers

**Upper GI bleeding** (above the ligament of Treitz) gives haematemesis and melaena; the causes are peptic ulcer, oesophageal varices, gastritis and tumours. **Lower GI bleeding** gives fresh red blood per rectum (haemorrhoids, colitis, polyps, cancer). The **blood volume** of an adult is about **70 mL/kg**. The **haemorrhage classes** are: **class I** under 15% loss (under 750 mL), pulse normal; **class II** 15-30% (750-1,500 mL), pulse over 100, narrow pulse pressure; **class III** 30-40% (1,500-2,000 mL), pulse over 120, low BP, confusion; **class IV** over 40%, pulse over 140, collapse. The **shock index** (heart rate ÷ systolic BP) is above 0.9 in significant bleeding.

```python
w = 60; bv = 70 * w; loss = 0.35 * bv
hr, sbp = 120, 90
print(f"Blood volume = 70 x {w} = {bv:,} mL; 35% loss = {loss:,.0f} mL: class III")
print(f"Shock index = {hr} / {sbp} = {hr / sbp:.2f} (above 0.9: significant bleeding)")
crys = loss * 3
print(f"Crystalloid 3 mL per mL lost = {crys:,.0f} mL; or blood: 1 unit raises Hb by 1 g/dL in a 70 kg adult")
score = 1 + 1 + 1 + 2 + 1 + 1 + 2 + 0
print(f"Alvarado score = {score} (pain migration 1, anorexia 1, nausea 1, RLQ tenderness 2, rebound 1, fever 1, WBC 2, shift 0): appendicitis likely")
ngl = 1500; total = 1800 + ngl
print(f"Obstruction: maintenance 1,800 + NG loss {ngl:,} = {total:,} mL/24 h = {total / 24:.1f} mL/h")
```

```text
Blood volume = 70 x 60 = 4,200 mL; 35% loss = 1,470 mL: class III
Shock index = 120 / 90 = 1.33 (above 0.9: significant bleeding)
Crystalloid 3 mL per mL lost = 4,410 mL; or blood: 1 unit raises Hb by 1 g/dL in a 70 kg adult
Alvarado score = 9 (pain migration 1, anorexia 1, nausea 1, RLQ tenderness 2, rebound 1, fever 1, WBC 2, shift 0): appendicitis likely
Obstruction: maintenance 1,800 + NG loss 1,500 = 3,300 mL/24 h = 137.5 mL/h
```

A 60-kg patient has **4,200 mL of blood**, so a 35% loss is **1,470 mL (class III)**, and the **shock index of 120/90 is 1.33**. Replacing a haemorrhage with crystalloid needs about 3 mL for each mL lost (**4,410 mL**), but blood is needed in class III and IV. A patient with an **Alvarado score of 9** (0-4 unlikely, 5-6 possible, 7-10 probable) most likely has appendicitis and needs surgical review. In intestinal obstruction, maintenance fluid of 1,800 mL plus 1,500 mL of nasogastric loss gives **3,300 mL in 24 hours, which is 137.5 mL/h**.

```svgfig label="4.3" caption="Management algorithm for acute upper GI bleeding. Resuscitate first (airway, two large IV lines, fluids, blood), then give a PPI (and terlipressin or octreotide if varices are suspected, with ceftriaxone), then arrange endoscopy within 24 hours. The nurse records pulse, BP, urine and every vomit."
f = Fig(760, 230)
f.box(10, 15, 170, 70, "1 ABC and shock?\nOxygen, 2 large IV\nlines, group and match", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(200, 15, 170, 70, "2 Resuscitate\nFluid then blood\nHb target 7-8 g/dL", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(390, 15, 170, 70, "3 Drugs\nIV PPI; if varices\nterlipressin + antibiotic", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(580, 15, 170, 70, "4 Endoscopy\nwithin 24 h: clip,\nband, inject", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(180, 50), (200, 50)], sw=2); f.arrow([(370, 50), (390, 50)], sw=2); f.arrow([(560, 50), (580, 50)], sw=2)
f.box(10, 120, 360, 90, "Nurse: pulse, BP, urine (0.5 mL/kg/h) every 15 min\nNil by mouth, keep head to the side\nMeasure every vomit and stool; reassure", fill=SOFT, stroke=NAVY, size=10.5)
f.box(390, 120, 360, 90, "Call the surgeon for: rebleeding, pulse over 120,\nSBP below 90, fall in Hb, severe abdominal pain\nRefer if endoscopy or surgery is not available", fill=SOFT, stroke=RED, size=10.5)
```

## 4.4 Acute abdomen, intestinal obstruction and stoma care

An **acute abdomen** is sudden severe abdominal pain needing urgent decision on surgery. Causes: **appendicitis** (pain moving from the umbilicus to the right iliac fossa, anorexia, fever, tenderness and rebound), **perforated ulcer**, **intestinal obstruction**, **strangulated hernia**, **acute cholecystitis**, **pancreatitis** and **peritonitis**. **Intestinal obstruction** gives colicky pain, vomiting, distension and absolute constipation (no stool or flatus); causes are adhesions, hernia and tumour in adults, and volvulus is common in Nepal's hill population on a high-fibre diet. The film shows dilated loops with air-fluid levels (Figure 4.1c). Management is **"drip and suck"**: nil by mouth, a nasogastric tube on free drainage, IV fluids with potassium, pain relief, and surgery if there are signs of strangulation (continuous pain, fever, rising pulse, tenderness). **Do not give strong laxatives or enemas** and **do not give analgesics that hide signs before the surgeon sees the patient** unless the doctor orders them.

A **stoma** is a surgical opening of the bowel onto the abdominal wall. A healthy stoma is **pink to red, moist and slightly swollen at first**; a **pale** stoma means poor blood supply or anaemia, and a **dark purple or black** stoma means ischaemia and needs urgent surgical review. Output: colostomy passes formed stool; ileostomy passes liquid stool that can cause dehydration and salt loss.

### Stoma care: eight points of nursing care and teaching

1. **Inspect the stoma every shift.** Note the colour, swelling, bleeding and the skin around it. Report a dark, dry or retracted stoma. A healthy stoma is not painful to touch because it has no pain nerves.
2. **Choose and fit the appliance.** Measure the stoma with the template and cut the skin barrier 2-3 mm larger than the stoma. Apply to clean dry skin and press from the inside out. A tight cut cuts the stoma; a loose cut lets stool burn the skin.
3. **Empty the bag at one-third full.** A heavy bag pulls off the seal and leaks. Change the whole appliance every 3-5 days or sooner if it leaks. Dispose of the used bag in a sealed plastic bag.
4. **Protect the skin.** Wash with plain water, dry gently and avoid alcohol and strong soaps. Look for redness, weeping or sores and use a barrier cream or powder if advised. Skin damage prevents a good seal.
5. **Give diet advice.** For a colostomy, eat a normal fibre-rich diet with plenty of fluid and chew well; some foods cause gas (cabbage, beans, onion) and odour (egg, fish, garlic). For an ileostomy, drink 2-3 litres a day and add salt to food to replace losses. Introduce new foods one by one.
6. **Prevent dehydration (ileostomy).** Output above 1,000-1,500 mL a day with thirst, dizziness and dark urine is a warning. Give oral rehydration solution and report to the doctor. Record the output volume each shift.
7. **Support the body image.** Stoma surgery is a big shock. Listen, let the patient look at and touch the stoma early, and involve a family member. Introduce a peer with a stoma if one exists; most return to work, social life and marriage.
8. **Prepare for home.** Teach changing the bag with return demonstration, where to buy supplies in Nepal, and when to call for help (bleeding, no output for 24 hours with pain, or a dark stoma). Show how to bathe and travel with the bag. Follow-up at the stoma clinic or surgical OPD is arranged.

## 4.5 Liver disease: hepatitis and cirrhosis

**Viral hepatitis A and E** spread by faeces-contaminated water and food (the cause of outbreaks after monsoon floods and in crowded areas); they cause fever, jaundice and dark urine and recover without treatment in most cases, but hepatitis E is dangerous in pregnancy. **Hepatitis B and C** spread by blood, unsafe injections, sexual contact and from mother to baby, and can become chronic, leading to cirrhosis and liver cancer. Hepatitis B vaccine is given in the **pentavalent vaccine** of Nepal's NIP; health workers receive it too. **Cirrhosis** is irreversible scarring of the liver. In Nepal the leading causes are **alcohol (raksi and other home-brewed spirits), hepatitis B and C**, and fatty liver in people with diabetes.

```svgfig label="4.4" caption="Consequences of cirrhosis. Scarring blocks the portal circulation (portal hypertension) and reduces the liver's synthetic and detoxifying work. Portal hypertension gives varices, ascites and splenomegaly; liver failure gives jaundice, bleeding, low albumin and encephalopathy."
f = Fig(760, 230)
f.box(290, 8, 180, 50, "CIRRHOSIS\nscarred, shrunken liver", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(20, 90, 330, 40, "Portal hypertension", fill=SAND, stroke=AMBER, size=12, bold=True)
f.box(410, 90, 330, 40, "Liver cell failure", fill=SAND, stroke=AMBER, size=12, bold=True)
f.arrow([(330, 58), (190, 90)], sw=2); f.arrow([(440, 58), (580, 90)], sw=2)
for i, t in enumerate(["Oesophageal varices\nbleed", "Ascites,\nSBP", "Splenomegaly,\nlow platelets"]):
    f.box(20 + i * 112, 150, 106, 60, t, fill=BLUE, stroke=NAVY, size=9.5, bold=True); f.arrow([(73 + i * 112, 130), (73 + i * 112, 150)], sw=1.6)
for i, t in enumerate(["Jaundice,\nlow albumin", "Bleeding:\nlow clotting", "Hepatic\nencephalopathy"]):
    f.box(410 + i * 112, 150, 106, 60, t, fill=MINT, stroke=TEAL, size=9.5, bold=True); f.arrow([(463 + i * 112, 130), (463 + i * 112, 150)], sw=1.6)
```

The **Child-Pugh score** grades severity by five features, scored 1 to 3 each: **bilirubin** (under 2 mg/dL = 1; 2-3 = 2; over 3 = 3), **albumin** (over 3.5 g/dL = 1; 2.8-3.5 = 2; under 2.8 = 3), **INR** (under 1.7 = 1; 1.7-2.3 = 2; over 2.3 = 3), **ascites** (none = 1; mild = 2; moderate or severe = 3) and **encephalopathy** (none = 1; grade 1-2 = 2; grade 3-4 = 3). **Class A is 5-6, class B is 7-9 and class C is 10-15.**

```python
def cp(bil, alb, inr, asc, enc):
    s = (1 if bil < 2 else 2 if bil <= 3 else 3) + (1 if alb > 3.5 else 2 if alb >= 2.8 else 3)
    s += (1 if inr < 1.7 else 2 if inr <= 2.3 else 3) + asc + enc
    return s, "A" if s <= 6 else "B" if s <= 9 else "C"
print("Compensated patient (bil 1.2, alb 3.8, INR 1.2, no ascites, no encephalopathy):", cp(1.2, 3.8, 1.2, 1, 1))
print("Case patient (bil 3.4, alb 2.5, INR 1.8, moderate ascites, grade 1 encephalopathy):", cp(3.4, 2.5, 1.8, 3, 2))
print(f"Paracentesis 6 L: albumin 8 g per litre = {8 * 6} g = {8 * 6 / 0.20:.0f} mL of 20% albumin")
print(f"SAAG = serum albumin 2.5 - ascitic albumin 0.8 = {2.5 - 0.8:.1f} g/dL (1.1 or more: portal hypertension)")
print(f"Diuretics spironolactone 100 mg : furosemide 40 mg; target weight loss 0.5 kg/day = {0.5 * 7} kg a week; sodium 2 g = {2000 / 393.4:.1f} g salt")
print(f"Protein 1.2 g/kg x 62 kg = {1.2 * 62:.1f} g; lactulose 30 mL three times a day = {30 * 3} mL")
```

```text
Compensated patient (bil 1.2, alb 3.8, INR 1.2, no ascites, no encephalopathy): (5, 'A')
Case patient (bil 3.4, alb 2.5, INR 1.8, moderate ascites, grade 1 encephalopathy): (13, 'C')
Paracentesis 6 L: albumin 8 g per litre = 48 g = 240 mL of 20% albumin
SAAG = serum albumin 2.5 - ascitic albumin 0.8 = 1.7 g/dL (1.1 or more: portal hypertension)
Diuretics spironolactone 100 mg : furosemide 40 mg; target weight loss 0.5 kg/day = 3.5 kg a week; sodium 2 g = 5.1 g salt
Protein 1.2 g/kg x 62 kg = 74.4 g; lactulose 30 mL three times a day = 90 mL
```

The compensated patient scores **5** (class A) and the case patient **13** (class C, poor outlook). After a 6-litre paracentesis, **albumin 8 g per litre removed is 48 g, which is 240 mL of 20% albumin**, given to prevent circulatory collapse. A **SAAG of 1.7 g/dL** shows portal hypertension as the cause of ascites. The safe diuretic aim is a weight loss of **0.5 kg a day**, and protein of 1.2 g/kg for a 62-kg man is **74.4 g**.

### Cirrhosis and ascites: eight points of nursing care

1. **Monitor fluid status daily.** Weigh each morning, measure abdominal girth at the same level (the umbilicus), and record intake and output. A loss over 0.5 kg a day (1 kg if oedema is present) risks kidney injury. Report any fall in urine output.
2. **Restrict sodium and, if needed, fluid.** Allow 2 g of sodium (5 g of salt) a day; fluid is limited to 1-1.5 L only if the serum sodium is below 125. Remove table salt, pickles and packet snacks. A bland diet is not needed.
3. **Give a protein-adequate diet.** Give 1.2-1.5 g/kg of protein with a late-evening snack to prevent muscle breakdown. Do not restrict protein except in severe encephalopathy. Give vitamins (thiamine and folate) especially in alcohol-related disease.
4. **Position and protect the skin.** Raise the head of the bed to ease breathing, support the abdomen and scrotum with pillows, turn every 2 hours and keep nails short for itching. Oedematous, jaundiced skin breaks down easily. Use a pressure-relieving mattress.
5. **Prevent and watch for bleeding.** Varices can bleed suddenly: watch for vomiting blood, black stool and falling BP. Avoid IM injections, use a soft toothbrush and give vitamin K as ordered. Keep a blood group and cross-match ready.
6. **Recognise hepatic encephalopathy.** Early signs are sleep reversal, mood change, a flapping tremor and slow thinking, then drowsiness and coma. Give **lactulose 30 mL three times daily** and adjust to 2-3 soft stools a day, and rifaximin as ordered. Avoid sedatives, correct constipation and bleeding, and treat infection.
7. **Spot infection.** Fever, abdominal pain or tenderness and confusion may mean spontaneous bacterial peritonitis (SBP); ascitic fluid with over 250 neutrophils/mm3 confirms it. Prepare for paracentesis, send samples and give antibiotics. Check the paracentesis site after the procedure.
8. **Teach and counsel.** Stopping alcohol is the most important step, and tell the family that raksi is the commonest cause. Teach drug names, salt limits, the danger signs (vomiting blood, confusion, fever, less urine), hepatitis B vaccination for contacts and regular follow-up. Offer alcohol-treatment services and a social worker.

## 4.6 Gallbladder and pancreas in brief

**Cholelithiasis (gallstones)** is common in women over 40 who are overweight; **biliary colic** is severe right upper abdominal pain after a fatty meal, and **acute cholecystitis** adds fever and a positive Murphy's sign; ultrasound shows stones, and **cholecystectomy** (often laparoscopic) cures it. **Acute pancreatitis**, caused by gallstones or alcohol, gives severe epigastric pain radiating to the back, vomiting and a serum amylase or lipase **at least three times normal**; treatment is nil by mouth, aggressive IV fluid, strong pain relief (opioids), oxygen and early feeding. The nurse measures pain, fluids, urine output, blood glucose and calcium and teaches the patient to avoid alcohol and fatty meals.

## Formula and fact sheet

- Blood volume = 70 mL/kg; haemorrhage class I under 15%, II 15-30%, III 30-40%, IV over 40%; shock index = heart rate ÷ systolic BP (above 0.9 is concerning).
- Alvarado score 0-10 (0-4 unlikely, 5-6 possible, 7-10 probable); maintenance fluid 30 mL/kg/day plus NG loss.
- Child-Pugh A 5-6, B 7-9, C 10-15; SAAG = serum albumin - ascitic albumin (1.1 or more means portal hypertension); give 8 g albumin per litre removed if more than 5 L is drained.
- H. pylori triple therapy: PPI + amoxicillin 1 g BD + clarithromycin 500 mg BD for 14 days; lactulose aim 2-3 soft stools a day.

## Chapter summary

- A GI history and an abdominal examination that listens before it touches guide diagnosis and early action.
- Peptic ulcer is treated by acid suppression, NSAID avoidance and H. pylori eradication; bleeding is a resuscitation emergency.
- Obstruction is managed by "drip and suck" and urgent surgical review; a stoma needs inspection, a correct appliance and teaching.
- Cirrhosis is graded by Child-Pugh; nursing care covers fluid, salt, protein, bleeding, encephalopathy, infection and stopping alcohol.

## Practice

**MCQs (with reasons)**

1. The blood volume of an 80-kg adult is about: (a) 3,000 mL (b) 4,000 mL (c) 5,600 mL (d) 8,000 mL.
2. A patient with pulse 110 and systolic BP 100 has a shock index of: (a) 0.9 (b) 1.1 (c) 1.5 (d) 11.
3. After a 7-litre paracentesis the albumin replacement at 8 g per litre is: (a) 8 g (b) 28 g (c) 56 g (d) 70 g.
4. Serum albumin 2.8 g/dL and ascitic albumin 0.9 g/dL give a SAAG of: (a) 0.3 (b) 1.9 (c) 2.5 (d) 3.7.
5. In hepatic encephalopathy the drug given to produce 2-3 soft stools a day is: (a) furosemide (b) lactulose (c) loperamide (d) morphine.

::: note Answers and rationales
**1. (c).** 70 × 80 = 5,600 mL; (b) uses 50 mL/kg, a child's figure.
**2. (b).** 110 ÷ 100 = 1.1, above 0.9, so the patient is probably bleeding; 0.9 is the cut-off, not the value.
**3. (c).** 8 × 7 = 56 g; albumin is given when more than 5 litres is removed.
**4. (b).** 2.8 - 0.9 = 1.9, so the ascites is caused by portal hypertension (SAAG 1.1 or more).
**5. (b).** Lactulose acidifies the colon, traps ammonia and speeds transit; furosemide treats fluid, and loperamide or morphine slow the gut and worsen encephalopathy.
:::

**Short answer (3 marks): Child-Pugh score.** It is a five-item score for cirrhosis: bilirubin, albumin, INR, ascites and encephalopathy, each scored 1-3. A total of 5-6 is class A, 7-9 class B and 10-15 class C. It predicts survival and guides treatment and surgical risk.

**Medium answer (5 marks): Describe the nursing care of a patient with an upper GI bleed (Figure 4.3).** Keep the airway clear with the head to one side, give oxygen, and insert two large IV lines. Send blood for Hb, group and match and start fluids then blood as ordered. Keep the patient nil by mouth, monitor pulse, BP and urine every 15 minutes and measure every vomit and stool. Give IV PPI, and terlipressin and an antibiotic if varices are suspected. Prepare for endoscopy within 24 hours, report rebleeding or a pulse above 120 or systolic BP below 90, and reassure the patient and family.

**Long answer (10 marks): Mr Dil Bahadur Rai, 48 years, 62 kg, a long-term drinker of raksi, is admitted with a swollen abdomen and yellow eyes for a month. He is drowsy but rousable and has a flapping tremor. Bilirubin 3.4 mg/dL, albumin 2.5 g/dL, INR 1.8, moderate ascites; ascitic albumin 0.8 g/dL. Plan his care.**

*Assessment.* His **Child-Pugh score is 13 (class C)**, with moderate ascites and early encephalopathy. The **SAAG is 2.5 - 0.8 = 1.7 g/dL**, so the ascites is caused by portal hypertension. If a 6-litre paracentesis is done he needs **48 g of albumin (240 mL of 20%)**.

*Plan.* Start **lactulose 30 mL three times a day** and adjust to 2-3 soft stools; avoid sedatives. Give **spironolactone 100 mg with furosemide 40 mg** in the morning and aim for 0.5 kg weight loss a day. Protein is **74.4 g a day (1.2 g/kg)** with a late-evening snack and salt is under 5 g. Weigh daily, measure girth, keep the intake-output chart and check for bleeding and infection. Raise the head of the bed, turn every 2 hours and keep the skin clean. Teach him and his wife that stopping alcohol is the key, give thiamine, refer to alcohol counselling, and explain the danger signs: vomiting blood, confusion, fever and passing little urine.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** moderate ascites, weight 62 kg, girth 98 cm. | **Excess fluid volume** related to portal hypertension and low albumin, as evidenced by ascites. | **Fluid balance:** weight loss 0.5 kg a day and girth falling in 1 week. | 1. Daily weight and girth; *shows response.* 2. Sodium 2 g and diuretics as ordered; *removes retained water.* 3. Intake-output chart; *detects kidney injury.* | Weight 60 kg, girth 92 cm at 5 days. |
| **O:** drowsy, flapping tremor, bilirubin 3.4. | **Acute confusion** related to hepatic encephalopathy. | **Cognitive orientation:** alert and oriented in 3 days. | 1. Lactulose to 2-3 stools a day; *traps ammonia.* 2. Avoid sedatives; *they worsen coma.* 3. Orientation and safety checks; *prevents falls.* | Oriented, no tremor on day 3. |
| **O:** albumin 2.5, jaundiced, bed rest. | **Risk for impaired skin integrity** related to oedema, jaundice and immobility. | **Tissue integrity:** skin intact by discharge. | 1. Turn every 2 hours and pressure mattress; *relieves pressure.* 2. Keep nails short; *prevents scratch wounds.* 3. Protein and vitamins; *support repair.* | Skin intact at discharge. |
| **S:** "I drink raksi every day." | **Deficient knowledge** about liver disease and alcohol. | **Knowledge: illness care:** states 4 danger signs and commits to abstinence. | 1. Teach causes and danger signs in Nepali; *recognition.* 2. Counselling and support group; *sustains abstinence.* 3. Vaccinate contacts for hepatitis B; *prevents spread.* | Repeats 4 danger signs; accepts counselling. |

::: tip Exam tip
For a cirrhosis case write the Child-Pugh score, SAAG, paracentesis albumin, diuretic and weight-loss targets, lactulose aim and four NANDA-I diagnoses beginning with excess fluid volume and acute confusion.
:::

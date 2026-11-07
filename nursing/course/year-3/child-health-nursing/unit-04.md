---
subject: Child Health Nursing
grade: BSc Nursing Year 3
unit: 4
title: Paediatric Infectious Diseases and Systemic Disorders: Measles, Rash Illnesses, Fevers, Meningitis, Rheumatic Fever, Nephrotic Syndrome, Leukaemia and Thalassaemia
hours: 26
area: BSN 21-22 · Child Health Nursing · Units 13-18
---

Bikash Rai is **2 years old**, weighs **11.5 kg** and lives in Jhapa. He has not had the MR vaccine. For 4 days he has had **fever of 39.5 °C, a runny nose, cough and red watery eyes**. Today a **red rash** has started behind his ears and on his face, and the nurse sees **white spots on the inner cheeks (Koplik spots)**. He is irritable, drinks poorly and has 4 loose stools. This is **measles**, and it is a reminder that vaccine-preventable disease still returns wherever coverage falls. The unit also covers other childhood fevers and the systemic disorders that fill the paediatric ward.

::: key What this unit gives you
- Real images: **measles rash**, **Koplik spots**, **chickenpox**, **mumps**, the **dengue "islands of white" rash** and a **blood film of acute lymphoblastic leukaemia**; with numbered marks.
- SVG figures: the **measles course and infectious period** and the **nephrotic syndrome pathway**.
- **Eight points of nursing care in measles** and **seven points of nursing care in nephrotic syndrome**, each in 3-4 plain sentences, anchored in the NIP, MoHP surveillance (EWARS), IMNCI and Nepal practice.
- Verified maths: **vitamin A dose, vaccine efficacy, herd-immunity threshold, aciclovir, BSA and prednisolone, ceftriaxone, benzathine penicillin, transfusion volume**; MCQs, short, medium and long answers and a 5-column NANDA-I plan.
:::

## 4.1 Rash illnesses and vaccine-preventable diseases

| Disease | Cause and incubation | Key features | Treatment and prevention |
|---|---|---|---|
| **Measles** | Measles virus; 10-14 days | Fever, cough, coryza, conjunctivitis, **Koplik spots**, rash from face downwards on day 3-4 | Supportive, **vitamin A**; **MR at 9 and 15 months** |
| **Rubella** | Rubella virus; 14-21 days | Mild rash, enlarged **post-auricular nodes**; **congenital rubella syndrome** if in early pregnancy | Supportive; MR vaccine |
| **Chickenpox** | Varicella-zoster virus; 14-16 days | Itchy vesicles in crops, centripetal, all stages at once | Calamine, trim nails, **no aspirin**; aciclovir if high risk |
| **Mumps** | Paramyxovirus; 16-18 days | Painful **parotid swelling**; orchitis, meningitis | Supportive, rest, mouth care; (MMR not in Nepal NIP) |
| **Pertussis** | *Bordetella pertussis*; 7-10 days | Paroxysmal cough, **whoop**, post-tussive vomiting, apnoea in infants | **Azithromycin 10 mg/kg for 5 days**; DPT-HepB-Hib |
| **Diphtheria** | *Corynebacterium diphtheriae*; 2-5 days | Grey adherent **membrane**, "bull neck", myocarditis | **Antitoxin**, penicillin, isolation; vaccine |
| **Tetanus** | *Clostridium tetani* | Trismus, spasms, risus sardonicus; **neonatal** from cord | TIG, metronidazole, muscle relaxants, quiet room; Td in pregnancy |
| **Polio** | Poliovirus | **Acute flaccid paralysis**; Nepal reports every AFP under 15 years | No cure; bOPV and fIPV; Nepal is polio-free |
| **Typhoid** | *Salmonella* Typhi; 7-14 days | Step-ladder fever, relative bradycardia, rose spots, constipation or diarrhoea | Azithromycin or ceftriaxone (fluoroquinolone resistance is high in Nepal); **TCV at 15 months** |

**Measles** is the most infectious of all. The patient spreads it **from 4 days before to 4 days after the rash starts**. Complications are **otitis media, pneumonia (the commonest cause of death), diarrhoea, encephalitis, subacute sclerosing panencephalitis (years later), blindness (corneal ulcer in vitamin A lack) and malnutrition**. The **vitamin A dose** for measles is **200,000 IU for 12 months and over, 100,000 IU for 6-11 months and 50,000 IU under 6 months, on 2 consecutive days**, with a third dose 2-4 weeks later if there are eye signs. In Nepal every suspected case is reported through the **EWARS/case-based surveillance system** and contacts are checked for immunisation.

```svgfig label="4.1" caption="Course of measles and the infectious period. After 10-14 days of incubation, the prodrome of fever, cough, runny nose and red eyes lasts 3-4 days; Koplik spots appear 1-2 days before the rash; the rash begins on the face on day 4 and spreads down; the child is infectious from 4 days before to 4 days after the rash starts."
f = Fig(760, 320)
f.box(15, 12, 730, 30, "DAY OF ILLNESS (rash starts on day 4)", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
days = ["-4 to -1\nincubation\nends", "1\nfever, cough", "2\ncoryza, red\neyes", "3\nKoplik\nspots", "4\nrash on face\nand neck", "5\nrash to\ntrunk", "6\nrash to arms\nand legs", "8-10\nfades,\nbrownish"]
for i, d in enumerate(days):
    f.box(15 + i * 92, 54, 86, 66, d, fill=BLUE if i < 4 else ROSE, stroke=NAVY if i < 4 else RED, size=10, bold=True)
f.box(15, 134, 370, 34, "INFECTIOUS: from 4 days before the rash ...", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(385, 134, 360, 34, "... to 4 days after the rash starts (isolate)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
comp = ["OTITIS\nMEDIA", "PNEUMONIA\n(main killer)", "DIARRHOEA,\nmalnutrition", "ENCEPHALITIS,\nSSPE", "BLINDNESS\n(vitamin A)"]
for i, c in enumerate(comp):
    f.box(15 + i * 148, 184, 140, 56, c, fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(15, 254, 730, 56, "CARE: isolate, vitamin A on 2 days, feed and fluids, treat fever, eye and mouth care, antibiotics only for\ncomplications, report the case, vaccinate contacts with MR within 72 hours", fill=MINT, stroke=TEAL, size=10.5, bold=True)
```

```photogrid label="4.2" cols="4" ratio="1.0" caption="Rash illnesses of childhood. (a) Measles rash: red, flat and raised spots that join on the back and buttocks. (b) Koplik spots: tiny white dots on a red cheek lining, seen before the rash. (c) Chickenpox in a girl: vesicles and scabs on the face in different stages. (d) Mumps: swelling of the parotid gland that lifts the earlobe."
@ photo id="nur13/measles" cap="Measles rash"
fit 1.0
focus 0.5 0.5
mark 0.5 0.45 "1"
key 1 (a) Confluent red rash on back and buttocks
@ photo id="nur13/koplik" cap="Koplik spots"
fit 1.0
focus 0.4 0.5
mark 0.25 0.7 "2"
key 2 (b) White spots on the inner cheek
@ photo id="nur13/varicella" cap="Chickenpox"
fit 1.0
focus 0.5 0.45
mark 0.65 0.5 "3"
mark 0.3 0.4 "4"
key 3 (c) Vesicle with a red base
key 4 (c) Dry crust of an older lesion
@ photo id="nur13/mumps" cap="Mumps"
fit 1.0
focus 0.5 0.5
mark 0.65 0.35 "5"
key 5 (d) Swollen parotid region
```

### Eight points of nursing care in measles

1. **Isolate the child and protect others.** Keep him in a separate, well-ventilated room until 4 days after the rash starts, and let only vaccinated carers attend. Measles spreads through the air to non-immune children and pregnant women. Tell the health post the same day.
2. **Give vitamin A.** Give 200,000 IU by mouth on day 1 and day 2 (100,000 IU if 6-11 months) and note it on the card. This lowers the risk of blindness and death by about half. Check the eyes daily.
3. **Control the fever.** Give paracetamol 15 mg/kg every 6 hours, tepid sponging and light clothes. A child with a very high fever may fit. Avoid aspirin because of Reye syndrome.
4. **Keep up fluids and feeding.** Breastfeed, give small and frequent soft feeds and extra fluids, and treat diarrhoea by Plan A or B. Mouth sores and nausea make him refuse food. Measles can quickly cause malnutrition.
5. **Give eye, mouth and skin care.** Clean the eyes with clean water or saline, use tetracycline ointment if there is pus, rinse the mouth with salt water and keep the skin clean and dry. Dim light is comfortable because the eyes hurt in light.
6. **Watch for complications.** Count the respiratory rate and check the ears, chest and consciousness every 4 hours. Report fast breathing (40 or more at 12-59 months), ear discharge, convulsions or drowsiness. Early antibiotics reduce deaths from pneumonia.
7. **Vaccinate and trace contacts.** Give MR to non-immune contacts within 72 hours, check the vaccine status of siblings and school mates and catch up the missing doses. This stops the outbreak.
8. **Teach the family.** Explain isolation, the signs of complications, the meaning of the vitamin A doses and the need for MR at 9 and 15 months for all children. Reassure them that most children recover in 7-10 days. Listen for fears and traditional beliefs, and answer them respectfully.

## 4.2 Fever, meningitis and seizures

**Fever in a child in Nepal.** IMNCI asks about the area: **malaria** (Terai and river valleys, mainly *P. vivax*; an RDS or smear confirms, treatment is chloroquine plus primaquine, and **artesunate IV 2.4 mg/kg at 0, 12 and 24 hours** for severe malaria), **dengue** (every year, from the Terai to Kathmandu and the hills), **typhoid, measles, scrub typhus, meningitis and urinary infection**. Always look for danger signs and a stiff neck.

**Dengue** begins with high fever, headache, pain behind the eyes, myalgia and a flushed rash. The **critical phase (days 3-7)** follows when the fever falls: leakage of plasma causes **abdominal pain, repeated vomiting, mucosal bleeding, lethargy, a rising haematocrit and a falling platelet count**, which may go on to shock. Treatment is **oral fluids and rest, paracetamol only (no aspirin or ibuprofen)**, and **careful IV crystalloid** for warning signs, with daily platelet and haematocrit checks. Control is by destroying *Aedes* breeding sites (containers, tyres) every week.

**Bacterial meningitis** shows fever, headache, vomiting, **neck stiffness, photophobia, drowsiness, seizures and a bulging fontanelle** in infants (an infant may only be irritable and feed poorly). The **lumbar puncture** shows turbid CSF with many white cells, high protein and low glucose. Give **ceftriaxone 100 mg/kg/day (50 mg/kg every 12 hours)** for 7-10 days with **dexamethasone** before or with the first dose, and treat shock, fits and low sodium. Complications are deafness, hydrocephalus, epilepsy and learning difficulty. The **Hib and pneumococcal vaccines** are the best prevention.

**Febrile seizure** occurs between **6 months and 5 years** with a fever above 38 °C, without CNS infection. A **simple** febrile seizure is generalised, lasts under 15 minutes and does not recur within 24 hours; a **complex** one is focal, longer or repeated. During a seizure: lay the child on his side, loosen clothing, **do not put anything in the mouth**, note the time, and give **rectal diazepam 0.5 mg/kg** (or buccal or IV lorazepam) if it lasts over 5 minutes. Then find the cause of fever. Paracetamol makes the child comfortable but does not prevent a recurrence. Teach parents that the risk of epilepsy is low (about 2%).

## 4.3 Systemic disorders

**Rheumatic fever and rheumatic heart disease.** An untreated group A streptococcal sore throat in a child aged 5-15 years can trigger rheumatic fever 2-3 weeks later. The **revised Jones criteria** need evidence of recent strep infection plus **two major** (carditis, polyarthritis, chorea, erythema marginatum, subcutaneous nodules) or **one major and two minor** (fever, arthralgia, raised ESR or CRP, long PR interval). Treatment is bed rest, **penicillin**, aspirin or naproxen for arthritis and steroids for carditis. **Secondary prevention** is **benzathine penicillin G 1.2 million units IM every 3-4 weeks (0.6 million units if under 27 kg)** for at least 5 years or until age 21, and longer after carditis. This is a major cause of heart valve disease in Nepali young adults.

**Nephrotic syndrome** is **heavy proteinuria (above 40 mg/m²/hour or urine protein:creatinine above 2), low albumin (below 2.5 g/dL), oedema and high cholesterol**, most often **minimal change disease** at 2-8 years. The child has **puffy eyes in the morning, then leg and abdominal swelling (ascites), frothy urine and weight gain**. The usual treatment is **prednisolone 60 mg/m²/day (maximum 60 mg) for 6 weeks, then 40 mg/m² on alternate days for 6 weeks**. Most children respond, but half relapse. **Complications** are infection (peritonitis, cellulitis), thrombosis, hypovolaemia and steroid effects. By contrast, **acute post-streptococcal glomerulonephritis** gives **tea-coloured urine, hypertension and oedema** 1-3 weeks after a throat infection or 3-6 weeks after impetigo, and is managed with salt and fluid restriction, antihypertensives, diuretics and penicillin.

```svgfig label="4.3" caption="Nephrotic syndrome pathway. Damage to the podocytes lets protein leak into the urine; low albumin lowers oncotic pressure, so fluid leaves the vessels and causes oedema and ascites; the kidney then holds salt and water, and the liver makes more cholesterol. Steroids repair the leak; the nurse weighs, measures urine protein and prevents infection."
f = Fig(760, 320)
f.box(15, 15, 170, 62, "PODOCYTE INJURY\nminimal change\n(age 2-8 years)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(210, 15, 170, 62, "PROTEINURIA\nfrothy urine\n(above 40 mg/m2/h)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(405, 15, 170, 62, "LOW ALBUMIN\nbelow 2.5 g/dL,\nlow oncotic pressure", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(600, 15, 145, 62, "OEDEMA\nface, legs,\nascites", fill=ROSE, stroke=RED, size=10.5, bold=True)
for x in (185, 380, 575): f.arrow([(x, 46), (x + 25, 46)], color=SLATE, sw=2)
f.box(15, 100, 730, 34, "Fluid shift lowers blood volume: kidney holds salt and water; liver makes more cholesterol; antibodies are lost", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
tr = ["PREDNISOLONE\n60 mg/m2/day\n6 weeks, then\n40 mg/m2 alternate\ndays for 6 weeks", "DIET\nnormal protein,\nno added salt\nwhile oedematous", "MONITOR\ndaily weight,\nabdominal girth,\nurine dipstick,\nBP, intake", "PROTECT\ninfection signs,\nvaccines (PCV),\nno live vaccine on\nhigh-dose steroids"]
for i, s in enumerate(tr):
    f.box(15 + i * 184, 152, 175, 112, s, fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(15, 276, 730, 34, "Relapse: protein 2+ on dipstick for 3 days. Remission: protein negative or trace for 3 days", fill=SAND, stroke=AMBER, size=10.5, bold=True)
```

**Acute lymphoblastic leukaemia (ALL).** ALL is the commonest childhood cancer, with a peak at **2-5 years**. Marrow failure gives **pallor, fever, bleeding and bone pain**, with enlarged lymph nodes, liver and spleen. The blood film and marrow show **blasts**. Treatment is multi-drug chemotherapy in phases (induction, consolidation, maintenance) over 2-3 years, with cure rates above 80% in good centres. Nursing care stresses **infection prevention (neutropenic precautions), mouth care, nutrition, safe handling of cytotoxic drugs, pain relief, transfusion safety and family support**; Kanti Children's Hospital and BP Koirala Memorial Cancer Hospital are the main referral points in Nepal.

**Thalassaemia major** (more common in the Terai, for example among the Tharu people) is an inherited lack of beta-globin chains. The child is **pale by 6 months, has jaundice, an enlarged spleen and liver, and thalassaemic facies**, and needs **regular transfusion every 3-4 weeks to keep haemoglobin above 9.5-10 g/dL** (10-15 mL/kg of packed red cells over 3-4 hours) and **iron chelation (for example deferasirox 20-30 mg/kg/day)** to prevent iron overload of the heart, liver and glands. A **bone-marrow transplant** can cure. Prevention is carrier screening and genetic counselling before marriage.

```photogrid label="4.4" cols="2" ratio="1.25" caption="Dengue and leukaemia. (a) The rash of dengue fever: red patches with small white 'islands' of normal skin. (b) A bone-marrow film of acute lymphoblastic leukaemia: many large purple blasts among the pale red cells."
@ photo id="nur13/dengue" cap="Dengue rash"
fit 1.25
focus 0.5 0.5
mark 0.4 0.5 "1"
mark 0.7 0.4 "2"
key 1 (a) Red area of the rash
key 2 (a) White island of unaffected skin
@ photo id="nur13/all" cap="ALL blood film"
fit 1.25
focus 0.5 0.5
mark 0.3 0.7 "3"
mark 0.55 0.35 "4"
key 3 (b) Blast cell with a large purple nucleus
key 4 (b) Normal red blood cells for size comparison
```

### Seven points of nursing care in nephrotic syndrome

1. **Weigh and measure daily.** Weigh each morning on the same scale before breakfast, measure the abdominal girth at the umbilicus, and chart fluid intake and urine output. Weight is the best sign of oedema. A rise of 500 g or more in 24 hours is reported.
2. **Test the urine and take blood pressure.** Test the first morning urine by dipstick daily and record the protein grade (negative, trace, 1+ to 4+). Check blood pressure every shift. Protein in the urine marks relapse, and high pressure can signal fluid overload or steroid effect.
3. **Give steroids correctly.** Give prednisolone in the morning with food, never stop it suddenly, and note moon face, mood change, high appetite and high pressure. A stopped steroid can cause adrenal crisis or relapse. Teach the family not to skip doses.
4. **Give the right diet.** Allow a normal-protein diet, no added salt while the child has oedema (no pickles or instant noodles) and enough calories. Restrict fluids only if ordered. Salt makes the child retain more water.
5. **Prevent infection.** Hand hygiene, protective isolation from sick children, early care for skin, and quick reporting of fever or belly pain. Low antibody levels and steroids make infection the most dangerous complication. Pneumococcal vaccine is given.
6. **Care for the skin and comfort.** Raise swollen legs on pillows, turn the child every 2 hours, and keep the scrotal skin clean and supported. Stretched, oedematous skin breaks easily. Gentle handling prevents sores.
7. **Teach home care and relapse recognition.** Teach urine testing at home, the diet, steroid tapering, vaccines (no live vaccines while on high-dose steroids), school return and the need to come back if the urine is frothy or the face puffs. Early detection of relapse allows early treatment. A good diary makes follow-up reliable.

## 4.4 Calculations

**Vaccine efficacy (VE) = (attack rate in the unvaccinated - attack rate in the vaccinated) ÷ attack rate in the unvaccinated × 100.** The **herd-immunity threshold = 1 - 1/R₀**; measles has an R₀ of 12-18, so over 92-95% must be immune. Child doses are **mg/kg × weight**. **Body surface area (Mosteller) = √(height in cm × weight in kg ÷ 3600)**, used for steroids in nephrotic syndrome. A blood transfusion for thalassaemia is **10-15 mL/kg of packed cells over 3-4 hours**.

```python
import math
kg = 11.5
print(f"Bikash: vitamin A 200,000 IU on 2 days = {2 * 200000} IU in total (2 capsules); paracetamol 15 mg/kg = {15 * kg:.1f} mg = {15 * kg / 25:.1f} mL of 125 mg/5 mL")
print(f"If chickenpox: aciclovir 20 mg/kg four times a day = {20 * kg:.0f} mg per dose, {20 * kg * 4:.0f} mg/day for 5 days")
aru, arv = 12.0, 1.2
print(f"Vaccine efficacy = ({aru} - {arv}) / {aru} = {(aru - arv) / aru * 100:.0f}%; relative risk {arv / aru:.1f}; herd-immunity threshold at R0 15 = {(1 - 1 / 15) * 100:.1f}%")
print(f"Meningitis: ceftriaxone 100 mg/kg/day for 12 kg = {100 * 12} mg/day = {100 * 12 / 2:.0f} mg every 12 h; rectal diazepam 0.5 mg/kg = {0.5 * 12:.0f} mg")
bsa = math.sqrt(90 * 12.5 / 3600)
print(f"Nephrotic child (90 cm, 12.5 kg): BSA {bsa:.3f} m2; prednisolone 60 mg/m2 = {60 * bsa:.1f} mg/day; 40 mg/m2 = {40 * bsa:.1f} mg on alternate days")
print(f"Thalassaemia 12 kg: 15 mL/kg = {15 * 12} mL over 4 h = {15 * 12 / 4:.0f} mL/h; severe malaria artesunate 2.4 mg/kg = {2.4 * 12:.1f} mg per dose, {3 * 2.4 * 12:.1f} mg in 3 doses")
```

```text
Bikash: vitamin A 200,000 IU on 2 days = 400000 IU in total (2 capsules); paracetamol 15 mg/kg = 172.5 mg = 6.9 mL of 125 mg/5 mL
If chickenpox: aciclovir 20 mg/kg four times a day = 230 mg per dose, 920 mg/day for 5 days
Vaccine efficacy = (12.0 - 1.2) / 12.0 = 90%; relative risk 0.1; herd-immunity threshold at R0 15 = 93.3%
Meningitis: ceftriaxone 100 mg/kg/day for 12 kg = 1200 mg/day = 600 mg every 12 h; rectal diazepam 0.5 mg/kg = 6 mg
Nephrotic child (90 cm, 12.5 kg): BSA 0.559 m2; prednisolone 60 mg/m2 = 33.5 mg/day; 40 mg/m2 = 22.4 mg on alternate days
Thalassaemia 12 kg: 15 mL/kg = 180 mL over 4 h = 45 mL/h; severe malaria artesunate 2.4 mg/kg = 28.8 mg per dose, 86.4 mg in 3 doses
```

## Formula and fact sheet

- **Measles:** incubation 10-14 days; infectious 4 days before to 4 days after the rash; vitamin A 200,000 IU (12 months or more), 100,000 IU (6-11 months), 50,000 IU (under 6 months) on days 1 and 2; MR at 9 and 15 months.
- **Other rashes:** rubella (post-auricular nodes), chickenpox (no aspirin), mumps (parotitis), pertussis (azithromycin), diphtheria (membrane, antitoxin), tetanus, polio (report every AFP), typhoid (TCV at 15 months).
- **Meningitis:** ceftriaxone 100 mg/kg/day with dexamethasone. **Febrile seizure:** 6 months-5 years, rectal diazepam 0.5 mg/kg after 5 minutes. **Dengue:** critical phase days 3-7, paracetamol only.
- **Rheumatic fever:** Jones criteria; benzathine penicillin 1.2 million units (0.6 million under 27 kg) every 3-4 weeks.
- **Nephrotic syndrome:** prednisolone 60 mg/m²/day × 6 weeks, then 40 mg/m² alternate days × 6 weeks. **Thalassaemia:** keep Hb above 9.5-10 g/dL; 10-15 mL/kg packed cells over 3-4 hours.
- **VE** = (ARU - ARV) ÷ ARU; **herd threshold** = 1 - 1/R₀.

## Chapter summary

- Measles is spread by air from 4 days before the rash; vitamin A, isolation, feeding, eye and mouth care and early treatment of complications save lives, and MR at 9 and 15 months prevents it.
- Rash illnesses and vaccine-preventable diseases are recognised by their features and prevented by the NIP.
- Fevers need a search for danger signs, malaria and dengue in season, and meningitis in a drowsy child; febrile seizures are managed by safe positioning and diazepam after 5 minutes.
- Rheumatic fever is prevented by penicillin; nephrotic syndrome is treated with steroids and watched by daily weight, urine protein and blood pressure; leukaemia and thalassaemia need long-term, family-centred care with infection and transfusion safety.

## Practice

```python
import math
mcq1 = 15 * 14 / 25                    # MCQ1 mL paracetamol for 14 kg
mcq2 = 100 * 9 / 2                     # MCQ2 ceftriaxone mg per 12-hourly dose
mcq3 = (10 - 2) / 10 * 100             # MCQ3 vaccine efficacy percent
mcq4 = (1 - 1 / 12) * 100              # MCQ4 herd-immunity threshold
mcq5 = 60 * 0.5                        # MCQ5 prednisolone mg
mcq6 = 0.5 * 16                        # MCQ6 diazepam mg
print(f"MCQ1 = {mcq1:.1f} mL; MCQ2 = {mcq2:.0f} mg; MCQ3 = {mcq3:.0f}%; MCQ4 = {mcq4:.1f}%; MCQ5 = {mcq5:.0f} mg; MCQ6 = {mcq6:.0f} mg")
```

```text
MCQ1 = 8.4 mL; MCQ2 = 450 mg; MCQ3 = 80%; MCQ4 = 91.7%; MCQ5 = 30 mg; MCQ6 = 8 mg
```

**MCQs (with reasons)**

1. A 14 kg child needs paracetamol 15 mg/kg using 125 mg/5 mL syrup. The volume is: (a) 4.2 mL (b) 6.0 mL (c) 8.4 mL (d) 10.5 mL.
2. A 9 kg infant has meningitis and needs ceftriaxone 100 mg/kg/day in two divided doses. Each dose is: (a) 225 mg (b) 450 mg (c) 900 mg (d) 1,800 mg.
3. The attack rate is 10% in the unvaccinated and 2% in the vaccinated. Vaccine efficacy is: (a) 20% (b) 60% (c) 80% (d) 98%.
4. For a disease with R₀ of 12, the herd-immunity threshold is about: (a) 50% (b) 83% (c) 91.7% (d) 99%.
5. A child with nephrotic syndrome has a BSA of 0.5 m². Prednisolone 60 mg/m²/day is: (a) 12 mg (b) 30 mg (c) 60 mg (d) 120 mg.
6. A 16 kg child has a seizure lasting 6 minutes. Rectal diazepam 0.5 mg/kg is: (a) 4 mg (b) 8 mg (c) 16 mg (d) 80 mg.
7. The vitamin A dose for measles in an 8-month-old baby is: (a) 50,000 IU (b) 100,000 IU (c) 200,000 IU (d) 400,000 IU.
8. Tea-coloured urine, hypertension and facial oedema 2 weeks after a sore throat suggest: (a) nephrotic syndrome (b) post-streptococcal glomerulonephritis (c) UTI (d) thalassaemia.

::: note Answers and rationales
**1. (c).** 15 × 14 = 210 mg ÷ 25 mg/mL = 8.4 mL. 4.2 mL is for 7 kg and 10.5 mL would be 18.75 mg/kg.
**2. (b).** 100 × 9 = 900 mg a day, so 450 mg twice daily. 900 mg is the daily total.
**3. (c).** (10 - 2) ÷ 10 = 80%. VE is the proportion of cases prevented, not the vaccinated attack rate.
**4. (c).** 1 - 1/12 = 0.917. A higher R₀ needs a higher immune fraction, so measles needs over 92%.
**5. (b).** 60 × 0.5 = 30 mg a day. 12 mg is wrongly using 24 mg/m² and 120 mg is double.
**6. (b).** 0.5 × 16 = 8 mg. 80 mg would be a ten-fold overdose with risk of apnoea.
**7. (b).** 6-11 months gets 100,000 IU; 200,000 IU is for 12 months and over.
**8. (b).** The nephritic picture (haematuria, hypertension, oedema) after strep infection is APSGN. Nephrotic syndrome gives heavy proteinuria without haematuria.
:::

**Short answer (3 marks): Differentiate nephrotic syndrome from acute glomerulonephritis.** Nephrotic syndrome has heavy proteinuria, low albumin, marked generalised oedema, high cholesterol, normal or low blood pressure and clear or frothy urine; it is commonly minimal change disease at 2-8 years and responds to steroids. Acute post-streptococcal glomerulonephritis follows a throat or skin infection after 1-6 weeks and gives haematuria (tea-coloured urine), hypertension, mild oedema and low urine output with mild proteinuria, and low C3. It usually heals by itself with salt restriction, diuretics, antihypertensives and penicillin.

**Short answer (3 marks): State the first aid of a febrile seizure.** Lay the child on his side on a soft, safe surface and loosen his clothes. Do not put anything in the mouth, do not hold him down and do not give water. Note the start time, the type of movement and the duration. If the seizure lasts over 5 minutes give rectal diazepam 0.5 mg/kg and call for help. After the fit, check temperature and airway, give paracetamol for comfort, look for the cause of the fever (meningitis, malaria) and calm the parents.

**Medium answer (5 marks): Explain the pathophysiology and medical management of nephrotic syndrome (Figure 4.3).** Injury of the podocytes (minimal change disease) makes the glomerular filter leak **protein**, mostly albumin. The urine becomes frothy with protein above 40 mg/m²/hour, the plasma albumin falls below 2.5 g/dL and the **oncotic pressure falls**, so water moves into the tissues as **oedema and ascites**. The lower blood volume makes the kidneys hold salt and water, and the liver produces more **cholesterol**. Management is **prednisolone 60 mg/m²/day for 6 weeks then 40 mg/m² on alternate days for 6 weeks**, a normal-protein diet with no added salt, diuretics or albumin only if severe, and treatment of infection (penicillin or ceftriaxone). Nursing watches daily weight, girth, urine protein, blood pressure and fluid balance, prevents infection and teaches home testing. Complications are infection, thrombosis, hypovolaemia and steroid effects.

**Long answer (10 marks): Bikash Rai, 2 years, 11.5 kg, unvaccinated against MR, has 4 days of fever (39.5 °C), cough, red eyes, Koplik spots and a new facial rash, with 4 loose stools and poor drinking. Calculate and write the management and nursing care plan.**

*Calculations.* Bikash has **measles** with early diarrhoea. His **vitamin A is 200,000 IU on day 1 and day 2 (400,000 IU in total, 2 capsules)**. **Paracetamol 15 mg/kg = 172.5 mg = 6.9 mL** of 125 mg/5 mL syrup, every 6 hours. If he later develops pneumonia, amoxicillin is added by weight. Measles vaccine has an efficacy of **90%** in a study where the attack rate was 12.0% in the unvaccinated and 1.2% in the vaccinated, and the group needs **93.3% immunity** (R₀ 15) to stop spread; this is why his siblings and neighbours must be checked.

*Management.* The nurse isolates Bikash until 4 days after the rash starts, gives vitamin A and paracetamol, and classifies the diarrhoea by IMNCI (no dehydration, Plan A with ORS and zinc 20 mg for 14 days). She counts the respiratory rate (40 or more would mean pneumonia), looks into the ears and eyes, and gives tetracycline eye ointment for any pus. She feeds him small meals and breast milk or cup milk, with an extra meal for 2 weeks, and records weight. The case is reported to the district health office for measles surveillance. The nurse and FCHV check all contacts and give MR within 72 hours to non-immune children aged 9 months and over. She teaches the mother danger signs (fast breathing, drowsiness, not drinking, fits) and arranges review in 2 days.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "He is burning hot." **O:** T 39.5 °C, irritable | **Hyperthermia** related to viral infection | **Thermoregulation:** temperature below 38 °C in 6 h | Paracetamol 172.5 mg (6.9 mL) q6h, tepid sponging, light clothes, fluids (lowers metabolic load, prevents fits) | T 37.8 °C at 6 h |
| **O:** measles on day 4 of illness, siblings unvaccinated | **Risk for infection transmission** related to airborne spread | **Infection status:** no secondary cases | Isolate to 4 days after rash, report the case, give MR to contacts within 72 h (breaks the chain) | No new cases in 3 weeks |
| **O:** 4 loose stools, poor drinking | **Risk for deficient fluid volume** related to diarrhoea and fever | **Hydration:** moist mouth, good urine output | ORS after each stool (50-100 mL), zinc, breastfeed, small frequent drinks (replaces losses) | No dehydration at day 3 |
| **S:** "He will not eat." **O:** sore mouth, 11.5 kg | **Imbalanced nutrition: less than body requirements** related to anorexia and mouth sores | **Nutritional status:** keeps weight, eats 3 meals | Soft, thick feeds, mouth rinses, extra meal for 2 weeks, weigh weekly (prevents post-measles malnutrition) | Weight 11.5 kg, eats 3 meals |
| **O:** red watery eyes, vitamin A lack risk | **Risk for impaired vision** (corneal injury) related to measles and vitamin A deficiency | **Sensory function:** clear cornea, no pus | Vitamin A 200,000 IU × 2 days, eye cleaning, ointment for pus, daily eye check (prevents blindness) | Eyes clear, no ulcer |
| **S:** "Is it dangerous?" **O:** mother anxious | **Deficient knowledge** (measles care, vaccines) | **Knowledge:** mother lists 4 danger signs and vaccine dates | Teach isolation, signs, MR at 9 and 15 months for siblings; teach-back (early return prevents death) | Mother names signs, siblings vaccinated |

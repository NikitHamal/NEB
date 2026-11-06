---
subject: Adult Nursing I
grade: BSc Nursing Year 2
unit: 2
title: Respiratory Nursing: Oxygen Therapy, Asthma, COPD, Pneumonia and Chest Drains
hours: 22
area: BSN 9 · Adult Nursing I · Unit 2
---

Breathlessness is among the commonest reasons an adult comes to a Nepali hospital. Cooking over a wood or dung fire in a closed kitchen, smoking cigarettes or bidi, dust and cold air all damage the lungs, and the health post nurse sees chronic cough every week. **COPD affects nearly one in five adults over 50 in some hill and valley surveys**, asthma flares in every cold season, and **pneumonia remains a leading cause of admission** at Bir, TUTH and the provincial hospitals. The nurse's first tasks are to recognise respiratory failure, give oxygen safely and keep the airway clear. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of a nebuliser mask on a training manikin, a pulse oximeter, a cuffed tracheostomy tube and a chest X-ray with lobar consolidation, and a line drawing of a two-bottle chest drain, plus four SVG figures.
- Respiratory assessment, pack-years, spirometry, the ABG compensation rule, oxygen devices and cylinder duration (eight nursing responsibilities).
- Asthma, COPD and pneumonia: causes, signs, treatment, GOLD grades, CURB-65, inhaler technique, and the eight points of chest-drain care.
- Model answers and a NANDA-I care plan for a man with a COPD exacerbation.
:::

## 2.1 Respiratory assessment and the numbers that matter

Ask about **dyspnoea** (grade it by what the patient can do: walking on level ground, stairs, dressing), **cough**, **sputum** (colour, amount, blood), **wheeze**, **chest pain** and **smoking history**. Look for the **respiratory rate** (normal 12-20 per minute), **use of accessory muscles**, **cyanosis**, **finger clubbing** and **pursed-lip breathing**. Measure **SpO2** by pulse oximeter (normal 95-100%; target 88-92% in a patient with chronic CO2 retention). The **chest X-ray**, **sputum for AFB and culture**, **spirometry** and **arterial blood gas (ABG)** complete the picture.

```python
sticks, years = 10, 30                          # bidi per day, years smoked
packyr = sticks / 20 * years                    # 20 sticks = 1 pack
fev1, fvc, pred = 1.4, 2.9, 2.8                 # litres, post-bronchodilator
ratio = fev1 / fvc; pct = fev1 / pred * 100
ph, pco2, hco3 = 7.30, 58, 30                   # chronic CO2 retainer
exp_hco3 = 24 + 0.35 * (pco2 - 40)              # chronic compensation rule
psi, factor, flow = 2000, 0.28, 6               # E cylinder, litres per psi, L/min
litres = (psi - 500) * factor; mins = litres / flow
fio2 = 21 + 4 * 3                               # nasal cannula 3 L/min
pf = 60 / 0.40                                  # PaO2 / FiO2
print(f"Pack-years = {sticks}/20 x {years} = {packyr:.0f}")
print(f"FEV1/FVC = {fev1}/{fvc} = {ratio:.2f} (below 0.70: obstruction); FEV1 = {pct:.0f}% of predicted: GOLD 2")
print(f"ABG pH {ph}, PaCO2 {pco2}, HCO3 {hco3}: chronic respiratory acidosis; expected HCO3 = 24 + 0.35 x ({pco2} - 40) = {exp_hco3:.1f}")
print(f"E cylinder: ({psi} - 500) x {factor} = {litres:.0f} L; at {flow} L/min lasts {mins:.0f} min")
print(f"Nasal cannula 3 L/min: FiO2 about 21 + 4 x 3 = {fio2}%; PaO2/FiO2 = 60/0.40 = {pf:.0f}")
```

```text
Pack-years = 10/20 x 30 = 15
FEV1/FVC = 1.4/2.9 = 0.48 (below 0.70: obstruction); FEV1 = 50% of predicted: GOLD 2
ABG pH 7.3, PaCO2 58, HCO3 30: chronic respiratory acidosis; expected HCO3 = 24 + 0.35 x (58 - 40) = 30.3
E cylinder: (2000 - 500) x 0.28 = 420 L; at 6 L/min lasts 70 min
Nasal cannula 3 L/min: FiO2 about 21 + 4 x 3 = 33%; PaO2/FiO2 = 60/0.40 = 150
```

A man who has smoked 10 bidi a day for 30 years has **15 pack-years**. Spirometry with FEV1 1.4 L and FVC 2.9 L gives **FEV1/FVC = 0.48**; because this is below 0.70 after a bronchodilator the diagnosis is COPD, and an FEV1 of **50% of predicted** is **GOLD grade 2**. For a pH of 7.30 with PaCO2 58 and HCO3 30, the expected bicarbonate in chronic compensation is **30.3**, which matches, so this is a chronic respiratory acidosis, not an acute one. An E cylinder at 2,000 psi gives **420 L usable**, which lasts **70 minutes at 6 L/min**. A nasal cannula at 3 L/min gives about **33% oxygen**, and a PaO2/FiO2 ratio of **150** shows moderate impairment of gas exchange (normal above 400).

## 2.2 Oxygen therapy

Oxygen is a drug: it has a dose, a target and side effects. **Indications** are a SpO2 below 94% (below 88% in COPD), acute breathlessness, shock, major trauma, acute coronary syndrome with hypoxia, carbon-monoxide poisoning and post-operative recovery. Devices are chosen by the flow needed and the accuracy of the fraction of inspired oxygen (FiO2). In **Nepal** oxygen comes from cylinders, from pipeline and **PSA plants** in larger hospitals and from concentrators in district hospitals, a lesson learnt strongly in the COVID-19 waves.

```photogrid label="2.1" cols="4" ratio="1.0" caption="Respiratory equipment. (a) A real oxygen mask with a nebuliser cup on a hospital training manikin: the drug is turned into a mist and breathed in. (b) A real finger pulse oximeter with its light sensor and display. (c) A real cuffed tracheostomy tube with its pilot balloon and flange. (d) A real chest X-ray with a hazy white patch (consolidation) at the right lower zone: pneumonia."
@ photo id="nur5/neb" cap="Nebuliser mask"
fit 1.0
focus 0.7 0.5
mark 0.60 0.52 "1"
mark 0.82 0.20 "2"
key 1 (a) Face mask: fits over nose and mouth, held with an elastic band
key 2 (a) Nebuliser cup: holds the liquid drug, driven by oxygen or air at 6-8 L/min
@ photo id="nur5/oxi" cap="Pulse oximeter"
fit 1.0
focus 0.55 0.5
mark 0.28 0.52 "3"
mark 0.65 0.40 "4"
key 3 (b) Display: SpO2 percentage and pulse rate; trust it only when the trace is steady
key 4 (b) Finger: warm the hand and remove nail polish for a correct reading
@ photo id="nur5/trach" cap="Tracheostomy tube"
fit 1.0
focus 0.5 0.5
mark 0.46 0.62 "5"
mark 0.82 0.48 "6"
mark 0.16 0.12 "7"
key 5 (c) Flange: sits on the neck and is tied with tapes (one finger should fit under the tape)
key 6 (c) Tube and cuff: the cuff seals the trachea, check its pressure (20-30 cm H2O)
key 7 (c) Pilot balloon: tells the nurse whether the cuff is inflated
@ photo id="nur5/lobar" cap="Pneumonia X-ray"
fit 1.0
focus 0.5 0.5
mark 0.15 0.38 "8"
mark 0.45 0.88 "9"
key 8 (d) Right lower zone: a hazy white patch where air has been replaced by pus and fluid
key 9 (d) Trachea: central; a shifted trachea suggests pneumothorax or collapse
```

```svgfig label="2.2" caption="Oxygen delivery devices ranked by the FiO2 they give. Choose the lowest device that keeps the SpO2 at target: nasal cannula for mild need, Venturi mask when exact low-flow oxygen is needed (COPD), simple face mask for moderate need, and non-rebreather bag mask for emergencies."
f = Fig(760, 200)
f.text(380, 14, "Flow (L/min) and approximate FiO2", size=12, color=NAVY, bold=True)
f.box(10, 28, 170, 70, "Nasal cannula\n1-6 L/min\nFiO2 24-44%", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(195, 28, 170, 70, "Venturi mask\nfixed 24-60%\n(colour valve)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(380, 28, 170, 70, "Simple face mask\n5-10 L/min\nFiO2 40-60%", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(565, 28, 185, 70, "Non-rebreather\n10-15 L/min\nFiO2 60-90%", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(30, 128), (730, 128)], sw=2.5, color=NAVY)
f.text(70, 150, "Low need", size=10.5, color=TEAL, bold=True); f.text(690, 150, "Emergency", size=10.5, color=RED, bold=True)
f.text(380, 182, "Target SpO2 94-98%; in COPD with CO2 retention 88-92%", size=11, color=NAVY, bold=True)
```

### Oxygen therapy: eight nursing responsibilities

1. **Check the order and the target.** Oxygen needs a prescription of device, flow and SpO2 target (94-98%, or 88-92% in COPD). A target prevents both hypoxia and the harm of too much oxygen. Record the flow and the SpO2 together at every observation.
2. **Choose and fit the right device.** Match the device to the need, fit it to the face and check that it is comfortable. A badly fitting mask leaks and gives much less oxygen than the dial says. Tell the patient why it is needed.
3. **Humidify when needed.** Oxygen from a cylinder is dry and dries the nose and mouth at flows above 4 L/min. Use a humidifier bottle with sterile water, and change it as per the hospital policy. Give mouth care and lubricant for the lips.
4. **Observe the patient, not only the monitor.** Watch the breathing rate, colour, effort, drowsiness and confusion in addition to the SpO2. Drowsiness in a COPD patient on oxygen may mean CO2 narcosis. Reduce the dose and call the doctor.
5. **Fire safety.** Oxygen supports burning; no smoking, matches, oil, grease or open flame near it. Post "No smoking, oxygen in use" signs and teach visitors; a spark in oxygen-rich air starts a fire fast.
6. **Cylinder safety.** Secure the cylinder upright in a trolley, open the valve slowly, check the gauge and use the formula to plan changes. Never use grease on the regulator and keep a full cylinder spare. Check that the cylinder is the correct colour and label.
7. **Protect the skin.** The tubing and the elastic band cause pressure sores on the cheeks and ears. Pad the ears, change the position of the tube and inspect the skin each shift. Clean or replace the device daily.
8. **Teach and prepare for home oxygen.** For long-term oxygen the family needs to know the flow, the hours (at least 15 hours a day), fire rules and when to call for help. Include them in the discharge plan and arrange a follow-up at the nearest health facility.

## 2.3 Asthma

**Asthma** is chronic airway inflammation with reversible narrowing: the airway wall swells, the muscle tightens and mucus plugs form. The result is **wheeze, cough (worse at night), chest tightness and breathlessness**. Triggers in Nepal include dust, smoke from cooking fires, cold air, pollen, respiratory infection, strong smells and some drugs (aspirin, beta-blockers). Severity is measured by the **peak expiratory flow rate (PEFR)** as a percentage of the predicted or personal best: **green zone above 80%, yellow zone 50-80%, red zone below 50%**.

**Acute severe asthma** is recognised by PEFR 33-50% of best, inability to speak a full sentence, respiratory rate over 25 and pulse over 110; **life-threatening** features are a silent chest, cyanosis, exhaustion, confusion and PEFR below 33%. Treatment: sit upright, **oxygen to keep SpO2 94-98%**, **nebulised salbutamol 2.5-5 mg** repeated, **ipratropium 0.5 mg**, **prednisolone 40-50 mg orally or hydrocortisone 100 mg IV**, and IV magnesium by the doctor if life-threatening. Drug volume from the vial: 2.5 mg from a 5 mg/mL solution is **0.5 mL**.

```svgfig label="2.3" caption="Asthma and COPD compared. Asthma is reversible, starts early and varies from day to day; COPD is largely fixed, starts after 40 and follows smoke exposure. Both are treated with inhaled bronchodilators; COPD also needs smoking and smoke cessation."
f = Fig(760, 230)
f.box(10, 10, 360, 34, "ASTHMA", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.box(390, 10, 360, 34, "COPD", fill=SAND, stroke=AMBER, size=12, bold=True)
rows = [("Onset in childhood or youth", "Onset after age 40"), ("Allergy, atopy, family history", "Tobacco, bidi, biomass smoke"), ("Night cough, variable wheeze", "Daily cough, sputum, breathless"), ("Reversible after salbutamol", "FEV1/FVC below 0.70 after bronchodilator"), ("Eosinophilic inflammation: steroid", "Fixed obstruction: bronchodilator first")]
for i, (a, b) in enumerate(rows):
    y = 54 + i * 34
    f.box(10, y, 360, 28, a, fill=SOFT, stroke=NAVY, size=10.5)
    f.box(390, y, 360, 28, b, fill=SOFT, stroke=AMBER, size=10.5)
```

### Inhaler and spacer technique: eight points to teach

1. **Prepare the inhaler.** Remove the cap, shake the pressurised inhaler and prime it if it is new or unused for a week. Check the dose counter. A cold, unshaken inhaler gives an uneven dose.
2. **Attach a spacer.** A spacer holds the mist so that more reaches the lungs and less sticks in the throat. Use it with every pressurised inhaler, especially for children and the elderly. Wash it in soapy water weekly and let it dry in air.
3. **Breathe out gently.** Empty the lungs before the puff, not into the device. This makes room for the drug. Sit or stand upright.
4. **Seal the lips and press once.** Put the mouthpiece between the teeth with the lips closed. Press the canister once as you start to breathe in slowly. One puff per breath, not several together.
5. **Breathe in slowly and hold.** Breathe in over 3-5 seconds, then hold your breath for 10 seconds if you can. The drug settles in the airways during the hold. Wait 30-60 seconds between puffs.
6. **Rinse the mouth after steroid inhalers.** Gargle with water and spit it out. This prevents oral thrush and a hoarse voice. It takes less than a minute.
7. **Know reliever and controller.** The blue reliever (salbutamol) is used for sudden symptoms; the controller (inhaled steroid) is used every day even when well. Needing the reliever more than twice a week means poor control. Never stop the controller on your own.
8. **Know the red flags.** If the reliever does not help within 10-15 minutes, speech is difficult, or lips are blue, go to the hospital at once. Keep the PEFR diary. Avoid smoke, dust and cold air.

## 2.4 Chronic obstructive pulmonary disease (COPD)

COPD combines **chronic bronchitis** (cough and sputum for 3 months in 2 consecutive years) and **emphysema** (destruction of alveolar walls) with airflow limitation that is not fully reversible. In Nepal the main causes are **smoking (cigarette and bidi) and biomass smoke from indoor cooking**, especially in women, with air pollution and past tuberculosis as contributors. Signs: chronic cough, sputum, breathlessness, wheeze, barrel chest, pursed-lip breathing, cyanosis, ankle swelling (cor pulmonale). **GOLD grades** use post-bronchodilator FEV1 as a percentage of predicted: **grade 1 at least 80%, grade 2 50-79%, grade 3 30-49%, grade 4 below 30%**; the 2025 GOLD report groups patients as A, B or E (E means 2 or more moderate exacerbations, or one needing hospital). **Treatment** is stopping smoking, long-acting bronchodilators (LAMA, LABA), short-acting bronchodilator for relief, vaccination, pulmonary rehabilitation and, in exacerbations, oxygen at **88-92%**, nebulised bronchodilators, prednisolone 40 mg for 5 days and antibiotics if sputum is purulent.

### COPD nursing care: eight points

1. **Controlled oxygen.** Give 24-28% by Venturi mask or 1-2 L/min by cannula and aim for SpO2 88-92%. Too much oxygen removes the hypoxic drive and CO2 rises. Report drowsiness at once.
2. **Teach breathing control.** Pursed-lip breathing (in through the nose for 2 counts, out through pursed lips for 4) keeps the airways open. Diaphragmatic breathing reduces effort. Practise at rest, then during activity.
3. **Position.** Sit the patient upright or leaning forward on a pillow-covered table. This lets the diaphragm and accessory muscles work. Avoid lying flat.
4. **Clear secretions.** Encourage fluids (unless heart failure), chest physiotherapy, steam inhalation as per policy and an effective cough. Record the colour, amount and smell of sputum. Send a sample for culture before antibiotics.
5. **Nutrition.** Breathlessness reduces eating; give small frequent meals rich in energy and protein, with fluids between. Weigh weekly. Weight loss predicts poor outcome.
6. **Energy conservation.** Plan rest between activities, keep needed items within reach and sit to wash. Pace walking. Increase activity slowly with rehabilitation.
7. **Stop smoking and smoke.** Give brief advice at every contact, refer to a quit service and teach the family to use an improved cookstove with a chimney. Quitting is the one action that slows the loss of lung function.
8. **Prevent exacerbation.** Give influenza and pneumococcal vaccine, teach early signs (more sputum, change of colour, more breathlessness) and an action plan, and make sure the inhaler technique is correct.

## 2.5 Pneumonia and the severity score

**Pneumonia** is infection of the lung's air spaces by bacteria (most often *Streptococcus pneumoniae*), viruses or other organisms. It gives **fever, cough with rusty sputum, pleuritic chest pain, fast breathing and crackles**; bronchial breathing and dullness appear when a lobe is consolidated (Figure 2.1d). Treat with oxygen, fluids, antipyretics and antibiotics given by the Nepal standard treatment protocol (for example amoxicillin for mild community-acquired disease; a cephalosporin with a macrolide in hospital). The **CURB-65 score** counts one point each for **C**onfusion, **U**rea above 7 mmol/L, **R**espiratory rate 30 or more, **B**lood pressure below 90/60 and age **65** or over: **0-1 treat at home, 2 consider admission, 3-5 severe, admit and consider ICU**.

```python
curb = 1 + 1 + 1 + 1 + 1                     # confusion, urea 8, RR 32, BP 85/50, age 70
print(f"CURB-65 = {curb}: severe, admit and consider ICU")
print(f"Salbutamol 2.5 mg from 5 mg/mL = {2.5 / 5:.1f} mL; prednisolone 40 mg from 5 mg tablets = {40 // 5} tablets")
cyl = (1800 - 500) * 0.28; print(f"Case cylinder: (1800 - 500) x 0.28 = {cyl:.0f} L; at 2 L/min = {cyl / 2:.0f} min = {int(cyl / 2 // 60)} h {int(cyl / 2 % 60)} min")
print(f"Case pack-years = 10/20 x 40 = {10 / 20 * 40:.0f}; FEV1/FVC = 1.2/2.7 = {1.2 / 2.7:.2f}")
```

```text
CURB-65 = 5: severe, admit and consider ICU
Salbutamol 2.5 mg from 5 mg/mL = 0.5 mL; prednisolone 40 mg from 5 mg tablets = 8 tablets
Case cylinder: (1800 - 500) x 0.28 = 364 L; at 2 L/min = 182 min = 3 h 2 min
Case pack-years = 10/20 x 40 = 20; FEV1/FVC = 1.2/2.7 = 0.44
```

The sample patient with all five features has a **CURB-65 of 5**. For the case below, a cylinder at 1,800 psi holds **364 L usable**, lasting **182 minutes (3 h 2 min) at 2 L/min**; the smoking history is **20 pack-years** and FEV1/FVC is **0.44**. A prednisolone dose of 40 mg from 5 mg tablets needs **8 tablets**.

## 2.6 Chest drain and tracheostomy care

A **chest drain** removes air (pneumothorax), blood (haemothorax) or pus (empyema) from the pleural space and lets the lung re-expand. The tube goes through an intercostal space into the pleura and is connected to a bottle with its tip **2-3 cm under water (the underwater seal)**. The bottle is kept **below chest level** and never lifted above it. **Tidaling** (water rising with inspiration and falling on expiration) shows that the tube is patent; **continuous bubbling** means an air leak; **no tidaling** means the lung has re-expanded or the tube is blocked or kinked.

```photogrid label="2.4" cols="2" ratio="1.0" caption="Chest-drain system. (a) A public-domain line drawing of the classic two-bottle drain: the patient's tube goes to the first bottle, the water seal and the vent allow air out, and the bottle stays below chest level. (b) The nurse's rules for the underwater-seal bottle."
@ photo id="nur5/icd" cap="Two-bottle chest drain"
fit 0.9
mark 0.30 0.50 "1"
mark 0.75 0.82 "2"
key 1 (a) Water level: tube tip 2-3 cm under water forms the seal
key 2 (a) Chest tube: leaves the pleura and runs down to the bottle
@ svg cap="Bottle rules"
f = Fig(300, 300)
f.box(10, 10, 280, 56, "Bottle below chest\nalways", fill=BLUE, stroke=NAVY, size=14, bold=True)
f.box(10, 76, 280, 56, "Tidaling: tube open\nBubbling: air leak", fill=MINT, stroke=TEAL, size=14, bold=True)
f.box(10, 142, 280, 56, "Clamp only to change\nthe bottle, briefly", fill=SAND, stroke=AMBER, size=14, bold=True)
f.box(10, 208, 280, 82, "Tube out of bottle:\nput end in sterile water,\ncall the doctor", fill=ROSE, stroke=RED, size=14, bold=True)
```

### Chest drain nursing care: eight points

1. **Keep the system closed and below the chest.** Tape every connection and keep the bottle on the floor in a stand. Lifting it above the chest lets fluid flow back into the pleura. Secure the tubing so it cannot be pulled.
2. **Check the water seal each shift.** Confirm the tube tip is under water, mark the fluid level and look for tidaling. Bubbling that is continuous means a leak. Report no swing or a sudden stop.
3. **Never clamp without an order.** Clamping a draining pneumothorax can cause a tension pneumothorax. Clamp only for the short time needed to change a bottle. Keep two clamps by the bed.
4. **Measure and record drainage.** Mark the level on the bottle with the time and the date each shift. Bright red blood over 200 mL an hour or sudden pus needs a doctor now. Note the colour.
5. **Position and move.** Sit the patient upright (semi-Fowler) and encourage deep breathing, coughing and arm movement on the affected side. Support the tube during walking. Early movement helps the lung re-expand.
6. **Dressing and skin.** Keep the occlusive dressing at the site clean, dry and sealed. Feel for air under the skin (surgical emphysema, crackling). Change the dressing by aseptic technique.
7. **Manage accidents.** If the tube comes out of the chest, cover the site with a sterile, vaseline gauze dressing taped on three sides and call the doctor. If the bottle breaks, put the tube end into sterile water. Keep a spare set at the bedside.
8. **Pain and psychology.** The tube hurts on breathing; give analgesia before physiotherapy. Explain to the patient and family why it is there. Teach the patient not to lie on the tube.

**Tracheostomy care** follows similar rules: keep the airway clear by suction (no more than 10-15 seconds, pre-oxygenate), clean the inner tube every shift, keep the tapes with one finger gap, keep spare tubes at the bed and humidify the air.

## Formula and fact sheet

- Pack-years = packs a day × years (20 cigarettes or bidi = 1 pack). COPD = post-bronchodilator FEV1/FVC below 0.70; GOLD 1 to 4 by FEV1 % predicted (80, 50, 30).
- Chronic compensation: expected HCO3 = 24 + 0.35 × (PaCO2 - 40); acute: HCO3 rises 1 per 10 mmHg of PaCO2.
- Cylinder duration (min) = (psi - 500) × factor ÷ flow; E cylinder 0.28 L/psi; FiO2 by cannula about 21 + 4 × L/min.
- PEFR zones: above 80% green, 50-80% yellow, below 50% red; CURB-65: 0-1 home, 2 consider admission, 3-5 severe.

## Chapter summary

- Assess the rate, effort, colour, SpO2 and sputum; use pack-years, spirometry and ABG to interpret the lungs.
- Oxygen is prescribed to a target (94-98%; 88-92% in COPD) and delivered by the lowest device that works, with fire and cylinder safety.
- Asthma is reversible and treated with reliever and controller; COPD is fixed and treated with bronchodilators, oxygen control, rehabilitation and smoke cessation.
- Pneumonia is graded by CURB-65; chest drains need a closed system below the chest, water-seal checks and no unordered clamping.

## Practice

**MCQs (with reasons)**

1. A man who smoked 20 bidi a day for 25 years has: (a) 5 pack-years (b) 25 pack-years (c) 50 pack-years (d) 500 pack-years.
2. A patient with PEFR 200 L/min whose predicted value is 400 L/min is at: (a) 25% (b) 50% (c) 80% (d) 200%.
3. A cylinder at 1,500 psi (E, factor 0.28) running at 4 L/min lasts about: (a) 40 min (b) 70 min (c) 105 min (d) 375 min.
4. PaO2 80 mmHg on an FiO2 of 0.40 gives a PaO2/FiO2 ratio of: (a) 32 (b) 120 (c) 200 (d) 320.
5. The SpO2 target for a COPD patient who retains CO2 is: (a) 94-98% (b) 88-92% (c) 80-85% (d) 100%.

::: note Answers and rationales
**1. (b).** 20 bidi is one pack, so 1 × 25 = 25 pack-years; (c) wrongly treats each year as 2 packs.
**2. (b).** 200 ÷ 400 × 100 = 50%: yellow-red border, treat as an acute attack; (a) inverts the ratio.
**3. (b).** (1,500 - 500) × 0.28 = 280 L; 280 ÷ 4 = 70 min; ignoring the 500-psi reserve overestimates the time.
**4. (c).** 80 ÷ 0.40 = 200; a ratio below 300 shows impaired gas exchange.
**5. (b).** In chronic CO2 retention, high oxygen removes the hypoxic drive and CO2 rises; keep 88-92% with a Venturi mask.
:::

**Short answer (3 marks): CURB-65.** It is a pneumonia severity score. One point is given for confusion, urea above 7 mmol/L, respiratory rate of 30 or more, blood pressure below 90/60 and age of 65 or more. A score of 0-1 allows home treatment, 2 needs consideration of admission and 3-5 means severe pneumonia needing admission and possibly intensive care.

**Medium answer (5 marks): Describe the nursing care of a patient with a chest drain (Figure 2.4).** Keep the system closed, taped and the bottle below the chest level. Check the tube tip is 2-3 cm under water and look for tidaling; continuous bubbling means a leak. Never clamp without an order except briefly to change a bottle. Record the drainage with the time every shift and report bright red blood over 200 mL an hour or pus. Sit the patient upright, give analgesia, encourage deep breathing and arm exercises. Keep the dressing sealed and check for air under the skin. If the tube falls out, seal the site on three sides and call the doctor; if the bottle breaks, put the tube end in sterile water.

**Long answer (10 marks): Mr Ram Bahadur Karki, 62 years, a farmer, has smoked 10 bidi a day for 40 years and cooks on a wood fire. He is admitted to the medical ward with three days of increased breathlessness and green sputum. RR 28, SpO2 84% on air, pulse 106, BP 130/80, temperature 37.9 °C. Spirometry shows FEV1 1.2 L, FVC 2.7 L. ABG shows pH 7.30, PaCO2 58, HCO3 30. Plan his care.**

*Interpretation.* His smoking history is 10 ÷ 20 × 40 = **20 pack-years**; FEV1/FVC is 1.2 ÷ 2.7 = **0.44**, which is below 0.70, so COPD with an infective exacerbation. The ABG shows a chronic respiratory acidosis with partial renal compensation: he retains CO2, so the SpO2 target is **88-92%**, not 94-98%. Oxygen is given at 2 L/min by nasal cannula (FiO2 about 29%) or a 28% Venturi mask; a cylinder at 1,800 psi holds **364 L** and lasts **182 minutes** at that flow, so a spare must be ready.

*Care.* Sit him upright. Give nebulised salbutamol 2.5 mg (0.5 mL of 5 mg/mL) with ipratropium, driven by air (not oxygen) to avoid raising CO2. Give prednisolone 40 mg (8 tablets of 5 mg) and the antibiotic after a sputum sample is sent. Check the SpO2 and respiratory rate every 30 minutes at first, repeat the ABG after an hour, and watch for drowsiness. Teach pursed-lip breathing, help him clear his sputum and give fluids and a high-energy diet in small meals. Give mouth care, record his intake and output, and keep a fire-free area around the oxygen. Before discharge teach the inhaler and spacer technique, smoking cessation, an improved cookstove, vaccines and the early signs of another attack, and refer him to the nearest health post for follow-up.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** SpO2 84%, RR 28, pH 7.30, PaCO2 58. | **Impaired gas exchange** related to alveolar-capillary changes, as evidenced by hypoxaemia and hypercapnia. | **Respiratory status: gas exchange:** SpO2 88-92%, RR below 24 in 24 hours. | 1. Controlled oxygen 24-28%; *avoids loss of hypoxic drive.* 2. Upright position; *improves chest expansion.* 3. Bronchodilator nebuliser on air; *opens the airways.* | SpO2 90%, RR 22 at 24 hours. |
| **S:** "I cough and cannot get it up." **O:** green sputum, crackles. | **Ineffective airway clearance** related to retained secretions, as evidenced by cough and crackles. | **Respiratory status: airway patency:** coughs up sputum, chest clearer by day 3. | 1. Fluids and chest physiotherapy; *thins mucus.* 2. Teach huff and effective cough; *saves energy.* 3. Sputum culture and antibiotics; *treats the infection.* | Easy cough, clear sputum by day 3. |
| **S:** "I get tired walking to the toilet." | **Activity intolerance** related to imbalance between oxygen supply and demand. | **Energy conservation:** walks 20 m with SpO2 above 88% before discharge. | 1. Pace and rest; *lowers oxygen demand.* 2. Pursed-lip breathing; *reduces air trapping.* 3. Graded walking; *builds endurance.* | Walks 20 m without distress. |
| **S:** "I have smoked all my life." | **Deficient knowledge** about smoking cessation and inhaler use. | **Knowledge: illness care:** correct inhaler demonstration and a quit date before discharge. | 1. Teach technique with return demonstration; *confirms skill.* 2. Brief advice and quit-line referral; *raises quitting.* 3. Cookstove advice; *reduces smoke.* | Correct inhaler technique; quit date set. |

::: tip Exam tip
For a COPD case state the pack-years, the FEV1/FVC with GOLD grade, the 88-92% oxygen target, a nebuliser driven by air, and four NANDA-I diagnoses beginning with impaired gas exchange.
:::

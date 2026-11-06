---
subject: Adult Nursing II
grade: BSc Nursing Year 2
unit: 5
title: Oncology and Emergency Nursing: Cancer, Chemotherapy, Triage, Shock, Burns, Poisoning and Snakebite
hours: 18
area: BSN 10 · Adult Nursing II · Unit 5
---

Cancer and emergencies meet in the same Nepali hospital corridor. Most patients reach cancer care late, often after travelling from the hills to **B.P. Koirala Memorial Cancer Hospital (Bharatpur)**, the Bhaktapur Cancer Hospital, Nepal Cancer Hospital (Harisiddhi) or a hospital in Kathmandu, and **cervical, breast, lung, oral, stomach and gall-bladder cancers** lead the registry. Emergencies in Nepal include road crashes, burns from open fires and kerosene, **organophosphate pesticide poisoning**, snakebite in the Terai and landslide and earthquake disasters. The nurse who does the first 10 minutes well often decides the outcome. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of chemotherapy infusion bags on a pole, a mammogram showing a chemoport, a commercial tourniquet and triage of a casualty in a disaster drill, plus four SVG figures.
- Body surface area and chemotherapy doses, absolute neutrophil count, VIA screening yield, burn area and the Parkland formula, shock index and the atropine ladder.
- Eight points each on chemotherapy nursing care, cancer prevention teaching and organophosphate poisoning care.
- Model answers and a NANDA-I care plan for a woman with neutropenic fever on chemotherapy.
:::

## 5.1 Cancer: causes, warning signs, staging and treatment

**Cancer** is uncontrolled growth of cells that invade tissue and spread (metastasis). Causes in Nepal include **tobacco and bidi, chewing of tobacco and betel (oral cancer), alcohol, wood-smoke and air pollution (lung), HPV (cervical), hepatitis B and C (liver), Helicobacter pylori, salted and smoked foods (stomach) and late childbearing and obesity (breast)**. The warning signs are remembered as **CAUTION**: a Change in bowel or bladder habit, a sore that does not heal, Unusual bleeding or discharge, Thickening or lump in the breast or elsewhere, Indigestion or difficulty swallowing, Obvious change in a wart or mole, and Nagging cough or hoarseness (with weight loss and tiredness). **TNM staging** describes the tumour size (T), the lymph nodes (N) and metastasis (M). Treatment is by **surgery, radiotherapy, chemotherapy**, hormone therapy and targeted drugs, alone or together, and **palliative care** for the pain and symptoms of advanced disease; the national guideline gives morphine tablets and syrup at district level.

```python
import math
ht, wt = 165, 60                                 # cm, kg
bsa = round(math.sqrt(ht * wt / 3600), 2)        # Mosteller formula
cyc = 600 * bsa; dox = 60 * bsa                  # cyclophosphamide 600 mg/m2, doxorubicin 60 mg/m2
wbc, neut = 2500, 28                             # white count per mm3, neutrophils %
anc = wbc * neut / 100
screened, pos = 500, 45                          # VIA screening camp
rate = pos / screened * 100
print(f"BSA = sqrt({ht} x {wt} / 3600) = {bsa:.2f} m2")
print(f"Cyclophosphamide 600 x {bsa:.2f} = {cyc:.0f} mg; doxorubicin 60 x {bsa:.2f} = {dox:.1f} mg")
print(f"ANC = {wbc} x {neut}% = {anc:.0f} per mm3 (moderate neutropenia 500-1000; under 500 severe)")
print(f"VIA positive rate = {pos}/{screened} x 100 = {rate:.1f}%")
```

```text
BSA = sqrt(165 x 60 / 3600) = 1.66 m2
Cyclophosphamide 600 x 1.66 = 996 mg; doxorubicin 60 x 1.66 = 99.6 mg
ANC = 2500 x 28% = 700 per mm3 (moderate neutropenia 500-1000; under 500 severe)
VIA positive rate = 45/500 x 100 = 9.0%
```

A patient of 165 cm and 60 kg has a **BSA of 1.66 m²** (Mosteller formula). Cyclophosphamide at 600 mg/m² is **996 mg** and doxorubicin at 60 mg/m² is **99.6 mg**; two nurses must independently check every chemotherapy calculation against the height, weight and protocol before the drug is prepared. A white count of 2,500 with 28% neutrophils gives an **absolute neutrophil count of 700 per mm³**, moderate neutropenia, so the infection risk is high and the next cycle may be delayed. A VIA screening camp that finds 45 positives among 500 women has a **positive rate of 9.0%**, and these women need colposcopy or cryotherapy.

```svgfig label="5.1" caption="Cervical cancer screening in Nepal's national programme by visual inspection with acetic acid (VIA) for women aged 30-60 years. VIA negative: repeat in 3-5 years. VIA positive: if the lesion is small and the squamocolumnar junction is seen, treat the same day by cryotherapy; if the lesion is large or suspicious, refer for colposcopy, biopsy and LEEP or surgery. Adolescent girls receive HPV vaccine in the National Immunization Programme."
f = Fig(760, 250)
f.box(10, 90, 150, 70, "Woman aged 30-60\ncounselled and\nconsents", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(200, 90, 150, 70, "VIA: 3-5% acetic\nacid on cervix,\nlook after 1 minute", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(400, 20, 160, 56, "VIA negative:\nrepeat in 3-5 years,\nhealth education", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(400, 100, 160, 56, "VIA positive, small\nlesion: cryotherapy\nthe same day", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(400, 180, 160, 56, "Large or suspicious\nlesion: colposcopy,\nbiopsy, LEEP", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(600, 90, 150, 70, "Follow up at\n1 year; treat\ncancer by stage", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.arrow([(160, 125), (200, 125)], sw=2); f.arrow([(350, 125), (375, 125), (375, 48), (400, 48)], sw=1.8); f.arrow([(375, 125), (400, 128)], sw=1.8); f.arrow([(375, 125), (375, 208), (400, 208)], sw=1.8)
f.arrow([(560, 128), (600, 128)], sw=1.8); f.arrow([(560, 208), (680, 208), (680, 160)], sw=1.8)
```

### Chemotherapy: eight points of nursing care

1. **Check the order and the calculation.** Verify the protocol, the diagnosis, the height and weight, the BSA and the dose with a second nurse, and check the blood counts (ANC above 1,000 and platelets above 100,000 in most protocols). Chemotherapy has a narrow safety margin, so one wrong number can kill. Never give a drug when the check is not complete.
2. **Protect yourself and the environment.** Prepare drugs in a safety cabinet, wear gloves, a gown and eye protection, and dispose of the waste in a labelled cytotoxic bin. Cytotoxic drugs harm the nurse's cells too. Pregnant nurses should not prepare them. Body fluids of the patient are handled with gloves for 48 hours.
3. **Ensure a safe vein and watch for extravasation.** Use a fresh cannula in a large vein or a central line or a **port** (Plate 5.2b), and confirm a blood return before and during the infusion. Leakage of vesicant drugs (doxorubicin, vincristine) destroys tissue. If a patient reports burning, stop the drug, aspirate, call the doctor and follow the extravasation kit.
4. **Control nausea and vomiting.** Give antiemetics (ondansetron, dexamethasone, aprepitant for high-risk drugs) before the chemotherapy as ordered, and offer small, cool meals, ginger and mouth care. Uncontrolled vomiting causes dehydration and refusal of treatment. Record the intake and output.
5. **Prevent and manage infection (neutropenia).** The white count is lowest 7-14 days after the drug (the nadir). Wash hands, keep the patient in a clean room away from sick visitors, give cooked food and boiled water, and teach to take the temperature. **A temperature of 38 °C or more with a low neutrophil count is an emergency**: take cultures and give IV antibiotics within 1 hour.
6. **Care for the mouth and the skin.** Mucositis causes painful mouth sores, so use a soft toothbrush, saline or bicarbonate rinses and avoid hot and spicy foods. Report ulcers and thrush. Protect the skin from sun and give gentle care for the hand-foot reaction.
7. **Watch for bleeding, anaemia and fatigue.** Check platelets, report bruising, gum bleeding and black stools, and avoid IM injections and rectal temperatures. Plan rest periods and give blood or platelets as ordered. Teach the soft-brush and electric-shaver rule.
8. **Give emotional support and teaching.** Hair loss, fear of death and costs distress patients and families. Explain each side effect before it happens, offer a wig or scarf, involve the family and refer to the palliative care and social workers. Give written advice on when to call and what to eat.

### Cancer prevention and early detection: eight points of health education

1. **Stop all tobacco.** Smoking, bidi and chewing tobacco cause lung, mouth, throat, oesophagus and bladder cancer. Quitting at any age lowers the risk, and the nurse can offer brief advice and refer to the quitline. A smoke-free home protects children.
2. **Limit alcohol.** Alcohol raises the risk of cancer of the mouth, liver and breast. Advise little or none, and never together with tobacco. Support a patient to cut down.
3. **Eat and move well.** Eat plenty of vegetables, fruit, pulses and whole grains, less salt, pickles and smoked or burnt meat, and walk 30 minutes a day. A healthy weight lowers the risk of breast, colon and other cancers.
4. **Vaccinate.** HPV vaccine for girls and hepatitis B vaccine for infants in the NIP prevent cervical and liver cancer. Check that girls in the school-age group received the dose. Explain that the vaccine is safe.
5. **Screen women for cervical cancer.** Women of 30-60 years should have VIA or an HPV test every 3-5 years at a health facility, a camp or the hospital. Early lesions are treated the same day. Remind the family that a screening visit is free in many programmes.
6. **Examine the breasts.** Teach the monthly self-examination a week after the period, an annual clinical examination from the age of 40 and mammography where available. Report a lump, nipple discharge, dimpling or a change of the skin. Most lumps are not cancer but all need review.
7. **Look inside the mouth.** Tobacco and betel users should look for white or red patches (leukoplakia), ulcers over 2 weeks and difficulty in opening the mouth, and ask the health worker to examine. Early oral cancer is curable. Refer a patch that persists.
8. **Reduce infection and smoke exposure.** Use clean fuel or a chimney stove, wear a mask when working with dust, treat hepatitis B and H. pylori, use condoms and avoid sharing needles. Report to the doctor for any warning sign (CAUTION) without delay.

```photogrid label="5.2" cols="4" ratio="1.0" caption="Oncology and emergency nursing. (a) A real chemotherapy infusion: a red anthracycline bag and clear bags hang from an IV pole. (b) A real mammogram with a chemoport (a small implanted venous access device) visible in the upper breast. (c) A real commercial tourniquet with a windlass strap for life-threatening limb bleeding. (d) A real triage in a disaster drill: a responder in protective clothing checks a casualty and the triage tag."
@ photo id="nur6/chemo" cap="Chemotherapy infusion"
fit 1.0
focus 0.5 0.5
mark 0.72 0.72 "1"
mark 0.45 0.35 "2"
key 1 (a) Red bag: an anthracycline drug; a vesicant, so a secure line and a blood return are checked
key 2 (a) IV pole and line: clear fluid bags run before and after the drug to flush the vein
@ photo id="nur6/port" cap="Chemoport on mammogram"
fit 1.0
focus 0.5 0.3
mark 0.72 0.80 "3"
mark 0.60 0.30 "4"
key 3 (b) Chemoport: a small chamber under the skin joined to a central vein; needle only with sterile technique
key 4 (b) Fibroglandular tissue: the white, dense breast tissue seen on mammography
@ photo id="nur6/tourn" cap="Tourniquet"
fit 1.0
focus 0.5 0.5
mark 0.45 0.50 "5"
mark 0.10 0.62 "6"
key 5 (c) Windlass and buckle: twist until the bleeding stops, then lock; write the time on it
key 6 (c) Strap: apply 5-7 cm above the wound over the clothes, never over a joint
@ photo id="nur6/triage" cap="Triage in a drill"
fit 1.0
focus 0.5 0.5
mark 0.57 0.28 "7"
mark 0.78 0.78 "8"
key 7 (d) Triage tag: the colour (red, yellow, green or black) records the priority
key 8 (d) Responder: protective clothing; check airway, breathing, circulation and tag in under a minute
```

## 5.2 Emergency nursing: triage, primary survey and shock

**Triage** sorts casualties by urgency so that the most good is done for the most people. A four-colour system is used in disasters (Plate 5.2d) and a 5-level scale in the emergency department: **red (immediate)**: airway obstruction, severe bleeding, shock, breathing difficulty; **yellow (delayed)**: stable but serious, such as a fracture or a moderate burn; **green (minor)**: walking and talking; **black (expectant or dead)**: no breathing after the airway is opened. The **START** method counts the respiration rate (over 30 is red), perfusion (capillary refill over 2 s or no radial pulse is red) and mental status (cannot obey commands is red). The **primary survey** follows **ABCDE**: **A**irway with cervical spine protection, **B**reathing, **C**irculation with bleeding control, **D**isability (GCS, pupils, glucose) and **E**xposure with warmth. Life threats are treated as they are found. **Shock** is inadequate tissue perfusion; hypovolaemic shock (bleeding, burns, diarrhoea) is the commonest, with a **shock index (heart rate ÷ systolic BP)** above 0.9 suggesting significant blood loss.

```svgfig label="5.3" caption="START triage for adult casualties in a disaster (earthquake, landslide, bus crash). Walking wounded are green. If not breathing after the airway is opened: black. Breathing rate over 30, no radial pulse or capillary refill over 2 seconds, or cannot obey commands: red. All others: yellow. Re-triage as conditions change; tag every casualty and record the time."
f = Fig(760, 250)
f.box(300, 8, 160, 34, "Can walk? Move to green area", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(300, 58, 160, 34, "Breathing? Open the airway", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(10, 58, 150, 34, "Not breathing: BLACK", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.box(300, 108, 160, 50, "Rate over 30 a minute?\nRed", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(300, 168, 160, 34, "No radial pulse? Red", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(300, 212, 160, 34, "Cannot obey commands? Red", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(560, 120, 190, 70, "All others:\nYELLOW (delayed)\nre-triage often", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(380, 42), (380, 58)], sw=1.6); f.arrow([(300, 75), (160, 75)], sw=1.6); f.arrow([(380, 92), (380, 108)], sw=1.6)
f.arrow([(380, 158), (380, 168)], sw=1.6); f.arrow([(380, 202), (380, 212)], sw=1.6); f.arrow([(460, 190), (560, 160)], sw=1.6, dash=True)
```

```python
tbsa = 9 + 18 + 9                                # head 9 + anterior trunk 18 + left arm 9 (rule of nines)
wt = 70; total = 4 * wt * tbsa                   # Parkland: 4 mL x kg x %TBSA
first = total / 2; r1 = first / 8; r2 = first / 16
hr, sbp = 126, 84
si = hr / sbp
atr = 2 / 0.6                                    # atropine 2 mg from 0.6 mg/mL ampoule
cum = 2 + 4 + 8                                  # doubling every 5 minutes: 2, 4, 8 mg
adr = 0.5 / 1.0                                  # adrenaline 0.5 mg IM from 1 mg/mL
print(f"Burn area = 9 + 18 + 9 = {tbsa}% TBSA")
print(f"Parkland = 4 x {wt} x {tbsa} = {total:,.0f} mL in 24 h; first 8 h {first:,.0f} mL = {r1:.0f} mL/h; next 16 h {r2:.0f} mL/h")
print(f"Shock index = {hr} / {sbp} = {si:.1f} (over 0.9: significant blood loss)")
print(f"Atropine 2 mg from 0.6 mg/mL = {atr:.1f} mL IV; doubling 2 + 4 + 8 = {cum} mg total after three doses")
print(f"Adrenaline 0.5 mg IM from 1 mg/mL = {adr:.1f} mL (anaphylaxis, outer thigh)")
```

```text
Burn area = 9 + 18 + 9 = 36% TBSA
Parkland = 4 x 70 x 36 = 10,080 mL in 24 h; first 8 h 5,040 mL = 630 mL/h; next 16 h 315 mL/h
Shock index = 126 / 84 = 1.5 (over 0.9: significant blood loss)
Atropine 2 mg from 0.6 mg/mL = 3.3 mL IV; doubling 2 + 4 + 8 = 14 mg total after three doses
Adrenaline 0.5 mg IM from 1 mg/mL = 0.5 mL (anaphylaxis, outer thigh)
```

A burn of the head (9%), the front of the trunk (18%) and one arm (9%) covers **36% TBSA** by the rule of nines. In a 70 kg adult the **Parkland formula** gives 4 × 70 × 36 = **10,080 mL** of Ringer's lactate in 24 hours, half (**5,040 mL**) in the first 8 hours from the time of the burn (**630 mL/h**) and the rest over 16 hours (**315 mL/h**), adjusted to a urine output of 0.5 mL/kg/h (35 mL/h). A pulse of 126 with a systolic BP of 84 gives a **shock index of 1.5**, which means severe blood loss. Atropine 2 mg from a 0.6 mg/mL ampoule is **3.3 mL**, and doubling the dose every 5 minutes (2, 4, 8) reaches **14 mg** after three doses. Adrenaline 0.5 mg IM for anaphylaxis is **0.5 mL** of the 1 mg/mL (1:1000) solution into the outer thigh. Control of life-threatening limb bleeding uses direct pressure first and then a **tourniquet** (Plate 5.2c) 5-7 cm above the wound, noting the time of application; and never use a tourniquet for snakebite.

## 5.3 Poisoning and snakebite

**Organophosphate (OP) poisoning** is the commonest serious poisoning in rural Nepal, from pesticides drunk in self-harm or used without protection in the fields. OPs block **acetylcholinesterase**, so acetylcholine builds up at the nerve endings (Figure 5.4). The muscarinic signs are remembered as **SLUDGE** or **DUMBELS** (diarrhoea, urination, miosis, bronchorrhoea, bradycardia, emesis, lacrimation, salivation); nicotinic signs are twitching and paralysis, and the central signs are confusion and fits. The garlic-like smell of the clothes helps diagnosis. The main danger is **bronchorrhoea and respiratory failure**. Treatment is to remove clothes and wash the skin, protect the airway, give oxygen, atropine until the chest is clear, and observe for the intermediate syndrome (paralysis at 1-4 days). Every patient who has taken poison by choice needs a psychosocial assessment; **suicide prevention** and referral for mental health care are part of the nursing role.

```svgfig label="5.4" caption="Organophosphate poisoning. The pesticide blocks acetylcholinesterase, so acetylcholine builds up and over-stimulates muscarinic receptors (secretions, small pupils, slow heart, sweating) and nicotinic receptors (twitching, then paralysis). Atropine blocks the muscarinic receptors only; it does not reverse paralysis. The dose is given until the chest is clear, the heart rate is above 80 and the pupils are no longer pinpoint."
f = Fig(760, 240)
f.box(10, 90, 130, 60, "Organophosphate\n(pesticide)", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(180, 90, 140, 60, "Blocks\nacetylcholinesterase", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(360, 90, 130, 60, "Acetylcholine\nbuilds up", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(540, 20, 210, 70, "MUSCARINIC: sweating, saliva,\nwheeze and secretions, slow pulse,\nsmall pupils, vomiting, diarrhoea", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(540, 130, 210, 56, "NICOTINIC: twitching, weakness,\nparalysis of breathing muscles", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(540, 196, 210, 36, "Atropine blocks muscarinic effects", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(140, 120), (180, 120)], sw=2); f.arrow([(320, 120), (360, 120)], sw=2); f.arrow([(490, 105), (540, 60)], sw=1.8); f.arrow([(490, 135), (540, 158)], sw=1.8)
```

### Organophosphate poisoning: eight points of nursing care

1. **Protect yourself first.** Wear gloves, a gown and a mask or apron, because the pesticide is absorbed through the skin and can poison the nurse. Seal the clothes in a plastic bag and wash your hands. Ventilate the room.
2. **Remove the poison from the skin.** Take off all contaminated clothes and wash the skin and hair with soap and plenty of water. Wash the eyes with saline. Do this before anything else if the patient is stable.
3. **Secure the airway and give oxygen.** Position the patient on the side, suction the secretions often and give high-flow oxygen. Prepare for intubation if the patient is drowsy or tiring. Bronchorrhoea is the cause of death.
4. **Give atropine as ordered.** Start with 2 mg IV (3.3 mL of 0.6 mg/mL) and double every 5 minutes (2, 4, 8 mg: 14 mg in three doses) until the chest is clear, the pulse is over 80, the SBP over 80 and the pupils are no longer pinpoint. Then give an infusion of about 10-20% of the loading dose per hour. Watch for atropine toxicity (fever, delirium, no bowel sounds).
5. **Do gastric decontamination only when ordered.** Gastric lavage is considered within 1 hour only by a doctor, with a protected airway; activated charcoal may be given. Do not induce vomiting. Never lavage a drowsy patient with an unprotected airway.
6. **Monitor closely.** Record the respiratory rate, SpO2, pulse, BP, GCS, pupils and secretions every 15 minutes at first. Watch for the intermediate syndrome 24-96 hours later, with weak neck flexion and breathing muscles, and keep the ventilator ready. Check cholinesterase levels if available.
7. **Treat seizures and agitation.** Give diazepam for seizures and avoid drugs that worsen cholinergic effects (succinylcholine, morphine). Keep the patient safe in bed with a nurse present, since an agitated, atropinised patient may pull lines.
8. **Assess for self-harm and refer.** Ask about the reason, never leave a patient who took poison deliberately unobserved, involve the family, remove access to pesticide at home and refer to the psychosocial counsellor or psychiatric service before discharge. Teach safe storage and use of pesticides with protective clothing.

**Snakebite.** The Terai has the krait (neurotoxic), cobra (neurotoxic with local necrosis) and vipers (blood-clotting toxins). Give reassurance, immobilise the limb with a splint and a pressure immobilisation bandage for neurotoxic bites, remove rings and keep the patient still and move them to the hospital quickly; **do not cut, suck, tie a tight tourniquet, or apply herbs**. At the hospital, record the time, mark the swelling margin hourly, check the neurological signs (ptosis, difficulty in swallowing, breathing) and perform the **20-minute whole blood clotting test (20WBCT)**: put 2 mL of blood in a clean glass tube, leave it for 20 minutes and tilt; a failure to clot means coagulopathy. Give **polyvalent anti-snake venom** according to the MoHP protocol (for example 10 vials initially), with adrenaline and hydrocortisone ready for an anaphylactic reaction, and tetanus toxoid. Intubate for respiratory failure and use neostigmine with atropine only on the doctor's order. **Anaphylaxis** is treated by lying the patient flat with the legs raised, **adrenaline 0.5 mg IM (0.5 mL of 1 mg/mL)** in the outer thigh, repeated every 5 minutes, oxygen and IV fluids.

## Formula and fact sheet

- BSA (Mosteller) = √(height cm × weight kg ÷ 3600); chemotherapy dose = dose per m² × BSA; ANC = WBC × (neutrophil %) ÷ 100; below 500 is severe neutropenia.
- Parkland = 4 mL × kg × %TBSA, half in 8 hours and half in 16 hours; rule of nines: head 9, each arm 9, front trunk 18, back trunk 18, each leg 18, perineum 1; urine at least 0.5 mL/kg/h.
- Shock index = HR ÷ SBP (over 0.9 abnormal); START: rate over 30, no radial pulse or refill over 2 s, cannot obey commands: red.
- Atropine in OP poisoning: 2 mg then double every 5 minutes until the chest is clear; adrenaline 0.5 mg IM; 20WBCT: 20 minutes in a clean glass tube.

## Chapter summary

- Cancer is prevented by avoiding tobacco, vaccination and screening (VIA, breast and oral examination); chemotherapy nursing is double-checked dosing, safe veins, nausea control and neutropenic fever action.
- Triage sorts casualties as red, yellow, green and black, and the ABCDE survey finds and treats life threats in order.
- Burns are resuscitated by the Parkland formula and urine output; shock is detected early by the shock index.
- Organophosphate poisoning is treated by decontamination, airway and atropine until the chest is clear; snakebite needs immobilisation, the 20WBCT and anti-venom; a tourniquet is for limb bleeding, not for snakebite.

## Practice

**MCQs (with reasons)**

1. A 60 kg adult has a 20% TBSA burn. The Parkland volume to be given in the first 8 hours is: (a) 1,200 mL (b) 2,400 mL (c) 4,800 mL (d) 9,600 mL.
2. The same patient's hourly rate over the first 8 hours is: (a) 150 mL/h (b) 300 mL/h (c) 600 mL/h (d) 2,400 mL/h.
3. WBC 3,000 per mm³ with 20% neutrophils gives an ANC of: (a) 60 (b) 300 (c) 600 (d) 2,400.
4. A woman is 150 cm tall and weighs 54 kg. Her BSA by the Mosteller formula is: (a) 1.0 m² (b) 1.5 m² (c) 2.25 m² (d) 3.0 m².
5. A patient on chemotherapy has a temperature of 38.5 °C and a low neutrophil count. The first priority is: (a) paracetamol and observe at home (b) blood cultures and IV antibiotics within 1 hour (c) wait for the next clinic day (d) apply a hot pack.

::: note Answers and rationales
**1. (b).** Total = 4 × 60 × 20 = 4,800 mL; half is 2,400 mL in the first 8 hours; 4,800 mL is the 24-hour total and 1,200 mL is only one quarter.
**2. (b).** 2,400 ÷ 8 = 300 mL/h; 600 mL/h would empty the half-dose in 4 hours and 150 mL/h is the next 16-hour rate halved wrongly.
**3. (c).** 3,000 × 20% = 600; this is just above the severe cut-off of 500, so the risk of infection is high; 60 forgets the factor of 10.
**4. (b).** √(150 × 54 ÷ 3600) = √2.25 = 1.5 m²; 2.25 is the value before taking the square root.
**5. (b).** Neutropenic fever is sepsis until proved otherwise and mortality rises each hour without antibiotics; paracetamol alone masks the fever and delay is dangerous.
:::

**Short answer (3 marks): Triage.** It is the sorting of patients by urgency so that treatment goes first to those who most need it and can benefit. The four categories are red (immediate), yellow (delayed), green (minor) and black (expectant or dead), recorded on a tag; START uses breathing rate, circulation and ability to obey commands. Casualties are re-triaged as their conditions change.

**Medium answer (5 marks): Describe the nursing care of a patient with organophosphate poisoning (Figure 5.4).** *Safety and decontamination:* wear gloves and a gown, remove the contaminated clothes and wash the skin, hair and eyes with soap and water. *Airway and breathing:* position on the side, suction, give high-flow oxygen and prepare for intubation. *Antidote:* atropine 2 mg IV (3.3 mL of 0.6 mg/mL) and double every 5 minutes until the chest is clear, the pulse is above 80 and the pupils are not pinpoint; watch for toxicity. *Monitor:* respiration, SpO2, pulse, BP, GCS and secretions every 15 minutes and watch for the intermediate syndrome after 24-96 hours. *Psychosocial:* never leave a deliberate self-poisoning patient alone, involve the family and refer for mental health care; teach safe pesticide storage.

**Long answer (10 marks): Mrs Sunita Karki, 46 years, a teacher from Bharatpur with breast cancer, weighs 52 kg and is 158 cm tall. She received her first cycle of AC chemotherapy (doxorubicin 60 mg/m² and cyclophosphamide 600 mg/m²) 10 days ago. She comes to the emergency department with fever 38.5 °C, chills and a sore mouth. Pulse 108, BP 104/66 mmHg, WBC 1,800 per mm³ with 30% neutrophils. Calculate her doses and write the nursing care plan.**

*Calculations.* Her BSA is √(158 × 52 ÷ 3600) = **1.51 m²**. The cyclophosphamide dose was 600 × 1.51 = **906 mg** and the doxorubicin dose 60 × 1.51 = **90.6 mg**. Her ANC is 1,800 × 30% = **540 per mm³**, which is moderate, close to severe, neutropenia; with a temperature of 38.5 °C this is **neutropenic fever**. If hypotension develops, a fluid bolus of 30 mL/kg is 30 × 52 = **1,560 mL**, and the minimum urine output is 0.5 × 52 = **26 mL/h**.

*Care.* Place her in a single clean room with protective isolation and take her vital signs every 30 minutes for the first 2 hours. Take two sets of blood cultures (one from the port if present), a urine culture and a chest X-ray, and give the first dose of IV broad-spectrum antibiotic (such as piperacillin-tazobactam or a carbapenem as per hospital policy) within 1 hour. Insert an IV line, give saline as ordered, give paracetamol for comfort after the cultures, keep strict intake-output records and monitor lactate. Examine the mouth, the port site and the skin for the source of infection and examine and clean the mouth with a soft brush and saline. Do not give rectal drugs or temperatures, and keep the chemotherapy on hold pending the doctor's review. Offer boiled water and cooked food, give filgrastim only if ordered and explain every step to her and her husband. Before discharge, teach her to take her temperature twice a day and to return at once for 38 °C or more, to wash hands, take mouth care, avoid crowds and eat safe food, and arrange the next cycle with the oncologist.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I feel hot and shivering." **O:** T 38.5 °C, pulse 108, ANC 540. | **Risk for infection** (sepsis) related to chemotherapy-induced neutropenia, as evidenced by fever and ANC 540. | **Infection severity:** afebrile and cultures negative within 72 hours; no signs of sepsis. | 1. Cultures then IV antibiotic within 1 hour; *early treatment lowers mortality.* 2. Protective isolation and hand hygiene; *reduces new infection.* 3. Vital signs every 30 minutes, lactate; *detects sepsis.* 4. Avoid rectal drugs and IM injections; *prevents entry of bacteria.* | Temperature 37.2 °C at 48 hours, cultures negative, pulse 82. |
| **S:** "My mouth is sore; I cannot eat." **O:** mouth ulcers, lost 2 kg. | **Impaired oral mucous membrane integrity** related to chemotherapy, as evidenced by ulcers and pain. | **Oral hygiene:** ulcers healing, eats soft food within 5 days. | 1. Soft toothbrush, saline or bicarbonate rinse every 4 hours; *cleans without injury.* 2. Soft, cool bland food; *less pain.* 3. Topical analgesic and antifungal as ordered; *comfort and treats thrush.* 4. Avoid hot, spicy, acid foods; *prevents irritation.* | Ulcers reduced, eats soft rice and dal. |
| **O:** 108 pulse, BP 104/66, fever. | **Risk for deficient fluid volume** related to fever and poor intake. | **Fluid balance:** urine at least 26 mL/h; stable vital signs. | 1. Give IV and oral fluids as ordered; *replaces losses.* 2. Strict intake-output chart; *shows balance.* 3. Fluid bolus 1,560 mL if hypotensive; *treats septic shock.* 4. Daily weight; *tracks fluid status.* | Urine 40 mL/h, BP 112/70. |
| **S:** "Will I die? Is the treatment failing?" **O:** tearful. | **Anxiety** related to threat to life and an unfamiliar illness. | **Anxiety level:** states she feels calm and understands the plan. | 1. Explain neutropenic fever and the plan in simple Nepali; *knowledge lowers fear.* 2. Let her husband stay; *support.* 3. Refer to palliative and counselling services; *coping help.* 4. Teach when to call; *confidence.* | Calm, asks questions, can state the warning signs. |

::: tip Exam tip
For a cancer-chemotherapy case write the BSA, the dose calculation with a second-nurse check, the ANC, the neutropenic fever action in 1 hour and four NANDA-I diagnoses beginning with risk for infection and impaired oral mucous membrane integrity. For an emergency case write ABCDE, the Parkland or shock index figure and the antidote dose.
:::

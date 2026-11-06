---
subject: Integrated Health Sciences II
grade: BSc Nursing Year 1
unit: 5
title: Musculoskeletal and Integumentary Systems
hours: 30
area: BSN 2-3 · Integrated Health Sciences II · Unit 5
---

Bones, muscles and skin give shape, movement and the first barrier against infection. Nurses turn immobile patients, apply splints and crutches, dress burns and teach against osteoporosis and falls. In Nepal the 2015 earthquake (about 9,000 deaths and 22,000 injuries), road crashes, falls from hill terraces and kitchen-fire burns in women fill the orthopaedic and burn wards, so this unit pairs the structure of bone, joint and skin with fracture healing, the burn fluid calculation and the care of a patient with major burns.

::: key What this unit gives you
- A real bone micrograph, a real knee X-ray with a joint schematic, a real skin micrograph, a burn photograph and the rule-of-nines figure.
- Bone remodelling and fracture healing, joint types, and the muscle contraction cycle.
- Parkland burn fluid, rate per hour, drip rate, Curreri calories, T-score and crutch length, all computed and checked.
- Eight points on preventing osteoporosis and falls, and model answers with a full care plan for a patient with major burns.
:::

## 5.1 Bone, joints and the knee

The adult skeleton has 206 bones. A long bone has a **diaphysis** (shaft of compact bone around a marrow cavity), two **epiphyses** (spongy bone covered with articular cartilage) and a **periosteum** that carries blood vessels and nerves. Compact bone is built of **osteons (Haversian systems)**: concentric rings of matrix around a central canal, with **osteocytes** in the lacunae. **Osteoblasts** make bone, **osteoclasts** remove it, and remodelling keeps the balance under the control of calcium, vitamin D, parathyroid hormone and weight-bearing exercise. Children's bones grow at the **epiphyseal plate**, so a growth-plate injury needs an orthopaedic review.

A **synovial joint** such as the knee has articular cartilage, a joint capsule, synovial fluid, ligaments (cruciates and collaterals) and menisci. Knee flexion is normally about 135° and extension 0°. Arthritis wears the cartilage, and a total **knee replacement (arthroplasty)** puts a metal and plastic implant in its place, as seen in the X-ray below.

```photogrid label="5.1" cols="3" ratio="1.0" caption="Bone and joint. (a) Real ground section of compact bone: osteons with concentric rings and dark lacunae. (b) A real X-ray of a knee after replacement: the metal parts are white and the plastic spacer does not show. (c) The parts of a synovial joint."
@ photo id="nur2/bone" cap="Compact bone, ground section"
fit 1.0
focus 0.5 0.5
mark 0.45 0.55 "1"
mark 0.72 0.75 "2"
key 1 (a) Osteon: rings of matrix around a central Haversian canal
key 2 (a) Lacunae (dark dots) hold osteocytes in the matrix
@ photo id="nur2/knee" cap="Knee X-ray after replacement"
fit 1.0
focus 0.5 0.5
mark 0.42 0.60 "3"
mark 0.55 0.15 "4"
key 3 (b) White metal femoral and tibial components of the knee replacement
key 4 (b) Shaft of the tibia and fibula: dense compact bone looks white
@ svg cap="Synovial joint"
f = Fig(300, 300)
f.box(70, 10, 160, 50, "Femur (thigh bone)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(70, 240, 160, 50, "Tibia (shin bone)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(95, 70, 110, 22, "Articular cartilage", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(95, 208, 110, 22, "Articular cartilage", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(105, 118, 90, 60, "Synovial\nfluid and\nmeniscus", fill=MINT, stroke=TEAL, size=10, bold=True)
f.line(70, 90, 70, 210, color=RED, sw=4); f.line(230, 90, 230, 210, color=RED, sw=4)
f.text(36, 150, "Capsule", size=9.5, color=RED, bold=True); f.text(266, 150, "Ligament", size=9.5, color=RED, bold=True)
```

**Fracture healing** passes through four overlapping stages: haematoma (hours to days), soft callus of cartilage (week 1-3), hard callus of woven bone (week 3-12) and remodelling (months to years). Healing is slowed by smoking, diabetes, poor protein and calcium intake, infection, and movement at the fracture site. Complications nurses watch for are **compartment syndrome** (the 6 Ps: pain, pallor, pulselessness, paraesthesia, paralysis, pressure), **fat embolism** (breathlessness and petechiae 24-72 hours after long-bone fracture), infection, and **crush syndrome** after prolonged entrapment, as in the earthquake.

```svgfig label="5.1" caption="Fracture healing. Each stage depends on blood supply; immobilisation with a plaster cast or fixation protects the soft callus."
f = Fig(760, 180)
st = [("Haematoma\nhours to days:\nclot, swelling", ROSE, RED), ("Soft callus\nweeks 1-3:\ncartilage bridge", SAND, AMBER), ("Hard callus\nweeks 3-12:\nwoven bone", BLUE, NAVY), ("Remodelling\nmonths to years:\nlamellar bone", MINT, TEAL)]
for i, (t_, fc, sc) in enumerate(st):
    x = 10 + i * 187; f.box(x, 40, 165, 70, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    if i < 3: f.arrow([(x + 165, 75), (x + 187, 75)], color=SLATE, sw=2)
f.text(380, 22, "Stages of fracture healing", size=11, color=SLATE, bold=True)
f.text(380, 145, "Teach: no smoking, protein and calcium, vitamin D, correct crutch use, report increasing pain or numbness", size=10.5, color=TEAL, bold=True)
```

## 5.2 Skeletal muscle and movement

A muscle fibre is packed with **myofibrils** made of **actin** and **myosin** arranged in sarcomeres. A nerve impulse releases acetylcholine at the neuromuscular junction, calcium is freed from the sarcoplasmic reticulum, myosin heads bind actin and pull (the sliding filament mechanism using ATP). **Myasthenia gravis** is an antibody attack on the acetylcholine receptors, giving weakness that worsens with use. Long immobility causes muscle wasting (1-3% of strength per day on strict bed rest), so range-of-motion exercises and early mobilisation are nursing priorities. For **crutch walking**, the length is height minus 40 cm: a patient 170 cm tall needs crutches of **130 cm**, with the elbow bent 20-30° and the pad two fingers below the armpit.

## 5.3 The skin, burns and fluid resuscitation

The skin has the **epidermis** (keratinised stratified squamous epithelium renewed every 4 weeks), the **dermis** (collagen, vessels, nerves, glands) and the **hypodermis** (fat). It protects against germs, prevents water loss, regulates temperature, makes vitamin D and senses touch. Sweat glands and capillaries cool the body, and shivering warms it.

```photogrid label="5.2" cols="3" ratio="1.0" caption="Skin and burns. (a) A real skin section (H and E) with the layers named: keratin on the surface, epidermis, papillary and reticular dermis. (b) A superficial (first-degree) burn on a hand: red, dry, painful, no blisters. (c) Rule of nines for the adult: head 9, each arm 9, front trunk 18, back trunk 18, each leg 18, perineum 1."
@ photo id="nur2/skin" cap="Skin, H and E"
fit 1.0
focus 0.5 0.5
mark 0.80 0.90 "1"
mark 0.60 0.20 "2"
key 1 (a) Surface keratin and epidermis: the barrier, renewed every 4 weeks
key 2 (a) Dermis: collagen, small vessels and nerve endings
@ photo id="nur2/burn" cap="Superficial burn of the hand"
fit 1.0
focus 0.5 0.5
mark 0.42 0.38 "3"
mark 0.62 0.70 "4"
key 3 (b) Red, dry area: erythema of a superficial burn, painful to touch
key 4 (b) Unburnt skin of the fingers for comparison
@ svg cap="Rule of nines"
f = Fig(300, 330)
f.circle(150, 30, 22, fill=ROSE, stroke=RED, sw=2, label="9", size=12)
f.box(110, 58, 80, 110, "Front\ntrunk 18\n(back 18)", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(52, 62, 52, 100, "Arm\n9", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(196, 62, 52, 100, "Arm\n9", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(110, 172, 38, 130, "Leg\n18", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(152, 172, 38, 130, "Leg\n18", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(150, 318, "Perineum 1.  Palm of patient's hand = 1%", size=10, color=SLATE, bold=True)
```

Burns are graded by depth. **Superficial** (first degree) involves only the epidermis: red, painful, no blister, heals in 3-7 days. **Partial-thickness** (second degree) reaches the dermis: blisters, wet, very painful, heals in 2-3 weeks. **Full-thickness** (third degree) destroys the dermis: white, leathery, painless, and needs grafting. First aid is to remove the heat, **cool the burn with running tap water for 20 minutes**, remove rings and clothing not stuck to the skin, and cover with clean cling film or a clean cloth; never apply toothpaste, ghee or ice. Burns above 15% (10% in a child) cause burn shock, so fluid is given by the **Parkland formula**: 4 mL × weight (kg) × % total body surface area (TBSA) of Ringer's lactate in the first 24 hours, **half in the first 8 hours** from the time of the burn and half in the next 16 hours. The target urine output is 0.5 mL/kg/h in adults and 1 mL/kg/h in small children.

```python
wt, tbsa = 70, 40
total = 4 * wt * tbsa
first8 = total / 2
print(f"Parkland total = {total} mL RL in 24 h")
print(f"First 8 h = {first8:.0f} mL = {first8 / 8:.0f} mL/h")
print(f"Next 16 h = {first8:.0f} mL = {first8 / 16:.0f} mL/h")
tscore = (0.62 - 0.94) / 0.12
print(f"T-score = {tscore:.2f}")
print("Crutch length for 170 cm =", 170 - 40, "cm")
```

```text
Parkland total = 11200 mL RL in 24 h
First 8 h = 5600 mL = 700 mL/h
Next 16 h = 5600 mL = 350 mL/h
T-score = -2.67
Crutch length for 170 cm = 130 cm
```

For a 70-kg man with 40% TBSA the 24-hour need is 11200 mL, with 700 mL/h for 8 hours and then 350 mL/h. The same block shows the bone density **T-score** = (patient BMD − young adult mean) ÷ SD = (0.62 − 0.94) ÷ 0.12 = **-2.67**: a T-score of −2.5 or below is **osteoporosis**, −1.0 to −2.5 is osteopenia. The **Curreri formula** for a burn patient's calories is 25 kcal × weight + 40 kcal × %TBSA a day, and the diet is high in protein (1.5-2 g/kg) to heal the wound.

## 5.4 Preventing osteoporosis, fractures and falls: eight points

Hip fractures in the elderly are rising in Nepal as life expectancy increases, and women after menopause lose bone fastest. The nurse teaches these eight points at the OPD, in senior citizen groups and in the ward.

1. **Take enough calcium.** An adult needs about 1000 mg a day, and a woman after menopause 1200 mg. Milk, curd, small fish eaten with bones, green leafy vegetables (saag), soybean and sesame (til) give calcium. A glass of milk has about 300 mg, so three servings a day meet the need.
2. **Get vitamin D from sunlight.** Sit in the morning sun for 15-20 minutes on face and arms on most days. Vitamin D helps the gut absorb calcium. Veiled women, bedridden patients and people in smoky homes may need a supplement, which the doctor prescribes.
3. **Do weight-bearing exercise.** Walking, climbing steps, dancing and light lifting make bones stronger. Aim for 30 minutes on most days. Bones that are not loaded lose mass quickly, as in bed rest.
4. **Stop smoking and limit alcohol.** Tobacco and heavy alcohol reduce bone formation and slow fracture healing. Offer cessation advice at every visit. Raksi drinking also raises the risk of falls.
5. **Avoid long steroid use and check medicines.** Long prednisolone courses, some anti-epileptics and heparin weaken bone. Use the lowest dose for the shortest time, and add calcium and vitamin D. Never stop a steroid suddenly.
6. **Make the home safe against falls.** Fix loose mats, light the stairs and toilets, put a rail in the bathroom, and keep floors dry. Many Nepali homes have slippery steps and open fires. Use non-slip footwear and a stick when advised.
7. **Check eyesight, blood pressure and balance.** Poor vision from cataract, dizziness from BP tablets and weak legs are common causes of falls in the old. Send for eye care and review medicines. Teach getting up slowly from bed.
8. **Screen and treat early.** Women over 65 and those with earlier fractures, low weight or long steroid use should have a bone density test (DEXA) where available. A T-score of −2.5 or below needs treatment such as alendronate, taken with water while standing upright for 30 minutes. Teach that a minor fall with a wrist or hip fracture is a warning sign.

## Formula and fact sheet

- Parkland: 4 mL × kg × %TBSA of Ringer's lactate in 24 h; half in the first 8 h from the time of burn, half in the next 16 h. 70 kg, 40%: 11200 mL (700 mL/h, then 350 mL/h).
- Rule of nines (adult): head 9, each arm 9, front trunk 18, back trunk 18, each leg 18, perineum 1. Palm = 1%. Cool a burn 20 minutes.
- Urine target in burns 0.5 mL/kg/h (adult), 1 mL/kg/h (small child). Curreri calories = 25 × kg + 40 × %TBSA.
- T-score = (BMD − young mean) ÷ SD: -2.67 means osteoporosis (−2.5 or below). Crutch length = height − 40 cm (130 cm for 170 cm).
- Fracture healing: haematoma, soft callus, hard callus, remodelling. Compartment syndrome: 6 Ps.

## Chapter summary

- Bone is remodelled all life by osteoblasts and osteoclasts; compact bone is built of osteons.
- Fractures heal in four stages; the main dangers are compartment syndrome, fat embolism and infection.
- Muscle contracts by sliding filaments using calcium and ATP; bed rest wastes muscle fast.
- The skin has three layers and its loss in burns means fluid loss, infection and heat loss.
- Burn care is cooling, fluid by Parkland, pain control, nutrition and infection prevention.

## Practice

**MCQs (with reasons)**

1. The cells that remove bone are: (a) osteoblasts (b) osteocytes (c) osteoclasts (d) chondrocytes.
2. A T-score of −2.67 means: (a) normal bone (b) osteopenia (c) osteoporosis (d) Paget's disease.
3. A 70-kg man with 40% TBSA burns needs in the first 8 hours: (a) 2800 mL (b) 5600 mL (c) 11200 mL (d) 700 mL.
4. First aid for a thermal burn is to cool with running water for: (a) 2 minutes (b) 5 minutes (c) 20 minutes (d) 60 minutes.
5. The first sign of compartment syndrome is: (a) absent pulse (b) pain out of proportion (c) paralysis (d) pallor.

::: note Answers and rationales
**1. (c).** Osteoclasts resorb bone, osteoblasts form it, osteocytes maintain it and chondrocytes are cartilage cells.
**2. (c).** A T-score of −2.5 or lower defines osteoporosis; −1 to −2.5 is osteopenia.
**3. (b).** 4 × 70 × 40 = 11,200 mL in 24 h, half (5,600 mL) in the first 8 hours, which is 700 mL/h; option (d) is the hourly rate, not the 8-hour volume.
**4. (c).** Cooling for 20 minutes limits the depth of injury and eases pain; shorter cooling does less good and ice causes more damage.
**5. (b).** Pain out of proportion that is worse on passive stretch comes first; absent pulse, paralysis and pallor are late signs.
:::

**Short answer (3 marks): Rule of nines and Parkland formula.** The rule of nines estimates the burned area: head 9%, each arm 9%, front trunk 18%, back trunk 18%, each leg 18% and perineum 1%. The Parkland formula gives the fluid for 24 hours as 4 mL × weight (kg) × %TBSA of Ringer's lactate, with half in the first 8 hours from the time of burn. For 70 kg and 40% TBSA the total is 11200 mL, which is 700 mL/h for the first 8 hours. The rate is adjusted to a urine output of 0.5 mL/kg/h.

**Medium answer (5 marks): Describe the healing of a fracture and the nursing care of a patient in a plaster cast (Figure 5.1).** A fracture heals in four stages: a **haematoma** forms in hours, a **soft callus** of cartilage bridges the gap in weeks 1-3, a **hard callus** of woven bone replaces it in weeks 3-12, and **remodelling** restores lamellar bone over months. Healing needs blood supply, immobilisation, protein, calcium and vitamin D, and is slowed by smoking, diabetes and infection. In the cast, elevate the limb above heart level for 48 hours, keep the cast dry and uncovered until dry (24-48 hours), check the **5 Ps (pain, pallor, pulse, paraesthesia, paralysis)** and the colour and warmth of the fingers or toes every hour in the first day, and teach the patient not to push objects inside the cast. Report increasing pain, swelling, a foul smell or numbness at once because compartment syndrome needs the cast to be split. Encourage movement of unaffected joints and isometric muscle exercises.

**Long answer (10 marks): Sabina Magar, 28, 55 kg, is brought to the burn unit of a teaching hospital 2 hours after her clothes caught fire at the kitchen hearth. She has partial-thickness burns to the front of the trunk, the whole left arm and the front of the right leg. She is in severe pain, BP 100/60 mmHg, pulse 118/min, urine 10 mL in the last hour. Calculate her fluid and discuss her care.**

*Estimate and fluid.* By the rule of nines the burned area is 18 (front trunk) + 9 (left arm) + 9 (front of right leg) = **36% TBSA**. The Parkland total is 4 × 55 × 36 = **7920 mL** of Ringer's lactate in 24 hours: half, 3960 mL, in the first 8 hours from the burn (**495 mL/h**), and the rest at **247.5 mL/h** over the next 16 hours. Since 2 hours have already passed with no fluid given, the same 3960 mL must go in over the remaining 6 hours, which is 3960 ÷ 6 = **660 mL/h**; with a 20 drops/mL set this is 660 × 20 ÷ 60 = **220 drops/min**, though a pump is preferred. The target urine output is 0.5 × 55 = **27.5 mL/h**. Her calorie need by Curreri is 25 × 55 + 40 × 36 = **2815 kcal/day**, with 1.5-2 g/kg protein.

*Management.* Airway check (singed nasal hair, hoarseness), oxygen, two large IV lines, cool the wound if within the first 3 hours, remove jewellery, give IV morphine for pain, insert a urinary catheter, tetanus toxoid, and nasogastric feeding within 24 hours. Cover with clean sterile dressing (silver sulfadiazine or paraffin gauze), keep the room warm, and refer to the national burn unit. Observe for infection (Pseudomonas, Staphylococcus), contractures and the psychological trauma of disfigurement. In Nepal many such burns are from open hearths and kerosene, so household safety teaching is part of care.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** 36% TBSA, BP 100/60, pulse 118, urine 10 mL/h. | **Deficient fluid volume** related to loss through burned skin and capillary leak, as evidenced by hypotension, tachycardia and low urine. | **Fluid balance:** urine at least 28 mL/h, pulse below 100, BP above 100 systolic in 6 h. | 1. Ringer's lactate by Parkland at 660 mL/h (remaining 6 h) with a pump; *replaces capillary leak.* 2. Hourly urine through a catheter; *the best guide to perfusion.* 3. Adjust rate by 10-20% each hour as needed; *avoids overload or shock.* 4. Daily weight and electrolytes; *shows fluid trend.* | Urine and vitals hourly; goal met at urine 28 mL/h or more. |
| **S:** "it burns terribly." **O:** pain 9/10, grimacing, restless. | **Acute pain** related to tissue injury, as evidenced by self-report and facial expression. | **Pain level:** pain 3/10 or less within 30 min of analgesia. | 1. IV morphine in small doses as ordered, monitor RR; *burn pain is severe and needs opioids.* 2. Cover the wounds; *air exposure increases pain.* 3. Premedicate before dressings; *dressing change is the worst pain.* 4. Distraction and reassurance; *reduces anxiety.* | Pain score every 30 min until stable. |
| **O:** open partial-thickness wounds, WBC 15,000/mm³. | **Risk for infection** related to loss of skin barrier and immunosuppression. | **Infection status:** wounds clean, temperature below 38 °C for 14 days. | 1. Strict hand hygiene, gloves and sterile dressing technique; *the burn is a rich culture medium.* 2. Topical antimicrobial as ordered; *reduces bacterial growth.* 3. Isolation or single room; *prevents cross-infection.* 4. Monitor temperature and wound smell; *early sign of sepsis.* | Wound swab and temperature daily. |
| **S:** "will I look normal?" **O:** tearful, avoids looking at the wound. | **Disturbed body image and anxiety** related to burn injury and scars. | **Psychosocial adjustment:** talks about feelings and joins rehabilitation within 1 week. | 1. Listen without judgement and involve the family; *support lowers distress.* 2. Explain skin graft, pressure garments and physiotherapy; *gives hope.* 3. Refer to the psychosocial counsellor; *treats trauma.* | Patient takes part in dressing care and exercises. |

*Prevention and education.* Use closed stoves and raised hearths, keep children away from fire, never wear loose clothes near fire, store kerosene safely, and teach "stop, drop, roll". *Conclusion.* In major burns the nurse's priorities are airway, fluid by hourly urine, pain relief and infection control.

::: tip Exam tip
For any burn question write the rule-of-nines total, the Parkland total with the 8-hour and 16-hour rates and the urine target. Examiners award full marks for stating that fluid is counted from the time of burn, not from the time of arrival.
:::

---
subject: Adult Nursing II
grade: BSc Nursing Year 2
unit: 4
title: Musculoskeletal and Orthopaedic Nursing: Fractures, Casts, Traction, Compartment Syndrome and Osteoporosis
hours: 20
area: BSN 10 · Adult Nursing II · Unit 4
---

Bones break in Nepal because of its roads, its slopes and its work. Motorbike and bus crashes, falls from terraces, trees and roofs, and loads carried by porters on steep trails fill the orthopaedic wards of Bir Hospital, Patan, TUTH, the **Nepal Orthopaedic Hospital (Jorpati)** and the regional hospitals. The **2015 Gorkha earthquake injured over 22,000 people**, and the crush injuries, open fractures and amputations taught Nepali nurses that bone, wound and nerve care are one job. In the elderly, osteoporosis makes a fall at home a hip fracture. All arithmetic in this unit is checked by program.

::: key What this unit gives you
- Real photographs of a distal radius fracture on X-ray, a plaster splint on a forearm, a femoral external fixator and a girl walking with crutches and a walking boot, plus four SVG figures.
- The six Ps of neurovascular assessment, blood loss in fractures, traction weight, crutch length, compartment perfusion pressure and the bone-density T-score.
- Eight points each on fracture complications, cast and traction care, crutch walking and osteoporosis prevention.
- Model answers and a NANDA-I care plan for a young man with a femoral shaft fracture.
:::

## 4.1 Assessment, fractures and first aid

Assess **pain**, deformity, swelling, bruising, the position of the limb, movement, tenderness and **crepitus** (grating), and always examine the **neurovascular status** distal to the injury. A **fracture** is a break in the continuity of a bone. It is **closed** (skin intact) or **open/compound** (bone or the wound communicates with the outside; high risk of infection). By pattern it is **transverse, oblique, spiral, comminuted** (many pieces), **greenstick** (children), **impacted** or **avulsion**. The X-ray is taken in two views (Plate 4.2a). First aid is **to stop bleeding, splint the limb in the position found, cover open wounds with a clean dressing, give analgesia, keep the patient warm and move to hospital**; apply a splint that covers the joint above and below the fracture. For a suspected spinal injury, do not move the neck or back and use a log roll with a hard board.

```python
bmd, young, sd = 0.62, 1.00, 0.12                # g/cm2: patient, young adult mean, SD
t = (bmd - young) / sd
wt = 60; ebv = 70 * wt; loss = 1500              # femoral shaft fracture, blood lost in thigh (mL)
pct = loss / ebv * 100
dia, comp = 70, 45                               # diastolic BP and compartment pressure (mmHg)
dp = dia - comp
trac = 0.1 * wt                                  # starting traction about 10% of body weight
height = 170; crutch = height - 40               # crutch length (cm)
print(f"T-score = ({bmd} - {young}) / {sd} = {t:.1f}: osteoporosis (-2.5 or lower)")
print(f"Blood volume = 70 x {wt} = {ebv:,} mL; thigh loss {loss:,} mL = {pct:.1f}% (class III, over 30%)")
print(f"Compartment perfusion pressure = {dia} - {comp} = {dp} mmHg (30 or less: fasciotomy)")
print(f"Traction weight = 10% x {wt} kg = {trac:.0f} kg (as ordered by the surgeon)")
print(f"Crutch length = {height} - 40 = {crutch} cm; elbow bent 20-30 degrees")
```

```text
T-score = (0.62 - 1.0) / 0.12 = -3.2: osteoporosis (-2.5 or lower)
Blood volume = 70 x 60 = 4,200 mL; thigh loss 1,500 mL = 35.7% (class III, over 30%)
Compartment perfusion pressure = 70 - 45 = 25 mmHg (30 or less: fasciotomy)
Traction weight = 10% x 60 kg = 6 kg (as ordered by the surgeon)
Crutch length = 170 - 40 = 130 cm; elbow bent 20-30 degrees
```

A woman with a bone density of 0.62 g/cm² (young adult mean 1.00, SD 0.12) has a **T-score of -3.2**, which is osteoporosis (-2.5 or lower). A closed femoral shaft fracture can hide **1,000-1,500 mL** of blood; in a 60 kg adult (blood volume **4,200 mL**) a loss of 1,500 mL is **35.7%**, which is class III shock, so two IV lines and blood group and cross-match are needed. If the diastolic BP is 70 and the compartment pressure is 45, the **perfusion pressure is 25 mmHg**, below the threshold of 30, so the surgeon must perform a fasciotomy. A starting skeletal traction weight is about 10% of body weight, **6 kg** for 60 kg, as ordered, and the **crutch length for a patient of 170 cm is 130 cm**.

```svgfig label="4.1" caption="The six Ps of neurovascular assessment below a fracture, cast or tight bandage. Compare with the other limb: Pain out of proportion (the earliest sign of compartment syndrome), Pallor, Pulselessness, Paraesthesia (numbness, tingling), Paralysis and Poikilothermia (cold). Any new sign must be reported at once; do not wait for the pulse to disappear."
f = Fig(760, 230)
items = [("PAIN", "out of proportion,\nnot relieved by\nanalgesia, on stretch", ROSE, RED), ("PALLOR", "pale, mottled,\nslow capillary refill\n(over 3 s)", SAND, AMBER), ("PULSE", "weak or absent\n(late sign)", SAND, AMBER), ("PARAESTHESIA", "numbness,\ntingling, pins\nand needles", BLUE, NAVY), ("PARALYSIS", "cannot move\nthe fingers\nor toes (late)", ROSE, RED), ("POIKILOTHERMIA", "limb cooler\nthan the other\nside", BLUE, NAVY)]
for i, (h, t, fl, st) in enumerate(items):
    x = 8 + i * 124
    f.box(x, 20, 116, 34, h, fill=st, stroke=st, color="#ffffff", size=10, bold=True)
    f.box(x, 60, 116, 90, t, fill=fl, stroke=st, size=10, bold=True)
f.box(8, 170, 744, 46, "Action: loosen the bandage or split the cast, elevate to heart level (not higher), call the surgeon, record the time", fill=MINT, stroke=TEAL, size=11, bold=True)
```

### Fractures: eight early complications to watch for

1. **Haemorrhagic shock.** Pelvic and femoral fractures bleed a great deal into the tissue. Watch the pulse, BP, skin colour and urine, give oxygen and IV fluids and send for cross-match. A rising pulse is the first sign.
2. **Compartment syndrome.** Swelling inside a tight muscle compartment cuts off the blood supply and kills muscle in 4-6 hours. The earliest sign is pain that is out of proportion to the injury and worsens on passive stretch. Loosen the bandage, keep the limb at heart level and call the surgeon.
3. **Fat embolism.** Fat from the marrow of a long bone reaches the lungs 24-72 hours after the injury, causing breathlessness, confusion, a low SpO2 and petechiae over the chest and axillae. Give oxygen, monitor and call the doctor. Early fracture fixation lowers the risk.
4. **Deep vein thrombosis and pulmonary embolism.** Immobility and injury make clots in the calf or thigh. Give enoxaparin as ordered, use stockings, encourage ankle movements and early mobilisation, and report a swollen, painful calf or sudden breathlessness.
5. **Infection and osteomyelitis.** An open fracture, a pin site or surgery allows bacteria to reach the bone. Give tetanus prophylaxis and antibiotics as early as possible, use strict asepsis for dressings and report fever, pus or smell.
6. **Nerve and vessel injury.** The broken ends may cut or press on nerves and arteries (for example the radial nerve in a humerus fracture). Test the movement and the sensation of the fingers or toes and report a change. Compare both limbs.
7. **Delayed union, malunion and non-union.** Poor blood supply, infection, smoking, diabetes and movement at the fracture site slow bone healing. Teach the patient to stop tobacco, eat protein, calcium and vitamin D, and follow the weight-bearing advice. Check the X-rays on schedule.
8. **Pressure injury, constipation and complications of bed rest.** Immobility harms the skin, bowel, lungs and mood. Turn, give deep-breathing exercises, high-fibre food, fluids and company. Use a pressure-relieving mattress and keep the heels free.

```photogrid label="4.2" cols="4" ratio="1.0" caption="Orthopaedic nursing. (a) A real X-ray of a wrist with a displaced distal radius fracture. (b) A real plaster-slab splint with an elastic bandage on a forearm, with the fingers left free for neurovascular checks. (c) A real external fixator on a patient's femur: pins pass through the skin into the bone and are held by connecting rods. (d) A real patient walking with underarm crutches and a protective walking boot, taking weight through the hands."
@ photo id="nur6/radius" cap="Distal radius fracture"
fit 1.0
focus 0.5 0.5
mark 0.58 0.45 "1"
mark 0.42 0.74 "2"
key 1 (a) Fracture line through the end of the radius, with the broken end displaced backward
key 2 (a) Carpal bones: look at the alignment of the wrist for associated injury
@ photo id="nur6/cast" cap="Plaster slab on forearm"
fit 1.0
focus 0.5 0.35
mark 0.50 0.40 "3"
mark 0.45 0.82 "4"
key 3 (b) Slab and bandage: snug but never tight; two fingers should fit under the edge
key 4 (b) Fingers: leave free to check colour, warmth, movement and feeling every hour at first
@ photo id="nur6/exfix" cap="External fixator"
fit 1.0
focus 0.6 0.5
mark 0.62 0.60 "5"
mark 0.88 0.42 "6"
key 5 (c) Pins entering the skin: clean each pin site daily and watch for redness or pus
key 6 (c) Rods and clamps: hold the bone fragments aligned; never use them as a handle to lift the limb
@ photo id="nur6/crutch" cap="Crutch walking"
fit 1.0
focus 0.5 0.5
mark 0.50 0.10 "7"
mark 0.40 0.50 "8"
key 7 (d) Walking boot on the injured foot: protects the foot during healing
key 8 (d) Crutch handgrip: the hands carry the weight, not the armpits
```

### Cast and traction: eight points of nursing care

1. **Keep the cast dry and let it dry correctly.** A plaster of Paris cast takes 24-72 hours to dry; handle it with the palms, not the fingertips, which make dents and pressure points. Do not cover it with plastic or a blanket in the first hours. A wet cast softens and loses its support.
2. **Elevate the limb.** Raise the limb to heart level on pillows for the first 24-48 hours to reduce swelling, and ask the patient to move the fingers or toes every hour. Swelling inside a cast causes pressure and compartment syndrome.
3. **Do the neurovascular check.** Check the six Ps hourly in the first 24 hours and then every 4 hours. Compare with the other limb. Report any change at once and record the time.
4. **Protect the skin.** Pad the edges and prominences, and tell the patient not to put sticks, spoons or powder inside the cast to scratch. Itching can be eased by a hair dryer on a cool setting at the opening. Check for smell, wet patches and sores.
5. **Know the warning signs.** Teach the patient to report increasing pain, a tight feeling, swelling, numbness, a cold or blue finger or toe, a foul smell or a cracked cast. These need urgent review, not waiting until the next appointment.
6. **Keep traction working.** The weights must hang free and never rest on the floor or the bed; ropes must run in the pulleys; the patient must lie in line with the pull and the foot must not touch the end of the bed. Never remove the weights without an order. Keep the heel off the bed in skin traction.
7. **Care for pin sites and skin of traction.** Clean each pin site with normal saline or the unit's solution daily with sterile technique and record the drainage. Watch for redness, heat and pus. Check the skin under traction tapes and the peroneal nerve at the fibular head (foot drop).
8. **Prevent complications and support the patient.** Give deep-breathing exercises, ankle pumps, a high-fibre and high-protein diet with fluids, enoxaparin as ordered, and a trapeze to help moving. Give analgesia before movement, include the family in care and teach crutch use before discharge.

## 4.2 Fracture healing, surgery and rehabilitation

Bone heals in four overlapping stages: **haematoma** (hours to days: bleeding and inflammation), **soft callus** (1-3 weeks: cartilage and fibrous tissue bridge the gap), **hard callus** (3-12 weeks: woven bone) and **remodelling** (months to years: bone returns to shape). A child's forearm heals in 4-6 weeks, an adult's tibia in 3-6 months. Treatment is **reduction** (closed or open) followed by **immobilisation** (cast, traction, external fixator) or **internal fixation** (plates, screws, intramedullary nails). Surgeons use an external fixator (Plate 4.2c) for open fractures with soft-tissue damage, as in earthquake and road injuries, because it keeps the wound open for dressing. The nurse gives analgesia in steps: paracetamol 15 mg/kg, an NSAID such as diclofenac, and an opioid such as tramadol or morphine for severe pain.

```svgfig label="4.3" caption="The four stages of fracture healing. Stage 1 haematoma and inflammation (hours to 5 days): bleeding and clot at the break. Stage 2 soft callus (1-3 weeks): new capillaries and cartilage bridge the gap. Stage 3 hard callus (3-12 weeks): woven bone replaces cartilage and the fracture becomes stable. Stage 4 remodelling (months to years): the bone is reshaped along lines of stress."
f = Fig(760, 220)
st = [("1 Haematoma\nhours to 5 days", ROSE, RED, "pain, swelling"), ("2 Soft callus\n1-3 weeks", SAND, AMBER, "cartilage bridge"), ("3 Hard callus\n3-12 weeks", MINT, TEAL, "woven bone, stable"), ("4 Remodelling\nmonths to years", BLUE, NAVY, "bone reshaped")]
for i, (t, fl, s, n) in enumerate(st):
    x = 10 + i * 188
    f.box(x, 30, 170, 70, t, fill=fl, stroke=s, size=12, bold=True)
    f.text(x + 85, 122, n, size=11, color=s, bold=True)
    if i < 3: f.arrow([(x + 170, 65), (x + 188, 65)], sw=2)
f.arrow([(20, 160), (740, 160)], sw=2.5, color=NAVY)
f.text(380, 190, "Time: protect from stress early, add weight-bearing gradually; poor healing: smoking, diabetes, infection, movement", size=10.5, color=NAVY, bold=True)
```

### Crutch walking: eight points of teaching

1. **Fit the crutches.** The crutch tip should be 15 cm to the side and in front of the foot, the top 2-3 finger-breadths below the armpit and the handgrip at the level of the wrist, so the elbow bends 20-30°. For a patient of 172 cm the rule of height minus 40 cm gives **132 cm**. A wrong length causes nerve injury in the armpit.
2. **Bear weight on the hands.** The hands and arms carry the weight, never the armpits. Pressing on the top of the crutch can compress the radial nerve (crutch palsy). Wear shoes with a firm sole.
3. **Use the correct gait.** In the **three-point gait** (non-weight-bearing) both crutches and the injured leg move together, then the good leg; in the **two-point** and **four-point** gaits crutch and opposite leg alternate. The surgeon says which to use. Move slowly at first.
4. **Climb stairs safely.** Going up, lead with the good leg ("up with the good"); going down, lead with the crutches and the injured leg ("down with the bad"). Hold the rail with one hand and both crutches in the other. Stay with the patient for the first practice.
5. **Sit and stand safely.** To sit, back up to the chair, hold both crutches in one hand and lower slowly using the arm of the chair; to stand, reverse the steps. Never pull up on the crutches.
6. **Remove hazards.** Clear loose rugs, wet floors, stray wires and clutter in the house; paths in hill homes may be steep or muddy. Wear shoes at all times and use a handrail or a stick on a slope. Falls can break the fixation.
7. **Check the skin and the nerves.** Look for rubbing under the armpit and on the palms, and ask about tingling in the hands. Pad the top of the crutch. Report numbness.
8. **Follow the weight-bearing order.** The surgeon decides non-weight-bearing, touch, partial or full weight bearing. Stay within it until the X-ray shows healing. Return for follow-up and report new pain, swelling or fever.

## 4.3 Osteoporosis, osteomyelitis and arthritis

**Osteoporosis** is low bone mass with damaged structure, so bones break from small falls (hip, wrist and spine). Risk factors are age, female sex and menopause, low calcium and vitamin D, little exercise, smoking, alcohol, long steroid use and family history. The **DEXA scan** measures bone density as a **T-score**: normal is -1.0 or above, osteopenia -1.0 to -2.5 and osteoporosis -2.5 or lower. Treatment uses calcium, vitamin D, **alendronate 70 mg once a week** (taken with a full glass of water, on an empty stomach, standing for 30 minutes), zoledronic acid yearly, and fall prevention. A hip fracture in an elderly person needs surgery within 24-48 hours, early mobilisation and prevention of pressure injury, pneumonia and clots.

```python
wt = 60
para = 15 * wt                                   # paracetamol 15 mg/kg
diclo = 75 / 25                                  # diclofenac 75 mg from 25 mg/mL ampoule
cal = 1000; cup = 300                            # calcium need mg/day, mg per glass of milk
glasses = cal / cup
t2 = (0.75 - 1.00) / 0.10
print(f"Paracetamol 15 mg/kg x {wt} kg = {para} mg (1 g tablet = {para/1000:.1f} of a gram)")
print(f"Diclofenac 75 mg from 25 mg/mL = {diclo:.0f} mL IM, deep gluteal, not in a dehydrated patient")
print(f"Calcium {cal} mg/day: about {glasses:.1f} glasses of milk if one gives {cup} mg")
print(f"T-score = (0.75 - 1.00) / 0.10 = {t2:.1f}: at the border of osteoporosis")
```

```text
Paracetamol 15 mg/kg x 60 kg = 900 mg (1 g tablet = 0.9 of a gram)
Diclofenac 75 mg from 25 mg/mL = 3 mL IM, deep gluteal, not in a dehydrated patient
Calcium 1000 mg/day: about 3.3 glasses of milk if one gives 300 mg
T-score = (0.75 - 1.00) / 0.10 = -2.5: at the border of osteoporosis
```

A 60 kg patient needs paracetamol at 15 mg/kg, which is **900 mg** per dose (usually rounded to 1 g, four times a day at most, up to 4 g a day in adults). Diclofenac 75 mg from the 25 mg/mL ampoule is **3 mL**, and it is avoided in kidney failure, ulcer and dehydration. An adult needs **1,000 mg of calcium** a day, about 3.3 glasses of milk if one glass gives 300 mg, and a bone density of 0.75 with a young mean of 1.00 and SD 0.10 gives a T-score of **-2.5**, the border of osteoporosis.

### Osteoporosis: eight points of prevention and health education

1. **Eat enough calcium.** Adults need 1,000-1,200 mg a day; good Nepali sources are milk, curd, paneer, dried fish with bones, green leaves, soya and finger millet (kodo). Calcium builds the bone. Take calcium tablets with food if the diet is low.
2. **Get vitamin D.** Sit in morning sun for 15-20 minutes on the arms and face on most days, and eat eggs, oily fish and fortified foods. Women who cover fully need a supplement. Without vitamin D, calcium is not absorbed.
3. **Do weight-bearing exercise.** Walking, climbing stairs, dancing and light weights for 30 minutes on most days strengthen bone. Hill people who walk daily have an advantage. Balance exercises such as tai chi lower the risk of falls.
4. **Stop smoking and limit alcohol.** Tobacco and alcohol reduce bone formation and increase fracture risk. Offer help to quit (the MoHP tobacco quitline and counselling). Limit alcohol to a very small amount.
5. **Prevent falls at home.** Fix loose mats, add lights and handrails in the toilet and stairs, wear non-slip footwear, and treat poor vision. Falls in the dark in the village yard or on the toilet path are common. Review sedatives and blood pressure drugs.
6. **Review medicines.** Long-term steroids, thyroid over-dosing, some anticonvulsants and heparin thin the bone. Use the lowest effective dose and add calcium and vitamin D. Tell the doctor of all drugs.
7. **Take bisphosphonates correctly.** Take the weekly tablet with a full glass of water, on an empty stomach, and sit or stand for 30 minutes to prevent oesophageal irritation. Report chest pain or difficulty swallowing. Dental review is needed before starting.
8. **Screen and follow up.** Women after menopause and men over 70, and younger people with risk factors, should have a DEXA scan where it is available (Kathmandu, Pokhara and provincial hospitals). Follow the T-score and treat to prevent the first break. Teach the family to spot back pain and loss of height.

**Osteomyelitis** is bone infection (usually *Staphylococcus aureus*) from an open fracture, surgery or the blood. It causes fever, bone pain, swelling and a discharging sinus. The treatment is a long course of IV then oral antibiotics (4-6 weeks), drainage or debridement and immobilisation. **Rheumatoid arthritis** causes symmetrical swelling and morning stiffness of the small joints that lasts more than an hour; **osteoarthritis** causes pain on movement of the knees and hips that is better with rest; **gout** causes a hot, red big toe from uric acid crystals. Nurses teach joint protection, weight loss, exercise, heat for stiffness and the correct use of NSAIDs, methotrexate and allopurinol.

## Formula and fact sheet

- T-score = (patient BMD − young adult mean) ÷ SD; osteoporosis −2.5 or lower; the six Ps; compartment perfusion pressure = diastolic BP − compartment pressure (30 mmHg or less: fasciotomy).
- Blood volume = 70 mL/kg; class III shock is a loss of 30-40%; femoral shaft fracture hides 1,000-1,500 mL; traction weight about 10% of body weight as ordered.
- Crutch length = height − 40 cm; elbow flexion 20-30°; paracetamol 15 mg/kg; diclofenac 75 mg from 25 mg/mL = 3 mL; alendronate 70 mg weekly; calcium 1,000-1,200 mg/day.
- Healing: haematoma, soft callus, hard callus, remodelling; cast dries in 24-72 hours; check neurovascular status hourly at first.

## Chapter summary

- Fracture care begins with first aid, splinting and neurovascular checks; the six Ps detect compartment syndrome early.
- Cast and traction care keep the cast dry and the weights hanging free, protect pin sites and prevent bed-rest complications.
- Crutches bear weight on the hands, are measured as height minus 40 cm, and are taught with the correct gait and stair rules.
- Osteoporosis is prevented by calcium, vitamin D, exercise, fall prevention and no tobacco; the T-score of −2.5 defines it.

## Practice

**MCQs (with reasons)**

1. A woman has a bone density of 0.75 g/cm², a young adult mean of 1.00 and an SD of 0.10. Her T-score is: (a) −0.25 (b) −1.0 (c) −2.5 (d) −25.
2. A patient is 158 cm tall. By the height-minus-40 rule the crutch length is: (a) 98 cm (b) 108 cm (c) 118 cm (d) 128 cm.
3. Paracetamol 15 mg/kg is ordered for a 50 kg adult. The dose is: (a) 75 mg (b) 500 mg (c) 750 mg (d) 1,500 mg.
4. A starting skeletal traction weight of 10% of body weight for a 70 kg patient is: (a) 0.7 kg (b) 3.5 kg (c) 7 kg (d) 14 kg.
5. The earliest and most reliable sign of compartment syndrome is: (a) absent pulse (b) pain out of proportion to the injury, worse on passive stretch (c) paralysis (d) a cold limb.

::: note Answers and rationales
**1. (c).** (0.75 − 1.00) ÷ 0.10 = -2.5, the cut-off for osteoporosis; −0.25 forgets to divide by the SD and −25 divides by 0.01.
**2. (c).** 158 − 40 = 118 cm; 98 cm subtracts 60 and 128 subtracts only 30.
**3. (c).** 15 × 50 = 750 mg; 1,500 mg is 30 mg/kg and 75 mg is a tenfold error.
**4. (c).** 0.10 × 70 = 7 kg; 0.7 kg is a tenfold error and 14 kg is 20% of the body weight.
**5. (b).** Pain out of proportion appears first; pulselessness, paralysis and coldness are late signs and the pulse is often present until the muscle is dead.
:::

**Short answer (3 marks): Compartment syndrome.** It is raised pressure within a closed muscle compartment that reduces blood flow and kills muscle and nerve, mostly after a tibial or forearm fracture or a tight cast. The signs are pain out of proportion to the injury, pain on passive stretch, tense swelling and, late, pallor, paraesthesia and pulselessness. The treatment is to loosen the cast, keep the limb at heart level and perform an urgent fasciotomy if the perfusion pressure (diastolic minus compartment pressure) is 30 mmHg or less.

**Medium answer (5 marks): Describe the nursing care of a patient with a plaster cast (Figure 4.1).** *First 24-72 hours:* keep the cast uncovered and dry, handle it with the palms and elevate the limb to heart level. *Observe:* check the six Ps (pain, pallor, pulse, paraesthesia, paralysis and temperature) hourly at first and then every 4 hours, comparing with the other limb. *Skin:* pad the edges and teach the patient never to insert objects. *Teaching:* report pain, swelling, numbness, a cold or blue finger or toe, a smell or a crack; move the fingers or toes often; keep the cast dry. *Follow-up:* attend the clinic for the X-ray and the cast change, and begin exercises as advised.

**Long answer (10 marks): Mr Bishnu Prasad Rai, 28 years, a driver from Dhankuta weighing 62 kg, is brought to the emergency department of a regional hospital after a motorbike crash with a painful, swollen and shortened right thigh. He has a closed mid-shaft femoral fracture on X-ray, BP 100/60 mmHg, pulse 118, pain score 9/10, and the toes are warm with a palpable pulse. Calculate his blood loss and write the nursing care plan.**

*Calculations.* His blood volume is 70 × 62 = **4,340 mL**. If the thigh holds about 1,500 mL of blood, the loss is 1,500 ÷ 4,340 × 100 = **34.6%**, class III hypovolaemic shock, so rapid IV crystalloid and blood are needed. A starting skeletal traction weight of 10% of his body weight is **6.2 kg**, as ordered. His paracetamol dose of 15 mg/kg is **930 mg** (usually 1 g), and diclofenac 75 mg from the 25 mg/mL ampoule is 3 mL. For compartment checks after fixation, a perfusion pressure of diastolic 80 minus compartment pressure 50 is **30 mmHg**, which is at the limit, so the surgeon must be called and the readings repeated.

*Care.* Give oxygen, place two large IV cannulas, take blood for group and cross-match, haemoglobin and clotting and start crystalloid as ordered. Splint the thigh with a long splint (Thomas splint or traction) to reduce bleeding and pain, give IV analgesia and keep him warm. Check pulse, BP, SpO2, urine output and the six Ps of the right foot every 15 minutes until stable, then hourly. Give tetanus prophylaxis only if there is a wound. Keep him nil by mouth for surgery (intramedullary nailing). After surgery, give enoxaparin as ordered, start ankle exercises, deep breathing and early sitting, and teach three-point crutch walking with the **132 cm** crutch rule. Observe for fat embolism (confusion, breathlessness, petechiae) in the first 72 hours. Teach pin or wound care, calcium and protein diet, no smoking and a follow-up X-ray, and discuss the cost and return to work with the social worker and the family.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "The pain in my thigh is unbearable." **O:** pain 9/10, swollen shortened thigh, pulse 118. | **Acute pain** related to tissue and bone injury, as evidenced by pain score 9/10 and guarding. | **Pain level:** pain 3 or less within 1 hour and during dressing. | 1. IV analgesia as ordered, then regular paracetamol and NSAID; *breaks the pain cycle.* 2. Splint or traction; *immobilisation reduces pain.* 3. Support the limb with pillows when moving; *prevents movement of the fracture.* 4. Reassess pain every hour; *measures effect.* | Pain 3/10 at 1 hour; sleeps. |
| **O:** BP 100/60, pulse 118, estimated loss 34.6%. | **Risk for shock** (hypovolaemic) related to blood loss from the fractured femur. | **Hydration and circulation:** pulse below 100, SBP above 100, urine at least 0.5 mL/kg/h. | 1. Two IV lines, crystalloid and blood as ordered; *restores volume.* 2. Monitor pulse, BP, SpO2 and urine every 15 minutes; *early detection.* 3. Keep warm and flat with the leg splinted; *reduces loss.* 4. Cross-match and record the blood loss; *guides transfusion.* | Pulse 92, BP 118/72, urine 40 mL/h after 2 L and 1 unit. |
| **O:** foot warm, pulse present, risk after fixation. | **Risk for peripheral neurovascular dysfunction** related to fracture, swelling and traction. | **Tissue perfusion: peripheral:** six Ps normal; perfusion pressure above 30 mmHg. | 1. Check the six Ps hourly; *early detection of compartment syndrome.* 2. Keep the limb at heart level, loosen the bandage; *reduces swelling.* 3. Report pain out of proportion at once; *saves the muscle.* 4. Keep weights hanging free; *traction works.* | Toes warm, capillary refill 2 s, no neurological change. |
| **O:** traction, crutches planned, bed rest. | **Impaired physical mobility** related to fracture and traction. | **Mobility:** walks 20 m with crutches by day 5 after surgery without a fall. | 1. Ankle pumps and quadriceps exercises; *prevent clots and wasting.* 2. Physiotherapy and crutch fitting (height minus 40 cm); *safe walking.* 3. Teach three-point gait and the weight-bearing order; *protects the fixation.* 4. Remove home hazards; *prevents falls.* | Walked 25 m with crutches on day 5, no fall. |

::: tip Exam tip
For a fracture case write the blood volume and the percentage lost, the six Ps, the perfusion pressure rule, the traction weight and crutch length calculations and four NANDA-I diagnoses beginning with acute pain and risk for shock.
:::

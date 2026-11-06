---
subject: Fundamentals of Nursing
grade: BSc Nursing Year 1
unit: 2
title: The Nursing Process, NANDA-I Care Planning and Documentation
hours: 14
area: BSN 4 · Fundamentals of Nursing · Unit 2
---

The nursing process is the thinking method behind every nursing action, and the 5-column care plan is the most repeated 10-mark answer in nursing exams. This unit teaches the five steps, how to write a NANDA-I diagnosis, how to set an outcome and choose interventions, how to record, and then applies all of it to a real problem: the pressure injury.

::: key What this unit gives you
- The five steps: Assessment, Diagnosis, Planning, Implementation, Evaluation (ADPIE).
- Subjective versus objective data, and how to write a PES nursing diagnosis.
- SMART outcomes (NOC) and interventions (NIC) with a rationale for each.
- Eight principles of good documentation and SOAPIE charting.
- The Braden scale, the four stages of pressure injury, and eight prevention measures.
:::

## 2.1 The nursing process

The nursing process is a **systematic, cyclic, problem-solving method** of giving individualised care. It is cyclic because evaluation sends the nurse back to assessment.

```svgfig label="2.1" caption="The nursing process as a cycle. Each step has a product; evaluation loops back to assessment until the goal is met."
f = Fig(760, 250)
steps = [("1 Assessment", "collect data", MINT), ("2 Diagnosis", "name the problem", BLUE), ("3 Planning", "goals + orders", SAND), ("4 Implementation", "do and record", ROSE), ("5 Evaluation", "goal met?", MINT)]
x = 10
for t, s, c in steps:
    f.box(x, 40, 130, 56, t, fill=c, stroke=NAVY, size=12, bold=True, color=NAVY)
    f.text(x + 65, 118, s, size=11, color=SLATE)
    if x < 600: f.arrow([(x + 130, 68), (x + 148, 68)], color=SLATE, sw=2)
    x += 150
f.arrow([(675, 134), (675, 200), (75, 200), (75, 134)], color=TEAL, sw=2)
f.text(375, 222, "if not met or new problem: reassess, revise the plan", size=11.5, color=TEAL, bold=True)
f.text(75, 160, "data", size=10.5, color=SLATE); f.text(225, 160, "NANDA-I", size=10.5, color=SLATE); f.text(375, 160, "NOC + NIC", size=10.5, color=SLATE); f.text(525, 160, "action", size=10.5, color=SLATE)
```

## 2.2 Step 1: Assessment

Assessment is the collection, validation and organisation of data. **Subjective data** (symptoms) are what the patient says: "I feel dizzy." **Objective data** (signs) are what you observe or measure: pulse 112/min, skin cold. Sources are the patient (primary), family, the chart, the laboratory and other staff. Methods are interview, observation and physical examination (inspection, palpation, percussion, auscultation). Validate unclear data, for example by repeating a blood pressure on the other arm. Record in the patient's own words in quotation marks.

## 2.3 Step 2: Nursing diagnosis (NANDA-I)

A nursing diagnosis is a clinical judgement about a **human response** to a health problem that a nurse can treat independently. A medical diagnosis names the disease and is treated by the doctor.

| Point | Nursing diagnosis | Medical diagnosis |
|---|---|---|
| Describes | Human response to illness | Disease or pathology |
| Example | Impaired skin integrity | Pressure ulcer stage 2 |
| Treated by | Nursing interventions | Medical orders |
| Changes | Changes as the response changes | Stays while the disease lasts |

**PES format.** Problem (the NANDA-I label), Etiology ("related to") and Signs ("as evidenced by"): *Impaired skin integrity related to prolonged pressure and immobility, as evidenced by a 2 cm blister over the sacrum.* A **risk diagnosis** has no signs, only risk factors: *Risk for pressure injury related to immobility.* Never write the cause as a medical disease the nurse cannot treat ("related to stroke") when a nursing cause exists ("related to hemiplegia").

## 2.4 Step 3: Planning

Planning has four tasks: set **priorities** (life threats and ABC first, then Maslow's needs), write **outcomes** (NOC) that are SMART (specific, measurable, achievable, realistic, time-bound), select **interventions** (NIC) and write them as orders with a rationale, and document the plan. An example outcome: "Wound size reduced by at least 25% in 7 days." A poor outcome: "Patient will get better."

## 2.5 Steps 4 and 5: Implementation and evaluation

Implementation is carrying out the plan: independent (nurse-initiated, such as repositioning), dependent (on a doctor's order, such as giving an antibiotic) and collaborative (with physiotherapist or dietitian). Check the patient's condition first, protect the patient, and record immediately. Evaluation compares the patient's response with the outcome and decides: **goal met, partly met or not met**. If not met, ask why: was the assessment wrong, the plan unrealistic, or the intervention not done?

## 2.6 Documentation: eight principles

1. **Factual.** Record only what you saw, heard, measured or did; avoid words such as "seems" or "appears" without evidence. Opinions are not data. Facts protect the nurse in a legal case.
2. **Accurate.** Use correct numbers, spellings and units, and the patient's right name and bed number. A wrong decimal in a drug dose can kill. Check twice before you sign.
3. **Timely.** Write at the time of care or soon after, never before. Late entries are labelled as late. Memory fades within hours.
4. **Complete.** Include assessment, action, patient response and who was informed. A missing step looks like a missing action. Incomplete notes cannot continue care.
5. **Legible and permanent.** Use clear handwriting and blue or black ink; never use pencil or correction fluid. Correct a mistake with a single line, the word "error", your sign and the date. The original must remain readable.
6. **Signed.** Sign with name, designation and NNC registration number after each entry. An unsigned entry is of no value. Never sign for another nurse.
7. **Confidential.** The chart belongs to the hospital and is shared only with the care team. Do not discuss the chart in a corridor or on social media. Patients may read their notes with permission through the proper channel.
8. **Organised and in sequence.** Leave no blank lines between entries, and draw a line through unused space. Use accepted abbreviations only. The record then tells one story from admission to discharge.

**SOAPIE note:** **S** subjective, **O** objective, **A** assessment, **P** plan, **I** intervention, **E** evaluation.

## 2.7 Applying the process: the pressure injury

A pressure injury (pressure ulcer, bedsore) is localised damage to skin and underlying tissue from pressure, or pressure plus shear. It occurs over bony prominences: sacrum, heels, hips, elbows, back of the head. In Nepal it is common in stroke, spinal cord injury and elderly patients in district hospitals, where mattresses and nursing time are limited.

```photogrid label="2.1" cols="2" ratio="1.15" caption="Pressure injury. (a) A deep stage 4 sacral-area wound with exposed deeper tissue (the yellow box marks slough). (b) Skin layers and how far each stage reaches."
@ photo id="nur4/pu4" cap="Stage 4 pressure injury"
fit 1.15
call 0.50 0.93 0.62 0.60 "Deep crater, tissue loss"
call 0.50 0.07 0.28 0.45 "Wound edge"
@ svg cap="Depth of each stage"
f = Fig(300, 300)
bands = [("Epidermis", 30, 24, "#fde68a"), ("Dermis", 54, 46, "#fbcfe8"), ("Fat", 100, 66, "#fef3c7"), ("Muscle", 166, 60, "#fecaca"), ("Bone", 226, 40, "#e2e8f0")]
for n, y, h, c in bands:
    f.box(10, y, 160, h, n, fill=c, stroke=SLATE, size=11, color=NAVY, r=0)
for lab, x, y2 in [("1", 195, 36), ("2", 225, 80), ("3", 255, 140), ("4", 285, 240)]:
    f.arrow([(x, 30), (x, y2)], color=RED, sw=2)
    f.text(x, 22, "S" + lab, size=12, color=RED, bold=True)
f.text(150, 288, "S = stage; arrow tip = deepest tissue involved", size=10, color=SLATE)
```

```photo id="nur4/pu-stages" caption="Real photographs of pressure injury stages 1 to 4 (left to right): non-blanchable redness, partial-thickness loss with a shallow open area, full-thickness loss reaching fat, and a deep wound reaching muscle and bone." width="94"
crop 0 0.14 1 1
label 0.13 0.90 "Stage 1"
label 0.38 0.90 "Stage 2"
label 0.63 0.90 "Stage 3"
label 0.88 0.90 "Stage 4"
```

| Stage (NPIAP) | Description |
|---|---|
| 1 | Intact skin with non-blanchable redness |
| 2 | Partial-thickness loss, shallow open ulcer or blister |
| 3 | Full-thickness skin loss, fat visible, no muscle or bone |
| 4 | Full-thickness loss with exposed muscle, tendon or bone |
| Unstageable | Base covered by slough or eschar; depth unknown |
| Deep tissue injury | Persistent deep red, maroon or purple discoloration |

**Braden scale.** Six subscales are scored: sensory perception, moisture, activity, mobility and nutrition (1-4 each) and friction and shear (1-3). Total 6-23; the lower, the greater the risk: 9 or less very high, 10-12 high, 13-14 moderate, 15-18 mild.

::: example Worked example: Braden score
Mrs Sita, 72, on a stroke ward: sensory 2, moisture 2, activity 2, mobility 2, nutrition 3, friction/shear 1. Total = 2+2+2+2+3+1 = **12**, which is **HIGH** risk (10-12). A second patient scores 3, 3, 3, 3, 3, 2 = **17**, **MILD** risk (15-18). Repositioning every 2 hours means 12 turns in 24 hours, a turning chart with 12 signed rows.
:::

```svgfig label="2.2" caption="Braden score bands. Mrs Sita (12) sits in the high-risk band; a score of 17 is mild risk."
f = Fig(760, 150)
bands = [("6-9\nvery high", 20, 150, "#fecaca"), ("10-12\nhigh", 170, 150, "#fed7aa"), ("13-14\nmoderate", 320, 150, "#fef3c7"), ("15-18\nmild", 470, 150, "#d1fae5"), ("19-23\nno risk", 620, 120, "#e0f2fe")]
for t, x, w, c in bands:
    f.box(x, 30, w, 54, t, fill=c, stroke=SLATE, size=11.5, color=NAVY, bold=True, r=0)
f.poly([(245, 100), (235, 118), (255, 118)], fill=RED, stroke=RED); f.text(245, 136, "Mrs Sita = 12", size=11, color=RED, bold=True)
f.poly([(545, 100), (535, 118), (555, 118)], fill=TEAL, stroke=TEAL); f.text(545, 136, "Patient 2 = 17", size=11, color=TEAL, bold=True)
```

## 2.8 Prevention of pressure injury: eight points

1. **Risk assessment.** Score every admitted patient with the Braden scale on admission and repeat it daily or when the condition changes. A score of 12 or less starts the full prevention bundle. Early scoring prevents most injuries.
2. **Reposition every 2 hours.** Use a turning chart and the 30-degree side-lying position, so the weight is off the hip bone. Keep the head of the bed below 30 degrees unless feeding or breathing needs more. Sustained pressure for even a couple of hours can begin tissue damage.
3. **Pressure-relieving surfaces.** Use an alternating-pressure or foam mattress, and heel cushions. Avoid ring cushions, which concentrate pressure on the surrounding skin. In a district hospital even a folded blanket under the calves lifts the heels.
4. **Skin care.** Inspect the whole skin daily, wash with mild soap, dry gently and apply a barrier cream. Do not massage red areas, as that damages deeper tissue. Keep the bed linen dry and wrinkle-free.
5. **Moisture control.** Change wet linen at once, use pads for incontinence and clean the perineum after each episode. Wet skin is softer and breaks down more easily than dry skin. Offer the commode or bedpan on a schedule.
6. **Reduce friction and shear.** Lift, do not drag, the patient with a draw-sheet and two helpers. Raise the foot of the bed slightly to stop sliding down. Shear stretches the deep vessels that supply the skin.
7. **Nutrition and fluids.** Give a diet with protein, energy, vitamin C and zinc, and about 1.5-2 litres of fluid unless restricted. Weigh weekly and involve the dietitian. Malnourished patients in Nepal heal slowly even with perfect dressings.
8. **Education and documentation.** Teach the family to turn the patient and check the skin, because at home they are the nurses. Document the Braden score, each turn, skin findings and the education given. Records show the injury was preventable, or that it was present on admission.

## Formula and fact sheet

- ADPIE: Assessment, Diagnosis, Planning, Implementation, Evaluation.
- PES: Problem + Etiology + Signs. Risk diagnosis = Problem + risk factors.
- SMART outcome: Specific, Measurable, Achievable, Realistic, Time-bound.
- Braden range 6-23; at risk when 18 or less; turning every 2 h.

## Chapter summary

- The nursing process is a five-step cycle that individualises care.
- A nursing diagnosis names a human response that nurses treat; a medical diagnosis names a disease.
- A plan needs a measurable outcome, interventions and a rationale for each.
- Good records are factual, timely, signed and confidential.
- The Braden scale predicts, and the 2-hourly turn prevents, pressure injury.

## Practice

**MCQs (with reasons)**

1. The second step of the nursing process is: (a) assessment (b) diagnosis (c) planning (d) evaluation.
2. "Patient says: I feel nauseated" is: (a) objective data (b) subjective data (c) a nursing diagnosis (d) an outcome.
3. A Braden score of 11 means: (a) no risk (b) mild risk (c) high risk (d) very high risk.
4. The best-written outcome is: (a) patient will improve (b) patient will walk 20 metres with a walker by day 5 (c) nurse will turn patient (d) wound will heal.
5. Stage 3 pressure injury shows: (a) intact red skin (b) blister only (c) fat visible, no bone (d) bone exposed.

::: note Answers and rationales
**1. (b).** Diagnosis follows assessment. Planning is third and evaluation is last.
**2. (b).** A symptom reported by the patient is subjective. Objective data are measured or observed.
**3. (c).** 10-12 is high risk. 9 or less is very high and 13-14 is moderate.
**4. (b).** It is specific, measurable and time-bound, and it is about the patient. (c) is a nurse action; (a) and (d) are vague.
**5. (c).** Stage 3 is full-thickness skin loss with visible fat. Bone exposure is stage 4.
:::

**Short answer (3 marks): Differentiate nursing diagnosis from medical diagnosis.** A nursing diagnosis describes the patient's response to illness, is treated by independent nursing action and changes often, for example "Impaired skin integrity". A medical diagnosis names the disease, is treated by medical orders and stays the same during the illness, for example "Pressure ulcer stage 2". The nursing diagnosis uses NANDA-I labels and the PES format.

**Medium answer (5 marks): Explain the steps of the nursing process (Figure 2.1).** The nursing process has five steps. **Assessment** collects subjective and objective data from the patient, family, chart and examination, and validates them. **Diagnosis** analyses the data and states the problem in NANDA-I PES format. **Planning** sets priorities, writes SMART outcomes (NOC) and selects interventions (NIC) with rationale. **Implementation** carries out independent, dependent and collaborative actions and records them. **Evaluation** compares the response with the outcome and labels it met, partly met or not met; if not met the process restarts from assessment. The process is cyclic, patient-centred, continuous and gives a scientific basis to care. Example: for a patient with a Braden score of 12, the nurse assesses the skin, diagnoses risk for impaired skin integrity, plans 2-hourly turns, turns the patient, and evaluates the skin each shift.

**Long answer (10 marks): Mrs Sita Thapa, 72, bed-bound after a stroke, admitted in the medical ward with a 2 cm blister over the sacrum. Braden score 12. Prepare a nursing care plan.**

*Introduction.* The patient has a **stage 2 pressure injury** (partial-thickness loss with a blister) and a **HIGH** risk score. The aim is to heal the wound and stop new ones. After assessing the whole skin, I identify the priority diagnosis as impaired skin integrity, with a second diagnosis of impaired physical mobility as the root cause. Interventions follow the prevention bundle in Section 2.8 and the wound principles of moist healing, pressure relief, nutrition and infection control.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** Daughter says she cannot turn her mother alone; patient points to buttock pain. **O:** 2 cm sacral blister, surrounding redness, Braden 12, right hemiplegia, eats half of meals, wet pad. | **Impaired skin integrity** related to prolonged pressure, moisture and immobility, as evidenced by a 2 cm sacral blister. | **Tissue integrity: skin and mucous membranes.** Wound size reduced by 25% and no new red area in 7 days. | 1. Turn every 2 h in 30-degree side-lying position and sign the chart; *removes pressure and restores blood flow.* 2. Keep blister intact, clean with normal saline and cover with a hydrocolloid or non-adherent dressing; *moist wound healing and infection barrier.* 3. Alternating-pressure mattress and heel pads; *spread the load.* 4. Change wet pads at once and apply barrier cream; *moisture softens skin.* 5. Protein-rich diet, fluids 1.5-2 L, dietitian review; *tissue repair needs nutrients.* 6. Measure and record the wound every 3 days; *shows progress.* | Wound measured on day 7: size and surrounding skin recorded; goal met, partly met or not met and plan revised. |
| **O:** Cannot move the right side; needs two persons to turn. | **Impaired physical mobility** related to hemiplegia. | **Mobility.** Patient takes part in turning and passive exercises daily. | Passive range-of-motion exercises 2 times daily; teach daughter safe turning and lifting with a draw-sheet; *prevents contracture and shear.* | Daughter demonstrates the turn correctly before discharge. |
| **O:** Family unaware of risk. | **Deficient knowledge** (pressure injury prevention) related to lack of exposure. | Daughter lists 4 prevention steps by discharge. | Teach skin check, turning, hygiene, diet; give a written Nepali leaflet; *the family is the carer at home.* | Teach-back done and recorded. |

:::tip Exam tip
Always write the diagnosis in PES form and give a rationale for every intervention. A table with only actions and no rationale loses the explanation marks.
:::

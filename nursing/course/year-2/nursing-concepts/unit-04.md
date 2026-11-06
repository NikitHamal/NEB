---
subject: Nursing Concepts
grade: BSc Nursing Year 2
unit: 4
title: Nursing Theories and Models: Nightingale, Henderson, Abdellah, Orem and Neuman in Practice
hours: 8
area: BSN 15 · Nursing Concepts · Unit 5
---

In February 1855 nearly 43 of every 100 soldiers admitted to the Barrack Hospital at Scutari died. By June, after the sewers were flushed and the wards cleaned and ventilated, fewer than 3 in 100 died. Florence Nightingale had **observed, counted, explained and acted**: that is what a theory does. A **nursing theory** gives nurses a reason for what they do. This unit covers Unit 5 of BSN 15 (8 h): the scope of theory in practice, education and research, and five theories named in the syllabus, with a worked application in Nepal.

::: key What this unit gives you
- Real images: **Nightingale's portrait**, the **Barrack Hospital at Scutari**, her **rose diagram** of mortality and the **Lady with the Lamp**; with SVG figures on the Neuman systems model and the Orem nursing systems.
- Concepts, **metaparadigm** (person, health, environment, nursing), levels of theory, and the **uses of theory** in practice, education and research.
- **Nightingale** (environment), **Henderson** (14 needs), **Abdellah** (21 problems), **Orem** (self-care deficit, three nursing systems) and **Neuman** (lines of defence, three levels of prevention).
- Nightingale's mortality fall calculated as relative and absolute reduction; insulin-dose maths in a worked Orem case.
- Eight points on how theory helps nurses; model answers and a 5-column NANDA-I plan applying Orem to a diabetic foot ulcer.
:::

## 4.1 Theory, models and their scope

A **concept** is an idea (pain, stress, adaptation). A **theory** is a group of related concepts that explains or predicts events. A **model** is a simplified picture of a theory. **Levels:** **grand theories** cover the whole of nursing (Orem, Neuman); **middle-range theories** focus on one phenomenon (pain, comfort, self-efficacy); **practice theories** guide specific actions. The **metaparadigm** of nursing has four concepts: **person** (the client), **health**, **environment** and **nursing** (what the nurse does).

**Eight ways theory helps nursing.**

1. **It gives a language.** Terms such as "self-care deficit" let nurses describe the same problem in the same way. Shared words reduce confusion in a team. Records become clearer.
2. **It guides assessment.** A theory tells the nurse what to look for: needs, environment, stressors. Nothing important is skipped. Assessment becomes organised, not random.
3. **It supports the nursing process.** A framework links assessment, diagnosis, planning, action and evaluation. Care plans have a clear logic. The nurse can explain why she chose each action.
4. **It improves quality and safety.** Care based on theory is planned, repeatable and open to audit. Nurses can compare results. Mistakes are found earlier.
5. **It guides education.** Curricula and teaching plans are built on theories such as Orem's, as in many Nepali nursing colleges. Students learn to think, not to memorise tasks. Clinical teaching has a fixed framework.
6. **It guides research.** Theories give testable questions, for example "Does teaching improve self-care in diabetes?". Research then adds to the theory. Evidence-based practice grows.
7. **It defines the profession.** Theory shows that nursing has its own knowledge, separate from medicine. This supports professional status, the Nepal Nursing Council standards and nursing leadership.
8. **It supports decisions and advocacy.** When resources are limited, a nurse can justify staffing and care with a theory-based reason. Policy makers listen to reasoned arguments. Patients receive fair care.

## 4.2 Florence Nightingale (1820-1910): the environmental theory

In *Notes on Nursing* (1859) Nightingale said that **the nurse puts the patient in the best condition for nature to act upon him**. Disease is a **reparative process**, and the nurse controls the **environment**: **ventilation and warmth, light, cleanliness (of rooms, bed and nurse), pure water, quiet, a healthy diet and variety**, with careful observation. She also trained nurses and founded the first secular nursing school (St Thomas' Hospital, 1860). She was a pioneer of statistics: her **polar-area (rose) diagram** showed that most deaths in the army in the East came from **preventable disease**, not from wounds.

```python
adm_death_feb, adm_death_jun = 42.7, 2.2          # % of admissions who died at Scutari, Feb 1855 and Jun 1855
arr = adm_death_feb - adm_death_jun               # absolute reduction, percentage points
rrr = arr / adm_death_feb * 100                   # relative reduction, %
per1000_before, per1000_after = adm_death_feb * 10, adm_death_jun * 10
saved = per1000_before - per1000_after
print(f"Absolute reduction = {arr:.1f} percentage points; relative reduction = {rrr:.1f}%")
print(f"Per 1,000 admissions: {per1000_before:.0f} deaths before, {per1000_after:.0f} after; {saved:.0f} lives saved")
```

```text
Absolute reduction = 40.5 percentage points; relative reduction = 94.8%
Per 1,000 admissions: 427 deaths before, 22 after; 405 lives saved
```

The fall from 42.7% to 2.2% is **40.5 percentage points**, a **relative reduction of 94.8%**; of every 1,000 soldiers admitted, deaths fell from **427 to 22**, so **405 lives** were saved per 1,000. (The figures are widely quoted from Nightingale's reports; the sanitary commission's work was a main part of the improvement.)

```photogrid label="4.1" cols="4" ratio="1.0" caption="Florence Nightingale in real images. (a) A photographic portrait. (b) The Barrack Hospital at Scutari, 1855 (Illustrated London News): long wards of crowded beds. (c) Her rose diagram of mortality in the army in the East: wedges show deaths from preventable disease (outer, blue), wounds (red) and other causes. (d) The Lady with the Lamp (lithograph after Henrietta Rae): night rounds with a lamp, the symbol of nursing and of the lamp-lighting ceremony in Nepali nursing colleges."
@ photo id="nur9/fnport" cap="Florence Nightingale"
fit 1.0
focus 0.5 0.55
mark 0.50 0.60 "1"
key 1 (a) The founder of modern nursing, aged about 35
@ photo id="nur9/scutari" cap="Barrack Hospital, Scutari"
fit 1.0
focus 0.5 0.5
mark 0.50 0.45 "2"
mark 0.20 0.20 "3"
key 2 (b) Long ward with beds close together: overcrowding and poor air
key 3 (b) Nurses walking the ward: observation and care
@ photo id="nur9/rose" cap="Rose diagram of mortality"
fit 1.0
focus 0.75 0.5
mark 0.80 0.55 "4"
key 4 (c) Large wedges: deaths from preventable disease
@ photo id="nur9/lamp" cap="The Lady with the Lamp"
fit 1.0
focus 0.4 0.62
mark 0.35 0.65 "5"
key 5 (d) The lamp: night-time rounds and the symbol of caring
```

## 4.3 Virginia Henderson (1897-1996): the 14 basic needs

Henderson defined nursing as **assisting the individual, sick or well, in the performance of those activities contributing to health or its recovery (or to a peaceful death) that he would perform unaided if he had the necessary strength, will or knowledge**, and doing it so as to help him gain independence as rapidly as possible. The nurse is a **substitute, helper or partner**. The **14 components**: (1) breathe normally; (2) eat and drink adequately; (3) eliminate body wastes; (4) move and maintain posture; (5) sleep and rest; (6) select clothing, dress and undress; (7) maintain body temperature; (8) keep the body clean and groomed and protect the skin; (9) avoid dangers and avoid injuring others; (10) communicate emotions, needs, fears and opinions; (11) worship according to one's faith; (12) work so that there is a sense of accomplishment; (13) play or take part in recreation; (14) learn, discover or satisfy curiosity. **Use:** an easy checklist for ward assessment, especially in the care of the elderly, the disabled and the dying.

## 4.4 Faye Abdellah (1919-2017): 21 nursing problems

Abdellah moved the focus from disease to the **patient's needs**, and in 1960 listed **21 nursing problems** in three groups: **physical, sociological and emotional needs**, and **types of relationship between the nurse and family**. Examples include maintaining good hygiene and physical comfort, promoting optimal activity, rest and sleep, preventing accidents and infection, maintaining oxygen supply, nutrition, elimination, and fluid and electrolyte balance, recognising the physical, emotional and social responses of illness, using community resources, and understanding the role of social problems in illness. Her work is the base of **patient-centred care** and of the nursing diagnosis; she was also the first nurse to hold the rank of Deputy Surgeon General of the US.

## 4.5 Dorothea Orem (1914-2007): the self-care deficit theory

Orem's theory has three linked parts. **(1) Self-care:** the practice of activities that people begin and carry out for themselves to maintain life, health and well-being (universal needs such as air, water, food, elimination, activity and rest, solitude and social interaction, safety, and health-related needs). **(2) Self-care deficit:** the theory's core: **nursing is needed when the person's self-care agency is less than the therapeutic self-care demand**. **(3) Nursing systems:** the nurse chooses the system by how much the person can do (Figure 4.2).

```svgfig label="4.2" caption="Orem's three nursing systems. Wholly compensatory: the nurse does everything because the patient cannot act (unconscious, ventilated). Partly compensatory: the nurse and patient share the work (a patient after surgery can wash his face but cannot walk). Supportive-educative: the patient can do the care but needs teaching, support and encouragement (a woman with diabetes learning to inject insulin). The aim is to move the patient to the right, towards independence."
f = Fig(760, 250)
f.box(10, 40, 230, 110, "WHOLLY COMPENSATORY\nNurse does it ALL\nPatient cannot act:\nunconscious, ventilated", fill=ROSE, stroke=RED, color=RED, size=11, bold=True)
f.box(265, 40, 230, 110, "PARTLY COMPENSATORY\nNurse and patient SHARE\nPost-operative: nurse\nturns, patient washes face", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(520, 40, 230, 110, "SUPPORTIVE-EDUCATIVE\nPatient does, nurse TEACHES\nDiabetes: learns to inject\ninsulin and check feet", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(750, 185), (10, 185)], color=TEAL, sw=2.4, label="NURSE'S ROLE FALLS as self-care agency grows", lpos=(380, 175))
f.text(380, 225, "Self-care agency < therapeutic self-care demand = self-care DEFICIT = nursing needed", size=11, color=NAVY, bold=True)
```

## 4.6 Betty Neuman (born 1924): the systems model

Neuman sees the person as an open **system** in constant exchange with the environment, surrounded by **stressors** (intrapersonal, interpersonal and extrapersonal). The model (Figure 4.3) has a **basic structure (central core)** of survival factors (temperature, genes, organ function), surrounded by **lines of resistance** (internal defences: immune response, antibodies), the **normal line of defence** (the person's usual stable state and health) and the outer, **flexible line of defence** (a protective buffer that expands or shrinks, such as sleep, nutrition and support). A stressor breaks the flexible line first; if it penetrates, **reaction** occurs, and the nurse acts through **three levels of prevention**: **primary** (strengthen the flexible line before the stressor, e.g. immunisation), **secondary** (treat symptoms and strengthen the lines of resistance, e.g. early treatment) and **tertiary** (reconstitution, rehabilitation).

```svgfig label="4.3" caption="The Neuman systems model. The central core (survival factors) is protected by rings: the lines of resistance, the normal line of defence and the outer flexible line of defence. Stressors approach from outside; if the flexible line is thin (poor sleep, hunger, no support), they pass through and cause a reaction. Primary prevention strengthens the flexible line; secondary prevention supports the lines of resistance; tertiary prevention rebuilds the system after the reaction."
f = Fig(760, 300)
f.circle(240, 150, 135, fill="#ecfdf5", stroke=TEAL, sw=2.2)
f.circle(240, 150, 105, fill="#eff6ff", stroke=NAVY, sw=2.2)
f.circle(240, 150, 72, fill="#fef3c7", stroke=AMBER, sw=2.2)
f.circle(240, 150, 38, fill="#fecdd3", stroke=RED, sw=2.2, label="CORE", size=11, color=RED)
f.text(240, 28, "FLEXIBLE line of defence", size=10.5, color=TEAL, bold=True)
f.text(240, 62, "NORMAL line of defence", size=10.5, color=NAVY, bold=True)
f.text(240, 94, "LINES OF RESISTANCE", size=10, color=AMBER, bold=True)
f.arrow([(10, 80), (110, 110)], color=RED, sw=2.4, label="stressor", lpos=(55, 70))
f.arrow([(10, 220), (112, 190)], color=RED, sw=2.4)
f.box(430, 20, 320, 70, "PRIMARY prevention: strengthen the\nflexible line BEFORE the stressor\n(immunise, teach, nutrition)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(430, 110, 320, 70, "SECONDARY prevention: treat symptoms,\nsupport the lines of resistance\n(early diagnosis and treatment)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(430, 200, 320, 70, "TERTIARY prevention: reconstitution\nand rehabilitation after the reaction\n(foot care, physiotherapy)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
```

## Formula and fact sheet

- Metaparadigm: person, health, environment, nursing. Levels: grand, middle-range, practice.
- Nightingale: environment (air, light, warmth, cleanliness, quiet, diet), observation, statistics; Scutari 42.7% to 2.2% (absolute fall 40.5 points, relative 94.8%).
- Henderson: 14 basic needs; Abdellah: 21 problems; Orem: self-care, self-care deficit, 3 systems; Neuman: lines of resistance, normal and flexible lines, 3 levels of prevention.

## Chapter summary

- Theory explains why nurses act; it guides practice, education and research.
- Nightingale: nursing is control of the environment and careful observation; Henderson: helping with 14 needs towards independence; Abdellah: 21 patient problems.
- Orem: nurse acts when self-care agency is less than demand, using a wholly compensatory, partly compensatory or supportive-educative system.
- Neuman: protect the core with the flexible line, resistance lines and three levels of prevention.

## Practice

```python
m1 = round((42.7 - 2.2) / 42.7 * 100, 1)       # MCQ1 relative reduction
m2 = 14 + 21                                    # MCQ2 sum of Henderson needs and Abdellah problems
weight, units_per_kg = 64, 0.5                  # Mr Krishna Prasad: starting insulin
c_total = weight * units_per_kg
c_am = round(c_total * 2 / 3)                   # two-thirds in the morning
c_pm = round(c_total / 3)                       # one-third in the evening
print(f"MCQ1 = {m1}%; MCQ2 = {m2}")
print(f"Mr Prasad: insulin {c_total:.0f} units a day = {c_am} units morning + {c_pm} units evening")
```

```text
MCQ1 = 94.8%; MCQ2 = 35
Mr Prasad: insulin 32 units a day = 21 units morning + 11 units evening
```

**MCQs (with reasons)**

1. Scutari mortality fell from 42.7% to 2.2%. The relative reduction is about: (a) 40.5% (b) 94.8% (c) 5.2% (d) 19.4%.
2. The nursing system for an unconscious ventilated patient (Orem) is: (a) supportive-educative (b) partly compensatory (c) wholly compensatory (d) none.
3. In Neuman's model the outermost ring that is first met by stressors is: (a) lines of resistance (b) normal line of defence (c) flexible line of defence (d) basic structure.
4. Henderson's theory lists: (a) 14 basic needs (b) 21 problems (c) 5 stages (d) 4 phases.
5. Immunising a child before exposure is which Neuman level? (a) primary (b) secondary (c) tertiary (d) quaternary.

::: note Answers and rationales
**1. (b).** (42.7 − 2.2) ÷ 42.7 = 94.8%; 40.5 is the absolute fall in percentage points and 5.2% is the leftover share.
**2. (c).** The patient cannot act, so the nurse does everything; supportive-educative is for patients who can act with teaching.
**3. (c).** The flexible line is the outer protective buffer; the others lie inside it.
**4. (a).** Henderson has 14 needs; 21 problems belong to Abdellah.
**5. (a).** Strengthening defences before the stressor is primary prevention; secondary treats early disease and tertiary rehabilitates.
:::

**Short answer (3 marks): State Orem's three theories and the three nursing systems.** Orem described the theory of self-care, the theory of self-care deficit and the theory of nursing systems. The deficit exists when the person's self-care agency is less than the therapeutic self-care demand, and nursing is needed. The systems are wholly compensatory, partly compensatory and supportive-educative.

**Medium answer (5 marks): Describe Nightingale's contribution to nursing.** Nightingale (1820-1910) nursed in the Crimean War at Scutari and reduced hospital mortality from 42.7% to 2.2% through sanitation, ventilation, cleanliness, diet and organisation, with the Sanitary Commission. Her environmental theory in *Notes on Nursing* (1859) says that the nurse places the patient in the best condition for nature to heal, controlling air, light, warmth, cleanliness, quiet and diet and observing carefully. She used statistics (rose diagram) to prove that preventable disease killed most soldiers, founded the Nightingale Training School at St Thomas' Hospital (1860) and shaped hospital design and public health. Her ideas remain the base of infection control and the nurse's duty of observation.

**Long answer (10 marks): Mr Krishna Prasad Adhikari, 58 years, 64 kg, has type 2 diabetes for 12 years and a foot ulcer on the right great toe with random blood sugar 286 mg/dL. He is newly started on insulin 0.5 units/kg/day, does not know how to inject, and walks barefoot in the field. Apply Orem's theory, calculate the insulin and write the nursing care plan.**

*Calculation.* Total insulin **= 64 × 0.5 = 32 units a day**, split two-thirds in the morning (**21 units**) and one-third in the evening (**11 units**), by the doctor's order; the nurse checks and gives.

*Orem application.* His **universal self-care requisites** are food, activity and safety; the **health-deviation requisite** is diabetes with an ulcer. His **therapeutic self-care demand** is insulin, glucose monitoring, diet, foot care and wound care. His **self-care agency** is low because of lack of knowledge, not of ability. In the first days he needs a **partly compensatory** system: the nurse does the dressing and injection, and he washes and feeds himself. As he learns, the system becomes **supportive-educative**: the nurse teaches injection technique with a pen and a demonstration, rotation of sites, hypoglycaemia signs and foot inspection. The plan includes diet in dal-bhat portions, daily foot washing, drying between toes, footwear and nail care, and follow-up at the health post and the diabetic foot clinic.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I do not know how to inject." **O:** insulin 32 units/day newly started. | **Deficient knowledge** about insulin therapy related to new diagnosis, as evidenced by inability to inject. | **Knowledge: diabetes management:** gives a correct injection with a pen and states hypoglycaemia signs in 3 days. | Demonstrate, then return-demonstrate (skill learning); teach site rotation and timing 21 units morning and 11 units evening; teach glucose and hypoglycaemia signs (safety). | Self-injects correctly. |
| **O:** ulcer right great toe, RBS 286 mg/dL. | **Impaired skin integrity** related to neuropathy and high glucose, as evidenced by ulcer. | **Wound healing:** wound clean, ulcer size reduced in 2 weeks. | Clean dressing and off-loading (prevents infection and pressure); control blood sugar (healing needs it); inspect daily; refer to foot clinic (prevents amputation). | Ulcer shrinking; no pus. |
| **O:** walks barefoot in the field. | **Risk for injury** related to loss of protective sensation. | **Safety behaviour:** wears footwear and checks feet daily. | Teach daily foot check with a mirror, shoes at all times, nail care (prevents new wounds); involve the family. | Wears shoes; checks feet. |
| **S:** "Rice is my main food." **O:** BMI 25. | **Imbalanced nutrition** related to uneven carbohydrate intake. | **Nutritional status:** follows the diet plan and RBS falls below 180 mg/dL in 2 weeks. | Dietary teaching with local foods (dal, vegetables, controlled rice) (steady glucose); regular meal times (match insulin). | RBS 170; eats as planned. |
| **S:** "I have no time for treatment." **O:** a farmer, far from health post. | **Ineffective health management** related to access and beliefs. | **Participation:** attends follow-up and states a plan within 1 month. | Link with the FCHV and the nearest health post (access); give a written chart (continuity); set goals with him (autonomy, Orem's supportive-educative role). | Attends clinic; follows plan. |

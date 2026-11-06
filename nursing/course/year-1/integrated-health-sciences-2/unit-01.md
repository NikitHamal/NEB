---
subject: Integrated Health Sciences II
grade: BSc Nursing Year 1
unit: 1
title: Nervous System and Special Senses
hours: 30
area: BSN 2-3 · Integrated Health Sciences II · Unit 1
---

Every nursing assessment begins with the nervous system: Is the patient awake, do they follow commands, are the pupils equal, can they see and hear? This unit covers the organisation of the brain and spinal cord, the neuron and the reflex arc, intracranial pressure and cerebral perfusion, the Glasgow Coma Scale, the eye and ear, and the stroke and head-injury care that fills the neuro wards of Bir, TUTH and Bharatpur hospitals.

::: key What this unit gives you
- A real MRI of the brain, labelled, paired with a lobe-function schematic.
- The neuron, action potential and reflex arc as clean diagrams, with the Nernst potassium potential computed.
- Intracranial pressure, MAP, cerebral perfusion pressure, GCS scoring and mannitol dose, all checked by script.
- The eye: a labelled photograph, a Snellen chart and a refraction diagram with dioptre arithmetic; the ear and balance.
- Eight points of stroke prevention and first aid, and model answers with a full care plan for raised ICP after head injury.
:::

## 1.1 Organisation of the nervous system

The **central nervous system (CNS)** is the brain and spinal cord; the **peripheral nervous system (PNS)** is the 12 pairs of cranial nerves and 31 pairs of spinal nerves. The PNS divides into a **somatic** part (voluntary muscle and skin sensation) and an **autonomic** part (heart, glands, smooth muscle) with **sympathetic** ("fight or flight") and **parasympathetic** ("rest and digest") arms. The brain has the **cerebrum** (two hemispheres joined by the corpus callosum), the **diencephalon** (thalamus and hypothalamus), the **brainstem** (midbrain, pons, medulla) and the **cerebellum**. The brain is wrapped in three meninges (dura, arachnoid, pia) and floats in cerebrospinal fluid (CSF), which is made at about 0.35 mL/min, so 504 mL a day, with 150 mL present at any moment.

```photogrid label="1.1" cols="2" ratio="1.05" caption="The brain in mid-sagittal section. (a) A real T1 MRI with the main structures marked. (b) The lobes of the cerebral hemisphere and what each one does; damage to a lobe gives the matching deficit."
@ photo id="nur2/mri" cap="Sagittal MRI of the head"
fit 1.05
focus 0.5 0.55
mark 0.50 0.64 "1"
mark 0.27 0.40 "2"
mark 0.46 0.45 "3"
mark 0.66 0.74 "4"
key 1 (a) Corpus callosum: the white arch joining the two hemispheres
key 2 (a) Cerebellum: balance and smooth coordination, behind the brainstem
key 3 (a) Brainstem (midbrain, pons, medulla): breathing, heart rate, consciousness
key 4 (a) Frontal lobe: planning, personality, voluntary movement
@ svg cap="Lobes and functions"
f = Fig(360, 340)
f.box(10, 20, 110, 70, "Frontal\nmotor cortex,\nspeech (Broca),\njudgement", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(125, 20, 110, 70, "Parietal\nsensation,\nbody position,\nspatial sense", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(240, 20, 110, 70, "Occipital\nvision", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(10, 110, 170, 70, "Temporal\nhearing, memory,\nspeech understanding\n(Wernicke)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(190, 110, 160, 70, "Cerebellum\nbalance, coordination\n(damage: ataxia)", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.box(10, 200, 340, 50, "Thalamus: relay of all senses.  Hypothalamus: temperature,\nhunger, thirst, pituitary control", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(10, 270, 340, 50, "Brainstem: breathing, heart rate, swallowing, arousal.\nCranial nerves III to XII arise here", fill=ROSE, stroke=RED, size=10.5, bold=True)
```

## 1.2 The neuron, action potential and reflex arc

A **neuron** has dendrites (receive), a cell body, and an axon (conducts); myelin from Schwann cells (PNS) or oligodendrocytes (CNS) speeds conduction by saltatory jumps between nodes of Ranvier. At rest the inside of the cell is about **-70 mV** because the Na⁺/K⁺ pump and leaky K⁺ channels hold K⁺ in. The equilibrium potential for potassium follows the Nernst equation, E = 61.5 × log₁₀([K]out ÷ [K]in): with 5 mmol/L outside and 150 inside, E = **-90.8 mV**. When the membrane is depolarised to the threshold (about -55 mV), voltage-gated Na⁺ channels open (upstroke to about +30 mV), then K⁺ channels open (repolarisation), and the pump restores the balance. Local anaesthetics such as lignocaine block the Na⁺ channel, so no impulse passes and the patient feels no pain.

```svgfig label="1.2" caption="Action potential. Threshold -55 mV triggers an all-or-none spike; the refractory period keeps the impulse moving one way."
import math
f = Fig(760, 250)
f.line(60, 30, 60, 210, color=SLATE, sw=1.6); f.line(60, 210, 720, 210, color=SLATE, sw=1.6)
for mv, y in [(30, 50), (0, 80), (-55, 150), (-70, 175)]:
    f.line(55, y, 720, y, color="#e2e8f0", sw=1); f.text(48, y, str(mv), size=10, color=SLATE, anchor="end", vmid=True)
f.text(20, 120, "mV", size=11, color=SLATE, bold=True)
pts = [(60, 175), (140, 175), (170, 150), (195, 50), (230, 120), (265, 195), (310, 175), (400, 175)]
for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=3)
f.text(215, 40, "Na⁺ in: depolarisation", size=10.5, color=RED, bold=True, anchor="start")
f.text(255, 150, "K⁺ out: repolarisation", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(330, 195, "hyperpolarisation, then rest -70", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(100, 142, "threshold -55", size=10, color=SLATE, bold=True)
f.text(450, 80, "All-or-none: a stronger stimulus makes MORE spikes,", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(450, 98, "never a bigger spike.", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(390, 232, "Time (about 2 ms)", size=11, color=SLATE, bold=True)
```

A **reflex arc** is the fastest response: receptor, sensory neuron, integration in the spinal cord, motor neuron, effector. The knee jerk (patellar tendon, L2-L4) is monosynaptic, and nurses test reflexes with a hammer to find lesions: reflexes are lost in lower motor neuron damage (Guillain-Barré syndrome) and brisk in upper motor neuron damage (stroke).

## 1.3 Intracranial pressure, perfusion and the Glasgow Coma Scale

The skull is a rigid box holding brain (80%), blood (10%) and CSF (10%): the **Monro-Kellie doctrine** says that if one grows (a clot, oedema), another must shrink or **intracranial pressure (ICP)** rises. Normal ICP is 5-15 mmHg; above 20 mmHg needs treatment. **Cerebral perfusion pressure** is CPP = MAP − ICP and should stay at 60-70 mmHg or more, otherwise the brain is starved of blood.

```python
sbp, dbp, icp = 130, 80, 25
map_ = (sbp + 2 * dbp) / 3
cpp = map_ - icp
print(f"MAP = {map_:.1f} mmHg")
print(f"CPP = {cpp:.1f} mmHg")
print("Mannitol 0.5 g/kg for 70 kg =", 0.5 * 70, "g =", 0.5 * 70 / 0.2, "mL of 20%")
```

```text
MAP = 96.7 mmHg
CPP = 71.7 mmHg
Mannitol 0.5 g/kg for 70 kg = 35.0 g = 175.0 mL of 20%
```

Here the CPP of 71.7 mmHg is acceptable, but if the ICP climbs to 45 mmHg with the same BP, CPP falls to 51.7 mmHg and the brain is ischaemic. Signs of rising ICP are a worsening headache, vomiting, drowsiness, unequal pupils and **Cushing's triad** (hypertension with a wide pulse pressure, bradycardia, irregular breathing).

**Glasgow Coma Scale (GCS)** scores Eye opening (1-4), Verbal response (1-5) and Motor response (1-6): the minimum is 3 and the maximum 15. A patient who opens eyes to voice (3), is confused (4) and localises pain (5) scores 12; a patient with no eye opening (1), incomprehensible sounds (2) and abnormal flexion (3) scores 6. **GCS 8 or less means intubate** because the airway is not protected. Mild head injury is 13-15, moderate 9-12, severe 3-8.

```svgfig label="1.3" caption="Monro-Kellie doctrine and the ICP cascade. Treatment aims to break the cycle: head up 30 degrees, mannitol, airway and oxygen, avoid hypotension."
f = Fig(760, 200)
st = [("Brain injury,\nclot or oedema", ROSE, RED), ("Volume rises\nin a rigid skull", SAND, AMBER), ("ICP above 20\nCPP falls", SAND, AMBER), ("Ischaemia and\nmore oedema", ROSE, RED), ("Herniation:\nCushing triad,\ncoma, death", ROSE, RED)]
for i, (t_, fc, sc) in enumerate(st):
    x = 8 + i * 150; f.box(x, 40, 128, 66, t_, fill=fc, stroke=sc, size=10.5, bold=True)
    if i < 4: f.arrow([(x + 128, 73), (x + 150, 73)], color=SLATE, sw=2)
f.arrow([(690, 106), (690, 150), (70, 150), (70, 106)], color=RED, sw=1.6, dash=True)
f.text(380, 168, "Vicious cycle", size=11, color=RED, bold=True)
f.text(380, 188, "Break it: head up 30°, airway, mannitol or hypertonic saline, treat fever and seizures", size=10.5, color=TEAL, bold=True)
f.text(380, 20, "Raised intracranial pressure", size=11, color=SLATE, bold=True)
```

## 1.4 The eye and vision

Light passes the **cornea** (about 43 dioptres, the main refracting surface), the aqueous humour, the **pupil** (size set by the iris), the **lens** (about 19 dioptres at rest, thickened by the ciliary muscle for near vision) and the vitreous, and is focused on the **retina**. Rods (night vision, vitamin A needed) and cones (colour, detail, fovea) send impulses along the optic nerve to the occipital cortex. A dioptre is 1 ÷ focal length in metres, so the combined power of cornea and lens is about 62 D and the focal length is about 16.1 mm.

```photogrid label="1.2" cols="2" ratio="1.1" caption="The eye. (a) A labelled photograph of the front of the eye with the cross-section inset. (b) Refraction: the emmetropic eye focuses on the retina, the myopic eye in front of it, the hypermetropic eye behind it."
@ photo id="nur2/eye" cap="External eye"
fit 1.1
focus 0.5 0.45
mark 0.50 0.70 "1"
mark 0.42 0.52 "2"
key 1 (a) Pupil and iris: the iris muscle sets the pupil size
key 2 (a) Sclera and cornea: the white of the eye and the clear window in front
@ svg cap="Refraction errors"
f = Fig(380, 330)
for k, (name, fx, col) in enumerate([("Normal (emmetropia)", 0, TEAL), ("Myopia: image in front", -30, RED), ("Hypermetropia: image behind", 30, AMBER)]):
    y0 = 20 + k * 105
    f.circle(150, y0 + 40, 36, fill="#ffffff", stroke=SLATE, sw=2)
    f.line(110, y0 + 40, 80, y0 + 40, color=col, sw=1.5)
    for dy in (-18, 0, 18):
        f.line(20, y0 + 40 + dy, 118, y0 + 40 + dy, color=col, sw=1.3)
        f.line(118, y0 + 40 + dy, 186 + fx, y0 + 40, color=col, sw=1.3)
    f.line(186, y0 + 10, 186, y0 + 70, color=NAVY, sw=3)
    f.text(285, y0 + 38, name, size=10, color=col, bold=True)
    f.text(285, y0 + 54, ["no correction", "concave lens (minus)", "convex lens (plus)"][k], size=9.5, color=SLATE)
```

**Visual acuity** is tested with the **Snellen chart** at 6 metres, one eye at a time with spectacles on: 6/6 is normal; 6/60 means the patient sees at 6 m what a normal eye sees at 60 m, and **below 3/60 (or 6/60 in the better eye) is the WHO and Nepal definition of blindness** used for the National Eye Care Programme. A patient with a far point of 40 cm needs a lens of 1 ÷ 0.40 = **-2.50 D** (a concave lens) to see distant objects; a lens of +2.5 D has a focal length of 40 cm.

```photogrid label="1.3" cols="3" ratio="0.9" caption="Eye testing and the visual pathway. (a) A Snellen chart: each line is read from the top, and the smallest line read correctly gives the acuity. (b) The three common causes of preventable blindness in Nepal and the matching action. (c) Hearing and balance share the inner ear."
@ photo id="nur2/snellen" cap="Snellen chart"
fit 0.9
focus 0.5 0.5
mark 0.52 0.90 "1"
mark 0.50 0.40 "2"
key 1 (a) Top letter "E/A": read at 6 m by a normal eye from 60 m, so it is the 6/60 line
key 2 (a) Middle lines: 6/18 to 6/12; the bottom lines are 6/9 to 6/6
@ svg cap="Preventable blindness"
f = Fig(300, 330)
for i, (a, b, c) in enumerate([("Cataract", "lens clouding", "surgery (Tilganga, Lumbini Eye)"), ("Refractive error", "glasses", "school screening"), ("Trachoma", "Chlamydia", "SAFE strategy; Nepal eliminated 2018"), ("Vitamin A lack", "night blindness", "capsules at 6-59 months")]):
    y = 14 + i * 78
    f.box(8, y, 284, 66, a + "\n" + b + "\n" + c, fill=[MINT, BLUE, SAND, ROSE][i], stroke=[TEAL, NAVY, AMBER, RED][i], size=10.5, bold=True)
@ svg cap="Ear: hearing and balance"
f = Fig(300, 330)
f.box(8, 14, 284, 50, "Sound: pinna → canal → eardrum", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(8, 80, 284, 50, "Ossicles: malleus, incus, stapes\n(amplify about 20 times)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(8, 146, 284, 50, "Cochlea: hair cells → cranial nerve VIII", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(8, 212, 284, 50, "Semicircular canals: rotation.\nUtricle, saccule: gravity", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(150, 290, "Eustachian tube equalises middle-ear pressure", size=10, color=SLATE, bold=True)
for y in (64, 130, 196): f.arrow([(150, y), (150, y + 16)], color=SLATE, sw=2)
```

## 1.5 Stroke: prevention and first-aid education in eight points

A stroke is sudden loss of brain function from a blocked (ischaemic, about 85%) or burst (haemorrhagic) vessel. Nepal's PEN programme treats the main cause, hypertension, at the health post; nurses teach these eight points in clinics and community groups.

1. **Control blood pressure.** High pressure is the number-one cause of stroke, and it gives no symptoms. Check BP every year after 25 and every month if known hypertensive, aiming below 140/90 mmHg. Take amlodipine, losartan or enalapril every day even when well.
2. **Cut salt and fatty food.** Keep salt below 5 g a day and limit pickles, dried fish, ghee and fried snacks. Salt raises BP and fat clogs arteries. Eat green vegetables, fruit, dal and whole grains instead.
3. **Stop tobacco and limit alcohol.** Smoking, hookah and chewing tobacco narrow the arteries and make blood stick together. Quitting halves the risk within a few years. Refer to the tobacco cessation service and never drink and drive.
4. **Treat diabetes and cholesterol.** High sugar damages vessel walls and high LDL builds plaque. Check fasting glucose yearly and take metformin and statins as prescribed. Keep HbA1c near 7%.
5. **Be active and keep weight healthy.** Walk briskly 30 minutes on five days a week and keep BMI below 23. Exercise lowers BP, sugar and weight together. Yoga and household work count.
6. **Treat atrial fibrillation.** An irregular pulse lets clots form in the heart and travel to the brain. Feel the pulse of every older patient for one minute and refer an irregular pulse for ECG. Anticoagulants such as warfarin need regular INR checks.
7. **Know FAST and act at once.** **F**ace drooping, **A**rm weakness, **S**peech slurred, **T**ime to go to hospital. Note the time symptoms began and go to the nearest hospital with CT; clot-busting treatment works only within 4.5 hours.
8. **Give correct first aid.** Lay the patient on the side with the head slightly raised, keep the airway clear, and give nothing by mouth because swallowing is unsafe. Do not give aspirin until the doctor has excluded bleeding, and do not use traditional "cuts" or oil. Check the blood sugar if a glucometer is available.

## Formula and fact sheet

- MAP = (SBP + 2 × DBP) ÷ 3. CPP = MAP − ICP; keep at least 60 mmHg. Normal ICP 5-15, treat above 20 mmHg.
- GCS = E (1-4) + V (1-5) + M (1-6), range 3-15; 8 or less means secure the airway. Cushing triad: high BP, slow pulse, irregular breathing.
- Nernst: E_K = 61.5 × log₁₀(Kout ÷ Kin) = -90.8 mV. Resting potential -70 mV, threshold -55 mV.
- Lens power in dioptres = 1 ÷ focal length (m); myopia needs a minus lens, hypermetropia a plus lens. Blindness: below 3/60.
- Mannitol 0.5-1 g/kg of 20% solution (0.2 g per mL), over 15-20 minutes through a filter.

## Chapter summary

- The CNS is brain and cord, the PNS cranial and spinal nerves; the brainstem controls the vital functions.
- Neurons fire by all-or-none action potentials; reflexes are the quickest protective response.
- The skull is a closed box, so any added volume raises ICP and lowers CPP; GCS 8 or less needs an airway.
- The eye focuses by cornea and lens; Snellen tests acuity and glasses correct refractive error.
- Stroke prevention rests on BP control, no tobacco, FAST recognition and early transfer.

## Practice

**MCQs (with reasons)**

1. Resting membrane potential of a neuron is about: (a) +30 mV (b) -70 mV (c) -55 mV (d) 0 mV.
2. MAP 100 mmHg and ICP 30 mmHg give a CPP of: (a) 130 (b) 70 (c) 30 (d) 3.3 mmHg.
3. A patient with E2, V3, M4 has a GCS of: (a) 7 (b) 9 (c) 10 (d) 12.
4. Myopia is corrected with a: (a) convex lens (b) concave lens (c) cylindrical prism (d) bifocal only.
5. The structure that joins the two cerebral hemispheres is the: (a) corpus callosum (b) thalamus (c) pons (d) falx.

::: note Answers and rationales
**1. (b).** The Na⁺/K⁺ pump and K⁺ leak hold the inside at about -70 mV; -55 mV is the threshold and +30 mV is the peak of the spike.
**2. (b).** CPP = MAP − ICP = 100 − 30 = 70 mmHg. Option (a) adds the two numbers instead of subtracting them.
**3. (b).** 2 + 3 + 4 = 9, a moderate head injury; the airway should be watched closely since the score is near 8.
**4. (b).** In myopia the image falls in front of the retina, so a diverging (concave, minus) lens pushes it back; a convex lens is for hypermetropia.
**5. (a).** The corpus callosum is the large white-matter bridge seen as an arch in the sagittal MRI; the thalamus is a relay, and the pons is in the brainstem.
:::

**Short answer (3 marks): Cerebral perfusion pressure.** Cerebral perfusion pressure is the pressure that drives blood through the brain, equal to mean arterial pressure minus intracranial pressure. With BP 130/80 the MAP is 96.7 mmHg, and with an ICP of 25 mmHg the CPP is 71.7 mmHg. It must stay at 60-70 mmHg or above; if the ICP rises to 45 mmHg the CPP falls to 51.7 mmHg and the brain becomes ischaemic. Nurses protect it by raising the head to 30 degrees, avoiding hypotension, and treating fever and seizures.

**Medium answer (5 marks): Describe the action potential and the reflex arc (Figure 1.2).** A neuron at rest is at -70 mV. A stimulus that depolarises it to the threshold of -55 mV opens voltage-gated **Na⁺ channels**, so sodium rushes in and the potential climbs to about +30 mV (depolarisation). The Na⁺ channels then close and **K⁺ channels** open, so potassium leaves and the cell repolarises, briefly overshooting (hyperpolarisation) before the Na⁺/K⁺ pump restores rest. The spike is **all-or-none**, and a refractory period makes it travel one way; myelin speeds it by saltatory conduction between nodes of Ranvier. The **reflex arc** has five parts: receptor, sensory neuron, spinal cord integration centre, motor neuron and effector. The knee jerk is monosynaptic (L2-L4). Reflexes are lost in lower motor neuron lesions and brisk in upper motor neuron lesions, so they guide diagnosis.

**Long answer (10 marks): Ramesh Thapa, 24, a motorcyclist without a helmet, is brought to the emergency of a teaching hospital after a road crash. He opens his eyes to pain, groans without words and withdraws from pain (E2 V2 M4). Over two hours he becomes drowsier: E1 V2 M4, BP 150/90 mmHg, pulse 52/min, irregular breathing, right pupil dilated. Weight 60 kg; ICP monitor reads 28 mmHg. Discuss the condition and prepare a nursing care plan.**

*Introduction.* This is a severe traumatic brain injury with rising ICP. The GCS fell from 8 to 7, below the intubation threshold. His MAP is (150 + 2 × 90) ÷ 3 = **110.0 mmHg**, so the CPP is 110.0 − 28 = **82.0 mmHg**, still adequate, but the slow pulse, high BP, irregular breathing and a blown pupil are **Cushing's triad** with uncal herniation, a surgical emergency. Helmet use is required by the Nepal Motor Vehicles and Transport Management Act and prevents most such deaths.

*Management.* Secure the airway with cervical spine protection and intubate; give oxygen to keep SpO₂ above 94% and aim for PaCO₂ 35-40 mmHg. Raise the head 30 degrees with the neck neutral. Give **mannitol 0.5 g/kg**: 0.5 × 60 = 30 g = **150 mL of 20%** over 20 minutes; with a 15 drops/mL set the rate is 150 × 15 ÷ 20 = 112.5, so about **113 drops/min**. Insert a urinary catheter because mannitol causes diuresis. Urgent CT head and neurosurgical review for evacuation of a haematoma (Bir, TUTH or Bhaktapur neuro units). Treat seizures with phenytoin or levetiracetam, keep sodium above 135 mmol/L and glucose 4-10 mmol/L, and avoid hypotension.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **O:** GCS 7, ICP 28, pulse 52, BP 150/90, right pupil dilated. | **Decreased intracranial adaptive capacity** related to brain injury, as evidenced by raised ICP and falling GCS. | **Neurological status:** ICP below 20 mmHg, CPP at least 60, GCS not falling within 6 h. | 1. Head up 30 degrees, neck midline, no tight neck ties; *promotes venous drainage.* 2. Neuro checks (GCS, pupils, limb power) every 15 min; *detects herniation early.* 3. Mannitol as ordered with strict urine output; *draws water out of the brain.* 4. Cluster care and quiet room; *suction and noise raise ICP.* | ICP chart and GCS reviewed each hour; goal met when ICP is under 20 mmHg. |
| **O:** GCS 7, irregular breathing, SpO₂ 90% before intubation. | **Ineffective airway clearance** related to depressed consciousness, as evidenced by irregular breathing and poor cough. | **Respiratory status: airway patency:** clear airway, SpO₂ at least 94% in 1 h. | 1. Intubate and ventilate to PaCO₂ 35-40; *hypercapnia dilates vessels and raises ICP.* 2. Suction for under 10 seconds with pre-oxygenation; *avoids hypoxia and ICP spikes.* 3. Lateral position if not intubated; *prevents aspiration.* | SpO₂, ABG and chest sounds each 2 h. |
| **O:** unconscious, unable to blink fully, on bed rest, mannitol diuresis. | **Risk for injury and impaired skin integrity** related to unconsciousness and immobility. | **Safety and tissue integrity:** no eye or pressure injury during stay. | 1. Eye care with saline and lubricant, pad if needed; *prevents corneal ulcer.* 2. Two-hourly turning with spine alignment; *prevents pressure injury.* 3. Pad side rails for seizures; *avoids trauma.* 4. Hourly urine and daily electrolytes; *mannitol can cause dehydration and low sodium.* | Skin and eyes inspected each shift; Braden score reviewed. |
| **S:** family asks "will he live?" **O:** parents anxious and crying. | **Anxiety (family)** related to critical illness, as evidenced by repeated questions and tearfulness. | **Anxiety level:** family states understanding and takes part in care within 24 h. | 1. Update the family twice a day in simple Nepali; *honest information lowers fear.* 2. Allow short visits and hold the hand; *touch and hearing may persist.* 3. Link with the hospital social worker for costs and referral; *reduces financial stress.* | Family stays calm and asks informed questions. |

*Prevention and health education.* Use a helmet and seat belts, never drive after raksi, keep children away from roads, and teach first aid: do not move the neck, keep the airway open, call an ambulance (102). *Conclusion.* In raised ICP the nurse's eyes are the monitor: a falling GCS or an unequal pupil is reported at once.

::: tip Exam tip
In any head-injury answer, write the CPP formula with the patient's own numbers and name Cushing's triad. Write head up 30 degrees, airway, and mannitol dose in that order, and finish with a table of NANDA-I diagnoses.
:::

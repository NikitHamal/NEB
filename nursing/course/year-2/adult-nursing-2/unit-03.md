---
subject: Adult Nursing II
grade: BSc Nursing Year 2
unit: 3
title: Neurological Nursing: Assessment, Stroke, Head Injury, Seizures and Meningitis
hours: 22
area: BSN 10 · Adult Nursing II · Unit 3
---

Stroke, head injury and meningitis fill the neurology and emergency beds of Nepal. Raised blood pressure (about one quarter of adults in STEPS 2019) is the main cause of stroke, **road traffic crashes and falls from trees and terraces cause most head injuries**, and meningitis and encephalitis (including Japanese encephalitis in the Terai) are seasonal threats. Neurological care is concentrated in Kathmandu, at the **Upendra Devkota Memorial National Institute of Neurological and Allied Sciences (Bansbari)**, Bir Hospital, TUTH, Patan and the provincial hospitals, so the district nurse often stabilises the patient and refers. Her tools are a torch, a watch and the **Glasgow Coma Scale**, and every number in this unit is checked by program.

::: key What this unit gives you
- Real photographs of an intracerebral haemorrhage on CT, an epidural haematoma on CT, a patient with Bell's palsy and a lumbar puncture in progress, plus four SVG figures.
- GCS, MAP and cerebral perfusion pressure, alteplase and mannitol doses, drip rate, phenytoin loading and the diazepam volume.
- Eight points each on raised ICP care, stroke care, seizure first aid and meningitis care.
- Model answers and a NANDA-I care plan for a man with an acute ischaemic stroke.
:::

## 3.1 Neurological assessment, GCS and intracranial pressure

A quick neurological check covers the **level of consciousness**, **pupils** (size, equality, reaction to light), **limb power** (0-5), speech, face symmetry, sensation and vital signs. The **Glasgow Coma Scale (GCS)** adds three scores: **eye opening E (1-4)**, **verbal response V (1-5)** and **best motor response M (1-6)**; the total runs from 3 (deep coma) to 15 (fully alert). **A GCS of 8 or less means the patient cannot protect the airway and needs airway support.** The skull is a closed box, so brain swelling, bleeding or tumour raises the **intracranial pressure (ICP, normal 5-15 mmHg)**. The brain's blood supply depends on the **cerebral perfusion pressure, CPP = MAP − ICP**, which should stay at 60-70 mmHg or more.

```python
e, v, m = 2, 3, 4                                # eye to pain, inappropriate words, flexion
gcs = e + v + m
sbp, dbp, icp = 110, 70, 30
mapx = (sbp + 2 * dbp) / 3; cpp = mapx - icp
wt = 70
alt = 0.9 * wt; bol = alt * 0.1; inf = alt * 0.9           # alteplase 0.9 mg/kg, 10% bolus
man = 0.5 * wt; ml = man / 20 * 100; gtt = ml * 15 / 30   # mannitol 0.5 g/kg, 20% solution, 30 min
print(f"GCS = E{e} + V{v} + M{m} = {gcs} (8 or less: protect the airway)")
print(f"MAP = ({sbp} + 2 x {dbp}) / 3 = {mapx:.1f}; CPP = {mapx:.1f} - {icp} = {cpp:.1f} mmHg (target 60-70)")
print(f"Alteplase 0.9 x {wt} = {alt:.0f} mg: bolus {bol:.1f} mg, then {inf:.1f} mg over 60 min (maximum total 90 mg)")
print(f"Mannitol 0.5 x {wt} = {man:.0f} g = {ml:.0f} mL of 20%; over 30 min at 15 gtt/mL = {gtt:.1f} = {round(gtt)} gtt/min")
```

```text
GCS = E2 + V3 + M4 = 9 (8 or less: protect the airway)
MAP = (110 + 2 x 70) / 3 = 83.3; CPP = 83.3 - 30 = 53.3 mmHg (target 60-70)
Alteplase 0.9 x 70 = 63 mg: bolus 6.3 mg, then 56.7 mg over 60 min (maximum total 90 mg)
Mannitol 0.5 x 70 = 35 g = 175 mL of 20%; over 30 min at 15 gtt/mL = 87.5 = 88 gtt/min
```

A patient who opens the eyes to pain (E2), speaks inappropriate words (V3) and flexes abnormally (M4) has **GCS 9**, so the airway is at risk and an urgent doctor review is needed. With BP 110/70 the **MAP is 83.3** and an ICP of 30 leaves a **CPP of 53.3 mmHg**, which is too low (the target is 60-70). For a 70 kg patient the alteplase dose is **63 mg** in total (0.9 mg/kg; maximum 90 mg), with **6.3 mg** as a bolus over 1 minute and **56.7 mg** over 60 minutes. Mannitol 0.5 g/kg is **35 g**, which is **175 mL** of the 20% solution, run over 30 minutes at **88 gtt/min** on a 15 gtt/mL set.

### Raised intracranial pressure: eight points of nursing care

1. **Recognise the early signs.** Restlessness, a new headache, vomiting, drowsiness and a falling GCS come first, while the late signs are a slow pulse, high BP and irregular breathing (Cushing's triad) and a dilated pupil. Check GCS and pupils every 15-60 minutes. Report a fall of 2 points at once.
2. **Position the head.** Raise the head of the bed to 30° with the neck straight, since this helps venous drainage from the head. Avoid neck flexion, tight tapes on the neck and hip flexion. Turn the whole body together.
3. **Protect the airway and the oxygen.** Give oxygen to keep the SpO2 at 94% or above, and suction briefly (under 10 seconds) because coughing and suction raise the ICP. Prepare for intubation if the GCS is 8 or less. Keep CO2 normal because high CO2 dilates the brain vessels.
4. **Control BP and temperature.** Keep CPP above 60 and avoid a sharp fall in BP, and treat fever with paracetamol and cooling, since each degree raises the brain's oxygen demand. Do not give sedatives unless ordered, as they hide the signs.
5. **Give osmotic drugs correctly.** Mannitol 20% is given over 15-30 minutes with a filter and a urinary catheter; watch the urine output, serum sodium and osmolality. It shrinks the brain by drawing water into blood. Do not give it if the serum osmolality exceeds 320 mOsm/kg.
6. **Reduce stimulation and prevent straining.** Cluster care, keep the room quiet, and give laxatives so the patient does not strain. Avoid coughing and the Valsalva manoeuvre because they raise the pressure. Allow the family to speak calmly.
7. **Give fluids and nutrition carefully.** Use isotonic saline and avoid glucose in water (hypotonic fluids swell the brain). Keep the fluid balance neutral and start tube feeding early. Check the sodium daily.
8. **Prevent complications and support the family.** Turn two-hourly, give eye and mouth care, use anti-embolism stockings and observe for seizures. Explain every change in the GCS to the family honestly and refer to rehabilitation.

## 3.2 Stroke

A **stroke** is the sudden loss of brain function from a blocked (**ischaemic**, about 85%) or burst (**haemorrhagic**) blood vessel. In ischaemic stroke a clot from the heart (atrial fibrillation) or from an atherosclerotic neck artery blocks a cerebral artery; in haemorrhagic stroke raised BP breaks a small vessel and blood destroys the brain (Plate 3.2a). Risk factors are hypertension, diabetes, smoking and bidi, atrial fibrillation, high cholesterol, heavy drinking and obesity. The **BE-FAST** signs are **B**alance loss, **E**yes (sudden vision loss), **F**ace drooping, **A**rm weakness, **S**peech difficulty and **T**ime to call: every minute without treatment destroys about 1.9 million neurons. A CT scan without contrast (blood is white) is done at once to tell ischaemic from haemorrhagic stroke. In a clot stroke, **IV alteplase can be given within 4.5 hours of the last time the patient was well**, and a **thrombectomy** within 6-24 hours in selected patients, where these services exist (available in Kathmandu hospitals). **Door-to-needle time should be under 60 minutes.**

```photogrid label="3.2" cols="4" ratio="1.0" caption="Neurological emergencies. (a) A real CT slice of the brain with an intracerebral haemorrhage: blood is the bright white area. (b) A real CT of an epidural haematoma (left panel, brain window) with the lens-shaped white collection under the skull on the patient's right, beside the same slice in bone window. (c) A real patient with Bell's palsy trying to smile: the mouth droops on one side. (d) A real lumbar puncture in progress: a spinal needle in the low back, with the skin cleaned with antiseptic."
@ photo id="nur6/ich" cap="Intracerebral haemorrhage"
fit 1.0
focus 0.5 0.5
mark 0.50 0.60 "1"
mark 0.10 0.50 "2"
key 1 (a) Bright white area: fresh blood inside the brain, with swelling around it
key 2 (a) Skull: the bright rim; blood cannot expand, so the pressure rises
@ photo id="nur6/edh" cap="Epidural haematoma"
fit 1.0
focus 0.0 0.5
mark 0.14 0.60 "3"
mark 0.34 0.55 "4"
key 3 (b) Lens-shaped bleed under the skull: classic epidural haematoma after a head blow
key 4 (b) Midline and ventricles: shifted away from the bleed when the mass is large
@ photo id="nur6/bell" cap="Bell's palsy"
fit 1.0
focus 0.5 0.5
mark 0.72 0.30 "5"
mark 0.28 0.62 "6"
key 5 (c) Mouth: drooping corner and a lost fold on the weak side
key 6 (c) Eye: the weak eyelid does not close fully; protect the cornea with drops and a patch at night
@ photo id="nur6/lp" cap="Lumbar puncture"
fit 1.0
focus 0.5 0.5
mark 0.50 0.62 "7"
mark 0.30 0.85 "8"
key 7 (d) Spinal needle between L3 and L4, below the end of the spinal cord
key 8 (d) Orange antiseptic on the skin: sterile technique prevents meningitis
```

```svgfig label="3.1" caption="Ischaemic stroke pathway in a Nepali hospital. Recognise BE-FAST, note the time last known well, call ahead, take the patient straight to CT, check glucose and BP, then treat: alteplase if within 4.5 hours and no bleed on CT, otherwise aspirin 300 mg after the CT; swallow screen before any oral intake; transfer for thrombectomy if available."
f = Fig(760, 250)
steps = [("1 BE-FAST signs\nNote time last\nknown well", ROSE, RED), ("2 Glucose, BP,\nECG, IV line\nCT brain at once", SAND, AMBER), ("3 Bleed on CT?", BLUE, NAVY)]
for i, (t, fl, st) in enumerate(steps):
    x = 10 + i * 200
    f.box(x, 20, 175, 70, t, fill=fl, stroke=st, size=11, bold=True)
    if i < 2: f.arrow([(x + 175, 55), (x + 200, 55)], sw=2)
f.arrow([(585, 55), (610, 55)], sw=2)
f.box(610, 20, 140, 70, "4 Swallow screen\nbefore food or drug", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(10, 150, 340, 80, "NO bleed, within 4.5 h: alteplase 0.9 mg/kg\n(10% bolus, rest over 60 min), BP below 185/110,\nno anticoagulant; monitor neuro obs every 15 min", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(380, 150, 370, 80, "BLEED or outside window: no alteplase; aspirin 300 mg\nonly if no bleed; BP control, ICP care, refer to\nneurosurgery; thrombectomy transfer where available", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(397, 90), (397, 125), (180, 125), (180, 150)], sw=1.6); f.arrow([(397, 125), (565, 125), (565, 150)], sw=1.6)
```

### Stroke: eight points of nursing care

1. **Act on time.** Note the time last known well, give the doctor the BE-FAST findings and arrange a CT at once. The treatable window is short. Record every clock time.
2. **Keep the airway and oxygen.** Position the patient on the side if drowsy, suction if needed and give oxygen only if the SpO2 is below 94%. Keep the head of the bed at 30° if the ICP is high. Do not give food, drink or tablets until a swallow screen is passed.
3. **Control the blood pressure.** Do not lower the BP quickly in a clot stroke unless it exceeds 220/120 (or 185/110 before alteplase); a sudden fall extends the brain damage. Check BP every 15 minutes during thrombolysis. Give drugs as ordered.
4. **Monitor neurology.** Check the GCS, pupils, speech, power and the face every 15 minutes in the first 2 hours of thrombolysis, then hourly. A new headache, vomiting or a fall in GCS during alteplase means a bleed: stop the infusion and call the doctor.
5. **Check glucose and temperature.** Treat glucose below 60 mg/dL at once and keep it at 140-180 mg/dL; treat fever above 37.5 °C. Both hypoglycaemia and fever worsen the stroke. Give paracetamol as ordered.
6. **Prevent complications.** Turn two-hourly, use an air mattress, give heel and eye care, use pneumatic compression or stockings and mobilise early. Place the weak arm on a pillow and never pull on the weak shoulder. Prevent pneumonia with swallow care and chest physiotherapy.
7. **Start rehabilitation early.** Position the limbs in good alignment, begin passive movements on day 1, and teach transfers and walking with the physiotherapist. Speak slowly to an aphasic patient with simple questions and gestures. Encourage self-care to build confidence.
8. **Teach secondary prevention.** Teach BP control, daily aspirin or other antiplatelet, a statin, anticoagulation for AF, glucose control, no tobacco or alcohol, less salt and regular walking. The CHA2DS2-VASc score guides AF anticoagulation: a 72-year-old woman with hypertension and diabetes scores 1 (age 65-74) + 1 + 1 + 1 (female) = **4**, so she needs an anticoagulant. Teach the family the FAST signs.

## 3.3 Head injury

Head injury follows road crashes (motorbikes without helmets are a main cause in Nepal), falls and assault. A blow can cause a **concussion**, a **skull fracture**, a **contusion** or bleeding. An **epidural haematoma** is arterial bleeding between the skull and the dura (often from the middle meningeal artery after a temporal fracture); the classic story is a blow, a **lucid interval** of minutes to hours and then a rapid fall in consciousness with a dilated pupil on the same side (Plate 3.2b). A **subdural haematoma** is venous bleeding below the dura, common in alcoholics and elderly people after a minor fall, which may present days or weeks later with confusion. Signs of a **base-of-skull fracture** are bruising behind the ear (Battle's sign), raccoon eyes and CSF leaking from the nose or ear. The nurse does primary survey (airway with cervical spine protection, breathing, circulation), uses the GCS for triage (13-15 mild, 9-12 moderate, 3-8 severe), keeps the neck immobilised until cleared, and arranges an urgent CT and neurosurgical referral. **Never put a nasogastric tube through the nose** in a suspected base-of-skull fracture, and do not plug a leaking ear or nose; cover it loosely with a sterile pad.

## 3.4 Seizures and epilepsy

A **seizure** is a burst of abnormal electrical activity in the brain; **epilepsy** is the tendency to repeated, unprovoked seizures. A **generalised tonic-clonic** seizure causes loss of consciousness, stiffening and jerking for 1-3 minutes followed by a sleepy, confused (postictal) state. Causes include birth injury, neurocysticercosis from pork tapeworm (common in parts of Nepal), head injury, stroke, meningitis, low glucose and alcohol withdrawal. **Status epilepticus** is a seizure lasting over 5 minutes, or repeated seizures without recovery, and it is an emergency. Diagnosis uses the history, EEG, CT or MRI and blood tests; treatment uses carbamazepine, sodium valproate, phenytoin or levetiracetam, taken regularly. Epilepsy carries stigma in Nepal, where it is sometimes blamed on spirits and treated by faith healers; nurses should counsel that it is a medical condition that can be controlled in about 70% of patients.

```python
wt = 70
load = 20 * wt                                   # phenytoin 20 mg/kg load
mins = load / 50                                 # maximum infusion rate 50 mg/min
dose, conc = 10, 5                               # diazepam 10 mg from 5 mg/mL
vol = dose / conc
age_pts, htn, dm, fem = 1, 1, 1, 1               # CHA2DS2-VASc for a 72-year-old woman
print(f"Phenytoin load = 20 x {wt} = {load:,} mg; at not more than 50 mg/min takes at least {mins:.0f} min")
print(f"Diazepam {dose} mg from {conc} mg/mL = {vol:.0f} mL, injected slowly at not more than 5 mg/min")
print(f"CHA2DS2-VASc = {age_pts} + {htn} + {dm} + {fem} = {age_pts + htn + dm + fem}")
```

```text
Phenytoin load = 20 x 70 = 1,400 mg; at not more than 50 mg/min takes at least 28 min
Diazepam 10 mg from 5 mg/mL = 2 mL, injected slowly at not more than 5 mg/min
CHA2DS2-VASc = 1 + 1 + 1 + 1 = 4
```

A 70 kg adult with status epilepticus who needs a phenytoin loading dose of 20 mg/kg receives **1,400 mg**, and since phenytoin must not run faster than 50 mg/min (to protect the heart and veins), the infusion takes at least **28 minutes** in normal saline only. Diazepam 10 mg from a 5 mg/mL ampoule is **2 mL**, given slowly, at not more than 5 mg/min, with resuscitation equipment nearby.

```svgfig label="3.2" caption="Status epilepticus time line for an adult. 0-5 minutes: protect, time the seizure, airway, oxygen, glucose. 5-20 minutes: first-line benzodiazepine (diazepam 10 mg IV or rectal, or midazolam 10 mg IM or buccal); repeat once if needed. 20-40 minutes: second-line IV phenytoin 20 mg/kg, valproate or levetiracetam. After 40 minutes: ICU, intubation and anaesthetic infusion."
f = Fig(760, 240)
cols = [("0-5 min", "Time it. Protect head,\nside position, oxygen,\ncheck glucose, IV line", BLUE, NAVY), ("5-20 min", "Diazepam 10 mg IV\n(2 mL of 5 mg/mL) or\nmidazolam IM; repeat once", SAND, AMBER), ("20-40 min", "Phenytoin 20 mg/kg\nat up to 50 mg/min\nor valproate, levetiracetam", ROSE, RED), ("Over 40 min", "ICU: intubate,\nanaesthetic infusion,\nEEG, find the cause", MINT, TEAL)]
for i, (h, t, fl, st) in enumerate(cols):
    x = 10 + i * 188
    f.box(x, 20, 170, 34, h, fill=st, stroke=st, color="#ffffff", size=12, bold=True)
    f.box(x, 62, 170, 90, t, fill=fl, stroke=st, size=10.5, bold=True)
    if i < 3: f.arrow([(x + 170, 107), (x + 188, 107)], sw=2)
f.box(10, 175, 740, 50, "Throughout: ECG and BP monitoring, suction ready, watch breathing after benzodiazepine; never put anything in the mouth", fill=SOFT, stroke=SLATE, size=11, bold=True)
```

### Seizure: eight points of first aid and nursing care

1. **Stay calm and note the time.** Look at the clock when the seizure begins and record how long it lasts and what happens. Seizures longer than 5 minutes need drugs. Good observation helps the doctor.
2. **Protect from injury.** Clear furniture and sharp objects, loosen tight clothes and put something soft under the head. Do not hold the person down. Restraint causes fractures and does not stop the fit.
3. **Put nothing in the mouth.** Do not force a spoon, a cloth or fingers between the teeth, and do not give water or tablets. This can break teeth and block the airway. The tongue cannot be swallowed.
4. **Open and keep the airway clear.** When the jerking stops, turn the person onto the side (recovery position), tilt the head back slightly and suction vomit or saliva. Give oxygen if the lips are blue. Stay until fully awake.
5. **Give emergency drugs as ordered.** If the seizure lasts over 5 minutes, give diazepam or midazolam as ordered, with monitoring of breathing. Check blood glucose, and give glucose if low. Keep the resuscitation trolley nearby.
6. **Observe and record afterwards.** Note the type, the body parts involved, the eye position, incontinence, injuries, the length of the postictal state and the vital signs. Check the neurological state. Report a first seizure, injury or a repeat.
7. **Teach about medicines.** Regular medicine at fixed times is the key, so missed doses cause fits. Never stop drugs suddenly, and do not share them. Give valproate and carbamazepine in correct doses and teach about sleepiness, rash and gum care with phenytoin.
8. **Teach safety and remove stigma.** Advise no swimming or tree climbing alone, no driving until seizure-free as the law and doctor advise, and care near fires and water. Explain to the family that epilepsy is not contagious and is not caused by spirits. Women should plan pregnancy with the doctor and take folic acid.

## 3.5 Meningitis, Parkinson's disease and other conditions

**Meningitis** is inflammation of the brain coverings. **Bacterial meningitis** (pneumococcus, meningococcus, Haemophilus) is an emergency with fever, severe headache, neck stiffness (**nuchal rigidity**), photophobia, vomiting, **Kernig's and Brudzinski's signs**, a purpuric rash in meningococcal disease and drowsiness. The diagnosis needs a **lumbar puncture (LP)** (Plate 3.2d) after checking for signs of raised ICP, with CSF examined for cells, protein, glucose, Gram stain and culture. Give IV ceftriaxone 2 g at once (do not wait for the LP) and dexamethasone as ordered; the nurse uses droplet isolation for the first 24 hours of antibiotics in meningococcal disease. **Tuberculous meningitis** is slower and common in Nepal, with a high protein and low glucose in the CSF. Prevention uses the **pneumococcal (PCV)** and **BCG** vaccines of the National Immunization Programme and JE vaccine at 12 months in endemic districts.

| CSF finding | Normal | Bacterial | Viral | Tuberculous |
|---|---|---|---|---|
| Appearance | Clear | Turbid | Clear | Clear or slightly turbid |
| Cells per mm³ | 0-5 lymphocytes | 100-5,000 neutrophils | 10-500 lymphocytes | 10-500 lymphocytes |
| Protein (mg/dL) | 15-45 | High (over 100) | Mild rise | Very high |
| Glucose | 60% of blood | Very low | Normal | Low |

### Meningitis: eight points of nursing care

1. **Give antibiotics at once.** Ceftriaxone must be started within 1 hour of suspecting bacterial meningitis, even before the CT or the LP. Delay increases death and deafness. Record the time given.
2. **Isolate and protect staff.** Use droplet precautions until 24 hours of effective antibiotics, with a mask for close contact. Give prophylaxis (ciprofloxacin or rifampicin) to household contacts of meningococcal disease as ordered. Report to the epidemiology unit.
3. **Assist with a lumbar puncture.** Explain the procedure, position the patient on the side with the knees to the chest and the back at the edge of the bed, keep the field sterile and label the tubes in order. Keep the patient flat for 1-4 hours as ordered after the procedure to reduce headache. Check the site for leaking.
4. **Monitor the neurology.** Check GCS, pupils, pulse, BP and temperature every 1-2 hours. A falling GCS or a slow pulse suggests raised ICP. Observe for seizures and prepare drugs.
5. **Reduce the headache and fever.** Give paracetamol, tepid sponging and a dark, quiet room. Photophobia makes light painful. Avoid sedatives that mask the signs.
6. **Maintain fluids and nutrition.** Give IV fluids to keep normal hydration without overload (cerebral oedema), and start tube feeding if the patient cannot swallow. Record the intake and output. Check the sodium daily.
7. **Protect the skin and prevent complications.** Turn two-hourly, give mouth and eye care and pad the bed rails for seizures. Check hearing before discharge, as deafness is the commonest sequel. Watch for hydrocephalus in children and adults.
8. **Teach and support.** Explain the illness and the reason for isolation, the importance of finishing the full antibiotic course, the vaccines for the family and the signs of relapse. Refer for rehabilitation of hearing, learning and movement problems.

**Parkinson's disease** is loss of dopamine neurons, causing **tremor at rest, rigidity, slow movement (bradykinesia)** and a stooped, shuffling walk; levodopa with carbidopa is the main drug, given 30 minutes before meals and not with a high-protein meal; the nurse prevents falls, gives a cueing and walking plan, ensures safe swallowing and never stops the drug suddenly. **Bell's palsy** is a sudden weakness of one side of the face from facial nerve inflammation (Plate 3.2c); the eye must be protected with artificial tears and a night patch, prednisolone is started within 72 hours, and most patients recover within weeks. **Guillain-Barré syndrome** is an ascending weakness after an infection; check the breathing (vital capacity) because it can lead to respiratory failure.

## Formula and fact sheet

- GCS = E (1-4) + V (1-5) + M (1-6), range 3-15; 8 or less needs the airway secured; CPP = MAP − ICP, target 60-70 mmHg.
- Alteplase 0.9 mg/kg (maximum 90 mg), 10% bolus, 90% over 60 minutes, within 4.5 hours; door-to-needle under 60 minutes; BE-FAST.
- Mannitol 0.5-1 g/kg of 20% solution (20 g per 100 mL); phenytoin load 20 mg/kg at not more than 50 mg/min; status epilepticus is a seizure over 5 minutes.
- Bacterial meningitis: ceftriaxone within 1 hour; CSF low glucose and high neutrophils; droplet precautions for 24 hours.

## Chapter summary

- The GCS, the pupils and the CPP guide care in raised ICP; keep the head up at 30°, protect the airway and avoid hypotonic fluids.
- Stroke is time-critical: BE-FAST, CT, glucose and BP, alteplase within 4.5 hours if no bleed, swallow screen, rehabilitation and secondary prevention.
- Head injury needs neck protection and neurological observation; epidural haematoma has a lucid interval.
- Seizure first aid protects and times the fit; status epilepticus is treated by benzodiazepine, phenytoin and ICU care; meningitis needs antibiotics within an hour.

## Practice

**MCQs (with reasons)**

1. A patient opens the eyes to voice (3), is confused (4) and localises pain (5). The GCS is: (a) 9 (b) 10 (c) 12 (d) 15.
2. MAP 90 mmHg and ICP 20 mmHg give a CPP of: (a) 20 (b) 50 (c) 70 (d) 110.
3. Alteplase 0.9 mg/kg for an 80 kg patient is: (a) 7.2 mg (b) 72 mg (c) 80 mg (d) 90 mg.
4. Mannitol 0.5 g/kg is ordered for a 60 kg patient as 20% solution. The volume is: (a) 30 mL (b) 60 mL (c) 150 mL (d) 300 mL.
5. The best position for a patient with raised ICP is: (a) flat with the legs raised (b) head of bed 30° with the neck straight (c) head down (d) sitting with the neck flexed.

::: note Answers and rationales
**1. (c).** E3 + V4 + M5 = 12; 15 is a fully alert person and 9 would need a lower motor score.
**2. (c).** CPP = MAP − ICP = 90 − 20 = 70 mmHg, which is in the target range of 60-70 or more; 110 forgets to subtract.
**3. (b).** 0.9 × 80 = 72 mg, below the 90 mg maximum; 7.2 mg is a tenfold error and 90 mg is the ceiling, not the dose.
**4. (c).** 0.5 × 60 = 30 g; a 20% solution has 20 g in 100 mL, so 30 ÷ 20 × 100 = 150 mL; 30 mL confuses grams with millilitres.
**5. (b).** Raising the head to 30° with a straight neck helps venous drainage and lowers the ICP; head-down and flexed neck raise the pressure.
:::

**Short answer (3 marks): Glasgow Coma Scale.** It is a standard score of consciousness from three responses: eye opening (1-4), verbal response (1-5) and best motor response (1-6), giving a total of 3-15. A score of 13-15 is mild, 9-12 moderate and 8 or less severe, and a patient with 8 or less needs airway protection. It is recorded on a chart at regular intervals and any fall of 2 points is reported.

**Medium answer (5 marks): Describe the first aid and nursing care of a patient during and after a generalised seizure (Figure 3.2).** *During:* note the time, stay with the patient, clear the area, put a soft pad under the head, loosen tight clothing, and do not restrain or put anything in the mouth. *After:* turn the patient onto the side, clear the airway, give oxygen if needed and check glucose, breathing, pulse and BP. If it lasts more than 5 minutes, give diazepam 10 mg IV (2 mL of 5 mg/mL) slowly or midazolam as ordered and call the doctor. *Record:* the type, duration, injuries and recovery time. *Teach:* regular medicine, safety and that epilepsy is not contagious or caused by spirits.

**Long answer (10 marks): Mr Hari Bahadur Magar, 66 years, a farmer from Dhading weighing 64 kg, is brought to the emergency department of a regional hospital with sudden right arm and leg weakness and slurred speech that began at 07:30 while he was last seen well. He has known hypertension and an irregular pulse. On arrival at 08:00: BP 180/100 mmHg, pulse 96 irregular, GCS 13 (E4 V3 M6), blood glucose 142 mg/dL. The CT shows no bleeding. Write the calculations and a nursing care plan.**

*Calculations.* His GCS is E4 + V3 + M6 = **13** and his MAP is (180 + 2 × 100) ÷ 3 = **126.7 mmHg**. The 4.5-hour window from 07:30 closes at **12:00**, and a door-to-needle time of 60 minutes from 08:00 means that alteplase should start by **09:00**. The BP of 180/100 is below 185/110, so he is eligible. Alteplase 0.9 mg/kg × 64 kg is **57.6 mg**: a **5.8 mg** bolus over 1 minute and **51.8 mg** over 60 minutes. If brain swelling develops, mannitol 0.5 g/kg is **32 g**, which is **160 mL** of 20% solution.

*Care.* Keep him nil by mouth until a swallow screen is done, place him with the head up 30° and give oxygen only if SpO2 falls below 94%. Insert two IV lines, send blood for count, clotting, glucose and electrolytes and record an ECG, which will confirm atrial fibrillation (the likely cause). Give alteplase through a pump after checking the dose with a second nurse. During and for 24 hours after the infusion record BP, pulse and GCS every 15 minutes for 2 hours, every 30 minutes for 6 hours and hourly after that, and keep the BP below 180/105. Stop the infusion and call the doctor for severe headache, vomiting, a fall in GCS or bleeding. Do not give aspirin, heparin or IM injections and do not insert a nasogastric tube or catheter for 24 hours unless necessary. Afterwards begin turning, passive limb movements, an anticoagulant for AF as ordered and referral for speech and physiotherapy. Teach the wife about BE-FAST, BP medicines, anticoagulant safety and follow-up, and discuss costs and rehabilitation with the social worker.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** wife says "He could not lift his arm." **O:** right hemiparesis, GCS 13, BP 180/100, AF. | **Risk for ineffective cerebral tissue perfusion** related to cerebral thrombo-embolism from atrial fibrillation. | **Tissue perfusion: cerebral:** GCS 15 and no new deficit at 24 hours; no bleeding. | 1. Neuro checks every 15 min; *early sign of extension or bleed.* 2. Give alteplase as per protocol; *dissolves the clot.* 3. Keep BP below 180/105; *reduces the bleeding risk.* 4. Head up 30°; *helps venous drainage.* | GCS 14, power improved to 3/5 at 24 hours; no bleeding. |
| **O:** slurred speech, facial droop, drooling. | **Risk for aspiration** related to impaired swallowing after stroke. | **Aspiration prevention:** no choking or chest infection. | 1. Nil by mouth until swallow screen; *prevents aspiration.* 2. Sit upright for feeding after clearance; *safe swallowing.* 3. Mouth care and suction ready; *protect the airway.* 4. Speech therapist referral; *specialist assessment.* | Swallow screen passed on day 2; chest clear. |
| **S:** "Words do not come out." **O:** slurred, slow speech. | **Impaired verbal communication** related to neurological damage, as evidenced by dysarthria. | **Communication:** makes needs known using words or signs by discharge. | 1. Speak slowly with short questions; *reduces the load.* 2. Use gestures, pictures and a call bell; *alternative methods.* 3. Allow time; *reduces frustration.* 4. Speech therapy; *rehabilitation.* | Uses simple words and gestures to ask for water and the toilet. |
| **O:** right arm and leg power 2/5; bed-bound. | **Impaired physical mobility** related to hemiparesis. | **Mobility:** sits at the bed edge on day 3; no pressure injury or contracture. | 1. Turn two-hourly and use an air mattress; *prevents pressure injury.* 2. Passive range-of-motion and positioning; *prevents contracture.* 3. Never pull the weak arm; *protects the shoulder.* 4. Early mobilisation with the physiotherapist; *speeds recovery.* | Sits supported on day 3; skin intact. |

::: tip Exam tip
For a stroke case write the GCS, the clock time of onset and the 4.5-hour window, the alteplase calculation (0.9 mg/kg, 10% bolus), BP limits, the swallow screen and four NANDA-I diagnoses beginning with risk for ineffective cerebral tissue perfusion.
:::

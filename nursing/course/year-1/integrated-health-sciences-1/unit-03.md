---
subject: Integrated Health Sciences I
grade: BSc Nursing Year 1
unit: 3
title: The Cardiovascular System and ECG
hours: 30
area: BSN 1 · Integrated Health Sciences I · Unit 3
---

The heart pumps about 7,000 litres of blood a day through two circuits. Nurses count its rate, listen to its sounds, read its tracing and treat its failures, so this unit covers the chambers and valves, the conduction system, the cardiac cycle, the ECG with its interval arithmetic, cardiac output, and the control of blood pressure that sits behind Nepal's PEN hypertension programme.

::: key What this unit gives you
- Heart chambers, valves and the two circulations in a flow diagram, with the conduction system.
- A real 12-lead ECG paired with a labelled waveform schematic, and a stethoscope photograph with auscultation areas.
- Cardiac output, stroke volume, ejection fraction, cardiac index, SVR, MAP and QTc worked step by step.
- Heart rate from an ECG strip by three methods.
- Eight points of health education against hypertension and heart disease, and model answers with a full care plan for heart failure.
:::

## 3.1 Structure of the heart and the two circulations

The heart is a four-chambered muscular pump in the middle mediastinum, two-thirds to the left of the midline, resting on the diaphragm; its apex points to the 5th left intercostal space in the mid-clavicular line. The wall has three layers: **epicardium**, **myocardium** and **endocardium**, and is covered by the double-layered pericardium. The right side pumps deoxygenated blood to the lungs (**pulmonary circulation**, low pressure) and the left side pumps oxygenated blood to the body (**systemic circulation**, high pressure, hence the thicker left ventricle). Valves keep flow one way: **tricuspid** (right atrium to ventricle), **pulmonary**, **mitral (bicuspid)** and **aortic**. The heart itself is fed by the right and left **coronary arteries**, which fill during diastole; blockage causes myocardial infarction.

```svgfig label="3.1" caption="Path of blood. Blue is deoxygenated and red is oxygenated blood. The four valves keep the flow one way. Pulmonary and systemic circuits are in series, so each carries the same output (about 5 L/min at rest)."
f = Fig(760, 220)
names = [("Body\n(tissues)", "#fef3c7", AMBER), ("Right\natrium", "#dbeafe", NAVY), ("Right\nventricle", "#dbeafe", NAVY), ("Lungs", "#e5e7eb", SLATE), ("Left\natrium", "#fee2e2", RED), ("Left\nventricle", "#fee2e2", RED)]
xs = [10 + i * 126 for i in range(6)]
for x, (n, fc, sc) in zip(xs, names): f.box(x, 40, 90, 46, n, fill=fc, stroke=sc, size=11, bold=True)
cols = [NAVY, NAVY, NAVY, RED, RED]
for i in range(5): f.arrow([(xs[i] + 90, 63), (xs[i + 1], 63)], color=cols[i], sw=2.5)
for i, v in enumerate(["vena cavae", "tricuspid", "pulmonary valve", "pulmonary veins", "mitral valve"]):
    f.text(xs[i] + 108, 104 + (14 if i % 2 else 0), v, size=10, color=SLATE, bold=True)
f.arrow([(xs[5] + 45, 86), (xs[5] + 45, 170), (xs[0] + 45, 170), (xs[0] + 45, 86)], color=RED, sw=2.5)
f.text(380, 188, "Aortic valve, then the systemic circulation back to the right atrium", size=11, color=RED, bold=True)
f.text(380, 20, "Pulmonary circulation: right ventricle to lungs to left atrium", size=11, color=NAVY, bold=True)
```

## 3.2 Conduction system and the cardiac cycle

The heart beats on its own (automaticity). The **sinoatrial (SA) node** in the right atrium is the pacemaker and fires at 60-100/min; the impulse crosses both atria, pauses about 0.1 s at the **AV node** (so the ventricles fill), runs down the **bundle of His** and its right and left branches, and spreads through **Purkinje fibres**, giving a coordinated ventricular squeeze from the apex up. If the SA node fails, the AV node (40-60/min) or Purkinje fibres (20-40/min) take over.

```svgfig label="3.2" caption="Conduction pathway with intrinsic rates. The delay at the AV node lets the ventricles fill before they contract."
f = Fig(760, 150)
st = [("SA node\n60-100/min\n(pacemaker)", TEAL), ("Atrial muscle\natria contract", NAVY), ("AV node\n40-60/min\n0.1 s delay", AMBER), ("Bundle of His\nand branches", NAVY), ("Purkinje fibres\n20-40/min\nventricles contract", RED)]
for i, (t_, c) in enumerate(st):
    x = 8 + i * 150; f.box(x, 40, 130, 66, t_, fill="#ffffff", stroke=c, size=10.5, color=c, bold=True)
    if i < 4: f.arrow([(x + 130, 73), (x + 150, 73)], color=SLATE, sw=2)
f.text(380, 22, "Impulse travels in this order", size=11, color=SLATE, bold=True)
```

**The cardiac cycle** lasts about 0.8 s at 75/min: **ventricular diastole** (about 0.5 s, filling) and **systole** (about 0.3 s, ejection). The first heart sound **S1 ("lub")** is the closing of the mitral and tricuspid valves at the start of systole, and **S2 ("dub")** is the closing of the aortic and pulmonary valves at its end. A murmur is a turbulent sound from a narrowed or leaking valve.

## 3.3 Cardiac output and haemodynamic numbers

- **Stroke volume (SV)** is the blood ejected per beat (about 70 mL). **Cardiac output (CO)** = heart rate × SV. At 72 beats/min and 70 mL: 72 × 70 = **5.04 L/min**. With exercise, 120 beats/min with the same SV gives **8.40 L/min**.
- If CO is 5000 mL/min at 80 beats/min, SV = 5000 ÷ 80 = **62.5 mL**.
- **Ejection fraction (EF)** = SV ÷ end-diastolic volume. For SV 70 and EDV 120: **58.3%** (normal 55-70%; below 40% is heart failure with reduced EF).
- **Cardiac index** = CO ÷ body surface area = 5.04 ÷ 1.7 = **2.96 L/min/m²** (normal 2.5-4.0).
- **MAP** = (SBP + 2 × DBP) ÷ 3 = (120 + 160) ÷ 3 = **93.3 mmHg**; for 130/85 it is **100.0 mmHg**.
- **Systemic vascular resistance** = (MAP − CVP) ÷ CO × 80. With CVP 5 mmHg: (93.3 − 5) ÷ 5.04 × 80 = **1402 dyn·s/cm⁵** (normal 800-1200).

Blood pressure is regulated at once by the **baroreceptors** in the carotid sinus and aortic arch (a fall in pressure raises heart rate and vasoconstriction), and over hours by the **renin-angiotensin-aldosterone system (RAAS)**: low renal perfusion releases renin, which makes angiotensin II (a vasoconstrictor) and aldosterone (sodium and water retention).

```svgfig label="3.3" caption="Renin-angiotensin-aldosterone system. ACE inhibitors (enalapril) block the conversion to angiotensin II; ARBs (losartan) block its receptor; spironolactone blocks aldosterone."
f = Fig(760, 200)
f.box(10, 70, 130, 54, "Low BP or low\nrenal perfusion", fill=ROSE, stroke=RED, size=11, bold=True)
f.box(170, 70, 100, 54, "Kidney\nreleases renin", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(300, 70, 130, 54, "Angiotensinogen →\nAngiotensin I", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.box(460, 70, 130, 54, "Angiotensin II\n(ACE in lung)", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(620, 10, 130, 50, "Vasoconstriction\nBP rises", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(620, 90, 130, 50, "Aldosterone: Na⁺\nand water retained", fill=MINT, stroke=TEAL, size=10.5, bold=True)
for a, b in [(140, 170), (270, 300), (430, 460)]: f.arrow([(a, 97), (b, 97)], color=SLATE, sw=2)
f.arrow([(590, 85), (620, 40)], color=AMBER, sw=2); f.arrow([(590, 110), (620, 115)], color=AMBER, sw=2)
f.text(525, 160, "ACE inhibitor blocks here", size=10.5, color=RED, bold=True); f.text(525, 176, "ARB blocks the receptor", size=10.5, color=RED, bold=True)
f.arrow([(685, 140), (685, 185), (200, 185), (200, 130)], color=TEAL, sw=1.6, dash=True)
```

## 3.4 The electrocardiogram (ECG)

The ECG records the electrical activity of the heart from electrodes on the skin; it does not show pumping. Standard paper runs at **25 mm/s**: one small square (1 mm) is **0.04 s** and one large square (5 mm) is **0.20 s**. The **P wave** is atrial depolarisation, the **QRS complex** is ventricular depolarisation, the **T wave** is ventricular repolarisation. The **PR interval** is 3-5 small squares, so at most 5 × 0.04 = **0.20 s**; a QRS is normally under 3 small squares, **0.12 s**.

**Heart rate from the strip.** (1) *Large-square method:* 300 ÷ large squares between two R waves. If R-R is 4 large squares, rate = **75/min**; if 2, rate = **150/min**. (2) *Small-square method:* 1500 ÷ small squares; for 20 small squares, **75/min**. (3) *Six-second method* for irregular rhythms: count the QRS complexes in a 6-second strip and multiply by 10; 8 complexes give **80/min**.

**QTc.** Bazett's formula corrects the QT interval for rate: QTc = QT ÷ √RR (seconds). At 75/min the R-R interval is 0.8 s, so a QT of 400 ms gives QTc = 400 ÷ √0.8 = **447 ms**, which is borderline (above 450 ms in men and 460 ms in women is prolonged and carries a risk of torsades).

```photogrid label="3.1" cols="2" ratio="1.6" caption="ECG. (a) A real 12-lead tracing on pink grid paper with sinus rhythm. (b) The labelled single-beat schematic: each large square is 0.20 s."
@ photo id="nur1/ecg" cap="12-lead ECG, sinus rhythm"
fit 1.6
focus 0.3 0.5
mark 0.40 0.70 "1"
mark 0.15 0.30 "2"
key 1 (a) QRS complexes: sharp spikes, regular spacing means regular rhythm
key 2 (a) The pink grid of small and large squares used to time the beat
@ svg cap="One normal ECG beat"
import math
f = Fig(380, 240)
for i in range(0, 361, 20): f.line(10 + i, 20, 10 + i, 200, color="#fbcfe8", sw=1 if i % 100 else 1.6)
for j in range(0, 181, 20): f.line(10, 20 + j, 370, 20 + j, color="#fbcfe8", sw=1)
base = 130; pts = []
for x in range(10, 371, 2):
    t = x - 10
    y = base - 12 * math.exp(-((t - 60) / 12) ** 2) - 14 * math.exp(-((t - 235) / 22) ** 2)
    y += -75 * math.exp(-((t - 135) / 3.5) ** 2) + 22 * math.exp(-((t - 126) / 3) ** 2) + 14 * math.exp(-((t - 146) / 3) ** 2)
    pts.append((x, y))
for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=2.2)
f.text(70, 106, "P", size=12, color=TEAL, bold=True); f.text(145, 44, "R", size=12, color=RED, bold=True)
f.text(120, 168, "Q", size=11, color=SLATE, bold=True); f.text(153, 168, "S", size=11, color=SLATE, bold=True); f.text(245, 100, "T", size=12, color=AMBER, bold=True)
f.arrow([(50, 215), (128, 215)], color=TEAL, sw=1.4, both=True); f.text(89, 230, "PR 0.12-0.20 s", size=10, color=TEAL, bold=True)
f.arrow([(120, 190), (160, 190)], color=RED, sw=1.4, both=True); f.text(222, 190, "QRS under 0.12 s", size=10, color=RED, bold=True)
```

## 3.5 Auscultation of the heart

The stethoscope **diaphragm** hears high-pitched sounds (S1, S2, murmurs) and the **bell** hears low-pitched sounds (S3, mitral stenosis). Listen in a quiet room with the patient lying at 30 degrees or sitting, and always count the **apical pulse for one full minute**.

```photogrid label="3.2" cols="2" ratio="1.35" caption="Auscultation. (a) A stethoscope: chest piece with a diaphragm on one side and a bell on the other, binaurals and tubing. (b) The five areas on the chest wall (ICS = intercostal space)."
@ photo id="nur1/steth" cap="Stethoscope"
fit 1.35
focus 0.65 0.7
mark 0.70 0.15 "1"
mark 0.30 0.78 "2"
key 1 (a) Chest piece: flat diaphragm, bell on the reverse
key 2 (a) Ear tips angled forward to follow the ear canal
@ svg cap="Valve areas on the chest"
f = Fig(330, 240)
f.line(70, 10, 70, 230, color=SLATE, sw=8)
for y in (50, 85, 120, 155, 190): f.line(15, y, 125, y, color="#cbd5e1", sw=1.5)
for n, x, y, c in [("A", 40, 50, RED), ("P", 100, 50, NAVY), ("E", 100, 85, SLATE), ("T", 95, 155, TEAL), ("M", 112, 172, AMBER)]:
    f.circle(x, y, 11, fill="#ffffff", stroke=c, sw=2.5, label=n, size=11, color=c)
for i, (n, s, c) in enumerate([("A", "Aortic: 2nd right\nintercostal space (ICS)", RED), ("P", "Pulmonary: 2nd left ICS", NAVY), ("E", "Erb's point: 3rd left ICS", SLATE), ("T", "Tricuspid: 4th-5th left ICS\nat the sternal border", TEAL), ("M", "Mitral (apex): 5th left ICS,\nmid-clavicular line", AMBER)]):
    y = 34 + i * 42
    f.circle(150, y + 6, 9, fill="#ffffff", stroke=c, sw=2, label=n, size=10, color=c)
    f.text(168, y + 6, s, size=10, color=c, bold=True, anchor="start", vmid=True)
```

```python
import math
co = 72 * 70 / 1000
ef = 70 / 120 * 100
mapv = (120 + 2 * 80) / 3
svr = (mapv - 5) / co * 80
qtc = 400 / math.sqrt(60 / 75)
print("CO L/min", f"{co:.2f}")
print("EF %", f"{ef:.1f}")
print("MAP", f"{mapv:.1f}")
print("SVR", f"{svr:.0f}")
print("QTc ms", f"{qtc:.0f}")
print("HR, R-R 4 large squares", 300 // 4)
```

```text
CO L/min 5.04
EF % 58.3
MAP 93.3
SVR 1402
QTc ms 447
HR, R-R 4 large squares 75
```

## 3.6 Health education to prevent hypertension and heart disease: eight points

Nepal's **Package of Essential Non-Communicable Disease Interventions (PEN)** screens adults at health posts and treats hypertension from 140/90 mmHg. Nurses teach these eight points at every contact.

1. **Cut salt.** Keep salt below 5 g (one level teaspoon) a day, including pickles (achar), dried fish, instant noodles and salty tea (noon chiya). Salt holds water in the blood and raises pressure. Read packet labels and add salt after cooking, not before.
2. **Eat a heart-friendly diet.** Eat green leafy vegetables, fruit, lentils and whole grain daily, and limit ghee, fried snacks (sel roti, samosa) and red meat. Fibre and potassium lower pressure and cholesterol. Use mustard oil sparingly.
3. **Move every day.** Walk briskly or cycle for at least 150 minutes a week, 30 minutes on five days. Exercise strengthens the heart, lowers weight and improves blood sugar. Start slowly if you are old or have symptoms.
4. **Stop tobacco.** Smoking, hookah and chewing tobacco damage the artery lining and raise clot risk, and a smoker has about double the heart-attack risk. Quitting benefits within weeks. Refer to the tobacco cessation service and avoid second-hand smoke.
5. **Limit alcohol.** Local raksi and chhyang in large amounts raise BP and weaken heart muscle. Advise not more than one drink a day for women and two for men, or none if on treatment. Never drive after drinking.
6. **Watch weight and waist.** Keep BMI below 23 (South Asian cut-off) and waist under 90 cm for men and 80 cm for women. Central fat raises insulin resistance and BP. Weigh monthly.
7. **Check pressure and take medicines.** Adults over 25 should check BP yearly and hypertensives monthly. Take tablets such as amlodipine or losartan daily even when feeling well, since hypertension has no symptoms. Never stop suddenly, and carry the PEN card.
8. **Know the warning signs.** Chest pain or pressure spreading to the left arm or jaw, sweating, sudden breathlessness, facial droop, arm weakness or slurred speech need urgent transport to the nearest hospital. Chew a 300 mg aspirin for suspected heart attack unless allergic. Reduce stress by sleep, prayer or yoga.

## Formula and fact sheet

- CO = HR × SV (5.04 L/min at 72 × 70 mL). SV = CO ÷ HR. EF = SV ÷ EDV (58.3% for 70/120). CI = CO ÷ BSA (2.96).
- MAP = (SBP + 2 × DBP) ÷ 3 (93.3 for 120/80). SVR = (MAP − CVP) ÷ CO × 80 (1402).
- ECG: 1 small square 0.04 s, 1 large 0.20 s. Rate = 300 ÷ large squares = 1500 ÷ small squares = QRS in 6 s × 10. QTc = QT ÷ √RR (447 ms for QT 400, 75/min).
- Pacemaker rates: SA 60-100, AV 40-60, Purkinje 20-40 per minute. S1 closure of AV valves, S2 closure of aortic and pulmonary valves.

## Chapter summary

- The right heart serves the lungs, the left heart serves the body; valves ensure one-way flow.
- The SA node paces the heart, the AV node delays the impulse, Purkinje fibres spread it.
- ECG intervals and heart rate come from counting squares; QTc corrects for rate.
- Cardiac output depends on rate and stroke volume; BP is held by baroreceptors and RAAS.
- Prevention in Nepal rests on salt reduction, activity, no tobacco, BP screening (PEN) and early referral.

## Practice

**MCQs (with reasons)**

1. The normal pacemaker of the heart is the: (a) AV node (b) SA node (c) bundle of His (d) Purkinje fibre.
2. On an ECG, R-R is 4 large squares. The heart rate is: (a) 60 (b) 75 (c) 100 (d) 150.
3. Stroke volume 70 mL at 72 beats/min gives a cardiac output of: (a) 3.5 L/min (b) 5.04 L/min (c) 7.2 L/min (d) 50.4 L/min.
4. The first heart sound is produced by closure of the: (a) aortic and pulmonary valves (b) mitral and tricuspid valves (c) coronary valves (d) venous valves.
5. ACE inhibitors lower BP by blocking the formation of: (a) renin (b) angiotensin II (c) aldosterone (d) adrenaline.

::: note Answers and rationales
**1. (b).** The SA node has the fastest intrinsic rate (60-100/min), so it controls the heart; the AV node (40-60) and Purkinje fibres (20-40) only take over on failure.
**2. (b).** 300 ÷ 4 = 75/min. A value of 150 would need an R-R of 2 large squares.
**3. (b).** 72 × 70 = 5,040 mL = 5.04 L/min. Option (d) forgets to convert mL to litres.
**4. (b).** S1 ("lub") is closure of the mitral and tricuspid valves as the ventricles begin to contract; S2 is closure of the semilunar valves.
**5. (b).** ACE converts angiotensin I to angiotensin II, a strong vasoconstrictor; blocking it lowers vascular tone and aldosterone release.
:::

**Short answer (3 marks): Cardiac output and its determinants.** Cardiac output is the volume of blood pumped by each ventricle per minute, equal to heart rate times stroke volume: 72 × 70 mL = 5.04 L/min at rest. Stroke volume depends on preload (venous return, Starling's law), afterload (resistance the ventricle pumps against) and contractility. Heart rate is raised by sympathetic and lowered by vagal stimulation. Cardiac index divides CO by body surface area (2.96 L/min/m² for 1.7 m²).

**Medium answer (5 marks): Describe the conduction system of the heart and the normal ECG (Figures 3.2 and 3.1).** The impulse starts in the **SA node** (60-100/min), spreads across the atria (P wave, atrial contraction), and is delayed 0.1 s at the **AV node** so that ventricles fill. It then travels down the **bundle of His**, right and left bundle branches and **Purkinje fibres**, depolarising both ventricles from apex upward (QRS complex, under 0.12 s). Repolarisation of the ventricles gives the **T wave**. The PR interval (0.12-0.20 s) measures conduction from atria to ventricles, the ST segment is isoelectric, and the QT interval is the time of ventricular activity (QTc under 450 ms). Paper speed is 25 mm/s, so 1 small square is 0.04 s, and rate is 300 ÷ large squares. ST elevation suggests myocardial infarction and a long PR suggests AV block.

**Long answer (10 marks): Mr Ram Bahadur Gurung, 62, a known hypertensive, comes to the emergency of a provincial hospital with 3 days of breathlessness on lying flat, ankle swelling and fatigue. Pulse 110/min, BP 100/60 mmHg, RR 28/min, SpO₂ 90%, bibasal crackles, raised JVP, pitting oedema. Stroke volume is estimated at 45 mL with an end-diastolic volume of 130 mL. Discuss the condition and prepare a nursing care plan.**

*Introduction.* The picture is acute decompensated left and right heart failure. His ejection fraction is 45 ÷ 130 = **34.6%** (normal 55-70%), so the pump is weak, and his cardiac output is 110 × 45 ÷ 1000 = **4.95 L/min**, below the resting 5 L/min. The MAP is (100 + 120) ÷ 3 = **73.3 mmHg**, so perfusion is borderline. Falling output activates RAAS and the sympathetic system, which retain salt and water and raise the afterload, so the lungs flood (crackles, orthopnoea) and the veins congest (oedema, raised JVP). Management: sit upright, oxygen to keep SpO₂ at 94% or above, IV furosemide, ACE inhibitor or ARB, beta-blocker and spironolactone as ordered once stable, a 12-lead ECG, chest X-ray, echocardiogram and renal function, fluid restriction (about 1.5 L/day) and salt below 2 g/day.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I cannot sleep lying down." **O:** P 110, BP 100/60, EF 34.6%, cool peripheries. | **Decreased cardiac output** related to altered contractility, as evidenced by tachycardia, hypotension and low ejection fraction. | **Cardiac pump effectiveness:** P below 100, MAP at least 65, urine at least 0.5 mL/kg/h in 24 h. | 1. Continuous ECG and vitals every 15-30 min; *detects arrhythmia and hypotension.* 2. Give ACE inhibitor and diuretic as ordered, check BP before each dose; *reduces afterload and preload.* 3. Position upright with legs down; *reduces venous return and lung congestion.* 4. Record hourly urine; *shows renal perfusion and diuretic response.* | Pulse, BP and urine reviewed each hour; goal met when targets are reached. |
| **O:** RR 28, SpO₂ 90%, bibasal crackles, orthopnoea. | **Impaired gas exchange** related to pulmonary congestion, as evidenced by dyspnoea and hypoxaemia. | **Respiratory status: gas exchange:** SpO₂ at least 94%, RR 12-20 in 6 h. | 1. Oxygen via mask or cannula as ordered; *corrects hypoxaemia.* 2. High Fowler's position and deep breathing coaching; *increases lung expansion.* 3. Auscultate chest each 4 h; *tracks crackles.* | SpO₂ and RR hourly; oxygen weaned as target is held. |
| **O:** pitting oedema 3+, JVP raised, weight 4 kg above usual. | **Excess fluid volume** related to compromised regulatory mechanism, as evidenced by oedema and weight gain. | **Fluid balance:** weight down 1 kg/day, oedema 1+ or less in 5 days. | 1. Daily morning weight and strict input-output; *the most sensitive measure of fluid.* 2. Restrict fluid to 1.5 L and salt below 2 g; *limits retention.* 3. Skin care and leg elevation; *prevents breakdown of oedematous skin.* 4. Teach daily weighing at home and a 2 kg rise in 3 days to be reported; *early warning of relapse.* | Weight chart and oedema grade each day; goal met when weight loss is steady. |

::: tip Exam tip
For heart failure always quote the numbers: EF, CO and MAP, then link each symptom to either the congested lungs (left) or the congested veins (right). The examiner rewards the link between physiology and nursing action.
:::

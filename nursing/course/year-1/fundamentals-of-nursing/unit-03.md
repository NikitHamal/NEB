---
subject: Fundamentals of Nursing
grade: BSc Nursing Year 1
unit: 3
title: Vital Signs and Health Assessment
hours: 18
area: BSN 4 · Fundamentals of Nursing · Unit 3
---

Vital signs are the first numbers a nurse collects and the first warning of a patient going wrong. This unit covers temperature, pulse, respiration, blood pressure and oxygen saturation, the derived numbers (MAP, pulse pressure, shock index, BMI) and the Glasgow Coma Scale, all with worked arithmetic.

::: key What this unit gives you
- Normal adult ranges and the equipment, with real photographs of a sphygmomanometer, pulse oximeter and two thermometers.
- Correct technique and common errors for each vital sign.
- MAP, pulse pressure, shock index, BMI, GCS, temperature conversion and intake-output balance, every one computed and checked.
- Eight points on nursing care of a patient with fever.
- Model answers, including a full care plan for hyperthermia.
:::

## 3.1 Normal adult values

| Vital sign | Normal adult range | Alert if |
|---|---|---|
| Temperature (oral) | 36.5 to 37.5 °C (97.7 to 99.5 °F) | 38 °C or above, or below 36 °C |
| Pulse | 60 to 100 beats/min | below 50 or above 120 |
| Respiration | 12 to 20 breaths/min | below 10 or above 24 |
| Blood pressure | about 120/80 mmHg; Nepal PEN treats 140/90 and above as hypertension | systolic below 90 or above 180 |
| SpO₂ (room air) | 95 to 100% | below 92% |

```photogrid label="3.1" cols="4" ratio="1.0" caption="The instruments of vital signs. (a) Aneroid sphygmomanometer on a patient's arm. (b) Finger pulse oximeter. (c) Digital thermometer with a flexible tip. (d) Clinical mercury-in-glass thermometer. Mercury devices are being withdrawn worldwide because of mercury toxicity."
@ photo id="nur4/bp" cap="Aneroid BP cuff and gauge"
fit 1.0
focus 0.55 0.5
mark 0.80 0.80 "1"
mark 0.35 0.45 "2"
key 1 Dial gauge in mmHg
key 2 Cuff over the brachial artery
@ photo id="nur4/spo2" cap="Pulse oximeter"
fit 1.0
focus 0.4 0.5
mark 0.28 0.62 "1"
key 1 Sensor clip on the fingertip shows SpO2 and pulse
@ photo id="nur4/thermo-digital" cap="Digital thermometer"
fit 1.0
focus 0.62 0.5
mark 0.50 0.58 "1"
key 1 LCD shows the reading (°C)
@ photo id="nur4/thermo-hg" cap="Mercury-in-glass thermometer"
fit 1.0
mark 0.50 0.50 "1"
key 1 Scale 35 to 42 °C; 37 marked in red
```

## 3.2 Body temperature

Temperature is the balance between heat produced (metabolism, muscle activity) and heat lost (radiation, conduction, convection, evaporation). The hypothalamus is the thermostat. **Sites:** oral, axillary (about 0.5 °C lower), rectal (about 0.5 °C higher), tympanic and temporal. In Nepali wards the axillary route with a digital thermometer is the usual one; leave it in place for the beep (about 1 minute) with the arm pressed to the chest.

**Conversions.** °F = (°C × 9/5) + 32 and °C = (°F − 32) × 5/9. A patient at 38.5 °C is at 38.5 × 9/5 + 32 = **101.3 °F**; a chart reading of 98.6 °F equals **37.0 °C**; 102.2 °F equals **39.0 °C**.

**Fever (pyrexia)** is a core temperature above 38 °C. Patterns: *continuous* (small variation, typhoid), *intermittent* (returns to normal daily, malaria) and *remittent* (varies but never normal). **Hypothermia** is below 35 °C.

## 3.3 Pulse

The pulse is the pressure wave of blood in an artery with each heartbeat. Sites: **temporal, carotid, brachial, radial, femoral, popliteal, posterior tibial, dorsalis pedis** and the apex of the heart (apical, heard with a stethoscope at the 5th left intercostal space). Assess **rate, rhythm, volume and tension**. For a regular pulse count 30 seconds × 2 or 15 seconds × 4; for an irregular pulse count a **full minute**. If 18 beats are counted in 15 seconds, the rate is 18 × 4 = **72 /min**. A rate above 100 is tachycardia; below 60, bradycardia. A pulse deficit (apical minus radial rate) suggests atrial fibrillation.

```svgfig label="3.1" caption="Pulse points on the body. Radial is the routine site; carotid is used in cardiac arrest; apical is used in infants and arrhythmia."
f = Fig(760, 340)
f.circle(380, 40, 20, fill=SOFT, stroke=SLATE, label="")
f.line(380, 60, 380, 200, color=SLATE, sw=6)
f.line(380, 90, 300, 160, color=SLATE, sw=5); f.line(380, 90, 460, 160, color=SLATE, sw=5)
f.line(380, 200, 350, 310, color=SLATE, sw=6); f.line(380, 200, 410, 310, color=SLATE, sw=6)
pts = [("Temporal", 360, 30, 190, 22), ("Carotid", 372, 70, 190, 62), ("Brachial", 330, 120, 190, 108), ("Radial", 300, 160, 190, 154), ("Apical", 395, 110, 570, 70), ("Femoral", 366, 205, 570, 140), ("Popliteal", 357, 255, 570, 200), ("Dorsalis pedis", 350, 308, 570, 270)]
for n, x, y, tx, ty in pts:
    f.circle(x, y, 4, fill=RED, stroke=RED)
    f.arrow([(tx + (60 if tx < 380 else -10), ty), (x + (-6 if tx < 380 else 6), y)], color=AMBER, sw=1.2)
    f.text(tx, ty, n, size=11.5, color=NAVY, bold=True, anchor="start" if tx > 380 else "end")
```

## 3.4 Respiration

One respiration is one inspiration plus one expiration. Count for **a full minute without telling the patient** (they change the rate if they know), while appearing to hold the pulse. If 9 breaths are counted in 30 seconds, the rate is 9 × 2 = **18 /min**. Note depth, rhythm, effort and use of accessory muscles. Terms: **tachypnoea** (above 20), **bradypnoea** (below 12), **apnoea** (absence), **dyspnoea** (difficulty), **Kussmaul** (deep, fast, in diabetic ketoacidosis), **Cheyne-Stokes** (waxing and waning with pauses, near death or in brain injury).

## 3.5 Blood pressure

BP is the force of blood against the arterial wall. **Systolic** is the pressure during ventricular contraction, **diastolic** during relaxation. **Pulse pressure** = systolic − diastolic; for 120/80 it is **40 mmHg**. **Mean arterial pressure** = (SBP + 2 × DBP) ÷ 3 is the average pressure that drives organ perfusion; at least 65 mmHg is needed. For 120/80: (120 + 160) ÷ 3 = **93.3 mmHg**; for 90/60: **70.0 mmHg**; for 160/100: **120.0 mmHg**.

**Auscultatory method.** Patient rested 5 minutes, seated, arm at heart level, no tight sleeve. The **cuff bladder width is about 40% and length about 80% of the arm circumference**, applied 2.5 cm above the elbow with the artery marker over the brachial artery. Inflate to 30 mmHg above the point where the radial pulse disappears, then deflate at 2-3 mmHg per second. The first sound is systolic (Korotkoff phase I) and the disappearance is diastolic (phase V).

```svgfig label="3.2" caption="Cuff deflation and Korotkoff sounds. The first tapping sound marks the systolic pressure (120), the point where sound disappears marks the diastolic (80)."
f = Fig(760, 250)
f.line(60, 20, 60, 210, color=SLATE); f.line(60, 210, 720, 210, color=SLATE)
f.text(30, 16, "mmHg", size=11, color=SLATE)
for v, y in [(160, 50), (120, 90), (80, 150), (40, 190)]:
    f.line(55, y, 720, y, color="#e2e8f0", sw=1); f.text(40, y, str(v), size=10.5, color=SLATE)
f.arrow([(90, 50), (650, 190)], color=NAVY, sw=2.5)
f.text(110, 36, "cuff inflated", size=11, color=NAVY, bold=True, anchor="start")
for x in range(300, 470, 28):
    f.line(x, 196, x, 176 - (x % 5), color=TEAL, sw=2)
f.line(60, 90, 300, 90, color=RED, dash=True); f.text(310, 76, "Systolic 120: first tapping sound (phase I)", size=11, color=RED, bold=True, anchor="start")
f.line(60, 150, 480, 150, color=AMBER, dash=True); f.text(490, 142, "Diastolic 80: sounds disappear (phase V)", size=11, color=AMBER, bold=True, anchor="start")
f.text(660, 228, "time", size=10.5, color=SLATE)
```

::: caution Common errors in BP measurement
A cuff that is **too small gives a falsely high reading**; a cuff over clothing, a full bladder, talking, a dangling arm and an arm below heart level all raise the reading. Deflating too fast underestimates systolic and overestimates diastolic. Recheck after 1-2 minutes before reporting.
:::

## 3.6 Oxygen saturation (SpO₂)

A pulse oximeter uses red and infrared light to estimate the percentage of haemoglobin carrying oxygen. Normal is 95-100%; below 90% is hypoxaemia and needs oxygen and a doctor. Readings are false in cold fingers, nail polish, poor perfusion, movement, severe anaemia and carbon monoxide poisoning. Check that the pulse on the device matches the radial pulse.

## 3.7 Health assessment: BMI, GCS, shock index and intake-output

- **BMI** = weight (kg) ÷ height (m)². A woman of 54 kg and 1.58 m has BMI 54 ÷ 2.4964 = **21.6** (normal 18.5-24.9; WHO Asia-Pacific proposes 23 as the overweight cut-off for South Asians).
- **Glasgow Coma Scale:** Eye 1-4, Verbal 1-5, Motor 1-6, total 3-15. A patient who opens eyes to voice (E3), is confused (V4) and localises pain (M5) scores 3 + 4 + 5 = **12**; 8 or less means intubation is considered.
- **Shock index** = heart rate ÷ systolic BP. HR 110 and BP 88 systolic gives **1.25**; above 0.9 suggests shock.
- **Intake-output:** intake 1850 mL, output 1500 mL gives a positive balance of **350 mL**.

```python
sbp, dbp = 120, 80
print("MAP", round((sbp + 2 * dbp) / 3, 1))
print("PP", sbp - dbp)
w, h = 54, 1.58
print("BMI", round(w / h ** 2, 1))
print("F", round(38.5 * 9 / 5 + 32, 1))
```

```text
MAP 93.3
PP 40
BMI 21.6
F 101.3
```

## 3.8 Nursing care of a patient with fever: eight points

1. **Measure accurately.** Record temperature, pulse and respiration every 4 hours, or every hour if above 39 °C. A rising temperature with a falling BP is an emergency. Use the same site every time so that readings can be compared.
2. **Remove heat sources.** Take off extra blankets, use light cotton clothes and keep the room cool and ventilated. Heavy covers trap heat. Do not remove covers during shivering until the chill passes.
3. **Tepid sponging.** If the temperature is above 39 °C, sponge with lukewarm water for 15-20 minutes, and stop if the patient shivers. Cold water or alcohol causes shivering, which raises heat. Re-measure 30 minutes later.
4. **Give antipyretics.** Give paracetamol as prescribed (not aspirin to children, because of Reye's syndrome) and record the time and effect. Never give a dose earlier than the interval ordered. Check the dose against weight in children.
5. **Maintain fluids.** Encourage 2-3 litres a day or give IV fluids as ordered, because fever increases fluid loss through sweat and faster breathing. Use ORS in diarrhoeal fever. Record intake and output.
6. **Provide nutrition.** Offer small, light, high-calorie meals, as metabolism is raised. Fever causes anorexia, so offer favourites. Weigh if fever is prolonged.
7. **Skin and mouth care.** Change damp linen, give a bed bath and mouth care four times a day, because dry cracked lips and a coated tongue are common. Moisturise lips. Check pressure areas.
8. **Find the cause and report.** Look for the source: urinary, chest, wound, IV site, malaria or dengue in season. Send blood or other cultures as ordered before antibiotics. Report persistent fever, rash or altered consciousness at once.

## Formula and fact sheet

- °F = °C × 9/5 + 32; °C = (°F − 32) × 5/9.
- Pulse pressure = SBP − DBP. MAP = (SBP + 2 × DBP) ÷ 3.
- BMI = kg ÷ m². Shock index = HR ÷ SBP. GCS = E + V + M (3-15).
- Cuff width 40%, length 80% of the arm circumference.

## Chapter summary

- Measure each vital sign with the right method; count irregular pulses for a full minute and respiration without warning.
- BP depends on cuff size, arm position and deflation speed.
- Derived numbers (MAP, BMI, GCS, shock index) turn readings into decisions.
- Fever care is cooling, fluids, antipyretic, nutrition, hygiene and finding the cause.

## Practice

**MCQs (with reasons)**

1. A BP cuff that is too narrow gives: (a) a falsely low reading (b) a falsely high reading (c) no change (d) a variable pulse.
2. MAP for BP 90/60 mmHg is: (a) 70 (b) 75 (c) 80 (d) 150.
3. An irregular pulse is counted for: (a) 15 seconds (b) 30 seconds (c) 1 full minute (d) 2 minutes.
4. A patient opens eyes to voice, is confused and localises pain. GCS is: (a) 9 (b) 10 (c) 12 (d) 15.
5. 102.2 °F equals: (a) 38 °C (b) 39 °C (c) 40 °C (d) 41 °C.

::: note Answers and rationales
**1. (b).** A narrow cuff needs more pressure to compress the artery, so the reading is too high. A wide cuff gives a low reading.
**2. (a).** (90 + 2 × 60) ÷ 3 = 70. The other numbers are arithmetic slips such as adding without doubling the diastolic.
**3. (c).** Irregular beats vary, so only a full minute is reliable.
**4. (c).** E3 + V4 + M5 = 12. The patient is moderately impaired.
**5. (b).** (102.2 − 32) × 5/9 = 39.0.
:::

**Short answer (3 marks): Mean arterial pressure and pulse pressure.** Pulse pressure is the difference between systolic and diastolic pressure (120 − 80 = 40 mmHg) and reflects stroke volume and arterial stiffness. MAP is the mean pressure during the cardiac cycle, calculated as (SBP + 2 × DBP) ÷ 3, giving 93.3 mmHg for 120/80. A MAP of at least 65 mmHg is needed to perfuse the kidneys and brain; below this, shock is suspected.

**Medium answer (5 marks): Describe the steps and precautions in recording blood pressure (Figure 3.2).** Explain the procedure and rest the patient for 5 minutes, seated, back supported, arm bare and supported at heart level. Choose a cuff whose bladder is 40% of the arm circumference in width and 80% in length. Wrap it snugly 2.5 cm above the elbow with the marker over the brachial artery. Palpate the radial pulse and inflate until it disappears, then add 30 mmHg. Place the stethoscope diaphragm over the brachial artery and deflate at 2-3 mmHg per second. Note the first Korotkoff sound as systolic and the disappearance as diastolic. Wait 1-2 minutes before repeating, and record the arm, position and values. Precautions: no talking, empty bladder, never measure on a limb with IV, fistula or mastectomy, and calibrate the aneroid gauge to zero regularly.

**Long answer (10 marks): Mr Hari Prasad, 58, admitted to the medical ward with pneumonia. T 39.0 °C (102.2 °F), pulse 108/min, RR 26/min, BP 100/60, SpO₂ 91%. He is sweating and restless. Describe the nursing care with a care plan.**

*Introduction.* The vitals show fever, tachycardia, tachypnoea and borderline hypoxia. His MAP is (100 + 120) ÷ 3 = 73 mmHg, acceptable but watched, and his shock index is 108 ÷ 100 = 1.08, above 0.9, so deterioration is possible. Priorities by ABC: **breathing first (SpO₂ 91%)**, then circulation and temperature. Sit him upright (Fowler's), start oxygen as ordered to keep SpO₂ at 94% or above, check airway, send blood and sputum cultures before antibiotics, and inform the doctor of the shock index.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I am burning and cannot breathe properly." **O:** T 39.0 °C, P 108, RR 26, BP 100/60, SpO₂ 91%, sweating, flushed. | **Hyperthermia** related to infection, as evidenced by temperature 39.0 °C, tachycardia and flushed skin. | **Thermoregulation:** temperature below 37.5 °C within 24 h; no shivering. | 1. Monitor T, P, R, BP hourly while above 39 °C; *detects trend.* 2. Remove extra covers, cool room, tepid sponge 15-20 min; *increases heat loss without shivering.* 3. Give paracetamol as ordered and record; *resets the hypothalamic set point.* 4. Oral fluids 2-3 L or IV as ordered; *replaces sweat loss.* 5. Change damp linen; *comfort and skin.* | T measured 30 min after sponging and every 4 h; target reached or doctor informed. |
| **O:** RR 26, SpO₂ 91%, productive cough. | **Ineffective breathing pattern** related to lung inflammation, as evidenced by RR 26 and SpO₂ 91%. | **Respiratory status:** RR 12-20 and SpO₂ at least 94% in 6 h. | Semi-Fowler's position, oxygen as ordered, teach deep breathing and coughing, suction if needed; *increases lung expansion and clears secretions.* | RR and SpO₂ charted hourly; goal met or oxygen increased and doctor called. |
| **O:** Dry lips, urine output low. | **Deficient fluid volume** related to fever and sweating. | **Hydration:** output at least 0.5 mL/kg/h; moist mucosa in 24 h. | Intake-output chart, mouth care, encourage fluids; *tracks balance and comfort.* | Net balance and mucosa checked each shift. |

:::tip Exam tip
In vitals questions show the arithmetic (MAP, shock index) and say what the number means. A bare number with no interpretation earns half the marks.
:::

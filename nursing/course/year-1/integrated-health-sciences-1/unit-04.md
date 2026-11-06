---
subject: Integrated Health Sciences I
grade: BSc Nursing Year 1
unit: 4
title: The Respiratory System, Gas Transport and Acid-Base
hours: 30
area: BSN 1 · Integrated Health Sciences I · Unit 4
---

Breathing is measured by every nurse on every patient, yet its physiology is where most drug and oxygen decisions begin. This unit covers the airway and lungs, the mechanics of breathing, lung volumes and spirometry, ventilation arithmetic, oxygen transport and the oxyhaemoglobin curve, the effect of Kathmandu's altitude, and the systematic reading of an arterial blood gas.

::: key What this unit gives you
- The respiratory tract beside a real labelled chest X-ray, a spirometer and a peak flow meter.
- Lung volumes and capacities in a spirogram, with minute and alveolar ventilation computed.
- Oxygen content, the oxyhaemoglobin curve and the alveolar gas equation at sea level and in Kathmandu.
- A step-by-step ABG interpretation with Winter's formula and the anion gap.
- Eight points on nursing care of a patient on oxygen therapy, and model answers with a full care plan for COPD exacerbation.
:::

## 4.1 Structure and mechanics of breathing

The **upper airway** (nose, pharynx, larynx) warms, filters and humidifies air; the **lower airway** begins with the trachea (C6 to T4-5, about 11 cm, kept open by C-shaped hyaline cartilage), which divides at the carina into the right and left main bronchi. The **right bronchus is shorter, wider and more vertical**, so inhaled foreign bodies and misplaced tubes go to the right lung. The bronchi branch about 23 times to the terminal bronchioles and then the **alveoli** (about 300 million), where a one-cell-thick wall of type I cells lets gas cross, and type II cells make **surfactant**, which lowers surface tension and stops collapse (absent in premature babies, causing respiratory distress syndrome; antenatal steroids help).

**Mechanics.** By Boyle's law, volume and pressure change in opposite directions. In inspiration the **diaphragm** (phrenic nerve C3-5) flattens and the **external intercostals** lift the ribs, the chest volume rises, the pressure inside falls below atmospheric and air flows in. Quiet expiration is passive elastic recoil. The pleural space holds a thin film of fluid at a negative pressure; air in this space is a **pneumothorax** and the lung collapses. The respiratory centre in the medulla and pons is driven mainly by rising **PaCO₂** (through H⁺ in the CSF); only in chronic CO₂ retention does low oxygen become the main drive.

```photogrid label="4.1" cols="2" ratio="0.95" caption="The chest. (a) A real normal posteroanterior chest X-ray (the patient's right is on the viewer's left). (b) The respiratory tract: airway, lungs and the diaphragm."
@ photo id="nur1/cxr" cap="Normal PA chest radiograph"
fit 0.95
focus 0.5 0.5
mark 0.50 0.85 "1"
mark 0.58 0.38 "2"
mark 0.20 0.17 "3"
key 1 (a) Trachea: a midline dark air column
key 2 (a) Heart shadow: under half of the chest width
key 3 (a) Costophrenic angle: sharp when the pleura is clear
@ svg cap="Respiratory tract"
f = Fig(330, 330)
f.box(120, 6, 90, 22, "Nose / pharynx", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(142, 36, 46, 18, "Larynx", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.line(165, 54, 165, 130, color=SLATE, sw=9)
f.line(165, 130, 110, 175, color=SLATE, sw=7); f.line(165, 130, 220, 175, color=SLATE, sw=7)
f.poly([(60, 110), (150, 120), (140, 260), (50, 262), (30, 180)], fill="#fee2e2", stroke=RED, sw=2)
f.poly([(270, 110), (182, 120), (192, 262), (280, 262), (300, 180)], fill="#fee2e2", stroke=RED, sw=2)
f.line(30, 275, 300, 275, color=NAVY, sw=3); f.text(165, 296, "Diaphragm (dome)", size=10.5, color=NAVY, bold=True)
f.text(180, 92, "Trachea", size=10, color=SLATE, bold=True, anchor="start"); f.text(238, 140, "Carina and\nmain bronchi", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(80, 190, "Right lung\n3 lobes", size=10.5, color=RED, bold=True); f.text(240, 215, "Left lung\n2 lobes", size=10.5, color=RED, bold=True)
f.text(165, 318, "Alveoli at the ends of 23 branchings", size=10, color=SLATE, bold=True)
```

## 4.2 Lung volumes and spirometry

A **spirometer** records air moved. **Tidal volume (TV)** is about 500 mL per quiet breath, **inspiratory reserve volume (IRV)** about 3000 mL, **expiratory reserve volume (ERV)** about 1100 mL and **residual volume (RV)** about 1200 mL, which cannot be exhaled. Capacities are sums: **vital capacity (VC)** = TV + IRV + ERV = **4600 mL**, **total lung capacity (TLC)** = VC + RV = **5800 mL**, **functional residual capacity (FRC)** = ERV + RV = **2300 mL** and **inspiratory capacity** = TV + IRV = **3500 mL**. **FEV₁/FVC** above 70% is normal; below 70% is **obstruction** (asthma, COPD). With FEV₁ 3.2 L and FVC 4.0 L the ratio is **80%**; with FEV₁ 1.2 and FVC 2.4 it is **50%**, an obstructive pattern. In restrictive disease (fibrosis, scoliosis) both fall but the ratio stays normal or high. The **peak flow meter** gives the peak expiratory flow, a cheap bedside tool for asthma at health posts.

```photogrid label="4.2" cols="2" ratio="1.2" caption="Measuring the breath. (a) An older water-sealed spirometer: the bell rises and falls as the patient breathes, and a pen records the volume. (b) A hand-held peak expiratory flow meter with its sliding marker and scale."
@ photo id="nur1/spirometer" cap="Water-sealed spirometer"
fit 1.2
focus 0.5 0.45
mark 0.45 0.60 "1"
key 1 (a) Bell (cylinder) that moves with the volume breathed
@ photo id="nur1/peakflow" cap="Peak flow meter"
fit 1.2
focus 0.5 0.5
mark 0.50 0.62 "1"
mark 0.12 0.25 "2"
key 1 (b) Scale in L/min with a sliding marker
key 2 (b) Mouthpiece: seal lips, blow once as hard and fast as possible
```

```svgfig label="4.1" caption="Spirogram showing the lung volumes and capacities of a healthy adult. Residual volume cannot be measured by simple spirometry."
f = Fig(760, 280)
f.line(70, 20, 70, 250, color=SLATE, sw=1.5); f.line(70, 250, 560, 250, color=SLATE, sw=1.5)
for v, y in [(0, 250), (1200, 222), (2300, 195), (5800, 112)]:
    f.line(66, y, 560, y, color="#e2e8f0", sw=1); f.text(62, y, str(v), size=9.5, color=SLATE, anchor="end")
pts = [(70, 195), (110, 183), (150, 195), (190, 183), (230, 195), (260, 195), (290, 112), (330, 112), (360, 222), (390, 222), (420, 222), (450, 195), (490, 183), (530, 195)]
for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=2.4)
f.box(580, 40, 170, 38, "IRV 3000 mL", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(580, 84, 170, 24, "TV 500 mL", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(580, 114, 170, 34, "ERV 1100 mL", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(580, 154, 170, 34, "RV 1200 mL", fill=ROSE, stroke=RED, size=11, bold=True)
f.text(665, 210, "VC = 4600 mL", size=11.5, color=TEAL, bold=True); f.text(665, 228, "TLC = 5800 mL", size=11.5, color=NAVY, bold=True)
f.text(310, 98, "maximal inspiration", size=10, color=SLATE, bold=True); f.text(405, 240, "maximal expiration", size=10, color=SLATE, bold=True, anchor="start")
f.text(300, 270, "time", size=10.5, color=SLATE)
```

## 4.3 Ventilation arithmetic

**Minute ventilation** = tidal volume × respiratory rate = 500 × 14 = **7000 mL/min**. Part of each breath stays in the conducting airways (the **anatomical dead space**, about 150 mL or 2 mL/kg; here 30% of the tidal volume), so **alveolar ventilation** = (TV − dead space) × RR = (500 − 150) × 14 = **4900 mL/min**. Doubling the rate to 28/min at the same volume gives 14000 mL/min and 9800 mL/min. But **shallow fast breathing** (TV 250, RR 28) has the same minute ventilation of 7,000 mL yet an alveolar ventilation of only (250 − 150) × 28 = **2800 mL/min**, so CO₂ rises: this is why a patient with a high respiratory rate and tiring muscles is in danger even though the "number looks busy". For mechanical ventilation the tidal volume is set by **predicted body weight**: for a man of 170 cm, PBW = 50 + 0.91 × (170 − 152.4) = **66.0 kg**, and 6-8 mL/kg gives **396 to 528 mL**.

## 4.4 Gas exchange and oxygen transport

Gas moves across the alveolar-capillary membrane by diffusion down partial-pressure gradients. Air is 21% oxygen, and the alveolar oxygen pressure follows the **alveolar gas equation**: PAO₂ = FiO₂ × (Patm − 47) − PaCO₂ ÷ 0.8. At sea level (760 mmHg) with PaCO₂ 40: 0.21 × 713 − 50 = **100 mmHg**. Kathmandu (about 1,400 m) has a barometric pressure of about **642 mmHg**, so PAO₂ = 0.21 × (642 − 47) − 50 = **75 mmHg**: a healthy person is a little more hypoxic and their normal SpO₂ may be 94-96%, which matters when a lowlander nurse reads a pulse oximeter in a Himalayan district.

**Oxygen content** = 1.34 × Hb × SaO₂ + 0.003 × PaO₂. For Hb 15, SaO₂ 98% and PaO₂ 95: 1.34 × 15 × 0.98 + 0.003 × 95 = **20.0 mL/dL**. Almost all oxygen rides on haemoglobin, so anaemia lowers oxygen content even when SpO₂ looks normal, while dissolved oxygen is trivial. The **oxyhaemoglobin dissociation curve** is S-shaped: the flat top (above 60 mmHg, saturation 90%) protects against moderate drops in PaO₂, and the steep part releases oxygen to tissues. **Right shift** (acidosis, raised CO₂, fever, 2,3-DPG, exercise) lowers affinity and unloads oxygen; **left shift** (alkalosis, cold, carbon monoxide, fetal Hb) raises affinity.

```svgfig label="4.2" caption="Oxyhaemoglobin dissociation curve. Normal P50 is 26.6 mmHg. A right shift (acidosis, fever) unloads more oxygen to tissue; a left shift holds oxygen tighter. PaO₂ 60 mmHg corresponds to about 90% saturation."
import math
f = Fig(760, 290)
X = lambda p: 80 + p * 5.2
Y = lambda s: 250 - s * 2.1
f.line(80, 30, 80, 250, color=SLATE, sw=1.5); f.line(80, 250, 600, 250, color=SLATE, sw=1.5)
for p in (0, 20, 40, 60, 80, 100): f.text(X(p), 266, str(p), size=10, color=SLATE)
for s in (0, 25, 50, 75, 100): f.line(80, Y(s), 600, Y(s), color="#e2e8f0", sw=1); f.text(72, Y(s), str(s), size=10, color=SLATE, anchor="end")
def curve(p50, col, dash=False):
    pts = [(X(p), Y(100 * p ** 2.7 / (p ** 2.7 + p50 ** 2.7))) for p in range(1, 101)]
    for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=col, sw=2.6, dash=dash)
curve(35, RED, True); curve(26.6, NAVY); curve(20, TEAL, True)
f.line(X(60), Y(90), X(60), 250, color=AMBER, dash=True); f.line(80, Y(90), X(60), Y(90), color=AMBER, dash=True)
f.line(X(40), Y(75), X(40), 250, color=SLATE, dash=True); f.line(80, Y(75), X(40), Y(75), color=SLATE, dash=True)
f.text(330, 282, "PaO₂ (mmHg)", size=11, color=SLATE, bold=True); f.text(20, 140, "SaO₂ %", size=11, color=SLATE, bold=True)
f.text(620, 70, "Left shift:", size=11, color=TEAL, bold=True, anchor="start"); f.text(620, 86, "alkalosis, cold, CO, HbF", size=10, color=TEAL, anchor="start")
f.text(620, 130, "Normal curve", size=11, color=NAVY, bold=True, anchor="start"); f.text(620, 146, "P50 = 26.6 mmHg", size=10, color=NAVY, anchor="start")
f.text(620, 190, "Right shift:", size=11, color=RED, bold=True, anchor="start"); f.text(620, 206, "acidosis, fever, high CO₂", size=10, color=RED, anchor="start")
f.text(X(60) + 6, Y(90) + 22, "60 mmHg, 90%", size=10, color=AMBER, bold=True, anchor="start"); f.text(X(40) + 6, Y(75) + 24, "venous 40 mmHg, 75%", size=10, color=SLATE, bold=True, anchor="start")
```

## 4.5 Reading an arterial blood gas (ABG)

Normal: **pH 7.35-7.45, PaCO₂ 35-45 mmHg, HCO₃⁻ 22-26 mmol/L, PaO₂ 80-100 mmHg, SaO₂ 95-100%**. Follow five steps: (1) look at the pH (acidosis or alkalosis), (2) check which of PaCO₂ and HCO₃⁻ moves the same way (the primary disorder), (3) work out whether the other has compensated, (4) check oxygenation, (5) link to the patient.

| Disorder | pH | PaCO₂ | HCO₃⁻ | Typical causes |
|---|---|---|---|---|
| Respiratory acidosis | low | high | normal (acute) or high (chronic) | COPD, sedative overdose, neuromuscular failure |
| Respiratory alkalosis | high | low | normal or low | hyperventilation, pain, anxiety, altitude |
| Metabolic acidosis | low | low (compensating) | low | DKA, diarrhoea, renal failure, lactic acidosis |
| Metabolic alkalosis | high | high (compensating) | high | persistent vomiting, nasogastric suction, diuretics |

**Worked example.** pH 7.30, PaCO₂ 30, HCO₃⁻ 14. The pH is low and the HCO₃⁻ is low, so this is a metabolic acidosis. **Winter's formula** predicts the PaCO₂: 1.5 × 14 + 8 = **29 mmHg** (±2); the measured 30 is within range, so respiratory compensation is appropriate. The **anion gap** = Na − (Cl + HCO₃) = 140 − (104 + 14) = **22 mmol/L** (normal 8-12), a high-gap acidosis suggesting DKA, lactate or poisoning rather than diarrhoea. A second example: pH 7.26 with PaCO₂ 60 and HCO₃⁻ 26 gives pH = 6.1 + log [26 ÷ (0.03 × 60)] = 6.1 + log 14.4 = **7.26**, an acute respiratory acidosis.

```python
import math
mv = 500 * 14
av = (500 - 150) * 14
pbw = 50 + 0.91 * (170 - 152.4)
cao2 = 1.34 * 15 * 0.98 + 0.003 * 95
patm = 760 * (1 - 2.25577e-5 * 1400) ** 5.25588
pao2 = 0.21 * (patm - 47) - 40 / 0.8
winter = 1.5 * 14 + 8
ag = 140 - (104 + 14)
ph = 6.1 + math.log10(26 / (0.03 * 60))
print("Minute vent", mv)
print("Alveolar vent", av)
print("PBW kg", f"{pbw:.1f}")
print("CaO2", f"{cao2:.1f}")
print("Kathmandu Patm", f"{patm:.0f}")
print("Kathmandu PAO2", f"{pao2:.0f}")
print("Winter PaCO2", f"{winter:.0f}")
print("Anion gap", ag)
print("pH resp acidosis", f"{ph:.2f}")
```

```text
Minute vent 7000
Alveolar vent 4900
PBW kg 66.0
CaO2 20.0
Kathmandu Patm 642
Kathmandu PAO2 75
Winter PaCO2 29
Anion gap 22
pH resp acidosis 7.26
```

## 4.6 Nursing care of a patient on oxygen therapy: eight points

A nasal cannula at 4 L/min gives an FiO₂ of about 21 + 4 × 4 = **37%**; a simple mask gives 40-60% at 5-10 L/min and a non-rebreather mask with a reservoir bag gives up to 90% at 10-15 L/min. A venturi mask gives a fixed FiO₂ and is preferred in COPD. A full E cylinder at 2,000 psi with a 500 psi safe residual and a factor of 0.28 L/psi lasts (2000 − 500) × 0.28 ÷ 4 = **105 minutes** at 4 L/min, which is the sum the nurse does before transferring a patient between wards or to a referral hospital.

1. **Confirm the prescription.** Oxygen is a drug: check the order for device, flow rate and target SpO₂ (94-98%, or 88-92% in COPD). Never start or change a flow without an order except in an emergency. Record the flow on every chart check.
2. **Assess before and after.** Count respiratory rate, depth, effort, colour, SpO₂ and mental state before starting and 15 minutes after any change. Confusion, restlessness and a rising rate warn of hypoxia early. Cyanosis is a late sign.
3. **Position the patient.** Sit the patient upright in a Fowler's or orthopnoeic position to let the diaphragm drop. This eases breathing and improves oxygen delivery. Support the arms on a pillow or overbed table.
4. **Prepare the equipment safely.** Check the cylinder gauge or wall flowmeter, the humidifier water level (sterile water, changed daily) and the tubing for kinks. Fix the cylinder upright on a trolley. A leak or a wrong connection wastes oxygen and harms the patient.
5. **Fire safety.** Oxygen supports burning. Put up a "No smoking, oxygen in use" sign, keep matches, kerosene lamps, naked flame, oil and grease at least 2 metres away, and use cotton rather than nylon. Tell relatives, because smoking and incense are common near beds.
6. **Protect skin and mucosa.** Cannulas and masks press behind the ears, over the cheeks and in the nostrils. Pad these areas, clean the nares and give mouth care every 4 hours. Dry oxygen dries the nose, so humidify above 4 L/min.
7. **Avoid oxygen toxicity and CO₂ narcosis.** In chronic CO₂ retainers a high flow removes the hypoxic drive and the patient becomes drowsy with a rising PaCO₂. Use a venturi mask or 1-2 L/min and call the doctor for drowsiness or headache. Long high-FiO₂ therapy can injure the lung, so reduce as soon as safe.
8. **Teach and document.** Tell the patient and family not to change the flow, not to remove the device to eat without asking, and to call for breathlessness. Record device, flow, SpO₂, respiratory rate and response, and report if the target is not met. Plan weaning and cylinder replacement before the gauge falls below 500 psi.

## Formula and fact sheet

- VC = TV + IRV + ERV = 4600 mL; TLC = VC + RV = 5800 mL; FRC = ERV + RV = 2300 mL. FEV₁/FVC below 70% = obstruction.
- Minute ventilation = TV × RR (7000 mL/min); alveolar ventilation = (TV − 150) × RR (4900 mL/min).
- PAO₂ = FiO₂ (Patm − 47) − PaCO₂ ÷ 0.8: 100 mmHg at sea level, 75 mmHg in Kathmandu. CaO₂ = 1.34 × Hb × SaO₂ + 0.003 × PaO₂ = 20.0 mL/dL.
- pH = 6.1 + log [HCO₃⁻ ÷ (0.03 × PaCO₂)]. Winter: PaCO₂ = 1.5 × HCO₃⁻ + 8 (29). Anion gap = Na − (Cl + HCO₃⁻) (22).
- Cannula FiO₂ about 21 + 4 × flow (L/min). Cylinder time = (psi − 500) × 0.28 ÷ flow (105 min).

## Chapter summary

- The right bronchus is wider and more vertical; surfactant keeps alveoli open.
- Breathing follows Boyle's law: the diaphragm and intercostals expand the chest and air flows in.
- Alveolar ventilation, not minute ventilation, clears CO₂; shallow fast breathing is dangerous.
- Oxygen travels on haemoglobin; the S-shaped curve shifts right in acid, hot, high-CO₂ tissue.
- Read an ABG in five steps and name the primary disorder and the compensation.
- Oxygen is a drug with a target, a fire risk and, in COPD, a CO₂-narcosis risk.

## Practice

**MCQs (with reasons)**

1. The bronchus into which a foreign body most often enters is: (a) the left (b) the right (c) either equally (d) the carina.
2. Tidal volume 500 mL, dead space 150 mL and rate 14/min give an alveolar ventilation of: (a) 2,100 (b) 4,900 (c) 7,000 (d) 9,800 mL/min.
3. pH 7.30, PaCO₂ 30 and HCO₃⁻ 14 mmol/L represent: (a) respiratory acidosis (b) respiratory alkalosis (c) metabolic acidosis (d) metabolic alkalosis.
4. A right shift of the oxyhaemoglobin curve is caused by: (a) alkalosis (b) fever and acidosis (c) hypothermia (d) carbon monoxide.
5. FEV₁/FVC of 50% suggests: (a) a normal lung (b) an obstructive pattern (c) a restrictive pattern (d) a faulty test only.

::: note Answers and rationales
**1. (b).** The right main bronchus is shorter, wider and more vertical, so aspirated material and misplaced tubes enter it.
**2. (b).** (500 − 150) × 14 = 4900 mL/min. 7000 mL/min is the minute ventilation, which ignores dead space.
**3. (c).** Both pH and HCO₃⁻ are low (metabolic acidosis); the low PaCO₂ is the compensation (Winter's value 29).
**4. (b).** Acid, heat and high CO₂ lower haemoglobin affinity so oxygen is unloaded in active tissues; the other options cause a left shift.
**5. (b).** A ratio below 70% means airflow obstruction, as in COPD or asthma; restrictive disease keeps the ratio normal.
:::

**Short answer (3 marks): Alveolar ventilation and dead space.** Alveolar ventilation is the volume of fresh air reaching the alveoli per minute: (tidal volume − dead space) × rate. With 500 mL, 150 mL and 14/min it is 4900 mL/min. Dead space (about 2 mL/kg) is the air that fills the airway but takes no part in gas exchange. Shallow rapid breathing keeps the minute ventilation (7000 mL) but cuts alveolar ventilation to 2800 mL/min, so PaCO₂ rises.

**Medium answer (5 marks): Describe the transport of oxygen in blood and the oxyhaemoglobin curve (Figure 4.2).** About 98.5% of oxygen is carried bound to haemoglobin (each gram holds 1.34 mL) and only 1.5% is dissolved. Oxygen content is 1.34 × Hb × SaO₂ + 0.003 × PaO₂, about 20.0 mL/dL at Hb 15. The curve is S-shaped because binding of the first oxygen makes the next ones easier (cooperativity). The flat upper part, where PaO₂ above 60 mmHg gives saturation of 90% or more, is a safety margin for the lungs; the steep lower part releases oxygen to tissues. P50, the PaO₂ at 50% saturation, is 26.6 mmHg. A right shift (acidosis, raised temperature, CO₂ and 2,3-DPG) releases more oxygen; a left shift (alkalosis, cold, carbon monoxide, fetal Hb) holds it. Clinical points: anaemia lowers content though SpO₂ is normal, and carbon monoxide gives a falsely normal SpO₂.

**Long answer (10 marks): Mr Dhan Bahadur Rai, 66, a former smoker who cooked for 40 years on a wood fire, is admitted from a hill district with 3 days of worsening breathlessness and green sputum. RR 28/min, pulse 110/min, SpO₂ 84% on room air, drowsy, using accessory muscles, wheeze on chest auscultation. Spirometry: FEV₁ 1.2 L, FVC 2.4 L. ABG: pH 7.26, PaCO₂ 60, HCO₃⁻ 26, PaO₂ 52. Discuss the physiology and the nursing care with a care plan.**

*Introduction.* The FEV₁/FVC is 1.2 ÷ 2.4 = **50%**, below 70%, confirming chronic obstructive pulmonary disease (COPD), a leading cause of death in Nepal from tobacco and indoor biomass smoke. The ABG gives pH = 6.1 + log [26 ÷ (0.03 × 60)] = 6.1 + log 14.4 = **7.26**: an acute-on-chronic respiratory acidosis with hypoxaemia. Airway narrowing, mucus and alveolar damage cut alveolar ventilation, CO₂ is retained, and the hypoxic drive may control breathing. The priority is **controlled oxygen** (venturi mask 24-28% or cannula at 1-2 L/min, SpO₂ target 88-92%) with repeat ABG in 30-60 minutes, nebulised salbutamol and ipratropium, oral prednisolone, antibiotics for purulent sputum, and non-invasive ventilation if pH stays below 7.30. If the drowsiness deepens, the doctor is called, since too much oxygen would worsen CO₂ narcosis.

| Assessment | Nursing diagnosis (NANDA-I) | Goal / outcome (NOC) | Interventions (NIC) with rationale | Evaluation |
|---|---|---|---|---|
| **S:** "I cannot catch my breath." **O:** RR 28, SpO₂ 84%, PaO₂ 52, PaCO₂ 60, drowsy. | **Impaired gas exchange** related to alveolar-capillary changes and ventilation-perfusion imbalance, as evidenced by hypoxaemia and hypercapnia. | **Respiratory status: gas exchange:** SpO₂ 88-92%, RR below 24 and alert in 6 h. | 1. Controlled oxygen by venturi mask; *relieves hypoxia without removing the drive to breathe.* 2. Upright position; *lets the diaphragm descend.* 3. Continuous SpO₂ and repeat ABG as ordered; *detects CO₂ narcosis early.* 4. Give bronchodilator nebuliser on time; *opens airways.* | SpO₂, RR and consciousness checked hourly; ABG pH above 7.30 at 6 h. |
| **S:** "Phlegm is stuck." **O:** green sputum, wheeze, weak cough. | **Ineffective airway clearance** related to retained secretions and bronchospasm, as evidenced by wheeze and abnormal sputum. | **Airway patency:** clear breath sounds and productive cough within 24 h. | 1. Oral fluids 2-2.5 L unless restricted and humidify; *thins mucus.* 2. Teach huff coughing and chest physiotherapy; *moves secretions without exhaustion.* 3. Send sputum culture before antibiotics; *targets treatment.* | Sputum amount and colour recorded each shift; breath sounds improve. |
| **S:** "I smoked for 40 years." **O:** uses inhaler incorrectly; fire used indoors. | **Deficient knowledge** about COPD management and risk factors. | **Knowledge: disease process:** states 3 triggers and shows inhaler technique before discharge. | 1. Demonstrate inhaler with spacer and check return demonstration; *ensures drug reaches lungs.* 2. Counsel to stop tobacco and use a chimney or improved cookstove; *slows lung decline.* 3. Teach pursed-lip breathing and vaccination (influenza, pneumococcal); *reduces air trapping and infection.* | Teach-back at discharge; follow-up plan with PEN clinic. |

::: tip Exam tip
In every ABG question write the pH step, the primary disorder, the compensation (Winter's formula for metabolic acidosis) and then the oxygenation. Add the one nursing fact the examiner expects: controlled oxygen in COPD.
:::

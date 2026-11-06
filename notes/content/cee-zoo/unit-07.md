---
subject: Zoology
grade: CEE
unit: 7
title: Circulatory System
hours: 3
area: Human Biology and Physiology
---

The circulatory system carries **3 of the 40 Zoology questions** — the largest
share of the human physiology units. The paper draws on four blocks: the **heart**
(chambers, valves, conducting system, cardiac cycle and output), the **vessels and
blood pressure**, the **blood** (cells, clotting, ABO and Rh groups), and the
**disorders** (atherosclerosis, heart attack, angina, varicose veins, anaemia).
Almost every question is a name, a number or a direction of flow. The three traps
that decide marks are: the **left ventricle has the thickest wall**, the
**pulmonary artery carries deoxygenated blood**, and **O negative is the universal
donor for red cells**.

::: key What the paper asks from this chapter
- **Anatomy**: four chambers, the **tricuspid** and **bicuspid (mitral)** valves, the two semilunar valves, and the great vessels; the **left ventricle** wall is the thickest because it drives the systemic circuit.
- **Double circulation**: right heart → lungs → left heart (**pulmonary**); left heart → body → right heart (**systemic**); the **coronary** arteries come from the ascending aorta.
- **Conducting system**: **SA node → AV node → bundle of His → right and left branches → Purkinje fibres**; the SA node is the pacemaker because it depolarises fastest.
- **Cardiac cycle** (0.8 s at 72/min): atrial systole 0.1 s, ventricular systole 0.3 s, diastole 0.5 s; **S1** = AV valves closing, **S2** = semilunar valves closing.
- **Cardiac output = stroke volume × heart rate** ≈ 70 mL × 72 ≈ **5 L min⁻¹**; ejection fraction ≈ 60 %.
- **ECG**: **P** = atrial depolarisation, **QRS** = ventricular depolarisation, **T** = ventricular repolarisation.
- **Vessels**: arteries thick-walled, no valves, high pressure; veins thin-walled, **valves**, low pressure; the **hepatic portal vein** runs gut → liver.
- **Blood pressure 120/80**; hypertension ≥ 140/90; **baroreceptors** in the carotid sinus and aortic arch.
- **Blood**: plasma 55 %, cells 45 %; RBC 5 million/mm³, 120 days; WBC 4000–11 000/mm³; platelets 1.5–4 lakh/mm³; **ABO and Rh** groups; **O−** donor, **AB+** recipient; **erythroblastosis fetalis**.
:::

## 7.1 The heart, the heartbeat, the cardiac cycle and cardiac output

### Position and coverings

The heart is a hollow muscular organ of about **250–300 g**, roughly the size of
the owner's fist, lying in the **mediastinum** between the lungs, behind the
sternum. Two-thirds of it lies to the left of the midline, and its apex points
down and to the left, reaching the **fifth intercostal space** about 9 cm from the
midline.

```photo id="bio12/heart-numbered" caption="Longitudinal (frontal) section of the human heart. Blue = deoxygenated blood, red = oxygenated; arrows show the direction of flow. Note the left ventricular wall, about three times thicker than the right." width="74"
key 1 Right atrium
key 2 Left atrium
key 3 Superior vena cava
key 4 Aorta
key 5 Pulmonary artery
key 6 Pulmonary veins
key 7 Bicuspid (mitral) valve
key 8 Aortic (semilunar) valve
key 9 Left ventricle
key 10 Right ventricle
key 11 Inferior vena cava
key 12 Tricuspid valve
key 13 Pulmonary (semilunar) valve
```


It is enclosed in the **pericardium**: a tough outer **fibrous** layer and a
**serous** layer of two sheets — the **parietal** lining the sac and the
**visceral** stuck to the heart (the epicardium). Between them is a film of
**pericardial fluid** that lets the heart move without friction.

The wall has three layers:

| Layer | Structure | Note |
|---|---|---|
| **Epicardium** | visceral serous pericardium + fat | carries the coronary vessels |
| **Myocardium** | cardiac muscle | **thickest in the left ventricle** |
| **Endocardium** | endothelium + connective tissue | lines the chambers and valves |

### The chambers and valves

| Chamber | Receives | Sends blood to | Wall |
|---|---|---|---|
| **Right atrium** | superior and inferior vena cava, coronary sinus | right ventricle | thin |
| **Right ventricle** | right atrium | **pulmonary artery** | moderate |
| **Left atrium** | four **pulmonary veins** | left ventricle | thin |
| **Left ventricle** | left atrium | **aorta** | **thickest** |

The two atria are separated by the **interatrial septum**, which bears the
**fossa ovalis** — the remnant of the fetal opening. The ventricles are separated
by the thick **interventricular septum**.

There are **four valves**, all of which open and close **passively** with the
pressure difference across them:

| Valve | Position | Opens when | Prevents |
|---|---|---|---|
| **Tricuspid** (right AV) | between right atrium and ventricle | atrial pressure > ventricular | backflow into the right atrium |
| **Bicuspid / mitral** (left AV) | between left atrium and ventricle | atrial pressure > ventricular | backflow into the left atrium |
| **Pulmonary semilunar** | at the exit of the right ventricle | ventricular pressure > pulmonary artery | backflow into the right ventricle |
| **Aortic semilunar** | at the exit of the left ventricle | ventricular pressure > aorta | backflow into the left ventricle |

The AV valves are held by **chordae tendineae** attached to **papillary muscles**,
which stop them turning inside out during ventricular contraction.

```figure caption="The double circulation, drawn as a flow chart. Blood from the body enters the right atrium, passes the tricuspid valve into the right ventricle, and is sent through the pulmonary valve to the lungs. Oxygenated blood returns to the left atrium, passes the mitral valve into the left ventricle, and leaves through the aortic valve into the aorta. Every valve lies between two chambers or between a chamber and a vessel, and each opens only downstream."
import numpy as np
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 4.3))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
BLUE, BLUEF = "#1d6fb8", "#e3eefa"
RED, REDF = "#c0392b", "#fbe6e3"

def box(x, y, w, h, text, ec, fc, fs=6.9):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.14",
                                fc=fc, ec=ec, lw=1.3, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=4)

def path_arrow(pts, c):
    xs = [q[0] for q in pts]
    ys = [q[1] for q in pts]
    ax.plot(xs, ys, color=c, lw=1.8, solid_joinstyle="miter",
            solid_capstyle="butt", zorder=2)
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8, shrinkA=0,
                                shrinkB=2), zorder=2)

box(2.30, 6.45, 2.30, 0.92, "RIGHT\nATRIUM", BLUE, BLUEF)
box(2.30, 4.20, 2.30, 0.92, "RIGHT\nVENTRICLE", BLUE, BLUEF)
box(7.70, 6.45, 2.30, 0.92, "LEFT\nATRIUM", RED, REDF)
box(7.70, 4.20, 2.30, 0.92, "LEFT\nVENTRICLE", RED, REDF)
box(5.00, 9.25, 2.30, 0.78, "LUNGS", MUTED, "#f2f4f7")
box(5.00, 0.75, 2.30, 0.78, "BODY TISSUES", MUTED, "#f2f4f7")

path_arrow([(3.85, 0.75), (0.95, 0.75), (0.95, 6.45), (1.12, 6.45)], BLUE)
path_arrow([(2.30, 5.99), (2.30, 4.69)], BLUE)
path_arrow([(3.45, 4.20), (3.95, 4.20), (3.95, 8.82)], BLUE)
path_arrow([(6.15, 9.25), (7.70, 9.25), (7.70, 6.94)], RED)
path_arrow([(7.70, 5.99), (7.70, 4.69)], RED)
path_arrow([(7.70, 3.74), (7.70, 0.75), (6.18, 0.75)], RED)

ax.text(2.30, 5.34, "tricuspid", ha="center", fontsize=6.7, color=BLUE,
        bbox=dict(fc="white", ec="none", pad=1.2), zorder=6)
ax.text(7.70, 5.34, "bicuspid (mitral)", ha="center", fontsize=6.7, color=RED,
        bbox=dict(fc="white", ec="none", pad=1.2), zorder=6)
ax.text(4.48, 5.05, "pulmonary valve", ha="left", fontsize=6.7, color=BLUE,
        zorder=6)
ax.plot([4.02, 4.42], [5.05, 5.05], color=MUTED, lw=0.7, zorder=5)
ax.text(7.70, 3.45, "aortic valve", ha="center", fontsize=6.7, color=RED,
        bbox=dict(fc="white", ec="none", pad=1.2), zorder=6)
ax.text(0.58, 3.60, "vena cava", fontsize=6.7, color=BLUE, rotation=90,
        va="center")
ax.text(4.22, 6.35, "pulmonary artery", fontsize=6.7, color=BLUE, rotation=90,
        va="center", ha="center")
ax.text(8.05, 8.10, "pulmonary veins", fontsize=6.7, color=RED, rotation=90,
        va="center")
ax.text(8.10, 2.20, "aorta", fontsize=6.7, color=RED, rotation=90, va="center")
ax.text(5.45, 2.55, "SYSTEMIC", ha="center", fontsize=7.0, color=MUTED)
ax.text(5.45, 2.15, "circulation", ha="center", fontsize=7.0, color=MUTED)
ax.text(5.45, 7.60, "PULMONARY", ha="center", fontsize=7.0, color=MUTED)
ax.text(5.45, 7.20, "circulation", ha="center", fontsize=7.0, color=MUTED)
```

::: caution Why the left ventricle is thickest
It pumps blood round the **whole body**, so it must generate about **120 mmHg**;
the right ventricle only pumps to the lungs, at about **25 mmHg**. A question that
offers "the right ventricle, because it is larger" is testing this.
:::

### The double circulation and the coronary circulation

Blood passes through the heart **twice** in one complete circuit:

- **Pulmonary circulation**: right ventricle → pulmonary trunk → pulmonary
  arteries → lungs → pulmonary veins → left atrium. Short, low pressure.
- **Systemic circulation**: left ventricle → aorta → all the tissues → superior
  and inferior vena cava → right atrium. Long, high pressure.

This is why the heart is described as a **double pump** and why the two sides
never mix in a healthy adult.

The heart muscle itself is fed by the **coronary circulation**. The **right and
left coronary arteries** arise from the **ascending aorta** just above the aortic
valve, and their branches run in the epicardium. Blood returns by the cardiac
veins into the **coronary sinus**, which opens into the right atrium. The coronary
arteries fill mainly **during diastole**, when the ventricle is relaxed — one
reason a very fast heart rate is dangerous.

### The conducting system

Cardiac muscle contracts **without any nerve**: it is **myogenic**. A special
patch of muscle, the **sinoatrial (SA) node**, in the wall of the right atrium
near the opening of the superior vena cava, depolarises spontaneously about
**70–80 times a minute** and sets the rhythm. The wave then travels:

**SA node → atria → AV node → bundle of His → right and left bundle branches →
Purkinje fibres → ventricular muscle.**

| Part | Rate if it acts alone (per min) | Conduction velocity |
|---|---|---|
| **SA node** | **70–80** (the pacemaker) | slow |
| **AV node** | 40–60 | **0.05 m s⁻¹** — the slowest, giving a **0.1 s delay** |
| Bundle of His and branches | 30–40 | 1–2 m s⁻¹ |
| **Purkinje fibres** | 20–40 | **4 m s⁻¹** — the fastest |

The **SA node sets the rhythm** because its membrane leaks ions so that it
reaches threshold **first**; it therefore drives the other, slower pacemakers
before they can fire on their own. They are **latent pacemakers**, ready to take
over if the SA node fails.

The **AV nodal delay** matters: it lets the atria finish emptying before the
ventricles contract, so the ventricles are properly filled.

```figure caption="The conducting system of the heart. The SA node fires first and sets the rhythm; the impulse spreads through the atria, is delayed at the AV node, and then races down the bundle of His and the Purkinje fibres so that both ventricles contract together from the apex upwards."
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 4.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
# heart outline
ax.add_patch(Polygon([[2.10, 8.60], [4.30, 9.00], [6.30, 8.55], [7.30, 7.10],
                      [7.20, 4.60], [6.20, 2.20], [5.00, 1.10], [3.80, 2.20],
                      [2.80, 4.60], [2.70, 7.10]], closed=True,
                     fc="#fbe9ea", ec="#a9555e", lw=1.4, zorder=2))
ax.plot([4.95, 4.95], [8.80, 2.00], color="#a9555e", lw=1.4, zorder=3)
ax.plot([2.70, 7.20], [6.60, 6.60], color="#a9555e", lw=1.4, zorder=3)
# SA node
ax.add_patch(Circle((3.75, 8.15), 0.24, fc="#1d6fb8", ec="none", zorder=6))
# AV node
ax.add_patch(Circle((4.95, 6.95), 0.22, fc="#b8860b", ec="none", zorder=6))
# bundle of His and branches
ax.plot([4.95, 4.95], [6.75, 4.10], color="#2e8b57", lw=3.2, zorder=6)
ax.plot([4.95, 4.20, 4.05], [4.10, 3.30, 2.30], color="#2e8b57", lw=2.6, zorder=6)
ax.plot([4.95, 5.75, 5.90], [4.10, 3.30, 2.30], color="#2e8b57", lw=2.6, zorder=6)
for x0, y0, s in [(4.05, 2.30, -1), (5.90, 2.30, 1)]:
    for k in range(3):
        ax.plot([x0, x0 + s * 0.55], [y0, y0 - 0.45 + 0.15 * k],
                color="#2e8b57", lw=1.4, zorder=6)
# labels
ax.text(1.25, 8.65, "SA node\n(pacemaker)", fontsize=7.0, color="#1d6fb8")
ax.annotate("", xy=(3.66, 8.16), xytext=(3.05, 8.55),
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=5)
ax.text(3.42, 6.22, "AV node", fontsize=7.0, color="#b8860b", ha="right")
ax.annotate("", xy=(4.84, 6.90), xytext=(3.50, 6.26),
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7), zorder=5)
ax.text(5.15, 5.20, "bundle of His", fontsize=7.0, color="#2e8b57", ha="left")
ax.text(2.05, 2.60, "Purkinje\nfibres", fontsize=7.0, color="#2e8b57", ha="right")
ax.annotate("", xy=(4.88, 7.10), xytext=(3.88, 7.98),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9,
                            connectionstyle="arc3,rad=0.30"), zorder=5)
ax.text(1.15, 9.45, "right atrium", fontsize=7.0, color=MUTED)
ax.text(1.15, 4.90, "right ventricle", fontsize=7.0, color=MUTED)
ax.text(7.55, 9.45, "left atrium", fontsize=7.0, color=MUTED, ha="left")
ax.text(7.55, 4.90, "left ventricle", fontsize=7.0, color=MUTED, ha="left")
```

### The cardiac cycle

One complete beat — contraction (**systole**) and relaxation (**diastole**) of
the four chambers — is the **cardiac cycle**. At a rate of **72–75 beats a
minute** it lasts **0.8 s**:

| Phase | Duration | What happens |
|---|---|---|
| **Atrial systole** | 0.1 s | the atria contract and top up the ventricles (about 20 % of filling) |
| **Ventricular systole** | 0.3 s | AV valves close (S1); pressure rises; semilunar valves open; blood is ejected |
| **Ventricular diastole** | 0.5 s | semilunar valves close (S2); ventricles relax and fill; AV valves open |

The pressure changes drive everything:

| Event | Pressure relation | Result |
|---|---|---|
| AV valves close | ventricular > atrial | **first heart sound** |
| Semilunar valves open | ventricular > aorta / pulmonary artery | ejection begins |
| Semilunar valves close | aorta > ventricular | **second heart sound** |
| AV valves open | atrial > ventricular | rapid filling |

Typical pressures: left ventricle **120/0–10 mmHg**, aorta **120/80**, left atrium
about **8 mmHg**, right atrium about **2 mmHg**.

**Heart sounds.** **S1 ("lub")** is the closure of the **AV valves** at the start
of ventricular systole — longer and lower. **S2 ("dub")** is the closure of the
**semilunar valves** at the end of systole — shorter and sharper. S3 and S4 are
soft filling sounds, often inaudible in health.

```figure caption="The cardiac cycle. The upper panel shows the pressures in the left ventricle and the aorta; the middle panel is the ECG; the lower panel marks the heart sounds. Note that the AV valves close at the start of ventricular systole (S1) and the semilunar valves at its end (S2), and that the whole cycle takes 0.8 s at 75 beats a minute."
import numpy as np
fig, axes = plt.subplots(3, 1, figsize=(5.1, 4.4), sharex=True,
                         gridspec_kw=dict(height_ratios=[2.0, 1.0, 0.55]))
ax = axes[0]
t = np.linspace(0, 0.8, 900)
tc = np.array([0.00, 0.10, 0.13, 0.16, 0.20, 0.25, 0.32, 0.40, 0.45,
               0.47, 0.50, 0.55, 0.70, 0.80])
lv = np.array([5, 5, 40, 85, 105, 120, 112, 95, 82, 40, 12, 6, 5, 8], float)
ao = np.array([80, 80, 82, 90, 106, 120, 114, 104, 100, 96, 94, 90, 84, 81],
              float)

def smooth(y, k=21):
    w = np.ones(k) / k
    return np.convolve(np.r_[y[:k][::-1], y, y[-k:][::-1]], w, "same")[k:-k]

lv_s = smooth(np.interp(t, tc, lv))
ao_s = smooth(np.interp(t, tc, ao))
ax.plot(t, lv_s, color=SERIES[0], lw=1.6, label="left ventricle")
ax.plot(t, ao_s, color=SERIES[1], lw=1.6, label="aorta")
ax.set_ylabel("pressure\n(mmHg)", fontsize=7.0)
ax.set_ylim(0, 135); ax.set_yticks([0, 40, 80, 120])
ax.legend(fontsize=6.4, frameon=False, loc="upper right", ncol=1)
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(labelsize=6.8)
for x in (0.10, 0.47):
    ax.axvline(x, color=MUTED, lw=0.7, ls=":")

ax = axes[1]
ecg = np.zeros_like(t)
ecg += 0.18 * np.exp(-((t - 0.03) / 0.012) ** 2)
ecg -= 0.22 * np.exp(-((t - 0.145) / 0.008) ** 2)
ecg += 1.00 * np.exp(-((t - 0.165) / 0.010) ** 2)
ecg -= 0.30 * np.exp(-((t - 0.185) / 0.010) ** 2)
ecg += 0.32 * np.exp(-((t - 0.36) / 0.035) ** 2)
ax.plot(t, ecg, color=INK, lw=1.3)
ax.set_ylabel("ECG", fontsize=7.0); ax.set_yticks([])
ax.text(0.035, 0.42, "P", fontsize=7.4, color=INK)
ax.text(0.175, 0.86, "QRS", fontsize=7.4, color=INK)
ax.text(0.375, 0.44, "T", fontsize=7.4, color=INK)
ax.set_ylim(-0.6, 1.25)
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(labelsize=6.8)

ax = axes[2]
ax.set_ylim(0, 1); ax.set_yticks([]); ax.set_xlim(0, 0.8)
ax.axvspan(0.10, 0.19, color=SERIES[0], alpha=0.35, lw=0)
ax.axvspan(0.46, 0.53, color=SERIES[1], alpha=0.35, lw=0)
ax.text(0.145, 0.52, "S1", ha="center", fontsize=7.4, color=SERIES[0])
ax.text(0.495, 0.52, "S2", ha="center", fontsize=7.4, color=SERIES[1])
ax.set_ylabel("sounds", fontsize=7.0)
ax.set_xlabel("time (s)", fontsize=7.2)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
ax.tick_params(labelsize=6.8)
```

### Cardiac output

**Stroke volume (SV)** is the blood ejected by one ventricle in one beat — about
**70 mL**. **Heart rate (HR)** is the number of beats per minute — about **72**.
**Cardiac output (CO)** is the volume pumped by one ventricle in a minute:

$$CO = SV \times HR$$

$$CO = 70\ \text{mL} \times 72\ \text{min}^{-1} = 5040\ \text{mL min}^{-1} \approx 5\ \text{L min}^{-1}$$

The **ejection fraction** is the fraction of the end-diastolic volume that is
ejected:

$$EF = \frac{SV}{EDV} = \frac{70}{120} \approx 0.58\ (58\ \%)$$

Cardiac output rises in exercise to 20–25 L min⁻¹, by increasing both rate and
stroke volume. It depends on:

| Factor | Effect |
|---|---|
| **Preload** (venous return) | more filling → more stretch → stronger contraction (**Frank–Starling law**) |
| **Afterload** (arterial pressure) | higher pressure → harder to eject → lower stroke volume |
| **Contractility** | adrenaline and sympathetic nerves increase it |
| **Heart rate** | up to a point raises output; too fast shortens filling and lowers it |

### The electrocardiogram

The **ECG** records the electrical activity of the heart from the body surface.
Its three waves:

| Wave | Meaning | Duration |
|---|---|---|
| **P** | **atrial depolarisation** (just before atrial systole) | 0.08–0.10 s |
| **QRS** | **ventricular depolarisation** (atrial repolarisation is hidden inside it) | 0.08–0.12 s |
| **T** | **ventricular repolarisation** | — |

The **PR interval** (0.12–0.20 s) shows the AV nodal delay; a long PR means heart
block. ST elevation is the classic sign of a **myocardial infarction**.

::: example Cardiac output at rest and in exercise
**Problem.** At rest a student has a stroke volume of 70 mL and a heart rate of
72 min⁻¹. In exercise his stroke volume rises to 120 mL and his rate to 150 min⁻¹.
Find both cardiac outputs.

**Solution.** Rest: $70 \times 72 = 5040$ mL min⁻¹ ≈ **5.0 L min⁻¹**.
Exercise: $120 \times 150 = 18\,000$ mL min⁻¹ = **18 L min⁻¹**.

So the output can rise more than threefold, and most of the rise comes from the
stroke volume at first, then from the rate.
:::

::: example Ejection fraction
**Problem.** A patient's end-diastolic volume is 120 mL and end-systolic volume
50 mL. Find the stroke volume and the ejection fraction.

**Solution.** $SV = 120 - 50 = 70$ mL. $EF = 70/120 = 0.58$ = **58 %**.

A failing heart may have an ejection fraction below 40 %, which is why it tires on
exertion.
:::

```photogrid label="7.1" cols="2" ratio="1.2" caption="Cardiac output and blood pressure. (a) Measuring blood pressure with a sphygmomanometer and a stethoscope over the brachial artery. (b) Cardiac output = heart rate x stroke volume: at rest 72 beats/min x 70 mL = 5.04 L/min, which is the whole 5 L blood volume once a minute; in hard exercise 180 x 120 mL = 21.6 L/min, 4.3 times higher. A reading of 120/80 mm Hg gives a mean arterial pressure MAP = diastolic + (systolic - diastolic)/3 = 93 mm Hg, because the heart spends about two thirds of each cycle in diastole."
@ photo id="ceezoo/bp" cap="Measuring blood pressure"
fit 1.2
focus 0.5 0.4
@ svg cap="Cardiac output at rest and in exercise (L/min)"
co1, co2 = 72 * 70 / 1000, 180 * 120 / 1000
mp = 80 + (120 - 80) / 3
assert abs(co1 - 5.04) < 1e-9 and abs(co2 - 21.6) < 1e-9 and abs(mp - 93.33) < 0.01
facts = dict(co1="%.2f" % co1, co2="%.1f" % co2, r="%.1f" % (co2 / co1), map="%.0f" % mp)
f = Fig(300, 236)
f.text(150, 12, "CO = heart rate x stroke volume", size=10.5, color=NAVY, bold=True)
for i, (lab, hr, sv, v, c, fl) in enumerate((("rest: 72 x 70 mL", 72, 70, co1, TEAL, MINT), ("exercise: 180 x 120 mL", 180, 120, co2, RED, ROSE))):
    y = 34 + i * 54
    f.text(10, y, lab, size=10.5, color=c, bold=True, anchor="start")
    w = v / 21.6 * 200
    f.box(10, y + 8, w, 24, fill=fl, stroke=c, r=2)
    f.text(10 + w + 6, y + 20, "%.2f L/min" % v if i == 0 else "%.1f L/min" % v, size=10.5, color=c, bold=True, anchor="start", vmid=True)
f.text(150, 164, "MAP = 80 + (120 - 80)/3 = 93 mm Hg", size=10.5, color=NAVY, bold=True)
f.text(150, 184, "exercise output is 4.3 times resting", size=10.5, color=SLATE, bold=True)
```

## 7.2 Arterial and venous systems; blood pressure

### Artery, vein and capillary

| Feature | **Artery** | **Vein** | **Capillary** |
|---|---|---|---|
| Wall | **thick**, three coats, much elastic and smooth muscle | **thin**, little muscle | **one cell thick** (endothelium + basement membrane) |
| Lumen | narrow, stays round | wide, collapses when empty | extremely narrow (7–10 μm) |
| Valves | **none** (except at the heart) | **yes**, especially in the limbs | none |
| Blood flow | fast, **pulsatile** | slow, steady | **slowest** — the widest total cross-section |
| Pressure | **high** (120/80 in the aorta) | **low** (near 0 in the vena cava) | falls from arteriole to venule |
| Carries | blood **away** from the heart | blood **towards** the heart | exchange between blood and tissue |
| Example | aorta, carotid, renal artery | vena cava, jugular, saphenous | in every tissue |

Arteries near the heart are **elastic** (the aorta expands with each systole and
recoils in diastole, smoothing the flow into a pulse); arteries further out are
**muscular** and control the distribution of blood. **Arterioles** are the main
resistance vessels and set blood pressure.

### The main vessels

| Region | Artery | Vein |
|---|---|---|
| Head and neck | common carotid → internal and external carotid | internal and external jugular |
| Upper limb | subclavian → axillary → brachial → radial and ulnar | cephalic, basilic, brachial |
| Thorax | descending thoracic aorta | azygos, hemiazygos |
| Abdomen | coeliac trunk, superior and inferior mesenteric, renal, gonadal | hepatic, renal, mesenteric |
| Lower limb | common iliac → external iliac → femoral → popliteal | great saphenous, femoral, popliteal |
| Whole body | **aorta** (largest artery) | **vena cava** (largest vein) |

The **aorta** has three parts: **ascending**, the **arch** (giving the
brachiocephalic, left common carotid and left subclavian), and the **descending**
thoracic and abdominal aorta, which ends by dividing into the two common iliac
arteries. The **superior vena cava** drains the head, neck and arms; the
**inferior vena cava** drains everything below the diaphragm.

### The hepatic portal system

A **portal system** is a set of veins that breaks into a second capillary bed
before reaching the heart. The **hepatic portal vein** is formed behind the neck
of the pancreas by the union of the **superior mesenteric vein** and the **splenic
vein** (joined by the **inferior mesenteric** and gastric veins). It carries
absorbed glucose, amino acids, vitamins and also drugs and toxins from the gut to
the **sinusoids of the liver**. There the liver stores, converts or detoxifies
them, and the blood leaves by the **hepatic veins** into the **inferior vena
cava**.

This is why the liver is the first organ to see what we eat, and why a drug taken
by mouth is partly destroyed before it reaches the rest of the body (the
**first-pass effect**).

```figure caption="The hepatic portal system. Venous blood from the stomach, spleen, pancreas and intestines drains into the portal vein, passes through the liver sinusoids, and leaves by the hepatic veins into the inferior vena cava. No other organ receives the products of digestion before the liver does."
import numpy as np
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.5); ax.set_aspect("equal"); ax.axis("off")
BROWN, BROWNL = "#8a7132", "#e8d2ae"

ax.add_patch(FancyBboxPatch((0.30, 1.90), 2.70, 2.60,
                            boxstyle="round,pad=0,rounding_size=0.12",
                            fc=BROWNL, ec=BROWN, lw=1.3, zorder=2))
ax.text(1.65, 3.55, "LIVER", ha="center", fontsize=7.6, color="#6b4f1d")
ax.text(1.65, 3.12, "sinusoids", ha="center", fontsize=6.9, color="#6b4f1d")

ax.plot([3.00, 6.30], [3.20, 3.20], color=BROWN, lw=7, solid_capstyle="butt",
        zorder=2)
ax.annotate("", xy=(3.10, 3.20), xytext=(4.30, 3.20),
            arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4), zorder=3)

def organ(x, y, w, h, t):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=0.10",
                                fc="#f7e9e9", ec="#a9555e", lw=1.0, zorder=4))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=6.8,
            color=INK, zorder=5)

organ(6.55, 4.05, 1.55, 0.72, "stomach")
organ(8.35, 4.05, 1.45, 0.72, "spleen")
organ(6.55, 1.60, 1.55, 0.72, "intestine")
organ(8.35, 1.60, 1.45, 0.72, "colon")

for x0, y0 in [(7.30, 4.05), (8.35, 4.40), (7.30, 2.32), (8.35, 1.96)]:
    ax.annotate("", xy=(6.36, 3.20), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=BROWN, lw=1.3,
                                connectionstyle="arc3,rad=0.18",
                                shrinkA=1, shrinkB=1), zorder=3)

ax.text(4.65, 2.62, "hepatic portal vein", ha="center", fontsize=7.0,
        color="#6b4f1d")

ax.annotate("", xy=(1.65, 5.55), xytext=(1.65, 4.52),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[0], lw=2.0), zorder=3)
ax.text(1.82, 5.15, "hepatic veins", fontsize=7.0, color=SERIES[0])
ax.text(1.82, 5.80, "to inferior vena cava", fontsize=7.0, color=SERIES[0])
```

### Blood pressure

**Blood pressure** is the force the blood exerts on the vessel wall. It is written
as **systolic/diastolic**: **120/80 mmHg** in a healthy young adult.

- **Systolic pressure** (120) is the peak during ventricular ejection.
- **Diastolic pressure** (80) is the lowest, just before the next beat.
- **Pulse pressure** = systolic − diastolic = **40 mmHg**.
- **Mean arterial pressure** ≈ diastolic + ⅓ pulse pressure ≈ **93 mmHg**.

It is measured with a **sphygmomanometer** and a cuff on the upper arm, at the
level of the heart. As the cuff deflates, the first tapping sound (**Korotkoff
sound**) marks the systolic pressure, and the point at which the sound disappears
marks the diastolic.

| Category | Systolic | Diastolic |
|---|---|---|
| Hypotension | below 90 | below 60 |
| **Normal** | **90–119** | **60–79** |
| Pre-hypertension / high normal | 120–139 | 80–89 |
| **Hypertension** | **140 or more** | **90 or more** |

::: example Mean arterial pressure
**Problem.** A patient's blood pressure is 150/95 mmHg. Find the pulse pressure and
the mean arterial pressure.

**Solution.** Pulse pressure $= 150 - 95 = 55$ mmHg.

$$MAP = DP + \frac{PP}{3} = 95 + \frac{55}{3} = 95 + 18.3 \approx 113\ \text{mmHg}$$

The mean pressure is nearer the diastolic value because the heart spends about
twice as long in diastole as in systole. A MAP below about 60 mmHg means the brain
and kidneys are badly perfused.
:::

Blood pressure depends on **cardiac output** and **peripheral resistance** (the
radius of the arterioles), and also on blood volume, blood viscosity and the
elasticity of the arteries. A **vasoconstriction** of the arterioles raises
pressure; **atherosclerosis** stiffens the arteries and raises the systolic
pressure.

**Regulation** is both nervous and hormonal:

| Mechanism | Where | Effect |
|---|---|---|
| **Baroreceptors** | **carotid sinus** and **aortic arch** | stretch signals to the medulla; a rise in pressure slows the heart and dilates vessels |
| **Chemoreceptors** | carotid and aortic bodies | low O₂, high CO₂ → vasoconstriction and faster heart |
| **Vasomotor centre** | medulla | sets sympathetic tone to arterioles |
| Adrenaline, noradrenaline | adrenal medulla, sympathetic nerves | raise rate, force and resistance |
| **Renin–angiotensin–aldosterone** | kidney | angiotensin II constricts vessels; aldosterone retains Na⁺ and water |
| **ADH** | posterior pituitary | water retention, raises volume |
| **ANP** | heart atria | promotes Na⁺ and water loss, lowers pressure |

::: caution The pulse is not the same as the heart rate in every case
The **pulse** is the wave felt in an artery when the aorta expands in systole. It
normally equals the heart rate, but in some arrhythmias a beat is too weak to
produce a wave, so the pulse rate is lower than the rate on the ECG (a **pulse
deficit**). In an exam, "pulse rate always equals heart rate" is the wrong option.
:::

## 7.3 Blood and blood groups

Blood is a **fluid connective tissue**: cells suspended in a liquid matrix. An
adult has about **5 L** (7–8 % of body mass). If a sample is spun in a
centrifuge, the **plasma** forms about **55 %** and the cells about **45 %**; the
percentage of cells is the **haematocrit** (packed cell volume).

### Plasma

Plasma is **91–92 % water** with **7–8 % protein** and about **0.9 % inorganic
salts**, plus glucose, amino acids, lipids, hormones, urea and CO₂.

| Protein | Percentage of plasma protein | Function |
|---|---|---|
| **Albumin** | **55–60 %** (most abundant) | maintains **osmotic pressure**; carries fatty acids and drugs |
| **Globulins** | about 35 % | α and β carry lipids and vitamins; **γ-globulins are antibodies** |
| **Fibrinogen** | about 4 % | converted to **fibrin** in clotting |

**Serum** is plasma **without fibrinogen** — that is, the fluid left after blood
has clotted.

### The formed elements

| Cell | Count per mm³ | Structure | Function | Life span |
|---|---|---|---|---|
| **Red blood cells (erythrocytes)** | **4.5–5.5 million** | biconcave disc, **no nucleus** in man, filled with **haemoglobin** | carry O₂ and CO₂ | **120 days** |
| **Neutrophils** | 3000–6000 (60–70 % of WBC) | lobed nucleus, granular | **phagocytosis** of bacteria — the first responders | hours to days |
| **Eosinophils** | 2–4 % | bilobed, red granules | attack **parasites**; allergy | days |
| **Basophils** | 0.5–1 % | lobed, blue granules | release **histamine** and **heparin** | days |
| **Lymphocytes** | 20–30 % | round nucleus, little cytoplasm | **B cells** make antibodies; **T cells** kill infected cells | years |
| **Monocytes** | 2–8 % | kidney-shaped nucleus, largest WBC | become **macrophages** | months |
| **Platelets (thrombocytes)** | **1.5–4 lakh** | cell fragments from megakaryocytes | **haemostasis** | 8–10 days |

**Erythropoiesis** — the making of red cells — happens in the **red bone marrow**
of ribs, sternum, vertebrae and pelvis, under the hormone **erythropoietin** from
the kidney, which rises when the kidney senses low oxygen. It needs **iron**
(for haem), **vitamin B₁₂ and folic acid** (for DNA in dividing cells) and
**vitamin B₆**. Old red cells are destroyed by macrophages in the **spleen**,
liver and bone marrow; the iron is recycled and the haem is converted to
**bilirubin**.

### Haemostasis — stopping bleeding

1. **Vascular spasm** — the cut vessel constricts.
2. **Platelet plug** — platelets stick to the collagen, swell and aggregate.
3. **Coagulation** — the clotting cascade. Tissue damage exposes
   **thromboplastin (factor III)**, which with Ca²⁺ and other factors converts
   **prothrombin (II) → thrombin**. Thrombin converts soluble **fibrinogen (I)**
   into insoluble **fibrin** threads that trap the cells into a clot.
4. **Clot retraction and repair** — the clot shrinks, and fibroblasts repair the
   vessel.
5. **Fibrinolysis** — **plasmin** dissolves the clot once the vessel is healed.

There are **13 clotting factors**. **Vitamin K** is needed by the liver to make
**prothrombin and factors VII, IX and X**, and **Ca²⁺ (factor IV)** is required at
several steps — which is why calcium-binding drugs such as citrate stop blood
clotting in a bottle. **Heparin**, from basophils and mast cells, is a natural
anticoagulant.

### Blood groups — ABO and Rh

**Karl Landsteiner** described the **ABO** groups in **1900**. The red cell
carries **agglutinogens (antigens)** and the plasma carries **agglutinins
(antibodies)** against the antigens it does not have:

| Group | Agglutinogen on RBC | Agglutinin in plasma | Can receive red cells from |
|---|---|---|---|
| **A** | **A** | **anti-B** | A, O |
| **B** | **B** | **anti-A** | B, O |
| **AB** | **A and B** | **none** | **A, B, AB, O** |
| **O** | **none** | **anti-A and anti-B** | **O only** |

A transfusion of the wrong group makes the donor cells clump (**agglutination**)
and then burst (**haemolysis**), releasing haemoglobin that can block the kidney
tubules — a transfusion reaction.

- **O negative** is the **universal donor of red cells**: its cells carry no A, B
  or D antigen, so no recipient's antibodies can attack them.
- **AB positive** is the **universal recipient**: its plasma has no anti-A,
  anti-B or anti-D.

The **Rh factor** (rhesus antigen, **D antigen**) was found by **Landsteiner and
Wiener in 1940**. About **85 %** of people are **Rh positive**. Anti-D is not
present naturally; it appears only after an Rh-negative person is exposed to Rh-
positive blood.

**Erythroblastosis fetalis (haemolytic disease of the newborn).** An **Rh-negative
mother** carrying an **Rh-positive fetus** is sensitised at delivery, when fetal
cells enter her blood, and makes **anti-D IgG**. In a **later pregnancy** with
another Rh-positive fetus, that IgG crosses the placenta and destroys the fetal
red cells: the baby is born anaemic and jaundiced, and may die. It is prevented by
giving the mother **anti-D immunoglobulin** after the first delivery.

::: caution The donor rule is about red cells, not plasma
"O negative is the universal donor" is true **for packed red cells**. If whole
plasma were transfused, O plasma contains anti-A and anti-B and would attack A or
B recipient cells. The paper asks the red-cell rule; answer O negative, but know
why.
:::

```photogrid label="7.2" cols="2" ratio="1.2" caption="Inheriting blood groups. (a) Human blood: red cells, white cells and platelets in plasma; the ABO antigens sit on the red cell membrane. (b) The gene I has three alleles: IA and IB are co-dominant and IO is recessive. A cross IA IO x IB IO gives 4 equally likely types of child: AB, A, B and O, 25 per cent each, so all four groups can come from one pair of parents. A cross IA IO x IA IO gives 75 per cent group A and 25 per cent group O. Blood group O is therefore the universal donor for red cells, and AB is the universal recipient."
@ photo id="bio12/human-blood" cap="Human blood film"
fit 1.2
focus 0.5 0.5
@ svg cap="Offspring of two crosses (per cent)"
def ph(a, b):
    s = {a, b}
    return "AB" if s == {"A", "B"} else "A" if "A" in s else "B" if "B" in s else "O"
def cross(p1, p2):
    kids = [ph(x, y) for x in p1 for y in p2]
    return {g: 100 * kids.count(g) / 4 for g in ("A", "B", "AB", "O")}
c1 = cross(("A", "O"), ("B", "O")); c2 = cross(("A", "O"), ("A", "O"))
assert c1 == {"A": 25, "B": 25, "AB": 25, "O": 25} and c2 == {"A": 75, "B": 0, "AB": 0, "O": 25}
facts = dict(c1=4, c2="%.0f" % c2["A"], c3="%.0f" % c2["O"])
f = Fig(300, 236)
f.text(150, 12, "Phenotype of the children (per cent)", size=10.5, color=NAVY, bold=True)
cols = {"A": (BLUE, NAVY), "B": (MINT, TEAL), "AB": (SAND, AMBER), "O": (ROSE, RED)}
for i, (lab, c) in enumerate((("IA IO x IB IO", c1), ("IA IO x IA IO", c2))):
    y = 36 + i * 76
    f.text(10, y, lab, size=10.5, color=SLATE, bold=True, anchor="start")
    x = 10
    for g in ("A", "B", "AB", "O"):
        if c[g]:
            fl, st = cols[g]
            f.box(x, y + 8, c[g] * 2.8, 30, fill=fl, stroke=st, r=0, sw=1.3)
            f.text(x + c[g] * 1.4, y + 23, "%s %g" % (g, c[g]), size=10.5, color=st, bold=True, vmid=True)
            x += c[g] * 2.8
f.text(150, 200, "IA and IB co-dominant; IO recessive", size=10.5, color=NAVY, bold=True)
f.text(150, 216, "AB x O parents give only A or B children", size=10.5, color=SLATE, bold=True)
```

## 7.4 Cardiovascular disorders

| Disorder | What happens | Cause / risk | Key feature |
|---|---|---|---|
| **Atherosclerosis** | fatty streaks → **plaque** of cholesterol, cells and calcium in the arterial intima; lumen narrows and the wall stiffens | high LDL, smoking, hypertension, diabetes, obesity, family history | angina, heart attack, stroke, gangrene |
| **Angina pectoris** | **reversible** ischaemia of the heart muscle | narrowed coronary arteries | crushing chest pain on exertion, relieved by **rest or nitrates** |
| **Myocardial infarction (heart attack)** | a coronary artery is blocked by a **thrombus**; part of the muscle dies | plaque rupture, smoking, hypertension | severe chest pain radiating to the **left arm and jaw**, sweating, **ST elevation**, **troponin** rises |
| **Hypertension** | sustained BP ≥ 140/90 | age, salt, obesity, stress, kidney disease | "silent killer": stroke, heart failure, kidney damage |
| **Varicose veins** | dilated, tortuous, elongated veins with **incompetent valves** | long standing, pregnancy, heredity | aching legs, visible blue swellings; worse in the lower limb |
| **Anaemia** | haemoglobin below normal | iron deficiency (commonest), B₁₂ deficiency, blood loss, haemolysis | pallor, fatigue, breathlessness, fast pulse |
| **Stroke** | blood supply to part of the brain is cut | thrombus, embolus, haemorrhage | sudden weakness, speech loss |

**Atherosclerosis** begins with injury to the endothelium; **LDL cholesterol**
enters the wall, is oxidised, and macrophages swallow it to become "foam cells".
Smooth muscle and collagen form a fibrous cap over a lipid core. A plaque may
rupture, exposing the core to blood, and a clot forms on it — the event that
causes most heart attacks and strokes.

**Anaemia** is classified by the size of the red cells:

| Type | Cause | Cell size |
|---|---|---|
| **Iron-deficiency** | poor diet, blood loss, pregnancy | **microcytic, hypochromic** |
| **Pernicious** | lack of **intrinsic factor** → no B₁₂ absorption | **macrocytic** |
| **Haemolytic** | red cells destroyed (malaria, sickle cell, Rh disease) | normal or abnormal shape |
| **Aplastic** | bone marrow fails (drugs, radiation) | few cells of all types |

::: tip Telling the chest pains apart
**Angina**: pain on exertion, lasts minutes, relieved by rest or a nitrate, no
enzyme rise. **Heart attack**: pain at rest, lasts longer, not relieved, with
sweating and nausea, **ECG changes and raised troponin**. That single contrast
answers most clinical stems.
:::

## Formula and fact sheet

**The heart**

| Fact | Value |
|---|---|
| Mass | 250–300 g |
| Chambers / valves | 4 / 4 (2 AV, 2 semilunar) |
| Thickest wall | **left ventricle** |
| Pacemaker | **SA node**, 70–80 min⁻¹ |
| AV node rate / delay | 40–60 min⁻¹ / **0.1 s** |
| Fastest conduction | **Purkinje fibres, 4 m s⁻¹** |
| Slowest conduction | **AV node, 0.05 m s⁻¹** |
| Cardiac cycle at 72–75 min⁻¹ | **0.8 s** (atrial systole 0.1, ventricular systole 0.3, diastole 0.5) |
| Stroke volume | **70 mL** |
| End-diastolic / end-systolic volume | 120 / 50 mL |
| Ejection fraction | **≈ 60 %** |
| Cardiac output | **≈ 5 L min⁻¹** |
| S1 / S2 | AV valves close / semilunar valves close |

**ECG**

| Wave | Meaning |
|---|---|
| P | atrial depolarisation |
| QRS | ventricular depolarisation |
| T | ventricular repolarisation |
| PR interval | 0.12–0.20 s (AV nodal delay) |

**Vessels and pressure**

| Fact | Value |
|---|---|
| Normal BP | **120/80 mmHg** |
| Pulse pressure | 40 mmHg |
| Mean arterial pressure | ≈ 93 mmHg |
| Hypertension | **≥ 140/90** |
| Hypotension | < 90/60 |
| Largest artery / vein | aorta / vena cava |
| Portal vein formed by | superior mesenteric + splenic veins |

**Blood**

| Fact | Value |
|---|---|
| Volume | about 5 L |
| Plasma / cells | 55 % / 45 % |
| Plasma water / protein | 91–92 % / 7–8 % |
| Most abundant plasma protein | **albumin** (55–60 %) |
| RBC count | **4.5–5.5 million/mm³** |
| RBC life span | **120 days** |
| Haemoglobin | 13–17 g/dL (about 15) |
| WBC count | **4000–11 000/mm³** |
| Neutrophil / lymphocyte / monocyte | 60–70 % / 20–30 % / 2–8 % |
| Platelets | **1.5–4 lakh/mm³** |
| Clotting factors | 13; vitamin K for II, VII, IX, X |

**Blood groups**

| Group | Antigen | Antibody |
|---|---|---|
| A | A | anti-B |
| B | B | anti-A |
| AB | A + B | none |
| O | none | anti-A + anti-B |

- **Universal donor (red cells): O negative.**
- **Universal recipient: AB positive.**
- **Rh positive: about 85 %**; anti-D causes **erythroblastosis fetalis**.
- ABO described by **Landsteiner (1900)**; Rh by **Landsteiner and Wiener (1940)**.

**Traps**

1. The **left ventricle** wall is thickest.
2. The **pulmonary artery** carries **deoxygenated** blood; the **pulmonary vein** carries oxygenated blood.
3. **O negative** is the universal donor; **AB positive** the universal recipient.
4. **S1 = AV valves**, **S2 = semilunar valves**.
5. **Most CO₂ is carried as bicarbonate** (unit 6), not by red cells alone.
6. **Veins have valves; arteries do not.**
7. The **SA node**, not the AV node, is the pacemaker.
8. **Cardiac output = SV × HR**, not SV + HR.

## Chapter summary

- The heart (250–300 g) lies in the mediastinum inside the **pericardium**; its wall is epicardium, **myocardium** (thickest in the **left ventricle**) and endocardium.
- Four chambers and four valves: **tricuspid** and **bicuspid (mitral)** AV valves with chordae tendineae, and the **pulmonary** and **aortic** semilunar valves; all open and close **passively**.
- **Double circulation**: right ventricle → lungs → left atrium (pulmonary); left ventricle → body → right atrium (systemic). The **coronary arteries** arise from the ascending aorta.
- The **SA node** (70–80 min⁻¹) is the pacemaker because it depolarises fastest; the impulse passes **SA → AV → bundle of His → Purkinje**, with a **0.1 s delay at the AV node**.
- The **cardiac cycle** lasts **0.8 s**: atrial systole 0.1 s, ventricular systole 0.3 s, diastole 0.5 s; **S1** is AV valve closure, **S2** semilunar closure.
- **CO = SV × HR ≈ 70 × 72 ≈ 5 L min⁻¹**; ejection fraction ≈ 60 %; exercise raises output to 20–25 L min⁻¹.
- **ECG**: P = atrial depolarisation, QRS = ventricular depolarisation, T = ventricular repolarisation.
- **Arteries** are thick-walled, valveless and high-pressure; **veins** are thin-walled, valved and low-pressure; the **hepatic portal vein** carries gut blood to the liver before the heart.
- **BP 120/80**; hypertension ≥ 140/90; baroreceptors in the **carotid sinus and aortic arch**; the medulla sets vasomotor tone.
- Blood is 55 % plasma and 45 % cells; **RBC 5 million/mm³ and 120 days**, **WBC 4000–11 000/mm³**, **platelets 1.5–4 lakh/mm³**; **albumin** is the commonest plasma protein.
- **Haemostasis**: spasm → platelet plug → **prothrombin → thrombin → fibrin** → clot retraction → fibrinolysis.
- **ABO**: A has anti-B, B has anti-A, AB has none, O has both; **O− donor, AB+ recipient**; **Rh** incompatibility causes **erythroblastosis fetalis**.
- Disorders: **atherosclerosis** (plaque), **angina** (reversible), **MI** (thrombus, troponin), **varicose veins** (valve failure), **anaemia** (low haemoglobin).

## Practice questions

**Set A — Recall (29 questions)**

1. The pacemaker of the human heart is the
   (a) AV node (b) bundle of His (c) SA node (d) Purkinje fibre
2. The left atrioventricular valve is also called the
   (a) tricuspid valve (b) bicuspid valve (c) pulmonary valve (d) aortic valve
3. The number of chambers in the human heart is
   (a) two (b) three (c) five (d) four
4. The heart is enclosed in a sac called the
   (a) pericardium (b) pleura (c) peritoneum (d) mesentery
5. At 75 beats per minute, one cardiac cycle lasts
   (a) 0.3 s (b) 0.8 s (c) 1.0 s (d) 0.5 s
6. The stroke volume of a resting adult is about
   (a) 70 mL (b) 120 mL (c) 5 L (d) 50 mL
7. The cardiac output of a resting adult is about
   (a) 70 mL (b) 500 mL (c) 5 L per minute (d) 50 L per minute
8. The first heart sound is produced by closure of the
   (a) semilunar valves (b) opening of the AV valves (c) blood entering the aorta (d) atrioventricular valves
9. The P wave of an ECG represents
   (a) atrial depolarisation (b) ventricular depolarisation (c) ventricular repolarisation (d) atrial repolarisation
10. The QRS complex of an ECG represents
   (a) atrial depolarisation (b) atrial repolarisation (c) ventricular repolarisation (d) ventricular depolarisation
11. The T wave of an ECG represents
   (a) atrial systole (b) ventricular depolarisation (c) ventricular repolarisation (d) closure of the valves
12. The impulse is delayed on its way from the atria to the ventricles at the
   (a) SA node (b) AV node (c) bundle of His (d) Purkinje fibres
13. The normal blood pressure of a young adult is
   (a) 80/120 mmHg (b) 140/90 mmHg (c) 100/70 mmHg (d) 120/80 mmHg
14. Blood pressure is measured with a
   (a) stethoscope (b) spirometer (c) sphygmomanometer (d) electrocardiograph
15. The universal donor for red cells is
   (a) O negative (b) AB positive (c) A positive (d) B negative
16. The universal recipient of blood is
   (a) O negative (b) AB positive (c) A negative (d) B positive
17. Rh incompatibility between mother and fetus causes
   (a) jaundice in the mother (b) erythroblastosis fetalis (c) haemophilia (d) leukaemia
18. The most numerous formed element of blood is the
   (a) white blood cell (b) platelet (c) lymphocyte (d) red blood cell
19. The average life span of a human red blood cell is
   (a) 120 days (b) 60 days (c) 30 days (d) 180 days
20. The normal white blood cell count per mm³ is
   (a) 4–5 million (b) 1.5–4 lakh (c) 4000–11 000 (d) 500–1000
21. The normal platelet count per mm³ is
   (a) 4–5 million (b) 4000–11 000 (c) 1.5–4 lakh (d) 5–10 lakh
22. The most abundant protein of plasma is
   (a) albumin (b) globulin (c) fibrinogen (d) prothrombin
23. Vitamin K is required for the synthesis of
   (a) haemoglobin (b) albumin (c) platelets (d) prothrombin
24. The hepatic portal vein is formed by the union of the
   (a) hepatic vein and inferior vena cava (b) superior mesenteric and splenic veins (c) renal and iliac veins (d) jugular and subclavian veins
25. Which vessel carries deoxygenated blood?
   (a) aorta (b) pulmonary artery (c) pulmonary vein (d) carotid artery
26. The coronary arteries arise from the
   (a) pulmonary trunk (b) arch of the aorta (c) ascending aorta (d) brachiocephalic artery
27. A heart attack is caused by blockage of a
   (a) pulmonary artery (b) carotid artery (c) renal artery (d) coronary artery
28. Varicose veins are caused mainly by
   (a) incompetent valves in the veins (b) atherosclerosis (c) anaemia (d) hypertension
29. Which of the following is a granulocyte?
   (a) lymphocyte (b) monocyte (c) neutrophil (d) red blood cell

::: note Answers and explanations — Set A
**1.** (c) — the SA node, in the wall of the right atrium, depolarises fastest and so sets the rhythm.
**2.** (b) — the bicuspid or mitral valve, on the left side; the tricuspid is on the right.
**3.** (d) — two atria and two ventricles, making the heart a double pump.
**4.** (a) — the pericardium, with fibrous and serous layers and a film of fluid between them.
**5.** (b) — 0.8 s, made up of atrial systole 0.1 s, ventricular systole 0.3 s and diastole 0.5 s.
**6.** (a) — about 70 mL per beat; 120 mL is the end-diastolic volume and 50 mL the end-systolic volume.
**7.** (c) — 70 mL × 72 ≈ 5 L per minute.
**8.** (d) — S1 is the closure of the AV valves at the start of ventricular systole; S2 is the closure of the semilunar valves.
**9.** (a) — atrial depolarisation, which just precedes atrial systole.
**10.** (d) — ventricular depolarisation. Atrial repolarisation is hidden inside the same complex.
**11.** (c) — ventricular repolarisation; the ventricles recover before the next beat.
**12.** (b) — the AV node conducts at only 0.05 m s⁻¹, giving a delay of about 0.1 s.
**13.** (d) — 120/80 mmHg. 140/90 is the threshold for hypertension.
**14.** (c) — the sphygmomanometer, with a cuff and a mercury or digital gauge.
**15.** (a) — O negative red cells carry no A, B or D antigen, so no recipient has antibodies against them.
**16.** (b) — AB positive plasma has no anti-A, anti-B or anti-D.
**17.** (b) — anti-D from a sensitised Rh-negative mother destroys fetal red cells.
**18.** (d) — about 5 million red cells per mm³, against 4000–11 000 white cells.
**19.** (a) — 120 days; about 2 million are destroyed every second and replaced by the marrow.
**20.** (c) — 4000–11 000 per mm³. 4–5 million is the red cell count.
**21.** (c) — 1.5–4 lakh per mm³, from megakaryocytes.
**22.** (a) — albumin, 55–60 % of plasma protein; it holds the osmotic pressure.
**23.** (d) — prothrombin and factors VII, IX and X are made in the liver and need vitamin K.
**24.** (b) — the superior mesenteric and splenic veins join behind the pancreas.
**25.** (b) — the pulmonary artery carries blood from the right ventricle to the lungs.
**26.** (c) — the right and left coronary arteries leave the ascending aorta just above the aortic valve.
**27.** (d) — a coronary artery blocked by a thrombus starves part of the muscle, which dies.
**28.** (a) — the valves fail, blood pools and the vein stretches and becomes tortuous.
**29.** (c) — neutrophils, eosinophils and basophils have granules; lymphocytes and monocytes do not.
:::

**Set B — Understanding (17 questions)**

1. The wall of the left ventricle is the thickest because it
   (a) holds the largest volume of blood (b) lies closest to the lungs (c) pumps blood round the whole body (d) receives oxygenated blood
2. The SA node sets the rhythm of the heart because it
   (a) has the fastest rate of spontaneous depolarisation (b) is the largest part of the conducting system (c) has the richest nerve supply (d) lies in the left atrium
3. The AV valves close at the start of ventricular systole because
   (a) the atria contract at that moment (b) the semilunar valves open (c) blood pushes them shut from below (d) ventricular pressure rises above atrial pressure
4. The delay at the AV node is useful because it
   (a) lets the atria fill with blood (b) lets the atria empty completely before the ventricles contract (c) slows the heart rate (d) keeps the semilunar valves closed
5. The pulmonary artery carries deoxygenated blood because it
   (a) carries blood from the right ventricle to the lungs (b) is really a vein in structure (c) has a very thin wall (d) carries blood towards the heart
6. Blood pressure is higher in arteries than in veins because arteries
   (a) contain more blood (b) are closer to the pump and have thick elastic walls (c) contain valves (d) are wider than veins
7. Veins in the legs have valves in order to
   (a) raise the pressure of the blood (b) slow the flow of blood (c) prevent backflow when pressure is low (d) filter the blood
8. O negative blood can be given to anyone because its red cells
   (a) carry both A and B antigens (b) carry no antibodies (c) are the commonest type (d) carry no A, B or D antigen
9. AB positive blood can receive any group because its plasma
   (a) has no antigens (b) has all the antibodies (c) is Rh negative (d) has no anti-A, anti-B or anti-D
10. Erythroblastosis fetalis usually appears in a second pregnancy because
   (a) the second baby is Rh negative (b) the mother was sensitised in the first pregnancy (c) the father is Rh negative (d) the first baby was AB positive
11. Cardiac muscle does not fatigue because it
   (a) has a long refractory period and rests in diastole (b) has no nerve supply (c) does not use oxygen (d) contains no mitochondria
12. The hepatic portal vein is important because it
   (a) carries oxygen to the liver (b) drains blood from the heart (c) takes absorbed nutrients to the liver first (d) carries hormones to the brain
13. The ECG shows no separate wave for atrial repolarisation because it
   (a) is hidden inside the QRS complex (b) never happens (c) is too small to record (d) comes after the T wave
14. The second heart sound is shorter and sharper than the first because the
   (a) AV valves are larger (b) atria contract at that moment (c) semilunar valves snap shut against high pressure (d) blood flow stops completely
15. The pulse is felt as a wave because the
   (a) blood flows in a continuous stream (b) aorta expands with each systole (c) veins contract rhythmically (d) heart moves inside the chest
16. Blood pressure is measured on the arm held at heart level so that
   (a) the cuff fits easily (b) the artery is at its widest (c) no valves interfere (d) the reading is not changed by gravity
17. Severe anaemia makes the pulse fast because the heart
   (a) compensates for poor oxygen carriage by raising its output (b) becomes weaker (c) is compressed by the lungs (d) loses its nerve supply

::: note Answers and explanations — Set B
**1.** (c) — the systemic circuit has a much higher resistance, so the left ventricle needs a much thicker muscle.
**2.** (a) — its membrane reaches threshold first, so it fires before the slower latent pacemakers can.
**3.** (d) — the valves are passive: when ventricular pressure exceeds atrial pressure they are pushed shut.
**4.** (b) — the 0.1 s delay allows complete filling, so stroke volume is not wasted.
**5.** (a) — it is an artery by structure but carries deoxygenated blood from the right ventricle to the lungs.
**6.** (b) — pressure falls steadily along the circuit because of resistance; the elastic aorta also smooths the flow.
**7.** (c) — venous pressure is too low to push blood up the leg against gravity, so valves and the muscle pump do the work.
**8.** (d) — with no A, B or D antigen on the red cells, no recipient's plasma has an antibody that can clump them.
**9.** (d) — the plasma of AB positive has no antibodies at all, so it does not attack transfused cells.
**10.** (b) — the first delivery sensitises the mother, who then makes anti-D IgG that crosses the placenta next time.
**11.** (a) — the long refractory period prevents tetanus, and the heart rests for about 0.5 s in every 0.8 s cycle.
**12.** (c) — first-pass delivery lets the liver store, convert or detoxify what the gut has absorbed.
**13.** (a) — atrial repolarisation coincides with ventricular depolarisation and is buried in the QRS.
**14.** (c) — the semilunar valves close suddenly against the high pressure of the aorta and pulmonary artery.
**15.** (b) — each systole pushes blood into the aorta, which stretches and then recoils, sending a wave along the arteries.
**16.** (d) — hydrostatic pressure would add to or subtract from the reading if the arm were above or below heart level.
**17.** (a) — with less haemoglobin the heart raises output to keep oxygen delivery up, so the pulse is fast.

:::

**Set C — Application (10 questions)**

1. A man has a stroke volume of 80 mL and a heart rate of 75 per minute. His cardiac output is
   (a) 5.0 L min⁻¹ (b) 6.0 L min⁻¹ (c) 0.6 L min⁻¹ (d) 60 L min⁻¹
2. A patient's end-diastolic volume is 120 mL and end-systolic volume 50 mL. His ejection fraction is
   (a) 70 % (b) 50 % (c) 42 % (d) 58 %
3. A patient's blood pressure is 140/90 mmHg. His pulse pressure is
   (a) 50 mmHg (b) 230 mmHg (c) 40 mmHg (d) 90 mmHg
4. For the same patient, the mean arterial pressure is about
   (a) 115 mmHg (b) 90 mmHg (c) 107 mmHg (d) 140 mmHg
5. A 55-year-old has crushing chest pain at rest, sweating, ST elevation and a raised troponin. The diagnosis is
   (a) angina pectoris (b) pericarditis (c) asthma (d) myocardial infarction
6. A shopkeeper who stands all day has dilated, tortuous veins in both legs that ache in the evening. The condition is
   (a) varicose veins (b) myocardial infarction (c) anaemia (d) hypertension
7. A newborn is deeply jaundiced within 24 hours; the mother is O negative and the baby A positive. The cause is
   (a) iron deficiency (b) physiological jaundice only (c) ABO incompatibility with haemolysis (d) congenital heart disease
8. A man loses 1 litre of blood in an accident. The immediate compensation is
   (a) a rise in red cell production within hours (b) tachycardia and vasoconstriction (c) a fall in ADH secretion (d) bradycardia
9. A man has readings of 160/100 mmHg on three separate visits. He has
   (a) hypotension (b) normal pressure (c) a pulse deficit (d) hypertension
10. A woman has fatigue and breathlessness; her haemoglobin is 8 g/dL and the red cells are microcytic and hypochromic. The likely cause is
   (a) iron deficiency (b) vitamin B₁₂ deficiency (c) haemolysis (d) aplastic anaemia

::: note Answers and explanations — Set C
**1.** (b) — CO = SV × HR = 80 × 75 = 6000 mL = 6.0 L min⁻¹.
**2.** (d) — SV = 120 − 50 = 70 mL; EF = 70/120 = 0.58 = 58 %.
**3.** (a) — pulse pressure = systolic − diastolic = 140 − 90 = 50 mmHg.
**4.** (c) — MAP = diastolic + ⅓ pulse pressure = 90 + 50/3 ≈ 107 mmHg.
**5.** (d) — pain at rest with ST elevation and raised troponin means muscle is dying: infarction, not angina.
**6.** (a) — long standing raises venous pressure; the valves fail and the veins dilate.
**7.** (c) — maternal anti-A (and anti-D if Rh negative) crossed the placenta and haemolysed the baby's cells.
**8.** (b) — the baroreceptor reflex raises heart rate and constricts vessels; new red cells take days, not hours.
**9.** (d) — 160/100 on repeated readings is hypertension (≥ 140/90).
**10.** (a) — microcytic, hypochromic cells with low haemoglobin are the signature of iron deficiency; B₁₂ deficiency gives macrocytic cells.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Describe the structure of the human heart and explain the cardiac cycle and cardiac output. <span class="marks">[10]</span>
2. Compare arteries, veins and capillaries; explain blood pressure and the common cardiovascular disorders. <span class="marks">[10]</span>
3. Describe the composition and functions of blood and the ABO and Rh blood groups. <span class="marks">[10]</span>

```photogrid label="7.H" cols="5" ratio="1.1" caption="The circulatory system. (a) A numbered diagram of the human heart. (b) A real heart cut to show its chambers. (c) A normal ECG trace with P, QRS and T waves. (d) Measuring blood pressure with a sphygmomanometer. (e) A blood smear with red cells and a white cell."
@ photo id="bio12/heart-numbered" cap="(a) Heart diagram"
fit 1.1
focus 0.5 0.5
@ photo id="sci10/heart-real" cap="(b) Real heart"
fit 1.1
focus 0.5 0.5
@ photo id="bio12/ecg" cap="(c) ECG"
fit 1.1
focus 0.5 0.5
@ photo id="ceezoo/bp" cap="(d) Blood pressure"
fit 1.1
focus 0.5 0.5
@ photo id="sci10/blood-smear" cap="(e) Blood smear"
fit 1.1
focus 0.5 0.5
```

### Model answer D1: The heart and the cardiac cycle (10 marks)

**Introduction.** The human heart is a hollow muscular organ about the size of a fist, lying between the lungs, slightly to the left. It is covered by the **pericardium** and weighs about 300 g.

**Structure.** The heart has **four chambers**: the right atrium and right ventricle (**deoxygenated** blood) and the left atrium and left ventricle (**oxygenated** blood). The left ventricle wall is thickest as it pumps blood to the whole body. **Valves** keep blood flowing one way: the **tricuspid** valve (right) and **bicuspid (mitral)** valve (left) between atrium and ventricle, and the **aortic** and **pulmonary semilunar** valves at the exits.

**Conduction system.** The **sino-atrial (SA) node** (pacemaker) in the right atrium starts each beat → **atrio-ventricular (AV) node** → **bundle of His** → **Purkinje fibres** in the ventricles. The heart is **myogenic**, as the beat starts in the heart muscle itself.

**Cardiac cycle (0.8 s at 75 beats per minute).**

1. **Atrial systole (0.1 s):** both atria contract and fill the ventricles.
2. **Ventricular systole (0.3 s):** the AV valves close (first sound **"lub"**), pressure rises, and the semilunar valves open to eject blood into the aorta and pulmonary artery.
3. **Joint diastole (0.4 s):** the semilunar valves close (second sound **"dup"**), all chambers relax and blood flows in.

**Cardiac output.** Cardiac output = stroke volume × heart rate. With a stroke volume of 70 mL and a rate of 72 beats/min, CO = 70 × 72 = 5040 mL ≈ **5 L per minute**, so the total blood volume (5 L) passes through the heart each minute.

**ECG.** The **P wave** shows atrial depolarisation, the **QRS complex** shows ventricular depolarisation and the **T wave** shows ventricular repolarisation.

| Heart sound | Cause | Time |
|---|---|---|
| Lub | Closing of AV valves | Start of ventricular systole |
| Dup | Closing of semilunar valves | Start of diastole |

**Conclusion.** Coordinated contraction of atria and ventricles, directed by the SA node and valves, keeps the double circulation moving.

### Model answer D2: Blood vessels, blood pressure and disorders (10 marks)

**Introduction.** Blood travels in a **double circulation**: the **pulmonary circuit** (heart → lungs → heart) and the **systemic circuit** (heart → body → heart). Three kinds of vessel are involved.

| Feature | Artery | Vein | Capillary |
|---|---|---|---|
| Direction | Away from heart | To heart | Between artery and vein |
| Wall | Thick, elastic | Thin | One cell thick |
| Valves | Absent (except at origin) | Present | Absent |
| Blood | Oxygenated (except pulmonary) | Deoxygenated (except pulmonary) | Exchange of materials |
| Pressure | High | Low | Falling |

**Blood pressure (BP).** It is the force of blood on the vessel wall, measured by a **sphygmomanometer** over the brachial artery. Normal BP is **120/80 mm Hg** (systolic/diastolic). **Pulse pressure** = 120 − 80 = 40 mm Hg. Pressure falls from arteries to veins. It depends on cardiac output, blood volume, and the resistance of arterioles.

**Cardiovascular disorders.**

1. **Hypertension:** BP above 140/90 mm Hg; a "silent killer" that damages the heart, brain and kidneys. Salt and stress raise it.
2. **Atherosclerosis:** fats (cholesterol) deposit in artery walls and narrow them.
3. **Coronary artery disease (CAD):** the arteries to the heart muscle are narrowed, causing **angina**.
4. **Heart attack (myocardial infarction):** a clot blocks a coronary artery and part of the heart muscle dies.
5. **Stroke:** a brain vessel bursts or is blocked.
6. **Heart failure:** the heart cannot pump enough blood.

**Prevention.** Eat less salt, fat and sugar, exercise, avoid tobacco and alcohol, and check BP regularly, which is a free service in many Nepali health posts.

**Conclusion.** The structure of each vessel fits its job, and a healthy life style keeps blood pressure and the vessels normal.

### Model answer D3: Blood and blood groups (10 marks)

**Introduction.** **Blood** is a red fluid connective tissue. An adult has about **5 litres**, which is 7–8% of body weight, and its pH is about 7.4.

**Composition.**

1. **Plasma (55%):** 90–92% water with proteins (albumin, globulin, fibrinogen), glucose, salts, hormones and wastes.
2. **Red blood corpuscles (RBC):** biconcave, **non-nucleated**, with haemoglobin; 5–5.5 million per mm³; life 120 days; made in red bone marrow; carry O₂.
3. **White blood corpuscles (WBC):** 5,000–10,000 per mm³; granulocytes (neutrophil, eosinophil, basophil) and agranulocytes (lymphocyte, monocyte); defend the body.
4. **Platelets:** 1.5–4 lakh per mm³; help clotting.

**Functions.** Transport of gases, food, hormones and wastes; defence; clotting; regulation of temperature and pH.

**ABO blood groups.** They depend on antigens on RBCs and antibodies in plasma (Landsteiner, 1900).

| Group | Antigen on RBC | Antibody in plasma | Can donate to | Can receive from |
|---|---|---|---|---|
| A | A | anti-B | A, AB | A, O |
| B | B | anti-A | B, AB | B, O |
| AB | A and B | None | AB (universal recipient) | All |
| O | None | anti-A, anti-B | All (universal donor) | O |

**Rh factor.** People with the Rh antigen are **Rh-positive** (about 85%) and others are **Rh-negative**. If an Rh-negative mother carries an Rh-positive baby, her antibodies may destroy the red cells of a later baby (**erythroblastosis foetalis**). A shot of anti-D after the first birth prevents this.

**Clotting.** Damaged tissue releases thromboplastin; with Ca²⁺ it turns prothrombin into thrombin, which changes fibrinogen into **fibrin threads** that trap cells and form a clot.

**Conclusion.** Blood links all organs and defends the body, and matching the blood group is vital in transfusion.

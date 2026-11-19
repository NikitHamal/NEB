---
file: NEBians-BLE-Past-Paper-Grade-8-Science-2082-Kathmandu.pdf
subject: Science and Technology
grade: 8
year_bs: 2082
year_ad: 2026
stream: Basic Level Examination, Kathmandu Metropolitan City
code:
kind: BLE Past Paper
time: 2 hrs
marks: 50
students: Class 8 Basic Level Examination (BLE) Science and Technology paper set by Kathmandu Metropolitan City for 2082 BS (2026 AD). Questions are re-typeset in English from the bilingual published paper; all figures, worked solutions and diagrams are NEBians.
category: Basic Level Exam
---
## Section 'A'
<small>Multiple choice questions · choose the best alternative and write it in the answer sheet · [10×1=10]</small>

@mcq 1(a)
Report of which commission has defined sustainable development clearly?
@opts Kyoto report | Agenda-30 | UNO | Brutland

@mcq 1(b)
Why are seeds not stored in wet and moist places?
@opts-col To increase the size of seeds | To change the color of seeds | To prevent seeds from decaying | To make the seeds heavier

@mcq 1(c)
What is the shortest distance between any two points in a particular direction?
@opts Relative Velocity | Average velocity | Displacement | Speed

@mcq 1(d)
Which one of the followings is not affected by friction?
@opts efficiency | input work | velocity ratio | mechanical advantage

@mcq 1(e)
A car is moving with a velocity of $60\text{ km/h}$ towards a running man who is moving with a velocity of $15\text{ km/h}$ towards the car. What is the velocity of the car with respect to the man?
@opts $15\text{ km/h}$ | $45\text{ km/h}$ | $60\text{ km/h}$ | $75\text{ km/h}$

<div style="break-before:page"></div>

@mcq 1(f)
A block with flat rectangular sides rests on a table in two ways as shown in the diagram given below. How does this change affect the force and pressure exerted by the block kept horizontally on the table?

```figure caption="Question 1(f): a rectangular block resting vertically (top) and horizontally (bottom) on a table."
from matplotlib.patches import Polygon, Rectangle
fig, ax = plt.subplots(figsize=(3.2, 1.25))
# Top table + vertical block
ax.add_patch(Polygon([(0.2,0.95),(2.5,0.95),(2.9,1.2),(0.6,1.2)], fc='#f3f6fc', ec=INK, lw=1.0))
ax.add_patch(Rectangle((1.35,1.08), 0.28, 0.72, fc=ACCENT, alpha=0.25, ec=INK, lw=1.2))
ax.text(2.2, 1.58, 'Block', fontsize=8); ax.annotate('', xy=(1.63,1.58), xytext=(2.15,1.58), arrowprops=dict(arrowstyle='->', color=INK, lw=0.8))
ax.text(2.35, 1.03, 'Table', fontsize=8)
# Bottom table + horizontal block
ax.add_patch(Polygon([(0.2,0.15),(2.5,0.15),(2.9,0.4),(0.6,0.4)], fc='#f3f6fc', ec=INK, lw=1.0))
ax.add_patch(Rectangle((1.1,0.26), 0.78, 0.24, fc=ACCENT, alpha=0.25, ec=INK, lw=1.2))
ax.set_xlim(0, 3.1); ax.set_ylim(0.05, 1.9); ax.axis('off')
```

| Option | Force | Pressure |
| --- | --- | --- |
| A | Decreased | Decreased |
| B | Decreased | Unchanged |
| C | Unchanged | Decreased |
| D | Unchanged | Unchanged |

@opts Option A | Option B | Option C | Option D

@mcq 1(g)
The given diagram shows a domestic circuit. Connecting which device threatens consumer's safety?

```figure caption="Question 1(g): domestic wiring diagram with live (L), neutral (N) and earth (E) lines."
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.8, 1.55))
# Live (L) and Neutral (N) lines
ax.plot([0.2, 1.0], [1.55, 1.55], color=INK, lw=1.1); ax.text(0.05, 1.55, 'L', fontsize=8, va='center', fontweight='bold')
ax.add_patch(Rectangle((1.0, 1.43), 0.42, 0.24, fc='white', ec=INK, lw=1.0)); ax.text(1.21, 1.73, 'main fuse $F_1$', fontsize=6.5, ha='center')
ax.plot([1.05, 1.37], [1.55, 1.55], color=INK, lw=0.9)
ax.plot([1.42, 1.75], [1.55, 1.55], color=INK, lw=1.1)
ax.plot([0.2, 1.75], [1.25, 1.25], color=INK, lw=1.1); ax.text(0.05, 1.25, 'N', fontsize=8, va='center', fontweight='bold')
# Meter
ax.add_patch(Rectangle((1.75, 1.12), 0.52, 0.58, fc='#f3f6fc', ec=INK, lw=1.1))
ax.text(2.01, 1.76, 'meter', fontsize=6.5, ha='center'); ax.text(2.01, 1.41, 'kWh', fontsize=7, ha='center', va='center')
ax.plot([2.27, 2.6], [1.55, 1.55], color=INK, lw=1.1); ax.plot([2.27, 2.6], [1.25, 1.25], color=INK, lw=1.1)
# Main switch S
ax.add_patch(Rectangle((2.55, 1.12), 0.48, 0.58, fc='white', ec=INK, lw=1.1)); ax.text(2.79, 1.76, 'main switch $S$', fontsize=6.3, ha='center')
ax.plot([2.55, 3.03], [1.55, 1.55], color=INK, lw=1.0); ax.plot([2.55, 3.03], [1.25, 1.25], color=INK, lw=1.0)
# Consumer fuse F2
ax.plot([3.03, 3.45], [1.55, 1.55], color=INK, lw=1.1)
ax.add_patch(Rectangle((3.45, 1.43), 0.42, 0.24, fc='white', ec=INK, lw=1.0)); ax.text(3.66, 1.73, 'fuse $F_2$', fontsize=6.3, ha='center')
ax.plot([3.48, 3.84], [1.55, 1.55], color=INK, lw=0.9)
ax.plot([3.87, 5.6], [1.55, 1.55], color=INK, lw=1.1); ax.annotate('', xy=(5.55, 1.63), xytext=(5.15, 1.63), arrowprops=dict(arrowstyle='->', color=INK, lw=0.8)); ax.text(5.05, 1.63, 'to fan', fontsize=6.5, ha='right', va='center')
ax.plot([3.03, 5.6], [1.25, 1.25], color=INK, lw=1.1)
# Earth line E
ax.plot([2.79, 2.79], [1.12, 0.25], color=INK, lw=1.0); ax.plot([2.59, 2.99], [0.25, 0.25], color=INK, lw=1.2); ax.plot([2.67, 2.91], [0.18, 0.18], color=INK, lw=1.0)
ax.text(2.65, 0.65, 'E', fontsize=7, fontweight='bold'); ax.text(3.05, 0.24, 'earth', fontsize=6.3)
ax.plot([2.79, 3.9], [0.85, 0.85], color=INK, lw=0.9); ax.plot([3.9, 3.9], [0.85, 1.25], color=INK, lw=0.9)
# Bulb branch
ax.plot([4.2, 4.2], [1.55, 0.42], color=INK, lw=0.9); ax.plot([4.2, 4.75], [0.42, 0.42], color=INK, lw=0.9); ax.text(4.45, 0.20, 'switch $S_1$', fontsize=6.2, ha='center')
ax.plot([4.75, 4.75], [0.42, 1.25], color=INK, lw=0.9)
ax.add_patch(Circle((4.75, 0.88), 0.14, fc='white', ec=INK, lw=1.0)); ax.text(4.75, 0.62, 'bulb', fontsize=6.3, ha='center')
# Socket branch
ax.plot([5.12, 5.12], [1.25, 0.42], color=INK, lw=0.9); ax.plot([5.12, 5.45], [0.42, 0.42], color=INK, lw=0.9); ax.text(5.15, 0.20, 'switch $S_2$', fontsize=6.2, ha='center')
ax.plot([5.45, 5.45], [1.55, 0.58], color=INK, lw=0.9)
ax.add_patch(Circle((5.45, 0.44), 0.15, fc='white', ec=INK, lw=1.0))
ax.add_patch(Circle((5.45, 0.50), 0.032, fc=INK)); ax.add_patch(Circle((5.39, 0.39), 0.028, fc=INK)); ax.add_patch(Circle((5.51, 0.39), 0.028, fc=INK))
ax.text(5.52, 0.18, 'socket', fontsize=6.3, ha='left')
ax.set_xlim(-0.05, 5.85); ax.set_ylim(0.05, 1.9); ax.axis('off')
```

@opts electric meter | main switch | main fuse | three-pin socket

@mcq 1(h)
Which of the following is an example of metallic mineral?
@opts Gypsum | Haematite | Quartz | Sulphur

@mcq 1(i)
Which of the following elements belong to the same period?

| Element | A | B | C | D |
| --- | --- | --- | --- | --- |
| Atomic no. | 2 | 10 | 5 | 11 |

@opts A, B | B, C | A, C | C, D

@mcq 1(j)
If you want to wash cloth quickly using less soap, which water will you choose?

| Stage | Water source | Option |
| --- | --- | --- |
| While applying soap | Tap water | Option-A |
| While applying soap | Well water | Option-B |
| While rinsing | Tap water | Option-C |
| While rinsing | Well water | Option-D |

@opts A, C | A, D | B, C | B, D

## Section 'B'
<small>Write very short answers to the following questions · [8×1=8]</small>

@q 2
What is the first step in scientific learning? [[1]]

@q 3
Rose is planted by stem cutting. What type of reproduction is this? [[1]]

@q 4
Which method of reproduction in plant do you think is the best for the economic growth of the farmers and why? [[1]]

@q 5
In which condition does a lever multiply force? [[1]]

@q 6
The figure shows the wave produced in a second. Find out the frequency. [[1]]

```figure caption="Question 6: wave produced in 1 second."
import numpy as np
fig, ax = plt.subplots(figsize=(3.8, 1.15))
t = np.linspace(0, 3*2*np.pi, 400)
ax.plot(t, np.sin(t), color=INK, lw=1.5)
ax.annotate('', xy=(3*2*np.pi+0.6, 0), xytext=(-0.2, 0), arrowprops=dict(arrowstyle='->', color=INK, lw=1.0))
ax.text(3*np.pi, 1.25, 'Wave produced in 1 sec', ha='center', fontsize=8)
ax.set_xlim(-0.4, 3*2*np.pi+0.8); ax.set_ylim(-1.3, 1.6); ax.axis('off')
```

@q 7
Why is an atom electrically neutral? [[1]]

@q 8
Define acid. [[1]]

@q 9
Which of the given two solutions will be slippery while touching? [[1]]

| Solution | pH value |
| --- | --- |
| A | 6 |
| B | 8 |

## Section 'C'
<small>Write short answers to the following questions · [8×2=16]</small>

@q 10
Write any two measures that you would follow in lab while testing a sample whether it is acid/base or salt. [[2]]

@q 11
Differentiate virtual reality (VR) and artificial intelligence (AI) in two points. [[2]]

@q 12
Complete the Venn diagram by comparing plant and animal cell (on the basis of cell organelles). [[2]]

```figure caption="Question 12: Venn diagram comparing plant cell and animal cell."
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(3.4, 1.45))
ax.add_patch(Circle((-0.55, 0), 0.85, fc='none', ec=INK, lw=1.4))
ax.add_patch(Circle((0.55, 0), 0.85, fc='none', ec=INK, lw=1.4))
ax.text(-1.55, 0.25, 'Plant cell', fontsize=8.5, fontweight='bold', ha='right')
ax.text(1.55, 0.25, 'Animal cell', fontsize=8.5, fontweight='bold', ha='left')
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-0.95, 0.95); ax.set_aspect('equal'); ax.axis('off')
```

@q 13
Five kingdom system is better than two kingdom system, justify the statement in two points. [[2]]

@q 14
Write any two human activities responsible for degradation of biodiversity. [[2]]

@q 15
Tissue culture is considered as the most advanced method among other methods of vegetative propagation. Clarify with two points. [[2]]

@q 16
In which era did the following organisms evolve? [[2]]

@img 8-sci-2082-q16-organisms.png | Question 16: Fig-A (fish) and Fig-B (dinosaur). | 68

@q 17
Rita is suffering from acidity. What would you suggest her to take for the solution of her problem? How would that chemical cure her problem? [[2]]

## Section 'D'
<small>Write long answers to the following questions · [4×4=16]</small>

@q 18
Mention any four measures that you would follow for your internet security. [[4]]

@q 19
A spherical mirror forms virtual, erect and magnified image of an object. Name the mirror. Draw the ray diagram of the image formation. For what purpose can that mirror be used and why? [[4]]

@q 20
In a house three bulbs rated $100\text{ W}$ each are lit for 3 hours a day and 10 tube lights each of $40\text{ W}$ are lit for 3 hours a day. Find the energy consumed by these loads in a month. Also calculate the cost of the electricity consumed, if rate of electrical energy is Rs. 8 per kWh. [[4]]

@q 21
Name the element having atomic number 8. Also mention its symbol, valency and valence electron. [[4]]

<!-- SOLUTIONS -->

### Section 'A' — Multiple Choice Answer Key

@s 1
Answer key with reasons for Question 1(a) to 1(j): [[10]]

| Q | Key | Option | One-line reason |
| --- | --- | --- | --- |
| 1(a) | **D** | Brutland | The 1987 Brundtland Commission report (*Our Common Future*) defined sustainable development as meeting present needs without compromising future generations. |
| 1(b) | **C** | To prevent seeds from decaying | Moisture promotes fungal/bacterial growth and premature germination, so seeds are kept dry to prevent decay. |
| 1(c) | **C** | Displacement | Displacement is the shortest straight-line distance between two points in a specified direction. |
| 1(d) | **C** | velocity ratio | Velocity ratio ($\text{VR}=d_E/d_L$) depends only on the geometry of the machine, not on friction. |
| 1(e) | **D** | $75\text{ km/h}$ | For two bodies moving towards each other in opposite directions, $v_{\text{rel}} = 60 + 15 = 75\text{ km/h}$. |
| 1(f) | **C** | Option C (Force unchanged, Pressure decreased) | The weight ($F=mg$) is unchanged, while laying the block flat increases contact area $A$, decreasing pressure $P=F/A$. |
| 1(g) | **D** | three-pin socket | In the printed circuit, the three-pin socket has its switch $S_2$ on the neutral line and the live wire routed to the top (earth) pin, making any appliance plugged into it a shock hazard. |
| 1(h) | **B** | Haematite | Haematite ($\mathrm{Fe_2O_3}$) is the chief metallic ore of iron; gypsum, quartz and sulphur are non-metallic minerals. |
| 1(i) | **B** | B, C | Element $B$ ($Z=10$, config $2,8$) and element $C$ ($Z=5$, config $2,3$) both have 2 electron shells, so both belong to Period 2. |
| 1(j) | **A** | A, C | Tap water is soft water, so applying soap in tap water (A) lathers quickly with less soap and rinsing in tap water (C) avoids hard-water scum (note: *B: A, D* if well water is used only for rinsing). |

### Section 'B' — Very Short Answers

@s 2
The first step in scientific learning (scientific method) is **observation** (or identifying a problem through curiosity and observation). [[1]]

@s 3
Planting rose by stem cutting is **artificial vegetative propagation** (a form of asexual reproduction through stem cutting). [[1]]

@s 4
**Vegetative propagation** (such as tissue culture or grafting) is the best method for the economic growth of farmers because plants raised by this method bear flowers and fruits much earlier than seed-grown plants and retain the exact high-yielding qualities of the parent plant. [[1]]

@s 5
A lever multiplies force when the **effort distance (effort arm) is greater than the load distance (load arm)** ($\text{ED} > \text{LD}$, so mechanical advantage $\text{MA} > 1$). [[1]]

@s 6
From the wave diagram, **3 complete waves** (3 crests and 3 troughs) are produced in $1\text{ second}$. Since frequency ($f$) is the number of complete waves produced per second ($n / t$), we get $f = 3 / 1\text{ s}$, which gives **$3\text{ Hz}$**. [[1]]

@s 7
An atom is electrically neutral because it contains an **equal number of positively charged protons ($p^+$) in its nucleus and negatively charged electrons ($e^-$) revolving in its shells**, so their opposite charges cancel each other out. [[1]]

@s 8
An **acid** is a chemical compound that dissociates in aqueous solution to produce hydrogen ions ($\mathrm{H^+}$) (or hydronium ions, $\mathrm{H_3O^+}$) and turns blue litmus paper red. [[1]]

@s 9
**Solution B** (with $\text{pH} = 8$) will feel slippery while touching because a solution with $\text{pH} > 7$ is basic (alkaline), and bases are soapy/slippery to touch, whereas Solution A ($\text{pH} = 6$) is weakly acidic. [[1]]

### Section 'C' — Short Answers

@s 10
Any two laboratory safety measures to follow while testing whether a sample is an acid, base or salt: [[2]]
1. **Never taste or touch chemicals directly** with bare hands; always use a dropper or test-tube holder and wear safety goggles and a lab coat.
2. **Use small quantities of the sample** in a clean test tube and test it with indicators (litmus paper, methyl orange or phenolphthalein) rather than pouring concentrated reagents directly.

<div style="break-before:page"></div>

@s 11
Two differences between Virtual Reality (VR) and Artificial Intelligence (AI): [[2]]

| S.N. | Virtual Reality (VR) | Artificial Intelligence (AI) |
| --- | --- | --- |
| 1. | VR is a computer-generated 3D simulated environment that a user can experience and interact with using a headset and sensors. | AI is the branch of computer science that enables machines and software to think, learn from data, reason and make decisions like humans. |
| 2. | Its primary goal is **immersive simulation** (used in 3D training simulators, virtual tours and gaming). | Its primary goal is **intelligent automation and problem-solving** (used in voice assistants, medical diagnosis and self-driving cars). |

@s 12
Completed Venn diagram comparing a **plant cell** and an **animal cell** on the basis of cell organelles: [[2]]

```figure caption="Solution 12: Venn diagram of plant cell vs. animal cell organelles."
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.0, 2.25))
ax.add_patch(Circle((-0.95, 0), 1.35, fc=ACCENT, alpha=0.10, ec=INK, lw=1.4))
ax.add_patch(Circle((0.95, 0), 1.35, fc=ACCENT, alpha=0.10, ec=INK, lw=1.4))
ax.text(-1.45, 1.48, 'Plant cell only', fontsize=8.5, fontweight='bold', ha='center', color=INK)
ax.text(0.0, 1.48, 'Both cells', fontsize=8.5, fontweight='bold', ha='center', color=ACCENT)
ax.text(1.45, 1.48, 'Animal cell only', fontsize=8.5, fontweight='bold', ha='center', color=INK)
ax.text(-1.52, 0.0, '• Cell wall\n• Plastids\n  (chloroplast)\n• Large central\n  vacuole', fontsize=7.5, va='center', ha='center')
ax.text(0.0, 0.0, '• Nucleus\n• Cell membrane\n• Mitochondria\n• Cytoplasm\n• Ribosomes', fontsize=7.2, va='center', ha='center')
ax.text(1.52, 0.0, '• Centrosome\n  (centrioles)\n• Small temporary\n  vacuoles\n• Lysosomes', fontsize=7.5, va='center', ha='center')
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-1.45, 1.72); ax.set_aspect('equal'); ax.axis('off')
```

@s 13
The five-kingdom classification system (proposed by R. H. Whittaker) is better than the two-kingdom system for the following two reasons: [[2]]
1. **Separation of prokaryotes and eukaryotes:** It places unicellular prokaryotic organisms (bacteria and cyanobacteria) into a separate kingdom **Monera**, whereas the two-kingdom system grouped them together with eukaryotic plants.
2. **Distinct placement of fungi and unicellular eukaryotes:** Non-photosynthetic saprophytic **Fungi** (which have chitinous cell walls and heterotrophic nutrition) are separated from green plants, and unicellular eukaryotes are placed in **Protista**, making classification evolutionary and scientifically accurate.

@s 14
Any two human activities responsible for the degradation of biodiversity: [[2]]
1. **Deforestation and habitat destruction:** Clearing forests for agriculture, settlement, roads and timber destroys the natural habitats and food chains of wild flora and fauna.
2. **Environmental pollution and over-exploitation:** Industrial effluents, plastic and chemical pesticides pollute soil and water bodies, while poaching, overfishing and illegal trade push species towards extinction.

@s 15
Tissue culture (micropropagation) is considered the most advanced method of vegetative propagation for the following two reasons: [[2]]
1. **Rapid mass production in a small space:** Thousands of genetically identical plantlets (clones) can be grown in a short time from a tiny tissue sample (explant) in a nutrient medium regardless of the season.
2. **Production of disease-free plants:** By culturing meristematic tissues under sterile laboratory conditions, completely virus-free and disease-free healthy plantlets of rare or commercially valuable species (such as orchids, banana and potato) are obtained.

@s 16
Geological eras in which the given organisms evolved: [[2]]
- **Fig-A (Early fish):** Evolved in the **Palaeozoic Era**.
- **Fig-B (Dinosaur):** Evolved and dominated in the **Mesozoic Era**.

@s 17
Rita is suffering from stomach acidity caused by excess hydrochloric acid ($\mathrm{HCl}$) in the gastric juice. [[2]]
- **Suggested chemical:** I would suggest her to take an **antacid** containing a mild edible base such as **magnesium hydroxide** ($\mathrm{Mg(OH)_2}$, *milk of magnesia*) or **sodium bicarbonate** ($\mathrm{NaHCO_3}$).
- **How it cures acidity:** The mild base in the antacid undergoes a **neutralization reaction** with the excess hydrochloric acid in the stomach to form a neutral salt and water ($\mathrm{Mg(OH)_2 + 2HCl \rightarrow MgCl_2 + 2H_2O}$), reducing stomach acidity and relieving the burning sensation.

### Section 'D' — Long Answers

@s 18
Any four measures to follow for personal internet security (cyber safety): [[4]]
1. **Use strong passwords and two-factor authentication (2FA):** Create unique passwords combining uppercase and lowercase letters, numbers and symbols, and enable two-factor authentication on email and social accounts.
2. **Avoid clicking suspicious links and phishing emails:** Do not open unknown email attachments, pop-up links or messages asking for OTPs, bank PINs or personal credentials.
3. **Keep operating systems, browsers and antivirus updated:** Regularly install security patches and use reliable antivirus/firewall software to block malware, spyware and ransomware.
4. **Practice safe browsing and privacy control:** Use secure websites (`https://`), avoid logging into sensitive accounts on public Wi-Fi networks, and restrict personal information shared publicly on social media.

@s 19
A spherical mirror that forms a **virtual, erect and magnified** image of an object is a **concave mirror** (when the object is placed between its pole $P$ and principal focus $F$). [[4]]

```figure caption="Solution 19: ray diagram of a concave mirror forming a virtual, erect and magnified image."
import numpy as np
fig, ax = plt.subplots(figsize=(4.6, 2.2))
# Principal axis
ax.plot([-3.4, 2.2], [0, 0], color=INK, lw=1.0)
# Concave mirror arc at x=0 (curving left at top/bottom)
th = np.linspace(-0.48, 0.48, 100)
R = 2.8
mx = R * (np.cos(th) - 1)
my = R * np.sin(th)
ax.plot(mx, my, color=INK, lw=2.0)
for t in np.linspace(-0.45, 0.45, 13):
    x0, y0 = R*(np.cos(t)-1), R*np.sin(t)
    ax.plot([x0, x0+0.12], [y0, y0+0.06], color=INK, lw=0.7)
# Points C, F, P
C, F, P = -2.4, -1.2, 0.0
for x, lbl in [(C, 'C'), (F, 'F'), (P, 'P')]:
    ax.plot(x, 0, 'o', color=INK, ms=3.5)
    ax.text(x, -0.22, lbl, fontsize=8, fontweight='bold', ha='center')
# Object AB at x = -0.65, height = 0.52
ox, oh = -0.65, 0.52
ax.annotate('', xy=(ox, oh), xytext=(ox, 0), arrowprops=dict(arrowstyle='->', color=INK, lw=1.5))
ax.text(ox, oh+0.08, 'A', fontsize=8, fontweight='bold', ha='center')
ax.text(ox, -0.22, 'B', fontsize=8, fontweight='bold', ha='center')
# Ray 1: parallel to axis from A(-0.65, 0.52) to mirror M(0, 0.52), reflects through F(-1.2, 0)
ax.plot([ox, 0], [oh, oh], color=ACCENT, lw=1.2)
ax.annotate('', xy=(-0.25, oh), xytext=(-0.5, oh), arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.1))
# Reflected line passes through (0, oh) and (-1.2, 0): slope = oh / 1.2
m1 = oh / 1.2
ax.plot([-2.8, 0], [oh + m1*(-2.8), oh], color=ACCENT, lw=1.2)
ax.annotate('', xy=(-1.8, oh + m1*(-1.8)), xytext=(-0.6, oh + m1*(-0.6)), arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.1))
# Virtual extension behind mirror to x = 1.48
ix = 1.48
iy = oh + m1 * ix
ax.plot([0, ix], [oh, iy], color=ACCENT, lw=1.0, ls='--')
# Ray 2: from C(-2.4, 0) through A(-0.65, 0.52) to mirror, reflects back along itself
m2 = oh / (ox - C)
ym2 = m2 * (0 - C)
ax.plot([C, 0], [0, ym2], color=INK, lw=1.1)
ax.plot([0, ix], [ym2, iy], color=INK, lw=1.0, ls='--')
# Virtual image A'B' at x = ix
ax.annotate('', xy=(ix, iy), xytext=(ix, 0), arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5, ls='--'))
ax.text(ix, iy+0.08, "A'", fontsize=8, fontweight='bold', ha='center', color=ACCENT)
ax.text(ix, -0.22, "B'", fontsize=8, fontweight='bold', ha='center', color=ACCENT)
ax.set_xlim(-3.2, 2.0); ax.set_ylim(-1.35, 1.45); ax.set_aspect('equal'); ax.axis('off')
```

- **Name of the mirror:** **Concave mirror** *(1 mark)*
- **Ray diagram:** Shown above with object $AB$ placed between the pole ($P$) and focus ($F$), forming a virtual, erect and magnified image $A'B'$ behind the mirror. *(1 mark)*
- **Purpose and reason:** It is used as a **shaving mirror (or make-up mirror) and as a dentist's mirror**. When the face or tooth is held within the focal length of the concave mirror, it produces an upright (erect) and enlarged (magnified) image, allowing fine details to be seen clearly. *(2 marks)*

@s 20
Given electrical loads and daily usage: [[4]]
- **Three electric bulbs ($100\text{ W}$ each, $3\text{ hours/day}$):**
  Total power $P_1 = 3 \times 100\text{ W}$, which is $300\text{ W}$ or $0.3\text{ kW}$.
  Daily energy consumed by bulbs: $E_1 = 0.3\text{ kW} \times 3\text{ h}$, which gives **$0.9\text{ kWh/day}$**.
- **Ten tube lights ($40\text{ W}$ each, $3\text{ hours/day}$):**
  Total power $P_2 = 10 \times 40\text{ W}$, which is $400\text{ W}$ or $0.4\text{ kW}$.
  Daily energy consumed by tube lights: $E_2 = 0.4\text{ kW} \times 3\text{ h}$, which gives **$1.2\text{ kWh/day}$**.
- **Total energy consumed in $1\text{ month}$ ($30\text{ days}$):**
  Total daily energy is $E_1 + E_2 = 0.9 + 1.2$, which equals **$2.1\text{ kWh/day}$**.
  $$E_{\text{month}} = 2.1\text{ kWh/day} \times 30\text{ days}$$
  $$E_{\text{month}} = 63\text{ kWh (or 63 units)}$$
- **Total electricity cost at Rs. $8$ per kWh:**
  $$\text{Total cost} = 63 \times \text{Rs. } 8$$
  $$\text{Total cost} = \text{Rs. } 504$$
Therefore, the energy consumed in a month is **$63\text{ kWh}$** and the total cost of electricity is **Rs. $504$**.

@s 21
For the element having **atomic number ($Z$) $= 8$**: [[4]]
- **Name of the element:** **Oxygen** *(1 mark)*
- **Chemical symbol:** **$\mathrm{O}$** *(1 mark)*
- **Electronic configuration:** $\text{K} = 2,\ \text{L} = 6$ (or $1s^2\,2s^2\,2p^4$)
- **Number of valence electrons:** **$6$** *(since there are $6$ electrons in its outermost L-shell)* *(1 mark)*
- **Valency:** **$2$** *(since an oxygen atom requires $8 - 6 = 2$ more electrons to complete its octet)* *(1 mark)*

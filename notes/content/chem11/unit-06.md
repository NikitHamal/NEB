---
subject: Chemistry
grade: 11
unit: 6
title: Oxidation and Reduction
hours: 5
area: General and Physical Chemistry
---

Rusting iron, a burning candle, the battery in a torch, the dry cell in a phone,
photosynthesis in a leaf and the refining of copper at Bhaktapur are all the same
reaction type: electrons move from one species to another. This unit gives you the
bookkeeping — oxidation numbers — that turns that idea into a method, then applies
it twice: to balancing equations that look impossible, and to electrolysis, where
we pay for the electrons ourselves.

::: key What this unit really is
One idea (electrons move), one tool (oxidation number), two skills (balance a
redox equation by two different methods, and calculate a mass from a current).
Marks in the NEB paper come almost entirely from the two skills.
:::

## 6.1 General and electronic concept of oxidation and reduction

The old, **classical** definitions came from the laboratory bench:

| | Oxidation | Reduction |
|---|---|---|
| Oxygen | addition of oxygen: 2Mg + O₂ → 2MgO | removal of oxygen: CuO + H₂ → Cu + H₂O |
| Hydrogen | removal of hydrogen: H₂S + Cl₂ → 2HCl + S | addition of hydrogen: N₂ + 3H₂ → 2NH₃ |
| Electronegative element | addition: Fe + S → FeS | removal: 2FeCl₃ + H₂ → 2FeCl₂ + 2HCl |
| Electropositive element | removal: 2KI + H₂O₂ → 2KOH + I₂ | addition: HgCl₂ + Hg → Hg₂Cl₂ |

These four rules agree with one another but cover only reactions that happen to
contain oxygen or hydrogen. The **electronic concept** replaces all four:

::: definition Electronic concept
**Oxidation** is the **loss** of electrons; **reduction** is the **gain** of
electrons. Remember it as **OIL RIG** — Oxidation Is Loss, Reduction Is Gain.
:::

The species that takes electrons is the **oxidising agent** (and is itself
reduced); the species that gives them up is the **reducing agent** (and is itself
oxidised). Because electrons cannot float about free, the two processes always
happen together, in exactly matching numbers — which is why the reaction is called
a **redox** reaction.

```figure caption="Electron transfer in Zn + Cu²⁺ → Zn²⁺ + Cu. Zinc loses two electrons and copper(II) gains them; neither half reaction can occur alone."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.2, 2.8))
RED, GRN = SERIES[1], SERIES[2]

terms = [(0.55, 'Zn(s)', '0', RED), (1.72, '+', None, None),
         (2.95, 'Cu$^{2+}$(aq)', '+2', GRN), (4.20, '→', None, None),
         (5.45, 'Zn$^{2+}$(aq)', '+2', RED), (6.62, '+', None, None),
         (7.70, 'Cu(s)', '0', GRN)]
for x, t, ox, c in terms:
    ax.text(x, 1.40, t, ha='center', va='center', fontsize=10.0, color=INK)
    if ox is not None:
        ax.text(x, 1.00, ox, ha='center', va='center', fontsize=7.8, color=c)

ax.text(-0.30, 1.00, 'ox. no.', ha='left', va='center', fontsize=7.0, color=MUTED)

ax.annotate('', xy=(2.80, 1.92), xytext=(0.62, 1.92),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3,
                            mutation_scale=10,
                            connectionstyle='arc3,rad=-0.34'))
ax.text(1.70, 2.62, 'two electrons transferred', ha='center', va='bottom',
        fontsize=7.4, color=ACCENT)

def box(y, head, eq, tail, c):
    ax.add_patch(FancyBboxPatch((0.18, y - 0.30), 7.74, 0.60,
                                boxstyle='round,pad=0.05,rounding_size=0.10',
                                facecolor='white', edgecolor=c, lw=1.0))
    ax.text(0.38, y + 0.10, head, ha='left', va='center', fontsize=7.6, color=c)
    ax.text(0.38, y - 0.14, eq, ha='left', va='center', fontsize=8.6, color=INK)
    ax.text(7.74, y - 0.02, tail, ha='right', va='center', fontsize=7.2, color=MUTED)

box(0.20, 'OXIDATION  — loss of electrons, ox. no. rises',
    'Zn → Zn$^{2+}$ + 2e$^{-}$',
    'Zn is the reducing agent\n(it is itself oxidised)', RED)
box(-0.86, 'REDUCTION  — gain of electrons, ox. no. falls',
    'Cu$^{2+}$ + 2e$^{-}$ → Cu',
    'Cu$^{2+}$ is the oxidising agent\n(it is itself reduced)', GRN)

ax.text(4.05, -1.44, 'the two half reactions always occur together, and the '
        'electrons lost equal the electrons gained',
        ha='center', va='top', fontsize=7.0, color=MUTED)

ax.set_xlim(-0.36, 8.10)
ax.set_ylim(-1.78, 2.98)
ax.axis('off')
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.02)
```

A species can even oxidise and reduce itself. In **disproportionation** the same
element in a single substance is simultaneously oxidised and reduced:

Cl₂ + 2NaOH → NaCl + NaOCl + H₂O

Here chlorine goes from 0 to −1 (in NaCl) and from 0 to +1 (in NaOCl).

## 6.2 Oxidation number and rules for assigning oxidation number

::: definition Oxidation number
The **oxidation number** (oxidation state) of an atom in a compound is the charge
it *would* carry if every bond in the compound were assumed to be completely
ionic, with each shared pair given entirely to the more electronegative atom.
:::

It is a bookkeeping device, not a real charge — carbon in CH₄ is not really 4−.
The rules, applied in this order, settle every case you will meet:

| # | Rule | Example |
|---|---|---|
| 1 | Every atom in a free element is **0** | Na, O₂, P₄, S₈, Cl₂ |
| 2 | A monatomic ion has the oxidation number of its charge | Na⁺ = +1, S²⁻ = −2, Al³⁺ = +3 |
| 3 | Group 1 metals are +1, group 2 metals +2, aluminium +3 | NaCl, CaO, AlCl₃ |
| 4 | **Hydrogen is +1**, except −1 in metal hydrides | HCl (+1) but NaH, CaH₂ (−1) |
| 5 | **Oxygen is −2**, except −1 in peroxides, −½ in superoxides, +2 in OF₂ | H₂O (−2), H₂O₂ (−1), KO₂ (−½) |
| 6 | Fluorine is always −1; other halogens are −1 except with oxygen or a more electronegative halogen | HCl (−1) but HClO₄ (+7) |
| 7 | The sum over a neutral molecule is **0** | H₂SO₄: 2(+1) + x + 4(−2) = 0 |
| 8 | The sum over a polyatomic ion equals the **charge on the ion** | Cr₂O₇²⁻: 2x + 7(−2) = −2 |

Oxidation number may be **fractional**, because it is an average over atoms that
are not all equivalent.

```figure caption="Oxidation numbers of nitrogen from −3 to +5. Moving right along the line is oxidation, moving left is reduction; the size of the step is the number of electrons per atom."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle

fig, ax = plt.subplots(figsize=(5.2, 2.6))
lo, hi = -3, 5
ax.annotate('', xy=(hi + 0.55, 0), xytext=(lo - 0.55, 0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=10))
for n in range(lo, hi + 1):
    ax.plot([n, n], [-0.09, 0.09], color=INK, lw=1.0)
    lab = '0' if n == 0 else (('+%d' % n) if n > 0 else ('\u2212%d' % -n))
    ax.text(n, -0.22, lab, ha='center', va='top', fontsize=7.6, color=INK)

species = [(-3, 'NH$_3$'), (-2, 'N$_2$H$_4$'), (-1, 'NH$_2$OH'), (0, 'N$_2$'),
           (1, 'N$_2$O'), (2, 'NO'), (3, 'HNO$_2$'), (4, 'NO$_2$'), (5, 'HNO$_3$')]
for n, s in species:
    ax.scatter([n], [0], s=34, color=ACCENT, zorder=4, linewidths=0)
    ax.text(n, 0.24, s, ha='center', va='bottom', fontsize=7.4, color=INK,
            rotation=38, rotation_mode='anchor')

ax.annotate('', xy=(4.55, -0.86), xytext=(0.45, -0.86),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.2, mutation_scale=9))
ax.text(2.5, -0.98, 'oxidation: oxidation number increases, electrons lost',
        ha='center', va='top', fontsize=7.0, color=SERIES[1])
ax.annotate('', xy=(-2.55, -1.52), xytext=(-0.45, -1.52),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.2, mutation_scale=9))
ax.text(-1.5, -1.64, 'reduction: gain of electrons',
        ha='center', va='top', fontsize=7.0, color=SERIES[2])
ax.text(lo - 0.95, 1.28, 'oxidation number of nitrogen', ha='left', va='top',
        fontsize=7.8, color=MUTED)

ax.set_xlim(lo - 0.95, hi + 0.95)
ax.set_ylim(-2.05, 1.35)
ax.axis('off')
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.02)
```

::: example Worked example 6.1 — assigning oxidation numbers
**Problem.** Find the oxidation number of the bold atom in (a) **Cr** in K₂Cr₂O₇,
(b) **S** in Na₂S₂O₃, (c) **Fe** in Fe₃O₄, (d) **C** in C₆H₁₂O₆.

**Solution.** (a) K is +1 and O is −2, and the molecule is neutral:

$$ 2(+1) + 2x + 7(-2) = 0 \;\Rightarrow\; 2x = 12 \;\Rightarrow\; x = +6 $$

(b) $2(+1) + 2x + 3(-2) = 0 \Rightarrow 2x = +4 \Rightarrow x = +2$.

(c) $3x + 4(-2) = 0 \Rightarrow x = +8/3$. The fraction is real: Fe₃O₄ is
FeO·Fe₂O₃, containing one Fe²⁺ and two Fe³⁺, and $(2+3+3)/3 = 8/3$.

(d) $6x + 12(+1) + 6(-2) = 0 \Rightarrow 6x = 0 \Rightarrow x = 0$. Glucose is a
reminder that an oxidation number of zero does not mean an uncombined element.
:::

::: caution Oxidation number is not valency
The valency of carbon is 4 in every one of CH₄, CH₃OH, HCHO, HCOOH and CO₂, but
its oxidation number runs −4, −2, 0, +2, +4. Valency counts bonds and is never
negative or fractional; oxidation number counts notional charge and can be both.
:::

## 6.3 Balancing redox reactions by oxidation number and ion-electron methods

**Oxidation number method** — follow the atoms whose oxidation number changes:

1. Assign oxidation numbers and find which atoms are oxidised and which reduced.
2. Compute the **total** increase and the **total** decrease per formula unit.
3. Multiply the two species by whatever factors make increase = decrease.
4. Balance the remaining atoms by inspection: other elements first, then H, then
   O (add H₂O), checking charge at the end.

**Ion-electron (half reaction) method** — split the reaction into two ion
equations:

1. Write the skeletal ionic equation and split it into an oxidation half and a
   reduction half.
2. Balance all atoms except H and O in each half.
3. Balance O by adding H₂O, then H by adding H⁺.
4. **In basic medium only**: add to both sides as many OH⁻ as there are H⁺, and
   combine H⁺ + OH⁻ into H₂O.
5. Balance charge by adding electrons to the more positive side.
6. Multiply the halves so the electrons cancel, then add them.

::: example Worked example 6.2 — oxidation number method
**Problem.** Balance Cu + HNO₃ → Cu(NO₃)₂ + NO + H₂O.

**Solution.** Oxidation numbers: Cu goes 0 → +2, an **increase of 2**. Nitrogen
goes +5 in HNO₃ → +2 in NO, a **decrease of 3**. (The nitrogen in Cu(NO₃)₂ is
still +5, so it is a spectator.)

To equalise, take 3 Cu (total increase 6) and 2 N reduced (total decrease 6):

3Cu + HNO₃ → 3Cu(NO₃)₂ + 2NO + H₂O

Nitrogen: 6 atoms are needed for the nitrate and 2 more are reduced, so 8 HNO₃:

3Cu + 8HNO₃ → 3Cu(NO₃)₂ + 2NO + 4H₂O

**Check.** Cu 3 = 3; N 8 = 6 + 2; H 8 = 8; O 24 = 18 + 2 + 4. Charge is 0 on both
sides. Balanced.
:::

::: example Worked example 6.3 — the same reaction, both ways
**Problem.** Balance, in acidic medium, Cr₂O₇²⁻ + I⁻ → Cr³⁺ + I₂ by (a) the
oxidation number method and (b) the ion-electron method.

**(a) Oxidation number method.** Cr is +6 in Cr₂O₇²⁻ and +3 in Cr³⁺: a decrease of
3 per Cr, so **6 per dichromate ion**. Iodine goes −1 → 0: an increase of 1 per
atom, so **2 per I₂**. Equalising, one Cr₂O₇²⁻ needs 3 I₂, i.e. 6 I⁻:

Cr₂O₇²⁻ + 6I⁻ → 2Cr³⁺ + 3I₂

Balance the 7 oxygens with 7 H₂O on the right and therefore 14 H⁺ on the left:

Cr₂O₇²⁻ + 6I⁻ + 14H⁺ → 2Cr³⁺ + 3I₂ + 7H₂O

**(b) Ion-electron method.** Reduction half — balance Cr, then O with water, then
H with H⁺, then charge with electrons:

Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O  (charge: −2 + 14 − 6 = +6 = 2 × +3)

Oxidation half:

2I⁻ → I₂ + 2e⁻  (charge: −2 = −2)

Multiply the oxidation half by 3 so that 6 electrons cancel, then add:

Cr₂O₇²⁻ + 6I⁻ + 14H⁺ → 2Cr³⁺ + 3I₂ + 7H₂O

**Check.** Cr 2 = 2; I 6 = 6; H 14 = 14; O 7 = 7. Charge: (−2) + (−6) + (+14) =
**+6** on the left and 2(+3) = **+6** on the right. Both methods agree.
:::

::: example Worked example 6.4 — ion-electron method in basic medium
**Problem.** Balance MnO₄⁻ + I⁻ → MnO₂ + I₂ in alkaline solution.

**Solution.** Reduction half, first in acid:

MnO₄⁻ + 4H⁺ + 3e⁻ → MnO₂ + 2H₂O

Add 4 OH⁻ to each side to remove the H⁺, since the medium is basic:

MnO₄⁻ + 4H₂O + 3e⁻ → MnO₂ + 2H₂O + 4OH⁻,  i.e.  MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻

Charge: −1 − 3 = −4 on the left and −4 on the right. Oxidation half:
2I⁻ → I₂ + 2e⁻. The LCM of 3 and 2 is 6, so multiply the halves by 2 and 3:

2MnO₄⁻ + 4H₂O + 6e⁻ → 2MnO₂ + 8OH⁻
6I⁻ → 3I₂ + 6e⁻

Adding,

2MnO₄⁻ + 6I⁻ + 4H₂O → 2MnO₂ + 3I₂ + 8OH⁻

**Check.** Mn 2 = 2; I 6 = 6; H 8 = 8; O (8 + 4) = 12 = (4 + 8). Charge:
(−2) + (−6) = **−8** on the left, 8(−1) = **−8** on the right. Balanced.
:::

::: tip Two habits that save marks
Always finish with the **charge check**, not just the atom check — an equation can
have every atom balanced and still be wrong. And in the ion-electron method, never
add H⁺ to an alkaline solution and leave it there: neutralise it with OH⁻ in
step 4.
:::

## 6.4 Electrolysis: qualitative and quantitative aspects

### Qualitative aspect

::: definition Electrolysis
The decomposition of an electrolyte, in the molten state or in aqueous solution,
by the passage of direct current through it.
:::

An **electrolyte** conducts by the movement of ions. The electrode joined to the
positive terminal is the **anode**, where **anions** give up electrons and are
**oxidised**; the electrode joined to the negative terminal is the **cathode**,
where **cations** accept electrons and are **reduced**. (In electrolysis the
cathode is negative — the opposite of a galvanic cell.)

```figure caption="Electrolysis of molten sodium chloride. Cations travel to the cathode and are reduced, anions travel to the anode and are oxidised; the external circuit carries electrons, the electrolyte carries ions."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

fig, ax = plt.subplots(figsize=(5.0, 3.2))
RED, GRN = SERIES[1], SERIES[2]

ax.add_patch(Rectangle((0.55, 0.30), 5.90, 3.05, facecolor='#eef4fa',
                       edgecolor=MUTED, lw=1.2, zorder=1))
ax.plot([0.55, 0.55, 6.45, 6.45], [4.05, 0.30, 0.30, 4.05],
        color=INK, lw=1.6, zorder=3)
ax.plot([0.55, 6.45], [3.35, 3.35], color=ACCENT, lw=1.0, zorder=2)

for x, lbl, sign, c in ((1.85, 'CATHODE', '−', GRN), (5.15, 'ANODE', '+', RED)):
    ax.add_patch(Rectangle((x - 0.22, 0.75), 0.44, 4.05, facecolor='#d7dbe2',
                           edgecolor=INK, lw=1.0, zorder=4))
    ax.text(x + 0.40, 4.62, sign, ha='center', va='center', fontsize=12, color=c, zorder=6)
    ax.text(x, 0.66, lbl, ha='center', va='top', fontsize=7.2, color=c, zorder=6)

ax.plot([1.85, 1.85, 5.15, 5.15], [4.80, 5.62, 5.62, 4.80], color=INK, lw=1.3)
for dx, h in ((-0.10, 0.30), (0.10, 0.16), (0.30, 0.30), (0.50, 0.16)):
    ax.plot([3.50 + dx, 3.50 + dx], [5.62 - h, 5.62 + h], color=INK, lw=1.5)
ax.text(3.70, 6.10, 'd.c. source', ha='center', va='bottom', fontsize=7.6, color=INK)

ax.annotate('', xy=(2.55, 5.62), xytext=(3.30, 5.62),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1, mutation_scale=9))
ax.text(2.92, 5.48, 'e$^{-}$', ha='center', va='top', fontsize=7.4, color=ACCENT)
ax.annotate('', xy=(4.45, 5.62), xytext=(5.15, 5.62),
            arrowprops=dict(arrowstyle='<|-', color=ACCENT, lw=1.1, mutation_scale=9))
ax.text(4.80, 5.48, 'e$^{-}$', ha='center', va='top', fontsize=7.4, color=ACCENT)

ax.annotate('', xy=(2.32, 2.12), xytext=(4.68, 2.12),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.2, mutation_scale=9))
ax.text(3.50, 2.24, 'Na$^{+}$ → cathode', ha='center', va='bottom',
        fontsize=7.2, color=GRN)
ax.annotate('', xy=(4.68, 1.16), xytext=(2.32, 1.16),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.2, mutation_scale=9))
ax.text(3.50, 1.04, 'Cl$^{-}$ → anode', ha='center', va='top',
        fontsize=7.2, color=RED)

ax.text(3.50, 3.02, 'molten NaCl', ha='center', va='center', fontsize=8.0, color=ACCENT)
ax.text(3.50, 2.74, '(the electrolyte)', ha='center', va='center', fontsize=7.0, color=ACCENT)

def half(x, y, head, eq, c, ha):
    ax.text(x, y, head, ha=ha, va='bottom', fontsize=6.9, color=c)
    ax.text(x, y - 0.44, eq, ha=ha, va='bottom', fontsize=8.2, color=INK)

half(0.15, -0.95, 'cathode (reduction)',
     'Na$^{+}$ + e$^{-}$ → Na', GRN, 'left')
half(6.85, -0.95, 'anode (oxidation)',
     '2Cl$^{-}$ → Cl$_2$ + 2e$^{-}$', RED, 'right')

ax.set_xlim(0.02, 7.00)
ax.set_ylim(-1.55, 6.55)
ax.set_aspect('equal')
ax.axis('off')
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
```

When more than one kind of ion is present, the one discharged is the one needing
the least energy — the rule of **preferential discharge**:

| | Discharged with most difficulty → most easily |
|---|---|
| Cations | K⁺ < Na⁺ < Ca²⁺ < Mg²⁺ < Al³⁺ < Zn²⁺ < Fe²⁺ < H⁺ < Cu²⁺ < Ag⁺ |
| Anions | SO₄²⁻ < NO₃⁻ < OH⁻ < Cl⁻ < Br⁻ < I⁻ |

This explains three standard cases:

- **Molten NaCl**: Na at the cathode, Cl₂ at the anode (the Down's process).
- **Aqueous NaCl**: H⁺ from water beats Na⁺, so H₂ is released at the cathode
  while Cl₂ comes off at the anode and NaOH is left in solution — the chlor-alkali
  industry.
- **Aqueous CuSO₄ with platinum electrodes**: Cu at the cathode, O₂ at the anode
  (since SO₄²⁻ is very hard to discharge).

Electrolysis is used for **electroplating**, the **electrorefining** of copper,
the extraction of reactive metals (Na, Mg, Al by the Hall–Héroult process) and the
manufacture of NaOH, Cl₂ and H₂.

### Quantitative aspect — Faraday's laws

**First law.** The mass of a substance deposited or liberated at an electrode is
directly proportional to the quantity of electricity passed:

$$ m \propto Q \quad\Rightarrow\quad m = ZQ = Zit $$

where $Z$ is the **electrochemical equivalent** — the mass deposited by one
coulomb.

**Second law.** When the same quantity of electricity is passed through different
electrolytes, the masses deposited are proportional to their **chemical equivalent
masses** $E$:

$$ \frac{m_1}{m_2} = \frac{E_1}{E_2}, \qquad E = \frac{\text{atomic mass}}{\text{valency}} $$

One **faraday**, $1\,F = 96500$ C, is the charge on one mole of electrons
($N_A e = 6.022\times10^{23} \times 1.602\times10^{-19}$ C), and it deposits
exactly one equivalent of any substance. Combining the two laws,

$$ Z = \frac{E}{96500} \qquad\text{so}\qquad m = \frac{E\,i\,t}{96500} $$

```figure caption="Faraday's two laws. Left: mass is a straight line through the origin against charge, with slope Z = E/F. Right: one faraday always deposits one equivalent, so the mass depends on E = atomic mass / valency."
import numpy as np, matplotlib.pyplot as plt

F = 96500.0
sp = [('Ag  (E = 108)', 107.87, 1), ('Cu  (E = 31.8)', 63.55, 2),
      ('Al  (E = 9.0)', 26.98, 3)]

fig = plt.figure(figsize=(5.2, 2.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.18, 1.0], wspace=0.34,
                      left=0.10, right=0.98, top=0.88, bottom=0.18)
ax = fig.add_subplot(gs[0, 0])
Q = np.linspace(0, 3000, 200)
for i, (name, M, n) in enumerate(sp):
    E = M / n
    ax.plot(Q, E * Q / F, color=SERIES[i], lw=1.4, label=name)
ax.set_xlabel('charge passed  Q / C')
ax.set_ylabel('mass deposited / g')
ax.set_title("first law:  m = ZQ", fontsize=8.6, pad=3)
ax.set_xlim(0, 3000); ax.set_ylim(0, 3.6)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=.40)
ax.legend(fontsize=6.4, loc='upper left', handlelength=1.3)

bx = fig.add_subplot(gs[0, 1])
labs = ['Ag$^{+}$', 'Cu$^{2+}$', 'Al$^{3+}$']
vals = [M / n for _, M, n in sp]
bars = bx.bar(labs, vals, color=[SERIES[i] for i in range(3)], width=0.62)
for b, v in zip(bars, vals):
    bx.text(b.get_x() + b.get_width() / 2, v + 2.5, '%.1f' % v,
            ha='center', va='bottom', fontsize=6.8, color=INK)
bx.set_ylabel('mass deposited by 1 F / g')
bx.set_title('second law:  m ∝ eq. mass', fontsize=8.4, pad=3)
bx.set_ylim(0, 126)
bx.spines[['top', 'right']].set_visible(False)
bx.grid(True, axis='y', alpha=.40)
bx.tick_params(axis='x', labelsize=7.4)
```

::: example Worked example 6.5 — Faraday numerical
**Problem.** A current of 1.5 A is passed for 30 minutes through solutions of
AgNO₃ and CuSO₄ connected **in series**. Calculate the mass of silver and of
copper deposited. (Ag = 108, Cu = 63.5, 1 F = 96500 C)

**Solution.** The same charge passes through both cells:

$$ Q = it = 1.5 \times (30 \times 60) = 2700\ \text{C} $$

For silver, Ag⁺ + e⁻ → Ag, so the valency is 1 and $E = 108/1 = 108$:

$$ m_{Ag} = \frac{E\,Q}{96500} = \frac{108 \times 2700}{96500} = 3.02\ \text{g} $$

For copper, Cu²⁺ + 2e⁻ → Cu, so $E = 63.5/2 = 31.75$:

$$ m_{Cu} = \frac{31.75 \times 2700}{96500} = 0.888\ \text{g} $$

**Check with the second law**: $m_{Ag}/m_{Cu} = 3.02/0.888 = 3.40$, and
$E_{Ag}/E_{Cu} = 108/31.75 = 3.40$. The two agree.
:::

## Chapter summary

- Classically, oxidation is addition of oxygen or removal of hydrogen; electronically
  it is **loss of electrons** (OIL RIG). Reduction is the reverse, and the two
  always occur together.
- The **oxidising agent** gains electrons and is reduced; the **reducing agent**
  loses electrons and is oxidised. In disproportionation one element does both.
- Oxidation number is the charge an atom would have if all bonds were ionic. Key
  rules: free element 0; H = +1 (−1 in hydrides); O = −2 (−1 in peroxides); the
  sum equals 0 for a molecule and the charge for an ion.
- Oxidation number can be fractional (Fe₃O₄ = +8/3, Na₂S₄O₆ = +2.5) because it is
  an average; valency never can.
- **Oxidation number method**: equalise total increase with total decrease, then
  balance the rest by inspection.
- **Ion-electron method**: split into halves, balance O with H₂O and H with H⁺
  (converting to OH⁻ in base), balance charge with electrons, cross-multiply and add.
- Always verify both **mass and charge**.
- In electrolysis the anode is positive and oxidises anions; the cathode is
  negative and reduces cations. Preferential discharge decides which ion reacts.
- Faraday: $m = Zit = Eit/96500$; one faraday (96500 C) is one mole of electrons
  and deposits one equivalent of any substance.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The oxidation number of chromium in K₂Cr₂O₇ is <span class="marks">[1]</span>
   (a) +2 (b) +3 (c) +6 (d) +7
2. In the reaction Zn + CuSO₄ → ZnSO₄ + Cu, the oxidising agent is <span class="marks">[1]</span>
   (a) Zn (b) Cu²⁺ (c) SO₄²⁻ (d) ZnSO₄
3. The oxidation number of oxygen in hydrogen peroxide is <span class="marks">[1]</span>
   (a) −2 (b) −1 (c) 0 (d) +2
4. One faraday of electricity is equal to <span class="marks">[1]</span>
   (a) 965 C (b) 9650 C (c) 96500 C (d) 1 C
5. During the electrolysis of molten NaCl, chlorine is liberated at the anode because <span class="marks">[1]</span>
   (a) Cl⁻ is reduced there (b) Cl⁻ is oxidised there
   (c) Na⁺ migrates there (d) the anode is negative

::: note Answers to Group A
**1.** (c) — $2(+1) + 2x + 7(-2) = 0$ gives $x = +6$.

**2.** (b) — Cu²⁺ gains the two electrons lost by zinc, so it is reduced and is therefore the oxidising agent.

**3.** (b) — H₂O₂ is a peroxide; with H at +1, $2(+1) + 2x = 0$ gives $x = -1$.

**4.** (c) — 96500 C, the charge carried by one mole of electrons.

**5.** (b) — the anode is positive, so it attracts anions and removes electrons from them: 2Cl⁻ → Cl₂ + 2e⁻.
:::

**Group B — Short answer (5 marks each)**

1. Define oxidation and reduction in terms of electron transfer. Identify the
   oxidising and reducing agent in (i) 2Na + Cl₂ → 2NaCl and
   (ii) MnO₂ + 4HCl → MnCl₂ + Cl₂ + 2H₂O. <span class="marks">[5]</span>
2. Find the oxidation number of the named atom: S in H₂SO₄, S in Na₂S₂O₃,
   Cl in HClO₄, Fe in Fe₃O₄ and S in S₈. <span class="marks">[5]</span>
3. Balance by the **oxidation number method**:
   MnO₂ + HCl → MnCl₂ + Cl₂ + H₂O. <span class="marks">[5]</span>
4. Balance by the **ion-electron method** in acidic medium:
   MnO₄⁻ + C₂O₄²⁻ → Mn²⁺ + CO₂. <span class="marks">[5]</span>
5. State Faraday's two laws of electrolysis. A current of 2 A is passed through
   copper sulphate solution for 965 s. Calculate the mass of copper deposited
   (Cu = 63.5). <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Oxidation is loss of electrons, reduction is gain. (i) Na → Na⁺ + e⁻, so
sodium is oxidised and is the **reducing agent**; Cl₂ + 2e⁻ → 2Cl⁻, so chlorine is
reduced and is the **oxidising agent**. (ii) Mn falls from +4 to +2, so MnO₂ is the
**oxidising agent**; Cl rises from −1 to 0, so HCl is the **reducing agent** (only
two of the four HCl are oxidised, the rest form MnCl₂).

**2.** H₂SO₄: $2 + x - 8 = 0$, $x = +6$. Na₂S₂O₃: $2 + 2x - 6 = 0$, $x = +2$.
HClO₄: $1 + x - 8 = 0$, $x = +7$. Fe₃O₄: $3x - 8 = 0$, $x = +8/3$. S₈: a free
element, so $x = 0$.

**3.** Mn: +4 → +2, a decrease of 2. Cl: −1 → 0, an increase of 1 per atom, i.e. 2
per Cl₂. One MnO₂ therefore oxidises 2 Cl⁻; two more Cl are needed for MnCl₂, so
4 HCl in all, and the 4 H with the 2 O give 2 H₂O:

MnO₂ + 4HCl → MnCl₂ + Cl₂ + 2H₂O

(Mn 1 = 1, Cl 4 = 2 + 2, H 4 = 4, O 2 = 2; charge 0 = 0.)

**4.** Halves: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O and C₂O₄²⁻ → 2CO₂ + 2e⁻.
Multiplying by 2 and 5 to cancel 10 electrons:

2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O

Charge: (−2) + (−10) + (+16) = +4 on the left and 2(+2) = +4 on the right.

**5.** $Q = it = 2 \times 965 = 1930$ C; $E = 63.5/2 = 31.75$;
$m = 31.75 \times 1930 / 96500 = 0.635$ g.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the rules for assigning oxidation numbers and use them to find the
   oxidation number of Mn in KMnO₄, Cr in Cr₂O₇²⁻ and S in Na₂S₄O₆. <span class="marks">[4]</span>
   (b) Balance by the ion-electron method in **basic** medium:
   MnO₄⁻ + I⁻ → MnO₂ + I₂. <span class="marks">[4]</span>
2. (a) Describe the electrolysis of molten sodium chloride, writing the reaction
   at each electrode, and state the rule of preferential discharge. <span class="marks">[3]</span>
   (b) State Faraday's two laws. The same current of 1.5 A is passed for 30
   minutes through AgNO₃ and CuSO₄ solutions connected in series. Calculate the
   mass of silver and of copper deposited. <span class="marks">[5]</span>

::: note Answers to Group C
**1.(a)** KMnO₄: $1 + x - 8 = 0$, so Mn is **+7**. Cr₂O₇²⁻: $2x - 14 = -2$, so Cr
is **+6**. Na₂S₄O₆: $2 + 4x - 12 = 0$, so $4x = 10$ and S is **+2.5**, an average
over four non-equivalent sulphur atoms.

**1.(b)** MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻ and 2I⁻ → I₂ + 2e⁻. Multiplying by 2
and 3 to cancel 6 electrons gives

2MnO₄⁻ + 6I⁻ + 4H₂O → 2MnO₂ + 3I₂ + 8OH⁻

with charge −8 on both sides and O 12 = 12.

**2.(b)** $Q = 1.5 \times 1800 = 2700$ C. Silver: $E = 108$, so
$m = 108 \times 2700/96500 = 3.02$ g. Copper: $E = 63.5/2 = 31.75$, so
$m = 31.75 \times 2700/96500 = 0.888$ g. The ratio 3.40 equals $E_{Ag}/E_{Cu}$, as
the second law requires.
:::

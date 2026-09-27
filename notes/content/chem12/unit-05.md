---
subject: Chemistry
grade: 12
unit: 5
title: Electrochemistry
hours: 7
area: General and Physical Chemistry
---

Electrochemistry is about the two-way traffic between chemical energy and
electrical energy. A redox reaction that happens spontaneously can be made to
push electrons round a wire — that is a **cell**, and it is how a torch, a
mobile phone and an electric vehicle are powered. Run in reverse, electricity
forces an unwilling reaction to go — that is **electrolysis**, and it is how
aluminium, chlorine and electroplated metal are made.

::: key What the examiner wants from this unit
Three things dominate the board paper: describing the **Daniell cell** with its
electrode reactions and cell notation, using the electrochemical series or the
Nernst equation to **calculate an EMF**, and linking EMF to free energy through
$\Delta G^{\circ} = -nFE^{\circ}_{cell}$. Every one of these is a full-mark
question if the signs are right.
:::

## 5.1 Electrode potential and standard electrode potential

Dip a strip of zinc into water. A few Zn atoms leave the metal as Zn²⁺ ions,
leaving their electrons behind:

Zn(s) ⇌ Zn²⁺(aq) + 2e⁻

The metal becomes slightly negative and the layer of solution touching it
slightly positive. This **electrical double layer** stops the process almost at
once, and an equilibrium potential difference is set up across the
metal–solution boundary.

::: definition Electrode potential
The **electrode potential** of an electrode is the potential difference
developed between the metal and its solution when the two are in contact and at
equilibrium. It measures the tendency of the electrode to lose electrons
(oxidation potential) or to gain them (reduction potential).
:::

A metal that loses electrons readily, such as zinc, builds up a negative charge
and has a positive *oxidation* potential. A metal that prefers to take electrons
back, such as copper, behaves the other way round. By international convention
we always tabulate **reduction** potentials, and

$$ E_{\text{oxidation}} = -\,E_{\text{reduction}} $$

The value depends on concentration, temperature and gas pressure, so a reference
set of conditions is fixed.

::: definition Standard electrode potential ($E^{\circ}$)
The standard electrode potential is the electrode potential measured at 298 K
when every ion in the solution is at unit concentration (1 M, strictly unit
activity) and every gas is at 1 bar, relative to the standard hydrogen electrode
which is assigned exactly 0.000 V.
:::

::: caution Absolute electrode potentials cannot be measured
A voltmeter needs two contacts, so any measurement gives a *difference* between
two electrodes. That is why every tabulated $E^{\circ}$ is a value relative to
the hydrogen electrode, not an absolute number.
:::

## 5.2 Types of electrodes: standard hydrogen electrode and calomel electrode

```figure caption="Left: the standard hydrogen electrode — platinised platinum in 1 M H⁺ with H₂ at 1 bar, defined as 0.000 V. Right: the saturated calomel electrode, a convenient secondary reference at +0.242 V."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axes = plt.subplots(1, 2, figsize=(5.2, 3.4))
for ax in axes:
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')

# ---- standard hydrogen electrode -------------------------------------
ax = axes[0]
ax.plot([1.2, 1.2, 8.4, 8.4], [7.4, 1.2, 1.2, 7.4], color=INK, lw=1.5)
ax.add_patch(Rectangle((1.2, 1.2), 7.2, 4.4, facecolor=ACCENT, alpha=0.12, lw=0))
ax.plot([3.4, 3.4, 6.2, 6.2], [9.1, 2.3, 2.3, 9.1], color=MUTED, lw=1.3)
ax.add_patch(Rectangle((4.1, 2.6), 1.4, 0.9, facecolor=INK, lw=0))
ax.text(4.8, 4.0, 'Pt foil', ha='center', fontsize=7.6, color=INK)
for (bx, by) in [(4.2, 4.9), (5.2, 5.4), (4.6, 6.2), (5.4, 6.9), (4.3, 7.6)]:
    ax.add_patch(Circle((bx, by), 0.22, facecolor='none', edgecolor=MUTED, lw=0.9))
ax.annotate('', xy=(3.4, 8.1), xytext=(1.6, 9.2),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.3, mutation_scale=11))
ax.text(1.5, 9.5, 'H₂ at 1 bar', fontsize=7.8, color=INK, ha='left')
ax.text(8.2, 6.1, '1 M H⁺', fontsize=7.8, color=INK, ha='right')
ax.plot([6.2, 9.4], [8.7, 8.7], color=INK, lw=1.3)
ax.text(9.4, 9.0, 'to cell', fontsize=7.6, color=MUTED, ha='right')
ax.text(4.8, 0.35, '2H⁺ + 2e⁻ → H₂', ha='center', fontsize=8.2, color=INK)
ax.text(4.8, -0.25, 'E° = 0.000 V', ha='center', fontsize=8.2, color=INK)
ax.set_title('Standard hydrogen electrode', fontsize=8.6, pad=3)

# ---- calomel electrode -----------------------------------------------
ax = axes[1]
ax.plot([2.4, 2.4, 6.4, 6.4], [8.6, 1.0, 1.0, 8.6], color=INK, lw=1.5)
ax.add_patch(Rectangle((2.4, 1.0), 4.0, 6.4, facecolor=ACCENT, alpha=0.12, lw=0))
ax.add_patch(Rectangle((2.4, 1.0), 4.0, 0.9, facecolor='#8f97a4', lw=0))
ax.text(4.4, 1.42, 'Hg', ha='center', va='center', fontsize=8.0, color='white')
ax.add_patch(Rectangle((2.4, 1.9), 4.0, 0.9, facecolor='#cfd5de', lw=0))
ax.text(4.4, 2.32, 'Hg₂Cl₂ paste', ha='center', va='center', fontsize=7.4, color=INK)
ax.text(4.4, 5.2, 'saturated\nKCl solution', ha='center', fontsize=7.8, color=INK)
ax.plot([4.4, 4.4], [1.45, 9.4], color=MUTED, lw=1.4)
ax.text(4.75, 9.1, 'Pt wire', fontsize=7.6, color=MUTED, ha='left')
# side arm ending in a porous plug
ax.plot([6.4, 8.9], [1.6, 1.6], color=INK, lw=1.4)
ax.plot([6.4, 8.9], [1.0, 1.0], color=INK, lw=1.4)
ax.add_patch(Rectangle((8.5, 1.0), 0.4, 0.6, facecolor='#cfd5de',
                       edgecolor=INK, lw=1.0, hatch='..'))
ax.annotate('', xy=(8.7, 1.7), xytext=(9.2, 3.1),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.text(9.5, 3.3, 'porous\nplug', fontsize=7.2, color=MUTED, ha='right')
ax.text(4.4, 0.35, 'Hg₂Cl₂ + 2e⁻ → 2Hg + 2Cl⁻', ha='center', fontsize=7.8, color=INK)
ax.text(4.4, -0.25, 'E = +0.242 V (saturated KCl)', ha='center', fontsize=7.8,
        color=INK)
ax.set_title('Saturated calomel electrode', fontsize=8.6, pad=3)
fig.subplots_adjust(wspace=0.34)
```
**Standard hydrogen electrode (SHE).** A strip of platinum foil coated with
finely divided platinum black is dipped in a 1 M solution of H⁺ ions, and pure
hydrogen gas at 1 bar is bubbled over it at 298 K. The platinum takes no part in
the reaction; it only provides a surface for the electron transfer and a path
for the current. Its half-reaction is

2H⁺(aq) + 2e⁻ ⇌ H₂(g),  E° = 0.000 V (by definition)

It is the **primary reference electrode**, but it is awkward: it needs a supply
of very pure hydrogen at constant pressure, the solution must be exactly 1 M,
and the platinum surface is poisoned by traces of arsenic or sulphide.

**Calomel electrode.** For daily laboratory work a **secondary reference
electrode** is used instead. The calomel electrode consists of mercury covered
with a paste of mercury(I) chloride, Hg₂Cl₂ (calomel), in contact with a
potassium chloride solution, with a platinum wire dipping into the mercury:

Hg(l) | Hg₂Cl₂(s) | KCl(aq)

Hg₂Cl₂(s) + 2e⁻ ⇌ 2Hg(l) + 2Cl⁻(aq)

Its potential depends only on the chloride concentration, which is easy to fix:

| KCl solution | Electrode potential |
|---|---|
| Saturated | +0.242 V |
| 1.0 M | +0.280 V |
| 0.1 M | +0.334 V |

It is compact, robust, and keeps a steady potential, so it is the reference half
of almost every pH meter.

## 5.3 Electrochemical series and its applications

Arranging the standard reduction potentials of all electrodes in increasing
order gives the **electrochemical series** (also called the activity series or
the electromotive series).

```figure caption="The electrochemical series: standard reduction potentials at 298 K. Reading down, the species on the left become weaker oxidising agents; reading up, the metals become weaker reducing agents. Hydrogen at 0.000 V is the reference."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 4.5))
data = [('Li⁺ / Li', -3.04), ('K⁺ / K', -2.93), ('Ca²⁺ / Ca', -2.87),
        ('Na⁺ / Na', -2.71), ('Mg²⁺ / Mg', -2.37), ('Al³⁺ / Al', -1.66),
        ('Zn²⁺ / Zn', -0.76), ('Fe²⁺ / Fe', -0.44), ('Ni²⁺ / Ni', -0.25),
        ('Pb²⁺ / Pb', -0.13), ('2H⁺ / H₂', 0.00), ('Cu²⁺ / Cu', 0.34),
        ('I₂ / I⁻', 0.54), ('Fe³⁺ / Fe²⁺', 0.77), ('Ag⁺ / Ag', 0.80),
        ('Br₂ / Br⁻', 1.09), ('Cl₂ / Cl⁻', 1.36), ('Au³⁺ / Au', 1.50),
        ('F₂ / F⁻', 2.87)]
vals = [v for _, v in data]
sep = 0.235
lab_y = list(vals)
for i in range(1, len(lab_y)):
    if lab_y[i] - lab_y[i - 1] < sep:
        lab_y[i] = lab_y[i - 1] + sep
for (name, v), ly in zip(data, lab_y):
    c = SERIES[1] if v > 0 else (INK if v == 0 else SERIES[0])
    ax.plot([0, 0.12], [v, v], color=c, lw=1.6)
    ax.plot([0.12, 0.42], [v, ly], color=MUTED, lw=0.6)
    ax.text(0.47, ly, name, fontsize=8.0, color=c, va='center')
    txt = ('+' if v > 0 else ('' if v == 0 else '−')) + f'{abs(v):.2f}'
    if v == 0:
        txt = ' 0.00'
    ax.text(1.42, ly, txt, fontsize=8.0, color=MUTED, va='center')
ax.plot([-0.04, 0.30], [0, 0], color=INK, lw=0.9, ls='--')
ax.annotate('', xy=(2.02, 2.95), xytext=(2.02, 0.35),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5,
                            mutation_scale=11))
ax.text(2.16, 1.65, 'stronger\noxidising agent', fontsize=7.8, color=SERIES[1],
        rotation=90, va='center', ha='center')
ax.annotate('', xy=(2.02, -3.35), xytext=(2.02, -0.35),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.5,
                            mutation_scale=11))
ax.text(2.16, -1.85, 'stronger\nreducing agent', fontsize=7.8, color=SERIES[0],
        rotation=90, va='center', ha='center')
ax.text(1.42, 3.30, 'E° / V', fontsize=8.2, color=INK, va='center')
ax.set_xlim(-0.05, 2.45); ax.set_ylim(-3.6, 3.5)
ax.set_ylabel('standard reduction potential  $E^{\\circ}$  (V)')
ax.set_xticks([])
ax.spines[['top', 'right', 'bottom']].set_visible(False)
```
::: memory The order that matters
**Li K Ca Na Mg Al Zn Fe Ni Sn Pb H Cu Hg Ag Pt Au** — "**L**ittle **K**atie
**Ca**n **Na**me **Mg** **Al**l **Zi**nc **Fe**rrous **Ni**ckel **Sn**ow
**Pb**lue **H**ere **Cu**p **Hg** **Ag**ain **Pt**, **Au**." Everything above
hydrogen displaces it from dilute acids; everything below does not.
:::

**Applications of the electrochemical series**

1. **Relative strength of reducing agents.** The more negative $E^{\circ}$, the
   greater the tendency to lose electrons. Li is the strongest reducing agent in
   the list; Au is the weakest.
2. **Relative strength of oxidising agents.** The more positive $E^{\circ}$, the
   greater the tendency to gain electrons. F₂ is the strongest oxidising agent
   known in aqueous solution.
3. **Predicting displacement reactions.** A metal displaces from solution any
   metal lying below it. Zn (−0.76) displaces Cu (+0.34):
   Zn + CuSO₄ → ZnSO₄ + Cu. Copper cannot displace zinc.
4. **Liberation of hydrogen from acids.** Metals above hydrogen (Zn, Fe, Mg, Al)
   dissolve in dilute HCl or H₂SO₄ giving H₂; Cu, Ag, Hg and Au do not.
5. **Calculating the EMF of a cell** and deciding which electrode is the anode.
6. **Predicting the feasibility of a redox reaction:** if the calculated
   $E^{\circ}_{cell}$ is positive the reaction goes as written.
7. **Products of electrolysis.** When two cations compete at the cathode, the
   one with the higher reduction potential is discharged first.
8. **Corrosion and its prevention.** Iron is protected by coating with a more
   easily oxidised metal (zinc — galvanising), which corrodes sacrificially.

## 5.4 Voltaic cell: Zn-Cu cell, Ag-Cu cell

If zinc is dropped into copper sulphate solution, the reaction
Zn + Cu²⁺ → Zn²⁺ + Cu occurs at once, but the electrons pass directly from Zn
to Cu²⁺ and all the energy appears as heat. A **voltaic (galvanic) cell**
separates the two half-reactions so the electrons are forced to travel through
an external wire, where they can do useful work.

```figure caption="The Daniell cell, Zn(s) | Zn²⁺(1 M) || Cu²⁺(1 M) | Cu(s). Electrons leave the zinc anode, travel through the external wire to the copper cathode; the salt bridge carries ions to keep both solutions electrically neutral."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.2, 3.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 7.3); ax.axis('off')
RED = '#A8271F'; GRN = '#0B6A62'

# beakers and solutions
for x0, col, sol in [(0.6, '#cfd5de', '1 M ZnSO₄'), (5.9, ACCENT, '1 M CuSO₄')]:
    ax.plot([x0, x0, x0 + 3.5, x0 + 3.5], [4.4, 1.0, 1.0, 4.4], color=INK, lw=1.5)
    ax.add_patch(Rectangle((x0, 1.0), 3.5, 2.6, facecolor=col, alpha=0.22, lw=0))
    ax.text(x0 + 1.75, 1.35, sol, ha='center', fontsize=7.8, color=INK)

# electrodes
ax.add_patch(Rectangle((1.35, 1.6), 0.30, 3.5, facecolor='#8f97a4', lw=0))
ax.add_patch(Rectangle((8.35, 1.6), 0.30, 3.5, facecolor='#b06a3b', lw=0))
ax.text(1.85, 4.75, 'Zn', fontsize=9.0, color=INK)
ax.text(8.15, 4.75, 'Cu', fontsize=9.0, color=INK, ha='right')

# external circuit with voltmeter
ax.plot([1.50, 1.50, 4.55], [5.1, 6.6, 6.6], color=INK, lw=1.4)
ax.plot([5.45, 8.50, 8.50], [6.6, 6.6, 5.1], color=INK, lw=1.4)
ax.add_patch(Circle((5.0, 6.6), 0.45, facecolor='none', edgecolor=INK, lw=1.3))
ax.text(5.0, 6.6, 'V', ha='center', va='center', fontsize=9.5, color=INK)
for xa, xb in [(2.2, 3.3), (6.7, 7.8)]:
    ax.annotate('', xy=(xb, 6.6), xytext=(xa, 6.6),
                arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.5,
                                mutation_scale=11))
ax.text(2.75, 6.85, 'e⁻', ha='center', fontsize=8.6, color=RED)
ax.text(7.25, 6.85, 'e⁻', ha='center', fontsize=8.6, color=RED)

# salt bridge
ax.plot([2.95, 2.95, 7.05, 7.05], [3.0, 4.85, 4.85, 3.0], color='#9aa2ae', lw=5,
        solid_capstyle='butt', zorder=1)
ax.text(5.0, 5.55, 'salt bridge (KCl in agar)', ha='center', fontsize=7.8,
        color=MUTED)
ax.annotate('', xy=(5.65, 5.15), xytext=(4.35, 5.15),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.3, mutation_scale=10))
ax.text(6.55, 5.15, 'K⁺', fontsize=8.0, color=GRN, va='center', ha='center')
ax.annotate('', xy=(4.35, 4.52), xytext=(5.65, 4.52),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.3, mutation_scale=10))
ax.text(3.45, 4.52, 'Cl⁻', fontsize=8.0, color=GRN, va='center', ha='center')

# electrode labels and half reactions
ax.text(0.45, 0.62, 'anode (−)  oxidation', fontsize=8.0, color=INK, ha='left')
ax.text(0.45, 0.18, 'Zn → Zn²⁺ + 2e⁻', fontsize=8.0, color=RED, ha='left')
ax.text(9.55, 0.62, 'cathode (+)  reduction', fontsize=8.0, color=INK, ha='right')
ax.text(9.55, 0.18, 'Cu²⁺ + 2e⁻ → Cu', fontsize=8.0, color=RED, ha='right')
```

**The Daniell cell (Zn–Cu cell).** A zinc rod stands in 1 M ZnSO₄ in one beaker
and a copper rod in 1 M CuSO₄ in another. The rods are joined by a wire through
a voltmeter, and the two solutions by a **salt bridge** — an inverted U-tube
packed with a saturated solution of KCl (or KNO₃) set in agar jelly.

| Electrode | Name | Sign | Process | Half-reaction |
|---|---|---|---|---|
| Zn | Anode | − | Oxidation | Zn(s) → Zn²⁺(aq) + 2e⁻ |
| Cu | Cathode | + | Reduction | Cu²⁺(aq) + 2e⁻ → Cu(s) |

Overall: Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s),  $E^{\circ}_{cell} = 1.10$ V

The cell is written, by IUPAC convention, with the anode on the left, a single
bar for a phase boundary and a double bar for the salt bridge:

Zn(s) | Zn²⁺(1 M) || Cu²⁺(1 M) | Cu(s)

::: key Three jobs of the salt bridge
1. It completes the electrical circuit by allowing ions to move between the two
   half-cells.
2. It keeps both solutions **electrically neutral**: its anions move to the
   anode compartment (which is gaining Zn²⁺) and its cations to the cathode
   compartment (which is losing Cu²⁺).
3. It prevents the two solutions from mixing, and eliminates the liquid-junction
   potential that would otherwise appear.
:::

**The Ag–Cu cell.** Here copper is the more easily oxidised metal, so copper is
now the anode and silver the cathode:

Cu(s) | Cu²⁺(1 M) || Ag⁺(1 M) | Ag(s)

| Electrode | Half-reaction | $E^{\circ}$ / V |
|---|---|---|
| Anode (Cu) | Cu(s) → Cu²⁺(aq) + 2e⁻ | $-0.34$ (oxidation) |
| Cathode (Ag) | 2Ag⁺(aq) + 2e⁻ → 2Ag(s) | $+0.80$ (reduction) |

Overall: Cu(s) + 2Ag⁺(aq) → Cu²⁺(aq) + 2Ag(s),  $E^{\circ}_{cell} = 0.46$ V

::: caution Never multiply $E^{\circ}$ by the stoichiometric number
The silver half-reaction had to be doubled to balance the two electrons, but
$E^{\circ}$ stays at +0.80 V. Electrode potential is an **intensive** property —
it is energy *per unit charge*, so it does not depend on how much reaction you
write. Only $\Delta G$ scales with $n$.
:::

**Electrolytic cells — the reverse process.** If an external source pushes
current the other way, a non-spontaneous reaction can be driven. That is an
electrolytic cell.

```figure caption="An electrolytic cell for molten sodium chloride. The battery forces electrons on to the cathode, where Na⁺ is reduced, and pulls them from the anode, where Cl⁻ is oxidised. Here the cathode is negative — the opposite of a galvanic cell."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 7.4); ax.axis('off')
RED = '#A8271F'; GRN = '#0B6A62'

ax.plot([1.8, 1.8, 8.2, 8.2], [4.6, 1.0, 1.0, 4.6], color=INK, lw=1.5)
ax.add_patch(Rectangle((1.8, 1.0), 6.4, 2.9, facecolor=SERIES[3], alpha=0.16, lw=0))
ax.text(5.0, 1.35, 'molten NaCl', ha='center', fontsize=8.2, color=INK)

ax.add_patch(Rectangle((3.15, 1.7), 0.30, 3.6, facecolor='#8f97a4', lw=0))
ax.add_patch(Rectangle((6.55, 1.7), 0.30, 3.6, facecolor='#8f97a4', lw=0))

# battery
ax.plot([3.30, 3.30, 4.35], [5.3, 6.6, 6.6], color=INK, lw=1.4)
ax.plot([5.65, 6.70, 6.70], [6.6, 6.6, 5.3], color=INK, lw=1.4)
for dx, h, lw in [(0.0, 0.26, 2.4), (0.30, 0.45, 1.3), (0.60, 0.26, 2.4),
                  (0.90, 0.45, 1.3)]:
    ax.plot([4.45 + dx, 4.45 + dx], [6.6 - h, 6.6 + h], color=INK, lw=lw)
ax.text(4.32, 7.05, '−', fontsize=12, color=INK, ha='center')
ax.text(5.48, 7.05, '+', fontsize=11, color=INK, ha='center')
ax.text(5.0, 5.75, 'DC source', ha='center', fontsize=8.0, color=MUTED)

ax.annotate('', xy=(3.45, 6.6), xytext=(4.15, 6.6),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.5, mutation_scale=11))
ax.annotate('', xy=(6.55, 6.6), xytext=(5.85, 6.6),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.5, mutation_scale=11))
ax.text(3.80, 6.85, 'e⁻', ha='center', fontsize=8.6, color=RED)
ax.text(6.20, 6.85, 'e⁻', ha='center', fontsize=8.6, color=RED)

# ion migration
ax.annotate('', xy=(3.75, 3.05), xytext=(5.05, 3.05),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.3, mutation_scale=10))
ax.text(5.30, 3.05, 'Na⁺', fontsize=8.2, color=GRN, va='center')
ax.annotate('', xy=(6.25, 2.30), xytext=(4.95, 2.30),
            arrowprops=dict(arrowstyle='-|>', color=GRN, lw=1.3, mutation_scale=10))
ax.text(4.70, 2.30, 'Cl⁻', fontsize=8.2, color=GRN, va='center', ha='right')

ax.text(0.30, 0.62, 'cathode (−)', fontsize=8.2, color=INK, ha='left')
ax.text(0.30, 0.18, 'Na⁺ + e⁻ → Na', fontsize=8.0, color=RED, ha='left')
ax.text(9.70, 0.62, 'anode (+)', fontsize=8.2, color=INK, ha='right')
ax.text(9.70, 0.18, '2Cl⁻ → Cl₂ + 2e⁻', fontsize=8.0, color=RED, ha='right')
```

| | Galvanic (voltaic) cell | Electrolytic cell |
|---|---|---|
| Energy change | Chemical → electrical | Electrical → chemical |
| Reaction | Spontaneous, $\Delta G < 0$ | Non-spontaneous, $\Delta G > 0$ |
| Anode | Negative, oxidation | Positive, oxidation |
| Cathode | Positive, reduction | Negative, reduction |
| Electrolytes | Two, joined by a salt bridge | One, both electrodes in it |
| Example | Daniell cell, dry cell | Electroplating, extraction of Na, Al |

Note that oxidation always happens at the anode and reduction always at the
cathode. Only the **signs** swap.

## 5.5 Cell potential and standard cell potential

::: definition Cell potential (EMF)
The **cell potential** or **electromotive force** is the potential difference
between the two electrodes of a cell when no current is drawn. Under standard
conditions it is the **standard cell potential** $E^{\circ}_{cell}$, and

$$ E^{\circ}_{cell} = E^{\circ}_{cathode} - E^{\circ}_{anode} $$

where both values are standard **reduction** potentials.
:::

A positive $E^{\circ}_{cell}$ means the reaction as written is spontaneous. If
the answer comes out negative, the cell has been written backwards.

When the concentrations are not 1 M the EMF changes, and the **Nernst equation**
gives the correction. For a general cell reaction
$aA + bB \rightarrow cC + dD$ involving $n$ electrons,

$$ E_{cell} = E^{\circ}_{cell} - \frac{RT}{nF}\ln Q = E^{\circ}_{cell} - \frac{0.0591}{n}\log Q \quad (\text{at }298\ \text{K}) $$

The constant follows from $2.303RT/F = 2.303 \times 8.314 \times 298 / 96500 = 0.0591$ V.
Pure solids and pure liquids do not appear in $Q$.

::: example Worked example 5.1
**Problem.** For the Daniell cell at 298 K, $E^{\circ}(\text{Zn}^{2+}/\text{Zn})
= -0.76$ V and $E^{\circ}(\text{Cu}^{2+}/\text{Cu}) = +0.34$ V. Write the cell
reaction and calculate $E^{\circ}_{cell}$. Then find the EMF when
[Zn²⁺] = 0.10 M and [Cu²⁺] = 0.010 M.

**Solution.** Copper has the higher (more positive) reduction potential, so
copper is reduced and is the cathode; zinc is oxidised at the anode.

Anode: Zn → Zn²⁺ + 2e⁻ ; Cathode: Cu²⁺ + 2e⁻ → Cu ; overall
Zn + Cu²⁺ → Zn²⁺ + Cu, with $n = 2$.

$$ E^{\circ}_{cell} = E^{\circ}_{cathode} - E^{\circ}_{anode} = 0.34 - (-0.76) = 1.10\ \text{V} $$

For the non-standard concentrations, $Q = [\text{Zn}^{2+}]/[\text{Cu}^{2+}]$
(the two solids are omitted):

$$ Q = \frac{0.10}{0.010} = 10 \qquad \log Q = 1 $$
$$ E_{cell} = 1.10 - \frac{0.0591}{2}(1) = 1.10 - 0.0296 = 1.07\ \text{V} $$

Raising the product-ion concentration lowers the EMF, exactly as Le Chatelier's
principle predicts.
:::

::: tip Getting the Nernst sign right every time
Put the **products** of the cell reaction on top of $Q$. If $Q > 1$ the log is
positive and the EMF falls below $E^{\circ}$; if $Q < 1$ the EMF rises. A cell
runs down because $Q$ climbs towards $K$, at which point $E_{cell} = 0$ and the
battery is flat.
:::

## 5.6 Relationship between cell potential and free energy

The electrical work a cell can deliver is (charge transferred) × (potential
difference). For $n$ moles of electrons the charge is $nF$, where
$F = 96500$ C mol⁻¹ is the **Faraday constant** — the charge on one mole of
electrons, $F = N_A e = (6.022\times10^{23})(1.602\times10^{-19})$ C.

::: derivation $\Delta G = -nFE_{cell}$
At constant temperature and pressure, the maximum non-expansion work obtainable
from a process equals $\Delta G$:

$$ w_{\max} = \Delta G $$

A cell working reversibly transfers $nF$ coulombs through a potential difference
$E_{cell}$, doing electrical work $nFE_{cell}$ **on the surroundings**. Work
done by the system is negative, so

$$ \Delta G = -nFE_{cell}, \qquad \Delta G^{\circ} = -nFE^{\circ}_{cell} $$

Combining this with $\Delta G^{\circ} = -2.303RT\log K$ from Unit 4,

$$ -nFE^{\circ}_{cell} = -2.303RT\log K \;\Longrightarrow\; \log K = \frac{nE^{\circ}_{cell}}{0.0591} \quad (298\ \text{K}) $$
:::

So a spontaneous cell reaction ($\Delta G < 0$) is exactly one with a positive
EMF, and a large EMF means a large equilibrium constant.

::: example Worked example 5.2
**Problem.** For the cell Cu(s) | Cu²⁺(1 M) || Ag⁺(1 M) | Ag(s),
$E^{\circ}(\text{Cu}^{2+}/\text{Cu}) = +0.34$ V and
$E^{\circ}(\text{Ag}^{+}/\text{Ag}) = +0.80$ V. Calculate $E^{\circ}_{cell}$,
$\Delta G^{\circ}$ and the equilibrium constant at 298 K.

**Solution.** The cell reaction is Cu + 2Ag⁺ → Cu²⁺ + 2Ag, so $n = 2$.

$$ E^{\circ}_{cell} = 0.80 - 0.34 = 0.46\ \text{V} $$
$$ \Delta G^{\circ} = -nFE^{\circ}_{cell} = -(2)(96500)(0.46) = -88780\ \text{J} = -88.8\ \text{kJ mol}^{-1} $$
$$ \log K = \frac{nE^{\circ}_{cell}}{0.0591} = \frac{2 \times 0.46}{0.0591} = 15.57 $$
$$ K = 10^{15.57} = 3.7\times10^{15} $$

$\Delta G^{\circ}$ is large and negative and $K$ enormous, so copper metal
reduces silver ions essentially completely — the basis of the silver-mirror
deposits seen when a copper wire is left in silver nitrate solution.
:::

::: example Worked example 5.3
**Problem.** The EMF of the cell
Zn(s) | Zn²⁺(1 M) || H⁺(unknown) | H₂(1 bar), Pt
is 0.5827 V at 298 K. Given $E^{\circ}(\text{Zn}^{2+}/\text{Zn}) = -0.76$ V,
calculate the pH of the acid solution.

**Solution.** The cell reaction is Zn + 2H⁺ → Zn²⁺ + H₂, with $n = 2$, and

$$ E^{\circ}_{cell} = E^{\circ}_{cathode} - E^{\circ}_{anode} = 0.00 - (-0.76) = 0.76\ \text{V} $$

Applying the Nernst equation, with the pure solid and the gas at 1 bar omitted,

$$ E = E^{\circ} - \frac{0.0591}{2}\log\frac{[\text{Zn}^{2+}]}{[\text{H}^{+}]^{2}}
= 0.76 - \frac{0.0591}{2}\log\frac{1}{[\text{H}^{+}]^{2}} $$

Now $\log(1/[\text{H}^{+}]^{2}) = -2\log[\text{H}^{+}] = 2\,\text{pH}$, so

$$ 0.5827 = 0.76 - \frac{0.0591}{2}(2\,\text{pH}) = 0.76 - 0.0591\,\text{pH} $$
$$ \text{pH} = \frac{0.76 - 0.5827}{0.0591} = \frac{0.1773}{0.0591} = 3.00 $$

The solution has pH 3. This is precisely how a pH meter works, except that a
glass electrode and a calomel electrode replace the zinc and hydrogen electrodes.
:::

### Faraday's laws of electrolysis

The same constant $F$ governs how much substance an electric current deposits.

::: key Faraday's two laws
**First law.** The mass of a substance liberated at an electrode is directly
proportional to the quantity of electricity passed:
$m = Zit$, where $Q = it$ and $Z$ is the electrochemical equivalent.

**Second law.** When the same quantity of electricity is passed through
different electrolytes, the masses liberated are proportional to their
equivalent weights.

In practice: 1 faraday (96500 C) deposits one gram-equivalent, i.e.
$\dfrac{\text{molar mass}}{n}$ grams, where $n$ is the number of electrons in
the electrode half-reaction.
:::

::: example Worked example 5.4
**Problem.** A current of 5.0 A is passed for 30 minutes through a solution of
copper(II) sulphate using inert electrodes. Calculate (a) the mass of copper
deposited at the cathode and (b) the volume of oxygen liberated at the anode,
measured at STP. (Cu = 63.5, $F = 96500$ C mol⁻¹, molar volume at STP =
22400 cm³.)

**Solution.** First find the charge passed:

$$ Q = it = (5.0\ \text{A})(30 \times 60\ \text{s}) = 9000\ \text{C} $$
$$ \text{moles of electrons} = \frac{9000}{96500} = 0.09326\ \text{mol} $$

(a) At the cathode, Cu²⁺ + 2e⁻ → Cu, so 2 mol of electrons give 1 mol of Cu:

$$ n(\text{Cu}) = \frac{0.09326}{2} = 0.04663\ \text{mol} $$
$$ m(\text{Cu}) = 0.04663 \times 63.5 = 2.96\ \text{g} $$

(b) At the anode, 2H₂O → O₂ + 4H⁺ + 4e⁻, so 4 mol of electrons give 1 mol of O₂:

$$ n(\text{O}_2) = \frac{0.09326}{4} = 0.02332\ \text{mol} $$
$$ V(\text{O}_2) = 0.02332 \times 22400 = 522\ \text{cm}^{3} $$
:::

## 5.7 Commercial batteries and fuel cells (hydrogen/oxygen)

A **battery** is one or more galvanic cells packaged for use. **Primary cells**
cannot be recharged because the electrode reaction is not reversible;
**secondary cells** (accumulators) can.

| Battery | Anode | Cathode | Electrolyte | EMF | Type |
|---|---|---|---|---|---|
| Dry (Leclanché) cell | Zn can | graphite rod in MnO₂ + C | NH₄Cl + ZnCl₂ paste | ≈1.5 V | Primary |
| Lead storage battery | Pb | PbO₂ | 38 % H₂SO₄ | 2.0 V per cell | Secondary |
| Nickel–cadmium cell | Cd | NiO(OH) | KOH | ≈1.2 V | Secondary |
| Lithium-ion cell | graphite holding Li | LiCoO₂ | Li salt in organic solvent | ≈3.7 V | Secondary |

**Dry cell.** Anode: Zn(s) → Zn²⁺(aq) + 2e⁻. Cathode:
2MnO₂(s) + 2NH₄⁺(aq) + 2e⁻ → Mn₂O₃(s) + 2NH₃(aq) + H₂O(l). It runs down because
the zinc case is eaten away and NH₃ collects round the cathode.

**Lead storage battery.** Used in every car and in inverter backup systems
during load-shedding. On **discharge**:

- Anode: Pb(s) + SO₄²⁻(aq) → PbSO₄(s) + 2e⁻
- Cathode: PbO₂(s) + SO₄²⁻(aq) + 4H⁺(aq) + 2e⁻ → PbSO₄(s) + 2H₂O(l)
- Overall: Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O

On **charging** the whole reaction is reversed, regenerating Pb and PbO₂ and
restoring the acid. Because sulphuric acid is consumed on discharge, the state
of charge can be checked by measuring the density of the acid with a hydrometer.

**Fuel cells.** A fuel cell is a galvanic cell in which the reactants are
supplied continuously from outside, so the cell never "runs down". The
hydrogen–oxygen fuel cell used on the Apollo spacecraft is the standard example.

```figure caption="The hydrogen–oxygen fuel cell. Hydrogen and oxygen are fed continuously to porous carbon electrodes containing a finely divided platinum catalyst; the only product is water, and $E^{\circ}_{cell} = 1.23$ V."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.3))
ax.set_xlim(0, 10); ax.set_ylim(0, 8.0); ax.axis('off')
RED = '#A8271F'

ax.add_patch(Rectangle((2.3, 1.6), 5.4, 3.6, facecolor=ACCENT, alpha=0.13, lw=0))
ax.plot([2.3, 2.3, 7.7, 7.7], [5.2, 1.6, 1.6, 5.2], color=INK, lw=1.5)
ax.text(5.0, 3.1, 'aqueous KOH\n(electrolyte)', ha='center', fontsize=8.0,
        color=INK)

for x0 in (3.05, 6.25):
    ax.add_patch(Rectangle((x0, 1.95), 0.44, 3.9, facecolor='#6b7280',
                           alpha=0.85, lw=0, hatch='///'))
ax.text(3.27, 3.6, 'porous C + Pt', fontsize=6.8, color='white', rotation=90,
        ha='center', va='center')
ax.text(6.47, 3.6, 'porous C + Pt', fontsize=6.8, color='white', rotation=90,
        ha='center', va='center')

# gas inlets, entering from the sides above the liquid
ax.annotate('', xy=(3.00, 6.35), xytext=(1.05, 6.35),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4, mutation_scale=11))
ax.text(1.05, 6.62, 'H₂ in', fontsize=8.4, color=INK, ha='left')
ax.annotate('', xy=(6.74, 6.35), xytext=(8.95, 6.35),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4, mutation_scale=11))
ax.text(8.95, 6.62, 'O₂ in', fontsize=8.4, color=INK, ha='right')

# external circuit with load
ax.plot([3.27, 3.27, 4.30], [5.90, 7.55, 7.55], color=INK, lw=1.4)
ax.plot([5.70, 6.47, 6.47], [7.55, 7.55, 5.90], color=INK, lw=1.4)
ax.add_patch(Rectangle((4.30, 7.28), 1.40, 0.54, facecolor='none',
                       edgecolor=INK, lw=1.2))
ax.text(5.00, 7.55, 'load', ha='center', va='center', fontsize=8.0, color=INK)
ax.annotate('', xy=(4.15, 7.55), xytext=(3.45, 7.55),
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.5, mutation_scale=11))
ax.text(3.80, 7.78, 'e⁻', ha='center', fontsize=8.4, color=RED)

# water out
ax.annotate('', xy=(5.00, 0.85), xytext=(5.00, 1.55),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4, mutation_scale=11))
ax.text(5.30, 0.92, 'H₂O out', fontsize=8.0, color=ACCENT, ha='left')

ax.text(0.10, 4.55, 'anode (−)', fontsize=8.0, color=INK, ha='left')
ax.text(0.10, 4.10, '2H₂ + 4OH⁻ →', fontsize=7.0, color=RED, ha='left')
ax.text(0.10, 3.70, '4H₂O + 4e⁻', fontsize=7.0, color=RED, ha='left')
ax.text(9.90, 4.55, 'cathode (+)', fontsize=8.0, color=INK, ha='right')
ax.text(9.90, 4.10, 'O₂ + 2H₂O + 4e⁻', fontsize=7.0, color=RED, ha='right')
ax.text(9.90, 3.70, '→ 4OH⁻', fontsize=7.0, color=RED, ha='right')
```
- Anode: 2H₂(g) + 4OH⁻(aq) → 4H₂O(l) + 4e⁻
- Cathode: O₂(g) + 2H₂O(l) + 4e⁻ → 4OH⁻(aq)
- Overall: 2H₂(g) + O₂(g) → 2H₂O(l),  $E^{\circ}_{cell} = 1.23$ V

**Advantages:** efficiency of 70–75 % against about 40 % for a thermal power
station, because the energy is not first turned into heat; no smoke, no oxides
of nitrogen or sulphur, and the only product is drinkable water; it runs
continuously as long as fuel is supplied. **Disadvantages:** the platinum
catalyst is expensive, and hydrogen is difficult to store and transport safely.

## Chapter summary

- Electrode potential arises from the electrical double layer at a
  metal–solution boundary; only *differences* can be measured, so all
  $E^{\circ}$ values are quoted against the SHE (1 M H⁺, H₂ at 1 bar, 298 K,
  defined as 0.000 V). The calomel electrode (+0.242 V saturated) is the
  practical secondary reference.
- The **electrochemical series** orders standard reduction potentials. More
  negative = better reducing agent; more positive = better oxidising agent.
  A metal displaces any metal below it, and metals above hydrogen liberate H₂
  from dilute acids.
- In a **galvanic cell**, oxidation occurs at the negative anode (written on the
  left) and reduction at the positive cathode. Daniell cell:
  Zn | Zn²⁺(1 M) || Cu²⁺(1 M) | Cu, $E^{\circ}_{cell} = 1.10$ V.
  Ag–Cu cell: Cu | Cu²⁺ || Ag⁺ | Ag, $E^{\circ}_{cell} = 0.46$ V.
- $E^{\circ}_{cell} = E^{\circ}_{cathode} - E^{\circ}_{anode}$; positive means
  spontaneous. $E^{\circ}$ is intensive and is never multiplied by a
  stoichiometric coefficient.
- **Nernst equation:** $E_{cell} = E^{\circ}_{cell} - \frac{0.0591}{n}\log Q$ at 298 K.
- $\Delta G = -nFE_{cell}$, $\Delta G^{\circ} = -nFE^{\circ}_{cell}$ and
  $\log K = nE^{\circ}_{cell}/0.0591$, with $F = 96500$ C mol⁻¹.
- **Faraday:** $Q = it$; 96500 C liberates one gram-equivalent of any substance.
- Primary cells (dry cell) cannot be recharged; secondary cells (lead storage,
  Ni–Cd, Li-ion) can. The H₂–O₂ **fuel cell** is fed continuously,
  $E^{\circ}_{cell} = 1.23$ V, and produces only water.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The standard electrode potential of the standard hydrogen electrode at 298 K is <span class="marks">[1]</span>
   (a) 0.00 V (b) 0.242 V (c) 1.00 V (d) −0.76 V
2. In a galvanic cell the anode is <span class="marks">[1]</span>
   (a) positive and reduction occurs (b) negative and oxidation occurs
   (c) negative and reduction occurs (d) positive and oxidation occurs
3. Which of these metals cannot liberate hydrogen from dilute hydrochloric acid? <span class="marks">[1]</span>
   (a) Zn (b) Fe (c) Mg (d) Cu
4. For the cell Zn | Zn²⁺ || Cu²⁺ | Cu, given $E^{\circ}$ values of −0.76 V and
   +0.34 V, the standard cell potential is <span class="marks">[1]</span>
   (a) 0.42 V (b) 1.10 V (c) −1.10 V (d) 0.34 V
5. The quantity of charge carried by one mole of electrons is about <span class="marks">[1]</span>
   (a) 9650 C (b) 96500 C (c) $1.6\times10^{-19}$ C (d) $6.02\times10^{23}$ C
6. If $E^{\circ}_{cell}$ is positive, then $\Delta G^{\circ}$ for the cell reaction is <span class="marks">[1]</span>
   (a) positive (b) zero (c) negative (d) unpredictable

::: note Answers to Group A
**1.** (a) — it is the arbitrary zero of the whole scale.

**2.** (b) — electrons are released there, so it is the negative terminal of a galvanic cell.

**3.** (d) — copper lies below hydrogen in the electrochemical series.

**4.** (b) — $E^{\circ}_{cell} = 0.34 - (-0.76) = 1.10$ V.

**5.** (b) — one faraday, $F = N_Ae \approx 96500$ C mol⁻¹.

**6.** (c) — $\Delta G^{\circ} = -nFE^{\circ}_{cell}$, and $n$ and $F$ are positive.
:::

**Group B — Short answer (5 marks each)**

1. Define electrode potential and standard electrode potential. Describe the
   construction and working of the standard hydrogen electrode with a labelled
   diagram, and give two of its limitations. <span class="marks">[5]</span>
2. What is a salt bridge? Give its three functions. Describe the Daniell cell,
   writing the electrode reactions, the overall reaction and the cell notation. <span class="marks">[5]</span>
3. State any five applications of the electrochemical series. <span class="marks">[5]</span>
4. Calculate the EMF at 298 K of the cell
   Zn(s) | Zn²⁺(0.01 M) || Cu²⁺(0.1 M) | Cu(s), given
   $E^{\circ}_{cell} = 1.10$ V. <span class="marks">[5]</span>
5. A current of 1.5 A is passed through a silver nitrate solution for 20 minutes.
   Calculate the mass of silver deposited. (Ag = 108) <span class="marks">[5]</span>
6. Explain with electrode reactions the working of the hydrogen–oxygen fuel cell,
   and state two advantages over a thermal power plant. <span class="marks">[5]</span>

::: note Answers to Group B
**4.** The cell reaction is Zn + Cu²⁺ → Zn²⁺ + Cu with $n = 2$, so

$$ Q = \frac{[\text{Zn}^{2+}]}{[\text{Cu}^{2+}]} = \frac{0.01}{0.1} = 0.1, \qquad \log Q = -1 $$
$$ E_{cell} = 1.10 - \frac{0.0591}{2}(-1) = 1.10 + 0.0296 = 1.13\ \text{V} $$

**5.** $Q = it = 1.5 \times 20 \times 60 = 1800$ C. Since Ag⁺ + e⁻ → Ag needs one
electron per silver atom,

$$ n(\text{Ag}) = \frac{1800}{96500} = 0.01865\ \text{mol}, \qquad
m = 0.01865 \times 108 = 2.01\ \text{g} $$

**6.** Anode: 2H₂ + 4OH⁻ → 4H₂O + 4e⁻. Cathode: O₂ + 2H₂O + 4e⁻ → 4OH⁻.
Overall 2H₂ + O₂ → 2H₂O, $E^{\circ}_{cell} = 1.23$ V. Advantages: much higher
conversion efficiency (about 70 % against 40 %) because no heat engine is
involved, and no polluting emissions — the product is pure water.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the relation $\Delta G^{\circ} = -nFE^{\circ}_{cell}$ and hence
   obtain an expression relating $E^{\circ}_{cell}$ to the equilibrium constant. <span class="marks">[4]</span>
   (b) For the cell Cu | Cu²⁺(1 M) || Ag⁺(1 M) | Ag, $E^{\circ}_{cell} = 0.46$ V.
   Calculate $\Delta G^{\circ}$ and $K$ at 298 K, and comment on the extent of
   the reaction. <span class="marks">[4]</span>
2. (a) With a labelled diagram, describe the construction, discharge and
   charging reactions of the lead storage battery. <span class="marks">[5]</span>
   (b) Distinguish between a galvanic cell and an electrolytic cell on any three
   grounds, and state Faraday's two laws of electrolysis. <span class="marks">[3]</span>

::: note Answers to Group C
**1.(b)** The cell reaction Cu + 2Ag⁺ → Cu²⁺ + 2Ag transfers $n = 2$ electrons.

$$ \Delta G^{\circ} = -nFE^{\circ}_{cell} = -(2)(96500)(0.46) = -88780\ \text{J mol}^{-1} = -88.8\ \text{kJ mol}^{-1} $$
$$ \log K = \frac{nE^{\circ}_{cell}}{0.0591} = \frac{0.92}{0.0591} = 15.57
\;\Longrightarrow\; K = 3.7\times10^{15} $$

$K$ is very large, so the reaction goes essentially to completion: copper
dissolves and silver is deposited almost quantitatively.

**2.(a)** Lead plates packed with spongy Pb form the anode, plates packed with
PbO₂ the cathode, both dipping in about 38 % H₂SO₄. Discharge:
Pb + SO₄²⁻ → PbSO₄ + 2e⁻ at the anode and
PbO₂ + SO₄²⁻ + 4H⁺ + 2e⁻ → PbSO₄ + 2H₂O at the cathode, overall
Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O, giving 2.0 V per cell. Charging drives the
same equation backwards: 2PbSO₄ + 2H₂O → Pb + PbO₂ + 2H₂SO₄.

**2.(b)** Galvanic: spontaneous, converts chemical to electrical energy, anode
negative, two electrolytes joined by a salt bridge. Electrolytic:
non-spontaneous, converts electrical to chemical energy, anode positive, one
electrolyte. Faraday's first law: the mass liberated at an electrode is
proportional to the quantity of electricity passed, $m = Zit$. Second law: with
the same quantity of electricity, the masses liberated in different electrolytes
are proportional to their equivalent weights.
:::

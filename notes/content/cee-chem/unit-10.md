---
subject: Chemistry
grade: CEE
unit: 10
title: Electrochemistry
hours: 1
area: Physical Chemistry
---

Electrochemistry is the chemistry of electrons that travel through a wire instead of
jumping between atoms. The paper carries about **one question** from this chapter (our
estimate from the MEC topic list), and it comes in three shapes: a Faraday's-law
calculation with 96 500 C in it, a cell-potential subtraction, or a fact about a named
cell (SHE, calomel, lead–acid, fuel cell) with one word changed. The two ideas that
decide most marks are that **oxidation is always at the anode** in both kinds of cell,
and that **E° is an intensive property** — doubling a half-reaction does not double the
voltage.

::: key What the paper asks from this chapter
- Electrolytic cell: electrical → chemical, anode **positive**, cathode **negative**. Galvanic cell: chemical → electrical, anode **negative**, cathode **positive**. Oxidation at the anode in both.
- Faraday's first law $m = ZIt$ with $Z = E/96500$; second law $m_1/m_2 = E_1/E_2$; one faraday (96 500 C) deposits one gram equivalent.
- Standard electrode potential is a **reduction** potential, measured against the SHE, which is fixed at 0.00 V (1 M H⁺, 1 atm H₂, 298 K, Pt).
- Calomel electrode: a secondary reference, Hg₂Cl₂/Hg in KCl, 0.24 V when saturated.
- The electrochemical series gives reactivity, displacement, cell emf and the products of electrolysis.
- $E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}$; positive means spontaneous. $E^\circ$ is intensive.
- Nernst: $E = E^\circ - \frac{0.059}{n}\log Q$ at 298 K; $\Delta G^\circ = -nFE^\circ$.
- Primary (dry cell, 1.5 V), secondary (lead–acid 2 V per cell, lithium-ion) and fuel cells (H₂–O₂, water is the only product); rusting is an electrochemical cell.
:::

## 10.1 Electrolytic cells and the qualitative and quantitative laws of electrolysis

### The electrolytic cell

::: definition Electrolysis and electrolytic cell
**Electrolysis** is the decomposition of an electrolyte by the passage of a direct
electric current. The apparatus — two electrodes dipping into the electrolyte, connected
to a source of direct current — is an **electrolytic cell**. It converts **electrical
energy into chemical energy**.
:::

- The **anode** is the electrode connected to the **positive** terminal of the supply.
  Oxidation happens there: anions lose electrons.
- The **cathode** is the electrode connected to the **negative** terminal. Reduction
  happens there: cations gain electrons.
- In the external circuit electrons travel from the anode to the positive terminal of the
  battery, and from its negative terminal to the cathode. Inside the electrolyte the
  current is carried by **ions**, not electrons.
- The electrolyte must be an ionic conductor — a molten salt, or a solution of an acid,
  base or salt. Solid ionic compounds do not conduct.

```figure caption="An electrolytic cell. The battery forces electrons out of the anode, where oxidation occurs, and into the cathode, where reduction occurs — the reverse of what the same pair of electrodes would do in a galvanic cell."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis('off')
ax.add_patch(Rectangle((1.2, 0.8), 7.6, 2.9, fc='#dce8f4', ec=INK, lw=1.2, zorder=2))
for x0, col in [(3.2, '#9aa4b2'), (7.0, '#c98a5a')]:
    ax.add_patch(Rectangle((x0, 1.1), 0.26, 3.9, fc=col, ec=INK, lw=0.8, zorder=3))
ax.plot([3.33, 3.33], [5.0, 5.55], color=INK, lw=1.2)
ax.plot([7.13, 7.13], [5.0, 5.55], color=INK, lw=1.2)
ax.plot([3.33, 4.55], [5.55, 5.55], color=INK, lw=1.2)
ax.plot([5.65, 7.13], [5.55, 5.55], color=INK, lw=1.2)
ax.plot([4.85, 4.85], [5.20, 5.90], color=INK, lw=2.2)
ax.plot([5.15, 5.15], [5.38, 5.72], color=INK, lw=2.2)
ax.annotate('', xy=(4.35, 5.55), xytext=(3.55, 5.55),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3))
ax.annotate('', xy=(6.9, 5.55), xytext=(6.1, 5.55),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3))
ax.text(3.95, 5.92, 'e⁻', fontsize=9, color=SERIES[1], ha='center')
ax.text(6.5, 5.92, 'e⁻', fontsize=9, color=SERIES[1], ha='center')
ax.text(5.0, 4.55, 'battery', fontsize=8.6, color=INK, ha='center')
ax.text(3.33, 0.42, 'anode (+)', fontsize=8.8, color=INK, ha='center')
ax.text(7.13, 0.42, 'cathode (−)', fontsize=8.8, color=INK, ha='center')
ax.text(3.62, 3.12, 'oxidation', fontsize=8.4, color=INK)
ax.text(6.6, 3.12, 'reduction', fontsize=8.4, color=INK, ha='right')
ax.text(5.0, 1.15, 'CuSO₄(aq)', fontsize=8.8, color=INK, ha='center')
ax.text(3.62, 2.55, 'O₂', fontsize=8.4, color=MUTED)
ax.text(6.55, 2.55, 'Cu', fontsize=8.4, color=MUTED, ha='right')
```

### Products of electrolysis — the qualitative laws

What appears at the electrodes depends on three things: the electrolyte, the material of
the electrodes and the concentration. The rules of preferential discharge are:

- **At the cathode**, the ion that is **more easily reduced** — the one with the higher
  (more positive) standard reduction potential — is discharged first. In aqueous solution
  Cu²⁺, Ag⁺ and H⁺ compete; Na⁺, K⁺, Ca²⁺, Mg²⁺ and Al³⁺ are never discharged from water,
  because hydrogen is liberated instead.
- **At the anode**, the species more easily oxidised is discharged. With inert electrodes
  in water, OH⁻/H₂O is oxidised to O₂ unless a concentrated halide is present, when Cl₂,
  Br₂ or I₂ appears.

| Electrolyte | Electrodes | At cathode | At anode |
|---|---|---|---|
| Molten NaCl | inert | Na | Cl₂ |
| Aqueous NaCl (concentrated brine) | inert | H₂ | Cl₂ |
| Dilute NaCl solution | inert | H₂ | O₂ |
| Aqueous CuSO₄ | platinum (inert) | Cu | O₂ |
| Aqueous CuSO₄ | copper | Cu (pure) | Cu dissolves |
| Acidified water | platinum | H₂ | O₂ |
| Molten Al₂O₃ in cryolite | carbon | Al | O₂ (which burns the carbon to CO₂) |

The copper-refining case is the important exception: with **copper electrodes**, copper
dissolves at the anode and is deposited at the cathode, so the concentration of CuSO₄
stays constant and impure copper is refined.

::: caution Anode is not always the positive electrode
In an **electrolytic** cell the anode is **positive**; in a **galvanic** cell the anode
is **negative**. What never changes is that **oxidation occurs at the anode** and
**reduction at the cathode**. A question that says "oxidation occurs at the positive
electrode" is wrong for a galvanic cell, and "at the cathode" is wrong for both.
:::

### Faraday's first law

::: definition Faraday's first law of electrolysis
The mass of a substance deposited or liberated at an electrode is **directly
proportional to the quantity of electricity** passed through the electrolyte:
$m \propto Q$, or $m = ZQ = ZIt$, where $I$ is the current in amperes, $t$ the time in
seconds and $Z$ the **electrochemical equivalent** — the mass deposited by one coulomb.
:::

$$ m = ZIt \qquad Z = \frac{E}{96500} $$

$E$ is the equivalent weight in g equiv⁻¹, equal to the molar mass divided by the number
of electrons in the half-reaction ($E = M/n$). The constant **96 500 C** is one
**faraday** ($F$), the charge on one mole of electrons.

$$ F = N_A \times e = (6.02 \times 10^{23})(1.6 \times 10^{-19}) \approx 96\,500\ \text{C mol}^{-1} $$

### Faraday's second law

::: definition Faraday's second law of electrolysis
When the **same quantity of electricity** is passed through several electrolytes in
series, the masses of the substances deposited are **proportional to their equivalent
weights**: $\frac{m_1}{m_2} = \frac{E_1}{E_2}$. Equivalently, **one faraday deposits one
gram equivalent** of any substance.
:::

| Substance | Half-reaction | $n$ | $E = M/n$ | Mass from 96 500 C |
|---|---|---|---|---|
| Ag | Ag⁺ + e⁻ → Ag | 1 | 108 | 108 g |
| Cu | Cu²⁺ + 2e⁻ → Cu | 2 | 31.75 | 31.75 g |
| Al | Al³⁺ + 3e⁻ → Al | 3 | 9 | 9 g |
| H₂ | 2H⁺ + 2e⁻ → H₂ | 2 | 1 | 1 g (11.2 L at STP) |
| O₂ | 2H₂O → O₂ + 4H⁺ + 4e⁻ | 4 | 8 | 8 g (5.6 L at STP) |
| Cl₂ | 2Cl⁻ → Cl₂ + 2e⁻ | 2 | 35.5 | 35.5 g (11.2 L at STP) |

::: example Faraday's first law with 96 500 C
**Problem.** A current of 9.65 A is passed through silver nitrate solution for 100 s.
Find the mass of silver deposited (Ag = 108).

**Solution.** $Q = It = 9.65 \times 100 = 965$ C.
Moles of electrons $= \frac{965}{96\,500} = 0.010$ mol.
Ag⁺ + e⁻ → Ag, so 0.010 mol of Ag is deposited:
$m = 0.010 \times 108 = \mathbf{1.08}$ g.
By the formula: $Z = \frac{108}{96\,500} = 1.119 \times 10^{-3}$ g C⁻¹, and
$m = 1.119 \times 10^{-3} \times 965 = 1.08$ g.
:::

::: example Charge needed for a stated mass
**Problem.** What charge is needed to deposit 1.0 g of copper from copper sulphate
solution? How long will it take at 1.0 A? (Cu = 63.5)

**Solution.** Moles of Cu $= 1.0/63.5 = 0.0157$ mol. Cu²⁺ + 2e⁻ → Cu needs 2 mol of
electrons per mole of copper, so $n(e^-) = 0.0315$ mol.
$Q = 0.0315 \times 96\,500 = \mathbf{3040}$ C (about 3.0 × 10³ C).
$t = Q/I = 3040/1.0 = \mathbf{3040}$ s ≈ 51 min.
:::

::: example Volumes of gases from a charge
**Problem.** 965 C is passed through acidified water between platinum electrodes. What
volume of hydrogen and of oxygen, at STP, is liberated?

**Solution.** 965 C = 0.010 mol of electrons.
Cathode: 2H⁺ + 2e⁻ → H₂, so H₂ = 0.010/2 = 0.005 mol = $0.005 \times 22\,400$ =
**112 mL**.
Anode: 2H₂O → O₂ + 4H⁺ + 4e⁻, so O₂ = 0.010/4 = 0.0025 mol = **56 mL**.
The volumes are in the 2 : 1 ratio the formula of water demands.
:::

::: tip The 96 500 arithmetic in one line
Convert everything to **moles of electrons** first: $n(e^-) = \frac{It}{96\,500}$. Then
divide by the number of electrons in the half-reaction to get moles of substance, and
multiply by the molar mass. Nearly every Faraday question falls to this single chain, and
it avoids the equivalent-weight formula going upside down.
:::

## 10.2 Standard electrode potential, the SHE and the calomel electrode, and the electrochemical series

### Electrode potential

When a metal is dipped into a solution of its own ions, two opposing processes start: metal
atoms leave the lattice as ions (oxidation), and ions from solution deposit on the metal
(reduction). A separation of charge builds up until the two rates balance, leaving the
metal with a definite potential relative to the solution — its **electrode potential**.

::: definition Standard electrode potential
The **standard electrode potential** $E^\circ$ of a half-cell is the potential of that
half-cell measured against the standard hydrogen electrode at 298 K, with every ion at
**1 mol L⁻¹** (or 1 bar for gases). By IUPAC convention it is quoted as a **reduction
potential**: it refers to the half-reaction written as a reduction, $M^{n+} + ne^- \rightarrow M$.
:::

A single electrode potential cannot be measured on its own — only a **difference** between
two electrodes can. So one electrode is chosen as the zero and everything is quoted
against it.

### The standard hydrogen electrode (SHE)

The SHE is a platinum plate coated with finely divided platinum black, dipping into
1 M H⁺ (strictly, unit activity) with hydrogen gas bubbled over it at 1 atm and 298 K.

$$ 2H^+ + 2e^- \rightarrow H_2 \qquad E^\circ = 0.00\ \text{V (by definition)} $$

- Platinum black is used because it **adsorbs** hydrogen and catalyses the electrode
  reaction; platinum itself does not take part.
- To measure the potential of another electrode, it is paired with the SHE and the
  reading of the voltmeter is the required potential — sign included.
- If the unknown electrode is the cathode, the reading is its reduction potential; if it
  is the anode, the reading is the negative of that.

| Feature | Standard hydrogen electrode | Calomel electrode |
|---|---|---|
| Composition | Pt black, 1 M H⁺, H₂ at 1 atm | Hg over Hg₂Cl₂ paste in KCl solution |
| Electrode reaction | 2H⁺ + 2e⁻ → H₂ | Hg₂Cl₂ + 2e⁻ → 2Hg + 2Cl⁻ |
| Potential at 25 °C | 0.00 V by definition | 0.28 V (1 M KCl), 0.24 V (saturated) |
| Role | primary reference | secondary reference |
| Practical drawback | needs a constant supply of pure H₂; fragile; hard to set up | — |

### The calomel electrode

A **calomel electrode** is mercury in contact with a paste of mercury(I) chloride
(calomel, Hg₂Cl₂) and potassium chloride solution, with a platinum wire for contact.

$$ Hg_2Cl_2(s) + 2e^- \rightarrow 2Hg(l) + 2Cl^-(aq) $$

Its potential depends on the chloride concentration, because Cl⁻ appears in the
half-reaction. The **saturated calomel electrode (SCE)** is the laboratory standard:
0.2415 V at 25 °C. It is preferred to the SHE because it is **compact, portable, needs no
hydrogen gas and gives a steady, reproducible potential** — which is why it is called a
**secondary reference electrode**.

::: caution Reference electrodes are not zero
Only the SHE is defined as 0.00 V. A calomel electrode has a real potential of about
+0.24 V, so a reading taken against it must be corrected before it is quoted against the
SHE. Options that call calomel "the zero of the scale" are wrong.
:::

### The electrochemical series

Arranging the standard reduction potentials in order gives the **electrochemical series**
(activity series). The values below are the ones the paper uses.

| Half-reaction (reduction) | $E^\circ$ (V) | Half-reaction (reduction) | $E^\circ$ (V) |
|---|---|---|---|
| F₂ + 2e⁻ → 2F⁻ | +2.87 | 2H⁺ + 2e⁻ → H₂ | 0.00 |
| MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O | +1.51 | Pb²⁺ + 2e⁻ → Pb | −0.13 |
| Au³⁺ + 3e⁻ → Au | +1.50 | Sn²⁺ + 2e⁻ → Sn | −0.14 |
| Cl₂ + 2e⁻ → 2Cl⁻ | +1.36 | Ni²⁺ + 2e⁻ → Ni | −0.25 |
| Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O | +1.33 | Fe²⁺ + 2e⁻ → Fe | −0.44 |
| O₂ + 4H⁺ + 4e⁻ → 2H₂O | +1.23 | Zn²⁺ + 2e⁻ → Zn | −0.76 |
| Br₂ + 2e⁻ → 2Br⁻ | +1.09 | Al³⁺ + 3e⁻ → Al | −1.66 |
| Ag⁺ + e⁻ → Ag | +0.80 | Mg²⁺ + 2e⁻ → Mg | −2.37 |
| Fe³⁺ + e⁻ → Fe²⁺ | +0.77 | Na⁺ + e⁻ → Na | −2.71 |
| Cu²⁺ + 2e⁻ → Cu | +0.34 | K⁺ + e⁻ → K | −2.93 |
| I₂ + 2e⁻ → 2I⁻ | +0.54 | Li⁺ + e⁻ → Li | −3.05 |

```figure caption="The electrochemical series as a ladder. A species high on the left is easily reduced, so it is a good oxidising agent; a metal low on the left holds its electrons tightly and is a strong reducing agent."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.2))
names = ['Li⁺/Li', 'K⁺/K', 'Na⁺/Na', 'Mg²⁺/Mg', 'Al³⁺/Al', 'Zn²⁺/Zn',
         'Fe²⁺/Fe', 'H⁺/H₂', 'Cu²⁺/Cu', 'Ag⁺/Ag', 'Cl₂/Cl⁻', 'F₂/F⁻']
vals = [-3.05, -2.93, -2.71, -2.37, -1.66, -0.76, -0.44, 0.0, 0.34, 0.80, 1.36, 2.87]
y = np.arange(len(names))
cols = [SERIES[1] if v < 0 else ACCENT for v in vals]
ax.barh(y, vals, color=cols, height=0.62, zorder=3)
for i, v in enumerate(vals):
    lab = '0.00' if v == 0 else f'{v:+.2f}'
    ax.text(v + (0.12 if v >= 0 else -0.12), i, lab, va='center',
            ha='left' if v >= 0 else 'right', fontsize=8.0, color=INK)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=8.4)
ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-4.3, 3.9)
ax.set_xlabel('standard reduction potential $E^\\circ$ (V)')
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, axis='x', alpha=0.45, zorder=0)
```

**The four uses of the series — every one of them is examinable.**

1. **Reactivity and reducing strength.** The lower (more negative) the $E^\circ$, the more
   reactive the metal and the stronger its reducing power: K > Na > Mg > Al > Zn > Fe > Pb
   > H > Cu > Ag > Au. Metals above hydrogen displace H₂ from dilute acids; copper, silver
   and gold do not.
2. **Displacement reactions.** A metal higher in the series displaces a metal lower down
   from a solution of its salt: Zn + CuSO₄ → ZnSO₄ + Cu. The reverse never happens
   spontaneously. The same rule predicts halogen displacement: Cl₂ + 2KBr → 2KCl + Br₂.
3. **Cell emf.** $E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}$.
   A positive value means the reaction as written is spontaneous.
4. **Predicting the products of electrolysis.** At the cathode, the ion with the **higher**
   $E^\circ$ is discharged; at the anode, the species with the **lower** $E^\circ$ is
   oxidised. This is why copper, not hydrogen, is deposited from CuSO₄ solution, and why
   sodium is never obtained from aqueous NaCl.

::: memory Two sentences that answer half the questions
"Higher $E^\circ$ wins the electrons" — that is the cathode. "Lower $E^\circ$ loses them"
— that is the anode. Everything else (displacement, corrosion, electrolysis products) is
this one rule applied twice.
:::

## 10.3 Galvanic cells and their standard emf; primary, secondary and hydrogen–oxygen fuel cells

### The galvanic (voltaic) cell

::: definition Galvanic cell
A **galvanic cell** converts the chemical energy of a spontaneous redox reaction into
electrical energy. The two half-reactions are carried out in separate compartments joined
by a **salt bridge**, so that the electrons must travel through an external wire to get
from the reducing agent to the oxidising agent.
:::

In the Daniell cell, zinc is dipped into ZnSO₄ and copper into CuSO₄.

- **Anode (negative):** zinc is oxidised, Zn → Zn²⁺ + 2e⁻. Electrons leave the cell here.
- **Cathode (positive):** copper ions are reduced, Cu²⁺ + 2e⁻ → Cu.
- **Salt bridge:** a tube of KCl or KNO₃ in agar. It lets ions move — cations towards the
  cathode compartment, anions towards the anode — so that both solutions stay electrically
  neutral. Without it the cell stops after a few seconds.

```figure caption="The Daniell cell. Zinc dissolves at the anode and copper is deposited at the cathode; the salt bridge keeps both solutions neutral while the electrons travel round the outside circuit."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.3); ax.axis('off')
ax.add_patch(Rectangle((0.5, 0.6), 3.3, 2.6, fc='#dce8f4', ec=INK, lw=1.2, zorder=2))
ax.add_patch(Rectangle((6.2, 0.6), 3.3, 2.6, fc='#f7e2e0', ec=INK, lw=1.2, zorder=2))
ax.add_patch(Rectangle((1.75, 1.1), 0.26, 3.3, fc='#9aa4b2', ec=INK, lw=0.8, zorder=3))
ax.add_patch(Rectangle((7.45, 1.1), 0.26, 3.3, fc='#c98a5a', ec=INK, lw=0.8, zorder=3))
ax.plot([3.8, 6.2], [2.75, 2.75], color='#b9c3d0', lw=7, solid_capstyle='round', zorder=1)
ax.plot([3.8, 6.2], [2.75, 2.75], color=MUTED, lw=0.9, zorder=2)
ax.plot([1.88, 1.88], [4.4, 5.15], color=INK, lw=1.2)
ax.plot([7.58, 7.58], [4.4, 5.15], color=INK, lw=1.2)
ax.plot([1.88, 4.55], [5.15, 5.15], color=INK, lw=1.2)
ax.plot([5.45, 7.58], [5.15, 5.15], color=INK, lw=1.2)
ax.add_patch(Circle((5.0, 5.15), 0.45, fc='white', ec=INK, lw=1.2, zorder=4))
ax.text(5.0, 5.15, 'V', fontsize=9.5, color=INK, ha='center', va='center', zorder=5)
ax.annotate('', xy=(4.2, 5.42), xytext=(3.0, 5.42),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3))
ax.text(3.6, 5.62, 'e⁻', fontsize=9, color=SERIES[1], ha='center')
ax.text(1.55, 3.95, 'Zn', fontsize=9, color=INK, ha='right')
ax.text(7.95, 3.95, 'Cu', fontsize=9, color=INK, ha='left')
ax.text(2.12, 1.95, 'ZnSO₄(aq)', fontsize=8.2, color=INK, ha='left')
ax.text(7.85, 1.95, 'CuSO₄(aq)', fontsize=8.2, color=INK, ha='left')
ax.text(1.88, 0.28, 'anode (−)', fontsize=8.6, color=INK, ha='center')
ax.text(7.58, 0.28, 'cathode (+)', fontsize=8.6, color=INK, ha='center')
ax.text(5.0, 3.05, 'salt bridge', fontsize=8.2, color=INK, ha='center')
```

**Cell notation** writes the same cell on one line:

$$ \text{Zn(s)} \mid \text{Zn}^{2+}(aq) \parallel \text{Cu}^{2+}(aq) \mid \text{Cu(s)} $$

- The **anode is written on the left** and the cathode on the right.
- A single bar `|` is a phase boundary; the **double bar `||` is the salt bridge**.
- By convention the cell emf is the potential of the right-hand electrode minus that of the
  left-hand one, which is why the anode must be on the left for a positive reading.

### Standard emf of the cell

$$ E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}} = E^\circ_{\text{right}} - E^\circ_{\text{left}} $$

For the Daniell cell: $E^\circ = (+0.34) - (-0.76) = \mathbf{1.10}$ V.

- A **positive** $E^\circ_{\text{cell}}$ means the cell reaction as written is spontaneous
  and the cell delivers current.
- A **negative** value means the reaction runs the other way; the cell as written is
  electrolytic, not galvanic.
- $E^\circ_{\text{cell}} = 0$ means the cell is dead — equilibrium has been reached.

::: caution E° is intensive — doubling a half-reaction changes nothing
$E^\circ$ is a potential difference, an intensive property, like temperature. Multiplying
the coefficients of a half-reaction by 2 doubles $\Delta G^\circ$ and doubles the number of
electrons $n$, but leaves $E^\circ$ **unchanged**, because $\Delta G^\circ = -nFE^\circ$
and both $\Delta G^\circ$ and $n$ double.
Zn²⁺ + 2e⁻ → Zn has $E^\circ = -0.76$ V; so does 2Zn²⁺ + 4e⁻ → 2Zn. Only when you
**reverse** a half-reaction does the sign flip. This is the single most common wrong key
in electrochemistry papers.
:::

**Free energy and the equilibrium constant.** The electrical work a cell can do is the
decrease in free energy:

$$ \Delta G^\circ = -nFE^\circ $$

with $n$ the number of moles of electrons transferred and $F = 96\,500$ C mol⁻¹. For the
Daniell cell, $n = 2$ and $E^\circ = 1.10$ V:
$\Delta G^\circ = -2(96\,500)(1.10) = -2.12 \times 10^5$ J mol⁻¹ = **−212 kJ mol⁻¹**.
At equilibrium $E = 0$ and $\Delta G = 0$, so $E^\circ = \frac{0.059}{n}\log K$ at 298 K.

### The Nernst equation

Real cells do not run at 1 M. The emf depends on concentration:

$$ E = E^\circ - \frac{2.303RT}{nF}\log Q = E^\circ - \frac{0.059}{n}\log Q \quad (298\ \text{K}) $$

where $Q$ is the reaction quotient in the same form as an equilibrium constant.

- If the products are at low concentration ($Q < 1$), $E > E^\circ$.
- If the reactants are at low concentration ($Q > 1$), $E < E^\circ$.
- As the cell discharges, $Q$ rises and $E$ falls until $Q = K$ and $E = 0$: the cell is
  flat.

::: example Nernst equation for a dilute half-cell
**Problem.** Find the emf at 298 K of Zn | Zn²⁺(0.01 M) || Cu²⁺(1 M) | Cu, given
$E^\circ = 1.10$ V.

**Solution.** The cell reaction is Zn + Cu²⁺ → Zn²⁺ + Cu, so $Q = [\text{Zn}^{2+}]/[\text{Cu}^{2+}] = 0.01/1 = 0.01$ and $n = 2$.
$E = 1.10 - \frac{0.059}{2}\log(0.01) = 1.10 - 0.0295(-2) = 1.10 + 0.059 = \mathbf{1.16}$ V.
Diluting the anode compartment makes the cell **stronger**, because the zinc has more
room to dissolve.
:::

### Primary, secondary and fuel cells

| Cell | Anode | Cathode | Electrolyte | emf | Rechargeable |
|---|---|---|---|---|---|
| **Leclanché dry cell** (primary) | zinc can | MnO₂ + carbon rod | NH₄Cl + ZnCl₂ paste | 1.5 V | no |
| **Alkaline cell** (primary) | zinc powder | MnO₂ | KOH | 1.5 V | no |
| **Lead–acid accumulator** (secondary) | Pb | PbO₂ | dilute H₂SO₄ | 2 V per cell | yes |
| **Lithium-ion** (secondary) | graphite (LiC₆) | LiCoO₂ | Li salt in organic solvent | 3.7 V | yes |
| **H₂–O₂ fuel cell** | porous carbon with H₂ | porous carbon with O₂ | KOH or polymer membrane | 1.23 V | continuous |

**The dry cell.** The zinc container is itself the anode; a central carbon rod with MnO₂
and graphite powder is the cathode; the paste of NH₄Cl and ZnCl₂ is the electrolyte.

- Anode: Zn → Zn²⁺ + 2e⁻
- Cathode: 2MnO₂ + 2H⁺ + 2e⁻ → Mn₂O₃ + H₂O
- Overall: Zn + 2MnO₂ + 2NH₄⁺ → Zn²⁺ + Mn₂O₃ + 2NH₃ + H₂O

The zinc can is gradually eaten away, which is why an old dry cell leaks. It cannot be
recharged because the electrode reactions are not easily reversed.

**The lead–acid accumulator.** Six cells in series give the familiar 12 V car battery.

- Anode: Pb + SO₄²⁻ → PbSO₄ + 2e⁻
- Cathode: PbO₂ + 4H⁺ + SO₄²⁻ + 2e⁻ → PbSO₄ + 2H₂O
- Overall: Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O

Both electrodes become lead(II) sulphate on discharge, and the sulphuric acid is diluted —
which is why the density of the electrolyte is used to test the state of charge. Recharging
reverses both half-reactions exactly.

**The hydrogen–oxygen fuel cell.** Hydrogen is fed to the anode and oxygen to the cathode
of porous carbon electrodes; the only product is water.

- Anode (alkaline): 2H₂ + 4OH⁻ → 4H₂O + 4e⁻
- Cathode (alkaline): O₂ + 2H₂O + 4e⁻ → 4OH⁻
- Overall: 2H₂ + O₂ → 2H₂O

Its efficiency is about 70 %, far above the 30–40 % of a heat engine, because it is not
limited by the Carnot cycle. Fuel cells powered the Apollo spacecraft and are the model
for hydrogen vehicles.

```figure caption="A Leclanché dry cell in section. The zinc can is the anode and is consumed; the carbon rod in a paste of MnO₂ and graphite is the cathode; the moist NH₄Cl and ZnCl₂ paste is the electrolyte."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.5, 3.3))
ax.set_xlim(0, 10); ax.set_ylim(0, 7.5); ax.axis('off')
ax.add_patch(Rectangle((3.3, 0.7), 3.8, 5.3, fc='#eef1f5', ec=INK, lw=1.3, zorder=2))
ax.add_patch(Rectangle((3.62, 1.02), 3.16, 4.65, fc='#d9c9a3', ec='none', zorder=3))
ax.add_patch(Rectangle((4.02, 1.02), 2.36, 4.65, fc='#4a4a4a', ec='none', zorder=4))
ax.add_patch(Rectangle((4.95, 1.02), 0.5, 5.35, fc='#2b2b2b', ec=INK, lw=0.9, zorder=5))
ax.add_patch(Rectangle((4.72, 6.37), 0.96, 0.36, fc='#b8860b', ec=INK, lw=0.9, zorder=6))
ax.plot([5.2, 5.2], [6.73, 7.10], color=INK, lw=1.2, zorder=6)
ax.text(5.2, 7.28, '+', fontsize=11, color=INK, ha='center')
ax.annotate('zinc can (anode)', xy=(3.28, 2.2), xytext=(0.15, 2.2), fontsize=8.2,
            color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('NH₄Cl + ZnCl₂\npaste', xy=(3.72, 5.15), xytext=(0.15, 5.15), fontsize=8.2,
            color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('MnO₂ + graphite\n(cathode)', xy=(6.3, 4.3), xytext=(7.45, 4.3), fontsize=8.2,
            color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('carbon rod', xy=(5.47, 6.18), xytext=(7.45, 6.10), fontsize=8.2,
            color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('brass cap', xy=(5.70, 6.55), xytext=(7.45, 7.02), fontsize=8.2,
            color=INK, va='center', ha='left',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
```

### Corrosion as an electrochemical cell

Rusting is not a simple combination of iron with oxygen; it needs **both oxygen and
water**, and it happens through tiny short-circuited galvanic cells on the metal surface.

1. At **anodic** patches (where the metal is strained or less protected), iron dissolves:
   Fe → Fe²⁺ + 2e⁻.
2. The electrons travel through the metal to **cathodic** patches, where dissolved oxygen
   is reduced: O₂ + 2H₂O + 4e⁻ → 4OH⁻.
3. The ions meet and precipitate iron(II) hydroxide, which is oxidised further by air to
   hydrated iron(III) oxide — rust, Fe₂O₃·xH₂O.

The water film acts as the electrolyte and the metal itself is the wire, so iron is the
**anode** and is consumed. Anything that makes iron the cathode protects it:

| Method | How it works |
|---|---|
| **Galvanising** (zinc coating) | zinc has the lower $E^\circ$ (−0.76 V), so it oxidises in place of iron — a **sacrificial** coating that still protects a scratched surface |
| **Cathodic protection** | blocks of Mg or Zn are bolted to pipelines and hulls and corrode instead of the steel |
| Painting, greasing, enamelling | keeps out water and oxygen — a barrier, useless once broken |
| Alloying (stainless steel) | chromium forms a thin adherent oxide film that seals the surface |
| Tin plating | tin has a higher $E^\circ$; it protects only while the coat is intact, and makes rusting *faster* once scratched |

::: caution The tin-can trap
A tin coating protects iron only as a physical barrier. Once the tin is scratched, the
iron — lower in the series — becomes the anode and corrodes faster than it would
unprotected. Zinc is the opposite: it keeps protecting even when scratched, because it is
sacrificed.
:::

## Formula and fact sheet

| Quantity | Relation | Note |
|---|---|---|
| Quantity of electricity | $Q = It$ | coulomb = ampere × second |
| One faraday | $F = 96\,500$ C mol⁻¹ $= N_Ae$ | charge of 1 mol of electrons |
| Faraday's first law | $m = ZIt = \frac{EIt}{96\,500}$ | $Z$ = electrochemical equivalent |
| Faraday's second law | $\frac{m_1}{m_2} = \frac{E_1}{E_2}$ | same charge, series cells |
| Equivalent weight | $E = M/n$ | $n$ = electrons per formula unit |
| Mass from charge | $n(e^-) = \frac{It}{96\,500}$ | then ÷ $n$, × $M$ |
| Cell emf | $E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}$ | positive = spontaneous |
| Free energy | $\Delta G^\circ = -nFE^\circ$ | J mol⁻¹ |
| Nernst (298 K) | $E = E^\circ - \frac{0.059}{n}\log Q$ | $Q$ = reaction quotient |
| Equilibrium | $E^\circ = \frac{0.059}{n}\log K$ | at equilibrium $E = 0$ |
| SHE | 2H⁺ + 2e⁻ → H₂, $E^\circ = 0.00$ V | 1 M H⁺, 1 atm, 298 K, Pt black |
| Calomel | Hg₂Cl₂ + 2e⁻ → 2Hg + 2Cl⁻ | 0.28 V (1 M KCl), 0.24 V (saturated) |

| | Electrolytic cell | Galvanic cell |
|---|---|---|
| Energy change | electrical → chemical | chemical → electrical |
| Source of drive | external battery | spontaneous redox reaction |
| Anode sign | **positive** | **negative** |
| Cathode sign | **negative** | **positive** |
| Oxidation | at the anode | at the anode |
| Reduction | at the cathode | at the cathode |
| Electron flow (external) | anode → battery → cathode | anode → cathode |
| Example | electrolysis of brine | Daniell cell, dry cell |

Numbers worth carrying in: 1 F = 96 500 C; 1 F deposits 108 g Ag, 31.75 g Cu, 9 g Al,
1 g H₂ (11.2 L at STP), 8 g O₂ (5.6 L at STP), 35.5 g Cl₂ (11.2 L at STP);
dry cell 1.5 V; lead–acid 2 V per cell (12 V for six); lithium-ion 3.7 V; H₂–O₂ fuel
cell 1.23 V.

## Chapter summary

- An electrolytic cell uses electrical energy to drive a non-spontaneous reaction; the anode is positive and the cathode negative, but oxidation is at the anode and reduction at the cathode in every cell.
- Products of electrolysis follow preferential discharge: the ion with the higher $E^\circ$ is reduced at the cathode; with inert electrodes in water, O₂ appears at the anode unless a concentrated halide gives Cl₂, Br₂ or I₂.
- Faraday's first law: $m = ZIt$ with $Z = E/96\,500$; second law: $m_1/m_2 = E_1/E_2$, and one faraday deposits one gram equivalent.
- $E^\circ$ is a reduction potential measured against the SHE (0.00 V; 1 M H⁺, 1 atm H₂, 298 K, Pt black); the calomel electrode is a portable secondary reference at about 0.24 V.
- The electrochemical series gives reactivity, displacement, cell emf and electrolysis products; higher $E^\circ$ gains electrons, lower $E^\circ$ loses them.
- $E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}$; positive means spontaneous; $E^\circ$ is intensive, so doubling a half-reaction leaves it unchanged.
- Nernst: $E = E^\circ - (0.059/n)\log Q$ at 298 K; $\Delta G^\circ = -nFE^\circ$; at equilibrium $E = 0$ and $E^\circ = (0.059/n)\log K$.
- Primary cells (dry cell 1.5 V, alkaline) cannot be recharged; secondary cells (lead–acid 2 V per cell, lithium-ion) can; fuel cells (H₂–O₂) run continuously and give only water.
- Rusting is an electrochemical cell with iron as the anode; galvanising and cathodic protection work by sacrificing a metal with a lower $E^\circ$.

## Practice questions

**Set A — Recall (25 questions)**

1. In an electrolytic cell, oxidation takes place at the
   (a) cathode (b) anode (c) salt bridge (d) electrolyte
2. In a galvanic cell, the cathode is the electrode where
   (a) oxidation occurs (b) electrons leave the cell (c) reduction occurs (d) zinc dissolves
3. The SI unit of quantity of electricity is the
   (a) coulomb (b) ampere (c) volt (d) farad
4. One faraday is equal to
   (a) 1 C (b) 9 650 C (c) 6.02 × 10²³ C (d) 96 500 C
5. Faraday's first law states that the mass deposited at an electrode is proportional to the
   (a) current only (b) time only (c) quantity of electricity passed (d) equivalent weight
6. The electrochemical equivalent of a substance is the mass deposited by
   (a) 1 coulomb (b) 1 ampere (c) 96 500 coulomb (d) 1 mole of electrons
7. The standard hydrogen electrode is assigned a potential of
   (a) 1.00 V (b) −0.76 V (c) +0.34 V (d) 0.00 V
8. In the standard hydrogen electrode, the H⁺ concentration and the H₂ pressure are
   (a) 0.1 M and 1 atm (b) 1 M and 1 atm (c) 1 M and 0.1 atm (d) 0.1 M and 0.1 atm
9. Standard electrode potentials are quoted as
   (a) reduction potentials (b) oxidation potentials (c) ionisation potentials (d) dissociation potentials
10. The calomel electrode is used as a
   (a) primary standard (b) fuel cell (c) secondary reference electrode (d) salt bridge
11. The potential of the saturated calomel electrode at 25 °C is about
   (a) 0.00 V (b) 0.28 V (c) 0.80 V (d) 0.24 V
12. Metals placed above hydrogen in the electrochemical series
   (a) are noble (b) displace hydrogen from dilute acids (c) cannot be oxidised (d) have positive $E^\circ$ values
13. The emf of the cell Zn | Zn²⁺ || Cu²⁺ | Cu is
   (a) 0.42 V (b) 0.76 V (c) 1.10 V (d) 1.56 V
14. The standard emf of a cell is given by
   (a) $E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}$ (b) $E^\circ_{\text{anode}} - E^\circ_{\text{cathode}}$ (c) $E^\circ_{\text{cathode}} + E^\circ_{\text{anode}}$ (d) their product
15. A lead–acid accumulator is an example of a
   (a) primary cell (b) fuel cell (c) dry cell (d) secondary cell
16. The electrolyte in a lead–acid battery is
   (a) dilute HCl (b) dilute H₂SO₄ (c) NH₄Cl paste (d) molten NaCl
17. The fuel used at the anode of a hydrogen–oxygen fuel cell is
   (a) hydrogen (b) methane (c) methanol (d) ammonia
18. In the Leclanché dry cell the anode is the
   (a) carbon rod (b) MnO₂ powder (c) zinc can (d) graphite powder
19. The emf of a single lead–acid cell is about
   (a) 1.5 V (b) 2.0 V (c) 1.1 V (d) 12 V
20. Rusting of iron is essentially
   (a) a thermal decomposition (b) a photochemical change (c) a simple combination with oxygen (d) an electrochemical process
21. In the rusting of iron, the iron acts as the
   (a) anode (b) cathode (c) electrolyte (d) salt bridge
22. The Nernst equation at 298 K is
   (a) $E = E^\circ - 0.059n\log Q$ (b) $E = E^\circ - \frac{0.059}{n}\log Q$ (c) $E = E^\circ + \frac{0.059}{n}\log Q$ (d) $E = E^\circ - \frac{n}{0.059}\log Q$
23. The relation between standard free-energy change and standard emf is
   (a) $\Delta G^\circ = nFE^\circ$ (b) $\Delta G^\circ = -nE^\circ$ (c) $\Delta G^\circ = -FE^\circ/n$ (d) $\Delta G^\circ = -nFE^\circ$
24. The charge carried by one mole of electrons is called
   (a) one coulomb (b) one ampere (c) one faraday (d) one volt
25. Which of these is a primary cell?
   (a) Leclanché dry cell (b) lead–acid accumulator (c) nickel–cadmium cell (d) lithium-ion cell

::: note Answers and explanations — Set A
**1.** (b) — Oxidation is loss of electrons and always happens at the anode. In an electrolytic cell the anode is the electrode connected to the positive terminal.
**2.** (c) — Reduction at the cathode in every cell. In a galvanic cell the cathode is positive and electrons arrive there from the external circuit.
**3.** (a) — The coulomb is the unit of charge; the ampere is charge per second.
**4.** (d) — 96 500 C, the charge on one mole of electrons ($N_A e$).
**5.** (c) — $m = ZQ$, and $Q = It$, so mass depends on current and time only through the charge they produce.
**6.** (a) — $Z = E/96\,500$ is the mass per coulomb. The mass per mole of electrons is the equivalent weight itself.
**7.** (d) — Zero, by definition; it is the reference against which every other electrode is quoted.
**8.** (b) — Unit activity of H⁺ (1 M in practice), H₂ at 1 atm, 298 K, on platinum black.
**9.** (a) — IUPAC uses reduction potentials. An oxidation potential is the same number with the sign reversed.
**10.** (c) — It is a secondary reference: stable and portable, but its potential is about +0.24 V, not zero.
**11.** (d) — 0.2415 V for the saturated electrode; 0.28 V is the 1 M KCl value.
**12.** (b) — They have negative $E^\circ$ and are oxidised by H⁺. Copper and silver lie below hydrogen and do not.
**13.** (c) — $0.34 - (-0.76) = 1.10$ V. Option (b) is the zinc potential alone; (d) is the Zn–Ag cell.
**14.** (a) — Cathode minus anode, which is the same as right minus left in cell notation.
**15.** (d) — It is rechargeable, so it is a secondary cell. Primary cells cannot be recharged.
**16.** (b) — Dilute sulphuric acid; both electrodes become PbSO₄ on discharge and the acid is diluted.
**17.** (a) — Hydrogen is oxidised at the anode and oxygen reduced at the cathode; the only product is water.
**18.** (c) — The zinc container is oxidised to Zn²⁺. The carbon rod is the cathode, where MnO₂ is reduced.
**19.** (b) — 2 V per cell; six in series give the 12 V car battery.
**20.** (d) — Anodic and cathodic sites on the surface form short-circuited galvanic cells, with iron as the anode.
**21.** (a) — Iron dissolves as Fe²⁺ and releases electrons, so it is oxidised and is the anode.
**22.** (b) — $E = E^\circ - \frac{0.059}{n}\log Q$; the sign is negative because the emf falls as products accumulate.
**23.** (d) — $\Delta G^\circ = -nFE^\circ$; the negative sign shows that a spontaneous cell releases free energy.
**24.** (c) — One faraday, 96 500 C mol⁻¹.
**25.** (a) — The dry cell cannot be recharged. The other three are secondary cells.
:::

**Set B — Understanding (15 questions)**

1. In both galvanic and electrolytic cells, oxidation always occurs at the
   (a) cathode (b) positive electrode of a galvanic cell (c) anode (d) electrode joined to the negative terminal
2. $E^\circ$ for Zn²⁺ + 2e⁻ → Zn is −0.76 V. For 2Zn²⁺ + 4e⁻ → 2Zn, $E^\circ$ is
   (a) −0.76 V (b) −1.52 V (c) −0.38 V (d) +0.76 V
3. A galvanic cell has $E^\circ_{\text{cell}} = +1.10$ V. The cell reaction is
   (a) non-spontaneous (b) at equilibrium (c) spontaneous only on heating (d) spontaneous
4. The salt bridge in a galvanic cell
   (a) carries electrons between the electrodes (b) completes the circuit and keeps the solutions neutral (c) blocks all ion movement (d) supplies the driving voltage
5. Copper does not displace hydrogen from dilute hydrochloric acid because
   (a) its $E^\circ$ lies above that of hydrogen (b) it is too dense (c) it forms a covalent hydride (d) its $E^\circ$ lies below that of hydrogen
6. In the electrolysis of concentrated aqueous NaCl with inert electrodes, the gas at the cathode is
   (a) Cl₂ (b) O₂ (c) H₂ (d) HCl
7. In the electrolysis of aqueous CuSO₄ using copper electrodes, the concentration of CuSO₄
   (a) falls steadily (b) stays unchanged (c) rises steadily (d) falls to zero
8. The same current passes through two cells in series. The masses of copper and silver deposited are in the ratio of their
   (a) atomic masses (b) molar masses (c) valencies (d) equivalent weights
9. $E^\circ$ is +0.80 V for silver and −0.76 V for zinc. In a cell built from them, zinc
   (a) is the cathode (b) is reduced (c) is oxidised and is the anode (d) does not react
10. The calomel electrode is preferred to the hydrogen electrode because it
   (a) is compact and needs no hydrogen supply (b) has a potential of exactly zero (c) is a primary cell (d) contains no mercury
11. A cell reaction has $E^\circ_{\text{cell}} = 0.20$ V. The reaction is
   (a) at equilibrium (b) non-spontaneous (c) impossible (d) spontaneous with a small driving force
12. The overall reaction in a hydrogen–oxygen fuel cell is
   (a) 2H₂O → 2H₂ + O₂ (b) 2H₂ + O₂ → 2H₂O (c) H₂ + O₂ → H₂O₂ (d) 2H₂ + O₂ → 2H₂O₂
13. Galvanising protects iron because zinc
   (a) is oxidised in place of iron (b) is less reactive than iron (c) forms an alloy with iron (d) dissolves oxygen
14. The notation Zn | Zn²⁺(1 M) || Cu²⁺(1 M) | Cu shows that
   (a) zinc is the cathode (b) the double line is a wire (c) zinc is the anode and copper the cathode (d) electrons flow from copper to zinc
15. When a galvanic cell has reached equilibrium, its emf is
   (a) maximum (b) equal to $E^\circ$ (c) negative (d) zero

::: note Answers and explanations — Set B
**1.** (c) — Oxidation is loss of electrons, and the electrode where electrons are released is the anode by definition, whatever its charge.
**2.** (a) — $E^\circ$ is intensive. Doubling the coefficients doubles both $\Delta G^\circ$ and $n$, so $\Delta G^\circ = -nFE^\circ$ leaves $E^\circ$ unchanged.
**3.** (d) — A positive $E^\circ_{\text{cell}}$ gives a negative $\Delta G^\circ$, which is the condition for spontaneity.
**4.** (b) — Ions move through the bridge to balance charge; electrons never travel through it.
**5.** (a) — Copper's $E^\circ$ is +0.34 V, above hydrogen's 0.00 V, so H⁺ cannot oxidise it. Zinc, at −0.76 V, can be oxidised and does displace hydrogen.
**6.** (c) — Water is reduced in preference to Na⁺: 2H₂O + 2e⁻ → H₂ + 2OH⁻. Chlorine appears at the anode.
**7.** (b) — Copper dissolves at the anode and is deposited at the cathode at the same rate, so the concentration is unchanged. This is the basis of electro-refining.
**8.** (d) — Faraday's second law: equal charge deposits masses in the ratio of equivalent weights, 31.75 : 108, not of molar masses.
**9.** (c) — The lower $E^\circ$ is oxidised, so zinc is the anode and dissolves; silver is deposited at the cathode.
**10.** (a) — No gas supply, no fragile platinum black, and a steady reproducible potential — hence "secondary reference".
**11.** (d) — Positive but small: spontaneous, with a modest driving force. $\Delta G^\circ = -nF(0.20)$ is negative but not large.
**12.** (b) — Hydrogen is oxidised, oxygen reduced, and water is the only product.
**13.** (a) — Zinc has the lower $E^\circ$ and is sacrificed, so it protects iron even where the coating is broken.
**14.** (c) — Anode on the left, cathode on the right; the double bar is the salt bridge, and electrons flow from zinc to copper in the wire.
**15.** (d) — At equilibrium $Q = K$ and the Nernst equation gives $E = 0$; the cell is flat.
:::

**Set C — Application (10 questions)**

1. A current of 9.65 A is passed through AgNO₃ solution for 100 s. The mass of silver deposited is (Ag = 108)
   (a) 2.16 g (b) 1.08 g (c) 0.54 g (d) 10.8 g
2. The charge needed to deposit 1.0 g of copper from CuSO₄ is (Cu = 63.5, F = 96 500)
   (a) 1 520 C (b) 96 500 C (c) 6 080 C (d) 3 040 C
3. The time needed to deposit 0.635 g of copper at 1.0 A is (Cu = 63.5)
   (a) 1 930 s (b) 965 s (c) 3 860 s (d) 96.5 s
4. In the electrolysis of acidified water, 965 C liberates at STP
   (a) 224 mL H₂ and 112 mL O₂ (b) 56 mL H₂ and 112 mL O₂ (c) 112 mL H₂ and 56 mL O₂ (d) 112 mL of each
5. For the cell Zn | Zn²⁺ || Ag⁺ | Ag, $E^\circ_{\text{cell}}$ is ($E^\circ$: Zn = −0.76 V, Ag = +0.80 V)
   (a) 0.04 V (b) 1.56 V (c) 0.76 V (d) 1.10 V
6. For the Daniell cell ($E^\circ = 1.10$ V, $n = 2$), $\Delta G^\circ$ is about
   (a) −212 kJ mol⁻¹ (b) −106 kJ mol⁻¹ (c) +212 kJ mol⁻¹ (d) −424 kJ mol⁻¹
7. For Zn | Zn²⁺(0.01 M) || Cu²⁺(1 M) | Cu at 298 K, the emf is about
   (a) 1.16 V (b) 1.10 V (c) 1.04 V (d) 0.96 V
8. The mass of aluminium deposited by 96 500 C from AlCl₃ is (Al = 27)
   (a) 27 g (b) 13.5 g (c) 54 g (d) 9.0 g
9. A current of 2.0 A flows for 30 min through CuSO₄ solution. The mass of copper deposited is (Cu = 63.5)
   (a) 2.37 g (b) 1.18 g (c) 0.59 g (d) 4.74 g
10. Three cells in series carry the same charge. The masses of Ag, Cu and Al deposited are in the ratio (Ag = 108, Cu = 63.5, Al = 27)
   (a) 108 : 63.5 : 27 (b) 1 : 2 : 3 (c) 108 : 31.75 : 9 (d) 54 : 31.75 : 27

::: note Answers and explanations — Set C
**1.** (b) — $Q = 9.65 \times 100 = 965$ C = 0.010 mol e⁻; Ag⁺ + e⁻ → Ag gives 0.010 mol = 1.08 g. Option (a) doubles it by using $n = 1$ twice.
**2.** (d) — 1.0/63.5 = 0.0157 mol Cu, needing 0.0315 mol e⁻; $Q = 0.0315 \times 96\,500 = 3040$ C. Option (a) forgets that two electrons are needed per copper ion.
**3.** (a) — 0.635/63.5 = 0.010 mol Cu → 0.020 mol e⁻ → 1930 C, and at 1.0 A that is 1930 s. Option (b) uses one electron per copper.
**4.** (c) — 965 C = 0.010 mol e⁻; H₂ = 0.005 mol = 112 mL, O₂ = 0.0025 mol = 56 mL, the 2 : 1 volume ratio of water.
**5.** (b) — $0.80 - (-0.76) = 1.56$ V. Option (a) subtracts the magnitudes instead of the signed values; (d) is the Zn–Cu cell.
**6.** (a) — $\Delta G^\circ = -nFE^\circ = -2(96\,500)(1.10) = -2.12 \times 10^5$ J mol⁻¹. Option (b) forgets the factor $n = 2$.
**7.** (a) — $E = 1.10 - \frac{0.059}{2}\log(0.01) = 1.10 + 0.059 = 1.16$ V. Option (c) subtracts instead of adding.
**8.** (d) — 96 500 C = 1 mol e⁻; Al³⁺ + 3e⁻ → Al gives 1/3 mol = 9 g. Option (a) ignores the three electrons.
**9.** (b) — $Q = 2.0 \times 1800 = 3600$ C = 0.0373 mol e⁻ → 0.0187 mol Cu = 1.18 g. Option (a) uses 63.5 g per mole of electrons.
**10.** (c) — Faraday's second law: masses ∝ equivalent weights, 108 : 31.75 : 9. Option (a) uses molar masses and ignores the valencies.
:::

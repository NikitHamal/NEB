---
subject: Chemistry
grade: 12
unit: 6
title: Transition Metals
hours: 5
area: Inorganic Chemistry
---

The ten elements from scandium to zinc fill the 3d orbitals, and in doing so
behave quite unlike the s-block metals of Grade 11. They are hard and
high-melting, they show several oxidation states, their compounds are coloured
and magnetic, they form complex ions, and they catalyse a large share of the
world's industrial chemistry. All of this comes from one structural fact: the
3d and 4s orbitals are very close in energy.

::: key What the examiner wants from this unit
Four recurring questions: list and **explain** the characteristic properties;
explain variable oxidation states from the electronic configuration; define
ligand, coordination number and EAN and calculate them; and draw the **crystal
field splitting** in an octahedral complex and use it to explain colour and
magnetism.
:::

## 6.1 Characteristics of transition metals

::: definition Transition element
A transition element is one whose atom, or one of whose common ions, contains a
**partially filled d subshell**. On this definition the 3d series runs from
Sc to Zn, but zinc (3d¹⁰4s², Zn²⁺ = 3d¹⁰) is **not** a typical transition metal
because neither its atom nor its ion has an incomplete d subshell.
:::

| Element | Sc | Ti | V | Cr | Mn | Fe | Co | Ni | Cu | Zn |
|---|---|---|---|---|---|---|---|---|---|---|
| Z | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
| Configuration ([Ar]) | 3d¹4s² | 3d²4s² | 3d³4s² | 3d⁵4s¹ | 3d⁵4s² | 3d⁶4s² | 3d⁷4s² | 3d⁸4s² | 3d¹⁰4s¹ | 3d¹⁰4s² |

Chromium and copper break the expected pattern because a **half-filled** (3d⁵)
or **completely filled** (3d¹⁰) d subshell is extra stable, so one 4s electron
is promoted.

The characteristic properties, with the reason for each:

1. **Metallic character, hardness and high melting point.** Besides the 4s
   electrons, unpaired 3d electrons also take part in metallic bonding, giving
   strong interatomic bonds. Chromium is the hardest metal; tungsten in the 5d
   series melts at 3410 °C, which is why it is used for lamp filaments. Zinc,
   with no unpaired d electrons, melts at only 420 °C.
2. **High density.** Small atomic volume plus high atomic mass.
3. **Variable oxidation states** (Section 6.2).
4. **Coloured ions** (Section 6.6).
5. **Paramagnetism.** Unpaired d electrons give a magnetic moment;
   $\mu = \sqrt{n(n+2)}$ Bohr magnetons, where $n$ is the number of unpaired
   electrons. Fe, Co and Ni are ferromagnetic.
6. **Complex formation** (Section 6.3) — small, highly charged ions with vacant
   d orbitals attract lone pairs strongly.
7. **Catalytic activity** (Section 6.7).
8. **Alloy formation.** The atomic radii are similar, so atoms replace one
   another freely in the lattice: stainless steel, bronze, brass.
9. **Interstitial compounds.** Small atoms (H, C, N, B) occupy the holes in the
   metal lattice, giving hard, non-stoichiometric solids such as steel and TiC.

```figure caption="Two properties across the 3d series. Melting point rises to a maximum near the middle, where the maximum number of unpaired d electrons is available for bonding, and collapses at zinc (3d¹⁰). Atomic radius falls at first, stays almost constant in the middle, then rises again as d–d repulsion outweighs the rising nuclear charge."
import numpy as np, matplotlib.pyplot as plt
el = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn']
mp = [1541, 1668, 1910, 1907, 1246, 1538, 1495, 1455, 1085, 420]
r = [164, 147, 135, 129, 137, 126, 125, 125, 128, 137]
x = np.arange(10)
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.7))
ax = axes[0]
ax.plot(x, mp, 'o-', color=SERIES[1], ms=4.5)
ax.set_xticks(x); ax.set_xticklabels(el, fontsize=7.6)
ax.set_ylabel('melting point (°C)')
ax.set_ylim(0, 2200)
ax.annotate('Mn: 3d⁵4s²\nhalf-filled,\nweak bonding', (4, 1246),
            textcoords='offset points', xytext=(-6, -46), fontsize=6.8,
            color=MUTED, ha='center')
ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.45)
ax = axes[1]
ax.plot(x, r, 's-', color=SERIES[0], ms=4.0)
ax.set_xticks(x); ax.set_xticklabels(el, fontsize=7.6)
ax.set_ylabel('metallic radius (pm)')
ax.set_ylim(115, 175)
ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.45)
fig.subplots_adjust(wspace=0.38)
```

## 6.2 Oxidation states

The 4s and 3d orbitals differ so little in energy that after the 4s electrons
are removed, 3d electrons can be removed one at a time with comparable effort.
Every intermediate configuration is therefore accessible, and the elements show
a **range of oxidation states differing by one**, unlike the s-block where only
one state exists.

```figure caption="Oxidation states of the 3d elements. Filled circles are the common, stable states; open circles are less common. The maximum state rises to +7 at manganese, where all the 3d and 4s electrons can be used, then falls away as the d electrons become harder to remove."
import numpy as np, matplotlib.pyplot as plt
el = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn']
common = {0: [3], 1: [4], 2: [5], 3: [3, 6], 4: [2, 4, 7],
          5: [2, 3], 6: [2], 7: [2], 8: [2], 9: [2]}
rare = {0: [], 1: [2, 3], 2: [2, 3, 4], 3: [2, 4, 5], 4: [3, 6],
        5: [4, 6], 6: [3], 7: [3, 4], 8: [1, 3], 9: []}
fig, ax = plt.subplots(figsize=(5.0, 3.0))
for i, e in enumerate(el):
    for s in rare.get(i, []):
        ax.plot(i, s, 'o', mfc='none', mec=MUTED, ms=6.5, mew=1.1)
    for s in common.get(i, []):
        ax.plot(i, s, 'o', color=SERIES[0], ms=7.0)
tops = [3, 4, 5, 6, 7, 6, 4, 4, 3, 2]
ax.plot(range(10), tops, color=SERIES[1], lw=1.1, ls='--', alpha=0.8)
ax.text(5.6, 6.35, 'highest state reached', fontsize=7.6, color=SERIES[1])
ax.set_xticks(range(10)); ax.set_xticklabels(el, fontsize=8.0)
ax.set_yticks(range(1, 8))
ax.set_yticklabels([f'+{k}' for k in range(1, 8)], fontsize=8.0)
ax.set_ylabel('oxidation state')
ax.set_xlim(-0.6, 9.6); ax.set_ylim(0.4, 7.8)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='y', alpha=0.4)
```

Points the examiner looks for:

- The **minimum** common state is +2 (loss of the two 4s electrons) for every
  element from Ti onwards. Scandium has only one d electron and forms Sc³⁺,
  giving the noble-gas core.
- The **maximum** state equals the total of 3d and 4s electrons up to manganese
  (Mn: 5 + 2 = +7 in MnO₄⁻; Cr: +6 in Cr₂O₇²⁻; V: +5 in VO₃⁻).
- After Mn, the effective nuclear charge has grown so much that the remaining d
  electrons are held too tightly; Fe rarely goes beyond +3 and Ni, Cu, Zn stop
  at +2 (copper also has a +1 state, 3d¹⁰).
- High oxidation states occur with the most electronegative partners, **oxygen
  and fluorine** (MnO₄⁻, CrO₄²⁻, VF₅).
- Oxides in a **low** oxidation state are basic (MnO), in an intermediate state
  amphoteric (Mn₂O₃, Cr₂O₃), and in a **high** state acidic (Mn₂O₇, CrO₃).

::: example Worked example 6.1
**Problem.** Determine the oxidation state of the metal in (a) KMnO₄,
(b) K₂Cr₂O₇, (c) K₄[Fe(CN)₆] and (d) [Ni(CO)₄].

**Solution.** Take O = −2, K = +1, CN = −1 and CO = 0 (a neutral ligand).

(a) $(+1) + x + 4(-2) = 0 \Rightarrow x - 7 = 0 \Rightarrow x = +7$.

(b) $2(+1) + 2x + 7(-2) = 0 \Rightarrow 2x - 12 = 0 \Rightarrow x = +6$.

(c) The complex ion is [Fe(CN)₆]⁴⁻, so $x + 6(-1) = -4 \Rightarrow x = +2$.

(d) Carbon monoxide is neutral, so $x + 4(0) = 0 \Rightarrow x = 0$. Nickel is
in the **zero** oxidation state — only transition metals do this, and only with
ligands like CO that can accept electron density back from the metal.
:::

::: example Worked example 6.2
**Problem.** 25.0 cm³ of 0.020 M KMnO₄ solution exactly oxidises an acidified
solution of iron(II) sulphate. Write the balanced ionic equation and calculate
the mass of FeSO₄ present. (FeSO₄ = 152 g mol⁻¹.)

**Solution.** Manganese falls from +7 to +2 (5 electrons gained) while iron goes
from +2 to +3 (1 electron lost), so five Fe²⁺ are needed per MnO₄⁻:

MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O

Check: 1 Mn, 5 Fe, 4 O and 8 H on each side; charge $-1 + 10 + 8 = +17$ on the
left and $+2 + 15 = +17$ on the right. Balanced.

$$ n(\text{MnO}_4^{-}) = 0.020 \times \frac{25.0}{1000} = 5.0\times10^{-4}\ \text{mol} $$
$$ n(\text{Fe}^{2+}) = 5 \times 5.0\times10^{-4} = 2.5\times10^{-3}\ \text{mol} $$
$$ m(\text{FeSO}_4) = 2.5\times10^{-3} \times 152 = 0.38\ \text{g} $$

No indicator is needed: the first drop of excess MnO₄⁻ turns the solution pink.
:::

## 6.3 Complex ions and metal complexes

When ammonia is added to copper(II) sulphate solution the pale blue colour
deepens to an intense royal blue:

[Cu(H₂O)₄]²⁺ + 4NH₃ → [Cu(NH₃)₄]²⁺ + 4H₂O

The species in square brackets is a **complex ion** — a central metal ion joined
to a fixed number of surrounding molecules or ions by **coordinate (dative)
bonds**, in which the surrounding species supplies both electrons.

| Term | Meaning | Example in [Cu(NH₃)₄]SO₄ |
|---|---|---|
| Central metal ion | The electron-pair **acceptor** (a Lewis acid) | Cu²⁺ |
| Ligand | The electron-pair **donor** (a Lewis base) | NH₃ |
| Coordination number | Number of coordinate bonds to the central ion | 4 |
| Coordination sphere | The part written inside the square brackets | [Cu(NH₃)₄]²⁺ |
| Counter ion | The ion outside the brackets, free in solution | SO₄²⁻ |

Ligands are classified by how many donor atoms each one uses:

| Type | Donor sites | Examples |
|---|---|---|
| Monodentate | 1 | NH₃, H₂O, CN⁻, Cl⁻, OH⁻, CO, NO₂⁻ |
| Bidentate | 2 | ethane-1,2-diamine (en), oxalate C₂O₄²⁻ |
| Hexadentate | 6 | EDTA⁴⁻ |

A ring formed by a poly-dentate ligand is called a **chelate**, and chelates are
unusually stable — this is why EDTA is used to soften water and to treat lead
poisoning.

::: definition Effective atomic number (EAN)
$$ \text{EAN} = Z - (\text{oxidation state}) + 2 \times (\text{coordination number}) $$
Sidgwick's rule says that a complex is especially stable if its EAN equals the
atomic number of the next noble gas (36 for Kr, 54 for Xe, 86 for Rn).
:::

::: example Worked example 6.3
**Problem.** Calculate the EAN of the metal in (a) [Fe(CN)₆]⁴⁻,
(b) [Co(NH₃)₆]³⁺, (c) [Ni(CO)₄] and (d) [Cu(NH₃)₄]²⁺. State which obey
Sidgwick's rule. ($Z$: Fe = 26, Co = 27, Ni = 28, Cu = 29.)

**Solution.**

(a) Fe is +2 with coordination number 6:
$\text{EAN} = 26 - 2 + 2(6) = 24 + 12 = 36$ — krypton. Stable.

(b) Co is +3 with coordination number 6:
$\text{EAN} = 27 - 3 + 2(6) = 24 + 12 = 36$ — krypton. Stable.

(c) Ni is 0 with coordination number 4:
$\text{EAN} = 28 - 0 + 2(4) = 28 + 8 = 36$ — krypton. Stable.

(d) Cu is +2 with coordination number 4:
$\text{EAN} = 29 - 2 + 2(4) = 27 + 8 = 35$ — not a noble-gas number, yet
[Cu(NH₃)₄]²⁺ is perfectly stable. The EAN rule is a useful guide, not a law.
:::

**Double salts versus complex salts.** Both are made by crystallising two salts
together, but they behave quite differently in water.

| | Double salt | Complex salt |
|---|---|---|
| Example | Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O | Potassium ferrocyanide, K₄[Fe(CN)₆] |
| In solution | Splits completely into all its simple ions | Gives the complex ion, which stays intact |
| Ions given | Fe²⁺, NH₄⁺, SO₄²⁻ | K⁺ and [Fe(CN)₆]⁴⁻ |
| Test | Gives the normal tests for Fe²⁺ | Gives **no** test for Fe²⁺ |
| Exists | Only in the solid state | In the solid **and** in solution |

## 6.4 Shapes of complex ions

The shape follows from the coordination number and from the hybridisation the
metal ion adopts.

| CN | Hybridisation | Shape | Example |
|---|---|---|---|
| 2 | sp | Linear | [Ag(NH₃)₂]⁺, [CuCl₂]⁻ |
| 4 | sp³ | Tetrahedral | [NiCl₄]²⁻, [CoCl₄]²⁻, [Zn(NH₃)₄]²⁺ |
| 4 | dsp² | Square planar | [Ni(CN)₄]²⁻, [PtCl₄]²⁻, [Cu(NH₃)₄]²⁺ |
| 6 | d²sp³ or sp³d² | Octahedral | [Fe(CN)₆]³⁻, [Co(NH₃)₆]³⁺, [Cr(H₂O)₆]³⁺ |

```figure caption="The four common geometries of complex ions. The same coordination number of four can give either a tetrahedral (sp³) or a square planar (dsp²) complex, depending on the metal ion and the ligand."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 4, figsize=(5.2, 2.4))
for ax in axes:
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.75, 1.45)
    ax.set_aspect('equal'); ax.axis('off')

def draw(ax, pts, title, sub, dashed=()):
    for i, p in enumerate(pts):
        ls = '--' if i in dashed else '-'
        ax.plot([0, p[0]], [0, p[1]], color=MUTED, lw=1.1, ls=ls)
        ax.plot([p[0]], [p[1]], 'o', color=SERIES[0], ms=7.0)
    ax.plot([0], [0], 'o', color=SERIES[1], ms=9.0)
    ax.set_title(title, fontsize=8.2, pad=2)
    ax.text(0, -1.62, sub, ha='center', va='center', fontsize=7.0, color=MUTED)

draw(axes[0], [(-1.0, 0), (1.0, 0)], 'Linear', 'sp,  CN 2')
t = [(0, 1.00), (-0.92, -0.34), (0.60, -0.60), (0.34, 0.27)]
draw(axes[1], t, 'Tetrahedral', 'sp³,  CN 4', dashed=(3,))
draw(axes[2], [(-1.0, 0), (1.0, 0), (0, 1.0), (0, -1.0)],
     'Square planar', 'dsp²,  CN 4')
oc = [(-1.05, 0), (1.05, 0), (0, 1.0), (0, -1.0), (-0.52, -0.42), (0.52, 0.42)]
draw(axes[3], oc, 'Octahedral', 'd²sp³,  CN 6', dashed=(4, 5))
fig.subplots_adjust(wspace=0.10)
```
## 6.5 d-orbitals in complex ions (crystal field theory, octahedral complex)

Valence-bond theory gives the shapes but says nothing about colour or about why
some complexes are strongly magnetic and others are not. **Crystal field theory
(CFT)** does both. Its postulates:

1. The metal–ligand bond is purely **electrostatic** — the ligands are treated
   as point negative charges (or as the negative end of dipoles).
2. In a free gaseous metal ion the five d orbitals are **degenerate** (equal in
   energy).
3. When ligands approach, they repel the d electrons. Orbitals that point
   **directly at** the ligands are raised in energy more than those that point
   **between** them, so the degeneracy is lifted.

In an **octahedral** field the six ligands approach along the $x$, $y$ and $z$
axes. The $d_{z^{2}}$ and $d_{x^{2}-y^{2}}$ orbitals point straight at them and
are raised; the $d_{xy}$, $d_{yz}$ and $d_{zx}$ orbitals point between the axes
and are lowered.

```figure caption="Crystal field splitting. Left: in an octahedral field the $e_g$ pair is raised by $0.6\\Delta_o$ and the $t_{2g}$ trio lowered by $0.4\\Delta_o$ about the barycentre. Right: in a tetrahedral field the order is inverted and the gap is smaller, $\\Delta_t = \\frac{4}{9}\\Delta_o$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 3.2))
ax.set_xlim(0, 10); ax.set_ylim(-1.05, 1.35); ax.axis('off')

def lev(x0, x1, y, col=INK, lw=2.0):
    ax.plot([x0, x1], [y, y], color=col, lw=lw, solid_capstyle='butt')

# free ion reference level
lev(0.20, 1.30, 0.0, MUTED)
ax.text(0.75, -0.26, 'free ion\n(degenerate)', ha='center', va='top',
        fontsize=7.6, color=MUTED)

# ---- octahedral ----
ax.plot([1.55, 4.55], [0, 0], color=MUTED, lw=0.8, ls=':')
for x0 in (2.30, 3.15):
    lev(x0, x0 + 0.62, 0.60, SERIES[1])
for x0 in (1.75, 2.60, 3.45):
    lev(x0, x0 + 0.62, -0.40, SERIES[0])
ax.annotate('', xy=(4.75, 0.60), xytext=(4.75, -0.40),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.2,
                            mutation_scale=9))
ax.text(4.90, 0.10, 'Δ$_o$', fontsize=9.0, color=INK, va='center')
ax.text(3.90, 0.70, '$e_g$', fontsize=8.6, color=SERIES[1])
ax.text(4.20, -0.31, '$t_{2g}$', fontsize=8.6, color=SERIES[0])
ax.text(2.55, 0.88, 'd$_{z^2}$ , d$_{x^2-y^2}$', fontsize=7.4, color=SERIES[1],
        ha='center')
ax.text(2.55, -0.62, 'd$_{xy}$ , d$_{yz}$ , d$_{zx}$', fontsize=7.4,
        color=SERIES[0], ha='center')
ax.text(2.90, 1.16, 'Octahedral field', fontsize=8.8, color=INK, ha='center')
ax.text(5.22, 0.60, '+0.6Δ$_o$', fontsize=7.2, color=SERIES[1], va='center')
ax.text(5.22, -0.40, '−0.4Δ$_o$', fontsize=7.2, color=SERIES[0], va='center')

# ---- tetrahedral ----
ax.plot([6.55, 9.55], [0, 0], color=MUTED, lw=0.8, ls=':')
for x0 in (6.75, 7.60, 8.45):
    lev(x0, x0 + 0.62, 0.28, SERIES[1])
for x0 in (7.30, 8.15):
    lev(x0, x0 + 0.62, -0.19, SERIES[0])
ax.annotate('', xy=(9.72, 0.28), xytext=(9.72, -0.19),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.2,
                            mutation_scale=9))
ax.text(9.84, 0.05, 'Δ$_t$', fontsize=9.0, color=INK, va='center')
ax.text(9.15, 0.36, '$t_2$', fontsize=8.6, color=SERIES[1])
ax.text(8.85, -0.30, '$e$', fontsize=8.6, color=SERIES[0])
ax.text(7.90, 0.56, 'd$_{xy}$ , d$_{yz}$ , d$_{zx}$', fontsize=7.4,
        color=SERIES[1], ha='center')
ax.text(7.90, -0.46, 'd$_{z^2}$ , d$_{x^2-y^2}$', fontsize=7.4, color=SERIES[0],
        ha='center')
ax.text(8.05, 1.16, 'Tetrahedral field', fontsize=8.8, color=INK, ha='center')
ax.text(5.60, -0.96, 'dotted line = barycentre (mean energy of the five d orbitals)',
        fontsize=7.2, color=MUTED, ha='center')
```
The energy gap $\Delta_{o}$ is the **crystal field splitting energy**. The three
$t_{2g}$ orbitals fall by $0.4\Delta_{o}$ and the two $e_{g}$ orbitals rise by
$0.6\Delta_{o}$, so the average energy (the *barycentre*) is unchanged.

**Crystal field stabilisation energy (CFSE)** is the net energy gained by
placing the d electrons in the split set:

$$ \text{CFSE} = \left(-0.4\,n_{t_{2g}} + 0.6\,n_{e_{g}}\right)\Delta_{o} $$

**High spin or low spin?** For d⁴ to d⁷ there are two ways to fill the orbitals,
and the winner depends on how $\Delta_{o}$ compares with the **pairing energy**
$P$ needed to force two electrons into one orbital:

- If $\Delta_{o} < P$ (**weak field** ligand), electrons spread out to give the
  maximum number of unpaired spins — **high spin**.
- If $\Delta_{o} > P$ (**strong field** ligand), the $t_{2g}$ set fills first —
  **low spin**.

::: memory Spectrochemical series — weak field to strong field
I⁻ < Br⁻ < Cl⁻ < F⁻ < OH⁻ < H₂O < NH₃ < en < NO₂⁻ < CN⁻ < CO

Halides are weak (small $\Delta$, high spin, pale colours); cyanide and carbonyl
are strong (large $\Delta$, low spin, deep colours).
:::

::: example Worked example 6.4
**Problem.** Both [Fe(H₂O)₆]²⁺ and [Fe(CN)₆]⁴⁻ contain Fe(II). Explain why the
first is strongly paramagnetic and the second is diamagnetic, and calculate the
CFSE and the spin-only magnetic moment of each.

**Solution.** Fe²⁺ is 3d⁶ in both complexes.

**[Fe(H₂O)₆]²⁺.** Water is a weak-field ligand, so $\Delta_{o} < P$ and the
configuration is high spin, $t_{2g}^{4}e_{g}^{2}$, with **4 unpaired**
electrons.

$$ \text{CFSE} = [-0.4(4) + 0.6(2)]\Delta_{o} = (-1.6 + 1.2)\Delta_{o} = -0.4\,\Delta_{o} $$
$$ \mu = \sqrt{n(n+2)} = \sqrt{4 \times 6} = \sqrt{24} = 4.90\ \text{BM} $$

**[Fe(CN)₆]⁴⁻.** Cyanide is a strong-field ligand, so $\Delta_{o} > P$ and all
six electrons pair up in the lower set, $t_{2g}^{6}e_{g}^{0}$, with **no
unpaired** electrons.

$$ \text{CFSE} = [-0.4(6) + 0.6(0)]\Delta_{o} = -2.4\,\Delta_{o} $$
$$ \mu = \sqrt{0(0+2)} = 0\ \text{BM (diamagnetic)} $$

The far larger CFSE is what pays for the pairing energy.
:::

In a **tetrahedral** field only four ligands approach, and they come between the
axes, so the pattern is inverted: the $e$ pair ($d_{z^2}$, $d_{x^2-y^2}$) lies
lower and the $t_2$ trio higher. The splitting is much smaller,
$\Delta_{t} = \frac{4}{9}\Delta_{o}$, because there are fewer ligands and none
of them points at an orbital. Consequently **tetrahedral complexes are almost
always high spin**.

## 6.6 Reasons for the colour of transition metal compounds

::: key Why transition metal compounds are coloured
The splitting $\Delta_{o}$ happens to be about 150–400 kJ mol⁻¹, which matches
the energy of **visible light**. A d electron absorbs a photon and jumps from
the $t_{2g}$ level to the $e_g$ level — a **d–d transition**. The colour we see
is the **complementary** colour of the light absorbed.
:::

| Light absorbed | Wavelength / nm | Colour seen |
|---|---|---|
| Violet | 400–430 | Yellow-green |
| Blue | 450–490 | Orange-yellow |
| Green | 490–560 | Purple / red |
| Yellow | 570–590 | Blue |
| Red | 620–750 | Blue-green |

```figure caption="Colours of some common aqueous transition-metal species. Sc³⁺ (3d⁰) and Zn²⁺ (3d¹⁰) have no possible d–d transition and are colourless; the permanganate and dichromate colours come from charge transfer, not from d–d jumps."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
items = [('Sc³⁺', '3d⁰', '#f4f6f9', 'colourless'),
         ('Ti³⁺', '3d¹', '#7b4fa0', 'purple'),
         ('V³⁺', '3d²', '#3f8f5f', 'green'),
         ('Cr³⁺', '3d³', '#3c7d52', 'green'),
         ('Mn²⁺', '3d⁵', '#f0cbd8', 'pale pink'),
         ('Fe²⁺', '3d⁶', '#b3d6ab', 'pale green'),
         ('Fe³⁺', '3d⁵', '#d8a13a', 'yellow-brown'),
         ('Co²⁺', '3d⁷', '#e8899f', 'pink'),
         ('Ni²⁺', '3d⁸', '#4f9e6a', 'green'),
         ('Cu²⁺', '3d⁹', '#2b7fd4', 'blue'),
         ('Zn²⁺', '3d¹⁰', '#f4f6f9', 'colourless'),
         ('MnO₄⁻', '3d⁰', '#6b2d8f', 'purple'),
         ('Cr₂O₇²⁻', '3d⁰', '#e07b1f', 'orange'),
         ('CrO₄²⁻', '3d⁰', '#f2c53d', 'yellow')]
fig, ax = plt.subplots(figsize=(5.2, 3.0))
ncol = 7
for i, (ion, cfg, col, name) in enumerate(items):
    r, c = divmod(i, ncol)
    x = c * 1.0; y = -r * 1.0
    ax.add_patch(Rectangle((x + 0.08, y + 0.30), 0.84, 0.44, facecolor=col,
                           edgecolor='#9aa2ae', lw=0.7))
    ax.text(x + 0.50, y + 0.84, ion, ha='center', fontsize=8.2, color=INK)
    ax.text(x + 0.50, y + 0.17, cfg, ha='center', fontsize=7.0, color=MUTED)
    ax.text(x + 0.50, y - 0.02, name, ha='center', fontsize=6.6, color=MUTED)
ax.set_xlim(-0.05, ncol); ax.set_ylim(-1.25, 1.05)
ax.axis('off')
```

Three consequences:

1. **d⁰ and d¹⁰ ions are colourless** — Sc³⁺, Ti⁴⁺, Zn²⁺, Cu⁺, Ag⁺ — because
   there is either no d electron to promote or no vacancy to promote it into.
2. **The ligand changes the colour**, because it changes $\Delta_{o}$.
   [Cu(H₂O)₄]²⁺ is pale blue while [Cu(NH₃)₄]²⁺ is deep royal blue; ammonia is
   higher in the spectrochemical series, so it absorbs at shorter wavelength.
3. **The oxidation state changes the colour** — Fe²⁺ is pale green, Fe³⁺
   yellow-brown; Cr³⁺ green, Cr₂O₇²⁻ orange.

::: caution MnO₄⁻ and Cr₂O₇²⁻ are not coloured by d–d transitions
In permanganate the manganese is Mn(VII), which is 3d⁰ — there are no d
electrons at all, so a d–d jump is impossible. The intense purple comes from
**charge transfer**: a photon shifts an electron from an oxygen lone pair on to
the metal. That is why the colour is so much more intense than a normal d–d
colour.
:::

::: example Worked example 6.5
**Problem.** The complex [Ti(H₂O)₆]³⁺ absorbs most strongly at 500 nm.
Calculate $\Delta_{o}$ in kJ mol⁻¹ and explain the observed violet colour.
($h = 6.626\times10^{-34}$ J s, $c = 3.0\times10^{8}$ m s⁻¹,
$N_A = 6.022\times10^{23}$ mol⁻¹.)

**Solution.** The energy of one absorbed photon is

$$ E = \frac{hc}{\lambda} = \frac{(6.626\times10^{-34})(3.0\times10^{8})}{500\times10^{-9}} = 3.976\times10^{-19}\ \text{J} $$

Per mole,

$$ \Delta_{o} = E \times N_A = (3.976\times10^{-19})(6.022\times10^{23}) = 2.394\times10^{5}\ \text{J mol}^{-1} $$
$$ \Delta_{o} = 239\ \text{kJ mol}^{-1} $$

Ti³⁺ is 3d¹, so the single electron is promoted $t_{2g}^{1} \rightarrow e_{g}^{1}$
by absorbing green light at 500 nm. The transmitted light is the complement of
green, so the solution looks **violet-purple**.
:::

## 6.7 Catalytic properties of transition metals

Transition metals and their compounds catalyse an enormous number of reactions.
Two mechanisms account for this:

1. **Variable oxidation state.** The metal can hand electrons to one reactant
   and take them from another, forming an unstable intermediate that provides a
   lower-energy path. Fe³⁺ catalysing the reaction of iodide with persulphate is
   the classic example: Fe³⁺ oxidises I⁻ and is then re-oxidised by S₂O₈²⁻.
2. **Surface adsorption.** A metal surface has partly filled d orbitals and
   unsatisfied valencies, so it **adsorbs** gaseous reactants, holds them close
   together in the right orientation, and weakens their bonds. This is
   heterogeneous catalysis; iron in the Haber process works this way.

| Catalyst | Process | Reaction |
|---|---|---|
| Fe with Mo promoter | Haber process | N₂ + 3H₂ ⇌ 2NH₃ |
| V₂O₅ | Contact process | 2SO₂ + O₂ ⇌ 2SO₃ |
| Pt / Rh gauze | Ostwald process | 4NH₃ + 5O₂ → 4NO + 6H₂O |
| Ni (finely divided) | Hydrogenation of oils to vanaspati ghee | vegetable oil + H₂ → fat |
| MnO₂ | Decomposition of potassium chlorate | 2KClO₃ → 2KCl + 3O₂ |
| TiCl₄ + Al(C₂H₅)₃ | Ziegler–Natta polymerisation | n CH₂=CH₂ → polythene |
| Cu | Dehydrogenation of ethanol | C₂H₅OH → CH₃CHO + H₂ |

Living systems use the same chemistry: the iron in haemoglobin carries oxygen,
cobalt sits at the centre of vitamin B₁₂, and zinc is the active site of
carbonic anhydrase.

## Chapter summary

- A transition element has a partially filled d subshell in the atom or in a
  common ion. Zn (3d¹⁰4s², Zn²⁺ = 3d¹⁰) is therefore not typical. Cr and Cu
  have 4s¹ configurations because half-filled and full d subshells are stable.
- Characteristic properties: hardness, high melting point and density, variable
  oxidation states, coloured and paramagnetic ions, complex formation,
  catalysis, alloys and interstitial compounds.
- Variable oxidation states arise because 3d and 4s are close in energy. The
  maximum state rises to +7 at Mn, then falls; the +2 state dominates on the
  right.
- A **complex ion** is a central metal ion bonded to ligands by coordinate
  bonds. $\text{EAN} = Z - (\text{oxidation state}) + 2(\text{CN})$.
- Shapes: CN 2 linear (sp); CN 4 tetrahedral (sp³) or square planar (dsp²);
  CN 6 octahedral (d²sp³).
- **CFT:** in an octahedral field $e_g$ rises by $0.6\Delta_{o}$ and $t_{2g}$
  falls by $0.4\Delta_{o}$;
  $\text{CFSE} = (-0.4n_{t_{2g}} + 0.6n_{e_{g}})\Delta_{o}$. Weak field
  ($\Delta_{o} < P$) gives high spin, strong field gives low spin. In a
  tetrahedral field the order inverts and $\Delta_{t} = \frac{4}{9}\Delta_{o}$.
- Colour comes from **d–d transitions** whose energy matches visible light;
  d⁰ and d¹⁰ ions are colourless. MnO₄⁻ and Cr₂O₇²⁻ are coloured by charge
  transfer.
- Spin-only magnetic moment $\mu = \sqrt{n(n+2)}$ BM.
- Catalysis works through variable oxidation states (homogeneous) or surface
  adsorption (heterogeneous).

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is **not** regarded as a typical transition element? <span class="marks">[1]</span>
   (a) Sc (b) Zn (c) Fe (d) Cr
2. The highest oxidation state shown by manganese is <span class="marks">[1]</span>
   (a) +2 (b) +4 (c) +6 (d) +7
3. Which aqueous ion is colourless? <span class="marks">[1]</span>
   (a) Cu²⁺ (b) Ni²⁺ (c) Zn²⁺ (d) Co²⁺
4. The crystal field stabilisation energy of an octahedral d¹ complex is <span class="marks">[1]</span>
   (a) $-0.4\Delta_{o}$ (b) $-0.6\Delta_{o}$ (c) $+0.4\Delta_{o}$ (d) $-1.2\Delta_{o}$
5. The oxidation state of iron in K₃[Fe(CN)₆] is <span class="marks">[1]</span>
   (a) +2 (b) +3 (c) +4 (d) 0
6. The coordination number and shape of [Ni(CN)₄]²⁻ are <span class="marks">[1]</span>
   (a) 4, tetrahedral (b) 4, square planar (c) 6, octahedral (d) 2, linear

::: note Answers to Group A
**1.** (b) — zinc has a complete 3d¹⁰ subshell in both the atom and the Zn²⁺ ion.

**2.** (d) — all five 3d and both 4s electrons are used, as in MnO₄⁻.

**3.** (c) — Zn²⁺ is 3d¹⁰, so no d–d transition is possible.

**4.** (a) — the single electron occupies a $t_{2g}$ orbital, which lies $0.4\Delta_{o}$ below the barycentre.

**5.** (b) — $x + 6(-1) = -3$, so $x = +3$.

**6.** (b) — CN⁻ is a strong-field ligand, forcing dsp² hybridisation.
:::

**Group B — Short answer (5 marks each)**

1. Define a transition element. State any five characteristic properties of
   transition metals and explain why they show variable oxidation states. <span class="marks">[5]</span>
2. Why are most transition metal compounds coloured? Explain why Sc³⁺ and Zn²⁺
   are colourless, and why the colour of MnO₄⁻ has a different origin. <span class="marks">[5]</span>
3. Define ligand, coordination number and effective atomic number. Calculate the
   EAN of the metal in [Cu(NH₃)₄]²⁺ and [Fe(CN)₆]³⁻.
   ($Z$: Cu = 29, Fe = 26) <span class="marks">[5]</span>
4. Distinguish between a double salt and a complex salt, using Mohr's salt and
   potassium ferrocyanide as examples. <span class="marks">[5]</span>
5. State the postulates of crystal field theory. Draw the splitting of the d
   orbitals in an octahedral field and calculate the spin-only magnetic moment
   of [Mn(H₂O)₆]²⁺. <span class="marks">[5]</span>
6. Why do transition metals and their compounds act as good catalysts? Give any
   four industrial catalysts with the process in which each is used. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** A **ligand** is a molecule or ion with at least one lone pair that it
donates to a central metal ion to form a coordinate bond. The **coordination
number** is the number of such bonds. The **EAN** is
$Z - (\text{oxidation state}) + 2(\text{CN})$.

For [Cu(NH₃)₄]²⁺: $\text{EAN} = 29 - 2 + 2(4) = 35$.

For [Fe(CN)₆]³⁻: $\text{EAN} = 26 - 3 + 2(6) = 35$.

**5.** Mn²⁺ is 3d⁵. Water is a weak-field ligand, so the complex is high spin,
$t_{2g}^{3}e_{g}^{2}$, with $n = 5$ unpaired electrons:

$$ \mu = \sqrt{n(n+2)} = \sqrt{5 \times 7} = \sqrt{35} = 5.92\ \text{BM} $$

(The CFSE is $[-0.4(3) + 0.6(2)]\Delta_{o} = 0$, which is why high-spin d⁵ ions
are so pale.)
:::

**Group C — Long answer (8 marks each)**

1. (a) Discuss the variation of oxidation states across the 3d series and
   explain why the +2 state becomes increasingly stable towards the right-hand
   end. <span class="marks">[4]</span>
   (b) Give the hybridisation, shape and coordination number of
   [Ag(NH₃)₂]⁺, [NiCl₄]²⁻, [Ni(CN)₄]²⁻ and [Co(NH₃)₆]³⁺. <span class="marks">[4]</span>
2. (a) State the postulates of crystal field theory. Explain the splitting of
   the d orbitals in octahedral and in tetrahedral fields, and state the
   relation between $\Delta_{t}$ and $\Delta_{o}$. <span class="marks">[5]</span>
   (b) [Fe(H₂O)₆]²⁺ has four unpaired electrons whereas [Fe(CN)₆]⁴⁻ has none,
   although both contain Fe(II). Explain, and calculate the CFSE of each. <span class="marks">[3]</span>

::: note Answers to Group C
**1.(a)** The lowest common state is +2 (loss of the two 4s electrons) and the
highest rises steadily from +3 at Sc to +7 at Mn, where all five 3d electrons
plus both 4s electrons can be used. Beyond Mn the nuclear charge keeps growing
while the d electrons are added to the same shell, so the effective nuclear
charge rises and the ionisation energies climb steeply. The 3d electrons are
then held too tightly to be removed, and only the 4s pair is easily lost —
hence Fe (+2, +3), Co (+2), Ni (+2), Cu (+1, +2), Zn (+2 only).

**1.(b)**

| Complex | CN | Hybridisation | Shape |
|---|---|---|---|
| [Ag(NH₃)₂]⁺ | 2 | sp | Linear |
| [NiCl₄]²⁻ | 4 | sp³ | Tetrahedral |
| [Ni(CN)₄]²⁻ | 4 | dsp² | Square planar |
| [Co(NH₃)₆]³⁺ | 6 | d²sp³ | Octahedral |

**2.(b)** Fe²⁺ is 3d⁶ in both. H₂O is a weak-field ligand, so
$\Delta_{o} < P$ and the electrons spread out over all five orbitals,
$t_{2g}^{4}e_{g}^{2}$, leaving four unpaired: high spin, and
$\text{CFSE} = [-0.4(4) + 0.6(2)]\Delta_{o} = -0.4\Delta_{o}$.

CN⁻ is a strong-field ligand, so $\Delta_{o} > P$; it costs less energy to pair
the electrons than to promote them, giving $t_{2g}^{6}e_{g}^{0}$ with no
unpaired electrons: low spin, diamagnetic, and
$\text{CFSE} = -0.4(6)\Delta_{o} = -2.4\Delta_{o}$.
:::

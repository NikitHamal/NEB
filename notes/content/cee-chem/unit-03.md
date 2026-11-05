---
subject: Chemistry
grade: CEE
unit: 3
title: Classification of Elements and Periodicity
hours: 1
area: Physical Chemistry
---

Periodicity carries about **one question** in the paper (our estimate from the MEC topic
list), but its trends are used again in bonding, s-block, non-metal and transition-metal
questions. The question is almost always one of four kinds: locate an element (period,
group, block) from its atomic number, put a set of atoms or ions in order of a property,
explain an exception (Be > B, N > O, Cl > F), or read successive ionisation energies.
Everything follows from two ideas — effective nuclear charge and the number of shells.

::: key What the paper asks from this chapter
- Modern periodic law (Moseley): properties are periodic functions of **atomic number**.
- Period = highest shell number; block = subshell receiving the last electron; group from the valence electrons (s: ns; p: 10 + ns + np; d: ns + (n − 1)d).
- Isoelectronic species: same electrons, so the radius falls as the nuclear charge rises (N³⁻ > O²⁻ > F⁻ > Na⁺ > Mg²⁺ > Al³⁺).
- Across a period: size ↓, ionisation energy ↑, electronegativity ↑, electron affinity ↑, metallic character ↓; down a group the reverse.
- Exceptions: IE Be > B and N > O (also Mg > Al, P > S); EA Cl > F and S > O; Ga is smaller than Al; Zr ≈ Hf (lanthanoid contraction).
- Superlatives: He highest IE, Cs lowest (stable elements); F most electronegative (4.0); Cl highest electron affinity.
:::

## 3.1 Modern periodic law and table; s, p, d and f blocks; isoelectronic species

### From Mendeleev to Moseley

**Mendeleev (1869)** arranged the elements by increasing atomic mass and grouped elements
with similar properties. He left gaps and predicted the properties of undiscovered
elements — eka-boron (Sc), eka-aluminium (Ga) and eka-silicon (Ge). But he had to reverse
some pairs to keep the chemistry right (Te 127.6 before I 126.9; Co before Ni; and, once
argon was discovered in 1894, Ar 39.9 before K 39.1), and isotopes had no place.
**Moseley (1913)** found that the square root of the frequency of an element's
characteristic X-rays varies linearly with its atomic number, $\sqrt{\nu} = a(Z - b)$. Ordered by Z, every reversal disappears.

::: definition Modern periodic law
The physical and chemical properties of the elements are **periodic functions of their
atomic numbers**.
:::

The cause of periodicity is the **repetition of similar outer electronic configurations**
after intervals of 2, 8, 8, 18, 18, 32 and 32 elements.

### The long form of the table

The modern table has **7 periods** and **18 groups** (IUPAC numbering 1–18) and holds 118
elements. The period number is the principal quantum number of the outermost shell.

| Period | Subshells filled | Elements | Description |
|---|---|---|---|
| 1 | 1s | 2 | very short |
| 2, 3 | ns np | 8 each | short |
| 4, 5 | ns (n − 1)d np | 18 each | long |
| 6, 7 | ns (n − 2)f (n − 1)d np | 32 each | very long |

| Group | Family | Valence configuration |
|---|---|---|
| 1 | alkali metals (H is placed here but is not one) | ns¹ |
| 2 | alkaline earth metals | ns² |
| 3–12 | transition metals (Zn, Cd, Hg of group 12 are d-block but not true transition metals: full d¹⁰) | (n − 1)d¹⁻¹⁰ ns⁰⁻² |
| 13 | boron family | ns² np¹ |
| 14 | carbon family | ns² np² |
| 15 | nitrogen family (pnictogens) | ns² np³ |
| 16 | oxygen family (chalcogens) | ns² np⁴ |
| 17 | halogens | ns² np⁵ |
| 18 | noble gases | ns² np⁶ (He 1s²) |

### The four blocks

| Block | Last (differentiating) electron enters | General configuration | Position | Character |
|---|---|---|---|---|
| s | ns | ns¹⁻² | groups 1, 2 (and He) | reactive metals, low IE, fixed valency, ionic compounds, basic oxides |
| p | np | ns² np¹⁻⁶ | groups 13–18 | metals, metalloids and non-metals; most variable oxidation states |
| d | (n − 1)d | (n − 1)d¹⁻¹⁰ ns⁰⁻² | groups 3–12, periods 4–7 | transition metals: variable oxidation states, coloured ions, complexes, catalysts |
| f | (n − 2)f | (n − 2)f¹⁻¹⁴ (n − 1)d⁰⁻¹ ns² | two rows below the table | inner transition: lanthanoids (4f, Z = 58–71) and actinoids (5f, Z = 90–103, all radioactive) |

The s- and p-block elements together are the **representative (main-group) elements**
(some older books leave out the noble gases). **Metalloids** (B, Si, Ge, As, Sb, Te) lie on the diagonal staircase
between metals and non-metals. **Helium** is 1s² — an s-block configuration — but sits in
group 18 because its shell is complete and it is inert like the other noble gases.

```figure caption="Layout of the long-form periodic table by blocks. Helium (dark cell) is s-block by configuration but sits over group 18. The f-block rows belong in group 3 of periods 6 and 7 and are drawn below to keep the table narrow."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2, 3.3))
CS, CP, CD, CF = '#cfe0f3', '#f6d5cf', '#d8ecd2', '#ece0f2'
def cell(col, row, fc, ec='white'):
    ax.add_patch(Rectangle((col-1, -row), 0.96, 0.92, fc=fc, ec=ec, lw=0.6))
for r in range(1, 8):
    if r == 1:
        cell(1, 1, CS); cell(18, 1, '#7fa7d6')
        continue
    for c in (1, 2):
        cell(c, r, CS)
    for c in range(13, 19):
        cell(c, r, CP)
    if r >= 4:
        for c in range(3, 13):
            cell(c, r, CD)
for r in (8.6, 9.6):
    for k in range(14):
        ax.add_patch(Rectangle((2.5+k, -r), 0.96, 0.92, fc=CF, ec='white', lw=0.6))
for c in range(1, 19):
    ax.text(c-0.52, 0.55 if c in (1, 18) else (-0.45 if c in (2, 13, 14, 15, 16, 17) else -2.45),
            str(c), ha='center', va='center', fontsize=7.2, color=MUTED)
for r in range(1, 8):
    ax.text(-0.45, -r+0.46, str(r), ha='right', va='center', fontsize=7.4, color=MUTED)
ax.text(-1.25, -3.5, 'period', rotation=90, ha='center', va='center', fontsize=7.6, color=MUTED)
ax.text(0.98, -5.0, 's', ha='center', va='center', fontsize=10, color=INK)
ax.text(7.48, -5.6, 'd-block\n(transition)', ha='center', va='center', fontsize=8.6, color=INK)
ax.text(15.0, -4.6, 'p-block', ha='center', va='center', fontsize=9, color=INK)
ax.text(9.48, -9.1, 'f-block: lanthanoids (4f) and actinoids (5f)', ha='center', va='center', fontsize=8.2, color=INK)
ax.text(17.48, -0.54, 'He', ha='center', va='center', fontsize=7.4, color='white')
ax.text(0.48, -0.54, 'H', ha='center', va='center', fontsize=7.4, color=INK)
ax.set_xlim(-1.6, 18.2); ax.set_ylim(-10.0, 1.1)
ax.set_aspect('equal'); ax.axis('off')
```

### Locating an element from its atomic number

Write the configuration; the **period** is the highest n; the **block** is the subshell
that received the last electron; the **group** is the number of ns electrons (s-block),
10 + the ns and np electrons (p-block), or the ns + (n − 1)d electrons (d-block). All
f-block elements belong to group 3.

**Noble-gas shortcut.** Subtract the atomic number of the previous noble gas
(2, 10, 18, 36, 54, 86). The remainder is the element's place in the next period. In
periods 4 and 5 that place *is* the group number. In periods 6 and 7 places 4–17 are the
f-block, and from place 18 onwards subtract 14 to get the group.

::: example Period, group and block in ten seconds
**Problem.** Locate the elements with Z = 33, 26 and 82.

**Solution.** Z = 33: 33 − 18 = 15th place in period 4 → **period 4, group 15, p-block**
(arsenic, [Ar] 3d¹⁰ 4s² 4p³). Z = 26: [Ar] 3d⁶ 4s², 6 + 2 = 8 → **period 4, group 8,
d-block** (iron). Z = 82: 82 − 54 = 28th place in period 6; 28 − 14 = 14 → **period 6,
group 14, p-block** (lead).
:::

**IUPAC names for Z > 100.** Read the digits with the roots 0 nil, 1 un, 2 bi, 3 tri,
4 quad, 5 pent, 6 hex, 7 sept, 8 oct, 9 enn, and add **-ium**; the symbol is the first
letters of the three roots. Z = 104 → un-nil-quad-ium, **unnilquadium (Unq)** (now
rutherfordium); Z = 114 → **ununquadium (Uuq)** (now flerovium); Z = 120 →
**unbinilium (Ubn)**. (The final "i" of bi and tri is dropped before -ium.)

### Isoelectronic species

::: definition Isoelectronic species
Atoms, ions or molecules that contain the **same number of electrons** (usually with the
same configuration) are isoelectronic.
:::

| Electrons | Isoelectronic set |
|---|---|
| 2 | H⁻, He, Li⁺, Be²⁺ |
| 10 | N³⁻, O²⁻, F⁻, Ne, Na⁺, Mg²⁺, Al³⁺; CH₄, NH₃, H₂O, HF, NH₄⁺, H₃O⁺, OH⁻ |
| 14 | N₂, CO, CN⁻, NO⁺, C₂²⁻ |
| 18 | P³⁻, S²⁻, Cl⁻, Ar, K⁺, Ca²⁺; HCl, H₂S, PH₃, SiH₄ |
| 22 | CO₂, N₂O, N₃⁻, NO₂⁺ |

In an isoelectronic series the same number of electrons is held by an increasing number
of protons, so the **radius decreases as Z increases**: N³⁻ > O²⁻ > F⁻ > Na⁺ > Mg²⁺ >
Al³⁺ and S²⁻ > Cl⁻ > K⁺ > Ca²⁺. Quick rule: the more negative the charge, the larger the
species.

## 3.2 Periodic trends: size, ionisation energy, electronegativity, electron affinity and metallic character

### The two causes behind every trend

**Effective nuclear charge**, $Z_{eff} = Z - \sigma$, is the nuclear charge actually felt
by an outer electron after the inner electrons have **screened** (shielded) part of it
(σ is the screening constant). Screening power falls in the order s > p > d > f.

- **Across a period** Z rises by one at each step, but the new electron goes into the same
  shell and screens poorly, so Z_eff rises and the outer electrons are pulled closer.
- **Down a group** a new shell is added each period; the larger distance and extra
  screening outweigh the larger nuclear charge.

### Atomic radius

Atomic radius is measured as the **covalent radius** (half the distance between two
identical atoms joined by a single bond), the **metallic radius** (half the distance
between neighbouring atoms in a metal) or the **van der Waals radius** (half the distance
of closest approach of non-bonded atoms). For one element, van der Waals radius >
covalent radius (Cl: 180 pm against 99 pm). Noble gases have only van der Waals radii, so
they cannot be compared fairly with the rest of their period.

| Period 3 | Na | Mg | Al | Si | P | S | Cl |
|---|---|---|---|---|---|---|---|
| Atomic radius (pm) | 186 | 160 | 143 | 117 | 110 | 104 | 99 |
| IE₁ (kJ mol⁻¹) | 496 | 738 | 578 | 787 | 1012 | 1000 | 1251 |
| Electronegativity | 0.9 | 1.2 | 1.5 | 1.8 | 2.1 | 2.5 | 3.0 |

Down group 1 the radius grows: Li 152, Na 186, K 227, Rb 248, Cs 265 pm. Two exceptions
are popular:

- **Ga (135 pm) is smaller than Al (143 pm):** the ten 3d electrons added before gallium
  shield the nucleus poorly, so Z_eff is higher than expected.
- **Lanthanoid contraction:** across the fourteen 4f elements the radius falls steadily,
  because 4f electrons shield very poorly. The 5d metals after them are therefore almost
  the same size as the 4d metals above them — **Zr (160 pm) ≈ Hf (159 pm)** — and so are
  chemically very similar.

### Ionic radius

| Rule | Example |
|---|---|
| A cation is smaller than its atom (fewer electrons, often one shell fewer, same nuclear charge) | Na⁺ is about half the size of Na |
| An anion is larger than its atom (more electron repulsion, same nuclear charge) | Cl 99 pm, Cl⁻ 181 pm |
| The higher the positive charge, the smaller the ion | Fe > Fe²⁺ > Fe³⁺; Pb²⁺ > Pb⁴⁺ |
| Isoelectronic ions: higher Z, smaller ion | O²⁻ > F⁻ > Na⁺ > Mg²⁺ |
| Down a group ions grow | Li⁺ < Na⁺ < K⁺ < Rb⁺ < Cs⁺; F⁻ < Cl⁻ < Br⁻ < I⁻ |

### Ionisation energy

::: definition Ionisation energy (ionisation enthalpy)
The **first ionisation energy** is the minimum energy needed to remove the most loosely
held electron from an isolated gaseous atom in its ground state:
M(g) → M⁺(g) + e⁻. It is quoted in kJ mol⁻¹ or in eV per atom
(1 eV per atom = 96.5 kJ mol⁻¹).
:::

**It rises** with nuclear charge and with a stable (half-filled or filled) configuration;
**it falls** with atomic size and with screening; and an s electron (more penetrating) is
harder to remove than a p electron of the same shell. Hence IE increases across a period
and decreases down a group: He (2372 kJ mol⁻¹) is the highest of all; Cs (376) is the
lowest among the stable elements.

```figure caption="First ionisation energies for Z = 1 to 38. Peaks at the noble gases, troughs at the alkali metals; the small dips at B and Al (a p electron) and at O and S (a paired p electron) are the textbook exceptions. Across the 3d metals the values change little."
import numpy as np, matplotlib.pyplot as plt
ie = [1312,2372,520,899,801,1086,1402,1314,1681,2081,496,738,578,787,1012,1000,1251,1521,
      419,590,633,659,651,653,717,762,760,737,746,906,579,762,947,941,1140,1351,403,550]
Z = np.arange(1, len(ie)+1)
fig, ax = plt.subplots(figsize=(5.2, 3.0))
ax.plot(Z, ie, '-', color=ACCENT, lw=1.3, zorder=2)
ax.plot(Z, ie, 'o', color=ACCENT, ms=3.0, zorder=3)
lab = {2:('He',(4,2)), 10:('Ne',(4,2)), 18:('Ar',(4,2)), 36:('Kr',(-6,6)),
       3:('Li',(-2,-12)), 11:('Na',(-4,-12)), 19:('K',(-3,-12)), 37:('Rb',(-4,-12)),
       5:('B',(2,-12)), 8:('O',(4,-10)), 13:('Al',(2,-12)), 16:('S',(4,-10)), 7:('N',(-12,2))}
for z, (s, off) in lab.items():
    c = SERIES[1] if s in ('B','O','Al','S','N') else INK
    ax.annotate(s, (z, ie[z-1]), textcoords='offset points', xytext=off, fontsize=8, color=c)
ax.text(25.5, 1000, '3d metals', ha='center', fontsize=8, color=MUTED)
ax.set_xlabel('atomic number Z'); ax.set_ylabel('IE$_1$ (kJ mol$^{-1}$)')
ax.set_xlim(0, 39.5); ax.set_ylim(250, 2600)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=0.45)
```

::: caution The two dips everyone is asked about
- **Be (899) > B (801)** and **Mg > Al:** boron's electron is a 2p electron, higher in
  energy and shielded by the filled 2s² pair, so it is easier to remove.
- **N (1402) > O (1314)** and **P > S:** nitrogen's 2p³ is half-filled and extra stable;
  in oxygen the fourth 2p electron is paired, and repulsion between the paired electrons
  makes it easier to remove.
So across period 2 the order is Li < B < Be < C < O < N < F < Ne — not a smooth rise.
:::

**Successive ionisation energies** always increase (IE₁ < IE₂ < IE₃ …), because each
electron is removed from an ion that is more positive. A **very large jump** means the
next electron has to come from a complete inner shell — so the number of electrons
removed before the jump is the number of valence electrons.

::: example Reading successive ionisation energies
**Problem.** An element has IE₁ to IE₄ = 578, 1817, 2745 and 11 577 kJ mol⁻¹. To which
group does it belong?

**Solution.** The ratios IE₂/IE₁ ≈ 3.1 and IE₃/IE₂ ≈ 1.5 are modest, but IE₄/IE₃ ≈ 4.2
is the big jump: three electrons come off easily, the fourth comes from a noble-gas core.
Three valence electrons → **group 13** (it is aluminium).
:::

### Electron affinity (electron gain enthalpy)

::: definition Electron affinity
**Electron affinity** is the energy released when an electron is added to an isolated
gaseous atom in its ground state: X(g) + e⁻ → X⁻(g). The **electron gain enthalpy**
ΔegH is the same quantity with the opposite sign: a large electron affinity means a large
negative ΔegH.
:::

Electron affinity generally **increases across a period** (higher Z_eff, smaller atom)
and **decreases down a group**. The exceptions are examined more often than the rule:

| Fact | Reason |
|---|---|
| Cl (349) > F (328) > Br (325) > I (295) kJ mol⁻¹ | F is so small that its compact 2p shell repels the incoming electron strongly |
| S (200) > O (141) | the same small-size effect in oxygen |
| Noble gases: ΔegH positive (energy absorbed) | the electron would have to enter a new shell |
| Be, Mg and N: almost zero or slightly negative EA | filled ns² or half-filled np³ subshells are stable |
| Every second EA is negative (O⁻ + e⁻ → O²⁻ absorbs energy) | the electron is added to an ion that is already negative |

Halogens have the highest electron affinities of all, because one electron completes
their octet; **chlorine has the highest of all elements**.

### Electronegativity

::: definition Electronegativity
**Electronegativity** is the tendency of an atom **in a molecule** to attract the shared
pair of electrons towards itself. It is a relative number with **no unit**. On Pauling's
scale fluorine = 4.0. Mulliken defined it as the average of the ionisation energy and the
electron affinity.
:::

It increases across a period and decreases down a group: **F 4.0 > O 3.5 > N 3.0 ≈ Cl 3.0
> Br 2.8 > C 2.5 ≈ S 2.5 ≈ I 2.5 > H 2.1**; the least electronegative are Cs and Fr (0.7).
An atom's electronegativity rises with its oxidation state and with the s character of its
hybrid orbital (sp > sp² > sp³).

| | Electronegativity | Electron affinity |
|---|---|---|
| Refers to | an atom bonded in a molecule | an isolated gaseous atom |
| Nature | a relative tendency | an energy change |
| Unit | none (Pauling scale) | kJ mol⁻¹ or eV |
| Highest | F | Cl |

### Metallic character, oxides and the diagonal relationship

**Metallic character** (electropositivity) is the tendency of an atom to lose electrons.
It falls across a period and rises down a group, the opposite of ionisation energy. The
oxides follow it: across period 3, Na₂O and MgO are **basic**, Al₂O₃ is **amphoteric**
(it reacts with both acids and alkalis), and SiO₂ (weakly), P₄O₁₀, SO₃ and Cl₂O₇
(strongly) are **acidic**. Down a group the oxides and hydroxides become more basic
(Be(OH)₂ is amphoteric, Ba(OH)₂ a strong alkali). The **diagonal relationship** — Li with
Mg, Be with Al, B with Si — arises because the diagonal pairs have similar size-to-charge
ratios (polarising power).

| Property | Across a period → | Down a group ↓ |
|---|---|---|
| Atomic and ionic radius | decreases | increases |
| Ionisation energy | increases (dips at groups 13 and 16) | decreases |
| Electron affinity | increases (dips at groups 2, 15 and 18) | decreases (but Cl > F, S > O) |
| Electronegativity | increases | decreases |
| Metallic character, reducing power | decreases | increases |
| Non-metallic character, oxidising power | increases | decreases |
| Basic character of oxides | decreases | increases |

::: tip Ordering questions in one pass
Put the species on the periodic table in your head. For size, ionisation energy and
electronegativity, decide position first (period beats group: going down one shell changes
size more than moving one place across), then check the exceptions list — Be/B, N/O,
Mg/Al, P/S, Cl/F, Ga/Al. If two options differ only in one adjacent pair, that pair is
the exception the setter is testing.
:::

::: example Ranking ionic radii in an isoelectronic series
**Problem.** Arrange the isoelectronic ions $\text{N}^{3-},\text{O}^{2-},\text{F}^-,\text{Na}^+,\text{Mg}^{2+},\text{Al}^{3+}$ in order of decreasing ionic radius and justify the order.

**Solution.** All six ions contain $10\text{ e}^-$ ($1s^2 2s^2 2p^6$), while nuclear charge $Z$ rises from $7$ ($\text{N}^{3-}$) to $13$ ($\text{Al}^{3+}$). For isoelectronic species, radius $\propto 1/Z$, giving $\mathbf{\text{N}^{3-} > \text{O}^{2-} > \text{F}^- > \text{Na}^+ > \text{Mg}^{2+} > \text{Al}^{3+}}$.
:::

```photogrid label="3.1" cols="2" ratio="1.2" caption="Energy of a flame colour. (a) Heated alkali-metal atoms emit light when their outer electron falls back to a lower level. (b) The photon energy per mole is N h c / lambda: 178 kJ/mol for lithium (670.8 nm), 203 for sodium (589.0 nm) and 156 for potassium (766.5 nm). Each is only about a third to two-fifths of the first ionisation energy (520, 496 and 419 kJ/mol), because the flame excites the electron to a higher level but does not remove it. Ionisation energy falls down the group as the outer electron lies farther from the nucleus."
@ photo id="chem11/flame-colours" cap="Metal salts colour a flame: each metal emits its own wavelengths"
fit 1.2
focus 0.5 0.5
@ svg cap="Flame photon energy against first ionisation energy"
NA, h, c = 6.022e23, 6.626e-34, 2.998e8
E = lambda nm: NA * h * c / (nm * 1e-9) / 1000
data = (("Li", 670.8, 520, RED, ROSE), ("Na", 589.0, 496, AMBER, SAND), ("K", 766.5, 419, "#6d28d9", BLUE))
eli, ena, ek = E(670.8), E(589.0), E(766.5)
assert abs(eli - 178.3) < 0.3 and abs(ena - 203.1) < 0.3 and abs(ek - 156.1) < 0.3
ratios = [E(nm) / ie for _, nm, ie, *_ in data]
assert all(0.3 < r < 0.42 for r in ratios)
facts = dict(eli="%.0f" % eli, ena="%.0f" % ena, ek="%.0f" % ek)
f = Fig(300, 236)
f.text(150, 14, "kJ per mole: flame photon (fill) and ionisation (box)", size=10, color=NAVY, bold=True)
for i, (s, nm, ie, col, fl) in enumerate(data):
    y = 34 + i * 40
    f.text(14, y + 4, "%s (%.1f nm)" % (s, nm), size=10.5, color=SLATE, anchor="start")
    f.box(14, y + 10, ie * 0.42, 16, fill="#ffffff", stroke=col, r=2, sw=1.4)
    f.box(14, y + 10, E(nm) * 0.42, 16, fill=fl, stroke=col, r=2, sw=1.4)
    f.text(14 + ie * 0.42 + 5, y + 18, "%.0f / %d" % (E(nm), ie), size=10.5, color=col, bold=True, anchor="start", vmid=True)
f.text(150, 166, "photon energy = N h c / lambda", size=10.5, color=NAVY, bold=True)
f.text(150, 184, "ratio to ionisation: %.2f to %.2f" % (min(ratios), max(ratios)), size=10.5, color=NAVY, bold=True)
f.text(150, 202, "IE falls: Li 520 > Na 496 > K 419", size=10.5, color=NAVY, bold=True)
```

```photogrid label="3.2" cols="2" ratio="1.2" caption="Bigger atoms let go of their outer electron more easily. (a) Sodium is a soft silvery metal whose single 3s electron is lost with ease. (b) The cell lists the first ionisation energy and the atomic radius of the five alkali metals. From lithium to caesium the energy falls by 27.7 per cent (520 to 376 kJ/mol) while the radius rises from 152 to 265 pm, because the outer electron sits in a higher shell, farther from the nucleus and shielded by more inner electrons. The product IE x r stays between 79 and 100 thousand kJ pm/mol, which is why a simple inverse relation to radius explains the trend and why caesium is the most reactive of the group."
@ photo id="ceechem2/sodium2" cap="Cut pieces of sodium, a soft group-1 metal"
fit 1.2
focus 0.5 0.5
@ svg cap="Group 1: ionisation energy against atomic radius"
els = ["Li", "Na", "K", "Rb", "Cs"]
ie = [520, 496, 419, 403, 376]
r = [152, 186, 227, 248, 265]
prod = [a * b / 1000 for a, b in zip(ie, r)]
drop = (ie[0] - ie[-1]) / ie[0] * 100
assert round(drop, 1) == 27.7 and min(prod) > 79 and max(prod) < 100
f = Fig(300, 236)
f.text(150, 12, "Group 1: IE falls as radius grows", size=10.5, color=NAVY, bold=True)
hbars(f, [(n, a) for n, a in zip(els, ie)], vmax=520, fmt="%d", x0=40, y0=28, bw=120, gap=26)
for i, v in enumerate(r):
    f.text(292, 36 + i * 26, "r = %d pm" % v, size=9.5, color=SLATE, bold=True, anchor="end", vmid=True)
f.text(150, 170, "first ionisation energy, kJ/mol", size=10, color=SLATE, bold=True)
f.text(150, 200, "IE x r stays near %.0f to %.0f (x1000)" % (min(prod), max(prod)), size=10.5, color=NAVY, bold=True)
f.text(150, 218, "so IE is roughly proportional to 1/r", size=10.5, color=SLATE, bold=True)
facts = dict(drop=drop, lo=min(prod), hi=max(prod))
```

## Formula and fact sheet

| Item | Value or rule |
|---|---|
| Modern periodic law | properties are periodic functions of atomic number (Moseley, 1913) |
| Moseley's law | $\sqrt{\nu} = a(Z - b)$ |
| Period lengths | 2, 8, 8, 18, 18, 32, 32 (118 elements, 18 groups) |
| Noble-gas atomic numbers | 2, 10, 18, 36, 54, 86, 118 |
| Group from configuration | s: ns e⁻; p: 10 + ns + np e⁻; d: ns + (n − 1)d e⁻; f: group 3 |
| Effective nuclear charge | $Z_{eff} = Z - \sigma$; screening s > p > d > f |
| Energy units | 1 eV per atom = 96.5 kJ mol⁻¹ |
| Mulliken electronegativity | (IE + EA)/2 |
| IUPAC roots | 0 nil, 1 un, 2 bi, 3 tri, 4 quad, 5 pent, 6 hex, 7 sept, 8 oct, 9 enn + ium |

| Numbers worth knowing | |
|---|---|
| IE₁, period 2 (kJ mol⁻¹) | Li 520, Be 899, B 801, C 1086, N 1402, O 1314, F 1681, Ne 2081 |
| IE₁ extremes | He 2372 (highest), H 1312, Cs 376 (lowest stable) |
| Electron affinity (kJ mol⁻¹) | Cl 349 > F 328 > Br 325 > I 295; S 200 > O 141 |
| Pauling electronegativity | F 4.0, O 3.5, N 3.0, Cl 3.0, Br 2.8, C 2.5, S 2.5, I 2.5, H 2.1, Na 0.9, Cs 0.7 |
| Radii (pm) | Li 152, Na 186, K 227, Cs 265; Al 143 > Ga 135; Zr 160 ≈ Hf 159 |
| Isoelectronic orders | N³⁻ > O²⁻ > F⁻ > Na⁺ > Mg²⁺ > Al³⁺; S²⁻ > Cl⁻ > K⁺ > Ca²⁺ |

## Chapter summary

- Modern periodic law: properties are periodic functions of atomic number; periodicity comes from the recurrence of similar outer configurations.
- 7 periods (2, 8, 8, 18, 18, 32, 32 elements) and 18 groups; s, p, d and f blocks by the subshell that takes the last electron; He is s-block but sits in group 18.
- Group from configuration: s-block ns electrons, p-block 10 + ns + np, d-block ns + (n − 1)d.
- Isoelectronic species share an electron count; their radius falls as Z rises.
- Across a period Z_eff rises: size falls; IE, EA and electronegativity rise; metallic character and basic character of oxides fall. Down a group the reverse.
- IE exceptions Be > B, N > O (Mg > Al, P > S); EA exceptions Cl > F, S > O; noble gases, Be, Mg and N have near-zero or negative EA.
- Highest IE He, lowest Cs; most electronegative F (4.0); highest EA Cl. A big jump in successive IEs counts the valence electrons.
- Ga < Al in size (poor 3d shielding); Zr ≈ Hf (lanthanoid contraction).

## Practice questions

**Set A — Recall (20 questions)**

1. The modern periodic law states that the properties of elements are periodic functions of their
   (a) atomic masses (b) atomic numbers (c) numbers of neutrons (d) atomic volumes
2. The modern periodic law grew out of the X-ray work of
   (a) Mendeleev (b) Newlands (c) Döbereiner (d) Moseley
3. The number of elements in the fourth period of the periodic table is
   (a) 18 (b) 8 (c) 32 (d) 10
4. The f-block elements are also called
   (a) representative elements (b) transition elements (c) inner transition elements (d) noble gases
5. The most electronegative element is
   (a) oxygen (b) chlorine (c) fluorine (d) nitrogen
6. The element with the highest electron affinity (most negative electron gain enthalpy) is
   (a) chlorine (b) fluorine (c) oxygen (d) bromine
7. The element with the highest first ionisation energy is
   (a) hydrogen (b) helium (c) neon (d) fluorine
8. Among the following, the lowest first ionisation energy belongs to
   (a) Li (b) Na (c) K (d) Cs
9. Across a period from left to right, the atomic radius of main-group elements generally
   (a) increases (b) decreases (c) remains the same (d) first decreases, then increases
10. Which of these elements is a metalloid?
   (a) Si (b) Na (c) S (d) Cl
11. Isoelectronic species have the same number of
   (a) protons (b) neutrons (c) nucleons (d) electrons
12. The IUPAC temporary name of the element with atomic number 104 is
   (a) unniltetrium (b) ununquadium (c) unnilquadium (d) unquadnilium
13. Which element belongs to the d-block?
   (a) Zn (b) Ga (c) Ca (d) Ge
14. The elements of group 16 are called
   (a) halogens (b) pnictogens (c) noble gases (d) chalcogens
15. The nearly equal atomic radii of zirconium and hafnium are due to
   (a) the inert-pair effect (b) the lanthanoid contraction (c) the diagonal relationship (d) the screening effect of s electrons
16. Which oxide is amphoteric?
   (a) Na₂O (b) MgO (c) Al₂O₃ (d) SO₃
17. Compared with its parent atom, a cation is always
   (a) larger (b) the same size (c) larger or smaller, depending on the group (d) smaller
18. For any element with two or more electrons, the second ionisation energy is
   (a) greater than the first (b) less than the first (c) equal to the first (d) zero
19. Helium has the configuration 1s² but is placed in group 18 because
   (a) it is an s-block metal (b) it has eight valence electrons (c) its shell is complete and it is inert, like the noble gases (d) it has the highest atomic mass in period 1
20. On Pauling's scale, the electronegativity of fluorine is
   (a) 3.0 (b) 4.0 (c) 3.5 (d) 2.8

::: note Answers and explanations — Set A
**1.** (b) — Moseley showed atomic number, not atomic mass, is the fundamental property; ordering by mass forced Mendeleev to reverse pairs such as Te and I (and, later, Ar and K).
**2.** (d) — Moseley's law, √ν = a(Z − b), linked X-ray frequency to atomic number (1913). Mendeleev's law (1869) was based on atomic mass.
**3.** (a) — Period 4 fills 4s, 3d and 4p: 2 + 10 + 6 = 18 elements (K to Kr).
**4.** (c) — The lanthanoids and actinoids fill (n − 2)f orbitals: inner transition elements. "Transition elements" are the d-block.
**5.** (c) — Fluorine, 4.0 on the Pauling scale. Oxygen (3.5) is second.
**6.** (a) — Chlorine (349 kJ mol⁻¹) beats fluorine (328), whose tiny 2p shell repels the added electron.
**7.** (b) — Helium (2372 kJ mol⁻¹): a 1s² pair held by two protons with no inner electrons to screen them. Neon is next (2081).
**8.** (d) — Ionisation energy falls down group 1 as size grows; Cs (376 kJ mol⁻¹) is the lowest of these.
**9.** (b) — The nuclear charge rises while electrons enter the same shell, so Z_eff rises and pulls the shell in.
**10.** (a) — Silicon is a metalloid (semiconductor); Na is a metal, S and Cl are non-metals.
**11.** (d) — Isoelectronic means "equal electrons" (e.g. Na⁺, Ne and F⁻ have 10 each).
**12.** (c) — 1-0-4 → un-nil-quad-ium: unnilquadium, symbol Unq (now rutherfordium). Ununquadium is element 114.
**13.** (a) — Zinc ([Ar] 3d¹⁰ 4s²) is in group 12 of the d-block. Ga and Ge are p-block, Ca is s-block.
**14.** (d) — Group 16 (O, S, Se, Te, Po) are the chalcogens ("ore-formers"); pnictogens are group 15, halogens group 17.
**15.** (b) — Poor screening by the 4f electrons shrinks the elements after the lanthanoids, so Hf (5d) ends up the size of Zr (4d).
**16.** (c) — Al₂O₃ dissolves in acids and in alkalis. Na₂O and MgO are basic; SO₃ is acidic.
**17.** (d) — With fewer electrons for the same nuclear charge (and often one shell fewer), a cation is always smaller than its atom.
**18.** (a) — The second electron is removed from a positive ion, which holds its electrons more tightly.
**19.** (c) — By configuration helium is s-block, but its complete shell and inertness place it with the noble gases. It has two valence electrons, not eight.
**20.** (b) — F = 4.0 on Pauling's scale; 3.5 is oxygen, 3.0 nitrogen or chlorine, 2.8 bromine.
:::

**Set B — Understanding (13 questions)**

1. The correct order of atomic radius is
   (a) Si > Al > Mg > Na (b) Mg > Na > Si > Al (c) Na > Mg > Al > Si (d) Al > Si > Na > Mg
2. The correct order of first ionisation energy is
   (a) B < Be < C < O < N (b) Be < B < C < N < O (c) B < Be < C < N < O (d) Be < B < C < O < N
3. Nitrogen has a higher first ionisation energy than oxygen because
   (a) nitrogen is the larger atom (b) oxygen has a higher nuclear charge (c) oxygen is more electronegative (d) nitrogen has a half-filled, extra-stable 2p³ subshell
4. Chlorine has a higher electron affinity than fluorine because
   (a) chlorine has a higher nuclear charge (b) fluorine's compact 2p shell repels the added electron (c) fluorine is less electronegative (d) chlorine has fewer shells
5. Among the isoelectronic ions O²⁻, F⁻, Na⁺ and Mg²⁺, the largest is
   (a) O²⁻ (b) F⁻ (c) Na⁺ (d) Mg²⁺
6. Which pair is isoelectronic?
   (a) CO and NO (b) Na⁺ and K⁺ (c) CO and N₂ (d) F⁻ and Cl⁻
7. The element with atomic number 35 lies in
   (a) period 4, group 7, d-block (b) period 5, group 17, p-block (c) period 3, group 15, p-block (d) period 4, group 17, p-block
8. An element of period 4 has the outer configuration 3d⁵ 4s¹. It belongs to group
   (a) 1 (b) 6 (c) 5 (d) 11
9. The correct order of size is
   (a) Fe³⁺ > Fe²⁺ > Fe (b) Fe²⁺ > Fe > Fe³⁺ (c) Fe > Fe²⁺ > Fe³⁺ (d) Fe = Fe²⁺ = Fe³⁺
10. Gallium has a slightly smaller atomic radius than aluminium because
   (a) its ten 3d electrons shield the nucleus poorly (b) it has fewer shells than aluminium (c) it is a non-metal (d) it has a lower nuclear charge
11. Which statement about electronegativity and electron affinity is correct?
   (a) both are measured in kJ mol⁻¹ (b) electronegativity refers to an isolated gaseous atom (c) electron affinity refers to an atom in a bond (d) electronegativity refers to a bonded atom and has no unit
12. Which oxide is the most basic?
   (a) Al₂O₃ (b) Na₂O (c) MgO (d) SiO₂
13. The electron gain enthalpy of a noble gas is positive (energy is absorbed) because
   (a) noble gases have the largest atoms in their periods (b) noble gases have the highest electronegativities (c) the added electron must enter a new, higher shell (d) noble gases have low nuclear charges

::: note Answers and explanations — Set B
**1.** (c) — Across period 3 the radius falls: Na 186, Mg 160, Al 143, Si 117 pm.
**2.** (a) — B 801 < Be 899 < C 1086 < O 1314 < N 1402 kJ mol⁻¹: boron dips below beryllium and oxygen below nitrogen.
**3.** (d) — The half-filled 2p³ subshell is extra stable; oxygen's paired 2p electron is repelled by its partner and leaves more easily. Being larger (a) would lower, not raise, the IE.
**4.** (b) — Fluorine's 2p shell is so small and crowded that the incoming electron is strongly repelled. Cl's higher nuclear charge is largely screened by its extra shell.
**5.** (a) — All have 10 electrons; O²⁻ has the fewest protons (8) holding them, so it is the largest.
**6.** (c) — CO (6 + 8) and N₂ (7 + 7) both have 14 electrons. NO has 15; Na⁺ 10 vs K⁺ 18; F⁻ 10 vs Cl⁻ 18.
**7.** (d) — Z = 35: [Ar] 3d¹⁰ 4s² 4p⁵ — period 4, p-block, group 10 + 7 = 17 (bromine).
**8.** (b) — d-block group = ns + (n − 1)d electrons = 1 + 5 = 6 (chromium).
**9.** (c) — Removing electrons lets the same nucleus pull the rest closer; the more electrons removed, the smaller the species.
**10.** (a) — The filled 3d¹⁰ shells poorly, so gallium's outer electrons feel a higher effective nuclear charge. Ga has more shells than Al, and a higher Z.
**11.** (d) — Electronegativity is a relative tendency of a bonded atom (no unit); electron affinity is an energy of an isolated gaseous atom.
**12.** (b) — Metallic character, and so basic character of the oxide, is greatest at the left of a period: Na₂O > MgO > Al₂O₃ (amphoteric) > SiO₂ (acidic).
**13.** (c) — The ns² np⁶ shell is full, so an extra electron must go into the next shell, far from the nucleus and well screened — energy has to be supplied.
:::

**Set C — Application (10 questions)**

1. The first four ionisation energies of an element are 738, 1451, 7733 and 10 540 kJ mol⁻¹. The element is most likely in group
   (a) 1 (b) 2 (c) 13 (d) 14
2. The correct order of decreasing radius of the isoelectronic species S²⁻, Cl⁻, K⁺ and Ca²⁺ is
   (a) Ca²⁺ > K⁺ > Cl⁻ > S²⁻ (b) Cl⁻ > S²⁻ > K⁺ > Ca²⁺ (c) K⁺ > Ca²⁺ > S²⁻ > Cl⁻ (d) S²⁻ > Cl⁻ > K⁺ > Ca²⁺
3. The element with atomic number 48 is placed in
   (a) period 5, group 12, d-block (b) period 4, group 12, d-block (c) period 5, group 2, s-block (d) period 5, group 14, p-block
4. The element with atomic number 117 belongs to group
   (a) 15 (b) 16 (c) 17 (d) 18
5. The IUPAC temporary symbol of the element with atomic number 120 is
   (a) Unb (b) Ubu (c) Uun (d) Ubn
6. The first ionisation energy of sodium is 496 kJ mol⁻¹. The energy needed to ionise all the atoms in 2.3 g of sodium vapour is (Na = 23)
   (a) 4.96 kJ (b) 49.6 kJ (c) 496 kJ (d) 1141 kJ
7. The first ionisation energy of an atom is 5.14 eV. Per mole of atoms this is about (1 eV per atom = 96.5 kJ mol⁻¹)
   (a) 496 kJ mol⁻¹ (b) 5.14 kJ mol⁻¹ (c) 49.6 kJ mol⁻¹ (d) 1312 kJ mol⁻¹
8. Which of these elements has the highest second ionisation energy?
   (a) Mg (b) Al (c) Na (d) Si
9. The correct order of electron affinity of the halogens is
   (a) Cl > F > Br > I (b) F > Cl > Br > I (c) Cl > Br > F > I (d) I > Br > Cl > F
10. An element X of period 3 forms an oxide X₂O₃ that dissolves both in dilute HCl and in NaOH solution. X is
   (a) Na (b) P (c) Al (d) Mg

::: note Answers and explanations — Set C
**1.** (b) — The big jump comes after the second electron (1451 → 7733), so there are two valence electrons: group 2 (these are magnesium's values).
**2.** (d) — All have 18 electrons; protons 16, 17, 19, 20. Fewer protons, larger species: S²⁻ > Cl⁻ > K⁺ > Ca²⁺.
**3.** (a) — Z = 48 is cadmium, [Kr] 4d¹⁰ 5s²: period 5, d-block, group 10 + 2 = 12. (48 − 36 = 12th place of period 5.)
**4.** (c) — 117 − 86 = 31st place in period 7; subtract 14 for the f-block: group 17 (tennessine). Element 118 closes the period in group 18.
**5.** (d) — 1-2-0 → un-bi-nil-ium: unbinilium, Ubn. Unb is 102, Ubu is 121 and Uun is 110.
**6.** (b) — n = 2.3/23 = 0.1 mol; energy = 0.1 × 496 = 49.6 kJ. Option (d) multiplies by the mass instead of the moles.
**7.** (a) — 5.14 × 96.5 = 496 kJ mol⁻¹ — the value for sodium.
**8.** (c) — Na⁺ has the neon configuration, so its second electron comes from a complete 2p shell (about 4560 kJ mol⁻¹). For Mg, Al and Si the second electron is still a valence electron.
**9.** (a) — Cl 349 > F 328 > Br 325 > I 295 kJ mol⁻¹: the general fall down the group, except that F lies below Cl because of its small size.
**10.** (c) — Al₂O₃ is amphoteric: Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O and Al₂O₃ + 2NaOH → 2NaAlO₂ + H₂O. Na₂O and MgO are basic and do not fit X₂O₃; phosphorus oxides are acidic.
:::

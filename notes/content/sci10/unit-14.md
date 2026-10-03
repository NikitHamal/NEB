---
subject: Science and Technology
grade: 10
unit: 14
title: Classification of Elements
hours: 0
area: Science and Technology
---

There are 118 known elements. If each one were studied on its own, chemistry would be a list of facts to memorise. Scientists found that elements fall into families with similar behaviour, and that this pattern repeats in a regular way. The periodic table is the map of that pattern. In this chapter you will learn how the table was built, how to read it, and how to predict the size, reactivity and metallic nature of an element from its position alone.

::: key What the SEE paper asks from this chapter
Expect: the names of the scientists and their laws (1 mark); the limitations of Mendeleev's table (2 marks); the electronic configuration, group and period of an element from its atomic number (2 to 4 marks); and the trend of atomic size, ionisation energy or electronegativity down a group or across a period (4 marks).
:::

## 14.1 Periodic table

### Why classify?

Early chemists found elements one by one. By 1860 about 60 were known. To study them in an orderly way, scientists tried to group them by atomic mass and by chemical properties.

### Dobereiner's law of triads (1829)

Johann Dobereiner, a German chemist, noticed that some elements occur in groups of three with similar properties. He called such a group a **triad**. In a triad, when the elements are arranged in the order of increasing atomic mass, the atomic mass of the middle element is nearly the **average** of the other two.

| Triad | Atomic masses | Average of first and third |
|---|---|---|
| Li, Na, K | 7, 23, 39 | (7 + 39) / 2 = 23 |
| Ca, Sr, Ba | 40, 88, 137 | (40 + 137) / 2 = 88.5 |
| Cl, Br, I | 35.5, 80, 127 | (35.5 + 127) / 2 = 81.25 |

**Limitation.** Only a few triads could be found. Many elements with similar properties (such as F, Cl, Br, I) did not fit into groups of three.

### Newlands' law of octaves (1864)

John Newlands, an English chemist, arranged the elements in the order of increasing atomic mass. He found that **every eighth element had properties similar to the first**, like the notes of a music scale (sa, re, ga, ma, pa, dha, ni, sa). This is the **law of octaves**.

| Sa | Re | Ga | Ma | Pa | Dha | Ni |
|---|---|---|---|---|---|---|
| H | Li | Be | B | C | N | O |
| F | Na | Mg | Al | Si | P | S |
| Cl | K | Ca | Cr | Ti | Mn | Fe |

**Limitations.**

- It worked only up to calcium. After that, the eighth element did not resemble the first.
- It assumed that only 56 elements existed. Newer elements, such as the noble gases, had no place.
- Some unlike elements were forced into the same column (for example Co and Ni with F, Cl).

### Mendeleev's periodic table (1869)

Dmitri Mendeleev, a Russian chemist, arranged the 63 elements known to him in rows and columns.

::: definition Mendeleev's periodic law
The physical and chemical properties of the elements are a **periodic function of their atomic masses**.
:::

His table had **8 vertical columns called groups** and **horizontal rows called periods**. Its strengths and weaknesses are shown below.

| Merits | Demerits |
|---|---|
| Elements with similar properties were placed in the same group. | The position of hydrogen was not fixed. |
| He **left gaps** for undiscovered elements and predicted their properties. | Isotopes had no separate places, although they have different atomic masses. |
| He placed some elements in order of properties, not mass, to keep a family together. | Elements of higher atomic mass came before those of lower mass (for example Co before Ni, Te before I). |
| Gaps were later filled: gallium (eka-aluminium), scandium (eka-boron) and germanium (eka-silicon) matched his predictions. | Chemically unlike elements (alkali metals and coinage metals Cu, Ag, Au) were put in the same group. |

### Modern periodic law (Moseley, 1913)

Henry Moseley studied X-rays from different elements. He proved that the true basis of an element is its **atomic number** (the number of protons) and not its atomic mass.

::: definition Modern periodic law
The physical and chemical properties of the elements are a **periodic function of their atomic numbers**.
:::

This removed the faults of Mendeleev's table. Cobalt (Z = 27) comes before nickel (Z = 28) because of its lower atomic number, and isotopes share one place because they have the same atomic number.

### The modern (long form) periodic table

The modern table has **18 vertical columns (groups 1 to 18)** and **7 horizontal rows (periods 1 to 7)**. Elements are arranged in increasing order of atomic number. Two rows of 14 elements each (the lanthanides and actinides) are placed below the main table so that the table does not become too wide.

```figure caption="The first 20 elements of the modern periodic table, with atomic numbers. Colour shows metals (blue), non-metals (orange) and noble gases (green)."
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.9))
cells = {
 1:(0,0,'H',1), 2:(17,0,'He',2),
 3:(0,1,'Li',3),4:(1,1,'Be',4),5:(12,1,'B',5),6:(13,1,'C',6),7:(14,1,'N',7),8:(15,1,'O',8),9:(16,1,'F',9),10:(17,1,'Ne',10),
 11:(0,2,'Na',11),12:(1,2,'Mg',12),13:(12,2,'Al',13),14:(13,2,'Si',14),15:(14,2,'P',15),16:(15,2,'S',16),17:(16,2,'Cl',17),18:(17,2,'Ar',18),
 19:(0,3,'K',19),20:(1,3,'Ca',20)}
nonmetal = {1,6,7,8,9,15,16,17}
for z,(c,r,s,n) in cells.items():
    col = '#bfe3c0' if z in (2,10,18) else ('#f9d4a8' if z in nonmetal else '#c4d7f2')
    ax.add_patch(Rectangle((c, -r), 0.94, 0.94, fc=col, ec=INK, lw=0.6))
    ax.text(c+0.47, -r+0.60, s, ha='center', va='center', fontsize=7.2, color=INK, weight='bold')
    ax.text(c+0.47, -r+0.22, str(n), ha='center', va='center', fontsize=5.4, color=MUTED)
ax.add_patch(Rectangle((2,-3), 10, 3.94, fc='#f4f4f4', ec=GRID, lw=0.6, hatch='//'))
ax.text(7, -1.0, 'transition elements (d-block)\nbegin from Sc (Z = 21)', ha='center', va='center', fontsize=6.6, color=MUTED)
for g in range(18):
    ax.text(g+0.47, 1.12, str(g+1), ha='center', fontsize=5.6, color=MUTED)
for p in range(4):
    ax.text(-0.35, -p+0.47, str(p+1), ha='center', va='center', fontsize=6.4, color=MUTED)
ax.text(-0.2, 1.45, 'Group', fontsize=6.4, color=MUTED); ax.text(-1.0, 0.47, 'Period', fontsize=6.4, color=MUTED, rotation=90, va='center')
ax.set_xlim(-1.3, 18.2); ax.set_ylim(-3.2, 1.7); ax.set_aspect('equal'); ax.axis('off')
```

## 14.2 Periodic properties

### Groups and periods

- A **group** is a vertical column. Elements of a group have the **same number of valence electrons** and so similar chemical properties.
- A **period** is a horizontal row. In a period the number of electron shells is the same; the number of valence electrons increases from left to right by one at each step.

| Period | Number of elements | Elements |
|---|---|---|
| 1 (very short) | 2 | H, He |
| 2 (short) | 8 | Li to Ne |
| 3 (short) | 8 | Na to Ar |
| 4 (long) | 18 | K to Kr |
| 5 (long) | 18 | Rb to Xe |
| 6 (very long) | 32 | Cs to Rn (includes lanthanides) |
| 7 (incomplete) | 32 (when complete) | Fr onwards (includes actinides) |

### Electronic configuration

Electrons are filled in shells K, L, M, N with a maximum of $2n^2$ electrons in the nth shell: K = 2, L = 8, M = 18. The outermost shell of the first 18 elements can hold at most 8 electrons (2 for K). For the first 20 elements, the third shell holds 8 before the fourth shell starts to fill (K gets 2, 8, 8, 1).

| Element | Z | Configuration (K, L, M, N) | Valence electrons | Group | Period |
|---|---|---|---|---|---|
| Hydrogen | 1 | 1 | 1 | 1 | 1 |
| Helium | 2 | 2 | 2 | 18 | 1 |
| Lithium | 3 | 2, 1 | 1 | 1 | 2 |
| Carbon | 6 | 2, 4 | 4 | 14 | 2 |
| Nitrogen | 7 | 2, 5 | 5 | 15 | 2 |
| Oxygen | 8 | 2, 6 | 6 | 16 | 2 |
| Neon | 10 | 2, 8 | 8 | 18 | 2 |
| Sodium | 11 | 2, 8, 1 | 1 | 1 | 3 |
| Magnesium | 12 | 2, 8, 2 | 2 | 2 | 3 |
| Aluminium | 13 | 2, 8, 3 | 3 | 13 | 3 |
| Silicon | 14 | 2, 8, 4 | 4 | 14 | 3 |
| Chlorine | 17 | 2, 8, 7 | 7 | 17 | 3 |
| Argon | 18 | 2, 8, 8 | 8 | 18 | 3 |
| Potassium | 19 | 2, 8, 8, 1 | 1 | 1 | 4 |
| Calcium | 20 | 2, 8, 8, 2 | 2 | 2 | 4 |

::: tip Finding group and period quickly
**Period number = number of occupied shells.** For groups 1 and 2, **group number = valence electrons**. For groups 13 to 18, **group number = valence electrons + 10**. For example, Cl is 2, 8, 7: three shells, so period 3; 7 + 10 = 17, so group 17.
:::

::: example Group and period from atomic number
**Problem.** An element X has atomic number 16. Write its electronic configuration and state its period, group, valency and whether it is a metal or non-metal.

**Solution.** Z = 16, so there are 16 electrons.

K = 2, L = 8, M = 16 − 10 = 6. Configuration: 2, 8, 6.

- Shells occupied = 3, so **period 3**.
- Valence electrons = 6, so group = 6 + 10 = **group 16**.
- It needs 2 more electrons to complete the octet, so **valency = 2**.
- It is sulphur, a **non-metal**.
:::

### Valency

**Valency** is the combining capacity of an atom. It equals the number of electrons an atom loses, gains or shares to reach a stable (duplet or octet) arrangement.

- Valence electrons 1, 2, 3 → valency equal to the number of valence electrons (1, 2, 3).
- Valence electrons 4 to 7 → valency = 8 − number of valence electrons (4, 3, 2, 1).
- Noble gases (full outer shell) → valency 0.

### The s-, p-, d- and f-block elements

Elements are also grouped as blocks according to the subshell that receives the last electron.

| Block | Groups | Subshell being filled | Examples |
|---|---|---|---|
| s-block | 1, 2 (and He) | s | Na, Mg, Ca |
| p-block | 13 to 18 | p | Al, C, O, Cl, Ne |
| d-block | 3 to 12 (transition elements) | d | Fe, Cu, Zn |
| f-block | lanthanides and actinides | f | Ce, U |

### Periodic properties

A **periodic property** is a property that changes in a regular way across a period and down a group, and repeats after a certain interval.

#### Atomic size (atomic radius)

Atomic size is the distance from the nucleus to the outermost electron shell.

- **Down a group** it **increases**, because each new element has one more shell.
- **Across a period** (left to right) it **decreases**, because the nuclear charge increases by one each step and pulls the same shells in more strongly, while the number of shells stays the same.

#### Ionisation energy

**Ionisation energy (ionisation potential)** is the minimum energy needed to remove the most loosely held electron from an isolated gaseous atom.

- **Down a group** it **decreases**: the outer electron is farther from the nucleus and is shielded by inner shells, so it is removed more easily.
- **Across a period** it **increases**: the atoms are smaller and the nuclear pull is greater.

#### Electronegativity

**Electronegativity** is the power of an atom to attract the shared pair of electrons towards itself in a covalent bond. Fluorine is the most electronegative element (4.0 on the Pauling scale).

- **Down a group** it **decreases**.
- **Across a period** it **increases**.

#### Metallic and non-metallic character

Metals tend to lose electrons, so metallic character is greater when ionisation energy is low. Metallic character **increases down a group** and **decreases across a period**. Non-metallic character follows the opposite trend. Hence the most reactive metal (Cs, Fr) is at the bottom left and the most reactive non-metal (F) is at the top right.

| Property | Down a group | Left to right in a period |
|---|---|---|
| Atomic size | increases | decreases |
| Ionisation energy | decreases | increases |
| Electronegativity | decreases | increases |
| Metallic character | increases | decreases |
| Non-metallic character | decreases | increases |

```figure caption="Atomic radius (pm): it rises down group 1 (left) and falls across period 3 (right)."
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0,2.5))
g1 = ['Li','Na','K','Rb']; r1 = [152,186,227,248]
a1.bar(g1, r1, color=ACCENT, width=0.6)
for i,v in enumerate(r1): a1.text(i, v+4, str(v), ha='center', fontsize=7, color=INK)
a1.set_title('Group 1', fontsize=8, color=INK); a1.set_ylim(0,290)
p3 = ['Na','Mg','Al','Si','P','S','Cl']; r3 = [186,160,143,118,110,103,99]
a2.plot(p3, r3, marker='o', color=SERIES[1], lw=1.6, ms=4)
for i,v in enumerate(r3): a2.text(i, v+8, str(v), ha='center', fontsize=6.5, color=INK)
a2.set_title('Period 3', fontsize=8, color=INK); a2.set_ylim(60,220)
for a in (a1,a2):
    a.spines[['top','right']].set_visible(False); a.tick_params(labelsize=7); a.set_ylabel('radius (pm)', fontsize=7, color=MUTED)
fig.tight_layout()
```

::: caution Do not mix up the two trends
Atomic size **falls** from Na to Cl even though the atomic number rises. Students often reason "more electrons, bigger atom". Across a period the electrons go into the **same** shell while the nuclear charge grows, so the atom shrinks. Size grows only when a **new shell** is added, which happens down a group.
:::

::: example Using trends to compare elements
**Problem.** Arrange Na, Mg, Cl and K in order of (a) increasing atomic size, (b) increasing electronegativity.

**Solution.** Na, Mg and Cl are in period 3 and K is in period 4.

(a) K has an extra shell, so it is the largest. In period 3, size falls from left to right, so Na > Mg > Cl. Increasing order: **Cl < Mg < Na < K**.

(b) Electronegativity rises across a period and falls down a group. So K is the lowest, then Na, then Mg, and Cl the highest. Increasing order: **K < Na < Mg < Cl**.
:::

## 14.3 Groups and periods

### Some important groups

| Group | Name | Valence electrons | Members | Key properties |
|---|---|---|---|---|
| 1 | Alkali metals | 1 | Li, Na, K, Rb, Cs, Fr | Soft, very reactive, react with water to form alkali and hydrogen, valency 1, stored under kerosene |
| 2 | Alkaline earth metals | 2 | Be, Mg, Ca, Sr, Ba, Ra | Harder than group 1, less reactive, valency 2 |
| 13 | Boron group | 3 | B, Al, Ga, In, Tl | Valency 3; Al is the most abundant metal in the crust |
| 14 | Carbon group | 4 | C, Si, Ge, Sn, Pb | Carbon is the basis of organic life; Si is a semiconductor |
| 15 | Nitrogen group | 5 | N, P, As, Sb, Bi | Valency 3 (and 5); N₂ is 78 % of air |
| 16 | Oxygen group (chalcogens) | 6 | O, S, Se, Te, Po | Valency 2 |
| 17 | Halogens | 7 | F, Cl, Br, I, At | Reactive non-metals, valency 1, form salts with metals |
| 18 | Noble (inert) gases | 8 (He: 2) | He, Ne, Ar, Kr, Xe, Rn | Stable, unreactive, valency 0 |

### Position of hydrogen

Hydrogen has one valence electron like the alkali metals, but it is a non-metal and a gas, and it can also gain one electron like a halogen. It is usually placed at the top of group 1, though this position is not settled.

### Characteristics of a period

Moving left to right in a period, the elements change from strongly metallic (group 1) to metalloids (such as Si) to non-metals (group 17) and end with an inert gas (group 18). Oxides change from strongly basic (Na₂O) to amphoteric (Al₂O₃) to acidic (SO₃, Cl₂O₇).

### Why the table is useful

- It lets us predict the properties of an element from its neighbours.
- It explains why Na, K and Li behave alike (same group).
- It helps in finding the valency and the formula of compounds.
- It guided the discovery of new elements (Ga, Sc, Ge).

::: example Predicting a formula
**Problem.** Calcium has atomic number 20 and chlorine 17. Find the formula of calcium chloride.

**Solution.** Ca: 2, 8, 8, 2, so it loses 2 electrons and has valency 2. Cl: 2, 8, 7, so it gains 1 electron and has valency 1. Exchange the valencies (criss-cross): Ca₁Cl₂, so the formula is **CaCl₂**.
:::

::: example Dobereiner's triad check
**Problem.** The atomic masses of Ca and Ba are 40 and 137. Predict the atomic mass of Sr and compare it with the real value, 87.6.

**Solution.** Predicted mass of Sr = (40 + 137) / 2 = 177 / 2 = **88.5**. The real value is 87.6, so the law holds only approximately (difference 0.9).
:::

## Chapter summary

- Dobereiner (triads), Newlands (octaves) and Mendeleev (periodic law by atomic mass) were early attempts; Moseley's **modern periodic law** uses **atomic number**.
- The modern table has **18 groups and 7 periods**; blocks are s, p, d and f.
- Period number = number of shells; group number (1, 2) = valence electrons; groups 13 to 18: valence electrons + 10.
- Valency = valence electrons (1 to 3) or 8 − valence electrons (4 to 7); noble gases are 0.
- Down a group: atomic size increases; ionisation energy and electronegativity decrease; metallic character increases.
- Across a period: atomic size decreases; ionisation energy and electronegativity increase; non-metallic character increases.
- Group 1 = alkali metals, group 2 = alkaline earth metals, group 17 = halogens, group 18 = noble gases.

## Practice questions

**Group A — Objective questions (1 mark each)**

1. Who proposed the law of triads? <span class="marks">[1]</span>
   (a) Newlands (b) Dobereiner (c) Mendeleev (d) Moseley
2. The modern periodic law is based on <span class="marks">[1]</span>
   (a) atomic mass (b) atomic number (c) number of neutrons (d) density
3. The number of elements in the third period is <span class="marks">[1]</span>
   (a) 2 (b) 8 (c) 18 (d) 32
4. Which has the largest atomic size? <span class="marks">[1]</span>
   (a) Li (b) Na (c) K (d) Be
5. The most electronegative element is <span class="marks">[1]</span>
   (a) O (b) Cl (c) F (d) N
6. An element with configuration 2, 8, 2 is in <span class="marks">[1]</span>
   (a) group 2, period 3 (b) group 3, period 2 (c) group 12, period 2 (d) group 2, period 2
7. Elements of group 17 are called <span class="marks">[1]</span>
   (a) alkali metals (b) halogens (c) noble gases (d) chalcogens

::: note Answers to Group A
**1.** (b) — Dobereiner, 1829.
**2.** (b) — Moseley showed atomic number is the basis.
**3.** (b) — Na to Ar.
**4.** (c) — K has four shells.
**5.** (c) — fluorine, 4.0.
**6.** (a) — Mg: 3 shells, 2 valence electrons.
**7.** (b) — halogens.
:::

**Group B — Short answer (2 marks each)**

1. State the modern periodic law. <span class="marks">[2]</span>
2. Write any two limitations of Newlands' law of octaves. <span class="marks">[2]</span>
3. Why does atomic size decrease from left to right in a period? <span class="marks">[2]</span>
4. Define ionisation energy. How does it change down a group? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** The physical and chemical properties of elements are a periodic function of their atomic numbers.
**2.** (i) It worked only up to calcium. (ii) It did not leave places for new elements such as the noble gases; unlike elements were placed together.
**3.** The number of shells remains the same, but the nuclear charge increases by one at every step. The stronger pull draws the electrons nearer to the nucleus.
**4.** It is the minimum energy needed to remove the outermost electron from an isolated gaseous atom. It decreases down a group because the outer electron is farther away and shielded by more inner shells.
:::

**Group C — Long answer (4 marks each)**

1. Write the electronic configuration of Mg (Z = 12) and Cl (Z = 17). State the period, group and valency of each, and write the formula of the compound they form. <span class="marks">[4]</span>
2. Describe the merits and demerits of Mendeleev's periodic table. <span class="marks">[4]</span>
3. Compare the elements Na, Mg, Al in terms of atomic size, ionisation energy and metallic character. Give reasons. <span class="marks">[4]</span>
4. The atomic masses of Li and K are 7 and 39. Using Dobereiner's law, find the atomic mass of Na and state whether it fits. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Mg: 2, 8, 2; period 3, group 2, valency 2. Cl: 2, 8, 7; period 3, group 17, valency 1. Mg loses two electrons, Cl gains one each, so two Cl atoms combine with one Mg: **MgCl₂**.
**2.** Merits: similar elements in one group; gaps left and properties of Ga, Sc, Ge predicted correctly. Demerits: position of hydrogen uncertain; no place for isotopes; some higher-mass elements placed before lower-mass ones (Co before Ni); unlike elements in one group.
**3.** All are in period 3, so the number of shells is constant while the nuclear charge increases from Na (+11) to Al (+13). Atomic size decreases (Na > Mg > Al); ionisation energy increases (Na < Mg < Al, roughly); metallic character decreases (Na > Mg > Al).
**4.** Mass of Na = (7 + 39) / 2 = 46 / 2 = **23**. The actual atomic mass of sodium is 23, so it fits the law exactly.
:::

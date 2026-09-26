---
subject: Chemistry
grade: 11
unit: 4
title: Classification of elements and Periodic Table
hours: 5
area: General and Physical Chemistry
---

There are 118 known elements. Learning each one separately would be hopeless;
learning the *pattern* they fall into takes an afternoon. Arrange the elements in
order of atomic number and their properties come back again and again at regular
intervals. This unit explains why the table has the shape it has, and how six
properties — atomic radius, ionic radius, ionization energy, electron affinity,
electronegativity and metallic character — change in a way you can predict.

::: key What the examiner wants
Nearly every NEB question on this unit is one of three kinds: (i) place an element
given its electronic configuration, (ii) compare two elements on a trend, (iii)
explain an *irregularity* (Be above B, N above O, Cl above F). Stating the trend
earns half the marks. The reason — always effective nuclear charge, shell number
or half-filled stability — earns the other half.
:::

## 4.1 Modern periodic law and modern periodic table

Mendeleev (1869) arranged the elements by increasing **atomic mass**, but had to
reverse some pairs to keep the chemistry right: Ar (39.9) before K (39.1), Co
before Ni, Te before I. In 1913 **Henry Moseley** measured the frequency $\nu$ of
the characteristic X-rays emitted by different metals and found

$$ \sqrt{\nu} = a(Z - b) $$

where $Z$ is the atomic number and $a$, $b$ are constants. Atomic number, not
atomic mass, is the fundamental property of an element, and every reversal
disappears when the elements are ordered by $Z$.

::: definition Modern periodic law
The physical and chemical properties of the elements are **periodic functions of
their atomic numbers**.
:::

The long form (modern) periodic table has **7 horizontal periods** and **18
vertical groups**. A period number equals the principal quantum number $n$ of the
outermost shell being filled, so the number of elements in a period is fixed by
how many orbitals that shell offers.

| Period | $n$ | Subshells filled | No. of elements | Name |
|---|---|---|---|---|
| 1 | 1 | 1s | 2 | very short |
| 2 | 2 | 2s 2p | 8 | short |
| 3 | 3 | 3s 3p | 8 | short |
| 4 | 4 | 4s 3d 4p | 18 | long |
| 5 | 5 | 5s 4d 5p | 18 | long |
| 6 | 6 | 6s 4f 5d 6p | 32 | very long |
| 7 | 7 | 7s 5f 6d 7p | 32 | very long |

Elements in the same **group** have the same valence configuration, so they behave
alike: all of group 1 reacts with water to give a hydroxide and hydrogen, all of
group 17 forms an X⁻ ion. Depending on which subshell receives the last electron,
an element belongs to one of four **blocks**.

| Block | Last electron enters | Outer configuration | Groups | Character |
|---|---|---|---|---|
| s | ns | ns¹⁻² | 1, 2 (and He) | soft, very reactive metals |
| p | np | ns² np¹⁻⁶ | 13–18 | metals, metalloids, non-metals |
| d | (n−1)d | (n−1)d¹⁻¹⁰ ns⁰⁻² | 3–12 | transition metals |
| f | (n−2)f | (n−2)f¹⁻¹⁴ (n−1)d⁰⁻¹ ns² | inside group 3 | inner transition |

```figure caption="Block structure of the long-form periodic table. Period number = $n$ of the outermost shell; the block is fixed by the subshell that receives the last electron."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2,3.1))
COL = {'s':'#1d6fb8','p':'#d9534f','d':'#2e8b57','f':'#b8860b'}
def blk(g,p):
    if g <= 2: return 's'
    if g >= 13: return 'p'
    return 'd'
for p in range(1,8):
    for g in range(1,19):
        if p == 1 and g not in (1,18): continue
        if p in (2,3) and 3 <= g <= 12: continue
        b = 's' if (p == 1) else blk(g,p)
        ax.add_patch(Rectangle((g,-p),0.9,0.9, facecolor=COL[b], alpha=0.34,
                               edgecolor='white', lw=0.7))
for i in range(14):
    for r,y in ((0,-8.6),(1,-9.5)):
        ax.add_patch(Rectangle((4+i,y),0.9,0.9, facecolor=COL['f'], alpha=0.34,
                               edgecolor='white', lw=0.7))
for g in range(1,19):
    ax.text(g+0.45, 0.25, str(g), ha='center', va='bottom', fontsize=5.4, color=MUTED)
for p in range(1,8):
    ax.text(0.7, -p+0.45, str(p), ha='right', va='center', fontsize=6.2, color=MUTED)
ax.text(3.7,-8.15,'4f', ha='right', va='center', fontsize=6.2, color=MUTED)
ax.text(3.7,-9.05,'5f', ha='right', va='center', fontsize=6.2, color=MUTED)
ax.text(1.9,-2.1,'s', ha='center', va='center', fontsize=11, color=COL['s'], weight='bold')
ax.text(7.5,-5.1,'d', ha='center', va='center', fontsize=11, color=COL['d'], weight='bold')
ax.text(15.9,-4.1,'p', ha='center', va='center', fontsize=11, color=COL['p'], weight='bold')
ax.text(10.9,-9.05,'f', ha='center', va='center', fontsize=11, color=COL['f'], weight='bold')
ax.text(1.45,-0.55,'H', ha='center', va='center', fontsize=5.6, color=INK)
ax.text(18.45,-0.55,'He', ha='center', va='center', fontsize=5.0, color=INK)
ax.set_xlim(0.2,19.4); ax.set_ylim(-10.7,1.1)
ax.set_aspect('equal'); ax.axis('off')
```

## 4.2 IUPAC classification of elements

The old labels IA, IIA … IB, IIB were used differently in Europe and America, which
caused confusion. In 1988 IUPAC replaced them: the groups are simply numbered
**1 to 18 from left to right**.

| IUPAC group | Old (CAS) | Family name | Valence configuration |
|---|---|---|---|
| 1 | IA | Alkali metals | ns¹ |
| 2 | IIA | Alkaline earth metals | ns² |
| 3–12 | IIIB–IIB | Transition elements | (n−1)d¹⁻¹⁰ns¹⁻² |
| 13 | IIIA | Boron family | ns²np¹ |
| 14 | IVA | Carbon family | ns²np² |
| 15 | VA | Nitrogen family | ns²np³ |
| 16 | VIA | Chalcogens | ns²np⁴ |
| 17 | VIIA | Halogens | ns²np⁵ |
| 18 | 0 | Noble gases | ns²np⁶ (He: 1s²) |

IUPAC also fixed the quarrel over who discovered the very heavy elements by giving
a **systematic name** to every element with $Z > 100$. Write the digits of the
atomic number, replace each digit by its Latin/Greek root, join them in order, and
add **-ium**. The symbol is the first letter of each root.

::: memory The numerical roots
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| nil | un | bi | tri | quad | pent | hex | sept | oct | enn |
| n | u | b | t | q | p | h | s | o | e |

Two spelling rules: **bi + ium → bium** and **tri + ium → trium** (one *i* is
dropped), and **enn + nil → ennil** (one *n* is dropped).
:::

::: example Worked example 4.1 — systematic names
**Problem.** Give the IUPAC systematic name and symbol for the elements with
$Z = 105$, $Z = 109$ and $Z = 113$.

**Solution.**

$Z = 105 \Rightarrow$ 1, 0, 5 → un + nil + pent + ium = **Unnilpentium**, symbol **Unp**.

$Z = 109 \Rightarrow$ 1, 0, 9 → un + nil + enn + ium = **Unnilennium**, symbol **Une**.

$Z = 113 \Rightarrow$ 1, 1, 3 → un + un + tri + ium; *triium* loses one *i*, giving
**Ununtrium**, symbol **Uut**.

(These three are now officially dubnium Db, meitnerium Mt and nihonium Nh, but the
systematic name is what NEB asks you to construct.)
:::

## 4.3 Nuclear charge and effective nuclear charge

The nucleus carries a charge of $+Ze$. An outer electron, however, does not feel
the full pull of $+Ze$, because the electrons between it and the nucleus push it
outwards. This partial cancellation is the **screening** or **shielding effect**,
measured by the screening constant $\sigma$. What the electron actually feels is
the **effective nuclear charge**:

$$ Z_{\text{eff}} = Z - \sigma $$

Screening power depends on how close to the nucleus an orbital keeps its electron.
Penetration falls in the order s > p > d > f, so the shielding power of the
subshells also falls in the order **s > p > d > f**.

::: definition Effective nuclear charge
The effective nuclear charge is the net positive charge actually experienced by a
particular electron in a multi-electron atom, after the shielding due to all the
other electrons has been subtracted from the true nuclear charge.
:::

$\sigma$ can be estimated with **Slater's rules**. Write the configuration in the
groups (1s)(2s,2p)(3s,3p)(3d)(4s,4p)… and, for an electron in an ns or np orbital,
add up:

| Other electrons located in | Contribution to $\sigma$ each |
|---|---|
| a group to the right (higher shells) | 0.00 |
| the same (ns, np) group | 0.35 (but 0.30 in 1s) |
| the shell just inside, $n-1$ | 0.85 |
| shell $n-2$ and deeper | 1.00 |

::: example Worked example 4.2 — effective nuclear charge
**Problem.** Calculate $Z_{\text{eff}}$ felt by a 3s electron of sodium ($Z = 11$)
and by a 3p electron of chlorine ($Z = 17$).

**Solution.** Sodium: (1s²)(2s²2p⁶)(3s¹). The 3s electron has no partner in its
own group, eight electrons in the $n-1$ shell and two in the $n-2$ shell.

$$ \sigma = (0 \times 0.35) + (8 \times 0.85) + (2 \times 1.00) = 0 + 6.80 + 2.00 = 8.80 $$
$$ Z_{\text{eff}} = 11 - 8.80 = 2.20 $$

Chlorine: (1s²)(2s²2p⁶)(3s²3p⁵). The chosen 3p electron has six partners in the
(3s,3p) group, eight electrons in shell 2 and two in shell 1.

$$ \sigma = (6 \times 0.35) + (8 \times 0.85) + (2 \times 1.00) = 2.10 + 6.80 + 2.00 = 10.90 $$
$$ Z_{\text{eff}} = 17 - 10.90 = 6.10 $$

Across period 3 the nuclear charge rises by 6 but the screening rises by only
2.10, so $Z_{\text{eff}}$ almost triples. That single number explains every trend
in the rest of this chapter.
:::

| Period 3 element | Na | Mg | Al | Si | P | S | Cl |
|---|---|---|---|---|---|---|---|
| $Z$ | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| $Z_{\text{eff}}$ (Slater) | 2.20 | 2.85 | 3.50 | 4.15 | 4.80 | 5.45 | 6.10 |
| Atomic radius / pm | 186 | 160 | 143 | 117 | 110 | 104 | 99 |
| IE₁ / kJ mol⁻¹ | 496 | 738 | 578 | 786 | 1012 | 1000 | 1251 |

::: caution Nuclear charge is not effective nuclear charge
Potassium ($Z = 19$) has a far bigger nuclear charge than lithium ($Z = 3$), yet
its valence electron is held much more weakly. The reason is that $Z_{\text{eff}}$
for the outermost electron of *every* alkali metal is only about 2.2, while the
electron sits in a shell of larger and larger $n$. Always compare $Z_{\text{eff}}$
and $n$ together, never $Z$ alone.
:::

## 4.4 Periodic trend and periodicity: atomic radii, ionic radii, ionization energy, electron affinity, electronegativity, metallic character

**Periodicity** is the repetition of similar properties after regular intervals in
the periodic table. It happens because the outer-shell configuration repeats:
every element in group 1 ends in ns¹, so every element in group 1 behaves alike.

### Atomic radii

An atom has no sharp boundary, so radius is always defined operationally.

| Type | Defined as | Used for |
|---|---|---|
| Covalent radius | half the internuclear distance in X–X of a single bond | non-metals, e.g. Cl 99 pm |
| Metallic radius | half the internuclear distance of nearest atoms in the metal crystal | metals, e.g. Na 186 pm |
| van der Waals radius | half the distance of closest approach of two non-bonded atoms | noble gases, e.g. Ar 154 pm |

For the same element van der Waals radius > metallic radius > covalent radius.

**Across a period** the radius *decreases*: $n$ stays the same while
$Z_{\text{eff}}$ rises, pulling the shell in. **Down a group** it *increases*: a
whole new shell is added, which easily beats the rise in $Z_{\text{eff}}$.

```figure caption="Atomic radii from real data. Left: the sharp contraction across periods 2 and 3. Right: the steady expansion down group 1 and group 17."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2,2.7))
lab = ['1','2','13','14','15','16','17']
p2 = [152,111,88,77,74,66,64]; s2 = ['Li','Be','B','C','N','O','F']
p3 = [186,160,143,117,110,104,99]; s3 = ['Na','Mg','Al','Si','P','S','Cl']
x = np.arange(7)
a1.plot(x, p3, 'o-', color=SERIES[1], ms=4, label='period 3')
a1.plot(x, p2, 'o-', color=SERIES[0], ms=4, label='period 2')
for i in (0,6):
    a1.annotate(s2[i], (x[i],p2[i]), textcoords='offset points', xytext=(3,6),
                fontsize=7.5, color=SERIES[0])
    a1.annotate(s3[i], (x[i],p3[i]), textcoords='offset points', xytext=(3,6),
                fontsize=7.5, color=SERIES[1])
a1.set_xticks(x); a1.set_xticklabels(lab, fontsize=7.5)
a1.set_xlabel('group'); a1.set_ylabel('atomic radius / pm')
a1.set_ylim(40,210); a1.legend(fontsize=7.5, loc='upper right')
g1 = [152,186,227,248,265]; g1s = ['Li','Na','K','Rb','Cs']
g17 = [64,99,114,133]; g17s = ['F','Cl','Br','I']
a2.plot([2,3,4,5,6], g1, 'o-', color=SERIES[2], ms=4, label='group 1')
a2.plot([2,3,4,5], g17, 'o-', color=SERIES[3], ms=4, label='group 17')
for p,v,s in zip([2,3,4,5,6], g1, g1s):
    a2.annotate(s, (p,v), textcoords='offset points', xytext=(-3,7), fontsize=7.5, color=SERIES[2])
for p,v,s in zip([2,3,4,5], g17, g17s):
    a2.annotate(s, (p,v), textcoords='offset points', xytext=(-3,-12), fontsize=7.5, color=SERIES[3])
a2.set_xticks([2,3,4,5,6]); a2.set_xlabel('period')
a2.set_ylim(40,300); a2.legend(fontsize=7.5, loc='upper left')
for a in (a1,a2):
    a.spines[['top','right']].set_visible(False); a.grid(True, alpha=.45)
fig.tight_layout()
```

### Ionic radii

A **cation is always smaller** than its parent atom: Na (186 pm) → Na⁺ (95 pm),
because the whole 3s shell is removed and the remaining 10 electrons are pulled in
by 11 protons. An **anion is always larger**: Cl (99 pm) → Cl⁻ (181 pm), because
the added electron increases electron–electron repulsion while $Z$ is unchanged.

For an **isoelectronic series** — ions with the same number of electrons — size
falls as nuclear charge rises:

| Ion | N³⁻ | O²⁻ | F⁻ | Ne | Na⁺ | Mg²⁺ | Al³⁺ |
|---|---|---|---|---|---|---|---|
| Electrons | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Protons | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
| Radius / pm | 171 | 140 | 136 | — | 95 | 65 | 50 |

::: example Worked example 4.3 — ordering ions by size
**Problem.** Arrange O²⁻, F⁻, Na⁺, Mg²⁺ in increasing order of ionic radius and
justify your answer.

**Solution.** Each ion has 10 electrons, so the screening is identical. Only the
nuclear charge differs: Mg²⁺ (12 p) > Na⁺ (11 p) > F⁻ (9 p) > O²⁻ (8 p). The
charge per electron is $12/10 = 1.20$, $1.10$, $0.90$ and $0.80$ respectively, so
the pull on each electron weakens in that order and the ions swell:

**Mg²⁺ (65) < Na⁺ (95) < F⁻ (136) < O²⁻ (171) pm.**
:::

### Ionization energy

::: definition Ionization energy
The **first ionization energy** (IE₁) is the minimum energy required to remove the
most loosely bound electron from one mole of isolated gaseous atoms in their
ground state: M(g) + IE₁ → M⁺(g) + e⁻. It is measured in kJ mol⁻¹ or eV atom⁻¹
(1 eV atom⁻¹ = 96.5 kJ mol⁻¹).
:::

Successive values always increase, IE₁ < IE₂ < IE₃ …, because each electron is
pulled from an ion of higher positive charge. A very big jump marks the point at
which a noble-gas core is broken: for sodium IE₁ = 496 but IE₂ = 4562 kJ mol⁻¹,
which is why sodium forms Na⁺ and never Na²⁺.

Ionization energy **increases across a period** ($Z_{\text{eff}}$ up, size down)
and **decreases down a group** (size up, shielding up).

```figure caption="First ionization energy against atomic number for the first 20 elements. Noble gases are maxima, alkali metals minima; the dips at B, O, Al and S are the half-filled and fully-filled anomalies."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,2.9))
sym = ['H','He','Li','Be','B','C','N','O','F','Ne',
       'Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca']
ie = [1312,2372,520,899,801,1086,1402,1314,1681,2081,
      496,738,578,786,1012,1000,1251,1521,419,590]
z = np.arange(1,21)
ax.plot(z, ie, '-o', color=ACCENT, ms=3.4, lw=1.4)
for i,(s,v) in enumerate(zip(sym,ie)):
    if s in ('He','Ne','Ar'):
        ax.annotate(s,(z[i],v),textcoords='offset points',xytext=(0,6),
                    ha='center',fontsize=7.6,color='#A8271F')
    elif s in ('Li','Na','K'):
        ax.annotate(s,(z[i],v),textcoords='offset points',xytext=(0,-13),
                    ha='center',fontsize=7.6,color=SERIES[2])
for s,i in (('B',4),('O',7),('Al',12),('S',15)):
    ax.plot([z[i]],[ie[i]],'o',color='#b8860b',ms=6.5,mfc='none',mew=1.3)
    ax.annotate(s,(z[i],ie[i]),textcoords='offset points',xytext=(5,-9),
                fontsize=7.4,color='#b8860b')
ax.set_xlabel('atomic number  $Z$'); ax.set_ylabel('IE$_1$ / kJ mol$^{-1}$')
ax.set_xticks([1,5,10,15,20]); ax.set_xlim(0,21); ax.set_ylim(0,2600)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
```

Two irregularities are asked almost every year:

- **Be (899) > B (801).** Beryllium's electron leaves a filled 2s² orbital, while
  boron's leaves a 2p orbital that is higher in energy and well shielded by 2s².
- **N (1402) > O (1314).** Nitrogen is 2p³, a half-filled subshell with extra
  exchange stability and no paired electron. Oxygen is 2p⁴; the two electrons
  paired in one 2p orbital repel each other, so one is easier to pull off.

The same pair of reasons gives Mg > Al and P > S in period 3.

### Electron affinity

::: definition Electron affinity
Electron affinity is the energy **released** when an electron is added to one mole
of isolated gaseous atoms in the ground state: X(g) + e⁻ → X⁻(g) + energy. A large
positive electron affinity means a strong pull for the extra electron (the
corresponding enthalpy change ΔH is negative).
:::

Second electron affinity is always **endothermic**, because the electron must be
forced onto an already negative ion: O⁻(g) + e⁻ → O²⁻(g) needs about
+780 kJ mol⁻¹. Electron affinity rises across a period and falls down a group, but
the first member of each group breaks the rule.

```figure caption="Left: electronegativity across period 3 and down group 17. Right: electron affinity, showing that Cl beats F and S beats O because the 2p subshell is too compact."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2,2.7))
p3 = ['Na','Mg','Al','Si','P','S','Cl']; en3 = [0.9,1.2,1.5,1.8,2.1,2.5,3.0]
a1.plot(range(7), en3, 'o-', color=SERIES[0], ms=4, label='period 3 (across)')
g17 = ['F','Cl','Br','I']; en17 = [4.0,3.0,2.8,2.5]
a1.plot(range(4), en17, 's--', color=SERIES[1], ms=4, label='group 17 (down)')
a1.set_xticks(range(7)); a1.set_xticklabels(p3, fontsize=7.4)
for i,s in enumerate(g17):
    a1.annotate(s,(i,en17[i]),textcoords='offset points',xytext=(2,6),
                fontsize=7.2,color=SERIES[1])
a1.set_ylabel('electronegativity (Pauling)'); a1.set_ylim(0.5,4.6)
a1.legend(fontsize=6.8, loc='upper left')
x = np.arange(4); w = 0.38
ea17 = [328,349,325,295]; ea16 = [141,200,195,190]
a2.bar(x-w/2, ea17, w, color=SERIES[1], label='group 17')
a2.bar(x+w/2, ea16, w, color=SERIES[2], label='group 16')
a2.set_xticks(x); a2.set_xticklabels(['period 2','3','4','5'], fontsize=7.2)
a2.set_ylabel('electron affinity / kJ mol$^{-1}$'); a2.set_ylim(0,430)
a2.annotate('F < Cl', (0.0,345), textcoords='offset points', xytext=(-2,10),
            fontsize=7.4, color='#A8271F')
a2.legend(fontsize=7.0, loc='upper right')
for a in (a1,a2):
    a.spines[['top','right']].set_visible(False); a.grid(True, axis='y', alpha=.45)
fig.tight_layout()
```

Fluorine (328) has a *smaller* electron affinity than chlorine (349), and oxygen
(141) a smaller one than sulphur (200): in F and O the 2p subshell is so compact
that the electrons already there repel the incoming one strongly. Groups 2, 15 and
18 have near-zero or negative values because their subshells are filled or
half-filled.

### Electronegativity

::: definition Electronegativity
Electronegativity is the tendency of an atom **in a molecule** to attract the
shared pair of electrons towards itself. It is a relative, dimensionless number;
on Pauling's scale fluorine, the most electronegative element, is 4.0 and caesium
is 0.7.
:::

It increases across a period and decreases down a group. It is **not** the same as
electron affinity: electron affinity belongs to an isolated atom and is an energy
in kJ mol⁻¹, whereas electronegativity belongs to a bonded atom and has no units.
The electronegativity difference decides whether a bond is non-polar covalent,
polar covalent or ionic (Unit 5).

### Metallic character

Metallic (electropositive) character is the tendency to *lose* electrons. It runs
opposite to ionization energy: it **decreases across a period** and **increases
down a group**. The diagonal staircase B, Si, Ge, As, Sb, Te (the metalloids)
marks the metal / non-metal boundary.

| Property | Across a period (left → right) | Down a group | Main reason |
|---|---|---|---|
| Atomic radius | decreases | increases | $Z_{\text{eff}}$ vs new shell |
| Ionic radius | decreases (same charge) | increases | same |
| Ionization energy | increases | decreases | $Z_{\text{eff}}$ vs size and shielding |
| Electron affinity | increases | decreases | $Z_{\text{eff}}$ vs size |
| Electronegativity | increases | decreases | $Z_{\text{eff}}$ vs size |
| Metallic character | decreases | increases | opposite of IE |
| Valency w.r.t. oxygen | 1 → 7 | constant | valence electrons |

## Chapter summary

- Modern periodic law: properties are periodic functions of **atomic number**,
  established by Moseley's relation $\sqrt{\nu} = a(Z-b)$.
- The long form has 7 periods (2, 8, 8, 18, 18, 32, 32 elements) and 18 IUPAC
  groups; blocks s, p, d, f are named after the subshell filled last.
- Elements with $Z > 100$ are named systematically from the roots nil, un, bi,
  tri, quad, pent, hex, sept, oct, enn plus **-ium**.
- $Z_{\text{eff}} = Z - \sigma$; screening power falls as s > p > d > f.
  Slater's rules give $Z_{\text{eff}} = 2.20$ for Na(3s) and 6.10 for Cl(3p).
- Across a period: radius ↓, IE ↑, EA ↑, EN ↑, metallic character ↓.
  Down a group: radius ↑, IE ↓, EA ↓, EN ↓, metallic character ↑.
- Cations are smaller and anions larger than the parent atom; in an isoelectronic
  series radius falls as the number of protons rises.
- Anomalies: Be > B and N > O (and Mg > Al, P > S) in ionization energy because of
  filled 2s and half-filled 2p stability; Cl > F and S > O in electron affinity
  because the second-period atoms are too compact.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. An element has the configuration [Ar] 3d¹⁰ 4s² 4p³. It belongs to <span class="marks">[1]</span>
   (a) group 13, p-block (b) group 15, p-block (c) group 5, d-block (d) group 15, d-block
2. The correct order of ionic radii is <span class="marks">[1]</span>
   (a) Al³⁺ > Mg²⁺ > Na⁺ > F⁻ (b) O²⁻ > F⁻ > Na⁺ > Mg²⁺ (c) Na⁺ > F⁻ > O²⁻ > N³⁻ (d) F⁻ > O²⁻ > N³⁻ > Na⁺
3. The first ionization energy of nitrogen is greater than that of oxygen because <span class="marks">[1]</span>
   (a) nitrogen has higher nuclear charge (b) nitrogen has a half-filled 2p subshell
   (c) oxygen is more electronegative (d) oxygen has a larger radius
4. The IUPAC systematic name of the element with $Z = 106$ is <span class="marks">[1]</span>
   (a) Unnilhexium (b) Unnilsextium (c) Ununhexium (d) Unhexium
5. Using Slater's rules, the effective nuclear charge felt by the 3s electron of sodium is <span class="marks">[1]</span>
   (a) 11.00 (b) 8.80 (c) 2.20 (d) 1.00

::: note Answers to Group A
**1.** (b) — the last electron enters 4p, so p-block; 2 + 3 = 5 valence electrons gives group 15 (arsenic, $Z = 33$).

**2.** (b) — all are isoelectronic with 10 electrons, so radius falls as protons rise: 8 < 9 < 11 < 12.

**3.** (b) — 2p³ is half-filled and has no paired 2p electron, so it is extra stable.

**4.** (a) — 1, 0, 6 → un + nil + hex + ium.

**5.** (c) — $\sigma = 8(0.85) + 2(1.00) = 8.80$, so $Z_{\text{eff}} = 11 - 8.80 = 2.20$.
:::

**Group B — Short answer (5 marks each)**

1. State the modern periodic law. Explain, in terms of orbital filling, why the
   second period contains 8 elements while the fourth contains 18. <span class="marks">[5]</span>
2. Define effective nuclear charge. Using Slater's rules calculate $Z_{\text{eff}}$
   for a 3p electron of phosphorus ($Z=15$) and of sulphur ($Z=16$), and comment on
   the result. <span class="marks">[5]</span>
3. Define ionization energy. Why is the second ionization energy of sodium
   (4562 kJ mol⁻¹) nearly nine times the first (496 kJ mol⁻¹)? <span class="marks">[5]</span>
4. Why is the electron affinity of fluorine smaller than that of chlorine even
   though fluorine is the more electronegative element? Distinguish clearly between
   electron affinity and electronegativity. <span class="marks">[5]</span>
5. Arrange with reasons: (i) Li, Be, B, C in increasing atomic radius;
   (ii) N³⁻, O²⁻, F⁻, Na⁺ in decreasing ionic radius. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Properties are periodic functions of atomic number. Period 2 fills 2s and
2p only: 1 + 3 = 4 orbitals × 2 electrons = 8 elements. Period 4 fills 4s, then
3d, then 4p: 1 + 5 + 3 = 9 orbitals × 2 = 18 elements.

**2.** $Z_{\text{eff}} = Z - \sigma$. Phosphorus (1s²)(2s²2p⁶)(3s²3p³):
$\sigma = 4(0.35)+8(0.85)+2(1.00) = 1.40+6.80+2.00 = 10.20$, so
$Z_{\text{eff}} = 15-10.20 = 4.80$. Sulphur (3s²3p⁴):
$\sigma = 5(0.35)+6.80+2.00 = 10.55$, so $Z_{\text{eff}} = 16-10.55 = 5.45$. Adding
one proton raises $Z_{\text{eff}}$ by only 0.65 because the new electron screens
0.35 of it — this is why atoms shrink only gradually across a period.

**3.** IE₁ removes the 3s¹ electron from a neutral atom. IE₂ must break into the
filled 2s²2p⁶ neon core of Na⁺, where the electron is in a lower shell, feels a
much larger $Z_{\text{eff}}$ and must be pulled away from a positive ion. Hence
the huge jump, and hence sodium's valency of 1.

**4.** Adding an electron to the very small fluorine atom forces it into a compact
2p subshell where inter-electronic repulsion is severe; chlorine's 3p subshell is
larger, so more energy is released (F 328, Cl 349 kJ mol⁻¹). Electron affinity is
an energy (kJ mol⁻¹) belonging to an isolated gaseous *atom*; electronegativity is
a dimensionless relative number describing a *bonded* atom's pull on a shared pair.

**5.** (i) C (77) < B (88) < Be (111) < Li (152) pm: across period 2, $n$ is fixed
but $Z_{\text{eff}}$ rises, so the shell contracts. (ii) N³⁻ (171) > O²⁻ (140) >
F⁻ (136) > Na⁺ (95) pm: isoelectronic, so radius falls as protons rise.
:::

**Group C — Long answer (8 marks each)**

1. (a) Classify the elements into s-, p-, d- and f-blocks, giving the general outer
   electronic configuration and one example of each. <span class="marks">[4]</span>
   (b) Discuss the variation of atomic radius and first ionization energy along
   period 3, and explain the irregularities observed at aluminium and sulphur. <span class="marks">[4]</span>
2. (a) Define ionization energy, electron affinity and electronegativity, and state
   how each varies across a period and down a group, with the reason. <span class="marks">[5]</span>
   (b) An element X has atomic number 26. Write its ground-state electronic
   configuration and deduce its period, group and block. <span class="marks">[3]</span>

::: note Answers to Group C
**1.(b)** Radius falls steadily 186 → 99 pm because $Z_{\text{eff}}$ climbs from
2.20 to 6.10 while $n = 3$ throughout. IE₁ rises overall 496 → 1251 kJ mol⁻¹ but
dips twice. Al (578) < Mg (738): aluminium's electron comes from 3p, which is
higher in energy and shielded by the filled 3s². S (1000) < P (1012): phosphorus
is 3p³, half-filled and stable, whereas sulphur is 3p⁴ with one repelling pair.

**2.(b)** X is iron: 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁶ 4s². The outermost shell is $n = 4$,
so the **period is 4**. The last electron enters 3d, so it is a **d-block**
element, and for groups 3–10 the group number = (number of d electrons) +
(number of s electrons) = 6 + 2 = **group 8**. Common oxidation states +2 and +3.
:::

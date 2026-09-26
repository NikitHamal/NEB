---
subject: Chemistry
grade: 11
unit: 5
title: Chemical Bonding and Shapes of Molecules
hours: 9
area: General and Physical Chemistry
---

Almost nothing in nature exists as free atoms. Atoms join because the combination
has lower energy than the separate atoms, and *how* they join — by transferring
electrons, sharing them, or pooling them — decides everything about the substance:
whether it melts at 801 °C like NaCl or boils at −161 °C like CH₄, whether it
conducts, and what it dissolves in.

::: key The three questions the exam asks
(i) *Why* does this bond form — in terms of electrons and octets? (ii) *What
shape* is the molecule — from VSEPR and hybridisation, with the bond angle?
(iii) *What property* follows — melting point, conductivity, solubility, dipole
moment. Learn to answer all three for any formula you are given.
:::

## 5.1 Valence shell, valence electron and octet theory

The **valence shell** is the outermost shell of an atom; the electrons in it are
the **valence electrons**, and only these take part in bonding. Sodium
(2, 8, 1) has one; chlorine (2, 8, 7) has seven.

In 1916 Kössel and Lewis noted that the noble gases — with ns²np⁶ — are almost
completely unreactive, which gives the **octet rule**.

::: definition Octet rule
Atoms combine by losing, gaining or sharing electrons so as to acquire eight
electrons in their valence shell, the configuration of the nearest noble gas.
H, He, Li and Be aim for a **duplet** (two electrons) instead.
:::

The rule is a good first guess, not a law. It fails in four ways:

| Failure | Examples |
|---|---|
| Incomplete octet | BeCl₂ (4 e⁻ on Be), BF₃ (6 e⁻ on B), AlCl₃ |
| Expanded octet (elements of period 3 onwards, which have vacant d orbitals) | PCl₅ (10 e⁻), SF₆ (12 e⁻), IF₇ |
| Odd-electron molecules | NO (11 e⁻), NO₂, ClO₂ |
| Noble gases do react | XeF₂, XeF₄, XeO₃ |

It also says nothing about the **shape** or the **strength** of a bond — which is
why the rest of this unit exists.

## 5.2 Ionic bond and its properties

::: definition Ionic (electrovalent) bond
The electrostatic force of attraction that holds together the oppositely charged
ions produced by the **complete transfer** of one or more electrons from a metal
atom to a non-metal atom.
:::

Na (2, 8, 1) − e⁻ → Na⁺ (2, 8) and Cl (2, 8, 7) + e⁻ → Cl⁻ (2, 8, 8), so

2Na + Cl₂ → 2Na⁺Cl⁻

Three conditions favour it: **low ionization energy** of the metal, **high
electron affinity** of the non-metal, and a **high lattice energy** — the energy
released when one mole of the crystal forms from its gaseous ions. As a working
rule ΔEN must exceed about **1.7** (Na–Cl is 3.0 − 0.9 = 2.1). Lattice energy is
788 kJ mol⁻¹ for NaCl but 3791 kJ mol⁻¹ for MgO, whose ions carry double charges
— hence melting points of 801 °C and 2852 °C.

The electrostatic field of an ion is the same in every direction, so the ionic
bond is **non-directional**: there is no "molecule" of NaCl, only a giant lattice
in which every Na⁺ touches six Cl⁻.

## 5.3 Covalent bond and coordinate covalent bond; properties of covalent compounds

A **covalent bond** is formed by the **mutual sharing** of one or more electron
pairs between two atoms, each contributing an equal number of electrons. Sharing
one pair gives a single bond (H–H), two pairs a double bond (O=O), three pairs a
triple bond (N≡N).

::: definition Coordinate (dative) covalent bond
A covalent bond in which **both** the shared electrons come from the same atom.
The atom supplying the lone pair is the **donor**, the atom with the empty orbital
is the **acceptor**, and the bond is written as an arrow from donor to acceptor.
:::

Two standard examples: NH₃ + H⁺ → NH₄⁺ (the lone pair on N is donated to a bare
proton) and NH₃ + BF₃ → H₃N→BF₃ (the same lone pair completes boron's octet).
Once formed, a coordinate bond is indistinguishable from an ordinary covalent
bond — all four N–H bonds in NH₄⁺ are identical.

| Property | Ionic compounds | Covalent compounds |
|---|---|---|
| Physical state | hard, brittle crystalline solids | gases, liquids or soft solids |
| Melting / boiling point | very high (NaCl 801 °C) | low (CCl₄ 77 °C) |
| Electrical conduction | conduct when molten or in water, not when solid | do not conduct (no free ions) |
| Solubility | soluble in polar solvents (water) | soluble in non-polar solvents (benzene, ether) |
| Nature of bond | non-directional | strongly directional |
| Isomerism | not shown | shown |
| Rate of reaction | fast (ionic reactions) | slow (bonds must break) |

## 5.4 Lewis dot structure of common compounds of s and p block elements

A Lewis (electron-dot) structure shows every valence electron as a dot — shared
pairs between the symbols, lone pairs around them. To draw one:

1. Add up the valence electrons of all atoms; **add** one for each negative charge
   and **subtract** one for each positive charge. Call this $A$.
2. Work out the electrons needed to give every atom a full shell (8 each, 2 for
   hydrogen). Call this $N$.
3. The number of **shared** electrons is $S = N - A$, i.e. $S/2$ bond pairs.
4. The remaining $(A - S)/2$ pairs are placed as lone pairs, oxygen and the
   halogens first.

```figure caption="Lewis dot structures. Every dot is one valence electron; a shared pair lies between two symbols and a lone pair belongs to one atom. In NH₄⁺ the red pair came entirely from nitrogen."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(5.2, 3.4))

def dot(ax, x, y, c=INK, s=13):
    ax.scatter([x], [y], s=s, color=c, zorder=6, linewidths=0)

def sym(ax, x, y, t, c=INK, fs=11.5):
    ax.text(x, y, t, ha='center', va='center', fontsize=fs, color=c, zorder=7)

def shared(ax, a, b, order=1, c=INK, gap=0.30):
    """n pairs of dots between atom centres a and b."""
    a = np.array(a, float); b = np.array(b, float)
    u = (b - a); L = np.hypot(*u); u = u / L
    p = np.array([-u[1], u[0]])
    mid = a + u * (L / 2)
    offs = {1: [0.0], 2: [0.11, -0.11], 3: [0.15, 0.0, -0.15]}[order]
    for o in offs:
        for s in (+1, -1):
            d = mid + p * o + u * (s * 0.055)
            dot(ax, d[0], d[1], c)

def lp(ax, cen, ang, r=0.40, sep=0.115, c=INK):
    cen = np.array(cen, float)
    th = np.radians(ang)
    u = np.array([np.cos(th), np.sin(th)]); p = np.array([-u[1], u[0]])
    for s in (+1, -1):
        d = cen + u * r + p * s * sep / 2
        dot(ax, d[0], d[1], c)

for ax in axes.ravel():
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.0, 1.0)
    ax.set_aspect('equal'); ax.axis('off')

# --- H2O : two bond pairs + two lone pairs -> bent
ax = axes[0, 0]
O = (0, -0.05)
H1 = (-0.72, -0.48); H2 = (0.72, -0.48)
sym(ax, *O, 'O'); sym(ax, *H1, 'H'); sym(ax, *H2, 'H')
shared(ax, O, H1); shared(ax, O, H2)
lp(ax, O, 62, r=0.40); lp(ax, O, 118, r=0.40)
ax.set_title('H$_2$O', fontsize=9.5, pad=1)
ax.text(0, -0.88, '2 bond pairs + 2 lone pairs', ha='center', fontsize=7.2, color=MUTED)

# --- CO2 : two double bonds, no lone pair on C
ax = axes[0, 1]
C = (0, -0.05); Oa = (-0.80, -0.05); Ob = (0.80, -0.05)
sym(ax, *C, 'C'); sym(ax, *Oa, 'O'); sym(ax, *Ob, 'O')
shared(ax, C, Oa, 2); shared(ax, C, Ob, 2)
lp(ax, Oa, 90, r=0.33); lp(ax, Oa, 180, r=0.33)
lp(ax, Ob, 90, r=0.33); lp(ax, Ob, 0, r=0.33)
ax.set_title('CO$_2$', fontsize=9.5, pad=1)
ax.text(0, -0.88, 'two double bonds, octet on every atom', ha='center', fontsize=7.2, color=MUTED)

# --- N2 : triple bond
ax = axes[1, 0]
Na = (-0.42, 0.0); Nb = (0.42, 0.0)
sym(ax, *Na, 'N'); sym(ax, *Nb, 'N')
shared(ax, Na, Nb, 3)
lp(ax, Na, 180, r=0.33); lp(ax, Nb, 0, r=0.33)
ax.set_title('N$_2$', fontsize=9.5, pad=1)
ax.text(0, -0.88, 'triple bond: three shared pairs', ha='center', fontsize=7.2, color=MUTED)

# --- NH4+ : coordinate bond shown in colour
ax = axes[1, 1]
DON = '#A8271F'
N = (0.0, -0.05)
Hs = [(0.0, 0.62), (-0.68, -0.05), (0.0, -0.72)]
Hd = (0.68, -0.05)
sym(ax, *N, 'N');
for h in Hs:
    sym(ax, *h, 'H'); shared(ax, N, h)
sym(ax, *Hd, 'H')
shared(ax, N, Hd, c=DON)
ax.annotate('', xy=(0.66, 0.16), xytext=(0.06, 0.16),
            arrowprops=dict(arrowstyle='-|>', color=DON, lw=1.2, mutation_scale=9,
                            connectionstyle='arc3,rad=-0.20'))
ax.text(1.17, 0.66, '+', fontsize=11, color=INK, ha='center', va='center')
ax.plot([0.98, 1.06, 1.06, 0.98], [0.82, 0.82, -0.92, -0.92], color=INK, lw=0.8)
ax.plot([-1.06, -1.14, -1.14, -1.06], [0.82, 0.82, -0.92, -0.92], color=INK, lw=0.8)
ax.set_title('NH$_4^{+}$', fontsize=9.5, pad=1)
ax.text(0, -0.99, 'red = coordinate bond (both electrons from N)',
        ha='center', fontsize=7.0, color=DON)
fig.subplots_adjust(wspace=0.02, hspace=0.30)
```

::: example Worked example 5.1 — Lewis structure of SO₂
**Problem.** Draw the Lewis structure of sulphur dioxide and assign formal charges.

**Solution.** Step 1: $A = 6 + 2(6) = 18$ valence electrons.

Step 2: $N = 3 \times 8 = 24$ electrons for three complete octets.

Step 3: shared electrons $S = N - A = 24 - 18 = 6$, i.e. **3 bond pairs**. With
only two S–O links, one must be a double bond and the other a single bond.

Step 4: lone pairs $= (A - S)/2 = (18-6)/2 = 6$ pairs — one on S, two on the
doubly bonded O, three on the singly bonded O.

Formal charge = (valence electrons) − (lone-pair electrons) − ½(bonding electrons):

$$ \text{S}: 6 - 2 - \tfrac{1}{2}(6) = +1, \quad \text{O(double)}: 6 - 4 - \tfrac{1}{2}(4) = 0, \quad \text{O(single)}: 6 - 6 - \tfrac{1}{2}(2) = -1 $$

So the structure is O=S⁺–O⁻. Since the double bond could equally be on the other
oxygen, SO₂ is a **resonance hybrid** of two such forms, and both S–O bonds are
found to be the same length (143 pm) with an O–S–O angle of 119.5°.
:::

## 5.5 Resonance

When a single Lewis structure cannot account for all the observed properties of a
molecule, several structures are written that differ **only in the positions of
electrons**, never of atoms.

::: definition Resonance
The actual structure of such a molecule is a **resonance hybrid** — a single
structure intermediate between all the contributing (canonical) forms, and more
stable than any of them. The extra stability is the **resonance energy**.
:::

Conditions: the canonical forms must have the same arrangement of atoms, the same
number of paired electrons, and roughly comparable energies.

```figure caption="Resonance. The carbonate ion has three equivalent canonical forms, so all three C–O bonds are identical and intermediate between a single and a double bond."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle

fig, ax = plt.subplots(figsize=(5.2, 3.2))
CEN = '#1d6fb8'; OUT = '#d9534f'

def atom(ax, p, t, r=0.20, ec=CEN, fs=8.5):
    ax.add_patch(Circle(p, r, facecolor='white', edgecolor=ec, lw=1.1, zorder=5))
    ax.text(p[0], p[1], t, ha='center', va='center', fontsize=fs, color=INK, zorder=6)

def bond(ax, a, b, order=1, ra=0.22, rb=0.22):
    a = np.array(a, float); b = np.array(b, float)
    u = b - a; L = np.hypot(*u); u = u / L; n = np.array([-u[1], u[0]])
    p, q = a + u * ra, b - u * rb
    offs = [0.0] if order == 1 else [0.055, -0.055]
    for o in offs:
        ax.plot([p[0] + n[0] * o, q[0] + n[0] * o],
                [p[1] + n[1] * o, q[1] + n[1] * o], color=INK, lw=1.15, zorder=3)

def charge(ax, p, cen, t, d=0.34):
    p = np.array(p, float); c = np.array(cen, float)
    u = p - c; u = u / np.hypot(*u)
    ax.text(p[0] + u[0] * d, p[1] + u[1] * d, t, ha='center', va='center',
            fontsize=7.4, color=OUT, zorder=7)

def carbonate(cx, cy, dbl):
    C = np.array([cx, cy])
    pos = {}
    for k, a in zip((0, 1, 2), (90, 210, 330)):
        t = np.radians(a)
        pos[k] = C + 0.66 * np.array([np.cos(t), np.sin(t)])
    for k in pos:
        bond(ax, C, pos[k], 2 if k == dbl else 1)
        atom(ax, pos[k], 'O', ec=OUT)
        if k != dbl:
            charge(ax, pos[k], C, '−')
    atom(ax, C, 'C')
    ax.plot([cx-1.08, cx-1.20, cx-1.20, cx-1.08], [cy+0.98, cy+0.98, cy-0.92, cy-0.92],
            color=INK, lw=0.8)
    ax.plot([cx+1.08, cx+1.20, cx+1.20, cx+1.08], [cy+0.98, cy+0.98, cy-0.92, cy-0.92],
            color=INK, lw=0.8)
    ax.text(cx + 1.40, cy + 0.80, '2−', fontsize=8.0, color=INK, ha='center')

def ozone(cx, cy, flip):
    O2 = np.array([cx, cy + 0.30])
    L = np.array([cx - 0.72, cy - 0.28]); R = np.array([cx + 0.72, cy - 0.28])
    bond(ax, O2, L, 2 if flip else 1)
    bond(ax, O2, R, 1 if flip else 2)
    atom(ax, O2, 'O', ec=OUT); atom(ax, L, 'O', ec=OUT); atom(ax, R, 'O', ec=OUT)
    ax.text(O2[0] + 0.02, O2[1] + 0.36, '+', fontsize=7.6, color=OUT, ha='center')
    end = L if flip == 0 else R
    sx = -0.38 if flip == 0 else 0.38
    ax.text(end[0] + sx, end[1] - 0.04, '−', fontsize=7.6, color=OUT, ha='center')

def dblarrow(x, y):
    ax.annotate('', xy=(x + 0.34, y), xytext=(x - 0.34, y),
                arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.1, mutation_scale=9))

for i, (cx, d) in enumerate(zip([1.50, 4.72, 7.94], [0, 1, 2])):
    carbonate(cx, 1.55, d)
for x in (3.11, 6.33):
    dblarrow(x, 1.55)
ax.text(4.72, 3.00, 'CO$_3^{2-}$  — three equivalent canonical forms',
        ha='center', fontsize=8.2, color=INK)
ax.text(4.72, 0.28, 'all three C–O bonds are identical, length 129 pm '
        '(C–O 143 pm, C=O 122 pm)', ha='center', fontsize=6.9, color=MUTED)

ozone(3.05, -1.35, 0)
dblarrow(4.72, -1.28)
ozone(6.39, -1.35, 1)
ax.text(4.72, -0.42, 'O$_3$  — two canonical forms', ha='center', fontsize=8.2, color=INK)
ax.text(4.72, -2.32, 'resonance energy of ozone ≈ 143 kJ mol$^{-1}$',
        ha='center', fontsize=6.9, color=MUTED)

ax.set_xlim(-0.1, 9.6); ax.set_ylim(-2.62, 3.25)
ax.set_aspect('equal'); ax.axis('off')
```

::: caution Resonance is not oscillation
The carbonate ion does **not** flip between the three structures. It has one
structure — the hybrid — at all times. The canonical forms are imaginary pictures
we draw because our dot notation cannot show a delocalised pair, just as a mule is
not a horse on Sundays and a donkey on Mondays.
:::

## 5.6 VSEPR theory and shapes of simple molecules

The **Valence Shell Electron Pair Repulsion** theory (Sidgwick and Powell,
developed by Gillespie and Nyholm) predicts shape from electron-pair counting
alone. Its postulates:

1. The shape of a molecule depends on the **total number of electron pairs**
   (bonding + lone) in the valence shell of the central atom.
2. These pairs repel one another and arrange themselves as far apart as possible.
3. Repulsion falls in the order **lone pair–lone pair > lone pair–bond pair >
   bond pair–bond pair**, so lone pairs squeeze the bond angles.
4. A multiple bond is treated as a single "super pair" for counting shape, but it
   repels more strongly than a single bond.

The number of electron pairs $X$ around the central atom is

$$ X = \tfrac{1}{2}\left(V + M - c + a\right) $$

where $V$ is the number of valence electrons of the central atom, $M$ the number
of monovalent atoms attached, $c$ the positive charge and $a$ the negative charge
on the ion.

```figure caption="Shapes predicted by VSEPR. Bond angles are the experimental values; note how each lone pair on N and O pushes the bond angle below the tetrahedral 109.5°."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Arc

fig, axes = plt.subplots(3, 3, figsize=(5.2, 4.6))
CEN = '#1d6fb8'; OUT = '#d9534f'; LP = '#A8271F'

def atom(ax, p, t, r=0.145, fc='#ffffff', ec=CEN, fs=8.0):
    ax.add_patch(Circle(p, r, facecolor=fc, edgecolor=ec, lw=1.1, zorder=5))
    ax.text(p[0], p[1], t, ha='center', va='center', fontsize=fs, color=INK, zorder=6)

def _trim(a, b, ra, rb):
    a = np.array(a, float); b = np.array(b, float)
    u = (b - a); L = np.hypot(*u); u = u / L
    return a + u * ra, b - u * rb, u

def bond(ax, a, b, ra=0.16, rb=0.15):
    p, q, u = _trim(a, b, ra, rb)
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=1.2, zorder=3)

def wedge(ax, a, b, ra=0.16, rb=0.15, w=0.075):
    p, q, u = _trim(a, b, ra, rb)
    n = np.array([-u[1], u[0]])
    ax.add_patch(Polygon([p, q + n * w, q - n * w], closed=True,
                         facecolor=INK, edgecolor=INK, lw=0.4, zorder=3))

def dash(ax, a, b, ra=0.17, rb=0.15, n=5, w=0.075):
    p, q, u = _trim(a, b, ra, rb)
    nv = np.array([-u[1], u[0]])
    for i in range(n):
        t = (i + 0.7) / (n + 0.4)
        c = p + (q - p) * t
        hw = w * (0.30 + 0.70 * t)
        ax.plot([c[0] - nv[0] * hw, c[0] + nv[0] * hw],
                [c[1] - nv[1] * hw, c[1] + nv[1] * hw], color=INK, lw=1.0, zorder=3)

def lonepair(ax, cen, ang, r=0.34, sep=0.13):
    cen = np.array(cen, float); th = np.radians(ang)
    u = np.array([np.cos(th), np.sin(th)]); pv = np.array([-u[1], u[0]])
    for s in (+1, -1):
        d = cen + u * r + pv * s * sep / 2
        ax.scatter([d[0]], [d[1]], s=15, color=LP, zorder=7, linewidths=0)

def ang(ax, cen, a1, a2, txt, r=0.40, tr=0.52, c=MUTED, tpos=None):
    ax.add_patch(Arc(cen, 2 * r, 2 * r, theta1=a1, theta2=a2, color=c, lw=0.9, zorder=4))
    if tpos is None:
        m = np.radians((a1 + a2) / 2)
        tpos = (cen[0] + tr * np.cos(m), cen[1] + tr * np.sin(m))
    ax.text(tpos[0], tpos[1], txt, ha='center', va='center', fontsize=6.8,
            color=c, zorder=8, bbox=dict(boxstyle='square,pad=0.08', fc='white',
                                         ec='none', alpha=0.85))

def frame(ax, title, sub):
    ax.set_xlim(-1.14, 1.14); ax.set_ylim(-1.30, 1.36)
    ax.set_aspect('equal'); ax.axis('off')
    ax.text(0, 1.33, title, ha='center', va='top', fontsize=9.0, color=INK)
    ax.text(0, -1.27, sub, ha='center', va='bottom', fontsize=6.6, color=MUTED)

def pol(a, r):
    t = np.radians(a); return (r * np.cos(t), r * np.sin(t))

A = axes.ravel()

# 1 BeF2 - linear
ax = A[0]; C = (0, 0.05)
for a in (0, 180):
    p = pol(a, 0.72); p = (p[0], p[1] + 0.05)
    bond(ax, C, p); atom(ax, p, 'F', ec=OUT)
atom(ax, C, 'Be', r=0.17)
ang(ax, C, 0, 180, '180°', r=0.40, tr=0.50)
frame(ax, 'BeF$_2$   sp', 'linear · 2 bp, 0 lp')

# 2 BF3 - trigonal planar
ax = A[1]; C = (0, 0.0)
for a in (90, 210, 330):
    p = pol(a, 0.74); bond(ax, C, p); atom(ax, p, 'F', ec=OUT)
atom(ax, C, 'B', r=0.17)
ang(ax, C, 90, 210, '120°', r=0.38, tr=0.50)
frame(ax, 'BF$_3$   sp$^2$', 'trigonal planar · 3 bp, 0 lp')

# 3 CH4 - tetrahedral
ax = A[2]; C = (0, 0.0)
h = {'pl1': (-0.70, -0.50), 'pl2': (0.70, -0.50), 'dsh': (-0.44, 0.66), 'wdg': (0.44, 0.66)}
bond(ax, C, h['pl1']); bond(ax, C, h['pl2'])
dash(ax, C, h['dsh']); wedge(ax, C, h['wdg'])
for k in h: atom(ax, h[k], 'H', r=0.135, ec=OUT)
atom(ax, C, 'C', r=0.17)
ang(ax, C, 215, 325, '109.5°', r=0.36, tr=0.50)
frame(ax, 'CH$_4$   sp$^3$', 'tetrahedral · 4 bp, 0 lp')

# 4 CH3Cl
ax = A[3]; C = (0, 0.0)
bond(ax, C, h['pl1']); bond(ax, C, h['pl2'])
dash(ax, C, h['dsh']); wedge(ax, C, h['wdg'], rb=0.18)
atom(ax, h['pl1'], 'H', r=0.135, ec=OUT); atom(ax, h['pl2'], 'H', r=0.135, ec=OUT)
atom(ax, h['dsh'], 'H', r=0.135, ec=OUT); atom(ax, h['wdg'], 'Cl', r=0.175, ec=OUT)
atom(ax, C, 'C', r=0.17)
frame(ax, 'CH$_3$Cl   sp$^3$', 'tetrahedral, slightly distorted')

# 5 PCl5 - trigonal bipyramidal
ax = A[4]; C = (0, 0.0)
axl = [(0, 0.80), (0, -0.80)]
eq = [(-0.80, 0.0)]
for p in axl: bond(ax, C, p); atom(ax, p, 'Cl', r=0.175, ec=OUT)
bond(ax, C, eq[0]); atom(ax, eq[0], 'Cl', r=0.175, ec=OUT)
wedge(ax, C, (0.58, -0.40), rb=0.18); atom(ax, (0.58, -0.40), 'Cl', r=0.175, ec=OUT)
dash(ax, C, (0.58, 0.40), rb=0.18); atom(ax, (0.58, 0.40), 'Cl', r=0.175, ec=OUT)
atom(ax, C, 'P', r=0.17)
ang(ax, C, 90, 180, '90°', r=0.33, tr=0.45)
frame(ax, 'PCl$_5$   sp$^3$d', 'trigonal bipyramidal · 90° and 120°')

# 6 SF6 - octahedral
ax = A[5]; C = (0, 0.0)
for p in [(0, 0.80), (0, -0.80), (-0.80, 0.0), (0.80, 0.0)]:
    bond(ax, C, p); atom(ax, p, 'F', r=0.145, ec=OUT)
wedge(ax, C, (0.46, -0.46)); atom(ax, (0.46, -0.46), 'F', r=0.145, ec=OUT)
dash(ax, C, (-0.46, 0.46)); atom(ax, (-0.46, 0.46), 'F', r=0.145, ec=OUT)
atom(ax, C, 'S', r=0.17)
ang(ax, C, 0, 90, '90°', r=0.32, tr=0.44)
frame(ax, 'SF$_6$   sp$^3$d$^2$', 'octahedral · 6 bp, 0 lp')

# 7 NH3 - pyramidal
ax = A[6]; C = (0, 0.12)
bond(ax, C, (-0.72, -0.40)); atom(ax, (-0.72, -0.40), 'H', r=0.135, ec=OUT)
wedge(ax, C, (0.70, -0.38)); atom(ax, (0.70, -0.38), 'H', r=0.135, ec=OUT)
dash(ax, C, (-0.14, -0.78)); atom(ax, (-0.14, -0.78), 'H', r=0.135, ec=OUT)
atom(ax, C, 'N', r=0.17)
lonepair(ax, C, 90, r=0.32)
ax.text(0.22, 0.56, 'lone pair', fontsize=6.4, color=LP, ha='left')
ang(ax, C, 208, 332, '107°', r=0.30, tpos=(0.46, 0.02))
frame(ax, 'NH$_3$   sp$^3$', 'pyramidal · 3 bp, 1 lp')

# 8 H2O - bent
ax = A[7]; C = (0, 0.10)
for p in [(-0.66, -0.44), (0.66, -0.44)]:
    bond(ax, C, p); atom(ax, p, 'H', r=0.135, ec=OUT)
atom(ax, C, 'O', r=0.17)
lonepair(ax, C, 55, r=0.36); lonepair(ax, C, 125, r=0.36)
ang(ax, C, 214, 326, '104.5°', r=0.34, tr=0.49)
frame(ax, 'H$_2$O   sp$^3$', 'bent (V-shaped) · 2 bp, 2 lp')

# 9 key
ax = A[8]
ax.set_xlim(-1.14, 1.14); ax.set_ylim(-1.30, 1.36); ax.set_aspect('equal'); ax.axis('off')
ax.text(0, 1.33, 'how to read the bonds', ha='center', va='top', fontsize=8.2, color=INK)
bond(ax, (-0.85, 0.55), (0.05, 0.55), ra=0.0, rb=0.0)
ax.text(0.15, 0.55, 'in the plane', fontsize=6.8, color=MUTED, va='center')
wedge(ax, (-0.85, 0.12), (0.05, 0.12), ra=0.0, rb=0.0)
ax.text(0.15, 0.12, 'towards you', fontsize=6.8, color=MUTED, va='center')
dash(ax, (-0.85, -0.31), (0.05, -0.31), ra=0.0, rb=0.0)
ax.text(0.15, -0.31, 'behind the plane', fontsize=6.8, color=MUTED, va='center')
ax.scatter([-0.62, -0.42], [-0.72, -0.72], s=15, color=LP, linewidths=0)
ax.text(0.15, -0.72, 'lone pair', fontsize=6.8, color=LP, va='center')
fig.subplots_adjust(wspace=0.02, hspace=0.14, left=0.01, right=0.99, top=0.99, bottom=0.01)
```

| Molecule | Bond pairs | Lone pairs | $X$ | Hybridisation | Arrangement of pairs | Shape | Bond angle |
|---|---|---|---|---|---|---|---|
| BeF₂ | 2 | 0 | 2 | sp | linear | linear | 180° |
| CO₂ | 2 | 0 | 2 | sp | linear | linear | 180° |
| BF₃ | 3 | 0 | 3 | sp² | trigonal planar | trigonal planar | 120° |
| CH₄ | 4 | 0 | 4 | sp³ | tetrahedral | tetrahedral | 109.5° |
| CH₃Cl | 4 | 0 | 4 | sp³ | tetrahedral | tetrahedral (distorted) | ≈110° |
| NH₃ | 3 | 1 | 4 | sp³ | tetrahedral | trigonal pyramidal | 107° |
| PH₃ | 3 | 1 | 4 | sp³ | tetrahedral | trigonal pyramidal | 93.5° |
| H₂O | 2 | 2 | 4 | sp³ | tetrahedral | bent (V-shaped) | 104.5° |
| H₂S | 2 | 2 | 4 | sp³ | tetrahedral | bent (V-shaped) | 92° |
| PCl₅ | 5 | 0 | 5 | sp³d | trigonal bipyramidal | trigonal bipyramidal | 120° and 90° |
| SF₆ | 6 | 0 | 6 | sp³d² | octahedral | octahedral | 90° |

::: example Worked example 5.2 — predicting shapes
**Problem.** Predict the shape and bond angle of (a) H₂S, (b) PH₃, (c) CO₂.

**Solution.** (a) H₂S: $V = 6$ (sulphur), $M = 2$, $c = a = 0$.

$$ X = \tfrac{1}{2}(6 + 2) = 4 $$

Four pairs → tetrahedral arrangement; two are bonding, two are lone pairs, so the
**shape is bent**. The two lone pairs push the bonds together, giving 92° —
smaller than in H₂O because sulphur is bigger and less electronegative, so its
bond pairs sit further from the central atom.

(b) PH₃: $X = \frac{1}{2}(5+3) = 4$; 3 bond pairs + 1 lone pair → **trigonal
pyramidal**, angle 93.5°.

(c) CO₂: oxygen is divalent, so $M = 0$ and $X = \frac{1}{2}(4+0) = 2$. Two
electron regions → **linear**, 180°. Note that although each C=O bond is polar,
the molecule is not.
:::

## 5.7 Elementary idea of Valence Bond Theory

Valence Bond Theory (Heitler, London and Pauling) treats a covalent bond as the
**overlap of two half-filled atomic orbitals** holding electrons of opposite spin.
As two H atoms approach, the attraction of each nucleus for the other's electron
lowers the potential energy; at 74 pm it reaches a minimum 436 kJ mol⁻¹ below the
free atoms, and any closer the nuclei repel. That minimum *is* the bond: 74 pm is
the bond length and 436 kJ mol⁻¹ the bond dissociation energy of H₂.

The greater the overlap, the stronger the bond. Two kinds occur:

| Bond | Overlap | Strength | Rotation | Example |
|---|---|---|---|---|
| **σ (sigma)** | head-on, along the internuclear axis (s–s, s–p, p–p) | strong | free | H–H, C–H |
| **π (pi)** | sideways, above and below the axis (p–p) | weaker | not free | second bond of C=C |

A double bond is therefore σ + π and a triple bond σ + 2π. Simple VBT cannot
explain why CH₄ has four *identical* bonds at 109.5°, or why O₂ is paramagnetic;
the first difficulty is removed by hybridisation.

## 5.8 Hybridization involving s and p orbitals only

::: definition Hybridisation
The intermixing of atomic orbitals of an atom that are close in energy to produce
a set of **new orbitals of equal energy and identical shape**, called hybrid
orbitals, which are oriented so as to be as far apart as possible.
:::

The number of hybrids always equals the number of orbitals mixed, and hybrids
overlap better than pure orbitals, so their bonds are stronger.

```figure caption="Hybridisation in carbon. One 2s electron is promoted to the empty 2p orbital, then the 2s and three 2p orbitals mix to give four identical sp³ hybrids — which is why all four C–H bonds in methane are the same."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, Circle

fig = plt.figure(figsize=(5.2, 4.4))
gs = fig.add_gridspec(2, 3, height_ratios=[1.02, 1.55], hspace=0.10,
                      wspace=0.04, left=0.01, right=0.99, top=0.99, bottom=0.02)
top = fig.add_subplot(gs[0, :])
BW, BH = 0.52, 0.52

def box(ax, x, y, spins, c=INK):
    ax.add_patch(Rectangle((x, y), BW, BH, facecolor='none', edgecolor=c, lw=0.9))
    for s, dx in zip(spins, (0.30, 0.70)):
        if s == 0:
            continue
        xc = x + BW * dx
        ax.annotate('', xy=(xc, y + BH * (0.86 if s > 0 else 0.14)),
                    xytext=(xc, y + BH * (0.14 if s > 0 else 0.86)),
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=0.9, mutation_scale=6))

def row(ax, x0, y, groups, lab, c=INK, above=True):
    x = x0
    for n, spins, name in groups:
        for i in range(n):
            box(ax, x, y, spins[i], c)
            x += BW + 0.07
        if name:
            cx = x - n * (BW + 0.07) + (n * (BW + 0.07) - 0.07) / 2
            if above:
                ax.text(cx, y + BH + 0.09, name, ha='center', va='bottom',
                        fontsize=7.0, color=MUTED)
            else:
                ax.text(cx, y - 0.11, name, ha='center', va='top',
                        fontsize=7.0, color=MUTED)
        x += 0.26
    ax.text(x0 - 0.16, y + BH / 2, lab, ha='right', va='center', fontsize=7.4, color=c)
    return x

UD = (1, -1); U = (1, 0); N = (0, 0)
y1 = 1.74
row(top, 1.35, y1, [(1, [UD], '2s'), (3, [U, U, N], '2p')], 'ground state  C')
y2 = 0.72
row(top, 1.35, y2, [(1, [U], ''), (3, [U, U, U], '')], 'excited state  C*')
y3 = -0.30
row(top, 1.35, y3, [(4, [U, U, U, U], 'four equivalent sp$^3$ hybrid orbitals')],
    'hybridised  C', c=ACCENT, above=False)
for ya, yb, txt in ((y1, y2, 'promotion of\none 2s electron'),
                    (y2, y3, 'hybridisation\n(mixing 2s + three 2p)')):
    top.annotate('', xy=(4.30, yb + BH + 0.03), xytext=(4.30, ya - 0.06),
                 arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0, mutation_scale=8))
    top.text(4.45, (ya + yb + BH) / 2, txt, fontsize=6.6, color=SERIES[1], va='center')
top.set_xlim(-0.65, 7.35); top.set_ylim(-0.86, 2.52)
top.set_aspect('equal'); top.axis('off')

def lobe(ax, ang, c=ACCENT, sc=1.0, alpha=0.32, ls='solid'):
    t = np.radians(ang); u = np.array([np.cos(t), np.sin(t)])
    big = Ellipse(u * 0.46 * sc, 0.86 * sc, 0.44 * sc, angle=ang,
                  facecolor=c, alpha=alpha, edgecolor=c, lw=1.0, linestyle=ls, zorder=2)
    sml = Ellipse(-u * 0.15 * sc, 0.30 * sc, 0.24 * sc, angle=ang,
                  facecolor=c, alpha=alpha * 0.6, edgecolor=c, lw=0.7, zorder=1)
    ax.add_patch(big); ax.add_patch(sml)

def shell(ax, title, sub, angs, extra=None):
    ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.30, 1.30)
    ax.set_aspect('equal'); ax.axis('off')
    for a in angs:
        lobe(ax, a)
    if extra is not None:
        lobe(ax, extra, c=SERIES[4], alpha=0.26, sc=0.62, ls='dashed')
    ax.add_patch(Circle((0, 0), 0.10, facecolor='white', edgecolor=INK, lw=0.9, zorder=4))
    ax.text(0, 1.26, title, ha='center', va='top', fontsize=8.6, color=INK)
    ax.text(0, -1.26, sub, ha='center', va='bottom', fontsize=6.8, color=MUTED)

a1 = fig.add_subplot(gs[1, 0]); a2 = fig.add_subplot(gs[1, 1]); a3 = fig.add_subplot(gs[1, 2])
shell(a1, 'sp', 'linear, 180°\n50% s, 50% p  (BeF$_2$, C$_2$H$_2$)', [0, 180])
shell(a2, 'sp$^2$', 'trigonal planar, 120°\n33% s, 67% p  (BF$_3$, C$_2$H$_4$)', [90, 210, 330])
shell(a3, 'sp$^3$', 'tetrahedral, 109.5°\n25% s, 75% p  (CH$_4$, NH$_3$, H$_2$O)\n'
      'dashed lobe points at the reader', [90, 210, 330], extra=270)
```

| Hybridisation | Orbitals mixed | Hybrids formed | Geometry | Angle | Examples |
|---|---|---|---|---|---|
| sp | one s + one p | 2 | linear | 180° | BeF₂, BeCl₂, C₂H₂, CO₂ |
| sp² | one s + two p | 3 | trigonal planar | 120° | BF₃, C₂H₄, SO₂ |
| sp³ | one s + three p | 4 | tetrahedral | 109.5° | CH₄, NH₃, H₂O, NH₄⁺ |

In NH₃ and H₂O the central atom is still sp³, but one and two of the four hybrids
respectively hold lone pairs, which is exactly why the observed angles (107° and
104.5°) fall short of 109.5°.

## 5.9 Bond characteristics: bond length, ionic character, dipole moment

**Bond length** is the equilibrium internuclear distance. It *decreases* as bond
order rises, as the atoms get smaller, and as the s character of the hybrid
increases (sp > sp² > sp³).

| Bond | C–C | C=C | C≡C | H–H | O–H | C–Cl |
|---|---|---|---|---|---|---|
| Length / pm | 154 | 134 | 120 | 74 | 96 | 177 |
| Bond energy / kJ mol⁻¹ | 348 | 614 | 839 | 436 | 463 | 328 |

**Ionic character.** No bond is purely covalent unless the two atoms are
identical. When they differ in electronegativity the shared pair is pulled to the
more electronegative atom, giving partial charges δ⁺ and δ⁻ — a **polar covalent**
bond. The bigger the ΔEN, the more ionic the bond; at ΔEN ≈ 1.7 it is half ionic.

**Dipole moment** measures that polarity:

$$ \mu = q \times d $$

where $q$ is the separated charge and $d$ the distance between the centres of
positive and negative charge. The unit is the **debye**, 1 D = 3.336 × 10⁻³⁰ C m.
Dipole moment is a **vector** drawn from δ⁺ to δ⁻, so the molecular dipole is the
vector sum of the bond dipoles.

| Molecule | μ / D | Why |
|---|---|---|
| HF, HCl, HBr, HI | 1.91, 1.03, 0.79, 0.38 | falls as ΔEN falls |
| H₂O | 1.85 | bent, so bond dipoles do not cancel |
| NH₃ | 1.47 | pyramidal; lone pair adds to the resultant |
| CO₂, BF₃, CCl₄ | 0 | symmetrical, bond dipoles cancel exactly |
| CHCl₃ | 1.04 | symmetry broken by replacing one Cl with H |

::: caution Polar bonds do not always give a polar molecule
CO₂ has two strongly polar C=O bonds yet μ = 0, because the molecule is linear
and the two equal dipoles point in opposite directions. Always check the
**shape** before deciding whether a molecule is polar.
:::

::: example Worked example 5.3 — percentage ionic character
**Problem.** The observed dipole moment of HCl is 1.03 D and the H–Cl bond length
is 1.27 Å. Calculate the percentage ionic character of the bond.

**Solution.** If the bond were 100% ionic, a full electronic charge
$e = 1.602\times10^{-19}$ C would sit at each end, separated by
$d = 1.27\times10^{-10}$ m:

$$ \mu_{ionic} = qd = (1.602\times10^{-19})(1.27\times10^{-10}) = 2.035\times10^{-29}\ \text{C m} $$

Converting to debye,

$$ \mu_{ionic} = \frac{2.035\times10^{-29}}{3.336\times10^{-30}} = 6.10\ \text{D} $$

$$ \text{% ionic character} = \frac{\mu_{obs}}{\mu_{ionic}}\times 100 = \frac{1.03}{6.10}\times 100 = 16.9\% $$

So the H–Cl bond is about 17% ionic and 83% covalent — consistent with
ΔEN = 3.0 − 2.1 = 0.9.
:::

::: example Worked example 5.4 — adding bond dipoles
**Problem.** Each O–H bond moment in water is 1.5 D and the H–O–H angle is
104.5°. Calculate the dipole moment of the molecule.

**Solution.** The two bond dipoles are equal in magnitude and inclined at
$\theta = 104.5^{\circ}$, so by the parallelogram law

$$ \mu = \sqrt{\mu_1^2 + \mu_2^2 + 2\mu_1\mu_2\cos\theta} = 2\mu_1\cos\frac{\theta}{2} $$
$$ \mu = 2(1.5)\cos 52.25^{\circ} = 3.0 \times 0.6122 = 1.84\ \text{D} $$

The measured value is 1.85 D, so the bent shape is confirmed. Had the molecule
been linear, $\theta = 180^{\circ}$ would give $\mu = 0$.
:::

## 5.10 Van der Waals' force and molecular solids

Even molecules with no net charge attract one another weakly. These **van der
Waals forces** are worth 1–40 kJ mol⁻¹ against ≈400 for a covalent bond.

| Type | Acts between | Example |
|---|---|---|
| Dipole–dipole | two polar molecules | HCl, CH₃Cl |
| Dipole–induced dipole | a polar and a non-polar molecule | HCl and Ar |
| London dispersion | any two molecules; an instantaneous dipole induces one in its neighbour | Cl₂, I₂, noble gases |

Dispersion forces grow with the number of electrons, so the halogens turn from gas
to solid down the group: F₂ boils at −188 °C, Cl₂ at −34 °C, Br₂ at 59 °C, and I₂
melts at 114 °C. **Molecular solids** (I₂, dry ice, naphthalene, ice) are held by
these forces alone, so they are soft, volatile, low-melting and non-conducting.

## 5.11 Hydrogen bonding and its application

::: definition Hydrogen bond
The weak electrostatic attraction between a hydrogen atom covalently bonded to a
**small, highly electronegative atom (F, O or N)** and a lone pair on another such
atom. Its strength is 10–40 kJ mol⁻¹, about one twentieth of a covalent bond.
:::

It is **intermolecular** when it joins separate molecules (water, HF, alcohols,
carboxylic acids) and **intramolecular** when it closes a ring inside one molecule.
The difference is measurable: o-nitrophenol, bonded to itself, melts at 45 °C,
while p-nitrophenol, which can only bond to its neighbours, melts at 114 °C.

```figure caption="Left: boiling points of the hydrides. Only NH₃, H₂O and HF sit far above the trend of their own group — that gap is the hydrogen bond. Right: each water molecule can donate two and accept two hydrogen bonds."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle

fig = plt.figure(figsize=(5.2, 2.9))
gs = fig.add_gridspec(1, 2, width_ratios=[1.30, 1.0], wspace=0.28,
                      left=0.10, right=0.99, top=0.92, bottom=0.14)
ax = fig.add_subplot(gs[0, 0])
per = [2, 3, 4, 5]
data = [('group 14', [-161.5, -111.8, -88.5, -52.0], ['CH$_4$', 'SiH$_4$', 'GeH$_4$', 'SnH$_4$'], SERIES[3]),
        ('group 15', [-33.3, -87.7, -62.5, -17.0], ['NH$_3$', 'PH$_3$', 'AsH$_3$', 'SbH$_3$'], SERIES[2]),
        ('group 16', [100.0, -60.3, -41.3, -2.0], ['H$_2$O', 'H$_2$S', 'H$_2$Se', 'H$_2$Te'], SERIES[1]),
        ('group 17', [19.5, -85.0, -66.7, -35.4], ['HF', 'HCl', 'HBr', 'HI'], SERIES[0])]
for name, bp, lab, c in data:
    ax.plot(per, bp, 'o-', color=c, ms=3.6, lw=1.3, label=name)
    ax.annotate(lab[0], (per[0], bp[0]), textcoords='offset points',
                xytext=(-3, 6), ha='right', fontsize=6.8, color=c)
ax.annotate('H-bonded', (2, 100), textcoords='offset points', xytext=(12, -4),
            fontsize=7.0, color='#A8271F')
ax.axhline(0, color=GRID, lw=0.8)
ax.set_xticks(per); ax.set_xlabel('period of the central atom')
ax.set_ylabel('boiling point / °C')
ax.set_ylim(-195, 150); ax.set_xlim(1.68, 5.18)
ax.spines[['top', 'right']].set_visible(False); ax.grid(True, alpha=.40)
ax.legend(fontsize=6.6, loc='lower right', ncol=2, columnspacing=0.8)

bx = fig.add_subplot(gs[0, 1])
bx.set_xlim(-1.45, 1.55); bx.set_ylim(-1.55, 1.45)
bx.set_aspect('equal'); bx.axis('off')
RED = '#d9534f'

def water(cen, rot, scale=1.0):
    cen = np.array(cen, float)
    a = np.radians(rot)
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    hs = []
    for th in (-52.25, 52.25):
        t = np.radians(th - 90)
        v = np.array([np.cos(t), np.sin(t)]) * 0.52 * scale
        hs.append(cen + R @ v)
    for h in hs:
        bx.plot([cen[0], h[0]], [cen[1], h[1]], color=INK, lw=1.1, zorder=3)
    bx.add_patch(Circle(cen, 0.20 * scale, facecolor='white', edgecolor=RED, lw=1.1, zorder=5))
    bx.text(cen[0], cen[1], 'O', ha='center', va='center', fontsize=8.0, color=INK, zorder=6)
    for h in hs:
        bx.add_patch(Circle(h, 0.135 * scale, facecolor='white', edgecolor=MUTED,
                            lw=1.0, zorder=5))
        bx.text(h[0], h[1], 'H', ha='center', va='center', fontsize=6.6, color=INK, zorder=6)
    return cen, hs

cA, hA = water((-0.62, 0.86), 168)
cB, hB = water((0.10, -0.18), 0)
cC, hC = water((0.98, -1.02), 12)

def hbond(a, b, ra=0.15, rb=0.21):
    a = np.array(a, float); b = np.array(b, float)
    u = b - a; L = np.hypot(*u); u = u / L
    p, q = a + u * ra, b - u * rb
    bx.plot([p[0], q[0]], [p[1], q[1]], color='#A8271F', lw=1.3, ls=(0, (2.2, 1.6)), zorder=2)

hbond(hA[1], cB)
hbond(hB[1], cC)
bx.text(-0.02, 0.48, 'hydrogen\nbond', fontsize=6.6, color='#A8271F', ha='left', va='center')
bx.text(cB[0] - 0.34, cB[1] + 0.06, 'δ−', fontsize=7.2, color=RED, ha='right')
bx.text(hB[1][0] + 0.26, hB[1][1] - 0.06, 'δ+', fontsize=7.2, color=MUTED)
bx.set_title('H-bonding in water', fontsize=8.4, pad=2)
```

Applications and consequences:

- **High boiling points**: water boils at 100 °C when H₂S, with a heavier
  molecule, boils at −60 °C.
- **Ice floats.** In ice every molecule is hydrogen-bonded tetrahedrally to four
  others, making an open cage. Ice has a density of 0.92 g cm⁻³ against 1.00 for
  water, so lakes freeze from the top and fish survive the Himalayan winter.
- **Solubility**: ethanol, sugar, glucose and ammonia dissolve freely in water
  because they can hydrogen-bond to it; hydrocarbons cannot and do not.
- **Association**: ethanoic acid exists as a dimer in benzene, so its measured
  molecular mass is 120 instead of 60.
- **Biology**: the two strands of DNA are held together by hydrogen bonds between
  base pairs, and proteins owe their α-helix to them.
- High surface tension and viscosity of water, and the stiffness of cellulose
  and nylon fibres.

## 5.12 Metallic bonding and properties of metallic solids

In a metal the valence electrons are so loosely held that they leave their parent
atoms and move freely through the whole crystal.

::: definition Metallic bond (electron-sea model)
The force of attraction between the positively charged metal ions fixed at the
lattice points and the "sea" of delocalised valence electrons moving among them.
:::

```figure caption="The electron-sea model. Because the electrons are delocalised and the bond has no direction, one layer of cations can slide over another without the metal shattering."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

rng = np.random.default_rng(7)
fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.0, 2.6))

def lattice(ax, shift_row=None, dx=0.0):
    for r in range(3):
        for c in range(4):
            x = c * 1.0 + (dx if (shift_row is not None and r >= shift_row) else 0.0)
            y = -r * 1.0
            ax.add_patch(Circle((x, y), 0.30, facecolor='#cfe0ef',
                                edgecolor=ACCENT, lw=1.0, zorder=4))
            ax.text(x, y, 'M$^{+}$', ha='center', va='center', fontsize=7.0,
                    color=INK, zorder=5)
    pts = []
    while len(pts) < 46:
        p = np.array([rng.uniform(-0.55, 3.55), rng.uniform(-2.55, 0.55)])
        row = int(round(-p[1]))
        px = p[0] - (dx if (shift_row is not None and row >= shift_row) else 0.0)
        ok = True
        for r in range(3):
            for c in range(4):
                cx = c * 1.0 + (dx if (shift_row is not None and r >= shift_row) else 0.0)
                if np.hypot(p[0] - cx, p[1] + r) < 0.40:
                    ok = False; break
            if not ok: break
        if ok: pts.append(p)
    pts = np.array(pts)
    ax.scatter(pts[:, 0], pts[:, 1], s=7, color='#A8271F', zorder=6, linewidths=0)

for a in (ax, bx):
    a.set_xlim(-0.75, 4.35); a.set_ylim(-3.05, 1.15)
    a.set_aspect('equal'); a.axis('off')

lattice(ax)
ax.text(1.5, 1.02, 'electron sea model', ha='center', va='top', fontsize=8.4, color=INK)
ax.text(1.5, -2.72, 'fixed cations held together by\na sea of mobile valence electrons',
        ha='center', va='top', fontsize=6.8, color=MUTED)
ax.text(-0.72, 0.60, 'red dots = delocalised electrons', fontsize=6.6,
        color='#A8271F', ha='left', va='center')

lattice(bx, shift_row=1, dx=0.62)
bx.annotate('', xy=(3.45, 0.62), xytext=(2.10, 0.62),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.4, mutation_scale=11))
bx.text(2.05, 0.66, 'force', fontsize=7.0, color=SERIES[2], ha='right', va='center')
bx.text(1.5, 1.02, 'why metals are malleable', ha='center', va='top', fontsize=8.4, color=INK)
bx.text(1.5, -2.72, 'layers slip, but the electron sea\nis non-directional so bonding survives',
        ha='center', va='top', fontsize=6.8, color=MUTED)
fig.subplots_adjust(wspace=0.04, left=0.01, right=0.99, top=0.99, bottom=0.01)
```

Its strength rises with the **number of valence electrons** contributed and falls
with **cation size**: Na (1 e⁻, m.p. 98 °C) < Mg (2 e⁻, 650 °C) < Al (3 e⁻, 660 °C
and far harder).

| Property of metallic solids | Explanation |
|---|---|
| Electrical conductivity | delocalised electrons drift under an applied field |
| Thermal conductivity | mobile electrons carry kinetic energy quickly |
| Metallic lustre | free electrons absorb and re-emit light of all frequencies |
| Malleability and ductility | layers slip without breaking a directional bond |
| High density, high m.p. and b.p. | close packing and strong non-directional attraction |
| Alloy formation | similar-sized cations substitute freely in the lattice |

## Chapter summary

- Atoms bond to reach a noble-gas octet (duplet for H). The octet rule fails for
  incomplete octets (BF₃), expanded octets (SF₆), odd-electron molecules (NO) and
  noble-gas compounds.
- Ionic bond = complete transfer (ΔEN > 1.7), giving a non-directional giant
  lattice: high melting point, conducts only when molten or aqueous.
- Covalent bond = shared pairs; a coordinate bond is a shared pair donated
  entirely by one atom (NH₄⁺, H₃N→BF₃).
- Lewis structures: shared pairs $S = N - A$; lone pairs $= (A-S)/2$; formal
  charge = valence − lone-pair electrons − ½(bonding electrons).
- Resonance: one hybrid structure, not a mixture; it equalises bond lengths and
  lowers the energy by the resonance energy.
- VSEPR: $X = \frac{1}{2}(V + M - c + a)$ pairs; repulsion lp–lp > lp–bp > bp–bp,
  so CH₄ 109.5° > NH₃ 107° > H₂O 104.5°.
- sp, sp² and sp³ hybrids give linear (180°), trigonal planar (120°) and
  tetrahedral (109.5°) geometries; a double bond is σ + π, a triple bond σ + 2π.
- $\mu = q \times d$ in debye; a symmetrical molecule has $\mu = 0$ even with
  polar bonds; % ionic character $= (\mu_{obs}/\mu_{ionic}) \times 100$.
- Van der Waals forces (weak, grow with size) < hydrogen bonds (10–40 kJ mol⁻¹,
  need F, O or N) < covalent/ionic/metallic bonds.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The shape of the PH₃ molecule is <span class="marks">[1]</span>
   (a) trigonal planar (b) trigonal pyramidal (c) tetrahedral (d) bent
2. Which of the following has zero dipole moment? <span class="marks">[1]</span>
   (a) H₂O (b) NH₃ (c) BF₃ (d) CHCl₃
3. The number of coordinate covalent bonds in the ammonium ion is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) 4
4. The correct order of bond angle is <span class="marks">[1]</span>
   (a) H₂O > NH₃ > CH₄ (b) CH₄ > NH₃ > H₂O (c) NH₃ > CH₄ > H₂O (d) CH₄ > H₂O > NH₃
5. Which property is **not** a consequence of hydrogen bonding? <span class="marks">[1]</span>
   (a) ice floats on water (b) HF is a liquid near room temperature
   (c) methane has a very low boiling point (d) ethanol mixes with water in all proportions

::: note Answers to Group A
**1.** (b) — $X = \frac{1}{2}(5+3) = 4$: three bond pairs and one lone pair.

**2.** (c) — BF₃ is trigonal planar and symmetrical, so the three bond dipoles cancel.

**3.** (b) — one, formed when N donates its lone pair to H⁺; all four bonds then become identical.

**4.** (b) — lone pairs repel more strongly, so each lone pair closes the angle: 109.5°, 107°, 104.5°.

**5.** (c) — CH₄ has no F, O or N, so there is no hydrogen bonding at all; its low boiling point is due to weak dispersion forces.
:::

**Group B — Short answer (5 marks each)**

1. What is a coordinate covalent bond? Explain its formation in NH₄⁺ and in the
   addition compound H₃N→BF₃. <span class="marks">[5]</span>
2. State the postulates of VSEPR theory and use them to account for the fall in
   bond angle from CH₄ (109.5°) to NH₃ (107°) to H₂O (104.5°). <span class="marks">[5]</span>
3. Define dipole moment. The observed dipole moment of HBr is 0.79 D and the
   H–Br bond length is 1.41 Å. Calculate the percentage ionic character of the
   bond. <span class="marks">[5]</span>
4. What is hydrogen bonding? Explain why water boils at 100 °C while H₂S boils at
   −60 °C, and why ice floats on water. <span class="marks">[5]</span>
5. Give any five points of difference between ionic and covalent compounds. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** All three have four electron pairs and sp³ hybridisation, so the ideal
angle is 109.5°. CH₄ has no lone pair and keeps it. NH₃ has one lone pair; since
lp–bp repulsion exceeds bp–bp repulsion, the three bonds are pushed closer to
107°. H₂O has two lone pairs, and the additional lp–lp repulsion closes the angle
further to 104.5°.

**3.** $\mu = q \times d$ is the product of the separated charge and its
separation, measured in debye. For a fully ionic H–Br bond,
$\mu_{ionic} = (1.602\times10^{-19})(1.41\times10^{-10}) = 2.259\times10^{-29}$ C m
$= 2.259\times10^{-29}/3.336\times10^{-30} = 6.77$ D. Hence

% ionic character $= (0.79/6.77)\times100 = 11.7\%$.

**4.** A hydrogen bond is the attraction between an H atom bonded to F, O or N and
a lone pair on another such atom. Water molecules are extensively hydrogen-bonded,
so a great deal of extra energy is needed to separate them; sulphur is too large
and too weakly electronegative to hydrogen-bond, so H₂S is held only by weak van
der Waals forces and boils 160 °C lower. In ice each molecule is hydrogen-bonded
to four neighbours in an open tetrahedral cage containing empty space; this makes
ice (0.92 g cm⁻³) less dense than liquid water (1.00 g cm⁻³), so it floats.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the postulates of VSEPR theory. Predict, with reasons, the shape,
   hybridisation and bond angle of BF₃, PCl₅, SF₆ and H₂O. <span class="marks">[5]</span>
   (b) Both BeF₂ and H₂O are triatomic, yet BeF₂ is linear and H₂O is bent.
   Explain. <span class="marks">[3]</span>
2. (a) What is hybridisation? Describe sp, sp² and sp³ hybridisation with one
   example of each, stating the geometry and bond angle. <span class="marks">[5]</span>
   (b) The dipole moment of H₂O is 1.85 D but that of CO₂ is zero, although both
   contain polar bonds. Explain, and calculate the resultant for water from an
   O–H bond moment of 1.5 D and a bond angle of 104.5°. <span class="marks">[3]</span>

::: note Answers to Group C
**1.(b)** In BeF₂, $X = \frac{1}{2}(2+2) = 2$: beryllium has two bond pairs and no
lone pair, so the pairs get as far apart as possible at 180° and the molecule is
linear (sp). In H₂O, $X = \frac{1}{2}(6+2) = 4$: oxygen has two bond pairs **and
two lone pairs**, arranged tetrahedrally (sp³). Only the atoms are seen, so the
shape is bent, and the lone pairs squeeze the angle to 104.5°.

**2.(b)** CO₂ is linear, so its two equal C=O bond dipoles point in exactly
opposite directions and cancel: $\mu = 0$. Water is bent, so its bond dipoles add
vectorially to a non-zero resultant:
$\mu = 2(1.5)\cos(104.5^{\circ}/2) = 3.0 \times 0.6122 = 1.84$ D, in agreement
with the measured 1.85 D.
:::

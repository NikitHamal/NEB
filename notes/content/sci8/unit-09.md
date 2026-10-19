---
subject: Science and Technology
grade: 8
title: Matter
unit: 9
hours: 0
area: Science and Technology
---

Books, desks, water and air all have **mass** and occupy space (**volume**); heat,
light and shadows do not. **Anything that has mass and volume is matter.** Matter is
made of atoms of the same or different kinds. It is classified into pure substances
(elements and compounds) and impure substances (mixtures), and it is found as solid,
liquid or gas. The CDC textbook for this unit concentrates on the **structure of the
atom**, **valency and molecular formulae**, **atomic and molecular weight**, the
**modern periodic table** and **chemical equations**; these are taught in full below,
together with the other topics of the syllabus.

::: key What this unit asks of you
Describe the proton, neutron and electron; use the $2n^2$ rule to write the electronic
configuration of the first 20 elements; find valency; write molecular formulae by the
criss-cross method; calculate atomic and molecular weights; state the modern periodic
law and the trends in groups and periods; and write and balance chemical equations.
Also: states of matter, element–compound–mixture, physical and chemical change,
solutions, separation methods, acids–bases–salts and metals–non-metals.
:::

## 9.1 States of matter and the kinetic idea of particles

Matter is made of tiny particles that are always moving. How closely they are packed
and how freely they move decides the state.

```figure caption="Particles in the three states. In a solid they are packed and only vibrate; in a liquid they slide over one another; in a gas they are far apart and move fast."
fig, ax = plt.subplots(figsize=(5.1, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.4); ax.axis("off")
rng = np.random.default_rng(7)
labels = [("Solid", "fixed shape,\nfixed volume"), ("Liquid", "no fixed shape,\nfixed volume"),
          ("Gas", "no fixed shape,\nno fixed volume")]
for k, (name, note) in enumerate(labels):
    x0 = 0.6 + k * 3.2
    ax.add_patch(plt.Rectangle((x0, 1.5), 2.6, 2.4, fill=False, ec=MUTED, lw=1.1))
    ax.text(x0 + 1.3, 4.3, name, ha="center", fontsize=8.4, color=INK)
    ax.text(x0 + 1.3, 0.75, note, ha="center", va="center", fontsize=7.4, color=INK)
    if k == 0:
        for i in range(5):
            for j in range(4):
                ax.add_patch(plt.Circle((x0 + 0.38 + i * 0.46, 1.85 + j * 0.5), 0.18, color=ACCENT))
    elif k == 1:
        for i in range(5):
            for j in range(3):
                ax.add_patch(plt.Circle((x0 + 0.38 + i * 0.46 + rng.uniform(-0.08, 0.08),
                                         1.75 + j * 0.42 + rng.uniform(-0.05, 0.05)), 0.18, color=SERIES[1]))
    else:
        for px, py in rng.uniform([x0 + 0.3, 1.8], [x0 + 2.3, 3.6], size=(6, 2)):
            ax.add_patch(plt.Circle((px, py), 0.16, color=SERIES[2]))
fig.tight_layout()
```

| Property | Solid | Liquid | Gas |
|---|---|---|---|
| arrangement of particles | close, regular | close, irregular | far apart |
| movement | vibrate in place | slide past each other | move fast in all directions |
| shape / volume | fixed / fixed | shape of container / fixed | fills container / not fixed |
| compression | almost none | very little | easily compressed |

**Changes of state:** melting (solid → liquid), freezing, evaporation and boiling
(liquid → gas), condensation (gas → liquid), and **sublimation** (solid → gas directly,
e.g. camphor, naphthalene, iodine). Heating gives particles more energy.

## 9.2 Element, compound and mixture; atom and molecule

| | Element | Compound | Mixture |
|---|---|---|---|
| made of | one kind of atom | two or more elements chemically combined in a fixed ratio | two or more substances mixed in any ratio |
| separation | cannot be split by chemical means | split only by chemical means | separated by physical means |
| properties | its own | different from its elements | each part keeps its properties |
| examples | H, O, Fe, Cu, Au | water (H₂O), salt (NaCl), CO₂ | air, soil, sea water, brass |

A **molecule** is the smallest particle of an element or compound that can exist
freely; it may have one atom (He), two (O₂) or more (H₂O).

### 9.2.1 The atom and its structure

::: definition Atom
An **atom** is the smallest particle of an element that can take part in a chemical
reaction. It is far too small to be seen. Atoms of one element are alike and are
different from atoms of other elements.
:::

An atom has a central **nucleus** containing **protons** and **neutrons**; **electrons**
revolve around the nucleus in fixed paths called **shells** (orbits or energy levels).

| Particle | Symbol | Location | Charge | Mass |
|---|---|---|---|---|
| Proton | p⁺ | nucleus | positive (+1) | 1 amu (≈ mass of an H atom) |
| Neutron | n⁰ | nucleus | none | 1 amu |
| Electron | e⁻ | shells | negative (−1) | $\frac{1}{1837}$ amu |

The **atomic number** is the number of protons (= number of electrons in a neutral
atom). An atom is **electrically neutral** because it has equal numbers of protons and
electrons, so the positive and negative charges cancel.

### 9.2.2 The 2n² rule and electronic configuration

The shells, from the nucleus outwards, are **K, L, M, N** (n = 1, 2, 3, 4). By the
**Bohr–Bury rule**, the maximum number of electrons in a shell is $2n^2$:
K = $2\times1^2=2$, L = $2\times2^2=8$, M = $2\times3^2=18$, N = $2\times4^2=32$.
(For the first 20 elements the outermost shell holds no more than 8.)

| Element (Z) | Configuration | Element (Z) | Configuration |
|---|---|---|---|
| H (1) | 1 | Na (11) | 2, 8, 1 |
| He (2) | 2 | Mg (12) | 2, 8, 2 |
| Li (3) | 2, 1 | Al (13) | 2, 8, 3 |
| Be (4) | 2, 2 | Si (14) | 2, 8, 4 |
| B (5) | 2, 3 | P (15) | 2, 8, 5 |
| C (6) | 2, 4 | S (16) | 2, 8, 6 |
| N (7) | 2, 5 | Cl (17) | 2, 8, 7 |
| O (8) | 2, 6 | Ar (18) | 2, 8, 8 |
| F (9) | 2, 7 | K (19) | 2, 8, 8, 1 |
| Ne (10) | 2, 8 | Ca (20) | 2, 8, 8, 2 |

```figure caption="Atomic structure of sodium (Z = 11): 11 protons and 12 neutrons in the nucleus, electrons arranged 2, 8, 1."
fig, ax = plt.subplots(figsize=(4.4, 3.3))
ax.set_xlim(-4.2, 6.2); ax.set_ylim(-3.8, 3.8); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(plt.Circle((0, 0), 0.75, fc="#f6d9a8", ec=INK))
ax.text(0, 0.15, "11 p", ha="center", va="center", fontsize=7.6, color=INK)
ax.text(0, -0.25, "12 n", ha="center", va="center", fontsize=7.6, color=INK)
for r, n in [(1.5, 2), (2.4, 8), (3.3, 1)]:
    ax.add_patch(plt.Circle((0, 0), r, fill=False, ec=MUTED, lw=0.9))
    for k in range(n):
        a = 2 * np.pi * k / n + 0.4
        ax.plot(r * np.cos(a), r * np.sin(a), "o", ms=6, color=ACCENT)
for r, t, y in [(1.5, "K shell: 2", 0.9), (2.4, "L shell: 8", 0.0), (3.3, "M shell (valence): 1", -0.9)]:
    ax.plot([r * 0.97, 3.7], [0.2 * y + 0.05, y], color=MUTED, lw=0.6)
    ax.text(3.75, y, t, fontsize=7.6, color=INK, va="center")
fig.tight_layout()
```

### 9.2.3 Valence shell, valence electrons and valency

The outermost shell is the **valence shell**, and its electrons are the **valence
electrons**. Atoms become stable with 2 electrons (for very small atoms) or **8** in the
valence shell. To do this:

- atoms with **1–3** valence electrons **lose** them (metals: Na, Mg, Al);
- atoms with **4** valence electrons **share** them (C, Si);
- atoms with **5–7** valence electrons **gain** electrons (N, O, Cl).

::: definition Valency
**Valency** is the number of electrons an atom loses, gains or shares to become stable
(combining capacity). It depends on the number of valence electrons.
:::

| Valence electrons | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 (or 2 for He) |
|---|---|---|---|---|---|---|---|---|
| Valency | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 0 |
| Examples | H, Li, Na, K | Be, Mg, Ca | B, Al | C, Si | N, P | O, S | F, Cl | He, Ne, Ar |

A **valency of zero** means the atom already has a stable (full) valence shell; it does not
lose, gain or share electrons, so these **inert (noble) gases** do not normally react.
Chlorine (2, 8, 7) has valency 1 because it needs to gain just **one** electron to complete
its octet.

::: example From atomic number to valency and position
**Problem.** An element has atomic number 13. Write its electronic configuration, valency, and
whether it is a metal or non-metal.
**Solution.** 13 electrons: K = 2, L = 8, M = 3 → **2, 8, 3**. It has 3 valence electrons, which
it loses, so its **valency is 3** and it is a **metal** (aluminium). It has 3 shells, so it is in
period 3; with 3 valence electrons it is in group 13.
:::

### 9.2.4 Molecular formula by the criss-cross method

A **molecular formula** shows the symbols and number of atoms in one molecule
(H₂O, CO₂). To write it we must know the **elements (symbols)** and their **valencies**.

**Steps (magnesium oxide):** (1) write the name; (2) write the symbols Mg and O;
(3) write the valencies above them, Mg 2 and O 2; (4) cross over the valencies;
(5) write them as subscripts, Mg₂O₂; (6) divide by the common factor 2 → **MgO**. A
subscript 1 is not written.

| Compound | Symbols and valencies | Formula |
|---|---|---|
| potassium chloride | K (1), Cl (1) | KCl |
| calcium chloride | Ca (2), Cl (1) | CaCl₂ |
| sodium chloride | Na (1), Cl (1) | NaCl |
| potassium oxide | K (1), O (2) | K₂O |
| aluminium chloride | Al (3), Cl (1) | AlCl₃ |
| ammonia | N (3), H (1) | NH₃ |
| water | H (1), O (2) | H₂O |
| carbon dioxide | C (4), O (2) → C₂O₄ ÷ 2 | CO₂ |
| calcium oxide | Ca (2), O (2) → Ca₂O₂ ÷ 2 | CaO |

### 9.2.5 Atomic weight and molecular weight

**Atomic weight** (mass number) = number of protons + number of neutrons. Electrons are
not counted because their mass ($\frac{1}{1837}$ amu each) is negligible.

**Molecular weight** = sum of the atomic weights of all atoms in a molecule.

Useful atomic weights: H 1, C 12, N 14, O 16, Na 23, Mg 24, Al 27, S 32, Cl 35.5, K 39,
Ar 40, Ca 40.

::: example Atomic and molecular weights
**(a)** Calcium has 20 protons and 20 neutrons. Atomic weight $=20+20=40$ amu.

**(b)** Water, H₂O: $2\times1+16=18$ amu.

**(c)** Calcium carbonate, CaCO₃: $40+12+3\times16=40+12+48=100$ amu.

**(d)** Magnesium chloride, MgCl₂: $24+2\times35.5=95$ amu. *(The textbook rounds Cl to 35
and gets 94 amu; either is accepted if the value used for Cl is shown.)*

**(e)** Calcium chloride, CaCl₂: $40+2\times35.5=111$ amu (110 amu with Cl = 35).

**(f)** Sulphuric acid, H₂SO₄, has 2 H, 1 S and 4 O atoms: $2\times1+32+4\times16=98$ amu.
:::

## 9.3 Physical and chemical change; chemical reactions and equations

| Physical change | Chemical change |
|---|---|
| no new substance forms; composition unchanged | new substance(s) with new properties form |
| usually reversible | usually not easily reversible |
| e.g. melting of ice, dissolving salt, breaking glass | e.g. burning paper, rusting of iron, cooking, digestion |

A **chemical reaction** is a chemical change in which atoms combine, separate or exchange
to form new substances. The substances that react are **reactants** (written on the
left); the new substances formed are **products** (on the right).

A **chemical equation** is the short representation of a chemical reaction using words or
symbols and formulae. A **word equation** uses names; a **formula equation** uses formulae.
An unbalanced formula equation is a **skeletal equation**. In a **balanced equation** the
number of atoms of each element is equal on both sides; we balance it by putting numbers
(coefficients) in front of formulae — never by changing the subscripts.

::: example Balancing equations
**(a)** Sodium + chlorine → sodium chloride.
Skeletal: Na + Cl₂ → NaCl (2 Cl on the left, 1 on the right).
Put 2 before NaCl: Na + Cl₂ → 2NaCl (now 2 Na on the right); put 2 before Na:
**2Na + Cl₂ → 2NaCl**.

**(b)** Nitrogen + hydrogen → ammonia: **N₂ + 3H₂ → 2NH₃** (2 N and 6 H on each side).

**(c)** Calcium carbonate → calcium oxide + carbon dioxide: **CaCO₃ → CaO + CO₂** (already balanced).

**(d)** Zinc + hydrochloric acid → zinc chloride + hydrogen: **Zn + 2HCl → ZnCl₂ + H₂**.
With sulphuric acid instead: **Zn + H₂SO₄ → ZnSO₄ + H₂**.
:::

## 9.4 Solution, solute and solvent; saturated and unsaturated solution

A **solution** is a uniform mixture of a **solute** (the substance that dissolves, e.g.
salt) in a **solvent** (the substance in which it dissolves, e.g. water). Water dissolves
so many substances that it is called the universal solvent. A solution that can dissolve
more solute at that temperature is **unsaturated**; one that cannot dissolve any more is
**saturated**. Heating usually lets more solid dissolve, and stirring and powdering make it
dissolve faster. On cooling a hot saturated solution, the extra solute separates as crystals.

## 9.5 Separation of mixtures

| Method | Used to separate | Example |
|---|---|---|
| Filtration | an insoluble solid from a liquid | sand from water, tea leaves from tea |
| Evaporation | a dissolved solid from its solvent | salt from salt water |
| Distillation | a pure liquid from a solution (boil, then condense the vapour) | pure water from salt water |
| Sublimation | a solid that sublimes from one that does not | camphor or naphthalene from sand or salt |
| Chromatography | different dissolved colours that move at different speeds on paper | dyes in ink |
| Magnetic separation | iron from non-magnetic material | iron filings from sulphur |
| Sedimentation and decantation | heavy solid from liquid | muddy water left to settle |

## 9.6 Acids, bases and salts; indicators and pH

**Acids** taste sour, turn **blue litmus red**, and give hydrogen ions in water (lemon juice,
vinegar, HCl, H₂SO₄). **Bases** taste bitter and feel soapy; soluble bases are **alkalis**
and turn **red litmus blue** (soap, lime water, NaOH). An acid and a base **neutralise**
each other to form a **salt** and water: HCl + NaOH → NaCl + H₂O.

| Indicator | In acid | In base |
|---|---|---|
| blue litmus | red | blue |
| red litmus | red | blue |
| methyl orange | red | yellow |
| phenolphthalein | colourless | pink |
| turmeric | yellow | reddish-brown |

The **pH scale** runs from **0 to 14**: below 7 acidic, 7 neutral (pure water), above 7 basic.

```figure caption="The pH scale with some common substances (approximate values)."
fig, ax = plt.subplots(figsize=(5.1, 2.3))
ax.set_xlim(-0.2, 14.4); ax.set_ylim(0, 3.6); ax.axis("off")
for i in range(15):
    ax.add_patch(plt.Rectangle((i * 0.95, 1.6), 0.95, 0.75, color=plt.cm.RdYlBu(i / 14.0), ec="white", lw=0.6))
    ax.text(i * 0.95 + 0.475, 1.975, str(i), ha="center", va="center", fontsize=7.4, color=INK)
ax.text(2.0, 2.85, "acidic", ha="center", fontsize=8.2, color=SERIES[1])
ax.text(7.1, 2.85, "neutral", ha="center", fontsize=8.2, color=INK)
ax.text(12.3, 2.85, "basic", ha="center", fontsize=8.2, color=ACCENT)
for v, t in [(2, "lemon 2"), (4.5, "curd 4.5"), (7, "water 7"), (9.5, "soap 9-10"), (12.5, "lime 12")]:
    ax.text(v * 0.95 + 0.475, 1.15, t, ha="center", fontsize=7.2, color=INK)
fig.tight_layout()
```

```photo id="sci10/litmus" caption="Litmus paper. Blue litmus turns red in an acid; red litmus turns blue in a base." width="56"
```

## 9.7 Metals and non-metals; alloys

| Property | Metals | Non-metals |
|---|---|---|
| electrons in reactions | **donate** (lose) electrons; 1–3 valence electrons | **gain** electrons; 5–7 valence electrons |
| lustre | shiny | dull (except iodine, graphite) |
| conduction | good conductors of heat and electricity | poor (except graphite) |
| malleable / ductile | yes | brittle |
| state at room temperature | solid, except **mercury** (liquid) | solid, liquid (bromine) or gas |
| examples | Na, Mg, Al, Fe, Cu, Zn | C, N, O, S, Cl |

An **alloy** is a mixture of a metal with other metals or non-metals, made to improve its
properties: **brass** (copper + zinc), **bronze** (copper + tin), **steel** (iron + a little
carbon), **stainless steel** (iron + chromium + nickel), **solder** (lead + tin).

```photo id="sci10/malachite" caption="Malachite, an ore of copper. Metals are extracted from such naturally occurring minerals." width="54"
```

## 9.8 Classification of elements: the modern periodic table

As more elements were discovered, it became hard to study them one by one, so they were
arranged in a table of rows and columns — the **periodic table**. The **modern periodic
table** is based on the work of **Henry Moseley (1913)**, who showed that the properties
of elements depend on their **atomic number**.

::: definition Modern periodic law
The physical and chemical properties of elements are a periodic function of their
**atomic numbers**.
:::

The modern periodic table has **18 groups** (vertical columns) and **7 periods** (horizontal
rows). Elements in a group have similar properties.

| Position | Elements | Features |
|---|---|---|
| Group 1 (except H) | Li, Na, K — **alkali metals** | 1 valence electron, valency 1, very reactive metals |
| Group 2 | Be, Mg, Ca — **alkaline earth metals** | 2 valence electrons, valency 2 |
| Groups 3–12 | Fe, Cu, Zn … — transition metals | metals |
| Groups 13–16 | B, Al, C, N, O, S … | Al is a metal; groups 15–16 are mostly non-metals |
| Group 17 | F, Cl, Br, I — **halogens** | 7 valence electrons, valency 1, very reactive non-metals |
| Group 18 | He, Ne, Ar — **inert (noble) gases** | full valence shell, valency 0, unreactive |

**Hydrogen** has one valence electron, so it is placed in group 1, but it is a non-metal.
Metals lie on the left and middle; non-metals on the right.

| Trends in a group (top → bottom) | Trends in a period (left → right) |
|---|---|
| number of shells increases by one each step | number of shells stays the same |
| valence electrons — and valency — stay the same | valence electrons increase from 1 to 8; valency changes |
| atomic size increases | atomic size decreases (except the noble gas) |
| metallic character (electron-losing) increases; non-metallic character decreases | metallic character decreases; non-metallic character increases |
| similar chemical properties | properties change gradually |

::: tip Sodium and chlorine both have valency 1 — why?
Sodium (2, 8, 1) loses **one** electron; chlorine (2, 8, 7) gains **one** electron. Both
change by one electron to reach an octet, so both have valency 1, although Na is in group 1
and Cl in group 17.
:::

## Chapter summary

- Matter has mass and volume; it exists as solid, liquid and gas.
- Atom: nucleus (protons +1, 1 amu; neutrons 0, 1 amu) and electrons (−1, 1/1837 amu)
  in shells K, L, M, N with at most $2n^2$ electrons.
- Valency = electrons lost, gained or shared to become stable; noble gases have valency 0.
- Criss-cross method gives formulae (MgO, CaCl₂, AlCl₃, NH₃, K₂O).
- Atomic weight = protons + neutrons; molecular weight = sum of atomic weights.
- Chemical equation: reactants → products; balance by coefficients (2Na + Cl₂ → 2NaCl).
- Modern periodic law (Moseley): properties depend on atomic number; 18 groups, 7 periods.
  Down a group size and metallic character increase; across a period they decrease.
- pH < 7 acid, 7 neutral, > 7 base; acid + base → salt + water.

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Textbook exercises.)*

1. Which element has zero valency? <span class="marks">[1]</span>
   (a) hydrogen (b) sodium (c) neon (d) calcium
2. The atomic weight of argon is <span class="marks">[1]</span>
   (a) 40 amu (b) 42 amu (c) 44 amu (d) 46 amu
3. The mass of an electron is <span class="marks">[1]</span>
   (a) 1/1834 amu (b) 1/1835 amu (c) 1/1836 amu (d) 1/1837 amu
4. The particles in the nucleus are <span class="marks">[1]</span>
   (a) proton and electron (b) electron and neutron (c) neutron and proton (d) all three
5. The formula of calcium oxide is <span class="marks">[1]</span>
   (a) CaO (b) CaO₂ (c) Ca₂O (d) CaCO₃
6. Of potassium (19 p, 20 n), carbon (6 p, 6 n), oxygen (8 p, 8 n) and argon (18 p, 22 n), which has the highest atomic weight? <span class="marks">[1]</span>
   (a) potassium (b) carbon (c) oxygen (d) argon
7. The modern periodic table was given by <span class="marks">[1]</span>
   (a) Mendeleev (b) Moseley (c) Dalton (d) Bohr
8. Elements in the modern periodic table are arranged by <span class="marks">[1]</span>
   (a) atomic weight (b) atomic mass (c) molecular mass (d) atomic number
9. Which statement about a group is true? <span class="marks">[1]</span>
   (a) its elements have different properties (b) atomic size decreases downwards (c) its elements have the same valency (d) non-metallic character increases downwards
10. Which metal is liquid at room temperature? <span class="marks">[1]</span>
   (a) sodium (b) magnesium (c) aluminium (d) mercury
11. Which element is in group 18? <span class="marks">[1]</span>
   (a) sodium (b) magnesium (c) phosphorus (d) argon
12. A similarity between argon and chlorine is that both <span class="marks">[1]</span>
   (a) are inert gases (b) are in the same period (c) are equally reactive (d) are in the same group

::: note Answers to Group A
**1.** (c) — its valence shell is full (2, 8). **2.** (a) — 18 + 22. **3.** (d). **4.** (c). **5.** (a) — Ca₂O₂ ÷ 2. **6.** (d) — Ar 40, K 39, O 16, C 12. **7.** (b). **8.** (d). **9.** (c). **10.** (d). **11.** (d). **12.** (b) — both have three shells (period 3).
:::

**Group B — Short answer (2 marks each)**

1. Differentiate: (a) proton and electron (b) K shell and M shell (c) valence shell and valence electron (d) atomic weight and molecular weight. <span class="marks">[4]</span>
2. Give reasons: (a) An atom is electrically neutral. (b) The valency of chlorine is 1. (c) Electrons are not counted in atomic weight. <span class="marks">[3]</span>
3. Write the formulae by the criss-cross method: magnesium oxide, sodium chloride, potassium oxide, aluminium chloride, ammonia. <span class="marks">[3]</span>
4. What is the $2n^2$ rule used for? Find the maximum electrons in the L and M shells. <span class="marks">[2]</span>
5. What will be the valency of an element with configuration 2, 8, 8, 1? Why? <span class="marks">[2]</span>
6. Complete for O, C, Cl, K, Ar: symbol, atomic number, atomic mass, protons, neutrons, electrons. <span class="marks">[3]</span>
7. A nucleus has 19 protons and 20 neutrons. Name the element, find its atomic weight and draw its electron arrangement. <span class="marks">[2]</span>
8. Can an atom exist without electrons? Give reasons. <span class="marks">[2]</span>
9. Differentiate: (a) group and period (b) metals and non-metals (c) group 1 and group 17 elements (d) word equation and formula equation (e) reactants and products. <span class="marks">[5]</span>
10. Give reasons: (a) Classification of elements is necessary. (b) Products are different from reactants. (c) Metals and non-metals are kept separately in the periodic table. <span class="marks">[3]</span>

::: note Answers to Group B
**1.** (a) A proton is positive, 1 amu, in the nucleus; an electron is negative, 1/1837 amu, in the shells. (b) K is the first shell (n = 1) holding at most 2 electrons; M is the third shell (n = 3) holding at most 18. (c) The valence shell is the outermost shell; valence electrons are the electrons in it. (d) Atomic weight is the protons + neutrons of one atom (Na = 23); molecular weight is the sum of atomic weights in one molecule (H₂O = 18).
**2.** (a) It has equal numbers of protons (+) and electrons (−), so the charges cancel. (b) Chlorine is 2, 8, 7; it gains one electron to complete its octet. (c) The mass of an electron is only 1/1837 of a proton, which is negligible.
**3.** MgO, NaCl, K₂O, AlCl₃, NH₃.
**4.** It gives the maximum number of electrons in a shell. L: $2\times2^2=8$; M: $2\times3^2=18$.
**5.** 1. It has one valence electron, which it loses to get a stable octet (it is potassium).
**6.** O: O, 8, 16, 8, 8, 8. C: C, 6, 12, 6, 6, 6. Cl: Cl, 17, 35 (35.5), 17, 18, 17. K: K, 19, 39, 19, 20, 19. Ar: Ar, 18, 40, 18, 22, 18.
**7.** Potassium (Z = 19). Atomic weight $=19+20=39$ amu. Electrons 2, 8, 8, 1 (K, L, M, N shells).
**8.** A neutral atom must have electrons equal to its protons. If all electrons are removed, only a positively charged nucleus (an ion) is left — it is no longer a neutral atom (e.g. H⁺ is just a proton).
**9.** (a) A group is a vertical column of elements with the same valence electrons and similar properties; a period is a horizontal row with the same number of shells. (b) See the table in 9.7. (c) Group 1: alkali metals, 1 valence electron, lose it; group 17: halogens, 7 valence electrons, gain one; both have valency 1. (d) A word equation uses names; a formula equation uses symbols and formulae. (e) Reactants take part in a reaction (left side); products are formed by it (right side).
**10.** (a) More than a hundred elements exist; grouping elements with similar properties makes them easy to study and remember. (b) In a chemical reaction atoms rearrange to form new substances with new properties. (c) Metals lose electrons and non-metals gain them; their properties are opposite, so they fall in different groups.
:::

**Group C — Long answer (4 marks each)**

1. Calculate the molecular weights of CaCl₂, MgCl₂ and CaCO₃ (Ca = 40, Mg = 24, C = 12, O = 16, Cl = 35.5). <span class="marks">[3]</span>
2. Write balanced equations: (i) magnesium oxide + hydrogen → magnesium + water (ii) calcium carbonate + hydrochloric acid → calcium chloride + water + carbon dioxide (iii) potassium + chlorine → potassium chloride (iv) sodium + oxygen → sodium oxide (v) hydrogen + oxygen → water. <span class="marks">[5]</span>
3. Explain how metallic character changes down a group and across a period of the modern periodic table. <span class="marks">[4]</span>
4. Be, Mg and Ca form a group. Write four characteristics of this group. <span class="marks">[4]</span>
5. Write the electronic configuration and valency of the elements from hydrogen to calcium. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** CaCl₂ $=40+2\times35.5=111$ amu; MgCl₂ $=24+2\times35.5=95$ amu; CaCO₃ $=40+12+3\times16=100$ amu.
**2.** (i) MgO + H₂ → Mg + H₂O (already balanced). (ii) CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂. (iii) 2K + Cl₂ → 2KCl. (iv) 4Na + O₂ → 2Na₂O. (v) 2H₂ + O₂ → 2H₂O.
**3.** Down a group a new shell is added at each step, so the atom gets bigger and the valence electrons are farther from the nucleus and held less tightly; they are lost more easily, so metallic character increases. Across a period the number of shells is the same but protons and valence electrons increase, so electrons are held more tightly and the atom becomes smaller; losing electrons gets harder and gaining easier, so metallic character decreases and non-metallic character increases.
**4.** Group 2 (alkaline earth metals): (i) each has 2 valence electrons (Be 2,2; Mg 2,8,2; Ca 2,8,8,2) and valency 2; (ii) all are metals that lose 2 electrons; (iii) atomic size increases from Be to Ca as shells increase; (iv) metallic character and reactivity increase downwards; their chemical properties are similar.
**5.** See the table in 9.2.2 and the valency table in 9.2.3: H 1 (1); He 2 (0); Li 2,1 (1); Be 2,2 (2); B 2,3 (3); C 2,4 (4); N 2,5 (3); O 2,6 (2); F 2,7 (1); Ne 2,8 (0); Na 2,8,1 (1); Mg 2,8,2 (2); Al 2,8,3 (3); Si 2,8,4 (4); P 2,8,5 (3); S 2,8,6 (2); Cl 2,8,7 (1); Ar 2,8,8 (0); K 2,8,8,1 (1); Ca 2,8,8,2 (2).
:::

---
subject: Chemistry
grade: CEE
unit: 5
title: Redox Reactions
hours: 1
area: Physical Chemistry
---

Redox reactions carry about **one question** in the paper (our estimate from the MEC topic
list), but oxidation numbers and balanced redox equations are used again in
electrochemistry, volumetric analysis (permanganate and dichromate titrations), metallurgy
and the chemistry of non-metals. The question is usually an oxidation number (often a
tricky one such as Fe₃O₄, CrO₅ or S₄O₆²⁻), identifying the oxidant, reductant or a
disproportionation, or a coefficient or mole ratio from a balanced redox equation.

::: key What the paper asks from this chapter
- Oxidation = loss of electrons (increase in oxidation number); reduction = gain of electrons (decrease). The oxidising agent is reduced; the reducing agent is oxidised.
- The oxidation-number rules, and the exceptions: O is −1 in peroxides, −½ in superoxides, +2 in OF₂; H is −1 in metal hydrides; F is always −1.
- Fractional and "impossible" values: Fe₃O₄ +8/3, S₄O₆²⁻ +2.5; peroxide bridges keep CrO₅ and H₂S₂O₈ at +6.
- Disproportionation (one element both oxidised and reduced) and its reverse, comproportionation.
- Balancing by oxidation number and by ion-electron (half-reaction) methods, in acid and in base.
- n-factor: moles react in the inverse ratio of their electron changes (KMnO₄ 5 in acid, K₂Cr₂O₇ 6).
:::

## 5.1 Classical and electronic concepts of oxidation and reduction; oxidation number

### The classical concept

| Oxidation is | Reduction is | Example |
|---|---|---|
| addition of oxygen | removal of oxygen | 2Mg + O₂ → 2MgO (Mg oxidised); CuO + H₂ → Cu + H₂O (CuO reduced) |
| removal of hydrogen | addition of hydrogen | H₂S + Cl₂ → 2HCl + S (H₂S oxidised, Cl₂ reduced) |
| addition of an electronegative element | removal of an electronegative element | 2FeCl₂ + Cl₂ → 2FeCl₃ (FeCl₂ oxidised) |
| removal of an electropositive element | addition of an electropositive element | 2KI + H₂O₂ → 2KOH + I₂ (KI oxidised: K removed from I) |

The classical definitions cannot handle reactions with no oxygen or hydrogen at all, such as
Zn + Cu²⁺ → Zn²⁺ + Cu. The electronic concept covers everything.

### The electronic concept

::: definition Oxidation and reduction (electronic)
**Oxidation** is the **loss of electrons** by an atom, ion or molecule (de-electronation);
**reduction** is the **gain of electrons** (electronation). An **oxidising agent
(oxidant)** accepts electrons and is itself reduced; a **reducing agent (reductant)**
donates electrons and is itself oxidised. The two always happen together — a **redox**
reaction.
:::

In Zn + Cu²⁺ → Zn²⁺ + Cu, the half-reactions are Zn → Zn²⁺ + 2e⁻ (oxidation) and
Cu²⁺ + 2e⁻ → Cu (reduction). Zinc is the reducing agent; Cu²⁺ is the oxidising agent.

::: memory OIL RIG
**O**xidation **I**s **L**oss, **R**eduction **I**s **G**ain (of electrons). And the
agent is the opposite of what happens to it: the oxidising agent gets reduced.
:::

### Oxidation number

::: definition Oxidation number
The **oxidation number** (oxidation state) of an atom is the charge it would carry if every
bond in the compound were ionic, the shared electrons being given to the more
electronegative atom. It can be positive, negative, zero or fractional (an average).
:::

| Rule | Exceptions to remember |
|---|---|
| An element in the free state: 0 (Na, H₂, O₃, P₄, S₈) | — |
| A monatomic ion: its charge (Na⁺ +1, Cl⁻ −1, Al³⁺ +3) | — |
| Fluorine: always −1 | none — it is the most electronegative element |
| Oxygen: −2 | peroxides (H₂O₂, Na₂O₂, BaO₂) −1; superoxides (KO₂) −½; OF₂ +2; O₂F₂ +1 |
| Hydrogen: +1 | metal hydrides (NaH, CaH₂, LiAlH₄) −1 |
| Group 1 metals +1, group 2 metals +2 in compounds | — |
| Sum of all oxidation numbers = 0 for a molecule, = the charge for an ion | — |

In terms of oxidation numbers, **oxidation is an increase and reduction a decrease**. A
reaction in which no oxidation number changes (neutralisation, precipitation, most
double decompositions) is not a redox reaction.

| Element | Oxidation numbers worth knowing |
|---|---|
| Mn | KMnO₄ +7, K₂MnO₄ +6, MnO₂ +4, Mn²⁺ +2 |
| Cr | K₂Cr₂O₇ and K₂CrO₄ +6, Cr³⁺ +3, CrO₅ +6 (two peroxide groups) |
| S | H₂S −2, S 0, S₂O₃²⁻ +2 (average), S₄O₆²⁻ +2.5 (average), SO₂ +4, H₂SO₄ +6, H₂S₂O₈ +6 |
| N | NH₃ −3, N₂H₄ −2, NH₂OH −1, N₂ 0, N₂O +1, NO +2, HNO₂ +3, NO₂ +4, HNO₃ +5, HN₃ −⅓ |
| C | CH₄ −4, CH₃OH −2, HCHO 0, HCOOH +2, CO +2, CO₂ +4 |
| P | H₃PO₂ +1, H₃PO₃ +3, H₃PO₄ +5 |
| Cl | HCl −1, HOCl +1, HClO₂ +3, HClO₃ +5, HClO₄ +7 |
| Fe | Fe₃O₄ +8/3 (average; really one Fe²⁺ and two Fe³⁺), [Fe(CN)₆]⁴⁻ +2, [Fe(CN)₆]³⁻ +3 |
| Others | OsO₄ +8 (the highest in any stable compound), Ni(CO)₄ 0, NH₄NO₃: N −3 and +5 |

::: caution When the simple sum gives an impossible answer
A sum that exceeds the group number (Cr > +6, S > +6) means the formula hides a
**peroxide** (–O–O–) link, whose oxygens are −1. CrO₅ by simple arithmetic gives +10, but
its structure has two peroxide groups and one ordinary oxygen: x + 4(−1) + (−2) = 0, so
x = **+6**. Fractional values (Fe₃O₄, S₄O₆²⁻, HN₃) are averages over atoms in different
environments.
:::

::: example Oxidation numbers by the rules
**Problem.** Find the oxidation number of (i) S in H₂S₂O₈ (one peroxide link), (ii) N in
NH₂OH, (iii) C in C₃O₂.

**Solution.** (i) 2(+1) + 2x + 6(−2) + 2(−1) = 0 → 2x = 12 → **+6** (not +7, which the
naive sum gives). (ii) x + 2(+1) + (−2) + (+1) = 0 → **−1**. (iii) 3x + 2(−2) = 0 →
**+4/3** (an average).
:::

### Types of redox reaction

| Type | What happens | Examples |
|---|---|---|
| Combination | elements or compounds join | C + O₂ → CO₂; 2Na + Cl₂ → 2NaCl |
| Decomposition | a compound breaks up | 2KClO₃ → 2KCl + 3O₂; 2H₂O → 2H₂ + O₂ |
| Displacement | a more reactive element displaces a less reactive one | Zn + CuSO₄ → ZnSO₄ + Cu; Cl₂ + 2KBr → 2KCl + Br₂ |
| **Disproportionation** | the **same element** is both oxidised and reduced | 2H₂O₂ → 2H₂O + O₂; Cl₂ + 2NaOH (cold, dilute) → NaCl + NaClO + H₂O; 3Cl₂ + 6NaOH (hot) → 5NaCl + NaClO₃ + 3H₂O; 2Cu⁺ → Cu + Cu²⁺; 3HNO₂ → HNO₃ + 2NO + H₂O |
| Comproportionation | two oxidation states of one element meet in the middle | 2H₂S + SO₂ → 3S + 2H₂O |

**Who can do what?** An element in its **highest** oxidation state can only gain electrons —
it can act **only as an oxidising agent** (KMnO₄, K₂Cr₂O₇, HNO₃). In its **lowest** state it
can act **only as a reducing agent** (H₂S, NH₃, I⁻). In an **intermediate** state it can act
**as both** (H₂O₂, SO₂, HNO₂, NO₂⁻) — which is also why such species can disproportionate.

```figure caption="Oxidation-number ladders for four elements that the paper loves. Moving up a ladder is oxidation (loss of electrons), moving down is reduction. A species at the top of its ladder can only oxidise; one at the bottom can only reduce; those in between can do both."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2, 3.6))
cols = [('N', 0.0), ('S', 1.45), ('Cl', 2.9), ('Mn', 4.35)]
species = {
 'N': [(-3, 'NH₃, NH₄⁺'), (-2, 'N₂H₄'), (-1, 'NH₂OH'), (0, 'N₂'), (1, 'N₂O'), (2, 'NO'),
       (3, 'HNO₂, NO₂⁻'), (4, 'NO₂'), (5, 'HNO₃, NO₃⁻')],
 'S': [(-2, 'H₂S, S²⁻'), (0, 'S'), (2, 'S₂O₃²⁻ (avg.)'), (4, 'SO₂, SO₃²⁻'), (6, 'H₂SO₄, SO₄²⁻')],
 'Cl': [(-1, 'HCl, Cl⁻'), (0, 'Cl₂'), (1, 'HOCl, OCl⁻'), (3, 'HClO₂'), (5, 'HClO₃, ClO₃⁻'), (7, 'HClO₄')],
 'Mn': [(0, 'Mn'), (2, 'Mn²⁺'), (4, 'MnO₂'), (6, 'MnO₄²⁻'), (7, 'MnO₄⁻')]}
for y in range(-3, 8):
    ax.axhline(y, color=GRID, lw=0.6, zorder=0)
    ax.text(-0.35, y, ('+%d' % y) if y > 0 else str(y).replace('-', '−'), ha='right', va='center',
            fontsize=7.8, color=MUTED)
ax.text(-1.05, 2.0, 'oxidation number', rotation=90, ha='center', va='center', fontsize=8, color=MUTED)
for el, x in cols:
    ys = [s[0] for s in species[el]]
    ax.plot([x, x], [min(ys), max(ys)], color=ACCENT, lw=1.6, zorder=2)
    for y, lab in species[el]:
        ax.plot([x], [y], 'o', color=ACCENT, ms=3.6, zorder=3)
        ax.text(x+0.1, y, lab, va='center', ha='left', fontsize=7.8, color=INK, zorder=4,
                bbox=dict(fc='white', ec='none', pad=0.6))
    ax.text(x, max(ys)+0.75, el, fontsize=10, ha='center', va='center', color=INK)
ax.annotate('', xy=(6.05, 6.6), xytext=(6.05, 2.4),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5, mutation_scale=11))
ax.text(6.25, 4.5, 'oxidation\n(loss of e⁻)', rotation=90, ha='center', va='center', fontsize=7.8, color=SERIES[1])
ax.annotate('', xy=(6.05, -2.6), xytext=(6.05, 1.6),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.5, mutation_scale=11))
ax.text(6.25, -0.5, 'reduction\n(gain of e⁻)', rotation=90, ha='center', va='center', fontsize=7.8, color=SERIES[0])
ax.set_xlim(-1.3, 6.6); ax.set_ylim(-3.6, 8.2)
ax.axis('off')
```

## 5.2 Balancing redox equations by the oxidation-number and ion-electron methods; applications

### The oxidation-number method

1. Write the skeleton equation and the oxidation numbers of every atom; pick out the atoms
   whose oxidation numbers change.
2. Find the increase per formula unit of the reductant and the decrease per formula unit of
   the oxidant (multiply by the number of such atoms in the formula).
3. Multiply so that the **total increase equals the total decrease**.
4. Balance the other atoms by inspection — the spectator ions first, then H with H₂O (or
   H⁺/OH⁻ in ionic equations), and check O last.

::: example Oxidation-number method: KMnO₄ with HCl
**Problem.** Balance KMnO₄ + HCl → KCl + MnCl₂ + Cl₂ + H₂O.

**Solution.** Mn: +7 → +2, a decrease of **5** per Mn. Cl: −1 → 0, an increase of 1 per Cl,
so **2** per Cl₂ formed. Equalise: 2 Mn (decrease 10) and 5 Cl₂ (increase 10):
2KMnO₄ + ? HCl → 2KCl + 2MnCl₂ + 5Cl₂ + ? H₂O. Chlorine on the right = 2 + 4 + 10 = 16, so
16 HCl; hydrogen 16 → 8 H₂O; oxygen 8 = 8. ✓
**2KMnO₄ + 16HCl → 2KCl + 2MnCl₂ + 5Cl₂ + 8H₂O.**
:::

### The ion-electron (half-reaction) method

1. Split the ionic equation into an oxidation and a reduction half.
2. In each half balance the atoms other than O and H.
3. **Acidic medium:** balance O by adding H₂O to the side short of O, then balance H by
   adding H⁺ to the other side. **Basic medium:** balance as if acidic, then add as many
   OH⁻ to *both* sides as there are H⁺; combine H⁺ + OH⁻ into H₂O and cancel water.
4. Balance charge by adding electrons.
5. Multiply the halves so that electrons lost = electrons gained; add and cancel.

::: example Ion-electron method in acid: dichromate and hydrogen sulphide
**Problem.** Balance Cr₂O₇²⁻ + H₂S → Cr³⁺ + S in acidic solution.

**Solution.** Reduction: Cr₂O₇²⁻ → 2Cr³⁺; add 7H₂O on the right and 14H⁺ on the left;
charge: left +12, right +6, so add 6e⁻ on the left:
Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O.
Oxidation: H₂S → S + 2H⁺ + 2e⁻. Multiply it by 3 and add, cancelling 6H⁺:
**Cr₂O₇²⁻ + 3H₂S + 8H⁺ → 2Cr³⁺ + 3S + 7H₂O.** Check charge: −2 + 8 = +6 = 2(+3). ✓
:::

::: example Ion-electron method in base: chromium(III) hydroxide and hypochlorite
**Problem.** Balance Cr(OH)₃ + ClO⁻ → CrO₄²⁻ + Cl⁻ in basic solution.

**Solution.** Oxidation (as if acidic): Cr(OH)₃ + H₂O → CrO₄²⁻ + 5H⁺ + 3e⁻.
Reduction: ClO⁻ + 2H⁺ + 2e⁻ → Cl⁻ + H₂O. Multiply by 2 and 3 to equalise six electrons and
add: 2Cr(OH)₃ + 3ClO⁻ → 2CrO₄²⁻ + 3Cl⁻ + 4H⁺ + H₂O. Add 4OH⁻ to both sides
(4H⁺ + 4OH⁻ = 4H₂O):
**2Cr(OH)₃ + 3ClO⁻ + 4OH⁻ → 2CrO₄²⁻ + 3Cl⁻ + 5H₂O.** Charge: −7 = −7. ✓
:::

### The n-factor shortcut

The **n-factor** of an oxidant or reductant is the number of electrons it gains or loses per
formula unit. In any redox reaction the moles that react are in the **inverse ratio of the
n-factors** — the same idea gives equivalent weights in Unit 8.

| Reagent and change | n-factor |
|---|---|
| MnO₄⁻ → Mn²⁺ (acidic) | 5 |
| MnO₄⁻ → MnO₂ (neutral or weakly basic) | 3 |
| MnO₄⁻ → MnO₄²⁻ (strongly basic) | 1 |
| Cr₂O₇²⁻ → 2Cr³⁺ (acidic) | 6 |
| Fe²⁺ → Fe³⁺ | 1 |
| C₂O₄²⁻ → 2CO₂ | 2 |
| FeC₂O₄ → Fe³⁺ + 2CO₂ | 1 + 2 = 3 |
| H₂O₂ → O₂ (as reductant) or → H₂O (as oxidant) | 2 |
| 2S₂O₃²⁻ → S₄O₆²⁻ | 1 per S₂O₃²⁻ |
| I₂ → 2I⁻ | 2 |

So one MnO₄⁻ (n = 5) oxidises five Fe²⁺ (n = 1) in acid, and one Cr₂O₇²⁻ (n = 6) oxidises
six: MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O and
Cr₂O₇²⁻ + 6Fe²⁺ + 14H⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O. In acidified permanganate–oxalate,
2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O, ten electrons change hands.

::: tip Check a coefficient question without balancing
For "what is x?" questions, first equalise the electrons (n-factors), which fixes the
coefficients of the oxidant and reductant at once; then count O to fix H₂O, and H (or the
charge) to fix H⁺. The charge check — left side total equals right side total — catches
most slips.
:::

### Applications of redox reactions

| Field | Redox at work |
|---|---|
| Metallurgy | ores are reduced to metals: Fe₂O₃ + 3CO → 2Fe + 3CO₂ (blast furnace); Cr₂O₃ + 2Al → 2Cr + Al₂O₃ (aluminothermy) |
| Electrochemistry | cells and batteries: oxidation at the anode, reduction at the cathode (Unit 10) |
| Titrations | permanganometry, dichrometry, iodometry and iodimetry (Units 8 and 22) |
| Bleaching | Cl₂ bleaches by oxidation (HOCl releases [O]) — permanent; SO₂ bleaches by reduction (nascent hydrogen) — temporary |
| Corrosion | rusting is the oxidation of iron by O₂ and water |
| Biology | photosynthesis (CO₂ reduced) and respiration (glucose oxidised) |
| Industry | Ostwald process (NH₃ oxidised to HNO₃), contact process (SO₂ → SO₃), chlorine water treatment |
| Breath tests | orange Cr₂O₇²⁻ is reduced to green Cr³⁺ by ethanol |

## Formula and fact sheet

| Item | Rule |
|---|---|
| Oxidation | loss of e⁻; increase in oxidation number; addition of O or removal of H (classical) |
| Reduction | gain of e⁻; decrease in oxidation number |
| Oxidising agent | gets reduced (accepts e⁻); reducing agent gets oxidised |
| Sum of oxidation numbers | 0 for a molecule; the charge for an ion |
| Fixed values | F −1; group 1 +1; group 2 +2; O −2 (except peroxide −1, superoxide −½, OF₂ +2); H +1 (−1 in metal hydrides) |
| Balancing in acid | O with H₂O, H with H⁺, charge with e⁻ |
| Balancing in base | balance as acid, then add OH⁻ to both sides to remove H⁺ |
| n-factor rule | moles react in the inverse ratio of n-factors |

| Must-know balanced equations |
|---|
| MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O |
| Cr₂O₇²⁻ + 6Fe²⁺ + 14H⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O |
| 2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O |
| 3Cu + 8HNO₃ (dilute) → 3Cu(NO₃)₂ + 2NO + 4H₂O |
| Cu + 4HNO₃ (concentrated) → Cu(NO₃)₂ + 2NO₂ + 2H₂O |
| 2KMnO₄ + 16HCl → 2KCl + 2MnCl₂ + 5Cl₂ + 8H₂O |
| 2S₂O₃²⁻ + I₂ → S₄O₆²⁻ + 2I⁻ |

## Chapter summary

- Classical: oxidation = addition of O or an electronegative element, removal of H or an electropositive element; reduction the reverse.
- Electronic: oxidation = loss of electrons, reduction = gain; the oxidant is reduced and the reductant oxidised; both always occur together.
- Oxidation number rules: free element 0; F −1; O −2 except peroxides (−1), superoxides (−½) and OF₂ (+2); H +1 except metal hydrides (−1); the sum equals the charge.
- Watch the traps: Fe₃O₄ +8/3, S₄O₆²⁻ +2.5, CrO₅ and H₂S₂O₈ +6 (peroxide links), OsO₄ +8, NH₄NO₃ −3 and +5.
- Highest oxidation state → only an oxidant; lowest → only a reductant; intermediate → both, and able to disproportionate (H₂O₂, Cl₂ in alkali, Cu⁺, HNO₂).
- Balancing: equalise the total change in oxidation number, or add half-reactions after balancing O with H₂O, H with H⁺ (OH⁻ in base) and charge with electrons.
- n-factors: MnO₄⁻ 5 (acid), 3 (neutral), 1 (strong base); Cr₂O₇²⁻ 6; moles react in the inverse ratio of n-factors.

## Practice questions

**Set A — Recall (20 questions)**

1. In terms of electrons, oxidation is
   (a) loss of electrons (b) gain of electrons (c) gain of protons (d) loss of neutrons
2. In the classical concept, which change is a reduction?
   (a) addition of oxygen (b) removal of hydrogen (c) removal of oxygen (d) addition of an electronegative element
3. An oxidising agent is a substance that
   (a) loses electrons (b) is itself oxidised (c) donates hydrogen (d) gains electrons and is itself reduced
4. The oxidation number of an element in its free (uncombined) state is
   (a) +1 (b) 0 (c) −1 (d) equal to its valency
5. The oxidation number of oxygen in H₂O₂ is
   (a) −2 (b) −½ (c) −1 (d) +1
6. The oxidation number of hydrogen in NaH is
   (a) −1 (b) +1 (c) 0 (d) +2
7. The oxidation number of manganese in KMnO₄ is
   (a) +6 (b) +7 (c) +5 (d) +4
8. The oxidation number of chromium in K₂Cr₂O₇ is
   (a) +3 (b) +7 (c) +12 (d) +6
9. The oxidation number of oxygen in OF₂ is
   (a) −2 (b) −1 (c) +2 (d) 0
10. A reaction in which the same element is both oxidised and reduced is called
   (a) disproportionation (b) displacement (c) combination (d) neutralisation
11. The oxidation number of fluorine in all its compounds is
   (a) +1 (b) 0 (c) +1 or −1 (d) −1
12. In the reaction Zn + Cu²⁺ → Zn²⁺ + Cu, the reducing agent is
   (a) Cu²⁺ (b) Zn (c) Zn²⁺ (d) Cu
13. The oxidation number of osmium in OsO₄, the highest found in any stable compound, is
   (a) +8 (b) +7 (c) +6 (d) +4
14. Oxygen has the oxidation number −½ in
   (a) H₂O₂ (b) BaO₂ (c) KO₂ (d) OF₂
15. Which of these can act only as a reducing agent?
   (a) SO₂ (b) H₂S (c) H₂SO₄ (d) S
16. Which of these can act only as an oxidising agent?
   (a) H₂O₂ (b) SO₂ (c) HNO₂ (d) KMnO₄
17. The oxidation number of nitrogen in HNO₃ is
   (a) +5 (b) +3 (c) +4 (d) −3
18. In the ion-electron method for an acidic solution, oxygen atoms are balanced by adding
   (a) OH⁻ ions (b) O₂ molecules (c) electrons (d) H₂O molecules
19. The rusting of iron is an example of
   (a) the reduction of iron (b) neutralisation (c) the oxidation of iron (d) the decomposition of iron
20. In the reaction 2FeCl₂ + Cl₂ → 2FeCl₃, iron(II) chloride is
   (a) reduced, as chlorine is removed (b) oxidised, as an electronegative element is added (c) neither oxidised nor reduced (d) oxidised, as hydrogen is removed

::: note Answers and explanations — Set A
**1.** (a) — Oxidation is loss of electrons (OIL RIG); gain of electrons is reduction.
**2.** (c) — Removal of oxygen is reduction (CuO + H₂ → Cu + H₂O). The other three are classical oxidations.
**3.** (d) — An oxidant takes electrons from something else and is reduced in doing so.
**4.** (b) — Atoms of one element share bonding electrons equally, so each is 0 (H₂, O₂, P₄, S₈, Na).
**5.** (c) — 2(+1) + 2x = 0 → x = −1 (a peroxide). −½ is the superoxide value.
**6.** (a) — In a metal hydride hydrogen is the more electronegative partner: Na⁺H⁻.
**7.** (b) — +1 + x + 4(−2) = 0 → x = +7.
**8.** (d) — 2(+1) + 2x + 7(−2) = 0 → 2x = 12 → x = +6 for each Cr. Option (c) is the total for both Cr atoms.
**9.** (c) — Fluorine is more electronegative, so each F is −1 and O must be +2.
**10.** (a) — Disproportionation, e.g. 2H₂O₂ → 2H₂O + O₂ (O: −1 → −2 and 0).
**11.** (d) — Fluorine, the most electronegative element, is −1 in every compound.
**12.** (b) — Zn loses two electrons (0 → +2), so it is the reducing agent; Cu²⁺ is the oxidising agent.
**13.** (a) — x + 4(−2) = 0 → x = +8. Osmium in OsO₄ and ruthenium in RuO₄ reach +8, the highest oxidation number in stable compounds.
**14.** (c) — In KO₂ the superoxide ion O₂⁻ carries −1 over two O atoms: −½ each. BaO₂ and H₂O₂ are peroxides (−1).
**15.** (b) — Sulphur at −2, its lowest state, can only lose electrons. SO₂ (+4) and S (0) can go up or down; H₂SO₄ (+6) can only go down.
**16.** (d) — Mn in KMnO₄ is +7, its maximum, so it can only gain electrons. H₂O₂, SO₂ and HNO₂ are in intermediate states and can act both ways.
**17.** (a) — +1 + x + 3(−2) = 0 → x = +5.
**18.** (d) — Water supplies O; H⁺ then balances the hydrogen. OH⁻ is used only when converting to a basic medium.
**19.** (c) — Iron goes from 0 to +3 in hydrated Fe₂O₃ (rust) — it is oxidised; oxygen is reduced.
**20.** (b) — Adding an electronegative element (Cl) is oxidation in the classical sense; electronically Fe²⁺ → Fe³⁺ + e⁻.
:::

**Set B — Understanding (13 questions)**

1. The oxidation number of iron in Fe₃O₄ is
   (a) +2 (b) +3 (c) +8/3 (d) +4/3
2. The average oxidation number of sulphur in the tetrathionate ion S₄O₆²⁻ is
   (a) +2.5 (b) +2 (c) +3 (d) +6
3. The oxidation number of chromium in CrO₅, which contains two peroxide groups, is
   (a) +10 (b) +5 (c) +8 (d) +6
4. In the reaction Cl₂ + 2NaOH (cold, dilute) → NaCl + NaClO + H₂O, chlorine is
   (a) only oxidised (b) both oxidised and reduced (c) only reduced (d) unchanged in oxidation number
5. Which of the following is NOT a redox reaction?
   (a) NaOH + HCl → NaCl + H₂O (b) Zn + 2HCl → ZnCl₂ + H₂ (c) 2KClO₃ → 2KCl + 3O₂ (d) CuO + H₂ → Cu + H₂O
6. H₂O₂ can act both as an oxidising agent and as a reducing agent because
   (a) it contains hydrogen (b) it is a liquid (c) its oxygen is at −1, between −2 and 0 (d) it is a strong acid
7. In H₂S + Cl₂ → 2HCl + S, the substance oxidised is
   (a) Cl₂ (b) HCl (c) S (d) H₂S
8. The oxidation numbers of the two nitrogen atoms in NH₄NO₃ are
   (a) +1 and +5 (b) −3 and +5 (c) +3 and −5 (d) 0 and +2
9. In acidic solution MnO₄⁻ is reduced to Mn²⁺. The number of electrons gained per MnO₄⁻ ion is
   (a) 3 (b) 1 (c) 5 (d) 7
10. In which compound is the oxidation number of carbon zero?
   (a) HCHO (b) CH₃OH (c) HCOOH (d) CO₂
11. When Cr₂O₇²⁻ is reduced to Cr³⁺ in acid, the number of electrons gained per Cr₂O₇²⁻ ion is
   (a) 3 (b) 6 (c) 2 (d) 12
12. Which reaction is a comproportionation, the reverse of disproportionation?
   (a) 2H₂O₂ → 2H₂O + O₂ (b) Cl₂ + 2OH⁻ → Cl⁻ + OCl⁻ + H₂O (c) 3HNO₂ → HNO₃ + 2NO + H₂O (d) 2H₂S + SO₂ → 3S + 2H₂O
13. Sulphur dioxide bleaches by ___ and chlorine bleaches by ___.
   (a) reduction; oxidation (b) oxidation; reduction (c) oxidation; oxidation (d) reduction; reduction

::: note Answers and explanations — Set B
**1.** (c) — 3x + 4(−2) = 0 → x = +8/3, an average: Fe₃O₄ is really FeO·Fe₂O₃, one Fe²⁺ and two Fe³⁺.
**2.** (a) — 4x + 6(−2) = −2 → 4x = 10 → x = +2.5 (an average of two S at +5 and two at 0).
**3.** (d) — x + 4(−1) + (−2) = 0 → x = +6. The naive sum with every O at −2 gives +10, beyond chromium's maximum of +6.
**4.** (b) — Cl goes from 0 to −1 in NaCl (reduced) and from 0 to +1 in NaClO (oxidised): disproportionation.
**5.** (a) — Neutralisation: Na +1, O −2, H +1, Cl −1 on both sides — no oxidation number changes.
**6.** (c) — Oxygen at −1 can be reduced to −2 (H₂O) or oxidised to 0 (O₂).
**7.** (d) — S goes from −2 in H₂S to 0: H₂S is oxidised (it loses hydrogen); Cl₂ is reduced.
**8.** (b) — NH₄⁺: x + 4 = +1 → −3; NO₃⁻: x − 6 = −1 → +5.
**9.** (c) — +7 → +2 is a gain of 5 electrons: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O.
**10.** (a) — HCHO: x + 2(+1) + (−2) = 0 → 0. CH₃OH −2, HCOOH +2, CO₂ +4.
**11.** (b) — Each Cr goes +6 → +3 (3 electrons) and there are two Cr atoms: 6 electrons.
**12.** (d) — S at −2 (H₂S) and +4 (SO₂) both end at 0. Options (a), (b) and (c) are disproportionations.
**13.** (a) — SO₂ + 2H₂O → H₂SO₄ + 2[H]: the nascent hydrogen reduces the dye (temporary bleaching). Cl₂ + H₂O → HCl + HOCl, and HOCl gives [O], which oxidises the dye (permanent).
:::

**Set C — Application (9 questions)**

1. In the balanced equation a Cu + b HNO₃ (dilute) → a Cu(NO₃)₂ + 2NO + 4H₂O, a and b are
   (a) 1, 4 (b) 3, 8 (c) 3, 6 (d) 2, 8
2. In the balanced equation MnO₄⁻ + 5Fe²⁺ + x H⁺ → Mn²⁺ + 5Fe³⁺ + y H₂O, x and y are
   (a) 4, 8 (b) 8, 8 (c) 16, 8 (d) 8, 4
3. The number of moles of KMnO₄ needed to oxidise 1 mol of Fe²⁺ to Fe³⁺ in acidic solution is
   (a) 0.2 (b) 5 (c) 1 (d) 0.5
4. The number of moles of K₂Cr₂O₇ needed to oxidise 1 mol of ferrous oxalate, FeC₂O₄, completely in acidic solution (Fe²⁺ → Fe³⁺ and C₂O₄²⁻ → CO₂) is
   (a) 1 (b) 1/6 (c) 1/2 (d) 3
5. The total number of electrons transferred in 2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O is
   (a) 5 (b) 2 (c) 16 (d) 10
6. In neutral or faintly alkaline solution MnO₄⁻ oxidises I⁻ to IO₃⁻ and is itself reduced to MnO₂. The number of moles of MnO₄⁻ that react with 1 mol of I⁻ is
   (a) 1 (b) 2 (c) 3 (d) 6
7. The oxidation number of phosphorus in hypophosphorous acid, H₃PO₂ (one OH group and two P–H bonds), is
   (a) +1 (b) +3 (c) +5 (d) −1
8. In the balanced equation Cr₂O₇²⁻ + x Fe²⁺ + y H⁺ → 2Cr³⁺ + x Fe³⁺ + 7H₂O, x and y are
   (a) 3, 14 (b) 6, 7 (c) 6, 14 (d) 2, 14
9. In hot alkali, 3Cl₂ + 6OH⁻ → 5Cl⁻ + ClO₃⁻ + 3H₂O. The ratio of chlorine atoms reduced to chlorine atoms oxidised is
   (a) 5 : 1 (b) 1 : 5 (c) 3 : 1 (d) 1 : 1

::: note Answers and explanations — Set C
**1.** (b) — Cu 0 → +2 (2e⁻); N +5 → +2 (3e⁻): 3Cu (6e⁻) against 2NO (6e⁻). Nitrogen: 3 × 2 in Cu(NO₃)₂ + 2 = 8 HNO₃; hydrogen 8 = 4H₂O × 2. ✓
**2.** (d) — Oxygen: 4 O in MnO₄⁻ → y = 4 H₂O; hydrogen: x = 8 H⁺. Charge check: −1 + 10 + 8 = +17 = +2 + 15. ✓
**3.** (a) — n-factors 5 (MnO₄⁻) and 1 (Fe²⁺): moles in the inverse ratio, so 1/5 = 0.2 mol KMnO₄.
**4.** (c) — FeC₂O₄ loses 1 (Fe) + 2 (C₂O₄²⁻) = 3 electrons; Cr₂O₇²⁻ gains 6. Moles of dichromate = 3/6 = 1/2. Option (b) forgets the oxalate.
**5.** (d) — Each MnO₄⁻ gains 5e⁻ and there are 2: 10 electrons (equally, 5 C₂O₄²⁻ × 2e⁻ = 10).
**6.** (b) — I⁻ → IO₃⁻ loses 6 electrons; MnO₄⁻ → MnO₂ gains 3. So 2 MnO₄⁻ per I⁻: 2MnO₄⁻ + I⁻ + H₂O → 2MnO₂ + IO₃⁻ + 2OH⁻.
**7.** (a) — 3(+1) + x + 2(−2) = 0 → x = +1. (+3 is H₃PO₃ and +5 is H₃PO₄.)
**8.** (c) — Cr₂O₇²⁻ gains 6 electrons, so x = 6 Fe²⁺; 7 H₂O need y = 14 H⁺. Charge: −2 + 12 + 14 = +24 = 6 + 18. ✓
**9.** (a) — Five Cl go 0 → −1 (Cl⁻, reduced) and one goes 0 → +5 (ClO₃⁻, oxidised): 5 × 1 e⁻ gained = 1 × 5 e⁻ lost.
:::

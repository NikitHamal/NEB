---
subject: Chemistry
grade: CEE
unit: 6
title: States of Matter
hours: 2
area: Physical Chemistry
---

States of matter carries about **two questions** in the paper. It is a wide chapter, so the questions spread: a gas-law or kinetic-theory
calculation (combined gas equation, Graham's law, partial pressure, rms speed), a
real-gas idea (van der Waals constants, when gases behave ideally), a liquid property
(vapour pressure, boiling point, surface tension, viscosity, liquid crystals, solubility
curves) or a solid-state fact (crystalline versus amorphous, deliquescent versus
hygroscopic, crystal systems, atoms per unit cell). Most are one-line answers if the
relations are learnt as proportionalities.

::: key What the paper asks from this chapter
- Kinetic theory: average KE = (3/2)RT per mole, depends only on T; $u_{rms} = \sqrt{3RT/M}$; $u_{mp} : u_{av} : u_{rms} = 1 : 1.128 : 1.224$.
- Gas laws: Boyle, Charles, pressure law, Avogadro → PV = nRT; combined $P_1V_1/T_1 = P_2V_2/T_2$ (T in kelvin); Dalton $p_i = x_iP$; Graham $r \propto 1/\sqrt{M}$.
- Real gases: Z = PV/nRT; van der Waals a (attraction) and b (volume); ideal at low P and high T.
- Liquids: vapour pressure depends only on the liquid and T; boiling point when VP = external pressure; surface tension and viscosity fall with temperature; liquid crystals are the mesophase.
- Solids: crystalline (sharp mp, anisotropic) versus amorphous (softening range, isotropic); efflorescent, deliquescent, hygroscopic; water of crystallisation.
- 7 crystal systems, 14 Bravais lattices; Z = 1, 2, 4 and coordination 6, 8, 12 for simple, body-centred and face-centred cubic; ρ = ZM/(a³N_A).
:::

## 6.1 Gases: kinetic theory, gas laws, ideal and combined gas equations, deviation of real gases

### Kinetic theory of gases

The postulates (for an ideal gas):

1. A gas consists of a very large number of tiny particles whose own volume is negligible
   compared with the volume of the container.
2. The particles move randomly in straight lines in all directions, colliding with one
   another and with the walls; the **pressure** is due to collisions with the walls.
3. The collisions are perfectly **elastic** (no loss of total kinetic energy).
4. There are **no forces of attraction or repulsion** between the particles.
5. The **average kinetic energy is proportional to the absolute temperature**.

From these follows the kinetic gas equation, $PV = \frac{1}{3}mNu_{rms}^2$, and with
PV = RT for one mole:

$$ E_k = \frac{3}{2}RT \ \text{per mole}, \qquad \bar{\varepsilon} = \frac{3}{2}kT \ \text{per molecule}, \qquad u_{rms} = \sqrt{\frac{3RT}{M}} = \sqrt{\frac{3P}{\rho}} $$

(k = R/N_A = 1.38 × 10⁻²³ J K⁻¹; M in **kg mol⁻¹** when R = 8.314 J mol⁻¹ K⁻¹.) At a given
temperature **all gases have the same average kinetic energy**; lighter molecules simply
move faster. At absolute zero the kinetic energy would be zero.

| Speed | Formula | Relative value |
|---|---|---|
| Most probable, $u_{mp}$ | $\sqrt{2RT/M}$ | 1 |
| Average (mean), $u_{av}$ | $\sqrt{8RT/\pi M}$ | 1.128 |
| Root mean square, $u_{rms}$ | $\sqrt{3RT/M}$ | 1.224 |

```figure caption="Maxwell distribution of molecular speeds for nitrogen. At 300 K the three characteristic speeds are $u_{mp} < u_{av} < u_{rms}$. At a higher temperature the curve flattens and shifts to higher speeds, but the area under it (the total number of molecules) stays the same."
import numpy as np, matplotlib.pyplot as plt
R = 8.314; M = 0.028
v = np.linspace(0, 1600, 600)
def f(T):
    return 4*np.pi*(M/(2*np.pi*R*T))**1.5 * v**2 * np.exp(-M*v**2/(2*R*T))*1000
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.plot(v, f(300), color=ACCENT, lw=2.0, label='300 K')
ax.plot(v, f(900), color=SERIES[1], lw=1.8, ls='--', label='900 K')
T = 300
sp = [('u$_{mp}$', np.sqrt(2*R*T/M), 250, 2.45, 'right'), ('u$_{av}$', np.sqrt(8*R*T/(np.pi*M)), 476, 2.85, 'center'),
      ('u$_{rms}$', np.sqrt(3*R*T/M), 690, 2.45, 'left')]
for lab, u, xt, yt, ha in sp:
    y = np.interp(u, v, f(300))
    ax.plot([u, u], [0, y], color=MUTED, lw=0.8, ls=':')
    ax.annotate(lab, (u, y), xytext=(xt, yt), fontsize=8.6, color=INK, va='bottom' if ha == 'center' else 'center', ha=ha,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6, shrinkA=1, shrinkB=1))
ax.set_xlabel('molecular speed (m s$^{-1}$)')
ax.set_ylabel('fraction of molecules\n(per km s$^{-1}$)')
ax.set_xlim(0, 1600); ax.set_ylim(0, 2.6*1.25)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=0.45)
ax.legend(loc='upper right', fontsize=8.2, frameon=False)
```

### The gas laws

| Law | Statement (fixed amount of gas) | Form |
|---|---|---|
| Boyle (1662) | at constant T, volume is inversely proportional to pressure | PV = constant; P₁V₁ = P₂V₂ |
| Charles (1787) | at constant P, volume is directly proportional to absolute temperature | V/T = constant; V_t = V₀(1 + t/273) |
| Pressure law (Gay-Lussac) | at constant V, pressure is directly proportional to absolute temperature | P/T = constant |
| Avogadro | at constant T and P, volume is proportional to the number of moles | V/n = constant |
| Combined | all of the above together | P₁V₁/T₁ = P₂V₂/T₂ |

Charles's law, extrapolated, gives zero volume at **−273.15 °C** — absolute zero, the
origin of the kelvin scale (T/K = t/°C + 273). Graph shapes are a favourite: P against V
is a rectangular hyperbola; P against 1/V, and V against T, are straight lines through the
origin; PV against P (at constant T) is a horizontal line.

### The ideal gas equation

$$ PV = nRT, \qquad n = \frac{w}{M} \;\Rightarrow\; PV = \frac{w}{M}RT, \qquad \rho = \frac{PM}{RT} $$

| R in | Value |
|---|---|
| J mol⁻¹ K⁻¹ (SI) | 8.314 |
| L atm mol⁻¹ K⁻¹ | 0.0821 |
| cal mol⁻¹ K⁻¹ | 1.987 (≈ 2) |

R is the work done by one mole of an ideal gas when it is heated through 1 K at constant
pressure; it has the same value for all gases. An **ideal gas** obeys PV = nRT exactly at all temperatures and
pressures; no real gas does.

::: example Combined gas equation
**Problem.** A gas occupies 500 mL at 27 °C and 1.0 atm. Find its volume at 177 °C and
1.5 atm.

**Solution.** Convert to kelvin: 300 K and 450 K.
V₂ = V₁ × (P₁/P₂) × (T₂/T₁) = 500 × (1.0/1.5) × (450/300) = **500 mL** — the two changes
cancel exactly. Never put °C into a gas law.
:::

### Dalton's law of partial pressures

The total pressure of a mixture of **non-reacting** gases equals the sum of their partial
pressures (the pressure each would exert alone in the whole volume):
$P = p_1 + p_2 + \ldots$, and $p_i = x_iP$ where $x_i$ is the mole fraction. A gas collected
over water is saturated with water vapour, so
p(dry gas) = P(total) − aqueous tension (the vapour pressure of water at that temperature).

### Graham's law of diffusion

At constant temperature and pressure, the rate of diffusion (or effusion) of a gas is
inversely proportional to the square root of its density, and hence of its molar mass:

$$ \frac{r_1}{r_2} = \sqrt{\frac{\rho_2}{\rho_1}} = \sqrt{\frac{M_2}{M_1}}, \qquad \text{and for equal volumes } \frac{t_1}{t_2} = \sqrt{\frac{M_1}{M_2}} $$

Uses: separating ²³⁵UF₆ from ²³⁸UF₆; finding molar masses. When NH₃ and HCl are released
at the two ends of a tube, NH₃ (M = 17) travels √(36.5/17) = 1.47 times faster than HCl,
so the white ring of NH₄Cl forms **nearer the HCl end** (about 59 % of the way from the NH₃
end).

::: example Graham's law in one line
**Problem.** A gas takes 3 times as long as oxygen to effuse through the same hole under the
same conditions. Find its molar mass.

**Solution.** t ∝ √M, so M = 32 × 3² = **288 g mol⁻¹**. (Squaring the time ratio is the step
most often forgotten.)
:::

### Deviation of real gases from ideality

Real gases deviate because two postulates are false: the molecules **do** have volume and
they **do** attract one another. The deviation is measured by the **compressibility factor**

$$ Z = \frac{PV}{nRT} $$

Z = 1 for an ideal gas. Z < 1 (more compressible than ideal) when attractions dominate —
moderate pressures, for easily liquefied gases such as CO₂ and NH₃. Z > 1 when the molecular
volume dominates — at high pressure for all gases, and at all pressures for H₂ and He at
room temperature. Real gases behave most ideally at **low pressure and high temperature**.

**The van der Waals equation** corrects both postulates:

$$ \left(P + \frac{an^2}{V^2}\right)(V - nb) = nRT $$

- a measures the **attractive forces** (pressure correction, unit atm L² mol⁻²). Easily
  liquefied gases (NH₃, SO₂, CO₂) have large a; H₂ and He have very small a.
- b is the **excluded volume** (volume correction, unit L mol⁻¹), about four times the
  actual volume of the molecules in one mole.
- **Boyle temperature** $T_B = a/Rb$: the temperature at which a real gas obeys Boyle's law
  over a range of pressure. **Critical temperature** $T_c = 8a/27Rb$: above it a gas cannot
  be liquefied by pressure alone (CO₂ 31 °C, NH₃ 132 °C, O₂ −119 °C, He −268 °C).

::: caution Gas-law slips the options are built on
Celsius instead of kelvin; M in g mol⁻¹ with R = 8.314 J (it must be kg mol⁻¹ — the answer
comes out √1000 ≈ 31.6 times too small); forgetting to square the time ratio in Graham's law;
and using total moles instead of the mole fraction for a partial pressure.
:::

## 6.2 Liquids: vapour pressure, boiling point, surface tension, viscosity, liquid crystals, solubility and solubility curves

### Vapour pressure and boiling point

**Evaporation** is the escape of the fastest surface molecules at any temperature; it
cools the liquid left behind. In a closed vessel evaporation and condensation reach a
dynamic equilibrium, and the pressure of the vapour then is the **vapour pressure**. It
depends **only on the nature of the liquid and the temperature** — not on the amount of
liquid, the surface area or the volume of the vessel. It rises steeply with temperature,
and it is high for liquids with weak intermolecular forces (diethyl ether > ethanol >
water at the same temperature).

::: definition Boiling point
A liquid boils when its **vapour pressure equals the external pressure**. The **normal
boiling point** is the boiling temperature at 1 atm (760 mmHg): water 100 °C.
:::

Lower the external pressure and the boiling point falls: water boils at about 95 °C in
Kathmandu (about 1400 m, near 640 mmHg) and at about 70 °C on the summit of Mount Everest,
so food cooks slowly there. A pressure cooker raises the pressure, and so the boiling
point, to about 120 °C. Water at 25 °C has a vapour pressure of 23.8 mmHg.

### Surface tension

::: definition Surface tension
**Surface tension** is the force acting per unit length at right angles to an imaginary
line drawn on the surface of a liquid. SI unit **N m⁻¹** (also J m⁻², energy per unit
area; CGS dyne cm⁻¹).
:::

A molecule inside the liquid is pulled equally in all directions; one at the surface is
pulled inwards only, so the surface behaves like a stretched skin and tends to
**minimise its area**. Results: drops and bubbles are spherical; water rises in a narrow
glass capillary (mercury falls); insects walk on water; a needle floats. Surface tension
**decreases as temperature rises** (it vanishes at the critical temperature) and is lowered
sharply by soaps and detergents. Water's value (about 72 mN m⁻¹ at 25 °C) is high because
of hydrogen bonding. With a stalagmometer (drop-number method),
$\gamma_1/\gamma_2 = \rho_1 n_2/(\rho_2 n_1)$ — fewer, bigger drops mean a higher surface
tension.

### Viscosity

::: definition Viscosity
**Viscosity** is the internal resistance of a fluid to flow. The coefficient of viscosity
η is the tangential force per unit area needed to maintain unit velocity gradient between
two layers: $F = \eta A\,(dv/dx)$. SI unit **N s m⁻² = Pa s** (= kg m⁻¹ s⁻¹); CGS unit the
poise (1 P = 0.1 Pa s). Its reciprocal is fluidity.
:::

The viscosity of a liquid **decreases with rising temperature** (molecules gain energy to
overcome attractions) — but the viscosity of a **gas increases** with temperature. Strong
intermolecular forces and large molecules raise viscosity: glycerol (three OH groups,
extensive hydrogen bonding) ≫ ethylene glycol > water > diethyl ether. With an Ostwald
viscometer, $\eta_1/\eta_2 = \rho_1 t_1/(\rho_2 t_2)$.

### Liquid crystals

Some organic substances with long, rod-like molecules melt first to a cloudy fluid that
**flows like a liquid but keeps some of the orientational order of a crystal** — the
**liquid crystal** (mesomorphic) state. Reinitzer (1888) saw it in cholesteryl benzoate,
which turns cloudy at 145 °C and clear at 179 °C.

| Type | Order | Note |
|---|---|---|
| Nematic (thermotropic) | molecules parallel, not in layers | used in LCD screens |
| Smectic (thermotropic) | parallel and arranged in layers | most ordered |
| Cholesteric (thermotropic) | layers twisted one over another | colour changes with temperature |
| Lyotropic | formed on dissolving in a solvent | soap solutions, cell membranes |

Uses: liquid crystal displays (watches, calculators, phones, televisions), temperature
strips and thermometers, and medical thermography (locating tumours and blocked blood
vessels by skin temperature).

### Solubility and solubility curves

**Solubility** is the mass of solute (in grams) that dissolves in **100 g of solvent** to
give a saturated solution at a stated temperature. A **solubility curve** plots it against
temperature.

```figure caption="Solubility curves in water. KNO₃ rises steeply, NaCl hardly changes, and sodium sulphate rises (as Na₂SO₄·10H₂O) up to the transition point near 32.4 °C, then falls (as anhydrous Na₂SO₄)."
import numpy as np, matplotlib.pyplot as plt
T = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
kno3 = [13.3, 20.9, 31.6, 45.8, 63.9, 85.5, 110, 138, 169, 202, 246]
nacl = [35.7, 35.8, 35.9, 36.1, 36.4, 36.7, 37.1, 37.5, 38.0, 38.5, 39.2]
kcl = [27.6, 31.0, 34.0, 37.0, 40.0, 42.6, 45.5, 48.3, 51.1, 54.0, 56.7]
Ts = [0, 10, 20, 30, 32.4, 40, 60, 80, 100]
na2so4 = [4.9, 9.1, 19.5, 40.8, 49.7, 48.8, 45.3, 43.7, 42.5]
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.plot(T, kno3, '-', color=SERIES[0], lw=1.9)
ax.plot(T, kcl, '-', color=SERIES[2], lw=1.6)
ax.plot(T, nacl, '-', color=SERIES[1], lw=1.6)
ax.plot(Ts, na2so4, '-', color=SERIES[3], lw=1.6)
ax.text(78, 205, 'KNO₃', fontsize=8.6, color=SERIES[0])
ax.text(101, 60, 'KCl', fontsize=8.6, color=SERIES[2], va='center')
ax.text(101, 44, 'Na₂SO₄', fontsize=8.6, color=SERIES[3], va='center')
ax.text(2, 44, 'NaCl', fontsize=8.6, color=SERIES[1], va='center')
ax.plot([32.4], [49.7], 'o', color=SERIES[3], ms=4.5, zorder=5)
ax.annotate('Na₂SO₄ transition\npoint, 32.4 °C', (32.4, 49.7), xytext=(18, 100), fontsize=8, color=SERIES[3],
            arrowprops=dict(arrowstyle='-', color=SERIES[3], lw=0.7))
ax.set_xlabel('temperature (°C)'); ax.set_ylabel('solubility (g per 100 g water)')
ax.set_xlim(0, 118); ax.set_ylim(0, 260)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=0.45)
```

- Most solids dissolve better when hot; KNO₃, NH₄Cl and KCl strongly, NaCl only slightly.
  A few become **less** soluble on heating — Ca(OH)₂, Li₂SO₄ and Ce₂(SO₄)₃.
- A kink marks a change of the solid phase (Na₂SO₄·10H₂O → Na₂SO₄ at 32.4 °C).
- **Gases** become less soluble as temperature rises and more soluble as pressure rises
  (Henry's law) — that is why fish need cool, oxygen-rich water and why a soft drink
  fizzes when opened.
- **Uses of curves:** finding the mass that crystallises on cooling (difference of two
  solubilities), choosing a method of crystallisation (cooling for KNO₃, evaporation for
  NaCl), and separating salts by fractional crystallisation.

::: example Mass crystallising on cooling
**Problem.** A solution of KNO₃ saturated at 60 °C contains 100 g of water. How much KNO₃
crystallises when it is cooled to 20 °C? (Solubility 110 g and 31.6 g per 100 g water.)

**Solution.** Mass that crystallises = 110 − 31.6 = **78.4 g**. (For w grams of water,
scale by w/100.) The same cooling would deposit only about 1.2 g of NaCl from its saturated
solution, which is why salt is crystallised by evaporation instead.
:::

## 6.3 Solids: crystalline and amorphous solids; efflorescent, deliquescent and hygroscopic substances; water of crystallisation

### Crystalline and amorphous solids

| Property | Crystalline | Amorphous |
|---|---|---|
| Arrangement of particles | regular, repeating, **long-range order** | irregular, only **short-range order** |
| Shape | definite geometric shape | no definite shape |
| Melting | **sharp** melting point | **soften over a range** of temperature |
| Heat of fusion | definite | not definite |
| Physical properties with direction | **anisotropic** (differ with direction) | **isotropic** (same in all directions) |
| Cutting | clean cleavage along planes | irregular fracture |
| Nature | true solids | pseudo-solids or supercooled liquids |
| Examples | NaCl, quartz, diamond, sugar, ice, metals | glass, rubber, plastics, fused silica, pitch |

Quartz (crystalline SiO₂) and fused silica glass (amorphous SiO₂) are the same compound in
the two forms. Amorphous solids are often called **pseudo-solids** or **supercooled
liquids**: their particles are frozen in the disorder of a liquid.

### Efflorescent, deliquescent and hygroscopic substances

| Term | Behaviour in moist air | Examples |
|---|---|---|
| **Efflorescent** | **loses** water of crystallisation to the air and crumbles to a powder | washing soda Na₂CO₃·10H₂O, Glauber's salt Na₂SO₄·10H₂O, FeSO₄·7H₂O |
| **Deliquescent** | **absorbs** so much moisture that it **dissolves** in it | CaCl₂, NaOH, KOH, MgCl₂, FeCl₃, ZnCl₂ |
| **Hygroscopic** | **absorbs** moisture but **does not dissolve** (or is a liquid that takes up water) | quicklime CaO, silica gel, anhydrous CuSO₄, P₄O₁₀, conc. H₂SO₄ |

A hydrate effloresces when its own water-vapour pressure is **greater** than the partial
pressure of water in the air; a solid deliquesces when its saturated solution has a vapour
pressure **lower** than that of the air. Deliquescent and hygroscopic substances are
**drying agents**: fused CaCl₂, quicklime (for ammonia), conc. H₂SO₄, P₄O₁₀ and silica gel.
Common salt becomes damp in the rainy season only because of traces of deliquescent MgCl₂
and CaCl₂ in it.

::: caution Deliquescent is not the same as hygroscopic
Both absorb water. A deliquescent solid ends up as a **solution**; a hygroscopic solid only
becomes **damp**. Every deliquescent substance is hygroscopic, but not every hygroscopic
substance is deliquescent.
:::

### Crystallisation and water of crystallisation

**Crystallisation** purifies a solid: dissolve it in the minimum of hot solvent, filter hot,
and cool slowly; crystals separate and soluble impurities stay in the mother liquor. A
crystal grows by **nucleation** (a tiny ordered cluster forms) followed by **growth** (more
particles add to its faces); slow, undisturbed cooling gives fewer, larger crystals.

::: definition Water of crystallisation
The **water of crystallisation** is the fixed number of water molecules combined with one
formula unit of a salt in its crystals. It is responsible for the shape (and often the
colour) of the crystals and is driven off on heating: CuSO₄·5H₂O (blue) → CuSO₄ (white)
+ 5H₂O.
:::

| Name | Formula | Name | Formula |
|---|---|---|---|
| Blue vitriol | CuSO₄·5H₂O | Washing soda | Na₂CO₃·10H₂O |
| Green vitriol | FeSO₄·7H₂O | Glauber's salt | Na₂SO₄·10H₂O |
| White vitriol | ZnSO₄·7H₂O | Gypsum | CaSO₄·2H₂O |
| Epsom salt | MgSO₄·7H₂O | Plaster of Paris | CaSO₄·½H₂O |
| Borax | Na₂B₄O₇·10H₂O | Potash alum | K₂SO₄·Al₂(SO₄)₃·24H₂O |
| Mohr's salt | FeSO₄·(NH₄)₂SO₄·6H₂O | Hypo | Na₂S₂O₃·5H₂O |

::: example Finding x in a hydrate
**Problem.** Crystals of Na₂CO₃·xH₂O lose 62.9 % of their mass when heated to constant mass.
Find x. (Na₂CO₃ = 106)

**Solution.** 18x/(106 + 18x) = 0.629 → 18x(1 − 0.629) = 66.7 → x = 66.7/6.68 = **10**
(washing soda).
:::

## 6.4 The unit cell, the seven crystal systems and the fourteen Bravais lattices; types of crystalline solid by bonding

### Lattice, unit cell and crystal systems

::: definition Crystal lattice and unit cell
A **crystal lattice** (space lattice) is the regular three-dimensional array of points that
shows the positions of the particles in a crystal. The **unit cell** is the smallest
portion of the lattice which, repeated in three dimensions, generates the whole crystal.
It is described by the edge lengths a, b, c and the angles α, β, γ between them.
:::

Only **seven crystal systems** are possible, and placing particles at corners, body centres,
face centres or end-face centres gives **fourteen Bravais lattices** in all (Bravais, 1848).

```photo id="chem11/nacl-cell" caption="A ball-and-stick model of the sodium chloride unit cell: each ion sits at the centre of an octahedron of six ions of the opposite charge (6 : 6 coordination)." width="50"
```

| Crystal system | Edges | Angles | Bravais lattices | Examples |
|---|---|---|---|---|
| Cubic | a = b = c | α = β = γ = 90° | 3 (simple, body-centred, face-centred) | NaCl, Cu, diamond, ZnS |
| Tetragonal | a = b ≠ c | α = β = γ = 90° | 2 (simple, body-centred) | white tin, SnO₂, TiO₂ |
| Orthorhombic | a ≠ b ≠ c | α = β = γ = 90° | 4 (simple, body, face, end-centred) | rhombic sulphur, KNO₃, BaSO₄ |
| Monoclinic | a ≠ b ≠ c | α = γ = 90°, β ≠ 90° | 2 (simple, end-centred) | monoclinic sulphur, Na₂SO₄·10H₂O |
| Triclinic | a ≠ b ≠ c | α ≠ β ≠ γ ≠ 90° | 1 | CuSO₄·5H₂O, K₂Cr₂O₇, H₃BO₃ |
| Hexagonal | a = b ≠ c | α = β = 90°, γ = 120° | 1 | graphite, ZnO, Mg, ice |
| Rhombohedral (trigonal) | a = b = c | α = β = γ ≠ 90° | 1 | calcite (CaCO₃), cinnabar (HgS), NaNO₃ |

3 + 2 + 4 + 2 + 1 + 1 + 1 = 14. The cubic system is the most symmetrical and the triclinic
the least.

### Counting particles in cubic unit cells

A corner particle is shared by 8 unit cells (contributes 1/8), an edge particle by 4 (1/4),
a face-centre particle by 2 (1/2), and a body-centre particle belongs wholly to its cell.

```photo id="chem11/halite-crystal" caption="A crystal of halite (rock salt, NaCl). Its cube-like faces and cleavage planes reflect the face-centred cubic arrangement of the ions inside." width="60"
```

```figure caption="The three cubic unit cells. Z is the number of atoms belonging to one cell and CN the coordination number (nearest neighbours of each atom)."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3, figsize=(5.1, 2.4))
def P(p):
    x, y, z = p
    return x + 0.42*z, y + 0.32*z
cor = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
edges = [(p, q) for i, p in enumerate(cor) for q in cor[i+1:] if sum(abs(np.array(p) - np.array(q))) == 1]
extra = [[], [(0.5, 0.5, 0.5)],
         [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5), (0.5, 1, 0.5), (0, 0.5, 0.5), (1, 0.5, 0.5)]]
names = ['simple cubic', 'body-centred cubic', 'face-centred cubic']
foot = ['Z = 8 × 1/8 = 1;  CN 6', 'Z = 1 + 1 = 2;  CN 8', 'Z = 1 + 6 × 1/2 = 4;  CN 12']
for k, ax in enumerate(axs):
    for p, q in edges:
        back = (p[2] == 1 and q[2] == 1) or (p[0] == 0 and q[0] == 0 and (p[2] + q[2]) > 0 and False)
        ax.plot([P(p)[0], P(q)[0]], [P(p)[1], P(q)[1]], color=MUTED, lw=0.9, zorder=1)
    for p in cor:
        X, Y = P(p); ax.plot([X], [Y], 'o', color=ACCENT, ms=7.5, zorder=3)
    for p in extra[k]:
        X, Y = P(p); ax.plot([X], [Y], 'o', color=SERIES[1], ms=7.5, zorder=4)
    ax.set_title(names[k], fontsize=8.6, color=INK, pad=2)
    ax.text(0.71, -0.42, foot[k], ha='center', fontsize=7.6, color=INK)
    ax.set_xlim(-0.3, 1.72); ax.set_ylim(-0.55, 1.5)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.05)
```

| Cubic cell | Atoms per cell, Z | Coordination number | Edge and radius | Packing efficiency |
|---|---|---|---|---|
| Simple (primitive) | 1 | 6 | a = 2r | 52.4 % |
| Body-centred (bcc) | 2 | 8 | √3 a = 4r | 68 % |
| Face-centred (fcc, ccp) | 4 | 12 | √2 a = 4r | 74 % |

The density of a cubic crystal follows from the unit cell:

$$ \rho = \frac{Z \times M}{a^3 \times N_A} $$

(a in cm gives ρ in g cm⁻³.) Examples: Na, K and Fe (at room temperature) are bcc; Cu, Ag,
Au and Al are fcc; NaCl has 4 formula units per cubic cell.

::: example Density of rock salt
**Problem.** NaCl has a face-centred cubic cell with edge 564 pm and 4 formula units per
cell. Find its density (NaCl = 58.5 g mol⁻¹, N_A = 6.02 × 10²³ mol⁻¹).

**Solution.** a = 5.64 × 10⁻⁸ cm, a³ = 1.794 × 10⁻²² cm³.
$\rho = \frac{4 \times 58.5}{1.794 \times 10^{-22} \times 6.02 \times 10^{23}} = \frac{234}{108} =$ **2.17 g cm⁻³** — the measured
value, which confirms the structure.
:::

### Types of crystalline solid by bonding

| Type | Particles | Forces | Properties | Examples |
|---|---|---|---|---|
| Ionic | cations and anions | electrostatic (ionic) bonds | hard, brittle, high mp; conduct only when molten or dissolved | NaCl, KNO₃, MgO, CaF₂ |
| Covalent (network) | atoms | covalent bonds throughout | very hard, very high mp, non-conductors (graphite excepted) | diamond, quartz SiO₂, SiC, graphite |
| Molecular | molecules | van der Waals forces or hydrogen bonds | soft, low mp, often volatile, insulators | I₂, dry ice (CO₂), naphthalene, ice, S₈, P₄ |
| Metallic | positive kernels in an electron sea | metallic bonds | lustrous, malleable, ductile, good conductors; mp varies | Na, Cu, Fe, Ag |

Graphite is the classic exception: a covalent solid that conducts, because each carbon
(sp²) leaves one electron delocalised over its layer; the layers are held by weak van der
Waals forces, so it is soft and slippery.

```photogrid label="6.1" cols="2" ratio="1.2" caption="Light molecules move faster. (a) A Kipp apparatus makes gas whenever the tap is opened. (b) Graham's law says rate is proportional to 1 / sqrt(M). Taking carbon dioxide (44.01 g/mol) as 1, hydrogen escapes 4.67 times faster, methane 1.66, ammonia 1.61, hydrogen sulfide 1.14 and chlorine only 0.79. The mean molecular speed sqrt(8RT / pi M) at 298 K is 1,769 m/s for H2 and 379 m/s for CO2, so the lighter gas is about 4.7 times quicker, the same factor."
@ photo id="chem11/kipp" cap="A Kipp apparatus generates gases such as H2S and CO2 on demand"
fit 1.2
focus 0.5 0.5
@ svg cap="Relative rates of effusion by Graham's law (CO2 = 1)"
gases = (("H2", 2.016), ("CH4", 16.04), ("NH3", 17.03), ("H2S", 34.08), ("CO2", 44.01), ("Cl2", 70.90))
rel = {n: math.sqrt(44.01 / M) for n, M in gases}
v = lambda M: math.sqrt(8 * 8.314 * 298 / (math.pi * M / 1000))
assert abs(rel["H2"] - 4.672) < 0.005 and abs(rel["CO2"] - 1) < 1e-12 and abs(v(2.016) / v(44.01) - rel["H2"]) < 1e-9
facts = dict(rh="%.2f" % rel["H2"], rch="%.2f" % rel["CH4"], rn="%.2f" % rel["NH3"], rs="%.2f" % rel["H2S"], rcl="%.2f" % rel["Cl2"], vh="{:,.0f}".format(v(2.016)), vc="{:,.0f}".format(v(44.01)), vr="%.1f" % (v(2.016) / v(44.01)))
f = Fig(300, 236)
f.text(150, 14, "rate relative to CO2 = sqrt(44.01 / M)", size=10.5, color=NAVY, bold=True)
for i, (n, M) in enumerate(gases):
    y = 28 + i * 26
    f.text(14, y + 14, "%s  %.2f" % (n, M), size=10.5, color=SLATE, anchor="start", vmid=True)
    w = rel[n] * 28
    col, fl = (RED, ROSE) if n == "H2" else ((AMBER, SAND) if n == "CO2" else (TEAL, MINT))
    f.box(96, y + 4, w, 14, fill=fl, stroke=col, r=2, sw=1.4)
    f.text(96 + w + 5, y + 11, "%.2f" % rel[n], size=10.5, color=col, bold=True, anchor="start", vmid=True)
f.text(150, 196, "mean speed at 298 K: H2 %s m/s" % "{:,.0f}".format(v(2.016)), size=10.5, color=NAVY, bold=True)
f.text(150, 214, "CO2 %s m/s (ratio %.2f)" % ("{:,.0f}".format(v(44.01)), v(2.016) / v(44.01)), size=10.5, color=NAVY, bold=True)
```

```photogrid label="6.2" cols="2" ratio="1.2" caption="Gas laws that fly. (a) Looking up into a balloon envelope, the air is heated by a propane burner. (b) The cell uses PV = nRT in the form density = PM / RT. At 15 degrees C and 101.3 kPa air has a density of 1.225 kg/m3; heated to 100 degrees C it is only 0.946 kg/m3, because the open mouth lets the hot gas expand until its pressure equals the outside pressure (Charles's law). The envelope of 2800 m3 then floats up with a lift of about 781 kg, enough for the fabric, basket, burners, fuel and a few passengers. Raising the inside temperature to 120 degrees C gives 916 kg, so each extra 20 degrees buys a little less lift than the one before."
@ photo id="ceechem2/balloon" cap="The inside of a hot-air balloon envelope"
fit 1.2
focus 0.5 0.5
@ svg cap="Lift of a hot-air balloon from Charles's law"
P, Mair, R, Tout = 101325.0, 0.02896, 8.314, 288.15
V = 2800.0
def rho(T):
    return P * Mair / (R * T)
rows = []
for tc in (60, 80, 100, 120):
    rows.append(("%d C" % tc, (rho(Tout) - rho(tc + 273.15)) * V))
assert round(rho(Tout), 3) == 1.225 and round(rows[2][1]) == 781
f = Fig(300, 236)
f.text(150, 12, "Lift of a 2800 m3 envelope, kg", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=max(v for _, v in rows) * 1.05, fmt="%.0f", x0=48, y0=32, bw=170, gap=30)
f.text(150, 164, "air inside at the temperature shown", size=10, color=SLATE, bold=True)
f.text(150, 192, "outside 15 C: density %.3f kg/m3" % rho(Tout), size=10.5, color=NAVY, bold=True)
f.text(150, 210, "inside 100 C: density %.3f kg/m3" % rho(373.15), size=10.5, color=NAVY, bold=True)
f.text(150, 226, "volume is fixed, so lift = (r_out - r_in) V", size=10, color=SLATE, bold=True)
facts = dict(ro=rho(Tout), ri=rho(373.15), lift=rows[2][1], l120=rows[3][1])
```

## Formula and fact sheet

| Quantity | Formula |
|---|---|
| Kinetic gas equation | $PV = \frac{1}{3}mNu_{rms}^2$ |
| Kinetic energy | (3/2)RT per mole; (3/2)kT per molecule; depends only on T |
| Molecular speeds | $u_{mp} = \sqrt{2RT/M}$, $u_{av} = \sqrt{8RT/\pi M}$, $u_{rms} = \sqrt{3RT/M}$; $u_{mp} : u_{av} : u_{rms}$ = 1 : 1.128 : 1.224 |
| Gas laws | PV = const (T); V/T = const (P); P/T = const (V); V/n = const |
| Ideal and combined | PV = nRT; ρ = PM/RT; P₁V₁/T₁ = P₂V₂/T₂ |
| R | 8.314 J mol⁻¹ K⁻¹ = 0.0821 L atm mol⁻¹ K⁻¹ = 1.987 cal mol⁻¹ K⁻¹ |
| Dalton | P = Σpᵢ; pᵢ = xᵢP; p(dry) = P − aqueous tension |
| Graham | r₁/r₂ = √(M₂/M₁) = √(ρ₂/ρ₁); t₁/t₂ = √(M₁/M₂) |
| Real gases | Z = PV/nRT; (P + an²/V²)(V − nb) = nRT; T_B = a/Rb; T_c = 8a/27Rb |
| Surface tension (drops) | γ₁/γ₂ = ρ₁n₂/(ρ₂n₁); unit N m⁻¹ |
| Viscosity (Ostwald) | η₁/η₂ = ρ₁t₁/(ρ₂t₂); unit Pa s; 1 P = 0.1 Pa s |
| Unit cell | Z = 1, 2, 4 (sc, bcc, fcc); CN 6, 8, 12; ρ = ZM/(a³N_A) |

Facts: 7 crystal systems and 14 Bravais lattices; liquid viscosity and surface tension fall
with temperature (gas viscosity rises); boiling point is where VP = external pressure
(water: about 95 °C in Kathmandu, about 70 °C on Everest); efflorescent loses water,
deliquescent dissolves in absorbed water, hygroscopic merely absorbs it.

## Chapter summary

- Kinetic theory: random elastic motion, no attractions, negligible molecular volume; KE = (3/2)RT per mole for every gas; $u_{rms} = \sqrt{3RT/M}$ and $u_{mp} : u_{av} : u_{rms} = 1 : 1.128 : 1.224$.
- Boyle, Charles, pressure and Avogadro laws combine into PV = nRT (R = 8.314 J or 0.0821 L atm mol⁻¹ K⁻¹); always use kelvin.
- Dalton: $p_i = x_iP$; Graham: rate ∝ 1/√M (lighter gases diffuse faster; time ∝ √M).
- Real gases: Z = PV/nRT; van der Waals a (attraction) and b (excluded volume); ideal behaviour at low P and high T; large a means easy liquefaction.
- Vapour pressure depends only on the liquid and T; boiling occurs when VP = external pressure. Surface tension (N m⁻¹) and liquid viscosity (Pa s) fall as T rises.
- Liquid crystals (nematic, smectic, cholesteric) flow but keep orientational order; used in LCDs and thermometers. Solubility curves show crystallisation yields; KNO₃ rises steeply, NaCl barely.
- Crystalline solids: long-range order, sharp mp, anisotropic; amorphous: short-range order, soften over a range, isotropic. Efflorescent loses water; deliquescent dissolves; hygroscopic absorbs.
- 7 crystal systems, 14 Bravais lattices; sc, bcc, fcc have Z = 1, 2, 4 and CN 6, 8, 12; ρ = ZM/(a³N_A). Solids are ionic, covalent network, molecular or metallic.

## Practice questions

**Set A — Recall (20 questions)**

1. According to the kinetic theory, the average kinetic energy of gas molecules is directly proportional to
   (a) the pressure (b) the volume (c) the absolute temperature (d) the molar mass
2. Boyle's law states that, for a fixed mass of gas at constant temperature,
   (a) PV = constant (b) V/T = constant (c) P/T = constant (d) PT = constant
3. The value of the gas constant R in L atm mol⁻¹ K⁻¹ is
   (a) 8.314 (b) 0.0821 (c) 1.987 (d) 22.4
4. Graham's law states that the rate of diffusion of a gas is
   (a) proportional to its molar mass (b) inversely proportional to its molar mass (c) proportional to the square root of its density (d) inversely proportional to the square root of its density
5. Real gases behave most nearly like an ideal gas at
   (a) low pressure and high temperature (b) high pressure and low temperature (c) high pressure and high temperature (d) low pressure and low temperature
6. In the van der Waals equation the constant a corrects for
   (a) the volume of the molecules (b) the mass of the molecules (c) the attraction between the molecules (d) the speed of the molecules
7. A liquid boils at the temperature at which
   (a) it starts to evaporate (b) its vapour pressure becomes zero (c) its vapour pressure is 1 mmHg (d) its vapour pressure equals the external pressure
8. The SI unit of surface tension is
   (a) N m (b) N m⁻¹ (c) N m⁻² (d) N s m⁻²
9. When the temperature rises, the viscosity of a liquid
   (a) decreases (b) increases (c) does not change (d) first increases, then decreases
10. A substance that absorbs moisture from the air and dissolves in it is called
   (a) efflorescent (b) hygroscopic (c) deliquescent (d) amorphous
11. Which of the following is an amorphous solid?
   (a) sodium chloride (b) glass (c) quartz (d) diamond
12. The numbers of crystal systems and of Bravais lattices are respectively
   (a) 14 and 7 (b) 7 and 7 (c) 6 and 14 (d) 7 and 14
13. The state of matter that flows like a liquid but keeps some orientational order of a crystal is
   (a) an amorphous solid (b) a plasma (c) a liquid crystal (d) a supercritical fluid
14. The number of atoms in a face-centred cubic unit cell is
   (a) 4 (b) 2 (c) 1 (d) 6
15. Crystals of washing soda lose water and crumble when exposed to air. This property is called
   (a) deliquescence (b) hygroscopy (c) sublimation (d) efflorescence
16. Dalton's law of partial pressures applies to
   (a) reacting gases only (b) mixtures of non-reacting gases (c) liquids (d) solutions of gases in water
17. Unlike amorphous solids, crystalline solids are
   (a) isotropic (b) without a sharp melting point (c) anisotropic, with a sharp melting point (d) supercooled liquids
18. The number of molecules of water of crystallisation in blue vitriol is
   (a) 5 (b) 7 (c) 10 (d) 2
19. Diamond is an example of a
   (a) molecular solid (b) ionic solid (c) metallic solid (d) covalent network solid
20. The solubility of a gas in water generally
   (a) increases with temperature (b) decreases with temperature (c) is independent of pressure (d) decreases with pressure

::: note Answers and explanations — Set A
**1.** (c) — KE = (3/2)RT per mole: it depends on the absolute temperature only, not on P, V or the kind of gas.
**2.** (a) — P ∝ 1/V at constant T, so PV is constant. V/T = constant is Charles's law; P/T = constant the pressure law.
**3.** (b) — 0.0821 L atm mol⁻¹ K⁻¹. 8.314 is in J mol⁻¹ K⁻¹ and 1.987 in cal mol⁻¹ K⁻¹; 22.4 L is the molar volume.
**4.** (d) — r ∝ 1/√ρ ∝ 1/√M. Option (b) misses the square root.
**5.** (a) — At low pressure the molecular volume is negligible, and at high temperature the attractions hardly matter.
**6.** (c) — a corrects the pressure for intermolecular attraction; b corrects the volume for the size of the molecules.
**7.** (d) — Boiling begins when bubbles of vapour can form inside the liquid, i.e. when its vapour pressure equals the pressure above it.
**8.** (b) — Force per unit length: N m⁻¹ (equivalently J m⁻²). N s m⁻² is the unit of viscosity.
**9.** (a) — Warmer molecules overcome intermolecular attraction more easily, so the liquid flows more freely. (Gas viscosity does the opposite.)
**10.** (c) — Deliquescent solids, such as CaCl₂ and NaOH, dissolve in the water they absorb; hygroscopic ones only become damp.
**11.** (b) — Glass has only short-range order and softens over a range of temperature. NaCl, quartz and diamond are crystalline.
**12.** (d) — Seven crystal systems give fourteen Bravais lattices.
**13.** (c) — The liquid crystal (mesophase) lies between the crystalline solid and the isotropic liquid.
**14.** (a) — 8 corners × 1/8 + 6 face centres × 1/2 = 1 + 3 = 4.
**15.** (d) — Efflorescence: Na₂CO₃·10H₂O gives up water of crystallisation to the air and turns powdery.
**16.** (b) — The partial pressures add only when the gases do not react with one another.
**17.** (c) — Long-range order makes crystals anisotropic and gives them a sharp melting point.
**18.** (a) — CuSO₄·5H₂O. Green and white vitriol have 7 H₂O; washing soda 10; gypsum 2.
**19.** (d) — Every carbon is covalently bonded to four others in a giant 3-D network, hence extreme hardness and a very high melting point.
**20.** (b) — Dissolving a gas releases heat, so warming drives gas out; higher pressure increases solubility (Henry's law).
:::

**Set B — Understanding (14 questions)**

1. At the same temperature, which gas has the greatest average kinetic energy per molecule?
   (a) all have the same (b) H₂ (c) O₂ (d) CO₂
2. The ratio of the most probable, average and root-mean-square speeds of gas molecules is
   (a) 1 : 1.224 : 1.128 (b) 1.224 : 1.128 : 1 (c) 1 : 1 : 1 (d) 1 : 1.128 : 1.224
3. The vapour pressure of a pure liquid depends on
   (a) the amount of liquid (b) the surface area of the liquid (c) the nature of the liquid and the temperature (d) the volume of the container
4. Water boils at a lower temperature on Mount Everest than in Kathmandu because
   (a) the air is colder there (b) the atmospheric pressure is lower there (c) the vapour pressure of water is higher there (d) the water there is purer
5. Small liquid drops are spherical because of
   (a) surface tension (b) viscosity (c) vapour pressure (d) gravity
6. Glycerol is far more viscous than water mainly because
   (a) it has a lower molar mass (b) it is an ionic compound (c) its three OH groups form extensive hydrogen bonds (d) it has a lower density
7. A real gas shows Z < 1 at moderate pressure. The main cause is
   (a) the finite volume of its molecules (b) attraction between its molecules (c) the high speed of its molecules (d) a chemical reaction between its molecules
8. Fused CaCl₂ is used in desiccators to dry substances because it is
   (a) efflorescent (b) amorphous (c) volatile (d) deliquescent
9. KNO₃ is far more soluble in hot water than in cold, while NaCl is about equally soluble in both. To recover pure KNO₃ by crystallisation one should
   (a) cool a hot saturated solution (b) evaporate at room temperature only (c) heat a cold saturated solution (d) add more water
10. Which property shows that glass is an amorphous solid?
   (a) it is transparent (b) it is hard (c) it is brittle (d) it softens over a range of temperature
11. The coordination number of an atom in a body-centred cubic lattice is
   (a) 6 (b) 12 (c) 8 (d) 4
12. Ice is a molecular solid in which the molecules are held together by
   (a) ionic bonds (b) hydrogen bonds (c) metallic bonds (d) covalent bonds between the molecules
13. Which set of parameters describes a cubic unit cell?
   (a) a = b = c; α = β = γ = 90° (b) a = b ≠ c; α = β = γ = 90° (c) a ≠ b ≠ c; α = β = γ = 90° (d) a = b ≠ c; α = β = 90°, γ = 120°
14. NH₃ and HCl gases released at the same moment at opposite ends of a long tube meet and form a white ring of NH₄Cl. The ring forms
   (a) exactly in the middle (b) nearer the NH₃ end (c) nearer the HCl end (d) at the NH₃ end itself

::: note Answers and explanations — Set B
**1.** (a) — Average KE = (3/2)kT depends only on temperature; H₂ moves fastest, but its KE per molecule is the same as that of O₂ or CO₂.
**2.** (d) — √2 : √(8/π) : √3 = 1 : 1.128 : 1.224, so u_mp < u_av < u_rms.
**3.** (c) — It is an equilibrium property, set by the intermolecular forces and the temperature; the amount and the area change only how fast equilibrium is reached.
**4.** (b) — Lower outside pressure is matched by the vapour pressure at a lower temperature (about 70 °C on the summit against about 95 °C in Kathmandu).
**5.** (a) — Surface tension pulls a free liquid into the shape of least surface area for its volume — a sphere.
**6.** (c) — Each glycerol molecule has three OH groups and is held to its neighbours by many hydrogen bonds, which resist flow.
**7.** (b) — Attractions pull the molecules together, so the gas is more compressible than ideal (PV < nRT). Molecular volume makes Z > 1.
**8.** (d) — CaCl₂ takes up water vapour so strongly that it dissolves in it; that is what makes it a good drying agent.
**9.** (a) — A large drop in solubility on cooling throws out most of the KNO₃ as crystals, while the small amount of NaCl impurity stays dissolved.
**10.** (d) — Amorphous solids have no sharp melting point; transparency, hardness and brittleness are shown by crystals too.
**11.** (c) — The body-centre atom touches the 8 corner atoms; simple cubic has CN 6 and fcc 12.
**12.** (b) — Each water molecule is hydrogen-bonded to four neighbours in a tetrahedral, open arrangement.
**13.** (a) — Cubic: all edges and all angles equal, angles 90°. (b) is tetragonal, (c) orthorhombic, (d) hexagonal.
**14.** (c) — Lighter NH₃ diffuses √(36.5/17) ≈ 1.47 times faster, so it covers more of the tube before the two meet.
:::

**Set C — Application (10 questions)**

1. A gas occupies 600 mL at 27 °C and 760 mmHg. Its volume at 127 °C and 380 mmHg is
   (a) 800 mL (b) 1600 mL (c) 1200 mL (d) 225 mL
2. The root-mean-square speed of O₂ molecules at 27 °C is about (R = 8.314 J mol⁻¹ K⁻¹)
   (a) 15.3 m s⁻¹ (b) 395 m s⁻¹ (c) 446 m s⁻¹ (d) 484 m s⁻¹
3. The rates of diffusion of H₂ and O₂ under the same conditions are in the ratio
   (a) 4 : 1 (b) 1 : 4 (c) 16 : 1 (d) 1 : 16
4. A flask contains 0.20 mol of N₂ and 0.30 mol of O₂ at a total pressure of 5.0 atm. The partial pressure of O₂ is
   (a) 2.0 atm (b) 2.5 atm (c) 3.0 atm (d) 5.0 atm
5. 50 mL of a gas X effuses through a pinhole in 20 s, while 50 mL of O₂ takes 10 s under the same conditions. The molar mass of X is
   (a) 64 g mol⁻¹ (b) 128 g mol⁻¹ (c) 16 g mol⁻¹ (d) 8 g mol⁻¹
6. A gas has a density of 1.30 g L⁻¹ at 27 °C and 1.0 atm. Its molar mass is about (R = 0.0821 L atm mol⁻¹ K⁻¹)
   (a) 28 g mol⁻¹ (b) 2.9 g mol⁻¹ (c) 44 g mol⁻¹ (d) 32 g mol⁻¹
7. A solution of KNO₃ saturated at 60 °C contains 100 g of water. The solubility of KNO₃ is 110 g at 60 °C and 31.6 g at 20 °C per 100 g of water. On cooling to 20 °C, the mass of KNO₃ that crystallises is
   (a) 78.4 g (b) 110 g (c) 31.6 g (d) 141.6 g
8. A metal of molar mass 50 g mol⁻¹ has a face-centred cubic lattice with edge length 400 pm. Its density is about (N_A = 6.02 × 10²³ mol⁻¹)
   (a) 1.30 g cm⁻³ (b) 2.60 g cm⁻³ (c) 5.19 g cm⁻³ (d) 10.4 g cm⁻³
9. Crystals of Na₂CO₃·xH₂O lose 62.9 % of their mass on heating to constant mass. The value of x is (Na₂CO₃ = 106)
   (a) 1 (b) 5 (c) 7 (d) 10
10. A stalagmometer delivers 20 drops of water (density 1.0 g mL⁻¹, surface tension 72 mN m⁻¹) and 50 drops of a liquid of density 0.80 g mL⁻¹ for the same volume. The surface tension of the liquid is
   (a) 23 mN m⁻¹ (b) 36 mN m⁻¹ (c) 144 mN m⁻¹ (d) 225 mN m⁻¹

::: note Answers and explanations — Set C
**1.** (b) — V₂ = 600 × (760/380) × (400/300) = 600 × 2 × 4/3 = 1600 mL. (a) ignores the pressure change, (c) ignores the temperature change, (d) inverts both.
**2.** (d) — u_rms = √(3 × 8.314 × 300/0.032) = 484 m s⁻¹. (a) uses M = 32 instead of 0.032 kg mol⁻¹; (b) and (c) are u_mp and u_av.
**3.** (a) — r(H₂)/r(O₂) = √(32/2) = √16 = 4. Option (c) forgets the square root.
**4.** (c) — x(O₂) = 0.30/0.50 = 0.60; p(O₂) = 0.60 × 5.0 = 3.0 atm.
**5.** (b) — t ∝ √M: (20/10)² = 4, so M = 4 × 32 = 128 g mol⁻¹. Option (a) forgets to square the time ratio.
**6.** (d) — M = ρRT/P = 1.30 × 0.0821 × 300/1.0 = 32.0 g mol⁻¹ (the gas could be O₂). Option (b) uses 27 instead of 300 K.
**7.** (a) — 110 − 31.6 = 78.4 g crystallises; 31.6 g stays in the 100 g of water.
**8.** (c) — ρ = ZM/(a³N_A) = 4 × 50/((4.00 × 10⁻⁸)³ × 6.02 × 10²³) = 200/38.5 = 5.19 g cm⁻³. (a) and (b) use Z = 1 and 2.
**9.** (d) — 18x/(106 + 18x) = 0.629 gives x = 9.98 ≈ 10: washing soda, Na₂CO₃·10H₂O.
**10.** (a) — γ = 72 × (0.80 × 20)/(1.0 × 50) = 72 × 0.32 = 23 mN m⁻¹: more, smaller drops mean lower surface tension. (c) inverts the drop ratio.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. State the gas laws, derive the ideal gas equation and explain Graham's law, Dalton's law and deviations of real gases with numericals. <span class="marks">[10]</span>
2. Describe the properties of liquids and the types of crystal lattice, and calculate packing efficiency and density of a unit cell. <span class="marks">[10]</span>

```photogrid label="6.H" cols="3" ratio="1.25" caption="States of matter. (a) A balloon filled with gas: pressure, volume and temperature are linked by the gas laws. (b) A crystal of rock salt shows the regular faces of a cubic lattice. (c) Naphthalene (mothballs) sublimes, passing directly from solid to vapour."
@ photo id="ceechem2/balloon" cap="(a) Gas in a balloon"
fit 1.25
focus 0.5 0.5
@ photo id="chem11/halite" cap="(b) Cubic crystal"
fit 1.25
focus 0.5 0.5
@ photo id="chem11/mothball" cap="(c) Sublimation of naphthalene"
fit 1.25
focus 0.5 0.5
```

### Model answer D1: gas laws, ideal gas equation and real gases (10 marks)

**Introduction.** A gas has no fixed shape or volume, and its state is given by pressure $P$, volume $V$, temperature $T$ and amount $n$.

**Gas laws.**

| Law | Statement | Expression |
|---|---|---|
| Boyle | $V \propto 1/P$ at constant $T$ | $P_1V_1 = P_2V_2$ |
| Charles | $V \propto T$ at constant $P$ | $V_1/T_1 = V_2/T_2$ |
| Gay-Lussac | $P \propto T$ at constant $V$ | $P_1/T_1 = P_2/T_2$ |
| Avogadro | $V \propto n$ at constant $T$ and $P$ | $V/n$ constant |

**Ideal gas equation.** Combining the laws gives $PV = nRT$, where $R = 0.0821\ \text{L atm K}^{-1}\text{mol}^{-1} = 8.314\ \text{J K}^{-1}\text{mol}^{-1}$. Also $PM = dRT$, so the density of a gas is $d = PM/RT$.

**Dalton's law of partial pressures.** $P_{total} = p_1 + p_2 + \cdots$ and $p_i = x_iP_{total}$.

**Graham's law of diffusion.** At constant $T$ and $P$, the rate of diffusion is inversely proportional to the square root of the density (or molar mass): $\dfrac{r_1}{r_2} = \sqrt{\dfrac{M_2}{M_1}}$.

**Kinetic theory results.** $PV = \tfrac13mN\overline{c^2}$; the average kinetic energy is $\tfrac32kT$; $u_{rms} = \sqrt{3RT/M}$, the most probable speed $\sqrt{2RT/M}$ and the average speed $\sqrt{8RT/\pi M}$, in the ratio $1 : 1.128 : 1.224$.

**Real gases.** At high pressure and low temperature, gases deviate from ideal behaviour, because the molecular volume is not negligible and the attractions are not zero. The van der Waals equation is $\left(P + \dfrac{an^2}{V^2}\right)(V - nb) = nRT$, where $a$ corrects for attraction and $b$ for volume. The compressibility factor is $Z = PV/nRT$ ($Z = 1$ for an ideal gas). Above the **critical temperature** a gas cannot be liquefied by pressure alone. The **Boyle temperature** is $T_B = a/Rb$.

**Numerical.**

- $2\ \text{g}$ of H₂ ($1\ \text{mol}$) at $27^{\circ}\text{C}$ in $10\ \text{L}$: $P = \dfrac{1\times0.0821\times300}{10} = 2.46\ \text{atm}$.
- Graham: $\dfrac{r_{H_2}}{r_{O_2}} = \sqrt{\dfrac{32}{2}} = 4$, so hydrogen diffuses four times as fast as oxygen.
- Density of CO₂ at STP $= \dfrac{1\times44}{0.0821\times273} = 1.96\ \text{g L}^{-1}$.
- $u_{rms}$ of O₂ at $300\ \text{K}$ $= \sqrt{\dfrac{3\times8.314\times300}{0.032}} = 484\ \text{m s}^{-1}$.

**Conclusion.** $PV = nRT$ describes an ideal gas, and the van der Waals equation corrects it for molecular size and attractions.

### Model answer D2: liquids and crystalline solids (10 marks)

**Introduction.** Liquids have definite volume but no definite shape, while crystalline solids have a regular, long-range arrangement of particles.

**Properties of liquids.**

1. **Vapour pressure:** the pressure of the vapour in equilibrium with the liquid. It rises with temperature, and the liquid boils when it equals the external pressure. The **Clausius-Clapeyron equation** is $\log\dfrac{p_2}{p_1} = \dfrac{\Delta H_{vap}}{2.303R}\left(\dfrac1{T_1} - \dfrac1{T_2}\right)$.
2. **Surface tension:** the force per unit length acting along the surface, which causes spherical drops and capillary rise. It decreases as the temperature rises.
3. **Viscosity:** resistance to flow, which decreases as the temperature rises for liquids.
4. **Hydrogen bonding** raises the boiling point of water ($100^{\circ}\text{C}$) above that of H₂S.

**Crystal lattices.** The **unit cell** is the smallest repeating unit. The three cubic types:

| Unit cell | Atoms per cell $Z$ | Coordination number | Packing efficiency | Relation of $a$ and $r$ |
|---|---|---|---|---|
| Simple cubic | 1 | 6 | $52.4\%$ | $a = 2r$ |
| Body-centred cubic | 2 | 8 | $68\%$ | $\sqrt3a = 4r$ |
| Face-centred cubic (ccp) | 4 | 12 | $74\%$ | $\sqrt2a = 4r$ |

Hexagonal close packing also has $74\%$ and coordination number $12$. In a close-packed structure of $N$ atoms there are $N$ octahedral voids and $2N$ tetrahedral voids.

**Density of a unit cell.** $\rho = \dfrac{ZM}{N_Aa^3}$.

**Types of solid.** Ionic (NaCl), covalent network (diamond, SiC), molecular (ice, I₂) and metallic (Cu). **Defects:** Schottky (missing ion pairs, density decreases, in NaCl) and Frenkel (an ion shifts to an interstitial site, density unchanged, in AgCl).

**Numerical.** NaCl is fcc with $Z = 4$, $M = 58.5\ \text{g mol}^{-1}$ and $a = 564\ \text{pm}$: $\rho = \dfrac{4\times58.5}{6.022\times10^{23}\times(5.64\times10^{-8})^3} = 2.17\ \text{g cm}^{-3}$. For copper (fcc) with $a = 361\ \text{pm}$, $r = \dfrac{\sqrt2\times361}{4} = 127.6\ \text{pm}$.

**Conclusion.** fcc and hcp are the most efficient packings ($74\%$), and the density of a crystal follows from $\rho = ZM/N_Aa^3$.

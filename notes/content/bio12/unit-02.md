---
subject: Biology
grade: 12
unit: 2
title: Plant Physiology
hours: 20
area: Botany
---

A plant does not move, does not hunt and does not drink. Yet a single maize plant in a Terai field pulls something like two hundred litres of water out of the soil in a season, loses almost all of it to the air, and builds its entire body out of a gas that makes up four hundredths of one per cent of that air. This unit is about how. It is the longest unit in the Botany paper — twenty of your eighty-odd Botany hours — and it is the one that rewards understanding over memorising, because almost every question is a *why* question wearing a *what* disguise.

::: key What the examiner asks from this unit
Photosynthesis and respiration together supply most of the marks. Expect one long question from the pair almost every year — the light reaction and the Z-scheme, the Calvin cycle with its stoichiometry, C3 against C4 against CAM, or the complete aerobic breakdown of glucose with a correct ATP tally. Water relations supplies the short questions: water potential and its components, ascent of sap, the mechanism of stomatal opening, transpiration versus guttation. Hormones and movements are small but certain — a four-mark comparison or a one-mark "which hormone does X". Learn the numbers. ATP counts, RQ values and hormone functions are the only places in this unit where an examiner can mark you wrong without argument.
:::

## 2.1 Water relation

Ninety per cent of a growing herbaceous plant is water. It is the solvent every reaction runs in, the reagent that photolysis splits, the pressure that holds a soft stem upright, and the vehicle that carries every mineral ion from soil to leaf. Water relations is the study of how a plant gets it, moves it and loses it.

### Diffusion, imbibition and osmosis

**Diffusion** is the net movement of particles of a gas, liquid or dissolved solute from a region of higher concentration to a region of lower concentration, down a concentration gradient, by their own kinetic energy. It needs no membrane, no energy input and no living cell. It is how carbon dioxide reaches a mesophyll cell and how oxygen leaves one. It is fast over micrometres and hopelessly slow over metres — which is exactly why plants need a transport system at all.

**Imbibition** is the adsorption of water by a hydrophilic colloid, which swells as a result. A dry gram seed dropped in water at night is three times its size by morning; the wooden handle of a *khukuri* swells and tightens in the monsoon. Two conditions must be met: there must be an **affinity** between the imbibant and the liquid, and there must be a water potential gradient between them. The force developed is the **imbibition pressure**, and it can be enormous — measured swelling pressures of wood run from about 0.4 to 4 MPa. Imbibition capacity follows the order **protein > starch > cellulose**, which is why a pea seed (protein-rich) swells more than a wheat grain (starch-rich). Imbibition is the first step in seed germination, and the heat released as water molecules bind to the colloid is the **heat of wetting**.

**Osmosis** is the net diffusion of *water* (the solvent) across a **selectively permeable membrane**, from a solution of higher water potential to one of lower water potential. Osmosis is a special case of diffusion, not a separate process. In a plant cell the plasma membrane and the tonoplast are the selectively permeable membranes; the cell wall is freely permeable and plays no part in selection.

::: caution
Do not define osmosis as "movement of water from a dilute to a concentrated solution." That is true only when both solutions are at the same pressure. The moment you press on one side — and a turgid plant cell is under several atmospheres of pressure — water can move *into* the more dilute solution. The only definition that always works is the one in terms of water potential.
:::

### Water potential and its components

The free energy of water per unit volume, compared with pure free water at the same temperature and atmospheric pressure, is the **water potential**, $\Psi_w$ (Greek letter psi). Because the reference state is pure free water, and because anything you do to water — dissolving something in it, putting it under tension, letting it wet a surface — lowers its free energy, the rule is simple:

$$\Psi_w \text{ of pure free water} = 0$$

and the water potential of any solution or any cell is **negative**. Water always moves from higher (less negative) to lower (more negative) water potential. The SI unit is the pascal; in practice we use the **megapascal (MPa)**, where 1 MPa = 10 bar = 9.87 atmospheres.

Water potential is a sum of four components:

$$\Psi_w = \Psi_s + \Psi_p + \Psi_m + \Psi_g$$

| Component | Name | Sign | What causes it |
|---|---|---|---|
| $\Psi_s$ | Solute (osmotic) potential | always $\le 0$ | dissolved solutes lowering free energy |
| $\Psi_p$ | Pressure potential | usually $> 0$ in cells, **negative in xylem** | turgor pressure, or tension |
| $\Psi_m$ | Matric potential | always $\le 0$ | water bound to walls, colloids, soil particles |
| $\Psi_g$ | Gravitational potential | $+0.01$ MPa per metre of height | the weight of the water column |

For an ordinary vacuolated cell $\Psi_m$ is small and $\Psi_g$ is ignorable below about ten metres, so the working equation you will use in problems is

$$\Psi_w = \Psi_s + \Psi_p$$

Two of these deserve a second look. **$\Psi_p$ is negative in the xylem** — the water there is under tension, being pulled from above, not pushed from below, and a negative pressure potential is the single most important idea in the ascent of sap. **$\Psi_m$ dominates in drying soil and in dry seeds**, where measured water potentials of $-50$ to $-350$ MPa are routine; that is the gradient that drives imbibition.

```figure caption="A plant cell in three bathing solutions. The outer square is the cell wall, the shaded block the protoplast. Water always moves towards the more negative water potential. Values are typical, in MPa."
fig, axes = plt.subplots(1, 3, figsize=(5.1, 2.9))
Rect = matplotlib.patches.Rectangle
heads = ["Hypotonic bath\n$\\Psi_w = -0.1$", "Isotonic bath\n$\\Psi_w = -0.8$",
         "Hypertonic bath\n$\\Psi_w = -2.0$"]
states = ["TURGID", "FLACCID", "PLASMOLYSED"]
inset = [0.03, 0.10, 0.26]
sub = [r"$\Psi_s=-0.9$,  $\Psi_p=+0.8$" + "\n" + r"net $\Psi_w=-0.1$",
       r"$\Psi_s=-0.8$,  $\Psi_p=0$" + "\n" + r"net $\Psi_w=-0.8$",
       r"$\Psi_s=-1.2$,  $\Psi_p=0$" + "\n" + r"net $\Psi_w=-1.2$"]
flow = ["water IN", "no net flow", "water OUT"]
for k, ax in enumerate(axes):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rect((0.12, 0.44), 0.76, 0.42, fill=False, ec=INK, lw=1.7))
    d = inset[k]
    ax.add_patch(Rect((0.12 + d, 0.44 + d * 0.55), 0.76 - 2 * d,
                      0.42 - 1.1 * d * 0.55, fc="#dbeaf6", ec=ACCENT, lw=1.2))
    ax.text(0.5, 0.985, heads[k], fontsize=7.2, ha="center", va="top", color=INK)
    ax.text(0.5, 0.355, states[k], fontsize=7.6, weight="600", ha="center",
            va="center", color=ACCENT if k == 0 else INK)
    ax.text(0.5, 0.255, sub[k], fontsize=6.4, ha="center", va="top", color=MUTED)
    ax.text(0.5, 0.045, flow[k], fontsize=7.0, ha="center", va="center",
            color=SERIES[1], weight="600")
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.10)
```


### Osmotic pressure, turgor and plasmolysis

The **osmotic pressure (OP)** of a solution is the pressure that must be applied to it to stop water entering it through a selectively permeable membrane. It is a positive quantity, and it is numerically equal to the solute potential with the sign reversed: $\Psi_s = -\text{OP}$. For a dilute solution it obeys the van't Hoff equation

$$\Psi_s = - i\,m\,R\,T$$

where $i$ is the van't Hoff factor (1 for sucrose or glucose, about 2 for NaCl, about 3 for CaCl$_2$), $m$ is molality in mol kg$^{-1}$ (molarity is close enough for dilute solutions), $R = 0.00831$ L MPa mol$^{-1}$ K$^{-1}$ and $T$ is absolute temperature in kelvin.

::: example Solute potential of a sucrose solution
**Calculate the solute potential of a 1.0 M sucrose solution at 25 °C.**

Sucrose does not ionise, so $i = 1$. Convert the temperature: $T = 25 + 273 = 298$ K.

$$\Psi_s = -(1)(1.0)(0.00831)(298)$$

$$\Psi_s = -2.48 \text{ MPa}$$

Because a solution open to the atmosphere has $\Psi_p = 0$, the water potential of this solution is also $-2.48$ MPa. A cell with $\Psi_w = -1.2$ MPa placed in it would lose water and plasmolyse.

*A note for the careful student:* the measured value for real 1.0 M sucrose is about $-2.7$ MPa, because a concentrated sucrose solution is not ideal. Quote $-2.48$ MPa as the van't Hoff answer and $-2.7$ MPa as the measured one — never present the measured figure as the result of the calculation.
:::

When a cell is put in a hypertonic solution it loses water, the protoplast shrinks and pulls away from the wall, and the cell is **plasmolysed**. The stage at which the protoplast has *just* begun to pull away — when the wall is exerting no pressure at all, so $\Psi_p = 0$ — is **incipient plasmolysis**, and at that moment $\Psi_w = \Psi_s$. Operationally it is taken as the external concentration at which half the cells in a peeled onion epidermis show visible plasmolysis; a 0.6 M sucrose solution is the standard. Returning the cell to water reverses the process — **deplasmolysis**. Plasmolysis proves that the protoplast is alive and that the membrane is selectively permeable, and it is the only simple way to estimate a cell's solute potential.

::: note What happened to DPD?
Older Nepali and Indian textbooks work in **diffusion pressure deficit (DPD)**, where DPD = OP − TP. The term was coined by B. S. Meyer in 1938 and it was superseded by Slatyer and Taylor in 1960. The mapping is exact: **$\Psi_w = -\text{DPD}$, $\Psi_s = -\text{OP}$, $\Psi_p = +\text{TP}$**. DPD was abandoned because it has no matric term, no gravitational term, an inverted sign convention, and because "diffusion pressure" is not a real pressure. If a question is set in DPD, convert, solve in $\Psi$, and convert back.
:::

### Absorption of water by roots

Water enters through the **root hair zone** and, less obviously, along the whole length of the young root. A root hair is a tubular extension of a single epiblema cell, with a thin cellulose wall, no cuticle, and a large vacuole whose sap has a water potential more negative than that of the soil solution. Soil at field capacity sits at about $-0.015$ MPa; a root hair at perhaps $-0.6$ MPa; water flows inward.

From the epiblema water crosses the cortex to the xylem by three pathways running in parallel:

- **Apoplast pathway** — through the interconnected cell walls and intercellular spaces, never crossing a membrane. Fastest, and the main route in a rapidly transpiring plant.
- **Symplast pathway** — from cytoplasm to cytoplasm through **plasmodesmata**, crossing the plasma membrane once at the start.
- **Transmembrane pathway** — in and out of each cell in turn across both membranes, through water channels called **aquaporins**.

At the endodermis the apoplast route is blocked. The **Casparian strip** — a band of **lignin** (with suberin deposited later) in the radial and transverse walls of every endodermal cell — forces water and dissolved ions to cross at least one plasma membrane before they can reach the stele. That single checkpoint gives the root its selectivity, stops solutes leaking back out, and makes root pressure possible.

**Aquaporins** are integral membrane proteins forming water-selective pores; Peter Agre received the 2003 Nobel Prize in Chemistry for discovering them, and the first plant aquaporin was identified in *Arabidopsis* in 1993. They are **channels, not pumps** — they let water move faster down a gradient, but they cannot move it against one.

Absorption is classified as **passive** or **active**. In passive absorption, which accounts for the overwhelming majority of uptake in a transpiring plant, the pull originates in the leaves and the root is a passive absorbing surface. In "active" absorption the root itself generates the driving force by pumping ions into the xylem, lowering its water potential, so water follows osmotically.

::: caution
"Active absorption of water" does not mean water is pumped. There is no water pump in any plant. What is active is the **transport of ions**; water always follows its own potential gradient. The commonly quoted "96 % passive, 4 % active" split is a teaching heuristic, not a measurement.
:::

### Root pressure

If you cut the stem of a well-watered tomato or *Colocasia* plant near the ground early in the morning, sap wells up from the stump. Attach a manometer and you can measure the positive hydrostatic pressure developing in the root xylem: **root pressure**. Stephen Hales measured it first, in a grapevine, in *Vegetable Staticks* (1727), obtaining about 0.14 MPa.

Root pressure is osmotic in origin. Endodermal cells actively secrete ions into the xylem; the Casparian strip prevents them leaking back; the xylem sap becomes more concentrated than the surrounding cortical cells; water enters osmotically and, having nowhere else to go, pushes upward. Typical values are **0.1–0.2 MPa**, and a survey of 109 species found a maximum of only 0.148 MPa.

Root pressure **cannot** explain the ascent of sap, for four reasons that are worth learning as a set:

1. It is far too small — 0.1 MPa would lift water about ten metres, against the thirty or more that a tall tree needs.
2. It is greatest at night and in humid weather, and falls to zero or goes negative at midday, exactly when the plant is moving the most water.
3. It is absent in many gymnosperms; detopped pine and spruce trunks do not exude at all.
4. Ascent continues perfectly well in stems whose living cells have been killed by poison or heat.

Its real function, in modern physiology, is to **refill xylem vessels that have become air-locked (embolised)** overnight, and to drive guttation.

### Ascent of sap

Water has to climb from root to leaf. In the 115 m *Sequoia sempervirens* "Hyperion", the tallest tree measured, that is a gravitational cost alone of about 1.15 MPa, plus another 2 MPa or so to overcome friction in the conduits. Three classes of theory have been offered.

**Vital force theories** hold that living cells of the stem pump the water up. Godlewski's relay-pump theory (1884) proposed that xylem parenchyma and medullary ray cells pump in relay; J. C. Bose (1923) proposed that the innermost cortical cells pulsate rhythmically. Both are dead, killed by **Strasburger's experiment (1891–93)**: twenty-metre oak trunks were stood in picric acid, copper sulphate and boiling water. The poison rose to the leaves, killing every living cell on the way, and the ascent of sap continued. A quantitative objection finishes Bose's version — sap would have to pass through 230 to 400 pulsating cells every second, against a pulse period Bose himself gave as about fourteen seconds.

**Physical force theories** that rely on capillarity also fail, and the arithmetic is worth doing. Capillary rise is $h = 2\gamma\cos\theta / \rho g r$. With $\gamma = 72.8$ mN m$^{-1}$, a xylem vessel of radius 25 µm gives $h \approx 0.6$ m; a wide vessel of radius 200 µm gives just 7 cm. Worse, the theory predicts that the tallest trees should have the narrowest vessels, whereas conduit diameter actually *increases* towards the base of a tall trunk.

**The cohesion–tension theory** of **Dixon and Joly** (preliminary note 1894; full paper, *Philosophical Transactions of the Royal Society B*, 1895), proposed independently by Askenasy in the same year, is the accepted explanation. It rests on three pillars:

- **Transpiration pull.** Water evaporates from the menisci held in nanometre-scale pores in the mesophyll cell walls — pores of radius 5–10 nm, not from the open cell surfaces. The Laplace relation $\Delta P \approx 2\gamma/r$ shows that such menisci can generate tensions of the order of $-30$ MPa, far more than any tree requires. The energy comes entirely from the sun as latent heat of vaporisation (2260 kJ per litre); no metabolic energy is spent.
- **Cohesion.** Hydrogen bonding between water molecules gives liquid water a tensile strength that has been measured at better than $-25$ MPa in spinning Z-tubes, so the column does not snap.
- **Adhesion.** Hydrogen bonding between water and the lignocellulose of the vessel wall keeps the column attached and prevents it pulling away.

The result is a continuous, cohesive, tense water column — the **transpiration–cohesion–tension mechanism** — running unbroken from the soil solution to the evaporating surface of the leaf, with the xylem sap under a negative pressure potential of typically $-0.5$ to $-3.0$ MPa at midday. Direct measurement by the pressure chamber and by the centrifuge confirmed sustained negative pressures in 1995, and the xylem-pressure-probe controversy of the 1990s was resolved when it was shown that inserting the probe itself nucleates cavitation.

```figure caption="The soil–plant–atmosphere continuum. Water moves down a continuous water-potential gradient; note the broken scale — the step into unsaturated air is enormous, and it is what does the pulling."
fig, ax = plt.subplots(figsize=(5.0, 3.0))
names = ["Soil\n(field capacity)", "Root hair", "Root xylem", "Trunk xylem",
         "Leaf mesophyll", "Outside air\n(50% RH)"]
vals = [-0.015, -0.3, -0.6, -1.2, -2.0, -93.5]
y = np.arange(len(names))[::-1]
cols = [SERIES[2]] + [ACCENT] * 4 + [SERIES[1]]
ax.barh(y, vals, color=cols, height=0.56)
ax.set_xscale("symlog", linthresh=1.0)
ax.set_xlim(-700, 2)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=6.8)
ax.set_xlabel("water potential  $\\Psi_w$  (MPa, symlog scale)", fontsize=7.4)
ax.axvline(0, color=INK, lw=0.9)
for yy, v in zip(y, vals):
    ax.text(v * 1.18, yy, f"{v:g}", fontsize=6.4, va="center", ha="right", color=INK)
ax.tick_params(axis="x", labelsize=6.6)
ax.grid(axis="x", color=GRID, lw=0.6)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
```

### Transpiration

**Transpiration** is the loss of water in the form of vapour from the aerial parts of a plant. Between 97 and 99.5 per cent of all the water a plant absorbs is lost this way. It comes in three kinds:

| Type | Site | Share of total |
|---|---|---|
| **Stomatal** | through stomata | 80–90 % |
| **Cuticular** | directly through the cuticle | 5–10 % (up to 20–30 % in thin-cuticled mesophytes) |
| **Lenticular** | through lenticels of woody stems | about 0.1 % |

The remarkable fact about stomatal transpiration is that stomata occupy only 0.5 to 3 per cent of the leaf surface yet carry almost all the water loss — because diffusion through many small pores is nearly as fast as through one large opening of the same total area.

Transpiration has real benefits: it drives the ascent of sap and with it the bulk movement of mineral ions, and the latent heat carried off cools the leaf by a useful 2–5 °C on a hot Terai afternoon. It also costs the plant enormously — roughly 400 molecules of water are lost for every molecule of CO$_2$ fixed in a C3 plant. Curtis called it a **"necessary evil"** in 1926, and the phrase has stuck, but the modern framing is better: transpiration is not a process the plant performs, it is the unavoidable price of opening the stomata to let carbon dioxide in.

The **transpiration ratio** — grams of water transpired per gram of dry matter produced — is about 500 for C3 plants, 250 for C4 plants and 50 for CAM plants (figures vary between textbook editions; quote them as approximations).

### The mechanism of stomatal movement

A stoma is a pore bounded by two **guard cells**. Unlike ordinary epidermal cells, guard cells contain chloroplasts and have walls of uneven thickness and, crucially, **circumferentially arranged cellulose microfibrils** — the property called **radial micellation**. Because the microfibrils hoop the cell, turgor cannot make the cell fatter; it can only make it longer. The two guard cells are attached to each other at their ends, so as they lengthen they bow apart, and the pore opens.

```photo id="bio12/stomata" caption="Lower epidermis of a leaf peeled and mounted, seen in the light microscope. Two open stomata sit among ordinary epidermal cells whose walls are wavy like jigsaw pieces." width="94"
crop 0.00 0.28 0.78 1.00
mark 0.115 0.760 "1"
mark 0.385 0.375 "2"
mark 0.450 0.500 "3"
mark 0.795 0.200 "4"
key 1 Ordinary epidermal cell — wavy walls, large vacuole, no chloroplasts
key 2 Guard cell — kidney-shaped, one of a pair, with a thicker inner wall
key 3 Stomatal pore (aperture) — the gap between the two guard cells
key 4 Chloroplasts inside the guard cell; ordinary epidermal cells have none
```

Opening is driven by **potassium influx**. The accepted sequence is:

1. Blue light is absorbed by **phototropin** receptors in the guard-cell plasma membrane.
2. This activates the plasma-membrane **H$^+$-ATPase**, which pumps protons out and hyperpolarises the membrane to around $-150$ mV.
3. The negative interior opens **inward-rectifying K$^+$ channels**, and K$^+$ floods in — guard-cell potassium rises from about 100 mM to 400–800 mM.
4. Charge is balanced by Cl$^-$ and NO$_3^-$ taken up from outside, and by **malate** synthesised inside the guard cell by PEP carboxylase from carbon skeletons released by starch breakdown.
5. The solute potential of the guard cell falls by 0.4–0.8 MPa, water enters osmotically, turgor rises, and radial micellation converts that turgor into opening.

Closing is driven by **abscisic acid**. Water stress raises ABA, ABA binds its receptors, an anion channel opens, the membrane depolarises, an outward K$^+$ channel opens, solutes leak out, water follows and the pore shuts.

::: caution
Many textbooks still teach the **starch–sugar interconversion theory** (Sayre's pH mechanism) as *the* mechanism of stomatal movement. It is history, not current science. It is too slow, the pH changes are too small, and the soluble sugars never rise enough to account for the osmotic change. The decisive counterexample is **onion (*Allium cepa*)**: its guard cells contain **no starch at all**, yet they open and close perfectly normally, using KCl as the osmoticum. Starch's real role is to supply the carbon skeletons for **malate**, the counter-ion for K$^+$. Write about K$^+$ fluxes.
:::

::: caution
"Monocots have dumb-bell shaped guard cells" is wrong. **Dumb-bell guard cells are a feature of the grass family (Poaceae)**, and of some sedges — maize, rice, wheat, bamboo. Non-grass monocots such as onion, *Tradescantia*, lilies and orchids have ordinary kidney-shaped guard cells. Grass stomata open and close faster because of their geometry and because they work as an ionic see-saw with a pair of **subsidiary cells**.
:::

### Factors affecting transpiration

**External factors.** Light opens stomata and so raises transpiration. **Temperature** raises it steeply, because it raises the saturation vapour pressure of the air inside the leaf. **Atmospheric humidity** lowers it. **Wind** is biphasic — a breeze thins the boundary layer of still, humid air over the leaf and raises transpiration, but a strong wind eventually causes stomatal closure and the rate falls again. **Soil water** availability is the ultimate limit.

::: note Relative humidity is the wrong variable
The driving force for evaporation is the **vapour pressure deficit (VPD)**, not relative humidity. At 50 % RH the VPD is 0.61 kPa at 10 °C but 3.69 kPa at 40 °C — a six-fold difference at identical relative humidity. That is why a plant wilts on a hot dry Terai afternoon and not on a cool humid Kathmandu morning at the same RH reading.
:::

**Internal factors.** Total leaf area; thickness of the cuticle and the wax layer; **trichomes**, which trap a humid boundary layer; **sunken stomata** buried in pits, as in *Nerium*; leaf rolling by **bulliform cells** in grasses; stomatal frequency, typically 100–1000 per mm$^2$; and the distribution of stomata — most leaves are **hypostomatous** (stomata on the lower surface only), grasses are **amphistomatous**, and the floating leaf of *Nymphaea* is **epistomatous**, with stomata only on top.

**Antitranspirants** are substances applied to reduce transpiration: stomatal-closing types such as phenylmercuric acetate and ABA; film-forming types such as wax emulsions and pinolene; and reflectants such as kaolin. All share the same limitation — CO$_2$ and H$_2$O share the same pore, so cutting water loss cuts photosynthesis roughly in proportion, and the leaf runs hotter.

### Guttation

**Guttation** is the exudation of liquid water — not vapour — from the margins and tips of intact leaves, through specialised pores called **hydathodes**. The word is from the Latin *gutta*, a drop, and was coined by Burgerstein in 1887.

A hydathode is a modified region at a vein ending. Working outward: the tracheids of the vein end blindly in a mass of loosely packed, chlorophyll-poor parenchyma called the **epithem**, which is enclosed by a sheath and opens to the outside through one or more **water pores**. A water pore is a **modified stoma — larger than an ordinary stoma and permanently open, having lost the power of movement**.

Guttation happens when **root pressure is high and transpiration is low**: at night and in the early morning, in moist soil and humid air. The classic demonstration plant is *Colocasia esculenta* (**pidalu**, taro), which can exude 5 to 300 mL from a single leaf in one night; grasses, tomato, strawberry, *Tropaeolum* and *Fuchsia* do it too. Most conifers do not.

```photo id="bio12/guttation" caption="Guttation drops standing along the margin of a crucifer leaf at dawn. Each drop marks a hydathode at a vein ending — the drops are evenly spaced because the vein endings are." width="96"
crop 0.08 0.28 1.00 1.00
mark 0.565 0.288 "1"
mark 0.424 0.382 "2"
mark 0.886 0.632 "3"
mark 0.652 0.611 "4"
key 1 A guttation drop — liquid xylem sap forced out by root pressure
key 2 The leaf margin, where the hydathodes and their water pores open
key 3 The drops continue to the leaf tip, one to each vein ending
key 4 The lamina itself stays dry — this is not condensation from the air
```

| | Guttation | Dew |
|---|---|---|
| Origin of the water | internal — xylem sap | external — atmospheric vapour |
| Driving force | root pressure | cooling of the surface below dew point |
| Exit site | hydathodes at margins and tips | anywhere, including stones and metal |
| Composition | dilute solution of salts, sugars, amino acids | essentially pure water |
| Residue on drying | a white crust | none |

Distinguish both from **bleeding**, which is the exudation of sap from a *cut* or injured surface — the flow from a tapped *Borassus* inflorescence or a pruned grapevine.

## 2.2 Photosynthesis

Photosynthesis is the process by which green plants use light energy to reduce carbon dioxide to carbohydrate, with water as the electron donor and oxygen as a by-product. It is the only significant entry point of energy into the biosphere, and every gram of food in every kitchen in Nepal traces back to it.

The overall equation is written best as

6 CO₂ + 12 H₂O  →  C₆H₁₂O₆ + 6 O₂ + 6 H₂O   (in light, in the presence of chlorophyll)

Twelve water molecules appear on the left, not six, because **all of the oxygen released comes from water, not from carbon dioxide**. Van Niel predicted this from the chemistry of photosynthetic bacteria, and Ruben, Randall, Kamen and Hyde proved it in 1941 by supplying *Chlorella* with water labelled with the heavy isotope $^{18}$O and recovering the label in the oxygen gas.

### The site: the chloroplast

The chloroplast is a double-membrane-bounded plastid. Inside the inner membrane is the **stroma**, a protein-rich matrix containing the enzymes of carbon fixation, circular DNA, 70S ribosomes and starch grains. Suspended in the stroma is a third, quite separate membrane system: flattened sacs called **thylakoids**, stacked into piles called **grana** (singular *granum*) and connected between stacks by **stroma lamellae** (intergranal thylakoids). The space enclosed by the thylakoid membrane is the **lumen**.

That three-compartment design is the whole point. The pigments and electron carriers sit in the thylakoid membrane; protons are pumped into the lumen; the enzymes that use the products sit in the stroma. Remember the rule: **light reaction in the thylakoid, dark reaction in the stroma.**

The **photosynthetic pigments** fall into three groups. **Chlorophyll *a*** (blue-green, $\text{C}_{55}\text{H}_{72}\text{O}_5\text{N}_4\text{Mg}$) is the only pigment that can convert light into chemical energy; it is the **primary or reaction-centre pigment**. **Chlorophyll *b***, the **carotenes** (orange) and the **xanthophylls** (yellow) are **accessory pigments**: they absorb wavelengths chlorophyll *a* misses and transfer the energy to it, and carotenoids additionally protect the reaction centre from photo-oxidation. Chlorophyll absorbs strongly in the blue and the red and reflects green, which is why leaves are green.

### The light reaction

Light energy is absorbed by two pigment assemblies, each an antenna of a few hundred pigment molecules funnelling energy into a single special pair of chlorophyll *a* molecules:

- **Photosystem II (PS II)**, reaction centre **P680** — named for its absorption maximum at 680 nm. Found mostly in the grana.
- **Photosystem I (PS I)**, reaction centre **P700** — absorption maximum 700 nm. Found mostly in the stroma lamellae and at granal margins.

::: caution
P680 and P700 are both **chlorophyll *a***. The numbers are wavelengths in nanometres, not molecular differences. And despite its name, PS II acts *first* in the chain — it was simply discovered second.
:::

**Non-cyclic photophosphorylation** is the main pathway. Electrons travel one way, from water to NADP$^+$, through the famous **Z-scheme**:

```figure caption="The Z-scheme. Vertical axis is redox potential: the two light absorptions are the two upward jumps, and everything else runs downhill. Water is the electron source, NADP+ the sink."
fig, ax = plt.subplots(figsize=(5.1, 3.6))
pts = [(0.06, 0.82, "H$_2$O"), (0.16, 0.82, "P680"), (0.16, -0.80, "P680*"),
       (0.28, -0.14, "Q$_A$"), (0.40, 0.10, "PQ"), (0.50, 0.37, "cyt $b_6f$"),
       (0.60, 0.45, "P700"), (0.60, -1.30, "P700*"), (0.75, -0.42, "Fd"),
       (0.90, -0.32, "NADP$^+$")]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
path = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for a, b in zip(path[:-1], path[1:]):
    col = SERIES[3] if (a, b) in ((1, 2), (6, 7)) else MUTED
    ax.annotate("", xy=(xs[b], ys[b]), xytext=(xs[a], ys[a]),
                arrowprops=dict(arrowstyle="-|>", color=col,
                                lw=1.7 if col == SERIES[3] else 1.1,
                                shrinkA=9, shrinkB=9))
for x, y, lab in pts:
    ax.text(x, y, lab, fontsize=6.9, ha="center", va="center", color=INK,
            bbox=dict(fc="white", ec=GRID, lw=0.6, boxstyle="round,pad=0.24"))
ax.annotate("light\n(680 nm)", xy=(0.135, 0.0), fontsize=6.6, color=SERIES[3],
            ha="right", va="center", weight="600")
ax.annotate("light\n(700 nm)", xy=(0.578, -0.45), fontsize=6.6, color=SERIES[3],
            ha="right", va="center", weight="600")
ax.text(0.06, 0.60, "O$_2$ released\nhere", fontsize=6.3, color=SERIES[1], ha="center")
ax.text(0.90, -0.13, "NADPH", fontsize=6.7, color=SERIES[2], ha="center", weight="600")
ax.text(0.34, 0.74, "ATP is made here, as H$^+$\ncross cyt $b_6f$ into the lumen", fontsize=6.3,
        color=SERIES[2], ha="center")
ax.set_ylim(1.15, -1.65)
ax.set_xlim(-0.01, 1.0)
ax.set_ylabel("redox potential (volts)", fontsize=7.2)
ax.set_yticks([0.8, 0.4, 0.0, -0.4, -0.8, -1.2])
ax.tick_params(axis="y", labelsize=6.6)
ax.set_xticks([])
ax.grid(axis="y", color=GRID, lw=0.6)
ax.set_axisbelow(True)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
```

Trace it in words. Light strikes PS II; P680 is excited to P680\* and loses an electron to **pheophytin**. The electron passes to plastoquinone ($\text{Q}_A$, $\text{Q}_B$, then the PQ pool), to the **cytochrome $b_6f$ complex**, to the copper protein **plastocyanin**, and so to PS I. Meanwhile P680$^+$ — the strongest oxidising agent known in biology, at about $+1.2$ V — is so electron-hungry that it can tear electrons out of water. Light then excites P700 to P700\*, which passes its electron through $\text{A}_0$, phylloquinone and a chain of iron–sulphur centres to **ferredoxin**, and finally the enzyme **ferredoxin–NADP$^+$ reductase (FNR)** uses it to reduce NADP$^+$ to NADPH.

**Photolysis of water** happens at the **oxygen-evolving complex**, a cluster of four manganese, one calcium and five oxygen atoms ($\text{Mn}_4\text{CaO}_5$) on the lumen side of PS II, which also needs chloride:

$$2\,\text{H}_2\text{O} \longrightarrow \text{O}_2 + 4\,\text{H}^+ + 4\,e^-$$

::: caution
The oxygen-evolving complex faces the **lumen**. All four protons from photolysis are released **into the lumen**, where they add to the proton gradient. Textbooks that say photolysis releases protons into the stroma have the geometry backwards — and have thrown away half the explanation of how ATP is made.
:::

The protons accumulating in the lumen — four per two water molecules from photolysis, plus four more pumped across by the cytochrome $b_6f$ complex — create a proton gradient. They escape through **ATP synthase**, whose stalk projects into the stroma, and their passage drives the phosphorylation of ADP. This is **chemiosmosis**, and because the phosphorylation is ultimately driven by light it is called **photophosphorylation**.

**Cyclic photophosphorylation** uses PS I alone. The electron from ferredoxin, instead of going to NADP$^+$, is fed back into the plastoquinone pool and returns to P700 through cytochrome $b_6f$. Protons are still pumped, so **ATP is made — but no NADPH, and no oxygen**, because water is never split.

| | Non-cyclic | Cyclic |
|---|---|---|
| Photosystems | PS II and PS I | PS I only |
| Electron path | open — water to NADP$^+$ | closed loop |
| Electron donor | water | the electron returns; none needed |
| Products | ATP + NADPH + O$_2$ | ATP only |
| Photolysis | yes | no |
| Main location | grana thylakoids | stroma lamellae |

Why keep both? Because the Calvin cycle needs ATP and NADPH in a ratio of exactly **3 : 2 (= 1.50)**, while linear electron flow delivers them at about **1.28**. Cyclic flow makes up the ATP shortfall. This is the answer to "what is the significance of cyclic photophosphorylation," and it is worth more than the usual vague line about "extra ATP".

### The dark reaction: the Calvin cycle

The **dark reaction** is light-independent, not nocturnal. It is a cycle of enzyme-catalysed reactions in the **stroma**, worked out by Melvin Calvin, Andrew Benson and James Bassham using $^{14}$C and paper chromatography; Calvin received the 1961 Nobel Prize in Chemistry. Because the first stable product is a **three-carbon** acid, plants using it alone are called **C3 plants**.

```figure caption="The Calvin cycle. Three turns fix three CO2 and release one triose phosphate; six turns give one hexose. Follow the arrows clockwise."
fig, ax = plt.subplots(figsize=(4.9, 3.6))
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(np.cos(th), np.sin(th), color=GRID, lw=12, solid_capstyle="round", zorder=1)
nodes = [(90, "RuBP\n(5C) x 3"), (330, "3-PGA\n(3C) x 6"), (210, "G3P\n(3C) x 6")]
for ang, lab in nodes:
    a = np.radians(ang)
    ax.text(np.cos(a), np.sin(a), lab, fontsize=7.0, ha="center", va="center",
            color=INK, zorder=4,
            bbox=dict(fc="white", ec=ACCENT, lw=1.3, boxstyle="round,pad=0.32"))
for ang in (30, 270, 150):
    a = np.radians(ang)
    ax.annotate("", xy=(np.cos(a - 0.20), np.sin(a - 0.20)),
                xytext=(np.cos(a + 0.20), np.sin(a + 0.20)),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.6), zorder=5)
ax.text(0, 1.70, "1. CARBOXYLATION", fontsize=6.9, weight="600", color=SERIES[1], ha="center")
ax.text(0, 1.50, "3 CO$_2$, fixed by RuBisCO", fontsize=6.6, color=INK, ha="center")
ax.text(1.32, -0.02, "2. REDUCTION", fontsize=6.9, weight="600", color=SERIES[1], ha="left")
ax.text(1.32, -0.22, "6 ATP + 6 NADPH", fontsize=6.6, color=INK, ha="left")
ax.text(-1.32, -0.02, "3. REGENERATION", fontsize=6.9, weight="600", color=SERIES[1], ha="right")
ax.text(-1.32, -0.22, "3 ATP", fontsize=6.6, color=INK, ha="right")
ax.annotate("", xy=(-0.87, -1.12), xytext=(-0.87, -0.70),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[2], lw=1.7))
ax.text(-0.87, -1.24, "1 G3P leaves the cycle\nto build sugar", fontsize=6.5,
        color=SERIES[2], ha="center", va="top", weight="600")
ax.set_xlim(-2.30, 2.30); ax.set_ylim(-1.66, 1.88)
ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
```

The cycle has three phases.

**1. Carboxylation.** The five-carbon acceptor **ribulose-1,5-bisphosphate (RuBP)** combines with CO$_2$, catalysed by **ribulose bisphosphate carboxylase-oxygenase (RuBisCO)**. The unstable six-carbon intermediate splits at once into **two molecules of 3-phosphoglyceric acid (3-PGA)** — the first stable product. RuBisCO is a sixteen-subunit enzyme ($\text{L}_8\text{S}_8$), the most abundant protein on Earth, and remarkably slow, turning over only 3 to 10 molecules of CO$_2$ per second. A plant compensates by making colossal quantities of it.

**2. Reduction.** Each 3-PGA is phosphorylated by ATP to 1,3-bisphosphoglycerate, then reduced by NADPH to **glyceraldehyde-3-phosphate (G3P)**, a triose phosphate. This is the only reduction step and the only place NADPH is used.

**3. Regeneration.** Most of the G3P is reshuffled through a series of 4-, 5-, 6- and 7-carbon sugar phosphates to rebuild RuBP, a step that costs one more ATP each (at phosphoribulokinase).

::: example The stoichiometry of the Calvin cycle
**How many ATP and NADPH are needed to make one molecule of glucose?**

Fixing one CO$_2$ gives two 3-PGA. Each 3-PGA costs **1 ATP** (phosphoglycerate kinase) and **1 NADPH** (G3P dehydrogenase). So per CO$_2$ the reduction phase costs 2 ATP and 2 NADPH. Regeneration costs a further 1 ATP per CO$_2$.

**Per CO$_2$: 3 ATP + 2 NADPH.**

Glucose has six carbons, so six turns are needed:

$$6 \times 3 = 18 \text{ ATP} \qquad 6 \times 2 = 12 \text{ NADPH}$$

**6 CO$_2$ + 18 ATP + 12 NADPH → 1 glucose.** Twelve G3P are produced in those six turns; two leave the cycle to build the hexose and ten are recycled to regenerate the six RuBP. Note the ATP : NADPH ratio of 18 : 12 = **3 : 2**.
:::

### Photorespiration

RuBisCO's second name — *oxygenase* — is its weakness. The active site cannot fully discriminate between CO$_2$ and O$_2$, and in ordinary air, where oxygen is some 500 times more abundant than carbon dioxide, RuBP is sometimes oxygenated instead of carboxylated. The products are one 3-PGA and one molecule of **2-phosphoglycolate**, which is useless. Salvaging it consumes ATP and runs a loop through three organelles — chloroplast, **peroxisome** (where glycolate oxidase makes hydrogen peroxide, destroyed by catalase) and **mitochondrion** (where two glycines condense to serine, releasing CO$_2$ and ammonia).

The cost: **one CO$_2$ is lost for every two oxygenation events**, about a quarter of the carbon that enters the pathway. Photorespiration consumes O$_2$ and releases CO$_2$ in the light, with no ATP gain — hence the name. It gets worse as temperature rises and as stomata close, because closed stomata let internal CO$_2$ fall and internal O$_2$ rise.

### C4 plants and the Hatch–Slack pathway

Some tropical grasses solve the RuBisCO problem by **concentrating CO$_2$** around the enzyme. Hatch and Slack described the pathway in sugarcane in 1966.

C4 leaves have **Kranz anatomy** (German *Kranz*, a wreath): the vascular bundles are surrounded by a ring of large, thick-walled **bundle-sheath cells** packed with chloroplasts, and outside that a ring of mesophyll cells.

```figure caption="C4 photosynthesis separates the two carboxylations in SPACE. PEP carboxylase pumps carbon into the bundle sheath, where RuBisCO works in CO2-rich air."
fig, ax = plt.subplots(figsize=(5.1, 3.1))
Rect = matplotlib.patches.Rectangle
ax.add_patch(Rect((0.03, 0.10), 0.42, 0.80, fc="#eaf3fb", ec=ACCENT, lw=1.3))
ax.add_patch(Rect((0.55, 0.10), 0.42, 0.80, fc="#eef7ee", ec=SERIES[2], lw=1.3))
ax.text(0.24, 0.955, "MESOPHYLL CELL", fontsize=7.2, weight="600", color=ACCENT, ha="center")
ax.text(0.76, 0.955, "BUNDLE-SHEATH CELL", fontsize=7.2, weight="600", color=SERIES[2], ha="center")
ax.text(0.24, 0.80, "atmospheric CO$_2$\n(as HCO$_3^-$)", fontsize=6.6, ha="center", color=INK)
ax.annotate("", xy=(0.24, 0.63), xytext=(0.24, 0.735),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3))
ax.text(0.24, 0.575, "PEP (3C)  +  CO$_2$", fontsize=6.8, ha="center", color=INK)
ax.text(0.24, 0.485, "PEP carboxylase", fontsize=6.3, ha="center",
        color=SERIES[1], style="italic")
ax.annotate("", xy=(0.24, 0.36), xytext=(0.24, 0.445),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3))
ax.text(0.24, 0.305, "OXALOACETATE (4C)", fontsize=6.9, ha="center",
        color=INK, weight="600")
ax.annotate("", xy=(0.24, 0.185), xytext=(0.24, 0.265),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3))
ax.text(0.24, 0.150, "MALATE (4C)", fontsize=6.9, ha="center", color=INK)
ax.annotate("", xy=(0.545, 0.22), xytext=(0.455, 0.16),
            arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.8))
ax.text(0.50, 0.075, "malate in", fontsize=6.3, ha="center", color=SERIES[1])
ax.text(0.76, 0.27, "malate  →  CO$_2$  +  pyruvate (3C)", fontsize=6.6,
        ha="center", color=INK)
ax.annotate("", xy=(0.76, 0.46), xytext=(0.76, 0.335),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3))
ax.text(0.76, 0.545, "CO$_2$ now 10–20x\natmospheric", fontsize=6.6, ha="center",
        color=SERIES[2], weight="600")
ax.text(0.76, 0.735, "RuBisCO +\nCALVIN CYCLE", fontsize=7.3, ha="center",
        color=INK, weight="600",
        bbox=dict(fc="white", ec=SERIES[2], lw=1.1, boxstyle="round,pad=0.3"))
ax.annotate("", xy=(0.455, 0.520), xytext=(0.545, 0.420),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.5))
ax.text(0.50, 0.578, "pyruvate", fontsize=6.1, ha="center", color=MUTED)
ax.text(0.24, 0.040, "regenerating PEP costs 2 ATP", fontsize=6.2,
        ha="center", color=MUTED, style="italic")
ax.set_xlim(0, 1); ax.set_ylim(0.02, 1.02); ax.axis("off")
fig.tight_layout()
```

The sequence: in the **mesophyll cytosol**, atmospheric CO$_2$ is first converted to bicarbonate and fixed by **PEP carboxylase** onto phosphoenolpyruvate, giving **oxaloacetate**, a four-carbon acid — hence "C4", and hence the first stable product being OAA, not 3-PGA. OAA is reduced to malate, which travels through plasmodesmata into the bundle sheath, where it is decarboxylated. The released CO$_2$ accumulates to 10–20 times atmospheric concentration around RuBisCO, which now works at near its maximum rate with almost no oxygenation. The pyruvate returns to the mesophyll and is regenerated to PEP by **pyruvate phosphate dikinase**.

Two facts make C4 work. **PEP carboxylase has no oxygenase activity at all** and a far higher affinity for its substrate than RuBisCO. And the whole scheme is a **spatial** separation: two cell types, two carboxylations.

The extra cost is real. Regenerating PEP by PPDK produces AMP, not ADP, so restoring it takes **two ATP equivalents**. C4 photosynthesis therefore costs **5 ATP + 2 NADPH per CO$_2$** — 30 ATP per glucose, against the C3 plant's 18.

### CAM plants

**Crassulacean acid metabolism** solves the same problem by **temporal** separation instead. At night, when the air is cool and humid, the stomata open; PEP carboxylase fixes CO$_2$ to oxaloacetate and then malate, which is stored as **malic acid in the large central vacuole** — which is why a *ghiukumari* (*Aloe vera*) leaf tastes sour at dawn and bland at dusk. By day the stomata shut tight; the malic acid moves out of the vacuole, is decarboxylated, and the CO$_2$ released behind closed stomata is fixed by RuBisCO in the ordinary Calvin cycle.

| | C3 | C4 | CAM |
|---|---|---|---|
| First stable product | 3-PGA (3C) | oxaloacetate (4C) | oxaloacetate (4C) |
| Primary CO$_2$ acceptor | RuBP | PEP | PEP |
| Primary enzyme | RuBisCO | PEP carboxylase | PEP carboxylase |
| Separation | none | **spatial** (mesophyll / bundle sheath) | **temporal** (night / day) |
| Kranz anatomy | absent | present | absent |
| Photorespiration | high | greatly suppressed | greatly suppressed |
| CO$_2$ compensation point | 40–100 ppm | 3–10 ppm | very low |
| ATP per CO$_2$ | 3 | 5 | 5–6 |
| Stomata open | day | day | **night** |
| Nepali examples | rice, wheat, barley, potato, mustard, soybean | **maize, sugarcane, sorghum, finger millet (kodo), amaranth (latte)** | pineapple, *Aloe vera*, *Opuntia* |

::: caution
Three errors to avoid. **C4 plants are not free of photorespiration** — it is greatly suppressed, not abolished. **Bundle-sheath chloroplasts are not thylakoid-free** — in NADP-ME species such as maize they lack *grana*, which is not the same thing. And it is the **mesophyll** cells of a C4 leaf that lack RuBisCO, not the bundle sheath; get that backwards and the whole pathway becomes nonsense.
:::

### Factors affecting photosynthesis

**Blackman's Law of Limiting Factors (1905):** when a process is governed by several factors, its rate is limited by the factor that is in shortest supply. Raise that one and the rate rises until some other factor becomes limiting in turn.

```figure caption="Light-response curves at two CO2 concentrations. At low light, light limits and the two curves coincide; at high light, CO2 limits and they separate."
fig, ax = plt.subplots(figsize=(4.9, 3.0))
I = np.linspace(0, 1800, 400)
def curve(pmax, alpha, resp):
    return (pmax * alpha * I) / (pmax + alpha * I) - resp
lo = curve(18.0, 0.055, 2.0)
hi = curve(34.0, 0.058, 2.0)
ax.plot(I, hi, color=SERIES[1], lw=2.0, label="high CO$_2$ (700 ppm)")
ax.plot(I, lo, color=ACCENT, lw=2.0, label="normal CO$_2$ (420 ppm)")
ax.axhline(0, color=INK, lw=0.9)
lcp = I[np.argmin(np.abs(lo))]
ax.plot([lcp], [0], "o", color=INK, ms=4.5, zorder=5)
ax.annotate("light compensation point\n(photosynthesis = respiration)",
            xy=(lcp, 0), xytext=(330, -7.5), fontsize=6.4, color=INK,
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9))
ax.text(1180, 30.5, "light is not limiting here;\nCO$_2$ is what limits the rate", fontsize=6.4,
        color=MUTED, ha="center", va="top")
ax.text(210, 9.5, "light\nlimiting", fontsize=6.4, color=MUTED, ha="center")
ax.set_xlabel("light intensity (µmol photons m$^{-2}$ s$^{-1}$)", fontsize=7.2)
ax.set_ylabel("net CO$_2$ uptake", fontsize=7.2)
ax.set_xlim(0, 1850); ax.set_ylim(-9, 34)
ax.tick_params(labelsize=6.6)
ax.legend(fontsize=6.5, frameon=False, loc="lower right")
ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
```

**Light.** Rate rises with intensity and then saturates. The **light compensation point** is the intensity at which photosynthesis exactly balances respiration, so net gas exchange is zero — about 10–50 µmol m$^{-2}$ s$^{-1}$ for a shade plant, over 100 for a sun plant. Quality matters too: red and blue light are most effective, green least.

**Carbon dioxide.** Usually the limiting factor in the field. Atmospheric CO$_2$ is now about **427 ppm (0.043 %)** — do not write 0.03 %, which was true in the 1950s. The **CO$_2$ compensation point** is where uptake balances release: 40–100 ppm in C3 plants, only 3–10 ppm in C4 plants, which is exactly why maize outgrows wheat in hot bright weather.

**Temperature.** Photosynthesis is enzyme-driven, so the rate roughly doubles for each 10 °C rise up to an optimum, then falls steeply as enzymes denature.

**Water, minerals and chlorophyll.** Water shortage closes the stomata and cuts off CO$_2$ long before it affects the biochemistry. Magnesium is in the chlorophyll ring; nitrogen is in the porphyrin and in RuBisCO; iron and manganese are needed to build the electron chain.

::: example Which factor is limiting?
**A rice plant is photosynthesising at 20 °C in bright sunlight with the CO$_2$ concentration held at 420 ppm. The rate does not increase when the light is doubled, but doubles when the CO$_2$ is raised to 800 ppm. What is limiting, and what would happen if the temperature were raised to 30 °C at 800 ppm?**

Doubling the light changes nothing, so **light is not limiting** — the plant is already light-saturated. Raising CO$_2$ doubles the rate, so **CO$_2$ is the limiting factor**.

At 800 ppm, CO$_2$ is no longer in short supply, so the next factor in line takes over. Since enzymes are involved and 20 °C is below the optimum for rice, raising the temperature to 30 °C should raise the rate further — **temperature is now limiting**. This is exactly Blackman's principle: the rate is set by whichever single factor is nearest its minimum.
:::

## 2.3 Respiration

Respiration is the controlled, stepwise oxidation of organic food inside living cells to release energy in a usable form. The point of the many steps is control: burning glucose in a flame releases the same energy, but all at once and all as heat. A cell releases it in small packets and traps much of it in **ATP**, the universal energy currency.

$$\text{C}_6\text{H}_{12}\text{O}_6 + 6\,\text{O}_2 \longrightarrow 6\,\text{CO}_2 + 6\,\text{H}_2\text{O} + \text{energy}$$

The standard free-energy change is about $-2870$ kJ per mole of glucose. Aerobic respiration has four stages.

```figure caption="Aerobic respiration of one glucose molecule. Carbon leaves as CO2 in the first three stages; almost all the ATP is made in the fourth."
fig, ax = plt.subplots(figsize=(4.7, 4.4))
Rect = matplotlib.patches.Rectangle
rows = [
    ("GLYCOLYSIS", "cytoplasm", "glucose (6C) → 2 pyruvate (3C)",
     "net 2 ATP  •  2 NADH", ACCENT),
    ("LINK REACTION", "mitochondrial matrix", "2 pyruvate → 2 acetyl-CoA (2C)",
     "2 CO₂  •  2 NADH", SERIES[4]),
    ("KREBS CYCLE", "mitochondrial matrix", "2 acetyl-CoA → oxidised completely",
     "4 CO₂  •  6 NADH  •  2 FADH₂  •  2 ATP", SERIES[2]),
    ("ELECTRON TRANSPORT + CHEMIOSMOSIS", "inner mitochondrial membrane",
     "10 NADH + 2 FADH₂ + 6 O₂ → 6 H₂O", "about 26 ATP", SERIES[3]),
]
h = 0.190
for i, (name, where, what, out, col) in enumerate(rows):
    y = 0.985 - (i + 1) * h - i * 0.028
    ax.add_patch(Rect((0.02, y), 0.96, h, fc="white", ec=col, lw=1.5))
    ax.text(0.05, y + h - 0.048, name, fontsize=7.0, weight="600", color=col, va="top")
    ax.text(0.95, y + h - 0.046, where, fontsize=6.2, color=MUTED, ha="right",
            va="top", style="italic")
    ax.text(0.05, y + h - 0.113, what, fontsize=6.7, color=INK, va="top")
    ax.text(0.05, y + 0.026, out, fontsize=6.7, color=col, va="bottom", weight="600")
    if i < 3:
        ax.annotate("", xy=(0.50, y - 0.026), xytext=(0.50, y),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4))
ax.text(0.50, 0.060, "TOTAL:  about 30–32 ATP per glucose", fontsize=7.6,
        weight="600", color=INK, ha="center",
        bbox=dict(fc="#f2f5f9", ec=INK, lw=1.0, boxstyle="round,pad=0.34"))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
fig.tight_layout()
```

### Glycolysis

**Glycolysis** (the Embden–Meyerhof–Parnas pathway) happens in the **cytoplasm**, needs no oxygen, and occurs in every living cell. Glucose is phosphorylated twice — an **investment of 2 ATP**, at hexokinase and at **phosphofructokinase**, the committed and rate-limiting step — then split into two three-carbon triose phosphates. Each is oxidised (producing **NADH** at glyceraldehyde-3-phosphate dehydrogenase) and then yields two ATP by **substrate-level phosphorylation**, at phosphoglycerate kinase and at pyruvate kinase.

Gross yield 4 ATP, investment 2 ATP: **net 2 ATP and 2 NADH per glucose**, ending in two molecules of **pyruvate**.

### The link reaction

Pyruvate enters the **mitochondrial matrix** and is handled by the **pyruvate dehydrogenase complex**, which needs thiamine pyrophosphate, lipoic acid, FAD, NAD$^+$, coenzyme A and Mg$^{2+}$. Each pyruvate loses one carbon as CO$_2$, is oxidised, and is attached to coenzyme A:

pyruvate (3C) + NAD⁺ + CoA → acetyl-CoA (2C) + CO₂ + NADH

Per glucose this gives **2 CO$_2$ + 2 NADH**. The reaction is irreversible — which is why animals and plants cannot convert fat back into sugar by simply reversing it.

### The Krebs cycle

Also called the **citric acid cycle** or **tricarboxylic acid (TCA) cycle**, described by Hans Krebs in 1937 (Nobel Prize 1953). It runs in the **matrix**.

Acetyl-CoA (2C) condenses with oxaloacetate (4C) to give **citrate (6C)**. The cycle then runs: citrate → isocitrate → **α-ketoglutarate (5C)** → **succinyl-CoA (4C)** → succinate → fumarate → malate → **oxaloacetate**, regenerated and ready for the next acetyl-CoA. The two carbons that entered leave as CO$_2$ at the two decarboxylations, at isocitrate dehydrogenase and α-ketoglutarate dehydrogenase.

Per turn: 3 NADH, 1 FADH$_2$, 1 ATP (in plants, made directly as ATP), 2 CO$_2$. Per glucose the cycle turns twice: **6 NADH, 2 FADH$_2$, 2 ATP, 4 CO$_2$**.

Running total before the electron transport system: **10 NADH, 2 FADH$_2$, 4 ATP, 6 CO$_2$**. Notice that all six carbons of glucose have now left as carbon dioxide, and not one molecule of oxygen has been used yet.

### The electron transport system and oxidative phosphorylation

The reduced coenzymes are cashed in at the **inner mitochondrial membrane**, whose infoldings — **cristae** — provide the enormous surface area needed. Four complexes and two mobile carriers pass electrons downhill in energy:

**Complex I** (NADH dehydrogenase) → **ubiquinone (coenzyme Q)** → **Complex III** (cytochrome $bc_1$) → **cytochrome c** → **Complex IV** (cytochrome c oxidase) → **oxygen**. FADH$_2$ enters at **Complex II** (succinate dehydrogenase), bypassing Complex I. Oxygen is the **terminal electron acceptor**, combining with electrons and protons to form water — which is why you die without it, and why the whole of the Krebs cycle grinds to a halt in its absence.

As electrons pass, Complexes I, III and IV pump protons from the matrix into the intermembrane space. Per pair of electrons: **Complex I pumps 4, Complex III pumps 4, Complex IV pumps 2** — so **10 H$^+$ per NADH** and **6 H$^+$ per FADH$_2$**. The protons return through **ATP synthase** ($\text{F}_1\text{F}_0$ particles), and their flow drives ATP synthesis. This is **Peter Mitchell's chemiosmotic hypothesis** (Nobel Prize 1978).

### Why 38 and why 30–32

Older books state a yield of **38 ATP per glucose**. That number came from the pre-chemiosmotic assumption that each NADH must yield a whole number of ATP — 3, and each FADH$_2$ exactly 2. Once Mitchell showed that ATP synthesis is driven by a proton gradient, there was no reason for the ratio to be a whole number at all.

Modern accounting: about **4 H$^+$ are consumed per ATP made** (three to turn the rotor and one to carry the phosphate in). So

$$\text{P/O for NADH} = \frac{10}{4} = 2.5 \qquad \text{P/O for FADH}_2 = \frac{6}{4} = 1.5$$

::: example The modern ATP tally
**Calculate the net ATP yield from the complete aerobic oxidation of one glucose molecule.**

| Source | Number | ATP each | ATP |
|---|---|---|---|
| Glycolysis, substrate-level | — | — | **2** |
| Krebs cycle, substrate-level | — | — | **2** |
| NADH (2 glycolysis + 2 link + 6 Krebs) | 10 | 2.5 | **25** |
| FADH$_2$ (Krebs) | 2 | 1.5 | **3** |
| | | **Total** | **32** |

But the 2 NADH made in glycolysis are in the **cytoplasm**, and NADH cannot cross the inner mitochondrial membrane. Their electrons must be ferried in by a shuttle:

- **Malate–aspartate shuttle** — electrons arrive as NADH at Complex I, worth 2.5 each → **32 ATP**.
- **Glycerol-3-phosphate shuttle** — electrons arrive at the ubiquinone pool, worth only 1.5 each → 32 − 2 = **30 ATP**.

Hence the modern answer: **30 to 32 ATP per glucose**, with the real figure in a living cell lower still, because some of the proton gradient leaks and some is spent driving transport. Quote 38 only as the classical figure, and say why it is wrong.
:::

Plants complicate the tally further. Their mitochondria carry **external and internal NAD(P)H dehydrogenases** that feed electrons into the chain without pumping any protons, and a **cyanide-resistant alternative oxidase (AOX)** that passes electrons from ubiquinol straight to oxygen, bypassing Complexes III and IV entirely and releasing the energy as heat. That is how the spadix of *Arum* warms itself by 10 °C or more to volatilise the scents that attract its pollinators.

### Anaerobic respiration and fermentation

Without oxygen the electron transport system stops, NADH cannot be reoxidised, and glycolysis would halt for want of NAD$^+$. **Fermentation exists to regenerate NAD$^+$** so that glycolysis can continue.

**Alcoholic fermentation**, in yeast and in flooded plant roots: pyruvate is decarboxylated by **pyruvate decarboxylase** to acetaldehyde, which is reduced by **alcohol dehydrogenase** to ethanol.

C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + energy

**Lactic acid fermentation**, in overworked muscle and in *Lactobacillus*: pyruvate is reduced directly by lactate dehydrogenase, with **no CO$_2$ released**.

C₆H₁₂O₆ → 2 C₃H₆O₃ (lactic acid) + energy

::: caution
Fermentation itself yields **zero ATP**. The 2 ATP per glucose that anaerobic respiration nets all come from **glycolysis**. The free-energy change of alcoholic fermentation is about $-235$ kJ mol$^{-1}$ against $-2870$ for aerobic respiration — only about 8 % of the available energy is released, and the rest stays locked in the ethanol. That is why yeast makes alcohol and why anaerobic organisms must eat so much.
:::

The **Pasteur effect** is the observation that glucose consumption falls sharply when a fermenting culture is given oxygen — ATP and citrate accumulate and inhibit phosphofructokinase, throttling glycolysis back.

### Respiratory quotient

The **respiratory quotient (RQ)** is the ratio of the volume of carbon dioxide evolved to the volume of oxygen consumed in the same time. It is measured with a **Ganong's respirometer**, and it tells you what substrate is being respired.

$$\text{RQ} = \frac{\text{volume of CO}_2 \text{ evolved}}{\text{volume of O}_2 \text{ consumed}}$$

| Substrate | Example | RQ |
|---|---|---|
| Carbohydrate | glucose, sucrose | **1.00** |
| Fat | tripalmitin | **0.70** |
| Protein | albumin | **0.82** |
| Organic acid | malic acid | **1.33** |
| Organic acid | oxalic acid | **4.00** |
| Anaerobic (CAM at night) | — | **0** (CO$_2$ fixed, none evolved) |
| Strict anaerobiosis | fermenting seed in nitrogen | **undefined** — no O$_2$ is used |

::: example The RQ of a fat
**Show that the RQ of tripalmitin ($\text{C}_{51}\text{H}_{98}\text{O}_6$) is about 0.7.**

Balance the equation for complete oxidation. Two molecules are needed to balance the hydrogens in whole numbers:

2 C₅₁H₉₈O₆ + 145 O₂ → 102 CO₂ + 98 H₂O

Check: carbon, $2 \times 51 = 102$ ✓. Hydrogen, $2 \times 98 = 196 = 98 \times 2$ ✓. Oxygen on the left, $2 \times 6 + 145 \times 2 = 302$; on the right, $102 \times 2 + 98 = 302$ ✓.

$$\text{RQ} = \frac{102}{145} = 0.703$$

Fats are **poor in oxygen relative to carbon**, so oxidising them needs a great deal of external oxygen and the RQ falls below 1. Organic acids are the opposite — already oxygen-rich — so they need little oxygen and the RQ rises above 1. That single idea explains the whole table.
:::

## 2.4 Plant hormones

A **plant hormone** (phytohormone, plant growth regulator) is an organic substance produced in small quantities in one part of a plant, transported to another part, where it regulates a physiological process. Plants have no glands and no nervous system; hormones are the whole of their long-distance chemical coordination.

### Auxin

**Indole-3-acetic acid (IAA)** is the principal natural auxin, made from the amino acid **tryptophan**, chiefly in the **shoot apical meristem, young leaves and developing seeds**.

The discovery is a chain of four experiments, and examiners like it:

1. **Charles and Francis Darwin (1880)**, in *The Power of Movement in Plants*, covered the tips of canary-grass coleoptiles and found that they no longer bent towards light, while covering the lower part made no difference. The **tip perceives** the light; the bending happens below it. They inferred that some "influence" is transmitted downward.
2. **Boysen-Jensen (1913)** cut off the tip and replaced it on a block of gelatin. Bending still occurred, so the influence is a **chemical** that can diffuse.
3. **Paál (1918)** replaced a severed tip **off-centre, in complete darkness**, and got curvature anyway — proving that the chemical, not the light, causes the bending.
4. **Went (1926–28)** let the substance diffuse out of severed tips into agar blocks, applied the blocks to decapitated *Avena* coleoptiles, and found curvature proportional to concentration. He named the substance **auxin** and gave us the *Avena* curvature bioassay.

Auxin moves by **polar transport**, cell to cell, basipetally in the shoot, driven by efflux carrier proteins. Its functions: cell elongation, **apical dominance** (auxin from the apex suppresses the axillary buds below — which is exactly why plucking the tip of a tea bush makes it branch), root initiation on cuttings, prevention of pre-harvest fruit and leaf fall, **parthenocarpy**, and the formation of the abscission layer at high concentration.

Synthetic auxins include **IBA** and **NAA** (rooting hormones), **2,4-D** and 2,4,5-T. As weedkillers they are **selective against dicots**, which is why 2,4-D kills broadleaf weeds in a rice or wheat field while leaving the crop untouched.

::: caution
Auxin's dose–response is **bell-shaped**, and roots and shoots have wildly different optima. A concentration that gives maximum stem elongation ($10^{-5}$ M) strongly **inhibits** root growth; roots are promoted only around $10^{-10}$–$10^{-8}$ M. "Auxin promotes growth" is only half a sentence.
:::

### Gibberellin

**Gibberellic acid (GA$_3$)** is the best known of over a hundred and thirty gibberellins, though only a handful are biologically active. The story begins with **bakanae** or "foolish seedling" disease of rice, in which infected seedlings grow tall, pale and spindly and then collapse. **Kurosawa (1926)** showed that a **cell-free filtrate** of the fungus reproduced the symptoms; **Yabuta and Sumiki (1938)** crystallised the substance. The fungus is *Gibberella fujikuroi* (anamorph *Fusarium fujikuroi*).

Functions: internode elongation (a GA-treated dwarf pea grows as tall as a normal one), **bolting** — the sudden elongation of the stem in rosette plants like cabbage and beet before flowering — breaking of seed and bud dormancy, induction of **α-amylase in the barley aleurone layer** during germination (the basis of commercial malting), and delay of senescence in citrus. Commercially it is sprayed on **Thompson Seedless grapes** to enlarge the berries and loosen the bunch.

### Cytokinin

**Kinetin** (N$^6$-furfuryladenine) was isolated by **Miller and Skoog (1955)** from **autoclaved herring sperm DNA**; it is an artefact of DNA breakdown and not a normal plant constituent. The first genuine natural cytokinin was **zeatin**, isolated by **Letham (1963)** from the milky endosperm of maize. Cytokinins are adenine derivatives, made chiefly in the **root apex** and carried upward in the **xylem**.

Functions: promotion of **cytokinesis** (cell division — but only in the presence of auxin), breaking of bud dormancy, **counteraction of apical dominance** by promoting lateral bud growth, and delay of leaf senescence, known as the **Richmond–Lang effect**.

::: note The tissue-culture ratio — get the direction right
In plant tissue culture the **ratio of auxin to cytokinin** determines what the callus becomes:

- **High auxin : low cytokinin → roots**
- **High cytokinin : low auxin → shoots**
- **Roughly equal → undifferentiated callus**

This is Skoog and Miller's 1957 result, and it is the most commonly inverted fact in the whole chapter.
:::

### Abscisic acid

**ABA** was found twice at once — as **abscisin II** by Addicott's group working on cotton boll abscission, and as **dormin** by Wareing's group working on bud dormancy in sycamore — and the two proved identical. It is a sesquiterpenoid, but in plants it is made by **cleaving a carotenoid** (violaxanthin, then 9-*cis*-neoxanthin) by the enzyme NCED.

ABA is the **stress hormone**, the general growth *inhibitor* and the antagonist of gibberellin. Its functions: **closure of stomata** under water stress (its single most important role), induction and maintenance of **seed dormancy** and seed maturation, inhibition of germination, and promotion of senescence.

::: caution
Despite the name, **ABA is not the hormone of abscission** in most plants. It got its name from the cotton bolls it was first isolated from. Leaf and fruit abscission is regulated mainly by **ethylene**; auxin *delays* it. If a question asks which hormone causes leaf fall, the answer is ethylene.
:::

### Ethylene

**Ethylene (C$_2$H$_4$)** is the only gaseous plant hormone. **Neljubow (1901)** traced the stunting of pea seedlings near gas lamps to ethylene in the illuminating gas, and described the **triple response** — inhibition of stem elongation, radial swelling of the stem, and horizontal growth. **Gane (1934)** proved that apples themselves produce it. It is made from the amino acid **methionine**, via SAM and then **ACC**, the immediate precursor.

Functions: **ripening of fruits**, senescence and abscission of leaves and flowers, **epinasty** (the downward curving of tomato leaves in waterlogged soil), breaking of dormancy, induction of flowering in pineapple and mango, and promotion of female flowers in cucurbits.

Fruit ripening deserves a paragraph of its own. **Climacteric fruits** — banana, mango, papaya, tomato, apple, guava — show a sudden burst of ethylene and a matching surge of respiration at the onset of ripening, and this burst is **autocatalytic**: ethylene stimulates its own production, so one ripe fruit ripens its neighbours. That is "one bad apple spoils the barrel", and it is why ripe fruit is packed with green fruit in a closed basket. **Non-climacteric fruits** — orange, grape, litchi, strawberry, pineapple — have no such burst and will never ripen properly once picked. Commercially, ethylene is supplied as **ethephon (ethrel)**, a liquid that releases ethylene inside the plant.

::: caution
The **calcium carbide** widely used to ripen mangoes and bananas in South Asian markets does **not** release ethylene. It releases **acetylene**, a weak mimic which de-greens the peel without properly developing the sugars and flavour, so the fruit looks ripe and tastes of nothing. The real danger is the impurities in technical-grade carbide, which release **phosphine and arsine**. Carbide ripening is banned in India and prohibited in Nepal; controlled ethylene gas in a ripening chamber is the legal method.
:::

| Hormone | Chemical nature | Main site of synthesis | Signature function |
|---|---|---|---|
| **Auxin (IAA)** | indole derivative | shoot apex, young leaves | cell elongation; apical dominance |
| **Gibberellin (GA$_3$)** | diterpenoid acid | young leaves, embryo, roots | internode elongation; bolting |
| **Cytokinin (zeatin)** | adenine derivative | root apex | cell division; delays senescence |
| **Abscisic acid** | apocarotenoid sesquiterpenoid | leaves, roots, seeds | stomatal closure; seed dormancy |
| **Ethylene** | gaseous hydrocarbon | ripening fruit, senescing tissue | fruit ripening; abscission |

## 2.5 Plant growth and movement

### Growth

**Growth** is a permanent and irreversible increase in size, volume or dry weight of an organism or its parts, accompanied by metabolic activity. The word *irreversible* does the work: a wilted leaf that swells again after watering has not grown, because the change was reversible turgor, not new material.

Growth in plants is **localised**, confined to the meristems, and **indeterminate** — a tree keeps adding new organs for as long as it lives. The growing region of a root or shoot has three zones, running back from the tip: the **zone of cell division** (the meristem proper), the **zone of cell elongation**, where most of the measurable lengthening occurs, and the **zone of maturation or differentiation**, where cells take on their final form.

Growth is measured with an **auxanometer**. In the simple **arc auxanometer** the growing shoot tip is tied to a thread passing over a pulley carrying a long pointer that sweeps across a calibrated arc; the ratio of the pointer arm to the pulley radius magnifies the movement.

Plotted against time, growth follows a **sigmoid (S-shaped) curve**, called the **grand period of growth**, with four phases.

```figure caption="The grand period of growth. The same S-shape describes a single cell, an organ, a whole plant or a population."
fig, ax = plt.subplots(figsize=(5.0, 3.1))
t = np.linspace(0, 12, 400)
y = 100 / (1 + np.exp(-(t - 6.0) * 0.85))
ax.plot(t, y, color=ACCENT, lw=2.3)
bounds = [(0, 3.2), (3.2, 6.0), (6.0, 8.8), (8.8, 12)]
names = ["1. LAG\n(slow)", "2. LOG\n(exponential)", "3. DECELERATION\n(diminishing)",
         "4. STATIONARY\n(maturation)"]
for (a, b), nm, c in zip(bounds, names, [GRID, "#e8f0f8", GRID, "#e8f0f8"]):
    ax.axvspan(a, b, color=c, alpha=0.75, lw=0)
    ax.text((a + b) / 2, 112, nm, fontsize=6.3, ha="center", va="top", color=INK)
ax.plot([6.0], [50], "o", color=SERIES[1], ms=5.5, zorder=5)
ax.annotate("point of inflexion —\ngrowth rate is maximal here",
            xy=(6.0, 50), xytext=(8.0, 30), fontsize=6.4, color=SERIES[1],
            arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.0))
ax.set_xlabel("time", fontsize=7.4)
ax.set_ylabel("total growth (size or dry mass)", fontsize=7.4)
ax.set_xlim(0, 12); ax.set_ylim(0, 128)
ax.set_xticks([]); ax.set_yticks([])
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
```

Two ways of describing growth rate matter. **Arithmetic growth** occurs when, of two daughter cells, only one continues to divide while the other differentiates; length increases linearly, $L_t = L_0 + rt$. **Geometric growth** occurs when both daughters divide, giving exponential increase, $W_1 = W_0 e^{rt}$, where $r$ is the relative growth rate. Real growth is geometric early and arithmetic later, which is what produces the sigmoid shape.

**Absolute growth rate** is the total increase per unit time. **Relative growth rate** is the increase per unit of initial size per unit time — the only fair way to compare a seedling with a sapling.

### Movement

Plants move. They cannot walk, but parts of them change position, and the movements fall into two great classes.

**Tropic movements (tropisms)** are **growth** movements in which the **direction of the response is determined by the direction of the stimulus**. They result from unequal elongation on the two sides of an organ.

| Tropism | Stimulus | Response |
|---|---|---|
| **Phototropism** | light | shoot positive, root negative |
| **Geotropism (gravitropism)** | gravity | **root positive, shoot negative** |
| **Hydrotropism** | water | root positive; overrides gravitropism in dry soil |
| **Chemotropism** | chemical | pollen tube grows down the style to the ovule |
| **Thigmotropism** | touch/contact | tendril of *Cucurbita* or pea coils round a support |

Gravity is perceived by **statoliths** — dense, starch-filled **amyloplasts** that settle under gravity in special cells called statocytes, which in a root are the **columella cells of the root cap**. The **Cholodny–Went hypothesis** (1927–28) explains the response: gravity or light causes auxin to be redistributed laterally, and the unequal auxin causes unequal growth.

::: caution
In a horizontally placed seedling, auxin accumulates on the **lower side of both the root and the shoot**. The shoot bends up and the root bends down not because the auxin goes to opposite sides, but because **roots and shoots respond to auxin in opposite ways** — the concentration that stimulates a shoot inhibits a root. Textbooks that claim auxin moves to the upper side of the root have invented a fact to avoid explaining this.
:::

**Nastic movements (nasties)** are movements in which the **direction of the response is fixed by the structure of the organ and is independent of the direction of the stimulus**. Some are growth movements; some are reversible **turgor (variation) movements** and involve no growth at all.

| Nasty | Stimulus | Example | Growth or turgor? |
|---|---|---|---|
| **Photonasty / nyctinasty** | light / darkness | "sleep movements" of *Oxalis* and tamarind leaves; *Mirabilis* flowers opening at dusk | both types occur |
| **Thermonasty** | temperature | *Crocus* and tulip perianth opening on warming | growth |
| **Seismonasty (thigmonasty)** | shock or touch | folding of *Mimosa pudica* leaflets | **turgor** |
| **Chemonasty** | chemicals | tentacles of *Drosera* bending onto prey | turgor |
| **Epinasty / hyponasty** | internal, ethylene | tomato petioles curving down in waterlogged soil | growth |

```photo id="bio12/mimosa" caption="*Mimosa pudica* — lajjawati, the touch-me-not. One bipinnate leaf: four pinnae spread from the tip of a single petiole, each carrying leaflets in pairs. Every joint marked below is a pulvinus, and every pulvinus is a place where the leaf can move." width="96"
crop 0.00 0.30 0.80 1.00
mark 0.625 0.229 "1"
mark 0.200 0.714 "2"
mark 0.300 0.330 "3"
key 1 Leaflets in opposite pairs along a pinna; on touching, each pair folds upwards and closes like a book
key 2 A second pinna of the same leaf — the four pinnae fold together towards one another
key 3 Pulvinus — the swollen joint where the pinnae meet the petiole; its motor cells lose turgor and the whole leaf drops
```

*Mimosa pudica* — **lajjawati**, the sensitive plant — is the classic example and deserves the detail. At the base of each leaflet, each pinna and the whole petiole is a swollen cushion of thin-walled cells called a **pulvinus**. When a leaflet is touched, mechanically sensitive channels fire an electrical signal — a genuine **action potential** — that travels along the leaf at one to three centimetres per second. When it reaches a pulvinus, the motor cells on the lower (ventral) side suddenly lose K$^+$ and anions; water follows osmotically; those cells go flaccid while the upper cells stay turgid; and the leaflet folds or the petiole drops. Folding takes **one to three seconds**; recovery takes **ten to thirty minutes**.

::: caution
*Mimosa*'s response is **seismonasty — a nastic, turgor (variation) movement — not thigmotropism and not a growth movement**. Nothing grows and nothing is permanent; the leaf returns to exactly where it was. Thigmo*tropism* is the tendril, which really does grow unequally and really is permanent. Confusing the two is one of the easiest marks to throw away in this unit.
:::

## Chapter summary

- Water potential $\Psi_w = \Psi_s + \Psi_p$ for an ordinary cell; pure free water is **0 MPa** and every solution is negative. Water moves from higher to lower water potential, and $\Psi_p$ is **negative in the xylem**. DPD is the obsolete equivalent, with $\Psi_w = -\text{DPD}$. Water crosses the root cortex by apoplast, symplast and transmembrane routes, and the **Casparian strip** of lignin in the endodermis forces all of it through at least one plasma membrane; root pressure (0.1–0.2 MPa) is real but far too small to raise sap, and its modern role is refilling embolised vessels.
- Ascent of sap is explained by the **cohesion–tension theory** of Dixon and Joly (1895): evaporation from mesophyll wall menisci creates tension, cohesion holds the column together and adhesion keeps it attached. Strasburger's poisoned-trunk experiment killed the vital-force theories; the capillarity arithmetic kills that one.
- Transpiration is 80–90 % stomatal. Stomata open when **K$^+$ floods into the guard cells**, lowering their solute potential; radial micellation turns the resulting turgor into opening. ABA closes them. The starch–sugar theory is obsolete — onion guard cells have no starch and work perfectly. **Guttation** is different: liquid xylem sap forced out through **hydathodes** by root pressure at night, to be distinguished from dew (external, pure) and bleeding (from a cut).
- Light reaction, in the **thylakoid**: PS II (P680) and PS I (P700) work in series along the **Z-scheme**; photolysis at the Mn$_4$CaO$_5$ complex releases O$_2$ and dumps 4 H$^+$ **into the lumen**. Non-cyclic flow gives ATP + NADPH + O$_2$; **cyclic flow (PS I alone) gives ATP only**, and exists because the Calvin cycle needs a 3 : 2 ratio that linear flow cannot supply.
- Calvin cycle, in the **stroma**: carboxylation, reduction, regeneration. **Per CO$_2$, 3 ATP + 2 NADPH; per glucose, 6 CO$_2$ + 18 ATP + 12 NADPH.** First stable product **3-PGA**.
- **C4** separates the two carboxylations in **space** (Kranz anatomy, PEP carboxylase in mesophyll, RuBisCO in bundle sheath, first product oxaloacetate, 5 ATP per CO$_2$); **CAM** separates them in **time** (stomata open at night, malic acid stored in the vacuole). Both suppress — but do not abolish — photorespiration.
- Aerobic respiration: glycolysis (cytoplasm, net 2 ATP + 2 NADH) → link reaction (2 CO$_2$ + 2 NADH) → Krebs (4 CO$_2$, 6 NADH, 2 FADH$_2$, 2 ATP) → ETS. With P/O ratios of **2.5 for NADH and 1.5 for FADH$_2$**, the total is **30–32 ATP**, not 38. Fermentation makes **no ATP of its own** — it exists to regenerate NAD$^+$. **RQ** = CO$_2$ out / O$_2$ in: 1.00 for carbohydrate, about 0.70 for fat, 0.82 for protein, above 1 for organic acids.
- Five hormones: **auxin** (elongation, apical dominance), **gibberellin** (internode elongation, bolting, α-amylase), **cytokinin** (cell division, delays senescence; high cytokinin gives shoots), **ABA** (stomatal closure, dormancy — *not* abscission), **ethylene** (fruit ripening, abscission, epinasty).
- Growth is irreversible and follows a **sigmoid curve** with lag, log, deceleration and stationary phases. **Tropisms are directional growth movements; nasties are non-directional**, and *Mimosa*'s seismonasty is a reversible **turgor** movement of the pulvinus, not growth.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The water potential of pure water at standard temperature and atmospheric pressure is: <span class="marks">[1]</span>
   (a) $+1$ MPa (b) $-1$ MPa (c) zero (d) equal to its osmotic pressure

2. In the xylem of a rapidly transpiring tree, the pressure potential $\Psi_p$ is: <span class="marks">[1]</span>
   (a) positive and large (b) negative (c) always zero (d) equal to $\Psi_s$

3. The first stable product of the C4 pathway is: <span class="marks">[1]</span>
   (a) 3-phosphoglyceric acid (b) phosphoenolpyruvate (c) oxaloacetic acid (d) malic acid

4. Cyclic photophosphorylation produces: <span class="marks">[1]</span>
   (a) ATP, NADPH and O$_2$ (b) NADPH only (c) ATP only (d) ATP and O$_2$ only

5. The net gain of ATP from glycolysis per molecule of glucose is: <span class="marks">[1]</span>
   (a) 2 (b) 4 (c) 8 (d) 38

6. The respiratory quotient of a germinating castor seed rich in fat is closest to: <span class="marks">[1]</span>
   (a) 0.70 (b) 1.00 (c) 1.33 (d) 4.00

7. Guard cells differ from ordinary epidermal cells in that they: <span class="marks">[1]</span>
   (a) lack a nucleus (b) contain chloroplasts (c) have no wall (d) are dead at maturity

8. Which hormone is sprayed on Thompson Seedless grapes to increase berry size? <span class="marks">[1]</span>
   (a) IAA (b) GA$_3$ (c) zeatin (d) ethephon

9. The folding of *Mimosa pudica* leaflets on touch is an example of: <span class="marks">[1]</span>
   (a) thigmotropism (b) seismonasty (c) photonasty (d) hydrotropism

10. In tissue culture, a high cytokinin to auxin ratio induces the callus to form: <span class="marks">[1]</span>
    (a) roots (b) shoots (c) more callus (d) somatic embryos only

::: note Answers to Group A
**1.** (c) — pure free water is the reference state, defined as zero.
**2.** (b) — the column is under tension, being pulled from above.
**3.** (c) — oxaloacetate, a 4-carbon acid; malate forms afterwards.
**4.** (c) — no water is split, so no O$_2$ and no NADPH.
**5.** (a) — gross 4, investment 2, net 2.
**6.** (a) — fats are oxygen-poor and need a lot of O$_2$.
**7.** (b) — and that is why they can make malate from starch.
**8.** (b) — gibberellic acid, the standard treatment.
**9.** (b) — nastic and turgor-driven, not tropic and not growth.
**10.** (b) — high cytokinin gives shoots; high auxin gives roots.
:::

**Group B — Short answer (4 marks each)**

1. Define water potential and name its four components, stating the sign of each. Why is the working equation for a vacuolated cell only $\Psi_w = \Psi_s + \Psi_p$? <span class="marks">[4]</span>

2. A 0.2 M sucrose solution is prepared at 22 °C. Calculate its solute potential, and state what would happen to a plant cell of $\Psi_w = -0.9$ MPa placed in it. <span class="marks">[4]</span>

3. Give four reasons why root pressure cannot account for the ascent of sap in a tall tree. What is its accepted function in modern plant physiology? <span class="marks">[4]</span>

4. Describe the mechanism of stomatal opening in terms of potassium ion movement. Why is the starch–sugar interconversion theory no longer accepted? <span class="marks">[4]</span>

5. Differentiate between guttation and dew under any four heads. <span class="marks">[4]</span>

6. Distinguish cyclic from non-cyclic photophosphorylation under four heads, and explain why a chloroplast needs both. <span class="marks">[4]</span>

7. Why is the modern ATP yield of aerobic respiration given as 30–32 rather than 38? Explain both the change from 38 and the reason for the range. <span class="marks">[4]</span>

8. Explain, with the balanced equation, why the respiratory quotient of tripalmitin is about 0.7 while that of malic acid is 1.33. <span class="marks">[4]</span>

9. Write short notes on: (a) apical dominance (b) the Richmond–Lang effect. <span class="marks">[4]</span>

10. Distinguish tropic from nastic movements, giving two examples of each and stating in each case whether growth or turgor is involved. <span class="marks">[4]</span>::: note Answers to Group B — outline
1. Definition as free energy of water per unit volume relative to pure free water; $\Psi_s$ negative, $\Psi_p$ usually positive (negative in xylem), $\Psi_m$ negative, $\Psi_g$ $+0.01$ MPa m$^{-1}$. In a vacuolated cell the matric component is negligible against the large vacuolar solute effect, and gravity is negligible below about 10 m.
2. $T = 295$ K; $\Psi_s = -(1)(0.2)(0.00831)(295) = -0.49$ MPa. The solution is **less negative** than the cell ($-0.49 > -0.9$), so water enters the cell, turgor rises and the cell becomes **turgid**.
3. Magnitude too small (0.1–0.2 MPa lifts only about 10–20 m); it disappears at midday when demand is highest; it is absent in many gymnosperms; ascent continues in stems whose living cells have been killed. Modern function: refilling embolised vessels and driving guttation.
4. Blue light → phototropin → H$^+$-ATPase pumps H$^+$ out → hyperpolarisation → inward K$^+$ channels open → K$^+$ in, balanced by Cl$^-$ and malate → $\Psi_s$ falls 0.4–0.8 MPa → water in → turgor + radial micellation → pore opens. Starch–sugar theory rejected because it is too slow, the pH changes are too small, sugars do not rise enough, and **onion guard cells contain no starch yet function normally**.
5. Any four of: internal xylem sap vs external atmospheric vapour; root pressure vs cooling below dew point; hydathodes at margins vs any surface; dilute salt solution vs pure water; leaves a crust vs leaves none.
6. Table as in §2.2, plus: linear flow supplies ATP and NADPH in a ratio of about 1.28 while the Calvin cycle needs 1.50, so cyclic flow makes up the ATP shortfall.
7. The 38 assumed integer P/O ratios (3 per NADH, 2 per FADH$_2$), a pre-chemiosmotic requirement. Since about 10 H$^+$ are pumped per NADH and 4 consumed per ATP, P/O = 2.5; for FADH$_2$, 6/4 = 1.5. The **range** 30–32 arises from the shuttle used for cytoplasmic NADH: malate–aspartate (Complex I, 2.5 each) gives 32; glycerol-3-phosphate (ubiquinone, 1.5 each) gives 30.
8. 2 C₅₁H₉₈O₆ + 145 O₂ → 102 CO₂ + 98 H₂O, RQ = 102/145 = 0.70. Fats are hydrogen-rich and oxygen-poor, so much external O$_2$ is consumed. For malic acid, 2 C₄H₆O₅ + 6 O₂ → 8 CO₂ + 6 H₂O, RQ = 8/6 = 1.33 — the substrate is already partly oxidised and needs little O$_2$.
9. (a) Auxin produced at the shoot apex is transported basipetally and suppresses the growth of axillary buds; decapitation removes the source and the laterals grow, which is the basis of pruning, hedging and tea plucking. (b) Cytokinin applied to a detached leaf delays chlorophyll loss and protein breakdown and mobilises nutrients towards the treated area — demonstrated by Richmond and Lang in *Xanthium* in 1957.
10. Tropic: directional, determined by stimulus direction, always growth — phototropism, gravitropism. Nastic: direction fixed by organ structure, independent of stimulus direction — thermonasty in *Crocus* (growth), seismonasty in *Mimosa* (turgor).
:::

**Group C — Long answer (8 marks each)**

1. Describe the light reaction of photosynthesis. Draw and explain the Z-scheme, state exactly where ATP, NADPH and oxygen are produced, and compare cyclic with non-cyclic photophosphorylation. <span class="marks">[8]</span>

2. Describe the Calvin cycle under its three phases and derive the ATP and NADPH requirement per molecule of glucose. Then explain how C4 and CAM plants each overcome the limitation of RuBisCO, and tabulate the differences between C3, C4 and CAM plants. <span class="marks">[8]</span>

3. Give an account of the aerobic respiration of one molecule of glucose, naming the site, the substrates and the products of each of the four stages, and calculate the total ATP yield showing why the answer is 30–32 and not 38. <span class="marks">[8]</span>

4. Explain the ascent of sap. Evaluate the vital-force and capillarity theories, state the evidence that refutes them, and describe the cohesion–tension theory under its three pillars. <span class="marks">[8]</span>

::: note Answers to Group C — outline
1. Absorption by antenna pigments; PS II (P680, grana) and PS I (P700, stroma lamellae). Z-scheme with redox potential on the vertical axis: P680 → pheophytin → plastoquinone → cytochrome $b_6f$ → plastocyanin → P700 → ferredoxin → FNR → NADPH. Photolysis at the Mn$_4$CaO$_5$ oxygen-evolving complex on the **lumen** side: 2H₂O → O₂ + 4H⁺ + 4e⁻, replacing the electron lost by P680$^+$ ($+1.2$ V, the strongest biological oxidant). Protons accumulate in the lumen from photolysis and from cytochrome $b_6f$ pumping; they return through ATP synthase into the stroma, making ATP by chemiosmosis. **O$_2$ in the lumen, NADPH in the stroma, ATP in the stroma.** Comparison table; significance of cyclic flow as the ATP top-up for the 3 : 2 Calvin requirement. Credit for the diagram.
2. Carboxylation (RuBP + CO$_2$ by RuBisCO → 2 × 3-PGA); reduction (1 ATP + 1 NADPH per 3-PGA → G3P); regeneration (1 ATP per CO$_2$ at phosphoribulokinase). Per CO$_2$ = 3 ATP + 2 NADPH; per glucose, 6 CO$_2$, 18 ATP, 12 NADPH, 12 G3P of which 2 leave. RuBisCO's oxygenase activity and photorespiration; C4 spatial solution with Kranz anatomy, PEP carboxylase (no oxygenase activity, uses HCO$_3^-$), malate shuttle, CO$_2$ concentrated 10–20× in the bundle sheath, extra cost 2 ATP at PPDK giving 5 ATP per CO$_2$; CAM temporal solution with night fixation and vacuolar malic acid storage. Full comparison table with Nepali examples.
3. Glycolysis in the cytoplasm: investment of 2 ATP at hexokinase and PFK, gross 4 ATP at PGK and pyruvate kinase, net 2 ATP + 2 NADH + 2 pyruvate. Link reaction in the matrix by the pyruvate dehydrogenase complex: 2 CO$_2$ + 2 NADH + 2 acetyl-CoA. Krebs cycle in the matrix, citrate through to oxaloacetate, two turns giving 6 NADH, 2 FADH$_2$, 2 ATP, 4 CO$_2$. ETS on the inner membrane: Complexes I–IV, ubiquinone and cytochrome c, O$_2$ as terminal acceptor, 10 H$^+$ per NADH and 6 per FADH$_2$, 4 H$^+$ per ATP, chemiosmosis at ATP synthase. Tally 2 + 2 + 25 + 3 = 32, or 30 with the glycerol-3-phosphate shuttle; the classical 38 assumed integer P/O ratios that chemiosmosis does not require.
4. Magnitude of the problem (0.01 MPa m$^{-1}$ plus friction; a 100 m tree needs about 3 MPa). Vital-force theories — Godlewski's relay pump, Bose's pulsation theory — refuted by Strasburger's experiment (poisoned 20 m oak trunks; all living cells killed, ascent continued) and by the arithmetic of Bose's own pulse rate. Capillarity refuted by calculation ($h \approx 0.6$ m for a 25 µm vessel) and by the fact that conduit diameter increases, not decreases, in taller trunks. Cohesion–tension (Dixon and Joly, 1895): transpiration pull from menisci in wall nanopores of radius 5–10 nm generating up to $-30$ MPa; cohesion by hydrogen bonding with measured tensile strength beyond $-25$ MPa; adhesion to the lignocellulose wall. Result is an unbroken column under a negative pressure potential of $-0.5$ to $-3.0$ MPa, energised by solar latent heat alone.
:::

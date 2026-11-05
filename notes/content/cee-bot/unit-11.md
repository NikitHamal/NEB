---
subject: Botany
grade: CEE
unit: 11
title: Water Relations of Plants
hours: 2
area: Plant Physiology
---

Plant Physiology begins here, and this chapter's **2 of the 40 Botany
questions** are among the most calculation-friendly in the subject: a water
potential sum, a plasmolysis diagnosis, a theory name. The whole chapter
hangs on one quantity — **water potential, Ψw** — and one rule: water
always moves from where Ψw is higher (less negative) to where it is lower.
Master that, the older **DPD** language the Nepali textbooks still use, the
cohesion–tension account of the ascent of sap, and the small cast of
related facts (root pressure, guttation, wilting), and both questions
should fall.

::: key What the paper asks from this chapter
- **Definitions** — diffusion (no membrane), osmosis (solvent across a selectively permeable membrane), imbibition (colloid swelling; protein > starch > cellulose), plasmolysis and deplasmolysis.
- **Water potential** — Ψw = Ψs + Ψp (+ Ψm + Ψg); pure water = 0, everything else negative; Ψs = −imRT.
- **Old language** — OP, TP ( = wall–turgor pressure), **DPD = OP − TP**; mapping: Ψw = −DPD, Ψs = −OP, Ψp = +TP.
- **Cell states** — turgid (Ψp > 0), flaccid (Ψp = 0), plasmolysed (hypertonic bath); incipient plasmolysis: Ψw = Ψs of the cell.
- **Absorption** — root hair zone; apoplast, symplast, transmembrane (aquaporin) paths; Casparian strip blocks the apoplast; no water pump exists — ions move actively, water follows.
- **Ascent of sap** — cohesion–tension (transpiration pull) of Dixon and Joly; why root pressure (≈0.1–0.2 MPa), capillarity and vital-force theories fail; Strasburger's killed-stem experiment; Ψp in xylem is negative.
- **Transpiration** — stomatal 80–90%, cuticular 5–10%, lenticular ~0.1%; "necessary evil" (Curtis); K⁺-influx opens stomata, ABA closes them; factors; potometer measures uptake.
- **Guttation vs dew vs bleeding** — hydathodes (water pores), root pressure at night, *Colocasia*; white salt crust on drying.
- **Wilting** — temporary (midday, recovers) vs permanent (soil below the permanent wilting point ≈ −1.5 MPa).
:::

## 11.1 Diffusion, diffusion pressure deficit, osmosis and plasmolysis

**Diffusion** is the net movement of particles from a region of higher
concentration to one of lower concentration, by their own kinetic energy.
It needs **no membrane, no energy and no living cell**. It brings CO₂ into
a leaf and takes O₂ out — but it is usefully fast only over micrometres,
which is why plants need plumbing.

**Osmosis** is the special case of diffusion in which **water (the
solvent) crosses a selectively permeable membrane**, moving from higher
water potential to lower. In a plant cell the plasma membrane and the
tonoplast select; the cell wall is freely permeable and selects nothing.
Water entering a cell is **endosmosis**, leaving it **exosmosis**.

A solution outside a cell may be **hypotonic** (less concentrated → water
enters, cell swells **turgid**), **isotonic** (no net movement, cell
**flaccid**) or **hypertonic** (more concentrated → water leaves). In a
hypertonic bath the protoplast shrinks and **pulls away from the wall** —
**plasmolysis**. Return the cell to water and it recovers —
**deplasmolysis**. Plasmolysis does three jobs in examinations: it proves
the membrane is selectively permeable (a dead, boiled cell does not
plasmolyse — its membrane is wrecked), and the bath concentration at
which cells *just* begin to plasmolyse (**incipient plasmolysis**, where
turgor pressure is exactly zero) gives the cell sap's osmotic
concentration: at that moment **Ψw(cell) = Ψs(cell) = Ψw(bath)**.

::: caution The definition that always works
"Water moves from a dilute to a concentrated solution" is true only at
equal pressures. Press on one side — as a turgid cell wall presses — and
water can move *into the dilute* side. The definition that never fails:
**water moves from higher to lower water potential**.
:::

### The older language: OP, TP and DPD

Nepali and Indian textbooks long described the cell with three pressures.
The **osmotic pressure (OP)** of the cell sap is the pressure needed to
stop osmosis into it. As water enters, the protoplast presses the wall —
the **turgor pressure (TP)** — and the wall pushes back with an equal
and opposite **wall pressure (WP)**. The cell's actual thirst is the
difference, the **diffusion pressure deficit**:

$$ \text{DPD} = \text{OP} - \text{TP} $$

When TP = OP the cell is fully turgid, DPD = 0 and net entry stops; when
the cell is flaccid or plasmolysed, TP = 0 and **DPD = OP**. The modern
water-potential system (next section) replaced DPD in 1960, but the CEE
syllabus names DPD explicitly, so learn the exact translation:
**Ψw = −DPD, Ψs = −OP, Ψp = +TP**. If a question is set in DPD, convert,
solve in Ψ, convert back.


```figure caption="A water molecule's road through the plant in four stages: osmosis from the soil film into the root hair, inward passage by the apoplast and symplast routes to the xylem, the cohesion–tension column lifted by evaporation at the leaf, and transpiration paying the pull at the stomata."
flow([("root hair", "osmosis from\nthe soil film"),
      ("cortex", "apoplast and\nsymplast in"),
      ("xylem", "cohesion lifts\nthe column"),
      ("leaf", "transpiration\npays the pull")], figsize=(5.2, 2.15))
```

::: example Two cells, one direction: DPD and Ψw agree
**Problem.** Cell A has OP 12 atm and TP 5 atm; cell B has OP 9 atm and TP
1 atm. Which way does water move? Repeat in potentials: A has Ψs = −12,
Ψp = +5; B has Ψs = −9, Ψp = +1.
**Solution.** DPD(A) = 12 − 5 = **7**; DPD(B) = 9 − 1 = **8**: water runs
low DPD → high DPD, i.e. **A → B**. In potentials: Ψw(A) = −12 + 5 = **−7**;
Ψw(B) = −9 + 1 = **−8**: water runs high Ψw → low Ψw, again **A → B**. The
two vocabularies are one physics with opposite sign conventions — which is
exactly what the paper tests.
:::
```photogrid label="11.1" cols="2" ratio="1.2" caption="How a cell decides whether water enters or leaves. (a) Red onion epidermal cells in a strong solution: the purple vacuole shrinks and the membrane pulls away from the wall (plasmolysis). (b) The water potential of a cell is its solute potential plus its pressure potential. A cell with solute potential -0.90 MPa and pressure potential +0.40 MPa has a water potential of -0.50 MPa. A 0.3 M sucrose solution has -iCRT = -0.74 MPa at 25 degrees C, which is lower, so water leaves the cell and the cell loses turgor. Incipient plasmolysis happens when the outside solution equals the cell solute potential, at about 0.36 M sucrose."
@ photo id="ceebot/plasmolysis" cap="Plasmolysis in red onion epidermal cells"
fit 1.2
focus 0.5 0.5
@ svg cap="Water potential of a turgid cell and of 0.3 M sucrose (MPa)"
R, T = 0.008314, 298.15
ps_sol = -1 * 0.3 * R * T
ps_cell, pp_cell = -0.90, 0.40
pc = ps_cell + pp_cell
cinc = -ps_cell / (R * T)
assert abs(ps_sol + 0.7437) < 1e-3 and abs(pc + 0.50) < 1e-9 and abs(cinc - 0.363) < 1e-3 and ps_sol < pc
facts = dict(ps="%.2f" % abs(ps_sol), pc="%.2f" % pc, cinc="%.2f" % cinc)
f = Fig(300, 236)
f.text(150, 12, "Bars left of zero are negative", size=10.5, color=NAVY, bold=True)
rows = (("cell: solute potential", ps_cell, RED, ROSE), ("cell: pressure potential", pp_cell, TEAL, MINT), ("cell: water potential", pc, NAVY, BLUE), ("0.3 M sucrose: water potential", ps_sol, AMBER, SAND))
x0, sc = 160, 130
f.line(x0, 24, x0, 186, color=SLATE)
for i, (lab, v, c, fl) in enumerate(rows):
    y = 28 + i * 39
    f.text(8, y + 2, lab, size=10.5, color=SLATE, anchor="start")
    w = abs(v) * sc
    f.box(x0 - w if v < 0 else x0, y + 10, w, 16, fill=fl, stroke=c, r=2)
    f.text(x0 - w - 5 if v < 0 else x0 + w + 5, y + 18, "%+.2f" % v, size=10.5, color=c, bold=True, anchor="end" if v < 0 else "start", vmid=True)
f.text(150, 208, "-0.74 is below -0.50: water moves out", size=10.5, color=NAVY, bold=True)
f.text(150, 224, "incipient plasmolysis near %s M" % facts["cinc"], size=10.5, color=SLATE, bold=True)
```

## 11.2 Osmotic pressure and potential, water potential, wall pressure and turgor pressure

The **water potential** Ψw is the free energy of water per unit volume,
measured against pure free water. Hence

$$ \Psi_w \text{ of pure free water} = 0 $$

and dissolving anything, tensioning, or binding water to surfaces makes
it **negative**. The working unit is the **megapascal (MPa)** — 1 MPa =
10 bar ≈ 9.87 atmospheres. Water potential is a sum:

$$ \Psi_w = \Psi_s + \Psi_p + \Psi_m + \Psi_g $$

| Component | Name | Sign | Cause |
|---|---|---|---|
| Ψs | solute (osmotic) potential | always ≤ 0 | dissolved solutes |
| Ψp | pressure potential | positive in turgid cells, **negative in xylem** | turgor, or tension |
| Ψm | matric potential | always ≤ 0 | water bound to walls, colloids, soil — huge in dry seeds |
| Ψg | gravitational potential | +0.01 MPa per metre of height | weight of the column |

For an ordinary vacuolated cell Ψm and Ψg are negligible, leaving the
exam equation **Ψw = Ψs + Ψp**. The solute potential of a solution
follows the van't Hoff relation,

$$ \Psi_s = -i\,m\,R\,T $$

where *i* is the ionisation factor (1 for sucrose, about 2 for NaCl), *m*
the molality (≈ molarity when dilute), R = 0.00831 L MPa mol⁻¹ K⁻¹ and T
the absolute temperature. The **osmotic pressure** OP is simply
Ψs with the sign flipped, a positive number.

```figure caption="One cell in three baths. The box is the wall, the shaded block the protoplast. In a hypotonic bath water enters until turgor (Psi_p) balances the solute pull; in a hypertonic bath the protoplast abandons the wall."
fig, axs = plt.subplots(1, 3, figsize=(7.0, 3.5))
cases = [("Hypotonic bath", r"bath $\psi_w=-0.1$ MPa", 2.15, "turgid", "#1d6fb8", r"$\psi_s=-0.9$, $\psi_p=+0.8$", r"cell $\psi_w=-0.1$", "water IN", 1),
         ("Isotonic bath", r"bath $\psi_w=-0.8$ MPa", 1.75, "flaccid", "#5b6472", r"$\psi_s=-0.8$, $\psi_p=0$", r"cell $\psi_w=-0.8$", "no net flow", 0),
         ("Hypertonic bath", r"bath $\psi_w=-2.0$ MPa", 0.85, "plasmolysed", "#c0392b", r"$\psi_s=-1.2$, $\psi_p=0$", r"cell $\psi_w=-1.2$", "water OUT", -1)]
for ax, (ttl, bath, size, state, col, l1, l2, flow, d) in zip(axs, cases):
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-2.6, 2.4); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((-1.15, -1.15), 2.3, 2.3, fc="none", ec=INK, lw=2.6))
    ax.add_patch(Rectangle((-size / 2, -size / 2), size, size, fc="#dbe9f6", ec="#1d6fb8", lw=1.5))
    ax.text(0, 2.12, ttl, ha="center", fontsize=9, fontweight="bold"); ax.text(0, 1.82, bath, ha="center", fontsize=8)
    if d:
        for xx in (-0.55, 0.55):
            y0, y1 = (1.62, 1.25) if d > 0 else (1.0, 1.55)
            ax.annotate("", xy=(xx, y1 - 0.0 if d > 0 else y1), xytext=(xx, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5, mutation_scale=9))
    ax.text(0, -1.5, state.upper(), ha="center", fontsize=9, fontweight="bold", color=col)
    ax.text(0, -1.9, l1, ha="center", fontsize=8); ax.text(0, -2.2, l2, ha="center", fontsize=8)
    ax.text(0, -2.55, flow, ha="center", fontsize=8, color="#2e8b57", fontweight="bold")
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.04)
```

::: example Worked example — a cell coming to equilibrium (in both languages)
**Problem.** A cell has Ψs = −1.1 MPa. It is placed in a solution of
Ψw = −0.3 MPa and left until no net water movement occurs. Find the
cell's Ψp and Ψw at equilibrium, and state its OP, TP and DPD at that
moment.

**Solution.** At equilibrium the cell's water potential equals the
bath's:

$$ \Psi_w(\text{cell}) = -0.3\ \text{MPa} $$

The solute potential is (approximately) unchanged, so

$$ \Psi_p = \Psi_w - \Psi_s = -0.3 - (-1.1) = +0.8\ \text{MPa} $$

The cell is turgid, pressing its wall with 0.8 MPa. In the old language:
OP = −Ψs = 1.1 MPa, TP = Ψp = 0.8 MPa, and DPD = OP − TP = 0.3 MPa = −Ψw,
as it must be. Placed in pure water, the same cell would swell until
Ψp = +1.1 MPa, Ψw = 0 and DPD = 0 — fully turgid and drinking no more.
:::

## 11.3 Absorption, imbibition, ascent of sap, transpiration, guttation and wilting

### Absorption and imbibition

**Imbibition** is the adsorption of water by a hydrophilic colloid, which
swells: dry gram seed triples overnight; a wooden chopping block
tightens in the monsoon. Imbibing capacity runs **protein > starch >
cellulose** (a protein-rich pea out-swells a starchy wheat grain), the
force is the huge matric potential of the dry colloid, and the heat
released as water binds is the **heat of wetting**. Imbibition is the
first step of seed germination.

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


Roots absorb mainly through the **root hair zone**: each hair is one
epiblema cell with a thin wall, no cuticle and sap at a more negative Ψw
than the soil solution (field-capacity soil sits near −0.015 MPa).
Across the cortex water takes three parallel paths — **apoplast**
(through walls, fastest), **symplast** (cytoplasm to cytoplasm through
plasmodesmata) and **transmembrane** (in and out of each cell through
**aquaporin** water channels — Peter Agre, Nobel Prize 2003). At the
endodermis the **Casparian strip** blocks the apoplast, forcing a
membrane crossing: this is the root's selectivity checkpoint and what
makes root pressure possible. Remember: **no plant pumps water**. Ions
are pumped actively; water always follows its potential gradient, which
is why "active absorption" is really active salt uptake with osmosis
trailing behind.

### Ascent of sap

**Root pressure** — the positive pressure (≈0.1–0.2 MPa) that makes sap
well from a cut tomato stump (Hales, 1727) — is osmosis into ion-loaded
xylem sealed by the Casparian strip. It cannot drive the ascent of sap:
0.1 MPa lifts water only about 10 m; it vanishes at midday when flow is
fastest; many gymnosperms never show it; and killed stems still conduct.
Its real jobs are refilling air-locked vessels and driving guttation.

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


**Vital-force theories** (Godlewski's relay pump, J. C. Bose's pulsating
cells) died with **Strasburger's experiment**: poison and boiling water
rose through oak trunks, killing every living cell, while ascent
continued. **Capillarity** fails on arithmetic — it lifts water only
about 0.6 m in a 25 μm vessel, centimetres in wide ones.

The accepted theory is **cohesion–tension (transpiration pull), Dixon
and Joly (1895)**: evaporation from nanometre pores in mesophyll walls
pulls menisci that can generate tensions of tens of MPa; **cohesion**
(hydrogen bonds between water molecules, tensile strength beyond 25 MPa)
keeps the column unbroken, and **adhesion** to vessel walls holds it up.
The whole soil–plant–atmosphere path is one continuous, sun-powered,
metabolically free water column under tension — **xylem Ψp is negative**,
typically −0.5 to −3 MPa at midday.

```figure caption="The soil-plant-atmosphere continuum: each step is more negative than the last, so water runs 'downhill' from soil to air. Note the enormous final step into dry air - that is the engine of the ascent of sap."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.9))
names = ['soil', 'root hair', 'root xylem', 'trunk xylem', 'leaf mesophyll', 'outside air']
vals = [-0.015, -0.3, -0.6, -1.2, -2.0, -93.5]
y = np.arange(len(names))[::-1]
cols = ['#b8860b'] + ['#1d6fb8']*4 + ['#d9534f']
ax.barh(y, vals, color=cols, height=0.56)
ax.set_xscale('symlog', linthresh=1.0)
ax.set_xlim(-400, 3)
ax.set_yticks(y); ax.set_yticklabels(names, fontsize=6.8)
ax.set_xlabel('water potential (MPa, symlog scale)', fontsize=7.2)
ax.axvline(0, color=INK, lw=0.9)
for yy, v in zip(y, vals):
    ax.text(v*1.35 if v < -1 else v - 0.09, yy, f'{v:g}', fontsize=6.3, va='center', ha='right', color=INK)
ax.tick_params(axis='x', labelsize=6.6)
ax.grid(axis='x', lw=0.5, alpha=0.5)
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
fig.tight_layout()
```

### Transpiration, guttation and wilting

**Transpiration** is the loss of water **as vapour** from aerial parts.
**Stomatal** loss is 80–90% of the total, **cuticular** 5–10%, and
**lenticular** (through lenticels) about 0.1%. Stomata occupy a mere
0.5–3% of the leaf surface, yet dominate because many small pores diffuse
almost as fast as one big hole. Transpiration drags minerals up and cools
the leaf; Curtis (1926) called it a **"necessary evil"** — better read
today as the unavoidable price of opening stomata for CO₂. The rate is
measured (as uptake) with a **Ganong potometer**.

Stomata open when blue light switches on the guard cells' proton pump,
**K⁺ floods in** (balanced by Cl⁻ and malate made from starch), Ψs falls,
water enters, and the hoop-like wall microfibrils (**radial
micellation**) force the swelling cells to bow apart. **Abscisic acid
(ABA)** from droughted roots reverses the flow and shuts the pore. (The
old "starch–sugar" theory is history: onion guard cells contain no
starch yet work perfectly, using KCl.) Light, temperature and
low humidity raise transpiration; wind first raises it (thinning the
boundary layer) then lowers it (stomata slam); the true driving force is
the **vapour pressure deficit**, not relative humidity alone.

**Guttation** is the exudation of **liquid** xylem sap through
**hydathodes** (permanently open water pores over loose **epithem** at
vein endings) when root pressure is high and transpiration low — the
dawn drops on *Colocasia* (pidalu), grasses and tomato. Unlike **dew**
(condensed, pure, settles anywhere), guttation fluid carries salts and
sugars and dries to a **white crust**; unlike **bleeding**, it needs no
wound.

**Wilting** is the droop of cells that have lost turgor. **Temporary
wilting** strikes at midday when transpiration briefly outruns
absorption, and the plant recovers by evening although the soil is still
moist. **Permanent wilting** sets in when the soil dries to the
**permanent wilting point** (about **−1.5 MPa**), below which roots
cannot extract water; the plant recovers only if watered before damage
becomes irreversible.



```figure caption="Water relations in four drawers: the pressure arithmetic of the cell, the potential arithmetic that mirrors it, the guard-cell motor that gates the loss, and the four ways water arrives, climbs, leaves or fails."
cards([
    ("Pressures", "DPD = OP − TP\nturgid: DPD 0\nflaccid: DPD = OP"),
    ("Potentials", "Ψw = Ψs + Ψp\npure water Ψw = 0\nhigh Ψw → low Ψw"),
    ("Stomatal motor", "K⁺ in, water follows: open\nABA pumps K⁺ out: close\n90 % of loss is stomatal"),
    ("Arrive and leave", "imbibition swells the seed\nroot pressure: guttation\ncohesion–tension ascent"),
], cols=2, figsize=(6.2, 3.0))
```

::: caution
Four pairs the paper swaps: **DPD and Ψw point opposite ways** (low→high DPD
= high→low Ψw); **OP is positive, Ψs negative**, same magnitude;
**guttation is liquid from hydathodes by root pressure, transpiration is
vapour from stomata by evaporation** — dew is neither; and **plasmolysis
happens only in living cells**, so a plasmolysing cell is by definition
alive.
:::

::: example Water-potential and DPD direction between adjacent cells
**Problem.** Cell A has $\text{OP} = 14\text{ atm}$ and $\text{TP} = 8\text{ atm}$; adjacent Cell B has $\Psi_s = -12\text{ atm}$ and $\Psi_p = 3\text{ atm}$. In which direction does water flow?

**Solution.** For Cell A, $\Psi_w = -\text{OP} + \text{TP} = -14 + 8 = -6\text{ atm}$ ($\text{DPD} = 6\text{ atm}$). For Cell B, $\Psi_w = -12 + 3 = -9\text{ atm}$ ($\text{DPD} = 9\text{ atm}$). Water moves from higher (less negative) $\Psi_w$ to lower $\Psi_w$ (lower DPD to higher DPD): **from Cell A to Cell B**.
:::

```photogrid label="11.2" cols="2" ratio="1.2" caption="Lifting water 100 m. (a) A coast redwood, one of the tallest trees, lifts water from soil to leaves about 100 m up. (b) Capillary rise h = 2 T cos(theta)/(rho g r) is only 1.48 m in a xylem vessel of radius 10 micrometres (T = 0.0728 N/m, rho = 1,000 kg/m3), so it cannot be the main cause. Gravity alone needs a tension of 0.00981 MPa per metre, 0.98 MPa at 100 m; with an equal friction loss in the narrow xylem the leaf end must pull with 1.96 MPa. Transpiration provides that suction and the cohesion of water molecules transmits it, the cohesion-tension theory."
@ photo id="ceebot/redwood" cap="Coast redwoods"
fit 1.2
focus 0.5 0.35
@ svg cap="Tension in the xylem against height (gravity and friction)"
rho, g, Tn = 1000.0, 9.81, 0.0728
cap = lambda r: 2 * Tn / (rho * g * r)
grav = rho * g / 1e6
assert abs(cap(10e-6) - 1.484) < 0.001 and abs(grav - 0.00981) < 1e-9
facts = dict(h10="%.2f" % cap(10e-6), g100="%.2f" % (grav * 100), t100="%.2f" % (2 * grav * 100))
f = Fig(300, 236)
f.text(150, 12, "Tension (MPa) against height (m)", size=10.5, color=NAVY, bold=True)
ax = Axes(f, 44, 34, 232, 140, (0, 120), (0, 2.4))
ax.grid(30, 0.6).axes("m", "MPa")
ax.curve(lambda h: grav * h, 0, 120, color=AMBER, dash=True)
ax.curve(lambda h: 2 * grav * h, 0, 120, color=RED)
ax.pt(100, 2 * grav * 100, "1.96", dx=-6, dy=-10, anchor="end")
ax.pt(100, grav * 100, "0.98", dx=0, dy=18, anchor="middle", color=AMBER)
f.text(52, 50, "red: gravity + friction", size=10.5, color=RED, bold=True, anchor="start")
f.text(52, 64, "amber: gravity only", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(150, 206, "capillary rise in 10 um vessel: 1.48 m only", size=10.5, color=NAVY, bold=True)
f.text(150, 222, "100 m needs about 1.96 MPa suction", size=10.5, color=SLATE, bold=True)
```

## Formula and fact sheet

- **Water moves high Ψw → low Ψw.** Pure water Ψw = 0; cells and solutions negative. 1 MPa = 10 bar ≈ 9.87 atm.
- **Ψw = Ψs + Ψp** (+ Ψm, Ψg = +0.01 MPa/m). Ψs = −imRT, R = 0.00831 L MPa mol⁻¹ K⁻¹; i = 1 sucrose, ≈2 NaCl.
- **Legacy terms**: DPD = OP − TP; Ψw = −DPD; Ψs = −OP; Ψp = +TP = WP (wall pressure, equal and opposite).
- **States**: fully turgid Ψw = 0 (DPD = 0, TP = OP); flaccid/plasmolysed Ψp = 0 (DPD = OP); incipient plasmolysis measures cell Ψs.
- **Imbibition**: colloid swelling, protein > starch > cellulose, heat of wetting; starts germination.
- **Root paths**: apoplast (walls, fast), symplast (plasmodesmata), transmembrane (aquaporins, Agre 2003); Casparian strip blocks apoplast at endodermis.
- **Root pressure**: 0.1–0.2 MPa (Hales 1727), ion-loading + osmosis; refills emboli, drives guttation; cannot raise sap in tall trees.
- **Ascent**: cohesion–tension (Dixon and Joly, 1895); hydrogen-bond cohesion + adhesion + transpiration pull; xylem under negative Ψp; Strasburger's dead trunks refute vital theories; capillarity only ~0.6 m in narrow vessels.
- **Transpiration**: stomatal 80–90%, cuticular 5–10%, lenticular 0.1%; K⁺ in → open, ABA → close; Ganong potometer; "necessary evil" (Curtis, 1926).
- **Guttation**: hydathodes + epithem, night/early morning, *Colocasia*; leaves white crust; ≠ dew, ≠ bleeding.
- **Wilting**: temporary (midday lag) vs permanent (soil ≤ about −1.5 MPa, the permanent wilting point; field capacity ≈ −0.015 MPa).

### Rapid-revision tables and high-yield facts

| Quantity | Value |
|---|---|
| DPD | OP − TP |
| Turgid / flaccid | DPD 0 / DPD = OP |
| Ψw | Ψs + Ψp; pure water 0 |
| Flow rules | low DPD → high DPD; high Ψw → low Ψw |
| WP vs TP | equal magnitude, opposite direction |
| Imbibition | hydrophilic colloids swell; seeds, wood |
| Routes | apoplast (walls), symplast (cytoplasm) |
| Ascent of sap | cohesion–tension (transpiration pull) |
| Transpiration | ~90 % stomatal; K⁺ opens, ABA closes |
| Guttation | hydathodes, liquid, night, root pressure |
| Wilting point | soil water held tighter than roots pull |

## Chapter summary

- Diffusion needs no membrane; osmosis is water diffusing across a selectively permeable one; plasmolysis (reversible) demonstrates both the membrane's selectivity and the cell sap's osmotic strength.
- Water potential Ψw = Ψs + Ψp rules every movement: pure water is zero, all else negative, and water runs from less negative to more negative; van't Hoff's Ψs = −imRT sizes any solution.
- The older DPD = OP − TP is the same physics with flipped signs (Ψw = −DPD): fully turgid means DPD zero; flaccid means DPD = OP.
- Roots absorb through root hairs by apoplast, symplast and aquaporin routes, with the Casparian strip as the membrane checkpoint; imbibition by colloids (protein strongest) starts germination.
- Root pressure (≈0.1–0.2 MPa) is too feeble and too nocturnal to lift sap; the sun does it instead — transpiration tension dragging a cohesive, adhesive water column from soil to air (Dixon and Joly), with xylem under negative pressure.
- Transpiration is mostly stomatal, opened by potassium influx and closed by ABA, driven by vapour pressure deficit and measured with a potometer.
- Liquid water forced out of hydathodes by root pressure is guttation (not dew, not bleeding), and loss of turgor shows as wilting — temporary at midday, permanent below the soil's wilting point of about −1.5 MPa.

## Practice questions

**Set A — Recall (20 questions)**

1. Diffusion is the movement of particles
   (a) against a concentration gradient using ATP (b) from higher to lower concentration by their kinetic energy (c) only across a membrane (d) only in living cells
2. Osmosis is the diffusion of water across a
   (a) freely permeable wall (b) completely impermeable membrane (c) selectively permeable membrane (d) sheet of glass
3. The water potential of pure free water is
   (a) +1 MPa (b) −1 MPa (c) 100 MPa (d) zero
4. Diffusion pressure deficit (DPD) of a cell is equal to
   (a) OP − TP (b) OP + TP (c) TP − OP (d) OP × TP
5. Plasmolysis occurs when a cell is placed in a
   (a) hypertonic solution (b) hypotonic solution (c) isotonic solution (d) distilled water
6. At incipient plasmolysis, the turgor (pressure) potential of the cell is
   (a) maximum (b) equal to the osmotic pressure (c) negative (d) zero
7. Turgor pressure in a plant cell develops because of
   (a) exosmosis (b) photosynthesis (c) endosmosis pressing the protoplast against the wall (d) transpiration
8. The correct order of imbibition capacity is
   (a) cellulose > starch > protein (b) starch > protein > cellulose (c) protein > starch > cellulose (d) protein > cellulose > starch
9. The principal water-absorbing region of the root is the
   (a) root hair zone (b) root cap (c) zone of elongation (d) meristematic zone
10. The Casparian strip blocks which pathway of water movement in the root?
   (a) symplast (b) apoplast (c) transmembrane (d) xylem vessels
11. The cohesion–tension theory of ascent of sap was proposed by
   (a) J. C. Bose (b) Godlewski (c) Stephen Hales (d) Dixon and Joly
12. Root pressure in plants is typically about
   (a) 5–10 MPa (b) 0.1–0.2 MPa (c) 50 MPa (d) 2–3 MPa
13. Stomatal transpiration accounts for about what share of total water loss?
   (a) 5–10% (b) 0.1% (c) 50% (d) 80–90%
14. Stomata open primarily because of the influx into guard cells of
   (a) Na⁺ ions (b) K⁺ ions (c) Ca²⁺ ions (d) Mg²⁺ ions
15. Guttation takes place through special structures called
   (a) hydathodes (b) lenticels (c) stomata (d) nectaries
16. Transpiration was called a "necessary evil" by
   (a) Dixon (b) Strasburger (c) Curtis (d) Hales
17. In the xylem of a transpiring plant, the pressure potential Ψp is
   (a) strongly positive (b) zero (c) equal to Ψs (d) negative (tension)
18. Permanent wilting occurs when the soil water potential falls to about
   (a) 0 MPa (b) −1.5 MPa (c) −0.015 MPa (d) +1.5 MPa
19. Aquaporins are
   (a) water pumps using ATP (b) enzymes splitting water (c) membrane proteins forming water channels (d) holes in the cell wall
20. The rate of transpiration (water uptake) is measured with a
   (a) Ganong potometer (b) respirometer (c) auxanometer (d) manometer only

::: note Answers and explanations — Set A
**1.** (b) — Net movement down the gradient by thermal motion; membranes and ATP are not involved.
**2.** (c) — Osmosis needs a membrane that passes water but restricts solutes.
**3.** (d) — Pure free water is the reference state, Ψw = 0; all solutions and cells are negative.
**4.** (a) — The cell's thirst is its osmotic pull minus the wall's push-back (turgor).
**5.** (a) — A more concentrated (more negative Ψw) bath draws water out until the protoplast leaves the wall.
**6.** (d) — Just as the protoplast loses contact, turgor has fallen to zero, so Ψw = Ψs.
**7.** (c) — Water taken in by endosmosis inflates the protoplast against the inextensible wall.
**8.** (c) — Proteins are the most hydrophilic colloids, then starch, then cellulose.
**9.** (a) — Root hairs multiply the absorbing area; the tip zones behind them absorb little.
**10.** (b) — The ligno-suberin band seals the wall pathway at the endodermis, forcing membrane control.
**11.** (d) — Dixon and Joly (1895); Bose's pulsation and Godlewski's relay pump are the discarded vital theories.
**12.** (b) — A tenth or two of a megapascal lifts water only about ten to twenty metres.
**13.** (d) — Cuticular loss is 5–10% and lenticular only about 0.1%.
**14.** (b) — Light-driven proton pumping lets K⁺ flood in; water follows osmotically.
**15.** (a) — Hydathodes (water pores over epithem) release liquid sap at vein endings.
**16.** (c) — Curtis (1926); the modern reading is the price of admitting CO₂.
**17.** (d) — The whole cohesion–tension mechanism runs on xylem under tension, −0.5 to −3 MPa at midday.
**18.** (b) — The permanent wilting point, against a field capacity of about −0.015 MPa.
**19.** (c) — Channels (Peter Agre, Nobel 2003): they speed water down gradients, they never pump.
**20.** (a) — A potometer tracks the water a cut shoot takes up; an auxanometer measures growth.
:::

**Set B — Understanding (12 questions)**

1. Defining osmosis as movement "from dilute to concentrated" fails in a turgid cell because
   (a) cells have no membranes (b) the wall selects solutes (c) solutes move instead (d) the pressure potential can make water move towards the dilute side
2. For a flaccid or plasmolysed cell, DPD equals OP because
   (a) OP is zero (b) the wall has dissolved (c) turgor pressure is zero (d) water potential is positive
3. A cell placed in pure water stops taking in water when
   (a) its Ψs becomes zero (b) its Ψp rises to balance Ψs, making Ψw = 0 (c) its membrane becomes impermeable (d) all its solutes leak out
4. Aquaporins cannot cause "active absorption" of water because they
   (a) are channels that only speed movement down a water-potential gradient (b) occur only in leaves (c) are made of lipid (d) block water completely
5. Root pressure cannot raise water to the top of a tall tree chiefly because it
   (a) is only about 0.1–0.2 MPa, enough for roughly ten metres (b) acts downwards (c) occurs only in monocots (d) needs stomata
6. The capillarity theory of ascent of sap was rejected because capillary rise in wide vessels is
   (a) several hundred metres (b) independent of radius (c) exactly ten metres (d) only a few centimetres to about half a metre
7. The water column in xylem does not snap under tension mainly because of
   (a) root pressure (b) lignin rings (c) living xylem parenchyma (d) cohesion between water molecules through hydrogen bonds
8. Strasburger's experiment, in which poisoned and boiled tree trunks still conducted water, disproved the
   (a) vital-force theories (b) cohesion–tension theory (c) root pressure measurements (d) existence of vessels
9. A gentle breeze increases transpiration, but a very strong wind can decrease it, because strong wind
   (a) freezes the leaf (b) fills the stomata with dust (c) causes stomatal closure after first thinning the boundary layer (d) raises humidity
10. In drought, abscisic acid (ABA) reaching the leaves causes
   (a) stomatal opening (b) more root hairs (c) stomatal closure by driving ions out of guard cells (d) faster photosynthesis
11. Drops of water at leaf margins at dawn that dry to a white crust are guttation, not dew, because they are
   (a) condensed from air (b) xylem sap forced out by root pressure, carrying dissolved salts (c) rain water (d) secreted nectar
12. A plant that wilts at midday but recovers by evening in moist soil shows temporary wilting because
   (a) its roots have died (b) transpiration temporarily exceeds absorption (c) the soil is below the wilting point (d) its stomata are missing

::: note Answers and explanations — Set B
**1.** (d) — Turgor makes Ψw of a concentrated cell equal to or above that of dilute water outside; only the Ψ definition survives.
**2.** (c) — DPD = OP − TP with TP = 0 when the wall is unstressed.
**3.** (b) — Entry stops at full turgor: Ψw = Ψs + Ψp = 0, the same as the bath.
**4.** (a) — A channel cannot move water uphill; the gradient still does the work.
**5.** (a) — It is also absent at the midday peak of flow and in many gymnosperms.
**6.** (d) — $h = 2\gamma/\rho g r$: even a 25 μm vessel manages only about 0.6 m.
**7.** (d) — Hydrogen bonding gives the column a tensile strength greater than 25 MPa; adhesion holds it to the walls.
**8.** (a) — Dead stems conduct, so no living pump (relay cells, pulsations) can be doing the lifting.
**9.** (c) — First the humid boundary layer is swept away; then guard cells lose water and the pores close.
**10.** (c) — ABA opens anion and outward K⁺ channels; guard cells deflate and the pore shuts.
**11.** (b) — Dew is pure condensed water anywhere; guttation sap exudes at hydathodes and leaves its salts behind.
**12.** (b) — A midday lag between loss and uptake, corrected when transpiration eases.
:::

**Set C — Application (8 questions)**

1. The solute potential of a 0.4 M sucrose solution at 27 °C (R = 0.00831 L MPa mol⁻¹ K⁻¹) is about
   (a) −1.0 MPa (b) −0.25 MPa (c) −2.5 MPa (d) +1.0 MPa
2. A cell has Ψs = −0.9 MPa and Ψp = +0.5 MPa. Its water potential is
   (a) −1.4 MPa (b) +0.4 MPa (c) 0 MPa (d) −0.4 MPa
3. The cell of question 2 is placed in a solution of Ψw = −0.8 MPa. It will
   (a) gain water and burst (b) show no change (c) become fully turgid (d) lose water and tend towards plasmolysis
4. A cell has OP = 12 atm and TP = 7 atm. Its DPD is
   (a) 19 atm (b) 12 atm (c) 5 atm (d) 0 atm
5. Cell A has Ψw = −0.6 MPa and neighbouring cell B has Ψw = −1.1 MPa. Net water movement is
   (a) from B to A (b) none (c) from A to B (d) out of both cells
6. The solute potential of 0.2 M NaCl at 25 °C, taking i ≈ 2, is about
   (a) −0.5 MPa (b) −1.0 MPa (c) −2.0 MPa (d) −0.1 MPa
7. Onion epidermal cells mounted in strong salt solution under the microscope show the protoplast shrunk away from the wall. The cells are
   (a) turgid (b) plasmolysed (c) dividing (d) dead and dissolved
8. The gravitational potential cost of raising water 30 m up a tree is about
   (a) 0.3 MPa (b) 3.0 MPa (c) 0.03 MPa (d) 30 MPa

::: note Answers and explanations — Set C
**1.** (a) — Ψs $= -(1)(0.4)(0.00831)(300) = -1.0$ MPa.
**2.** (d) — Ψw $= \Psi_s + \Psi_p = -0.9 + 0.5 = -0.4$ MPa.
**3.** (d) — The bath (−0.8) is more negative than the cell (−0.4), so water leaves.
**4.** (c) — DPD $= \text{OP} - \text{TP} = 12 - 7 = 5$ atm.
**5.** (c) — Water moves from the less negative (−0.6) to the more negative (−1.1) potential.
**6.** (b) — Ψs $= -(2)(0.2)(0.00831)(298) \approx -0.99$ MPa; ionisation roughly doubles the effect.
**7.** (b) — Exosmosis into the hypertonic mount has plasmolysed them; water would deplasmolyse living cells.
**8.** (a) — Ψg rises 0.01 MPa per metre: $30 \times 0.01 = 0.3$ MPa (friction costs extra on top).
:::

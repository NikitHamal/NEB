---
file: NEBians-IOE-Past-Paper-Engineering-Geology-I-CE102-2081-Baishakh.pdf
subject: Engineering Geology I
level: BE · Year I / Part I
code: CE 102
year_bs: 2081 Baishakh
cal: BS
year_ad: 2024
stream: BCE
time: 1½ hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define engineering geology. Briefly describe the importance of engineering geology in the context of Nepal with suitable examples. [[0.5+1.5]]

@q 2
Discuss the nebular hypothesis. Differentiate between convergent and divergent plate boundary. [[2+2]]

@q 3
(a) Write down the physical properties of minerals. [[2]]
(b) How can you identify the metamorphic rock in the field? [[2]]
(c) Write down the classification of sedimentary rocks. [[2]]

@q 4
(a) Quartzite rock bed dipping towards S25°E. Find its strike direction with figure. [[2]]
(b) Differentiate primary sedimentary structures and secondary structures. [[2]]
(c) What are the field identification criteria of fault? [[2]]
(d) Define thrust. What is the importance of fold in civil engineering? [[2]]

@q 5
(a) Describe geological work of wind with landform developed in brief. [[3]]
(b) Define volcanism. Differentiate between straight and meandering river channel system. [[1+2]]

@q 6
Provide an overview of the tectonic divisions of the Himalayas and discuss the significant engineering geological challenges present in each subdivision. [[3+1]]

<!-- SOLUTIONS -->

@s 1
**Engineering geology** is the application of geological knowledge, principles and methods to the investigation, design, construction and maintenance of engineering works, so that the geological factors (rock and soil type, structure, groundwater, geomorphology and natural hazards) are recognised and taken into account for the safety, economy and durability of the project. [0.5 mark]

**Importance in the context of Nepal.** Nepal lies in the young, tectonically active and still rising Himalaya, where the Indian plate is pushing under Tibet at about 19 mm per year. Its geology is complex (weak, folded and sheared rocks, steep slopes, intense monsoon rain, many large rivers), so almost every engineering project depends on geological input:

1. **Site selection and investigation** of dams, powerhouses, tunnels, bridges and roads: geological mapping, drilling and testing (for example the Melamchi water supply tunnel in the Lesser Himalaya, the Kulekhani, Kaligandaki and Marsyangdi hydropower schemes).
2. **Landslides and slope stability**: road alignment and cuttings (Mugling–Narayangadh, Prithvi and BP highways, Jure landslide 2014 that dammed the Sunkoshi) need geological mapping, slope design and drainage.
3. **Earthquake hazard and active faults**: the Gorkha earthquake of 2015 (Mw 7.8) showed the need for seismic zoning, liquefaction assessment in the Kathmandu basin and the Terai, and for avoiding active faults.
4. **Foundation conditions**: soft lacustrine clays of the Kathmandu basin, loose alluvium in the Terai, and weak Siwalik rocks control bearing capacity and settlement.
5. **Construction materials**: location of good quality aggregate, sand, gravel, stone and limestone (cement), and checking the alkali–aggregate reactivity.
6. **Water resources and floods**: groundwater exploration, springs, reservoir siltation (Churia hills) and river training works (Koshi barrage).
7. **Glacier lake outburst floods (GLOF), debris flows and avalanches** in the high Himalaya (Tsho Rolpa lake): hazard mapping and mitigation.

Without geological study, projects face cost and time overruns, tunnel collapses, dam leakages and failures. [1.5 marks]

@s 2
**Nebular hypothesis.** It was proposed by the German philosopher **Immanuel Kant (1755)** and developed mathematically by the French mathematician **Pierre-Simon Laplace (1796)** to explain the origin of the solar system.

```figure caption="The nebular hypothesis (Kant, Laplace): a hot rotating gas nebula cools and contracts, spins faster and flattens, sheds rings at its equator, and the rings condense into planets orbiting the central Sun."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(1,4,figsize=(6.4,1.9))
for a in axs: a.set_xlim(-3,3); a.set_ylim(-3,3); a.set_aspect("equal"); a.axis("off")
a=axs[0]; a.set_title("1. hot rotating\ngas nebula",fontsize=7.2); a.add_patch(mp.Circle((0,0),2.4,fc="#f9d29a",ec=INK,lw=0.9)); a.annotate("",xy=(-1.0,2.7),xytext=(1.5,2.7),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.1,connectionstyle="arc3,rad=0.3"))
a=axs[1]; a.set_title("2. cooling: contracts,\nspins faster, flattens",fontsize=7.2); a.add_patch(mp.Ellipse((0,0),5.4,1.7,fc="#f9d29a",ec=INK,lw=0.9)); a.add_patch(mp.Circle((0,0),0.6,fc="#f08a2a",ec=INK,lw=0.7))
a=axs[2]; a.set_title("3. rings are shed at\nthe equator",fontsize=7.2)
for r in (1.2,1.8,2.4,2.9): a.add_patch(mp.Circle((0,0),r,fc="none",ec="#d08a2a",lw=1.2))
a.add_patch(mp.Circle((0,0),0.7,fc="#f08a2a",ec=INK,lw=0.7))
a=axs[3]; a.set_title("4. rings condense\ninto planets",fontsize=7.2)
for r in (1.2,1.8,2.4,2.9): a.add_patch(mp.Circle((0,0),r,fc="none",ec="#cfcfcf",lw=0.7,ls="--"))
a.add_patch(mp.Circle((0,0),0.7,fc="#f08a2a",ec=INK,lw=0.7))
for r,ang,s in ((1.2,40,0.14),(1.8,150,0.2),(2.4,250,0.26),(2.9,-30,0.3)): a.add_patch(mp.Circle((r*_np.cos(_np.radians(ang)),r*_np.sin(_np.radians(ang))),s,fc="#3d6fb0",ec=INK,lw=0.6))
```


*Main points.*

1. The solar system began as a huge, hot, slowly rotating cloud (nebula) of gas and dust.
2. The nebula **cooled by radiation and contracted** under gravity. By conservation of angular momentum its **rotation became faster** and it **flattened** at the poles into a disc, bulging at the equator.
3. When the **centrifugal force at the equator balanced gravity**, a ring of gas was thrown off. As contraction continued, **successive rings** were shed one after another.
4. Each ring broke up and the material **condensed (aggregated) into a planet**, which could in turn shed small rings that became its satellites. Saturn's rings are the remains of such a ring.
5. The central mass, still hot and luminous, remained as the **Sun**.

*Merits.* It explains why the planets revolve in the same direction (anticlockwise) and in nearly the same plane, why the orbits are nearly circular, and the origin of satellites.

*Demerits.* The Sun holds 99.8 % of the mass but only about 2 % of the angular momentum of the system (the hypothesis predicts far more); a contracting gas would disperse rather than form rings; some satellites revolve in retrograde directions (e.g. of Uranus, Neptune); and the planets are cold and solid and not formed of hot gas. The modern **solar nebula (planetesimal) theory** keeps the nebular idea but adds accretion of planetesimals. [2 marks]

**Convergent and divergent plate boundaries.**

```figure caption="Plate boundaries: at divergent boundaries plates move apart and new crust forms; at convergent boundaries they move together and one plate is consumed (subduction or collision); at transform boundaries they slide past each other and crust is neither created nor destroyed."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(1,3,figsize=(6.4,2.4))
def base(a,t):
    a.set_xlim(0,10); a.set_ylim(0,6.4); a.set_aspect("equal"); a.axis("off"); a.set_title(t,fontsize=8)
ar=dict(arrowstyle="-|>",color=INK,lw=1.3)
a=axs[0]; base(a,"Divergent (constructive)")
a.add_patch(mp.Rectangle((0,0),10,3.2,fc="#f7e1b5",ec="none"))
a.add_patch(mp.Rectangle((0,3.2),4.4,1.0,fc="#b9bec6",ec=INK,lw=0.8)); a.add_patch(mp.Rectangle((5.6,3.2),4.4,1.0,fc="#b9bec6",ec=INK,lw=0.8))
a.add_patch(mp.Rectangle((4.4,2.6),1.2,1.6,fc="#e8743b",ec="none"))
a.annotate("",xy=(0.6,5.0),xytext=(3.2,5.0),arrowprops=ar); a.annotate("",xy=(9.4,5.0),xytext=(6.8,5.0),arrowprops=ar)
a.annotate("",xy=(5,4.9),xytext=(5,1.8),arrowprops=dict(arrowstyle="-|>",color="#b03a10",lw=1.4))
a.text(5,0.8,"asthenosphere",ha="center",fontsize=6.5); a.text(2.2,3.55,"plate",ha="center",fontsize=6.5); a.text(7.8,3.55,"plate",ha="center",fontsize=6.5)
a=axs[1]; base(a,"Convergent (destructive)")
a.add_patch(mp.Rectangle((0,0),10,3.2,fc="#f7e1b5",ec="none"))
a.add_patch(mp.Polygon([(0,3.2),(4.0,3.2),(7.8,0.4),(7.2,0.0),(3.6,2.6),(0,2.6)],closed=True,fc="#8fa6c4",ec=INK,lw=0.8))
a.add_patch(mp.Polygon([(4.0,3.2),(10,3.2),(10,4.7),(8.6,5.1),(7.0,4.5),(5.2,3.7)],closed=True,fc="#c9b79a",ec=INK,lw=0.8))
a.add_patch(mp.Polygon([(7.4,4.5),(7.9,5.4),(8.4,4.9)],closed=True,fc="#b03a10",ec=INK,lw=0.6))
a.annotate("",xy=(2.6,4.1),xytext=(0.4,4.1),arrowprops=ar); a.annotate("",xy=(7.6,1.9),xytext=(9.6,1.9),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.0,ls="--"))
a.text(1.5,3.55,"oceanic plate",fontsize=6.0,ha="center"); a.text(8.2,3.75,"continental plate",fontsize=5.8,ha="center"); a.text(3.9,5.2,"trench",fontsize=6.0,ha="center")
a=axs[2]; base(a,"Transform (conservative)")
a.add_patch(mp.Rectangle((1,3.2),8,1.8,fc="#c9b79a",ec=INK,lw=0.8)); a.add_patch(mp.Rectangle((1,1.4),8,1.8,fc="#b9bec6",ec=INK,lw=0.8))
a.plot([0.5,9.5],[3.2,3.2],color="#b03a10",lw=2.0)
a.annotate("",xy=(8.2,4.1),xytext=(5.0,4.1),arrowprops=ar); a.annotate("",xy=(1.8,2.3),xytext=(5.0,2.3),arrowprops=ar)
a.text(5,5.6,"plan view",fontsize=6.5,ha="center"); a.text(5,0.6,"transform fault",fontsize=6.5,ha="center",color="#b03a10")
```


| Point | Convergent boundary | Divergent boundary |
|---|---|---|
| Plate motion | plates move **towards** each other | plates move **away** from each other |
| Crust | crust is **destroyed** (consumed) by subduction, or is crumpled in collision | new crust is **created** from rising magma |
| Also called | destructive or compressive margin | constructive or extensional margin |
| Stress | compression | tension |
| Landforms | deep ocean trenches, volcanic arcs, folded mountain belts (Himalaya, Andes), thrusts | mid-oceanic ridges, rift valleys, fissure volcanoes (East African rift, Mid-Atlantic Ridge) |
| Earthquakes | shallow to deep (up to 700 km), very large | shallow only, usually small to moderate |
| Volcanism | explosive, andesitic and rhyolitic | quiet, basaltic |
| Rocks formed | metamorphic and granitic rocks, deformed sedimentary rocks | fresh basalt and gabbro |

| Boundary | Motion | Examples |
|---|---|---|
| **Divergent (constructive)** | plates move apart; new crust forms from rising magma; shallow earthquakes | Mid-Atlantic Ridge, East African rift |
| **Convergent (destructive)** | plates move together: (i) oceanic–continental (the oceanic plate subducts, giving a trench, a volcanic arc and mountains: the Andes), (ii) oceanic–oceanic (island arc: Japan, Mariana trench), (iii) continental–continental (collision, no subduction of light crust, thick mountain belt: the **Himalaya**) | Andes, Japan, Himalaya |
| **Transform (conservative)** | plates slide horizontally past each other; crust neither created nor destroyed; shallow earthquakes | San Andreas fault, Alpine fault of New Zealand |


@s 3
**(a) Physical properties of minerals.** Physical properties are used for the identification of minerals in the field and hand specimen, because they depend on the chemical composition and the atomic structure.

| Property | Meaning and examples |
|---|---|
| **Colour** | the colour in reflected light (quartz white or colourless, magnetite black); varies with impurities, so unreliable for many minerals |
| **Streak** | colour of the powder on a white unglazed porcelain plate (haematite: red-brown, pyrite: greenish black) |
| **Lustre** | appearance in reflected light: metallic, sub-metallic, vitreous (quartz), pearly, silky (gypsum), resinous, greasy, dull or earthy |
| **Hardness** | resistance to scratching, on **Mohs' scale**: 1 talc, 2 gypsum, 3 calcite, 4 fluorite, 5 apatite, 6 orthoclase, 7 quartz, 8 topaz, 9 corundum, 10 diamond |
| **Cleavage** | tendency to break along smooth planes of weak bonding (mica: perfect one direction, feldspar: two directions at 90°, calcite: three directions, not at 90°) |
| **Fracture** | the way a mineral breaks where there is no cleavage: conchoidal (quartz), uneven, splintery, hackly |
| **Specific gravity** | ratio of its weight to that of an equal volume of water (quartz 2.65, galena 7.5) |
| **Crystal form and habit** | external shape: cubic (galena), prismatic, tabular, fibrous, massive |
| **Tenacity** | resistance to breaking, bending: brittle, malleable, flexible, elastic (mica) |
| **Transparency, magnetism, taste, effervescence** | transparent, translucent or opaque; magnetite is attracted by a magnet; halite tastes salty; calcite fizzes in dilute HCl |

**(b) Field identification of metamorphic rocks.** Metamorphic rocks are formed from pre-existing rocks by heat, pressure and chemically active fluids in the solid state. In the field they are identified by:

1. **Foliation**: parallel orientation of platy minerals as slaty cleavage (slate), phyllitic sheen (phyllite), schistosity (schist) or gneissic banding (gneiss). Non-foliated types such as marble and quartzite have a granular texture.
2. **Recrystallised, interlocking grains** of mica, quartz and feldspar, with a **crystalline, sugary** or glittering appearance; porphyroblasts of garnet, staurolite or kyanite in a fine matrix.
3. **Hardness and ring**: the rock is hard and compact and rings when hit with a hammer (slate, quartzite); marble fizzes with dilute HCl.
4. **No fossils** (they are destroyed), no clastic grains, no vesicles; any original bedding is distorted, with crenulations, folds and boudins.
5. **Mode of occurrence**: in mountain belts (the Lesser and Higher Himalaya), along thrusts and shear zones, and as contact zones (aureoles) around igneous intrusions; a **metamorphic grade** increases towards a thrust or intrusion (slate → phyllite → schist → gneiss).

**(c) Classification of sedimentary rocks.** By the mode of origin:

| Class | Origin | Sub-division | Examples |
|---|---|---|---|
| **Clastic (mechanical, detrital)** | cementation of rock fragments transported by water, wind or ice | *Rudaceous* (grain size over 2 mm): conglomerate, breccia. *Arenaceous* (2–1/16 mm): sandstone, arkose, greywacke. *Argillaceous* (below 1/16 mm): siltstone, shale, mudstone, claystone | conglomerate, sandstone, shale |
| **Chemical** | precipitation or evaporation from solution | *Carbonate*: oolitic limestone, dolomite. *Evaporite*: rock salt, gypsum. *Siliceous*: chert, flint. *Ferruginous*: ironstone | gypsum, rock salt, chert |
| **Organic (biogenic)** | accumulation of plant and animal remains | *Calcareous*: fossiliferous limestone, coquina, chalk. *Carbonaceous*: peat, lignite, coal. *Siliceous*: diatomite | coal, chalk, coquina |

@s 4
**(a) Strike of the quartzite bed.** *Strike* is the direction of the horizontal line drawn on a bed, and it is always at right angles to the direction of dip.

The bed dips towards **S25°E**, an azimuth of $180^\circ - 25^\circ = 155^\circ$. The strike is $155^\circ - 90^\circ = 65^\circ$, so it is

$$\boxed{\text{strike} = \text{N65°E (or S65°W)}, \text{ azimuth } 065^\circ\text{–}245^\circ}$$

(a strike of N65°E – S65°W, dipping to the south-east at the dip angle).

```figure caption="Plan view: the bed dips towards S25°E, so the strike line is perpendicular to the dip direction, N65°E–S65°W (azimuth 065°–245°)."
import numpy as _np, matplotlib.patches as mp

da=155; sa=65
fig,ax=plt.subplots(figsize=(3.7,3.4)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3.4,3.4); ax.set_ylim(-3.1,3.3)
def v(az,r): return (r*_np.sin(_np.radians(az)), r*_np.cos(_np.radians(az)))
ax.plot([0,0],[-2.6,2.6],color=MUTED,lw=0.9,ls="--"); ax.text(0.12,2.7,"N",fontsize=9,fontweight="bold")
p1=v(sa,2.6); p2=v(sa+180,2.6); ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=ACCENT,lw=2.4)
ax.annotate("",xy=v(da,1.9),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=2.2))
ax.add_patch(mp.Arc((0,0),2.0,2.0,theta1=90-sa,theta2=90,color=INK,lw=0.9)); t=v(sa/2.0,1.35); ax.text(t[0],t[1]+0.05,"65°",fontsize=8,ha="center")
ax.add_patch(mp.Arc((0,0),1.4,1.4,theta1=-90,theta2=90-da,color=INK,lw=0.9)); t=v((180+da)/2.0,1.05); ax.text(t[0]+0.25,t[1]-0.15,"25°",fontsize=8,ha="center")
ax.plot([0,0],[0,-2.6],color=MUTED,lw=0.9,ls="--"); ax.text(0.12,-2.85,"S",fontsize=9,fontweight="bold")
ax.plot([0],[0],"o",color=INK,ms=4)
q=v(sa,2.95); ax.text(q[0],q[1]+0.1,"strike line  N65°E",fontsize=7.6,ha="center",color=ACCENT)
r=v(da,2.35); ax.text(r[0]+0.1,r[1]-0.25,"dip direction  S25°E",fontsize=7.6,ha="left",color=SERIES[1])
```


**(b) Primary and secondary sedimentary structures.**

| Point | Primary structures | Secondary structures |
|---|---|---|
| Time of formation | formed **during** deposition or immediately after (syn-depositional) | formed **after** deposition, during diagenesis or later weathering and fluid action (post-depositional) |
| Cause | currents, waves, wind, gravity, desiccation | chemical precipitation, groundwater, pressure and solution |
| Examples | bedding and lamination, **cross-bedding**, **graded bedding**, **ripple marks**, mud cracks, rain prints, flute and groove casts (sole marks), load casts | **concretions** and nodules, geodes, stylolites, septaria, **cone-in-cone**, Liesegang rings |
| Use | show the current direction, the top and bottom of beds (younging) and the environment of deposition | show the diagenetic history, fluid movement and the later stresses |

**(c) Field identification criteria of a fault.**

1. **Displacement and discontinuity of beds, dykes, veins or ridges**: the same bed is found offset across a line, or the beds on the two sides do not match.
2. **Repetition or omission of strata** in the stratigraphic sequence (repetition in a reverse fault and omission in a normal fault, when seen along a traverse).
3. **Fault rocks along the plane**: fault breccia, fault gouge (clay-like crushed material), cataclasite and mylonite, often cemented or silicified.
4. **Slickensides, striations and grooves** (polished and scratched surfaces) on the fault plane, whose direction gives the direction of the last movement.
5. **Drag folds** (beds bent near the fault) and sudden changes in the dip and strike of beds across a line.
6. **Topographic evidence**: fault scarps, triangular facets, linear valleys and saddles, truncated spurs, offset streams, sag ponds, sudden break of slope, alignment of springs and hot springs along a line.
7. **Hydrological and vegetation evidence**: line of springs or seepages, sudden change in vegetation, and zones of shearing or mineralisation.


**(d) Thrust and importance of fold.** A **thrust (thrust fault)** is a low-angle **reverse fault** (dip normally less than 45°) in which the hanging wall has moved up and over the foot wall under compression, so that older rocks are pushed over younger rocks. Examples in Nepal: **MCT, MBT and HFT**.

*Importance of fold in civil engineering.*

1. **Dams and reservoirs**: a syncline (trough) tends to hold water and is favourable for a reservoir; an anticline crest has open tension fractures and is likely to leak. Dam axes should be across the fold axis, and not along the dipping limbs towards the downstream side.
2. **Tunnels and underground works**: the crest of an anticline has tension fractures and the rock may fall (roof falls); a syncline core collects water (groundwater inflow) and stress is concentrated at the hinge. Tunnel alignment is best across the strike where the beds are stable.
3. **Slope stability and road cuts**: the dip of beds in the limbs controls dip-slope failures; cuts should avoid slopes parallel to the dip direction.
4. **Foundation** conditions change from the limbs to the hinge; fractured rock, shear along bedding and different strengths of the folded beds need study.
5. **Groundwater and mineral/oil resources**: folds control aquifers (artesian conditions in a syncline) and oil and gas traps (anticlines).
6. Folds are evidence of past stress and are often associated with faults and shear zones, so they help in hazard assessment.

```figure caption="A fold: alternating anticlines (arches, older beds in the core) and synclines (troughs, younger beds in the core). The limbs lie on either side of the hinge; the axial plane divides the fold into two limbs."
import numpy as _np, matplotlib.patches as mp

x=_np.linspace(-1.2,8.2,500)
fig,ax=plt.subplots(figsize=(5.8,3.0))
cols=["#f4d7a1","#e6b97a","#cf9a58","#b27c3f","#8f6130"]
f=0.9*_np.cos(x)
for k in range(5):
    ax.fill_between(x,f-k*0.55,f-(k+1)*0.55,color=cols[k],ec=INK,lw=0.6)
for xa,t in ((0,"anticline"),(6.283,"anticline")):
    ax.plot([xa,xa],[-3.4,1.9],color=ACCENT,lw=1.0,ls="--"); ax.text(xa,2.05,t,ha="center",fontsize=8,fontweight="bold")
ax.plot([3.1416,3.1416],[-3.4,1.9],color=ACCENT,lw=1.0,ls="--"); ax.text(3.14,2.05,"syncline",ha="center",fontsize=8,fontweight="bold")
ax.text(0.05,-0.5,"oldest\nbeds",fontsize=6.5,ha="center",color="white"); ax.text(3.5,1.4,"youngest beds",fontsize=6.5,ha="center")
ax.annotate("axial plane",xy=(3.1416,-2.3),xytext=(4.4,-3.1),fontsize=7.2,color=ACCENT,arrowprops=dict(arrowstyle="-",color=ACCENT,lw=0.7))
ax.annotate("limb",xy=(1.57,0.1),xytext=(1.5,1.15),fontsize=7.2,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.annotate("hinge (crest line)",xy=(0,0.9),xytext=(-1.25,1.6),fontsize=7.2,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.annotate("trough",xy=(3.1416,-0.9),xytext=(3.7,-1.4),fontsize=7.2,color="white",arrowprops=dict(arrowstyle="-|>",color="white",lw=0.8))
ax.set_xlim(-1.3,8.3); ax.set_ylim(-3.5,2.5); ax.axis("off")
```


@s 5
**(a) Geological work of wind** (aeolian processes) is most active in arid and semi-arid regions with little vegetation and loose dry sediment. It consists of erosion, transportation and deposition.

**1. Erosion** (three ways):

- **Deflation**: removal of loose fine particles by the wind, leaving blow-outs or **deflation hollows** (the Qattara depression, Egypt) and a **desert pavement** of pebbles.
- **Abrasion**: sandblasting of rock by wind-borne grains, mostly within 1 m of the ground. It produces **ventifacts** (faceted pebbles), **yardangs** (streamlined ridges parallel to the wind), grooves and **mushroom (pedestal) rocks**.
- **Attrition**: collision of grains that rounds them (well-rounded, frosted sand).

**2. Transportation.** Fine dust in **suspension** (hundreds of km), sand grains by **saltation** (bouncing, up to 75 % of load) and larger grains by **surface creep** (rolling).

**3. Deposition** when the wind speed falls or meets an obstacle:

- **Sand dunes**: *barchan* (crescent-shaped, horns pointing downwind, in limited sand supply), *seif* (longitudinal, parallel to the wind), *transverse* and *parabolic* dunes.
- **Loess**: a thick, fine, buff, unstratified deposit of wind-blown silt (China, and the Himalayan margin).
- **Sand sheets** and ripples.

```figure caption="Landforms of wind action: a barchan dune (plan and profile; sand moves by saltation up the gentle windward face and avalanches down the slip face) and a mushroom rock sculpted by sand abrasion."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(1,3,figsize=(6.4,2.3))
ar=dict(arrowstyle="-|>",color=INK,lw=1.2)
a=axs[0]; a.set_xlim(-3,3); a.set_ylim(-2.6,2.6); a.set_aspect("equal"); a.axis("off"); a.set_title("Barchan dune (plan)",fontsize=8)
t=_np.linspace(-1.0,1.0,100)
xo=-1.2+1.3*(1-t**2); yo=2.0*t
xi=-0.9+0.6*(1-t**2)+0.0*t
a.fill(_np.concatenate([xo,xi[::-1]]),_np.concatenate([yo,yo[::-1]]),color="#e8c98a",ec=INK,lw=0.9)
a.annotate("",xy=(-0.5,0),xytext=(-2.9,0),arrowprops=ar); a.text(-2.4,0.35,"wind",fontsize=7)
a.text(0.9,-2.3,"horns point downwind",fontsize=6.3,ha="center")
b=axs[1]; b.set_xlim(0,10); b.set_ylim(-1.0,4.0); b.axis("off"); b.set_title("Dune profile",fontsize=8)
xs=_np.linspace(0,10,200); yy=_np.where(xs<7,2.6*(xs/7)**1.3,2.6-2.6*(xs-7)/1.2); yy=_np.clip(yy,0,3)
b.fill_between(xs,0,yy,color="#e8c98a",ec=INK,lw=0.9); b.plot([0,10],[0,0],color=INK,lw=0.8)
b.annotate("",xy=(3,3.7),xytext=(0.5,3.7),arrowprops=ar); b.text(1.7,3.9,"wind",fontsize=7,ha="center")
b.text(3.0,1.0,"windward\n(gentle)",fontsize=6.4,ha="center"); b.text(8.7,1.3,"slip face\n(steep, 32°)",fontsize=6.4,ha="center")
c=axs[2]; c.set_xlim(-3,3); c.set_ylim(-3,3.2); c.set_aspect("equal"); c.axis("off"); c.set_title("Mushroom rock",fontsize=8)
c.add_patch(mp.Polygon([(-0.55,-2.5),(0.55,-2.5),(0.35,0.5),(-0.35,0.5)],closed=True,fc="#b9a58a",ec=INK,lw=0.9))
c.add_patch(mp.Ellipse((0,0.9),3.6,1.3,fc="#9d8a70",ec=INK,lw=0.9))
c.plot([-2.8,2.8],[-2.5,-2.5],color=INK,lw=0.8); c.text(0,-2.85,"abrasion is greatest near the ground",fontsize=6.0,ha="center")
```


*Relevance to Nepal.* Wind action is limited to the dry, cold trans-Himalayan region (Mustang and Dolpo, the Kali Gandaki valley) where strong valley winds carry silt and sand.

**(b) Volcanism.** Volcanism (vulcanism) is the whole of the processes by which **molten rock (magma), gases and rock fragments rise from the interior of the Earth and are erupted onto the surface** (or are intruded near it), to form volcanoes and associated landforms. It is common at plate boundaries, along the Pacific Ring of Fire, and at hot spots (Hawaii). Products: lava (basalt, andesite, rhyolite), pyroclastics (ash, lapilli, bombs) and gases (steam, CO₂, SO₂).

```figure caption="Cross-section of a composite (strato) volcano: magma rises from the magma chamber through the vent to the crater and is erupted as lava, ash and gases; successive eruptions build the cone in layers."
import numpy as _np, matplotlib.patches as mp

fig,ax=plt.subplots(figsize=(5.2,3.2)); ax.set_xlim(0,10); ax.set_ylim(-0.2,7.6); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Polygon([(0,2),(2,2),(4.35,5.1),(5.0,4.7),(5.65,5.1),(8,2),(10,2),(10,0),(0,0)],closed=True,fc="#b9a68a",ec=INK,lw=1.0))
for k,(a0,a1) in enumerate(((2.3,0.9),(3.0,1.7))):
    ax.plot([2+0.55*k,4.4+0.2*k],[2.1+0.75*k,5.0-0.1*k],color="#7a6a55",lw=0.8)
ax.add_patch(mp.Rectangle((4.88,0.9),0.24,3.8,fc="#e8743b",ec="none"))
ax.add_patch(mp.Ellipse((5,0.7),4.0,1.3,fc="#d9501f",ec=INK,lw=0.9))
ax.add_patch(mp.Polygon([(7.3,2.5),(8.4,2.0),(9.4,2.0),(8.5,2.35),(7.6,2.9)],closed=True,fc="#e8743b",ec="none"))
for i,(cx,cy,r) in enumerate(((5.0,6.0,0.55),(5.6,6.5,0.7),(4.5,6.6,0.6),(5.2,7.1,0.5))): ax.add_patch(mp.Circle((cx,cy),r,fc="#cfcfcf",ec="none",alpha=0.85))
ax.annotate("crater",xy=(5.0,4.8),xytext=(6.4,6.2),fontsize=7.2,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.annotate("vent (conduit)",xy=(5.0,2.7),xytext=(6.3,3.8),fontsize=7.2,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.text(5,0.62,"magma chamber",fontsize=7.2,ha="center",color="white",fontweight="bold")
ax.annotate("lava flow",xy=(8.6,2.1),xytext=(8.2,3.4),fontsize=7.2,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.text(2.5,6.6,"ash cloud and gases",fontsize=7.2,ha="center")
ax.text(2.3,3.4,"alternating lava and\nash layers",fontsize=6.6,ha="center",rotation=0)
```


**Straight and meandering river channels.**

```figure caption="Straight and meandering river channels in plan view. In a meander the current erodes the outer (cut) bank and deposits sediment on the inner bank as a point bar; a cut-off meander is left as an oxbow lake."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(2,1,figsize=(5.4,3.5))
ar=dict(arrowstyle="-|>",color=INK,lw=1.2)
a=axs[0]; a.set_xlim(0,12); a.set_ylim(-1.0,1.0); a.axis("off"); a.set_title("Straight channel (sinuosity below about 1.1)",fontsize=8)
a.fill_between([0,12],-0.35,0.35,color="#bcd9f2"); a.plot([0,12],[0.35,0.35],color=INK,lw=1.2); a.plot([0,12],[-0.35,-0.35],color=INK,lw=1.2)
a.annotate("",xy=(11.0,0),xytext=(8.5,0),arrowprops=ar); a.text(9.8,0.12,"flow",fontsize=7,ha="center")
b=axs[1]; b.set_xlim(0,12); b.set_ylim(-2.4,2.0); b.axis("off"); b.set_title("Meandering channel (sinuosity above about 1.5)",fontsize=8)
x=_np.linspace(0,12,400); y=0.8*_np.sin(1.1*x)
b.fill_between(x,y-0.3,y+0.3,color="#bcd9f2"); b.plot(x,y+0.3,color=INK,lw=1.2); b.plot(x,y-0.3,color=INK,lw=1.2)
b.annotate("cut bank (erosion, outer bend)",xy=(1.43,1.1),xytext=(2.6,1.7),fontsize=7,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
b.annotate("point bar (deposition, inner bend)",xy=(1.43,0.35),xytext=(2.4,-1.35),fontsize=7,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
b.add_patch(mp.Ellipse((9.7,-1.2),1.8,0.5,fc="#bcd9f2",ec=INK,lw=0.8)); b.text(9.7,-1.75,"oxbow lake",fontsize=7,ha="center")
```


| Point | Straight channel | Meandering channel |
|---|---|---|
| Sinuosity (channel length ÷ valley length) | below 1.05–1.1 | above 1.5 (sinuous, with loops) |
| Plan | nearly straight | series of S-shaped bends |
| Gradient and energy | steep gradient, high energy, in the youth stage and in the upper course | low gradient, moderate energy, in the lower course across the flood plain |
| Erosion and deposition | mostly downcutting; deposits are alternate bars along the banks | erosion of the **outer (cut) bank**, deposition on the **inner bank** (point bar); the loops migrate downvalley |
| Cross-section | symmetrical and nearly uniform | asymmetrical (deep at the outer bend, shallow at the inner bend) |
| Features | rapids, waterfalls, V-valley | oxbow lakes, meander scars, point bars, natural levees |
| Engineering importance | stable river training and bridge location | bank erosion and shifting channel threaten bridges and embankments, and spurs and revetments are needed |

@s 6
**Overview of the tectonic divisions of the Nepal Himalaya.** The Himalayan arc was formed by the collision of the Indian and Eurasian plates (about 50 million years ago) and is divided from south to north into five tectonic zones that are separated by major thrusts or faults, each with a distinctive rock type, structure and relief, and running roughly east–west for the full length of Nepal (about 800 km).

```figure caption="Schematic north-south section through the Nepal Himalaya showing the five tectonic divisions and the thrusts that separate them: HFT (Himalayan Frontal Thrust), MBT (Main Boundary Thrust), MCT (Main Central Thrust) and STDS (South Tibetan Detachment System), all rooted in the Main Himalayan Thrust (MHT). Not to scale."
import numpy as _np, matplotlib.patches as mp

fig,ax=plt.subplots(figsize=(6.4,3.4))
x=_np.linspace(0,9.6,600)
prof=_np.interp(x,[0,1.2,2.4,3.4,5.0,6.0,7.0,9.6],[0.1,0.3,0.8,1.0,1.4,3.3,2.6,2.2])
bounds=[0,1.2,2.4,5.0,7.0,9.6]; cols=["#f0e4a8","#e3c27a","#a8c79a","#c79ab8","#9fb9d6"]
names=["Terai\n(Gangetic\nplain)","Sub-\nHimalaya\n(Siwalik)","Lesser\nHimalaya","Higher\nHimalaya","Tibetan-\nTethys\nHimalaya"]
for i in range(5):
    m=(x>=bounds[i])&(x<=bounds[i+1]); ax.fill_between(x[m],-3.4,prof[m],color=cols[i],ec="none")
    ax.text((bounds[i]+bounds[i+1])/2,4.2,names[i],ha="center",va="center",fontsize=6.4,fontweight="bold",color=INK)
ax.plot(x,prof,color=INK,lw=1.4)
mht=lambda xx: -0.1-0.33*(xx-1.2)
ax.plot([1.2,9.6],[mht(1.2),mht(9.6)],color="#b03a10",lw=1.6)
for xb,t in ((1.2,"MFT/HFT"),(2.4,"MBT"),(5.0,"MCT"),(7.0,"STDS")):
    yb=float(_np.interp(xb,x,prof)); xe=xb+1.9 if t!="STDS" else xb+1.5
    ax.plot([xb,xe],[yb,mht(xe)],color="#b03a10",lw=1.2)
    ax.text(xb,yb+0.35,t,ha="center",fontsize=7,fontweight="bold",color="#b03a10")
ax.text(9.5,-3.25,"MHT (Main Himalayan Thrust)",fontsize=6.6,color="#b03a10",ha="right")
ax.annotate("S",xy=(0.0,-3.3),fontsize=9,fontweight="bold"); ax.annotate("N",xy=(9.5,-2.0),fontsize=9,fontweight="bold")
ax.set_xlim(-0.05,9.7); ax.set_ylim(-3.5,5.0); ax.axis("off")
```


| Division (south to north) | Boundary | Rocks and age | Width and relief |
|---|---|---|---|
| **Terai** (Indo-Gangetic plain) | south of the HFT/MFT | unconsolidated Quaternary alluvium: gravel, sand, silt and clay | 20–50 km wide, 60–300 m above sea level |
| **Sub-Himalaya** (Siwalik or Churia hills) | between the HFT and the MBT | Miocene to Pleistocene molasse: mudstone, siltstone, soft sandstone and conglomerate | 10–50 km, 200–1500 m |
| **Lesser Himalaya** (Mahabharat range and midlands) | between the MBT and the MCT | Precambrian to Palaeozoic phyllite, slate, schist, quartzite, limestone, dolomite, plus granite and gneiss of the Kathmandu and Dadeldhura nappes | 60–80 km, 1000–3000 m |
| **Higher Himalaya** | between the MCT and the STDS | Precambrian to Cambrian high-grade gneiss, schist, migmatite, marble, quartzite and leucogranite | 10–60 km, 3000–8848 m |
| **Tibetan–Tethys Himalaya** | north of the STDS up to the Indus–Tsangpo suture | Cambrian to Cretaceous/Eocene fossiliferous marine rocks: limestone, shale, sandstone | 30–50 km in Nepal, 2500–7000 m |


The boundaries: **MFT/HFT** (Main Frontal Thrust or Himalayan Frontal Thrust) between the Terai and Siwalik; **MBT** (Main Boundary Thrust) between the Siwalik and Lesser Himalaya; **MCT** (Main Central Thrust) between the Lesser and Higher Himalaya; **STDS** (South Tibetan Detachment System) between the Higher Himalaya and the Tibetan–Tethys zone. [3 marks]

**Significant engineering geological challenges** in each division:

| Division | Engineering geological problems |
|---|---|
| **Terai** | Frequent flooding, shifting of river channels, bank cutting and sedimentation; thick soft soils with low bearing capacity and high settlement; high water table; liquefaction of loose sand during earthquakes (Terai is a deep foreland basin that amplifies shaking); arsenic in shallow groundwater; scarcity of rock for aggregate, so river boulders are mined. |
| **Sub-Himalaya (Churia)** | Weak, poorly consolidated sandstone, mudstone and conglomerate that weather quickly; gully erosion, landslides, debris flows and very high sediment yield (reservoir siltation); steeply dipping beds and shear zones along the HFT and MBT; squeezing and water inflow in tunnels; badlands; active faulting with earthquakes; piping and slaking of mudstone. |
| **Lesser Himalaya** | Highly folded, faulted and deeply weathered phyllite, schist and slate with low shear strength along foliation; most of the large landslides (translational and rotational) on road and hydropower projects; thick colluvium and residual soils; tunnelling problems (squeezing, shear zones, groundwater inflow); karst and solution cavities in limestone and dolomite; reservoir leakage; road-cut slope failures on the dip slopes; high seismic hazard (2015 Gorkha earthquake). |
| **Higher Himalaya** | Very steep, rugged terrain and deep gorges; hard but heavily jointed gneiss with rock falls, rockslides and toppling (for example the Jure landslide, 2014); rock avalanches, snow avalanches and glacier retreat; glacial lake outburst floods (GLOF) and debris flows; high seismicity near the MCT; high in-situ stress and rock bursts in deep tunnels; difficult access and short working season. |
| **Tibetan–Tethys Himalaya** | Arid, cold climate with frost shattering and freeze–thaw weathering; weak shale and thin-bedded limestone; large old landslides and talus; permafrost and solifluction at high altitude; active faults (STDS, Thakkhola graben); strong wind erosion; wide variation in rock strength; thin soil and slope instability on steep gorges such as Kali Gandaki. |


In all divisions the **high seismicity** and **intense monsoon rainfall** make landslides, floods and debris flows the key hazards; the careful geological mapping and slope stabilisation (bio-engineering, drainage, retaining structures) are essential. [1 mark]

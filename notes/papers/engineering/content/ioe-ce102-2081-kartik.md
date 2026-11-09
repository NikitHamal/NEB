---
file: NEBians-IOE-Past-Paper-Engineering-Geology-I-CE102-2081-Kartik.pdf
subject: Engineering Geology I
level: BE · Year I / Part I
code: CE 102
year_bs: 2081 Kartik
cal: BS
year_ad: 2024
stream: BCE
time: 1½ hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course, 2080 batch). Pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Differentiate between engineering geology and geology. List various disciplines within the field of geology. [[3]]

@q 2
What is plate tectonics? Describe different types of plate boundaries. [[0.5+1.5]]

@q 3
(a) How do you identify silicate minerals and carbonate minerals in the field? [[2]]
(b) Discuss the engineering significance of three rock types. [[3]]
(c) Define rock texture and describe the texture of igneous rocks. [[3]]

@q 4
(a) Define various geological plane with suitable figures. [[2]]
(b) Differentiate between fault and joint. [[2]]
(c) Define dip amount and strike of a geological plane. Write down the field identification criteria of fold in the field. [[3]]

@q 5
(a) Define geological agent and discuss the geomorphic features produced by running water. [[3]]
(b) Discuss in brief the physical and chemical weathering process. [[3]]

@q 6
Describe the major discontinuities systems and their engineering significance along with different engineering geological problems in the different tectonic sub-division of the Nepal Himalaya. [[2+2]]

<!-- SOLUTIONS -->

@s 1
**Difference between geology and engineering geology.**

| Point | Geology | Engineering geology |
|---|---|---|
| Definition | the science of the Earth: its materials, structure, processes and history | the application of geology to engineering projects and to the environment |
| Aim | to understand the origin and evolution of the Earth and of life | to ensure the safety, economy and durability of engineering structures |
| Nature | pure (basic) science | applied science, a branch of geology |
| Scope | wide: minerals, rocks, fossils, oceans, atmosphere, planets | limited to the site: rock and soil, structure, groundwater, hazards, construction materials |
| Output | theories, maps and age data | site investigation, geotechnical parameters, hazard maps, design recommendations |
| Users | geologists, researchers | civil, mining, hydropower and environmental engineers |

**Disciplines (branches) of geology.**

| Branch | Study of |
|---|---|
| Mineralogy | minerals: composition, structure and properties |
| Petrology | rocks (igneous, sedimentary, metamorphic petrology) |
| Structural geology | folds, faults, joints, foliation and deformation |
| Stratigraphy | rock layers, their sequence, correlation and age |
| Palaeontology | fossils and past life |
| Geomorphology | landforms and the processes that shape them |
| Sedimentology | sediments, sedimentary processes and environments |
| Physical geology | the Earth's processes: weathering, erosion, volcanism, earthquakes |
| Historical geology | the geological history of the Earth |
| Hydrogeology | groundwater |
| Economic geology | ore, coal, oil, and industrial minerals |
| Geophysics and seismology | physical properties of the Earth, earthquakes |
| Geochemistry and geochronology | chemical composition and age dating |
| Volcanology and glaciology | volcanoes; glaciers and ice |
| Engineering geology | application of geology to engineering |

@s 2
**Plate tectonics** is the theory that the Earth's outer rigid shell, the **lithosphere** (crust plus the uppermost mantle, about 100 km thick), is broken into about seven large and several small **plates**, which float on and move slowly (2–15 cm per year) over the plastic **asthenosphere**, driven by mantle convection, ridge push and slab pull. Most earthquakes, volcanoes and mountain building occur at plate boundaries. (It developed from Wegener's continental drift and Hess's sea-floor spreading.) [0.5 mark]

**Types of plate boundary.**

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


| Boundary | Motion | Examples |
|---|---|---|
| **Divergent (constructive)** | plates move apart; new crust forms from rising magma; shallow earthquakes | Mid-Atlantic Ridge, East African rift |
| **Convergent (destructive)** | plates move together: (i) oceanic–continental (the oceanic plate subducts, giving a trench, a volcanic arc and mountains: the Andes), (ii) oceanic–oceanic (island arc: Japan, Mariana trench), (iii) continental–continental (collision, no subduction of light crust, thick mountain belt: the **Himalaya**) | Andes, Japan, Himalaya |
| **Transform (conservative)** | plates slide horizontally past each other; crust neither created nor destroyed; shallow earthquakes | San Andreas fault, Alpine fault of New Zealand |


*Himalaya.* The Himalaya is a continental–continental convergent boundary; the Indian plate moves north at about 40 mm per year and converges with Eurasia at about 19–20 mm per year in the Nepal Himalaya, creating the thrusts MFT, MBT, MCT and the frequent earthquakes. [1.5 marks]

@s 3
**(a) Silicate and carbonate minerals in the field.**

| Test | Silicate minerals (quartz, feldspar, mica, olivine, pyroxene, amphibole, garnet) | Carbonate minerals (calcite, dolomite, magnesite, siderite) |
|---|---|---|
| Composition | contain the Si–O tetrahedron | contain the CO₃²⁻ group with Ca, Mg, Fe |
| **Dilute HCl test** | **no effervescence** | **calcite fizzes briskly in cold dilute HCl**; dolomite fizzes only as a powder or when warm; magnesite and siderite only on heating |
| Hardness | mostly hard, 5–7 (quartz 7, feldspar 6): scratch glass, not scratched by a knife | soft to medium, 3–4: scratched easily by a knife blade or a copper coin |
| Cleavage | varied: one direction (mica), two at 90° (feldspar), none (quartz, conchoidal fracture) | **rhombohedral cleavage in three directions not at 90°** (calcite and dolomite) |
| Lustre and colour | vitreous, colourful (green olivine, black hornblende) | vitreous to pearly, usually white, colourless or pale, translucent |
| Specific gravity | about 2.5–3.5 (3.2–4.3 for garnet and olivine) | 2.7–3.1 |
| Occurrence | igneous and metamorphic rocks, sandstone | limestone, dolomite and marble; veins |

**(b) Engineering significance of the three rock types.**

| Rock type | Properties | Engineering significance |
|---|---|---|
| **Igneous** (granite, basalt, gabbro, diorite) | massive, strong, hard, dense, low porosity and permeability, durable | excellent foundation rock for dams, bridges and tall buildings; aggregate for concrete and roads; building and dimension stone. Weak points are joints (leakage), weathering (grus), vesicular and weathered volcanic rocks, and sheeting in granite |
| **Sedimentary** (sandstone, limestone, shale, conglomerate) | stratified, variable strength and porosity; limestone is soluble; shale is weak and slakes | sandstone and limestone as building stone, aggregate and (limestone) cement, lime and flux; layers form aquifers and reservoirs. Problems: bedding-plane slides, solution cavities and sinkholes (karst), swelling and slaking of shale and mudstone, weak Siwalik rocks |
| **Metamorphic** (slate, phyllite, schist, gneiss, quartzite, marble) | foliated or non-foliated; foliated rocks are anisotropic | quartzite and gneiss are strong aggregate and foundation rock; marble is decorative stone; slate for roofing and flooring. Problems: low shear strength along foliation (phyllite and schist), slope failures and tunnel squeezing in the Lesser Himalaya |

**(c) Rock texture.** *Texture* is the **size, shape and mutual arrangement (relationship) of the mineral grains or crystals in a rock**; in igneous rocks it records the **rate and place of cooling of the magma** (slow cooling at depth gives large crystals, fast cooling at the surface gives fine grains or glass).

| Texture | Description | Example |
|---|---|---|
| **Phaneritic** (coarse-grained) | crystals visible to the naked eye, from slow cooling (plutonic) | granite, gabbro |
| **Aphanitic** (fine-grained) | crystals too small to see, rapid cooling (volcanic) | basalt, rhyolite |
| **Porphyritic** | large crystals (phenocrysts) in a fine groundmass: two stages of cooling | porphyry, andesite porphyry |
| **Glassy (vitreous)** | no crystals, very rapid cooling | obsidian |
| **Vesicular** | gas bubble holes (vesicles); **amygdaloidal** when filled with minerals | pumice, scoria, amygdaloidal basalt |
| **Pegmatitic** | very coarse crystals (over 1 cm) from water-rich residual magma | pegmatite |
| **Pyroclastic (fragmental)** | rock made of explosively ejected fragments | tuff, volcanic breccia, agglomerate |
| **Equigranular / inequigranular** | crystals of the same size or of different sizes | granite, syenite |
| **Special**: graphic, ophitic, poikilitic, spinifex | intergrowths of minerals | graphic granite, dolerite |

@s 4
**(a) Geological planes.** A geological plane is a planar surface in a rock mass that separates two rock bodies or is a surface of weakness. The main ones:

```figure caption="Section showing several geological planes: tilted older beds, an angular unconformity, horizontal bedding planes with vertical joint planes, and an inclined fault plane."
import numpy as _np, matplotlib.patches as mp

fig,ax=plt.subplots(figsize=(5.6,3.2)); ax.set_xlim(0,12); ax.set_ylim(0,7); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),12,3.3,fc="#e3d3b4",ec=INK,lw=1.0))
for k in range(-5,10):
    ax.plot([0,12],[0.0+0.45*k-0.0,0.0+0.45*k+4.2*0+2.2*0+0.0+3.0*0.35],color="#9a8566",lw=0.6) if False else None
import math
for k in range(-6,8):
    x0=0; y0=k*0.55; x1=12; y1=k*0.55+12*0.45
    ax.plot([x0,x1],[max(min(y0,3.3),0) if False else y0,y1],color="#9a8566",lw=0.6,clip_on=True)
ax.add_patch(mp.Rectangle((0,3.3),12,3.7,fc="white",ec="none",zorder=2))
ax.add_patch(mp.Rectangle((0,3.3),12,3.0,fc="#cfe0c0",ec=INK,lw=1.0,zorder=3))
for yy in (3.9,4.5,5.1,5.7): ax.plot([0,12],[yy,yy],color="#7a8f69",lw=0.7,zorder=4)
for xx in (1.8,4.4,7.0,9.6): ax.plot([xx,xx],[3.3,6.3],color=INK,lw=1.0,ls=(0,(4,2)),zorder=5)
ax.plot([0,12],[3.3,3.3],color="#b03a10",lw=2.0,zorder=6)
ax.plot([8.2,10.5],[0,3.3],color=ACCENT,lw=2.0,zorder=6)
ax.annotate("fault plane",xy=(9.4,1.7),xytext=(10.0,0.35),fontsize=7.3,color=ACCENT,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.8),zorder=7)
ax.annotate("unconformity surface",xy=(3.0,3.3),xytext=(0.4,6.6),fontsize=7.3,color="#b03a10",arrowprops=dict(arrowstyle="-|>",color="#b03a10",lw=0.8),zorder=7)
ax.annotate("bedding planes (horizontal)",xy=(6.0,5.1),xytext=(3.9,6.7),fontsize=7.3,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8),zorder=7)
ax.annotate("joint planes (vertical)",xy=(7.0,4.2),xytext=(8.4,6.5),fontsize=7.3,arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8),zorder=7)
ax.text(2.2,1.2,"tilted older beds\n(bedding / foliation planes)",fontsize=7.0,zorder=7)
```


1. **Bedding plane**: the surface that separates successive layers (beds) of sedimentary rock, formed during deposition; it is the original horizontal surface and may later be tilted.
2. **Joint plane**: a fracture along which there is **no appreciable displacement**; joints occur in sets (systematic) and often are perpendicular to the bedding.
3. **Fault plane**: the fracture along which the rock masses on the two sides have **moved relative to each other**.
4. **Foliation / cleavage plane**: the parallel surfaces produced in metamorphic rocks by oriented platy minerals or by flattening (slaty cleavage, schistosity).
5. **Unconformity surface**: the buried erosional surface that separates younger beds from older rocks (represents a time gap).
6. **Axial plane** of a fold: the plane that divides the fold into two limbs.

Each plane is described by its **strike and dip**.

**(b) Fault and joint.**

| Point | Fault | Joint |
|---|---|---|
| Displacement | the rock masses are **displaced** along the plane | **no displacement** (or negligible) across the plane |
| Size | usually long, from metres to hundreds of km | usually short, from cm to a few tens of m |
| Associated material | breccia, gouge, mylonite and slickensides | clean planes, sometimes veins; no crushed rock |
| Cause | shear stress, tension or compression (tectonic) | tension, cooling, unloading, tectonic stress |
| Occurrence | single or a few planes, in zones | in sets (systems) of parallel planes |
| Types | normal, reverse, thrust, strike-slip | tension joints, shear joints, sheet joints, columnar joints |
| Engineering effect | weak zones, earthquakes, leakage; avoid for dams and tunnels | increase permeability, reduce rock strength, control slope failures and overbreak |

**(c) Dip amount and strike.**

```figure caption="Dip and strike. Strike is the direction of the horizontal line in a bed; the dip amount (true dip) is the maximum inclination of the bed to the horizontal, measured in the vertical plane at right angles to the strike, in the direction of dip."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(1,2,figsize=(6.2,2.6))
a=axs[0]; a.set_xlim(-0.5,9); a.set_ylim(-3.2,3.2); a.set_aspect("equal"); a.axis("off"); a.set_title("Section along the dip direction",fontsize=8)
a.plot([0,8],[0,0],color=MUTED,lw=1.0,ls="--"); a.text(8.1,0,"horizontal",fontsize=6.8,va="center")
a.fill([0,8,8],[0,0,-3.0],color="#e6b97a",ec=INK,lw=1.0,alpha=0.85)
a.add_patch(mp.Arc((0,0),3.6,3.6,theta1=-20.6,theta2=0,color=INK,lw=1.0))
a.text(2.2,-0.55,"δ",fontsize=11); a.text(4.6,0.35,"true dip δ",fontsize=7.4)
a.text(0.2,1.2,"bed (plane)",fontsize=7.0,color=ACCENT)
b=axs[1]; b.set_xlim(-3,3); b.set_ylim(-3,3.2); b.set_aspect("equal"); b.axis("off"); b.set_title("Plan view",fontsize=8)
b.plot([0,0],[-2.6,2.6],color=ACCENT,lw=2.4); b.text(0.1,2.8,"N",fontsize=9,fontweight="bold")
b.annotate("",xy=(1.9,0),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=2.0))
b.text(-0.15,-1.4,"strike line\n(horizontal line\non the bed)",fontsize=6.8,color=ACCENT,ha="right"); b.text(0.3,0.3,"dip direction",fontsize=6.8,color=SERIES[1])
```


- **Strike** of a plane is the **direction (bearing) of the horizontal line** formed by the intersection of the plane with a horizontal plane. It is measured with a compass-clinometer from the north (for example N65°E).
- **Dip** is the **maximum inclination of the plane to the horizontal**, measured in the vertical plane at right angles to the strike. The **dip amount** (true dip angle) is the angle of that inclination, from 0° (horizontal) to 90° (vertical), and the **dip direction** is the direction in which the plane slopes down, always 90° from the strike (for example 40° towards S25°E).

*Apparent dip* is the inclination measured along any direction other than the true dip direction, and it is always less than the true dip.

**Field identification criteria of a fold.**

1. **Symmetrical repetition of beds** on the two sides of a line (the axis): in an **anticline** the oldest beds are in the core and the dips are *away* from the axis; in a **syncline** the youngest beds are in the core and the dips are *towards* the axis.
2. **Opposite dips on the two limbs** of the structure when traversing across the strike (for example NE dips followed by SW dips).
3. **Outcrop pattern** on a map: a V or U shaped outcrop closing around the hinge; a zig-zag or nose-shaped pattern in a plunging fold; the oldest beds in the centre of an eroded anticline.
4. **Top-and-bottom evidence** (ripple marks, graded bedding, cross-bedding) shows the younging direction of the beds, so that anticlines and synclines are told apart even when beds are overturned.
5. **Minor structures**: drag folds on the limbs, axial plane cleavage (it dips more steeply than the bedding in the limbs), joints that fan out, and the *S* and *Z* shape of small parasitic folds that tell the position on the large fold.
6. **Measurement of dip and strike** at several stations along a traverse across the strike, plotted on a map or section.


@s 5
**(a) Geological agent.** A *geological agent* is any natural medium that **wears down (erodes), transports and deposits** the Earth's surface materials, and so shapes the landscape. They are **running water (rivers)**, **wind**, **glaciers**, **groundwater**, **sea waves and currents** and **gravity** (mass wasting), in addition to the internal agents (volcanism and earthquakes). Running water is the most important agent of erosion on the continents, especially in Nepal.

**Geomorphic features produced by running water.**

**Erosional features** (mainly in the youth stage and in the upper course, where the valley is steep):

| Feature | Description |
|---|---|
| V-shaped valley | vertical downcutting by a swift river; steep walls, narrow floor |
| Gorge and canyon | deep, very narrow valley in resistant rock (Kali Gandaki, Trishuli, Arun gorges) |
| Waterfall and rapids | hard rock band over softer rock; the plunge pool under the fall |
| Potholes | circular depressions drilled in the river bed by pebbles in swirling water |
| River (stream) terraces | step-like surfaces left when the river cuts down into its old flood plain (the Kathmandu and Pokhara basin terraces) |
| Interlocking spurs | ridges that alternate from the two sides of a V-valley |
| Meander scars and cut banks | outer banks of meanders eroded by the current |

**Depositional features** (mainly in the mature and old stage, in the lower course where the gradient is gentle):

| Feature | Description |
|---|---|
| Alluvial fan and cone | fan-shaped deposit where a mountain stream enters a plain (the Terai bhabar belt) |
| Flood plain | broad flat area covered by silt during floods |
| Natural levees | low ridges built along the banks by overflow |
| Point bars and channel bars | sediment deposited on the inner bank of a meander or in mid-channel |
| Braided channels | a network of shifting channels and bars (Koshi, Narayani, Karnali rivers in the Terai) |
| Oxbow lakes | cut-off meander loops |
| Delta and estuary | fan-shaped deposit where the river enters the sea or a lake (Ganga delta) |


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


**(b) Weathering** is the **in-situ disintegration and decomposition of rocks at or near the Earth's surface** by the atmosphere, water and organisms, without transport. It forms soil, and creates weak zones that affect engineering structures.

**Physical (mechanical) weathering** breaks the rock into smaller pieces without changing its composition:

1. **Frost wedging**: water freezes in joints and expands by about 9 %, which wedges the rock (frequent in the Himalaya above 3000 m).
2. **Thermal expansion and exfoliation**: repeated heating and cooling produces unequal expansion of minerals and the peeling of sheets from rock, in arid regions.
3. **Pressure release (unloading)**: erosion of the cover releases confining stress and the rock cracks into sheets parallel to the surface (sheeting in granite).
4. **Salt crystal growth** in pores and cracks.
5. **Biological action**: plant roots wedging in cracks and burrowing animals.

**Chemical weathering** changes the minerals into new, usually weaker, minerals. It is faster in warm, humid climates:

| Process | Example reaction |
|---|---|
| **Solution** | halite and gypsum dissolve in water |
| **Carbonation** (and dissolution of limestone) | CaCO₃ + H₂CO₃ ⇌ Ca²⁺ + 2HCO₃⁻, giving caves and karst |
| **Hydrolysis** | 2KAlSi₃O₈ (orthoclase) + 2H₂CO₃ + 9H₂O → Al₂Si₂O₅(OH)₄ (kaolinite) + 4H₄SiO₄ + 2K⁺ + 2HCO₃⁻ |
| **Oxidation** | 4FeO + O₂ → 2Fe₂O₃ (iron minerals rust: red-brown stains) |
| **Hydration** | CaSO₄ (anhydrite) + 2H₂O → CaSO₄·2H₂O (gypsum): swells |
| **Chelation (organic acids)** | organic acids from lichen and humus remove metal ions |

Granite and gneiss weather mainly into clay, quartz sand and iron oxides, and limestone dissolves. The *rate* depends on the rock, climate (temperature and rain), slope, time and vegetation. Weathering depth in the Lesser Himalaya can reach tens of metres, causing deep landslides.

@s 6
**Major discontinuities (thrust systems) of the Nepal Himalaya** and their significance. All are roughly east–west, north-dipping thrusts that **root in a basal detachment, the Main Himalayan Thrust (MHT)**, at 5–15 km depth.

| Discontinuity | Position | Nature | Engineering significance |
|---|---|---|---|
| **MFT / HFT** (Main Frontal Thrust or Himalayan Frontal Thrust) | between the Terai and the Sub-Himalaya | youngest and active thrust; Siwalik rocks over the Quaternary alluvium | active fault: surface rupture and earthquakes (the 1934 Bihar–Nepal earthquake), scarps, groundwater springs along the front; avoid siting dams and large buildings across it |
| **MBT** (Main Boundary Thrust) | Siwalik and Lesser Himalaya | thrust of pre-Tertiary rocks over Siwalik; wide shear zone | fractured, sheared rock; many landslides and springs along the zone; roads, tunnels and dams are difficult in the crushed rocks |
| **MCT** (Main Central Thrust) | Lesser and Higher Himalaya | a shear zone some kilometres thick, with strongly sheared and metamorphosed rock (schist, mylonite) | high seismicity, strong landslides and weak rock in the shear zone; tunnels and bridge sites need detailed study |
| **STDS** (South Tibetan Detachment System) | Higher Himalaya and Tethys Himalaya | north-dipping normal fault | hydrothermal activity, thick fractured zones; relevant for roads near the Tibetan border |
| **Indus–Tsangpo Suture Zone (ITSZ)** | north of the Tethys Himalaya | the collision suture of the two plates | ophiolites and a highly sheared zone; remote, rarely engineered |

Because of these thrusts, Nepal is exposed to large earthquakes (average recurrence of great events in centuries), and project sites should be at a safe distance from the traces of active faults (HFT and others) and seismic design must be adopted. [2 marks]

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


**Engineering geological problems in the tectonic divisions.**

| Division | Engineering geological problems |
|---|---|
| **Terai** | Frequent flooding, shifting of river channels, bank cutting and sedimentation; thick soft soils with low bearing capacity and high settlement; high water table; liquefaction of loose sand during earthquakes (Terai is a deep foreland basin that amplifies shaking); arsenic in shallow groundwater; scarcity of rock for aggregate, so river boulders are mined. |
| **Sub-Himalaya (Churia)** | Weak, poorly consolidated sandstone, mudstone and conglomerate that weather quickly; gully erosion, landslides, debris flows and very high sediment yield (reservoir siltation); steeply dipping beds and shear zones along the HFT and MBT; squeezing and water inflow in tunnels; badlands; active faulting with earthquakes; piping and slaking of mudstone. |
| **Lesser Himalaya** | Highly folded, faulted and deeply weathered phyllite, schist and slate with low shear strength along foliation; most of the large landslides (translational and rotational) on road and hydropower projects; thick colluvium and residual soils; tunnelling problems (squeezing, shear zones, groundwater inflow); karst and solution cavities in limestone and dolomite; reservoir leakage; road-cut slope failures on the dip slopes; high seismic hazard (2015 Gorkha earthquake). |
| **Higher Himalaya** | Very steep, rugged terrain and deep gorges; hard but heavily jointed gneiss with rock falls, rockslides and toppling (for example the Jure landslide, 2014); rock avalanches, snow avalanches and glacier retreat; glacial lake outburst floods (GLOF) and debris flows; high seismicity near the MCT; high in-situ stress and rock bursts in deep tunnels; difficult access and short working season. |
| **Tibetan–Tethys Himalaya** | Arid, cold climate with frost shattering and freeze–thaw weathering; weak shale and thin-bedded limestone; large old landslides and talus; permafrost and solifluction at high altitude; active faults (STDS, Thakkhola graben); strong wind erosion; wide variation in rock strength; thin soil and slope instability on steep gorges such as Kali Gandaki. |


(Rock types and widths of the five divisions are given in the schematic section above: Terai alluvium, Siwalik molasse, Lesser Himalayan phyllite, schist and quartzite, Higher Himalayan gneiss, and Tethys fossiliferous limestone and shale.) [2 marks]

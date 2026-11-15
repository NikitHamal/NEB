---
file: NEBians-IOE-Past-Paper-Engineering-Geology-I-ENCE102-2081-Chaitra.pdf
subject: Engineering Geology I
level: BE · Year I / Part I
code: ENCE 102
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE
time: 1½ hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Discuss the branches of geology with their interrelationships. [[2]]

@q 2
Define tidal hypothesis. Explain the mountain building process focussing on the evolution of the Himalaya. [[1+2]]

@q 3
(a) How do you identify three rock types in the field? [[2]]
(b) Describe the physical properties, engineering properties and engineering uses of following rocks. [[3×2]]
(i) Granite (ii) Phyllite (iii) Limestone

@q 4
(a) A limestone rock bed dips towards S 55°E. Find its strike direction with figure. [[2]]
(b) Define fold with neat sketch. What are the field identification criteria of fault? Discuss the importance of fault in civil engineering. [[2+2+2]]

@q 5
(a) What are various erosional and depositional features formed by a river? [[3]]
(b) Write short notes on Karst topography and Cirque. [[2]]

@q 6
Discuss engineering geological problems in different tectonic subdivision of the Nepal Himalaya. [[4]]

<!-- SOLUTIONS -->

@s 1
**Geology** is the science of the Earth (its materials, structure, processes and history). It is divided into many branches that overlap and depend on each other:

| Branch | Study of | Links to other branches |
|---|---|---|
| **Mineralogy** | minerals | basis of petrology; ores are studied in economic geology; geochemistry gives the composition |
| **Petrology** | rocks: igneous, sedimentary and metamorphic | uses mineralogy; the rock cycle links the three groups; needed for engineering geology |
| **Structural geology** | folds, faults, joints, foliation | deforms the rocks studied in petrology and stratigraphy; connected to tectonics and seismology |
| **Stratigraphy** | succession, correlation and age of strata | uses palaeontology (index fossils), sedimentology and geochronology |
| **Palaeontology** | fossils | dates the strata (stratigraphy) and tells the past environment |
| **Geomorphology** | landforms and processes | depends on rock type (petrology), structure and climate; used in hazard assessment |
| **Hydrogeology** | groundwater | depends on the structure and permeability of rocks |
| **Geophysics and seismology** | physical properties; earthquakes | explore the interior and structure (tectonics) |
| **Economic geology** | ores, coal, oil, construction materials | depends on mineralogy, petrology and structural geology |
| **Engineering geology** | application of the above to engineering | combines petrology, structure, geomorphology, hydrogeology and rock and soil mechanics |

*Interrelationship.* No branch stands alone: a **rock** (petrology) is made of **minerals** (mineralogy), is deformed into **folds and faults** (structural geology), forms **strata** that are dated by **fossils** (stratigraphy and palaeontology), is shaped into **landforms** by weathering and erosion (geomorphology), holds **groundwater** (hydrogeology), and finally becomes the **foundation material** of the engineer (engineering geology).

@s 2
**Tidal hypothesis.** The tidal (encounter) hypothesis for the origin of the planets was proposed by **James Jeans (1919)** and **Harold Jeffreys (1929)**. It says that the **Sun was once a lone star; a much larger passing star came very close**, and its gravitational (tidal) pull drew a **long, cigar-shaped filament of hot gas** out of the Sun. The filament, thicker in the middle, broke up into blobs that **condensed into the planets** (the largest Jupiter and Saturn from the centre of the filament, the small Mercury and Pluto from its ends), and the intruder went away. The satellites formed from smaller tidal pulls of the planets. A *weakness*: it needs a rare near collision of stars, and gas pulled from the Sun would be too hot and would expand and disperse; it also does not explain the angular momentum of the planets. [1 mark]

```figure caption="The tidal (encounter) hypothesis of Jeans and Jeffreys: a passing star raises a huge tidal filament from the Sun, which breaks into blobs that condense into planets (largest in the middle of the filament)."
import numpy as _np, matplotlib.patches as mp

fig,ax=plt.subplots(figsize=(5.0,2.4)); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Circle((2.0,2.5),1.3,fc="#f08a2a",ec=INK,lw=0.9)); ax.text(2.0,2.5,"Sun",fontsize=8,ha="center",va="center")
ax.add_patch(mp.Polygon([(3.1,2.9),(6.2,2.6),(3.1,2.1)],closed=True,fc="#f9d29a",ec=INK,lw=0.8)); ax.text(5.0,3.05,"cigar-shaped\ntidal filament",fontsize=6.6,ha="center")
ax.add_patch(mp.Circle((7.6,1.2),0.7,fc="#cfd8ff",ec=INK,lw=0.9)); ax.text(7.6,0.1,"passing star",fontsize=7,ha="center")
ax.annotate("",xy=(9.6,3.2),xytext=(7.6,1.4),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2,ls="--")); ax.text(9.4,3.6,"path",fontsize=7)
ax.annotate("tidal pull",xy=(6.0,2.5),xytext=(5.6,1.2),fontsize=7,arrowprops=dict(arrowstyle="-|>",color="#b03a10",lw=1.2),color="#b03a10")
```


**Mountain building and the evolution of the Himalaya.** Mountains are formed by **orogeny**: the compression of the lithosphere at convergent boundaries, which produces folding, thrusting, metamorphism, magmatism and uplift. The classical sequence is: (1) deposition of thick sediments in a trough (geosyncline); (2) compression by plate convergence; (3) folding, faulting, metamorphism and intrusion; (4) isostatic uplift and erosion. The **Himalaya**, a *collisional (Alpine type)* range, is the best-known example:

```figure caption="Stages in the building of the Himalaya: (a) India separated from Tibet by the Tethys Sea, (b) subduction of Tethys oceanic crust beneath Tibet, (c) continental collision with scraping of the Tethys sediments, (d) continuing convergence thrusts India beneath the range along the MCT, MBT and HFT."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(2,2,figsize=(6.4,4.2))
def base(a,t):
    a.set_xlim(0,10); a.set_ylim(0,6); a.axis("off"); a.set_title(t,fontsize=7.6)
    a.add_patch(mp.Rectangle((0,0),10,2.0,fc="#f7e1b5",ec="none"))
t1="#c9b79a"; oc="#8fa6c4"; sea="#cfe6f7"
a=axs[0,0]; base(a,"(a) Before collision: Tethys Sea (about 100 Ma)")
a.add_patch(mp.Polygon([(0,2),(3.2,2),(3.2,3.0),(0,3.0)],closed=True,fc=t1,ec=INK,lw=0.8)); a.add_patch(mp.Rectangle((3.2,2),3.6,0.9,fc=sea,ec=INK,lw=0.7)); a.add_patch(mp.Polygon([(6.8,2),(10,2),(10,3.4),(6.8,3.0)],closed=True,fc=t1,ec=INK,lw=0.8))
a.text(1.6,2.5,"India",fontsize=7,ha="center"); a.text(5,2.45,"Tethys\nsediments",fontsize=6.6,ha="center"); a.text(8.4,2.6,"Tibet (Asia)",fontsize=7,ha="center")
a.annotate("",xy=(3.0,4.2),xytext=(0.6,4.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3))
a=axs[0,1]; base(a,"(b) Subduction of Tethys crust (about 65-55 Ma)")
a.add_patch(mp.Polygon([(0,2),(3.4,2),(3.4,3.0),(0,3.0)],closed=True,fc=t1,ec=INK,lw=0.8))
a.add_patch(mp.Polygon([(3.4,2.0),(5.6,2.0),(7.4,0.6),(7.0,0.3),(5.4,1.5),(3.4,1.5)],closed=True,fc=oc,ec=INK,lw=0.8))
a.add_patch(mp.Polygon([(5.6,2),(10,2),(10,3.8),(6.4,3.3)],closed=True,fc=t1,ec=INK,lw=0.8))
a.add_patch(mp.Polygon([(7.4,3.5),(7.8,4.3),(8.2,3.6)],closed=True,fc="#b03a10",ec=INK,lw=0.6))
a.text(1.6,2.5,"India",fontsize=7,ha="center"); a.text(8.3,2.7,"Tibet",fontsize=7,ha="center"); a.text(4.3,1.0,"oceanic slab",fontsize=6.4,ha="center")
a.annotate("",xy=(3.0,4.2),xytext=(0.6,4.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3))
a=axs[1,0]; base(a,"(c) Continental collision (about 50 Ma)")
a.add_patch(mp.Polygon([(0,2),(5.0,2),(5.4,3.0),(0,3.0)],closed=True,fc=t1,ec=INK,lw=0.8))
a.add_patch(mp.Polygon([(5.0,2),(10,2),(10,3.8),(5.6,3.3),(5.4,3.0)],closed=True,fc=t1,ec=INK,lw=0.8))
a.add_patch(mp.Polygon([(5.0,3.0),(5.6,3.7),(6.2,3.4),(5.6,3.0)],closed=True,fc="#a8c79a",ec=INK,lw=0.6))
a.plot([5.2,6.5],[2.6,1.0],color="#b03a10",lw=1.4); a.text(7.2,1.0,"suture (IYSZ)",fontsize=6.4,color="#b03a10",ha="left")
a.annotate("",xy=(3.4,4.2),xytext=(1.0,4.2),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3)); a.text(2.0,2.5,"India",fontsize=7,ha="center"); a.text(8.4,2.7,"Tibet",fontsize=7,ha="center")
a=axs[1,1]; base(a,"(d) Present: thrusting and uplift (MCT, MBT, HFT)")
a.add_patch(mp.Polygon([(0,2),(1.5,2.2),(3.0,2.5),(4.0,3.2),(5.0,4.3),(6.0,5.0),(7.2,4.4),(10,4.0),(10,2),(0,2)],closed=True,fc=t1,ec=INK,lw=0.8))
for xb,yb,t in ((1.5,2.2,"HFT"),(3.0,2.5,"MBT"),(4.9,4.2,"MCT")):
    a.plot([xb,xb+2.0],[yb,yb-1.2],color="#b03a10",lw=1.2); a.text(xb,yb+0.3,t,fontsize=6.6,color="#b03a10",ha="center",fontweight="bold")
a.text(6.0,5.35,"Himalaya",fontsize=7,ha="center"); a.text(8.6,4.4,"Tibetan plateau",fontsize=6.6,ha="center"); a.text(0.8,2.5,"Ganga plain",fontsize=6.3,ha="center")
```


1. **Before collision (above 100 Ma).** India, once part of Gondwanaland, broke off about 130 Ma ago and moved north at up to 15–20 cm per year, across the **Tethys Sea**, in which thick marine sediments (the Tethys sediments) accumulated.
2. **Subduction (about 100–55 Ma).** The oceanic crust of the Tethys was subducted beneath the Tibetan (Eurasian) margin, forming a volcanic arc (the Transhimalayan batholith).
3. **Collision (about 55–50 Ma).** When the oceanic crust was consumed, the Indian continent met Eurasia. Because both are buoyant continental crust, neither could subduct fully: the crust **thickened**, the Tethys sediments were scraped up and folded, and the **Indus–Tsangpo suture** formed.
4. **Thrusting and uplift.** Continuing convergence (about 19 mm per year in Nepal) shortened the crust by hundreds of kilometres through **thrusting towards the south**: the **MCT** (about 25–20 Ma) lifted the Higher Himalaya, the **MBT** (about 10 Ma) lifted the Lesser Himalaya and the **HFT** (Pleistocene, still active) lifted the Siwalik hills. The **STDS** allowed the Higher Himalaya to move up relative to the Tethys zone. The molasse eroded from the rising range was deposited in the Gangetic foredeep (the Siwalik, now the Terai).
5. **Present.** The range is still rising (several mm per year), which explains the high earthquakes (Gorkha 2015) and the Mt Everest (8848 m) with marine fossil limestone near the summit.

[2 marks]

@s 3
**(a) Field identification of the three rock types.**

| Feature | Igneous | Sedimentary | Metamorphic |
|---|---|---|---|
| Origin | cooling and solidification of magma or lava | cementation and compaction of sediments | recrystallisation of older rock by heat and pressure |
| Texture and structure | crystalline, interlocking grains; massive, no layers; vesicles or glass in volcanic rocks | clastic grains or crystalline, **bedded (stratified)**; cemented | **foliated** (banded, schistose, slaty), or granular and sugary (marble, quartzite) |
| Fossils | none | **may contain fossils**, and ripple marks, cross-bedding and mud cracks | none (destroyed) |
| Minerals | quartz, feldspar, mica, olivine, pyroxene | quartz, clay, calcite, gypsum, mica | mica, garnet, kyanite, staurolite, chlorite |
| Hardness and feel | hard, dense | soft to medium; porous; fizzes with HCl (limestone); grains rub off (sandstone) | hard; rings; sheen of mica on foliation |
| Occurrence | volcanoes, dykes, sills and batholiths | basins, river and sea deposits; horizontal to gently dipping | mountain belts, thrust zones and around intrusions |

**(b) Granite, phyllite and limestone.**

| Property | (i) Granite | (ii) Phyllite | (iii) Limestone |
|---|---|---|---|
| **Rock group** | plutonic igneous (acidic) | low-grade foliated metamorphic (from shale or mudstone) | sedimentary (chemical, organic or clastic), mainly CaCO₃ |
| **Physical properties** | coarse, crystalline of quartz, feldspar and mica; light grey, pink or white; hard (Mohs 6–7), massive, specific gravity 2.6–2.7, takes a good polish | very fine grained, **silky or glossy sheen** on cleavage surfaces (sericite, chlorite); grey, green or silver; wavy foliation; soft to medium hardness (Mohs 3–4 in the foliation plane), SG 2.7–2.8 | fine to coarse grained, white, grey or yellowish, fossiliferous or oolitic; soft (Mohs 3); SG 2.6–2.7; **effervesces with dilute HCl**; soluble in rainwater |
| **Engineering properties** | compressive strength 100–250 MPa; porosity under 1 %, water absorption under 0.5 %; very durable, high abrasion and weathering resistance; jointed and may be weathered to grus | compressive strength 20–80 MPa and **strongly anisotropic**: low shear strength along foliation; slakes and weathers into soil; high deformability; poor aggregate | compressive strength 30–150 MPa (varies); porosity 1–15 %; moderately durable; **dissolves to form caves, sinkholes and cavities (karst)**; permeable along joints |
| **Engineering uses** | foundations and abutments of dams and bridges; coarse aggregate for concrete and road; building and facing stone, kerbs, monuments; tunnelling in sound rock | usually of limited use: fill, road sub-base, local roofing and flooring slabs; weak foundation and slope-failure problems (the Lesser Himalaya) and tunnelling with squeezing | raw material for **cement and lime**, aggregate, building and flooring stone, flux in iron and steel making, agricultural lime; dam sites need grouting against leakage |

@s 4
**(a) Strike direction.** The strike is perpendicular to the dip direction. The bed dips towards S 55°E, which is an azimuth of $180^\circ - 55^\circ = 125^\circ$. Hence the strike azimuth is $125^\circ - 90^\circ = 35^\circ$:

$$\boxed{\text{strike} = \text{N35°E (or S35°W)}, \text{ azimuth } 035^\circ\text{–}215^\circ}$$

```figure caption="Plan view: the bed dips towards S55°E, so the strike line is perpendicular to the dip direction, N35°E–S35°W (azimuth 035°–215°)."
import numpy as _np, matplotlib.patches as mp

da=125; sa=35
fig,ax=plt.subplots(figsize=(3.7,3.4)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3.4,3.4); ax.set_ylim(-3.1,3.3)
def v(az,r): return (r*_np.sin(_np.radians(az)), r*_np.cos(_np.radians(az)))
ax.plot([0,0],[-2.6,2.6],color=MUTED,lw=0.9,ls="--"); ax.text(0.12,2.7,"N",fontsize=9,fontweight="bold")
p1=v(sa,2.6); p2=v(sa+180,2.6); ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=ACCENT,lw=2.4)
ax.annotate("",xy=v(da,1.9),xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=2.2))
ax.add_patch(mp.Arc((0,0),2.0,2.0,theta1=90-sa,theta2=90,color=INK,lw=0.9)); t=v(sa/2.0,1.35); ax.text(t[0],t[1]+0.05,"35°",fontsize=8,ha="center")
ax.add_patch(mp.Arc((0,0),1.4,1.4,theta1=-90,theta2=90-da,color=INK,lw=0.9)); t=v((180+da)/2.0,1.05); ax.text(t[0]+0.25,t[1]-0.15,"55°",fontsize=8,ha="center")
ax.plot([0,0],[0,-2.6],color=MUTED,lw=0.9,ls="--"); ax.text(0.12,-2.85,"S",fontsize=9,fontweight="bold")
ax.plot([0],[0],"o",color=INK,ms=4)
q=v(sa,2.95); ax.text(q[0],q[1]+0.1,"strike line  N35°E",fontsize=7.6,ha="center",color=ACCENT)
r=v(da,2.35); ax.text(r[0]+0.1,r[1]-0.25,"dip direction  S55°E",fontsize=7.6,ha="left",color=SERIES[1])
```


**(b) Fold.** A **fold** is a **bend or wave-like curvature in originally flat (planar) rock layers**, produced by compressive (and sometimes shear) stress, mostly in the plastic state of the rock, during mountain building. Elements: the **limbs** (the two sides), **hinge (crest) line**, **axial plane** (divides the fold into halves), **plunge** and **amplitude**. The main types are the **anticline** (upfold, with the older beds in the core), the **syncline** (downfold, with younger beds in the core), the **monocline**, **symmetrical** and **asymmetrical**, **overturned**, **recumbent**, and **plunging** folds, **dome** and **basin**.

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


**Field identification criteria of a fault.**

1. **Displacement and discontinuity of beds, dykes, veins or ridges**: the same bed is found offset across a line, or the beds on the two sides do not match.
2. **Repetition or omission of strata** in the stratigraphic sequence (repetition in a reverse fault and omission in a normal fault, when seen along a traverse).
3. **Fault rocks along the plane**: fault breccia, fault gouge (clay-like crushed material), cataclasite and mylonite, often cemented or silicified.
4. **Slickensides, striations and grooves** (polished and scratched surfaces) on the fault plane, whose direction gives the direction of the last movement.
5. **Drag folds** (beds bent near the fault) and sudden changes in the dip and strike of beds across a line.
6. **Topographic evidence**: fault scarps, triangular facets, linear valleys and saddles, truncated spurs, offset streams, sag ponds, sudden break of slope, alignment of springs and hot springs along a line.
7. **Hydrological and vegetation evidence**: line of springs or seepages, sudden change in vegetation, and zones of shearing or mineralisation.


**Importance of faults in civil engineering.**

```figure caption="Fault types: a normal fault (hanging wall moves down, caused by tension), a reverse or thrust fault (hanging wall moves up, caused by compression; a thrust dips at less than 45°) and a strike-slip fault (horizontal displacement along the strike)."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(1,3,figsize=(6.4,2.3))
def base(a,t):
    a.set_xlim(-0.5,10.5); a.set_ylim(-1.0,7.0); a.set_aspect("equal"); a.axis("off"); a.set_title(t,fontsize=8)
ar=dict(arrowstyle="-|>",color="#b03a10",lw=1.6)
a=axs[0]; base(a,"Normal fault")
a.add_patch(mp.Polygon([(0,0),(3,0),(6,4),(0,4)],closed=True,fc="#e6b97a",ec=INK,lw=0.9))
a.add_patch(mp.Polygon([(3,0),(10,0),(10,3),(5.25,3)],closed=True,fc="#cf9a58",ec=INK,lw=0.9))
a.annotate("",xy=(6.9,2.0),xytext=(6.1,3.0),arrowprops=ar); a.text(8.2,1.3,"hanging wall",fontsize=6.3,ha="center"); a.text(1.7,1.2,"foot wall",fontsize=6.3,ha="center"); a.text(5,-0.7,"tension: hanging wall down",fontsize=6.2,ha="center")
a=axs[1]; base(a,"Reverse / thrust fault")
a.add_patch(mp.Polygon([(0,0),(3,0),(6,4),(0,4)],closed=True,fc="#e6b97a",ec=INK,lw=0.9))
a.add_patch(mp.Polygon([(3,0),(10,0),(10,5.2),(6.9,5.2)],closed=True,fc="#cf9a58",ec=INK,lw=0.9))
a.annotate("",xy=(7.6,4.6),xytext=(6.4,3.2),arrowprops=ar); a.text(8.3,1.6,"hanging wall",fontsize=6.3,ha="center"); a.text(1.7,1.2,"foot wall",fontsize=6.3,ha="center"); a.text(5,-0.7,"compression: hanging wall up",fontsize=6.2,ha="center")
a=axs[2]; base(a,"Strike-slip fault (plan)")
a.add_patch(mp.Rectangle((0.5,3.6),9,2.6,fc="#c9b79a",ec=INK,lw=0.9)); a.add_patch(mp.Rectangle((0.5,0.6),9,2.6,fc="#b9bec6",ec=INK,lw=0.9))
a.plot([0,10],[3.4,3.4],color="#b03a10",lw=2.0)
a.annotate("",xy=(8.0,5.0),xytext=(4.5,5.0),arrowprops=ar); a.annotate("",xy=(2.0,1.9),xytext=(5.5,1.9),arrowprops=ar); a.text(5,-0.7,"shear: blocks slide sideways",fontsize=6.2,ha="center")
```


1. **Dam and reservoir sites**: an active fault under or near a dam may rupture and cause the failure of the dam; faults cause leakage of the reservoir and shear zones are weak foundations. Reservoir-induced seismicity occurs along faults.
2. **Tunnels**: fault zones contain crushed, fractured rock (gouge and breccia) that **collapses, squeezes and brings heavy water inflow**; the tunnel must cross faults at a large angle, with heavy support and drainage.
3. **Slope stability**: faults are planes of weakness for landslides and rockfall; roads along fault zones (MBT and MCT) fail frequently.
4. **Earthquakes**: **active faults** (HFT, the Gorkha rupture) are the source of destructive earthquakes: the buildings, bridges and lifelines should be located at a safe distance from the trace, with seismic zoning.
5. **Foundation**: differential settlement and variable bearing capacity where rocks of different strength lie across a fault; a fault displaces the aquifer and the rock types.
6. **Groundwater and resources**: faults form conduits or barriers for groundwater (springs and hot springs) and control the location of ore deposits and petroleum traps.

@s 5
**(a) Erosional and depositional features formed by a river.**

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


**(b) Short notes.**

**Karst topography.** Karst is the **distinctive landscape formed by chemical solution of soluble rock, mainly limestone** (also dolomite and gypsum), by slightly acidic water (carbonic acid): CaCO₃ + H₂O + CO₂ → Ca(HCO₃)₂ (soluble). It needs soluble, well-jointed rock, a humid climate and a high relief for drainage. *Surface features*: **sinkholes (dolines)**, **uvalas** (merged sinkholes), **poljes** (large flat-floored basins), **karren or lapies** (grooved rock surface), **disappearing streams** and **blind valleys**. *Subsurface features*: **caves** and caverns, **stalactites** (hanging from the roof), **stalagmites** (growing from the floor), **columns**, and **underground streams** (Mahendra cave in Pokhara and Siddha cave of Nepal). *Engineering problems*: subsidence and collapse of the foundation, leakage of reservoirs and tunnels, unpredictable cavities, and groundwater contamination.

**Cirque.** A cirque (corrie, cwm) is an **armchair-shaped, steep-walled hollow at the head of a glaciated valley**, carved by a mountain glacier by plucking (freeze–thaw) and abrasion. It has a steep **headwall**, a gently sloping, over-deepened **floor** that often holds a small lake (**tarn**), and a **rock lip (threshold)** at the open side. Where two cirques meet back to back they leave a sharp, narrow ridge (**arête**), and where several cut a peak they leave a **horn (pyramidal peak)**, as with the Machhapuchhre. Cirques are widespread above 4000 m in the Nepal Himalaya (for example around Gokyo and Tilicho), and the associated hazards include the moraine-dammed glacial lakes (GLOF) and rock avalanches.

```figure caption="Left: karst features formed by solution of limestone (sinkhole, cave with stalactites and stalagmites, underground stream). Right: a cirque, the armchair-shaped hollow cut by a glacier at the head of a valley, with its steep headwall, over-deepened floor, tarn and lip."
import numpy as _np, matplotlib.patches as mp

fig,axs=plt.subplots(1,2,figsize=(6.4,2.8))
a=axs[0]; a.set_xlim(0,10); a.set_ylim(-0.5,6.5); a.axis("off"); a.set_title("Karst topography (limestone)",fontsize=8)
a.add_patch(mp.Polygon([(0,5),(2.5,5),(3.2,4.0),(3.9,5),(10,5),(10,0),(0,0)],closed=True,fc="#d8d2c0",ec=INK,lw=0.9))
a.add_patch(mp.Polygon([(0,5),(10,5),(10,5.3),(0,5.3)],closed=True,fc="#a8c79a",ec="none"))
a.add_patch(mp.Ellipse((6.2,2.0),5.2,1.9,fc="#f7f3e8",ec=INK,lw=0.9))
for xs in (4.3,5.3,6.4,7.3):
    a.plot([xs,xs],[2.9,2.4],color=INK,lw=1.6)
    a.plot([xs+0.2,xs+0.2],[1.1,1.5],color=INK,lw=1.6)
a.plot([0,10],[0.55,0.55],color="#4a90d9",lw=2.2)
a.text(3.2,5.5,"sinkhole\n(doline)",fontsize=6.6,ha="center"); a.text(6.2,1.9,"cave",fontsize=6.8,ha="center")
a.text(6.2,3.25,"stalactites",fontsize=6.2,ha="center"); a.text(6.3,0.82,"stalagmites",fontsize=6.2,ha="center"); a.text(5,0.1,"underground stream",fontsize=6.4,ha="center",color="#2c6aa8")
a.text(1.2,3.5,"soluble\nlimestone",fontsize=6.6,ha="center")
b=axs[1]; b.set_xlim(0,10); b.set_ylim(-0.5,6.5); b.axis("off"); b.set_title("Cirque (glacial)",fontsize=8)
xx=_np.array([0,1.2,2.2,3.0,3.6,4.8,6.0,7.0,10.0]); yy=_np.array([5.9,5.7,5.2,3.2,1.9,1.4,1.6,2.6,3.2])
b.fill_between(xx,0,yy,color="#cfcfcf",ec=INK,lw=0.9); b.plot(xx,yy,color=INK,lw=1.3)
b.fill_between([3.7,6.0],[1.9,1.45],[1.5,1.5],color="#4a90d9",alpha=0.0)
b.add_patch(mp.Ellipse((5.0,1.6),2.2,0.4,fc="#6ab0f0",ec=INK,lw=0.7)); b.text(5.0,0.8,"tarn (lake)",fontsize=6.6,ha="center")
b.text(1.5,6.2,"arete / peak",fontsize=6.6,ha="center"); b.text(2.0,4.0,"steep\nheadwall",fontsize=6.6,ha="center")
b.text(8.2,3.6,"threshold (lip)",fontsize=6.6,ha="center"); b.text(3.2,2.7,"ice",fontsize=7,color="#2c6aa8",ha="center")
```


@s 6
The Nepal Himalaya is divided from south to north into the **Terai, Sub-Himalaya (Siwalik), Lesser Himalaya, Higher Himalaya and Tibetan–Tethys Himalaya**, separated by the **HFT, MBT, MCT and STDS**.

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


**Engineering geological problems of each division:**

| Division | Engineering geological problems |
|---|---|
| **Terai** | Frequent flooding, shifting of river channels, bank cutting and sedimentation; thick soft soils with low bearing capacity and high settlement; high water table; liquefaction of loose sand during earthquakes (Terai is a deep foreland basin that amplifies shaking); arsenic in shallow groundwater; scarcity of rock for aggregate, so river boulders are mined. |
| **Sub-Himalaya (Churia)** | Weak, poorly consolidated sandstone, mudstone and conglomerate that weather quickly; gully erosion, landslides, debris flows and very high sediment yield (reservoir siltation); steeply dipping beds and shear zones along the HFT and MBT; squeezing and water inflow in tunnels; badlands; active faulting with earthquakes; piping and slaking of mudstone. |
| **Lesser Himalaya** | Highly folded, faulted and deeply weathered phyllite, schist and slate with low shear strength along foliation; most of the large landslides (translational and rotational) on road and hydropower projects; thick colluvium and residual soils; tunnelling problems (squeezing, shear zones, groundwater inflow); karst and solution cavities in limestone and dolomite; reservoir leakage; road-cut slope failures on the dip slopes; high seismic hazard (2015 Gorkha earthquake). |
| **Higher Himalaya** | Very steep, rugged terrain and deep gorges; hard but heavily jointed gneiss with rock falls, rockslides and toppling (for example the Jure landslide, 2014); rock avalanches, snow avalanches and glacier retreat; glacial lake outburst floods (GLOF) and debris flows; high seismicity near the MCT; high in-situ stress and rock bursts in deep tunnels; difficult access and short working season. |
| **Tibetan–Tethys Himalaya** | Arid, cold climate with frost shattering and freeze–thaw weathering; weak shale and thin-bedded limestone; large old landslides and talus; permafrost and solifluction at high altitude; active faults (STDS, Thakkhola graben); strong wind erosion; wide variation in rock strength; thin soil and slope instability on steep gorges such as Kali Gandaki. |


In general the problems are made worse by the active tectonics (large earthquakes), steep slopes and the intense monsoon, so that **landslides, floods, debris flows and earthquakes** control the planning of roads, dams, tunnels and settlements in Nepal. The geological mapping, slope stabilisation, bio-engineering and the earthquake-resistant design are the main remedies.

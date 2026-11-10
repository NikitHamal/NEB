---
file: NEBians-IOE-Past-Paper-Engineering-Geology-II-ENCE152-2083-Baishakh.pdf
subject: Engineering Geology II
level: BE · Year I / Part II
code: ENCE 152
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCE
time: 1½ hrs
marks: 30
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). BE Civil Engineering (BCE), Year I / Part II. Full marks 30, pass marks 12.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · The figures in the margin indicate Full Marks · Assume suitable data if necessary</small>

@q 1
Define aquifer. Differentiate between confined and unconfined aquifer. [[3]]

@q 2
Describe Hoek-Brown failure criterion. Discuss the importance of mechanical properties of rock in civil engineering. [[4]]

@q 3
Write down the importance of discontinuities characters that affect rock mass classification. Discuss the tunnel excavation methods and support system in rock mass class IV based on Rock Mass Rating (RMR) classification. [[4]]

@q 4
Define earthquake. How do you calculate earthquake magnitude (Richter Scale)? [[4]]

@q 5
What are the major engineering geological investigations carried out for the dam construction? Discuss the importance of core drilling for sub-surface geological investigation. [[6]]

@q 6
Discuss the stability analysis based on the following information. Hill slope: $120^\circ/38^\circ$; Joint set 1: $270^\circ/42^\circ$; Joint set 2: $140^\circ/56^\circ$; Friction angle: $28^\circ$. [[4]]

@q 7
Write short notes (Any Two): (a) Seismic Refraction Tomography (SRT); (b) Elastic Modulus; (c) Landslide Dam Outburst Flood (LDOF). [[5]]

<!-- SOLUTIONS -->

@s 1
**Aquifer.** An aquifer is a saturated geological formation (sand, gravel, fractured or karstified rock) that is permeable enough to store and transmit groundwater in usable quantities to wells and springs.

| Confined aquifer | Unconfined aquifer |
|---|---|
| Bounded above and below by impermeable layers (aquicludes) | Upper boundary is the water table, open to the atmosphere |
| Water is under pressure greater than atmospheric; the piezometric surface rises above the top of the aquifer | Water is at atmospheric pressure; the water table is the free surface |
| Recharged only in the distant outcrop area | Recharged directly by rainfall percolating from above |
| Well may be artesian (flowing) | Water level in a well equals the water table |
| Storage coefficient small ($10^{-5}$ to $10^{-3}$), released by compressibility | Storage coefficient = specific yield (0.05 to 0.30) |
| Less vulnerable to pollution | Highly vulnerable to pollution |

@s 2
**Hoek-Brown failure criterion.** An empirical criterion for the strength of intact rock and rock masses under triaxial stress. In terms of the major and minor effective principal stresses at failure,

$$\sigma_1' = \sigma_3' + \sigma_{ci}\left(m_b\frac{\sigma_3'}{\sigma_{ci}} + s\right)^a$$

where $\sigma_{ci}$ is the uniaxial compressive strength of the intact rock, and $m_b = m_i\exp\!\left(\dfrac{GSI - 100}{28 - 14D}\right)$, $s = \exp\!\left(\dfrac{GSI - 100}{9 - 3D}\right)$, $a = \tfrac12 + \tfrac16\left(e^{-GSI/15} - e^{-20/3}\right)$. Here $m_i$ is a rock-type constant (about 7 for shale, 17 for sandstone, 25 for granite), $GSI$ the Geological Strength Index (0 to 100) and $D$ the disturbance factor (0 for undisturbed, 1 for heavily blast-damaged). For intact rock $s = 1$, $a = 0.5$. Uniaxial compressive strength is $\sigma_c = \sigma_{ci}s^a$ and tensile strength $\sigma_t = -s\sigma_{ci}/m_b$. The criterion can be converted to equivalent Mohr-Coulomb $c$ and $\phi$ for slope and tunnel design.

**Importance of mechanical properties of rock in civil engineering.** They decide whether a rock can carry, resist or be excavated safely:

- *Compressive strength* (UCS): bearing capacity of foundations of dams, bridges and buildings; classification of rock strength; crushing strength of aggregate and building stone.
- *Tensile strength*: stability of tunnel roofs, cut slopes and rock beams; excavation and fracturing.
- *Shear strength* ($c$, $\phi$) of rock and discontinuities: slope stability, sliding of dam abutments and foundations.
- *Elastic constants* ($E$, $\nu$) and deformability: settlement of foundations, deformation of tunnels and underground caverns.
- *Density, porosity, water absorption, permeability*: self-weight loads, seepage under dams, durability.
- *Hardness, abrasion, toughness, durability and slake durability*: road aggregate and railway ballast, selection of drilling and excavation methods (drillability, TBM wear).

@s 3
**Importance of discontinuity characters in rock mass classification.** Rock masses fail mainly along discontinuities (joints, bedding, faults, foliation), so their character controls strength, deformability and permeability:

- *Orientation (dip and dip direction):* determines whether blocks can slide, topple or fall in a slope or tunnel (rated by the orientation adjustment).
- *Spacing and RQD:* give the block size; closer spacing means a weaker, more deformable mass.
- *Persistence:* continuous discontinuities make sliding surfaces.
- *Roughness and aperture:* control the shear strength and the water flow.
- *Infilling and weathering:* soft or clay infill and altered walls greatly reduce friction.
- *Water:* reduces effective stress and strength.

**Rock Mass Rating (RMR, Bieniawski 1989).** The rock mass is divided into structural regions and the following six parameters are rated and summed:

| Parameter | Maximum rating |
|---|---|
| 1. Uniaxial compressive strength of intact rock | 15 |
| 2. Rock Quality Designation (RQD) | 20 |
| 3. Spacing of discontinuities | 20 |
| 4. Condition of discontinuities (persistence, aperture, roughness, infilling, weathering) | 30 |
| 5. Groundwater (inflow, water pressure ratio) | 15 |
| 6. Adjustment for orientation of discontinuities (very favourable 0 to very unfavourable $-12$ for tunnels) | 0 to $-12$ |

$RMR = \sum(1 \text{ to } 5) + \text{adjustment}$ ($0$ to $100$).

| RMR | 81 to 100 | 61 to 80 | 41 to 60 | 21 to 40 | $<$ 20 |
|---|---|---|---|---|---|
| Class | I | II | III | IV | V |
| Description | Very good | Good | Fair | Poor | Very poor |
| Cohesion (kPa) | $>$ 400 | 300 to 400 | 200 to 300 | 100 to 200 | $<$ 100 |
| Friction angle | $>$ 45° | 35° to 45° | 25° to 35° | 15° to 25° | $<$ 15° |
| Stand-up time | 20 yr for 15 m span | 1 yr for 10 m | 1 week for 5 m | 10 h for 2.5 m | 30 min for 1 m |

**Tunnel excavation and support in Class IV (RMR 21 to 40, poor rock).** Short stand-up time (about 10 h for a 2.5 m span) means excavation and support must go together.

- *Excavation method:* top heading and bench with heading advance of $1.0$ to $1.5$ m (smaller rounds, controlled or mechanical excavation, short blast rounds).
- *Support installed concurrently with excavation:* complete support within $10$ m of the face.
- *Rock bolts:* systematically spaced $1.0$ to $1.5$ m, $4$ to $5$ m long, in the crown and walls, with wire mesh in the crown.
- *Shotcrete:* $100$ to $150$ mm in the crown and $100$ mm in the sides.
- *Steel ribs:* light to medium ribs spaced $1.5$ m where required.

@s 4
**Earthquake.** An earthquake is the sudden release of strain energy stored in the Earth's crust, usually by slip on a fault, which radiates as seismic waves (P, S, Love, Rayleigh) and shakes the ground. The point of rupture at depth is the focus (hypocentre) and the point on the surface vertically above it the epicentre.

**Richter (local) magnitude.** Richter defined

$$M_L = \log_{10}A - \log_{10}A_0(\delta)$$

where $A$ is the maximum trace amplitude (mm) on a Wood-Anderson seismograph and $A_0(\delta)$ the amplitude of a standard reference event ($M = 0$, amplitude $1\ \mu$m) at the same epicentral distance $\delta$. In practice, for a recording at distance $\delta$ determined from the S-P time difference $\Delta t$ (s), $\;M_L = \log_{10}A + 3\log_{10}(8\Delta t) - 2.92$. The scale is logarithmic: one unit increase means $10\times$ larger amplitude and about $31.6\times$ more energy, from $\log_{10}E = 1.5M + 4.8$ ($E$ in joules). Example: $A = 20$ mm at $\Delta t = 24$ s gives $M_L = 1.30 + 3(2.283) - 2.92 = 5.2$.

@s 5
**Engineering-geological investigations for a dam.**

1. *Regional and reservoir geology:* reconnaissance, geological mapping at scale 1:5000 to 1:1000 of the dam site and reservoir rim; lithology, structure (folds, faults, thrusts), regional seismicity.
2. *Topographic and geomorphological survey:* valley shape, terraces, river channel deposits, landslides on the reservoir slopes.
3. *Surface exploration:* test pits, trenches and adits to see the weathered zone, shear zones and abutment rock.
4. *Geophysical surveys:* seismic refraction and electrical resistivity to find bedrock depth, weathering profile and buried channels.
5. *Drilling and core logging:* boreholes along the axis, in the foundation, abutments and spillway/power-house sites.
6. *In-situ tests:* Lugeon (packer) permeability tests, plate load, borehole dilatometer, direct shear on discontinuities.
7. *Laboratory tests:* UCS, density, absorption, shear strength, petrography of rock; soil tests on foundation soils.
8. *Construction materials survey:* quarries for aggregates, clay core, sand and gravel.
9. *Reservoir investigations:* leakage paths, water tightness, rim stability, siltation, reservoir-induced seismicity.
10. *Groundwater and seepage conditions* at the site.

**Importance of core drilling.** Core drilling gives a continuous undisturbed sample of the sub-surface, from which we get: the sequence and thickness of rock and overburden; depth to sound bedrock and depth of weathering (foundation level); RQD, fracture frequency and discontinuity condition; shear zones, cavities and weak seams; samples for laboratory strength tests; water-pressure (Lugeon) tests in the same hole for permeability and grouting design; piezometer and groundwater observation; and a permanent record for design and contract disputes. A reliable log requires a double-tube core barrel with core recovery above 85 percent.

@s 6
**Stability analysis (kinematic, stereographic).** Data (dip direction / dip): hill slope $120^\circ/38^\circ$, joint set 1 $J_1 = 270^\circ/42^\circ$, joint set 2 $J_2 = 140^\circ/56^\circ$, friction angle $\phi = 28^\circ$.

**1. Plane failure** needs: (a) the plane dips in nearly the same direction as the slope face (within $\pm20^\circ$); (b) the plane daylights, $\psi_p < \psi_f$ (dip of plane less than dip of face); (c) $\psi_p > \phi$.

- $J_1$: dip direction $270^\circ$ differs from the face ($120^\circ$) by $150^\circ$, so it dips into the hill: **no plane failure**.
- $J_2$: dip direction $140^\circ$ is within $20^\circ$ of the face, but its dip $56^\circ$ is greater than the slope dip $38^\circ$ (it does not daylight): **no plane failure**.

**2. Wedge failure** (intersection of $J_1$ and $J_2$). Line of intersection from the cross product of the poles: trend $031.5^\circ$, plunge $25.2^\circ$. Condition for sliding: the line must daylight in the face ($\psi_i < \psi_f$: $25.2^\circ < 38^\circ$ satisfied, but its trend is almost parallel to the strike of the face, $88.5^\circ$ from the dip direction, so it only just emerges) and $\psi_i > \phi$. Here $\psi_i = 25.2^\circ < \phi = 28^\circ$, so the wedge is held by friction: **stable**. Factor of safety (frictional, dry) $\approx \dfrac{\tan\phi}{\tan\psi_i} = \dfrac{\tan28^\circ}{\tan25.2^\circ} = 1.13$ (marginal, so it must be checked in the wet condition).

**3. Toppling** needs planes dipping steeply into the face (dip direction $\approx$ face dip direction $\pm180^\circ\pm10^\circ$) with $\psi_p \ge 90^\circ - (\psi_f - \phi) = 80^\circ$. $J_1$ is $150^\circ$ off ($30^\circ$ from the exact opposite) and dips only $42^\circ$; $J_2$ dips along the face; **no toppling**.

**Conclusion.** None of the three modes is kinematically possible: the slope is stable in the dry condition. Because the wedge factor of safety is only about $1.1$, steepening the cut above $38^\circ$ or heavy rain (water pressure) could change this, so provide drainage (surface drains, horizontal drains), protect the toe and monitor.

```figure caption="Equal-angle (lower hemisphere) stereonet: great circles of the slope face, $J_1$ and $J_2$, the intersection line (plunge $25.2^\circ$, trend $031.5^\circ$) and the friction circle ($28^\circ$). The intersection lies inside the friction circle, so the wedge does not slide."
import numpy as np, matplotlib.pyplot as plt
def pl(dd,dip):
    a,d=np.radians(dd),np.radians(dip); s=np.radians(dd-90)
    t=np.linspace(0,np.pi,200); X=[];Y=[]
    for u in t:
        v=np.cos(u)*np.array([np.sin(s),np.cos(s),0])+np.sin(u)*np.array([np.sin(a)*np.cos(d),np.cos(a)*np.cos(d),-np.sin(d)])
        p=np.arcsin(-v[2]); tr=np.arctan2(v[0],v[1]); r=np.tan(np.pi/4-p/2); X.append(r*np.sin(tr)); Y.append(r*np.cos(tr))
    return X,Y
def pt(tr,pg):
    r=np.tan(np.radians(45-pg/2)); return r*np.sin(np.radians(tr)), r*np.cos(np.radians(tr))
fig,ax=plt.subplots(figsize=(3.6,3.6))
c=np.linspace(0,2*np.pi,300); ax.plot(np.sin(c),np.cos(c),color=INK,lw=1)
ax.plot(*pl(120,38),color=INK,lw=1.3,label="slope face")
ax.plot(*pl(270,42),color=ACCENT,lw=1.3,label="J1 270/42")
ax.plot(*pl(140,56),color=SERIES[1],lw=1.3,label="J2 140/56")
ax.plot(*[np.tan(np.radians(45-28/2))*f(c) for f in (np.sin,np.cos)],ls=':',color=INK,lw=0.9)
ax.annotate("friction circle",(0,np.tan(np.radians(45-28/2))),textcoords="offset points",xytext=(2,2),fontsize=6.5)
ax.plot(*pt(31.5,25.2),"o",color=SERIES[2],ms=4,label="J1-J2 line 031.5/25.2")
ax.annotate("N",(0,1.02),ha='center',fontsize=8); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.1,1.1); ax.set_ylim(-1.1,1.1); ax.legend(fontsize=6.5,loc='lower right')

```

@s 7
All three are answered (any two are required).

**Seismic Refraction Tomography (SRT).** A seismic source (hammer, weight drop, small explosive) generates P-waves that travel through the ground; the first arrival times at a line of geophones are recorded. Where velocity increases with depth, waves refract along the layer interface and return as head waves. Unlike classical refraction, tomography inverts all first-arrival times (using ray tracing and iteration) to produce a 2-D velocity section $V_p(x,z)$ with smooth lateral and vertical velocity variation. Uses: depth to bedrock and weathering, rippability and excavation classification, faults and shear zones, landslide slip surface, tunnel portals, dam foundations and groundwater table. It cannot see low-velocity layers beneath high-velocity layers (hidden layer problem).

**Elastic modulus.** The elastic (Young's) modulus $E = \sigma/\varepsilon$ is the slope of the linear part of the stress-strain curve of rock, the measure of stiffness. It is determined in the laboratory from UCS tests on cores as the tangent modulus at 50 percent of the peak stress ($E_{t50}$), the secant modulus, or from the average slope; and in-situ by plate-load, dilatometer or flat-jack tests ($E_m$, the deformation modulus of the rock mass, which is much smaller than the intact $E$ because of discontinuities) and by seismic velocities ($E_d = \rho V_s^2\,\dfrac{3V_p^2 - 4V_s^2}{V_p^2 - V_s^2}$). Typical values: granite 50 to 70 GPa, sandstone 5 to 30 GPa, shale 1 to 20 GPa. It is used to calculate settlement of foundations, deformation of tunnels and abutments, and in rock-mass classification ($E_m = 2RMR - 100$ GPa for $RMR > 50$).

**Glacial Lake Outburst Flood (GLOF) / Landslide Dam Outburst Flood (LDOF).** A *GLOF* is the sudden release of water from a glacial lake dammed by a moraine or ice, triggered by an ice or rock avalanche into the lake, an earthquake, a piping failure, or melting of ice cores. Peak discharges many times the normal flow travel tens to hundreds of kilometres downstream, carrying debris (e.g. the 1985 Dig Tsho event destroyed the Namche small hydropower project; Tsho Rolpa and Imja are among the most dangerous lakes). An *LDOF* occurs when a river blocked by a landslide or rock avalanche forms a lake that overtops or breaches the natural dam (e.g. Kali Gandaki landslide dam 1988, Jure 2014, the Melamchi flood 2021). Both give very rapid, sediment-laden floods, very destructive to dams, bridges and settlements. Mitigation: monitoring, early warning, siphoning or controlled lowering of the lake, spillways, and hazard zoning and risk-sensitive siting.

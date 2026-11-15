---
file: NEBians-IOE-Past-Paper-Soil-Mechanics-ENCE253-2083-Baishakh.pdf
subject: Soil Mechanics
level: BE · Year II / Part II
code: ENCE 253
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Civil, Year II / Part II. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define alluvial and colluvial soil. What are the recent developments in Soil Mechanics? [[2]]

b) Differentiate between flocculated and dispersed structure. [[2]]

c) Explain the structure of Montmorillonite with diagram. [[2]]

@q 2
a) Define $D_{10}$, $D_{30}$ and $D_{60}$ with the help of gradation curve. Why are $C_u$ and $C_c$ important? What is the value of $C_u$ for a soil with only one grain size? [[2]]

b) An undisturbed sample of clay brought from field was noted to have a volume of 18 cc and weight of 30.8 gm. On oven drying the weight of sample was reduced to 20.5 gm. The volume of dried sample as obtained by displacement of mercury was 12.5 cc. Calculate shrinkage limit, specific gravity and shrinkage ratio. [[4]]

c) Three soils A, B and C are mixed in proportion of 20%, 30% and 50% respectively by mass. The specific gravity of soils A, B and C are 2.5, 2.6 and 2.7 respectively. If the bulk density of mixed soil is 2.0 g/cc at 20% water content, determine void ratio and degree of saturation. [[4]]

d) Describe field identification procedure of soil. [[2]]

@q 3
a) Describe different laboratory and field methods of determination of permeability and their significance. [[4]]

b) An earth dam is built on an impervious foundation with a horizontal filter at the base near toe. The permeability of the soil in the horizontal and vertical directions are $4\times10^{-2}$ mm/s and $2\times10^{-2}$ mm/s respectively. The height of water and free board are 35 m and 5 m respectively. If top width is 10 m, side slope is 2H:1V and the length of drainage is 15 m. Estimate the seepage loss per meter length of dam. [[4]]

@q 4
a) What are the factors affecting effective stress, and explain one of them, showing a stress diagram? [[3]]

b) Determine the vertical stress at point P due to strip load as shown in figure. [[3]]

```figure caption="Question 4(b): a strip load q = 200 kN/m² of width 5 m; point P lies 5 m below the ground surface and its vertical line is 5 m from the near edge of the strip (dimensions as read from the scan)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.2,2.7)); ax.axis("off")
ax.add_patch(mp.Rectangle((5,0),5,0.35,fc="#555",ec=INK))
for x in np.linspace(5.4,9.6,6): ax.annotate("",xy=(x,0.4),xytext=(x,1.1),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.1))
ax.text(7.5,1.25,"q = 200 kN/m²",ha="center",fontsize=9)
ax.plot([-1,12],[0,0],color=INK,lw=1.2)
ax.plot([0,0],[0,-5],color=INK,lw=1.2,ls="--"); ax.plot([0],[-5],"o",color="#d9534f",ms=6); ax.text(0.3,-5.1,"P",fontsize=10)
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(0,-0.7),xytext=(5,-0.7),arrowprops=ar); ax.text(2.5,-1.1,"5 m",ha="center",fontsize=8.5)
ax.annotate("",xy=(5,-0.7),xytext=(10,-0.7),arrowprops=ar); ax.text(7.5,-1.1,"5 m",ha="center",fontsize=8.5)
ax.annotate("",xy=(-0.6,0),xytext=(-0.6,-5),arrowprops=ar); ax.text(-0.9,-2.5,"5 m",rotation=90,va="center",ha="center",fontsize=8.5)
ax.plot([0,5],[-5,0],color=MUTED,lw=0.8,ls=":"); ax.plot([0,10],[-5,0],color=MUTED,lw=0.8,ls=":")
ax.set_xlim(-1.5,12); ax.set_ylim(-5.6,1.8)
```

c) Describe Newmark's chart and its application. [[2]]

@q 5
a) Write the assumption of Terzaghi's one-dimensional consolidation theory. A soil sample 20 mm thick takes 20 minutes to reach 20% consolidation. Find the time taken for a 4 m thick clay layer to reach 40% consolidation. Assume double drainage for both cases. [[1+3]]

b) Why is it necessary to accelerate consolidation? Should it be done before or after construction? How can it be done? [[2]]

c) Explain the method to determine preconsolidation pressure. [[2]]

@q 6
a) Explain direct shear test and its data presentation and interpretation. [[2+3]]

b) An unconfined compression test was carried on a saturated clay soil sample. The maximum load clay sustained was 150 N and the vertical displacement was 0.7 mm. The size of the sample was 38 mm diameter and 76 mm long. Determine the undrained shear strength. Draw Mohr's circle of stress for the test and locate undrained shear strength ($C_u$). [[3]]

c) List out merits and demerits of triaxial test. [[2]]

d) What is cyclic shear strength? What is its importance in geotechnical engineering? [[2]]

@q 7
a) Discuss the effects of compaction on soil characteristics. [[2]]

b) In a standard proctor test on a soil having a specific gravity of 2.6, the following results were obtained. [[4]]

| Water content (%) | 5 | 8 | 10 | 12 | 16 | 20 |
|---|---|---|---|---|---|---|
| Bulk density (kg/m³) | 1890 | 2130 | 2200 | 2210 | 2160 | 2080 |

Plot the dry density versus water content curve in a graph. Also, show the zero-air void line on the same curve. Determine the values of void ratio, porosity, and degree of saturation for the soil at the optimum moisture content condition.

<!-- SOLUTIONS -->

@s 1
**(a) Alluvial and colluvial soils.**

- **Alluvial soil** is a *transported* soil carried by running water (rivers and streams) and deposited on flood plains, river terraces, deltas and in river channels. It is stratified, with rounded and well-sorted grains (gravel and sand in the channel, silt and clay on the flood plain). The Terai plain of Nepal and the Ganga plain are alluvial deposits.
- **Colluvial soil** is a transported soil moved only by *gravity* (landslides, soil creep, rain-wash, rock fall) and deposited at the foot or on the lower part of a slope. It is angular, unsorted, loose and heterogeneous, with boulders mixed with silt and clay. Hill slopes and landslide debris in Nepal's Mahabharat and Siwalik zones are colluvial. It is a frequent source of slope failure.

**Recent developments in Soil Mechanics:**

1. Critical state soil mechanics and advanced constitutive models (Cam-clay, hardening-soil, bounding-surface models).
2. Unsaturated soil mechanics (matric suction, soil–water characteristic curve).
3. Numerical modelling: finite element, finite difference and discrete element programs (PLAXIS, GeoStudio, FLAC) for deformation, seepage and slope stability.
4. In-situ testing and monitoring: piezocone (CPTu), flat dilatometer, seismic cone, shear-wave velocity and geophysical (ERT, MASW) methods.
5. Ground improvement and reinforced soil: geosynthetics, prefabricated vertical drains, stone columns, deep soil mixing, dynamic compaction.
6. Earthquake geotechnics, liquefaction assessment, and landslide hazard mapping using GIS and remote sensing.
7. Centrifuge and physical modelling, geo-environmental engineering (landfill liners, contaminant transport), and probabilistic / reliability-based design and machine learning in geotechnics.

**(b) Flocculated and dispersed structure.**

| Property | Flocculated structure | Dispersed structure |
|---|---|---|
| Particle arrangement | Edge-to-face / edge-to-edge contact, "card-house" | Face-to-face, parallel orientation |
| Cause | Net attraction: high electrolyte concentration, low pH, salt water | Net repulsion: low electrolyte concentration, fresh water, dispersing agent |
| Void ratio | High, open, large voids | Low, dense |
| Strength | Higher, strongly bonded, sensitive to disturbance | Lower, strength gained on remoulding is small |
| Permeability | Higher | Lower |
| Compressibility | Higher on loading, but stiffer at small strain | Lower |
| Example | Marine clays, compacted dry of optimum | Lacustrine clay, compacted wet of optimum |

**(c) Structure of Montmorillonite.** Montmorillonite (smectite group) is a **2:1** clay mineral. Each unit layer is made of one **octahedral (gibbsite, Al–OH) sheet sandwiched between two tetrahedral (silica) sheets**, with the tips of both silica sheets pointing towards the central octahedral sheet. The layer is about 0.96 nm (9.6 Å) thick. Successive layers are held together only by very weak **van der Waals forces and oxygen–oxygen bonds**, so water and exchangeable cations (Na⁺, Ca²⁺) can enter between them and the lattice **expands** (basal spacing varies from 9.6 Å to complete separation). Isomorphous substitution of Mg²⁺ for Al³⁺ in the octahedral sheet gives a high negative charge, which is balanced by the interlayer cations. Consequently montmorillonite has very high specific surface (about 800 m²/g), cation-exchange capacity (80–150 meq/100 g), liquid limit (100–900 %), swelling and shrinkage. Bentonite is largely montmorillonite.

```figure caption="Structure of montmorillonite: a 2:1 layer (silica – gibbsite – silica) with weak, expandable interlayer bonding (water and exchangeable cations)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,3.1)); ax.axis("off")
def layer(y0):
    ax.add_patch(mp.Rectangle((0,y0),8,0.55,fc="#f2d9a0",ec=INK,lw=0.8)); ax.add_patch(mp.Rectangle((0,y0+0.55),8,0.55,fc="#9fc5e8",ec=INK,lw=0.8)); ax.add_patch(mp.Rectangle((0,y0+1.1),8,0.55,fc="#f2d9a0",ec=INK,lw=0.8))
layer(0); layer(3.2)
ax.text(4,0.27,"silica sheet (tetrahedral)",ha="center",va="center",fontsize=7.5); ax.text(4,0.82,"gibbsite sheet (octahedral)",ha="center",va="center",fontsize=7.5); ax.text(4,1.37,"silica sheet (tetrahedral)",ha="center",va="center",fontsize=7.5)
ax.text(4,3.47,"silica sheet",ha="center",va="center",fontsize=7.5); ax.text(4,4.02,"gibbsite sheet",ha="center",va="center",fontsize=7.5); ax.text(4,4.57,"silica sheet",ha="center",va="center",fontsize=7.5)
rng=np.random.default_rng(3)
ax.scatter(rng.uniform(0.3,7.7,14),rng.uniform(1.95,2.9,14),s=14,c="#d9534f"); ax.text(8.2,2.4,"water + exchangeable\ncations (Na$^+$, Ca$^{2+}$)\nweak bond, expands",fontsize=7.5,va="center")
ax.annotate("",xy=(-0.3,1.65),xytext=(-0.3,0),arrowprops=dict(arrowstyle="<->",lw=0.8)); ax.text(-0.45,0.8,"≈ 9.6 Å",rotation=90,ha="right",va="center",fontsize=7.5)
ax.set_xlim(-1.2,11.8); ax.set_ylim(-0.3,4.9)
```

@s 2
**(a) Particle-size definitions.** On the gradation (particle-size distribution) curve, plotted as percent finer against log grain size:

- $D_{10}$ = effective size: the particle size below which 10 % of the soil by mass is finer;
- $D_{30}$ = the size below which 30 % is finer;
- $D_{60}$ = the size below which 60 % is finer.

```figure caption="Gradation curve with D10, D30 and D60 read off at 10 %, 30 % and 60 % finer (illustrative soil)."
fig,ax=plt.subplots(figsize=(5.0,2.9))
d=np.array([0.02,0.06,0.2,0.6,2,6,20]); p=np.array([2,8,25,52,75,92,100])
ax.semilogx(d,p,color=ACCENT,lw=2,marker="o",ms=4)
for pc,lab in [(10,"D$_{10}$"),(30,"D$_{30}$"),(60,"D$_{60}$")]:
    dd=10**np.interp(pc,p,np.log10(d)); ax.plot([0.01,dd,dd],[pc,pc,0],color="#d9534f",lw=0.9,ls="--"); ax.text(dd*1.08,pc-7,lab,fontsize=8.5,color="#d9534f")
ax.set_xlim(0.01,30); ax.set_ylim(0,100); ax.set_xlabel("particle size (mm), log scale",fontsize=8.5); ax.set_ylabel("percent finer",fontsize=8.5); ax.grid(True,which="both",color=GRID,lw=0.6)
```

$$\begin{gathered}C_u=\frac{D_{60}}{D_{10}}\ \text{(uniformity coefficient)} \\ C_c=\frac{D_{30}^{\,2}}{D_{10}\,D_{60}}\ \text{(coefficient of curvature)}\end{gathered}$$

*Importance.* $C_u$ measures the range of sizes (slope of the curve) and $C_c$ the smoothness of its shape. Together they classify a coarse soil as well graded or poorly graded: clean gravel is well graded if $C_u\ge4$ and $1\le C_c\le3$, and clean sand if $C_u\ge6$ and $1\le C_c\le3$. Well-graded soils compact to a high density, have high strength and low compressibility, and make good fill and filter material; $D_{10}$ also controls permeability (Hazen: $k=C D_{10}^2$).

*Single grain size.* If every grain has the same size, $D_{60}=D_{10}$, so $\boldsymbol{C_u=1}$ (a perfectly uniform soil).

**(b) Shrinkage limit, shrinkage ratio and specific gravity.** Given $V_1=18$ cc, $W_1=30.8$ g, $W_d=20.5$ g, $V_d=12.5$ cc.

$$w_1=\frac{W_1-W_d}{W_d}=\frac{30.8-20.5}{20.5}=50.24\%$$

$$w_s=w_1-\frac{(V_1-V_d)\,\rho_w}{W_d}\times100=50.24-\frac{(18-12.5)(1)}{20.5}\times100=\boxed{23.41\%}$$

$$\boxed{SR=\frac{W_d}{V_d\,\rho_w}=\frac{20.5}{12.5}=1.64}$$

Since $\dfrac1G=\dfrac1{SR}-\dfrac{w_s}{100}$,

$$\frac1G=\frac1{1.64}-0.2341=0.6098-0.2341=0.3757\ \Rightarrow\ \boxed{G=2.66}$$

**(c) Mixed soil.** For mixing by mass, the specific gravity of the mixture follows from $\dfrac{1}{G}=\sum\dfrac{p_i}{G_i}$:

$$\frac1{G_m}=\frac{0.20}{2.5}+\frac{0.30}{2.6}+\frac{0.50}{2.7}=0.0800+0.1154+0.1852=0.3806\ \Rightarrow\ G_m=2.628$$

Dry density from the bulk density $\rho=2.0$ g/cc and $w=0.20$:

$$\rho_d=\frac{\rho}{1+w}=\frac{2.0}{1.20}=1.667\ \text{g/cc}$$

$$\boxed{e=\frac{G_m\rho_w}{\rho_d}-1=\frac{2.628}{1.667}-1=0.577}$$

$$\boxed{S=\frac{wG_m}{e}=\frac{0.20(2.628)}{0.5766}=0.911=91.1\%}$$

**(d) Field identification of soil.** Simple tests on a hand sample, as in IS 1498 / ASTM D2488 (visual–manual procedure):

1. *Visual:* colour, odour, and whether grains can be seen with the naked eye. If more than half the particles are visible (> 0.075 mm) the soil is coarse-grained (gravel, sand); otherwise fine-grained (silt, clay). Note angularity, gradation, and presence of organic matter (dark colour, musty smell).
2. *Dry strength test:* a moist pat is dried and crushed. None to low: silt; medium to high: clay.
3. *Dilatancy (shake) test:* a wet pat is shaken in the palm and squeezed. Water appears quickly and vanishes on squeezing: silt (rapid reaction); no reaction: clay.
4. *Toughness (thread) test:* the soil is rolled into a 3 mm thread near the plastic limit. A tough thread and stiff lump indicates clay of high plasticity; weak, crumbling thread indicates silt.
5. *Feel and sedimentation:* gritty feel indicates sand; smooth, soapy and sticky indicates clay; a jar test settles sand in 30 s, silt in about 1 hour and clay over hours or days.
6. *Organic / peat:* spongy, fibrous, dark brown or black material with a strong smell.

@s 3
**(a) Determination of permeability.**

*Laboratory methods*

- **Constant-head test** for clean sands and gravels ($k>10^{-3}$ cm/s): $k=\dfrac{QL}{Aht}$.
- **Falling-head test** for silts and clays ($10^{-3}$ to $10^{-7}$ cm/s): $k=\dfrac{aL}{At}\ln\dfrac{h_1}{h_2}$.
- **Indirect methods**: from the consolidation test ($k=c_v\,m_v\gamma_w$), from grain size (Hazen: $k=C D_{10}^2$) and from capillary-rise test.

*Field methods*

- **Pumping-out test** (large-scale, most reliable): water is pumped at a steady rate from a well with observation wells at $r_1$, $r_2$. For an unconfined aquifer $k=\dfrac{2.303\,q\log(r_2/r_1)}{\pi(h_2^2-h_1^2)}$; for a confined aquifer $k=\dfrac{2.303\,q\log(r_2/r_1)}{2\pi D(h_2-h_1)}$.
- **Pumping-in test** (borehole infiltration, packer test) for rock and soil above the water table.
- **Auger-hole and piezometer tests** for shallow ground-water conditions.

*Significance.* Permeability governs the quantity of seepage under dams and through embankments, uplift and piping, the rate of consolidation settlement ($c_v=k/m_v\gamma_w$), the design of drains, filters and dewatering systems, the design of landfill liners, and the stability of slopes and excavations.

**(b) Seepage through the earth dam (Casagrande's solution).**

*Geometry.* Dam height $=35+5=40$ m; crest width 10 m; both slopes 2H:1V. Base width $=10+2(40)(2)=170$ m. The upstream face meets the reservoir level (35 m) at a horizontal distance $2(35)=70$ m from the upstream toe. The horizontal filter is 15 m long, from $x=155$ m to the downstream toe at $x=170$ m, so the focus of the parabola is $F$ at $x=155$ m.

*Anisotropy.* Transform to an equivalent isotropic section by scaling horizontal distances with $\sqrt{k_z/k_x}=\sqrt{2/4}=0.7071$, and use the equivalent permeability

$$k'=\sqrt{k_xk_z}=\sqrt{(4\times10^{-2})(2\times10^{-2})}=2.83\times10^{-2}\ \text{mm/s}=2.83\times10^{-5}\ \text{m/s}$$

*Transformed distances.* Entry point of water on the upstream face $E$: $70(0.7071)=49.50$ m; Casagrande's point $A$ lies $0.3$ of the horizontal projection of the wetted upstream slope beyond $E$, so $x'_A=49.50+0.3(49.50)\approx64.35$ m, and the focus is at $x'_F\approx109.60$ m ($155\times0.7071$). Hence

$$\begin{gathered}d=x'_F-x'_A=109.60-64.35=45.25\ \text{m} \\ H=35\ \text{m}\end{gathered}$$

*Basic parabola with focus $F$ passing through $A$:*

$$y_0=\sqrt{d^2+H^2}-d=\sqrt{45.25^2+35^2}-45.25=57.20-45.25=11.96\ \text{m}$$

The discharge equals $k'$ times the ordinate of the parabola at the focus ($q=k'y_0$):

$$q=k'y_0=(2.83\times10^{-5})(11.96)=3.38\times10^{-4}\ \text{m}^3/\text{s per m}$$

$$\boxed{q\approx3.4\times10^{-4}\ \text{m}^3/\text{s per metre}\ \approx 29\ \text{m}^3/\text{day per metre length of dam}}$$

```figure caption="Transformed section of the dam (horizontal scale × 0.7071): Casagrande's basic parabola with focus F at the start of the horizontal filter; A is 0.3 of the wetted upstream projection beyond the entry point E."
import matplotlib.patches as mp
f=0.7071
fig,ax=plt.subplots(figsize=(5.8,2.8)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Polygon([[0,0],[80*f,40],[90*f,40],[170*f,0]],fc="#e8dcc4",ec=INK,lw=1.2))
ax.add_patch(mp.Polygon([[0,0],[70*f,35],[-8,35],[-8,0]],fc="#cfe3f5",ec="none"))
ax.plot([-8,70*f],[35,35],color=ACCENT,lw=1.3); ax.text(-7,36.5,"reservoir level (H = 35 m)",fontsize=7.5,color=ACCENT)
y0=11.955; y=np.linspace(y0,35,60); xF=155*f; xs=xF-(y**2-y0**2)/(2*y0)
ax.plot(xs,y,color="#d9534f",lw=1.6); ax.plot([49.5,xs[-1]],[35,35],color="#d9534f",lw=0.8)
ax.plot([62,xs[-12]],[31.6,y[-12]],color="#d9534f",lw=1.0,ls="--")
ax.add_patch(mp.Rectangle((xF,0),170*f-xF,2.2,fc="#7a8a99",ec=INK,lw=0.8)); ax.text(xF+2,-4.5,"filter (15 m → 10.6 m)",fontsize=7.5)
for nm,(px,py) in {"E":(49.5,35),"A":(64.35,35),"F":(xF,0)}.items(): ax.plot([px],[py],"o",color=INK,ms=3.5); ax.text(px,py+2.2 if nm!="F" else py-4.5,nm,fontsize=9,ha="center")
ax.annotate("",xy=(64.35,-8),xytext=(xF,-8),arrowprops=dict(arrowstyle="<->",lw=0.8)); ax.text((64.35+xF)/2,-12.5,"d = 45.25 m",fontsize=8,ha="center")
ax.text(xF+8,y0+3,"y$_0$ = 11.96 m",fontsize=8,color="#d9534f")
ax.set_xlim(-10,125); ax.set_ylim(-15,46)
```

@s 4
**(a) Factors affecting effective stress.** The effective stress $\sigma'=\sigma-u$ at a point in a soil mass depends on:

1. *Position of the water table:* a rise reduces $\sigma'$ (soil goes from moist to buoyant unit weight, and pore pressure increases); a fall increases it, causing settlement.
2. *Capillary rise* above the water table: negative pore pressure $u=-\gamma_wh_c$ increases $\sigma'$ (apparent cohesion in sands and silts).
3. *Seepage:* upward flow reduces $\sigma'$ (to zero at the critical gradient, quick condition); downward flow increases $\sigma'$.
4. *Surcharge and loads* from structures, fills and excavations (change of total stress, and of $u$ until consolidation is complete).
5. *Unit weight of soil* and degree of saturation, and flooding or drawdown of a reservoir (rapid drawdown).

*Explained: rise of the water table.* Take a sand with unit weights $\gamma$ above and $\gamma_{sat}$ below the water table, at depth $z_1$ from the ground surface. At depth $z$ below the table:

$$\begin{gathered}\sigma=\gamma z_1+\gamma_{sat}z \\ u=\gamma_wz \\ \sigma'=\gamma z_1+\gamma'z\quad(\gamma'=\gamma_{sat}-\gamma_w)\end{gathered}$$

If the water table rises to the surface ($z_1=0$) the effective stress at depth $z$ drops from $\gamma z$ to $\gamma' z$, a reduction of about 40 %. This is the cause of loss of bearing capacity during floods.

```figure caption="Stress diagrams for a soil with the water table at depth z1: total stress σ, pore pressure u and effective stress σ' = σ − u."
fig,axs=plt.subplots(1,3,figsize=(5.8,2.5),sharey=True)
z1,z2=3,7; g,gs,gw=17,20,9.81
zz=np.array([0,z1,z2]); sig=np.array([0,g*z1,g*z1+gs*(z2-z1)]); u=np.array([0,0,gw*(z2-z1)])
for ax,v,t in zip(axs,[sig,u,sig-u],["total σ","pore u","effective σ'"]):
    ax.plot(v,-zz,color=ACCENT,lw=1.8); ax.fill_betweenx(-zz,0,v,color=ACCENT,alpha=0.15); ax.axhline(-z1,color="#d9534f",lw=0.8,ls="--"); ax.set_title(t,fontsize=8.5); ax.tick_params(labelsize=7); ax.grid(True,color=GRID,lw=0.5)
axs[0].set_ylabel("depth (m)",fontsize=8); axs[0].text(2,-z1+0.3,"W.T.",fontsize=7.5,color="#d9534f")
for ax in axs: ax.set_xlabel("kN/m²",fontsize=7.5)
fig.tight_layout()
```

**(b) Vertical stress at P due to the strip load.** For a strip of width $B$ and intensity $q$, the vertical stress at a point is

$$\Delta\sigma_z=\frac{q}{\pi}\bigl[(\theta_2-\theta_1)+(\sin\theta_2\cos\theta_2-\sin\theta_1\cos\theta_1)\bigr]$$

where $\theta_1,\theta_2$ are the angles from the vertical through P to the near and far edges. With $z=5$ m, near edge at $x_1=5$ m, far edge at $x_2=10$ m:

$$\begin{gathered}\theta_1=\tan^{-1}\frac55=45^\circ \\ \theta_2=\tan^{-1}\frac{10}{5}=63.43^\circ\end{gathered}$$

so $\alpha=\theta_2-\theta_1=18.43^\circ=0.3217$ rad, and

$$\Delta\sigma_z=\frac{200}{\pi}\bigl[0.3217+(0.4000-0.5000)\bigr]=63.66(0.2217)$$

$$\boxed{\Delta\sigma_z\approx14.1\ \text{kN/m}^2}$$

(Equivalent form: $\Delta\sigma_z=\frac q\pi[\alpha+\sin\alpha\cos(\alpha+2\delta)]$ with $\delta=45^\circ$ gives the same value.)

**(c) Newmark's influence chart.** It is a graphical method of obtaining the vertical stress $\sigma_z$ under any point of a uniformly loaded area of any shape, based on Boussinesq's solution for the stress under the centre of a circular area. The chart consists of concentric circles whose radii are chosen as $R/z$ for $\sigma_z/q=0.1,0.2,\dots,0.9,1.0$ ($R/z=0.270,\,0.400,\,0.518,\dots,\infty$), divided by 20 equally spaced radial lines, so that each element (mesh) has the same *influence value* $I=1/N$ (commonly $0.005$ with $N=200$ elements, or $0.001$).

*Procedure.* (1) Draw the footing plan to a scale such that the length of the scale line on the chart (OQ) equals the depth $z$ of the point considered. (2) Place the point at which stress is wanted at the centre of the chart. (3) Count the number of elements $M$ covered by the plan. (4) $\sigma_z=I\,M\,q$.

*Applications:* stress at any depth under irregular footings, under raft and combined footings; stress under or outside the loaded area; calculating settlement under groups of loads; stress below embankments and tanks. A new drawing is needed for each depth.

@s 5
**(a) Assumptions of Terzaghi's one-dimensional theory.**

1. The soil is homogeneous and completely (100 %) saturated.
2. Water and soil particles are incompressible.
3. Compression and flow are one-dimensional (vertical).
4. Darcy's law is valid; $k$ is constant during consolidation.
5. Coefficient of volume compressibility $m_v$ (and so $c_v$) is constant.
6. Strains are small, the time-lag of compression is due entirely to the low permeability (no secondary compression), and there is a unique relation between void ratio and effective stress.

*Numerical.* For $U<60\%$: $T_v=\dfrac\pi4U^2$. So

$$\begin{gathered}T_v(20\%)=\frac\pi4(0.2)^2=0.0314\\ T_v(40\%)=\frac\pi4(0.4)^2=0.1257\end{gathered}$$

With double drainage the drainage path is half the thickness: $H_{dr,1}=10$ mm and $H_{dr,2}=2000$ mm. Since $t=T_vH_{dr}^2/c_v$ and $c_v$ is the same (same soil):

$$c_v=\frac{0.0314(10)^2}{20}=0.157\ \text{mm}^2/\text{min}$$

$$t_2=\frac{T_{v2}H_{dr,2}^2}{c_v}=\frac{0.1257(2000)^2}{0.157}=3.2\times10^{6}\ \text{min}$$

$$\boxed{t_2=3.2\times10^6\ \text{min}=2222\ \text{days}\approx6.09\ \text{years}}$$

(Check by ratio: $t_2=20\times\frac{0.1257}{0.0314}\times\left(\frac{2000}{10}\right)^2=20\times4\times40000$ min.)

**(b) Accelerating consolidation.** *Why:* clay has very low permeability, so primary consolidation of a thick clay layer can take years (here, over 6 years). If the structure is built before the settlement is complete, it suffers large total and differential settlement, cracking, tilting and loss of service. Faster consolidation also increases the strength gain of the soil and shortens the construction schedule.

*Before or after construction:* **before** construction (or at least during the early stage), so that the major part of the settlement has already taken place and the structure is built on a stiffer, mostly settled ground.

*How:* (1) **Preloading / surcharge fill** that is greater than the final structural load, removed once the required settlement is reached. (2) **Vertical drains**: sand drains, prefabricated vertical (wick) drains at 1–3 m spacing, which shorten the drainage path from $H$ to about half of the drain spacing. (3) **Vacuum consolidation** with a membrane. (4) Lowering the water table, electro-osmosis, and stone columns / sand compaction piles with drainage function. (5) Dynamic compaction for granular and partly saturated soils.

**(c) Preconsolidation pressure (Casagrande's method).** The preconsolidation pressure $\sigma'_c$ is the maximum past effective stress experienced by the soil. It is found from the laboratory $e$–$\log\sigma'$ curve of an undisturbed oedometer test:

1. Choose the point of maximum curvature $A$ on the curve (smallest radius).
2. Draw a horizontal line through $A$ and a tangent to the curve at $A$.
3. Bisect the angle between them.
4. Extend the straight (virgin compression) line backward to meet the bisector. The abscissa of the intersection gives $\sigma'_c$.

Compare $\sigma'_c$ with the present effective overburden $\sigma'_0$: $OCR=\sigma'_c/\sigma'_0$; $OCR=1$ is normally consolidated, $OCR>1$ overconsolidated.

```figure caption="Casagrande's construction for the preconsolidation pressure on the e–log σ' curve (schematic)."
fig,ax=plt.subplots(figsize=(4.8,3.0))
xc,cs,cc,k,e0=1.6,0.06,0.45,0.10,1.0
f=lambda x: e0-cs*(x-1)-(cc-cs)*k*np.log(1+np.exp((x-xc)/k))
x=np.linspace(1,3.0,300); ax.plot(x,f(x),color=ACCENT,lw=2)
xA=xc+0.02; yA=f(xA); m=(f(xA+1e-3)-f(xA-1e-3))/2e-3
ax.plot([xA],[yA],"o",color="#d9534f",ms=5); ax.text(xA-0.12,yA+0.04,"A",fontsize=9)
ax.plot([1.0,2.4],[yA,yA],color=MUTED,lw=0.8,ls=":")
xs=np.array([1.2,2.1]); ax.plot(xs,yA+m*(xs-xA),color=MUTED,lw=0.8,ls=":")
mb=np.tan(np.arctan(m)/2); xb=np.array([1.1,2.3]); ax.plot(xb,yA+mb*(xb-xA),color="#2e8b57",lw=1.1); ax.text(2.3,yA+mb*(2.3-xA)-0.04,"bisector",fontsize=7.5,color="#2e8b57")
xv=np.array([2.0,3.0]); sl=(f(3.0)-f(2.5))/0.5; yv=f(2.5)+sl*(xv-2.5); ax.plot(xv,yv,color=MUTED,lw=1,ls="--"); ax.plot([1.4,2.0],[f(2.5)+sl*(1.4-2.5)]*0+[f(2.5)+sl*(1.4-2.5),f(2.5)+sl*(2.0-2.5)],color=MUTED,lw=1,ls="--")
# intersection of bisector and virgin line
xi=(f(2.5)+sl*(-2.5)-(yA-mb*xA))/(mb-sl); ax.axvline(xi,color="#d9534f",lw=1,ls="--"); ax.text(xi+0.03,0.42,"σ'$_c$",fontsize=9,color="#d9534f")
ax.set_xlabel("log σ'  (kN/m²)",fontsize=8.5); ax.set_ylabel("void ratio e",fontsize=8.5); ax.tick_params(labelsize=7); ax.set_ylim(0.35,1.08); ax.set_xlim(1,3)
```


@s 6
**(a) Direct shear test.** *Apparatus:* a split shear box (60 mm × 60 mm or 100 mm × 100 mm) with porous stones and grid plates, a loading yoke for the normal load, a motor-driven horizontal loading frame (rate 1.25 mm/min for drained test on sand), proving ring (or load cell) for the shear force and dial gauges for horizontal and vertical displacements.

*Procedure.* A sample is placed in the box, a normal load $N$ is applied ($\sigma_n=N/A$; typical 50, 100, 200 kN/m²), and the box is sheared at a constant rate while the shear force $T$ and displacement $\Delta l$ are recorded until failure or 15–20 % strain. At least three samples are tested at different $\sigma_n$.

*Data presentation.* (1) Plot shear stress $\tau=T/A$ against horizontal displacement for each $\sigma_n$ (peak $\tau_f$ and residual strength); (2) plot vertical displacement against horizontal displacement (dense sand dilates, loose sand contracts); (3) plot the peak shear stress $\tau_f$ against normal stress $\sigma_n$ for the three tests.

*Interpretation.* The points lie on the Mohr–Coulomb failure envelope $\tau_f=c+\sigma_n\tan\phi$. The **intercept on the $\tau$ axis is the cohesion $c$** and the **slope is the angle of internal friction $\phi$**. For clean sand $c=0$ and $\phi\approx28^\circ$–$40^\circ$ (higher for dense sand). The test gives drained parameters on sands and, if slow enough, on clays; residual strength is found from reversal tests. *Limitations:* failure plane is forced; stress distribution is non-uniform; pore pressure cannot be measured and drainage cannot be controlled.

**(b) Unconfined compression test.** Area $A_0=\dfrac\pi4(38)^2\approx1134.1\ \text{mm}^2$; length $L_0=76$ mm; failure load $P=150$ N at $\Delta L=0.7$ mm.

$$\begin{gathered}\varepsilon=\frac{0.7}{76}=0.00921 \\ A=\frac{A_0}{1-\varepsilon}=\frac{1134.1}{0.99079}=1144.7\ \text{mm}^2\end{gathered}$$

$$q_u=\frac{P}{A}=\frac{150}{1144.7}=0.1310\ \text{N/mm}^2=131.0\ \text{kN/m}^2$$

For a saturated clay in the undrained condition $\phi_u=0$, so

$$\boxed{C_u=\frac{q_u}{2}=65.5\ \text{kN/m}^2}$$

*Mohr's circle:* the minor principal stress is $\sigma_3=0$ and the major $\sigma_1=q_u=131.0$ kN/m². The circle has centre at 65.5 and radius 65.5; the failure envelope is horizontal ($\phi_u=0$) and touches the circle at its top, whose ordinate is $C_u$.

```figure caption="Mohr's circle for the unconfined compression test (σ3 = 0, σ1 = qu = 131 kN/m²); the horizontal envelope touches the circle at τ = Cu = 65.5 kN/m²."
th=np.linspace(0,np.pi,200); cu=65.5
fig,ax=plt.subplots(figsize=(4.8,2.6)); ax.set_aspect("equal")
ax.plot(cu+cu*np.cos(th),cu*np.sin(th),color=ACCENT,lw=2)
ax.axhline(0,color=INK,lw=1); ax.plot([0,160],[cu,cu],color="#d9534f",lw=1.4); ax.plot([cu],[cu],"o",color="#d9534f",ms=4)
ax.text(cu+2,cu+4,"C$_u$ = 65.5",fontsize=8.5,color="#d9534f"); ax.text(-8,-14,"σ$_3$ = 0",fontsize=8); ax.text(112,-14,"σ$_1$ = q$_u$ = 131",fontsize=8)
ax.text(120,cu+4,"φ$_u$ = 0 envelope",fontsize=8,color="#d9534f")
ax.set_xlim(-15,165); ax.set_ylim(-22,80); ax.axis("off")
```

**(c) Triaxial test: merits and demerits.**

*Merits:* (1) drainage conditions (UU, CU, CD) are fully controlled; (2) pore pressure can be measured, so effective-stress parameters ($c'$, $\phi'$) are obtained; (3) stress state is uniform and the failure plane is free to form in the weakest plane; (4) stress path can be varied, volume change and stiffness (E, $K_0$) are measured; (5) specimens may be saturated by back pressure and tested at in-situ stress.

*Demerits:* (1) equipment is costly and requires skilled operators; (2) CD tests on clay are slow (days to weeks); (3) axisymmetric loading ($\sigma_2=\sigma_3$) only, which does not represent plane-strain field conditions; (4) sample disturbance and end restraint from the platens; (5) small specimens may not represent the macro-fabric (fissures) of the deposit.

**(d) Cyclic shear strength.** It is the shear strength of a soil under repeated (cyclic) loading: the maximum cyclic shear stress ratio $\tau_{cyc}/\sigma'_0$ that the soil can sustain for a given number of cycles $N$ before failure (or before pore pressure rises to the confining pressure, i.e. liquefaction, or strain reaches 5 %). It is determined by cyclic triaxial, cyclic simple shear or cyclic torsional shear tests and is lower than the monotonic strength. 

*Importance:* it is required to evaluate **liquefaction** of loose saturated sands in earthquakes (Gorkha 2015, Terai region), the stability of earth dams and slopes under seismic loading, the design of foundations for machines and traffic, offshore structures under waves, and railway and pavement subgrades (fatigue and degradation of stiffness).

@s 7
**(a) Effects of compaction on soil characteristics.** Compaction (densification by expelling air using mechanical energy) results in:

1. increase in dry unit weight and shear strength (and bearing capacity);
2. decrease in void ratio, permeability and seepage;
3. decrease in compressibility and settlement under load;
4. decrease in swelling, shrinkage and frost susceptibility, improved resistance to erosion and liquefaction;
5. a change of fabric: the soil compacted **dry of optimum is flocculated** (stiff, higher strength, more permeable, swells more) and **wet of optimum is dispersed** (soft, ductile, less permeable, shrinks more). Maximum dry density is obtained at the optimum moisture content (OMC) for a given energy.

**(b) Standard Proctor test.** Dry density $\rho_d=\rho/(1+w)$ with $G=2.6$:

| $w$ (%) | 5 | 8 | 10 | 12 | 16 | 20 |
|---|---|---|---|---|---|---|
| $\rho$ (kg/m³) | 1890 | 2130 | 2200 | 2210 | 2160 | 2080 |
| $\rho_d$ (kg/m³) | 1800.0 | 1972.2 | 2000.0 | 1973.2 | 1862.1 | 1733.3 |

*Zero-air-void line* ($S=1$): $\rho_{d,zav}=\dfrac{G\rho_w}{1+wG}$, e.g. 2301 (5 %), 2152 (8 %), 2063 (10 %), 1982 (12 %), 1835 (16 %), 1710 (20 %) kg/m³ at $w=5,\ 8,\ 10,\ 12,\ 16,\ 20$ %.

```figure caption="Compaction curve (standard Proctor) with the zero-air-void line for G = 2.6; peak at OMC ≈ 10 %, maximum dry density ≈ 2000 kg/m³."
w=np.array([5,8,10,12,16,20.]); rd=np.array([1800,1972.2,2000,1973.2,1862.1,1733.3])
fig,ax=plt.subplots(figsize=(5.0,3.1))
ww=np.linspace(4,21,100); ax.plot(ww,2600/(1+ww/100*2.6),color="#d9534f",lw=1.4,ls="--",label="zero-air-void line (S = 100 %)")
from scipy.interpolate import PchipInterpolator
ax.plot(ww[(ww>=5)&(ww<=20)],PchipInterpolator(w,rd)(ww[(ww>=5)&(ww<=20)]),color=ACCENT,lw=2,label="compaction curve"); ax.plot(w,rd,"o",color=ACCENT,ms=4)
ax.plot([10,10],[1650,2000],color=MUTED,lw=0.8,ls=":"); ax.plot([4,10],[2000,2000],color=MUTED,lw=0.8,ls=":")
ax.text(10.3,1700,"OMC ≈ 10 %",fontsize=8); ax.text(4.2,2010,"ρ$_{d,max}$ ≈ 2000",fontsize=8)
ax.set_xlabel("water content w (%)",fontsize=8.5); ax.set_ylabel("dry density (kg/m³)",fontsize=8.5); ax.set_ylim(1650,2350); ax.legend(fontsize=7.5,loc="upper right"); ax.grid(True,color=GRID,lw=0.6); ax.tick_params(labelsize=7.5)
```

*At the optimum (peak of the curve):* $w_{opt}=10\%$ and $\rho_{d,max}=2000$ kg/m³ (a quadratic fit through the peak points gives 10.0 % and 2000 kg/m³).

$$\boxed{e=\frac{G\rho_w}{\rho_{d,max}}-1=\frac{2600}{2000}-1=0.30}$$

$$\boxed{n=\frac{e}{1+e}=\frac{0.30}{1.30}=0.231\ (23.1\%)}$$

$$\boxed{S=\frac{wG}{e}=\frac{0.10(2.6)}{0.30}=0.867=86.7\%}$$

At the optimum 13.3 % of the voids still contain air (air content $n_a=n(1-S)=3.1\%$ of the total volume), as expected: the zero-air-void density at 10 % is 2063 kg/m³, above the curve.

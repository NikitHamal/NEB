---
file: NEBians-IOE-Past-Paper-Soil-Mechanics-ENCE253-2082-Bhadra.pdf
subject: Soil Mechanics
level: BE · Year II / Part II
code: ENCE 253
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course), BE Civil, Year II / Part II. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Write about the historical development of soil mechanics. Differentiate between residual and transported soil. [[2+1]]

b) Describe isomorphous substitution. Describe briefly the different types of clay minerals with a neat sketch. [[1+2]]

@q 2
a) Derive a relationship between dry density, percentage air voids, water content and specific gravity. [[3]]

b) A 1000 cc saturated clay sample weigh 1550 g which reduced to 1100 g up on oven drying. Calculate water content, void ratio and specific gravity of the specimen. [[3]]

c) Describe shrinkage limit and its laboratory procedure. [[3]]

d) Classify following soil as per USCS. [[3]]

Soil passing 75 μ sieve = 8%; soil passing 4.75 mm sieve = 70%; LL of fines = 60% and PL of fines = 50%; $C_u$ = 6.5 and $C_c$ = 2

@q 3
a) Discuss characteristics of flow net and its applications. [[1+3]]

b) In field, 4 m thick soil layer is underlain by another soil layer of 5.5 m thick. Samples from both layers were subjected to falling head permeability test where the cross-sectional area of the stand pipe = 400 mm², cross-sectional area of soil sample = 2700 mm² and sample thickness = 55 mm. In both tests the water level in the stand pipe were left to decrease from 1000 mm to 200 mm. The elapsed time during the decrease of the water level in the stand pipe was 500 seconds for the sample of the upper layer and 100 seconds for that of the lower layer. (i) Determine the coefficient of permeability of both soils. (ii) Determine the average coefficient of permeability for flow parallel to bedding in field. [[4]]

@q 4
a) What is quick sand condition? What are the problems associated with quick sand condition? [[2]]

b) For the subsoil conditions as shown in figure below, plot the total, neutral and effective stress distribution upto the bottom of the clay layer. [[4]]

```figure caption="Question 4(b): sand 3 m thick (S = 20 %, e = 0.4, γ = ?), then a 1 m capillary-rise zone (γsat = ?) with the water table at its bottom, then 5 m of clay (γsat). G and γsat of the clay are not printed on the scan and are assumed in the solution."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.0,2.7)); ax.axis("off")
ax.add_patch(mp.Rectangle((0,6),6,3,fc="#f3e3b5",ec=INK)); ax.add_patch(mp.Rectangle((0,5),6,1,fc="#e3d3a0",ec=INK)); ax.add_patch(mp.Rectangle((0,0),6,5,fc="#c9b9a6",ec=INK))
ax.text(3,7.5,"Sand; S = 20 %; e = 0.4; γ = ?",ha="center",fontsize=8.5); ax.text(3,5.5,"Capillary rise; γ$_{sat}$ = ?",ha="center",fontsize=8.5); ax.text(3,2.5,"Clay; γ$_{sat}$",ha="center",fontsize=9)
ax.plot([5.2,5.8],[5,5],color=ACCENT,lw=1.5); ax.text(5.5,4.55,"▽",ha="center",fontsize=8,color=ACCENT)
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
for y0,y1,t in [(9,6,"3 m"),(6,5,"1 m"),(5,0,"5 m")]:
    ax.annotate("",xy=(-0.4,y0),xytext=(-0.4,y1),arrowprops=ar); ax.text(-0.7,(y0+y1)/2,t,ha="right",va="center",fontsize=9)
ax.set_xlim(-2,7); ax.set_ylim(-0.5,9.5)
```

c) A circular tank of 10 m diameter has rested on elastic soil mass of great with the uniformly distributed base pressure of 200 kN/m². Compute the vertical stress caused by the tank at a depth of 5 m below the center of the foundation base. [[2]]

@q 5
a) What are the compression parameters that can be determined from Oedometer test? Describe with necessary curves. [[4]]

b) An undisturbed sample of clay, 24 mm in thickness, is tested in a consolidometer. The total change in thickness of specimen is 4.74 mm when the applied pressure is 200 kN/m² and 6.13 mm when the applied pressure is 400 kN/m². On reducing the pressure to zero, the specimen swells to a thickness of 18.5 mm. The final water content of the specimen is 32.6% and G = 2.72. The clay stratum, 1 m thick, is sandwiched between pervious strata and is subjected to an overburden pressure of 200 kN/m². Estimate that probable settlement of a proposed structure if effective pressure at the center of the clay layer is increased to 400 kN/m². [[4]]

@q 6
a) Describe different methods of determining shear strength parameters in the laboratory. Define stress path. Also, draw Mohr-Coulomb strength envelopes for cohesive soil, cohesionless soil and purely cohesive soil. [[1+1+2]]

b) A triaxial tests on two specimens of the same soil sample is given below. [[5]]

| Specimen Number | 1 | 2 |
|---|---|---|
| Cell pressure (kN/m²) | 100 | 200 |
| Deviator pressure (kN/m²) | 570 | 600 |

Find the value of cohesion and angle of friction by analytical as well as graphical methods.

c) Define critical state line (CSL) using data from consolidation and triaxial tests. [[3]]

@q 7
a) Differentiate between Modified Proctor test and Harvard Miniature compaction test. [[2]]

b) The following results were obtained from standard compaction test: [[4]]

| Mass of compacted soil (g) | 1700 | 1800 | 1850 | 1875 | 1750 | 1600 |
|---|---|---|---|---|---|---|
| Water content (w%) | 10 | 11 | 12 | 13 | 14.5 | 16 |

Take G = 2.7; Volume of compaction mould = 1000 cc

a) Plot the compaction curve and obtain the maximum dry density and optimum moisture content.

b) Plot zero air void line.

If dry density in the field is 1650 kg/m³, what is the relative compaction?

<!-- SOLUTIONS -->

@s 1
**(a) Historical development of soil mechanics.**

- *Early empirical stage (before 1700):* the Egyptians, Greeks, Romans and the builders of Pagoda / Stupa / Kot in Nepal built foundations and earthworks by experience; Vitruvius wrote on foundations.
- *Classical stage (1700–1900):* Coulomb (1776) – earth pressure and shear strength, $\tau=c+\sigma\tan\phi$; Darcy (1856) – law of seepage; Rankine (1857) – earth-pressure theory; Boussinesq (1885) – stresses in an elastic half-space; Mohr (1900) – stress circle and failure criterion.
- *Modern stage:* Atterberg (1911) – consistency limits; Fellenius (1916) – slip-circle stability; **Terzaghi (1923–25)** – principle of effective stress and consolidation theory, who published *Erdbaumechanik* in 1925 and is called the *father of soil mechanics*; Casagrande – soil classification, flow nets and preconsolidation; Proctor (1933) – compaction; Skempton, Bishop and Bjerrum – pore-pressure parameters, undrained strength; Roscoe, Schofield and Wroth (1958–68) – critical state soil mechanics; since then computers, FEM, in-situ testing and ground improvement.

*Residual and transported soils.* **Residual soil** is formed by weathering of the parent rock and remains *in place* (laterite, red soils); it grades from soil to weathered rock with depth, is angular, poorly sorted and rock-like in the lower parts. **Transported soil** is moved from the place of origin by water (alluvial, lacustrine, marine), wind (aeolian, loess), glacier (glacial till) or gravity (colluvial) and deposited elsewhere; it is stratified/sorted, rounded, and its properties are independent of the underlying bedrock.

**(b) Isomorphous substitution** is the replacement of the central cation of the tetrahedral or octahedral sheet by another cation of nearly the same size but lower valence, *without any change in the crystal structure*, e.g. Al³⁺ for Si⁴⁺ in the silica sheet, or Mg²⁺ for Al³⁺ in the gibbsite sheet. The lattice then carries a net **negative charge**, which is balanced by adsorbed exchangeable cations (Na⁺, Ca²⁺, K⁺) on the particle surface. It controls cation exchange capacity, swelling, and the plasticity of the clay.

*Types of clay minerals:*

1. **Kaolinite** (1:1): one silica sheet + one gibbsite sheet, thickness 7.2 Å. Layers held by strong hydrogen bonds, so there is no interlayer swelling; low plasticity and compressibility, low activity (0.4); stacks are thick (large particles). Used in ceramics and paper.
2. **Illite** (2:1, mica-like): a gibbsite sheet between two silica sheets, thickness 10 Å; layers are bonded by **potassium ions** (K⁺) that fit into the hexagonal holes of the silica sheet, which is moderately strong, so swelling is limited; intermediate activity (0.9).
3. **Montmorillonite** (2:1): the same sandwich as illite but with very weak O–O / van der Waals bonds and water between layers, so it is highly expansive; high plasticity and activity (1–7); thickness 9.6 Å to infinity (bentonite).

```figure caption="Schematic structures of the three common clay minerals: kaolinite (1:1, H-bonded), illite (2:1, K+ bonded) and montmorillonite (2:1, expanding with water between layers)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.8,3.0)); ax.axis("off")
S,Gb="#f2d9a0","#9fc5e8"
def box(x,y,h,c): ax.add_patch(mp.Rectangle((x,y),2.6,h,fc=c,ec=INK,lw=0.7))
x=0
for y in (0,1.55): box(x,y,0.5,Gb); box(x,y+0.5,0.5,S)
ax.text(1.3,2.9,"Kaolinite\n1:1, 7.2 Å\nH-bond",ha="center",fontsize=8)
for y in (0,1.9):
    box(4,y,0.4,S); box(4,y+0.4,0.4,Gb); box(4,y+0.8,0.4,S)
ax.scatter([4.4,5.0,5.6,6.2],[1.6]*4,s=18,c="#d9534f"); ax.text(5.3,3.3,"Illite\n2:1, 10 Å\nK$^+$ ions bond",ha="center",fontsize=8)
for y in (0,2.4):
    box(8,y,0.4,S); box(8,y+0.4,0.4,Gb); box(8,y+0.8,0.4,S)
ax.scatter(np.linspace(8.2,10.4,7),[1.5,2.0,1.7,2.1,1.6,1.9,1.55],s=14,c=ACCENT); ax.text(9.3,3.7,"Montmorillonite\n2:1, 9.6 Å → ∞\nwater + cations",ha="center",fontsize=8)
ax.text(1.3,-0.5,"■ silica  ■ gibbsite",fontsize=7,ha="center",color=MUTED)
ax.set_xlim(-0.5,11.2); ax.set_ylim(-0.8,4.6)
```

@s 2
**(a) Derivation.** Take a soil element of total volume $V=1$ and let the percentage (fraction) of air voids be $n_a=V_a/V$, the specific gravity of solids $G$ and water content $w$.

$$\begin{gathered}V_a=n_a \\ V_s+V_w+V_a=1\end{gathered}$$

$$w=\frac{W_w}{W_s}=\frac{V_w\gamma_w}{G\gamma_wV_s}\ \Rightarrow\ V_w=wGV_s$$

$$V_s(1+wG)+n_a=1\ \Rightarrow\ V_s=\frac{1-n_a}{1+wG}$$

The dry unit weight is $\gamma_d=\dfrac{W_s}{V}=G\gamma_wV_s$:

$$\boxed{\gamma_d=\frac{(1-n_a)\,G\,\gamma_w}{1+wG}}$$

For zero air voids ($n_a=0$) it reduces to $\gamma_{d}=\dfrac{G\gamma_w}{1+wG}=\dfrac{G\gamma_w}{1+e}$, the zero-air-void (saturation) line.

**(b) Saturated clay.** $V=1000$ cc, $W=1550$ g, $W_s=1100$ g, so $W_w=450$ g and $V_w=450$ cc. Saturated, hence $V_v=V_w=450$ cc and $V_s=1000-450=550$ cc.

$$\boxed{w=\frac{450}{1100}=40.9\%}$$

$$\boxed{e=\frac{V_v}{V_s}=\frac{450}{550}=0.818}$$

$$\boxed{G=\frac{W_s}{V_s\gamma_w}=\frac{1100}{550(1)}=2.00}$$

(Check: $e=wG/S=0.409(2.0)/1=0.818$. A value of $G=2.0$ is low for a mineral soil, which suggests organic matter, but follows from the data.)

**(c) Shrinkage limit.** It is the water content at which a soil, on further drying, stops shrinking: the boundary between the semi-solid and solid states. Below $w_s$ the volume stays constant and the soil is still saturated.

*Laboratory procedure (IS 2720 Part 6).*

1. Take about 100 g of soil passing the 425 μ sieve and mix it with distilled water to a paste at about the liquid limit (the paste should be workable and free of air).
2. Coat the inside of a shrinkage dish (45 mm dia, 15 mm high) with petroleum jelly and weigh it empty ($W_1$).
3. Fill the dish in three layers, tapping to remove air, strike off the top, and weigh ($W_2$). The mass of wet soil is $W_2-W_1$ and its volume $V_1$ equals the volume of the dish.
4. Air-dry until the colour changes, then oven dry at 105–110 °C and weigh ($W_3$), so $W_d=W_3-W_1$.
5. Determine the volume of the dry pat $V_2$ by mercury displacement: fill a glass cup with mercury, strike off with a glass plate with three prongs, press the pat into it, and weigh the displaced mercury ($V_2=m_{Hg}/13.6$).

$$\begin{gathered}w_1=\frac{(W_2-W_1)-W_d}{W_d}\times100 \\ \boxed{w_s=w_1-\frac{(V_1-V_2)\gamma_w}{W_d}\times100}\end{gathered}$$

The shrinkage ratio is $SR=W_d/(V_2\gamma_w)$ and the volumetric shrinkage $V_s=(w_1-w_s)SR$.

**(d) USCS classification.**

- Percent passing 75 μ = 8 % ⇒ fines < 50 %, so a **coarse-grained** soil (92 % retained).
- Percent passing 4.75 mm = 70 %, so 30 % of the total is retained on the 4.75 mm sieve. The gravel fraction is $30/92=32.6\%<50\%$ of the coarse fraction ⇒ the soil is a **sand** (S).
- Fines are 8 %, which lies between 5 and 12 %, so a **dual symbol** is required (clean part + fines part).
- Grading: $C_u=6.5\ge6$ and $1\le C_c=2\le3$ ⇒ **well graded** (SW).
- Fines: $PI=LL-PL=60-50=10$. The A-line at $LL=60$ gives $PI_A=0.73(60-20)=29.2$. Since $PI=10<29.2$ the fines plot **below the A-line** with high LL ⇒ silt of high plasticity (MH, used as the suffix M).

$$\boxed{\text{USCS group symbol: SW–SM (well-graded sand with silt)}}$$

@s 3
**(a) Flow net.** A flow net is a graphical representation of steady two-dimensional seepage, formed by a family of **flow lines** (paths of water particles) and **equipotential lines** (lines of equal total head) satisfying Laplace's equation $\partial^2h/\partial x^2+\partial^2h/\partial z^2=0$.

*Characteristics:*

1. Flow lines and equipotential lines intersect each other at **right angles**.
2. The elements (field) are curvilinear **squares** (the mean length equals the mean width, for $\Delta l=\Delta b$).
3. The same quantity of water flows through every flow channel ($\Delta q$ is equal), and the head loss between any two adjacent equipotential lines is equal ($\Delta h=H/N_d$).
4. Flow lines do not cross each other, nor do equipotentials; flow lines never leave the soil boundary except at the entry/exit surfaces; an impermeable boundary is a flow line and a submerged soil surface is an equipotential.
5. The smaller the field, the greater the hydraulic gradient and velocity.

*Applications:*

- Seepage quantity: $q=kH\dfrac{N_f}{N_d}$ per unit length.
- Pore water pressure at any point ($u=\gamma_w h_p$) and the uplift pressure under hydraulic structures (weirs, dams).
- Exit gradient $i_e=\Delta h/\Delta l$ to check against piping, $FS=i_c/i_e$.
- Seepage force on soil, and the stability of slopes, sheet-pile and excavation bottoms.

**(b) Falling-head tests.** $a=400$ mm², $A=2700$ mm², $L=55$ mm, $h_1=1000$ mm, $h_2=200$ mm.

$$k=\frac{aL}{At}\ln\frac{h_1}{h_2}=\frac{400(55)}{2700\,t}\ln5=\frac{22000(1.6094)}{2700\,t}$$

*(i)* Upper layer ($t=500$ s) and lower layer ($t=100$ s):

$$\boxed{k_1=\frac{22000(1.6094)}{2700(500)}=2.62\times10^{-2}\ \text{mm/s}}$$

$$\boxed{k_2=\frac{22000(1.6094)}{2700(100)}=13.11\times10^{-2}\ \text{mm/s}=0.131\ \text{mm/s}}$$

*(ii)* For flow **parallel** to bedding the equivalent permeability is the thickness-weighted mean:

$$k_{eq,H}=\frac{k_1H_1+k_2H_2}{H_1+H_2}=\frac{0.02623(4)+0.13114(5.5)}{9.5}=\frac{0.1049+0.7213}{9.5}$$

$$\boxed{k_{eq,H}=0.087\ \text{mm/s}=8.7\times10^{-5}\ \text{m/s}}$$

(For comparison, the equivalent permeability for flow perpendicular to the bedding is only 0.0458 mm/s.)

@s 4
**(a) Quick sand condition.** Quick sand is not a type of soil but a *condition* in cohesionless soil (fine sand, silt) when the upward seepage gradient equals the critical hydraulic gradient. The seepage force then balances the submerged weight, the effective stress becomes zero and the soil loses its shear strength and behaves like a liquid ("boiling"):

$$i_c=\frac{\gamma'}{\gamma_w}=\frac{G-1}{1+e}\approx1.0$$

*Problems:* (1) loss of bearing capacity and sudden failure of foundations; (2) boiling and heaving of the bottom of excavations, collapse of cofferdams and sheet piling; (3) piping and erosion of material beneath dams, weirs and levees, leading to failure; (4) failure of slopes and retaining walls due to upward seepage; (5) difficulty in construction and dewatering. Remedies include dewatering, well points, a filter layer or surcharge at the exit, cut-off walls, and a longer seepage path.

**(b) Stress distribution.** Because $G$ and $\gamma_{sat}$ of the clay are not printed, assume $G=2.65$ for the sand and $\gamma_{sat}=19.0$ kN/m³ for the clay, $\gamma_w=9.81$ kN/m³.

*Sand above the capillary fringe* ($S=0.2$, $e=0.4$):

$$\gamma=\frac{(G+Se)\gamma_w}{1+e}=\frac{(2.65+0.2\times0.4)9.81}{1.4}=19.13\ \text{kN/m}^3$$

*Capillary zone* (fully saturated, $S=1$):

$$\gamma_{sat}=\frac{(G+e)\gamma_w}{1+e}=\frac{(2.65+0.4)9.81}{1.4}=21.37\ \text{kN/m}^3$$

The water table is at the bottom of the capillary zone (4 m depth). The pore pressure in the capillary zone is *negative*: $u=-\gamma_wh_c$, where $h_c$ is the height above the water table.

| Depth (m) | Total stress $\sigma$ (kN/m²) | Neutral stress $u$ (kN/m²) | Effective stress $\sigma'=\sigma-u$ (kN/m²) |
|---|---|---|---|
| 0 (ground) | 0 | 0 | 0 |
| 3 (top of capillary zone) | $3(19.13)=57.39$ | $-1(9.81)=-9.81$ | $67.20$ |
| 4 (water table) | $57.39+21.37=78.76$ | 0 | $78.76$ |
| 9 (bottom of clay) | $78.76+5(19.0)=173.76$ | $5(9.81)=49.05$ | $124.71$ |

*Check:* $\sigma'_9=78.76+5(9.19)$, which is again 124.71 kN/m². ✔

```figure caption="Total, neutral (pore water) and effective stress distribution to the bottom of the clay layer (G = 2.65 and clay γsat = 19 kN/m³ assumed). The pore pressure is negative (−9.81 kN/m²) in the capillary zone."
fig,axs=plt.subplots(1,3,figsize=(5.9,3.0),sharey=True)
z=np.array([0,3,4,9]); sig=np.array([0,57.39,78.76,173.76]); u=np.array([0,-9.81,0,49.05]); se=sig-u
for ax,v,t in zip(axs,[sig,u,se],["total stress σ","neutral stress u","effective stress σ'"]):
    ax.plot(v,-z,color=ACCENT,lw=1.8,marker="o",ms=3.5); ax.fill_betweenx(-z,0,v,color=ACCENT,alpha=0.13); ax.set_title(t,fontsize=8); ax.tick_params(labelsize=7); ax.grid(True,color=GRID,lw=0.5)
    for zz,vv in zip(z,v): ax.text(vv,-zz+0.25,f"{vv:.1f}",fontsize=6.5,ha="center" if vv>0 else "right")
    for zb in (3,4): ax.axhline(-zb,color=MUTED,lw=0.6,ls=":")
    ax.axvline(0,color=INK,lw=0.7); ax.set_xlabel("kN/m²",fontsize=7.5)
axs[0].set_ylabel("depth (m)",fontsize=8); axs[0].set_xlim(-10,210); axs[1].set_xlim(-30,75); axs[2].set_xlim(-10,160)
fig.tight_layout()
```

**(c) Circular tank.** For a uniformly loaded circular area of radius $R$, the stress at depth $z$ below the centre is

$$\Delta\sigma_z=q\left[1-\frac{1}{\left(1+(R/z)^2\right)^{3/2}}\right]$$

With $R=5$ m, $z=5$ m, $q=200$ kN/m²:

$$\Delta\sigma_z=200\left[1-\frac{1}{(1+1)^{3/2}}\right]=200\left[1-\frac{1}{2.828}\right]=200(0.6464)$$

$$\boxed{\Delta\sigma_z=129.3\ \text{kN/m}^2}$$

@s 5
**(a) Compression parameters from the oedometer (consolidation) test.** The sample, laterally confined in a ring and drained at top and bottom, is loaded in increments (e.g. 25, 50, 100, 200, 400, 800 kN/m²), each held for 24 h, and the change in thickness is recorded. From the equilibrium void ratio at each pressure ($e=e_0-\Delta H(1+e_0)/H_0$) we plot $e$ vs $\sigma'$ and $e$ vs $\log\sigma'$.

| Parameter | Definition | Source |
|---|---|---|
| Coefficient of compressibility $a_v$ | $a_v=-\dfrac{\Delta e}{\Delta\sigma'}$ (m²/kN) | slope of the $e$–$\sigma'$ curve |
| Coefficient of volume compressibility $m_v$ | $m_v=\dfrac{a_v}{1+e_0}$ | $=\Delta\varepsilon_v/\Delta\sigma'$ |
| Compression index $C_c$ | $C_c=-\dfrac{\Delta e}{\Delta\log\sigma'}$ | slope of the virgin (straight) line on the $e$–$\log\sigma'$ curve |
| Swelling (recompression) index $C_s$ | slope of the unloading/reloading loop | $C_s\approx\tfrac15$ to $\tfrac1{10}C_c$ |
| Preconsolidation pressure $\sigma'_c$ | maximum past effective stress | Casagrande construction |
| Coefficient of consolidation $c_v$ | $c_v=\dfrac{T_vH_{dr}^2}{t}$ | time curves (log-time or root-time) |

Typical correlation: $C_c=0.009(LL-10)$ for undisturbed clay. The settlement is $S=\dfrac{C_cH}{1+e_0}\log\dfrac{\sigma'_0+\Delta\sigma'}{\sigma'_0}$ for normally consolidated clay.

```figure caption="Oedometer results: (left) e against σ' (slope gives av); (right) e against log σ' showing the recompression (Cs) and virgin compression (Cc) lines and σ'c."
fig,axs=plt.subplots(1,2,figsize=(5.8,2.7))
s=np.linspace(10,800,200); e1=1.0-0.12*np.log10(s/10)*np.where(s<200,0.35,1)
x=np.linspace(1,3,200); xc=2.0
e2=np.where(x<xc,1.0-0.06*(x-1),1.0-0.06-0.45*(x-xc))
axs[0].plot(s,1.0-0.0007*s*np.exp(-s/700)*1.6,color=ACCENT,lw=2); axs[0].set_xlabel("σ' (kN/m²)",fontsize=8); axs[0].set_ylabel("e",fontsize=8); axs[0].set_title("e – σ'  (slope = −a$_v$)",fontsize=8)
axs[1].plot(x,e2,color=ACCENT,lw=2); axs[1].plot([xc,3],[0.94,0.94-0.45],color=ACCENT,lw=0); axs[1].plot([3,2.6],[0.49,0.49+0.06*0.4*0+0.0],lw=0)
axs[1].plot([2.9,2.55],[0.49,0.4+0.12],color="#d9534f",lw=1.2); axs[1].text(2.55,0.57,"C$_s$",fontsize=8,color="#d9534f")
axs[1].text(2.35,0.78,"C$_c$ (virgin)",fontsize=8,color=ACCENT); axs[1].text(1.15,0.97,"C$_s$",fontsize=8); axs[1].axvline(xc,color=MUTED,lw=0.8,ls="--"); axs[1].text(xc+0.03,0.52,"σ'$_c$",fontsize=8.5)
axs[1].set_xlabel("log σ'",fontsize=8); axs[1].set_title("e – log σ'",fontsize=8)
for a in axs: a.tick_params(labelsize=7); a.grid(True,color=GRID,lw=0.5)
fig.tight_layout()
```

**(b) Settlement from the consolidation test data.** Initial thickness $H_0=24$ mm.

*Height of solids from the final state.* After unloading the specimen is $H_f=18.5$ mm thick, with $w_f=32.6\%$ and (saturated) $e_f=w_fG$, i.e. $0.326\times2.72=0.8867$:

$$H_s=\frac{H_f}{1+e_f}=\frac{18.5}{1.8867}=9.805\ \text{mm}$$

*Void ratios at the two pressures:*

$$e_{200}=\frac{24-4.74}{9.805}-1=\frac{19.26}{9.805}-1=0.9642$$

$$e_{400}=\frac{24-6.13}{9.805}-1=\frac{17.87}{9.805}-1=0.8225$$

so $\Delta e=0.1418$ between 200 and 400 kN/m², and the compression index is

$$C_c=\frac{\Delta e}{\log(400/200)}=\frac{0.1418}{0.3010}=0.471$$

*Settlement of the 1 m ($1000$ mm) clay layer* from $\sigma'_0=200$ to $\sigma'_f=400$ kN/m² (the laboratory test shows normal consolidation over this range, the field overburden equals the pressure for $e_{200}$):

$$S=\frac{\Delta e}{1+e_0}H=\frac{0.1418}{1+0.9642}(1000)$$

$$\boxed{S\approx72\ \text{mm}}$$

(Check: the formula $S=\dfrac{C_cH}{1+e_0}\log\dfrac{\sigma'_f}{\sigma'_0}$ also gives 72.2 mm.)

@s 6
**(a) Laboratory methods for the shear strength parameters ($c$, $\phi$).**

1. **Direct shear test:** a prismatic sample sheared along a predetermined horizontal plane in a split box at constant normal stress; at least three $\sigma_n$ give $c$ and $\phi$; simple and quick, used for sands and drained shear of clays.
2. **Triaxial compression test:** a cylindrical sample enclosed in a rubber membrane, subjected to cell pressure $\sigma_3$ and an axial deviator stress $\sigma_d$ until failure. Variants: **UU** (unconsolidated undrained, $c_u$, $\phi_u$), **CU** (consolidated undrained, with pore-pressure measurement gives $c'$, $\phi'$) and **CD** (consolidated drained). Controlled drainage, best method.
3. **Unconfined compression test:** the special case $\sigma_3=0$ for saturated cohesive soil, $c_u=q_u/2$.
4. **Laboratory vane shear test:** a cruciform vane rotated in soft clay, $c_u=T/(\pi D^2(H/2+D/6))$.
5. **Simple shear and ring shear tests** (cyclic and residual strength).

*Stress path.* It is the locus of successive stress states (the top points of the Mohr circles, $p=\tfrac{\sigma_1+\sigma_3}{2}$, $q=\tfrac{\sigma_1-\sigma_3}{2}$) followed by a soil element during loading, plotted in $p$–$q$ (or $p'$–$q$) space. The stress path ends at the $K_f$-line, which lies at angle $\alpha$ with $\tan\alpha=\sin\phi$ and intercept $a=c\cos\phi$.

*Mohr–Coulomb envelopes:* (i) cohesive–frictional ($c$–$\phi$) soil: $\tau_f=c+\sigma\tan\phi$ (straight line with intercept and slope); (ii) cohesionless soil (clean sand): $\tau_f=\sigma\tan\phi$ passes through the origin; (iii) purely cohesive soil (saturated clay, undrained, $\phi_u=0$): $\tau_f=c_u$, a horizontal line.

```figure caption="Mohr–Coulomb strength envelopes: (a) cohesive–frictional soil, (b) cohesionless soil, (c) purely cohesive soil (φu = 0)."
fig,axs=plt.subplots(1,3,figsize=(5.9,2.0),sharey=True)
sg=np.linspace(0,10,10)
data=[(3,0.45,"(a) c–φ soil","c"),(0,0.6,"(b) cohesionless","φ"),(4,0,"(c) purely cohesive","c$_u$")]
for ax,(c,t,ti,lab) in zip(axs,data):
    ax.plot(sg,c+t*sg,color="#d9534f",lw=2); ax.set_title(ti,fontsize=8); ax.set_xlabel("σ",fontsize=8); ax.tick_params(labelsize=0); ax.set_ylim(0,9)
    th=np.linspace(0,np.pi,60); 
    for cx,r in [(3,1.6),(6,2.6)]: ax.plot(cx+r*np.cos(th),r*np.sin(th),color=ACCENT,lw=0.9)
    if c: ax.text(0.2,c+0.3,lab,fontsize=8)
    if lab=="φ": ax.text(7.2,2.0,"φ",fontsize=8)
axs[0].set_ylabel("τ",fontsize=8); fig.tight_layout()
```

**(b) Triaxial tests.** The major principal stress at failure is $\sigma_1=\sigma_3+\sigma_d$:

$$\begin{gathered}\sigma_{1(1)}=100+570=670\ \text{kN/m}^2 \\ \sigma_{1(2)}=200+600=800\ \text{kN/m}^2\end{gathered}$$

*Analytical method.* With $N_\phi=\tan^2(45^\circ+\phi/2)$ the failure condition is $\sigma_1=\sigma_3N_\phi+2c\sqrt{N_\phi}$. Subtracting the two equations:

$$800-670=(200-100)N_\phi\ \Rightarrow\ N_\phi=1.30,\quad \sqrt{N_\phi}=1.1402$$

$$\tan(45^\circ+\tfrac\phi2)=1.1402\ \Rightarrow\ 45^\circ+\tfrac\phi2=48.74^\circ\ \Rightarrow\ \boxed{\phi=7.5^\circ}$$

$$670=100(1.30)+2c(1.1402)\ \Rightarrow\ c=\frac{540}{2.2804}\ \Rightarrow\ \boxed{c=236.8\ \text{kN/m}^2}$$

(The high $c$ and low $\phi$ show a stiff, cohesive clay, typical of an undrained test.)

*Graphical method.* Draw on the $\sigma$–$\tau$ plane the two Mohr circles on the diameters $100$–$670$ (centre 385, radius 285) and $200$–$800$ (centre 500, radius 300), then draw the common tangent to both circles. Its intercept on the $\tau$ axis is $c\approx237$ kN/m² and its inclination to the $\sigma$ axis is $\phi\approx7.5^\circ$, which confirms the analytical result.

```figure caption="Graphical solution: Mohr circles for specimens 1 and 2 and the common tangent (failure envelope), giving c ≈ 237 kN/m² and φ ≈ 7.5°."
fig,ax=plt.subplots(figsize=(5.4,2.9)); ax.set_aspect("equal")
th=np.linspace(0,np.pi,200)
for a,b,col in [(100,670,ACCENT),(200,800,"#2e8b57")]:
    ax.plot((a+b)/2+(b-a)/2*np.cos(th),(b-a)/2*np.sin(th),color=col,lw=1.8)
phi=np.radians(7.4947); c=236.806; sg=np.array([-40,860]); ax.plot(sg,c+sg*np.tan(phi),color="#d9534f",lw=1.5)
ax.axhline(0,color=INK,lw=0.9); ax.axvline(0,color=INK,lw=0.9)
ax.plot([0],[c],"o",color="#d9534f",ms=4); ax.text(15,c-32,"c = 237",fontsize=8.5,color="#d9534f"); ax.text(620,c+620*np.tan(phi)+14,"φ = 7.5°",fontsize=8.5,color="#d9534f")
ax.text(100,-45,"100",fontsize=7.5,ha="center"); ax.text(670,-45,"670",fontsize=7.5,ha="center"); ax.text(200,-45,"200",fontsize=7.5,ha="center"); ax.text(800,-45,"800",fontsize=7.5,ha="center")
ax.set_xlim(-50,880); ax.set_ylim(-70,340); ax.set_xlabel("σ (kN/m²)",fontsize=8.5); ax.set_ylabel("τ",fontsize=8.5); ax.tick_params(labelsize=7)
```

**(c) Critical state line (CSL).** In critical state soil mechanics a soil sheared to large strain reaches a *critical state*, at which it continues to deform at constant stress ($p'$, $q$) and constant volume (void ratio $e_{cs}$). The locus of all critical-state points is the CSL, and it is unique for a soil independent of the drainage and the stress path. It is defined in two planes:

- **From the triaxial test** ($q$–$p'$ plane, $p'=\tfrac{\sigma'_1+2\sigma'_3}{3}$, $q=\sigma_1-\sigma_3$): the failure points of CD and CU tests at large strain lie on a straight line through the origin,

$$\begin{gathered}q_{cs}=Mp'_{cs} \\ M=\frac{6\sin\phi'_{cs}}{3-\sin\phi'_{cs}}\end{gathered}$$

- **From the consolidation test** ($e$–$\ln p'$ plane): the isotropic normal consolidation line is $e_N-\lambda\ln p'$ (slope $\lambda$, equivalent to $C_c/2.303$), and the CSL is parallel to it, lying below it by $\ln 2$-related distance:

$$\begin{gathered}e_{cs}=e_\Gamma-\lambda\ln p'_{cs} \\ e_\Gamma=e_N-(\lambda-\kappa)\ln2\end{gathered}$$

where $\kappa=C_s/2.303$ is the slope of the swelling line. Together, the CSL is a line in the three-dimensional space ($p'$, $q$, $e$) and a soil state lying on the "dry" side (heavily overconsolidated) dilates and shows a peak, while on the "wet" side (lightly overconsolidated or normally consolidated) it contracts, both finishing on the CSL.

```figure caption="Critical state line: (left) in the q–p' plane it is a straight line q = M p' ; (right) in the e–ln p' plane it is parallel to the normal consolidation line (NCL), below it."
fig,axs=plt.subplots(1,2,figsize=(5.8,2.6))
p=np.linspace(0,10,10); axs[0].plot(p,0.9*p,color="#d9534f",lw=2); axs[0].text(6,5.9,"CSL: q = M p'",fontsize=8,color="#d9534f",rotation=33); axs[0].annotate("",xy=(4,3.6),xytext=(0,0),arrowprops=dict(arrowstyle="->",color=ACCENT,lw=1.1)); axs[0].text(1.5,0.2,"M = slope",fontsize=7.5)
axs[0].set_xlabel("p'",fontsize=8.5); axs[0].set_ylabel("q",fontsize=8.5); axs[0].set_xlim(0,10); axs[0].set_ylim(0,9)
lp=np.linspace(1,3,10); axs[1].plot(lp,2.0-0.4*(lp-1),color=ACCENT,lw=2); axs[1].plot(lp,1.72-0.4*(lp-1),color="#d9534f",lw=2); axs[1].plot(lp,2.0-0.06*0-0.4*(lp-1),lw=0)
axs[1].text(1.9,1.5,"NCL (slope −λ)",fontsize=7.5,color=ACCENT,rotation=-17); axs[1].text(1.9,1.2,"CSL (slope −λ)",fontsize=7.5,color="#d9534f",rotation=-17)
axs[1].set_xlabel("ln p'",fontsize=8.5); axs[1].set_ylabel("e",fontsize=8.5)
for a in axs: a.tick_params(labelsize=0); a.grid(True,color=GRID,lw=0.5)
fig.tight_layout()
```

@s 7
**(a) Modified Proctor and Harvard miniature tests.**

| Feature | Modified Proctor test | Harvard miniature compaction test |
|---|---|---|
| Purpose | Laboratory compaction for heavy structures (highways, airfields) with heavy rollers | Small-scale compaction for small samples and research, to simulate field kneading compaction |
| Mould | 100 mm dia × 127.3 mm high (1000 cc) | 33.3 mm dia × 71.6 mm high (about 62 cc) |
| Compaction tool | 4.9 kg rammer, 450 mm drop (impact) | Spring-loaded tamper (about 178 N, 40 lbf), kneading action |
| Layers and blows | 5 layers, 25 blows per layer | 3 layers, 25 tamps per layer |
| Energy | about 2700 kJ/m³ (4.5 × standard) | variable (adjustable by spring and number of tamps) |
| Sample size | 5–6 kg; particles ≤ 19 mm | about 200 g; fine soils |
| Result | Higher $\gamma_{d,max}$, lower OMC | Fabric and strength similar to field kneading; simulates sheepsfoot roller |

**(b) Standard compaction test.** Bulk density $\rho=m/1000$ g/cc and dry density $\rho_d=\rho/(1+w)$:

| $w$ (%) | 10 | 11 | 12 | 13 | 14.5 | 16 |
|---|---|---|---|---|---|---|
| $\rho$ (kg/m³) | 1700 | 1800 | 1850 | 1875 | 1750 | 1600 |
| $\rho_d$ (kg/m³) | 1545.5 | 1621.6 | 1651.8 | 1659.3 | 1528.4 | 1379.3 |
| $\rho_{d,zav}$ ($G=2.7$) | 2126.0 | 2081.1 | 2038.3 | 1997.3 | 1941.9 | 1886.4 |

(zero-air-void: $\rho_{d,zav}=\dfrac{G\rho_w}{1+wG}$ at the same water contents.)

*(a) Compaction curve.* The peak of the smooth curve through the points (a parabola fitted through the points near the peak) is at

$$\boxed{w_{opt}\approx12.3\%,\qquad \rho_{d,max}\approx1664\ \text{kg/m}^3}$$

(the measured point with the highest density is 1659 kg/m³ at 13 %.)

*(b) Zero-air-void line.* It is the curve of the last row of the table and lies above the compaction curve everywhere, so the compaction curve cannot cross it.

```figure caption="Compaction curve with the zero-air-void line (G = 2.7). The × marks the fitted peak: OMC ≈ 12.3 %, maximum dry density ≈ 1664 kg/m³; the dashed horizontal line is the field dry density 1650 kg/m³."
from scipy.interpolate import PchipInterpolator
w=np.array([10,11,12,13,14.5,16.]); rd=np.array([1545.5,1621.6,1651.8,1659.3,1528.4,1379.3])
pf=np.polyfit(w[1:5],rd[1:5],2); wo=-pf[1]/(2*pf[0]); rm=np.polyval(pf,wo)
fig,ax=plt.subplots(figsize=(5.0,3.1)); ww=np.linspace(9,17,100)
ax.plot(ww,2700/(1+ww/100*2.7),color="#d9534f",lw=1.4,ls="--",label="zero-air-void line (G = 2.7)")
wc=np.linspace(10,16,100); ax.plot(wc,PchipInterpolator(w,rd)(wc),color=ACCENT,lw=2,label="compaction curve"); ax.plot(w,rd,"o",color=ACCENT,ms=4)
ax.plot([wo],[rm],"x",color=INK,ms=8,mew=2); ax.plot([wo,wo],[1350,rm],color=MUTED,lw=0.8,ls=":"); ax.text(wo+0.1,1400,f"OMC ≈ {wo:.1f} %",fontsize=8)
ax.axhline(1650,color="#2e8b57",lw=1,ls="--"); ax.text(15.0,1660,"field 1650",fontsize=7.5,color="#2e8b57")
ax.text(9.1,rm+12,f"ρ$_{{d,max}}$ ≈ {rm:.0f}",fontsize=8)
ax.set_xlabel("water content w (%)",fontsize=8.5); ax.set_ylabel("dry density (kg/m³)",fontsize=8.5); ax.set_ylim(1350,2200); ax.legend(fontsize=7.5); ax.grid(True,color=GRID,lw=0.6); ax.tick_params(labelsize=7.5)
```

*Relative compaction* (field dry density to the laboratory maximum):

$$\boxed{RC=\frac{\rho_{d,field}}{\rho_{d,max}}\times100=\frac{1650}{1664}\times100\approx99.1\%}$$

(Using the highest measured density, 1659 kg/m³, gives 99.4 %.) This is just under the usual specification of 95–100 % of standard Proctor density, so the field compaction is satisfactory.

---
file: NEBians-IOE-Past-Paper-Engineering-Hydrology-ENCE306-2082-Chaitra.pdf
subject: Engineering Hydrology
level: BE · Year III / Part I
code: ENCE 306
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular exam (new course), BE Civil (BCE), Year III / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
How hydrological boundary at an outlet point is delineated? What is drainage density? [[3+1]]

@q 2
a) Explain the methods of estimating the missing rainfall data at the rain gauge stations. [[4]]

b) What criteria should be adopted for the optimum location of a rain gauge? A drainage basin is monitored with eight rainfall gauging stations, and the annual rainfall observed is as follows: 120, 135.5, 150.4, 165, 180.6, 195.4, 160, 145.7. If the allowable error in estimating the mean annual rainfall is 5%, determine the number of additional rainfall gauges if required. [[4]]

@q 3
a) What is Φ-index? How is it different from W-index? [[2]]

b) Estimate the potential evapotranspiration (PET) for an agricultural field near Birgunj during April using Penman's method, given: mean temperature = 28 °C; mean relative humidity = 70 %; wind speed at 2 m height = 2.5 m/s; net radiation = 10.5 mm/day (equivalent evaporation); slope of saturation vapour pressure curve (Δ) = 1.8 mmHg/°C; psychrometric constant (γ) = 0.66 mmHg/°C; saturation vapour pressure (e<sub>s</sub>) = 28.4 mmHg; actual vapour pressure (e<sub>a</sub>) = 17.0 mmHg. (Handwritten on the paper: mean monthly solar radiation = 15 mm of water/day.) [[6]]

@q 4
What is meant by rainfall–runoff modelling? Explain its basic components with a simple diagram. [[5]]

@q 5
a) What is rating curve? Explain the parameters of rating equation. [[3]]

b) During stream gauging of Kankai river at Domukha, the following observations were taken using a current meter. Observation time at each vertical = 120 s. Estimate the total discharge of the river using the velocity–area method. The rating equation of the current meter is given as v = (0.28N + 0.04) m/s. [[5]]

| Distance from left bank (m) | Depth (m) | Number of revolutions at 0.2d | Number of revolutions at 0.8d |
|---|---|---|---|
| 0.0 | – | – | – |
| 2.0 | 1.4 | 292 | 198 |
| 4.5 | 2.1 | 359 | 255 |
| 7.0 | 2.5 | 389 | 278 |
| 9.5 | 1.9 | 327 | 229 |
| 12.0 | 1.2 | 241 | 170 |
| 14.0 | – | – | – |

@q 6
a) Why do we need to separate base flow in hydrograph analysis? Describe the methods to separate base flow. [[4]]

b) A 4 hour unit hydrograph of a sub-catchment of the Gandaki river basin near Pokhara is given below: [[8]]

| Time (hr) | 0 | 4 | 8 | 12 | 16 | 20 | 24 | 28 | 32 |
|---|---|---|---|---|---|---|---|---|---|
| 4-hr UH (m³/s per cm) | 0 | 22 | 58 | 92 | 80 | 60 | 38 | 18 | 0 |

(i) Using the S-curve method, derive the 6-hour Unit Hydrograph for the catchment.

(ii) Determine peak discharge of the 6-hour UH as well as time to peak.

@q 7
a) Define flash flood. Discuss the major causes of flash floods. Explain how climate change influences the occurrence and intensity of flash floods. [[4]]

b) Flood frequency computations for the river Koshi at Chatara station give the following results. Estimate the flood magnitude with a return period of 500 years. [[6]]

| Return period T (years) | Peak flood (m³/s) |
|---|---|
| 50 | 35820 |
| 100 | 47380 |

@q 8
Using the Muskingum method route the following hydrograph through a channel reach for which K = 10 hours and x = 0.3. At the start of the inflow flood, the outflow discharge is 8 m³/s. [[5]]

| Time (hr) | 0 | 6 | 12 | 18 | 24 | 30 | 36 | 42 | 48 | 54 |
|---|---|---|---|---|---|---|---|---|---|---|
| Inflow (m³/s) | 14 | 24 | 54 | 64 | 59 | 49 | 39 | 32 | 24 | 19 |

<!-- SOLUTIONS -->

@s 1
**Delineation of the hydrological boundary (watershed / catchment divide) at an outlet point.** The boundary is the line that separates the area whose surface runoff drains to the chosen outlet from the neighbouring areas. It is drawn on a **contour (topographic) map**, or on a DEM in GIS:

1. Mark the **outlet (gauging) point** on the stream and trace the main stream and all its tributaries (the blue lines) upstream of it.
2. Starting at the outlet, move along **the highest ground** on either side, so that every point of the line is higher than the ground on its basin side. The line crosses the contour lines at **right angles** (it follows the line of steepest ascent from the stream to the ridge).
3. It passes through the **peaks, ridges and saddles (cols)** that enclose the stream network. It never crosses a stream, except at the outlet.
4. Continue around the head of the basin and return to the outlet. The closed curve is the **watershed boundary**; the area inside (planimeter, grid or GIS) is the catchment area $A$.
5. In GIS: fill the sinks of the DEM, compute flow direction (D8) and flow accumulation, snap the pour point to the cell of highest accumulation, and delineate the cells that drain to it.

```figure caption="Question 1: a watershed boundary (dashed) drawn on a contour map. The divide crosses the contours at right angles, passes over ridges and saddles and closes at the outlet; the stream and its tributaries lie inside."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.5)); ax.axis("off"); ax.set_aspect("equal")
th=np.linspace(0,2*np.pi,400)
for k,s in enumerate([1.0,0.78,0.58,0.40,0.22]):
    r=s*(1+0.12*np.sin(3*th+0.6))
    ax.plot(4*r*np.cos(th)*1.05,3.1*r*np.sin(th)-0.15,color="#b08a4a",lw=0.8)
rb=1+0.12*np.sin(3*th+0.6)
ax.plot(4.35*rb*np.cos(th)*1.05,3.4*rb*np.sin(th)-0.15,color=ACCENT,lw=1.6,ls="--")
# stream
ax.plot([0,0.3,-0.4,0.2,0],[3,1.8,0.8,-0.6,-3.15],color="#2b6cb0",lw=1.8)
ax.plot([-2.2,-1.2,-0.4],[1.6,1.3,0.8],color="#2b6cb0",lw=1.2); ax.plot([2.2,1.2,0.3],[1.1,0.4,0.2],color="#2b6cb0",lw=1.2)
ax.plot(0,-3.15,"o",color=INK,ms=6); ax.text(0.25,-3.45,"outlet",fontsize=8)
ax.text(-3.5,2.9,"ridge / divide",fontsize=8,color=ACCENT); ax.text(-1.1,0,"catchment A",fontsize=8.5,color=INK)
ax.set_xlim(-5,5); ax.set_ylim(-3.8,3.8)
```

**Drainage density.** It is the total length of all streams (perennial and intermittent) in the basin divided by the basin area:

$$ D_d = \frac{\sum L}{A}\ \ \text{(km/km}^2\text{)} $$

A **high** $D_d$ (steep, impermeable, sparsely vegetated, fine textured basins; 5–50 km/km²) means a fast response and a peaky hydrograph; a **low** $D_d$ (permeable, flat, vegetated, coarse textured basins) means a slow response and higher infiltration.

@s 2
**(a) Missing rainfall at a gauge.** Let the station $X$ miss a record. Use the neighbouring **index stations** $A, B, C,\dots$ (preferably at least 3, evenly spread around $X$). Let $N_x$ be the normal annual rainfall at $X$ and $N_A, N_B, \dots$ those at the index stations, $P_A, P_B,\dots$ the rainfall of the same storm / period at the index stations.

1. **Simple arithmetic mean method.** If the normal annual rainfall of each index station is **within 10 %** of $N_x$:

$$ P_x = \frac{1}{n}\left(P_A + P_B + \dots + P_n\right) $$

2. **Normal ratio method.** If the normals differ by **more than 10 %**, each index value is weighted by the ratio of normals:

$$ P_x = \frac{1}{n}\left(\frac{N_x}{N_A}P_A + \frac{N_x}{N_B}P_B + \dots + \frac{N_x}{N_n}P_n\right) $$

3. **Inverse distance weighting.** The nearer the station, the larger its weight ($d_i$ is the distance from $X$ to station $i$, $b$ commonly 2):

$$ P_x = \frac{\sum P_i / d_i^{\,b}}{\sum 1 / d_i^{\,b}} $$

4. **Regression / correlation method.** A relation $P_x = a + bP_A$ (or a multiple regression on several stations) is fitted from the concurrent record and used to fill the gap.
5. **Isohyetal / spatial interpolation (kriging, Thiessen) method.** The isohyets of the storm are drawn from the surrounding stations and the missing value is read off at $X$.

Before the filled data are used, a **double mass curve** check is advisable to detect an inconsistent record (a change in gauge exposure, relocation).

**(b) Optimum location of a rain gauge.** A gauge should give a record that is **representative of the area**, and it must be reliable:

- Sited on **level, open ground**, not on a slope, roof top or windy summit; the surface is covered by short grass or gravel (no splash).
- **Distance from obstructions** (trees, buildings, fences) at least **2 to 4 times the height of the obstruction** (the 45° rule), so wind eddies and shelter do not alter the catch.
- The **funnel rim is horizontal at a standard height** (0.3 m above the ground for a non-recording gauge in Nepal practice), fenced against animals and tampering.
- **Easily accessible** all year to the observer, and reasonably close to a road/settlement, with the network density meeting the **WMO guidelines** (for the hills and the mountains one gauge for 100 to 250 km², for the plains 600 to 900 km²) and some gauges at **different altitudes** to represent the orographic effect.
- The site should be **permanent** and free from the future building or the vegetation growth.

**Optimum number of gauges.** Let $\bar P$ be the mean and $\sigma$ the standard deviation of the existing records:

$$\begin{gathered}N = \left(\frac{C_v}{\varepsilon}\right)^2 \\ C_v = \frac{100\,\sigma_{n-1}}{\bar P}\end{gathered}$$

| Quantity | Value |
|---|---|
| $n$ | 8 |
| Mean $\bar P = \dfrac{1252.6}{8}$ | 156.575 mm |
| Standard deviation $\sigma_{n-1}$ | 24.218 mm |
| $C_v = 100(24.218)/156.575$ | 15.47 % |
| Allowable error $\varepsilon$ | 5 % |

$$ N = \left(\frac{15.47}{5}\right)^2 = 9.57 \approx 10 $$

$$ \boxed{\text{Additional gauges} = 10 - 8 = 2} $$

@s 3
**(a) Φ-index and W-index.**

- The **Φ-index** is the **constant rate of rainfall** (cm/h or mm/h) above which the rainfall volume just equals the **direct runoff volume**. It lumps all the abstractions (interception, depression storage, infiltration and evaporation) into the single constant rate: rain below Φ is assumed all lost, the excess above is the effective rainfall. It is found by trial from the hyetograph and the observed runoff depth.
- The **W-index** is the **average infiltration rate** during the time rainfall intensity exceeds the infiltration capacity:

$$ W = \frac{P - R - S}{t_r} $$

where $P$ is the total storm precipitation, $R$ the direct runoff, $S$ the **depression and interception storage**, and $t_r$ the time for which the intensity exceeds the capacity.

The difference: the W-index **deducts the initial storage losses** ($S$), so it represents the infiltration alone and is **more accurate**, while the Φ-index includes **all** abstractions (so $\Phi > W$ for the same storm: $\Phi$ treats $S$ as part of the loss spread over the whole storm). W-index needs data on the storage, Φ-index does not. Because $W$ varies with the antecedent moisture, the two coincide only if the initial losses are negligible (wet catchments, large storms).

**(b) PET by the Penman method.** Penman's combined (energy-balance plus aerodynamic) equation, in terms of the equivalent evaporation of the net radiation $H_n$:

$$ \text{PET} = \frac{A\,H_n + \gamma\,E_a}{A + \gamma} $$

with the **drying power of the air**

$$ E_a = 0.35\left(1 + \frac{u_2}{160}\right)(e_s - e_a)\ \text{mm/day} $$

where $u_2$ is the wind speed at 2 m in km/day.

Wind speed: $u_2 = 2.5\ \text{m/s} \times 86.4 = 216\ \text{km/day}$.

$$ E_a = 0.35\left(1+\frac{216}{160}\right)(28.4-17.0) = 0.35(2.35)(11.4) = 9.377\ \text{mm/day} $$

$$ \text{PET} = \frac{1.8(10.5) + 0.66(9.377)}{1.8+0.66} = \frac{18.90 + 6.189}{2.46} = 10.20\ \text{mm/day} $$

$$ \boxed{\text{PET} \approx 10.2\ \text{mm/day}\ (\approx 306\ \text{mm for the 30 days of April})} $$

*Note.* The net radiation $H_n$ is given directly, so the handwritten "mean monthly solar radiation = 15 mm/day" (cut off at the edge of the scan) is not needed; it would be used only if $H_n$ had to be computed from the sunshine hours. The relative humidity is already contained in $e_a = 0.70 \times 28.4 \approx 19.9$ mmHg, but the paper gives $e_a = 17.0$ mmHg, which is used as printed.

@s 4
**Rainfall–runoff modelling** is the representation of the **transformation of catchment rainfall into the streamflow at the outlet** by a mathematical (or physical) model. The catchment is treated as a system: the **input** is the rainfall (and the evaporation demand), the **output** is the discharge hydrograph, and the model describes the processes between them. The purposes are the design flood and flood forecasting, the water resources and the effect of land-use change, and the prediction of the flow in the ungauged basins.

**Basic components.**

1. **Input:** the precipitation $P(t)$ (the areal average from the gauges or the radar), plus the potential evapotranspiration PET.
2. **Loss (production) module:** the **abstractions**: interception, depression storage, infiltration (Horton, Green–Ampt, Φ-index, SCS-CN), and evapotranspiration, subtracted from $P$ to give the **effective (excess) rainfall** $P_e$ (and the soil moisture accounting).
3. **Transformation (transfer / routing) module:** converts $P_e$ to the **direct runoff** hydrograph on the surface and the channel: unit hydrograph (Snyder, SCS, Clark), kinematic wave, or the linear reservoir, with the channel routing (Muskingum).
4. **Base flow (sub-surface / groundwater) module:** the delayed contribution from the groundwater storage (a linear reservoir or the recession).
5. **Output and calibration:** the simulated hydrograph $Q(t)$ is compared with the observed one, the parameters are **calibrated** and the model is **validated** by a different period (the efficiency measures: Nash–Sutcliffe, $R^2$, bias).

Models are classified as **empirical (black box), conceptual (HEC-HMS, HBV, Sacramento), or physically based** (MIKE-SHE), and **lumped or distributed**.

```figure caption="Question 4: components of a simple rainfall–runoff model: input, loss (abstractions), transformation to direct runoff, baseflow, and the simulated outflow compared with the observed one for calibration."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.2,3.0)); ax.axis("off")
def box(x,y,w,h,t,fc="#eef2fb"):
    ax.add_patch(mp.FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc=fc,ec=INK,lw=0.9)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=5.4)
ar=dict(arrowstyle="-|>",color=ACCENT,lw=1.3)
box(0,2.2,1.9,1.2,"INPUT\nrainfall P(t)\n+ PET")
box(3.0,2.2,2.3,1.2,"LOSSES\ninterception, depression\nstorage, infiltration, ET")
box(6.4,2.2,2.3,1.2,"TRANSFORMATION\neffective rain Pe → direct\nrunoff (unit hydrograph)")
box(9.8,1.0,2.0,1.2,"OUTPUT\nstreamflow Q(t)\nat the outlet",fc="#fdf1dd")
box(6.4,0.0,2.3,1.0,"BASEFLOW\n(groundwater store)",fc="#e8f4ea")
ax.annotate("",xy=(3.0,2.8),xytext=(1.9,2.8),arrowprops=ar); ax.annotate("",xy=(6.4,2.8),xytext=(5.3,2.8),arrowprops=ar)
ax.annotate("",xy=(10.4,2.2),xytext=(8.7,2.8),arrowprops=ar); ax.annotate("",xy=(9.8,1.3),xytext=(8.7,0.5),arrowprops=ar)
ax.annotate("",xy=(6.4,0.7),xytext=(4.9,2.2),arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1,ls="--"))
ax.text(4.5,1.2,"percolation",fontsize=6.8,color=MUTED)
ax.text(10.8,0.35,"compare with observed Q\n→ calibrate parameters",ha="center",fontsize=6.5,color=MUTED)
ax.set_xlim(-0.3,12.2); ax.set_ylim(-0.3,3.7)
```

@s 5
**(a) Rating curve.** The **stage–discharge relation** of a river section: the graph of the discharge $Q$ (m³/s) against the gauge height (stage) $G$ at a station, prepared from many simultaneous stage and discharge (current-meter) measurements. Once established, the continuous stage record is converted into the discharge. The curve is normally a parabola; it is extended beyond the measured range on the log paper or by the slope–area method.

**Rating equation** (the simple, steady-flow, single-valued type):

$$ Q = C_r\,(G - a)^{\,\beta} $$

- $Q$ = discharge;
- $G$ = observed stage (gauge height);
- $a$ = the **stage at zero discharge** (the gauge reading when $Q = 0$, the datum correction, found by trial so that $\log Q$ against $\log(G-a)$ plots as a straight line);
- $C_r$ = **rating constant** (the discharge when $G - a = 1$ m, depends on the channel shape and the roughness);
- $\beta$ = **rating exponent** (the slope of the log–log straight line; 1.3 to 1.8 typically, about 1.5 for a rectangular section as in the weir, 2 for a triangular one, about 1.67 for a wide natural channel).

$C_r$ and $\beta$ are obtained by the least squares fit of $\log Q = \log C_r + \beta\log(G-a)$.

**(b) Velocity–area method (mid-section method).** Each vertical's mean velocity is the average of the velocities at 0.2$d$ and 0.8$d$, with $N$ (revolutions per second) $=$ revolutions/120 s and $v = 0.28N + 0.04$. The discharge in the section represented by a vertical is $q_i = v_i\,d_i\,w_i$, with the width $w_i = (x_{i+1} - x_{i-1})/2$ (the end verticals at 0 and 14 m have zero depth).

For the vertical at 2.0 m:

$$ N_{0.2} = \frac{292}{120} = 2.433,\quad v_{0.2} = 0.28(2.433)+0.04 = 0.7213\ \text{m/s} $$

$$ N_{0.8} = \frac{198}{120} = 1.650,\quad v_{0.8} = 0.28(1.650)+0.04 = 0.5020\ \text{m/s},\quad v_m = 0.6117\ \text{m/s} $$

| $x$ (m) | $d$ (m) | $w$ (m) | $v_{0.2}$ | $v_{0.8}$ | $v_m$ (m/s) | $a = wd$ (m²) | $q = v_m a$ (m³/s) |
|---|---|---|---|---|---|---|---|
| 2.0 | 1.4 | 2.25 | 0.7213 | 0.5020 | 0.6117 | 3.150 | 1.927 |
| 4.5 | 2.1 | 2.50 | 0.8777 | 0.6350 | 0.7563 | 5.250 | 3.971 |
| 7.0 | 2.5 | 2.50 | 0.9477 | 0.6887 | 0.8182 | 6.250 | 5.114 |
| 9.5 | 1.9 | 2.50 | 0.8030 | 0.5743 | 0.6887 | 4.750 | 3.271 |
| 12.0 | 1.2 | 2.25 | 0.6023 | 0.4367 | 0.5195 | 2.700 | 1.403 |
| **Total** | | | | | | **22.10** | **15.68** |

$$ \boxed{Q = \sum q_i \approx 15.7\ \text{m}^3/\text{s}} $$

The mean velocity of the section is $15.68/22.10 = 0.71$ m/s.

```figure caption="Question 5(b): the gauged cross-section of the Kankai river at Domukha with the verticals and their mid-section widths; discharge in each strip q (m³/s) is printed."
fig,ax=plt.subplots(figsize=(5.6,2.5))
x=[0,2,4.5,7,9.5,12,14]; d=[0,1.4,2.1,2.5,1.9,1.2,0]; q=[None,1.927,3.971,5.114,3.271,1.403,None]
ax.fill_between(x,0,[-v for v in d],color="#c9dff2",alpha=0.8); ax.plot(x,[-v for v in d],color=INK,lw=1.4,marker="o",ms=3.5)
ax.axhline(0,color="#2b6cb0",lw=1)
for xi,di,qi in zip(x,d,q):
    if qi: ax.plot([xi,xi],[0,-di],color=MUTED,lw=0.8,ls=":"); ax.text(xi,0.25,f"q={qi:.2f}",ha="center",fontsize=7,color=ACCENT)
ax.set_xlabel("distance from left bank (m)",fontsize=8); ax.set_ylabel("depth (m)",fontsize=8); ax.tick_params(labelsize=7); ax.set_ylim(-3,0.8); ax.grid(True,color=GRID,lw=0.5)
fig.tight_layout()
```

@s 6
**(a) Why separate the base flow.** The **total streamflow hydrograph** = **direct runoff** (surface runoff + prompt interflow) + **base flow** (the delayed groundwater flow). The **unit hydrograph theory** applies to the direct runoff only, so, to derive the UH, to compute the **effective rainfall** (from the direct runoff volume by the Φ-index, SCS-CN), to estimate the **runoff coefficient**, to know the **groundwater contribution** and to design the floods, the base flow must be separated from the storm hydrograph.

**Methods of base flow separation** (all start from the point $A$ where the rising limb begins, the base flow before the storm is the recession of the earlier flow):

1. **Straight line method.** Join the beginning of the rising limb $A$ to the point $B$ on the recession limb where the direct runoff ends, by a straight horizontal (or a straight sloping) line. $B$ is at $N$ days after the peak: 

$$ N = 0.827\,A^{0.2}\quad (A\ \text{in km}^2,\ N\ \text{in days}) $$

2. **Fixed base length method.** From $A$ draw the base flow recession, extended to the time of the peak; at the time $N$ days after the peak mark $B$ and join the point under the peak to $B$ by a straight line. The fixed base length is thus $N$ plus the time to peak.
3. **Variable slope (concave) method.** Extend the base flow recession curve **backward** from the end of the direct runoff to under the peak, and the recession **forward** from $A$ to the time of peak; join the two ends by a straight line to the point of **inflexion (concavity) on the recession limb**.
4. **Master recession curve / semilogarithmic method.** The recession limb plots as a straight line on the log scale ($Q_t = Q_0K_r^{t}$); the point where it departs from the straight line marks the end of the direct runoff.

The straight line is the simplest and is used for small catchments; the variable-slope method is more physical for the large ones.

**(b) 6-hour UH from the 4-hour UH by the S-curve.**

*Step 1: S-curve.* An S-curve (summation curve) is the hydrograph due to a **continuous effective rainfall of 1 cm per 4 h** (i.e. the intensity 0.25 cm/h), obtained by adding the 4-hr UH ordinates, each lagged by 4 hours:

$$ S(t) = \sum_{k=0}^{t/4} U_4(t - 4k) $$

| $t$ (h) | 0 | 4 | 8 | 12 | 16 | 20 | 24 | 28 | 32 | 36 |
|---|---|---|---|---|---|---|---|---|---|---|
| $U_4$ | 0 | 22 | 58 | 92 | 80 | 60 | 38 | 18 | 0 | 0 |
| $S(t)$ | 0 | 22 | 80 | 172 | 252 | 312 | 350 | 368 | 368 | 368 |

The S-curve reaches its **equilibrium discharge of 368 m³/s** at 28 h; this is the sum of the UH ordinates. With 1 cm of rain per 4 h the equilibrium discharge is $Q_e = A\times 0.01\ \text{m}/(4\times3600\ \text{s})$, so the catchment area is

$$ A = \frac{368\,(4\times 3600)}{0.01} = 5.30\times 10^{8}\ \text{m}^2 \approx 530\ \text{km}^2 $$

*Step 2: shift and subtract.* Lag the S-curve by the new duration $t_r' = 6$ h, giving $S(t-6)$. The difference $S(t) - S(t-6)$ is the hydrograph of **6 h of rain at 0.25 cm/h = 1.5 cm**, so the 6-hour UH (for 1 cm) is scaled by $t_r/t_r' = 4/6$:

$$ U_6(t) = \frac{4}{6}\left[S(t) - S(t-6)\right] $$

The S-curve is read at the 2-hour interval (linear interpolation between the 4-hourly points):

| $t$ (h) | $S(t)$ | $S(t-6)$ | $S(t)-S(t-6)$ | $U_6 = \tfrac{4}{6}\times$ (m³/s per cm) |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 2 | 11 | 0 | 11 | 7.33 |
| 4 | 22 | 0 | 22 | 14.67 |
| 6 | 51 | 0 | 51 | 34.00 |
| 8 | 80 | 11 | 69 | 46.00 |
| 10 | 126 | 22 | 104 | 69.33 |
| 12 | 172 | 51 | 121 | 80.67 |
| 14 | 212 | 80 | 132 | **88.00** |
| 16 | 252 | 126 | 126 | 84.00 |
| 18 | 282 | 172 | 110 | 73.33 |
| 20 | 312 | 212 | 100 | 66.67 |
| 22 | 331 | 252 | 79 | 52.67 |
| 24 | 350 | 282 | 68 | 45.33 |
| 26 | 359 | 312 | 47 | 31.33 |
| 28 | 368 | 331 | 37 | 24.67 |
| 30 | 368 | 350 | 18 | 12.00 |
| 32 | 368 | 359 | 9 | 6.00 |
| 34 | 368 | 368 | 0 | 0 |

(At the 6-hourly points only: 0, 34.0, 80.7, 73.3, 45.3, 12.0, 0 at $t = 0, 6, 12, \dots, 36$ h.)

*Check:* the area under the 6-hour UH is the same as under the 4-hour UH (1 cm over 530 km²):

$$ 2\ \text{h}\times 736\ \text{m}^3/\text{s} = 4\ \text{h}\times 368\ \text{m}^3/\text{s} = 1472\ \text{m}^3\text{/s}\cdot\text{h} \quad\checkmark $$

**(ii)** The 6-hour unit hydrograph has

$$ \boxed{Q_p \approx 88\ \text{m}^3/\text{s per cm at the time to peak } t_p \approx 14\ \text{h}} $$

(and the base is about 34 h). With only 6-hourly ordinates the largest ordinate is 80.7 m³/s at 12 h, but the 2-hourly reading above is the better estimate of the true peak.

```figure caption="Question 6(b): the S-curve of the 4-hour unit hydrograph (equilibrium 368 m³/s), the S-curve lagged by 6 h, and the derived 6-hour unit hydrograph (peak 88 m³/s per cm at 14 h) compared with the 4-hour one."
t4=np.arange(0,49,4); u4=np.array([0,22,58,92,80,60,38,18,0,0,0,0,0]); S=np.cumsum(u4)
tt=np.arange(0,49,2); Sf=np.interp(tt,t4,S); Sl=np.interp(tt-6,t4,S,left=0)
u6=(Sf-Sl)*4/6
fig,axs=plt.subplots(1,2,figsize=(6.2,2.8))
a=axs[0]; a.plot(t4,S,color=ACCENT,lw=1.8,marker="o",ms=3,label="S(t)"); a.plot(tt+6,Sf,color=INK,lw=1.2,ls="--",label="S(t−6)"); a.axhline(368,color=MUTED,lw=0.7,ls=":")
a.set_xlim(0,44); a.set_xlabel("t (h)",fontsize=8); a.set_ylabel("m³/s",fontsize=8); a.legend(fontsize=7); a.grid(True,color=GRID,lw=0.5); a.tick_params(labelsize=7); a.set_title("S-curve and lagged S-curve",fontsize=8)
b=axs[1]; b.plot(t4[:9],u4[:9],color=MUTED,lw=1.3,marker="s",ms=3,label="4-h UH"); b.plot(tt[:18],u6[:18],color=ACCENT,lw=1.8,marker="o",ms=3,label="6-h UH")
b.annotate("88 at 14 h",xy=(14,88),xytext=(18,95),fontsize=7.5,arrowprops=dict(arrowstyle="->",color=INK,lw=0.7))
b.set_xlabel("t (h)",fontsize=8); b.set_ylabel("m³/s per cm",fontsize=8); b.legend(fontsize=7); b.grid(True,color=GRID,lw=0.5); b.tick_params(labelsize=7); b.set_title("derived 6-hour UH",fontsize=8); b.set_ylim(0,110)
fig.tight_layout()
```

@s 7
**(a) Flash flood.** A **sudden, very rapid rise of the water level (a few minutes to about 6 hours after the causative event) in a small, steep catchment**, with high velocity and large debris/sediment load, usually of short duration, giving very little warning time (common in the Nepal hills, e.g. the Melamchi 2021 and the Budhi Gandaki floods).

**Major causes.**

1. **Intense, short-duration rainfall** (cloudburst, convective storms, the monsoon bursts on the steep windward slopes);
2. **Glacial lake outburst floods (GLOF)** and the failure of the **landslide / moraine / ice dams** (the natural dam break), and the **failure of man-made dams** or the embankments;
3. **Steep slopes, thin soil, rocky and impervious terrain** and small time of concentration; **antecedent saturated soil**; the **deforestation, urbanisation** and road construction without drainage (the more runoff, the less infiltration);
4. **Snow and ice melt** with rain on snow; and the **blocked channels and bridges** by debris (flow surges).

**Effect of climate change.**

- A **warmer atmosphere holds about 7 % more moisture per °C** (the Clausius–Clapeyron relation), so that the **extreme rainfall intensities increase** and the cloudbursts are more frequent, with the **monsoon more erratic** (the longer dry spells and the heavier bursts).
- **Faster glacier and snow melt** forms more and larger **glacial lakes**, increasing the **GLOF** risk in the Himalaya; the **permafrost thaw** destabilises slopes and **landslide dams**.
- The **rain-on-snow events** rise, the **freezing level** goes up, the more rain and less snow fall in the high basins, and **soil moisture** and vegetation change; thus both the **frequency and the magnitude** of the flash floods increase, and the old flood frequency estimates (the stationarity) under-estimate the design flood, so that the design should include a climate factor and the early warning.

**(b) Flood of 500-year return period (Gumbel's extreme value distribution).** For a return period $T$:

$$\begin{gathered}Q_T = \bar Q + K_T\,\sigma \\ K_T = -\frac{\sqrt6}{\pi}\left\{0.5772 + \ln\ln\frac{T}{T-1}\right\}\end{gathered}$$

$$ K_{50} = -0.7797\{0.5772 + \ln\ln(1.0204)\} = 2.5923,\quad K_{100} = 3.1367,\quad K_{500} = 4.3947 $$

The two data points give $\bar Q$ and $\sigma$:

$$ \sigma = \frac{47380 - 35820}{3.1367 - 2.5923} = \frac{11560}{0.5444} = 21\,235\ \text{m}^3/\text{s} $$

$$ \bar Q = 35820 - 2.5923(21235) = -19\,226\ \text{m}^3/\text{s} $$

(a negative $\bar Q$ is only the intercept of the two-point fit and has no physical meaning).

$$ Q_{500} = -19\,226 + 4.3947(21\,235) = 74\,093 $$

$$ \boxed{Q_{500} \approx 7.4\times 10^{4}\ \text{m}^3/\text{s}} $$

*Check.* The Gumbel reduced variate is almost linear in $\ln T$ for large $T$, so a straight line of $Q$ against $\ln T$ has the slope $11560/\ln 2 = 16\,678$ m³/s per unit of $\ln T$, and

$$ Q_{500} = 47380 + 16678\ln 5 = 74\,222\ \text{m}^3/\text{s} $$

which is within 0.2 % of the Gumbel value.

@s 8
**Muskingum routing.** The storage equation $S = K[xI + (1-x)O]$ leads to

$$ O_2 = C_0I_2 + C_1I_1 + C_2O_1 $$

$$ \begin{gathered} C_0 = \frac{-Kx + 0.5\Delta t}{K(1-x) + 0.5\Delta t} \\[4pt] C_1 = \frac{Kx + 0.5\Delta t}{K(1-x) + 0.5\Delta t} \\[4pt] C_2 = \frac{K(1-x) - 0.5\Delta t}{K(1-x) + 0.5\Delta t} \end{gathered} $$

With $K = 10$ h, $x = 0.3$ and $\Delta t = 6$ h (the inflow interval): $Kx = 3$, $K(1-x) = 7$, $0.5\Delta t = 3$, so the denominator is $10$:

$$\begin{gathered}C_0 = \frac{-3+3}{10} = 0 \\ C_1 = \frac{3+3}{10} = 0.6 \\ C_2 = \frac{7-3}{10} = 0.4\end{gathered}$$

Check: $C_0 + C_1 + C_2 = 1$ ✓; stability $2Kx = 6 \le \Delta t = 6 \le 2K(1-x) = 14$ ✓.

Since $C_0 = 0$, the routing is simply $O_2 = 0.6\,I_1 + 0.4\,O_1$. Starting from $O_0 = 8$ m³/s:

| $t$ (h) | Inflow $I$ | $0.6\,I_{\text{prev}}$ | $0.4\,O_{\text{prev}}$ | Outflow $O$ (m³/s) |
|---|---|---|---|---|
| 0 | 14 | – | – | 8.00 |
| 6 | 24 | 8.40 | 3.20 | 11.60 |
| 12 | 54 | 14.40 | 4.64 | 19.04 |
| 18 | 64 | 32.40 | 7.62 | 40.02 |
| 24 | 59 | 38.40 | 16.01 | 54.41 |
| 30 | 49 | 35.40 | 21.76 | **57.16** |
| 36 | 39 | 29.40 | 22.86 | 52.27 |
| 42 | 32 | 23.40 | 20.91 | 44.31 |
| 48 | 24 | 19.20 | 17.72 | 36.92 |
| 54 | 19 | 14.40 | 14.77 | 29.17 |

$$ \boxed{\text{Peak outflow} \approx 57.2\ \text{m}^3/\text{s at } t = 30\ \text{h}} $$

The peak inflow of 64 m³/s at 18 h is **attenuated by about 11 %** and **delayed by about 12 h** (the lag is nearly $K$ = 10 h).

```figure caption="Question 8: Muskingum routing, K = 10 h, x = 0.3, Δt = 6 h: the outflow peak (57.2 m³/s at 30 h) is attenuated and delayed compared with the inflow peak (64 m³/s at 18 h)."
t=np.arange(0,55,6); I=np.array([14,24,54,64,59,49,39,32,24,19]); O=[8]
for i in range(9): O.append(0.6*I[i]+0.4*O[-1])
fig,ax=plt.subplots(figsize=(5.4,2.7))
ax.plot(t,I,color=INK,lw=1.6,marker="o",ms=3.5,label="inflow I"); ax.plot(t,O,color=ACCENT,lw=1.8,marker="s",ms=3.5,label="outflow O")
ax.annotate("64 at 18 h",xy=(18,64),xytext=(4,68),fontsize=7.5,arrowprops=dict(arrowstyle="->",color=INK,lw=0.7))
ax.annotate("57.2 at 30 h",xy=(30,57.16),xytext=(36,64),fontsize=7.5,arrowprops=dict(arrowstyle="->",color=ACCENT,lw=0.7))
ax.set_xlabel("time (h)",fontsize=8); ax.set_ylabel("discharge (m³/s)",fontsize=8); ax.set_ylim(0,75); ax.legend(fontsize=7.5); ax.grid(True,color=GRID,lw=0.5); ax.tick_params(labelsize=7)
fig.tight_layout()
```

---
file: NEBians-IOE-Past-Paper-Engineering-Survey-II-ENCE203-2081-Chaitra.pdf
subject: Engineering Survey II
level: BE · Year II / Part I
code: ENCE 203
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Why traverse balance is necessary? List the traverse balancing method and explain any one. You are computing the traverse independent coordinates; the given relative precision is 1:5000; you achieved the precision while calculation is 1:4200. Explain your action about it. [[1+1+2]]

@q 2
For the traverse surveying following data are given below; compute the independent coordinates with required action and calculate the area by DMD method. [[6+2]]

| Station | Line | Length (m) | Consecutive coordinates L | Consecutive coordinates D | Remarks |
|---|---|---|---|---|---|
| A | | | | | C (1500 mN, 1500 mE) |
| B | AB | 71.40 | -35.58 | 59.43 | |
| C | BC | 42.00 | 29.78 | 29.68 | |
| D | CD | 70.00 | 45.58 | -49.53 | |
| A | DA | 56.10 | -39.69 | -39.65 | |

@q 3
Draw the neat sketch of trigonometric levelling with the condition; base inaccessible and same vertical plane; instrument axes are at very large difference. Explain the procedures of contour plotting with considering the surveying principles. What are the uses of contour map? [[2+2+2]]

@q 4
What is field astronomy? What are its uses in civil engineering? The coordinates of three unknown station A, B and C are given below. The point P is instrument station and observations are taken to these known coordinate points which is given below. Calculate the coordinate of station P. [[2+4]]

| Station | Horizontal angle | Easting (m) | Northing (m) |
|---|---|---|---|
| A | ∠APB = 41°20'20" | 7464.718 | 6928.474 |
| B | ∠BPC = 97°56'40" | 9602.054 | 5363.275 |
| C | ∠CPA = 220°42'50" | 7611.753 | 1479.468 |

@q 5
For the small degree of curvature; curve length and chord length is approximately equal justify it. Derive the ideal equation of transition curve. [[1+3]]

@q 6
In a highway alignment the deflection angle is 52°. The geometry is such that the long chord is 26.303 m. The chainage of IP is 2+345.00 km. The peg interval is 5 m. Prepare the setting out table. Use three digits round off to calculate. [[6]]

@q 7
A grade of 1.25% meets another grade of 3.75%. The elevation and chainage of intersection point are 1056 m and (1+690) km. Field condition requires that the vertical curve should pass through a point of elevation of 1056.7 m at chainage (1+690) km. Compute a suitable equal tangent vertical curve and full station elevation. Peg interval is 30 m. Use parabolic equation. [[6]]

@q 8
Why vertical scale on photogrammetry is important? How you can estimate the value? Describe the features of drone. Explain the uses of drone in civil engineering. [[2+4]]

@q 9
What is GPS? Explain about the component of GPS. Do you think DGPS is better for the mapping and surveying than normal GPS? How you can apply the remote sensing in the field of civil engineering? [[4+1]]

@q 10
What is hydrographic survey? Describe the methods of measurement of velocity of flow. [[5]]

@q 11
How is the linear method of building setting out carried out? Why gyroscope is used to locate the tunnel instead of theodolite and compass? [[3+1]]

<!-- SOLUTIONS -->

@s 1
**Why a traverse is balanced.** Every angle and every length carries small accidental errors, so a closed (or link) traverse does not close exactly: $\Sigma L\neq0$ and $\Sigma D\neq0$. The balancing (adjustment) distributes this closing error over the whole traverse so that the plotted traverse closes, the coordinates are consistent, and the errors do not accumulate in the later work and the areas.

**Methods of balancing.**

1. **Bowditch (compass) rule**, 2. **transit rule**, 3. **Crandall's method** (least squares in the lengths, angles being held), 4. **graphical method** (Bowditch by proportional division of the closing line on the plot) and 5. the **axis (least-squares) method**.

**Bowditch rule (explained).** The angular errors are adjusted first. The corrections in latitude and departure of a line are proportional to the *length of the line* (taking the errors in the angles and the lengths to be equally important):

$$\begin{gathered}c_L=-\Sigma L\,\frac{l}{\Sigma l} \\ c_D=-\Sigma D\,\frac{l}{\Sigma l}\end{gathered}$$

where $\Sigma l$ is the perimeter. The corrected latitudes and departures are $L+c_L$ and $D+c_D$; after correction $\sum L=\sum D=0$. The relative precision is $\dfrac{e}{\Sigma l}$, with $e=\sqrt{(\Sigma L)^2+(\Sigma D)^2}$.

**Precision achieved 1:4200 against the required 1:5000.** The achieved precision $1/4200$ is **poorer** than the required $1/5000$ (the error is $1/4200>1/5000$), so the **traverse should not be balanced yet**. Action:

1. recheck the computations (angles, bearings, the arithmetic of latitudes and departures);
2. look for a blunder: the line whose bearing is nearly parallel to the direction of the closing error ($\tan\theta=\Sigma D/\Sigma L$), or the station on the perpendicular bisector of the closing line, is the likely culprit;
3. re-measure in the field the suspected lines or angles and the lengths (for the doubtful lines), and recompute;
4. balance with the Bowditch rule only after the specified precision of 1:5000 is attained; if it cannot be reached, repeat the traverse.

@s 2
**Closing error.**

$$\begin{gathered}\Sigma L=-35.58+29.78+45.58-39.69=+0.09\ \text{m} \\ \Sigma D=59.43+29.68-49.53-39.65=-0.07\ \text{m}\end{gathered}$$

$$\begin{gathered}e=\sqrt{0.09^2+0.07^2}=0.114\ \text{m} \\ \Sigma l=71.40+42.00+70.00+56.10=239.50\ \text{m} \\ \text{precision}=\frac{1}{239.5/0.114}=\frac1{2100}\end{gathered}$$

The direction of the error is $N\,37^\circ52'W$ (whole circle bearing $322^\circ08'$).

**Required action.** The precision $1/2100$ is much lower than the usual specification (1/3000 to 1/5000), so the first action in the field is the checking and re-measurement described in Question 1 (starting with line AB, whose printed length 71.40 m does not agree with the 69.27 m given by its own latitude and departure). The data given here cannot be re-measured, so the traverse is **balanced by the Bowditch rule** (the lengths and the angles are taken to be of the same quality, with the angles already adjusted).

$$\begin{gathered}c_L=-\frac{0.09}{239.5}l=-0.000376\,l \\ c_D=+\frac{0.07}{239.5}l=+0.000292\,l\end{gathered}$$

| Line | $l$ (m) | $L$ | $c_L$ | adjusted $L$ | $D$ | $c_D$ | adjusted $D$ |
|---|---|---|---|---|---|---|---|
| AB | 71.40 | -35.58 | -0.0268 | -35.607 | 59.43 | +0.0209 | 59.451 |
| BC | 42.00 | 29.78 | -0.0158 | 29.764 | 29.68 | +0.0123 | 29.692 |
| CD | 70.00 | 45.58 | -0.0263 | 45.554 | -49.53 | +0.0205 | -49.510 |
| DA | 56.10 | -39.69 | -0.0211 | -39.711 | -39.65 | +0.0164 | -39.634 |
| **Sum** | **239.50** | **0.09** | **-0.0900** | **0.000** | **-0.07** | **+0.0700** | **0.000** |

**Independent coordinates.** Station C is known (1500 mN, 1500 mE). Going round C → D → A → B → C:

| Station | Northing (m) | Easting (m) |
|---|---|---|
| C | 1500.000 | 1500.000 |
| D | 1545.554 | 1450.490 |
| A | 1505.843 | 1410.857 |
| B | 1470.236 | 1470.308 |
| C (check) | 1500.000 | 1500.000 |

**Area by the DMD method.** A is the westernmost station (smallest easting 1410.857 m), so the meridian through A is used and every DMD is positive. DMD of the first line $=$ its departure; DMD(next) $=$ DMD(previous) + $D$(previous) + $D$(this line). The last DMD must be equal to its departure with the sign changed, $39.634$.

| Line | adjusted $D$ | DMD (m) | adjusted $L$ | DMD $\times L$ ($\text{m}^2$) |
|---|---|---|---|---|
| AB | 59.451 | 59.451 | -35.607 | -2 116.86 |
| BC | 29.692 | 148.594 | 29.764 | +4 422.78 |
| CD | -49.510 | 128.777 | 45.554 | +5 866.26 |
| DA | -39.634 | 39.634 | -39.711 | -1 573.89 |
| | | | **Sum** | **6 598.29** |

$$\text{Area}=\tfrac12(6\,598.29)=\mathbf{3299\ m^2}\ (0.330\ \text{ha})$$

(check by the coordinate formula on the adjusted coordinates: $3299.15\ \text{m}^2$).

```figure caption="Question 2: the balanced traverse A-B-C-D with C at 1500 mN, 1500 mE. Area 3299 square metres."
fig,ax=plt.subplots(figsize=(4.6,3.2))
E=[1410.857,1470.308,1500,1450.490,1410.857]; N=[1505.843,1470.236,1500,1545.554,1505.843]
ax.fill(E,N,color=ACCENT,alpha=0.15); ax.plot(E,N,"-o",color=ACCENT,ms=4,lw=1.6)
for n,x,y in zip("ABCD",E,N): ax.text(x+1.5,y+1.5,n,fontsize=9)
ax.text(1450,1495,"3299 m2",fontsize=8,ha="center")
ax.set_xlabel("Easting (m)",fontsize=8); ax.set_ylabel("Northing (m)",fontsize=8); ax.set_aspect("equal"); ax.grid(color=GRID,lw=0.5)
```

@s 3
**Trigonometric levelling, base inaccessible, instrument stations and the object in the same vertical plane, instrument axes at different levels.** The foot of the object (a tower, a chimney or a hill top) $T$ cannot be reached, so the horizontal distance cannot be measured. Two instrument stations $A$ and $B$ are set up **in the same vertical plane as the object**, in a straight line with it, at a known horizontal distance $b$ apart, and the instrument axes are at different levels (a difference $\Delta$ found by a staff on a bench mark from both stations, the **axes of the instrument being at a very different level**).

**Conditions:** $A$, $B$ and the object are in one vertical plane (the line $ABT$ is straight); the angles of elevation $\alpha_A$ and $\alpha_B$ are measured at both stations, with face left and face right, using the same object point; the horizontal distance $AB=b$ is carefully measured; and the staff readings on a benchmark give the heights of the axes $HI_A$ and $HI_B$.

Let $d$ be the horizontal distance from the nearer station $A$ to the object ($d+b$ from $B$), and let $\Delta=HI_B-HI_A$.

$$d\tan\alpha_A=\Delta+(d+b)\tan\alpha_B\ \Rightarrow\ d=\frac{\Delta+b\tan\alpha_B}{\tan\alpha_A-\tan\alpha_B}$$

$$\text{RL of the top}=HI_A+d\tan\alpha_A=HI_B+(d+b)\tan\alpha_B$$

($\Delta$ is positive when the instrument at the farther station $B$ is higher; the sign follows the case; if the angles are depression angles, the tangents are subtracted.) The height of the object above its base is found by subtracting the RL of the base.

```figure caption="Question 3: trigonometric levelling, base inaccessible, A and B in the vertical plane of the object T, instrument axes at different levels (HI_B above HI_A)."
fig,ax=plt.subplots(figsize=(5.8,2.8)); ax.axis("off")
ax.plot([-1,4],[0,0],color="#8a6d3b",lw=2); ax.plot([4,11],[0.9,0.9],color="#8a6d3b",lw=2); ax.plot([4,4],[0,0.9],color="#8a6d3b",lw=2)
ax.plot([9.5,9.5],[0.9,4.3],color=INK,lw=3); ax.plot(9.5,4.3,"o",color="#d9534f"); ax.text(9.7,4.3,"T",fontsize=9)
A_=(0.3,0.5); B_=(5.0,1.4)
for P_,n in ((A_,"A"),(B_,"B")): ax.plot(*P_,"s",color=ACCENT,ms=5); ax.text(P_[0]-0.1,P_[1]-0.5,n,fontsize=9); ax.plot([P_[0],9.5],[P_[1],4.3],color=ACCENT,lw=1); ax.plot([P_[0],9.5],[P_[1],P_[1]],color=MUTED,lw=0.8,ls=":")
ax.annotate("",xy=(5.0,-0.6),xytext=(0.3,-0.6),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(2.6,-1.0,"b",fontsize=9,ha="center")
ax.annotate("",xy=(9.5,-0.6),xytext=(5.0,-0.6),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(7.2,-1.0,"d (from B to T)",fontsize=7.5,ha="center")
ax.text(1.5,0.8,"alpha A",fontsize=7.5,color=ACCENT); ax.text(6.0,1.7,"alpha B",fontsize=7.5,color=ACCENT); ax.text(-0.9,0.85,"HI_A",fontsize=7.5); ax.text(5.3,1.9,"HI_B",fontsize=7.5)
ax.set_xlim(-1.2,11.2); ax.set_ylim(-1.4,4.8)
```

**Procedure of contour plotting (with the surveying principles).**

1. **Whole to part:** first a framework of **horizontal control** (a traverse or triangulation, with coordinates) and **vertical control** (a level line with benchmarks at intervals) is made for the whole area with high accuracy. The details come next within this framework with a lower order of accuracy, so that the errors do not accumulate.
2. Plot the control stations on the sheet by the coordinates and the scale (central alignment on the grid).
3. Locate the **ground points** by the direct (the grid or the cross-section and the spot levels) or the indirect method (radial lines with the tacheometer, or the total station), including the *characteristic points* (ridge, valley, saddle, the break in the slope), and the RL of each. A *second* check on each is taken from a different station (**location by two independent measurements**).
4. **Interpolate** the contour points between the spot levels (by estimation, arithmetical calculation, or the graphical method with the tracing paper) for the chosen contour interval.
5. Join the points of equal RL with smooth curves, with the **index contour** (every fifth) bolder and numbered, check against the field, and give the title, the scale, the north line, the datum and the contour interval.

**Uses of a contour map.** Determination of the RL of any point and the **slope** between two points; the selection of the **site and the route** (the road, the canal, the pipeline) with the limited gradient; drawing the **sections** (the profiles); the **volume of earthwork**, the reservoir **capacity** and the dam site; the **catchment area** and the drainage lines; the inter-visibility of the stations; the design of drainage and layout of the building plots; the landslide and flood zoning.

@s 4
**Field astronomy.** Field (geodetic) astronomy is the determination of the **latitude, longitude and azimuth of a point on the earth**, and of the **time**, from the observations of the sun and the stars, by the use of a theodolite (or the astrolabe) and a chronometer, and the astronomical triangle (the pole, the zenith and the star) is solved. It uses the **celestial sphere** with the coordinates (declination, right ascension, hour angle, altitude and azimuth).

**Uses in civil engineering.**

- **The true meridian** (the azimuth of a line) from the sun or Polaris to orient a survey, to fix the **declination of the magnetic needle**, and to check the traverse or the triangulation (the Laplace azimuth) for the large projects;
- the **latitude and longitude** of points in remote areas where there is no control, the fixing of the **starting point of the control networks**, the national boundary and the datum;
- the alignment and orientation of **long tunnels, bridges, canals and transmission lines**, the **orientation of the buildings** (the sun path), the setting of the sun-compass;
- the **time and the length** of the day for the design of solar installations; and the independent check against the GNSS results.

**Position of P by Tienstra's formula (three-point resection).**

The observed angles add to $41^\circ20'20''+97^\circ56'40''+220^\circ42'50''=359^\circ59'50''$ (10" short, negligible). With $A=(7464.718,6928.474)$, $B=(9602.054,5363.275)$, $C=(7611.753,1479.468)$ ($E,N$):

$AB=2649.16$ m, $BC=4364.09$ m, $CA=5450.99$ m; the angles of the triangle are $\hat A=52^\circ14'19''$ ($\cot=0.77460$), $\hat B=99^\circ04'57''$ ($\cot=-0.15986$), $\hat C=28^\circ40'45''$ ($\cot=1.82812$).

$\alpha=\angle BPC=97^\circ56'40''$ ($\cot=-0.13955$), $\beta=\angle CPA=220^\circ42'50''$ ($\cot=1.16204$), $\gamma=\angle APB=41^\circ20'20''$ ($\cot=1.13672$).

$$K_A=\frac1{\cot\hat A-\cot\alpha}=\frac1{0.77460+0.13955}=1.09391$$

$$\begin{gathered}K_B=\frac1{\cot\hat B-\cot\beta}=\frac1{-0.15986-1.16204}=-0.75649 \\ K_C=\frac1{\cot\hat C-\cot\gamma}=\frac1{1.82812-1.13672}=1.44633\end{gathered}$$

$$\textstyle\sum K=1.78375$$

$$E_P=\frac{1.09391(7464.718)-0.75649(9602.054)+1.44633(7611.753)}{1.78375}=\mathbf{6677.50\ m}$$

$$N_P=\frac{1.09391(6928.474)-0.75649(5363.275)+1.44633(1479.468)}{1.78375}=\mathbf{3174.01\ m}$$

**Check.** The angles recomputed at $P$ are $\angle APB=41^\circ20'25''$, $\angle BPC=97^\circ56'54''$, $\angle CPA=220^\circ42'41''$, which agree with the observed ones to within 15", and the distances are $PA=3836.1$ m, $PB=3653.2$ m, $PC=1935.0$ m.

**Answer:** $P=(E,N)=(6677.50\ \text{m},\ 3174.01\ \text{m})$.

```figure caption="Question 4: three-point resection. P lies outside triangle ABC on the side of the reflex angle CPA."
fig,ax=plt.subplots(figsize=(4.4,4.0)); ax.set_aspect("equal")
A_=(7464.718,6928.474); B_=(9602.054,5363.275); C_=(7611.753,1479.468); P_=(6677.50,3174.01)
ax.fill([A_[0],B_[0],C_[0]],[A_[1],B_[1],C_[1]],color=ACCENT,alpha=0.10); ax.plot([A_[0],B_[0],C_[0],A_[0]],[A_[1],B_[1],C_[1],A_[1]],color=ACCENT,lw=1.2)
for Q,n in ((A_,"A"),(B_,"B"),(C_,"C")):
    ax.plot([P_[0],Q[0]],[P_[1],Q[1]],color=MUTED,lw=0.8,ls="--"); ax.plot(*Q,"o",color=INK,ms=4); ax.text(Q[0]+80,Q[1]+80,n,fontsize=9)
ax.plot(*P_,"o",color="#d9534f"); ax.text(P_[0]-380,P_[1]-80,"P",fontsize=9,color="#d9534f")
ax.set_xlabel("Easting (m)",fontsize=8); ax.set_ylabel("Northing (m)",fontsize=8); ax.grid(color=GRID,lw=0.5)
```

@s 5
**Arc and chord for a small degree of curve.** For a curve of radius $R$ the arc $l=R\theta$ and the chord $c=2R\sin(\theta/2)$ with $\theta=l/R$:

$$\begin{gathered}c=2R\Big[\frac\theta2-\frac1{6}\Big(\frac\theta2\Big)^3+\cdots\Big]=l-\frac{l^3}{24R^2}+\cdots \\ \frac{l-c}{l}\approx\frac{l^2}{24R^2}=\frac{\theta^2}{24}\end{gathered}$$

For a *small degree of curvature* (large $R$, i.e. $l\ll R$) the ratio $l/R$ is very small, so the relative difference is negligible: for $l=30$ m and $R=300$ m, $\theta=0.1$ rad, $(l-c)/l=0.1^2/24=1/2400=0.04\ \%$; with $l\le R/20$ it is $\le1/9600$. Hence the chord may be taken as the arc (which is the basis of the degree of curve and the deflection-angle method).

**Equation of the ideal transition curve.** The ideal curve provides a **uniform rate of increase of the centrifugal acceleration** at the constant speed $v$. At a distance $l$ from the start (radius $r$) the acceleration is $v^2/r$; it must reach $v^2/R$ at the end of the transition of length $L$, and so grows uniformly with $l$ (time $t=l/v$):

$$\frac{v^2}{r}=\frac{v^2}{R}\cdot\frac{l}{L}\ \Rightarrow\ \boxed{rl=RL}$$

(the radius is inversely proportional to the length of the curve measured from the start: the *clothoid*). The tangent angle: $d\phi=dl/r=\dfrac{l}{RL}dl\Rightarrow\phi=\dfrac{l^2}{2RL}$, and at the end $\phi_s=\dfrac{L}{2R}$. With $dx=\cos\phi\,dl$ and $dy=\sin\phi\,dl$ and a small $\phi$:

$$\begin{gathered}x=l-\frac{l^5}{40R^2L^2} \\ y=\frac{l^3}{6RL}-\cdots\approx\frac{l^3}{6RL}\end{gathered}$$

(the cubic spiral), with the shift $s=\dfrac{L^2}{24R}$.

@s 6
**Radius from the long chord.** $LC=2R\sin\dfrac\Delta2$:

$$R=\frac{26.303}{2\sin26^\circ}=\frac{26.303}{2(0.438371)}=30.00\ \text{m}$$

**Curve elements** ($\Delta=52^\circ$, IP at $2+345.00=2345.00$ m):

$$\begin{gathered}T=R\tan\frac\Delta2=30\tan26^\circ=14.632\ \text{m} \\ L=R\Delta\frac\pi{180}=30(0.907571)=27.227\ \text{m}\end{gathered}$$

$$\begin{gathered}\text{Ch(PC)}=2345.000-14.632=2330.368\ \text{m} \\ \text{Ch(PT)}=2330.368+27.227=2357.595\ \text{m}\end{gathered}$$

**Pegs every 5 m:** 2335, 2340, 2345, 2350, 2355 and the PT 2357.595. Sub-chords: first $=2335-2330.368=4.632$ m, full $=5$ m, last $=2357.595-2355=2.595$ m. The deflection angle (arc taken as the chord, Rankine) is $\delta=\dfrac{c}{2R}$ rad:

- first: $\dfrac{4.632}{60}=0.07720$ rad $=4^\circ25'23.6''$
- full: $\dfrac5{60}=0.083333$ rad $=4^\circ46'28.7''$
- last: $\dfrac{2.595}{60}=0.04325$ rad $=2^\circ28'41.5''$

**Setting out table (theodolite at PC, zero on the IP).**

| Peg | Chainage (m) | Chord $c$ (m) | Deflection for the chord | Total deflection | Chord $2R\sin\delta$ (m) |
|---|---|---|---|---|---|
| PC | 2330.368 | 0 | 0 | 0°00'00.0" | 0 |
| 1 | 2335.000 | 4.632 | 4°25'23.6" | 4°25'23.6" | 4.627 |
| 2 | 2340.000 | 5.000 | 4°46'28.7" | 9°11'52.3" | 4.994 |
| 3 | 2345.000 | 5.000 | 4°46'28.7" | 13°58'21.0" | 4.994 |
| 4 | 2350.000 | 5.000 | 4°46'28.7" | 18°44'49.8" | 4.994 |
| 5 | 2355.000 | 5.000 | 4°46'28.7" | 23°31'18.5" | 4.994 |
| PT | 2357.595 | 2.595 | 2°28'41.5" | 26°00'00.0" | 2.594 |

**Check:** total deflection at the PT $=\Delta/2=26^\circ00'00''$; the long chord $2R\sin26^\circ=26.302$ m, equal to the given 26.303 m.

@s 7
**Length of the curve.** $g_1=+1.25\%$, $g_2=+3.75\%$, $A=2.50\%$ (a sag curve, because the grade increases). IP: chainage $1+690=1690$ m, RL 1056.00 m. The curve passes through RL 1056.70 m at chainage 1690 m (the IP chainage), so the offset at the IP is

$$e=1056.70-1056.00=0.70\ \text{m}=\frac{AL}{800}\ \Rightarrow\ L=\frac{800\times0.70}{2.50}=\mathbf{224\ m}$$

$$\text{Ch(PVC)}=1690-112=1578\ \text{m},\quad \text{RL(PVC)}=1056-0.0125\times112=1054.600\ \text{m}$$

$$\text{Ch(PVT)}=1690+112=1802\ \text{m},\quad \text{RL(PVT)}=1056+0.0375\times112=1060.200\ \text{m}$$

**Parabolic equation.** $y=y_{PVC}+g_1x+\dfrac{g_2-g_1}{2L}x^2=1054.600+0.0125x+0.0000558\,x^2$ ($x$ from the PVC; $\dfrac{0.025}{2\times224}=5.5804\times10^{-5}$). Both grades are rising, so there is **no low point** on the curve: the gradient $0.0125+1.1161\times10^{-4}x$ is positive for all $x\ge0$ and the lowest point is the PVC.

**Elevations at the full stations (30 m pegs, multiples of 30 m).**

| Chainage (m) | $x$ (m) | Tangent RL $=1054.6+0.0125x$ | Offset $5.5804\times10^{-5}x^2$ | Curve RL (m) |
|---|---|---|---|---|
| 1578 (PVC) | 0 | 1054.600 | 0.000 | 1054.600 |
| 1590 | 12 | 1054.750 | 0.008 | 1054.758 |
| 1620 | 42 | 1055.125 | 0.098 | 1055.223 |
| 1650 | 72 | 1055.500 | 0.289 | 1055.789 |
| 1680 | 102 | 1055.875 | 0.581 | 1056.456 |
| 1690 (IP) | 112 | 1056.000 | 0.700 | 1056.700 |
| 1710 | 132 | 1056.250 | 0.972 | 1057.222 |
| 1740 | 162 | 1056.625 | 1.465 | 1058.090 |
| 1770 | 192 | 1057.000 | 2.057 | 1059.057 |
| 1800 | 222 | 1057.375 | 2.750 | 1060.125 |
| 1802 (PVT) | 224 | 1057.400 | 2.800 | 1060.200 |

(At the PVT the offset is $4e=2.80$ m, which brings $1057.40$ to $1060.20$ m, the same as RL(PVT) from the second grade.) The full stations are 1590, 1620, ..., 1800 m (the 1680 level lies close to the IP, which is at 1690 m).

```figure caption="Question 7: sag vertical curve, L = 224 m, g1 = +1.25 %, g2 = +3.75 %, PVI at chainage 1690 (RL 1056.00), curve through RL 1056.70 at the PVI."
fig,ax=plt.subplots(figsize=(5.8,2.7))
x=np.linspace(0,224,100); y=1054.6+0.0125*x+0.025/448*x**2
ax.plot(1578+x,y,color=ACCENT,lw=2.2,label="vertical curve")
ax.plot([1466,1690,1914],[1056-0.0125*224,1056,1056+0.0375*224],color=MUTED,lw=1,ls="--",label="grade lines")
ax.plot([1578,1802],[1054.6,1060.2],"o",color="#d9534f",ms=4); ax.text(1578,1054.0,"PVC 1054.600",fontsize=6.5,ha="center"); ax.text(1802,1060.5,"PVT 1060.200",fontsize=6.5,ha="center")
ax.plot(1690,1056,"s",color=INK,ms=4); ax.text(1690,1055.2,"IP 1056.00",fontsize=6.5,ha="center"); ax.plot(1690,1056.7,"o",color="#d9534f",ms=4); ax.text(1700,1057.25,"curve 1056.70",fontsize=6.5)
ax.set_xlabel("Chainage (m)",fontsize=8); ax.set_ylabel("RL (m)",fontsize=8); ax.legend(fontsize=7,loc="upper left"); ax.grid(color=GRID,lw=0.5)
```

@s 8
**Scale in photogrammetry and why it matters.** The scale of a vertical aerial photograph (the ratio of the distance on the photo to the corresponding ground distance) fixes the relation between the photo and the ground and is needed for measuring the **distances, the areas and the heights** on the photograph, for **planning the flight** (the flying height and the number of photographs for the area to be covered) and for the **map compilation and the accuracy of the output**. Because a photograph is a central projection, the scale varies with the ground elevation: points higher than the datum have a larger scale. The **vertical scale** (the exaggeration in the stereo-model and the DEM, equal to the ratio of the vertical to the horizontal scale, and the relation between the parallax difference and the height $h=\dfrac{H\,\Delta p}{p_a+\Delta p}$) matters because the heights come out wrong if it is wrong; the height scale is the one that controls the contouring and the volume computation.

**Estimating the value.**

1. **From the focal length and the flying height:** $S=\dfrac{f}{H-h}$ ($H$ above datum, $h$ the average elevation of the terrain); e.g. $f=152$ mm, $H-h=3040$ m gives $S=1:20\,000$.
2. **From a known ground distance** between two points measured on the ground: $S=\dfrac{\text{photo distance }ab}{\text{ground distance }AB}$.
3. **From a map:** $S=\dfrac{ab}{AB_{map}}\times\text{map scale}$.
4. For the heights (**vertical exaggeration** in stereo viewing) from the stereo-pair parallax by the relation $h=\dfrac{H\Delta p}{p_a+\Delta p}$ with $p_a$ the average photo base, checked on points of known elevation.

**Features of a drone (UAV).** An unmanned aircraft, flown by a remote controller or by a pre-programmed route (GNSS, an IMU, and an autopilot), as a **multi-rotor** (small area, hovering, short flight time) or a **fixed wing** (a large area, long endurance); carries the camera (RGB, multispectral, thermal) or the LiDAR; low flying height (50 to 120 m), a ground resolution of a few cm, the flight time of 20 to 60 min, a real-time telemetry link, the **RTK/PPK** GNSS for the accuracy of centimetres, the automatic overlap (80 % forward, 60 % side), cheap, quick and safe, but limited by the weather, the battery, the regulation and the line of sight.

**Uses in civil engineering.** Topographic and corridor mapping, the DEM and contour production, the orthophoto, the volume of earthwork and the stockpiles, the monitoring of the progress of construction, the inspection of bridges, dams, towers and slopes, the landslide and flood mapping, the cadastral and the land-use survey, and the 3D modelling and the disaster assessment.

@s 9
**GPS (Global Positioning System).** GPS is a satellite-based navigation and positioning system, owned by the USA, that gives the **three-dimensional position, the velocity and the time** anywhere in the world, at any time, in any weather. A receiver measures the pseudo-ranges to at least four satellites (the signal travel time multiplied by the speed of light), and by **trilateration** it solves for $(x,y,z)$ and the receiver clock error $\delta t$:

$$\begin{gathered}\rho_i=\sqrt{(x_i-x)^2+(y_i-y)^2+(z_i-z)^2}+c\,\delta t \\ i=1\ldots4\end{gathered}$$

**Components.**

1. **Space segment:** at least 24 satellites in 6 orbital planes (55° inclination) at an altitude of 20 200 km with a period of about 12 h; they carry atomic clocks and transmit on L1 and L2 (and L5) with the navigation message (the ephemeris, the clock corrections).
2. **Control segment:** the master control station (Colorado Springs) with the monitor stations and the ground antennas that track the satellites, compute the orbits and the clock corrections, and upload them.
3. **User segment:** the receivers (handheld, geodetic or survey grade, in the phones and the vehicles) with the antenna and the processing unit.

**Is DGPS better than normal GPS?** Yes. In DGPS a base receiver at a point of known coordinates computes the errors in the ranges (the satellite clock, the orbit, the ionospheric and the tropospheric delay), which are common to both receivers at a short distance, and the corrections are sent to the rover, giving an accuracy of 1 to 3 m (code) or the **cm level** (carrier phase, RTK and PPK) against the 5 to 10 m of a single GPS; so DGPS is suitable for mapping, the control surveys, the cadastral and the layout work.

**Remote sensing in civil engineering** (1 mark): land-use and terrain mapping, the route and the site selection, the watershed and the flood mapping, the landslide and the geological studies, the monitoring of the reservoirs and the construction, and the damage assessment after the disasters.

@s 10
**Hydrographic survey.** Hydrographic surveying is the measurement and the mapping of the **underwater features**: the water depth (the bed topography), the **shoreline**, the water levels, the tides and the **currents (the velocity and the discharge)**, in rivers, lakes, reservoirs and harbours. It is used for the design of dams, weirs and bridges, the reservoir capacity and the sediment, the navigation channels and the dredging, and the scour at foundations.

**Methods of measuring the velocity of flow.**

1. **Floats.** *Surface floats* (a wood block, a bottle) timed over a measured run of 20 to 100 m between two cross-sections: $v_s=\dfrac{\text{length}}{\text{time}}$, the mean velocity $v\approx0.8$ to $0.85\,v_s$. *Sub-surface (double) floats* (a weighted float below a surface buoy) give the velocity at a depth; *rod (velocity) floats* — a weighted tube reaching to nearly the bed — give the mean velocity in the vertical, $v\approx0.9\ v_{rod}$ (a correction factor from the rod depth).
2. **Current meter (the most accurate).** A cup- or propeller-type meter whose rotation rate $N$ (rev/s) gives $v=aN+b$ (the calibration equation). Readings are taken at $0.6d$ (the mean), or at $0.2d$ and $0.8d$ ($v_m=\tfrac12(v_{0.2}+v_{0.8})$), or at $0.2d$, $0.6d$, $0.8d$, in each vertical of the cross-section, and the discharge is $Q=\sum v_i a_i$.
3. **Pitot tube**, in which the velocity head $h$ gives $v=C\sqrt{2gh}$ at a point.
4. **Dilution (chemical gauging) method:** a salt or a dye of a known concentration is injected at a known rate, and the dilution at a downstream section gives $Q$ (for the turbulent mountain streams, where the current meters are not usable).
5. **Acoustic Doppler (ADCP) and the electromagnetic methods:** the Doppler shift of the sound scattered from the particles gives the velocity profile and the discharge as the boat crosses the river.
6. **Slope-area method** (indirect): $v=\dfrac1nR^{2/3}S^{1/2}$ by Manning's equation using the surveyed section and the water-surface slope (used for floods).

@s 11
**Linear method of building setting out.** The building is laid out from a **baseline** (a boundary or road line, or a line parallel to it) with the tape (or EDM) alone.

1. Establish the baseline $AB$ and the reference point; measure along the baseline and offset at right angles (with the **3-4-5 tape triangle** or an optical square) to fix the first corner $P$ at the set-back required.
2. Lay out $PQ$ along the line (the building length) and $PS$ at right angles to it (the breadth) by the same 3-4-5 triangle, and fix $R$ by the intersection of two tape arcs: $QR=PS$ and $SR=PQ$.
3. **Check:** the opposite sides must be equal and the **two diagonals must be equal**, $PR=QS=\sqrt{PQ^2+PS^2}$ (to within about 1 in 2000); the corners are marked with pegs and transferred to the **batter boards** set about 1.5 to 2 m away from the excavation, where the nails and the strings give the centre lines and the trench widths.
4. The inner walls and the columns are fixed from these lines by the offsets, and the levels with the level and a temporary bench mark.

*Example:* a 10 m by 6 m building, 3 m from the road and 2 m from the side line. Measure 2 m from the boundary point along the road, set 3 m perpendicular by the 3-4-5 triangle to get $P$; $Q$ is 10 m along the line, $S$ is 6 m on the perpendicular, $R$ by the arcs of 6 m from $Q$ and 10 m from $S$; check $PR=QS=\sqrt{10^2+6^2}=11.66$ m.

**Why a gyroscope is used to locate (align) the tunnel instead of a theodolite and compass.** Underground there is **no line of sight to the surface or to the stars**, so a theodolite alone cannot give the direction, and a **compass is useless** because of the local magnetic disturbance by the steel, the rails, the machinery and the electric power, and the lower accuracy of $\pm0.5^\circ$. A **gyro-theodolite** seeks the **true meridian by itself** (by the earth's rotation), so that it gives the azimuth of a line directly, **independently of the surface** and of magnetism, with an accuracy of 10" to 20", and it controls the accumulation of the traverse direction error (the breakthrough accuracy) over the long tunnel and the shaft.

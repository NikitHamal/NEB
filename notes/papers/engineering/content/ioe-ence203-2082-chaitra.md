---
file: NEBians-IOE-Past-Paper-Engineering-Survey-II-ENCE203-2082-Chaitra.pdf
subject: Engineering Survey II
level: BE · Year II / Part I
code: ENCE 203
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Why is a traverse necessary in surveying? Explain the central alignment process of a traverse on a grid by manual plotting, using assumed values and a suitable scale of your choice. Why is the coordinate method considered so versatile for area computation, and how is the area calculated using this method? [[1+3+2]]

@q 2
A link traverse was run between two stations A and F. Calculate independent coordinates of stations B, C, D and E. Find the direction and magnitude of misclosure and adjust it. [[6]]

| Station | Line | Length (m) | Consecutive coordinates L | Consecutive coordinates D | Remarks |
|---|---|---|---|---|---|
| A | | | | | A: (1995.70 mN, 1650.15 mE) |
| B | AB | 207.15 | 122.72 | 166.88 | |
| C | BC | 192.40 | 140.81 | 131.13 | |
| D | CD | 324.16 | -265.97 | 185.31 | |
| E | DA | 310.10 | -277.26 | -135.84 | |
| F | EF | 215.82 | -53.66 | 209.04 | F: (1662.58 mN, 2206.57 mE) |

@q 3
Define contour and list the four major characteristics of contour. Find the elevation of the top of tower with following observations: The instrument axes and elevated objects are at same vertical plane. RL of Bench Mark is 1248.362 m. [[3+3]]

| Inst. Station | Staff reading on Bench Mark (m) | Angle of elevation | Remarks |
|---|---|---|---|
| A | 1.266 | 10°48' | Distance between Inst. Station = 50 m |
| B | 1.086 | 7°12' | |

@q 4
What are the Map projection system of Nepal? The coordinates of three unknown station A, B and C and horizontal angle to these known coordinate points from instrument station are given in the table below. Calculate the coordinate of station P. [[2+4]]

| Station | Horizontal angle | Easting (m) | Northing (m) |
|---|---|---|---|
| A | ∠APB = 38°45'15" | 5210.450 | 8120.660 |
| B | ∠BPC = 105°12'30" | 7340.110 | 6540.220 |
| C | ∠CPA = 216°02'10" | 5450.330 | 2310.880 |

@q 5
Based on which relationship can it be assumed that the chord length is approximately equal to the arc length of circular curve? Why transition curve is provided at the both end of circular curve? [[3+1]]

@q 6
For the 8° of curve and fixed arc length 25 m the highway alignment deflection angle is 56°. The chainage of IP is 3+500.00 km. The peg interval is 30 m. Prepare the setting out table. Also find the total deflection angle for middle of curve. Use nearest multiple of 5 for the radius value. [[6]]

@q 7
Derive the general equation of parabolic curve and establish the relationship between its parameters. A grade of (-) 2.75% meets another grade of 3.5%. The elevation and chainage of IP are 2470.00 m and 2800.00 m respectively. Field condition requires that the vertical curve should pass through a point of elevation 2471.25 m at a chainage of 2800.00 m. Compute a suitable equal tangent vertical curve including lowest chainage and full station elevation. Take peg interval = 30 m. [[2+4]]

@q 8
Explain about the relief displacement in photogrammetry. Describe the Drone regulation in Nepal and flight permission of drones. What are the uses of drone in Civil Engineering? [[2+4]]

@q 9
How DGPS is better for mapping and surveying than normal GPS? What is the application of remote sensing in Civil engineering? [[2+3]]

@q 10
What are the uses of hydrographic surveys in civil engineering? Explain the method of echo sounding. [[5]]

@q 11
Explain the linear method of building layouts with suitable examples. Why is the gyroscope used in the tunnel alignment? [[4]]

<!-- SOLUTIONS -->

@s 1
**Why a traverse is necessary.** A traverse is a chain of survey lines whose lengths and directions are measured. It is the cheapest and quickest way to create a *control framework* (a set of stations with known coordinates) over a long, narrow or obstructed area, where triangulation is impractical. All detail (buildings, roads, contours, boundaries) is then fixed from these control stations, so the principle *work from the whole to the part* is met and errors do not accumulate.

**Central alignment of a traverse on a grid (manual plotting).** The plan must lie in the middle of the drawing sheet with a margin on every side, so the plotting is done as follows.

1. Compute the coordinates $(N_i,E_i)$ of every station from an assumed origin (for example $A=(1000.00,1000.00)$) after the closing error has been adjusted.
2. Find the extreme values $N_{max},N_{min},E_{max},E_{min}$ and the extents $\Delta N=N_{max}-N_{min}$, $\Delta E=E_{max}-E_{min}$.
3. **Choose the scale** so that the larger extent, plus a margin (about 3 to 5 cm on each side), fits the usable sheet, and take the next standard scale (1:500, 1:1000, 1:2000 ...). For example, a traverse 480 m by 300 m on an A1 sheet (usable 55 cm by 75 cm) gives $480\,\text{m}/0.55\,\text{m}\approx873$, so the scale 1:1000 is chosen.
4. **Find the centre** of the traverse, $N_c=\tfrac12(N_{max}+N_{min})$, $E_c=\tfrac12(E_{max}+E_{min})$. This point is made to fall on the centre of the sheet.
5. Draw the grid, i.e. lines of constant $E$ (vertical) and constant $N$ (horizontal) at a round interval (for 1:1000, every 50 m = 5 cm). Number the grid lines so that the point $(N_c,E_c)$ falls at the centre of the sheet.
6. Plot each station from its coordinates by the offsets $x=(E_i-E_c)\times\text{scale}$ and $y=(N_i-N_c)\times\text{scale}$ measured from the sheet centre. Join the stations, check the plotted lengths and bearings against the field values, then plot the details.

```figure caption="Question 1: central alignment. The bounding box of the traverse is centred on the grid sheet; its centre (Nc, Ec) is placed at the centre of the sheet, leaving an equal margin on every side."
fig,ax=plt.subplots(figsize=(5.0,3.4)); ax.set_aspect("equal")
ax.add_patch(plt.Rectangle((0,0),10,7,fill=False,ec=INK,lw=1.4))
for g in range(1,10): ax.plot([g,g],[0,7],color=GRID,lw=0.7)
for g in range(1,7): ax.plot([0,10],[g,g],color=GRID,lw=0.7)
P=np.array([[2.4,2.1],[7.0,1.7],[7.7,4.6],[4.9,5.4],[2.9,4.4]])
ax.add_patch(plt.Rectangle((2.4,1.7),5.3,3.7,fill=False,ec="#d9534f",lw=1.0,ls="--"))
ax.fill(P[:,0],P[:,1],color=ACCENT,alpha=0.18); ax.plot(np.r_[P[:,0],P[0,0]],np.r_[P[:,1],P[0,1]],color=ACCENT,lw=1.6)
for n,p in zip("ABCDE",P): ax.text(p[0]-0.2,p[1]-0.3,n,fontsize=8,color=INK)
ax.plot(5.05,3.55,"o",color="#d9534f"); ax.text(5.2,3.75,"centre (Nc, Ec)",fontsize=7,color="#d9534f")
ax.annotate("",xy=(0,6.5),xytext=(2.4,6.5),arrowprops=dict(arrowstyle="<->",color=MUTED)); ax.text(1.2,6.65,"margin",ha="center",fontsize=7,color=MUTED)
ax.text(5,-0.55,"E (grid lines at equal interval)",ha="center",fontsize=7); ax.text(-0.35,3.5,"N",fontsize=7,va="center")
ax.set_xlim(-0.8,10.4); ax.set_ylim(-1,7.4); ax.axis("off")
```

**Why the coordinate method is so versatile for area.** The only data needed are the coordinates of the boundary stations, which a traverse, a total station or GNSS gives directly (and already adjusted). Hence:

- it applies to a polygon of **any shape and any number of sides**, convex or concave, with no division into triangles or trapezoids and no plotting;
- the result is **analytical**, with no scaling error from a map;
- the formula is simple to programme, so the area follows immediately in a spreadsheet, a total station or CAD;
- the same figures serve for plotting, setting out and the calculation of volume.

**Area by coordinates (Gauss' shoelace formula).** For stations $1,2,\dots,n$ taken in order round the boundary with $(N_i,E_i)$ and $N_{n+1}=N_1$, $E_{n+1}=E_1$,

$$A=\tfrac12\Big|\sum_{i=1}^{n}\big(E_iN_{i+1}-E_{i+1}N_i\big)\Big|=\tfrac12\Big|\sum_{i=1}^{n}N_i\big(E_{i-1}-E_{i+1}\big)\Big|$$

*Example.* $A(0,0)$, $B(80,20)$, $C(100,110)$, $D(10,90)$ in $(N,E)$ metres: $\sum N_i(E_{i-1}-E_{i+1})=0\cdot(90-20)+80(0-110)+100(20-90)+10(110-0)=-8800-7000+1100=-14\,700$, so $A=\tfrac12\times14\,700=7350\ \text{m}^2$.

@s 2
**Misclosure.** For a link traverse between two stations of known coordinates, the sum of the consecutive coordinates must equal the difference between the known coordinates of the end stations.

$$\Sigma L=122.72+140.81-265.97-277.26-53.66=-333.36\ \text{m}$$

$$\Sigma D=166.88+131.13+185.31-135.84+209.04=+556.52\ \text{m}$$

Required: $N_F-N_A=1662.58-1995.70=-333.12$ m and $E_F-E_A=2206.57-1650.15=+556.42$ m.

Error in latitude $e_L=-333.36-(-333.12)=-0.24$ m; error in departure $e_D=556.52-556.42=+0.10$ m.

**Magnitude and direction of the misclosure.**

$$\begin{gathered}e=\sqrt{0.24^2+0.10^2}=0.260\ \text{m} \\ \tan\theta=\frac{0.10}{0.24}\ \Rightarrow\ \theta=22^\circ37'\end{gathered}$$

The computed end point lies 0.26 m from the true $F$ towards the *south-east*, in the direction $S\,22^\circ37'E$ (whole circle bearing $157^\circ23'$). To close the traverse the correction is applied in the opposite sense. The perimeter is $\Sigma l=1249.63$ m, so the relative precision is $1/4800$ (acceptable for an ordinary traverse).

**Adjustment (Bowditch rule).** The correction to each line is proportional to its length:

$$\begin{gathered}c_L=-e_L\frac{l}{\Sigma l}=+0.24\frac{l}{1249.63} \\ c_D=-e_D\frac{l}{\Sigma l}=-0.10\frac{l}{1249.63}\end{gathered}$$

| Line | $l$ (m) | $L$ | $c_L$ | adjusted $L$ | $D$ | $c_D$ | adjusted $D$ |
|---|---|---|---|---|---|---|---|
| AB | 207.15 | 122.72 | +0.040 | 122.760 | 166.88 | -0.017 | 166.863 |
| BC | 192.40 | 140.81 | +0.037 | 140.847 | 131.13 | -0.015 | 131.115 |
| CD | 324.16 | -265.97 | +0.062 | -265.908 | 185.31 | -0.026 | 185.284 |
| DE | 310.10 | -277.26 | +0.060 | -277.200 | -135.84 | -0.025 | -135.865 |
| EF | 215.82 | -53.66 | +0.041 | -53.619 | 209.04 | -0.017 | 209.023 |
| **Sum** | **1249.63** | **-333.36** | **+0.240** | **-333.120** | **556.52** | **-0.100** | **556.420** |

Both sums now equal the required values (-333.12 and +556.42), so the traverse closes on F. (The paper prints the line D to E as "DA"; the order of the stations is A-B-C-D-E-F.)

**Independent (adjusted) coordinates.** $N_{i}=N_{i-1}+L_{adj}$ and $E_i=E_{i-1}+D_{adj}$.

| Station | Northing (m) | Easting (m) |
|---|---|---|
| A | 1995.700 | 1650.150 |
| B | 2118.460 | 1817.013 |
| C | 2259.307 | 1948.128 |
| D | 1993.399 | 2133.412 |
| E | 1716.199 | 1997.547 |
| F | 1662.580 | 2206.570 |

```figure caption="Question 2: unadjusted (dashed) and Bowditch-adjusted (solid) link traverse from A to F. The adjusted line ends exactly at F."
fig,ax=plt.subplots(figsize=(5.2,3.2))
adj=np.array([[1650.150,1995.700],[1817.013,2118.460],[1948.128,2259.307],[2133.412,1993.399],[1997.547,1716.199],[2206.570,1662.580]])
un=[[1650.15,1995.70]]
for l_,d_ in [(122.72,166.88),(140.81,131.13),(-265.97,185.31),(-277.26,-135.84),(-53.66,209.04)]: un.append([un[-1][0]+d_,un[-1][1]+l_])
un=np.array(un)
ax.plot(un[:,0],un[:,1],"--o",color="#d9534f",ms=3,lw=1.1,label="computed (misclosure 0.26 m)")
ax.plot(adj[:,0],adj[:,1],"-o",color=ACCENT,ms=4,lw=1.6,label="adjusted")
for n,p in zip("ABCDEF",adj): ax.text(p[0]+12,p[1]+8,n,fontsize=8)
ax.set_xlabel("Easting (m)",fontsize=8); ax.set_ylabel("Northing (m)",fontsize=8); ax.legend(fontsize=7,loc="upper left"); ax.set_aspect("equal"); ax.grid(color=GRID,lw=0.6)
```

@s 3
**Contour.** A contour is an imaginary line on the ground (and its trace on a map) joining points of **equal elevation** above a datum. The vertical distance between two consecutive contours is the contour interval.

**Four main characteristics.**

1. Contour lines of different elevations **do not cross or meet** each other, except at a vertical cliff (they merge) or an overhanging cliff or cave (they cross).
2. **Spacing shows the slope**: closely spaced contours mean a steep slope, widely spaced contours a gentle slope, and equally spaced straight contours a uniform slope.
3. A contour line is a **closed curve**; it may close beyond the limits of the map. A closed set of contours with the highest value inside is a hill, and with the lowest value inside is a depression.
4. Contours cross **ridge and valley lines at right angles**. Contour bends pointing *down* the slope show a ridge (spur); bends pointing *up* the slope show a valley.

**Height of the tower (base inaccessible, axes in the same vertical plane).** Let the tower base be at horizontal distance $d$ from the nearer station $A$ (so it is $d+50$ from $B$). The angles are $\alpha_A=10^\circ48'$ and $\alpha_B=7^\circ12'$.

Height of instrument (axis level):

$$\begin{gathered}HI_A=1248.362+1.266=1249.628\ \text{m} \\ HI_B=1248.362+1.086=1249.448\ \text{m}\end{gathered}$$

The RL of the top of the tower $T$ is the same from each station:

$$HI_A+d\tan\alpha_A=HI_B+(d+50)\tan\alpha_B$$

$$d=\frac{HI_B-HI_A+50\tan\alpha_B}{\tan\alpha_A-\tan\alpha_B}=\frac{-0.180+50(0.12633)}{0.19076-0.12633}=\frac{6.1365}{0.06443}\approx95.24\ \text{m}$$

$$\text{RL of top}=1249.628+95.24\times0.19076=1249.628+18.17=\mathbf{1267.80\ m}$$

Check from B: $1249.448+(95.24+50)\times0.12633=1249.448+18.35=1267.80$ m. The tower is 95.24 m from A and 145.24 m from B, and its top is $1267.80-1248.362=19.43$ m above the bench mark.

```figure caption="Question 3: instrument stations A and B in the vertical plane of the tower; the top T is fixed by the two angles of elevation (not to scale)."
fig,ax=plt.subplots(figsize=(5.8,2.6)); ax.axis("off")
ax.plot([-1,10.5],[0,0],color="#8a6d3b",lw=2)
A_=(0.5,0.35); B_=(2.5,0.35); T_=(8.5,2.8)
ax.plot([8.5,8.5],[0,2.8],color=INK,lw=3); ax.plot(8.5,2.8,"o",color="#d9534f"); ax.text(8.7,2.8,"T (top)",fontsize=8)
for P_,n in ((A_,"A"),(B_,"B")):
    ax.plot(*P_,"s",color=ACCENT,ms=5); ax.plot([P_[0],T_[0]],[P_[1],T_[1]],color=ACCENT,lw=1.0); ax.text(P_[0],P_[1]-0.4,n,fontsize=8,ha="center")
ax.plot([A_[0],T_[0]],[A_[1],A_[1]],color=MUTED,lw=0.8,ls=":"); ax.plot([B_[0],T_[0]],[B_[1],B_[1]],color=MUTED,lw=0.8,ls=":")
ax.annotate("",xy=(2.5,-0.5),xytext=(0.5,-0.5),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(1.5,-0.9,"50 m",ha="center",fontsize=8)
ax.annotate("",xy=(8.5,-0.5),xytext=(2.5,-0.5),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(5.5,-0.9,"145.24 m (from B)",ha="center",fontsize=8)
ax.text(1.3,0.6,"10°48'",fontsize=7,color=ACCENT); ax.text(3.4,0.55,"7°12'",fontsize=7,color=ACCENT)
ax.text(8.8,0.9,"RL top = 1267.80 m",fontsize=8,color="#d9534f"); ax.set_xlim(-1,11.5); ax.set_ylim(-1.3,3.3)
```

@s 4
**Map projection system of Nepal.** Nepal uses the **Modified Universal Transverse Mercator (MUTM)** projection on the Everest 1830 spheroid (Indian datum). The country is covered by three zones, each 3° wide, with central meridians at **81°E, 84°E and 87°E**. The scale factor on the central meridian is **0.9999** (UTM uses 0.9996), the false easting is 500 000 m and the false northing is 0 at the equator. (For GNSS work the Survey Department now also uses the standard UTM zones 44 and 45 on the WGS-84 datum.)

**Position of P by Tienstra's formula (three-point resection).** With the angles at $P$ subtended by the known points,

$$P=\frac{K_AA+K_BB+K_CC}{K_A+K_B+K_C},\quad K_A=\frac1{\cot\hat A-\cot\alpha},\ K_B=\frac1{\cot\hat B-\cot\beta},\ K_C=\frac1{\cot\hat C-\cot\gamma}$$

where $\hat A,\hat B,\hat C$ are the angles of triangle $ABC$, and $\alpha=\angle BPC$, $\beta=\angle CPA$, $\gamma=\angle APB$ are the observed angles at $P$ opposite to $A$, $B$, $C$. The observed angles add to $38^\circ45'15''+105^\circ12'30''+216^\circ02'10''=359^\circ59'55''$ (5" short, negligible).

**Triangle ABC** from the coordinates: $AB=2652.03$ m, $BC=4632.34$ m, $CA=5814.73$ m, and the angles (dot product of the side vectors)

$$\hat A=51^\circ03'22''\ (\cot=0.80816),\quad \hat B=102^\circ30'11''\ (\cot=-0.22175),\quad \hat C=26^\circ26'27''\ (\cot=2.01090)$$

with sum $180^\circ$.

**Weights.** $\cot\alpha=\cot105^\circ12'30''=-0.27185$, $\cot\beta=\cot216^\circ02'10''=+1.37456$, $\cot\gamma=\cot38^\circ45'15''=+1.24579$.

$$\begin{gathered}K_A=\frac1{0.80816+0.27185}=0.9259 \\ K_B=\frac1{-0.22175-1.37456}=-0.6264 \\ K_C=\frac1{2.01090-1.24579}=1.3070\end{gathered}$$

$$\textstyle\sum K=1.6065$$

The negative weight $K_B$ tells us that $P$ lies *outside* triangle $ABC$ (the reflex angle $216^\circ$ means $B$ is on the far side of $P$ from the side $CA$).

$$E_P=\frac{0.9259(5210.450)-0.6264(7340.110)+1.3070(5450.330)}{1.6065}=\mathbf{4575.15\ m}$$

$$N_P=\frac{0.9259(8120.660)-0.6264(6540.220)+1.3070(2310.880)}{1.6065}=\mathbf{4010.21\ m}$$

**Check.** Angles computed back at $P$: $\angle APB=38^\circ45'17''$, $\angle BPC=105^\circ12'37''$, $\angle CPA=216^\circ02'06''$, all within a few seconds of the observed values. Distances: $PA=4159.3$ m, $PB=3747.8$ m, $PC=1911.5$ m.

**Answer:** $P$ is at **Easting 4575.15 m, Northing 4010.21 m**.

```figure caption="Question 4: three-point resection. P lies outside triangle ABC, on the side of the reflex angle CPA = 216 deg."
fig,ax=plt.subplots(figsize=(4.6,3.9)); ax.set_aspect("equal")
A_=(5210.450,8120.660); B_=(7340.110,6540.220); C_=(5450.330,2310.880); P_=(4575.15,4010.21)
ax.fill([A_[0],B_[0],C_[0]],[A_[1],B_[1],C_[1]],color=ACCENT,alpha=0.10)
ax.plot([A_[0],B_[0],C_[0],A_[0]],[A_[1],B_[1],C_[1],A_[1]],color=ACCENT,lw=1.2)
for Q,n in ((A_,"A"),(B_,"B"),(C_,"C")):
    ax.plot([P_[0],Q[0]],[P_[1],Q[1]],color=MUTED,lw=0.8,ls="--"); ax.plot(*Q,"o",color=INK,ms=4); ax.text(Q[0]+90,Q[1]+90,n,fontsize=9)
ax.plot(*P_,"o",color="#d9534f"); ax.text(P_[0]-450,P_[1]-250,"P",fontsize=9,color="#d9534f")
ax.text(4750,6300,"38°45'15\"",fontsize=7); ax.text(5400,5000,"105°12'30\"",fontsize=7); ax.text(3350,3300,"216°02'10\" (through B)",fontsize=7)
ax.set_xlabel("Easting (m)",fontsize=8); ax.set_ylabel("Northing (m)",fontsize=8); ax.grid(color=GRID,lw=0.5)
```

@s 5
**Chord is approximately equal to the arc.** For a circular curve of radius $R$ subtending an angle $\theta$ at the centre, the arc and the chord are

$$\begin{gathered}l=R\theta \\ c=2R\sin\frac{\theta}{2}=R\theta-\frac{R\theta^3}{24}+\cdots\end{gathered}$$

so the difference is

$$l-c\approx\frac{l^3}{24R^2}$$

Since $\sin x\approx x$ for a small $x$, the chord is practically equal to the arc when the **length is small compared with the radius**. The usual rule: take the chord equal to the arc when $l\le R/20$ (the relative error is then $l^2/24R^2\le1/9600$, about 0.01 %). For a 20 or 30 m chord this holds for $R\ge400$ or $600$ m; for sharper curves shorter chords (10 m or 5 m) are used. This relation is the basis of the *degree of curve* by the arc definition, of the peg-interval chord in the deflection-angle method, and of the approximation $\delta=\dfrac{l}{2R}$ radians for the deflection angle.

**Why a transition curve is provided at both ends of the circular curve.**
A vehicle moving from a straight (radius infinite) into a circular curve (radius $R$) is suddenly subjected to the centrifugal force $mv^2/R$. The transition (spiral) curve, whose radius decreases gradually from $\infty$ to $R$, provides:

1. a **gradual build-up of the centrifugal acceleration** (rate $v^3/(RL_s)$), which gives comfort and safety and prevents skidding or overturning;
2. a length over which the **superelevation** is raised gradually from the crown to the full value, and over which the **extra widening** is introduced;
3. a **better appearance** of the alignment with no sudden kink.

@s 6
**Radius.** Degree of curve by the arc definition for an arc of 25 m: $D=\dfrac{25\times180}{\pi R}$, so

$$R=\frac{25\times180}{\pi\times 8}=\frac{572.96}{8}=179.05\ \text{m}\ \Rightarrow\ \text{nearest multiple of 5: } R=180\ \text{m}$$

**Curve elements** ($\Delta=56^\circ$, IP chainage $=3+500.00=3500.00$ m; the printed "km" is read as the usual station notation).

$$T=R\tan\frac{\Delta}{2}=180\tan28^\circ=180(0.53171)=95.708\ \text{m}$$

$$L=R\Delta\,\frac{\pi}{180}=180\times0.977384=175.929\ \text{m}$$

$$\begin{gathered}\text{Ch(PC)}=3500.000-95.708=3404.292\ \text{m} \\ \text{Ch(PT)}=3404.292+175.929=3580.221\ \text{m}\end{gathered}$$

**Chainages of the pegs** (peg interval 30 m, so the pegs fall on multiples of 30 m): 3420, 3450, 3480, 3510, 3540, 3570 m and the PT at 3580.221 m.

Sub-chords: first $=3420-3404.292=15.708$ m; full chords $=30$ m; last $=3580.221-3570=10.221$ m. Deflection angle $\delta=\dfrac{c}{2R}$ rad:

- first: $\dfrac{15.708}{360}$ rad $=2^\circ30'00''$
- full 30 m chord: $\dfrac{30}{360}$ rad $=4^\circ46'28.7''$
- last: $\dfrac{10.221}{360}$ rad $=1^\circ37'36.4''$

**Setting out table (theodolite at PC, zero set on the tangent towards the IP).**

| Peg | Chainage (m) | Chord $c$ (m) | Deflection for chord | Total deflection (reading) | Chord length by tape, $2R\sin\delta$ (m) |
|---|---|---|---|---|---|
| PC | 3404.292 | 0 | 0 | 0°00'00" | 0 |
| 1 | 3420.000 | 15.708 | 2°30'00" | 2°30'00" | 15.703 |
| 2 | 3450.000 | 30.000 | 4°46'28.7" | 7°16'28.7" | 29.965 |
| 3 | 3480.000 | 30.000 | 4°46'28.7" | 12°02'57.4" | 29.965 |
| 4 | 3510.000 | 30.000 | 4°46'28.7" | 16°49'26.1" | 29.965 |
| 5 | 3540.000 | 30.000 | 4°46'28.7" | 21°35'54.8" | 29.965 |
| 6 | 3570.000 | 30.000 | 4°46'28.7" | 26°22'23.5" | 29.965 |
| PT | 3580.221 | 10.221 | 1°37'36.4" | 28°00'00" | 10.220 |

**Check:** the total deflection at the PT must be $\Delta/2=28^\circ00'00''$, which agrees. (The pegs are located with the peg-to-peg distance of 30 m measured along the curve, i.e. the chord is taken equal to the arc as in Question 5; the last column gives the exact chord if it is preferred.)

**Total deflection to the middle of the curve.** The middle point is at the arc length $L/2$ from the PC, so

$$\delta_{mid}=\frac{L/2}{2R}=\frac{\Delta}{4}=\frac{56^\circ}{4}=\mathbf{14^\circ00'00''}$$

(at chainage $3404.292+87.965=3492.257$ m).

```figure caption="Question 6: simple circular curve R = 180 m, Delta = 56 deg. Tangent length 95.708 m, curve length 175.929 m; the deflection angle to the middle point is Delta/4 = 14 deg."
fig,ax=plt.subplots(figsize=(5.2,3.4)); ax.set_aspect("equal"); ax.axis("off")
R=180; D=np.radians(56); T=R*np.tan(D/2)
PC=np.array([-T,0.0]); PT=np.array([T*np.cos(D),-T*np.sin(D)]); IP=np.array([0.0,0.0])
O=np.array([-T,-R]); a0=np.pi/2; th=np.linspace(a0,a0-D,60)
ax.plot(O[0]+R*np.cos(th),O[1]+R*np.sin(th),color=ACCENT,lw=2.2)
ax.plot([-T-80,0],[0,0],color=INK,lw=1.2); ax.plot([0,(T+80)*np.cos(D)],[0,-(T+80)*np.sin(D)],color=INK,lw=1.2)
for p,n,dx,dy in ((PC,"PC 3404.292",-30,12),(IP,"IP 3500.000",5,12),(PT,"PT 3580.221",8,-22)):
    ax.plot(*p,"o",color="#d9534f",ms=4); ax.text(p[0]+dx,p[1]+dy,n,fontsize=7.5)
ax.plot([PC[0],O[0]],[0,O[1]],color=GRID,lw=1,ls=":"); ax.plot([PT[0],O[0]],[PT[1],O[1]],color=GRID,lw=1,ls=":")
ax.text(-T/2,-18,"T = 95.708 m",ha="center",fontsize=7.5); ax.text(-T+8,-95,"R = 180 m",fontsize=7.5,color=ACCENT)
ax.text(T*0.35,16,"Delta = 56 deg",fontsize=8)
ax.set_xlim(-T-100,T+100); ax.set_ylim(-190,40)
```

@s 7
**General equation of the parabolic vertical curve.** The rate of change of grade is constant along an equal-tangent parabola:

$$\frac{d^2y}{dx^2}=\frac{g_2-g_1}{L}=r$$

where $g_1,g_2$ are the grades (decimal, rising positive) and $L$ is the horizontal length of the curve. Integrating, with the origin at the point of vertical curvature (PVC) where the slope is $g_1$:

$$\begin{gathered}\frac{dy}{dx}=g_1+rx \\ y=y_{PVC}+g_1x+\frac{g_2-g_1}{2L}x^2\end{gathered}$$

**Relations between the parameters.**

- At $x=L$ the slope is $g_2$, and $y_{PVT}=y_{PVC}+\dfrac{(g_1+g_2)L}{2}$.
- PVC and PVT are $L/2$ either side of the IP, so $y_{PVC}=y_{IP}-g_1\dfrac{L}{2}$ and $y_{PVT}=y_{IP}+g_2\dfrac{L}{2}$.
- The vertical offset from the tangent at distance $x$ from the PVC is $y_t=\dfrac{g_2-g_1}{2L}x^2$, proportional to $x^2$. At the IP ($x=L/2$) the offset (external distance) is $e=\dfrac{(g_2-g_1)L}{8}=\dfrac{AL}{800}$, with $A=|G_2-G_1|$ in per cent. The curve passes midway between the IP and the mid-point of the chord PVC-PVT.
- The turning point (summit or sag) is where $dy/dx=0$: $x_m=\dfrac{-g_1L}{g_2-g_1}$ from the PVC (when $g_1$ and $g_2$ have opposite signs).
- The rate of change of grade is $r=\dfrac{g_2-g_1}{L}$.

**Data.** $g_1=-2.75\%$, $g_2=+3.5\%$, so $A=3.5-(-2.75)=6.25\%$: a **sag (valley) curve**. The IP is at chainage 2800.00 m, RL 2470.00 m.

**Length of curve.** The curve passes through RL 2471.25 m at chainage 2800.00 m, which is the chainage of the IP. The offset at the IP is therefore $e=2471.25-2470.00=1.25$ m (above the IP, as it must be for a sag curve).

$$e=\frac{AL}{800}\ \Rightarrow\ L=\frac{800e}{A}=\frac{800\times1.25}{6.25}=\mathbf{160\ m}$$

**PVC and PVT.**

$$\text{Ch(PVC)}=2800-80=2720\ \text{m},\quad \text{RL(PVC)}=2470+0.0275\times80=2472.200\ \text{m}$$

$$\text{Ch(PVT)}=2800+80=2880\ \text{m},\quad \text{RL(PVT)}=2470+0.035\times80=2472.800\ \text{m}$$

**Curve equation.** $y=2472.200-0.0275x+\dfrac{0.0625}{2\times160}\,x^2=2472.200-0.0275x+0.00019531x^2$, with $x$ the distance from the PVC in metres.

**Lowest point.**

$$\begin{gathered}x_m=\frac{2.75\times160}{6.25}=70.4\ \text{m} \\ \text{chainage}=2720+70.4=\mathbf{2790.40\ m}\end{gathered}$$

$$\text{RL}_{min}=2472.200-0.0275(70.4)+0.00019531(70.4)^2=2472.200-1.936+0.968=\mathbf{2471.232\ m}$$

**Elevations at full stations (30 m pegs).**

| Chainage (m) | $x$ from PVC (m) | Tangent RL $=2472.2-0.0275x$ | Offset $0.00019531x^2$ | Curve RL (m) |
|---|---|---|---|---|
| 2720 (PVC) | 0 | 2472.2000 | 0.0000 | 2472.200 |
| 2730 | 10 | 2471.9250 | 0.0195 | 2471.945 |
| 2760 | 40 | 2471.1000 | 0.3125 | 2471.413 |
| 2790 | 70 | 2470.2750 | 0.9570 | 2471.232 |
| 2800 (IP) | 80 | 2470.0000 | 1.2500 | 2471.250 |
| 2820 | 100 | 2469.4500 | 1.9531 | 2471.403 |
| 2850 | 130 | 2468.6250 | 3.3008 | 2471.926 |
| 2880 (PVT) | 160 | 2467.8000 | 5.0000 | 2472.800 |

The tangent RL in the table is the first grade line extended (at the PVT it is $2467.80$ m), and the offset of $4e=5.00$ m at the PVT brings the curve back to RL $2472.80$ m, which checks with the PVT level found from the second tangent. The full stations are 2730, 2760, 2790, 2820 and 2850 m, plus the end points PVC 2720 m and PVT 2880 m.

```figure caption="Question 7: equal-tangent sag vertical curve, L = 160 m, g1 = -2.75 %, g2 = +3.5 %. The low point is at chainage 2790.40 m, RL 2471.232 m."
fig,ax=plt.subplots(figsize=(5.8,2.9))
x=np.linspace(0,160,100); y=2472.2-0.0275*x+0.0625/320*x**2
ax.plot(2720+x,y,color=ACCENT,lw=2.2,label="vertical curve")
ax.plot([2640,2800,2960],[2470+0.0275*160,2470,2470+0.035*160],color=MUTED,lw=1,ls="--",label="grade lines")
for c,r_,n,dy in ((2720,2472.2,"PVC 2472.200",0.35),(2880,2472.8,"PVT 2472.800",0.35),(2790.4,2471.232,"lowest 2790.40 / 2471.232",-0.75)):
    ax.plot(c,r_,"o",color="#d9534f",ms=4); ax.text(c,r_+dy,n,fontsize=6.5,ha="center")
ax.plot(2800,2470,"s",color=INK,ms=4); ax.text(2800,2469.55,"IP 2470.00",fontsize=6.5,ha="center")
ax.set_xlabel("Chainage (m)",fontsize=8); ax.set_ylabel("RL (m)",fontsize=8); ax.legend(fontsize=7,loc="upper center"); ax.grid(color=GRID,lw=0.5); ax.set_ylim(2468.8,2474.8)
```

@s 8
**Relief displacement.** On a vertical aerial photograph the scale is true only on a plane at the datum (or the mean ground plane). A point above or below that plane is displaced radially from the principal point (nadir). The displacement is

$$d=\frac{r\,h}{H}$$

where $r$ is the radial distance of the displaced image from the principal point, $h$ the height of the object above the datum and $H$ the flying height above the datum (measured to the base of the object, with $r$ taken to the top, $h=dH/r$ is used to find the height of towers and buildings from a single photo).

- It is **radial** from the nadir: zero at the principal point and largest at the edges of the photograph.
- A point **above** the datum is displaced *outwards*; a point below it *inwards*.
- It increases with the height of the object and the distance from the nadir, and decreases with the flying height.
- Orthorectification, or the use of the central part of overlapping photos (stereo pairs), removes or reduces it.

**Drone regulation in Nepal and flight permission.** Drones (unmanned aircraft, UAS/RPAS) are regulated by the **Civil Aviation Authority of Nepal (CAAN)** under the Civil Aviation Act and its UAS requirements, with permission from other agencies for sensitive areas. In general (check the latest CAAN notice before every flight):

- the drone must be **registered** with CAAN, and the pilot must be trained and authorised for commercial work;
- a **flight permission** is needed from CAAN, and for aerial photography or mapping also from the Ministry of Home Affairs (or the local administration) and the Survey Department for mapping; some districts and the security forces require extra consent;
- flights are limited in height (normally **below 120 m / 400 ft above ground**), kept in **visual line of sight**, in daylight and within weather limits;
- **no flying** near airports and flight paths, over crowds, security installations, border areas or national parks without permission, or over private property without consent;
- rules on insurance, privacy and security of the images taken also apply.

**Uses of drones in civil engineering.** Topographic and corridor surveys for roads, canals and transmission lines; photogrammetric DEM and contour maps; volume computation of stockpiles and earthwork; progress monitoring and inspection of construction sites; inspection of bridges, dams, tall structures and landslide areas that are difficult to reach; disaster assessment (flood, earthquake, landslide); cadastral and land-use mapping; and 3D modelling of buildings and heritage structures.

@s 9
**DGPS against normal (standalone) GPS.** In standalone GPS a single receiver computes its position from pseudo-ranges that contain **common errors**: satellite clock and orbit (ephemeris) errors, and ionospheric and tropospheric delay (and selective availability, when it was on). The accuracy is 5 to 10 m horizontally.

In **Differential GPS (DGPS)** a *reference (base) station* is placed on a point of exactly known coordinates. It compares the range computed from every satellite with the true range and finds a **correction** for each satellite. These corrections are sent (by radio, mobile network or satellite) in real time, or applied in post-processing, to the *rover*, which applies them.

Advantages:

- the errors in the signals are nearly the same for two receivers within about 100 to 200 km, so they are **cancelled**;
- accuracy rises to 1 to 3 m (code-based DGPS) and to **centimetre or millimetre** level with carrier-phase differential methods (RTK, static, PPK);
- a faster, more reliable fix with integrity, so it can be used for control surveys, cadastral mapping, engineering layout, machine guidance and GIS data collection where plain GPS is too coarse.

**Applications of remote sensing in civil engineering.**

- Land-use and land-cover mapping, site selection and route alignment for roads, canals, pipelines and transmission lines;
- terrain analysis, DEM and slope maps, watershed and drainage delineation, **hydrological studies** and flood-plain mapping;
- identification of **landslide, erosion and fault** zones, and geological and soil mapping for foundations and construction materials;
- monitoring of reservoirs, river morphology, glacial lakes, construction progress and ground subsidence (InSAR);
- urban planning, infrastructure inventory and post-disaster damage assessment.

@s 10
**Uses of hydrographic survey in civil engineering.**

1. Measuring the **depth and bed profile** of rivers, lakes, reservoirs and harbours (soundings) for the design of dams, weirs, bridges, intakes and barrages;
2. determining **storage capacity** and **siltation** of reservoirs by comparing repeat surveys;
3. planning and maintenance of **navigation channels, ports and jetties**, and dredging quantities;
4. finding **scour** around bridge piers and foundations, and the stream cross-section for discharge computation;
5. locating submerged structures, pipelines and obstructions, and fixing the shoreline and water-level (tide) data.

**Echo sounding.** The depth is found from the time taken by a sound (ultrasonic) pulse to travel to the bed and return. A **transducer** fixed below the boat sends a pulse (about 30 to 200 kHz); the receiver measures the two-way time $t$ of the echo. The depth below the transducer is

$$D=\frac{v\,t}{2}$$

where $v$ is the speed of sound in water ($\approx1450$ to $1500$ m/s, depending on temperature, salinity and pressure, calibrated by a *bar check*: lowering a plate to known depths). The water depth is $D_w=D+d_t$, where $d_t$ is the draught of the transducer below the water surface; a correction for water level (tide) to the datum is added, and the position of each sounding is fixed with a total station, DGPS or sextant angles. The recorder draws a continuous trace of the bed profile along the line of travel; sounding lines run at right angles to the shore at a spacing of a few tens of metres, with cross-lines for checking.

```figure caption="Question 10: principle of echo sounding. The pulse travels to the bed and back in time t, giving D = vt/2."
fig,ax=plt.subplots(figsize=(5.2,2.5)); ax.axis("off")
ax.fill_between([0,10],[0,0],[-3,-3],color=ACCENT,alpha=0.12); ax.plot([0,10],[0,0],color=ACCENT,lw=1.2)
xs=np.linspace(0,10,60); bed=-2.6-0.5*np.sin(xs*0.8); ax.plot(xs,bed,color="#8a6d3b",lw=2)
ax.fill_between(xs,bed,-3.6,color="#8a6d3b",alpha=0.25)
ax.fill([3.2,5.8,5.0,4.0],[0.22,0.22,0.5,0.5],color=INK); ax.plot([4.5,4.5],[0.5,0.9],color=INK,lw=1)
ax.plot([4.5],[-0.12],"s",color="#d9534f",ms=4); ax.text(5.1,-0.2,"transducer",fontsize=7.5)
ax.annotate("",xy=(4.35,-2.9),xytext=(4.35,-0.15),arrowprops=dict(arrowstyle="-|>",color="#d9534f")); ax.annotate("",xy=(4.65,-0.15),xytext=(4.65,-2.9),arrowprops=dict(arrowstyle="-|>",color=ACCENT))
ax.annotate("",xy=(8.2,-2.9),xytext=(8.2,0),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(8.35,-1.5,"D = vt/2",fontsize=8)
ax.text(2.8,-1.0,"pulse",fontsize=7.5,color="#d9534f"); ax.text(4.8,-1.0,"echo",fontsize=7.5,color=ACCENT); ax.set_xlim(0,10); ax.set_ylim(-3.7,1.1)
```

@s 11
**Linear method of building layout.** The building is set out by *linear measurements only* (tape or EDM) from a **baseline** or from existing reference lines (the road edge or boundary line, or a line parallel to it at a given offset), without angle-measuring instruments.

1. Fix the **baseline** (e.g. parallel to the front boundary at the set-back distance). Mark the corner of the building by measuring from a reference point along the baseline and by a perpendicular offset from it.
2. Set out the right angle by the **3-4-5 (Pythagorean) triangle**, e.g. 3 m, 4 m, 5 m (or 6, 8, 10 m for large buildings), forming the perpendicular offset at the corner.
3. Complete the rectangle with the **building dimensions**, then **check by measuring both diagonals**, which must be equal for a rectangle (and opposite sides equal). Fix the corners with pegs.
4. Establish **batter boards (profile boards)** at a safe distance, e.g. 1.5 to 2 m outside the excavation line, with nails or saw-cuts to carry the strings for the wall centre lines, so the lines can be replaced after the excavation.

*Example.* A 10 m by 8 m room is to be placed 5 m behind the road edge and 3 m from the boundary. From the boundary point measure 3 m along the road edge and offset 5 m perpendicular (3-4-5 check) to fix corner $P$. Mark $Q$ 10 m along the line parallel to the road, and $S$ 8 m on the perpendicular from $P$ (6-8-10 triangle). The fourth corner $R$ comes from the arcs $QR=8$ m and $SR=10$ m. The check is $PR=QS=\sqrt{10^2+8^2}=12.81$ m.

```figure caption="Question 11: linear method. Rectangle PQRS is laid out from the baseline with a 3-4-5 right angle and checked with equal diagonals PR = QS."
fig,ax=plt.subplots(figsize=(4.8,3.0)); ax.axis("off")
ax.plot([-0.5,11],[0,0],color=INK,lw=2); ax.text(11,-0.5,"road edge / baseline",fontsize=7,ha="right")
P=(2.0,3.0);Q=(8.0,3.0);R=(8.0,7.0);S=(2.0,7.0)
ax.plot([P[0],Q[0],R[0],S[0],P[0]],[P[1],Q[1],R[1],S[1],P[1]],color=ACCENT,lw=2)
ax.plot([P[0],R[0]],[P[1],R[1]],color="#d9534f",lw=1,ls="--"); ax.plot([Q[0],S[0]],[Q[1],S[1]],color="#d9534f",lw=1,ls="--")
for pt,n,dx,dy in ((P,"P",-0.4,-0.5),(Q,"Q",0.15,-0.5),(R,"R",0.15,0.15),(S,"S",-0.4,0.15)): ax.text(pt[0]+dx,pt[1]+dy,n,fontsize=9)
ax.plot([2,2],[0,3],color=MUTED,lw=0.8,ls=":"); ax.text(0.2,1.4,"set-back (offset)",fontsize=7,color=MUTED)
ax.text(5,2.4,"10 m",ha="center",fontsize=7.5); ax.text(8.2,5,"8 m",fontsize=7.5); ax.text(3.2,4.6,"equal diagonals",fontsize=7,color="#d9534f",rotation=33)
ax.set_xlim(-0.8,11.2); ax.set_ylim(-0.9,7.8)
```

**Gyroscope in tunnel alignment.** In a long tunnel the headings are driven from the two portals or from shafts, and the surface sight line cannot be carried underground. A **gyro-theodolite** (a gyroscope fixed on a theodolite) is used because:

- a gyroscope with its spin axis horizontal, acted on by the earth's rotation, oscillates about the **true (geographic) meridian** by itself, independently of magnetism and of the steel of the machinery, rails or lining;
- so the **azimuth of a line** underground (or at the bottom of a shaft) is found directly, with no line of sight to the surface, and no transfer through a pair of plumb lines whose short base magnifies the errors;
- it provides an independent azimuth check on the underground traverse and controls the **direction error**, which grows with the tunnel length, thus giving the accuracy of the breakthrough where the two headings meet.

The observations are repeated several times (reversal-point or transit method) to find the direction of true north.

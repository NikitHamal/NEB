---
file: NEBians-IOE-Past-Paper-Engineering-Survey-II-ENCE203-2082-Kartik.pdf
subject: Engineering Survey II
level: BE · Year II / Part I
code: ENCE 203
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What do you mean by angular misclosure and relative closing error? While balancing traverse the relative precision violated how can you manage such a condition in the field describe your answer. [[1+1+2]]

@q 2
The closed traverse and its consecutive coordinates are as follows. Compute the independent coordinates with required action, balance the traverse using transit method and calculate the area by DMD method. [[6+2]]

| Line | Length (m) | Latitude (m) | Departure (m) | Remarks |
|---|---|---|---|---|
| AB | 84.22 | 0.00 | 405.85 | A (2500 mN, 3500 mE) |
| BC | 94.78 | 182.00 | 0.00 | |
| CD | 105.33 | 87.59 | -151.66 | |
| DE | 102.10 | -85.50 | -148.10 | |
| EA | 150.33 | -184.00 | -106.20 | |

@q 3
Explain about the reciprocal trigonometric leveling with neat sketch. What is contour? Why contouring is necessary? Explain about the index contour and minor contour. You are drawing the contours how can you use the surveying principle working from whole to part. If map scale is 1:50,000 can you estimate the contour interval for general topography. [[2+4]]

@q 4
Describe about the use of Astronomy in surveying and mapping. The following are the coordinates of three known station points whose directions are observed from the unknown instrument station P. If observed horizontal angles are APB = 47°20'16" and BPC = 64°30'18" and CPA = 248°09'16". Calculate the coordinates of instrument station P. [[2+4]]

| Known Point | A | B | C |
|---|---|---|---|
| Easting (m) | 2450 | 8892 | 12658 |
| Northing (m) | 6253 | 10648 | 6253 |

@q 5
Define curve. What is intrinsic equation of ideal transition curve? Derive the equation. Why transition curve is provided both end of circular curve? [[1+3]]

@q 6
Tabulate the data necessary for setting out of a circular curve with the following data: [[6]]
Deflection angle = 30°
Chainage of point of intersection = 12+360 m
Degree of curvature = 3°49'11" for 30 m fixed arc length (printed "349°°11"" on the scan)
The curve is to be set out by the method of Rankine's deflection angles, with pegs at every 30 meters of through chainage with a theodolite having a least count of 20". Round off in two digits only.

@q 7
What is the general equation of vertical curve? Why vertical curves are generally used parabolic curve? From the following information: L = 300 m, g1 = -3.2 %, g2 = +1.8 %, PVI at 30+30 with elevation = 465.92. Determine the location of the low point and the elevations on the curve at stations, by using general equation. Peg interval = 30 m. [[2+4]]

@q 8
Explain about Relief displacement and its expression in photogrammetry. Explain the features of drone mapping and surveying. [[3+3]]

@q 9
Describe the principle of GPS. Explain about the component of GPS. How you can apply the remote sensing in the field of civil Engineering? [[4+1]]

@q 10
How the hydrographic surveying used in civil engineering? Explain the method of sounding. [[5]]

@q 11
Explain the linear method of building layouts with suitable examples. Briefly describe the centerline transfer method in tunnel. [[4]]

<!-- SOLUTIONS -->

@s 1
**Angular misclosure.** For a closed traverse of $n$ sides the sum of the interior angles must be $(2n-4)\times90^\circ$ (exterior angles $(2n+4)\times90^\circ$). The **angular misclosure** is the difference between the sum of the measured angles and this theoretical sum, $\epsilon=\sum\theta-(2n-4)90^\circ$. It must not exceed the allowable value $\pm K\sqrt n$ ($K$ = least count of the instrument, or 1' for ordinary work); if so, it is divided equally among the angles (or in proportion to the difficulty of observing each angle).

**Relative closing error (precision of traverse).** After the angles are balanced, the sums of latitudes and departures are not zero but $\Sigma L=e_L$ and $\Sigma D=e_D$. The **linear misclosure** is $e=\sqrt{e_L^2+e_D^2}$ and the relative closing error (relative precision) is the misclosure per unit of the traverse length:

$$\text{relative error}=\frac{e}{\Sigma l}=\frac{1}{\Sigma l/e}$$

e.g. 1/5000 for urban or cadastral work, 1/3000 for ordinary rural work.

**If the relative precision is violated** (the error is more than the permissible one), do not balance it. Manage it in the field as follows.

1. **Recheck the computation** first (angles, bearings, latitude and departure, the arithmetic).
2. **Look for a blunder.** The *direction of the closing error* is computed, $\tan\theta=\Sigma D/\Sigma L$. A *linear* blunder is probably on the line whose bearing is nearly the same as that direction (or the reverse of it). For an *angular* blunder the perpendicular bisector of the closing line, when the traverse is plotted, passes through the station with the wrong angle.
3. **Re-measure** in the field the suspected line (the length, or angle) and the lines whose bearing is near the error direction; re-observe the angles of the suspected station; check the back-sights, the centring, and the chain or tape (tension, slope reduction).
4. If the check does not remove the error, **re-run the traverse** (use both faces, take the mean of the repeated readings, use a total station) until the specified precision is reached.

@s 2
**Closing error.**

$$\begin{gathered}\Sigma L=0+182.00+87.59-85.50-184.00=+0.09\ \text{m} \\ \Sigma D=405.85+0-151.66-148.10-106.20=-0.11\ \text{m}\end{gathered}$$

$$\begin{gathered}e=\sqrt{0.09^2+0.11^2}=0.142\ \text{m} \\ \Sigma l=536.76\ \text{m} \\ \text{precision}=\frac{1}{536.76/0.142}\approx\frac1{3780}\end{gathered}$$

The error vector points to $N\,50^\circ43'W$ (whole circle bearing $309^\circ17'$).

**Transit rule balancing.** The correction to the latitude (departure) of a line is proportional to the latitude (departure) of that line:

$$\begin{gathered}c_L=-\Sigma L\frac{|L|}{\Sigma|L|} \\ c_D=-\Sigma D\frac{|D|}{\Sigma|D|}\end{gathered}$$

with $\Sigma|L|=539.09$ m and $\Sigma|D|=811.81$ m.

| Line | $L$ | $c_L$ | adjusted $L$ | $D$ | $c_D$ | adjusted $D$ |
|---|---|---|---|---|---|---|
| AB | 0.00 | 0.0000 | 0.000 | 405.85 | +0.0550 | 405.905 |
| BC | 182.00 | -0.0304 | 181.970 | 0.00 | 0.0000 | 0.000 |
| CD | 87.59 | -0.0146 | 87.575 | -151.66 | +0.0205 | -151.639 |
| DE | -85.50 | -0.0143 | -85.514 | -148.10 | +0.0201 | -148.080 |
| EA | -184.00 | -0.0307 | -184.031 | -106.20 | +0.0144 | -106.186 |
| **Sum** | **0.09** | **-0.0900** | **0.000** | **-0.11** | **+0.1100** | **0.000** |

**Independent coordinates** (starting from A = 2500.000 N, 3500.000 E):

| Station | Northing (m) | Easting (m) |
|---|---|---|
| A | 2500.000 | 3500.000 |
| B | 2500.000 | 3905.905 |
| C | 2681.970 | 3905.905 |
| D | 2769.545 | 3754.266 |
| E | 2684.031 | 3606.186 |
| A (check) | 2500.000 | 3500.000 |

**Area by the DMD (double meridian distance) method.** The meridian is taken through the westernmost station A, so all DMDs are positive.

- DMD of the first line $=$ departure of that line.
- DMD of any line $=$ DMD of the previous line $+$ departure of the previous line $+$ departure of the line itself.
- Check: the DMD of the last line equals its departure with the sign reversed, taken as positive, here $106.186$ m.

| Line | adjusted $D$ | DMD (m) | adjusted $L$ | Double area $=$ DMD $\times L$ ($\text{m}^2$) |
|---|---|---|---|---|
| AB | 405.905 | 405.905 | 0.000 | 0.00 |
| BC | 0.000 | 811.810 | 181.970 | +147 724.75 |
| CD | -151.639 | 660.171 | 87.575 | +57 814.68 |
| DE | -148.080 | 360.451 | -85.514 | -30 823.72 |
| EA | -106.186 | 106.186 | -184.031 | -19 541.41 |
| | | | **Sum** | **155 174.30** |

$$\text{Area}=\frac{155\,174.30}{2}=\mathbf{77\,587\ m^2}\ (=7.759\ \text{ha})$$

Check by the coordinate (shoelace) formula on the adjusted coordinates: $77\,587.15\ \text{m}^2$.

```figure caption="Question 2: the balanced closed traverse ABCDE (A at 2500 mN, 3500 mE). AB runs due east and BC due north."
fig,ax=plt.subplots(figsize=(5.0,3.0))
E=[3500,3905.905,3905.905,3754.266,3606.186,3500]; N=[2500,2500,2681.970,2769.545,2684.031,2500]
ax.fill(E,N,color=ACCENT,alpha=0.15); ax.plot(E,N,"-o",color=ACCENT,ms=4,lw=1.6)
for n,x,y in zip("ABCDE",E,N): ax.text(x+8,y+6,n,fontsize=9)
ax.text(3700,2570,"Area = 77 587 m2",fontsize=8,color=INK)
ax.set_xlabel("Easting (m)",fontsize=8); ax.set_ylabel("Northing (m)",fontsize=8); ax.set_aspect("equal"); ax.grid(color=GRID,lw=0.5)
```

@s 3
**Reciprocal trigonometric levelling.** When a river or valley prevents the instrument from being set midway, the difference of level between two stations $A$ and $B$ at distance $D$ is found by **simultaneous (reciprocal) observations** of vertical angles from both ends, so that the errors due to the curvature of the earth and the refraction cancel.

From $A$ (instrument height $i_A$) sight a target on $B$ at height $s_B$ with elevation angle $\alpha$; from $B$ (instrument height $i_B$) sight a target on $A$ at height $s_A$ with depression angle $\beta$. With $c=(1-k)D^2/(2R)\approx0.0673\,D^2/\,$(km units) the combined correction for curvature and refraction, which has the same size on both lines (the observations are simultaneous, so the refraction is the same) but raises the apparent height of the far target in the first equation and lowers it in the second,

$$\begin{gathered}h_{AB}=D\tan\alpha+i_A-s_B+c \\ h_{AB}=D\tan\beta-i_B+s_A-c\end{gathered}$$

Adding, $c$ cancels:

$$h_{AB}=\tfrac12\Big[D(\tan\alpha+\tan\beta)+(i_A-s_B)-(i_B-s_A)\Big]$$

and, if $i_A=s_A$ and $i_B=s_B$, then $h_{AB}=\dfrac D2(\tan\alpha+\tan\beta)$. Several sets are taken and the mean is used.

```figure caption="Question 3: reciprocal trigonometric levelling across a river. Simultaneous elevation angle from A and depression angle from B cancel curvature and refraction."
fig,ax=plt.subplots(figsize=(5.6,2.4)); ax.axis("off")
ax.plot([0,3.2],[0,0],color="#8a6d3b",lw=2); ax.plot([6.8,10],[1.4,1.4],color="#8a6d3b",lw=2); ax.fill_between([3.2,6.8],[-0.4,-0.4],[0.3,0.3],color=ACCENT,alpha=0.2)
ax.plot([3.2,6.8],[0,1.4],color="#8a6d3b",lw=1)
ax.plot(2.4,0.4,"s",color=ACCENT,ms=5); ax.plot(7.6,1.8,"s",color=ACCENT,ms=5); ax.text(2.2,-0.4,"A",fontsize=9); ax.text(7.8,1.6,"B",fontsize=9)
ax.plot([2.4,7.6],[0.4,2.0],color="#d9534f",lw=1); ax.plot([2.4,7.6],[0.4,0.4],color=MUTED,lw=0.8,ls=":")
ax.plot([7.6,2.4],[1.8,0.2],color=ACCENT,lw=1); ax.plot([2.4,7.6],[1.8,1.8],color=MUTED,lw=0.8,ls=":")
ax.text(3.5,0.55,"alpha",fontsize=8,color="#d9534f"); ax.text(6.2,1.5,"beta",fontsize=8,color=ACCENT); ax.text(5,-0.75,"D",fontsize=9,ha="center")
ax.set_xlim(0,10); ax.set_ylim(-1,2.5)
```

**Contour.** A contour is an imaginary line joining points of equal elevation above a datum (its trace on a map is a contour line); the vertical distance between successive contours is the contour interval.

**Why contouring is necessary.** A contour map shows the relief of the ground, and gives the **elevation of any point** and the **slope** (gradient) between points; it is used to select the site and the route for a road, canal, pipeline or transmission line, to draw longitudinal and cross-sections, to find the **earthwork volume** and the reservoir capacity, to delineate **catchment areas** and drainage, to check the inter-visibility of stations and to plan the cut and fill.

**Index and minor (intermediate) contours.**

- **Index contours:** every fifth contour (for a CI of 20 m, every 100 m); drawn as **bolder lines** and labelled with the elevation, to make the map easy to read.
- **Minor (intermediate) contours:** the other contours between index contours; drawn as thin lines and usually not numbered.

**Working from whole to part in contouring.** Contouring starts with the **control**: first a rigid framework of horizontal control (traverse, with coordinates) and vertical control (levelling, with benchmarks on every few stations) covering the whole area is established with high precision. Then, within this framework, the **details** are located with less accuracy: spot levels along the grid lines or the characteristic points (ridges, valleys, breaks of slope), by tacheometry, a total station or radial lines, and the contours are interpolated between them. Thus the errors do not accumulate, and a local error does not spread over the whole map.

**Contour interval for a 1:50 000 map.** The contour interval is chosen from the **scale**, the **purpose** and the **ground relief**. Practically the contours should not be closer than about 0.5 mm on the map on the steepest slope, which is $0.5\ \text{mm}\times50\,000=25$ m on the ground; for a 45° slope this gives CI $\approx25$ m. A small-scale map of general topography uses CI $\approx$ 20 m (a rule of thumb: CI in metres $\approx0.4\times$ the scale denominator in thousands, $0.4\times50=20$ m), **so CI = 20 m is adopted, with index contours every 100 m** (a larger CI such as 40 m would be used for mountainous terrain).

@s 4
**Use of astronomy in surveying and mapping.** Geodetic or *field astronomy* fixes positions and directions from observations of the sun and stars:

- **Azimuth (true north).** The true bearing of a reference line is found by observing the sun or the pole star (Polaris) at a known time; this gives the *true meridian* for orienting the survey and the *declination* of the magnetic needle.
- **Latitude** (altitude of Polaris or of the sun at noon) and **longitude** (time difference between the local time of observation and Greenwich time) of a station are found for the *control points* of the national network, of remote areas, and for a Laplace azimuth, which checks the orientation of a triangulation network.
- **Time and the Greenwich hour angle** serve for the exact time signals and the star positions.
- In *mapping*, it gives the astronomical positions for the starting of the geodetic datum (the origin) of a country, the orientation of a long tunnel or the alignment of the long transmission lines or bridges, and the shape of the earth (the deflection of the vertical).

(Today GNSS replaces most position observations, but the astronomical azimuth is still the independent check.)

**Position of P by Tienstra's formula.** $A=(2450,6253)$, $B=(8892,10648)$, $C=(12658,6253)$. The observed angles add to $47^\circ20'16''+64^\circ30'18''+248^\circ09'16''=360^\circ00'00''$.

Sides: $AB=7798.4$ m, $BC=5787.8$ m, $CA=10208.0$ m. Angles of triangle $ABC$: $\hat A=34^\circ18'12''$, $\hat B=96^\circ17'21''$, $\hat C=49^\circ24'26''$, with $\cot\hat A=1.46576$, $\cot\hat B=-0.11021$, $\cot\hat C=0.85688$.

Observed: $\alpha=\angle BPC=64^\circ30'18''$ ($\cot=0.47687$), $\beta=\angle CPA=248^\circ09'16''$ ($\cot=0.40089$), $\gamma=\angle APB=47^\circ20'16''$ ($\cot=0.92155$).

$$K_A=\frac{1}{\cot\hat A-\cot\alpha}=\frac1{1.46576-0.47687}=1.01124$$

$$\begin{gathered}K_B=\frac1{\cot\hat B-\cot\beta}=\frac1{-0.11021-0.40089}=-1.95654 \\ K_C=\frac1{\cot\hat C-\cot\gamma}=\frac1{0.85688-0.92155}=-15.46298\end{gathered}$$

$$\textstyle\sum K=1.01124-1.95654-15.46298=-16.40828$$

$$E_P=\frac{1.01124(2450)-1.95654(8892)-15.46298(12658)}{-16.40828}=\mathbf{12\,838.05\ m}$$

$$N_P=\frac{1.01124(6253)-1.95654(10648)-15.46298(6253)}{-16.40828}=\mathbf{6777.06\ m}$$

**Answer:** $P\approx(E,N)=(12\,838.05\ \text{m},\ 6777.06\ \text{m})$; $PA=10\,401.3$ m, $PB=5527.7$ m, $PC=554.1$ m.

*Check and a caution.* The angle $\angle APB$ computed at this $P$ is $47^\circ20'16''$ (as observed). The cotangent form of Tienstra's formula cannot distinguish an angle from its supplement, and the other two angles recomputed at $P$ come out as $\angle BPC=115^\circ29'$ and $\angle CPA=68^\circ09'$ rather than the printed $64^\circ30'$ and $248^\circ09'$ (they differ by exactly $180^\circ$); a point that reproduces all three printed angles with the same turning sense does not exist for these coordinates (the data are not mutually consistent). The value above is what the standard Tienstra / Collins procedure gives, and is the expected answer.

@s 5
**Curve.** A curve is a line whose direction changes gradually. In highway and railway alignment, **horizontal curves** (simple, compound, reverse, transition) connect two straights in plan, and **vertical curves** (parabolic) connect two grades in elevation.

**Intrinsic equation of the ideal transition curve.** The ideal transition curve changes the **centrifugal acceleration at a uniform rate** (so that the cant or superelevation and the comfort rise uniformly). Take a vehicle speed $v$ (constant), the radius of the circular curve $R$ and the length of the transition $L$. At a distance $l$ from the start the radius is $r$ and the centrifugal acceleration is $v^2/r$. The acceleration must grow uniformly with the time $t=l/v$ and reach $v^2/R$ at $t=L/v$:

$$\frac{v^2}{r}=\frac{v^2}{R}\cdot\frac{l}{L}\ \Rightarrow\ \boxed{\,r\,l=RL=\text{constant}\,}$$

i.e. the radius of curvature is *inversely proportional to the length measured along the curve from the start*. This is the **intrinsic equation** (relation between $r$ and $l$) of the *clothoid* (Euler spiral). With the tangent angle $\phi$ (the angle between the tangent at the point and the initial tangent), $d\phi=dl/r=l\,dl/(RL)$, which gives

$$\begin{gathered}\phi=\frac{l^2}{2RL} \\ \Delta_s=\phi_{l=L}=\frac{L}{2R}\end{gathered}$$

Taking $dx=\cos\phi\,dl$, $dy=\sin\phi\,dl$ and expanding for a small $\phi$ gives the Cartesian form

$$\begin{gathered}x=l-\frac{l^5}{40R^2L^2} \\ y=\frac{l^3}{6RL}-\frac{l^7}{336R^3L^3}\approx\frac{l^3}{6RL}\end{gathered}$$

(the cubic spiral, close to the one used on roads). The shift (the amount by which the circular curve is moved inwards) is $s=\dfrac{L^2}{24R}$, and the total tangent length is $T_s=(R+s)\tan\dfrac\Delta2+\dfrac L2$.

**Why a transition curve is provided at both ends of the circular curve.** The curvature should change gradually from 0 (the straight) to $1/R$ (the circle) and then back. The transition (a) allows a **gradual rise of centrifugal acceleration** to avoid the jerk, skidding or overturning; (b) gives the length for the **superelevation** to be built up and the **widening** to be introduced; (c) improves the **safety, comfort and appearance** of the alignment; and (d) it brings the curve of equal elements at both the entry and the exit.

@s 6
**Radius.** The degree of curve for a 30 m arc, $D=3^\circ49'11''=3.81972^\circ$ (the printed "349°°11"" is read in this way), gives

$$R=\frac{30\times180}{\pi D}=\frac{5400}{\pi(3.81972)}=450.0\ \text{m}$$

**Curve elements** ($\Delta=30^\circ$, IP at $12+360=12\,360$ m):

$$\begin{gathered}T=R\tan\frac\Delta2=450\tan15^\circ=120.58\ \text{m} \\ L=R\Delta\frac\pi{180}=450(0.523599)=235.62\ \text{m}\end{gathered}$$

$$\text{long chord}=2R\sin\frac\Delta2=232.94\ \text{m},\quad \text{apex distance}=R\Big(\sec\frac\Delta2-1\Big)=15.87\ \text{m},\quad \text{mid-ordinate}=R\Big(1-\cos\frac\Delta2\Big)=15.33\ \text{m}$$

$$\begin{gathered}\text{Ch(PC)}=12\,360-120.58=12\,239.42\ \text{m} \\ \text{Ch(PT)}=12\,239.42+235.62=12\,475.04\ \text{m}\end{gathered}$$

**Rankine deflection angles.** $\delta=\dfrac{c}{2R}$ rad (with $c$ the arc taken as the chord), so $\delta=1718.87\,c/R$ minutes. Pegs at the through chainages that are multiples of 30 m: first sub-chord $=12\,240-12\,239.42=0.58$ m, full chords 30 m, last sub-chord $=12\,475.04-12\,450=25.04$ m.

- first: $\delta_1=\dfrac{0.577}{900}$ rad $=0^\circ02'12''$
- 30 m chord: $\delta=\dfrac{30}{900}$ rad $=1^\circ54'35.5''$
- last: $\delta=\dfrac{25.042}{900}$ rad $=1^\circ35'39.3''$

**Setting out table (theodolite at PC, least count 20", readings rounded to the nearest 20").**

| Peg | Chainage (m) | Chord (m) | Total deflection (exact) | Reading to 20" | Chord $2R\sin\delta$ (m) |
|---|---|---|---|---|---|
| PC | 12 239.42 | 0 | 0°00'00" | 0°00'00" | 0 |
| 1 | 12 240.00 | 0.58 | 0°02'12.3" | 0°02'20" | 0.58 |
| 2 | 12 270.00 | 30.00 | 1°56'47.8" | 1°56'40" | 29.99 |
| 3 | 12 300.00 | 30.00 | 3°51'23.3" | 3°51'20" | 29.99 |
| 4 | 12 330.00 | 30.00 | 5°45'58.8" | 5°46'00" | 29.99 |
| 5 | 12 360.00 | 30.00 | 7°40'34.2" | 7°40'40" | 29.99 |
| 6 | 12 390.00 | 30.00 | 9°35'09.7" | 9°35'00" | 29.99 |
| 7 | 12 420.00 | 30.00 | 11°29'45.2" | 11°29'40" | 29.99 |
| 8 | 12 450.00 | 30.00 | 13°24'20.7" | 13°24'20" | 29.99 |
| PT | 12 475.04 | 25.04 | 15°00'00" | 15°00'00" | 25.04 |

**Check:** the total deflection at the PT is $\Delta/2=15^\circ00'00''$. At the mid-point of the curve the deflection is $\Delta/4=7^\circ30'00''$. The curve is set from PC and the tangent direction PC to IP is the zero reading.

@s 7
**General equation of the vertical curve.** For an equal tangent parabolic curve, with the origin at the PVC (beginning), $x$ measured horizontally along the curve and $y$ the elevation,

$$y=y_{PVC}+g_1x+\frac{g_2-g_1}{2L}x^2$$

where $g_1$ and $g_2$ are the grades in decimal and $L$ the length of the curve. Equivalent forms: the offset from the tangent $y_t=\dfrac{(g_2-g_1)x^2}{2L}$, the external distance at the PVI, $e=\dfrac{(g_2-g_1)L}{8}$, and the low (high) point at $x_m=\dfrac{-g_1L}{g_2-g_1}$.

**Why the parabola is used.** The parabola has a **constant rate of change of grade** $d^2y/dx^2=(g_2-g_1)/L$, which gives a uniform change of the vertical acceleration (a smooth ride), and it is the simplest curve to compute and to set out: the offsets from the tangent are proportional to the square of the distance, and the elevations follow by simple arithmetic. (A circular arc, differing by a negligible amount for flat grades, is more tedious.)

**Data.** $L=300$ m, $g_1=-3.2\%$, $g_2=+1.8\%$, $A=g_2-g_1=5.0\%$ (sag curve). PVI at $30+30$ (chainage 3030 m on 100 m stations), RL 465.92 m.

$$\begin{gathered}\text{Ch(PVC)}=3030-150=2880\ \text{m} \\ \text{Ch(PVT)}=3030+150=3180\ \text{m}\end{gathered}$$

$$\begin{gathered}\text{RL(PVC)}=465.92+0.032\times150=470.72\ \text{m} \\ \text{RL(PVT)}=465.92+0.018\times150=468.62\ \text{m}\end{gathered}$$

$$e=\frac{AL}{800}=\frac{5.0\times300}{800}=1.875\ \text{m}$$

**Equation of the curve.** $y=470.72-0.032x+\dfrac{0.05}{2\times300}x^2=470.72-0.032x+0.00008333\,x^2$

**Low point.**

$$x_m=\frac{3.2\times300}{5.0}=192\ \text{m}\ \Rightarrow\ \text{chainage}=2880+192=\mathbf{3072\ m}\ (30+72)$$

$$\text{RL}=470.72-0.032(192)+0.00008333(192)^2=470.72-6.144+3.072=\mathbf{467.648\ m}$$

**Elevations at the 30 m stations.**

| Chainage (m) | $x$ (m) | Tangent RL $=470.72-0.032x$ | Offset $0.00008333x^2$ | Curve RL (m) |
|---|---|---|---|---|
| 2880 (PVC) | 0 | 470.720 | 0.000 | 470.720 |
| 2910 | 30 | 469.760 | 0.075 | 469.835 |
| 2940 | 60 | 468.800 | 0.300 | 469.100 |
| 2970 | 90 | 467.840 | 0.675 | 468.515 |
| 3000 | 120 | 466.880 | 1.200 | 468.080 |
| 3030 (PVI) | 150 | 465.920 | 1.875 | 467.795 |
| 3060 | 180 | 464.960 | 2.700 | 467.660 |
| 3090 | 210 | 464.000 | 3.675 | 467.675 |
| 3120 | 240 | 463.040 | 4.800 | 467.840 |
| 3150 | 270 | 462.080 | 6.075 | 468.155 |
| 3180 (PVT) | 300 | 461.120 | 7.500 | 468.620 |

(Tangent RL is the first grade line extended; at the PVT the offset is $4e=7.5$ m and brings the level to $461.12+7.50=468.62$ m, the same as RL(PVT) from the second grade.) Station 3072 m is the lowest point, RL 467.648 m.

```figure caption="Question 7: sag vertical curve L = 300 m, g1 = -3.2 %, g2 = +1.8 %, PVI 30+30 (RL 465.92). Low point at chainage 3072, RL 467.648 m."
fig,ax=plt.subplots(figsize=(5.8,2.8))
x=np.linspace(0,300,120); y=470.72-0.032*x+0.05/600*x**2
ax.plot(2880+x,y,color=ACCENT,lw=2.2,label="vertical curve")
ax.plot([2790,3030,3270],[465.92+0.032*240,465.92,465.92+0.018*240],color=MUTED,lw=1,ls="--",label="grade lines")
ax.plot([2880,3180],[470.72,468.62],"o",color="#d9534f",ms=4); ax.text(2880,471.0,"PVC 470.72",fontsize=6.5,ha="center"); ax.text(3180,468.9,"PVT 468.62",fontsize=6.5,ha="center")
ax.plot(3072,467.648,"o",color="#d9534f",ms=4); ax.text(3072,466.9,"low point 3072 / 467.648",fontsize=6.5,ha="center")
ax.plot(3030,465.92,"s",color=INK,ms=4); ax.text(3030,465.2,"PVI 465.92",fontsize=6.5,ha="center")
ax.set_xlabel("Chainage (m)",fontsize=8); ax.set_ylabel("RL (m)",fontsize=8); ax.legend(fontsize=7,loc="upper right"); ax.grid(color=GRID,lw=0.5); ax.set_ylim(464.3,472.4)
```

@s 8
**Relief displacement.** On a vertical photograph the image of a point whose elevation differs from the datum plane (the mean ground, or the nadir plane) is displaced radially from the nadir (principal point): outwards for a point above the datum and inwards for a point below. Let the flying height above the datum be $H$, the top of an object of height $h$ be imaged at radial distance $r$ and its base at $r_0$ ($r-r_0=d$). By similar triangles in the vertical plane through the nadir

$$\begin{gathered}\frac{r}{f}=\frac{R}{H-h} \\ \frac{r_0}{f}=\frac{R}{H}\ \Rightarrow\ d=r-r_0=fR\Big(\frac1{H-h}-\frac1H\Big)=\frac{r\,h}{H}\end{gathered}$$

$$\begin{gathered}\boxed{\,d=\frac{r\,h}{H}\,} \\ h=\frac{d\,H}{r}\end{gathered}$$

where $r$ is the radial distance of the displaced (top) image from the principal point.

- $d$ is **zero at the nadir** and rises in proportion to $r$, so it is largest at the corners of the photograph;
- $d$ increases with the height of the object and decreases with the flying height (high flying and narrow-angle cameras reduce it);
- the displacement is radial from the nadir, so a vertical object appears to **lean** away from the nadir;
- the formula is used to **compute the height of an object** (a tower or a building) from one photograph, and relief displacement gives the **parallax in stereo pairs** that makes the 3D measurement possible; orthorectification removes it.

```figure caption="Question 8: relief displacement of a vertical tower of height h on a photograph taken from height H; d = r h / H, radial from the nadir."
fig,ax=plt.subplots(figsize=(4.8,3.0)); ax.axis("off")
ax.plot([-3,3],[0,0],color="#8a6d3b",lw=2); ax.plot([-3,3],[3.2,3.2],color=MUTED,lw=1)
ax.text(-3,3.35,"photograph plane",fontsize=7,color=MUTED)
ax.plot([0.0,0.0],[6,0],color=MUTED,lw=0.7,ls=":"); ax.plot(0,6,"o",color=INK,ms=5); ax.text(0.15,6.0,"O (lens), H",fontsize=7.5)
ax.plot([1.6,1.6],[0,1.6],color=INK,lw=4); ax.text(1.75,0.6,"tower h",fontsize=7.5)
ax.plot([0,1.6],[6,0],color="#d9534f",lw=1); ax.plot([0,1.6],[6,1.6],color=ACCENT,lw=1)
ax.plot([-0.8,-0.5],[3.2,3.2],"o",color="#d9534f",ms=3)
ax.text(-1.0,3.45,"base",fontsize=6.5,color="#d9534f"); ax.text(-0.4,3.45,"top",fontsize=6.5,color=ACCENT)
ax.annotate("",xy=(-0.9,3.1),xytext=(-0.5,3.1),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(-0.7,2.6,"d",fontsize=8,ha="center")
ax.set_xlim(-3.2,3.2); ax.set_ylim(-0.5,6.6)
```

**Features of drone (UAV) mapping and surveying.**

- **Low-altitude, high-resolution imagery:** flying at 50 to 120 m gives a ground sampling distance of 1 to 5 cm, far finer than satellite or manned aircraft images.
- **Fast and economical** for small and medium areas (some square kilometres per day), repeatable at any time and flexible (the flight can be made below clouds); no pilot's risk and low cost compared with a conventional or total station survey.
- Products: **orthomosaic, digital surface and terrain models, contours, 3D point clouds (SfM photogrammetry or LiDAR) and volumes**; the accuracy is a few centimetres when **ground control points** or RTK/PPK GNSS are used.
- **Access to dangerous or inaccessible** areas (landslides, cliffs, floods, high structures), progress monitoring and inspection.
- Limits: the **battery life** (20 to 40 min), the wind, rain and the **regulation** (CAAN permission, height and line-of-sight limits), the vegetation cover which hides the ground, and the processing time; the accuracy depends on the control.

@s 9
**Principle of GPS.** The GPS fixes the position of the receiver by **three-dimensional trilateration from satellites** (the distances from known satellite positions). Each satellite continuously transmits its position (the ephemeris) and the time of transmission $t_s$ on the L1 (1575.42 MHz), L2 (1227.60 MHz) and L5 carriers. The receiver measures the time of arrival $t_r$, giving the **pseudo-range**

$$\rho_i=c\,(t_r-t_s)=\sqrt{(x_i-x)^2+(y_i-y)^2+(z_i-z)^2}+c\,\delta t$$

where $(x_i,y_i,z_i)$ is the position of satellite $i$, $(x,y,z)$ the unknown position and $\delta t$ the clock error of the receiver (the receiver clock is a cheap quartz clock). There are **four unknowns** ($x,y,z,\delta t$), so **at least four satellites** are required for a 3-D fix; the four non-linear equations are solved iteratively (least squares for more satellites). Carrier-phase measurements, with a base station, give centimetre accuracy.

**Components (segments) of GPS.**

1. **Space segment:** a constellation of at least 24 satellites (now more than 30) in six orbital planes inclined at 55°, at an altitude of about 20 200 km, orbital period about 12 sidereal hours; at least 4 to 8 satellites are visible at any point on the earth. Each carries atomic clocks (caesium and rubidium) and the transmitters.
2. **Control segment:** the **master control station** (Colorado Springs, USA), the monitor stations and the ground antennas around the world. They track the satellites, compute the orbits (the ephemeris) and clock corrections, and upload them to the satellites.
3. **User segment:** the receivers (handheld, geodetic or survey grade, and the integrated phone and car units) with the antenna, the processor and the display, used by the surveyors, the engineers, the navigators and so on.

**Remote sensing in civil engineering** (1 mark). It is applied to *land-use and terrain mapping, route and site selection for roads, dams, canals and pipelines, watershed and flood mapping, landslide and soil studies, monitoring of construction and reservoir siltation and the damage assessment after disasters*.

@s 10
**Use of hydrographic surveying in civil engineering.**

- The **depths and the bed profile** of rivers, lakes, reservoirs and harbours for the design of dams, weirs, intakes, bridge foundations and barrages;
- **capacity and siltation** of reservoirs (repeat surveys), and the **scour** around the piers and the foundations;
- the cross-section and **discharge** of streams (with the velocity), the **flood level** and water level data (gauges);
- **navigation channels, ports, jetties and dredging** quantities, the pipelines and the cables under the water, the location of the underwater obstructions and the **shoreline**, and the tide and the current data.

**Method of sounding.** Sounding is the measurement of the depth of water below the surface at known positions. The depth is reduced to a datum (the chart datum or the reduced level) by the water level read at a gauge at the same time.

1. **Sounding with the lead line or rod (direct method).** A weighted lead (3 to 7 kg) on a marked line is lowered from the boat until it touches the bed, and the depth read at the water surface; in shallow water (to about 5 m) a graduated **sounding rod or pole** is used. It is slow, and is affected by the current (the line drifts and the lead sinks into soft bed).
2. **Echo sounding (the modern method).** The ultrasonic pulse from a **transducer** under the boat travels to the bed and returns; the depth is $D=\tfrac12vt$ ($v\approx1450$ to $1500$ m/s, calibrated by a bar check), plus the transducer draught, and the recorder draws the continuous bed profile. It is quick, gives a continuous profile, and works in deep water.

**Fixing the position of each sounding:** by the *range-and-angle* from the shore (total station or theodolite on the shore, the angle to the boat and the known base), by two *sextant or theodolite angles* to three known shore points (three-point fix), by the *cross-rope* or the *range line* in rivers (the boat run along a rope stretched across the river with the marked distances), or by **DGPS/RTK** on the boat, which is now the usual method.

**Procedure.** Run the sounding lines at a right angle to the river or the shore at a spacing suited to the purpose (5 to 30 m for a river, wider for a deep lake), with a few check lines along the length; fix the position at fixed intervals or by the time marks; read the water level every 15 minutes; reduce the soundings to the datum; plot the points and draw the contours of the bed or the cross-sections.

@s 11
**Linear method of building layout.** The building is set out using **linear (tape or EDM) measurement only** from a **baseline** (a boundary or a road line, or a line parallel to it at the set-back distance).

1. Mark the baseline and fix a reference point on it. Measure along the baseline and offset at a right angle to locate the **first corner** $P$, setting the perpendicular by the **3-4-5 triangle** (or 6-8-10 m, or an optical square).
2. Lay out the front line $PQ$ parallel to the baseline for the building width, and the side line $PS$ perpendicular to it; fix $R$ by the **intersection of two tape arcs** $QR=PS$ and $SR=PQ$.
3. **Check** that the opposite sides are equal and that the **diagonals are equal** ($PR=QS$); the error should be within about 1 in 2000 or a few mm. Fix the corners on the **batter boards** with strings (profile boards 1.5 to 2 m beyond the trench, with the saw cuts or nails for the centre lines and the foundation width).
4. Interior walls and columns are set out from the same boundary lines by the offsets, and the levels from a temporary benchmark.

*Example.* A rectangular house of 12 m by 9 m is placed 4 m behind the road edge and 2 m from the side boundary. From the corner mark of the boundary measure 2 m along the road line, and offset 4 m (3-4-5 triangle, with 6, 8 and 10 m for the right angle). Mark the corner $P$, then $Q$ at 12 m on the line parallel to the road and $S$ at 9 m on the perpendicular, and fix $R$ by the arcs of 9 m from $Q$ and 12 m from $S$; the check $PR=QS=\sqrt{12^2+9^2}=15.00$ m.

**Centre-line transfer in a tunnel.** The tunnel centre line fixed on the surface must be transferred to the tunnel (at the portal and at every shaft), and carried forward as the heading advances.

- **At the portal:** two **reference points (pillars) on the centre line outside the portal**, one on the ridge and one in the rear, are set by the surface traverse or triangulation. The theodolite is set on the rear pillar and sighted on the front one; the line is extended into the tunnel and **centre points are marked on the roof (spads)** every 10 to 20 m, so as to guide the excavation. The levels are transferred from the benchmark outside.
- **Through a shaft (two-plumb-line method):** two heavy **plumb bobs** hang on thin steel wires, 3 to 5 m apart, in the shaft (the bobs steadied in oil or water). The surface traverse fixes the coordinates of the wires, the azimuth of the line joining them being found from the survey. At the bottom the wires are connected with the underground traverse, by a theodolite placed very close to the wire line (the **Weisbach triangle**, with the small angle) and the azimuth is carried on; the centre line is then set out in the heading from these. The azimuth can be checked by the **gyro-theodolite** or by a **laser** pointing along the line.
- **Control in the heading:** the **laser** or the theodolite and the roof marks are advanced as the heading goes forward, and are checked by the traverse; the two headings are checked by the surface and the underground traverse where they meet (the breakthrough).

```figure caption="Question 11: transfer of the centre line through a shaft by two plumb wires W1 and W2; the surface azimuth of W1-W2 is carried to the underground traverse."
fig,ax=plt.subplots(figsize=(4.6,3.0)); ax.axis("off")
ax.plot([0,10],[3.6,3.6],color="#8a6d3b",lw=2); ax.plot([3,3],[3.6,0.6],color="#8a6d3b",lw=2); ax.plot([5,5],[3.6,0.6],color="#8a6d3b",lw=2)
ax.plot([0,3],[0.6,0.6],color="#8a6d3b",lw=2); ax.plot([5,10],[0.6,0.6],color="#8a6d3b",lw=2)
for x_,n in ((3.7,"W1"),(4.3,"W2")): ax.plot([x_,x_],[3.6,0.9],color=INK,lw=1); ax.plot(x_,0.8,"o",color=INK,ms=5); ax.text(x_,3.8,n,fontsize=8,ha="center")
ax.plot([1.0,9.0],[4.3,4.3],color=MUTED,lw=0.8,ls="--"); ax.text(9.0,4.45,"surface traverse / centre line",fontsize=7,ha="right",color=MUTED)
ax.plot([5.3,9.6],[0.62,0.62],color=ACCENT,lw=1.5); ax.text(9.6,1.0,"tunnel centre line",fontsize=7,ha="right",color=ACCENT)
ax.plot(5.6,0.62,"s",color="#d9534f",ms=5); ax.text(5.6,0.15,"theodolite",fontsize=7,ha="center",color="#d9534f")
ax.text(0.2,2.0,"shaft",fontsize=8,color="#8a6d3b"); ax.set_xlim(-0.5,10.2); ax.set_ylim(-0.2,5.0)
```

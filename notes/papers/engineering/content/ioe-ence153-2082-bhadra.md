---
file: NEBians-IOE-Past-Paper-Engineering-Survey-I-ENCE153-2082-Bhadra.pdf
subject: Engineering Survey I
level: BE · Year I / Part II
code: ENCE 153
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course), BE Civil, Year I / Part II. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What is surveying and principle of surveying? Differentiate between plane and geodetic surveying. [[1+1+2]]

@q 2
Explain the types of error in linear distance measurement. In surveying, why is the term precision used more often than accuracy? A rectangular plot of land of area 0.55 hectare is represented on a map of similar rectangle area of 6.11 cm². Calculate the representative fraction of the scale of the map. Draw a diagonal scale to read at least a meter from the map. The scale should be long enough to measure up to 500 m. [Note: - 1 hectare = 10⁴ m², and also show distance of 357 m] [[2+1+5]]

@q 3
Discuss the importance of offsets; list the types. What is the principle of plane table surveying, and what are the advantages over the chain surveying? [[1+1+2]]

@q 4
What is local attraction? Draw sketch only for the graphical adjustment of closing error in compass traverse when closing error is exactly horizontal. In a link traverse ABCDEF the two points A (1000 mE, 2000 mN) and B(2000 mE,1000 mN). The angles to the right at stations are: 125°30' at B, 237°45' at C, 145°15' at D and 55°30' at E. FB of EF = 339°00'20". Check whether the observations for angles are correct or not. If not, compute the correct bearing of all lines. [[3+5]]

@q 5
You are hired to survey a bridge site and you know the RL of one bank of a river and your task is to transfer the RL to another bank. Explain how you can transfer the RL to another bank, and also find the expression for RL. Does any error exist in this method, if exist find the expression for error also. [[4]]

@q 6
The following consecutive readings were taken with a level and 5-metre levelling staff on continuously sloping ground at a common interval of 20 m is 0.385, 1.030, 1.925, 2.52, 1.25, 2.87, 3.66, 4.685, 0.625, 2.005, 3.110 and 4.485 m. The reduced level of the last station was 2208.00 m. Rule out a page of a level field book and enter the above readings. Calculate the reduced levels of the points. Also, find the gradient of the line joining the first and last point. [[5]]

@q 7
In a closed traverse ABCDEA, the following data were provided. Calculate the adjusted RLs of traverse stations. RL of A = 2255.00 m. [[4]]

| Line | Length (km) | Rise (m) | Fall (m) |
|---|---|---|---|
| AB | 1.600 | 3.530 | - |
| BC | 1.000 | 2.150 | - |
| CD | 1.250 | - | 1.050 |
| DE | 1.400 | - | 2.670 |
| EA | 0.800 | - | 2.000 |

@q 8
What is total station and its uses? Describe basic concept of digital data recording in the total station. [[2+2]]

@q 9
Define tacheometry. What is the principle of tacheometry? A staff was held vertically at a distance of 100 m and 300 m from the tacheometer and staff intercepts with the telescope horizontal were 0.995 m and 3.00 m respectively. The instrument was then set over a station P of RL 1950.50 m and height of instrument was 1.42 m. The stadia readings of a staff held vertically at a station Q were 1.00, 1.83, 2.67 m while the vertical angle was −10°00'. Find the distance PQ and RL of PQ. [[2+4]]

@q 10
The following observations were recorded in a theodolite traverse. Complete the average horizontal angle and perform check and correction. Also find missing data in VCR. [[5]]

| Inst. St. | Sighted To | Face | HCR Observation | VCR Observation |
|---|---|---|---|---|
| O | A | L | 00° 00' 00" | 65° 45' 00" |
| | | R | 180° 00' 00" | ? |
| | B | L | 100° 40' 40" | ? |
| | | R | 280° 39' 50" | 268° 55' 00" |
| | C | L | 161° 20' 40" | ? |
| | | R | 341° 20' 20" | 300° 40' 00" |
| | A | L | 00° 00' 10" | |
| | | R | 179° 59' 40" | |

@q 11
Differentiate between the triangulation and trilateration methods of surveying based on their principles. [[4]]

@q 12
Provide the list of available plotting software. What are the advantages of plotting software compared to conventional manual plotting? Is the customized software like SW DTM being better to use? [[4]]

<!-- SOLUTIONS -->

@s 1
**Surveying** is the art and science of determining the relative positions of points on, above or beneath the surface of the earth by measuring distances, angles and directions, and of representing them in the form of a plan or map (or setting them out on the ground).

**Principles of surveying.**

1. **Working from the whole to the part**: control stations are fixed first with the greatest accuracy, and the details are then located within this frame by less accurate methods, so that errors do not accumulate.
2. **Fixing a new point from at least two known points** by two independent measurements (lengths or angles), with a third as a check.

| Plane surveying | Geodetic surveying |
|---|---|
| Curvature of the earth is ignored; the level surface is taken as a plane | The true shape (spheroid) of the earth is considered |
| Area up to about 250 km² | Large areas, above about 250 km² |
| Plane triangles, plane trigonometry | Spherical triangles, spherical excess |
| Ordinary accuracy; chain, compass, theodolite, level, total station | Very high accuracy; precise theodolite, invar tape, EDM, GNSS |
| Used for engineering projects, site and cadastral survey | Used for national control networks and the figure of the earth |

@s 2
**Types of error in linear (tape) measurement.**

- **Mistakes (gross errors):** wrong counting of tape lengths, misreading or misbooking of the figures; they are avoided by measuring twice and by cross-checks.
- **Systematic (cumulative) errors:** keep a fixed sign and sum up with the number of tape lengths: *wrong tape length* (standardisation), *temperature*, *pull (tension)*, *sag*, *slope*, *misalignment*, *tape not horizontal*, *reduction to mean sea level*. The corrections are applied: $C_L=\dfrac{c}{l}L$, $C_t=\alpha(T-T_0)L$, $C_p=\dfrac{(P-P_0)L}{AE}$, $C_s=-\dfrac{w^2L^3}{24P^2}$, $C_h=-\dfrac{h^2}{2L}$.
- **Random (accidental) errors:** small, plus or minus, because of the limits of the human senses (marking the tape ends, reading the tape); they cannot be eliminated but reduce with repeated measurements and the mean.

**Why precision is used more often than accuracy.** *Accuracy* is the closeness of a measurement to the **true value**, but the true value of a measured quantity is *never known*, so the accuracy cannot be computed in practice. *Precision* is the closeness of repeated measurements to each other (or to their mean) and can be computed from the field data themselves, for example the relative precision of a length measured twice is $\dfrac{|L_1-L_2|}{L_{\text{mean}}}=\dfrac1N$, and the standard deviation, so it is what the surveyor can report and check against the specification. (Precision is also needed for accuracy: a precise survey with the systematic errors corrected is accurate.)

**Scale.** $0.55$ ha $=5500$ m² $=5.5\times10^{7}$ cm²; map area $6.11$ cm²:

$$\text{R.F.}=\sqrt{\frac{6.11}{5.5\times10^{7}}}=\sqrt{1.111\times10^{-7}}=3.333\times10^{-4}=\boxed{\frac1{3000}}$$

So 1 cm = 30 m and 500 m $=16.67$ cm. Diagonal scale reading to 1 m: 5 main divisions of $100/30=3.33$ cm (100 m each), the first division on the left of 0 divided into 10 subdivisions (10 m each), 10 horizontal lines and the diagonals joining the top of each subdivision to the bottom of the next one, so each horizontal line is 1 m.

$$357\ \text{m}=300+50+7=3\ \text{main divisions}+5\ \text{subdivisions}+7\ \text{m}$$

```figure caption="Question 2: diagonal scale 1 cm = 30 m (RF 1/3000), 500 m long, reading to 1 m, with 357 m shown. Vertical spacing is not to scale."
fig,ax=plt.subplots(figsize=(6.0,2.9)); ax.axis("off")
H=2.2; n=10
for j in range(n+1): ax.plot([-1,5],[H*j/n]*2,color=INK,lw=0.6)
for m in range(0,6): ax.plot([m,m],[0,H],color=INK,lw=1.0)
for k in range(0,11): ax.plot([-k/10,-k/10],[0,H],color=INK,lw=0.7)
for k in range(1,11): ax.plot([-(k-1)/10,-k/10],[H,0],color=ACCENT,lw=0.8)
for m in range(0,6): ax.text(m,-0.15,str(100*m),ha="center",va="top",fontsize=7)
for k in range(1,11): ax.text(-k/10,H+0.07,str(10*k),ha="center",va="bottom",fontsize=5.5,color=ACCENT)
for j in range(0,n+1,2): ax.text(5.1,H*j/n,str(j),va="center",fontsize=6)
ax.text(2,-0.5,"metres (main divisions 100 m; left subdivisions 10 m; horizontal lines 1 m)",ha="center",fontsize=7)
m,k,j=3,6,3; x=-(k-1)/10-(10-j)/100; y=H*j/10
ax.plot([x,m],[y,y],color="#d9534f",lw=2.4); ax.plot([x,m],[y,y],"o",color="#d9534f",ms=4); ax.text((x+m)/2,y+0.08,"357 m",color="#d9534f",fontsize=8,ha="center")
ax.set_xlim(-1.2,5.5); ax.set_ylim(-0.8,H+0.55)
```

@s 3
**Importance of offsets.** In a chain survey the chain lines form the skeleton, and the details (buildings, boundaries, roads, streams, trees) are located by measuring their lateral distances (offsets) from the chain lines. Offsets are therefore the only way by which the details are fixed and plotted, and their accuracy decides the accuracy of the plan.

**Types.** (i) **Perpendicular offsets**, set out at $90^\circ$ with the cross staff, optical square or the 3-4-5 tape method; (ii) **oblique offsets**, measured at any angle by the tie-line method from two points of the chain line, when a perpendicular cannot be set. They are classified also as *short* (up to about 15 m) and *long* offsets.

**Principle of plane table survey.** *Parallelism*: the table is oriented at every station so that the rays on the sheet are always parallel to the corresponding lines on the ground; the field work and plotting go together, by radiation, intersection, traversing or resection.

**Advantages over chain survey:** (1) the map is plotted in the field, so omissions and mistakes are seen and corrected at once, and no field book or later plotting is needed; (2) only a few measurements are needed (the angles are drawn with the alidade, not measured), saving time; (3) irregular details, contours and the terrain relief can be drawn by direct inspection; (4) it can be used where a chain cannot be used (obstacles, rolling ground, large open areas); (5) the check of the work is by resection and the closing of the traverse.

@s 4
**Local attraction.** The deflection of a magnetic needle from the magnetic meridian caused by magnetic substances near it (steel structures, iron ore, electric cables, pipelines, keys, steel tapes, the chain and arrows). It makes the F.B. and B.B. of the line differ from exactly $180^\circ$, and is detected by $\text{F.B.}-\text{B.B.}\neq180^\circ$, and corrected by the included-angle method or by the bearing of a line that is free from attraction.

**Graphical adjustment of the closing error (Bowditch's rule, error exactly horizontal).** The traverse is plotted ABCDE with the end falling at E', away from A by the closing error $EE'$. A horizontal base line is drawn with the length of the perimeter at the scale, with the stations marked at their cumulative distances; the closing error is drawn vertically, to scale, at the last station and joined to the first station by a straight line. Each station of the traverse is moved parallel to the closing line, by the length intercepted by the sloping line at the ordinate of that station.

```figure caption="Question 4(a): graphical adjustment of a horizontal closing error. Left: traverse A-B-C-D-E' with closing error E'A horizontal; each station is shifted parallel to the error by the intercept in the diagram on the right."
fig,(a,b)=plt.subplots(1,2,figsize=(6.4,2.4))
for ax in (a,b): ax.axis("off")
P=np.array([[0,0],[1.2,1.8],[3.2,2.4],[4.4,0.9],[4.9,0.0]])
a.plot(P[:,0],P[:,1],"-o",color=INK,ms=3,lw=1.3)
for p,l in zip(P,["A","B","C","D","E'"]): a.text(p[0]+0.08,p[1]+0.1,l,fontsize=8)
a.plot([0,4.9],[0,0],color="#d9534f",lw=2,ls="--"); a.text(2.4,-0.4,"closing error (horizontal)",fontsize=7,ha="center",color="#d9534f")
d=np.array([0,1.2,2.8,3.9,4.9]); e=0.7
Q=P.copy(); Q[:,0]=Q[:,0]-e*d/d[-1]
a.plot(Q[:,0],Q[:,1],"-o",color=ACCENT,ms=3,lw=1.2); a.set_xlim(-0.5,5.5); a.set_ylim(-0.9,3.0)
L=np.array([0,1.5,3.2,4.4,5.5]); b.plot([0,5.5],[0,0],color=INK,lw=1.3); b.plot([5.5,5.5],[0,0.9],color="#d9534f",lw=2); b.plot([0,5.5],[0,0.9],color=ACCENT,lw=1.4)
for x,l in zip(L,["A","B","C","D","E"]): b.plot([x,x],[0,0.9*x/5.5],color="#888",lw=0.8); b.text(x,-0.25,l,ha="center",fontsize=8)
b.text(2.7,-0.6,"base = perimeter, ordinate = closing error",fontsize=7,ha="center"); b.set_xlim(-0.4,6.0); b.set_ylim(-0.9,1.4)
plt.tight_layout()
```

**Link traverse.** Bearing of AB from the coordinates: $\Delta E=2000-1000=+1000$ m, $\Delta N=1000-2000=-1000$ m, so the line AB points south-east:

$$\theta_{AB}=\tan^{-1}\frac{1000}{-1000}=135^\circ00'$$

With the angles to the right, $\theta_{\text{next}}=\theta_{\text{prev}}+180^\circ+\beta$ (subtract $360^\circ$ if over $360^\circ$):

$$\begin{gathered}\theta_{BC}=135^\circ00'+180^\circ+125^\circ30'-360^\circ=80^\circ30'\\ \theta_{CD}=80^\circ30'+180^\circ+237^\circ45'-360^\circ=138^\circ15'\\ \theta_{DE}=138^\circ15'+180^\circ+145^\circ15'-360^\circ=103^\circ30'\\ \theta_{EF}=103^\circ30'+180^\circ+55^\circ30'-360^\circ=339^\circ00'\end{gathered}$$

The known bearing of EF is $339^\circ00'20''$, so the computed bearing is $20''$ short. **The observations are not exactly correct**, but the error of $20''$ is small, much below the permissible $1'\sqrt n=1'\sqrt4=2'$ (or $30''\sqrt n$), so the observations are acceptable and the error is distributed equally among the four angles: correction $+20''/4=+5''$ at each station.

| Station | Observed angle | Corrected angle |
|---|---|---|
| B | 125° 30' 00" | 125° 30' 05" |
| C | 237° 45' 00" | 237° 45' 05" |
| D | 145° 15' 00" | 145° 15' 05" |
| E | 55° 30' 00" | 55° 30' 05" |

**Corrected bearings.**

$$\begin{gathered}\theta_{AB}=135^\circ00'00''\\ \theta_{BC}=135^\circ00'00''+180^\circ+125^\circ30'05''-360^\circ=80^\circ30'05''\\ \theta_{CD}=80^\circ30'05''+180^\circ+237^\circ45'05''-360^\circ=138^\circ15'10''\\ \theta_{DE}=138^\circ15'10''+180^\circ+145^\circ15'05''-360^\circ=103^\circ30'15''\\ \theta_{EF}=103^\circ30'15''+180^\circ+55^\circ30'05''-360^\circ=339^\circ00'20''\ \checkmark\end{gathered}$$

| Line | Corrected bearing (F.B.) | Back bearing |
|---|---|---|
| AB | 135° 00' 00" | 315° 00' 00" |
| BC | 80° 30' 05" | 260° 30' 05" |
| CD | 138° 15' 10" | 318° 15' 10" |
| DE | 103° 30' 15" | 283° 30' 15" |
| EF | 339° 00' 20" | 159° 00' 20" |

@s 5
**Transfer of RL across the river: reciprocal levelling.** Direct levelling with the level at the middle is not possible because the sights across the river are long and unequal, so the collimation error, the earth's curvature and the refraction do not cancel. *Reciprocal levelling* is used:

1. Set up the level at a point $X$ very near bank A (the known RL) and take the staff reading $a_1$ on A (near, nearly free from error) and $b_1$ on B on the opposite bank (far, with the error).
2. Without changing the staff, move the level to a point $Y$ near bank B, take $b_2$ on B (near) and $a_2$ on A (far).
3. Use the same instrument, with the same bubble care, and (ideally) make the observations at the same time, so that the atmospheric conditions are the same.

**Expression for RL.** The true difference of level of B above A is the mean of the two apparent differences:

$$\begin{gathered}H=\frac{(a_1-b_1)+(a_2-b_2)}{2} \\ RL_B=RL_A+\frac{(a_1-b_1)+(a_2-b_2)}{2}\end{gathered}$$

**Error.** Let $e$ be the combined error in the far reading (collimation error of the line of sight + curvature − refraction, proportional to the distance and the same in both set-ups). The apparent differences are $h_1=a_1-b_1=H-e$ (far reading on B, too high by $e$) and $h_2=a_2-b_2=H+e$ (far reading on A, too high by $e$). Therefore

$$e=\frac{(a_2-b_2)-(a_1-b_1)}{2}$$

(For example, with $a_1=1.524$, $b_1=1.288$ and $a_2=1.876$, $b_2=1.600$: $h_1=0.236$, $h_2=0.276$, $H=0.256$ m and $e=0.020$ m.) **Does any error exist?** Yes: the instrumental (collimation) error, curvature and mean refraction cancel in the mean, but the variation of refraction between the two set-ups (when they are not simultaneous), changes of the instrument over time, the staff-reading errors at long range and errors in setting the bubble remain. They are reduced by taking several sets, simultaneous observations with two levels, and by using a target or a staff with a vane.

```figure caption="Question 5: reciprocal levelling across a river. Set-up 1 near A (readings a1, b1); set-up 2 near B (readings a2, b2); H = [(a1 - b1) + (a2 - b2)] / 2."
fig,(a,b)=plt.subplots(1,2,figsize=(6.4,2.2))
for ax in (a,b):
    ax.axis("off"); ax.fill_between([3.5,6.5],[-0.6,-0.6],[0,0],color="#cfe3f5"); ax.plot([0,3.5],[0,0],color="#8a6d3b",lw=2); ax.plot([6.5,10],[0,0],color="#8a6d3b",lw=2)
    ax.plot([1.0,1.0],[0,2.3],color=INK,lw=3); ax.plot([9.0,9.0],[0,2.3],color=INK,lw=3)
    ax.text(1.0,-0.45,"A",ha="center",fontsize=9); ax.text(9.0,-0.45,"B",ha="center",fontsize=9); ax.set_xlim(-0.4,10.6); ax.set_ylim(-0.8,3.1)
a.plot(0.1,0.4,"^",color=INK,ms=7); a.plot([0.1,1.0],[0.8,0.8],color=ACCENT,lw=1.1,ls="--"); a.plot([0.1,9.0],[0.8,1.4],color=ACCENT,lw=1.1,ls="--"); a.text(1.1,0.9,"a1",fontsize=8); a.text(9.1,1.5,"b1",fontsize=8); a.set_title("set-up 1 (near A)",fontsize=7.5)
b.plot(9.9,0.4,"^",color=INK,ms=7); b.plot([9.0,9.9],[0.8,0.8],color=ACCENT,lw=1.1,ls="--"); b.plot([1.0,9.9],[1.4,0.8],color=ACCENT,lw=1.1,ls="--"); b.text(1.1,1.5,"a2",fontsize=8); b.text(8.2,0.95,"b2",fontsize=8); b.set_title("set-up 2 (near B)",fontsize=7.5)
plt.tight_layout()
```

@s 6
**Level book (rise and fall / HI).** Because the staff is 5 m long and the ground slopes continuously down, the readings increase until they approach the length of the staff, then the instrument has to be moved: after the 4th reading (2.52 to 1.25) and the 8th reading (4.685 to 0.625). So: set-up 1: BS 0.385, IS 1.030, IS 1.925, FS 2.52; set-up 2: BS 1.25, IS 2.87, IS 3.66, FS 4.685; set-up 3: BS 0.625, IS 2.005, IS 3.110, FS 4.485 (last point, RL 2208.000). The RLs are therefore worked **backwards from the last station**: $RL_{\text{before}}=RL_{\text{next}}+(\text{next reading}-\text{previous reading})$ within a set-up (the ground falls with increasing reading).

| Station | Chainage (m) | BS | IS | FS | Rise | Fall | RL (m) | Remark |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0.385 | | | | | 2217.430 | first point |
| 2 | 20 | | 1.030 | | | 0.645 | 2216.785 | |
| 3 | 40 | | 1.925 | | | 0.895 | 2215.890 | |
| 4 | 60 | | | 2.520 | | 0.595 | 2215.295 | CP |
| 4 | 60 | 1.250 | | | | | 2215.295 | CP |
| 5 | 80 | | 2.870 | | | 1.620 | 2213.675 | |
| 6 | 100 | | 3.660 | | | 0.790 | 2212.885 | |
| 7 | 120 | | | 4.685 | | 1.025 | 2211.860 | CP |
| 7 | 120 | 0.625 | | | | | 2211.860 | CP |
| 8 | 140 | | 2.005 | | | 1.380 | 2210.480 | |
| 9 | 160 | | 3.110 | | | 1.105 | 2209.375 | |
| 10 | 180 | | | 4.485 | | 1.375 | 2208.000 | last point (given) |
| Sum | | 2.260 | | 11.690 | 0.000 | 9.430 | | |

**Check.**

$$\begin{gathered}\Sigma BS-\Sigma FS=2.260-11.690=-9.430 \\ \Sigma\text{Rise}-\Sigma\text{Fall}=0-9.430=-9.430 \\ RL_{\text{last}}-RL_{\text{first}}=2208.000-2217.430=-9.430\ \checkmark\end{gathered}$$

**Gradient of the first to the last point** (nine intervals, $9\times20=180$ m):

$$\text{gradient}=\frac{9.430}{180}=\frac1{19.1}=\boxed{1\text{ in }19.1\ \text{falling}\ (5.24\%)}$$

@s 7
Sum of rises $=3.530+2.150=5.680$ m; sum of falls $=1.050+2.670+2.000=5.720$ m. For a closed traverse the sum must be zero:

$$\text{misclosure}=5.680-5.720=-0.040\ \text{m}$$

Total length $=1.6+1.0+1.25+1.4+0.8=6.05$ km. The correction $+0.040$ m is distributed in proportion to the length, $c=+0.040\dfrac{L}{6.05}$:

| Line | L (km) | Rise (+) / Fall (−) (m) | Correction (m) | Corrected (m) | Station | Adjusted RL (m) |
|---|---|---|---|---|---|---|
| | | | | | A | 2255.000 |
| AB | 1.600 | +3.530 | +0.0106 | +3.5406 | B | 2258.541 |
| BC | 1.000 | +2.150 | +0.0066 | +2.1566 | C | 2260.697 |
| CD | 1.250 | −1.050 | +0.0083 | −1.0417 | D | 2259.656 |
| DE | 1.400 | −2.670 | +0.0093 | −2.6607 | E | 2256.995 |
| EA | 0.800 | −2.000 | +0.0053 | −1.9947 | A | 2255.000 ✓ |

$$\boxed{RL_B=2258.541,\ RL_C=2260.697,\ RL_D=2259.656,\ RL_E=2256.995\ \text{m}}$$

The misclosure of 40 mm is within the allowable $\pm24\sqrt{6.05}=\pm59$ mm (third order), so the work is accepted.

@s 8
**Total station.** An electro-optical instrument that combines an electronic theodolite (horizontal and vertical angles), an EDM (slope distance) and a microprocessor with memory in one unit, so that angles and distance are measured together and the horizontal distance, vertical difference, and the coordinates $(N,E,Z)$ of the target are computed and stored.

**Uses:** topographic and detailed surveys; traversing and control; setting out of buildings, roads, bridges and tunnels; deformation monitoring; volume and area computation; as-built and cadastral surveys; resection and remote elevation measurement; mine, construction and industrial surveys, and direct download of the data for plotting in CAD or DTM software.

**Basic concept of digital data recording.** The data are recorded **electronically in the instrument** (or in a data collector) and not by hand in a field book:

1. A **job** is created. The occupied station (coordinates, instrument height $h_i$) and the back-sight (orientation, by a coordinate or azimuth) are entered; the circle is set to the azimuth of the back-sight, and the target height $h_t$ is entered.
2. For each observed point the operator keys a **point number** and **feature code**, and presses *measure*: the HA, VA and slope distance are recorded as raw data, and the coordinates are computed:

$$N=N_O+D\cos\theta,\quad E=E_O+D\sin\theta,\quad Z=Z_O+h_i+V-h_t$$

3. The records are stored in the memory and later *downloaded* (cable, Bluetooth, USB or card) to the computer for adjustment and plotting; because the data are never hand-copied, booking errors are avoided. The back-sight check on a known point at the end of the set-up controls the quality.

@s 9
**Tacheometry** is a method of rapid surveying in which the horizontal distance and the difference of elevation of a point are determined from *angular and staff observations of a theodolite fitted with stadia hairs* (a tacheometer), without chaining or levelling.

**Principle.** The stadia hairs make a fixed small angle; the staff intercept $s$ between the upper and lower hairs is proportional to the distance of the staff from the instrument: $D=ks+C$ ($k=f/i$, $C=f+d$). For an inclined sight at angle $\alpha$ with a vertical staff:

$$\begin{gathered}D=ks\cos^2\alpha+C\cos\alpha \\ V=\tfrac12ks\sin2\alpha+C\sin\alpha\end{gathered}$$

**Instrument constants.** For the horizontal sights, $D=ks+C$:

$$100=0.995k+C,\quad300=3.000k+C\ \Rightarrow\ k=\frac{200}{2.005}=99.75,\quad C=100-99.75(0.995)=0.748\ \text{m}$$

**Staff at Q.** $s=2.67-1.00=1.67$ m, $\alpha=-10^\circ00'$ (depression):

$$PQ=D=99.75(1.67)\cos^210^\circ+0.748\cos10^\circ=161.55+0.74=\boxed{162.30\ \text{m}}$$

$$V=\tfrac12(99.75)(1.67)\sin20^\circ+0.748\sin10^\circ=28.49+0.13=28.62\ \text{m}\ (\text{below the axis})$$

$$\begin{gathered}RL_{\text{axis}}=1950.50+1.42=1951.92\ \text{m} \\ RL_Q=1951.92-28.62-1.83=\boxed{1921.47\ \text{m}}\end{gathered}$$

(The central hair reading 1.83 is the mean of 1.00 and 2.67 within rounding. With $k=100$ and $C=0$ the result is $D=161.96$ m and $RL_Q=1921.53$ m.)

@s 10
**Horizontal angles.** The angles are the differences of the successive pointings, the line of sight returning to A at the end:

| Angle | Face left | Face right | Mean |
|---|---|---|---|
| AOB | 100°40'40" − 0°00'00" = 100° 40' 40" | 280°39'50" − 180°00'00" = 100° 39' 50" | 100° 40' 15" |
| BOC | 161°20'40" − 100°40'40" = 60° 40' 00" | 341°20'20" − 280°39'50" = 60° 40' 30" | 60° 40' 15" |
| COA | 360°00'10" − 161°20'40" = 198° 39' 30" | 539°59'40" − 341°20'20" = 198° 39' 20" | 198° 39' 25" |

**Check.** The sum of the angles round the point must be $360^\circ$:

$$100^\circ40'15''+60^\circ40'15''+198^\circ39'25''=359^\circ59'55''$$

so the error is $-5''$ (very small; the face readings on A also show a closing difference of $10''$ on the left and $-20''$ on the right). It is distributed equally, $+5''/3=+1.67''$ each:

$$\boxed{\angle AOB=100^\circ40'16.7'',\quad\angle BOC=60^\circ40'16.7'',\quad\angle COA=198^\circ39'26.7''}$$

(sum $=360^\circ00'00''$.)

**Missing VCR data.** For a vertical circle reading zenith angles, the face-left and face-right readings of the same target add up to $360^\circ$ when there is no index error:

$$\begin{gathered}A_R=360^\circ-65^\circ45'00''=294^\circ15'00''\\ B_L=360^\circ-268^\circ55'00''=91^\circ05'00''\\ C_L=360^\circ-300^\circ40'00''=59^\circ20'00''\end{gathered}$$

| Target | Face | HCR | VCR (zenith) | Mean zenith angle $Z=\tfrac12(L-R+360^\circ)$ | Vertical angle $90^\circ-Z$ |
|---|---|---|---|---|---|
| A | L / R | 0°00'00" / 180°00'00" | 65°45'00" / **294°15'00"** | 65° 45' 00" | +24° 15' 00" |
| B | L / R | 100°40'40" / 280°39'50" | **91°05'00"** / 268°55'00" | 91° 05' 00" | −1° 05' 00" |
| C | L / R | 161°20'40" / 341°20'20" | **59°20'00"** / 300°40'00" | 59° 20' 00" | +30° 40' 00" |

The sums are $360^\circ00'00''$ for all the three targets, so the index error is zero.

@s 11
| | Triangulation | Trilateration |
|---|---|---|
| **Principle** | The network is made of triangles; one **base line** is measured accurately and *all the angles* are measured. The sides follow from the **sine rule** and the coordinates from the azimuth of one side | The same network, but *all the sides* are measured with EDM (or total station); the angles are *computed* with the **cosine rule** |
| Equations | $b=a\dfrac{\sin B}{\sin A}$ | $\cos A=\dfrac{b^2+c^2-a^2}{2bc}$ |
| Measurements | Angles (theodolite), one base and a check base | Distances (EDM, total station, GNSS) |
| Check | Sum of the angles of a triangle $=180^\circ$ (plus the spherical excess), check base | Closing of the figure and the redundant sides (adjustment by least squares) |
| Base line | A long, level, carefully measured base and its extension are needed | No base line extension needed |
| Suitability | Old and long lines of sight with fewer, slower observations | Fast with modern EDM, good in hills and for dense networks; often combined with triangulation (*triangulateration*) |

**Principle in short:** triangulation fixes the shape and size of the network through the **angles** and one length, while trilateration fixes it through the **lengths** only. A triangle is rigid when either its three angles and one side, or its three sides, are known.

@s 12
**Available plotting (mapping) software:** AutoCAD and AutoCAD Civil 3D, Bentley MicroStation and OpenRoads, SurvCADD, Leica Infinity, Trimble Business Center, Carlson Survey, 12d Model, Surfer, Global Mapper, ArcGIS, and the free and open-source **QGIS**, GRASS GIS and LibreCAD.

**Advantages over manual plotting.**

- Points are plotted from coordinates (imported from a total station or GNSS file), with no scaling or protractor error; accuracy is that of the coordinates (mm), and not 0.2 mm on paper.
- Fast; any scale, sheet size or projection from one database; the plan is easy to edit and revise (layers, undo), and is stored, copied and shared without deformation of paper.
- Automatic contours, TIN surface, profiles and cross-sections, area and volume, and setting-out data for the stakeout.
- Consistent symbols, text and standards; export to CAD, GIS and printing.

**Is customised software like SW DTM better?** Yes, for the survey and engineering design work: a customised DTM package is built for *survey data*, with direct import of the total-station formats, the traverse adjustment, the TIN and contour generation, longitudinal and cross-section, the earthwork volume, and the road, canal and drainage design templates. A generic CAD program needs manual work and add-ons for the same. Its limits are the licence cost and the training; where the cost matters, a free tool such as QGIS with the survey plugins can do most of the work.

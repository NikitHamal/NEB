---
file: NEBians-IOE-Past-Paper-Engineering-Survey-I-CE153-2081-Ashwin.pdf
subject: Engineering Survey I
level: BE · Year I / Part II
code: CE 153
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch), BE Civil, Year I / Part II. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define surveying. List the principle of surveying in chronological order. Explain any two with suitable examples. [[1+1+2]]

b) What are the factors affecting the selection of scale. Describe the types of errors. [[2+2]]

c) A rectangular plot of land of area 0.96 hectare is represented on map of similar rectangle area of 6 cm². Calculate the R.F. of scale of the map. Draw a scale to read up to a meter from a map. The map should be long enough to measure up to 500m. Also show distance of 369 m. [[4]]

@q 2
a) What is principle of Chain survey and Plane table survey? Also write down advantages and disadvantages of Plane table survey. [[1+1+2]]

b) Define bearing and meridians. [[1+1]]

c) The following bearing was observed in the compass traverse [[6]]

| Lines | AB | BC | CD | DE | EA |
|---|---|---|---|---|---|
| FB | 188°45' | 119°15' | 346°30' | 337°00' | 293°30' |
| BB | 7°45' | 298°15' | 168°30' | 158°30' | 113°00' |

At which stations do you suspect local attraction? Find the correct bearing of the lines by included angle method.

@q 3
a) What are the points to be considered while doing fly levelling? If RL of one TBM is known give the example to calculate RL of another TMB at k loop distance in km. [[3+1]]

b) Explain the Longitudinal and cross section levelling with sketch. [[3]]

c) The consecutive readings taken during a levelling operation at 20 m intervals are as follows: 0.685, 1.315, 1.825, 0.635, 1.205, 1.235, 2.631, 1.355 and 2.015 m. The instrument was shifted after third and sixth readings. The third reading was taken to a BM of assumed elevation 1580.000 m. Find the reduced level of points using Rise and fall method. Find the gradient from first to last stations. Apply check. [[5]]

@q 4
a) What are the features of Total Station? List and explain briefly. [[4]]

b) What is tangential tacheometry? Explain the cases with sketch. [[3]]

c) Calculate the mean horizontal angle <AOB, <BOC and <COA from the following observation. [[5]]

| Instrument station | Sighted to | Face Left | Face Right |
|---|---|---|---|
| O | A | 00°10'30" | 180°50'30" |
| | B | 150°35'20" | 330°15'20" |
| | C | 240°20'30" | 60°25'40" |
| | A | 0°05'40" | 180°10'40" |

@q 5
a) What is triangulation? Write down norms and specification of Third Order Triangulation. [[1+3]]

b) Differentiate between manual plotting and computer aided plotting. [[4]]

c) Following observations were made in a tacheometric survey a station A of RL 1085.550, the height of instrument being 1.385 m. [[4]]

| Inst Station | HI | Staff Station | Azimuth | Zenithal angle | Staff Reading |
|---|---|---|---|---|---|
| A | 1.385 | B | 18°00' | 71°30' | 1.295, 1.820, 2.345 |
| | | C | 127°00' | 96°00' | 1.010, 1.790, 2.570 |

The instrument is fitted with an anallactic lens and the multiplying constants is 100. Determine the RL of B and C and the gradient of line BC.

<!-- SOLUTIONS -->

@s 1
**(a) Surveying** is the art and science of determining the relative positions of points on, above or beneath the earth's surface by measuring horizontal and vertical distances, angles and directions, and of representing them on a plan or map (or setting them out on the ground).

**Principles (in the order they are applied).**

1. **Work from the whole to the part:** a framework of control stations is fixed first with high accuracy and the detail is fixed inside it by less accurate methods.
2. **Fix a point by at least two independent measurements** from points already fixed, with a third as a check.

*Explanation with examples.* (1) In a large site survey, a main traverse of 4 or 5 stations is run with the theodolite and closed to a $1/5000$ precision; the buildings and boundary details are then fixed from the traverse stations by tape offsets. A small error in a detail measurement then remains local and does not spread to the whole survey. (2) A new station P is fixed from the stations A and B of known coordinates by measuring the two lengths AP and BP (linear intersection) or the angles at A and B (angular intersection); a third measurement from C is used as a check.

**(b) Factors affecting the selection of scale:** the *purpose* of the map (design maps need a large scale, reconnaissance maps a small scale); the *size and shape of the area* and the size of drawing sheet; the *amount of detail* required, bearing in mind that $0.25$ mm is the smallest line the eye can plot (graphical accuracy) and so a ground detail of 0.25 mm × the scale denominator can be shown; the *accuracy* of the field work; and the cost, time and the available instruments.

**Types of errors.**

- **Mistakes (blunders, gross errors):** careless reading, booking, counting of tape lengths, or plotting; removed by checks and repeated measurements.
- **Systematic (cumulative) errors:** follow a physical law and keep the same sign: *instrumental* (a tape that is too short, collimation error), *natural* (temperature, sag, refraction, curvature), *personal* (a bias in reading). Removed by applying corrections.
- **Random (accidental) errors:** small, positive or negative, obey the law of probability; they cannot be eliminated but are reduced by repeated measurements and the mean (adjusted by least squares).

**(c) Scale.** Plot area $0.96$ ha $=9600$ m² $=9.6\times10^{7}$ cm²; map area $6$ cm²:

$$\text{R.F.}=\sqrt{\frac{6}{9.6\times10^{7}}}=\sqrt{6.25\times10^{-8}}=2.5\times10^{-4}=\boxed{\frac1{4000}}$$

So 1 cm = 40 m, and 500 m $=12.5$ cm. Diagonal scale (reading to 1 m): 5 main divisions of 2.5 cm (100 m each), the first division on the left of 0 divided into 10 subdivisions (10 m each), 10 horizontals and the diagonals joining the top of one subdivision to the bottom of the next. Each horizontal line is then 1 m.

$$369\ \text{m}=300+60+9=3\ \text{main divisions}+6\ \text{subdivisions}+9\ \text{m}$$

```figure caption="Question 1(c): diagonal scale 1 cm = 40 m (RF 1/4000), 500 m long, reading to 1 m, with 369 m shown. Vertical spacing is not to scale."
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
m,k,j=3,7,1; x=-(k-1)/10-(10-j)/100; y=H*j/10
ax.plot([x,m],[y,y],color="#d9534f",lw=2.4); ax.plot([x,m],[y,y],"o",color="#d9534f",ms=4); ax.text((x+m)/2,y+0.08,"369 m",color="#d9534f",fontsize=8,ha="center")
ax.set_xlim(-1.2,5.5); ax.set_ylim(-0.8,H+0.55)
```

@s 2
**(a) Principle of chain survey.** The area is divided into a network of well-conditioned triangles (no angle below $30^\circ$ nor above $120^\circ$), and only *lengths* are measured, because a triangle is fixed uniquely by its three sides; details are located by offsets from the chain lines, with check lines.

**Principle of plane table survey.** *Parallelism*: the table is oriented at each station so that all rays drawn on the sheet are parallel to the corresponding ground lines; the survey and plotting are done at the same time in the field (radiation, intersection, traversing, resection).

| Advantages of plane table survey | Disadvantages of plane table survey |
|---|---|
| Plan is drawn in the field, so details cannot be missed or wrongly plotted | Needs fair weather; not suitable in rain, wind or dense forest |
| No field book, no transcription errors | Less accurate than a theodolite survey; the sheet shrinks or swells |
| Check by resection and the three-point problem; can fix irregular details by sketching | Heavy equipment and a lot of carrying; difficult to use in crowded areas |
| Rapid for small and medium-size topographic and detail maps | Plan is not easy to redraw to another scale; no record of the field measurements |

**(b) Bearing.** The *bearing* of a line is its horizontal direction relative to a meridian: the angle measured clockwise from the north end of the meridian to the line (whole circle bearing, $0^\circ$ to $360^\circ$), or the acute angle from the nearest N or S end (quadrantal bearing).

**Meridian.** The fixed reference direction from which the bearings are reckoned: **true meridian** (the great circle through the geographic poles, from astronomical observation), **magnetic meridian** (the direction of a freely suspended magnetic needle), **grid meridian** (a line parallel to the central meridian of the map projection), and an **arbitrary meridian** (any assumed direction, such as the first line of a small survey).

**(c) Local attraction.** For a line free from attraction at both ends, $\text{F.B.}-\text{B.B.}=180^\circ$:

| Line | F.B. − B.B. | Difference from 180° |
|---|---|---|
| AB | 181° 00' | +1° 00' |
| BC | 181° 00' | +1° 00' |
| CD | 178° 00' | −2° 00' |
| DE | 178° 30' | −1° 30' |
| EA | 180° 30' | +0° 30' |

*No line has the exact difference of 180°*, so all the stations are suspected of local attraction, the CD, DE, AB and BC lines most (1° to 2°), and the line EA is the least disturbed ($30'$, which is the same as the likely observation error).

**Included-angle method.** The traverse runs clockwise, so the interior angle is on the right, $\alpha=\text{F.B.}_{\text{next}}-\text{B.B.}_{\text{previous}}$ (the angle between two lines at the same station is not changed by the attraction at that station):

$$\begin{gathered}\angle A=188^\circ45'-113^\circ00'=75^\circ45'\\ \angle B=119^\circ15'-7^\circ45'=111^\circ30'\\ \angle C=346^\circ30'-298^\circ15'=48^\circ15'\\ \angle D=337^\circ00'-168^\circ30'=168^\circ30'\\ \angle E=293^\circ30'-158^\circ30'=135^\circ00'\end{gathered}$$

Sum $=539^\circ00'$; the required sum is $(2n-4)\times90^\circ=540^\circ$, so the error is $-1^\circ00'$. The correction $+60'/5=+12'$ per angle:

| Station | Observed angle | Corrected angle |
|---|---|---|
| A | 75° 45' | 75° 57' |
| B | 111° 30' | 111° 42' |
| C | 48° 15' | 48° 27' |
| D | 168° 30' | 168° 42' |
| E | 135° 00' | 135° 12' |
| Sum | 539° 00' | 540° 00' |

**Corrected bearings.** The least-disturbed line EA ($293^\circ30'$) is adopted as correct, and for a clockwise traverse $\theta_{\text{next}}=\theta_{\text{prev}}-180^\circ+\alpha$:

$$\begin{gathered}\theta_{AB}=293^\circ30'-180^\circ+75^\circ57'=189^\circ27'\\ \theta_{BC}=189^\circ27'-180^\circ+111^\circ42'=121^\circ09'\\ \theta_{CD}=121^\circ09'-180^\circ+48^\circ27'=349^\circ36'\\ \theta_{DE}=349^\circ36'-180^\circ+168^\circ42'=338^\circ18'\\ \theta_{EA}=338^\circ18'-180^\circ+135^\circ12'=293^\circ30'\ \checkmark\end{gathered}$$

| Line | Corrected F.B. | Corrected B.B. |
|---|---|---|
| AB | 189° 27' | 9° 27' |
| BC | 121° 09' | 301° 09' |
| CD | 349° 36' | 169° 36' |
| DE | 338° 18' | 158° 18' |
| EA | 293° 30' | 113° 30' |

@s 3
**(a) Points to consider in fly levelling.** Fly levelling is differential levelling run quickly between two benchmarks (to carry or check an RL):

- Keep the **back-sight and fore-sight distances equal** at every set-up (this cancels the collimation, curvature and refraction errors); keep the sights short (not above about 60 m to 100 m) and use the fewest possible set-ups.
- Use firm **change points** (pegs, stones, or a foot plate), and do not move the staff until the fore-sight on it has been taken and the instrument has been shifted and the back-sight taken.
- Keep the staff **vertical** (use a staff bubble), read the three hairs or check the central hair against the mean, and avoid readings near the ground (refraction) and the staff top.
- Test the instrument (two peg test) before the work, **check** the work by closing the line on the start or on another BM, and keep the allowable error within $\pm C\sqrt{k}$ (mm), $k$ in km.
- Record the levels carefully in the level book and carry out the arithmetic checks.

**Example (RL of another TBM at a distance $k$).** TBM1 has an RL of 1500.000 m. A fly levelling line run to TBM2, $k=2.4$ km away, gives $\Sigma BS=9.215$ m and $\Sigma FS=8.540$ m:

$$RL_{TBM2}=RL_{TBM1}+\Sigma BS-\Sigma FS=1500.000+9.215-8.540=1500.675\ \text{m}$$

If the levelling is repeated back to TBM1 with a misclosure of $+0.021$ m, the allowable error for ordinary levelling is $\pm24\sqrt{k}=\pm24\sqrt{2.4}=\pm37$ mm, so the work is accepted, and the correction $-21$ mm is distributed in proportion to the set-ups (or distance).

**(b) Longitudinal and cross-section levelling.**

*Longitudinal section (profile) levelling* gives the elevation of the ground along a *centre line* (the alignment of a road, canal, sewer or pipeline) at regular intervals (for example every 20 m or 30 m) and at every break of the slope; the levels are plotted with the chainage on the horizontal scale (for example 1:1000) and the RL on a vertical scale 10 times larger (1:100). It shows the ground profile, and is used to fix the formation level or the gradient and to compute cut and fill.

*Cross-section levelling* gives the ground levels along lines *at right angles* to the centre line at each chainage (for example 10 to 20 m left and right), for the width of the work. It shows the lateral slope and allows the earthwork volume (the area of the cross-section × the distance) to be computed.

```figure caption="Question 3(b): left, plan with the centre line and cross-section lines; middle, longitudinal profile (vertical scale exaggerated); right, one cross section."
fig,(a,b,c)=plt.subplots(1,3,figsize=(6.6,2.2))
for ax in (a,b,c): ax.axis("off")
a.plot([0,6],[0.5,0.9],color=INK,lw=2)
for x in (1,2.5,4,5.4):
    y=0.5+0.4*x/6; a.plot([x,x+0.1],[y-0.8,y+0.8],color=ACCENT,lw=1.2)
a.text(3,-0.55,"plan: centre line + X-sections",fontsize=7,ha="center"); a.set_xlim(-0.3,6.4); a.set_ylim(-0.8,1.9)
x=np.array([0,1,2,3,4,5,6]); y=np.array([2.0,1.7,1.9,1.2,1.4,0.9,1.1])
b.plot(x,y,color="#8a6d3b",lw=2); b.plot([0,6],[1.9,0.6],color=ACCENT,lw=1.2,ls="--")
for xi,yi in zip(x,y): b.plot([xi,xi],[0,yi],color="#bbb",lw=0.6)
b.text(3,-0.45,"L-section: ground and formation",fontsize=7,ha="center"); b.set_xlim(-0.3,6.4); b.set_ylim(-0.7,2.5)
xs=np.array([-4,-3,-2,-1,0,1,2,3,4]); ys=np.array([1.9,1.6,1.4,1.3,1.2,1.0,0.8,0.6,0.5])
c.plot(xs,ys,color="#8a6d3b",lw=2); c.plot([0,0],[0,1.2],color=INK,lw=1,ls=":")
c.text(0,-0.45,"cross-section at a chainage",fontsize=7,ha="center"); c.text(0.2,0.3,"CL",fontsize=7); c.set_xlim(-4.4,4.4); c.set_ylim(-0.7,2.3)
plt.tight_layout()
```

**(c) Rise and fall method.** Set-ups: (1) readings 1, 2, 3 (BS 0.685, IS 1.315, FS 1.825); (2) readings 4, 5, 6 (BS 0.635, IS 1.205, FS 1.235); (3) readings 7, 8, 9 (BS 2.631, IS 1.355, FS 2.015). The 3rd reading was taken on a BM of RL 1580.000 m, so the RLs of the first two points are found backwards from it. The rise or fall between two consecutive staff readings of the same set-up is: $\text{previous reading}-\text{next reading}$ (+ rise, − fall).

| Point | Chainage (m) | BS | IS | FS | Rise | Fall | RL (m) | Remark |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0.685 | | | | | 1581.140 | first station |
| 2 | 20 | | 1.315 | | | 0.630 | 1580.510 | |
| 3 | 40 | | | 1.825 | | 0.510 | 1580.000 | BM (given) and CP |
| 3 | 40 | 0.635 | | | | | 1580.000 | CP |
| 4 | 60 | | 1.205 | | | 0.570 | 1579.430 | |
| 5 | 80 | | | 1.235 | | 0.030 | 1579.400 | CP |
| 5 | 80 | 2.631 | | | | | 1579.400 | CP |
| 6 | 100 | | 1.355 | | 1.276 | | 1580.676 | |
| 7 | 120 | | | 2.015 | | 0.660 | 1580.016 | last station |
| Sum | | 3.951 | | 5.075 | 1.276 | 2.400 | | |

**Checks.**

$$\begin{gathered}\Sigma BS-\Sigma FS=3.951-5.075=-1.124\\ \Sigma\text{Rise}-\Sigma\text{Fall}=1.276-2.400=-1.124\\ RL_{\text{last}}-RL_{\text{first}}=1580.016-1581.140=-1.124\end{gathered}$$

All three agree, so the computation is arithmetically correct.

**Gradient from the first to the last station** ($120$ m, six intervals of 20 m):

$$\text{gradient}=\frac{-1.124}{120}=-\frac{1}{106.8}\approx\boxed{1\text{ in }107\ \text{falling}\ (0.94\%)}$$

@s 4
**(a) Features of the total station.**

- **Combined angle and distance measurement:** an electronic theodolite and an EDM in one body, so that HA, VA and slope distance are read together (angle accuracy 1" to 5", distance $\pm(2\text{ mm}+2\text{ ppm})$).
- **On-board processor:** computes the horizontal distance, vertical difference, coordinates, area, and angle corrections, and has built-in programs: resection, remote elevation, missing line, set-out (stakeout), traverse adjustment, and COGO.
- **Data storage and transfer:** internal memory or card, cable, Bluetooth or USB transfer, feature codes, directly to CAD/DTM software; there are no field-book booking errors.
- **Reflectorless (laser) measurement** to a surface, and measurement to a prism over several kilometres.
- **Automatic corrections** for the earth's curvature and refraction, atmospheric ppm, prism constant, and the dual-axis compensator for the level; laser plummet and electronic bubble for fast set-up.
- **Robotic** models (servo motors, auto-tracking) allow a one-person survey, and can be controlled remotely.

**(b) Tangential tacheometry.** The method is used when the stadia hairs cannot be read on the staff (a tilted line of sight, or when the staff is too far or the stadia hairs are not fitted), the distances are found by sighting two *vanes* or targets on the staff at a known separation $s$ and measuring the **two vertical angles** with the theodolite, and no stadia reading is needed: $D=\dfrac{s}{\tan\alpha_1\pm\tan\alpha_2}$.

*Case 1: both angles of elevation* ($\alpha_2>\alpha_1$), the instrument axis below both vanes:

$$\begin{gathered}D=\frac{s}{\tan\alpha_2-\tan\alpha_1} \\ V=D\tan\alpha_1 \\ RL_{\text{staff}}=RL_{\text{axis}}+D\tan\alpha_1-h_1\end{gathered}$$

*Case 2: both angles of depression* ($\alpha_1>\alpha_2$, upper vane depression $\alpha_2$):

$$\begin{gathered}D=\frac{s}{\tan\alpha_1-\tan\alpha_2} \\ RL_{\text{staff}}=RL_{\text{axis}}-D\tan\alpha_2-h_2\end{gathered}$$

*Case 3: one elevation $\alpha_2$ (upper vane) and one depression $\alpha_1$ (lower vane):*

$$\begin{gathered}D=\frac{s}{\tan\alpha_1+\tan\alpha_2} \\ RL_{\text{staff}}=RL_{\text{axis}}-D\tan\alpha_1-h_1\end{gathered}$$

where $h_1$ and $h_2$ are the heights of the lower and upper vanes above the staff point.

```figure caption="Question 4(b): tangential tacheometry. Case 1: both vanes above the horizontal (elevation angles a1 and a2); case 3: lower vane in depression and upper vane in elevation. s = vane separation."
fig,(a,b)=plt.subplots(1,2,figsize=(6.4,2.3))
for ax in (a,b): ax.axis("off")
D=8
for ax in (a,b): ax.plot([0,D+1],[0,0],color="#888",lw=0.8,ls=":"); ax.plot(0,0,"^",color=INK,ms=7)
a1=np.radians(6); a2=np.radians(14)
a.plot([0,D],[0,D*np.tan(a1)],color=ACCENT,lw=1.2); a.plot([0,D],[0,D*np.tan(a2)],color=ACCENT,lw=1.2); a.plot([D,D],[-0.6,D*np.tan(a2)+0.7],color=INK,lw=3)
a.plot([D-0.4,D+0.4],[D*np.tan(a1)]*2,color="#d9534f",lw=3); a.plot([D-0.4,D+0.4],[D*np.tan(a2)]*2,color="#d9534f",lw=3)
a.text(3,0.15,"α1",fontsize=8); a.text(2.2,1.0,"α2",fontsize=8); a.text(D+0.6,(D*np.tan(a1)+D*np.tan(a2))/2,"s",fontsize=9); a.set_title("case 1: both elevations",fontsize=7.5)
b1=np.radians(5); b2=np.radians(8)
b.plot([0,D],[0,-D*np.tan(b1)],color=ACCENT,lw=1.2); b.plot([0,D],[0,D*np.tan(b2)],color=ACCENT,lw=1.2); b.plot([D,D],[-D*np.tan(b1)-0.7,D*np.tan(b2)+0.7],color=INK,lw=3)
b.plot([D-0.4,D+0.4],[-D*np.tan(b1)]*2,color="#d9534f",lw=3); b.plot([D-0.4,D+0.4],[D*np.tan(b2)]*2,color="#d9534f",lw=3)
b.text(3,-0.55,"α1",fontsize=8); b.text(3,0.4,"α2",fontsize=8); b.text(D+0.6,0,"s",fontsize=9); b.set_title("case 3: depression and elevation",fontsize=7.5)
for ax in (a,b): ax.set_xlim(-0.8,D+2); ax.set_ylim(-2.5,3.2)
plt.tight_layout()
```

**(c) Mean horizontal angles.** The same readings as printed in the 2082 Baishakh paper. Differences of successive pointings (A to B, B to C, C to the closing A):

| Angle | Face left | Face right | Mean |
|---|---|---|---|
| AOB | 150°35'20" − 0°10'30" = 150° 24' 50" | 330°15'20" − 180°50'30" = 149° 24' 50" | 149° 54' 50" |
| BOC | 240°20'30" − 150°35'20" = 89° 45' 10" | 60°25'40" + 360° − 330°15'20" = 90° 10' 20" | 89° 57' 45" |
| COA | 360° + 0°05'40" − 240°20'30" = 119° 45' 10" | 180°10'40" − 60°25'40" = 119° 45' 00" | 119° 45' 05" |
| Sum | 359° 55' 10" | 359° 20' 10" | 359° 37' 40" |

The three angles round a point should sum to $360^\circ$; the closing error is $22'20''$, due to the closing readings on A differing from the opening readings (and the printed face-right start of $180^\circ50'30''$, which is $40'$ off the face-left value plus $180^\circ$; the AOB values differ by exactly $1^\circ$, which suggests a misprint in the question). The error is distributed equally ($+7'26.7''$ per angle):

$$\boxed{\angle AOB=150^\circ02'17'',\quad\angle BOC=90^\circ05'12'',\quad\angle COA=119^\circ52'32''}$$

@s 5
**(a) Triangulation** is the method of control surveying in which the area is covered by a network of connected triangles; one side (the base line) is measured accurately, the angles of every triangle are measured with a precise theodolite, and the other sides and the coordinates of the stations are computed by the sine rule (checked by a check base):

$$b=a\frac{\sin B}{\sin A}$$

**Norms and specification (third-order triangulation).** The classification follows the accuracy and purpose. Typical values for third order, as given in the surveying textbooks (Survey-of-India style classification):

| Item | Third order |
|---|---|
| Purpose | Control for engineering and cadastral surveys, detail and local mapping, locates points inside the first- and second-order frame |
| Length of base line | about 0.5 km to 3 km |
| Length of sides of triangles | about 1.5 km to 10 km |
| Average triangular error (closure) | about 12" (not above 5" to 15" in the best practice) |
| Maximum triangular error | about 15" |
| Station error (probable error of an observed direction) | about 5" |
| Discrepancy between two measures of the base | about 20 mm $\sqrt{k}$ ($k$ in km) |
| Probable error of the base | about 1 in 250 000 |
| Probable error of the computed distance | about 1 in 5 000 |
| Other norms | well-conditioned triangles (all angles between $30^\circ$ and $120^\circ$, never below $20^\circ$ in the best chain), each angle observed on both faces with a 1" to 20" theodolite on several zeroes, a check base after about 6 to 8 triangles, and signals visible from the neighbouring stations |

**(b) Manual and computer-aided plotting.**

| Manual plotting | Computer-aided plotting |
|---|---|
| Points plotted by scale, protractor and ruler on paper; slow and tiring | Points plotted directly from the coordinates (or digitised or imported from the total station); very fast |
| Graphical accuracy about 0.2 mm on paper (error at scale), plus an error from the paper shrinkage | Accuracy of the coordinates (mm), no shrinkage |
| A new scale or sheet needs a re-draw | Any scale, sheet size or projection, from one database |
| Contours, areas and volumes by hand and planimeter | Contours by TIN or grid interpolation, area and volume by command |
| Editing means erasing, so it is a bad record when the drawing is revised | Layers, easy editing, undo, and digital storage, backup and sharing |
| Skilled draftsman needed; the quality varies | Standard symbols and quality; needs a computer and a trained operator, and software or power cost |

**(c) Anallactic tacheometry** ($k=100$, $C=0$): the axis RL is $1085.550+1.385=1086.935$ m, and $D=ks\sin^2\theta$, $V=\tfrac12ks\sin2\theta$, $RL=RL_{\text{axis}}+V-h$ ($h$ the central hair).

**Staff at B.** $s=2.345-1.295=1.050$ m, $\theta=71^\circ30'$ (elevation $+18^\circ30'$), $h=1.820$:

$$D_B=100(1.050)\sin^2(71^\circ30')=94.43\ \text{m},\quad V_B=\tfrac12(100)(1.050)\sin(143^\circ)=+31.60\ \text{m}$$

$$RL_B=1086.935+31.60-1.820=\boxed{1116.71\ \text{m}}$$

**Staff at C.** $s=2.570-1.010=1.560$ m, $\theta=96^\circ00'$ (depression $-6^\circ$), $h=1.790$:

$$D_C=100(1.560)\sin^2(96^\circ)=154.30\ \text{m},\quad V_C=\tfrac12(100)(1.560)\sin(192^\circ)=-16.22\ \text{m}$$

$$RL_C=1086.935-16.22-1.790=\boxed{1068.93\ \text{m}}$$

**Line BC.** Using the azimuths (18° and 127°) the coordinates of B and C relative to A are:

$$\begin{gathered}B:\ \Delta E=94.43\sin18^\circ=29.18,\quad\Delta N=94.43\cos18^\circ=89.81\\ C:\ \Delta E=154.30\sin127^\circ=123.23,\quad\Delta N=154.30\cos127^\circ=-92.86\end{gathered}$$

$$BC=\sqrt{(123.23-29.18)^2+(-92.86-89.81)^2}=\sqrt{94.05^2+182.67^2}=205.45\ \text{m}$$

The bearing of BC is $152^\circ45'$ and the difference of level is $1068.93-1116.71=-47.78$ m:

$$\boxed{\text{gradient of BC}=\frac{47.78}{205.45}=0.2326=\frac{1}{4.30}\ \text{(falling from B to C, 23.3\%)}}$$

---
file: NEBians-IOE-Past-Paper-Engineering-Survey-I-CE153-2082-Baishakh.pdf
subject: Engineering Survey I
level: BE · Year I / Part II
code: CE 153
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Civil, Year I / Part II. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) List the principle of surveying in chronological order. Differentiate the primary classification of surveying with examples. [[1+3]]

b) What are the method that you can apply for the distance measurements at the sloping ground? Explain with neat sketch. Is there any need to check precision if so explain? [[3+1]]

c) A rectangular plot of land of area 2.25 hectare is represented on a map of similar rectangle area of 36 cm². Calculate the representative factor of the scale of the map. Draw a diagonal scale from the map. The scale should be long enough to measure up to 500 m. Also show 275 m on the drawn scale. [[4]]

@q 2
a) What are the types of offsets that you used in chain surveying? What is the principle of plane table survey? Is the plane table survey being better than the chain survey if so give reason behind this? [[2+1+1]]

b) List and explain the types of bearing according to designation of bearing. [[2]]

c) The following are bearing taken on closed compass traverse. [[6]]

| Line/leg | FB | BB |
|---|---|---|
| AB | 120° 20' | 301° 50' |
| BC | 170° 50' | 350° 50' |
| CD | 230° 10' | 49° 30' |
| DE | 310° 20' | 130° 15' |
| EA | 80° 10' | 259° 0' |

Compute correct interior angle and corrected bearing also. The least count of compass is 30'.

@q 3
a) Explain the field procedure and process to find out correct staff reading on two peg test. Why you are performing the two peg test? Give reason. [[3+1]]

b) You are asked to transfer the reduced level from TBM1 to TBM2, which type of levelling operation you preferred? Explain with neat sketch. [[3]]

c) The consecutive readings taken during a levelling operation at a common interval of 15 m were as follows: 0.597, 2.587, 3.132, 1.565, 1.911, 0.376, 1.522, 2.244, 0.376, 1.522, 2.244, 3.771, 1.985, 1.334, 0.601 and 2.002 m. The level instrument was shifted after 2nd, 7th and 10th readings. The first reading was taken to a benchmark of assumed elevation 2778.233 m. Reduce the levels and apply appropriate checks. [[5]]

@q 4
a) What is total station? Describe the procedure for the digital data recording on the total station briefly. [[4]]

b) What is the principle of stadia tacheometry? Explain with neat sketch. [[3]]

c) Calculate the mean horizontal angle <AOB, <BOC and <COA from the following observation. [[5]]

| Instrument station | Sighted to | Face Left | Face Right |
|---|---|---|---|
| O | A | 00°10'30" | 180°50'30" |
| | B | 150°35'20" | 330°15'20" |
| | C | 240°20'30" | 60°25'40" |
| | A | 0°05'40" | 180°10'40" |

@q 5
a) Differentiate between triangulation and trilateration. Explain the different layout of triangles in triangulation with sketch. [[2+2]]

b) Write the features of any software that be used for mapping and plotting. Explain briefly how does that software works. [[4]]

c) Find out Reduced level, distance and gradient between P and Q by using the following data in table, the staff held vertical to the line of sight by using anallactic lens. Take RL of instrument station is 1250.50 m. HI = 1.450 m. [[4]]

| Instrument Station | Staff | Line | Bearing | Zenithal angle | Stadia Hair readings |
|---|---|---|---|---|---|
| O | P | OP | 60°30' | 87°30' | 1.35, 2.10, 2.85 |
| O | Q | OQ | 170°45' | 92°45' | 1.955, 2.875, 3.795 |

<!-- SOLUTIONS -->

@s 1
**(a) Principles of surveying (in the order they are applied).**

1. **Working from whole to part:** first fix a framework of control stations accurately, then fix the details inside it with less accurate methods, so that errors do not accumulate.
2. **Fixing a new station by at least two independent measurements** (two lengths, two angles, or a length and an angle) from points already fixed, with a third measurement as an independent check on the work.

(Reconnaissance, planning and the *independent check* on every stage of the field work and the plotting are the practical steps that carry out these two principles.)

**Primary classification.**

| Plane surveying | Geodetic surveying |
|---|---|
| The earth's surface is taken as a plane; the effect of curvature is ignored | The earth is taken as a spheroid; curvature is allowed for |
| Small areas (below about 250 km²); plane trigonometry | Large areas; spherical trigonometry (spherical excess) |
| Ordinary accuracy; chain, compass, theodolite, level, total station | Very high accuracy; precise theodolite, invar tape, EDM, GNSS |
| Examples: site survey for a building, road, canal or small bridge; cadastral parcel map | Examples: national triangulation network, long-distance geodetic control, a country-wide levelling net |

**(b) Distance measurement on sloping ground.**

1. **Direct method (stepping).** The tape is stretched horizontally in short steps, and the plumb bob transfers the end of each step to the ground. Used on steep, rough slopes with the chain shortened, the steps added to give $D=\sum l$.
2. **Slope measurement with reduction.** The slope length $L$ is measured along the ground, and the angle of slope $\theta$ (clinometer or theodolite) or the difference of level $h$ between the ends (by levelling) is measured:

$$D=L\cos\theta=\sqrt{L^2-h^2}\approx L-\frac{h^2}{2L}$$

3. **Indirect methods:** stadia tacheometry, EDM, total station, triangulation.

```figure caption="Question 1(b): (left) direct stepping method on a slope with plumb bobs; (right) slope length L, horizontal distance D and difference of level h."
fig,(a,b)=plt.subplots(1,2,figsize=(6.4,2.2))
for ax in (a,b): ax.axis("off")
x=np.linspace(0,6,50); a.plot(x,0.5*x,color="#8a6d3b",lw=2)
for i in range(4):
    x0=1.2*i+0.2; y0=0.5*x0
    a.plot([x0,x0+1.2],[y0+0.55,y0+0.55],color=ACCENT,lw=1.6); a.plot([x0,x0],[y0,y0+0.55],color=INK,lw=0.8,ls=":")
    a.plot([x0+1.2,x0+1.2],[y0+0.55,0.5*(x0+1.2)],color=INK,lw=0.8,ls=":")
a.text(3,0.2,"horizontal steps, plumb bobs",fontsize=7,ha="center"); a.set_xlim(-0.2,6.5); a.set_ylim(-0.3,4)
b.plot([0,5],[0,2.2],color=INK,lw=2); b.plot([0,5],[0,0],color=ACCENT,lw=1.4); b.plot([5,5],[0,2.2],color=ACCENT,lw=1.4)
b.text(2.2,1.4,"L",fontsize=10); b.text(2.5,-0.35,"D = L cos θ",fontsize=8,ha="center"); b.text(5.1,1.0,"h",fontsize=10); b.text(0.8,0.12,"θ",fontsize=9)
b.set_xlim(-0.3,5.8); b.set_ylim(-0.7,2.6)
plt.tight_layout()
```

**Precision check.** Yes. Slope measurement is more error-prone, so each length is measured twice (forward and backward), and the discrepancy gives the *relative precision*, for example $\dfrac{|L_1-L_2|}{L_{\text{mean}}}$ must not exceed about $1/2000$ for ordinary chaining. Without the check, errors of slope angle, sag and tension on the slope would pass unnoticed.

**(c) Scale.**

Area of plot: $2.25\ \text{ha}=2.25\times10^4\ \text{m}^2=2.25\times10^8\ \text{cm}^2$. Map area $=36\ \text{cm}^2$. Since area scales with the square of the linear scale:

$$\text{R.F.}=\sqrt{\frac{36}{2.25\times10^8}}=\sqrt{1.6\times10^{-7}}=4\times10^{-4}=\boxed{\frac1{2500}}$$

So 1 cm on the map = 25 m on the ground. A length of 500 m is $500/25=20$ cm. A plain scale cannot give the metres, so a diagonal scale is used (reading to 1 m):

- Draw a line of 20 cm, divided into 5 main divisions of 4 cm (each 100 m).
- Divide the first main division (to the left of 0) into 10 subdivisions of 0.4 cm (10 m each).
- Draw 10 equally spaced horizontal lines through the scale and join the top of each subdivision to the bottom of the next one: each horizontal then gives $1/10$ of 10 m $=1$ m.

$$275\ \text{m}=200+70+5=2\ \text{main divisions}+7\ \text{subdivisions}+5\ \text{m}$$

```figure caption="Question 1(c): diagonal scale 1 cm = 25 m (RF 1/2500), 500 m long, reading to 1 m, with 275 m shown. Vertical spacing is not to scale."
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
m,k,j=2,8,5; x=-(k-1)/10-(10-j)/100; y=H*j/10
ax.plot([x,m],[y,y],color="#d9534f",lw=2.4); ax.plot([x,m],[y,y],"o",color="#d9534f",ms=4); ax.text((x+m)/2,y+0.08,"275 m",color="#d9534f",fontsize=8,ha="center")
ax.set_xlim(-1.2,5.5); ax.set_ylim(-0.8,H+0.55)
```

@s 2
**(a) Offsets in chain surveying.**

- **Perpendicular offset:** at right angles to the chain line, set out with a cross staff, an optical square or by the 3-4-5 tape method. Accurate, used for most detail.
- **Oblique offset:** at an angle other than $90^\circ$, measured with a tape from two points of the chain line (tie lines); used where a perpendicular cannot be set out (obstacle, long distance).

(The offsets are also classed by length: *long* beyond the maximum of 15 m for a 20 m chain is not permitted in good work, and *short* offsets are accurate.)

**Principle of plane table survey.** *Parallelism*: the plane table is **oriented** at each station, so that every line drawn on the sheet is parallel to the corresponding line on the ground, and the plan is plotted *in the field* by drawing rays from the station with the alidade and scaling the distances (methods: radiation, intersection, traversing, resection).

**Better than chain survey?** *Often yes, but not always.*

- The map is drawn in the field, so mistakes and omissions are seen immediately; no booking or transcription errors.
- Fewer measurements are needed (angles are drawn instead of being measured), and the surveyor can sketch irregular detail, contours and slopes with judgment.
- It is rapid for medium-size areas and detail mapping, and no field book is needed.

But it needs fair weather and open, not crowded ground; it is less precise than a theodolite and for small flat areas, a simple chain survey is cheaper and just as good. So it is better where detail is rich and speed matters, and chain survey is better for small and open plots.

**(b) Types of bearing according to designation.**

1. **Whole circle bearing (WCB)**, or azimuth: the angle from the north end of the meridian *clockwise* to the line, $0^\circ$ to $360^\circ$ (for example $230^\circ10'$). Used in the prismatic compass and the surveyor's compass in the field.
2. **Quadrantal (reduced) bearing (QB)**: the acute angle between the line and the nearer end (N or S) of the meridian, measured towards E or W, written as N $\alpha$ E, S $\alpha$ W (e.g. S $50^\circ10'$ W).

| WCB $\theta$ | $0$–$90^\circ$ | $90$–$180^\circ$ | $180$–$270^\circ$ | $270$–$360^\circ$ |
|---|---|---|---|---|
| QB | N $\theta$ E | S $(180^\circ-\theta)$ E | S $(\theta-180^\circ)$ W | N $(360^\circ-\theta)$ W |

**(c) Closed compass traverse.**

*Local attraction check.* $\text{B.B.}-\text{F.B.}$ should be $180^\circ$ for a line free of local attraction at both ends: AB $181^\circ30'$, **BC $180^\circ00'$**, CD $179^\circ20'$, DE $179^\circ55'$, EA $178^\circ50'$. Only **BC** is correct, so stations B and C are free of attraction, and the other lines show the effect at A, D and E.

*Interior angles* (traverse run anti-clockwise, interior angle on the left): $\alpha=\text{B.B.}_{\text{previous line}}-\text{F.B.}_{\text{next line}}$ (add $360^\circ$ if negative).

$$\begin{gathered}\angle A=259^\circ00'-120^\circ20'=138^\circ40'\\ \angle B=301^\circ50'-170^\circ50'=131^\circ00'\\ \angle C=350^\circ50'-230^\circ10'=120^\circ40'\\ \angle D=49^\circ30'+360^\circ-310^\circ20'=99^\circ10'\\ \angle E=130^\circ15'-80^\circ10'=50^\circ05'\end{gathered}$$

The sum is $539^\circ35'$, but a closed five-sided figure needs $(2n-4)\times90^\circ=540^\circ$. The error is $-25'$, which is less than the least count of the compass ($30'$), so the observation is acceptable; the correction is $+25'/5=+5'$ at each station:

| Station | Observed interior angle | Correction | Corrected interior angle |
|---|---|---|---|
| A | 138° 40' | +5' | 138° 45' |
| B | 131° 00' | +5' | 131° 05' |
| C | 120° 40' | +5' | 120° 45' |
| D | 99° 10' | +5' | 99° 15' |
| E | 50° 05' | +5' | 50° 10' |
| Sum | 539° 35' | +25' | 540° 00' |

*Corrected bearings.* The line BC has no local attraction, so its bearing $170^\circ50'$ is taken as correct, and the others follow from $\theta_{\text{next}}=\theta_{\text{prev}}+180^\circ-\alpha$:

$$\begin{gathered}\theta_{CD}=170^\circ50'+180^\circ-120^\circ45'=230^\circ05'\\ \theta_{DE}=230^\circ05'+180^\circ-99^\circ15'=310^\circ50'\\ \theta_{EA}=310^\circ50'+180^\circ-50^\circ10'=80^\circ40'\\ \theta_{AB}=80^\circ40'+180^\circ-138^\circ45'=121^\circ55'\\ \theta_{BC}=121^\circ55'+180^\circ-131^\circ05'=170^\circ50'\ \checkmark\end{gathered}$$

| Line | Corrected F.B. | Corrected B.B. |
|---|---|---|
| AB | 121° 55' | 301° 55' |
| BC | 170° 50' | 350° 50' |
| CD | 230° 05' | 50° 05' |
| DE | 310° 50' | 130° 50' |
| EA | 80° 40' | 260° 40' |

@s 3
**(a) Two peg test (to find the correct staff reading and test the line of collimation).**

1. Choose two points A and B about 60 m to 100 m apart on level ground, drive pegs and hold the staff on each.
2. **Set-up 1.** Place the level at the mid-point C (equal sight lengths, so the collimation error is the same on both sights and cancels). Read the staff at A ($a_1$) and at B ($b_1$). The **true difference of level** is $H=a_1-b_1$ (rise or fall from A to B), free of the instrument error.
3. **Set-up 2.** Shift the level to a point D on the line AB produced, about 2 m beyond A (or 2 m before A), so that it is very close to staff A. Read A ($a_2$, practically free from the error because the sight is very short) and B ($b_2$, the full error).
4. **The correct reading on B** is $b_2'=a_2-H=a_2-(a_1-b_1)$. If $b_2=b_2'$ the line of sight is horizontal. If not, the collimation error is $e=b_2-b_2'$ over the distance DB, and the line of sight is brought to the reading $b_2'$ on staff B with the capstan screws of the diaphragm (reticle), or with the tilting screw and the bubble re-centred by the foot screws; the test is repeated.

```figure caption="Question 3(a): two peg test. Left: level midway between A and B (true difference a1 - b1). Right: level near A, reading a2 on A and b2 on B; the correct reading on B is a2 - (a1 - b1)."
fig,(a,b)=plt.subplots(1,2,figsize=(6.4,2.3))
for ax in (a,b): ax.axis("off")
for ax in (a,b):
    ax.plot([0,10],[0,0],color="#8a6d3b",lw=2)
    for x in (1.0,9.0): ax.plot([x,x],[0,3],color=INK,lw=3)
    ax.text(1.0,-0.45,"A",ha="center",fontsize=9); ax.text(9.0,-0.45,"B",ha="center",fontsize=9)
a.plot(5,0.4,"^",color=INK,ms=7); a.plot([5,1],[0.8,1.9],color=ACCENT,lw=1.1,ls="--"); a.plot([5,9],[0.8,1.2],color=ACCENT,lw=1.1,ls="--"); a.plot([1,9],[0.8,0.8],color="#aaa",lw=0.8,ls=":")
a.text(1.2,2.0,"a1",fontsize=8); a.text(9.2,1.3,"b1",fontsize=8); a.text(5,-0.45,"C (mid)",ha="center",fontsize=8)
b.plot(0.1,0.4,"^",color=INK,ms=7); b.plot([0.1,1],[0.8,0.82],color=ACCENT,lw=1.1,ls="--"); b.plot([0.1,9],[0.8,1.5],color=ACCENT,lw=1.1,ls="--"); b.plot([0.1,9],[0.8,0.8],color="#aaa",lw=0.8,ls=":")
b.text(1.2,0.95,"a2",fontsize=8); b.text(9.2,1.55,"b2",fontsize=8); b.text(0.1,-0.45,"D (near A)",ha="center",fontsize=8)
for ax in (a,b): ax.set_xlim(-0.6,10.4); ax.set_ylim(-0.8,3.3)
plt.tight_layout()
```

**Why.** The line of sight of a level should be horizontal when the bubble is centred (the *permanent adjustment*). If the line of collimation is inclined by an angle $\alpha$, every staff reading has an error of $D\tan\alpha$ proportional to the sight length, and this does not cancel when the sights are unequal. The test finds the error and allows its removal (or its allowance), and so protects the accuracy of the levelling.

**(b) Transfer of RL from TBM1 to TBM2.** The proper method is **differential (fly) levelling**: a line of levels between the two benchmarks, with the instrument set up at convenient positions (back-sight and fore-sight distances about equal) and the staff carried over *change points*. $RL_{TBM2}=RL_{TBM1}+\Sigma BS-\Sigma FS$. Its accuracy is checked by running a second line back from TBM2 to TBM1 (check levelling) or by tying to a third BM, and the misclosure (allowable $\pm k\sqrt K$ mm, $K$ in km) is distributed over the change points. If a river, valley or other obstacle makes sights unequal, **reciprocal levelling** is used across it, and over a long distance, **precise levelling** of a higher order can be used.

```figure caption="Question 3(b): fly levelling from TBM1 to TBM2 with change points (CP) and equal back-sight and fore-sight distances."
fig,ax=plt.subplots(figsize=(6.2,1.9)); ax.axis("off")
x=np.array([0,2,4,6,8,10,12]); y=np.array([2.0,1.4,1.9,1.1,0.9,1.5,1.0])
ax.plot(np.linspace(0,12,100),np.interp(np.linspace(0,12,100),x,y),color="#8a6d3b",lw=2)
for xx in (1,3.4,5,7,9,11): pass
for xs,lab in [(0,"TBM1"),(4,"CP1"),(8,"CP2"),(12,"TBM2")]:
    yy=np.interp(xs,x,y); ax.plot([xs,xs],[yy,yy+1.5],color=INK,lw=3); ax.text(xs,yy-0.25,lab,ha="center",fontsize=8)
for xi in (2,6,10):
    yy=np.interp(xi,x,y); ax.plot(xi,yy+1.3,"^",color=ACCENT,ms=7); ax.plot([xi-2,xi+2],[yy+1.3]*2,color=ACCENT,lw=1,ls="--")
ax.text(1,3.25,"BS",fontsize=7); ax.text(3,3.25,"FS",fontsize=7)
ax.set_xlim(-0.8,12.8); ax.set_ylim(0,3.6)
```

**(c) Reduction of levels** (readings in order: BS, FS | BS, IS, IS, IS, FS | BS, IS, FS | BS, IS, IS, IS, IS, FS). The instrument was shifted after the 2nd, 7th and 10th readings, so the 3rd, 8th and 11th readings are back-sights, and the 2nd, 7th and 10th are fore-sights on the change points; the 16th is the last fore-sight. HI method, $HI=RL+BS$, $RL=HI-\text{reading}$:

| Reading | Chainage (m) | BS | IS | FS | HI | RL (m) | Remark |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 0.597 | | | 2778.830 | 2778.233 | BM |
| 2 | 15 | | | 2.587 | | 2776.243 | CP1 |
| 3 | 15 | 3.132 | | | 2779.375 | 2776.243 | CP1 |
| 4 | 30 | | 1.565 | | 2779.375 | 2777.810 | |
| 5 | 45 | | 1.911 | | 2779.375 | 2777.464 | |
| 6 | 60 | | 0.376 | | 2779.375 | 2778.999 | |
| 7 | 75 | | | 1.522 | | 2777.853 | CP2 |
| 8 | 75 | 2.244 | | | 2780.097 | 2777.853 | CP2 |
| 9 | 90 | | 0.376 | | 2780.097 | 2779.721 | |
| 10 | 105 | | | 1.522 | | 2778.575 | CP3 |
| 11 | 105 | 2.244 | | | 2780.819 | 2778.575 | CP3 |
| 12 | 120 | | 3.771 | | 2780.819 | 2777.048 | |
| 13 | 135 | | 1.985 | | 2780.819 | 2778.834 | |
| 14 | 150 | | 1.334 | | 2780.819 | 2779.485 | |
| 15 | 165 | | 0.601 | | 2780.819 | 2780.218 | |
| 16 | 180 | | | 2.002 | | 2778.817 | last point |

**Checks.** (1) $\Sigma BS=0.597+3.132+2.244+2.244=8.217$, $\Sigma FS=2.587+1.522+1.522+2.002=7.633$; $\Sigma BS-\Sigma FS=+0.584$ m.

(2) Rise and fall: rises 1.567 + 1.535 + 1.868 + 1.786 + 0.651 + 0.733 = 8.140; falls 1.990 + 0.346 + 1.146 + 1.146 + 1.527 + 1.401 = 7.556; $\Sigma\text{rise}-\Sigma\text{fall}=+0.584$ m.

(3) Last RL − first RL $=2778.817-2778.233=+0.584$ m.

$$\Sigma BS-\Sigma FS=\Sigma\text{rise}-\Sigma\text{fall}=RL_{\text{last}}-RL_{\text{first}}=0.584\ \text{m}\ \checkmark$$

All three checks agree, so the reduction is arithmetically correct. As the line does not close on a second benchmark, no field (misclosure) check is possible.


@s 4
**(a) Total station.** An electronic instrument that combines an electronic theodolite (horizontal and vertical angles), an EDM (slope distance) and an on-board computer with memory, so that angles and distances are measured together and the horizontal distance, elevation difference and the coordinates $(N,E,Z)$ of a sighted point are computed and stored automatically.

**Digital data recording (procedure).**

1. Set up and centre the instrument over the occupied station (tripod, optical or laser plummet), level it with the foot screws and the electronic bubble, switch on and check the battery, memory and the atmospheric (ppm) and prism-constant settings.
2. **Create a job (file)** with a name, and set the units, the coordinate order and the scale factor.
3. Enter the **station data**: occupied station number and coordinates (or assume 1000, 1000, 100), the height of the instrument $h_i$.
4. Enter the **back-sight (orientation)**: the back-station number and its coordinates or the known azimuth; sight the prism on it, set the horizontal circle to the computed azimuth (or zero), and record. Check the orientation on a second known point.
5. Enter the target (prism) height $h_t$, then sight each detail point, press *measure*; the instrument stores the point number, code (feature), HA, VA, slope distance and the computed $N,E,Z$:

$$N=N_O+D\cos\theta,\quad E=E_O+D\sin\theta,\quad Z=Z_O+h_i+V-h_t$$

6. After the last point, close the job, and (if wanted) take a check shot to the back-sight again; download to a computer by cable, Bluetooth or memory card for plotting.

**(b) Principle of stadia tacheometry.** Two additional horizontal hairs (the stadia hairs), at equal distances above and below the central hair, are fixed in the diaphragm of the telescope. The lines of sight through them diverge at a fixed angle, so the staff intercept $s$ between the stadia hairs is proportional to the distance of the staff from the instrument. With $f$ the focal length, $i$ the stadia interval and $d$ the distance from the objective to the vertical axis, similar triangles give $D=\dfrac fis+(f+d)=ks+C$, where $k=f/i$ (=100) and $C=f+d$ (about 0.3 m, zero in an anallatic telescope). For an inclined line of sight at the vertical angle $\alpha$ with the staff held vertical:

$$\begin{gathered}D=ks\cos^2\alpha+C\cos\alpha \\ V=\tfrac12ks\sin2\alpha+C\sin\alpha\end{gathered}$$

$$RL_{\text{staff point}}=RL_{\text{inst. axis}}\pm V-h\ (h=\text{central hair reading})$$

```figure caption="Question 4(b): stadia tacheometry. Staff held vertically with the line of sight inclined at angle alpha; intercept s between the upper and lower hairs; D = k s cos^2(alpha), V = (1/2) k s sin(2 alpha)."
fig,ax=plt.subplots(figsize=(5.8,2.4)); ax.axis("off")
al=np.radians(12); Dd=8.0
ax.plot([0,Dd+1],[0,0],color="#888",lw=0.8,ls=":")
ax.plot([0,Dd],[0,Dd*np.tan(al)],color=ACCENT,lw=1.4)
for d in (-0.35,0.35): ax.plot([0,Dd],[0,Dd*np.tan(al)+d*2],color=ACCENT,lw=0.8,ls="--")
ax.plot([Dd,Dd],[-0.5,3.6],color=INK,lw=3)
ax.annotate("",xy=(Dd+0.5,Dd*np.tan(al)-0.7),xytext=(Dd+0.5,Dd*np.tan(al)+0.7),arrowprops=dict(arrowstyle="<->",lw=0.8)); ax.text(Dd+0.7,Dd*np.tan(al),"s",fontsize=9)
ax.plot(0,0,"^",color=INK,ms=8); ax.text(0.2,-0.5,"instrument axis",fontsize=7)
ax.text(1.8,0.1,"α",fontsize=10,color=ACCENT)
ax.plot([0,Dd],[-0.9,-0.9],color=INK,lw=0.8); ax.text(Dd/2,-1.5,"D (horizontal)",fontsize=8,ha="center")
ax.plot([Dd-1.2,Dd-1.2],[0,Dd*np.tan(al)],color=INK,lw=0.8); ax.text(Dd-2.6,0.7,"V",fontsize=9)
ax.set_xlim(-0.8,Dd+2); ax.set_ylim(-2,3.9)
```

**(c) Mean horizontal angles.** The angles at O are the differences of successive pointings, A to B (AOB), B to C (BOC), and C back to the closing A (COA). The pointings are taken exactly as printed.

*Face left*

$$\begin{gathered}\angle AOB=150^\circ35'20''-0^\circ10'30''=150^\circ24'50''\\ \angle BOC=240^\circ20'30''-150^\circ35'20''=89^\circ45'10''\\ \angle COA=360^\circ+0^\circ05'40''-240^\circ20'30''=119^\circ45'10''\end{gathered}$$

*Face right*

$$\begin{gathered}\angle AOB=330^\circ15'20''-180^\circ50'30''=149^\circ24'50''\\ \angle BOC=360^\circ+60^\circ25'40''-330^\circ15'20''=90^\circ10'20''\\ \angle COA=180^\circ10'40''-60^\circ25'40''=119^\circ45'00''\end{gathered}$$

| Angle | Face left | Face right | Mean |
|---|---|---|---|
| AOB | 150° 24' 50" | 149° 24' 50" | 149° 54' 50" |
| BOC | 89° 45' 10" | 90° 10' 20" | 89° 57' 45" |
| COA | 119° 45' 10" | 119° 45' 00" | 119° 45' 05" |
| Sum | 359° 55' 10" | 359° 20' 10" | 359° 37' 40" |

The three angles round the point should add up to $360^\circ$. The sums above show a closing error of $360^\circ-359^\circ37'40''=+22'20''$. *Note on the data:* the printed face-right reading on A at the start (180°50'30") is $40'$ away from the face-left reading plus $180^\circ$, and the face-left and face-right values of AOB differ by exactly $1^\circ$, so one of these digits seems misprinted in the question. With the data as printed, the error is distributed equally to the three angles ($+7'26.7''$ each):

$$\boxed{\angle AOB=150^\circ02'17'',\quad\angle BOC=90^\circ05'12'',\quad\angle COA=119^\circ52'32''}$$

(sum $360^\circ00'01''$ by rounding). If the intended face-right start on A was $179^\circ50'30''$, the face-right AOB equals the face-left value $150^\circ24'50''$, and the method above applies unchanged to the corrected figures.

@s 5
**(a) Triangulation and trilateration.**

| Triangulation | Trilateration |
|---|---|
| Angles of the triangles are measured; only one side (the base line) and a check base are measured | All the sides are measured; the angles are computed with the cosine rule |
| Precise theodolite | EDM, total station or GNSS |
| Sides computed by the sine rule $b=a\sin B/\sin A$ | Angles by $\cos A=(b^2+c^2-a^2)/2bc$ |
| Needs base-line extension and a long, level, clear base | No base line needed; it is better where long lines can be measured by EDM |
| Check: sum of the angles of each triangle, and the check base | Check: closing of the figure and redundant sides |

**Layouts of triangles (figures) in triangulation.**

1. **Single chain of triangles**: for a long narrow strip (a road, canal, or railway) the quickest and cheapest, but the weakest in checks, since only one path of computation exists.
2. **Chain of quadrilaterals (braced)**: each quadrilateral has both diagonals observed, which gives several independent routes and a strong check; the best layout for a narrow strip needing accuracy.
3. **Chain of polygons with central stations** (hexagon or pentagon with a central point): used for an extensive area, gives many checks, but more observations.
4. **Combination / grid (network)** of quadrilaterals and polygons: covers a wide area; used in national control surveys.

```figure caption="Question 5(a): layouts of triangles: (1) chain of single triangles, (2) braced quadrilaterals, (3) central-point polygon."
fig,axs=plt.subplots(1,3,figsize=(6.4,2.0))
for ax in axs: ax.axis("off")
a,b,c=axs
pts=[(0,0),(1,1.0),(2,0),(3,1.0),(4,0),(5,1.0)]
for i in range(len(pts)-1): a.plot(*zip(pts[i],pts[i+1]),color=INK,lw=1.2)
for i in range(len(pts)-2): a.plot(*zip(pts[i],pts[i+2]),color=INK,lw=1.2)
a.set_title("1  chain of triangles",fontsize=7.5); a.set_xlim(-0.3,5.3); a.set_ylim(-0.3,1.4)
for x0 in (0,2):
    q=[(x0,0),(x0,1.2),(x0+2,1.2),(x0+2,0)]
    for i in range(4): b.plot(*zip(q[i],q[(i+1)%4]),color=INK,lw=1.2)
    b.plot(*zip(q[0],q[2]),color=ACCENT,lw=1); b.plot(*zip(q[1],q[3]),color=ACCENT,lw=1)
b.set_title("2  braced quadrilaterals",fontsize=7.5); b.set_xlim(-0.3,4.3); b.set_ylim(-0.3,1.5)
th=np.linspace(0,2*np.pi,7)[:-1]; P=np.c_[np.cos(th),np.sin(th)]
for i in range(6):
    c.plot(*zip(P[i],P[(i+1)%6]),color=INK,lw=1.2); c.plot(*zip((0,0),P[i]),color=ACCENT,lw=1)
c.plot(0,0,"o",color=INK,ms=4); c.set_title("3  central-point polygon",fontsize=7.5); c.set_xlim(-1.4,1.4); c.set_ylim(-1.3,1.3)
plt.tight_layout()
```

**(b) Mapping and plotting software (QGIS, free and open source, as the example).** QGIS (Quantum GIS) is a free desktop GIS. Alternatives with the same working are Civil 3D, SurvCADD, ArcGIS, or Global Mapper.

*Features.*

- Free, cross-platform; opens survey data (CSV or text of $N,E,Z$ from the total station, GNSS, shapefile, GeoJSON, DXF, raster images, DEM, web maps).
- Handles coordinate reference systems (e.g. UTM 44N/45N, Nepal MUTM) with on-the-fly re-projection.
- Vector layers (points, lines, polygons) with attribute tables, symbology and labels; raster analysis (hillshade, slope, contours from a DEM, TIN interpolation); area and distance measurement.
- Print layouts (title, scale bar, north arrow, legend, grid) giving a finished map in PDF or PNG; plugins for profile tools, georeferencer and field data (QField).

*How it works (survey data to a plotted map).*

1. Create a project and set its coordinate system.
2. Import the survey points (*Add delimited text layer*, X = Easting, Y = Northing, with Z as an attribute) or digitize features over a georeferenced image.
3. Group the features into layers (boundary, building, road, spot heights), edit geometry and attributes.
4. Interpolate the surface (TIN or IDW from the spot heights), and generate contours at a chosen interval.
5. Style the layers with symbols and labels, compose a print layout with the scale, and export a plot or a shapefile or DXF.

**(c) Anallactic stadia (additive constant $C=0$, $k=100$, line of sight inclined, staff vertical).**

Instrument axis $=RL_O+HI=1250.50+1.450=1251.950$ m. The zenith angle $\theta$ gives the vertical angle $\alpha=90^\circ-\theta$. With the staff vertical: $D=ks\sin^2\theta$ and $V=\tfrac12ks\sin2\theta$ (positive when the line of sight is upward, $\theta<90^\circ$), and $RL=RL_{\text{axis}}+V-h$ with $h$ the middle hair reading.

**Staff at P.** $s=2.85-1.35=1.50$ m, $\theta=87^\circ30'$ ($\alpha=+2^\circ30'$):

$$\begin{gathered}D_P=100(1.50)\sin^2(87^\circ30')=149.71\ \text{m} \\ V_P=\tfrac12(100)(1.50)\sin(175^\circ)=+6.54\ \text{m}\end{gathered}$$

$$RL_P=1251.950+6.54-2.10=1256.39\ \text{m}$$

**Staff at Q.** $s=3.795-1.955=1.840$ m, $\theta=92^\circ45'$ ($\alpha=-2^\circ45'$, depression):

$$\begin{gathered}D_Q=100(1.840)\sin^2(92^\circ45')=183.58\ \text{m} \\ V_Q=\tfrac12(100)(1.840)\sin(185^\circ30')=-8.82\ \text{m}\end{gathered}$$

$$RL_Q=1251.950-8.82-2.875=1240.26\ \text{m}$$

(the central hair, 2.875, is the mean of 1.955 and 3.795). **Distance PQ.** The angle at O is $170^\circ45'-60^\circ30'=110^\circ15'$:

$$PQ=\sqrt{D_P^2+D_Q^2-2D_PD_Q\cos110^\circ15'}=\sqrt{149.71^2+183.58^2+2(149.71)(183.58)(0.3502)}=274.12\ \text{m}$$

**Gradient.** $\Delta RL=1240.26-1256.39=-16.13$ m:

$$\boxed{RL_P=1256.39\ \text{m},\ RL_Q=1240.26\ \text{m},\ PQ=274.12\ \text{m},\ \text{gradient}=\frac{16.13}{274.12}=\frac1{17.0}\ (5.9\%\ \text{falling from P to Q})}$$

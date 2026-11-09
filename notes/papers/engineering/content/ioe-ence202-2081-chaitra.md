---
file: NEBians-IOE-Past-Paper-Theory-of-Structures-I-ENCE202-2081-Chaitra.pdf
subject: Theory of Structures I
level: BE · Year II / Part I
code: ENCE 202
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Describe various types of structures based on load transfer mechanism. [[2]]

b) Determine maximum dynamic stress and dynamic deflection in the steel bar of diameter 20 mm and length 2 m caused by a mass of 5 kg falling freely through a distance of 1 m. (i) When rubber compression washer is attached to lower end of rod. (ii) When the rubber washer is removed. Take E = 200 GPa (for steel rod) K = 3 N/mm (For rubber washer) [[8]]

@q 2
A triangular shape truss is loaded as shown in figure below. Using virtual work method, determine vertical deflection at joint D if the member BC is too short by 2.4 mm and AB is too long by 1.8 mm and both member AD and DC are subjected to temperature rise by 10°C, take coefficient of thermal expansion (α) = 12 × 10⁻⁶/°C and AE = 100 × 10³ kN. [[8]]

```figure caption="Question 2: truss with A (pin) at the left end of the bottom chord, D 4 m from A, C (roller) 3 m beyond D; B is 3 m above D. Loads at B: 10 kN downward and 20 kN horizontal (to the right). Members AB, BD, BC, AD, DC."
fig,ax=plt.subplots(figsize=(4.6,2.5)); ax.axis("off")
P={"A":(0,0),"D":(4,0),"C":(7,0),"B":(4,3)}
for a,b in ["AB","BD","BC","AD","DC"]: ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=2.4)
for k,(x,y) in P.items(): ax.text(x,y+(0.25 if y>0 else -0.55),k,ha="center",fontsize=9,fontweight="bold")
ax.annotate("",xy=(4,3.05),xytext=(4,4.0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)); ax.text(4.2,3.7,"10 kN",fontsize=8)
ax.annotate("",xy=(6,3.0),xytext=(4.1,3.0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)); ax.text(5.0,3.2,"20 kN",fontsize=8)
ax.text(2,-0.7,"4.0 m",ha="center",fontsize=8); ax.text(5.5,-0.7,"3.0 m",ha="center",fontsize=8); ax.text(4.3,1.5,"3.0 m",fontsize=8)
ax.set_xlim(-1,8); ax.set_ylim(-1.2,4.4)
```

@q 3
a) Using moment area method, determine slope at B and C and deflection at C for the beam shown in figure below. Take EI constant throughout. [[6]]

```figure caption="Question 3(a): beam ABC, pin at A, roller at B (AB = 2 + 3 = 5 m), overhang BC = 3 m; 10 kN at 2 m from A, 20 kN at C; EI over AB, 2EI over BC (as marked on the scan)."
fig,ax=plt.subplots(figsize=(5.0,1.9)); ax.axis("off")
ax.plot([0,5],[0,0],color=INK,lw=3); ax.plot([5,8],[0,0],color=INK,lw=5); ax.plot([0],[-0.25],"^",color=INK,ms=9); ax.plot([5],[-0.25],"o",mfc="white",mec=INK,ms=9)
ax.annotate("",xy=(2,0.05),xytext=(2,1.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)); ax.text(2,1.2,"10 kN",ha="center",fontsize=8.5)
ax.annotate("",xy=(8,0.05),xytext=(8,1.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)); ax.text(8,1.2,"20 kN",ha="center",fontsize=8.5)
ax.text(1,-0.8,"EI",ha="center",fontsize=9); ax.text(6.5,-0.8,"2EI",ha="center",fontsize=9); ax.text(0,0.35,"A",fontsize=9); ax.text(5,-0.95,"B",ha="center",fontsize=9); ax.text(8.2,0.2,"C",fontsize=9)
ax.set_xlim(-1,9.2); ax.set_ylim(-1.3,1.8)
```

b) Determine slope and vertical deflection at point C for the beam shown in figure below, using conjugate beam method. [[6]]

```figure caption="Question 3(b): beam ABC, pin at A, roller at B (AB = 4 m, rigidity 0.5EI, UDL 10 kN/m), overhang BC = 2 m (rigidity EI) with a 20 kN load at C."
fig,ax=plt.subplots(figsize=(5.0,1.9)); ax.axis("off")
ax.plot([0,4],[0,0],color=INK,lw=2.5); ax.plot([4,6],[0,0],color=INK,lw=4.5); ax.plot([0],[-0.25],"^",color=INK,ms=9); ax.plot([4],[-0.25],"o",mfc="white",mec=INK,ms=9)
for x in np.linspace(0.2,3.8,10): ax.annotate("",xy=(x,0.05),xytext=(x,0.7),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
ax.text(2,0.85,"10 kN/m",ha="center",fontsize=8.5); ax.annotate("",xy=(6,0.05),xytext=(6,1.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)); ax.text(6,1.2,"20 kN",ha="center",fontsize=8.5)
ax.text(2,-0.8,"0.5EI",ha="center",fontsize=9); ax.text(5,-0.8,"EI",ha="center",fontsize=9); ax.text(0,0.35,"A",fontsize=9); ax.text(4,-0.95,"B",ha="center",fontsize=9); ax.text(6.2,0.2,"C",fontsize=9)
ax.set_xlim(-1,7.2); ax.set_ylim(-1.3,1.8)
```

@q 4
a) Using ILD, determine the maximum bending moment at a point at 20 m from right support in a simply supported girder of span 50 m when four concentrated loads of 100 kN, 150 kN, 200 kN and 150 kN each separated from adjacent load by 3 m moving from right to left with 100 kN load leading. Also calculate the maximum moment under 100 kN load in the beam. [[10]]

b) A three hinged parabolic arch has a span of 50 m and a central rise of 6 m. The arch is loaded with uniformly distributed load of 4 kN/m over the left half of the span along with a concentrated load of 20 kN acting vertically at crown. Determine the normal thrust, radial shear and bending moment at 10m from the left support. Draw BMD. [[8]]

@q 5
a) Using line diagrams, show the different components of a suspension cable system. A suspension cable having span 300 m and central dip 25 m supports a three hinged stiffening girder carrying 180 kN at 50m from left support and 120 kN at 40 m from the right support. The dead load of the girder is 5 kN/m. Determine; [[10]]

i) Bending moment and shear force at a section 30m from the left support.

ii) Maximum tension in the cable and inclination

iii) Length of the cable

iv) Draw SFD and BMD for the girder

b) Describe types of supports for space truss. [[2]]

<!-- SOLUTIONS -->

@s 1
**(a) Types of structures by load-transfer mechanism.**

| Type | How the load is carried | Examples |
|---|---|---|
| **Beams** | Transverse load is carried by bending and shear to the supports | floor beams, girders, lintels |
| **Trusses** | Pin-jointed triangulated members carry only axial tension or compression (loads at joints) | roof trusses, bridge trusses, towers |
| **Frames** (rigid-jointed) | Bending, shear and axial force in members connected by moment-resisting joints | building frames, portal frames |
| **Arches** | Load is transferred mainly by compressive thrust along the curved axis, producing horizontal thrust at the supports | masonry and concrete arch bridges, three-hinged arches |
| **Cables and suspension systems** | The flexible cable carries the load by pure tension (funicular shape); the stiffening girder shares the live load | suspension bridges, cable roofs |
| **Plates and shells** | Two-way slab action or membrane forces in a curved surface | slabs, domes, tanks, folded plates |
| **Space (3-D) structures** | Axial forces in three-dimensional trusses or space frames | transmission towers, domes, space-frame roofs |

Structures are also classified as **statically determinate** or **indeterminate**, depending on whether they can be analysed by equilibrium alone.

**(b) Impact on a vertical steel bar.** $d=20$ mm, $A=\dfrac\pi4(20)^2=314.16$ mm², $L=2000$ mm, $E=200\times10^3$ N/mm², $W=mg=5(9.81)=49.05$ N, fall height $h=1000$ mm. Stiffness of the bar: $k_r=\dfrac{AE}{L}=\dfrac{314.16(200\,000)}{2000}=31\,416$ N/mm.

The energy balance (loss of potential energy = strain energy in the spring system of stiffness $k$) is $W(h+\delta)=\tfrac12k\delta^2$, whose positive root is

$$\delta=\frac{W}{k}\left[1+\sqrt{1+\frac{2hk}{W}}\right]$$

**(ii) Without the rubber washer** ($k=k_r=31\,416$ N/mm): $\delta_{st}=W/k=0.001561$ mm, $\dfrac{2hk}{W}=1.281\times10^{6}$:

$$\delta=0.001561\left[1+\sqrt{1+1.281\times10^{6}}\right]=0.001561(1+1131.8)=1.769\ \text{mm}$$

$$\begin{gathered}P_{max}=k_r\delta=55.56\ \text{kN} \\ \boxed{\sigma_{max}=\frac{P}{A}=\frac{55\,564}{314.16}=176.9\ \text{N/mm}^2}\end{gathered}$$

$$\boxed{\text{dynamic deflection (elongation of the bar)}=1.77\ \text{mm}},\quad IF=\frac{\delta}{\delta_{st}}=1133$$

**(i) With the rubber washer** at the lower end (it acts as a spring of $K=3$ N/mm in series with the bar):

$$\frac1k=\frac1{31\,416}+\frac1{3}\ \Rightarrow\ k=2.9997\ \text{N/mm}$$

$$\begin{gathered}\delta_{st}=\frac{49.05}{2.9997}=16.35\ \text{mm} \\ \frac{2hk}{W}=122.3\end{gathered}$$

$$\delta_{total}=16.35\left[1+\sqrt{1+122.3}\right]=16.35(12.10)=197.9\ \text{mm}$$

Almost all of this compression takes place in the rubber washer. The maximum load is $P_{max}=k\delta=2.9997(197.9)=593.7$ N, so

$$\begin{gathered}\boxed{\sigma_{max}=\frac{593.7}{314.16}=1.89\ \text{N/mm}^2} \\ \boxed{\delta_{bar}=\frac{P_{max}}{k_r}=\frac{593.7}{31\,416}=0.0189\ \text{mm}}\end{gathered}$$

(the washer compresses by $593.7/3=197.9$ mm). The washer reduces the impact stress in the rod from 176.9 to 1.89 N/mm², a factor of about 94, because it makes the system much more flexible and absorbs the energy.

@s 2
**Truss with lack of fit and temperature** (virtual work, unit vertical load at D). Reactions under the real load (10 kN downward and 20 kN to the right at B): $\sum M_A=0$: $V_C(7)=10(4)+20(3)=100\Rightarrow V_C=14.286$ kN; $V_A=10-14.286=-4.286$ kN (downward); $H_A=-20$ kN.

Lengths: $AB=5.0$ m, $BD=3.0$ m, $BC=\sqrt{3^2+3^2}=4.243$ m, $AD=4.0$ m, $DC=3.0$ m. Member forces $F$ (kN, tension +) under the real loads and $u$ for a downward unit load at D (method of joints):

| Member | $L$ (m) | $F$ (kN) | $u$ | $\dfrac{FuL}{AE}$ (mm) | fit (mm) | temp (mm) |
|---|---|---|---|---|---|---|
| AB | 5.000 | +7.143 | −0.7143 | −0.2551 | −1.2857 | – |
| BD | 3.000 | 0 | +1.0000 | 0 | – | – |
| BC | 4.243 | −20.203 | −0.8081 | +0.6926 | +1.9394 | – |
| AD | 4.000 | +14.286 | +0.5714 | +0.3265 | – | +0.2743 |
| DC | 3.000 | +14.286 | +0.5714 | +0.2449 | – | +0.2057 |
| **Σ** | | | | **+1.0090** | **+0.6537** | **+0.4800** |

(Fit column = $u\,\Delta L$ for the lack of fit and temp column = $u\,\alpha\,\Delta T\,L$; $\dfrac{FuL}{AE}$ in mm is $\dfrac{F\,u\,L}{100\,000}\times1000$; thermal elongation $\alpha\Delta TL=12\times10^{-6}(10)L$: 0.48 mm for AD and 0.36 mm for DC; BC is too short, so $\Delta L=-2.4$ mm, and AB is too long, so $\Delta L=+1.8$ mm.)

$$\Delta_{D}=\sum\frac{FuL}{AE}+\sum u\,\Delta L_{fit}+\sum u\,\alpha\Delta T\,L=1.009+0.654+0.480$$

$$\boxed{\Delta_{D}\approx2.14\ \text{mm downward}}$$

@s 3
**(a) Moment-area method.** *Reactions* (moments about A): $R_B=\dfrac{10(2)+20(8)}{5}=36$ kN, $R_A=30-36=-6$ kN (downward). *Bending moments:* $M_A=0$, $M(2)=-6(2)=-12$ kN·m, $M_B=-6(5)-10(3)=-60$ kN·m, $M_C=0$ (hogging throughout; the diagram on BC is a triangle).

*$M/EI$ areas* (EI over AB, 2EI over BC; units kN·m²/EI):

| Segment | Shape | Area | Centroid |
|---|---|---|---|
| A–2 m | triangle, peak $-12$ | $\tfrac12(2)(12)=-12$ | $\tfrac23(2)=1.333$ m from A |
| 2–5 m (3 m) | trapezoid $-12\to-60$ | $-\tfrac{12+60}2(3)=-108$ | from the 2 m point: split: rectangle $-36$ at 1.5, triangle $-72$ at 2.0 |
| B–C (3 m) | triangle $-60/2$ | $-\tfrac12(3)(30)=-45$ | $1$ m from B |

*Slope at B.* With $y_A=y_B=0$, the deviation of A from the tangent at B is $t_{A/B}$ = the moment of the $M/EI$ areas of AB about A:

$$t_{A/B}=-12(1.333)-36(3.5)-72(4.0)=-430/EI$$

so the tangent at B passes $430/EI$ above A, and $\theta_B=\dfrac{t_{A/B}}{5}$:

$$\boxed{\theta_B=-\frac{86}{EI}\ \text{(clockwise)}}$$

*Slope at A:* $\theta_A=\theta_B-\text{area}_{AB}=-86+120=+\dfrac{34}{EI}$ (counter-clockwise). *Slope at C:* $\theta_C=\theta_B+\text{area}_{BC}$:

$$\boxed{\theta_C=\frac{-86-45}{EI}=-\frac{131}{EI}\ \text{(clockwise)}}$$

*Deflection at C.* Relative to the tangent at B, C deviates by $t_{C/B}=45\times2=90/EI$ (the area of BC acts 2 m from C) *below* it (hogging). The tangent itself falls $86(3)=258/EI$ over BC:

$$\boxed{\Delta_C=\frac{258+90}{EI}=\frac{348}{EI}\ \text{downward}}$$

(Here $EI$ is the rigidity of AB; the moment-diagram ordinates of BC were divided by $2EI$ already. The scan prints "EI constant" in the question but marks EI and 2EI on the figure; the figure was followed.)

**(b) Conjugate beam method.** *Reactions:* load on AB is $10(4)=40$ kN at 2 m; $R_B=\dfrac{40(2)+20(6)}{4}=50$ kN, $R_A=60-50=10$ kN. *Bending moments:* on AB, $M=10x-5x^2$ ($M_B=-40$ kN·m); on BC, $M=-20s$ ($s$ measured from C, $M_B=-40$).

*Conjugate beam.* The real pin A stays a pin, the interior roller B becomes an internal hinge B′, and the free end C becomes a fixed end C′; the conjugate load is $M/EI$ with $0.5EI$ on AB and $EI$ on BC.

- *Span AB:* $\dfrac{M}{0.5EI}=\dfrac{2(10x-5x^2)}{EI}$. Area $=2\left(5(16)-\dfrac{5(64)}3\right)=-53.33$; moment about A $=2\left(\dfrac{10(64)}3-\dfrac{5(256)}4\right)=-213.3$. Moments about the hinge: $R'_A(4)=-53.33(4)+213.3=0$, so $R'_A=0$ and the force at the hinge is $R'_B=-53.33$.
- *Overhang BC (cantilever fixed at C′):* $\dfrac M{EI}=-\dfrac{20s}{EI}$, a triangle with area $\tfrac12(2)(40)=-40$ and centroid $1.333$ m from C.

$$\begin{gathered}\theta_A=V'_A=0 \\ \theta_B=-\frac{53.33}{EI}\ (\text{clockwise})\end{gathered}$$

$$\begin{gathered}\theta_C=V'_C=\frac{-53.33-40}{EI}=-\frac{93.3}{EI} \\ \Delta_C=M'_C=\frac{-53.33(2)-40(1.333)}{EI}=-\frac{160}{EI}\end{gathered}$$

$$\boxed{\theta_C=\frac{93.3}{EI}\ \text{(clockwise)},\qquad \Delta_C=\frac{160}{EI}\ \text{downward}}$$

(the rigidity $EI$ is that of BC; the end slopes: $\theta_A=0$ and $\theta_B=53.3/EI$ clockwise).

@s 4
**(a) Moving loads on the 50 m girder** (loads 100, 150, 200, 150 kN at 3 m spacing, total $W=600$ kN; moving from right to left, with the 100 kN load leading, i.e. 100 kN is the left-most load). The section is 20 m from the right support, i.e. at $a=30$ m from the left support A.

*Influence line for the bending moment at the section X* ($a=30$ m, $b=20$ m): the ordinate under the section is $\dfrac{ab}{L}=\dfrac{30(20)}{50}=12$ m, the ILD is a triangle with ordinates falling linearly to zero at both supports:

$$\begin{gathered}y(x)=\frac{x(50-30)}{50}=0.4x\ \ (x\le30) \\ y(x)=\frac{30(50-x)}{50}=0.6(50-x)\ \ (x\ge30)\end{gathered}$$

*Criterion for the position:* a load is placed at the section so that the sign of $\dfrac{W_{left}}{a}-\dfrac{W}{L}$ changes as the load crosses the section, with $\dfrac WL=\dfrac{600}{50}=12$ kN/m. Place the **200 kN load at the section** (30 m): the loads lie at 24 m (100 kN), 27 m (150 kN), 30 m (200 kN) and 33 m (150 kN). With the 200 kN load counted on the left of the section, $\dfrac{450}{30}=15>12$; with it counted on the right, $\dfrac{250}{30}=8.33<12$, so the sign changes ✔.

$$M_{max}=\sum P\,y=100(0.4\times24)+150(0.4\times27)+200(12)+150(0.6\times17)$$

$$=960+1620+2400+1530=\boxed{6510\ \text{kN·m}}$$

(this position was verified numerically by trying all positions of the train: 6510 kN·m is the largest value at the section.)

*Maximum bending moment under the 100 kN load.* The maximum moment under a given load occurs when that load and the centre of gravity of the loads on the span are equidistant from the mid-span. Centre of gravity from the 100 kN load: $\bar x=\dfrac{150(3)+200(6)+150(9)}{600}=5.0$ m. So the 100 kN load is placed $\dfrac{5.0}{2}=2.5$ m to the left of the centre, i.e. at $x=22.5$ m from A (the 150, 200 and 150 kN loads at 25.5, 28.5 and 31.5 m, all on the girder):

$$R_A=\frac{600(50-27.5)}{50}=270\ \text{kN}$$

$$\boxed{M_{100}=270(22.5)=6075\ \text{kN·m}}$$

(under the 100 kN load, 22.5 m from the left, i.e. 27.5 m from the right support; the load order was taken as in the question, with the 100 kN load leading on the left. For information, the absolute maximum of the whole train, 6753 kN·m, occurs under the 200 kN load at 25.5 m from A.)

**(b) Three-hinged parabolic arch** ($L=50$ m, $h=6$ m): $y=\dfrac{4h}{L^2}x(L-x)=\dfrac{24x(50-x)}{2500}$, slope $\tan\theta=\dfrac{24(50-2x)}{2500}$.

*Loads:* UDL $4\times25=100$ kN on the left half (centroid 12.5 m from A) and 20 kN at the crown.

*Reactions:* $V_B=\dfrac{100(12.5)+20(25)}{50}=35$ kN, $V_A=120-35=85$ kN. The moment at the crown hinge is zero (right side): $V_B(25)-H(6)=0$:

$$H=\frac{35(25)}{6}=145.83\ \text{kN}$$

*Section at $x=10$ m:* $y=\dfrac{24(10)(40)}{2500}=3.84$ m, $\tan\theta=\dfrac{24(30)}{2500}=0.288$, $\theta=16.07^\circ$, $\cos\theta=0.9609$, $\sin\theta=0.2767$. Beam shear $V=85-4(10)=45$ kN.

$$\boxed{M=85(10)-4\frac{10^2}{2}-145.83(3.84)=850-200-560=90.0\ \text{kN·m}}$$

$$\boxed{Q=V\cos\theta-H\sin\theta=45(0.9609)-145.83(0.2767)=2.88\ \text{kN (radial shear)}}$$

$$\boxed{N=V\sin\theta+H\cos\theta=45(0.2767)+145.83(0.9609)=152.6\ \text{kN (normal thrust)}}$$

*BMD:* $M(x)=V_Ax-(\text{load to the left of }x)-Hy$: 0 (A), 60.0 (5 m), 90.0 (10 m), 90.0 (15 m), 60.0 (20 m), 0 (crown, 25 m), −140 (30 m), −210 (35 m), −210 (40 m), −140 (45 m), 0 (B) kN·m.

```figure caption="BMD of the three-hinged arch of Q4(b): maximum sagging moment 90 kN·m at 10–15 m from A, zero at the hinges, maximum hogging moment −210 kN·m between 35 m and 40 m."
x=np.linspace(0,50,501); VA,H=85,145.8333
M=VA*x-np.where(x<=25,4*x**2/2,100*(x-12.5))-np.where(x>25,20*(x-25),0)-H*24*x*(50-x)/2500
fig,ax=plt.subplots(figsize=(5.4,2.5)); ax.fill_between(x,0,M,where=M>=0,color=ACCENT,alpha=0.25); ax.fill_between(x,0,M,where=M<0,color="#d9534f",alpha=0.25)
ax.plot(x,M,color=INK,lw=1.6); ax.axhline(0,color=INK,lw=0.9)
for xx,t,o in [(12.5,"90",6),(37.5,"−210",-12)]: ax.annotate(t,(xx,np.interp(xx,x,M)),textcoords="offset points",xytext=(0,o),ha="center",fontsize=8)
ax.set_xlabel("distance from left support (m)",fontsize=8.5); ax.set_ylabel("M (kN·m)",fontsize=8.5); ax.tick_params(labelsize=7.5); ax.grid(True,color=GRID,lw=0.5)
```

@s 5
**(a) Components of a suspension cable system.** A suspension system consists of (1) the **main cable** (flexible, in tension, hanging between the two towers in a parabola for a UDL), (2) the **towers** (compression, supporting the cable at its saddles), (3) the **hangers (suspenders)** (vertical ties transferring the girder load to the cable), (4) the **stiffening girder** (here three-hinged, which carries the live load and limits the deformation) and (5) the **anchorages and back-stays** (ground anchors that take the horizontal and vertical components of the cable pull).

```figure caption="Line diagram of a suspension cable system: cable (parabola), towers, hangers, stiffening girder with a central hinge, back-stays and anchorages."
fig,ax=plt.subplots(figsize=(5.8,2.4)); ax.axis("off")
x=np.linspace(0,10,100); cab=4-0.04*(x-5)**2*4/1+0.0
ax.plot(x,4-(1-(x-5)**2/25)*0-0.0+(0.14*(x-5)**2-3.5)+3.5-0.0,color=ACCENT,lw=0)
cab=1+3.0*((x-5)/5)**2; ax.plot(x,cab,color=ACCENT,lw=2.2); ax.plot([0,10],[0.6,0.6],color=INK,lw=3)
for xx in np.linspace(0.6,9.4,12): ax.plot([xx,xx],[0.6,1+3.0*((xx-5)/5)**2],color=MUTED,lw=0.8)
for xx in (0,10): ax.plot([xx,xx],[0,4.4],color=INK,lw=3)
ax.plot([0,-1.5],[4,1.2],color=ACCENT,lw=1.6); ax.plot([10,11.5],[4,1.2],color=ACCENT,lw=1.6); ax.plot([-1.5],[1.2],"s",color=INK,ms=8); ax.plot([11.5],[1.2],"s",color=INK,ms=8)
ax.plot([5],[0.6],"o",mfc="white",mec=INK,ms=7); ax.text(5.15,0.25,"central hinge",fontsize=7.5); ax.text(5,1.2,"cable",fontsize=8,color=ACCENT,ha="center"); ax.text(2.2,2.7,"hangers",fontsize=7.5,color=MUTED)
ax.text(0.1,4.5,"tower",fontsize=8); ax.text(-1.8,0.6,"anchorage",fontsize=7.5); ax.text(5,-0.25,"stiffening girder (three-hinged)",ha="center",fontsize=8)
ax.set_xlim(-2.6,12.6); ax.set_ylim(-0.6,5)
```

*Data:* $L=300$ m, $d=25$ m, dead load of the girder $w=5$ kN/m (carried by the cable); live loads 180 kN at 50 m from A and 120 kN at 40 m from B (260 m from A).

*Dead-load horizontal pull:* $H_d=\dfrac{wL^2}{8d}=\dfrac{5(300)^2}{8(25)}=2250$ kN. *Live-load reactions (simple beam):* $V_A=\dfrac{180(250)+120(40)}{300}=166$ kN, $V_B=134$ kN. The moment at the central hinge is zero:

$$\begin{gathered}H_p=\frac{V_A(150)-180(100)}{25}=\frac{24\,900-18\,000}{25}=276\ \text{kN} \\ H=2250+276=2526\ \text{kN}\end{gathered}$$

**(i) Section 30 m from the left support.** The cable ordinate is $y=\dfrac{4(25)(30)(270)}{300^2}=9.0$ m and the slope $\tan\theta=\dfrac{4(25)(300-60)}{300^2}=0.2667$. Under the dead load the girder carries no bending moment, so only the live load acts on the girder:

$$\boxed{M=V_A(30)-H_py=166(30)-276(9.0)=4980-2484=2496\ \text{kN·m}}$$

$$\boxed{V=V_A-H_p\tan\theta=166-276(0.2667)=92.4\ \text{kN}}$$

**(ii) Maximum tension and inclination.** The maximum tension occurs at the support where the vertical component is greater (the left one, with $V_A$ larger): vertical component $=5(150)+166=916$ kN:

$$\begin{gathered}\boxed{T_{max}=\sqrt{H^2+V^2}=\sqrt{2526^2+916^2}=2687\ \text{kN}} \\ \boxed{\alpha=\tan^{-1}\frac{916}{2526}=19.93^\circ}\end{gathered}$$

(the tension at the right support is $\sqrt{2526^2+884^2}=2676$ kN).

**(iii) Length of the cable** (a parabola, with $d/L=1/12$):

$$\ell_c=L\left[1+\frac83\left(\frac dL\right)^2-\frac{32}5\left(\frac dL\right)^4\right]=300\left[1+0.018519-0.000309\right]\ \Rightarrow\ \boxed{\ell_c\approx305.5\ \text{m}}$$

**(iv) SFD and BMD of the girder** (live load only; $M=M_{beam}-H_py$, $V=V_{beam}-H_p\tan\theta$):

| $x$ (m) | 0 | 30 | 50 | 100 | 150 | 200 | 250 | 260 | 300 |
|---|---|---|---|---|---|---|---|---|---|
| $M$ (kN·m) | 0 | 2496 | 4467 | 1467 | 0 (hinge) | 67 | 1667 | 2171 | 0 |

Shear force just left/right of the points: at A, $+74.0$; just left of 50 m, $+104.6$ kN; just right of 50 m, $-75.4$ kN; at 150 m, $-14.0$ kN; just left of 260 m, $+53.4$ kN; just right of 260 m, $-66.5$ kN; at B, $-42.0$ kN.

```figure caption="SFD and BMD of the stiffening girder of Q5(a) (live load only): BM maximum 4467 kN·m under the 180 kN load; BM is zero at the central hinge."
x=np.linspace(0,300,3001); VA,Hp=166,276; yf=4*25*x*(300-x)/300**2; sl=4*25*(300-2*x)/300**2
M=VA*x-np.where(x>50,180*(x-50),0)-np.where(x>260,120*(x-260),0)-Hp*yf
V=VA-np.where(x>50,180,0)-np.where(x>260,120,0)-Hp*sl
fig,axs=plt.subplots(2,1,figsize=(5.6,3.9),sharex=True)
axs[0].fill_between(x,0,V,color=ACCENT,alpha=0.25); axs[0].plot(x,V,color=INK,lw=1.3); axs[0].axhline(0,color=INK,lw=0.8); axs[0].set_ylabel("SF (kN)",fontsize=8.5)
axs[1].fill_between(x,0,M,color="#d9534f",alpha=0.25); axs[1].plot(x,M,color=INK,lw=1.3); axs[1].axhline(0,color=INK,lw=0.8); axs[1].set_ylabel("BM (kN·m)",fontsize=8.5); axs[1].set_xlabel("distance from left support (m)",fontsize=8.5)
axs[1].annotate("4467",(50,4467),textcoords="offset points",xytext=(14,-4),fontsize=8)
for a in axs: a.grid(True,color=GRID,lw=0.5); a.tick_params(labelsize=7.5)
fig.tight_layout()
```

**(b) Supports for a space truss.** Because the joints of a space truss are ball-and-socket (they carry no moment), the supports can only provide force reactions. Typical supports are:

1. **Ball-and-socket (spherical) support:** prevents translation in all three directions, with three reaction components ($R_x,R_y,R_z$).
2. **Roller (slotted-roller or ball on a smooth plane) support:** prevents translation normal to the supporting surface and in one other direction (the surface being rough in one direction), so two reaction components; if it is free in the plane, it provides one reaction (normal to the surface).
3. **Link (short-link, rocker) support:** a member pinned at both ends, with one reaction component acting along the axis of the link.

Overall, at least **six independent reaction components** are needed to hold a space truss in stable equilibrium (three force and three moment equilibrium equations); e.g. one ball-and-socket (3), one two-component roller (2) and one link (1).

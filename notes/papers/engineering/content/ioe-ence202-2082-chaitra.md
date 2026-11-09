---
file: NEBians-IOE-Past-Paper-Theory-of-Structures-I-ENCE202-2082-Chaitra.pdf
subject: Theory of Structures I
level: BE · Year II / Part I
code: ENCE 202
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Mention the necessity of structural idealization with an example. [[3]]

b) Define impact factor. A block of weight 'W' is dropped from a height 'h' at the center of a simply supported beam of length ℓ and cross section b × d (width × depth). Derive the expression for the impact factor. [[4]]

@q 2
a) Determine vertical deflection and rotation at free end of given cantilever frame shown in figure below using virtual work method. [[6]]

```figure caption="Question 2(a): cantilever frame fixed at the bottom of the left column (2EI, 5 m = 4 m + 1 m, with a 100 kN horizontal load 4 m above the base), beam of 6 m (EI) carrying 60 kN/m, and a 3 m right column (1.5EI) whose lower end is the free end."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.0)); ax.axis("off")
ax.plot([0,0],[0,5],color=INK,lw=3); ax.plot([0,6],[5,5],color=INK,lw=3); ax.plot([6,6],[5,2],color=INK,lw=3)
ax.add_patch(mp.Rectangle((-0.5,-0.3),1,0.3,fc="#999",ec=INK,hatch="///"))
for x in np.linspace(0.3,5.7,9): ax.annotate("",xy=(x,5.05),xytext=(x,5.8),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1))
ax.text(3,6.0,"60 kN/m",ha="center",fontsize=9); ax.annotate("",xy=(-0.05,4),xytext=(-1.2,4),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.6)); ax.text(-1.3,4.25,"100 kN",ha="center",fontsize=8.5)
ax.text(0.2,2.3,"2EI",fontsize=9); ax.text(3,4.55,"EI",fontsize=9,ha="center"); ax.text(6.2,3.4,"1.5EI",fontsize=9); ax.plot([6],[2],"o",color="#d9534f"); ax.text(6.2,1.8,"free end",fontsize=8)
ax.text(-0.3,4.5,"1 m",fontsize=7.5,ha="right"); ax.text(-0.3,1.8,"4 m",fontsize=7.5,ha="right"); ax.text(3,-0.6,"6 m",ha="center",fontsize=8.5); ax.text(6.9,3.5,"3 m",fontsize=7.5)
ax.set_xlim(-2.5,8); ax.set_ylim(-1,6.6)
```

b) For given truss as shown in figure below, determine vertical deflection at joint E. The cross sectional area of inclined members is 250 mm² and rest members are 500 mm². Also, member BE is too short by 3.0 mm. Take, E = 210 GPa. [[7]]

```figure caption="Question 2(b): truss with joints A, F, E, D on the bottom chord (4 m panels), B and C on the top chord (4 m high); 25 kN downward loads at F and E; pin at A and roller at D. Members: AB, AF, BF, BC, BE, FE, CE, CD, ED."
fig,ax=plt.subplots(figsize=(5.0,2.4)); ax.axis("off")
P={"A":(0,0),"F":(4,0),"E":(8,0),"D":(12,0),"B":(4,4),"C":(8,4)}
for a,b in ["AB","AF","BF","BC","BE","FE","CE","CD","ED"]: ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=2.2)
for k,(x,y) in P.items(): ax.text(x,y+(0.35 if y>0 else -0.7),k,ha="center",fontsize=9,fontweight="bold")
for k in "FE": ax.annotate("",xy=(P[k][0],-0.05),xytext=(P[k][0],-1.5),arrowprops=dict(arrowstyle="<|-",color="#d9534f",lw=1.5)); ax.text(P[k][0]+0.2,-1.6,"25 kN",fontsize=8)
ax.set_xlim(-1,13); ax.set_ylim(-2.2,5)
```

@q 3
a) A propped cantilever beam ABC of length 14 m with internal hinge at B is given in figure below. An external counter-clockwise moment of 100 kNm is acting at support C. Using conjugate beam method, determine deflection at B and slopes at the left and right of B in terms of EI. Consider uniform rigidity (EI) of the beam. [[5]]

```figure caption="Question 3(a): beam fixed at A, internal hinge at B (AB = 6 m, BC = 8 m), roller at C with a counter-clockwise moment of 100 kN·m."
fig,ax=plt.subplots(figsize=(4.8,1.6)); ax.axis("off")
ax.plot([0,14],[0,0],color=INK,lw=3); ax.plot([0,0],[-0.8,0.8],color=INK,lw=4); ax.plot([6],[0],"o",mfc="white",mec=INK,ms=8); ax.plot([14],[-0.25],"^",color=INK,ms=9)
ax.text(0,0.9,"A",fontsize=9); ax.text(6,0.5,"B",ha="center",fontsize=9); ax.text(14.3,0.4,"C",fontsize=9)
th=np.linspace(0.3*np.pi,1.7*np.pi,50); ax.plot(14+1.3*np.cos(th)*0.7+0.0,1.0*np.sin(th)*0.8+0.2,color="#d9534f",lw=1.5); ax.text(15.8,0.3,"100 kN·m",fontsize=8)
ax.text(3,-0.9,"6 m",ha="center",fontsize=8); ax.text(10,-0.9,"8 m",ha="center",fontsize=8); ax.set_xlim(-1,19); ax.set_ylim(-1.3,1.6)
```

b) Determine the slope and vertical deflection at point C for the beam shown in figure below using conjugate beam method. Take EI constant throughout. [[5]]

```figure caption="Question 3(b): beam ABC, pin at A, roller at B (AB = 6 m), overhang BC = 3 m; load rising from zero at A to 10 kN/m at B on AB and 5 kN/m on BC."
fig,ax=plt.subplots(figsize=(4.8,1.9)); ax.axis("off")
ax.plot([0,9],[0,0],color=INK,lw=3); ax.plot([0],[-0.25],"^",color=INK,ms=9); ax.plot([6],[-0.25],"o",mfc="white",mec=INK,ms=9)
ax.fill([0,6,6],[0,0,1.6],color="#cfe3f5",ec=ACCENT); ax.fill([6,9,9,6],[0,0,0.8,0.8],color="#cfe3f5",ec=ACCENT)
ax.text(3.5,1.6,"10 kN/m",fontsize=8.5); ax.text(7.5,1.0,"5 kN/m",ha="center",fontsize=8.5)
ax.text(0,0.4,"A",fontsize=9); ax.text(6,-0.9,"B",ha="center",fontsize=9); ax.text(9.2,0.2,"C",fontsize=9)
ax.text(3,-0.9,"6 m",ha="center",fontsize=8); ax.text(7.5,-0.9,"3 m",ha="center",fontsize=8); ax.set_xlim(-1,10.5); ax.set_ylim(-1.3,2.1)
```

@q 4
a) A train of moving load as shown in figure below crosses a beam girder of span 60 m from left to right. Determine maximum bending moment at 15 m from left support. Also determine absolute maximum bending moment in beam girder. [[6]]

```figure caption="Question 4(a): train of loads 100 kN, 120 kN, 160 kN and 80 kN at spacings 0.8 m, 2 m and 1.2 m crossing a girder of span 60 m from left to right (the 80 kN load leads); section C is 15 m from the left support A."
fig,ax=plt.subplots(figsize=(5.4,1.9)); ax.axis("off")
xs=[0,0.8,2.8,4.0]; Ps=[100,120,160,80]
for x,P in zip(xs,Ps): ax.annotate("",xy=(x,0.05),xytext=(x,1.0),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.5)); ax.text(x,1.1,f"{P} kN",ha="center",fontsize=7.5)
ax.plot([-0.5,4.5],[0,0],color=INK,lw=1)
ax.plot([-2,18],[-1.4,-1.4],color=INK,lw=3); ax.text(-2,-1.1,"A",fontsize=9); ax.text(18,-1.1,"B",fontsize=9); ax.plot([7],[-1.4],"o",color="#d9534f"); ax.text(7,-1.1,"C",ha="center",fontsize=9)
ax.text(0.4,0.3,"0.8",fontsize=7); ax.text(1.8,0.3,"2",fontsize=7); ax.text(3.4,0.3,"1.2",fontsize=7); ax.text(3,-2.0,"(span 60 m, C at 15 m from A; drawing not to scale)",fontsize=7.5,ha="center")
ax.set_xlim(-3,19); ax.set_ylim(-2.3,1.7)
```

b) Determine the maximum forces in the members U₃U₄, U₃L₃ and L₂L₃ in the following deck type truss bridge if UDL of 60 kN/m longer than the span traverses from left to right in the bridge. [[6]]

```figure caption="Question 4(b): deck-type Warren truss bridge, 4 panels at 5 m, 60° diagonals; top-chord joints U1–U5, bottom-chord joints L1–L4 (read from the scan as equilateral triangles with the supports at the end joints U1 and U5)."
fig,ax=plt.subplots(figsize=(5.2,1.9)); ax.axis("off"); h=4.3301
U=[(5*i,h) for i in range(5)]; Lw=[(2.5+5*i,0) for i in range(4)]
for i in range(4): ax.plot([U[i][0],U[i+1][0]],[h,h],color=INK,lw=2.4)
for i in range(3): ax.plot([Lw[i][0],Lw[i+1][0]],[0,0],color=INK,lw=2.4)
for i in range(4): ax.plot([U[i][0],Lw[i][0]],[h,0],color=INK,lw=1.6); ax.plot([Lw[i][0],U[i+1][0]],[0,h],color=INK,lw=1.6)
for i,(x,y) in enumerate(U): ax.text(x,y+0.3,f"U$_{i+1}$",ha="center",fontsize=8.5)
for i,(x,y) in enumerate(Lw): ax.text(x,-0.9,f"L$_{i+1}$",ha="center",fontsize=8.5)
ax.plot([0],[h+0.0],"^",color=INK,ms=1); ax.text(10,h+1.3,"4 @ 5 m",ha="center",fontsize=8.5); ax.set_xlim(-1,21); ax.set_ylim(-1.5,6.3)
```

@q 5
A three-hinged parabolic arch, hinged at both supports and at the crown, has a span of 24 m and a central rise of 4 m. The arch carries a concentrated load of 75 kN acting at a distance of 18 m from the right support, and a UDL of 45 kN/m over the left half of the span. Determine bending moment, normal thrust and radial shear at a section 6 m from the left support. Also draw BMD of given arch. [[8]]

@q 6
a) A 90 m long suspension bridge is supported on two three-hinged stiffening girders hanging by two cables with a central dip of 10 m. Bridge's dead load is 16 kN/m uniformly distributed over the whole span. It carries two-point loads of 250 kN and 300 kN at the distance of 30 m and 60 m from the left end. Find the maximum and minimum tensions in the cable. Also, determine the shear force and bending moment in the girder at 40 m from the left support. [[7]]

b) Describe the procedure to solve space truss by tension coefficient method. [[3]]

<!-- SOLUTIONS -->

@s 1
**(a) Necessity of structural idealization.** A real structure is far too complex to analyse exactly: members have finite width, joints have a finite size and stiffness, supports are never perfectly rigid, loads are distributed in a complicated way, and materials are neither perfectly elastic nor homogeneous. *Structural idealization* replaces the real structure by a simplified **analytical (mathematical) model** whose behaviour is close enough to the real one and which can be analysed with the available theory. It is necessary because:

1. it makes the analysis possible and economical (a few degrees of freedom instead of an infinite number);
2. it allows the use of standard methods (equilibrium, virtual work, slope-deflection etc.) and of computer programs;
3. it makes the design reproducible and focuses on the main load-carrying behaviour; the errors are covered by safety factors.

*Idealizations used:* members are represented by their centroidal axes (lines); supports by a roller, pin or fixed support; joints as pinned or rigid; loads as point loads, UDL or UVL; material as linear elastic; small deformations; 3-D structures as plane frames.

*Example.* A beam-and-column building frame is replaced by a plane frame of lines with fixed bases; the roof slab load is converted into a UDL on the beam; a steel-truss bridge is idealized as a pin-jointed truss with loads acting only at the joints, so that each member carries axial force only. A simply supported bridge girder with a bearing at each end is idealized by a pin at one end and a roller at the other.

**(b) Impact factor.** The impact factor is the ratio of the maximum dynamic (impact) deflection (or stress) to the deflection (or stress) caused by the same load applied statically:

$$IF=\frac{\delta_{dyn}}{\delta_{st}}=\frac{\sigma_{dyn}}{\sigma_{st}}$$

*Derivation.* The weight $W$ falls through the height $h$ and strikes the centre of the beam, which deflects $\delta$ (the maximum dynamic deflection). The beam behaves as a linear spring, so the equivalent static force is $P=k\delta$ with stiffness $k=W/\delta_{st}$. Energy balance (the loss of potential energy of the block equals the strain energy stored in the beam):

$$W(h+\delta)=\frac12P\delta=\frac12\frac{W}{\delta_{st}}\delta^2\ \Rightarrow\ \delta^2-2\delta_{st}\delta-2h\delta_{st}=0$$

$$\delta=\delta_{st}\left[1+\sqrt{1+\frac{2h}{\delta_{st}}}\right]\ \Rightarrow\ \boxed{IF=1+\sqrt{1+\frac{2h}{\delta_{st}}}}$$

For a simply supported beam with a central load, $\delta_{st}=\dfrac{W\ell^3}{48EI}$ and $I=\dfrac{bd^3}{12}$, so $\delta_{st}=\dfrac{W\ell^3}{4Ebd^3}$ and

$$\boxed{IF=1+\sqrt{1+\frac{96EIh}{W\ell^3}}=1+\sqrt{1+\frac{8Ebd^3h}{W\ell^3}}}$$

For $h=0$ (sudden load) $IF=2$.

@s 2
**(a) Virtual work (unit load method).** Axial and shear deformations are neglected, so $\Delta=\sum\int\dfrac{Mm}{EI}ds$. Take the free end as the lower end of the 3 m column. A moment is taken positive when it is clockwise as seen from the load, i.e. all bending moments of the actual loads have the same sense.

*Actual bending moments $M$:* right column (no load on it): $M=0$. Beam, at a distance $x'$ from the right corner: $M=60x'^2/2=30x'^2$. Left column, at a distance $s$ below the beam: the UDL (360 kN acting 3 m from the column axis) gives $1080$ kN·m, constant, and the 100 kN load (4 m above the base) adds $100(s-1)$ below it:

$$\begin{gathered}M=1080\ (0\le s\le1) \\ M=1080+100(s-1)\ (1\le s\le5)\end{gathered}$$

*Vertical deflection.* Unit vertical load at the free end: $m=0$ in the right column, $m=x'$ in the beam, $m=6$ in the left column.

$$\Delta_v=\frac1{EI}\int_0^630x'^2\,x'\,dx'+\frac1{2EI}\left[\int_0^11080(6)\,ds+\int_1^5\left(1080+100(s-1)\right)6\,ds\right]$$

$$=\frac{9720}{EI}+\frac{6(1080+4320+800)}{2EI}=\frac{9720+18600}{EI}$$

$$\boxed{\Delta_v=\frac{28\,320}{EI}\ \text{kN·m}^3\ \text{(downward)}}$$

*Rotation.* Unit moment at the free end: $m=1$ everywhere (right column carries $M=0$ so contributes nothing).

$$\theta=\frac1{EI}\int_0^630x'^2dx'+\frac1{2EI}\left(1080+4320+800\right)=\frac{2160}{EI}+\frac{3100}{EI}$$

$$\boxed{\theta=\frac{5260}{EI}\ \text{kN·m}^2\ \text{(clockwise)}}$$

**(b) Truss deflection with a lack of fit.** Reactions: $V_A=V_D=25$ kN. The inclined members are AB, BE, CD (250 mm²); all others have 500 mm². Forces $F$ (tension +) under the real loads and $u$ for a unit downward load at E (method of joints):

| Member | $L$ (m) | $A$ (mm²) | $F$ (kN) | $u$ | $FuL/A$ (kN²·m/mm²) |
|---|---|---|---|---|---|
| AB | 5.657 | 250 | −35.36 | −0.4714 | 0.3772 |
| AF | 4 | 500 | +25.0 | +0.3333 | 0.0667 |
| BF | 4 | 500 | +25.0 | 0 | 0 |
| BC | 4 | 500 | −25.0 | −0.6667 | 0.1333 |
| BE | 5.657 | 250 | 0 | +0.4714 | 0 |
| FE | 4 | 500 | +25.0 | +0.3333 | 0.0667 |
| CE | 4 | 500 | +25.0 | +0.6667 | 0.1333 |
| CD | 5.657 | 250 | −35.36 | −0.9428 | 0.7544 |
| ED | 4 | 500 | +25.0 | +0.6667 | 0.1333 |

$$\sum\frac{FuL}{A}=1.6648\ \text{kN·m/mm}^2\ \Rightarrow\ \Delta_{load}=\frac{1.6648}{210}=0.007927\ \text{m}\approx7.93\ \text{mm}$$

(with $E=210$ GPa $=210$ kN/mm²).

*Lack of fit.* Member BE is 3.0 mm too short; the virtual-work term is $u_{BE}\,\Delta L=(+0.4714)(-3.0)=-1.414$ mm.

$$\boxed{\Delta_{E}=7.93-1.41\approx6.51\ \text{mm downward}}$$

@s 3
**(a) Conjugate beam method.** *Reactions.* For the part BC (hinge at B, roller at C), $\sum M_B=0$ with the counter-clockwise couple of 100 kN·m at C: $8R_C=-100$, so $R_C=-12.5$ kN (downward); hence the force transmitted by the hinge to AB is $12.5$ kN **downward** at B. The beam AB is therefore a cantilever fixed at A with a downward end load $P=12.5$ kN: $M_A=-75$ kN·m (hogging), zero at B.

*Conjugate beam for AB.* Fixed support at A becomes a free end; the hinge at B becomes a hinge of the conjugate beam; the conjugate load is $M/EI$. The $M/EI$ triangle has peak $75/EI$ at A, area $\tfrac12(75)(6)/EI=225/EI$, centroid $4$ m from B:

$$\begin{gathered}\theta_B^{left}=V'_B=\frac{225}{EI}\ \\ \Delta_B=M'_B=\frac{225(4)}{EI}\end{gathered}$$

$$\boxed{\Delta_B=\frac{900}{EI}\ \downarrow\ ,\qquad \theta_B^{left}=\frac{225}{EI}\ \text{(clockwise)}}$$

*Right of B.* The span BC (simply supported between B, deflected down by $900/EI$, and the roller C) has the moment varying linearly from 0 at B to $100$ kN·m at C. The bending slope at B is $\dfrac{ML}{6EI}=\dfrac{100(8)}{6EI}=\dfrac{133.33}{EI}$ (clockwise), and the rigid-body rotation due to the settlement of B relative to C is $\dfrac{900/EI}{8}=\dfrac{112.5}{EI}$ in the counter-clockwise sense:

$$\boxed{\theta_B^{right}=\frac{133.33-112.5}{EI}=\frac{20.83}{EI}\ \text{(clockwise)}}$$

The slopes on the two sides of the hinge differ by $\theta_B^{left}-\theta_B^{right}=204.2/EI$ (the relative rotation of the hinge).

**(b) Conjugate beam for the beam with overhang.** *Reactions* (moments about A): load on AB is the triangle $\tfrac12(10)(6)=30$ kN at 4 m from A; on BC, $5(3)=15$ kN at 7.5 m:

$$\begin{gathered}R_B=\frac{30(4)+15(7.5)}{6}=38.75\ \text{kN} \\ R_A=45-38.75=6.25\ \text{kN}\end{gathered}$$

*Bending moments:* on AB, $M=6.25x-\dfrac{10}{36}x^3$; at B, $M_B=-22.5$ kN·m (hogging); on BC, $M=-\tfrac52 s^2$ at a distance $s$ from C.

*Conjugate beam.* The real pin A stays a pin, the interior roller B becomes an **internal hinge**, and the free end C becomes a **fixed end**; the conjugate load is $M/EI$.

- *Span AB:* $M/EI=(6.25x-0.2778x^3)/EI$; net area $=3.125(36)-0.06944(1296)=22.5$; first moment about A $=6.25\dfrac{216}3-0.2778\dfrac{7776}5=18$, so the centroid is $0.8$ m from A. Taking moments about the hinge B′: $R'_A=\dfrac{22.5(6-0.8)}{6}=19.5$ and the force at the hinge is $R'_B=22.5-19.5=3.0$.
- *Overhang BC (cantilever B′C′ fixed at C′):* $M=-\tfrac52s^2$ ($s$ from C), area $=-\tfrac56(3)^3=-22.5$ with the centroid $\tfrac34(3)=2.25$ m from C; the hinge force $3.0$ acts at B′.

Slopes and deflection (conjugate shear = slope, conjugate moment = deflection):

$$\begin{gathered}\theta_A=\frac{19.5}{EI}\ (\text{clockwise}) \\ \theta_B=\frac{3.0}{EI}\ (\text{counter-clockwise})\end{gathered}$$

$$\theta_C=V'_C=\frac{3.0-22.5}{EI}=-\frac{19.5}{EI}\ \Rightarrow\ \boxed{\theta_C=\frac{19.5}{EI}\ \text{(clockwise)}}$$

$$\Delta_C=M'_C=\frac{3.0(3)-22.5(2.25)}{EI}=-\frac{41.6}{EI}\ \Rightarrow\ \boxed{\Delta_C=\frac{41.6}{EI}\ \text{downward}}$$

(Check by double integration of $EIy''=M$ with $y_A=y_B=0$: $EI\theta_A=19.5$ cw, $EI\theta_B=3.0$ ccw, $EI\theta_C=19.5$ cw, $EI\Delta_C=41.625$ kN·m³ down.)

@s 4
**(a) Train of loads on a girder of span $L=60$ m** (the 80 kN load leads; loads 100, 120, 160, 80 kN spaced at 0.8, 2.0, 1.2 m; total $W=460$ kN, centre of gravity at $\bar x=\dfrac{120(0.8)+160(2.8)+80(4.0)}{460}=1.878$ m from the 100 kN load).

*Maximum bending moment at C, 15 m from A.* For a section C at $a=15$ m, $M_C=R_Aa-\sum P(a-x_P)$, and the maximum occurs when a heavy load stands at the section such that the loads on the shorter segment AC satisfy $\dfrac{W_{AC}}{a}\ge\dfrac{W}{L}$ (criterion: $\dfrac{W_{AC}}{15}\ge\dfrac{460}{60}=7.67$ and with the same load moved to the other side the inequality reverses). Trying the 120 kN load at C: loads on AC are 100 + 120 = 220 kN, $\dfrac{220}{15}=14.7>7.67$ and with 120 kN removed from AC, $\dfrac{100}{15}=6.7<7.67$ ✔. So the 120 kN load is placed at the section with the 100 kN load 0.8 m to its left (at 14.2 m), and the 160 and 80 kN loads at 17.0 and 18.2 m:

$$R_A=\frac{100(45.8)+120(45)+160(43)+80(41.8)}{60}=\frac{20\,204}{60}=336.7\ \text{kN}$$

$$M_C=336.7(15)-100(0.8)=5051-80\approx\boxed{4971\ \text{kN·m}}$$

(verified by trying every position of the train: 4971 kN·m is the maximum, with the 100 kN load at 14.2 m.)

*Absolute maximum bending moment.* It occurs under a load near the middle of the span when that load and the resultant of all the loads on the span are placed symmetrically about the mid-span. The point of application of the resultant is $1.878$ m from the 100 kN load. Candidate: the 160 kN load (2.8 m from the 100 kN load) is $2.8-1.878=0.922$ m to the right of the resultant; place the resultant $0.461$ m to the left of the centre, i.e. the 160 kN load $0.461$ m to the right of the centre, at $x=30.461$ m from A (the 100 kN load at 27.661 m, all four loads on the span):

$$R_A=\frac{460(60-29.539)}{60}=233.5\ \text{kN}$$

$$M_{160}=233.5(30.461)-100(2.8)-120(2.0)=7113.0-280-240\approx6593.6\ \text{kN·m}$$

(The 120 kN load placed similarly gives 6574 kN·m and the 100 kN and 80 kN loads give 6475 and 6421 kN·m, all smaller.)

$$\boxed{M_{max,abs}\approx6594\ \text{kN·m}\ \text{under the 160 kN load, 30.46 m from the left support}}$$

**(b) Maximum member forces in the deck-type truss bridge.** *Assumed geometry* (the scan gives 4 panels at 5 m with 60° members): a Warren truss with top joints $U_1$–$U_5$ at $x=0,5,10,15,20$ m, bottom joints $L_1$–$L_4$ at $x=2.5,7.5,12.5,17.5$ m, height $h=5\sin60^\circ=4.33$ m, supports at the end joints $U_1$ (pin) and $U_5$ (roller); the load is transferred to the top joints. The influence-line ordinates of the three members for a unit load at $U_1,\dots,U_5$ (method of sections; tension positive):

| Unit load at | $U_1$ | $U_2$ | $U_3$ | $U_4$ | $U_5$ |
|---|---|---|---|---|---|
| $U_3U_4$ | 0 | −0.433 | −0.866 | −0.722 | 0 |
| $U_3L_3$ | 0 | −0.289 | −0.577 | +0.289 | 0 |
| $L_2L_3$ | 0 | +0.577 | +1.155 | +0.577 | 0 |

*Maximum force for a UDL longer than the span* (the whole length is loaded for the member whose ILD has one sign, the loaded length must cover the positive and negative parts separately for $U_3L_3$): force $=w\times$ area of the ILD.

- $U_3U_4$: area $=-10.10$ m, $F=60(-10.10)=-606.2$: **606 kN compression** (full span loaded).
- $L_2L_3$: area $=+11.55$ m, $F=60(11.55)=+692.8$: **693 kN tension**.
- $U_3L_3$: the ILD changes sign at 13.3 m (between $U_3$ and $U_4$): negative area $-3.85$ m, positive area $+0.96$ m. Maximum compression $=60(-3.85)=-230.9$ kN: **231 kN compression** (UDL from the left end to 13.3 m); maximum tension $=60(0.96)=+57.7$ kN: **57.7 kN tension** (UDL from 13.3 m to the right end).

$$\boxed{U_3U_4=606\ \text{kN (C)},\quad U_3L_3=231\ \text{kN (C)}\ /\ 57.7\ \text{kN (T)},\quad L_2L_3=693\ \text{kN (T)}}$$

@s 5
**Three-hinged parabolic arch.** Span $L=24$ m, rise $h=4$ m, hinges at A, B and the crown C. The shape is $y=\dfrac{4h}{L^2}x(L-x)=\dfrac{x(24-x)}{36}$ and the slope is $\tan\theta=\dfrac{dy}{dx}=\dfrac{24-2x}{36}$.

*Loads.* $P=75$ kN at 18 m from the right support, i.e. at $x=6$ m from the left; UDL $45\times12=540$ kN on the left half, centroid at $x=6$ m.

*Reactions.* $\sum M_A=0$: $V_B(24)=75(6)+540(6)=3690\ \Rightarrow\ V_B=153.75$ kN; $V_A=75+540-153.75=461.25$ kN. The bending moment at the crown hinge is zero (take the right side): $V_B(12)-H(4)=0$:

$$H=\frac{153.75(12)}{4}=461.25\ \text{kN}$$

*Section at $x=6$ m.* $y=\dfrac{6(18)}{36}=3.00$ m, $\tan\theta=\dfrac{12}{36}=\dfrac13$, so $\theta=18.43^\circ$, $\cos\theta=0.9487$, $\sin\theta=0.3162$.

$$M=V_A(6)-45\frac{6^2}{2}-H(3.00)=2767.5-810-1383.75$$

$$\boxed{M=573.75\ \text{kN·m}}$$

The vertical shear (beam shear) just left of the 75 kN load is $V=461.25-45(6)=191.25$ kN and just right of it is $V=191.25-75=116.25$ kN. Normal thrust $N=V\sin\theta+H\cos\theta$ and radial shear $Q=V\cos\theta-H\sin\theta$:

| Position | $V$ (kN) | Radial shear $Q$ (kN) | Normal thrust $N$ (kN) |
|---|---|---|---|
| just left of the 75 kN load | 191.25 | $191.25(0.9487)-461.25(0.3162)=+35.6$ | $191.25(0.3162)+461.25(0.9487)=498.1$ |
| just right of the 75 kN load | 116.25 | $116.25(0.9487)-461.25(0.3162)=-35.6$ | $116.25(0.3162)+461.25(0.9487)=474.3$ |

$$\boxed{M=573.75\ \text{kN·m},\quad N\approx498\ \text{kN (left), }474\ \text{kN (right)},\quad Q=\pm35.6\ \text{kN}}$$

*BMD.* $M(x)=V_Ax-\text{(loads to the left)}-Hy$; 0 at A, 374.1 at 3 m, **573.75 at 6 m**, 374.1 at 9 m, 0 at the crown (12 m), −345.9 at 15 m, −461.25 at 18 m, −345.9 at 21 m and 0 at B (kN·m).

```figure caption="Bending moment diagram of the three-hinged parabolic arch (plotted on the horizontal span, positive moments upward): maximum +573.75 kN·m at the 75 kN load, zero at the hinges, maximum hogging −461.25 kN·m at 18 m."
x=np.linspace(0,24,481); VA,H=461.25,461.25
M=VA*x-np.where(x<=12,45*x**2/2,45*12*(x-6))-np.where(x>6,75*(x-6),0)-H*4*4*x*(24-x)/576
fig,ax=plt.subplots(figsize=(5.4,2.5)); ax.fill_between(x,0,M,where=M>=0,color=ACCENT,alpha=0.25); ax.fill_between(x,0,M,where=M<0,color="#d9534f",alpha=0.25)
ax.plot(x,M,color=INK,lw=1.6); ax.axhline(0,color=INK,lw=0.9)
for xx,t in [(6,"573.75"),(18,"−461.25")]: ax.annotate(t,(xx,np.interp(xx,x,M)),textcoords="offset points",xytext=(0,6 if xx==6 else -12),ha="center",fontsize=8)
ax.set_xlabel("distance from left support (m)",fontsize=8.5); ax.set_ylabel("M (kN·m)",fontsize=8.5); ax.tick_params(labelsize=7.5); ax.grid(True,color=GRID,lw=0.5)
```

@s 6
**(a) Suspension bridge** (span $L=90$ m, dip $d=10$ m; the load is shared equally by the two cables and the two stiffening girders).

*Dead load.* $w=16$ kN/m on the whole span is carried by the cables alone (the cable takes the parabolic shape and the three-hinged girders carry no moment under the dead load): the total horizontal pull is

$$H_d=\frac{wL^2}{8d}=\frac{16(90)^2}{8(10)}=1620\ \text{kN}\ (810\ \text{kN per cable})$$

*Point loads* (250 kN at 30 m, 300 kN at 60 m): simple-beam reactions $V_A=\dfrac{250(60)+300(30)}{90}=266.67$ kN, $V_B=283.33$ kN. The girder hinge at the crown (45 m) has zero moment:

$$H_p=\frac{V_A(45)-250(15)}{10}=\frac{12000-3750}{10}=825\ \text{kN}$$

$$H=H_d+H_p=2445\ \text{kN}\ \Rightarrow\ \text{per cable}\ H=1222.5\ \text{kN}$$

*Vertical component at the supports.* Left: $16(45)+266.67=986.7$ kN; right: $16(45)+283.33=1003.3$ kN (both cables). For one cable the larger is $V=501.7$ kN at B:

$$T_{max}=\sqrt{H^2+V^2}=\sqrt{1222.5^2+501.7^2}$$

$$\boxed{T_{max}=1321\ \text{kN (at the right support)}}$$

The tension is least where the cable is horizontal, at the crown, where $T=H$:

$$\boxed{T_{min}=H=1222.5\ \text{kN (at the crown, with the live loads on); 810 kN with the dead load only}}$$

*Girder at 40 m from the left support* (for the whole bridge, then half for each girder). The ordinate of the cable at 40 m is $y=\dfrac{4(10)(40)(50)}{90^2}=9.877$ m and its slope $\tan\theta=\dfrac{4(10)(90-80)}{90^2}=0.04938$.

$$M_{40}=V_A(40)-250(10)-H_py=8166.7-8148.5=18.5\ \text{kN·m}\quad(\text{both girders})$$

$$V_{40}=V_A-250-H_p\tan\theta=266.67-250-40.74=-24.1\ \text{kN}\quad(\text{both girders})$$

$$\boxed{M_{40}\approx9.3\ \text{kN·m},\qquad V_{40}\approx-12.0\ \text{kN}\ \ \text{for each girder}}$$

**(b) Tension coefficient method for a space truss.** For a member $ij$ with length $L$ and tension $T$, the *tension coefficient* is $t=T/L$. The components of the member force at joint $i$ are $t(x_j-x_i)$, $t(y_j-y_i)$, $t(z_j-z_i)$ along the axes.

1. Choose axes $x,y,z$, number the joints and note their coordinates; compute the length $L_{ij}=\sqrt{\Delta x^2+\Delta y^2+\Delta z^2}$ of every member.
2. Check that the truss is determinate ($m+r=3j$), and find the support reactions from the equations of equilibrium of the whole truss, if needed (or leave them as unknowns at the supports and start from a joint with three unknown members).
3. Start at a joint with not more than three unknown bars. Write the three equilibrium equations: $\sum_{j}t_{ij}(x_j-x_i)+X_i=0$, $\sum_{j}t_{ij}(y_j-y_i)+Y_i=0$, $\sum_{j}t_{ij}(z_j-z_i)+Z_i=0$ ($X_i,Y_i,Z_i$ are the external loads and reactions at the joint).
4. Solve the three simultaneous equations for the tension coefficients, then continue to the next joint with three unknowns.
5. The force in every member is $T=tL$; a positive value means tension and a negative value compression.

The method is a systematic joint-by-joint method, well suited to a tabular layout, and gives the three components of the force of each member directly.

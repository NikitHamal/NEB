---
file: NEBians-IOE-Past-Paper-Engineering-Mechanics-CE101-2081-Baishakh.pdf
subject: Engineering Mechanics
level: BE · Year I / Part I
code: CE 101
year_bs: 2081 Baishakh
cal: BS
year_ad: 2024
stream: BCE, BAG
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Explain the concept of particle and rigid body. What are the equations of Static Equilibrium for 2-D and 3-D analysis of particle and rigid body? [[2+2]]

b) Determine the magnitude, direction and position (with respect to O) of the resultant of the following forces and moments acting on the plate (7 m × 8 m). [[5]]

```figure caption="Question 1(b): plate 8 m × 7 m with O at the bottom-left corner. Forces: 10 kN at 55° (top-left corner), 11 kN at 70° (top-right corner), 3 kN horizontal, 4 m below the top edge, 7 kN vertical at 5 m from O, 9 kN at 60° (bottom-right corner); couples 60 kN·m at O and 50 kN·m at 5 m."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.2,4.2)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),8,7,fc="#eef2f8",ec=INK,lw=1))
a=dict(arrowstyle="-|>",color=INK,lw=1.3)
def arr(p,q,t,tp):
    ax.annotate("",xy=q,xytext=p,arrowprops=a); ax.text(tp[0],tp[1],t,fontsize=8)
c,s=_np.cos,_np.sin; d=_np.radians
arr((0,7),(0+2*c(d(55)),7+2*s(d(55))),"10 kN, 55°",(0.6,9.4))
arr((8-2*c(d(70)),7+2*s(d(70))),(8,7),"11 kN, 70°",(5.4,9.1))
arr((10,3),(8,3),"3 kN",(9.0,3.25))
arr((8+2*s(d(60)),0+2*c(d(60))),(8,0),"9 kN, 60°",(9.0,1.3))
arr((5,2),(5,0),"7 kN",(5.2,1.2))
ax.add_patch(mp.Arc((0,0),1.8,1.8,theta1=90,theta2=270,color=INK,lw=1.2)); ax.text(-3.2,-0.9,"60 kN·m",fontsize=8)
ax.add_patch(mp.Arc((5,0),1.8,1.8,theta1=180,theta2=360,color=INK,lw=1.2)); ax.text(5.6,-1.4,"50 kN·m",fontsize=8)
ax.text(-0.5,-0.7,"O",fontsize=9)
ax.text(2.2,3.3,"8 m × 7 m",fontsize=9,color=MUTED)
ax.set_xlim(-3.6,11.8); ax.set_ylim(-2,10)
```

@q 2
a) Three vertical wires as shown in the figure support a plate of 35 Kg. Determine the tension in each wire. [[5]]

```figure caption="Question 2(a): plan of the 1500 mm × 1500 mm plate. T$_1$ and T$_2$ act on the left edge at 375 mm from the front and the back corners; T$_3$ acts on the right edge at 750 mm from the back."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.4,3.6)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),1500,1500,fc="#eef2f8",ec=INK,lw=1.2))
for (x,y,t) in ((0,375,"T$_1$ (A)"),(0,1125,"T$_2$ (B)"),(1500,750,"T$_3$ (C)")):
    ax.plot([x],[y],"o",color="#c0392b",ms=6)
    ax.text(x+(-60 if x==0 else 60),y,t,fontsize=8,ha="right" if x==0 else "left",va="center")
ax.plot([750],[750],"x",color=INK,ms=7); ax.text(780,690,"G (W = 343.35 N)",fontsize=7.5)
ar=dict(arrowstyle="<->",color=INK,lw=0.7)
ax.annotate("",xy=(0,-110),xytext=(1500,-110),arrowprops=ar); ax.text(750,-230,"1500 mm",ha="center",fontsize=7.5)
ax.annotate("",xy=(-330,0),xytext=(-330,375),arrowprops=ar); ax.text(-370,190,"375",ha="right",va="center",fontsize=7)
ax.annotate("",xy=(-330,1125),xytext=(-330,1500),arrowprops=ar); ax.text(-370,1310,"375",ha="right",va="center",fontsize=7)
ax.annotate("",xy=(1700,750),xytext=(1700,1500),arrowprops=ar); ax.text(1740,1120,"750",va="center",fontsize=7)
ax.text(750,1560,"back",ha="center",fontsize=7,color=MUTED)
ax.set_xlim(-900,2300); ax.set_ylim(-320,1700)
```

b) Define angle of friction. A body weighing 300 N is lying on a rough horizontal plane having coefficient of static friction as 0.35. Find the magnitude of force P which can move the body at an angle of 25 degrees. [[1+3]]

@q 3
a) How can we check the determinacy and stability of a frame structure? Explain with suitable example. [[3]]

b) Draw axial force, shear force and bending moment for the beam loaded as shown. Indicate salient features if any. [[10]]

```figure caption="Question 3(b): beam ABCDEF. 15 kN at the free end A; hinge support at B (2 m from A); 10 kN/m UDL over BC (3 m); a bracket at D carrying 20 kN at 1 m from D and 2 m above the axis; 12 kN/m triangular load over EF (3 m) reducing to zero at the roller support F. Spans: AB 2 m, BC 3 m, CD 1 m, DE 2 m, EF 3 m."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.4,2.6)); ax.axis("off")
ax.plot([0,11],[0,0],color=INK,lw=2)
a=dict(arrowstyle="-|>",color=INK,lw=1.2)
ax.annotate("",xy=(0,0),xytext=(0,1.1),arrowprops=a); ax.text(0.1,1.15,"15 kN",fontsize=8)
for x in [2.1+0.3*i for i in range(10)]:
    ax.annotate("",xy=(x,0),xytext=(x,0.45),arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.plot([2,5],[0.45,0.45],color=INK,lw=1); ax.text(3.2,0.6,"10 kN/m",fontsize=8)
ax.plot([6,6,7],[0,2,2],color=INK,lw=1.3); ax.annotate("",xy=(7,0.9),xytext=(7,2.0),arrowprops=a); ax.text(7.1,1.5,"20 kN",fontsize=8)
ax.text(6.1,0.9,"2 m",fontsize=7); ax.text(6.4,2.08,"1 m",fontsize=7)
xs=[8+0.5*i for i in range(6)]
for x in xs:
    h=1.1*(1-(x-8)/3)
    if h>0.02: ax.annotate("",xy=(x,0),xytext=(x,h),arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.plot([8,11],[1.1,0],color=INK,lw=1); ax.text(8.1,1.25,"12 kN/m",fontsize=8)
ax.add_patch(mp.Polygon([(2,0),(1.8,-0.35),(2.2,-0.35)],closed=True,fc="white",ec=INK))
ax.add_patch(mp.Circle((11,-0.18),0.17,fc="white",ec=INK)); ax.plot([10.7,11.3],[-0.38,-0.38],color=INK)
for x,l in ((0,"A"),(2,"B"),(5,"C"),(6,"D"),(8,"E"),(11,"F")): ax.text(x,-0.85,l,ha="center",fontsize=8)
ax.set_xlim(-0.6,11.8); ax.set_ylim(-1.1,2.5)
```

@q 4
a) Explain with diagram the general conditions in which a zero force member arises in a truss. Find the force in all the members of the truss shown. [[2+4]]

```figure caption="Question 4(a): truss ABCDE. A(0, 4), B(6, 4), C(12, 4) on the top chord and D(3, 0), E(9, 0) on the bottom chord (m). 5 kN at A and 10 kN at B. C is pinned to the wall, E is on a roller."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.0,2.8)); ax.set_aspect("equal"); ax.axis("off")
P={"A":(0,4),"B":(6,4),"C":(12,4),"D":(3,0),"E":(9,0)}
for m in ("AB","BC","DE","AD","DB","BE","EC"):
    ax.plot([P[m[0]][0],P[m[1]][0]],[P[m[0]][1],P[m[1]][1]],color=INK,lw=1.6)
for k,(x,y) in P.items():
    ax.plot([x],[y],"o",color=INK,ms=4); ax.text(x+(0.25 if k in "CE" else -0.1),y+(0.3 if y>1 else -0.65),k,fontsize=9)
a=dict(arrowstyle="-|>",color=INK,lw=1.3)
ax.annotate("",xy=(0,4),xytext=(0,5.6),arrowprops=a); ax.text(0.2,5.0,"5 kN",fontsize=8)
ax.annotate("",xy=(6,4),xytext=(6,5.6),arrowprops=a); ax.text(6.2,5.0,"10 kN",fontsize=8)
ax.add_patch(mp.Polygon([(12,4),(12.6,3.5),(12.6,4.5)],closed=True,fc="white",ec=INK))
ax.plot([12.7,12.7],[3.4,4.6],color=INK,lw=1.2)
ax.add_patch(mp.Polygon([(9,0),(8.6,-0.6),(9.4,-0.6)],closed=True,fc="white",ec=INK)); ax.plot([8.5,9.5],[-0.75,-0.75],color=INK)
ar=dict(arrowstyle="<->",color=MUTED,lw=0.7)
for x0,x1,l in ((0,3,"3 m"),(3,9,"6 m"),(9,12,"3 m")):
    ax.annotate("",xy=(x0,-1.3),xytext=(x1,-1.3),arrowprops=ar); ax.text((x0+x1)/2,-1.9,l,ha="center",fontsize=8)
ax.annotate("",xy=(13.6,0),xytext=(13.6,4),arrowprops=ar); ax.text(13.8,2,"4 m",fontsize=8,va="center")
ax.set_xlim(-1,15); ax.set_ylim(-2.3,6.2)
```

b) "Location of center of gravity/centroid is independent of choice of reference point/axis" Explain the statement. Calculate moment of inertia about centroidal y-axis of the composite shaded area shown below. [[1+4]]

```figure caption="Question 4(b): shaded area = trapezium (bottom width 6 m, top width 3 m, height 6 m) minus a semicircle of radius 3 m whose diameter lies on the Y axis."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.6,3.4)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Polygon([(0,0),(6,0),(3,6),(0,6)],closed=True,fc="#cfdcec",ec=INK,lw=1.2))
ax.add_patch(mp.Wedge((0,3),3,-90,90,fc="white",ec=INK,lw=1.2))
ar=dict(arrowstyle="-|>",color=INK,lw=1)
ax.annotate("",xy=(0,6.9),xytext=(0,-0.3),arrowprops=ar); ax.text(0.15,6.9,"Y",fontsize=9)
ax.annotate("",xy=(7.2,0),xytext=(-0.3,0),arrowprops=ar); ax.text(7.2,0.1,"X",fontsize=9)
ax.plot([0,3],[3,3],color=MUTED,lw=0.8,ls="--"); ax.text(1.1,3.15,"R = 3 m",fontsize=8)
ax2=dict(arrowstyle="<->",color=MUTED,lw=0.7)
ax.annotate("",xy=(0,-0.9),xytext=(6,-0.9),arrowprops=ax2); ax.text(3,-1.6,"6 m",ha="center",fontsize=8)
ax.annotate("",xy=(0,6.5),xytext=(3,6.5),arrowprops=ax2); ax.text(1.5,6.65,"3 m",ha="center",fontsize=8)
ax.set_xlim(-1,8); ax.set_ylim(-2,7.6)
```

@q 5
a) How does kinematics differ from kinetics for a particle moving along its path? A ski jumper starts with a horizontal take-off velocity of 25 m/s and lands on a straight landing hill inclined at 30°. Determine (i) the time between take-off and landing, (ii) the length d of the jump, (iii) the maximum vertical distance between the jumper and the landing hill. [[1+5]]

```figure caption="Question 5(a): ski jumper leaving the take-off with a horizontal velocity of 25 m/s and landing on a 30° hill after a jump of length d measured along the hill."
import numpy as _np
fig,ax=plt.subplots(figsize=(4.6,3.0)); ax.set_aspect("equal"); ax.axis("off")
x=_np.linspace(0,73.57,100); ax.plot(x,-9.81*(x/25)**2/2,color=INK,lw=1.3)
ax.plot([0,100],[0,-100*_np.tan(_np.radians(30))],color=INK,lw=2); ax.plot([-20,0],[0,0],color=INK,lw=2)
ax.annotate("",xy=(14,0.8),xytext=(0,0.8),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2)); ax.text(2,3.5,"25 m/s",fontsize=8)
ax.text(30,-52,"d",fontsize=9); ax.text(72,-67,"30°",fontsize=8)
ax.plot([100,100],[0,-57.7],color=MUTED,lw=0.6,ls="--"); ax.plot([0,100],[-57.7,-57.7],color=MUTED,lw=0.6,ls="--")
ax.set_xlim(-25,110); ax.set_ylim(-70,10)
```

b) Derive work-energy principle for a particle. The bob of a 3 m pendulum describes an arc of a circle in a vertical plane. If the tension in the chord is 2 times the weight of the bob for the position when it is displaced through an angle of 30 degree from its mean position, find the velocity and acceleration of the bob for this situation? [[2+4]]

```figure caption="Question 5(b): simple pendulum of length 3 m displaced through 30° from the vertical."
import numpy as _np
fig,ax=plt.subplots(figsize=(2.8,3.0)); ax.set_aspect("equal"); ax.axis("off")
ax.plot([-1.5,1.5],[0,0],color=INK,lw=2); ax.plot([0,0],[0,-3],color=MUTED,lw=0.8,ls="--")
bx,by=3*_np.sin(_np.radians(30)),-3*_np.cos(_np.radians(30))
ax.plot([0,bx],[0,by],color=INK,lw=1.3); ax.add_patch(plt.Circle((bx,by),0.22,fc="#cfdcec",ec=INK))
t=_np.linspace(-_np.pi/2,-_np.pi/2+_np.radians(30),20); ax.plot(0.9*_np.cos(t),0.9*_np.sin(t),color=INK,lw=0.8)
ax.text(0.15,-1.25,"30°",fontsize=8); ax.text(0.5,-0.9,"3 m",fontsize=8,rotation=-60); ax.text(-0.3,0.15,"O",fontsize=9)
ax.set_xlim(-1.8,2.6); ax.set_ylim(-3.6,0.6)
```

@q 6
a) Explain D' Alembert's principle for plane motion of rigid body. [[2]]

b) In the engine system shown, the crank AB has a constant clockwise angular velocity of 2000 rpm. For the crank position shown in figure below, determine, (i) the angular velocity of the connecting rod BD, (ii) the velocity of the piston P. [[4]]

```figure caption="Question 6(b): crank AB (r = 3 in) at 40° to the horizontal, connecting rod BD (l = 8 in) with centre of mass G, piston P at D."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.2,2.4)); ax.set_aspect("equal"); ax.axis("off")
th=_np.radians(40); B=(3*_np.cos(th),3*_np.sin(th)); be=_np.arcsin(3*_np.sin(th)/8); D=(B[0]+8*_np.cos(be),0)
ax.plot([0,B[0]],[0,B[1]],color=INK,lw=3); ax.plot([B[0],D[0]],[B[1],0],color=INK,lw=3)
ax.add_patch(mp.Rectangle((D[0],-0.8),2.2,1.6,fc="#cfdcec",ec=INK)); ax.text(D[0]+0.8,-0.2,"P",fontsize=9)
ax.plot([-0.6,10.5],[0,0],color=MUTED,lw=0.7,ls="--")
for p,l,o in (((0,0),"A",(-0.7,-0.5)),(B,"B",(0.05,0.2)),(D,"D",(-0.3,-1.2))):
    ax.plot(*p,"o",color=INK,ms=5); ax.text(p[0]+o[0],p[1]+o[1],l,fontsize=9)
ax.text(1.6,0.45,"40°",fontsize=8); ax.text(0.5,1.9,"r = 3 in",fontsize=8,rotation=40)
ax.text(5.2,2.2,"l = 8 in",fontsize=8); ax.text(B[0]+3.3,0.35,"β",fontsize=9)
ax.set_xlim(-1.2,11); ax.set_ylim(-1.6,3.2)
```

<!-- SOLUTIONS -->

@s 1
**(a) Particle and rigid body.**

- A **particle** is a body whose dimensions are negligible compared with the other lengths in the problem, so all forces on it can be taken as concurrent at one point and its rotation is of no interest (a car on a long road, a ball in flight).
- A **rigid body** is a body of finite size in which the distance between any two points never changes, whatever the loads: deformation is neglected. Forces on it act at different points, so both their sum and their moments matter.

*Equations of static equilibrium*

| Case | Particle (concurrent forces) | Rigid body |
|---|---|---|
| 2-D | $\sum F_x=0,\ \sum F_y=0$ | $\sum F_x=0,\ \sum F_y=0,\ \sum M_O=0$ (3 equations) |
| 3-D | $\sum F_x=0,\ \sum F_y=0,\ \sum F_z=0$ | $\sum F_x=\sum F_y=\sum F_z=0$ and $\sum M_x=\sum M_y=\sum M_z=0$ (6 equations) |

In vector form $\sum\vec F=\vec 0$ for a particle, and $\sum\vec F=\vec 0,\ \sum\vec M_O=\vec 0$ for a rigid body.

**(b) Resultant of the force system.** Take O as origin, $x$ to the right and $y$ upward. Moments counter-clockwise (+). The 60 kN·m and 50 kN·m couples are read as counter-clockwise (the arrows on the figure curl the same way). The 9 kN force is read as 60° to the vertical, i.e. 30° below the horizontal; the 10 kN and 11 kN forces make 55° and 70° with the top edge.

| Force | Point (m) | $F_x$ (kN) | $F_y$ (kN) | $M_O=xF_y-yF_x$ (kN·m) |
|---|---|---|---|---|
| 10 kN, 55° | (0, 7) | $10\cos55^\circ=+5.736$ | $10\sin55^\circ=+8.192$ | $-40.15$ |
| 11 kN, 70° | (8, 7) | $11\cos70^\circ=+3.762$ | $-11\sin70^\circ=-10.337$ | $-109.03$ |
| 3 kN | (8, 3) | $-3.000$ | $0$ | $+9.00$ |
| 9 kN | (8, 0) | $-9\sin60^\circ=-7.794$ | $-9\cos60^\circ=-4.500$ | $-36.00$ |
| 7 kN | (5, 0) | $0$ | $-7.000$ | $-35.00$ |
| Couples | | | | $+60+50=+110$ |

$$\begin{gathered}R_x=\sum F_x=-1.296\ \text{kN} \\ R_y=\sum F_y=-13.645\ \text{kN}\end{gathered}$$

**Magnitude and direction**

$$\begin{gathered}R=\sqrt{1.296^2+13.645^2}=\boxed{13.71\ \text{kN}} \\ \theta=\tan^{-1}\frac{13.645}{1.296}=84.57^\circ\ \text{below the negative } x\text{-axis}\end{gathered}$$

The resultant points down and slightly to the left, $5.43^\circ$ from the vertical (direction angle $264.6^\circ$ measured counter-clockwise from $+x$).

**Position.** The resultant moment about O is $M_O=-40.15-109.03+9-36-35+110=-101.18$ kN·m, i.e. **101.18 kN·m clockwise**. The single resultant must give the same moment about O. It cuts the bottom edge ($y=0$) at

$$x\,R_y=M_O\ \Rightarrow\ x=\frac{-101.18}{-13.645}=\boxed{7.415\ \text{m from O}}$$

so the resultant of 13.71 kN acts through the point (7.42 m, 0) on the bottom edge, i.e. 0.585 m to the left of the bottom-right corner. (It meets the line $x=0$ at $y=-78.06$ m, far below the plate, which is why the base intercept is the useful position.)

@s 2
**(a) Tensions in the three wires.** Mass 35 kg gives $W=35\times9.81=343.35$ N acting at the centre of the 1500 mm × 1500 mm plate. Take the front-left corner as origin, $x$ across the 1500 mm width and $y$ along the depth. Reading the figure: A is on the left edge at 375 mm from the front, B on the left edge at 375 mm from the back ($y=1125$ mm) and C on the right edge at 750 mm from the back ($y=750$ mm).

Points: $A(0,375)$, $B(0,1125)$, $C(1500,750)$, $G(750,750)$.

$$\sum F_z=0:\quad T_1+T_2+T_3=W$$

Moment about the left edge (the $y$-axis): only $T_3$ and $W$ have an arm in $x$:

$$T_3(1500)=W(750)\ \Rightarrow\ \boxed{T_3=\frac W2=171.68\ \text{N}}$$

Moment about the front edge (the $x$-axis):

$$375\,T_1+1125\,T_2+750\,T_3=750\,W$$

With $T_3=W/2$ this gives $375T_1+1125T_2=375W$, i.e. $T_1+3T_2=W$. Together with $T_1+T_2=W/2$:

$$\begin{gathered}2T_2=\frac W2 \\ \boxed{T_2=\frac W4=85.84\ \text{N}},\qquad \boxed{T_1=\frac W4=85.84\ \text{N}}\end{gathered}$$

Check: $85.84+85.84+171.68=343.35$ N. ✓

**(b) Angle of friction and force P.**

*Angle of friction* $\phi$ is the angle between the normal reaction and the resultant of the normal reaction and the limiting friction force. At the point of slipping $\tan\phi=F/N=\mu$, so $\phi=\tan^{-1}\mu=\tan^{-1}0.35=19.29^\circ$.

*Force P* at $25^\circ$ to the horizontal, pulling upward (the usual arrangement; $W=300$ N, $\mu=0.35$). At the point of motion:

$$\begin{gathered}\sum F_y=0:\ N=W-P\sin25^\circ \\ \sum F_x=0:\ P\cos25^\circ=\mu N=\mu(W-P\sin25^\circ)\end{gathered}$$

$$P=\frac{\mu W}{\cos25^\circ+\mu\sin25^\circ}=\frac{0.35\times300}{0.9063+0.35\times0.4226}=\frac{105}{1.0542}=\boxed{99.6\ \text{N}}$$

Then $N=300-99.6\sin25^\circ=257.9$ N and $F=0.35\times257.9=90.3$ N $=P\cos25^\circ$ ✓. A pull of just over 99.6 N at 25° will start the body moving. (If P were instead a push inclined 25° below the horizontal, $P=\mu W/(\cos25^\circ-\mu\sin25^\circ)=138.5$ N; the least force at any angle is $\mu W/\sqrt{1+\mu^2}=99.0$ N, at $\theta=\phi=19.29^\circ$.)

@s 3
**(a) Determinacy and stability of a plane frame.** Let $m$ = number of members, $j$ = number of joints, $r$ = number of support reactions and $c$ = number of extra equations of condition (internal hinges release one each).

| Check | Rule |
|---|---|
| Unknowns | $3m+r$ (3 internal force components per member plus the reactions) |
| Equations | $3j+c$ (3 per joint) |
| Statically determinate | $3m+r=3j+c$ |
| Indeterminate | $3m+r>3j+c$, degree of indeterminacy $=(3m+r)-(3j+c)$ |
| Unstable | $3m+r<3j+c$ |

The equation count is *necessary but not sufficient*. The frame is also **geometrically unstable** if the reactions are all parallel, all pass through one point, or a part of the frame can move as a mechanism, even when $3m+r\ge3j+c$. Stability is therefore confirmed by looking at the support arrangement too: at least three reactions that are neither concurrent nor parallel.

*Example (portal frame, $m=3$, $j=4$).*

| Supports | $r$ | $c$ | $3m+r$ | $3j+c$ | Result |
|---|---|---|---|---|---|
| Both feet fixed | 6 | 0 | 15 | 12 | indeterminate to the 3rd degree |
| Both feet hinged | 4 | 0 | 13 | 12 | indeterminate to the 1st degree |
| Hinged feet + hinge in the beam (three-hinged) | 4 | 1 | 13 | 13 | determinate and stable |
| Hinge + roller, no internal hinge | 3 | 0 | 12 | 12 | determinate and stable |

**(b) Axial force, shear force and bending moment.** Take $x$ from A. Loads: 15 kN at A; UDL 10 kN/m on $2\le x\le5$ (total 30 kN at $x=3.5$); at D ($x=6$) the 20 kN load on the bracket is moved to the axis and gives 20 kN downward plus a couple $20\times1=20$ kN·m clockwise; the triangular load on $8\le x\le11$ has resultant $\tfrac12\times12\times3=18$ kN at 1 m from E, $x=9$. All loads are vertical, so **the axial force is zero throughout**.

*Reactions* (upward $B_y$, $F_y$; the roller F carries vertical load only). Taking moments about B (counter-clockwise +):

$$15(2)-30(1.5)-20(4)-20-18(7)+F_y(9)=0\ \Rightarrow\ F_y=\frac{241}{9}=\boxed{26.78\ \text{kN}}$$

$$B_y=15+30+20+18-26.78=\boxed{56.22\ \text{kN}}$$

*Shear force* (up positive, left to right):

| Section | $V$ (kN) |
|---|---|
| A to B | $-15$ |
| B, just right | $-15+56.22=+41.22$ |
| at C ($x=5$) | $41.22-10\times3=+11.22$ (linear fall in BC) |
| C to D | $+11.22$ |
| D, just right | $11.22-20=-8.78$ |
| D to E | $-8.78$ |
| at F, left ($s=3$ m from E) | $-8.78-(12s-2s^2)=-26.78$ (parabolic) |
| F, after reaction | $-26.78+26.78=0$ ✓ |

$V$ is $-15$ just left of B and jumps by 56.22 kN at B and by $-20$ at D.

*Bending moment* (sagging positive):

| Section | $M$ (kN·m) |
|---|---|
| A | 0 |
| B | $-15\times2=-30.00$ (hogging) |
| C ($x=5$) | $-30+41.22(3)-10(3)^2/2=+48.67$ |
| D, left ($x=6$) | $48.67+11.22(1)=+59.89$ |
| D, right | $59.89+20=+79.89$ (jump of 20 kN·m for the clockwise couple) |
| E ($x=8$) | $79.89-8.78(2)=+62.33$ |
| F | $62.33-8.78(3)-6(3)^2+\tfrac23(3)^3=0$ ✓ |

Between E and F: $M=62.33-8.78\,s-6s^2+\tfrac23s^3$ (cubic).

*Salient features*

- Axial force is zero in all parts.
- Maximum shear $=\mathbf{-26.78}$ kN at F (the support reaction); the largest positive value is $+41.22$ kN just right of B. Shear is nowhere zero between B and C ($V$ falls from 41.22 to 11.22) or between E and F, so there is no local extreme of $M$ there.
- Maximum sagging moment $=\mathbf{+79.89}$ kN·m just right of D (where the couple is applied); maximum hogging moment $=\mathbf{-30}$ kN·m at the support B.
- Point of contraflexure in BC: $-30+41.22u-5u^2=0$ with $u=x-2$, so $u=0.806$ and $x=2.81$ m from A.
- $M=0$ at A and F as required at a free end and a roller.

```figure caption="Question 3(b): axial force (zero), shear force and bending moment diagrams of the beam (V in kN, M in kN·m)."
import numpy as _np
Bv=56.2222; Fv=26.7778
x=_np.linspace(0,11,4401)
u=_np.clip(x-2,0,3); s=_np.clip(x-8,0,3)
V=-15+Bv*(x>=2)-10*u-20*(x>=6)-(12*s-2*s**2)
V=_np.where(x>=10.9999,0,V)
M=_np.concatenate([[0],_np.cumsum((V[1:]+V[:-1])/2*_np.diff(x))])+20*(x>=6)
fig,axs=plt.subplots(3,1,figsize=(6.4,6.0),sharex=True)
for a,y,t,c in zip(axs,(0*x,V,M),("Axial force N (kN): zero throughout","Shear force V (kN)","Bending moment M (kN·m)"),("#999","#2c6fb0","#c0392b")):
    a.axhline(0,color=INK,lw=0.8); a.plot(x,y,color=c,lw=1.5); a.fill_between(x,0,y,color=c,alpha=0.12)
    a.set_title(t,fontsize=8,loc="left"); a.tick_params(labelsize=7); a.grid(alpha=0.25)
for a in axs[1:]:
    for xv in (2,5,6,8,11): a.axvline(xv,color=MUTED,lw=0.5,ls=":")
axs[1].annotate("+41.22",(2.05,41.22),fontsize=7); axs[1].annotate("-26.78",(10.0,-26.78),fontsize=7,va="top")
axs[1].annotate("-15",(0.8,-15),fontsize=7,va="top"); axs[1].annotate("-8.78",(6.6,-8.78),fontsize=7,va="top")
axs[2].annotate("-30",(2.0,-30),fontsize=7,va="top"); axs[2].annotate("+79.89",(6.05,79.9),fontsize=7)
axs[2].annotate("x = 2.81 m (M = 0)",(2.81,0),(3.2,-25),fontsize=7,arrowprops=dict(arrowstyle="->",lw=0.6))
axs[2].set_xlabel("x from A (m): A 0, B 2, C 5, D 6, E 8, F 11",fontsize=7)
fig.tight_layout()
```

@s 4
**(a) Zero-force members.** A member that carries no force under a given loading is a *zero-force member*. It still holds the truss stable and takes load if the loading changes. The standard joint conditions (a joint with no support, judged by the equilibrium of the pin) are:

1. *Two non-collinear members meeting at an unloaded joint*: both are zero (no way to balance a force in one without the other).
2. *Three members at an unloaded joint, two of which are collinear*: the third (non-collinear) member is zero; the two collinear members carry equal force.
3. *Two non-collinear members at a joint where the only external load acts along one of them*: the other member is zero.

```figure caption="Zero-force members: (1) two non-collinear members at an unloaded joint, (2) a third member at an unloaded joint with two collinear members, (3) an external load along one of two non-collinear members."
import numpy as _np
fig,axs=plt.subplots(1,3,figsize=(6.4,1.9))
for a in axs: a.set_aspect("equal"); a.axis("off"); a.set_xlim(-2.2,2.2); a.set_ylim(-1.8,1.8)
def m(a,p,q,c=INK,lw=2): a.plot([p[0],q[0]],[p[1],q[1]],color=c,lw=lw)
a=axs[0]; m(a,(0,0),(1.6,0)); m(a,(0,0),(0,1.4),"#c0392b"); a.plot([0],[0],"ko"); a.text(-1.4,-1.5,"(1) both = 0",fontsize=8)
a=axs[1]; m(a,(-1.6,0),(0,0)); m(a,(0,0),(1.6,0)); m(a,(0,0),(0.8,1.3),"#c0392b"); a.plot([0],[0],"ko"); a.text(-1.4,-1.5,"(2) third = 0",fontsize=8)
a=axs[2]; m(a,(0,0),(1.6,0)); m(a,(0,0),(0,1.4),"#c0392b")
a.annotate("",xy=(0,0),xytext=(-1.5,0),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.4)); a.plot([0],[0],"ko"); a.text(-1.9,-1.5,"(3) other member = 0",fontsize=8)
fig.tight_layout()
```

*Method of joints.* Members: AB, BC, DE (chords) and AD, DB, BE, EC (diagonals), each diagonal being 5 m long with $\sin\theta=4/5=0.8$, $\cos\theta=3/5=0.6$. Joint count 5, members 7, reactions 3 ($C_x$, $C_y$ at the pin; $E_y$ at the roller): $7+3=2\times5$, so the truss is statically determinate.

*Reactions.* Taking moments about C: $E_y(3)=5(12)+10(6)$, so $E_y=40$ kN upward. $\sum F_y=0$: $C_y=15-40=-25$ kN (downward, 25 kN). $\sum F_x=0$: $C_x=0$.

*Joint A* (5 kN down; members AB, AD; unit vector from A to D is $(0.6,-0.8)$):

$$\begin{gathered}\sum F_y=0:\ -5-0.8F_{AD}=0 \Rightarrow F_{AD}=-6.25\ \text{kN} \\ \sum F_x=0:\ F_{AB}+0.6F_{AD}=0 \Rightarrow F_{AB}=+3.75\ \text{kN}\end{gathered}$$

*Joint D* (members DA, DB, DE; unit vectors from D: to A $(-0.6,0.8)$, to B $(0.6,0.8)$, to E $(1,0)$):

$$\begin{gathered}\sum F_y=0:\ 0.8(F_{AD}+F_{DB})=0 \Rightarrow F_{DB}=+6.25\ \text{kN} \\ \sum F_x=0:\ -0.6F_{AD}+0.6F_{DB}+F_{DE}=0 \Rightarrow F_{DE}=-7.5\ \text{kN}\end{gathered}$$

*Joint E* (reaction 40 kN up; unit vectors from E: to D $(-1,0)$, to B $(-0.6,0.8)$, to C $(0.6,0.8)$):

$$\begin{gathered}\sum F_y=0:\ 40+0.8(F_{EB}+F_{EC})=0 \Rightarrow F_{EB}+F_{EC}=-50 \\ \sum F_x=0:\ -F_{DE}-0.6F_{EB}+0.6F_{EC}=0 \Rightarrow F_{EC}-F_{EB}=-12.5\end{gathered}$$

$$\begin{gathered}F_{EC}=-31.25\ \text{kN} \\ F_{EB}=-18.75\ \text{kN}\end{gathered}$$

*Joint B* (10 kN down; unit vectors from B: to A $(-1,0)$, to C $(1,0)$, to D $(-0.6,-0.8)$, to E $(0.6,-0.8)$):

A tension member pulls the pin towards the member's far end, so with $F_{AB}=+3.75$, $F_{BD}=+6.25$, $F_{BE}=-18.75$:

$$\begin{gathered}\sum F_x=0:\ -3.75+F_{BC}-0.6(6.25)+0.6(-18.75)=0 \Rightarrow F_{BC}=+18.75\ \text{kN} \\ \sum F_y=0:\ -10-0.8(6.25)-0.8(-18.75)=-10-5+15=0\ \checkmark\end{gathered}$$

*Joint C* check: $\sum F_y=-0.8(-31.25)+C_y=25-25=0$ ✓ and $\sum F_x=-F_{BC}-0.6F_{CE}+C_x=-18.75+18.75+0=0$ ✓.

| Member | AB | BC | DE | AD | DB | BE | EC |
|---|---|---|---|---|---|---|---|
| Force (kN) | 3.75 T | 18.75 T | 7.50 C | 6.25 C | 6.25 T | 18.75 C | 31.25 C |

(T = tension, C = compression.) For this loading **no member is a zero-force member**; the largest force is 31.25 kN compression in EC.

**(b) Centroid is independent of the reference axis.** The centroid $\bar x=\dfrac{\sum A_ix_i}{\sum A_i}$ is a property of the shape. If the reference axes are shifted by $a$ then every $x_i$ becomes $x_i+a$ and $\bar x$ becomes $\bar x+a$: the *coordinates* change but the *point* in the body remains the same, since it is the point about which the first moment of area (or the moment of weight) is zero, $\int(x-\bar x)\,dA=0$. Shifting the origin changes the numbers, not the physical point. The same argument holds for the centre of gravity.

*Composite area.* Y is the left edge of the figure; area = rectangle + right triangle − semicircle ($r=3$ m). Split the trapezium by the vertical line $x=3$:

| Part | Area (m²) | $\bar x$ (m) | $I_{\text{own}}$ about its centroidal vertical axis (m⁴) |
|---|---|---|---|
| 1 Rectangle 3 × 6 | 18 | 1.5 | $\dfrac{6(3)^3}{12}=40.5$ |
| 2 Right triangle, base 3, height 6 | 9 | $3+\dfrac33=4$ | $\dfrac{6(3)^3}{36}=4.5$ |
| 3 Semicircle $r=3$ (removed) | $\dfrac{\pi(3)^2}{2}=14.137$ | $\dfrac{4(3)}{3\pi}=1.273$ | $\left(\dfrac\pi8-\dfrac{8}{9\pi}\right)3^4=8.890$ |

$$\begin{gathered}A=18+9-14.137=12.863\ \text{m}^2 \\ \bar x=\frac{18(1.5)+9(4)-14.137(1.273)}{12.863}=\frac{45.0}{12.863}=3.498\ \text{m}\end{gathered}$$

Parallel-axis theorem about the centroidal axis $\bar y$ (through $\bar x=3.498$ m):

$$\begin{gathered}I_1=40.5+18(1.5-3.498)^2=112.4 \\ I_2=4.5+9(4-3.498)^2=6.77 \\ I_3=8.890+14.137(1.273-3.498)^2=78.87\end{gathered}$$

$$\boxed{I_{\bar y}=112.4+6.77-78.87=13.26\ \text{m}^4}$$

Check using the Y axis directly: $I_{Y}=(40.5+18(1.5)^2)+(4.5+9(4)^2)-\tfrac{\pi(3)^4}{8}=81.0+148.5-31.8=170.69$ m⁴, and $I_Y-A\bar x^2=170.69-12.863(3.498)^2=13.26$ m⁴ ✓.

@s 5
**(a) Kinematics versus kinetics.** *Kinematics* describes the motion of a particle along its path (position, velocity, acceleration against time) without asking why it moves; the relations are geometric: $v=ds/dt$, $a=dv/dt$. *Kinetics* relates the motion to the forces acting (Newton's second law $\sum\vec F=m\vec a$, work-energy, impulse-momentum) and so involves mass and force.

*Ski jumper.* Origin at the take-off point, $x$ horizontal, $y$ measured downward. $v_x=25$ m/s, $x=25t$, $y=\tfrac12gt^2$ with $g=9.81$ m/s². The hill is the line $y=x\tan30^\circ$.

*(i) Time of flight.* At landing $\tfrac12gt^2=25t\tan30^\circ$:

$$t=\frac{2(25)\tan30^\circ}{9.81}=\frac{28.87}{9.81}=\boxed{2.94\ \text{s}}$$

*(ii) Length of the jump.* $x=25(2.943)=73.57$ m, $y=\tfrac12(9.81)(2.943)^2=42.48$ m, so measured along the hill

$$d=\frac{x}{\cos30^\circ}=\frac{73.57}{0.8660}=\boxed{84.9\ \text{m}}$$

*(iii) Maximum vertical distance between jumper and hill.* At a given $x$ the vertical gap is $h=x\tan30^\circ-\dfrac{g x^2}{2v_0^2}$. For a maximum $dh/dx=0$:

$$\tan30^\circ=\frac{gx}{v_0^2}\Rightarrow x=\frac{625(0.5774)}{9.81}=36.78\ \text{m}\ (t=1.47\ \text{s})$$

$$h_{\max}=\tfrac12x\tan30^\circ=\tfrac12(36.78)(0.5774)=\boxed{10.6\ \text{m}}$$

(If the distance is taken perpendicular to the hill, the same method with $v_\perp=25\sin30^\circ=12.5$ m/s and $a_\perp=g\cos30^\circ$ gives $12.5^2/(2\times9.81\cos30^\circ)=9.20$ m.)

**(b) Work-energy principle.** For a particle of mass $m$ moving along its path under a resultant force $\vec F$, with $F_t=m\,dv/dt=m\,v\,dv/ds$ along the tangent (the normal component does no work because it is perpendicular to the displacement):

$$\begin{gathered}\int_{s_1}^{s_2}F_t\,ds=\int_{v_1}^{v_2}m\,v\,dv \\ U_{1\to2}=\tfrac12mv_2^2-\tfrac12mv_1^2=T_2-T_1\end{gathered}$$

So **the work done by all forces on a particle during a displacement equals the change in its kinetic energy**, $T_1+U_{1\to2}=T_2$. For conservative forces this becomes $T_1+V_1=T_2+V_2$.

*Pendulum.* $L=3$ m, $\theta=30^\circ$, cord tension $T=2W=2mg$. Along the cord (normal direction, towards O):

$$T-W\cos\theta=m\frac{v^2}{L}\ \Rightarrow\ 2mg-mg\cos30^\circ=\frac{mv^2}{L}$$

$$v^2=gL(2-\cos30^\circ)=9.81(3)(1.134)=33.37\ \Rightarrow\ \boxed{v=5.78\ \text{m/s}}$$

Acceleration components:

$$\begin{gathered}a_n=\frac{v^2}{L}=\frac{33.37}{3}=11.12\ \text{m/s}^2\ \text{(towards O)} \\ a_t=g\sin30^\circ=4.905\ \text{m/s}^2\ \text{(tangential, towards the mean position)}\end{gathered}$$

$$\boxed{a=\sqrt{a_n^2+a_t^2}=\sqrt{11.12^2+4.905^2}=12.16\ \text{m/s}^2}$$

directed at $\tan^{-1}(a_t/a_n)=23.8^\circ$ from the cord, towards the mean position.

@s 6
**(a) D'Alembert's principle for plane motion.** For a rigid body in plane motion the equations of motion are $\sum F_x=m\bar a_x$, $\sum F_y=m\bar a_y$ and $\sum M_G=\bar I\alpha$. D'Alembert's principle rewrites them as equilibrium equations: add to the real forces an **inertia force** $-m\vec{\bar a}$ acting at the centre of mass G (with components $-m\bar a_x$, $-m\bar a_y$) and an **inertia couple** $-\bar I\alpha$ opposing the angular acceleration. The body then satisfies

$$\begin{gathered}\sum\vec F+(-m\vec{\bar a})=\vec 0 \\ \sum M_G+(-\bar I\alpha)=0\end{gathered}$$

i.e. the real forces together with the reversed effective forces form a system in *dynamic equilibrium*, and the methods of statics (moments about any point) can be applied. The mass moment of inertia $\bar I$ is taken about the axis through G perpendicular to the plane.

**(b) Engine mechanism.** $r=AB=3$ in, $l=BD=8$ in, crank angle $\theta=40^\circ$ and

$$\omega_{AB}=2000\ \text{rpm}=\frac{2000(2\pi)}{60}=209.44\ \text{rad/s (clockwise)}$$

*Geometry.* $\sin\beta=\dfrac{r\sin\theta}{l}=\dfrac{3\sin40^\circ}{8}=0.2411\Rightarrow\beta=13.95^\circ$ (rod inclination).

*Velocity of B:* $v_B=r\omega_{AB}=3(209.44)=628.3$ in/s, perpendicular to AB; for a clockwise crank with B up and to the right, $\vec v_B=628.3(\sin40^\circ\,\hat i-\cos40^\circ\,\hat j)=(403.9,\,-481.3)$ in/s.

*Relative velocity.* $\vec v_D=\vec v_B+\vec\omega_{BD}\times\vec r_{D/B}$ with $\vec r_{D/B}=(l\cos\beta,\,-l\sin\beta)=(7.76,\,-1.93)$ in, and $\vec\omega_{BD}=\omega_{BD}\hat k$ so that $\vec\omega\times\vec r=\omega(1.93,\,7.76)$. The piston D moves horizontally, so the vertical component of $\vec v_D$ must vanish:

$$-481.3+7.76\,\omega_{BD}=0\ \Rightarrow\ \boxed{\omega_{BD}=62.0\ \text{rad/s (counter-clockwise)}}$$

*Piston velocity.*

$$v_P=v_D=403.9+1.93(62.0)=523.5\ \text{in/s}\ \Rightarrow\ \boxed{v_P\approx523\ \text{in/s}=43.6\ \text{ft/s}=13.3\ \text{m/s, to the right}}$$

Check by the closed form $v_P=r\omega\sin\theta\left(1+\dfrac{r\cos\theta}{l\cos\beta}\right)=628.3(0.6428)\left(1+\dfrac{2.298}{7.762}\right)=523.4$ in/s ✓.

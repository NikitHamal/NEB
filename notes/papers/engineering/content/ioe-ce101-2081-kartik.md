---
file: NEBians-IOE-Past-Paper-Engineering-Mechanics-CE101-2081-Kartik.pdf
subject: Engineering Mechanics
level: BE · Year I / Part I
code: CE 101
year_bs: 2081 Kartik
cal: BS
year_ad: 2024
stream: BCE, BAG
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define free body diagram. "Solid body is considered as perfectly rigid body in Engineering Mechanics" Justify the statement. [[2+2]]

b) The cylinder A and B rest in an inclined surface which makes an angle of 25° with horizontal as shown in figure below. Determine reaction at the contact points. Take: weight of cylinder A (W$_A$) = 200 N, weight of cylinder B (W$_B$) = 400 N, diameter of cylinder A (d$_A$) = 100 mm, diameter of cylinder B (d$_B$) = 150 mm. [[6]]

```figure caption="Question 1(b): cylinders A (d = 100 mm, 200 N) and B (d = 150 mm, 400 N) on a 25° incline, A pressed against a vertical wall."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.2,3.2)); ax.set_aspect("equal"); ax.axis("off")
th=_np.radians(25); L=330
ax.plot([0,0],[0,170],color=INK,lw=2); ax.plot([0,L*_np.cos(th)],[0,L*_np.sin(th)],color=INK,lw=2)
n=_np.array([-_np.sin(th),_np.cos(th)]); u=_np.array([_np.cos(th),_np.sin(th)])
rA,rB=50,75
cA=_np.array([rA,0.0]); cA[1]=rA/_np.cos(th)*0+ (rA*_np.cos(th)+rA*_np.sin(th)*0)  # placeholder, fixed below
# A touches the wall (x = rA) and the incline: centre height from line y = x tan(th)
cAx=rA; cAy=cAx*_np.tan(th)+rA/_np.cos(th)
phi=_np.arcsin((rB-rA)/(rA+rB)); d=_np.array([_np.cos(th+phi),_np.sin(th+phi)])*(rA+rB); cB=_np.array([cAx,cAy])+d
ax.add_patch(mp.Circle((cAx,cAy),rA,fc="#dbe7f5",ec=INK,lw=1.2)); ax.add_patch(mp.Circle(tuple(cB),rB,fc="#cfdcec",ec=INK,lw=1.2))
ax.text(cAx-4,cAy-4,"A",fontsize=9); ax.text(cB[0]-4,cB[1]-4,"B",fontsize=9)
ax.text(70,18,"25°",fontsize=8)
ax.set_xlim(-30,320); ax.set_ylim(-20,260)
```

@q 2
a) Find the magnitude, direction, and position of resultant force of the following system as shown in the Plate ABCD. [[4]]

```figure caption="Question 2(a): plate ABCD, 4 m × 3 m. 200 kN at A (leftwards), 400 kN at B (rightwards), 150 kN at C at 30° above the horizontal (pointing up-left) and 150 kN at D at 20° above the horizontal (pointing up-right)."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,3.0)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),4,3,fc="#eef2f8",ec=INK,lw=1.2))
a=dict(arrowstyle="-|>",color=INK,lw=1.4)
ax.annotate("",xy=(-1.4,3),xytext=(0,3),arrowprops=a); ax.text(-2.0,3.12,"200 kN",fontsize=8)
ax.annotate("",xy=(5.4,3),xytext=(4,3),arrowprops=a); ax.text(4.6,3.12,"400 kN",fontsize=8)
c,s=_np.cos,_np.sin; d=_np.radians
ax.annotate("",xy=(-1.3*c(d(30)),1.3*s(d(30))),xytext=(0,0),arrowprops=a); ax.text(-2.2,0.9,"150 kN",fontsize=8); ax.text(-0.9,0.1,"30°",fontsize=7)
ax.annotate("",xy=(4+1.3*c(d(20)),1.3*s(d(20))),xytext=(4,0),arrowprops=a); ax.text(5.3,0.6,"150 kN",fontsize=8); ax.text(4.55,0.1,"20°",fontsize=7)
for p,l,o in (((0,3),"A",(-0.25,0.2)),((4,3),"B",(0.1,0.2)),((0,0),"C",(-0.3,-0.5)),((4,0),"D",(0.1,-0.5))): ax.text(p[0]+o[0],p[1]+o[1],l,fontsize=9)
ar=dict(arrowstyle="<->",color=MUTED,lw=0.7)
ax.annotate("",xy=(0,-0.8),xytext=(4,-0.8),arrowprops=ar); ax.text(2,-1.3,"4 m",ha="center",fontsize=8)
ax.annotate("",xy=(6.6,0),xytext=(6.6,3),arrowprops=ar); ax.text(6.75,1.5,"3 m",fontsize=8,va="center")
ax.set_xlim(-2.5,7.4); ax.set_ylim(-1.8,3.9)
```

b) How can you assure the condition of tipping or sliding of a block? Explain with suitable diagram. [[3]]

@q 3
a) Derive an expression to show that area under the shear force curve between any two points is equal to change in bending moment between those two points. [[3]]

b) Draw axial force, shear force and bending moment diagram for the frame shown. Indicate salient points, if any. [[12]]

```figure caption="Question 3(b): portal frame ABCDEF. Pin at A, roller at F; 20 kN at B (rightwards, 4 m above A); 5 kN/m UDL on CD; 50 kN·m couple at D (clockwise); 40 kN at E (leftwards, 2 m above F). Heights AB = 4 m, BC = 2 m, DE = 4 m, EF = 2 m. The span CD is cut off at the foot of the scan: L = 4 m is assumed."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.6)); ax.set_aspect("equal"); ax.axis("off")
ax.plot([0,0,4,4],[0,6,6,0],color=INK,lw=2.2)
a=dict(arrowstyle="-|>",color=INK,lw=1.3)
ax.annotate("",xy=(0,4),xytext=(-1.4,4),arrowprops=a); ax.text(-2.2,4.15,"20 kN",fontsize=8)
ax.annotate("",xy=(4,2),xytext=(5.4,2),arrowprops=a); ax.text(5.0,2.15,"40 kN",fontsize=8)
for x in [0.3+0.47*i for i in range(8)]: ax.annotate("",xy=(x,6),xytext=(x,6.6),arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.plot([0,4],[6.6,6.6],color=INK,lw=0.8); ax.text(1.4,6.8,"5 kN/m",fontsize=8)
ax.add_patch(mp.Arc((4,6),1.0,1.0,theta1=-100,theta2=170,color=INK,lw=1.3)); ax.text(4.4,6.5,"50 kN·m",fontsize=8)
ax.add_patch(mp.Polygon([(0,0),(-0.3,-0.5),(0.3,-0.5)],closed=True,fc="white",ec=INK))
ax.add_patch(mp.Circle((4,-0.25),0.25,fc="white",ec=INK)); ax.plot([3.6,4.4],[-0.55,-0.55],color=INK)
for p,l,o in (((0,0),"A",(-0.5,-0.2)),((0,4),"B",(0.15,0.0)),((0,6),"C",(-0.5,0.1)),((4,6),"D",(0.15,-0.5)),((4,2),"E",(-0.5,0.1)),((4,0),"F",(0.4,-0.2))): ax.text(p[0]+o[0],p[1]+o[1],l,fontsize=9)
ax.set_xlim(-2.8,7); ax.set_ylim(-1.2,7.6)
```

@q 4
a) Explain the applicability of method of joint and section for the analysis of plane truss. Determine the force developed in all the members of the truss loaded as shown in figure below. [[1+4]]

```figure caption="Question 4(a): truss with joints A(0, 0), F(4, 0), E(8, 0) on the bottom chord and B(0, 4), C(4, 4), D(8, 4) on the top chord (m). Loads: 35 kN at B, 70 kN at C, 35 kN at D and 80 kN at F. A is pinned, E is on a roller."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,3.2)); ax.set_aspect("equal"); ax.axis("off")
P={"A":(0,0),"F":(4,0),"E":(8,0),"B":(0,4),"C":(4,4),"D":(8,4)}
for m in ("AB","BC","CD","DE","AF","FE","AC","CE","CF"):
    ax.plot([P[m[0]][0],P[m[1]][0]],[P[m[0]][1],P[m[1]][1]],color=INK,lw=1.6)
for k,(x,y) in P.items():
    ax.plot([x],[y],"o",color=INK,ms=4); ax.text(x+(-0.45 if x==0 else 0.2),y+(0.2 if y>1 else -0.6),k,fontsize=9)
a=dict(arrowstyle="-|>",color=INK,lw=1.3)
for x,t in ((0,"35 kN"),(4,"70 kN"),(8,"35 kN")):
    ax.annotate("",xy=(x,4),xytext=(x,5.4),arrowprops=a); ax.text(x+0.15,4.9,t,fontsize=8)
ax.annotate("",xy=(4,0),xytext=(4,-1.4),arrowprops=a); ax.text(4.15,-1.2,"80 kN",fontsize=8)
ax.add_patch(mp.Polygon([(0,0),(-0.35,-0.6),(0.35,-0.6)],closed=True,fc="white",ec=INK))
ax.add_patch(mp.Circle((8,-0.3),0.3,fc="white",ec=INK)); ax.plot([7.6,8.4],[-0.65,-0.65],color=INK)
ar=dict(arrowstyle="<->",color=MUTED,lw=0.7)
for x0,x1 in ((0,4),(4,8)): ax.annotate("",xy=(x0,-2.1),xytext=(x1,-2.1),arrowprops=ar); ax.text((x0+x1)/2,-2.7,"4 m",ha="center",fontsize=8)
ax.annotate("",xy=(9.2,0),xytext=(9.2,4),arrowprops=ar); ax.text(9.35,2,"4 m",fontsize=8,va="center")
ax.set_xlim(-1.5,10.5); ax.set_ylim(-3,6)
```

b) What are the basic differences between center of gravity and centroid? Determine the moment of inertia of the shaded area using method of integration about a horizontal axis which is b/2 distance from base. [[1+4]]

```figure caption="Question 4(b): area enclosed between the line y = mx and the parabola y = kx², from x = 0 to x = a, height b at x = a. The axis is at y = b/2."
import numpy as _np
fig,ax=plt.subplots(figsize=(3.8,3.2)); ax.axis("off")
x=_np.linspace(0,1,100); ax.fill_between(x,x**2,x,color="#cfdcec",alpha=0.9); ax.plot(x,x,color=INK,lw=1.4); ax.plot(x,x**2,color=INK,lw=1.4)
ax.annotate("",xy=(1.15,0),xytext=(-0.05,0),arrowprops=dict(arrowstyle="-|>",color=INK)); ax.annotate("",xy=(0,1.2),xytext=(0,-0.05),arrowprops=dict(arrowstyle="-|>",color=INK))
ax.plot([-0.05,1.05],[0.5,0.5],color="#c0392b",lw=1,ls="--"); ax.text(-0.04,0.53,"b/2",fontsize=8,color="#c0392b",ha="right")
ax.plot([1,1],[0,1],color=MUTED,lw=0.6,ls=":"); ax.text(1.02,0.5,"b",fontsize=8); ax.text(0.5,-0.1,"a",fontsize=8,ha="center")
ax.text(0.2,0.45,"y = mx",fontsize=8,rotation=40); ax.text(0.7,0.25,"y = kx²",fontsize=8)
ax.text(1.17,-0.03,"x",fontsize=9); ax.text(0.02,1.2,"y",fontsize=9)
ax.set_xlim(-0.25,1.3); ax.set_ylim(-0.2,1.3)
```

@q 5
a) Derive an expression for radial and transverse component of velocity and acceleration for a particle moving along a curved path. The motion of a particle is defined by the relation x = t² − 10t + 30, where x is expressed in meter and t in second. Determine the position and total distance travelled when t = 8 sec. [[3+3]]

b) Differentiate between conservative and non-conservative forces with examples. Two block A and B having respective weights 500 N and 1000 N starts from rest. The pulley is friction less and practically mass less. The kinetic coefficient of friction between the block A and the inclined surface is 0.35. Determine the acceleration of each block and tension in the cord. [[1+5]]

```figure caption="Question 5(b): block A (500 N) on a 15° incline joined by a cord over the fixed pulley D to the movable pulley C that carries block B (1000 N); the other end of the cord is fixed. The incline falls towards D, so when B descends A is dragged up the incline."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.8,3.6)); ax.set_aspect("equal"); ax.axis("off")
th=_np.radians(15); xd=6.0; yd=0.0
ax.plot([0,xd],[xd*_np.tan(th),0],color=INK,lw=2)
ax.add_patch(mp.Rectangle((0,0),1,1,angle=-15,rotation_point=(0,0),fc="#dbe7f5",ec=INK,lw=1.2)) if False else None
bx=1.4; by=(xd-bx)*_np.tan(th)
ax.add_patch(mp.Rectangle((bx,by),1.0,0.8,angle=-15,rotation_point=(bx,by),fc="#dbe7f5",ec=INK,lw=1.2)); ax.text(bx+0.3,by+0.95,"A (500 N)",fontsize=8)
ax.add_patch(mp.Circle((xd,yd),0.28,fc="white",ec=INK)); ax.text(xd+0.4,yd+0.1,"D",fontsize=9)
ax.plot([bx+0.5,xd],[by+0.3,yd+0.28],color=INK,lw=1)
ax.plot([xd-0.28,xd-0.28],[yd,-4.2],color=INK,lw=1); ax.plot([xd+0.28,xd+0.28],[yd,-4.2],color=INK,lw=1)
ax.add_patch(mp.Circle((xd,-4.2),0.28,fc="white",ec=INK)); ax.text(xd+0.4,-4.1,"C",fontsize=9)
ax.plot([xd,xd],[-4.5,-5.0],color=INK,lw=1)
ax.add_patch(mp.Rectangle((xd-0.6,-6.2),1.2,1.2,fc="#cfdcec",ec=INK,lw=1.2)); ax.text(xd-0.55,-5.8,"B 1000 N",fontsize=7)
ax.plot([xd+0.28,xd+0.28],[-4.2,0],color=INK,lw=1)
ax.add_patch(mp.Rectangle((xd+1.0,-4.2),0.2,4.2,fc="#ddd",ec=INK,lw=0.5,hatch="////"))
ax.plot([xd+0.28,xd+1.0],[yd,yd],color=INK,lw=1) if False else None
ax.text(1.0,0.0,"15°",fontsize=8)
ax.set_xlim(-0.3,8.5); ax.set_ylim(-6.6,2.4)
```

@q 6
a) Derive an expression for kinetic energy in plane motion of rigid body. [[2]]

b) Load B is connected to a double pulley by one of the two inextensible cables as shown in fig. The motion of the pulley is controlled by cable C, which has a constant acceleration of 225 mm/sec² and an initial velocity of 300 mm/sec, both directed to the right. Determine (i) the number of revolutions executed by the pulley in 2 sec (ii) the velocity and change in position of the load B after 2 sec. [[4]]

```figure caption="Question 6(b): double pulley, inner radius 75 mm and outer radius 125 mm, turning about the fixed centre A. Cable C leaves the inner pulley at D (top); the cable carrying load B is wound on the outer pulley."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.0,3.4)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Circle((0,0),125,fc="#eef2f8",ec=INK,lw=1.3)); ax.add_patch(mp.Circle((0,0),75,fc="#cfdcec",ec=INK,lw=1.3))
ax.plot([0],[0],"o",color=INK,ms=4); ax.text(8,-22,"A",fontsize=9)
ax.plot([0,260],[75,75],color=INK,lw=1.6); ax.text(265,70,"C",fontsize=9); ax.text(-10,82,"D",fontsize=9)
ax.annotate("",xy=(330,75),xytext=(270,75),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2))
ax.plot([-125,-125],[0,-190],color=INK,lw=1.6); ax.add_patch(mp.Rectangle((-145,-235),40,40,fc="#cfdcec",ec=INK)); ax.text(-132,-222,"B",fontsize=9)
ar=dict(arrowstyle="<->",color=MUTED,lw=0.7)
ax.plot([0,-88],[0,88],color=MUTED,lw=0.6); ax.text(-70,30,"75 mm",fontsize=7,rotation=0)
ax.plot([0,88],[0,-88],color=MUTED,lw=0.6); ax.text(30,-110,"125 mm",fontsize=7)
ax.set_xlim(-190,360); ax.set_ylim(-250,160)
```

<!-- SOLUTIONS -->

@s 1
**(a) Free body diagram.** A *free body diagram* (FBD) is a sketch of a body (or part of a structure) isolated from its surroundings, on which *all* the external forces acting on it are drawn: the applied loads, its weight and the reactions of every support or contact that was removed. It is the first step of any equilibrium problem, because the equations $\sum F=0$, $\sum M=0$ are written for the forces shown on it.

*Why a solid is treated as perfectly rigid.* Real solids deform when loaded, but in engineering structures the deformation is tiny (strains of the order $10^{-3}$) compared with the dimensions of the body. Therefore the geometry used to compute lever arms and the lines of action of forces does not change measurably between the unloaded and loaded states, and the equations of equilibrium can be applied to the original geometry. Rigidity thus makes the problem tractable and gives results correct for practical purposes; deformation (elasticity) is treated separately in Strength of Materials.

**(b) Cylinders on the incline.** Radii $r_A=50$ mm, $r_B=75$ mm; all contacts smooth, so every reaction is normal to the surface. The incline reaction is perpendicular to the plane (at $25^\circ$ to the vertical), the wall reaction is horizontal and the reaction between the cylinders acts along the line of centres.

*Direction of the line of centres.* Both centres are at perpendicular distances $r_A$ and $r_B$ from the incline and are $r_A+r_B=125$ mm apart. So the line of centres makes an angle $\varphi$ with the incline where

$$\sin\varphi=\frac{r_B-r_A}{r_A+r_B}=\frac{25}{125}=0.2\ \Rightarrow\ \varphi=11.54^\circ$$

so the line from A to B is inclined at $\theta=25^\circ+11.54^\circ=36.54^\circ$ to the horizontal.

*Cylinder B* (weight 400 N, forces: $N_B$ perpendicular to the incline, $P$ from A along the line of centres, weight):

$$\begin{gathered}\sum F_x=0:\ -N_B\sin25^\circ+P\cos36.54^\circ=0 \\ \sum F_y=0:\ N_B\cos25^\circ+P\sin36.54^\circ-400=0\end{gathered}$$

From the first, $P=N_B\sin25^\circ/\cos36.54^\circ=0.5262\,N_B$. Substituting in the second:

$$\begin{gathered}N_B(0.9063+0.5262\times0.5953)=400\ \Rightarrow\ N_B=\frac{400}{1.2195}=\boxed{328.0\ \text{N}} \\ P=\boxed{172.5\ \text{N}}\end{gathered}$$

*Cylinder A* (weight 200 N; $N_A$ from the incline, $R_w$ from the wall, force $P$ from B acting down-left along the line of centres):

$$\begin{gathered}\sum F_y=0:\ N_A\cos25^\circ-P\sin36.54^\circ-200=0 \Rightarrow N_A=\frac{200+102.7}{0.9063}=\boxed{334.0\ \text{N}} \\ \sum F_x=0:\ R_w-N_A\sin25^\circ-P\cos36.54^\circ=0 \Rightarrow R_w=141.2+138.6=\boxed{279.8\ \text{N}}\end{gathered}$$

| Contact | Reaction |
|---|---|
| A with the incline | 334.0 N, perpendicular to the incline |
| A with the vertical wall | 279.8 N, horizontal |
| A with B | 172.5 N, along the line of centres (36.54° to the horizontal) |
| B with the incline | 328.0 N, perpendicular to the incline |

Check: for the whole system, $\sum F_y$: $N_A\cos25^\circ+N_B\cos25^\circ=(334.0+328.0)(0.9063)=600.0=200+400$ ✓.

@s 2
**(a) Resultant of the plate system.** Origin at C (bottom-left), $x$ to the right, $y$ up; A $(0,3)$, B $(4,3)$, C $(0,0)$, D $(4,0)$. Reading: 200 kN at A acts to the left, 400 kN at B to the right, the 150 kN at C is directed up-left at $30^\circ$ and the 150 kN at D up-right at $20^\circ$ to the horizontal. Moments counter-clockwise (+), $M=xF_y-yF_x$.

| Force | Point | $F_x$ (kN) | $F_y$ (kN) | $M_C$ (kN·m) |
|---|---|---|---|---|
| 200 kN | A (0, 3) | $-200.0$ | 0 | $-3(-200)=+600.0$ |
| 400 kN | B (4, 3) | $+400.0$ | 0 | $-3(400)=-1200.0$ |
| 150 kN, 30° | C (0, 0) | $-150\cos30^\circ=-129.90$ | $150\sin30^\circ=+75.00$ | 0 |
| 150 kN, 20° | D (4, 0) | $150\cos20^\circ=+140.95$ | $150\sin20^\circ=+51.30$ | $4(51.30)=+205.21$ |
| **Sum** | | $R_x=+211.05$ | $R_y=+126.30$ | $M_C=-394.79$ |

$$\begin{gathered}R=\sqrt{211.05^2+126.30^2}=\boxed{245.96\ \text{kN}} \\ \theta=\tan^{-1}\frac{126.30}{211.05}=\boxed{30.9^\circ\ \text{above the }+x\text{ axis (up and to the right)}}\end{gathered}$$

*Position.* The resultant must give $M_C=-394.79$ kN·m (clockwise). With $M=xR_y-yR_x$:

- Where it crosses the base line CD extended ($y=0$): $x=\dfrac{-394.79}{126.30}=-3.13$ m, i.e. **3.13 m to the left of C** on the line CD produced.
- Where it crosses the left side CA ($x=0$): $y=\dfrac{394.79}{211.05}=\boxed{1.87\ \text{m above C}}$.

So the resultant of 245.96 kN, inclined at $30.9^\circ$, acts through the point on side CA at 1.87 m above C (equivalent to a force through C with a clockwise couple of 394.79 kN·m).

**(b) Tipping or sliding of a block.** Consider a block of weight $W$, width $b$ and height $h$ on a rough horizontal floor (coefficient of static friction $\mu$), pushed by a horizontal force $P$ applied at height $y$ above the floor.

```figure caption="Block of weight W pushed by P at height y: sliding is checked by P against mu W, tipping by the moment of P against W b/2 about the toe."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.4,2.4)); ax.set_aspect("equal"); ax.axis("off")
ax.plot([-1,6],[0,0],color=INK,lw=2)
ax.add_patch(mp.Rectangle((1,0),2,2.4,fc="#dbe7f5",ec=INK,lw=1.2))
a=dict(arrowstyle="-|>",color=INK,lw=1.4)
ax.annotate("",xy=(1,1.7),xytext=(-0.4,1.7),arrowprops=a); ax.text(-0.9,1.9,"P",fontsize=9)
ax.annotate("",xy=(2,0.9),xytext=(2,2.0),arrowprops=dict(arrowstyle="-|>",color="#c0392b",lw=1.4)); ax.text(2.1,1.9,"W",fontsize=9)
ax.annotate("",xy=(2.9,0),xytext=(2.9,0.9),arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1.1)); ax.text(3.0,0.5,"N",fontsize=8)
ax.annotate("",xy=(1.1,0.0),xytext=(2.1,0.0),arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1.1)); ax.text(1.4,-0.5,"F",fontsize=8)
ax.plot([3,3],[0,-0.4],color=INK,lw=0.8); ax.text(3.15,-0.6,"tipping edge",fontsize=7)
ax.annotate("",xy=(1,2.9),xytext=(3,2.9),arrowprops=dict(arrowstyle="<->",lw=0.7)); ax.text(2,3.0,"b",ha="center",fontsize=8)
ax.annotate("",xy=(0.6,0),xytext=(0.6,1.7),arrowprops=dict(arrowstyle="<->",lw=0.7)); ax.text(0.3,0.8,"y",fontsize=8,ha="right")
ax.set_xlim(-1.2,6); ax.set_ylim(-1,3.4)
```

*Sliding.* Vertical equilibrium gives $N=W$, so the limiting friction is $F_{\max}=\mu N=\mu W$. The block **slides** when $P>\mu W$ and stays at rest in this respect while $P\le\mu W$.

*Tipping* (about the lower toe at the right edge). The overturning moment is $Py$ and the restoring moment of the weight is $W\,b/2$. The block **tips** when

$$Py\ge W\frac b2\ \Rightarrow\ P\ge\frac{Wb}{2y}.$$

*Which happens first?* Sliding occurs first if $\mu W<\dfrac{Wb}{2y}$, i.e. $\mu<\dfrac{b}{2y}$; otherwise the block tips before it slides. The same two checks are made for dams and retaining walls (the resultant must stay inside the middle third to avoid tipping and $F/N\le\mu$ to avoid sliding). For an inclined plane the block tips if the vertical through G falls outside the base, $\tan\alpha>b/h$, and slides if $\tan\alpha>\mu$.

@s 3
**(a) Area under the shear diagram equals the change in bending moment.** Take an element of length $dx$ of a beam carrying a distributed load $w(x)$ (downward). Let the shear and moment at the left face be $V$ and $M$ and at the right face $V+dV$ and $M+dM$.

*Vertical equilibrium:* $V-w\,dx-(V+dV)=0\Rightarrow\dfrac{dV}{dx}=-w$.

*Moments about the right face:* $M+V\,dx-w\,dx\,\dfrac{dx}{2}-(M+dM)=0$. Neglecting the second-order term $w\,dx^2/2$:

$$dM=V\,dx\ \Rightarrow\ \frac{dM}{dx}=V.$$

Integrating between sections 1 and 2:

$$\boxed{M_2-M_1=\int_{x_1}^{x_2}V\,dx=\text{area under the shear force diagram between 1 and 2}}$$

(For a point couple $M_0$ the bending moment jumps by $M_0$; this is the only exception.)

**(b) Frame.** The dimension of the span CD is cut off at the foot of the scan. A span $L=4$ m is assumed (so the UDL is $5\times4=20$ kN). Coordinates: A $(0,0)$, B $(0,4)$, C $(0,6)$, D $(4,6)$, E $(4,2)$, F $(4,0)$. The 20 kN at B acts to the right, the 40 kN at E to the left and the 50 kN·m couple at D is clockwise.

*Reactions* (pin A: $A_x$, $A_y$; roller F: $F_y$ vertical). Moments about A (counter-clockwise +):

$$\begin{gathered}-20(4)+40(2)-20(2)-50+F_y(4)=0 \\ \Rightarrow F_y=\frac{80-80+40+50}{4}=\boxed{22.5\ \text{kN}\ \uparrow}\end{gathered}$$

$$\begin{gathered}\sum F_x=0:\ A_x+20-40=0 \Rightarrow A_x=\boxed{20\ \text{kN}\ \rightarrow} \\ \sum F_y=0:\ A_y+22.5-20=0 \Rightarrow A_y=\boxed{-2.5\ \text{kN (2.5 kN downward)}}\end{gathered}$$

*Member AB–BC (left column).* Axial: the 2.5 kN downward reaction pulls on the column: **tension 2.5 kN**. Shear: 20 kN between A and B, and $20+20=40$ kN between B and C (the 20 kN at B acts in the same direction as $A_x$). Moment (tension on the outer, left face): $M=20y$ for $0\le y\le4$ so $M_B=80$ kN·m, then $M=20y+20(y-4)$, giving $M_C=160$ kN·m.

*Member CD (beam).* Left of the section at $x$ from C: horizontal force $20+20=40$ kN to the right, so axial **compression 40 kN**. Shear (magnitude) $V=2.5+5x$: 2.5 kN at C rising linearly to 22.5 kN at D. Moment (tension on top):

$$M(x)=160+2.5x+2.5x^2\ \Rightarrow\ M_C=160,\ M_D=160+10+40=210\ \text{kN·m}$$

No zero of shear exists on CD, so the maximum is at D.

*Member DE–EF (right column).* Axial: **compression 22.5 kN** throughout (the roller reaction). Shear: nothing below E (the roller gives no horizontal force), and 40 kN between E and D. Moment (tension on the outer, right face): zero from F to E, then $M=40(y-2)$ rising to $160$ kN·m at D (below the couple).

*Joint checks.* Joint C: column 160 = beam 160 ✓. Joint D: the beam end moment 210 equals the column moment 160 plus the applied couple 50 kN·m ✓. Vertical equilibrium at the joints: 2.5 kN at C ✓; the beam shear 22.5 kN at D equals the column axial 22.5 kN ✓. Horizontal: 40 kN beam axial equals the column shear 40 kN ✓.

| Member | Axial (kN) | Shear (kN) | Bending moment (kN·m) |
|---|---|---|---|
| AB | 2.5 T | 20 | 0 at A, 80 at B |
| BC | 2.5 T | 40 | 80 at B, 160 at C |
| CD | 40 C | 2.5 at C, 22.5 at D | 160 at C, **210 at D** (parabola) |
| DE | 22.5 C | 40 | 160 at D, 0 at E |
| EF | 22.5 C | 0 | 0 |

*Salient points:* maximum bending moment 210 kN·m at the beam end of joint D (tension on top); a 50 kN·m jump at D from the couple; $M=0$ at both supports; moment is zero over EF; maximum shear 40 kN; maximum axial force 40 kN (compression in CD).

```figure caption="Question 3(b): axial force, shear force and bending moment diagrams of the frame (values in kN and kN·m; the moment is drawn on the tension side)."
import numpy as _np
fig,axs=plt.subplots(1,3,figsize=(6.6,3.3))
mem={"L":((0,0),(0,1),(-1,0)),"T":((0,6),(1,0),(0,1)),"R":((4,6),(0,-1),(1,0))}
def panel(a,title,data,sc,c,lab):
    a.set_aspect("equal"); a.axis("off"); a.set_title(title,fontsize=8)
    a.plot([0,0,4,4],[0,6,6,0],color=INK,lw=1.6)
    for k,pts in data.items():
        b,u,n=mem[k]; pts=_np.array(pts,float)
        xs=b[0]+pts[:,0]*u[0]+sc*pts[:,1]*n[0]; ys=b[1]+pts[:,0]*u[1]+sc*pts[:,1]*n[1]
        bx=b[0]+pts[:,0]*u[0]; by=b[1]+pts[:,0]*u[1]
        a.fill(_np.concatenate([bx,xs[::-1]]),_np.concatenate([by,ys[::-1]]),color=c,alpha=0.25); a.plot(xs,ys,color=c,lw=1.3)
    for (x,y,t) in lab: a.text(x,y,t,fontsize=6.5)
    a.set_xlim(-2.6,6.6); a.set_ylim(-0.5,8.4)
xb=_np.linspace(0,4,21)
panel(axs[0],"Axial force (kN)",{"L":[(0,2.5),(6,2.5)],"T":[(0,40),(4,40)],"R":[(0,22.5),(6,22.5)]},0.03,"#8e44ad",[(-2.4,3,"2.5 T"),(1.4,7.4,"40 C"),(4.9,3,"22.5 C")])
panel(axs[1],"Shear force (kN)",{"L":[(0,20),(4,20),(4,40),(6,40)],"T":[(0,2.5),(4,22.5)],"R":[(0,40),(4,40),(4,0),(6,0)]},0.04,"#2c6fb0",[(-2.4,2,"20"),(-2.4,5,"40"),(0.1,7.3,"2.5"),(3.0,7.8,"22.5"),(5.3,4,"40")])
panel(axs[2],"Bending moment (kN·m)",{"L":[(0,0),(4,80),(6,160)],"T":[(x,160+2.5*x+2.5*x**2) for x in xb],"R":[(0,160),(4,0),(6,0)]},0.011,"#c0392b",[(-2.5,3.5,"80"),(-2.5,6.0,"160"),(1.3,8.2,"160 → 210"),(4.9,6.2,"160")])
fig.tight_layout()
```

@s 4
**(a) Method of joints and method of sections.**

- **Method of joints**: each pin is a concurrent force system, so two equations $\sum F_x=0$, $\sum F_y=0$ are available per joint. It is applicable to any determinate truss (start at a joint with at most two unknown member forces) and is the best choice when the forces in *all* members are needed.
- **Method of sections**: the truss is cut by a section through at most three members (not all concurrent, not all parallel) and the equilibrium of one part ($\sum F_x,\ \sum F_y,\ \sum M$) gives the three forces directly, with moments taken about the intersection of two of them. It is best when only a few members (in a large truss) are wanted or to check a joint solution. Both methods need the truss to be statically determinate, $m+r=2j$, and pin-jointed with loads at joints only.

*Truss analysis.* Joints $j=6$, members $m=9$, reactions $r=3$: $9+3=12=2j$ ✓. Members: AB, BC, CD, DE (top chord and end posts), AF, FE (bottom chord), AC, CE (diagonals) and CF (post). By symmetry of both truss and loading: $A_x=0$ and $A_y=E_y=\dfrac{35+70+35+80}{2}=110$ kN.

*Joint B* (35 kN down; members BA vertical and BC horizontal): the load is along BA and the two members are not collinear, so **BC = 0** (zero-force member) and $F_{AB}=-35$ kN (35 kN compression). Similarly at *joint D*: **CD = 0** and $F_{DE}=-35$ kN.

*Joint A* (reaction 110 kN up, members AB, AC at 45°, AF):

$$\begin{gathered}\sum F_y=0:\ 110-35+F_{AC}\sin45^\circ=0 \Rightarrow F_{AC}=-106.07\ \text{kN} \\ \sum F_x=0:\ F_{AF}+F_{AC}\cos45^\circ=0 \Rightarrow F_{AF}=+75\ \text{kN}\end{gathered}$$

By symmetry $F_{CE}=-106.07$ kN and $F_{FE}=+75$ kN.

*Joint F* (80 kN down, AF = FE = 75 kN tension pulling horizontally, post CF): $\sum F_y=0$ gives $F_{CF}-80=0$, so $F_{CF}=+80$ kN (tension).

*Check at joint C:* downward loads $70+80=150$ kN (the load plus the tension in CF pulling down) against the vertical components of AC and CE: $2\times106.07\sin45^\circ=150$ kN ✓; horizontally the two diagonals balance each other and BC = CD = 0 ✓.

| Member | AB | BC | CD | DE | AF | FE | AC | CE | CF |
|---|---|---|---|---|---|---|---|---|---|
| Force (kN) | 35 C | 0 | 0 | 35 C | 75 T | 75 T | 106.07 C | 106.07 C | 80 T |

**(b) Centre of gravity versus centroid.**

| Centre of gravity | Centroid |
|---|---|
| Point through which the whole *weight* of the body acts | Geometric centre of a *line, area or volume* |
| Depends on the distribution of mass and on gravity | Depends only on the shape (geometry) |
| Defined for bodies (3-D) | Defined for lines, plane areas and volumes |
| Coincides with the centroid only for a homogeneous body in a uniform gravitational field | Same as the centre of mass of a homogeneous body |

*Moment of inertia by integration.* The line $y=mx$ and the parabola $y=kx^2$ both pass through $(a,b)$, so $m=\dfrac ba$ and $k=\dfrac b{a^2}$; between $x=0$ and $x=a$ the line is above the parabola. Take a vertical strip of width $dx$ extending from $y_1=kx^2$ to $y_2=mx$. About the horizontal axis $y=b/2$:

$$dI=\int_{y_1}^{y_2}\left(y-\frac b2\right)^2dy\,dx=\frac{1}{3}\left[\left(mx-\frac b2\right)^3-\left(kx^2-\frac b2\right)^3\right]dx$$

$$I=\frac13\int_0^a\left[\left(\frac{b x}{a}-\frac b2\right)^3-\left(\frac{b x^2}{a^2}-\frac b2\right)^3\right]dx$$

Evaluating with $x=a\xi$: $\displaystyle\int_0^1\left(\xi-\tfrac12\right)^3d\xi=0$ (odd about $\xi=\tfrac12$) and $\displaystyle\int_0^1\left(\xi^2-\tfrac12\right)^3d\xi=\tfrac17-\tfrac{3}{10}+\tfrac14-\tfrac18=-\tfrac{9}{280}$, so $I=\dfrac{ab^3}{3}\left(0+\dfrac{9}{280}\right)$, i.e.

$$\boxed{I_{y=b/2}=\frac{3\,ab^3}{280}}$$

*Check by the parallel-axis theorem.* Area $A=\int_0^a(mx-kx^2)dx=\dfrac{ab}{6}$; centroid height $\bar y=\dfrac{2b}{5}$; moment of inertia about the base $\int\tfrac13(y_2^3-y_1^3)dx=\dfrac{ab^3}{28}$, so about the centroid $I_c=\dfrac{ab^3}{28}-\dfrac{ab}{6}\left(\dfrac{2b}{5}\right)^2=\dfrac{19ab^3}{2100}$. The axis $y=b/2$ is $d=\dfrac b2-\dfrac{2b}{5}=\dfrac b{10}$ from the centroid:

$$I=\frac{19ab^3}{2100}+\frac{ab}{6}\cdot\frac{b^2}{100}=\frac{38+7}{4200}ab^3=\frac{3ab^3}{280}\ \checkmark$$

@s 5
**(a) Radial and transverse components.** Let the position of a particle be $\vec r=r\,\hat e_r$ in polar coordinates $(r,\theta)$. The unit vectors rotate with $\theta$: $\dot{\hat e}_r=\dot\theta\,\hat e_\theta$ and $\dot{\hat e}_\theta=-\dot\theta\,\hat e_r$.

*Velocity:*

$$\vec v=\dot{\vec r}=\dot r\,\hat e_r+r\dot\theta\,\hat e_\theta\ \Rightarrow\ v_r=\dot r,\quad v_\theta=r\dot\theta,\quad v=\sqrt{v_r^2+v_\theta^2}$$

*Acceleration:*

$$\vec a=\dot{\vec v}=(\ddot r-r\dot\theta^2)\,\hat e_r+(r\ddot\theta+2\dot r\dot\theta)\,\hat e_\theta\ \Rightarrow\ a_r=\ddot r-r\dot\theta^2,\quad a_\theta=r\ddot\theta+2\dot r\dot\theta$$

*Rectilinear motion* $x=t^2-10t+30$ (m). Then $v=\dfrac{dx}{dt}=2t-10$ and $a=2$ m/s².

At $t=8$ s: $x=64-80+30=\boxed{14\ \text{m}}$ and $v=+6$ m/s. At $t=0$, $x_0=30$ m and $v_0=-10$ m/s; the velocity is zero when $t=5$ s, where $x=25-50+30=5$ m. So the particle first moves in the negative direction for 5 s (30 m to 5 m) and then reverses.

$$\text{Distance}=|5-30|+|14-5|=25+9=\boxed{34\ \text{m}}$$

(The displacement is only $14-30=-16$ m.)

**(b) Conservative and non-conservative forces.**

| Conservative | Non-conservative |
|---|---|
| Work done depends only on the end points, not on the path; work around a closed path is zero | Work depends on the path; work around a closed path is not zero |
| Mechanical energy is conserved; a potential energy exists | Mechanical energy is dissipated (as heat, sound) |
| Weight, spring force, gravitation, electrostatic force | Friction, air drag, viscous forces, a human push |

*Blocks.* The cord from A passes over the fixed pulley D and down to the movable pulley C, which carries B; the cord then goes up to a fixed support. If B moves down by $y_B$ the cord on the incline side lengthens by $2y_B$, so A moves up the incline twice as far: $a_A=2a_B$. Since B (1000 N) is heavy enough to pull A up the incline (checked below), take A moving up the incline and B moving down.

*Block A* (mass $500/9.81$ kg; friction opposes motion, down the incline):

$$T-500\sin15^\circ-0.35(500\cos15^\circ)=\frac{500}{9.81}(2a_B)$$

$$T-129.41-169.04=101.94\,a_B$$

*Block B plus pulley C* (the pulley is carried by two cord segments, each with tension $T$):

$$1000-2T=\frac{1000}{9.81}a_B=101.94\,a_B$$

Substituting $T=500-50.97\,a_B$ from the second equation into the first:

$$500-50.97a_B-298.45=101.94a_B\ \Rightarrow\ a_B=\frac{201.55}{152.91}=\boxed{1.318\ \text{m/s}^2\ \downarrow}$$

$$\begin{gathered}\boxed{a_A=2a_B=2.636\ \text{m/s}^2\ \text{up the incline}} \\ \boxed{T=500-50.97(1.318)=432.8\ \text{N}}\end{gathered}$$

Check: with the cord taut, the pull needed to start A is $T=298.45$ N and the available $T=500$ N (when $a=0$) is bigger, so the system does move as assumed; the resulting forces on B: $1000-2(432.8)=134.4$ N $=101.94\times1.318$ ✓.

@s 6
**(a) Kinetic energy in plane motion.** For a rigid body of mass $m$ in plane motion with angular velocity $\omega$, let G be the mass centre with velocity $\bar v$. A particle $dm$ at position $\vec\rho$ from G has velocity $\vec v=\vec{\bar v}+\vec\omega\times\vec\rho$. Then

$$T=\tfrac12\int v^2\,dm=\tfrac12\bar v^2\int dm+\vec{\bar v}\cdot\left(\vec\omega\times\int\vec\rho\,dm\right)+\tfrac12\omega^2\int\rho^2\,dm$$

The middle term vanishes because $\int\vec\rho\,dm=\vec 0$ (G is the origin). With $\bar I=\int\rho^2dm$:

$$\boxed{T=\tfrac12m\bar v^2+\tfrac12\bar I\omega^2}$$

The first term is the kinetic energy of translation of G and the second that of rotation about G. For rotation about a fixed axis O this reduces to $T=\tfrac12I_O\omega^2$.

**(b) Double pulley.** The pulley turns about the fixed centre A. Cable C leaves the inner pulley (radius $r_i=75$ mm) at the top point D, so the speed of that point is that of the cable: $v_D=v_C$, with $v_C(0)=300$ mm/s and $a_C=225$ mm/s² to the right. A top point moving right means a **clockwise** rotation. The cable carrying B is on the outer pulley ($r_o=125$ mm).

*Angular motion* (constant acceleration):

$$\begin{gathered}\omega_0=\frac{300}{75}=4\ \text{rad/s} \\ \alpha=\frac{225}{75}=3\ \text{rad/s}^2\end{gathered}$$

**(i) Revolutions in 2 s:**

$$\begin{gathered}\theta=\omega_0t+\tfrac12\alpha t^2=4(2)+\tfrac12(3)(2)^2=14\ \text{rad} \\ N=\frac{14}{2\pi}=\boxed{2.23\ \text{revolutions}}\end{gathered}$$

**(ii) Load B after 2 s.** Load B has the speed of the point on the outer rim to which its cable is attached.

$$\begin{gathered}\omega=\omega_0+\alpha t=4+3(2)=10\ \text{rad/s} \\ v_B=r_o\omega=125(10)=\boxed{1250\ \text{mm/s}} \\ \Delta y_B=r_o\theta=125(14)=\boxed{1750\ \text{mm}}\end{gathered}$$

Because the pulley turns clockwise and the cable of B hangs from the left side of the outer pulley (the side that moves upward), **B moves up**: velocity 1.25 m/s upward and a rise of 1.75 m in 2 s. (If cable C were attached at the bottom of the inner pulley, the sense of rotation and the direction of B would both be reversed; the magnitudes are the same.)

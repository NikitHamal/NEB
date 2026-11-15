---
file: NEBians-IOE-Past-Paper-Engineering-Mechanics-ENCE101-2081-Chaitra.pdf
subject: Engineering Mechanics
level: BE · Year I / Part I
code: ENCE 101
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE, BAG
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course), BE Civil and Agriculture, Year I / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define free body diagram with example. A smooth cylinder of weight 500 N is supported in contact with a smooth vertical wall by a string attached to a point on its surface, the end being attached to a point on the wall. If the length of the string is equal to the diameter of the cylinder, find tension in the string and reaction on the wall. [[1.5+3.5]]

```figure caption="Question 1: cylinder (centre O, radius r, weight 500 N) touching the smooth wall at B and held by a string AS of length 2r, A on the wall and S on the cylinder."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(2.8,3.3)); ax.set_aspect("equal"); ax.axis("off")
ax.plot([0,0],[-1.4,4.2],color=INK,lw=2); 
for y in _np.arange(-1.4,4.2,0.4): ax.plot([0,-0.25],[y,y-0.25],color=MUTED,lw=0.8)
ax.add_patch(mp.Circle((1,0),1,fc="#dbe7f5",ec=INK,lw=1.3)); ax.plot([1],[0],"o",color=INK,ms=3)
a=_np.arcsin(1/3); A=(0,3*_np.cos(a)); ax.plot([A[0],1-_np.sin(a)*1*1],[A[1],_np.cos(a)*1*1],color=INK,lw=1.6)
ax.text(0.12,A[1],"A",fontsize=9); ax.text(0.12,-0.3,"B",fontsize=9); ax.text(1.1,-0.35,"O",fontsize=9)
ax.set_xlim(-0.6,2.4); ax.set_ylim(-1.5,3.4)
```

@q 2
Determine resultant force-couple system of the following system of forces about O and obtain an equivalent wrench with line of action. [[4+5]]

```figure caption="Question 2: box 5 m (x) × 4 m (y) × 3 m (z), origin O at the rear bottom left corner. Forces: 200 kN from the front-bottom-left corner and 100 kN from the front-bottom-right corner, both directed towards the top-rear-left corner P (0, 4, 0); 10 kN upward at P; 10 kN downward at the front-bottom-right corner; three couples: a pair of 70 kN vertical forces 2 m apart on the top face, a pair of 80 kN forces (parallel to z) 3 m apart on the bottom face and a pair of 200 kN forces (parallel to z) 2.5 m apart on the right face."
import numpy as _np
fig,ax=plt.subplots(figsize=(5.6,3.6)); ax.set_aspect("equal"); ax.axis("off")
S=lambda x,y,z:(x-0.5*z,y-0.38*z)
def L(p,q,**k): a=S(*p);b=S(*q); ax.plot([a[0],b[0]],[a[1],b[1]],**k)
V=[(0,0,0),(5,0,0),(5,4,0),(0,4,0),(0,0,3),(5,0,3),(5,4,3),(0,4,3)]
for i,j in ((0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)): L(V[i],V[j],color=MUTED,lw=1.0)
ar=dict(arrowstyle="-|>",color=INK,lw=1.4)
def arrow(p,q,c=INK): a=S(*p);b=S(*q); ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=c,lw=1.5))
arrow((0,0,3),(0,2.0,1.5),"#d9534f"); arrow((5,0,3),(2.5,2.0,1.5),"#1d6fb8")
ax.text(*S(-0.2,1.2,3.0),"200 kN",fontsize=7.8,ha="right",color="#d9534f"); ax.text(*S(3.9,1.4,1.3),"100 kN",fontsize=7.8,color="#1d6fb8")
arrow((0,4,0),(0,5.3,0)); ax.text(*S(0.2,5.3,0),"10 kN",fontsize=7.8)
arrow((5,0,3),(5,-1.3,3)); ax.text(*S(4.0,-1.1,3),"10 kN",fontsize=7.8)
arrow((2.2,4,0),(2.2,5.2,0),"#2e8b57"); arrow((4.2,5.2,0),(4.2,4,0),"#2e8b57"); ax.text(*S(2.4,5.3,0),"70 kN couple, 2 m",fontsize=7.4,color="#2e8b57")
arrow((1.0,0,0.8),(1.0,0,2.2),"#6a5acd"); arrow((4.0,0,2.2),(4.0,0,0.8),"#6a5acd"); ax.text(*S(1.2,-0.2,2.8),"80 kN couple, 3 m",fontsize=7.4,color="#6a5acd")
arrow((5,0.8,0.8),(5,0.8,2.2),"#b8860b"); arrow((5,3.3,2.2),(5,3.3,0.8),"#b8860b"); ax.text(*S(5.1,2.0,0.3),"200 kN couple, 2.5 m",fontsize=7.4,color="#b8860b")
ax.text(*S(-0.4,-0.3,0),"O",fontsize=9); ax.text(*S(-0.4,4.2,0),"P",fontsize=9)
ax.set_xlim(-3.4,9.5); ax.set_ylim(-2.4,6.4)
```

@q 3
A ladder of weight $W$ is placed against a wall as shown in the figure. Calculate the minimum angle of inclination of the ladder with ground so that the ladder doesn't slip under its own weight. Assume coefficient of friction for all surfaces as 0.3. [[4]]

@q 4
Draw AFD, SFD and BMD of the given loaded frame as shown in figure. Also, indicate salient points if any. [[10]]

```figure caption="Question 4: frame ABDF. Pin at A and pin at F, internal hinge (pin) at D. 12 kN at B (rightwards), 24 kN point load at C (3 m from B, downward), 6 kN/m UDL on CD (6 m), 15 kN at E (rightwards, 2.5 m below D). Column height 5.0 m, span BD = 9.0 m."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(5.6,2.9)); ax.set_aspect("equal"); ax.axis("off")
ax.plot([0,0,9,9],[0,5,5,0],color=INK,lw=2.4)
for x0 in (0,9): ax.add_patch(mp.Polygon([(x0,0),(x0-0.3,-0.5),(x0+0.3,-0.5)],closed=True,fc="white",ec=INK))
ar=dict(arrowstyle="-|>",color=INK,lw=1.4)
ax.annotate("",xy=(0,5),xytext=(-1.6,5),arrowprops=ar); ax.text(-2.5,5.2,"12 kN",fontsize=8)
ax.annotate("",xy=(3,5),xytext=(3,6.3),arrowprops=ar); ax.text(3.2,6.2,"24 kN",fontsize=8)
for x in _np.arange(3.3,9,0.6): ax.annotate("",xy=(x,5),xytext=(x,5.6),arrowprops=dict(arrowstyle="-|>",color=INK,lw=0.8))
ax.plot([3,9],[5.6,5.6],color=INK,lw=0.8); ax.text(6,5.8,"6 kN/m",ha="center",fontsize=8)
ax.annotate("",xy=(9,2.5),xytext=(7.4,2.5),arrowprops=ar); ax.text(6.0,2.7,"15 kN",fontsize=8)
ax.plot([9],[5],"o",mfc="white",mec=INK,ms=6); 
for p,l,o in (((0,0),"A",(-0.6,-0.1)),((0,5),"B",(-0.6,0.15)),((3,5),"C",(-0.1,-0.7)),((9,5),"D",(0.2,0.15)),((9,2.5),"E",(0.25,-0.2)),((9,0),"F",(0.25,-0.1))): ax.text(p[0]+o[0],p[1]+o[1],l,fontsize=9)
ax.text(9.4,5.5,"pin",fontsize=7.5)
ax.set_xlim(-3,10.5); ax.set_ylim(-1,7)
```

@q 5
For the given pin-jointed truss, determine forces in members BD, BE, CE, DE, DF and EF. [[5]]

```figure caption="Question 5: pin-jointed truss. A (pin) at (0, 0), C (4, 0), E (8, 0) on a roller; B (4, 2.5) above C, D (8, 5) above E, F (12, 5). Loads: 10 kN down at D, 10 kN down at F, 15 kN to the right at F."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,2.9)); ax.set_aspect("equal"); ax.axis("off")
N={"A":(0,0),"C":(4,0),"E":(8,0),"B":(4,2.5),"D":(8,5),"F":(12,5)}
for a,b in ("AB","BD","AC","CE","BC","BE","DE","DF","EF"): ax.plot([N[a][0],N[b][0]],[N[a][1],N[b][1]],color=INK,lw=1.8)
for k,(x,y) in N.items(): ax.plot([x],[y],"o",color=INK,ms=3.5); ax.text(x+(0.1 if k in "FD" else -0.3),y+(0.35 if k in "BDF" else -0.7),k,fontsize=9)
ax.add_patch(mp.Polygon([(0,0),(-0.4,-0.7),(0.4,-0.7)],closed=True,fc="white",ec=INK)); ax.add_patch(mp.Circle((8,-0.35),0.35,fc="white",ec=INK))
ar=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)
ax.annotate("",xy=(8,5),xytext=(8,6.6),arrowprops=ar); ax.text(8.2,6.2,"10 kN",fontsize=8)
ax.annotate("",xy=(12,5),xytext=(12,6.6),arrowprops=ar); ax.text(12.2,6.2,"10 kN",fontsize=8)
ax.annotate("",xy=(14.2,5),xytext=(12,5),arrowprops=ar); ax.text(12.3,4.2,"15 kN",fontsize=8)
ax.set_xlim(-1.5,15.5); ax.set_ylim(-1.5,7.4)
```

@q 6
Determine the moment of inertia about centroidal axes of the area bounded by the curves as shown. [[7]]

```figure caption="Question 6: area between the parabola 4y² = 9x and the line 4y = 3x (they meet at the origin and at (4, 3))."
import numpy as _np
fig,ax=plt.subplots(figsize=(3.4,2.8)); ax.set_aspect("equal")
x=_np.linspace(0,4,100); ax.fill_between(x,0.75*x,1.5*_np.sqrt(x),color="#cfdcec"); ax.plot(x,1.5*_np.sqrt(x),color=INK,lw=1.5); ax.plot(x,0.75*x,color=INK,lw=1.5)
ax.plot([1.6],[1.5],"o",color="#d9534f",ms=4); ax.text(1.7,1.2,"G",fontsize=8.5,color="#d9534f")
ax.text(0.6,2.6,"4y² = 9x",fontsize=8); ax.text(2.7,0.6,"4y = 3x",fontsize=8)
ax.set_xlim(-0.3,4.4); ax.set_ylim(-0.3,3.4); ax.tick_params(labelsize=7); ax.spines[["top","right"]].set_visible(False)
```

@q 7
a) The motion of a particle is defined by the position vector $\vec r=3t^2\hat i+4t^3\hat j+5t^4\hat k$ where $\vec r$ in metres and $t$ in sec. At the instant $t=3$ sec, find the tangential and normal components of acceleration. [[4]]

b) The rotation of the arm 1.5 m arm OA about O is defined by the relation $\theta=0.15t^2$, where $\theta$ is in radians and $t$ in seconds. Collar B slides along the arm in such a way that its distance from O is $r=1.5-0.12t^2$, where $r$ is in metres and $t$ in seconds. Calculate the magnitudes of the velocity and acceleration of the collar after the arm has rotated through 45°. [[4]]

@q 8
Two blocks shown in figure below are released from rest. The pulleys are frictionless and having no mass. Determine the acceleration of each block and tension in each cord. [[6]]

```figure caption="Question 8: block A (25.48 kg) on a 15° incline with μk = 0.25; the cord from A passes over the fixed pulley D and round the movable pulley C which carries block B (50.96 kg) and is anchored to the support at D."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(4.4,3.5)); ax.set_aspect("equal"); ax.axis("off")
th=_np.radians(15); ax.plot([-5,0],[5*_np.tan(th),0],color=INK,lw=2); ax.plot([0,0],[0,-5],color=INK,lw=2)
ax.add_patch(mp.Polygon([(-3.6,3.6*_np.tan(th)),(-1.6,1.6*_np.tan(th)),(-1.6-0.65*_np.sin(th),1.6*_np.tan(th)+0.65*_np.cos(th)),(-3.6-0.65*_np.sin(th),3.6*_np.tan(th)+0.65*_np.cos(th))],closed=True,fc="#dbe7f5",ec=INK,lw=1.2)); ax.text(-3.0,1.35,"A",fontsize=9)
ax.add_patch(mp.Circle((0.3,0.35),0.3,fc="white",ec=INK)); ax.text(0.55,0.75,"D",fontsize=9)
ax.plot([-1.7,0.3],[1.55*_np.tan(th)+0.32,0.65],color=INK,lw=1.2); ax.plot([0.6,0.6],[0.35,-2.0],color=INK,lw=1.2); ax.plot([0.0,0.0],[0.35,-2.0],color=INK,lw=1.2)
ax.add_patch(mp.Circle((0.3,-2.2),0.3,fc="white",ec=INK)); ax.text(0.7,-2.3,"C",fontsize=9)
ax.plot([0.3,0.3],[-2.5,-3.0],color=INK,lw=1.2); ax.add_patch(mp.Rectangle((-0.2,-4.0),1.0,1.0,fc="#c9d3df",ec=INK)); ax.text(0.3,-3.5,"B",fontsize=9,ha="center",va="center")
ax.text(-4.1,0.75,"15°",fontsize=8); ax.text(1.0,-3.9,"50.96 kg",fontsize=8); ax.text(-4.4,2.5,"25.48 kg",fontsize=8); ax.text(-3.5,0.1,"μk = 0.25",fontsize=8)
ax.set_xlim(-5,2.8); ax.set_ylim(-4.4,3.4)
```

@q 9
Length of crank AB is 100 mm and that of connecting rod is 250 mm as shown in figure. For the position shown in figure, determine the angular velocity of connecting rod and the velocity of the piston if the crank AB is rotating in clockwise direction at 1500 rpm. [[6]]

```figure caption="Question 9: slider-crank mechanism. Crank AB = 100 mm at 30° above the line of stroke, connecting rod BC = 250 mm, piston at C."
import numpy as _np
fig,ax=plt.subplots(figsize=(5.0,2.0)); ax.set_aspect("equal"); ax.axis("off")
B=(100*_np.cos(_np.radians(30)),50); phi=_np.arcsin(50/250); C=(B[0]+250*_np.cos(phi),0)
ax.plot([0,B[0]],[0,B[1]],color=INK,lw=3); ax.plot([B[0],C[0]],[B[1],0],color=INK,lw=2.2)
ax.plot([-30,C[0]+60],[0,0],color=MUTED,lw=0.8,ls="--"); ax.plot([0],[0],"o",color=INK,ms=6); ax.plot([B[0],C[0]],[B[1],0],"o",color=INK,ms=4)
ax.add_patch(plt.Rectangle((C[0],-18),50,36,fc="#c9d3df",ec=INK)); ax.text(C[0]+25,-35,"piston",ha="center",fontsize=8)
ax.text(-10,-18,"A",fontsize=9); ax.text(B[0]-5,B[1]+8,"B",fontsize=9); ax.text(C[0]-12,10,"C",fontsize=9); ax.text(40,6,"30°",fontsize=8)
ax.text(30,45,"100 mm",fontsize=8,rotation=30); ax.text(200,35,"250 mm",fontsize=8,rotation=-11)
ax.set_xlim(-40,C[0]+90); ax.set_ylim(-50,80)
```

<!-- SOLUTIONS -->

@s 1
**Free body diagram.** A *free body diagram* (FBD) is a sketch of a body (or part of a structure) separated from its surroundings, on which every external force acting on it is drawn: applied loads, its weight and the reactions of all supports and contacts that were removed. Equations of equilibrium are written for the forces on the FBD. *Example:* a ladder leaning on a wall: the FBD of the ladder shows its weight $W$ at the centre, the normal reaction and friction at the floor and the normal reaction (and friction) at the wall.

**Cylinder and string.** Let $r$ be the radius. The cylinder is acted on by three forces: the weight $W=500$ N (vertical through the centre O), the reaction $R$ of the *smooth* wall (horizontal, at the contact B, so its line of action passes through O) and the tension $T$ in the string. Three non-parallel forces in equilibrium are concurrent, so the string must pass through O. The string is attached at a point S on the surface, its length $AS=2r$, and the line continues for a further $SO=r$, so $AO=3r$. The centre is at the horizontal distance $r$ from the wall, so the string makes the angle $\alpha$ with the vertical wall:

$$\sin\alpha=\frac{r}{3r}=\frac13\ \Rightarrow\ \alpha=19.47^\circ,\quad\cos\alpha=0.9428$$

$$\begin{gathered}\sum F_y=0:\ T\cos\alpha=W\ \Rightarrow\ T=\frac{500}{0.9428}=\boxed{530.3\ \text{N}}\\ \sum F_x=0:\ R=T\sin\alpha=\boxed{176.8\ \text{N}}\end{gathered}$$

@s 2
Reading of the figure (box 5 m along $x$, 4 m along $y$, 3 m along $z$, origin O at the rear bottom left corner, P = (0, 4, 0) the top rear left corner): the 200 kN force acts at the front-bottom-left corner $(0,0,3)$ and the 100 kN force at the front-bottom-right corner $(5,0,3)$, both directed towards P; 10 kN acts upward at P and 10 kN downward at $(5,0,3)$; the three pairs of equal and opposite forces are couples (the force-pair 70 kN, vertical, 2 m apart in $x$; 80 kN along $z$, 3 m apart in $x$; 200 kN along $z$, 2.5 m apart in $y$).

*Forces.* Unit vectors towards P: from $(0,0,3)$: $\dfrac{(0,4,-3)}{5}$; from $(5,0,3)$: $\dfrac{(-5,4,-3)}{\sqrt{50}}$.

| Force | Point (m) | Vector (kN) | Moment about O, $\vec r\times\vec F$ (kN·m) |
|---|---|---|---|
| 200 kN | (0, 0, 3) | (0, 160, −120) | (−480, 0, 0) |
| 100 kN | (5, 0, 3) | (−70.71, 56.57, −42.43) | (−169.7, 0, 282.8) |
| 10 kN up | (0, 4, 0) | (0, 10, 0) | (0, 0, 0) |
| 10 kN down | (5, 0, 3) | (0, −10, 0) | (30, 0, −50) |
| **Sum** | | $\vec R=(-70.71,\ 216.57,\ -162.43)$ | $(-619.7,\ 0,\ 232.8)$ |

*Couples (free vectors).* 70 kN pair: forces up at the left and down at the right, $2\times70=140$ kN·m clockwise seen from $+z$, $\vec M_1=(0,0,-140)$. 80 kN pair along $z$ with arm 3 m along $x$: $\vec M_2=(0,+240,0)$. 200 kN pair along $z$ with arm 2.5 m along $y$: $\vec M_3=(+500,0,0)$.

$$\vec M_O=(-619.7+500,\ 0+240,\ 232.8-140)=(-119.7,\ 240.0,\ 92.8)\ \text{kN·m}$$

$$\boxed{\vec R=-70.71\hat i+216.57\hat j-162.43\hat k\ \text{kN},\ |R|=279.8\ \text{kN};\qquad \vec M_O=-119.7\hat i+240.0\hat j+92.8\hat k\ \text{kN·m}\ (|M_O|=282.9)}$$

The direction cosines of $\vec R$ are $(-0.2527,\ 0.7740,\ -0.5805)$, i.e. angles $104.6^\circ,\ 39.3^\circ,\ 125.5^\circ$ with $x,y,z$.

**Equivalent wrench.** A wrench is a force along an axis together with a couple parallel to it. The component of $\vec M_O$ along $\vec R$:

$$M_\parallel=\frac{\vec R\cdot\vec M_O}{|R|}=\frac{(-70.71)(-119.7)+(216.57)(240.0)+(-162.43)(92.8)}{279.8}=\frac{45\,361}{279.8}=\boxed{162.1\ \text{kN·m}}$$

(the pitch is $M_\parallel/R=0.579$ m, positive: the couple has the same sense as the force). The wrench axis passes through the point nearest to O,

$$\vec r_0=\frac{\vec R\times\vec M_O}{R^2}=\boxed{(0.755,\ 0.332,\ 0.114)\ \text{m}}$$

so the **line of action** of the wrench is $\vec r=(0.755,0.332,0.114)+\lambda(-0.2527,\ 0.7740,\ -0.5805)$ m, i.e. $\dfrac{x-0.755}{-0.2527}=\dfrac{y-0.332}{0.7740}=\dfrac{z-0.114}{-0.5805}$. Check: $\vec r_0\times\vec R+M_\parallel\hat R=\vec M_O$ ✓ (verified numerically).

@s 3
**Ladder with friction on both surfaces ($\mu=0.3$).** Let the ladder AB (length $L$, weight $W$ at the midpoint) rest with A on the ground and B on the wall, at the angle $\theta$ with the ground. At the point of slipping, the foot A tends to slide away from the wall and B slides down; both friction forces are limiting: $F_A=\mu N_A$ (towards the wall) and $F_B=\mu N_B$ (upward).

$$\begin{gathered}\sum F_x=0:\ F_A=N_B\ \Rightarrow\ \mu N_A=N_B\\ \sum F_y=0:\ N_A+F_B=W\ \Rightarrow\ N_A+\mu N_B=W\end{gathered}$$

$$\begin{gathered}N_A=\frac{W}{1+\mu^2}=\frac{W}{1.09}=0.917\,W \\ N_B=\mu N_A=0.275\,W \\ F_B=0.0826\,W\end{gathered}$$

Moments about A:

$$W\frac L2\cos\theta=N_BL\sin\theta+F_BL\cos\theta\ \Rightarrow\ \tan\theta=\frac{W}{2N_B}-\mu=\frac{1}{2(0.2752)}-0.3=1.8167-0.3=1.5167$$

(general result $\tan\theta=\dfrac{1-\mu^2}{2\mu}=\dfrac{0.91}{0.6}$)

$$\boxed{\theta_{min}=56.6^\circ}$$

For any angle larger than this the ladder is in equilibrium.

@s 4
**Frame ABDF.** Coordinates: A (0, 0), B (0, 5), C (3, 5), D (9, 5), E (9, 2.5), F (9, 0) m. UDL resultant $6\times6=36$ kN at $x=6$ m. Pins at A and F; the internal hinge D transmits no moment. Loads: 12 kN → at B, 24 kN ↓ at C, 36 kN ↓, 15 kN → at E.

*Reactions.* The hinge condition $M_D=0$ for the right part DF (moments about D; $F_y$ passes through D):

$$5F_x+15(2.5)=0\ \Rightarrow\ F_x=-7.5\ \text{kN (the reaction at F acts to the left)}$$

Whole frame:

$$\begin{gathered}\sum F_x=0:\ A_x-7.5+12+15=0\ \Rightarrow\ A_x=-19.5\ \text{kN (to the left)}\\ \sum M_A=0:\ 9F_y-12(5)-24(3)-36(6)-15(2.5)=0\ \Rightarrow\ F_y=\frac{385.5}{9}=42.83\ \text{kN}\uparrow\\ \sum F_y=0:\ A_y=24+36-42.83=17.17\ \text{kN}\uparrow\end{gathered}$$

Check: moment about D of the left part is $0$ ✓.

*Member forces* (axial: compression negative; shear positive when it rotates the segment clockwise; bending moment: sagging positive on the beam, tension on the inside for the columns).

| Member | Axial force (kN) | Shear (kN) | Bending moment (kN·m) |
|---|---|---|---|
| Column AB | −17.17 (compression), constant | 19.5, constant | 0 at A, rising linearly to 97.5 at B (tension outside, on the left face) |
| Beam BC | −7.5 (compression) | +17.17 | 97.5 at B to 149.0 at C |
| Beam CD | −7.5 | −6.83 at C, falling to −42.83 at D | 149.0 at C, decreasing (maximum at C since $V$ changes sign there) to 0 at D (hinge) |
| Column DE | −42.83 | −7.5 (D to E, constant) | 0 at D, 18.75 at E |
| Column EF | −42.83 | +7.5 (E to F, constant) | 18.75 at E to 0 at F |

*Beam BD in detail.* With $x$ measured from B:

$$\begin{gathered}V(x)=17.17\ (0<x<3) \\ V(x)=17.17-24-6(x-3)=-6.83-6(x-3)\ (3<x<9)\end{gathered}$$

$$\begin{gathered}M(x)=97.5+17.17x\ (0<x\le3) \\ M(x)=97.5+17.17x-24(x-3)-3(x-3)^2\ (3\le x\le9)\end{gathered}$$

$M(0)=97.5$, $M(3)=149.0$ (maximum; the shear is positive before C and negative after it, so $V=0$ only at C), $M(6)=149.0+17.17(3)-\dots=$ falling steadily, e.g. $M(6)=97.5+103.0-72-27=101.5$, and $M(9)=0$ ✓ (hinge).

The **salient points** are: the maximum sagging moment 149.0 kN·m at C, where the shear changes from +17.17 to −6.83 kN; the moment at the rigid joint B, 97.5 kN·m (the outer face of the joint is in tension); the zero moment at the hinge D and at both pins A and F; the maximum shear 42.83 kN at D (the end of the UDL); and the maximum compression 42.83 kN in the right column.

```figure caption="Question 4 solution: shear force and bending moment diagrams for the beam BD (x measured from B) and the end values of the frame."
import numpy as _np
fig,(a1,a2)=plt.subplots(1,2,figsize=(5.8,2.4))
x=_np.linspace(0,9,400); V=_np.where(x<3,17.17,-6.83-6*(x-3)); M=_np.where(x<3,97.5+17.17*x,97.5+17.17*x-24*(x-3)-3*(x-3)**2)
a1.plot(x,V,color=ACCENT,lw=1.8); a1.fill_between(x,0,V,color="#dbe7f5"); a1.axhline(0,color=INK,lw=0.8); a1.set_title("SFD, beam BD (kN)",fontsize=8)
for xp,yp in ((0,17.17),(3,-6.83),(9,-42.83)): a1.annotate(f"{yp:+.2f}",(xp,yp),fontsize=7,xytext=(3,3),textcoords="offset points")
a2.plot(x,M,color="#d9534f",lw=1.8); a2.fill_between(x,0,M,color="#f3d6d4"); a2.axhline(0,color=INK,lw=0.8); a2.set_title("BMD, beam BD (kN·m)",fontsize=8)
for xp,yp in ((0,97.5),(3,149.0),(9,0)): a2.annotate(f"{yp:.1f}",(xp,yp),fontsize=7,xytext=(3,3),textcoords="offset points")
for a in (a1,a2): a.tick_params(labelsize=7); a.set_xlabel("x from B (m)",fontsize=7.5)
a1.set_ylim(-50,25); a2.set_ylim(-10,170)
```

@s 5
**Truss.** Take A (0, 0), C (4, 0), E (8, 0), B (4, 2.5), D (8, 5), F (12, 5) m. Member directions: BD and AB have slope $2.5/4$ (length 4.717 m), BE: $(4,-2.5)$, EF: $(4,5)$ (length 6.403 m). *Reactions* (A pin, E roller):

$$\sum M_A=0:\ 8E_y-10(8)-10(12)-15(5)=0\ \Rightarrow\ E_y=34.375\ \text{kN}\uparrow;\quad A_x=-15\ \text{kN},\ A_y=-14.375\ \text{kN}$$

*Joint F* (loads 15 kN →, 10 kN ↓; members DF to the left, EF down-left, $\sin=0.7809,\ \cos=0.6247$; tension positive):

$$\begin{gathered}\sum F_y:\ -10-0.7809\,F_{EF}=0\ \Rightarrow\ F_{EF}=-12.81\ \text{kN}\\ \sum F_x:\ 15-F_{DF}-0.6247F_{EF}=0\ \Rightarrow\ F_{DF}=15+8.0=23.0\ \text{kN}\end{gathered}$$

*Joint D* (10 kN ↓; DF to the right, BD down-left with $\cos=0.848$, $\sin=0.530$, DE down):

$$\begin{gathered}\sum F_x:\ 23.0-0.848F_{BD}=0\ \Rightarrow\ F_{BD}=27.12\ \text{kN}\\ \sum F_y:\ -10-0.530(27.12)-F_{DE}=0\ \Rightarrow\ F_{DE}=-24.38\ \text{kN}\end{gathered}$$

*Joint C* has no load and only the collinear members AC and CE and the vertical BC, so $F_{BC}=0$.

*Joint E* ($E_y=34.375$ kN upward; members CE to the left, DE up, BE up-left, EF up-right):

$$\begin{gathered}\sum F_y:\ 34.375-24.38+0.530F_{BE}+0.7809(-12.81)=0\ \Rightarrow\ F_{BE}=0\\ \sum F_x:\ -F_{CE}-0.848F_{BE}+0.6247(-12.81)=0\ \Rightarrow\ F_{CE}=-8.0\ \text{kN}\end{gathered}$$

| Member | Force (kN) | Nature |
|---|---|---|
| BD | 27.12 | tension |
| BE | 0 | zero-force member |
| CE | 8.00 | compression |
| DE | 24.38 | compression |
| DF | 23.00 | tension |
| EF | 12.81 | compression |

@s 6
**Area between $4y^2=9x$ and $4y=3x$.** Parabola $y_1=1.5\sqrt x$, line $y_2=0.75x$; they meet where $1.5\sqrt x=0.75x\Rightarrow x=4$ (point (4, 3)). The parabola is the upper curve in $0\le x\le4$.

$$A=\int_0^4(1.5\sqrt x-0.75x)\,dx=\Big[x^{3/2}-0.375x^2\Big]_0^4=8-6=2$$

*Centroid.*

$$\begin{gathered}\bar x=\frac1A\int_0^4x(y_1-y_2)\,dx=\frac12\Big[0.6x^{5/2}-0.25x^3\Big]_0^4=\frac{19.2-16}{2}=1.6 \\ \bar y=\frac{1}{2A}\int_0^4(y_1^2-y_2^2)dx=\frac14\Big[1.125x^2-0.1875x^3\Big]_0^4=\frac{18-12}{4}=1.5\end{gathered}$$

*Moments of inertia about the coordinate axes.*

$$I_x=\frac13\int_0^4(y_1^3-y_2^3)\,dx=\frac13\Big[3.375\tfrac25x^{5/2}-\tfrac{0.421875}{4}x^4\Big]_0^4=\frac13(43.2-27)=5.4$$

$$I_y=\int_0^4x^2(y_1-y_2)\,dx=\Big[1.5\tfrac27x^{7/2}-0.1875x^4\Big]_0^4=54.857-48=6.857$$

*Parallel-axis transfer to the centroid:*

$$\begin{gathered}\boxed{I_{\bar x}=I_x-A\bar y^2=5.4-2(1.5)^2=0.90\ \text{(units)}^4} \\ \boxed{I_{\bar y}=I_y-A\bar x^2=6.857-2(1.6)^2=1.737\ \text{(units)}^4}\end{gathered}$$

(The figure carries no units; with the lengths in metres the answers are in m⁴. Polar moment about the centroid $=2.64$.)

@s 7
**(a)** $\vec r=3t^2\hat i+4t^3\hat j+5t^4\hat k$:

$$\begin{gathered}\vec v=6t\hat i+12t^2\hat j+20t^3\hat k \\ \vec a=6\hat i+24t\hat j+60t^2\hat k\end{gathered}$$

At $t=3$ s: $\vec v=18\hat i+108\hat j+540\hat k$ ($v=550.99$ m/s) and $\vec a=6\hat i+72\hat j+540\hat k$ ($a=544.81$ m/s²).

$$\boxed{a_t=\frac{\vec a\cdot\vec v}{v}=\frac{6(18)+72(108)+540(540)}{550.99}=\frac{299\,484}{550.99}=543.5\ \text{m/s}^2}$$

$$\boxed{a_n=\sqrt{a^2-a_t^2}=\sqrt{544.81^2-543.54^2}=37.2\ \text{m/s}^2}$$

**(b) Collar B on the rotating arm** (polar coordinates $r,\theta$). $\theta=0.15t^2$, $\dot\theta=0.3t$, $\ddot\theta=0.3$ rad/s²; $r=1.5-0.12t^2$, $\dot r=-0.24t$, $\ddot r=-0.24$ m/s².

*Time for $45^\circ$:* $\theta=45^\circ=0.7854$ rad $\Rightarrow t^2=\dfrac{0.7854}{0.15}=5.236$, $t=2.288$ s. Then

$$\begin{gathered}\dot\theta=0.3(2.288)=0.6865\ \text{rad/s},\quad r=1.5-0.12(5.236)=0.8717\ \text{m},\quad\dot r=-0.5492\ \text{m/s}\end{gathered}$$

$$v_r=\dot r=-0.5492,\quad v_\theta=r\dot\theta=0.8717(0.6865)=0.5984\ \Rightarrow\ \boxed{v=\sqrt{0.5492^2+0.5984^2}=0.812\ \text{m/s}}$$

$$\begin{gathered}a_r=\ddot r-r\dot\theta^2=-0.24-0.8717(0.4713)=-0.6508 \\ a_\theta=r\ddot\theta+2\dot r\dot\theta=0.8717(0.3)+2(-0.5492)(0.6865)=-0.4925\end{gathered}$$

$$\boxed{a=\sqrt{0.6508^2+0.4925^2}=0.816\ \text{m/s}^2}$$

@s 8
**Blocks and pulleys.** The cord runs from block A over the fixed pulley D and round the movable pulley C (carrying B), with its other end fixed at D's support. If A moves a distance $x_A$ down the incline and B moves down $y_B$, the cord length gives $x_A=2y_B$, so $a_A=2a_B$. The massless pulley C is in equilibrium: the tension in each of its two cord segments is $T$ and the pull on B through it is $2T$. Block A moves down the 15° slope pulled by the cord, with kinetic friction opposing.

$$\begin{gathered}\text{Block B}:\ m_Bg-2T=m_Ba_B\\ \text{Block A}:\ T+m_Ag\sin15^\circ-\mu_km_Ag\cos15^\circ=m_Aa_A=2m_Aa_B\end{gathered}$$

With $m_A=25.48$ kg, $m_B=50.96$ kg, $\mu_k=0.25$, $g=9.81$ m/s²: $m_Ag=249.96$ N, $m_Bg=499.92$ N, $\sin15^\circ-0.25\cos15^\circ=0.2588-0.2415=0.0173$.

$$\begin{gathered}T=249.96-25.48\,a_B\quad\text{(from B)} \\ T+4.32=50.96\,a_B\quad\text{(from A)}\end{gathered}$$

$$249.96-25.48a_B+4.32=50.96a_B\ \Rightarrow\ a_B=\frac{254.28}{76.44}$$

$$\boxed{a_B=3.327\ \text{m/s}^2\ \text{downward},\qquad a_A=2a_B=6.653\ \text{m/s}^2\ \text{down the incline}}$$

$$\boxed{T=249.96-25.48(3.327)=165.2\ \text{N in each cord segment (the tension in the cord is 165.2 N; the force through pulley C on B is }2T=330.4\ \text{N)}}$$

@s 9
**Slider-crank mechanism.** $\omega_{AB}=\dfrac{2\pi(1500)}{60}=157.08$ rad/s clockwise; $v_B=\omega_{AB}\,(AB)=157.08(0.1)=15.71$ m/s, perpendicular to AB.

*Geometry.* B is at $(0.1\cos30^\circ,\ 0.1\sin30^\circ)=(0.0866,\ 0.05)$ m. For the rod BC ($L=0.25$ m, C on the line of stroke): $\sin\varphi=\dfrac{0.05}{0.25}=0.2\Rightarrow\varphi=11.54^\circ$ below the horizontal; $r_{C/B}=(0.2449,\ -0.05)$ m.

*Velocity of B* (clockwise rotation): $\vec v_B=\omega\hat k\times\vec r_{B/A}$ with $\omega=-157.08$ rad/s: $\vec v_B=(7.854,\ -13.60)$ m/s (right and down, 15.71 m/s at $60^\circ$ below the horizontal).

*Velocity of C.* C moves horizontally ($v_C$ along the line of stroke): $\vec v_C=\vec v_B+\vec\omega_{BC}\times\vec r_{C/B}$ with $\vec\omega_{BC}=\omega_{BC}\hat k$:

$$\begin{gathered}y:\ 0=-13.60+\omega_{BC}(0.2449)\ \Rightarrow\ \omega_{BC}=55.54\ \text{rad/s}\\ x:\ v_C=7.854-\omega_{BC}(-0.05)=7.854+2.777=10.63\ \text{m/s}\end{gathered}$$

(Instantaneous-centre check: $v_C=\omega_{BC}\,(I_C)$ with the vertical distance from the instantaneous centre to C, $0.1914$ m: $55.54(0.1914)=10.63$ m/s ✓.)

$$\begin{gathered}\boxed{\omega_{BC}=55.5\ \text{rad/s, counter-clockwise}} \\ \boxed{v_{piston}=10.63\ \text{m/s (towards the right, away from the crank)}}\end{gathered}$$

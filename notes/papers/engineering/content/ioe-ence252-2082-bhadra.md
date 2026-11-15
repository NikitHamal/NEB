---
file: NEBians-IOE-Past-Paper-Theory-of-Structures-II-ENCE252-2082-Bhadra.pdf
subject: Theory of Structures II
level: BE · Year II / Part II
code: ENCE 252
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course), BE Civil, Year II / Part II. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Describe method of flexibilities and stiffness. [[4]]

b) A spring with stiffness $k$ supports a simply supported beam shown in the figure below. Find the reaction at elastic support using Castigliano's theorem. [[6]]

```figure caption="Question 1(b): simply supported beam AB of span 2L (EI constant) carrying a UDL of P/2L over the whole span, resting at mid-span C on a spring of stiffness k."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,2.3)); ax.axis("off")
ax.plot([0,10],[0,0],color=INK,lw=3)
for x in np.linspace(0.3,9.7,15): ax.annotate("",xy=(x,0.05),xytext=(x,0.8),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
ax.text(5,1.0,"P / 2L  (per unit length)",ha="center",fontsize=9)
ax.plot([0,-0.3,0.3,0],[0,-0.55,-0.55,0],color=INK,lw=1.8); ax.add_patch(mp.Circle((10,-0.3),0.28,fc="white",ec=INK,lw=1.6)); ax.plot([9.5,10.5],[-0.62,-0.62],color=INK,lw=1.6)
yy=np.linspace(0,-1.4,11); xx=5+np.array([0,0.0]+[(0.25 if i%2 else -0.25) for i in range(7)]+[0,0.0]); ax.plot(xx,yy,color=INK,lw=1.4); ax.plot([4.6,5.4],[-1.4,-1.4],color=INK,lw=2)
ax.text(5.4,-0.8,"k",fontsize=10); ax.text(5,0.35,"C",ha="center",fontsize=9,fontweight="bold"); ax.text(0,-0.9,"A",ha="center",fontsize=9,fontweight="bold"); ax.text(10,-0.95,"B",ha="center",fontsize=9,fontweight="bold")
ax.text(2.5,-1.9,"L   (EI)",ha="center",fontsize=9); ax.text(7.5,-1.9,"L   (EI)",ha="center",fontsize=9)
ax.set_xlim(-1,11); ax.set_ylim(-2.3,1.5)
```

@q 2
For the truss shown in figure below, calculate the member forces using force method. Take $EA$ constant for all. [[10]]

```figure caption="Question 2: rectangular truss 4 m wide and 3 m high; joints A (bottom left) and B (bottom right) are pinned supports, C (top left) and D (top right) are free; both diagonals AD and BC; 35 kN horizontal load at C."
fig,ax=plt.subplots(figsize=(4.2,3.4)); ax.axis("off")
P={"A":(0,0),"B":(4,0),"C":(0,3),"D":(4,3)}
for a,b in ["AB","CD","AC","BD","AD","BC"]: ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=2)
for k,(x,y) in P.items(): ax.text(x+(-0.35 if x==0 else 0.35),y+(-0.5 if y==0 else 0.15),k,fontsize=10,fontweight="bold",ha="center")
ax.annotate("",xy=(-0.03,3),xytext=(-1.5,3),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(-2.1,3.25,"35 kN",fontsize=9)
for x in (0,4): ax.plot([x,x-0.3,x+0.3,x],[0,-0.5,-0.5,0],color=INK,lw=1.6)
ax.text(2,-1.0,"4 m",ha="center",fontsize=8.5); ax.text(4.35,1.5,"3 m",fontsize=8.5,va="center")
ax.set_xlim(-2.4,5.2); ax.set_ylim(-1.4,4.0)
```

@q 3
Calculate the horizontal thrust of the given two hinged parabolic arch. [[6]]

```figure caption="Question 3: two-hinged parabolic arch, span 100 m (50 m + 30 m + 20 m), rise 10 m at the crown; 10 kN/m UDL over the left half A to C (50 m), 100 kN at D, 20 m from the right support B."
fig,ax=plt.subplots(figsize=(5.8,2.6)); ax.axis("off")
x=np.linspace(0,100,300); y=4*10*x*(100-x)/10000
ax.plot(x,y,color=INK,lw=2.6)
for xx in np.linspace(2,48,11):
    yy=4*10*xx*(100-xx)/10000; ax.annotate("",xy=(xx,yy+0.1),xytext=(xx,yy+2.2),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
ax.text(25,13.2,"10 kN/m",ha="center",fontsize=9)
yd=4*10*80*20/10000; ax.annotate("",xy=(80,yd+0.1),xytext=(80,yd+4.5),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(80,yd+5.0,"100 kN",ha="center",fontsize=9)
for xs in (0,100): ax.plot([xs,xs-2,xs+2,xs],[0,-2,-2,0],color=INK,lw=1.6)
ax.text(50,10.6,"C",ha="center",fontsize=9,fontweight="bold"); ax.text(82,yd-1.3,"D",fontsize=9,fontweight="bold"); ax.text(-3,0.5,"A",fontsize=9,fontweight="bold"); ax.text(102,0.5,"B",fontsize=9,fontweight="bold")
ax.text(25,-4.5,"50 m",ha="center",fontsize=8.5); ax.text(65,-4.5,"30 m",ha="center",fontsize=8.5); ax.text(90,-4.5,"20 m",ha="center",fontsize=8.5); ax.text(104,5,"10 m",fontsize=8.5)
ax.set_xlim(-6,112); ax.set_ylim(-6,17)
```

@q 4
Analyze the beam shown in figure below using slope deflection method. [[5]]

```figure caption="Question 4: beam fixed at A, rollers at B (5 m from A) and C (6 m beyond B), overhang CD = 2 m. 10 kN/m UDL over AB (EI); 200 kN at mid-span of BC (2EI); 20 kN at the free end D."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.0,2.2)); ax.axis("off")
ax.plot([0,16],[0,0],color=INK,lw=3)
for xx in np.linspace(0.3,4.7,12): ax.annotate("",xy=(xx,0.05),xytext=(xx,0.8),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
ax.text(2.5,1.0,"10 kN/m",ha="center",fontsize=8.5); ax.text(2.5,-1.6,"5 m  (EI)",ha="center",fontsize=8.5)
ax.annotate("",xy=(8,0.05),xytext=(8,1.3),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(8,1.5,"200 kN",ha="center",fontsize=8.5)
ax.annotate("",xy=(16,0.05),xytext=(16,1.3),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(16,1.5,"20 kN",ha="center",fontsize=8.5)
for x in (5,11): ax.add_patch(mp.Circle((x,-0.3),0.3,fc="white",ec=INK,lw=1.5)); ax.plot([x-0.6,x+0.6],[-0.66,-0.66],color=INK,lw=1.5)
ax.add_patch(mp.Rectangle((-0.5,-0.9),0.5,1.8,fc="#999",ec=INK,hatch="///"))
for x,t in ((0,"A"),(5,"B"),(11,"C"),(16,"D")): ax.text(x,-1.15,t,ha="center",fontsize=9,fontweight="bold")
ax.text(8,-1.6,"3 m + 3 m  (2EI)",ha="center",fontsize=8.5); ax.text(14,-1.6,"2 m",ha="center",fontsize=8.5)
ax.set_xlim(-1,17); ax.set_ylim(-2.0,2.0)
```

@q 5
Analyze the frame by using moment distribution method. [[5]]

```figure caption="Question 5: frame with beam A-B-C (A fixed; 2EI), 50 kN at 2 m from A; AB = 5 m; BC = 4 m (2EI) carrying 10 kN/m; column BE (EI, 6 m) fixed at E with a 200 kN horizontal load at its mid-height; column CD (EI, 6 m) hinged at D."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.2,3.6)); ax.axis("off")
ax.plot([0,9],[0,0],color=INK,lw=3); ax.plot([5,5],[0,-6],color=INK,lw=2.4); ax.plot([9,9],[0,-6],color=INK,lw=2.4)
ax.add_patch(mp.Rectangle((-0.5,-0.8),0.5,1.6,fc="#999",ec=INK,hatch="///")); ax.add_patch(mp.Rectangle((4.4,-6.5),1.2,0.5,fc="#999",ec=INK,hatch="///")); ax.plot([9,8.7,9.3,9],[-6,-6.6,-6.6,-6],color=INK,lw=1.6)
ax.annotate("",xy=(2,0.05),xytext=(2,1.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(2,1.25,"50 kN",ha="center",fontsize=8.5)
for xx in np.linspace(5.2,8.8,9): ax.annotate("",xy=(xx,0.05),xytext=(xx,0.8),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
ax.text(7,1.0,"10 kN/m",ha="center",fontsize=8.5)
ax.annotate("",xy=(4.95,-3),xytext=(3.2,-3),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(2.0,-3.15,"200 kN",fontsize=8.5)
for x,y,t in ((-0.9,0.3,"A"),(4.6,0.3,"B"),(9.2,0.3,"C"),(5.1,-6.9,"E"),(9.2,-6.5,"D")): ax.text(x,y,t,fontsize=9,fontweight="bold")
ax.text(1,-0.9,"2 m",ha="center",fontsize=8); ax.text(3.5,-0.9,"3 m",ha="center",fontsize=8); ax.text(7,-0.9,"4 m",ha="center",fontsize=8); ax.text(5.2,-1.6,"EI",fontsize=8.5); ax.text(9.2,-1.6,"EI",fontsize=8.5); ax.text(2,0.35-1.3,"2EI",fontsize=8.5,ha="center"); ax.text(7,-1.5,"2EI",fontsize=8.5,ha="center")
ax.set_xlim(-1.4,10.5); ax.set_ylim(-7.4,2.0)
```

@q 6
Determine member stiffness matrices for each member and find the reactions in all supports of truss as shown in figure below using direct stiffness method. [[4+8]]

```figure caption="Question 6: plane truss, 40 cm x 30 cm; node 1 (top left) rests on a roller below the ceiling and carries a 20 kN load to the left; node 2 (bottom left) carries a 25 kN upward load; nodes 3 and 4 are pinned to the wall on the right. Members 1-3 (40 cm), 1-2 (30 cm), 2-3 (50 cm) and 2-4 (40 cm)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.5)); ax.axis("off")
P={"1":(0,30),"2":(0,0),"3":(40,30),"4":(40,0)}
for a,b in ["13","12","23","24"]: ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=2.2)
for k,(x,y) in P.items(): ax.plot(x,y,"o",color=INK,ms=4); ax.text(x+(-4 if x==0 else 3),y+(3 if y else -6),k,fontsize=10,fontweight="bold")
ax.add_patch(mp.Circle((0,33),2.5,fc="white",ec=INK,lw=1.5)); ax.plot([-6,6],[35.8,35.8],color=INK,lw=1.6)
ax.annotate("",xy=(-1,30),xytext=(-18,30),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(-28,32,"20 kN",fontsize=9)
ax.annotate("",xy=(0,-1),xytext=(0,-16),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(3,-14,"25 kN",fontsize=9)
for y in (30,0): ax.plot([40,40],[y-5,y+5],color=INK,lw=3)
ax.text(20,32,"40 cm",ha="center",fontsize=8.5); ax.text(-5,15,"30 cm",rotation=90,va="center",fontsize=8.5); ax.text(22,13,"50 cm",fontsize=8.5,rotation=36)
ax.set_xlim(-34,50); ax.set_ylim(-20,42)
```

@q 7
Determine the plastic moment capacity for the frame shown in figure below. Take load factor 1.5. [[6]]

```figure caption="Question 7: frame with hinged supports at A (foot of the 4 m column AB) and D (2 m below C); beam BC = 4 m; 20 kN/m horizontal UDL on the whole of AB."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.3)); ax.axis("off")
ax.plot([0,0],[0,4],color=INK,lw=2.8); ax.plot([0,4],[4,4],color=INK,lw=2.8); ax.plot([4,4],[2,4],color=INK,lw=2.8)
for yy in np.linspace(0.2,3.8,10): ax.annotate("",xy=(0.02,yy),xytext=(-0.9,yy),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
ax.text(-1.0,2,"20 kN/m",rotation=90,va="center",ha="right",fontsize=9)
for p in ((0,0),(4,2)): ax.plot([p[0],p[0]-0.3,p[0]+0.3,p[0]],[p[1],p[1]-0.55,p[1]-0.55,p[1]],color=INK,lw=1.6)
for x,y,t in ((-0.4,-0.1,"A"),(-0.4,4.2,"B"),(4.15,4.2,"C"),(4.2,1.8,"D")): ax.text(x,y,t,fontsize=9,fontweight="bold")
ax.text(2,4.3,"4 m",ha="center",fontsize=8.5); ax.text(0.2,2,"4 m",fontsize=8.5); ax.text(4.2,3,"2 m",fontsize=8.5)
ax.set_xlim(-2.2,5.4); ax.set_ylim(-1.0,5.0)
```

@q 8
Draw ILD for reaction at fixed support of a propped cantilever beam of span 6 m. Take 1 m ordinate interval. [[6]]

```figure caption="Question 8: propped cantilever, span 6 m, fixed at A and propped by a roller at B."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.8,1.6)); ax.axis("off")
ax.plot([0,6],[0,0],color=INK,lw=3); ax.add_patch(mp.Rectangle((-0.35,-0.6),0.35,1.2,fc="#999",ec=INK,hatch="///")); ax.add_patch(mp.Circle((6,-0.22),0.22,fc="white",ec=INK,lw=1.6)); ax.plot([5.6,6.4],[-0.47,-0.47],color=INK,lw=1.6)
ax.text(0,0.55,"A",ha="center",fontsize=9,fontweight="bold"); ax.text(6,0.4,"B",ha="center",fontsize=9,fontweight="bold"); ax.text(3,-0.95,"6 m",ha="center",fontsize=9)
ax.set_xlim(-1,7); ax.set_ylim(-1.3,1.0)
```

<!-- SOLUTIONS -->

@s 1
**(a) Method of flexibilities (force method) and method of stiffness (displacement method).**

*Method of flexibilities.* The unknowns are **redundant forces**. The indeterminate structure is made statically determinate (primary structure) by removing $D_s$ redundants $X_1\ldots X_n$. The displacements of the primary structure at the released points, caused by the loads ($\Delta_{i0}$) and by unit redundants ($f_{ij}$, the *flexibility coefficients*), must satisfy the compatibility of the original structure:

$$\{\Delta\}=\{\Delta_0\}+[F]\{X\}\ \Rightarrow\ \{X\}=-[F]^{-1}\{\Delta_0\}\ \text{(when the released displacements are zero)}$$

Here $f_{ij}=\sum\int\dfrac{m_im_j}{EI}ds$ (or $\sum\dfrac{f_if_jL}{EA}$ for trusses). The final forces are $F=F_0+\sum X_if_i$. It is convenient for structures with a low degree of static indeterminacy, and also handles support settlement, temperature and lack of fit.

*Method of stiffness.* The unknowns are the **joint displacements** (rotations and translations). The structure is restrained at the $D_k$ possible joint displacements; the *stiffness coefficients* $k_{ij}$ (the force needed at $i$ for a unit displacement at $j$ with all others locked) are assembled and the equilibrium of the joints is solved:

$$[K]\{\Delta\}=\{P\}-\{P_F\}\ \Rightarrow\ \{\Delta\}=[K]^{-1}\{P-P_F\}$$

where $P_F$ are the fixed-end actions. The member end forces follow from the member stiffness relations. It suits computer programming (direct stiffness method) and structures with a low degree of kinematic indeterminacy; slope-deflection and moment distribution are hand versions of it.

| | Flexibility (force) method | Stiffness (displacement) method |
|---|---|---|
| Unknowns | redundant forces, $D_s$ | joint displacements, $D_k$ |
| Condition used | compatibility | equilibrium |
| Matrix | flexibility $[F]$ | stiffness $[K]$ |
| Best for | few redundants | many redundants, computer analysis |

**(b) Spring-supported beam.** The beam is statically indeterminate to the first degree. Take the spring force $R$ as the redundant (acting upward on the beam). The spring stretches downward by $R/k$ and its strain energy is $R^2/2k$; the total strain energy is

$$\begin{gathered}U=\int_0^{2L}\frac{M^2}{2EI}dx+\frac{R^2}{2k} \\ \frac{\partial U}{\partial R}=0\end{gathered}$$

The beam is symmetric, so use one half and double it. With $w=P/2L$ and the reactions $\begin{gathered}A=B=\dfrac P2-\dfrac R2\end{gathered}$ (measured from the left end):

$$\begin{gathered}M=\left(\frac P2-\frac R2\right)x-\frac{wx^2}{2} \\ \frac{\partial M}{\partial R}=-\frac x2 \\ (0\le x\le L)\end{gathered}$$

$$\frac{\partial U}{\partial R}=2\int_0^L\frac{M}{EI}\left(-\frac x2\right)dx+\frac Rk=0$$

$$-\frac1{EI}\int_0^L\left[\left(\frac P2-\frac R2\right)x^2-\frac{P}{4L}x^3\right]dx+\frac Rk=0$$

$$-\frac1{EI}\left[\left(\frac P2-\frac R2\right)\frac{L^3}{3}-\frac{PL^3}{16}\right]+\frac Rk=0\ \Rightarrow\ \frac{5PL^3}{48EI}-\frac{RL^3}{6EI}=\frac Rk$$

(The left-hand side is the net upward central deflection of the beam: $\dfrac{5w(2L)^4}{384EI}=\dfrac{5PL^3}{48EI}$ for the UDL minus $\dfrac{R(2L)^3}{48EI}=\dfrac{RL^3}{6EI}$ for the spring force; it must equal the spring extension $R/k$.) Solving,

$$R\left(\frac{L^3}{6EI}+\frac1k\right)=\frac{5PL^3}{48EI}\ \Rightarrow\ \boxed{R=\frac{5P}{8}\cdot\frac{1}{1+\dfrac{6EI}{kL^3}}}$$

Limits: $k\to\infty$ (rigid support) gives $R=5P/8$, the middle reaction of a two-span continuous beam; $k\to0$ gives $R=0$, the simply supported beam. The end reactions are $\begin{gathered}A=B=(P-R)/2\end{gathered}$.

@s 2
Members: $AB,CD,AC,BD,AD,BC$ ($m=6$), joints $j=4$, reactions $r=4$ (two pins): $\begin{gathered}D_s=m+r-2j=6+4-8=\mathbf2\end{gathered}$. A suitable choice of redundants is the bottom chord $AB$ ($X_1$) and the diagonal $BC$ ($X_2$): after their removal the remaining members $CD, AC, BD, AD$ with the two pins form a stable, determinate structure (triangle $ACD$ pinned at $A$, and the link $DB$ to the pin $B$). Joints: $A(0,0)$, $B(4,0)$, $C(0,3)$, $D(4,3)$; lengths $\begin{gathered}AB=CD=4\end{gathered}$, $\begin{gathered}AC=BD=3\end{gathered}$, $\begin{gathered}AD=BC=5\end{gathered}$ m. Tension positive.

**Primary structure with the 35 kN load ($F_0$).** Joint $C$ (members $CD$, $AC$; $BC$ removed): $\Sigma F_y$: $F_{AC}=0$; $\Sigma F_x$: $\begin{gathered}F_{CD}+35=0\Rightarrow F_{CD}=-35\end{gathered}$. Joint $D$ (the compressed $CD$ pushes $D$ to the right with 35 kN; $AD$ pulls $D$ towards $A$ with components $0.8F_{AD}$ and $0.6F_{AD}$; $BD$ is vertical): $\Sigma F_x$: $35-0.8F_{AD}=0$ and $\Sigma F_y$: $-0.6F_{AD}-F_{BD}=0$, so

$$\begin{gathered}F_{AD}=\frac{35}{0.8}=+43.75\ \text{(T)} \\ F_{BD}=-0.6\times43.75=-26.25\ \text{(C)}\end{gathered}$$

**Unit load cases.** $X_1=1$ (a tension pair on $A$ and $B$ along $AB$) is carried directly by the two pins; no forces appear in the other members: $f^{(1)}=0$ in $CD,AC,BD,AD$. $X_2=1$ (pair along $BC$): $f_{CD}=-0.8$, $f_{AC}=-0.6$, $f_{BD}=-0.6$, $f_{AD}=+1$.

*Flexibility terms* (in units of $1/EA$, $L$ in m):

$$\begin{gathered}\delta_{11}=4 \\ \delta_{12}=0 \\ \delta_{10}=0\end{gathered}$$

$$\delta_{22}=0.8^2(4)+0.6^2(3)+0.6^2(3)+1^2(5)+1^2(5)=2.56+1.08+1.08+5+5=14.72$$

$$\delta_{20}=(-35)(-0.8)(4)+0+(-26.25)(-0.6)(3)+(43.75)(1)(5)=112+47.25+218.75=378$$

*Compatibility:*

$$\begin{bmatrix}4&0\\0&14.72\end{bmatrix}\begin{Bmatrix}X_1\\X_2\end{Bmatrix}=-\begin{Bmatrix}0\\378\end{Bmatrix}\ \Rightarrow\ X_1=0,\quad X_2=-\frac{378}{14.72}=-25.68\ \text{kN}$$

$AB$ carries no force because its two ends are held by two fixed pins at the same level: it cannot change in length. Final forces $F=F_0+X_2f^{(2)}$:

| Member | $AB$ | $CD$ | $AC$ | $BD$ | $AD$ | $BC$ |
|---|---|---|---|---|---|---|
| $F_0$ (kN) | – | −35.00 | 0 | −26.25 | +43.75 | – |
| $X_2f^{(2)}$ (kN) | – | +20.54 | +15.41 | +15.41 | −25.68 | −25.68 |
| **Final force (kN)** | **0** | **−14.46 (C)** | **+15.41 (T)** | **−10.84 (C)** | **+18.07 (T)** | **−25.68 (C)** |

**Reactions.** $A$: $H_A=-14.46$ kN (to the left), $V_A=-26.25$ kN (downward); $B$: $H_B=-20.54$ kN (to the left), $V_B=+26.25$ kN (upward). Checks: $\begin{gathered}\Sigma H=-14.46-20.54+35=0\end{gathered}$ ✓, $\Sigma V=0$ ✓, joint $A$: $15.41+0.6(18.07)=26.25$ ✓. (The same answer follows from the direct stiffness method on the four joints, used as a cross-check.)

@s 3
**Two-hinged parabolic arch.** The loading is asymmetric and the moment of inertia is not stated, so the usual textbook assumption for a two-hinged arch is made, $I=I_c\sec\theta$ (secant variation). Then $ds/I=dx/I_c$ and the thrust is

$$H=\frac{\int M_0\,y\,dx}{\int y^2\,dx}$$

*Arch axis:* $\begin{gathered}y=\dfrac{4h}{L^2}x(L-x)=0.004\,x(100-x)\end{gathered}$ ($h=10$ m, $L=100$ m); $y(80)=6.4$ m.

*Vertical reactions* (loads: UDL $10\times50=500$ kN at $x=25$; $100$ kN at $x=80$):

$$\begin{gathered}V_B=\frac{500(25)+100(80)}{100}=205\ \text{kN} \\ V_A=600-205=395\ \text{kN}\end{gathered}$$

*Beam moments:* $0\le x\le50$: $M_0=395x-5x^2$; $50\le x\le80$: $M_0=395x-500(x-25)$; $80\le x\le100$: $M_0=205(100-x)$.

$$\begin{gathered}\int_0^{100}M_0\,y\,dx=3.952\times10^{6}\ \text{kN·m}^2 \\ \int_0^{100}y^2dx=\frac8{15}h^2L=\frac8{15}(10)^2(100)=5333.3\ \text{m}^3\end{gathered}$$

$$H=\frac{3.952\times10^{6}}{5333.3}=\boxed{741\ \text{kN}}$$

*Support reactions:* $V_A=395$ kN$\uparrow$, $V_B=205$ kN$\uparrow$, $\begin{gathered}H_A=H_B=741\end{gathered}$ kN (inward).

*Some resulting moments* $M=M_0-Hy$: at $x=25$ m: $6750-741(7.5)=+1192.5$ kN·m; at C ($x=50$): $395(50)-5(2500)-741(10)=-160$ kN·m; at D ($x=80$): $4100-741(6.4)=-642.4$ kN·m.

*Check with constant $I$:* integrating with the true arc length $ds=\sqrt{1+y'^2}\,dx$ and constant $I$ gives $H=741.2$ kN (numerical integration), practically the same value, so the result does not depend on the assumption.

@s 4
**Slope-deflection method.** $\theta_A=0$ (fixed), no settlement ($\psi=0$ for all spans). Unknowns $\theta_B,\theta_C$. Clockwise end moments are positive. $M_{ij}=M^F_{ij}+\dfrac{2EI}{L}(2\theta_i+\theta_j)$.

*Fixed-end moments:*

$$\begin{gathered}M^F_{AB}=-\frac{wL^2}{12}=-\frac{10(25)}{12}=-20.833 \\ M^F_{BA}=+20.833\end{gathered}$$

$$\begin{gathered}M^F_{BC}=-\frac{PL}8=-\frac{200(6)}8=-150 \\ M^F_{CB}=+150\ \text{kN·m}\end{gathered}$$

*Overhang CD:* $\begin{gathered}M_{CD}=-20\times2=-40\end{gathered}$ kN·m, so at joint C: $M_{CB}=+40$.

*Slope-deflection equations* ($\Theta=EI\theta$):

$$\begin{gathered}M_{AB}=-20.833+0.4\,\Theta_B\\ M_{BA}=20.833+0.8\,\Theta_B\\ M_{BC}=-150+\tfrac23(2\Theta_B+\Theta_C)\ \ \text{(the factor }2\times2EI/6=2EI/3)\\ M_{CB}=150+\tfrac23(2\Theta_C+\Theta_B)\end{gathered}$$

*Joint conditions:* $M_{BA}+M_{BC}=0$ and $M_{CB}=40$:

$$\begin{gathered}2.1333\,\Theta_B+0.6667\,\Theta_C=129.167\\0.6667\,\Theta_B+1.3333\,\Theta_C=-110\end{gathered}$$

$$\boxed{EI\theta_B=102.31,\qquad EI\theta_C=-133.66}$$

*End moments:*

| $M_{AB}$ | $M_{BA}$ | $M_{BC}$ | $M_{CB}$ | $M_{CD}$ |
|---|---|---|---|---|
| **+20.09** | **+102.69** | **−102.69** | **+40.00** | **−40.00** |

Joint check: $M_{BA}+M_{BC}=0$ ✓.

*Reactions* ($V_{left}=[\sum Pd-M_L-M_R]/L$): $V_{AB}=0.44$, $V_{BA}=49.56$; $V_{BC}=110.45$, $V_{CB}=89.55$ kN, hence

$$R_A=0.44\ \text{kN}\uparrow,\quad R_B=49.56+110.45=160.00\ \text{kN}\uparrow,\quad R_C=89.55+20=109.55\ \text{kN}\uparrow$$

Check: $\begin{gathered}0.44+160.00+109.55=270=50+200+20\end{gathered}$ ✓.

*Bending moments:* $M_A=+20.09$ (sagging); $M_B=-102.69$ (hogging); under the 200 kN load $\begin{gathered}M=M_{BC}+V_{BC}(3)=+228.66\end{gathered}$ kN·m (sagging, maximum); $M_C=-40$ (hogging); $M_D=0$. The moment at A is of the opposite sign to the usual fixed-end hogging because the heavily loaded BC span rotates joint B strongly.

@s 5
**Moment distribution with sway.** The frame can sway: B and C move together horizontally (beam axially rigid) with the same $\Delta$ for both 6 m columns. Support E is fixed, D hinged, A fixed. $EI$ is the column rigidity and $2EI$ the beam rigidity.

*Stiffness* ($K$) and distribution factors (D is hinged, so CD uses $3EI/L$):

| Joint | Member | $K$ | DF |
|---|---|---|---|
| B | BA $\ 4(2EI)/5$ | $1.6EI$ | 0.375 |
| B | BC $\ 4(2EI)/4$ | $2.0EI$ | 0.469 |
| B | BE $\ 4EI/6$ | $0.667EI$ | 0.156 |
| C | CB $\ 4(2EI)/4$ | $2.0EI$ | 0.800 |
| C | CD $\ 3EI/6$ | $0.5EI$ | 0.200 |

*Fixed-end moments (stage 1, sway prevented):*

$$M^F_{AB}=-\frac{50(2)(3)^2}{25}=-36,\quad M^F_{BA}=+\frac{50(2)^2(3)}{25}=+24,\quad M^F_{BC}=-\frac{10(16)}{12}=-13.33,\quad M^F_{CB}=+13.33$$

$$\begin{gathered}M^F_{BE}=+\frac{200(6)}8=+150 \\ M^F_{EB}=-150\ \text{kN·m}\end{gathered}$$

(The sign of the column FEM follows from rotating the standard beam result: a load to the right on a column running downward from B is opposite to the rotated downward load.)

*Stage 1 distribution (iterated to convergence):* $M_{AB}=-68.14$, $M_{BA}=-40.28$, $M_{BC}=-82.94$, $M_{BE}=+123.22$, $M_{EB}=-163.39$, $M_{CB}=-5.37$, $M_{CD}=+5.37$ kN·m. The sum of the column end moments is $123.22-163.39+5.37=-34.80$ kN·m, which is not in equilibrium with the 200 kN: the horizontal equilibrium of the frame requires $M_{BE}+M_{EB}+M_{CD}+M_{DC}+600=0$ (from $H_E+H_D+200=0$ with the load at mid-height), so a sway correction is needed (residual $=565.2$).

*Stage 2 (sway, arbitrary $\Delta=100/EI$):* the column fixed-end moments are $-6EI\Delta/L^2=-16.67$ (BE and EB) and $-3EI\Delta/L^2=-8.33$ (CD, hinged far end). Distributing gives $M_{AB}=2.76$, $M_{BA}=5.52$, $M_{BC}=8.85$, $M_{BE}=-14.37$, $M_{EB}=-15.52$, $M_{CB}=7.36$, $M_{CD}=-7.36$ kN·m; the column sum is $-37.24$.

*Combination:* final $=$ stage 1 $+\ \lambda\,\times$ stage 2 with $-34.80+\lambda(-37.24)+600=0$, so $\begin{gathered}\lambda=\dfrac{565.2}{37.24}=15.18\end{gathered}$.

**Final end moments (kN·m):**

| $M_{AB}$ | $M_{BA}$ | $M_{BC}$ | $M_{BE}$ | $M_{EB}$ | $M_{CB}$ | $M_{CD}$ | $M_{DC}$ |
|---|---|---|---|---|---|---|---|
| **−26.27** | **+43.46** | **+51.38** | **−94.84** | **−398.89** | **+106.28** | **−106.28** | **0** |

Joint checks: B: $43.46+51.38-94.84=0$ ✓; C: $106.28-106.28=0$ ✓. (The same values come out of the slope-deflection equations with the unknowns $\theta_B,\theta_C,\Delta$; the sway is $\Delta=1517.7/EI$ to the right.)

*Reactions:* the column shears give $H_E=182.29$ kN and $H_D=17.71$ kN, both to the left ($182.29+17.71=200$ ✓). Vertical: $V_A=26.56$ kN$\uparrow$, $V_E=4.02$ kN$\uparrow$, $V_D=59.41$ kN$\uparrow$ (sum $90=50+40$ ✓); $M_A=26.27$ kN·m (anticlockwise).

@s 6
**Data.** Nodes (cm): 1 (0, 30), 2 (0, 0), 3 (40, 30), 4 (40, 0). Elements: (1-3) $L=40$, (1-2) $L=30$, (2-3) $L=50$, (2-4) $L=40$. $EA$ is common (not given): the member forces and reactions do not depend on it, the displacements are proportional to $1/EA$.

**(a) Member stiffness matrices.** $\mathbf k=\dfrac{EA}{L}\begin{bmatrix}c^2&cs&-c^2&-cs\\cs&s^2&-cs&-s^2\\-c^2&-cs&c^2&cs\\-cs&-s^2&cs&s^2\end{bmatrix}$ for the degrees of freedom $(u_i,v_i,u_j,v_j)$, $c,s$ for the direction $i\to j$.

| Element | $L$ (cm) | $c$ | $s$ | $EA/L$ | Matrix |
|---|---|---|---|---|---|
| 1-3 | 40 | 1 | 0 | $EA/40$ | $\dfrac{EA}{40}\begin{bmatrix}1&0&-1&0\\0&0&0&0\\-1&0&1&0\\0&0&0&0\end{bmatrix}$ |
| 1-2 | 30 | 0 | −1 | $EA/30$ | $\dfrac{EA}{30}\begin{bmatrix}0&0&0&0\\0&1&0&-1\\0&0&0&0\\0&-1&0&1\end{bmatrix}$ |
| 2-3 | 50 | 0.8 | 0.6 | $EA/50$ | $\dfrac{EA}{50}\begin{bmatrix}0.64&0.48&-0.64&-0.48\\0.48&0.36&-0.48&-0.36\\-0.64&-0.48&0.64&0.48\\-0.48&-0.36&0.48&0.36\end{bmatrix}$ |
| 2-4 | 40 | 1 | 0 | $EA/40$ | $\dfrac{EA}{40}\begin{bmatrix}1&0&-1&0\\0&0&0&0\\-1&0&1&0\\0&0&0&0\end{bmatrix}$ |

**(b) Assembly.** The restraints are: node 1 on a roller ($v_1=0$), nodes 3 and 4 pinned ($\begin{gathered}u=v=0\end{gathered}$). The free degrees of freedom are $u_1,u_2,v_2$. Adding the element terms:

$$EA\begin{bmatrix}0.025&0&0\\0&0.0378&0.0096\\0&0.0096&0.04053\end{bmatrix}\begin{Bmatrix}u_1\\u_2\\v_2\end{Bmatrix}=\begin{Bmatrix}-20\\0\\25\end{Bmatrix}$$

The terms are $K_{u_1u_1}=\tfrac1{40}$ (member 1-3); $K_{u_2u_2}=\tfrac1{40}+\tfrac{0.64}{50}=0.0378$; $K_{v_2v_2}=\tfrac1{30}+\tfrac{0.36}{50}=0.04053$; $K_{u_2v_2}=\tfrac{0.48}{50}=0.0096$.

$$\begin{gathered}u_1=-\frac{800}{EA} \\ u_2=-\frac{166.7}{EA} \\ v_2=+\frac{656.3}{EA}\ \ (\text{cm, with }EA\text{ in kN})\end{gathered}$$

*Member forces* $F=\dfrac{EA}{L}(\Delta u\cdot\hat n)$: $F_{13}=+20.00$ kN (tension), $F_{12}=-21.88$ kN (compression), $F_{23}=-5.21$ kN (compression), $F_{24}=+4.17$ kN (tension).

**Reactions** $\{R\}=[K]\{u\}-\{P\}$:

| Support | $R_x$ (kN) | $R_y$ (kN) |
|---|---|---|
| Node 1 (roller) | 0 | **−21.88** (downward) |
| Node 3 (pin) | **+15.83** (to the right) | **−3.13** (downward) |
| Node 4 (pin) | **+4.17** (to the right) | 0 |

Equilibrium: $\begin{gathered}\Sigma R_x=15.83+4.17=20\end{gathered}$ kN balances the 20 kN to the left ✓; $\begin{gathered}\Sigma R_y=-21.88-3.13=-25\end{gathered}$ kN balances the 25 kN upward ✓. Joint 2: $25-21.88-0.6(5.21)=0$ ✓ and $-0.8(5.21)+4.17=0$ ✓. (The figure was read as: the arrow below node 2 is an upward 25 kN load, the ring at node 1 is a roller on a horizontal surface, and nodes 3 and 4 are pins.)

@s 7
**Plastic moment of the frame, load factor 1.5.** Factored load: $\begin{gathered}w=1.5\times20=30\end{gathered}$ kN/m horizontal on AB. Supports A and D are hinges ($M=0$); the frame is indeterminate to the first degree (4 reactions $-3$). Possible hinge positions: C (and B), and a point P on AB where the moment is a maximum under the UDL. Two hinges (P and C) give a mechanism.

**Mechanism.** Hinges at P (height $y$ above A) and C, pins at A and D. The part AP rotates about A, the rigid piece P-B-C translates horizontally by $\delta$ (the instantaneous centres of P and C lie on parallel verticals, so the centre of PBC is at infinity), and CD rotates about D.

$$\begin{gathered}\theta_{AP}=\frac{\delta}{y} \\ \theta_{CD}=\frac\delta2 \\ \text{hinge rotations: P}=\frac\delta y,\ \ \text{C}=\frac\delta2\end{gathered}$$

*Virtual work:* internal $M_p\left(\dfrac\delta y+\dfrac\delta2\right)$; external work of the UDL: on AP, average displacement $\delta/2$: $30\,y\,\dfrac\delta2$; on PB (length $4-y$) displacement $\delta$: $30(4-y)\delta$:

$$M_p\,\delta\,\frac{2+y}{2y}=30\,\delta\left(4-\frac y2\right)\ \Rightarrow\ M_p=\frac{30\,y(8-y)}{2+y}$$

The collapse mechanism corresponds to the largest $M_p$ over the possible hinge positions: $\dfrac{dM_p}{dy}=0$ gives $y^2+4y-16=0$, so $\begin{gathered}y=-2+\sqrt{20}=2.472\end{gathered}$ m, and

$$M_p=\frac{30(2.472)(5.528)}{4.472}=\boxed{91.67\ \text{kN·m}}$$

**Static check.** Let $A_x$ be the horizontal reaction at A (the redundant). The moments are $M(y)=A_xy+15y^2$ in AB, $M_B=4A_x+240$, $M_C=2A_x+240$. Choosing $A_x=-74.17$ kN: $M_C=+91.67$ kN·m, the maximum in AB is $-A_x^2/60=-91.67$ kN·m at $\begin{gathered}y=-A_x/30=2.472\end{gathered}$ m, and $M_B=-56.7$ kN·m, so $|M|\le M_p$ everywhere with hinges at C and at P: the moment diagram is statically admissible and the mechanism is correct. The required plastic moment is $M_p=91.67$ kN·m (corresponding to $61.1$ kN·m for the working loads).

@s 8
**ILD for the reaction at the fixed support A of a propped cantilever** (fixed at A, roller at B, $L=6$ m). Remove the prop B: for a unit load at distance $x$ from A the deflection at B of the cantilever is $\dfrac{x^2(3L-x)}{6EI}$ and the deflection due to a unit force at B is $\dfrac{L^3}{3EI}$. Compatibility at B gives the prop reaction

$$R_B(x)=\frac{x^2(3L-x)}{2L^3}$$

and from the vertical equilibrium

$$R_A(x)=1-R_B(x)=1-\frac{x^2(3L-x)}{2L^3}=1-\frac{x^2(18-x)}{432}$$

*Ordinates at 1 m intervals:*

| $x$ from A (m) | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $R_B$ | 0 | 0.0394 | 0.1481 | 0.3125 | 0.5185 | 0.7523 | 1.0000 |
| **$R_A$ (ILD ordinate)** | **1.0000** | **0.9606** | **0.8519** | **0.6875** | **0.4815** | **0.2477** | **0** |

For the fixed-end moment (hogging), in the same way $M_A(x)=\dfrac{x(L-x)(2L-x)}{2L^2}$, with ordinates (kN·m per unit load) $0,\ 0.764,\ 1.111,\ 1.125,\ 0.889,\ 0.486,\ 0$ at $x=0\ldots6$ m (maximum $1.125$ near $x=2.7$ m).

```figure caption="Question 8: influence line for the reaction R_A at the fixed support of the propped cantilever (ordinates at 1 m). Unity at A, falling to zero at the prop B."
fig,ax=plt.subplots(figsize=(5.4,2.6))
x=np.arange(0,7); y=1-x**2*(18-x)/432.0
xs=np.linspace(0,6,100); ax.plot(xs,1-xs**2*(18-xs)/432.0,color=ACCENT,lw=2); ax.plot(x,y,"o",color=ACCENT)
ax.fill_between(xs,0,1-xs**2*(18-xs)/432.0,color=ACCENT,alpha=0.12); ax.axhline(0,color=INK,lw=1.5)
for a,b in zip(x,y): ax.text(a,b+0.05,f"{b:.3f}",ha="center",fontsize=8)
ax.text(0,-0.14,"A",ha="center",fontweight="bold"); ax.text(6,-0.14,"B",ha="center",fontweight="bold")
ax.set_xlabel("position of unit load x from A (m)"); ax.set_ylabel("R_A"); ax.set_ylim(-0.2,1.2); ax.set_xlim(-0.4,6.4)
```

---
file: NEBians-IOE-Past-Paper-Theory-of-Structures-II-ENCE252-2083-Baishakh.pdf
subject: Theory of Structures II
level: BE · Year II / Part II
code: ENCE 252
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Civil, Year II / Part II. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Describe difference between static and kinematic indeterminacies with an example. [[4]]

b) Determine the reaction at the support B in the figure below using Castigliano's theorem. [[6]]

```figure caption="Question 1(b): beam ABC, pin at A, rollers at B (4 m from A) and C (6 m beyond B). A 10 kN/m UDL acts on AB, which has flexural rigidity EI; BC has 2EI."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,2.0)); ax.axis("off")
ax.plot([0,10],[0,0],color=INK,lw=3)
for x in np.linspace(0.2,3.8,10): ax.annotate("",xy=(x,0.05),xytext=(x,0.8),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1))
ax.text(2,0.95,"10 kN/m",ha="center",fontsize=9)
ax.plot([0,-0.3,0.3,0],[0,-0.55,-0.55,0],color=INK,lw=1.8)
for x in (4,10): ax.add_patch(mp.Circle((x,-0.3),0.28,fc="white",ec=INK,lw=1.6)); ax.plot([x-0.5,x+0.5],[-0.62,-0.62],color=INK,lw=1.6)
for x,t in ((0,"A"),(4,"B"),(10,"C")): ax.text(x,0.35 if x else -1.1,t,ha="center",fontsize=9,fontweight="bold")
ax.text(2,-1.25,"4 m   (EI)",ha="center",fontsize=8.5); ax.text(7,-1.25,"6 m   (2EI)",ha="center",fontsize=8.5)
ax.set_xlim(-1,11); ax.set_ylim(-1.6,1.4)
```

@q 2
Compute the member forces of the truss shown in the figure below due to, [[10]]

a) loads given

b) member 02 is large by 2 cm

c) member 02 is heated by 36 °C

$\alpha=15\times10^{-6}/{}^\circ$C, $E=2\times10^{6}$ MPa, $A=500$ mm² for all members.

```figure caption="Question 2: square truss 4 m x 4 m, joints 0 (bottom left), 1 (bottom right), 2 (top right), 3 (top left); both diagonals 02 and 13; 100 kN downward and 50 kN to the right at joint 3."
fig,ax=plt.subplots(figsize=(3.8,3.4)); ax.axis("off")
P={"0":(0,0),"1":(4,0),"2":(4,4),"3":(0,4)}
for a,b in ["01","12","23","30","02","13"]: ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=2)
for k,(x,y) in P.items(): ax.text(x+(-0.35 if x==0 else 0.35),y+(-0.45 if y==0 else 0.15),k,fontsize=10,fontweight="bold",ha="center")
ax.annotate("",xy=(0,4.02),xytext=(0,5.3),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(0.15,5.3,"100 kN",fontsize=8.5)
ax.annotate("",xy=(-0.05,4),xytext=(-1.6,4),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(-2.1,4.25,"50 kN",fontsize=8.5)
ax.plot([0,-0.3,0.3,0],[0,-0.5,-0.5,0],color=INK,lw=1.6); ax.plot([4,3.7,4.3,4],[0,-0.5,-0.5,0],color=INK,lw=1.6); ax.plot([3.6,4.4],[-0.62,-0.62],color=INK,lw=1.6)
ax.text(2,-1.0,"4 m",ha="center",fontsize=8.5); ax.text(4.8,2,"4 m",fontsize=8.5,va="center")
ax.set_xlim(-2.4,5.6); ax.set_ylim(-1.4,5.9)
```

@q 3
A two hinged parabolic arch as shown in figure below has secant variation of moment of inertia. Determine the value of support reactions, bending moment, normal thrust and radial shear at 10 m from the left support. [[6]]

```figure caption="Question 3: two-hinged parabolic arch, span 30 m, crown B at a rise of 4.5 m, 20 kN/m UDL on the left half (A to B)."
fig,ax=plt.subplots(figsize=(5.4,2.7)); ax.axis("off")
x=np.linspace(0,30,200); y=4*4.5*x*(30-x)/900
ax.plot(x,y,color=INK,lw=2.6)
for xx in np.linspace(0.5,14.5,10):
    yy=4*4.5*xx*(30-xx)/900; ax.annotate("",xy=(xx,yy+0.05),xytext=(xx,yy+1.5),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1))
ax.text(7.5,4.6,"20 kN/m",ha="center",fontsize=9)
for xs in (0,30): ax.plot([xs,xs-0.8,xs+0.8,xs],[0,-0.9,-0.9,0],color=INK,lw=1.6)
ax.plot([0,30],[0,0],color=MUTED,lw=0.8,ls=":"); ax.plot([15,15],[0,4.5],color=MUTED,lw=0.8,ls=":")
ax.text(15.4,2,"4.5 m",fontsize=8.5); ax.text(15,5.0,"B",ha="center",fontsize=9,fontweight="bold"); ax.text(-0.5,0.4,"A",fontsize=9,fontweight="bold",ha="right"); ax.text(30.5,0.4,"C",fontsize=9,fontweight="bold")
ax.text(15,-1.7,"30 m",ha="center",fontsize=8.5)
ax.set_xlim(-2,32); ax.set_ylim(-2.2,6.5)
```

@q 4
Analyze the beam shown in the figure below using slope deflection method if support B sinks down by 200/EI and C uplift 100/EI. Take EI is constant. [[5]]

```figure caption="Question 4: beam fixed at A with supports B, C, D and an overhang DE. A triangular load of 10 kN/m (zero at A) on AB (3 m); 20 kN at 2 m right of B; BC = 5 m; 10 kN/m UDL on CD plus a 10 kN point load at its centre (CD = 4 m); 20 kN at the free end E, 1.5 m beyond D."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.4,2.2)); ax.axis("off")
ax.plot([0,14.5],[0,0],color=INK,lw=3)
ax.fill([0,3,3],[0,0,1.0],fc="#e8ecf5",ec=ACCENT); ax.text(1.5,1.2,"10 kN/m",ha="center",fontsize=8)
ax.annotate("",xy=(5,0.05),xytext=(5,1.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.6)); ax.text(5,1.25,"20 kN",ha="center",fontsize=8)
for xx in np.linspace(8.1,11.9,9): ax.annotate("",xy=(xx,0.05),xytext=(xx,0.8),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=0.9))
ax.text(9.2,1.25,"10 kN/m",ha="center",fontsize=8)
ax.annotate("",xy=(10,0.05),xytext=(10,1.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.6)); ax.text(10.9,1.25,"10 kN",ha="center",fontsize=8)
ax.annotate("",xy=(14.5,0.05),xytext=(14.5,1.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.6)); ax.text(14.5,1.25,"20 kN",ha="center",fontsize=8)
for x in (3,8,12): ax.add_patch(mp.Circle((x,-0.3),0.28,fc="white",ec=INK,lw=1.5)); ax.plot([x-0.5,x+0.5],[-0.62,-0.62],color=INK,lw=1.5)
ax.add_patch(mp.Rectangle((-0.5,-0.9),0.5,1.8,fc="#999",ec=INK,hatch="///"))
for x,t in ((0,"A"),(3,"B"),(8,"C"),(12,"D"),(14.5,"E")): ax.text(x,-1.15,t,ha="center",fontsize=9,fontweight="bold")
for a,b,l in ((0,3,"3 m"),(3,5,"2 m"),(5,8,"3 m"),(8,10,"2 m"),(10,12,"2 m"),(12,14.5,"1.5 m")): ax.text((a+b)/2,-1.7,l,ha="center",fontsize=7.5)
ax.set_xlim(-1,15.5); ax.set_ylim(-2.1,1.8)
```

@q 5
Analyze the frame shown in the figure below to calculate end moments using moment distribution method if support A settles down by 15 mm. Take EI = 20000 kNm² constant throughout. [[5]]

```figure caption="Question 5: frame with fixed support A (settles 15 mm), beam A-B-C (40 kN at 2 m from A, AB = 4 m; 10 kN/m UDL on BC = 3 m), hinge support at C and a 4 m column BD fixed at D."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.8,3.4)); ax.axis("off")
ax.plot([0,7],[4,4],color=INK,lw=3); ax.plot([4,4],[0,4],color=INK,lw=3)
ax.annotate("",xy=(2,4.05),xytext=(2,5.0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(2,5.15,"40 kN",ha="center",fontsize=8.5)
for xx in np.linspace(4.2,6.8,8): ax.annotate("",xy=(xx,4.05),xytext=(xx,4.8),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1))
ax.text(5.5,5.0,"10 kN/m",ha="center",fontsize=8.5)
ax.add_patch(mp.Rectangle((-0.5,3.2),0.5,1.6,fc="#999",ec=INK,hatch="///")); ax.add_patch(mp.Rectangle((3.4,-0.5),1.2,0.5,fc="#999",ec=INK,hatch="///"))
ax.plot([7,6.7,7.3,7],[4,3.4,3.4,4],color=INK,lw=1.6)
for x,y,t in ((-0.7,4.2,"A"),(3.7,4.25,"B"),(7.4,4.2,"C"),(4.35,-0.1,"D")): ax.text(x,y,t,fontsize=9,fontweight="bold")
ax.text(1,3.4,"2 m",fontsize=8,ha="center"); ax.text(3,3.4,"2 m",fontsize=8,ha="center"); ax.text(5.5,3.4,"3 m",fontsize=8,ha="center"); ax.text(4.3,2,"4 m",fontsize=8.5)
ax.set_xlim(-1.2,8.2); ax.set_ylim(-0.9,5.6)
```

@q 6
Determine member stiffness matrices for each member and using direct stiffness methods, find the displacement of node 1 for the following structure. Combine spring and bar elements. Both bars have $E=210$ GPa and $A=5\times10^{-4}$ m². The spring stiffness of spring $k=2000$ kN/m. [[3+9]]

```figure caption="Question 6: node 1 carries a 25 kN load (taken vertically downward). Bar 3-1 is horizontal, 10 m long, pinned at node 3; bar 1-2 is 5 m long at 45 degrees to the horizontal, pinned at node 2; a vertical spring k = 2000 kN/m joins node 1 to the support 4."
fig,ax=plt.subplots(figsize=(5.0,3.2)); ax.axis("off")
P={"3":(0,0),"1":(10,0),"2":(6.46,3.54),"4":(10,-3.5)}
ax.plot([0,10],[0,0],color=INK,lw=2.6); ax.plot([10,6.46],[0,3.54],color=INK,lw=2.6)
yy=np.linspace(0,-3.5,13); xx=10+np.array([0,0]+[(0.35 if i%2 else -0.35) for i in range(9)]+[0,0]); ax.plot(xx,yy,color=INK,lw=1.4)
ax.annotate("",xy=(10,-0.05),xytext=(10,1.8),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=2)); ax.text(10.3,1.6,"25 kN",fontsize=9)
for k,(x,y) in P.items(): ax.plot(x,y,"o",color=INK,ms=4); ax.text(x+(0.25 if k in "12" else -0.45 if k=="3" else 0.3),y+(0.3 if k in "12" else 0.15 if k=="3" else -0.1),k,fontsize=10,fontweight="bold")
ax.text(5,-0.55,"10 m",ha="center",fontsize=9); ax.text(7.7,2.5,"5 m",fontsize=9); ax.text(10.6,-1.8,"k = 2000 kN/m",fontsize=8.5); ax.text(8.8,0.6,"45°",fontsize=8.5)
ax.plot([-0.3,0.3],[-1,1],color=INK,lw=0.0); ax.plot([9.5,10.5],[-3.5,-3.5],color=INK,lw=2)
ax.set_xlim(-1,14); ax.set_ylim(-4.2,4.3)
```

@q 7
Draw ILD for SF at D for given continuous beam shown in the figure below. Compute ordinate at 2 m interval. Take EI = constant. [[6]]

```figure caption="Question 7: continuous beam A-D-B-C, pin at A, rollers at B and C; AD = DB = 4 m, BC = 6 m."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.4,1.7)); ax.axis("off")
ax.plot([0,14],[0,0],color=INK,lw=3)
ax.plot([0,-0.4,0.4,0],[0,-0.7,-0.7,0],color=INK,lw=1.8)
for x in (8,14): ax.add_patch(mp.Circle((x,-0.35),0.35,fc="white",ec=INK,lw=1.6)); ax.plot([x-0.6,x+0.6],[-0.8,-0.8],color=INK,lw=1.6)
for x,t in ((0,"A"),(4,"D"),(8,"B"),(14,"C")): ax.text(x,0.45,t,ha="center",fontsize=9,fontweight="bold")
ax.plot([4,4],[-0.15,0.15],color=INK,lw=2)
for a,b,l in ((0,4,"4 m"),(4,8,"4 m"),(8,14,"6 m")): ax.text((a+b)/2,-1.5,l,ha="center",fontsize=8.5)
ax.set_xlim(-1,15); ax.set_ylim(-2,1.3)
```

@q 8
Determine the plastic moment capacity of the frame for given loading for load factor 1.5 shown in figure below. [[6]]

```figure caption="Question 8: portal frame with fixed supports at A (bottom of the 2 m column AB) and D (bottom of the 6 m column CD); 20 kN horizontal at B, 50 kN vertical at 2 m from C (mid-span of BC = 4 m)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.8,3.6)); ax.axis("off")
ax.plot([0,0],[4,6],color=INK,lw=3); ax.plot([0,4],[6,6],color=INK,lw=3); ax.plot([4,4],[0,6],color=INK,lw=3)
ax.add_patch(mp.Rectangle((-0.5,3.5),1.0,0.5,fc="#999",ec=INK,hatch="///")); ax.add_patch(mp.Rectangle((3.5,-0.5),1.0,0.5,fc="#999",ec=INK,hatch="///"))
ax.annotate("",xy=(-0.05,6),xytext=(-1.4,6),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(-1.5,6.25,"20 kN",fontsize=8.5)
ax.annotate("",xy=(2,6.05),xytext=(2,7.1),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.8)); ax.text(2,7.25,"50 kN",fontsize=8.5,ha="center")
for x,y,t in ((-0.4,3.7,"A"),(-0.45,6.2,"B"),(4.2,6.2,"C"),(4.2,-0.1,"D")): ax.text(x,y,t,fontsize=9,fontweight="bold")
ax.text(-0.6,5,"2 m",fontsize=8,ha="right"); ax.text(4.6,3,"6 m",fontsize=8); ax.text(3,5.6,"2 m",fontsize=8,ha="center"); ax.text(1,5.6,"2 m",fontsize=8,ha="center"); ax.text(2,-0.9,"4 m",fontsize=8.5,ha="center")
ax.set_xlim(-2.4,5.4); ax.set_ylim(-1.3,7.8)
```

<!-- SOLUTIONS -->

@s 1
**(a) Static and kinematic indeterminacy.**

*Static indeterminacy* $D_s$ is the number of unknown forces (reactions or member forces) in excess of the equations of equilibrium; it is the number of redundants that must be released to make the structure statically determinate. It is the unknown count of the **force method**.

*Kinematic indeterminacy* $D_k$ is the number of independent joint displacements (rotations and translations) that are needed to describe the deformed shape completely; it is the unknown count of the **displacement (stiffness, slope-deflection, moment-distribution) method**.

| | Static indeterminacy $D_s$ | Kinematic indeterminacy $D_k$ |
|---|---|---|
| Unknowns | redundant forces / moments | joint rotations and translations |
| Related to | equilibrium equations | compatibility (continuity) conditions |
| Used in | flexibility (force) method | stiffness (displacement) method |
| Plane frame formula | $3m+r-3j$ | $3j-r$ (axial deformations included), fewer if members are axially rigid |
| Effect of a hinge or release | reduces $D_s$ by one | increases $D_k$ by one |

*Example.* Take a beam fixed at A and resting on rollers at B and C (two spans, a propped-cantilever type of structure). Reactions: $3+1+1=5$, equations $3$, so $\begin{gathered}D_s=5-3=2\end{gathered}$. The joint rotations $\theta_B,\theta_C$ are unknown ($\theta_A=0$, no sway because the beam is axially rigid), so $D_k=2$. For a *simply supported* beam $D_s=0$ but $D_k=2$ ($\theta_A,\theta_B$), while for a *fixed-fixed* beam $\begin{gathered}D_s=3-1=2\end{gathered}$ (3 for a beam that also resists axial load) but $D_k=0$. A fixed-base portal frame has $D_s=3$ and $D_k=3$ ($\theta_B,\theta_C$ and one sway). So the two indeterminacies are different numbers for the same structure and a designer chooses the method that has the smaller one.

**(b) Reaction at B by Castigliano's theorem.** The beam has three supports, one more than needed, so it is indeterminate to the first degree. Take $R_B$ (upward) as the redundant. Its point of application does not deflect, so (Castigliano's second theorem)

$$\frac{\partial U}{\partial R_B}=\int\frac{M}{EI}\frac{\partial M}{\partial R_B}\,dx=0$$

*Reactions in terms of $R_B$.* Moments about C: $10R_A+6R_B-40\times8=0$, so

$$\begin{gathered}R_A=32-0.6R_B \\ R_C=40-R_A-R_B=8-0.4R_B\end{gathered}$$

*Bending moments* (sagging positive). In span AB, $x$ is measured from A; in span BC it is simplest to take $s$ from the right end C, where there is no load:

$$\begin{gathered}AB\ (0\le x\le4,\ EI):\ M=R_Ax-5x^2,\quad \frac{\partial M}{\partial R_B}=-0.6x\\ BC\ (0\le s\le6,\ 2EI):\ M=R_Cs=(8-0.4R_B)s,\quad \frac{\partial M}{\partial R_B}=-0.4s\end{gathered}$$

$$\int_0^4\frac{(R_Ax-5x^2)(-0.6x)}{EI}dx+\int_0^6\frac{(8-0.4R_B)s\,(-0.4s)}{2EI}ds=0$$

Evaluate with $R_A=32-0.6R_B$:

$$\int_0^4(R_Ax^2-5x^3)\,dx=\frac{64R_A}{3}-320=\frac{64(32-0.6R_B)}{3}-320=362.67-12.8R_B$$

so the first integral is $-0.6\,(362.67-12.8R_B)=-217.6+7.68R_B$. For the second,

$$\int_0^6 s^2ds=72\ \Rightarrow\ \frac{-0.4(8-0.4R_B)\,72}{2}=-115.2+5.76R_B$$

$$-217.6+7.68R_B-115.2+5.76R_B=0\ \Rightarrow\ 13.44R_B=332.8\ \Rightarrow\ \boxed{R_B=\frac{520}{21}\approx24.76\ \text{kN}\uparrow}$$

Then $\begin{gathered}R_A=32-0.6(24.76)=\mathbf{17.14\ kN\uparrow}\end{gathered}$ and $\begin{gathered}R_C=8-0.4(24.76)=\mathbf{-1.90\ kN}\end{gathered}$ (a small downward reaction, i.e. C must be a bilateral support or be held down). Check: $17.14+24.76-1.90=40$ kN ✓. The moment at B is $\begin{gathered}M_B=17.14\times4-5\times16=-11.43\end{gathered}$ kN·m (hogging), the same as $R_C\times6=-11.43$ ✓.

@s 2
Number of members $m=6$, joints $j=4$, reactions $r=3$: $\begin{gathered}D_s=m+r-2j=6+3-8=1\end{gathered}$. Choose the diagonal **02** as the redundant ($X$, tension positive). Joints: 0 (0, 0), 1 (4, 0), 2 (4, 4), 3 (0, 4); every side is 4 m and the diagonals are $4\sqrt2=5.657$ m. $EA$ is the same for all members.

*Material.* The paper prints $E=2\times10^{6}$ MPa; for steel this is almost certainly $2\times10^{6}$ kg/cm² $\approx2\times10^{5}$ MPa, so $E=2\times10^{5}$ MPa is used: $\begin{gathered}EA=2\times10^{5}\times500=10^{8}\end{gathered}$ N $=10^{5}$ kN. (The member forces of part (a) do not depend on $E$; the forces of (b) and (c) are proportional to $E$, so the values for the printed $E$ are ten times larger and are quoted as well.)

**Reactions (from the loads, independent of the redundant).** $\Sigma F_x$: $H_0=-50$ kN (to the left). Moments about 0: $R_1\times4=50\times4$, so $R_1=50$ kN$\uparrow$; $\Sigma F_y$: $\begin{gathered}R_0=100-50=50\end{gathered}$ kN$\uparrow$.

**Primary structure ($X=0$, diagonal 02 removed), forces $F_0$** (tension positive). Joint 2 has only the members 12 and 23 (02 removed) and no load, so $\begin{gathered}F_{12}=F_{23}=0\end{gathered}$. Joint 3: $\Sigma F_x$: $F_{13}\cos45^\circ+50=0$, so $F_{13}=-70.71$ kN; $\Sigma F_y$: $-F_{30}-F_{13}\sin45^\circ-100=0$, so $F_{30}=-50$ kN. Joint 0: $\begin{gathered}F_{01}=-R_{0x}=+50\end{gathered}$ kN. Hence

$$\begin{gathered}F_{13}=-70.71\ \text{(C)} \\ F_{30}=-50\ \text{(C)} \\ F_{23}=0 \\ F_{12}=0 \\ F_{01}=+50\ \text{(T)}\end{gathered}$$

(all four joint-equilibrium pairs are satisfied).

**Unit state ($X=1$ in 02):** a pair of unit tensile forces on joints 0 and 2 is equilibrated by $f_{13}=+1$ and $\begin{gathered}f_{01}=f_{12}=f_{23}=f_{30}=-0.7071\end{gathered}$ (no reactions arise).

*Flexibility coefficients* ($L$ in m, divided by $EA$):

$$\delta_{10}=\sum\frac{F_0f\,L}{EA}=\frac{1}{EA}\left[50(-0.7071)4+(-50)(-0.7071)4+(-70.71)(1)(5.657)\right]=\frac{-400}{EA}$$

$$\delta_{11}=\sum\frac{f^2L}{EA}=\frac{1}{EA}\left[4(0.5)(4)+1(5.657)+1(5.657)\right]=\frac{19.31}{EA}$$

**(a) Loads.** $X\delta_{11}+\delta_{10}=0$:

$$X=-\frac{\delta_{10}}{\delta_{11}}=\frac{400}{19.31}=\boxed{+20.71\ \text{kN (tension in 02)}}$$

Final forces $F=F_0+Xf$:

| Member | 01 | 12 | 23 | 30 | 02 | 13 |
|---|---|---|---|---|---|---|
| Force (kN) | +35.36 (T) | −14.64 (C) | −14.64 (C) | −64.64 (C) | **+20.71 (T)** | **−50.00 (C)** |

Check at joint 3: $\begin{gathered}\Sigma F_x=-14.64+0.7071(-50)+50=0\end{gathered}$ ✓, $\begin{gathered}\Sigma F_y=64.64+0.7071(50)-100=0\end{gathered}$ ✓.

**(b) Member 02 is 20 mm too long (lack of fit).** The member is forced between joints 0 and 2 and is compressed. The compatibility condition is $X\delta_{11}=-\lambda$ (the member is longer than the gap by $\lambda=0.02$ m):

$$X=-\frac{0.02\times EA}{19.31}=-\frac{0.02\times10^{5}}{19.31}=\boxed{-103.6\ \text{kN (C) in 02}}$$

Other members: $F=Xf$: $F_{13}=-103.6$ (C), $\begin{gathered}F_{01}=F_{12}=F_{23}=F_{30}=+0.7071\times103.6=+73.2\end{gathered}$ kN (T). There are no reactions. (With the printed $E=2\times10^{6}$ MPa all these are $\times10$: $-1035.5$ and $+732.2$ kN.)

**(c) Member 02 heated by 36 °C.** Free expansion $\begin{gathered}\lambda=\alpha\,\Delta T\,L=15\times10^{-6}\times36\times5657=3.055\end{gathered}$ mm $=0.003055$ m; the surrounding frame restrains it, so

$$X=-\frac{\lambda\,EA}{19.31}=-\frac{0.003055\times10^{5}}{19.31}=\boxed{-15.82\ \text{kN (C) in 02}}$$

$F_{13}=-15.82$ kN (C) and $\begin{gathered}F_{01}=F_{12}=F_{23}=F_{30}=+11.18\end{gathered}$ kN (T); reactions are zero (printed $E$: $-158.2$ and $+111.8$ kN).

| Member | 01 | 12 | 23 | 30 | 02 | 13 |
|---|---|---|---|---|---|---|
| (a) loads | +35.36 | −14.64 | −14.64 | −64.64 | +20.71 | −50.00 |
| (b) misfit 2 cm | +73.22 | +73.22 | +73.22 | +73.22 | −103.55 | −103.55 |
| (c) heating 36 °C | +11.18 | +11.18 | +11.18 | +11.18 | −15.82 | −15.82 |

(T positive; the effects may be superposed for a combined case.)

@s 3
**Two-hinged arch with $I=I_c\sec\theta$.** The arch is indeterminate to the first degree; the horizontal thrust $H$ is the redundant. Condition: no horizontal movement of the support, $\partial U/\partial H=0$:

$$\begin{gathered}\int\frac{M}{EI}\frac{\partial M}{\partial H}ds=0 \\ M=M_0-Hy,\quad \frac{\partial M}{\partial H}=-y\end{gathered}$$

With $I=I_c\sec\theta$ and $ds=dx\sec\theta$, the factor $ds/I=dx/I_c$, so

$$H=\frac{\int M_0\,y\,dx}{\int y^2\,dx}$$

*Arch axis:* $\begin{gathered}y=\dfrac{4h}{L^2}x(L-x)=0.02\,x(30-x)\end{gathered}$ ($h=4.5$ m, $L=30$ m).

*Beam moments $M_0$ (simply supported span).* $\begin{gathered}V_A=300\times22.5/30=225\end{gathered}$ kN, $V_C=75$ kN. For $0\le x\le15$: $M_0=225x-10x^2$; for $15\le x\le30$: $M_0=75(30-x)$.

$$\int M_0y\,dx=0.02\left[\int_0^{15}(225x-10x^2)\,x(30-x)\,dx+\int_{15}^{30}75(30-x)\,x(30-x)\,dx\right]=0.02\times4.05\times10^{6}=81\,000$$

$$\int_0^{30}y^2dx=\frac{8}{15}h^2L=\frac{8}{15}(4.5)^2(30)=324$$

$$H=\frac{81000}{324}=\boxed{250\ \text{kN}}$$

**Support reactions:** $V_A=\mathbf{225\ kN\uparrow}$, $V_C=\mathbf{75\ kN\uparrow}$, $\begin{gathered}H_A=H_C=\mathbf{250\ kN}\end{gathered}$ (inward). Check: the crown moment is $\begin{gathered}M_B=225(15)-20\times15\times7.5-250\times4.5=3375-2250-1125=0\end{gathered}$ (the crown carries no moment, a good check).

**Section at $x=10$ m.**

$$\begin{gathered}y=0.02\times10\times20=4.0\ \text{m} \\ \tan\theta=\frac{dy}{dx}=0.02(30-2\times10)=0.2\ \Rightarrow\ \theta=11.31^\circ\end{gathered}$$

$\cos\theta=0.9806$, $\sin\theta=0.1961$.

$\begin{gathered}M_0=225(10)-10(10)^2=1250\end{gathered}$ kN·m. Beam shear $\begin{gathered}V=225-20\times10=25\end{gathered}$ kN.

$$\begin{gathered}M=M_0-Hy=1250-250\times4=\boxed{250\ \text{kN·m (sagging)}}\\ N=V\sin\theta+H\cos\theta=25(0.1961)+250(0.9806)=\boxed{250.0\ \text{kN (compression)}}\\ V_r=V\cos\theta-H\sin\theta=25(0.9806)-250(0.1961)=\boxed{-24.5\ \text{kN}}\end{gathered}$$

The negative radial shear means its sense is opposite to the usual positive sense.

@s 4
**Slope-deflection method.** $\theta_A=0$ (fixed). Unknowns $\theta_B,\theta_C,\theta_D$. The sign convention: end moments clockwise positive; $\psi=\Delta/L$ is positive when the right end of a member moves down relative to the left end. Equation: $M_{ij}=M^F_{ij}+\dfrac{2EI}{L}\left(2\theta_i+\theta_j-3\psi\right)$.

*Settlements (downward positive):* $\Delta_B=200/EI$, $\Delta_C=-100/EI$ (up), $\Delta_D=0$.

$$\begin{gathered}\psi_{AB}=\frac{200}{3EI} \\ \psi_{BC}=\frac{-100-200}{5EI}=-\frac{60}{EI} \\ \psi_{CD}=\frac{0-(-100)}{4EI}=\frac{25}{EI}\end{gathered}$$

*Fixed-end moments (loads):*

| Span | FEM (kN·m) |
|---|---|
| AB (triangular, zero at A, 10 kN/m at B) | $\begin{gathered}M^F_{AB}=-\dfrac{w_0L^2}{30}=-3.0,\ M^F_{BA}=+\dfrac{w_0L^2}{20}=+4.5\end{gathered}$ |
| BC (20 kN, $a=2$, $b=3$) | $\begin{gathered}M^F_{BC}=-\dfrac{Pab^2}{L^2}=-14.4,\ M^F_{CB}=+\dfrac{Pa^2b}{L^2}=+9.6\end{gathered}$ |
| CD (10 kN/m, 4 m; 10 kN at centre) | $\mp\left(\dfrac{10\times16}{12}+\dfrac{10\times4}{8}\right)=\mp18.333$ |

*Overhang DE:* $\begin{gathered}M_{DE}=-20\times1.5=-30\end{gathered}$ kN·m (hogging), so the joint D requires $M_{DC}=+30$.

*Slope-deflection equations* ($EI\theta\to\Theta$; the factor $EI$ cancels because the settlements are in $1/EI$):

$$\begin{gathered}M_{AB}=-3+\tfrac23(\Theta_B-200)\\ M_{BA}=4.5+\tfrac23(2\Theta_B-200)\\ M_{BC}=-14.4+0.4(2\Theta_B+\Theta_C+180)\\ M_{CB}=9.6+0.4(2\Theta_C+\Theta_B+180)\\ M_{CD}=-18.333+0.5(2\Theta_C+\Theta_D-75)\\ M_{DC}=18.333+0.5(2\Theta_D+\Theta_C-75)\end{gathered}$$

*Equilibrium:* $M_{BA}+M_{BC}=0$, $M_{CB}+M_{CD}=0$, $M_{DC}=30$:

Collecting terms gives three linear equations:

$$\begin{gathered}2.1333\,\Theta_B+0.4\,\Theta_C=71.233\\0.4\,\Theta_B+1.8\,\Theta_C+0.5\,\Theta_D=-25.767\\0.5\,\Theta_C+\Theta_D=49.167\end{gathered}$$

Solving them (elimination, or on a calculator) gives

$$\boxed{EI\theta_B=41.49,\quad EI\theta_C=-43.19,\quad EI\theta_D=70.76}$$

**End moments (kN·m):**

| $M_{AB}$ | $M_{BA}$ | $M_{BC}$ | $M_{CB}$ | $M_{CD}$ | $M_{DC}$ | $M_{DE}$ |
|---|---|---|---|---|---|---|
| **−108.67** | **+73.51** | **−73.51** | **+63.64** | **−63.64** | **+30.00** | **−30.00** |

Joint checks: $M_{BA}+M_{BC}=0$ ✓, $M_{CB}+M_{CD}=0$ ✓, $M_{DC}+M_{DE}=0$ ✓.

**Reactions** (span equilibrium, $V_{left}=\left[\sum Pd-M_L-M_R\right]/L$): $V_{AB}=65.73$, $V_{BA}=-50.73$; $V_{BC}=-15.43$, $V_{CB}=35.43$; $V_{CD}=33.41$, $V_{DC}=16.59$ (+20 kN from the overhang):

$$R_A=65.73\uparrow,\quad R_B=-66.16\ (66.16\downarrow),\quad R_C=68.84\uparrow,\quad R_D=36.59\uparrow$$

Check: $\begin{gathered}\Sigma R=105.0=15+20+50+20\end{gathered}$ ✓. (The large moments come from the settlements, which are comparable with the loads when expressed as $200/EI$. B sinks so far that its reaction becomes tension, i.e. the bearing is taken to be bilateral.)

*Bending moment values:* A hogging 108.67; B sagging 73.51; under the 20 kN load $\begin{gathered}M=M_{BC}+V_{BC}\times2=42.65\end{gathered}$ kN·m (sagging); C hogging 63.64; D hogging 30; E zero.


@s 5
**Moment distribution with a support settlement.** $EI=20\,000$ kN·m², settlement of A: $\delta=15$ mm $=0.015$ m. The joint B is held in place (BD is axially rigid and C is a hinge), so A moving down is the same as B moving up relative to A by $\delta$ in the member AB (chord rotation, clockwise end moments of the same sign at both ends).

*Fixed-end moments.*

$$M^F_{AB}=-\frac{PL}{8}+\frac{6EI\delta}{L^2}=-20+\frac{6(20000)(0.015)}{16}=-20+112.5=+92.5\ \text{kN·m}$$

$$M^F_{BA}=+\frac{PL}{8}+\frac{6EI\delta}{L^2}=+20+112.5=+132.5\ \text{kN·m}$$

$$\begin{gathered}M^F_{BC}=+\frac{wL^2}{12}=+7.5 \\ M^F_{CB}=-7.5\ \text{kN·m}\end{gathered}$$

*Stiffness and distribution factors at B* (C is hinged, so BC uses $3EI/L$):

$$\begin{gathered}K_{BA}=\frac{4EI}{4}=EI \\ K_{BC}=\frac{3EI}{3}=EI \\ K_{BD}=\frac{4EI}{4}=EI\ \Rightarrow\ DF=\tfrac13,\ \tfrac13,\ \tfrac13\end{gathered}$$

*Distribution table* (moments in kN·m):

| Member | AB | BA | BC | BD | CB | DB |
|---|---|---|---|---|---|---|
| DF | – | 0.333 | 0.333 | 0.333 | 1 (hinge) | – |
| FEM | +92.50 | +132.50 | +7.50 | 0 | −7.50 | 0 |
| Release hinge C | | | +3.75 | | +7.50 | |
| Balance B (unbalanced $-143.75$) | | −47.92 | −47.92 | −47.92 | | |
| Carry over | −23.96 | | | | 0 | −23.96 |
| **Final moments** | **+68.54** | **+84.58** | **−36.67** | **−47.92** | **0** | **−23.96** |

The check at joint B: $84.58-36.67-47.92=0$ ✓.

Slope-deflection check: $M_{BA}=132.5+EI\theta_B$, $M_{BC}=11.25+EI\theta_B$, $M_{BD}=EI\theta_B$; $\Sigma M_B=0$ gives $3EI\theta_B=-143.75$, so $\theta_B=-2.396\times10^{-3}$ rad, which agrees with the table.

$$\boxed{M_{AB}=68.54,\ M_{BA}=84.58,\ M_{BC}=-36.67,\ M_{BD}=-47.92,\ M_{DB}=-23.96,\ M_{CB}=0\ \text{kN·m}}$$

@s 6
**(a) Member stiffness matrices.** For a bar between nodes $i$ and $j$, with direction cosines $c,s$ of the line $i\to j$, the global matrix in the degrees of freedom $(u_i,v_i,u_j,v_j)$ is

$$\mathbf k=\frac{EA}{L}\begin{bmatrix}c^2&cs&-c^2&-cs\\cs&s^2&-cs&-s^2\\-c^2&-cs&c^2&cs\\-cs&-s^2&cs&s^2\end{bmatrix}$$

$\begin{gathered}EA=210\times10^{6}\times5\times10^{-4}=1.05\times10^{5}\end{gathered}$ kN.

*Bar 3-1:* $L=10$ m, $c=1$, $s=0$, $EA/L=10\,500$ kN/m (dofs $u_3,v_3,u_1,v_1$):

$$\mathbf k_{31}=10500\begin{bmatrix}1&0&-1&0\\0&0&0&0\\-1&0&1&0\\0&0&0&0\end{bmatrix}$$

*Bar 1-2:* $L=5$ m, direction $1\to2$ is up and to the left at $45^\circ$: $c=-0.7071$, $s=0.7071$, $EA/L=21\,000$ kN/m, so $\frac{EA}{L}c^2=10\,500$ (dofs $u_1,v_1,u_2,v_2$):

$$\mathbf k_{12}=10500\begin{bmatrix}1&-1&-1&1\\-1&1&1&-1\\-1&1&1&-1\\1&-1&-1&1\end{bmatrix}$$

*Spring 1-4:* vertical, $k=2000$ kN/m ($c=0$, $s=\pm1$; dofs $u_1,v_1,u_4,v_4$):

$$\mathbf k_{14}=2000\begin{bmatrix}0&0&0&0\\0&1&0&-1\\0&0&0&0\\0&-1&0&1\end{bmatrix}$$

**(b) Assembly and displacement of node 1.** Nodes 2, 3 and 4 are fixed, so only $u_1,v_1$ are free. Adding the terms that belong to the dofs $u_1,v_1$:

$$\begin{bmatrix}10500+10500&-10500\\-10500&10500+2000\end{bmatrix}\begin{Bmatrix}u_1\\v_1\end{Bmatrix}=\begin{Bmatrix}0\\-25\end{Bmatrix}\ \Rightarrow\ \begin{bmatrix}21000&-10500\\-10500&12500\end{bmatrix}\begin{Bmatrix}u_1\\v_1\end{Bmatrix}=\begin{Bmatrix}0\\-25\end{Bmatrix}$$

$\begin{gathered}\det=21000(12500)-10500^2=1.5225\times10^{8}\end{gathered}$, so

$$\begin{gathered}u_1=\frac{0\cdot12500-(-10500)(-25)}{1.5225\times10^{8}}=-1.724\times10^{-3}\ \text{m} \\ v_1=\frac{21000(-25)-0}{1.5225\times10^{8}}=-3.448\times10^{-3}\ \text{m}\end{gathered}$$

$$\boxed{u_1=-1.724\ \text{mm (to the left)},\quad v_1=-3.448\ \text{mm (downward)}}$$

The resultant displacement is $3.855$ mm.

*Member forces and reactions (check).*

$$F_{31}=\frac{EA}{L}u_1=-18.10\ \text{kN (compression)}$$

$$F_{12}=-\frac{EA}{L}(cu_1+sv_1)=+25.60\ \text{kN (tension)}$$

$$F_{spring}=2000\,v_1=-6.90\ \text{kN (compressed)}$$

Reactions: node 3: $R_x=+18.10$ kN; node 2: $R_x=-18.10$ kN, $R_y=+18.10$ kN; node 4: $R_y=+6.90$ kN. $\Sigma R_x=0$ ✓ and $\Sigma R_y=25$ kN ✓. (The 25 kN load was read as acting vertically downward at node 1.)

@s 7
**Influence line for the shear at D.** D is the mid-point of span AB. The beam A-B-C is continuous with two spans $L_1=8$ m and $L_2=6$ m, $EI$ constant, so for a unit load at a distance $x$ from A the hogging moment at B follows from the three-moment equation ($\begin{gathered}M_A=M_C=0\end{gathered}$):

$$2M_B(L_1+L_2)=-\left[\frac{6A_1\bar a_1}{L_1}+\frac{6A_2\bar b_2}{L_2}\right]$$

For the unit load in span AB ($a=x$, $b=8-x$) the bracket is $\dfrac{ab(L_1+a)}{L_1}$; in span BC ($a=x-8$, $b=14-x$) it is $\dfrac{ab(L_2+b)}{L_2}$. Then $M_B=-\dfrac{\text{bracket}}{28}$ and

$$V_A=\begin{cases}\dfrac{8-x}{8}+\dfrac{M_B}{8}&0\le x\le8\\[2mm]\dfrac{M_B}{8}&8\le x\le14\end{cases}\qquad V_D=\begin{cases}V_A-1&x<4\ \text{(load to the left of D)}\\V_A&x>4\ \text{(load to the right of D)}\end{cases}$$

*Ordinates at 2 m intervals:*

| $x$ (m) | bracket | $M_B$ | $V_A$ | **ordinate of $V_D$** |
|---|---|---|---|---|
| 0 | 0 | 0 | 1.0000 | **0** |
| 2 | 15.00 | −0.5357 | 0.6830 | **−0.3170** |
| 4 (just left of D) | 24.00 | −0.8571 | 0.3929 | **−0.6071** |
| 4 (just right of D) | 24.00 | −0.8571 | 0.3929 | **+0.3929** |
| 6 | 21.00 | −0.7500 | 0.1563 | **+0.1563** |
| 8 (support B) | 0 | 0 | 0 | **0** |
| 10 | 13.33 | −0.4762 | −0.0595 | **−0.0595** |
| 12 | 10.67 | −0.3810 | −0.0476 | **−0.0476** |
| 14 (support C) | 0 | 0 | 0 | **0** |

The influence line jumps by exactly $1.0$ at D (from $-0.607$ to $+0.393$) as it should for a shear influence line, passes through zero at B and C, and is small and negative over span BC.

```figure caption="Question 7: influence line for the shear force at D (ordinates at 2 m, straight lines drawn between the computed points; the real curve between the points is a cubic). The shear changes by 1.0 at D."
fig,ax=plt.subplots(figsize=(5.8,2.8))
xs1=[0,2,4]; ys1=[0,-0.3170,-0.6071]
xs2=[4,6,8,10,12,14]; ys2=[0.3929,0.1563,0,-0.0595,-0.0476,0]
ax.plot(xs1,ys1,"o-",color=ACCENT,lw=2); ax.plot(xs2,ys2,"o-",color=ACCENT,lw=2); ax.plot([4,4],[-0.6071,0.3929],color=ACCENT,lw=1.2,ls="--")
ax.axhline(0,color=INK,lw=1.5)
for x,y in zip(xs1+xs2,ys1+ys2): ax.text(x,y+(0.07 if y>=0 else -0.13),f"{y:+.3f}",ha="center",fontsize=7.5)
for x,t in ((0,"A"),(4,"D"),(8,"B"),(14,"C")): ax.text(x,-0.82,t,ha="center",fontsize=9,fontweight="bold")
ax.set_xlabel("position of unit load x (m)"); ax.set_ylabel("shear at D"); ax.set_ylim(-0.9,0.6); ax.set_xlim(-0.5,14.5)
```

@s 8
**Plastic collapse load factor 1.5.** Factored loads: horizontal $1.5\times20=30$ kN at B, vertical $1.5\times50=75$ kN at the mid-span of BC. $M_p$ is the same for all members. A column height difference exists: AB is 2 m and CD is 6 m, so the supports A and D are at different levels, and the columns rotate through different angles in sway.

*Critical sections (possible hinges):* A, B, E (under the 75 kN load), C and D: 5 sections. Degree of indeterminacy $=3$, so the number of independent mechanisms is $5-3=2$: the **beam** mechanism and the **sway** mechanism; their combination gives a third one.

**1. Beam mechanism** (hinges at B, E, C; E is at the middle, rotation $\theta,\ 2\theta,\ \theta$, E moves down $2\theta$):

$$M_p(\theta+2\theta+\theta)=75\times2\theta\ \Rightarrow\ M_p=\frac{150}{4}=37.5\ \text{kN·m}$$

**2. Sway mechanism** (hinges at A, B, C, D). The beam moves horizontally by $\Delta$; with $\Delta=6\theta$ the short column AB rotates $\Delta/2=3\theta$ and the long column CD rotates $\theta$:

$$M_p(3\theta+3\theta+\theta+\theta)=30\times6\theta\ \Rightarrow\ M_p=\frac{180}{8}=22.5\ \text{kN·m}$$

**3. Combined mechanism** (beam rotation $b=3\theta$ added to the sway rotation $3\theta$ at B: the two rotations at B are opposite, so the hinge at B disappears). Hinge rotations: A $=3\theta$, E $\begin{gathered}=2b=6\theta\end{gathered}$, C $\begin{gathered}=\theta+b=4\theta\end{gathered}$, D $=\theta$, total $14\theta$. External work: sway $30\times6\theta=180\theta$ plus the vertical load $\begin{gathered}75\times(2b)=75\times6\theta=450\theta\end{gathered}$:

$$M_p(3\theta+6\theta+4\theta+\theta)=180\theta+450\theta\ \Rightarrow\ M_p=\frac{630}{14}=45\ \text{kN·m}$$

The combined mechanism needs the greatest moment, so it governs (any trial mechanism gives a lower bound on the required $M_p$, and the true value is the largest). Mixing the mechanisms in other proportions gives $M_p=(180+150b)/(8+2b)$ for $b\le3\theta$ and $(180+150b)/(2+4b)$ for $b>3\theta$ (with $\theta=1$), which both peak at $b=3$.

**Static check (moment diagram).** With the support reactions $A_x=-15$ kN, $A_y=30$ kN, $D_x=-15$ kN, $D_y=45$ kN at collapse, the moments at the five sections are (with the sign chosen so that the hinge moments reach $M_p$):

| Section | A | B | E | C | D |
|---|---|---|---|---|---|
| $M$ (kN·m) | +45 | +15 | −45 | +45 | −45 |

so $|M|\le45=M_p$ everywhere and four hinges (A, E, C, D) form: the moment diagram is **safe and the mechanism is complete**, therefore the collapse load is correct.

$$\boxed{M_p=45\ \text{kN·m}}\quad\text{(for the factored loads; hinges at A, E, C and D)}$$

```figure caption="Question 8: bending moments at the critical sections at collapse (kN m); the plastic hinges at A, E, C and D are marked in red."
fig,ax=plt.subplots(figsize=(4.8,3.3)); ax.axis("off")
ax.plot([0,0],[4,6],color=INK,lw=2.4); ax.plot([0,4],[6,6],color=INK,lw=2.4); ax.plot([4,4],[0,6],color=INK,lw=2.4)
for p,t,dx,dy in (((0,4),"A  45",-1.2,-0.1),((0,6),"B  15",-1.2,0.2),((2,6),"E  45",-0.3,0.45),((4,6),"C  45",0.15,0.3),((4,0),"D  45",0.2,-0.2)):
    ax.plot(*p,"o",color="#d9534f" if "15" not in t else INK,ms=7 if "15" not in t else 4); ax.text(p[0]+dx,p[1]+dy,t,fontsize=8.5)
ax.set_xlim(-2,5.2); ax.set_ylim(-0.8,7)
```

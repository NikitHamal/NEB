---
file: NEBians-IOE-Past-Paper-Fluid-Mechanics-ENCE201-2082-Chaitra.pdf
subject: Fluid Mechanics
level: BE · Year II / Part I
code: ENCE 201
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define cavitation. Derive an expression of capillary fall when a small diameter tube is vertically submerged in the mercury. [[1+2]]

b) For the multi-fluid manometer system shown in the figure below, determine the unknown differential reading ($h$) in the central manometer. Assume the specific weight of air = 12 N/m³. [[6]]

```figure caption="Question 1(b): water tanks A and B (centres on the datum, 50 cm above the base). Left U-tube: mercury (S = 13.6), open to the atmosphere, left surface 20 cm above the right one and the right surface 10 cm above the base. Central inverted U-tube: air, differential reading h. Right side: mercury (left surface 20 cm above the base, right surface 20 cm higher), oil (S = 0.8) over the top and down to an open tube whose oil surface stands 25 cm above the datum."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.2,5.0)); ax.set_aspect("equal"); ax.axis("off")
def tube(p,c="white",lw=3.6,o=True):
    x=[a for a,b in p]; y=[b for a,b in p]
    if o: ax.plot(x,y,color=INK,lw=lw+2.0,solid_capstyle="butt",solid_joinstyle="round")
    ax.plot(x,y,color=c,lw=lw,solid_capstyle="butt",solid_joinstyle="round")
W="#bcd7ee"; HG="#8b929c"; OIL="#e3b25a"
tube([(0,50),(0,0),(4,0),(4,50),(7.5,50)],"white")
tube([(18.5,50),(20,50),(20,76),(24,76),(24,50),(25.5,50)],"white")
tube([(36.5,50),(38,50),(38,0),(42,0),(42,50),(45,50),(45,0),(48,0),(48,76)],"white")
tube([(4,10),(4,50),(7.5,50)],W,o=False); tube([(18.5,50),(20,50),(20,60)],W,o=False); tube([(25.5,50),(24,50),(24,72)],W,o=False)
tube([(36.5,50),(38,50),(38,20)],W,o=False)
tube([(0,30),(0,0),(4,0),(4,10)],HG,o=False); tube([(38,20),(38,0),(42,0),(42,40)],HG,o=False)
tube([(42,40),(42,50),(45,50),(45,0),(48,0),(48,75)],OIL,o=False)
for cx in (13,31):
    ax.add_patch(mp.Circle((cx,50),5.5,fc="#e4eef8",ec=INK,lw=1.2))
ax.text(13,50,"A",ha="center",va="center",fontsize=9); ax.text(31,50,"B",ha="center",va="center",fontsize=9)
ax.text(13,45,"water",ha="center",fontsize=7.5); ax.text(31,45,"water",ha="center",fontsize=7.5)
ax.plot([-3,52],[50,50],color=MUTED,lw=0.8,ls="--"); ax.plot([-3,52],[0,0],color=MUTED,lw=0.8,ls="--")
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(22,60),xytext=(22,72),arrowprops=ar); ax.text(22.7,64.5,"h",fontsize=9)
ax.text(21.5,79,"air",ha="center",fontsize=8)
ax.annotate("",xy=(-3,0),xytext=(-3,50),arrowprops=ar); ax.text(-3.6,25,"50 cm",rotation=90,ha="right",va="center",fontsize=7.5)
ax.text(1.4,18,"mercury\nS = 13.6",fontsize=7.2,ha="center"); ax.text(-1.2,40,"20 cm\nbetween\nsurfaces",fontsize=6.9,ha="right",va="center")
ax.text(5.2,5,"10 cm",fontsize=7.2)
ax.text(36.2,11,"mercury\nS = 13.6",fontsize=7.2,ha="right"); ax.text(49.3,35,"oil\nS = 0.8",fontsize=7.2)
ax.text(49.3,64,"25 cm\nabove datum",fontsize=7.2)
ax.text(43.5,-6,"oil",fontsize=7.2,ha="center"); ax.text(39.5,-6,"Hg",fontsize=7.2,ha="center"); ax.text(1.8,-6,"Hg",fontsize=7.2,ha="center")
ax.set_xlim(-12,60); ax.set_ylim(-9,84)
```

@q 2
a) A solid object composed of a rectangular base (0.3 m × 0.3 m × 0.1 m) and a cylinder on top (height = 0.3 m and diameter = 0.1 m), as shown below, having a density of 900 kg/m³, is floating in water. Is it in stable equilibrium or not? Justify. [[6]]

```figure caption="Question 2(a): square base 0.3 m × 0.3 m × 0.1 m carrying a cylinder of diameter 0.1 m and height 0.3 m (side view; the object is the same material throughout, 900 kg/m³)."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.6,3.0)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),0.3,0.1,fc="#dbe7f5",ec=INK,lw=1.3)); ax.add_patch(mp.Rectangle((0.1,0.1),0.1,0.3,fc="#cfdcec",ec=INK,lw=1.3))
ar=dict(arrowstyle="<->",color=MUTED,lw=0.8)
ax.annotate("",xy=(0,-0.05),xytext=(0.3,-0.05),arrowprops=ar); ax.text(0.15,-0.1,"0.3 m",ha="center",fontsize=8)
ax.annotate("",xy=(0.1,0.45),xytext=(0.2,0.45),arrowprops=ar); ax.text(0.15,0.47,"0.1 m",ha="center",fontsize=8)
ax.annotate("",xy=(0.26,0.1),xytext=(0.26,0.4),arrowprops=ar); ax.text(0.275,0.25,"0.3 m",fontsize=8,va="center")
ax.annotate("",xy=(-0.04,0),xytext=(-0.04,0.1),arrowprops=ar); ax.text(-0.05,0.05,"0.1 m",fontsize=8,va="center",ha="right")
ax.set_xlim(-0.2,0.5); ax.set_ylim(-0.15,0.55)
```

b) A curved surface ABCDE divides a closed pressurised tank and an open tank as shown in the figure below. If the width of the tank is 10 m, calculate the horizontal and vertical components of force on the curved surface ABCDE. Calculate also the location of those components. [[6+2]]

```figure caption="Question 2(b): closed tank (S = 1, gauge reading 98.1 kN/m² at the bottom) on the left and open tank (S = 2.5) on the right; AB C is a semicircle of radius 1 m bulging into the open tank and CDE a semicircle of radius 2 m bulging into the closed tank. Levels (depth below the top): A 2 m, C 4 m, D 6 m (= free surface of the open tank), E 8 m, bottom 10 m."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(5.4,3.6)); ax.set_aspect("equal"); ax.axis("off")
Y=lambda d:10-d
t=_np.linspace(-_np.pi/2,_np.pi/2,60)
ab=[(_np.cos(a)*1,Y(3)+_np.sin(a)*1) for a in t][::-1]
t2=_np.linspace(_np.pi/2,3*_np.pi/2,80)
cd=[(_np.cos(a)*2,Y(6)+_np.sin(a)*2) for a in t2]
wall=[(0,Y(0)),(0,Y(2))]+ab+cd+[(0,Y(8)),(0,Y(10))]
ax.add_patch(mp.Polygon([(-8,0),(-8,10)]+[(0,10)]+wall[1:]+[(0,0)],closed=True,fc="#dbe7f5",ec="none"))
ax.add_patch(mp.Polygon([(6,0),(6,Y(6))]+[(p[0],p[1]) for p in cd if p[1]<=Y(6)+1e-9]+[(0,0)],closed=True,fc="#b6c4d6",ec="none"))
ax.plot([p[0] for p in wall],[p[1] for p in wall],color=INK,lw=2.2)
ax.plot([-8,-8,0],[10,0,0],color=INK,lw=1.4); ax.plot([0,6],[0,0],color=INK,lw=1.4)
ax.plot([-8,0],[10,10],color=INK,lw=1.4)
ax.plot([0,6],[Y(6)]*2,color=INK,lw=0.8,ls="--")
for d,l,dx in ((2,"A",0.15),(3,"B",0.25),(4,"C",0.2),(6,"D",-0.5),(8,"E",0.2)):
    px={2:0,3:1,4:0,6:-2,8:0}[d]; ax.text(px+dx,Y(d)+0.15,l,fontsize=9,fontweight="bold")
ax.text(-4,5,"closed tank\nS = 1",ha="center",fontsize=8.5); ax.text(3.2,2.4,"open tank\nS = 2.5",ha="center",fontsize=8.5)
ax.text(-8.2,0.6,"98.1 kPa",ha="right",fontsize=7.5); ax.plot([-8.9,-8],[0.5,0.5],color=INK,lw=1)
ax.text(2.5,Y(6)+0.35,"air (open)",fontsize=7.5,color=MUTED)
ax.set_xlim(-11,6.5); ax.set_ylim(-0.5,10.6)
```

@q 3
a) Define pathlines and streaklines. In a two-dimensional incompressible flow, the fluid velocity components are given by $u = x - 4y$ and $v = -y - 4x$. Do velocity potential and stream function exist? If yes, determine their equations. [[2+4]]

b) Water at 20°C is conveyed from a reservoir through a two-stage piping system as illustrated in the figure. The initial, smaller pipe section has a diameter of 10 cm, which expands to a larger pipe section with a diameter of 20 cm. Considering head loss in the flow, through section 1-2 is given as $h_{L1-2}=\dfrac{2V_1^2}{2g}$, through section 2-3 as $h_{L2-3}=\dfrac{3V_2^2}{2g}$ and through section 3-4 as $h_{L3-4}=\dfrac{2V_2^2}{2g}$, where $V_1$ and $V_2$ are the average fluid velocities in their respective sections. Given a local atmospheric pressure of $p_{atm}=101{,}323$ Pa and a water saturation (vapour) pressure of $p_v=2{,}338$ Pa, determine the following: [[2+2+2]]

i) The flow rate (Q) in the pipe.

ii) Pressure at points 2 and 3 in the pipe.

iii) Whether cavitation occurs or not in the pipe system? Justify.

```figure caption="Question 3(b): reservoir with the water surface 5 m above the datum (4 m above the pipe axis; the pipe axis is 1 m above the tank bottom); 10 cm pipe to point 2 (2 m above the datum) where the pipe enlarges to 20 cm; summit 3 at 7 m; discharge to the atmosphere at point 4 on the datum."
import numpy as _np
fig,ax=plt.subplots(figsize=(5.8,3.2)); ax.set_aspect("equal"); ax.axis("off")
ax.fill([-4,0,0,-4],[0,0,5,5],color="#cfe3f5",ec=INK,lw=1.2); ax.plot([-4,5],[0,0],color=MUTED,lw=0.8,ls="--")
ax.plot([-4.0,0],[5,5],color=INK,lw=1.2); ax.text(-3.9,5.15,"1",fontsize=9)
ax.plot([0,1.5],[1,1],color=INK,lw=3.0,solid_capstyle="butt")
ax.plot([1.5,2.3],[1,2],color=INK,lw=3.0,solid_capstyle="butt")
ax.plot([2.3,6.2,10.8],[2,7,0],color="#5b6472",lw=7,solid_joinstyle="round")
ax.plot([2.3,6.2,10.8],[2,7,0],color="#d8e6f3",lw=5,solid_joinstyle="round")
ax.text(2.0,2.35,"2",fontsize=9); ax.text(6.0,7.3,"3",fontsize=9); ax.text(10.9,0.1,"4",fontsize=9)
ax.text(0.2,0.45,"10 cm",fontsize=7.5); ax.text(5.5,3.4,"20 cm",fontsize=7.5,rotation=60)
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(-4.4,0),xytext=(-4.4,5),arrowprops=ar); ax.text(-4.6,2.5,"5 m",ha="right",va="center",fontsize=8)
ax.annotate("",xy=(8.9,0),xytext=(8.9,7),arrowprops=ar); ax.text(9.1,5.6,"7 m",fontsize=8)
ax.annotate("",xy=(3.1,0),xytext=(3.1,2),arrowprops=ar); ax.text(3.3,0.7,"2 m",fontsize=8)
ax.set_xlim(-7,12.5); ax.set_ylim(-0.7,8)
```

@q 4
a) Define hydraulic coefficients. Derive an expression for the discharge in the case of partially and fully submerged orifices. [[1+3]]

b) Consider the steady flow of water in a fluid mixing box with two inlets (1 and 2) and one outlet (3), as shown in the figure. The total weight of the water and the mixing box is 4000 N. The pipes have diameters of $D_1 = 0.4$ m, $D_2 = 0.3$ m, and $D_3 = 0.5$ m. At inlet 1, water enters with a volume flow rate of $Q_1 = 0.8$ m³/s and a gage pressure of $p_1 = 10$ kPa. At outlet 3, the mixture discharges to the atmosphere with a volume flow rate of $Q_3 = 1.2$ m³/s. Determine the following: [[1]] [[3+3]]

i) The velocity of flow required at inlet 2.

ii) The reaction forces $R_x$ and $R_y$ required to hold the box stationary.

```figure caption="Question 4(b): mixing box. Inlet 1 (p₁ = 10 kPa, Q₁ = 0.8 m³/s) enters at θ₁ = 60° to the horizontal (flowing down and to the right); inlet 2 (p₂ = 15 kPa) enters horizontally from the right (flowing left); outlet 3 (Q₃ = 1.2 m³/s) leaves at θ₃ = 45° (down and to the left). Rₓ acts to the right, Rᵧ upwards (positive)."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(4.8,3.4)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),4,4,fc="#c9d3df",ec=INK,lw=1.3))
a=dict(arrowstyle="-|>",color=INK,lw=1.5)
c,s=_np.cos,_np.sin; d=_np.radians
ax.annotate("",xy=(0.8,4.0),xytext=(0.8-1.6*c(d(60)),4+1.6*s(d(60))),arrowprops=a)
ax.text(-1.4,5.6,"1:  p₁ = 10 kPa\nQ₁ = 0.8 m³/s",fontsize=7.8)
ax.annotate("",xy=(4,2.2),xytext=(5.8,2.2),arrowprops=a); ax.text(4.4,2.45,"2:  p₂ = 15 kPa",fontsize=7.8)
ax.annotate("",xy=(0.6-1.7*c(d(45)),-1.7*s(d(45))),xytext=(0.6,0),arrowprops=a); ax.text(-2.5,-1.9,"3:  Q₃ = 1.2 m³/s",fontsize=7.8)
ax.annotate("",xy=(0,2.0),xytext=(-1.5,2.0),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)); ax.text(-2.2,2.15,"Rₓ",fontsize=9,color="#d9534f")
ax.annotate("",xy=(3.0,0),xytext=(3.0,-1.4),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.5)); ax.text(3.2,-1.2,"Rᵧ",fontsize=9,color="#d9534f")
ax.text(2,2.0,"W = 4000 N",ha="center",fontsize=8)
ax.set_xlim(-3.4,6.6); ax.set_ylim(-2.4,6.6)
```

@q 5
a) Explain various similarities in physical modeling. Using the Froude model law, derive the scale relationships for discharge and power between a model and its prototype in hydraulic similitude. [[2+2]]

b) The resisting torque $T$ against the motion of a shaft in a lubricated bearing depends on the viscosity $\mu$, the rotational speed $N$, the diameter $D$ and the bearing pressure intensity $p$. Show that $T=\mu ND^{3}\,\phi\!\left(\dfrac{p}{\mu N}\right)$. [[4]]

c) Derive an expression of displacement thickness. A smooth flat plate 35 m long and 10 m wide moves in sea water with a speed of 1.5 m/s in the direction of length. The density and viscosity of sea water are 1050 kg/m³ and 0.001 Pa·s. Find out the drag force on the bottom of the plate. [[2+4]]

**OR**

Define drag and lift coefficients with equations. Discuss the variation of drag force on a smooth circular cylinder placed in a uniform flow with respect to the Reynolds number. Explain the changes in flow separation, wake formation, and drag coefficient for different ranges of Reynolds number. [[2+4]]

<!-- SOLUTIONS -->

@s 1
**(a) Cavitation.** Cavitation is the formation of vapour bubbles in a flowing liquid wherever the local absolute pressure falls to the vapour pressure of the liquid at that temperature (for example at a pipe summit, a pump inlet or a high-velocity throat). The bubbles are swept into regions of higher pressure where they collapse suddenly, producing noise, vibration, pitting of the boundary and loss of efficiency.

**Capillary fall in mercury.** Mercury does not wet glass: the angle of contact $\theta$ is obtuse (about $130^\circ$ to $140^\circ$), the meniscus is convex upward and the mercury level *inside* a tube of diameter $d$ stands *below* the outside level by a depth $h$.

Consider the mercury column of height $h$ in the tube (below the outside level). The vertical forces on it are:

- the surface-tension force along the circumference, $F_\sigma=\sigma\,(\pi d)\cos\theta$ with $\cos\theta<0$, acting downward on the mercury, magnitude $\sigma\pi d\cos(180^\circ-\theta)$;
- the weight of the displaced column that is missing, i.e. the excess hydrostatic pressure force $\rho g h\,\dfrac{\pi d^{2}}{4}$ acting on the cross-section at the outside level.

For equilibrium the two are equal:

$$\sigma\,\pi d\,\cos(180^\circ-\theta)=\rho g h\,\frac{\pi d^{2}}{4}\ \Rightarrow\ \boxed{h=\frac{4\sigma\cos(180^\circ-\theta)}{\rho g d}=-\frac{4\sigma\cos\theta}{\rho g d}}$$

The capillary depression is inversely proportional to the diameter. Example: $d=2$ mm, $\sigma=0.48$ N/m, $\theta=140^\circ$, $\rho=13\,600$ kg/m³ gives

$$\begin{gathered}h=\dfrac{4(0.48)(0.766)}{13600(9.81)(0.002)}=5.5\ \text{mm}\end{gathered}$$

**(b) Multi-fluid manometer.** Work in gauge pressures and in units of $\gamma_w$ (so a column of a fluid of specific gravity $S$ and height $z$ contributes $S\,z$). Heights are measured from the base line; both tank centres A and B are on the datum at 50 cm.

*Left U-tube (finds $p_A$).* The right mercury surface is 10 cm above the base, the left one is 20 cm higher (30 cm) and is open to the atmosphere ($p=0$).

$$\begin{gathered}\dfrac{p_A}{\gamma_w}=0+13.6(0.20)-1(0.50-0.10)\\ \dfrac{p_A}{\gamma_w}=2.72-0.40=2.32\ \text{m of water}\end{gathered}$$

(from the left mercury surface down 20 cm in mercury to the right surface, then up through water from 10 cm to the datum at 50 cm).

*Right manometer (finds $p_B$).* The open oil tube has its surface 25 cm above the datum, i.e. at 75 cm. The oil is continuous over the top of the inverted U down to the right mercury surface at 40 cm, so the pressure there is $0.8(0.75-0.40)=0.28\,\gamma_w$. The left mercury surface is at 20 cm:

$$\begin{gathered}\dfrac{p_B}{\gamma_w}=0.80(0.75-0.40)+13.6(0.40-0.20)-1(0.50-0.20)\\ \dfrac{p_B}{\gamma_w}=0.28+2.72-0.30=2.70\ \text{m of water}\end{gathered}$$

*Central air manometer.* Let the water surface in the limb connected to A be at height $z$ above the datum; the surface in the limb of B is higher by $h$ (the air column is the gap). Pressure in the air at the left surface: $p_A-\gamma_w z$. At the right surface it is lower by the weight of the air column: $p_B-\gamma_w(z+h)=(p_A-\gamma_w z)-\gamma_a h$. Hence

$$p_B-p_A=(\gamma_w-\gamma_a)\,h\ \Rightarrow\ h=\frac{p_B-p_A}{\gamma_w-\gamma_a}=\frac{(2.70-2.32)(9810)}{9810-12}=\frac{3727.8}{9798}$$

$$\boxed{h=0.3805\ \text{m}\approx 38.0\ \text{cm}}$$

(Neglecting the air, $h=0.38$ m; the 12 N/m³ changes the answer by only 0.1 %.)

@s 2
**(a) Stability of the floating composite body.** Take the base of the block as the reference level, $z$ upward.

*Volumes and centre of gravity.*

$$\begin{gathered}V_b=0.3(0.3)(0.1)=9.000\times10^{-3}\ \text{m}^3\ (z_b=0.05\ \text{m})\\ V_c=\tfrac{\pi}{4}(0.1)^2(0.3)=2.356\times10^{-3}\ \text{m}^3\ (z_c=0.25\ \text{m})\\ V=11.356\times10^{-3}\ \text{m}^3\end{gathered}$$

$$z_G=\frac{9.000(0.05)+2.356(0.25)}{11.356}=\boxed{0.0915\ \text{m}}$$

*Draught.* $\rho=900$ kg/m³ so $V_{sub}=0.9V=10.220\times10^{-3}$ m³. The base alone gives 9.000×10⁻³, so the water line cuts the cylinder; the submerged part of the cylinder is $1.220\times10^{-3}$ m³, i.e. a depth

$$\begin{gathered}d_c=\frac{1.220\times10^{-3}}{\pi(0.1)^2/4}=0.1554\ \text{m} \\ \text{draught}=0.1+0.1554=0.2554\ \text{m}.\end{gathered}$$

*Centre of buoyancy.*

$$z_B=\frac{9.000(0.05)+1.220(0.1+0.0777)}{10.220}=0.0653\ \text{m}$$

*Metacentric height.* The water-line section is the **circle of diameter 0.1 m** (the cylinder cuts the surface), so the second moment of the water-line area is small:

$$\begin{gathered}I=\frac{\pi d^4}{64}=\frac{\pi(0.1)^4}{64}=4.909\times10^{-6}\ \text{m}^4 \\ BM=\frac{I}{V_{sub}}=\frac{4.909\times10^{-6}}{10.220\times10^{-3}}=0.00048\ \text{m}\end{gathered}$$

$$GM=z_B+BM-z_G=0.0653+0.0005-0.0915=\boxed{-0.0258\ \text{m}}$$

$GM<0$ (the metacentre M lies *below* the centre of gravity G, at 0.0658 m against 0.0915 m), so the **body is in unstable equilibrium** in the upright position: a small tilt produces an overturning couple and the body will heel over (it will float stably only lying on its side). The tall, heavy cylinder raises G while the thin water-line section gives almost no restoring moment.

```figure caption="Question 2(a) solution: upright position. Water line at 0.2554 m above the base of the block; G = 0.0915 m, B = 0.0653 m, M = 0.0658 m (below G): GM = −0.0258 m, unstable."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.7,3.2)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((-0.3,-0.12),0.9,0.25,fc="#b8d6ee",ec="none",alpha=0.7))
ax.add_patch(mp.Rectangle((0,0),0.3,0.1,fc="#dbe7f5",ec=INK,lw=1.3)); ax.add_patch(mp.Rectangle((0.1,0.1),0.1,0.3,fc="#cfdcec",ec=INK,lw=1.3))
ax.plot([-0.3,0.6],[0.2554,0.2554],color="#1d6fb8",lw=1.3)
for z,l,c in ((0.0915,"G","#d9534f"),(0.0653,"B","#2e8b57"),(0.0658,"M","#6a5acd")):
    off={"G":0.012,"B":-0.02,"M":0.0}[l]
    ax.plot([0.15],[z],"o",color=c,ms=4.5)
ax.text(0.23,0.093,"G",fontsize=9,color="#d9534f",va="bottom"); ax.text(0.23,0.045,"B",fontsize=9,color="#2e8b57",va="top"); ax.text(0.04,0.075,"M",fontsize=9,color="#6a5acd",ha="right",va="center")
ax.text(-0.28,0.27,"water line",fontsize=8,color="#1d6fb8")
ax.set_xlim(-0.35,0.65); ax.set_ylim(-0.12,0.45)
```

**(b) Curved surface ABCDE.** Width $w=10$ m, $\gamma_w=9.81$ kN/m³; $\gamma_1=9.81$ and $\gamma_2=2.5(9.81)=24.525$ kN/m³. Depths are measured downward from the top of the closed tank: A 2 m, C 4 m, D 6 m, E 8 m, tank bottom 10 m. The gauge at the bottom reads 98.1 kN/m², so the pressure at depth $h$ in the closed tank is $98.1-9.81(10-h)=9.81\,h$ kN/m², i.e. **zero gauge pressure at the top level** (the tank behaves as if open at the top). In the open tank the liquid surface is at D (depth 6 m); above it is air at zero gauge pressure.

*Horizontal component.* It equals the force on the vertical projection (depth 2 m to 8 m), taken separately for each side.

- Left liquid (S = 1), pushing to the right:

$$F_{H1}=\gamma_1 w\,\frac{8^2-2^2}{2}=9.81(10)(30)=2943\ \text{kN}\rightarrow$$

Its line of action is at the centroid of the triangular-trapezoidal pressure diagram: $\bar h=\dfrac{(8^3-2^3)/3}{(8^2-2^2)/2}=5.60$ m below the top.

- Right liquid (S = 2.5), depth 6 m to 8 m (projection 2 m), pushing to the left:

$$F_{H2}=\gamma_2 w\,\frac{2^2}{2}=24.525(10)(2)=490.5\ \text{kN}\leftarrow$$

It acts at two-thirds of the 2 m height below the surface of the open tank, i.e. at $6+\tfrac23(2)=7.333$ m depth.

$$\boxed{F_H=2943-490.5=2452.5\ \text{kN}\ \text{(to the right, i.e. towards the open tank)}}$$

Location (moments about the top level): $\bar y=\dfrac{2943(5.60)-490.5(7.333)}{2452.5}=\boxed{5.25\ \text{m below the top}}$ (that is 4.75 m above the tank bottom).

*Vertical component* (weights of the real or imaginary liquid above the surface, per 10 m width).

- Arc ABC (semicircle, $r=1$ m, the closed-tank liquid is inside the bulge, air outside): the upper half is pushed up by the liquid column above it, the lower half is pushed down by a larger column; net downward = weight of the half-disc of liquid:

$$\begin{gathered}F_{V,ABC}=\gamma_1\,w\,\frac{\pi(1)^2}{2}=9.81(10)(1.571)=154.1\ \text{kN}\downarrow \\ \bar x=\frac{4r}{3\pi}=0.424\ \text{m to the right of the line AE}\end{gathered}$$

- Arc CDE ($r=2$ m, closed-tank liquid on the outside, S = 2.5 liquid and air inside). From the left liquid the net force is upward and equal to the weight of the half-disc of S = 1 liquid between the two quarter arcs:

$$F_{V,CDE}^{(1)}=\gamma_1 w\frac{\pi(2)^2}{2}=9.81(10)(6.283)=616.4\ \text{kN}\uparrow$$

It acts at $\bar x=4r/3\pi=0.849$ m to the left of AE.

From the S = 2.5 liquid inside the lower quarter circle (D to E) acting downward:

$$F_{V,CDE}^{(2)}=\gamma_2 w\frac{\pi(2)^2}{4}=24.525(10)(3.142)=770.5\ \text{kN}\downarrow$$

Its line of action (centroid of the quarter disc) is also 0.849 m to the left of AE.

so the net on CDE is $616.4-770.5=154.1$ kN downward at 0.849 m left of AE.

$$\boxed{F_V=154.1+154.1=308.2\ \text{kN downward}}$$

*Location.* Taking moments about the vertical line AE (right positive):

$$\bar x=\frac{154.1(+0.424)+154.1(-0.849)}{308.2}=\boxed{0.212\ \text{m to the left of the wall line AE}}$$

*Resultant.*

$$\begin{gathered}R=\sqrt{2452.5^2+308.2^2}=2471.8\ \text{kN} \\ \theta=\tan^{-1}\frac{308.2}{2452.5}=7.16^\circ\ \text{below the horizontal (towards the open tank)}\end{gathered}$$


@s 3
**(a) Pathline and streakline.** A *pathline* is the actual trace of the route followed by one individual fluid particle over a period of time (what a long-exposure photograph of a single marked particle shows); it is the Lagrangian history $x=x(x_0,t)$. A *streakline* is the instantaneous locus of all particles that have passed through one fixed point (for example the filament of dye released continuously from a nozzle). In **steady flow** streamlines, pathlines and streaklines coincide.

*Existence of $\psi$ and $\phi$.* Given $u=x-4y$ and $v=-y-4x$:

- **Continuity (stream function exists if the flow is possible and incompressible):** $\dfrac{\partial u}{\partial x}+\dfrac{\partial v}{\partial y}=1+(-1)=0$ ✓. So a **stream function exists**.
- **Irrotationality (velocity potential exists if the vorticity is zero):** $\omega_z=\tfrac12\left(\dfrac{\partial v}{\partial x}-\dfrac{\partial u}{\partial y}\right)=\tfrac12\big(-4-(-4)\big)=0$ ✓. So a **velocity potential exists** (the flow is irrotational).

*Velocity potential* (convention $u=-\partial\phi/\partial x$, $v=-\partial\phi/\partial y$):

$$\begin{gathered}\frac{\partial\phi}{\partial x}=-(x-4y)\ \Rightarrow\ \phi=-\frac{x^2}{2}+4xy+f(y)\\ \frac{\partial\phi}{\partial y}=4x+f'(y)=-v=y+4x\ \Rightarrow\ f'(y)=y,\ f=\frac{y^2}{2}\end{gathered}$$

$$\begin{gathered}\boxed{\phi=-\frac{x^2}{2}+4xy+\frac{y^2}{2}} \\ (+\text{ constant})\end{gathered}$$

*Stream function* (convention $u=\partial\psi/\partial y$, $v=-\partial\psi/\partial x$):

$$\begin{gathered}\frac{\partial\psi}{\partial y}=x-4y\ \Rightarrow\ \psi=xy-2y^2+g(x)\\ -\frac{\partial\psi}{\partial x}=-y-g'(x)=-y-4x\ \Rightarrow\ g'(x)=4x,\ g=2x^2\end{gathered}$$

$$\begin{gathered}\boxed{\psi=2x^2+xy-2y^2} \\ (+\text{ constant})\end{gathered}$$

Check: $\nabla^2\phi=-1+1=0$ and $\nabla^2\psi=4-4=0$ ✓. (With the other common sign convention $u=+\partial\phi/\partial x$ the potential is $\phi=\frac{x^2}{2}-4xy-\frac{y^2}{2}$ and $\psi=-2x^2-xy+2y^2$.)

**(b) Two-stage piping system.** Water at 20 °C: take $\rho=998$ kg/m³, $\gamma=\rho g=9.79$ kN/m³. Datum through point 4 (the outlet). Reservoir surface (point 1): $z_1=1+4=5$ m, $p_1=0$ gauge, $V\approx0$. Outlet 4: $z_4=0$, $p_4=0$ gauge, velocity $V_2$ (the 20 cm pipe).

Continuity: $V_1A_1=V_2A_2\Rightarrow V_1=V_2\left(\dfrac{20}{10}\right)^2=4V_2$, so $V_1^2=16V_2^2$ (the velocity head in the small pipe is 16 times that in the large pipe).

**(i) Flow rate.** Energy equation from 1 to 4:

$$5=\frac{V_2^2}{2g}+\frac{2V_1^2+3V_2^2+2V_2^2}{2g}=\frac{V_2^2}{2g}\big(1+32+3+2\big)=38\,\frac{V_2^2}{2g}$$

$$\begin{gathered}\frac{V_2^2}{2g}=\frac{5}{38}=0.1316\ \text{m}\ \Rightarrow\ V_2=1.607\ \text{m/s},\ V_1=6.427\ \text{m/s}\\ Q=\frac{\pi}{4}(0.2)^2(1.607)=\boxed{0.0505\ \text{m}^3/\text{s}\ (50.5\ \text{L/s})}\end{gathered}$$

**(ii) Pressures.** Point 2 is taken at the start of the 20 cm pipe ($z_2=2$ m, velocity $V_2$; the loss $h_{L1-2}$ includes the enlargement). Energy from 1 to 2:

$$5=2+\frac{p_2}{\gamma}+\frac{V_2^2}{2g}+\frac{2V_1^2}{2g}\ \Rightarrow\ \frac{p_2}{\gamma}=3-33(0.1316)=-1.342\ \text{m}$$

$$\boxed{p_2=-1.342(9.79)=-13.1\ \text{kPa (gauge)}\ =88.2\ \text{kPa abs}}$$

Point 3 (summit, $z_3=7$ m, velocity $V_2$, losses $h_{L1-2}+h_{L2-3}$ equal 35 velocity heads of the 20 cm pipe, since $2V_1^2=32V_2^2$ and $3V_2^2$):

$$5=7+\frac{p_3}{\gamma}+\frac{V_2^2}{2g}+35\frac{V_2^2}{2g}\ \Rightarrow\ \frac{p_3}{\gamma}=-2-36(0.1316)=-6.737\ \text{m}$$

$$\begin{gathered}\boxed{p_3=-6.737(9.79)=-66.0\ \text{kPa (gauge)}} \\ p_{3,abs}=101.323-65.96=35.4\ \text{kPa}\end{gathered}$$

**(iii) Cavitation.** The lowest pressure in the system occurs at the summit, point 3: $p_{3,abs}=35.4$ kPa, which is well above the vapour pressure $p_v=2.338$ kPa. Because $p_{min}>p_v$ (the margin is 33 kPa, about 3.4 m of water), **cavitation does not occur**; the siphon works.

@s 4
**(a) Hydraulic coefficients.** For flow through an orifice of area $a$ under head $H$:

- *Coefficient of contraction* $C_c=\dfrac{a_c}{a}$ (area of the vena contracta over the area of the orifice; about 0.61–0.64).
- *Coefficient of velocity* $C_v=\dfrac{V_{actual}}{V_{theoretical}}=\dfrac{V}{\sqrt{2gH}}$ (about 0.97–0.99).
- *Coefficient of discharge* $C_d=\dfrac{Q_{actual}}{Q_{theoretical}}=C_cC_v$ (about 0.60–0.62).
- *Coefficient of resistance* $C_r=\dfrac{\text{head lost}}{H}=\dfrac{1}{C_v^2}-1$ in terms of velocity head.

**Fully submerged orifice** (both faces under liquid; upstream level above downstream level by $H$, rectangular orifice of width $b$, top edge at depth $H_1$ and bottom edge at depth $H_2$ below the upstream surface). Consider a strip of height $dh$ at depth $h$ below the upstream surface. The pressure head upstream is $h$ and downstream $h-H$, so the effective head across *every* strip is $H$ and the velocity is $\sqrt{2gH}$:

$$dQ=C_d\,b\,dh\sqrt{2gH}\ \Rightarrow\ \boxed{Q=C_d\,b\,(H_2-H_1)\sqrt{2gH}}$$

**Partially submerged orifice** (the downstream level lies between the top and the bottom edge; downstream surface at depth $H$ below the upstream surface, $H_1<H<H_2$). The upper part $(H_1\to H)$ discharges freely into the air, the lower part $(H\to H_2)$ discharges submerged:

$$Q_1=\int_{H_1}^{H}C_{d1}\,b\sqrt{2gh}\,dh=\tfrac23C_{d1}\,b\sqrt{2g}\left(H^{3/2}-H_1^{3/2}\right)$$

$$Q_2=C_{d2}\,b\,(H_2-H)\sqrt{2gH}$$

$$\boxed{Q=Q_1+Q_2=\tfrac23C_{d1}\,b\sqrt{2g}\left(H^{3/2}-H_1^{3/2}\right)+C_{d2}\,b\,(H_2-H)\sqrt{2gH}}$$

(With $C_{d1}=C_{d2}=C_d$ if only one value is known.)

```figure caption="Question 4(a): partially submerged rectangular orifice. H₁ and H₂ are the depths of the top and bottom edges below the upstream surface; the downstream surface is a distance H below the upstream one. The upper part flows freely, the lower part flows submerged."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.2,2.7)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),4,5,fc="#cfe3f5",ec="none")); ax.add_patch(mp.Rectangle((4.4,0),4,3.4,fc="#cfe3f5",ec="none"))
ax.plot([0,4,4,4.4,4.4,8.4],[5,5,0,0,0,0],color="none")
ax.add_patch(mp.Rectangle((4,0),0.4,6,fc="#8b929c",ec=INK,lw=1.2)); ax.add_patch(mp.Rectangle((4,1.1),0.4,2.3,fc="white",ec=INK,lw=1.0)) 
ax.plot([-0.4,4],[5,5],color=INK,lw=1.2); ax.plot([4.4,8.8],[3.4,3.4],color=INK,lw=1.2)
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(-0.6,5),xytext=(-0.6,3.4),arrowprops=ar); ax.text(-0.8,4.2,"H₁",ha="right",va="center",fontsize=9)
ax.annotate("",xy=(9.3,5),xytext=(9.3,3.4),arrowprops=ar); ax.text(9.5,4.2,"H",va="center",fontsize=9)
ax.annotate("",xy=(-1.6,5),xytext=(-1.6,1.1),arrowprops=ar); ax.text(-1.8,3.0,"H₂",ha="right",va="center",fontsize=9)
ax.annotate("",xy=(7.4,3.4),xytext=(4.4,3.4),arrowprops=dict(arrowstyle="-|>",color="#1d6fb8",lw=1.4))
ax.annotate("",xy=(7.4,2.0),xytext=(4.4,2.0),arrowprops=dict(arrowstyle="-|>",color="#1d6fb8",lw=1.4))
ax.text(6.0,3.55,"free part",fontsize=7.8); ax.text(5.9,1.3,"submerged part",fontsize=7.8)
ax.text(2,-0.9,"upstream",ha="center",fontsize=8); ax.text(6.4,-0.9,"downstream",ha="center",fontsize=8)
ax.set_xlim(-3.3,10.3); ax.set_ylim(-1.3,6.3)
```

**(b) Mixing box.** $$\begin{gathered}A_1=\tfrac{\pi}{4}(0.4)^2=0.12566\ \text{m}^2,\quad A_2=\tfrac{\pi}{4}(0.3)^2=0.07069\ \text{m}^2\\ A_3=\tfrac{\pi}{4}(0.5)^2=0.19635\ \text{m}^2,\quad \rho=1000\ \text{kg/m}^3\end{gathered}$$

**(i) Velocity at inlet 2.** Continuity $Q_1+Q_2=Q_3$:

$$\begin{gathered}Q_2=1.2-0.8=0.4\ \text{m}^3/\text{s} \\ V_2=\frac{Q_2}{A_2}=\frac{0.4}{0.07069}=\boxed{5.66\ \text{m/s}}\end{gathered}$$

$$\begin{gathered}V_1=\dfrac{0.8}{0.12566}=6.366\ \text{m/s}\\ V_3=\dfrac{1.2}{0.19635}=6.112\ \text{m/s}\end{gathered}$$

**(ii) Reactions.** Control volume = the box with the water in it. Directions (see the figure): velocity at 1 is $V_1(\cos60^\circ,-\sin60^\circ)$, at 2 it is $V_2(-1,0)$, at 3 it is $V_3(-\cos45^\circ,-\sin45^\circ)$. Pressure forces act *into* the control volume at the inlets, in the direction of the incoming flow; the exit is at atmospheric pressure (gauge 0):

$$\begin{gathered}p_1A_1=10(0.12566)=1.2566\ \text{kN} \\ p_2A_2=15(0.07069)=1.0603\ \text{kN}\end{gathered}$$

Momentum equation $\sum\vec F=\sum\dot m_{out}\vec V_{out}-\sum\dot m_{in}\vec V_{in}$ ($\dot m_i=\rho Q_i$):

$$x:\ R_x+p_1A_1\cos60^\circ-p_2A_2=\rho\big[Q_3(-V_3\cos45^\circ)-Q_1V_1\cos60^\circ-Q_2(-V_2)\big]$$

$$R_x+628.3-1060.3=1000\big[-5.186-2.546+2.264\big]=-5469\ \text{N}\ \Rightarrow\ \boxed{R_x=-5037\ \text{N}\approx-5.04\ \text{kN}}$$

$$y:\ R_y-p_1A_1\sin60^\circ-W=\rho\big[Q_3(-V_3\sin45^\circ)-Q_1(-V_1\sin60^\circ)\big]$$

$$R_y-1088.3-4000=1000\big[-5.186+4.410\big]=-776\ \text{N}\ \Rightarrow\ \boxed{R_y=+4312\ \text{N}\approx4.31\ \text{kN}}$$

The negative sign means $R_x$ actually acts to the **left** (5.04 kN), $R_y$ acts **upward** (4.31 kN). Resultant support force $=\sqrt{5.04^2+4.31^2}=6.63$ kN, directed at $40.6^\circ$ above the negative $x$ axis (up and to the left).

@s 5
**(a) Similarities (physical modelling).** A model is dynamically similar to its prototype when three conditions hold:

1. **Geometric similarity:** the ratio of every corresponding length is the same, $L_r=L_p/L_m$ (hence equal angles, and area ratio $L_r^2$, volume ratio $L_r^3$).
2. **Kinematic similarity:** velocities (and accelerations) at corresponding points have the same direction and a constant ratio, $V_r=V_p/V_m$; the flow patterns (streamlines) are geometrically similar.
3. **Dynamic similarity:** the ratio of corresponding forces (inertia, gravity, viscous, pressure, surface tension, elastic) at corresponding points is constant; in practice the relevant dimensionless number (Reynolds, Froude, Weber, Mach) is equal in model and prototype.

**Froude model law.** For free-surface flows (spillways, weirs, open channels) gravity governs, so $Fr=\dfrac{V}{\sqrt{gL}}$ is the same:

$$\begin{gathered}\left(\frac{V}{\sqrt{gL}}\right)_m=\left(\frac{V}{\sqrt{gL}}\right)_p\\ V_r=\sqrt{g_rL_r}=L_r^{1/2}\quad(g_r=1)\end{gathered}$$

*Discharge.* $Q=VA$, so

$$\begin{gathered}\boxed{Q_r=V_rL_r^2=L_r^{5/2}} \\ \text{i.e.}\ Q_p=Q_mL_r^{5/2}\end{gathered}$$

*Power.* $P=F\,V$, and the force ratio from dynamic similarity is $F_r=\rho_rL_r^2V_r^2=\rho_rL_r^3$ (the same fluid, $\rho_r=1$). Therefore

$$\begin{gathered}\boxed{P_r=F_rV_r=\rho_rL_r^{3}\,L_r^{1/2}=\rho_rL_r^{7/2}\;\to\;L_r^{7/2}} \\ \text{i.e.}\ P_p=P_mL_r^{7/2}\end{gathered}$$

**(b) Buckingham $\pi$-theorem.** Variables: $T,\mu,N,D,p$, so $n=5$. Dimensions in M, L, T: $T=ML^2T^{-2}$, $\mu=ML^{-1}T^{-1}$, $N=T^{-1}$, $D=L$, $p=ML^{-1}T^{-2}$; the number of fundamental dimensions is $m=3$, so there are $n-m=2$ dimensionless groups. Choose the repeating variables $\mu,N,D$ (they contain M, T and L between them).

$$\begin{gathered}\pi_1=T\,\mu^{a}N^{b}D^{c}\ \Rightarrow\ M^{1+a}L^{2-a+c}T^{-2-a-b}=M^0L^0T^0\\ a=-1,\ b=-1,\ c=-3\ \Rightarrow\ \pi_1=\frac{T}{\mu ND^3}\end{gathered}$$

$$\begin{gathered}\pi_2=p\,\mu^{a}N^{b}D^{c}\ \Rightarrow\ M^{1+a}L^{-1-a+c}T^{-2-a-b}=1\\ a=-1,\ b=-1,\ c=0\ \Rightarrow\ \pi_2=\frac{p}{\mu N}\end{gathered}$$

Since $\pi_1=\phi(\pi_2)$:

$$\boxed{T=\mu ND^{3}\,\phi\!\left(\frac{p}{\mu N}\right)}$$

**(c) Displacement thickness.** The boundary layer slows the fluid, so the streamlines outside it are displaced away from the plate. The mass flow deficit across the layer, $\int_0^\delta\rho(U-u)\,dy$ (per unit width), equals the flow that would pass through a layer of the free-stream velocity $U$ and thickness $\delta^*$:

$$\rho U\delta^*=\int_0^\delta\rho\,(U-u)\,dy\ \Rightarrow\ \boxed{\delta^*=\int_0^\delta\left(1-\frac{u}{U}\right)dy}$$

$\delta^*$ is the distance by which the external streamlines are shifted outward. For the Blasius laminar layer $\delta^*=1.72\,x/\sqrt{Re_x}$, and for a $1/7$-power turbulent profile $\delta^*=\delta/8$.

*Drag on the plate.* $L=35$ m, $b=10$ m, $U=1.5$ m/s, $\rho=1050$ kg/m³, $\mu=0.001$ Pa·s, $A=35\times10=350$ m² (the bottom face).

$$Re_L=\frac{\rho UL}{\mu}=\frac{1050(1.5)(35)}{0.001}=5.51\times10^{7}\gg5\times10^5$$

so the layer is turbulent over almost the whole length. For a smooth plate with $10^{6}<Re<10^{9}$ the Prandtl–Schlichting formula gives

$$C_D=\frac{0.455}{(\log_{10}Re)^{2.58}}=\frac{0.455}{(7.7414)^{2.58}}=0.002317$$

$$F_D=C_D\,\tfrac12\rho U^2A=0.002317\,(0.5)(1050)(1.5)^2(350)=\boxed{958\ \text{N}\approx0.96\ \text{kN}}$$

(Checks: $0.074/Re^{0.2}$ gives 866 N but is valid only for $Re<10^7$; allowing for the short laminar start with the $1700/Re$ correction gives 853 N; the standard answer is of order 0.9 kN.)

**OR: Drag and lift; cylinder in a uniform stream.** Drag $F_D$ is the component of the total fluid force on a body *parallel* to the approach velocity $U$, and lift $F_L$ the component *perpendicular* to it:

$$\begin{gathered}F_D=C_D\,\tfrac12\rho U^2A \\ F_L=C_L\,\tfrac12\rho U^2A\ \ \Rightarrow\ C_D=\frac{F_D}{\tfrac12\rho U^2A},\quad C_L=\frac{F_L}{\tfrac12\rho U^2A}\end{gathered}$$

($A$ = projected area normal to the stream, $=dL$ for a cylinder). Total drag is the sum of **friction (skin) drag** from the wall shear and **pressure (form) drag** from the unbalanced pressure on the front and wake faces.

With $Re=\dfrac{\rho Ud}{\mu}$ the flow around a smooth cylinder changes as follows:

| Reynolds number | Flow and wake | $C_D$ |
|---|---|---|
| $Re<1$ | Creeping flow, no separation, streamlines symmetric before and after; drag is almost all viscous | very large ($\approx 10$ at $Re=1$), falling like $1/Re$ |
| $4\lesssim Re\lesssim40$ | Boundary layer separates near the rear; a steady pair of attached vortices forms in the wake | about 4 to 1.5 |
| $40\lesssim Re\lesssim 200$ | The wake becomes unstable and sheds alternate vortices, the Kármán vortex street (Strouhal number about 0.2); oscillating lift | about 1.5 to 1.3 |
| $200\lesssim Re\lesssim 2\times10^{5}$ (subcritical) | Laminar boundary layer separates at about $80^\circ$ from the stagnation point; a wide turbulent wake; pressure drag dominates | nearly constant, about 1.0 to 1.2 |
| $2\times10^5\lesssim Re\lesssim 5\times10^5$ (critical, *drag crisis*) | The boundary layer turns turbulent before separation, sticks longer (separation at about $120^\circ$), the wake narrows sharply | falls suddenly to about 0.3 |
| $Re>5\times10^5$ (supercritical to post-critical) | Turbulent separation, narrow wake, the separation point moves slowly forward again | rises slowly to about 0.6–0.7 |

```figure caption="Question 5 (OR): drag coefficient of a smooth circular cylinder against Reynolds number (schematic curve of the standard experimental results)."
import numpy as _np
fig,ax=plt.subplots(figsize=(5.2,3.0))
Re=_np.array([0.1,0.3,1,3,10,30,100,300,1e3,3e3,1e4,1e5,2e5,3e5,4e5,6e5,1e6,3e6,1e7])
Cd=_np.array([60,25,10,5.5,3.0,1.9,1.4,1.3,1.0,1.0,1.2,1.2,1.2,0.6,0.35,0.4,0.5,0.6,0.7])
ax.loglog(Re,Cd,color=ACCENT,lw=2)
for x0 in (40,200,2e5,5e5): ax.axvline(x0,color=GRID,lw=0.9)
ax.set_xlabel("Reynolds number $Re=\\rho U d/\\mu$",fontsize=8); ax.set_ylabel("$C_D$",fontsize=8)
ax.text(0.15,0.5,"creeping",fontsize=7.5); ax.text(3,0.22,"steady\nvortex pair",fontsize=7.5); ax.text(35,0.22,"vortex\nstreet",fontsize=7.5); ax.text(2e3,2.3,"laminar separation,\n$C_D\\approx1.2$",fontsize=7.5)
ax.text(3.5e5,0.17,"drag\ncrisis",fontsize=7.5); ax.text(1.5e6,0.95,"turbulent\nseparation",fontsize=7.5)
ax.set_ylim(0.1,100); ax.set_xlim(0.1,2e7); ax.tick_params(labelsize=7.5)
```

*Summary.* $C_D$ falls steadily with $Re$ while the flow is attached (viscous drag), levels off near 1.2 when a laminar layer separates at $80^\circ$ and a broad wake forms (pressure drag), drops abruptly near $Re\approx3\times10^5$ when a turbulent layer delays separation and narrows the wake, and then recovers slightly. Hence the drag force ($\propto C_DU^2$) grows with $U$ almost as $U^2$, except for the sudden drop at the drag crisis.

---
file: NEBians-IOE-Past-Paper-Fluid-Mechanics-ENCE201-2081-Chaitra.pdf
subject: Fluid Mechanics
level: BE · Year II / Part I
code: ENCE 201
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course), BE Civil, Year II / Part I. Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) What do you mean by capillarity? Obtain the expression for capillary rise of a liquid in a glass tube. [[3]]

b) Define the term poise and stokes with their dimensions. What is cavitation? [[3]]

c) Determine the magnitude and direction of the resultant hydrostatic force on curve surface ABCDEFGHI. [[6]]

```figure caption="Question 1(c): curved surface ABCDEFGHI (depths below the free surface of the left liquid, which is also the level of A): A 0, B 2 m, D 6 m, E 8 m (= free surface of the right liquid at I), F and H 10 m, G 12 m. BCD is a semicircle of radius 2 m (centre on the line AB produced, at 4 m) bulging to the right, DEF a semicircle of radius 2 m bulging to the left (centre 8 m), FGH a semicircle of radius 2 m (centre 10 m, 2 m right of AB) holding liquid of S = 1; the left liquid has S = 2 and the right liquid S = 3. The right-hand side of ABCDEF is air."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(5.2,4.6)); ax.set_aspect("equal"); ax.axis("off")
def arc(cx,cy,a0,a1,n=60,R=2):
    t=_np.radians(_np.linspace(a0,a1,n)); return [(cx+R*_np.cos(a),cy+R*_np.sin(a)) for a in t]
bcd=arc(0,-4,90,-90); def_=arc(0,-8,90,270); fgh=arc(2,-10,180,360)
wallL=[(0,0),(0,-2)]+bcd+def_+fgh[:31]
ax.add_patch(mp.Polygon([(-5,0)]+wallL+[(2,-13),(-5,-13)],closed=True,fc="#cfdcec",ec="none"))
ax.add_patch(mp.Polygon(fgh[30:]+[(4,-8),(7,-8),(7,-13),(2,-13)],closed=True,fc="#a9bdd3",ec="none"))
ax.add_patch(mp.Polygon(fgh,closed=True,fc="#e7eef6",ec="none"))
w=[(0,0),(0,-2)]+bcd+def_+fgh+[(4,-8)]
ax.plot([p[0] for p in w],[p[1] for p in w],color=INK,lw=2.2)
ax.plot([-5,0],[0,0],color=INK,lw=1.0,ls="--"); ax.plot([4,7],[-8,-8],color=INK,lw=1.0,ls="--"); ax.plot([2,4],[-10,-10],color=MUTED,lw=0.8,ls="--")
ax.plot([2,2],[-10,-13.4],color=INK,lw=0.8); ax.plot([-5,7],[-13,-13],color=INK,lw=1.2)
for l,p,o in (("A",(0,0),(-0.5,0.15)),("B",(0,-2),(-0.5,-0.2)),("C",(2,-4),(0.15,0.0)),("D",(0,-6),(-0.5,-0.1)),("E",(-2,-8),(-0.6,-0.1)),("F",(0,-10),(-0.5,0.15)),("G",(2,-12),(-0.5,-0.7)),("H",(4,-10),(0.1,0.1)),("I",(4,-8),(0.1,0.15))):
    ax.text(p[0]+o[0],p[1]+o[1],l,fontsize=9,fontweight="bold")
ax.text(-3.0,-3.5,"S = 2",fontsize=9,ha="center"); ax.text(5.2,-11.3,"S = 3",fontsize=9,ha="center"); ax.text(2,-10.9,"S = 1",fontsize=8.5,ha="center")
ax.text(3.2,-4.5,"air",fontsize=8,color=MUTED)
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
for y0,y1,l in ((0,-2,"2 m"),(-2,-6,"4 m"),(-6,-8,"2 m"),(-8,-10,"2 m"),(-10,-12,"2 m")):
    ax.annotate("",xy=(7.4,y0),xytext=(7.4,y1),arrowprops=ar); ax.text(7.6,(y0+y1)/2,l,va="center",fontsize=8)
ax.set_xlim(-5.5,9.2); ax.set_ylim(-13.8,1.0)
```

@q 2
a) A pump having efficiency 80% draws water from reservoir A and lifts it to reservoir B with the help of 100 mm diameter pipe as shown in the figure below. The loss of head in the pipe from A to 1 is two times the velocity head, from 2 to 3 is 5 times the velocity head and from 3 to B is 3 times the velocity head. Determine the following: [[3+3]]

(i) Discharge delivered by the pump.

(ii) Power delivered by the pump in kW.

```figure caption="Question 2(a): reservoir A (water surface 12 m above the pump), pump between 1 and 2, pipe D = 100 mm rising to point 3 where the gauge reads −29.43 kPa (4 m above the water surface of reservoir B), then down to tank B whose water surface is 20 m above the pump level."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(6.0,5.4)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,12-1.6),3,1.6,fc="#cfe3f5",ec=INK,lw=1.2)); ax.plot([0,0,3,3],[13.4,10.4,10.4,13.4],color=INK,lw=1.2)
ax.plot([1.5,1.5,5,5,9.5,9.5,12.5],[10.4,0,0,26,26,22,22],color=INK,lw=3.0,solid_joinstyle="round")
ax.add_patch(mp.Rectangle((12.5,19.5),4,2.5,fc="#cfe3f5",ec=INK,lw=1.2)); ax.plot([12.5,12.5,16.5,16.5],[24,19.5,19.5,24],color=INK,lw=1.2)
ax.add_patch(mp.Circle((3.6,0),0.8,fc="white",ec=INK,lw=1.3)); ax.text(3.6,-1.9,"pump",ha="center",fontsize=8); ax.text(2.7,0.8,"1",fontsize=8); ax.text(4.4,0.8,"2",fontsize=8)
ax.text(9.0,23.5,"3",fontsize=9); ax.text(10.0,24.2,"−29.43 kPa",fontsize=7.8)
ax.plot([-1,3.5],[12,12],color=MUTED,lw=0.8,ls="--"); ax.plot([-1,17],[0,0],color=MUTED,lw=0.8,ls="--")
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(-0.6,0),xytext=(-0.6,12),arrowprops=ar); ax.text(-0.9,6,"12 m",ha="right",va="center",fontsize=8)
ax.annotate("",xy=(17.6,0),xytext=(17.6,22),arrowprops=ar); ax.text(17.8,11,"20 m",va="center",fontsize=8)
ax.annotate("",xy=(11.3,22),xytext=(11.3,26),arrowprops=ar); ax.text(11.5,23.5,"4 m",fontsize=8)
ax.text(1.5,12.3,"A",fontsize=9,ha="center"); ax.text(14.5,22.3,"B",fontsize=9,ha="center"); ax.text(5.4,13,"D = 100 mm",fontsize=7.8)
ax.set_xlim(-4.5,20.5); ax.set_ylim(-3,28)
```

b) An open circular cylinder of 60 cm diameter and 1 m long is rotated with an angular velocity $\omega$. The water surface profile in the rotating cylinder is as shown in the figure below. Determine the angular velocity ($\omega$) of the cylinder if the gauge pressure at point 1 is found to be 4.9 kPa. [[6]]

```figure caption="Question 2(b): open cylinder, diameter 0.6 m, height 1 m, rotating; the free surface (a paraboloid) just reaches the rim at point 2; point 1 is on the bottom at a radius of 0.2 m."
import numpy as _np
fig,ax=plt.subplots(figsize=(3.6,3.3)); ax.set_aspect("equal"); ax.axis("off")
ax.plot([-0.3,-0.3,0.3,0.3],[1,0,0,1],color=INK,lw=2)
r=_np.linspace(-0.3,0.3,80); z=0.1+196.2*r**2/19.62
ax.fill_between(r,0,z,color="#cfe3f5"); ax.plot(r,z,color=ACCENT,lw=1.4)
ax.plot([0,0],[0,1.05],color=MUTED,lw=0.8,ls="-.")
ax.plot([0.2],[0],"o",color="#d9534f",ms=4); ax.text(0.205,0.04,"1",fontsize=8.5,color="#d9534f"); ax.text(-0.34,1.0,"2",fontsize=9,ha="right")
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(0,-0.08),xytext=(0.2,-0.08),arrowprops=ar); ax.text(0.1,-0.17,"0.2 m",ha="center",fontsize=7.8)
ax.annotate("",xy=(-0.3,-0.3),xytext=(0.3,-0.3),arrowprops=ar); ax.text(0,-0.4,"0.6 m",ha="center",fontsize=7.8)
ax.annotate("",xy=(0.38,0),xytext=(0.38,1),arrowprops=ar); ax.text(0.41,0.5,"1 m",va="center",fontsize=8)
ax.set_xlim(-0.55,0.6); ax.set_ylim(-0.5,1.15)
```

@q 3
a) Two tanks with orifices A and B in the same vertical plane are placed on the same level and it is desired to adjust the distance between them so that the jets intersect in the plane of bases. Calculate the distance $x$ if the depth of water in each tank is 40 cm. Is the point equidistant from the two tanks? What happens if the orifices A and B are located differently? [[4+1+1]]

```figure caption="Question 3(a): two tanks (water depth 40 cm each); orifice A is 10 cm below the surface of its tank and orifice B is 30 cm below the surface of its tank. The jets meet at P on the base plane, a distance x apart."
import matplotlib.patches as mp, numpy as _np
fig,ax=plt.subplots(figsize=(5.4,2.7)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),30,40,fc="#cfe3f5",ec=INK,lw=1.2)); ax.add_patch(mp.Rectangle((100,0),30,40,fc="#cfe3f5",ec=INK,lw=1.2))
ax.plot([-5,135],[0,0],color=INK,lw=1.5)
t=_np.linspace(0,1,40); xa=30+34.64*t; ya=30-30*t**2
ax.plot(xa,ya,color=ACCENT,lw=1.5); ax.plot(100-34.64*t,10-10*t**2,color=ACCENT,lw=1.5)
ax.plot([30],[30],"o",color=INK,ms=3.5); ax.plot([100],[10],"o",color=INK,ms=3.5)
ax.text(24,32,"A",fontsize=9,ha="right"); ax.text(106,12,"B",fontsize=9)
ax.text(64.6,-7,"P",fontsize=9,ha="center")
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(30,-14),xytext=(100,-14),arrowprops=ar); ax.text(65,-24,"x = ?",ha="center",fontsize=8.5)
ax.annotate("",xy=(-3,40),xytext=(-3,30),arrowprops=ar); ax.text(-6,35,"10 cm",ha="right",va="center",fontsize=7.8)
ax.annotate("",xy=(133,40),xytext=(133,10),arrowprops=ar); ax.text(136,25,"30 cm",va="center",fontsize=7.8)
ax.set_xlim(-30,160); ax.set_ylim(-30,46)
```

**OR**

Determine the rate of flow of water through a pipe of 400 mm diameter placed in an inclined position where a venturimeter is inserted, having a throat diameter of 250 mm. The difference of pressure between the main and throat is measured by a liquid of sp. gravity 0.7 in an inverted U-tube which gives a reading of 260 mm. The loss of head between the main and throat is 0.4 times the kinetic head of the pipe. [[6]]

b) Water and oil flow in horizontal pipelines. A double U-tube manometer is connected between the pipelines as shown in figure below. Calculate the pressure difference between the pipes. [[6]]

```figure caption="Question 3(b): water in pipe 1 (left), alcohol (S₂ = 0.9) in pipe 5 (right). Interface 2 is 20 cm below the axis of pipe 1 (water above, S₁ = 1.6 liquid below); the S₁ liquid rises to interface 3, 2 cm above the pipe axis; air fills the gap up to the alcohol interface 4, which is 13 cm above the axis level of pipe 5; the alcohol runs down to pipe 5."
import matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(5.6,5.0)); ax.set_aspect("equal"); ax.axis("off")
def tube(p,c="white",lw=3.4,o=True):
    x=[a for a,b in p]; y=[b for a,b in p]
    if o: ax.plot(x,y,color=INK,lw=lw+2.0,solid_capstyle="butt",solid_joinstyle="round")
    ax.plot(x,y,color=c,lw=lw,solid_capstyle="butt",solid_joinstyle="round")
W="#bcd7ee"; L="#8b929c"; AL="#e3b25a"
tube([(2,22),(5,22),(5,0),(10,0),(10,24),(10,35.6),(18,35.6),(18,22),(21,22)],"white")
tube([(2,22),(5,22),(5,2)],W,o=False); tube([(5,2),(5,0),(10,0),(10,24)],L,o=False); tube([(18,35.6),(18,22),(21,22)],AL,o=False)
ax.add_patch(mp.Circle((-1,22),3.2,fc="#d4e6f6",ec=INK,lw=1.2)); ax.add_patch(mp.Circle((24,22),3.2,fc="#f2dcae",ec=INK,lw=1.2))
ax.text(-1,22,"1",ha="center",va="center",fontsize=8); ax.text(24,22,"5",ha="center",va="center",fontsize=8)
ax.text(-1,26,"water",ha="center",fontsize=7.8); ax.text(24,27.0,"alcohol\nS₂ = 0.9",ha="left",fontsize=7.8)
ax.text(3.0,2.4,"2",fontsize=8,ha="right"); ax.text(11,24.0,"3",fontsize=8); ax.text(18.8,35.8,"4",fontsize=8)
ax.text(7.5,-3.5,"S₁ = 1.6",ha="center",fontsize=7.8); ax.text(12.5,30,"air",fontsize=7.8)
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(3.4,22),xytext=(3.4,2),arrowprops=ar); ax.text(3.0,12,"20 cm",ha="right",va="center",fontsize=7.8)
ax.annotate("",xy=(19.5,35.6),xytext=(19.5,22),arrowprops=ar); ax.text(19.9,29,"13 cm",va="center",fontsize=7.8)
ax.plot([-3,26],[22,22],color=MUTED,lw=0.6,ls="--")
ax.set_xlim(-8,34); ax.set_ylim(-6,40)
```

@q 4
a) Define the Lagrangian and Eulerian methods in fluid kinematics. Derive an expression for continuity equation in the Cartesian coordinate system. [[2+4]]

b) A 0.4 m diameter 90° vertical bend carries 0.5 m³/s oil of specific gravity 0.85 with a pressure of 118 kN/m² at inlet to the bend. The volume of the bend is 0.1 m³. Find the magnitude and direction of the force on the bend. Neglect friction and assume both inlet and outlet sections to be at same horizontal level. Also assume that water enters the bend at 45° to the horizontal. [[6]]

@q 5
a) Describe with neat sketch the formation of boundary layer in the flat plate with zero pressure gradient. What are pressure drag, friction drag and lift forces? [[3+3]]

b) Prove that the form of equation for discharge $Q$ through a sharp-edge triangular notch assuming $Q$ depends on the central angle $\theta$, head $H$, acceleration due to gravity $g$, density of fluid $\rho$, viscosity of fluid $\mu$ and surface tension of fluid $\sigma$ is $Q=CH^{5/2}$ where $C=g^{1/2}\,\phi\left[\left(\dfrac{\mu}{\rho g^{1/2}H^{3/2}}\right),\left(\dfrac{\sigma}{\rho gH^2}\right),\theta\right]$ using Buckingham-$\pi$ method. [[6]]

<!-- SOLUTIONS -->

@s 1
**(a) Capillarity.** Capillarity is the rise or fall of a liquid in a tube of small bore (or between close plates) relative to the surrounding free surface, caused by the combined action of cohesion between liquid molecules and adhesion between the liquid and the wall. A liquid that wets the wall (water on glass, $\theta<90^\circ$) rises; a non-wetting liquid (mercury, $\theta>90^\circ$) is depressed.

*Capillary rise in a glass tube of diameter $d$.* The liquid column of height $h$ is held up by the vertical component of the surface-tension force acting round the circumference of the meniscus (angle of contact $\theta$):

$$\text{upward pull}=\sigma\cos\theta\,(\pi d)$$

Its weight is $\rho g\,h\,\dfrac{\pi d^2}{4}$. At equilibrium:

$$\sigma\pi d\cos\theta=\rho g\,h\,\frac{\pi d^2}{4}\ \Rightarrow\ \boxed{h=\frac{4\sigma\cos\theta}{\rho g d}}$$

For clean water in glass $\theta\approx0^\circ$: $h=\dfrac{4(0.0728)}{998(9.81)d}=\dfrac{0.0298\ \text{m·mm}}{d}$, e.g. $h=14.9$ mm for $d=2$ mm. The rise is inversely proportional to the tube diameter.

**(b) Poise and stokes.**

- **Poise** is the CGS unit of *dynamic viscosity* $\mu$: the viscosity of a fluid that requires a shear force of 1 dyne per cm² to maintain a velocity gradient of 1 cm/s per cm. $1\ \text{poise}=1\ \text{dyne·s/cm}^2=1\ \text{g/(cm·s)}=0.1\ \text{Pa·s}$; dimensions $[ML^{-1}T^{-1}]$.
- **Stokes** is the CGS unit of *kinematic viscosity* $\nu=\mu/\rho$: $1\ \text{stoke}=1\ \text{cm}^2/\text{s}=10^{-4}\ \text{m}^2/\text{s}$; dimensions $[L^2T^{-1}]$.

**Cavitation.** The formation of vapour cavities in a flowing liquid where the local absolute pressure falls to the vapour pressure; the bubbles collapse violently when carried into higher pressure, causing noise, vibration, pitting erosion and loss of efficiency in pumps, turbines and spillways.

**(c) Resultant force on ABCDEFGHI** (per metre width of the surface; the width is not given). Depth $y$ is measured down from the free surface of the left liquid (level of A) with $\gamma=9.81$ kN/m³. Each fluid has its own pressure distribution: S = 2 on the left (free surface at $y=0$), S = 3 on the right (free surface at $y=8$, level of I), S = 1 inside the cup FGH (free surface at $y=10$); the region right of ABCDEF is air. The surface is divided into AB, BCD, DEF, FG, GH, HI and the forces are found fluid by fluid.

*Horizontal components* (force on the vertical projection):

| Fluid | Projection (depth) | Force (kN/m) | Direction | Depth of action |
|---|---|---|---|---|
| S = 2 (AB, BCD, DEF, FG) | 0 to 12 m | $2\gamma\dfrac{12^2}{2}=1412.6$ | → right | $\frac23(12)=8.00$ m |
| S = 3 (GH, HI) | 8 to 12 m | $3\gamma\dfrac{4^2}{2}=235.4$ | ← left | $8+\frac23(4)=10.67$ m |
| S = 1 (inside FG and GH) | 10 to 12 m | $\gamma\dfrac{2^2}{2}=19.6$ on FG ← and 19.6 on GH → | cancel | — |

$$\begin{gathered}\boxed{F_H=1412.6-235.4=1177.2\ \text{kN/m}\ (\text{to the right})} \\ \bar y_H=\frac{1412.6(8.00)-235.4(10.67)}{1177.2}=7.47\ \text{m below A}\end{gathered}$$

*Vertical components* (weight of the real or imaginary liquid above each part of the surface):

- BCD and DEF (S = 2, two semicircles of radius 2 m, area $\pi r^2/2=6.283$ m²): the force on BCD is $2\gamma(6.283)=123.3$ kN **down** (centroid 0.849 m to the right of AB) and the force on DEF is $123.3$ kN **up** (0.849 m to the left of AB): they cancel as forces and leave only a couple.
- FG (S = 2, outside, force up): the column above FG up to the free surface at $y=0$ has the area $2(10)+\pi=23.14$ m² (rectangle 2×10 plus the quarter disc), so $F=2\gamma(23.14)=454.0$ kN **up**, at $\bar x=1.02$ m from AB.
- GH (S = 3, outside, force up): the column above GH up to $y=8$ is the 2×2 rectangle plus the quarter disc, area $4+\pi=7.142$ m²; $F=3\gamma(7.142)=210.2$ kN **up**, at $\bar x=2.93$ m.
- FGH inside (S = 1, force down): the half disc of radius 2 m (area 6.283 m²) between the arc and the level F–H: $F=\gamma(6.283)=61.6$ kN **down**, at $\bar x=2.00$ m.

$$\boxed{F_V=454.0+210.2-61.6=602.6\ \text{kN/m upward}}$$

Moments about the line AB (right positive, up forces): $454.0(1.02)+210.2(2.93)-61.6(2.00)-123.3(0.849)+123.3(-0.849)=747.3$ kN·m/m, so

$$\bar x_V=\frac{747.3}{602.6}=1.24\ \text{m to the right of AB}$$

*Resultant.*

$$\begin{gathered}R=\sqrt{1177.2^2+602.6^2}=\boxed{1322.5\ \text{kN per metre width}} \\ \theta=\tan^{-1}\frac{602.6}{1177.2}=\boxed{27.1^\circ\ \text{above the horizontal, pointing to the right and up}}\end{gathered}$$

The line of action passes through the point on line AB produced which is 8.10 m below A (obtained from the total moment about A, 9537 kN·m/m, divided by $F_H$ with the vertical-force moment included). The numbers were confirmed by numerical integration of the pressure over the whole boundary.

@s 2
**(a) Pump between two reservoirs.** Datum at the pump level; velocity head $\dfrac{V^2}{2g}$ in the 100 mm pipe; reservoir surfaces A at $z=12$ m and B at $z=20$ m; the gauge at point 3 reads $p_3=-29.43$ kPa, $\dfrac{p_3}{\gamma}=-3.0$ m, and point 3 is 4 m above the surface of B, $z_3=24$ m.

**(i) Discharge.** Apply the energy equation from 3 to B (no pump, both free surfaces at rest, loss $3\dfrac{V^2}{2g}$):

$$\frac{p_3}{\gamma}+\frac{V^2}{2g}+z_3=z_B+3\frac{V^2}{2g}\ \Rightarrow\ -3+\frac{V^2}{2g}+24=20+3\frac{V^2}{2g}\ \Rightarrow\ \frac{V^2}{2g}=0.5\ \text{m}$$

$$\begin{gathered}V=\sqrt{2(9.81)(0.5)}=3.132\ \text{m/s}\\ Q=\frac{\pi}{4}(0.1)^2(3.132)=\boxed{0.0246\ \text{m}^3/\text{s}\ (24.6\ \text{L/s})}\end{gathered}$$

**(ii) Power.** Energy equation from A to 3 with the pump head $h_p$; total losses $(2+5)=7$ velocity heads:

$$12+h_p=\frac{p_3}{\gamma}+\frac{V^2}{2g}+z_3+7\frac{V^2}{2g}=-3+24+8(0.5)=25\ \Rightarrow\ h_p=13\ \text{m}$$

$$\begin{gathered}P_{\text{water}}=\gamma Qh_p=9.81(0.0246)(13)=\boxed{3.14\ \text{kW}}\ \text{(power delivered by the pump to the water)}\\ P_{\text{input}}=\frac{P_{\text{water}}}{\eta}=\frac{3.14}{0.8}=\boxed{3.92\ \text{kW}}\ \text{(shaft power required)}\end{gathered}$$

**(b) Rotating open cylinder.** The free surface of a liquid rotating at $\omega$ is a paraboloid, $z_s=z_0+\dfrac{\omega^2r^2}{2g}$, with the vertex at $r=0$ at height $z_0$ above the bottom. From the figure, the surface passes through the rim (point 2: $r=0.3$ m, $z=1$ m), so

$$z_0=1-\frac{\omega^2(0.3)^2}{2g}$$

The pressure at point 1 (bottom, $r=0.2$ m, $z=0$) is hydrostatic below the surface at that radius:

$$\frac{p_1}{\gamma}=z_s(0.2)=z_0+\frac{\omega^2(0.2)^2}{2g}=1-\frac{\omega^2}{2g}\left(0.09-0.04\right)=1-\frac{0.05\,\omega^2}{2g}$$

With $p_1=4.9$ kPa, $\dfrac{p_1}{\gamma}=\dfrac{4900}{9810}=0.4995$ m:

$$\omega^2=\frac{(1-0.4995)(2)(9.81)}{0.05}=196.4\ \Rightarrow\ \boxed{\omega=14.0\ \text{rad/s}}\ \ (N=\tfrac{60\omega}{2\pi}=133.8\ \text{rpm})$$

Check: $z_0=1-196.4(0.09)/19.62=0.099$ m, a vertex 0.1 m above the bottom, so the surface does not touch the bottom ✓.

@s 3
**(a) Two tanks, jets meeting on the base plane.** For an orifice at a depth $h$ below the water surface and a height $y$ above the base plane, the jet leaves horizontally with $v=\sqrt{2gh}$ and reaches the base after the fall time $t=\sqrt{2y/g}$, so the horizontal range is

$$R=vt=\sqrt{2gh}\sqrt{\frac{2y}{g}}=2\sqrt{h\,y}$$

Total depth $H=40$ cm so $y=H-h$. From the figure orifice A is 10 cm below the surface of its tank ($h_A=10$ cm, $y_A=30$ cm) and orifice B is 30 cm below the surface ($h_B=30$ cm, $y_B=10$ cm):

$$\begin{gathered}R_A=2\sqrt{10(30)}=34.64\ \text{cm} \\ R_B=2\sqrt{30(10)}=34.64\ \text{cm}\end{gathered}$$

$$\boxed{x=R_A+R_B=69.3\ \text{cm}=0.693\ \text{m}}$$

*Is the point equidistant?* **Yes**: $R_A=R_B=34.64$ cm, because $h_A\,y_A=h_B\,y_B$ (the depths 10 cm and 30 cm are complementary, $h_B=H-h_A$): orifices at depth $h$ and at depth $H-h$ give the same range, so P is exactly midway between the tanks.

*If the orifices are located differently* (general positions $h_A$ and $h_B$ with $h_A\neq h_B$ and $h_A+h_B\neq H$) the two ranges $2\sqrt{h_A(H-h_A)}$ and $2\sqrt{h_B(H-h_B)}$ are no longer equal; the meeting point is not at the middle and the tank spacing becomes $x=2\sqrt{h_A(H-h_A)}+2\sqrt{h_B(H-h_B)}$. The range of one orifice is greatest, $R=H$, when the orifice is at the mid-depth $h=H/2$, so for two such orifices the maximum possible spacing is $2H=80$ cm.

**OR: Venturimeter.** $d_1=0.4$ m, $d_2=0.25$ m: $a_1=0.12566$ m², $a_2=0.04909$ m². The inverted U-tube contains a liquid lighter than water (S = 0.7), so the pressure-head difference (piezometric) is

$$\left(\frac{p_1}{\gamma}+z_1\right)-\left(\frac{p_2}{\gamma}+z_2\right)=x\,(1-S_l)=0.26(1-0.7)=0.078\ \text{m of water}$$

Continuity: $V_2=V_1\dfrac{a_1}{a_2}=V_1\left(\dfrac{400}{250}\right)^2=2.56V_1$. Energy between main and throat with the loss $0.4\dfrac{V_1^2}{2g}$:

$$0.078=\frac{V_2^2-V_1^2}{2g}+0.4\frac{V_1^2}{2g}=\frac{V_1^2}{2g}\,(6.5536-1+0.4)=5.9536\,\frac{V_1^2}{2g}$$

$$V_1^2=\frac{0.078(19.62)}{5.9536}=0.2570\ \Rightarrow\ V_1=0.507\ \text{m/s}$$

$$\boxed{Q=a_1V_1=0.12566(0.507)=0.0637\ \text{m}^3/\text{s}\ (63.7\ \text{L/s})}$$

**(b) Double U-tube manometer.** Reading of the figure: interface 2 is 20 cm below the axis of pipe 1; the S₁ = 1.6 liquid rises in the second limb to interface 3, which is 2 cm above the axis of pipe 1 (so 22 cm above interface 2); air sits between 3 and 4 (uniform pressure, its weight neglected); the air–alcohol interface 4 is 13 cm above the level of pipe 5, which is level with 3. Work with gauge differences in terms of $\gamma_w$ and take the axis of pipe 1 as the datum.

$$\begin{gathered}p_2=p_1+\gamma_w(0.20)\\ p_3=p_2-1.6\gamma_w(0.22)\\ p_4=p_3\ (\text{air})\\ p_5=p_4+0.9\gamma_w(0.13)\end{gathered}$$

$$p_5=p_1+\gamma_w\big[0.20-0.352+0.117\big]=p_1-0.035\,\gamma_w$$

$$\boxed{p_1-p_5=0.035\,\gamma_w=0.035(9810)=343\ \text{Pa}\approx0.34\ \text{kPa}}$$

(the pressure in the water pipe 1 is higher than in the alcohol pipe 5 by 0.343 kPa, i.e. 3.5 cm of water).

@s 4
**(a) Lagrangian method.** The motion of each individual fluid particle is followed in time (like tracking a car along a road): the position, velocity and acceleration of a particle are written as functions of time and of the initial position, $\vec r=\vec r(\vec r_0,t)$. It is the natural description of particle dynamics and of pathlines, but is cumbersome for continuous flow fields.

**Eulerian method.** Attention is fixed on points in space (like watching traffic at a junction): the velocity, pressure and density are given as functions of position and time at the fixed point, $\vec V=\vec V(x,y,z,t)$, and the acceleration is the substantial derivative, e.g. $a_x=u\frac{\partial u}{\partial x}+v\frac{\partial u}{\partial y}+w\frac{\partial u}{\partial z}+\frac{\partial u}{\partial t}$ (convective plus local). It is the method used in almost all fluid mechanics.

**Continuity equation in Cartesian form.** Consider a fixed rectangular control volume $dx\,dy\,dz$ with velocity components $u,v,w$ and density $\rho$. Mass entering the left face in the time $dt$: $\rho u\,dy\,dz\,dt$; leaving the right face: $\left[\rho u+\frac{\partial(\rho u)}{\partial x}dx\right]dy\,dz\,dt$. Net gain of mass in the $x$ direction:

$$-\frac{\partial(\rho u)}{\partial x}dx\,dy\,dz\,dt$$

and similarly $-\frac{\partial(\rho v)}{\partial y}$ and $-\frac{\partial(\rho w)}{\partial z}$ times $dx\,dy\,dz\,dt$. The mass inside increases at the rate $\dfrac{\partial\rho}{\partial t}dx\,dy\,dz\,dt$; equating,

$$\boxed{\frac{\partial\rho}{\partial t}+\frac{\partial(\rho u)}{\partial x}+\frac{\partial(\rho v)}{\partial y}+\frac{\partial(\rho w)}{\partial z}=0}$$

For steady flow $\partial\rho/\partial t=0$; for incompressible flow ($\rho$ constant) this reduces to $\boxed{\dfrac{\partial u}{\partial x}+\dfrac{\partial v}{\partial y}+\dfrac{\partial w}{\partial z}=0}$, and for two-dimensional flow $\dfrac{\partial u}{\partial x}+\dfrac{\partial v}{\partial y}=0$.

**(b) Force on the vertical bend.** $A=\frac{\pi}{4}(0.4)^2=0.12566$ m², $V=\dfrac{Q}{A}=\dfrac{0.5}{0.12566}=3.979$ m/s at both ends (same diameter, friction neglected). Both ends are at the same level and the velocity is the same, so by Bernoulli $p_2=p_1=118$ kN/m². $\rho=0.85(1000)=850$ kg/m³, $\dot m=\rho Q=425$ kg/s; the weight of oil in the bend is $W=850(9.81)(0.1)=833.9$ N; $p_1A=118(0.12566)=14.83$ kN.

*Geometry.* The vertical bend turns the flow through 90°: oil enters travelling down at 45° below the horizontal, and leaves travelling up at 45° above it (both ends are at the same level, so the bend is symmetric about the vertical):

$$\begin{gathered}\vec V_1=V(\cos45^\circ,-\sin45^\circ) \\ \vec V_2=V(\cos45^\circ,+\sin45^\circ)\end{gathered}$$

Let $F_x,F_y$ be the force of the bend *on the oil* (the oil exerts the opposite force on the bend). Momentum equation $\sum\vec F=\dot m(\vec V_2-\vec V_1)$, with pressure forces $p_1A$ along $\vec V_1$ (pushing in) and $p_2A$ opposite to $\vec V_2$:

$$x:\quad F_x+p_1A\cos45^\circ-p_2A\cos45^\circ=\dot m(V\cos45^\circ-V\cos45^\circ)=0\ \Rightarrow\ F_x=0$$

$$y:\quad F_y-W-p_1A\sin45^\circ-p_2A\sin45^\circ=\dot m(V\sin45^\circ+V\sin45^\circ)$$

$$\begin{gathered}F_y=W+2p_1A\sin45^\circ+2\dot mV\sin45^\circ\\ F_y=833.9+2(14\,830)(0.7071)+2(425)(3.979)(0.7071)\\ F_y=0.834+20.97+2.39=24.2\ \text{kN}\end{gathered}$$

The bend exerts 24.2 kN upward on the oil, so the oil exerts on the bend

$$\boxed{F=24.2\ \text{kN, vertically downward}\ (F_x=0)}$$

(If the bend is the other way up, i.e. oil enters going up at 45° and leaves going down, the same equations give $F_y=W-2p_1A\sin45^\circ-2\dot mV\sin45^\circ=-22.5$ kN: the force on the bend is **22.5 kN vertically upward**, again with $F_x=0$.)

@s 5
**(a) Boundary layer on a flat plate.** When a real fluid of free-stream velocity $U$ meets a thin flat plate parallel to the stream, the layer of fluid touching the plate sticks to it ($u=0$ no-slip) and the shear between layers slows the fluid in a thin region of thickness $\delta(x)$ next to the wall; outside it the flow is practically ideal ($u\approx U$). $\delta$ is the distance at which $u=0.99\,U$. The development along the plate (zero pressure gradient) is:

1. **Laminar region** from the leading edge: $\delta$ grows smoothly, $\delta=5x/\sqrt{Re_x}$; the velocity profile is nearly parabolic.
2. **Transition region** at the critical $Re_x\approx5\times10^5$ ($Re_x=Ux/\nu$): the layer becomes unstable and turns turbulent.
3. **Turbulent region**: $\delta$ grows faster, $\delta\approx0.37x/Re_x^{1/5}$, with a flatter, fuller profile and a very thin *laminar sub-layer* of thickness $\delta'=11.6\nu/u_*$ at the wall.

```figure caption="Question 5(a): growth of the boundary layer on a flat plate with zero pressure gradient: laminar, transition and turbulent regions with the laminar sub-layer."
import numpy as _np
fig,ax=plt.subplots(figsize=(5.8,2.7)); ax.axis("off")
x=_np.linspace(0.02,10,200)
d=_np.where(x<4,0.5*_np.sqrt(x/4)*1.2,0.6*1.0+0.12*(x-4)**0.8)
d[x>=4]=0.6+0.14*(x[x>=4]-4)**0.9
ax.fill_between(x,0,d,color="#dbe7f5"); ax.plot(x,d,color=ACCENT,lw=1.6)
ax.plot([0,10.5],[0,0],color=INK,lw=2.4)
ax.annotate("",xy=(0.0,1.7),xytext=(-1.2,1.7),arrowprops=dict(arrowstyle="-|>",color=INK)); ax.text(-1.3,1.9,"U",fontsize=9)
ax.plot([0,10.5],[1.45,1.45],color=GRID,lw=0.8)
for xp,w in ((1.5,0.5),(3.4,0.5)):
    yy=_np.linspace(0,0.5*_np.sqrt(xp/4)*1.2,20); u=1.5*yy/yy[-1]-0.5*(yy/yy[-1])**2*1.0
    ax.plot(xp+0.9*u/1.0*0.6,yy,color=INK,lw=1.0)
for xp in (7.0,9.2):
    dd=0.6+0.14*(xp-4)**0.9; yy=_np.linspace(0,dd,25); u=(yy/dd)**(1/7)
    ax.plot(xp+0.9*u,yy,color=INK,lw=1.0)
ax.text(2.0,-0.32,"laminar",ha="center",fontsize=8); ax.text(4.2,-0.32,"transition",ha="center",fontsize=8); ax.text(7.6,-0.32,"turbulent",ha="center",fontsize=8)
ax.text(8.0,0.08,"laminar sub-layer",fontsize=7.2,color=MUTED); ax.text(5.1,1.1,"δ",fontsize=10)
ax.axvline(3.9,color=GRID,lw=0.8,ls="--"); ax.axvline(5.2,color=GRID,lw=0.8,ls="--")
ax.set_xlim(-1.6,11); ax.set_ylim(-0.6,2.1)
```

**Pressure drag, friction drag and lift.**

- **Friction (skin-friction) drag:** the component of the wall shear stress along the free-stream direction, integrated over the wetted surface, $F_f=\int\tau_0\,dA$; it dominates for streamlined bodies and flat plates parallel to the flow.
- **Pressure (form) drag:** the component, along the stream, of the pressure forces normal to the surface; it arises when the boundary layer separates and a low-pressure wake forms, so the pressure at the rear is lower than at the front; it dominates for bluff bodies (cylinder, sphere, plate normal to the flow). Total drag = friction drag + pressure drag.
- **Lift:** the component of the resultant fluid force *perpendicular* to the free stream, caused by the unsymmetrical pressure distribution (lower pressure on the upper surface of an aerofoil or by circulation); $F_L=C_L\tfrac12\rho U^2A$.

**(b) Buckingham-$\pi$ for the triangular notch.** $Q=f(\theta,H,g,\rho,\mu,\sigma)$: $n=7$ variables; fundamental dimensions M, L, T so $m=3$; the number of dimensionless groups is $n-m=4$. Choose the repeating variables $H,\ g,\ \rho$ (they contain L, T and M respectively). $\theta$ is already dimensionless: $\pi_4=\theta$.

*$\pi_1$ with $Q=L^3T^{-1}$:* $\pi_1=Q\,H^{a}g^{b}\rho^{c}$, $[L^3T^{-1}][L]^a[LT^{-2}]^b[ML^{-3}]^c=1$:

$$\begin{gathered}M:\ c=0\\ T:\ -1-2b=0\ \Rightarrow\ b=-\tfrac12\\ L:\ 3+a+b-3c=0\ \Rightarrow\ a=-\tfrac52\end{gathered}\qquad\Rightarrow\ \pi_1=\frac{Q}{H^{5/2}g^{1/2}}$$

*$\pi_2$ with $\mu=ML^{-1}T^{-1}$:* $\pi_2=\mu H^{a}g^{b}\rho^{c}$:

$$\begin{gathered}M:\ 1+c=0\ \Rightarrow\ c=-1\\ T:\ -1-2b=0\ \Rightarrow\ b=-\tfrac12\\ L:\ -1+a+b-3c=0\ \Rightarrow\ a=-\tfrac32\end{gathered}\qquad\Rightarrow\ \pi_2=\frac{\mu}{\rho\,g^{1/2}H^{3/2}}$$

*$\pi_3$ with $\sigma=MT^{-2}$:* $\pi_3=\sigma H^{a}g^{b}\rho^{c}$:

$$\begin{gathered}M:\ 1+c=0\ \Rightarrow\ c=-1\\ T:\ -2-2b=0\ \Rightarrow\ b=-1\\ L:\ a+b-3c=0\ \Rightarrow\ a=-2\end{gathered}\qquad\Rightarrow\ \pi_3=\frac{\sigma}{\rho\,g\,H^{2}}$$

By the $\pi$-theorem $\pi_1=\phi_1(\pi_2,\pi_3,\pi_4)$:

$$\frac{Q}{H^{5/2}g^{1/2}}=\phi\left[\frac{\mu}{\rho g^{1/2}H^{3/2}},\ \frac{\sigma}{\rho gH^2},\ \theta\right]$$

$$\begin{gathered}\boxed{Q=g^{1/2}H^{5/2}\,\phi\left[\frac{\mu}{\rho g^{1/2}H^{3/2}},\frac{\sigma}{\rho gH^2},\theta\right]=C\,H^{5/2}} \\ C=g^{1/2}\phi\left[\cdots\right]\end{gathered}$$

which is the required form. (For a $V$-notch the viscous and surface-tension terms are small, and experiment gives $C=\tfrac{8}{15}C_d\sqrt{2g}\tan\tfrac{\theta}{2}$.)

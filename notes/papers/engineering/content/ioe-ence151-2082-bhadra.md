---
file: NEBians-IOE-Past-Paper-Strength-of-Materials-ENCE151-2082-Bhadra.pdf
subject: Strength of Materials
level: BE · Year I / Part II
code: ENCE 151
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Derive the relation between Young's Modulus (E) and Shear Modulus (G). [[4]]

b) A C.I. flat, 300 mm long and of 30 mm × 50 mm uniform section, is acted upon by the following forces uniformly distributed over the respective cross-section; 25 kN in the direction of length (tensile); 350 kN in the direction of the width (compressive); and 200 kN in the direction of thickness (tensile). Determine the change in dimensions and volume of the flat. Take E = 140 GN/m², and Poisson's ratio (υ) = 1/4. [[6]]

c) A rigid bar is supported by three rods at one end in the same vertical plane and equidistant. The other end of rods is rigidly fixed. The outer rods are of brass and of length 600 mm and diameter 30 mm. The central rod is of steel of 900 mm length and of 37.5 mm diameter. Calculate the forces in the bars due to an applied force 100 kN, if the bar remains horizontal after the load has been applied. Take E$_s$ / E$_b$ = 2. [[4]]

@q 2
Define product moment of inertia. Calculate principal moment of inertia and show their orientation of the following homogeneous plate. [[1+6]]

```figure caption="Question 2: the homogeneous plate made of a rectangle 140 mm × 240 mm, a quarter disc of radius 80 mm and a right triangle (base 180 mm, height 120 mm). The 40 mm and 120 mm dimensions on the right fix the vertical positions (80 + 40 + 120 = 240 mm)."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.5)); ax.set_aspect("equal"); ax.axis("off")
fc="#dbe7f5"
ax.add_patch(mp.Rectangle((0,0),140,240,fc=fc,ec=INK,lw=1))
t=_np.linspace(0,_np.pi/2,50)
q=[(140,160)]+[(140+80*_np.cos(a),160+80*_np.sin(a)) for a in t]
ax.add_patch(mp.Polygon(q,closed=True,fc=fc,ec=INK,lw=1))
ax.add_patch(mp.Polygon([(140,0),(320,0),(140,120)],closed=True,fc=fc,ec=INK,lw=1))
ax.plot([140,140],[0,240],color=MUTED,lw=0.8,ls="--")
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(0,-18),xytext=(140,-18),arrowprops=ar); ax.text(70,-34,"140 mm",ha="center",fontsize=7)
ax.annotate("",xy=(140,-18),xytext=(320,-18),arrowprops=ar); ax.text(230,-34,"180 mm",ha="center",fontsize=7)
ax.annotate("",xy=(345,0),xytext=(345,120),arrowprops=ar); ax.text(350,60,"120 mm",rotation=90,va="center",fontsize=7)
ax.annotate("",xy=(345,120),xytext=(345,160),arrowprops=ar); ax.text(350,140,"40 mm",va="center",fontsize=7)
ax.text(168,200,"R = 80 mm",fontsize=7,rotation=-10)
ax.text(-8,244,"L",fontsize=8,ha="right"); ax.text(-8,-4,"M",fontsize=8,ha="right"); ax.text(324,-6,"N",fontsize=8)
ax.set_xlim(-30,400); ax.set_ylim(-50,260)
```

@q 3
For the stresses shown in the figure, find the normal and tangential stress at a plane inclined at 60 degrees with major axis. Also determine principal stresses and their orientation. Verify the results with Mohr's circle. [[4+3]]

```figure caption="Question 3: stress element. σ$_x$ = 50 MN/m² (tension), σ$_y$ = 30 MN/m² (compression) and shear stress 30 MN/m² on all four faces."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.6,2.9)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),2,2,fc="#eef2f8",ec=INK,lw=1))
a=dict(arrowstyle="-|>",color=INK,lw=1.2)
ax.annotate("",xy=(1,2),xytext=(1,2.8),arrowprops=a); ax.text(1.1,2.55,"30",fontsize=8)
ax.annotate("",xy=(1,0),xytext=(1,-0.8),arrowprops=a); ax.text(1.1,-0.65,"30",fontsize=8)
ax.annotate("",xy=(-0.8,1),xytext=(0,1),arrowprops=a); ax.text(-0.75,1.1,"50",fontsize=8)
ax.annotate("",xy=(2.8,1),xytext=(2,1),arrowprops=a); ax.text(2.4,1.1,"50",fontsize=8)
ax.annotate("",xy=(1.8,2.25),xytext=(0.2,2.25),arrowprops=a); ax.text(0.9,2.32,"30",fontsize=8)
ax.annotate("",xy=(0.2,-0.25),xytext=(1.8,-0.25),arrowprops=a); ax.text(0.9,-0.5,"30",fontsize=8)
ax.annotate("",xy=(2.25,1.8),xytext=(2.25,0.2),arrowprops=a); ax.text(2.32,0.7,"30",fontsize=8)
ax.annotate("",xy=(-0.25,0.2),xytext=(-0.25,1.8),arrowprops=a); ax.text(-0.5,0.7,"30",fontsize=8)
ax.set_xlim(-1.1,3.2); ax.set_ylim(-1,3.1)
```

@q 4
A rectangular strain rosette, shown in figure, gives following readings in a strain measurement task, ε$^a$ = 1000 × 10$^{-6}$, ε$^b$ = 800 × 10$^{-6}$, ε$^c$ = 600 × 10$^{-6}$. Determine the principal strain and principal planes. [[4]]

```figure caption="Question 4: rectangular (45°) strain rosette: gauge a along the x-axis, gauge b at 45° and gauge c along the y-axis."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.0,2.6)); ax.set_aspect("equal"); ax.axis("off")
a=dict(arrowstyle="-|>",color=INK,lw=1)
ax.annotate("",xy=(3.3,0),xytext=(0,0),arrowprops=a); ax.text(3.35,-0.05,"x",fontsize=8)
ax.annotate("",xy=(0,3.0),xytext=(0,0),arrowprops=a); ax.text(0.05,3.05,"y",fontsize=8)
for ang,l in ((0,"a"),(45,"b"),(90,"c")):
    r=_np.radians(ang); cx,cy=1.8*_np.cos(r),1.8*_np.sin(r)
    ax.add_patch(mp.Rectangle((cx-0.55,cy-0.13),1.1,0.26,angle=ang,rotation_point="center",fc="#f4d9a8",ec=INK,lw=0.9))
    ax.text(2.6*_np.cos(r)+0.1,2.6*_np.sin(r)+0.1,l,fontsize=9,fontweight="bold")
ax.text(0.1,-0.35,"O",fontsize=8)
ax.set_xlim(-0.4,3.7); ax.set_ylim(-0.6,3.3)
```

@q 5
Define hoop and longitudinal stress. Prove that longitudinal stress is half of the circumferential stress for the thin cylinder with neat sketch. [[1+3]]

@q 6
a) Show that hollow shaft is more strong than solid shaft when material, weight and length are same. [[4]]

b) A solid circular shaft transmits 75 kW power at 200 RPM. Calculate the shaft diameter, if the twist in the shaft is not to exceed 1° in 2 meters length of shaft, and shear stress is limited to 50 MN/m². Take G = 100 GN/m². [[3]]

@q 7
a) Derive pure bending equation. [[4]]

b) A cantilever beam 4 m carries a uniformly distributed load of 50 kN/m over the whole span. The beam is of T-section with web 45 cm × 3 cm and flange is 35 cm × 5 cm making overall depth of 50 cm. Find the maximum tensile and compressive stresses if the flange is at the bottom and horizontal. Also determine the stress and its nature at 3 cm from top. [[6]]

@q 8
Derive Euler's formula of critical load for a steel column with one end fixed and other hinged. Derive the condition of no tension in rectangular column. [[4+3]]

<!-- SOLUTIONS -->

@s 1
**(a) Relation between E and G.**

Take a square element ABCD of side $a$, thickness 1, fixed along AB and acted on by a shear stress $\tau$ on the top face DC (with complementary shear on the sides). The face DC moves to D′C′, a distance $CC' = \gamma a$ where $\gamma = \tau/G$ is the shear strain.

*Strain along the diagonal.* The diagonal AC (length $\sqrt2\,a$) becomes AC′. For a small angle, the extension of the diagonal is the component of $CC'$ along it:

$$\begin{gathered}\Delta(AC)= CC'\cos 45^\circ=\frac{\gamma a}{\sqrt2} \\ \Rightarrow \\ \varepsilon_{AC}=\frac{\gamma a/\sqrt2}{\sqrt2\,a}=\frac{\gamma}{2}=\frac{\tau}{2G}.\end{gathered}$$

*Stresses on the diagonal planes.* A state of pure shear $\tau$ is equivalent to a **tensile stress $\tau$ on the diagonal plane BD (normal along AC)** and a **compressive stress $\tau$ on the other diagonal plane (normal along BD)**. Hence the strain along AC from Hooke's law is

$$\varepsilon_{AC}=\frac{\tau}{E}+\nu\frac{\tau}{E}=\frac{\tau}{E}(1+\nu).$$

Equating the two expressions for $\varepsilon_{AC}$:

$$\begin{gathered}\frac{\tau}{2G}=\frac{\tau(1+\nu)}{E} \\ \Longrightarrow \\ \boxed{E=2G(1+\nu)}\end{gathered}$$

**(b) C.I. flat under a triaxial load.** Let $x$ = length (300 mm), $y$ = width (50 mm) and $z$ = thickness (30 mm). $E = 140\ \text{GN/m}^2 = 140\times10^3$ N/mm², $\nu=0.25$. The stresses are the loads divided by the areas normal to them:

$$\begin{gathered}\sigma_x=\frac{25\times10^3}{50\times30}=+16.667 \\ \sigma_y=-\frac{350\times10^3}{300\times30}=-38.889 \\ \sigma_z=\frac{200\times10^3}{300\times50}=+13.333\ \ \text{N/mm}^2.\end{gathered}$$

Strains (tension positive):

$$\varepsilon_x=\frac{1}{E}\big[\sigma_x-\nu(\sigma_y+\sigma_z)\big]=\frac{16.667-0.25(-25.556)}{140\times10^3}=+1.6468\times10^{-4}$$

$$\varepsilon_y=\frac{1}{E}\big[\sigma_y-\nu(\sigma_x+\sigma_z)\big]=\frac{-38.889-0.25(30.0)}{140\times10^3}=-3.3135\times10^{-4}$$

$$\varepsilon_z=\frac{1}{E}\big[\sigma_z-\nu(\sigma_x+\sigma_y)\big]=\frac{13.333-0.25(-22.222)}{140\times10^3}=+1.3492\times10^{-4}$$

Changes in dimensions:

| Direction | Change |
|---|---|
| Length 300 mm | $\delta_x = 1.6468\times10^{-4}\times300 = +0.0494$ mm (increase) |
| Width 50 mm | $\delta_y = -3.3135\times10^{-4}\times50 = -0.01657$ mm (decrease) |
| Thickness 30 mm | $\delta_z = 1.3492\times10^{-4}\times30 = +0.00405$ mm (increase) |

Volumetric strain $\varepsilon_v=\varepsilon_x+\varepsilon_y+\varepsilon_z=-3.175\times10^{-5}$ (check: $\varepsilon_v=\dfrac{(1-2\nu)}{E}(\sigma_x+\sigma_y+\sigma_z)=\dfrac{0.5\times(-8.889)}{140\times10^3}=-3.175\times10^{-5}$). With $V=300\times50\times30=4.5\times10^5$ mm³:

$$\Delta V=\varepsilon_v V=-14.29\ \text{mm}^3\quad(\text{a decrease of } 14.3\ \text{mm}^3).$$

**(c) Rigid bar on three rods (statically indeterminate).** The rods are fixed to a wall at one end and carry the rigid bar at the other, so the bar stays horizontal when **all three rods extend equally**.

```figure caption="Three rods (two brass, one steel) fixed to the wall and joined at the free end by the rigid bar that carries the load P = 100 kN."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,2.0)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((-0.5,-1.2),0.5,2.4,fc="#c9ced6",ec=INK,lw=0.8,hatch="///"))
for y,w,l,c,nm in ((0.8,0.18,6,"#d9a441","brass 30 mm, 600 mm"),(0,0.24,9,"#8fa3b8","steel 37.5 mm, 900 mm"),(-0.8,0.18,6,"#d9a441","brass 30 mm, 600 mm")):
    ax.add_patch(mp.Rectangle((0,y-w/2),l*0.9,w,fc=c,ec=INK,lw=0.8))
ax.add_patch(mp.Rectangle((8.1,-1.2),0.2,2.4,fc="#555",ec=INK))
ax.annotate("",xy=(8.2,-1.2),xytext=(8.2,-2.2),arrowprops=dict(arrowstyle="<|-",color=INK,lw=1.3)); ax.text(8.45,-1.9,"P = 100 kN",fontsize=8)
ax.text(2.7,1.05,"brass: 600 mm, d = 30 mm",fontsize=7); ax.text(3.5,0.28,"steel: 900 mm, d = 37.5 mm",fontsize=7)
ax.set_xlim(-0.6,10.6); ax.set_ylim(-2.4,1.5)
```

Let $P_b$ be the load in each brass rod and $P_s$ the load in the steel rod. Equilibrium: $2P_b+P_s=100\times10^3$ N. Areas: $A_b=\dfrac{\pi}{4}(30)^2=706.86$ mm², $A_s=\dfrac{\pi}{4}(37.5)^2=1104.47$ mm².

Compatibility, $\delta_b=\delta_s$ with $E_s=2E_b$:

$$\frac{P_b(600)}{A_bE_b}=\frac{P_s(900)}{A_s(2E_b)}\ \Rightarrow\ P_s=P_b\,\frac{600}{900}\cdot 2\cdot\frac{A_s}{A_b}=2.0833\,P_b .$$

Substituting: $2P_b+2.0833P_b=100\times10^3$, so

$$\boxed{P_b=24.49\ \text{kN (each brass rod)},\qquad P_s=51.02\ \text{kN (steel rod)}}$$

Stresses: $\sigma_b=24490/706.86=34.65$ N/mm², $\sigma_s=51020/1104.47=46.19$ N/mm². (Check: $2(24.49)+51.02=100.0$ kN.)

@s 2
**Product moment of inertia.** For an area $A$, the product of inertia about the axes $x$ and $y$ is $I_{xy}=\int xy\,dA$. It is zero if either axis is an axis of symmetry, positive or negative otherwise, and it is used to find the principal axes about which $I$ is maximum and minimum.

**Choice of axes and the parts.** Take the origin at M, $x$ along MN and $y$ along ML. Reading the figure (80 + 40 + 120 = 240 mm):

1. a rectangle 140 × 240 mm,
2. a quarter disc of radius 80 mm with its centre at (140, 160) and lying in the upper right quadrant (arc from (140, 240) to (220, 160)),
3. a right triangle with vertices (140, 0), (320, 0), (140, 120).

| Part | Area (mm²) | $\bar x$ | $\bar y$ | $I_x$ about O (mm⁴) | $I_y$ about O (mm⁴) | $I_{xy}$ about O (mm⁴) |
|---|---|---|---|---|---|---|
| 1 rectangle | 33 600 | 70 | 120 | $645.12\times10^6$ | $219.52\times10^6$ | $282.24\times10^6$ |
| 2 quarter disc | 5 026.5 | 173.95 | 193.95 | $191.34\times10^6$ | $154.35\times10^6$ | $168.91\times10^6$ |
| 3 triangle | 10 800 | 200 | 40 | $25.92\times10^6$ | $451.44\times10^6$ | $79.92\times10^6$ |
| **Total** | **49 426.5** | | | $862.38\times10^6$ | $825.31\times10^6$ | $531.08\times10^6$ |

How the rows come out: rectangle $I_x=bh^3/3$, $I_y=hb^3/3$, $I_{xy}=b^2h^2/4$. Triangle: $I_x=bh^3/12$, $I_y=\dfrac{hb^3}{36}+A\bar x^2$, $I_{xy}=I_{x'y'}+A\bar x\bar y$ with $I_{x'y'}=-b^2h^2/72$. Quarter disc: about its own centroid $I_x=I_y=\left(\dfrac{\pi}{16}-\dfrac{4}{9\pi}\right)r^4=0.0549\,r^4$ and $I_{xy}=\left(\dfrac18-\dfrac{4}{9\pi}\right)r^4=-0.01647\,r^4$, centroid $\dfrac{4r}{3\pi}=33.95$ mm from the straight edges; then the parallel axis theorem is applied.

**Centroid.**

$$\begin{gathered}\bar X=\frac{\sum A\bar x}{\sum A}=108.98\ \text{mm} \\ \bar Y=\frac{\sum A\bar y}{\sum A}=110.04\ \text{mm}.\end{gathered}$$

**Centroidal moments (parallel axis theorem).**

$$I_{\bar x}=862.38\times10^6-49\,426.5(110.04)^2=263.88\times10^6\ \text{mm}^4$$

$$I_{\bar y}=825.31\times10^6-49\,426.5(108.98)^2=238.31\times10^6\ \text{mm}^4$$

$$I_{\bar x\bar y}=531.08\times10^6-49\,426.5(108.98)(110.04)=-61.64\times10^6\ \text{mm}^4$$

**Principal moments of inertia.**

$$I_{\max,\min}=\frac{I_{\bar x}+I_{\bar y}}{2}\pm\sqrt{\left(\frac{I_{\bar x}-I_{\bar y}}{2}\right)^2+I_{\bar x\bar y}^2}=251.10\times10^6\pm\sqrt{(12.78\times10^6)^2+(61.64\times10^6)^2}$$

$$\boxed{I_{\max}=314.05\times10^6\ \text{mm}^4,\qquad I_{\min}=188.14\times10^6\ \text{mm}^4}$$

**Orientation.**

$$\tan2\theta_p=\frac{-2I_{\bar x\bar y}}{I_{\bar x}-I_{\bar y}}=\frac{123.29}{25.56}=4.824\quad\Rightarrow\quad 2\theta_p=78.29^\circ,\ \ \theta_p=39.14^\circ .$$

The axis of $I_{\max}$ is inclined at $\theta_p=39.14^\circ$ anticlockwise from the centroidal $x$-axis, and the axis of $I_{\min}$ is perpendicular to it (at $129.14^\circ$). (Check: $I_{\theta}=I_{\text{avg}}+\frac{I_x-I_y}{2}\cos2\theta-I_{xy}\sin2\theta=251.10+2.59+60.36=314.05\times10^6$.)

```figure caption="Centroid C (108.98, 110.04) and principal axes: I$_{max}$ = 314.05×10⁶ mm⁴ along the axis at 39.14° to the x-axis, I$_{min}$ = 188.14×10⁶ mm⁴ along the perpendicular axis."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.8,3.6)); ax.set_aspect("equal"); ax.axis("off")
fc="#e4ecf7"
ax.add_patch(mp.Rectangle((0,0),140,240,fc=fc,ec=INK,lw=0.9))
t=_np.linspace(0,_np.pi/2,50)
ax.add_patch(mp.Polygon([(140,160)]+[(140+80*_np.cos(a),160+80*_np.sin(a)) for a in t],closed=True,fc=fc,ec=INK,lw=0.9))
ax.add_patch(mp.Polygon([(140,0),(320,0),(140,120)],closed=True,fc=fc,ec=INK,lw=0.9))
cx,cy=108.98,110.04
ax.plot([cx-110,cx+110],[cy,cy],color=MUTED,lw=0.8,ls="--"); ax.plot([cx,cx],[cy-110,cy+130],color=MUTED,lw=0.8,ls="--")
th=_np.radians(39.14); L=150
ax.plot([cx-L*_np.cos(th),cx+L*_np.cos(th)],[cy-L*_np.sin(th),cy+L*_np.sin(th)],color=SERIES[1],lw=1.6)
ax.plot([cx+L*_np.sin(th)*0.8,cx-L*_np.sin(th)*0.8],[cy-L*_np.cos(th)*0.8,cy+L*_np.cos(th)*0.8],color=SERIES[2],lw=1.6)
ax.plot([cx],[cy],"o",color=INK,ms=4); ax.text(cx+6,cy-16,"C",fontsize=8)
ax.add_patch(mp.Arc((cx,cy),120,120,theta1=0,theta2=39.14,color=INK,lw=0.8)); ax.text(cx+66,cy+14,"39.14°",fontsize=7)
ax.text(cx+L*_np.cos(th)+4,cy+L*_np.sin(th)-2,"I$_{max}$",fontsize=8,color=SERIES[1])
ax.text(cx-L*_np.sin(th)*0.8-52,cy+L*_np.cos(th)*0.8+4,"I$_{min}$",fontsize=8,color=SERIES[2])
ax.set_xlim(-20,340); ax.set_ylim(-20,262)
```

@s 3
Taking tension as positive and the shear on the right face acting upward as positive: $\sigma_x=+50$, $\sigma_y=-30$ (the arrows push on the faces) and $\tau_{xy}=+30$, all in MN/m² (= N/mm²).

**Principal stresses.**

$$\begin{gathered}\frac{\sigma_x+\sigma_y}{2}=10 \\ \frac{\sigma_x-\sigma_y}{2}=40 \\ R=\sqrt{40^2+30^2}=50 .\end{gathered}$$

$$\boxed{\sigma_1=10+50=60\ \text{MN/m}^2\ (\text{tensile}),\qquad \sigma_2=10-50=-40\ \text{MN/m}^2\ (\text{compressive})}$$

**Orientation.**

$$\tan2\theta_p=\frac{2\tau_{xy}}{\sigma_x-\sigma_y}=\frac{60}{80}=0.75\ \Rightarrow\ 2\theta_p=36.87^\circ,\quad \boxed{\theta_p=18.43^\circ}$$

The major principal plane ($\sigma_1$ = 60) has its normal at $18.43^\circ$ anticlockwise from the $x$-axis; the minor principal plane ($\sigma_2$ = −40) is at $108.43^\circ$. Maximum shear stress $=R=50$ MN/m².

**Stresses on a plane inclined at 60° with the major axis.** Taking the major principal axis as the reference (the plane's normal at $\theta=60^\circ$ from the $\sigma_1$ direction), the principal stresses are the "$\sigma_x,\sigma_y$" of the transformation with no shear:

$$\sigma_n=\frac{\sigma_1+\sigma_2}{2}+\frac{\sigma_1-\sigma_2}{2}\cos2\theta=10+50\cos120^\circ=\boxed{-15\ \text{MN/m}^2\ (\text{compressive})}$$

$$\tau=\frac{\sigma_1-\sigma_2}{2}\sin2\theta=50\sin120^\circ=\boxed{43.30\ \text{MN/m}^2}$$

(the shear stress tends to rotate the element clockwise). The resultant is $\sqrt{15^2+43.3^2}=45.8$ MN/m². Check: $\sigma_n+\sigma_n'=-15+(10+50\cos300^\circ)=-15+35=20=\sigma_x+\sigma_y$ ✓.

*If the 60° is measured from the x-axis instead* (plane with normal at 60° anticlockwise from $x$): $\sigma_n=10+40\cos120^\circ+30\sin120^\circ=15.98$ MN/m² (tensile) and $|\tau|=\left|-40\sin120^\circ+30\cos120^\circ\right|=49.64$ MN/m².

**Mohr's circle verification.** Centre $C(10,0)$, radius 50. With shear drawn positive when it tends to rotate the element clockwise, point X (on the $x$-face) is $(50,-30)$ and point Y is $(-30,+30)$. The circle meets the $\sigma$-axis at $60$ and $-40$ (principal stresses), $2\theta_p=36.87^\circ$. A plane at 60° from the $\sigma_1$ axis is the point reached by turning $120^\circ$ from the $\sigma_1$ point, which scales to $\sigma_n=10+50\cos120^\circ=-15$ and $\tau=50\sin120^\circ=43.3$ — the same as the analytical results.

```figure caption="Mohr's circle (σ, τ in MN/m²): centre (10, 0), radius 50. X (50, −30) and Y (−30, +30) are the stresses on the x- and y-faces; the circle cuts the σ-axis at σ$_1$ = 60 and σ$_2$ = −40; point P (−15, 43.3) is the plane at 60° to the major axis."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.4,3.5))
t=_np.linspace(0,2*_np.pi,300); ax.plot(10+50*_np.cos(t),50*_np.sin(t),color=ACCENT,lw=1.4)
ax.axhline(0,color=MUTED,lw=0.8); ax.axvline(0,color=MUTED,lw=0.8)
X=(50,-30); Y=(-30,30); P=(-15,43.3)
ax.plot([X[0],Y[0]],[X[1],Y[1]],color=INK,lw=1)
ax.plot([10,P[0]],[0,P[1]],color=SERIES[1],lw=1.1)
for p,l,dx,dy in ((X,"X (50, −30)",3,-8),(Y,"Y (−30, 30)",-42,6),(P,"P (−15, 43.3)",-20,5),((60,0),"σ₁ = 60",3,4),((-40,0),"σ₂ = −40",-30,4),((10,0),"C",2,-8)):
    ax.plot(*p,"o",color=INK,ms=3.5); ax.text(p[0]+dx,p[1]+dy,l,fontsize=7)
ax.set_aspect("equal"); ax.set_xlabel("σ (MN/m²)"); ax.set_ylabel("τ (clockwise +)")
ax.set_xlim(-65,80); ax.set_ylim(-62,62)
```

@s 4
For a rectangular (45°) rosette with gauge $a$ at $0^\circ$ (the $x$-axis), $b$ at $45^\circ$ and $c$ at $90^\circ$ (the $y$-axis):

$$\begin{gathered}\varepsilon_x=\varepsilon_a=1000\times10^{-6} \\ \varepsilon_y=\varepsilon_c=600\times10^{-6}.\end{gathered}$$

The strain at 45° is $\varepsilon_b=\dfrac{\varepsilon_x+\varepsilon_y}{2}+\dfrac{\gamma_{xy}}{2}$, so

$$\gamma_{xy}=2\varepsilon_b-\varepsilon_a-\varepsilon_c=(1600-1000-600)\times10^{-6}=0 .$$

**Principal strains.**

$$\varepsilon_{1,2}=\frac{\varepsilon_x+\varepsilon_y}{2}\pm\sqrt{\left(\frac{\varepsilon_x-\varepsilon_y}{2}\right)^2+\left(\frac{\gamma_{xy}}{2}\right)^2}=800\times10^{-6}\pm200\times10^{-6}$$

$$\boxed{\varepsilon_1=1000\times10^{-6},\qquad \varepsilon_2=600\times10^{-6}}$$

**Principal planes.** $\tan2\theta_p=\dfrac{\gamma_{xy}}{\varepsilon_x-\varepsilon_y}=\dfrac{0}{400\times10^{-6}}=0$, so $\boxed{\theta_p=0^\circ}$ (and $90^\circ$): the principal directions coincide with the gauge axes $a$ (maximum strain $1000\times10^{-6}$) and $c$ (minimum strain $600\times10^{-6}$). Maximum shear strain $\gamma_{\max}=\varepsilon_1-\varepsilon_2=400\times10^{-6}$ at 45° (gauge $b$ reads the mean strain 800 × 10⁻⁶, as expected).

@s 5
**Hoop (circumferential) stress.** In a thin cylindrical shell under internal pressure, the tensile stress acting **tangentially to the circumference** (it tends to split the cylinder along a longitudinal line) is the hoop or circumferential stress $\sigma_h$ (or $\sigma_c$).

**Longitudinal stress.** The tensile stress acting **along the axis of the cylinder** on a transverse cross-section (it tends to tear the cylinder across a circular section) is the longitudinal stress $\sigma_l$.

```figure caption="Thin cylinder (internal diameter d, wall thickness t, length l, pressure p). Left: a longitudinal section; the bursting force p·d·l is resisted by the hoop stress on two strips of area t·l. Right: a transverse cut; the end thrust p·πd²/4 is resisted by the longitudinal stress on the ring of area πdt."
import numpy as _np, matplotlib.patches as mp
fig,axs=plt.subplots(1,2,figsize=(6.2,2.5))
a=axs[0]; a.set_aspect("equal"); a.axis("off"); a.set_title("longitudinal section",fontsize=8)
a.add_patch(mp.Rectangle((0,0),4,2.6,fc="#eef2f8",ec=INK,lw=1)); a.add_patch(mp.Rectangle((0,0),4,0.22,fc="#8fa3b8",ec=INK)); a.add_patch(mp.Rectangle((0,2.38),4,0.22,fc="#8fa3b8",ec=INK))
for x in (0.8,1.8,2.8,3.4): a.annotate("",xy=(x,2.38),xytext=(x,1.3),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1)); a.annotate("",xy=(x,0.22),xytext=(x,1.3),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1))
a.text(2.0,1.35,"p",fontsize=8,color=SERIES[1],ha="center"); a.annotate("",xy=(4.1,0),xytext=(4.1,2.6),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.8)); a.text(4.25,1.2,"d",fontsize=8)
a.annotate("",xy=(0.6,-0.65),xytext=(0.6,0),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2)); a.annotate("",xy=(0.6,3.25),xytext=(0.6,2.6),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2)); a.text(0.8,3.0,"σ$_h$ t l",fontsize=7.5); a.text(0.8,-0.55,"σ$_h$ t l",fontsize=7.5)
a.set_xlim(-0.2,4.8); a.set_ylim(-0.9,3.5)
b=axs[1]; b.set_aspect("equal"); b.axis("off"); b.set_title("transverse cut (end view of the cut part)",fontsize=8)
b.add_patch(mp.Rectangle((0,0),1.2,2.6,fc="#8fa3b8",ec=INK)); b.add_patch(mp.Rectangle((1.2,0.22),2.2,2.16,fc="#eef2f8",ec=INK)); b.add_patch(mp.Rectangle((0,0),0.22,2.6,fc="#8fa3b8",ec=INK))
for y in (0.7,1.3,1.9): b.annotate("",xy=(0.22,y),xytext=(1.2,y),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1))
b.text(0.55,1.4,"p",fontsize=8,color=SERIES[1])
b.annotate("",xy=(3.9,1.3),xytext=(3.4,1.3),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.3)); b.text(3.5,1.45,"σ$_l$ π d t",fontsize=7.5)
b.set_xlim(-0.2,4.8); b.set_ylim(-0.3,3.0)
```

**Hoop stress.** Consider half the cylinder of length $l$ cut along a diameter. The bursting force due to the pressure on the projected area is $F_b=p\times(d\,l)$. It is resisted by the tension in the two cut walls, $F_r=\sigma_h\times(2\,t\,l)$. For equilibrium:

$$p\,d\,l=2\sigma_h t\,l\quad\Rightarrow\quad \boxed{\sigma_h=\frac{p\,d}{2t}}$$

**Longitudinal stress.** Cut the cylinder by a plane perpendicular to the axis. The pressure acts on the end area $\dfrac{\pi d^2}{4}$, giving the force $p\dfrac{\pi d^2}{4}$ (tending to separate the ends). It is resisted by the stress $\sigma_l$ over the thin ring area $\pi d\,t$ (thin shell, $\pi(d+t)t\approx\pi d t$):

$$p\,\frac{\pi d^2}{4}=\sigma_l\,\pi d\,t\quad\Rightarrow\quad \boxed{\sigma_l=\frac{p\,d}{4t}}$$

**Comparison.**

$$\begin{gathered}\frac{\sigma_l}{\sigma_h}=\frac{pd/4t}{pd/2t}=\frac12 \\ \Longrightarrow \\ \sigma_l=\frac{\sigma_h}{2}\ \ \blacksquare\end{gathered}$$

So the longitudinal stress is half of the circumferential stress, which is why a pressurised pipe (or a boiler or a sausage) always splits along its length first.

@s 6
**(a) Hollow shaft is stronger than a solid shaft of the same material, weight and length.**

Same material and length and the same weight mean the **same cross-sectional area**. Let the solid shaft have diameter $d$ and the hollow shaft outer and inner diameters $D$ and $d_i$:

$$\frac{\pi}{4}d^2=\frac{\pi}{4}(D^2-d_i^2)\quad\Rightarrow\quad d^2=D^2-d_i^2 .$$

For the same maximum shear stress $\tau$, the torque capacities are $T_s=\dfrac{\pi}{16}\tau d^3$ and $T_h=\dfrac{\pi}{16}\tau\dfrac{D^4-d_i^4}{D}$. So

$$\frac{T_h}{T_s}=\frac{D^4-d_i^4}{D\,d^3}=\frac{(D^2+d_i^2)(D^2-d_i^2)}{D\,d^3}=\frac{(D^2+d_i^2)\,d^2}{D\,d^3}=\frac{D^2+d_i^2}{D\,d}.$$

This is greater than 1, because squaring the condition $\dfrac{D^2+d_i^2}{Dd}>1$ and using $d^2=D^2-d_i^2$ gives $(D^2+d_i^2)^2>D^2(D^2-d_i^2)$, i.e. $D^4+2D^2d_i^2+d_i^4>D^4-D^2d_i^2$, which is always true. Hence $T_h>T_s$: **the hollow shaft carries more torque**, i.e. it is stronger.

*Numerical illustration.* For $d_i=0.6D$: $d^2=D^2(1-0.36)=0.64D^2$, $d=0.8D$, and $T_h/T_s=\dfrac{1+0.36}{0.8}=1.70$: the hollow shaft is 70 % stronger for the same weight. The reason is that in a solid shaft the material near the axis is lightly stressed, while in the hollow shaft the material is pushed to the outside, where the shear stress and the lever arm are the largest (it is also stiffer: $J_h>J_s$).

**(b) Solid shaft: 75 kW at 200 rpm.**

$$T=\frac{P}{\omega}=\frac{75\times10^3}{2\pi(200)/60}=3580.99\ \text{N·m}=3.581\times10^6\ \text{N·mm}.$$

*By strength* ($\tau\le50$ N/mm²): $\ \dfrac{\pi}{16}d^3\tau=T\Rightarrow d^3=\dfrac{16(3.581\times10^6)}{\pi(50)}=364\,770$, so $d=71.45$ mm.

*By stiffness* ($\theta\le1^\circ=0.017453$ rad in $L=2000$ mm, $G=100\times10^3$ N/mm²): $\ \theta=\dfrac{TL}{GJ}$ with $J=\dfrac{\pi d^4}{32}$:

$$d^4=\frac{32\,T\,L}{\pi G\theta}=\frac{32(3.581\times10^6)(2000)}{\pi(100\times10^3)(0.017453)}=4.18\times10^{7}\ \text{mm}^4\ \Rightarrow\ d=80.41\ \text{mm}.$$

The larger value governs, so

$$\boxed{d\approx80.4\ \text{mm}\ \ (\text{adopt }82\ \text{or }85\ \text{mm in practice})}$$

Check of the shear stress at $d=80.4$ mm: $\tau=\dfrac{16T}{\pi d^3}=\dfrac{16(3.581\times10^6)}{\pi(80.4)^3}=35.1\ \text{N/mm}^2<50$ ✓ (the shaft is governed by the twist limit).

@s 7
**(a) Pure bending equation $\dfrac{M}{I}=\dfrac{\sigma}{y}=\dfrac{E}{R}$.**

*Assumptions.* The material is homogeneous and isotropic and obeys Hooke's law; $E$ is the same in tension and compression; plane sections remain plane after bending; the radius of curvature is large compared with the depth; each layer is free to expand or contract; the beam is initially straight and the loading is in a plane of symmetry (pure bending: constant $M$, no shear).

```figure caption="Pure bending of a beam element: the neutral layer NN keeps its length; a layer at distance y from it is stretched (above) or shortened (below)."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.2,2.7)); ax.set_aspect("equal"); ax.axis("off")
R=6.0; ph=_np.radians(26)
t=_np.linspace(_np.pi/2-ph/2,_np.pi/2+ph/2,40)
O=(0,-R)
for r,c,lw,ls in ((R,ACCENT,1.6,"-"),(R+1.4,INK,1.0,"-"),(R-1.4,INK,1.0,"-"),(R+0.7,MUTED,0.8,"--")):
    ax.plot(O[0]+r*_np.cos(t),O[1]+r*_np.sin(t),color=c,lw=lw,ls=ls)
for a_ in (t[0],t[-1]):
    ax.plot([O[0]+(R-1.4)*_np.cos(a_),O[0]+(R+1.4)*_np.cos(a_)],[O[1]+(R-1.4)*_np.sin(a_),O[1]+(R+1.4)*_np.sin(a_)],color=INK,lw=1)
    ax.plot([O[0],O[0]+(R-1.4)*_np.cos(a_)],[O[1],O[1]+(R-1.4)*_np.sin(a_)],color=MUTED,lw=0.7,ls=":")
ax.text(-0.15,0.2,"N",fontsize=8,color=ACCENT); ax.text(-0.1,0.55,"neutral layer",fontsize=7,color=ACCENT,ha="center")
ax.text(0.0,1.27,"layer at y",fontsize=7,color=MUTED,ha="center")
ax.text(0.8,-2.2,"R",fontsize=9); ax.plot([0,0.0],[-R,0],color=MUTED,lw=0.7,ls=":")
ax.plot([0],[-R],"o",color=INK,ms=3); ax.text(0.15,-R-0.3,"O",fontsize=8)
ax.add_patch(mp.Arc(O,3.2,3.2,theta1=_np.degrees(t[0]),theta2=_np.degrees(t[-1]),color=INK,lw=0.8)); ax.text(0.0,-R+3.4,"θ",fontsize=9,ha="center")
ax.set_xlim(-3,3); ax.set_ylim(-R-0.6,2.4)
```

Consider a short element of length $dx$ bent to radius of curvature $R$ (measured to the neutral layer NN), subtending the angle $\theta$ at the centre O. The neutral layer length is $NN=R\theta$ (unchanged). The layer at distance $y$ from NN has original length $R\theta$ and final length $(R+y)\theta$:

$$\varepsilon=\frac{(R+y)\theta-R\theta}{R\theta}=\frac{y}{R}.$$

By Hooke's law, $\sigma=E\varepsilon$:

$$\begin{gathered}\frac{\sigma}{y}=\frac{E}{R}. \\ (1)\end{gathered}$$

*Neutral axis.* The net axial force is zero: $\int\sigma\,dA=\dfrac{E}{R}\int y\,dA=0$, so $\int y\,dA=0$: the neutral axis passes through the **centroid**.

*Moment of resistance.* The moment of the stress about the neutral axis, with $dF=\sigma\,dA$:

$$\begin{gathered}M=\int\sigma\,y\,dA=\frac{E}{R}\int y^2dA=\frac{E}{R}I\quad\Rightarrow\quad\frac{M}{I}=\frac{E}{R}. \\ (2)\end{gathered}$$

Combining (1) and (2):

$$\boxed{\frac{M}{I}=\frac{\sigma}{y}=\frac{E}{R}}$$

The bending stress varies linearly with the distance from the neutral axis, and $\sigma_{\max}=M\,y_{\max}/I=M/Z$ with the section modulus $Z=I/y_{\max}$.

**(b) Cantilever with a T-section (flange at the bottom).**

$w=50$ kN/m over $L=4$ m. The maximum bending moment is at the fixed end (hogging, so the top fibres are in tension and the bottom fibres in compression):

$$M_{\max}=\frac{wL^2}{2}=\frac{50(4)^2}{2}=400\ \text{kN·m}=400\times10^6\ \text{N·mm}.$$

*Section (in cm; the flange 35 × 5 at the bottom, the web 3 × 45 above it; overall depth 50).*

$$\bar y=\frac{(35\times5)(2.5)+(45\times3)(27.5)}{175+135}=\frac{437.5+3712.5}{310}=13.387\ \text{cm from the bottom}.$$

$$I=\frac{35(5)^3}{12}+175(13.387-2.5)^2+\frac{3(45)^3}{12}+135(27.5-13.387)^2=70\,777\ \text{cm}^4=7.0777\times10^8\ \text{mm}^4.$$

Distances of the extreme fibres from the neutral axis: top $y_t=50-13.387=36.613$ cm, bottom $y_b=13.387$ cm.

```figure caption="T-section with the flange at the bottom (dimensions in cm), the neutral axis 13.387 cm above the base and the bending stress diagram for the hogging moment of 400 kN·m (tension at the top, compression at the bottom)."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.8,3.3)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((-17.5,0),35,5,fc="#dbe7f5",ec=INK,lw=1)); ax.add_patch(mp.Rectangle((-1.5,5),3,45,fc="#dbe7f5",ec=INK,lw=1))
ax.plot([-24,24],[13.387,13.387],color=SERIES[1],lw=1,ls="--"); ax.text(-24,15,"N.A.",fontsize=7,color=SERIES[1])
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(-17.5,-4),xytext=(17.5,-4),arrowprops=ar); ax.text(0,-8,"35",ha="center",fontsize=7)
ax.annotate("",xy=(-24,0),xytext=(-24,50),arrowprops=ar); ax.text(-27,25,"50",rotation=90,va="center",fontsize=7)
ax.text(2.6,38,"3",fontsize=7); ax.text(-22,2,"5",fontsize=7)
sx=0.12; x0=30
ax.plot([x0,x0],[0,50],color=INK,lw=0.8)
ax.add_patch(mp.Polygon([(x0,13.387),(x0,50),(x0+206.9*sx,50)],closed=True,fc="#f6c9c4",ec=INK,lw=0.8))
ax.add_patch(mp.Polygon([(x0,13.387),(x0,0),(x0-75.66*sx,0)],closed=True,fc="#c3d6f0",ec=INK,lw=0.8))
ax.plot([x0-8,x0+30],[13.387,13.387],color=SERIES[1],lw=0.8,ls="--")
ax.text(x0+206.9*sx+1,49,"206.9 (T)",fontsize=7); ax.text(x0-75.66*sx-2,-5,"75.7 (C)",fontsize=7,ha="center")
ax.set_xlim(-32,70); ax.set_ylim(-12,54)
```

**Maximum stresses** ($\sigma=\dfrac{M\,y}{I}$):

$$\sigma_{\text{top}}=\frac{400\times10^6(366.13)}{7.0777\times10^8}=\boxed{206.9\ \text{N/mm}^2\ \text{(tensile)}}$$

$$\sigma_{\text{bottom}}=\frac{400\times10^6(133.87)}{7.0777\times10^8}=\boxed{75.7\ \text{N/mm}^2\ \text{(compressive)}}$$

**Stress at 3 cm from the top.** Its distance from the neutral axis is $y=36.613-3=33.613$ cm, above the neutral axis (tension zone):

$$\sigma=\frac{400\times10^6(336.13)}{7.0777\times10^8}=\boxed{190.0\ \text{N/mm}^2\ \text{(tensile)}}$$

@s 8
**(a) Euler's critical load for a column fixed at one end and hinged at the other.**

*Assumptions:* the column is initially straight, homogeneous and perfectly elastic (Hooke's law), the load is axial, the length is large compared with the cross-section (slender, so that the direct stress is negligible against the bending effect), and the section is uniform.

```figure caption="Column of length L, fixed at A and hinged at B: the axial load P produces a horizontal reaction H at the hinge and a fixing moment HL at A. Right: a rectangular column, the load must lie in the middle third (shaded) of each dimension for no tension."
import numpy as _np, matplotlib.patches as mp
fig,axs=plt.subplots(1,2,figsize=(6.0,3.0),gridspec_kw=dict(width_ratios=[1,1.1]))
a=axs[0]; a.set_aspect("equal"); a.axis("off")
a.add_patch(mp.Rectangle((-1.2,-0.35),2.4,0.35,fc="#c9ced6",ec=INK,hatch="///"))
yy=_np.linspace(0,6,80); xx=0.62*((yy/6)**2*(1-yy/6)*3.2)
a.plot(xx,yy,color=ACCENT,lw=2)
a.plot([0,0],[0,6.3],color=MUTED,lw=0.7,ls="--")
a.plot([0],[6],"o",color=INK,ms=5,mfc="white"); a.text(0.2,6.0,"B (hinge)",fontsize=7)
a.annotate("",xy=(0,5.95),xytext=(0,7.0),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1.5)); a.text(0.15,6.7,"P",fontsize=9,color=SERIES[1])
a.annotate("",xy=(-0.8,6),xytext=(0,6),arrowprops=dict(arrowstyle="-|>",color=SERIES[2],lw=1.3)); a.text(-1.15,6.15,"H",fontsize=8,color=SERIES[2])
a.text(-1.5,-0.9,"A (fixed), M$_A$ = H L",fontsize=7); a.annotate("",xy=(1.3,0),xytext=(1.3,6),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.8)); a.text(1.4,3,"L",fontsize=8)
a.set_xlim(-2,2); a.set_ylim(-1.2,7.4)
b=axs[1]; b.set_aspect("equal"); b.axis("off")
b.add_patch(mp.Rectangle((0,0),3,2,fc="#eef2f8",ec=INK,lw=1))
b.add_patch(mp.Polygon([(1.5,0.667),(2,1),(1.5,1.333),(1.0,1)],closed=True,fc="#f6c9c4",ec=SERIES[1],lw=1.2))
b.add_patch(mp.Rectangle((1,0),1,2,fc="none",ec=MUTED,lw=0.8,ls="--")); b.add_patch(mp.Rectangle((0,0.667),3,0.667,fc="none",ec=MUTED,lw=0.8,ls="--"))
b.annotate("",xy=(0,-0.35),xytext=(3,-0.35),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.8)); b.text(1.5,-0.7,"d",ha="center",fontsize=8)
b.annotate("",xy=(1,2.3),xytext=(2,2.3),arrowprops=dict(arrowstyle="<->",color=SERIES[1],lw=0.8)); b.text(1.5,2.45,"d/3 (middle third)",ha="center",fontsize=7)
b.text(1.5,1.0,"kernel",ha="center",va="center",fontsize=7,color=SERIES[1])
b.set_xlim(-0.4,3.4); b.set_ylim(-1.0,2.9)
```

Take the origin at the hinged end B with $x$ along the column and $y$ the deflection. The load $P$ requires a horizontal reaction $H$ at B (since the moment $P\,y$ must be balanced; the fixed end gives a fixing moment $M_A=HL$). The bending moment at a section at distance $x$ from B is $Py-Hx$, so the differential equation of the elastic curve is

$$\begin{gathered}EI\frac{d^2y}{dx^2}=-Py+Hx\quad\Rightarrow\quad\frac{d^2y}{dx^2}+\alpha^2y=\frac{H}{EI}x \\ \alpha^2=\frac{P}{EI}.\end{gathered}$$

The general solution is

$$y=A\cos\alpha x+B\sin\alpha x+\frac{H}{P}x .$$

*Boundary conditions:*

1. $x=0,\ y=0$ (hinge): $A=0$.
2. $x=L,\ y=0$ (fixed end, no deflection): $B\sin\alpha L+\dfrac{H}{P}L=0.$
3. $x=L,\ \dfrac{dy}{dx}=0$ (fixed end, no rotation): $B\alpha\cos\alpha L+\dfrac{H}{P}=0.$

From (2), $B=-\dfrac{HL}{P\sin\alpha L}$; putting it in (3):

$$-\frac{HL\,\alpha\cos\alpha L}{P\sin\alpha L}+\frac{H}{P}=0\quad\Longrightarrow\quad\tan\alpha L=\alpha L .$$

The smallest non-zero root of $\tan\theta=\theta$ is $\alpha L=4.4934$ rad (slightly less than $3\pi/2=4.712$). Hence

$$P_{cr}=\alpha^2EI=\frac{(4.4934)^2EI}{L^2}=\frac{20.19\,EI}{L^2}=2.046\,\frac{\pi^2EI}{L^2}\approx\boxed{\frac{2\pi^2EI}{L^2}}$$

In the standard form $P_{cr}=\dfrac{\pi^2EI}{L_e^2}$, the **effective length is $L_e=\dfrac{L}{\sqrt2}\approx0.7L$** (exactly $0.699L$). (For the steel column: $I$ is the least moment of inertia of the section, $E=2\times10^5$ N/mm².)

**(b) Condition of no tension in a rectangular column.**

A rectangular column $b\times d$ carries a load $P$ at an eccentricity $e$ from the centroid along the side $d$. The direct stress is $\sigma_0=\dfrac{P}{bd}$ (compressive) and the bending stress is $\sigma_b=\dfrac{M}{Z}=\dfrac{Pe}{bd^2/6}=\dfrac{6Pe}{bd^2}$. The stress at the two extreme edges is

$$\sigma_{\max,\min}=\frac{P}{bd}\left(1\pm\frac{6e}{d}\right).$$

For **no tension** anywhere in the section the minimum stress must not be tensile:

$$\sigma_{\min}=\frac{P}{bd}\left(1-\frac{6e}{d}\right)\ge0\quad\Longrightarrow\quad\boxed{e\le\frac{d}{6}}$$

So the load must act **within the middle third** of the depth (the "middle third rule"). Similarly, an eccentricity $e_y$ along $b$ must satisfy $e_y\le b/6$; for eccentricity in both directions the load must lie within the rhombus (the **core or kernel**) whose diagonals are $d/3$ and $b/3$, shown shaded in the figure. At the limit $e=d/6$ the stress is zero at one edge and $2P/(bd)$ at the other.

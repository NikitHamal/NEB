---
file: NEBians-IOE-Past-Paper-Strength-of-Materials-CE151-2081-Ashwin.pdf
subject: Strength of Materials
level: BE · Year I / Part II
code: CE 151
year_bs: 2081 Ashwin
cal: BS
year_ad: 2024
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Derive the expression for the extension in a bar of length ℓ, uniformly tapering from a diameter d$_1$ at one end to a diameter d$_2$ at another end subjected to an axial tensile load P. [[7]]

b) A reinforced concrete column is 300 mm × 300 mm in section. The column is provided with 8 bars of 20 mm diameter. The column carries a load of 360 kN. Find the stresses in concrete and the steel bars. Take E$_s$ = 2.1×10$^5$ N/mm² and E$_c$ = 0.14×10$^5$ N/mm². [[5]]

@q 2
State the parallel axis theorem. Determine principal MOI for the section shown below. [[1+6]]

```figure caption="Question 2: the section is made of 1 a right triangle (base 70 mm, height 140 mm), 2 a rectangle 70 mm × 70 mm and 3 a quarter disc of radius 70 mm; the origin O is at the lower left corner."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.0,3.3)); ax.set_aspect("equal"); ax.axis("off")
fc="#dbe7f5"
ax.add_patch(mp.Polygon([(0,0),(70,0),(70,140)],closed=True,fc=fc,ec=INK,lw=1))
ax.add_patch(mp.Rectangle((70,0),70,70,fc=fc,ec=INK,lw=1))
t=_np.linspace(0,_np.pi/2,50)
ax.add_patch(mp.Polygon([(70,70)]+[(70+70*_np.cos(a),70+70*_np.sin(a)) for a in t],closed=True,fc=fc,ec=INK,lw=1))
ax.plot([70,70],[0,140],color=MUTED,lw=0.8,ls="--"); ax.plot([70,140],[70,70],color=MUTED,lw=0.8,ls="--")
ax.text(40,30,"1",fontsize=9); ax.text(100,32,"2",fontsize=9); ax.text(88,92,"3",fontsize=9)
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(0,-12),xytext=(70,-12),arrowprops=ar); ax.text(35,-25,"70 mm",ha="center",fontsize=7)
ax.annotate("",xy=(70,-12),xytext=(140,-12),arrowprops=ar); ax.text(105,-25,"70 mm",ha="center",fontsize=7)
ax.annotate("",xy=(155,0),xytext=(155,70),arrowprops=ar); ax.text(160,35,"70 mm",rotation=90,va="center",fontsize=7)
ax.annotate("",xy=(155,70),xytext=(155,140),arrowprops=ar); ax.text(160,105,"70 mm",rotation=90,va="center",fontsize=7)
a2=dict(arrowstyle="-|>",color=INK,lw=1)
ax.annotate("",xy=(175,0),xytext=(-15,0),arrowprops=a2); ax.text(172,-14,"x",fontsize=8)
ax.annotate("",xy=(0,160),xytext=(0,-15),arrowprops=a2); ax.text(4,158,"y",fontsize=8); ax.text(-12,-14,"O",fontsize=8)
ax.set_xlim(-25,200); ax.set_ylim(-35,170)
```

@q 3
a) State the state of stress at a point in a two-dimensional strained material is as shown in the figure. Determine the magnitude of principal planes, orientation of principal planes and maximum shear stress. Also, determine resultant stress on the plane of maximum shear stress. [[7]]

```figure caption="Question 3(a): σ$_x$ = 75 N/mm² (tension), σ$_y$ = 40 N/mm² (compression) and τ = 20 N/mm² on all faces."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(3.8,2.8)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Rectangle((0,0),2.4,1.6,fc="#eef2f8",ec=INK,lw=1))
a=dict(arrowstyle="-|>",color=INK,lw=1.2)
ax.annotate("",xy=(1.2,1.6),xytext=(1.2,2.3),arrowprops=a); ax.text(1.3,2.0,"σ$_y$",fontsize=8)
ax.annotate("",xy=(1.2,0),xytext=(1.2,-0.7),arrowprops=a); ax.text(1.3,-0.6,"σ$_y$ = 40",fontsize=8)
ax.annotate("",xy=(-0.7,0.8),xytext=(0,0.8),arrowprops=a); ax.text(-1.1,0.9,"σ$_x$",fontsize=8)
ax.annotate("",xy=(3.1,0.8),xytext=(2.4,0.8),arrowprops=a); ax.text(2.55,0.92,"σ$_x$ = 75",fontsize=8)
ax.annotate("",xy=(2.1,1.9),xytext=(0.3,1.9),arrowprops=a); ax.text(1.0,1.98,"τ",fontsize=8)
ax.annotate("",xy=(0.3,-0.3),xytext=(2.1,-0.3),arrowprops=a)
ax.annotate("",xy=(2.7,1.3),xytext=(2.7,0.3),arrowprops=a); ax.text(2.8,0.35,"τ = 20",fontsize=8)
ax.annotate("",xy=(-0.3,0.3),xytext=(-0.3,1.3),arrowprops=a)
ax.set_xlim(-1.3,3.9); ax.set_ylim(-0.9,2.5)
```

b) Draw the Mohr's circle diagram for plane strain and show on it the value of principal strains. [[5]]

@q 4
a) A thin cylindrical shell is 4 m long and has 2 m internal diameter and 14 mm metal thickness. Calculate the maximum intensity of shear produced and change in dimension of shell if it subjected to an internal pressure of 3 N/mm². Take E = 2×10$^5$ N/mm² and v = 0.3. [[4]]

b) Mention the physical meaning of torsional rigidity. A solid shaft transmits 250 kW at 100 rpm. If the shear stress is not to exceed 75 MPa, what should be the diameter of the shaft. Let the shaft be replaced by a hollow shaft whose internal is 0.6 times the outer diameter. Determine the size and percentage saving in weight if the maximum shear stress being the same. [[2+6]]

@q 5
A symmetrical I-section beam has 200 mm wide flanges and overall depth 500 mm. Each flange is 25 mm thick and the web is 20 mm thick. Determine (i) the maximum bending moment that should be imposed in the section if the tensile or the compressive stress is not exceed 40 N/mm² (ii) Determine the shear stress variation in this section. [[6+4]]

@q 6
Mention the limitations of Euler's formula for buckling. Derive the relation of crippling load for a long column with one end hinged and other end fixed. [[2+5]]

<!-- SOLUTIONS -->

@s 1
**(a) Extension of a uniformly tapering circular bar.**

```figure caption="Tapering bar of length ℓ: the diameter varies linearly from d$_1$ at the small end to d$_2$ at the large end. An elementary strip of thickness dx at distance x from the small end has diameter d$_x$."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.8,2.1)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(mp.Polygon([(0,-0.6),(6,-1.2),(6,1.2),(0,0.6)],closed=True,fc="#dbe7f5",ec=INK,lw=1))
ax.add_patch(mp.Polygon([(2.9,-0.9),(3.2,-0.915),(3.2,0.915),(2.9,0.9)],closed=True,fc="#f4d9a8",ec=INK,lw=0.8))
ax.annotate("",xy=(-1.2,0),xytext=(0,0),arrowprops=dict(arrowstyle="<|-",color=SERIES[1],lw=1.5)); ax.text(-1.25,0.2,"P",fontsize=9,color=SERIES[1])
ax.annotate("",xy=(7.2,0),xytext=(6,0),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1.5)); ax.text(7.0,0.2,"P",fontsize=9,color=SERIES[1])
ar=dict(arrowstyle="<->",color=INK,lw=0.8)
ax.annotate("",xy=(-0.2,-0.6),xytext=(-0.2,0.6),arrowprops=ar); ax.text(-0.75,-0.1,"d$_1$",fontsize=8)
ax.annotate("",xy=(6.25,-1.2),xytext=(6.25,1.2),arrowprops=ar); ax.text(6.35,-0.1,"d$_2$",fontsize=8)
ax.annotate("",xy=(0,-1.65),xytext=(6,-1.65),arrowprops=ar); ax.text(3,-1.95,"ℓ",ha="center",fontsize=8)
ax.annotate("",xy=(0,1.5),xytext=(3.05,1.5),arrowprops=ar); ax.text(1.5,1.62,"x",ha="center",fontsize=8); ax.text(3.0,1.15,"dx",fontsize=7)
ax.set_xlim(-1.5,7.8); ax.set_ylim(-2.2,2.0)
```

Let the diameter at distance $x$ from the small end be

$$\begin{gathered}d_x=d_1+\frac{d_2-d_1}{\ell}\,x=d_1+kx \\ k=\frac{d_2-d_1}{\ell}.\end{gathered}$$

The load $P$ is the same at every section, so the stress in the strip is $\sigma_x=\dfrac{P}{\frac{\pi}{4}d_x^2}=\dfrac{4P}{\pi d_x^2}$. The extension of the strip of length $dx$ is

$$d\delta=\frac{\sigma_x}{E}\,dx=\frac{4P}{\pi E}\frac{dx}{(d_1+kx)^2}.$$

Integrating over the length,

$$\delta=\frac{4P}{\pi E}\int_0^{\ell}\frac{dx}{(d_1+kx)^2}=\frac{4P}{\pi E}\left[-\frac{1}{k(d_1+kx)}\right]_0^{\ell}=\frac{4P}{\pi E k}\left(\frac{1}{d_1}-\frac{1}{d_2}\right).$$

Since $\dfrac1{d_1}-\dfrac1{d_2}=\dfrac{d_2-d_1}{d_1d_2}=\dfrac{k\ell}{d_1d_2}$,

$$\boxed{\delta=\frac{4P\,\ell}{\pi E\,d_1d_2}}$$

Check: for $d_1=d_2=d$ this gives $\delta=\dfrac{P\ell}{\frac{\pi}{4}d^2E}=\dfrac{P\ell}{AE}$, the extension of a prismatic bar.

**(b) Reinforced concrete column.**

$A_s=8\times\dfrac{\pi}{4}(20)^2=2513.27$ mm², $A_c=300\times300-A_s=87\,486.73$ mm², modular ratio $m=\dfrac{E_s}{E_c}=\dfrac{2.1\times10^5}{0.14\times10^5}=15$.

The steel and the concrete shorten equally ($\varepsilon_s=\varepsilon_c$), so $\sigma_s=m\,\sigma_c$. The load is shared: $P=\sigma_cA_c+\sigma_sA_s=\sigma_c\,(A_c+mA_s)$:

$$\sigma_c=\frac{360\times10^3}{87\,486.73+15(2513.27)}=\frac{360\times10^3}{125\,185.8}=\boxed{2.876\ \text{N/mm}^2}$$

$$\sigma_s=m\,\sigma_c=15(2.876)=\boxed{43.14\ \text{N/mm}^2}$$

Check: load on concrete $=2.876\times87\,486.7=251.6$ kN, load on steel $=43.14\times2513.27=108.4$ kN; $251.6+108.4=360$ kN ✓.

@s 2
**Parallel axis theorem.** The moment of inertia of an area about any axis in its plane is equal to the moment of inertia about the **parallel centroidal axis** plus the **product of the area and the square of the distance between the two axes**:

$$I_{AB}=I_G+A\,h^2 .$$

For the product of inertia, $I_{xy}=I_{\bar x\bar y}+A\,\bar x\,\bar y$ ($\bar x,\bar y$ = coordinates of the centroid of the part).

**The parts** (origin O at the lower left corner):

1. Right triangle (0,0), (70,0), (70,140): $A=\tfrac12(70)(140)=4900$ mm², centroid (46.67, 46.67).
2. Rectangle 70 × 70, from (70,0) to (140,70): $A=4900$ mm², centroid (105, 35).
3. Quarter disc, radius 70 mm, centre (70, 70), upper right quadrant: $A=\dfrac{\pi r^2}{4}=3848.45$ mm², centroid $(70+\tfrac{4r}{3\pi},\,70+\tfrac{4r}{3\pi})=(99.71,\,99.71)$.

**Moments about the axes through O.**

| Part | Area (mm²) | $\bar x$ | $\bar y$ | $I_x$ (mm⁴) | $I_y$ (mm⁴) | $I_{xy}$ (mm⁴) |
|---|---|---|---|---|---|---|
| 1 triangle | 4 900 | 46.67 | 46.67 | $16.007\times10^6$ | $12.005\times10^6$ | $12.005\times10^6$ |
| 2 rectangle | 4 900 | 105 | 35 | $8.003\times10^6$ | $56.023\times10^6$ | $18.008\times10^6$ |
| 3 quarter disc | 3 848.45 | 99.71 | 99.71 | $39.578\times10^6$ | $39.578\times10^6$ | $37.865\times10^6$ |
| **Total** | **13 648.45** | | | $63.588\times10^6$ | $107.607\times10^6$ | $67.878\times10^6$ |

Formulae used: triangle $I_x=\dfrac{bh^3}{12}=\dfrac{70(140)^3}{12}$, $I_y=\dfrac{hb^3}{4}$, and $I_{xy}=\displaystyle\int_0^{70}x\,\frac{(2x)^2}{2}\,dx=\frac{70^4}{2}$. Rectangle $I_x=\dfrac{bh^3}{3}$, $I_y=\dfrac{h(x_2^3-x_1^3)}{3}$, $I_{xy}=\dfrac{(x_2^2-x_1^2)}{2}\cdot\dfrac{h^2}{2}$. Quarter disc: about its own centroid $I_x=I_y=\left(\dfrac{\pi}{16}-\dfrac{4}{9\pi}\right)r^4=1.318\times10^6$ mm⁴ and $I_{xy}=\left(\dfrac18-\dfrac{4}{9\pi}\right)r^4=-0.3955\times10^6$ mm⁴, then the parallel axis theorem is applied to move to O.

**Centroid of the whole section.**

$$\begin{gathered}\bar X=\frac{4900(46.67)+4900(105)+3848.45(99.71)}{13\,648.45}=82.57\ \text{mm} \\ \bar Y=\frac{4900(46.67)+4900(35)+3848.45(99.71)}{13\,648.45}=57.43\ \text{mm}.\end{gathered}$$

**Centroidal moments.**

$$I_{\bar x}=63.588\times10^6-13\,648.45(57.43)^2=18.566\times10^6\ \text{mm}^4$$

$$I_{\bar y}=107.607\times10^6-13\,648.45(82.57)^2=14.564\times10^6\ \text{mm}^4$$

$$I_{\bar x\bar y}=67.878\times10^6-13\,648.45(82.57)(57.43)=3.155\times10^6\ \text{mm}^4$$

**Principal moments of inertia.**

$$I_{\max,\min}=\frac{I_{\bar x}+I_{\bar y}}{2}\pm\sqrt{\left(\frac{I_{\bar x}-I_{\bar y}}{2}\right)^2+I_{\bar x\bar y}^2}=16.565\times10^6\pm\sqrt{(2.001\times10^6)^2+(3.155\times10^6)^2}=16.565\times10^6\pm3.736\times10^6$$

$$\boxed{I_{\max}=20.30\times10^6\ \text{mm}^4,\qquad I_{\min}=12.83\times10^6\ \text{mm}^4}$$

**Orientation of the principal axes.**

$$\tan2\theta_p=\frac{-2I_{\bar x\bar y}}{I_{\bar x}-I_{\bar y}}=\frac{-6.311}{4.002}=-1.577\ \Rightarrow\ 2\theta_p=-57.62^\circ,\quad \boxed{\theta_p=-28.81^\circ}$$

The axis of $I_{\max}$ is inclined at $28.81^\circ$ **clockwise** from the centroidal $x$-axis, and the axis of $I_{\min}$ is perpendicular to it (at $61.19^\circ$ anticlockwise from the $x$-axis). Check: $I_{\theta}=16.565+2.001\cos(-57.62^\circ)-3.155\sin(-57.62^\circ)=16.565+1.072+2.664=20.30\times10^6$ ✓.

```figure caption="Centroid C (82.57, 57.43) and the principal axes of the section: I$_{max}$ = 20.30×10⁶ mm⁴ along the axis at 28.81° below the x-axis; I$_{min}$ = 12.83×10⁶ mm⁴ along the perpendicular axis."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.2,3.4)); ax.set_aspect("equal"); ax.axis("off")
fc="#e4ecf7"
ax.add_patch(mp.Polygon([(0,0),(70,0),(70,140)],closed=True,fc=fc,ec=INK,lw=0.9))
ax.add_patch(mp.Rectangle((70,0),70,70,fc=fc,ec=INK,lw=0.9))
t=_np.linspace(0,_np.pi/2,50)
ax.add_patch(mp.Polygon([(70,70)]+[(70+70*_np.cos(a),70+70*_np.sin(a)) for a in t],closed=True,fc=fc,ec=INK,lw=0.9))
cx,cy=82.57,57.43
ax.plot([cx-90,cx+90],[cy,cy],color=MUTED,lw=0.8,ls="--"); ax.plot([cx,cx],[cy-70,cy+100],color=MUTED,lw=0.8,ls="--")
th=_np.radians(-28.81); L=85
ax.plot([cx-L*_np.cos(th),cx+L*_np.cos(th)],[cy-L*_np.sin(th),cy+L*_np.sin(th)],color=SERIES[1],lw=1.6)
ax.plot([cx-L*0.9*_np.sin(th),cx+L*0.9*_np.sin(th)],[cy+L*0.9*_np.cos(th),cy-L*0.9*_np.cos(th)],color=SERIES[2],lw=1.6)
ax.plot([cx],[cy],"o",color=INK,ms=4); ax.text(cx+4,cy+5,"C",fontsize=8)
ax.add_patch(mp.Arc((cx,cy),60,60,theta1=-28.81,theta2=0,color=INK,lw=0.8)); ax.text(cx+32,cy-12,"28.81°",fontsize=7)
ax.text(cx+L*_np.cos(th)+3,cy+L*_np.sin(th)-6,"I$_{max}$",fontsize=8,color=SERIES[1])
ax.text(cx-L*0.9*_np.sin(th)-6,cy+L*0.9*_np.cos(th)+4,"I$_{min}$",fontsize=8,color=SERIES[2])
ax.set_xlim(-10,190); ax.set_ylim(-25,160)
```

@s 3
**(a) Biaxial stress with shear.** From the figure: $\sigma_x=+75$ N/mm² (tension), $\sigma_y=-40$ N/mm² (compression; the arrows push on the top and bottom faces) and $\tau_{xy}=+20$ N/mm².

$$\begin{gathered}\frac{\sigma_x+\sigma_y}{2}=17.5 \\ \frac{\sigma_x-\sigma_y}{2}=57.5 \\ R=\sqrt{57.5^2+20^2}=60.88 .\end{gathered}$$

**Principal stresses.**

$$\boxed{\sigma_1=17.5+60.88=78.38\ \text{N/mm}^2\ (\text{tensile}),\qquad \sigma_2=17.5-60.88=-43.38\ \text{N/mm}^2\ (\text{compressive})}$$

**Orientation of the principal planes.**

$$\tan2\theta_p=\frac{2\tau_{xy}}{\sigma_x-\sigma_y}=\frac{40}{115}=0.3478\ \Rightarrow\ 2\theta_p=19.18^\circ,\quad \boxed{\theta_p=9.59^\circ\ \ \text{and}\ \ 99.59^\circ}$$

The plane of $\sigma_1$ (78.38) has its normal at $9.59^\circ$ anticlockwise from the $x$-axis and the plane of $\sigma_2$ (−43.38) at $99.59^\circ$.

**Maximum shear stress.**

$$\boxed{\tau_{\max}=\frac{\sigma_1-\sigma_2}{2}=R=60.88\ \text{N/mm}^2}$$

on the planes at $\theta_s=\theta_p\pm45^\circ=54.59^\circ$ and $144.59^\circ$.

**Resultant stress on the plane of maximum shear.** On that plane the normal stress is $\sigma_n=\dfrac{\sigma_1+\sigma_2}{2}=17.5$ N/mm² (tensile) and the shear stress is $60.88$ N/mm², so

$$\sigma_R=\sqrt{\sigma_n^2+\tau_{\max}^2}=\sqrt{17.5^2+60.88^2}=\boxed{63.34\ \text{N/mm}^2}$$

inclined to the normal of the plane at $\phi=\tan^{-1}\dfrac{60.88}{17.5}=73.96^\circ$.

```figure caption="Mohr's circle for Question 3(a) (stresses in N/mm², shear positive when it tends to turn the element clockwise): centre (17.5, 0), radius 60.88. X (75, −20), Y (−40, 20); principal stresses 78.38 and −43.38; maximum shear ±60.88 at σ = 17.5."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.5))
c,R=17.5,60.88
t=_np.linspace(0,2*_np.pi,300); ax.plot(c+R*_np.cos(t),R*_np.sin(t),color=ACCENT,lw=1.4)
ax.axhline(0,color=MUTED,lw=0.8); ax.axvline(0,color=MUTED,lw=0.8)
X=(75,-20); Y=(-40,20)
ax.plot([X[0],Y[0]],[X[1],Y[1]],color=INK,lw=1)
ax.plot([c,c],[-R,R],color=SERIES[1],lw=1,ls="--")
for p,l,dx,dy in ((X,"X (75, −20)",3,-9),(Y,"Y (−40, 20)",-44,6),((78.38,0),"σ₁ = 78.38",-6,5),((-43.38,0),"σ₂ = −43.38",-30,-12),((c,R),"τmax = 60.88",3,3),((c,0),"C",2,-9)):
    ax.plot(*p,"o",color=INK,ms=3.5); ax.text(p[0]+dx,p[1]+dy,l,fontsize=7)
ax.add_patch(mp.Arc((c,0),50,50,theta1=-9.59*2,theta2=0,color=INK,lw=0.8)); ax.text(c+27,-14,"2θ$_p$",fontsize=7)
ax.set_aspect("equal"); ax.set_xlabel("σ (N/mm²)"); ax.set_ylabel("τ (clockwise +)")
ax.set_xlim(-60,100); ax.set_ylim(-70,72)
```

**(b) Mohr's circle for plane strain.**

*Construction.* Plot the **normal strain $\varepsilon$ on the horizontal axis** and **half the shear strain $\gamma/2$ on the vertical axis** (the shear drawn positive downward for the clockwise convention). The state of strain is $\varepsilon_x,\ \varepsilon_y,\ \gamma_{xy}$.

1. Plot X $\left(\varepsilon_x,\ +\dfrac{\gamma_{xy}}{2}\right)$ and Y $\left(\varepsilon_y,\ -\dfrac{\gamma_{xy}}{2}\right)$.
2. Join X and Y; the line cuts the $\varepsilon$-axis at the centre C, with $OC=\dfrac{\varepsilon_x+\varepsilon_y}{2}$.
3. Draw the circle with centre C and radius

$$R=\sqrt{\left(\frac{\varepsilon_x-\varepsilon_y}{2}\right)^2+\left(\frac{\gamma_{xy}}{2}\right)^2}.$$

4. The circle meets the $\varepsilon$-axis at the **principal strains**:

$$\begin{gathered}\varepsilon_1=\frac{\varepsilon_x+\varepsilon_y}{2}+R \\ \varepsilon_2=\frac{\varepsilon_x+\varepsilon_y}{2}-R .\end{gathered}$$

5. The angle $\angle XC\varepsilon_1=2\theta_p$ with $\tan2\theta_p=\dfrac{\gamma_{xy}}{\varepsilon_x-\varepsilon_y}$ gives the principal directions (rotate by $\theta_p$ on the element in the same sense as the $2\theta_p$ on the circle).
6. The top and bottom points of the circle give the maximum shear strain, $\dfrac{\gamma_{\max}}{2}=R$, i.e. $\gamma_{\max}=\varepsilon_1-\varepsilon_2$, at a normal strain $\dfrac{\varepsilon_x+\varepsilon_y}{2}$.

```figure caption="Mohr's circle for plane strain: ε on the horizontal axis and γ/2 on the vertical axis. The principal strains ε$_1$ and ε$_2$ are where the circle cuts the ε-axis; X and Y represent the x- and y-directions."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.6,3.3)); ax.axis("off")
c,R=4.0,3.0
t=_np.linspace(0,2*_np.pi,300); ax.plot(c+R*_np.cos(t),R*_np.sin(t),color=ACCENT,lw=1.5)
ax.annotate("",xy=(9.2,0),xytext=(-1.0,0),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1)); ax.text(9.0,-0.45,"ε",fontsize=9)
ax.annotate("",xy=(0,3.9),xytext=(0,-3.7),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1)); ax.text(0.15,3.7,"γ/2",fontsize=9)
th=_np.radians(-52); ex=(c+R*_np.cos(th),R*_np.sin(th)); ey=(c-R*_np.cos(th),-R*_np.sin(th))
ax.plot([ex[0],ey[0]],[ex[1],ey[1]],color=INK,lw=1)
ax.plot([c,c],[-R,R],color=MUTED,lw=0.7,ls="--")
pts=[(ex,"X (ε$_x$, γ$_{xy}$/2)",0.1,-0.4),(ey,"Y (ε$_y$, −γ$_{xy}$/2)",-2.6,0.2),((c+R,0),"ε$_1$",0.15,0.2),((c-R,0),"ε$_2$",-0.55,0.2),((c,0),"C",0.1,-0.45),((c,R),"γ$_{max}$/2",0.15,0.1)]
for p,l,dx,dy in pts:
    ax.plot(*p,"o",color=INK,ms=3.5); ax.text(p[0]+dx,p[1]+dy,l,fontsize=7.5)
ax.add_patch(mp.Arc((c,0),2.2,2.2,theta1=-52,theta2=0,color=INK,lw=0.8)); ax.text(c+1.3,-0.6,"2θ$_p$",fontsize=7.5)
ax.text(c-0.7,-3.55,"R",fontsize=8,color=SERIES[1]); ax.plot([c,ex[0]],[0,ex[1]],color=SERIES[1],lw=0.9)
ax.set_xlim(-1.4,9.6); ax.set_ylim(-3.9,4.1); ax.set_aspect("equal")
```

@s 4
**(a) Thin cylindrical shell.** $d=2000$ mm, $t=14$ mm, $\ell=4000$ mm, $p=3$ N/mm², $E=2\times10^5$ N/mm², $\nu=0.3$.

$$\begin{gathered}\sigma_h=\frac{pd}{2t}=\frac{3(2000)}{2(14)}=214.29\ \text{N/mm}^2 \\ \sigma_l=\frac{pd}{4t}=107.14\ \text{N/mm}^2 .\end{gathered}$$

**Maximum shear stress.** The in-plane maximum shear stress (the radial stress is neglected in a thin shell) is

$$\tau_{\max}=\frac{\sigma_h-\sigma_l}{2}=\frac{pd}{8t}=\frac{3(2000)}{8(14)}=\boxed{53.57\ \text{N/mm}^2}$$

(The absolute maximum shear stress, including the zero radial stress, would be $\sigma_h/2=107.14$ N/mm².)

**Strains and changes in dimensions.**

$$\begin{gathered}\varepsilon_h=\frac{1}{E}(\sigma_h-\nu\sigma_l)=\frac{214.29-0.3(107.14)}{2\times10^5}=9.107\times10^{-4} \\ \varepsilon_l=\frac{1}{E}(\sigma_l-\nu\sigma_h)=\frac{107.14-0.3(214.29)}{2\times10^5}=2.143\times10^{-4}.\end{gathered}$$

$$\boxed{\delta d=\varepsilon_h\,d=9.107\times10^{-4}\times2000=1.82\ \text{mm (increase in diameter)}}$$

$$\boxed{\delta\ell=\varepsilon_l\,\ell=2.143\times10^{-4}\times4000=0.857\ \text{mm (increase in length)}}$$

Volumetric strain $\varepsilon_v=2\varepsilon_h+\varepsilon_l=2.036\times10^{-3}$, with $V=\dfrac{\pi}{4}(2000)^2(4000)=1.2566\times10^{10}$ mm³, so $\delta V=2.56\times10^{7}$ mm³ (25.6 litres).

**(b) Torsional rigidity.** The torsional rigidity is the product $GJ$ of the modulus of rigidity and the polar moment of inertia. Physically, it is the **torque required to produce a twist of one radian per unit length** of the shaft ($T=GJ\,\theta/\ell$, so $GJ=T\ell/\theta$): it measures the shaft's resistance to twisting. A larger $GJ$ means a stiffer shaft.

**Solid shaft.** $P=250$ kW, $N=100$ rpm, $\tau=75$ N/mm²:

$$T=\frac{P}{\omega}=\frac{250\times10^3}{2\pi(100)/60}=23\,873\ \text{N·m}=23.873\times10^6\ \text{N·mm}.$$

$$T=\frac{\pi}{16}\tau d^3\ \Rightarrow\ d^3=\frac{16(23.873\times10^6)}{\pi(75)}=1.621\times10^6\ \Rightarrow\ \boxed{d=117.5\ \text{mm}\ (\text{say }120\ \text{mm})}$$

**Hollow shaft** with $d_i=0.6D$ and the same maximum shear stress (same torque): $T=\dfrac{\pi}{16}\tau D^3(1-k^4)$ with $k=0.6$, $k^4=0.1296$:

$$D^3=\frac{16(23.873\times10^6)}{\pi(75)(0.8704)}=1.8627\times10^6\ \Rightarrow\ \boxed{D=123.0\ \text{mm},\qquad d_i=0.6D=73.8\ \text{mm}}$$

**Saving in weight** (same material and length, so weight is proportional to area):

$$\begin{gathered}\frac{W_h}{W_s}=\frac{D^2(1-k^2)}{d^2}=\frac{(123.04)^2(0.64)}{(117.47)^2}=0.702 \\ \text{saving}=1-0.702=\boxed{29.8\ \%}\end{gathered}$$

@s 5
**I-section:** $B=200$, $D=500$, $t_f=25$, $t_w=20$ (mm). The section is symmetrical, so the neutral axis is at mid-depth, $y_{\max}=250$ mm.

$$I=\frac{BD^3-(B-t_w)(D-2t_f)^3}{12}=\frac{200(500)^3-180(450)^3}{12}=\frac{25\times10^9-16.4025\times10^9}{12}=716.46\times10^6\ \text{mm}^4 .$$

**(i) Maximum bending moment.** $\sigma_{\max}=\dfrac{M\,y_{\max}}{I}\le40$ N/mm²:

$$M_{\max}=\frac{\sigma I}{y_{\max}}=\frac{40(716.46\times10^6)}{250}=114.63\times10^6\ \text{N·mm}=\boxed{114.6\ \text{kN·m}}$$

**(ii) Shear stress variation.** For a shear force $F$ the shear stress at a level is $\tau=\dfrac{F\,A\bar y}{I\,b}$, where $A\bar y$ is the first moment of the area above the level about the neutral axis and $b$ the width there.

*In the flange* (width 200 mm), at a distance $y$ from the neutral axis ($225\le y\le250$): $A\bar y=200(250-y)\,\dfrac{250+y}{2}=100(250^2-y^2)$, a parabola:

- at the top edge ($y=250$): $\tau=0$;
- at the bottom of the flange ($y=225$): $A\bar y=200(25)(237.5)=1.1875\times10^6$ mm³, so $\tau=\dfrac{F(1.1875\times10^6)}{716.46\times10^6(200)}=8.29\times10^{-6}F$.

*In the web* (width 20 mm), at a distance $y$ ($0\le y\le225$): $A\bar y=1.1875\times10^6+\dfrac{20}{2}(225^2-y^2)$ mm³, again a parabola:

- at the top of the web ($y=225$): $\tau=\dfrac{F(1.1875\times10^6)}{716.46\times10^6(20)}=8.29\times10^{-5}F$ (**10 times** the value just inside the flange, because the width drops from 200 to 20 mm);
- at $y=100$ mm: $A\bar y=1.59375\times10^6$, $\tau=1.112\times10^{-4}F$;
- at the neutral axis ($y=0$): $A\bar y=1.69375\times10^6$ mm³, $\tau_{\max}=\dfrac{F(1.69375\times10^6)}{716.46\times10^6(20)}=1.182\times10^{-4}F$.

With $F$ in newtons and $\tau$ in N/mm²:

| Level | Width (mm) | $\tau$ (N/mm²) |
|---|---|---|
| top edge of the flange | 200 | 0 |
| flange, at the junction | 200 | $8.29\times10^{-6}F$ |
| web, at the junction | 20 | $8.29\times10^{-5}F$ |
| web, 100 mm from N.A. | 20 | $1.112\times10^{-4}F$ |
| neutral axis | 20 | $1.182\times10^{-4}F$ (maximum) |

For example, for $F=100$ kN: $\tau_{\text{flange junction}}=0.83$, $\tau_{\text{web junction}}=8.29$ and $\tau_{\max}=11.82$ N/mm². The web carries almost all the shear (the average stress over the web area $20\times500$ is $F/10^4=1.0\times10^{-4}F$, within 15 % of the maximum), and $\tau_{\max}/\tau_{\text{avg}}\approx1.18$.

```figure caption="Shear stress distribution in the I-section (values per newton of shear force F, in units of 10⁻⁶ N/mm²): it is parabolic in the web, with the maximum at the neutral axis, and falls to a small value in the flanges because of their large width."
import numpy as _np, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.4,3.2)); ax.set_aspect("equal"); ax.axis("off")
sc=1/1.6
ax.add_patch(mp.Rectangle((-100,225),200,25,fc="#dbe7f5",ec=INK,lw=1)); ax.add_patch(mp.Rectangle((-100,-250),200,25,fc="#dbe7f5",ec=INK,lw=1)); ax.add_patch(mp.Rectangle((-10,-225),20,450,fc="#dbe7f5",ec=INK,lw=1))
ax.plot([-130,150],[0,0],color=SERIES[1],lw=0.9,ls="--"); ax.text(-170,8,"N.A.",fontsize=7,color=SERIES[1])
x0=150
yy=_np.linspace(225,0,50); tw=(1.1875e6+10*(225**2-yy**2))/(716.46e6*20)*1e6
fl=_np.linspace(250,225,20); tf=(100*(250**2-fl**2))/(716.46e6*200)*1e6
ys=list(fl)+list(yy); xs=[x0+0.9*v for v in list(tf)+list(tw)]
ax.plot(xs,ys,color=SERIES[1],lw=1.4); ax.plot(xs,[-v for v in ys],color=SERIES[1],lw=1.4)
ax.plot([x0,x0],[-250,250],color=INK,lw=0.8)
ax.text(x0+0.9*118.2+4,-4,"118.2",fontsize=7); ax.text(x0+0.9*82.9+4,215,"82.9",fontsize=7); ax.text(x0+8,258,"0 at the top edge",fontsize=6.5)
ax.set_xlim(-190,310); ax.set_ylim(-275,285)
```

@s 6
**Limitations of Euler's formula.**

1. It applies only to **long (slender) columns**. The critical stress $\sigma_{cr}=\dfrac{\pi^2E}{\lambda^2}$ ($\lambda=\ell_e/r$, the slenderness ratio) must not exceed the proportional limit; for mild steel this means $\lambda\gtrsim 90$ to 100. For short and intermediate columns it gives a stress above the yield point, so a different formula (Rankine, Johnson, a straight-line formula) is used.
2. It assumes an **initially perfectly straight column of uniform section** and a load applied **exactly along the axis**; in practice, crookedness and accidental eccentricity lower the real buckling load.
3. The **material is homogeneous, isotropic and elastic** (obeys Hooke's law), the same in tension and compression.
4. The **direct compressive stress and the shear deformation are neglected**; only the bending effect is considered.
5. The **end conditions are assumed ideal** (perfectly hinged or perfectly fixed); real supports are partly restrained.
6. The **self-weight** of the column is ignored, and failure is assumed to be only by buckling (no local buckling, no creep).

**Crippling load for a column with one end hinged and the other fixed.**

Let the column of length $L$ be fixed at A and hinged at B, carrying the axial load $P$ (crippling load). Take the origin at the hinged end B, $x$ along the column and $y$ the lateral deflection. The hinge needs a horizontal reaction $H$ (the fixed end then has the fixing moment $M_A=HL$). The bending moment at a section at distance $x$ from B is $Py-Hx$, so

$$\begin{gathered}EI\frac{d^2y}{dx^2}=-Py+Hx\quad\Rightarrow\quad\frac{d^2y}{dx^2}+\alpha^2y=\frac{H}{EI}x \\ \alpha^2=\frac{P}{EI}.\end{gathered}$$

Solution:

$$y=A\cos\alpha x+B\sin\alpha x+\frac{H}{P}x .$$

*Boundary conditions.*

1. $x=0,\ y=0$ gives $A=0$.
2. $x=L,\ y=0$ gives $B\sin\alpha L+\dfrac{H}{P}L=0$.
3. $x=L,\ \dfrac{dy}{dx}=0$ (fixed end) gives $B\alpha\cos\alpha L+\dfrac{H}{P}=0$.

Eliminating $B$ and $H$ from (2) and (3):

$$\tan\alpha L=\alpha L .$$

The smallest non-zero root is $\alpha L=4.4934$ rad (a little less than $3\pi/2$). Therefore

$$P_{cr}=\alpha^2EI=\frac{(4.4934)^2EI}{L^2}=\frac{20.19\,EI}{L^2}\approx\boxed{\frac{2\pi^2EI}{L^2}}=\frac{\pi^2EI}{(L/\sqrt2)^2}$$

so that the equivalent (effective) length of the column is $L_e=\dfrac{L}{\sqrt2}\approx0.7L$. The corresponding crippling stress is $\sigma_{cr}=\dfrac{P_{cr}}{A}=\dfrac{2\pi^2E}{\lambda^2}$ with $\lambda=L/r$. For comparison, the hinged-hinged column has $P_{cr}=\pi^2EI/L^2$ ($L_e=L$), the fixed-fixed column $4\pi^2EI/L^2$ ($L_e=L/2$) and the fixed-free column $\pi^2EI/4L^2$ ($L_e=2L$).

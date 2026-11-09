---
file: NEBians-IOE-Past-Paper-Electromagnetics-ENEX254-2083-Baishakh.pdf
subject: Electromagnetics
level: BE · Year II / Part II
code: ENEX 254
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Necessary formula sheet is attached (curl, divergence, gradient and Laplacian in the three co-ordinate systems) · Assume suitable data if necessary</small>

@q 1
Given the points $C(-3, 2, 1)$ and $D(r = 5,\ \theta = 20^\circ,\ \phi = -70^\circ)$, express the distance vector from $C$ to $D$ in the spherical co-ordinate system at $D$. [[5]]

@q 2
State Gauss's law. A uniform line charge density of $5$ nC/m is at $y = 0,\ z = 2$ m in free space, while $-5$ nC/m is located at $y = 0,\ z = -2$ m. A uniform surface charge density of $0.3$ nC/m$^2$ is at $y = 0.2$ m and $-0.3$ nC/m$^2$ is at $y = -0.2$ m. Find $|\vec E|$ at the origin. [[1+5]]

@q 3
Derive the expression for electric boundary conditions between two perfect dielectric materials. [[5]]

@q 4
A dipole of moment $\vec p = 6\,\hat a_z$ nC·m is located at the origin in free space. (a) Find $V$ at $P(r = 4,\ \theta = 20^\circ,\ \phi = 0^\circ)$. (b) Find $\vec E$ at $P$. [[2+2]]

@q 5
Can the scalar magnetic potential be defined similar to the scalar electric potential? Explain. If $\vec A = x^2 y\,\hat a_x + x y^2\,\hat a_y - 4xyz\,\hat a_z$ Wb/m, determine the total magnetic flux crossing the surface $z = 1,\ 0 < x < 1,\ -1 < y < 4$. [[3+3]]

@q 6
Using the concept of vector magnetic potential, derive the expression for magnetic field intensity due to an infinitely long filament carrying current $I$. [[6]]

@q 7
Explain the significance of curl with an example. Evaluate both sides of Stokes' theorem for the field $\vec H = 4xy\,\hat a_x - 2y^2\,\hat a_y$ A/m and the rectangular path around the region $3 \le x \le 6,\ -2 \le y \le 2,\ z = 0$. Let the positive direction of $d\vec S$ be $\hat a_z$. [[2+4]]

@q 8
Explain motional emf with the necessary derivations. List out Maxwell's equations in point form for time-varying fields. [[3+3]]

@q 9
Explain a uniform plane wave. Derive the equation of an EM wave when travelling in a lossy dielectric medium. [[2+4]]

@q 10
An $\vec H$ field in free space is given as $\vec H(x, t) = 10\cos(10^8 t - \beta x)\,\hat a_y$ A/m. Find (a) $\omega$ (b) $\beta$ (c) $\lambda$ (d) $\vec E(x, t)$ at $P(0.1, 0.2, 0.3)$ at $t = 1$ ns. [[1+1+1+3]]

@q 11
A distortionless line has a characteristic impedance of $50\ \Omega$, an attenuation constant of $22$ mNp/m and a phase velocity of $2 \times 10^8$ m/s. Determine the line parameters $R, L, C$ and $G$ at $300$ MHz. [[4]]

<!-- SOLUTIONS -->

@s 1
The distance vector from $C$ to $D$ is $\vec R_{CD} = \vec r_D - \vec r_C$. First change $D$ to Cartesian co-ordinates.

$$\begin{gathered} x = r\sin\theta\cos\phi = 5\sin 20^\circ\cos(-70^\circ) = 0.585 \\ y = r\sin\theta\sin\phi = 5\sin 20^\circ\sin(-70^\circ) = -1.607 \\ z = r\cos\theta = 5\cos 20^\circ = 4.698 \end{gathered}$$

$$\vec R_{CD} = (0.585 + 3)\,\hat a_x + (-1.607 - 2)\,\hat a_y + (4.698 - 1)\,\hat a_z = 3.585\,\hat a_x - 3.607\,\hat a_y + 3.698\,\hat a_z$$

To express it in spherical components **at D** use the unit vectors at $D$ ($\theta = 20^\circ,\ \phi = -70^\circ$):

$$\begin{gathered} \hat a_r = (\sin\theta\cos\phi,\ \sin\theta\sin\phi,\ \cos\theta) = (0.1170,\ -0.3214,\ 0.9397) \\ \hat a_\theta = (\cos\theta\cos\phi,\ \cos\theta\sin\phi,\ -\sin\theta) = (0.3214,\ -0.8830,\ -0.3420) \\ \hat a_\phi = (-\sin\phi,\ \cos\phi,\ 0) = (0.9397,\ 0.3420,\ 0) \end{gathered}$$

The spherical components are the dot products of $\vec R_{CD}$ with these unit vectors:

$$\begin{aligned} R_r &= 3.585(0.1170) + (-3.607)(-0.3214) + 3.698(0.9397) = 5.054 \\ R_\theta &= 3.585(0.3214) + (-3.607)(-0.8830) + 3.698(-0.3420) = 3.072 \\ R_\phi &= 3.585(0.9397) + (-3.607)(0.3420) + 0 = 2.135 \end{aligned}$$

$$\boxed{\vec R_{CD} = 5.05\,\hat a_r + 3.07\,\hat a_\theta + 2.14\,\hat a_\phi}$$

Check: $|\vec R| = \sqrt{5.054^2 + 3.072^2 + 2.135^2} = 6.288 = \sqrt{3.585^2 + 3.607^2 + 3.698^2}$. ✓.

@s 2
**Gauss's law.** The net electric flux through any closed surface equals the total charge enclosed by it:

$$\begin{gathered}\oint_S \vec D\cdot d\vec S = Q_{enc} \\ \text{(point form: } \nabla\cdot\vec D = \rho_v\text{)}\end{gathered}$$

Use superposition at the origin, with $\epsilon_0 = 8.854\times10^{-12}$ F/m.

**Line charges** (both parallel to the $x$-axis). A line charge gives $\vec E = \dfrac{\rho_L}{2\pi\epsilon_0\rho}\hat a_\rho$, directed away from a positive line and towards a negative one.

- $+5$ nC/m at $z = 2$: the origin is $\rho = 2$ m below it, so $\vec E_1 = \dfrac{5\times10^{-9}}{2\pi\epsilon_0(2)}(-\hat a_z) = -44.94\,\hat a_z$ V/m.
- $-5$ nC/m at $z = -2$: the field points towards the line, i.e. again in $-\hat a_z$, so $\vec E_2 = -44.94\,\hat a_z$ V/m.

$$\vec E_{lines} = -89.88\,\hat a_z \text{ V/m}$$

**Sheets** (planes $y = \pm0.2$). An infinite sheet gives $|\vec E| = \dfrac{\rho_s}{2\epsilon_0} = \dfrac{0.3\times10^{-9}}{2\epsilon_0} = 16.94$ V/m.

- $+0.3$ nC/m$^2$ at $y = 0.2$: the origin is on its $y < 0.2$ side, so the field points away from the sheet: $-16.94\,\hat a_y$.
- $-0.3$ nC/m$^2$ at $y = -0.2$: the origin lies at $y > -0.2$ and the field points towards the sheet: $-16.94\,\hat a_y$.

$$\vec E_{sheets} = -33.88\,\hat a_y \text{ V/m}$$

$$\begin{gathered}\vec E_{total} = -33.88\,\hat a_y - 89.88\,\hat a_z \text{ V/m} \\ \boxed{|\vec E| = \sqrt{33.88^2 + 89.88^2} = 96.05 \text{ V/m}}\end{gathered}$$

@s 3
Consider the interface between dielectric 1 (permittivity $\epsilon_1$) and dielectric 2 ($\epsilon_2$). Perfect dielectrics carry no free surface charge ($\rho_s = 0$) and no free charge moves. Split every field into a component tangential ($t$) and normal ($n$) to the interface.

```figure caption="Boundary between two dielectrics. Left: the closed rectangular path abcd (width Δw, height Δh → 0) used for the tangential component. Right: the small cylindrical pillbox (top and bottom area ΔS, height Δh → 0) used for the normal component."
fig,(a,b)=plt.subplots(1,2,figsize=(7.2,2.9))
for z in (a,b):
    z.axis("off"); z.set_xlim(0,6); z.set_ylim(0,4)
    z.fill_between([0,6],2,4,color="#eaf3ff"); z.fill_between([0,6],0,2,color="#fff4d6")
    z.plot([0,6],[2,2],color=INK,lw=1.4)
    z.text(0.15,3.6,r"medium 1 ($\epsilon_1$)",fontsize=8); z.text(0.15,0.25,r"medium 2 ($\epsilon_2$)",fontsize=8)
def A(z,p,q,c=ACCENT,lw=1.4): z.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="-|>",color=c,lw=lw))
a.set_title("Tangential component",fontsize=8.5)
a.plot([1.7,4.3,4.3,1.7,1.7],[1.35,1.35,2.65,2.65,1.35],color=INK,lw=1.2)
A(a,(2.3,1.35),(3.2,1.35)); A(a,(3.6,2.65),(2.7,2.65))
a.text(1.55,1.1,"a",fontsize=8); a.text(4.4,1.1,"b",fontsize=8); a.text(4.4,2.75,"c",fontsize=8); a.text(1.55,2.75,"d",fontsize=8)
a.text(3.0,3.05,r"$E_{t1}$",fontsize=9,ha="center",color=ACCENT); a.text(3.0,0.85,r"$E_{t2}$",fontsize=9,ha="center",color=ACCENT)
a.annotate("",xy=(4.3,0.55),xytext=(1.7,0.55),arrowprops=dict(arrowstyle="<->",color=MUTED,lw=0.9)); a.text(3.0,0.62,r"$\Delta w$",fontsize=8,ha="center",color=MUTED,va="bottom")
b.set_title("Normal component",fontsize=8.5)
b.plot([1.7,4.3,4.3,1.7,1.7],[1.35,1.35,2.65,2.65,1.35],color=INK,lw=1.2,ls="--")
A(b,(3.0,2.65),(3.0,3.55)); A(b,(3.0,1.35),(3.0,0.45),c="#d9534f")
b.text(3.15,3.3,r"$D_{n1}$",fontsize=9,color=ACCENT); b.text(3.15,0.7,r"$D_{n2}$",fontsize=9,color="#d9534f")
A(b,(2.2,2.0),(2.2,2.5),c=INK,lw=1); b.text(2.0,2.35,r"$\hat a_n$",fontsize=8.5,ha="right")
```

**1. Tangential component of E.** In electrostatics $\oint \vec E\cdot d\vec l = 0$. Take the thin rectangle $abcd$ with $ab$ and $cd$ (length $\Delta w$) parallel to the surface, one on each side, and the short sides $\Delta h \to 0$ (their contribution vanishes):

$$\oint \vec E\cdot d\vec l = E_{t2}\,\Delta w - E_{t1}\,\Delta w = 0$$

$$\begin{gathered}\boxed{E_{t1} = E_{t2}} \\ \Longrightarrow \\ \frac{D_{t1}}{\epsilon_1} = \frac{D_{t2}}{\epsilon_2}\end{gathered}$$

The tangential component of $\vec E$ is continuous across the boundary; the tangential component of $\vec D$ is not.

**2. Normal component of D.** Apply Gauss's law to the pillbox with $\Delta h \to 0$, so only the top and bottom faces contribute (normal $\hat a_n$ pointing from 2 into 1):

$$\oint \vec D\cdot d\vec S = D_{n1}\Delta S - D_{n2}\Delta S = Q_{enc} = \rho_s\,\Delta S$$

$$\begin{gathered}D_{n1} - D_{n2} = \rho_s = 0 \quad\Longrightarrow\quad \boxed{D_{n1} = D_{n2}} \\ \Longleftrightarrow \\ \epsilon_1 E_{n1} = \epsilon_2 E_{n2}\end{gathered}$$

The normal component of $\vec D$ is continuous, and the normal component of $\vec E$ is discontinuous (jumps by the ratio $\epsilon_2/\epsilon_1$).

**3. Law of refraction.** If $\vec E_1$ and $\vec E_2$ make angles $\theta_1$ and $\theta_2$ with the normal, then $E_1\sin\theta_1 = E_2\sin\theta_2$ and $\epsilon_1E_1\cos\theta_1 = \epsilon_2E_2\cos\theta_2$. Dividing,

$$\frac{\tan\theta_1}{\tan\theta_2} = \frac{\epsilon_1}{\epsilon_2} = \frac{\epsilon_{r1}}{\epsilon_{r2}}$$

@s 4
For a point dipole at the origin, with $\vec p = p\,\hat a_z$, $p = 6$ nC·m, $r = 4$ m, $\theta = 20^\circ$ and $\dfrac{1}{4\pi\epsilon_0} = 8.988\times10^{9}$.

**(a)** The potential is

$$V = \frac{\vec p\cdot\hat a_r}{4\pi\epsilon_0 r^2} = \frac{p\cos\theta}{4\pi\epsilon_0 r^2} = \frac{(8.988\times10^{9})(6\times10^{-9})\cos 20^\circ}{4^2} = \frac{50.67}{16}$$

$$\boxed{V = 3.17 \text{ V}}$$

**(b)** The electric field is $\vec E = -\nabla V$, which for the dipole becomes

$$\begin{gathered}\vec E = \frac{p}{4\pi\epsilon_0 r^3}\left(2\cos\theta\,\hat a_r + \sin\theta\,\hat a_\theta\right) \\ \frac{p}{4\pi\epsilon_0 r^3} = \frac{53.93}{64} = 0.8426\end{gathered}$$

$$\vec E = 0.8426\,(2\cos20^\circ\,\hat a_r + \sin 20^\circ\,\hat a_\theta) = 0.8426\,(1.879\,\hat a_r + 0.342\,\hat a_\theta)$$

$$\begin{gathered}\boxed{\vec E = 1.584\,\hat a_r + 0.288\,\hat a_\theta \text{ V/m}} \\ |\vec E| = 1.61 \text{ V/m}\end{gathered}$$

@s 5
**Scalar magnetic potential.** In electrostatics $\nabla\times\vec E = 0$ everywhere, so $\vec E = -\nabla V$ with a single-valued $V$. For magnetostatics $\nabla\times\vec H = \vec J$. Since $\nabla\times(\nabla V_m) \equiv 0$, we can write

$$\vec H = -\nabla V_m \quad\text{only where } \vec J = 0$$

So **yes, but only in a current-free region**, and with two differences from $V$:

1. $\nabla\times\vec H = \vec J \neq 0$ at the conductor, so $V_m$ cannot be defined inside the current-carrying region (in the free-space region it satisfies $\nabla^2 V_m = 0$ because $\nabla\cdot\vec B = 0$).
2. $V_m$ is **multi-valued**: a closed path around the current gives $\oint\vec H\cdot d\vec l = I \ne 0$, so each loop around the wire adds $I$ to $V_m$ (a "barrier surface" must be introduced to make it single valued). Also, the unit of $V_m$ is the ampere, not the volt, and $V_m$ has no work interpretation.

For this reason the vector magnetic potential $\vec A$ ($\vec B = \nabla\times\vec A$), which exists everywhere, is used in general.

**Flux through the surface.** $\vec B = \nabla\times\vec A$. On $z = 1$ the normal is $\hat a_z$, so only $B_z$ is needed:

$$B_z = \frac{\partial A_y}{\partial x} - \frac{\partial A_x}{\partial y} = y^2 - x^2$$

$$\Phi = \int_{x=0}^{1}\int_{y=-1}^{4}(y^2 - x^2)\,dy\,dx = \int_0^1\left[\frac{y^3}{3} - x^2 y\right]_{-1}^{4} dx = \int_0^1\left(\frac{65}{3} - 5x^2\right)dx = \frac{65}{3} - \frac{5}{3}$$

$$\boxed{\Phi = 20 \text{ Wb}}$$

Check by $\oint\vec A\cdot d\vec l$ round the rectangle (counter-clockwise): the $x$-sides contribute $\int_0^1 x^2(-1)dx - \int_0^1 x^2(4)dx = -\tfrac13 - \tfrac43 = -\tfrac53$; the $y$-sides $\int_{-1}^{4}(1)y^2dy - \int_{-1}^{4}0 = \tfrac{65}{3}$. Total $\tfrac{65}{3} - \tfrac{5}{3} = 20$ Wb ✓.

@s 6
**Setup.** The filament lies along the $z$-axis from $z' = -L$ to $z' = +L$ (let $L \to \infty$). For a line current the vector potential is

$$\begin{gathered}\vec A = \frac{\mu_0}{4\pi}\int \frac{I\,d\vec l'}{R} \\ d\vec l' = dz'\,\hat a_z \\ R = \sqrt{\rho^2 + z'^2}\end{gathered}$$

```figure caption="Infinite filament on the z-axis carrying current I. The field point P is at distance ρ; dz' is a current element at height z', R is the distance from the element to P. By symmetry H has only an aφ component."
fig,ax=plt.subplots(figsize=(4.8,3.0)); ax.axis("off"); ax.set_xlim(-1.5,4.4); ax.set_ylim(-1.6,3.4)
ax.annotate("",xy=(0,3.2),xytext=(0,-1.5),arrowprops=dict(arrowstyle="-|>",color=INK,lw=2))
ax.text(0.12,3.05,"z",fontsize=9); ax.text(-0.45,2.2,"I",fontsize=10,color=ACCENT,fontweight="bold")
ax.plot([0,3.0],[0.0,0.0],color=MUTED,lw=1,ls="--"); ax.plot(3.0,0,"o",color=INK,ms=5); ax.text(3.1,-0.35,"P(ρ, φ, z)",fontsize=8.5)
ax.plot([0,3.0],[1.6,0.0],color="#d9534f",lw=1.3); ax.text(1.0,1.0,"R",fontsize=9,color="#d9534f")
ax.plot(0,1.6,"o",color=ACCENT,ms=4); ax.text(0.15,1.65,"dz'",fontsize=8.5,color=ACCENT)
ax.text(1.5,-0.38,"ρ",fontsize=9,ha="center")
th=np.linspace(0,2*np.pi,60); ax.plot(3.0+0.55*np.cos(th),-0.0+0.17*np.sin(th),color=ACCENT,lw=1.2)
ax.annotate("",xy=(3.55,0.04),xytext=(3.55,0.0),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.2)); ax.text(3.65,0.25,r"$\mathbf{H}$ (aφ)",fontsize=8.5,color=ACCENT)
```

**Vector potential.** Integrating from $-L$ to $L$,

$$\vec A = \frac{\mu_0 I}{4\pi}\hat a_z\int_{-L}^{L}\frac{dz'}{\sqrt{\rho^2 + z'^2}} = \frac{\mu_0 I}{4\pi}\hat a_z\cdot 2\ln\!\left[\frac{L + \sqrt{L^2 + \rho^2}}{\rho}\right]$$

For $L \gg \rho$, $L + \sqrt{L^2+\rho^2} \to 2L$, therefore

$$\vec A = \frac{\mu_0 I}{2\pi}\left[\ln 2L - \ln\rho\right]\hat a_z$$

The term $\ln 2L$ is a constant (it diverges as $L \to \infty$ but vanishes on taking the curl), so choose the reference of $\vec A$ at $\rho = \rho_0$ and write

$$\vec A = -\frac{\mu_0 I}{2\pi}\ln\!\left(\frac{\rho}{\rho_0}\right)\hat a_z$$

**Magnetic flux density.** $\vec B = \nabla\times\vec A$. In cylindrical co-ordinates, with only $A_z(\rho)$ present,

$$\nabla\times\vec A = \left(\frac{1}{\rho}\frac{\partial A_z}{\partial\phi}\right)\hat a_\rho - \frac{\partial A_z}{\partial\rho}\,\hat a_\phi = -\frac{d}{d\rho}\left[-\frac{\mu_0 I}{2\pi}\ln\rho\right]\hat a_\phi = \frac{\mu_0 I}{2\pi\rho}\,\hat a_\phi$$

Since $\vec H = \vec B/\mu_0$:

$$\boxed{\vec H = \frac{I}{2\pi\rho}\,\hat a_\phi \ \text{A/m}}$$

The field circles the wire in the right-hand-rule direction and falls off as $1/\rho$. This agrees with Ampere's law: $\oint\vec H\cdot d\vec l = H_\phi\,2\pi\rho = I$.

@s 7
**Significance of curl.** The curl of a vector field measures its **rotation (circulation per unit area)** at a point. It is a vector whose direction is the axis about which the circulation is maximum and whose magnitude is that maximum circulation per unit area:

$$(\nabla\times\vec H)\cdot\hat a_n = \lim_{\Delta S\to0}\frac{\oint\vec H\cdot d\vec l}{\Delta S}$$

A small paddle wheel placed in the field turns only where the curl is non-zero (zero curl = irrotational/conservative field, such as $\vec E$ in electrostatics). *Example:* water flowing in a river faster at the middle than at the banks makes a paddle wheel spin, i.e. its velocity field has non-zero curl; in magnetostatics $\nabla\times\vec H = \vec J$, so $\vec H$ circulates around every current-carrying conductor (and $\vec H$ of a straight wire has zero curl everywhere outside it).

**Stokes' theorem:** $\displaystyle\oint_L\vec H\cdot d\vec l = \int_S(\nabla\times\vec H)\cdot d\vec S$.

```figure caption="Rectangular path for Stokes' theorem, traversed counter-clockwise when seen from +z so that dS = dx dy aₛ points along +aᴢ. The four sides are labelled 1 to 4."
fig,ax=plt.subplots(figsize=(4.8,3.0)); ax.set_xlim(2,7); ax.set_ylim(-3,3); ax.set_xlabel("x"); ax.set_ylabel("y"); ax.grid(True)
xs=[3,6,6,3,3]; ys=[-2,-2,2,2,-2]; ax.fill(xs,ys,color="#eaf3ff"); ax.plot(xs,ys,color=INK,lw=1.4)
for p,q in [((3.8,-2),(4.6,-2)),((6,-1),(6,-0.2)),((5.2,2),(4.4,2)),((3,1),(3,0.2))]:
    ax.annotate("",xy=q,xytext=p,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.6))
for t,x,y in [("1",4.5,-2.45),("2",6.25,0),("3",4.5,2.3),("4",2.7,0)]: ax.text(x,y,t,fontsize=9,ha="center",color="#d9534f")
ax.text(4.5,0,r"$d\mathbf{S}=dx\,dy\,\mathbf{a}_z$",ha="center",fontsize=9)
```

**Left side (line integral).** $\vec H = 4xy\,\hat a_x - 2y^2\,\hat a_y$ and $d\vec l = dx\,\hat a_x + dy\,\hat a_y$ on $z=0$.

| Side | Path | $\vec H\cdot d\vec l$ | Value |
|---|---|---|---|
| 1 | $y=-2,\ x:3\to6$ | $4x(-2)\,dx$ | $-8\left[\dfrac{x^2}{2}\right]_3^6 = -108$ |
| 2 | $x=6,\ y:-2\to2$ | $-2y^2\,dy$ | $-2\left[\dfrac{y^3}{3}\right]_{-2}^{2} = -\dfrac{32}{3}$ |
| 3 | $y=2,\ x:6\to3$ | $4x(2)\,dx$ | $8\left[\dfrac{x^2}{2}\right]_6^3 = -108$ |
| 4 | $x=3,\ y:2\to-2$ | $-2y^2\,dy$ | $-2\left[\dfrac{y^3}{3}\right]_{2}^{-2} = +\dfrac{32}{3}$ |

$$\oint\vec H\cdot d\vec l = -108 - \frac{32}{3} - 108 + \frac{32}{3} = -216 \text{ A}$$

**Right side (surface integral).**

$$\nabla\times\vec H = \left(\frac{\partial H_y}{\partial x} - \frac{\partial H_x}{\partial y}\right)\hat a_z = (0 - 4x)\,\hat a_z = -4x\,\hat a_z$$

$$\int_S(\nabla\times\vec H)\cdot d\vec S = \int_{y=-2}^{2}\int_{x=3}^{6}(-4x)\,dx\,dy = -4\left[\frac{x^2}{2}\right]_3^6(4) = -4\,(13.5)(4) = -216 \text{ A}$$

$$\boxed{\oint\vec H\cdot d\vec l = \int_S(\nabla\times\vec H)\cdot d\vec S = -216 \text{ A}} \quad\text{Stokes' theorem is verified.}$$

@s 8
**Motional emf.** When a conductor moves with velocity $\vec u$ through a magnetic field $\vec B$, each free charge $Q$ experiences the magnetic force $\vec F_m = Q\,\vec u\times\vec B$. This is equivalent to an electric field acting on the moving charge:

$$\vec E_m = \frac{\vec F_m}{Q} = \vec u\times\vec B$$

The emf generated around a (moving) closed path is therefore

$$\mathrm{emf} = \oint(\vec u\times\vec B)\cdot d\vec l$$

```figure caption="A conducting bar of length ℓ slides with velocity u along two rails in a uniform field B (into the page). The magnetic force on the charges drives a current I; the loop area grows as ℓ·u·t."
fig,ax=plt.subplots(figsize=(4.8,2.7)); ax.axis("off"); ax.set_xlim(0,6); ax.set_ylim(0,3.4)
ax.plot([0.5,5.5],[0.6,0.6],color=INK,lw=2); ax.plot([0.5,5.5],[2.6,2.6],color=INK,lw=2); ax.plot([0.5,0.5],[0.6,2.6],color=INK,lw=2)
ax.plot([4.0,4.0],[0.6,2.6],color="#d9534f",lw=4)
ax.annotate("",xy=(5.2,1.6),xytext=(4.1,1.6),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.8)); ax.text(4.65,1.78,"u",fontsize=10,color=ACCENT,ha="center")
for x in (1.2,2.0,2.8,3.4):
    for y in (1.0,1.6,2.2): ax.text(x,y,"×",fontsize=11,color=MUTED,ha="center",va="center")
ax.text(2.1,2.85,"B (into the page)",fontsize=8.5,color=MUTED,ha="center"); ax.text(4.2,0.25,"bar, length ℓ",fontsize=8.5)
ax.annotate("",xy=(0.8,1.9),xytext=(0.8,1.3),arrowprops=dict(arrowstyle="-|>",color=INK,lw=1.2)); ax.text(0.65,1.6,"I",fontsize=9,ha="right")
```

**Cases of Faraday's law.** The total emf is

$$\mathrm{emf} = \oint\vec E\cdot d\vec l = -\frac{d\Psi}{dt} = \underbrace{-\int_S\frac{\partial\vec B}{\partial t}\cdot d\vec S}_{\text{transformer emf (loop at rest, B varies)}} + \underbrace{\oint(\vec u\times\vec B)\cdot d\vec l}_{\text{motional emf (loop moves, B static)}}$$

**Example, the sliding bar.** With $\vec B = B\,(-\hat a_z)$ into the page and $\vec u = u\,\hat a_x$: $\vec u\times\vec B = uB\,\hat a_y$ (up the bar), and only the bar contributes:

$$\mathrm{emf} = \int_0^{\ell}(uB)\,dy = B\,\ell\,u$$

The same result follows from flux: $\Psi = B\ell x$, $x = ut$, so $|\mathrm{emf}| = d\Psi/dt = B\ell u$. For $B = 0.5$ T, $\ell = 0.2$ m and $u = 4$ m/s: $\mathrm{emf} = 0.4$ V. The direction of the induced current opposes the change in flux (Lenz's law).

**Maxwell's equations (point form, time-varying fields):**

| Law | Point form |
|---|---|
| Gauss's law (electric) | $\nabla\cdot\vec D = \rho_v$ |
| Gauss's law (magnetic) | $\nabla\cdot\vec B = 0$ |
| Faraday's law | $\nabla\times\vec E = -\dfrac{\partial\vec B}{\partial t}$ |
| Ampere's circuital law (with displacement current) | $\nabla\times\vec H = \vec J + \dfrac{\partial\vec D}{\partial t}$ |

with the constitutive relations $\vec D = \epsilon\vec E$, $\vec B = \mu\vec H$, $\vec J = \sigma\vec E$.

@s 9
**Uniform plane wave.** A wave whose electric and magnetic fields lie in planes **perpendicular to the direction of propagation** and whose magnitude and phase are **constant over each plane** (the fields depend on one co-ordinate only, say $z$ and $t$). $\vec E$, $\vec H$ and the direction of propagation are mutually perpendicular (a TEM wave), and $\vec E/\vec H$ is the intrinsic impedance $\eta$.

**Lossy dielectric** ($\sigma \ne 0$, source-free, $\rho_v = 0$). Maxwell's curl equations in phasor form are

$$\begin{gathered}\nabla\times\vec E_s = -j\omega\mu\vec H_s \\ \nabla\times\vec H_s = (\sigma + j\omega\epsilon)\vec E_s\end{gathered}$$

Take the curl of the first and use $\nabla\times\nabla\times\vec E = \nabla(\nabla\cdot\vec E) - \nabla^2\vec E$ with $\nabla\cdot\vec E = 0$:

$$\nabla^2\vec E_s = j\omega\mu(\sigma + j\omega\epsilon)\vec E_s = \gamma^2\vec E_s$$

where the **propagation constant** is

$$\gamma = \alpha + j\beta = \sqrt{j\omega\mu(\sigma + j\omega\epsilon)} = j\omega\sqrt{\mu\epsilon}\sqrt{1 - j\frac{\sigma}{\omega\epsilon}}$$

Separating real and imaginary parts of $\gamma^2 = -\omega^2\mu\epsilon + j\omega\mu\sigma$:

$$\begin{gathered}\alpha = \omega\sqrt{\frac{\mu\epsilon}{2}}\left[\sqrt{1 + \left(\frac{\sigma}{\omega\epsilon}\right)^{2}} - 1\right]^{1/2} \text{ Np/m} \\ \beta = \omega\sqrt{\frac{\mu\epsilon}{2}}\left[\sqrt{1 + \left(\frac{\sigma}{\omega\epsilon}\right)^{2}} + 1\right]^{1/2} \text{ rad/m}\end{gathered}$$

For a wave with $\vec E = E_x(z)\,\hat a_x$ the equation reduces to $\dfrac{d^2E_{xs}}{dz^2} = \gamma^2E_{xs}$, with the forward-travelling solution $E_{xs} = E_0e^{-\gamma z}$. In the time domain,

$$\boxed{\vec E(z,t) = E_0\,e^{-\alpha z}\cos(\omega t - \beta z)\,\hat a_x \text{ V/m}}$$

The magnetic field is obtained from $\vec H_s = \dfrac{1}{-j\omega\mu}\nabla\times\vec E_s$:

$$\vec H(z,t) = \frac{E_0}{|\eta|}e^{-\alpha z}\cos(\omega t - \beta z - \theta_\eta)\,\hat a_y$$

with the complex intrinsic impedance

$$\begin{gathered}\eta = \sqrt{\frac{j\omega\mu}{\sigma + j\omega\epsilon}} = |\eta|\angle\theta_\eta \\ |\eta| = \frac{\sqrt{\mu/\epsilon}}{\left[1 + (\sigma/\omega\epsilon)^2\right]^{1/4}} \\ \tan 2\theta_\eta = \frac{\sigma}{\omega\epsilon}\end{gathered}$$

Hence in a lossy medium (i) the amplitude decays as $e^{-\alpha z}$ (skin depth $\delta = 1/\alpha$), (ii) $\vec H$ lags $\vec E$ by $\theta_\eta$ ($0 < \theta_\eta < 45^\circ$), and (iii) $u = \omega/\beta$ and $\lambda = 2\pi/\beta$. For a lossless medium ($\sigma = 0$) $\alpha = 0$, $\beta = \omega\sqrt{\mu\epsilon}$ and $\eta = \sqrt{\mu/\epsilon}$ is real.

@s 10
The wave is $\vec H = 10\cos(10^8t - \beta x)\,\hat a_y$ A/m in free space, travelling along $+x$.

**(a)** $\omega = 10^8$ rad/s.

**(b)** In free space $\beta = \omega\sqrt{\mu_0\epsilon_0} = \dfrac{\omega}{c} = \dfrac{10^8}{3\times10^8}$, so $\boxed{\beta = 0.333 \text{ rad/m}}$.

**(c)** $\lambda = \dfrac{2\pi}{\beta} = \dfrac{2\pi}{0.3333}$, so $\boxed{\lambda = 18.85 \text{ m}}$ (and $f = 15.9$ MHz).

**(d)** In free space $\eta_0 = 377\ \Omega$, so $E_0 = \eta_0H_0 = 377\times10 = 3770$ V/m. The direction of $\vec E$ follows from $\vec E\times\vec H \parallel +\hat a_x$ (direction of propagation). Since $\hat a_x = (-\hat a_z)\times\hat a_y$, $\vec E$ is along $-\hat a_z$:

$$\vec E(x,t) = -3770\cos(10^8t - 0.3333x)\,\hat a_z \text{ V/m}$$

At $P(0.1, 0.2, 0.3)$ and $t = 1$ ns $= 10^{-9}$ s:

$$\begin{gathered}\text{phase} = 10^8(10^{-9}) - 0.3333(0.1) = 0.1 - 0.0333 = 0.0667 \text{ rad} \\ \cos(0.0667) = 0.99778\end{gathered}$$

$$\boxed{\vec E = -3770(0.9978)\,\hat a_z \approx -3.76\times10^{3}\,\hat a_z \text{ V/m}}$$

@s 11
A **distortionless line** satisfies $\dfrac{R}{L} = \dfrac{G}{C}$. Then

$$\begin{gathered}\gamma = \sqrt{RG} + j\omega\sqrt{LC} \\ \alpha = \sqrt{RG} = R\sqrt{\frac{C}{L}} = \frac{R}{Z_0} \\ \beta = \omega\sqrt{LC} \\ Z_0 = \sqrt{\frac{L}{C}} \ (\text{real})\end{gathered}$$

and $u = \dfrac{1}{\sqrt{LC}}$. All of these are **independent of frequency**, so the values at 300 MHz are the same as at any frequency. Given $Z_0 = 50\ \Omega$, $\alpha = 0.022$ Np/m, $u = 2\times10^8$ m/s.

$$\begin{aligned} R &= \alpha Z_0 = 0.022\times50 = 1.1\ \Omega/\text{m} \\ L &= \frac{Z_0}{u} = \frac{50}{2\times10^8} = 0.25\ \mu\text{H/m} \\ C &= \frac{1}{Z_0u} = \frac{1}{50\times2\times10^8} = 100 \text{ pF/m} \\ G &= \frac{RC}{L} = \frac{\alpha}{Z_0} = \frac{0.022}{50} = 0.44 \text{ mS/m} \end{aligned}$$

$$\boxed{R = 1.1\ \Omega/\text{m},\quad L = 0.25\ \mu\text{H/m},\quad C = 100\ \text{pF/m},\quad G = 0.44\ \text{mS/m}}$$

Check: $\sqrt{L/C} = \sqrt{0.25\times10^{-6}/100\times10^{-12}} = 50\ \Omega$ ✓; $1/\sqrt{LC} = 2\times10^{8}$ m/s ✓; $R/L = 4.4\times10^{6} = G/C$ ✓; and at 300 MHz $\beta = \omega/u = 2\pi(300\times10^6)/(2\times10^8) = 9.42$ rad/m.

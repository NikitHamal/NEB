---
file: NEBians-IOE-Past-Paper-Electromagnetics-ENEX254-2082-Bhadra.pdf
subject: Electromagnetics
level: BE · Year II / Part II
code: ENEX 254
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Necessary formula sheet is attached (curl, divergence, gradient and Laplacian in the three co-ordinate systems) · Assume suitable data if necessary</small>

@q 1
Given a point $P(-2, 6, 3)$ and the vector field $\vec A = y\,\hat a_x + (xy + z)\,\hat a_y$, express $P$ and $\vec A$ in the cylindrical co-ordinate system, and evaluate $\vec A$ at $P$. [[5]]

@q 2
State the divergence theorem. A uniform sheet of charge $\rho_s = 20\epsilon_0$ C/m$^2$ is located in the plane $x = 2$ in free space. A uniform line charge $\rho_L = 0.5$ nC/m lies along the line $x = 6,\ y = 3$ in free space. Find the potential at the point $P(4, 6, -2)$ if $V = 8$ V at $A(2, 6, 4)$. [[1+5]]

@q 3
Derive the expression for the electric field intensity in the different regions of a coaxial cable with inner conductor of radius $a$ and outer conductor of radius $b$. [[5]]

@q 4
The region $y < 0$ contains a dielectric material for which $\epsilon_{r1} = 2.5$, while the region $y > 0$ is characterized by $\epsilon_{r2} = 4$. Let $\vec E_1 = -30\,\hat a_x + 50\,\hat a_y + 70\,\hat a_z$ V/m, find the electric field intensity and flux density in region 2, and the angle $\theta_1$. [[2+2+1]]

@q 5
Find the capacitance of a spherical capacitor by using the solution of the one-dimensional Laplace equation. [[4]]

@q 6
State Stokes' theorem. Let $\mu_{r1} = 2$ in region 1, defined by $2x + 3y - 4z > 1$, while $\mu_{r2} = 5$ in region 2 where $2x + 3y - 4z < 1$. In region 1, $\vec H_1 = 50\,\hat a_x - 30\,\hat a_y + 20\,\hat a_z$ A/m. Find (a) $\vec H_2$ (b) $\theta_2$. [[1+5]]

@q 7
Derive the expression for the magnetic field intensity due to an infinitely long current-carrying element using Ampere's circuital law. Given the vector magnetic potential $\vec A = -\left(\dfrac{10}{\rho^2}\right)\hat a_z$ Wb/m, find the current density $\vec J$. [[3+3]]

@q 8
Derive the expression for the net emf in electromagnetic induction. How does the equation $\nabla\times\vec H = \sigma\vec E$ change for time-varying fields? [[4+2]]

@q 9
Define the Poynting vector. Derive the expression for the average power density when a wave propagates in a lossy dielectric. [[2+4]]

@q 10
In phasor form, the electric field intensity of a uniform plane wave in free space is expressed as $\vec E_s = (40 - j30)\,e^{-j20z}\,\hat a_x$ V/m. Find (a) $\beta$ (b) $\omega$ (c) $f$ (d) $\vec H_s$. [[1+1+1+3]]

@q 11
The parameters of a certain transmission line operating at $6\times10^8$ rad/s are $L = 0.4\ \mu$H/m, $C = 40$ pF/m, $G = 80$ mS/m and $R = 20\ \Omega$/m. Find $\gamma,\ \alpha,\ \beta$ and $Z_0$. [[1+1+1+2]]

<!-- SOLUTIONS -->

@s 1
**Point P.** For $P(x, y, z) = (-2, 6, 3)$:

$$\begin{gathered}\rho = \sqrt{x^2 + y^2} = \sqrt{4 + 36} = 6.325 \\ \phi = \tan^{-1}\frac{y}{x} = \tan^{-1}\frac{6}{-2} = 108.43^\circ \ (\text{2nd quadrant}) \\ z = 3\end{gathered}$$

$$\boxed{P(\rho, \phi, z) = (6.325,\ 108.43^\circ,\ 3)}$$

**Vector field.** Substituting $x = \rho\cos\phi$, $y = \rho\sin\phi$,

$$\begin{gathered}A_x = \rho\sin\phi \\ A_y = \rho^2\sin\phi\cos\phi + z \\ A_z = 0\end{gathered}$$

The transformation is $A_\rho = A_x\cos\phi + A_y\sin\phi$, $A_\phi = -A_x\sin\phi + A_y\cos\phi$, $A_z = 0$, so

$$\begin{aligned} A_\rho &= \rho\sin\phi\cos\phi + (\rho^2\sin\phi\cos\phi + z)\sin\phi \\ A_\phi &= -\rho\sin^2\phi + (\rho^2\sin\phi\cos\phi + z)\cos\phi \end{aligned}$$

$$\vec A = A_\rho\,\hat a_\rho + A_\phi\,\hat a_\phi \quad(A_z = 0)$$

**At P.** In Cartesian form $A_x = y = 6$ and $A_y = xy + z = -12 + 3 = -9$. With $\cos\phi = -0.3162$ and $\sin\phi = 0.9487$:

$$A_\rho = 6(-0.3162) + (-9)(0.9487) = -1.897 - 8.538 = -10.44$$

$$A_\phi = -6(0.9487) + (-9)(-0.3162) = -5.692 + 2.846 = -2.846$$

$$\boxed{\vec A(P) = -10.44\,\hat a_\rho - 2.85\,\hat a_\phi}$$

Check: $|\vec A| = \sqrt{10.44^2 + 2.85^2} = 10.82 = \sqrt{6^2 + 9^2}$ ✓.

@s 2
**Divergence theorem.** The total outward flux of a vector field through a closed surface equals the volume integral of its divergence over the enclosed volume:

$$\oint_S\vec D\cdot d\vec S = \int_V(\nabla\cdot\vec D)\,dv$$

**Sheet.** $\rho_s = 20\epsilon_0$ gives a uniform field of magnitude $\dfrac{\rho_s}{2\epsilon_0} = 10$ V/m: $\vec E_s = +10\,\hat a_x$ for $x > 2$ and $-10\,\hat a_x$ for $x < 2$. Both $A$ ($x = 2$) and $P$ ($x = 4$) are on or beyond the sheet, so the potential change from $A$ to $P$ is

$$V_{P} - V_{A}\big|_{sheet} = -\int_{2}^{4}10\,dx = -20 \text{ V}$$

**Line charge.** The line is parallel to $z$ at $(6, 3)$. The distances of $A(2,6)$ and $P(4,6)$ from it are

$$\begin{gathered}\rho_A = \sqrt{(2-6)^2 + (6-3)^2} = 5 \\ \rho_P = \sqrt{(4-6)^2 + (6-3)^2} = \sqrt{13} = 3.606\end{gathered}$$

For the line, $V = -\dfrac{\rho_L}{2\pi\epsilon_0}\ln\rho + C$, so

$$V_P - V_A\big|_{line} = -\frac{\rho_L}{2\pi\epsilon_0}\ln\frac{\rho_P}{\rho_A} = -(8.988)\ln\frac{3.606}{5} = -8.988(-0.3270) = +2.94 \text{ V}$$

using $\dfrac{\rho_L}{2\pi\epsilon_0} = \dfrac{0.5\times10^{-9}}{2\pi(8.854\times10^{-12})} = 8.988$ V.

**Total** (superposition), starting from $V_A = 8$ V:

$$V_P = V_A + (-20) + 2.94 = 8 - 20 + 2.94$$

$$\boxed{V_P = -9.06 \text{ V}}$$

@s 3
```figure caption="Cross-section (left) and side view (right) of a coaxial cable: inner conductor radius a carrying charge +ρL per unit length, outer conductor radius b carrying −ρL. The dotted cylinder of radius ρ is the Gaussian surface."
fig,(a,b)=plt.subplots(1,2,figsize=(7.2,2.8),gridspec_kw={"width_ratios":[1,1.3]})
t=np.linspace(0,2*np.pi,200)
a.set_aspect("equal"); a.axis("off"); a.set_xlim(-2.4,2.4); a.set_ylim(-2.4,2.4)
a.fill(2.0*np.cos(t),2.0*np.sin(t),color="#fff4d6"); a.fill(0.7*np.cos(t),0.7*np.sin(t),color="white")
a.plot(2.0*np.cos(t),2.0*np.sin(t),color=INK,lw=2); a.plot(0.7*np.cos(t),0.7*np.sin(t),color=INK,lw=2)
a.fill(0.7*np.cos(t),0.7*np.sin(t),color="#d6e6f7"); a.plot(1.3*np.cos(t),1.3*np.sin(t),color=ACCENT,lw=1.2,ls=":")
a.annotate("",xy=(0.7,0),xytext=(0,0),arrowprops=dict(arrowstyle="<->",color=INK,lw=1)); a.text(0.35,0.12,"a",fontsize=9,ha="center")
a.annotate("",xy=(-1.41,-1.41),xytext=(0,0),arrowprops=dict(arrowstyle="<->",color=INK,lw=1)); a.text(-0.95,-0.5,"b",fontsize=9)
for ang in (30,150,270): a.annotate("",xy=(1.8*np.cos(np.radians(ang)),1.8*np.sin(np.radians(ang))),xytext=(1.0*np.cos(np.radians(ang)),1.0*np.sin(np.radians(ang))),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.3))
a.text(0.0,0.0,"+ρL",fontsize=8,ha="center",va="center"); a.text(1.55,1.55,"E",fontsize=9,color="#d9534f"); a.text(1.5,-2.25,"outer: −ρL",fontsize=8)
b.axis("off"); b.set_xlim(0,7); b.set_ylim(0,3)
b.add_patch(__import__("matplotlib.patches",fromlist=["x"]).Rectangle((0.5,0.4),6,2.2,fc="#fff4d6",ec=INK,lw=2)); b.add_patch(__import__("matplotlib.patches",fromlist=["x"]).Rectangle((0.5,1.2),6,0.6,fc="#d6e6f7",ec=INK,lw=2))
b.add_patch(__import__("matplotlib.patches",fromlist=["x"]).Rectangle((2.0,0.75),3,1.5,fc="none",ec=ACCENT,lw=1.2,ls=":"))
b.text(3.5,1.5,"inner conductor (a)",ha="center",va="center",fontsize=8); b.text(3.5,2.45,"outer conductor (b)",ha="center",fontsize=8,va="top"); b.text(3.5,0.58,"Gaussian surface ρ, length L",ha="center",fontsize=8,color=ACCENT)
```

Let the inner conductor carry a charge $+\rho_L$ per unit length and the outer conductor $-\rho_L$ (equal and opposite), with a dielectric of permittivity $\epsilon$ in between. By symmetry $\vec E = E_\rho(\rho)\,\hat a_\rho$ only (long cable, no end effects). Apply Gauss's law to a coaxial cylinder of radius $\rho$ and length $L$:

$$\oint\vec D\cdot d\vec S = D_\rho\,(2\pi\rho L) = Q_{enc}$$

**Region 1: $\rho < a$ (inside the inner conductor).** All charge resides on the surface of a conductor, so $Q_{enc} = 0$:

$$\vec E = 0$$

**Region 2: $a < \rho < b$ (dielectric).** $Q_{enc} = \rho_L L$ (or $\rho_s(2\pi aL)$ with $\rho_L = 2\pi a\rho_s$):

$$\begin{gathered}D_\rho = \frac{\rho_L}{2\pi\rho} \\ \Longrightarrow \\ \boxed{\vec E = \frac{\rho_L}{2\pi\epsilon\rho}\,\hat a_\rho = \frac{a\rho_s}{\epsilon\rho}\,\hat a_\rho}\end{gathered}$$

**Region 3: $\rho > b$ (outside).** $Q_{enc} = \rho_LL - \rho_LL = 0$:

$$\vec E = 0$$

So the field of a coaxial cable is confined to the space between the conductors (that is why coax is shielded). The potential difference between the conductors and the capacitance per unit length follow as

$$\begin{gathered}V_{ab} = -\int_b^a\frac{\rho_L}{2\pi\epsilon\rho}d\rho = \frac{\rho_L}{2\pi\epsilon}\ln\frac{b}{a} \\ C' = \frac{\rho_L}{V_{ab}} = \frac{2\pi\epsilon}{\ln(b/a)} \text{ F/m}\end{gathered}$$

@s 4
The boundary is the plane $y = 0$, so the **normal** direction is $\hat a_y$ and the **tangential** components are $x$ and $z$. Region 1 ($y < 0$) has $\epsilon_1 = 2.5\epsilon_0$ and region 2 ($y > 0$) has $\epsilon_2 = 4\epsilon_0$. There is no free surface charge on a dielectric boundary.

**Electric field in region 2.**

- Tangential $\vec E$ is continuous: $E_{2x} = E_{1x} = -30$ and $E_{2z} = E_{1z} = 70$ V/m.
- Normal $\vec D$ is continuous: $\epsilon_2E_{2y} = \epsilon_1E_{1y}$, so $E_{2y} = \dfrac{2.5}{4}(50) = 31.25$ V/m.

$$\begin{gathered}\boxed{\vec E_2 = -30\,\hat a_x + 31.25\,\hat a_y + 70\,\hat a_z \text{ V/m}} \\ |\vec E_2| = 82.3 \text{ V/m}\end{gathered}$$

**Flux density in region 2.** $\vec D_2 = \epsilon_0\epsilon_{r2}\vec E_2 = (8.854\times10^{-12})(4)\vec E_2$:

$$\boxed{\vec D_2 = -1.062\,\hat a_x + 1.107\,\hat a_y + 2.479\,\hat a_z \text{ nC/m}^2} \quad\left(= \epsilon_0(-120,\ 125,\ 280)\right)$$

**Angle $\theta_1$** (between $\vec E_1$ and the normal $\hat a_y$):

$$\begin{gathered}|\vec E_1| = \sqrt{30^2 + 50^2 + 70^2} = 91.10 \\ \cos\theta_1 = \frac{E_{1y}}{|\vec E_1|} = \frac{50}{91.10} = 0.549\end{gathered}$$

$$\boxed{\theta_1 = 56.7^\circ}$$

Check with the tangential magnitude: $\tan\theta_1 = \dfrac{\sqrt{30^2 + 70^2}}{50} = \dfrac{76.16}{50}$, giving $56.7^\circ$ ✓. In region 2 the field makes $\theta_2 = \tan^{-1}(76.16/31.25) = 67.7^\circ$ with the normal, and $\tan\theta_1/\tan\theta_2 = \epsilon_1/\epsilon_2 = 0.625$ ✓.

@s 5
```figure caption="Spherical capacitor: inner conductor of radius a at potential V0, outer spherical shell of radius b at zero potential, dielectric of permittivity ε between. Equipotentials are concentric spheres, so V depends on r only."
fig,ax=plt.subplots(figsize=(3.8,3.0)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.4,2.4); ax.set_ylim(-2.3,2.3)
t=np.linspace(0,2*np.pi,200)
ax.fill(2*np.cos(t),2*np.sin(t),color="#fff4d6"); ax.fill(0.8*np.cos(t),0.8*np.sin(t),color="#d6e6f7")
ax.plot(2*np.cos(t),2*np.sin(t),color=INK,lw=2); ax.plot(0.8*np.cos(t),0.8*np.sin(t),color=INK,lw=2)
ax.annotate("",xy=(0.8,0),xytext=(0,0),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(0.4,0.1,"a",fontsize=9,ha="center")
ax.annotate("",xy=(1.41,-1.41),xytext=(0,0),arrowprops=dict(arrowstyle="<->",color=INK)); ax.text(0.9,-0.95,"b",fontsize=9)
ax.text(0,0.45,"V = V0",ha="center",fontsize=8); ax.text(0,1.4,"ε",ha="center",fontsize=10); ax.text(-1.9,1.9,"V = 0",fontsize=8)
for ang in (30,120,200,300): c,s=np.cos(np.radians(ang)),np.sin(np.radians(ang)); ax.annotate("",xy=(1.85*c,1.85*s),xytext=(1.0*c,1.0*s),arrowprops=dict(arrowstyle="-|>",color="#d9534f",lw=1.1))
```

Let the inner sphere (radius $a$) be at potential $V_0$ and the outer sphere (radius $b$) at zero. In the dielectric there is no charge, so Laplace's equation holds. By symmetry $V = V(r)$, and in spherical co-ordinates

$$\nabla^2V = \frac{1}{r^2}\frac{d}{dr}\left(r^2\frac{dV}{dr}\right) = 0$$

**Solution.** Integrating once, $r^2\dfrac{dV}{dr} = A$, so $\dfrac{dV}{dr} = \dfrac{A}{r^2}$, and again

$$V = -\frac{A}{r} + B$$

**Boundary conditions:** $V(r = b) = 0$ and $V(r = a) = V_0$.

$$\begin{gathered}0 = -\frac{A}{b} + B \\ V_0 = -\frac{A}{a} + B \quad\Longrightarrow\quad A = -\frac{V_0ab}{b - a} \\ B = -\frac{V_0a}{b - a}\end{gathered}$$

$$V(r) = V_0\,\frac{a}{b-a}\left(\frac{b}{r} - 1\right) = V_0\,\frac{\dfrac1r - \dfrac1b}{\dfrac1a - \dfrac1b}$$

**Field and charge.**

$$\vec E = -\nabla V = -\frac{dV}{dr}\hat a_r = \frac{V_0\,ab}{(b-a)\,r^2}\hat a_r$$

The surface charge on the inner sphere is $\rho_s = D_r(a) = \epsilon E_r(a) = \dfrac{\epsilon V_0\,b}{(b-a)\,a}$, so

$$Q = \rho_s\,(4\pi a^2) = \frac{4\pi\epsilon\,ab}{b - a}V_0$$

$$\boxed{C = \frac{Q}{V_0} = \frac{4\pi\epsilon\,ab}{b - a} = \frac{4\pi\epsilon}{\dfrac{1}{a} - \dfrac{1}{b}} \text{ F}}$$

As $b \to \infty$ this becomes the isolated sphere, $C = 4\pi\epsilon a$.

@s 6
**Stokes' theorem.** The circulation of a vector field around a closed path equals the flux of its curl through any surface bounded by that path:

$$\oint_L\vec H\cdot d\vec l = \int_S(\nabla\times\vec H)\cdot d\vec S$$

**Boundary conditions used.** The boundary $2x + 3y - 4z = 1$ carries no surface current, hence tangential $\vec H$ is continuous ($\vec H_{t1} = \vec H_{t2}$) and normal $\vec B$ is continuous ($\mu_1H_{n1} = \mu_2H_{n2}$).

**Unit normal.** For $f = 2x + 3y - 4z$, $\nabla f = (2, 3, -4)$, $|\nabla f| = \sqrt{29}$:

$$\hat a_n = \frac{2\,\hat a_x + 3\,\hat a_y - 4\,\hat a_z}{\sqrt{29}} \quad(\text{pointing into region 1, where } f > 1)$$

**(a) Components of $\vec H_1$.**

$$\vec H_1\cdot\hat a_n = \frac{50(2) - 30(3) + 20(-4)}{\sqrt{29}} = \frac{100 - 90 - 80}{\sqrt{29}} = \frac{-70}{\sqrt{29}} = -13.0$$

$$\vec H_{n1} = (\vec H_1\cdot\hat a_n)\hat a_n = \frac{-70}{29}(2, 3, -4) = (-4.828,\ -7.241,\ 9.655)$$

$$\vec H_{t1} = \vec H_1 - \vec H_{n1} = (54.83,\ -22.76,\ 10.34)$$

Now $\vec H_{t2} = \vec H_{t1}$ and $\mu_{r1}H_{n1} = \mu_{r2}H_{n2}$, so $\vec H_{n2} = \dfrac{2}{5}\vec H_{n1} = (-1.931,\ -2.897,\ 3.862)$.

$$\begin{gathered}\boxed{\vec H_2 = \vec H_{t2} + \vec H_{n2} = 52.90\,\hat a_x - 25.66\,\hat a_y + 14.21\,\hat a_z \text{ A/m}} \\ |\vec H_2| = 60.48 \text{ A/m}\end{gathered}$$

**(b) Angle $\theta_2$** (between $\vec H_2$ and the normal). With $|\vec H_1| = \sqrt{50^2 + 30^2 + 20^2} = 61.64$:

$$\theta_1 = \cos^{-1}\frac{|H_{n1}|}{|\vec H_1|} = \cos^{-1}\frac{13.0}{61.64} = 77.83^\circ$$

$$\tan\theta_2 = \frac{\mu_{r2}}{\mu_{r1}}\tan\theta_1 = 2.5(4.63) = 11.58 \ \Rightarrow\ \boxed{\theta_2 = 85.07^\circ}$$

Direct check: $\cos\theta_2 = \dfrac{|\vec H_2\cdot\hat a_n|}{|\vec H_2|} = \dfrac{5.20}{60.48} = 0.0860$, so $\theta_2 = 85.07^\circ$ ✓.

@s 7
**Part 1: Field of an infinitely long current element by Ampere's circuital law.**

```figure caption="Amperian circle of radius ρ around an infinitely long straight wire carrying current I along +z. By symmetry H has only an aφ component, constant on the circle."
fig,ax=plt.subplots(figsize=(3.8,3.0)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.2,2.2); ax.set_ylim(-2.0,2.0)
t=np.linspace(0,2*np.pi,200); ax.plot(1.5*np.cos(t),1.5*np.sin(t),color=ACCENT,lw=1.6)
ax.plot(0,0,"o",ms=14,color="#d9534f"); ax.plot(0,0,".",ms=4,color="white"); ax.text(0.15,0.15,"I (out of page)",fontsize=8,color="#d9534f")
ax.annotate("",xy=(0,1.5),xytext=(0,0),arrowprops=dict(arrowstyle="<->",color=INK,lw=1)); ax.text(0.1,0.7,"ρ",fontsize=9)
for ang in (45,135,225,315):
    c,s=np.cos(np.radians(ang)),np.sin(np.radians(ang)); ax.annotate("",xy=(1.5*c-0.28*s,1.5*s+0.28*c),xytext=(1.5*c,1.5*s),arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.5))
ax.text(1.3,1.35,"H",fontsize=10,color=ACCENT,fontweight="bold")
```

**Ampere's circuital law:** $\oint\vec H\cdot d\vec l = I_{enc}$. For a filament on the $z$-axis, the symmetry of the geometry gives $\vec H = H_\phi(\rho)\,\hat a_\phi$ (no $\rho$ or $z$ components, and $H_\phi$ independent of $\phi$ and $z$). Choose the circle of radius $\rho$ in the plane $z = $ const as the Amperian path, $d\vec l = \rho\,d\phi\,\hat a_\phi$:

$$\oint\vec H\cdot d\vec l = \int_0^{2\pi}H_\phi\,\rho\,d\phi = H_\phi\,(2\pi\rho) = I$$

$$\boxed{\vec H = \frac{I}{2\pi\rho}\,\hat a_\phi \text{ A/m}}$$

**Part 2: Current density from $\vec A = -\dfrac{10}{\rho^2}\hat a_z$ Wb/m.**

$$\begin{gathered}\vec B = \nabla\times\vec A = \left(\frac{1}{\rho}\frac{\partial A_z}{\partial\phi}\right)\hat a_\rho - \frac{\partial A_z}{\partial\rho}\hat a_\phi \\ \frac{\partial A_z}{\partial\rho} = \frac{20}{\rho^3}\end{gathered}$$

$$\begin{gathered}\vec B = -\frac{20}{\rho^3}\,\hat a_\phi \text{ Wb/m}^2 \\ \Rightarrow \\ \vec H = \frac{\vec B}{\mu_0} = -\frac{20}{\mu_0\rho^3}\,\hat a_\phi\end{gathered}$$

The current density is $\vec J = \nabla\times\vec H$. With only $H_\phi(\rho)$:

$$\vec J = \frac{1}{\rho}\frac{\partial(\rho H_\phi)}{\partial\rho}\,\hat a_z = \frac{1}{\rho}\frac{d}{d\rho}\left(-\frac{20}{\mu_0\rho^2}\right)\hat a_z = \frac{1}{\rho}\cdot\frac{40}{\mu_0\rho^3}\,\hat a_z$$

$$\boxed{\vec J = \frac{40}{\mu_0\rho^4}\,\hat a_z = \frac{3.18\times10^{7}}{\rho^4}\,\hat a_z \text{ A/m}^2}$$

Check with the Poisson equation for $\vec A$: $\nabla^2\vec A = -\mu_0\vec J$. $\nabla^2A_z = \dfrac{1}{\rho}\dfrac{d}{d\rho}\left(\rho\cdot\dfrac{20}{\rho^3}\right) = \dfrac{1}{\rho}\left(-\dfrac{40}{\rho^3}\right) = -\dfrac{40}{\rho^4}$, so $J_z = \dfrac{40}{\mu_0\rho^4}$ ✓.

@s 8
**Faraday's law and net emf.** Faraday experimentally found that a time-varying magnetic flux $\Psi$ linking a closed circuit induces an emf in it, in the direction that opposes the change (Lenz's law):

$$\begin{gathered}\mathrm{emf} = -\frac{d\Psi}{dt} \\ \Psi = \int_S\vec B\cdot d\vec S\end{gathered}$$

The emf is the line integral of the *total* electric field seen by the charges, $\mathrm{emf} = \oint\vec E\cdot d\vec l$. If the loop of contour $L$ is moving with velocity $\vec u$ while $\vec B$ may vary, the force per unit charge is $\vec E + \vec u\times\vec B$, hence

$$\mathrm{emf} = \oint_L(\vec E + \vec u\times\vec B)\cdot d\vec l = -\frac{d}{dt}\int_S\vec B\cdot d\vec S$$

The flux can change in two ways, so the **net emf** is

$$\boxed{\mathrm{emf} = \oint_L\vec E\cdot d\vec l = \underbrace{-\int_S\frac{\partial\vec B}{\partial t}\cdot d\vec S}_{\text{transformer emf}} + \underbrace{\oint_L(\vec u\times\vec B)\cdot d\vec l}_{\text{motional emf}}}$$

Special cases: (i) stationary loop, time-varying $\vec B$ gives only the transformer emf; (ii) moving or deforming loop in a static field gives only the motional emf, e.g. the sliding bar gives $B\ell u$; (iii) generator: both. For a stationary loop, applying Stokes' theorem to $\oint\vec E\cdot d\vec l = -\int\dfrac{\partial\vec B}{\partial t}\cdot d\vec S$ gives the point form

$$\nabla\times\vec E = -\frac{\partial\vec B}{\partial t}$$

**How $\nabla\times\vec H = \sigma\vec E$ changes.** For static fields $\nabla\times\vec H = \vec J = \sigma\vec E$ (conduction current only). Its divergence is $\nabla\cdot\vec J = 0$, which contradicts the continuity equation $\nabla\cdot\vec J = -\partial\rho_v/\partial t$ when the charge density changes with time. Maxwell added the displacement current density $\vec J_d = \dfrac{\partial\vec D}{\partial t}$:

$$\nabla\times\vec H = \vec J + \frac{\partial\vec D}{\partial t} = \boxed{\sigma\vec E + \epsilon\frac{\partial\vec E}{\partial t}}$$

Taking the divergence now gives $0 = \nabla\cdot\vec J + \partial(\nabla\cdot\vec D)/\partial t = \nabla\cdot\vec J + \partial\rho_v/\partial t$, which is the continuity equation. In phasor form $\nabla\times\vec H_s = (\sigma + j\omega\epsilon)\vec E_s$; the displacement current is negligible for good conductors ($\sigma \gg \omega\epsilon$) and dominant for good insulators.

@s 9
**Poynting vector.** The Poynting vector $\vec{\mathcal P} = \vec E\times\vec H$ (W/m$^2$) is the instantaneous power density of an electromagnetic field: its direction is that of the power flow and its magnitude is the power crossing unit area normal to it.

Origin (Poynting's theorem): from $\nabla\cdot(\vec E\times\vec H) = \vec H\cdot(\nabla\times\vec E) - \vec E\cdot(\nabla\times\vec H)$ and Maxwell's curl equations,

$$-\oint_S(\vec E\times\vec H)\cdot d\vec S = \frac{d}{dt}\int_V\left(\tfrac12\epsilon E^2 + \tfrac12\mu H^2\right)dv + \int_V\sigma E^2\,dv$$

i.e. the power flowing into a volume equals the rate of increase of stored energy plus the ohmic loss.

**Average power density in a lossy dielectric.** For a wave travelling in $+z$ with

$$\begin{gathered}\vec E_s = E_0\,e^{-\alpha z}e^{-j\beta z}\,\hat a_x \\ \vec H_s = \frac{E_0}{|\eta|}e^{-\alpha z}e^{-j\beta z}e^{-j\theta_\eta}\,\hat a_y \\ \eta = |\eta|\angle\theta_\eta\end{gathered}$$

the time-average Poynting vector is

$$\vec{\mathcal P}_{ave} = \frac12\mathrm{Re}\left(\vec E_s\times\vec H_s^*\right)$$

$$\vec E_s\times\vec H_s^* = E_0\,e^{-\alpha z}\hat a_x\times\frac{E_0}{|\eta|}e^{-\alpha z}e^{+j\theta_\eta}\hat a_y = \frac{E_0^2}{|\eta|}e^{-2\alpha z}e^{j\theta_\eta}\,\hat a_z$$

$$\boxed{\vec{\mathcal P}_{ave} = \frac{E_0^2}{2|\eta|}\,e^{-2\alpha z}\cos\theta_\eta\,\hat a_z \text{ W/m}^2}$$

Hence the power density decays as $e^{-2\alpha z}$ (twice as fast as the field amplitude), and is reduced by $\cos\theta_\eta$ because $\vec E$ and $\vec H$ are not in phase. For a lossless medium $\alpha = 0$, $\theta_\eta = 0$ and $\mathcal P_{ave} = E_0^2/2\eta$.

@s 10
$\vec E_s = (40 - j30)\,e^{-j20z}\,\hat a_x$ V/m: a uniform plane wave in free space travelling along $+z$ ($e^{-j\beta z}$ with $\beta = 20$).

**(a)** Comparing with $e^{-j\beta z}$: $\boxed{\beta = 20 \text{ rad/m}}$.

**(b)** In free space $\beta = \omega/c$:

$$\boxed{\omega = \beta c = 20(3\times10^8) = 6\times10^9 \text{ rad/s}}$$

**(c)**

$$\boxed{f = \frac{\omega}{2\pi} = \frac{6\times10^9}{2\pi} = 954.9 \text{ MHz}}$$

**(d)** $\vec E$ is along $\hat a_x$ and propagation is along $+\hat a_z$, so $\vec H$ is along $\hat a_y$ ($\hat a_x\times\hat a_y = \hat a_z$). With $\eta_0 = 377\ \Omega$:

$$\vec H_s = \frac{40 - j30}{377}\,e^{-j20z}\,\hat a_y = (0.1061 - j0.0796)\,e^{-j20z}\,\hat a_y$$

$$\boxed{\vec H_s = (0.106 - j0.0796)\,e^{-j20z}\,\hat a_y = 0.1326\angle{-36.87^\circ}\,e^{-j20z}\,\hat a_y \text{ A/m}}$$

In the time domain $\vec H(z,t) = 0.1326\cos(6\times10^9t - 20z - 36.87^\circ)\,\hat a_y$ A/m, since $|40 - j30| = 50$ V/m and $50/377 = 0.1326$.

@s 11
Given $\omega = 6\times10^8$ rad/s, $R = 20\ \Omega$/m, $L = 0.4\ \mu$H/m, $G = 80$ mS/m, $C = 40$ pF/m.

$$Z = R + j\omega L = 20 + j(6\times10^8)(0.4\times10^{-6}) = 20 + j240\ \Omega/\text{m}$$

$$Y = G + j\omega C = 0.08 + j(6\times10^8)(40\times10^{-12}) = 0.08 + j0.024\ \text{S/m}$$

**Propagation constant.**

$$\gamma = \sqrt{ZY} = \sqrt{(20 + j240)(0.08 + j0.024)} = \sqrt{(1.6 - 5.76) + j(0.48 + 19.2)} = \sqrt{-4.16 + j19.68}$$

$$\begin{gathered}|ZY| = \sqrt{4.16^2 + 19.68^2} = 20.12 \\ \angle ZY = 180^\circ - 78.1^\circ = 101.9^\circ\end{gathered}$$

$$\gamma = \sqrt{20.12}\,\angle50.97^\circ = 4.485\angle50.97^\circ$$

$$\boxed{\gamma = 2.824 + j3.484 \text{ m}^{-1}}$$

so $\boxed{\alpha = 2.82 \text{ Np/m}}$ and $\boxed{\beta = 3.48 \text{ rad/m}}$.

**Characteristic impedance.**

$$Z_0 = \sqrt{\frac{Z}{Y}} = \sqrt{\frac{20 + j240}{0.08 + j0.024}} = \sqrt{\frac{241.0\angle85.24^\circ}{0.08352\angle16.70^\circ}} = \sqrt{2885.6\angle68.54^\circ} = 53.70\angle34.27^\circ$$

$$\boxed{Z_0 = 44.38 + j30.24\ \Omega = 53.7\angle34.3^\circ\ \Omega}$$

Check: $\gamma Z_0 = Z$: $(4.485\angle50.97^\circ)(53.70\angle34.27^\circ) = 240.9\angle85.24^\circ = 20 + j240$ ✓. The line is not distortionless ($R/L = 5\times10^7 \ne G/C = 2\times10^9$); the phase velocity is $u = \omega/\beta = 1.72\times10^8$ m/s and $\lambda = 2\pi/\beta = 1.80$ m.

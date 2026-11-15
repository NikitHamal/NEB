---
file: NEBians-IOE-Past-Paper-Engineering-Physics-SH402-2082-Baishakh.pdf
subject: Engineering Physics
level: BE · Year I / Part I
code: SH 402
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: BEL, BEI, BCT, BAM, BIE, BAG, BAS
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 402). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define physical pendulum. Show that the time period is minimum when the length of the pendulum is equal to the radius of gyration. [[5]]

**OR**

What is electromagnetic oscillation? Prove that an LC circuit is an analogy of the spring-mass system and hence find its frequency. [[5]]

@q 2
A metallic disc of mass $0.5\ \text{kg}$ and radius $0.1\ \text{m}$ is suspended by a wire of length $40\ \text{cm}$ and radius $1\ \text{mm}$. The torsional oscillations of the disc are found to have a period of $2.5\ \text{s}$. Find the modulus of rigidity of the wire. [[5]]

@q 3
A room has dimensions of $6\times4\times5\ \text{m}$. Find (a) the mean free path of the sound wave in the room and (b) the number of reflections made per second by the sound waves with the walls of the room. Given the velocity of sound in air $350\ \text{m s}^{-1}$. [[5]]

@q 4
What are Newton's rings? Give the necessary theory for the determination of the wavelength of monochromatic light using Newton's rings method. [[5]]

**OR**

Show that the intensity of the second-order maximum of Fraunhofer's single-slit diffraction is $\left(\dfrac2{5\pi}\right)^2$ times the intensity of the central maximum. [[5]]

@q 5
Light of wavelength $6000\ \text{Å}$ falls normally on a thin wedge-shaped film of refractive index $1.4$ forming fringes that are $2\ \text{mm}$ apart. Find the angle of the wedge. [[5]]

@q 6
The refractive indices for the O-ray and E-ray are $1.65$ and $1.55$. Calculate the thickness of the retardation plate such that (i) the emergent ray is plane polarized, (ii) the emergent ray is elliptically polarized. (Given wavelength of light is $6000\ \text{Å}$.) [[5]]

@q 7
Derive the expression for the equivalent focal length of two thin lenses having focal lengths $f_1$ and $f_2$ separated by a distance $d$. Also find the position of the principal points. [[5]]

@q 8
Define the acceptance angle of an optical fibre. Derive the expressions for the acceptance angle and numerical aperture. Also show $\text{N.A.} = \mu_1\sqrt{2\Delta}$, where the symbols have their usual meanings. [[5]]

@q 9
Derive an expression for the electric field intensity due to a uniformly distributed charged plastic ring of radius $R$ at a distance $x$ from the centre on its axis. Also locate the point where the electric field is maximum. [[5]]

**OR**

Define electric quadrupole and electric quadrupole moment. Show that the electric potential due to a linear quadrupole for a large distance $r$ is proportional to $r^{-3}$. [[5]]

@q 10
Mention the steps to calculate the capacitance of a capacitor. Show that the capacitance of a cylindrical capacitor is inversely proportional to the logarithm of the ratio between the outer radius and the inner radius. [[5]]

@q 11
A typical copper wire of household wiring has a cross-sectional area $3.31\times10^{-6}\ \text{m}^2$ and carries a current of $5\ \text{A}$. What is the drift speed of the electrons? Given: density of copper $8.95\ \text{g cm}^{-3}$, Avogadro's number $6.02\times10^{23}\ \text{mol}^{-1}$, molar mass of copper $63.5\ \text{g}$. [[5]]

@q 12
Compare Ampere's law with the Biot-Savart law. Calculate the magnetic field outside and inside a long straight wire carrying current using Ampere's law. [[5]]

**OR**

What is the Hall effect? Derive the expressions for the Hall coefficient and the Hall resistance. Also show the variation of the Hall resistance with the magnetic field. [[5]]

@q 13
Deuterons in a cyclotron describe a circle of radius $0.3\ \text{m}$ just before emerging from the dees. The frequency of the applied emf is $10\ \text{MHz}$. Find the flux density of the magnetic field and the velocity of the deuterons emerging out of the cyclotron. (Mass of deuteron $3.32\times10^{-27}\ \text{kg}$ and charge $1.6\times10^{-19}\ \text{C}$.) [[5]]

@q 14
What is the magnetic flux density at the centre of a circular coil of radius $2\ \text{cm}$ and with $20$ turns carrying a current of $2\ \text{A}$? [[5]]

@q 15
Write Maxwell's equations in differential form. Convert them into integral form. Explain the physical significance of each of them. [[5]]

@q 16
Derive Schrödinger's time-dependent wave equation. Explain the physical significance of the wave function. [[5]]
<!-- SOLUTIONS -->

@s 1
**Physical (compound) pendulum.** Any rigid body free to oscillate in a vertical plane about a fixed horizontal axis that does not pass through its centre of gravity $G$ is a physical pendulum.

Let $m$ be the mass, $l$ the distance of the pivot $O$ from $G$ and $k$ the radius of gyration about the parallel axis through $G$. For a small angle $\theta$, the restoring torque is $mgl\sin\theta\approx mgl\theta$ and $I_O = m(k^2+l^2)$, so
$$m(k^2+l^2)\ddot\theta = -mgl\,\theta\ \Rightarrow\ \omega = \sqrt{\frac{gl}{k^2+l^2}}$$
$$T = 2\pi\sqrt{\frac{k^2+l^2}{gl}} = 2\pi\sqrt{\frac{1}{g}\left(\frac{k^2}{l} + l\right)}$$

**Minimum period.** $T$ is least when $f(l) = \dfrac{k^2}l + l$ is least:
$$\frac{df}{dl} = -\frac{k^2}{l^2} + 1 = 0\ \Rightarrow\ l = k$$
$$\frac{d^2f}{dl^2} = \frac{2k^2}{l^3} = \frac2k>0$$
so $f$ is a minimum at $l = k$. Hence
$$\boxed{T\ \text{is minimum when}\ l = k,\qquad T_{min} = 2\pi\sqrt{\frac{2k}g}}$$
$\blacksquare$

**OR: electromagnetic oscillation.** The periodic exchange of energy between the electric field of a capacitor and the magnetic field of an inductor, with the charge and the current oscillating sinusoidally, is called electromagnetic oscillation (as in an ideal LC circuit).

For an LC circuit with charge $q$ on the capacitor and current $i = \dfrac{dq}{dt}$, Kirchhoff's law gives $L\dfrac{di}{dt} + \dfrac qC = 0$:
$$L\frac{d^2q}{dt^2} + \frac1Cq = 0$$
For a spring-mass system: $m\dfrac{d^2x}{dt^2} + kx = 0$. The two equations are identical in form, giving the **analogy**:

| Mechanical | Electrical |
|---|---|
| displacement $x$ | charge $q$ |
| velocity $v = dx/dt$ | current $i = dq/dt$ |
| mass $m$ (inertia) | inductance $L$ |
| spring constant $k$ | $1/C$ |
| kinetic energy $\tfrac12mv^2$ | magnetic energy $\tfrac12Li^2$ |
| potential energy $\tfrac12kx^2$ | electric energy $\tfrac{q^2}{2C}$ |
| damping constant $b$ | resistance $R$ |

The total energy $U = \tfrac12Li^2 + \dfrac{q^2}{2C}$ is constant ($\dfrac{dU}{dt} = 0$ reproduces the equation above), just like $\tfrac12mv^2 + \tfrac12kx^2$.

Replacing $k/m\to\dfrac1{LC}$, the solution is $q = q_0\cos(\omega t + \phi)$ with
$$\boxed{\omega = \frac1{\sqrt{LC}},\qquad f = \frac1{2\pi\sqrt{LC}}}$$
(compare $\omega = \sqrt{k/m}$ for the spring).

@s 2
For a torsional pendulum, $T = 2\pi\sqrt{\dfrac IC}$ where $C$ is the torsional constant of the wire, $C = \dfrac{\pi\eta r^4}{2l}$, and $I$ is the moment of inertia of the disc about the wire (its axis):
$$I = \tfrac12MR^2 = \tfrac12(0.5)(0.1)^2 = 2.5\times10^{-3}\ \text{kg m}^2$$
$$C = \frac{4\pi^2I}{T^2} = \frac{4\pi^2(2.5\times10^{-3})}{(2.5)^2} = 1.579\times10^{-2}\ \text{N m/rad}$$
$$\eta = \frac{2lC}{\pi r^4} = \frac{2(0.40)(1.579\times10^{-2})}{\pi(10^{-3})^4}$$
$$\boxed{\eta\approx4.02\times10^{9}\ \text{N/m}^2}$$

@s 3
Room: $l = 6$ m, $b = 4$ m, $h = 5$ m. Volume $V = 6\times4\times5 = 120$ m³ and total surface area $S = 2(lb + bh + hl) = 2(24 + 20 + 30) = 148$ m².

**(a) Mean free path of sound** (average distance between successive reflections in a closed room):
$$\lambda_m = \frac{4V}{S} = \frac{4(120)}{148}$$
$$\boxed{\lambda_m\approx3.24\ \text{m}}$$
**(b) Number of reflections per second:**
$$n = \frac v{\lambda_m} = \frac{350}{3.243}$$
$$\boxed{n\approx108\ \text{reflections per second}}$$

@s 4
**Newton's rings.** When a plano-convex lens of a large radius of curvature $R$ is placed with its convex surface on a plane glass plate and illuminated by monochromatic light, a series of alternate bright and dark **concentric circular fringes** is seen around the point of contact. They are produced by interference between the rays reflected from the top and bottom surfaces of the air film enclosed between the lens and the plate, and are called Newton's rings.

```figure caption="Question 4: air film between the plano-convex lens and the plate; a ring of radius r corresponds to film thickness t."
th=np.linspace(np.pi/2-0.45,np.pi/2+0.45,100)
fig,ax=plt.subplots(figsize=(4.2,2.6))
R=6
ax.plot(R*np.cos(th),R*np.sin(th)-R+1.4,color='#1d6fb8',lw=1.6)
ax.plot([-3,3],[0,0],color='#14181f',lw=2)
ax.plot([-2,-2],[0,1.4-R+np.sqrt(R*R-4)],color='#d9534f',ls='--')
ax.text(-1.95,0.5,'$t$',color='#d9534f',fontsize=9)
ax.plot([0,2],[0,0],color='#2e8b57',lw=1.2); ax.text(0.8,-0.5,'$r$',color='#2e8b57',fontsize=9)
ax.text(0.1,1.5,'lens',fontsize=8); ax.text(2.4,-0.6,'glass plate',fontsize=8)
ax.set_xlim(-3.2,3.6); ax.set_ylim(-1,2.2); ax.axis('off')
```

**Theory (reflected light, normal incidence, air film $\mu = 1$).** The reflection at the glass plate adds a phase change $\pi$, so the effective path difference is $2t + \dfrac\lambda2$. For a **dark** ring $2t = n\lambda$. From the geometry, for a ring of radius $r_n$ (diameter $D_n$)
$$r_n^2 = 2Rt - t^2\approx2Rt\ \Rightarrow\ t = \frac{D_n^2}{8R}$$
$$\frac{D_n^2}{4R} = n\lambda\ \Rightarrow\ D_n^2 = 4n\lambda R$$
Similarly for the $(n+p)$th dark ring $D_{n+p}^2 = 4(n+p)\lambda R$. Subtracting eliminates the correction to the zero of ring counting (the centre is not a perfect point contact due to dust and elastic compression):
$$D_{n+p}^2 - D_n^2 = 4p\lambda R$$
$$\boxed{\lambda = \frac{D_{n+p}^2 - D_n^2}{4pR}}$$
**Procedure.** Measure $D_n$ and $D_{n+p}$ of the $n$th and $(n+p)$th dark rings with a travelling microscope and the radius $R$ of the lens with a spherometer. Plotting $D_n^2$ against $n$ gives a straight line of slope $4\lambda R$, so $\lambda = \dfrac{\text{slope}}{4R}$.

**OR: second maximum of the single slit.** The intensity of the Fraunhofer pattern of a slit of width $a$ is
$$\begin{gathered}I = I_0\left(\frac{\sin\alpha}\alpha\right)^2 \\ \alpha = \frac{\pi a\sin\theta}\lambda\end{gathered}$$
Setting $\dfrac{dI}{d\alpha} = 0$: $\dfrac{2\sin\alpha(\alpha\cos\alpha - \sin\alpha)}{\alpha^3} = 0$. Zeros of $\sin\alpha$ ($\alpha = n\pi$) are minima; the secondary maxima satisfy $\tan\alpha = \alpha$, with roots very nearly at $\alpha = \pm\dfrac{3\pi}2,\ \pm\dfrac{5\pi}2,\dots$ (first, second, ... secondary maxima).

For the second-order maximum $\alpha\approx\dfrac{5\pi}2$ and $\sin\alpha = 1$:
$$\frac I{I_0} = \left(\frac{1}{5\pi/2}\right)^2 = \left(\frac2{5\pi}\right)^2\approx0.0162$$
$$\boxed{I_2 = \left(\frac2{5\pi}\right)^2I_0}$$
(The first secondary maximum similarly gives $\left(\dfrac2{3\pi}\right)^2 = 0.045$.)

@s 5
For a wedge of angle $\theta$ and index $\mu$ in normal reflected light, the fringe width is
$$\beta = \frac\lambda{2\mu\theta}\ \Rightarrow\ \theta = \frac\lambda{2\mu\beta}$$
With $\lambda = 6000\ \text{Å} = 6\times10^{-7}$ m, $\mu = 1.4$, $\beta = 2\times10^{-3}$ m:
$$\theta = \frac{6\times10^{-7}}{2(1.4)(2\times10^{-3})} = 1.071\times10^{-4}\ \text{rad}$$
$$\boxed{\theta\approx1.07\times10^{-4}\ \text{rad}\approx6.1\times10^{-3}\ \text{degree}\approx22''}$$

@s 6
Data: $\mu_o = 1.65$, $\mu_e = 1.55$, $\mu_o - \mu_e = 0.10$, $\lambda = 6\times10^{-7}$ m. A plate of thickness $t$ introduces a path difference $(\mu_o - \mu_e)t$ and a phase difference $\delta = \dfrac{2\pi}\lambda(\mu_o-\mu_e)t$ between the O and E components.

**(i) Plane polarized emergent light.** A **half-wave plate** introduces a path difference $\dfrac\lambda2$ (phase difference $\pi$), which turns plane polarized light into plane polarized light with its plane rotated by $2\theta$. Minimum thickness:
$$t = \frac\lambda{2(\mu_o-\mu_e)} = \frac{6\times10^{-7}}{2(0.10)}$$
$$\boxed{t = 3\times10^{-6}\ \text{m} = 3\ \mu\text{m}\ \ (\text{odd multiples }(2m+1)\,3\ \mu\text{m};\ \text{a full-wave plate, }6\ \mu\text{m, also keeps it plane})}$$

**(ii) Elliptically polarized emergent light.** When the phase difference is neither $0$, $\pi$ nor a multiple of these, the vibrations of the E and O rays combine into an ellipse. A **quarter-wave plate** (phase difference $\pi/2$) with plane polarized light incident at an angle other than $45^\circ$ to the optic axis gives elliptical light with its axes along and perpendicular to the optic axis (at exactly $45^\circ$ the light is circular):
$$t = \frac\lambda{4(\mu_o-\mu_e)} = \frac{6\times10^{-7}}{4(0.10)}$$
$$\boxed{t = 1.5\times10^{-6}\ \text{m} = 1.5\ \mu\text{m}}$$
(any other thickness, for example $t = \lambda/8(\mu_o-\mu_e) = 0.75\ \mu$m for $\delta = \pi/4$, also gives elliptically polarized light for any orientation of the incident plane).

@s 7
**Equivalent focal length.** Let two thin convex lenses of focal lengths $f_1$ and $f_2$ be coaxial and separated by $d$. A ray parallel to the axis at height $h$ falls on lens 1.

```figure caption="Question 7: a ray parallel to the axis is refracted by L1 towards its focus and then by L2; the emergent ray, extended back, meets the incident ray at the second principal plane H2, and the focal length F is measured from there."
fig,ax=plt.subplots(figsize=(6.0,2.8))
ax.plot([-1,9],[0,0],color='#999',lw=0.8)
for x,lab in [(2,'L$_1$'),(5,'L$_2$')]:
    ax.annotate('',xy=(x,1.6),xytext=(x,-1.6),arrowprops=dict(arrowstyle='<->',color='#1d6fb8',lw=1.6)); ax.text(x,1.75,lab,ha='center',fontsize=9)
h=1.0; f1=4.0; f2=3.0; d=3.0
h2=h-d*h/f1; F=1/(1/f1+1/f2-d/(f1*f2))
ax.plot([-1,2],[h,h],color='#d9534f'); ax.plot([2,5],[h,h2],color='#d9534f')
x_f=5+h2/(h/F)
ax.plot([5,x_f],[h2,0],color='#d9534f')
ax.plot([5-d*F/f1,5-d*F/f1],[-1.2,1.2],color='#2e8b57',ls='--'); ax.text(5-d*F/f1,-1.55,'$H_2$',color='#2e8b57',ha='center',fontsize=9)
ax.plot([x_f],[0],'o',color='#14181f',ms=4); ax.text(x_f,-0.35,'$F_2$',ha='center',fontsize=9)
ax.plot([5-d*F/f1,5-d*F/f1+0],[h,h],'o',color='#14181f',ms=3)
ax.plot([5-d*F/f1,x_f],[-0.8,-0.8],color='#b8860b'); ax.text((5-d*F/f1+x_f)/2,-1.1,'$F$',color='#b8860b',ha='center',fontsize=9)
ax.text(-0.9,h+0.1,'$h$',fontsize=9)
ax.set_xlim(-1,9); ax.set_ylim(-1.8,2.0); ax.axis('off')
```

Lens 1 alone would converge the ray to its focus with slope $\dfrac h{f_1}$. At lens 2 the ray height is $h_2 = h - d\dfrac h{f_1} = h\left(1 - \dfrac d{f_1}\right)$. Lens 2 adds a convergence $\dfrac{h_2}{f_2}$, so the final slope toward the axis is
$$u = \frac h{f_1} + \frac{h_2}{f_2} = h\left[\frac1{f_1} + \frac1{f_2} - \frac d{f_1f_2}\right] \equiv\frac hF$$
$$\boxed{\frac1F = \frac1{f_1} + \frac1{f_2} - \frac d{f_1f_2}\quad\Rightarrow\quad F = \frac{f_1f_2}{f_1+f_2-d}}$$

**Principal points.** The emergent ray, extended backward, meets the incident ray (height $h$) at the **second principal plane** $H_2$. The ray falls from height $h_2$ (at $L_2$) to height $h$ over a horizontal distance
$$\beta = \frac{h - h_2}{h/F} = \frac{dh/f_1}{h/F}\ \Rightarrow\ \boxed{\beta = \frac{Fd}{f_1}}$$
measured from lens 2 **towards lens 1** (i.e. inside the system for $F>0$, $d$ not too large).

By reversibility, for a ray incident from the right, the **first principal plane** $H_1$ is at
$$\boxed{\alpha = \frac{Fd}{f_2}}$$
from lens 1 **towards lens 2**. The first and second focal points lie $F$ before $H_1$ and $F$ beyond $H_2$ respectively. (Example $f_1 = f_2 = 8$, $d = 4$ cm: $F = 5.33$ cm, $\alpha = \beta = 2.67$ cm.)

@s 8
**Acceptance angle.** The maximum angle $\theta_0$ with the fibre axis (in the surrounding medium) at which light can be launched into the fibre such that it is totally internally reflected inside, is the **acceptance angle**. The cone with this half angle is the acceptance cone.

```figure caption="Question 8: light enters from a medium of index n0 at angle θ0 (the acceptance angle) and is refracted at θr; at the core-cladding interface the angle of incidence is φ = 90° − θr, equal to the critical angle at the limit."
fig,ax=plt.subplots(figsize=(6.0,2.2))
ax.add_patch(plt.Rectangle((0,-0.7),8,1.4,fc='#e8eef7',ec='#1d6fb8'))
ax.add_patch(plt.Rectangle((0,0.7),8,0.5,fc='#d9dde3',ec='#1d6fb8')); ax.add_patch(plt.Rectangle((0,-1.2),8,0.5,fc='#d9dde3',ec='#1d6fb8'))
ax.plot([-2,0],[-0.93,0],color='#d9534f')
ax.plot([0,2.4],[0,0.7],color='#d9534f'); ax.plot([2.4,5.6],[0.7,-0.7],color='#d9534f'); ax.plot([5.6,8],[-0.7,0],color='#d9534f')
ax.plot([-2,8],[0,0],color='#999',ls=':')
ax.text(-1.7,-0.6,'$n_0$',fontsize=9); ax.text(3.8,0.0,'core $n_1$',fontsize=8); ax.text(3.4,0.95,'cladding $n_2$',fontsize=8)
ax.text(-0.9,0.12,'$\\theta_0$',fontsize=9,color='#d9534f'); ax.text(0.5,-0.3,'$\\theta_r$',fontsize=9,color='#d9534f'); ax.text(2.0,0.25,'$\\varphi$',fontsize=9,color='#d9534f')
ax.set_xlim(-2.2,8.2); ax.set_ylim(-1.3,1.4); ax.axis('off')
```

**Derivation.** At the entrance face, Snell's law: $n_0\sin\theta_0 = n_1\sin\theta_r$. Inside the core the ray meets the core-cladding boundary at angle $\varphi = 90^\circ - \theta_r$. For total internal reflection $\varphi\ge\varphi_c$ where $\sin\varphi_c = \dfrac{n_2}{n_1}$. At the limit $\varphi = \varphi_c$:
$$\sin\theta_r = \cos\varphi_c = \sqrt{1 - \frac{n_2^2}{n_1^2}}$$
$$n_0\sin\theta_{0,max} = n_1\sin\theta_r = \sqrt{n_1^2 - n_2^2}$$
For air $n_0 = 1$:
$$\boxed{\theta_0 = \sin^{-1}\sqrt{n_1^2 - n_2^2}}$$
**Numerical aperture** is the light-gathering capacity, $\text{N.A.} = n_0\sin\theta_0$:
$$\boxed{\text{N.A.} = \sqrt{n_1^2 - n_2^2}}$$
**In terms of $\Delta$.** With the fractional index difference $\Delta = \dfrac{n_1-n_2}{n_1}$, $n_1 - n_2 = n_1\Delta$ and $n_1 + n_2\approx2n_1$ (since $\Delta\ll1$):
$$n_1^2 - n_2^2 = (n_1-n_2)(n_1+n_2)\approx n_1\Delta(2n_1) = 2n_1^2\Delta$$
$$\boxed{\text{N.A.} = n_1\sqrt{2\Delta}}\ \ (n_1 = \mu_1)$$
$\blacksquare$

@s 9
**Field on the axis of a uniformly charged ring.** Let a ring of radius $R$ carry a total charge $Q$ uniformly distributed over it. Take $P$ on the axis at distance $x$ from the centre.

```figure caption="Question 9: an element dq of the ring produces dE at P with an axial component dE cos θ; the perpendicular components cancel in pairs."
fig,ax=plt.subplots(figsize=(4.4,2.6))
ax.plot([-0.3,4.5],[0,0],color='#999',lw=0.8)
ax.plot([0,0],[-1.4,1.4],color='#1d6fb8',lw=2.2)
ax.plot([0,3.2],[1.4,0],color='#d9534f'); ax.plot([0,3.2],[-1.4,0],color='#d9534f')
ax.plot([3.2],[0],'o',color='#14181f',ms=4); ax.text(3.25,0.15,'P',fontsize=9)
ax.annotate('',xy=(4.3,0),xytext=(3.2,0),arrowprops=dict(arrowstyle='->',color='#2e8b57')); ax.text(3.6,-0.4,'$dE\\cos\\theta$',color='#2e8b57',fontsize=8)
ax.plot([0,0],[0,1.4],color='#b8860b',ls='--'); ax.text(0.1,0.6,'$R$',color='#b8860b',fontsize=9)
ax.text(1.4,-0.3,'$x$',fontsize=9); ax.text(1.5,0.8,'$r$',color='#d9534f',fontsize=9); ax.text(2.4,0.12,'$\\theta$',fontsize=8)
ax.set_xlim(-0.5,4.8); ax.set_ylim(-1.7,1.7); ax.axis('off')
```

An element $dq = \dfrac{Q}{2\pi R}dl$ is at distance $r = \sqrt{R^2+x^2}$ from $P$:
$$dE = \frac1{4\pi\varepsilon_0}\frac{dq}{r^2}$$
By symmetry the components perpendicular to the axis cancel, leaving $dE_x = dE\cos\theta$ with $\cos\theta = \dfrac xr$:
$$E = \oint\frac{1}{4\pi\varepsilon_0}\frac{dq}{r^2}\frac xr = \frac{x}{4\pi\varepsilon_0(R^2+x^2)^{3/2}}\oint dq$$
$$\boxed{E = \frac{1}{4\pi\varepsilon_0}\frac{Qx}{(R^2+x^2)^{3/2}}}$$
along the axis, away from the ring for $Q>0$. $E = 0$ at the centre ($x = 0$) and $E\to\dfrac{Q}{4\pi\varepsilon_0x^2}$ for $x\gg R$.

**Maximum field.** Set $\dfrac{dE}{dx} = 0$:
$$\frac{d}{dx}\left[x(R^2+x^2)^{-3/2}\right] = (R^2+x^2)^{-3/2} - 3x^2(R^2+x^2)^{-5/2} = 0\ \Rightarrow\ R^2 + x^2 = 3x^2$$
$$\boxed{x = \pm\frac R{\sqrt2}}$$
(a maximum, since $E$ rises from $0$ at the centre and falls to $0$ at infinity). The maximum value is
$$E_{max} = \frac{Q}{4\pi\varepsilon_0}\cdot\frac{R/\sqrt2}{(3R^2/2)^{3/2}} = \frac{Q}{6\sqrt3\,\pi\varepsilon_0R^2}$$

**OR: electric quadrupole.** An **electric quadrupole** is a system of two equal and opposite dipoles placed end to end so that the net charge and net dipole moment are zero. A **linear quadrupole** is a charge $+q$ at $z=-a$, $-2q$ at the origin and $+q$ at $z=+a$. Its **quadrupole moment** is
$$Q = \sum q_iz_i^2 = q a^2 + 0 + q a^2 = 2qa^2$$
**Potential on the axis** at distance $r\gg a$:
$$V = \frac{q}{4\pi\varepsilon_0}\left[\frac1{r-a} + \frac1{r+a} - \frac2r\right] = \frac q{4\pi\varepsilon_0}\cdot\frac{2a^2}{r(r^2-a^2)}$$
For $r\gg a$, $r^2 - a^2\approx r^2$:
$$\boxed{V\approx\frac{2qa^2}{4\pi\varepsilon_0r^3} = \frac{Q}{4\pi\varepsilon_0}\frac1{r^3}\ \propto\ r^{-3}}$$
$\blacksquare$

@s 10
**Steps to calculate the capacitance of a capacitor.**

1. Assume charges $+Q$ and $-Q$ on the two conductors.
2. Find the electric field $\vec E$ between the conductors (usually with Gauss's law, using the symmetry).
3. Find the potential difference $V = -\displaystyle\int_-^+\vec E\cdot d\vec l$ between the conductors.
4. Compute $C = \dfrac QV$ (it depends only on geometry and the dielectric).

**Cylindrical capacitor.** Two coaxial cylinders of radii $a$ (inner) and $b$ (outer), length $L\gg b$, carry $+Q$ and $-Q$. Take a coaxial Gaussian cylinder of radius $r$ ($a<r<b$) and length $l$. The charge enclosed is $\dfrac QLl$ and the field is radial:
$$E(2\pi rl) = \frac{Ql}{L\varepsilon_0}\ \Rightarrow\ E = \frac{Q}{2\pi\varepsilon_0Lr}$$
$$V = -\int_b^aE\,dr = \frac{Q}{2\pi\varepsilon_0L}\int_a^b\frac{dr}r = \frac{Q}{2\pi\varepsilon_0L}\ln\frac ba$$
$$\boxed{C = \frac QV = \frac{2\pi\varepsilon_0L}{\ln(b/a)}}$$
Thus for a given length $C\propto\dfrac1{\ln(b/a)}$: the capacitance is inversely proportional to the logarithm of the ratio of outer to inner radius. $\blacksquare$ (With a dielectric of constant $K$ replace $\varepsilon_0$ by $K\varepsilon_0$.)

@s 11
Number density of free electrons (one per copper atom):
$$n = \frac{\rho N_A}{M} = \frac{(8.95\ \text{g cm}^{-3})(6.02\times10^{23})}{63.5\ \text{g}} = 8.485\times10^{22}\ \text{cm}^{-3} = 8.485\times10^{28}\ \text{m}^{-3}$$
The drift speed from $I = nAev_d$:
$$v_d = \frac I{nAe} = \frac{5}{(8.485\times10^{28})(3.31\times10^{-6})(1.6\times10^{-19})} = \frac5{4.494\times10^4}$$
$$\boxed{v_d\approx1.11\times10^{-4}\ \text{m/s}\approx0.11\ \text{mm/s}}$$

@s 12
**Comparison.**

| Biot-Savart law | Ampere's circuital law |
|---|---|
| $d\vec B = \dfrac{\mu_0}{4\pi}\dfrac{i\,d\vec l\times\hat r}{r^2}$, field of a current element | $\oint\vec B\cdot d\vec l = \mu_0i_{enc}$ |
| General: any current distribution | Practical only for symmetric distributions (wire, solenoid, toroid) |
| Needs integration over the whole conductor | Needs an Amperian loop only |
| Magnetic analogue of Coulomb's law | Magnetic analogue of Gauss's law |

**Field of a long straight wire** of radius $R$ carrying a uniform current $i$. By symmetry $\vec B$ is tangential and has a constant magnitude at a constant distance $r$ from the axis. Use a circular Amperian loop of radius $r$.

*Outside ($r>R$):* $B(2\pi r) = \mu_0i$
$$\boxed{B = \frac{\mu_0i}{2\pi r}}$$
*Inside ($r<R$):* the enclosed current is $i_{enc} = i\dfrac{\pi r^2}{\pi R^2} = \dfrac{ir^2}{R^2}$, so $B(2\pi r) = \mu_0\dfrac{ir^2}{R^2}$
$$\boxed{B = \frac{\mu_0ir}{2\pi R^2}}$$
$B$ rises linearly from $0$ at the axis to $\dfrac{\mu_0i}{2\pi R}$ at the surface and then falls as $1/r$.

```figure caption="Question 12: B of a long straight wire as a function of distance r from the axis: linear inside the wire (r < R) and falling as 1/r outside."
r=np.linspace(0.001,4,400)
B=np.where(r<1,r,1/r)
fig,ax=plt.subplots(figsize=(4.2,2.6))
ax.plot(r,B,color='#1d6fb8',lw=1.8); ax.axvline(1,color='#999',ls=':')
ax.text(0.5,0.2,'$B\\propto r$',fontsize=8,color='#1d6fb8'); ax.text(2,0.6,'$B\\propto 1/r$',fontsize=8,color='#1d6fb8')
ax.set_xticks([1]); ax.set_xticklabels(['R']); ax.set_xlabel('$r$',fontsize=9); ax.set_ylabel('$B$',fontsize=9)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

**OR: Hall effect.** When a current-carrying conductor (or semiconductor) is placed in a magnetic field perpendicular to the current, a transverse potential difference (the **Hall voltage**) appears across the conductor perpendicular to both the current and the field.

**Derivation.** Take a slab of thickness $t$ (along $B$), width $w$, with current $I$ along $x$, field $B$ along $z$, and carriers of charge $q$ and number density $n$. The magnetic force $qv_dB$ pushes the carriers to one side; charge accumulates there until the Hall electric field $E_H$ balances it:
$$\begin{gathered}qE_H = qv_dB\ \Rightarrow\ E_H = v_dB \\ V_H = E_Hw = v_dBw\end{gathered}$$
Using $J = \dfrac I{wt} = nqv_d$, so $v_d = \dfrac{I}{nqwt}$:
$$V_H = \frac{BI}{nqt}$$
**Hall coefficient:**
$$\boxed{R_H = \frac{E_H}{JB} = \frac{1}{nq}\ \ \left(= -\frac1{ne}\ \text{for electrons},\ +\frac1{pe}\ \text{for holes}\right)}$$
**Hall resistance:**
$$\boxed{R_{xy} = \frac{V_H}{I} = \frac{B}{nqt} = \frac{R_H}{t}B}$$
**Variation with $B$.** $R_{xy}$ is **directly proportional to the magnetic field** (a straight line through the origin of slope $R_H/t$); the sign of the slope tells whether the carriers are electrons or holes. In a two-dimensional electron gas at very low temperature and very high field, the line breaks into plateaus at $R_{xy} = \dfrac{h}{\nu e^2}$ (quantum Hall effect).

```figure caption="Question 12 (OR): Hall resistance against B: linear in the classical regime (dashed line) and quantized steps R = h/(νe²) in a 2-D electron gas at high B and low temperature."
B=np.linspace(0,10,400)
fig,ax=plt.subplots(figsize=(4.2,2.6))
ax.plot(B,0.8*B,color='#1d6fb8',lw=1.6,ls='--')
nu=10/B
nr=np.maximum(np.round(nu),1)
R=np.where(nu<5.5,8/nr,0.8*B)
ax.plot(B,R,color='#d9534f',lw=1.4)
ax.text(0.6,4.2,'classical',fontsize=8,color='#1d6fb8',rotation=32); ax.text(4.2,1.0,'quantum Hall plateaus',fontsize=8,color='#d9534f')
ax.set_xlabel('$B$',fontsize=9); ax.set_ylabel('$R_{xy}$',fontsize=9); ax.set_ylim(0,8)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 13
In a cyclotron the frequency of the oscillator equals the cyclotron frequency $f = \dfrac{qB}{2\pi m}$.

**Magnetic flux density:**
$$B = \frac{2\pi fm}{q} = \frac{2\pi(10^7)(3.32\times10^{-27})}{1.6\times10^{-19}} = \frac{2.086\times10^{-19}}{1.6\times10^{-19}}$$
$$\boxed{B\approx1.30\ \text{T}}$$
**Velocity of emerging deuterons** at $r = 0.3$ m: $v = \dfrac{qBr}{m} = 2\pi fr$
$$v = 2\pi(10^7)(0.3) = 1.885\times10^7\ \text{m/s}$$
$$\boxed{v\approx1.88\times10^7\ \text{m/s}}$$
(about $6\ \%$ of the speed of light, so the non-relativistic treatment is acceptable). The kinetic energy is $\tfrac12mv^2 = 5.9\times10^{-13}$ J $\approx3.7$ MeV.

@s 14
At the centre of a circular coil of $N$ turns, radius $R$ and current $i$:
$$B = \frac{N\mu_0i}{2R} = \frac{20(4\pi\times10^{-7})(2)}{2(0.02)} = \frac{5.027\times10^{-5}}{0.04}$$
$$\boxed{B\approx1.26\times10^{-3}\ \text{T} = 1.26\ \text{mT}}$$

@s 15
**Maxwell's equations.** In free space (with charge density $\rho$ and current density $\vec J$):

| # | Differential form | Integral form | Physical significance |
|---|---|---|---|
| 1 | $\nabla\cdot\vec E = \dfrac\rho{\varepsilon_0}$ | $\oint\vec E\cdot d\vec A = \dfrac{q_{enc}}{\varepsilon_0}$ | **Gauss's law (electric).** Electric charges are the sources of the electric field; the flux out of a closed surface equals the enclosed charge$/\varepsilon_0$. |
| 2 | $\nabla\cdot\vec B = 0$ | $\oint\vec B\cdot d\vec A = 0$ | **Gauss's law (magnetism).** There are no magnetic monopoles; magnetic field lines are closed loops. |
| 3 | $\nabla\times\vec E = -\dfrac{\partial\vec B}{\partial t}$ | $\oint\vec E\cdot d\vec l = -\dfrac{d\Phi_B}{dt}$ | **Faraday's law.** A changing magnetic field induces an electric field (emf). |
| 4 | $\nabla\times\vec B = \mu_0\vec J + \mu_0\varepsilon_0\dfrac{\partial\vec E}{\partial t}$ | $\oint\vec B\cdot d\vec l = \mu_0\left(i + \varepsilon_0\dfrac{d\Phi_E}{dt}\right)$ | **Ampere-Maxwell law.** Currents and changing electric fields (displacement current) produce magnetic fields. |

**Conversion to integral form.**

- Equation 1: integrate over a volume and use the divergence theorem $\int_V\nabla\cdot\vec E\,dV = \oint_S\vec E\cdot d\vec A$ and $\int\rho\,dV = q_{enc}$.
- Equation 2: same with $\nabla\cdot\vec B = 0$.
- Equation 3: integrate over an open surface and use Stokes' theorem $\int_S(\nabla\times\vec E)\cdot d\vec A = \oint_C\vec E\cdot d\vec l$ and $\int\vec B\cdot d\vec A = \Phi_B$.
- Equation 4: Stokes' theorem on $\vec B$, with $\int\vec J\cdot d\vec A = i$ and $\int\varepsilon_0\dfrac{\partial\vec E}{\partial t}\cdot d\vec A = \varepsilon_0\dfrac{d\Phi_E}{dt}$.

Taken together (in free space, $\rho = 0$, $\vec J = 0$) they predict electromagnetic waves travelling with speed $c = \dfrac1{\sqrt{\mu_0\varepsilon_0}}$.

@s 16
**Time-dependent Schrödinger equation.** A free particle of momentum $p$ and energy $E$ is described by the plane wave
$$\begin{gathered}\psi(x,t) = Ae^{i(kx-\omega t)} = Ae^{\frac i\hbar(px - Et)} \\ k = \frac p\hbar,\ \omega = \frac E\hbar\end{gathered}$$
Differentiating,
$$\frac{\partial\psi}{\partial t} = -\frac{iE}\hbar\psi\ \Rightarrow\ E\psi = i\hbar\frac{\partial\psi}{\partial t}$$
$$\frac{\partial^2\psi}{\partial x^2} = -\frac{p^2}{\hbar^2}\psi\ \Rightarrow\ p^2\psi = -\hbar^2\frac{\partial^2\psi}{\partial x^2}$$
With total energy $E = \dfrac{p^2}{2m} + V$ (kinetic plus potential), $E\psi = \dfrac{p^2}{2m}\psi + V\psi$, so
$$\boxed{i\hbar\frac{\partial\psi}{\partial t} = -\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2} + V(x,t)\psi}$$
In three dimensions, $i\hbar\dfrac{\partial\psi}{\partial t} = -\dfrac{\hbar^2}{2m}\nabla^2\psi + V\psi$. For $V = V(x)$ only, $\psi = \phi(x)e^{-iEt/\hbar}$ gives the time-independent equation $\dfrac{d^2\phi}{dx^2} + \dfrac{2m}{\hbar^2}(E-V)\phi = 0$.

**Physical significance of $\psi$.**

- $\psi$ is the complex amplitude of the matter wave; it is not itself measurable.
- $|\psi|^2 = \psi\psi^*$ is the **probability density**: $|\psi|^2dV$ is the probability of finding the particle in the volume $dV$ at time $t$.
- Normalization: $\displaystyle\int_{-\infty}^\infty|\psi|^2dV = 1$ (the particle must be somewhere).
- $\psi$ must be single valued, finite, continuous and have a continuous derivative (square-integrable), so that probabilities are well defined.
- Expectation values of observables follow from $\psi$, e.g. $\langle x\rangle = \int\psi^*x\psi\,dx$.

---
file: NEBians-IOE-Past-Paper-Engineering-Physics-SH402-2081-Bhadra.pdf
subject: Engineering Physics
level: BE · Year I / Part I
code: SH 402
year_bs: 2081 Bhadra
cal: BS
year_ad: 2024
stream: BEL, BEX, BEI, BCT, BAM, BIE, BAG, BAS
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 402). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary.</small>

@q 1
Show that the motion of torsional pendulum is angular simple harmonic in nature and find the time period of torsional pendulum. [[3+2]]

**OR**

Derive the differential equation of LC oscillation and find its frequency. [[5]]

@q 2
A mass of $1\ \text{kg}$ is suspended from a spring of spring constant $25\ \text{N/m}$. If the undamped frequency is $\dfrac{2}{\sqrt3}$ times the damped frequency, what will be the damping factor? [[5]]

@q 3
The volume of a room is $980\ \text{m}^3$. The wall area of the room is $140\ \text{m}^2$, ceiling floor area is $85\ \text{m}^2$. The average sound absorption coefficient (i) for wall is $0.03$, (ii) for ceiling is $0.80$ and (iii) for the floor is $0.06$, calculate the average sound absorption coefficient and reverberation time. [[2.5+2.5]]

@q 4
What are Newton's rings? Show that the radius of $n$th bright ring in reflected system is proportional to square root of odd natural number and that of $n$th dark ring is proportional to square root of natural number in Newton's ring. [[5]]

**OR**

Show that both dispersive power and resolving power of grating are proportional to the number of order. [[5]]

@q 5
Light of wavelength $600\ \text{nm}$ is incident normally on a slit of width $0.1\ \text{mm}$. What is the intensity at $\theta = 0.3^\circ$ in terms of the intensity of central maximum? [[5]]

@q 6
A $200\ \text{mm}$ long glass tube is filled with a solution of sugar, containing $15\ \text{gram}$ of sugar in $100\ \text{ml}$ of water. The plane of polarized light, passing through this solution, is rotated through $20^\circ$. Find the specific rotation of sugar. [[5]]

@q 7
Derive the expression for the equivalent focal length of two thin lenses having focal lengths $f_1$ and $f_2$ separated by a finite distance. Also find the expression for equivalent power. [[4+1]]

@q 8
Name the principle on which optical fiber works. Derive the expressions for acceptance angle and numerical aperture of optical fiber. [[1+2+2]]

@q 9
Derive an expression for the electric field intensity due to a uniformly distributed charged plastic ring at a point on its axis. [[5]]

**OR**

Derive the expression for energy stored in a capacitor and hence show that the electrical energy density is proportional to square of the electric field. [[5]]

@q 10
Over certain region of space, the electric potential is $V = (2x - x^2y + y^2z)\ \text{volt}$. Find the expressions for the $x$, $y$ and $z$ components of the electric field over this region. What is the magnitude of the field at a point that has coordinates $(1, 3, -2)\ \text{m}$? [[5]]

@q 11
A typical copper wire of household wiring has a cross-sectional area $3.3\times10^{-6}\ \text{m}^2$ and carries a current of $6\ \text{A}$. What is the drift speed of the electrons? Given, density of copper is $8.95\times10^{3}\ \text{kg m}^{-3}$, Avogadro's number $6.02\times10^{23}\ \text{mol}^{-1}$, molar mass of copper is $63.5\ \text{gm}$. [[5]]

@q 12
Compare Ampere's law with Biot-Savart's law. Calculate the magnetic field inside and outside a long straight wire carrying current $I$. [[1+2+2]]

**OR**

What is Hall effect? Derive the expressions for Hall coefficient and Hall voltage. [[5]]

@q 13
A physicist designed a cyclotron to accelerate protons to $1/10^{\text{th}}$ the speed of light. The magnet used will produce a field of $1.4\ \text{T}$. Calculate (i) the radius of the cyclotron (ii) the corresponding oscillator frequency. [[2.5+2.5]]

@q 14
A solenoid having an inductance of $6.3\ \mu\text{H}$ is connected in series with a $1.2\ \text{k}\Omega$ resistor. If a $14\ \text{V}$ battery is connected across the pair, how long will it take for the current through the resistor to reach $90\%$ of its final value? [[5]]

@q 15
What is Poynting vector? Show that the intensity of electromagnetic wave in free space is proportional to square of the amplitude of electric field. [[1+4]]

@q 16
An electron is confined in one dimensional infinite potential well. Show that energy levels are quantized. Also derive the wave function. [[3+2]]
<!-- SOLUTIONS -->

@s 1
**Torsional pendulum.** A rigid body (disc, bob) hung from a fixed point by a wire and free to rotate about the wire's axis is a torsional pendulum.

If the body is twisted through a small angle $\theta$, the wire exerts a restoring torque proportional to the twist (within the elastic limit):
$$\tau = -C\theta$$
where $C$ is the torsional constant (torque per unit twist) of the wire. Newton's law for rotation, $\tau = I\alpha = I\dfrac{d^2\theta}{dt^2}$, with $I$ the moment of inertia about the wire, gives
$$I\frac{d^2\theta}{dt^2} = -C\theta\ \Rightarrow\ \frac{d^2\theta}{dt^2} + \frac{C}{I}\theta = 0$$
This is the equation $\ddot\theta + \omega^2\theta = 0$ of **angular simple harmonic motion** (the angular acceleration is proportional to the angular displacement and opposite to it), with $\omega^2 = C/I$. Its solution is $\theta = \theta_0\sin(\omega t + \phi)$.

$$\boxed{\omega = \sqrt{\frac CI},\qquad T = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac IC}}$$
For a wire of length $l$, radius $r$ and rigidity modulus $\eta$, $C = \dfrac{\pi\eta r^4}{2l}$.

**OR: LC oscillation.** Consider an ideal capacitor $C$, charged to $q_0$, connected to an inductor $L$ (no resistance). At any instant let the capacitor charge be $q$ and the current $i = \dfrac{dq}{dt}$. Kirchhoff's voltage law around the loop:
$$L\frac{di}{dt} + \frac qC = 0$$
Using $i = dq/dt$:
$$\boxed{\frac{d^2q}{dt^2} + \frac{1}{LC}\,q = 0}$$
This is the equation of SHM with $\omega_0^2 = \dfrac1{LC}$, so $q = q_0\cos(\omega_0 t + \phi)$ and $i = -\omega_0 q_0\sin(\omega_0 t + \phi)$:
$$\boxed{\omega_0 = \frac{1}{\sqrt{LC}},\qquad f = \frac{1}{2\pi\sqrt{LC}}}$$
Energy: $U = \dfrac{q^2}{2C} + \tfrac12Li^2 = \dfrac{q_0^2}{2C}$ stays constant, and swaps between the electric and magnetic forms.

@s 2
Mass $m = 1$ kg, $k = 25$ N/m. Undamped angular frequency:
$$\omega_0 = \sqrt{\frac km} = \sqrt{25} = 5\ \text{rad/s}$$
Damped oscillation: $m\ddot x + b\dot x + kx = 0$, $\omega_d = \sqrt{\omega_0^2 - \gamma^2}$ with $\gamma = \dfrac{b}{2m}$.

Given $\omega_0 = \dfrac{2}{\sqrt3}\,\omega_d$, so $\omega_d^2 = \dfrac34\omega_0^2$:
$$\gamma^2 = \omega_0^2 - \omega_d^2 = \frac{\omega_0^2}{4}\ \Rightarrow\ \gamma = \frac{\omega_0}{2} = 2.5\ \text{s}^{-1}$$
The damping constant is $b = 2m\gamma = 2(1)(2.5) = 5\ \text{kg/s}$ and the dimensionless damping factor (damping ratio) is
$$\zeta = \frac{\gamma}{\omega_0} = \frac{b}{2\sqrt{km}} = \frac{2.5}{5}$$
$$\boxed{\zeta = 0.5\quad(\gamma = 2.5\ \text{s}^{-1},\ b = 5\ \text{kg/s})}$$
$\zeta<1$: the motion is under-damped, as it should be.

@s 3
Absorption $A = \sum a_iS_i$:
$$\begin{gathered}A_{wall} = 0.03(140) = 4.2 \\ A_{ceiling} = 0.80(85) = 68.0 \\ A_{floor} = 0.06(85) = 5.1\end{gathered}$$
$$A = 4.2 + 68.0 + 5.1 = 77.3\ \text{m}^2\ \text{(sabine)}$$
Total area $S = 140 + 85 + 85 = 310\ \text{m}^2$.

**Average absorption coefficient**
$$\bar a = \frac{A}{S} = \frac{77.3}{310}$$
$$\boxed{\bar a \approx 0.249}$$
**Reverberation time (Sabine's formula)**
$$T = \frac{0.161\,V}{A} = \frac{0.161(980)}{77.3}$$
$$\boxed{T \approx 2.04\ \text{s}}$$

@s 4
**Newton's rings.** When a plano-convex lens of large radius of curvature $R$ is placed with its curved face on a flat glass plate and lit by monochromatic light from above, concentric alternately bright and dark circular fringes are seen about the point of contact. They come from interference between the light reflected from the top and the bottom of the air film between the lens and the plate.

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

**Geometry.** For a ring of radius $r$ where the film thickness is $t$: $r^2 = 2Rt - t^2\approx2Rt$ (as $t\ll R$), so $t = \dfrac{r^2}{2R}$.

**Path difference** for normal incidence in the air film ($\mu = 1$): $2t$ plus an extra $\lambda/2$ from the reflection at the denser glass plate (the ray reflected from the lens surface has no phase change):
$$\Delta = 2t + \frac\lambda2 = \frac{r^2}{R} + \frac\lambda2$$

**Bright rings** need $\Delta = n\lambda$ ($n = 1, 2, 3, \dots$):
$$\frac{r_n^2}{R} = n\lambda - \frac\lambda2 = \frac{(2n-1)\lambda}{2}$$
$$\boxed{r_n = \sqrt{\frac{(2n-1)\lambda R}{2}}\ \propto\ \sqrt{2n-1}}$$
i.e. the radii of bright rings are proportional to the square roots of the odd natural numbers $1, 3, 5, \dots$

**Dark rings** need $\Delta = (2n+1)\dfrac\lambda2$ ($n = 0, 1, 2, \dots$):
$$\frac{r_n^2}{R} = n\lambda$$
$$\boxed{r_n = \sqrt{n\lambda R}\ \propto\ \sqrt n}$$
i.e. the radii of dark rings are proportional to the square roots of the natural numbers; the centre ($n = 0$) is dark. $\blacksquare$

**OR: dispersive and resolving power of a grating.** Let $(a + b)$ be the grating element and $N$ the total number of lines. The principal maximum of order $n$ for wavelength $\lambda$ is at
$$(a+b)\sin\theta = n\lambda$$

**Dispersive power** is the angular separation per unit wavelength, $\dfrac{d\theta}{d\lambda}$. Differentiating:
$$(a+b)\cos\theta\,d\theta = n\,d\lambda\ \Rightarrow\ \boxed{\frac{d\theta}{d\lambda} = \frac{n}{(a+b)\cos\theta}\ \propto\ n}$$

**Resolving power** $R = \dfrac{\lambda}{d\lambda}$. By Rayleigh's criterion the $n$th maximum of $\lambda + d\lambda$ must fall on the first minimum next to the $n$th maximum of $\lambda$. The $n$th maximum of $\lambda + d\lambda$ is at $(a+b)\sin\theta = n(\lambda + d\lambda)$, and the first minimum next to the $n$th maximum of $\lambda$ is where the path difference across the whole grating is $n\lambda + \lambda/N$:
$$(a+b)\sin\theta = n\lambda + \frac\lambda N$$
Equating, $n\,d\lambda = \dfrac{\lambda}{N}$:
$$\boxed{R = \frac{\lambda}{d\lambda} = nN\ \propto\ n}$$
So both are proportional to the order $n$. $\blacksquare$

@s 5
For a single slit of width $a$, the intensity at angle $\theta$ is
$$\begin{gathered}I = I_0\left(\frac{\sin\alpha}{\alpha}\right)^2 \\ \alpha = \frac{\pi a\sin\theta}{\lambda}\end{gathered}$$
Data: $a = 0.1\ \text{mm} = 10^{-4}$ m, $\lambda = 600\ \text{nm} = 6\times10^{-7}$ m, $\theta = 0.3^\circ$, $\sin0.3^\circ = 5.236\times10^{-3}$.
$$\alpha = \frac{\pi(10^{-4})(5.236\times10^{-3})}{6\times10^{-7}} = 2.7415\ \text{rad}$$
$$\sin\alpha = \sin(2.7415) = 0.3895$$
$$\frac{I}{I_0} = \left(\frac{0.3895}{2.7415}\right)^2 = (0.1421)^2$$
$$\boxed{I\approx0.0202\,I_0\ \ (\approx2\%\ \text{of the central maximum})}$$
(This point lies between the central peak and the first minimum at $\alpha = \pi$, on the central maximum's falling edge.)

@s 6
Specific rotation is the rotation produced by a 1 dm column of solution of concentration 1 g/cm³:
$$[\alpha] = \frac{\theta}{l\,c}$$
$$\begin{gathered}\theta = 20^\circ,\quad l = 200\ \text{mm} = 2\ \text{dm} \\ c = \frac{15\ \text{g}}{100\ \text{cm}^3} = 0.15\ \text{g/cm}^3\end{gathered}$$
$$[\alpha] = \frac{20}{2\times0.15}$$
$$\boxed{[\alpha]\approx66.7^\circ\ \text{dm}^{-1}\,(\text{g/cm}^3)^{-1}}$$

@s 7
**Equivalent focal length of two thin coaxial lenses** $L_1$ ($f_1$) and $L_2$ ($f_2$) separated by $d$ (in air).

```figure caption="Question 7: a ray parallel to the axis at height h1 is refracted by L1 (towards its focus) and then by L2; the emergent ray meets the axis at the second focal point of the combination."
fig,ax=plt.subplots(figsize=(5.4,2.5))
ax.plot([-1,9],[0,0],color='#999',lw=.8)
for x,l in ((2,'$L_1$'),(5,'$L_2$')):
    ax.annotate('',xy=(x,1.3),xytext=(x,-1.3),arrowprops=dict(arrowstyle='<->',color='#14181f'))
    ax.text(x+.1,1.4,l,fontsize=9)
ax.plot([-1,2],[1,1],color='#1d6fb8',lw=1.3)
ax.plot([2,5],[1,0.25],color='#1d6fb8',lw=1.3)
ax.plot([5,8.5],[0.25,0.25-3.5*(0.25/2.5)],color='#d9534f',lw=1.3)
ax.plot([2,6],[1,0],color='#1d6fb8',ls=':',lw=.9)
ax.text(1.1,1.1,'$h_1$',fontsize=8); ax.text(5.05,0.45,'$h_2$',fontsize=8)
ax.annotate('',xy=(5,-0.9),xytext=(2,-0.9),arrowprops=dict(arrowstyle='<->',color='#2e8b57'))
ax.text(3.3,-1.15,'$d$',fontsize=9,color='#2e8b57')
ax.plot([7.5],[0],'o',color='#d9534f',ms=4); ax.text(7.55,-0.35,'$F$',fontsize=9)
ax.set_xlim(-1,9); ax.set_ylim(-1.5,1.7); ax.axis('off')
```

A ray parallel to the axis strikes $L_1$ at height $h_1$. $L_1$ alone would bring it to its focus, at distance $f_1$ behind $L_1$, so the ray makes a small angle $\alpha_1 = \dfrac{h_1}{f_1}$ with the axis (converging). It reaches $L_2$ at height
$$h_2 = h_1 - d\,\alpha_1 = h_1\left(1 - \frac{d}{f_1}\right)$$
$L_2$ deviates the ray further, by the angle $\dfrac{h_2}{f_2}$ (thin lens, small angles). The final slope of the emergent ray is therefore
$$\alpha = \frac{h_1}{f_1} + \frac{h_2}{f_2}$$
If $F$ is the equivalent focal length, a single lens must give the same slope for the same incident height: $\alpha = \dfrac{h_1}{F}$. Hence
$$\frac{h_1}{F} = \frac{h_1}{f_1} + \frac{h_1}{f_2}\left(1 - \frac{d}{f_1}\right)$$
$$\boxed{\frac1F = \frac1{f_1} + \frac1{f_2} - \frac{d}{f_1f_2}\quad\Rightarrow\quad F = \frac{f_1f_2}{f_1 + f_2 - d}}$$
**Equivalent power.** Power is $P = \dfrac1F$ (in dioptre if $F$ is in metres). With $P_1 = 1/f_1$, $P_2 = 1/f_2$:
$$\boxed{P = P_1 + P_2 - d\,P_1P_2}$$
For $d = 0$ (lenses in contact) the powers simply add, $P = P_1 + P_2$. $\blacksquare$

@s 8
**Principle.** An optical fibre works on **total internal reflection** (TIR): light travelling in the denser core $(n_1)$ strikes the core-cladding boundary $(n_2<n_1)$ at an angle larger than the critical angle $\theta_c = \sin^{-1}(n_2/n_1)$ and is completely reflected again and again along the fibre.

```figure caption="Question 8: ray entering the fibre at the acceptance angle theta_0 and striking the core-cladding boundary at the critical angle."
fig,ax=plt.subplots(figsize=(5.4,2.3))
ax.fill([0,6,6,0],[-.7,-.7,.7,.7],color='#dbe8f6')
ax.fill([0,6,6,0],[-.7,-.7,-1.0,-1.0],color='#c8ccd2'); ax.fill([0,6,6,0],[.7,.7,1.0,1.0],color='#c8ccd2')
ax.plot([-1.5,0],[-.9,0],color='#1d6fb8',lw=1.4)
ax.plot([0,1.1],[0,.7],color='#1d6fb8',lw=1.4)
ax.plot([1.1,2.9],[.7,-.7],color='#1d6fb8',lw=1.4)
ax.plot([2.9,4.7],[-.7,.7],color='#1d6fb8',lw=1.4)
ax.plot([-1.5,6],[0,0],color='#999',ls='--',lw=.7)
ax.text(-1.0,.12,r'$\theta_0$',fontsize=9,color='#d9534f')
ax.text(2.3,0.0,'core $n_1$',fontsize=9); ax.text(3.3,.8,'cladding $n_2$',fontsize=8)
ax.text(-1.5,-1.2,'air $n_0$',fontsize=8)
ax.set_xlim(-1.7,6.1); ax.set_ylim(-1.3,1.2); ax.axis('off')
```

**Acceptance angle.** Let a ray from a medium of index $n_0$ (air, $n_0 = 1$) enter the core face at angle $\theta_0$ with the axis, refract at angle $\theta_r$, and hit the core-cladding boundary at the critical angle $\theta_c$, so $\theta_r = 90^\circ - \theta_c$.

At the entrance face (Snell): $n_0\sin\theta_0 = n_1\sin\theta_r = n_1\cos\theta_c$.

At the boundary at the critical angle: $\sin\theta_c = \dfrac{n_2}{n_1}$, hence $\cos\theta_c = \sqrt{1 - \dfrac{n_2^2}{n_1^2}}$.
$$n_0\sin\theta_0 = n_1\sqrt{1 - \frac{n_2^2}{n_1^2}} = \sqrt{n_1^2 - n_2^2}$$
$$\boxed{\theta_0 = \sin^{-1}\!\left(\frac{\sqrt{n_1^2 - n_2^2}}{n_0}\right)}$$
Any ray entering within the cone of half-angle $\theta_0$ (the **acceptance angle**) is trapped by TIR. For larger entry angles the ray meets the boundary at less than $\theta_c$ and leaks into the cladding.

**Numerical aperture** is the light-gathering ability, $NA = n_0\sin\theta_0$:
$$\boxed{NA = \sqrt{n_1^2 - n_2^2}}\quad(\text{for air, }n_0 = 1:\ NA = \sin\theta_0)$$
With the fractional index difference $\Delta = \dfrac{n_1 - n_2}{n_1}$: $n_1^2 - n_2^2 = (n_1 - n_2)(n_1 + n_2)\approx2n_1^2\Delta$, so $NA\approx n_1\sqrt{2\Delta}$.

@s 9
**Field of a uniformly charged ring on its axis.** Let the ring have radius $R$ and total charge $Q$, and let $P$ be a point on the axis at distance $x$ from the centre.

```figure caption="Question 9: element dq of the ring; dE has an axial part dE cos(phi), and the perpendicular parts cancel in pairs."
fig,ax=plt.subplots(figsize=(4.6,2.6))
t=np.linspace(0,2*np.pi,200)
ax.plot(0.7*np.cos(t)*0.35-0.0, 1.2*np.sin(t)*0.0+0.7*np.sin(t),color='#14181f',lw=1.4)
ax.plot([-1,5],[0,0],color='#999',lw=.8)
ax.plot([0,4],[0,0],color='#2e8b57',lw=1.4); ax.text(2,-0.28,'$x$',color='#2e8b57')
ax.plot([0,0],[0,.7],color='#14181f',ls=':'); ax.text(-0.35,.3,'$R$')
ax.plot([0,4],[.7,0],color='#1d6fb8',lw=1.2); ax.text(1.5,.5,'$r$',color='#1d6fb8')
ax.annotate('',xy=(5.0,0),xytext=(4,0),arrowprops=dict(arrowstyle='->',color='#d9534f',lw=1.6)); ax.text(4.6,.12,r'$dE_x$',color='#d9534f',fontsize=8)
ax.annotate('',xy=(4.8,.3),xytext=(4,0),arrowprops=dict(arrowstyle='->',color='#999'))
ax.text(4.1,-.35,'P'); ax.text(-0.2,.85,'$dq$',fontsize=8)
ax.set_xlim(-1,5.4); ax.set_ylim(-.8,1.1); ax.axis('off')
```

Take a small charge element $dq = \dfrac{Q}{2\pi R}\,dl$. Its distance from $P$ is $r = \sqrt{R^2 + x^2}$, and it produces a field of magnitude
$$dE = \frac{1}{4\pi\varepsilon_0}\frac{dq}{r^2}$$
along the line joining $dq$ to $P$. Resolve it into a component along the axis, $dE\cos\phi$, and a component perpendicular to the axis, $dE\sin\phi$. Elements on opposite ends of a diameter have equal and opposite perpendicular components, so these cancel over the whole ring. Only the axial parts add. With $\cos\phi = \dfrac{x}{r}$:
$$E = \int dE\cos\phi = \frac{1}{4\pi\varepsilon_0}\frac{x}{r^3}\int dq = \frac{1}{4\pi\varepsilon_0}\frac{Qx}{(R^2 + x^2)^{3/2}}$$
$$\boxed{E = \frac{Q\,x}{4\pi\varepsilon_0\,(R^2 + x^2)^{3/2}}}$$
directed along the axis, away from the ring for $Q>0$.

*Checks.* At $x = 0$, $E = 0$. For $x\gg R$, $E\to\dfrac{Q}{4\pi\varepsilon_0x^2}$ (a point charge). The field is largest at $x = R/\sqrt2$, where $dE/dx = 0$.

**OR: energy stored in a capacitor.** While charging a capacitor $C$, suppose the charge is $q$ and the potential difference $V' = q/C$. To bring a further $dq$ across, the work done is $dW = V'\,dq = \dfrac qC\,dq$. Charging from $0$ to $Q$:
$$U = \int_0^Q\frac qC\,dq = \frac{Q^2}{2C}$$
$$\boxed{U = \frac{Q^2}{2C} = \tfrac12CV^2 = \tfrac12QV}$$
**Energy density.** For a parallel-plate capacitor of plate area $A$ and separation $d$: $C = \dfrac{\varepsilon_0A}{d}$, and $V = Ed$. Then
$$U = \tfrac12\frac{\varepsilon_0A}{d}(Ed)^2 = \tfrac12\varepsilon_0E^2\,(Ad)$$
$Ad$ is the volume in which the field exists, so the energy per unit volume is
$$\boxed{u = \frac{U}{Ad} = \tfrac12\varepsilon_0E^2\ \propto\ E^2}$$
This holds for any electric field in free space (for a dielectric, $u = \tfrac12\varepsilon_0\varepsilon_rE^2$). $\blacksquare$

@s 10
The field is $\vec E = -\nabla V$, so $E_x = -\dfrac{\partial V}{\partial x}$, etc. With $V = 2x - x^2y + y^2z$:
$$\begin{gathered}E_x = -\frac{\partial V}{\partial x} = -(2 - 2xy) = 2xy - 2 \\ E_y = -\frac{\partial V}{\partial y} = -(-x^2 + 2yz) = x^2 - 2yz \\ E_z = -\frac{\partial V}{\partial z} = -y^2\end{gathered}$$
At $(1, 3, -2)$ m:
$$\begin{gathered}E_x = 2(1)(3) - 2 = 4\ \text{V/m} \\ E_y = 1 - 2(3)(-2) = 13\ \text{V/m} \\ E_z = -9\ \text{V/m}\end{gathered}$$
$$|E| = \sqrt{4^2 + 13^2 + (-9)^2} = \sqrt{266}$$
$$\boxed{E_x = 2xy - 2,\ \ E_y = x^2 - 2yz,\ \ E_z = -y^2;\qquad |E|\approx16.3\ \text{V/m}}$$

@s 11
Drift speed: $I = nevA\ \Rightarrow\ v_d = \dfrac{I}{neA}$, where $n$ is the free-electron density (one free electron per Cu atom).
$$n = \frac{\rho N_A}{M} = \frac{(8.95\times10^3)(6.02\times10^{23})}{63.5\times10^{-3}} = 8.485\times10^{28}\ \text{m}^{-3}$$
$$v_d = \frac{6}{(8.485\times10^{28})(1.6\times10^{-19})(3.3\times10^{-6})} = \frac{6}{4.48\times10^4}$$
$$\boxed{v_d\approx1.34\times10^{-4}\ \text{m/s}\ (\approx0.13\ \text{mm/s})}$$

@s 12
**Comparison of Ampere's law and Biot-Savart's law**

| | Biot-Savart law | Ampere's circuital law |
|---|---|---|
| Statement | $d\vec B = \dfrac{\mu_0}{4\pi}\dfrac{I\,d\vec l\times\hat r}{r^2}$ | $\oint\vec B\cdot d\vec l = \mu_0I_{enc}$ |
| Use | Gives $B$ for any current distribution by integration | Gives $B$ easily only when there is symmetry (long wire, solenoid, toroid) |
| Nature | Current-element to field, like Coulomb's law | Closed loop to enclosed current, like Gauss's law |
| Validity | Steady currents (magnetostatics) | Steady currents; with Maxwell's displacement current it is general |

Both give the same result where both apply: Ampere's law is the integral form of $\nabla\times\vec B = \mu_0\vec J$ for steady currents, and Biot-Savart's law is its solution.

**Field of a long straight wire** of radius $R$ carrying a current $I$ uniformly over its cross-section. By symmetry the field lines are circles around the axis, with $B$ constant in magnitude on a circle of radius $r$. Take that circle as the Amperian loop: $\oint\vec B\cdot d\vec l = B(2\pi r)$.

```figure caption="Question 12: B versus r for a long straight wire of radius R: linear inside, 1/r outside."
r=np.linspace(0.001,3,300); R=1
B=np.where(r<R,r/R,R/r)
fig,ax=plt.subplots(figsize=(4.2,2.3))
ax.plot(r,B,color='#1d6fb8',lw=1.8)
ax.axvline(R,color='#999',ls='--',lw=.8)
ax.text(1.05,0.12,'$r=R$',fontsize=8)
ax.text(0.2,0.75,r'$B\propto r$',fontsize=9,color='#d9534f'); ax.text(1.6,0.7,r'$B\propto 1/r$',fontsize=9,color='#2e8b57')
ax.set_xlabel('$r$',fontsize=9); ax.set_ylabel('$B$',fontsize=9)
ax.set_xticks([]); ax.set_yticks([])
```

*Outside* ($r\ge R$): the loop encloses the whole current, $I_{enc} = I$:
$$B(2\pi r) = \mu_0I\ \Rightarrow\ \boxed{B = \frac{\mu_0I}{2\pi r}}$$
*Inside* ($r<R$): the enclosed current is the fraction of the area, $I_{enc} = I\dfrac{\pi r^2}{\pi R^2} = \dfrac{Ir^2}{R^2}$:
$$B(2\pi r) = \mu_0\frac{Ir^2}{R^2}\ \Rightarrow\ \boxed{B = \frac{\mu_0Ir}{2\pi R^2}}$$
$B$ is zero on the axis, rises linearly to $\dfrac{\mu_0I}{2\pi R}$ at the surface and then falls as $1/r$.

**OR: Hall effect.** When a conductor or semiconductor strip carrying a current $I$ is placed in a magnetic field $B$ perpendicular to the current, a transverse potential difference (the Hall voltage) appears across the sides, perpendicular to both $I$ and $B$.

```figure caption="Question 12 (OR): Hall effect in a strip of thickness t; the magnetic force pushes carriers to one side until the Hall field balances it."
fig,ax=plt.subplots(figsize=(4.6,2.4))
ax.fill([0,4,4,0],[0,0,1.2,1.2],color='#dbe8f6',ec='#14181f')
ax.annotate('',xy=(3.6,.6),xytext=(.4,.6),arrowprops=dict(arrowstyle='->',color='#1d6fb8',lw=1.6)); ax.text(1.8,.7,'$I$',color='#1d6fb8')
ax.text(1.0,-.4,r'$B$ out of page $\odot$',fontsize=8)
ax.annotate('',xy=(2.0,.1),xytext=(2.0,1.1),arrowprops=dict(arrowstyle='<->',color='#d9534f')); ax.text(2.1,.85,r'$E_H$',color='#d9534f',fontsize=9)
ax.text(.2,1.3,'$+$ $+$ $+$ $+$ $+$',fontsize=8); ax.text(.2,-.25,'$-$ $-$ $-$ $-$ $-$',fontsize=8)
ax.text(3.4,.2,'$V_H$',fontsize=9); ax.set_xlim(-.3,4.4); ax.set_ylim(-.7,1.6); ax.axis('off')
```

*Derivation.* Let the carriers (charge $q$, density $n$) drift with velocity $v_d$ in a strip of width $w$ (the Hall direction) and thickness $t$. The magnetic force $qv_dB$ pushes the carriers sideways, so charge piles up on one face, and a transverse **Hall field** $E_H$ builds up until the electric force balances the magnetic force:
$$qE_H = qv_dB\ \Rightarrow\ E_H = v_dB$$
Since $I = nqv_dA = nqv_d(wt)$, $v_d = \dfrac{I}{nqwt}$. The Hall voltage across the width $w$ is
$$V_H = E_Hw = v_dBw = \frac{IB}{nqt}$$
$$\boxed{V_H = \frac{IB}{nqt}}$$
The **Hall coefficient** is defined by $R_H = \dfrac{E_H}{JB}$ (with $J = I/wt$), which gives
$$\begin{gathered}\boxed{R_H = \frac{1}{nq}} \\ \text{so} \\ V_H = R_H\frac{IB}{t}\end{gathered}$$
$R_H$ is negative for electrons (n-type) and positive for holes (p-type), so its sign shows the type of carrier, and its magnitude gives the carrier density $n = 1/(|R_H|e)$.

@s 13
For a cyclotron the radius and frequency are $r = \dfrac{mv}{qB}$ and $f = \dfrac{qB}{2\pi m}$. Take $c = 3\times10^8$ m/s, so $v = \dfrac c{10} = 3\times10^7$ m/s (still non-relativistic, $\gamma = 1.005$), $m_p = 1.67\times10^{-27}$ kg, $q = 1.6\times10^{-19}$ C, $B = 1.4$ T.

**(i) Radius**
$$r = \frac{(1.67\times10^{-27})(3\times10^7)}{(1.6\times10^{-19})(1.4)} = \frac{5.01\times10^{-20}}{2.24\times10^{-19}}$$
$$\boxed{r\approx0.224\ \text{m}}$$
**(ii) Oscillator frequency**
$$f = \frac{qB}{2\pi m} = \frac{(1.6\times10^{-19})(1.4)}{2\pi(1.67\times10^{-27})}$$
$$\boxed{f\approx2.13\times10^{7}\ \text{Hz}\approx21.3\ \text{MHz}}$$

@s 14
For an $L$-$R$ circuit connected to a battery, the current grows as
$$\begin{gathered}i = I_0\left(1 - e^{-t/\tau}\right) \\ \tau = \frac LR,\quad I_0 = \frac{V}{R}\end{gathered}$$
$$\begin{gathered}\tau = \frac{6.3\times10^{-6}}{1.2\times10^3} = 5.25\times10^{-9}\ \text{s} \\ I_0 = \frac{14}{1200} = 11.67\ \text{mA}\end{gathered}$$
For $i = 0.9I_0$:
$$1 - e^{-t/\tau} = 0.9\ \Rightarrow\ e^{-t/\tau} = 0.1\ \Rightarrow\ t = \tau\ln10$$
$$t = (5.25\times10^{-9})(2.3026)$$
$$\boxed{t\approx1.21\times10^{-8}\ \text{s}\approx12.1\ \text{ns}}$$

@s 15
**Poynting vector.** The Poynting vector is the rate of energy flow per unit area carried by an electromagnetic field (power per unit area, in W/m²):
$$\boxed{\vec S = \vec E\times\vec H = \frac1{\mu_0}\vec E\times\vec B}$$
Its direction is the direction of propagation of the energy. (Poynting's theorem: $-\dfrac{\partial u}{\partial t} = \nabla\cdot\vec S + \vec J\cdot\vec E$, with $u = \tfrac12\varepsilon_0E^2 + \tfrac1{2\mu_0}B^2$.)

**Intensity of a plane wave in free space.** For a wave travelling along $+z$ with $\vec E = E_0\sin(kz - \omega t)\,\hat x$ and $\vec B = B_0\sin(kz - \omega t)\,\hat y$, $\vec E$ and $\vec B$ are perpendicular, in phase, and $E_0/B_0 = c = \dfrac{1}{\sqrt{\mu_0\varepsilon_0}}$. Then $\vec E\times\vec B$ points along $+z$, with magnitude
$$\begin{gathered}S = \frac{EB}{\mu_0} = \frac{E^2}{\mu_0c} = \varepsilon_0cE^2 \\ \left(\text{using }B = \frac Ec,\ \frac{1}{\mu_0c} = \varepsilon_0c\right)\end{gathered}$$
The instantaneous $S$ varies with $\sin^2$; the intensity is its time average, $\langle\sin^2\rangle = \tfrac12$:
$$\boxed{I = \langle S\rangle = \tfrac12\varepsilon_0cE_0^2 = \frac{E_0^2}{2\mu_0c}\ \propto\ E_0^2}$$
So the intensity is proportional to the square of the amplitude of the electric field. $\blacksquare$

*Consistency check.* The energy density is $u = \varepsilon_0E^2$ (the electric and magnetic parts are equal), and the energy flows at speed $c$, so $S = uc = \varepsilon_0cE^2$, the same result.

@s 16
**Particle in a one-dimensional infinite well.** The electron (mass $m$) moves freely in $0<x<L$ and the potential is infinite outside: $V = 0$ for $0<x<L$ and $V = \infty$ for $x\le0$, $x\ge L$. The wave function must vanish outside and, by continuity, at the walls: $\psi(0) = \psi(L) = 0$.

Inside the well, the time-independent Schrödinger equation is
$$\begin{gathered}-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} = E\psi\ \Rightarrow\ \frac{d^2\psi}{dx^2} + k^2\psi = 0 \\ k^2 = \frac{2mE}{\hbar^2}\end{gathered}$$
General solution: $\psi(x) = A\sin kx + B\cos kx$.

*Boundary conditions.* $\psi(0) = 0\Rightarrow B = 0$. $\psi(L) = 0\Rightarrow A\sin kL = 0$. $A\ne0$ (else $\psi\equiv0$), so
$$\begin{gathered}kL = n\pi,\quad n = 1, 2, 3, \dots \\ (n = 0\text{ gives }\psi\equiv0)\end{gathered}$$
So $k$ can take only the discrete values $k_n = \dfrac{n\pi}{L}$, and therefore
$$\boxed{E_n = \frac{\hbar^2k_n^2}{2m} = \frac{n^2\pi^2\hbar^2}{2mL^2} = \frac{n^2h^2}{8mL^2}}$$
**The energy is quantized:** only $E_1, 4E_1, 9E_1,\dots$ are allowed. The lowest level (zero-point energy) $E_1 = \dfrac{h^2}{8mL^2}\ne0$.

**Wave function.** $\psi_n = A\sin\dfrac{n\pi x}{L}$. Normalize with $\displaystyle\int_0^L|\psi_n|^2dx = 1$:
$$A^2\int_0^L\sin^2\frac{n\pi x}{L}\,dx = A^2\frac L2 = 1\ \Rightarrow\ A = \sqrt{\frac2L}$$
$$\boxed{\psi_n(x) = \sqrt{\frac2L}\,\sin\frac{n\pi x}{L},\qquad 0<x<L}$$
(and $\psi_n = 0$ elsewhere), with time dependence $\Psi_n(x,t) = \psi_n(x)\,e^{-iE_nt/\hbar}$.

```figure caption="Question 16: energy levels E_n = n^2 E_1 and the first three wave functions of the infinite well."
x=np.linspace(0,1,200)
fig,ax=plt.subplots(figsize=(4.6,3.0))
for n,c in ((1,'#1d6fb8'),(2,'#d9534f'),(3,'#2e8b57')):
    E=n*n
    ax.axhline(E,color=c,lw=.7,ls=':')
    ax.plot(x,E+0.9*np.sqrt(2)*np.sin(n*np.pi*x),color=c,lw=1.5)
    ax.text(1.03,E-.15,'$n=%d$, $E_%d=%dE_1$'%(n,n,E) if n==1 else '$n=%d$, $E_%d=%dE_1$'%(n,n,E),fontsize=7,color=c)
ax.plot([0,0],[0,10.5],color='#14181f',lw=2); ax.plot([1,1],[0,10.5],color='#14181f',lw=2)
ax.set_xlim(-.1,1.55); ax.set_ylim(0,10.5); ax.set_xlabel('$x/L$',fontsize=9); ax.set_ylabel('$E/E_1$',fontsize=9)
```

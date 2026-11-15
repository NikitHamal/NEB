---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-III-ENSH201-2082-Kartik.pdf
subject: Engineering Mathematics III
level: BE · Year II / Part I
code: ENSH 201
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: All programmes except B.Arch
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) Find half range sine series for the function $f(x) = \pi - x$ in $0<x<\pi$. [[2]]
(b) Find Fourier integral representation of $f(x) = e^{-|x|}$. [[2]]
(c) Determine Fourier cosine transform of $f(x) = \begin{cases}1 & ;0<x<a\\ 0 & ;\text{otherwise}\end{cases}$ [[2]]

@q 2
(a) Show that the function $u(x,y) = 2x + x^3 - 3xy^2$ is harmonic. [[2]]
(b) What will be the image of circle $|z - i| = 1$ under the mapping $w = f(z) = \dfrac1z$ in complex plane? [[2]]
(c) Expand $f(z) = e^{-z}$ in a Taylor's series about $z = 0$. [[2]]

@q 3
(a) Find the residue of $f(z) = \dfrac{3z-4}{(z-1)(z-2)}$ at each of its singularities. [[2]]
(b) Evaluate $\displaystyle\oint_C\frac{e^z}{(z-1)(z-2)}dz$ over the circle $C: |z| = 3$. [[2]]

@q 4
(a) Classify the PDE: $x^2\dfrac{\partial^2u}{\partial x^2} + 3\dfrac{\partial^2u}{\partial x\partial y} + x\dfrac{\partial^2u}{\partial y^2} + 17\dfrac{\partial u}{\partial t} = 100u$. [[2]]
(b) Solve the PDE: $y^2u_x - x^2u_y = 0$ by the method of separation of the variables. [[2]]

@q 5
(a) Find $x(\infty)$ using the final value theorem of $z$-transform when $x(t) = 1 - e^{-at}$. [[2]]
(b) Apply $Z$-transform to find the sum of infinite series: $\displaystyle\sum_{k=0}^\infty e^{ak}$ for $a>0$. [[2]]

@q 6
Find Fourier series representation of $f(x) = x - x^2$ for $-1\le x\le1$. [[4]]

@q 7
Obtain Fourier integral of the function $f(x) = \begin{cases}e^{-x}; & x>0\\ 0; & x<0\end{cases}$. Hence evaluate $\displaystyle\int_0^\infty\frac1{1+x^2}dx$. [[4]]

@q 8
Solve the integral equation $\displaystyle\int_0^\infty f(x)\sin\omega x\,dx = \begin{cases}1; & 0\le\omega<1\\ 2; & 1\le\omega<2\\ 0; & \omega\ge2\end{cases}$, using Fourier transform. [[4]]

@q 9
An electrostatic field in a plane is given by the potential function $\phi(x,y) = 3x^2y - y^3$. Find the corresponding stream function and complex potential $f(z)$. [[4]]
@or
Find bilinear transform that maps the points $1, i, -1$ in $z$-plane into the points $0, 1, \infty$ in $w$ plane. [[4]]

@q 10
Evaluate the real integral $\displaystyle\int_{-\infty}^\infty\frac{x^2}{(x^2+1)(x^2+4)}dx$ using Cauchy's residue theorem. [[4]]

@q 11
Apply Charpit's method to find complete integral of $2xz - px^2 - 2qxy + pq = 0$, where the symbols have their usual meanings. [[4]]
@or
Apply Lagrange's method to solve the PDE: $y^2p - xyq = x(z - 2y)$, where the symbols have their usual meanings. [[4]]

@q 12
Derive two dimensional heat equation for steady state heat flow. [[4]]
@or
Derive Navier-Stokes equation of fluid flow. [[4]]

@q 13
A tightly stretched string fixed at two ends $x = 0$ and $x = \pi$ is initially at rest in equilibrium position. If it is set in vibration by giving to each of its points a velocity $\dfrac{\partial u}{\partial t} = 0.03\sin x - 0.04\sin3x$, find the deflection $u(x,t)$ at any point of the string at any time. [[4]]

@q 14
Apply $Z$-transform to solve the difference equation $x(k+2) - x(k+1) - 2x(k) = 0$, given that $x(0) = 0$, $x(1) = 1$. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** Half-range sine series: $f(x) = \sum b_n\sin nx$, $b_n = \dfrac2\pi\displaystyle\int_0^\pi(\pi - x)\sin nx\,dx$. By parts,
$$\int_0^\pi(\pi - x)\sin nx\,dx = \left[-\frac{(\pi - x)\cos nx}n - \frac{\sin nx}{n^2}\right]_0^\pi = 0 - \left(-\frac\pi n\right) = \frac\pi n\ \Rightarrow\ b_n = \frac2n$$
$$\boxed{\pi - x = 2\sum_{n=1}^\infty\frac{\sin nx}n = 2\left(\sin x + \frac{\sin2x}2 + \frac{\sin3x}3 + \cdots\right),\quad 0<x<\pi}$$

**(b)** $f(x) = e^{-|x|}$ is even, so the Fourier integral is a cosine integral, $f(x) = \dfrac2\pi\displaystyle\int_0^\infty A(\omega)\cos\omega x\,d\omega$ with
$$A(\omega) = \int_0^\infty e^{-t}\cos\omega t\,dt = \frac1{1 + \omega^2}$$
$$\boxed{e^{-|x|} = \frac2\pi\int_0^\infty\frac{\cos\omega x}{1 + \omega^2}\,d\omega}$$

**(c)** $F_c(\omega) = \displaystyle\int_0^\infty f(x)\cos\omega x\,dx = \int_0^a\cos\omega x\,dx = \left[\frac{\sin\omega x}\omega\right]_0^a$
$$\boxed{F_c(\omega) = \frac{\sin a\omega}{\omega}}\qquad\left(\text{with the }\sqrt{2/\pi}\text{ convention: }\sqrt{\tfrac2\pi}\,\tfrac{\sin a\omega}\omega\right)$$

@s 2
**(a)** $u = 2x + x^3 - 3xy^2$: $u_x = 2 + 3x^2 - 3y^2$, $u_{xx} = 6x$; $u_y = -6xy$, $u_{yy} = -6x$. So $u_{xx} + u_{yy} = 6x - 6x = 0$: **$u$ is harmonic**. ∎

**(b)** $|z - i| = 1$ means $x^2 + y^2 = 2y$, a circle through the origin. For $w = 1/z = u + iv$: $u = \dfrac x{x^2 + y^2}$, $v = -\dfrac y{x^2 + y^2}$. On the circle $x^2 + y^2 = 2y$, so $v = -\dfrac y{2y} = -\dfrac12$.
$$\boxed{\text{The image is the straight line } v = -\tfrac12}$$
(A circle through the pole maps to a straight line.)

**(c)** $e^{w} = \sum\dfrac{w^n}{n!}$ with $w = -z$:
$$\boxed{e^{-z} = 1 - z + \frac{z^2}{2!} - \frac{z^3}{3!} + \frac{z^4}{4!} - \cdots = \sum_{n=0}^\infty\frac{(-1)^nz^n}{n!}}$$
valid for all $z$ (radius of convergence $\infty$).

@s 3
**(a)** Simple poles at $z = 1$ and $z = 2$:
$$\text{Res}_{z=1} = \frac{3(1) - 4}{1 - 2} = \boxed{1},\qquad\text{Res}_{z=2} = \frac{3(2) - 4}{2 - 1} = \boxed{2}$$

**(b)** Both poles $z = 1$ and $z = 2$ lie inside $|z| = 3$.
$$\text{Res}_{z=1} = \frac{e^1}{1 - 2} = -e,\qquad\text{Res}_{z=2} = \frac{e^2}{2 - 1} = e^2$$
$$\oint_C = 2\pi i\left(-e + e^2\right) = \boxed{2\pi i\,e(e - 1)}$$

@s 4
**(a)** Compare with $Au_{xx} + Bu_{xy} + Cu_{yy} + \cdots = 0$: $A = x^2$, $B = 3$, $C = x$. The discriminant is
$$B^2 - 4AC = 9 - 4x^2\cdot x = 9 - 4x^3$$
- **Hyperbolic** where $9 - 4x^3>0$, i.e. $x^3<\tfrac94$ ($x<1.31$);
- **Parabolic** on $x^3 = \tfrac94$;
- **Elliptic** where $x^3>\tfrac94$ ($x>1.31$).

So the type depends on the region. (The terms $17u_t$ and $100u$ are lower-order and do not affect the classification.)

**(b)** Let $u = X(x)Y(y)$: $y^2X'Y = x^2XY'$, so $\dfrac{X'}{x^2X} = \dfrac{Y'}{y^2Y} = k$. Then $X' = kx^2X\Rightarrow X = Ae^{kx^3/3}$ and $Y' = ky^2Y\Rightarrow Y = Be^{ky^3/3}$.
$$\boxed{u(x,y) = C\exp\left[\frac k3\left(x^3 + y^3\right)\right]}$$

@s 5
**(a)** For the sampled signal $x(k) = 1 - e^{-ak}$, $X(z) = \dfrac z{z-1} - \dfrac z{z - e^{-a}}$. The final value theorem: $x(\infty) = \displaystyle\lim_{z\to1}(z-1)X(z)$ (valid since the poles of $(z-1)X(z)$ lie inside the unit circle for $a>0$).
$$(z-1)X(z) = z - \frac{(z-1)z}{z - e^{-a}}\ \to\ 1 - 0 = 1$$
$$\boxed{x(\infty) = 1}$$
This agrees with $\lim_{t\to\infty}(1 - e^{-at}) = 1$.

**(b)** The Z-transform of $x(k) = 1$ ($k\ge0$) is $X(z) = \displaystyle\sum_{k=0}^\infty z^{-k} = \frac z{z-1}$ for $|z|>1$. The series $\sum e^{ak}$ is obtained by putting $z^{-1} = e^{a}$, i.e. $z = e^{-a}$, giving $\dfrac{z}{z-1}\Big|_{z = e^{-a}} = \dfrac{1}{1 - e^{a}}$. But this is a geometric series with ratio $e^a$, which converges only if $e^a<1$ (that is $a<0$), because the transform requires $|z| = e^{-a}>1$.
- For $a>0$, as printed, the ratio is $e^a>1$ and the series **diverges** to $+\infty$.
- For the convergent version $\displaystyle\sum_{k=0}^\infty e^{-ak}$ (i.e. $z = e^{a}>1$): $\displaystyle\sum_{k=0}^\infty e^{-ak} = \frac{z}{z-1}\Big|_{z=e^a} = \boxed{\frac{1}{1 - e^{-a}}}$ for $a>0$.

@s 6
$f(x) = x - x^2$ on $[-1, 1]$ (period $2L = 2$, $L = 1$): $f(x) = \dfrac{a_0}2 + \sum\left(a_n\cos n\pi x + b_n\sin n\pi x\right)$.
$$a_0 = \int_{-1}^1(x - x^2)dx = -2\int_0^1x^2dx = -\frac23$$
$$a_n = \int_{-1}^1(x - x^2)\cos n\pi x\,dx = -2\int_0^1x^2\cos n\pi x\,dx = -2\left[\frac{x^2\sin n\pi x}{n\pi} + \frac{2x\cos n\pi x}{n^2\pi^2} - \frac{2\sin n\pi x}{n^3\pi^3}\right]_0^1 = -\frac{4(-1)^n}{n^2\pi^2}$$
(the odd part $x\cos n\pi x$ integrates to zero.)
$$b_n = \int_{-1}^1(x - x^2)\sin n\pi x\,dx = 2\int_0^1x\sin n\pi x\,dx = 2\left[-\frac{x\cos n\pi x}{n\pi} + \frac{\sin n\pi x}{n^2\pi^2}\right]_0^1 = \frac{2(-1)^{n+1}}{n\pi}$$
$$\boxed{x - x^2 = -\frac13 + \frac4{\pi^2}\sum_{n=1}^\infty\frac{(-1)^{n+1}}{n^2}\cos n\pi x + \frac2\pi\sum_{n=1}^\infty\frac{(-1)^{n+1}}n\sin n\pi x}$$

@s 7
For $f(x) = e^{-x}$ ($x>0$), $0$ ($x<0$): $A(\omega) = \dfrac1\pi\displaystyle\int_0^\infty e^{-t}\cos\omega t\,dt = \dfrac1{\pi(1 + \omega^2)}$ and $B(\omega) = \dfrac1\pi\displaystyle\int_0^\infty e^{-t}\sin\omega t\,dt = \dfrac{\omega}{\pi(1 + \omega^2)}$.
$$\boxed{f(x) = \frac1\pi\int_0^\infty\frac{\cos\omega x + \omega\sin\omega x}{1 + \omega^2}\,d\omega}$$
**Evaluation.** At the point of discontinuity $x = 0$ the integral converges to $\dfrac{f(0^+) + f(0^-)}2 = \dfrac12$. Putting $x = 0$:
$$\frac1\pi\int_0^\infty\frac{1}{1 + \omega^2}d\omega = \frac12\ \Rightarrow\ \boxed{\int_0^\infty\frac{dx}{1 + x^2} = \frac\pi2}$$
(Check: $[\tan^{-1}x]_0^\infty = \pi/2$ ✓.)

@s 8
Let $F_s(\omega) = \displaystyle\int_0^\infty f(x)\sin\omega x\,dx$ be the given Fourier sine transform. The inverse is
$$f(x) = \frac2\pi\int_0^\infty F_s(\omega)\sin\omega x\,d\omega = \frac2\pi\left[\int_0^1\sin\omega x\,d\omega + 2\int_1^2\sin\omega x\,d\omega\right]$$
$$\begin{gathered}\int_0^1\sin\omega x\,d\omega = \frac{1 - \cos x}x \\ \int_1^2\sin\omega x\,d\omega = \frac{\cos x - \cos2x}x\end{gathered}$$
$$f(x) = \frac{2}{\pi x}\left[1 - \cos x + 2\cos x - 2\cos2x\right]$$
$$\boxed{f(x) = \frac{2\left(1 + \cos x - 2\cos2x\right)}{\pi x},\qquad x>0}$$

@s 9
$\phi = 3x^2y - y^3$ is harmonic ($\phi_{xx} = 6y$, $\phi_{yy} = -6y$). Let the complex potential be $f(z) = \phi + i\psi$, where $\psi$ is the stream function. Cauchy–Riemann: $\psi_y = \phi_x = 6xy$ and $\psi_x = -\phi_y = -3x^2 + 3y^2$.
$$\psi = 3xy^2 + h(x)\ \Rightarrow\ \psi_x = 3y^2 + h'(x) = -3x^2 + 3y^2\ \Rightarrow\ h' = -3x^2,\ h = -x^3$$
$$\boxed{\psi = 3xy^2 - x^3}$$
$$f(z) = (3x^2y - y^3) + i(3xy^2 - x^3)$$
Since $z^3 = (x^3 - 3xy^2) + i(3x^2y - y^3)$ and $-iz^3 = (3x^2y - y^3) - i(x^3 - 3xy^2)$,
$$\boxed{f(z) = -iz^3 + c}$$

**Or.** A bilinear transformation $w = \dfrac{az + b}{cz + d}$. Since $z = 1\to w = 0$, the numerator contains $(z - 1)$, and since $z = -1\to w = \infty$ the denominator contains $(z + 1)$: $w = k\dfrac{z - 1}{z + 1}$. Condition $z = i\to w = 1$:
$$k\frac{i - 1}{i + 1} = k\frac{(i-1)(1 - i)}{(1+i)(1-i)} = k\frac{2i}2 = ik = 1\ \Rightarrow\ k = \frac1i = -i$$
$$\boxed{w = -i\,\frac{z - 1}{z + 1} = \frac{i(1 - z)}{1 + z}}$$
Check: $z = 1\to0$, $z = -1\to\infty$, $z = i\to\dfrac{i(1 - i)}{1 + i} = i\cdot\dfrac{(1-i)^2}{2} = i\cdot(-i) = 1$ ✓.

@s 10
Let $f(z) = \dfrac{z^2}{(z^2 + 1)(z^2 + 4)}$. Take the closed contour made of the real axis from $-R$ to $R$ and the upper semicircle $\Gamma_R$. On $\Gamma_R$, $|f|\sim R^{-2}$, so $\int_{\Gamma_R}\to0$ as $R\to\infty$. The poles in the upper half-plane are $z = i$ and $z = 2i$ (simple).
$$\text{Res}_{z=i} = \frac{z^2}{(z + i)(z^2 + 4)}\Big|_{z=i} = \frac{-1}{(2i)(3)} = -\frac1{6i},\qquad\text{Res}_{z=2i} = \frac{z^2}{(z^2 + 1)(z + 2i)}\Big|_{z=2i} = \frac{-4}{(-3)(4i)} = \frac1{3i}$$
$$\int_{-\infty}^\infty\frac{x^2\,dx}{(x^2+1)(x^2+4)} = 2\pi i\left(-\frac1{6i} + \frac1{3i}\right) = 2\pi i\cdot\frac{1}{6i} = \boxed{\frac\pi3}$$
(Check by partial fractions: $\dfrac{x^2}{(x^2+1)(x^2+4)} = \dfrac{-1/3}{x^2+1} + \dfrac{4/3}{x^2+4}$, giving $-\dfrac\pi3 + \dfrac43\cdot\dfrac\pi2 = \dfrac\pi3$ ✓.)

@s 11
Let $F = 2xz - px^2 - 2qxy + pq = 0$. Then $F_x = 2z - 2px - 2qy$, $F_y = -2qx$, $F_z = 2x$, $F_p = q - x^2$, $F_q = p - 2xy$. Charpit's equations:
$$\frac{dp}{F_x + pF_z} = \frac{dq}{F_y + qF_z} = \frac{dz}{-pF_p - qF_q} = \frac{dx}{-F_p} = \frac{dy}{-F_q}$$
Here $F_y + qF_z = -2qx + 2qx = 0$, so $dq = 0$ and $q = a$ (constant). Substituting in $F = 0$:
$$2xz - px^2 - 2axy + pa = 0\ \Rightarrow\ p(a - x^2) = 2x(ay - z)\ \Rightarrow\ p = \frac{2x(ay - z)}{a - x^2}$$
Now $dz = p\,dx + q\,dy = \dfrac{2x(ay - z)}{a - x^2}dx + a\,dy$. Let $t = z - ay$, so $dt = dz - a\,dy = -\dfrac{2x\,t}{a - x^2}dx$:
$$\frac{dt}t = -\frac{2x\,dx}{a - x^2} = d\left[\ln(a - x^2)\right]\ \Rightarrow\ t = b(a - x^2)$$
$$\boxed{z = ay + b(a - x^2)}$$
which is the complete integral ($a$, $b$ arbitrary constants). Check: $p = -2bx$, $q = a$: $2xz - px^2 - 2qxy + pq = 2x(ay + ab - bx^2) + 2bx^3 - 2axy - 2abx = 0$ ✓.

**Or (Lagrange).** Auxiliary equations: $\dfrac{dx}{y^2} = \dfrac{dy}{-xy} = \dfrac{dz}{x(z - 2y)}$.
*First integral:* from the first two, $-x\,dx = y\,dy$, so $x^2 + y^2 = c_1$.
*Second integral:* from the last two, $\dfrac{dy}{-y} = \dfrac{dz}{z - 2y}\Rightarrow(z - 2y)\,dy + y\,dz = 0\Rightarrow z\,dy + y\,dz - 2y\,dy = 0\Rightarrow d(yz - y^2) = 0$, so $yz - y^2 = c_2$.
$$\boxed{\phi\left(x^2 + y^2,\ yz - y^2\right) = 0}$$
for an arbitrary function $\phi$, i.e. $y(z - y) = f(x^2 + y^2)$.

@s 12
**Derivation of the two-dimensional steady-state heat equation.** Consider a thin rectangular plate element $dx\,dy$ of thickness $t$, with conductivity $k$, insulated on its faces, so that heat flows only in the $x$–$y$ plane. By Fourier's law the heat flux in the $x$ direction is $q_x = -k\dfrac{\partial u}{\partial x}$ and in the $y$ direction $q_y = -k\dfrac{\partial u}{\partial y}$, where $u(x,y,t)$ is the temperature.
- Heat entering across the face at $x$: $q_x\,t\,dy$; leaving across $x + dx$: $\left(q_x + \dfrac{\partial q_x}{\partial x}dx\right)t\,dy$.
- Heat entering across the face at $y$: $q_y\,t\,dx$; leaving across $y + dy$: $\left(q_y + \dfrac{\partial q_y}{\partial y}dy\right)t\,dx$.

The net gain of heat per unit time is $-\left(\dfrac{\partial q_x}{\partial x} + \dfrac{\partial q_y}{\partial y}\right)t\,dx\,dy = k\left(\dfrac{\partial^2u}{\partial x^2} + \dfrac{\partial^2u}{\partial y^2}\right)t\,dx\,dy$. It equals the rate of storage $\rho s\,t\,dx\,dy\,\dfrac{\partial u}{\partial t}$ ($\rho$ = density, $s$ = specific heat), so
$$\begin{gathered}\frac{\partial u}{\partial t} = c^2\left(\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial y^2}\right) \\ c^2 = \frac{k}{\rho s}\end{gathered}$$
In the **steady state** the temperature does not change with time, $\partial u/\partial t = 0$, so
$$\boxed{\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial y^2} = 0}\quad\text{(Laplace's equation, } \nabla^2u = 0\text{)}$$

**Or.**
**Derivation of the Navier–Stokes equation.** Take a small fixed fluid element $dx\,dy\,dz$ of a fluid of density $\rho$ and velocity $\vec V = (u, v, w)$. Newton's second law for the element gives $\rho\dfrac{D\vec V}{Dt}\,dx\,dy\,dz = $ (body force) + (surface forces).
- *Acceleration* (material derivative): $\dfrac{D\vec V}{Dt} = \dfrac{\partial\vec V}{\partial t} + (\vec V\cdot\nabla)\vec V$.
- *Body force* (gravity): $\rho\vec g\,dx\,dy\,dz$.
- *Surface forces* come from the stress tensor $\sigma_{ij} = -p\,\delta_{ij} + \tau_{ij}$. The net force on the element in the $x$-direction is $\left(\dfrac{\partial\sigma_{xx}}{\partial x} + \dfrac{\partial\sigma_{yx}}{\partial y} + \dfrac{\partial\sigma_{zx}}{\partial z}\right)dx\,dy\,dz$.

For a Newtonian fluid, viscous stress is proportional to the rate of strain: $\tau_{ij} = \mu\left(\dfrac{\partial V_i}{\partial x_j} + \dfrac{\partial V_j}{\partial x_i}\right) + \lambda\,\delta_{ij}\,\nabla\cdot\vec V$. For an incompressible fluid (continuity: $\nabla\cdot\vec V = 0$) with constant viscosity $\mu$, the viscous force reduces to $\mu\nabla^2\vec V$. The $x$-component of the momentum equation is
$$\rho\left(\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} + w\frac{\partial u}{\partial z}\right) = -\frac{\partial p}{\partial x} + \mu\left(\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial y^2} + \frac{\partial^2u}{\partial z^2}\right) + \rho g_x$$
and similarly for $y$ and $z$. In vector form, the **Navier–Stokes equation** is
$$\begin{gathered}\boxed{\rho\left[\frac{\partial\vec V}{\partial t} + (\vec V\cdot\nabla)\vec V\right] = -\nabla p + \mu\nabla^2\vec V + \rho\vec g} \\ \nabla\cdot\vec V = 0\end{gathered}$$
The terms are: inertia (local and convective), pressure gradient, viscous diffusion, and body force.

@s 13
The string obeys $u_{tt} = c^2u_{xx}$ with $u(0,t) = u(\pi,t) = 0$, initial displacement $u(x,0) = 0$ and initial velocity $u_t(x,0) = 0.03\sin x - 0.04\sin3x$. Separating variables, the solutions that vanish at both ends are
$$u(x,t) = \sum_{n=1}^\infty\left(B_n\cos nct + C_n\sin nct\right)\sin nx$$
- $u(x,0) = 0\Rightarrow\sum B_n\sin nx = 0\Rightarrow B_n = 0$.
- $u_t(x,0) = \sum nc\,C_n\sin nx = 0.03\sin x - 0.04\sin3x$. Comparing coefficients: $cC_1 = 0.03$, $3cC_3 = -0.04$, all others zero. So $C_1 = \dfrac{0.03}c$ and $C_3 = -\dfrac{0.04}{3c}$.

$$\boxed{u(x,t) = \frac{0.03}c\sin x\sin ct - \frac{0.04}{3c}\sin3x\sin3ct}$$
where $c$ is the wave speed $\sqrt{T/\rho}$.

@s 14
Taking the Z-transform with $x(0) = 0$, $x(1) = 1$:
$$(z^2X - z) - zX - 2X = 0\ \Rightarrow\ (z^2 - z - 2)X = z\ \Rightarrow\ X(z) = \frac{z}{(z - 2)(z + 1)}$$
$$X(z) = \frac13\left(\frac z{z-2} - \frac z{z+1}\right)\ \Rightarrow\ \boxed{x(k) = \frac{2^k - (-1)^k}3}$$
Check: $x(0) = 0$, $x(1) = 1$, $x(2) = 1 = x(1) + 2x(0)$ ✓, $x(3) = 3 = x(2) + 2x(1)$ ✓.

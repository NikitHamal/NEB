---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-III-ENSH201-2082-Chaitra.pdf
subject: Engineering Mathematics III
level: BE · Year II / Part I
code: ENSH 201
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: All programmes except B.Arch
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) In the series $f(x) = \dfrac{a_0}2 + \sum_{n=1}^\infty(a_n\cos nx + b_n\sin nx)$, find the coefficient $b_n$ for the function $f(x) = e^{-x}$ where $x\in(0, 2\pi)$. [[2]]
(b) Find the Fourier integral representation of $f(x) = \begin{cases}1 & \text{for } |x|<1\\ 0 & \text{for } |x|>1\end{cases}$ [[2]]
(c) Solve the integral equation $\displaystyle\int_0^\infty f(x)\cos\alpha x\,dx = e^{-\alpha}$, $\alpha>0$. [[2]]

@q 2
(a) Define harmonic function. Show that the function $u(x,y) = e^x\cos y$ is harmonic. [[2]]
(b) Find the bilinear transformation which maps the points $z = 0, -1, i$ into $w = i, 0, \infty$. [[2]]
(c) Evaluate $\displaystyle\int_C\frac{5z-2}{z-1}dz$, $C$ being the circle $|z| = 2$. [[2]]

@q 3
(a) Find the residue of $f(z) = \dfrac{2z+1}{(z-3)(z+5)}$ at each of the singularities. [[2]]
(b) Find the Taylor series expansion of $f(z) = \dfrac1{z-3}$ centered at the point $z = 4i$. [[2]]

@q 4
(a) Solve the partial differential equation $\dfrac{\partial^2z}{\partial x\partial y} = \sin x\sin y$ given that $\dfrac{\partial z}{\partial y} = -2\sin y$ when $x = 0$; $z = 0$ when $y = \dfrac\pi2$. [[2]]
(b) Write down the classification rules for general second order partial differential equation and hence use it to classify the equation $u_{xx} + x^2u_{yy} = 0$. [[2]]

@q 5
(a) Find $x(0)$ and $x(1)$ of Z-transform of $x(t) = 1 - e^{-t}$. [[2]]
(b) Find inverse z-transform of $\dfrac{z}{(z-1)(z-2)}$. [[2]]

@q 6
If $f(x) = x + x^2$ for $-\pi\le x\le\pi$, then find the Fourier series of $f(x)$. [[4]]

@q 7
Find Fourier cosine integral of $f(x) = e^{-kx}$, $k>0$, $x>0$ and use it to evaluate $\displaystyle\int_0^\infty\frac{\cos\omega x}{k^2 + \omega^2}d\omega$. [[4]]

@q 8
Find Fourier sine transform of $f(x) = e^{-x}$ and hence use the result in Parseval's identity to show $\displaystyle\int_0^\infty\frac{x^2\,dx}{(x^2+1)^2} = \frac\pi4$. [[4]]

@q 9
Express the function $\dfrac1{z^2 - 3z + 2}$ in Laurent series form in the region $1<|z|<2$. [[4]]

@q 10
Evaluate $\displaystyle\int_0^{2\pi}\frac{\cos2\theta}{5 + 4\sin\theta}d\theta$ using method of contour integration in the complex plane. [[4]]

@q 11
Apply Charpit's method to solve the PDE: $2zx - px^2 - 2qxy + pq = 0$, where the symbols have their usual meanings. [[4]]
@or
Solve the PDE: $z(p - q) = z^2 + (x + y)^2$, using Lagrange's method where $p = \dfrac{\partial z}{\partial x}$ and $q = \dfrac{\partial z}{\partial y}$. [[4]]

@q 12
Using Z-transform technique, solve the difference equation $x(k+2) - 4x(k+1) + 4x(k) = 0$ under $x(0) = 0$, $x(1) = 1$. [[4]]

@q 13
Solve one dimensional heat equation $\dfrac{\partial u}{\partial t} = c^2\dfrac{\partial^2u}{\partial x^2}$ completely. [[4]]
@or
Solve the wave equation $u_{tt} = c^2u_{xx}$ under boundary conditions $u(0,t) = 0$, $u(\pi,t) = 0$ and initial conditions $\dfrac{\partial u}{\partial t} = 0$ at $t = 0$ and $u(x,0) = x$ for $0<x<\pi$. [[4]]

@q 14
Derive Navier-Stoke's equation of motion for fluid flow. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** For $f(x) = e^{-x}$ on $(0, 2\pi)$ (period $2\pi$), $b_n = \dfrac1\pi\displaystyle\int_0^{2\pi}e^{-x}\sin nx\,dx$. Using $\displaystyle\int e^{-x}\sin nx\,dx = -\frac{e^{-x}(\sin nx + n\cos nx)}{1 + n^2}$:
$$b_n = \frac1\pi\left[-\frac{e^{-x}(\sin nx + n\cos nx)}{1 + n^2}\right]_0^{2\pi} = \frac1\pi\cdot\frac{n\left(1 - e^{-2\pi}\right)}{1 + n^2}$$
$$\boxed{b_n = \frac{n\left(1 - e^{-2\pi}\right)}{\pi(1 + n^2)}}$$
(Similarly $a_n = \dfrac{1 - e^{-2\pi}}{\pi(1 + n^2)}$.)

**(b)** $f$ is even, so $f(x) = \dfrac2\pi\displaystyle\int_0^\infty A(\omega)\cos\omega x\,d\omega$ with $A(\omega) = \displaystyle\int_0^1\cos\omega t\,dt = \dfrac{\sin\omega}\omega$.
$$\boxed{f(x) = \frac2\pi\int_0^\infty\frac{\sin\omega\cos\omega x}{\omega}\,d\omega = \begin{cases}1, & |x|<1\\ \tfrac12, & |x| = 1\\ 0, & |x|>1\end{cases}}$$

**(c)** The left side is the Fourier cosine transform $F_c(\alpha) = e^{-\alpha}$. By the inversion formula,
$$f(x) = \frac2\pi\int_0^\infty F_c(\alpha)\cos\alpha x\,d\alpha = \frac2\pi\int_0^\infty e^{-\alpha}\cos\alpha x\,d\alpha = \frac2\pi\cdot\frac1{1 + x^2}$$
$$\boxed{f(x) = \frac{2}{\pi(1 + x^2)}}$$

@s 2
**(a)** A real function $u(x,y)$ with continuous second partial derivatives is **harmonic** if it satisfies Laplace's equation $\nabla^2u = u_{xx} + u_{yy} = 0$.
For $u = e^x\cos y$: $u_x = e^x\cos y$, $u_{xx} = e^x\cos y$, $u_y = -e^x\sin y$, $u_{yy} = -e^x\cos y$. So $u_{xx} + u_{yy} = 0$ ✓, and $u$ is harmonic. ∎ (It is the real part of $e^z$.)

**(b)** $z = -1\to w = 0$ gives a factor $(z + 1)$ in the numerator, and $z = i\to w = \infty$ gives $(z - i)$ in the denominator: $w = k\dfrac{z + 1}{z - i}$. With $z = 0\to w = i$:
$$i = k\cdot\frac{1}{-i} = ik\ \Rightarrow\ k = 1$$
$$\boxed{w = \frac{z + 1}{z - i}}$$

**(c)** $\dfrac{5z - 2}{z - 1} = 5 + \dfrac3{z - 1}$, with a simple pole at $z = 1$ (inside $|z| = 2$), residue $3$.
$$\int_C\frac{5z-2}{z-1}dz = 2\pi i\cdot3 = \boxed{6\pi i}$$

@s 3
**(a)** Simple poles at $z = 3$ and $z = -5$.
$$\text{Res}_{z=3} = \frac{2(3) + 1}{3 + 5} = \boxed{\frac78},\qquad\text{Res}_{z=-5} = \frac{2(-5) + 1}{-5 - 3} = \boxed{\frac98}$$

**(b)** Write $z - 3 = (z - 4i) + (4i - 3)$:
$$\frac1{z-3} = \frac1{(4i - 3)}\cdot\frac1{1 + \dfrac{z - 4i}{4i - 3}} = \sum_{n=0}^\infty\frac{(-1)^n(z - 4i)^n}{(4i - 3)^{n+1}}$$
$$\boxed{\frac1{z-3} = \frac1{4i-3} - \frac{z - 4i}{(4i-3)^2} + \frac{(z-4i)^2}{(4i-3)^3} - \cdots}$$
valid for $|z - 4i|<|4i - 3| = 5$ (the distance to the singularity $z = 3$).

@s 4
**(a)** $\dfrac{\partial^2z}{\partial x\partial y} = \sin x\sin y$. Integrate with respect to $x$: $\dfrac{\partial z}{\partial y} = -\cos x\sin y + f(y)$. At $x = 0$: $-\sin y + f(y) = -2\sin y\Rightarrow f(y) = -\sin y$. So $\dfrac{\partial z}{\partial y} = -(1 + \cos x)\sin y$. Integrate with respect to $y$: $z = (1 + \cos x)\cos y + g(x)$. At $y = \dfrac\pi2$: $z = 0 + g(x) = 0\Rightarrow g = 0$.
$$\boxed{z = (1 + \cos x)\cos y}$$

**(b)** **Classification rules.** For $Au_{xx} + Bu_{xy} + Cu_{yy} + Du_x + Eu_y + Fu = G$ the discriminant $B^2 - 4AC$ decides:
- $B^2 - 4AC>0$: **hyperbolic** (e.g. wave equation);
- $B^2 - 4AC = 0$: **parabolic** (e.g. heat equation);
- $B^2 - 4AC<0$: **elliptic** (e.g. Laplace equation).

For $u_{xx} + x^2u_{yy} = 0$: $A = 1$, $B = 0$, $C = x^2$, so $B^2 - 4AC = -4x^2$.
$$\boxed{\text{elliptic for } x\ne0\ (-4x^2<0);\ \text{parabolic on the line } x = 0}$$

@s 5
**(a)** Sampling with $T = 1$: $x(k) = 1 - e^{-k}$, so $X(z) = \dfrac z{z-1} - \dfrac z{z - e^{-1}}$.
$$x(0) = \lim_{z\to\infty}X(z) = 1 - 1 = \boxed{0}$$
$$x(1) = \lim_{z\to\infty}z\left[X(z) - x(0)\right] = \lim_{z\to\infty}z^2\left[\frac{1}{z-1} - \frac{1}{z - e^{-1}}\right] = \lim_{z\to\infty}\frac{z^2\left(1 - e^{-1}\right)}{(z-1)(z - e^{-1})} = \boxed{1 - e^{-1}\approx0.632}$$
These agree with $x(k) = 1 - e^{-k}$ at $k = 0, 1$.

**(b)** $\dfrac{X(z)}z = \dfrac1{(z-1)(z-2)} = \dfrac1{z-2} - \dfrac1{z-1}$, so $X(z) = \dfrac z{z-2} - \dfrac z{z-1}$. For the causal sequence ($|z|>2$):
$$\boxed{x(k) = 2^k - 1,\qquad k = 0, 1, 2,\ldots}$$

@s 6
$f(x) = x + x^2$ on $[-\pi, \pi]$. The part $x$ is odd and $x^2$ is even.
$$\begin{gathered}a_0 = \frac2\pi\int_0^\pi x^2dx = \frac{2\pi^2}3 \\ a_n = \frac2\pi\int_0^\pi x^2\cos nx\,dx = \frac{4(-1)^n}{n^2}\end{gathered}$$
$$b_n = \frac2\pi\int_0^\pi x\sin nx\,dx = \frac2\pi\left[-\frac{x\cos nx}n + \frac{\sin nx}{n^2}\right]_0^\pi = \frac{2(-1)^{n+1}}n$$
$$\boxed{x + x^2 = \frac{\pi^2}3 + 4\sum_{n=1}^\infty\frac{(-1)^n}{n^2}\cos nx + 2\sum_{n=1}^\infty\frac{(-1)^{n+1}}n\sin nx}$$
(Writing out: $\dfrac{\pi^2}3 - 4\cos x + \cos2x - \cdots + 2\sin x - \sin2x + \tfrac23\sin3x - \cdots$.)

@s 7
For $f(x) = e^{-kx}$, $x>0$, the Fourier cosine integral is $f(x) = \dfrac2\pi\displaystyle\int_0^\infty A(\omega)\cos\omega x\,d\omega$ with
$$A(\omega) = \int_0^\infty e^{-kt}\cos\omega t\,dt = \frac{k}{k^2 + \omega^2}$$
$$\boxed{e^{-kx} = \frac2\pi\int_0^\infty\frac{k\cos\omega x}{k^2 + \omega^2}\,d\omega}$$
**Evaluation.** Rearranging,
$$\boxed{\int_0^\infty\frac{\cos\omega x}{k^2 + \omega^2}\,d\omega = \frac{\pi}{2k}e^{-kx}}\qquad(x>0,\ k>0)$$
For $x = 0$ this reduces to $\displaystyle\int_0^\infty\frac{d\omega}{k^2 + \omega^2} = \frac\pi{2k}$ ✓.

@s 8
**Fourier sine transform:** $F_s(\omega) = \displaystyle\int_0^\infty e^{-x}\sin\omega x\,dx = \frac{\omega}{1 + \omega^2}$.
**Parseval's identity** for the sine transform: $\displaystyle\int_0^\infty\left[F_s(\omega)\right]^2d\omega = \frac\pi2\int_0^\infty\left[f(x)\right]^2dx$.
$$\int_0^\infty\frac{\omega^2}{(1 + \omega^2)^2}d\omega = \frac\pi2\int_0^\infty e^{-2x}dx = \frac\pi2\cdot\frac12 = \frac\pi4$$
Renaming the dummy variable $\omega\to x$:
$$\boxed{\int_0^\infty\frac{x^2\,dx}{(x^2 + 1)^2} = \frac\pi4}\ ∎$$

@s 9
Partial fractions: $\dfrac1{z^2 - 3z + 2} = \dfrac1{(z-1)(z-2)} = \dfrac1{z-2} - \dfrac1{z-1}$. In the annulus $1<|z|<2$:
- $|z|<2$: $\dfrac1{z-2} = -\dfrac12\cdot\dfrac1{1 - z/2} = -\displaystyle\sum_{n=0}^\infty\frac{z^n}{2^{n+1}}$;
- $|z|>1$: $-\dfrac1{z-1} = -\dfrac1z\cdot\dfrac1{1 - 1/z} = -\displaystyle\sum_{n=0}^\infty z^{-(n+1)}$.

$$\boxed{\frac1{z^2 - 3z + 2} = -\sum_{n=0}^\infty\frac{z^n}{2^{n+1}} - \sum_{n=1}^\infty\frac1{z^n} = \cdots - \frac1{z^2} - \frac1z - \frac12 - \frac z4 - \frac{z^2}8 - \cdots}$$

@s 10
Put $z = e^{i\theta}$: $\cos2\theta = \dfrac{z^2 + z^{-2}}2$, $\sin\theta = \dfrac{z - z^{-1}}{2i}$, $d\theta = \dfrac{dz}{iz}$. Then $iz(5 + 4\sin\theta) = 5iz + 2z^2 - 2 = 2(z + \tfrac i2)(z + 2i)$.
$$I = \oint_{|z|=1}\frac{(z^4 + 1)}{2z^2}\cdot\frac{dz}{2(z + \tfrac i2)(z + 2i)} = \oint\frac{z^4 + 1}{4z^2(z + \tfrac i2)(z + 2i)}dz$$
Poles inside $|z| = 1$: $z = 0$ (double) and $z = -\tfrac i2$ ($z = -2i$ is outside).
*Residue at $z = -\tfrac i2$:* $z^4 = \tfrac1{16}$, $z^2 = -\tfrac14$, $z + 2i = \tfrac{3i}2$:
$$\text{Res} = \frac{17/16}{4\left(-\tfrac14\right)\left(\tfrac{3i}2\right)} = \frac{17/16}{-3i/2} = \frac{17i}{24}$$
*Residue at $z = 0$ (double pole):* with $h(z) = (z + \tfrac i2)(z + 2i) = z^2 + \tfrac{5i}2z - 1$,
$$\text{Res}_0 = \frac{d}{dz}\left[\frac{z^4 + 1}{4h(z)}\right]_{z=0} = \frac{-h'(0)}{4h(0)^2} = -\frac{5i/2}{4} = -\frac{5i}8 = -\frac{15i}{24}$$
$$I = 2\pi i\left(\frac{17i}{24} - \frac{15i}{24}\right) = 2\pi i\cdot\frac{2i}{24} = \boxed{-\frac\pi6}$$
(Check: the same integral with $\cos\theta$ in place of $\sin\theta$ is $+\pi/6$; the shift $\theta\to\theta - \pi/2$ changes $\cos2\theta$ to $-\cos2\theta$ ✓.)

@s 11
*Note:* the printed equation reads $2zx - px^2 - 2xy + pq = 0$ with the $q$ lost in the scan; it is read as $2zx - px^2 - 2qxy + pq = 0$, the form that appears in the 2082 Kartik paper.

Let $F = 2xz - px^2 - 2qxy + pq$. $F_x = 2z - 2px - 2qy$, $F_y = -2qx$, $F_z = 2x$, $F_p = q - x^2$, $F_q = p - 2xy$. Charpit's equations: $\dfrac{dp}{F_x + pF_z} = \dfrac{dq}{F_y + qF_z} = \cdots$. Since $F_y + qF_z = -2qx + 2qx = 0$, $dq = 0$, so $q = a$. Substituting in $F = 0$:
$$p(a - x^2) = 2x(ay - z)\ \Rightarrow\ p = \frac{2x(ay - z)}{a - x^2}$$
With $t = z - ay$: $dt = p\,dx + q\,dy - a\,dy = -\dfrac{2xt}{a - x^2}dx$, so $\dfrac{dt}t = d\ln(a - x^2)$ and $t = b(a - x^2)$:
$$\boxed{z = ay + b(a - x^2)}\quad(\text{complete integral})$$
Check: $p = -2bx$, $q = a$ gives $2x(ay + ab - bx^2) + 2bx^3 - 2axy - 2abx = 0$ ✓.

**Or (Lagrange).** $zp - zq = z^2 + (x + y)^2$. Auxiliary equations:
$$\frac{dx}z = \frac{dy}{-z} = \frac{dz}{z^2 + (x + y)^2}$$
*First integral:* $dx = -dy\Rightarrow x + y = c_1$.
*Second integral:* with $x + y = c_1$, $\dfrac{dx}z = \dfrac{dz}{z^2 + c_1^2}\Rightarrow dx = \dfrac{z\,dz}{z^2 + c_1^2}\Rightarrow x = \tfrac12\ln\left(z^2 + c_1^2\right) + c_2$.
$$\boxed{\phi\left(x + y,\ 2x - \ln\left[z^2 + (x + y)^2\right]\right) = 0}$$
for an arbitrary function $\phi$.

@s 12
Take the Z-transform with $x(0) = 0$, $x(1) = 1$: $(z^2X - z) - 4zX + 4X = 0$, so
$$(z - 2)^2X(z) = z\ \Rightarrow\ X(z) = \frac{z}{(z - 2)^2} = \frac12\cdot\frac{2z}{(z-2)^2}$$
Using $Z^{-1}\left[\dfrac{az}{(z - a)^2}\right] = ka^k$ with $a = 2$:
$$\boxed{x(k) = \tfrac12\,k\,2^k = k\,2^{k-1}}$$
Check: $x(0) = 0$, $x(1) = 1$, $x(2) = 4 = 4x(1) - 4x(0)$ ✓, $x(3) = 12 = 4(4) - 4(1)$ ✓.

@s 13
Let $u = X(x)T(t)$ in $u_t = c^2u_{xx}$: $\dfrac{X''}X = \dfrac{T'}{c^2T} = k$. Three cases:
1. $k = 0$: $X = Ax + B$, $T = C$, so $u = (Ax + B)C$ (steady state, linear profile).
2. $k = p^2>0$: $X = Ae^{px} + Be^{-px}$, $T = Ce^{c^2p^2t}$, so $u = (Ae^{px} + Be^{-px})Ce^{c^2p^2t}$. This grows without bound with time and is not physical.
3. $k = -p^2<0$: $X = A\cos px + B\sin px$, $T = Ce^{-c^2p^2t}$, so
$$\boxed{u(x,t) = \left(A\cos px + B\sin px\right)e^{-c^2p^2t}}$$
which is the physically acceptable (decaying) solution. If the ends are kept at $0$, i.e. $u(0,t) = u(L,t) = 0$, then $A = 0$ and $p = \dfrac{n\pi}L$, so the complete solution is
$$\begin{gathered}u(x,t) = \sum_{n=1}^\infty b_n\sin\frac{n\pi x}L\,e^{-c^2n^2\pi^2t/L^2} \\ b_n = \frac2L\int_0^Lu(x,0)\sin\frac{n\pi x}Ldx\end{gathered}$$

**Or.** $u_{tt} = c^2u_{xx}$ with $u(0,t) = u(\pi,t) = 0$, $u_t(x,0) = 0$, $u(x,0) = x$. Separation of variables gives $u = (A\cos px + B\sin px)(C\cos cpt + D\sin cpt)$.
- $u(0,t) = 0\Rightarrow A = 0$. $u(\pi,t) = 0\Rightarrow\sin p\pi = 0\Rightarrow p = n$ (integer).
- $u_t(x,0) = 0\Rightarrow D = 0$.

So $u = \sum_{n=1}^\infty b_n\sin nx\cos nct$. With $u(x,0) = x = \sum b_n\sin nx$:
$$b_n = \frac2\pi\int_0^\pi x\sin nx\,dx = \frac2\pi\left[-\frac{x\cos nx}n + \frac{\sin nx}{n^2}\right]_0^\pi = \frac{2(-1)^{n+1}}n$$
$$\boxed{u(x,t) = 2\sum_{n=1}^\infty\frac{(-1)^{n+1}}n\sin nx\cos nct}$$

@s 14
**Derivation of the Navier–Stokes equation.** Take a small fixed fluid element $dx\,dy\,dz$ of a fluid of density $\rho$ and velocity $\vec V = (u, v, w)$. Newton's second law for the element gives $\rho\dfrac{D\vec V}{Dt}\,dx\,dy\,dz = $ (body force) + (surface forces).
- *Acceleration* (material derivative): $\dfrac{D\vec V}{Dt} = \dfrac{\partial\vec V}{\partial t} + (\vec V\cdot\nabla)\vec V$.
- *Body force* (gravity): $\rho\vec g\,dx\,dy\,dz$.
- *Surface forces* come from the stress tensor $\sigma_{ij} = -p\,\delta_{ij} + \tau_{ij}$. The net force on the element in the $x$-direction is $\left(\dfrac{\partial\sigma_{xx}}{\partial x} + \dfrac{\partial\sigma_{yx}}{\partial y} + \dfrac{\partial\sigma_{zx}}{\partial z}\right)dx\,dy\,dz$.

For a Newtonian fluid, viscous stress is proportional to the rate of strain: $\tau_{ij} = \mu\left(\dfrac{\partial V_i}{\partial x_j} + \dfrac{\partial V_j}{\partial x_i}\right) + \lambda\,\delta_{ij}\,\nabla\cdot\vec V$. For an incompressible fluid (continuity: $\nabla\cdot\vec V = 0$) with constant viscosity $\mu$, the viscous force reduces to $\mu\nabla^2\vec V$. The $x$-component of the momentum equation is
$$\rho\left(\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} + w\frac{\partial u}{\partial z}\right) = -\frac{\partial p}{\partial x} + \mu\left(\frac{\partial^2u}{\partial x^2} + \frac{\partial^2u}{\partial y^2} + \frac{\partial^2u}{\partial z^2}\right) + \rho g_x$$
and similarly for $y$ and $z$. In vector form, the **Navier–Stokes equation** is
$$\begin{gathered}\boxed{\rho\left[\frac{\partial\vec V}{\partial t} + (\vec V\cdot\nabla)\vec V\right] = -\nabla p + \mu\nabla^2\vec V + \rho\vec g} \\ \nabla\cdot\vec V = 0\end{gathered}$$
The terms are: inertia (local and convective), pressure gradient, viscous diffusion, and body force.

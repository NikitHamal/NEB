---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-III-ENSH201-2081-Chaitra.pdf
subject: Engineering Mathematics III
level: BE · Year II / Part I
code: ENSH 201
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: All programmes except B.Arch
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) Find the half range Fourier sine series of the function $f(x) = x$ in the interval $(0, 2)$. [[2]]
(b) Find the Fourier cosine integral of $f(x) = e^{-ax}$ for $x>0$, $a>0$. [[2]]
(c) Find the Fourier transform of $f(x) = \begin{cases}1 & \text{if } |x|<1\\ 0 & \text{if } |x|>1\end{cases}$ [[2]]

@q 2
(a) For a complex variable, show that $f(z) = \sin z$ is analytic. [[2]]
(b) Find the image of the circle $|z - i| = 1$ under the mapping $w = \dfrac1z$. [[2]]
(c) Show that $\displaystyle\int_C\frac{1}{z-a}\,dz = 2\pi i$ where $C$ is a unit circle $|z - a| = 1$. [[2]]

@q 3
(a) Expand the function $f(z) = \dfrac1z$ about $z = i$ in Taylor's series. [[2]]
(b) Find the residue of $f(z) = \dfrac{3z-4}{(z-2)(z-3)}$ at each of the singularities. [[2]]

@q 4
(a) Solve the partial differential equation $\dfrac{\partial^2u}{\partial x^2} = 12x^2(t+1)$ subject to $u(0,t) = \cos2t$ and $u_x(0,t) = \sin t$. [[2]]
(b) Find the solution of the equation $3u_x + 2u_y = 0$, by the method of the separation of the variables. [[2]]

@q 5
(a) If $Z[x(k)] = X(z)$, show that $x(1) = \displaystyle\lim_{z\to\infty}z[X(z) - x(0)]$, where the symbols have their usual meaning. [[2]]
(b) If $Z[x(k)] = X(z)$ and $y(k) = \displaystyle\sum_{m=0}^kx(m)$, then show that $Y(z) = \dfrac{z}{z-1}X(z)$. [[2]]

@q 6
Find the Fourier series for $f(x) = x^2$ in the interval $-\pi<x<\pi$ and deduce the relation $\dfrac{\pi^2}{12} = \dfrac1{1^2} - \dfrac1{2^2} + \dfrac1{3^2} - \dfrac1{4^2} + \cdots$ [[4]]

@q 7
Find the Fourier integral of $f(x) = \begin{cases}e^{-x}; & x>0\\ 0; & x<0\end{cases}$ and hence show that $\displaystyle\int_0^\infty\frac{\cos\omega x + \omega\sin\omega x}{1 + \omega^2}\,d\omega = \begin{cases}\pi e^{-x} & ;x>0\\ \dfrac\pi2 & ;x = 0\\ 0 & ;x<0\end{cases}$ [[3+1]]

@q 8
Find the Fourier transform of $f(x) = e^{-ax}$ and use the result to show $\displaystyle\int_0^\infty\frac{dx}{(a^2 + x^2)(b^2 + x^2)} = \frac{\pi}{2ab(a+b)}$. [[2+2]]

@q 9
Prove that $u = y^3 - 3x^2y$ is harmonic function. Find its harmonic conjugate and hence construct corresponding analytic function $w = f(z)$. [[2+2]]

@q 10
Evaluate $\displaystyle\int_0^{2\pi}\frac{d\theta}{5 + 4\sin\theta}$, using method of contour integration in the complex plane. [[4]]
@or
Evaluate $\displaystyle\oint_C\frac{\sin z}{z^2}\,dz$, where $C$ is any closed path not passing through 0. [[4]]

@q 11
Apply Charpit's method to solve the PDE: $p^2x + q^2y = z$, where the symbols have their usual meanings. [[4]]
@or
Solve the partial differential equation $(y - z)p + (x - y)q = (z - x)$, using Lagrange's method. [[4]]

@q 12
Derive one dimensional wave equation representing the vibration of the particles of a string. [[4]]
@or
Derive Navier-Stokes equation of fluid flow. [[4]]

@q 13
Solve one dimensional heat equation $\dfrac{\partial u}{\partial t} = \dfrac{\partial^2u}{\partial x^2}$, subject to $u(0,t) = u(\ell,t) = 0$ and $u(x,0) = u_0\sin\dfrac{\pi x}{\ell}$. [[4]]

@q 14
Apply Z-transform to solve the difference equation $x(k+2) - 4x(k+1) - 5x(k) = 0$, given that $x(0) = 0$, $x(1) = 1$. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** For the half-range sine series on $(0, L)$ with $L = 2$: $f(x) = \sum b_n\sin\dfrac{n\pi x}{2}$, $b_n = \dfrac2L\displaystyle\int_0^Lf(x)\sin\frac{n\pi x}L\,dx = \int_0^2x\sin\frac{n\pi x}2\,dx$. Integrating by parts,
$$b_n = \left[-\frac{2x}{n\pi}\cos\frac{n\pi x}2\right]_0^2 + \frac2{n\pi}\int_0^2\cos\frac{n\pi x}2\,dx = -\frac{4\cos n\pi}{n\pi} + \frac{4}{n^2\pi^2}\sin n\pi = \frac{4(-1)^{n+1}}{n\pi}$$
$$\boxed{x = \frac4\pi\left[\sin\frac{\pi x}2 - \frac12\sin\frac{2\pi x}2 + \frac13\sin\frac{3\pi x}2 - \cdots\right] = \frac4\pi\sum_{n=1}^\infty\frac{(-1)^{n+1}}n\sin\frac{n\pi x}2}$$

**(b)** The Fourier cosine integral is $f(x) = \dfrac2\pi\displaystyle\int_0^\infty A(\omega)\cos\omega x\,d\omega$ with $A(\omega) = \displaystyle\int_0^\infty f(t)\cos\omega t\,dt$. Here
$$A(\omega) = \int_0^\infty e^{-at}\cos\omega t\,dt = \frac{a}{a^2 + \omega^2}$$
$$\boxed{e^{-ax} = \frac2\pi\int_0^\infty\frac{a\cos\omega x}{a^2 + \omega^2}\,d\omega,\qquad x>0}$$
which also gives $\displaystyle\int_0^\infty\frac{\cos\omega x}{a^2 + \omega^2}d\omega = \frac{\pi}{2a}e^{-ax}$.

**(c)** $F(\omega) = \displaystyle\int_{-\infty}^\infty f(x)e^{-i\omega x}dx = \int_{-1}^1e^{-i\omega x}dx = \left[\frac{e^{-i\omega x}}{-i\omega}\right]_{-1}^1 = \frac{e^{i\omega} - e^{-i\omega}}{i\omega}$
$$\boxed{F(\omega) = \frac{2\sin\omega}{\omega}}\qquad\left(\text{with the symmetric convention }\tfrac1{\sqrt{2\pi}}\text{: }\sqrt{\tfrac2\pi}\,\tfrac{\sin\omega}\omega\right)$$

@s 2
**(a)** Write $\sin z = \sin(x + iy) = \sin x\cosh y + i\cos x\sinh y$, so $u = \sin x\cosh y$, $v = \cos x\sinh y$. The partial derivatives are
$$\begin{gathered}u_x = \cos x\cosh y = v_y \\ u_y = \sin x\sinh y = -v_x\end{gathered}$$
The Cauchy–Riemann equations hold for all $(x, y)$ and the partials are continuous, so $\sin z$ is analytic everywhere (an entire function).

**(b)** The circle is $x^2 + (y-1)^2 = 1$, i.e. $x^2 + y^2 = 2y$. It passes through $z = 0$, so its image under $w = 1/z$ is a straight line. With $w = u + iv = \dfrac{x - iy}{x^2 + y^2}$, we have $v = -\dfrac{y}{x^2 + y^2} = -\dfrac{y}{2y} = -\dfrac12$.
$$\boxed{\text{The image is the straight line } v = -\tfrac12\ (\text{Im}\,w = -\tfrac12)}$$

**(c)** On $C$: $z - a = e^{i\theta}$, $0\le\theta\le2\pi$, $dz = ie^{i\theta}d\theta$:
$$\int_C\frac{dz}{z-a} = \int_0^{2\pi}\frac{ie^{i\theta}}{e^{i\theta}}d\theta = i\int_0^{2\pi}d\theta = \boxed{2\pi i}$$

@s 3
**(a)** Put $z = i + (z - i)$ and expand for $|z - i|<1$:
$$\frac1z = \frac1{i + (z-i)} = \frac1i\cdot\frac{1}{1 + \dfrac{z-i}{i}} = -i\sum_{n=0}^\infty\left(-\frac{z-i}{i}\right)^n = -i\sum_{n=0}^\infty i^n(z-i)^n$$
(using $(-1/i)^n = i^n$). Hence
$$\boxed{\frac1z = -i + (z - i) + i(z-i)^2 - (z-i)^3 - i(z-i)^4 + \cdots,\qquad |z - i|<1}$$

**(b)** $f(z) = \dfrac{3z-4}{(z-2)(z-3)}$ has simple poles at $z = 2$ and $z = 3$.
$$\text{Res}_{z=2} = \frac{3(2) - 4}{2 - 3} = \boxed{-2},\qquad\text{Res}_{z=3} = \frac{3(3) - 4}{3 - 2} = \boxed{5}$$

@s 4
**(a)** Integrate $u_{xx} = 12x^2(t+1)$ with respect to $x$: $u_x = 4x^3(t+1) + f(t)$. The condition $u_x(0,t) = \sin t$ gives $f(t) = \sin t$. Integrating again, $u = x^4(t+1) + x\sin t + g(t)$, and $u(0,t) = \cos2t$ gives $g(t) = \cos2t$.
$$\boxed{u(x,t) = x^4(t+1) + x\sin t + \cos2t}$$

**(b)** Let $u = X(x)Y(y)$. Then $3X'Y + 2XY' = 0\Rightarrow\dfrac{3X'}{X} = -\dfrac{2Y'}{Y} = 3k$ (a constant). So $X' = kX$, giving $X = Ae^{kx}$, and $Y' = -\tfrac{3k}{2}Y$, giving $Y = Be^{-3ky/2}$.
$$\boxed{u(x,y) = Ce^{k(x - 3y/2)}}$$
where $C = AB$ and $k$ is an arbitrary constant. (Check: $3u_x + 2u_y = 3ku - 3ku = 0$ ✓.)

@s 5
**(a)** By definition $X(z) = \displaystyle\sum_{k=0}^\infty x(k)z^{-k} = x(0) + \frac{x(1)}z + \frac{x(2)}{z^2} + \cdots$. So
$$z\left[X(z) - x(0)\right] = x(1) + \frac{x(2)}z + \frac{x(3)}{z^2} + \cdots$$
As $z\to\infty$ every term except the first tends to 0. Hence $x(1) = \displaystyle\lim_{z\to\infty}z\left[X(z) - x(0)\right]$. ∎

**(b)** $y(k) = \sum_{m=0}^kx(m)$ gives $y(k) - y(k-1) = x(k)$ with $y(-1) = 0$. Taking the Z-transform, and using $Z[y(k-1)] = z^{-1}Y(z)$:
$$Y(z) - z^{-1}Y(z) = X(z)\ \Rightarrow\ Y(z)\left(\frac{z-1}z\right) = X(z)\ \Rightarrow\ \boxed{Y(z) = \frac{z}{z-1}X(z)}\ ∎$$

@s 6
$f(x) = x^2$ is even on $(-\pi, \pi)$, so $b_n = 0$.
$$\begin{gathered}a_0 = \frac2\pi\int_0^\pi x^2dx = \frac{2\pi^2}3 \\ a_n = \frac2\pi\int_0^\pi x^2\cos nx\,dx = \frac2\pi\left[\frac{x^2\sin nx}n + \frac{2x\cos nx}{n^2} - \frac{2\sin nx}{n^3}\right]_0^\pi = \frac{4(-1)^n}{n^2}\end{gathered}$$
$$\boxed{x^2 = \frac{\pi^2}3 + 4\sum_{n=1}^\infty\frac{(-1)^n}{n^2}\cos nx = \frac{\pi^2}{3} - 4\cos x + \cos2x - \frac49\cos3x + \cdots}$$
**Deduction.** The series converges to $f(0) = 0$ at $x = 0$ (continuous point):
$$0 = \frac{\pi^2}3 + 4\sum_{n=1}^\infty\frac{(-1)^n}{n^2}\ \Rightarrow\ \sum_{n=1}^\infty\frac{(-1)^{n+1}}{n^2} = \frac{\pi^2}{12}$$
$$\boxed{\frac{\pi^2}{12} = \frac1{1^2} - \frac1{2^2} + \frac1{3^2} - \frac1{4^2} + \cdots}$$

@s 7
The Fourier integral is $f(x) = \displaystyle\int_0^\infty[A(\omega)\cos\omega x + B(\omega)\sin\omega x]\,d\omega$ with $A = \dfrac1\pi\displaystyle\int_{-\infty}^\infty f(t)\cos\omega t\,dt$ and $B = \dfrac1\pi\displaystyle\int_{-\infty}^\infty f(t)\sin\omega t\,dt$.
$$\begin{gathered}A(\omega) = \frac1\pi\int_0^\infty e^{-t}\cos\omega t\,dt = \frac1\pi\cdot\frac{1}{1 + \omega^2} \\ B(\omega) = \frac1\pi\int_0^\infty e^{-t}\sin\omega t\,dt = \frac1\pi\cdot\frac{\omega}{1 + \omega^2}\end{gathered}$$
$$\boxed{f(x) = \frac1\pi\int_0^\infty\frac{\cos\omega x + \omega\sin\omega x}{1 + \omega^2}\,d\omega}$$
Hence $\displaystyle\int_0^\infty\frac{\cos\omega x + \omega\sin\omega x}{1 + \omega^2}d\omega = \pi f(x)$ at points of continuity: it equals $\pi e^{-x}$ for $x>0$ and $0$ for $x<0$. At the point of discontinuity $x = 0$ the integral converges to the mean $\dfrac{f(0^+) + f(0^-)}2 = \dfrac{1 + 0}2 = \dfrac12$, so its value is $\pi\cdot\dfrac12 = \dfrac\pi2$. ∎

@s 8
Take the Fourier cosine transform of $f(x) = e^{-ax}$ ($x>0$, which is $e^{-a|x|}$ extended evenly):
$$F_c(\omega) = \int_0^\infty e^{-ax}\cos\omega x\,dx = \frac{a}{a^2 + \omega^2}$$
(Its full Fourier transform is $\dfrac{2a}{a^2 + \omega^2}$.) Similarly, for $g(x) = e^{-bx}$, $G_c(\omega) = \dfrac{b}{b^2 + \omega^2}$. The Parseval relation for the cosine transform states
$$\int_0^\infty F_c(\omega)G_c(\omega)\,d\omega = \frac\pi2\int_0^\infty f(x)g(x)\,dx$$
$$ab\int_0^\infty\frac{d\omega}{(a^2 + \omega^2)(b^2 + \omega^2)} = \frac\pi2\int_0^\infty e^{-(a+b)x}dx = \frac{\pi}{2(a+b)}$$
$$\boxed{\int_0^\infty\frac{dx}{(a^2 + x^2)(b^2 + x^2)} = \frac{\pi}{2ab(a+b)}}\ ∎$$

@s 9
$u = y^3 - 3x^2y$. Then $u_x = -6xy$, $u_{xx} = -6y$, $u_y = 3y^2 - 3x^2$, $u_{yy} = 6y$, so $u_{xx} + u_{yy} = 0$ and $u$ is **harmonic**.

**Harmonic conjugate $v$.** By the Cauchy–Riemann equations $v_y = u_x = -6xy$, so $v = -3xy^2 + h(x)$. Also $v_x = -u_y = 3x^2 - 3y^2$, i.e. $-3y^2 + h'(x) = 3x^2 - 3y^2$, so $h' = 3x^2$, $h = x^3$.
$$\boxed{v = x^3 - 3xy^2 + c}$$
**Analytic function.**
$$w = f(z) = u + iv = (y^3 - 3x^2y) + i(x^3 - 3xy^2)$$
Since $z^3 = (x^3 - 3xy^2) + i(3x^2y - y^3)$, we have $iz^3 = -(3x^2y - y^3) + i(x^3 - 3xy^2) = u + iv$. Hence
$$\boxed{f(z) = iz^3 + c}$$

@s 10
Put $z = e^{i\theta}$: $d\theta = \dfrac{dz}{iz}$, $\sin\theta = \dfrac{z - z^{-1}}{2i}$, and $\theta: 0\to2\pi$ becomes the unit circle $|z| = 1$.
$$I = \oint_{|z|=1}\frac{1}{5 + \dfrac{4}{2i}\left(z - \dfrac1z\right)}\frac{dz}{iz} = \oint\frac{dz}{5iz + 2z^2 - 2} = \oint\frac{dz}{2z^2 + 5iz - 2}$$
The denominator factorises as $2(z + \tfrac i2)(z + 2i)$, with poles $z = -\tfrac i2$ (inside $|z| = 1$) and $z = -2i$ (outside). Residue at $z = -\tfrac i2$:
$$\text{Res} = \frac{1}{2\left(-\tfrac i2 + 2i\right)} = \frac{1}{2\cdot\tfrac{3i}2} = \frac1{3i}$$
$$I = 2\pi i\cdot\frac1{3i} = \boxed{\frac{2\pi}3}$$
(Check with $\int_0^{2\pi}\dfrac{d\theta}{a + b\sin\theta} = \dfrac{2\pi}{\sqrt{a^2 - b^2}} = \dfrac{2\pi}{3}$ ✓.)

**Or.** $\dfrac{\sin z}{z^2} = \dfrac1{z^2}\left(z - \dfrac{z^3}{6} + \cdots\right) = \dfrac1z - \dfrac z6 + \cdots$, so $z = 0$ is a simple pole with residue $1$. By the residue theorem, for a simple closed positively oriented path:
$$\oint_C\frac{\sin z}{z^2}dz = \begin{cases}2\pi i\cdot1 = \boxed{2\pi i} & \text{if } 0\text{ lies inside }C\\ \boxed{0} & \text{if } 0\text{ lies outside }C\end{cases}$$
(For a curve that winds $n$ times about 0 the value is $2\pi in$.)

@s 11
Let $F = p^2x + q^2y - z = 0$. Then $F_x = p^2$, $F_y = q^2$, $F_z = -1$, $F_p = 2px$, $F_q = 2qy$. Charpit's equations are
$$\frac{dp}{F_x + pF_z} = \frac{dq}{F_y + qF_z} = \frac{dx}{-F_p} = \frac{dy}{-F_q}$$
$$\frac{dp}{p^2 - p} = \frac{dq}{q^2 - q} = \frac{dx}{-2px} = \frac{dy}{-2qy}$$
From $\dfrac{dp}{p(p-1)} = \dfrac{dx}{-2px}$ we get $\dfrac{dp}{p-1} = -\dfrac{dx}{2x}$, so $\ln(p-1) = -\tfrac12\ln x + \ln a$, i.e. $(p-1)\sqrt x = a$. In the same way $(q-1)\sqrt y = b$. These give
$$\begin{gathered}p = 1 + \frac a{\sqrt x} \\ q = 1 + \frac b{\sqrt y}\end{gathered}$$
Substituting in the equation: $p^2x + q^2y = (\sqrt x + a)^2 + (\sqrt y + b)^2 = z$. Then $dz = p\,dx + q\,dy$ is integrated by $z = \left(\sqrt x + a\right)^2 + \left(\sqrt y + b\right)^2$, which is consistent (it gives $z_x = p$, $z_y = q$). The **complete integral** is
$$\boxed{z = \left(\sqrt x + a\right)^2 + \left(\sqrt y + b\right)^2}$$
where $a$ and $b$ are arbitrary constants. Check: $z_x = \dfrac{\sqrt x + a}{\sqrt x}$, so $x z_x^2 = (\sqrt x + a)^2$ and similarly for $y$, and the sum is $z$ ✓.

**Or (Lagrange).** The auxiliary equations of $(y - z)p + (x - y)q = z - x$ are
$$\frac{dx}{y - z} = \frac{dy}{x - y} = \frac{dz}{z - x}$$
*First integral.* Using multipliers $1, 1, 1$: $\dfrac{dx + dy + dz}{(y - z) + (x - y) + (z - x)} = \dfrac{dx + dy + dz}{0}$, so $dx + dy + dz = 0$, giving $x + y + z = c_1$.
*Second integral.* Use the multipliers $x,\ z,\ y$ ... in the form $\dfrac{x\,dx + z\,dy + y\,dz}{x(y - z) + z(x - y) + y(z - x)}$. The denominator is $xy - xz + zx - zy + yz - xy = 0$, so $x\,dx + z\,dy + y\,dz = 0$. Since $d\left(\tfrac{x^2}2\right) = x\,dx$ and $d(yz) = z\,dy + y\,dz$, this is $d\left(\tfrac{x^2}2 + yz\right) = 0$, giving $x^2 + 2yz = c_2$.
The The **general solution** is
$$\boxed{\phi\left(x + y + z,\ x^2 + 2yz\right) = 0}$$
for an arbitrary function $\phi$.

@s 12
**Derivation of the one-dimensional wave equation.** Consider a tightly stretched elastic string of linear density $\rho$ and constant tension $T$, lying along the $x$-axis and displaced slightly so that the transverse displacement is $u(x,t)$. Take an element $PQ$ of length $\delta x$. The tensions at $P$ and $Q$ act along the tangents, at small angles $\alpha$ and $\beta$ to the $x$-axis.
- *Horizontal:* there is no horizontal motion, so $T\cos\beta - T\cos\alpha = 0$ (for small angles, $\cos\approx1$), hence $T$ is constant along the string.
- *Vertical:* the net force is $T\sin\beta - T\sin\alpha$, which equals mass times acceleration, $\rho\,\delta x\,\dfrac{\partial^2u}{\partial t^2}$.

For small slopes $\sin\theta\approx\tan\theta = \dfrac{\partial u}{\partial x}$, so
$$\rho\,\delta x\,\frac{\partial^2u}{\partial t^2} = T\left[\left(\frac{\partial u}{\partial x}\right)_Q - \left(\frac{\partial u}{\partial x}\right)_P\right]$$
Divide by $\rho\,\delta x$ and let $\delta x\to0$:
$$\boxed{\frac{\partial^2u}{\partial t^2} = c^2\frac{\partial^2u}{\partial x^2},\qquad c^2 = \frac T\rho}$$

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
Let $u = X(x)T(t)$. Then $XT' = X''T$, so $\dfrac{X''}X = \dfrac{T'}T = -\lambda^2$ (a negative constant, for a solution that decays with time). Hence $X'' + \lambda^2X = 0$, $X = A\cos\lambda x + B\sin\lambda x$, and $T = Ce^{-\lambda^2t}$.
*Boundary conditions.* $u(0,t) = 0\Rightarrow A = 0$. $u(\ell,t) = 0\Rightarrow B\sin\lambda\ell = 0\Rightarrow\lambda = \dfrac{n\pi}\ell$. The general solution is
$$u(x,t) = \sum_{n=1}^\infty b_n\sin\frac{n\pi x}\ell\,e^{-n^2\pi^2t/\ell^2}$$
*Initial condition.* $u(x,0) = \sum b_n\sin\dfrac{n\pi x}\ell = u_0\sin\dfrac{\pi x}\ell$. Comparing coefficients: $b_1 = u_0$ and $b_n = 0$ for $n\ge2$.
$$\boxed{u(x,t) = u_0\,e^{-\pi^2t/\ell^2}\sin\frac{\pi x}\ell}$$

@s 14
Take the Z-transform with $x(0) = 0$, $x(1) = 1$. Using $Z[x(k+2)] = z^2X - z^2x(0) - zx(1) = z^2X - z$ and $Z[x(k+1)] = zX - zx(0) = zX$:
$$(z^2X - z) - 4zX - 5X = 0\ \Rightarrow\ (z^2 - 4z - 5)X(z) = z\ \Rightarrow\ X(z) = \frac{z}{(z - 5)(z + 1)}$$
Partial fractions: $\dfrac{X(z)}z = \dfrac1{(z-5)(z+1)} = \dfrac16\left(\dfrac1{z-5} - \dfrac1{z+1}\right)$, so $X(z) = \dfrac16\left(\dfrac{z}{z-5} - \dfrac{z}{z+1}\right)$. Inverting:
$$\boxed{x(k) = \frac{5^k - (-1)^k}6,\qquad k\ge0}$$
Check: $x(0) = 0$, $x(1) = 1$, $x(2) = 4 = 4x(1) + 5x(0)$ ✓, $x(3) = 21 = 4(4) + 5(1)$ ✓.

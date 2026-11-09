---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-ENSH101-2081-Chaitra.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: ENSH 101
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: All programmes except B.Arch
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering. Regular, new course. Pass marks 24.
category: University Exam
---
<small>Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) List the indeterminate forms for which L'Hospital's rule can be applied. Evaluate $\lim_{x \to 0} x^{\tan x}$ using L'Hospital's rule. [[2]]
(b) Assuming the validity of the expansion, find the expansion of $\cosh x$ by using Maclaurin's series. [[2]]
(c) Find the radius of curvature of $xy = c^2$ at $(c, c)$. [[2]]

@q 2
(a) Evaluate the improper integral $\int_0^1 \log_e x\,dx$. [[2]]
(b) Evaluate $\int_0^1 x^6\sqrt{1 - x^2}\,dx$ using properties of Beta and Gamma functions. [[2]]
(c) The area bounded by the parabola $y^2 = 4px$ and the line $x = a$ revolves about the $x$-axis. Find the volume generated. [[2]]

@q 3
(a) Solve the differential equation $\dfrac{dy}{dx} + \dfrac{1}{x}\,y = e^{-x}$. [[2]]
(b) Define Clairaut's equation. Find the general solution of $y = px + p - p^2$, where $p = \dfrac{dy}{dx}$. [[2]]
(c) Find the solution of the differential equation $y'' - 3y' + 2y = e^{-3x}$. [[2]]

@q 4
Transform the equation $x^2 + y^2 - 6x + 4y - 4 = 0$ to a parallel axes system with origin $(3, -2)$. [[2]]

@q 5
(a) Prove that the lines $x = ay + b,\ z = cy + d$ and $x = a'y + b',\ z = c'y + d'$ are perpendicular if $aa' + cc' + 1 = 0$. [[2]]
(b) If the tangent plane to the sphere $x^2 + y^2 + z^2 = r^2$ makes intercepts $a, b, c$ on the coordinate axes, then prove that $\dfrac{1}{a^2} + \dfrac{1}{b^2} + \dfrac{1}{c^2} = \dfrac{1}{r^2}$. [[2]]

@q 6
Find the asymptotes of $x^3 + y^3 - xy^2 - x^2y + x^2 - y^2 - 1 = 0$. [[4]]

@q 7
Find the radius of curvature of the curve $\sqrt{x} + \sqrt{y} = \sqrt{a}$ at the point where it cuts the line $y = x$. [[4]]

@q 8
Apply the method of differentiation under the integral sign to evaluate $\int_0^\infty \dfrac{e^{-ax} - e^{-bx}}{x}\,dx$. [[4]]

@q 9
Find the centroid of the region $R$ bounded by $y = \cos x,\ y = 0,\ x = 0$ and $x = \dfrac{\pi}{2}$. [[4]]

@q 10
Identify, sketch and describe the graph of the conic $r = \dfrac{4\sec\theta}{2\sec\theta - 1}$. [[4]]

@q 11
Show that the lines $\dfrac{x+1}{-3} = \dfrac{y-3}{2} = \dfrac{z+2}{1}$ and $\dfrac{x}{1} = \dfrac{y-7}{-3} = \dfrac{z+7}{2}$ are coplanar. Also find their point of intersection and the common plane. [[4]]

@q 12
Find the equation of the right circular cone with vertex at $(2, -3, 5)$, whose axis makes equal angles with the co-ordinate axes and whose semi-vertical angle is $30^\circ$. [[4]]
@or
Find the equation of the right circular cylinder of radius 2 whose axis is the line $\dfrac{x-1}{-2} = \dfrac{y-2}{1} = \dfrac{z-3}{2}$. [[4]]

@q 13
Solve the differential equation $x^2\dfrac{d^2y}{dx^2} - x\dfrac{dy}{dx} + y = \log_e x$. [[4]]

@q 14
Find the current $i$ in the RLC circuit, assuming zero initial current and charge $q$, if $R = 80\ \Omega$, $L = 20$ henrys, $C = 0.01$ farads and $E = 100$ volts. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** L'Hospital's rule applies directly to the forms $\dfrac{0}{0}$ and $\dfrac{\infty}{\infty}$. The forms $0\cdot\infty$, $\infty-\infty$, $0^0$, $1^\infty$ and $\infty^0$ are first rewritten as one of these two (by taking logarithms for the exponential ones).

Let $y = x^{\tan x}$, a $0^0$ form as $x \to 0^+$. Then $\ln y = \tan x\,\ln x = \dfrac{\ln x}{\cot x}$, which is $\dfrac{-\infty}{\infty}$. Apply the rule:
$$\lim_{x\to 0}\ln y = \lim_{x\to 0}\frac{1/x}{-\mathrm{cosec}^2 x} = -\lim_{x\to 0}\frac{\sin^2 x}{x} = -\lim_{x\to 0}\left(\frac{\sin x}{x}\right)\sin x = -1\cdot 0 = 0$$
Hence $\lim_{x\to 0}x^{\tan x} = e^0 = \mathbf{1}$.

**(b)** Let $f(x) = \cosh x$. Then $f(0)=1$, $f'(x)=\sinh x$ so $f'(0)=0$, $f''(x)=\cosh x$ so $f''(0)=1$, and the derivatives alternate between $\sinh x$ (value 0) and $\cosh x$ (value 1) at $x=0$. Maclaurin's series $f(x)=f(0)+xf'(0)+\dfrac{x^2}{2!}f''(0)+\dots$ gives
$$\cosh x = 1 + \frac{x^2}{2!} + \frac{x^4}{4!} + \frac{x^6}{6!} + \dots = \sum_{n=0}^{\infty}\frac{x^{2n}}{(2n)!}$$

**(c)** From $y = \dfrac{c^2}{x}$: $y' = -\dfrac{c^2}{x^2}$ and $y'' = \dfrac{2c^2}{x^3}$. At $(c, c)$: $y' = -1$ and $y'' = \dfrac{2}{c}$. So
$$\rho = \frac{(1 + y'^2)^{3/2}}{|y''|} = \frac{(1+1)^{3/2}}{2/c} = \frac{2\sqrt{2}\,c}{2} = \sqrt{2}\,c$$


@s 2
**(a)** The integrand is unbounded at $x = 0$, so write $\int_0^1\ln x\,dx = \lim_{\epsilon\to 0^+}\int_\epsilon^1\ln x\,dx = \lim_{\epsilon\to 0^+}\big[x\ln x - x\big]_\epsilon^1$. Since $\epsilon\ln\epsilon \to 0$,
$$\int_0^1\ln x\,dx = (0 - 1) - (0 - 0) = \mathbf{-1}$$
The integral converges.

**(b)** Put $x^2 = t$, so $x = t^{1/2}$ and $dx = \tfrac12 t^{-1/2}dt$:
$$I = \tfrac12\int_0^1 t^{5/2}(1-t)^{1/2}\,dt = \tfrac12\,B\!\left(\tfrac72, \tfrac32\right) = \frac{1}{2}\cdot\frac{\Gamma(7/2)\,\Gamma(3/2)}{\Gamma(5)}$$
With $\Gamma(3/2) = \dfrac{\sqrt\pi}{2}$ and $\Gamma(7/2) = \dfrac52\cdot\dfrac32\cdot\dfrac{\sqrt\pi}{2} = \dfrac{15\sqrt\pi}{8}$, and $\Gamma(5) = 4! = 24$:
$$I = \frac12\cdot\frac{\frac{15\sqrt\pi}{8}\cdot\frac{\sqrt\pi}{2}}{24} = \frac12\cdot\frac{15\pi}{16\cdot 24} = \frac{5\pi}{256}$$

**(c)** The region lies between $x = 0$ and $x = a$. Rotating about the $x$-axis,
$$V = \pi\int_0^a y^2\,dx = \pi\int_0^a 4px\,dx = 4\pi p\left[\frac{x^2}{2}\right]_0^a = 2\pi p\,a^2 \text{ cubic units}$$


@s 3
**(a)** The equation is linear: $\dfrac{dy}{dx} + \dfrac1x y = e^{-x}$. Integrating factor $= e^{\int dx/x} = x$. Then $\dfrac{d}{dx}(xy) = xe^{-x}$, and by parts $\int xe^{-x}dx = -xe^{-x} - e^{-x}$. So
$$xy = -(x+1)e^{-x} + C \quad\Rightarrow\quad y = \frac{C}{x} - \frac{(x+1)e^{-x}}{x}$$

**(b)** *Clairaut's equation* is a first-order equation of the form $y = px + f(p)$, where $p = \dfrac{dy}{dx}$. Its general solution is obtained by replacing $p$ with an arbitrary constant $c$ (differentiating gives $(x + f'(p))\dfrac{dp}{dx} = 0$, and the factor $\dfrac{dp}{dx}=0$ gives $p = c$).

Here $f(p) = p - p^2$, so the general solution is
$$y = cx + c - c^2$$
(The singular solution comes from $x + 1 - 2p = 0$: $p = \dfrac{x+1}{2}$, giving $y = \dfrac{(x+1)^2}{4}$.)

**(c)** Auxiliary equation $m^2 - 3m + 2 = 0 \Rightarrow m = 1, 2$, so $y_c = C_1e^{x} + C_2e^{2x}$. For the particular integral replace $D$ by $-3$:
$$y_p = \frac{e^{-3x}}{(-3)^2 - 3(-3) + 2} = \frac{e^{-3x}}{20}$$
$$y = C_1e^{x} + C_2e^{2x} + \frac{1}{20}e^{-3x}$$


@s 4
Shifting the origin to $(3, -2)$ means $x = X + 3$ and $y = Y - 2$. Completing the square in the given equation,
$$(x-3)^2 + (y+2)^2 - 9 - 4 - 4 = 0 \quad\Rightarrow\quad (x-3)^2 + (y+2)^2 = 17$$
Substituting $x - 3 = X$ and $y + 2 = Y$:
$$X^2 + Y^2 = 17$$
It is a circle of radius $\sqrt{17}$ whose centre is the new origin.


@s 5
**(a)** Write the first line as $\begin{gathered}\dfrac{x-b}{a} = \dfrac{y}{1} = \dfrac{z-d}{c}\end{gathered}$, which has direction ratios $(a, 1, c)$; the second line has direction ratios $(a', 1, c')$. Two lines are perpendicular when the dot product of their directions is zero:
$$aa' + 1\cdot 1 + cc' = 0 \quad\Rightarrow\quad aa' + cc' + 1 = 0$$

**(b)** Let the plane touch the sphere at $(x_1, y_1, z_1)$, so $x_1^2 + y_1^2 + z_1^2 = r^2$. The tangent plane there is $xx_1 + yy_1 + zz_1 = r^2$, i.e. $\dfrac{x}{r^2/x_1} + \dfrac{y}{r^2/y_1} + \dfrac{z}{r^2/z_1} = 1$. The intercepts are $a = \dfrac{r^2}{x_1}$, $b = \dfrac{r^2}{y_1}$, $c = \dfrac{r^2}{z_1}$. Therefore
$$\frac{1}{a^2} + \frac{1}{b^2} + \frac{1}{c^2} = \frac{x_1^2 + y_1^2 + z_1^2}{r^4} = \frac{r^2}{r^4} = \frac{1}{r^2}$$


@s 6
Group the cubic terms: $x^3 - x^2y - xy^2 + y^3 = x^2(x - y) - y^2(x - y) = (x-y)(x^2-y^2)$, so the curve is
$$(x+y)(x-y)^2 + (x-y)(x+y) - 1 = 0 \quad\Rightarrow\quad (x+y)(x-y)(x-y+1) = 1$$
Let $u = x - y$ and $v = x + y$, so the curve is $v\,u\,(u+1) = 1$. Along a branch going to infinity either $v \to \infty$ with $u$ staying finite, or $u \to \infty$ with $v$ finite.

- If $v \to \infty$, then $u(u+1) = \dfrac{1}{v} \to 0$, so $u \to 0$ or $u \to -1$: the lines $x - y = 0$ and $x - y + 1 = 0$.
- If $u \to \infty$, then $v = \dfrac{1}{u(u+1)} \to 0$: the line $x + y = 0$.

Check by the standard method: the highest-degree part is $\phi_3 = (x-y)^2(x+y)$, whose roots $m = 1$ (twice) and $m = -1$ give slopes $1$ and $-1$; for the repeated root $m = 1$, $\tfrac{c^2}{2}\phi_3''(1) + c\,\phi_2'(1) = 2c^2 - 2c = 0$ gives $c = 0, 1$; for $m = -1$, $c = -\dfrac{\phi_2(-1)}{\phi_3'(-1)} = 0$.

**Asymptotes:** $x + y = 0$, $\ x - y = 0$, $\ x - y + 1 = 0$.


@s 7
The line $y = x$ meets the curve where $2\sqrt{x} = \sqrt{a}$, so $x = y = \dfrac{a}{4}$.

Differentiate $x^{1/2} + y^{1/2} = a^{1/2}$: $\dfrac{1}{2\sqrt x} + \dfrac{y'}{2\sqrt y} = 0$, so $y' = -\sqrt{y/x}$, which is $-1$ at $\left(\dfrac a4, \dfrac a4\right)$.

Differentiate again, with $y' = -y^{1/2}x^{-1/2}$:
$$y'' = -\frac12\left[\frac{y'}{\sqrt{x}\sqrt{y}} - \frac{\sqrt y}{x^{3/2}}\right]$$
At the point, $\sqrt x\sqrt y = \dfrac a4$ and $\dfrac{\sqrt y}{x^{3/2}} = \dfrac1x = \dfrac4a$, so
$$y'' = -\frac12\left[-\frac4a - \frac4a\right] = \frac4a$$
$$\rho = \frac{(1+y'^2)^{3/2}}{|y''|} = \frac{2^{3/2}}{4/a} = \frac{a}{\sqrt2}$$


@s 8
Let $I(a) = \int_0^\infty\dfrac{e^{-ax} - e^{-bx}}{x}\,dx$ with $a, b > 0$ and $b$ fixed. Differentiating under the integral sign with respect to $a$ (the limits do not depend on $a$):
$$\frac{dI}{da} = \int_0^\infty\frac{\partial}{\partial a}\left(\frac{e^{-ax} - e^{-bx}}{x}\right)dx = -\int_0^\infty e^{-ax}\,dx = -\frac1a$$
Integrating, $I(a) = -\ln a + C$. When $a = b$ the integrand is zero, so $I(b) = 0$ and $C = \ln b$. Hence
$$\int_0^\infty\frac{e^{-ax} - e^{-bx}}{x}\,dx = \ln\frac{b}{a}$$


@s 9
Area $A = \int_0^{\pi/2}\cos x\,dx = [\sin x]_0^{\pi/2} = 1$.

$$\bar x = \frac1A\int_0^{\pi/2}x\cos x\,dx = \big[x\sin x + \cos x\big]_0^{\pi/2} = \left(\frac\pi2 + 0\right) - (0 + 1) = \frac\pi2 - 1$$
$$\bar y = \frac1A\int_0^{\pi/2}\tfrac12\cos^2x\,dx = \frac14\int_0^{\pi/2}(1 + \cos 2x)\,dx = \frac14\cdot\frac\pi2 = \frac\pi8$$
**Centroid:** $\left(\dfrac\pi2 - 1,\ \dfrac\pi8\right) \approx (0.571,\ 0.393)$.


@s 10
Multiply the numerator and denominator by $\cos\theta$:
$$r = \frac{4\sec\theta}{2\sec\theta - 1} = \frac{4}{2 - \cos\theta} = \frac{2}{1 - \tfrac12\cos\theta}$$
This is the polar form $r = \dfrac{\ell}{1 - e\cos\theta}$ with $e = \dfrac12 < 1$ and semi-latus rectum $\ell = 2$. The conic is an **ellipse** with a focus at the pole and the directrix $x = -\dfrac{\ell}{e} = -4$.

| Property | Value |
|---|---|
| Vertices ($\theta = 0$, $\theta = \pi$) | $r = 4$ and $r = \dfrac43$, i.e. $(4, 0)$ and $\left(-\dfrac43, 0\right)$ |
| Semi-major axis | $a = \dfrac{\ell}{1 - e^2} = \dfrac{8}{3}$ |
| Semi-minor axis | $b = a\sqrt{1 - e^2} = \dfrac{4}{\sqrt3}$ |
| Centre | $\left(\dfrac43, 0\right)$ (since $ae = \dfrac43$, the pole is the left focus) |
| Ends of latus rectum ($\theta = \pm\dfrac\pi2$) | $r = 2$: $(0, \pm 2)$ |

Cartesian form: $2r = 4 + r\cos\theta$ gives $4r^2 = (x + 4)^2$, so $3x^2 + 4y^2 - 8x - 16 = 0$, or $\dfrac{(x - 4/3)^2}{64/9} + \dfrac{y^2}{16/3} = 1$.

```figure caption="The ellipse r = 4 / (2 - cos θ): focus at the pole, e = 1/2, directrix x = -4."
fig, ax = plt.subplots(figsize=(4.6, 3.0))
th = np.linspace(0, 2*np.pi, 400)
r = 4/(2 - np.cos(th))
ax.plot(r*np.cos(th), r*np.sin(th), color=ACCENT, lw=2)
ax.axvline(-4, color=GRID, ls='--', lw=1.1)
ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
ax.plot([0, 4/3], [0, 0], 'o', color=INK, ms=4)
ax.text(0.12, -0.42, 'F (pole)', fontsize=8); ax.text(1.45, -0.42, 'centre', fontsize=8)
ax.text(-3.9, 1.7, 'directrix\nx = -4', fontsize=8)
ax.plot([0, 0], [-2, 2], color=INK, lw=0.9, ls=':'); ax.text(0.1, 1.9, 'latus rectum', fontsize=7)
ax.set_aspect('equal'); ax.set_xlim(-4.8, 4.8); ax.set_ylim(-2.6, 2.6)
ax.spines[['top', 'right']].set_visible(False)
```


@s 11
The first line passes through $A(-1, 3, -2)$ with direction $\vec d_1 = (-3, 2, 1)$; the second through $B(0, 7, -7)$ with direction $\vec d_2 = (1, -3, 2)$. Then $\overrightarrow{AB} = (1, 4, -5)$.

**Coplanar:** the scalar triple product must vanish.
$$[\overrightarrow{AB}, \vec d_1, \vec d_2] = \begin{vmatrix}1 & 4 & -5\\ -3 & 2 & 1\\ 1 & -3 & 2\end{vmatrix} = 1(4 + 3) - 4(-6 - 1) + (-5)(9 - 2) = 7 + 28 - 35 = 0$$
So the lines are coplanar.

**Point of intersection.** A point of the first line is $(-1 - 3s,\ 3 + 2s,\ -2 + s)$ and of the second $(t,\ 7 - 3t,\ -7 + 2t)$. Equating $x$: $t = -1 - 3s$. Equating $y$: $3 + 2s = 7 - 3t = 10 + 9s$, so $s = -1$ and $t = 2$. Check $z$: $-2 + (-1) = -3$ and $-7 + 4 = -3$. The point is $(2, 1, -3)$.

**Common plane.** Normal $= \vec d_1\times\vec d_2 = (2\cdot 2 - 1\cdot(-3),\ 1\cdot 1 - (-3)\cdot 2,\ (-3)(-3) - 2\cdot 1) = (7, 7, 7)\parallel(1, 1, 1)$. Through $(2, 1, -3)$ the plane is $x + y + z = 2 + 1 - 3 = 0$:
$$x + y + z = 0$$
(Check: $A$ gives $-1 + 3 - 2 = 0$ and $B$ gives $0 + 7 - 7 = 0$.)


@s 12
**Either (cone).** The axis has equal direction cosines, so its direction is $(1, 1, 1)$ with $|\,(1,1,1)\,| = \sqrt3$. Let $P(x, y, z)$ be on the cone and put $X = x - 2$, $Y = y + 3$, $Z = z - 5$, the components of the generator from the vertex. The angle between the generator and the axis is $30^\circ$:
$$\cos 30^\circ = \frac{X + Y + Z}{\sqrt3\,\sqrt{X^2 + Y^2 + Z^2}}$$
Squaring, with $\cos^2 30^\circ = \dfrac34$: $4(X + Y + Z)^2 = 9(X^2 + Y^2 + Z^2)$, which simplifies to
$$5(X^2 + Y^2 + Z^2) - 8(XY + YZ + ZX) = 0$$
$$5\big[(x-2)^2 + (y+3)^2 + (z-5)^2\big] - 8\big[(x-2)(y+3) + (y+3)(z-5) + (z-5)(x-2)\big] = 0$$

**Or (cylinder).** The axis passes through $A(1, 2, 3)$ with direction $\vec d = (-2, 1, 2)$, $|\vec d| = 3$. A point $P$ is at distance $2$ from the axis when $|\overrightarrow{AP}\times\vec d|^2 = 2^2|\vec d|^2 = 36$. With $X = x - 1$, $Y = y - 2$, $Z = z - 3$:
$$\overrightarrow{AP}\times\vec d = (2Y - Z,\ -2Z - 2X,\ X + 2Y)$$
$$(2Y - Z)^2 + 4(X + Z)^2 + (X + 2Y)^2 = 36$$
$$5X^2 + 8Y^2 + 5Z^2 + 4XY - 4YZ + 8ZX = 36$$
i.e. $5(x-1)^2 + 8(y-2)^2 + 5(z-3)^2 + 4(x-1)(y-2) - 4(y-2)(z-3) + 8(z-3)(x-1) = 36$. (A point on the axis such as $X, Y, Z = -2, 1, 2$ makes the left side $0$, as it must.)


@s 13
This is a Cauchy-Euler equation. Put $x = e^t$, $t = \ln x$ and $D = \dfrac{d}{dt}$, so $x\dfrac{dy}{dx} = Dy$ and $x^2\dfrac{d^2y}{dx^2} = D(D-1)y$:
$$\big[D(D - 1) - D + 1\big]y = t \quad\Rightarrow\quad (D - 1)^2y = t$$
Complementary function (repeated root $m = 1$): $y_c = (C_1 + C_2t)e^t$. Particular integral:
$$y_p = \frac{1}{(1 - D)^2}\,t = (1 + 2D + 3D^2 + \dots)\,t = t + 2$$
Returning to $x$:
$$y = (C_1 + C_2\ln x)\,x + \ln x + 2$$
(Check: for $y = \ln x + 2$, $x^2(-x^{-2}) - x(x^{-1}) + \ln x + 2 = \ln x$.)


@s 14
For a series RLC circuit, $L\dfrac{di}{dt} + Ri + \dfrac{q}{C} = E$ with $i = \dfrac{dq}{dt}$:
$$20q'' + 80q' + 100q = 100 \quad\Rightarrow\quad q'' + 4q' + 5q = 5$$
Auxiliary equation $m^2 + 4m + 5 = 0$ gives $m = -2 \pm i$ (underdamped). A constant particular solution has $5q = 5$, so $q_p = 1$:
$$q = e^{-2t}(A\cos t + B\sin t) + 1$$
Initial charge $q(0) = 0$: $A + 1 = 0$, so $A = -1$. Initial current $i(0) = q'(0) = 0$, with $q' = e^{-2t}\big[(-2A + B)\cos t + (-2B - A)\sin t\big]$: $-2A + B = 0$, so $B = -2$. Thus
$$q(t) = 1 - e^{-2t}(\cos t + 2\sin t)$$
$$i = \frac{dq}{dt} = e^{-2t}\big[2(\cos t + 2\sin t) - (-\sin t + 2\cos t)\big] = 5e^{-2t}\sin t$$
**Current:** $i(t) = 5e^{-2t}\sin t$ amperes. The charge settles at $q = CE = 1$ coulomb.

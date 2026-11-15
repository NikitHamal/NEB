---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH101-2081-Baishakh.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 101
year_bs: 2081 Baishakh
cal: BS
year_ad: 2024
stream: All programmes except B.Arch
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) Assuming the validity of the expansion, show that $e^x = 1 + x + \dfrac{x^2}{2!} + \dfrac{x^3}{3!} + \cdots$ [[2]]
(b) Find the pedal equation of the polar curve $r = a\theta$. [[2]]
(c) Evaluate the limit $\displaystyle\lim_{x\to\infty}\dfrac{e^{px}}{x^{100}}$, $p > 0$, and interpret the limit. [[2]]

@q 2
(a) Evaluate the integral $\displaystyle\int_1^\infty \dfrac{1}{1+x^2}\,dx$. [[2]]
(b) Use the gamma function to evaluate $\displaystyle\int_0^{\pi/2}\sin^3 x\cos^5 x\,dx$. [[2]]
(c) Find the arc length of the semi-cubical parabola $ay^2 = x^3$ from $x = 0$ to $x = a$. [[2]]

@q 3
(a) Solve the differential equation $\dfrac{dy}{dx} + \dfrac{y}{x} = x^2$. [[2]]
(b) Define Clairaut's differential equation and find the general solution of $\sin(y - px) = p$, where $p = \dfrac{dy}{dx}$. [[2]]
(c) Solve $x''(t) + \mu x(t) = 0$, $\mu > 0$, given that $x = a$ and $x' = 0$ when $t = \dfrac{\pi}{2\sqrt{\mu}}$. [[2]]

@q 4
Transform the equation $2x^2 + 4xy + 5y^2 - 4x - 22y + 7 = 0$ to parallel axes through $(-2, 3)$. [[2]]

@q 5
(a) Show that the lines $\dfrac{x+3}{2} = \dfrac{y+5}{3} = \dfrac{z-7}{-3}$ and $\dfrac{x+1}{4} = \dfrac{y+1}{5} = \dfrac{z+1}{-1}$ are coplanar. [[2]]
(b) Find the equation of the sphere through the circle $x^2 + y^2 + z^2 = 9,\ x + 3y + 4z = 2$ and the origin. [[2]]

@q 6
Find the asymptotes of the curve $y^3 - xy^2 - x^2y + x^3 + x^2 - y^2 = 1$. [[4]]

@q 7
Find the radius of curvature of the curve $y = x^2(x - 3)$ at the point where the tangent is parallel to the $x$-axis. [[4]]

@q 8
Evaluate $\displaystyle\int_0^\infty \dfrac{\tan^{-1}(ax)}{x(1+x^2)}\,dx$ using differentiation under the integral sign. [[4]]
@or
Find the volume of the ellipsoid obtained by the rotation of the ellipse $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1$. [[4]]

@q 9
Find the centroid of the region $R$ bounded by $y = \cos x,\ y = 0,\ x = 0$ and $x = \pi/2$. [[4]]

@q 10
Identify the conic $9x^2 + 4xy + 6y^2 - 22x - 16y + 9 = 0$. Find the centre and the lengths of the axes. [[4]]

@q 11
Find the length and the equation of the shortest distance between the lines $\dfrac{x-3}{3} = \dfrac{y-8}{-1} = \dfrac{z-3}{1}$ and $2x - 3y + 27 = 0,\ 2y - z + 20 = 0$. [[4]]

@q 12
Find the equation of a right circular cylinder of radius 2 units, whose axis passes through the point $(1, 2, 3)$ and has direction ratios $2, -3, 6$. [[4]]
@or
Find the equation of the right circular cone with vertex $(1, 1, 1)$, axis the line $\dfrac{x-1}{-1} = \dfrac{y-1}{2} = \dfrac{z-1}{3}$ and semi-vertical angle $30^\circ$. [[4]]

@q 13
Solve $\dfrac{dy}{dx} + xy\log y = xy(\log y)^2$. [[4]]

@q 14
A mass of 1 kg is attached at one end of a spring on a frictionless horizontal surface fixed at one end. A force of 6 N applied to the spring stretches it 1.5 m from its natural length. If the mass is initially released from rest from 1 m to the right of its equilibrium position, determine the position of the mass as a function of time $t$. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** Let $e^x = a_0 + a_1x + a_2x^2 + a_3x^3 + \cdots$. Differentiating repeatedly, every derivative of $e^x$ is again $e^x$, so $f^{(n)}(0) = 1$ for all $n$. Maclaurin's theorem $f(x) = f(0) + xf'(0) + \dfrac{x^2}{2!}f''(0) + \dfrac{x^3}{3!}f'''(0) + \cdots$ then gives
$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

**(b)** For $r = a\theta$, $\dfrac{dr}{d\theta} = a$. The polar form of the pedal relation is
$$\frac{1}{p^2} = \frac{1}{r^2} + \frac{1}{r^4}\left(\frac{dr}{d\theta}\right)^2 = \frac{1}{r^2} + \frac{a^2}{r^4} = \frac{r^2 + a^2}{r^4}$$
$$\boxed{p = \frac{r^2}{\sqrt{r^2 + a^2}}}\qquad\text{or}\qquad p^2(r^2 + a^2) = r^4$$

**(c)** The form is $\dfrac{\infty}{\infty}$. Apply L'Hospital's rule 100 times; each time the power of $x$ drops by one and a factor $p$ comes out of the exponential:
$$\lim_{x\to\infty}\frac{e^{px}}{x^{100}} = \lim_{x\to\infty}\frac{p^{100}e^{px}}{100!} = \infty \quad (p>0)$$
**Interpretation:** the exponential $e^{px}$ grows faster than any fixed power of $x$, however large (here $x^{100}$), so the ratio increases without bound.

@s 2
**(a)** $\displaystyle\int_1^\infty\frac{dx}{1+x^2} = \Big[\tan^{-1}x\Big]_1^\infty = \frac\pi2 - \frac\pi4 = \frac{\pi}{4}$.

**(b)** Use $\displaystyle\int_0^{\pi/2}\sin^{m}x\cos^{n}x\,dx = \tfrac12 B\!\left(\tfrac{m+1}{2}, \tfrac{n+1}{2}\right)$ with $m = 3,\ n = 5$:
$$I = \frac12 B(2, 3) = \frac12\cdot\frac{\Gamma(2)\Gamma(3)}{\Gamma(5)} = \frac12\cdot\frac{1\cdot 2}{24} = \frac{1}{24}$$

**(c)** From $y = \dfrac{x^{3/2}}{\sqrt a}$, $\dfrac{dy}{dx} = \dfrac{3}{2}\dfrac{x^{1/2}}{\sqrt a}$, so $1 + y'^2 = 1 + \dfrac{9x}{4a}$.
$$L = \int_0^a\sqrt{1 + \frac{9x}{4a}}\,dx = \frac{4a}{9}\cdot\frac23\left[\left(1 + \frac{9x}{4a}\right)^{3/2}\right]_0^a = \frac{8a}{27}\left[\left(\frac{13}{4}\right)^{3/2} - 1\right]$$
Since $\left(\dfrac{13}{4}\right)^{3/2} = \dfrac{13\sqrt{13}}{8}$,
$$\boxed{L = \frac{a\,(13\sqrt{13} - 8)}{27}} \approx 1.440\,a$$

@s 3
**(a)** Linear equation with $P = \dfrac1x$, integrating factor $e^{\int dx/x} = x$:
$$\frac{d}{dx}(xy) = x^3 \;\Rightarrow\; xy = \frac{x^4}{4} + C \;\Rightarrow\; y = \frac{x^3}{4} + \frac{C}{x}$$

**(b)** *Clairaut's equation* is an equation of the form $y = px + f(p)$, $p = \dfrac{dy}{dx}$; its general solution is $y = cx + f(c)$.

Here $\sin(y - px) = p$ gives $y - px = \sin^{-1}p$, i.e. $y = px + \sin^{-1}p$, which is Clairaut's form with $f(p) = \sin^{-1}p$. Replacing $p$ by a constant $c$:
$$\boxed{y = cx + \sin^{-1}c}$$
(The singular solution follows from $x + \dfrac{1}{\sqrt{1-p^2}} = 0$.)

**(c)** Let $\omega = \sqrt\mu$. The auxiliary equation $m^2 + \mu = 0$ has roots $\pm i\omega$, so $x = A\cos\omega t + B\sin\omega t$ and $x' = \omega(-A\sin\omega t + B\cos\omega t)$.
At $t = \dfrac{\pi}{2\omega}$ we have $\omega t = \dfrac\pi2$:
$x' = -A\omega = 0 \Rightarrow A = 0$, and $x = B = a$. Hence
$$\boxed{x(t) = a\sin(\sqrt\mu\,t)}$$

@s 4
Shifting the origin to $(-2, 3)$ means $x = X - 2,\ y = Y + 3$. Substituting,
$$2(X-2)^2 + 4(X-2)(Y+3) + 5(Y+3)^2 - 4(X-2) - 22(Y+3) + 7 = 0$$
Collecting terms:

| Term | Contributions | Total |
|---|---|---|
| $X^2,\ XY,\ Y^2$ | unchanged | $2X^2 + 4XY + 5Y^2$ |
| $X$ | $-8 + 12 - 4$ | $0$ |
| $Y$ | $-8 + 30 - 22$ | $0$ |
| constant | $8 - 24 + 45 + 8 - 66 + 7$ | $-22$ |

$$\boxed{2X^2 + 4XY + 5Y^2 = 22}$$
The linear terms vanish, so $(-2, 3)$ is the centre of the conic.

@s 5
**(a)** The lines pass through $A(-3, -5, 7)$ and $B(-1, -1, -1)$ with direction ratios $(2, 3, -3)$ and $(4, 5, -1)$. They are coplanar if $\overrightarrow{AB} = (2, 4, -8)$ and the two directions are coplanar:
$$\begin{vmatrix}2 & 4 & -8\\ 2 & 3 & -3\\ 4 & 5 & -1\end{vmatrix} = 2(-3 + 15) - 4(-2 + 12) - 8(10 - 12) = 24 - 40 + 16 = 0$$
The determinant is zero, so the lines are **coplanar**.

**(b)** Every sphere through the given circle is $x^2 + y^2 + z^2 - 9 + \lambda(x + 3y + 4z - 2) = 0$. It passes through the origin if $-9 - 2\lambda = 0$, i.e. $\lambda = -\dfrac92$. Then
$$x^2 + y^2 + z^2 - \frac92(x + 3y + 4z) = 0$$
$$\boxed{2x^2 + 2y^2 + 2z^2 - 9x - 27y - 36z = 0}$$

@s 6
The cubic terms are $x^3 - x^2y - xy^2 + y^3 = (x-y)^2(x+y)$ and the quadratic terms are $x^2 - y^2 = (x-y)(x+y)$. Hence the curve is
$$(x+y)(x-y)^2 + (x+y)(x-y) = 1 \quad\Rightarrow\quad (x+y)(x-y)(x-y+1) = 1$$
Let $u = x - y$ and $v = x + y$, so the curve is $v\,u\,(u+1) = 1$. For a branch to go to infinity, either $v \to \infty$ (then $u(u+1) = 1/v \to 0$, so $u \to 0$ or $u \to -1$) or $u \to \infty$ (then $v = \dfrac{1}{u(u+1)} \to 0$).

Check by the standard method with $\phi_3 = (x-y)^2(x+y)$, $\phi_2 = x^2 - y^2$: the slopes are $m = 1$ (twice) and $m = -1$. For $m = -1$: $c = -\dfrac{\phi_2(-1)}{\phi_3'(-1)} = 0$. For the repeated root $m = 1$: $\tfrac{c^2}{2}\phi_3''(1) + c\,\phi_2'(1) = 0$ gives $2c^2 - 2c = 0$, so $c = 0$ or $c = 1$ (that is, $y = x$ and $y = x + 1$).

**Asymptotes:** $x + y = 0,\quad x - y = 0,\quad x - y + 1 = 0$.

@s 7
$y = x^3 - 3x^2$, so $y' = 3x^2 - 6x = 3x(x-2)$. The tangent is parallel to the $x$-axis when $y' = 0$: $x = 0$ or $x = 2$, giving the points $(0, 0)$ and $(2, -4)$.

$y'' = 6x - 6$. At $(0,0)$: $y'' = -6$. At $(2, -4)$: $y'' = 6$. Since $y' = 0$ at both points,
$$\rho = \frac{(1 + y'^2)^{3/2}}{|y''|} = \frac{1}{|y''|} = \frac16 \quad\text{at both points.}$$
$$\boxed{\rho = \tfrac16}$$
(The centre of curvature lies above the curve at $(2,-4)$, a minimum, and below it at $(0,0)$, a maximum.)

@s 8
Let $I(a) = \displaystyle\int_0^\infty\frac{\tan^{-1}(ax)}{x(1+x^2)}\,dx$, so $I(0) = 0$. Differentiating under the integral sign with respect to $a$:
$$I'(a) = \int_0^\infty\frac{1}{x(1+x^2)}\cdot\frac{x}{1 + a^2x^2}\,dx = \int_0^\infty\frac{dx}{(1+x^2)(1+a^2x^2)}$$
By partial fractions, $\dfrac{1}{(1+x^2)(1+a^2x^2)} = \dfrac{1}{1-a^2}\left[\dfrac{1}{1+x^2} - \dfrac{a^2}{1+a^2x^2}\right]$, so
$$I'(a) = \frac{1}{1-a^2}\left[\frac\pi2 - a^2\cdot\frac{\pi}{2a}\right] = \frac{\pi(1-a)}{2(1-a^2)} = \frac{\pi}{2(1+a)}$$
Integrating, $I(a) = \dfrac\pi2\ln(1+a) + C$, and $I(0) = 0$ gives $C = 0$. Therefore
$$\boxed{\int_0^\infty\frac{\tan^{-1}(ax)}{x(1+x^2)}\,dx = \frac\pi2\ln(1+a)}\quad(a \ge 0)$$

**OR.** Rotating about the $x$-axis, $y^2 = b^2\left(1 - \dfrac{x^2}{a^2}\right)$ and $x$ runs from $-a$ to $a$:
$$V = \pi\int_{-a}^{a}y^2\,dx = 2\pi b^2\int_0^a\left(1 - \frac{x^2}{a^2}\right)dx = 2\pi b^2\left[a - \frac a3\right] = \frac{4}{3}\pi ab^2$$
$$\boxed{V = \tfrac43\pi a b^2}$$
(Rotation about the $y$-axis gives $\tfrac43\pi a^2 b$; for $a = b = r$ both reduce to the sphere $\tfrac43\pi r^3$.)

@s 9
Area $A = \displaystyle\int_0^{\pi/2}\cos x\,dx = 1$.
$$\bar x = \frac1A\int_0^{\pi/2}x\cos x\,dx = \Big[x\sin x + \cos x\Big]_0^{\pi/2} = \frac\pi2 - 1$$
$$\bar y = \frac1A\int_0^{\pi/2}\tfrac12\cos^2x\,dx = \frac14\int_0^{\pi/2}(1 + \cos 2x)\,dx = \frac\pi8$$
$$\boxed{(\bar x, \bar y) = \left(\frac\pi2 - 1,\ \frac\pi8\right)\approx(0.571,\ 0.393)}$$

@s 10
Here $a = 9,\ 2h = 4\ (h = 2),\ b = 6$, and $h^2 - ab = 4 - 54 = -50 < 0$. The discriminant is negative, so the conic is an **ellipse** (the $3\times3$ determinant is non-zero, so it is non-degenerate; see the constant below).

**Centre.** Solve $\dfrac{\partial F}{\partial x} = 18x + 4y - 22 = 0$ and $\dfrac{\partial F}{\partial y} = 4x + 12y - 16 = 0$. From the second, $x = 4 - 3y$; then $72 - 54y + 4y = 22$ gives $y = 1$, $x = 1$. **Centre $(1, 1)$.**

Shift the origin to $(1,1)$ ($x = X + 1,\ y = Y + 1$). The new constant is $F(1,1) = 9 + 4 + 6 - 22 - 16 + 9 = -10$, so
$$9X^2 + 4XY + 6Y^2 = 10$$
**Axes.** Rotate to remove $XY$. The eigenvalues of $\begin{pmatrix}9 & 2\\ 2 & 6\end{pmatrix}$ satisfy $\lambda^2 - 15\lambda + 50 = 0$, so $\lambda = 5$ and $10$. In the principal axes
$$5u^2 + 10v^2 = 10 \quad\Rightarrow\quad \frac{u^2}{2} + \frac{v^2}{1} = 1$$
Semi-axes $\sqrt2$ and $1$, so
$$\boxed{\text{length of major axis} = 2\sqrt2,\qquad \text{length of minor axis} = 2}$$
The major axis lies along the eigenvector of $\lambda = 5$, i.e. along $y - 1 = -2(x - 1)$; the minor axis is along $y - 1 = \tfrac12(x - 1)$.

```figure caption="The ellipse 9x² + 4xy + 6y² − 22x − 16y + 9 = 0: centre (1, 1), semi-axes √2 and 1."
fig, ax = plt.subplots(figsize=(4.4, 3.4))
t = np.linspace(0, 2*np.pi, 400)
u = np.sqrt(2)*np.cos(t); v = np.sin(t)
e1 = np.array([1, -2])/np.sqrt(5); e2 = np.array([2, 1])/np.sqrt(5)
X = 1 + u*e1[0] + v*e2[0]; Y = 1 + u*e1[1] + v*e2[1]
ax.plot(X, Y, color=ACCENT, lw=2)
s = np.sqrt(2)
ax.plot([1 - s*e1[0], 1 + s*e1[0]], [1 - s*e1[1], 1 + s*e1[1]], color=INK, lw=1, ls='--')
ax.plot([1 - e2[0], 1 + e2[0]], [1 - e2[1], 1 + e2[1]], color=INK, lw=1, ls=':')
ax.plot([1], [1], 'o', color=INK, ms=4); ax.text(1.08, 0.8, 'C(1, 1)', fontsize=8)
ax.text(1 + s*e1[0] + 0.05, 1 + s*e1[1] - 0.25, 'major axis', fontsize=7)
ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
ax.set_aspect('equal'); ax.spines[['top', 'right']].set_visible(False)
```

@s 11
**Line 1:** point $A(3, 8, 3)$, direction $\mathbf d_1 = (3, -1, 1)$.

**Line 2** is the intersection of the planes $2x - 3y + 27 = 0$ (normal $(2,-3,0)$) and $2y - z + 20 = 0$ (normal $(0,2,-1)$). Its direction is
$$\mathbf d_2 = (2,-3,0)\times(0,2,-1) = (3, 2, 4)$$
A point on it: put $y = 9$, then $x = 0$ and $z = 38$, so $B(0, 9, 38)$.

**Common perpendicular direction:** $\mathbf n = \mathbf d_1\times\mathbf d_2 = (-6, -9, 9) \parallel (2, 3, -3)$, $|\mathbf n| = \sqrt{22}$. (Check: $\mathbf n\cdot\mathbf d_1 = 6 - 3 - 3 = 0$, $\mathbf n\cdot\mathbf d_2 = 6 + 6 - 12 = 0$.)

**Length.** $\overrightarrow{AB} = (-3, 1, 35)$ and $\overrightarrow{AB}\cdot\mathbf n = -6 + 3 - 105 = -108$:
$$\boxed{SD = \frac{|-108|}{\sqrt{22}} = \frac{54\sqrt{22}}{11}\approx 23.03 \text{ units}}$$

**Equation.** The shortest-distance line is the intersection of the plane through line 1 containing $\mathbf n$ and the plane through line 2 containing $\mathbf n$.

- Plane 1: normal $\mathbf d_1\times\mathbf n = (0, 11, 11)\parallel(0,1,1)$, through $A$: $(y - 8) + (z - 3) = 0$, i.e. $y + z = 11$.
- Plane 2: normal $\mathbf d_2\times\mathbf n = (-18, 17, 5)$, through $B$: $-18x + 17(y - 9) + 5(z - 38) = 0$, i.e. $18x - 17y - 5z + 343 = 0$.

$$\boxed{y + z - 11 = 0 = 18x - 17y - 5z + 343}$$
Verification: the feet of the common perpendicular are $\left(-\tfrac{90}{11}, \tfrac{129}{11}, -\tfrac{8}{11}\right)$ on line 1 and $(-18, -3, 14)$ on line 2; both satisfy both plane equations and are $\tfrac{54\sqrt{22}}{11}$ apart.

@s 12
A point $P(x,y,z)$ lies on the cylinder when its distance from the axis equals 2. The axis passes through $A(1,2,3)$ with direction $\mathbf d = (2,-3,6)$, $|\mathbf d|^2 = 49$. With $\mathbf r = \overrightarrow{AP}$, the squared distance from the axis is $|\mathbf r|^2 - \dfrac{(\mathbf r\cdot\mathbf d)^2}{|\mathbf d|^2}$, so
$$49\big[(x-1)^2 + (y-2)^2 + (z-3)^2\big] - \big[2(x-1) - 3(y-2) + 6(z-3)\big]^2 = 4\cdot 49$$
Expanding and simplifying:
$$\boxed{45x^2 + 40y^2 + 13z^2 + 12xy - 24xz + 36yz - 42x - 280y - 126z + 294 = 0}$$

**OR.** Vertex $V(1,1,1)$, axis direction $\mathbf d = (-1, 2, 3)$, $|\mathbf d|^2 = 14$, semi-vertical angle $30^\circ$. For a point $P$ on the cone, the angle between $\overrightarrow{VP}$ and the axis is $30^\circ$:
$$\big[\overrightarrow{VP}\cdot\mathbf d\big]^2 = \cos^2 30^\circ\cdot|\mathbf d|^2\cdot|\overrightarrow{VP}|^2 = \frac34\cdot14\,|\overrightarrow{VP}|^2$$
$$2\big[-(x-1) + 2(y-1) + 3(z-1)\big]^2 = 21\big[(x-1)^2 + (y-1)^2 + (z-1)^2\big]$$
Expanding:
$$\boxed{19x^2 + 13y^2 + 3z^2 + 8xy + 12xz - 24yz - 58x - 10y + 6z + 31 = 0}$$

@s 13
Divide by $y(\log y)^2$:
$$\frac{1}{y(\log y)^2}\frac{dy}{dx} + \frac{x}{\log y} = x$$
Put $v = \dfrac{1}{\log y}$. Then $\dfrac{dv}{dx} = -\dfrac{1}{y(\log y)^2}\dfrac{dy}{dx}$, so the equation becomes the linear equation
$$-\frac{dv}{dx} + xv = x \;\Rightarrow\; \frac{dv}{dx} - xv = -x$$
Integrating factor $e^{-x^2/2}$: $\dfrac{d}{dx}\left(ve^{-x^2/2}\right) = -xe^{-x^2/2}$, hence $ve^{-x^2/2} = e^{-x^2/2} + C$:
$$\boxed{\frac{1}{\log y} = 1 + Ce^{x^2/2}}$$

@s 14
Spring constant from Hooke's law: $k = \dfrac{F}{x} = \dfrac{6}{1.5} = 4\ \text{N/m}$. With $m = 1$ kg and $x(t)$ measured from equilibrium (positive to the right), Newton's law gives
$$m\,x'' = -kx \;\Rightarrow\; x'' + 4x = 0$$
Roots $m = \pm 2i$, so $x = A\cos 2t + B\sin 2t$. Initial conditions: $x(0) = 1 \Rightarrow A = 1$; released from rest, $x'(0) = 0 \Rightarrow 2B = 0 \Rightarrow B = 0$.
$$\boxed{x(t) = \cos 2t \ \text{metres}}$$
The motion is simple harmonic with amplitude 1 m, angular frequency $2$ rad/s and period $\pi$ s.

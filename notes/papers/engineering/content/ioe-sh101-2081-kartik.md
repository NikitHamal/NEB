---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH101-2081-Kartik.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 101
year_bs: 2081 Kartik
cal: BS
year_ad: 2024
stream: All programmes except B.Arch
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course, 2080 batch). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) Expand $y = \cosh x$ in powers of $x$ up to three non-zero terms in the expansion. [[2]]
(b) Find the pedal equation of the polar curve $r = a(1 + \cos\theta)$. [[2]]
(c) Evaluate $\displaystyle\lim_{x\to 0}x^x$. [[2]]

@q 2
(a) Evaluate $\displaystyle\int_0^a\dfrac{x^4}{\sqrt{a^2 - x^2}}\,dx$ using beta and gamma functions. [[2]]
(b) Find the position of the centroid of a semi-circular plate of radius $a$. [[2]]
(c) Find the area of the surface of revolution of the curve $y = x^3$, $0 \le x \le 2$, about the $x$-axis. [[2]]

@q 3
(a) Find the integrating factor (I.F.) of $x\dfrac{dy}{dx} = x^2\ln x - 2y$. [[2]]
(b) Solve the differential equation $p^2 + p - 6 = 0$, where $p = \dfrac{dy}{dx}$. [[2]]
(c) Solve $(D^2 - 5D + 6)y = e^x$. [[2]]

@q 4
Identify the conic $9x^2 + 4xy + 6y^2 - 22x - 16y + 9 = 0$. [[2]]

@q 5
(a) Find the angle between the line $\dfrac{x+1}{2} = \dfrac{y}{3} = \dfrac{z-1}{6}$ and the plane $3x + y + z = 7$. [[2]]
(b) Find the equation of the right circular cone whose vertex is the origin and whose axis is the line $\dfrac{x}{1} = \dfrac{y}{2} = \dfrac{z}{3}$, with semi-vertical angle $30^\circ$. [[2]]

@q 6
Find the asymptotes of the curve $(x^2 - y^2)(x + 2y + 1) + x + y + 1 = 0$. [[4]]

@q 7
Find the radius of curvature of the curve $\sqrt{x} + \sqrt{y} = \sqrt{a}$ at the point where it cuts the line $y = x$. [[4]]

@q 8
Evaluate, by using the rule of differentiation under the sign of integration, $\displaystyle\int_0^\infty\dfrac{\log(1 + a^2x^2)}{1 + b^2x^2}\,dx$. [[4]]
@or
Find the surface area of the solid formed by revolving the astroid $x^{2/3} + y^{2/3} = a^{2/3}$ about the $x$-axis. [[4]]

@q 9
Find the centroid of the region between the curves $y = x^2$ and $y = x + 2$. [[4]]

@q 10
Transform the equation $x^2 - y^2 = a^2$ into $xy = c^2$ by a suitable angle of rotation of the axes. [[4]]

@q 11
Find the centre and radius of the circle $x^2 + y^2 + z^2 - 8x + 4y + 8z - 45 = 0,\ x - 2y + 2z = 3$. [[4]]

@q 12
Show that the lines $\dfrac{x+1}{-3} = \dfrac{y-3}{2} = \dfrac{z+2}{1}$ and $\dfrac{x}{1} = \dfrac{y-7}{-3} = \dfrac{z+7}{2}$ are coplanar. Also find their point of intersection and the common plane. [[4]]
@or
Find the length and the equation of the shortest distance between the lines $\dfrac{x+3}{-4} = \dfrac{y-6}{6} = \dfrac{z}{2}$ and $\dfrac{x+2}{-4} = \dfrac{y}{1} = \dfrac{z-7}{1}$. [[4]]

@q 13
Solve $\dfrac{dy}{dx} + x\sin 2y = x^3\cos^2 y$. [[4]]

@q 14
In a series $RLC$ circuit with $R = 20\ \Omega$, $L = 1$ H, $C = 0.002$ F and a 12 V battery, both the charge and the current are initially zero. Find the charge and the current at any time $t$ in the circuit. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** $f(x) = \cosh x$: $f(0) = 1,\ f'(0) = \sinh 0 = 0,\ f''(0) = 1,\ f'''(0) = 0,\ f^{(4)}(0) = 1,\ f^{(5)}(0)=0,\ f^{(6)}(0)=1$. By Maclaurin's series
$$\cosh x = 1 + \frac{x^2}{2!} + \frac{x^4}{4!} + \cdots = 1 + \frac{x^2}{2} + \frac{x^4}{24} + \cdots$$
The first three non-zero terms are $1,\ \dfrac{x^2}{2},\ \dfrac{x^4}{24}$.

**(b)** $r = a(1 + \cos\theta)$, $\dfrac{dr}{d\theta} = -a\sin\theta$. Then
$$\frac1{p^2} = \frac1{r^2} + \frac{1}{r^4}\left(\frac{dr}{d\theta}\right)^2 = \frac{r^2 + a^2\sin^2\theta}{r^4}$$
Now $r^2 + a^2\sin^2\theta = a^2(1 + \cos\theta)^2 + a^2(1 - \cos^2\theta) = 2a^2(1 + \cos\theta) = 2ar$. Therefore $\dfrac1{p^2} = \dfrac{2ar}{r^4} = \dfrac{2a}{r^3}$:
$$\boxed{r^3 = 2a\,p^2}$$

**(c)** Let $y = x^x$, so $\ln y = x\ln x = \dfrac{\ln x}{1/x}$, a form $\dfrac{-\infty}{\infty}$. By L'Hospital's rule
$$\lim_{x\to0^+}\ln y = \lim_{x\to0^+}\frac{1/x}{-1/x^2} = \lim_{x\to0^+}(-x) = 0 \;\Rightarrow\; \lim_{x\to0}x^x = e^0 = \mathbf{1}$$

@s 2
**(a)** Put $x = a\sin\theta$, $dx = a\cos\theta\,d\theta$, $\sqrt{a^2 - x^2} = a\cos\theta$:
$$I = a^4\int_0^{\pi/2}\sin^4\theta\,d\theta = a^4\cdot\frac12B\!\left(\frac52, \frac12\right) = \frac{a^4}{2}\cdot\frac{\Gamma(5/2)\Gamma(1/2)}{\Gamma(3)}$$
With $\Gamma(5/2) = \dfrac{3\sqrt\pi}{4}$, $\Gamma(1/2) = \sqrt\pi$, $\Gamma(3) = 2$:
$$I = \frac{a^4}{2}\cdot\frac{3\pi/4}{2} = \boxed{\frac{3\pi a^4}{16}}$$

**(b)** Take the plate $x^2 + y^2 \le a^2$, $y \ge 0$. By symmetry $\bar x = 0$. Area $A = \dfrac{\pi a^2}{2}$ and
$$\bar y = \frac1A\int_{-a}^{a}\frac{y^2}{2}\,dx = \frac{2}{\pi a^2}\cdot\frac12\int_{-a}^{a}(a^2 - x^2)\,dx = \frac{1}{\pi a^2}\cdot\frac{4a^3}{3} = \frac{4a}{3\pi}$$
**Centroid:** on the axis of symmetry at a distance $\dfrac{4a}{3\pi}\approx 0.424a$ from the diameter.

**(c)** $y = x^3$, $y' = 3x^2$. The surface area is
$$S = 2\pi\int_0^2 y\sqrt{1 + y'^2}\,dx = 2\pi\int_0^2x^3\sqrt{1 + 9x^4}\,dx$$
Put $u = 1 + 9x^4$, $du = 36x^3dx$; $x = 0 \to u = 1$, $x = 2 \to u = 145$:
$$S = \frac{2\pi}{36}\cdot\frac23\Big[u^{3/2}\Big]_1^{145} = \boxed{\frac{\pi}{27}\left(145\sqrt{145} - 1\right)}\approx 203.04 \text{ square units}$$

@s 3
**(a)** In standard form $\dfrac{dy}{dx} + \dfrac2x y = x\ln x$, so
$$\text{I.F.} = e^{\int\frac2x dx} = e^{2\ln x} = \boxed{x^2}$$
(Then $\dfrac{d}{dx}(x^2y) = x^3\ln x$, which can be integrated by parts.)

**(b)** Factorise: $p^2 + p - 6 = (p - 2)(p + 3) = 0$, so $\dfrac{dy}{dx} = 2$ or $\dfrac{dy}{dx} = -3$. Integrating, $y - 2x = c$ or $y + 3x = c$:
$$\boxed{(y - 2x - c)(y + 3x - c) = 0}$$

**(c)** Auxiliary equation $m^2 - 5m + 6 = 0 \Rightarrow m = 2, 3$, so $y_c = C_1e^{2x} + C_2e^{3x}$. Particular integral (replace $D$ by $1$):
$$y_p = \frac{e^x}{1 - 5 + 6} = \frac{e^x}{2}$$
$$\boxed{y = C_1e^{2x} + C_2e^{3x} + \tfrac12e^x}$$

@s 4
For $ax^2 + 2hxy + by^2 + 2gx + 2fy + c = 0$ here $a = 9,\ h = 2,\ b = 6,\ g = -11,\ f = -8,\ c = 9$.
$$\Delta = \begin{vmatrix}9 & 2 & -11\\ 2 & 6 & -8\\ -11 & -8 & 9\end{vmatrix} = 9(54 - 64) - 2(18 - 88) - 11(-16 + 66) = -90 + 140 - 550 = -500 \ne 0$$
and $h^2 - ab = 4 - 54 = -50 < 0$. The conic is a (real, non-degenerate) **ellipse**, with centre $(1, 1)$ and equation $\dfrac{u^2}{2} + v^2 = 1$ in its principal axes (semi-axes $\sqrt2$ and $1$).

@s 5
**(a)** Direction of the line: $\mathbf d = (2, 3, 6)$, $|\mathbf d| = 7$. Normal of the plane: $\mathbf n = (3, 1, 1)$, $|\mathbf n| = \sqrt{11}$. The angle $\varphi$ between line and plane satisfies
$$\sin\varphi = \frac{|\mathbf d\cdot\mathbf n|}{|\mathbf d||\mathbf n|} = \frac{6 + 3 + 6}{7\sqrt{11}} = \frac{15}{7\sqrt{11}}\approx 0.646$$
$$\boxed{\varphi = \sin^{-1}\frac{15}{7\sqrt{11}}\approx 40.25^\circ}$$

**(b)** Axis direction $(1, 2, 3)$, $|\mathbf d|^2 = 14$. For a point $P(x,y,z)$ of the cone, the angle between $\overrightarrow{OP}$ and the axis is $30^\circ$:
$$(x + 2y + 3z)^2 = \frac34\cdot14\,(x^2 + y^2 + z^2) \;\Rightarrow\; 2(x + 2y + 3z)^2 = 21(x^2 + y^2 + z^2)$$
Expanding the left side, $2x^2 + 8y^2 + 18z^2 + 8xy + 24yz + 12zx$:
$$\boxed{19x^2 + 13y^2 + 3z^2 - 8xy - 24yz - 12zx = 0}$$

@s 6
Cubic terms $\phi_3 = (x^2 - y^2)(x + 2y) = (x-y)(x+y)(x+2y)$; quadratic terms $\phi_2 = x^2 - y^2$; linear $\phi_1 = x + y$; constant $1$. Slopes of the asymptotes from $\phi_3(1, m) = (1-m)(1+m)(1+2m) = 0$: $m = 1,\ -1,\ -\tfrac12$. All roots are simple, so $c = -\dfrac{\phi_2(1, m)}{\phi_3'(1, m)}$ with $\phi_3'(m) = -2m(1+2m) + 2(1 - m^2)$ and $\phi_2(1,m) = 1 - m^2$:

| $m$ | $\phi_2(1,m)$ | $\phi_3'(m)$ | $c$ | Asymptote |
|---|---|---|---|---|
| $1$ | $0$ | $-6$ | $0$ | $y = x$ |
| $-1$ | $0$ | $2$ | $0$ | $y = -x$ |
| $-\tfrac12$ | $\tfrac34$ | $\tfrac32$ | $-\tfrac12$ | $y = -\tfrac12x - \tfrac12$ |

**Asymptotes:** $x - y = 0,\quad x + y = 0,\quad x + 2y + 1 = 0$.

Check: since the curve is $(x-y)(x+y)(x+2y+1) = -(x+y+1)$, along a branch with $x + 2y + 1\to0$ the left side stays finite, and along $x - y \to 0$ we need $x - y = -\dfrac{x+y+1}{(x+y)(x+2y+1)}\to0$, as required.

@s 7
Where $y = x$ meets the curve: $2\sqrt x = \sqrt a$, so $x = y = \dfrac a4$.

Differentiating $x^{1/2} + y^{1/2} = a^{1/2}$: $\dfrac{1}{2\sqrt x} + \dfrac{y'}{2\sqrt y} = 0$, so $y' = -\sqrt{y/x}$, which is $-1$ at $\left(\tfrac a4, \tfrac a4\right)$. Differentiating again,
$$y'' = -\frac12\left[\frac{y'}{\sqrt{x}\sqrt{y}} - \frac{\sqrt y}{x^{3/2}}\right]$$
At the point $\sqrt x\sqrt y = \dfrac a4$ and $\dfrac{\sqrt y}{x^{3/2}} = \dfrac1x = \dfrac4a$, so $y'' = -\dfrac12\left[-\dfrac4a - \dfrac4a\right] = \dfrac4a$.
$$\rho = \frac{(1 + y'^2)^{3/2}}{|y''|} = \frac{2^{3/2}}{4/a} = \boxed{\frac{a}{\sqrt2}}$$

@s 8
Let $I(a) = \displaystyle\int_0^\infty\frac{\log(1 + a^2x^2)}{1 + b^2x^2}\,dx$, so $I(0) = 0$. Differentiating with respect to $a$,
$$I'(a) = \int_0^\infty\frac{2ax^2}{(1 + a^2x^2)(1 + b^2x^2)}\,dx$$
Since $\dfrac{1}{1+a^2x^2} - \dfrac{1}{1+b^2x^2} = \dfrac{(b^2 - a^2)x^2}{(1+a^2x^2)(1+b^2x^2)}$,
$$I'(a) = \frac{2a}{b^2 - a^2}\int_0^\infty\left[\frac{1}{1+a^2x^2} - \frac{1}{1+b^2x^2}\right]dx = \frac{2a}{b^2 - a^2}\left[\frac{\pi}{2a} - \frac{\pi}{2b}\right] = \frac{\pi}{b(a+b)}$$
Integrating, $I(a) = \dfrac\pi b\ln(a + b) + C$; $I(0) = 0$ gives $C = -\dfrac\pi b\ln b$:
$$\boxed{I = \frac\pi b\ln\frac{a+b}{b} = \frac{\pi}{b}\ln\left(1 + \frac ab\right)}\quad(a, b > 0)$$

**OR.** Use the parametric form $x = a\cos^3t,\ y = a\sin^3t$. Then $\dfrac{dx}{dt} = -3a\cos^2t\sin t$, $\dfrac{dy}{dt} = 3a\sin^2t\cos t$ and $ds = \sqrt{x'^2 + y'^2}\,dt = 3a\sin t\cos t\,dt$ (for $0\le t\le\frac\pi2$). The upper half ($y\ge0$) is traced by $t \in [0, \pi]$, equivalent to twice the quadrant $0\le t\le\frac\pi2$:
$$S = 2\times 2\pi\int_0^{\pi/2}y\,ds = 4\pi\int_0^{\pi/2}a\sin^3t\cdot3a\sin t\cos t\,dt = 12\pi a^2\int_0^{\pi/2}\sin^4t\cos t\,dt = 12\pi a^2\cdot\frac15$$
$$\boxed{S = \frac{12\pi a^2}{5}}$$

@s 9
The curves meet where $x^2 = x + 2$, i.e. $(x-2)(x+1) = 0$, at $x = -1$ and $x = 2$. Between them the line lies above the parabola.

Area: $A = \displaystyle\int_{-1}^{2}(x + 2 - x^2)\,dx = \left[\frac{x^2}{2} + 2x - \frac{x^3}{3}\right]_{-1}^{2} = \frac{10}{3} + \frac76 = \frac92$.

$$\bar x = \frac1A\int_{-1}^{2}x(x + 2 - x^2)\,dx = \frac29\left[\frac{x^3}{3} + x^2 - \frac{x^4}{4}\right]_{-1}^{2} = \frac29\cdot\frac94 = \frac12$$
$$\bar y = \frac1A\int_{-1}^{2}\frac12\left[(x+2)^2 - x^4\right]dx = \frac19\left[\frac{(x+2)^3}{3} - \frac{x^5}{5}\right]_{-1}^{2} = \frac19\left[\left(\frac{64}{3} - \frac{32}{5}\right) - \left(\frac13 + \frac15\right)\right] = \frac19\cdot\frac{72}{5} = \frac85$$
$$\boxed{(\bar x, \bar y) = \left(\tfrac12, \tfrac85\right)}$$

```figure caption="The region between y = x² and y = x + 2, with its centroid (1/2, 8/5)."
fig, ax = plt.subplots(figsize=(4.2, 3.0))
x = np.linspace(-1.4, 2.4, 300)
xs = np.linspace(-1, 2, 200)
ax.fill_between(xs, xs**2, xs + 2, color=ACCENT, alpha=0.18)
ax.plot(x, x**2, color=ACCENT, lw=2); ax.plot(x, x + 2, color=INK, lw=1.6)
ax.plot([0.5], [1.6], 'o', color=INK, ms=5); ax.text(0.62, 1.45, '(1/2, 8/5)', fontsize=8)
ax.plot([-1, 2], [1, 4], 'o', color=INK, ms=3)
ax.text(1.6, 2.3, 'y = x²', fontsize=8); ax.text(-1.3, 0.35, 'y = x + 2', fontsize=8)
ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
ax.set_xlim(-1.5, 2.5); ax.set_ylim(-0.3, 4.5); ax.spines[['top', 'right']].set_visible(False)
```

@s 10
Rotate the axes through an angle $\theta$: $x = X\cos\theta - Y\sin\theta,\ y = X\sin\theta + Y\cos\theta$. Then
$$x^2 - y^2 = (X^2 - Y^2)\cos2\theta - 2XY\sin2\theta$$
To remove $X^2 - Y^2$ we need $\cos2\theta = 0$, so $\theta = \pm\dfrac\pi4$. Take $\theta = -\dfrac\pi4$ (axes turned $45^\circ$ clockwise), for which $\sin2\theta = -1$, i.e. $x = \dfrac{X + Y}{\sqrt2},\ y = \dfrac{Y - X}{\sqrt2}$. Then
$$x^2 - y^2 = \frac{(X+Y)^2 - (Y-X)^2}{2} = 2XY = a^2$$
$$\boxed{XY = \frac{a^2}{2} = c^2,\qquad c^2 = \frac{a^2}{2}}$$
So the rectangular hyperbola $x^2 - y^2 = a^2$ becomes $XY = c^2$ with $c = a/\sqrt2$ after rotating the axes through $-45^\circ$.

@s 11
The sphere is $(x-4)^2 + (y+2)^2 + (z+4)^2 = 16 + 4 + 16 + 45 = 81$: centre $C_0(4, -2, -4)$, radius $R = 9$. (The last line of the question is partly cut off in the scan and is read as the plane $x - 2y + 2z = 3$.)

Distance of $C_0$ from the plane $x - 2y + 2z - 3 = 0$:
$$d = \frac{|4 + 4 - 8 - 3|}{\sqrt{1 + 4 + 4}} = \frac33 = 1$$
**Radius of the circle:** $r = \sqrt{R^2 - d^2} = \sqrt{81 - 1} = \sqrt{80} = 4\sqrt5\approx 8.94$.

**Centre of the circle** is the foot of the perpendicular from $C_0$ on the plane, i.e. $C_0 + \lambda(1, -2, 2)$ lying on the plane: $(4 + \lambda) - 2(-2 - 2\lambda) + 2(-4 + 2\lambda) = 3 \Rightarrow$ $4 + \lambda + 4 + 4\lambda - 8 + 4\lambda = 9\lambda = 3$, so $\lambda = \tfrac13$:
$$\boxed{\text{centre} = \left(\frac{13}{3}, -\frac83, -\frac{10}{3}\right),\qquad \text{radius} = 4\sqrt5}$$

@s 12
Line 1 passes through $A(-1, 3, -2)$ with direction $(-3, 2, 1)$; line 2 through $B(0, 7, -7)$ with direction $(1, -3, 2)$. $\overrightarrow{AB} = (1, 4, -5)$.
$$\begin{vmatrix}1 & 4 & -5\\ -3 & 2 & 1\\ 1 & -3 & 2\end{vmatrix} = 1(4 + 3) - 4(-6 - 1) - 5(9 - 2) = 7 + 28 - 35 = 0$$
so the lines are **coplanar**.

**Point of intersection.** A point of line 1 is $(-1 - 3s,\ 3 + 2s,\ -2 + s)$ and of line 2 is $(t,\ 7 - 3t,\ -7 + 2t)$. Equating: $-1 - 3s = t$, $3 + 2s = 7 - 3t$, $-2 + s = -7 + 2t$. From the first and third, $s - 2 = -7 - 2 - 6s \Rightarrow 7s = -7$, so $s = -1,\ t = 2$ (the second equation: $1 = 1$ ✓). The point is $\boxed{(2, 1, -3)}$.

**Common plane.** Its normal is $(-3, 2, 1)\times(1, -3, 2) = (7, 7, 7)\parallel(1,1,1)$. Through $(2, 1, -3)$: $(x - 2) + (y - 1) + (z + 3) = 0$:
$$\boxed{x + y + z = 0}$$

**OR.** Line 1: $A(-3, 6, 0)$, $\mathbf d_1 = (-4, 6, 2)\parallel(-2, 3, 1)$. Line 2: $B(-2, 0, 7)$, $\mathbf d_2 = (-4, 1, 1)$. $\overrightarrow{AB} = (1, -6, 7)$.
$$\mathbf n = (-2, 3, 1)\times(-4, 1, 1) = (2, -2, 10)\parallel(1, -1, 5),\qquad |\mathbf n| = \sqrt{27} = 3\sqrt3$$
$$\overrightarrow{AB}\cdot\mathbf n = 1 + 6 + 35 = 42 \quad\Rightarrow\quad \boxed{SD = \frac{42}{3\sqrt3} = \frac{14}{\sqrt3} = \frac{14\sqrt3}{3}\approx 8.08\text{ units}}$$
**Equation.** Plane through line 1 containing $\mathbf n$: normal $(-2,3,1)\times(1,-1,5) = (16, 11, -1)$, through $A$: $16(x + 3) + 11(y - 6) - z = 0$, i.e. $16x + 11y - z - 18 = 0$. Plane through line 2 containing $\mathbf n$: normal $(-4,1,1)\times(1,-1,5) = (6, 21, 3)\parallel(2, 7, 1)$, through $B$: $2(x + 2) + 7y + (z - 7) = 0$, i.e. $2x + 7y + z - 3 = 0$.
$$\boxed{16x + 11y - z - 18 = 0 = 2x + 7y + z - 3}$$
(The feet of the common perpendicular are $\left(\tfrac23, \tfrac12, -\tfrac{11}{6}\right)$ and $\left(\tfrac{20}{9}, -\tfrac{19}{18}, \tfrac{107}{18}\right)$; both satisfy both planes.)

@s 13
Divide by $\cos^2y$: $\sec^2y\dfrac{dy}{dx} + 2x\tan y = x^3$ (using $\sin2y = 2\sin y\cos y$). Let $v = \tan y$, so $\dfrac{dv}{dx} = \sec^2y\dfrac{dy}{dx}$:
$$\frac{dv}{dx} + 2xv = x^3,\qquad \text{I.F.} = e^{x^2}$$
$$\frac{d}{dx}\left(ve^{x^2}\right) = x^3e^{x^2} \;\Rightarrow\; ve^{x^2} = \int x^3e^{x^2}dx$$
With $t = x^2$: $\int x^3e^{x^2}dx = \tfrac12\int te^t\,dt = \tfrac12(t - 1)e^t$. Therefore
$$\boxed{\tan y = \frac{x^2 - 1}{2} + Ce^{-x^2}}$$

@s 14
Kirchhoff's voltage law for the series circuit: $L\dfrac{d^2q}{dt^2} + R\dfrac{dq}{dt} + \dfrac qC = E$, with $L = 1$, $R = 20$, $\dfrac1C = 500$, $E = 12$:
$$q'' + 20q' + 500q = 12$$
Auxiliary equation $m^2 + 20m + 500 = 0$: $m = -10 \pm 20i$, so $q_c = e^{-10t}(A\cos20t + B\sin20t)$. A particular solution is the steady charge $q_p = \dfrac{12}{500} = 0.024$ C. So
$$q = 0.024 + e^{-10t}(A\cos20t + B\sin20t)$$
$q(0) = 0 \Rightarrow A = -0.024$. Differentiating, $q' = e^{-10t}\left[(-10A + 20B)\cos20t + (-10B - 20A)\sin20t\right]$, and $q'(0) = i(0) = 0 \Rightarrow -10A + 20B = 0 \Rightarrow B = \dfrac A2 = -0.012$.
$$\boxed{q(t) = 0.024 - e^{-10t}\left(0.024\cos20t + 0.012\sin20t\right)\ \text{coulomb}}$$
With $-10B - 20A = 0.12 + 0.48 = 0.6$:
$$\boxed{i(t) = \frac{dq}{dt} = 0.6\,e^{-10t}\sin20t\ \text{ampere}}$$
The current is a decaying oscillation (underdamped, $R^2 < 4L/C$), and the charge settles at $CE = 0.024$ C.

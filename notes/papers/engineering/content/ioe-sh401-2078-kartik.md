---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH401-2078-Kartik.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 401
year_bs: 2078 Kartik
cal: BS
year_ad: 2021
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 401). Pass marks 32. All questions carry equal marks (5 each).
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
State Leibnitz's theorem. If $y^{1/m} + y^{-1/m} = 2x$, prove that $(x^2 - 1)y_2 + xy_1 - m^2y = 0$, and hence show that $(x^2 - 1)y_{n+2} + (2n+1)xy_{n+1} + (n^2 - m^2)y_n = 0$. [[5]]

@q 2
Apply Maclaurin's series to find the expansion of $\dfrac{e^x}{1 + e^x}$ as far as the term in $x^3$ and hence find the expansion of $\log(1 + e^x)$. [[5]]

@q 3
State L'Hospital rule. Evaluate $\displaystyle\lim_{x\to0}\left(\frac{\sin x}{x}\right)^{1/x^2}$. [[5]]

@q 4
Find the asymptotes of the curve of $x^2(x - y)^2 - a^2(x^2 + y^2) = 0$. [[5]]

@q 5
Define the radius of curvature, obtain the radius of curvature for the curve at the origin $x^3 + y^3 = 3axy$. [[5]]

@q 6
Prove that: $\displaystyle\int_0^\pi\frac{x\tan x}{\sec x + \tan x}\,dx = \frac\pi2(\pi - 2)$. [[5]]

@q 7
Apply the method of differentiation under integral sign to prove: $\displaystyle\int_0^\pi\frac{dx}{(a + b\cos x)^2} = \frac{\pi a}{(a^2 - b^2)^{3/2}}$. [[5]]

@q 8
State Beta and Gamma function. Use them to evaluate: $\displaystyle\int_0^1x^6\sqrt{1 - x^2}\,dx$. [[5]]

@q 9
Define the term quadrature. Find the area bounded by the curve $r = a(1 - \cos\theta)$.

**OR**

Find the volume of the solid formed by revolution of cycloid $x = a(\theta + \sin\theta)$, $y = a(1 + \cos\theta)$ about $x$-axis. [[5]]

@q 10
Solve the differential equations: $(x + y + 1)\,dx + (y - x)\,dy = 0$. [[5]]

@q 11
Find the general solution of the differential equation: $e^y - p^3 - p = 0$ where $p = \dfrac{dy}{dx}$. [[5]]

@q 12
Solve the differential equation: $(D^2 + 2D + 1)y = e^x + x^2$. [[5]]

@q 13
Solve: $(x^2D^2 + xD - 1)y = x^2$.

**OR**

A radioactive material has an initial mass $100$ mg. After $2$ years, it is left to $80$ mg. Find the amount of material at any time $t$. [[5]]

@q 14
Through what angle the axes be rotated to remove the term containing $xy$ in $11x^2 + 4xy + 14y^2 - 5 = 0$. [[5]]

@q 15
Define hyperbola as a locus of a point and deduce the equation of hyperbola in standard form. [[5]]

@q 16
Find the centre, length of axes, and eccentricity of the following conic: $3x^2 + 8xy - 3y^2 - 20y - 40x + 50 = 0$. [[5]]
<!-- SOLUTIONS -->

@s 1
**Leibnitz's theorem.** If $u$ and $v$ possess derivatives of every order up to $n$, then

$$\boxed{(uv)_n = u_nv + {}^nC_1u_{n-1}v_1 + {}^nC_2u_{n-2}v_2 + \cdots + uv_n}$$

**First relation.** Put $t = y^{1/m}$: $t + \dfrac1t = 2x\Rightarrow t^2 - 2xt + 1 = 0\Rightarrow t = x\pm\sqrt{x^2 - 1}$. Taking $+$ (the other sign only changes $m\to-m$): $y = \left(x + \sqrt{x^2 - 1}\right)^m$.

$$\begin{gathered}y_1 = m\left(x + \sqrt{x^2-1}\right)^{m-1}\left(1 + \frac{x}{\sqrt{x^2-1}}\right) = \frac{m\left(x + \sqrt{x^2-1}\right)^m}{\sqrt{x^2 - 1}}\ \Longrightarrow\ \sqrt{x^2-1}\;y_1 = my\end{gathered}$$

Differentiate again: $\sqrt{x^2-1}\,y_2 + \dfrac{x}{\sqrt{x^2-1}}y_1 = my_1$. Multiply by $\sqrt{x^2-1}$:

$$\begin{gathered}(x^2-1)y_2 + xy_1 = m\sqrt{x^2-1}\,y_1 = m^2y\end{gathered}$$

$$\begin{gathered}\boxed{(x^2-1)y_2 + xy_1 - m^2y = 0} \\ (1)\end{gathered}$$

**$n$th derivative.** Differentiate (1) $n$ times by Leibnitz's theorem:

$$\big[(x^2-1)y_{n+2} + 2nxy_{n+1} + n(n-1)y_n\big] + \big[xy_{n+1} + ny_n\big] - m^2y_n = 0$$

$$\begin{gathered}\boxed{(x^2-1)y_{n+2} + (2n+1)xy_{n+1} + (n^2 - m^2)y_n = 0} \\ \blacksquare\end{gathered}$$

@s 2
Let $f(x) = \dfrac{e^x}{1 + e^x} = 1 - \dfrac{1}{1+e^x}$; then $f(0) = \dfrac12$. Using $f' = f(1 - f)$ (since $f' = \dfrac{e^x}{(1+e^x)^2}$):

- $f' = f - f^2\Rightarrow f'(0) = \dfrac12 - \dfrac14 = \dfrac14$
- $f'' = f'(1 - 2f)\Rightarrow f''(0) = \dfrac14(1 - 1) = 0$
- $f''' = f''(1 - 2f) - 2f'^2\Rightarrow f'''(0) = 0 - 2\cdot\dfrac1{16} = -\dfrac18$

Maclaurin: $f(x) = f(0) + xf'(0) + \dfrac{x^2}{2!}f''(0) + \dfrac{x^3}{3!}f'''(0) + \cdots$

$$\boxed{\frac{e^x}{1 + e^x} = \frac12 + \frac x4 - \frac{x^3}{48} + \cdots}$$

**Expansion of $\log(1 + e^x)$.** Since $\dfrac{d}{dx}\log(1 + e^x) = \dfrac{e^x}{1 + e^x}$, integrate the series term by term; the constant is $\log(1 + e^0) = \log2$:

$$\boxed{\log(1 + e^x) = \log2 + \frac x2 + \frac{x^2}{8} - \frac{x^4}{192} + \cdots}$$

(verified with sympy.)

@s 3
**L'Hospital's rule.** If $f(x)\to0$ and $g(x)\to0$ (or both $\to\infty$) as $x\to a$ and $\displaystyle\lim\frac{f'(x)}{g'(x)}$ exists, then $\displaystyle\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)}$.

The limit is of the form $1^\infty$. With $L = \left(\dfrac{\sin x}{x}\right)^{1/x^2}$, $\log L = \dfrac{\log\sin x - \log x}{x^2}$ ($\tfrac00$):

$$\begin{gathered}\lim_{x\to0}\frac{\cot x - \frac1x}{2x} = \lim_{x\to0}\frac{x\cos x - \sin x}{2x^2\sin x}\overset{\text{L'H}}{=}\lim_{x\to0}\frac{-x\sin x}{4x\sin x + 2x^2\cos x} = \lim_{x\to0}\frac{-\sin x}{4\sin x + 2x\cos x}\end{gathered}$$

$$\begin{gathered}\overset{\text{L'H}}{=}\lim_{x\to0}\frac{-\cos x}{6\cos x - 2x\sin x} = -\frac16\end{gathered}$$

$$\boxed{\lim_{x\to0}\left(\frac{\sin x}{x}\right)^{1/x^2} = e^{-1/6}}$$

@s 4
Expand: $x^2(x - y)^2 - a^2(x^2 + y^2) = 0$, i.e. $\phi_4 = x^2(x-y)^2$, $\phi_3 = 0$, $\phi_2 = -a^2(x^2 + y^2)$. Arranging in powers of $y$:

$$(x^2 - a^2)\,y^2 - 2x^3\,y + x^4 - a^2x^2 = 0$$

The coefficients of $y^4$ and $y^3$ are zero.

**Asymptotes parallel to the $y$-axis.** Equate the coefficient of the highest power of $y$ to zero: $x^2 - a^2 = 0$:

$$\begin{gathered}x = a \\ x = -a\end{gathered}$$

**Oblique asymptotes** ($y = mx + c$). $\phi_4(1, m) = (1 - m)^2 = 0\Rightarrow m = 1$ (double). Then $\dfrac{c^2}{2!}\phi_4''(m) + c\,\phi_3'(m) + \phi_2(m) = 0$ with $\phi_4'' = 2$, $\phi_3' = 0$, $\phi_2(1,1) = -2a^2$:

$$\begin{gathered}c^2 - 2a^2 = 0\ \Longrightarrow\ c = \pm\sqrt2\,a\end{gathered}$$

$$\begin{gathered}\boxed{x = a,\quad x = -a,\quad y = x + \sqrt2\,a,\quad y = x - \sqrt2\,a}\end{gathered}$$

*Check.* Solving the quadratic in $y$: $y = \dfrac{x^3\pm x\sqrt{2a^2x^2 - a^4}}{x^2 - a^2}$. As $x\to\infty$, $y\approx x\pm\sqrt2a$; as $x\to\pm a$, $y\to\infty$. ✓

```figure caption="Question 4: the curve x^2 (x - y)^2 = a^2 (x^2 + y^2) (a = 1) with its four asymptotes x = +-a and y = x +- sqrt(2) a."
X,Y=np.meshgrid(np.linspace(-5,5,1000),np.linspace(-5,5,1000))
Z=X**2*(X-Y)**2-(X**2+Y**2)
fig,ax=plt.subplots(figsize=(3.8,3.8))
ax.contour(X,Y,Z,[0],colors='#1d6fb8',linewidths=1.6)
xs=np.array([-5,5])
for c in (np.sqrt(2),-np.sqrt(2)): ax.plot(xs,xs+c,'--',color='#d9534f',lw=.8)
for xv in (1,-1): ax.axvline(xv,color='#d9534f',lw=.8,ls='--')
ax.axhline(0,color='#14181f',lw=.5); ax.axvline(0,color='#14181f',lw=.5)
ax.set_xlim(-5,5); ax.set_ylim(-5,5); ax.set_aspect('equal'); ax.axis('off')
```

@s 5
**Radius of curvature.** The radius of curvature at a point $P$ of a curve is the radius of the circle (the *circle of curvature*) that touches the curve at $P$ and has the same curvature there:

$$\begin{gathered}\rho = \frac1\kappa = \frac{(1 + y_1^2)^{3/2}}{y_2}\end{gathered}$$

(for a curve $y = f(x)$; $\kappa = \dfrac{d\psi}{ds}$ is the curvature).

**At the origin of $x^3 + y^3 = 3axy$ (folium of Descartes).** The lowest-degree terms are $3axy = 0$, so the tangents at the origin are $x = 0$ and $y = 0$ (a node, two branches). Use Newton's formula: if the $x$-axis is the tangent at the origin, then $\rho = \displaystyle\lim_{x\to0}\frac{x^2}{2y}$.

Near the origin along the branch tangent to the $x$-axis, $y$ is small and $y^3$ is negligible compared with $x^3$ and $xy$; the equation gives $3axy\approx x^3$, i.e. $y\approx\dfrac{x^2}{3a}$. Hence

$$\begin{gathered}\rho = \lim_{x\to0}\frac{x^2}{2y} = \lim_{x\to0}\frac{x^2}{2\cdot x^2/(3a)} = \frac{3a}{2}\end{gathered}$$

For the other branch (tangent the $y$-axis) interchange $x$ and $y$ (the curve is symmetric in $x$ and $y$): $\rho = \dfrac{y^2}{2x} = \dfrac{3a}2$ again.

$$\boxed{\rho = \frac{3a}{2}\ \text{ at the origin (for both branches)}}$$

@s 6
Note $\dfrac{\tan x}{\sec x + \tan x} = \dfrac{\sin x}{1 + \sin x}$. Let $I = \displaystyle\int_0^\pi\frac{x\sin x}{1 + \sin x}\,dx$. By $\displaystyle\int_0^af(x)dx = \int_0^af(a - x)dx$:

$$I = \int_0^\pi\frac{(\pi - x)\sin x}{1 + \sin x}\,dx$$

Adding:

$$\begin{gathered}2I = \pi\int_0^\pi\frac{\sin x}{1 + \sin x}\,dx = \pi\int_0^\pi\left(1 - \frac{1}{1 + \sin x}\right)dx\end{gathered}$$

Now $\dfrac{1}{1 + \sin x} = \dfrac{1 - \sin x}{\cos^2x} = \sec^2x - \sec x\tan x$, with antiderivative $\tan x - \sec x = -\dfrac{\cos x}{1 + \sin x}$ (continuous on $[0,\pi]$):

$$\begin{gathered}\int_0^\pi\frac{dx}{1 + \sin x} = \left[-\frac{\cos x}{1 + \sin x}\right]_0^\pi = 1 - (-1) = 2\end{gathered}$$

$$\begin{gathered}2I = \pi(\pi - 2)\ \Longrightarrow\ \boxed{I = \frac\pi2(\pi - 2)} \\ \blacksquare\end{gathered}$$

@s 7
*Reading note:* the scan shows a minus sign before the right-hand side, but the integrand is positive, so the value is $+\dfrac{\pi a}{(a^2 - b^2)^{3/2}}$ ($a > |b|$); the proof below gives the positive sign.

**Step 1.** Let $I(a) = \displaystyle\int_0^\pi\frac{dx}{a + b\cos x}$. With $t = \tan\dfrac x2$:

$$\begin{gathered}I(a) = \int_0^\infty\frac{2\,dt}{(a + b) + (a - b)t^2} = \frac{2}{\sqrt{a^2 - b^2}}\left[\tan^{-1}\left(t\sqrt{\tfrac{a-b}{a+b}}\right)\right]_0^\infty = \frac{\pi}{\sqrt{a^2 - b^2}}\end{gathered}$$

**Step 2.** Differentiate both sides with respect to $a$ (the limits $0,\pi$ do not depend on $a$), by the rule of differentiation under the integral sign:

$$\begin{gathered}\int_0^\pi\frac{-1}{(a + b\cos x)^2}\,dx = \pi\cdot\left(-\frac12\right)(a^2 - b^2)^{-3/2}(2a) = -\frac{\pi a}{(a^2 - b^2)^{3/2}}\end{gathered}$$

$$\begin{gathered}\boxed{\int_0^\pi\frac{dx}{(a + b\cos x)^2} = \frac{\pi a}{(a^2 - b^2)^{3/2}}} \\ \blacksquare\end{gathered}$$

@s 8
**Definitions.** $\Gamma(n) = \displaystyle\int_0^\infty e^{-x}x^{n-1}dx$ $(n>0)$, $B(m,n) = \displaystyle\int_0^1x^{m-1}(1-x)^{n-1}dx$ $(m,n>0)$, and $B(m,n) = \dfrac{\Gamma(m)\Gamma(n)}{\Gamma(m+n)}$.

**Evaluation.** Put $x^2 = t$, $x = t^{1/2}$, $dx = \tfrac12t^{-1/2}dt$:

$$\begin{gathered}\int_0^1x^6\sqrt{1 - x^2}\,dx = \frac12\int_0^1t^{3}\,t^{-1/2}(1-t)^{1/2}\,dt = \frac12\int_0^1t^{5/2}(1 - t)^{1/2}dt = \frac12B\left(\frac72,\frac32\right)\end{gathered}$$

$$\begin{gathered}B\left(\tfrac72,\tfrac32\right) = \frac{\Gamma(\frac72)\Gamma(\frac32)}{\Gamma(5)} = \frac{\frac{15}{8}\sqrt\pi\cdot\frac12\sqrt\pi}{24} = \frac{15\pi/16}{24} = \frac{5\pi}{128}\end{gathered}$$

$$\begin{gathered}\boxed{\int_0^1x^6\sqrt{1-x^2}\,dx = \frac12\cdot\frac{5\pi}{128} = \frac{5\pi}{256}}\end{gathered}$$

@s 9
**Quadrature** is the process of finding the area bounded by a plane curve (with the ordinates or radius vectors and the axis): the area is "squared", i.e. converted into the side of an equal square. For a polar curve $A = \dfrac12\displaystyle\int r^2\,d\theta$.

**Main question (area of the cardioid $r = a(1 - \cos\theta)$).** The curve is symmetric about the initial line; the upper half is $\theta:0\to\pi$:

$$\begin{gathered}A = 2\cdot\frac12\int_0^\pi a^2(1 - \cos\theta)^2\,d\theta = a^2\int_0^\pi4\sin^4\frac\theta2\,d\theta = 8a^2\int_0^{\pi/2}\sin^4u\,du\ \ (\theta = 2u)\end{gathered}$$

$$\begin{gathered}\boxed{A = 8a^2\cdot\frac{3\pi}{16} = \frac{3\pi a^2}{2}}\end{gathered}$$

```figure caption="Question 9: the cardioid r = a(1 - cos theta) (a = 1); area 3 pi a^2 / 2."
t=np.linspace(0,2*np.pi,400); r=1-np.cos(t)
fig,ax=plt.subplots(figsize=(3.8,2.8))
ax.fill(r*np.cos(t),r*np.sin(t),color='#dbe8f6',alpha=.8); ax.plot(r*np.cos(t),r*np.sin(t),color='#1d6fb8',lw=1.8)
ax.axhline(0,color='#14181f',lw=.6); ax.plot([0],[0],'o',color='#14181f',ms=3); ax.text(0.1,0.1,'O',fontsize=8)
ax.set_aspect('equal'); ax.axis('off')
```

**OR (volume of the solid generated by the cycloid $x = a(\theta + \sin\theta)$, $y = a(1 + \cos\theta)$ about the $x$-axis).** One arch runs from $\theta = -\pi$ ($x = -\pi a$) to $\theta = \pi$ ($x = \pi a$), with $dx = a(1 + \cos\theta)\,d\theta$:

$$\begin{gathered}V = \pi\int y^2\,dx = \pi\int_{-\pi}^\pi a^2(1 + \cos\theta)^2\cdot a(1 + \cos\theta)\,d\theta = \pi a^3\int_{-\pi}^\pi(1 + \cos\theta)^3\,d\theta\end{gathered}$$

With $1 + \cos\theta = 2\cos^2\dfrac\theta2$ and $\theta = 2u$:

$$\begin{gathered}V = \pi a^3\cdot2\int_0^\pi8\cos^6\frac\theta2\,d\theta = 32\pi a^3\int_0^{\pi/2}\cos^6u\,du = 32\pi a^3\cdot\frac{5\pi}{32}\end{gathered}$$

$$\boxed{V = 5\pi^2a^3}$$

@s 10
$(x + y + 1)dx + (y - x)dy = 0$, i.e. $\dfrac{dy}{dx} = -\dfrac{x + y + 1}{y - x}$. The lines $x + y + 1 = 0$ and $y - x = 0$ meet at $\left(-\tfrac12,-\tfrac12\right)$. Shift the origin: $x = X - \tfrac12$, $y = Y - \tfrac12$, so $x + y + 1 = X + Y$, $y - x = Y - X$:

$$(X + Y)\,dX + (Y - X)\,dY = 0$$

This is homogeneous. Put $Y = vX$, $dY = v\,dX + X\,dv$:

$$\begin{gathered}(1 + v)\,dX + (v - 1)(v\,dX + X\,dv) = 0\ \Longrightarrow\ (1 + v^2)\,dX + X(v - 1)\,dv = 0\end{gathered}$$

$$\frac{dX}{X} + \frac{v - 1}{1 + v^2}\,dv = 0$$

Integrate: $\log X + \dfrac12\log(1 + v^2) - \tan^{-1}v = C$, i.e. $\dfrac12\log\big(X^2 + Y^2\big) - \tan^{-1}\dfrac YX = C$ (since $X\sqrt{1 + v^2} = \sqrt{X^2 + Y^2}$). Returning to $x, y$:

$$\boxed{\frac12\log\left[\left(x + \tfrac12\right)^2 + \left(y + \tfrac12\right)^2\right] - \tan^{-1}\frac{2y + 1}{2x + 1} = C}$$

*Check.* With $F = \tfrac12\log(X^2+Y^2) - \tan^{-1}(Y/X)$: $F_X = \dfrac{X + Y}{X^2 + Y^2}$, $F_Y = \dfrac{Y - X}{X^2 + Y^2}$, which is proportional to the given $M\,dx + N\,dy$. ✓

@s 11
$e^y = p^3 + p$ is solvable for $y$: $y = \log(p^3 + p)$. Differentiate with respect to $x$ with $\dfrac{dy}{dx} = p$:

$$\begin{gathered}p = \frac{3p^2 + 1}{p^3 + p}\frac{dp}{dx}\ \Longrightarrow\ dx = \frac{3p^2 + 1}{p^2(p^2 + 1)}\,dp\end{gathered}$$

Partial fractions: $\dfrac{3p^2 + 1}{p^2(p^2 + 1)} = \dfrac{1}{p^2} + \dfrac{2}{p^2 + 1}$. Integrating,

$$x = -\frac1p + 2\tan^{-1}p + C$$

$$\begin{gathered}\boxed{x = C - \frac1p + 2\tan^{-1}p,\qquad y = \log(p^3 + p)}\end{gathered}$$

the general solution in parametric form (parameter $p$, arbitrary constant $C$; eliminating $p$ is not possible in closed form).

@s 12
$(D^2 + 2D + 1)y = e^x + x^2$.

**C.F.** $(m + 1)^2 = 0\Rightarrow m = -1, -1$: $y_c = (c_1 + c_2x)e^{-x}$.

**P.I.** For $e^x$: $\dfrac{1}{D^2 + 2D + 1}e^x = \dfrac{e^x}{1 + 2 + 1} = \dfrac{e^x}{4}$.

For $x^2$: $\dfrac{1}{(1 + D)^2}x^2 = (1 + D)^{-2}x^2 = (1 - 2D + 3D^2 - \cdots)x^2 = x^2 - 4x + 6$.

$$\boxed{y = (c_1 + c_2x)e^{-x} + \frac{e^x}{4} + x^2 - 4x + 6}$$

@s 13
**Main question.** $(x^2D^2 + xD - 1)y = x^2$ is a Cauchy-Euler equation. Put $x = e^z$, $D_1 = \dfrac{d}{dz}$: $x^2D^2 + xD = D_1^2$, so

$$(D_1^2 - 1)y = e^{2z}$$

**C.F.** $m = \pm1$: $y_c = c_1e^z + c_2e^{-z} = c_1x + \dfrac{c_2}{x}$.

**P.I.** $\dfrac{1}{D_1^2 - 1}e^{2z} = \dfrac{e^{2z}}{4 - 1} = \dfrac{e^{2z}}3 = \dfrac{x^2}3$.

$$\boxed{y = c_1x + \frac{c_2}x + \frac{x^2}{3}}$$

**OR (radioactive decay).** The rate of decay is proportional to the mass present: $\dfrac{dm}{dt} = -km$, so $m = m_0e^{-kt}$ with $m_0 = 100$ mg. At $t = 2$ years $m = 80$ mg:

$$\begin{gathered}80 = 100e^{-2k}\ \Longrightarrow\ e^{-2k} = 0.8\ \Longrightarrow\ k = \frac12\ln\frac{5}{4} = 0.1116\ \text{per year}\end{gathered}$$

$$\begin{gathered}\boxed{m(t) = 100e^{-0.1116\,t} = 100\,(0.8)^{t/2}\ \text{mg}}\end{gathered}$$

(for instance after $4$ years $64$ mg are left; the half-life is $\dfrac{\ln2}{k} = 6.21$ years.)

@s 14
For $ax^2 + 2hxy + by^2 + \cdots = 0$ the $xy$ term disappears after rotating through $\theta$, where

$$\begin{gathered}\tan2\theta = \frac{2h}{a - b} = \frac{4}{11 - 14} = -\frac43\end{gathered}$$

$2\theta$ lies in the second quadrant, so $\cos2\theta = -\dfrac35$ and $\tan^2\theta = \dfrac{1 - \cos2\theta}{1 + \cos2\theta} = 4$, so $\tan\theta = 2$:

$$\begin{gathered}\boxed{\theta = \tan^{-1}2\approx63.43^\circ}\end{gathered}$$

(equivalently $\theta = -26.57^\circ$, i.e. $\tan\theta = -\tfrac12$, which rotates by $90^\circ$ less.) The transformed equation for $\tan\theta = 2$ is $15X^2 + 10Y^2 = 5$ (an ellipse): the coefficients $15$ and $10$ are the roots of $\lambda^2 - 25\lambda + 150 = 0$, the eigenvalues of $\begin{pmatrix}11&2\\2&14\end{pmatrix}$. The given constant $-5$ moves to the right side.

@s 15
**Definition.** A hyperbola is the locus of a point $P$ that moves in a plane such that the ratio of its distance from a fixed point $S$ (the focus) to its distance from a fixed straight line (the directrix) is a constant $e$ greater than $1$: $\dfrac{SP}{PM} = e>1$. (Equivalently, the difference of its distances from two fixed points is constant, $|S'P - SP| = 2a$.)

**Deduction.** Take the focus $S = (ae, 0)$ and directrix $x = \dfrac ae$ (the axes through the centre):

$$\begin{gathered}(x - ae)^2 + y^2 = e^2\left(x - \frac ae\right)^2 = (ex - a)^2\end{gathered}$$

$$\begin{gathered}x^2 - 2aex + a^2e^2 + y^2 = e^2x^2 - 2aex + a^2\ \Longrightarrow\ (e^2 - 1)x^2 - y^2 = a^2(e^2 - 1)\end{gathered}$$

Divide by $a^2(e^2 - 1)>0$ and put $b^2 = a^2(e^2 - 1)$:

$$\begin{gathered}\boxed{\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1,\qquad b^2 = a^2(e^2 - 1)}\end{gathered}$$

Foci $(\pm ae, 0)$, directrices $x = \pm\dfrac ae$, vertices $(\pm a, 0)$, transverse axis $2a$, conjugate axis $2b$, latus rectum $\dfrac{2b^2}{a}$, asymptotes $\dfrac xa\pm\dfrac yb = 0$. For the point $P$: $SP = ex - a$ and $S'P = ex + a$, so $S'P - SP = 2a$.

```figure caption="Question 15: the hyperbola x^2/a^2 - y^2/b^2 = 1 with foci S, S', vertices A, A', directrices and asymptotes."
a,b=2.0,1.5; c=np.hypot(a,b); t=np.linspace(-1.6,1.6,200)
fig,ax=plt.subplots(figsize=(4.4,2.8))
for s in (1,-1): ax.plot(s*a*np.cosh(t),b*np.sinh(t),color='#1d6fb8',lw=1.8)
xs=np.array([-4.2,4.2]); ax.plot(xs,b/a*xs,'--',color='#999',lw=.9); ax.plot(xs,-b/a*xs,'--',color='#999',lw=.9)
for s in (1,-1): ax.axvline(s*a*a/c,color='#d9534f',lw=.9,ls=':')
ax.plot([c,-c,a,-a,0],[0,0,0,0,0],'o',color='#14181f',ms=3)
for xx,l in [(c,'S'),(-c,"S'"),(a,'A'),(-a,"A'"),(0,'O')]: ax.text(xx,-0.4,l,ha='center',fontsize=8)
ax.axhline(0,color='#14181f',lw=.6); ax.set_aspect('equal'); ax.axis('off'); ax.set_ylim(-2.6,2.8)
```

@s 16
$3x^2 + 8xy - 3y^2 - 40x - 20y + 50 = 0$: $a = 3$, $h = 4$, $b = -3$, $g = -20$, $f = -10$, $c = 50$. Since $h^2 - ab = 16 + 9 = 25>0$, this is a hyperbola, and $a + b = 0$ shows it is rectangular.

**Centre.** Solve $\dfrac{\partial}{\partial x} = \dfrac{\partial}{\partial y} = 0$:

$$\begin{gathered}6x + 8y - 40 = 0,\quad 8x - 6y - 20 = 0\ \Longrightarrow\ 3x + 4y = 20,\ 4x - 3y = 10\ \Longrightarrow\ x = 4,\ y = 2\end{gathered}$$

**Centre $(4, 2)$.** Shifting the origin there the constant becomes $c' = gx_0 + fy_0 + c = -20(4) - 10(2) + 50 = -50$:

$$3X^2 + 8XY - 3Y^2 = 50$$

**Axes.** The eigenvalues of $\begin{pmatrix}3&4\\4&-3\end{pmatrix}$ are $\pm5$ ($\lambda^2 = 25$), so after rotating the axes through $\theta$ with $\tan2\theta = \dfrac{8}{3 + 3} = \dfrac43$ ($\tan\theta = \tfrac12$):

$$\begin{gathered}5X'^2 - 5Y'^2 = 50\ \Longrightarrow\ \frac{X'^2}{10} - \frac{Y'^2}{10} = 1\end{gathered}$$

so $a^2 = b^2 = 10$. Transverse axis $2a = 2\sqrt{10}\approx6.32$, conjugate axis $2b = 2\sqrt{10}$, and $e = \sqrt{1 + \dfrac{b^2}{a^2}} = \sqrt2$.

$$\boxed{\text{Centre }(4,2),\quad\text{axes }2\sqrt{10}\text{ and }2\sqrt{10},\quad e = \sqrt2}$$

(The same conic appears as the OR part of Question 16 of the 2079 Baishakh paper.)

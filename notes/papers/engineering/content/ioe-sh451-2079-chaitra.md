---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-SH451-2079-Chaitra.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: SH 451
year_bs: 2079 Chaitra
cal: BS
year_ad: 2023
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (old course, SH 451). All questions carry equal marks (5 each). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
State Euler's Theorem for a homogeneous function in two variables. If $u = \cos^{-1}\!\left(\dfrac{x+y}{\sqrt x + \sqrt y}\right)$ prove that: $x\dfrac{\partial u}{\partial x} + y\dfrac{\partial u}{\partial y} = -\dfrac12\cot u$. [[5]]

@q 2
Find the extreme value of $x^2 + xy + y^2 + 3z^2$ connected by the relation $x + 2y + 4z = 60$. [[5]]

@q 3
Evaluate: $\displaystyle\iint_Ry\,dy\,dx$ where $R$ is the region bounded by parabola $y^2 = 4x$ and $x^2 = 4y$. [[5]]

@q 4
Find the volume of ellipsoid $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} + \dfrac{z^2}{c^2} = 1$ using triple integration. [[5]]

@q 5
Show that the lines $\dfrac{x-5}{4} = \dfrac{y-7}{4} = \dfrac{z+3}{-5}$; $\dfrac{x-8}{7} = \dfrac{y-4}{1} = \dfrac{z-5}{3}$ are coplanar. Find the plane in which they lie. [[5]]

@q 6
Find the magnitude and the equation of the shortest distance between the lines $\dfrac x2 = \dfrac y{-3} = \dfrac z1$ and $\dfrac{x-2}{3} = \dfrac{y-1}{-5} = \dfrac{z+2}{2}$. [[5]]

@q 7
Define the term 'Great Circle'. Find the equation of the sphere having the circle $x^2 + y^2 + z^2 + 10y - 4z - 8 = 0,\ x + y + z = 3$ as a Great Circle. [[5]]

@q 8
Find the equation of the cone with vertex at $(1, 2, 3)$ and guiding curve $y^2 = 16x,\ z = 1$. [[5]]

@q 9
Find a power series solution for $y'' - 4y = 0$. [[5]]

@q 10
Express $f(x) = 5x^3 + x$ in terms of Legendre's Polynomials. [[5]]

@q 11
Prove that $J_{3/2}(x) = \sqrt{\dfrac{2}{\pi x}}\left(\dfrac{\sin x}{x} - \cos x\right)$. [[5]]

@q 12
Define vector triple product. Prove that $\hat i\times(\vec a\times\hat i) + \hat j\times(\vec a\times\hat j) + \hat k\times(\vec a\times\hat k) = 2\vec a$ where $\hat i, \hat j, \hat k$ are mutually unit vectors along the co-ordinates axes. [[5]]

@q 13
The necessary and sufficient condition for the vector function of a scalar variable $t$ have a constant magnitude is $\vec a\cdot\dfrac{d\vec a}{dt} = 0$. [[5]]

@q 14
Find the directional derivative of $\phi = x^2yz + 4xz^2$ at $(1, -2, -1)$ in the direction of $2\hat i - \hat j - 2\hat k$. [[5]]

@q 15
Test the convergence of the series: $\displaystyle\sum_{n=1}^\infty\frac{x^n}{n\cdot(n+1)}$ where $x>0$. [[5]]

@q 16
Find the interval and radius of convergence of the power series: $\displaystyle\sum_{n=1}^\infty\frac{2^n(x-3)^n}{(n+4)}$. [[5]]
<!-- SOLUTIONS -->

@s 1
**Euler's theorem.** If $f(x,y)$ is a homogeneous function of degree $n$ (i.e. $f(tx,ty) = t^nf(x,y)$) with continuous first partial derivatives, then
$$\boxed{x\frac{\partial f}{\partial x} + y\frac{\partial f}{\partial y} = n\,f}$$
**Proof of the problem.** Let $f = \cos u = \dfrac{x+y}{\sqrt x+\sqrt y}$. Replace $x\to tx$, $y\to ty$: $f(tx,ty) = \dfrac{t(x+y)}{\sqrt t(\sqrt x+\sqrt y)} = t^{1/2}f(x,y)$, so $f$ is homogeneous of degree $n = \tfrac12$. By Euler's theorem
$$x\frac{\partial f}{\partial x} + y\frac{\partial f}{\partial y} = \frac12f$$
Since $f = \cos u$: $\dfrac{\partial f}{\partial x} = -\sin u\dfrac{\partial u}{\partial x}$, etc., so
$$-\sin u\left(x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y}\right) = \frac12\cos u$$
$$\boxed{x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = -\frac12\cot u}$$
$\blacksquare$

@s 2
Minimize / extremize $f = x^2 + xy + y^2 + 3z^2$ subject to $g = x + 2y + 4z - 60 = 0$. Lagrange's method: $F = f + \lambda'g$, or equivalently $\nabla f = \lambda\nabla g$:
$$\begin{gathered}2x + y = \lambda \\ x + 2y = 2\lambda \\ 6z = 4\lambda\end{gathered}$$
From the first two: subtract $2\times$(first) from second: $x + 2y - 4x - 2y = 2\lambda - 2\lambda\Rightarrow-3x = 0$, so $x = 0$. Then $y = \lambda$ and $z = \dfrac{2\lambda}3$. The constraint:
$$0 + 2\lambda + \frac{8\lambda}{3} = 60\ \Rightarrow\ \frac{14\lambda}3 = 60\ \Rightarrow\ \lambda = \frac{90}7$$
$$\begin{gathered}x = 0 \\ y = \frac{90}7 \\ z = \frac{60}7\end{gathered}$$
**Nature.** The Hessian of $f$, $\begin{pmatrix}2&1&0\\1&2&0\\0&0&6\end{pmatrix}$ has eigenvalues $1, 3, 6>0$ (positive definite), and the constraint is linear, so the point is a **minimum**.
$$f_{min} = \frac{90^2}{49} + 3\cdot\frac{60^2}{49} = \frac{8100 + 10800}{49}$$
$$\boxed{f_{min} = \frac{2700}{7}\approx385.7\ \text{at}\ \left(0,\tfrac{90}7,\tfrac{60}7\right)}$$

@s 3
The parabolas $y^2 = 4x$ and $x^2 = 4y$ meet where $y = \dfrac{x^2}{4}$ gives $\dfrac{x^4}{16} = 4x\Rightarrow x = 0, 4$: the points $(0,0)$ and $(4,4)$.

```figure caption="Question 3: region R between y^2 = 4x (upper curve) and x^2 = 4y (lower curve)."
x=np.linspace(0,4,200)
fig,ax=plt.subplots(figsize=(3.6,3.0))
ax.plot(x,2*np.sqrt(x),color='#1d6fb8',lw=1.6); ax.plot(x,x**2/4,color='#d9534f',lw=1.6)
ax.fill_between(x,x**2/4,2*np.sqrt(x),color='#dbe8f6')
ax.text(.6,2.6,'$y^2=4x$',fontsize=8,color='#1d6fb8'); ax.text(2.6,1.0,'$x^2=4y$',fontsize=8,color='#d9534f')
ax.plot([0,4],[0,4],'o',color='#14181f',ms=3); ax.text(4.05,4.0,'$(4,4)$',fontsize=7)
ax.set_xlim(-.2,5); ax.set_ylim(-.2,4.6); ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
```

For fixed $x\in[0,4]$, $y$ runs from $\dfrac{x^2}4$ to $2\sqrt x$:
$$\iint_Ry\,dy\,dx = \int_0^4\left[\frac{y^2}2\right]_{x^2/4}^{2\sqrt x}dx = \frac12\int_0^4\left(4x - \frac{x^4}{16}\right)dx$$
$$= \frac12\left[2x^2 - \frac{x^5}{80}\right]_0^4 = \frac12\left(32 - \frac{1024}{80}\right) = \frac12(32 - 12.8)$$
$$\boxed{\iint_Ry\,dy\,dx = \frac{48}5 = 9.6}$$

@s 4
Volume $V = \displaystyle\iiint dx\,dy\,dz$ over the ellipsoid. By symmetry take the first octant and multiply by $8$. For a given $(x,y)$ in the ellipse $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2}\le1$, $z$ runs from $0$ to $c\sqrt{1 - \dfrac{x^2}{a^2} - \dfrac{y^2}{b^2}}$:
$$V = 8\iint_{E}c\sqrt{1 - \frac{x^2}{a^2} - \frac{y^2}{b^2}}\,dx\,dy$$
Put $x = a r\cos\theta,\ y = br\sin\theta$ with Jacobian $J = abr$; $r: 0\to1,\ \theta: 0\to\dfrac\pi2$:
$$V = 8abc\int_0^{\pi/2}d\theta\int_0^1r\sqrt{1 - r^2}\,dr = 8abc\cdot\frac\pi2\cdot\left[-\frac13(1 - r^2)^{3/2}\right]_0^1 = 8abc\cdot\frac\pi2\cdot\frac13$$
$$\boxed{V = \frac{4}{3}\pi abc}$$
(For $a = b = c = R$ this gives the sphere, $\tfrac43\pi R^3$.)

@s 5
Line 1 passes through $A(5,7,-3)$ with direction $\vec d_1 = (4,4,-5)$; line 2 passes through $B(8,4,5)$ with direction $\vec d_2 = (7,1,3)$. The lines are coplanar iff $\overrightarrow{AB}\cdot(\vec d_1\times\vec d_2) = 0$:
$$\overrightarrow{AB} = (3,-3,8)$$
$$\begin{vmatrix}3&-3&8\\4&4&-5\\7&1&3\end{vmatrix} = 3(12 + 5) + 3(12 + 35) + 8(4 - 28) = 51 + 141 - 192 = 0$$
So the lines are **coplanar**. $\blacksquare$

**Plane.** Normal $\vec n = \vec d_1\times\vec d_2 = \begin{vmatrix}\hat i&\hat j&\hat k\\4&4&-5\\7&1&3\end{vmatrix} = (12 + 5)\hat i - (12 + 35)\hat j + (4 - 28)\hat k = (17, -47, -24)$.

Through $A(5,7,-3)$: $17(x-5) - 47(y-7) - 24(z+3) = 0$
$$\boxed{17x - 47y - 24z + 172 = 0}$$
Check with $B(8,4,5)$: $136 - 188 - 120 + 172 = 0$ ✓.

@s 6
Line 1: through $A(0,0,0)$, direction $\vec d_1 = (2,-3,1)$. Line 2: through $B(2,1,-2)$, direction $\vec d_2 = (3,-5,2)$.
$$\vec n = \vec d_1\times\vec d_2 = \begin{vmatrix}\hat i&\hat j&\hat k\\2&-3&1\\3&-5&2\end{vmatrix} = (-6 + 5)\hat i - (4 - 3)\hat j + (-10 + 9)\hat k = (-1,-1,-1)$$
$$\begin{gathered}|\vec n| = \sqrt3 \\ \overrightarrow{AB} = (2,1,-2)\end{gathered}$$
**Magnitude:**
$$SD = \frac{|\overrightarrow{AB}\cdot\vec n|}{|\vec n|} = \frac{|-2 - 1 + 2|}{\sqrt3}$$
$$\boxed{SD = \frac{1}{\sqrt3}\approx0.577}$$
**Equation of the line of shortest distance.** It is the intersection of the plane through line 1 containing $\vec n$ and the plane through line 2 containing $\vec n$.

Plane 1: normal $\vec d_1\times\vec n\parallel(2,-3,1)\times(1,1,1) = (-3-1,\ 1-2,\ 2+3) = (-4,-1,5)$; through the origin: $4x + y - 5z = 0$.

Plane 2: normal $\vec d_2\times\vec n\parallel(3,-5,2)\times(1,1,1) = (-5-2,\ 2-3,\ 3+5) = (-7,-1,8)$; through $B(2,1,-2)$: $7(x-2) + (y-1) - 8(z+2) = 0$, i.e. $7x + y - 8z - 31 = 0$.
$$\boxed{4x + y - 5z = 0,\qquad7x + y - 8z - 31 = 0}$$
(its direction ratios are $(1,1,1)$, perpendicular to both lines.)

@s 7
**Great circle.** The section of a sphere by a plane passing through its centre is called a great circle: it has the same centre and radius as the sphere (the largest possible circle on it).

Any sphere through the given circle is $S + \lambda P = 0$:
$$x^2 + y^2 + z^2 + 10y - 4z - 8 + \lambda(x + y + z - 3) = 0$$
Its centre is $\left(-\dfrac\lambda2,\ -\dfrac{10+\lambda}2,\ \dfrac{4-\lambda}2\right)$. For the circle to be a great circle the centre must lie on the plane $x + y + z = 3$:
$$-\frac\lambda2 - 5 - \frac\lambda2 + 2 - \frac\lambda2 = 3\ \Rightarrow\ -\frac{3\lambda}{2} = 6\ \Rightarrow\ \lambda = -4$$
Substituting:
$$x^2 + y^2 + z^2 + 10y - 4z - 8 - 4x - 4y - 4z + 12 = 0$$
$$\boxed{x^2 + y^2 + z^2 - 4x + 6y - 8z + 4 = 0}$$
Centre $(2,-3,4)$ (on $x+y+z=3$: $2 - 3 + 4 = 3$ ✓), radius $\sqrt{4 + 9 + 16 - 4} = 5$.

@s 8
Vertex $V(1,2,3)$. Let $P(\alpha,\beta,\gamma)$ be any point on the cone. The generator $VP$ has direction ratios $(\alpha-1,\beta-2,\gamma-3)$, so a point on it is
$$\frac{x-1}{\alpha-1} = \frac{y-2}{\beta-2} = \frac{z-3}{\gamma-3}$$
It meets the plane $z = 1$ of the guiding curve where
$$\frac{x-1}{\alpha-1} = \frac{y-2}{\beta-2} = \frac{1-3}{\gamma-3} = \frac{-2}{\gamma-3}$$
$$\begin{gathered}x = 1 - \frac{2(\alpha-1)}{\gamma-3} = \frac{\gamma - 2\alpha - 1}{\gamma-3} \\ y = 2 - \frac{2(\beta-2)}{\gamma-3} = \frac{2\gamma - 2\beta - 2}{\gamma-3}\end{gathered}$$
This point lies on $y^2 = 16x$:
$$\frac{(2\gamma - 2\beta - 2)^2}{(\gamma-3)^2} = \frac{16(\gamma - 2\alpha - 1)}{\gamma-3}\ \Rightarrow\ (\gamma - \beta - 1)^2 = 4(\gamma-3)(\gamma - 2\alpha - 1)$$
Locus of $(\alpha,\beta,\gamma)$:
$$(z - y - 1)^2 = 4(z-3)(z - 2x - 1)$$
Expanding: $z^2 + y^2 + 1 - 2yz - 2z + 2y = 4z^2 - 8xz - 4z - 12z + 24x + 12$:
$$\boxed{y^2 - 3z^2 - 2yz + 8xz - 24x + 2y + 14z - 11 = 0}$$
Check: the vertex $(1,2,3)$ satisfies it ($4 - 27 - 12 + 24 - 24 + 4 + 42 - 11 = 0$ ✓).

@s 9
Assume $y = \displaystyle\sum_{n=0}^\infty a_nx^n$. Then $y'' = \displaystyle\sum_{n=0}^\infty(n+2)(n+1)a_{n+2}x^n$. Substitute in $y'' - 4y = 0$ and equate the coefficient of $x^n$ to zero:
$$(n+2)(n+1)a_{n+2} - 4a_n = 0\ \Rightarrow\ \boxed{a_{n+2} = \frac{4\,a_n}{(n+1)(n+2)}}$$
Even terms: $a_2 = \dfrac{4a_0}{2} = 2a_0$, $a_4 = \dfrac{4a_2}{12} = \dfrac{2a_0}{3}$, $a_6 = \dfrac{4a_4}{30} = \dfrac{4a_0}{45}$.

Odd terms: $a_3 = \dfrac{4a_1}{6} = \dfrac{2a_1}{3}$, $a_5 = \dfrac{4a_3}{20} = \dfrac{2a_1}{15}$.
$$\boxed{y = a_0\left(1 + 2x^2 + \frac23x^4 + \frac4{45}x^6 + \cdots\right) + a_1\left(x + \frac23x^3 + \frac2{15}x^5 + \cdots\right)}$$
with $a_0, a_1$ arbitrary. The series are $\cosh2x$ and $\tfrac12\sinh2x$ (since $\cosh2x = \sum\dfrac{(2x)^{2k}}{(2k)!}$), so $y = a_0\cosh2x + \dfrac{a_1}2\sinh2x$ i.e. $y = c_1e^{2x} + c_2e^{-2x}$, as given directly by the auxiliary equation $m^2 = 4$.

@s 10
Legendre polynomials: $P_0 = 1,\ P_1 = x,\ P_2 = \tfrac12(3x^2 - 1),\ P_3 = \tfrac12(5x^3 - 3x)$.

From $P_3$: $5x^3 = 2P_3 + 3x = 2P_3 + 3P_1$. Hence
$$f(x) = 5x^3 + x = 2P_3 + 3P_1 + P_1$$
$$\boxed{5x^3 + x = 2P_3(x) + 4P_1(x)}$$
Check: $2\cdot\tfrac12(5x^3 - 3x) + 4x = 5x^3 - 3x + 4x = 5x^3 + x$ ✓.

@s 11
Bessel function: $J_n(x) = \displaystyle\sum_{r=0}^\infty\frac{(-1)^r}{r!\,\Gamma(n+r+1)}\left(\frac x2\right)^{n+2r}$.

**$J_{1/2}$:** use $r!\,\Gamma(r + \tfrac32) = \dfrac{\sqrt\pi\,(2r+1)!}{2^{2r+1}}$ and $\left(\dfrac x2\right)^{2r+1/2} = \dfrac{x^{2r+1/2}}{2^{2r+1/2}}$:
$$J_{1/2}(x) = \sum_{r=0}^\infty\frac{(-1)^r\,2^{2r+1}}{\sqrt\pi\,(2r+1)!}\cdot\frac{x^{2r+1/2}}{2^{2r+1/2}} = \sqrt{\frac{2}{\pi x}}\sum_{r=0}^\infty\frac{(-1)^rx^{2r+1}}{(2r+1)!}$$
$$\boxed{J_{1/2}(x) = \sqrt{\frac2{\pi x}}\sin x}$$
**$J_{-1/2}$:** similarly, using $r!\,\Gamma(r+\tfrac12) = \dfrac{\sqrt\pi\,(2r)!}{2^{2r}}$:
$$J_{-1/2}(x) = \sqrt{\frac{2}{\pi x}}\sum_{r=0}^\infty\frac{(-1)^rx^{2r}}{(2r)!} = \sqrt{\frac2{\pi x}}\cos x$$
**Recurrence relation** $J_{n+1}(x) = \dfrac{2n}xJ_n(x) - J_{n-1}(x)$ with $n = \tfrac12$:
$$J_{3/2}(x) = \frac1xJ_{1/2}(x) - J_{-1/2}(x) = \sqrt{\frac{2}{\pi x}}\left(\frac{\sin x}x - \cos x\right)$$
$\blacksquare$

@s 12
**Vector triple product.** For three vectors, $\vec a\times(\vec b\times\vec c) = (\vec a\cdot\vec c)\vec b - (\vec a\cdot\vec b)\vec c$. It is a vector in the plane of $\vec b$ and $\vec c$, perpendicular to $\vec a$, and generally $\vec a\times(\vec b\times\vec c)\ne(\vec a\times\vec b)\times\vec c$.

**Proof.** Using the formula, $\hat i\times(\vec a\times\hat i) = (\hat i\cdot\hat i)\vec a - (\hat i\cdot\vec a)\hat i = \vec a - a_1\hat i$, where $\vec a = a_1\hat i + a_2\hat j + a_3\hat k$. Similarly the other two terms are $\vec a - a_2\hat j$ and $\vec a - a_3\hat k$. Adding:
$$\sum\hat i\times(\vec a\times\hat i) = 3\vec a - (a_1\hat i + a_2\hat j + a_3\hat k) = 3\vec a - \vec a$$
$$\boxed{\hat i\times(\vec a\times\hat i) + \hat j\times(\vec a\times\hat j) + \hat k\times(\vec a\times\hat k) = 2\vec a}$$
$\blacksquare$

@s 13
Let $\vec a(t)$ be a differentiable vector function and $|\vec a| = a$.

**Necessary.** If the magnitude is constant, $\vec a\cdot\vec a = a^2 = $ constant. Differentiate with respect to $t$:
$$\vec a\cdot\frac{d\vec a}{dt} + \frac{d\vec a}{dt}\cdot\vec a = 0\ \Rightarrow\ 2\,\vec a\cdot\frac{d\vec a}{dt} = 0\ \Rightarrow\ \vec a\cdot\frac{d\vec a}{dt} = 0$$
**Sufficient.** If $\vec a\cdot\dfrac{d\vec a}{dt} = 0$, then $\dfrac{d}{dt}(\vec a\cdot\vec a) = 2\vec a\cdot\dfrac{d\vec a}{dt} = 0$, so $\vec a\cdot\vec a = |\vec a|^2$ is constant, i.e. $|\vec a|$ is constant. $\blacksquare$

(Geometrically: the derivative of a vector of constant length, e.g. the position vector of a particle in circular motion, is perpendicular to the vector itself.)

@s 14
$\phi = x^2yz + 4xz^2$:
$$\nabla\phi = (2xyz + 4z^2)\hat i + x^2z\,\hat j + (x^2y + 8xz)\hat k$$
At $(1,-2,-1)$:
$$\begin{gathered}\phi_x = 2(1)(-2)(-1) + 4(1) = 4 + 4 = 8 \\ \phi_y = (1)(-1) = -1 \\ \phi_z = (1)(-2) + 8(1)(-1) = -10\end{gathered}$$
$$\nabla\phi = 8\hat i - \hat j - 10\hat k$$
Unit vector along $2\hat i - \hat j - 2\hat k$: $\hat u = \dfrac{2\hat i - \hat j - 2\hat k}{\sqrt{4 + 1 + 4}} = \dfrac13(2,-1,-2)$.
$$D_{\hat u}\phi = \nabla\phi\cdot\hat u = \frac{16 + 1 + 20}{3}$$
$$\boxed{D_{\hat u}\phi = \frac{37}{3}\approx12.33}$$

@s 15
Let $u_n = \dfrac{x^n}{n(n+1)}$, $x>0$. By d'Alembert's ratio test:
$$\frac{u_{n+1}}{u_n} = \frac{x^{n+1}}{(n+1)(n+2)}\cdot\frac{n(n+1)}{x^n} = x\cdot\frac{n}{n+2}\ \to\ x\quad(n\to\infty)$$
- If $x<1$: the series **converges**.
- If $x>1$: the series **diverges** (the terms $u_n\to\infty$).
- If $x = 1$ the test fails: $u_n = \dfrac1{n(n+1)}$, which compares with $\dfrac1{n^2}$ (limit comparison, $\lim\dfrac{u_n}{1/n^2} = 1$, $p = 2>1$). Moreover $\sum\dfrac{1}{n(n+1)} = \sum\left(\dfrac1n - \dfrac1{n+1}\right) = 1$ (telescoping). So it **converges**.

$$\boxed{\text{Convergent for }0<x\le1;\ \text{divergent for }x>1}$$

@s 16
Series $\sum\dfrac{2^n(x-3)^n}{n+4}$: $a_n = \dfrac{2^n}{n+4}$, centre $x = 3$.
$$\left|\frac{a_{n+1}}{a_n}\right| = \frac{2^{n+1}}{n+5}\cdot\frac{n+4}{2^n} = 2\cdot\frac{n+4}{n+5}\to2\ \Rightarrow\ R = \frac1{2}$$
The series converges absolutely for $|x - 3|<\dfrac12$, i.e. $\dfrac52<x<\dfrac72$.

**Endpoints.**

- $x = \dfrac72$: $(x - 3) = \dfrac12$, the series is $\sum\dfrac1{n+4}$, which diverges (harmonic series, $p = 1$).
- $x = \dfrac52$: $(x-3) = -\dfrac12$, the series is $\sum\dfrac{(-1)^n}{n+4}$, an alternating series whose terms decrease to $0$: it converges (Leibnitz test).

$$\boxed{R = \frac12,\qquad\text{interval of convergence }\frac52\le x<\frac72}$$

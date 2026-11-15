---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-SH451-2078-Chaitra.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: SH 451
year_bs: 2078 Chaitra
cal: BS
year_ad: 2022
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (old course, SH 451). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
State Euler's Theorem for Homogeneous function of two variables. If $u = \sec^{-1}\!\left(\dfrac{x^3 + y^3}{x + y}\right)$ then show that $x\dfrac{\partial u}{\partial x} + y\dfrac{\partial u}{\partial y} = 2\cot u$ [[1+4]]

@q 2
What are the criteria for a function $f(x,y)$ to have local maximum and minimum value? Using the criteria, evaluate the extreme value of $x^2 + y^2 + z^2$ subject to the condition $x + y + z = 1$. [[5]]

@q 3
What advantage do we get by changing Cartesian integrals into polar form? Change the following integral into Polar and hence evaluate $\displaystyle\int_0^a\int_0^{\sqrt{a^2 - x^2}}\sqrt{x^2 + y^2}\,dy\,dx$ [[1+4]]

@q 4
Find by triple integration, the volume of the sphere $x^2 + y^2 + z^2 = a^2$ [[5]]

@q 5
Find the image of the point $(1, 3, 4)$ in the plane $2x - y + z + 3 = 0$. [[5]]

@q 6
Find the magnitude and equations of shortest distance between the lines $\dfrac{x-1}{2} = \dfrac{y-2}{3} = \dfrac{z-3}{4}$ and $\dfrac{x-2}{3} = \dfrac{y-4}{4} = \dfrac{z-5}{5}$ [[5]]

@q 7
What is the cross section of an intersecting sphere and a plane? How many spheres pass through their intersection?

Obtain the centre and radius of the circle $x^2 + y^2 + z^2 + x + y + z - 4 = 0,\ x + y + z = 0$. [[1+4]]

@q 8
Find the equation of the right circular cylinder of radius $2$ and whose axis is the line $\dfrac{x-1}{2} = \dfrac{y-2}{1} = \dfrac{z-3}{2}$. [[5]]

@q 9
Apply the power series method to solve the differential equation $y'' + xy' + y = 0$. [[5]]

@q 10
Express $x^3 - 5x^2 + 6x + 1$ in terms of Legendre's polynomials. [[5]]

@q 11
Prove that $xJ_n'(x) = nJ_n(x) - xJ_{n+1}(x)$ where the symbol $J_n$ denote Bessel's function. [[5]]

@q 12
Find the set of reciprocal system to the set vectors $2\hat i + 3\hat j - \hat k,\ -\hat i + 2\hat j - 3\hat k$ and $3\hat i - 4\hat j + 2\hat k$ [[5]]

@q 13
The necessary and sufficient condition for the vector function of a scalar variable $t$ have a constant magnitude is $\vec a\cdot\dfrac{d\vec a}{dt} = 0$. [[5]]

@q 14
Find the angle between the surfaces $xy^2z = 3x + z^2$ and $3x^2 - y^2 + 2z = 1$ at the point $(1, -2, 1)$. [[5]]

@q 15
Test the series for convergence or divergence $\dfrac{x}{1.2} + \dfrac{x^2}{2.3} + \dfrac{x^3}{3.4} + \cdots,\ (x>0)$ [[5]]

@q 16
Find the radius and interval of convergence of the power series: $\displaystyle\sum_{n=1}^\infty\frac{(-1)^n(x+1)^n}{2^n}$. [[5]]
<!-- SOLUTIONS -->

@s 1
**Euler's theorem.** If $f(x,y)$ is homogeneous of degree $n$ with continuous first partial derivatives, then
$$\boxed{x\frac{\partial f}{\partial x} + y\frac{\partial f}{\partial y} = nf}$$
**Proof of the problem.** Let $f = \sec u = \dfrac{x^3 + y^3}{x + y}$. Under $x\to tx,\ y\to ty$, $f\to\dfrac{t^3(x^3+y^3)}{t(x+y)} = t^2f$, so $f$ is homogeneous of degree $2$. By Euler's theorem
$$x\frac{\partial f}{\partial x} + y\frac{\partial f}{\partial y} = 2f$$
Now $\dfrac{\partial f}{\partial x} = \sec u\tan u\,\dfrac{\partial u}{\partial x}$ and similarly for $y$:
$$\sec u\tan u\left(x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y}\right) = 2\sec u$$
$$x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = \frac{2}{\tan u}$$
$$\boxed{x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = 2\cot u}$$
$\blacksquare$

@s 2
**Criteria.** Let $f(x,y)$ have continuous second partial derivatives. A **stationary point** $(a,b)$ satisfies $f_x = 0$ and $f_y = 0$. With $r = f_{xx}$, $s = f_{xy}$, $t = f_{yy}$ evaluated at $(a,b)$:

- $rt - s^2>0$ and $r<0$: local **maximum**;
- $rt - s^2>0$ and $r>0$: local **minimum**;
- $rt - s^2<0$: **saddle point** (no extremum);
- $rt - s^2 = 0$: the test fails (examine further).

**Extreme value.** On $x + y + z = 1$, $z = 1 - x - y$, so
$$f(x,y) = x^2 + y^2 + (1 - x - y)^2$$
$$\begin{gathered}f_x = 2x - 2(1 - x - y) = 4x + 2y - 2 = 0 \\ f_y = 4y + 2x - 2 = 0\end{gathered}$$
Subtracting: $x = y$; then $6x = 2$, $x = y = \dfrac13$, $z = \dfrac13$.
$$\begin{gathered}r = f_{xx} = 4 \\ s = f_{xy} = 2 \\ t = f_{yy} = 4\end{gathered}$$
$$\begin{gathered}rt - s^2 = 16 - 4 = 12>0 \\ r = 4>0\ \Rightarrow\ \text{minimum}\end{gathered}$$
$$\boxed{f_{min} = \frac19 + \frac19 + \frac19 = \frac13\ \text{at}\ \left(\tfrac13,\tfrac13,\tfrac13\right)}$$
(It is the squared distance from the origin to the plane $x + y + z = 1$: $\left(\dfrac{1}{\sqrt3}\right)^2$ ✓.)

@s 3
**Advantage of polar form.** When the region of integration is a circle, sector or annulus, or the integrand contains $x^2 + y^2$, the polar limits become simple constants and the integrand simplifies (e.g. $\sqrt{x^2+y^2} = r$); integrals that are difficult or impossible in Cartesian form become elementary. Also $dx\,dy = r\,dr\,d\theta$.

**Change of variables.** The region: $0\le x\le a$, $0\le y\le\sqrt{a^2 - x^2}$ is the quarter circle $x^2 + y^2\le a^2$ in the first quadrant. In polar coordinates $x = r\cos\theta$, $y = r\sin\theta$: $0\le r\le a$ and $0\le\theta\le\dfrac\pi2$.
$$I = \int_0^{\pi/2}\int_0^ar\cdot r\,dr\,d\theta = \int_0^{\pi/2}d\theta\int_0^ar^2\,dr = \frac\pi2\cdot\frac{a^3}{3}$$
$$\boxed{I = \frac{\pi a^3}{6}}$$

@s 4
Sphere $x^2 + y^2 + z^2 = a^2$. By symmetry $V = 8\times$ (volume in the first octant):
$$V = 8\int_0^a\int_0^{\sqrt{a^2 - x^2}}\int_0^{\sqrt{a^2 - x^2 - y^2}}dz\,dy\,dx = 8\int_0^a\int_0^{\sqrt{a^2 - x^2}}\sqrt{a^2 - x^2 - y^2}\,dy\,dx$$
With $\rho^2 = a^2 - x^2$ the inner integral is a quarter-disc area integral: $\displaystyle\int_0^{\rho}\sqrt{\rho^2 - y^2}\,dy = \dfrac{\pi\rho^2}4$. So
$$V = 8\int_0^a\frac\pi4(a^2 - x^2)\,dx = 2\pi\left[a^2x - \frac{x^3}3\right]_0^a = 2\pi\cdot\frac{2a^3}{3}$$
$$\boxed{V = \frac43\pi a^3}$$
(Spherical-polar check: $V = \displaystyle\int_0^{2\pi}\int_0^\pi\int_0^ar^2\sin\theta\,dr\,d\theta\,d\phi = 2\pi\cdot2\cdot\frac{a^3}3$.)

@s 5
Plane: $2x - y + z + 3 = 0$, normal $\vec n = (2,-1,1)$, $|\vec n|^2 = 6$. Point $P(1,3,4)$.

Value of the plane expression at $P$: $2(1) - 3 + 4 + 3 = 6$.

The foot of the perpendicular from $P$ is $P - \dfrac{6}{6}\vec n = (1,3,4) - (2,-1,1) = (-1,4,3)$; check on plane: $-2 - 4 + 3 + 3 = 0$ ✓. The image $P'$ is the point as far on the other side:
$$P' = P - 2\cdot\frac{(2x_1 - y_1 + z_1 + 3)}{|\vec n|^2}\vec n = (1,3,4) - 2(2,-1,1) = (-3,5,2)$$
$$\boxed{\text{Image} = (-3,\ 5,\ 2)}$$
(Check: midpoint of $P$ and $P'$ is $(-1,4,3)$, which is on the plane, and $PP'\parallel\vec n$ ✓.)

@s 6
Line 1: through $A(1,2,3)$, $\vec d_1 = (2,3,4)$. Line 2: through $B(2,4,5)$, $\vec d_2 = (3,4,5)$.
$$\vec n = \vec d_1\times\vec d_2 = \begin{vmatrix}\hat i&\hat j&\hat k\\2&3&4\\3&4&5\end{vmatrix} = (15 - 16)\hat i - (10 - 12)\hat j + (8 - 9)\hat k = (-1,2,-1),\qquad|\vec n| = \sqrt6$$
$$\begin{gathered}\overrightarrow{AB} = (1,2,2) \\ \overrightarrow{AB}\cdot\vec n = -1 + 4 - 2 = 1\end{gathered}$$
**Magnitude**
$$\boxed{SD = \frac{|\overrightarrow{AB}\cdot\vec n|}{|\vec n|} = \frac1{\sqrt6}\approx0.408}$$
**Equations of the line of shortest distance.** It is the intersection of the plane through line 1 and $\vec n$ with the plane through line 2 and $\vec n$.

Plane 1: normal $\vec d_1\times\vec n = (2,3,4)\times(-1,2,-1) = (-3-8,\ -4+2,\ 4+3) = (-11,-2,7)$; through $A(1,2,3)$: $-11(x-1) - 2(y-2) + 7(z-3) = 0\Rightarrow11x + 2y - 7z + 6 = 0$.

Plane 2: normal $\vec d_2\times\vec n = (3,4,5)\times(-1,2,-1) = (-4-10,\ -5+3,\ 6+4) = (-14,-2,10)$; through $B(2,4,5)$: $-14(x-2) - 2(y-4) + 10(z-5) = 0\Rightarrow7x + y - 5z + 7 = 0$.
$$\boxed{11x + 2y - 7z + 6 = 0,\qquad7x + y - 5z + 7 = 0}$$
(Check: at $A$: $11 + 4 - 21 + 6 = 0$ ✓; at $B$: $14 + 4 - 25 + 7 = 0$ ✓.)

@s 7
**Cross-section.** The intersection of a sphere and a plane is a **circle** (a point if the plane is tangent, empty if it does not meet the sphere). **Infinitely many** spheres pass through a given circle: the family $S + \lambda P = 0$ ($\lambda$ a parameter), where $S = 0$ is a sphere and $P = 0$ is the plane of the circle.

**The circle.** Sphere $S$: $x^2 + y^2 + z^2 + x + y + z - 4 = 0$, centre $C = \left(-\dfrac12,-\dfrac12,-\dfrac12\right)$, radius
$$R = \sqrt{\frac14 + \frac14 + \frac14 + 4} = \sqrt{\frac{19}4}$$
Plane $x + y + z = 0$. Distance from $C$ to the plane:
$$\begin{gathered}d = \frac{|-\frac12 - \frac12 - \frac12|}{\sqrt3} = \frac{3/2}{\sqrt3} = \frac{\sqrt3}2 \\ d^2 = \frac34\end{gathered}$$
The centre of the circle is the foot of the perpendicular from $C$ to the plane: $C + t(1,1,1)$ with coordinate sum zero: $-\dfrac32 + 3t = 0$, $t = \dfrac12$, giving $(0,0,0)$.
$$r = \sqrt{R^2 - d^2} = \sqrt{\frac{19}4 - \frac34} = \sqrt4 = 2$$
$$\boxed{\text{centre }(0,0,0),\quad\text{radius }2}$$
(Check: on the plane $x + y + z = 0$ the sphere reduces to $x^2 + y^2 + z^2 = 4$.)

@s 8
Axis through $A(1,2,3)$ with direction $\vec d = (2,1,2)$, $|\vec d| = 3$. A point $P(x,y,z)$ lies on the right circular cylinder of radius $2$ iff its perpendicular distance from the axis is $2$:
$$\frac{|\overrightarrow{AP}\times\vec d|}{|\vec d|} = 2\ \Rightarrow\ |\overrightarrow{AP}\times\vec d|^2 = 4\cdot9 = 36$$
$\overrightarrow{AP} = (x-1,\ y-2,\ z-3) = (a,b,c)$:
$$\overrightarrow{AP}\times\vec d = (b\cdot2 - c\cdot1,\ c\cdot2 - a\cdot2,\ a\cdot1 - b\cdot2) = (2b - c,\ 2c - 2a,\ a - 2b)$$
$$(2b - c)^2 + (2c - 2a)^2 + (a - 2b)^2 = 36$$
$$\left[2(y-2) - (z-3)\right]^2 + \left[2(z-3) - 2(x-1)\right]^2 + \left[(x-1) - 2(y-2)\right]^2 = 36$$
Expanding and collecting:
$$\boxed{5x^2 + 8y^2 + 5z^2 - 4xy - 4yz - 8zx + 22x - 16y - 14z - 10 = 0}$$
(Check: a point on the axis, $(1,2,3)$, gives $-36$ in the unexpanded form, i.e. distance $0$; the point $(1,2,3) + 2\cdot\frac13(2,-2,-1) = (\tfrac73,\tfrac23,\tfrac73)$, which is at distance $2$ from the axis since $(2,-2,-1)\cdot(2,1,2) = 0$, gives $0$ ✓.)

@s 9
Let $y = \displaystyle\sum_{n=0}^\infty a_nx^n$, $y' = \displaystyle\sum na_nx^{n-1}$, $y'' = \displaystyle\sum(n+2)(n+1)a_{n+2}x^n$. In $y'' + xy' + y = 0$ the term $xy' = \sum na_nx^n$. The coefficient of $x^n$:
$$(n+2)(n+1)a_{n+2} + na_n + a_n = 0\ \Rightarrow\ (n+2)(n+1)a_{n+2} = -(n+1)a_n$$
$$\boxed{a_{n+2} = -\frac{a_n}{n+2}}$$
Even: $a_2 = -\dfrac{a_0}2$, $a_4 = -\dfrac{a_2}4 = \dfrac{a_0}{8}$, $a_6 = -\dfrac{a_4}{6} = -\dfrac{a_0}{48}$.

Odd: $a_3 = -\dfrac{a_1}3$, $a_5 = -\dfrac{a_3}{5} = \dfrac{a_1}{15}$, $a_7 = -\dfrac{a_5}7 = -\dfrac{a_1}{105}$.
$$\boxed{y = a_0\left(1 - \frac{x^2}2 + \frac{x^4}{8} - \frac{x^6}{48} + \cdots\right) + a_1\left(x - \frac{x^3}{3} + \frac{x^5}{15} - \frac{x^7}{105} + \cdots\right)}$$
with $a_0, a_1$ arbitrary constants. The first series is $e^{-x^2/2}$: indeed $y = e^{-x^2/2}$ satisfies $y' = -xy$, $y'' = (x^2 - 1)y$, so $y'' + xy' + y = (x^2 - 1 - x^2 + 1)y = 0$ ✓.

@s 10
$P_0 = 1,\ P_1 = x,\ P_2 = \tfrac12(3x^2 - 1),\ P_3 = \tfrac12(5x^3 - 3x)$. Hence
$$\begin{gathered}x^3 = \frac{2P_3 + 3P_1}{5} \\ x^2 = \frac{2P_2 + P_0}{3} \\ x = P_1 \\ 1 = P_0\end{gathered}$$
$$f = x^3 - 5x^2 + 6x + 1 = \frac{2P_3 + 3P_1}5 - \frac{5(2P_2 + P_0)}{3} + 6P_1 + P_0$$
Collecting like terms:
$$\begin{gathered}P_3:\ \tfrac25; \\ P_2:\ -\tfrac{10}3; \\ P_1:\ \tfrac35 + 6 = \tfrac{33}5; \\ P_0:\ -\tfrac53 + 1 = -\tfrac23\end{gathered}$$
$$\boxed{x^3 - 5x^2 + 6x + 1 = \frac25P_3(x) - \frac{10}{3}P_2(x) + \frac{33}{5}P_1(x) - \frac23P_0(x)}$$
Check at $x = 1$: $\dfrac25 - \dfrac{10}3 + \dfrac{33}5 - \dfrac23 = \dfrac{6 - 50 + 99 - 10}{15} = 3$, and $f(1) = 1 - 5 + 6 + 1 = 3$ ✓.

@s 11
$J_n(x) = \displaystyle\sum_{r=0}^\infty\frac{(-1)^r}{r!\,\Gamma(n+r+1)}\left(\frac x2\right)^{n+2r}$. Differentiate:
$$J_n'(x) = \sum_{r=0}^\infty\frac{(-1)^r(n+2r)}{r!\,\Gamma(n+r+1)}\frac{1}{2}\left(\frac x2\right)^{n+2r-1}$$
Multiply by $x$ (note $x\cdot\dfrac12\left(\dfrac x2\right)^{n+2r-1} = \left(\dfrac x2\right)^{n+2r}$):
$$xJ_n'(x) = \sum_{r=0}^\infty\frac{(-1)^r(n+2r)}{r!\,\Gamma(n+r+1)}\left(\frac x2\right)^{n+2r}$$
Split $n + 2r = n + 2r$:
$$xJ_n' = nJ_n + \sum_{r=1}^\infty\frac{(-1)^r\,2r}{r!\,\Gamma(n+r+1)}\left(\frac x2\right)^{n+2r} = nJ_n + 2\sum_{r=1}^\infty\frac{(-1)^r}{(r-1)!\,\Gamma(n+r+1)}\left(\frac x2\right)^{n+2r}$$
Put $s = r - 1$:
$$2\sum_{s=0}^\infty\frac{(-1)^{s+1}}{s!\,\Gamma(n+s+2)}\left(\frac x2\right)^{n+2s+2} = -x\sum_{s=0}^\infty\frac{(-1)^s}{s!\,\Gamma(n+1+s+1)}\left(\frac x2\right)^{n+1+2s} = -xJ_{n+1}(x)$$
$$\boxed{xJ_n'(x) = nJ_n(x) - xJ_{n+1}(x)}$$
$\blacksquare$

@s 12
Let $\vec a = (2,3,-1)$, $\vec b = (-1,2,-3)$, $\vec c = (3,-4,2)$. The reciprocal system is
$$\begin{gathered}\vec a' = \frac{\vec b\times\vec c}{[\vec a\,\vec b\,\vec c]} \\ \vec b' = \frac{\vec c\times\vec a}{[\vec a\,\vec b\,\vec c]} \\ \vec c' = \frac{\vec a\times\vec b}{[\vec a\,\vec b\,\vec c]}\end{gathered}$$
$$\vec b\times\vec c = \begin{vmatrix}\hat i&\hat j&\hat k\\-1&2&-3\\3&-4&2\end{vmatrix} = (4 - 12)\hat i - (-2 + 9)\hat j + (4 - 6)\hat k = (-8,-7,-2)$$
$$[\vec a\,\vec b\,\vec c] = \vec a\cdot(\vec b\times\vec c) = -16 - 21 + 2 = -35$$
$$\vec c\times\vec a = \begin{vmatrix}\hat i&\hat j&\hat k\\3&-4&2\\2&3&-1\end{vmatrix} = (4 - 6)\hat i - (-3 - 4)\hat j + (9 + 8)\hat k = (-2,7,17)$$
$$\vec a\times\vec b = \begin{vmatrix}\hat i&\hat j&\hat k\\2&3&-1\\-1&2&-3\end{vmatrix} = (-9 + 2)\hat i - (-6 - 1)\hat j + (4 + 3)\hat k = (-7,7,7)$$
$$\boxed{\begin{gathered}\vec a' = \frac{1}{35}(8\hat i + 7\hat j + 2\hat k) \\ \vec b' = \frac1{35}(2\hat i - 7\hat j - 17\hat k) \\ \vec c' = \frac15(\hat i - \hat j - \hat k)\end{gathered}}$$
**Check:** $\vec a\cdot\vec a' = \dfrac{16 + 21 - 2}{35} = 1$, $\vec a\cdot\vec b' = \dfrac{4 - 21 + 17}{35} = 0$, $\vec b\cdot\vec b' = \dfrac{-2 - 14 + 51}{35} = 1$, $\vec c\cdot\vec c' = \dfrac{3 + 4 - 2}{5} = 1$ ✓.

@s 13
Let $\vec a(t)$ be a differentiable vector function of the scalar $t$ with magnitude $a = |\vec a|$.

**Necessary.** If $|\vec a|$ is constant, then $\vec a\cdot\vec a = a^2$ is constant, so differentiating
$$\frac{d}{dt}(\vec a\cdot\vec a) = 2\,\vec a\cdot\frac{d\vec a}{dt} = 0\ \Rightarrow\ \vec a\cdot\frac{d\vec a}{dt} = 0$$
**Sufficient.** If $\vec a\cdot\dfrac{d\vec a}{dt} = 0$, then $\dfrac{d}{dt}|\vec a|^2 = 2\vec a\cdot\dfrac{d\vec a}{dt} = 0$, so $|\vec a|^2$, hence $|\vec a|$, is constant. $\blacksquare$

The result means that a vector of constant length changes only in direction, and its derivative is perpendicular to it (or zero), e.g. $\vec r = (R\cos\omega t, R\sin\omega t)$ with $\vec r\cdot\dot{\vec r} = 0$.

@s 14
The angle between two surfaces at a point is the angle between their normals there, i.e. between the gradients.

Surface 1: $f = xy^2z - 3x - z^2$, $\nabla f = (y^2z - 3,\ 2xyz,\ xy^2 - 2z)$. At $(1,-2,1)$ (which satisfies $4 = 3 + 1$ ✓):
$$\begin{gathered}\vec n_1 = (4 - 3,\ 2(1)(-2)(1),\ 4 - 2) = (1,-4,2) \\ |\vec n_1| = \sqrt{21}\end{gathered}$$
Surface 2: $g = 3x^2 - y^2 + 2z - 1$, $\nabla g = (6x,\ -2y,\ 2)$. At the point ($3 - 4 + 2 = 1$ ✓):
$$\begin{gathered}\vec n_2 = (6,4,2) \\ |\vec n_2| = \sqrt{56}\end{gathered}$$
$$\vec n_1\cdot\vec n_2 = 6 - 16 + 4 = -6$$
$$\cos\theta = \frac{|\vec n_1\cdot\vec n_2|}{|\vec n_1||\vec n_2|} = \frac{6}{\sqrt{21\cdot56}} = \frac{6}{\sqrt{1176}} = \frac{3}{7\sqrt6}\approx0.1750$$
$$\boxed{\theta = \cos^{-1}\!\left(\frac{3}{7\sqrt6}\right)\approx79.9^\circ}$$

@s 15
The series is $\displaystyle\sum_{n=1}^\infty\frac{x^n}{n(n+1)}$, with $u_n = \dfrac{x^n}{n(n+1)}$.
$$\frac{u_{n+1}}{u_n} = \frac{x^{n+1}}{(n+1)(n+2)}\cdot\frac{n(n+1)}{x^n} = \frac{nx}{n+2}\ \to\ x$$
By the ratio test the series **converges for $x<1$** and **diverges for $x>1$**.

At $x = 1$: $u_n = \dfrac{1}{n(n+1)} = \dfrac1n - \dfrac1{n+1}$, so the partial sum $S_N = 1 - \dfrac1{N+1}\to1$: the series **converges** (also by comparison with $\sum\dfrac1{n^2}$).
$$\boxed{\text{Convergent for }0<x\le1;\ \text{divergent for }x>1}$$

@s 16
$$\sum_{n=1}^\infty\frac{(-1)^n(x+1)^n}{2^n} = \sum_{n=1}^\infty\left(-\frac{x+1}{2}\right)^n$$
This is a geometric series with ratio $\rho = -\dfrac{x+1}2$; it converges iff $|\rho|<1$:
$$\left|\frac{x+1}{2}\right|<1\ \Rightarrow\ |x + 1|<2\ \Rightarrow\ -3<x<1$$
Radius by the ratio test: $\left|\dfrac{a_{n+1}}{a_n}\right| = \dfrac12\Rightarrow R = 2$ (centre $x = -1$).

**Endpoints.** $x = 1$: the series is $\sum(-1)^n\cdot1 = -1 + 1 - 1 + \cdots$, whose terms do not tend to $0$ (diverges). $x = -3$: the series is $\sum(1)^n = 1 + 1 + \cdots$ (diverges).
$$\boxed{R = 2,\qquad\text{interval of convergence }-3<x<1}$$
(Its sum inside the interval is $\dfrac{\rho}{1 - \rho} = -\dfrac{x+1}{x+3}$.)

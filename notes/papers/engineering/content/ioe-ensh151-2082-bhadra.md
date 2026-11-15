---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-ENSH151-2082-Bhadra.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: ENSH 151
year_bs: 2082 Bhadra
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
(a) Show that $x\dfrac{\partial u}{\partial x} + y\dfrac{\partial u}{\partial y} = \sin 2u$, where $u = \tan^{-1}\left(\dfrac{x^3 + y^3}{x - y}\right)$. [[2]]
(b) If $x = r\cos\theta,\ y = r\sin\theta$, then find $\dfrac{\partial(x,y)}{\partial(r,\theta)}$. [[2]]

@q 2
(a) Find the moment about the $x$-axis of the lamina bounded by $y = x$ and $y = x^2$ with density $\rho(x,y) = 1$. [[2]]
(b) Find the area of the region bounded by the curves $x = y^2$ and $x = 2y - y^2$. [[2]]

@q 3
(a) A particle moves along the curve $x = 3\cos t,\ y = 3\sin t,\ z = 6t$. Find the velocity and acceleration at time $t = \dfrac\pi3$. [[2]]
(b) If $\vec F = \operatorname{grad}(x^3 + y^3 + z^3 - 3xyz)$, then find $\operatorname{div}\vec F$. [[2]]
(c) Find the work done by the force $\vec F = x^2\vec i - xy\vec j$ along the path $C$ given by $x^2 + y^2 = 1,\ z = 0$. [[2]]

@q 4
(a) State the existence conditions of the Laplace transform. Obtain the Laplace transform of $t\sin3t$. [[2]]
(b) Find the inverse Laplace transform of $F(s) = \cot^{-1}(s+1)$. [[2]]

@q 5
(a) Find the rank of the matrix $\begin{pmatrix}1 & 2 & -1 & 3\\ 2 & 4 & 1 & -2\\ 3 & 6 & 3 & -7\end{pmatrix}$. [[2]]
(b) Reduce the quadratic form $Q(X) = 17x_1^2 - 30x_1x_2 + 17x_2^2$ into canonical form. [[2]]

@q 6
Express the function $f(x) = 4 + 2x + x^2$ in terms of Legendre's polynomials. [[2]]

@q 7
Find the extreme values of the function $x^2 + y^2 + z^2$ subject to the condition $x + y + z = 1$. [[4]]

@q 8
Change the order of integration and evaluate $\displaystyle\int_0^1\int_{x^2}^{2-x}xy\,dy\,dx$. [[4]]

@q 9
Prove that the necessary and sufficient condition for a vector function $\vec a$ of a scalar variable $t$ to have constant direction is $\vec a\times\dfrac{d\vec a}{dt} = \vec0$. [[4]]

@q 10
State Green's theorem in the plane and, using it, find the area of the hypocycloid $\left(\dfrac xa\right)^{2/3} + \left(\dfrac yb\right)^{2/3} = 1$. [[4]]

@q 11
Use the Gauss divergence theorem to evaluate $\displaystyle\iint_S\vec F\cdot\hat n\,ds$, where $\vec F = (x^2 - yz)\vec i + (y^2 - zx)\vec j + (z^2 - xy)\vec k$ and $S$ is the surface of the parallelepiped bounded by $x = 0,\ x = a,\ y = 0,\ y = b$ and $z = 0,\ z = c$. [[4]]
@or
Apply Stokes' theorem to evaluate $\displaystyle\oint_C(x + y)\,dx + (2x - z)\,dy + (y + z)\,dz$, where $C$ is the boundary of the triangle with vertices $(2,0,0),\ (0,3,0)$ and $(0,0,6)$. [[4]]

@q 12
Using the Laplace transform, solve the initial value problem $x'' - 3x' + 2x = e^{-t}$, $x(0) = 0$, $x'(0) = 1$. [[4]]

@q 13
Apply the Cayley–Hamilton theorem to find the inverse of the matrix $\begin{pmatrix}1 & 0 & 1\\ 1 & 1 & 0\\ 1 & 0 & 2\end{pmatrix}$. [[4]]

@q 14
Diagonalize the matrix $\begin{pmatrix}1 & 4\\ 3 & 2\end{pmatrix}$. [[4]]

@q 15
Solve the differential equation $y'' + xy' + y = 0$ by using the power series method. [[4]]
@or
Prove that $J_{5/2}(x) = \sqrt{\dfrac{2}{\pi x}}\left\{\dfrac{3 - x^2}{x^2}\sin x - \dfrac3x\cos x\right\}$, where the symbols have their usual meanings. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** $f = \tan u = \dfrac{x^3 + y^3}{x - y}$ is homogeneous of degree $3 - 1 = 2$. By Euler's theorem $xf_x + yf_y = 2f$, i.e. $\sec^2u\,(xu_x + yu_y) = 2\tan u$, so
$$x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = 2\sin u\cos u = \sin2u$$

**(b)** $\dfrac{\partial(x,y)}{\partial(r,\theta)} = \begin{vmatrix}\cos\theta & -r\sin\theta\\ \sin\theta & r\cos\theta\end{vmatrix} = r\cos^2\theta + r\sin^2\theta = \boxed{r}$.

@s 2
**(a)** The curves meet at $x = 0$ and $x = 1$, with $x^2\le y\le x$. The moment about the $x$-axis is
$$M_x = \iint y\rho\,dA = \int_0^1\int_{x^2}^x y\,dy\,dx = \int_0^1\frac{x^2 - x^4}{2}\,dx = \frac12\left(\frac13 - \frac15\right) = \boxed{\frac1{15}}$$

**(b)** The curves meet where $y^2 = 2y - y^2$, i.e. $y = 0$ and $y = 1$, and for $0<y<1$ we have $y^2 < 2y - y^2$. Integrating with respect to $x$ first,
$$A = \int_0^1\left[(2y - y^2) - y^2\right]dy = \left[y^2 - \frac{2y^3}{3}\right]_0^1 = \boxed{\frac13}\ \text{square units}$$

@s 3
**(a)** $\vec r = (3\cos t, 3\sin t, 6t)$. $\vec v = (-3\sin t, 3\cos t, 6)$; at $t = \tfrac\pi3$: $\vec v = -\tfrac{3\sqrt3}{2}\vec i + \tfrac32\vec j + 6\vec k$, speed $\sqrt{9 + 36} = 3\sqrt5$. $\vec a = (-3\cos t, -3\sin t, 0)$; at $t = \tfrac\pi3$: $\vec a = -\tfrac32\vec i - \tfrac{3\sqrt3}{2}\vec j$, magnitude $3$.

**(b)** $\vec F = \nabla\phi = (3x^2 - 3yz,\ 3y^2 - 3xz,\ 3z^2 - 3xy)$, so
$$\operatorname{div}\vec F = 6x + 6y + 6z = \boxed{6(x + y + z)}$$

**(c)** $W = \oint_C\vec F\cdot d\vec r = \oint_Cx^2\,dx - xy\,dy$. By Green's theorem ($C$ traversed counter-clockwise), $W = \iint_D\left(\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y}\right)dA = \iint_D(-y - 0)\,dA = 0$ since the unit disc is symmetric about the $x$-axis. Directly, $x = \cos t,\ y = \sin t$: $W = \int_0^{2\pi}\left(-\cos^2t\sin t - \cos t\sin t\cos t\right)dt = -2\int_0^{2\pi}\cos^2t\sin t\,dt = \boxed{0}$.

@s 4
**(a)** *Existence:* $\mathcal L\{f\}$ exists if $f(t)$ is piecewise continuous on every finite interval $[0, b]$ and of exponential order, i.e. $|f(t)|\le Me^{at}$ for $t\ge T$ (these conditions are sufficient). Since $\mathcal L\{\sin3t\} = \dfrac{3}{s^2 + 9}$ and $\mathcal L\{tf(t)\} = -\dfrac{d}{ds}F(s)$,
$$\mathcal L\{t\sin3t\} = -\frac{d}{ds}\left(\frac{3}{s^2 + 9}\right) = \boxed{\frac{6s}{(s^2 + 9)^2}}$$

**(b)** Let $F(s) = \cot^{-1}(s+1)$. Then $F'(s) = -\dfrac{1}{1 + (s+1)^2}$ and $\mathcal L^{-1}\{F'(s)\} = -e^{-t}\sin t$. Since $\mathcal L^{-1}\{F'(s)\} = -t f(t)$,
$$t f(t) = e^{-t}\sin t \;\Rightarrow\; \boxed{f(t) = \frac{e^{-t}\sin t}{t}}$$

@s 5
**(a)** $R_2\to R_2 - 2R_1$ and $R_3\to R_3 - 3R_1$:
$$\begin{pmatrix}1 & 2 & -1 & 3\\ 0 & 0 & 3 & -8\\ 0 & 0 & 6 & -16\end{pmatrix}\xrightarrow{R_3 - 2R_2}\begin{pmatrix}1 & 2 & -1 & 3\\ 0 & 0 & 3 & -8\\ 0 & 0 & 0 & 0\end{pmatrix}\quad\Rightarrow\quad\boxed{\text{rank} = 2}$$

**(b)** The matrix of $Q$ is $A = \begin{pmatrix}17 & -15\\ -15 & 17\end{pmatrix}$. $|A - \lambda I| = (17 - \lambda)^2 - 225 = 0 \Rightarrow \lambda = 17\pm15 = 2,\ 32$. Eigenvectors: $\lambda = 2$: $(1, 1)$; $\lambda = 32$: $(1, -1)$ (orthogonal). With $x_1 = \dfrac{y_1 + y_2}{\sqrt2},\ x_2 = \dfrac{y_1 - y_2}{\sqrt2}$,
$$\boxed{Q = 2y_1^2 + 32y_2^2}$$
(positive definite, rank 2).

@s 6
Using $x^2 = \tfrac13(2P_2 + P_0)$ and $x = P_1$:
$$4 + 2x + x^2 = 4P_0 + 2P_1 + \tfrac23P_2 + \tfrac13P_0 = \boxed{\tfrac{13}{3}P_0(x) + 2P_1(x) + \tfrac23P_2(x)}$$
Check at $x = 1$: $\tfrac{13}{3} + 2 + \tfrac23 = 7 = 4 + 2 + 1$ ✓.

@s 7
Let $f = x^2 + y^2 + z^2$, $g = x + y + z - 1$. From $F = f - \lambda g$: $2x = \lambda,\ 2y = \lambda,\ 2z = \lambda$, so $x = y = z$. The constraint gives $3x = 1$, so $x = y = z = \dfrac13$ and $\lambda = \dfrac23$.
$$f\left(\tfrac13, \tfrac13, \tfrac13\right) = 3\cdot\frac19 = \boxed{\frac13}$$
This is the **minimum** value (it is the squared distance from the origin to the plane $x + y + z = 1$, namely $(1/\sqrt3)^2$); the function has no maximum on the plane since $x^2 + y^2 + z^2\to\infty$.

@s 8
The region is $0\le x\le1,\ x^2\le y\le2 - x$, bounded by the parabola $y = x^2$ (i.e. $x = \sqrt y$), the line $y = 2 - x$ (i.e. $x = 2 - y$) and the $y$-axis. They meet at $(1, 1)$. Reversing the order, split at $y = 1$:

- $0\le y\le1$: $x$ from $0$ to $\sqrt y$,
- $1\le y\le2$: $x$ from $0$ to $2 - y$.

$$I = \int_0^1y\cdot\frac{y}{2}\,dy + \int_1^2y\cdot\frac{(2-y)^2}{2}\,dy = \frac16 + \frac12\left[2y^2 - \frac{4y^3}{3} + \frac{y^4}{4}\right]_1^2 = \frac16 + \frac12\left(\frac43 - \frac{11}{12}\right) = \frac16 + \frac5{24}$$
$$\boxed{I = \frac38}$$
Check in the original order: $\displaystyle\int_0^1x\,\frac{(2-x)^2 - x^4}{2}\,dx = \frac12\left(2 - \frac43 + \frac14 - \frac16\right) = \frac38$ ✓.

@s 9
Write $\vec a = a\hat e$ with $a = |\vec a|$. Then $\vec a\times\dfrac{d\vec a}{dt} = a^2\left(\hat e\times\dfrac{d\hat e}{dt}\right)$ (the term with $\hat e\times\hat e$ vanishes).

*Necessary:* constant direction means $\hat e$ is constant, so $\dfrac{d\hat e}{dt} = \vec 0$ and the cross product is $\vec 0$.

*Sufficient:* if $\vec a\times\dfrac{d\vec a}{dt} = \vec0$ (with $a\ne0$) then $\hat e\times\dfrac{d\hat e}{dt} = \vec0$, so $\dfrac{d\hat e}{dt}\parallel\hat e$. But $\hat e\cdot\hat e = 1$ gives $\hat e\cdot\dfrac{d\hat e}{dt} = 0$, so $\dfrac{d\hat e}{dt}\perp\hat e$. Hence $\dfrac{d\hat e}{dt} = \vec 0$ and $\hat e$ is constant. $\blacksquare$

@s 10
**Green's theorem.** If $P(x,y), Q(x,y)$ have continuous first partial derivatives on a region $R$ bounded by a piecewise smooth simple closed curve $C$ traversed counter-clockwise, then
$$\oint_C(P\,dx + Q\,dy) = \iint_R\left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dx\,dy$$
Taking $P = -y,\ Q = x$ gives $A = \dfrac12\oint_C(x\,dy - y\,dx)$.

For the hypocycloid, $x = a\cos^3t,\ y = b\sin^3t$, $0\le t\le2\pi$: $dx = -3a\cos^2t\sin t\,dt$, $dy = 3b\sin^2t\cos t\,dt$, so $x\,dy - y\,dx = 3ab\sin^2t\cos^2t\,dt$.
$$A = \frac{3ab}{2}\int_0^{2\pi}\sin^2t\cos^2t\,dt = \frac{3ab}{2}\cdot\frac\pi4 = \boxed{\frac{3\pi ab}{8}}$$
(For $a = b$ this is the astroid area $\tfrac38\pi a^2$.)

@s 11
$\nabla\cdot\vec F = 2x + 2y + 2z$. By the divergence theorem, over the box $0\le x\le a,\ 0\le y\le b,\ 0\le z\le c$:
$$\iint_S\vec F\cdot\hat n\,dS = 2\int_0^a\int_0^b\int_0^c(x + y + z)\,dz\,dy\,dx = 2\left[\frac{a^2}{2}bc + \frac{b^2}{2}ac + \frac{c^2}{2}ab\right]$$
$$\boxed{= abc\,(a + b + c)}$$

**OR.** The triangle lies in the plane $\dfrac x2 + \dfrac y3 + \dfrac z6 = 1$, i.e. $3x + 2y + z = 6$. For $\vec F = (x + y,\ 2x - z,\ y + z)$,
$$\nabla\times\vec F = \begin{vmatrix}\vec i & \vec j & \vec k\\ \partial_x & \partial_y & \partial_z\\ x + y & 2x - z & y + z\end{vmatrix} = (1 + 1)\vec i + (0 - 0)\vec j + (2 - 1)\vec k = (2, 0, 1)$$
Taking the upward normal ($C$ counter-clockwise seen from above), $\hat n\,dS = (3, 2, 1)\,dx\,dy$ for the plane $z = 6 - 3x - 2y$. The projection on the $xy$-plane is the triangle $(0,0), (2,0), (0,3)$ of area $3$:
$$\oint_C\vec F\cdot d\vec r = \iint_D(2, 0, 1)\cdot(3, 2, 1)\,dx\,dy = 7\times3 = \boxed{21}$$

@s 12
Transform: $s^2X - sx(0) - x'(0) - 3\left[sX - x(0)\right] + 2X = \dfrac{1}{s+1}$, so $(s^2 - 3s + 2)X = 1 + \dfrac1{s+1} = \dfrac{s+2}{s+1}$:
$$X = \frac{s+2}{(s+1)(s-1)(s-2)} = \frac{1/6}{s+1} - \frac{3/2}{s-1} + \frac{4/3}{s-2}$$
(residues: at $s = -1$: $\dfrac{1}{(-2)(-3)} = \dfrac16$; at $s = 1$: $\dfrac{3}{2\cdot(-1)} = -\dfrac32$; at $s = 2$: $\dfrac{4}{3\cdot1} = \dfrac43$.)
$$\boxed{x(t) = \frac16e^{-t} - \frac32e^{t} + \frac43e^{2t}}$$
Check: $x(0) = \tfrac16 - \tfrac32 + \tfrac43 = 0$ ✓, $x'(0) = -\tfrac16 - \tfrac32 + \tfrac83 = 1$ ✓.

@s 13
$A = \begin{pmatrix}1 & 0 & 1\\ 1 & 1 & 0\\ 1 & 0 & 2\end{pmatrix}$. Characteristic equation: expanding $|A - \lambda I|$ along the second column, $|A - \lambda I| = (1-\lambda)\left[(1-\lambda)(2-\lambda) - 1\right] = (1-\lambda)(\lambda^2 - 3\lambda + 1)$, i.e.
$$\lambda^3 - 4\lambda^2 + 4\lambda - 1 = 0$$
(trace $= 4$, sum of principal minors $= 1 + 1 + 2 = 4$, $\det A = 1$.) By Cayley–Hamilton, $A^3 - 4A^2 + 4A - I = 0$. Multiply by $A^{-1}$: $A^2 - 4A + 4I - A^{-1} = 0$, so $A^{-1} = A^2 - 4A + 4I$.
$$A^2 = \begin{pmatrix}2 & 0 & 3\\ 2 & 1 & 1\\ 3 & 0 & 5\end{pmatrix},\qquad A^{-1} = \begin{pmatrix}2 - 4 + 4 & 0 & 3 - 4\\ 2 - 4 & 1 - 4 + 4 & 1\\ 3 - 4 & 0 & 5 - 8 + 4\end{pmatrix}$$
$$\boxed{A^{-1} = \begin{pmatrix}2 & 0 & -1\\ -2 & 1 & 1\\ -1 & 0 & 1\end{pmatrix}}$$
Check: first row of $A$ times first column of $A^{-1}$: $1\cdot2 + 0 + 1\cdot(-1) = 1$ ✓.

@s 14
$A = \begin{pmatrix}1 & 4\\ 3 & 2\end{pmatrix}$: $\lambda^2 - 3\lambda - 10 = 0 \Rightarrow \lambda = 5,\ -2$.
- $\lambda = 5$: $-4x + 4y = 0$, eigenvector $(1, 1)^T$.
- $\lambda = -2$: $3x + 4y = 0$, eigenvector $(4, -3)^T$.

With $P = \begin{pmatrix}1 & 4\\ 1 & -3\end{pmatrix}$, $\det P = -7$, $P^{-1} = \dfrac17\begin{pmatrix}3 & 4\\ 1 & -1\end{pmatrix}$:
$$P^{-1}AP = \frac17\begin{pmatrix}3 & 4\\ 1 & -1\end{pmatrix}\begin{pmatrix}5 & -8\\ 5 & 6\end{pmatrix} = \frac17\begin{pmatrix}35 & 0\\ 0 & -14\end{pmatrix} = \boxed{\begin{pmatrix}5 & 0\\ 0 & -2\end{pmatrix}}$$

@s 15
Let $y = \sum a_nx^n$. Then $y'' = \sum(n+2)(n+1)a_{n+2}x^n$, $xy' = \sum na_nx^n$. Coefficient of $x^n$: $(n+2)(n+1)a_{n+2} + (n+1)a_n = 0$, so
$$a_{n+2} = -\frac{a_n}{n+2}$$
Even terms: $a_2 = -\dfrac{a_0}{2},\ a_4 = \dfrac{a_0}{2\cdot4},\ a_6 = -\dfrac{a_0}{2\cdot4\cdot6}$, i.e. $a_{2k} = \dfrac{(-1)^ka_0}{2^kk!}$, which sums to $a_0e^{-x^2/2}$.
Odd terms: $a_3 = -\dfrac{a_1}{3},\ a_5 = \dfrac{a_1}{3\cdot5},\ a_7 = -\dfrac{a_1}{3\cdot5\cdot7}$.
$$\boxed{y = a_0\left(1 - \frac{x^2}{2} + \frac{x^4}{8} - \cdots\right) + a_1\left(x - \frac{x^3}{3} + \frac{x^5}{15} - \frac{x^7}{105} + \cdots\right) = a_0e^{-x^2/2} + a_1\left(x - \frac{x^3}{3} + \frac{x^5}{15} - \cdots\right)}$$

**OR.** From the series $J_n(x) = \sum_{r\ge0}\dfrac{(-1)^r}{r!\,\Gamma(n + r + 1)}\left(\dfrac x2\right)^{2r + n}$ with $n = \tfrac12$ and $\Gamma(r + \tfrac32) = \dfrac{(2r+2)!\sqrt\pi}{4^{r+1}(r+1)!}$, one gets
$$J_{1/2}(x) = \sqrt{\frac{2}{\pi x}}\sin x,\qquad J_{-1/2}(x) = \sqrt{\frac{2}{\pi x}}\cos x$$
The recurrence relation is $J_{n+1}(x) = \dfrac{2n}{x}J_n(x) - J_{n-1}(x)$. With $n = \tfrac12$:
$$J_{3/2} = \frac1xJ_{1/2} - J_{-1/2} = \sqrt{\frac{2}{\pi x}}\left(\frac{\sin x}{x} - \cos x\right)$$
With $n = \tfrac32$:
$$J_{5/2} = \frac3xJ_{3/2} - J_{1/2} = \sqrt{\frac{2}{\pi x}}\left[\frac{3\sin x}{x^2} - \frac{3\cos x}{x} - \sin x\right] = \sqrt{\frac{2}{\pi x}}\left\{\frac{3 - x^2}{x^2}\sin x - \frac3x\cos x\right\}\qquad\blacksquare$$

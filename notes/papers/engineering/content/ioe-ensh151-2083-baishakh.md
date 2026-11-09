---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-ENSH151-2083-Baishakh.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: ENSH 151
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: All programmes except B.Arch
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

**Group A (12 × 2)**

@q 1
(a) If $u = \sin^{-1}\left(\dfrac{x^2 + y^2}{x + y}\right)$, then show that $x\dfrac{\partial u}{\partial x} + y\dfrac{\partial u}{\partial y} = \tan u$. [[2]]
(b) If $u = xyz,\ v = xy + yz + zx,\ w = x + y + z$, find the Jacobian $\dfrac{\partial(u,v,w)}{\partial(x,y,z)}$. [[2]]

@q 2
(a) Evaluate $\displaystyle\iint\dfrac{1}{x^2 + y^2}\,dx\,dy$ with the limits as printed in the scan: upper limit $2x$, lower limits $1$ and $0$ (the outer upper limit is not legible; see the note in the solution). [[2]]
(b) Find the mass of the solid bounded by $z = 1 - x^2$ and the planes $z = 0,\ y = 1,\ y = -1$ with $\rho(x,y,z) = z(y+2)$. [[2]]

@q 3
(a) Find the directional derivative of $\phi = 4x^2 + 3y - 4z$ at $(1, 2, 1)$ in the direction $2\vec i + 2\vec j + \vec k$. [[2]]
(b) Prove that $\vec F = (y^2 - z^2 + 3yz - 2x)\vec i + (3xz + 2xy)\vec j + (3xy - 2xz + 2z)\vec k$ is solenoidal. [[2]]
(c) Find $\nabla\times(\nabla\phi)$ where $\phi = x^3 + y^3 + z^3 - 3xyz$. [[2]]

@q 4
(a) State the existence criteria of the Laplace transform. Evaluate the Laplace transform of $\dfrac{1 - e^t}{t}$. [[2]]
(b) Find the inverse Laplace transform of $\dfrac{1}{s^2 - 3s + 2}$. [[2]]

@q 5
(a) Find the rank of the matrix $\begin{pmatrix}6 & 1 & 3\\ 4 & 2 & 6\\ 10 & 3 & 9\end{pmatrix}$. [[2]]
(b) Find the eigenvalues of the matrix $A = \begin{pmatrix}3 & 1 & 0\\ 1 & 3 & 0\\ 0 & 0 & 2\end{pmatrix}$. [[2]]

@q 6
Express the function $f(x) = 1 + x - x^2$ in terms of Legendre's polynomials. [[2]]

**Group B (9 × 4)**

@q 7
Find the extreme value of $u(x,y) = x^2 + xy + y^2 + 3z^2$ under the constraint $x + 2y + 4z = 60$. [[4]]

@q 8
Evaluate $\displaystyle\int_0^\infty\int_x^\infty\dfrac{e^{-y}}{y}\,dy\,dx$ by changing the order of integration. [[4]]

@q 9
Prove that the necessary and sufficient condition for a vector function $\vec a$ of a scalar variable $t$ to have constant magnitude is $\vec a\cdot\dfrac{d\vec a}{dt} = 0$. [[4]]

@q 10
State Green's theorem in the plane. Apply it to find the area of the curve $x^{2/3} + y^{2/3} = a^{2/3}$. [[4]]

@q 11
Apply the Gauss divergence theorem to evaluate $\displaystyle\iint_S\vec F\cdot\hat n\,ds$, where $\vec F = (2xy + z)\vec i + y^2\vec j - (x + 3y)\vec k$ and $S$ is the region bounded by the surfaces of the planes $2x + 2y + z = 6,\ x = 0,\ y = 0,\ z = 0$. [[4]]
@or
Apply Stokes' theorem to evaluate the line integral $\oint_C(xy\,dx + xy^2\,dy)$, where $C$ is the boundary of the square in the $xy$-plane with vertices $(-1, 0),\ (1, 0),\ (0, 1)$ and $(0, -1)$. [[4]]

@q 12
Solve the differential equation $y''(t) + 4y'(t) + 4y(t) = e^{-t}$; $y(0) = y'(0) = 0$, using the Laplace transform method. [[4]]

@q 13
Test the consistency of the system of linear equations and find the solution if found consistent: $2x - y + 3z = 8,\ -x + 2y + z = 4,\ 3x + y - 4z = 0$. [[4]]

@q 14
Reduce the quadratic form $Q(X) = 5x_1^2 + 2x_2^2 + 2x_3^2 + 4x_1x_2 + 2x_2x_3 + 4x_1x_3$ into canonical form. [[4]]

@q 15
Solve $y'' - 4xy' + (4x^2 - 2)y = 0$ by the power series method. [[4]]
@or
Prove that $J_{5/2}(x) = \sqrt{\dfrac{2}{\pi x}}\left\{\dfrac{3 - x^2}{x^2}\sin x - \dfrac3x\cos x\right\}$, where the symbols have their usual meanings. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** $f = \sin u = \dfrac{x^2 + y^2}{x + y}$ is homogeneous of degree $n = 1$. Euler: $xf_x + yf_y = f$, i.e. $\cos u\left(xu_x + yu_y\right) = \sin u$:
$$x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = \frac{\sin u}{\cos u} = \tan u$$

**(b)** $\dfrac{\partial(u,v,w)}{\partial(x,y,z)} = \begin{vmatrix}yz & xz & xy\\ y+z & x+z & x+y\\ 1 & 1 & 1\end{vmatrix}$. Apply $C_1\to C_1 - C_2$ and $C_2\to C_2 - C_3$:
$$= \begin{vmatrix}z(y - x) & x(z - y) & xy\\ y - x & z - y & x + y\\ 0 & 0 & 1\end{vmatrix}$$
Expanding along the last row: $J = z(y-x)(z-y) - x(z-y)(y-x) = (y - x)(z - y)(z - x)$. Hence
$$\boxed{J = (x - y)(y - z)(z - x)}$$

@s 2
**(a)** *Note on the scan:* only the inner upper limit $2x$ and the lower limits $1$ and $0$ can be read. Since the inner upper limit contains $x$, the inner integral is in $y$ and the integral is taken as $\displaystyle\int_{x=1}^{2}\int_{y=0}^{2x}\dfrac{dy\,dx}{x^2 + y^2}$ (outer upper limit read as $2$). Inner integral:
$$\int_0^{2x}\frac{dy}{x^2 + y^2} = \frac1x\tan^{-1}\frac yx\Big|_0^{2x} = \frac{\tan^{-1}2}{x}$$
$$I = \tan^{-1}2\int_1^2\frac{dx}{x} = \boxed{\tan^{-1}(2)\,\ln2\approx0.767}$$
(For a general outer upper limit $b$ the value is $\tan^{-1}(2)\ln b$.)

**(b)** $M = \displaystyle\int_{-1}^1\int_{-1}^1\int_0^{1-x^2}z(y+2)\,dz\,dy\,dx = \int_{-1}^{1}\frac{(1-x^2)^2}{2}\,dx\cdot\int_{-1}^1(y+2)\,dy = \frac{1}{2}\cdot\frac{16}{15}\cdot4 = \boxed{\frac{32}{15}}$

@s 3
**(a)** $\nabla\phi = (8x, 3, -4) = (8, 3, -4)$ at $(1,2,1)$; $\hat e = \tfrac13(2,2,1)$. $D_{\hat e}\phi = \dfrac{16 + 6 - 4}{3} = \boxed{6}$.

**(b)** $\vec F$ is solenoidal if $\nabla\cdot\vec F = 0$:
$$\frac{\partial}{\partial x}(y^2 - z^2 + 3yz - 2x) + \frac{\partial}{\partial y}(3xz + 2xy) + \frac{\partial}{\partial z}(3xy - 2xz + 2z) = -2 + 2x + (-2x + 2) = 0$$
so $\vec F$ is solenoidal. $\blacksquare$

**(c)** $\nabla\phi = (3x^2 - 3yz,\ 3y^2 - 3xz,\ 3z^2 - 3xy)$. The $\vec i$-component of the curl is $\dfrac{\partial}{\partial y}(3z^2 - 3xy) - \dfrac{\partial}{\partial z}(3y^2 - 3xz) = -3x + 3x = 0$; similarly the other two vanish. $\nabla\times(\nabla\phi) = \boxed{\vec0}$ (the gradient field is irrotational).

@s 4
**(a)** *Existence:* $\mathcal L\{f(t)\}$ exists if $f$ is piecewise continuous on every finite interval $[0, b]$ and of exponential order ($|f(t)|\le Me^{at}$ for large $t$). Then, using $\mathcal L\{f/t\} = \int_s^\infty F(p)\,dp$,
$$\mathcal L\left\{\frac{1 - e^t}{t}\right\} = \int_s^\infty\left(\frac1p - \frac1{p-1}\right)dp = \Big[\ln\frac{p}{p-1}\Big]_s^\infty = \boxed{\ln\frac{s-1}{s}}\quad(s>1)$$

**(b)** $\dfrac{1}{s^2 - 3s + 2} = \dfrac{1}{(s-1)(s-2)} = \dfrac{1}{s-2} - \dfrac{1}{s-1}$, so $\mathcal L^{-1} = \boxed{e^{2t} - e^t}$.

@s 5
**(a)** Row 3 equals Row 1 plus Row 2: $(6 + 4,\ 1 + 2,\ 3 + 6) = (10, 3, 9)$. So $R_3\to R_3 - R_1 - R_2$ gives a zero row. The remaining rows $(6,1,3)$ and $(4,2,6)$ are not proportional (a $2\times2$ minor $\begin{vmatrix}6 & 1\\ 4 & 2\end{vmatrix} = 8\ne0$). $\boxed{\text{rank} = 2}$.

**(b)** $|A - \lambda I| = (2 - \lambda)\begin{vmatrix}3 - \lambda & 1\\ 1 & 3 - \lambda\end{vmatrix} = (2 - \lambda)\left[(3-\lambda)^2 - 1\right] = (2-\lambda)(\lambda - 2)(\lambda - 4)$. Eigenvalues: $\boxed{\lambda = 2, 2, 4}$.

@s 6
With $x^2 = \tfrac13(2P_2 + P_0)$:
$$1 + x - x^2 = P_0 + P_1 - \tfrac23P_2 - \tfrac13P_0 = \boxed{\tfrac23P_0(x) + P_1(x) - \tfrac23P_2(x)}$$
Check at $x = 1$: $\tfrac23 + 1 - \tfrac23 = 1 = 1 + 1 - 1$ ✓.

@s 7
Let $f = x^2 + xy + y^2 + 3z^2$, $g = x + 2y + 4z - 60$. Setting the partial derivatives of $f - \lambda g$ to zero: $2x + y = \lambda,\ x + 2y = 2\lambda,\ 6z = 4\lambda$. From the first two, $3x = 0$, so $x = 0$, $y = \lambda$, $z = \tfrac{2\lambda}{3}$. The constraint: $2\lambda + \tfrac{8\lambda}{3} = 60 \Rightarrow \lambda = \tfrac{90}{7}$. The stationary point is
$$\left(0,\ \frac{90}{7},\ \frac{60}{7}\right),\qquad u = \frac{90^2 + 3\cdot60^2}{49} = \boxed{\frac{2700}{7}\approx385.7}$$
Since $f$ is a positive-definite quadratic form on the constraint plane, this is the **minimum** (there is no maximum).

@s 8
The region is $0\le x\le y<\infty$. Changing the order: $y$ from $0$ to $\infty$, $x$ from $0$ to $y$:
$$I = \int_0^\infty\frac{e^{-y}}{y}\left[\int_0^ydx\right]dy = \int_0^\infty\frac{e^{-y}}{y}\cdot y\,dy = \int_0^\infty e^{-y}\,dy = \boxed{1}$$

@s 9
$|\vec a|^2 = \vec a\cdot\vec a$. Differentiating, $\dfrac{d}{dt}|\vec a|^2 = 2\,\vec a\cdot\dfrac{d\vec a}{dt}$.

*Necessary:* if $|\vec a|$ is constant, $|\vec a|^2$ is constant, so $\dfrac{d}{dt}|\vec a|^2 = 0$, giving $\vec a\cdot\dfrac{d\vec a}{dt} = 0$.

*Sufficient:* if $\vec a\cdot\dfrac{d\vec a}{dt} = 0$ then $\dfrac{d}{dt}|\vec a|^2 = 0$, so $|\vec a|^2$ and hence $|\vec a|$ is constant. $\blacksquare$

@s 10
**Green's theorem.** For $P, Q$ with continuous first partial derivatives on a region $R$ bounded by a piecewise smooth simple closed curve $C$ (counter-clockwise),
$$\oint_C(P\,dx + Q\,dy) = \iint_R\left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dx\,dy$$
Choosing $P = -y$, $Q = x$: $A = \dfrac12\oint_C(x\,dy - y\,dx)$. For the astroid $x = a\cos^3t,\ y = a\sin^3t$: $x\,dy - y\,dx = 3a^2\sin^2t\cos^2t\,dt$, so
$$A = \frac{3a^2}{2}\int_0^{2\pi}\sin^2t\cos^2t\,dt = \frac{3a^2}{2}\cdot\frac\pi4 = \boxed{\frac{3\pi a^2}{8}}$$

@s 11
$\nabla\cdot\vec F = 2y + 2y + 0 = 4y$. The solid is the tetrahedron with vertices $(0,0,0),\ (3,0,0),\ (0,3,0),\ (0,0,6)$: $0\le z\le6 - 2x - 2y$, $0\le y\le3 - x$, $0\le x\le3$.
$$\iint_S\vec F\cdot\hat n\,dS = \int_0^3\int_0^{3-x}\int_0^{6-2x-2y}4y\,dz\,dy\,dx = \int_0^3\int_0^{3-x}8y(3 - x - y)\,dy\,dx$$
With $s = 3 - x$: $\displaystyle\int_0^s8y(s - y)\,dy = 8\left(\frac{s^3}{2} - \frac{s^3}{3}\right) = \frac{4s^3}{3}$, so
$$I = \frac43\int_0^3(3 - x)^3\,dx = \frac43\cdot\frac{81}{4} = \boxed{27}$$

**OR.** For $\vec F = (xy, xy^2, 0)$, $(\nabla\times\vec F)\cdot\hat k = \dfrac{\partial(xy^2)}{\partial x} - \dfrac{\partial(xy)}{\partial y} = y^2 - x$. The square (a diamond) is $|x| + |y|\le1$, traversed counter-clockwise. By Stokes' theorem
$$\oint_C\vec F\cdot d\vec r = \iint_D(y^2 - x)\,dA = \iint_Dy^2\,dA - 0$$
($\iint x\,dA = 0$ by symmetry about the $y$-axis.) In the first quadrant $\displaystyle\int_0^1\int_0^{1-x}y^2\,dy\,dx = \int_0^1\frac{(1-x)^3}{3}dx = \frac1{12}$, and the four quadrants contribute equally:
$$\boxed{\oint_C xy\,dx + xy^2\,dy = \frac{4}{12} = \frac13}$$

@s 12
Transform: $(s^2 + 4s + 4)Y = \dfrac{1}{s+1}$, so
$$Y = \frac{1}{(s+1)(s+2)^2} = \frac{1}{s+1} - \frac{1}{s+2} - \frac{1}{(s+2)^2}$$
(at $s = -1$: $1$; coefficient of $\dfrac{1}{(s+2)^2}$: $\dfrac{1}{s+1}\Big|_{s=-2} = -1$; coefficient of $\dfrac{1}{s+2}$: $\dfrac{d}{ds}\dfrac{1}{s+1}\Big|_{s=-2} = -1$.)
$$\boxed{y(t) = e^{-t} - e^{-2t} - te^{-2t}}$$
Check: $y(0) = 0$ ✓; $y'(0) = -1 + 2 - 1 = 0$ ✓.

@s 13
Augmented matrix $[A\,|\,B]$ with $A = \begin{pmatrix}2 & -1 & 3\\ -1 & 2 & 1\\ 3 & 1 & -4\end{pmatrix}$, $B = (8, 4, 0)^T$. $\det A = 2(-8 - 1) + 1(4 - 3) + 3(-1 - 6) = -18 + 1 - 21 = -38\ne0$, so $\text{rank}(A) = \text{rank}[A|B] = 3 = $ number of unknowns: the system is **consistent with a unique solution**.

Reduce: $R_1\leftrightarrow R_2$ then scale: $\begin{pmatrix}1 & -2 & -1 & -4\\ 2 & -1 & 3 & 8\\ 3 & 1 & -4 & 0\end{pmatrix}\to\begin{pmatrix}1 & -2 & -1 & -4\\ 0 & 3 & 5 & 16\\ 0 & 7 & -1 & 12\end{pmatrix}$. Then $R_3\to3R_3 - 7R_2$: $0\cdot y + (-3 - 35)z = 36 - 112 \Rightarrow -38z = -76$, so $z = 2$. Back-substitute: $3y + 10 = 16 \Rightarrow y = 2$; $x - 4 - 2 = -4 \Rightarrow x = 2$.
$$\boxed{x = y = z = 2}$$
Check: $4 - 2 + 6 = 8$ ✓; $-2 + 4 + 2 = 4$ ✓; $6 + 2 - 8 = 0$ ✓.

@s 14
The symmetric matrix of $Q$ is $A = \begin{pmatrix}5 & 2 & 2\\ 2 & 2 & 1\\ 2 & 1 & 2\end{pmatrix}$. $\lambda^3 - 9\lambda^2 + 15\lambda - 7 = (\lambda - 1)^2(\lambda - 7) = 0$ (trace $9$, sum of principal minors $(10-4)+(10-4)+(4-1) = 15$, $\det A = 7$), so $\lambda = 1, 1, 7$.

- $\lambda = 7$: $-2x + 2y + 2z = 0,\ 2x - 5y + z = 0$ give $(2, 1, 1)^T$.
- $\lambda = 1$: the single equation $2x + y + z = 0$; two independent solutions $(-1, 2, 0)^T$ and $(-1, 0, 2)^T$ (both orthogonal to $(2,1,1)^T$).

Using the normalised eigenvectors as the columns of an orthogonal $P$ and $X = PY$:
$$\boxed{Q = y_1^2 + y_2^2 + 7y_3^2}$$
Rank $3$, positive definite.

@s 15
Put $y = \sum a_nx^n$ in $y'' - 4xy' + (4x^2 - 2)y = 0$. The coefficient of $x^n$ gives $(n+2)(n+1)a_{n+2} - (4n + 2)a_n + 4a_{n-2} = 0$:
$$a_{n+2} = \frac{(4n + 2)a_n - 4a_{n-2}}{(n+1)(n+2)}$$
$a_2 = a_0$, $a_3 = a_1$, $a_4 = \dfrac{10a_2 - 4a_0}{12} = \dfrac{a_0}{2}$, $a_5 = \dfrac{14a_3 - 4a_1}{20} = \dfrac{a_1}{2}$, … These are the coefficients of $e^{x^2}$ and $xe^{x^2}$:
$$\boxed{y = (a_0 + a_1x)\,e^{x^2}}$$
Check: $y = e^{x^2}$ gives $y'' - 4xy' + (4x^2-2)y = (2 + 4x^2 - 8x^2 + 4x^2 - 2)e^{x^2} = 0$ ✓.

**OR.** The Bessel series gives $J_{1/2}(x) = \sqrt{\dfrac{2}{\pi x}}\sin x$ and $J_{-1/2}(x) = \sqrt{\dfrac{2}{\pi x}}\cos x$. The recurrence $J_{n+1} = \dfrac{2n}{x}J_n - J_{n-1}$ gives, for $n = \tfrac12$, $J_{3/2} = \sqrt{\dfrac{2}{\pi x}}\left(\dfrac{\sin x}{x} - \cos x\right)$, and for $n = \tfrac32$,
$$J_{5/2} = \frac3xJ_{3/2} - J_{1/2} = \sqrt{\frac{2}{\pi x}}\left[\frac{3\sin x}{x^2} - \frac{3\cos x}{x} - \sin x\right] = \sqrt{\frac{2}{\pi x}}\left\{\frac{3 - x^2}{x^2}\sin x - \frac3x\cos x\right\}\qquad\blacksquare$$

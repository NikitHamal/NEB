---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-SH151-2081-Ashwin.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: SH 151
year_bs: 2081 Ashwin
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
(a) By using Euler's theorem show that $x\dfrac{\partial u}{\partial x} + y\dfrac{\partial u}{\partial y} = \sin 2u$, where $u = \tan^{-1}(x^2 + 2y^2)$. [[2]]
(b) If $u = x^2$ and $v = y^2$, then find $\dfrac{\partial(u,v)}{\partial(x,y)}$. [[2]]

@q 2
(a) Evaluate $\displaystyle\int_0^1\int_0^z\int_{x-z}^{x+z}(x + y + z)\,dy\,dx\,dz$. [[2]]
(b) Evaluate the mass of the solid region bounded by $z = 1 - x^2$ and the planes $z = 0$, $y = 1$, $y = -1$ with density $\rho(x,y,z) = z(y+2)$. [[2]]

@q 3
(a) Find the directional derivative of $\phi(x,y) = 4x^2 + 3y - 4z$ at $(1, 2, 1)$ in the direction of $2\vec i + 2\vec j + \vec k$. [[2]]
(b) A particle moves along the curve $x = \sqrt2\cos t,\ y = \sqrt2\sin t,\ z = 4t$. Find its velocity and acceleration at time $t = \dfrac\pi4$. [[2]]
(c) If $\phi = x^3 + y^3 + z^3 - 3xyz$, find $\operatorname{div}(\operatorname{grad}\phi)$ at the point $(1, -1, 1)$. [[2]]

@q 4
(a) Find the Laplace transform of $\dfrac{1 - e^t}{t}$. [[2]]
(b) Find the inverse Laplace transform of $\dfrac{s}{(s+2)^3}$. [[2]]

@q 5
(a) Find the rank of the matrix $\begin{pmatrix}2 & -4 & 3 & 1 & 0\\ 1 & -2 & 1 & -4 & 2\\ 0 & 1 & -1 & 3 & 1\end{pmatrix}$. [[2]]
(b) Test whether the vectors $(1,1,1),\ (1,-1,1),\ (2,0,3)$ are linearly independent or dependent. [[2]]

@q 6
Express $2x^2 - 4x + 2$ in Legendre's polynomials. [[2]]

@q 7
Find the minimum value of $x^2 + xy + y^2 + 3z^2$ subject to $x + 2y + 4z - 60 = 0$ using the Lagrange multiplier method. [[4]]

@q 8
Change the order of integration and evaluate $\displaystyle\int_0^a\int_0^x\dfrac{\cos y}{\sqrt{(a-x)(a-y)}}\,dy\,dx$. [[4]]

@q 9
Prove that the necessary and sufficient condition for a vector function $\vec a$ of a scalar variable $t$ to have a constant direction is $\vec a\times\dfrac{d\vec a}{dt} = \vec 0$. [[4]]

@q 10
Find the area of the astroid $x^{2/3} + y^{2/3} = a^{2/3}$ using Green's theorem. [[4]]

@q 11
Apply the Gauss divergence theorem to evaluate $\displaystyle\iint_S\vec F\cdot\hat n\,ds$ for $\vec F = x\vec i - y\vec j + (z^2 - 1)\vec k$, where $S$ is the cylinder formed by the surfaces $z = 0$, $z = 1$ and $x^2 + y^2 = 4$. [[4]]

@q 12
Using the Laplace transform technique, solve the initial value problem $y''(t) - y'(t) + 6y(t) = e^{-t}$, $y(0) = 0$, $y'(0) = 0$. [[4]]

@q 13
Find the eigenvalues and eigenvectors of the matrix $\begin{pmatrix}3 & 2 & 2\\ 1 & 4 & 1\\ -2 & -4 & -1\end{pmatrix}$. [[4]]

@q 14
Reduce the quadratic form $Q(x) = 6x_1^2 + 3x_2^2 + 3x_3^2 - 4x_1x_2 - 2x_2x_3 + 4x_1x_3$ into canonical form. [[4]]

@q 15
Solve $y'' - 4xy' + (4x^2 - 2)y = 0$ by the power series method. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a)** Let $f = \tan u = x^2 + 2y^2$. It is homogeneous of degree $n = 2$, so Euler's theorem gives $x f_x + y f_y = 2f$. Since $f_x = \sec^2u\,u_x$ and $f_y = \sec^2u\,u_y$,
$$\sec^2u\left(x u_x + y u_y\right) = 2\tan u \;\Rightarrow\; x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = \frac{2\tan u}{\sec^2u} = 2\sin u\cos u = \sin 2u$$

**(b)** $\dfrac{\partial(u,v)}{\partial(x,y)} = \begin{vmatrix}2x & 0\\ 0 & 2y\end{vmatrix} = \mathbf{4xy}$.

@s 2
**(a)** Innermost: $\displaystyle\int_{x-z}^{x+z}(x+y+z)\,dy = \left[(x+z)y + \frac{y^2}{2}\right]_{x-z}^{x+z} = 2z(x+z) + \frac{(x+z)^2 - (x-z)^2}{2} = 2zx + 2z^2 + 2xz = 4xz + 2z^2$.
Then $\displaystyle\int_0^z(4xz + 2z^2)\,dx = 2z^3 + 2z^3 = 4z^3$, and $\displaystyle\int_0^14z^3\,dz = \mathbf{1}$.

**(b)** Mass $= \displaystyle\iiint\rho\,dV = \int_{-1}^1\int_{-1}^1\int_0^{1-x^2}z(y+2)\,dz\,dy\,dx$.
$$\int_0^{1-x^2}z\,dz = \frac{(1-x^2)^2}{2},\qquad \int_{-1}^1(y+2)\,dy = 4$$
$$M = 4\cdot\frac12\int_{-1}^1(1 - x^2)^2dx = 2\cdot2\left[1 - \frac23 + \frac15\right] = 4\cdot\frac{8}{15}=\frac{32}{15}$$
$$\boxed{M = \tfrac{32}{15}\ \text{units of mass}}$$

@s 3
**(a)** $\nabla\phi = (8x, 3, -4)$, which at $(1,2,1)$ is $(8, 3, -4)$. Unit vector along $2\vec i + 2\vec j + \vec k$ is $\hat e = \tfrac13(2, 2, 1)$.
$$D_{\hat e}\phi = \nabla\phi\cdot\hat e = \frac{16 + 6 - 4}{3} = \boxed{6}$$

**(b)** $\vec r = (\sqrt2\cos t, \sqrt2\sin t, 4t)$.
$\vec v = \dfrac{d\vec r}{dt} = (-\sqrt2\sin t, \sqrt2\cos t, 4)$, at $t = \tfrac\pi4$: $\vec v = -\vec i + \vec j + 4\vec k$, speed $\sqrt{1 + 1 + 16} = 3\sqrt2$.
$\vec a = \dfrac{d\vec v}{dt} = (-\sqrt2\cos t, -\sqrt2\sin t, 0)$, at $t = \tfrac\pi4$: $\vec a = -\vec i - \vec j$, magnitude $\sqrt2$.

**(c)** $\operatorname{div}\operatorname{grad}\phi = \nabla^2\phi$. $\phi_x = 3x^2 - 3yz$, $\phi_y = 3y^2 - 3xz$, $\phi_z = 3z^2 - 3xy$, so $\nabla^2\phi = 6x + 6y + 6z$. At $(1,-1,1)$: $6(1 - 1 + 1) = \boxed{6}$.

@s 4
**(a)** $\mathcal L\{1 - e^t\} = \dfrac1s - \dfrac1{s-1}$. Using $\mathcal L\{f(t)/t\} = \int_s^\infty F(p)\,dp$,
$$\mathcal L\left\{\frac{1-e^t}{t}\right\} = \int_s^\infty\left(\frac1p - \frac1{p-1}\right)dp = \Big[\ln\frac{p}{p-1}\Big]_s^\infty = -\ln\frac{s}{s-1} = \boxed{\ln\frac{s-1}{s}}\quad(s>1)$$

**(b)** Write $s = (s+2) - 2$: $\dfrac{s}{(s+2)^3} = \dfrac{1}{(s+2)^2} - \dfrac{2}{(s+2)^3}$. By the first shifting theorem, $\mathcal L^{-1}\left\{\dfrac1{(s+2)^2}\right\} = te^{-2t}$ and $\mathcal L^{-1}\left\{\dfrac{2}{(s+2)^3}\right\} = t^2e^{-2t}$:
$$\boxed{\mathcal L^{-1}\left\{\frac{s}{(s+2)^3}\right\} = (t - t^2)e^{-2t}}$$

@s 5
**(a)** Row reduce $A = \begin{pmatrix}2 & -4 & 3 & 1 & 0\\ 1 & -2 & 1 & -4 & 2\\ 0 & 1 & -1 & 3 & 1\end{pmatrix}$. Interchange $R_1\leftrightarrow R_2$, then $R_2\to R_2 - 2R_1$:
$$\begin{pmatrix}1 & -2 & 1 & -4 & 2\\ 0 & 0 & 1 & 9 & -4\\ 0 & 1 & -1 & 3 & 1\end{pmatrix}\;\xrightarrow{R_2\leftrightarrow R_3}\;\begin{pmatrix}1 & -2 & 1 & -4 & 2\\ 0 & 1 & -1 & 3 & 1\\ 0 & 0 & 1 & 9 & -4\end{pmatrix}$$
Three non-zero rows in echelon form: $\boxed{\text{rank}(A) = 3}$.

**(b)** $\begin{vmatrix}1 & 1 & 1\\ 1 & -1 & 1\\ 2 & 0 & 3\end{vmatrix} = 1(-3 - 0) - 1(3 - 2) + 1(0 + 2) = -3 - 1 + 2 = -2\ne0$. The determinant is non-zero, so the vectors are **linearly independent**.

@s 6
Legendre polynomials: $P_0 = 1,\ P_1 = x,\ P_2 = \tfrac12(3x^2 - 1)$, so $x^2 = \tfrac13(2P_2 + P_0)$. Then
$$2x^2 - 4x + 2 = \tfrac23(2P_2 + P_0) - 4P_1 + 2P_0 = \tfrac43P_2 - 4P_1 + \left(\tfrac23 + 2\right)P_0$$
$$\boxed{2x^2 - 4x + 2 = \tfrac43P_2(x) - 4P_1(x) + \tfrac83P_0(x)}$$
Check at $x = 1$: $\tfrac43 - 4 + \tfrac83 = 0 = 2 - 4 + 2$ ✓.

@s 7
Let $f = x^2 + xy + y^2 + 3z^2$ and $g = x + 2y + 4z - 60$. Form $F = f - \lambda g$ and set its partial derivatives to zero:
$$2x + y = \lambda,\qquad x + 2y = 2\lambda,\qquad 6z = 4\lambda \;\Rightarrow\; z = \frac{2\lambda}{3}$$
From the first two, $2(2x + y) = x + 2y \Rightarrow 3x = 0$, so $x = 0$, $y = \lambda$. The constraint gives $0 + 2\lambda + \dfrac{8\lambda}{3} - 60 = 0 \Rightarrow \dfrac{14\lambda}{3} = 60 \Rightarrow \lambda = \dfrac{90}{7}$. Hence
$$x = 0,\qquad y = \frac{90}{7},\qquad z = \frac{60}{7}$$
The function is a positive-definite quadratic form restricted to a plane, so this stationary point is the minimum:
$$f_{\min} = \left(\frac{90}{7}\right)^2 + 3\left(\frac{60}{7}\right)^2 = \frac{8100 + 10800}{49} = \boxed{\frac{2700}{7}\approx 385.7}$$

@s 8
The region is $0\le y\le x\le a$. Reversing the order: $y$ from $0$ to $a$, $x$ from $y$ to $a$.
$$I = \int_0^a\frac{\cos y}{\sqrt{a-y}}\left[\int_y^a\frac{dx}{\sqrt{a-x}}\right]dy,\qquad \int_y^a\frac{dx}{\sqrt{a-x}} = \Big[-2\sqrt{a-x}\Big]_y^a = 2\sqrt{a-y}$$
$$I = \int_0^a2\cos y\,dy = \boxed{2\sin a}$$

@s 9
Let $\vec a = a\,\hat e$, where $a = |\vec a|$ and $\hat e$ is the unit vector along $\vec a$. Then $\dfrac{d\vec a}{dt} = \dfrac{da}{dt}\hat e + a\dfrac{d\hat e}{dt}$ and
$$\vec a\times\frac{d\vec a}{dt} = a\frac{da}{dt}(\hat e\times\hat e) + a^2\left(\hat e\times\frac{d\hat e}{dt}\right) = a^2\left(\hat e\times\frac{d\hat e}{dt}\right)$$

*Necessity.* If the direction is constant, $\hat e$ is constant, so $\dfrac{d\hat e}{dt} = \vec0$ and $\vec a\times\dfrac{d\vec a}{dt} = \vec 0$.

*Sufficiency.* Suppose $\vec a\times\dfrac{d\vec a}{dt} = \vec0$ and $a\ne0$. Then $\hat e\times\dfrac{d\hat e}{dt} = \vec0$. But $\hat e\cdot\hat e = 1 \Rightarrow \hat e\cdot\dfrac{d\hat e}{dt} = 0$, so $\dfrac{d\hat e}{dt}$ is perpendicular to $\hat e$; and it is also parallel to $\hat e$ (zero cross product). A vector both perpendicular and parallel to a non-zero vector is zero: $\dfrac{d\hat e}{dt} = \vec0$, so $\hat e$ is constant. Hence the direction of $\vec a$ is constant. $\blacksquare$

@s 10
By Green's theorem the area enclosed by a simple closed curve $C$ is $A = \dfrac12\oint_C(x\,dy - y\,dx)$. Parametrise the astroid as $x = a\cos^3t,\ y = a\sin^3t$, $0\le t\le2\pi$. Then $dx = -3a\cos^2t\sin t\,dt$ and $dy = 3a\sin^2t\cos t\,dt$, so
$$x\,dy - y\,dx = 3a^2\left(\cos^4t\sin^2t + \sin^4t\cos^2t\right)dt = 3a^2\sin^2t\cos^2t\,dt$$
$$A = \frac{3a^2}{2}\int_0^{2\pi}\sin^2t\cos^2t\,dt = \frac{3a^2}{2}\cdot\frac14\int_0^{2\pi}\sin^22t\,dt = \frac{3a^2}{8}\cdot\pi$$
$$\boxed{A = \frac{3\pi a^2}{8}}$$

@s 11
$\vec F = (x, -y, z^2 - 1)$, so $\nabla\cdot\vec F = 1 - 1 + 2z = 2z$. By the divergence theorem, with $V$ the solid cylinder $x^2 + y^2\le4$, $0\le z\le1$:
$$\iint_S\vec F\cdot\hat n\,dS = \iiint_V2z\,dV = \int_0^12z\left[\iint_{x^2+y^2\le4}dx\,dy\right]dz = \int_0^12z\cdot4\pi\,dz = 4\pi\left[z^2\right]_0^1 = \boxed{4\pi}$$
(Direct check: top $z=1$: $\vec F\cdot\hat k = 0$; bottom $z=0$: $\vec F\cdot(-\hat k) = 1$, flux $= 4\pi$; curved surface: $\vec F\cdot\hat n = \dfrac{x^2 - y^2}{2}$, flux $0$ by symmetry. Total $4\pi$ ✓.)

@s 12
Take Laplace transforms with $y(0) = y'(0) = 0$: $s^2Y - sY + 6Y = \dfrac{1}{s+1}$, so
$$Y = \frac{1}{(s+1)(s^2 - s + 6)} = \frac{1/8}{s+1} - \frac{1}{8}\cdot\frac{s - 2}{s^2 - s + 6}$$
(partial fractions: $1 = A(s^2 - s + 6) + (Bs + C)(s+1)$ gives $A = \tfrac18$, $B = -\tfrac18$, $C = \tfrac14$.) Complete the square: $s^2 - s + 6 = \left(s - \tfrac12\right)^2 + \tfrac{23}{4}$, and $s - 2 = \left(s - \tfrac12\right) - \tfrac32$. With $\omega = \dfrac{\sqrt{23}}{2}$,
$$\mathcal L^{-1}\left\{\frac{s-2}{s^2-s+6}\right\} = e^{t/2}\left[\cos\omega t - \frac{3}{\sqrt{23}}\sin\omega t\right]$$
$$\boxed{y(t) = \frac18e^{-t} - \frac18e^{t/2}\left[\cos\frac{\sqrt{23}\,t}{2} - \frac{3}{\sqrt{23}}\sin\frac{\sqrt{23}\,t}{2}\right]}$$
Check: $y(0) = \tfrac18 - \tfrac18 = 0$ ✓; $y'(0) = -\tfrac18 - \tfrac18\left[\tfrac12 - \tfrac{3}{\sqrt{23}}\cdot\tfrac{\sqrt{23}}{2}\right] = -\tfrac18 - \tfrac18(-1) = 0$ ✓.

@s 13
Characteristic equation $|A - \lambda I| = 0$:
$$\begin{vmatrix}3-\lambda & 2 & 2\\ 1 & 4-\lambda & 1\\ -2 & -4 & -1-\lambda\end{vmatrix} = -\lambda^3 + 6\lambda^2 - 11\lambda + 6 = 0$$
(sum of eigenvalues $=$ trace $=6$; sum of principal minors $= 11$; $\det A = 6$.) So $(\lambda-1)(\lambda-2)(\lambda-3) = 0$: **$\lambda = 1, 2, 3$**.

- $\lambda = 1$: $(A - I)X = 0$: $2x + 2y + 2z = 0,\ x + 3y + z = 0$. Subtracting, $y = 0$, $x = -z$: $X_1 = (1, 0, -1)^T$.
- $\lambda = 2$: $x + 2y + 2z = 0,\ x + 2y + z = 0$. Subtracting, $z = 0$, $x = -2y$: $X_2 = (2, -1, 0)^T$.
- $\lambda = 3$: $2y + 2z = 0,\ x + y + z = 0$. Then $z = -y$ and $x = 0$: $X_3 = (0, 1, -1)^T$.

$$\boxed{\lambda = 1: k(1,0,-1)^T;\quad \lambda = 2: k(2,-1,0)^T;\quad \lambda = 3: k(0,1,-1)^T}$$

@s 14
The symmetric matrix of $Q$ is $A = \begin{pmatrix}6 & -2 & 2\\ -2 & 3 & -1\\ 2 & -1 & 3\end{pmatrix}$. Its characteristic polynomial is $\lambda^3 - 12\lambda^2 + 36\lambda - 32 = (\lambda - 2)^2(\lambda - 8)$, so $\lambda = 2, 2, 8$.

- $\lambda = 8$: $-2x - 2y + 2z = 0,\ -2x - 5y - z = 0$ give $X_3 = (2, -1, 1)^T$.
- $\lambda = 2$: the single equation $2x - y + z = 0$ has two independent solutions orthogonal to $X_3$: $X_1 = (1, 2, 0)^T$ and $X_2 = (-1, 0, 2)^T$ (check: $X_1\cdot X_3 = 2 - 2 + 0 = 0$ and $X_2\cdot X_3 = -2 + 0 + 2 = 0$ ✓). Making $X_1, X_2$ orthogonal (Gram–Schmidt) is only needed if an orthonormal matrix is demanded; the canonical form below does not depend on it.

Under $X = PY$ with $P$ the (normalised, orthogonal) matrix of eigenvectors, $Q = Y^TP^TAPY = Y^T\,\text{diag}(2, 2, 8)\,Y$:
$$\boxed{Q = 2y_1^2 + 2y_2^2 + 8y_3^2}$$
Rank $3$, index $3$, signature $3$: $Q$ is positive definite.

@s 15
Let $y = \sum_{n=0}^\infty a_nx^n$. Substituting into $y'' - 4xy' + (4x^2 - 2)y = 0$ and equating the coefficient of $x^n$:
$$(n+2)(n+1)a_{n+2} - 4na_n + 4a_{n-2} - 2a_n = 0 \;\Rightarrow\; a_{n+2} = \frac{(4n+2)a_n - 4a_{n-2}}{(n+1)(n+2)}$$
(with $a_{-1} = a_{-2} = 0$). Computing:

| $n$ | $a_{n+2}$ |
|---|---|
| $0$ | $a_2 = a_0$ |
| $1$ | $a_3 = a_1$ |
| $2$ | $a_4 = \dfrac{10a_2 - 4a_0}{12} = \dfrac{a_0}{2}$ |
| $3$ | $a_5 = \dfrac{14a_3 - 4a_1}{20} = \dfrac{a_1}{2}$ |

so $y = a_0\left(1 + x^2 + \dfrac{x^4}{2} + \cdots\right) + a_1\left(x + x^3 + \dfrac{x^5}{2} + \cdots\right)$. Recognising $e^{x^2} = 1 + x^2 + \dfrac{x^4}{2!} + \cdots$:
$$\boxed{y = (a_0 + a_1x)\,e^{x^2}}$$
Check: for $y = e^{x^2}$, $y' = 2xe^{x^2}$, $y'' = (2 + 4x^2)e^{x^2}$, and $2 + 4x^2 - 8x^2 + 4x^2 - 2 = 0$ ✓.

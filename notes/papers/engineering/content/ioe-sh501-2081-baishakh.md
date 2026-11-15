---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-III-SH501-2081-Baishakh.pdf
subject: Engineering Mathematics III
level: BE · Year II / Part I
code: SH 501
year_bs: 2081 Baishakh
cal: BS
year_ad: 2024
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 501). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Use properties of determinant to prove: $\begin{vmatrix}(b+c)^2 & a^2 & a^2\\ b^2 & (c+a)^2 & b^2\\ c^2 & c^2 & (a+b)^2\end{vmatrix} = 2abc(a+b+c)^3$. [[5]]

@q 2
Prove that the necessary and sufficient condition for a square matrix $A$ to possess an inverse is that $A$ is non-singular. [[5]]

@q 3
Define rank of a matrix. Reduce the matrix $\begin{bmatrix}2&-2&0&6\\4&2&0&2\\1&-1&0&3\\1&-2&1&2\end{bmatrix}$ into echelon form and hence find its rank. [[1+4]]

@q 4
Find the modal matrix of the matrix $A = \begin{bmatrix}1&0&-1\\1&2&1\\2&2&3\end{bmatrix}$. [[5]]

@q 5
A vector field is given by $\vec F = \sin y\,\hat i + x(1 + \cos y)\hat j$. Evaluate the line integral over the circular path given by $x^2 + y^2 = a^2$, $z = 0$. [[5]]

@q 6
State Green's theorem. Using Green's theorem, find the area of astroid $x^{2/3} + y^{2/3} = a^{2/3}$. [[1+4]]

@q 7
State Gauss divergence theorem. Evaluate $\displaystyle\iint_S\vec F\cdot\hat n\,ds$ for $\vec F = 2x\hat i + 3y\hat j + 4z\hat k$ where $S$ is the surface of sphere $x^2 + y^2 + z^2 = 1$ by Gauss's divergence theorem. [[1+4]]

@q 8
Use Stoke's theorem to evaluate $\displaystyle\iint_S(\nabla\times\vec F)\cdot\hat n\,ds$ where $\vec F = y\hat i + x(1 - 2z)\hat j - xy\hat k$ and $S$ is the surface of the sphere $x^2 + y^2 + z^2 = a^2$ above the $xy$-plane. [[5]]

@q 9
Find the Fourier series of the function $f(x) = |x|$ for $-\pi\le x\le\pi$ in a Fourier series and deduce $\dfrac{\pi^2}{8} = \dfrac1{1^2} + \dfrac1{3^2} + \dfrac1{5^2} + \cdots$. [[4+1]]

@q 10
Find half-range Fourier sine series of $f(x) = e^{ax}$ in the interval $0\le x\le\pi$. [[5]]

@q 11
Discuss the existence of Laplace transform. Find the Laplace transform of (i) $te^t$ (ii) $\sinh at\sin at$. [[1+2+2]]

@q 12
Find the Inverse Laplace transform of a) $\dfrac{s^2}{(s-1)^3}$ b) $\dfrac{s^2}{(s^2+4)^2}$. [[2+3]]

@q 13
Solve the following differential equation by Laplace transform method $y'' + 3y' + 2y = e^t$, $y(0) = 0 = y'(0)$. [[5]]

@q 14
Solve the following linear programming problem using the big M method: Maximize $P = 2x_1 + x_2$ subject to $x_1 + x_2\le10$, $-x_1 + x_2\ge2$, $x_1, x_2\ge0$. [[7]]

@q 15
Use duality of simplex method to minimize $z = 8x_1 + 9x_2$ subject to: $x_1 + 3x_2\ge4$, $2x_1 + x_2\ge5$, $x_1, x_2\ge0$. [[8]]
<!-- SOLUTIONS -->

@s 1
Let $D$ be the determinant. Apply $C_1\to C_1 - C_3$ and $C_2\to C_2 - C_3$:

- $C_1$: $(b+c)^2 - a^2 = (b + c - a)(a + b + c)$; $\ b^2 - b^2 = 0$; $\ c^2 - (a+b)^2 = (c - a - b)(a + b + c)$
- $C_2$: $a^2 - a^2 = 0$; $\ (c+a)^2 - b^2 = (c + a - b)(a + b + c)$; $\ c^2 - (a+b)^2 = (c - a - b)(a + b + c)$

Take the common factor $(a+b+c)$ out of $C_1$ and of $C_2$. Writing $p = b + c - a$, $q = c + a - b$, $r = c - a - b$:

$$D = (a+b+c)^2\begin{vmatrix}p&0&a^2\\0&q&b^2\\r&r&(a+b)^2\end{vmatrix}$$

Apply $R_3\to R_3 - R_1 - R_2$: the new third row is $\big(r - p,\ r - q,\ (a+b)^2 - a^2 - b^2\big) = (-2b,\ -2a,\ 2ab)$:

$$D = (a+b+c)^2\begin{vmatrix}p&0&a^2\\0&q&b^2\\-2b&-2a&2ab\end{vmatrix}$$

Expand along the first row:

$$\begin{vmatrix}p&0&a^2\\0&q&b^2\\-2b&-2a&2ab\end{vmatrix} = p(2abq + 2ab^2) + a^2(0 + 2bq) = 2ab\big[p(q + b) + aq\big]$$

Now $q + b = c + a$, so

$$\begin{gathered}p(q + b) + aq = (b + c - a)(c + a) + a(c + a - b) = bc + c^2 + ab - a^2 + ac + a^2 - ab = c(a + b + c)\end{gathered}$$

$$\begin{gathered}D = (a+b+c)^2\cdot2abc(a+b+c) = \boxed{2abc(a+b+c)^3} \\ \blacksquare\end{gathered}$$

@s 2
A square matrix $A$ possesses an inverse if there is a matrix $B$ with $AB = BA = I$.

**Necessary.** Suppose $A^{-1}$ exists. Then $AA^{-1} = I$, and taking determinants, $|A|\cdot|A^{-1}| = |I| = 1$. Hence $|A|\ne0$: $A$ is non-singular.

**Sufficient.** Suppose $|A|\ne0$. For the adjoint matrix $\operatorname{adj}A$ (the transpose of the matrix of cofactors) the expansion theorems of determinants give

$$\begin{gathered}A\cdot\operatorname{adj}A = \operatorname{adj}A\cdot A = |A|\,I\end{gathered}$$

(the diagonal entries are $\sum a_{ij}C_{ij} = |A|$ and the off-diagonal ones $\sum a_{ij}C_{kj} = 0$ for $i\ne k$, a determinant with two equal rows). Dividing by $|A|\ne0$,

$$\begin{gathered}A\left(\frac{\operatorname{adj}A}{|A|}\right) = \left(\frac{\operatorname{adj}A}{|A|}\right)A = I\end{gathered}$$

So $A^{-1} = \dfrac{\operatorname{adj}A}{|A|}$ exists. $\blacksquare$ (The inverse is also unique: if $AB = BA = I$ and $AC = CA = I$, then $B = BI = B(AC) = (BA)C = C$.)

@s 3
**Rank.** The rank of a matrix is the order of the largest non-vanishing square sub-determinant (minor); equivalently, the number of non-zero rows in its row-echelon form (the maximum number of linearly independent rows).

**Reduction to echelon form.** Interchange $R_1\leftrightarrow R_3$ (to get a leading $1$):

$$\begin{bmatrix}1&-1&0&3\\4&2&0&2\\2&-2&0&6\\1&-2&1&2\end{bmatrix}\xrightarrow{R_2\to R_2 - 4R_1,\ R_3\to R_3 - 2R_1,\ R_4\to R_4 - R_1}\begin{bmatrix}1&-1&0&3\\0&6&0&-10\\0&0&0&0\\0&-1&1&-1\end{bmatrix}$$

Interchange $R_3\leftrightarrow R_4$ and apply $R_3\to R_3 + \tfrac16R_2$:

$$\begin{bmatrix}1&-1&0&3\\0&6&0&-10\\0&-1&1&-1\\0&0&0&0\end{bmatrix}\longrightarrow\begin{bmatrix}1&-1&0&3\\0&6&0&-10\\0&0&1&-\tfrac83\\0&0&0&0\end{bmatrix}$$

This is the echelon form. There are three non-zero rows, so

$$\boxed{\operatorname{rank} = 3}$$

(*Check:* the rows $R_1$ and $R_3$ of the original matrix are proportional ($R_1 = 2R_3$), so the rank is at most $3$; and the minor formed by columns $1, 2, 3$ of $R_1, R_2, R_4$ is non-zero.)

@s 4
**Characteristic equation** $|A - \lambda I| = 0$:

$$\begin{vmatrix}1 - \lambda&0&-1\\1&2 - \lambda&1\\2&2&3 - \lambda\end{vmatrix} = 0\ \Longrightarrow\ \lambda^3 - 6\lambda^2 + 11\lambda - 6 = 0$$

(sum of the diagonal $= 6$, sum of principal minors $= (2 - 0) + (3 + 2) + (6 - 2) = 11$, $|A| = 6$.) Factorising, $(\lambda - 1)(\lambda - 2)(\lambda - 3) = 0$: $\lambda = 1, 2, 3$.

**Eigenvectors** from $(A - \lambda I)X = 0$:

*$\lambda = 1$:* $\begin{bmatrix}0&0&-1\\1&1&1\\2&2&2\end{bmatrix}$: $z = 0$, $x + y = 0$: $X_1 = (-1, 1, 0)^T$.

*$\lambda = 2$:* $\begin{bmatrix}-1&0&-1\\1&0&1\\2&2&1\end{bmatrix}$: the first row gives $x = -z$ and the third gives $2x + 2y + z = 0\Rightarrow y = \dfrac z2$; with $z = 2$: $x = -2$, $y = 1$: $X_2 = (-2, 1, 2)^T$.

*$\lambda = 3$:* $\begin{bmatrix}-2&0&-1\\1&-1&1\\2&2&0\end{bmatrix}$: the third row gives $y = -x$, the first row $z = -2x$, and the second row is then satisfied ($x + x - 2x = 0$); with $x = -1$: $X_3 = (-1, 1, 2)^T$.

The **modal matrix** $P$ has the eigenvectors as its columns:

$$\boxed{P = \begin{bmatrix}-1&-2&-1\\1&1&1\\0&2&2\end{bmatrix}}$$

and $P^{-1}AP = \operatorname{diag}(1, 2, 3)$ (the eigenvalues in the same order as the columns; verified: $AX_i = \lambda_iX_i$ for each column). The eigenvalues are distinct, so $P$ is non-singular ($|P| = -2$).

@s 5
By Green's theorem in the plane, for the circle $C: x^2 + y^2 = a^2$ ($z = 0$) traversed counter-clockwise, with $\vec F\cdot d\vec r = P\,dx + Q\,dy$, $P = \sin y$, $Q = x(1 + \cos y)$:

$$\begin{gathered}\oint_C\vec F\cdot d\vec r = \iint_R\left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dx\,dy \\ \frac{\partial Q}{\partial x} = 1 + \cos y,\quad\frac{\partial P}{\partial y} = \cos y\end{gathered}$$

$$\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = 1$$

$$\begin{gathered}\boxed{\oint_C\vec F\cdot d\vec r = \iint_R dx\,dy = \text{area of the circle} = \pi a^2}\end{gathered}$$

(Alternatively, $\nabla\times\vec F = \hat k$ and Stokes' theorem gives the same value.)

@s 6
**Green's theorem.** If $P, Q$ have continuous first partial derivatives in a region $R$ bounded by a simple closed curve $C$ (counter-clockwise), then

$$\oint_C(P\,dx + Q\,dy) = \iint_R\left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dx\,dy$$

**Area.** Taking $P = -y$, $Q = x$ gives $\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y} = 2$, so the area is

$$A = \frac12\oint_C(x\,dy - y\,dx)$$

For the astroid $x = a\cos^3t$, $y = a\sin^3t$, $0\le t\le2\pi$: $dx = -3a\cos^2t\sin t\,dt$, $dy = 3a\sin^2t\cos t\,dt$:

$$\begin{gathered}x\,dy - y\,dx = 3a^2\big(\cos^4t\sin^2t + \sin^4t\cos^2t\big)dt = 3a^2\sin^2t\cos^2t\,dt\end{gathered}$$

$$\begin{gathered}A = \frac12\cdot3a^2\int_0^{2\pi}\sin^2t\cos^2t\,dt = \frac{3a^2}{2}\int_0^{2\pi}\frac{\sin^22t}{4}\,dt = \frac{3a^2}{2}\cdot\frac\pi4\end{gathered}$$

$$\boxed{A = \frac{3\pi a^2}{8}}$$

```figure caption="Question 6: the astroid x^(2/3) + y^(2/3) = a^(2/3) (a = 1), traversed counter-clockwise; area 3 pi a^2 / 8."
t=np.linspace(0,2*np.pi,400)
fig,ax=plt.subplots(figsize=(3.4,3.4))
ax.fill(np.cos(t)**3,np.sin(t)**3,color='#dbe8f6',alpha=.8); ax.plot(np.cos(t)**3,np.sin(t)**3,color='#1d6fb8',lw=1.8)
ax.annotate('',xy=(0.55,0.2),xytext=(0.7,0.05),arrowprops=dict(arrowstyle='->',color='#d9534f'))
ax.axhline(0,color='#14181f',lw=.6); ax.axvline(0,color='#14181f',lw=.6)
ax.text(1.03,0.03,'a',fontsize=8); ax.text(0.03,1.03,'a',fontsize=8)
ax.set_aspect('equal'); ax.axis('off')
```

@s 7
**Gauss's divergence theorem.** If $\vec F$ has continuous first partial derivatives in a volume $V$ bounded by a closed surface $S$ with outward unit normal $\hat n$, then

$$\iint_S\vec F\cdot\hat n\,ds = \iiint_V\nabla\cdot\vec F\,dV$$

Here $\nabla\cdot\vec F = 2 + 3 + 4 = 9$ and $V$ is the unit ball, of volume $\dfrac43\pi(1)^3$:

$$\begin{gathered}\boxed{\iint_S\vec F\cdot\hat n\,ds = 9\cdot\frac{4\pi}{3} = 12\pi}\end{gathered}$$

*Check by direct integration.* On the unit sphere $\hat n = (x, y, z)$, so $\vec F\cdot\hat n = 2x^2 + 3y^2 + 4z^2$. By symmetry $\iint x^2\,ds = \iint y^2\,ds = \iint z^2\,ds = \dfrac13(4\pi)$, so the integral equals $(2 + 3 + 4)\cdot\dfrac{4\pi}{3} = 12\pi$ ✓.

@s 8
**Stokes' theorem:** $\displaystyle\iint_S(\nabla\times\vec F)\cdot\hat n\,ds = \oint_C\vec F\cdot d\vec r$, $C$ being the boundary of $S$ (counter-clockwise seen from the tip of $\hat n$).

The surface is the upper hemisphere; its boundary is the circle $C: x^2 + y^2 = a^2$, $z = 0$. On $C$ ($z = 0$, $dz = 0$):

$$\begin{gathered}\vec F\cdot d\vec r = y\,dx + x(1 - 2z)\,dy - xy\,dz = y\,dx + x\,dy = d(xy)\end{gathered}$$

With $x = a\cos t$, $y = a\sin t$, $0\le t\le2\pi$: $\oint_Cd(xy) = [xy]_0^{2\pi} = 0$.

$$\boxed{\iint_S(\nabla\times\vec F)\cdot\hat n\,ds = 0}$$

(*Check:* $\nabla\times\vec F = (x, y, -2z)$ and $\hat n = (x, y, z)/a$; the integrand $\dfrac{x^2 + y^2 - 2z^2}{a}$ integrates to $0$ over the hemisphere because $\iint x^2 = \iint y^2 = \iint z^2$.)

@s 9
$f(x) = |x|$ is an even function on $[-\pi, \pi]$, so $b_n = 0$ and

$$\begin{gathered}a_0 = \frac2\pi\int_0^\pi x\,dx = \frac2\pi\cdot\frac{\pi^2}{2} = \pi\end{gathered}$$

$$a_n = \frac2\pi\int_0^\pi x\cos nx\,dx = \frac2\pi\left[\frac{x\sin nx}{n} + \frac{\cos nx}{n^2}\right]_0^\pi = \frac{2}{\pi n^2}\big[(-1)^n - 1\big] = \begin{cases}-\dfrac{4}{\pi n^2}&n\ \text{odd}\\0&n\ \text{even}\end{cases}$$

$$\begin{gathered}\boxed{|x| = \frac\pi2 - \frac4\pi\left[\cos x + \frac{\cos3x}{3^2} + \frac{\cos5x}{5^2} + \cdots\right],\quad-\pi\le x\le\pi}\end{gathered}$$

**Deduction.** $f$ is continuous at $x = 0$ with $f(0) = 0$:

$$\begin{gathered}0 = \frac\pi2 - \frac4\pi\left[\frac1{1^2} + \frac1{3^2} + \frac1{5^2} + \cdots\right]\ \Longrightarrow\ \boxed{\frac{\pi^2}{8} = \frac1{1^2} + \frac1{3^2} + \frac1{5^2} + \cdots} \\ \blacksquare\end{gathered}$$

@s 10
Half-range sine series: $f(x) = \displaystyle\sum_{n=1}^\infty b_n\sin nx$, $b_n = \dfrac2\pi\displaystyle\int_0^\pi e^{ax}\sin nx\,dx$. Using $\displaystyle\int e^{ax}\sin nx\,dx = \frac{e^{ax}(a\sin nx - n\cos nx)}{a^2 + n^2}$:

$$\begin{gathered}\int_0^\pi e^{ax}\sin nx\,dx = \frac{e^{a\pi}(-n\cos n\pi) + n}{a^2 + n^2} = \frac{n\big[1 - (-1)^ne^{a\pi}\big]}{a^2 + n^2}\end{gathered}$$

$$b_n = \frac{2n\big[1 - (-1)^ne^{a\pi}\big]}{\pi(a^2 + n^2)}$$

$$\begin{gathered}\boxed{e^{ax} = \frac2\pi\sum_{n=1}^\infty\frac{n\big[1 - (-1)^ne^{a\pi}\big]}{a^2 + n^2}\sin nx,\quad0<x<\pi}\end{gathered}$$

The first terms are $\dfrac2\pi\left[\dfrac{1 + e^{a\pi}}{a^2 + 1}\sin x + \dfrac{2(1 - e^{a\pi})}{a^2 + 4}\sin2x + \dfrac{3(1 + e^{a\pi})}{a^2 + 9}\sin3x + \cdots\right]$.

@s 11
**Existence.** $L\{f(t)\} = \displaystyle\int_0^\infty e^{-st}f(t)\,dt$ exists for $s > k$ if $f(t)$ is (i) piecewise continuous on every finite interval $[0, T]$ and (ii) of exponential order $k$, i.e. $|f(t)|\le Me^{kt}$ for $t\ge T$. (Sufficient, not necessary: for example $t^{-1/2}$ is not piecewise continuous at $0$ but has the transform $\sqrt{\pi/s}$; $e^{t^2}$ has no transform since it is not of exponential order.)

**(i)** $L\{e^t\} = \dfrac{1}{s - 1}$ and $L\{tf(t)\} = -F'(s)$:

$$\begin{gathered}\boxed{L\{te^t\} = -\frac{d}{ds}\frac{1}{s - 1} = \frac{1}{(s - 1)^2}}\end{gathered}$$

**(ii)** Write $\sinh at\sin at = \tfrac12\big(e^{at} - e^{-at}\big)\sin at$ and use $L\{e^{\pm at}\sin at\} = \dfrac{a}{(s\mp a)^2 + a^2}$:

$$\begin{gathered}L\{\sinh at\sin at\} = \frac a2\left[\frac{1}{(s - a)^2 + a^2} - \frac{1}{(s + a)^2 + a^2}\right] = \frac a2\cdot\frac{(s + a)^2 - (s - a)^2}{\big[(s-a)^2 + a^2\big]\big[(s + a)^2 + a^2\big]} = \frac a2\cdot\frac{4as}{(s^2 + 2a^2)^2 - 4a^2s^2}\end{gathered}$$

$$\boxed{L\{\sinh at\sin at\} = \frac{2a^2s}{s^4 + 4a^4}}$$

@s 12
**(a)** Write $s^2 = \big[(s - 1) + 1\big]^2 = (s-1)^2 + 2(s - 1) + 1$:

$$\frac{s^2}{(s-1)^3} = \frac{1}{s - 1} + \frac{2}{(s-1)^2} + \frac{1}{(s-1)^3}$$

Using $L^{-1}\left\{\dfrac{1}{(s-1)^{k+1}}\right\} = \dfrac{t^ke^t}{k!}$:

$$\boxed{L^{-1}\left\{\frac{s^2}{(s-1)^3}\right\} = e^t\left(1 + 2t + \frac{t^2}{2}\right)}$$

**(b)** $\dfrac{s^2}{(s^2 + 4)^2} = \dfrac12\left[\dfrac{s^2 - 4}{(s^2 + 4)^2} + \dfrac{1}{s^2 + 4}\right]$ and $L\{t\cos2t\} = \dfrac{s^2 - 4}{(s^2 + 4)^2}$, $L\{\sin2t\} = \dfrac{2}{s^2 + 4}$, so

$$\begin{gathered}\boxed{L^{-1}\left\{\frac{s^2}{(s^2+4)^2}\right\} = \frac12\left[t\cos2t + \frac{\sin2t}{2}\right] = \frac{t\cos2t}{2} + \frac{\sin2t}{4}}\end{gathered}$$

(*Check by convolution:* $L^{-1}\left\{\dfrac{s}{s^2+4}\cdot\dfrac{s}{s^2+4}\right\} = \displaystyle\int_0^t\cos2u\cos2(t - u)\,du = \tfrac12\int_0^t\big[\cos2t + \cos(4u - 2t)\big]du = \tfrac12t\cos2t + \tfrac14\sin2t$ ✓.)

@s 13
$y'' + 3y' + 2y = e^t$, $y(0) = 0$, $y'(0) = 0$. Take the Laplace transform ($Y = L\{y\}$):

$$\begin{gathered}s^2Y + 3sY + 2Y = \frac{1}{s - 1}\ \Longrightarrow\ Y = \frac{1}{(s - 1)(s + 1)(s + 2)}\end{gathered}$$

Partial fractions: $\dfrac{1}{(s-1)(s+1)(s+2)} = \dfrac{A}{s-1} + \dfrac{B}{s+1} + \dfrac{C}{s+2}$ with

$$\begin{gathered}A = \frac{1}{(2)(3)} = \frac16,\quad B = \frac{1}{(-2)(1)} = -\frac12,\quad C = \frac{1}{(-3)(-1)} = \frac13\end{gathered}$$

$$\boxed{y(t) = \frac{e^t}{6} - \frac{e^{-t}}{2} + \frac{e^{-2t}}{3}}$$

*Check:* $y(0) = \tfrac16 - \tfrac12 + \tfrac13 = 0$ ✓; $y'(0) = \tfrac16 + \tfrac12 - \tfrac23 = 0$ ✓; the particular part $\tfrac16e^t$ satisfies $(1 + 3 + 2)\tfrac16e^t = e^t$ ✓.

@s 14
**Maximize $P = 2x_1 + x_2$ subject to $x_1 + x_2\le10$, $-x_1 + x_2\ge2$, $x_1, x_2\ge0$.**

Add a slack $s_1$ to the first constraint; subtract a surplus $s_2$ and add an artificial variable $A_1$ in the second:

$$\begin{gathered}x_1 + x_2 + s_1 = 10 \\ -x_1 + x_2 - s_2 + A_1 = 2\end{gathered}$$

$$\text{Max }P = 2x_1 + x_2 + 0s_1 + 0s_2 - MA_1$$

The starting basis is $\{s_1, A_1\}$; the objective row $P - 2x_1 - x_2 + MA_1 = 0$ is made free of $A_1$ by $R_P\to R_P - M R_{A_1}$ (Table 1).

**Table 1**

| Basis | x1 | x2 | s1 | s2 | A1 | RHS |
|---|---|---|---|---|---|---|
| s1 | 1 | 1 | 1 | 0 | 0 | 10 |
| A1 | -1 | 1 | 0 | -1 | 1 | 2 |
| Z | M - 2 | -M - 1 | 0 | M | 0 | -2M |

Entering x2, leaving A1 (pivot 1).

**Table 2**

| Basis | x1 | x2 | s1 | s2 | A1 | RHS |
|---|---|---|---|---|---|---|
| s1 | 2 | 0 | 1 | 1 | -1 | 8 |
| x2 | -1 | 1 | 0 | -1 | 1 | 2 |
| Z | -3 | 0 | 0 | -1 | M + 1 | 2 |

Entering x1, leaving s1 (pivot 2).

**Table 3**

| Basis | x1 | x2 | s1 | s2 | A1 | RHS |
|---|---|---|---|---|---|---|
| x1 | 1 | 0 | 1/2 | 1/2 | -1/2 | 4 |
| x2 | 0 | 1 | 1/2 | -1/2 | 1/2 | 6 |
| Z | 0 | 0 | 3/2 | 1/2 | M - 1/2 | 14 |


All $P$-row entries are $\ge0$ (the artificial variable left the basis in Table 2): optimal.

$$\begin{gathered}\boxed{x_1 = 4,\quad x_2 = 6,\quad P_{\max} = 2(4) + 6 = 14}\end{gathered}$$

**Graphical check.** The feasible region is the triangle with corners $(0, 2)$, $(0, 10)$, $(4, 6)$: $P = 2$, $10$, $14$. The maximum $14$ is at $(4, 6)$ ✓.

```figure caption="Question 14: feasible region of x1 + x2 <= 10 and -x1 + x2 >= 2; the optimum is at (4, 6), P = 14."
x=np.linspace(0,10,100)
fig,ax=plt.subplots(figsize=(4.4,3.0))
ax.plot(x,10-x,color='#1d6fb8',lw=1.6); ax.plot(x,x+2,color='#2e8b57',lw=1.6)
xs=np.linspace(0,4,50); ax.fill_between(xs,xs+2,10-xs,color='#dbe8f6',alpha=.9)
ax.plot([0,0,4],[2,10,6],'o',color='#14181f',ms=4)
ax.text(.2,1.2,'(0, 2)  P = 2',fontsize=8); ax.text(.2,10.2,'(0, 10)  P = 10',fontsize=8); ax.text(4.2,6.2,'(4, 6)  P = 14',fontsize=8)
ax.text(6.3,3.2,'$x_1 + x_2 = 10$',fontsize=8,color='#1d6fb8'); ax.text(6.3,8.7,'$-x_1 + x_2 = 2$',fontsize=8,color='#2e8b57')
ax.set_xlim(0,10); ax.set_ylim(0,11.5); ax.set_xlabel('$x_1$'); ax.set_ylabel('$x_2$'); ax.tick_params(labelsize=7); ax.spines[['top','right']].set_visible(False)
```

@s 15
**Minimize $z = 8x_1 + 9x_2$ subject to $x_1 + 3x_2\ge4$, $2x_1 + x_2\ge5$, $x_1, x_2\ge0$.**

**Dual problem.** Attach dual variables $y_1, y_2$ to the two constraints. The primal is a minimisation with all constraints of the $\ge$ type, so the dual is

$$\begin{gathered}\text{Maximize }w = 4y_1 + 5y_2\quad\text{subject to}\quad y_1 + 2y_2\le8,\ \ 3y_1 + y_2\le9,\ \ y_1, y_2\ge0\end{gathered}$$

(the columns of the primal coefficient matrix become the dual rows). Adding slack variables $s_1, s_2$ and solving the dual by the simplex method:

**Table 1**

| Basis | y1 | y2 | s1 | s2 | RHS |
|---|---|---|---|---|---|
| s1 | 1 | 2 | 1 | 0 | 8 |
| s2 | 3 | 1 | 0 | 1 | 9 |
| Z | -4 | -5 | 0 | 0 | 0 |

Entering y2, leaving s1 (pivot 2).

**Table 2**

| Basis | y1 | y2 | s1 | s2 | RHS |
|---|---|---|---|---|---|
| y2 | 1/2 | 1 | 1/2 | 0 | 4 |
| s2 | 5/2 | 0 | -1/2 | 1 | 5 |
| Z | -3/2 | 0 | 5/2 | 0 | 20 |

Entering y1, leaving s2 (pivot 5/2).

**Table 3**

| Basis | y1 | y2 | s1 | s2 | RHS |
|---|---|---|---|---|---|
| y2 | 0 | 1 | 3/5 | -1/5 | 3 |
| y1 | 1 | 0 | -1/5 | 2/5 | 2 |
| Z | 0 | 0 | 11/5 | 3/5 | 23 |


All $w$-row entries are non-negative, so the dual is optimal: $y_1 = 2$, $y_2 = 3$, $w_{\max} = 4(2) + 5(3) = 23$.

**Primal solution.** The values of the primal variables $x_1, x_2$ are the entries of the final $w$-row under the slack columns $s_1, s_2$: $x_1 = \tfrac{11}{5}$, $x_2 = \tfrac35$, and $z_{\min} = w_{\max}$ (duality theorem):

$$\begin{gathered}\boxed{x_1 = \frac{11}{5},\quad x_2 = \frac35,\quad z_{\min} = 8\cdot\frac{11}5 + 9\cdot\frac35 = 23}\end{gathered}$$

**Check.** $x_1 + 3x_2 = \dfrac{11 + 9}{5} = 4$ ✓ and $2x_1 + x_2 = \dfrac{22 + 3}{5} = 5$ ✓ (both binding, as both $y_i>0$). The other corners of the primal region give $(4, 0)$: $z = 32$, and $(0, 5)$: $z = 45$, both larger than $23$.

---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-III-SH501-2081-Bhadra.pdf
subject: Engineering Mathematics III
level: BE · Year II / Part I
code: SH 501
year_bs: 2081 Bhadra
cal: BS
year_ad: 2024
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (old course, SH 501). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Show that $\begin{vmatrix}a & b & c\\ b+c & c+a & a+b\\ a^2 & b^2 & c^2\end{vmatrix} = (a-b)(b-c)(a-c)(a+b+c)$. [[5]]

@q 2
Prove that every square matrix can uniquely be expressed as the sum of symmetric and skew-symmetric matrices. [[5]]

@q 3
Test for consistency of the system of equations $5x + 3y + 7z = 4$, $3x + 26y + 2z = 9$, $7x + 2y + 10z = 5$ and solve if found consistent. [[3+2]]

@q 4
Find the eigen values and vectors of the matrix $\begin{bmatrix}1&2&-1\\0&2&1\\0&0&3\end{bmatrix}$. [[2+3]]

@q 5
Show that $\vec F = (x^2 - yz)\hat i + (y^2 - zx)\hat j + (z^2 - xy)\hat k$ is irrotational; also find its scalar potential function. [[2+3]]

@q 6
Apply Stoke's theorem to evaluate $\displaystyle\iint_S(\nabla\times\vec F)\cdot\hat n\,ds$ where $\vec F = y\hat i + x(1 - 2z)\hat j - xy\hat k$ and $S$ is the surface of the sphere $x^2 + y^2 + z^2 = a^2$ above the $xy$-plane. [[5]]

@q 7
State and prove Green's theorem in plane. [[1+4]]

@q 8
Using Gauss's divergence theorem, to evaluate $\displaystyle\iint_S\vec F\cdot\hat n\,ds$ where $\vec F = x\hat i + y\hat j + z^2\hat k$ and $S$ is the surface bounded by the cylinder $x^2 + y^2 = 9$, $z = 0$ and $z = 2$. [[5]]

@q 9
State existence condition for Laplace transform. Obtain the Laplace transform of

a) $t\cosh at$

b) $\dfrac{\sin2t}{t}$ [[1+2+2]]

@q 10
Find the inverse Laplace transform of (i) $\log\dfrac{s+1}{s-1}$ (ii) $\dfrac{s}{(s-3)(s^2+4)}$. [[3+2]]

@q 11
Solve the differential equation by using Laplace Transform $(D^2 - 3D + 2)y = e^{3t}$ under the conditions $y(0) = 0$, $y'(0) = 1$. [[5]]

@q 12
Find the Fourier series of the function $f(x) = \left(\dfrac{\pi - x}{2}\right)^2$ in the interval $0\le x\le2\pi$. [[5]]

@q 13
Expand $f(x) = \pi x - x^2$ in a half range sine series in the interval $(0, \pi)$ up to the first three terms. [[5]]

@q 14
Solve the following Linear Programming problem by constructing dual:

Minimize $Z = 21x + 50y$

Subject to $2x + 5y\ge12$, $3x + 7y\ge17$ and $x, y\ge0$ [[7]]

@q 15
Solving the following linear programming problem by using the Big-M method:

Maximize $Z = 4x_1 + 5x_2$;

Subject to $x_1 + x_2\le5$, $3x_1 + 10x_2\ge30$, $x_1, x_2\ge0$ [[8]]
<!-- SOLUTIONS -->

@s 1
Let $D$ be the determinant. Add $R_1$ to $R_2$ ($R_2\to R_2 + R_1$): the second row becomes $(a+b+c,\ a+b+c,\ a+b+c)$. Take $(a+b+c)$ common:

$$D = (a+b+c)\begin{vmatrix}a&b&c\\1&1&1\\a^2&b^2&c^2\end{vmatrix}$$

Interchange $R_1$ and $R_2$ (a sign change):

$$D = -(a+b+c)\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$$

Apply $C_1\to C_1 - C_2$ and $C_2\to C_2 - C_3$:

$$\begin{vmatrix}0&0&1\\a-b&b-c&c\\a^2-b^2&b^2-c^2&c^2\end{vmatrix} = (a-b)(b-c)\begin{vmatrix}0&0&1\\1&1&c\\a+b&b+c&c^2\end{vmatrix}$$

Expanding along the first row, the $3\times3$ determinant is $1\cdot\big[(b+c) - (a+b)\big] = c - a$. Hence

$$\begin{gathered}D = -(a+b+c)(a-b)(b-c)(c-a) = (a-b)(b-c)(a-c)(a+b+c) \\ \blacksquare\end{gathered}$$

@s 2
Let $A$ be an $n\times n$ matrix.

**Existence.** Write

$$A = \underbrace{\tfrac12(A + A^T)}_{P} + \underbrace{\tfrac12(A - A^T)}_{Q}$$

$P^T = \tfrac12(A^T + A) = P$, so $P$ is symmetric; $Q^T = \tfrac12(A^T - A) = -Q$, so $Q$ is skew-symmetric. Thus $A = P + Q$.

**Uniqueness.** Suppose also $A = R + S$ with $R$ symmetric ($R^T = R$) and $S$ skew-symmetric ($S^T = -S$). Taking the transpose, $A^T = R^T + S^T = R - S$. Therefore

$$\begin{gathered}A + A^T = 2R\ \Rightarrow\ R = \tfrac12(A + A^T) = P \\ A - A^T = 2S\ \Rightarrow\ S = \tfrac12(A - A^T) = Q\end{gathered}$$

So the decomposition is unique. $\blacksquare$

@s 3
Write the system as $AX = B$ with

$$A = \begin{bmatrix}5&3&7\\3&26&2\\7&2&10\end{bmatrix},\quad B = \begin{bmatrix}4\\9\\5\end{bmatrix}$$

**Consistency.** The system is consistent if $\operatorname{rank}A = \operatorname{rank}[A|B]$. Reduce the augmented matrix $[A|B]$ by $R_2\to5R_2 - 3R_1$ and $R_3\to5R_3 - 7R_1$:

$$\left[\begin{array}{ccc|c}5&3&7&4\\0&121&-11&33\\0&-11&1&-3\end{array}\right]$$

Now $R_2\to R_2 + 11R_3$:

$$\left[\begin{array}{ccc|c}5&3&7&4\\0&0&0&0\\0&-11&1&-3\end{array}\right]$$

Two non-zero rows remain, so $\operatorname{rank}A = \operatorname{rank}[A|B] = 2<3$ (also $|A| = 0$). The system is **consistent but has infinitely many solutions** ($3 - 2 = 1$ free variable).

**Solution.** From the third row, $-11y + z = -3$. Let $z = k$: $y = \dfrac{3 + k}{11}$. From the first row, $5x = 4 - 3y - 7z = 4 - \dfrac{9 + 3k}{11} - 7k = \dfrac{35 - 80k}{11}$, so $x = \dfrac{7 - 16k}{11}$.

$$\begin{gathered}\boxed{x = \frac{7 - 16k}{11},\quad y = \frac{3 + k}{11},\quad z = k\qquad(k\ \text{arbitrary})}\end{gathered}$$

*Check:* for $k = 0$, $(x, y, z) = (\tfrac7{11}, \tfrac3{11}, 0)$: $5x + 3y = \dfrac{35 + 9}{11} = 4$ ✓, $3x + 26y = \dfrac{21 + 78}{11} = 9$ ✓, $7x + 2y = \dfrac{49 + 6}{11} = 5$ ✓.

@s 4
$A$ is upper triangular, so its eigenvalues are its diagonal entries: the characteristic equation is $(1 - \lambda)(2 - \lambda)(3 - \lambda) = 0$:

$$\boxed{\lambda = 1,\ 2,\ 3}$$

**Eigenvectors**, from $(A - \lambda I)X = 0$:

*$\lambda = 1$:* $\begin{bmatrix}0&2&-1\\0&1&1\\0&0&2\end{bmatrix}X = 0\Rightarrow z = 0,\ y = 0$, $x$ free: $X_1 = (1, 0, 0)^T$.

*$\lambda = 2$:* $\begin{bmatrix}-1&2&-1\\0&0&1\\0&0&1\end{bmatrix}X = 0\Rightarrow z = 0,\ -x + 2y = 0$: $X_2 = (2, 1, 0)^T$.

*$\lambda = 3$:* $\begin{bmatrix}-2&2&-1\\0&-1&1\\0&0&0\end{bmatrix}X = 0\Rightarrow y = z,\ -2x + 2y - z = 0\Rightarrow x = \dfrac z2$: take $z = 2$, $X_3 = (1, 2, 2)^T$.

$$\begin{gathered}\boxed{X_1 = (1,0,0)^T,\quad X_2 = (2,1,0)^T,\quad X_3 = (1,2,2)^T}\end{gathered}$$

(each is determined up to a non-zero scalar multiple; $AX_i = \lambda_iX_i$ was verified.)

@s 5
**Irrotational.** $\nabla\times\vec F = \begin{vmatrix}\hat i&\hat j&\hat k\\\partial_x&\partial_y&\partial_z\\x^2 - yz&y^2 - zx&z^2 - xy\end{vmatrix}$:

- $\hat i$: $\dfrac{\partial}{\partial y}(z^2 - xy) - \dfrac{\partial}{\partial z}(y^2 - zx) = -x + x = 0$
- $\hat j$: $\dfrac{\partial}{\partial z}(x^2 - yz) - \dfrac{\partial}{\partial x}(z^2 - xy) = -y + y = 0$
- $\hat k$: $\dfrac{\partial}{\partial x}(y^2 - zx) - \dfrac{\partial}{\partial y}(x^2 - yz) = -z + z = 0$

So $\nabla\times\vec F = \vec 0$: $\vec F$ is irrotational. $\blacksquare$

**Scalar potential** $\phi$ with $\vec F = \nabla\phi$:

$$\begin{gathered}\frac{\partial\phi}{\partial x} = x^2 - yz\Rightarrow\phi = \frac{x^3}{3} - xyz + f(y, z)\end{gathered}$$

$$\begin{gathered}\frac{\partial\phi}{\partial y} = -xz + f_y = y^2 - zx\Rightarrow f_y = y^2\Rightarrow f = \frac{y^3}{3} + g(z)\end{gathered}$$

$$\begin{gathered}\frac{\partial\phi}{\partial z} = -xy + g'(z) = z^2 - xy\Rightarrow g = \frac{z^3}{3} + C\end{gathered}$$

$$\boxed{\phi = \frac{x^3 + y^3 + z^3}{3} - xyz + C}$$

@s 6
**Stokes' theorem:** $\displaystyle\iint_S(\nabla\times\vec F)\cdot\hat n\,ds = \oint_C\vec F\cdot d\vec r$, where $C$ is the closed boundary of $S$, traversed counter-clockwise when seen from the tip of $\hat n$.

The surface is the upper hemisphere, whose boundary is the circle $C: x^2 + y^2 = a^2$, $z = 0$. On $C$, $z = 0$ and $dz = 0$, so

$$\begin{gathered}\vec F\cdot d\vec r = y\,dx + x(1 - 0)\,dy - 0 = y\,dx + x\,dy = d(xy)\end{gathered}$$

Parametrise $x = a\cos t$, $y = a\sin t$, $0\le t\le2\pi$:

$$\begin{gathered}\oint_C d(xy) = \Big[xy\Big]_{t = 0}^{2\pi} = a^2\big[\sin t\cos t\big]_0^{2\pi} = 0\end{gathered}$$

$$\boxed{\iint_S(\nabla\times\vec F)\cdot\hat n\,ds = 0}$$

**Check by the surface integral.** $\nabla\times\vec F = (x,\ y,\ -2z)$ and $\hat n = \dfrac{(x, y, z)}{a}$, so $(\nabla\times\vec F)\cdot\hat n = \dfrac{x^2 + y^2 - 2z^2}{a}$. Over the hemisphere $\iint x^2\,ds = \iint y^2\,ds = \iint z^2\,ds = \dfrac{1}{3}a^2(2\pi a^2)$ by symmetry, so the integral of $x^2 + y^2 - 2z^2$ is $0$ ✓.

@s 7
**Green's theorem.** If $P(x,y)$ and $Q(x,y)$ have continuous first partial derivatives in a region $R$ of the $xy$-plane bounded by a simple closed piecewise smooth curve $C$ (traversed counter-clockwise), then

$$\boxed{\oint_C(P\,dx + Q\,dy) = \iint_R\left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dx\,dy}$$

**Proof** (for a region which is simple in both the $x$ and $y$ directions).

```figure caption="Question 7: region R bounded below by y = f1(x), above by y = f2(x), and between x = a and x = b (also described as x between g1(y) and g2(y))."
x=np.linspace(0,4,200); f1=0.6+0.35*np.sin(x*1.2); f2=2.6+0.4*np.cos(x*1.1)
fig,ax=plt.subplots(figsize=(4.4,2.6))
ax.fill_between(x,f1,f2,color='#dbe8f6',alpha=.9); ax.plot(x,f1,color='#1d6fb8',lw=1.8); ax.plot(x,f2,color='#1d6fb8',lw=1.8)
ax.plot([0,0],[f1[0],f2[0]],color='#1d6fb8',lw=1.8); ax.plot([4,4],[f1[-1],f2[-1]],color='#1d6fb8',lw=1.8)
ax.text(2,0.3,'$y=f_1(x)$',fontsize=8,ha='center'); ax.text(2,3.15,'$y=f_2(x)$',fontsize=8,ha='center'); ax.text(1.9,1.6,'R',fontsize=11,ha='center')
ax.annotate('',xy=(3.1,f1[155]),xytext=(2.5,f1[125]),arrowprops=dict(arrowstyle='->',color='#d9534f'))
ax.set_xticks([0,4]); ax.set_xticklabels(['a','b']); ax.set_yticks([]); ax.set_ylim(0,3.5); ax.spines[['top','right','left']].set_visible(False)
```

*Part 1: $\displaystyle\oint_CP\,dx = -\iint_R\frac{\partial P}{\partial y}\,dx\,dy$.* Let $R = \{a\le x\le b,\ f_1(x)\le y\le f_2(x)\}$. Then

$$\begin{gathered}\iint_R\frac{\partial P}{\partial y}\,dy\,dx = \int_a^b\Big[P(x,y)\Big]_{y = f_1(x)}^{f_2(x)}dx = \int_a^bP(x, f_2)\,dx - \int_a^bP(x, f_1)\,dx\end{gathered}$$

Along $C$ counter-clockwise, the lower curve $y = f_1$ is traversed from $a$ to $b$, the upper curve $y = f_2$ from $b$ to $a$, and on the vertical sides $dx = 0$. So

$$\begin{gathered}\oint_CP\,dx = \int_a^bP(x, f_1)\,dx + \int_b^aP(x, f_2)\,dx = -\left[\int_a^bP(x, f_2)\,dx - \int_a^bP(x, f_1)\,dx\right] = -\iint_R\frac{\partial P}{\partial y}\,dx\,dy\end{gathered}$$

*Part 2: $\displaystyle\oint_CQ\,dy = \iint_R\frac{\partial Q}{\partial x}\,dx\,dy$.* Describe $R$ also as $\{c\le y\le d,\ g_1(y)\le x\le g_2(y)\}$:

$$\iint_R\frac{\partial Q}{\partial x}\,dx\,dy = \int_c^d\big[Q(g_2, y) - Q(g_1, y)\big]dy$$

Counter-clockwise, the right curve $x = g_2$ is traversed upward ($c\to d$) and the left curve $x = g_1$ downward ($d\to c$); on the horizontal sides $dy = 0$:

$$\begin{gathered}\oint_CQ\,dy = \int_c^dQ(g_2, y)\,dy + \int_d^cQ(g_1, y)\,dy = \iint_R\frac{\partial Q}{\partial x}\,dx\,dy\end{gathered}$$

Adding the two parts gives Green's theorem. A region that is not simple is cut into simple pieces; the line integrals along the common cuts cancel (opposite directions), so the theorem holds for it too. $\blacksquare$

@s 8
**Gauss's divergence theorem:** $\displaystyle\iint_S\vec F\cdot\hat n\,ds = \iiint_V\nabla\cdot\vec F\,dV$ for a closed surface $S$ bounding the volume $V$ ($\hat n$ outward).

Here $\nabla\cdot\vec F = \dfrac{\partial x}{\partial x} + \dfrac{\partial y}{\partial y} + \dfrac{\partial z^2}{\partial z} = 1 + 1 + 2z = 2 + 2z$. The volume $V$ is the cylinder $x^2 + y^2\le9$, $0\le z\le2$; the cross-section has area $9\pi$:

$$\begin{gathered}\iiint_V(2 + 2z)\,dV = \int_0^2(2 + 2z)\,(9\pi)\,dz = 9\pi\Big[2z + z^2\Big]_0^2 = 9\pi(4 + 4)\end{gathered}$$

$$\boxed{\iint_S\vec F\cdot\hat n\,ds = 72\pi}$$

**Check by the three surfaces.** Top ($z = 2$, $\hat n = \hat k$): $\vec F\cdot\hat n = z^2 = 4$, area $9\pi$: $36\pi$. Bottom ($z = 0$, $\hat n = -\hat k$): $-z^2 = 0$: $0$. Curved surface ($\hat n = \frac{x\hat i + y\hat j}{3}$): $\vec F\cdot\hat n = \dfrac{x^2 + y^2}{3} = 3$, area $2\pi(3)(2) = 12\pi$: $36\pi$. Total $72\pi$ ✓.

@s 9
**Existence condition.** The Laplace transform $L\{f(t)\} = \displaystyle\int_0^\infty e^{-st}f(t)\,dt$ exists for $s > s_0$ if $f(t)$ is (i) piecewise (sectionally) continuous on every finite interval $[0, T]$ and (ii) of exponential order, i.e. there are constants $M, k$ with $|f(t)|\le Me^{kt}$ for all $t\ge T$ (then it exists for $s > k$). These are sufficient conditions (not necessary).

**(a)** $L\{\cosh at\} = \dfrac{s}{s^2 - a^2}$. By the multiplication-by-$t$ rule $L\{tf(t)\} = -\dfrac{d}{ds}F(s)$:

$$\begin{gathered}L\{t\cosh at\} = -\frac{d}{ds}\left[\frac{s}{s^2 - a^2}\right] = -\frac{(s^2 - a^2) - 2s^2}{(s^2 - a^2)^2}\end{gathered}$$

$$\boxed{L\{t\cosh at\} = \frac{s^2 + a^2}{(s^2 - a^2)^2}}$$

**(b)** $L\{\sin2t\} = \dfrac{2}{s^2 + 4}$. By the division-by-$t$ rule $L\left\{\dfrac{f(t)}{t}\right\} = \displaystyle\int_s^\infty F(u)\,du$:

$$\begin{gathered}L\left\{\frac{\sin2t}{t}\right\} = \int_s^\infty\frac{2\,du}{u^2 + 4} = \Big[\tan^{-1}\frac u2\Big]_s^\infty = \frac\pi2 - \tan^{-1}\frac s2\end{gathered}$$

$$\begin{gathered}\boxed{L\left\{\frac{\sin2t}{t}\right\} = \cot^{-1}\frac s2 = \tan^{-1}\frac2s}\end{gathered}$$

@s 10
**(i)** Let $F(s) = \log\dfrac{s+1}{s-1} = \log(s+1) - \log(s-1)$, so $F'(s) = \dfrac{1}{s+1} - \dfrac{1}{s-1}$. Then $L^{-1}\{F'(s)\} = e^{-t} - e^t = -2\sinh t$. Since $L\{tf(t)\} = -F'(s)$, i.e. $L^{-1}\{F'(s)\} = -tf(t)$:

$$\begin{gathered}-tf(t) = -2\sinh t\ \Longrightarrow\ \boxed{L^{-1}\left\{\log\frac{s+1}{s-1}\right\} = \frac{2\sinh t}{t}}\end{gathered}$$

**(ii)** Partial fractions: $\dfrac{s}{(s-3)(s^2+4)} = \dfrac{A}{s-3} + \dfrac{Bs + C}{s^2 + 4}$, so $s = A(s^2 + 4) + (Bs + C)(s - 3)$.

Put $s = 3$: $3 = 13A\Rightarrow A = \dfrac{3}{13}$. Coefficient of $s^2$: $A + B = 0\Rightarrow B = -\dfrac3{13}$. Constant: $4A - 3C = 0\Rightarrow C = \dfrac{4}{13}$. (Check: coefficient of $s$: $-3B + C = \dfrac{9 + 4}{13} = 1$ ✓.)

$$L^{-1}\{\cdot\} = \frac3{13}e^{3t} - \frac{3}{13}\cos2t + \frac{4}{13}\cdot\frac12\sin2t$$

$$\boxed{\frac{3}{13}e^{3t} - \frac3{13}\cos2t + \frac{2}{13}\sin2t}$$

@s 11
Take the Laplace transform of $y'' - 3y' + 2y = e^{3t}$ with $y(0) = 0$, $y'(0) = 1$, writing $Y = L\{y\}$:

$$\big[s^2Y - sy(0) - y'(0)\big] - 3\big[sY - y(0)\big] + 2Y = \frac{1}{s - 3}$$

$$\begin{gathered}(s^2 - 3s + 2)Y - 1 = \frac1{s - 3}\ \Longrightarrow\ (s-1)(s-2)Y = \frac{s - 2}{s - 3}\end{gathered}$$

$$\begin{gathered}Y = \frac{1}{(s-1)(s-3)} = \frac12\left[\frac{1}{s - 3} - \frac{1}{s - 1}\right]\end{gathered}$$

Inverting:

$$\boxed{y(t) = \frac12\big(e^{3t} - e^t\big)}$$

*Check:* $y(0) = 0$; $y' = \tfrac12(3e^{3t} - e^t)$, $y'(0) = 1$ ✓; $y'' - 3y' + 2y = \tfrac12\big[(9 - 9 + 2)e^{3t} + (-1 + 3 - 2)e^t\big] = e^{3t}$ ✓.

@s 12
On $0\le x\le2\pi$ (period $2\pi$): $f(x) = a_0/2 + \sum(a_n\cos nx + b_n\sin nx)$ with

$$\begin{gathered}a_0 = \frac1\pi\int_0^{2\pi}\frac{(\pi - x)^2}{4}\,dx = \frac{1}{4\pi}\left[-\frac{(\pi - x)^3}{3}\right]_0^{2\pi} = \frac{1}{4\pi}\cdot\frac{2\pi^3}{3} = \frac{\pi^2}{6}\end{gathered}$$

$$a_n = \frac1{4\pi}\int_0^{2\pi}(\pi - x)^2\cos nx\,dx$$

Integrate by parts twice (with $u = (\pi - x)^2$): the boundary terms $\big[(\pi - x)^2\frac{\sin nx}{n}\big]_0^{2\pi}$ vanish, so

$$\begin{gathered}\int_0^{2\pi}(\pi - x)^2\cos nx\,dx = \frac2n\int_0^{2\pi}(\pi - x)\sin nx\,dx = \frac2n\left\{\left[-\frac{(\pi - x)\cos nx}{n}\right]_0^{2\pi} - \frac1n\int_0^{2\pi}\cos nx\,dx\right\} = \frac2n\cdot\frac{2\pi}{n} = \frac{4\pi}{n^2}\end{gathered}$$

$$\begin{gathered}a_n = \frac{1}{4\pi}\cdot\frac{4\pi}{n^2} = \frac{1}{n^2}\end{gathered}$$

$b_n = \dfrac{1}{4\pi}\displaystyle\int_0^{2\pi}(\pi - x)^2\sin nx\,dx = 0$, because $(\pi - x)^2$ is symmetric about $x = \pi$ while $\sin nx$ is antisymmetric about $\pi$ (equivalently, substituting $x = \pi + u$ gives an odd integrand over $[-\pi, \pi]$).

$$\begin{gathered}\boxed{\left(\frac{\pi - x}{2}\right)^2 = \frac{\pi^2}{12} + \sum_{n=1}^\infty\frac{\cos nx}{n^2} = \frac{\pi^2}{12} + \cos x + \frac{\cos2x}{4} + \frac{\cos3x}{9} + \cdots}\end{gathered}$$

(*Check:* at $x = 0$, $\dfrac{\pi^2}{4} = \dfrac{\pi^2}{12} + \sum\dfrac1{n^2}$ gives the classical $\sum\dfrac1{n^2} = \dfrac{\pi^2}{6}$ ✓.)

@s 13
The half-range sine series is $f(x) = \displaystyle\sum_{n=1}^\infty b_n\sin nx$ with $b_n = \dfrac2\pi\displaystyle\int_0^\pi(\pi x - x^2)\sin nx\,dx$.

Using $\displaystyle\int_0^\pi x\sin nx\,dx = \frac{\pi(-1)^{n+1}}{n}$ and $\displaystyle\int_0^\pi x^2\sin nx\,dx = \frac{\pi^2(-1)^{n+1}}{n} + \frac{2\big[(-1)^n - 1\big]}{n^3}$:

$$\begin{gathered}\int_0^\pi(\pi x - x^2)\sin nx\,dx = \frac{\pi^2(-1)^{n+1}}{n} - \frac{\pi^2(-1)^{n+1}}{n} - \frac{2[(-1)^n - 1]}{n^3} = \frac{2\big[1 - (-1)^n\big]}{n^3}\end{gathered}$$

$$b_n = \frac{4\big[1 - (-1)^n\big]}{\pi n^3} = \begin{cases}\dfrac{8}{\pi n^3}&n\ \text{odd}\\[2mm]0&n\ \text{even}\end{cases}$$

So the first three non-zero terms ($n = 1, 3, 5$; the $n = 2, 4$ terms vanish) are

$$\boxed{\pi x - x^2 = \frac8\pi\left[\sin x + \frac{\sin3x}{27} + \frac{\sin5x}{125} + \cdots\right],\quad0<x<\pi}$$

(*Check:* at $x = \pi/2$, $\dfrac{\pi^2}{4} = \dfrac8\pi\left(1 - \dfrac1{27} + \dfrac{1}{125} - \cdots\right)$, i.e. $\dfrac{\pi^3}{32} = 1 - \dfrac1{27} + \dfrac1{125} - \cdots = 0.9689$ ✓.)

@s 14
**Primal:** Minimize $Z = 21x + 50y$ subject to $2x + 5y\ge12$, $3x + 7y\ge17$, $x, y\ge0$.

**Constructing the dual.** For a minimisation problem with all constraints of the $\ge$ type, the dual (variables $u, v$, one for each primal constraint) is: the objective coefficients are the right-hand sides, and the right-hand sides are the primal costs (the coefficient matrix is transposed):

$$\begin{gathered}\text{Maximize }W = 12u + 17v\quad\text{subject to}\quad2u + 3v\le21,\ \ 5u + 7v\le50,\ \ u, v\ge0\end{gathered}$$

**Simplex method on the dual.** Add slack variables $s_1, s_2$: $2u + 3v + s_1 = 21$, $5u + 7v + s_2 = 50$.

**Table 1**

| Basis | u | v | s1 | s2 | RHS |
|---|---|---|---|---|---|
| s1 | 2 | 3 | 1 | 0 | 21 |
| s2 | 5 | 7 | 0 | 1 | 50 |
| Z | -12 | -17 | 0 | 0 | 0 |

Entering v, leaving s1 (pivot 3).

**Table 2**

| Basis | u | v | s1 | s2 | RHS |
|---|---|---|---|---|---|
| v | 2/3 | 1 | 1/3 | 0 | 7 |
| s2 | 1/3 | 0 | -7/3 | 1 | 1 |
| Z | -2/3 | 0 | 17/3 | 0 | 119 |

Entering u, leaving s2 (pivot 1/3).

**Table 3**

| Basis | u | v | s1 | s2 | RHS |
|---|---|---|---|---|---|
| v | 0 | 1 | 5 | -2 | 5 |
| u | 1 | 0 | -7 | 3 | 3 |
| Z | 0 | 0 | 1 | 2 | 121 |


All entries of the $Z$-row are now $\ge0$, so the dual is optimal:

$$\begin{gathered}u = 3,\quad v = 5,\quad W_{\max} = 12(3) + 17(5) = 121\end{gathered}$$

**Reading the primal solution.** The optimal values of the primal variables are the entries of the $Z$-row under the slack columns $s_1, s_2$ of the final dual table: $x = 1$, $y = 2$, and by the duality theorem $Z_{\min} = W_{\max}$.

$$\begin{gathered}\boxed{x = 1,\quad y = 2,\quad Z_{\min} = 21(1) + 50(2) = 121}\end{gathered}$$

**Check:** $2(1) + 5(2) = 12\ge12$ ✓ (binding) and $3(1) + 7(2) = 17\ge17$ ✓ (binding); both dual variables are positive, which agrees with both primal constraints being binding (complementary slackness).

@s 15
**Maximize $Z = 4x_1 + 5x_2$ subject to $x_1 + x_2\le5$, $3x_1 + 10x_2\ge30$, $x_1, x_2\ge0$.**

**Standard form (Big-M).** Add a slack $s_1$ to the first constraint; subtract a surplus $s_2$ from the second and add an artificial variable $A_1$ (penalised by $-M$ in the objective, $M$ very large):

$$\text{Max }Z = 4x_1 + 5x_2 + 0s_1 + 0s_2 - MA_1$$

$$\begin{gathered}x_1 + x_2 + s_1 = 5 \\ 3x_1 + 10x_2 - s_2 + A_1 = 30\end{gathered}$$

The initial basic feasible solution is $s_1 = 5$, $A_1 = 30$. Writing the objective as $Z - 4x_1 - 5x_2 + MA_1 = 0$ and eliminating $A_1$ from the $Z$-row ($R_Z\to R_Z - M\cdot R_{A_1}$) gives Table 1 (the entering variable is the one with the most negative $Z$-row entry, treating $M$ as huge; the leaving variable has the least ratio RHS/pivot column).

**Table 1**

| Basis | x1 | x2 | s1 | s2 | A1 | RHS |
|---|---|---|---|---|---|---|
| s1 | 1 | 1 | 1 | 0 | 0 | 5 |
| A1 | 3 | 10 | 0 | -1 | 1 | 30 |
| Z | -3M - 4 | -10M - 5 | 0 | M | 0 | -30M |

Entering x2, leaving A1 (pivot 10).

**Table 2**

| Basis | x1 | x2 | s1 | s2 | A1 | RHS |
|---|---|---|---|---|---|---|
| s1 | 7/10 | 0 | 1 | 1/10 | -1/10 | 2 |
| x2 | 3/10 | 1 | 0 | -1/10 | 1/10 | 3 |
| Z | -5/2 | 0 | 0 | -1/2 | M + 1/2 | 15 |

Entering x1, leaving s1 (pivot 7/10).

**Table 3**

| Basis | x1 | x2 | s1 | s2 | A1 | RHS |
|---|---|---|---|---|---|---|
| x1 | 1 | 0 | 10/7 | 1/7 | -1/7 | 20/7 |
| x2 | 0 | 1 | -3/7 | -1/7 | 1/7 | 15/7 |
| Z | 0 | 0 | 25/7 | -1/7 | M + 1/7 | 155/7 |

Entering s2, leaving x1 (pivot 1/7).

**Table 4**

| Basis | x1 | x2 | s1 | s2 | A1 | RHS |
|---|---|---|---|---|---|---|
| s2 | 7 | 0 | 10 | 1 | -1 | 20 |
| x2 | 1 | 1 | 1 | 0 | 0 | 5 |
| Z | 1 | 0 | 5 | 0 | M | 25 |


In Table 4 every entry in the $Z$-row is $\ge0$ (the artificial variable has left the basis and stays at $0$), so the solution is optimal:

$$\begin{gathered}\boxed{x_1 = 0,\quad x_2 = 5,\quad Z_{\max} = 25}\end{gathered}$$

(with surplus $s_2 = 20$, i.e. $3x_1 + 10x_2 = 50\ge30$).

**Graphical check.** The feasible region is the triangle with corners $(0, 3)$, $(0, 5)$ and $\left(\tfrac{20}{7}, \tfrac{15}{7}\right)$: $Z = 15$, $25$ and $\tfrac{155}{7}\approx22.1$ respectively, so the maximum is $25$ at $(0, 5)$ ✓.

```figure caption="Question 15: feasible region (shaded) of x1 + x2 <= 5, 3x1 + 10x2 >= 30, with the optimum at (0, 5), Z = 25."
x=np.linspace(0,6,100)
fig,ax=plt.subplots(figsize=(4.4,3.0))
ax.plot(x,5-x,color='#1d6fb8',lw=1.6); ax.plot(x,(30-3*x)/10,color='#2e8b57',lw=1.6)
xs=np.linspace(0,20/7,50); ax.fill_between(xs,(30-3*xs)/10,5-xs,color='#dbe8f6',alpha=.9)
ax.plot([0,0,20/7],[3,5,15/7],'o',color='#14181f',ms=4)
ax.text(.1,5.15,'(0, 5)  Z = 25',fontsize=8); ax.text(.1,2.55,'(0, 3)  Z = 15',fontsize=8); ax.text(2.95,2.0,'(20/7, 15/7)  Z = 22.1',fontsize=8)
ax.text(4.1,0.7,'$x_1 + x_2 = 5$',fontsize=8,color='#1d6fb8'); ax.text(3.3,2.8,'$3x_1 + 10x_2 = 30$',fontsize=8,color='#2e8b57')
ax.set_xlim(0,6); ax.set_ylim(0,6); ax.set_xlabel('$x_1$'); ax.set_ylabel('$x_2$'); ax.tick_params(labelsize=7); ax.spines[['top','right']].set_visible(False)
```

---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-SH451-2080-Ashwin.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: SH 451
year_bs: 2080 Ashwin
cal: BS
year_ad: 2023
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 451). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
State Euler's theorem for a homogeneous function of two variables of degree $n$. If $u = \sin^{-1}\left(\dfrac{\sqrt x - \sqrt y}{\sqrt x + \sqrt y}\right)$, show that $x\dfrac{\partial u}{\partial x} + y\dfrac{\partial u}{\partial y} = 0$. [[5]]

@q 2
Find the extreme value of $x^2 + y^2 + z^2$ subject to the conditions $x + z = 1$, $2y + z = 2$. [[5]]

@q 3
Evaluate $\displaystyle\int_0^a\int_0^{\sqrt{a^2-x^2}} y^2\sqrt{x^2+y^2}\,dy\,dx$ by changing it into polar form. [[5]]

@q 4
Using a multiple integral, find the volume bounded by the cylinder $x^2 + y^2 = 4$ between the planes $y + z = 8$ and $z = 1$. [[5]]

@q 5
Find the image of the point $(2,-1,3)$ in the plane $3x - 2y - z = 9$. [[5]]

@q 6
Define coplanar lines and skew lines. Show that the lines $\dfrac x1 = \dfrac{y-2}{2} = \dfrac{z+3}{3}$ and $\dfrac{x-2}{2} = \dfrac{y-6}{3} = \dfrac{z-3}{4}$ are coplanar and also find their point of intersection and the equation of the common plane. [[5]]

@q 7
Obtain the equation of the sphere through the circle $x^2 + y^2 + z^2 = 9$, $x - 2y + 2z = 5$, as the great circle. Also determine its centre and radius. [[5]]

@q 8
Obtain the equation of the right circular cylinder of radius $4$ and axis the line $x = 2y = -z$. [[5]]

@q 9
Define a power series. Apply it to solve the differential equation $y'' + xy' + y = 0$. [[5]]

@q 10
Express the function $f(x) = x^3 + 5x^2 + 4x + 1$ in terms of Legendre's polynomials. [[5]]

@q 11
Prove that Bessel's function $J_{5/2}(x) = \sqrt{\dfrac{2}{\pi x}}\left\{\dfrac{3-x^2}{x^2}\sin x - \dfrac3x\cos x\right\}$, where the symbols have their usual meanings. [[5]]

@q 12
Define scalar triple product and vector triple product for vectors. Prove that $[\vec a+\vec b,\ \vec b+\vec c,\ \vec c+\vec a] = 2[\vec a,\ \vec b,\ \vec c]$. [[5]]

@q 13
Prove that the necessary and sufficient condition for a vector function $\vec a$ in the variable $t$ to have constant direction is $\vec a\times\dfrac{d\vec a}{dt} = \vec 0$. [[5]]

@q 14
Find the directional derivative of $\phi = x^2 - y^2 + z^2$ at the point $A(1,-3,2)$ in the direction of $\overrightarrow{AB}$, where $B$ is the point $(4,5,7)$. [[5]]

@q 15
Test for the convergence of the series $1 + \dfrac1{2^2} + \dfrac{2^2}{3^3} + \dfrac{3^3}{4^4} + \dfrac{4^4}{5^5} + \cdots$ [[5]]

@q 16
Find the interval and radius of convergence of the power series $\displaystyle\sum_{n=1}^\infty\frac{(-1)^n(2x+1)^n}{3^n}$. [[5]]
<!-- SOLUTIONS -->

@s 1
**Euler's theorem.** If $f(x,y)$ is a homogeneous function of degree $n$ with continuous first-order partial derivatives, then
$$x\frac{\partial f}{\partial x} + y\frac{\partial f}{\partial y} = nf$$

**Proof sketch.** Put $f(tx,ty) = t^nf(x,y)$ and differentiate with respect to $t$ at $t = 1$: the left side gives $xf_x + yf_y$ by the chain rule and the right side gives $nf$.

**Application.** Let $z = \sin u = \dfrac{\sqrt x-\sqrt y}{\sqrt x+\sqrt y}$. Replacing $x,y$ by $tx,ty$ gives $\dfrac{\sqrt t(\sqrt x-\sqrt y)}{\sqrt t(\sqrt x+\sqrt y)} = z$, so $z$ is homogeneous of degree $0$. By Euler's theorem
$$xz_x + yz_y = 0\cdot z = 0$$
Since $z = \sin u$, $z_x = \cos u\,u_x$ and $z_y = \cos u\,u_y$. Hence
$$\cos u\left(x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y}\right) = 0\quad\Longrightarrow\quad x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = 0$$
(where $\cos u\ne0$).
$$\boxed{x\,u_x + y\,u_y = 0}$$

@s 2
**Method 1: elimination.** From the conditions, $x = 1 - z$ and $y = \dfrac{2-z}{2}$, so with $z = t$
$$f(t) = (1-t)^2 + \frac{(2-t)^2}{4} + t^2$$
$$f'(t) = -2(1-t) - \frac{2-t}{2} + 2t = \frac92t - 3 = 0\ \Rightarrow\ t = \frac23$$
$f''(t) = \dfrac92 > 0$, so this is a **minimum**. Then $z = \dfrac23$, $x = \dfrac13$, $y = \dfrac23$ and
$$f = \frac19 + \frac49 + \frac49 = 1$$

**Method 2: Lagrange multipliers.** $F = x^2+y^2+z^2 + \lambda(x+z-1) + \mu(2y+z-2)$. Then
$$2x + \lambda = 0,\quad 2y + 2\mu = 0,\quad 2z + \lambda + \mu = 0$$
so $x = -\lambda/2$, $y = -\mu$, $z = -(\lambda+\mu)/2$. The constraints $x+z=1$ and $2y+z=2$ give $2\lambda + \mu = -2$ and $\lambda + 5\mu = -4$. Solving, $\lambda = \mu = -\dfrac23$. Then $(x,y,z) = \left(\dfrac13,\dfrac23,\dfrac23\right)$, the same point.
$$\boxed{\text{Extreme (minimum) value} = 1\ \text{at}\ \left(\tfrac13,\tfrac23,\tfrac23\right)}$$

@s 3
The region is the quarter disc $x^2+y^2\le a^2$ in the first quadrant: $0\le r\le a$, $0\le\theta\le\dfrac\pi2$. With $x = r\cos\theta$, $y = r\sin\theta$, $dy\,dx = r\,dr\,d\theta$:

```figure caption="Question 3: the region of integration is the quarter disc of radius a in the first quadrant, so 0 ≤ r ≤ a and 0 ≤ θ ≤ π/2."
t=np.linspace(0,np.pi/2,100)
fig,ax=plt.subplots(figsize=(3.4,3.4))
ax.fill(np.r_[0,np.cos(t),0],np.r_[0,np.sin(t),0],color='#1d6fb8',alpha=0.15)
ax.plot(np.cos(t),np.sin(t),color='#1d6fb8'); ax.plot([0,1],[0,0],color='#14181f'); ax.plot([0,0],[0,1],color='#14181f')
ax.plot([0,0.8],[0,0.6],color='#d9534f',lw=1.4); ax.text(0.45,0.2,'$r$',color='#d9534f',fontsize=9)
ax.text(1.02,-0.06,'$a$',fontsize=9); ax.text(-0.08,1.0,'$a$',fontsize=9); ax.text(0.28,0.07,'$\\theta$',fontsize=8)
ax.set_xlim(-0.15,1.2); ax.set_ylim(-0.15,1.2); ax.set_aspect('equal')
for s in ('top','right'): ax.spines[s].set_visible(False)
```

$$I = \int_0^{\pi/2}\int_0^a (r^2\sin^2\theta)\,r\,(r\,dr\,d\theta) = \int_0^{\pi/2}\sin^2\theta\,d\theta\int_0^a r^4\,dr$$
$$\begin{gathered}\int_0^{\pi/2}\sin^2\theta\,d\theta = \frac\pi4 \\ \int_0^ar^4\,dr = \frac{a^5}5\end{gathered}$$
$$\boxed{I = \frac{\pi a^5}{20}}$$

@s 4
The solid stands on the disc $D: x^2+y^2\le4$; its bottom is the plane $z=1$ and its top is the plane $z = 8 - y$. The height at $(x,y)$ is $(8-y) - 1 = 7 - y$ (positive on $D$ since $|y|\le2$).
$$V = \iint_D(7-y)\,dA = 7\iint_DdA - \iint_Dy\,dA$$
$\iint_D dA = \pi(2)^2 = 4\pi$, and $\iint_Dy\,dA = 0$ because $D$ is symmetric about the $x$-axis ($y$ is odd). In polar form the same result: $\displaystyle\int_0^{2\pi}\int_0^2(7-r\sin\theta)\,r\,dr\,d\theta = 7\cdot2\pi\cdot2 - 0 = 28\pi$.
$$\boxed{V = 28\pi\ \text{cubic units}\approx 87.96}$$

@s 5
Let $P = (2,-1,3)$ and the plane be $3x - 2y - z - 9 = 0$ with normal $\vec n = (3,-2,-1)$.

The foot of the perpendicular and the image lie on the line $\dfrac{x-2}{3} = \dfrac{y+1}{-2} = \dfrac{z-3}{-1} = k$, i.e. $Q = (2+3k,\ -1-2k,\ 3-k)$. Substituting $Q$ into the plane for the **foot**:
$$3(2+3k) - 2(-1-2k) - (3-k) - 9 = 14k - 4 = 0\ \Rightarrow\ k = \frac27$$
The foot is $\left(\dfrac{20}7,-\dfrac{11}7,\dfrac{19}7\right)$. The image corresponds to twice this parameter, $k = \dfrac47$:
$$\text{Image} = \left(2 + \frac{12}7,\ -1 - \frac87,\ 3 - \frac47\right)$$
$$\boxed{\text{Image} = \left(\frac{26}7,\ -\frac{15}7,\ \frac{17}7\right)}$$
Check: at the image, $3\cdot\frac{26}{7} - 2\cdot\left(-\frac{15}{7}\right) - \frac{17}{7} - 9 = \frac{91}{7} - 9 = +4$, the negative of the value $-4$ at $P$, as it should be for a mirror image.

@s 6
**Definitions.** Two straight lines are **coplanar** if they lie in one plane (they either intersect or are parallel). Two lines that are not coplanar, so that they neither intersect nor are parallel, are **skew lines**.

**Data.** Line 1 passes through $A(0,2,-3)$ with direction $\vec d_1 = (1,2,3)$; line 2 passes through $B(2,6,3)$ with $\vec d_2 = (2,3,4)$. $\overrightarrow{AB} = (2,4,6)$.

**Coplanarity.**
$$\begin{vmatrix}2&4&6\\1&2&3\\2&3&4\end{vmatrix} = 2(8-9) - 4(4-6) + 6(3-4) = -2 + 8 - 6 = 0$$
so the lines are coplanar. (They are not parallel since $\vec d_1\not\parallel\vec d_2$, so they intersect.)

**Point of intersection.** A point of line 1 is $(\lambda,\ 2+2\lambda,\ -3+3\lambda)$ and of line 2 is $(2+2\mu,\ 6+3\mu,\ 3+4\mu)$. Equating,
$$\begin{gathered}\lambda = 2+2\mu \\ 2+2\lambda = 6+3\mu \\ -3+3\lambda = 3+4\mu\end{gathered}$$
The first two give $2 + 4 + 4\mu = 6 + 3\mu$, so $\mu = 0$ and $\lambda = 2$; the third holds ($3 = 3$). The point of intersection is $(2,6,3)$.

**Common plane.** The normal is
$$\vec n = \vec d_1\times\vec d_2 = \begin{vmatrix}\hat i&\hat j&\hat k\\1&2&3\\2&3&4\end{vmatrix} = (8-9,\ 6-4,\ 3-4) = (-1,2,-1)$$
The plane through $A(0,2,-3)$: $-x + 2(y-2) - (z+3) = 0$, i.e.
$$\boxed{x - 2y + z + 7 = 0}$$
Check with $B(2,6,3)$: $2-12+3+7 = 0$ ✓.
$$\boxed{\text{Point of intersection }(2,6,3)}$$

@s 7
Every sphere through the circle $x^2+y^2+z^2 = 9$, $x-2y+2z = 5$ has the form
$$x^2+y^2+z^2 - 9 + \lambda(x - 2y + 2z - 5) = 0$$
Its centre is $\left(-\dfrac\lambda2,\ \lambda,\ -\lambda\right)$. For the given circle to be a **great circle**, the centre must lie in the plane $x-2y+2z = 5$:
$$-\frac\lambda2 - 2\lambda - 2\lambda = 5\ \Rightarrow\ -\frac{9\lambda}2 = 5\ \Rightarrow\ \lambda = -\frac{10}9$$
The sphere is
$$x^2+y^2+z^2 - 9 - \frac{10}9(x - 2y + 2z - 5) = 0$$
$$\boxed{9(x^2+y^2+z^2) - 10x + 20y - 20z - 31 = 0}$$
**Centre:** $\left(-\dfrac\lambda2,\lambda,-\lambda\right)$ with $\lambda = -\dfrac{10}9$ gives $\left(\dfrac59,\ -\dfrac{10}9,\ \dfrac{10}9\right)$.

**Radius:**
$$r^2 = \frac{25}{81} + \frac{100}{81} + \frac{100}{81} + \frac{31}9 = \frac{225 + 279}{81} = \frac{56}9$$
$$\boxed{r = \frac{\sqrt{56}}3 = \frac{2\sqrt{14}}3\approx2.494}$$
Check: the radius of the given circle is $\sqrt{9 - (5/3)^2} = \sqrt{56}/3$ since the distance of the origin from the plane is $5/\sqrt{1+4+4} = 5/3$. A great circle has the same radius as the sphere ✓.

@s 8
The axis $x = 2y = -z$ can be written $\dfrac x2 = \dfrac y1 = \dfrac z{-2}$ (dividing by 2), through the origin with direction $\vec d = (2,1,-2)$, $|\vec d| = 3$.

A point $P(x,y,z)$ lies on the cylinder when its distance from the axis is $4$: $|\vec r\times\vec d|^2 = 16|\vec d|^2$.
$$\vec r\times\vec d = \begin{vmatrix}\hat i&\hat j&\hat k\\x&y&z\\2&1&-2\end{vmatrix} = (-2y - z,\ 2z + 2x,\ x - 2y)$$
$$(2y+z)^2 + 4(x+z)^2 + (x-2y)^2 = 16\cdot9 = 144$$
Expanding,
$$4y^2 + 4yz + z^2 + 4x^2 + 8xz + 4z^2 + x^2 - 4xy + 4y^2 = 144$$
$$\boxed{5x^2 + 8y^2 + 5z^2 - 4xy + 4yz + 8zx = 144}$$
Check by the other form $x^2+y^2+z^2 - \dfrac{(2x+y-2z)^2}{9} = 16$, which expands to the same equation.

@s 9
**Power series.** An infinite series $\sum_{n=0}^\infty a_n(x-x_0)^n = a_0 + a_1(x-x_0) + a_2(x-x_0)^2 + \cdots$ is called a power series in $(x - x_0)$; it converges for $|x-x_0|<R$, where $R$ is its radius of convergence.

**Solution of $y'' + xy' + y = 0$.** Let $y = \displaystyle\sum_{n=0}^\infty a_nx^n$, so $y' = \sum na_nx^{n-1}$, $y'' = \sum n(n-1)a_nx^{n-2}$. Then
$$\sum_{n=0}^\infty(n+2)(n+1)a_{n+2}x^n + \sum_{n=0}^\infty na_nx^n + \sum_{n=0}^\infty a_nx^n = 0$$
Equating the coefficient of $x^n$ to zero:
$$(n+2)(n+1)a_{n+2} + (n+1)a_n = 0\ \Rightarrow\ a_{n+2} = -\frac{a_n}{n+2}$$
$a_0$ and $a_1$ are arbitrary.

*Even coefficients:* $a_2 = -\dfrac{a_0}2$, $a_4 = \dfrac{a_0}{2\cdot4}$, $a_6 = -\dfrac{a_0}{2\cdot4\cdot6}$, so $a_{2k} = \dfrac{(-1)^ka_0}{2^kk!}$.

*Odd coefficients:* $a_3 = -\dfrac{a_1}3$, $a_5 = \dfrac{a_1}{3\cdot5}$, $a_7 = -\dfrac{a_1}{3\cdot5\cdot7}$, so $a_{2k+1} = \dfrac{(-1)^ka_1}{3\cdot5\cdots(2k+1)}$.

$$\boxed{y = a_0\left(1 - \frac{x^2}2 + \frac{x^4}8 - \frac{x^6}{48} + \cdots\right) + a_1\left(x - \frac{x^3}3 + \frac{x^5}{15} - \frac{x^7}{105} + \cdots\right)}$$
The first series is $e^{-x^2/2}$, so $y = a_0e^{-x^2/2} + a_1\left(x - \dfrac{x^3}3 + \dfrac{x^5}{15} - \cdots\right)$.

@s 10
Legendre polynomials: $P_0 = 1$, $P_1 = x$, $P_2 = \dfrac{3x^2-1}2$, $P_3 = \dfrac{5x^3-3x}2$. Solving for the powers,
$$\begin{gathered}x^2 = \frac{2P_2 + P_0}3 \\ x^3 = \frac{2P_3 + 3P_1}5\end{gathered}$$
$$f(x) = \frac{2P_3+3P_1}5 + \frac{5(2P_2+P_0)}3 + 4P_1 + P_0$$
Collecting terms:
$$\boxed{f(x) = \frac25P_3(x) + \frac{10}3P_2(x) + \frac{23}5P_1(x) + \frac83P_0(x)}$$
Check at $x = 1$ (all $P_n(1) = 1$): the coefficients add up to $\dfrac25 + \dfrac{23}5 + \dfrac{10}3 + \dfrac83 = 5 + 6 = 11 = f(1)$ ✓.

@s 11
Bessel's function of order $n$: $J_n(x) = \displaystyle\sum_{r=0}^\infty\frac{(-1)^r}{r!\,\Gamma(n+r+1)}\left(\frac x2\right)^{n+2r}$.

Using $\Gamma\!\left(r+\tfrac32\right) = \dfrac{(2r+1)!\sqrt\pi}{2^{2r+1}\,r!}$ and $\Gamma\!\left(r+\tfrac12\right) = \dfrac{(2r)!\sqrt\pi}{4^r\,r!}$ in the series,
$$\begin{gathered}J_{1/2}(x) = \sqrt{\frac2{\pi x}}\sum_{r}\frac{(-1)^rx^{2r+1}}{(2r+1)!} = \sqrt{\frac2{\pi x}}\sin x \\ J_{-1/2}(x) = \sqrt{\frac2{\pi x}}\sum_{r}\frac{(-1)^rx^{2r}}{(2r)!} = \sqrt{\frac2{\pi x}}\cos x\end{gathered}$$
The recurrence relation is $J_{n+1}(x) = \dfrac{2n}xJ_n(x) - J_{n-1}(x)$.

For $n = \tfrac12$:
$$J_{3/2} = \frac1xJ_{1/2} - J_{-1/2} = \sqrt{\frac2{\pi x}}\left(\frac{\sin x}x - \cos x\right)$$
For $n = \tfrac32$:
$$J_{5/2} = \frac3xJ_{3/2} - J_{1/2} = \sqrt{\frac2{\pi x}}\left[\frac{3\sin x}{x^2} - \frac{3\cos x}x - \sin x\right]$$
$$\boxed{J_{5/2}(x) = \sqrt{\frac2{\pi x}}\left\{\frac{3-x^2}{x^2}\sin x - \frac3x\cos x\right\}}$$

@s 12
**Scalar triple product.** For vectors $\vec a,\vec b,\vec c$, $[\vec a\ \vec b\ \vec c] = \vec a\cdot(\vec b\times\vec c)$, a scalar equal to the (signed) volume of the parallelepiped on them. It equals $\begin{vmatrix}a_1&a_2&a_3\\b_1&b_2&b_3\\c_1&c_2&c_3\end{vmatrix}$ and is unchanged by cyclic permutation.

**Vector triple product.** $\vec a\times(\vec b\times\vec c) = (\vec a\cdot\vec c)\vec b - (\vec a\cdot\vec b)\vec c$, a vector lying in the plane of $\vec b$ and $\vec c$.

**Proof.**
$$(\vec b+\vec c)\times(\vec c+\vec a) = \vec b\times\vec c + \vec b\times\vec a + \vec c\times\vec c + \vec c\times\vec a = \vec b\times\vec c - \vec a\times\vec b + \vec c\times\vec a$$
Taking the dot product with $(\vec a+\vec b)$ and using $\vec x\cdot(\vec x\times\vec y) = 0$:

- $\vec a\cdot(\vec b\times\vec c) = [\vec a\ \vec b\ \vec c]$, $\ \vec a\cdot(\vec a\times\vec b) = 0$, $\ \vec a\cdot(\vec c\times\vec a) = 0$,
- $\vec b\cdot(\vec b\times\vec c) = 0$, $\ \vec b\cdot(\vec a\times\vec b) = 0$, $\ \vec b\cdot(\vec c\times\vec a) = [\vec a\ \vec b\ \vec c]$.

$$\boxed{[\vec a+\vec b,\ \vec b+\vec c,\ \vec c+\vec a] = 2[\vec a\ \vec b\ \vec c]}$$

@s 13
**Necessity.** If $\vec a$ has constant direction, $\vec a = s(t)\,\hat e$ with $\hat e$ a constant unit vector. Then $\dfrac{d\vec a}{dt} = s'\hat e$ and
$$\vec a\times\frac{d\vec a}{dt} = ss'(\hat e\times\hat e) = \vec 0$$

**Sufficiency.** Let $\vec a = a\hat u$ where $a = |\vec a|$ and $\hat u$ is the unit vector along $\vec a$. Then $\dfrac{d\vec a}{dt} = a'\hat u + a\dfrac{d\hat u}{dt}$ and
$$\vec a\times\frac{d\vec a}{dt} = aa'(\hat u\times\hat u) + a^2\left(\hat u\times\frac{d\hat u}{dt}\right) = a^2\left(\hat u\times\frac{d\hat u}{dt}\right)$$
If this is $\vec 0$ (and $a\ne0$) then $\hat u\times\dfrac{d\hat u}{dt} = \vec 0$. Also $\hat u\cdot\hat u = 1$ gives, on differentiating, $\hat u\cdot\dfrac{d\hat u}{dt} = 0$, so $\dfrac{d\hat u}{dt}\perp\hat u$. For perpendicular vectors $\left|\hat u\times\dfrac{d\hat u}{dt}\right| = \left|\dfrac{d\hat u}{dt}\right|$, which must be $0$. Hence $\dfrac{d\hat u}{dt} = \vec 0$, i.e. $\hat u$ is constant and $\vec a$ has constant direction. $\blacksquare$

@s 14
$\phi = x^2 - y^2 + z^2$, so $\nabla\phi = (2x,\ -2y,\ 2z)$. At $A(1,-3,2)$: $\nabla\phi = (2,\ 6,\ 4)$.

$\overrightarrow{AB} = (4-1,\ 5+3,\ 7-2) = (3,8,5)$, $|\overrightarrow{AB}| = \sqrt{9+64+25} = \sqrt{98} = 7\sqrt2$.

$$D_{\hat u}\phi = \nabla\phi\cdot\hat u = \frac{2(3) + 6(8) + 4(5)}{7\sqrt2} = \frac{74}{7\sqrt2}$$
$$\boxed{D = \frac{37\sqrt2}7\approx7.475}$$

@s 15
Apart from the first term, the series is $\displaystyle\sum_{n=1}^\infty u_n$ with $u_n = \dfrac{n^n}{(n+1)^{n+1}}$ ($u_1 = \tfrac14,\ u_2 = \tfrac4{27},\dots$). Dropping the finite first term does not affect convergence.

Ratio test: $\dfrac{u_{n+1}}{u_n}\to1$ (inconclusive), so use comparison.

$$u_n = \frac1{n+1}\left(\frac n{n+1}\right)^n = \frac1{n+1}\left(1 + \frac1n\right)^{-n}$$
Compare with $v_n = \dfrac1n$:
$$\lim_{n\to\infty}\frac{u_n}{v_n} = \lim\frac n{n+1}\left(1+\frac1n\right)^{-n} = 1\cdot\frac1e = \frac1e\ne0,\ \text{finite}$$
By the limit comparison test $\sum u_n$ and $\sum\dfrac1n$ behave alike. $\sum\dfrac1n$ is the harmonic series, divergent.
$$\boxed{\text{The series is divergent}}$$

@s 16
$\displaystyle\sum\frac{(-1)^n(2x+1)^n}{3^n} = \sum\left(-\frac{2x+1}3\right)^n$ is a geometric series with ratio $r = -\dfrac{2x+1}3$ (or by the ratio test $\left|\dfrac{u_{n+1}}{u_n}\right| = \dfrac{|2x+1|}3$).

It converges when $\left|\dfrac{2x+1}3\right|<1$, i.e. $|2x+1|<3$, $-3<2x+1<3$, so $-2<x<1$. In the form $|x - (-\tfrac12)|<\tfrac32$ the **radius of convergence is $R = \dfrac32$**, centred at $x = -\tfrac12$.

*Endpoints.*

- $x = 1$: $2x+1 = 3$ and the terms are $(-1)^n$, which do not tend to $0$: **divergent**.
- $x = -2$: $2x+1 = -3$ and the terms are $(-1)^n(-1)^n = 1$, which do not tend to $0$: **divergent**.

$$\boxed{R = \frac32,\qquad\text{interval of convergence }(-2,\ 1)}$$

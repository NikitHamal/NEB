---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-SH451-2080-Chaitra.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: SH 451
year_bs: 2080 Chaitra
cal: BS
year_ad: 2024
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (old course, SH 451). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
State Euler's theorem on homogeneous functions of two variables and use it to show $x\dfrac{\partial u}{\partial x} + y\dfrac{\partial u}{\partial y} = \sin2u$, where $u = \tan^{-1}\dfrac{x^3+y^3}{x-y}$. [[1+4]]

@q 2
Find the maximum value of $f(x,y,z) = xyz$ subject to the condition $x + y + z = 9$. [[5]]

@q 3
Sketch the region of integration for the integral $\displaystyle\int_0^2\int_{x^2}^{2x}(4x+2)\,dy\,dx$ and evaluate it by changing the order of integration. [[1+4]]

@q 4
Evaluate the integral $\displaystyle\iiint_Vx\,dx\,dy\,dz$, where $V$ is the region in the first octant bounded by the surface $x^{2/3} + y^{2/3} + z^{2/3} = 1$. [[5]]

@q 5
Find the distance of the point $(1,-2,3)$ from the plane $x - y + z = 5$ measured parallel to the line $\dfrac x2 = \dfrac y3 = \dfrac z{-6}$. [[5]]

@q 6
Show that the lines $\dfrac{x-1}{2} = \dfrac{y-2}{3} = \dfrac{z-3}{4}$ and $\dfrac{x-2}{3} = \dfrac{y-3}{4} = \dfrac{z-4}{5}$ are coplanar. Find the equation of the plane in which they lie. [[3+2]]

@q 7
Find the centre and radius of the circle $x^2 + y^2 + z^2 + x + y + z = 4$, $x + y + z = 0$. [[5]]

@q 8
Find the equation of the cylinder whose generators are parallel to the line $\dfrac x1 = \dfrac y{-2} = \dfrac z3$ and whose guiding curve is $x^2 + 2y^2 = 1$, $z = 3$. [[5]]

@q 9
Prove that the vectors $\vec b\times\vec c$, $\vec c\times\vec a$, $\vec a\times\vec b$ are coplanar if the vectors $\vec a,\vec b,\vec c$ are coplanar. [[5]]

@q 10
Prove that the necessary and sufficient condition for the vector function of a scalar variable $t$ to have a constant direction is $\vec a\times\dfrac{d\vec a}{dt} = \vec 0$. [[5]]

@q 11
If $f = x^3 + y^3 + z^3 - 3xyz$, find $\operatorname{div}(\operatorname{grad}f)$ and $\operatorname{curl}(\operatorname{grad}f)$. [[5]]

@q 12
Find the solution of the differential equation $y'' + 16y = 0$ using the power series method. [[5]]

@q 13
Express the function $f(x) = x^3 - 5x^2 + 6x + 1$ in terms of Legendre's polynomials. [[5]]

@q 14
Show that $J_{5/2}(x) = \sqrt{\dfrac{2}{\pi x}}\left\{\dfrac{3-x^2}{x^2}\sin x - \dfrac3x\cos x\right\}$, where the symbols have their usual meanings. [[5]]

@q 15
Test the convergence or divergence of the series $2x + \dfrac{9x^2}{8} + \dfrac{64x^3}{81} + \cdots + \dfrac{(n+1)^n}{n^{n+1}}x^n + \cdots$, where $x>0$. [[5]]

@q 16
Find the radius and interval of convergence of the series $\displaystyle\sum_{n=1}^\infty\dfrac{(x-1)^n}{\sqrt n}$. [[5]]
<!-- SOLUTIONS -->

@s 1
**Euler's theorem.** If $f(x,y)$ is homogeneous of degree $n$ and has continuous first-order partial derivatives, then $x f_x + y f_y = n f$.

Let $z = \tan u = \dfrac{x^3+y^3}{x-y}$. Since $\dfrac{(tx)^3 + (ty)^3}{tx - ty} = t^2z$, $z$ is homogeneous of degree $2$, so
$$xz_x + yz_y = 2z$$
With $z_x = \sec^2u\,u_x$ and $z_y = \sec^2u\,u_y$,
$$\begin{gathered}\sec^2u\left(xu_x + yu_y\right) = 2\tan u\;\Longrightarrow\;x\frac{\partial u}{\partial x} + y\frac{\partial u}{\partial y} = 2\sin u\cos u = \boxed{\sin2u} \\ \blacksquare\end{gathered}$$

@s 2
Maximise $f = xyz$ subject to $\varphi = x + y + z - 9 = 0$. Lagrange: $F = xyz + \lambda(x+y+z-9)$:
$$F_x = yz + \lambda = 0,\quad F_y = xz + \lambda = 0,\quad F_z = xy + \lambda = 0\;\Longrightarrow\;yz = xz = xy$$
For a maximum with positive $x, y, z$ this gives $x = y = z$, and the constraint gives $x = y = z = 3$ (with $\lambda = -9$). Then $f = 27$.

*It is a maximum:* by AM–GM, $\sqrt[3]{xyz}\le\dfrac{x+y+z}{3} = 3$ for positive $x,y,z$, so $xyz\le27$, with equality at $x = y = z = 3$.
$$\boxed{f_{\max} = 27\ \text{ at }(3,3,3)}$$

@s 3
**Region.** $0\le x\le2$ and, for each $x$, $x^2\le y\le2x$: the region between the parabola $y = x^2$ and the line $y = 2x$, which meet at $(0,0)$ and $(2,4)$.

```figure caption="Question 3: region between the parabola y = x² and the line y = 2x for 0 ≤ x ≤ 2; the vertical strip x² ≤ y ≤ 2x is replaced by the horizontal strip y/2 ≤ x ≤ √y."
x=np.linspace(0,2,200)
fig,ax=plt.subplots(figsize=(4.2,3.4))
ax.fill_between(x,x**2,2*x,color='#1d6fb8',alpha=0.15)
ax.plot(x,x**2,color='#1d6fb8'); ax.plot(x,2*x,color='#d9534f')
ax.plot([0.55,np.sqrt(1.1)],[1.1,1.1],color='#2e8b57',lw=1.6)
ax.plot([0.55,0.55],[0.3025,1.1],color='#b8860b',lw=1.0,ls='--')
ax.text(1.2,0.55,'$y=x^2$',color='#1d6fb8',fontsize=8); ax.text(0.2,0.9,'$y=2x$',color='#d9534f',fontsize=8,rotation=48)
ax.text(1.12,1.15,'$x=y/2\\to x=\\sqrt{y}$',color='#2e8b57',fontsize=7.5)
ax.plot([2],[4],'o',color='#14181f',ms=3.5); ax.text(1.7,4.1,'(2, 4)',fontsize=8)
ax.set_xlim(-0.1,2.4); ax.set_ylim(-0.2,4.5)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

**As given.**
$$I = \int_0^2(4x+2)\big[y\big]_{x^2}^{2x}dx = \int_0^2(4x+2)(2x-x^2)\,dx = \int_0^2\left(6x^2 - 4x^3 + 4x\right)dx = \Big[2x^3 - x^4 + 2x^2\Big]_0^2 = 16 - 16 + 8 = 8$$
**Order reversed.** For a fixed $y\in[0,4]$, $x$ runs from the line ($x = y/2$) to the parabola ($x = \sqrt y$):
$$I = \int_0^4\int_{y/2}^{\sqrt y}(4x+2)\,dx\,dy = \int_0^4\Big[2x^2 + 2x\Big]_{y/2}^{\sqrt y}dy = \int_0^4\left(2y + 2\sqrt y - \frac{y^2}2 - y\right)dy$$
$$= \int_0^4\left(y + 2\sqrt y - \frac{y^2}{2}\right)dy = \Big[\frac{y^2}2 + \frac43y^{3/2} - \frac{y^3}{6}\Big]_0^4 = 8 + \frac{32}{3} - \frac{32}{3} = \boxed{8}$$

@s 4
Put $X = x^{2/3}$, $Y = y^{2/3}$, $Z = z^{2/3}$, i.e. $x = X^{3/2}$, $dx = \tfrac32X^{1/2}dX$ (and similarly for $y, z$). The region becomes the simplex $X + Y + Z\le1$:
$$I = \iiint X^{3/2}\cdot\left(\tfrac32\right)^3X^{1/2}Y^{1/2}Z^{1/2}\,dX\,dY\,dZ = \frac{27}{8}\iiint X^{2}\,Y^{1/2}Z^{1/2}\,dX\,dY\,dZ$$
By **Dirichlet's integral** $\displaystyle\iiint_{X+Y+Z\le1}X^{l-1}Y^{m-1}Z^{n-1}\,dX\,dY\,dZ = \frac{\Gamma(l)\Gamma(m)\Gamma(n)}{\Gamma(l+m+n+1)}$ with $l = 3$, $m = n = \tfrac32$:
$$I = \frac{27}{8}\cdot\frac{\Gamma(3)\Gamma(\tfrac32)\Gamma(\tfrac32)}{\Gamma(7)} = \frac{27}{8}\cdot\frac{2\cdot\frac\pi4}{720} = \frac{27}{8}\cdot\frac{\pi}{1440}$$
$$\boxed{I = \frac{27\pi}{11520} = \frac{3\pi}{1280}}\approx0.00736$$
(Verified numerically by Monte-Carlo integration: $0.00734$.)

@s 5
The line through the point $P(1,-2,3)$ parallel to $\dfrac x2 = \dfrac y3 = \dfrac z{-6}$ is $(1+2t,\ -2+3t,\ 3-6t)$. It meets the plane $x - y + z = 5$ where
$$(1+2t) - (-2+3t) + (3-6t) = 5\;\Longrightarrow\;6 - 7t = 5\;\Longrightarrow\;t = \frac17$$
The distance from $P$ along the line is $|t|\cdot|(2,3,-6)| = \dfrac17\sqrt{4+9+36} = \dfrac{7}{7}$:
$$\boxed{d = 1\ \text{unit}}$$
(The foot of the line is $\left(\tfrac97,-\tfrac{11}7,\tfrac{15}{7}\right)$, and it satisfies $\tfrac97 + \tfrac{11}7 + \tfrac{15}7 = \tfrac{35}7 = 5$.)

@s 6
Line 1 passes through $A(1,2,3)$ with $\mathbf d_1 = (2,3,4)$; line 2 passes through $B(2,3,4)$ with $\mathbf d_2 = (3,4,5)$; $\overrightarrow{AB} = (1,1,1)$.
$$\begin{vmatrix}1&1&1\\2&3&4\\3&4&5\end{vmatrix} = 1(15-16) - 1(10-12) + 1(8-9) = -1 + 2 - 1 = 0$$
so the lines are coplanar. $\blacksquare$

The normal to the plane is $\mathbf d_1\times\mathbf d_2 = (15-16,\ 12-10,\ 8-9) = (-1,2,-1)$. The plane through $A(1,2,3)$:
$$-(x-1) + 2(y-2) - (z-3) = 0\;\Longrightarrow\;\boxed{x - 2y + z = 0}$$
(Check with $B$: $2 - 6 + 4 = 0$ ✓.)

@s 7
The sphere $x^2+y^2+z^2 + x + y + z - 4 = 0$ has centre $C\left(-\tfrac12,-\tfrac12,-\tfrac12\right)$ and radius $R = \sqrt{\tfrac34 + 4} = \dfrac{\sqrt{19}}{2}$. The distance of $C$ from the plane $x+y+z = 0$ is
$$p = \frac{|-\tfrac32|}{\sqrt3} = \frac{\sqrt3}{2}$$
The centre of the circle is the foot of the perpendicular from $C$ to the plane: $C + t(1,1,1)$ with sum zero, $-\tfrac32 + 3t = 0$, $t = \tfrac12$, i.e. $(0,0,0)$. The radius is
$$r = \sqrt{R^2 - p^2} = \sqrt{\frac{19}{4} - \frac34} = 2$$
$$\boxed{\text{centre }(0,0,0),\quad\text{radius }2}$$
(Directly: on the plane, $x + y + z = 0$ so the sphere reduces to $x^2 + y^2 + z^2 = 4$.)

@s 8
The guiding curve is $x^2 + 2y^2 = 1$, $z = 3$. Let $P(x,y,z)$ be on the cylinder; the generator through it has direction $(1,-2,3)$ and meets the plane $z = 3$ at
$$Q = (x - t,\ y + 2t,\ z - 3t)\quad\text{with}\quad z - 3t = 3\;\Rightarrow\;t = \frac{z-3}{3}$$
$$\begin{gathered}x_1 = x - \frac{z-3}{3} = \frac{3x - z + 3}{3} \\ y_1 = y + \frac{2(z-3)}{3} = \frac{3y + 2z - 6}{3}\end{gathered}$$
Since $Q$ lies on $x^2 + 2y^2 = 1$:
$$\left(\frac{3x - z + 3}{3}\right)^2 + 2\left(\frac{3y + 2z - 6}{3}\right)^2 = 1$$
$$\boxed{(3x - z + 3)^2 + 2(3y + 2z - 6)^2 = 9}$$

@s 9
Let $\vec a,\vec b,\vec c$ be coplanar, so $[\vec a\,\vec b\,\vec c] = \vec a\cdot(\vec b\times\vec c) = 0$. Three vectors are coplanar iff their scalar triple product is zero, so we compute
$$\big[\vec b\times\vec c,\ \vec c\times\vec a,\ \vec a\times\vec b\big] = (\vec b\times\vec c)\cdot\big[(\vec c\times\vec a)\times(\vec a\times\vec b)\big]$$
Using $\vec X\times(\vec a\times\vec b) = \vec a(\vec X\cdot\vec b) - \vec b(\vec X\cdot\vec a)$ with $\vec X = \vec c\times\vec a$: $\vec X\cdot\vec a = 0$ and $\vec X\cdot\vec b = [\vec c\,\vec a\,\vec b] = [\vec a\,\vec b\,\vec c]$, so $(\vec c\times\vec a)\times(\vec a\times\vec b) = [\vec a\,\vec b\,\vec c]\,\vec a$. Then
$$\big[\vec b\times\vec c,\ \vec c\times\vec a,\ \vec a\times\vec b\big] = [\vec a\,\vec b\,\vec c]\;(\vec b\times\vec c)\cdot\vec a = [\vec a\,\vec b\,\vec c]^2 = 0$$
Hence $\vec b\times\vec c$, $\vec c\times\vec a$, $\vec a\times\vec b$ are coplanar. $\blacksquare$ (Geometrically: when $\vec a,\vec b,\vec c$ lie in one plane, each of the three cross products is normal to that plane, so the three vectors are parallel to one another and hence coplanar.)

@s 10
**Necessary.** If $\vec a$ has constant direction, $\vec a = \varphi(t)\hat e$ with $\hat e$ a constant unit vector. Then $\dfrac{d\vec a}{dt} = \varphi'\hat e$ and $\vec a\times\dfrac{d\vec a}{dt} = \varphi\varphi'(\hat e\times\hat e) = \vec0$.

**Sufficient.** Let $\vec a = a\hat e$ with $a = |\vec a|$ and $\hat e$ the unit vector along $\vec a$. Then
$$\vec a\times\frac{d\vec a}{dt} = a\hat e\times\left(a'\hat e + a\frac{d\hat e}{dt}\right) = a^2\,\hat e\times\frac{d\hat e}{dt}$$
From $\hat e\cdot\hat e = 1$, $\hat e\cdot\dfrac{d\hat e}{dt} = 0$, so $\dfrac{d\hat e}{dt}\perp\hat e$ and $\left|\hat e\times\dfrac{d\hat e}{dt}\right| = \left|\dfrac{d\hat e}{dt}\right|$. If $\vec a\times\dfrac{d\vec a}{dt} = \vec0$ (and $a\ne0$), then $\left|\dfrac{d\hat e}{dt}\right| = 0$, so $\hat e$ is constant: the direction of $\vec a$ is constant. $\blacksquare$

@s 11
$$\operatorname{grad}f = \nabla f = \big(3x^2 - 3yz,\ 3y^2 - 3zx,\ 3z^2 - 3xy\big)$$
$$\operatorname{div}(\operatorname{grad}f) = \frac{\partial}{\partial x}(3x^2 - 3yz) + \frac{\partial}{\partial y}(3y^2 - 3zx) + \frac{\partial}{\partial z}(3z^2 - 3xy) = 6x + 6y + 6z$$
$$\boxed{\operatorname{div}(\operatorname{grad}f) = \nabla^2f = 6(x+y+z)}$$
$$\operatorname{curl}(\operatorname{grad}f) = \begin{vmatrix}\vec i&\vec j&\vec k\\ \partial_x&\partial_y&\partial_z\\ 3x^2-3yz&3y^2-3zx&3z^2-3xy\end{vmatrix} = (-3x+3x)\vec i + (-3y+3y)\vec j + (-3z+3z)\vec k$$
$$\boxed{\operatorname{curl}(\operatorname{grad}f) = \vec 0}$$
(as it must be for any scalar function with continuous second derivatives).

@s 12
Let $y = \sum_{n\ge0}a_nx^n$, $y'' = \sum_{n\ge0}(n+2)(n+1)a_{n+2}x^n$. Substituting into $y'' + 16y = 0$ and equating the coefficient of $x^n$:
$$(n+2)(n+1)a_{n+2} + 16a_n = 0\;\Longrightarrow\;a_{n+2} = -\frac{16\,a_n}{(n+2)(n+1)}$$
Even coefficients: $a_2 = -\dfrac{16}{2!}a_0$, $a_4 = \dfrac{16^2}{4!}a_0$, $\ldots$ so $a_{2k} = \dfrac{(-1)^k4^{2k}}{(2k)!}a_0$. Odd coefficients: $a_3 = -\dfrac{16}{3!}a_1$, $a_5 = \dfrac{16^2}{5!}a_1$, $\ldots$ so $a_{2k+1} = \dfrac{(-1)^k4^{2k}}{(2k+1)!}a_1$.
$$y = a_0\left[1 - \frac{(4x)^2}{2!} + \frac{(4x)^4}{4!} - \cdots\right] + \frac{a_1}{4}\left[4x - \frac{(4x)^3}{3!} + \frac{(4x)^5}{5!} - \cdots\right]$$
$$\boxed{y = a_0\cos4x + \frac{a_1}4\sin4x = A\cos4x + B\sin4x}$$

@s 13
Legendre polynomials: $P_0 = 1$, $P_1 = x$, $P_2 = \dfrac{3x^2-1}{2}$, $P_3 = \dfrac{5x^3-3x}2$. Inverting:
$$\begin{gathered}x = P_1 \\ x^2 = \frac{2P_2 + P_0}{3} \\ x^3 = \frac{2P_3 + 3P_1}{5}\end{gathered}$$
$$f(x) = x^3 - 5x^2 + 6x + 1 = \frac{2P_3 + 3P_1}{5} - \frac{5(2P_2 + P_0)}{3} + 6P_1 + P_0$$
$$\boxed{f(x) = \frac25P_3(x) - \frac{10}{3}P_2(x) + \frac{33}{5}P_1(x) - \frac23P_0(x)}$$
(Check at $x = 1$: $\tfrac25 - \tfrac{10}3 + \tfrac{33}5 - \tfrac23 = 3 = f(1)$ ✓.)

@s 14
From the series, $J_{1/2}(x) = \sqrt{\dfrac2{\pi x}}\sin x$ and $J_{-1/2}(x) = \sqrt{\dfrac2{\pi x}}\cos x$ (using $r!\,\Gamma(r+\tfrac32) = \dfrac{(2r+1)!\sqrt\pi}{2^{2r+1}}$). The recurrence relation is
$$J_{\nu+1}(x) = \frac{2\nu}{x}J_\nu(x) - J_{\nu-1}(x)$$
With $\nu = \tfrac12$: $J_{3/2} = \dfrac1xJ_{1/2} - J_{-1/2} = \sqrt{\dfrac{2}{\pi x}}\left(\dfrac{\sin x}{x} - \cos x\right)$. With $\nu = \tfrac32$:
$$\begin{gathered}J_{5/2}(x) = \frac3xJ_{3/2}(x) - J_{1/2}(x) = \sqrt{\frac2{\pi x}}\left[\frac3x\left(\frac{\sin x}{x} - \cos x\right) - \sin x\right] = \sqrt{\frac{2}{\pi x}}\left[\frac{3 - x^2}{x^2}\sin x - \frac3x\cos x\right] \\ \blacksquare\end{gathered}$$

@s 15
The $n$th term is $u_n = \dfrac{(n+1)^n}{n^{n+1}}x^n = \dfrac1n\left(1 + \dfrac1n\right)^nx^n$ (check: $u_1 = 2x$, $u_2 = \dfrac{9x^2}{8}$, $u_3 = \dfrac{64x^3}{81}$ ✓).

**Ratio test.**
$$\frac{u_{n+1}}{u_n} = x\cdot\frac{n}{n+1}\cdot\frac{\left(1+\frac1{n+1}\right)^{n+1}}{\left(1+\frac1n\right)^n}\;\longrightarrow\;x\cdot1\cdot\frac ee = x$$
So the series converges for $x<1$ and diverges for $x>1$.

**Case $x = 1$** (the test fails). $u_n = \dfrac1n\left(1+\dfrac1n\right)^n$ and $\dfrac{u_n}{1/n} = \left(1+\dfrac1n\right)^n\to e\ne0$. Since $\sum\dfrac1n$ diverges, the series diverges by limit comparison.
$$\boxed{\text{Convergent for }0<x<1;\ \text{divergent for }x\ge1}$$

@s 16
Ratio test: $\left|\dfrac{u_{n+1}}{u_n}\right| = |x-1|\sqrt{\dfrac n{n+1}}\to|x-1|$. The series converges absolutely for $|x-1|<1$, so the **radius of convergence is $R = 1$**, i.e. $0<x<2$.

*Endpoints.*
- $x = 2$: $\displaystyle\sum\frac1{\sqrt n} = \sum\frac{1}{n^{1/2}}$, a $p$-series with $p = \tfrac12\le1$: **divergent**.
- $x = 0$: $\displaystyle\sum\frac{(-1)^n}{\sqrt n}$ is alternating with $\dfrac1{\sqrt n}\downarrow0$: **convergent** (conditionally), by Leibnitz's test.
$$\boxed{R = 1,\qquad\text{interval of convergence }[0,\,2)}$$

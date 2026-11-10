---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-II-SH451-2081-Chaitra.pdf
subject: Engineering Mathematics II
level: BE · Year I / Part II
code: SH 451
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 451). All questions carry equal marks. Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
State Euler's theorem for homogeneous functions and use it to show that $x\dfrac{\partial z}{\partial x} + y\dfrac{\partial z}{\partial y} = \sin 2z$ for $\tan z = \dfrac{x^3+y^3}{x+y}$.

@q 2
Find the minimum value of the function $x^2 + y^2 + z^2$ under the condition $x + y + z = 3a$.

@q 3
Evaluate $\displaystyle\iint_R xy\,dx\,dy$, where $R$ is the region over the area of the ellipse $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1$ in the first octant (quadrant).

@q 4
Evaluate $\displaystyle\int_0^a\int_y^a\dfrac{x}{x^2+y^2}\,dx\,dy$ by changing the order of integration.

@q 5
Show that the lines $\dfrac{x-5}{4} = \dfrac{y-7}{4} = \dfrac{z+3}{-5}$ and $\dfrac{x-8}{7} = \dfrac{y-4}{1} = \dfrac{z-5}{3}$ are coplanar. Find their point of intersection and the equation of the plane in which they lie.

@q 6
Find the shortest distance between the lines $x + a = 2y = -12z$ and $x = y + 2a = 6z - 6a$.

@q 7
Find the equation of the sphere having the circle $x^2 + y^2 + z^2 + 7y - 2z + 2 = 0$, $2x + 3y + 4z - 8 = 0$ as a great circle.

@q 8
Find the equation of the right circular cylinder whose guiding curve is the circle $x^2 + y^2 + z^2 - x - y - z = 0$, $x + y + z - 1 = 0$.

@q 9
Solve the differential equation $y'' - y = 0$ by the power series method.

@q 10
Express $f(x) = 5x^3 + 3x$ in terms of Legendre's polynomials.
@or
Solve in series Legendre's equation $(1-x^2)y'' - 2xy' + n(n+1)y = 0$.

@q 11
Prove Bessel's function $J_{3/2}(x) = \sqrt{\dfrac{2}{\pi x}}\left(\dfrac{\sin x}{x} - \cos x\right)$.

@q 12
Find the set of reciprocal system to the set of vectors $2\vec i + 3\vec j - \vec k$, $-\vec i + 2\vec j - 3\vec k$, $3\vec i - 4\vec j + 2\vec k$.

@q 13
Prove that the necessary and sufficient condition for the vector function $\vec a(t)$ of the scalar variable $t$ to have constant direction is $\vec a\times\dfrac{d\vec a}{dt} = \vec 0$.

@q 14
Find the directional derivative of $\varphi(x,y,z) = xy^2 + yz^3$ at the point $(2,-1,1)$ in the direction of the vector $\vec i + 2\vec j + 2\vec k$.

@q 15
Determine whether the series given by $\displaystyle\sum_{n=1}^\infty\left(\sqrt{n^4+1} - n^2\right)$ is convergent or divergent.

@q 16
Determine the interval of convergence of the series $\displaystyle\sum_{n=1}^\infty\dfrac{2^n(x-3)^n}{n+3}$.
<!-- SOLUTIONS -->

@s 1
**Euler's theorem.** If $f(x,y)$ is homogeneous of degree $n$ (that is, $f(tx,ty) = t^nf(x,y)$) and has continuous first partial derivatives, then
$$x\frac{\partial f}{\partial x} + y\frac{\partial f}{\partial y} = n\,f$$
Let $u = \tan z = \dfrac{x^3+y^3}{x+y}$. Replacing $x, y$ by $tx, ty$ gives $\dfrac{t^3(x^3+y^3)}{t(x+y)} = t^2u$, so $u$ is homogeneous of degree $2$ and
$$x\,u_x + y\,u_y = 2u$$
But $u_x = \sec^2z\,z_x$ and $u_y = \sec^2z\,z_y$, so
$$\sec^2z\left(x z_x + y z_y\right) = 2\tan z\;\Longrightarrow\;x\frac{\partial z}{\partial x} + y\frac{\partial z}{\partial y} = 2\sin z\cos z = \boxed{\sin2z}$$
(The printed relation $z_x + z_y = \sin2z$ is the standard Euler form with the multipliers $x$ and $y$ lost in print.)

@s 2
Minimise $f = x^2 + y^2 + z^2$ subject to $\varphi = x + y + z - 3a = 0$. Lagrange's function $F = x^2 + y^2 + z^2 + \lambda(x + y + z - 3a)$:
$$F_x = 2x + \lambda = 0,\quad F_y = 2y + \lambda = 0,\quad F_z = 2z + \lambda = 0\;\Longrightarrow\;x = y = z = -\frac\lambda2$$
The constraint gives $3x = 3a$, so $x = y = z = a$ (and $\lambda = -2a$). The stationary value is $f = 3a^2$. It is a minimum: the second variation is $d^2F = 2(dx^2 + dy^2 + dz^2)>0$ (also, by the Cauchy–Schwarz inequality, $(x+y+z)^2\le3(x^2+y^2+z^2)$ gives $x^2 + y^2 + z^2\ge3a^2$).
$$\boxed{f_{\min} = 3a^2\ \text{ at }(a,a,a)}$$

@s 3
The region is the quarter of the ellipse in the first quadrant: $0\le x\le a$, $0\le y\le\dfrac ba\sqrt{a^2-x^2}$.
$$\iint_Rxy\,dx\,dy = \int_0^ax\left[\frac{y^2}2\right]_0^{\frac ba\sqrt{a^2-x^2}}dx = \int_0^a\frac{x}{2}\cdot\frac{b^2}{a^2}(a^2-x^2)\,dx = \frac{b^2}{2a^2}\left[\frac{a^2x^2}{2} - \frac{x^4}{4}\right]_0^a = \frac{b^2}{2a^2}\cdot\frac{a^4}{4}$$
$$\boxed{\iint_Rxy\,dx\,dy = \frac{a^2b^2}{8}}$$

@s 4
The region of integration is $0\le y\le a$, $y\le x\le a$, i.e. the triangle bounded by $y = 0$, $x = a$ and the line $y = x$. Taking horizontal strips first is awkward; reversing the order, $x$ runs from $0$ to $a$ and for each $x$, $y$ runs from $0$ to $x$:
$$I = \int_0^a\int_0^x\frac{x}{x^2+y^2}\,dy\,dx = \int_0^ax\left[\frac1x\tan^{-1}\frac yx\right]_0^x dx = \int_0^a\tan^{-1}(1)\,dx = \int_0^a\frac\pi4\,dx$$
$$\boxed{I = \frac{\pi a}{4}}$$

```figure caption="Question 4: the triangle 0 ≤ y ≤ x ≤ a. Original order: horizontal strips y ≤ x ≤ a; reversed order: vertical strips 0 ≤ y ≤ x."
a=1.0
fig,ax=plt.subplots(figsize=(3.6,3.2))
ax.fill([0,a,a],[0,0,a],color='#1d6fb8',alpha=0.15)
ax.plot([0,a],[0,a],color='#1d6fb8'); ax.plot([a,a],[0,a],color='#1d6fb8'); ax.plot([0,a],[0,0],color='#1d6fb8')
ax.annotate('',xy=(0.85,0.0),xytext=(0.85,0.85),arrowprops=dict(arrowstyle='<->',color='#d9534f'))
ax.text(0.5,0.18,'new strip:\n$0\\leq y\\leq x$',color='#d9534f',fontsize=8,ha='center')
ax.text(0.2,0.6,'$y=x$',fontsize=8,rotation=45); ax.text(a+0.03,0.5,'$x=a$',fontsize=8)
ax.set_aspect('equal'); ax.set_xlim(-0.1,1.3); ax.set_ylim(-0.1,1.15)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 5
Line 1: through $A(5,7,-3)$ with direction $\mathbf d_1 = (4,4,-5)$. Line 2: through $B(8,4,5)$ with direction $\mathbf d_2 = (7,1,3)$. Then $\overrightarrow{AB} = (3,-3,8)$. The lines are coplanar iff $[\overrightarrow{AB},\mathbf d_1,\mathbf d_2] = 0$:
$$\begin{vmatrix}3&-3&8\\4&4&-5\\7&1&3\end{vmatrix} = 3(12+5) + 3(12+35) + 8(4-28) = 51 + 141 - 192 = 0\qquad\blacksquare$$
*Reading note.* The scan prints the first line's third ratio as $\dfrac{z-3}{-5}$; this is the standard problem with $\dfrac{z+3}{-5}$. With $z-3$ the determinant is $144\ne0$ and the lines would be skew, so $z+3$ is used.

**Point of intersection.** Put $x = 5+4s$, $y = 7+4s$, $z = -3-5s$ and $x = 8+7t$, $y = 4+t$, $z = 5+3t$. From $x$ and $y$: $4s - 7t = 3$ and $4s - t = -3$; subtracting, $-6t = 6$, so $t = -1$ and $s = -1$. Check with $z$: $-3 + 5 = 2$ and $5 - 3 = 2$ ✓. The point is
$$\boxed{(1, 3, 2)}$$
**Plane.** Its normal is $\mathbf d_1\times\mathbf d_2 = (4,4,-5)\times(7,1,3) = (12+5,\ -35-12,\ 4-28) = (17,-47,-24)$. Through $(1,3,2)$:
$$17(x-1) - 47(y-3) - 24(z-2) = 0\;\Longrightarrow\;\boxed{17x - 47y - 24z + 172 = 0}$$
(Check: $A$: $85 - 329 + 72 + 172 = 0$ ✓; $B$: $136 - 188 - 120 + 172 = 0$ ✓.)

@s 6
Line 1: $x + a = 2y = -12z = k$ gives $x = k - a$, $y = \dfrac k2$, $z = -\dfrac{k}{12}$: it passes through $P(-a,0,0)$ with direction $(1,\tfrac12,-\tfrac1{12})\propto\mathbf d_1 = (12,6,-1)$.

Line 2: $x = y + 2a = 6z - 6a = k$ gives $x = k$, $y = k - 2a$, $z = \dfrac{k+6a}{6}$: it passes through $Q(0,-2a,a)$ with direction $(1,1,\tfrac16)\propto\mathbf d_2 = (6,6,1)$.
$$\begin{gathered}\mathbf d_1\times\mathbf d_2 = (12,6,-1)\times(6,6,1) = (6+6,\ -6-12,\ 72-36) = (12,-18,36) = 6\,(2,-3,6) \\ |(2,-3,6)| = 7\end{gathered}$$
$\overrightarrow{PQ} = (a,-2a,a)$. The shortest distance is the projection of $\overrightarrow{PQ}$ on the common perpendicular:
$$d = \frac{|(a,-2a,a)\cdot(2,-3,6)|}{7} = \frac{|2a + 6a + 6a|}{7} = \frac{14a}{7} = \boxed{2a}$$

@s 7
For the sphere to have the given circle as a great circle, its centre must lie in the plane of the circle. The spheres through the circle are
$$x^2 + y^2 + z^2 + 7y - 2z + 2 + \lambda(2x + 3y + 4z - 8) = 0$$
with centre $\left(-\lambda,\ -\dfrac{7+3\lambda}{2},\ 1 - 2\lambda\right)$. Putting the centre into $2x + 3y + 4z = 8$:
$$-2\lambda - \frac{3(7+3\lambda)}{2} + 4 - 8\lambda = 8\;\Longrightarrow\;-14.5\lambda - 14.5 = 0\;\Longrightarrow\;\lambda = -1$$
Hence
$$x^2 + y^2 + z^2 + 7y - 2z + 2 - 2x - 3y - 4z + 8 = 0\;\Longrightarrow\;\boxed{x^2 + y^2 + z^2 - 2x + 4y - 6z + 10 = 0}$$
This sphere has centre $(1,-2,3)$ and radius $\sqrt{1+4+9-10} = 2$ (the centre satisfies $2 - 6 + 12 = 8$ ✓).

@s 8
The axis of a right circular cylinder through a given circle is perpendicular to its plane; the plane $x+y+z = 1$ has normal $(1,1,1)$, so the generators are parallel to $(1,1,1)$.

Let $P(x,y,z)$ lie on the cylinder, and let the generator through $P$ meet the plane at $Q = (x-t, y-t, z-t)$. Since $Q$ is in the plane, $x+y+z-3t = 1$, i.e. $t = \dfrac{s-1}{3}$ with $s = x+y+z$. $Q$ must also lie on the sphere $x^2+y^2+z^2-x-y-z = 0$:
$$\sum(x-t)^2 - \sum(x-t) = \sum x^2 - 2ts + 3t^2 - s + 3t = 0$$
With $3t = s-1$: $-2ts + 3t^2 = \dfrac{(s-1)(-2s + s - 1)}{3} = -\dfrac{s^2-1}{3}$ and $-s + 3t = -1$. So
$$x^2+y^2+z^2 - \frac{s^2-1}{3} - 1 = 0\;\Longrightarrow\;3\sum x^2 - s^2 - 2 = 0$$
Since $s^2 = \sum x^2 + 2\sum xy$:
$$\boxed{x^2 + y^2 + z^2 - xy - yz - zx = 1}$$
(Check: the sphere has centre $(\tfrac12,\tfrac12,\tfrac12)$ and radius$^2 = \tfrac34$, the plane is at distance $\tfrac{1}{2\sqrt3}$ from it, so the circle has radius$^2 = \tfrac34 - \tfrac1{12} = \tfrac23$. The axis is the line $x = y = z$, and the squared distance of $(x,y,z)$ from it is $x^2+y^2+z^2 - \tfrac{(x+y+z)^2}{3} = \tfrac23\left(\sum x^2 - \sum xy\right)$, which equals $\tfrac23$ exactly when the equation above holds.)

@s 9
Put $y = \sum_{n=0}^\infty a_nx^n$, so $y'' = \sum_{n=0}^\infty(n+2)(n+1)a_{n+2}x^n$. Then $y'' - y = 0$ gives, for every $n\ge0$,
$$(n+2)(n+1)a_{n+2} - a_n = 0\;\Longrightarrow\;a_{n+2} = \frac{a_n}{(n+2)(n+1)}$$
$a_0, a_1$ are arbitrary: $a_2 = \dfrac{a_0}{2!}$, $a_4 = \dfrac{a_0}{4!}$, $\ldots$ and $a_3 = \dfrac{a_1}{3!}$, $a_5 = \dfrac{a_1}{5!}$, $\ldots$ Hence
$$y = a_0\left(1 + \frac{x^2}{2!} + \frac{x^4}{4!} + \cdots\right) + a_1\left(x + \frac{x^3}{3!} + \frac{x^5}{5!} + \cdots\right)$$
$$\boxed{y = a_0\cosh x + a_1\sinh x = c_1e^x + c_2e^{-x}}$$
which agrees with the solution by the auxiliary equation $m^2 - 1 = 0$.

@s 10
The Legendre polynomials are $P_0 = 1$, $P_1 = x$, $P_2 = \dfrac{3x^2-1}{2}$, $P_3 = \dfrac{5x^3 - 3x}{2}$. From $P_3$: $5x^3 = 2P_3 + 3x$, so
$$f(x) = 5x^3 + 3x = (2P_3 + 3x) + 3x = 2P_3 + 6x$$
$$\boxed{5x^3 + 3x = 2P_3(x) + 6P_1(x)}$$
(Check: $2\cdot\dfrac{5x^3-3x}{2} + 6x = 5x^3 + 3x$ ✓.)

**OR.** $x = 0$ is an ordinary point of $(1-x^2)y'' - 2xy' + n(n+1)y = 0$. Put $y = \sum a_kx^k$:
$$\sum(k+2)(k+1)a_{k+2}x^k - \sum k(k-1)a_kx^k - 2\sum ka_kx^k + n(n+1)\sum a_kx^k = 0$$
The coefficient of $x^k$: $(k+2)(k+1)a_{k+2} + \big[n(n+1) - k(k+1)\big]a_k = 0$, and $n(n+1) - k(k+1) = (n-k)(n+k+1)$, so
$$a_{k+2} = -\frac{(n-k)(n+k+1)}{(k+1)(k+2)}\,a_k$$
$$\begin{gathered}a_2 = -\frac{n(n+1)}{2!}a_0,\quad a_4 = \frac{n(n-2)(n+1)(n+3)}{4!}a_0 \\ a_3 = -\frac{(n-1)(n+2)}{3!}a_1,\quad a_5 = \frac{(n-1)(n-3)(n+2)(n+4)}{5!}a_1\end{gathered}$$
$$\boxed{y = a_0\left[1 - \frac{n(n+1)}{2!}x^2 + \frac{n(n-2)(n+1)(n+3)}{4!}x^4 - \cdots\right] + a_1\left[x - \frac{(n-1)(n+2)}{3!}x^3 + \frac{(n-1)(n-3)(n+2)(n+4)}{5!}x^5 - \cdots\right]}$$
The series converges for $|x|<1$. When $n$ is a non-negative integer one of the two series terminates and gives the Legendre polynomial $P_n(x)$ (for $a_0$ or $a_1$ chosen so that $P_n(1) = 1$).

@s 11
**Series.** $J_\nu(x) = \displaystyle\sum_{r=0}^\infty\frac{(-1)^r}{r!\,\Gamma(\nu+r+1)}\left(\frac x2\right)^{\nu+2r}$. For $\nu = \tfrac12$, use $r!\,\Gamma\!\left(r+\tfrac32\right) = \dfrac{(2r+1)!\sqrt\pi}{2^{2r+1}}$ (check: $r = 0$ gives $\Gamma(\tfrac32) = \tfrac{\sqrt\pi}2$ ✓):
$$J_{1/2}(x) = \sum_{r=0}^\infty\frac{(-1)^r2^{2r+1}}{(2r+1)!\sqrt\pi}\left(\frac x2\right)^{2r+\frac12} = \sqrt{\frac{x}{2}}\cdot\frac{2}{\sqrt\pi}\sum_{r=0}^\infty\frac{(-1)^rx^{2r}}{(2r+1)!} = \sqrt{\frac{2}{\pi x}}\,\sin x$$
Similarly, with $\Gamma\!\left(r+\tfrac12\right) = \dfrac{(2r)!\sqrt\pi}{4^rr!}$, $J_{-1/2}(x) = \sqrt{\dfrac{2}{\pi x}}\cos x$.

**Recurrence.** From the series, $xJ_\nu' = \nu J_\nu - xJ_{\nu+1}$ and $xJ_\nu' = -\nu J_\nu + xJ_{\nu-1}$; subtracting gives $J_{\nu+1}(x) = \dfrac{2\nu}{x}J_\nu(x) - J_{\nu-1}(x)$. Putting $\nu = \tfrac12$:
$$\begin{gathered}J_{3/2}(x) = \frac1xJ_{1/2}(x) - J_{-1/2}(x) = \sqrt{\frac{2}{\pi x}}\left(\frac{\sin x}{x} - \cos x\right) \\ \blacksquare\end{gathered}$$

@s 12
Let $\mathbf a = (2,3,-1)$, $\mathbf b = (-1,2,-3)$, $\mathbf c = (3,-4,2)$. The reciprocal system is $\mathbf a' = \dfrac{\mathbf b\times\mathbf c}{[\mathbf a\,\mathbf b\,\mathbf c]}$, $\mathbf b' = \dfrac{\mathbf c\times\mathbf a}{[\mathbf a\,\mathbf b\,\mathbf c]}$, $\mathbf c' = \dfrac{\mathbf a\times\mathbf b}{[\mathbf a\,\mathbf b\,\mathbf c]}$.
$$\begin{gathered}\mathbf b\times\mathbf c = (4-12,\ -9+2,\ 4-6) = (-8,-7,-2) \\ [\mathbf a\,\mathbf b\,\mathbf c] = \mathbf a\cdot(\mathbf b\times\mathbf c) = -16 - 21 + 2 = -35\end{gathered}$$
$$\begin{gathered}\mathbf c\times\mathbf a = (4-6,\ 4+3,\ 9+8) = (-2,7,17) \\ \mathbf a\times\mathbf b = (-9+2,\ 1+6,\ 4+3) = (-7,7,7)\end{gathered}$$
$$\boxed{\mathbf a' = \frac{8\vec i + 7\vec j + 2\vec k}{35},\quad\mathbf b' = \frac{2\vec i - 7\vec j - 17\vec k}{35},\quad\mathbf c' = \frac{\vec i - \vec j - \vec k}{5}}$$
*Check:* $\mathbf a\cdot\mathbf a' = \dfrac{16+21-2}{35} = 1$, $\mathbf b\cdot\mathbf b' = \dfrac{-2-14+51}{35} = 1$, $\mathbf c\cdot\mathbf c' = \dfrac{3+4-2}{5} = 1$, and $\mathbf a\cdot\mathbf b' = \dfrac{4-21+17}{35} = 0$. $\checkmark$

@s 13
**Necessary.** If $\vec a(t)$ has constant direction, write $\vec a = \varphi(t)\,\hat e$ with $\hat e$ a constant unit vector. Then $\dfrac{d\vec a}{dt} = \varphi'\hat e$ and $\vec a\times\dfrac{d\vec a}{dt} = \varphi\varphi'(\hat e\times\hat e) = \vec 0$.

**Sufficient.** Let $\vec a = a\,\hat e$ where $a = |\vec a|$ and $\hat e$ is the unit vector in the direction of $\vec a$. Then $\dfrac{d\vec a}{dt} = a'\hat e + a\dfrac{d\hat e}{dt}$ and
$$\vec a\times\frac{d\vec a}{dt} = a\hat e\times\left(a'\hat e + a\frac{d\hat e}{dt}\right) = a^2\left(\hat e\times\frac{d\hat e}{dt}\right) = \vec 0$$
Since $\hat e\cdot\hat e = 1$, differentiating gives $\hat e\cdot\dfrac{d\hat e}{dt} = 0$, so $\dfrac{d\hat e}{dt}$ is perpendicular to $\hat e$. Then $\left|\hat e\times\dfrac{d\hat e}{dt}\right| = \left|\dfrac{d\hat e}{dt}\right| = 0$ (for $a\ne0$), hence $\dfrac{d\hat e}{dt} = \vec 0$: $\hat e$ is constant, i.e. $\vec a$ has constant direction. $\blacksquare$

@s 14
$\nabla\varphi = \left(\dfrac{\partial\varphi}{\partial x},\dfrac{\partial\varphi}{\partial y},\dfrac{\partial\varphi}{\partial z}\right) = (y^2,\ 2xy + z^3,\ 3yz^2)$. At $(2,-1,1)$:
$$\nabla\varphi = (1,\ -4+1,\ -3) = (1,-3,-3)$$
The unit vector along $\vec i + 2\vec j + 2\vec k$ is $\hat u = \dfrac13(1,2,2)$. The directional derivative is
$$\nabla\varphi\cdot\hat u = \frac{1 - 6 - 6}{3} = \boxed{-\frac{11}{3}}$$
(The function decreases in that direction; the maximum rate of change at the point is $|\nabla\varphi| = \sqrt{19}$.)

@s 15
The $n$th term is
$$u_n = \sqrt{n^4+1} - n^2 = \frac{(n^4+1) - n^4}{\sqrt{n^4+1} + n^2} = \frac{1}{\sqrt{n^4+1} + n^2}>0$$
Compare with $v_n = \dfrac1{n^2}$:
$$\lim_{n\to\infty}\frac{u_n}{v_n} = \lim\frac{n^2}{\sqrt{n^4+1} + n^2} = \lim\frac{1}{\sqrt{1 + n^{-4}} + 1} = \frac12$$
a finite non-zero number. Since $\sum\dfrac1{n^2}$ converges ($p$-series, $p = 2>1$), by the limit comparison test
$$\boxed{\sum\left(\sqrt{n^4+1} - n^2\right)\text{ is convergent.}}$$

@s 16
*Reading note:* the exponent of $(x-3)$ is taken as $n$ (the power-series form $\sum\dfrac{2^n(x-3)^n}{n+3}$).

Ratio test: $\displaystyle\left|\frac{u_{n+1}}{u_n}\right| = \frac{2^{n+1}|x-3|^{n+1}/(n+4)}{2^n|x-3|^n/(n+3)} = 2|x-3|\frac{n+3}{n+4}\to2|x-3|$. The series converges absolutely when $2|x-3|<1$, i.e. $|x-3|<\tfrac12$ (radius of convergence $R = \tfrac12$), so $\tfrac52<x<\tfrac72$.

*Endpoints.*
- $x = \tfrac72$: $\displaystyle\sum\frac{1}{n+3}$ is the harmonic series (shifted), **divergent**.
- $x = \tfrac52$: $\displaystyle\sum\frac{(-1)^n}{n+3}$ is an alternating series with terms decreasing to $0$, **convergent** (conditionally).

$$\boxed{\text{Interval of convergence: }\ \tfrac52\le x<\tfrac72}$$

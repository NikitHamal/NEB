---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH401-2082-Baishakh.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 401
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 401). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
If $y = a\cos(\log x) + b\sin(\log x)$, then show that
(i) $x^2y_2 + xy_1 + y = 0$
(ii) $x^2y_{n+2} + (2n+1)xy_{n+1} + (n^2+1)y_n = 0$. [[5]]

@q 2
Assuming the validity of expansion, apply Maclaurin's series to find the expansion of $f(x) = \dfrac{e^x}{1+e^x}$ as far as the term in $x^3$, and hence find the expansion of $\log(1+e^x)$. [[5]]

@q 3
State L'Hospital's rule. Evaluate $\displaystyle\lim_{x\to a}\left[2 - \dfrac xa\right]^{\tan\left(\frac{\pi x}{2a}\right)}$. [[1+4]]

@q 4
Find the asymptotes of $(x^2-y^2)^2 - 2(x^2+y^2) + x - 1 = 0$. [[5]]

@q 5
Find the radius of curvature at any point $(x, y)$ for the curve $x^{2/3} + y^{2/3} = a^{2/3}$. [[5]]

@q 6
Prove that $\displaystyle\int_0^1\dfrac{\log x}{\sqrt{1+x^2}}\,dx = \dfrac\pi2\log\dfrac12$. [[5]]

@q 7
Apply the differentiation under the integral sign to evaluate $\displaystyle\int_0^\infty\dfrac{e^{-bx}\sin x}{x}\,dx$ and hence evaluate $\displaystyle\int_0^\infty\dfrac{\sin x}{x}\,dx$. [[5]]

@q 8
Define the Gamma function and find the value of $\displaystyle\int_0^{2a}x^5\sqrt{2ax - x^2}\,dx$. [[1+4]]

@q 9
Find the volume of the solid formed by the revolution of the cardioid $r = a(1+\cos\theta)$ about the initial line. [[5]]

@q 10
Solve the differential equation $x\dfrac{dy}{dx} + y\log y = xye^x$. [[5]]

@q 11
If $p$ stands for $\dfrac{dy}{dx}$, solve the differential equation $y = px - \sqrt{m^2+p^2}$, and also find its singular solution. [[5]]

@q 12
Solve the differential equation $(D^2 - 2D + 4)\,y = e^x\cos x$. [[5]]

@q 13
Solve the differential equation $\dfrac{d^2y}{dx^2} - \dfrac1x\dfrac{dy}{dx} + \dfrac{2y}{x^2} = \dfrac{\log x}{x}$. [[5]]

@q 14
Find the angle through which the axes must be turned so that the equation $x + 2y + 5 = 0$ may be reduced to the form $x = c$, and determine the value of $c$. [[5]]

@q 15
Define an ellipse. Obtain the equation of an ellipse in standard form. [[5]]

@q 16
Describe and sketch the graph of the polar equation of the conic $r = \dfrac{12\sec\theta}{3\sec\theta + 2}$. [[5]]
@or
Identify the conic $x^2 + 6xy + y^2 - 4x + 4y - 12 = 0$. Also find its centre and the lengths of its axes. [[5]]
<!-- SOLUTIONS -->

@s 1
Let $y = a\cos(\log x) + b\sin(\log x)$. Then
$$xy_1 = -a\sin(\log x) + b\cos(\log x)$$
**(i)** Differentiate again: $y_1 + xy_2 = \dfrac{-a\cos(\log x) - b\sin(\log x)}{x} = -\dfrac yx$. Multiply by $x$:
$$\boxed{x^2y_2 + xy_1 + y = 0}$$
**(ii)** Differentiate the result of (i) $n$ times by Leibnitz's theorem:
$$\big[x^2y_{n+2} + n(2x)y_{n+1} + \tfrac{n(n-1)}{2}(2)y_n\big] + \big[xy_{n+1} + n\,y_n\big] + y_n = 0$$
The coefficient of $y_{n+1}$ is $2nx + x = (2n+1)x$ and that of $y_n$ is $n(n-1) + n + 1 = n^2 + 1$:
$$\boxed{x^2y_{n+2} + (2n+1)\,x\,y_{n+1} + (n^2+1)\,y_n = 0}$$

@s 2
Write $f = \dfrac{e^x}{1+e^x} = 1 - \dfrac{1}{1+e^x}$. Its derivative satisfies the neat relation $f' = f(1-f)$. Repeated differentiation, with $f(0) = \tfrac12$:

| Derivative | Expression | At $x = 0$ |
|---|---|---|
| $f$ | $\dfrac{e^x}{1+e^x}$ | $\dfrac12$ |
| $f'$ | $f(1-f)$ | $\dfrac14$ |
| $f''$ | $f'(1-2f)$ | $\dfrac14\cdot0 = 0$ |
| $f'''$ | $f''(1-2f) - 2f'^2$ | $0 - 2\cdot\dfrac1{16} = -\dfrac18$ |

Maclaurin's series $f = f(0) + xf'(0) + \dfrac{x^2}{2!}f''(0) + \dfrac{x^3}{3!}f'''(0) + \cdots$:
$$\boxed{\frac{e^x}{1+e^x} = \frac12 + \frac x4 - \frac{x^3}{48} + \cdots}$$
(It is $\tfrac12\left(1 + \tanh\tfrac x2\right)$.)

**Hence the expansion of $\log(1+e^x)$.** Since $\dfrac{d}{dx}\log(1+e^x) = \dfrac{e^x}{1+e^x} = f(x)$, integrate term by term:
$$\log(1+e^x) = C + \frac x2 + \frac{x^2}{8} - \frac{x^4}{192} + \cdots$$
and putting $x = 0$ gives $C = \log 2$:
$$\boxed{\log(1+e^x) = \log2 + \frac x2 + \frac{x^2}{8} - \frac{x^4}{192} + \cdots}$$

@s 3
**L'Hospital's rule.** If $f$ and $g$ are differentiable near $a$, $f(x)\to0$ and $g(x)\to0$ (or both $\to\pm\infty$) as $x\to a$, and $f'(x)/g'(x)$ has a limit, then $\displaystyle\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)}$.

As $x\to a$, $2 - \dfrac xa\to1$ and $\tan\dfrac{\pi x}{2a}\to\infty$: the form is $1^\infty$. With $L$ the limit,
$$\log L = \lim_{x\to a}\tan\frac{\pi x}{2a}\,\log\left(2 - \frac xa\right) = \lim_{x\to a}\frac{\log\left(2 - \frac xa\right)}{\cot\frac{\pi x}{2a}}\quad\left(\tfrac00\right)$$
By L'Hospital's rule,
$$\log L = \lim_{x\to a}\frac{-\dfrac{1/a}{2 - x/a}}{-\dfrac{\pi}{2a}\csc^2\dfrac{\pi x}{2a}} = \lim_{x\to a}\frac{2}{\pi}\cdot\frac{\sin^2\dfrac{\pi x}{2a}}{2 - \dfrac xa} = \frac2\pi\cdot\frac{1}{1} = \frac2\pi$$
$$\boxed{L = e^{2/\pi}}\approx1.890$$

@s 4
Let $F(x,y) = (x^2-y^2)^2 - 2(x^2+y^2) + x - 1$. The highest-degree terms form $\phi_4 = (x^2-y^2)^2 = (x-y)^2(x+y)^2$; the cubic terms are absent ($\phi_3 = 0$), and $\phi_2 = -2(x^2+y^2)$.

The coefficients of $x^4$ and $y^4$ are not zero, so there is no asymptote parallel to an axis. The directions of the oblique asymptotes come from $\phi_4(m) = (1-m^2)^2 = 0$: $m = 1$ and $m = -1$, **each a double root**. For a double root, $y = mx + c$ is an asymptote when the coefficient of $x^2$ in $F(x, mx+c)$ vanishes:
$$\frac{c^2}{2}\phi_4''(m) + c\,\phi_3'(m) + \phi_2(m) = 0$$
With $\phi_4'' = -4(1-m^2) + 8m^2$, at $m = \pm1$ we have $\phi_4'' = 8$, $\phi_3' = 0$ and $\phi_2(\pm1) = -4$:
$$4c^2 - 4 = 0 \;\Rightarrow\; c = \pm1$$
Hence the four asymptotes are
$$\boxed{y = x + 1,\quad y = x - 1,\quad y = -x + 1,\quad y = -x - 1}$$
*Check:* on $y = x\pm1$, $x^2 - y^2 = \mp(2x\pm1)$ and $F = (2x\pm1)^2 - 2\big[x^2 + (x\pm1)^2\big] + x - 1 = x - 2$, which is of degree 1 (below degree $n - 2 = 2$), as an asymptote requires. The same holds for the other two lines.

```figure caption="Question 4: the curve (x² - y²)² - 2(x² + y²) + x - 1 = 0 with its four asymptotes y = ±x ± 1."
xs=np.linspace(-6,6,900); X,Y=np.meshgrid(xs,xs)
F=(X**2-Y**2)**2-2*(X**2+Y**2)+X-1
fig,ax=plt.subplots(figsize=(4.6,4.2))
ax.contour(X,Y,F,levels=[0],colors=['#1d6fb8'],linewidths=1.6)
xl=np.array([-6,6])
for m,c in [(1,1),(1,-1),(-1,1),(-1,-1)]:
    ax.plot(xl,m*xl+c,color='#d9534f',lw=1,ls='--')
ax.axhline(0,color='#aab0ba',lw=0.8); ax.axvline(0,color='#aab0ba',lw=0.8)
ax.set_xlim(-6,6); ax.set_ylim(-6,6); ax.set_aspect('equal')
ax.text(4.1,5.4,'$y=x+1$',color='#d9534f',fontsize=8); ax.text(4.1,-5.5,'$y=-x-1$',color='#d9534f',fontsize=8)
ax.text(-5.9,-5.5,'$y=x-1$',color='#d9534f',fontsize=8); ax.text(-5.9,5.4,'$y=-x+1$',color='#d9534f',fontsize=8)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 5
The curve is the **astroid** $x^{2/3} + y^{2/3} = a^{2/3}$; use $x = a\cos^3t$, $y = a\sin^3t$.
$$x' = -3a\cos^2t\sin t,\quad y' = 3a\sin^2t\cos t,\quad x'' = 3a\,(2\cos t\sin^2t - \cos^3t),\quad y'' = 3a\,(2\sin t\cos^2t - \sin^3t)$$
$$\begin{gathered}x'^2 + y'^2 = 9a^2\sin^2t\cos^2t \\ x'y'' - y'x'' = -9a^2\sin^2t\cos^2t\,(\cos^2t + \sin^2t) = -9a^2\sin^2t\cos^2t\end{gathered}$$
$$\rho = \frac{(x'^2+y'^2)^{3/2}}{|x'y''-y'x''|} = \frac{27a^3\sin^3t\cos^3t}{9a^2\sin^2t\cos^2t} = 3a\sin t\cos t$$
Since $\cos t = (x/a)^{1/3}$ and $\sin t = (y/a)^{1/3}$:
$$\begin{gathered}\boxed{\rho = 3a^{1/3}(xy)^{1/3} = 3\,(axy)^{1/3}} \\ \left(\text{numerically } |\rho| = \tfrac32 a\sin2t\right)\end{gathered}$$
(The sign of $\rho$ depends on the direction of the normal; the magnitude is $3\sqrt[3]{axy}$ and it vanishes at the cusps, where $xy = 0$.)

@s 6
*Note on the printed integrand.* With $\sqrt{1+x^2}$ the integral equals $-0.9552\ldots$, whereas $\tfrac\pi2\log\tfrac12 = -1.0888\ldots$. The stated result is the classical one for $\sqrt{1-x^2}$ (the sign in the root has been lost in print), so the proof below is for
$$I = \int_0^1\frac{\log x}{\sqrt{1-x^2}}\,dx = \frac\pi2\log\frac12$$
Put $x = \sin\theta$, $dx = \cos\theta\,d\theta$, $\sqrt{1-x^2} = \cos\theta$:
$$I = \int_0^{\pi/2}\log\sin\theta\,d\theta = J$$
Using $\displaystyle\int_0^{\pi/2}f(\theta)d\theta = \int_0^{\pi/2}f\!\left(\tfrac\pi2 - \theta\right)d\theta$, also $J = \displaystyle\int_0^{\pi/2}\log\cos\theta\,d\theta$. Adding,
$$2J = \int_0^{\pi/2}\log(\sin\theta\cos\theta)\,d\theta = \int_0^{\pi/2}\log\sin2\theta\,d\theta - \frac\pi2\log2$$
and with $\phi = 2\theta$, $\displaystyle\int_0^{\pi/2}\log\sin2\theta\,d\theta = \tfrac12\int_0^\pi\log\sin\phi\,d\phi = \int_0^{\pi/2}\log\sin\phi\,d\phi = J$ (symmetry of $\sin\phi$ about $\pi/2$). So $2J = J - \dfrac\pi2\log2$ and
$$\begin{gathered}\boxed{J = -\frac\pi2\log2 = \frac\pi2\log\frac12} \\ \text{(numerically } -1.0888\text{)}\end{gathered}$$

@s 7
Let $I(b) = \displaystyle\int_0^\infty\frac{e^{-bx}\sin x}{x}\,dx$, $b > 0$. Differentiating under the integral sign (the integral of the derivative converges uniformly for $b\ge b_0 > 0$):
$$\frac{dI}{db} = -\int_0^\infty e^{-bx}\sin x\,dx = -\left[\frac{e^{-bx}(-b\sin x - \cos x)}{b^2+1}\right]_0^\infty = -\frac{1}{1+b^2}$$
Integrating, $I(b) = -\tan^{-1}b + C$. As $b\to\infty$ the integrand tends to $0$ (for example $|I(b)|\le\int_0^\infty e^{-bx}dx = 1/b$), so $I(\infty) = 0$ and $C = \dfrac\pi2$:
$$\boxed{\int_0^\infty\frac{e^{-bx}\sin x}{x}\,dx = \frac\pi2 - \tan^{-1}b = \cot^{-1}b}$$
Letting $b\to0^+$:
$$\boxed{\int_0^\infty\frac{\sin x}{x}\,dx = \frac\pi2}$$
(Check: $b = 2$ gives $\tfrac\pi2 - \tan^{-1}2 = 0.46365$, which matches numerical integration.)

@s 8
**Gamma function.** For $n>0$, $\Gamma(n) = \displaystyle\int_0^\infty e^{-x}x^{n-1}dx$; $\Gamma(n+1) = n\Gamma(n)$, $\Gamma(\tfrac12) = \sqrt\pi$, and $\displaystyle\int_0^{\pi/2}\sin^{2p-1}\theta\cos^{2q-1}\theta\,d\theta = \frac{\Gamma(p)\Gamma(q)}{2\Gamma(p+q)}$.

Put $x = 2a\sin^2\theta$. Then $dx = 4a\sin\theta\cos\theta\,d\theta$ and $2ax - x^2 = x(2a-x) = 4a^2\sin^2\theta\cos^2\theta$, so $\sqrt{2ax - x^2} = 2a\sin\theta\cos\theta$; the limits $0\to2a$ become $0\to\tfrac\pi2$:
$$I = \int_0^{\pi/2}(2a)^5\sin^{10}\theta\cdot2a\sin\theta\cos\theta\cdot4a\sin\theta\cos\theta\,d\theta = 256\,a^7\int_0^{\pi/2}\sin^{12}\theta\cos^2\theta\,d\theta$$
With $2p - 1 = 12$, $2q - 1 = 2$, i.e. $p = \tfrac{13}2$, $q = \tfrac32$:
$$I = 256a^7\cdot\frac{\Gamma(13/2)\Gamma(3/2)}{2\Gamma(8)} = 128a^7\cdot\frac{\Gamma(13/2)\Gamma(3/2)}{7!}$$
$\Gamma\!\left(\tfrac{13}2\right) = \tfrac{11}2\cdot\tfrac92\cdot\tfrac72\cdot\tfrac52\cdot\tfrac32\cdot\tfrac12\sqrt\pi = \dfrac{10395}{64}\sqrt\pi$, $\ \Gamma\!\left(\tfrac32\right) = \dfrac{\sqrt\pi}2$, $\ 7! = 5040$:
$$I = 128a^7\cdot\frac{10395\pi/128}{5040} = \frac{10395}{5040}\pi a^7 = \boxed{\frac{33\pi}{16}\,a^7}\approx6.480\,a^7$$

@s 9
The cardioid $r = a(1+\cos\theta)$ is symmetric about the initial line; revolving its upper half $0\le\theta\le\pi$ about the initial line gives the solid. The volume of revolution about the initial line is
$$V = \frac{2\pi}{3}\int_0^{\pi}r^3\sin\theta\,d\theta = \frac{2\pi a^3}{3}\int_0^\pi(1+\cos\theta)^3\sin\theta\,d\theta$$
Put $u = 1 + \cos\theta$, $du = -\sin\theta\,d\theta$; the limits $\theta = 0,\pi$ become $u = 2, 0$:
$$V = \frac{2\pi a^3}{3}\int_0^2u^3\,du = \frac{2\pi a^3}{3}\cdot\frac{16}{4} = \boxed{\frac{8\pi a^3}{3}}$$

```figure caption="Question 9: the cardioid r = a(1 + cos θ) (a = 1); its upper half is revolved about the initial line."
th=np.linspace(0,2*np.pi,500); r=1+np.cos(th)
fig,ax=plt.subplots(figsize=(4.4,3.0))
ax.plot(r*np.cos(th),r*np.sin(th),color='#1d6fb8')
t2=np.linspace(0,np.pi,200); r2=1+np.cos(t2)
ax.fill(r2*np.cos(t2),r2*np.sin(t2),color='#1d6fb8',alpha=0.1)
ax.axhline(0,color='#d9534f',ls='--',lw=1.2); ax.text(2.02,0.06,'initial line',color='#d9534f',fontsize=8)
ax.plot([0],[0],'o',color='#14181f',ms=3.5); ax.text(0.04,-0.2,'pole',fontsize=8)
ax.text(1.2,0.9,'$r=a(1+\\cos\\theta)$',fontsize=8)
ax.set_aspect('equal'); ax.set_xlim(-0.4,3.1); ax.set_ylim(-1.5,1.5)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 10
Divide by $xy$: $\dfrac1y\dfrac{dy}{dx} + \dfrac{\log y}{x} = e^x$. Put $v = \log y$, so $\dfrac{dv}{dx} = \dfrac1y\dfrac{dy}{dx}$:
$$\begin{gathered}\frac{dv}{dx} + \frac vx = e^x \\ \text{IF} = e^{\int dx/x} = x\end{gathered}$$
$$xv = \int xe^x\,dx = (x-1)e^x + C$$
$$\boxed{\log y = \left(1 - \frac1x\right)e^x + \frac Cx}$$

@s 11
$y = px - \sqrt{m^2+p^2}$ is of **Clairaut's form** $y = px + f(p)$ with $f(p) = -\sqrt{m^2+p^2}$, so the general solution is obtained by replacing $p$ with an arbitrary constant $c$:
$$\boxed{y = cx - \sqrt{m^2 + c^2}}$$
**Singular solution.** Differentiate $y = px + f(p)$ with respect to $p$ (treating $x$ as constant): $x + f'(p) = 0$, i.e.
$$x = \frac{p}{\sqrt{m^2+p^2}}\;\Rightarrow\;p^2 = x^2(m^2+p^2)\;\Rightarrow\;p^2 = \frac{m^2x^2}{1-x^2},\quad\sqrt{m^2+p^2} = \frac{m}{\sqrt{1-x^2}}$$
Substituting into the equation,
$$y = px - \sqrt{m^2+p^2} = \frac{mx^2}{\sqrt{1-x^2}} - \frac{m}{\sqrt{1-x^2}} = -m\sqrt{1-x^2}$$
Eliminating the root (the envelope of the family of lines):
$$\boxed{y^2 = m^2(1-x^2)\quad\text{i.e.}\quad m^2x^2 + y^2 = m^2}$$
This is an ellipse $x^2 + \dfrac{y^2}{m^2} = 1$, which touches every line of the general solution. *Check:* a line $y = cx + k$ touches $x^2 + \dfrac{y^2}{m^2} = 1$ exactly when $k^2 = c^2 + m^2$; here $k = -\sqrt{m^2+c^2}$, so every member of the general solution is a tangent of this ellipse.

@s 12
Auxiliary equation $m^2 - 2m + 4 = 0\Rightarrow m = 1\pm i\sqrt3$, so
$$y_c = e^x\left(c_1\cos\sqrt3\,x + c_2\sin\sqrt3\,x\right)$$
Particular integral (shift $D\to D+1$):
$$y_p = \frac{1}{D^2-2D+4}\,e^x\cos x = e^x\frac{1}{(D+1)^2 - 2(D+1) + 4}\cos x = e^x\frac{1}{D^2+3}\cos x = e^x\,\frac{\cos x}{-1+3} = \frac12e^x\cos x$$
$$\boxed{y = e^x\left(c_1\cos\sqrt3\,x + c_2\sin\sqrt3\,x\right) + \frac12e^x\cos x}$$

@s 13
Multiply by $x^2$: $x^2y'' - xy' + 2y = x\log x$, a Cauchy–Euler equation. Put $z = \log x$, $x = e^z$, $x^2D^2 = D_z(D_z-1)$, $xD = D_z$:
$$\big[D_z(D_z - 1) - D_z + 2\big]y = ze^z\;\Longrightarrow\;(D_z^2 - 2D_z + 2)\,y = ze^z$$
Auxiliary roots $m = 1\pm i$, so $y_c = e^z(c_1\cos z + c_2\sin z)$. Particular integral:
$$y_p = e^z\frac{1}{(D+1)^2 - 2(D+1) + 2}\,z = e^z\frac{1}{D^2+1}\,z = e^z(1 - D^2 + \cdots)z = ze^z$$
$$\boxed{y = x\big[c_1\cos(\log x) + c_2\sin(\log x)\big] + x\log x}$$

@s 14
Rotate the axes through an angle $\alpha$ (anticlockwise): $x = X\cos\alpha - Y\sin\alpha,\ y = X\sin\alpha + Y\cos\alpha$. Then
$$x + 2y + 5 = (\cos\alpha + 2\sin\alpha)X + (2\cos\alpha - \sin\alpha)Y + 5 = 0$$
To reach the form $X = c$ the coefficient of $Y$ must vanish: $2\cos\alpha - \sin\alpha = 0$, i.e. $\tan\alpha = 2$, with $\cos\alpha = \dfrac1{\sqrt5}$ and $\sin\alpha = \dfrac2{\sqrt5}$. Then the coefficient of $X$ is $\dfrac{1+4}{\sqrt5} = \sqrt5$:
$$\sqrt5\,X + 5 = 0\;\Longrightarrow\;X = -\sqrt5$$
$$\boxed{\alpha = \tan^{-1}2\approx63.43^\circ,\qquad c = -\sqrt5}$$
(The line is at distance $5/\sqrt5 = \sqrt5$ from the origin; it passes through $(-1,-2)$. Rotating through $\alpha + 180^\circ$ would give $c = +\sqrt5$.)

```figure caption="Question 14: axes OX, OY turned through α = tan⁻¹2 so that the line x + 2y + 5 = 0 becomes X = -√5."
fig,ax=plt.subplots(figsize=(4.4,3.8))
xs=np.array([-4,2]); ax.plot(xs,(-5-xs)/2,color='#1d6fb8',lw=1.6); ax.text(-3.9,-0.95,'$x+2y+5=0$',color='#1d6fb8',fontsize=8,ha='left')
ax.annotate('',xy=(3.2,0),xytext=(-3,0),arrowprops=dict(arrowstyle='->',color='#14181f')); ax.text(3.25,-0.25,'$x$',fontsize=9)
ax.annotate('',xy=(0,3.2),xytext=(0,-3.4),arrowprops=dict(arrowstyle='->',color='#14181f')); ax.text(0.1,3.2,'$y$',fontsize=9)
c,s=1/np.sqrt(5),2/np.sqrt(5)
ax.annotate('',xy=(3.0*c,3.0*s),xytext=(-3.0*c,-3.0*s),arrowprops=dict(arrowstyle='->',color='#d9534f'))
ax.text(3.0*c+0.1,3.0*s,'$X$',color='#d9534f',fontsize=9)
ax.annotate('',xy=(-2.0*s,2.0*c),xytext=(2.0*s,-2.0*c),arrowprops=dict(arrowstyle='->',color='#d9534f'))
ax.text(-2.0*s-0.4,2.0*c+0.1,'$Y$',color='#d9534f',fontsize=9)
ax.plot([-1],[-2],'o',color='#14181f',ms=3.5); ax.text(-1.0,-2.45,'$X=-\\sqrt{5}$',fontsize=8)
ax.text(0.5,0.2,'$\\alpha$',fontsize=9)
ax.set_aspect('equal'); ax.set_xlim(-4.2,3.8); ax.set_ylim(-3.6,3.6); ax.axis('off')
```

@s 15
**Definition.** An ellipse is the locus of a point $P$ moving in a plane so that the sum of its distances from two fixed points $S, S'$ (the foci) is a constant $2a$ greater than $SS'$. Equivalently, it is the locus of a point whose distance from a fixed point (focus) is a constant $e<1$ times its distance from a fixed line (directrix).

**Derivation.** Take the origin at the midpoint of $SS'$ and the x-axis along $S'S$; let $S = (c, 0)$, $S' = (-c, 0)$ with $c < a$. For $P(x,y)$, $PS + PS' = 2a$:
$$\sqrt{(x-c)^2 + y^2} = 2a - \sqrt{(x+c)^2+y^2}$$
Squaring and simplifying gives $a\sqrt{(x+c)^2 + y^2} = a^2 + cx$; squaring once more and collecting,
$$(a^2 - c^2)\,x^2 + a^2y^2 = a^2(a^2 - c^2)$$
With $b^2 = a^2 - c^2 > 0$:
$$\begin{gathered}\boxed{\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1} \\ b^2 = a^2(1 - e^2),\quad e = \frac ca<1\end{gathered}$$
Vertices $(\pm a,0)$, foci $(\pm ae, 0)$, directrices $x = \pm\dfrac ae$, major axis $2a$, minor axis $2b$, latus rectum $\dfrac{2b^2}a$.

```figure caption="Question 15: the ellipse x²/a² + y²/b² = 1, foci S, S′ and directrices x = ±a/e."
a,b=2.6,1.7; c=np.sqrt(a*a-b*b); e=c/a
t=np.linspace(0,2*np.pi,400)
fig,ax=plt.subplots(figsize=(5.4,2.9))
ax.plot(a*np.cos(t),b*np.sin(t),color='#1d6fb8')
ax.axhline(0,color='#aab0ba',lw=0.8); ax.axvline(0,color='#aab0ba',lw=0.8)
for sgn in (1,-1):
    ax.axvline(sgn*a/e,color='#b8860b',ls='--',lw=1.1)
ax.text(a/e+0.08,1.6,'$x=a/e$',color='#b8860b',fontsize=8); ax.text(-a/e-0.08,1.6,'$x=-a/e$',color='#b8860b',fontsize=8,ha='right')
for px in (c,-c): ax.plot([px],[0],'o',color='#14181f',ms=3.5)
ax.text(c+0.06,-0.3,'$S$',fontsize=9); ax.text(-c-0.06,-0.3,"$S'$",fontsize=9,ha='right')
ax.text(a+0.05,0.08,'$a$',fontsize=8); ax.text(0.06,b+0.06,'$b$',fontsize=8)
ax.set_aspect('equal'); ax.set_xlim(-5.6,5.6); ax.set_ylim(-2.1,2.2)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 16
Since $\sec\theta = 1/\cos\theta$, multiply numerator and denominator by $\cos\theta$:
$$r = \frac{12}{3 + 2\cos\theta} = \frac{4}{1 + \tfrac23\cos\theta}$$
Compare with $\dfrac\ell r = 1 + e\cos\theta$: semi-latus rectum $\ell = 4$ and $e = \dfrac23<1$, so the conic is an **ellipse** with one focus at the pole.

| Feature | Value |
|---|---|
| Directrix | $x = \ell/e = 6$ |
| Vertices ($\theta = 0$, $\pi$) | $r = \tfrac{12}5$ and $r = 12$: $(2.4, 0)$ and $(-12, 0)$ |
| Major axis | $2a = 14.4$, $a = 7.2$ |
| Centre | $(-4.8, 0)$ |
| $c = ae$ | $4.8$: foci $(0,0)$ and $(-9.6, 0)$ |
| Semi-minor axis | $b = a\sqrt{1-e^2} = 7.2\cdot\dfrac{\sqrt5}{3} = \dfrac{12}{\sqrt5}\approx5.37$ ($b^2 = a\ell = 28.8$) |
| Ends of latus rectum ($\theta = \pm\tfrac\pi2$) | $r = 4$: $(0, \pm4)$ |

Cartesian form: $3r + 2x = 12\Rightarrow9(x^2+y^2) = (12-2x)^2\Rightarrow5x^2 + 9y^2 + 48x - 144 = 0$, i.e. $\dfrac{(x+4.8)^2}{51.84} + \dfrac{y^2}{28.8} = 1$. $\checkmark$

```figure caption="Question 16: r = 12/(3 + 2 cos θ), an ellipse with eccentricity 2/3, focus at the pole and directrix x = 6."
th=np.linspace(0,2*np.pi,500); r=12/(3+2*np.cos(th))
fig,ax=plt.subplots(figsize=(5.6,3.0))
ax.plot(r*np.cos(th),r*np.sin(th),color='#1d6fb8')
ax.axvline(6,color='#b8860b',ls='--',lw=1.1); ax.text(6.2,4.2,'directrix\n$x=6$',color='#b8860b',fontsize=8)
ax.axhline(0,color='#aab0ba',lw=0.8); ax.axvline(0,color='#aab0ba',lw=0.8)
for p,l,dx,dy in [((0,0),'$F_1$ (pole)',0.3,-1.2),((-9.6,0),'$F_2$',-0.4,-1.2),((2.4,0),'(2.4, 0)',0.1,0.5),((-12,0),'(-12, 0)',-0.6,0.8),((-4.8,0),'centre',-1.0,-1.3),((0,4),'(0, 4)',0.3,0.1),((0,-4),'(0, -4)',0.3,-0.9)]:
    ax.plot([p[0]],[p[1]],'o',color='#14181f',ms=3.5); ax.text(p[0]+dx,p[1]+dy,l,fontsize=8)
ax.set_aspect('equal'); ax.set_xlim(-13.5,9.5); ax.set_ylim(-6.8,6.8)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

**OR.** For $S = x^2 + 6xy + y^2 - 4x + 4y - 12$ we have $a = 1,\ h = 3,\ b = 1$, so $h^2 - ab = 8>0$. The determinant
$$\Delta = \begin{vmatrix}1&3&-2\\3&1&2\\-2&2&-12\end{vmatrix} = 1(-16) - 3(-32) + (-2)(8) = 64\ne0$$
so the conic is a **non-degenerate hyperbola**.

**Centre.** $\partial S/\partial x = 2x + 6y - 4 = 0$ and $\partial S/\partial y = 6x + 2y + 4 = 0$ give $x + 3y = 2$, $3x + y = -2$, hence $x = -1,\ y = 1$. Centre $= \boxed{(-1, 1)}$.

**Reduced form.** With $x = X - 1,\ y = Y + 1$ the constant term is $S(-1,1) = 1 - 6 + 1 + 4 + 4 - 12 = -8$:
$$X^2 + 6XY + Y^2 = 8$$
The matrix $\begin{pmatrix}1&3\\3&1\end{pmatrix}$ has eigenvalues $4$ (eigenvector $(1,1)$) and $-2$ (eigenvector $(-1,1)$). In the principal axes $(u,v)$ (the axes turned through $45^\circ$):
$$4u^2 - 2v^2 = 8\;\Longrightarrow\;\frac{u^2}{2} - \frac{v^2}{4} = 1$$
So $a^2 = 2$, $b^2 = 4$:

| Quantity | Value |
|---|---|
| Transverse axis | $2a = \boxed{2\sqrt2}\approx2.83$, along $y - 1 = x + 1$ ($y = x+2$) |
| Conjugate axis | $2b = \boxed{4}$, along $y - 1 = -(x+1)$ ($y = -x$) |
| Vertices | $(0, 2)$ and $(-2, 0)$ |
| Eccentricity | $e = \sqrt{1 + b^2/a^2} = \sqrt3$ |
| Foci | $(-1\pm\sqrt3,\ 1\pm\sqrt3)$ |
| Asymptotes | $X^2 + 6XY + Y^2 = 0$, i.e. $Y = (-3\pm2\sqrt2)X$ through $(-1, 1)$ |

```figure caption="Question 16 (OR): the hyperbola x² + 6xy + y² - 4x + 4y - 12 = 0, centre (-1, 1), transverse axis along y = x + 2, with its asymptotes."
t=np.linspace(-1.6,1.6,400)
u1=np.array([1,1])/np.sqrt(2); v1=np.array([-1,1])/np.sqrt(2); C=np.array([-1,1])[:,None]
fig,ax=plt.subplots(figsize=(4.6,4.2))
for sg in (1,-1):
    pts=C+sg*np.outer(u1,np.sqrt(2)*np.cosh(t))+np.outer(v1,2*np.sinh(t))
    ax.plot(pts[0],pts[1],color='#1d6fb8')
xl=np.array([-6,5])
for m in (-3+2*np.sqrt(2),-3-2*np.sqrt(2)):
    ax.plot(xl,1+m*(xl+1),color='#d9534f',lw=0.9,ls='--')
ax.plot([-4,3],[-2,5],color='#2e8b57',lw=1); ax.plot([-3,2],[3,-2],color='#b8860b',lw=1,ls=':')
ax.plot([-1],[1],'o',color='#14181f',ms=3.5); ax.text(-0.8,0.5,'centre (-1,1)',fontsize=8)
ax.plot([0,-2],[2,0],'o',color='#14181f',ms=3.5)
ax.text(0.15,2.05,'(0,2)',fontsize=8); ax.text(-2.9,-0.4,'(-2,0)',fontsize=8)
ax.axhline(0,color='#aab0ba',lw=0.8); ax.axvline(0,color='#aab0ba',lw=0.8)
ax.set_aspect('equal'); ax.set_xlim(-6,5); ax.set_ylim(-5,6)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

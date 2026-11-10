---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH401-2081-Bhadra.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 401
year_bs: 2081 Bhadra
cal: BS
year_ad: 2024
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 401). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
State Leibnitz's theorem. If $y = \left(x + \sqrt{1+x^2}\right)^m$, then show that $(1+x^2)y_{n+2} + (2n+1)xy_{n+1} + (n^2 - m^2)y_n = 0$. [[5]]

@q 2
State Lagrange's mean value theorem. Verify it for the function $f(x) = e^x$, $x\in[1,2]$. [[5]]

@q 3
State L'Hospital's rule. Evaluate $\displaystyle\lim_{x\to0}(\cot x)^{\sin2x}$. [[5]]

@q 4
Define asymptote to a curve with its types. Determine the asymptotes to the curve $4x^3 - 3xy^2 - y^3 + 2x^2 - xy - y^2 - 1 = 0$. [[1+1+3]]

@q 5
Find the radius of curvature at the origin for the curve $x^3 + y^3 = 3axy$. [[5]]

@q 6
What do you mean by the fundamental theorem of integral calculus? Hence show that $\displaystyle\int_0^a\dfrac{dx}{x + \sqrt{a^2-x^2}} = \dfrac\pi4$. [[5]]

@q 7
Using the rule of differentiation under the integral sign, evaluate $\displaystyle\int_0^{\pi/2}\dfrac{\log(1 + \cos\alpha\cos x)}{\cos x}\,dx$. [[5]]

@q 8
Define Beta and Gamma functions. Use them to evaluate $\displaystyle\int_0^{2a}x^5\sqrt{2ax - x^2}\,dx$. [[5]]

@q 9
Find the area enclosed by $y^2(a-x) = x^3$ and its asymptote. [[5]]

@q 10
Solve: $\dfrac{dy}{dx} + x\sin2y = x^3\cos^2y$. [[5]]

@q 11
If $p$ denotes $\dfrac{dy}{dx}$, then find the general and singular solution of $y = px + \dfrac ap$. [[5]]

@q 12
Solve: $(D^2 + 4D + 4)\,y = x^2 + e^{2x}$. [[5]]

@q 13
Solve: $x^2\dfrac{d^2y}{dx^2} + x\dfrac{dy}{dx} - 4y = x^2$. [[5]]

@q 14
What does the equation of the lines $7x^2 + 4xy + 4y^2 = 0$ become when the axes are the bisectors of the angle between them? [[5]]

@q 15
Derive the equation of a hyperbola in standard form. [[5]]

@q 16
Describe and sketch the graph of the curve $r = \dfrac{12}{3 + \cos\theta}$. [[5]]
@or
Prove that $2x^2 + 3y^2 - 4x - 12y + 13 = 0$ represents the equation of an ellipse. Hence find its centre, the lengths of its axes and its eccentricity. [[5]]
<!-- SOLUTIONS -->

@s 1
**Leibnitz's theorem.** If $u$ and $v$ are functions of $x$ possessing $n$th derivatives, then
$$(uv)_n = u_nv + \binom n1u_{n-1}v_1 + \binom n2u_{n-2}v_2 + \cdots + uv_n$$
Let $y = \left(x + \sqrt{1+x^2}\right)^m$. Then
$$y_1 = m\left(x+\sqrt{1+x^2}\right)^{m-1}\left(1 + \frac{x}{\sqrt{1+x^2}}\right) = \frac{m\left(x+\sqrt{1+x^2}\right)^m}{\sqrt{1+x^2}} = \frac{my}{\sqrt{1+x^2}}$$
so $(1+x^2)y_1^2 = m^2y^2$. Differentiate with respect to $x$ and divide by $2y_1$:
$$(1+x^2)\,y_2 + x\,y_1 - m^2y = 0 \tag{1}$$
Differentiate (1) $n$ times with Leibnitz's theorem:
$$\big[(1+x^2)y_{n+2} + 2nx\,y_{n+1} + n(n-1)y_n\big] + \big[x\,y_{n+1} + n\,y_n\big] - m^2y_n = 0$$
$$\boxed{(1+x^2)\,y_{n+2} + (2n+1)\,x\,y_{n+1} + (n^2 - m^2)\,y_n = 0}$$

@s 2
**Lagrange's mean value theorem.** If $f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, there exists a point $c\in(a,b)$ such that
$$f'(c) = \frac{f(b) - f(a)}{b - a}$$
**Verification.** $f(x) = e^x$ is continuous and differentiable everywhere, so both hypotheses hold on $[1, 2]$. Here $f'(x) = e^x$ and
$$\frac{f(2) - f(1)}{2 - 1} = e^2 - e = e(e-1)$$
We need $e^c = e(e-1)$, so $c = 1 + \log(e-1) = 1 + 0.5413 = 1.5413$. Since $1 < 1.5413 < 2$, such a $c$ exists in $(1,2)$, and the theorem is verified. $\blacksquare$

@s 3
**L'Hospital's rule.** If $f(x), g(x)\to0$ (or $\to\pm\infty$) as $x\to a$ and $\lim\dfrac{f'(x)}{g'(x)}$ exists, then $\displaystyle\lim\frac{f(x)}{g(x)} = \lim\frac{f'(x)}{g'(x)}$.

As $x\to0^+$, $\cot x\to\infty$ and $\sin2x\to0$: the form is $\infty^0$. Let $L$ be the limit:
$$\log L = \lim_{x\to0}\sin2x\,\log\cot x = \lim_{x\to0}\frac{\log\cot x}{\csc2x}\quad\left(\tfrac\infty\infty\right)$$
Since $\dfrac{d}{dx}\log\cot x = -\dfrac{\csc^2x}{\cot x} = -\dfrac{2}{\sin2x}$ and $\dfrac{d}{dx}\csc2x = -2\csc2x\cot2x = -\dfrac{2\cos2x}{\sin^22x}$,
$$\log L = \lim_{x\to0}\frac{-2/\sin2x}{-2\cos2x/\sin^22x} = \lim_{x\to0}\frac{\sin2x}{\cos2x} = 0$$
$$\boxed{L = e^0 = 1}$$

@s 4
**Asymptote.** A straight line is an asymptote of a curve if the perpendicular distance of a point of the curve from the line tends to zero as the point moves to infinity along a branch of the curve. **Types:** (i) vertical (parallel to the y-axis), (ii) horizontal (parallel to the x-axis), (iii) oblique ($y = mx + c$).

Let $\phi_3 = 4x^3 - 3xy^2 - y^3$, $\phi_2 = 2x^2 - xy - y^2$, $\phi_1 = 0$. The coefficients of $x^3$ and $y^3$ are non-zero, so there is no asymptote parallel to an axis. Put $y/x = m$:
$$\begin{gathered}\phi_3(m) = 4 - 3m^2 - m^3 = -(m-1)(m+2)^2 \\ \phi_2(m) = 2 - m - m^2 = (1-m)(2+m)\end{gathered}$$
- **$m = 1$ (simple root).** $c = -\dfrac{\phi_2(1)}{\phi_3'(1)}$, with $\phi_3'(m) = -6m - 3m^2$, so $\phi_3'(1) = -9$ and $\phi_2(1) = 0$: $c = 0$. Asymptote $y = x$.
- **$m = -2$ (double root).** Here $\phi_3(-2) = \phi_3'(-2) = 0$ and $\phi_2(-2) = 0$, so the parallel asymptotes are given by $\dfrac{c^2}2\phi_3''(-2) + c\,\phi_2'(-2) + \phi_1(-2) = 0$. With $\phi_3'' = -6 - 6m = 6$ and $\phi_2' = -1 - 2m = 3$: $3c^2 + 3c = 0$, $c = 0$ or $c = -1$. Asymptotes $y = -2x$ and $y = -2x - 1$.

$$\boxed{y = x,\qquad y = -2x,\qquad y = -2x - 1}$$
*Check:* on $y = -2x + c$, $F = 4x^3 - 12x^3 + 8x^3 + (2 + 2 - 4)x^2 + \ldots$; for $c = 0$ and $c = -1$ the result is the constant $-1$ (degree $0\le n-2 = 1$), and on $y = x$ it is also $-1$. $\checkmark$

```figure caption="Question 4: the cubic 4x³ - 3xy² - y³ + 2x² - xy - y² - 1 = 0 with its three asymptotes."
xs=np.linspace(-5,5,1000); X,Y=np.meshgrid(xs,xs)
F=4*X**3-3*X*Y**2-Y**3+2*X**2-X*Y-Y**2-1
fig,ax=plt.subplots(figsize=(4.6,4.2))
ax.contour(X,Y,F,levels=[0],colors=['#1d6fb8'],linewidths=1.6)
xl=np.array([-5,5])
ax.plot(xl,xl,color='#d9534f',ls='--',lw=1); ax.plot(xl,-2*xl,color='#2e8b57',ls='--',lw=1); ax.plot(xl,-2*xl-1,color='#b8860b',ls='--',lw=1)
ax.text(3.2,3.6,'$y=x$',color='#d9534f',fontsize=8); ax.text(-2.4,4.4,'$y=-2x$',color='#2e8b57',fontsize=8); ax.text(1.0,-4.6,'$y=-2x-1$',color='#b8860b',fontsize=8)
ax.axhline(0,color='#aab0ba',lw=0.8); ax.axvline(0,color='#aab0ba',lw=0.8)
ax.set_xlim(-5,5); ax.set_ylim(-5,5); ax.set_aspect('equal')
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 5
Near the origin the lowest-degree term of $x^3 + y^3 - 3axy = 0$ is $-3axy$, so $xy = 0$: the curve has a node at the origin with tangents $y = 0$ (the x-axis) and $x = 0$ (the y-axis).

*Branch tangent to the x-axis.* Newton's formula is $\rho = \displaystyle\lim_{x\to0}\frac{x^2}{2y}$. Near the origin $y$ is of order $x^2$, so $y^3$ is negligible and $x^3 + y^3 = 3axy$ gives $3axy \approx x^3$, i.e. $y\approx\dfrac{x^2}{3a}$. Hence
$$\rho = \lim\frac{x^2}{2\cdot x^2/(3a)} = \frac{3a}{2}$$
*Branch tangent to the y-axis.* By the symmetry of the curve in $y = x$, $\rho = \lim\dfrac{y^2}{2x} = \dfrac{3a}{2}$.
$$\boxed{\rho = \frac{3a}{2}\text{ at the origin (for both branches)}}$$

@s 6
**Fundamental theorem of integral calculus.** *Part 1:* if $f$ is continuous on $[a,b]$ then $F(x) = \displaystyle\int_a^xf(t)\,dt$ is differentiable and $F'(x) = f(x)$. *Part 2:* if $G$ is any antiderivative of $f$ ($G' = f$), then $\displaystyle\int_a^bf(x)\,dx = G(b) - G(a)$. A consequence is the substitution rule and the property $\displaystyle\int_0^af(x)\,dx = \int_0^af(a-x)\,dx$.

Put $x = a\sin\theta$, $dx = a\cos\theta\,d\theta$, $\sqrt{a^2-x^2} = a\cos\theta$:
$$I = \int_0^{\pi/2}\frac{a\cos\theta\,d\theta}{a\sin\theta + a\cos\theta} = \int_0^{\pi/2}\frac{\cos\theta}{\sin\theta + \cos\theta}\,d\theta$$
Replacing $\theta$ by $\tfrac\pi2 - \theta$ (the property above) gives also $I = \displaystyle\int_0^{\pi/2}\frac{\sin\theta}{\sin\theta+\cos\theta}\,d\theta$. Adding,
$$2I = \int_0^{\pi/2}1\,d\theta = \frac\pi2\;\Longrightarrow\;\boxed{I = \frac\pi4}$$

@s 7
Let $I(\alpha) = \displaystyle\int_0^{\pi/2}\frac{\log(1+\cos\alpha\cos x)}{\cos x}\,dx$, $0<\alpha<\pi$. Differentiating under the integral sign:
$$\frac{dI}{d\alpha} = \int_0^{\pi/2}\frac{1}{\cos x}\cdot\frac{-\sin\alpha\cos x}{1 + \cos\alpha\cos x}\,dx = -\sin\alpha\int_0^{\pi/2}\frac{dx}{1+\cos\alpha\cos x}$$
With $t = \tan\dfrac x2$, $\cos x = \dfrac{1-t^2}{1+t^2}$, $dx = \dfrac{2\,dt}{1+t^2}$:
$$\int_0^{\pi/2}\frac{dx}{1+\cos\alpha\cos x} = \int_0^1\frac{2\,dt}{(1+\cos\alpha) + (1-\cos\alpha)t^2} = \frac{2}{\sin\alpha}\tan^{-1}\!\left(\sqrt{\frac{1-\cos\alpha}{1+\cos\alpha}}\,t\right)\Bigg|_0^1 = \frac{2}{\sin\alpha}\cdot\frac\alpha2 = \frac{\alpha}{\sin\alpha}$$
Hence $\dfrac{dI}{d\alpha} = -\alpha$ and $I = -\dfrac{\alpha^2}{2} + C$. At $\alpha = \dfrac\pi2$ the integrand is $\dfrac{\log1}{\cos x} = 0$, so $I = 0$ and $C = \dfrac{\pi^2}{8}$:
$$\boxed{I(\alpha) = \frac{\pi^2}{8} - \frac{\alpha^2}{2} = \frac{\pi^2 - 4\alpha^2}{8}}$$
(Check at $\alpha = 0.7$: both sides $= 0.98870$.)

@s 8
**Gamma function:** $\Gamma(n) = \displaystyle\int_0^\infty e^{-x}x^{n-1}dx$, $n>0$. **Beta function:** $B(m,n) = \displaystyle\int_0^1x^{m-1}(1-x)^{n-1}dx$, $m,n>0$. They are related by $B(m,n) = \dfrac{\Gamma(m)\Gamma(n)}{\Gamma(m+n)}$, and $B(m,n) = 2\displaystyle\int_0^{\pi/2}\sin^{2m-1}\theta\cos^{2n-1}\theta\,d\theta$.

Put $x = 2a\sin^2\theta$: $dx = 4a\sin\theta\cos\theta\,d\theta$, $\sqrt{2ax - x^2} = 2a\sin\theta\cos\theta$.
$$I = \int_0^{\pi/2}(2a)^5\sin^{10}\theta\cdot2a\sin\theta\cos\theta\cdot4a\sin\theta\cos\theta\,d\theta = 256a^7\int_0^{\pi/2}\sin^{12}\theta\cos^2\theta\,d\theta = 128a^7B\!\left(\tfrac{13}2,\tfrac32\right)$$
$$I = 128a^7\frac{\Gamma(13/2)\Gamma(3/2)}{\Gamma(8)} = 128a^7\cdot\frac{\frac{10395}{64}\sqrt\pi\cdot\frac{\sqrt\pi}2}{5040} = \boxed{\frac{33\pi a^7}{16}}$$

@s 9
The curve $y^2 = \dfrac{x^3}{a-x}$ is the **cissoid** of Diocles. It is symmetric about the x-axis, passes through the origin (a cusp) and is defined for $0\le x<a$. As $x\to a^-$, $y\to\pm\infty$, so $x = a$ is its asymptote. The required area lies between the curve and $x = a$:
$$A = 2\int_0^a\frac{x^{3/2}}{\sqrt{a-x}}\,dx$$
Put $x = a\sin^2\theta$, $dx = 2a\sin\theta\cos\theta\,d\theta$, $\sqrt{a-x} = \sqrt a\cos\theta$:
$$A = 2\int_0^{\pi/2}\frac{a^{3/2}\sin^3\theta}{\sqrt a\cos\theta}\cdot2a\sin\theta\cos\theta\,d\theta = 4a^2\int_0^{\pi/2}\sin^4\theta\,d\theta = 4a^2\cdot\frac{3\pi}{16}$$
$$\boxed{A = \frac{3\pi a^2}{4}}$$

```figure caption="Question 9: the cissoid y²(a - x) = x³ (a = 1) and its asymptote x = a; the shaded region has area 3πa²/4."
a=1.0
x=np.linspace(0,0.985,600); y=np.sqrt(x**3/(a-x))
fig,ax=plt.subplots(figsize=(3.8,3.4))
ax.plot(x,y,color='#1d6fb8'); ax.plot(x,-y,color='#1d6fb8')
ax.fill_between(x,-y,y,color='#1d6fb8',alpha=0.1)
ax.axvline(a,color='#d9534f',ls='--',lw=1.2); ax.text(a+0.03,2.6,'asymptote\n$x=a$',color='#d9534f',fontsize=8)
ax.axhline(0,color='#aab0ba',lw=0.8); ax.text(0.3,0.0,'$A=3\\pi a^2/4$',fontsize=8)
ax.set_xlim(-0.2,1.7); ax.set_ylim(-4,4)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 10
Divide by $\cos^2y$: $\sec^2y\,\dfrac{dy}{dx} + 2x\tan y = x^3$. Put $v = \tan y$:
$$\begin{gathered}\frac{dv}{dx} + 2xv = x^3 \\ \text{IF} = e^{x^2} \\ ve^{x^2} = \int x^3e^{x^2}dx = \frac12(x^2-1)e^{x^2} + C\end{gathered}$$
$$\boxed{\tan y = \frac{x^2-1}{2} + Ce^{-x^2}}$$

@s 11
The equation $y = px + \dfrac ap$ is of Clairaut's form $y = px + f(p)$ with $f(p) = \dfrac ap$. Replacing $p$ by a constant $c$:
$$\boxed{y = cx + \frac ac}\quad\text{(general solution)}$$
**Singular solution.** $x + f'(p) = 0$ gives $x - \dfrac{a}{p^2} = 0$, so $p^2 = \dfrac ax$, $p = \sqrt{a/x}$. Then $y = px + \dfrac ap = \sqrt{ax} + \sqrt{ax} = 2\sqrt{ax}$. Squaring,
$$\boxed{y^2 = 4ax}$$
(the envelope of the family of lines: a parabola; the line $y = cx + a/c$ is tangent to it).

@s 12
Auxiliary equation $(m+2)^2 = 0$: $y_c = (c_1 + c_2x)e^{-2x}$.

Particular integral for $x^2$:
$$\frac{1}{(D+2)^2}x^2 = \frac14\left(1+\frac D2\right)^{-2}x^2 = \frac14\left(1 - D + \frac34D^2\right)x^2 = \frac14\left(x^2 - 2x + \frac32\right)$$
For $e^{2x}$: replace $D$ by $2$: $\dfrac{e^{2x}}{(2+2)^2} = \dfrac{e^{2x}}{16}$.
$$\boxed{y = (c_1 + c_2x)e^{-2x} + \frac{x^2}{4} - \frac x2 + \frac38 + \frac{e^{2x}}{16}}$$

@s 13
Cauchy–Euler equation. Put $z = \log x$: $x^2D^2 = D_z(D_z - 1)$ and $xD = D_z$:
$$\big[D_z(D_z-1) + D_z - 4\big]y = e^{2z}\;\Longrightarrow\;(D_z^2 - 4)\,y = e^{2z}$$
$y_c = c_1e^{2z} + c_2e^{-2z} = c_1x^2 + c_2x^{-2}$. Since $e^{2z}$ solves the homogeneous equation (case of failure),
$$y_p = \frac{z\,e^{2z}}{2D_z}\Big|_{D_z=2} = \frac{ze^{2z}}{4} = \frac{x^2\log x}{4}$$
$$\boxed{y = c_1x^2 + \frac{c_2}{x^2} + \frac{x^2}{4}\log x}$$

@s 14
The given equation is $7x^2 + 4xy + 4y^2 = 0$ ($a = 7$, $2h = 4$, $b = 4$), a homogeneous second-degree equation representing a pair of lines through the origin (here $h^2 - ab = 4 - 28<0$, so the lines are imaginary, a conjugate pair meeting in the real point $O$). The equation of the bisectors of the angles between them is
$$\frac{x^2 - y^2}{a - b} = \frac{xy}{h}\;\Longrightarrow\;\frac{x^2-y^2}{3} = \frac{xy}{2}\;\Longrightarrow\;2x^2 - 3xy - 2y^2 = 0 = (2x + y)(x - 2y)$$
Taking these two lines as the new axes means rotating the axes through $\theta$ with $\tan2\theta = \dfrac{2h}{a-b} = \dfrac43$, i.e. $\tan\theta = \dfrac12$, $\cos\theta = \dfrac2{\sqrt5}$, $\sin\theta = \dfrac1{\sqrt5}$ (new X-axis along $x - 2y = 0$). Substitute $x = X\cos\theta - Y\sin\theta = \dfrac{2X - Y}{\sqrt5}$ and $y = X\sin\theta + Y\cos\theta = \dfrac{X + 2Y}{\sqrt5}$:
$$7x^2 + 4xy + 4y^2 = \frac15\big[7(2X-Y)^2 + 4(2X-Y)(X+2Y) + 4(X+2Y)^2\big] = \frac15\big[40X^2 + 15Y^2\big]$$
$$\boxed{8X^2 + 3Y^2 = 0}$$
(The coefficients $8$ and $3$ are the eigenvalues of $\begin{pmatrix}7&2\\2&4\end{pmatrix}$, and the $XY$ term has vanished, as it must for the bisectors as axes. The new equation is a conjugate imaginary pair $Y = \pm i\sqrt{8/3}\,X$.)

@s 15
**Definition.** A hyperbola is the locus of a point $P$ whose distance from a fixed point $S$ (the focus) bears a constant ratio $e>1$ to its distance from a fixed line (the directrix); equivalently, $|PS - PS'| = 2a$ for the two foci $S, S'$, with $2a<SS'$.

**Derivation (focus–directrix).** Take the origin at the midpoint of the two vertices, the x-axis through the focus, so that $S = (ae, 0)$ and the directrix is $x = \dfrac ae$ (the vertices $A(a,0)$, $A'(-a,0)$ divide $SZ$ internally and externally in the ratio $e:1$). For $P(x,y)$ with foot of perpendicular $M$ on the directrix, $SP = e\,PM$:
$$(x - ae)^2 + y^2 = e^2\left(x - \frac ae\right)^2 = (ex - a)^2$$
$$x^2 - 2aex + a^2e^2 + y^2 = e^2x^2 - 2aex + a^2\;\Longrightarrow\;(e^2-1)x^2 - y^2 = a^2(e^2-1)$$
Put $b^2 = a^2(e^2 - 1)>0$ and divide by $a^2(e^2-1)$:
$$\boxed{\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1,\qquad b^2 = a^2(e^2-1)}$$
**Properties.** Centre $O$; vertices $(\pm a,0)$; foci $(\pm ae,0)$; directrices $x = \pm\dfrac ae$; transverse axis $2a$, conjugate axis $2b$; asymptotes $y = \pm\dfrac bax$; latus rectum $\dfrac{2b^2}{a}$.

```figure caption="Question 15: hyperbola x²/a² - y²/b² = 1 with foci S, S′, directrices x = ±a/e and asymptotes y = ±(b/a)x."
a,b=1.5,1.0; c=np.sqrt(a*a+b*b); e=c/a
t=np.linspace(-1.7,1.7,300)
fig,ax=plt.subplots(figsize=(5.2,3.2))
for s in (1,-1): ax.plot(s*a*np.cosh(t),b*np.sinh(t),color='#1d6fb8')
xl=np.array([-4,4]); ax.plot(xl,b/a*xl,color='#d9534f',ls='--',lw=0.9); ax.plot(xl,-b/a*xl,color='#d9534f',ls='--',lw=0.9)
for s in (1,-1): ax.axvline(s*a/e,color='#b8860b',ls=':',lw=1.1)
for px in (c,-c): ax.plot([px],[0],'o',color='#14181f',ms=3.5)
ax.text(c+0.05,-0.3,'$S(ae,0)$',fontsize=8); ax.text(-c-0.05,-0.3,"$S'$",fontsize=8,ha='right')
ax.text(a/e+0.05,2.0,'$x=a/e$',color='#b8860b',fontsize=8)
ax.text(3.1,2.3,'$y=\\frac{b}{a}x$',color='#d9534f',fontsize=8)
ax.axhline(0,color='#aab0ba',lw=0.8); ax.axvline(0,color='#aab0ba',lw=0.8)
ax.set_xlim(-4,4); ax.set_ylim(-2.6,2.6)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

@s 16
Write $r = \dfrac{12}{3 + \cos\theta} = \dfrac{4}{1 + \tfrac13\cos\theta}$. Compared with $\dfrac\ell r = 1 + e\cos\theta$: $\ell = 4$ and $e = \dfrac13<1$, so the curve is an **ellipse** with a focus at the pole.

| Feature | Value |
|---|---|
| Directrix | $x = \ell/e = 12$ |
| Vertices ($\theta = 0,\pi$) | $r = 3$ and $r = 6$: $(3, 0)$ and $(-6, 0)$ |
| Major axis | $2a = 9$, $a = 4.5$ |
| Centre | $(-1.5, 0)$ |
| Foci | $(0,0)$ and $(-3,0)$ ($c = ae = 1.5$) |
| Semi-minor axis | $b = \sqrt{a^2-c^2} = \sqrt{18} = 3\sqrt2\approx4.24$ ($b^2 = a\ell$) |
| Latus rectum ends | $(0,\pm4)$ |

Cartesian form: $3r + x = 12\Rightarrow9(x^2+y^2) = (12-x)^2\Rightarrow8x^2 + 9y^2 + 24x - 144 = 0$, i.e. $\dfrac{(x+1.5)^2}{20.25} + \dfrac{y^2}{18} = 1$. $\checkmark$

```figure caption="Question 16: r = 12/(3 + cos θ), an ellipse with e = 1/3, focus at the pole, directrix x = 12."
th=np.linspace(0,2*np.pi,500); r=12/(3+np.cos(th))
fig,ax=plt.subplots(figsize=(5.6,2.9))
ax.plot(r*np.cos(th),r*np.sin(th),color='#1d6fb8')
ax.axvline(12,color='#b8860b',ls='--',lw=1.1); ax.text(12.2,3.2,'directrix\n$x=12$',color='#b8860b',fontsize=8)
ax.axhline(0,color='#aab0ba',lw=0.8); ax.axvline(0,color='#aab0ba',lw=0.8)
for p,l,dx,dy in [((0,0),'$F_1$',0.25,-0.9),((-3,0),'$F_2$',-0.5,-0.9),((3,0),'(3,0)',0.2,0.4),((-6,0),'(-6,0)',-1.2,0.5),((0,4),'(0,4)',0.3,0.1),((0,-4),'(0,-4)',0.3,-0.6)]:
    ax.plot([p[0]],[p[1]],'o',color='#14181f',ms=3.5); ax.text(p[0]+dx,p[1]+dy,l,fontsize=8)
ax.set_aspect('equal'); ax.set_xlim(-8,16); ax.set_ylim(-5.5,5.5)
for s in ('top','right'): ax.spines[s].set_visible(False)
```

**OR.** For $2x^2 + 3y^2 - 4x - 12y + 13 = 0$ we have $a = 2$, $h = 0$, $b = 3$, so $h^2 - ab = -6<0$ (elliptic type). Complete the squares:
$$2(x^2 - 2x) + 3(y^2 - 4y) + 13 = 0\Longrightarrow2(x-1)^2 + 3(y-2)^2 = 2 + 12 - 13 = 1$$
$$\frac{(x-1)^2}{1/2} + \frac{(y-2)^2}{1/3} = 1$$
This is of the form $\dfrac{X^2}{A^2} + \dfrac{Y^2}{B^2} = 1$ with the positive right-hand side, so it represents an **ellipse**, with $A^2 = \dfrac12$ and $B^2 = \dfrac13$. $\blacksquare$

| Quantity | Value |
|---|---|
| Centre | $\boxed{(1,2)}$ |
| Semi-axes | $A = \dfrac1{\sqrt2}\approx0.707$ (along $x$), $B = \dfrac1{\sqrt3}\approx0.577$ (along $y$) |
| Major axis | $2A = \sqrt2\approx1.414$ |
| Minor axis | $2B = \dfrac2{\sqrt3}\approx1.155$ |
| Eccentricity | $e = \sqrt{1 - \dfrac{B^2}{A^2}} = \sqrt{1 - \dfrac23} = \dfrac{1}{\sqrt3}\approx0.577$ |
| Foci | $\left(1\pm\dfrac1{\sqrt6},\,2\right)$ |

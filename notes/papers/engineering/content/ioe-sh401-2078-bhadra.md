---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH401-2078-Bhadra.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 401
year_bs: 2078 Bhadra
cal: BS
year_ad: 2021
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (old course, SH 401). Pass marks 32. Every question carries 5 marks.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
If $y = (x^2 - 1)^n$, then prove that $(x^2 - 1)y_{n+2} + 2xy_{n+1} - n(n+1)y_n = 0$. [[5]]

@q 2
Assuming the validity of expansion, expand $\log(1 + x)$ by using Maclaurin's theorem. [[5]]

@q 3
Give an example of indeterminate form. Evaluate: $\displaystyle\lim_{x\to0}(\cot x)^{1/\log x}$. [[5]]

@q 4
Find the asymptote of the curve: $(x^2 - y^2)^2 - 2(x^2 + y^2) + x - 1 = 0$. [[5]]

@q 5
Find the radius of curvature for the curve $r^m = a^m\cos m\theta$.

**OR**

Find the pedal equation of the following curve $y^2 = 4a(x + a)$. [[5]]

@q 6
Evaluate: $\displaystyle\int_0^1\frac{\log(1+x)}{1 + x^2}\,dx$. [[5]]

@q 7
Evaluate by using the rule of differentiation under the sign of integration: $\displaystyle\int_0^\infty\frac{\log(1 + a^2x^2)}{1 + b^2x^2}\,dx$. [[5]]

@q 8
Define Gamma function. Use it to prove: $\displaystyle\int_0^{\pi/8}\cos^34x\,dx = \frac16$. [[5]]

@q 9
Find the area of a loop of the curve: $a^2y^2 = a^2x^2 - x^4$.

**OR**

Prove that the volume and surface area of a sphere of radius $a$ is $\dfrac43\pi a^3$ and $4\pi a^2$ respectively. [[5]]

@q 10
Solve: $\dfrac{dy}{dx} + \dfrac yx\log y = \dfrac{y}{x^2}(\log y)^2$. [[5]]

@q 11
Find the general solution of the differential equation $y = (1 + p)x + ap^2$. [[5]]

@q 12
Solve: $(D^2 + 3D + 2)y = e^{2x}\sin x$. [[5]]

@q 13
Solve: $(x^2D^2 - 2)y = x^2 + \dfrac1x$.

**OR**

A certain culture of bacteria grows at rate proportional to its size. If the size doubles in 4 days, find the time required for the culture to increase to 10 times its original size. [[5]]

@q 14
Through what angle must the axes be rotated to remove the term containing $xy$ in $11x^2 + 4xy + 14y^2 = 5$. [[5]]

@q 15
Prove that: $2x^2 + 3y^2 - 4x - 12y + 13 = 0$ represents equation of ellipse. Find its centre, length of axes, eccentricity, and directrices of ellipse. [[5]]

@q 16
Show that the line $x\cos\alpha + y\sin\alpha = p$ will be a tangent to the hyperbola $\dfrac{x^2}{a^2} - \dfrac{y^2}{b^2} = 1$ if $a^2\cos^2\alpha - b^2\sin^2\alpha = p^2$. [[5]]
<!-- SOLUTIONS -->

@s 1
Given $y = (x^2 - 1)^n$, so $y_1 = 2nx(x^2-1)^{n-1}$ and therefore

$$\begin{gathered}(x^2 - 1)y_1 = 2nxy \\ (1)\end{gathered}$$

Differentiate (1) $(n+1)$ times with Leibnitz's theorem $(uv)_k = \sum{}^kC_ru_{k-r}v_r$:

- Left side, $u = y_1$, $v = x^2-1$: $(x^2-1)y_{n+2} + (n+1)(2x)y_{n+1} + \dfrac{(n+1)n}{2}(2)y_n$
- Right side, $2n\cdot\dfrac{d^{n+1}}{dx^{n+1}}(xy)$ with $u = y$, $v = x$: $2n\big[xy_{n+1} + (n+1)y_n\big]$

Hence

$$(x^2-1)y_{n+2} + 2(n+1)xy_{n+1} + n(n+1)y_n = 2nxy_{n+1} + 2n(n+1)y_n$$

$$(x^2-1)y_{n+2} + \big[2(n+1) - 2n\big]xy_{n+1} + \big[n(n+1) - 2n(n+1)\big]y_n = 0$$

$$\begin{gathered}\boxed{(x^2-1)y_{n+2} + 2xy_{n+1} - n(n+1)y_n = 0} \\ \blacksquare\end{gathered}$$

@s 2
**Maclaurin's theorem.** If $f$ can be expanded in a power series about $0$,

$$f(x) = f(0) + xf'(0) + \frac{x^2}{2!}f''(0) + \cdots + \frac{x^n}{n!}f^{(n)}(0) + \cdots$$

Let $f(x) = \log(1+x)$. Successive derivatives:

$$\begin{gathered}f' = \frac{1}{1+x},\quad f'' = -\frac{1}{(1+x)^2},\quad f''' = \frac{2}{(1+x)^3},\quad f^{(4)} = -\frac{6}{(1+x)^4},\ \ldots,\quad f^{(n)} = \frac{(-1)^{n-1}(n-1)!}{(1+x)^n}\end{gathered}$$

At $x = 0$: $f(0) = 0$, $f'(0) = 1$, $f''(0) = -1$, $f'''(0) = 2$, $f^{(4)}(0) = -6$, $f^{(n)}(0) = (-1)^{n-1}(n-1)!$. Therefore

$$\begin{gathered}\boxed{\log(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \cdots + (-1)^{n-1}\frac{x^n}{n} + \cdots} \\ (-1 < x\le1)\end{gathered}$$

@s 3
**Example of an indeterminate form.** $\displaystyle\lim_{x\to0}\frac{\sin x}{x}$ is of the form $\dfrac00$ (value $1$); other forms are $\dfrac\infty\infty$, $0\cdot\infty$, $\infty - \infty$, $0^0$, $1^\infty$, $\infty^0$ (the given limit is of the type $\infty^0$ as $x\to0^+$, since $\cot x\to\infty$ and $\dfrac1{\log x}\to0$).

**Limit.** For $x\to0^+$ let $L = (\cot x)^{1/\log x}$:

$$\log L = \frac{\log\cot x}{\log x}\quad\left(\frac\infty\infty\right)$$

By L'Hospital's rule:

$$\begin{gathered}\lim_{x\to0^+}\frac{\dfrac{-\operatorname{cosec}^2x}{\cot x}}{\dfrac1x} = \lim_{x\to0^+}\frac{-x}{\sin x\cos x} = -1\cdot\frac{1}{1} = -1\end{gathered}$$

$$\begin{gathered}\boxed{\lim_{x\to0^+}(\cot x)^{1/\log x} = e^{-1} = \frac1e}\end{gathered}$$

@s 4
The curve is of degree $4$: $\phi_4 = (x^2 - y^2)^2$, $\phi_3 = 0$, $\phi_2 = -2(x^2+y^2)$, $\phi_1 = x$, $\phi_0 = -1$.

No asymptote is parallel to an axis (the coefficients of $x^4$ and $y^4$ are $1$). For the oblique ones put $x = 1$, $y = m$:

$$\begin{gathered}\phi_4(m) = (1 - m^2)^2 = 0\ \Longrightarrow\ m = 1\ (\text{double}),\ m = -1\ (\text{double})\end{gathered}$$

For a double root the constant $c$ in $y = mx + c$ satisfies

$$\frac{c^2}{2!}\phi_4''(m) + c\,\phi_3'(m) + \phi_2(m) = 0$$

$\phi_4' = -4m(1 - m^2)$, $\phi_4'' = -4 + 12m^2$, which equals $8$ at $m = \pm1$; $\phi_3' = 0$; $\phi_2(1,m) = -2(1 + m^2) = -4$ at $m = \pm1$:

$$\begin{gathered}4c^2 - 4 = 0\ \Longrightarrow\ c = \pm1\end{gathered}$$

Hence for $m = 1$: $y = x \pm 1$, and for $m = -1$: $y = -x \pm 1$.

$$\begin{gathered}\boxed{y = x + 1,\quad y = x - 1,\quad y = -x + 1,\quad y = -x - 1}\end{gathered}$$

(each of these four lines was substituted into the curve with sympy; the $x^4$, $x^3$ and $x^2$ coefficients all vanish.)

```figure caption="Question 4: the curve (x^2 - y^2)^2 = 2(x^2 + y^2) - x + 1 and its four asymptotes y = +-x +-1."
X,Y=np.meshgrid(np.linspace(-5,5,900),np.linspace(-5,5,900))
Z=(X**2-Y**2)**2-2*(X**2+Y**2)+X-1
fig,ax=plt.subplots(figsize=(3.8,3.8))
ax.contour(X,Y,Z,[0],colors='#1d6fb8',linewidths=1.6)
xs=np.array([-5,5])
for m in (1,-1):
    for c in (1,-1): ax.plot(xs,m*xs+c,'--',color='#d9534f',lw=.8)
ax.axhline(0,color='#14181f',lw=.5); ax.axvline(0,color='#14181f',lw=.5)
ax.set_xlim(-5,5); ax.set_ylim(-5,5); ax.set_aspect('equal'); ax.axis('off')
```

@s 5
**Main question (radius of curvature of $r^m = a^m\cos m\theta$).** First the pedal equation: taking logs and differentiating, $\dfrac1r\dfrac{dr}{d\theta} = -\tan m\theta = \cot\left(\dfrac\pi2 + m\theta\right)$, so the angle $\phi$ between the radius vector and the tangent is $\phi = \dfrac\pi2 + m\theta$ and

$$\begin{gathered}p = r\sin\phi = r\cos m\theta = \frac{r^{m+1}}{a^m}\end{gathered}$$

For a curve with pedal equation $p = f(r)$ the radius of curvature is $\rho = r\dfrac{dr}{dp}$. Here $\dfrac{dp}{dr} = \dfrac{(m+1)r^m}{a^m}$, so

$$\rho = r\cdot\frac{a^m}{(m+1)r^m}$$

$$\boxed{\rho = \frac{a^m}{(m+1)\,r^{m-1}}}$$

(For $m = 1$, the circle $r = a\cos\theta$, $\rho = a/2$, as it should.)

**OR (pedal equation of $y^2 = 4a(x + a)$).** This is a parabola with its vertex at $(-a, 0)$ and focus at the origin; the pedal is taken from the origin. At a point $(x_1, y_1)$ the tangent is

$$\begin{gathered}yy_1 = 2a(x + x_1) + 4a^2\quad\text{i.e.}\quad 2ax - y_1y + 2ax_1 + 4a^2 = 0\end{gathered}$$

(check: $y_1^2 = 4ax_1 + 4a^2$ ✓.). The perpendicular distance from the origin:

$$\begin{gathered}p = \frac{2a(x_1 + 2a)}{\sqrt{4a^2 + y_1^2}} = \frac{2a(x_1 + 2a)}{\sqrt{4a(x_1 + 2a)}}\quad\Longrightarrow\quad p^2 = a(x_1 + 2a)\end{gathered}$$

Also $r^2 = x_1^2 + y_1^2 = x_1^2 + 4ax_1 + 4a^2 = (x_1 + 2a)^2$, so $r = x_1 + 2a$. Therefore

$$\boxed{p^2 = ar}$$

@s 6
Put $x = \tan\theta$, $dx = \sec^2\theta\,d\theta$; $x:0\to1\Rightarrow\theta:0\to\frac\pi4$, and $1 + x^2 = \sec^2\theta$:

$$I = \int_0^{\pi/4}\log(1 + \tan\theta)\,d\theta$$

Use $\displaystyle\int_0^af(\theta)d\theta = \int_0^af(a - \theta)d\theta$ with $a = \frac\pi4$, noting $1 + \tan\left(\dfrac\pi4 - \theta\right) = 1 + \dfrac{1 - \tan\theta}{1 + \tan\theta} = \dfrac{2}{1 + \tan\theta}$:

$$\begin{gathered}I = \int_0^{\pi/4}\log\frac{2}{1 + \tan\theta}\,d\theta = \frac\pi4\log2 - I\end{gathered}$$

$$\begin{gathered}\boxed{I = \frac\pi8\log2\approx0.2722}\end{gathered}$$

@s 7
Let $I(a) = \displaystyle\int_0^\infty\frac{\log(1 + a^2x^2)}{1 + b^2x^2}\,dx$ ($a, b>0$). Differentiate with respect to $a$ (limits are constants):

$$\frac{dI}{da} = \int_0^\infty\frac{2ax^2}{(1 + a^2x^2)(1 + b^2x^2)}\,dx$$

Partial fractions: $\dfrac{x^2}{(1 + a^2x^2)(1 + b^2x^2)} = \dfrac{1}{b^2 - a^2}\left[\dfrac{1}{1 + a^2x^2} - \dfrac{1}{1 + b^2x^2}\right]$. Since $\displaystyle\int_0^\infty\frac{dx}{1 + k^2x^2} = \frac{\pi}{2k}$,

$$\begin{gathered}\frac{dI}{da} = \frac{2a}{b^2 - a^2}\cdot\frac\pi2\left(\frac1a - \frac1b\right) = \frac{\pi a}{b^2 - a^2}\cdot\frac{b - a}{ab} = \frac{\pi}{b(a + b)}\end{gathered}$$

Integrate with respect to $a$: $I = \dfrac\pi b\log(a + b) + C$. At $a = 0$, $I = 0$, so $C = -\dfrac\pi b\log b$:

$$\boxed{\int_0^\infty\frac{\log(1 + a^2x^2)}{1 + b^2x^2}\,dx = \frac\pi b\log\frac{a + b}{b}}$$

@s 8
**Gamma function.** For $n > 0$: $\Gamma(n) = \displaystyle\int_0^\infty e^{-x}x^{n-1}\,dx$, with $\Gamma(n+1) = n\Gamma(n)$, $\Gamma(1) = 1$, $\Gamma(\tfrac12) = \sqrt\pi$, and

$$\int_0^{\pi/2}\sin^p\theta\cos^q\theta\,d\theta = \frac{\Gamma\left(\frac{p+1}{2}\right)\Gamma\left(\frac{q+1}{2}\right)}{2\,\Gamma\left(\frac{p+q+2}{2}\right)}$$

**Proof of the result.** Put $u = 4x$, $dx = \dfrac14du$; $x:0\to\frac\pi8\Rightarrow u:0\to\frac\pi2$:

$$\begin{gathered}\int_0^{\pi/8}\cos^34x\,dx = \frac14\int_0^{\pi/2}\cos^3u\,du = \frac14\cdot\frac{\Gamma(\frac12)\Gamma(2)}{2\,\Gamma(\frac52)}\end{gathered}$$

With $\Gamma(\tfrac52) = \tfrac32\cdot\tfrac12\sqrt\pi = \tfrac34\sqrt\pi$ and $\Gamma(2) = 1$:

$$\begin{gathered}= \frac14\cdot\frac{\sqrt\pi}{2\cdot\frac34\sqrt\pi} = \frac14\cdot\frac23 = \frac16 \\ \blacksquare\end{gathered}$$

@s 9
**Main question.** The curve $a^2y^2 = x^2(a^2 - x^2)$ is symmetric about both axes; $y^2\ge0$ requires $|x|\le a$, so one loop lies in $-a\le x\le a$ (the curve is the "figure eight" of Gerono type with the origin as node).

```figure caption="Question 9: the curve a^2 y^2 = a^2 x^2 - x^4 (a = 1): two loops, the right one lies between x = 0 and x = a on both sides of the axis."
x=np.linspace(-1,1,400); y=x*np.sqrt(1-x**2)
fig,ax=plt.subplots(figsize=(4.4,2.4))
ax.fill_between(x[x>=0],-y[x>=0],y[x>=0],color='#dbe8f6',alpha=.9); ax.plot(x,y,color='#1d6fb8',lw=1.8); ax.plot(x,-y,color='#1d6fb8',lw=1.8)
ax.axhline(0,color='#14181f',lw=.6); ax.text(0.45,0,'one loop',fontsize=8,ha='center')
ax.set_xticks([-1,0,1]); ax.set_xticklabels(['-a','O','a']); ax.set_yticks([]); ax.set_aspect('equal'); ax.spines[['top','right','left']].set_visible(False)
```

The right-hand loop lies for $0\le x\le a$, symmetric about the $x$-axis, with $y = \pm\dfrac xa\sqrt{a^2 - x^2}$:

$$\begin{gathered}A = 2\int_0^a\frac xa\sqrt{a^2 - x^2}\,dx = \frac2a\left[-\frac13(a^2 - x^2)^{3/2}\right]_0^a = \frac2a\cdot\frac{a^3}{3}\end{gathered}$$

$$\boxed{A = \frac{2a^2}{3}\ \text{ for one loop }\ \ (\text{both loops: }\tfrac{4a^2}{3})}$$

Reading note: the two loops are mirror images, so each has area $\dfrac{2a^2}3$ and the full area enclosed is $\dfrac{4a^2}{3}$. Check with $\int_0^{a}x\sqrt{a^2 - x^2}dx = \dfrac{a^3}3$.

**OR (sphere).** Rotate the semicircle $y = \sqrt{a^2 - x^2}$, $-a\le x\le a$, about the $x$-axis.

*Volume:*

$$\begin{gathered}V = \pi\int_{-a}^ay^2\,dx = \pi\int_{-a}^a(a^2 - x^2)\,dx = 2\pi\left[a^2x - \frac{x^3}{3}\right]_0^a = 2\pi\left(a^3 - \frac{a^3}{3}\right) = \frac43\pi a^3\end{gathered}$$

*Surface area:* $\dfrac{dy}{dx} = \dfrac{-x}{\sqrt{a^2 - x^2}}$, $\sqrt{1 + y_1^2} = \dfrac{a}{\sqrt{a^2 - x^2}}$, so $y\sqrt{1 + y_1^2} = a$:

$$\begin{gathered}S = 2\pi\int_{-a}^ay\sqrt{1 + y_1^2}\,dx = 2\pi\int_{-a}^aa\,dx = 2\pi a(2a)\end{gathered}$$

$$\begin{gathered}\boxed{V = \frac43\pi a^3,\qquad S = 4\pi a^2} \\ \blacksquare\end{gathered}$$

@s 10
Put $v = \log y$, so $\dfrac{dv}{dx} = \dfrac1y\dfrac{dy}{dx}$. Dividing the equation by $y$:

$$\frac{dv}{dx} + \frac vx = \frac{v^2}{x^2}$$

This is Bernoulli's equation with $n = 2$. Divide by $v^2$ and put $w = \dfrac1v$, $\dfrac{dw}{dx} = -\dfrac{1}{v^2}\dfrac{dv}{dx}$:

$$\begin{gathered}-\frac{dw}{dx} + \frac wx = \frac1{x^2}\ \Longrightarrow\ \frac{dw}{dx} - \frac wx = -\frac1{x^2}\end{gathered}$$

Integrating factor $= e^{-\int dx/x} = \dfrac1x$:

$$\begin{gathered}\frac wx = -\int\frac{dx}{x^3} = \frac{1}{2x^2} + C\end{gathered}$$

$$\begin{gathered}w = \frac1{2x} + Cx\quad\Longrightarrow\quad\boxed{\frac{1}{\log y} = \frac{1}{2x} + Cx}\end{gathered}$$

@s 11
$y = (1 + p)x + ap^2$ is a Lagrange (d'Alembert) equation. Differentiate with respect to $x$, $\dfrac{dy}{dx} = p$:

$$\begin{gathered}p = (1 + p) + x\frac{dp}{dx} + 2ap\frac{dp}{dx}\ \Longrightarrow\ -1 = (x + 2ap)\frac{dp}{dx}\end{gathered}$$

Treat $x$ as a function of $p$: $\dfrac{dx}{dp} = -(x + 2ap)$, i.e.

$$\frac{dx}{dp} + x = -2ap$$

This is linear in $x$ with integrating factor $e^p$:

$$\begin{gathered}xe^p = -2a\int pe^p\,dp = -2a(p - 1)e^p + C\end{gathered}$$

$$x = 2a(1 - p) + Ce^{-p}$$

Substituting in the given equation,

$$\begin{gathered}y = (1+p)x + ap^2 = (1+p)\big[2a(1-p) + Ce^{-p}\big] + ap^2 = 2a(1 - p^2) + ap^2 + C(1+p)e^{-p}\end{gathered}$$

$$\begin{gathered}\boxed{x = 2a(1 - p) + Ce^{-p},\qquad y = a(2 - p^2) + C(1 + p)e^{-p}}\end{gathered}$$

which is the general solution in parametric form ($p$ is the parameter, $C$ the arbitrary constant). *Check:* $\dfrac{dy}{dp} = -2ap + C[e^{-p} - (1+p)e^{-p}] = -2ap - Cpe^{-p}$ and $p\dfrac{dx}{dp} = p(-2a - Ce^{-p}) = -2ap - Cpe^{-p}$ ✓ ($dy = p\,dx$).

@s 12
$(D^2 + 3D + 2)y = e^{2x}\sin x$.

**C.F.** $m^2 + 3m + 2 = 0\Rightarrow m = -1, -2$: $y_c = c_1e^{-x} + c_2e^{-2x}$.

**P.I.**

$$\begin{gathered}\frac{1}{D^2 + 3D + 2}e^{2x}\sin x = e^{2x}\frac{1}{(D+2)^2 + 3(D+2) + 2}\sin x = e^{2x}\frac{1}{D^2 + 7D + 12}\sin x\end{gathered}$$

$$\begin{gathered}= e^{2x}\frac{1}{7D + 11}\sin x = e^{2x}\frac{11 - 7D}{121 - 49D^2}\sin x = e^{2x}\frac{11\sin x - 7\cos x}{170}\end{gathered}$$

(using $D^2\to-1$, so the denominator is $121 + 49 = 170$.)

$$\boxed{y = c_1e^{-x} + c_2e^{-2x} + \frac{e^{2x}}{170}(11\sin x - 7\cos x)}$$

@s 13
**Main question.** $(x^2D^2 - 2)y = x^2 + \dfrac1x$ is a Cauchy-Euler equation. Put $x = e^z$, $D_1 = \dfrac d{dz}$:

$$\begin{gathered}\big[D_1(D_1 - 1) - 2\big]y = e^{2z} + e^{-z}\ \Longrightarrow\ (D_1 - 2)(D_1 + 1)y = e^{2z} + e^{-z}\end{gathered}$$

**C.F.** $m = 2, -1$: $y_c = c_1e^{2z} + c_2e^{-z} = c_1x^2 + \dfrac{c_2}{x}$.

**P.I.** Both terms are resonant with the C.F.; use $\dfrac1{f(D_1)}e^{az} = z\dfrac{1}{f'(a)}e^{az}$ when $f(a) = 0$, with $f'(D_1) = 2D_1 - 1$:

$$\begin{gathered}\frac{1}{f(D_1)}e^{2z} = \frac{ze^{2z}}{2(2) - 1} = \frac{ze^{2z}}{3} \\ \frac1{f(D_1)}e^{-z} = \frac{ze^{-z}}{2(-1) - 1} = -\frac{ze^{-z}}{3}\end{gathered}$$

Back to $x$ with $z = \log x$:

$$\boxed{y = c_1x^2 + \frac{c_2}{x} + \frac{x^2}{3}\log x - \frac{1}{3x}\log x}$$

(verified by substitution into the equation with sympy.)

**OR (bacteria).** Let $N(t)$ be the size; $\dfrac{dN}{dt} = kN$, so $N = N_0e^{kt}$. Doubling in $4$ days: $2N_0 = N_0e^{4k}\Rightarrow k = \dfrac{\ln2}{4} = 0.1733$ per day. For ten times, $10 = e^{kt}$:

$$\begin{gathered}t = \frac{\ln10}{k} = \frac{4\ln10}{\ln2} = 4\times3.3219\end{gathered}$$

$$\boxed{t\approx13.29\ \text{days}\ (\text{about 13 days 7 hours})}$$

```figure caption="Question 13 (OR): growth N/N0 = 2^(t/4); it reaches 10 at t = 13.29 days."
t=np.linspace(0,16,200)
fig,ax=plt.subplots(figsize=(4.2,2.4))
ax.plot(t,2**(t/4),color='#1d6fb8',lw=1.8); ax.axhline(10,color='#d9534f',lw=.8,ls='--'); ax.axvline(13.29,color='#d9534f',lw=.8,ls='--')
ax.plot([4,13.29],[2,10],'o',color='#14181f',ms=3); ax.text(4.2,2.3,'(4, 2)',fontsize=7); ax.text(10.2,10.6,'(13.29, 10)',fontsize=7)
ax.set_xlabel('t (days)',fontsize=8); ax.set_ylabel('N / N0',fontsize=8); ax.tick_params(labelsize=7); ax.spines[['top','right']].set_visible(False)
```

@s 14
For $ax^2 + 2hxy + by^2 = \ldots$ the $xy$ term is removed by rotating the axes through $\theta$ with

$$\begin{gathered}\tan2\theta = \frac{2h}{a - b} = \frac{4}{11 - 14} = -\frac43\end{gathered}$$

So $\cos2\theta = -\dfrac35$ (taking $2\theta$ in the second quadrant), giving $\tan^2\theta = \dfrac{1 - \cos2\theta}{1 + \cos2\theta} = \dfrac{8/5}{2/5} = 4$, i.e. $\tan\theta = 2$:

$$\begin{gathered}\boxed{\theta = \tan^{-1}2\approx63.43^\circ}\end{gathered}$$

(the other root, $\theta = \tan^{-1}\left(-\tfrac12\right) = -26.57^\circ$, differs by $90^\circ$ and works equally well).

*Check.* With $\tan\theta = 2$ ($\cos\theta = \tfrac1{\sqrt5}$, $\sin\theta = \tfrac2{\sqrt5}$) the transformed equation is $15X^2 + 10Y^2 = 5$, i.e. $3X^2 + 2Y^2 = 1$; the coefficients $15, 10$ are the eigenvalues of $\begin{pmatrix}11&2\\2&14\end{pmatrix}$ ($\lambda^2 - 25\lambda + 150 = 0$). For $\theta = -26.57^\circ$ the result is $10X^2 + 15Y^2 = 5$.

@s 15
Complete the squares:

$$\begin{gathered}2(x^2 - 2x) + 3(y^2 - 4y) + 13 = 0\ \Longrightarrow\ 2(x-1)^2 + 3(y-2)^2 = -13 + 2 + 12 = 1\end{gathered}$$

Put $X = x - 1$, $Y = y - 2$ (shift of origin to $(1, 2)$):

$$\begin{gathered}2X^2 + 3Y^2 = 1\ \Longrightarrow\ \frac{X^2}{1/2} + \frac{Y^2}{1/3} = 1\end{gathered}$$

This has the standard form $\dfrac{X^2}{a^2} + \dfrac{Y^2}{b^2} = 1$ with both $a^2 = \dfrac12$ and $b^2 = \dfrac13$ positive, so it **represents an ellipse**.

- **Centre:** $(1, 2)$.
- **Axes:** $a = \dfrac1{\sqrt2}>b = \dfrac1{\sqrt3}$, so the major axis (along $x$) has length $2a = \sqrt2\approx1.414$ and the minor axis $2b = \dfrac{2}{\sqrt3}\approx1.155$.
- **Eccentricity:** $e = \sqrt{1 - \dfrac{b^2}{a^2}} = \sqrt{1 - \dfrac23} = \dfrac{1}{\sqrt3}$.
- **Directrices:** $X = \pm\dfrac ae = \pm\dfrac{1}{\sqrt2}\cdot\sqrt3 = \pm\sqrt{\dfrac32}$, i.e.
$$\begin{gathered}\boxed{x = 1 \pm\sqrt{\tfrac32}\ \ (\approx2.225\ \text{and}\ -0.225)}\end{gathered}$$

```figure caption="Question 15: the ellipse 2(x-1)^2 + 3(y-2)^2 = 1 with centre (1, 2), foci and directrices x = 1 +- sqrt(3/2)."
a,b=1/np.sqrt(2),1/np.sqrt(3); e=1/np.sqrt(3); t=np.linspace(0,2*np.pi,300)
fig,ax=plt.subplots(figsize=(4.4,2.4))
ax.plot(1+a*np.cos(t),2+b*np.sin(t),color='#1d6fb8',lw=1.8)
for s in (1,-1): ax.axvline(1+s*a/e,color='#d9534f',lw=.9,ls=':')
ax.plot([1,1+a*e,1-a*e],[2,2,2],'o',color='#14181f',ms=3); ax.text(1.03,1.85,'C(1,2)',fontsize=7)
ax.set_ylim(1,3); ax.set_aspect('equal'); ax.tick_params(labelsize=7); ax.spines[['top','right']].set_visible(False)
```

@s 16
For the line $y = mx + c$ to touch $\dfrac{x^2}{a^2} - \dfrac{y^2}{b^2} = 1$ the condition is $c^2 = a^2m^2 - b^2$. *Proof:* substitute $y = mx + c$:

$$\begin{gathered}\frac{x^2}{a^2} - \frac{(mx+c)^2}{b^2} = 1\ \Longrightarrow\ (b^2 - a^2m^2)x^2 - 2a^2mc\,x - a^2(c^2 + b^2) = 0\end{gathered}$$

and equate the discriminant to zero: $4a^4m^2c^2 + 4a^2(b^2 - a^2m^2)(c^2 + b^2) = 0$, which simplifies to $c^2 = a^2m^2 - b^2$.

Write the given line as $y = -\cot\alpha\;x + \dfrac{p}{\sin\alpha}$, so $m = -\cot\alpha$, $c = \dfrac{p}{\sin\alpha}$. It is tangent when

$$\begin{gathered}\frac{p^2}{\sin^2\alpha} = a^2\cot^2\alpha - b^2\ \Longrightarrow\ p^2 = a^2\cos^2\alpha - b^2\sin^2\alpha\end{gathered}$$

$$\begin{gathered}\boxed{a^2\cos^2\alpha - b^2\sin^2\alpha = p^2} \\ \blacksquare\end{gathered}$$

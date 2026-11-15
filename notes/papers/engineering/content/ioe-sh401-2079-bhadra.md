---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH401-2079-Bhadra.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 401
year_bs: 2079 Bhadra
cal: BS
year_ad: 2022
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (old course, SH 401). Pass marks 32. All questions carry equal marks (5 each).
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
State Leibnitz's theorem. If $y = a\cos(\log x) + b\sin(\log x)$ then show that $x^2y_{n+2} + (2n+1)xy_{n+1} + (n^2+1)y_n = 0$. [[5]]

@q 2
Apply Maclaurin's series to find the expansion of $e^x\sec x$ as far as the term in $x^3$. [[5]]

@q 3
State L'Hospital's rule. Using it evaluate $\displaystyle\lim_{x\to0}\left(\frac{\sin x}{x}\right)^{1/x^2}$. [[5]]

@q 4
Find the asymptotes of the curve $(x+y)^2(x + 2y + 2) = x + 9y - 2$. [[5]]

@q 5
Show that for the ellipse $\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1$, the radius of curvature at the extremity of the major axis is equal to half of the latus rectum. [[5]]

@q 6
Integrate: $\displaystyle\int_0^{\pi/2}\frac{\cos x\,dx}{(1 + \sin x)(2 + \sin x)}$. [[5]]

@q 7
Apply the rule of differentiation under integral sign to evaluate $\displaystyle\int_0^\infty\frac{e^{-ax}\sin x}{x}\,dx$ and hence deduce that $\displaystyle\int_0^\infty\frac{\sin x}{x}\,dx = \frac\pi2$. [[5]]

@q 8
Define Beta and Gamma functions. Evaluate: $\displaystyle\int_0^a x^4\sqrt{a^2 - x^2}\,dx$. [[5]]

@q 9
Show that the area of the astroid $x^{2/3} + y^{2/3} = a^{2/3}$ is $\dfrac{3\pi a^2}{8}$.

**OR**

Find the volume of the solid of revolution of the cardioid $r = a(1 + \cos\theta)$ about the initial line. [[5]]

@q 10
Solve: $x\dfrac{dy}{dx} + 2y = x^2\log x$. [[5]]

@q 11
Solve: $y = yp^2 + 2px$ where $p = \dfrac{dy}{dx}$. [[5]]

@q 12
Solve: $\dfrac{d^2y}{dx^2} + 3\dfrac{dy}{dx} + 2y = e^{2x}\sin x$. [[5]]

@q 13
Solve: $x\dfrac{d^2y}{dx^2} - 2\dfrac{dy}{dx} + \dfrac{2y}{x} = \dfrac{1}{x^2}$. [[5]]

@q 14
Derive the standard equation of an ellipse. [[5]]

@q 15
Through what angle should the axes be rotated to reduce the equation $3x^2 + 2xy + 3y^2 - \sqrt2\,x = 0$ into one with the $xy$ term missing? [[5]]

@q 16
Find the centre, length of the axes and eccentricity of the conic $9x^2 + 4xy + 6y^2 - 22x - 16y + 9 = 0$.

**OR**

Describe and sketch the graph of the equation $r = \dfrac{10}{3 + 2\cos\theta}$. [[5]]
<!-- SOLUTIONS -->

@s 1
**Leibnitz's theorem.** If $u$ and $v$ have derivatives of every order up to $n$, then

$$\boxed{(uv)_n = u_nv + {}^nC_1u_{n-1}v_1 + {}^nC_2u_{n-2}v_2 + \cdots + uv_n}$$

**First relation.** With $y = a\cos(\log x) + b\sin(\log x)$:

$$\begin{gathered}y_1 = \frac{-a\sin(\log x) + b\cos(\log x)}{x}\ \Longrightarrow\ xy_1 = -a\sin(\log x) + b\cos(\log x)\end{gathered}$$

Differentiate again: $y_1 + xy_2 = \dfrac{-a\cos(\log x) - b\sin(\log x)}{x} = -\dfrac yx$. Multiply by $x$:

$$\begin{gathered}\boxed{x^2y_2 + xy_1 + y = 0} \\ (1)\end{gathered}$$

**$n$th derivative.** Differentiate (1) $n$ times with Leibnitz's theorem:

- $\dfrac{d^n}{dx^n}\big[x^2y_2\big] = x^2y_{n+2} + n(2x)y_{n+1} + \dfrac{n(n-1)}{2}(2)y_n$
- $\dfrac{d^n}{dx^n}\big[xy_1\big] = xy_{n+1} + ny_n$
- $\dfrac{d^n}{dx^n}\big[y\big] = y_n$

Adding:

$$x^2y_{n+2} + (2n+1)xy_{n+1} + \big[n(n-1) + n + 1\big]y_n = 0$$

$$\begin{gathered}\boxed{x^2y_{n+2} + (2n+1)xy_{n+1} + (n^2+1)y_n = 0} \\ \blacksquare\end{gathered}$$

@s 2
Use the known Maclaurin series (valid near $0$) and multiply. For $\sec x$: $\sec x = \dfrac1{\cos x}$ with $\cos x = 1 - \dfrac{x^2}2 + \dfrac{x^4}{24} - \cdots$, so

$$\sec x = 1 + \frac{x^2}{2} + \frac{5x^4}{24} + \cdots$$

(equivalently $f = \sec x$ has $f(0) = 1$, $f'(0) = 0$, $f''(0) = 1$, $f'''(0) = 0$ by Maclaurin's theorem). Then

$$e^x\sec x = \left(1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots\right)\left(1 + \frac{x^2}{2} + \cdots\right)$$

Collect powers of $x$:

- $x^0$: $1$
- $x^1$: $1$
- $x^2$: $\dfrac12 + \dfrac12 = 1$
- $x^3$: $\dfrac16 + \dfrac12 = \dfrac23$

$$\boxed{e^x\sec x = 1 + x + x^2 + \frac23x^3 + \cdots}$$

*Direct check by Maclaurin.* For $f = e^x\sec x$: $f(0) = 1$; $f' = e^x(\sec x + \sec x\tan x)$, $f'(0) = 1$; $f''(0) = 2$; $f'''(0) = 4$, giving $1 + x + \dfrac{2x^2}{2!} + \dfrac{4x^3}{3!}$, the same series.

@s 3
**L'Hospital's rule.** If $f(x)$ and $g(x)$ are differentiable near $a$, $f(x)\to0$ and $g(x)\to0$ (or both $\to\infty$) as $x\to a$, and $\displaystyle\lim\frac{f'(x)}{g'(x)}$ exists, then

$$\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)}$$

**Limit.** The form is $1^\infty$. Let $L = \left(\dfrac{\sin x}{x}\right)^{1/x^2}$; then $\log L = \dfrac{\log(\sin x/x)}{x^2}$, of the form $\dfrac00$.

$$\begin{gathered}\lim_{x\to0}\frac{\log\sin x - \log x}{x^2}\overset{\text{L'H}}{=}\lim_{x\to0}\frac{\cot x - \frac1x}{2x} = \lim_{x\to0}\frac{x\cos x - \sin x}{2x^2\sin x}\end{gathered}$$

Still $\dfrac00$; differentiate numerator and denominator once more:

$$\begin{gathered}\lim_{x\to0}\frac{\cos x - x\sin x - \cos x}{4x\sin x + 2x^2\cos x} = \lim_{x\to0}\frac{-x\sin x}{4x\sin x + 2x^2\cos x} = \lim_{x\to0}\frac{-\sin x}{4\sin x + 2x\cos x}\end{gathered}$$

and once more:

$$\lim_{x\to0}\frac{-\cos x}{4\cos x + 2\cos x - 2x\sin x} = \frac{-1}{6}$$

$$\boxed{\lim_{x\to0}\left(\frac{\sin x}{x}\right)^{1/x^2} = e^{-1/6}}$$

@s 4
Expand: $(x+y)^2(x+2y) + 2(x+y)^2 - (x + 9y) + 2 = 0$. So

$$\begin{gathered}\phi_3 = (x+y)^2(x+2y),\quad\phi_2 = 2(x+y)^2,\quad\phi_1 = -(x + 9y),\quad\phi_0 = 2\end{gathered}$$

There are no asymptotes parallel to the axes (coefficients of $x^3$ and $y^3$ in $\phi_3$ are $1$ and $2$). For the oblique ones put $x = 1$, $y = m$:

$$\begin{gathered}\phi_3(m) = (1+m)^2(1+2m) = 0\ \Longrightarrow\ m = -1\ (\text{double}),\quad m = -\tfrac12\end{gathered}$$

**Simple root $m = -\tfrac12$.** $\phi_3'(m) = 2(1+m)(1+2m) + 2(1+m)^2 = \tfrac12$ and $\phi_2(m) = 2(1+m)^2 = \tfrac12$:

$$\begin{gathered}c = -\frac{\phi_2(m)}{\phi_3'(m)} = -1\ \Longrightarrow\ y = -\tfrac12x - 1\ \Longrightarrow\ x + 2y + 2 = 0\end{gathered}$$

**Double root $m = -1$.** Here $c$ satisfies $\dfrac{c^2}{2!}\phi_3''(m) + c\,\phi_2'(m) + \phi_1(m) = 0$. Since $\phi_3 = (1+m)^2(1+2m)$, $\phi_3''(-1) = 2(1+2m)\big|_{m=-1} = -2$; also $\phi_2'(m) = 4(1+m) = 0$ and $\phi_1(m) = -(1 + 9m) = 8$:

$$\begin{gathered}-c^2 + 8 = 0\ \Longrightarrow\ c = \pm2\sqrt2 \\ y = -x \pm 2\sqrt2\end{gathered}$$

$$\begin{gathered}\boxed{x + 2y + 2 = 0,\qquad x + y = 2\sqrt2,\qquad x + y = -2\sqrt2}\end{gathered}$$

(verified by substituting each line into the curve with sympy.)

@s 5
**Radius of curvature.** Use the parametric form $x = a\cos t$, $y = b\sin t$:

$$\begin{gathered}x' = -a\sin t,\ y' = b\cos t,\ x'' = -a\cos t,\ y'' = -b\sin t\end{gathered}$$

$$\begin{gathered}\rho = \frac{(x'^2 + y'^2)^{3/2}}{x'y'' - y'x''} = \frac{(a^2\sin^2t + b^2\cos^2t)^{3/2}}{ab\sin^2t + ab\cos^2t} = \frac{(a^2\sin^2t + b^2\cos^2t)^{3/2}}{ab}\end{gathered}$$

**At the extremity of the major axis** (a vertex $(a, 0)$, i.e. $t = 0$; major axis assumed $a > b$):

$$\begin{gathered}\rho = \frac{(b^2)^{3/2}}{ab} = \frac{b^3}{ab} = \frac{b^2}{a}\end{gathered}$$

**Latus rectum.** The chord through a focus perpendicular to the major axis has length $\ell = \dfrac{2b^2}{a}$ (putting $x = ae$ in the ellipse gives $y = \pm\dfrac{b^2}{a}$). Hence

$$\begin{gathered}\boxed{\rho = \frac{b^2}{a} = \frac12\cdot\frac{2b^2}{a} = \frac12\,(\text{latus rectum})} \\ \blacksquare\end{gathered}$$

@s 6
Put $t = \sin x$, $dt = \cos x\,dx$; $x:0\to\frac\pi2\Rightarrow t:0\to1$:

$$I = \int_0^1\frac{dt}{(1+t)(2+t)}$$

Partial fractions: $\dfrac{1}{(1+t)(2+t)} = \dfrac{1}{1+t} - \dfrac{1}{2+t}$.

$$\begin{gathered}I = \Big[\log(1+t) - \log(2+t)\Big]_0^1 = \log\frac{1+t}{2+t}\Big|_0^1 = \log\frac23 - \log\frac12 = \log\frac43\end{gathered}$$

$$\begin{gathered}\boxed{I = \log\frac43\approx0.2877}\end{gathered}$$

@s 7
Let $I(a) = \displaystyle\int_0^\infty\frac{e^{-ax}\sin x}{x}\,dx$, $a > 0$. Differentiating under the integral sign:

$$\begin{gathered}\frac{dI}{da} = -\int_0^\infty e^{-ax}\sin x\,dx = -\frac{1}{a^2 + 1}\end{gathered}$$

using $\displaystyle\int_0^\infty e^{-ax}\sin bx\,dx = \dfrac{b}{a^2+b^2}$ with $b = 1$. Integrating,

$$I(a) = -\tan^{-1}a + C$$

As $a\to\infty$ the integrand $\to0$ (the integral is bounded by $\int e^{-ax}\,dx = 1/a$), so $I(\infty) = 0$:

$$\begin{gathered}0 = -\frac\pi2 + C\ \Longrightarrow\ C = \frac\pi2\end{gathered}$$

$$\begin{gathered}\boxed{\int_0^\infty\frac{e^{-ax}\sin x}{x}\,dx = \frac\pi2 - \tan^{-1}a = \cot^{-1}a}\end{gathered}$$

**Deduction.** Put $a = 0$: $\displaystyle\int_0^\infty\frac{\sin x}{x}\,dx = \frac\pi2 - 0 = \frac\pi2$. $\blacksquare$

@s 8
**Definitions.**

$$\begin{gathered}\Gamma(n) = \int_0^\infty e^{-x}x^{n-1}dx\ (n>0) \\ B(m,n) = \int_0^1x^{m-1}(1-x)^{n-1}dx\ (m,n>0)\end{gathered}$$

Related by $B(m,n) = \dfrac{\Gamma(m)\Gamma(n)}{\Gamma(m+n)}$; also $\Gamma(n+1) = n\Gamma(n)$ and $\Gamma(\tfrac12) = \sqrt\pi$. A useful form is $\displaystyle\int_0^{\pi/2}\sin^p\theta\cos^q\theta\,d\theta = \tfrac12B\left(\tfrac{p+1}2,\tfrac{q+1}2\right)$.

**Evaluation.** Put $x = a\sin\theta$, $dx = a\cos\theta\,d\theta$, $\sqrt{a^2 - x^2} = a\cos\theta$; $\theta:0\to\frac\pi2$:

$$\begin{gathered}I = \int_0^{\pi/2}a^4\sin^4\theta\cdot a\cos\theta\cdot a\cos\theta\,d\theta = a^6\int_0^{\pi/2}\sin^4\theta\cos^2\theta\,d\theta = \frac{a^6}{2}B\left(\frac52,\frac32\right)\end{gathered}$$

$$\begin{gathered}B\left(\tfrac52,\tfrac32\right) = \frac{\Gamma(\frac52)\Gamma(\frac32)}{\Gamma(4)} = \frac{\frac34\sqrt\pi\cdot\frac12\sqrt\pi}{6} = \frac{3\pi/8}{6} = \frac{\pi}{16}\end{gathered}$$

$$\begin{gathered}\boxed{I = \frac{a^6}{2}\cdot\frac\pi{16} = \frac{\pi a^6}{32}}\end{gathered}$$

@s 9
**Main question (area of the astroid).** *Reading note:* the scan prints $x^{2/3} - y^{2/3} = a^{2/3}$, a misprint of the astroid $x^{2/3} + y^{2/3} = a^{2/3}$ (the claimed area $3\pi a^2/8$ belongs only to this curve).

```figure caption="Question 9: the astroid x^(2/3) + y^(2/3) = a^(2/3) (a = 1). The area is four times the first-quadrant part."
t=np.linspace(0,2*np.pi,400)
fig,ax=plt.subplots(figsize=(3.4,3.4))
ax.fill(np.cos(t)**3,np.sin(t)**3,color='#dbe8f6',alpha=.8); ax.plot(np.cos(t)**3,np.sin(t)**3,color='#1d6fb8',lw=1.8)
ax.axhline(0,color='#14181f',lw=.6); ax.axvline(0,color='#14181f',lw=.6)
ax.text(1.03,0.03,'a',fontsize=8); ax.text(0.03,1.03,'a',fontsize=8)
ax.set_aspect('equal'); ax.axis('off')
```

Parametrise $x = a\cos^3t$, $y = a\sin^3t$, $dx = -3a\cos^2t\sin t\,dt$. By symmetry,

$$\begin{gathered}A = 4\int_{x=0}^{a}y\,dx = 4\int_{t=\pi/2}^{0}a\sin^3t\,(-3a\cos^2t\sin t)\,dt = 12a^2\int_0^{\pi/2}\sin^4t\cos^2t\,dt\end{gathered}$$

$$\begin{gathered}\int_0^{\pi/2}\sin^4t\cos^2t\,dt = \frac12B\left(\tfrac52,\tfrac32\right) = \frac{\pi}{32}\end{gathered}$$

$$\begin{gathered}\boxed{A = 12a^2\cdot\frac{\pi}{32} = \frac{3\pi a^2}{8}} \\ \blacksquare\end{gathered}$$

**OR (volume of the cardioid $r = a(1+\cos\theta)$ about the initial line).** The upper half $0\le\theta\le\pi$ generates the solid, and $V = \dfrac{2\pi}{3}\displaystyle\int r^3\sin\theta\,d\theta$:

$$\begin{gathered}V = \frac{2\pi a^3}{3}\int_0^\pi(1+\cos\theta)^3\sin\theta\,d\theta = \frac{2\pi a^3}{3}\int_0^2u^3\,du\quad(u = 1 + \cos\theta)\end{gathered}$$

$$\begin{gathered}\boxed{V = \frac{2\pi a^3}{3}\cdot4 = \frac{8\pi a^3}{3}}\end{gathered}$$

@s 10
Divide by $x$: $\dfrac{dy}{dx} + \dfrac2x\,y = x\log x$ (linear). The integrating factor is $e^{\int2/x\,dx} = x^2$:

$$\frac{d}{dx}\big(x^2y\big) = x^3\log x$$

Integrate by parts, $\displaystyle\int x^3\log x\,dx = \frac{x^4}{4}\log x - \int\frac{x^4}{4}\cdot\frac1x\,dx = \frac{x^4}{4}\log x - \frac{x^4}{16}$:

$$x^2y = \frac{x^4}{4}\log x - \frac{x^4}{16} + C$$

$$\boxed{y = \frac{x^2}{4}\log x - \frac{x^2}{16} + \frac{C}{x^2}}$$

@s 11
The equation $y = yp^2 + 2px$ is solvable for $x$:

$$\begin{gathered}x = \frac{y(1 - p^2)}{2p} = y\left(\frac{1}{2p} - \frac p2\right)\end{gathered}$$

Differentiate with respect to $y$, using $\dfrac{dx}{dy} = \dfrac1p$:

$$\frac1p = \left(\frac1{2p} - \frac p2\right) - y\left(\frac{1}{2p^2} + \frac12\right)\frac{dp}{dy}$$

Bring the first bracket to the left: $\dfrac1p - \dfrac1{2p} + \dfrac p2 = \dfrac{1 + p^2}{2p}$, so

$$\begin{gathered}\frac{1 + p^2}{2p} = -y\,\frac{1 + p^2}{2p^2}\,\frac{dp}{dy}\ \Longrightarrow\ p = -y\frac{dp}{dy}\ \Longrightarrow\ \frac{dp}{p} = -\frac{dy}{y}\end{gathered}$$

Integrating, $\log p = -\log y + \log c$, so $py = c$, i.e. $p = \dfrac cy$.

Substitute $p = c/y$ in the equation:

$$\begin{gathered}y = y\frac{c^2}{y^2} + \frac{2cx}{y}\ \Longrightarrow\ y^2 = c^2 + 2cx\end{gathered}$$

$$\boxed{y^2 = 2cx + c^2}$$

a family of parabolas with common focus at the origin. As a check, $2yy' = 2c$ gives $p = c/y$, and $y = y\cdot\dfrac{c^2}{y^2} + 2\dfrac cyx$ reproduces $y^2 = c^2 + 2cx$. Eliminating $c$ from $y^2 = 2cx + c^2$ and its $c$-derivative $0 = 2x + 2c$ gives $y^2 = -x^2$ which has no real curve, so there is no singular solution.

@s 12
$(D^2 + 3D + 2)y = e^{2x}\sin x$.

**C.F.** $m^2 + 3m + 2 = (m+1)(m+2) = 0$: $y_c = c_1e^{-x} + c_2e^{-2x}$.

**P.I.** Using $\dfrac{1}{f(D)}e^{2x}V = e^{2x}\dfrac{1}{f(D+2)}V$:

$$\begin{gathered}f(D+2) = (D+2)^2 + 3(D+2) + 2 = D^2 + 7D + 12\end{gathered}$$

$$\begin{gathered}\text{P.I.} = e^{2x}\frac{1}{D^2 + 7D + 12}\sin x = e^{2x}\frac{1}{7D + 11}\sin x\quad(D^2\to-1)\end{gathered}$$

$$\begin{gathered}\frac{1}{7D+11} = \frac{11 - 7D}{121 - 49D^2} = \frac{11 - 7D}{170}\quad(D^2\to-1)\end{gathered}$$

$$\text{P.I.} = \frac{e^{2x}}{170}(11\sin x - 7\cos x)$$

$$\boxed{y = c_1e^{-x} + c_2e^{-2x} + \frac{e^{2x}}{170}\big(11\sin x - 7\cos x\big)}$$

(verified by substitution.)

@s 13
Multiply by $x$: $x^2y'' - 2xy' + 2y = \dfrac1x$, a Cauchy-Euler equation. Put $x = e^z$, $D_1 = \dfrac d{dz}$:

$$\begin{gathered}\big[D_1(D_1 - 1) - 2D_1 + 2\big]y = e^{-z}\ \Longrightarrow\ (D_1^2 - 3D_1 + 2)y = e^{-z}\end{gathered}$$

**C.F.** $m^2 - 3m + 2 = 0\Rightarrow m = 1, 2$: $y_c = c_1e^z + c_2e^{2z} = c_1x + c_2x^2$.

**P.I.** $\dfrac{1}{D_1^2 - 3D_1 + 2}e^{-z} = \dfrac{1}{1 + 3 + 2}e^{-z} = \dfrac{e^{-z}}{6}$.

$$\boxed{y = c_1x + c_2x^2 + \frac{1}{6x}}$$

@s 14
**Definition.** An ellipse is the locus of a point $P$ that moves so that its distance from a fixed point $S$ (focus) is $e$ ($0<e<1$) times its distance from a fixed line (directrix): $SP = e\cdot PM$.

```figure caption="Question 14: ellipse with foci S, S', directrices x = +-a/e, semi-axes a and b."
a,b=2.4,1.6; c=np.sqrt(a*a-b*b); t=np.linspace(0,2*np.pi,300)
fig,ax=plt.subplots(figsize=(4.6,2.8))
ax.plot(a*np.cos(t),b*np.sin(t),color='#1d6fb8',lw=1.8)
for s in (1,-1): ax.axvline(s*a*a/c,color='#d9534f',lw=.9,ls=':')
ax.plot([c,-c,0],[0,0,0],'o',color='#14181f',ms=3)
for xx,l in [(c,'S'),(-c,"S'"),(0,'O')]: ax.text(xx,-0.3,l,ha='center',fontsize=8)
ax.text(a,0.1,'A',fontsize=8); ax.text(-a-.25,0.1,"A'",fontsize=8); ax.text(.05,b+.08,'B',fontsize=8)
ax.text(a*a/c+.05,1.3,'x = a/e',fontsize=7,color='#d9534f')
ax.axhline(0,color='#14181f',lw=.5); ax.axvline(0,color='#14181f',lw=.5); ax.set_aspect('equal'); ax.axis('off')
```

Take the focus $S = (ae, 0)$ and directrix $x = \dfrac ae$. For $P(x,y)$:

$$\begin{gathered}(x - ae)^2 + y^2 = e^2\left(\frac ae - x\right)^2 = (a - ex)^2\end{gathered}$$

$$x^2 - 2aex + a^2e^2 + y^2 = a^2 - 2aex + e^2x^2$$

$$x^2(1 - e^2) + y^2 = a^2(1 - e^2)$$

Divide by $a^2(1-e^2)$ and put $b^2 = a^2(1 - e^2)$ ($b<a$):

$$\begin{gathered}\boxed{\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1,\qquad b^2 = a^2(1 - e^2)}\end{gathered}$$

Foci $(\pm ae, 0)$, directrices $x = \pm\dfrac ae$, vertices $(\pm a, 0)$, major axis $2a$, minor axis $2b$, latus rectum $\dfrac{2b^2}{a}$. The relation $SP + S'P = 2a$ follows since $SP = a - ex$, $S'P = a + ex$.

@s 15
$ax^2 + 2hxy + by^2 + \ldots$ is turned into a form without $xy$ by rotating through $\theta$, $\tan2\theta = \dfrac{2h}{a - b}$. Here $a = b = 3$, $h = 1$:

$$\begin{gathered}\tan2\theta = \frac{2}{0} = \infty\ \Longrightarrow\ 2\theta = 90^\circ\end{gathered}$$

$$\begin{gathered}\boxed{\theta = 45^\circ = \frac\pi4}\end{gathered}$$

**Check.** Substituting $x = \dfrac{X - Y}{\sqrt2}$, $y = \dfrac{X + Y}{\sqrt2}$ gives $3(X^2 + Y^2) + (X^2 - Y^2) - (X - Y) = 0$, i.e. $4X^2 + 2Y^2 - X + Y = 0$, which has no $XY$ term.

@s 16
**Main question: $9x^2 + 4xy + 6y^2 - 22x - 16y + 9 = 0$.** Here $a = 9$, $2h = 4$ ($h = 2$), $b = 6$, $2g = -22$, $2f = -16$, $c = 9$. The discriminant $h^2 - ab = 4 - 54 < 0$, so it is an **ellipse**.

*Centre.* Solve $\partial/\partial x = 0$, $\partial/\partial y = 0$:

$$\begin{gathered}18x + 4y - 22 = 0,\quad 4x + 12y - 16 = 0\ \Longrightarrow\ 9x + 2y = 11,\ x + 3y = 4\ \Longrightarrow\ x = 1,\ y = 1\end{gathered}$$

**Centre $(1,1)$.** Shift the origin ($x = X + 1$, $y = Y + 1$): the constant is $gx_0 + fy_0 + c = -11 - 8 + 9 = -10$:

$$9X^2 + 4XY + 6Y^2 = 10$$

*Axes.* The quadratic form has matrix $\begin{pmatrix}9&2\\2&6\end{pmatrix}$, characteristic equation $\lambda^2 - 15\lambda + 50 = 0$, $\lambda = 10, 5$. Rotating the axes to the principal directions ($\tan2\theta = \dfrac{4}{9-6} = \dfrac43$):

$$\begin{gathered}10X'^2 + 5Y'^2 = 10\ \Longrightarrow\ \frac{X'^2}{1} + \frac{Y'^2}{2} = 1\end{gathered}$$

So the semi-axes are $\sqrt2$ (major, along the eigenvector for $\lambda = 5$, direction $(1,-2)$) and $1$ (minor). The eccentricity: $e^2 = 1 - \dfrac{1}{2} = \dfrac12$.

$$\boxed{\text{Centre }(1,1),\quad\text{major axis }2\sqrt2,\ \text{minor axis }2,\quad e = \frac1{\sqrt2}}$$

**OR: $r = \dfrac{10}{3 + 2\cos\theta}$.** Divide by $3$: $r = \dfrac{10/3}{1 + \frac23\cos\theta}$, the standard form $r = \dfrac{\ell}{1 + e\cos\theta}$ with

$$\begin{gathered}e = \frac23<1 \\ \ell = \frac{10}{3}\end{gathered}$$

So the curve is an **ellipse** with one focus at the pole, the directrix $x = \dfrac\ell e = 5$ (to the right of the pole) and major axis along the initial line.

*Vertices:* $\theta = 0$: $r = \dfrac{10}{5} = 2$, point $(2,0)$. $\theta = \pi$: $r = \dfrac{10}{1} = 10$, point $(-10, 0)$ (it lies on the negative side as $\cos\pi = -1$).

$2a = 2 + 10 = 12\Rightarrow a = 6$; centre $(-4, 0)$; $c = ae = 4$ so the second focus is $(-8, 0)$; $b^2 = a^2(1 - e^2) = 36\cdot\dfrac59 = 20$. Cartesian form: $\dfrac{(x+4)^2}{36} + \dfrac{y^2}{20} = 1$. Latus rectum $2\ell = \dfrac{20}{3}$; the semi-latus rectum $\ell = \dfrac{10}3$ is the length of the focal chord's half at $\theta = \dfrac\pi2$ ($r = \dfrac{10}{3}$).

```figure caption="Question 16 (OR): the ellipse r = 10/(3 + 2 cos theta): focus at the pole, vertices (2,0) and (-10,0), directrix x = 5."
t=np.linspace(0,2*np.pi,400); r=10/(3+2*np.cos(t))
fig,ax=plt.subplots(figsize=(4.8,2.8))
ax.plot(r*np.cos(t),r*np.sin(t),color='#1d6fb8',lw=1.8); ax.fill(r*np.cos(t),r*np.sin(t),color='#dbe8f6',alpha=.6)
ax.axvline(5,color='#d9534f',lw=.9,ls=':'); ax.text(5.2,3.3,'directrix x = 5',fontsize=7,color='#d9534f')
ax.plot([0,-8,-4],[0,0,0],'o',color='#14181f',ms=3)
ax.text(.3,-.9,'S (pole)',fontsize=7); ax.text(-8.2,-.9,"S'",fontsize=7); ax.text(-4,-.9,'C',fontsize=7)
ax.text(2.2,.3,'(2,0)',fontsize=7); ax.text(-10.5,.4,'(-10,0)',fontsize=7)
ax.axhline(0,color='#14181f',lw=.5); ax.set_aspect('equal'); ax.axis('off')
```

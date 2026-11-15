---
file: NEBians-IOE-Past-Paper-Engineering-Mathematics-I-SH401-2079-Baishakh.pdf
subject: Engineering Mathematics I
level: BE · Year I / Part I
code: SH 401
year_bs: 2079 Baishakh
cal: BS
year_ad: 2022
stream: All programmes except B.Arch
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, SH 401). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
State Leibnitz's theorem. If $y = \log\left(x + \sqrt{a^2 + x^2}\right)$ then using the theorem show that $(a^2 + x^2)y_2 + xy_1 = 0$ and hence show that $(a^2 + x^2)y_{n+2} + (2n+1)xy_{n+1} + n^2y_n = 0$. [[1+4]]

@q 2
Assuming the validity of expansion, find the expansion of $\log(\sec x)$ by using Maclaurin's theorem. [[5]]

@q 3
What do you mean by indeterminate form? State various forms of indeterminacy. Evaluate $\displaystyle\lim_{x\to0}\left(\frac{\sin x}{x}\right)^{1/x^2}$ [[5]]

@q 4
Define asymptotes and its types. Find the asymptotes of the curve $x^3 + 4x^2y + 5xy^2 + 2y^3 + 2x^2 + 4xy + 2y^2 - x - 9y + 1 = 0$. [[1+4]]

@q 5
Find the pedal equation of the curve $r^m = a^m\cos m\theta$. [[5]]

@q 6
Show that $\displaystyle\int_0^{\pi/2}\frac{x}{\sin x + \cos x}\,dx = \frac{\pi}{2\sqrt2}\log(\sqrt2 + 1)$. [[5]]

@q 7
Evaluate, by using the rule of differentiation under the sign of integration: $\displaystyle\int_0^\pi\frac{\log(1 + a\cos x)}{\cos x}\,dx$. [[5]]

@q 8
Define Beta and Gamma function and use these to evaluate $\displaystyle\int_0^1\frac{dx}{(1 - x^6)^{1/6}}$. [[5]]

@q 9
Find the area included between an arc of cycloid $x = a(\theta - \sin\theta)$, $y = a(1 - \cos\theta)$ and its base.

**OR**

Find the volume of the solid formed by revolution of the cardioid $r = a(1 + \cos\theta)$ about the initial base. [[5]]

@q 10
Solve the differential equation $\dfrac{dy}{dx} + \dfrac{x}{1 - x^2}\,y = x\sqrt y$. [[5]]

@q 11
State Clairaut's equation, find the general and singular solution of $y = px + p - p^2$. [[5]]

@q 12
Find the particular integral and hence solve the differential equation $y'' - 2y' + 5y = e^{2x}\sin x$. [[5]]

@q 13
Solve the differential equation $x^2\dfrac{d^2y}{dx^2} - x\dfrac{dy}{dx} + 2y = x\log x$. [[5]]

@q 14
Through what angle should the axes be rotated to reduce the equation $3x^2 + 2xy + 3y^2 - \sqrt2\,x = 0$ into one with the $xy$ term missing? Also obtain the transformed equation. [[2+3]]

@q 15
Deduce the standard equation of the hyperbola. [[5]]

@q 16
Describe and sketch the graph of the equation $r = \dfrac{10}{2 - 3\sin\theta}$.

**OR**

Find the centre, length of axes and eccentricity of the conic $3x^2 + 8xy - 3y^2 - 40x - 20y + 50 = 0$. [[5]]
<!-- SOLUTIONS -->

@s 1
**Leibnitz's theorem.** If $u,v$ are functions of $x$ possessing derivatives of every order up to $n$, then

$$\boxed{(uv)_n = u_nv + {}^nC_1u_{n-1}v_1 + {}^nC_2u_{n-2}v_2 + \cdots + uv_n}$$

**First relation.** $y = \log\left(x + \sqrt{a^2+x^2}\right)$ gives

$$\begin{gathered}y_1 = \frac{1 + \dfrac{x}{\sqrt{a^2+x^2}}}{x + \sqrt{a^2+x^2}} = \frac{1}{\sqrt{a^2+x^2}}\quad\Longrightarrow\quad \sqrt{a^2+x^2}\;y_1 = 1\end{gathered}$$

Differentiating once more:

$$\sqrt{a^2+x^2}\;y_2 + \frac{x}{\sqrt{a^2+x^2}}\,y_1 = 0$$

Multiplying by $\sqrt{a^2+x^2}$:

$$\begin{gathered}\boxed{(a^2+x^2)y_2 + xy_1 = 0} \\ (1)\end{gathered}$$

**$n$th derivative.** Differentiate (1) $n$ times by Leibnitz's theorem, taking $u = y_2$ or $y_1$ and $v = a^2+x^2$ or $x$:

- $\dfrac{d^n}{dx^n}\big[(a^2+x^2)y_2\big] = (a^2+x^2)y_{n+2} + n(2x)y_{n+1} + \dfrac{n(n-1)}{2}(2)y_n$
- $\dfrac{d^n}{dx^n}\big[xy_1\big] = xy_{n+1} + n(1)y_n$

Adding:

$$(a^2+x^2)y_{n+2} + (2n+1)xy_{n+1} + \big[n(n-1) + n\big]y_n = 0$$

$$\begin{gathered}\boxed{(a^2+x^2)y_{n+2} + (2n+1)xy_{n+1} + n^2y_n = 0} \\ \blacksquare\end{gathered}$$

@s 2
Let $f(x) = \log\sec x$, $f(0) = 0$. Writing $t = \tan x$ we have $f' = t$ and $t' = \sec^2x = 1 + t^2$, so every derivative is a polynomial in $t$:

| $k$ | $f^{(k)}(x)$ | $f^{(k)}(0)$ |
|---|---|---|
| 1 | $t$ | $0$ |
| 2 | $1 + t^2$ | $1$ |
| 3 | $2t(1+t^2)$ | $0$ |
| 4 | $2(1+t^2)(1+3t^2)$ | $2$ |
| 5 | $8t(1+t^2)(2+3t^2)$ | $0$ |
| 6 | $8(1+t^2)(2+15t^2+15t^4)$ | $16$ |

(odd derivatives vanish at $0$ because they contain the factor $t$; the even ones are obtained from $f^{(k+1)} = \dfrac{d}{dt}\big[f^{(k)}\big](1+t^2)$ at $t = 0$.)

Maclaurin's series $f(x) = f(0) + xf'(0) + \dfrac{x^2}{2!}f''(0) + \dfrac{x^3}{3!}f'''(0) + \cdots$ gives

$$\log\sec x = \frac{x^2}{2!}(1) + \frac{x^4}{4!}(2) + \frac{x^6}{6!}(16) + \cdots$$

$$\boxed{\log\sec x = \frac{x^2}{2} + \frac{x^4}{12} + \frac{x^6}{45} + \cdots}$$

*Check.* $-\log\cos x$ with $\cos x = 1 - \frac{x^2}2 + \frac{x^4}{24} - \frac{x^6}{720}$ gives the same series (verified with sympy).

@s 3
**Indeterminate form.** A function is said to be in an indeterminate form at $x = a$ if direct substitution of $a$ gives a symbol whose value is not determined, such as $\dfrac00$. The seven forms are

$$\frac00,\quad\frac\infty\infty,\quad0\cdot\infty,\quad\infty-\infty,\quad0^0,\quad1^\infty,\quad\infty^0$$

**Limit.** The given limit is of the form $1^\infty$. Let $L = \left(\dfrac{\sin x}{x}\right)^{1/x^2}$, so

$$\log L = \frac{\log(\sin x/x)}{x^2}\quad\left(\frac00\text{ form}\right)$$

Apply L'Hospital's rule:

$$\lim_{x\to0}\frac{\dfrac{x\cos x - \sin x}{x\sin x}}{2x} = \lim_{x\to0}\frac{x\cos x - \sin x}{2x^2\sin x}$$

Again $\dfrac00$. Using $x\cos x - \sin x = -\dfrac{x^3}{3} + O(x^5)$ and $2x^2\sin x = 2x^3 + O(x^5)$,

$$\begin{gathered}\lim_{x\to0}\log L = \frac{-x^3/3}{2x^3} = -\frac16\end{gathered}$$

$$\boxed{\lim_{x\to0}\left(\frac{\sin x}{x}\right)^{1/x^2} = e^{-1/6}}$$

@s 4
**Asymptote.** A straight line is an asymptote of a curve if the distance of a point $P$ on the curve from the line tends to zero as $P$ goes to infinity along the curve (equivalently, the line is a tangent to the curve at infinity). Types: (i) **parallel to the $x$-axis**, (ii) **parallel to the $y$-axis**, (iii) **oblique** ($y = mx + c$).

**Setting up.** Write the curve in homogeneous parts: $\phi_3 + \phi_2 + \phi_1 + \phi_0 = 0$ with

$$\begin{gathered}\phi_3 = x^3 + 4x^2y + 5xy^2 + 2y^3,\quad\phi_2 = 2x^2 + 4xy + 2y^2,\quad\phi_1 = -x - 9y,\quad\phi_0 = 1\end{gathered}$$

The coefficients of $x^3$ and $y^3$ are non-zero, so there are no asymptotes parallel to the axes. Put $x = 1$, $y = m$ in $\phi_3$:

$$\begin{gathered}\phi_3(m) = 2m^3 + 5m^2 + 4m + 1 = (m+1)^2(2m+1) = 0\ \Longrightarrow\ m = -1\ (\text{twice}),\ m = -\tfrac12\end{gathered}$$

**Simple root $m = -\tfrac12$.** $c = -\dfrac{\phi_2(m)}{\phi_3'(m)}$ with $\phi_2(m) = 2(1+m)^2 = \tfrac12$ and $\phi_3'(m) = 6m^2 + 10m + 4 = \tfrac12$, so $c = -1$:

$$\begin{gathered}y = -\tfrac12x - 1\quad\Longrightarrow\quad x + 2y + 2 = 0\end{gathered}$$

**Double root $m = -1$.** Here $c$ satisfies $\dfrac{c^2}{2!}\phi_3''(m) + c\,\phi_2'(m) + \phi_1(m) = 0$. With $\phi_3'' = 12m + 10 = -2$, $\phi_2' = 4(1+m) = 0$ and $\phi_1(m) = -1 - 9m = 8$:

$$\begin{gathered}-c^2 + 0 + 8 = 0\ \Longrightarrow\ c = \pm2\sqrt2\end{gathered}$$

$$\begin{gathered}y = -x \pm 2\sqrt2\ \Longrightarrow\ x + y = \pm2\sqrt2\end{gathered}$$

$$\begin{gathered}\boxed{x + 2y + 2 = 0,\qquad x + y - 2\sqrt2 = 0,\qquad x + y + 2\sqrt2 = 0}\end{gathered}$$

(Each line was substituted back into the curve with sympy: the $x^2$ coefficient vanishes for the double-root lines and the $x$ coefficient for the simple-root line, as an asymptote requires.)

@s 5
Take logarithms of $r^m = a^m\cos m\theta$ and differentiate with respect to $\theta$:

$$\begin{gathered}m\log r = m\log a + \log\cos m\theta\ \Longrightarrow\ \frac{m}{r}\frac{dr}{d\theta} = -m\tan m\theta\end{gathered}$$

$$\begin{gathered}\cot\phi = \frac1r\frac{dr}{d\theta} = -\tan m\theta = \cot\left(\frac\pi2 + m\theta\right)\ \Longrightarrow\ \phi = \frac\pi2 + m\theta\end{gathered}$$

where $\phi$ is the angle between the radius vector and the tangent. For the pedal $p = r\sin\phi$:

$$\begin{gathered}p = r\sin\left(\frac\pi2 + m\theta\right) = r\cos m\theta = r\cdot\frac{r^m}{a^m}\end{gathered}$$

$$\boxed{p\,a^m = r^{m+1}}$$

*Special cases.* $m = 1$: the circle $r = a\cos\theta$ has $pa = r^2$; $m = -1$: the straight line $r\cos\theta = a$ has $p = a$ (since $r^0 = 1$); $m = 2$: the lemniscate $r^2 = a^2\cos2\theta$ has $pa^2 = r^3$.

@s 6
Let $I = \displaystyle\int_0^{\pi/2}\frac{x}{\sin x + \cos x}\,dx$. Using $\displaystyle\int_0^af(x)\,dx = \int_0^af(a-x)\,dx$ with $a = \pi/2$ (so $\sin\to\cos$, $\cos\to\sin$):

$$I = \int_0^{\pi/2}\frac{\frac\pi2 - x}{\sin x + \cos x}\,dx$$

Adding the two forms:

$$\begin{gathered}2I = \frac\pi2\int_0^{\pi/2}\frac{dx}{\sin x + \cos x} = \frac\pi2\int_0^{\pi/2}\frac{dx}{\sqrt2\sin\left(x + \frac\pi4\right)} = \frac{\pi}{2\sqrt2}\int_0^{\pi/2}\operatorname{cosec}\left(x + \tfrac\pi4\right)dx\end{gathered}$$

Since $\displaystyle\int\operatorname{cosec}u\,du = \log\tan\frac u2$,

$$\begin{gathered}2I = \frac{\pi}{2\sqrt2}\left[\log\tan\left(\frac x2 + \frac\pi8\right)\right]_0^{\pi/2} = \frac{\pi}{2\sqrt2}\left[\log\tan\frac{3\pi}8 - \log\tan\frac\pi8\right]\end{gathered}$$

With $\tan\dfrac{3\pi}8 = \sqrt2 + 1$ and $\tan\dfrac\pi8 = \sqrt2 - 1$:

$$\begin{gathered}2I = \frac{\pi}{2\sqrt2}\log\frac{\sqrt2+1}{\sqrt2-1} = \frac{\pi}{2\sqrt2}\log(\sqrt2+1)^2 = \frac{\pi}{\sqrt2}\log(\sqrt2+1)\end{gathered}$$

$$\begin{gathered}\boxed{I = \frac{\pi}{2\sqrt2}\log(\sqrt2 + 1)} \\ \blacksquare\end{gathered}$$

@s 7
Let $I(a) = \displaystyle\int_0^\pi\frac{\log(1 + a\cos x)}{\cos x}\,dx$, $|a| < 1$. Differentiating under the integral sign (Leibnitz's rule; the limits are constant):

$$\begin{gathered}\frac{dI}{da} = \int_0^\pi\frac{1}{\cos x}\cdot\frac{\cos x}{1 + a\cos x}\,dx = \int_0^\pi\frac{dx}{1 + a\cos x}\end{gathered}$$

Put $t = \tan\dfrac x2$, $\cos x = \dfrac{1-t^2}{1+t^2}$, $dx = \dfrac{2\,dt}{1+t^2}$, $x:0\to\pi\Rightarrow t:0\to\infty$:

$$\begin{gathered}\frac{dI}{da} = \int_0^\infty\frac{2\,dt}{(1+a) + (1-a)t^2} = \frac{2}{\sqrt{1-a^2}}\left[\tan^{-1}\left(t\sqrt{\tfrac{1-a}{1+a}}\right)\right]_0^\infty = \frac{\pi}{\sqrt{1-a^2}}\end{gathered}$$

Integrate with respect to $a$:

$$I(a) = \pi\sin^{-1}a + C$$

At $a = 0$ the integrand is $0$, so $I(0) = 0$ and $C = 0$:

$$\boxed{\int_0^\pi\frac{\log(1 + a\cos x)}{\cos x}\,dx = \pi\sin^{-1}a}$$

@s 8
**Definitions.**

$$\begin{gathered}\Gamma(n) = \int_0^\infty e^{-x}x^{n-1}\,dx\ (n>0) \\ B(m,n) = \int_0^1x^{m-1}(1-x)^{n-1}\,dx\ (m,n>0)\end{gathered}$$

with $B(m,n) = \dfrac{\Gamma(m)\Gamma(n)}{\Gamma(m+n)}$, $\Gamma(n+1) = n\Gamma(n)$ and the reflection formula $\Gamma(n)\Gamma(1-n) = \dfrac{\pi}{\sin n\pi}$ for $0<n<1$.

**Evaluation.** Put $x^6 = t$, $x = t^{1/6}$, $dx = \tfrac16t^{-5/6}dt$; $x:0\to1\Rightarrow t:0\to1$:

$$\begin{gathered}\int_0^1\frac{dx}{(1-x^6)^{1/6}} = \frac16\int_0^1t^{-5/6}(1-t)^{-1/6}\,dt = \frac16B\left(\tfrac16,\tfrac56\right)\end{gathered}$$

$$\begin{gathered}= \frac16\cdot\frac{\Gamma(\frac16)\Gamma(\frac56)}{\Gamma(1)} = \frac16\cdot\frac{\pi}{\sin\frac\pi6} = \frac16\cdot2\pi\end{gathered}$$

$$\boxed{\int_0^1\frac{dx}{(1-x^6)^{1/6}} = \frac\pi3}$$

@s 9
**Main question (area under one arch of the cycloid).** The base is the $x$-axis and one arch is traced as $\theta$ goes from $0$ to $2\pi$ ($x$ from $0$ to $2\pi a$).

```figure caption="Question 9: one arch of the cycloid x = a(theta - sin theta), y = a(1 - cos theta), a = 1, and its base."
t=np.linspace(0,2*np.pi,300); x=t-np.sin(t); y=1-np.cos(t)
fig,ax=plt.subplots(figsize=(4.8,2.2))
ax.fill_between(x,y,color='#dbe8f6',alpha=.8); ax.plot(x,y,color='#1d6fb8',lw=1.8)
ax.axhline(0,color='#14181f',lw=.9)
ax.set_xticks([0,np.pi,2*np.pi]); ax.set_xticklabels(['O','$\\pi a$','$2\\pi a$'])
ax.set_yticks([0,2]); ax.set_yticklabels(['0','$2a$'])
ax.text(np.pi,0.8,'area A',ha='center',fontsize=8)
ax.set_aspect('equal'); ax.spines[['top','right']].set_visible(False)
```

$$\begin{gathered}A = \int y\,dx = \int_0^{2\pi}a(1-\cos\theta)\cdot a(1-\cos\theta)\,d\theta = a^2\int_0^{2\pi}(1-\cos\theta)^2\,d\theta\end{gathered}$$

Using $1 - \cos\theta = 2\sin^2\dfrac\theta2$ and $\theta = 2u$:

$$\begin{gathered}A = a^2\int_0^{2\pi}4\sin^4\frac\theta2\,d\theta = 8a^2\int_0^\pi\sin^4u\,du = 16a^2\int_0^{\pi/2}\sin^4u\,du = 16a^2\cdot\frac{3\pi}{16}\end{gathered}$$

$$\boxed{A = 3\pi a^2}$$

(three times the area of the generating circle).

**OR (volume of the cardioid $r = a(1 + \cos\theta)$ about the initial line).** The upper half $\theta\in[0,\pi]$ generates the solid. The volume of revolution of a polar curve about the initial line is $V = \dfrac{2\pi}{3}\displaystyle\int r^3\sin\theta\,d\theta$:

$$V = \frac{2\pi}{3}\int_0^\pi a^3(1+\cos\theta)^3\sin\theta\,d\theta$$

Put $u = 1 + \cos\theta$, $du = -\sin\theta\,d\theta$; $\theta:0\to\pi$ gives $u:2\to0$:

$$\begin{gathered}V = \frac{2\pi a^3}{3}\int_0^2u^3\,du = \frac{2\pi a^3}{3}\cdot\frac{2^4}{4}\end{gathered}$$

$$\boxed{V = \frac{8\pi a^3}{3}}$$

@s 10
The equation $\dfrac{dy}{dx} + \dfrac{x}{1-x^2}\,y = xy^{1/2}$ is Bernoulli's equation with $n = \tfrac12$. Divide by $y^{1/2}$ and put $v = y^{1/2}$, so that $\dfrac{dv}{dx} = \dfrac{1}{2y^{1/2}}\dfrac{dy}{dx}$:

$$\begin{gathered}2\frac{dv}{dx} + \frac{x}{1-x^2}\,v = x\ \Longrightarrow\ \frac{dv}{dx} + \frac{x}{2(1-x^2)}\,v = \frac x2\end{gathered}$$

This is linear. The integrating factor is

$$\begin{gathered}\text{I.F.} = \exp\int\frac{x\,dx}{2(1-x^2)} = \exp\left[-\tfrac14\log(1-x^2)\right] = (1-x^2)^{-1/4}\end{gathered}$$

Then

$$\begin{gathered}v(1-x^2)^{-1/4} = \int\frac x2(1-x^2)^{-1/4}dx = -\frac13(1-x^2)^{3/4} + C\end{gathered}$$

Multiplying through by $(1-x^2)^{1/4}$ and using $v = \sqrt y$:

$$\boxed{\sqrt y = C(1-x^2)^{1/4} - \tfrac13(1-x^2)}$$

(verified by substitution in sympy).

@s 11
**Clairaut's equation** is $y = px + f(p)$, $p = \dfrac{dy}{dx}$. Its general solution is obtained by replacing $p$ by an arbitrary constant $c$, and the singular solution is the envelope of that family (eliminate $p$ between the equation and $x + f'(p) = 0$).

Here $y = px + (p - p^2)$ is of Clairaut's type with $f(p) = p - p^2$.

**General solution:** put $p = c$:

$$\boxed{y = cx + c - c^2}$$

**Singular solution.** Differentiate $y = px + p - p^2$ with respect to $p$ (treating $x$ as constant): $0 = x + 1 - 2p$, so $p = \dfrac{x+1}{2}$. Substituting,

$$\begin{gathered}y = (x+1)p - p^2 = \frac{(x+1)^2}{2} - \frac{(x+1)^2}{4} = \frac{(x+1)^2}{4}\end{gathered}$$

$$\boxed{(x+1)^2 = 4y}$$

a parabola that touches every line of the general family.

@s 12
$y'' - 2y' + 5y = e^{2x}\sin x$, i.e. $(D^2 - 2D + 5)y = e^{2x}\sin x$.

**Complementary function.** $m^2 - 2m + 5 = 0\Rightarrow m = 1\pm2i$:

$$y_c = e^x(c_1\cos2x + c_2\sin2x)$$

**Particular integral.** Use $\dfrac{1}{f(D)}e^{ax}V = e^{ax}\dfrac{1}{f(D+a)}V$ with $a = 2$:

$$\begin{gathered}f(D+2) = (D+2)^2 - 2(D+2) + 5 = D^2 + 2D + 5\end{gathered}$$

$$\begin{gathered}\text{P.I.} = e^{2x}\frac{1}{D^2 + 2D + 5}\sin x = e^{2x}\frac{1}{2D + 4}\sin x\quad(D^2\to-1)\end{gathered}$$

Rationalise: $\dfrac{1}{2D+4} = \dfrac{2 - D}{2(4 - D^2)}\to\dfrac{2-D}{10}$ (with $D^2 = -1$):

$$\begin{gathered}\text{P.I.} = \frac{e^{2x}}{10}(2 - D)\sin x = \frac{e^{2x}}{10}(2\sin x - \cos x)\end{gathered}$$

$$\boxed{y = e^x(c_1\cos2x + c_2\sin2x) + \frac{e^{2x}}{10}(2\sin x - \cos x)}$$

(checked by direct substitution with sympy).

@s 13
$x^2y'' - xy' + 2y = x\log x$ is a Cauchy-Euler equation. Put $x = e^z$, $z = \log x$, $D_1 = \dfrac{d}{dz}$: $xy' = D_1y$, $x^2y'' = D_1(D_1-1)y$.

$$\begin{gathered}\big[D_1(D_1 - 1) - D_1 + 2\big]y = ze^z\ \Longrightarrow\ (D_1^2 - 2D_1 + 2)y = ze^z\end{gathered}$$

**C.F.** $m^2 - 2m + 2 = 0\Rightarrow m = 1\pm i$: $y_c = e^z(c_1\cos z + c_2\sin z)$.

**P.I.**

$$\begin{gathered}\frac{1}{D_1^2 - 2D_1 + 2}ze^z = e^z\frac{1}{(D_1+1)^2 - 2(D_1+1) + 2}z = e^z\frac{1}{D_1^2 + 1}z = e^z(1 + D_1^2)^{-1}z = e^z(1 - D_1^2 + \cdots)z = ze^z\end{gathered}$$

Returning to $x$ ($e^z = x$, $z = \log x$):

$$\boxed{y = x\big[c_1\cos(\log x) + c_2\sin(\log x)\big] + x\log x}$$

@s 14
For $ax^2 + 2hxy + by^2 + \ldots$ the axes are rotated through $\theta$ with $\tan2\theta = \dfrac{2h}{a - b}$. Here $a = b = 3$, $2h = 2$, so $\tan2\theta = \dfrac{2}{0} = \infty$:

$$\begin{gathered}2\theta = \frac\pi2\quad\Longrightarrow\quad\boxed{\theta = \frac\pi4 = 45^\circ}\end{gathered}$$

**Transformed equation.** Substituting $x = X\cos\theta - Y\sin\theta = \dfrac{X - Y}{\sqrt2}$ and $y = X\sin\theta + Y\cos\theta = \dfrac{X + Y}{\sqrt2}$:

$$\begin{gathered}3(x^2 + y^2) = 3(X^2 + Y^2) \\ 2xy = X^2 - Y^2 \\ -\sqrt2x = -(X - Y)\end{gathered}$$

$$3X^2 + 3Y^2 + X^2 - Y^2 - X + Y = 0$$

$$\boxed{4X^2 + 2Y^2 - X + Y = 0}$$

The $XY$ term is absent. Completing squares, $4\left(X - \tfrac18\right)^2 + 2\left(Y + \tfrac14\right)^2 = \tfrac1{16} + \tfrac18 = \tfrac{3}{16}$, an ellipse.

@s 15
**Definition.** A hyperbola is the locus of a point $P$ that moves so that the ratio of its distance from a fixed point $S$ (the *focus*) to its distance from a fixed line (the *directrix*) is a constant $e > 1$ (the *eccentricity*): $SP = e\cdot PM$.

**Deduction.** Let $S = (ae, 0)$ be the focus and $x = \dfrac ae$ the directrix, the point $P(x, y)$ and $PM\perp$ directrix.

```figure caption="Question 15: hyperbola from the focus-directrix definition, with foci S, S', centre O, vertices A, A' and asymptotes."
a,b=2.0,1.5; c=np.hypot(a,b); t=np.linspace(-1.6,1.6,200)
fig,ax=plt.subplots(figsize=(4.4,3.0))
for s in (1,-1): ax.plot(s*a*np.cosh(t),b*np.sinh(t),color='#1d6fb8',lw=1.8)
xs=np.array([-4.2,4.2]); ax.plot(xs,b/a*xs,'--',color='#999',lw=.9); ax.plot(xs,-b/a*xs,'--',color='#999',lw=.9)
for s in (1,-1): ax.axvline(s*a*a/c,color='#d9534f',lw=.9,ls=':')
ax.plot([c,-c,a,-a,0],[0,0,0,0,0],'o',color='#14181f',ms=3)
for xx,l in [(c,'S'),(-c,"S'"),(a,'A'),(-a,"A'"),(0,'O')]: ax.text(xx,-0.4,l,ha='center',fontsize=8)
ax.text(a*a/c+.05,2.2,'directrix',fontsize=7,color='#d9534f')
ax.axhline(0,color='#14181f',lw=.6); ax.set_aspect('equal'); ax.axis('off'); ax.set_ylim(-2.6,2.8)
```

$$\begin{gathered}SP^2 = e^2PM^2\ \Longrightarrow\ (x - ae)^2 + y^2 = e^2\left(x - \frac ae\right)^2 = (ex - a)^2\end{gathered}$$

$$x^2 - 2aex + a^2e^2 + y^2 = e^2x^2 - 2aex + a^2$$

$$x^2(e^2 - 1) - y^2 = a^2(e^2 - 1)$$

Dividing by $a^2(e^2-1)$ and putting $b^2 = a^2(e^2 - 1)$:

$$\begin{gathered}\boxed{\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1,\qquad b^2 = a^2(e^2-1)}\end{gathered}$$

By symmetry the second focus $S'(-ae, 0)$ and directrix $x = -\dfrac ae$ give the same curve. Vertices $(\pm a, 0)$, transverse axis $2a$, conjugate axis $2b$, latus rectum $\dfrac{2b^2}{a}$, asymptotes $y = \pm\dfrac bax$.

@s 16
**Main question: $r = \dfrac{10}{2 - 3\sin\theta}$.** Write it in the standard polar form $r = \dfrac{\ell}{1 - e\sin\theta}$ by dividing numerator and denominator by $2$:

$$\begin{gathered}r = \frac{5}{1 - \frac32\sin\theta}\quad\Longrightarrow\quad e = \frac32>1 \\ \ell = 5\ (\text{semi-latus rectum})\end{gathered}$$

So the curve is a **hyperbola** with a focus at the pole and directrix $y = -d$ where $ed = \ell\Rightarrow d = \dfrac{10}{3}$ (the directrix lies below the pole, $y = -\tfrac{10}3$). Its axis is the line $\theta = \dfrac\pi2$ ($y$-axis).

**Vertices.** At $\theta = \dfrac\pi2$: $r = \dfrac{5}{1 - 1.5} = -10$, the point $(0, -10)$. At $\theta = \dfrac{3\pi}{2}$: $r = \dfrac{5}{1 + 1.5} = 2$, the point $(0, -2)$ (since $\sin\frac{3\pi}2 = -1$, $y = r\sin\theta = -2$).

Centre $= (0, -6)$, $2a = 8\Rightarrow a = 4$, $c = ae = 6$ (so the foci are $(0,0)$ and $(0,-12)$), $b^2 = c^2 - a^2 = 20$. In Cartesian form

$$\frac{(y+6)^2}{16} - \frac{x^2}{20} = 1$$

The curve is unbounded where $1 - \frac32\sin\theta = 0$, i.e. $\sin\theta = \frac23$ (asymptotic directions $\theta = 41.8^\circ,\ 138.2^\circ$).

```figure caption="Question 16: the hyperbola r = 10/(2 - 3 sin theta): focus at the pole, vertices (0,-2) and (0,-10), directrix y = -10/3."
t=np.linspace(-1.5,1.5,200)
fig,ax=plt.subplots(figsize=(3.8,4.2))
for s in (1,-1): ax.plot(np.sqrt(20)*np.sinh(t),-6+s*4*np.cosh(t),color='#1d6fb8',lw=1.8)
xs=np.array([-8,8]); ax.plot(xs,-6+4/np.sqrt(20)*xs,'--',color='#999',lw=.9); ax.plot(xs,-6-4/np.sqrt(20)*xs,'--',color='#999',lw=.9)
ax.axhline(-10/3,color='#d9534f',lw=.9,ls=':'); ax.text(3.5,-10/3+.3,'directrix y = -10/3',fontsize=7,color='#d9534f')
ax.plot([0,0,0,0],[0,-12,-2,-10],'o',color='#14181f',ms=3); ax.plot([0],[-6],'s',color='#14181f',ms=3)
ax.text(.4,.2,'S (pole)',fontsize=7); ax.text(.4,-12.5,"S'",fontsize=7); ax.text(.4,-1.5,'(0,-2)',fontsize=7); ax.text(.4,-10.9,'(0,-10)',fontsize=7); ax.text(.4,-6.4,'C',fontsize=7)
ax.axhline(0,color='#14181f',lw=.5); ax.axvline(0,color='#14181f',lw=.5)
ax.set_xlim(-8,8); ax.set_ylim(-14,4); ax.set_aspect('equal'); ax.axis('off')
```

**OR: $3x^2 + 8xy - 3y^2 - 40x - 20y + 50 = 0$.** Here $a = 3$, $2h = 8$, $b = -3$, $2g = -40$, $2f = -20$, $c = 50$.

*Centre.* Solve $\dfrac{\partial}{\partial x} = 0$, $\dfrac{\partial}{\partial y} = 0$:

$$\begin{gathered}6x + 8y - 40 = 0 \\ 8x - 6y - 20 = 0\ \Longrightarrow\ 3x + 4y = 20,\ 4x - 3y = 10\ \Longrightarrow\ x = 4,\ y = 2\end{gathered}$$

**Centre $(4, 2)$.** Shift the origin there ($x = X + 4$, $y = Y + 2$): the constant becomes $gx_0 + fy_0 + c = -20(4) - 10(2) + 50 = -50$, so

$$3X^2 + 8XY - 3Y^2 = 50$$

*Axes.* The quadratic form has matrix $\begin{pmatrix}3&4\\4&-3\end{pmatrix}$ with eigenvalues $\lambda^2 - 25 = 0$, $\lambda = \pm5$. Rotating the axes through $\theta$ with $\tan2\theta = \dfrac{8}{3-(-3)} = \dfrac43$ (so $\tan\theta = \tfrac12$):

$$\begin{gathered}5X'^2 - 5Y'^2 = 50\ \Longrightarrow\ \frac{X'^2}{10} - \frac{Y'^2}{10} = 1\end{gathered}$$

It is a **rectangular hyperbola** ($a + b = 0$): $a^2 = b^2 = 10$.

$$\begin{gathered}\boxed{\text{Centre }(4,2),\quad\text{transverse axis }2a = 2\sqrt{10},\ \text{conjugate axis }2b = 2\sqrt{10},\quad e = \sqrt{1 + \tfrac{b^2}{a^2}} = \sqrt2}\end{gathered}$$

```figure caption="Question 16 (OR): the rectangular hyperbola 3x^2 + 8xy - 3y^2 - 40x - 20y + 50 = 0 with centre (4, 2), axes rotated by tan(theta) = 1/2."
t=np.linspace(-1.3,1.3,200); u=np.array([2,1])/np.sqrt(5); v=np.array([-1,2])/np.sqrt(5); C=np.array([4,2])
fig,ax=plt.subplots(figsize=(4.2,3.6))
for s in (1,-1):
    P=C[:,None]+u[:,None]*(s*np.sqrt(10)*np.cosh(t))+v[:,None]*(np.sqrt(10)*np.sinh(t)); ax.plot(P[0],P[1],color='#1d6fb8',lw=1.8)
for sg in (1,-1):
    s=np.array([-9,9]); P=C[:,None]+u[:,None]*s+v[:,None]*(sg*s); ax.plot(P[0],P[1],'--',color='#999',lw=.9)
ax.plot([4],[2],'o',color='#14181f',ms=3); ax.text(4.3,1.2,'C(4,2)',fontsize=7)
ax.axhline(0,color='#14181f',lw=.5); ax.axvline(0,color='#14181f',lw=.5)
ax.set_xlim(-7,12); ax.set_ylim(-7,10); ax.set_aspect('equal'); ax.axis('off')
```

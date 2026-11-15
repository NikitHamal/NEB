---
file: NEBians-IOE-Past-Paper-Engineering-Numerical-Methods-ENSH252-2083-Baishakh.pdf
subject: Numerical Methods
level: BE · Year II / Part II
code: ENSH 252
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE (BEL, BEI, BCT, BAM, BIE, BAG, BGE, BCH). Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
Find a real root of the equation $x\,e^{2x} + \cos 2x = 1.5$ using the secant method, correct to four places of decimal. [[5]]

@q 2
Write the Jacobian matrix for the following system of equations and then use the Newton-Raphson method to approximate a solution correct to two decimal places. Take $(x_0, y_0) = (1, 1)$.
$$\begin{gathered}\sin y + x^2 = 2\\ \cos x + y^2 = 4\end{gathered}$$
[[5]]

@q 3
Using the LU factorization method, solve the following system of equations.
$$\begin{gathered}4x - 5y + 7z = 27\\ 9x + 4y + z = 30\\ 7x + 10y + z = 48\end{gathered}$$
[[5]]

@q 4
Find the dominant eigenvalue and the corresponding eigenvector of the given matrix using the power method.
$$\begin{pmatrix} 2 & 4 & 1 \\ 4 & 2 & 1 \\ 1 & 1 & -2 \end{pmatrix}$$
[[5]]

@q 5
Using the least square method, fit the following data to the curve of the form $y = ae^{bx}$.

| $x$ | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|
| $y$ | 4.1 | 11.2 | 30.2 | 81.9 | 204.6 | 802.8 |

[[5]]

@q 6
From the following table, evaluate $y(9)$ using Newton's divided difference interpolation technique.

| $x$ | 0 | 2 | 5 | 7 | 8 | 10 |
|---|---|---|---|---|---|---|
| $y$ | 4.72 | 7.1 | 5.72 | 5.7 | 7.04 | 14.22 |

[[5]]

@q 7
Derive the formula for the first and second order derivatives using Newton's forward interpolation formula. Also find the expressions at the initial point. [[5]]

@q 8
Approximate the value of the following definite integral using Weddle's rule taking $n = 12$.
$$\int_0^1 \frac{1}{1 + x}\,dx$$
[[5]]

@q 9
Write a program code in Python to solve a first order initial value problem using the Runge-Kutta second order method. [[5]]

@q 10
Solve the following boundary value problem using the finite difference method by dividing the interval into four sub-intervals.
$$\begin{gathered}y'' + 5y' - 3y = \sin x; \\ y(0) = 2,\ y(2) = 4\end{gathered}$$
[[5]]

@q 11
Solve the equation $\dfrac{\partial^2 u}{\partial x^2} + \dfrac{\partial^2 u}{\partial y^2} = 0$ on the mesh bounded by $0 \le x, y \le 3$ and $\Delta x = \Delta y = h = k = 1$. The boundary values are
$$\begin{gathered}u(x, 0) = 100x\\ u(x, 3) = 200(3 - x)\\ u(3, y) = 100(3 - y)\\ u(0, y) = 200y\end{gathered}$$
[[5]]

@q 12
Solve the one-dimensional heat equation $u_t = u_{xx}$ for two time steps with $\Delta x = h = 1$ using the Crank-Nicolson method, given that $\alpha = 1$, with initial and boundary conditions:
$$\begin{gathered}u(x, 0) = x(4 - x)\\ u(0, t) = u(4, t) = 0\end{gathered}$$
[[5]]
<!-- SOLUTIONS -->

@s 1
**Secant method.** Replace the tangent of Newton's method by the chord through the last two iterates:

$$\begin{gathered}x_{i+1} = x_i - f(x_i)\,\frac{x_i - x_{i-1}}{f(x_i) - f(x_{i-1})} = \frac{x_{i-1}f(x_i) - x_i f(x_{i-1})}{f(x_i) - f(x_{i-1})}.\end{gathered}$$

Let $f(x) = x\,e^{2x} + \cos 2x - 1.5$ (radians). Then $f(0) = 0 + 1 - 1.5 = -0.5$ and $f(1) = 7.389 - 0.416 - 1.5 = 5.473$, so a root lies in $(0, 1)$. Start with $x_0 = 0,\ x_1 = 0.5$; $f(0.5) = 1.35914 + 0.54030 - 1.5 = 0.39944$.

| $i$ | $x_{i-1}$ | $x_i$ | $f(x_{i-1})$ | $f(x_i)$ | $x_{i+1}$ |
|---|---|---|---|---|---|
| 1 | 0 | 0.500000 | −0.500000 | 0.399443 | 0.277950 |
| 2 | 0.500000 | 0.277950 | 0.399443 | −0.165966 | 0.343129 |
| 3 | 0.277950 | 0.343129 | −0.165966 | −0.044831 | 0.367251 |
| 4 | 0.343129 | 0.367251 | −0.044831 | 0.007679 | 0.363724 |
| 5 | 0.367251 | 0.363724 | 0.007679 | −0.000294 | 0.363854 |
| 6 | 0.363724 | 0.363854 | −0.000294 | −0.000002 | 0.363855 |

The last two iterates, $0.363854$ and $0.363855$, agree to four decimals ($f \approx 4\times10^{-10}$ at the next step).

$$\boxed{x \approx 0.3639}$$

```figure caption="$f(x) = x e^{2x} + \cos 2x - 1.5$ crosses zero at $x \approx 0.3639$. The two starting points $x_0 = 0$ and $x_1 = 0.5$ and the first secant line are shown."
import numpy as np, matplotlib.pyplot as plt
x=np.linspace(-0.2,0.8,300); f=lambda t:t*np.exp(2*t)+np.cos(2*t)-1.5
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(x,f(x),color=ACCENT,label="f(x)"); ax.axhline(0,color=INK,lw=0.7)
ax.plot([0,0.5],[f(0),f(0.5)],'--',color=SERIES[1],lw=1,label="first secant")
ax.plot([0,0.5],[f(0),f(0.5)],'o',color=SERIES[1],ms=4)
ax.plot([0.363855],[0],'o',color=ACCENT); ax.annotate("x = 0.3639",(0.363855,0),textcoords="offset points",xytext=(12,10),fontsize=7.5)
ax.set_xlabel("x"); ax.set_ylabel("f(x)"); ax.legend(fontsize=7); ax.grid(True)
```

@s 2
Let $F_1(x, y) = \sin y + x^2 - 2$ and $F_2(x, y) = \cos x + y^2 - 4$. The **Jacobian matrix** is

$$J = \begin{pmatrix} \partial F_1/\partial x & \partial F_1/\partial y \\ \partial F_2/\partial x & \partial F_2/\partial y \end{pmatrix} = \begin{pmatrix} 2x & \cos y \\ -\sin x & 2y \end{pmatrix}.$$

Each Newton-Raphson step solves $J\,\Delta = -F$ and sets $(x, y) \leftarrow (x, y) + \Delta$.

**Iteration 1**, $(x_0, y_0) = (1, 1)$: $F = (-0.158529,\ -2.459698)$,

$$\begin{pmatrix} 2 & 0.540302 \\ -0.841471 & 2 \end{pmatrix}\begin{pmatrix}\Delta x\\ \Delta y\end{pmatrix} = \begin{pmatrix}0.158529\\ 2.459698\end{pmatrix} \Rightarrow \Delta = (-0.227161,\ 1.134274)$$

$$(x_1, y_1) = (0.772839,\ 2.134274)$$

**Iteration 2**: $F = (-0.557317,\ 1.271058)$, $J = \begin{pmatrix} 1.545678 & -0.534130 \\ -0.698171 & 4.268548\end{pmatrix}$, $\Delta = (0.273101,\ -0.253104)$,

$$(x_2, y_2) = (1.045940,\ 1.881170)$$

**Iteration 3**: $F = (0.046211,\ 0.039890)$, $J = \begin{pmatrix} 2.091881 & -0.305415 \\ -0.865396 & 3.762341\end{pmatrix}$, $\Delta = (-0.024460,\ -0.016229)$,

$$(x_3, y_3) = (1.021481,\ 1.864942)$$

**Iteration 4**: $F = (0.000473,\ 0.000111)$, $\Delta = (-0.000244,\ -0.000086)$,

$$(x_4, y_4) = (1.021237,\ 1.864856)$$

| Iter | $x$ | $y$ | $F_1$ | $F_2$ |
|---|---|---|---|---|
| 0 | 1.000000 | 1.000000 | −0.158529 | −2.459698 |
| 1 | 0.772839 | 2.134274 | −0.557317 | 1.271058 |
| 2 | 1.045940 | 1.881170 | 0.046211 | 0.039890 |
| 3 | 1.021481 | 1.864942 | 0.000473 | 0.000111 |
| 4 | 1.021237 | 1.864856 | 0.000000 | 0.000000 |

Iterates 3 and 4 agree to two decimals.

$$\boxed{x \approx 1.02,\qquad y \approx 1.86}$$

@s 3
**LU (Doolittle) factorization.** Write $A = LU$ with $L$ unit lower-triangular, then solve $Ly = b$ (forward) and $Ux = y$ (backward).

$$A = \begin{pmatrix} 4 & -5 & 7 \\ 9 & 4 & 1 \\ 7 & 10 & 1 \end{pmatrix}, \qquad b = \begin{pmatrix} 27 \\ 30 \\ 48 \end{pmatrix}$$

*First row of $U$* = first row of $A$: $u_{11} = 4,\ u_{12} = -5,\ u_{13} = 7$.

*First column of $L$*: $l_{21} = 9/4 = 2.25,\quad l_{31} = 7/4 = 1.75$.

*Second row of $U$*: $u_{22} = 4 - 2.25(-5) = 15.25,\quad u_{23} = 1 - 2.25(7) = -14.75$.

*Second column of $L$*: $l_{32} = \dfrac{10 - 1.75(-5)}{15.25} = \dfrac{18.75}{15.25} = 1.229508$.

*Third row of $U$*: $u_{33} = 1 - 1.75(7) - 1.229508(-14.75) = 6.885246$.

$$L = \begin{pmatrix} 1 & 0 & 0 \\ 2.25 & 1 & 0 \\ 1.75 & 1.229508 & 1 \end{pmatrix}, \qquad U = \begin{pmatrix} 4 & -5 & 7 \\ 0 & 15.25 & -14.75 \\ 0 & 0 & 6.885246 \end{pmatrix}$$

**Forward substitution** $Ly = b$:

$$\begin{gathered}y_1 = 27\\ y_2 = 30 - 2.25(27) = -30.75\\ y_3 = 48 - 1.75(27) - 1.229508(-30.75) = 38.557377\end{gathered}$$

**Back substitution** $Ux = y$:

$$\begin{gathered}z = \frac{38.557377}{6.885246} = 5.6\\ y = \frac{-30.75 + 14.75(5.6)}{15.25} = 3.4\\ x = \frac{27 + 5(3.4) - 7(5.6)}{4} = 1.2\end{gathered}$$

Check in the second equation: $9(1.2) + 4(3.4) + 5.6 = 10.8 + 13.6 + 5.6 = 30$ ✓.

$$\boxed{x = 1.2,\qquad y = 3.4,\qquad z = 5.6}$$

@s 4
**Power method.** Start with $x^{(0)} = (1, 1, 1)^T$. Repeat $y = Ax^{(k)}$, $\lambda_k = $ the entry of $y$ of largest magnitude, $x^{(k+1)} = y/\lambda_k$.

| $k$ | $Ax^{(k)}$ | $\lambda_k$ | $x^{(k+1)}$ |
|---|---|---|---|
| 0 | (7, 7, 0) | 7 | (1, 1, 0) |
| 1 | (6, 6, 2) | 6 | (1, 1, 0.33333) |
| 2 | (6.33333, 6.33333, 1.33333) | 6.33333 | (1, 1, 0.21053) |
| 3 | (6.21053, 6.21053, 1.57895) | 6.21053 | (1, 1, 0.25424) |
| 4 | (6.25424, 6.25424, 1.49153) | 6.25424 | (1, 1, 0.23848) |
| 5 | (6.23848, 6.23848, 1.52304) | 6.23848 | (1, 1, 0.24414) |
| 6 | (6.24414, 6.24414, 1.51173) | 6.24414 | (1, 1, 0.24210) |
| 7 | (6.24210, 6.24210, 1.51579) | 6.24210 | (1, 1, 0.24283) |
| 8 | (6.24283, 6.24283, 1.51433) | 6.24283 | (1, 1, 0.24257) |
| 9 | (6.24257, 6.24257, 1.51486) | 6.24257 | (1, 1, 0.24267) |

The estimates settle at $6.243$ with vector $(1, 1, 0.2426)^T$.

$$\boxed{\lambda_{max} \approx 6.243,\qquad v \approx (1,\ 1,\ 0.243)^T}$$

**Exact check.** Rows 1 and 2 are symmetric, so $v = (1, 1, c)$. Row 3 gives $2 - 2c = \lambda c$, and row 1 gives $6 + c = \lambda$. Eliminating $\lambda$: $2 - 2c = (6 + c)c$, i.e. $c^2 + 8c - 2 = 0$, so $c = 3\sqrt2 - 4 = 0.2426$ and $\lambda = 6 + c = 2 + 3\sqrt2 = 6.2426$ ✓. The other eigenvalues are $-2$ and $2 - 3\sqrt2 = -2.243$, smaller in magnitude, so the iteration converges (ratio $2.243/6.243 \approx 0.36$).

@s 5
Take logarithms: $y = ae^{bx} \Rightarrow \ln y = \ln a + bx$. With $Y = \ln y$, $A = \ln a$ this is a straight line $Y = A + bx$ with normal equations

$$\begin{gathered}\sum Y = nA + b\sum x \\ \sum xY = A\sum x + b\sum x^2.\end{gathered}$$

| $x$ | $y$ | $Y = \ln y$ | $x^2$ | $xY$ |
|---|---|---|---|---|
| 2 | 4.1 | 1.41099 | 4 | 2.82197 |
| 4 | 11.2 | 2.41591 | 16 | 9.66366 |
| 6 | 30.2 | 3.40784 | 36 | 20.44705 |
| 8 | 81.9 | 4.40550 | 64 | 35.24399 |
| 10 | 204.6 | 5.32106 | 100 | 53.21060 |
| 12 | 802.8 | 6.68811 | 144 | 80.25728 |
| **Σ = 42** | | **23.64940** | **364** | **201.64455** |

With $n = 6$:

$$\begin{gathered}b = \frac{n\sum xY - \sum x\sum Y}{n\sum x^2 - (\sum x)^2} = \frac{6(201.6446) - 42(23.6494)}{6(364) - 42^2} = \frac{216.592}{420} = 0.51570\end{gathered}$$

$$\begin{gathered}A = \frac{23.6494 - 0.51570(42)}{6} = 0.33170 \\ a = e^{0.33170} = 1.3933\end{gathered}$$

$$\boxed{y = 1.393\,e^{0.5157\,x}}$$

*Remark.* The last point ($x = 12$, $y = 802.8$) lies well above the curve ($1.393e^{6.188} = 679$); the data are not perfectly exponential, so the fit in $\ln y$ is a compromise over all six points (it minimises the error in $\ln y$, not in $y$).

@s 6
**Divided differences** $f[x_i, \dots, x_{i+k}] = \dfrac{f[x_{i+1},\dots,x_{i+k}] - f[x_i,\dots,x_{i+k-1}]}{x_{i+k} - x_i}$.

| $x$ | $y$ | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|---|
| 0 | **4.72** | | | | |
| | | **1.19** | | | |
| 2 | 7.10 | | **−0.33** | | |
| | | −0.46 | | **0.06** | |
| 5 | 5.72 | | 0.09 | | **0** |
| | | −0.01 | | 0.06 | |
| 7 | 5.70 | | 0.45 | | 0 |
| | | 1.34 | | 0.06 | |
| 8 | 7.04 | | 0.75 | | |
| | | 3.59 | | | |
| 10 | 14.22 | | | | |

For example $\dfrac{7.1 - 4.72}{2} = 1.19$, $\dfrac{5.72 - 7.1}{3} = -0.46$, and $\dfrac{-0.46 - 1.19}{5} = -0.33$, $\dfrac{0.09 + 0.33}{7} = 0.06$.

The third differences are constant ($0.06$) and the fourth are $0$, so the data come from a **cubic**. Newton's divided-difference formula with the nodes $0, 2, 5, 7$:

$$y(x) = 4.72 + 1.19\,x - 0.33\,x(x-2) + 0.06\,x(x-2)(x-5)$$

At $x = 9$:

$$\begin{gathered}y(9) = 4.72 + 1.19(9) - 0.33(9)(7) + 0.06(9)(7)(4) = 4.72 + 10.71 - 20.79 + 15.12\end{gathered}$$

$$\boxed{y(9) = 9.76}$$

Expanded, $y = 0.06x^3 - 0.75x^2 + 2.45x + 4.72$, which reproduces every tabulated value (e.g. $y(10) = 14.22$ ✓). Using all six nodes adds terms with zero coefficient, so the answer is unchanged.

```figure caption="The data lie exactly on the cubic $y = 0.06x^3 - 0.75x^2 + 2.45x + 4.72$; the interpolated value $y(9) = 9.76$ is marked."
import numpy as np, matplotlib.pyplot as plt
xs=np.array([0,2,5,7,8,10]); ys=np.array([4.72,7.1,5.72,5.7,7.04,14.22])
x=np.linspace(0,10.5,300); p=lambda t:0.06*t**3-0.75*t**2+2.45*t+4.72
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(x,p(x),color=ACCENT); ax.plot(xs,ys,'o',color=INK,ms=4,label="data")
ax.plot([9],[p(9)],'s',color=SERIES[1],label="y(9) = 9.76")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(fontsize=7); ax.grid(True)
```

@s 7
Let the points be equally spaced, $x_i = x_0 + ih$, with forward differences $\Delta y_0, \Delta^2 y_0, \dots$ and $p = \dfrac{x - x_0}{h}$. **Newton's forward formula** is

$$y = y_0 + p\,\Delta y_0 + \frac{p(p-1)}{2!}\Delta^2 y_0 + \frac{p(p-1)(p-2)}{3!}\Delta^3 y_0 + \frac{p(p-1)(p-2)(p-3)}{4!}\Delta^4 y_0 + \cdots$$

Since $\dfrac{dp}{dx} = \dfrac1h$, differentiate term by term with respect to $p$. Expanding $p(p-1) = p^2 - p$, $p(p-1)(p-2) = p^3 - 3p^2 + 2p$, $p(p-1)(p-2)(p-3) = p^4 - 6p^3 + 11p^2 - 6p$:

**First derivative**

$$\begin{gathered}\frac{dy}{dx} = \frac{1}{h}\frac{dy}{dp} = \frac1h\left[\Delta y_0 + \frac{2p - 1}{2}\Delta^2 y_0 + \frac{3p^2 - 6p + 2}{6}\Delta^3 y_0 + \frac{4p^3 - 18p^2 + 22p - 6}{24}\Delta^4 y_0 + \cdots\right]\end{gathered}$$

**Second derivative**

$$\begin{gathered}\frac{d^2y}{dx^2} = \frac{1}{h^2}\frac{d^2y}{dp^2} = \frac1{h^2}\left[\Delta^2 y_0 + (p - 1)\Delta^3 y_0 + \frac{6p^2 - 18p + 11}{12}\Delta^4 y_0 + \cdots\right]\end{gathered}$$

**At the initial point** $x = x_0$ ($p = 0$) these reduce to the working formulas

$$\boxed{y'_0 = \frac1h\left[\Delta y_0 - \frac12\Delta^2 y_0 + \frac13\Delta^3 y_0 - \frac14\Delta^4 y_0 + \cdots\right]}$$

$$\boxed{y''_0 = \frac1{h^2}\left[\Delta^2 y_0 - \Delta^3 y_0 + \frac{11}{12}\Delta^4 y_0 - \frac56\Delta^5 y_0 + \cdots\right]}$$

(The next term in $y'_0$ is $+\tfrac15\Delta^5y_0$.) These formulas are most accurate near the start of the table; for the end of a table use Newton's backward formula.

@s 8
**Weddle's rule** (6 sub-intervals per block, so $n$ must be a multiple of 6; here $n = 12$ gives two blocks):

$$\int_{a}^{b} f\,dx \approx \frac{3h}{10}\Big[y_0 + 5y_1 + y_2 + 6y_3 + y_4 + 5y_5 + 2y_6 + 5y_7 + y_8 + 6y_9 + y_{10} + 5y_{11} + y_{12}\Big]$$

($y_6$ carries weight $1 + 1 = 2$ because it ends the first block and starts the second.) Here $h = \dfrac{1 - 0}{12} = \dfrac1{12}$ and $y = \dfrac{1}{1 + x}$:

| $i$ | $x_i$ | $y_i$ | weight |
|---|---|---|---|
| 0 | 0 | 1.000000 | 1 |
| 1 | 1/12 | 0.923077 | 5 |
| 2 | 2/12 | 0.857143 | 1 |
| 3 | 3/12 | 0.800000 | 6 |
| 4 | 4/12 | 0.750000 | 1 |
| 5 | 5/12 | 0.705882 | 5 |
| 6 | 6/12 | 0.666667 | 2 |
| 7 | 7/12 | 0.631579 | 5 |
| 8 | 8/12 | 0.600000 | 1 |
| 9 | 9/12 | 0.571429 | 6 |
| 10 | 10/12 | 0.545455 | 1 |
| 11 | 11/12 | 0.521739 | 5 |
| 12 | 1 | 0.500000 | 1 |

Weighted sum:

$$\begin{gathered}(y_0 + y_{12}) = 1.500000\\ 5(y_1 + y_5 + y_7 + y_{11}) = 5(2.782277) = 13.911385\\ (y_2 + y_4 + y_8 + y_{10}) = 2.752597\\ 6(y_3 + y_9) = 6(1.371429) = 8.228571\\ 2y_6 = 1.333333\end{gathered}$$

Total $= 27.725886$, so

$$\begin{gathered}I \approx \frac{3(1/12)}{10}(27.725886) = 0.025 \times 27.725886 = 0.693147\end{gathered}$$

$$\boxed{\int_0^1 \frac{dx}{1+x} \approx 0.693147}$$

The exact value is $\ln 2 = 0.693147$; the error is about $4\times10^{-8}$.

@s 9
**Second-order Runge-Kutta (Heun) method** for $y' = f(x, y)$, $y(x_0) = y_0$, step $h$:

$$\begin{gathered}k_1 = h\,f(x_i, y_i) \\ k_2 = h\,f(x_i + h,\ y_i + k_1) \\ y_{i+1} = y_i + \tfrac12(k_1 + k_2).\end{gathered}$$

```python
def rk2(f, x0, y0, xn, n):
    """Heun (second-order Runge-Kutta): y_{i+1} = y_i + (k1 + k2)/2."""
    h = (xn - x0) / n
    x, y = x0, y0
    table = [(x, y)]
    for _ in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h, y + k1)
        y += 0.5 * (k1 + k2)
        x += h
        table.append((x, y))
    return table

if __name__ == "__main__":
    expr = input("Enter f(x, y): ")
    x0 = float(input("x0 = ")); y0 = float(input("y0 = "))
    xn = float(input("xn = ")); n = int(input("number of steps n = "))
    f = lambda x, y: eval(expr)
    for x, y in rk2(f, x0, y0, xn, n):
        print(f"x = {x:.4f}   y = {y:.6f}")
```

**Test run** for $y' = x + y$, $y(0) = 1$ on $[0, 0.4]$ with $n = 4$ (the program was executed to obtain this output):

```
Enter f(x, y): x + y
x0 = 0
y0 = 1
xn = 0.4
number of steps n = 4
x = 0.0000   y = 1.000000
x = 0.1000   y = 1.110000
x = 0.2000   y = 1.242050
x = 0.3000   y = 1.398465
x = 0.4000   y = 1.581804
```

The exact solution $y = 2e^x - x - 1$ gives $y(0.4) = 1.583649$, so the error is $1.8\times10^{-3}$, as expected of a method of order $h^2$. The user supplies $f$ as a text expression; to use another equation only the first prompt changes. (To use the midpoint variant, replace $k_2$ by `h*f(x+h/2, y+k1/2)` and the update by `y += k2`.)

@s 10
**Finite-difference method.** On $0 \le x \le 2$ with four sub-intervals, $h = 0.5$ and the nodes are $x_0 = 0,\ x_1 = 0.5,\ x_2 = 1,\ x_3 = 1.5,\ x_4 = 2$. Replace

$$\begin{gathered}y''_i \approx \frac{y_{i+1} - 2y_i + y_{i-1}}{h^2} \\ y'_i \approx \frac{y_{i+1} - y_{i-1}}{2h}\end{gathered}$$

in $y'' + 5y' - 3y = \sin x$:

$$\Big(\frac1{h^2} - \frac5{2h}\Big)y_{i-1} + \Big(-\frac2{h^2} - 3\Big)y_i + \Big(\frac1{h^2} + \frac5{2h}\Big)y_{i+1} = \sin x_i$$

With $h = 0.5$: $\ \dfrac1{h^2} = 4,\ \dfrac5{2h} = 5$, giving $\ -y_{i-1} - 11\,y_i + 9\,y_{i+1} = \sin x_i$. Boundary values $y_0 = 2,\ y_4 = 4$.

$$\begin{gathered}i=1:\ \ -2 - 11y_1 + 9y_2 = \sin 0.5 \Rightarrow -11y_1 + 9y_2 = 2.479426\\ i=2:\ \ -y_1 - 11y_2 + 9y_3 = \sin 1 = 0.841471\\ i=3:\ \ -y_2 - 11y_3 + 36 = \sin 1.5 \Rightarrow -y_2 - 11y_3 = -35.002505\end{gathered}$$

Solving this tridiagonal system (Gauss elimination / Thomas algorithm):

$$\boxed{y(0.5) \approx 1.5890,\qquad y(1.0) \approx 2.2176,\qquad y(1.5) \approx 2.9804}$$

Check in the middle equation: $-1.5890 - 24.3936 + 26.8240 = 0.8414$ ✓.

```figure caption="Finite-difference solution of $y'' + 5y' - 3y = \sin x$, $y(0) = 2$, $y(2) = 4$ with $h = 0.5$."
import numpy as np, matplotlib.pyplot as plt
x=[0,0.5,1,1.5,2]; y=[2,1.588994,2.217596,2.980446,4]
fig,ax=plt.subplots(figsize=(5.2,2.5))
ax.plot(x,y,'-o',color=ACCENT,ms=4)
for a,b in zip(x[1:4],y[1:4]): ax.annotate(f"{b:.4f}",(a,b),textcoords="offset points",xytext=(0,-12),ha='center',fontsize=7.5)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.grid(True)
```

@s 11
**Laplace equation by the five-point formula.** For $h = k$, each interior value is the average of its four neighbours:

$$u_{i,j} = \tfrac14\left(u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1}\right).$$

The mesh has the four interior nodes $(1,1),\ (2,1),\ (1,2),\ (2,2)$. Boundary values from the data:

| Edge | values |
|---|---|
| $u(x, 0) = 100x$ | $u(0,0) = 0,\ u(1,0) = 100,\ u(2,0) = 200,\ u(3,0) = 300$ |
| $u(x, 3) = 200(3 - x)$ | $u(0,3) = 600,\ u(1,3) = 400,\ u(2,3) = 200,\ u(3,3) = 0$ |
| $u(0, y) = 200y$ | $u(0,1) = 200,\ u(0,2) = 400$ |
| $u(3, y) = 100(3 - y)$ | $u(3,1) = 200,\ u(3,2) = 100$ |

Let $a = u_{1,1},\ b = u_{2,1},\ c = u_{1,2},\ d = u_{2,2}$:

$$\begin{gathered}4a = 200 + b + 100 + c \ \Rightarrow\ 4a - b - c = 300\\ 4b = a + 200 + 200 + d \ \Rightarrow\ -a + 4b - d = 400\\ 4c = 400 + d + a + 400 \ \Rightarrow\ -a + 4c - d = 800\\ 4d = c + 100 + b + 200 \ \Rightarrow\ -b - c + 4d = 300\end{gathered}$$

Adding the first and last, and the middle two: with $S = a + d$ and $T = b + c$,

$$\begin{gathered}4S - 2T = 600 \\ -2S + 4T = 1200 \ \Rightarrow\ S = 400,\ T = 500.\end{gathered}$$

Subtracting the first and last: $4(a - d) = 0 \Rightarrow a = d = 200$. Subtracting the two middle equations: $4(c - b) = 400 \Rightarrow c - b = 100$, so $c = 300,\ b = 200$.

$$\boxed{u(1,1) = 200,\quad u(2,1) = 200,\quad u(1,2) = 300,\quad u(2,2) = 200}$$

Check at $(1,2)$: $\tfrac14(400 + 200 + 400 + 200) = 300$ ✓. (Gauss-Seidel from the starting guess $200$ everywhere converges to the same values.)

@s 12
**Crank-Nicolson scheme.** Average the central-difference form of $u_{xx}$ at the old and the new time level. With $r = \dfrac{\alpha\,k}{h^2}$ ($k = \Delta t$):

$$-r\,u_{i-1}^{j+1} + 2(1 + r)\,u_i^{j+1} - r\,u_{i+1}^{j+1} = r\,u_{i-1}^{j} + 2(1 - r)\,u_i^{j} + r\,u_{i+1}^{j}.$$

The scan gives $\alpha = 1$ and $h = 1$ but no $\Delta t$; the usual choice is $r = 1$ (i.e. $\Delta t = 1$), which makes the scheme

$$-u_{i-1}^{j+1} + 4u_i^{j+1} - u_{i+1}^{j+1} = u_{i-1}^{j} + u_{i+1}^{j}.$$

Interior nodes $x = 1, 2, 3$ ($u_0 = u_4 = 0$ always). Initial values $u(x,0) = x(4 - x)$: $\ u_1^0 = 3,\ u_2^0 = 4,\ u_3^0 = 3$.

**First time step** ($t = 1$). Right-hand sides: $0 + 4 = 4,\ 3 + 3 = 6,\ 4 + 0 = 4$.

$$\begin{gathered}4u_1 - u_2 = 4\\ -u_1 + 4u_2 - u_3 = 6\\ -u_2 + 4u_3 = 4\end{gathered}\quad\Rightarrow\quad u_1 = u_3 = 1.5714,\ \ u_2 = 2.2857$$

(by symmetry $u_1 = u_3$: $4u_1 - u_2 = 4$, $-2u_1 + 4u_2 = 6$.)

**Second time step** ($t = 2$). Right-hand sides: $0 + 2.2857 = 2.2857,\ 1.5714 + 1.5714 = 3.1429,\ 2.2857$.

$$\begin{gathered}4u_1 - u_2 = 2.2857 \\ -2u_1 + 4u_2 = 3.1429 \ \Rightarrow\ u_1 = u_3 = 0.8776,\ \ u_2 = 1.2245\end{gathered}$$

| $t$ | $u(1,t)$ | $u(2,t)$ | $u(3,t)$ |
|---|---|---|---|
| 0 | 3.0000 | 4.0000 | 3.0000 |
| 1 | 1.5714 | 2.2857 | 1.5714 |
| 2 | 0.8776 | 1.2245 | 0.8776 |

$$\boxed{u(1,2) = u(3,2) \approx 0.878,\qquad u(2,2) \approx 1.224}$$

The temperature decays smoothly and stays symmetric about $x = 2$, as the symmetric initial profile and boundary data require.

---
file: NEBians-IOE-Past-Paper-Engineering-Numerical-Methods-ENSH252-2082-Bhadra.pdf
subject: Numerical Methods
level: BE · Year II / Part II
code: ENSH 252
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (new course), BE (BEL, BEI, BCT, BAM, BIE, BAG, BGE, BCH). Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt All questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
Find a real root of the equation $3x + \sin x - e^x = 0$ using the bisection method correct to three decimal places. [[5]]

@q 2
Write the Jacobian matrix for the following system of equations and then use the Newton-Raphson method to approximate a solution correct to two decimal places. Take $(x_0, y_0) = (1, 1)$.
$$\begin{gathered}x^2 - \cos y = 5\\ \sin x + y^2 = 6\end{gathered}$$
[[5]]

@q 3
Solve the system of equations $2x - 3y + 10z = 3,\ -x + 4y + 2z = 20,\ 5x + 2y + z = -12$ by using Gauss elimination with partial pivoting. [[5]]

@q 4
Find the dominant eigenvalue and the corresponding eigenvector of the given matrix using the power method.
$$\begin{pmatrix} 1 & 6 & 2 \\ 3 & 5 & 2 \\ 1 & 1 & -2 \end{pmatrix}$$
[[5]]

@q 5
Using the least square method, fit the following set of data to a curve of the form $y = ab^x$.

| $x$ | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|
| $y$ | 16 | 11.1 | 8.7 | 6.4 | 4.7 | 1.6 |

[[5]]

@q 6
Using the cubic spline interpolation technique, estimate $y(7)$ from the following data.

| $x$ | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|
| $y$ | 2 | 5 | 8 | 6 | 9 |

[[5]]

@q 7
Given that

| $x$ | 1 | 1.1 | 1.2 | 1.3 | 1.4 | 1.5 |
|---|---|---|---|---|---|---|
| $y$ | 7.989 | 8.403 | 8.781 | 9.129 | 9.451 | 9.750 |

find $\dfrac{dy}{dx}$ and $\dfrac{d^2y}{dx^2}$ at $x = 1.1$. [[5]]

@q 8
Write a program code in Python to find the integral value of a given definite integral using Simpson's 3/8 rule. [[5]]

@q 9
Approximate $y$ and $z$ at $x = 1.0$ for the following initial value problem using the Runge-Kutta second order method taking $h = 0.5$.
$$\begin{gathered}\frac{dy}{dx} = \cos(xy) + xz \\ \frac{dz}{dx} = \sin(xz) + yz\end{gathered}$$
Given that $(x_0, y_0, z_0) = (0, 1, 1)$. [[5]]

@q 10
Solve the following boundary value problem using the finite difference method by dividing the interval into 4 sub-intervals.
$$\begin{gathered}y'' + 3y' - y = \cos(x) \\ y(0) = 2,\ y(2) = 3.\end{gathered}$$
[[5]]

@q 11
Solve $\dfrac{\partial^2 u}{\partial x^2} + \dfrac{\partial^2 u}{\partial y^2} = 0$ on the mesh bounded by $0 \le x \le 1,\ 0 \le y \le 1$ and $\Delta x = \Delta y = h = k = \dfrac13$. The boundary values are
$$\begin{gathered}u(x, 0) = 900x\\ u(x, 1) = 600(1 - x)\\ u(1, y) = 900(1 - y)\\ u(0, y) = 600y\end{gathered}$$
[[5]]

@q 12
Solve the one-dimensional heat equation $2u_t = u_{xx}$ for $0 \le t \le 4$ with $\Delta x = h = 1$ using the Bendre-Schmidt recurrence relation method with initial and boundary conditions:
$$\begin{gathered}u(x, 0) = x(5 - x)\\ u(0, t) = u(5, t) = 0\end{gathered}$$
[[5]]
<!-- SOLUTIONS -->

@s 1
**Idea.** If $f$ is continuous and $f(a)f(b) < 0$, a root lies in $(a, b)$. Bisection halves the interval each time: $c = \dfrac{a+b}{2}$, and keeps the half in which the sign change survives.

Let $f(x) = 3x + \sin x - e^x$ (radians).

$$\begin{gathered}f(0) = 0 + 0 - 1 = -1 < 0 \\ f(1) = 3 + 0.84147 - 2.71828 = +1.12319 > 0\end{gathered}$$

So a root lies in $(0, 1)$. For an answer correct to three decimal places the error must be below $0.0005$:

$$\frac{b - a}{2^n} < 0.0005 \ \Rightarrow\ 2^n > 2000\ \Rightarrow\ n \ge 11.$$

| $n$ | $a$ | $b$ | $c = (a+b)/2$ | $f(c)$ |
|---|---|---|---|---|
| 1 | 0 | 1 | 0.500000 | +0.330704 |
| 2 | 0 | 0.5 | 0.250000 | −0.286621 |
| 3 | 0.25 | 0.5 | 0.375000 | +0.036281 |
| 4 | 0.25 | 0.375 | 0.312500 | −0.121899 |
| 5 | 0.3125 | 0.375 | 0.343750 | −0.041956 |
| 6 | 0.34375 | 0.375 | 0.359375 | −0.002620 |
| 7 | 0.359375 | 0.375 | 0.367188 | +0.016886 |
| 8 | 0.359375 | 0.367188 | 0.363281 | +0.007147 |
| 9 | 0.359375 | 0.363281 | 0.361328 | +0.002267 |
| 10 | 0.359375 | 0.361328 | 0.360352 | −0.000175 |
| 11 | 0.360352 | 0.361328 | 0.360840 | +0.001046 |
| 12 | 0.360352 | 0.360840 | 0.360596 | +0.000435 |

After the 12th step the root is trapped in $[0.360352,\ 0.360596]$, so every number in it rounds to $0.360$.

$$\boxed{x \approx 0.360}\quad(\text{more precisely } 0.3604)$$

*Remark.* $f(1.5) = +1.017$ and $f(2) = -0.480$ show a second root in $(1.5, 2)$; the same procedure gives $x \approx 1.890$.

```figure caption="$f(x) = 3x + \sin x - e^x$ crosses the axis at $x \approx 0.360$ and $x \approx 1.890$."
import numpy as np, matplotlib.pyplot as plt
x=np.linspace(-0.3,2.3,400); f=3*x+np.sin(x)-np.exp(x)
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(x,f,color=ACCENT); ax.axhline(0,color=INK,lw=0.7)
for r in (0.3604,1.8900):
    ax.plot([r],[0],'o',color=SERIES[1]); ax.annotate(f"x = {r:.3f}",(r,0),textcoords="offset points",xytext=(0,9),ha='center',fontsize=7.5)
ax.set_xlabel("x"); ax.set_ylabel("f(x)"); ax.grid(True)
```

@s 2
Let $F_1 = x^2 - \cos y - 5$ and $F_2 = \sin x + y^2 - 6$. The **Jacobian matrix** is

$$J = \begin{pmatrix} \partial F_1/\partial x & \partial F_1/\partial y \\ \partial F_2/\partial x & \partial F_2/\partial y \end{pmatrix} = \begin{pmatrix} 2x & \sin y \\ \cos x & 2y \end{pmatrix}.$$

Each Newton-Raphson step solves $J\,\Delta = -F$ and updates $(x, y) \leftarrow (x, y) + \Delta$.

**Iteration 1**, $(x_0, y_0) = (1, 1)$: $F = (-4.540302,\ -4.158529)$,

$$\begin{pmatrix} 2 & 0.841471 \\ 0.540302 & 2 \end{pmatrix}\begin{pmatrix}\Delta x\\ \Delta y\end{pmatrix} = \begin{pmatrix}4.540302\\ 4.158529\end{pmatrix} \Rightarrow \Delta = (1.574265,\ 1.653975)$$

$$(x_1, y_1) = (2.574265,\ 2.653975)$$

**Iteration 2**: $F = (2.510293,\ 1.580963)$, $J = \begin{pmatrix} 5.148530 & 0.468523 \\ -0.843340 & 5.307950\end{pmatrix}$, $\Delta = (-0.453907,\ -0.369966)$,

$$(x_2, y_2) = (2.120358,\ 2.284009)$$

**Iteration 3**: $F = (0.150184,\ 0.069450)$, $J = \begin{pmatrix} 4.240716 & 0.756264 \\ -0.522313 & 4.568018\end{pmatrix}$, $\Delta = (-0.032050,\ -0.018868)$,

$$(x_3, y_3) = (2.088308,\ 2.265141)$$

**Iteration 4**: $F = (0.000912,\ -0.000085)$, $\Delta = (-0.000217,\ -0.000005)$,

$$(x_4, y_4) = (2.088091,\ 2.265136)$$

| Iter | $x$ | $y$ | $F_1$ | $F_2$ |
|---|---|---|---|---|
| 0 | 1.000000 | 1.000000 | −4.540302 | −4.158529 |
| 1 | 2.574265 | 2.653975 | 2.510293 | 1.580963 |
| 2 | 2.120358 | 2.284009 | 0.150184 | 0.069450 |
| 3 | 2.088308 | 2.265141 | 0.000912 | −0.000085 |
| 4 | 2.088091 | 2.265136 | 0.000000 | 0.000000 |

Iterates 3 and 4 agree to two decimals.

$$\boxed{x \approx 2.09,\qquad y \approx 2.27}$$

@s 3
**Gauss elimination with partial pivoting.** In each column the entry of largest magnitude on or below the diagonal is swapped to the pivot position before eliminating, to keep the multipliers $\le 1$.

Augmented matrix:

$$\left[\begin{array}{ccc|c} 2 & -3 & 10 & 3 \\ -1 & 4 & 2 & 20 \\ 5 & 2 & 1 & -12 \end{array}\right]$$

**Column 1.** The largest entry is $5$ (row 3): swap $R_1 \leftrightarrow R_3$.

$$\left[\begin{array}{ccc|c} 5 & 2 & 1 & -12 \\ -1 & 4 & 2 & 20 \\ 2 & -3 & 10 & 3 \end{array}\right]$$

Multipliers $m_{21} = -1/5 = -0.2$ and $m_{31} = 2/5 = 0.4$: $R_2 \to R_2 + 0.2R_1$, $R_3 \to R_3 - 0.4R_1$:

$$\left[\begin{array}{ccc|c} 5 & 2 & 1 & -12 \\ 0 & 4.4 & 2.2 & 17.6 \\ 0 & -3.8 & 9.6 & 7.8 \end{array}\right]$$

**Column 2.** $|4.4| > |-3.8|$, so no swap. $m_{32} = -3.8/4.4 = -0.863636$: $R_3 \to R_3 + 0.863636\,R_2$:

$$\left[\begin{array}{ccc|c} 5 & 2 & 1 & -12 \\ 0 & 4.4 & 2.2 & 17.6 \\ 0 & 0 & 11.5 & 23 \end{array}\right]$$

**Back substitution**

$$\begin{gathered}z = \frac{23}{11.5} = 2\\ y = \frac{17.6 - 2.2(2)}{4.4} = 3\\ x = \frac{-12 - 2(3) - 1(2)}{5} = -4\end{gathered}$$

Check: $2(-4) - 3(3) + 10(2) = 3$ ✓; $4 + 12 + 4 = 20$ ✓; $-20 + 6 + 2 = -12$ ✓.

$$\boxed{x = -4,\qquad y = 3,\qquad z = 2}$$

@s 4
**Power method.** Start with $x^{(0)} = (1, 1, 1)^T$. Repeat $y = Ax^{(k)}$, $\lambda_k = $ the entry of $y$ of largest magnitude, $x^{(k+1)} = y/\lambda_k$.

| $k$ | $Ax^{(k)}$ | $\lambda_k$ | $x^{(k+1)}$ |
|---|---|---|---|
| 0 | (9, 10, 0) | 10 | (0.90000, 1, 0) |
| 1 | (6.90000, 7.70000, 1.90000) | 7.70000 | (0.89610, 1, 0.24675) |
| 2 | (7.38961, 8.18182, 1.40260) | 8.18182 | (0.90317, 1, 0.17143) |
| 3 | (7.24603, 8.05238, 1.56032) | 8.05238 | (0.89986, 1, 0.19377) |
| 4 | (7.28740, 8.08713, 1.51232) | 8.08713 | (0.90111, 1, 0.18700) |
| 5 | (7.27512, 8.07734, 1.52711) | 8.07734 | (0.90068, 1, 0.18906) |
| 6 | (7.27880, 8.08017, 1.52256) | 8.08017 | (0.90082, 1, 0.18843) |
| 7 | (7.27769, 8.07933, 1.52396) | 8.07933 | (0.90078, 1, 0.18862) |
| 8 | (7.27803, 8.07958, 1.52353) | 8.07958 | (0.90079, 1, 0.18857) |
| 9 | (7.27792, 8.07951, 1.52366) | 8.07951 | (0.90079, 1, 0.18858) |

The estimates settle at $8.080$ and the vector at $(0.9008, 1, 0.1886)^T$.

$$\boxed{\lambda_{max} \approx 8.080,\qquad v \approx (0.901,\ 1,\ 0.189)^T}$$

**Check.** $A v = (7.2779,\ 8.0795,\ 1.5236)^T = 8.0795\,(0.9008,\ 1,\ 0.1886)^T$ ✓. The other eigenvalues are $-1.593$ and $-2.487$, so the convergence ratio is $2.487/8.080 \approx 0.31$ and the iteration converges quickly.

@s 5
Take logarithms to base 10: $y = ab^x \Rightarrow \log y = \log a + x\log b$. With $Y = \log y$, $A = \log a$, $B = \log b$ this is the straight line $Y = A + Bx$, with normal equations

$$\begin{gathered}\sum Y = nA + B\sum x \\ \sum xY = A\sum x + B\sum x^2.\end{gathered}$$

| $x$ | $y$ | $Y = \log y$ | $x^2$ | $xY$ |
|---|---|---|---|---|
| 2 | 16 | 1.20412 | 4 | 2.40824 |
| 4 | 11.1 | 1.04532 | 16 | 4.18129 |
| 6 | 8.7 | 0.93952 | 36 | 5.63711 |
| 8 | 6.4 | 0.80618 | 64 | 6.44944 |
| 10 | 4.7 | 0.67210 | 100 | 6.72098 |
| 12 | 1.6 | 0.20412 | 144 | 2.44944 |
| **Σ = 42** | | **4.87136** | **364** | **27.84650** |

With $n = 6$:

$$B = \frac{6(27.8465) - 42(4.87136)}{6(364) - 42^2} = \frac{-37.518}{420} = -0.089329$$

$$A = \frac{4.87136 + 0.089329(42)}{6} = 1.43720$$

Therefore $a = 10^{1.43720} = 27.365$ and $b = 10^{-0.089329} = 0.8141$.

$$\boxed{y = 27.37\,(0.8141)^x}$$

(Equivalently $y = 27.37\,e^{-0.2057x}$.) The curve is a decay; the last point ($x = 12$, $y = 1.6$) lies below the fit, which gives $2.3$ there.

```figure caption="Data and the least-squares curve $y = 27.37(0.8141)^x$."
import numpy as np, matplotlib.pyplot as plt
X=np.array([2,4,6,8,10,12]); Y=np.array([16,11.1,8.7,6.4,4.7,1.6])
x=np.linspace(1,13,200)
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(x,27.365*0.8141**x,color=ACCENT,label="y = 27.37 (0.8141)^x"); ax.plot(X,Y,'o',color=INK,ms=4,label="data")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(fontsize=7); ax.grid(True)
```

@s 6
**Natural cubic spline.** Nodes $x_i = 4, 6, 8, 10, 12$ with $h = 2$, $y = 2, 5, 8, 6, 9$. Let $M_i = S''(x_i)$; natural end conditions $M_0 = M_4 = 0$. For equal spacing the spline condition (continuity of $S'$) gives

$$\begin{gathered}M_{i-1} + 4M_i + M_{i+1} = \frac{6}{h^2}\left(y_{i-1} - 2y_i + y_{i+1}\right) \\ i = 1, 2, 3.\end{gathered}$$

The right-hand sides ($6/h^2 = 1.5$):

$$\begin{gathered}i=1:\ 1.5(2 - 10 + 8) = 0\\ i=2:\ 1.5(5 - 16 + 6) = -7.5\\ i=3:\ 1.5(8 - 12 + 9) = 7.5\end{gathered}$$

$$\begin{gathered}4M_1 + M_2 = 0\\ M_1 + 4M_2 + M_3 = -7.5\\ M_2 + 4M_3 = 7.5\end{gathered}\quad\Rightarrow\quad M_1 = 0.669643,\ \ M_2 = -2.678571,\ \ M_3 = 2.544643$$

($M_1 = -M_2/4,\ M_3 = (7.5 - M_2)/4$, then $3.5M_2 = -9.375$.)

$x = 7$ lies in $[x_1, x_2] = [6, 8]$, where

$$S(x) = M_1\frac{(8 - x)^3}{6h} + M_2\frac{(x - 6)^3}{6h} + \left(\frac{y_1}{h} - \frac{M_1h}{6}\right)(8 - x) + \left(\frac{y_2}{h} - \frac{M_2h}{6}\right)(x - 6).$$

At $x = 7$:

$$S(7) = \frac{0.669643}{12} + \frac{-2.678571}{12} + \left(2.5 - 0.223214\right) + \left(4 + 0.892857\right)$$

$$= 0.055804 - 0.223214 + 2.276786 + 4.892857 = 7.0022$$

$$\boxed{y(7) \approx 7.002}$$

*Remark.* With "not-a-knot" end conditions instead of natural ones the value would be $7.047$; the natural spline is the standard choice in this syllabus.

```figure caption="Natural cubic spline through the five data points; the estimate $y(7) \approx 7.002$ is marked."
import numpy as np, matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
xs=[4,6,8,10,12]; ys=[2,5,8,6,9]; cs=CubicSpline(xs,ys,bc_type='natural')
x=np.linspace(4,12,300)
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(x,cs(x),color=ACCENT); ax.plot(xs,ys,'o',color=INK,ms=4,label="data")
ax.plot([7],[cs(7)],'s',color=SERIES[1],label="y(7) = 7.002")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(fontsize=7); ax.grid(True)
```

@s 7
The nodes are equally spaced ($h = 0.1$) and $x = 1.1$ is a tabulated point, so use Newton's forward-difference derivative formulas with $x_0 = 1.0$ and $p = \dfrac{1.1 - 1.0}{0.1} = 1$.

| $x$ | $y$ | $\Delta y$ | $\Delta^2 y$ | $\Delta^3 y$ | $\Delta^4 y$ | $\Delta^5 y$ |
|---|---|---|---|---|---|---|
| 1.0 | 7.989 | 0.414 | −0.036 | 0.006 | −0.002 | 0.001 |
| 1.1 | 8.403 | 0.378 | −0.030 | 0.004 | −0.001 | |
| 1.2 | 8.781 | 0.348 | −0.026 | 0.003 | | |
| 1.3 | 9.129 | 0.322 | −0.023 | | | |
| 1.4 | 9.451 | 0.299 | | | | |
| 1.5 | 9.750 | | | | | |

$$\frac{dy}{dx} = \frac1h\left[\Delta y_0 + \frac{2p-1}{2}\Delta^2y_0 + \frac{3p^2 - 6p + 2}{6}\Delta^3y_0 + \frac{4p^3 - 18p^2 + 22p - 6}{24}\Delta^4y_0 + \frac{5p^4 - 40p^3 + 105p^2 - 100p + 24}{120}\Delta^5y_0\right]$$

At $p = 1$ the coefficients are $\tfrac12,\ -\tfrac16,\ \tfrac1{12},\ -\tfrac1{20}$:

$$\frac{dy}{dx}\Big|_{1.1} = \frac1{0.1}\left[0.414 + \tfrac12(-0.036) - \tfrac16(0.006) + \tfrac1{12}(-0.002) - \tfrac1{20}(0.001)\right] = 10\,[0.414 - 0.018 - 0.001 - 0.000167 - 0.00005]$$

$$\frac{d^2y}{dx^2} = \frac1{h^2}\left[\Delta^2y_0 + (p-1)\Delta^3y_0 + \frac{6p^2 - 18p + 11}{12}\Delta^4y_0 + \frac{2p^3 - 12p^2 + 21p - 10}{12}\Delta^5y_0\right]$$

At $p = 1$ the coefficients are $0,\ -\tfrac1{12},\ \tfrac1{12}$:

$$\frac{d^2y}{dx^2}\Big|_{1.1} = \frac1{0.01}\left[-0.036 + 0 - \tfrac1{12}(-0.002) + \tfrac1{12}(0.001)\right] = 100\,[-0.036 + 0.000167 + 0.000083]$$

$$\boxed{\frac{dy}{dx}\Big|_{x=1.1} \approx 3.948,\qquad \frac{d^2y}{dx^2}\Big|_{x=1.1} \approx -3.575}$$

**Check.** Central differences about $x = 1.1$ give $\dfrac{8.781 - 7.989}{0.2} = 3.96$ and $\dfrac{8.781 - 2(8.403) + 7.989}{0.01} = -3.60$, in agreement to the accuracy of that lower-order formula. (Starting the forward formulas at $x_0 = 1.1$, $p = 0$, with the four available differences gives $3.946$ and $-3.492$.)

@s 8
**Simpson's 3/8 rule.** Fit a cubic through each group of four points. For $n$ sub-intervals ($n$ a multiple of 3), $h = \dfrac{b - a}{n}$:

$$\int_a^b f\,dx \approx \frac{3h}{8}\Big[y_0 + y_n + 3(y_1 + y_2 + y_4 + y_5 + \cdots) + 2(y_3 + y_6 + \cdots)\Big]$$

Weights follow the pattern $1,\ 3,\ 3,\ 2,\ 3,\ 3,\ 2,\ \dots,\ 3,\ 3,\ 1$: every third interior ordinate gets weight $2$, the other interior ordinates get $3$.

```python
import math

def simpson38(f, a, b, n):
    """Composite Simpson's 3/8 rule; n must be a multiple of 3."""
    if n % 3 != 0:
        raise ValueError("n must be a multiple of 3")
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (2 if i % 3 == 0 else 3) * f(a + i * h)
    return 3 * h / 8 * s

if __name__ == "__main__":
    expr = input("f(x) = ")
    a = float(input("lower limit a = ")); b = float(input("upper limit b = "))
    n = int(input("number of sub-intervals n (multiple of 3) = "))
    f = lambda x: eval(expr, {"math": math, "x": x, **vars(math)})
    print(f"Integral = {simpson38(f, a, b, n):.6f}")
```

**Test run** for $\int_0^{\pi}\sin x\,dx$ with $n = 6$ (the program was executed to obtain this output):

```
f(x) = sin(x)
lower limit a = 0
upper limit b = 3.141592653589793
number of sub-intervals n (multiple of 3) = 6
Integral = 2.002010
```

The exact value is $2$, so the error is $2\times10^{-3}$ for $h = \pi/6$ (error $\propto h^4$). Any expression in $x$ (using `sin`, `exp`, `log`, ...) may be typed at the first prompt.

@s 9
**Second-order Runge-Kutta (Heun) for a system.** For $y' = f(x, y, z)$, $z' = g(x, y, z)$:

$$\begin{gathered}k_1 = h f(x_i, y_i, z_i),\qquad l_1 = h g(x_i, y_i, z_i)\\ k_2 = h f(x_i + h,\ y_i + k_1,\ z_i + l_1),\qquad l_2 = h g(x_i + h,\ y_i + k_1,\ z_i + l_1)\\ y_{i+1} = y_i + \tfrac12(k_1 + k_2),\qquad z_{i+1} = z_i + \tfrac12(l_1 + l_2)\end{gathered}$$

with $f = \cos(xy) + xz$ and $g = \sin(xz) + yz$, $h = 0.5$.

**Step 1** ($x_0 = 0,\ y_0 = 1,\ z_0 = 1$):

$$\begin{gathered}k_1 = 0.5[\cos 0 + 0] = 0.5,\qquad l_1 = 0.5[\sin 0 + 1] = 0.5\\ k_2 = 0.5[\cos(0.5\times1.5) + 0.5\times1.5] = 0.5(1.481689) = 0.740844\\ l_2 = 0.5[\sin(0.75) + 1.5\times1.5] = 0.5(2.931639) = 1.465819\end{gathered}$$

$$\begin{gathered}y_1 = 1 + \tfrac12(0.5 + 0.740844) = 1.620422 \\ z_1 = 1 + \tfrac12(0.5 + 1.465819) = 1.982910.\end{gathered}$$

**Step 2** ($x_1 = 0.5,\ y_1 = 1.620422,\ z_1 = 1.982910$):

$$\begin{gathered}k_1 = 0.5[\cos(0.810211) + 0.991455] = 0.5(1.680801) = 0.840400\\ l_1 = 0.5[\sin(0.991455) + 3.213151] = 0.5(4.049974) = 2.024987\\ k_2 = 0.5[\cos(2.460822) + 4.007897] = 0.5(3.230809) = 1.615404\\ l_2 = 0.5[\sin(4.007897) + 9.862721] = 0.5(9.100780) = 4.550390\end{gathered}$$

(for $k_2, l_2$ the arguments are $x = 1,\ y = 1.620422 + 0.840400 = 2.460822,\ z = 1.982910 + 2.024987 = 4.007897$.)

$$y_2 = 1.620422 + \tfrac12(0.840400 + 1.615404) = 2.848324$$

$$z_2 = 1.982910 + \tfrac12(2.024987 + 4.550391) = 5.270599$$

| $x$ | $y$ | $z$ |
|---|---|---|
| 0 | 1 | 1 |
| 0.5 | 1.620422 | 1.982910 |
| 1.0 | 2.848324 | 5.270599 |

$$\boxed{y(1.0) \approx 2.848,\qquad z(1.0) \approx 5.271}$$

*Remarks.* With $h = 0.5$ the RK2 estimate is coarse because $z$ grows quickly; the midpoint variant of RK2 gives $y = 2.749,\ z = 5.336$, and a high-accuracy integration gives $y(1) = 3.189,\ z(1) = 7.095$. Halving $h$ repeatedly brings RK2 towards these values.

@s 10
**Finite-difference method.** $0 \le x \le 2$ with four sub-intervals gives $h = 0.5$ and nodes $x = 0,\ 0.5,\ 1,\ 1.5,\ 2$. With

$$\begin{gathered}y''_i \approx \frac{y_{i+1} - 2y_i + y_{i-1}}{h^2} \\ y'_i \approx \frac{y_{i+1} - y_{i-1}}{2h}\end{gathered}$$

the equation $y'' + 3y' - y = \cos x$ becomes

$$\Big(\frac1{h^2} - \frac3{2h}\Big)y_{i-1} + \Big(-\frac2{h^2} - 1\Big)y_i + \Big(\frac1{h^2} + \frac3{2h}\Big)y_{i+1} = \cos x_i.$$

For $h = 0.5$: $\dfrac1{h^2} = 4$ and $\dfrac3{2h} = 3$, so $\ y_{i-1} - 9y_i + 7y_{i+1} = \cos x_i$, with $y_0 = 2,\ y_4 = 3$.

$$\begin{gathered}i=1:\ \ 2 - 9y_1 + 7y_2 = \cos 0.5 \Rightarrow -9y_1 + 7y_2 = -1.122417\\ i=2:\ \ y_1 - 9y_2 + 7y_3 = \cos 1 = 0.540302\\ i=3:\ \ y_2 - 9y_3 + 21 = \cos 1.5 \Rightarrow y_2 - 9y_3 = -20.929263\end{gathered}$$

Solving the tridiagonal system:

$$\boxed{y(0.5) \approx 1.7820,\qquad y(1.0) \approx 2.1308,\qquad y(1.5) \approx 2.5622}$$

Check in the middle equation: $1.7820 - 19.1773 + 17.9356 = 0.5403$ ✓.

```figure caption="Finite-difference solution of $y'' + 3y' - y = \cos x$, $y(0) = 2$, $y(2) = 3$ with $h = 0.5$."
import numpy as np, matplotlib.pyplot as plt
x=[0,0.5,1,1.5,2]; y=[2,1.782013,2.130814,2.562231,3]
fig,ax=plt.subplots(figsize=(5.2,2.5))
ax.plot(x,y,'-o',color=ACCENT,ms=4)
for a,b in zip(x[1:4],y[1:4]): ax.annotate(f"{b:.4f}",(a,b),textcoords="offset points",xytext=(0,-12),ha='center',fontsize=7.5)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.grid(True)
```

@s 11
**Laplace equation, five-point formula.** With $h = k = \tfrac13$ the mesh has four interior nodes. Each satisfies $u_{i,j} = \tfrac14(u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1})$. Boundary values (in units of the grid, $x, y \in \{0, \tfrac13, \tfrac23, 1\}$):

| Edge | values |
|---|---|
| $u(x, 0) = 900x$ | $0,\ 300,\ 600,\ 900$ |
| $u(x, 1) = 600(1 - x)$ | $600,\ 400,\ 200,\ 0$ |
| $u(0, y) = 600y$ | $u(0,\tfrac13) = 200,\ u(0,\tfrac23) = 400$ |
| $u(1, y) = 900(1 - y)$ | $u(1,\tfrac13) = 600,\ u(1,\tfrac23) = 300$ |

Let $a = u(\tfrac13,\tfrac13),\ b = u(\tfrac23,\tfrac13),\ c = u(\tfrac13,\tfrac23),\ d = u(\tfrac23,\tfrac23)$:

$$\begin{gathered}4a = 200 + b + 300 + c \ \Rightarrow\ 4a - b - c = 500\\ 4b = a + 600 + 600 + d \ \Rightarrow\ -a + 4b - d = 1200\\ 4c = 400 + d + a + 400 \ \Rightarrow\ -a + 4c - d = 800\\ 4d = c + 300 + b + 200 \ \Rightarrow\ -b - c + 4d = 500\end{gathered}$$

With $S = a + d$ and $T = b + c$: adding the first and last gives $4S - 2T = 1000$, adding the middle two gives $-2S + 4T = 2000$, so $T = 833.33$, $S = 666.67$. Subtracting the first and last: $a = d$, so $a = d = 333.33$. Subtracting the middle two: $4(c - b) = -400$, so $c = b - 100$, hence $b = 466.67,\ c = 366.67$.

$$\boxed{u(\tfrac13,\tfrac13) = 333.33,\quad u(\tfrac23,\tfrac13) = 466.67,\quad u(\tfrac13,\tfrac23) = 366.67,\quad u(\tfrac23,\tfrac23) = 333.33}$$

Check at $(\tfrac23,\tfrac13)$: $\tfrac14(333.33 + 600 + 600 + 333.33) = 466.67$ ✓.

@s 12
**Bendre-Schmidt method.** The explicit scheme for $u_t = \alpha^2u_{xx}$ is

$$\begin{gathered}u_i^{j+1} = \lambda u_{i-1}^j + (1 - 2\lambda)u_i^j + \lambda u_{i+1}^j \\ \lambda = \frac{\alpha^2 k}{h^2}\end{gathered}$$

which is stable for $\lambda \le \tfrac12$. Choosing $\lambda = \tfrac12$ gives the **Bendre-Schmidt recurrence**

$$u_i^{j+1} = \tfrac12\left(u_{i-1}^j + u_{i+1}^j\right).$$

Here $2u_t = u_{xx}$ means $u_t = \tfrac12u_{xx}$, so $\alpha^2 = \tfrac12$, and $\lambda = \tfrac12$ with $h = 1$ requires the time step $k = \dfrac{\lambda h^2}{\alpha^2} = 1$. Thus $0 \le t \le 4$ is **four** time steps. Interior nodes $x = 1, 2, 3, 4$, with $u_0 = u_5 = 0$.

Initial values $u(x, 0) = x(5 - x)$: $\ 4,\ 6,\ 6,\ 4$ at $x = 1, 2, 3, 4$.

| $t$ | $u(0)$ | $u(1)$ | $u(2)$ | $u(3)$ | $u(4)$ | $u(5)$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 4 | 6 | 6 | 4 | 0 |
| 1 | 0 | 3 | 5 | 5 | 3 | 0 |
| 2 | 0 | 2.5 | 4 | 4 | 2.5 | 0 |
| 3 | 0 | 2 | 3.25 | 3.25 | 2 | 0 |
| 4 | 0 | 1.625 | 2.625 | 2.625 | 1.625 | 0 |

For example, $u(1, 1) = \tfrac12(0 + 6) = 3$, $u(2, 1) = \tfrac12(4 + 6) = 5$; $u(1, 2) = \tfrac12(0 + 5) = 2.5$, $u(2, 2) = \tfrac12(3 + 5) = 4$; $u(2, 4) = \tfrac12(2 + 3.25) = 2.625$.

$$\boxed{u(x, 4) = 1.625,\ 2.625,\ 2.625,\ 1.625\quad(x = 1, 2, 3, 4)}$$

```figure caption="Temperature profiles at $t = 0, 1, 2, 3, 4$ from the Bendre-Schmidt recurrence; the profile decays and stays symmetric about $x = 2.5$."
import numpy as np, matplotlib.pyplot as plt
u=np.array([0,4,6,6,4,0.]); fig,ax=plt.subplots(figsize=(5.2,2.6)); x=np.arange(6)
for t in range(5):
    ax.plot(x,u,'-o',ms=3,color=SERIES[t%len(SERIES)],label=f"t = {t}")
    un=u.copy()
    for i in range(1,5): un[i]=(u[i-1]+u[i+1])/2
    u=un
ax.set_xlabel("x"); ax.set_ylabel("u(x, t)"); ax.legend(fontsize=7,ncol=5); ax.grid(True)
```

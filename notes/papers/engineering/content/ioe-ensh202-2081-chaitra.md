---
file: NEBians-IOE-Past-Paper-Engineering-Numerical-Methods-ENSH202-2081-Chaitra.pdf
subject: Numerical Methods
level: BE · Year II / Part I
code: ENSH 202
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
Find a real root of $e^{0.5x+3} + \cos(0.4x) - 50 = 0$ precise to 4 significant figures using the bisection method. [[5]]

@q 2
Write Jacobian matrix for the following system of non-linear equations and use Newton-Raphson method to approximate a solution correct to two decimal places taking $(x_0, y_0) = (2, 1)$ as initial guess values.
$$x^3 - y^2 = 8$$
$$x^2 + y^3 = 6$$
[[5]]

@q 3
Solve the following system of linear equations using Do-Little's Factorization method.
$$\begin{pmatrix} 2 & 5 & 4 \\ 3 & 4 & 5 \\ 5 & 4 & 4 \end{pmatrix}\begin{pmatrix} x \\ y \\ z \end{pmatrix} = \begin{pmatrix} 24 \\ 28 \\ 32 \end{pmatrix}$$
[[5]]

@q 4
Find dominant eigen value and corresponding vector of the given matrix using the power method.
$$\begin{pmatrix} 2 & 4 & 1 \\ 4 & 2 & 1 \\ 1 & 1 & -2 \end{pmatrix}$$
[[5]]

@q 5
Construct divided difference table from the following data and use Newton's divided difference interpolation technique to approximate $y(9)$.

| $x$ | 0 | 2 | 5 | 7 | 8 | 10 |
|---|---|---|---|---|---|---|
| $y$ | 4.72 | 7.1 | 5.72 | 5.7 | 7.04 | 14.22 |

[[5]]

@q 6
Using the least square method, fit the following data to a curve of the form $y = ae^{bx}$.

| $x$ | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| $y$ | 4.1 | 11.2 | 30.2 | 81.9 | 204.6 |

[[5]]

@q 7
Evaluate the following integral using Gauss-Legendre 3-point formula and compare the result with exact value of the integral.
$$\int_0^4\left(\cos\left(\frac{\pi x}{2}\right) + 5\right)dx$$
[[5]]

@q 8
Derive the expressions to evaluate first and second order derivatives from a set of tabulated data using Newton's forward interpolation formula. Also derive the expressions for the initial point. [[5]]

@q 9
Write a python program to solve an initial value problem involving a first order ordinary differential equation using Runge-Kutta fourth order method. The program should also show the results graphically. [[5]]

@q 10
Using finite difference method, solve the following boundary value problem for three internal nodes.
$$\begin{gathered}y'' - 5y' + 4y = 5x \\ y(2) = 4,\quad y(4) = 5\end{gathered}$$
[[5]]

@q 11
Solve the Laplace equation $u_{xx} + u_{yy} = 0$ for a square mesh with the following boundary conditions using the finite difference method employing Gauss-Seidel iteration method to solve the equations.
$$\begin{gathered}0 \le x \le 1,\quad 0 \le y \le 1,\quad \Delta x = \Delta y = h = 1/3\\ u(x, 0) = 360x,\qquad u(x, 1) = 240(1 - x)\\ u(0, y) = 240y,\qquad u(1, y) = 360(1 - y)\end{gathered}$$
[[5]]

@q 12
Derive the recurrence relation for solving one dimensional heat equation using Bender-Schmidt method and use it to solve the following problem for five time steps taking $\Delta x = h = 1$.
$$\begin{gathered}u_t = 0.5\,u_{xx} \\ u(0, t) = u(4, t) = 0 \\ u(x, 0) = 2x(4 - x)\end{gathered}$$
[[5]]
<!-- SOLUTIONS -->

@s 1
Let $f(x) = e^{0.5x + 3} + \cos(0.4x) - 50$ (radians). Since $e^{0.5x+3} \approx 50$ needs $0.5x + 3 \approx \ln 50 = 3.91$, the root is near $x \approx 1.8$.

$$f(1) = e^{3.5} + \cos 0.4 - 50 = 33.1155 + 0.9211 - 50 = -15.9635 < 0$$

$$f(2) = e^{4} + \cos 0.8 - 50 = 54.5982 + 0.6967 - 50 = +5.2949 > 0$$

A root lies in $(1, 2)$. Four significant figures of a number between $1$ and $10$ means three decimals, so the error must be $< 0.0005$:

$$\frac{b - a}{2^n} < 0.0005 \Rightarrow 2^n > 2000 \Rightarrow n \ge 11.$$

| $n$ | $a$ | $b$ | $c$ | $f(c)$ |
|---|---|---|---|---|
| 1 | 1 | 2 | 1.500000 | −6.65358 |
| 2 | 1.5 | 2 | 1.750000 | −1.05246 |
| 3 | 1.75 | 2 | 1.875000 | +2.02190 |
| 4 | 1.75 | 1.875 | 1.812500 | +0.46068 |
| 5 | 1.75 | 1.8125 | 1.781250 | −0.30180 |
| 6 | 1.78125 | 1.8125 | 1.796875 | +0.07795 |
| 7 | 1.78125 | 1.796875 | 1.789063 | −0.11230 |
| 8 | 1.789063 | 1.796875 | 1.792969 | −0.01727 |
| 9 | 1.792969 | 1.796875 | 1.794922 | +0.03032 |
| 10 | 1.792969 | 1.794922 | 1.793945 | +0.00652 |
| 11 | 1.792969 | 1.793945 | 1.793457 | −0.00538 |
| 12 | 1.793457 | 1.793945 | 1.793701 | +0.00057 |

The root is bracketed in $[1.793457,\ 1.793701]$, whose points all round to $1.794$.

$$\boxed{x \approx 1.794}\quad(\text{to 4 significant figures; more precisely } 1.7937)$$

@s 2
$F_1 = x^3 - y^2 - 8$, $F_2 = x^2 + y^3 - 6$.

$$J = \begin{pmatrix} 3x^2 & -2y \\ 2x & 3y^2 \end{pmatrix},\qquad J\,\Delta = -F,\qquad (x, y) \leftarrow (x, y) + \Delta.$$

**Iteration 1**, $(2, 1)$: $F = (-1, -1)$, $J = \begin{pmatrix} 12 & -2 \\ 4 & 3\end{pmatrix}$:

$$12\Delta x - 2\Delta y = 1,\quad 4\Delta x + 3\Delta y = 1 \Rightarrow \Delta x = \tfrac{5}{44} = 0.11364,\ \Delta y = \tfrac{8}{44} = 0.18182$$

$$(x_1, y_1) = (2.11364,\ 1.18182)$$

**Iteration 2**: $F = (0.04589,\ 0.11810)$, $J = \begin{pmatrix} 13.4024 & -2.3636 \\ 4.2273 & 4.1901\end{pmatrix}$ gives $\Delta = (-0.00713,\ -0.02100)$:

$$(x_2, y_2) = (2.10651,\ 1.16082)$$

**Iteration 3**: $F = (-0.00012,\ 0.00160)$, $\Delta = (-0.00005,\ -0.00034)$:

$$(x_3, y_3) = (2.10646,\ 1.16048)$$

**Iteration 4**: $F \approx 0$, no further change.

| Iter | $x$ | $y$ | $F_1$ | $F_2$ |
|---|---|---|---|---|
| 0 | 2.00000 | 1.00000 | −1.00000 | −1.00000 |
| 1 | 2.11364 | 1.18182 | 0.04589 | 0.11810 |
| 2 | 2.10651 | 1.16082 | −0.00012 | 0.00160 |
| 3 | 2.10646 | 1.16048 | 0.00000 | 0.00000 |

The values $2.11$ and $1.16$ are the same in iterations 2 and 3.

$$\boxed{x \approx 2.11,\qquad y \approx 1.16}$$

@s 3
**Doolittle's method** writes $A = LU$ with $L$ unit lower triangular ($l_{ii} = 1$) and $U$ upper triangular, then solves $Ly = b$ (forward) and $Ux = y$ (backward).

$$\begin{pmatrix} 2 & 5 & 4 \\ 3 & 4 & 5 \\ 5 & 4 & 4 \end{pmatrix} = \begin{pmatrix} 1 & 0 & 0 \\ l_{21} & 1 & 0 \\ l_{31} & l_{32} & 1 \end{pmatrix}\begin{pmatrix} u_{11} & u_{12} & u_{13} \\ 0 & u_{22} & u_{23} \\ 0 & 0 & u_{33} \end{pmatrix}$$

**Row 1 of $U$:** $u_{11} = 2,\ u_{12} = 5,\ u_{13} = 4$.

**Column 1 of $L$:** $l_{21} = \dfrac32 = 1.5,\quad l_{31} = \dfrac52 = 2.5$.

**Row 2 of $U$:** $u_{22} = 4 - 1.5(5) = -3.5,\quad u_{23} = 5 - 1.5(4) = -1$.

**Column 2 of $L$:** $l_{32} = \dfrac{4 - 2.5(5)}{-3.5} = \dfrac{-8.5}{-3.5} = \dfrac{17}{7}$.

**Row 3 of $U$:** $u_{33} = 4 - 2.5(4) - \dfrac{17}{7}(-1) = -6 + \dfrac{17}7 = -\dfrac{25}{7}$.

$$L = \begin{pmatrix} 1 & 0 & 0 \\ 3/2 & 1 & 0 \\ 5/2 & 17/7 & 1 \end{pmatrix},\qquad U = \begin{pmatrix} 2 & 5 & 4 \\ 0 & -7/2 & -1 \\ 0 & 0 & -25/7 \end{pmatrix}$$

**Forward substitution** $Ly = b$:

$$\begin{gathered}y_1 = 24 \\ y_2 = 28 - 1.5(24) = -8 \\ y_3 = 32 - 2.5(24) - \tfrac{17}{7}(-8) = -28 + \tfrac{136}{7} = -\tfrac{60}{7}\end{gathered}$$

**Back substitution** $Ux = y$:

$$\begin{gathered}z = \frac{-60/7}{-25/7} = 2.4 \\ y = \frac{-8 + 2.4}{-3.5} = 1.6 \\ x = \frac{24 - 5(1.6) - 4(2.4)}{2} = 3.2\end{gathered}$$

$$\boxed{x = 3.2,\qquad y = 1.6,\qquad z = 2.4}$$

**Check:** $2(3.2) + 5(1.6) + 4(2.4) = 24$ ✓; $3(3.2) + 4(1.6) + 5(2.4) = 28$ ✓; $5(3.2) + 4(1.6) + 4(2.4) = 32$ ✓.

@s 4
Start with $x^{(0)} = (1, 1, 1)^T$; repeat $y = Ax$, $\lambda = $ largest-magnitude component, $x \leftarrow y/\lambda$.

| $k$ | $A x^{(k)}$ | $\lambda_k$ | $x^{(k+1)}$ |
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

The estimates converge to $\lambda \approx 6.24$ and $v \approx (1, 1, 0.243)^T$.

$$\boxed{\lambda_{max} \approx 6.24,\qquad v \approx (1,\ 1,\ 0.243)^T}$$

**Exact check.** For $v = (1, 1, t)$: row 1 gives $\lambda = 6 + t$; row 3 gives $2 - 2t = \lambda t$. So $t^2 + 8t - 2 = 0$, $t = 3\sqrt2 - 4 = 0.2426$, and $\lambda = 2 + 3\sqrt2 = 6.2426$ ✓. (The other eigenvalues are $-2$ and $2 - 3\sqrt2 = -2.243$, so $6.2426$ is dominant.)

@s 5
**Divided-difference table**

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

First differences: $\dfrac{7.1 - 4.72}{2} = 1.19$, $\dfrac{5.72 - 7.1}{3} = -0.46$, $\dfrac{5.7 - 5.72}{2} = -0.01$, $\dfrac{7.04 - 5.7}{1} = 1.34$, $\dfrac{14.22 - 7.04}{2} = 3.59$.
Second: $\dfrac{-0.46 - 1.19}{5} = -0.33$, $\dfrac{-0.01 + 0.46}{5} = 0.09$, $\dfrac{1.34 + 0.01}{3} = 0.45$, $\dfrac{3.59 - 1.34}{3} = 0.75$.
Third: $\dfrac{0.09 + 0.33}{7} = 0.06$, $\dfrac{0.45 - 0.09}{6} = 0.06$, $\dfrac{0.75 - 0.45}{5} = 0.06$. Fourth: $0$.

The third differences are constant, so the data follow a cubic. Newton's divided-difference polynomial:

$$y(x) = 4.72 + 1.19x - 0.33\,x(x - 2) + 0.06\,x(x - 2)(x - 5)$$

At $x = 9$: $x = 9$, $x - 2 = 7$, $x - 5 = 4$:

$$y(9) = 4.72 + 1.19(9) - 0.33(9)(7) + 0.06(9)(7)(4) = 4.72 + 10.71 - 20.79 + 15.12$$

$$\boxed{y(9) = 9.76}$$

@s 6
Take natural logarithms: $y = ae^{bx} \Rightarrow \ln y = \ln a + bx$, i.e. $Y = A + bx$ with $Y = \ln y$, $A = \ln a$. Normal equations:

$$\begin{gathered}\sum Y = nA + b\sum x\\ \sum xY = A\sum x + b\sum x^2\end{gathered}$$

| $x$ | $y$ | $Y = \ln y$ | $x^2$ | $xY$ |
|---|---|---|---|---|
| 2 | 4.1 | 1.41099 | 4 | 2.82197 |
| 4 | 11.2 | 2.41591 | 16 | 9.66366 |
| 6 | 30.2 | 3.40784 | 36 | 20.44705 |
| 8 | 81.9 | 4.40550 | 64 | 35.24398 |
| 10 | 204.6 | 5.32106 | 100 | 53.21057 |
| **Σ = 30** | | **16.96130** | **220** | **121.38724** |

$$\begin{gathered}5A + 30b = 16.96130\\ 30A + 220b = 121.38724\end{gathered}$$

Multiply the first by $6$: $30A + 180b = 101.7678$. Subtracting from the second, $40b = 19.61944$:

$$\begin{gathered}b = 0.49049 \\ A = \frac{16.96130 - 30(0.49049)}{5} = 0.44934 \\ a = e^{0.44934} = 1.5673\end{gathered}$$

$$\boxed{y = 1.567\,e^{0.4905x}}$$

Check: $x = 10$ gives $1.567e^{4.905} = 211.5$ (observed $204.6$); $x = 6$ gives $29.7$ (observed $30.2$).

@s 7
Map $[0, 4] \to [-1, 1]$: $x = 2 + 2t$, $dx = 2\,dt$.

$$\begin{gathered}I = 2\int_{-1}^{1}\left[\cos(\pi(1 + t)) + 5\right]dt \approx 2\sum_{i=1}^3 w_i\,g(t_i) \\ g = \cos\left(\tfrac{\pi x}{2}\right) + 5\end{gathered}$$

| $t_i$ | $w_i$ | $x_i = 2 + 2t_i$ | $g(x_i)$ |
|---|---|---|---|
| −0.774597 | 5/9 | 0.450807 | 5.759582 |
| 0 | 8/9 | 2 | 4 |
| +0.774597 | 5/9 | 3.549193 | 5.759582 |

$$I \approx 2\left[\tfrac59(5.759582) + \tfrac89(4) + \tfrac59(5.759582)\right] = 2\,[3.199768 + 3.555556 + 3.199768]$$

$$\boxed{I_{GL3} = 19.9102}$$

**Exact value**

$$\int_0^4\left(\cos\frac{\pi x}{2} + 5\right)dx = \left[\frac2\pi\sin\frac{\pi x}2 + 5x\right]_0^4 = \frac2\pi(\sin2\pi - 0) + 20 = 20$$

Error $= 20 - 19.9102 = 0.0898$, i.e. $0.45\%$. (The integrand has two full cosine periods in the range, which a 3-point rule cannot resolve exactly; splitting the range into sub-intervals would improve it.)

@s 8
Let $x_i = x_0 + ih$ and $p = \dfrac{x - x_0}{h}$. **Newton's forward interpolation formula**

$$y = y_0 + p\,\Delta y_0 + \frac{p(p-1)}{2!}\Delta^2y_0 + \frac{p(p-1)(p-2)}{3!}\Delta^3y_0 + \frac{p(p-1)(p-2)(p-3)}{4!}\Delta^4y_0 + \cdots$$

Expanding the products: $p(p-1) = p^2 - p$; $p(p-1)(p-2) = p^3 - 3p^2 + 2p$; $p(p-1)(p-2)(p-3) = p^4 - 6p^3 + 11p^2 - 6p$. Since $\dfrac{dp}{dx} = \dfrac1h$:

**First derivative**

$$\frac{dy}{dx} = \frac1h\left[\Delta y_0 + \frac{2p-1}{2}\Delta^2y_0 + \frac{3p^2 - 6p + 2}{6}\Delta^3y_0 + \frac{4p^3 - 18p^2 + 22p - 6}{24}\Delta^4y_0 + \cdots\right]$$

**Second derivative** (differentiate again with respect to $x$):

$$\frac{d^2y}{dx^2} = \frac1{h^2}\left[\Delta^2y_0 + (p-1)\Delta^3y_0 + \frac{6p^2 - 18p + 11}{12}\Delta^4y_0 + \cdots\right]$$

**For the initial point** $x = x_0$, $p = 0$, the formulas become

$$\boxed{\left(\frac{dy}{dx}\right)_{x_0} = \frac1h\left[\Delta y_0 - \frac12\Delta^2y_0 + \frac13\Delta^3y_0 - \frac14\Delta^4y_0 + \frac15\Delta^5y_0 - \cdots\right]}$$

$$\boxed{\left(\frac{d^2y}{dx^2}\right)_{x_0} = \frac1{h^2}\left[\Delta^2y_0 - \Delta^3y_0 + \frac{11}{12}\Delta^4y_0 - \frac56\Delta^5y_0 + \cdots\right]}$$

*Notes.* (i) At a general tabulated point $x_k$ use $x_k$ in place of $x_0$ and the differences that start at $y_k$. (ii) Truncating after $\Delta^2y_0$ and using $\Delta y_0 - \tfrac12\Delta^2y_0 = (y_1 - y_0) - \tfrac12(y_2 - 2y_1 + y_0) = \tfrac12(-3y_0 + 4y_1 - y_2)$ gives the three-point formula $y'_0 \approx \dfrac{-3y_0 + 4y_1 - y_2}{2h}$ with error $O(h^2)$, and $y''_0 \approx \dfrac{y_0 - 2y_1 + y_2}{h^2}$ with error $O(h)$.

@s 9
**Algorithm.** For $y' = f(x, y)$, $y(x_0) = y_0$ with step $h$:

$$k_1 = hf(x_i, y_i),\ k_2 = hf\!\left(x_i + \tfrac h2, y_i + \tfrac{k_1}2\right),\ k_3 = hf\!\left(x_i + \tfrac h2, y_i + \tfrac{k_2}2\right),\ k_4 = hf(x_i + h, y_i + k_3)$$

$$\begin{gathered}y_{i+1} = y_i + \tfrac16(k_1 + 2k_2 + 2k_3 + k_4) \\ x_{i+1} = x_i + h\end{gathered}$$

```python
import numpy as np
import matplotlib.pyplot as plt

def rk4(f, x0, y0, xn, h):
    """Classical fourth-order Runge-Kutta for y' = f(x, y), y(x0) = y0."""
    n = int(round((xn - x0) / h))
    xs, ys = [x0], [y0]
    for _ in range(n):
        x, y = xs[-1], ys[-1]
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)
        ys.append(y + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
        xs.append(x + h)
    return np.array(xs), np.array(ys)

if __name__ == "__main__":
    f = lambda x, y: x + y                      # example: y' = x + y, y(0) = 1
    xs, ys = rk4(f, 0.0, 1.0, 2.0, 0.2)
    for x, y in zip(xs, ys):
        print(f"x = {x:4.1f}   y = {y:.6f}")
    xe = np.linspace(0, 2, 200)
    plt.plot(xe, 2 * np.exp(xe) - xe - 1, label="exact")          # exact solution 2e^x - x - 1
    plt.plot(xs, ys, "o-", label="RK4, h = 0.2")
    plt.xlabel("x"); plt.ylabel("y"); plt.legend(); plt.grid(True)
    plt.savefig("rk4.png", dpi=150); plt.show()
```

**Output** of the program (executed) for the example $y' = x + y,\ y(0) = 1$, $h = 0.2$:

```
x =  0.0   y = 1.000000
x =  0.2   y = 1.242800
x =  0.4   y = 1.583636
x =  0.6   y = 2.044213
x =  0.8   y = 2.651042
x =  1.0   y = 3.436502
x =  1.2   y = 4.440144
x =  1.4   y = 5.710272
x =  1.6   y = 7.305886
x =  1.8   y = 9.299049
x =  2.0   y = 11.777778
```

The exact value $y(2) = 2e^2 - 3 = 11.77811$, so the RK4 error is only $3\times10^{-4}$. The graph produced by `matplotlib` is shown below (the dots are RK4, the curve is the exact solution).

```figure caption="Graphical output of the program: RK4 points (h = 0.2) lie on the exact solution $y = 2e^x - x - 1$ of $y' = x + y$, $y(0) = 1$."
import numpy as np, matplotlib.pyplot as plt
f=lambda x,y:x+y
xs=[0.0];ys=[1.0];h=0.2
for _ in range(10):
    x,y=xs[-1],ys[-1]
    k1=h*f(x,y);k2=h*f(x+h/2,y+k1/2);k3=h*f(x+h/2,y+k2/2);k4=h*f(x+h,y+k3)
    ys.append(y+(k1+2*k2+2*k3+k4)/6);xs.append(x+h)
xe=np.linspace(0,2,200)
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(xe,2*np.exp(xe)-xe-1,color=ACCENT,label="exact")
ax.plot(xs,ys,'o',color=SERIES[1],label="RK4, h = 0.2",ms=4)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(loc="upper left"); ax.grid(True)
```

@s 10
$h = \dfrac{4 - 2}{4} = 0.5$; internal nodes $x_1 = 2.5$, $x_2 = 3$, $x_3 = 3.5$; $y_0 = 4$, $y_4 = 5$. Use central differences $y''_i = \dfrac{y_{i+1} - 2y_i + y_{i-1}}{h^2}$, $y'_i = \dfrac{y_{i+1} - y_{i-1}}{2h}$ in $y'' - 5y' + 4y = 5x$:

$$\left(\frac1{h^2} + \frac5{2h}\right)y_{i-1} + \left(4 - \frac2{h^2}\right)y_i + \left(\frac1{h^2} - \frac5{2h}\right)y_{i+1} = 5x_i$$

With $h = 0.5$: $\dfrac1{h^2} = 4$, $\dfrac5{2h} = 5$, so the coefficients are $9,\ -4,\ -1$:

$$9y_{i-1} - 4y_i - y_{i+1} = 5x_i$$

| node | equation | simplified |
|---|---|---|
| $x_1 = 2.5$ | $9(4) - 4y_1 - y_2 = 12.5$ | $-4y_1 - y_2 = -23.5$ |
| $x_2 = 3$ | $9y_1 - 4y_2 - y_3 = 15$ | $9y_1 - 4y_2 - y_3 = 15$ |
| $x_3 = 3.5$ | $9y_2 - 4y_3 - 5 = 17.5$ | $9y_2 - 4y_3 = 22.5$ |

**Solve.** $y_2 = 23.5 - 4y_1$; $y_3 = \dfrac{9y_2 - 22.5}{4} = 47.25 - 9y_1$. In the second equation:

$$9y_1 - 4(23.5 - 4y_1) - (47.25 - 9y_1) = 15 \Rightarrow 34y_1 = 156.25$$

$$\begin{gathered}y_1 = 4.59559 \\ y_2 = 23.5 - 18.38235 = 5.11765 \\ y_3 = 47.25 - 41.36029 = 5.88971\end{gathered}$$

| $x$ | 2 | 2.5 | 3 | 3.5 | 4 |
|---|---|---|---|---|---|
| $y$ | 4 | **4.5956** | **5.1176** | **5.8897** | 5 |

@s 11
With $h = 1/3$ the interior nodes are $u_1 = u(\tfrac13,\tfrac13)$, $u_2 = u(\tfrac23,\tfrac13)$, $u_3 = u(\tfrac13,\tfrac23)$, $u_4 = u(\tfrac23,\tfrac23)$. Laplace's equation gives $u_{i,j} = \tfrac14(\text{four neighbours})$.

**Boundary values**

| Edge | at $\tfrac13$ | at $\tfrac23$ |
|---|---|---|
| bottom $u(x, 0) = 360x$ | 120 | 240 |
| top $u(x, 1) = 240(1 - x)$ | 160 | 80 |
| left $u(0, y) = 240y$ | 80 | 160 |
| right $u(1, y) = 360(1 - y)$ | 240 | 120 |

**Equations**

$$\begin{gathered}u_1 = \tfrac14(u_2 + u_3 + 80 + 120)\\ u_2 = \tfrac14(u_1 + u_4 + 240 + 240)\\ u_3 = \tfrac14(u_1 + u_4 + 160 + 160)\\ u_4 = \tfrac14(u_2 + u_3 + 120 + 80)\end{gathered}$$

**Gauss-Seidel.** Start from $u_i = 0$ and always use the newest value in the same sweep: $u_1 \to u_2 \to u_3 \to u_4$.

| Iter | $u_1$ | $u_2$ | $u_3$ | $u_4$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 50.000 | 132.500 | 92.500 | 106.250 |
| 2 | 106.250 | 173.125 | 133.125 | 126.563 |
| 3 | 126.563 | 183.281 | 143.281 | 131.641 |
| 4 | 131.641 | 185.820 | 145.820 | 132.910 |
| 5 | 132.910 | 186.455 | 146.455 | 133.228 |
| 6 | 133.228 | 186.614 | 146.614 | 133.307 |
| 7 | 133.307 | 186.653 | 146.653 | 133.327 |
| 8 | 133.327 | 186.663 | 146.663 | 133.332 |

(For example, iteration 1: $u_1 = \tfrac14(0 + 0 + 200) = 50$; $u_2 = \tfrac14(50 + 0 + 480) = 132.5$; $u_3 = \tfrac14(50 + 0 + 320) = 92.5$; $u_4 = \tfrac14(132.5 + 92.5 + 200) = 106.25$.)

The iterates are converging to the exact solution, which follows from the symmetry $u_1 = u_4 = a$: $u_2 = \dfrac{2a + 480}4$, $u_3 = \dfrac{2a + 320}4$, $4a = u_2 + u_3 + 200 \Rightarrow a = \dfrac{400}{3}$.

$$\boxed{u_1 = u_4 \approx 133.33,\qquad u_2 \approx 186.67,\qquad u_3 \approx 146.67}$$

@s 12
**Derivation.** For $u_t = c^2u_{xx}$ use a forward difference in time and a central difference in space:

$$\frac{u_{i,j+1} - u_{i,j}}{k} = c^2\frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{h^2}$$

With $\lambda = \dfrac{c^2k}{h^2}$:

$$u_{i,j+1} = \lambda u_{i-1,j} + (1 - 2\lambda)u_{i,j} + \lambda u_{i+1,j}$$

which is stable for $\lambda \le \tfrac12$. **Bender-Schmidt** takes $\lambda = \tfrac12$, so the middle term vanishes:

$$\boxed{u_{i,j+1} = \tfrac12\left[u_{i-1,j} + u_{i+1,j}\right]}$$

**Problem.** $c^2 = 0.5$, $h = 1$; $\lambda = \tfrac12$ requires $k = \dfrac{\lambda h^2}{c^2} = \dfrac{0.5}{0.5} = 1$.

$u_{i,0} = 2x_i(4 - x_i)$ at $x = 0, 1, 2, 3, 4$: $0,\ 6,\ 8,\ 6,\ 0$; the end values stay $0$.

| $t$ | $j$ | $x=0$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 6 | 8 | 6 | 0 |
| 1 | 1 | 0 | 4 | 6 | 4 | 0 |
| 2 | 2 | 0 | 3 | 4 | 3 | 0 |
| 3 | 3 | 0 | 2 | 3 | 2 | 0 |
| 4 | 4 | 0 | 1.5 | 2 | 1.5 | 0 |
| 5 | 5 | 0 | 1 | 1.5 | 1 | 0 |

Sample: $u_{1,1} = \tfrac12(0 + 8) = 4$, $u_{2,1} = \tfrac12(6 + 6) = 6$; $u_{1,2} = \tfrac12(0 + 6) = 3$, $u_{2,2} = \tfrac12(4 + 4) = 4$; $u_{1,5} = \tfrac12(0 + 2) = 1$, $u_{2,5} = \tfrac12(1.5 + 1.5) = 1.5$.

$$\boxed{\text{at } t = 5:\ u(1) = u(3) = 1,\quad u(2) = 1.5}$$

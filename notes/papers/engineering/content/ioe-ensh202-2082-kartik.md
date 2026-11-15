---
file: NEBians-IOE-Past-Paper-Engineering-Numerical-Methods-ENSH202-2082-Kartik.pdf
subject: Numerical Methods
level: BE · Year II / Part I
code: ENSH 202
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
Discuss the major difference between Secant method and Regula Falsi method. Find a real root of the equation $x^3 - 2x - 5 = 0$ correct to four decimal places using the secant method. [[5]]

@q 2
Write Jacobian matrix for the following system of non-linear equations and use Newton Raphson method to approximate the solution correct to two decimal places taking $(x_0, y_0) = (0.9, 0.5)$ as initial guess values.
$$x^2 + y^2 = 1$$
$$x^3 - y = 0$$
[[5]]

@q 3
Find the inverse of the following matrix using Gauss Jordan method.
$$\begin{pmatrix} -2 & 6 & 4 \\ 4 & -6 & 0 \\ -2 & 4 & 2 \end{pmatrix}$$
[[5]]

@q 4
Write a python program to determine the dominant eigen value and corresponding eigen vector of a square matrix using the power method. [[5]]

@q 5
Using the least square method, fit the following data to a curve of the form $y = ab^x$.

| $x$ | 5 | 15 | 25 | 35 | 45 | 55 |
|---|---|---|---|---|---|---|
| $y$ | 1.8 | 7.1 | 16.6 | 30.2 | 47.5 | 68.5 |

[[5]]

@q 6
Estimate $y(5)$ and $y(22)$ from the following data using appropriate polynomial interpolation technique used for equally spaced intervals.

| $x$ | 4 | 8 | 12 | 16 | 20 | 24 |
|---|---|---|---|---|---|---|
| $y$ | 15.4 | 16.5 | 14.2 | 10.8 | 8.6 | 9.9 |

[[5]]

@q 7
Evaluate the following integral with an accuracy of three decimal places using Romberg's method starting from $h = 0.5$.
$$\int_{-1}^{1}\frac{2}{1 + x^2}\,dx$$
[[5]]

@q 8
Evaluate the following integral using Simpson's three-eighth rule and Weddle's rule by dividing the range into six equally spaced intervals and compare the results with the exact solution.
$$\int_0^{3\pi}(\sin x + 5)\,dx$$
[[5]]

@q 9
Solve the following initial value problem for $y(0.2)$ and $y(0.5)$ using Runge-Kutta fourth order method (take $h = 0.2$ and $h = 0.3$ respectively).
$$\begin{gathered}y' = \sqrt{x + y} - 1 \\ y(0) = 1\end{gathered}$$
[[5]]

@q 10
Using finite difference method, solve the following boundary value problem for three internal nodes: $y'' - 3y' + 2y = 4x - 8$, $y(2) = 3$, $y(4) = 5$. [[5]]

@q 11
Write recurrence relation for solving Poisson's equation $u_{xx} + u_{yy} = f(x, y)$ and hence use it to solve partial differential equation $u_{xx} + u_{yy} = 243x^2y$ on domain $0 \le x \le 1$ and $0 \le y \le 1$ with $u = 30$ on the boundary and mesh length $h = 1/3$. [[5]]

@q 12
Derive the recurrence relation for solving one dimensional heat equation using Bender-Schmidt method and use it to solve the following problem for five time steps taking $\Delta x = h = 1$.
$$\begin{gathered}u_t = 0.25\,u_{xx} \\ u(0, t) = u(5, t) = 0 \\ u(x, 0) = x(5 - x)\end{gathered}$$
[[5]]
<!-- SOLUTIONS -->

@s 1
**Difference between the two methods.** Both replace the curve by the chord through two points and take the chord's $x$-intercept as the next estimate:

$$x_{n+1} = x_n - f(x_n)\frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

| | **Secant method** | **Regula Falsi (false position)** |
|---|---|---|
| Points used | the **two latest** estimates, always $x_n$ and $x_{n-1}$ | two points $a, b$ that **bracket** the root, $f(a)f(b) < 0$ |
| Replacement | the oldest point is discarded, whatever the sign | the new point replaces the end having the *same sign* as $f(c)$, so the root stays bracketed |
| Convergence | superlinear, order $\tfrac{1+\sqrt5}{2} \approx 1.618$ | linear (one end often gets stuck) |
| Safety | may diverge if the starting points are poor | always converges (for continuous $f$) |

**Solution.** $f(x) = x^3 - 2x - 5$; $f(2) = -1$, $f(3) = 16$. Take $x_0 = 2$, $x_1 = 3$.

| $i$ | $x_{i-1}$ | $x_i$ | $f(x_{i-1})$ | $f(x_i)$ | $x_{i+1}$ |
|---|---|---|---|---|---|
| 1 | 2 | 3 | −1 | 16 | 2.058824 |
| 2 | 3 | 2.058824 | 16 | −0.390800 | 2.081264 |
| 3 | 2.058824 | 2.081264 | −0.390800 | −0.147204 | 2.094824 |
| 4 | 2.081264 | 2.094824 | −0.147204 | 0.003044 | 2.094549 |
| 5 | 2.094824 | 2.094549 | 0.003044 | −0.000023 | 2.094551 |
| 6 | 2.094549 | 2.094551 | −0.000023 | $\approx 0$ | 2.094551 |

Successive iterates agree to the sixth decimal, $2.094551$.

$$\boxed{x \approx 2.0946}$$

@s 2
$F_1 = x^2 + y^2 - 1$, $F_2 = x^3 - y$. **Jacobian**

$$J = \begin{pmatrix} \partial F_1/\partial x & \partial F_1/\partial y \\ \partial F_2/\partial x & \partial F_2/\partial y \end{pmatrix} = \begin{pmatrix} 2x & 2y \\ 3x^2 & -1 \end{pmatrix}$$

At each step solve $J\,\Delta = -F$, then $(x, y) \leftarrow (x, y) + \Delta$.

**Iteration 1**, $(0.9, 0.5)$: $F = (0.06,\ 0.229)$, $J = \begin{pmatrix} 1.8 & 1 \\ 2.43 & -1\end{pmatrix}$. Adding the two equations $1.8\Delta x + \Delta y = -0.06$ and $2.43\Delta x - \Delta y = -0.229$ gives $4.23\Delta x = -0.289$:

$$\begin{gathered}\Delta x = -0.06832 \\ \Delta y = -0.06 - 1.8(-0.06832) = 0.06298\end{gathered}$$

$$(x_1, y_1) = (0.83168,\ 0.56298)$$

**Iteration 2**: $F = (0.00863,\ 0.01228)$, $J = \begin{pmatrix} 1.66336 & 1.12596 \\ 2.07507 & -1\end{pmatrix}$ gives $\Delta = (-0.00562,\ 0.00063)$:

$$(x_2, y_2) = (0.82606,\ 0.56361)$$

**Iteration 3**: $F = (3\times10^{-5},\ 8\times10^{-5})$, $\Delta = (-0.00003,\ 0.00002)$:

$$(x_3, y_3) = (0.82603,\ 0.56362)$$

The values $0.83$ and $0.56$ have not changed since iteration 1, so two-decimal accuracy is reached.

$$\boxed{x \approx 0.83,\qquad y \approx 0.56}$$

(Geometrically, this is the intersection of the unit circle with the cubic $y = x^3$.)

@s 3
Write $[A\,|\,I]$ and apply row operations until the left block becomes $I$; the right block is then $A^{-1}$. Here $\det A = -8 \ne 0$, so the inverse exists.

$$[A\,|\,I] = \left[\begin{array}{ccc|ccc} -2 & 6 & 4 & 1 & 0 & 0\\ 4 & -6 & 0 & 0 & 1 & 0\\ -2 & 4 & 2 & 0 & 0 & 1\end{array}\right]$$

**Column 1.** $R_1 \to R_1/(-2)$; $R_2 \to R_2 - 4R_1$; $R_3 \to R_3 + 2R_1$:

$$\left[\begin{array}{ccc|ccc} 1 & -3 & -2 & -\tfrac12 & 0 & 0\\ 0 & 6 & 8 & 2 & 1 & 0\\ 0 & -2 & -2 & -1 & 0 & 1\end{array}\right]$$

**Column 2.** $R_2 \to R_2/6$; $R_1 \to R_1 + 3R_2$; $R_3 \to R_3 + 2R_2$:

$$\left[\begin{array}{ccc|ccc} 1 & 0 & 2 & \tfrac12 & \tfrac12 & 0\\ 0 & 1 & \tfrac43 & \tfrac13 & \tfrac16 & 0\\ 0 & 0 & \tfrac23 & -\tfrac13 & \tfrac13 & 1\end{array}\right]$$

**Column 3.** $R_3 \to \tfrac32R_3$; $R_1 \to R_1 - 2R_3$; $R_2 \to R_2 - \tfrac43R_3$:

$$\left[\begin{array}{ccc|ccc} 1 & 0 & 0 & \tfrac32 & -\tfrac12 & -3\\ 0 & 1 & 0 & 1 & -\tfrac12 & -2\\ 0 & 0 & 1 & -\tfrac12 & \tfrac12 & \tfrac32\end{array}\right]$$

$$\boxed{A^{-1} = \begin{pmatrix} 1.5 & -0.5 & -3 \\ 1 & -0.5 & -2 \\ -0.5 & 0.5 & 1.5 \end{pmatrix}}$$

**Check:** first row of $A$ times first column of $A^{-1}$: $(-2)(1.5) + 6(1) + 4(-0.5) = -3 + 6 - 2 = 1$ ✓; first row times second column: $(-2)(-0.5) + 6(-0.5) + 4(0.5) = 1 - 3 + 2 = 0$ ✓.

@s 4
**Algorithm.** Start with $x^{(0)} = (1, \dots, 1)^T$. Repeat: $y = Ax$; $\lambda = $ the component of $y$ with the largest magnitude; $x = y/\lambda$. Stop when $|\lambda_{new} - \lambda_{old}| <$ tolerance. Then $\lambda$ is the dominant eigenvalue and $x$ its eigenvector (scaled so the largest entry is $1$).

```python
import numpy as np

def power_method(A, x0=None, tol=1e-6, max_iter=1000):
    """Dominant eigenvalue and eigenvector of a square matrix by the power method."""
    A = np.array(A, dtype=float)
    n = A.shape[0]
    x = np.ones(n) if x0 is None else np.array(x0, dtype=float)
    lam_old = 0.0
    for k in range(1, max_iter + 1):
        y = A @ x                              # y = A x
        lam = y[np.argmax(np.abs(y))]          # component of largest magnitude (with sign)
        if lam == 0:
            raise ZeroDivisionError("A x = 0, choose another starting vector")
        x = y / lam                            # scale so that the largest component is 1
        if abs(lam - lam_old) < tol:           # stop when the eigenvalue settles
            return lam, x, k
        lam_old = lam
    raise RuntimeError("power method did not converge")

if __name__ == "__main__":
    n = int(input("Order of the matrix: "))
    print("Enter the matrix row by row:")
    A = [list(map(float, input().split())) for _ in range(n)]
    lam, vec, its = power_method(A)
    print(f"Dominant eigenvalue = {lam:.6f}  (after {its} iterations)")
    print("Eigenvector         =", np.round(vec, 6))
```

**Test run** with $A = \begin{pmatrix}2&4&6\\4&2&6\\6&6&2\end{pmatrix}$ (executed):

```
Order of the matrix: 3
Enter the matrix row by row:
2 4 6
4 2 6
6 6 2
Dominant eigenvalue = 12.717798  (after 17 iterations)
Eigenvector         = [0.89315 0.89315 1.     ]
```

This agrees with `numpy.linalg.eigvals`, whose largest eigenvalue is $12.717798 = 4 + 2\sqrt{19}$.

@s 5
Take logarithms: $y = ab^x \Rightarrow \log y = \log a + x\log b$, i.e. $Y = A + Bx$ with $Y = \log_{10} y$, $A = \log a$, $B = \log b$. The normal equations are

$$\begin{gathered}\sum Y = nA + B\sum x\\ \sum xY = A\sum x + B\sum x^2\end{gathered}$$

| $x$ | $y$ | $Y = \log_{10}y$ | $x^2$ | $xY$ |
|---|---|---|---|---|
| 5 | 1.8 | 0.25527 | 25 | 1.27637 |
| 15 | 7.1 | 0.85126 | 225 | 12.76887 |
| 25 | 16.6 | 1.22011 | 625 | 30.50270 |
| 35 | 30.2 | 1.48001 | 1225 | 51.80025 |
| 45 | 47.5 | 1.67669 | 2025 | 75.45123 |
| 55 | 68.5 | 1.83569 | 3025 | 100.96300 |
| **Σ = 180** | | **7.31903** | **7150** | **272.76242** |

$$\begin{gathered}6A + 180B = 7.31903\\ 180A + 7150B = 272.76242\end{gathered}$$

Multiplying the first by $30$: $180A + 5400B = 219.5709$. Subtracting, $1750B = 53.19152$, so $B = 0.030395$ and $A = \dfrac{7.31903 - 180(0.030395)}{6} = 0.30798$.

$$\begin{gathered}a = 10^{0.30798} = 2.0323 \\ b = 10^{0.030395} = 1.0725\end{gathered}$$

$$\begin{gathered}\boxed{y = 2.032\,(1.0725)^x} \\ (\text{equivalently } y = 2.032\,e^{0.0700x})\end{gathered}$$

*Remark.* The data are closer to a parabola than to an exponential (e.g. $y(25) = 16.6$ against the fitted $2.032\times1.0725^{25} = 11.7$), so $y = ab^x$ is only a rough model here. The least-squares line through $(x, \log y)$ is nevertheless exactly the fit the question asks for.

@s 6
Because the table is equally spaced ($h = 4$), use **Newton's forward formula** for $y(5)$, which lies near the **start**, and **Newton's backward formula** for $y(22)$, which lies near the **end**.

**Difference table**

| $x$ | $y$ | $\Delta y$ | $\Delta^2y$ | $\Delta^3y$ | $\Delta^4y$ |
|---|---|---|---|---|---|
| 4 | 15.4 | | | | |
| | | 1.1 | | | |
| 8 | 16.5 | | −3.4 | | |
| | | −2.3 | | 2.3 | |
| 12 | 14.2 | | −1.1 | | 0 |
| | | −3.4 | | 2.3 | |
| 16 | 10.8 | | 1.2 | | 0 |
| | | −2.2 | | 2.3 | |
| 20 | 8.6 | | 3.5 | | |
| | | 1.3 | | | |
| 24 | 9.9 | | | | |

The third differences are constant ($2.3$), so a cubic fits exactly and all higher terms vanish.

**(i) $y(5)$** — forward: $p = \dfrac{5 - 4}{4} = 0.25$.

$$y = y_0 + p\Delta y_0 + \frac{p(p-1)}{2}\Delta^2y_0 + \frac{p(p-1)(p-2)}{6}\Delta^3y_0$$

$$= 15.4 + 0.25(1.1) + \frac{0.25(-0.75)}{2}(-3.4) + \frac{0.25(-0.75)(-1.75)}{6}(2.3)$$

$$= 15.4 + 0.27500 + 0.31875 + 0.12578$$

$$\boxed{y(5) \approx 16.1195}$$

**(ii) $y(22)$** — backward from $x_n = 24$: $p = \dfrac{22 - 24}{4} = -0.5$, with $\nabla y_n = 1.3$, $\nabla^2y_n = 3.5$, $\nabla^3y_n = 2.3$.

$$y = y_n + p\nabla y_n + \frac{p(p+1)}{2}\nabla^2y_n + \frac{p(p+1)(p+2)}{6}\nabla^3y_n$$

$$= 9.9 + (-0.5)(1.3) + \frac{(-0.5)(0.5)}{2}(3.5) + \frac{(-0.5)(0.5)(1.5)}{6}(2.3)$$

$$= 9.9 - 0.65 - 0.4375 - 0.14375$$

$$\boxed{y(22) \approx 8.6688}$$

```figure caption="The data points and the interpolating cubic. The two estimated points $y(5)$ and $y(22)$ are marked."
import numpy as np, matplotlib.pyplot as plt
x=np.array([4,8,12,16,20,24.]); y=np.array([15.4,16.5,14.2,10.8,8.6,9.9])
c=np.polyfit(x,y,3); xs=np.linspace(4,24,200)
fig,ax=plt.subplots(figsize=(5.2,2.6))
ax.plot(xs,np.polyval(c,xs),color=ACCENT,label="cubic through data"); ax.plot(x,y,'o',color=INK,label="data")
ax.plot([5,22],[16.1195,8.66875],'s',color=SERIES[1],label="estimates")
ax.annotate("y(5) = 16.12",(5,16.12),textcoords="offset points",xytext=(8,6),fontsize=7.5)
ax.annotate("y(22) = 8.67",(22,8.67),textcoords="offset points",xytext=(-30,-14),fontsize=7.5)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(loc="upper right"); ax.grid(True)
```

@s 7
**Romberg integration.** Compute trapezoidal estimates $T(h)$ with $h = 0.5, 0.25, 0.125$, then extrapolate: $R_{k,j} = \dfrac{4^{j}R_{k,j-1} - R_{k-1,j-1}}{4^{j} - 1}$.

$g(x) = \dfrac{2}{1 + x^2}$ is even. 

**$h = 0.5$** (nodes $-1, -0.5, 0, 0.5, 1$; $g = 1, 1.6, 2, 1.6, 1$):

$$T(0.5) = 0.5\left[\tfrac{1 + 1}{2} + 1.6 + 2 + 1.6\right] = 3.100000$$

**$h = 0.25$** (new nodes $\pm0.25, \pm0.75$; $g = 1.882353,\ 1.280000$):

$$T(0.25) = \tfrac12(3.1) + 0.25\,[2(1.882353) + 2(1.28)] = 1.55 + 1.581176 = 3.131176$$

**$h = 0.125$** (new nodes $\pm0.125, \pm0.375, \pm0.625, \pm0.875$; $g = 1.969231,\ 1.753425,\ 1.438202,\ 1.132743$):

$$T(0.125) = \tfrac12(3.131176) + 0.125\,[2(6.293601)] = 1.565588 + 1.573400 = 3.138988$$

| $h$ | $T(h)$ | $O(h^4)$ | $O(h^6)$ |
|---|---|---|---|
| 0.5 | 3.100000 | | |
| 0.25 | 3.131176 | 3.141569 | |
| 0.125 | 3.138988 | 3.141593 | 3.141594 |

Here $\dfrac{4(3.131176) - 3.1}{3} = 3.141569$, $\dfrac{4(3.138988) - 3.131176}{3} = 3.141593$, and $\dfrac{16(3.141593) - 3.141569}{15} = 3.141594$.

The last two columns agree to six decimals, so the value is accurate to three decimal places:

$$\boxed{\int_{-1}^{1}\frac{2}{1 + x^2}dx \approx 3.142}$$

(The exact value is $2\left[\arctan x\right]_{-1}^{1} = \pi = 3.141593$.)

@s 8
Six intervals on $[0, 3\pi]$: $h = \dfrac{3\pi}{6} = \dfrac\pi2$, nodes $x_i = i\pi/2$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $x_i$ | 0 | $\pi/2$ | $\pi$ | $3\pi/2$ | $2\pi$ | $5\pi/2$ | $3\pi$ |
| $f = \sin x + 5$ | 5 | 6 | 5 | 4 | 5 | 6 | 5 |

**Simpson's 3/8 rule**

$$I = \frac{3h}{8}\left[f_0 + 3f_1 + 3f_2 + 2f_3 + 3f_4 + 3f_5 + f_6\right] = \frac{3\pi}{16}\left[5 + 18 + 15 + 8 + 15 + 18 + 5\right] = \frac{3\pi}{16}(84)$$

$$\boxed{I_{3/8} = 15.75\pi = 49.4801}$$

**Weddle's rule**

$$I = \frac{3h}{10}\left[f_0 + 5f_1 + f_2 + 6f_3 + f_4 + 5f_5 + f_6\right] = \frac{3\pi}{20}\left[5 + 30 + 5 + 24 + 5 + 30 + 5\right] = \frac{3\pi}{20}(104)$$

$$\boxed{I_{W} = 15.6\pi = 49.0088}$$

**Exact value**

$$\int_0^{3\pi}(\sin x + 5)\,dx = \left[-\cos x + 5x\right]_0^{3\pi} = (1 + 15\pi) - (-1) = 2 + 15\pi = 49.1239$$

| Method | Value | Error | % error |
|---|---|---|---|
| Simpson 3/8 | 49.4801 | +0.3562 | 0.73 % |
| Weddle | 49.0088 | −0.1150 | 0.23 % |
| Exact | 49.1239 | | |

Weddle's rule is about three times closer here; Simpson's 3/8 rule over-estimates, Weddle's under-estimates.

@s 9
$f(x, y) = \sqrt{x + y} - 1$. The exact solution is $y = 1 + \dfrac{x^2}{4}$ (put $u = x + y$, $u' = \sqrt u$, $\sqrt u = x/2 + 1$), which is used as a check.

**(i) $y(0.2)$, $h = 0.2$, $(x_0, y_0) = (0, 1)$**

$$k_1 = 0.2\,f(0, 1) = 0.2(\sqrt1 - 1) = 0$$

$$k_2 = 0.2\,f(0.1, 1) = 0.2(\sqrt{1.1} - 1) = 0.009762$$

$$k_3 = 0.2\,f(0.1, 1.004881) = 0.2(\sqrt{1.104881} - 1) = 0.010227$$

$$k_4 = 0.2\,f(0.2, 1.010227) = 0.2(\sqrt{1.210227} - 1) = 0.020021$$

$$y(0.2) = 1 + \tfrac16[0 + 2(0.009762) + 2(0.010227) + 0.020021] = 1 + \tfrac{0.060}{6}$$

$$\boxed{y(0.2) = 1.010000}\quad(\text{exact } 1.01)$$

**(ii) $y(0.5)$, $h = 0.3$**, continuing from $(0.2, 1.01000)$ (since $0.2 + 0.3 = 0.5$):

$$k_1 = 0.3\,f(0.2, 1.01) = 0.3(\sqrt{1.21} - 1) = 0.030000$$

$$k_2 = 0.3\,f(0.35, 1.025) = 0.3(\sqrt{1.375} - 1) = 0.051781$$

$$k_3 = 0.3\,f(0.35, 1.035890) = 0.3(\sqrt{1.385890} - 1) = 0.053172$$

$$k_4 = 0.3\,f(0.5, 1.063172) = 0.3(\sqrt{1.563172} - 1) = 0.075081$$

$$y(0.5) = 1.01 + \tfrac16[0.030000 + 2(0.051781) + 2(0.053172) + 0.075081] = 1.01 + 0.052498$$

$$\boxed{y(0.5) = 1.062500}\quad(\text{exact } 1.0625)$$

@s 10
Put $h = \dfrac{4 - 2}{4} = 0.5$ (three internal nodes $x_1 = 2.5$, $x_2 = 3$, $x_3 = 3.5$; $y_0 = 3$, $y_4 = 5$). Central differences:

$$\begin{gathered}y''_i = \frac{y_{i+1} - 2y_i + y_{i-1}}{h^2} \\ y'_i = \frac{y_{i+1} - y_{i-1}}{2h}\end{gathered}$$

Substituting in $y'' - 3y' + 2y = 4x - 8$ and collecting terms:

$$\left(\frac1{h^2} + \frac3{2h}\right)y_{i-1} + \left(2 - \frac2{h^2}\right)y_i + \left(\frac1{h^2} - \frac3{2h}\right)y_{i+1} = 4x_i - 8$$

With $h = 0.5$: $\dfrac1{h^2} = 4$, $\dfrac3{2h} = 3$, so the coefficients are $7,\ -6,\ 1$:

$$7y_{i-1} - 6y_i + y_{i+1} = 4x_i - 8$$

| node | equation | right side |
|---|---|---|
| $x_1 = 2.5$ | $7(3) - 6y_1 + y_2 = 2$ | $-6y_1 + y_2 = -19$ |
| $x_2 = 3$ | $7y_1 - 6y_2 + y_3 = 4$ | $7y_1 - 6y_2 + y_3 = 4$ |
| $x_3 = 3.5$ | $7y_2 - 6y_3 + 5 = 6$ | $7y_2 - 6y_3 = 1$ |

**Solve.** From the first, $y_2 = 6y_1 - 19$. From the third, $y_3 = \dfrac{7y_2 - 1}{6} = \dfrac{42y_1 - 134}{6}$. Put in the second:

$$7y_1 - 6(6y_1 - 19) + \frac{42y_1 - 134}{6} = 4 \Rightarrow -29y_1 + 114 + 7y_1 - 22.3333 = 4 \Rightarrow -22y_1 = -87.6667$$

$$\begin{gathered}y_1 = 3.98485 \\ y_2 = 4.90909 \\ y_3 = 5.56061\end{gathered}$$

| $x$ | 2 | 2.5 | 3 | 3.5 | 4 |
|---|---|---|---|---|---|
| $y$ | 3 | **3.9848** | **4.9091** | **5.5606** | 5 |

@s 11
**Recurrence.** With a square mesh of side $h$ ($x_i = ih$, $y_j = jh$), the five-point central-difference formula gives

$$\frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{h^2} + \frac{u_{i,j+1} - 2u_{i,j} + u_{i,j-1}}{h^2} = f_{i,j}$$

$$\boxed{u_{i,j} = \tfrac14\left[u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1} - h^2f_{i,j}\right]}$$

For $f = 0$ this reduces to the Laplace (averaging) formula.

**Problem.** $h = 1/3$, $h^2 = 1/9$. Interior nodes: $u_1 = u(\tfrac13,\tfrac13)$, $u_2 = u(\tfrac23,\tfrac13)$, $u_3 = u(\tfrac13,\tfrac23)$, $u_4 = u(\tfrac23,\tfrac23)$. Every boundary value is $30$.

| node | $(x, y)$ | $f = 243x^2y$ | $h^2f$ |
|---|---|---|---|
| $u_1$ | (1/3, 1/3) | 9 | 1 |
| $u_2$ | (2/3, 1/3) | 36 | 4 |
| $u_3$ | (1/3, 2/3) | 18 | 2 |
| $u_4$ | (2/3, 2/3) | 72 | 8 |

Each node touches two boundary nodes (sum $60$):

$$\begin{gathered}4u_1 - u_2 - u_3 = 60 - 1 = 59\\ -u_1 + 4u_2 - u_4 = 60 - 4 = 56\\ -u_1 + 4u_3 - u_4 = 60 - 2 = 58\\ -u_2 - u_3 + 4u_4 = 60 - 8 = 52\end{gathered}$$

**Elimination.** Subtracting the 2nd equation from the 3rd gives $4(u_3 - u_2) = 2$, so $u_3 = u_2 + 0.5$. Put this into the 1st and 4th equations: $u_1 = \dfrac{59.5 + 2u_2}{4}$ and $u_4 = \dfrac{52.5 + 2u_2}{4}$. Then the 2nd equation becomes

$$-\frac{112 + 4u_2}{4} + 4u_2 = 56 \ \Rightarrow\ 3u_2 = 84 \ \Rightarrow\ u_2 = 28,$$

and back-substitution gives

$$\boxed{u_1 = 28.875,\quad u_2 = 28.000,\quad u_3 = 28.500,\quad u_4 = 27.125}$$

**Check:** equation 2: $4(28) - 28.875 - 27.125 = 56$ ✓; equation 4: $-28 - 28.5 + 4(27.125) = 52$ ✓. All interior values are below the boundary value $30$, as they must be, because $\nabla^2u > 0$ (the solution is subharmonic and the maximum principle holds).

@s 12
**Derivation.** The heat equation $u_t = c^2u_{xx}$ is discretised with a forward difference in time (step $k$) and a central difference in space (step $h$):

$$\frac{u_{i,j+1} - u_{i,j}}{k} = c^2\frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{h^2}$$

With $\lambda = \dfrac{c^2k}{h^2}$:

$$u_{i,j+1} = \lambda u_{i-1,j} + (1 - 2\lambda)u_{i,j} + \lambda u_{i+1,j}$$

This (explicit Schmidt) scheme is stable for $\lambda \le \tfrac12$. The **Bender-Schmidt** choice $\lambda = \tfrac12$ removes the middle term:

$$\boxed{u_{i,j+1} = \tfrac12\left[u_{i-1,j} + u_{i+1,j}\right]}$$

**Problem.** $c^2 = 0.25$, $h = 1$, so $\lambda = \tfrac12$ requires $k = \dfrac{\lambda h^2}{c^2} = \dfrac{0.5}{0.25} = 2$.

Initial values $u_{i,0} = x_i(5 - x_i)$ at $x = 0, 1, 2, 3, 4, 5$: $0, 4, 6, 6, 4, 0$; the end values stay $0$.

| $t$ | $j$ | $x=0$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 4 | 6 | 6 | 4 | 0 |
| 2 | 1 | 0 | 3 | 5 | 5 | 3 | 0 |
| 4 | 2 | 0 | 2.5 | 4 | 4 | 2.5 | 0 |
| 6 | 3 | 0 | 2 | 3.25 | 3.25 | 2 | 0 |
| 8 | 4 | 0 | 1.625 | 2.625 | 2.625 | 1.625 | 0 |
| 10 | 5 | 0 | 1.3125 | 2.125 | 2.125 | 1.3125 | 0 |

Sample: $u_{1,1} = \tfrac12(0 + 6) = 3$, $u_{2,1} = \tfrac12(4 + 6) = 5$; $u_{1,2} = \tfrac12(0 + 5) = 2.5$, $u_{2,2} = \tfrac12(3 + 5) = 4$; $u_{1,3} = \tfrac12(0 + 4) = 2$, $u_{2,3} = \tfrac12(2.5 + 4) = 3.25$.

$$\boxed{\text{at } t = 10:\ u(1) = u(4) = 1.3125,\quad u(2) = u(3) = 2.125}$$

The temperature profile is symmetric about $x = 2.5$ and decays toward zero because both ends are held at $0$.

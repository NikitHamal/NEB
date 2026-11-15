---
file: NEBians-IOE-Past-Paper-Engineering-Numerical-Methods-ENSH202-2082-Chaitra.pdf
subject: Numerical Methods
level: BE · Year II / Part I
code: ENSH 202
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BCE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · All questions carry equal marks · Assume suitable data if necessary</small>

@q 1
Approximate a real root of the non-linear equation $3x + \sin x - e^x = 0$ correct to three decimal places using the Bisection Method. [[5]]

@q 2
Solve the following system of non-linear equations using Newton-Raphson Method for a precision of 3 decimal places by taking $(1.8, 1.8)$ as the initial guess values.
$$x^4 - \cos y = 12$$
$$\sin x + y^4 = 15$$
[[5]]

@q 3
Write a python program to solve a system of linear equations using the Gauss-Jordan method. [[5]]

@q 4
Find the dominant eigen value and corresponding eigen vector of the following matrix using the Power method.
$$\begin{pmatrix} 2 & 4 & 6 \\ 4 & 2 & 6 \\ 6 & 6 & 2 \end{pmatrix}$$
[[5]]

@q 5
Using the method of least squares, fit the following data to a second-degree polynomial of the form $y = ax^2 + bx + c$.

| $x$ | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|
| $y$ | 2.5 | 2.7 | 3.5 | 6.5 | 5.4 | 4.8 |

[[5]]

@q 6
Construct divided difference table from the following data and use Newton's divided difference interpolation technique to approximate the value of $y(9)$.

| $x$ | 2 | 5 | 7 | 8 | 10 |
|---|---|---|---|---|---|
| $y$ | 8.10 | 6.72 | 6.70 | 8.04 | 15.22 |

[[5]]

@q 7
Derive expressions for evaluating the first and second order derivatives using Newton's forward interpolation formula. [[5]]

@q 8
Approximate the following integral using Gauss-Legendre 3-point formula.
$$\int_1^2 e^{\sin x}\,dx$$
[[5]]

@q 9
Given that $y' = \sin(\pi x) + \cos(y)$ and $y(0) = 2$, find the values of $y$ in $0 \le x \le 1$, taking a step-size of $h = 0.5$ using the Runge-Kutta fourth order method. [[5]]

@q 10
The results of two initial attempts while solving the two-point boundary value problem $y'' = 0.5x - y + y' + 3$, $y(0) = 5$, $y(2) = 8$ using the shooting method with Euler's formula taking a step-size of $0.5$ is given below.

| Initial Slope ($y'$) guessed | Final $y$ obtained |
|---|---|
| $m_1 = 1.0$ | 4.7187 |
| $m_2 = 3.0$ | 11.5938 |

Using this information, solve the given problem. [[5]]

@q 11
Solve the Laplace equation $u_{xx} + u_{yy} = 0$ on a square grid with $0 \le x \le 2$ and $0 \le y \le 2$ with step-size $h = 2/3$ in both directions having the following boundary conditions.
$$\begin{gathered}u(x,0) = 240x,\qquad u(0,y) = 180y\\ u(x,2) = 180(2 - x),\qquad u(2,y) = 240(2 - y)\end{gathered}$$
[[5]]

@q 12
Solve the wave equation $u_{tt} = 4u_{xx}$ for 5 time steps taking $\Delta x = h = 0.4$ with the following boundary and initial conditions:
$$\begin{gathered}u(0,t) = u(2,t) = 0\\ u(x,0) = 5x(2 - x)\ \text{and}\ u_t(x,0) = 0.\end{gathered}$$
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
Let $F_1 = x^4 - \cos y - 12$ and $F_2 = \sin x + y^4 - 15$. Newton-Raphson for a system solves $J\,\Delta = -F$ and updates $(x, y) \leftarrow (x, y) + \Delta$, with the Jacobian

$$J = \begin{pmatrix} \partial F_1/\partial x & \partial F_1/\partial y \\ \partial F_2/\partial x & \partial F_2/\partial y \end{pmatrix} = \begin{pmatrix} 4x^3 & \sin y \\ \cos x & 4y^3 \end{pmatrix}.$$

**Iteration 1**, $(x_0, y_0) = (1.8, 1.8)$:
$F_1 = 10.4976 - (-0.22720) - 12 = -1.27520$, $F_2 = 0.97385 + 10.4976 - 15 = -3.52855$.

$$\begin{pmatrix} 23.3280 & 0.97385 \\ -0.22720 & 23.3280 \end{pmatrix}\begin{pmatrix}\Delta x\\ \Delta y\end{pmatrix} = \begin{pmatrix}1.27520\\ 3.52855\end{pmatrix} \Rightarrow \Delta x = 0.04833,\ \Delta y = 0.15173$$

$$(x_1, y_1) = (1.84833,\ 1.95173)$$

**Iteration 2**: $F = (0.04305,\ 0.47209)$, $J = \begin{pmatrix} 25.2580 & 0.92832 \\ -0.27398 & 29.7385\end{pmatrix}$ gives $\Delta = (-0.00112,\ -0.01589)$.

$$(x_2, y_2) = (1.84721,\ 1.93584)$$

**Iteration 3**: $F = (-0.00002,\ 0.00574)$, $\Delta = (0.000008,\ -0.000198)$.

$$(x_3, y_3) = (1.84722,\ 1.93565)$$

**Iteration 4**: $F \approx (0, 10^{-6})$, no change in the sixth decimal.

| Iter | $x$ | $y$ | $F_1$ | $F_2$ |
|---|---|---|---|---|
| 0 | 1.80000 | 1.80000 | −1.27520 | −3.52855 |
| 1 | 1.84833 | 1.95173 | 0.04305 | 0.47209 |
| 2 | 1.84721 | 1.93584 | −0.00002 | 0.00574 |
| 3 | 1.84722 | 1.93565 | 0.00000 | 0.00000 |

Two successive iterates agree to three decimals (from iteration 2 to 3: $1.847$ and $1.936$).

$$\boxed{x \approx 1.847,\qquad y \approx 1.936}$$

@s 3
**Method.** Form the augmented matrix $[A\,|\,b]$. For each column $i$: (1) choose the pivot (largest $|a_{ri}|$, $r \ge i$, to limit round-off), swap it to row $i$; (2) divide row $i$ by the pivot so that $a_{ii} = 1$; (3) subtract a multiple of row $i$ from **every other row** so the rest of column $i$ becomes $0$. At the end $[A\,|\,b] \to [I\,|\,x]$, so the last column is the solution (no back substitution is needed).

```python
def gauss_jordan(A, b):
    """Solve A x = b by Gauss-Jordan elimination with partial pivoting."""
    n = len(A)
    M = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]   # augmented matrix
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))             # partial pivoting
        if abs(M[p][i]) < 1e-12:
            raise ValueError("Matrix is singular: no unique solution")
        M[i], M[p] = M[p], M[i]
        piv = M[i][i]
        M[i] = [v / piv for v in M[i]]                               # make the pivot 1
        for r in range(n):                                           # clear the whole column
            if r != i:
                f = M[r][i]
                M[r] = [a - f * c for a, c in zip(M[r], M[i])]
    return [M[i][n] for i in range(n)]

if __name__ == "__main__":
    n = int(input("Number of unknowns: "))
    print("Enter the augmented matrix row by row (a1 ... an b):")
    A, b = [], []
    for _ in range(n):
        row = list(map(float, input().split()))
        A.append(row[:n]); b.append(row[n])
    for i, xi in enumerate(gauss_jordan(A, b), 1):
        print(f"x{i} = {xi:.6f}")
```

**Test run** (system $2x + y - z = 8,\ -3x - y + 2z = -11,\ -2x + y + 2z = -3$):

```
Number of unknowns: 3
2 1 -1 8
-3 -1 2 -11
-2 1 2 -3
x1 = 2.000000
x2 = 3.000000
x3 = -1.000000
```

The output is $(2, 3, -1)$, which satisfies all three equations. The program was executed to obtain this output.

@s 4
**Method.** Start with $x^{(0)} = (1, 1, 1)^T$. Repeat $y = A x^{(k)}$, $\lambda_k = $ the component of $y$ of largest magnitude, $x^{(k+1)} = y/\lambda_k$.

| $k$ | $A x^{(k)}$ | $\lambda_k$ | $x^{(k+1)}$ |
|---|---|---|---|
| 0 | (12, 12, 14) | 14 | (0.85714, 0.85714, 1) |
| 1 | (11.14286, 11.14286, 12.28571) | 12.28571 | (0.90698, 0.90698, 1) |
| 2 | (11.44186, 11.44186, 12.88372) | 12.88372 | (0.88809, 0.88809, 1) |
| 3 | (11.32852, 11.32852, 12.65704) | 12.65704 | (0.89504, 0.89504, 1) |
| 4 | (11.37022, 11.37022, 12.74044) | 12.74044 | (0.89245, 0.89245, 1) |
| 5 | (11.35471, 11.35471, 12.70941) | 12.70941 | (0.89341, 0.89341, 1) |
| 6 | (11.36046, 11.36046, 12.72091) | 12.72091 | (0.89305, 0.89305, 1) |
| 7 | (11.35832, 11.35832, 12.71664) | 12.71664 | (0.89319, 0.89319, 1) |
| 8 | (11.35911, 11.35911, 12.71823) | 12.71823 | (0.89314, 0.89314, 1) |

The eigenvalue estimates settle at $12.72$ and the vector at $(0.893, 0.893, 1)^T$.

$$\boxed{\lambda_{max} \approx 12.72,\qquad v \approx (0.893,\ 0.893,\ 1)^T}$$

**Exact check.** The vector has the form $(a, a, 1)$. Rows 1 and 3 give $\lambda a = 6a + 6$ and $\lambda = 12a + 2$, so $6a^2 - 2a - 3 = 0$, $a = \dfrac{1 + \sqrt{19}}{6} = 0.8931$ and $\lambda = 4 + 2\sqrt{19} = 12.7178$. ✓ (The other eigenvalues are $-2$ and $4 - 2\sqrt{19} = -4.718$, smaller in magnitude, so the method converges.)

@s 5
For $y = ax^2 + bx + c$ the normal equations (from $\partial S/\partial a = \partial S/\partial b = \partial S/\partial c = 0$ with $S = \sum (y_i - ax_i^2 - bx_i - c)^2$) are

$$\begin{gathered}\sum y = a\sum x^2 + b\sum x + nc\\ \sum xy = a\sum x^3 + b\sum x^2 + c\sum x\\ \sum x^2y = a\sum x^4 + b\sum x^3 + c\sum x^2\end{gathered}$$

| $x$ | $y$ | $x^2$ | $x^3$ | $x^4$ | $xy$ | $x^2y$ |
|---|---|---|---|---|---|---|
| 2 | 2.5 | 4 | 8 | 16 | 5.0 | 10.0 |
| 4 | 2.7 | 16 | 64 | 256 | 10.8 | 43.2 |
| 6 | 3.5 | 36 | 216 | 1296 | 21.0 | 126.0 |
| 8 | 6.5 | 64 | 512 | 4096 | 52.0 | 416.0 |
| 10 | 5.4 | 100 | 1000 | 10000 | 54.0 | 540.0 |
| 12 | 4.8 | 144 | 1728 | 20736 | 57.6 | 691.2 |
| **Σ = 42** | **25.4** | **364** | **3528** | **36400** | **200.4** | **1826.4** |

Substituting ($n = 6$):

$$\begin{gathered}364a + 42b + 6c = 25.4\\ 3528a + 364b + 42c = 200.4\\ 36400a + 3528b + 364c = 1826.4\end{gathered}$$

Solving (elimination of $c$, then of $b$):

$$\begin{gathered}a = -0.05179\\ b = 1.04786\\ c = 0.04000\end{gathered}$$

$$\boxed{y = -0.0518\,x^2 + 1.0479\,x + 0.0400}$$

Check: the residuals $y_i - \hat y_i$ sum to zero, as least squares requires.

@s 6
**Divided differences** $f[x_i, \dots, x_{i+k}] = \dfrac{f[x_{i+1},\dots,x_{i+k}] - f[x_i,\dots,x_{i+k-1}]}{x_{i+k} - x_i}$.

| $x$ | $y$ | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|---|
| 2 | **8.10** | | | | |
| | | **−0.46** | | | |
| 5 | 6.72 | | **0.09** | | |
| | | −0.01 | | **0.06** | |
| 7 | 6.70 | | 0.45 | | **0** |
| | | 1.34 | | 0.06 | |
| 8 | 8.04 | | 0.75 | | |
| | | 3.59 | | | |
| 10 | 15.22 | | | | |

Computation: $\dfrac{6.72 - 8.10}{3} = -0.46$, $\dfrac{6.70 - 6.72}{2} = -0.01$, $\dfrac{8.04 - 6.70}{1} = 1.34$, $\dfrac{15.22 - 8.04}{2} = 3.59$; second: $\dfrac{-0.01 + 0.46}{5} = 0.09$, $\dfrac{1.34 + 0.01}{3} = 0.45$, $\dfrac{3.59 - 1.34}{3} = 0.75$; third: $\dfrac{0.45 - 0.09}{6} = 0.06$, $\dfrac{0.75 - 0.45}{5} = 0.06$; fourth: $0$.

The third differences are constant, so the data come from a cubic. Newton's formula:

$$y(x) = 8.10 - 0.46(x - 2) + 0.09(x - 2)(x - 5) + 0.06(x - 2)(x - 5)(x - 7)$$

At $x = 9$:

$$y(9) = 8.10 - 0.46(7) + 0.09(7)(4) + 0.06(7)(4)(2) = 8.10 - 3.22 + 2.52 + 3.36$$

$$\boxed{y(9) = 10.76}$$

@s 7
Let the points be equally spaced, $x_i = x_0 + ih$, with forward differences $\Delta y_0, \Delta^2 y_0, \dots$ and $p = \dfrac{x - x_0}{h}$. **Newton's forward formula** is

$$y = y_0 + p\,\Delta y_0 + \frac{p(p-1)}{2!}\Delta^2 y_0 + \frac{p(p-1)(p-2)}{3!}\Delta^3 y_0 + \frac{p(p-1)(p-2)(p-3)}{4!}\Delta^4 y_0 + \cdots$$

Since $\dfrac{dp}{dx} = \dfrac1h$, differentiate term by term with respect to $p$. Expanding $p(p-1) = p^2 - p$, $p(p-1)(p-2) = p^3 - 3p^2 + 2p$, $p(p-1)(p-2)(p-3) = p^4 - 6p^3 + 11p^2 - 6p$:

**First derivative**

$$\frac{dy}{dx} = \frac{1}{h}\frac{dy}{dp} = \frac1h\left[\Delta y_0 + \frac{2p - 1}{2}\Delta^2 y_0 + \frac{3p^2 - 6p + 2}{6}\Delta^3 y_0 + \frac{4p^3 - 18p^2 + 22p - 6}{24}\Delta^4 y_0 + \cdots\right]$$

**Second derivative**

$$\frac{d^2y}{dx^2} = \frac{1}{h^2}\frac{d^2y}{dp^2} = \frac1{h^2}\left[\Delta^2 y_0 + (p - 1)\Delta^3 y_0 + \frac{6p^2 - 18p + 11}{12}\Delta^4 y_0 + \cdots\right]$$

**At a tabulated point** $x = x_0$ ($p = 0$) these reduce to the working formulas

$$\boxed{y'_0 = \frac1h\left[\Delta y_0 - \frac12\Delta^2 y_0 + \frac13\Delta^3 y_0 - \frac14\Delta^4 y_0 + \cdots\right]}$$

$$\boxed{y''_0 = \frac1{h^2}\left[\Delta^2 y_0 - \Delta^3 y_0 + \frac{11}{12}\Delta^4 y_0 - \frac56\Delta^5 y_0 + \cdots\right]}$$

(The next term in $y'_0$ is $+\tfrac15\Delta^5y_0$.) These formulas are most accurate near the start of the table; for the end of a table use Newton's backward formula.

@s 8
Transform $[1, 2]$ to $[-1, 1]$: $x = \dfrac{1+2}{2} + \dfrac{2-1}{2}t = 1.5 + 0.5t$, $dx = 0.5\,dt$.

$$I = 0.5\int_{-1}^{1} e^{\sin(1.5 + 0.5t)}\,dt \approx 0.5\sum_{i=1}^{3} w_i\,g(t_i)$$

The 3-point Gauss-Legendre data are $t = -\sqrt{3/5},\ 0,\ +\sqrt{3/5}$ with $w = \tfrac59,\ \tfrac89,\ \tfrac59$.

| $t_i$ | $w_i$ | $x_i = 1.5 + 0.5t_i$ | $g = e^{\sin x_i}$ |
|---|---|---|---|
| −0.774597 | 5/9 | 1.112702 | 2.451982 |
| 0 | 8/9 | 1.500000 | 2.711481 |
| +0.774597 | 5/9 | 1.887298 | 2.586563 |

$$I \approx 0.5\left[\tfrac59(2.451982) + \tfrac89(2.711481) + \tfrac59(2.586563)\right] = 0.5\,[1.362212 + 2.410205 + 1.437091]$$

$$\boxed{I \approx 2.6047}$$

(The exact value of the integral, by high-precision quadrature, is $2.60466$, so the error is about $4\times10^{-5}$.)

@s 9
$f(x, y) = \sin\pi x + \cos y$, $h = 0.5$, $y_0 = 2$. RK4:
$k_1 = hf(x, y)$, $k_2 = hf(x + \tfrac h2, y + \tfrac{k_1}2)$, $k_3 = hf(x + \tfrac h2, y + \tfrac{k_2}2)$, $k_4 = hf(x + h, y + k_3)$, $y_{new} = y + \tfrac16(k_1 + 2k_2 + 2k_3 + k_4)$.

**Step 1** ($x = 0,\ y = 2$):

$$k_1 = 0.5[\sin 0 + \cos 2] = 0.5(-0.41615) = -0.20807$$

$$k_2 = 0.5[\sin(0.25\pi) + \cos(1.89596)] = 0.5[0.70711 - 0.31946] = 0.19382$$

$$k_3 = 0.5[\sin(0.25\pi) + \cos(2.09691)] = 0.5[0.70711 - 0.50218] = 0.10246$$

$$k_4 = 0.5[\sin(0.5\pi) + \cos(2.10246)] = 0.5[1 - 0.50697] = 0.24651$$

$$y(0.5) = 2 + \tfrac16[-0.20807 + 0.38764 + 0.20492 + 0.24651] = 2.10517$$

**Step 2** ($x = 0.5,\ y = 2.10517$):

$$k_1 = 0.5[1 + \cos 2.10517] = 0.24535,\quad k_2 = 0.5[\sin(0.75\pi) + \cos(2.22785)] = 0.04816$$

$$k_3 = 0.5[0.70711 + \cos(2.12925)] = 0.08862,\quad k_4 = 0.5[\sin\pi + \cos(2.19379)] = -0.29173$$

$$y(1) = 2.10517 + \tfrac16[0.24535 + 0.09632 + 0.17724 - 0.29173] = 2.14303$$

| $x$ | 0 | 0.5 | 1.0 |
|---|---|---|---|
| $y$ | 2 | **2.1052** | **2.1430** |

@s 10
Because the differential equation is **linear**, the end value $y(2)$ obtained with Euler's method is a linear function of the guessed slope $m$. So the slope that hits $y(2) = 8$ follows from linear interpolation (secant step), and it is *exact* for the Euler scheme:

$$m = m_1 + \frac{8 - y(m_1)}{y(m_2) - y(m_1)}(m_2 - m_1) = 1 + \frac{8 - 4.7187}{11.5938 - 4.7187}(3 - 1) = 1 + \frac{3.2813}{6.8751}(2)$$

$$\boxed{m = y'(0) \approx 1.9545}$$

**Final run** with Euler's formula, $h = 0.5$. Put $v = y'$ so $v' = y'' = 0.5x - y + v + 3$; $y_{i+1} = y_i + hv_i$, $v_{i+1} = v_i + h\,v'_i$:

| $x$ | $y$ | $v = y'$ | $y'' = 0.5x - y + v + 3$ |
|---|---|---|---|
| 0 | 5.00000 | 1.95455 | −0.04545 |
| 0.5 | 5.97727 | 1.93182 | −0.79545 |
| 1.0 | 6.94318 | 1.53409 | −1.90909 |
| 1.5 | 7.71023 | 0.57955 | −3.38068 |
| 2.0 | **8.00000** | −1.11079 | |

The boundary condition $y(2) = 8$ is met. (As a check, the same scheme with $m = 1$ and $m = 3$ reproduces the tabulated $4.7187$ and $11.5938$.)

$$\boxed{y(0.5) = 5.977,\ \ y(1.0) = 6.943,\ \ y(1.5) = 7.710,\ \ y(2.0) = 8.000}$$

@s 11
Step $h = 2/3$; the interior nodes are $u_1 = u(\tfrac23,\tfrac23)$, $u_2 = u(\tfrac43,\tfrac23)$, $u_3 = u(\tfrac23,\tfrac43)$, $u_4 = u(\tfrac43,\tfrac43)$. Laplace's equation becomes the five-point rule $u_{i,j} = \tfrac14(u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1})$.

**Boundary values** ($x$ or $y$ equal to $0, \tfrac23, \tfrac43, 2$):

| Edge | at $\tfrac23$ | at $\tfrac43$ |
|---|---|---|
| bottom $u(x, 0) = 240x$ | 160 | 320 |
| top $u(x, 2) = 180(2 - x)$ | 240 | 120 |
| left $u(0, y) = 180y$ | 120 | 240 |
| right $u(2, y) = 240(2 - y)$ | 320 | 160 |

**Equations**

$$\begin{gathered}4u_1 = u_2 + u_3 + 120 + 160\\ 4u_2 = u_1 + u_4 + 320 + 320\\ 4u_3 = u_1 + u_4 + 240 + 240\\ 4u_4 = u_2 + u_3 + 160 + 120\end{gathered}$$

The system is symmetric under $u_1 \leftrightarrow u_4$: put $u_1 = u_4 = a$. Then $u_2 = \dfrac{2a + 640}{4}$, $u_3 = \dfrac{2a + 480}{4}$, and $4a = u_2 + u_3 + 280 = a + 280 + 280 \Rightarrow a = \dfrac{560}{3}$.

$$\boxed{u_1 = u_4 = 186.67,\qquad u_2 = 253.33,\qquad u_3 = 213.33}$$

(Gauss-Seidel iteration from zero converges to the same values; the direct solution is exact for this $4\times4$ system.)

@s 12
**Scheme.** For $u_{tt} = c^2u_{xx}$ with $c^2 = 4$ ($c = 2$), replace both derivatives by central differences, with $\lambda = ck/h$:

$$\frac{u_{i,j+1} - 2u_{i,j} + u_{i,j-1}}{k^2} = c^2\frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{h^2}$$

Choose the time step $k = h/c = 0.2$, so $\lambda = 1$ (the best stable choice, since stability needs $\lambda\le1$). The $-2u_{i,j}$ terms cancel:

$$u_{i,j+1} = u_{i+1,j} + u_{i-1,j} - u_{i,j-1}$$

**Start-up.** The condition $u_t(x, 0) = 0$ gives $u_{i,-1} = u_{i,1}$ (central difference), and the formula at $j = 0$ yields

$$u_{i,1} = \tfrac12\left(u_{i+1,0} + u_{i-1,0}\right).$$

**Data.** $x_i = 0, 0.4, 0.8, 1.2, 1.6, 2.0$, $u_{i,0} = 5x_i(2 - x_i) = 0,\ 3.2,\ 4.8,\ 4.8,\ 3.2,\ 0$; the end values stay $0$.

| $t$ | $j$ | $x = 0$ | 0.4 | 0.8 | 1.2 | 1.6 | 2.0 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 3.2 | 4.8 | 4.8 | 3.2 | 0 |
| 0.2 | 1 | 0 | 2.4 | 4.0 | 4.0 | 2.4 | 0 |
| 0.4 | 2 | 0 | 0.8 | 1.6 | 1.6 | 0.8 | 0 |
| 0.6 | 3 | 0 | −0.8 | −1.6 | −1.6 | −0.8 | 0 |
| 0.8 | 4 | 0 | −2.4 | −4.0 | −4.0 | −2.4 | 0 |
| 1.0 | 5 | 0 | −3.2 | −4.8 | −4.8 | −3.2 | 0 |

Sample calculations: $u_{1,1} = \tfrac12(4.8 + 0) = 2.4$; $u_{1,2} = u_{2,1} + u_{0,1} - u_{1,0} = 4.0 + 0 - 3.2 = 0.8$; $u_{2,2} = 4.0 + 2.4 - 4.8 = 1.6$.

**Check with d'Alembert.** $u = \tfrac12[f(x + 2t) + f(x - 2t)]$ with $f$ the odd, 4-periodic extension of $5x(2 - x)$. At $x = 0.4,\ t = 1$: $\tfrac12[f(2.4) + f(-1.6)] = \tfrac12[-3.2 - 3.2] = -3.2$ ✓. The string has gone through half a period and is inverted.

```figure caption="Wave profiles at $t = 0, 0.4, 0.6, 1.0$ from the finite-difference table: the initial hump splits, collapses and returns inverted."
import numpy as np, matplotlib.pyplot as plt
x=np.arange(0,2.01,0.4)
rows={"t = 0":[0,3.2,4.8,4.8,3.2,0],"t = 0.4":[0,0.8,1.6,1.6,0.8,0],"t = 0.6":[0,-0.8,-1.6,-1.6,-0.8,0],"t = 1.0":[0,-3.2,-4.8,-4.8,-3.2,0]}
fig,ax=plt.subplots(figsize=(5.2,2.6))
for (k,v),c in zip(rows.items(),SERIES): ax.plot(x,v,'o-',color=c,label=k,ms=3.5)
ax.axhline(0,color=INK,lw=0.6); ax.set_xlabel("x"); ax.set_ylabel("u(x, t)"); ax.legend(ncol=4,loc="upper center",bbox_to_anchor=(0.5,1.18)); ax.grid(True)
```

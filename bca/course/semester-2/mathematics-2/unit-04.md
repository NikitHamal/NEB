---
subject: Mathematics II
grade: BCA Semester 2
unit: 4
title: Eigenvalues, Eigenvectors and Diagonalisation
area: BCA 154 · Mathematics II · Unit 4
---

Most vectors change direction when a matrix acts on them. **Eigenvectors** do not: they are only stretched. These special directions reveal what a transformation really does, and they power Google's PageRank, principal component analysis, vibration analysis and the stability of dynamical systems.

::: key What this unit gives you
- Eigenvalues and eigenvectors: definition, characteristic equation, computation.
- Properties (trace, determinant), Cayley–Hamilton theorem.
- Diagonalisation and matrix powers; symmetric matrices.
- Applications: Markov chains, Fibonacci, PageRank, principal components.
:::

## 4.1 Eigenvalues and eigenvectors

A non-zero vector *v* is an **eigenvector** of a square matrix A with **eigenvalue** *λ* if **Av = $\lambda v$**. Rewrite as $(A - \lambda I) v = 0$; a non-zero solution exists iff $\det (A - \lambda I) = 0$, the **characteristic equation**. For an $n \times n$ matrix it is a polynomial of degree *n*, so there are *n* eigenvalues counting multiplicity (possibly complex).

**Procedure:** (1) solve $\det (A - \lambda I) = 0$ for *λ*; (2) for each *λ* solve $(A - \lambda I) v = 0$; the non-zero solutions are the eigenvectors (the **eigenspace**).

::: example Worked example
$A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$. $\det (A - \lambda I) = (4 - \lambda) (3 - \lambda) - 2 = \lambda^{2} - 7 \lambda + 10 = (\lambda - 5) (\lambda - 2)$, so **$\lambda = 5$, 2**.

$\lambda = 5$: A − 5I = $\begin{bmatrix} - 1 & 1 \\ 2 & - 2 \end{bmatrix} \Rightarrow - x + y = 0 \Rightarrow v$ = **(1, 1)**. Check: $A (1 ,\  1) = (5 ,\  5) = 5 ( 1$, 1) ✓.

$\lambda = 2$: A − 2I = $\begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix} \Rightarrow 2 x + y = 0 \Rightarrow v$ = **(1, −2)**. Check: $A (1 ,\  - 2) = (2 ,\  - 4) = 2 (1 ,\  - 2)$ ✓.
:::

::: example Worked example: a 3 × 3 with repeated eigenvalue
$A = \begin{bmatrix} 2 & 0 & 0 \\ 0 & 3 & 4 \\ 0 & 4 & 9 \end{bmatrix}$ has $\det (A - \lambda I) = (2 - \lambda) ((3 - \lambda) (9 - \lambda) - 16) = (2 - \lambda) (\lambda^{2} - 12 \lambda + 11) = (2 - \lambda) (\lambda - 1) (\lambda - 11)$; eigenvalues **2, 1, 11**.
:::

**Properties.** Sum of eigenvalues = **trace** (sum of the diagonal): $5 + 2 = 7 = 4 + 3$ ✓. Product of eigenvalues = **determinant**: $5 \cdot 2 = 10 = 12 - 2$ ✓. A is invertible iff 0 is not an eigenvalue. Eigenvalues of $A^{k}$ are $\lambda^{k}$; of $A^{-1}$ are $\frac{1}{\lambda}$; of $A^{T}$ the same as A; of a triangular matrix the diagonal entries. Eigenvectors for *distinct* eigenvalues are linearly independent. **Cayley–Hamilton:** a matrix satisfies its own characteristic equation: for the example, $A^{2}$ − 7A + 10I = 0 (check: $A^{2} = \begin{bmatrix} 18 & 7 \\ 14 & 11 \end{bmatrix}$; 7A = $\begin{bmatrix} 28 & 7 \\ 14 & 21 \end{bmatrix} ;\  A^{2}$ − 7A + 10I = $\begin{bmatrix} 18 - 28 + 10 & 0 \\ 0 & 11 - 21 + 10 \end{bmatrix} = 0$ ✓). It gives $A^{-1}$ = (7I − $A ) / 10$ quickly.

## 4.2 Diagonalisation

A is **diagonalisable** if there is an invertible P and a diagonal D with **A = PDP⁻¹**: the columns of P are *n* independent eigenvectors and D has the eigenvalues. It happens iff A has *n* independent eigenvectors (guaranteed when the *n* eigenvalues are distinct).

::: example Worked example: powers
For A above: $P = \begin{bmatrix} 1 & 1 \\ 1 & - 2 \end{bmatrix} ,\  D$ = diag(5, $2 ) ,\  P^{-1} = \left( \frac{1}{- 3} \right) \begin{bmatrix} - 2 & - 1 \\ - 1 & 1 \end{bmatrix} = \begin{bmatrix} \frac{2}{3} & \frac{1}{3} \\ \frac{1}{3} & - \frac{1}{3} \end{bmatrix}$.

**$A^{5} = P D^{5} P^{-1}$** with $D^{5}$ = diag(3125, 32): $P D^{5} = \begin{bmatrix} 3125 & 32 \\ 3125 & - 64 \end{bmatrix}$, and multiplying by $P^{-1}$ gives **$A^{5} = \begin{bmatrix} 2094 & 1031 \\ 2062 & 1063 \end{bmatrix}$**. Check: the trace is $3157 = 3125 + 32$ ✓. Raising A to the power 5 directly needs four matrix products; diagonalisation makes **$A^{n} = P D^{n} P^{-1}$** a one-line computation for any *n*.
:::

**Not every matrix is diagonalisable**: $\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ has the single eigenvalue 1 (repeated) and only one independent eigenvector (1, 0); it is a *defective* matrix (a shear). The general fix is the **Jordan form**, outside this course.

**Symmetric matrices** $(A = A^{T})$ are special: all eigenvalues are real, eigenvectors of different eigenvalues are **orthogonal**, and they are always diagonalisable by an **orthogonal** P (**spectral theorem**): A = QDQᵀ. Example: $\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ has $\lambda = 3$ (eigenvector $\frac{1 ,\  1}{\sqrt{2}}$) and $\lambda = 1$ (eigenvector $\frac{1 ,\  - 1}{\sqrt{2}}$). A symmetric matrix is **positive definite** if all eigenvalues are > 0 (energy and covariance matrices).

## 4.3 Applications

**Fibonacci in matrix form.** $\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}$ⁿ = $\begin{bmatrix} F_{n+1} & F_{n} \\ F_{n} & F_{n-1} \end{bmatrix}$. Its eigenvalues solve $\lambda^{2} = \lambda + 1$, i.e. $\lambda = \frac{1 \pm \sqrt{5}}{2}$, so diagonalisation gives Binet's formula (Discrete Structure, Unit 4), and $F_{10} = 55$ follows from the 10th power.

**Markov chains.** A **stochastic matrix** P (rows sum to 1) gives the probabilities of moving between states. If the weather is "dry" or "wet" with $P = \begin{bmatrix} 0.9 & 0.1 \\ 0.5 & 0.5 \end{bmatrix}$, the long-run proportions *π* satisfy $\pi P = \pi$, i.e. *π* is a left eigenvector for $\lambda = 1$: $0.1 \pi_{1} = 0.5 \pi_{2} \Rightarrow \pi_{1} = 5 \pi_{2}$, so with $\pi_{1} + \pi_{2} = 1$, **$\pi = \left( \frac{5}{6} ,\  \frac{1}{6} \right)$**: in the long run, 83 % of days are dry. The other eigenvalue is 0.4, so the chain converges geometrically at rate $0.4^{n}$.

**PageRank.** The rank of web pages is the principal eigenvector of the (damped) link matrix: a page is important if important pages link to it. It is found by **power iteration**: multiply a vector by the matrix repeatedly, and it converges to the dominant eigenvector. Example: starting from (1, 0) and applying $A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$: (4, 2), (18, 14), (86, 70), … the ratio tends to (1, 1)-direction: $\frac{86}{70} = 1.23$, then slowly towards 1 ($5^{n}$ dominates $2^{n}$).

**Principal component analysis (PCA).** For data, form the covariance matrix (symmetric); its eigenvectors with the largest eigenvalues are the directions of greatest variance. Keeping the top *k* reduces dimensions with minimal information loss (image compression, face recognition, visualising data).

**Systems of differential equations and stability.** $x'$ = Ax has solutions made of $e^{\lambda t} v$; the system is stable (solutions decay) if all eigenvalues have negative real parts. **Vibrations** of a structure are governed by eigenvalues (natural frequencies). **Graph theory:** the eigenvalues of a graph's adjacency matrix describe its connectivity.

## 4.4 What an eigenvector looks like

Most vectors are turned and stretched when a matrix acts on them. An **eigenvector** is special: the matrix only stretches it along its own line, by the factor *λ*. Figure 4.1 shows $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ acting on the unit circle. Every point of the circle goes to an ellipse; the ellipse's long axis lies along the eigenvector (1, 1), stretched by $\lambda = 3$, and its short axis along (1, −1), stretched by $\lambda = 1$. A symmetric matrix always has such perpendicular axes, which is why principal-component analysis of data works.

```svgfig label="4.1" caption="The matrix $\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$ maps the unit circle (dashed) to an ellipse. The eigenvector (1,1) is stretched by 3 and the perpendicular eigenvector (1,-1) by 1; these are the principal axes of the ellipse."
import math
f = Fig(580, 240)
cx, cy, u = 290, 120, 36
circ = [(cx + u * math.cos(t / 30 * 2 * math.pi), cy - u * math.sin(t / 30 * 2 * math.pi)) for t in range(30)]
ell = []
for t in range(60):
    a = t / 60 * 2 * math.pi
    x, y = math.cos(a), math.sin(a)
    X, Y = 2 * x + y, x + 2 * y
    ell.append((cx + u * X, cy - u * Y))
f.poly(ell, fill=BLUE, stroke=NAVY)
f.poly(circ, fill="#ffffff", stroke=SLATE)
f.line(cx - 95, cy + 95, cx + 95, cy - 95, color=RED, sw=1.2, dash=True)
f.line(cx - 60, cy - 60, cx + 60, cy + 60, color=TEAL, sw=1.2, dash=True)
f.arrow([(cx, cy), (cx + 3 * u / 1.414 * 1.0 * 1.0, cy - 3 * u / 1.414)], color=RED, sw=2.6)
f.arrow([(cx, cy), (cx + u / 1.414, cy + u / 1.414)], color=TEAL, sw=2.6)
f.text(cx + 100, cy - 90, "lambda = 3 along (1, 1)", size=11, color=RED, bold=True, anchor="start")
f.text(cx + 52, cy + 62, "lambda = 1 along (1, -1)", size=11, color=TEAL, bold=True, anchor="start")
f.text(cx, 232, "unit circle (white) becomes an ellipse (blue)", size=10.5, color=SLATE, italic=True)
```

## 4.5 Eight uses of eigenvalues

1. **Ranking web pages.** PageRank is the eigenvector for the eigenvalue 1 of the web's link matrix. The largest component belongs to the page that many important pages point to. A search engine finds it by repeated multiplication.
2. **Markov chains and long-run forecasts.** If tomorrow's weather depends only on today's, the chain has a steady state that is the eigenvector for $\lambda = 1$ (Section 4.3 and the answers below). It predicts the long-run share of sunny days, customers or users.
3. **Principal component analysis (PCA).** The eigenvectors of a data covariance matrix point along the directions of greatest spread. Keeping the top few reduces hundreds of columns to two or three. Face recognition and survey analysis use it.
4. **Vibrations and earthquakes.** The natural frequencies of a building or bridge are the square roots of eigenvalues of its stiffness matrix. If shaking from an earthquake matches one, resonance can be destructive. Engineers in Nepal check this for tall buildings.
5. **Population growth.** In a Leslie matrix, the dominant eigenvalue is the long-run growth factor per period, and its eigenvector is the stable age distribution. Planners use this to project school and health needs.
6. **Stability of systems.** For $x'$ = Ax, all eigenvalues with negative real part mean the system settles. Control engineers choose a controller by moving eigenvalues. Cruise control and drone stabilisation rely on this.
7. **Image and data compression.** The singular-value decomposition, built from eigenvalues of $A^{T} A$, stores a picture with a few large values and drops the rest. Recommenders and photo apps compress this way.
8. **Quantum and physical systems.** Energy levels of atoms are eigenvalues of an operator; the allowed states are eigenvectors. The idea that measurement gives eigenvalues is the heart of quantum mechanics.

```photogrid label="4.1" cols="2" ratio="1.2" caption="Every structure has its own favourite frequencies. (a) The Tacoma Narrows Bridge twisting in the wind on 7 November 1940, an event that made engineers compute the natural frequencies of bridges: those frequencies are square roots of eigenvalues. (b) Two equal masses joined by three equal springs have the stiffness matrix $K = \begin{bmatrix} 2 & - 1 \\ - 1 & 2 \end{bmatrix}$. Its eigenvalues are 1 and 3 with eigenvectors (1, 1) and (1, -1): in the first mode both masses swing together at angular frequency 1.00, and in the second they swing in opposite directions at sqrt(3) = 1.73, faster. A wind that pushes at one of these frequencies adds energy every cycle, which is resonance. The values are computed in the figure with eigh."
@ photo id="bcamath/tacoma" cap="Tacoma Narrows Bridge twisting, 1940"
fit 1.2
focus 0.5 0.4
@ svg cap="Two normal modes of a 2-mass, 3-spring system"
import numpy as np
K = np.array([[2.0, -1.0], [-1.0, 2.0]])
w, V = np.linalg.eigh(K)
assert np.allclose(w, [1, 3]) and np.allclose(np.abs(V[:, 0]), [2 ** -.5, 2 ** -.5])
assert np.allclose(K @ V[:, 0], 1 * V[:, 0]) and np.allclose(K @ V[:, 1], 3 * V[:, 1])
assert round(float(np.sqrt(w[1])), 2) == 1.73 and V[0, 0] * V[1, 0] > 0 and V[0, 1] * V[1, 1] < 0
f = Fig(300, 240)
def row(y, d1, d2, title, col):
    f.text(150, y - 34, title, size=10.5, color=col, bold=True)
    x1, x2 = 100, 200
    f.line(20, y, x1 + d1, y, color=SLATE, sw=1.6); f.line(x1 + d1, y, x2 + d2, y, color=SLATE, sw=1.6); f.line(x2 + d2, y, 280, y, color=SLATE, sw=1.6)
    f.line(20, y - 14, 20, y + 14, color=SLATE, sw=3); f.line(280, y - 14, 280, y + 14, color=SLATE, sw=3)
    for x in (x1, x2): f.line(x, y - 20, x, y + 20, color="#94a3b8", sw=1, dash=True)
    f.circle(x1 + d1, y, 13, fill=BLUE, stroke=NAVY, label="m", size=10.5); f.circle(x2 + d2, y, 13, fill=BLUE, stroke=NAVY, label="m", size=10.5)
row(70, 16, 16, "mode 1: eigenvalue 1, vector (1, 1), w = 1.00", TEAL)
row(150, 16, -16, "mode 2: eigenvalue 3, vector (1, -1), w = 1.73", RED)
f.text(150, 206, "dashed = rest positions; solid = displaced", size=10.5, color=SLATE)
f.text(150, 226, "K v = lambda v checked for both modes", size=10.5, color=NAVY, bold=True)
```

```photogrid label="4.2" cols="2" ratio="1.2" caption="Ranking the web is an eigenvector problem. (a) Andrey Markov, who in 1906 studied chains in which the next state depends only on the present one; a random web surfer is such a chain. (b) Four pages with links A to B and C, B to C, C to A, and D to C. With a 0.85 chance of following a link and 0.15 of jumping to a random page, repeating $r = 0.0375 + 0.85 M r$ (the power method) converges in 41 steps to the PageRank vector (0.3725, 0.1958, 0.3941, 0.0375), which adds to 1. It is the eigenvector of the Google matrix for the eigenvalue 1, confirmed with a direct eigen-solver. C wins because three pages point to it, and D, which nobody links to, gets only the 0.0375 minimum."
@ photo id="bcamath/markov" cap="Andrey Markov (Markov chains)"
fit 1.2
focus 0.5 0.35
@ svg cap="PageRank of four pages by the power method"
import numpy as np
links = {0: [1, 2], 1: [2], 2: [0], 3: [2]}; N = 4; d = 0.85
M = np.zeros((N, N))
for j, o in links.items():
    for i in o: M[i, j] = 1 / len(o)
r = np.ones(N) / N; it = 0
while True:
    r2 = (1 - d) / N + d * M @ r; it += 1
    if abs(r2 - r).sum() < 1e-9: r = r2; break
    r = r2
G = (1 - d) / N + d * M
w, v = np.linalg.eig(G); k = int(np.argmax(w.real)); e = v[:, k].real; e = e / e.sum()
assert it == 41 and abs(r.sum() - 1) < 1e-9 and np.allclose(r, e, atol=1e-6) and abs(w[k].real - 1) < 1e-9
assert [round(x, 4) for x in r] == [0.3725, 0.1958, 0.3941, 0.0375]
f = Fig(300, 240)
pos = {0: (70, 60), 1: (230, 60), 2: (230, 150), 3: (70, 150)}
names = "ABCD"
import math
def edge(a, b, rad):
    ax, ay = pos[a]; bx, by = pos[b]; dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy); u = (dx / L, dy / L)
    f.arrow([(ax + u[0] * rad[0], ay + u[1] * rad[0]), (bx - u[0] * rad[1], by - u[1] * rad[1])], color=SLATE, sw=1.6)
rad = {i: 12 + 60 * r[i] for i in range(N)}
for j, o in links.items():
    for i in o: edge(j, i, (rad[j], rad[i]))
for i in range(N):
    f.circle(*pos[i], rad[i], fill=(MINT if i == 2 else BLUE), stroke=(TEAL if i == 2 else NAVY), label=names[i], size=12)
    f.text(pos[i][0], pos[i][1] + rad[i] + 14, f"{r[i]:.4f}", size=10.5, color=(TEAL if i == 2 else NAVY), bold=True)
f.text(150, 206, "power method: 41 steps; sum of ranks = 1", size=10.5, color=SLATE)
f.text(150, 226, "same as eigenvector for eigenvalue 1", size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

- Av = $\lambda v ;\  \det (A - \lambda I) = 0$; eigenspace = null space of $A - \lambda I$.
- $\sum \lambda$ = trace; $\prod \lambda = \det$. Eigenvalues of $A^{k}$: $\lambda^{k}$; of $A^{-1}$: $\frac{1}{\lambda}$.
- Cayley–Hamilton: $p (A) = 0$. A = PDP⁻¹ ⇒ Aⁿ = PDⁿP⁻¹.
- Symmetric: real eigenvalues, orthogonal eigenvectors, A = QDQᵀ.
- Markov steady state: $\pi P = \pi$ (eigenvalue 1). PageRank: power iteration.

## Chapter summary

- Eigenvectors are the directions a matrix only stretches; eigenvalues are the stretch factors.
- The characteristic polynomial finds them; trace and determinant give quick checks.
- Diagonalisation turns matrix powers into powers of numbers; symmetric matrices diagonalise orthogonally.
- Markov chains, PageRank, PCA, stability and vibration analysis are all eigenvalue problems.

## Practice

1. Find the eigenvalues and eigenvectors of $\begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$ and of $\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$.
2. Find the eigenvalues of $\begin{bmatrix} 1 & 2 & 3 \\ 0 & 4 & 5 \\ 0 & 0 & 6 \end{bmatrix}$ and the determinant.
3. If the eigenvalues of A are 2, 3 and 5, find $\det A ,\  t r A$, eigenvalues of $A^{2}$ and of $A^{-1}$.
4. Verify the Cayley–Hamilton theorem for $\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}$ and use it to find $A^{-1}$.
5. Diagonalise $\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ and find $A^{3}$.
6. Is $\begin{bmatrix} 2 & 1 \\ 0 & 2 \end{bmatrix}$ diagonalisable? Explain.
7. A 2-state Markov chain has $P = \begin{bmatrix} 0.7 & 0.3 \\ 0.4 & 0.6 \end{bmatrix}$. Find the steady state.
8. Show that the eigenvalues of a symmetric $2 \times 2$ matrix $\begin{bmatrix} a & b \\ b & c \end{bmatrix}$ are always real.
9. Find the eigenvalues of the rotation matrix $\begin{bmatrix} 0 & - 1 \\ 1 & 0 \end{bmatrix}$. Interpret.
10. A population model: young Y and adults A, with $Y_{n+1} = 2 A_{n} ,\  A_{n+1} = 0.5 Y_{n} + 0.6 A_{n}$. Find the long-term growth rate.

::: note Answers and worked solutions
**1.** $\begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$: triangular, $\lambda = 3 ( v = ( 1$, 0)) and $\lambda = 2 ( A$ − 2I = $\begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix} \Rightarrow v = (1 ,\  - 1)$). $\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$: $\lambda = 3 (v = (1 ,\  1)) ,\  \lambda = 1 (v = (1 ,\  - 1))$.

**2.** Triangular: **1, 4, 6**; $\det = 1 \cdot 4 \cdot 6$ = **24**.

**3.** det = 2·3·5 = **30**; trace = **10**; $A^{2}$ has $4 ,\  9 ,\  25 ;\  A^{-1}$ has $\frac{1}{2} ,\  \frac{1}{3} ,\  \frac{1}{5}$.

**4.** $t r = 5 ,\  \det = - 2$: $\lambda^{2} - 5 \lambda - 2 = 0$. $A^{2} = \begin{bmatrix} 7 & 10 \\ 15 & 22 \end{bmatrix} ;\  A^{2}$ − 5A − 2I = $\begin{bmatrix} 7 - 5 - 2 & 10 - 10 \\ 15 - 15 & 22 - 20 - 2 \end{bmatrix} = 0$ ✓. Then $A^{2}$ − 5A = 2I ⇒ $A ( A$ − 5I) = 2I ⇒ **$A^{-1} = \frac{A - 5 I}{2} = \begin{bmatrix} - 2 & 1 \\ 1.5 & - 0.5 \end{bmatrix}$**.

**5.** $P D P^{-1}$ as in §4.2. $A^{3} = P$ diag(125, 8) $P^{-1} = \begin{bmatrix} 125 & 8 \\ 125 & - 16 \end{bmatrix} \cdot \begin{bmatrix} \frac{2}{3} & \frac{1}{3} \\ \frac{1}{3} & - \frac{1}{3} \end{bmatrix} = \begin{bmatrix} \frac{250 + 8}{3} & \frac{125 - 8}{3} \\ \frac{250 - 16}{3} & \frac{125 + 16}{3} \end{bmatrix}$ = **$\begin{bmatrix} 86 & 39 \\ 78 & 47 \end{bmatrix}$**. (Trace $133 = 125 + 8$ ✓.)

**6.** **No**: $\lambda = 2$ is repeated but A − 2I = $\begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ has a one-dimensional null space, so there is only one independent eigenvector.

**7.** $\pi P = \pi$: $0.3 \pi_{1} = 0.4 \pi_{2} \Rightarrow \pi_{1} = \left( \frac{4}{3} \right) \pi_{2} ;\  \pi_{1} + \pi_{2} = 1 \Rightarrow \pi_{2} = \frac{3}{7}$. **$\pi = \left( \frac{4}{7} ,\  \frac{3}{7} \right) \approx ( 0.571$, 0.429)**.

**8.** $\lambda^{2} - (a + c) \lambda + (a c - b^{2}) = 0$ has discriminant $(a + c)^{2} - 4 (a c - b^{2}) = (a - c)^{2} + 4 b^{2} \geq 0$, so the roots are real.

**9.** $\lambda^{2} + 1 = 0 \Rightarrow \lambda = \pm i$ (complex): a rotation has no real direction that stays fixed (it turns every vector by $90 ^{\circ}$).

**10.** Matrix $\begin{bmatrix} 0 & 2 \\ 0.5 & 0.6 \end{bmatrix}$ acting on (Y, A): $\lambda^{2} - 0.6 \lambda - 1 = 0 \Rightarrow \lambda = \frac{0.6 + \sqrt{0.36 + 4}}{2} = \frac{0.6 + 2.088}{2}$ = **1.344**, so the population grows about 34 % per period (the other eigenvalue −0.744 dies out).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Find the eigenvalues and eigenvectors of $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, diagonalise it and find $A^{5}$.**

*Introduction.* *λ* is an eigenvalue of A if $\det (A - \lambda I) = 0$, and a non-zero vector *v* with Av = $\lambda v$ is the eigenvector.

*Characteristic equation.* $\det \begin{bmatrix} 2 - \lambda & 1 \\ 1 & 2 - \lambda \end{bmatrix} = (2 - \lambda)^{2} - 1 = \lambda^{2} - 4 \lambda + 3 = (\lambda - 1) (\lambda - 3) = 0$, so **$\lambda = 3$ and $\lambda = 1$**. Check: trace $4 = 3 + 1$ and $\det 3 = 3 \times 1$.

*Eigenvectors.* For $\lambda = 3$: (A − 3I)v = 0 gives $- x + y = 0$, so $v_{1} = (1 ,\  1)$. For $\lambda = 1$: $x + y = 0$, so $v_{2} = (1 ,\  - 1)$.

*Diagonalisation.* $P = \begin{bmatrix} 1 & 1 \\ 1 & - 1 \end{bmatrix}$ and $D = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}$, with A = PDP⁻¹.

*Power.* $A^{5} = P D^{5} P^{-1}$ with $D^{5} = \begin{bmatrix} 243 & 0 \\ 0 & 1 \end{bmatrix}$. Multiplying gives $A^{5} = \begin{bmatrix} 122 & 121 \\ 121 & 122 \end{bmatrix}$. *Conclusion.* Eigenvalues 3 and 1; diagonalisation turns a matrix power into the power of two numbers.

**Q2 (10 marks). Explain eigenvalues, eigenvectors and diagonalisation, state the conditions and properties, and show how a Markov chain uses them.**

*Introduction.* Eigenvalues and eigenvectors expose the directions in which a matrix acts as a simple stretch. They turn hard problems (powers of a matrix, long-run behaviour) into easy ones.

*Definitions and method.*

1. **Eigen-equation.** Av = $\lambda v$ with $v \neq 0$.
2. **Characteristic equation.** $\det (A - \lambda I) = 0$ is a polynomial of degree *n* in *λ*; its roots are the eigenvalues.
3. **Eigenvectors.** For each *λ*, solve $(A - \lambda I) v = 0$; the solutions form the eigenspace.
4. **Properties.** The sum of eigenvalues equals the trace and the product equals the determinant; for $B = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ these are $5 + 2 = 7$ and $5 \times 2 = 10$. A matrix is invertible exactly when 0 is not an eigenvalue.

*Diagonalisation.*

5. **Condition.** An $n \times n$ matrix is diagonalisable if it has *n* independent eigenvectors (distinct eigenvalues are enough; symmetric matrices always qualify).
6. **Result.** A = PDP⁻¹ with eigenvectors as columns of P and eigenvalues on the diagonal of D. For B: eigenvectors (1, 1) for 5 and (1, −2) for 2, so $B^{n} = P \mathrm{diag} (5^{n} ,\  2^{n}) P^{-1}$.

*Markov chain.* Let sunny days follow sunny days with probability 0.9 and rainy days follow sunny days with probability 0.5 (the other columns 0.1 and 0.5), so the transition matrix is $M = \begin{bmatrix} 0.9 & 0.5 \\ 0.1 & 0.5 \end{bmatrix}$.

7. **Eigenvalues.** One is 1 (the chain conserves probability) and the other is 0.4.
8. **Steady state.** The eigenvector for $\lambda = 1$ solves 0.9x + 0.5y = *x*, giving $y = x \div 5$, normalised to $\left( \frac{5}{6} ,\  \frac{1}{6} \right)$. In the long run about 83 percent of days are sunny, whatever today's weather is, because the $0.4^{n}$ part dies out.

| Idea | Rule |
|---|---|
| Eigenvalues | roots of $\det (A - \lambda I) = 0$ |
| Trace and determinant | sum and product of eigenvalues |
| Diagonalisation | A = PDP⁻¹, powers: $A^{n} = P D^{n} P^{-1}$ |
| Steady state | eigenvector for $\lambda = 1$ of a stochastic matrix |

*Conclusion.* Eigenvalues give the stretching factors, eigenvectors the directions, and together they make powers, long-run forecasts and principal axes easy to compute.

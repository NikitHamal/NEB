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

A non-zero vector v is an **eigenvector** of a square matrix A with **eigenvalue** λ if **Av = λv**. Rewrite as (A − λI)v = 0; a non-zero solution exists iff det(A − λI) = 0, the **characteristic equation**. For an n × n matrix it is a polynomial of degree n, so there are n eigenvalues counting multiplicity (possibly complex).

**Procedure:** (1) solve det(A − λI) = 0 for λ; (2) for each λ solve (A − λI)v = 0; the non-zero solutions are the eigenvectors (the **eigenspace**).

::: example Worked example
A = [[4, 1], [2, 3]]. det(A − λI) = (4 − λ)(3 − λ) − 2 = λ² − 7λ + 10 = (λ − 5)(λ − 2), so **λ = 5, 2**.
λ = 5: A − 5I = [[−1, 1], [2, −2]] ⇒ −x + y = 0 ⇒ v = **(1, 1)**. Check: A(1, 1) = (5, 5) = 5(1, 1) ✓.
λ = 2: A − 2I = [[2, 1], [2, 1]] ⇒ 2x + y = 0 ⇒ v = **(1, −2)**. Check: A(1, −2) = (2, −4) = 2(1, −2) ✓.
:::

::: example Worked example: a 3 × 3 with repeated eigenvalue
A = [[2, 0, 0], [0, 3, 4], [0, 4, 9]] has det(A − λI) = (2 − λ)((3 − λ)(9 − λ) − 16) = (2 − λ)(λ² − 12λ + 11) = (2 − λ)(λ − 1)(λ − 11); eigenvalues **2, 1, 11**.
:::

**Properties.** Sum of eigenvalues = **trace** (sum of the diagonal): 5 + 2 = 7 = 4 + 3 ✓. Product of eigenvalues = **determinant**: 5 · 2 = 10 = 12 − 2 ✓. A is invertible iff 0 is not an eigenvalue. Eigenvalues of Aᵏ are λᵏ; of A⁻¹ are 1/λ; of Aᵀ the same as A; of a triangular matrix the diagonal entries. Eigenvectors for *distinct* eigenvalues are linearly independent. **Cayley–Hamilton:** a matrix satisfies its own characteristic equation: for the example, A² − 7A + 10I = 0 (check: A² = [[18, 7], [14, 11]]; 7A = [[28, 7], [14, 21]]; A² − 7A + 10I = [[18 − 28 + 10, 0], [0, 11 − 21 + 10]] = 0 ✓). It gives A⁻¹ = (7I − A)/10 quickly.

## 4.2 Diagonalisation

A is **diagonalisable** if there is an invertible P and a diagonal D with **A = PDP⁻¹**: the columns of P are n independent eigenvectors and D has the eigenvalues. It happens iff A has n independent eigenvectors (guaranteed when the n eigenvalues are distinct).

::: example Worked example: powers
For A above: P = [[1, 1], [1, −2]], D = diag(5, 2), P⁻¹ = (1/(−3)) [[−2, −1], [−1, 1]] = [[2/3, 1/3], [1/3, −1/3]].
**A⁵ = P D⁵ P⁻¹** with D⁵ = diag(3125, 32): P D⁵ = [[3125, 32], [3125, −64]], and multiplying by P⁻¹ gives **A⁵ = [[2094, 1031], [2062, 1063]]**. Check: the trace is 3157 = 3125 + 32 ✓. Raising A to the power 5 directly needs four matrix products; diagonalisation makes **Aⁿ = PDⁿP⁻¹** a one-line computation for any n.
:::

**Not every matrix is diagonalisable**: [[1, 1], [0, 1]] has the single eigenvalue 1 (repeated) and only one independent eigenvector (1, 0); it is a *defective* matrix (a shear). The general fix is the **Jordan form**, outside this course.

**Symmetric matrices** (A = Aᵀ) are special: all eigenvalues are real, eigenvectors of different eigenvalues are **orthogonal**, and they are always diagonalisable by an **orthogonal** P (**spectral theorem**): A = QDQᵀ. Example: [[2, 1], [1, 2]] has λ = 3 (eigenvector (1, 1)/√2) and λ = 1 (eigenvector (1, −1)/√2). A symmetric matrix is **positive definite** if all eigenvalues are > 0 (energy and covariance matrices).

## 4.3 Applications

**Fibonacci in matrix form.** [[1, 1], [1, 0]]ⁿ = [[Fₙ₊₁, Fₙ], [Fₙ, Fₙ₋₁]]. Its eigenvalues solve λ² = λ + 1, i.e. λ = (1 ± √5)/2, so diagonalisation gives Binet's formula (Discrete Structure, Unit 4), and F₁₀ = 55 follows from the 10th power.

**Markov chains.** A **stochastic matrix** P (rows sum to 1) gives the probabilities of moving between states. If the weather is "dry" or "wet" with P = [[0.9, 0.1], [0.5, 0.5]], the long-run proportions π satisfy πP = π, i.e. π is a left eigenvector for λ = 1: 0.1π₁ = 0.5π₂ ⇒ π₁ = 5π₂, so with π₁ + π₂ = 1, **π = (5/6, 1/6)**: in the long run, 83 % of days are dry. The other eigenvalue is 0.4, so the chain converges geometrically at rate 0.4ⁿ.

**PageRank.** The rank of web pages is the principal eigenvector of the (damped) link matrix: a page is important if important pages link to it. It is found by **power iteration**: multiply a vector by the matrix repeatedly, and it converges to the dominant eigenvector. Example: starting from (1, 0) and applying A = [[4, 1], [2, 3]]: (4, 2), (18, 14), (86, 70), … the ratio tends to (1, 1)-direction: 86/70 = 1.23, then slowly towards 1 (5ⁿ dominates 2ⁿ).

**Principal component analysis (PCA).** For data, form the covariance matrix (symmetric); its eigenvectors with the largest eigenvalues are the directions of greatest variance. Keeping the top k reduces dimensions with minimal information loss (image compression, face recognition, visualising data).

**Systems of differential equations and stability.** x′ = Ax has solutions made of e^{λt}v; the system is stable (solutions decay) if all eigenvalues have negative real parts. **Vibrations** of a structure are governed by eigenvalues (natural frequencies). **Graph theory:** the eigenvalues of a graph's adjacency matrix describe its connectivity.

## 4.4 What an eigenvector looks like

Most vectors are turned and stretched when a matrix acts on them. An **eigenvector** is special: the matrix only stretches it along its own line, by the factor λ. Figure 4.1 shows A = [[2, 1], [1, 2]] acting on the unit circle. Every point of the circle goes to an ellipse; the ellipse's long axis lies along the eigenvector (1, 1), stretched by λ = 3, and its short axis along (1, −1), stretched by λ = 1. A symmetric matrix always has such perpendicular axes, which is why principal-component analysis of data works.

```svgfig label="4.1" caption="The matrix [[2,1],[1,2]] maps the unit circle (dashed) to an ellipse. The eigenvector (1,1) is stretched by 3 and the perpendicular eigenvector (1,-1) by 1; these are the principal axes of the ellipse."
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
2. **Markov chains and long-run forecasts.** If tomorrow's weather depends only on today's, the chain has a steady state that is the eigenvector for λ = 1 (Section 4.3 and the answers below). It predicts the long-run share of sunny days, customers or users.
3. **Principal component analysis (PCA).** The eigenvectors of a data covariance matrix point along the directions of greatest spread. Keeping the top few reduces hundreds of columns to two or three. Face recognition and survey analysis use it.
4. **Vibrations and earthquakes.** The natural frequencies of a building or bridge are the square roots of eigenvalues of its stiffness matrix. If shaking from an earthquake matches one, resonance can be destructive. Engineers in Nepal check this for tall buildings.
5. **Population growth.** In a Leslie matrix, the dominant eigenvalue is the long-run growth factor per period, and its eigenvector is the stable age distribution. Planners use this to project school and health needs.
6. **Stability of systems.** For x′ = Ax, all eigenvalues with negative real part mean the system settles. Control engineers choose a controller by moving eigenvalues. Cruise control and drone stabilisation rely on this.
7. **Image and data compression.** The singular-value decomposition, built from eigenvalues of AᵀA, stores a picture with a few large values and drops the rest. Recommenders and photo apps compress this way.
8. **Quantum and physical systems.** Energy levels of atoms are eigenvalues of an operator; the allowed states are eigenvectors. The idea that measurement gives eigenvalues is the heart of quantum mechanics.

## Formula and fact sheet

- Av = λv; det(A − λI) = 0; eigenspace = null space of A − λI.
- Σλ = trace; ∏λ = det. Eigenvalues of Aᵏ: λᵏ; of A⁻¹: 1/λ.
- Cayley–Hamilton: p(A) = 0. A = PDP⁻¹ ⇒ Aⁿ = PDⁿP⁻¹.
- Symmetric: real eigenvalues, orthogonal eigenvectors, A = QDQᵀ.
- Markov steady state: πP = π (eigenvalue 1). PageRank: power iteration.

## Chapter summary

- Eigenvectors are the directions a matrix only stretches; eigenvalues are the stretch factors.
- The characteristic polynomial finds them; trace and determinant give quick checks.
- Diagonalisation turns matrix powers into powers of numbers; symmetric matrices diagonalise orthogonally.
- Markov chains, PageRank, PCA, stability and vibration analysis are all eigenvalue problems.

## Practice

1. Find the eigenvalues and eigenvectors of [[3, 1], [0, 2]] and of [[2, 1], [1, 2]].
2. Find the eigenvalues of [[1, 2, 3], [0, 4, 5], [0, 0, 6]] and the determinant.
3. If the eigenvalues of A are 2, 3 and 5, find det A, tr A, eigenvalues of A² and of A⁻¹.
4. Verify the Cayley–Hamilton theorem for [[1, 2], [3, 4]] and use it to find A⁻¹.
5. Diagonalise [[4, 1], [2, 3]] and find A³.
6. Is [[2, 1], [0, 2]] diagonalisable? Explain.
7. A 2-state Markov chain has P = [[0.7, 0.3], [0.4, 0.6]]. Find the steady state.
8. Show that the eigenvalues of a symmetric 2 × 2 matrix [[a, b], [b, c]] are always real.
9. Find the eigenvalues of the rotation matrix [[0, −1], [1, 0]]. Interpret.
10. A population model: young Y and adults A, with Yₙ₊₁ = 2Aₙ, Aₙ₊₁ = 0.5Yₙ + 0.6Aₙ. Find the long-term growth rate.

::: note Answers and worked solutions
**1.** [[3, 1], [0, 2]]: triangular, λ = 3 (v = (1, 0)) and λ = 2 (A − 2I = [[1, 1], [0, 0]] ⇒ v = (1, −1)). [[2, 1], [1, 2]]: λ = 3 (v = (1, 1)), λ = 1 (v = (1, −1)).
**2.** Triangular: **1, 4, 6**; det = 1 · 4 · 6 = **24**.
**3.** det = 2·3·5 = **30**; trace = **10**; A² has 4, 9, 25; A⁻¹ has 1/2, 1/3, 1/5.
**4.** tr = 5, det = −2: λ² − 5λ − 2 = 0. A² = [[7, 10], [15, 22]]; A² − 5A − 2I = [[7 − 5 − 2, 10 − 10], [15 − 15, 22 − 20 − 2]] = 0 ✓. Then A² − 5A = 2I ⇒ A(A − 5I) = 2I ⇒ **A⁻¹ = (A − 5I)/2 = [[−2, 1], [1.5, −0.5]]**.
**5.** P D P⁻¹ as in §4.2. A³ = P diag(125, 8) P⁻¹ = [[125, 8], [125, −16]] · [[2/3, 1/3], [1/3, −1/3]] = [[(250 + 8)/3, (125 − 8)/3], [(250 − 16)/3, (125 + 16)/3]] = **[[86, 39], [78, 47]]**. (Trace 133 = 125 + 8 ✓.)
**6.** **No**: λ = 2 is repeated but A − 2I = [[0, 1], [0, 0]] has a one-dimensional null space, so there is only one independent eigenvector.
**7.** πP = π: 0.3π₁ = 0.4π₂ ⇒ π₁ = (4/3)π₂; π₁ + π₂ = 1 ⇒ π₂ = 3/7. **π = (4/7, 3/7) ≈ (0.571, 0.429)**.
**8.** λ² − (a + c)λ + (ac − b²) = 0 has discriminant (a + c)² − 4(ac − b²) = (a − c)² + 4b² ≥ 0, so the roots are real.
**9.** λ² + 1 = 0 ⇒ λ = ±i (complex): a rotation has no real direction that stays fixed (it turns every vector by 90°).
**10.** Matrix [[0, 2], [0.5, 0.6]] acting on (Y, A): λ² − 0.6λ − 1 = 0 ⇒ λ = (0.6 + √(0.36 + 4))/2 = (0.6 + 2.088)/2 = **1.344**, so the population grows about 34 % per period (the other eigenvalue −0.744 dies out).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Find the eigenvalues and eigenvectors of A = [[2, 1], [1, 2]], diagonalise it and find A⁵.**

*Introduction.* λ is an eigenvalue of A if det(A − λI) = 0, and a non-zero vector v with Av = λv is the eigenvector.

*Characteristic equation.* det [[2 − λ, 1], [1, 2 − λ]] = (2 − λ)² − 1 = λ² − 4λ + 3 = (λ − 1)(λ − 3) = 0, so **λ = 3 and λ = 1**. Check: trace 4 = 3 + 1 and det 3 = 3 × 1.

*Eigenvectors.* For λ = 3: (A − 3I)v = 0 gives −x + y = 0, so v₁ = (1, 1). For λ = 1: x + y = 0, so v₂ = (1, −1).

*Diagonalisation.* P = [[1, 1], [1, −1]] and D = [[3, 0], [0, 1]], with A = PDP⁻¹.

*Power.* A⁵ = PD⁵P⁻¹ with D⁵ = [[243, 0], [0, 1]]. Multiplying gives A⁵ = [[122, 121], [121, 122]]. *Conclusion.* Eigenvalues 3 and 1; diagonalisation turns a matrix power into the power of two numbers.

**Q2 (10 marks). Explain eigenvalues, eigenvectors and diagonalisation, state the conditions and properties, and show how a Markov chain uses them.**

*Introduction.* Eigenvalues and eigenvectors expose the directions in which a matrix acts as a simple stretch. They turn hard problems (powers of a matrix, long-run behaviour) into easy ones.

*Definitions and method.*

1. **Eigen-equation.** Av = λv with v ≠ 0.
2. **Characteristic equation.** det(A − λI) = 0 is a polynomial of degree n in λ; its roots are the eigenvalues.
3. **Eigenvectors.** For each λ, solve (A − λI)v = 0; the solutions form the eigenspace.
4. **Properties.** The sum of eigenvalues equals the trace and the product equals the determinant; for B = [[4, 1], [2, 3]] these are 5 + 2 = 7 and 5 × 2 = 10. A matrix is invertible exactly when 0 is not an eigenvalue.

*Diagonalisation.*

5. **Condition.** An n × n matrix is diagonalisable if it has n independent eigenvectors (distinct eigenvalues are enough; symmetric matrices always qualify).
6. **Result.** A = PDP⁻¹ with eigenvectors as columns of P and eigenvalues on the diagonal of D. For B: eigenvectors (1, 1) for 5 and (1, −2) for 2, so Bⁿ = P diag(5ⁿ, 2ⁿ) P⁻¹.

*Markov chain.* Let sunny days follow sunny days with probability 0.9 and rainy days follow sunny days with probability 0.5 (the other columns 0.1 and 0.5), so the transition matrix is M = [[0.9, 0.5], [0.1, 0.5]].

7. **Eigenvalues.** One is 1 (the chain conserves probability) and the other is 0.4.
8. **Steady state.** The eigenvector for λ = 1 solves 0.9x + 0.5y = x, giving y = x ÷ 5, normalised to (5/6, 1/6). In the long run about 83 percent of days are sunny, whatever today's weather is, because the 0.4ⁿ part dies out.

| Idea | Rule |
|---|---|
| Eigenvalues | roots of det(A − λI) = 0 |
| Trace and determinant | sum and product of eigenvalues |
| Diagonalisation | A = PDP⁻¹, powers: Aⁿ = PDⁿP⁻¹ |
| Steady state | eigenvector for λ = 1 of a stochastic matrix |

*Conclusion.* Eigenvalues give the stretching factors, eigenvectors the directions, and together they make powers, long-run forecasts and principal axes easy to compute.

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

---
subject: Mathematics
grade: BCA
unit: 6
title: Matrices and Determinants
hours: 2
area: Algebra
---

Matrices carry about two questions: the order of a matrix or a product, a 2 × 2 determinant or inverse, and one property question (singular, symmetric, effect of scalar multiplication). The Dean's Office model asks "how many elements in a single column of a 5 × 3 matrix". Matrices are written here in rows as `[[a, b], [c, d]]`.

::: key What the paper asks from this chapter
- **Order and operations**: $m\times n$, when $AB$ exists and its order, transpose rule.
- **Determinants**: $ad-bc$, 3 × 3 expansion, row properties, $|kA|=k^n|A|$.
- **Inverse**: exists iff $|A|\ne0$; 2 × 2 formula; $|A^{-1}|=\frac{1}{|A|}$, $|\text{adj}A|=|A|^{n-1}$.
- **Linear systems**: Cramer's rule and the matrix method.
:::

## 6.1 Types, order and operations on matrices

- A matrix with $m$ rows and $n$ columns has order $m\times n$ and $mn$ elements; each column has $m$ elements.
- Types: row, column, square, diagonal, scalar, identity $I$, zero (null), symmetric ($A=A^T$), skew-symmetric ($A=-A^T$, diagonal zero).
- $A+B$ needs equal order. $AB$ exists only if columns of $A$ = rows of $B$; order of $AB$ is (rows of $A$)×(columns of $B$). In general $AB\ne BA$; $AI=IA=A$.
- $(A+B)^T=A^T+B^T$ and $(AB)^T=B^TA^T$.

## 6.2 Determinants, minors and cofactors

- For `[[a, b], [c, d]]`, $|A|=ad-bc$. For a 3 × 3, expand along any row: $a_{11}C_{11}+a_{12}C_{12}+a_{13}C_{13}$ with cofactor $C_{ij}=(-1)^{i+j}M_{ij}$.
- A determinant is $0$ if two rows (or columns) are equal or proportional or a row is all zero. Swapping two rows changes the sign. A triangular matrix has $|A|=$ product of the diagonal.
- $|AB|=|A||B|$, $|A^T|=|A|$, and $|kA|=k^n|A|$ for order $n$.

## 6.3 Adjoint, inverse and linear systems

- $A^{-1}=\frac{\text{adj}A}{|A|}$ exists iff $|A|\ne0$ (non-singular). For 2 × 2 `[[a, b], [c, d]]`: $\text{adj}A=$ `[[d, -b], [-c, a]]`.
- $AA^{-1}=I$, $(AB)^{-1}=B^{-1}A^{-1}$, $|A^{-1}|=\frac{1}{|A|}$, $|\text{adj}A|=|A|^{n-1}$.
- **Cramer's rule** for $a_1x+b_1y=c_1$, $a_2x+b_2y=c_2$: $x=\frac{D_x}{D}$, $y=\frac{D_y}{D}$, $D=a_1b_2-a_2b_1$, with $D\ne0$.

## Formula and fact sheet

| Item | Result |
|---|---|
| $2\times2$ determinant | $ad-bc$ |
| Product order | $(m\times n)(n\times p)=m\times p$ |
| $(AB)^T$, $(AB)^{-1}$ | $B^TA^T$, $B^{-1}A^{-1}$ |
| $\lvert kA\rvert$ | $k^n\lvert A\rvert$ |
| $\lvert \text{adj}A\rvert$ | $\lvert A\rvert^{n-1}$ |

## Chapter summary

- Order $m\times n$: $m$ rows, $n$ columns; a column holds $m$ elements.
- $AB$ exists only if inner orders match, and $AB\ne BA$ in general.
- A zero determinant means singular: no inverse, and a row dependency.
- $|kA|=k^n|A|$: the factor is raised to the order.
- Reverse the order for $(AB)^T$ and $(AB)^{-1}$.
- Use Cramer's rule when $D\ne0$.

## Practice questions

**Set A — Recall (20 questions)**

1. A matrix of order 5 × 3 has how many elements in a single column?
   (a) 5 (b) 3 (c) 4 (d) 15
2. The determinant of `[[2, 3], [1, 4]]` is
   (a) 11 (b) 7 (c) 5 (d) 1
3. The product of a 2 × 3 matrix and a 3 × 4 matrix has order
   (a) 3 × 3 (b) 2 × 4 (c) 4 × 2 (d) not defined
4. A square matrix whose determinant is zero is called
   (a) identity (b) symmetric (c) orthogonal (d) singular
5. For a square matrix $A$ of order $n$, $AI$ equals
   (a) $A$ (b) 0 (c) $I$ (d) $A^2$
6. The transpose of a 2 × 3 matrix has order
   (a) 2 × 3 (b) 3 × 2 (c) 2 × 2 (d) 3 × 3
7. $(AB)^T$ equals
   (a) $A^TB^T$ (b) $AB$ (c) $B^TA^T$ (d) $BA$
8. The inverse of a square matrix $A$ exists if and only if
   (a) $A$ is symmetric (b) $|A|=0$ (c) $A$ is null (d) $|A|\ne0$
9. If $A=$ `[[1, 2], [3, 4]]` and $B=$ `[[0, 1], [1, 0]]`, the element in row 2, column 1 of $A+B$ is
   (a) 3 (b) 4 (c) 5 (d) 1
10. The determinant of the 3 × 3 identity matrix is
    (a) 1 (b) 0 (c) 3 (d) 9
11. A square matrix is symmetric if
    (a) $A=-A^T$ (b) $A=A^{-1}$ (c) $|A|=1$ (d) $A=A^T$
12. If $A$ is 3 × 3 and $|A|=2$, then $|2A|$ is
    (a) 4 (b) 8 (c) 16 (d) 6
13. The determinant of a matrix with two identical rows is
    (a) 0 (b) 1 (c) $-1$ (d) 2
14. The inverse of the 2 × 2 matrix $2I$ is
    (a) $2I$ (b) $\frac{1}{2}I$ (c) $I$ (d) $-2I$
15. A matrix all of whose elements are zero is called a
    (a) identity matrix (b) scalar matrix (c) diagonal matrix (d) null matrix
16. The number of elements in a 3 × 4 matrix is
    (a) 7 (b) 10 (c) 12 (d) 34
17. The determinant of `[[1, 2], [2, 4]]` is
    (a) 4 (b) 0 (c) 8 (d) $-4$
18. In the adjoint of `[[a, b], [c, d]]`, the element in row 1, column 2 is
    (a) $-b$ (b) $b$ (c) $-c$ (d) $c$
19. The diagonal elements of a skew-symmetric matrix are
    (a) 1 (b) $-1$ (c) all equal (d) zero
20. $|A^{-1}|$ equals
    (a) $|A|$ (b) $-|A|$ (c) $\frac{1}{|A|}$ (d) $|A|^2$

::: note Answers and explanations — Set A
**1.** (a) — a 5 × 3 matrix has 5 rows, so each column holds 5 entries.
**2.** (c) — 2·4 − 3·1 = 5.
**3.** (b) — (2×3)(3×4) gives 2 × 4.
**4.** (d) — zero determinant means singular.
**5.** (a) — I is the multiplicative identity.
**6.** (b) — rows and columns swap.
**7.** (c) — the order reverses.
**8.** (d) — |A| = 0 means no inverse.
**9.** (b) — row 2, column 1: 3 + 1 = 4.
**10.** (a) — diagonal product 1·1·1.
**11.** (d) — (a) defines skew-symmetric.
**12.** (c) — 2³ × 2 = 16, not 2 × 2 = 4.
**13.** (a) — equal rows make the determinant vanish.
**14.** (b) — (2I)(½I) = I.
**15.** (d) — null or zero matrix.
**16.** (c) — 3 × 4 = 12.
**17.** (b) — 1·4 − 2·2 = 0, rows proportional.
**18.** (a) — adj has −b in the top right.
**19.** (d) — aᵢᵢ = −aᵢᵢ forces 0.
**20.** (c) — |A||A⁻¹| = |I| = 1.
:::

**Set B — Understanding (12 questions)**

1. If the determinant of `[[x, 2], [3, 4]]` is $-2$, then $x$ is
   (a) 3 (b) 2 (c) $-1$ (d) 1
2. For $A=$ `[[1, 2], [3, 4]]`, the element in row 1, column 1 of $A^2$ is
   (a) 1 (b) 7 (c) 10 (d) 15
3. For $A=$ `[[1, 2], [0, 1]]` and $B=$ `[[1, 0], [3, 1]]`, the element in row 2, column 1 of $AB$ is
   (a) 3 (b) 7 (c) 1 (d) 0
4. In the inverse of `[[3, 1], [5, 2]]`, the element in row 1, column 2 is
   (a) 1 (b) 5 (c) $-1$ (d) 3
5. The matrix `[[k, 2], [3, 6]]` is singular when $k$ equals
   (a) 0 (b) 2 (c) 3 (d) 1
6. If $A$ is 3 × 3 and $|A|=5$, then $|\text{adj}A|$ is
   (a) 25 (b) 5 (c) 125 (d) 15
7. If $A$ is 3 × 2 and $B$ is 2 × 3, the order of $AB$ is
   (a) 2 × 2 (b) 3 × 2 (c) 3 × 3 (d) 2 × 3
8. For the system $x+y=5$, $x-y=1$, the value of $x$ is
   (a) 2 (b) 3 (c) 4 (d) 1
9. The determinant of `[[2, 5, 1], [0, 3, 7], [0, 0, 4]]` is
   (a) 24 (b) 14 (c) 9 (d) 0
10. If $A$ is 2 × 2 with $|A|=3$, then $|3A|$ is
    (a) 9 (b) 81 (c) 6 (d) 27
11. The cofactor of the element in row 1, column 2 of `[[1, 2], [3, 4]]` is
    (a) 3 (b) $-3$ (c) 4 (d) $-4$
12. If `[[a, 0], [0, a]]` squared equals $I$, a possible value of $a$ is
    (a) 0 (b) 2 (c) $-1$ (d) 3

::: note Answers and explanations — Set B
**1.** (d) — 4x − 6 = −2, x = 1.
**2.** (b) — 1·1 + 2·3 = 7.
**3.** (a) — row 2 of A is (0, 1); column 1 of B is (1, 3); 0 + 3 = 3.
**4.** (c) — |A| = 1; inverse is `[[2, -1], [-5, 3]]`.
**5.** (d) — 6k − 6 = 0, k = 1.
**6.** (a) — |A|^(3−1) = 25.
**7.** (c) — (3×2)(2×3) = 3 × 3, while BA would be 2 × 2.
**8.** (b) — adding the equations gives 2x = 6.
**9.** (a) — triangular: 2·3·4 = 24.
**10.** (d) — 3² × 3 = 27.
**11.** (b) — C₁₂ = −(minor 3) = −3.
**12.** (c) — a² = 1, so a = ±1; only −1 is listed.
:::

**Set C — Application (8 questions)**

1. Solving $2x+3y=8$ and $x+y=3$ by Cramer's rule gives $x+2y$ equal to
   (a) 4 (b) 5 (c) 6 (d) 3
2. If $A$ is a 3 × 3 matrix with $|A|=-2$, then $|A^{-1}|$ is
   (a) 2 (b) $-2$ (c) $\frac{1}{2}$ (d) $-\frac{1}{2}$
3. If $A=$ `[[1, 1], [0, 1]]`, the element in row 1, column 2 of $A^3$ is
   (a) 3 (b) 1 (c) 2 (d) 6
4. The determinant of `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]` is
   (a) 1 (b) 45 (c) 0 (d) $-6$
5. For $A=$ `[[2, 1], [1, 1]]`, the element in row 1, column 1 of $A^{-1}$ is
   (a) 2 (b) $-1$ (c) $\frac{1}{2}$ (d) 1
6. The product of `[[1, 2], [3, 4]]` and the column `[[1], [1]]` is a column whose entries add up to
   (a) 7 (b) 10 (c) 3 (d) 14
7. If the determinant of `[[x, 2], [3, x]]` is 3, a possible value of $x$ is
   (a) 9 (b) 6 (c) 3 (d) 0
8. If $A$ is the 2 × 2 matrix with $a_{ij}=i+j$, then $|A|$ is
   (a) $-1$ (b) 1 (c) 0 (d) 17

::: note Answers and explanations — Set C
**1.** (b) — D = −1, Dₓ = −1, so x = 1; y = 2 and x + 2y = 5.
**2.** (d) — 1/|A| = −1/2.
**3.** (a) — each multiplication adds 1 to the corner entry.
**4.** (c) — rows are in AP, so row 3 − row 2 = row 2 − row 1.
**5.** (d) — |A| = 1 and adj has d = 1 at the top left.
**6.** (b) — the column is (3, 7).
**7.** (c) — x² − 6 = 3 gives x = ±3.
**8.** (a) — `[[2, 3], [3, 4]]`: 8 − 9 = −1.
:::

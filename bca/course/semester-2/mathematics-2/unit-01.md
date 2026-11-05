---
subject: Mathematics II
grade: BCA Semester 2
unit: 1
title: Matrices and Determinants
area: BCA 154 · Mathematics II · Unit 1
---

Matrices store tables of numbers and describe linear change: a rotation of an image, a system of equations, a network's connections, a neural-network layer. This unit builds the algebra of matrices, determinants and inverses, the foundation of the whole subject.

::: key What this unit gives you
- Matrix types and operations (sum, product, transpose) with their laws.
- Determinants: expansion, properties, shortcuts.
- Inverse by adjoint and by row operations; properties of the inverse.
:::

## 1.1 Matrices and operations

An **m × n matrix** has m rows and n columns; aᵢⱼ is the entry in row i, column j.

| Type | Description |
|---|---|
| Square | m = n |
| Diagonal | non-zero entries only on the main diagonal |
| Identity Iₙ | diagonal of 1s; AI = IA = A |
| Zero | all entries 0 |
| Symmetric | Aᵀ = A; skew-symmetric: Aᵀ = −A |
| Upper/lower triangular | zeros below/above the diagonal |
| Orthogonal | AᵀA = I |

**Sum and scalar multiple** are entry by entry (same size). The **transpose** Aᵀ swaps rows and columns; (AB)ᵀ = BᵀAᵀ.

**Product.** If A is m × n and B is n × p, AB is m × p with (AB)ᵢⱼ = Σₖ aᵢₖ bₖⱼ (row of A times column of B). The inner sizes must agree.

::: example Worked example
A = [[2, 1], [4, 3]], B = [[1, 0], [2, 5]].
AB = [[2·1 + 1·2, 2·0 + 1·5], [4·1 + 3·2, 4·0 + 3·5]] = **[[4, 5], [10, 15]]**.
BA = [[1·2 + 0·4, 1·1 + 0·3], [2·2 + 5·4, 2·1 + 5·3]] = **[[2, 1], [24, 17]]**.
So **AB ≠ BA**: matrix multiplication is not commutative. It *is* associative, (AB)C = A(BC), and distributive, A(B + C) = AB + AC.
:::

Warning signs: AB = 0 does not imply A = 0 or B = 0; (A + B)² = A² + AB + BA + B² (not 2AB). **Powers:** Aⁿ for square A; for a diagonal matrix, raise each diagonal entry. Cost: the product of two n × n matrices takes about n³ multiplications, which is why algorithms (Strassen) and GPUs matter.

## 1.2 Determinants

The **determinant** det A (or |A|) is a number defined for square matrices.

- 2 × 2: det [[a, b], [c, d]] = **ad − bc**.
- 3 × 3: **cofactor expansion** along a row or column: det A = Σⱼ aᵢⱼ Cᵢⱼ, where Cᵢⱼ = (−1)ⁱ⁺ʲ Mᵢⱼ and the **minor** Mᵢⱼ is the determinant after deleting row i and column j. Sign pattern: [+ − +; − + −; + − +].

::: example Worked example
det [[2, 0, 1], [1, 3, 2], [1, 1, 1]] expanded along row 1 = 2·(3·1 − 2·1) − 0·(…) + 1·(1·1 − 3·1) = 2(1) + (−2) = **0**. A zero determinant means the matrix is **singular** (no inverse).
det [[1, 2, 3], [0, 1, 4], [5, 6, 0]] = 1(0 − 24) − 2(0 − 20) + 3(0 − 5) = −24 + 40 − 15 = **1**.
:::

**Properties** (the shortcuts that make hand computation practical):

1. det Aᵀ = det A; det(AB) = det A · det B; det(kA) = kⁿ det A for n × n.
2. Swapping two rows changes the sign. A row of zeros, or two equal (or proportional) rows, gives det = 0.
3. Multiplying one row by k multiplies the determinant by k.
4. Adding a multiple of one row to another changes nothing (use this to create zeros).
5. For triangular matrices, det = product of the diagonal.

::: example Worked example: row reduction for a determinant
det [[2, 4, 6], [1, 3, 5], [1, 1, 2]]: R₁ → R₁ − 2R₂ gives [0, −2, −4]; R₃ → R₃ − R₂ gives [0, −2, −3]. Now expand along column 1: its only non-zero entry is the 1 in position (2, 1), whose sign is −, so det = −1 · det [[−2, −4], [−2, −3]] = −1 · (6 − 8) = **2**. (Direct expansion gives the same: 2(1) − 4(−3) + 6(−2) = 2.)
:::

**Geometry:** |det A| is the factor by which the transformation x ↦ Ax scales areas (2 × 2) or volumes (3 × 3); a negative sign means orientation is flipped; det = 0 means the transformation collapses space to a lower dimension. The area of the triangle with vertices (x₁, y₁), (x₂, y₂), (x₃, y₃) is ½ |det [[x₁, y₁, 1], [x₂, y₂, 1], [x₃, y₃, 1]]|; three points are collinear iff that determinant is 0.

## 1.3 Inverse of a matrix

A square A is **invertible** if there is A⁻¹ with AA⁻¹ = A⁻¹A = I. This happens iff det A ≠ 0. Properties: (A⁻¹)⁻¹ = A; (AB)⁻¹ = B⁻¹A⁻¹; (Aᵀ)⁻¹ = (A⁻¹)ᵀ; det A⁻¹ = 1/det A.

**By the adjoint:** A⁻¹ = adj(A)/det A, where adj(A) is the transpose of the cofactor matrix. For 2 × 2: [[a, b], [c, d]]⁻¹ = (1/(ad − bc)) [[d, −b], [−c, a]].

**By row operations (Gauss–Jordan):** write [A | I] and row-reduce until the left side is I; the right side is then A⁻¹. This is how computers do it, in about n³ operations, and it also tells you if A is singular.

::: example Worked example
A = [[2, 1], [4, 3]]: det = 2, so A⁻¹ = ½ [[3, −1], [−4, 2]] = **[[1.5, −0.5], [−2, 1]]**. Check: row 1 of A times column 1 of A⁻¹: 2(1.5) + 1(−2) = 1 ✓.

N = [[1, 2, 3], [0, 1, 4], [5, 6, 0]], det N = 1. Cofactors give **N⁻¹ = [[−24, 18, 5], [20, −15, −4], [−5, 4, 1]]**; check the first entry of NN⁻¹: 1(−24) + 2(20) + 3(−5) = 1 ✓.
:::

**Solving AX = B** by X = A⁻¹B is elegant but in practice Gaussian elimination (Unit 2) is faster and more stable. **Elementary matrices** perform one row operation each; any invertible matrix is a product of them.

## 1.4 The determinant as an area

A 2 × 2 determinant has a picture. Take the matrix A with columns (3, 1) and (1, 2). It sends the unit square to a parallelogram whose sides are those two columns (Figure 1.1). The area of that parallelogram is |det A| = |3·2 − 1·1| = **5**, so A stretches every area by a factor of 5. The sign tells whether the picture is flipped. If the columns point along the same line, as in (2, 1) and (4, 2), the parallelogram collapses to a line segment, the area is 0, det = 0, and the matrix has **no inverse**: a squashed picture cannot be un-squashed.

```svgfig label="1.1" caption="Determinant as area. Left: the matrix with columns (3,1) and (1,2) turns the unit square (light) into a parallelogram of area det = 5. Right: columns (2,1) and (4,2) lie on one line, the parallelogram collapses, det = 0 and the matrix is singular."
f = Fig(580, 230)
ox, oy, u = 50, 200, 40
def P(x, y): return (ox + u * x, oy - u * y)
f.line(ox, oy, ox + 190, oy, color=SLATE); f.line(ox, oy, ox, oy - 170, color=SLATE)
f.poly([P(0, 0), P(1, 0), P(1, 1), P(0, 1)], fill="#e2e8f0", stroke=SLATE)
f.poly([P(0, 0), P(3, 1), P(4, 3), P(1, 2)], fill=BLUE, stroke=NAVY, label="area 5", lx=ox + 100, ly=oy - 80, color=NAVY)
f.arrow([P(0, 0), P(3, 1)], color=RED); f.arrow([P(0, 0), P(1, 2)], color=TEAL)
f.text(ox + 122, oy - 22, "(3,1)", size=10.5, color=RED, bold=True); f.text(ox + 14, oy - 92, "(1,2)", size=10.5, color=TEAL, bold=True)
f.text(ox + 95, oy + 18, "det = 3·2 − 1·1 = 5", size=11, color=NAVY, bold=True)
ox2 = 340
f.line(ox2, oy, ox2 + 220, oy, color=SLATE); f.line(ox2, oy, ox2, oy - 170, color=SLATE)
f.arrow([(ox2, oy), (ox2 + 80, oy - 40)], color=RED); f.arrow([(ox2, oy), (ox2 + 160, oy - 80)], color=TEAL)
f.text(ox2 + 60, oy - 60, "(2,1)", size=10.5, color=RED, bold=True); f.text(ox2 + 150, oy - 100, "(4,2)", size=10.5, color=TEAL, bold=True)
f.text(ox2 + 110, oy + 18, "det = 2·2 − 4·1 = 0: area 0", size=11, color=NAVY, bold=True)
f.text(ox2 + 110, 40, "both columns on one line: singular", size=10.5, color=SLATE, italic=True)
```

## 1.5 Eight uses of matrices in computing

1. **Computer graphics.** Every rotation, scaling and translation of an image or game object is a matrix multiplied by a coordinate vector. A phone screen applies thousands of such products every frame. Understanding 2 × 2 and 3 × 3 matrices is the first step to 3D graphics.
2. **Digital images.** A grey-scale photograph is a matrix of brightness numbers. Blurring, sharpening and edge detection are matrix operations on those numbers. Compression methods such as JPEG use matrix transforms to discard detail the eye cannot see.
3. **Search ranking.** Google's PageRank treats the web as a huge matrix of links and finds its dominant eigenvector (Unit 4). The same idea ranks pages, researchers and social-media accounts. It is a matrix problem with billions of rows.
4. **Machine learning.** Every layer of a neural network multiplies a weight matrix by an input vector. Training adjusts the matrix entries to reduce error. Fast matrix multiplication on graphics cards is why modern AI is possible.
5. **Networks and routing.** An adjacency matrix records which towns, routers or villages are connected. Powers of this matrix count the number of routes of a given length. Planners use it for road, fibre and power-grid design.
6. **Economics and planning.** Input-output tables show how the output of each industry feeds the others. Solving a linear system with the inverse matrix tells a planner how much each sector must produce to meet demand. The Nepal Rastra Bank and planning bodies use such tables.
7. **Cryptography.** The Hill cipher encrypts blocks of letters by multiplying with a key matrix; decryption needs the inverse matrix modulo 26. It teaches why a determinant of zero makes a key useless.
8. **Statistics and data tables.** A census table (districts by age group) is a matrix. Totals, averages and correlations come from matrix products. Spreadsheets and databases are everyday matrix tools.

## Formula and fact sheet

- (AB)ᵢⱼ = Σ aᵢₖ bₖⱼ; AB ≠ BA; (AB)ᵀ = BᵀAᵀ; (AB)⁻¹ = B⁻¹A⁻¹.
- det [[a, b], [c, d]] = ad − bc. det(AB) = det A det B; det Aᵀ = det A; det(kA) = kⁿ det A.
- Row swap flips the sign; adding a row multiple changes nothing; equal rows give 0.
- A⁻¹ = adj(A)/det A; exists iff det A ≠ 0. 2 × 2 inverse formula above.
- Triangle area = ½ |det [[x₁, y₁, 1], [x₂, y₂, 1], [x₃, y₃, 1]]|.

## Chapter summary

- Matrix multiplication combines rows with columns, is associative but not commutative.
- The determinant measures scaling and invertibility; row operations compute it efficiently.
- A matrix is invertible exactly when its determinant is non-zero; inverses come from the adjoint or Gauss–Jordan.

## Practice

1. For A = [[1, 2], [3, 4]] and B = [[0, 1], [1, 0]] find AB, BA, A² and Aᵀ.
2. Find det [[3, 1, 2], [0, 4, 1], [2, 0, 5]].
3. Use properties to show det [[1, a, b + c], [1, b, c + a], [1, c, a + b]] = 0.
4. Find the inverse of [[3, 5], [1, 2]] and verify.
5. Find the inverse of [[1, 2, 3], [0, 1, 4], [5, 6, 0]] by Gauss–Jordan (or check the given N⁻¹).
6. If A is 3 × 3 with det A = 4, find det(2A), det(A⁻¹), det(A²) and det(Aᵀ).
7. Are the points (1, 2), (3, 8), (5, 14) collinear? Use a determinant.
8. Find x for which [[x, 2], [3, x + 1]] is singular.
9. If A = [[1, 1], [0, 1]], find Aⁿ.
10. Show that the inverse of an orthogonal matrix is its transpose, and verify for the rotation by 90°, [[0, −1], [1, 0]].

::: note Answers and worked solutions
**1.** AB = [[2, 1], [4, 3]] (columns swapped); BA = [[3, 4], [1, 2]] (rows swapped); A² = [[7, 10], [15, 22]]; Aᵀ = [[1, 3], [2, 4]].
**2.** 3(4·5 − 1·0) − 1(0·5 − 1·2) + 2(0·0 − 4·2) = 60 + 2 − 16 = **46**.
**3.** Replace C₃ by C₃ + C₂ (the determinant does not change): every entry of the new third column is a + b + c, so it is (a + b + c) times the first column [1, 1, 1]ᵀ. Two proportional columns give det = **0**.
**4.** det = 6 − 5 = 1; inverse = [[2, −5], [−1, 3]]. Check: [[3, 5], [1, 2]]·[[2, −5], [−1, 3]] = [[1, 0], [0, 1]].
**5.** [[−24, 18, 5], [20, −15, −4], [−5, 4, 1]] (see §1.3; multiply to confirm it gives I).
**6.** det 2A = 2³ · 4 = **32**; det A⁻¹ = **1/4**; det A² = **16**; det Aᵀ = **4**.
**7.** det [[1, 2, 1], [3, 8, 1], [5, 14, 1]] = 1(8 − 14) − 2(3 − 5) + 1(42 − 40) = −6 + 4 + 2 = 0, so **collinear** (they lie on y = 3x − 1).
**8.** x(x + 1) − 6 = 0 ⇒ x² + x − 6 = 0 ⇒ (x + 3)(x − 2) = 0 ⇒ **x = −3 or x = 2**.
**9.** A² = [[1, 2], [0, 1]], A³ = [[1, 3], [0, 1]], so **Aⁿ = [[1, n], [0, 1]]** (induction: multiply by A).
**10.** AᵀA = I means Aᵀ is a left inverse of A, and for square matrices a left inverse is the inverse. For R = [[0, −1], [1, 0]], RᵀR = [[0, 1], [−1, 0]]·[[0, −1], [1, 0]] = [[1, 0], [0, 1]] ✓.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Find the inverse of N = [[1, 2, 3], [0, 1, 4], [5, 6, 0]] by the adjoint method.**

*Introduction.* For a square matrix, A⁻¹ = adj(A) ÷ det(A). The inverse exists only when det(A) ≠ 0.

*Step 1: determinant.* Expanding along the first row: det N = 1(1·0 − 4·6) − 2(0·0 − 4·5) + 3(0·6 − 1·5) = −24 + 40 − 15 = **1**. Since det N = 1 ≠ 0, N is invertible.

*Step 2: cofactors.* C11 = −24, C12 = 20, C13 = −5; C21 = 18, C22 = −15, C23 = 4; C31 = 5, C32 = −4, C33 = 1.

*Step 3: adjoint and inverse.* adj N is the transpose of the cofactor matrix, so N⁻¹ = [[−24, 18, 5], [20, −15, −4], [−5, 4, 1]] (the determinant is 1, so no division is needed).

*Check.* Row 1 of N times column 1 of N⁻¹ is 1(−24) + 2(20) + 3(−5) = 1, and row 1 times column 2 is 18 − 30 + 12 = 0, as required for the identity. *Conclusion.* N⁻¹ is the matrix above.

**Q2 (10 marks). Explain the operations on matrices and the properties of the determinant, with examples and the geometric meaning.**

*Introduction.* A matrix is a rectangular array of numbers; operations on matrices model transformations, systems of equations and data tables. The determinant is a single number that records whether a square matrix can be inverted.

*Operations.*

1. **Addition and scalar multiplication** work entry by entry and need equal sizes.
2. **Multiplication.** (AB)ᵢⱼ is row i of A times column j of B; the inner sizes must match.
3. **Non-commutative.** For A = [[2, 1], [4, 3]] and B = [[1, 0], [2, 5]], AB = [[4, 5], [10, 15]] but BA = [[2, 1], [24, 17]], so AB ≠ BA in general.
4. **Transpose.** Rows become columns, and (AB)ᵀ = BᵀAᵀ.
5. **Inverse.** A⁻¹ exists exactly when det A ≠ 0; for the 2 × 2 case [[a, b], [c, d]]⁻¹ = (1 ÷ (ad − bc)) [[d, −b], [−c, a]].

*Determinant properties.*

6. Swapping two rows changes the sign; a row of zeros or two equal rows gives 0.
7. Multiplying a row by k multiplies the determinant by k, and det(AB) = det A · det B.
8. Geometrically |det A| is the factor by which areas (2 × 2) or volumes (3 × 3) are multiplied (Figure 1.1); det = 0 means the transformation squashes space and cannot be undone.

| Property | Rule |
|---|---|
| AB versus BA | usually different |
| (AB)ᵀ | BᵀAᵀ |
| det(AB) | det A × det B |
| A invertible | det A ≠ 0 |
| 2 × 2 inverse | swap diagonal, negate off-diagonal, divide by det |

*Example.* For A = [[3, 1], [1, 2]], det = 5 and A⁻¹ = (1/5)[[2, −1], [−1, 3]]. *Conclusion.* Matrices combine data and transformations; the determinant tells at a glance whether a transformation is reversible.

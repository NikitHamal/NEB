---
subject: Mathematics II
grade: BCA Semester 2
unit: 3
title: Vector Spaces and Linear Transformations
area: BCA 154 · Mathematics II · Unit 3
---

Vectors are more than arrows: polynomials, images, signals and feature lists all behave as vectors. A **vector space** captures what they have in common, so that one theory (independence, basis, dimension, linear maps) serves graphics, data science and coding theory alike.

::: key What this unit gives you
- Vector space axioms and subspaces; span, linear independence, basis, dimension.
- Row space, column space, null space and the rank–nullity theorem.
- Linear transformations and their matrices; kernel and image.
- Inner products, orthogonality and the Gram–Schmidt process.
:::

## 3.1 Vector spaces and subspaces

A **vector space** over ℝ is a set V with addition and scalar multiplication satisfying: closure, commutativity and associativity of addition, a zero vector, additive inverses, and the distributive and identity rules for scalars (1·v = v, (ab)v = a(bv), a(u + v) = au + av, (a + b)v = av + bv).

Examples: ℝⁿ (n-tuples); the m × n matrices; the polynomials of degree ≤ n (Pₙ); the continuous functions on [0, 1]; the bit strings of length n over {0, 1} with XOR (a vector space over the field GF(2), used in error-correcting codes).

A **subspace** W ⊆ V is a vector space itself; test: W contains 0, and is closed under addition and scalar multiplication. In ℝ³ the subspaces are {0}, lines through the origin, planes through the origin, and ℝ³. **Not** subspaces: a line not through the origin; the set {(x, y) | x, y ≥ 0} (not closed under negative scalars); the set {(x, y) | xy = 0} (not closed under addition: (1, 0) + (0, 1) = (1, 1)).

## 3.2 Span, independence, basis and dimension

- **Linear combination**: c₁v₁ + … + cₖvₖ. The **span** is the set of all of them (a subspace).
- Vectors are **linearly independent** if c₁v₁ + … + cₖvₖ = 0 forces all cᵢ = 0; otherwise **dependent** (one is a combination of the others).
- A **basis** is a linearly independent spanning set. Every vector has a *unique* expression in a basis (its **coordinates**). All bases of a space have the same number of vectors, the **dimension**: dim ℝⁿ = n, dim Pₙ = n + 1, dim of m × n matrices = mn.

**Test for independence** (vectors in ℝⁿ): put them as columns of a matrix; they are independent iff rank = number of vectors (for n vectors in ℝⁿ iff det ≠ 0).

::: example Worked example
v₁ = (1, 2, 3), v₂ = (2, 4, 6), v₃ = (1, 0, 1). v₂ = 2v₁, so {v₁, v₂} is **dependent**. Matrix with columns v₁, v₃: rank 2, so {v₁, v₃} is independent, and span{v₁, v₂, v₃} has dimension 2 (a plane in ℝ³).
**Is {(1,0,0), (1,1,0), (1,1,1)} a basis of ℝ³?** The determinant of the matrix of these columns is 1 (triangular with 1s on the diagonal), so yes. Coordinates of (3, 2, 1): solve a(1,0,0) + b(1,1,0) + c(1,1,1) = (3, 2, 1): c = 1, b = 1, a = 1. So (3, 2, 1) has coordinates **(1, 1, 1)** in this basis.
**Polynomials:** {1, x, x²} is a basis of P₂, so dim P₂ = 3; {1, 1 + x, 1 + x + x²} is another.
:::

## 3.3 The four subspaces and rank–nullity

For an m × n matrix A:

| Subspace | Definition | Dimension |
|---|---|---|
| **Column space** C(A) | span of the columns (⊆ ℝᵐ) | rank r |
| **Row space** | span of the rows (⊆ ℝⁿ) | rank r |
| **Null space** N(A) | solutions of AX = 0 (⊆ ℝⁿ) | n − r (the **nullity**) |
| Left null space | solutions of AᵀY = 0 | m − r |

**Rank–nullity theorem: rank A + nullity A = n** (the number of columns). AX = B is solvable iff B lies in the column space; the full solution is one particular solution plus anything in the null space.

::: example Worked example
A = [[1, 2, 0, 1], [0, 1, 1, 0], [1, 3, 1, 1]]. Row 3 = row 1 + row 2, so rank 2. A has 4 columns, so nullity = 4 − 2 = **2**. Solve AX = 0: from R₂, y = −z; from R₁, x = −2y − w = 2z − w; free variables z = s, w = t: X = s(2, −1, 1, 0) + t(−1, 0, 0, 1). So {(2, −1, 1, 0), (−1, 0, 0, 1)} is a **basis of the null space** (dimension 2 ✓).
:::

## 3.4 Linear transformations

A map T: V → W is **linear** if T(u + v) = T(u) + T(v) and T(cv) = cT(v). Every linear map ℝⁿ → ℝᵐ is multiplication by an m × n matrix whose columns are T(e₁), …, T(eₙ), the images of the standard basis vectors.

::: example Worked example
T(x, y) = (x + y, x − y, 2x). T(1, 0) = (1, 1, 2) and T(0, 1) = (1, −1, 0), so the matrix is [[1, 1], [1, −1], [2, 0]].
**Rotation by θ** in the plane: [[cos θ, −sin θ], [sin θ, cos θ]]; for θ = 90°, (1, 0) ↦ (0, 1). **Scaling** by (sx, sy): diag(sx, sy). **Reflection** in the x-axis: diag(1, −1). **Shear**: [[1, k], [0, 1]]. **Projection** onto the x-axis: [[1, 0], [0, 0]] (singular: it loses information).
**Composition** is matrix multiplication; applying A then B is BA. In computer graphics, 2-D translations are not linear, so points are written as (x, y, 1) and a 3 × 3 matrix [[1, 0, tx], [0, 1, ty], [0, 0, 1]] translates; chains of rotations, scalings and translations multiply into a single matrix (**homogeneous coordinates**).
:::

**Kernel** ker T = {v | T(v) = 0} and **image** im T = {T(v)}. T is injective iff ker T = {0}; surjective iff im T = W; **rank–nullity**: dim ker T + dim im T = dim V. For the T above, ker = {0} (columns independent) and the image is a plane in ℝ³ (dimension 2). An **isomorphism** is a bijective linear map; every n-dimensional real space is isomorphic to ℝⁿ.

**Change of basis:** if P has the new basis vectors as columns, then coordinates convert by x = P x′, and a transformation matrix changes to P⁻¹AP (a **similar** matrix, with the same determinant, trace and eigenvalues, Unit 4).

## 3.5 Inner products and orthogonality

In ℝⁿ the **dot product** u · v = Σ uᵢvᵢ; **length** ‖v‖ = √(v · v); **angle** cos θ = u·v/(‖u‖‖v‖); **Cauchy–Schwarz** |u · v| ≤ ‖u‖‖v‖. Vectors are **orthogonal** if u · v = 0. **Projection** of v on u: proj_u v = ((v · u)/(u · u)) u.

An **orthonormal basis** (unit, mutually orthogonal vectors) makes coordinates easy: the coordinate of v along qᵢ is v · qᵢ. **Gram–Schmidt** builds one from any basis: q₁ = v₁/‖v₁‖; w₂ = v₂ − (v₂·q₁)q₁, q₂ = w₂/‖w₂‖; and so on.

::: example Worked example: Gram–Schmidt
v₁ = (1, 1, 0), v₂ = (1, 0, 1). ‖v₁‖ = √2, q₁ = (1, 1, 0)/√2. v₂ · q₁ = 1/√2, so w₂ = v₂ − (1/√2)(1, 1, 0)/√2 = (1, 0, 1) − (½, ½, 0) = (½, −½, 1). ‖w₂‖ = √(¼ + ¼ + 1) = √1.5, so q₂ = (½, −½, 1)/√1.5. Check q₁ · q₂ = (½ − ½)/… = 0 ✓.
:::

**Least squares** is a projection: the best approximate solution of an inconsistent AX = B is the X making AX the projection of B onto the column space, found from AᵀAX = AᵀB. Fitting y = a + bx to (1, 1), (2, 2), (3, 2): A = [[1, 1], [1, 2], [1, 3]], B = (1, 2, 2); AᵀA = [[3, 6], [6, 14]], AᵀB = (5, 11); solving gives b = 0.5, a = 2/3: **y = 0.667 + 0.5x**.

## Formula and fact sheet

- Subspace test: contains 0, closed under + and scalar multiplication.
- Independent ⇔ only the trivial combination gives 0; basis = independent + spanning; dimension = size of any basis.
- Rank–nullity: rank + nullity = number of columns (dim ker + dim im = dim V).
- Matrix of T has columns T(eᵢ). Composition = product. Similar matrices P⁻¹AP.
- u · v = ‖u‖‖v‖cos θ; proj_u v = (v·u/u·u)u; Gram–Schmidt; least squares AᵀAX = AᵀB.

## Chapter summary

- Vector spaces abstract the idea of vector; subspaces, span, independence, basis and dimension organise them.
- Rank–nullity ties the solutions of AX = 0 to the rank of A.
- Linear maps are matrices; their kernel and image measure what is lost and what is reached.
- Orthogonal bases and projections give coordinates, Gram–Schmidt and least squares.

## Practice

1. Is W = {(x, y, z) | x + y + z = 0} a subspace of ℝ³? Find a basis and the dimension.
2. Test the independence of (1, 2, 1), (2, 1, 0), (1, −1, −1).
3. Show {1, 1 + x, 1 + x + x²} is a basis of P₂ and find the coordinates of 3 + 2x + x².
4. A 4 × 6 matrix has rank 3. Find the dimensions of its four subspaces.
5. Find the matrix of T(x, y, z) = (x − y, y + 2z) and its kernel dimension.
6. Find the matrix of the rotation by 60° followed by a scaling by 2.
7. Find the angle between (1, 2, 2) and (2, −1, 2) and the projection of the first on the second.
8. Apply Gram–Schmidt to (1, 0, 0), (1, 1, 0), (1, 1, 1).
9. Is the set {(x, y) | y = 2x + 1} a subspace? Why or why not?
10. Fit a least-squares line through (0, 1), (1, 3), (2, 4).

::: note Answers and worked solutions
**1.** Contains 0; the sum of two vectors with coordinate-sum 0 also has sum 0; so a subspace (a plane through the origin). Basis {(1, −1, 0), (0, 1, −1)}, **dimension 2**.
**2.** det [[1, 2, 1], [2, 1, −1], [1, 0, −1]] = 1(−1 − 0) − 2(−2 + 1) + 1(0 − 1) = −1 + 2 − 1 = 0, so **dependent** ((1, 2, 1) − (2, 1, 0) = (−1, 1, 1) = −(1, −1, −1), i.e. v₁ − v₂ + v₃ = 0).
**3.** Three polynomials of degrees 0, 1, 2 are independent and dim P₂ = 3, so they form a basis. a + b(1 + x) + c(1 + x + x²) = 3 + 2x + x²: x²: c = 1; x: b + c = 2 ⇒ b = 1; constant: a + b + c = 3 ⇒ a = 1. Coordinates **(1, 1, 1)**.
**4.** Column space 3, row space 3, null space 6 − 3 = 3, left null space 4 − 3 = 1.
**5.** [[1, −1, 0], [0, 1, 2]]; rank 2, nullity 3 − 2 = **1** (kernel spanned by (2, 2, −1): 2 − 2 = 0 and 2 − 2 = 0 ✓).
**6.** Rotation R = [[½, −√3/2], [√3/2, ½]]; scale by 2 first applied after: 2R = [[1, −√3], [√3, 1]].
**7.** u · v = 2 − 2 + 4 = 4; ‖u‖ = 3, ‖v‖ = 3; cos θ = 4/9 ⇒ θ ≈ **63.6°**. Projection = (4/9)(2, −1, 2) = **(8/9, −4/9, 8/9)**.
**8.** q₁ = (1, 0, 0); w₂ = (1, 1, 0) − (1)(1, 0, 0) = (0, 1, 0) ⇒ q₂ = (0, 1, 0); w₃ = (1, 1, 1) − (1, 0, 0) − (0, 1, 0) = (0, 0, 1) ⇒ q₃ = (0, 0, 1): the standard basis.
**9.** **No**: (0, 0) does not satisfy y = 2x + 1, so the zero vector is missing (a line not through the origin).
**10.** A = [[1, 0], [1, 1], [1, 2]], B = (1, 3, 4): AᵀA = [[3, 3], [3, 5]], AᵀB = (8, 11). Solve 3a + 3b = 8, 3a + 5b = 11 ⇒ 2b = 3 ⇒ b = 1.5, a = 8/3 − 1.5 = 7/6: **y = 1.167 + 1.5x**.
:::

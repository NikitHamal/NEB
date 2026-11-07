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

A **vector space** over $\mathbb{R}$ is a set V with addition and scalar multiplication satisfying: closure, commutativity and associativity of addition, a zero vector, additive inverses, and the distributive and identity rules for scalars (1·v = *v*, (ab)v = $a (b v) ,\  a (u + v) = a u + a v ,\  ( a$ + b)v = $a v + b v$).

Examples: $\mathbb{R}^{n}$ (n-tuples); the $m \times n$ matrices; the polynomials of degree ≤ $n (P_{n})$; the continuous functions on [0, 1]; the bit strings of length *n* over {0, 1} with XOR (a vector space over the field GF(2), used in error-correcting codes).

A **subspace** $W \subseteq V$ is a vector space itself; test: W contains 0, and is closed under addition and scalar multiplication. In $\mathbb{R}^{3}$ the subspaces are {0}, lines through the origin, planes through the origin, and $\mathbb{R}^{3}$. **Not** subspaces: a line not through the origin; the set $\{(x ,\  y) \mid x ,\  y \geq 0\}$ (not closed under negative scalars); the set $\{(x ,\  y) \mid x y = 0\}$ (not closed under addition: $(1 ,\  0) + (0 ,\  1) = (1 ,\  1)$).

## 3.2 Span, independence, basis and dimension

- **Linear combination**: $c_{1} v_{1} + \ldots + c_{k} v_{k}$. The **span** is the set of all of them (a subspace).
- Vectors are **linearly independent** if $c_{1} v_{1} + \ldots + c_{k} v_{k} = 0$ forces all $c_{i} = 0$; otherwise **dependent** (one is a combination of the others).
- A **basis** is a linearly independent spanning set. Every vector has a *unique* expression in a basis (its **coordinates**). All bases of a space have the same number of vectors, the **dimension**: dim $\mathbb{R}^{n} = n$, dim $P_{n} = n + 1$, dim of $m \times n$ matrices = $m n$.

**Test for independence** (vectors in $\mathbb{R}^{n}$): put them as columns of a matrix; they are independent iff rank = number of vectors (for *n* vectors in $\mathbb{R}^{n}$ iff $\det \neq 0$).

::: example Worked example
$v_{1} = (1 ,\  2 ,\  3) ,\  v_{2} = (2 ,\  4 ,\  6) ,\  v_{3} = (1 ,\  0 ,\  1)$. $v_{2} = 2 v_{1}$, so $\{v_{1} ,\  v_{2}\}$ is **dependent**. Matrix with columns $v_{1} ,\  v_{3}$: rank 2, so $\{v_{1} ,\  v_{3}\}$ is independent, and $\mathrm{span} \{v_{1} ,\  v_{2} ,\  v_{3}\}$ has dimension 2 (a plane in $\mathbb{R}^{3}$).

**Is {(1,0,0), (1,1,0), (1,1,1)} a basis of $\mathbb{R}^{3}$?** The determinant of the matrix of these columns is 1 (triangular with 1s on the diagonal), so yes. Coordinates of (3, 2, 1): solve $a (1 ,\  0 ,\  0) + b (1 ,\  1 ,\  0) + c (1 ,\  1 ,\  1) = (3 ,\  2 ,\  1)$: $c = 1 ,\  b = 1 ,\  a = 1$. So (3, 2, 1) has coordinates **(1, 1, 1)** in this basis.

**Polynomials:** $\{1 ,\  x ,\  x^{2}\}$ is a basis of $P_{2}$, so dim $P_{2} = 3 ;\  \{1 ,\  1 + x ,\  1 + x + x^{2}\}$ is another.
:::

## 3.3 The four subspaces and rank–nullity

For an $m \times n$ matrix A:

| Subspace | Definition | Dimension |
|---|---|---|
| **Column space** $C (A)$ | span of the columns $(\subseteq \mathbb{R}^{m})$ | rank *r* |
| **Row space** | span of the rows $(\subseteq \mathbb{R}^{n})$ | rank *r* |
| **Null space** $N (A)$ | solutions of $A X = 0 (\subseteq \mathbb{R}^{n})$ | $n - r$ (the **nullity**) |
| Left null space | solutions of $A^{T} Y = 0$ | $m - r$ |

**Rank–nullity theorem: rank A + nullity $A = n$** (the number of columns). $A X = B$ is solvable iff B lies in the column space; the full solution is one particular solution plus anything in the null space.

::: example Worked example
$A = \begin{bmatrix} 1 & 2 & 0 & 1 \\ 0 & 1 & 1 & 0 \\ 1 & 3 & 1 & 1 \end{bmatrix}$. Row 3 = row 1 + row 2, so rank 2. A has 4 columns, so nullity = $4 - 2$ = **2**. Solve $A X = 0$: from $R_{2} ,\  y = - z$; from $R_{1} ,\  x = - 2 y - w = 2 z - w$; free variables $z = s ,\  w = t$: $X = s (2 ,\  - 1 ,\  1 ,\  0) + t (- 1 ,\  0 ,\  0 ,\  1)$. So {(2, −1, 1, 0), (−1, 0, 0, 1)} is a **basis of the null space** (dimension 2 ✓).
:::

## 3.4 Linear transformations

A map T: $V \to W$ is **linear** if $T (u + v) = T (u) + T (v)$ and $T (c v)$ = cT(v). Every linear map $\mathbb{R}^{n} \to \mathbb{R}^{m}$ is multiplication by an $m \times n$ matrix whose columns are $T (e_{1}) ,\  \ldots ,\  T (e_{n})$, the images of the standard basis vectors.

::: example Worked example
$T (x ,\  y) = (x + y ,\  x - y ,\  2 x)$. $T (1 ,\  0) = ( 1 ,\  1$, 2) and $T (0 ,\  1) = (1 ,\  - 1 ,\  0)$, so the matrix is $\begin{bmatrix} 1 & 1 \\ 1 & - 1 \\ 2 & 0 \end{bmatrix}$.

**Rotation by *θ*** in the plane: $\begin{bmatrix} \cos \theta & - \sin \theta \\ \sin \theta & \cos \theta \end{bmatrix}$; for $\theta = 90 ^{\circ} ,\  ( 1$, 0) ↦ (0, 1). **Scaling** by $(s x ,\  s y)$: diag(sx, $s y$). **Reflection** in the x-axis: diag(1, −1). **Shear**: $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$. **Projection** onto the x-axis: $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ (singular: it loses information).

**Composition** is matrix multiplication; applying A then B is BA. In computer graphics, $2 - D$ translations are not linear, so points are written as ($x ,\  y$, 1) and a $3 \times 3$ matrix $\begin{bmatrix} 1 & 0 & t x \\ 0 & 1 & t y \\ 0 & 0 & 1 \end{bmatrix}$ translates; chains of rotations, scalings and translations multiply into a single matrix (**homogeneous coordinates**).
:::

**Kernel** ker $T = \{v \mid T (v) = 0\}$ and **image** im $T = \{T (v)\}$. T is injective iff ker T = {0}; surjective iff im $T = W$; **rank–nullity**: dim ker T + dim im T = dim V. For the T above, ker = {0} (columns independent) and the image is a plane in $\mathbb{R}^{3}$ (dimension 2). An **isomorphism** is a bijective linear map; every n-dimensional real space is isomorphic to $\mathbb{R}^{n}$.

**Change of basis:** if P has the new basis vectors as columns, then coordinates convert by $x = P x'$, and a transformation matrix changes to $P^{-1} A P ( a$ **similar** matrix, with the same determinant, trace and eigenvalues, Unit 4).

## 3.5 Inner products and orthogonality

In $\mathbb{R}^{n}$ the **dot product** $u \cdot v = \sum u_{i} v_{i}$; **length** ‖v‖ = $\sqrt{v \cdot v}$; **angle** $\cos \theta$ = u·v/(‖u‖‖v‖); **Cauchy–Schwarz** |u · v| ≤ ‖u‖‖v‖. Vectors are **orthogonal** if $u \cdot v = 0$. **Projection** of *v* on *u*: proj_u v = ((v · u)/(u · u)) u.

An **orthonormal basis** (unit, mutually orthogonal vectors) makes coordinates easy: the coordinate of *v* along $q_{i}$ is $v \cdot q_{i}$. **Gram–Schmidt** builds one from any basis: q₁ = v₁/‖v₁‖; w₂ = v₂ − (v₂·q₁)q₁, q₂ = w₂/‖w₂‖; and so on.

::: example Worked example: Gram–Schmidt
$v_{1} = (1 ,\  1 ,\  0) ,\  v_{2} = (1 ,\  0 ,\  1)$. ‖v₁‖ = √2, q₁ = (1, 1, 0)/√2. $v_{2} \cdot q_{1} = \frac{1}{\sqrt{2}}$, so $w_{2} = v_{2} - \frac{\left( \frac{1}{\sqrt{2}} \right) (1 ,\  1 ,\  0)}{\sqrt{2}} = (1 ,\  0 ,\  1) - \left( \frac{1}{2} ,\  \frac{1}{2} ,\  0 \right) = \left( \frac{1}{2} ,\  - \frac{1}{2} ,\  1 \right)$. ‖w₂‖ = √(¼ + ¼ + 1) = √1.5, so $q_{2} = \frac{\frac{1}{2} ,\  - \frac{1}{2} ,\  1}{\sqrt{1.5}}$. Check $q_{1} \cdot q_{2} = \frac{\frac{1}{2} - \frac{1}{2}}{\ldots} = 0$ ✓.
:::

**Least squares** is a projection: the best approximate solution of an inconsistent $A X = B$ is the X making AX the projection of B onto the column space, found from $A^{T} A X = A^{T} B$. Fitting $y = a + b x$ to (1, 1), (2, 2), (3, 2): $A = \begin{bmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{bmatrix} ,\  B = (1 ,\  2 ,\  2) ;\  A^{T} A = \begin{bmatrix} 3 & 6 \\ 6 & 14 \end{bmatrix} ,\  A^{T} B = (5 ,\  11)$; solving gives $b = 0.5 ,\  a = \frac{2}{3}$: **$y = 0.667$ + 0.5x**.

## 3.6 The four subspaces in one picture

An $m \times n$ matrix A of rank *r* carries four subspaces, and rank–nullity says how they fit together (Figure 3.1). The **row space** (dimension *r*) and the **null space** (dimension $n - r$) split the input space $\mathbb{R}^{n}$, and they are perpendicular. The **column space** (dimension *r*) and the **left null space** (dimension $m - r$) split the output space $\mathbb{R}^{m}$, also perpendicular. A sends the row space one-to-one onto the column space and squashes the null space to zero. Everything an $m \times n$ matrix can do is visible in this picture.

```svgfig label="3.1" caption="The four fundamental subspaces of an *m* by *n* matrix of rank *r*. Input space (left): row space (dim *r*) and null space (dim *n* minus *r*), perpendicular. Output space (right): column space (dim *r*) and left null space (dim *m* minus *r*), perpendicular. A maps the row space onto the column space and the null space to zero."
f = Fig(580, 230)
f.box(20, 20, 200, 190, "", fill="#ffffff", stroke=NAVY)
f.box(20, 20, 200, 190, "", fill="#ffffff", stroke=NAVY)
f.text(120, 14, "input space R^n", size=11, color=NAVY, bold=True)
f.box(32, 36, 176, 82, "Row space\ndim r", fill=BLUE, stroke=NAVY, size=12, color=NAVY, bold=True)
f.box(32, 126, 176, 74, "Null space\ndim n - r\nA x = 0", fill="#fde68a", stroke=AMBER, size=12, color=NAVY, bold=True)
f.box(360, 20, 200, 190, "", fill="#ffffff", stroke=NAVY)
f.text(460, 14, "output space R^m", size=11, color=NAVY, bold=True)
f.box(372, 36, 176, 82, "Column space\ndim r", fill=SOFT, stroke=TEAL, size=12, color=NAVY, bold=True)
f.box(372, 126, 176, 74, "Left null space\ndim m - r\nA^T y = 0", fill="#fecaca", stroke=RED, size=12, color=NAVY, bold=True)
f.arrow([(208, 77), (372, 77)], color=NAVY, label="A: one-to-one", lpos=(290, 62))
f.arrow([(208, 163), (330, 163), (330, 150)], color=AMBER, label="A x = 0", lpos=(270, 182))
f.text(290, 130, "perpendicular pairs", size=10, color=SLATE, italic=True)
```

## 3.7 Eight uses of vector spaces and linear maps

1. **Data as vectors.** A student record with five marks is a vector in $\mathbb{R}^{5}$; a photo with a million pixels is a vector in $\mathbb{R}^{1000000}$. Distances and angles between vectors measure similarity. This is the starting point of every data-science method.
2. **Face unlock and recognition.** A phone reduces a face image to a short vector using a few basis directions (principal components). Two faces are compared by the distance between their vectors. Basis and dimension are the central ideas.
3. **Compression.** JPEG and MP3 change to a better basis in which most coordinates are nearly zero, then drop the small ones. The picture or song is the same vector written in a smarter basis. Files shrink by ten times with little visible loss.
4. **Recommender systems.** A table of users and films has low rank, because tastes follow a few patterns. Finding the column space of the table lets a service suggest what you may like. The rank is the number of independent tastes.
5. **Graphics and robotics.** Rotating, scaling and reflecting a shape are linear transformations. A robot $a r m$ composes several of them, one per joint, by multiplying their matrices. Kernel and image tell which movements are lost.
6. **Error-correcting codes.** Codes used in QR codes, SIM cards and storage are subspaces of vector spaces over the numbers 0 and 1. A received word is corrected by finding the nearest vector in the subspace. Dimension tells how much real data a code carries.
7. **Signals and communication.** A radio or mobile signal is a vector in a space of waveforms; the Fourier transform is a change of basis. Filters are linear transformations. FM stations in Nepal share the air because their signals sit in different directions of this space.
8. **Differential equations and systems.** The solutions of a linear homogeneous equation form a vector space whose dimension equals the order of the equation. Knowing a basis of solutions gives every solution as a combination. The same idea explains the null space of a matrix.

```photogrid label="3.1" cols="2" ratio="1.2" caption="Colour is a vector in $R^{3}$. (a) An LCD screen under a microscope: every pixel is three subpixels, red, green and blue, and each colour on screen is a combination *r* e1 + *g* e2 + *b* e3 of the three basis vectors with 0 <= $r ,\  g ,\  b$ <= 255. (b) Converting to grey is the linear map $Y = 0.299 r + 0.587 g + 0.114 b$. It is linear: for the colours c1 = (200, 50, 0) and c2 = (40, 100, 150) the grey of the sum, 176.9, equals the sum of the greys, $89.1 + 87.8$. Its matrix [0.299 0.587 0.114] has rank 1, so the nullity is $3 - 1 = 2$: a whole plane of different colours (all with $Y = 0$) is thrown onto black, which is why two very different colours can look identical in a grey print. Rank-nullity: $1 + 2 = 3$."
@ photo id="bcamath/lcdsub" cap="LCD subpixels: red, green, blue"
fit 1.2
focus 0.5 0.5
@ svg cap="Grey conversion is linear, rank 1, nullity 2"
import sympy
c1 = (200, 50, 0); c2 = (40, 100, 150); cs = tuple(a + b for a, b in zip(c1, c2))
w = (0.299, 0.587, 0.114)
Y = lambda c: sum(a * b for a, b in zip(w, c))
assert abs(Y(cs) - (Y(c1) + Y(c2))) < 1e-9 and round(Y(c1), 1) == 89.1 and round(Y(c2), 1) == 87.8 and round(Y(cs), 1) == 176.9
Mx = sympy.Matrix([[299, 587, 114]])
assert Mx.rank() == 1 and len(Mx.nullspace()) == 2 and Mx.rank() + len(Mx.nullspace()) == 3
hexc = lambda c: "#%02x%02x%02x" % tuple(int(round(v)) for v in c)
g = lambda c: (Y(c), Y(c), Y(c))
f = Fig(300, 240)
def sw(x, y, c, lab, s=52):
    f.box(x, y, s, s, "", fill=hexc(c), stroke=SLATE, r=4)
    f.text(x + s / 2, y + s + 14, lab, size=10.5, color=SLATE, bold=True)
sw(14, 20, c1, "c1 (200,50,0)"); f.text(84, 46, "+", size=18, color=SLATE, bold=True, vmid=True)
sw(98, 20, c2, "c2 (40,100,150)"); f.text(168, 46, "=", size=18, color=SLATE, bold=True, vmid=True)
sw(182, 20, cs, "c1 + c2")
sw(14, 110, g(c1), "Y = 89.1"); f.text(84, 136, "+", size=18, color=SLATE, bold=True, vmid=True)
sw(98, 110, g(c2), "Y = 87.8"); f.text(168, 136, "=", size=18, color=SLATE, bold=True, vmid=True)
sw(182, 110, g(cs), "Y = 176.9")
f.text(150, 208, "grey of the sum = sum of the greys: linear", size=10.5, color=TEAL, bold=True)
f.text(150, 228, "rank 1 + nullity 2 = 3 (RGB dimensions)", size=10.5, color=NAVY, bold=True)
```

```photogrid label="3.2" cols="2" ratio="1.2" caption="Right angles by calculation. (a) A set square: a carpenter or draughtsman checks that two lines are perpendicular; a vector space with an inner product does the same with the dot product. (b) The Gram-Schmidt step on $a = ( 3$, 1) and $b = (2 ,\  2)$. The projection of *b* on a is (a.b / a.a) $a = \left( \frac{8}{10} \right) a = (2.4 ,\  0.8)$, and what is left, *b* - proj = (-0.4, 1.2), is perpendicular to a because $a . (- 0.4 ,\  1.2) = - 1.2 + 1.2 = 0$. The angle between a and *b* is arccos(8 / (sqrt(10) *x* sqrt(8))) = 26.57 degrees. An orthogonal basis makes coordinates trivial to compute: each coordinate is a single dot product, which is why QR factorisation and least-squares fitting use it."
@ photo id="bcamath/setsquare" cap="A set square: a right angle to check against"
fit 1.2
focus 0.5 0.5
@ svg cap="Projection and the perpendicular part"
import numpy as np
a = np.array([3.0, 1.0]); b = np.array([2.0, 2.0])
p = (a @ b) / (a @ a) * a; r = b - p
assert np.allclose(p, [2.4, 0.8]) and np.allclose(r, [-0.4, 1.2]) and abs(a @ r) < 1e-12
ang = np.degrees(np.arccos(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))))
assert round(ang, 2) == 26.57 and a @ b == 8
f = Fig(300, 240)
O = (28, 200); S = 42
P = lambda v: (O[0] + v[0] * S, O[1] - v[1] * S)
f.line(O[0], O[1], 170, O[1], color="#94a3b8", sw=1); f.line(O[0], O[1], O[0], 70, color="#94a3b8", sw=1)
f.arrow([P((0, 0)), P(a)], color=NAVY, sw=2.4); f.arrow([P((0, 0)), P(b)], color=TEAL, sw=2.4)
f.line(*P(p), *P(b), color=RED, sw=2.2); f.line(*P((0, 0)), *P(p), color=AMBER, sw=3.2, dash=True)
q = P(p); f.line(q[0] - 7, q[1] - 2, q[0] - 7 + 0, q[1] - 2, color=RED, sw=1)
f.box(q[0] - 1, q[1] - 11, 10, 10, "", fill="none", stroke=RED, r=0, sw=1.2)
f.text(P(a)[0] + 6, P(a)[1] + 4, "a", size=11, color=NAVY, bold=True, anchor="start")
f.text(P(b)[0] - 4, P(b)[1] - 8, "b", size=11, color=TEAL, bold=True)
f.text(P(p)[0] - 6, P(p)[1] + 18, "proj", size=10.5, color=AMBER, bold=True)
f.text(180, 50, "a.b = 8", size=10.5, color=SLATE, anchor="start")
f.text(180, 70, "proj = (2.4, 0.8)", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(180, 90, "b - proj = (-0.4, 1.2)", size=10.5, color=RED, bold=True, anchor="start")
f.text(180, 110, "a.(b - proj) = 0", size=10.5, color=RED, bold=True, anchor="start")
f.text(180, 130, "angle(a, b) = 26.57", size=10.5, color=SLATE, anchor="start")
f.text(150, 228, "red part meets a at a right angle", size=10.5, color=SLATE)
```

## Formula and fact sheet

- Subspace test: contains 0, closed under + and scalar multiplication.
- Independent ⇔ only the trivial combination gives 0; basis = independent + spanning; dimension = size of any basis.
- Rank–nullity: rank + nullity = number of columns (dim ker + dim im = dim V).
- Matrix of T has columns $T (e_{i})$. Composition = product. Similar matrices $P^{-1} A P$.
- $u \cdot v$ = ‖u‖‖v‖cos θ; proj_u v = (v·u/u·u)u; Gram–Schmidt; least squares $A^{T} A X = A^{T} B$.

## Chapter summary

- Vector spaces abstract the idea of vector; subspaces, span, independence, basis and dimension organise them.
- Rank–nullity ties the solutions of $A X = 0$ to the rank of A.
- Linear maps are matrices; their kernel and image measure what is lost and what is reached.
- Orthogonal bases and projections give coordinates, Gram–Schmidt and least squares.

## Practice

1. Is $W = \{(x ,\  y ,\  z) \mid x + y + z = 0\}$ a subspace of $\mathbb{R}^{3}$? Find a basis and the dimension.
2. Test the independence of (1, 2, 1), (2, 1, 0), (1, −1, −1).
3. Show $\{1 ,\  1 + x ,\  1 + x + x^{2}\}$ is a basis of $P_{2}$ and find the coordinates of $3 + 2 x + x^{2}$.
4. A $4 \times 6$ matrix has rank 3. Find the dimensions of its four subspaces.
5. Find the matrix of $T (x ,\  y ,\  z) = (x - y ,\  y + 2 z)$ and its kernel dimension.
6. Find the matrix of the rotation by $60 ^{\circ}$ followed by a scaling by 2.
7. Find the angle between (1, 2, 2) and (2, −1, 2) and the projection of the first on the second.
8. Apply Gram–Schmidt to (1, 0, 0), (1, 1, 0), (1, 1, 1).
9. Is the set $\{(x ,\  y) \mid y = 2 x + 1\}$ a subspace? Why or why not?
10. Fit a least-squares line through (0, 1), (1, 3), (2, 4).

::: note Answers and worked solutions
**1.** Contains 0; the sum of two vectors with coordinate-sum 0 also has sum 0; so a subspace (a plane through the origin). Basis {(1, −1, 0), (0, 1, −1)}, **dimension 2**.

**2.** $\det \begin{bmatrix} 1 & 2 & 1 \\ 2 & 1 & - 1 \\ 1 & 0 & - 1 \end{bmatrix} = 1 (- 1 - 0) - 2 (- 2 + 1) + 1 (0 - 1) = - 1 + 2 - 1 = 0$, so **dependent** ($(1 ,\  2 ,\  1) - (2 ,\  1 ,\  0) = (- 1 ,\  1 ,\  1) = - (1 ,\  - 1 ,\  - 1)$, i.e. $v_{1} - v_{2} + v_{3} = 0$).

**3.** Three polynomials of degrees 0, 1, 2 are independent and dim $P_{2} = 3$, so they form a basis. $a + b (1 + x) + c (1 + x + x^{2}) = 3 + 2 x + x^{2}$: $x^{2}$: $c = 1 ;\  x$: $b + c = 2 \Rightarrow b = 1$; constant: $a + b + c = 3 \Rightarrow a = 1$. Coordinates **(1, 1, 1)**.

**4.** Column space 3, row space 3, null space $6 - 3 = 3$, left null space $4 - 3 = 1$.

**5.** $\begin{bmatrix} 1 & - 1 & 0 \\ 0 & 1 & 2 \end{bmatrix}$; rank 2, nullity $3 - 2$ = **1** (kernel spanned by (2, 2, −1): $2 - 2 = 0$ and $2 - 2 = 0$ ✓).

**6.** Rotation $R = \begin{bmatrix} \frac{1}{2} & - \frac{\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2} \end{bmatrix}$; scale by 2 first applied after: 2R = $\begin{bmatrix} 1 & - \sqrt{3} \\ \sqrt{3} & 1 \end{bmatrix}$.

**7.** $u \cdot v = 2 - 2 + 4 = 4$; ‖u‖ = 3, ‖v‖ = $3 ;\  \cos \theta = \frac{4}{9} \Rightarrow \theta$ ≈ **$63.6 ^{\circ}$**. Projection = ($\frac{4}{9} ) ( 2 ,\  - 1$, 2) = **$\left( \frac{8}{9} ,\  - \frac{4}{9} ,\  \frac{8}{9} \right)$**.

**8.** $q_{1} = (1 ,\  0 ,\  0) ;\  w_{2} = (1 ,\  1 ,\  0) - (1) (1 ,\  0 ,\  0) = (0 ,\  1 ,\  0) \Rightarrow q_{2} = (0 ,\  1 ,\  0) ;\  w_{3} = (1 ,\  1 ,\  1) - (1 ,\  0 ,\  0) - (0 ,\  1 ,\  0) = (0 ,\  0 ,\  1) \Rightarrow q_{3} = (0 ,\  0 ,\  1)$: the standard basis.

**9.** **No**: (0, 0) does not satisfy $y = 2 x + 1$, so the zero vector is missing (a line not through the origin).

**10.** $A = \begin{bmatrix} 1 & 0 \\ 1 & 1 \\ 1 & 2 \end{bmatrix} ,\  B = (1 ,\  3 ,\  4)$: $A^{T} A = \begin{bmatrix} 3 & 3 \\ 3 & 5 \end{bmatrix} ,\  A^{T} B = (8 ,\  11)$. Solve $3 a + 3 b = 8 ,\  3 a + 5 b = 11 \Rightarrow 2 b = 3 \Rightarrow b = 1.5 ,\  a = \frac{8}{3} - 1.5 = \frac{7}{6}$: **$y = 1.167$ + 1.5x**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Find the rank, nullity, a basis for the null space and a basis for the column space of $A = \begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 0 & 1 \end{bmatrix}$, and verify rank–nullity.**

*Introduction.* The rank is the number of independent rows (equivalently columns); the nullity is the dimension of the solution space of $A X = 0$; rank–nullity states rank + nullity = *n*.

*Row reduction.* R2 → R2 − 2R1 gives [0, 0, 0]. R3 → R3 − R1 gives [0, −2, −2]. So the non-zero rows are [1, 2, 3] and [0, −2, −2]: **rank = 2**.

*Null space.* $x + 2 y + 3 z = 0$ and $- 2 y - 2 z = 0$ give $y = - z$ and $x = - 3 z + 2 z = - z$. With $z = 1$ the vector is (−1, −1, 1); the null space is the line spanned by it, so **nullity = 1**. Check: $- 1 - 2 + 3 = 0$ and $- 1 + 0 + 1 = 0$.

*Column space.* The pivot columns are columns 1 and 2, so a basis is {(1, 2, 1), (2, 4, 0)}; column 3 equals column 1 + column 2, which agrees with the null vector.

*Verification.* rank + nullity = $2 + 1 = 3$ = number of columns *n*. *Conclusion.* rank 2, nullity 1, null basis {(−1, −1, 1)}, column basis {(1, 2, 1), (2, 4, 0)}.

**Q2 (10 marks). Define linear independence, basis and dimension, and linear transformation, with examples; relate kernel, image and rank–nullity.**

*Introduction.* A vector space is a set closed under addition and scalar multiplication. Its structure is described by independence, basis and dimension, and its maps by linear transformations.

*Linear independence, basis, dimension.*

1. **Linear combination.** $c_{1} v_{1} + c_{2} v_{2} + \ldots + c_{k} v_{k}$.
2. **Independent.** Vectors are independent if the only combination equal to 0 has all $c_{i} = 0$. The vectors (1, 0, 1), (0, 1, 1), (1, 1, 2) are **dependent**, because the third equals the sum of the first two (rank 2, not 3).
3. **Basis.** A set that is independent and spans the space. The standard basis (1, 0, 0), (0, 1, 0), (0, 0, 1) is a basis of $\mathbb{R}^{3}$.
4. **Dimension.** The number of vectors in any basis; all bases have the same size, so dim $\mathbb{R}^{3} = 3$.

*Linear transformations.*

5. **Definition.** T is linear if $T (u + v) = T (u) + T (v)$ and $T (c u)$ = cT(u). Every linear map $\mathbb{R}^{n} \to \mathbb{R}^{m}$ is multiplication by an $m \times n$ matrix.
6. **Example.** $T (x ,\  y) = (x + y ,\  x - y)$ has matrix $\begin{bmatrix} 1 & 1 \\ 1 & - 1 \end{bmatrix}$ with determinant −2, so it is invertible.
7. **Kernel and image.** ker $T = \{v : T (v) = 0\}$ is the null space; im T is the column space.
8. **Rank–nullity.** dim ker T + dim im T = dim of the input space. For the example, ker T = {0} (dimension 0) and im $T = \mathbb{R}^{2}$ (dimension 2), so $0 + 2 = 2$.

| Idea | Test or formula |
|---|---|
| Independent | only trivial combination gives 0 (rank = number of vectors) |
| Basis | independent and spanning |
| Dimension | size of any basis |
| Rank–nullity | rank + nullity = *n* |
| Invertible map | kernel = {0} and square matrix |

*Conclusion.* Independence, basis and dimension measure the size of a space, and kernel and image measure what a linear map keeps and what it destroys; rank–nullity balances the two.

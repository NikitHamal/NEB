---
subject: Mathematics
grade: IOE
unit: 6
title: Vectors and their Products
hours: 3
area: Mathematics
---

Vectors carry about **3 questions** (our estimate). The booklet's model question — the projection of $\vec b=2\hat i+3\hat j-2\hat k$ on $\vec a=\hat i+2\hat j+3\hat k$ — is typical: a dot product, a cross product, or a scalar triple product, computed from components. The whole chapter reduces to four formulas used fluently.

::: key What the paper asks from this chapter
- Components, magnitude, unit vector, section formula, collinearity.
- Dot product: $\vec a\cdot\vec b=ab\cos\theta$; projection of $\vec b$ on $\vec a$ is $\dfrac{\vec a\cdot\vec b}{|\vec a|}$.
- Cross product: $|\vec a\times\vec b|=ab\sin\theta$, area of a triangle $\frac{1}{2}|\vec a\times\vec b|$.
- Scalar triple product: volume, coplanarity ($[\vec a\,\vec b\,\vec c]=0$).
- Linear dependence: two vectors are dependent iff parallel; three iff coplanar.
:::

## 6.1 Vectors in plane and space, algebra, linear combination, dependence

A vector has magnitude and direction. For $\vec a=a_1\hat i+a_2\hat j+a_3\hat k$: $|\vec a|=\sqrt{a_1^2+a_2^2+a_3^2}$ and the **unit vector** is $\hat a=\vec a/|\vec a|$. Direction cosines $\frac{a_1}{|\vec a|},\frac{a_2}{|\vec a|},\frac{a_3}{|\vec a|}$. The vector $\overrightarrow{AB}=\vec b-\vec a$ (head minus tail).

- Triangle law: $\overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC}$; the parallelogram law; $|\vec a\pm\vec b|^2=a^2+b^2\pm2\vec a\cdot\vec b$.
- **Section formula:** point dividing $AB$ in the ratio $m:n$ internally is $\dfrac{m\vec b+n\vec a}{m+n}$ (externally $\dfrac{m\vec b-n\vec a}{m-n}$); midpoint $\frac{\vec a+\vec b}{2}$; centroid $\frac{\vec a+\vec b+\vec c}{3}$.
- **Collinear points** $A,B,C$: $\overrightarrow{AC}=k\,\overrightarrow{AB}$.
- **Linear combination:** $\vec r=x\vec a+y\vec b+z\vec c$. A set is **linearly dependent** if some non-trivial combination is zero: two vectors iff parallel; three iff coplanar ($[\vec a\,\vec b\,\vec c]=0$); any four in space always. Three non-coplanar vectors form a basis of space.

## 6.2 Product of two vectors, scalar and vector product, scalar triple product

### Scalar (dot) product

$\vec a\cdot\vec b=ab\cos\theta=a_1b_1+a_2b_2+a_3b_3$; commutative and distributive. $\hat i\cdot\hat i=1$, $\hat i\cdot\hat j=0$. $\vec a\cdot\vec a=|\vec a|^2$. **Perpendicular iff $\vec a\cdot\vec b=0$.**
$\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}$. **Projection** of $\vec b$ on $\vec a$: $\dfrac{\vec a\cdot\vec b}{|\vec a|}$ (a scalar); the vector component is that times $\hat a$. **Work** $=\vec F\cdot\vec d$. $(\vec a+\vec b)\cdot(\vec a-\vec b)=a^2-b^2$.

### Vector (cross) product

$\vec a\times\vec b=ab\sin\theta\,\hat n$ (right-hand rule), anticommutative; $\hat i\times\hat j=\hat k$, $\hat j\times\hat k=\hat i$, $\hat k\times\hat i=\hat j$.
$$\vec a\times\vec b=(det | \hat i&\hat j&\hat k ; a_1&a_2&a_3 ; b_1&b_2&b_3 |).$$
$|\vec a\times\vec b|^2=a^2b^2-(\vec a\cdot\vec b)^2$ (Lagrange). **Parallel iff $\vec a\times\vec b=\vec 0$.** Area of a parallelogram with sides $\vec a,\vec b$ is $|\vec a\times\vec b|$; of the triangle, half. A unit vector perpendicular to both: $\pm\dfrac{\vec a\times\vec b}{|\vec a\times\vec b|}$. Moment of a force: $\vec r\times\vec F$.

### Triple products

$[\vec a\,\vec b\,\vec c]=\vec a\cdot(\vec b\times\vec c)=$ the 3×3 determinant of components; cyclic invariant, changes sign when two vectors swap. **Volume** of the parallelepiped $=|[\vec a\,\vec b\,\vec c]|$; tetrahedron $=\frac{1}{6}|[\vec a\,\vec b\,\vec c]|$. **Coplanar iff $[\vec a\,\vec b\,\vec c]=0$.** Vector triple product: $\vec a\times(\vec b\times\vec c)=\vec b(\vec a\cdot\vec c)-\vec c(\vec a\cdot\vec b)$ ("BAC minus CAB").

::: caution
The dot product is a **scalar**, the cross product a **vector**. $\vec a\times(\vec b\times\vec c)\ne(\vec a\times\vec b)\times\vec c$. The projection can be negative.
:::

## Formula and fact sheet

| Topic | Result |
|---|---|
| angle | $\cos\theta=\frac{\vec a\cdot\vec b}{ab}$ |
| projection of $\vec b$ on $\vec a$ | $\frac{\vec a\cdot\vec b}{|\vec a|}$ |
| triangle area | $\frac{1}{2}|\vec a\times\vec b|$ |
| Lagrange | $|\vec a\times\vec b|^2=a^2b^2-(\vec a\cdot\vec b)^2$ |
| volume | $|[\vec a\,\vec b\,\vec c]|$; tetrahedron $\frac{1}{6}$ of it |
| triple product | $\vec a\times(\vec b\times\vec c)=\vec b(\vec a\cdot\vec c)-\vec c(\vec a\cdot\vec b)$ |

## Chapter summary

- Head minus tail gives $\overrightarrow{AB}$; the section formula weights the opposite end.
- Dot product zero means perpendicular; cross product zero means parallel; triple product zero means coplanar.
- Projection is $\frac{\vec a\cdot\vec b}{|\vec a|}$, a signed scalar.
- Areas come from $|\vec a\times\vec b|$, volumes from the scalar triple product.

## Practice questions

**Set A — Recall (10 questions)**

1. For $\vec a=2\hat i+3\hat j+\hat k$ and $\vec b=\hat i-\hat j+2\hat k$, $\vec a\cdot\vec b$ equals
   (a) 7 (b) 5 (c) 1 (d) $-1$
2. The magnitude of $3\hat i+4\hat j-12\hat k$ is
   (a) 13 (b) 19 (c) 11 (d) 5
3. $\hat i\times\hat j$ equals
   (a) 0 (b) $-\hat k$ (c) 1 (d) $\hat k$
4. The vectors $2\hat i+\lambda\hat j+\hat k$ and $\hat i-2\hat j+3\hat k$ are perpendicular for $\lambda=$
   (a) 2 (b) $5/2$ (c) $3/2$ (d) 1
5. The area of the parallelogram with adjacent sides $\hat i+\hat j$ and $\hat j+\hat k$ is
   (a) 2 (b) $\sqrt{2}$ (c) $\sqrt{3}$ (d) 3
6. If $[\vec a\,\vec b\,\vec c]=0$, the three vectors are
   (a) coplanar (b) parallel (c) mutually perpendicular (d) collinear
7. The angle between $\hat i+\hat j$ and $\hat j$ is
   (a) $30^\circ$ (b) $60^\circ$ (c) $90^\circ$ (d) $45^\circ$
8. The midpoint of $A(2,4,6)$ and $B(4,0,2)$ is
   (a) $(6,4,8)$ (b) $(3,2,4)$ (c) $(1,2,2)$ (d) $(3,4,2)$
9. The unit vector along $3\hat i-4\hat j$ is
   (a) $\dfrac{3\hat i-4\hat j}{25}$ (b) $3\hat i-4\hat j$ (c) $\dfrac{3\hat i+4\hat j}{5}$ (d) $\dfrac{3\hat i-4\hat j}{5}$
10. If $|\vec a|=5$ and $|\vec b|=3$, then $(\vec a+\vec b)\cdot(\vec a-\vec b)$ is
    (a) 16 (b) 34 (c) 4 (d) 25

::: note Answers and explanations — Set A
**1.** (c) — $2-3+2=1$.
**2.** (a) — $\sqrt{9+16+144}=13$.
**3.** (d) — right-hand rule: $\hat i\times\hat j=\hat k$ ($\hat j\times\hat i=-\hat k$).
**4.** (b) — $2-2\lambda+3=0\Rightarrow\lambda=\frac{5}{2}$.
**5.** (c) — $\vec a\times\vec b=(1,-1,1)$, magnitude $\sqrt{3}$.
**6.** (a) — a zero scalar triple product means the vectors lie in one plane.
**7.** (d) — $\cos\theta=\frac{1}{\sqrt{2}}$.
**8.** (b) — average of the coordinates.
**9.** (d) — divide by the magnitude 5.
**10.** (a) — $|\vec a|^2-|\vec b|^2=25-9=16$.
:::

**Set B — Understanding (7 questions)**

1. The projection of $\vec b=2\hat i+3\hat j-2\hat k$ on $\vec a=\hat i+2\hat j+3\hat k$ is
   (a) $2/\sqrt{17}$ (b) $2/\sqrt{14}$ (c) $2/7$ (d) $-2/7$
2. If $|\vec a|=3$, $|\vec b|=4$ and the angle between them is $30^\circ$, then $|\vec a\times\vec b|$ is
   (a) 12 (b) $6\sqrt{3}$ (c) 6 (d) 3
3. The vectors $2\hat i-\hat j+\hat k$, $\hat i+2\hat j-3\hat k$ and $3\hat i+\lambda\hat j+5\hat k$ are coplanar for $\lambda=$
   (a) 4 (b) $-1$ (c) 1 (d) $-4$
4. The area of the triangle with vertices $(1,0,0)$, $(0,1,0)$, $(0,0,1)$ is
   (a) $\frac{\sqrt{3}}{2}$ (b) $\sqrt{3}$ (c) $\frac{1}{2}$ (d) $\frac{3}{2}$
5. The volume of the parallelepiped with edges $\hat i+\hat j$, $\hat j+\hat k$, $\hat k+\hat i$ is
   (a) 1 (b) 4 (c) 2 (d) 3
6. A unit vector perpendicular to both $\hat i+\hat j$ and $\hat j+\hat k$ is
   (a) $\frac{\hat i+\hat j+\hat k}{\sqrt{3}}$ (b) $\frac{\hat i-\hat j+\hat k}{\sqrt{3}}$ (c) $\frac{\hat i-\hat j-\hat k}{3}$ (d) $\frac{\hat i+\hat j-\hat k}{\sqrt{3}}$
7. The value of $\hat i\times(\hat j\times\hat i)$ is
   (a) $\hat j$ (b) $0$ (c) $-\hat j$ (d) $\hat k$

::: note Answers and explanations — Set B
**1.** (b) — $\vec a\cdot\vec b=2+6-6=2$, $|\vec a|=\sqrt{14}$. The projection of $\vec b$ on $\vec a$ divides by $|\vec a|$.
**2.** (c) — $3\cdot4\sin30^\circ=6$.
**3.** (d) — the determinant is $28+7\lambda=0$.
**4.** (a) — $\overrightarrow{AB}\times\overrightarrow{AC}=(1,1,1)$; half of $\sqrt{3}$.
**5.** (c) — $(det | 1&1&0 ; 0&1&1 ; 1&0&1 |)=1+1=2$.
**6.** (b) — $(\hat i+\hat j)\times(\hat j+\hat k)=\hat i-\hat j+\hat k$, magnitude $\sqrt{3}$.
**7.** (a) — $\hat j\times\hat i=-\hat k$, and $\hat i\times(-\hat k)=\hat j$. Check with BAC–CAB: $\hat j(\hat i\cdot\hat i)-\hat i(\hat i\cdot\hat j)=\hat j$.
:::

**Set C — Application (6 questions)**

1. The points $(1,1,1)$, $(2,3,4)$ and $(3,5,\lambda)$ are collinear when $\lambda=$
   (a) 6 (b) 7 (c) 8 (d) 5
2. The work done by $\vec F=2\hat i+3\hat j+\hat k$ in moving a particle from $(1,1,1)$ to $(3,2,4)$ is
   (a) 10 (b) 12 (c) 8 (d) 9
3. If $\vec a,\vec b$ are unit vectors at $60^\circ$ to each other, $|\vec a+\vec b|$ is
   (a) $\sqrt{2}$ (b) 2 (c) 1 (d) $\sqrt{3}$
4. If $|\vec a|=2$, $|\vec b|=3$ and $\vec a\cdot\vec b=3$, then $|\vec a\times\vec b|$ is
   (a) 3 (b) 6 (c) 9 (d) $3\sqrt{3}$
5. The vectors $2\hat i+3\hat j$ and $\hat i+\lambda\hat j$ are linearly dependent for $\lambda=$
   (a) $2/3$ (b) $3/2$ (c) 6 (d) $1/6$
6. The volume of the tetrahedron with vertices $O$, $(1,0,0)$, $(0,2,0)$, $(0,0,3)$ is
   (a) 1 (b) 6 (c) 3 (d) 2

::: note Answers and explanations — Set C
**1.** (b) — $\overrightarrow{AB}=(1,2,3)$, $\overrightarrow{AC}=(2,4,\lambda-1)$ must be $2\overrightarrow{AB}$: $\lambda-1=6$.
**2.** (a) — displacement $(2,1,3)$: $4+3+3=10$.
**3.** (d) — $|\vec a+\vec b|^2=1+1+2\cdot\frac{1}{2}=3$.
**4.** (d) — $|\vec a\times\vec b|^2=36-9=27$.
**5.** (b) — parallel: $\frac{2}{1}=\frac{3}{\lambda}$.
**6.** (a) — $\frac{1}{6}|1\cdot2\cdot3|=1$.
:::

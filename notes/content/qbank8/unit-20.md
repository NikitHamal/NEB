---
subject: Question Bank
grade: 8
unit: 20
title: "Optional Mathematics: Unit-wise Objective Question Bank"
hours: 0
area: Optional Mathematics
---

Optional Mathematics in grade 8 is examined by your own school, in a written paper of 50 marks and two hours. Group A of that paper is **ten one-mark objective items**. They are the cheapest marks in the paper and the easiest to throw away: a sign slipped in a rotation rule, a degree confused with a grade, a median found before the data were put in order. This chapter drills those items unit by unit for all ten units of the Optional Mathematics 8 book, in the same order as the book.

Each section opens with a **facts line**, the few results that the items of that unit actually use. Then come twelve items, and then a key that gives the answer with a one-line reason. Work an item in under a minute, check it in ten seconds, and move on. The reasons matter more than the letters: a reason you can repeat is a mark you will not lose next time.

::: key The 50-mark paper used in this bank
| Group | Items | Marks each | Total | What it tests |
|---|---|---|---|---|
| A | 10 | 1 | 10 | one-step recall or a single substitution |
| B | 10 | 2 | 20 | one short method |
| C | 5 | 4 | 20 | a full method, a figure or a proof |
| **Total** | **25** | | **50** | 2 hours |

There is no national specification grid for this school paper. The weights in the chart below are the ones this bank uses for its model papers (chapter 22): every unit gets one Group A item, and the longer questions follow the size of each unit.
:::

::: caution Practice items, not past questions
Every item below is an original **practice** item written to the pattern above and to the chapters of the Optional Mathematics 8 book. None is claimed to come from any school's paper. Every numerical answer was worked out independently before it was written down.
:::

```figure caption="Marks per unit in the 50-mark paper used in this bank. Trigonometry and coordinate geometry carry the most; every unit has at least one Group A item, so no unit can be skipped."
fig, ax = barh_ranked(
    ["Trigonometry", "Coordinate Geometry", "Relation and Function", "Matrix", "Vector",
     "Transformation", "Statistics", "Polynomials", "Sequence and Series", "Limit"],
    [9, 7, 5, 5, 5, 5, 5, 3, 3, 3], unit=" marks", figsize=(5.2, 4.3),
    highlight={"Trigonometry", "Coordinate Geometry"})
```

## 20.1 Relation and Function

**Facts.** $(a,b)=(c,d)$ exactly when $a=c$ and $b=d$. $A\times B=\{(a,b): a\in A, b\in B\}$ and $n(A\times B)=n(A)\times n(B)$. A relation from $A$ to $B$ is a subset of $A\times B$, so there are $2^{n(A)\times n(B)}$ relations. The domain is the set of first components and the range the set of second components; $R^{-1}$ swaps every pair. A function gives **every** member of the domain **exactly one** image; a graph is a function if no vertical line meets it twice.

1. If $(a+3,\ 2b-1)=(5,\ 7)$, then $a+b$ is <span class="marks">[1]</span>
   (a) 6 (b) 2 (c) 4 (d) 8
2. If $(x,\ y)=(y,\ 4)$, then $x$ is <span class="marks">[1]</span>
   (a) 0 (b) 4 (c) 2 (d) $-4$
3. If $A=\{1,2,3\}$ and $B=\{4,5\}$, the number of members of $A\times B$ is <span class="marks">[1]</span>
   (a) 5 (b) 6 (c) 8 (d) 9
4. If $n(A\times B)=12$ and $n(A)=4$, then $n(B)$ is <span class="marks">[1]</span>
   (a) 3 (b) 8 (c) 16 (d) 48
5. For $A=\{p,q\}$ and $B=\{1,2\}$, which pair belongs to $A\times B$? <span class="marks">[1]</span>
   (a) $(1,p)$ (b) $(q,2)$ (c) $(2,q)$ (d) $(p,q)$
6. If $n(A)=2$ and $n(B)=2$, the number of relations from $A$ to $B$ is <span class="marks">[1]</span>
   (a) 4 (b) 8 (c) 16 (d) 2
7. The range of $R=\{(1,2),(2,4),(3,6)\}$ is <span class="marks">[1]</span>
   (a) $\{1,2,3\}$ (b) $\{2,4,6\}$ (c) $\{1,2,3,4,6\}$ (d) $\{2\}$
8. On $A=\{1,2,3,4\}$, the relation $R=\{(x,y): y=x+1\}$ is <span class="marks">[1]</span>
   (a) $\{(1,2),(2,3),(3,4)\}$ (b) $\{(1,2),(2,3),(3,4),(4,5)\}$ (c) $\{(2,1),(3,2),(4,3)\}$ (d) $\{(1,1),(2,2)\}$
9. The inverse of $R=\{(a,1),(b,2)\}$ is <span class="marks">[1]</span>
   (a) $\{(1,a),(2,b)\}$ (b) $\{(a,2),(b,1)\}$ (c) $\{(1,b),(2,a)\}$ (d) $\{(a,b),(1,2)\}$
10. Which kind of arrow diagram is **not** a function? <span class="marks">[1]</span>
    (a) one-to-one (b) many-to-one (c) one-to-many (d) constant
11. If $f(x)=5-2x$, then $f(-3)$ is <span class="marks">[1]</span>
    (a) $-1$ (b) 11 (c) $-11$ (d) 1
12. If $f(x)=x^2$ with domain $\{-2,-1,0,1,2\}$, the range is <span class="marks">[1]</span>
    (a) $\{-4,-1,0,1,4\}$ (b) $\{0,1,4\}$ (c) $\{0,1,2,4\}$ (d) $\{1,4\}$

::: note Answers to 20.1
**1.** (a) — $a+3=5$ gives $a=2$; $2b-1=7$ gives $b=4$; $2+4=6$.
**2.** (b) — the second components give $y=4$, and the first give $x=y=4$.
**3.** (b) — $3\times2=6$.
**4.** (a) — $4\times n(B)=12$.
**5.** (b) — the first component must come from $A$ and the second from $B$.
**6.** (c) — $A\times B$ has 4 pairs, and a set of 4 has $2^4=16$ subsets.
**7.** (b) — the range is the set of second components.
**8.** (a) — $(4,5)$ is not allowed because $5\notin A$.
**9.** (a) — swap the components of each pair.
**10.** (c) — one member with two images breaks the rule of a function.
**11.** (b) — $5-2(-3)=5+6=11$.
**12.** (b) — squares are never negative, and repeated images are listed once.
:::

## 20.2 Polynomials

**Facts.** A polynomial has only **whole-number** powers of the variable. The degree is the highest power (for a term in several variables, the sum of the powers). By degree: constant 0, linear 1, quadratic 2, cubic 3, biquadratic 4; by terms: monomial, binomial, trinomial. Standard form lists the powers in descending order; the first coefficient is the leading coefficient. Equal polynomials have equal coefficients of like powers. The degree of a product is the sum of the degrees.

1. Which of these is **not** a polynomial? <span class="marks">[1]</span>
   (a) $3x^2+2$ (b) $\sqrt{3}\,x+1$ (c) $\frac{2}{x}+1$ (d) 7
2. The degree of $3x^2y^2-5x^3+y$ is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 5
3. The polynomial $4x^3-2x+1$ is a <span class="marks">[1]</span>
   (a) cubic trinomial (b) cubic binomial (c) quadratic trinomial (d) biquadratic
4. The leading coefficient of $2-7x+3x^2-x^3$ is <span class="marks">[1]</span>
   (a) 2 (b) $-7$ (c) 3 (d) $-1$
5. A polynomial of degree 1 is called <span class="marks">[1]</span>
   (a) constant (b) linear (c) quadratic (d) cubic
6. If $f(x)=x^3-2x+1$, then $f(2)$ is <span class="marks">[1]</span>
   (a) 5 (b) 3 (c) 13 (d) 1
7. If $(p-2)x^2+5x=3x^2+qx$, then $(p,q)$ is <span class="marks">[1]</span>
   (a) $(5,5)$ (b) $(1,5)$ (c) $(5,3)$ (d) $(3,5)$
8. $(2x^2-3x+1)+(x^2+3x-4)$ equals <span class="marks">[1]</span>
   (a) $3x^2-3$ (b) $3x^2+6x-3$ (c) $x^2-3$ (d) $3x^2-6x-3$
9. $(x^2+2x)-(3x^2-x)$ equals <span class="marks">[1]</span>
   (a) $-2x^2+3x$ (b) $-2x^2+x$ (c) $4x^2+x$ (d) $-2x^2-3x$
10. $(x-3)^2$ equals <span class="marks">[1]</span>
    (a) $x^2-9$ (b) $x^2-6x+9$ (c) $x^2+9$ (d) $x^2-3x+9$
11. $(2x+1)(x-4)$ equals <span class="marks">[1]</span>
    (a) $2x^2-7x-4$ (b) $2x^2-9x-4$ (c) $2x^2+7x-4$ (d) $2x^2-8x-4$
12. If $f(x)$ has degree 4 and $g(x)$ has degree 3, then $f(x)\cdot g(x)$ has degree <span class="marks">[1]</span>
    (a) 1 (b) 7 (c) 12 (d) 4

::: note Answers to 20.2
**1.** (c) — $\frac{2}{x}=2x^{-1}$ has a negative power; a surd coefficient such as $\sqrt{3}$ is allowed.
**2.** (c) — the term $3x^2y^2$ has degree $2+2=4$, more than 3 or 1.
**3.** (a) — highest power 3 and three terms.
**4.** (d) — in standard form $-x^3+3x^2-7x+2$, the first coefficient is $-1$.
**5.** (b) — degree 1 is linear.
**6.** (a) — $8-4+1=5$.
**7.** (a) — $p-2=3$ gives $p=5$, and $q=5$.
**8.** (a) — the $x$ terms cancel: $-3x+3x=0$.
**9.** (a) — $x^2-3x^2=-2x^2$ and $2x-(-x)=3x$.
**10.** (b) — $(a-b)^2=a^2-2ab+b^2$; the middle term $-6x$ is not optional.
**11.** (a) — $2x^2-8x+x-4=2x^2-7x-4$.
**12.** (b) — degrees add: $4+3=7$.
:::

## 20.3 Sequence and Series

**Facts.** The general term $t_n$ gives the term in position $n$. Equal first differences $d$: $t_n=a+(n-1)d$; equal ratios: $t_n=ar^{n-1}$; equal second differences: the rule contains $n^2$. A number is a term only if solving $t_n=$ number gives a natural number $n$. $\sum_{k=1}^{n}t_k$ adds $t_k$ for $k=1$ to $n$; the number of terms is upper limit $-$ lower limit $+1$. $1+2+\cdots+n=\frac{n(n+1)}{2}$; $1+3+\cdots+(2n-1)=n^2$; $t_n=S_n-S_{n-1}$.

1. The 6th term of the sequence with $t_n=n^2-1$ is <span class="marks">[1]</span>
   (a) 35 (b) 36 (c) 11 (d) 25
2. The general term of $5, 8, 11, 14, \ldots$ is <span class="marks">[1]</span>
   (a) $3n+2$ (b) $5n$ (c) $n+3$ (d) $3n+5$
3. The next term of $1, 3, 6, 10, 15, \ldots$ is <span class="marks">[1]</span>
   (a) 20 (b) 21 (c) 25 (d) 18
4. The next term of $64, 32, 16, 8, \ldots$ is <span class="marks">[1]</span>
   (a) 0 (b) 2 (c) 4 (d) 6
5. Which term of $3, 7, 11, \ldots$ is 43? <span class="marks">[1]</span>
   (a) 9th (b) 10th (c) 11th (d) 12th
6. The general term of $1, -1, 1, -1, \ldots$ is <span class="marks">[1]</span>
   (a) $(-1)^n$ (b) $(-1)^{n+1}$ (c) $-1$ (d) $n$
7. $\sum_{k=1}^{3}k^2$ equals <span class="marks">[1]</span>
   (a) 6 (b) 9 (c) 14 (d) 36
8. $\sum_{k=1}^{4}3$ equals <span class="marks">[1]</span>
   (a) 3 (b) 7 (c) 12 (d) 81
9. $1+3+5+7+9$ in sigma notation is <span class="marks">[1]</span>
   (a) $\sum_{k=1}^{5}(2k-1)$ (b) $\sum_{k=1}^{9}k$ (c) $\sum_{k=1}^{5}2k$ (d) $\sum_{k=0}^{5}(2k+1)$
10. The sum of the first 20 natural numbers is <span class="marks">[1]</span>
    (a) 200 (b) 210 (c) 400 (d) 420
11. The number of terms in $\sum_{k=5}^{12}t_k$ is <span class="marks">[1]</span>
    (a) 7 (b) 8 (c) 12 (d) 17
12. If $S_n=n^2$ for every $n$, then $t_3$ is <span class="marks">[1]</span>
    (a) 9 (b) 5 (c) 3 (d) 4

::: note Answers to 20.3
**1.** (a) — $6^2-1=35$.
**2.** (a) — the difference is 3 and each term is 2 more than $3n$.
**3.** (b) — the differences are $2, 3, 4, 5$, so the next is $15+6=21$.
**4.** (c) — each term is half the one before.
**5.** (c) — $t_n=4n-1=43$ gives $n=11$.
**6.** (b) — it must be $+1$ when $n=1$; $(-1)^{n+1}$ does that.
**7.** (c) — $1+4+9=14$.
**8.** (c) — the constant 3 is added 4 times.
**9.** (a) — the $k$th odd number is $2k-1$; option (d) starts at $k=0$ and has six terms, ending with 11.
**10.** (b) — $\frac{20\times21}{2}=210$.
**11.** (b) — $12-5+1=8$.
**12.** (b) — $t_3=S_3-S_2=9-4=5$.
:::

::: caution Count the terms from both limits
Item 11 is lost by writing $12-5=7$. The terms are $t_5, t_6, \ldots, t_{12}$: list the first two and the last if in doubt, and the "+1" will not be forgotten. The same slip appears in item 9, where starting at $k=0$ adds an extra term.
:::

## 20.4 Limit

**Facts.** A sequence has limit $l$ if its terms come as close to $l$ as we wish and stay that close; the limit need not be a term. $\lim_{n\to\infty}\frac{1}{n}=0$; $\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\cdots$ approaches 1. $x\rightarrow a$ means $x$ approaches $a$ but never equals it. For a polynomial, substitute; for a $\frac{0}{0}$ form, factorise and cancel first. The limit exists only if the left-hand and right-hand values agree.

1. The sequence $2, 1.5, 1.25, 1.125, \ldots$ tends to <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) 1.1
2. $\lim_{n\to\infty}\frac{5}{n}$ is <span class="marks">[1]</span>
   (a) 5 (b) 0 (c) $\infty$ (d) 1
3. $\lim_{n\to\infty}\frac{n+1}{n}$ is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) $\infty$
4. The sum $\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\cdots$ approaches <span class="marks">[1]</span>
   (a) $\frac{1}{2}$ (b) 1 (c) 2 (d) $\infty$
5. $\lim_{x\to3}(2x-1)$ is <span class="marks">[1]</span>
   (a) 5 (b) 6 (c) 7 (d) 3
6. $\lim_{x\to0}(x^2+4)$ is <span class="marks">[1]</span>
   (a) 0 (b) 2 (c) 4 (d) not defined
7. $\lim_{x\to2}\frac{x^2-4}{x-2}$ is <span class="marks">[1]</span>
   (a) 0 (b) 2 (c) 4 (d) not defined
8. $\lim_{x\to1}\frac{x^2-1}{x-1}$ is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) not defined
9. For $f(x)=\frac{x^2-9}{x-3}$, the value $f(3)$ is <span class="marks">[1]</span>
   (a) 6 (b) 0 (c) 9 (d) not defined
10. "$x\rightarrow5^-$" means that $x$ approaches 5 <span class="marks">[1]</span>
    (a) through values greater than 5 (b) through values less than 5 (c) and becomes 5 (d) from both sides
11. If $\lim_{x\to a^-}f(x)=2$ and $\lim_{x\to a^+}f(x)=3$, then $\lim_{x\to a}f(x)$ <span class="marks">[1]</span>
    (a) is 2 (b) is 3 (c) is 2.5 (d) does not exist
12. As the number of sides increases, the perimeter of a regular polygon inscribed in a circle of radius 7 cm approaches (take $\pi=\frac{22}{7}$) <span class="marks">[1]</span>
    (a) 44 cm (b) 154 cm (c) 42 cm (d) 49 cm

::: note Answers to 20.4
**1.** (b) — the terms are $1+1$, $1+0.5$, $1+0.25$, …; the extra part halves towards 0.
**2.** (b) — $\frac{5}{n}$ shrinks without end.
**3.** (b) — $\frac{n+1}{n}=1+\frac{1}{n}\rightarrow1$.
**4.** (b) — the part still missing after $n$ terms is $\frac{1}{2^n}\rightarrow0$.
**5.** (a) — substitute: $6-1=5$.
**6.** (c) — substitute: $0+4=4$.
**7.** (c) — $\frac{(x-2)(x+2)}{x-2}=x+2\rightarrow4$.
**8.** (c) — $\frac{(x-1)(x+1)}{x-1}=x+1\rightarrow2$.
**9.** (d) — $\frac{0}{0}$ has no value, although the limit is 6.
**10.** (b) — the minus sign means "from the left", through smaller values.
**11.** (d) — the two sides disagree, so there is no single limit.
**12.** (a) — the polygons tend to the circle: $2\pi r=2\times\frac{22}{7}\times7=44$ cm.
:::

## 20.5 Matrix

**Facts.** A matrix with $m$ rows and $n$ columns has order $m\times n$ and $mn$ elements; $a_{ij}$ is in row $i$, column $j$. In this bank a matrix written $[(a,b),(c,d)]$ has first row $a, b$ and second row $c, d$. Row, column, zero, rectangular and square matrices are named by shape; diagonal, scalar, unit, symmetric ($a_{ij}=a_{ji}$) and triangular matrices are square. Equal matrices have the same order and equal corresponding elements. Only matrices of the same order can be added or subtracted; $kA$ multiplies every element by $k$.

1. A matrix of order $2\times3$ has <span class="marks">[1]</span>
   (a) 2 columns (b) 3 rows (c) 6 elements (d) 5 elements
2. In the matrix $[(5,2,7),(1,9,4)]$, the element $a_{21}$ is <span class="marks">[1]</span>
   (a) 2 (b) 1 (c) 9 (d) 7
3. A matrix with only one column is a <span class="marks">[1]</span>
   (a) row matrix (b) column matrix (c) square matrix (d) unit matrix
4. The matrix $[(3,0),(0,3)]$ is a <span class="marks">[1]</span>
   (a) unit matrix (b) scalar matrix (c) row matrix (d) zero matrix
5. A square matrix with $a_{ij}=a_{ji}$ for all $i$ and $j$ is <span class="marks">[1]</span>
   (a) diagonal (b) symmetric (c) triangular (d) zero
6. The unit matrix of order 2 is <span class="marks">[1]</span>
   (a) $[(1,1),(1,1)]$ (b) $[(1,0),(0,1)]$ (c) $[(0,1),(1,0)]$ (d) $[(0,0),(0,0)]$
7. If $[(x,3),(4,y)]=[(2,3),(4,5)]$, then $x+y$ is <span class="marks">[1]</span>
   (a) 5 (b) 7 (c) 9 (d) 10
8. Two matrices can be added only when they have <span class="marks">[1]</span>
   (a) the same number of rows (b) the same order (c) the same first element (d) a zero element
9. $[(1,2),(3,4)]+[(4,3),(2,1)]$ equals <span class="marks">[1]</span>
   (a) $[(5,5),(5,5)]$ (b) $[(4,6),(6,4)]$ (c) $[(3,1),(-1,-3)]$ (d) $[(5,5),(5,6)]$
10. $[(5,6),(7,8)]-[(1,2),(3,4)]$ equals <span class="marks">[1]</span>
    (a) $[(4,4),(4,4)]$ (b) $[(6,8),(10,12)]$ (c) $[(4,3),(2,1)]$ (d) $[(5,4),(4,4)]$
11. If $A=[(2,-1),(3,0)]$, then $-2A$ is <span class="marks">[1]</span>
    (a) $[(-4,2),(-6,0)]$ (b) $[(4,-2),(6,0)]$ (c) $[(-4,-2),(-6,0)]$ (d) $[(0,-3),(1,-2)]$
12. For matrices of the same order, $A+B=B+A$ is the <span class="marks">[1]</span>
    (a) associative property (b) commutative property (c) identity property (d) inverse property

::: note Answers to 20.5
**1.** (c) — 2 rows and 3 columns make $2\times3=6$ elements.
**2.** (b) — row 2, column 1.
**3.** (b) — by definition.
**4.** (b) — diagonal with equal diagonal elements; it would be the unit matrix only if they were 1.
**5.** (b) — the leading diagonal acts as a mirror.
**6.** (b) — 1s on the leading diagonal, 0s elsewhere.
**7.** (b) — $x=2$ and $y=5$.
**8.** (b) — only then do the elements have matching positions.
**9.** (a) — every pair of matching elements adds to 5.
**10.** (a) — every difference is 4.
**11.** (a) — multiply every element by $-2$; $-2\times-1=2$.
**12.** (b) — the order of adding does not matter.
:::

## 20.6 Coordinate Geometry

**Facts.** Distance $=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$; from the origin $\sqrt{x^2+y^2}$. Internal division in the ratio $m_1:m_2$: $\left(\frac{m_1x_2+m_2x_1}{m_1+m_2},\frac{m_1y_2+m_2y_1}{m_1+m_2}\right)$; mid-point $\left(\frac{x_1+x_2}{2},\frac{y_1+y_2}{2}\right)$. Slope $m=\frac{y_2-y_1}{x_2-x_1}$; horizontal lines have slope 0 and vertical lines no slope; $y=mx+c$ has slope $m$ and $y$-intercept $c$. Area of a triangle $=\frac{1}{2}\left|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right|$; zero area means collinear.

1. The distance between $(1,2)$ and $(4,6)$ is <span class="marks">[1]</span>
   (a) 5 (b) 7 (c) 25 (d) $\sqrt{7}$
2. The distance of $(-5,12)$ from the origin is <span class="marks">[1]</span>
   (a) 7 (b) 13 (c) 17 (d) 169
3. The mid-point of $(-2,5)$ and $(6,-1)$ is <span class="marks">[1]</span>
   (a) $(2,2)$ (b) $(4,4)$ (c) $(-4,3)$ (d) $(2,3)$
4. The point dividing the join of $(2,1)$ and $(8,4)$ internally in the ratio $2:1$ is <span class="marks">[1]</span>
   (a) $(6,3)$ (b) $(4,2)$ (c) $(5,2.5)$ (d) $(10,5)$
5. If $(3,4)$ is the mid-point of $(1,2)$ and $(x,y)$, then $(x,y)$ is <span class="marks">[1]</span>
   (a) $(5,6)$ (b) $(2,3)$ (c) $(4,6)$ (d) $(7,8)$
6. The slope of the line joining $(-1,3)$ and $(2,9)$ is <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) $\frac{1}{2}$ (d) 6
7. The slope of a line parallel to the $y$-axis is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) not defined (d) $-1$
8. The equation of the $x$-axis is <span class="marks">[1]</span>
   (a) $x=0$ (b) $y=0$ (c) $y=x$ (d) $x+y=0$
9. The line $y=3x-2$ cuts the $y$-axis at <span class="marks">[1]</span>
   (a) $(0,3)$ (b) $(0,-2)$ (c) $(-2,0)$ (d) $(3,0)$
10. The slope of the line $4x-2y=5$ is <span class="marks">[1]</span>
    (a) 4 (b) $-2$ (c) 2 (d) $-4$
11. The area of the triangle with vertices $(0,0)$, $(6,0)$ and $(0,4)$ is <span class="marks">[1]</span>
    (a) 24 (b) 12 (c) 10 (d) 6
12. The "triangle" with vertices $(1,1)$, $(2,2)$ and $(3,3)$ has area <span class="marks">[1]</span>
    (a) 0 (b) 1 (c) 3 (d) 6

::: note Answers to 20.6
**1.** (a) — $\sqrt{9+16}=5$.
**2.** (b) — $\sqrt{25+144}=13$.
**3.** (a) — $\left(\frac{-2+6}{2},\frac{5-1}{2}\right)$.
**4.** (a) — $\left(\frac{2(8)+1(2)}{3},\frac{2(4)+1(1)}{3}\right)=(6,3)$.
**5.** (a) — $x=2(3)-1=5$ and $y=2(4)-2=6$.
**6.** (a) — $\frac{9-3}{2+1}=2$.
**7.** (c) — its run is 0, and division by 0 is not defined.
**8.** (b) — every point on the $x$-axis has $y=0$.
**9.** (b) — put $x=0$: $y=-2$.
**10.** (c) — $y=2x-\frac{5}{2}$.
**11.** (b) — a right triangle with legs 6 and 4: $\frac{1}{2}\times6\times4$.
**12.** (a) — the points lie on the line $y=x$, so they are collinear.
:::

## 20.7 Trigonometry

**Facts.** Right angle $=90^\circ=100^g=\left(\frac{\pi}{2}\right)^c$; $1^g=100^c$; $\pi^c=180^\circ$; $\frac{D}{90}=\frac{G}{100}=\frac{2R}{\pi}$. $\sin\theta=\frac{p}{h}$, $\cos\theta=\frac{b}{h}$, $\tan\theta=\frac{p}{b}$, with reciprocals cosec, sec, cot. $\sin^2\theta+\cos^2\theta=1$, $1+\tan^2\theta=\sec^2\theta$, $1+\cot^2\theta=\mathrm{cosec}^2\theta$. $\sin30^\circ=\cos60^\circ=\frac{1}{2}$, $\tan45^\circ=1$, $\tan60^\circ=\sqrt{3}$. Signs: All, Sin, Tan, Cos. $\sin(-\theta)=-\sin\theta$, $\cos(-\theta)=\cos\theta$; $90^\circ\pm\theta$ changes the ratio to its partner, $180^\circ\pm\theta$ keeps it.

1. $60^\circ$ in grades is <span class="marks">[1]</span>
   (a) $54^g$ (b) $66\frac{2}{3}^g$ (c) $60^g$ (d) $75^g$
2. $90^g$ in degrees is <span class="marks">[1]</span>
   (a) $81^\circ$ (b) $100^\circ$ (c) $90^\circ$ (d) $99^\circ$
3. $\left(\frac{\pi}{6}\right)^c$ in degrees is <span class="marks">[1]</span>
   (a) $60^\circ$ (b) $30^\circ$ (c) $45^\circ$ (d) $15^\circ$
4. $1^g$ is equal to <span class="marks">[1]</span>
   (a) $60^c$ (b) $100^c$ (c) $90'$ (d) $100'$
5. If $\sin\theta=\frac{3}{5}$ and $\theta$ is acute, then $\cos\theta$ is <span class="marks">[1]</span>
   (a) $\frac{4}{5}$ (b) $\frac{3}{4}$ (c) $\frac{5}{4}$ (d) $\frac{5}{3}$
6. $\sec\theta$ is equal to <span class="marks">[1]</span>
   (a) $\frac{1}{\sin\theta}$ (b) $\frac{1}{\cos\theta}$ (c) $\frac{1}{\tan\theta}$ (d) $\frac{\sin\theta}{\cos\theta}$
7. $1+\tan^2\theta$ is equal to <span class="marks">[1]</span>
   (a) $\sec^2\theta$ (b) $\mathrm{cosec}^2\theta$ (c) $\cos^2\theta$ (d) $\cot^2\theta$
8. $\cos60^\circ+\sin30^\circ$ is equal to <span class="marks">[1]</span>
   (a) 0 (b) $\frac{1}{2}$ (c) 1 (d) $\sqrt{3}$
9. $\tan30^\circ\times\tan60^\circ$ is equal to <span class="marks">[1]</span>
   (a) 1 (b) $\sqrt{3}$ (c) $\frac{1}{\sqrt{3}}$ (d) 3
10. $\sin150^\circ$ is equal to <span class="marks">[1]</span>
    (a) $-\frac{1}{2}$ (b) $\frac{1}{2}$ (c) $\frac{\sqrt{3}}{2}$ (d) $-\frac{\sqrt{3}}{2}$
11. $\cos(-\theta)$ is equal to <span class="marks">[1]</span>
    (a) $-\cos\theta$ (b) $\cos\theta$ (c) $\sin\theta$ (d) $-\sin\theta$
12. From a point $20\sqrt{3}$ m from the foot of a 20 m pole, the angle of elevation of the top is <span class="marks">[1]</span>
    (a) $30^\circ$ (b) $45^\circ$ (c) $60^\circ$ (d) $90^\circ$

::: note Answers to 20.7
**1.** (b) — $60\times\frac{10}{9}=66\frac{2}{3}$ grades.
**2.** (a) — $90\times\frac{9}{10}=81^\circ$.
**3.** (b) — $\frac{180^\circ}{6}=30^\circ$.
**4.** (b) — a grade has 100 centesimal minutes.
**5.** (a) — $p=3$, $h=5$, so $b=4$.
**6.** (b) — secant is the reciprocal of cosine.
**7.** (a) — divide $p^2+b^2=h^2$ by $b^2$.
**8.** (c) — $\frac{1}{2}+\frac{1}{2}=1$.
**9.** (a) — $\frac{1}{\sqrt{3}}\times\sqrt{3}=1$.
**10.** (b) — $\sin(180^\circ-30^\circ)=\sin30^\circ$, positive in quadrant II.
**11.** (b) — reflecting in the $x$-axis does not change $x$.
**12.** (a) — $\tan\theta=\frac{20}{20\sqrt{3}}=\frac{1}{\sqrt{3}}$.
:::

::: caution Degrees, grades and the decimal point
$60^\circ$ is not $60^g$: a grade is smaller than a degree, so the same angle has **more** grades ($66\frac{2}{3}^g$). Check the direction of every conversion this way: grades are always the bigger number, radians the smallest.
:::

## 20.8 Vector

**Facts.** A scalar has magnitude only; a vector has magnitude and direction. $\overrightarrow{AB}=\binom{x_2-x_1}{y_2-y_1}$ (head minus tail); $|\vec{a}|=\sqrt{x^2+y^2}$; direction $\tan\theta=\frac{y}{x}$. Unit vector $\hat{a}=\frac{\vec{a}}{|\vec{a}|}$; null vector $\binom{0}{0}$; $\overrightarrow{BA}=-\overrightarrow{AB}$. $k\vec{a}=\binom{kx}{ky}$; $\vec{a}\parallel\vec{b}$ when $x_1y_2-x_2y_1=0$ (like if $\vec{a}=k\vec{b}$ with $k>0$, unlike if $k<0$). $\vec{a}\pm\vec{b}$ by components; $\overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC}$.

1. Which of these is a scalar quantity? <span class="marks">[1]</span>
   (a) weight (b) displacement (c) mass (d) velocity
2. If $A$ is $(2,-1)$ and $B$ is $(5,3)$, then $\overrightarrow{AB}$ is <span class="marks">[1]</span>
   (a) $\binom{3}{4}$ (b) $\binom{7}{2}$ (c) $\binom{-3}{-4}$ (d) $\binom{3}{2}$
3. The magnitude of $\binom{-6}{8}$ is <span class="marks">[1]</span>
   (a) 2 (b) 10 (c) 14 (d) 100
4. The vector $\binom{1}{1}$ makes with the positive $x$-axis an angle of <span class="marks">[1]</span>
   (a) $30^\circ$ (b) $45^\circ$ (c) $60^\circ$ (d) $90^\circ$
5. The unit vector in the direction of $\binom{0}{-5}$ is <span class="marks">[1]</span>
   (a) $\binom{0}{-1}$ (b) $\binom{0}{1}$ (c) $\binom{0}{-5}$ (d) $\binom{1}{0}$
6. The magnitude of the null vector is <span class="marks">[1]</span>
   (a) 1 (b) 0 (c) not defined (d) any number
7. $\overrightarrow{BA}$ is equal to <span class="marks">[1]</span>
   (a) $\overrightarrow{AB}$ (b) $-\overrightarrow{AB}$ (c) $2\overrightarrow{AB}$ (d) $\vec{0}$
8. The vectors $\binom{2}{6}$ and $\binom{1}{3}$ are <span class="marks">[1]</span>
   (a) unlike vectors (b) like vectors (c) unit vectors (d) null vectors
9. If $\vec{a}=\binom{4}{-2}$, then $\frac{1}{2}\vec{a}$ is <span class="marks">[1]</span>
   (a) $\binom{2}{-1}$ (b) $\binom{8}{-4}$ (c) $\binom{4}{-1}$ (d) $\binom{2}{-2}$
10. $\binom{k}{2}$ is parallel to $\binom{6}{4}$ when $k$ is <span class="marks">[1]</span>
    (a) 2 (b) 3 (c) 4 (d) 12
11. $\binom{3}{-1}-\binom{1}{2}$ is equal to <span class="marks">[1]</span>
    (a) $\binom{2}{-3}$ (b) $\binom{4}{1}$ (c) $\binom{2}{1}$ (d) $\binom{-2}{3}$
12. By the triangle law, $\overrightarrow{PQ}+\overrightarrow{QR}$ is equal to <span class="marks">[1]</span>
    (a) $\overrightarrow{PR}$ (b) $\overrightarrow{RP}$ (c) $\overrightarrow{QP}$ (d) $\vec{0}$

::: note Answers to 20.8
**1.** (c) — mass has no direction; weight is a force and acts downwards.
**2.** (a) — $\binom{5-2}{3+1}$.
**3.** (b) — $\sqrt{36+64}=10$.
**4.** (b) — $\tan\theta=1$ in quadrant I.
**5.** (a) — divide by the magnitude 5.
**6.** (b) — both components are 0.
**7.** (b) — same length, opposite direction.
**8.** (b) — $\binom{2}{6}=2\binom{1}{3}$ with a positive scalar.
**9.** (a) — halve each component.
**10.** (b) — $4k-6\times2=0$ gives $k=3$.
**11.** (a) — $\binom{3-1}{-1-2}$.
**12.** (a) — from the first tail to the last head.
:::

## 20.9 Transformation

**Facts.** Reflection, rotation and translation are isometric (congruent image); enlargement is not. Reflection in the $x$-axis: $(x,y)\rightarrow(x,-y)$; in the $y$-axis: $(x,y)\rightarrow(-x,y)$. Rotation about $O$: $+90^\circ\rightarrow(-y,x)$, $180^\circ\rightarrow(-x,-y)$, $+270^\circ=-90^\circ\rightarrow(y,-x)$, $360^\circ\rightarrow(x,y)$. Translation by $\binom{a}{b}$: $(x,y)\rightarrow(x+a,y+b)$; its inverse is the translation by $\binom{-a}{-b}$. Points on the mirror line do not move.

1. Which transformation changes the size of a figure? <span class="marks">[1]</span>
   (a) reflection (b) translation (c) rotation (d) enlargement
2. The image of $(-4,-1)$ after reflection in the $x$-axis is <span class="marks">[1]</span>
   (a) $(-4,1)$ (b) $(4,-1)$ (c) $(4,1)$ (d) $(-1,-4)$
3. The image of $(6,-2)$ after reflection in the $y$-axis is <span class="marks">[1]</span>
   (a) $(-6,-2)$ (b) $(6,2)$ (c) $(-6,2)$ (d) $(-2,6)$
4. Under reflection in the $y$-axis, the point $(0,5)$ goes to <span class="marks">[1]</span>
   (a) $(0,-5)$ (b) $(0,5)$ (c) $(5,0)$ (d) $(-5,0)$
5. Rotation through $+90^\circ$ about $O$ sends $(3,1)$ to <span class="marks">[1]</span>
   (a) $(-1,3)$ (b) $(1,-3)$ (c) $(-3,-1)$ (d) $(1,3)$
6. Rotation through $-90^\circ$ about $O$ sends $(3,1)$ to <span class="marks">[1]</span>
   (a) $(-1,3)$ (b) $(1,-3)$ (c) $(-3,-1)$ (d) $(3,-1)$
7. Rotation through $180^\circ$ about $O$ sends $(-2,7)$ to <span class="marks">[1]</span>
   (a) $(2,-7)$ (b) $(-7,2)$ (c) $(2,7)$ (d) $(-2,-7)$
8. A rotation about $O$ sends $(2,3)$ to $(-3,2)$. The rotation is <span class="marks">[1]</span>
   (a) $+90^\circ$ (b) $-90^\circ$ (c) $180^\circ$ (d) $360^\circ$
9. Translation by $\binom{-3}{4}$ sends $(5,-1)$ to <span class="marks">[1]</span>
   (a) $(2,3)$ (b) $(8,-5)$ (c) $(2,-5)$ (d) $(-15,-4)$
10. The translation vector that sends $(1,1)$ to $(4,-2)$ is <span class="marks">[1]</span>
    (a) $\binom{3}{-3}$ (b) $\binom{5}{-1}$ (c) $\binom{-3}{3}$ (d) $\binom{3}{3}$
11. Rotation through $270^\circ$ anticlockwise about $O$ sends $(x,y)$ to <span class="marks">[1]</span>
    (a) $(-y,x)$ (b) $(y,-x)$ (c) $(-x,-y)$ (d) $(y,x)$
12. The translation that undoes the translation by $\binom{2}{-5}$ is the translation by <span class="marks">[1]</span>
    (a) $\binom{-2}{5}$ (b) $\binom{2}{5}$ (c) $\binom{5}{-2}$ (d) $\binom{-2}{-5}$

::: note Answers to 20.9
**1.** (d) — the others keep every length.
**2.** (a) — the sign of $y$ changes.
**3.** (a) — the sign of $x$ changes.
**4.** (b) — the point lies on the mirror line.
**5.** (a) — $(-y,x)=(-1,3)$, into quadrant II.
**6.** (b) — $(y,-x)=(1,-3)$, into quadrant IV.
**7.** (a) — both signs change.
**8.** (a) — $(-y,x)$ for $(2,3)$ is $(-3,2)$.
**9.** (a) — $(5-3,\ -1+4)$.
**10.** (a) — $\binom{4-1}{-2-1}$.
**11.** (b) — the same as a quarter turn clockwise.
**12.** (a) — the negative vector brings every point back.
:::

::: caution The two quarter-turn rules
Items 5 and 6 differ only in direction, and their answers differ only in where the minus sign goes. Before choosing, say which quadrant the image must be in: an anticlockwise quarter turn from quadrant I lands in quadrant II ($x$ negative), a clockwise one in quadrant IV ($y$ negative).
:::

## 20.10 Statistics

**Facts.** Mean: $\frac{\sum x}{n}$, $\frac{\sum fx}{N}$, or $\frac{\sum fm}{N}$ with mid-values $m$ for grouped data. Median: the $\left(\frac{n+1}{2}\right)$th item of the **ordered** data; $Q_1$ the $\left(\frac{n+1}{4}\right)$th and $Q_3$ the $\left(\frac{3(n+1)}{4}\right)$th item. Mode: the most frequent value; for grouped data $M_o=L+\frac{f_1-f_0}{2f_1-f_0-f_2}\times i$ in the modal class. Range $=L-S$; coefficient of range $=\frac{L-S}{L+S}$.

1. The mean of 7, 9, 11, 13 is <span class="marks">[1]</span>
   (a) 9 (b) 10 (c) 11 (d) 40
2. If the mean of 6 numbers is 15, their sum is <span class="marks">[1]</span>
   (a) 21 (b) 90 (c) 2.5 (d) 9
3. The mean of the distribution $x$: 1, 2, 3 with $f$: 2, 3, 5 is <span class="marks">[1]</span>
   (a) 2 (b) 2.3 (c) 2.5 (d) 3
4. The mid-value of the class 30–40 is <span class="marks">[1]</span>
   (a) 30 (b) 35 (c) 40 (d) 70
5. The median of 8, 3, 6, 1, 9 is <span class="marks">[1]</span>
   (a) 3 (b) 6 (c) 5.4 (d) 9
6. The median of 4, 6, 9, 13, 15, 20 is <span class="marks">[1]</span>
   (a) 9 (b) 13 (c) 11 (d) 11.17
7. For 15 values in ascending order, $Q_1$ is the <span class="marks">[1]</span>
   (a) 3rd value (b) 4th value (c) 8th value (d) 12th value
8. For 15 values in ascending order, $Q_3$ is the <span class="marks">[1]</span>
   (a) 10th value (b) 11th value (c) 12th value (d) 13th value
9. The mode of 3, 5, 5, 6, 8, 8, 8, 10 is <span class="marks">[1]</span>
   (a) 5 (b) 6 (c) 8 (d) 10
10. For the classes 0–10: 5, 10–20: 9, 20–30: 6, the modal class is <span class="marks">[1]</span>
    (a) 0–10 (b) 10–20 (c) 20–30 (d) 0–30
11. The range of 34, 12, 56, 23, 45 is <span class="marks">[1]</span>
    (a) 44 (b) 22 (c) 56 (d) 33
12. If the largest value is 60 and the smallest is 20, the coefficient of range is <span class="marks">[1]</span>
    (a) 40 (b) 0.5 (c) 2 (d) 0.33

::: note Answers to 20.10
**1.** (b) — $\frac{40}{4}=10$.
**2.** (b) — $6\times15=90$.
**3.** (b) — $\sum fx=2+6+15=23$ and $N=10$.
**4.** (b) — $\frac{30+40}{2}$.
**5.** (b) — in order 1, 3, 6, 8, 9; the 3rd value is 6.
**6.** (c) — $\frac{9+13}{2}=11$.
**7.** (b) — $\frac{15+1}{4}=4$.
**8.** (c) — $\frac{3(15+1)}{4}=12$.
**9.** (c) — 8 occurs three times.
**10.** (b) — it has the highest frequency, 9.
**11.** (a) — $56-12=44$.
**12.** (b) — $\frac{40}{80}=0.5$.
:::

::: tip Before you leave this chapter
One hundred and twenty items, ten facts lines. Copy the ten facts lines onto one sheet: the rules for transformations, the standard trigonometric values, the conversion between degrees, grades and radians, the distance and section formulas, and the averages. In the last week before the paper that sheet replaces this chapter.
:::

## Chapter summary

- **Relations and functions:** $n(A\times B)=n(A)n(B)$; a function gives each member of the domain exactly one image; $R^{-1}$ swaps every pair.
- **Polynomials and sequences:** whole-number powers only; degree of a product $=$ sum of degrees; $t_n=a+(n-1)d$; number of terms in $\sum_{k=p}^{q}$ is $q-p+1$.
- **Limit:** substitute for polynomials; factorise and cancel a $\frac{0}{0}$ form; no limit when the two sides disagree.
- **Matrix:** order is rows $\times$ columns; add and subtract only the same order; $kA$ multiplies every element.
- **Coordinate geometry:** distance, section and mid-point formulas; slope $\frac{y_2-y_1}{x_2-x_1}$; $y=mx+c$; area $\frac{1}{2}|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)|$.
- **Trigonometry:** $90^\circ=100^g=\frac{\pi}{2}$ rad; the three identities; standard values; ASTC; allied-angle rules.
- **Vector and transformation:** head minus tail; parallel when $x_1y_2-x_2y_1=0$; $(x,-y)$, $(-x,y)$, $(-y,x)$, $(-x,-y)$, $(y,-x)$, $(x+a,y+b)$.
- **Statistics:** order the data before finding a median or quartile; divide by $N=\sum f$; range $L-S$ and coefficient $\frac{L-S}{L+S}$.

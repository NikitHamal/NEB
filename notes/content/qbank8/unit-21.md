---
subject: Question Bank
grade: 8
unit: 21
title: "Optional Mathematics: Unit-wise Subjective Question Bank"
hours: 0
area: Optional Mathematics
---

Group A is ten single marks. The other **40 marks** of the Optional Mathematics paper come from Group B (ten 2-mark questions) and Group C (five 4-mark questions), and here marks are won by **method**, not by recall. A 2-mark answer needs two visible steps; a 4-mark answer needs a figure or a table where one helps, the formula, the substitution, the working and a checked answer. This chapter takes the ten units of the Optional Mathematics 8 book in order. Each unit opens with a **model question** worked the way a marker wants to see it, followed by four 2-mark and three 4-mark questions with complete solutions.

::: key How to use this bank
Read the model question first. Then cover the solutions and write the seven questions out in full, on paper, against the clock: about **4 minutes** for a 2-mark question and **10 minutes** for a 4-mark question. Mark yourself **step by step**, not just by the final answer. In the real paper a correct method with one arithmetic slip still earns most of the marks, while a bare answer with no working may earn none.
:::

::: caution Practice items, not past questions
Every question below is an original **practice** item written for the 50-mark school paper and the chapters of the Optional Mathematics 8 book. None is claimed to have appeared in any school's paper. All numerical answers were worked out independently, and most solutions end with the check that proves them.
:::

```figure caption="Groups B and C carry 20 marks each, but a long question needs more time per mark than a short one. A sensible plan gives about 40 minutes to Group B and 50 minutes to Group C."
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
groups = ['B (10 × 2)', 'C (5 × 4)']
ax1.bar(groups, [20, 20], color=[ACCENT, SERIES[1]], width=0.55)
ax1.set_title('marks (of 50)', fontsize=8.5)
ax2.bar(groups, [40, 50], color=[ACCENT, SERIES[1]], width=0.55)
ax2.set_title('minutes (of 120)', fontsize=8.5)
for ax, vals in ((ax1, [20, 20]), (ax2, [40, 50])):
    for i, v in enumerate(vals):
        ax.text(i, v + 0.8, str(v), ha='center', fontsize=8.5)
    ax.set_ylim(0, max(vals)*1.25)
    ax.tick_params(labelsize=8, length=0)
    ax.spines[['top', 'right']].set_visible(False)
    ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
fig.tight_layout(pad=0.4)
```

## 21.1 Relation and Function

::: example Model question: a function and its inverse relation
**Problem.** Let $A=\{1,2,3,4\}$, $B=\{2,4,6,8,10\}$ and $f: A\rightarrow B$ be defined by $f(x)=2x$. (i) Write $f$ as a set of ordered pairs and show it in an arrow diagram. (ii) Write its domain, co-domain and range. (iii) Write the inverse relation $f^{-1}$. Is $f^{-1}$ a function from $B$ to $A$? Give a reason.

**Solution.** (i) $f(1)=2$, $f(2)=4$, $f(3)=6$, $f(4)=8$, so $f=\{(1,2),(2,4),(3,6),(4,8)\}$. In the arrow diagram, 1, 2, 3, 4 in the first oval send one arrow each to 2, 4, 6, 8; the member 10 of $B$ receives no arrow.

(ii) Domain $=A=\{1,2,3,4\}$; co-domain $=B=\{2,4,6,8,10\}$; range $=\{2,4,6,8\}$.

(iii) $f^{-1}=\{(2,1),(4,2),(6,3),(8,4)\}$. As a relation from $B$ to $A$ it is **not** a function, because the member 10 of $B$ has no image. (It would be a function from the range $\{2,4,6,8\}$ to $A$.)

**Check.** Every member of $A$ has exactly one image, so $f$ itself is a function ✓.
:::

1. Find $x$ and $y$ if $\left(\frac{x}{2}+1,\ y-2\right)=(3,\ x)$. <span class="marks">[2]</span>
2. If $P=\{a,b,c\}$ and $Q=\{0,1\}$, find $Q\times P$ and $n(P\times Q)$. <span class="marks">[2]</span>
3. On $A=\{1,2,3,6\}$, list the relation $R=\{(x,y): x \text{ is a factor of } y \text{ and } x\neq y\}$ and write its domain and range. <span class="marks">[2]</span>
4. If $f(x)=x^2-4x+3$, find the pre-images of 0 and of 3. <span class="marks">[2]</span>
5. A function $f$ from $A=\{-1,0,1,2\}$ to $B=\{0,1,2,3,4,5\}$ is defined by $f(x)=x^2+1$. (i) Write $f$ as ordered pairs. (ii) Find the range. (iii) Draw the arrow diagram. (iv) Is $f$ one-to-one? Give a reason. <span class="marks">[4]</span>
6. A function is defined by $f(x)=ax+b$. If $f(2)=7$ and $f(-1)=-2$, find $a$ and $b$, then find $f(5)$ and the pre-image of 19. <span class="marks">[4]</span>
7. State, with reasons, which of these are functions: $R_1=\{(1,1),(2,4),(3,9)\}$; $R_2=\{(4,2),(4,-2),(9,3)\}$; $R_3=\{(x,y): y=3\}$ on $\{1,2,3\}$; the circle $x^2+y^2=4$. Use the vertical line test where it helps. <span class="marks">[4]</span>

::: note Solutions to 21.1
**1.** First components: $\frac{x}{2}+1=3$, so $x=4$. Second components: $y-2=x=4$, so $y=6$.
**2.** $Q\times P=\{(0,a),(0,b),(0,c),(1,a),(1,b),(1,c)\}$ and $n(P\times Q)=3\times2=6$.
**3.** $R=\{(1,2),(1,3),(1,6),(2,6),(3,6)\}$. Domain $=\{1,2,3\}$; range $=\{2,3,6\}$.
**4.** Pre-images of 0: $x^2-4x+3=0$, $(x-1)(x-3)=0$, so $x=1$ or 3. Pre-images of 3: $x^2-4x=0$, $x(x-4)=0$, so $x=0$ or 4.
**5.** (i) $f=\{(-1,2),(0,1),(1,2),(2,5)\}$. (ii) Range $=\{1,2,5\}$. (iii) Arrows $-1\rightarrow2$, $0\rightarrow1$, $1\rightarrow2$, $2\rightarrow5$; the members 0, 3 and 4 of $B$ receive none. (iv) It is **not** one-to-one, because $-1$ and $1$ have the same image 2. It is still a function (many-to-one).
**6.** $2a+b=7$ and $-a+b=-2$. Subtracting, $3a=9$, so $a=3$ and $b=1$: $f(x)=3x+1$. Then $f(5)=16$, and $3x+1=19$ gives the pre-image $x=6$. Check: $f(2)=7$ ✓, $f(-1)=-2$ ✓.
**7.** $R_1$: a function, each first component appears once. $R_2$: not a function, 4 has two images, 2 and $-2$. $R_3=\{(1,3),(2,3),(3,3)\}$: a function (constant), each input has the one image 3. The circle: not a function, the vertical line $x=0$ meets it at $(0,2)$ and $(0,-2)$.
:::

## 21.2 Polynomials

::: example Model question: sum, difference and product
**Problem.** If $f(x)=2x^3-x+3$ and $g(x)=x^2-2x+1$, find $f(x)+g(x)$, $f(x)-g(x)$ and $f(x)\cdot g(x)$. State the degree of each result and check the product at $x=2$.

**Solution.**
$$ f+g=2x^3+x^2-3x+4 \quad(\text{degree }3),\qquad f-g=2x^3-x^2+x+2 \quad(\text{degree }3) $$
For the product, multiply each term of $f$ by each term of $g$:
$$ (2x^3-x+3)(x^2-2x+1)=2x^5-4x^4+2x^3-x^3+2x^2-x+3x^2-6x+3 $$
$$ =2x^5-4x^4+x^3+5x^2-7x+3 \quad(\text{degree }3+2=5) $$
**Check at $x=2$.** $f(2)=16-2+3=17$ and $g(2)=4-4+1=1$, so $f(2)g(2)=17$. The product gives $64-64+8+20-14+3=17$ ✓.
:::

1. Write the degree, the leading coefficient and the constant term of $3x^2-5+2x^4-x$. <span class="marks">[2]</span>
2. Find $a$ and $b$ if $(a-1)x^2+2x+3=4x^2+(b+1)x+3$. <span class="marks">[2]</span>
3. Subtract $2x^3-3x^2+4$ from $x^3+x^2-2x+1$. <span class="marks">[2]</span>
4. Multiply $(x+2)(x^2-3x+1)$. <span class="marks">[2]</span>
5. If $p(x)=x^3+2x^2-x$, $q(x)=2x^2-3x+4$ and $r(x)=x^3-5$, find $p(x)-q(x)+r(x)$ and its value at $x=-1$. <span class="marks">[4]</span>
6. Find the product $(2x^2-x+3)(x^2+2x-1)$, state its degree, and check it at $x=1$. <span class="marks">[4]</span>
7. A rectangle is $(3x-1)$ cm long and $(x+4)$ cm wide. (i) Find its area. (ii) Find its perimeter. (iii) Find both when $x=5$, and check with the actual sides. <span class="marks">[4]</span>

::: note Solutions to 21.2
**1.** In standard form $2x^4+3x^2-x-5$: degree 4, leading coefficient 2, constant term $-5$.
**2.** $x^2$: $a-1=4$, so $a=5$. $x$: $2=b+1$, so $b=1$.
**3.** $(x^3+x^2-2x+1)-(2x^3-3x^2+4)=-x^3+4x^2-2x-3$.
**4.** $x^3-3x^2+x+2x^2-6x+2=x^3-x^2-5x+2$.
**5.** $x^3+2x^2-x-2x^2+3x-4+x^3-5=2x^3+2x-9$. At $x=-1$: $-2-2-9=-13$. Check: $p(-1)=2$, $q(-1)=9$, $r(-1)=-6$, and $2-9-6=-13$ ✓.
**6.** $2x^4+4x^3-2x^2-x^3-2x^2+x+3x^2+6x-3=2x^4+3x^3-x^2+7x-3$; degree 4. At $x=1$: $(2-1+3)(1+2-1)=4\times2=8$, and $2+3-1+7-3=8$ ✓.
**7.** (i) $(3x-1)(x+4)=3x^2+11x-4$ cm². (ii) $2[(3x-1)+(x+4)]=8x+6$ cm. (iii) At $x=5$: area $=75+55-4=126$ cm², perimeter $=46$ cm. The sides are 14 cm and 9 cm: $14\times9=126$ ✓ and $2(14+9)=46$ ✓.
:::

## 21.3 Sequence and Series

::: example Model question: from terms to a sum
**Problem.** The first four terms of a sequence are 4, 9, 16, 25. (i) Find the general term. (ii) Find the 12th term. (iii) Is 225 a term? If so, which one? (iv) Write the sum of the first five terms in sigma notation and find it.

**Solution.** (i) The terms are $2^2, 3^2, 4^2, 5^2$, so $t_n=(n+1)^2$.

(ii) $t_{12}=13^2=169$.

(iii) $(n+1)^2=225=15^2$ gives $n+1=15$, so $n=14$: 225 is the **14th term**.

(iv) $\sum_{k=1}^{5}(k+1)^2=4+9+16+25+36=90$.

**Check.** $t_1=(1+1)^2=4$ ✓ and $t_4=25$ ✓.
:::

1. Write the first four terms of the sequence with $t_n=\frac{2n-1}{n+1}$. <span class="marks">[2]</span>
2. Find the general term and the 15th term of $2, 6, 10, 14, \ldots$. <span class="marks">[2]</span>
3. Is 101 a term of $5, 9, 13, \ldots$? If so, which term? <span class="marks">[2]</span>
4. Find the value of $\sum_{r=1}^{5}(r^2+1)$. <span class="marks">[2]</span>
5. Triangles in a row are made of matchsticks: 1 triangle needs 3 sticks, 2 triangles 5 sticks, 3 triangles 7 sticks. (i) Find the general term. (ii) How many sticks make 20 triangles? (iii) How many triangles can be made with 61 sticks? (iv) Write the total sticks for the first five patterns in sigma notation and find it. <span class="marks">[4]</span>
6. Find the general term of $0, 3, 8, 15, 24, \ldots$ by the method of differences, find the 10th term, and evaluate the sum of the first four terms written in sigma notation. <span class="marks">[4]</span>
7. Using $\sum_{k=1}^{n}k=\frac{n(n+1)}{2}$, find (i) $\sum_{k=1}^{30}k$ (ii) $\sum_{k=1}^{12}(2k+3)$ (iii) the sum of all the multiples of 4 from 4 to 100. <span class="marks">[4]</span>

::: note Solutions to 21.3
**1.** $t_1=\frac{1}{2}$, $t_2=\frac{3}{3}=1$, $t_3=\frac{5}{4}$, $t_4=\frac{7}{5}$.
**2.** The difference is 4 and each term is 2 less than $4n$: $t_n=4n-2$, so $t_{15}=58$.
**3.** $t_n=4n+1$. Setting $4n+1=101$ gives $n=25$, a natural number, so 101 is the **25th term**.
**4.** $2+5+10+17+26=60$.
**5.** (i) The difference is 2 and each term is 1 more than $2n$: $t_n=2n+1$. (ii) $t_{20}=41$ sticks. (iii) $2n+1=61$ gives $n=30$ triangles. (iv) $\sum_{k=1}^{5}(2k+1)=3+5+7+9+11=35$ sticks.
**6.** First differences $3, 5, 7, 9$; second differences 2, so compare with $n^2$: the terms are each 1 less, so $t_n=n^2-1$. Then $t_{10}=99$, and $\sum_{k=1}^{4}(k^2-1)=0+3+8+15=26$.
**7.** (i) $\frac{30\times31}{2}=465$. (ii) $2\sum_{k=1}^{12}k+\sum_{k=1}^{12}3=2\times78+36=192$. (iii) $4+8+\cdots+100=4(1+2+\cdots+25)=4\times\frac{25\times26}{2}=4\times325=1300$.
:::

## 21.4 Limit

::: example Model question: value and limit
**Problem.** Let $f(x)=\frac{x^2+x-6}{x-2}$. (i) Show that $f(2)$ is not defined. (ii) Find $f(x)$ for $x=1.9$, 1.99, 2.01 and 2.1. (iii) Find $\lim_{x\to2}f(x)$ by factorising. (iv) Describe the graph of $f$.

**Solution.** (i) $f(2)=\frac{4+2-6}{0}=\frac{0}{0}$, which has no value.

(ii) $f(1.9)=4.9$, $f(1.99)=4.99$, $f(2.01)=5.01$, $f(2.1)=5.1$.

(iii) $x^2+x-6=(x+3)(x-2)$, so for $x\neq2$, $f(x)=x+3$ and $\lim_{x\to2}f(x)=2+3=5$.

(iv) The graph is the straight line $y=x+3$ with a hole at the point $(2,5)$.

**Check.** The table approaches 5 from both sides, as the algebra says ✓.
:::

1. Write the next three terms of $\frac{1}{3}, \frac{2}{4}, \frac{3}{5}, \frac{4}{6}, \ldots$ and state the limit of the sequence. <span class="marks">[2]</span>
2. Evaluate $\lim_{x\to-2}(3x^2-x+1)$. <span class="marks">[2]</span>
3. Evaluate $\lim_{x\to5}\frac{x^2-25}{x-5}$. <span class="marks">[2]</span>
4. Evaluate $\lim_{n\to\infty}\frac{4n-1}{n}$. <span class="marks">[2]</span>
5. Evaluate (i) $\lim_{x\to3}\frac{x^2-5x+6}{x-3}$ (ii) $\lim_{x\to-1}\frac{x^2-1}{x+1}$ (iii) $\lim_{x\to4}\frac{x^2-3x-4}{x-4}$. <span class="marks">[4]</span>
6. After $n$ steps of "shade half of what is left", the shaded fraction of a square is $1-\frac{1}{2^n}$. (i) Write the first five values. (ii) State the limit. (iii) Find the least $n$ for which the unshaded part is less than 0.001. <span class="marks">[4]</span>
7. A function is defined by $f(x)=2x+1$ for $x<2$ and $f(x)=7-x$ for $x\geq2$. (i) Find $f(2)$. (ii) Find what $f(x)$ approaches as $x\rightarrow2^-$ and as $x\rightarrow2^+$. (iii) Does $\lim_{x\to2}f(x)$ exist, and does it equal $f(2)$? <span class="marks">[4]</span>

::: note Solutions to 21.4
**1.** The $n$th term is $\frac{n}{n+2}$, so the next terms are $\frac{5}{7}$, $\frac{6}{8}=\frac{3}{4}$, $\frac{7}{9}$. Since $\frac{n}{n+2}=1-\frac{2}{n+2}$ and $\frac{2}{n+2}\rightarrow0$, the limit is 1.
**2.** Substitute: $3(4)+2+1=15$.
**3.** $\frac{(x-5)(x+5)}{x-5}=x+5\rightarrow10$.
**4.** $\frac{4n-1}{n}=4-\frac{1}{n}\rightarrow4$.
**5.** (i) $\frac{(x-2)(x-3)}{x-3}=x-2\rightarrow1$. (ii) $\frac{(x-1)(x+1)}{x+1}=x-1\rightarrow-2$. (iii) $\frac{(x-4)(x+1)}{x-4}=x+1\rightarrow5$.
**6.** (i) $\frac{1}{2}, \frac{3}{4}, \frac{7}{8}, \frac{15}{16}, \frac{31}{32}$. (ii) The unshaded part $\frac{1}{2^n}\rightarrow0$, so the limit is 1. (iii) $\frac{1}{2^n}<\frac{1}{1000}$ needs $2^n>1000$; $2^9=512$ is too small and $2^{10}=1024$ works, so $n=10$.
**7.** (i) $x=2$ uses the second rule: $f(2)=7-2=5$. (ii) From the left, $2x+1\rightarrow2(2)+1=5$; from the right, $7-x\rightarrow5$. (iii) Both sides approach 5, so the limit exists and equals 5, which is also $f(2)$: the graph has no break at $x=2$.
:::

## 21.5 Matrix

::: example Model question: combining matrices
**Problem.** Let $A=[(2,-1),(0,3)]$, $B=[(1,4),(-2,5)]$ and $C=[(3,0),(1,-1)]$. Find (i) $A+B-C$ (ii) $2A-3B$ (iii) the matrix $X$ such that $A+X=2B$.

**Solution.** (i) $A+B=[(3,3),(-2,8)]$, so $A+B-C=[(3-3,\ 3-0),(-2-1,\ 8+1)]=[(0,3),(-3,9)]$.

(ii) $2A=[(4,-2),(0,6)]$ and $3B=[(3,12),(-6,15)]$, so $2A-3B=[(1,-14),(6,-9)]$.

(iii) $X=2B-A=[(2,8),(-4,10)]-[(2,-1),(0,3)]=[(0,9),(-4,7)]$.

**Check (iii).** $A+X=[(2+0,\ -1+9),(0-4,\ 3+7)]=[(2,8),(-4,10)]=2B$ ✓.
:::

1. Construct the $3\times2$ matrix $A=[a_{ij}]$ with $a_{ij}=i-2j$. <span class="marks">[2]</span>
2. Find $x$, $y$ and $z$ if $[(x+y,\ 2),(z,\ x-y)]=[(6,\ 2),(5,\ 2)]$. <span class="marks">[2]</span>
3. If $[(a,\ 2b),(4,\ 1)]$ is symmetric and $a+b=5$, find $a$ and $b$. <span class="marks">[2]</span>
4. If $A=[(3,-2),(1,4)]$, find $3A-2I$, where $I$ is the unit matrix of order 2. <span class="marks">[2]</span>
5. If $A=[(1,-2),(3,0)]$ and $B=[(2,1),(-1,4)]$, verify that $3(A+B)=3A+3B$. <span class="marks">[4]</span>
6. Find the matrices $X$ and $Y$ if $X+Y=[(5,2),(0,9)]$ and $X-Y=[(3,6),(4,-1)]$. <span class="marks">[4]</span>
7. The marks of two students in three subjects are $F=[(65,72,80),(58,66,75)]$ in the first term and $S=[(70,68,85),(64,70,79)]$ in the second term (rows: students; columns: subjects). Find (i) the total marks $F+S$ (ii) the change $S-F$, explaining any negative entry (iii) the average marks $\frac{1}{2}(F+S)$. <span class="marks">[4]</span>

::: note Solutions to 21.5
**1.** $a_{11}=-1$, $a_{12}=-3$, $a_{21}=0$, $a_{22}=-2$, $a_{31}=1$, $a_{32}=-1$, so $A=[(-1,-3),(0,-2),(1,-1)]$.
**2.** $z=5$; $x+y=6$ and $x-y=2$ give $x=4$, $y=2$.
**3.** Symmetric means $a_{12}=a_{21}$: $2b=4$, so $b=2$ and $a=3$.
**4.** $3A=[(9,-6),(3,12)]$ and $2I=[(2,0),(0,2)]$, so $3A-2I=[(7,-6),(3,10)]$.
**5.** $A+B=[(3,-1),(2,4)]$, so $3(A+B)=[(9,-3),(6,12)]$. $3A=[(3,-6),(9,0)]$ and $3B=[(6,3),(-3,12)]$, so $3A+3B=[(9,-3),(6,12)]$. The two are equal.
**6.** Adding the equations, $2X=[(8,8),(4,8)]$, so $X=[(4,4),(2,4)]$. Then $Y=[(5,2),(0,9)]-X=[(1,-2),(-2,5)]$. Check: $X-Y=[(3,6),(4,-1)]$ ✓.
**7.** (i) $F+S=[(135,140,165),(122,136,154)]$. (ii) $S-F=[(5,-4,5),(6,4,4)]$: the first student scored 4 marks fewer in the second subject; every other mark rose. (iii) $\frac{1}{2}(F+S)=[(67.5,70,82.5),(61,68,77)]$.
:::

## 21.6 Coordinate Geometry

::: example Model question: an isosceles right-angled triangle
**Problem.** The vertices of a triangle are $A(1,1)$, $B(5,4)$ and $C(-2,5)$. (i) Show that it is an isosceles right-angled triangle. (ii) Find its area. (iii) Find the mid-point of its hypotenuse.

**Solution.** (i) $AB^2=4^2+3^2=25$, $AC^2=(-3)^2+4^2=25$, $BC^2=(-7)^2+1^2=50$. So $AB=AC=5$ (isosceles) and $AB^2+AC^2=50=BC^2$, so the angle at $A$ is a right angle.

(ii) Area $=\frac{1}{2}\times AB\times AC=\frac{1}{2}\times5\times5=12.5$ square units.

(iii) The hypotenuse is $BC$; its mid-point is $\left(\frac{5-2}{2},\frac{4+5}{2}\right)=(1.5,\ 4.5)$.

**Check (ii).** $\frac{1}{2}\left|1(4-5)+5(5-1)+(-2)(1-4)\right|=\frac{1}{2}\left|-1+20+6\right|=12.5$ ✓.
:::

1. Find the distance between $(-3,-2)$ and $(3,6)$. <span class="marks">[2]</span>
2. Find the point that divides the join of $(-4,6)$ and $(8,-3)$ internally in the ratio $1:2$. <span class="marks">[2]</span>
3. Find the slope and the $y$-intercept of $3x+5y=15$. <span class="marks">[2]</span>
4. Find the equation of the line of slope $-1$ through $(2,5)$. <span class="marks">[2]</span>
5. Find $k$ if $(1,2)$, $(3,k)$ and $(6,12)$ are collinear, (i) using slopes (ii) using area. <span class="marks">[4]</span>
6. Find the points that divide the join of $A(-3,-1)$ and $B(9,7)$ into four equal parts. <span class="marks">[4]</span>
7. Show that $P(-2,1)$, $Q(3,-1)$, $R(5,4)$ and $S(0,6)$ are the vertices of a square, and find its area in two ways. <span class="marks">[4]</span>

::: note Solutions to 21.6
**1.** $\sqrt{6^2+8^2}=\sqrt{100}=10$ units.
**2.** $\left(\frac{1(8)+2(-4)}{3},\ \frac{1(-3)+2(6)}{3}\right)=(0,3)$.
**3.** $5y=-3x+15$, so $y=-\frac{3}{5}x+3$: slope $-\frac{3}{5}$, $y$-intercept 3.
**4.** $y=-x+c$ through $(2,5)$: $5=-2+c$, so $c=7$ and the line is $y=-x+7$.
**5.** (i) The slope from $(1,2)$ to $(6,12)$ is $\frac{10}{5}=2$, so the slope from $(1,2)$ to $(3,k)$ must be 2: $\frac{k-2}{2}=2$, $k=6$. (ii) $\frac{1}{2}\left|1(k-12)+3(12-2)+6(2-k)\right|=\frac{1}{2}\left|30-5k\right|=0$ gives $k=6$ ✓.
**6.** The quarter points divide $AB$ in the ratios $1:3$, $1:1$ and $3:1$: $\left(\frac{9-9}{4},\frac{7-3}{4}\right)=(0,1)$; the mid-point $(3,3)$; $\left(\frac{27-3}{4},\frac{21-1}{4}\right)=(6,5)$.
**7.** $PQ^2=25+4=29$, $QR^2=4+25=29$, $RS^2=25+4=29$, $SP^2=4+25=29$: all sides equal. Diagonals: $PR^2=49+9=58$ and $QS^2=9+49=58$: equal. Four equal sides and equal diagonals make a square. Area (i) $=$ side$^2=29$ square units. (ii) Arrow method: $(-2)(-1)-3(1)=-1$; $3(4)-5(-1)=17$; $5(6)-0(4)=30$; $0(1)-(-2)(6)=12$; total 58, so the area is $\frac{58}{2}=29$ ✓.
:::

## 21.7 Trigonometry

::: example Model question: a tree broken by the wind
**Problem.** A tree is broken by a storm at a point 6 m above the ground. Its top touches the ground, and the broken part makes an angle of $30^\circ$ with the ground. Draw a figure and find (i) the length of the broken part (ii) the original height of the tree (iii) the distance from the foot of the tree to the point where the top touches the ground.

**Solution.** **Figure.** A vertical segment $AB=6$ m (the standing part), the broken part $BC$ reaching the ground at $C$, and the right angle at $A$; the angle at $C$ is $30^\circ$.

(i) $\sin30^\circ=\frac{AB}{BC}=\frac{6}{BC}$, so $BC=\frac{6}{\frac{1}{2}}=12$ m.

(ii) Original height $=AB+BC=6+12=18$ m.

(iii) $\tan30^\circ=\frac{6}{AC}$, so $AC=6\sqrt{3}\approx10.39$ m.

**Check.** $AC^2+AB^2=108+36=144=12^2=BC^2$ ✓.
:::

1. Convert $48^\circ36'$ into grades. <span class="marks">[2]</span>
2. Express $\left(\frac{7\pi}{10}\right)^c$ in degrees and in grades. <span class="marks">[2]</span>
3. If $\cos\theta=\frac{12}{13}$ and $\theta$ is acute, find $\tan\theta$ and $\mathrm{cosec}\,\theta$. <span class="marks">[2]</span>
4. Find the value of $\sin^245^\circ+\cos^230^\circ-\tan^260^\circ$. <span class="marks">[2]</span>
5. Prove that (i) $(1+\tan^2\theta)(1-\sin^2\theta)=1$ (ii) $\sec\theta-\cos\theta=\sin\theta\tan\theta$. <span class="marks">[4]</span>
6. Find the values of (i) $\sin240^\circ$ (ii) $\cos150^\circ$ (iii) $\tan(-45^\circ)$ (iv) $\sin(90^\circ+30^\circ)+\cos(180^\circ-60^\circ)$. <span class="marks">[4]</span>
7. From the top of a tower 30 m high, the angle of depression of a car on the road is $60^\circ$. Draw a figure and find (i) the distance of the car from the foot of the tower (ii) the distance from the top of the tower to the car. <span class="marks">[4]</span>

::: note Solutions to 21.7
**1.** $36'=\frac{36}{60}=0.6^\circ$, so the angle is $48.6^\circ$, and $48.6\times\frac{10}{9}=54^g$.
**2.** $\frac{7\times180^\circ}{10}=126^\circ$ and $\frac{7\times200^g}{10}=140^g$.
**3.** $b=12$, $h=13$, so $p=\sqrt{169-144}=5$. $\tan\theta=\frac{5}{12}$ and $\mathrm{cosec}\,\theta=\frac{13}{5}$.
**4.** $\frac{1}{2}+\frac{3}{4}-3=\frac{2+3-12}{4}=-\frac{7}{4}$.
**5.** (i) LHS $=\sec^2\theta\cdot\cos^2\theta=\frac{1}{\cos^2\theta}\cdot\cos^2\theta=1=$ RHS. (ii) LHS $=\frac{1}{\cos\theta}-\cos\theta=\frac{1-\cos^2\theta}{\cos\theta}=\frac{\sin^2\theta}{\cos\theta}=\sin\theta\cdot\frac{\sin\theta}{\cos\theta}=\sin\theta\tan\theta=$ RHS.
**6.** (i) $\sin(180^\circ+60^\circ)=-\sin60^\circ=-\frac{\sqrt{3}}{2}$. (ii) $\cos(180^\circ-30^\circ)=-\cos30^\circ=-\frac{\sqrt{3}}{2}$. (iii) $-\tan45^\circ=-1$. (iv) $\cos30^\circ-\cos60^\circ=\frac{\sqrt{3}}{2}-\frac{1}{2}=\frac{\sqrt{3}-1}{2}$.
**7.** **Figure:** the tower $AB=30$ m with the horizontal through the top $A$, the car $C$ on the ground, and the $60^\circ$ depression at $A$ equal to the elevation at $C$. (i) $\tan60^\circ=\frac{30}{BC}$, so $BC=\frac{30}{\sqrt{3}}=10\sqrt{3}\approx17.32$ m. (ii) $\sin60^\circ=\frac{30}{AC}$, so $AC=\frac{60}{\sqrt{3}}=20\sqrt{3}\approx34.64$ m.
:::

## 21.8 Vector

::: example Model question: a triangle described by vectors
**Problem.** The points are $P(1,2)$, $Q(4,6)$ and $R(8,3)$. (i) Find $\overrightarrow{PQ}$ and $\overrightarrow{QR}$ and their magnitudes. (ii) What kind of triangle is $PQR$? (iii) Verify that $\overrightarrow{PQ}+\overrightarrow{QR}=\overrightarrow{PR}$ and find $|\overrightarrow{PR}|$.

**Solution.** (i) $\overrightarrow{PQ}=\binom{3}{4}$ with $|\overrightarrow{PQ}|=5$; $\overrightarrow{QR}=\binom{4}{-3}$ with $|\overrightarrow{QR}|=5$.

(ii) Two sides are equal, so the triangle is isosceles.

(iii) $\overrightarrow{PR}=\binom{8-1}{3-2}=\binom{7}{1}$ and $\overrightarrow{PQ}+\overrightarrow{QR}=\binom{3+4}{4-3}=\binom{7}{1}$ ✓. $|\overrightarrow{PR}|=\sqrt{49+1}=\sqrt{50}=5\sqrt{2}$.

**Check.** $5^2+5^2=50=|\overrightarrow{PR}|^2$, so the triangle is also right-angled at $Q$.
:::

1. Find the magnitude and direction of $\binom{-3}{3}$. <span class="marks">[2]</span>
2. If $\vec{a}=\binom{2}{-3}$ and $\vec{b}=\binom{-1}{4}$, find $3\vec{a}+2\vec{b}$. <span class="marks">[2]</span>
3. Find $m$ if $\binom{m}{-6}$ and $\binom{2}{-3}$ are parallel. Are they like or unlike? <span class="marks">[2]</span>
4. Find the unit vector in the direction of $\binom{5}{12}$. <span class="marks">[2]</span>
5. If $\vec{a}=\binom{3}{4}$ and $\vec{b}=\binom{-2}{1}$, find $|\vec{a}|$, $|\vec{b}|$, $\vec{a}+\vec{b}$ and $|\vec{a}+\vec{b}|$, and show that $|\vec{a}+\vec{b}|<|\vec{a}|+|\vec{b}|$. <span class="marks">[4]</span>
6. A boat is rowed straight across a river at 4 km/h while the water flows downstream at 3 km/h. Taking downstream as the $x$-direction and across as the $y$-direction, write both velocities as vectors and find the resultant velocity, its magnitude and its direction with the bank. <span class="marks">[4]</span>
7. Show that $A(1,1)$, $B(5,3)$, $C(7,7)$ and $D(3,5)$ form a parallelogram, and verify that $\overrightarrow{AB}+\overrightarrow{AD}=\overrightarrow{AC}$. Is it also a rhombus? <span class="marks">[4]</span>

::: note Solutions to 21.8
**1.** Magnitude $\sqrt{9+9}=3\sqrt{2}$. $x<0$, $y>0$: quadrant II, with acute angle $45^\circ$, so the direction is $180^\circ-45^\circ=135^\circ$.
**2.** $\binom{6}{-9}+\binom{-2}{8}=\binom{4}{-1}$.
**3.** $\binom{m}{-6}=k\binom{2}{-3}$ needs $k=2$, so $m=4$. The scalar is positive, so they are **like** vectors.
**4.** $|\vec{a}|=13$, so $\hat{a}=\binom{\frac{5}{13}}{\frac{12}{13}}$.
**5.** $|\vec{a}|=5$, $|\vec{b}|=\sqrt{5}\approx2.24$, $\vec{a}+\vec{b}=\binom{1}{5}$, $|\vec{a}+\vec{b}|=\sqrt{26}\approx5.10$. Since $5.10<5+2.24=7.24$, the inequality holds: two sides of a triangle are together longer than the third.
**6.** Water $\binom{3}{0}$, rowing $\binom{0}{4}$; resultant $\binom{3}{4}$ km/h, magnitude 5 km/h, at an angle with $\tan\theta=\frac{4}{3}$ to the bank, $\theta\approx53.13^\circ$.
**7.** $\overrightarrow{AB}=\binom{4}{2}=\overrightarrow{DC}$ and $\overrightarrow{AD}=\binom{2}{4}=\overrightarrow{BC}$, so both pairs of opposite sides are equal and parallel: a parallelogram. $\overrightarrow{AB}+\overrightarrow{AD}=\binom{6}{6}=\overrightarrow{AC}$ ✓. Also $|\overrightarrow{AB}|=|\overrightarrow{AD}|=\sqrt{20}$, so all four sides are equal: it is a **rhombus**.
:::

## 21.9 Transformation

::: example Model question: one transformation after another
**Problem.** The triangle $A(1,2)$, $B(3,1)$, $C(2,4)$ is reflected in the $x$-axis to $A'B'C'$, and $A'B'C'$ is rotated through $+90^\circ$ about the origin to $A''B''C''$. Find both images and describe what happens to the coordinates of a general point.

**Solution.** Reflection in the $x$-axis, $(x,y)\rightarrow(x,-y)$: $A'(1,-2)$, $B'(3,-1)$, $C'(2,-4)$.

Rotation $+90^\circ$, $(x,y)\rightarrow(-y,x)$: $A''(2,1)$, $B''(1,3)$, $C''(4,2)$.

A general point goes $(x,y)\rightarrow(x,-y)\rightarrow(y,x)$: the two transformations together simply **swap the coordinates**. (This single transformation is the reflection in the line $y=x$, which you will meet in grade 9.)

**Check.** $AB=\sqrt{4+1}=\sqrt{5}$ and $A''B''=\sqrt{1+4}=\sqrt{5}$: lengths are kept, as two isometric steps must keep them ✓.
:::

1. Find the images of $P(-2,5)$ after reflection in the $x$-axis and after reflection in the $y$-axis. <span class="marks">[2]</span>
2. Find the images of $(5,-3)$ under rotation about the origin through $+90^\circ$ and through $180^\circ$. <span class="marks">[2]</span>
3. A translation sends $(3,-2)$ to $(-1,4)$. Find the translation vector and the image of the origin. <span class="marks">[2]</span>
4. For the point $(4,7)$, show that rotation through $180^\circ$ about $O$ gives the same image as reflection in the $x$-axis followed by reflection in the $y$-axis. <span class="marks">[2]</span>
5. The triangle $A(2,1)$, $B(4,1)$, $C(4,3)$ is rotated through $-90^\circ$ about the origin and the image is then translated by $\binom{-1}{2}$. Find the final image. <span class="marks">[4]</span>
6. Reflect the rectangle $P(1,1)$, $Q(4,1)$, $R(4,3)$, $S(1,3)$ in the $y$-axis. Plot both figures and compare their areas. <span class="marks">[4]</span>
7. A point $P$ is rotated through $+90^\circ$ about the origin to $P'(-3,5)$. (i) Find $P$. (ii) Find the image of $P$ under reflection in the $x$-axis. (iii) Find the translation vector that would send $P$ to $P'$. <span class="marks">[4]</span>

::: note Solutions to 21.9
**1.** In the $x$-axis: $(-2,-5)$. In the $y$-axis: $(2,5)$.
**2.** $+90^\circ$: $(-y,x)=(3,5)$. $180^\circ$: $(-5,3)$.
**3.** $\binom{-1-3}{4+2}=\binom{-4}{6}$; the origin goes to $(-4,6)$.
**4.** $180^\circ$: $(-4,-7)$. Reflections: $(4,7)\rightarrow(4,-7)\rightarrow(-4,-7)$. The same image.
**5.** $-90^\circ$, $(x,y)\rightarrow(y,-x)$: $A'(1,-2)$, $B'(1,-4)$, $C'(3,-4)$. Translating by $\binom{-1}{2}$: $A''(0,0)$, $B''(0,-2)$, $C''(2,-2)$.
**6.** Images: $P'(-1,1)$, $Q'(-4,1)$, $R'(-4,3)$, $S'(-1,3)$. Both are rectangles 3 units by 2 units, so both areas are 6 square units, as an isometric transformation requires.
**7.** (i) Undo the rotation with $-90^\circ$, $(x,y)\rightarrow(y,-x)$: $P=(5,3)$. Check: $(-3,5)$ is $(-y,x)$ for $(5,3)$ ✓. (ii) $(5,-3)$. (iii) $\overrightarrow{PP'}=\binom{-3-5}{5-3}=\binom{-8}{2}$.
:::

## 21.10 Statistics

::: example Model question: mean and mode of grouped data
**Problem.** The ages of 50 people at a health camp are given below. Find the mean age and the modal age.

| Age (years) | 0–20 | 20–40 | 40–60 | 60–80 | 80–100 |
|---|---|---|---|---|---|
| People | 8 | 14 | 18 | 7 | 3 |

**Solution.** Mid-values 10, 30, 50, 70, 90.

| Age | $f$ | $m$ | $fm$ |
|---|---|---|---|
| 0–20 | 8 | 10 | 80 |
| 20–40 | 14 | 30 | 420 |
| 40–60 | 18 | 50 | 900 |
| 60–80 | 7 | 70 | 490 |
| 80–100 | 3 | 90 | 270 |
| Total | 50 | | 2160 |

Mean $=\frac{2160}{50}=43.2$ years.

Modal class 40–60: $L=40$, $f_1=18$, $f_0=14$, $f_2=7$, $i=20$:
$$ M_o=40+\frac{18-14}{36-14-7}\times20=40+\frac{4}{15}\times20\approx40+5.33=45.33 \text{ years} $$
**Check.** The mode lies inside the modal class 40–60 and nearer to 40, the side of the larger neighbour (14 against 7) ✓.
:::

1. Find the mean of 18, 22, 25, 30 and 35. <span class="marks">[2]</span>
2. The mean of 8 numbers is 20. If the number 34 is removed, find the mean of the remaining numbers. <span class="marks">[2]</span>
3. Find the median of 41, 28, 35, 50, 33, 46, 38, 29. <span class="marks">[2]</span>
4. Find the range and the coefficient of range for the classes 20–30, 30–40, 40–50, 50–60. <span class="marks">[2]</span>
5. Find the first quartile, the median and the third quartile of 12, 15, 9, 20, 18, 25, 30, 14, 22, 27. <span class="marks">[4]</span>
6. For the distribution $x$: 2, 4, 6, 8, 10 with $f$: 3, 7, 12, 5, 3, find the mean, the median and the mode. <span class="marks">[4]</span>
7. The mean of the distribution $x$: 5, 10, 15, 20, 25 with $f$: 2, 4, $p$, 6, 3 is 16. Find $p$ and check your answer. <span class="marks">[4]</span>

::: note Solutions to 21.10
**1.** $\frac{18+22+25+30+35}{5}=\frac{130}{5}=26$.
**2.** The total was $8\times20=160$; without 34 it is 126, shared by 7 numbers: $\frac{126}{7}=18$.
**3.** In order: 28, 29, 33, 35, 38, 41, 46, 50 ($n=8$). Median $=4.5$th item $=\frac{35+38}{2}=36.5$.
**4.** $L=60$, $S=20$: range $=40$, coefficient $=\frac{40}{80}=0.5$.
**5.** In order: 9, 12, 14, 15, 18, 20, 22, 25, 27, 30 ($n=10$). $Q_1$: $2.75$th item $=12+0.75(14-12)=13.5$. Median: $5.5$th item $=\frac{18+20}{2}=19$. $Q_3$: $8.25$th item $=25+0.25(27-25)=25.5$.
**6.** $N=30$, $\sum fx=6+28+72+40+30=176$, mean $=\frac{176}{30}\approx5.87$. Cumulative frequencies 3, 10, 22, 27, 30: the $15.5$th item lies where $cf$ first reaches 22, so the median is 6. The highest frequency is 12, so the mode is 6.
**7.** $N=15+p$ and $\sum fx=10+40+15p+120+75=245+15p$. Then $16(15+p)=245+15p$, so $240+16p=245+15p$ and $p=5$. Check: $N=20$, $\sum fx=320$, and $\frac{320}{20}=16$ ✓.
:::

::: tip The three habits that save marks
Write the formula before the numbers. Show the table in statistics and the figure in height and distance, because those are where method marks live. And finish with a check, by substitution, by a second method, or by asking whether the answer is sensible: a tree 18 m tall is believable; one 180 m tall is not.
:::

## Chapter summary

- A 2-mark answer is two visible steps; a 4-mark answer is figure or table, formula, substitution, working and a checked answer.
- **Relations and functions:** list ordered pairs, then read domain, range and inverse; a function needs exactly one image for every member of the domain.
- **Polynomials and sequences:** collect like terms; check products by substituting a number; find $t_n$ by differences, then test it on every given term.
- **Limit:** substitute, or factorise and cancel a $\frac{0}{0}$ form; compare the left-hand and right-hand values.
- **Matrix:** same order to add or subtract; solve $X+A=B$ as $X=B-A$; add two matrix equations to find $X$ and $Y$.
- **Coordinate geometry:** compare squared lengths; use the section formula for trisection and quarter points; area by formula or the arrow method.
- **Trigonometry:** draw the right triangle, name $p$, $b$, $h$, choose the ratio; prove identities from one side.
- **Vector and transformation:** head minus tail; parallel by $x_1y_2=x_2y_1$; undo a transformation with its inverse.
- **Statistics:** tables for $\sum fx$ and $\sum fm$; order the data for medians and quartiles; use the modal-class formula for grouped data.

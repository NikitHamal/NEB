---
subject: Question Bank
grade: 11
unit: 12
title: "Mathematics: Unit-wise Subjective Question Bank"
hours: 0
area: Mathematics
---

Sixty-four of the seventy-five marks in the Mathematics paper are written answers: Group B has eight questions of five marks and Group C has three questions of eight marks. The marks in these groups are given for **steps**, not for the final number, so a full model solution is the real teaching tool. This chapter gives, for every chapter of the syllabus, several five-mark questions and (where the chapter feeds Group C) an eight-mark question, each solved the way you should write it in the hall.

::: key How to use this chapter
- **Attempt first, read after.** Cover the solution, work the question against the clock (about 12 minutes for five marks, 22 for eight), then compare line by line.
- **Show every step.** Write the formula, substitute, simplify, state the answer with units or in the required form. A correct answer with no working loses marks; a wrong answer with the right method keeps most of them.
- **Eight-mark questions are split** into parts (for example $3+3+2$): treat each part as its own short question.
:::

::: caution Practice items, not past papers
No question here is tagged with an examination year. NEB does not publish its Grade 11 papers, and we will not print a year we cannot verify. Every item is an original practice question set to the CDC syllabus pattern.
:::

## 12.1 Logic and Set

**Short questions (5 marks each)**

1. Using a truth table, prove that $p\Rightarrow q$ is logically equivalent to $\sim p\vee q$. <span class="marks">[5]</span>
2. If $U=\{1,2,3,4,5,6,7,8\}$, $A=\{1,2,3,4\}$ and $B=\{3,4,5,6\}$, verify De Morgan's law $(A\cup B)'=A'\cap B'$. <span class="marks">[5]</span>

**Long question (8 marks)**

3. In a class of 60 students, 35 like football, 30 like cricket and 10 like neither game. Find the number of students who (i) like both games, (ii) like football only, (iii) like cricket only. Draw a Venn diagram in words. <span class="marks">[8]</span>

::: note Model answers
**1.** Build the table for all four cases of $p,q$:

| $p$ | $q$ | $p\Rightarrow q$ | $\sim p$ | $\sim p\vee q$ |
|---|---|---|---|---|
| T | T | T | F | T |
| T | F | F | F | F |
| F | T | T | T | T |
| F | F | T | T | T |

The columns for $p\Rightarrow q$ and $\sim p\vee q$ are identical in all four rows, so $p\Rightarrow q\equiv\sim p\vee q$.

**2.** $A\cup B=\{1,2,3,4,5,6\}$, so $(A\cup B)'=\{7,8\}$. Next $A'=\{5,6,7,8\}$ and $B'=\{1,2,7,8\}$, so $A'\cap B'=\{7,8\}$. Both sides equal $\{7,8\}$; the law is verified.

**3.** Let $F$ be the football set and $C$ the cricket set. At least one game: $n(F\cup C)=60-10=50$.

(i) Both: $n(F\cap C)=n(F)+n(C)-n(F\cup C)=35+30-50=15$.
(ii) Football only: $35-15=20$.
(iii) Cricket only: $30-15=15$.
Check: $20+15+15+10=60$. Venn diagram: two overlapping circles inside a rectangle, with 20 in the football-only part, 15 in the overlap, 15 in the cricket-only part and 10 outside both circles.
:::

## 12.2 Real Numbers

**Short questions (5 marks each)**

1. Solve $|2x-3|\le 5$ and write the solution as an interval. <span class="marks">[5]</span>
2. Solve $|x+1|>3$, write the answer in interval form and describe its graph on the number line. <span class="marks">[5]</span>

::: note Model answers
**1.** $|2x-3|\le 5\iff-5\le 2x-3\le 5$. Add 3: $-2\le 2x\le 8$. Divide by 2: $-1\le x\le 4$. Solution set $=[-1,4]$; the end points are included because the inequality is non-strict.

**2.** $|x+1|>3$ means $x+1>3$ or $x+1<-3$, so $x>2$ or $x<-4$. Solution set $=(-\infty,-4)\cup(2,\infty)$. On the number line draw open circles at $-4$ and $2$, shading to the left of $-4$ and to the right of $2$; the segment between them is not shaded.
:::

## 12.3 Functions

**Short questions (5 marks each)**

1. If $f(x)=\frac{2x+1}{x-3}$, find $f^{-1}(x)$ and state the domain and range of $f$. <span class="marks">[5]</span>
2. If $f(x)=2x-1$ and $g(x)=x^2+3$, find $(f\circ g)(x)$ and $(g\circ f)(x)$. Show that $f\circ g\ne g\circ f$ by evaluating both at $x=2$. <span class="marks">[5]</span>
3. Find the domain and range of $f(x)=\sqrt{9-x^2}$. <span class="marks">[5]</span>

::: note Model answers
**1.** Let $y=\frac{2x+1}{x-3}$. Then $y(x-3)=2x+1\Rightarrow xy-3y=2x+1\Rightarrow x(y-2)=3y+1\Rightarrow x=\frac{3y+1}{y-2}$. So $f^{-1}(x)=\frac{3x+1}{x-2}$. Domain of $f$ is $\mathbb{R}-\{3\}$ (denominator zero at 3); range is $\mathbb{R}-\{2\}$ (the value that $f^{-1}$ cannot take).

**2.** $(f\circ g)(x)=f(g(x))=2(x^2+3)-1=2x^2+5$. $(g\circ f)(x)=g(2x-1)=(2x-1)^2+3=4x^2-4x+4$. At $x=2$: $(f\circ g)(2)=8+5=13$ and $(g\circ f)(2)=16-8+4=12$. Since $13\ne12$, $f\circ g\ne g\circ f$.

**3.** We need $9-x^2\ge 0$, so $x^2\le 9$ and $-3\le x\le 3$: domain $=[-3,3]$. Inside the root the value runs from $0$ (at $x=\pm3$) to $9$ (at $x=0$), so $f$ runs from $0$ to $3$: range $=[0,3]$.
:::

## 12.4 Curve Sketching

**Short questions (5 marks each)**

1. Test whether $f(x)=x^3+\sin x$, $g(x)=x^2\cos x$ and $h(x)=x^2+x$ are even, odd or neither. <span class="marks">[5]</span>
2. Sketch the graph of $y=x^2-4x+3$, showing its vertex, intercepts and axis of symmetry. <span class="marks">[5]</span>
3. Sketch $y=2\sin x$ for $0\le x\le 2\pi$ and state its amplitude and period. <span class="marks">[5]</span>

::: note Model answers
**1.** $f(-x)=(-x)^3+\sin(-x)=-x^3-\sin x=-f(x)$: **odd**. $g(-x)=x^2\cos(-x)=x^2\cos x=g(x)$: **even**. $h(-x)=x^2-x$, which is neither $h(x)$ nor $-h(x)$: **neither**.

**2.** Write $y=(x-2)^2-1$. Vertex $(2,-1)$ (the minimum point); axis of symmetry $x=2$. $x$-intercepts: $(x-1)(x-3)=0$ gives $x=1,3$. $y$-intercept: $y=3$. The parabola opens upward, passes through $(0,3),(1,0),(2,-1),(3,0),(4,3)$ and is symmetric about $x=2$.

**3.** Amplitude $=2$, period $=2\pi$. Key points:

| $x$ | 0 | $\frac{\pi}{2}$ | $\pi$ | $\frac{3\pi}{2}$ | $2\pi$ |
|---|---|---|---|---|---|
| $y$ | 0 | 2 | 0 | $-2$ | 0 |

Join them with a smooth wave: it rises to a crest of height 2 at $\frac{\pi}{2}$, crosses the axis at $\pi$, reaches a trough of $-2$ at $\frac{3\pi}{2}$ and returns to 0 at $2\pi$.
:::

## 12.5 Sequence and Series

**Short questions (5 marks each)**

1. The sum of the first $n$ terms of an A.P. is $3n^2+2n$. Find its first term, common difference and 10th term. <span class="marks">[5]</span>
2. Three numbers are in G.P. Their sum is 14 and their product is 64. Find them. <span class="marks">[5]</span>
3. Find the A.M., G.M. and H.M. of 2 and 8 and verify that $G^2=A\times H$. <span class="marks">[5]</span>

**Long question (8 marks)**

4. (i) Insert three geometric means between 4 and 64. (ii) Find the sum of the first 10 terms of the G.P. $2,4,8,\dots$ (iii) Show that A.M. $\ge $ G.M. for the numbers 4 and 16. <span class="marks">[3+3+2]</span>

::: note Model answers
**1.** $t_n=S_n-S_{n-1}=(3n^2+2n)-[3(n-1)^2+2(n-1)]=6n-1$. So $a=t_1=5$, $t_2=11$, $d=6$, $t_{10}=60-1=59$.

**2.** Take the numbers $\frac{a}{r},a,ar$. Product: $a^3=64\Rightarrow a=4$. Sum: $\frac{4}{r}+4+4r=14\Rightarrow4+4r^2=10r\Rightarrow2r^2-5r+2=0\Rightarrow(2r-1)(r-2)=0$, so $r=2$ or $\frac{1}{2}$. The numbers are $2,4,8$ (or $8,4,2$).

**3.** $A=\frac{2+8}{2}=5$; $G=\sqrt{2\times8}=4$; $H=\frac{2\times2\times8}{2+8}=\frac{32}{10}=3.2$. Then $G^2=16$ and $A\times H=5\times3.2=16$, so $G^2=AH$.

**4.** (i) Five terms in all: $64=4r^4\Rightarrow r^4=16\Rightarrow r=2$. The means are $8,16,32$.
(ii) $S_{10}=\frac{a(r^{10}-1)}{r-1}=\frac{2(1024-1)}{1}=2046$.
(iii) $A=\frac{4+16}{2}=10$ and $G=\sqrt{64}=8$; $10>8$, so $A>G$. (Equality holds only when the two numbers are equal.)
:::

## 12.6 Matrices and Determinants

**Short questions (5 marks each)**

1. Find the inverse of the matrix $A$ whose first row is $(2,\ 1)$ and second row is $(5,\ 3)$, and verify $AA^{-1}=I$. <span class="marks">[5]</span>
2. Evaluate the determinant whose rows are $(1,2,3)$, $(4,5,6)$ and $(7,8,10)$. <span class="marks">[5]</span>
3. For $A$ with rows $(1,2),(3,4)$ and $B$ with rows $(0,1),(1,0)$, verify that $(AB)^T=B^TA^T$. <span class="marks">[5]</span>

**Long question (8 marks)**

4. Solve by Cramer's rule: $x+y+z=6$, $x-y+z=2$, $x+y-z=0$. <span class="marks">[8]</span>

::: note Model answers
**1.** $|A|=2\times3-1\times5=1\ne0$. The adjoint is found by swapping the diagonal entries and changing the sign of the others: first row $(3,\ -1)$, second row $(-5,\ 2)$. So $A^{-1}=\frac{1}{1}\,\text{adj}A$ has rows $(3,-1)$ and $(-5,2)$. Check: row 1 of $A$ times the columns: $2(3)+1(-5)=1$ and $2(-1)+1(2)=0$; row 2: $5(3)+3(-5)=0$ and $5(-1)+3(2)=1$. So $AA^{-1}=I$.

**2.** Expand along the first row: $1(5\cdot10-6\cdot8)-2(4\cdot10-6\cdot7)+3(4\cdot8-5\cdot7)=1(2)-2(-2)+3(-3)=2+4-9=-3$.

**3.** $AB$: row 1 $=(1\cdot0+2\cdot1,\ 1\cdot1+2\cdot0)=(2,1)$; row 2 $=(3\cdot0+4\cdot1,\ 3\cdot1+4\cdot0)=(4,3)$. So $(AB)^T$ has rows $(2,4)$ and $(1,3)$. Now $B^T=B$ (rows $(0,1),(1,0)$) and $A^T$ has rows $(1,3),(2,4)$. $B^TA^T$: row 1 $=(0\cdot1+1\cdot2,\ 0\cdot3+1\cdot4)=(2,4)$; row 2 $=(1\cdot1+0\cdot2,\ 1\cdot3+0\cdot4)=(1,3)$. The two results agree.

**4.** The coefficient determinant has rows $(1,1,1),(1,-1,1),(1,1,-1)$: $D=1[(-1)(-1)-1\cdot1]-1[1(-1)-1\cdot1]+1[1\cdot1-(-1)\cdot1]=0+2+2=4$.
$D_x$ (first column replaced by $6,2,0$): $6(1-1)-1(-2-0)+1(2-0)=0+2+2=4$.
$D_y$ (second column replaced): rows $(1,6,1),(1,2,1),(1,0,-1)$: $1(-2-0)-6(-1-1)+1(0-2)=-2+12-2=8$.
$D_z$ (third column replaced): rows $(1,1,6),(1,-1,2),(1,1,0)$: $1(0-2)-1(0-2)+6(1+1)=-2+2+12=12$.
$x=\frac{4}{4}=1$, $y=\frac{8}{4}=2$, $z=\frac{12}{4}=3$. Check in the first equation: $1+2+3=6$. ✓
:::

## 12.7 Quadratic Equation

**Short questions (5 marks each)**

1. If one root of $x^2-7x+k=0$ is twice the other, find $k$. <span class="marks">[5]</span>
2. If $\alpha,\beta$ are the roots of $x^2-6x+4=0$, find $\alpha^2+\beta^2$ and $\frac{1}{\alpha}+\frac{1}{\beta}$. <span class="marks">[5]</span>
3. Find the values of $k$ for which $x^2+2(k+1)x+k^2=0$ has equal roots. <span class="marks">[5]</span>

**Long question (8 marks)**

4. (i) If $\alpha,\beta$ are the roots of $ax^2+bx+c=0$, prove that the equation with roots $\frac{1}{\alpha},\frac{1}{\beta}$ is $cx^2+bx+a=0$. (ii) Form the equation whose roots are the sum and the product of the roots of $x^2-5x+6=0$. (iii) Find $k$ if $x^2-3x+k=0$ and $x^2-5x+6=0$ have a common root. <span class="marks">[3+3+2]</span>

::: note Model answers
**1.** Let the roots be $\alpha$ and $2\alpha$. Sum: $3\alpha=7\Rightarrow\alpha=\frac{7}{3}$. Product: $2\alpha^2=k\Rightarrow k=2\times\frac{49}{9}=\frac{98}{9}$.

**2.** $\alpha+\beta=6$, $\alpha\beta=4$. $\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta=36-8=28$. $\frac{1}{\alpha}+\frac{1}{\beta}=\frac{\alpha+\beta}{\alpha\beta}=\frac{6}{4}=\frac{3}{2}$.

**3.** Equal roots need $D=0$: $[2(k+1)]^2-4(1)(k^2)=4(k^2+2k+1)-4k^2=8k+4=0$, so $k=-\frac{1}{2}$.

**4.** (i) $\alpha+\beta=-\frac{b}{a}$, $\alpha\beta=\frac{c}{a}$. For the new roots: sum $=\frac{1}{\alpha}+\frac{1}{\beta}=\frac{\alpha+\beta}{\alpha\beta}=-\frac{b}{c}$, product $=\frac{1}{\alpha\beta}=\frac{a}{c}$. The equation is $x^2+\frac{b}{c}x+\frac{a}{c}=0$, that is $cx^2+bx+a=0$.
(ii) The roots of $x^2-5x+6=0$ are 2 and 3, so the new roots are $2+3=5$ and $2\times3=6$. Sum $=11$, product $=30$: $x^2-11x+30=0$.
(iii) The common root must be 2 or 3. Put $x=2$: $4-6+k=0\Rightarrow k=2$. Put $x=3$: $9-9+k=0\Rightarrow k=0$. So $k=2$ or $k=0$.
:::

## 12.8 Complex Numbers

**Short questions (5 marks each)**

1. Express $\frac{1+2i}{2-i}$ in the form $a+ib$ and find its modulus. <span class="marks">[5]</span>
2. Find the square roots of $5+12i$. <span class="marks">[5]</span>
3. If $z=3-4i$, find $|z|$, $\bar z$ and $z^{-1}$. <span class="marks">[5]</span>

**Long question (8 marks)**

4. (i) Prove that $|z_1z_2|=|z_1||z_2|$. (ii) Find real $x,y$ such that $(x+iy)(2+3i)=-4+7i$. (iii) Plot $3+4i$ on the Argand plane and find its modulus and argument. <span class="marks">[3+3+2]</span>

::: note Model answers
**1.** Multiply by the conjugate: $\frac{(1+2i)(2+i)}{(2-i)(2+i)}=\frac{2+i+4i+2i^2}{4+1}=\frac{0+5i}{5}=i$. So $a=0$, $b=1$ and $|i|=1$.

**2.** Let $\sqrt{5+12i}=a+ib$. Then $a^2-b^2=5$ and $2ab=12$. Also $a^2+b^2=|5+12i|=13$. Adding: $2a^2=18\Rightarrow a=\pm3$; subtracting: $2b^2=8\Rightarrow b=\pm2$. Since $ab>0$ the signs agree: the roots are $\pm(3+2i)$. Check: $(3+2i)^2=9-4+12i$. ✓

**3.** $|z|=\sqrt{9+16}=5$. $\bar z=3+4i$. $z^{-1}=\frac{\bar z}{|z|^2}=\frac{3+4i}{25}$.

**4.** (i) Let $z_1=a+ib$, $z_2=c+id$. Then $z_1z_2=(ac-bd)+i(ad+bc)$ and $|z_1z_2|^2=(ac-bd)^2+(ad+bc)^2=a^2c^2+b^2d^2+a^2d^2+b^2c^2=(a^2+b^2)(c^2+d^2)$. Taking square roots, $|z_1z_2|=|z_1||z_2|$.
(ii) $x+iy=\frac{-4+7i}{2+3i}=\frac{(-4+7i)(2-3i)}{13}=\frac{-8+12i+14i+21}{13}=\frac{13+26i}{13}=1+2i$. So $x=1$, $y=2$.
(iii) The point is $(3,4)$ in the first quadrant. $|z|=5$ and $\arg z=\tan^{-1}\frac{4}{3}\approx53.13^\circ$.
:::

## 12.9 Inverse Circular Functions

**Short questions (5 marks each)**

1. Prove that $\tan^{-1}\frac{1}{2}+\tan^{-1}\frac{1}{3}=\frac{\pi}{4}$. <span class="marks">[5]</span>
2. Evaluate $\sin\left(2\cos^{-1}\frac{3}{5}\right)$. <span class="marks">[5]</span>

**Long question (8 marks)**

3. (i) Prove that $2\tan^{-1}\frac{1}{3}+\tan^{-1}\frac{1}{7}=\frac{\pi}{4}$. (ii) Solve $\tan^{-1}(x+1)+\tan^{-1}(x-1)=\tan^{-1}\frac{8}{31}$. (iii) Find the value of $\sin^{-1}\left(\sin\frac{5\pi}{6}\right)$. <span class="marks">[3+3+2]</span>

::: note Model answers
**1.** Use $\tan^{-1}a+\tan^{-1}b=\tan^{-1}\frac{a+b}{1-ab}$ (valid as $ab<1$): $\tan^{-1}\frac{\frac{1}{2}+\frac{1}{3}}{1-\frac{1}{6}}=\tan^{-1}\frac{5/6}{5/6}=\tan^{-1}1=\frac{\pi}{4}$.

**2.** Let $\theta=\cos^{-1}\frac{3}{5}$, so $\cos\theta=\frac{3}{5}$ and $\sin\theta=\frac{4}{5}$. $\sin2\theta=2\sin\theta\cos\theta=2\cdot\frac{4}{5}\cdot\frac{3}{5}=\frac{24}{25}$.

**3.** (i) $2\tan^{-1}\frac{1}{3}=\tan^{-1}\frac{2/3}{1-1/9}=\tan^{-1}\frac{3}{4}$. Then $\tan^{-1}\frac{3}{4}+\tan^{-1}\frac{1}{7}=\tan^{-1}\frac{\frac{3}{4}+\frac{1}{7}}{1-\frac{3}{28}}=\tan^{-1}\frac{25/28}{25/28}=\tan^{-1}1=\frac{\pi}{4}$.
(ii) LHS $=\tan^{-1}\frac{2x}{1-(x^2-1)}=\tan^{-1}\frac{2x}{2-x^2}$. So $\frac{2x}{2-x^2}=\frac{8}{31}\Rightarrow62x=16-8x^2\Rightarrow4x^2+31x-8=0\Rightarrow x=\frac{-31\pm33}{8}$, giving $x=\frac{1}{4}$ or $x=-8$. For $x=-8$, $(x+1)(x-1)=63>1$ and the addition formula does not hold, so reject it. Hence $x=\frac{1}{4}$.
(iii) $\frac{5\pi}{6}$ is outside $[-\frac{\pi}{2},\frac{\pi}{2}]$; $\sin\frac{5\pi}{6}=\frac{1}{2}$, so the value is $\sin^{-1}\frac{1}{2}=\frac{\pi}{6}$.
:::

## 12.10 Trigonometric Equations and General Values

**Short questions (5 marks each)**

1. Solve $2\sin^2x+\sin x-1=0$ for $0\le x\le 2\pi$. <span class="marks">[5]</span>
2. Solve $\cos2x=\cos x$ for $0\le x\le 2\pi$. <span class="marks">[5]</span>
3. Find the general solution of $\sin3x=\sin x$. <span class="marks">[5]</span>

**Long question (8 marks)**

4. Find the general solution of $\sqrt{3}\cos x+\sin x=\sqrt{2}$. <span class="marks">[8]</span>

::: note Model answers
**1.** Factorise: $(2\sin x-1)(\sin x+1)=0$. So $\sin x=\frac{1}{2}$ giving $x=\frac{\pi}{6},\frac{5\pi}{6}$, or $\sin x=-1$ giving $x=\frac{3\pi}{2}$. Solutions: $\frac{\pi}{6},\ \frac{5\pi}{6},\ \frac{3\pi}{2}$.

**2.** $\cos2x=\cos x\Rightarrow2x=2n\pi\pm x$. Taking $+$: $x=2n\pi$; taking $-$: $3x=2n\pi$, $x=\frac{2n\pi}{3}$. In $[0,2\pi]$: $x=0,\ \frac{2\pi}{3},\ \frac{4\pi}{3},\ 2\pi$.

**3.** $\sin3x=\sin x\Rightarrow3x=n\pi+(-1)^nx$. If $n=2m$: $3x=2m\pi+x\Rightarrow x=m\pi$. If $n=2m+1$: $3x=(2m+1)\pi-x\Rightarrow x=\frac{(2m+1)\pi}{4}$. General solution: $x=m\pi$ or $x=\frac{(2m+1)\pi}{4}$, $m\in\mathbb{Z}$.

**4.** Write $\sqrt{3}\cos x+\sin x=R\cos(x-\alpha)$ with $R\cos\alpha=\sqrt{3}$, $R\sin\alpha=1$. Then $R=\sqrt{3+1}=2$ and $\tan\alpha=\frac{1}{\sqrt{3}}$, so $\alpha=\frac{\pi}{6}$. The equation becomes $2\cos\left(x-\frac{\pi}{6}\right)=\sqrt{2}$, i.e. $\cos\left(x-\frac{\pi}{6}\right)=\frac{1}{\sqrt{2}}=\cos\frac{\pi}{4}$. Hence $x-\frac{\pi}{6}=2n\pi\pm\frac{\pi}{4}$, so $x=2n\pi+\frac{\pi}{6}\pm\frac{\pi}{4}$, that is $x=2n\pi+\frac{5\pi}{12}$ or $x=2n\pi-\frac{\pi}{12}$, $n\in\mathbb{Z}$.
:::

## 12.11 Straight Line

**Short questions (5 marks each)**

1. Find the length of the perpendicular from the point $(4,1)$ to the line $3x-4y-18=0$. <span class="marks">[5]</span>
2. Find the distance between the parallel lines $3x+4y+5=0$ and $3x+4y-10=0$. <span class="marks">[5]</span>
3. Find the equations of the bisectors of the angles between the lines $4x+3y-7=0$ and $3x+4y-7=0$. <span class="marks">[5]</span>

**Long question (8 marks)**

4. A triangle has vertices $A(0,0)$, $B(4,0)$ and $C(0,3)$. (i) Find the equation of $BC$. (ii) Find the length of the perpendicular from $A$ to $BC$. (iii) Hence find the area of the triangle and check it by the base-height formula. <span class="marks">[2+3+3]</span>

::: note Model answers
**1.** $d=\frac{|3(4)-4(1)-18|}{\sqrt{3^2+4^2}}=\frac{|12-4-18|}{5}=\frac{10}{5}=2$ units.

**2.** Take the point $(0,-\frac{5}{4})$ on the first line (put $x=0$: $4y=-5$). Its distance from $3x+4y-10=0$ is $\frac{|0-5-10|}{5}=\frac{15}{5}=3$ units. (Equivalently, $\frac{|c_1-c_2|}{\sqrt{a^2+b^2}}=\frac{15}{5}$.)

**3.** A point on a bisector is equidistant from both lines: $\frac{|4x+3y-7|}{5}=\frac{|3x+4y-7|}{5}$. Taking $+$: $4x+3y-7=3x+4y-7\Rightarrow x-y=0$. Taking $-$: $4x+3y-7=-3x-4y+7\Rightarrow7x+7y-14=0\Rightarrow x+y-2=0$. The bisectors are $x-y=0$ and $x+y-2=0$.

**4.** (i) $BC$ has intercepts 4 and 3: $\frac{x}{4}+\frac{y}{3}=1\Rightarrow3x+4y-12=0$.
(ii) Perpendicular from $A(0,0)$: $\frac{|-12|}{\sqrt{9+16}}=\frac{12}{5}=2.4$ units.
(iii) $BC=\sqrt{16+9}=5$. Area $=\frac{1}{2}\times5\times\frac{12}{5}=6$. Check: $\frac{1}{2}\times AB\times AC=\frac{1}{2}\times4\times3=6$. ✓
:::

## 12.12 Pair of Straight Lines

**Short questions (5 marks each)**

1. Show that $2x^2+5xy+2y^2=0$ represents two straight lines and find the angle between them. <span class="marks">[5]</span>
2. Show that $6x^2-5xy-6y^2=0$ represents perpendicular lines and find the equation of its bisectors. <span class="marks">[5]</span>
3. For what values of $\lambda$ do the lines $x^2+\lambda xy+4y^2=0$ coincide? <span class="marks">[5]</span>

**Long question (8 marks)**

4. (i) Show that $3x^2+7xy+2y^2+5x+5y+2=0$ represents a pair of straight lines. (ii) Find the separate equations of the lines. (iii) Find the angle between them. <span class="marks">[3+3+2]</span>

::: note Model answers
**1.** Factorise: $2x^2+5xy+2y^2=(2x+y)(x+2y)=0$, so the lines are $2x+y=0$ and $x+2y=0$. Here $a=b=2$, $h=\frac{5}{2}$. $\tan\theta=\frac{2\sqrt{h^2-ab}}{|a+b|}=\frac{2\sqrt{\frac{25}{4}-4}}{4}=\frac{2\times\frac{3}{2}}{4}=\frac{3}{4}$, so $\theta=\tan^{-1}\frac{3}{4}\approx36.87^\circ$.

**2.** $a=6$, $b=-6$, so $a+b=0$: the lines are perpendicular. (Indeed $6x^2-5xy-6y^2=(3x+2y)(2x-3y)$; slopes $-\frac{3}{2}$ and $\frac{2}{3}$ have product $-1$.) With $h=-\frac{5}{2}$ the bisectors satisfy $\frac{x^2-y^2}{a-b}=\frac{xy}{h}$: $\frac{x^2-y^2}{12}=\frac{xy}{-5/2}=-\frac{2xy}{5}$, so $5(x^2-y^2)=-24xy$, i.e. $5x^2+24xy-5y^2=0$.

**3.** The lines coincide when $h^2=ab$. Here $a=1$, $2h=\lambda$, $b=4$: $\left(\frac{\lambda}{2}\right)^2=4\Rightarrow\lambda^2=16\Rightarrow\lambda=\pm4$.

**4.** (i) $a=3$, $h=\frac{7}{2}$, $b=2$, $g=\frac{5}{2}$, $f=\frac{5}{2}$, $c=2$. The condition is $abc+2fgh-af^2-bg^2-ch^2=0$. Compute: $abc=12$; $2fgh=2\cdot\frac{5}{2}\cdot\frac{5}{2}\cdot\frac{7}{2}=\frac{175}{4}$; $af^2=\frac{75}{4}$; $bg^2=\frac{50}{4}$; $ch^2=\frac{98}{4}$. Sum: $12+\frac{175-75-50-98}{4}=12-12=0$. ✓
(ii) $3x^2+7xy+2y^2=(3x+y)(x+2y)$. Write $(3x+y+p)(x+2y+q)$: matching $x$: $3q+p=5$; $y$: $q+2p=5$; constant $pq=2$. Solving, $q=1$, $p=2$, and $pq=2$ ✓. The lines are $3x+y+2=0$ and $x+2y+1=0$.
(iii) $\tan\theta=\frac{2\sqrt{h^2-ab}}{|a+b|}=\frac{2\sqrt{\frac{49}{4}-6}}{5}=\frac{2\times\frac{5}{2}}{5}=1$, so $\theta=45^\circ$.
:::

## 12.13 Coordinates in Space

**Short questions (5 marks each)**

1. Show that the points $A(0,7,10)$, $B(-1,6,6)$ and $C(-4,9,6)$ form a right-angled isosceles triangle. <span class="marks">[5]</span>
2. Find the direction cosines of the line joining $(2,3,-1)$ and $(-1,1,5)$. <span class="marks">[5]</span>
3. Find the point on the $y$-axis equidistant from $(1,2,3)$ and $(-1,4,5)$. <span class="marks">[5]</span>

**Long question (8 marks)**

4. (i) A line makes angles $\alpha,\beta,\gamma$ with the coordinate axes; prove $\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1$. (ii) Find the direction cosines of a line whose direction ratios are $1,-2,2$. (iii) Find the distance of $P(3,4,5)$ from the origin. <span class="marks">[3+3+2]</span>

::: note Model answers
**1.** $AB^2=1+1+16=18$; $BC^2=9+9+0=18$; $CA^2=16+4+16=36$. $AB=BC$ so the triangle is isosceles, and $AB^2+BC^2=36=CA^2$, so by the converse of Pythagoras the angle at $B$ is a right angle.

**2.** Direction ratios: $(-1-2,\ 1-3,\ 5+1)=(-3,-2,6)$. Magnitude $\sqrt{9+4+36}=7$. Direction cosines: $-\frac{3}{7},\ -\frac{2}{7},\ \frac{6}{7}$ (or all signs reversed).

**3.** Let the point be $P(0,y,0)$. $PA^2=1+(y-2)^2+9$ and $PB^2=1+(y-4)^2+25$. Equating: $(y-2)^2+10=(y-4)^2+26\Rightarrow y^2-4y+14=y^2-8y+42\Rightarrow4y=28\Rightarrow y=7$. The point is $(0,7,0)$.

**4.** (i) Let the line pass through the origin and let $P$ on it be at distance $r$. Its coordinates are $(lr,mr,nr)$, where $l=\cos\alpha$, $m=\cos\beta$, $n=\cos\gamma$. Then $OP^2=r^2=l^2r^2+m^2r^2+n^2r^2$, so $l^2+m^2+n^2=1$.
(ii) $\sqrt{1+4+4}=3$, so the direction cosines are $\frac{1}{3},\ -\frac{2}{3},\ \frac{2}{3}$ (or all signs reversed).
(iii) $OP=\sqrt{9+16+25}=\sqrt{50}=5\sqrt{2}$.
:::

## 12.14 Vectors

**Short questions (5 marks each)**

1. Show that the points with position vectors $\mathbf{a}-2\mathbf{b}+3\mathbf{c}$, $2\mathbf{a}+3\mathbf{b}-4\mathbf{c}$ and $-7\mathbf{b}+10\mathbf{c}$ are collinear. <span class="marks">[5]</span>
2. Express $5\mathbf{i}+3\mathbf{j}$ as a linear combination of $\mathbf{i}+\mathbf{j}$ and $\mathbf{i}-\mathbf{j}$. <span class="marks">[5]</span>
3. Prove by vectors that the diagonals of a parallelogram bisect each other. <span class="marks">[5]</span>

**Long question (8 marks)**

4. Using vectors, prove (i) that the line joining the midpoints of two sides of a triangle is parallel to the third side and half its length; (ii) that the point $G$ with position vector $\frac{\mathbf{a}+\mathbf{b}+\mathbf{c}}{3}$ lies on each median of the triangle with vertices $\mathbf{a},\mathbf{b},\mathbf{c}$, dividing it $2:1$. <span class="marks">[4+4]</span>

::: note Model answers
**1.** Name the points $A,B,C$ in order. $\overrightarrow{AB}=(2\mathbf{a}+3\mathbf{b}-4\mathbf{c})-(\mathbf{a}-2\mathbf{b}+3\mathbf{c})=\mathbf{a}+5\mathbf{b}-7\mathbf{c}$. $\overrightarrow{BC}=(-7\mathbf{b}+10\mathbf{c})-(2\mathbf{a}+3\mathbf{b}-4\mathbf{c})=-2\mathbf{a}-10\mathbf{b}+14\mathbf{c}=-2(\mathbf{a}+5\mathbf{b}-7\mathbf{c})$. So $\overrightarrow{BC}=-2\overrightarrow{AB}$: the vectors are parallel and share the point $B$, hence $A,B,C$ are collinear.

**2.** Let $5\mathbf{i}+3\mathbf{j}=x(\mathbf{i}+\mathbf{j})+y(\mathbf{i}-\mathbf{j})=(x+y)\mathbf{i}+(x-y)\mathbf{j}$. Comparing, $x+y=5$ and $x-y=3$, so $x=4$, $y=1$. Hence $5\mathbf{i}+3\mathbf{j}=4(\mathbf{i}+\mathbf{j})+1(\mathbf{i}-\mathbf{j})$.

**3.** Let $ABCD$ be a parallelogram with position vectors $\mathbf{a},\mathbf{b},\mathbf{c},\mathbf{d}$. Since $\overrightarrow{AB}=\overrightarrow{DC}$, $\mathbf{b}-\mathbf{a}=\mathbf{c}-\mathbf{d}$, so $\mathbf{a}+\mathbf{c}=\mathbf{b}+\mathbf{d}$. The midpoint of $AC$ is $\frac{\mathbf{a}+\mathbf{c}}{2}$ and the midpoint of $BD$ is $\frac{\mathbf{b}+\mathbf{d}}{2}$. These are equal, so the diagonals bisect each other.

**4.** (i) Take $A$ as origin, with $B=\mathbf{b}$ and $C=\mathbf{c}$. The midpoints of $AB$ and $AC$ are $D=\frac{\mathbf{b}}{2}$ and $E=\frac{\mathbf{c}}{2}$. $\overrightarrow{DE}=\frac{\mathbf{c}}{2}-\frac{\mathbf{b}}{2}=\frac{1}{2}(\mathbf{c}-\mathbf{b})=\frac{1}{2}\overrightarrow{BC}$. So $DE\parallel BC$ and $DE=\frac{1}{2}BC$.
(ii) Let $D$ be the midpoint of $BC$: $\frac{\mathbf{b}+\mathbf{c}}{2}$. The point dividing $AD$ in the ratio $2:1$ is $\frac{1\cdot\mathbf{a}+2\cdot\frac{\mathbf{b}+\mathbf{c}}{2}}{3}=\frac{\mathbf{a}+\mathbf{b}+\mathbf{c}}{3}=G$. The expression is symmetric in $\mathbf{a},\mathbf{b},\mathbf{c}$, so the same point divides the other two medians $2:1$ as well; the three medians concur at $G$.
:::

## 12.15 Measures of Dispersion

**Short questions (5 marks each)**

1. Find the standard deviation of $2,4,4,4,5,5,7,9$. <span class="marks">[5]</span>
2. Series A has mean 50 and standard deviation 10; series B has mean 80 and standard deviation 12. Which is more consistent? <span class="marks">[5]</span>
3. The mean of a distribution is 60, the median is 58 and the standard deviation is 8. Find Karl Pearson's coefficient of skewness and interpret it. <span class="marks">[5]</span>

**Long question (8 marks)**

4. The classes $0$–$10$, $10$–$20$, $20$–$30$, $30$–$40$, $40$–$50$ have frequencies $2,8,30,8,2$. Find (i) the mean, (ii) the standard deviation, (iii) the coefficient of variation. <span class="marks">[2+4+2]</span>

::: note Model answers
**1.** $n=8$, mean $=\frac{40}{8}=5$. Deviations: $-3,-1,-1,-1,0,0,2,4$; squares $9,1,1,1,0,0,4,16$, sum $=32$. Variance $=\frac{32}{8}=4$, so $\sigma=2$.

**2.** C.V. of A $=\frac{10}{50}\times100=20\%$. C.V. of B $=\frac{12}{80}\times100=15\%$. The smaller C.V. means greater consistency, so **series B is more consistent**.

**3.** Mode $=3\times\text{median}-2\times\text{mean}=174-120=54$. $S_k=\frac{\text{Mean}-\text{Mode}}{\sigma}=\frac{60-54}{8}=0.75$. Positive, so the distribution is positively skewed (longer tail to the right).

**4.** Mid-values: $5,15,25,35,45$. Take $A=25$, $u=\frac{x-25}{10}$: $-2,-1,0,1,2$. $N=2+8+30+8+2=50$.
(i) $\sum fu=2(-2)+8(-1)+0+8(1)+2(2)=0$, so $\bar x=25+10\times0=25$.
(ii) $\sum fu^2=2(4)+8(1)+0+8(1)+2(4)=32$. $\sigma^2=100\left[\frac{32}{50}-0^2\right]=64$, so $\sigma=8$.
(iii) C.V. $=\frac{8}{25}\times100=32\%$.
:::

## 12.16 Probability

**Short questions (5 marks each)**

1. A bag has 5 red and 3 blue balls. Two balls are drawn one after another. Find the probability that both are red (i) without replacement, (ii) with replacement. <span class="marks">[5]</span>
2. If $P(A)=0.5$, $P(B)=0.4$ and $P(A\cup B)=0.7$, find $P(A\cap B)$ and decide whether $A$ and $B$ are independent. <span class="marks">[5]</span>
3. Two dice are thrown. Find the probability that the sum is at least 10. <span class="marks">[5]</span>

**Long question (8 marks)**

4. A card is drawn from a well-shuffled pack of 52. Find the probability that it is (i) a king or a heart, (ii) neither a king nor a heart. (iii) Three coins are tossed; find the probability of exactly two heads. <span class="marks">[3+2+3]</span>

::: note Model answers
**1.** (i) $P=\frac{5}{8}\times\frac{4}{7}=\frac{20}{56}=\frac{5}{14}$. (ii) With replacement the draws are independent: $P=\frac{5}{8}\times\frac{5}{8}=\frac{25}{64}$.

**2.** $P(A\cap B)=P(A)+P(B)-P(A\cup B)=0.5+0.4-0.7=0.2$. Since $P(A)P(B)=0.5\times0.4=0.2=P(A\cap B)$, the events are independent.

**3.** Total outcomes $=36$. Sum $\ge 10$: $(4,6),(5,5),(6,4),(5,6),(6,5),(6,6)$, so 6 outcomes. $P=\frac{6}{36}=\frac{1}{6}$.

**4.** (i) There are 4 kings and 13 hearts, and the king of hearts is counted in both, so $P=\frac{4}{52}+\frac{13}{52}-\frac{1}{52}=\frac{16}{52}=\frac{4}{13}$.
(ii) $1-\frac{4}{13}=\frac{9}{13}$.
(iii) The sample space has $2^3=8$ outcomes. Exactly two heads: HHT, HTH, THH, so $P=\frac{3}{8}$.
:::

## 12.17 Limits and Continuity

**Short questions (5 marks each)**

1. Evaluate $\lim_{x\to3}\frac{x^3-27}{x^2-9}$. <span class="marks">[5]</span>
2. Evaluate $\lim_{x\to0}\frac{1-\cos x}{x^2}$. <span class="marks">[5]</span>
3. Find $k$ if $f(x)=kx+1$ for $x\le 3$ and $f(x)=3x-5$ for $x>3$ is continuous at $x=3$. <span class="marks">[5]</span>

**Long question (8 marks)**

4. (i) Evaluate $\lim_{x\to\infty}\left(\sqrt{x^2+3x}-x\right)$. (ii) Evaluate $\lim_{x\to0}\frac{\sin5x}{\tan3x}$. (iii) Examine the continuity of $f(x)=|x|$ at $x=0$. <span class="marks">[3+2+3]</span>

::: note Model answers
**1.** The direct substitution gives $\frac{0}{0}$, so factorise: $\frac{(x-3)(x^2+3x+9)}{(x-3)(x+3)}=\frac{x^2+3x+9}{x+3}\to\frac{27}{6}=\frac{9}{2}$.

**2.** $1-\cos x=2\sin^2\frac{x}{2}$, so $\frac{1-\cos x}{x^2}=\frac{1}{2}\left(\frac{\sin(x/2)}{x/2}\right)^2\to\frac{1}{2}(1)^2=\frac{1}{2}$.

**3.** Left limit at 3: $3k+1$. Right limit at 3: $3(3)-5=4$. Also $f(3)=3k+1$. Continuity needs left limit $=$ right limit: $3k+1=4\Rightarrow k=1$.

**4.** (i) Multiply and divide by the conjugate: $\frac{(x^2+3x)-x^2}{\sqrt{x^2+3x}+x}=\frac{3x}{\sqrt{x^2+3x}+x}=\frac{3}{\sqrt{1+\frac{3}{x}}+1}\to\frac{3}{1+1}=\frac{3}{2}$.
(ii) $\frac{\sin5x}{\tan3x}=\frac{\sin5x}{5x}\cdot\frac{3x}{\tan3x}\cdot\frac{5}{3}\to1\cdot1\cdot\frac{5}{3}=\frac{5}{3}$.
(iii) $f(0)=0$. Left limit: for $x<0$, $f(x)=-x\to0$. Right limit: for $x>0$, $f(x)=x\to0$. Left limit $=$ right limit $=f(0)$, so $f$ is continuous at $0$ (though not differentiable there).
:::

## 12.18 Derivatives

**Short questions (5 marks each)**

1. Find the derivative of $\sqrt{x}$ from the first principle. <span class="marks">[5]</span>
2. Differentiate $y=\frac{x^2+1}{x-1}$. <span class="marks">[5]</span>
3. If $x^3+y^3=3xy$, find $\frac{dy}{dx}$. <span class="marks">[5]</span>
4. Find the equation of the tangent to $y=x^2-3x+2$ at the point $(3,2)$. <span class="marks">[5]</span>
5. If $x=a(t-\sin t)$ and $y=a(1-\cos t)$, find $\frac{dy}{dx}$. <span class="marks">[5]</span>

**Long questions (8 marks)**

6. Find the maximum and minimum values of $f(x)=x^3-6x^2+9x+1$, and the intervals where it is increasing or decreasing. <span class="marks">[8]</span>
7. Divide 40 into two parts whose product is greatest, and show that your answer is a maximum. Then find the point of inflection of $y=x^3$. <span class="marks">[5+3]</span>

::: note Model answers
**1.** $f'(x)=\lim_{h\to0}\frac{\sqrt{x+h}-\sqrt{x}}{h}=\lim_{h\to0}\frac{(x+h)-x}{h(\sqrt{x+h}+\sqrt{x})}=\lim_{h\to0}\frac{1}{\sqrt{x+h}+\sqrt{x}}=\frac{1}{2\sqrt{x}}$.

**2.** Quotient rule: $y'=\frac{(x-1)(2x)-(x^2+1)(1)}{(x-1)^2}=\frac{2x^2-2x-x^2-1}{(x-1)^2}=\frac{x^2-2x-1}{(x-1)^2}$.

**3.** Differentiate implicitly: $3x^2+3y^2\frac{dy}{dx}=3y+3x\frac{dy}{dx}$. Collect: $\frac{dy}{dx}(y^2-x)=y-x^2$, so $\frac{dy}{dx}=\frac{y-x^2}{y^2-x}$.

**4.** $\frac{dy}{dx}=2x-3$, which is $3$ at $x=3$. Tangent: $y-2=3(x-3)\Rightarrow y=3x-7$, i.e. $3x-y-7=0$.

**5.** $\frac{dx}{dt}=a(1-\cos t)$ and $\frac{dy}{dt}=a\sin t$. $\frac{dy}{dx}=\frac{\sin t}{1-\cos t}=\frac{2\sin\frac{t}{2}\cos\frac{t}{2}}{2\sin^2\frac{t}{2}}=\cot\frac{t}{2}$.

**6.** $f'(x)=3x^2-12x+9=3(x-1)(x-3)$, zero at $x=1,3$. $f''(x)=6x-12$. At $x=1$: $f''=-6<0$, a **maximum**, $f(1)=1-6+9+1=5$. At $x=3$: $f''=6>0$, a **minimum**, $f(3)=27-54+27+1=1$. Sign of $f'$: positive for $x<1$, negative for $1<x<3$, positive for $x>3$. So $f$ is increasing on $(-\infty,1)$ and $(3,\infty)$ and decreasing on $(1,3)$. (The point of inflection is at $x=2$, where $f''=0$ and changes sign; $f(2)=3$.)

**7.** Let the parts be $x$ and $40-x$; $P=x(40-x)=40x-x^2$. $P'=40-2x=0\Rightarrow x=20$. $P''=-2<0$, so $x=20$ gives a maximum: the parts are 20 and 20 and the greatest product is 400. For $y=x^3$, $y''=6x$ is zero at $x=0$ and changes sign from negative to positive there, so $(0,0)$ is the point of inflection.
:::

## 12.19 Anti-derivatives

**Short questions (5 marks each)**

1. Evaluate $\int\frac{(1+x)^2}{x}\,dx$. <span class="marks">[5]</span>
2. Evaluate $\int xe^{x^2}\,dx$. <span class="marks">[5]</span>
3. Evaluate $\int x\sin x\,dx$. <span class="marks">[5]</span>
4. Evaluate $\int_0^{\pi/2}\frac{\cos x}{1+\sin x}\,dx$. <span class="marks">[5]</span>

**Long questions (8 marks)**

5. (i) Find the area bounded by $y=x^2$ and $y=2x$. (ii) Find the area under $y=\sin x$ from $x=0$ to $x=\pi$. <span class="marks">[5+3]</span>
6. Evaluate $\int\ln x\,dx$, and hence find $\int_1^e\ln x\,dx$. <span class="marks">[5+3]</span>

::: note Model answers
**1.** $\frac{(1+x)^2}{x}=\frac{1}{x}+2+x$. So the integral is $\ln|x|+2x+\frac{x^2}{2}+C$.

**2.** Put $u=x^2$, $du=2x\,dx$: $\int xe^{x^2}dx=\frac{1}{2}\int e^u\,du=\frac{1}{2}e^{x^2}+C$.

**3.** By parts with $u=x$, $dv=\sin x\,dx$: $\int x\sin x\,dx=-x\cos x+\int\cos x\,dx=-x\cos x+\sin x+C$.

**4.** Put $u=1+\sin x$, $du=\cos x\,dx$. Limits: $x=0\to u=1$; $x=\frac{\pi}{2}\to u=2$. $\int_1^2\frac{du}{u}=\ln2-\ln1=\ln2$.

**5.** (i) Intersections: $x^2=2x\Rightarrow x=0,2$. On $[0,2]$ the line is above the parabola: area $=\int_0^2(2x-x^2)dx=\left[x^2-\frac{x^3}{3}\right]_0^2=4-\frac{8}{3}=\frac{4}{3}$ square units. (ii) Area $=\int_0^\pi\sin x\,dx=[-\cos x]_0^\pi=1+1=2$ square units.

**6.** By parts with $u=\ln x$, $dv=dx$: $\int\ln x\,dx=x\ln x-\int x\cdot\frac{1}{x}\,dx=x\ln x-x+C$. Then $\int_1^e\ln x\,dx=[x\ln x-x]_1^e=(e-e)-(0-1)=1$.
:::

## 12.20 Computational Methods

**Short questions (5 marks each)**

1. Use the bisection method to locate the root of $x^3-x-1=0$ in $[1,2]$ after four iterations. <span class="marks">[5]</span>
2. Use the Newton–Raphson method to find $\sqrt{5}$ as the root of $x^2-5=0$, starting from $x_0=2$ (two iterations). <span class="marks">[5]</span>
3. Evaluate $\int_0^4x^2\,dx$ by the trapezoidal rule with $n=4$ and compare with the exact value. <span class="marks">[5]</span>
4. Evaluate $\int_0^1\frac{dx}{1+x^2}$ by Simpson's rule with $n=4$. <span class="marks">[5]</span>

**Long question (8 marks)**

5. Find a root of $x^3-2x-5=0$ near $x=2$ by Newton–Raphson, starting from $x_0=2$, and carry out two iterations. <span class="marks">[8]</span>

::: note Model answers
**1.** $f(1)=-1<0$, $f(2)=5>0$, so a root lies in $[1,2]$.

| Step | Interval | Midpoint $c$ | $f(c)$ | New interval |
|---|---|---|---|---|
| 1 | $[1,2]$ | 1.5 | $0.875>0$ | $[1,1.5]$ |
| 2 | $[1,1.5]$ | 1.25 | $-0.297<0$ | $[1.25,1.5]$ |
| 3 | $[1.25,1.5]$ | 1.375 | $0.225>0$ | $[1.25,1.375]$ |
| 4 | $[1.25,1.375]$ | 1.3125 | $-0.052<0$ | $[1.3125,1.375]$ |

The root lies in $(1.3125,1.375)$, so $x\approx1.34$ (the true root is $1.3247$).

**2.** $f(x)=x^2-5$, $f'(x)=2x$, $x_{n+1}=x_n-\frac{x_n^2-5}{2x_n}$. $x_1=2-\frac{4-5}{4}=2.25$. $x_2=2.25-\frac{5.0625-5}{4.5}=2.25-0.01389=2.23611$. So $\sqrt{5}\approx2.2361$.

**3.** $h=1$; $y$ values at $x=0,1,2,3,4$: $0,1,4,9,16$. $I\approx\frac{h}{2}[y_0+2(y_1+y_2+y_3)+y_4]=\frac{1}{2}[0+2(14)+16]=22$. Exact: $\frac{4^3}{3}=21.33$. The trapezoidal rule overestimates here because $x^2$ is convex.

**4.** $h=0.25$; $y=\frac{1}{1+x^2}$ at $0,0.25,0.5,0.75,1$: $1,\ 0.94118,\ 0.8,\ 0.64,\ 0.5$. Simpson: $\frac{h}{3}[y_0+4(y_1+y_3)+2y_2+y_4]=\frac{0.25}{3}[1+4(1.58118)+1.6+0.5]=0.083333\times9.42471=0.78539$. (Exact value $\frac{\pi}{4}=0.78540$.)

**5.** $f(x)=x^3-2x-5$, $f'(x)=3x^2-2$. At $x_0=2$: $f=8-4-5=-1$ and $f'=10$, so $x_1=2-\frac{-1}{10}=2.1$. At $x_1=2.1$: $f=9.261-4.2-5=0.061$ and $f'=13.23-2=11.23$, so $x_2=2.1-\frac{0.061}{11.23}=2.1-0.00543=2.09457$. The root is $\approx2.0946$.
:::

## 12.21 Mechanics

**Short questions (5 marks each)**

1. Two forces of 5 N and 12 N act at a point at right angles. Find their resultant and its direction relative to the 5 N force. <span class="marks">[5]</span>
2. Two forces of 3 N and 5 N act at a point with an angle of $60^\circ$ between them. Find the resultant. <span class="marks">[5]</span>
3. A particle moving at $10\ \text{m s}^{-1}$ is retarded uniformly at $2\ \text{m s}^{-2}$. Find the time to stop and the distance covered. <span class="marks">[5]</span>
4. A ball is thrown vertically upward at $30\ \text{m s}^{-1}$ ($g=10\ \text{m s}^{-2}$). Find the maximum height and the total time of flight. <span class="marks">[5]</span>
5. A body slides from rest down a smooth plane inclined at $30^\circ$ to the horizontal ($g=10\ \text{m s}^{-2}$). Find its acceleration, and its speed and distance after 4 s. <span class="marks">[5]</span>

**Long question (8 marks)**

6. A particle starts with a velocity of $4\ \text{m s}^{-1}$ and moves with a uniform acceleration of $2\ \text{m s}^{-2}$. Find (i) its velocity after 5 s, (ii) the distance covered in 5 s, (iii) the distance covered in the fifth second. <span class="marks">[2+3+3]</span>

::: note Model answers
**1.** $R=\sqrt{5^2+12^2}=13$ N. The angle with the 5 N force: $\tan\alpha=\frac{12}{5}$, so $\alpha=\tan^{-1}2.4\approx67.4^\circ$.

**2.** $R^2=P^2+Q^2+2PQ\cos\theta=9+25+2(3)(5)\cos60^\circ=34+15=49$, so $R=7$ N.

**3.** $v=u+at$: $0=10-2t\Rightarrow t=5$ s. Distance: $s=\frac{u^2}{2|a|}=\frac{100}{4}=25$ m (check: $ut+\frac{1}{2}at^2=50-25=25$).

**4.** Maximum height $h=\frac{u^2}{2g}=\frac{900}{20}=45$ m. Time to the top $=\frac{u}{g}=3$ s, so total time of flight $=6$ s.

**5.** $a=g\sin30^\circ=10\times\frac{1}{2}=5\ \text{m s}^{-2}$. After 4 s: $v=at=20\ \text{m s}^{-1}$ and $s=\frac{1}{2}at^2=\frac{1}{2}\times5\times16=40$ m.

**6.** (i) $v=u+at=4+2\times5=14\ \text{m s}^{-1}$.
(ii) $s=ut+\frac{1}{2}at^2=4(5)+\frac{1}{2}(2)(25)=20+25=45$ m.
(iii) Distance in the 5th second $=s_5-s_4$. $s_4=4(4)+\frac{1}{2}(2)(16)=32$ m, so the distance is $45-32=13$ m. (Formula check: $u+\frac{a}{2}(2n-1)=4+1\times9=13$.)
:::

## Chapter summary

- Write **every step** in Group B and C: formula, substitution, simplification, final answer.
- Algebra: $t_n=S_n-S_{n-1}$; G.P. trick $\frac{a}{r},a,ar$; $G^2=AH$; $\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta$; $|z_1z_2|=|z_1||z_2|$.
- Inverse circular: $\tan^{-1}a+\tan^{-1}b=\tan^{-1}\frac{a+b}{1-ab}$ (check $ab<1$).
- Trigonometric equations: $\sin x=\sin\alpha\Rightarrow n\pi+(-1)^n\alpha$; $\cos x=\cos\alpha\Rightarrow2n\pi\pm\alpha$; $a\cos x+b\sin x=R\cos(x-\alpha)$.
- Geometry: $d=\frac{|ax_1+by_1+c|}{\sqrt{a^2+b^2}}$; $\tan\theta=\frac{2\sqrt{h^2-ab}}{|a+b|}$; $l^2+m^2+n^2=1$.
- Vectors: collinear means one difference is a scalar multiple of the other; midpoint is $\frac{\mathbf{a}+\mathbf{b}}{2}$.
- Statistics: C.V. $=\frac{\sigma}{\bar x}\times100$; $S_k=\frac{\text{Mean}-\text{Mode}}{\sigma}$, mode $=3\,\text{median}-2\,\text{mean}$.
- Calculus: set $f'=0$, test with $f''$; Newton–Raphson $x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}$; area between curves $=\int(\text{upper}-\text{lower})\,dx$.

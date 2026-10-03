---
subject: Question Bank
grade: 12
unit: 12
title: "Mathematics: Unit-wise Subjective Question Bank"
hours: 0
area: Mathematics
---

Group B (eight questions of 5 marks) and Group C (three questions of 8 marks) carry
sixty-four of the seventy-five marks in NEB Grade 12 Mathematics. This chapter takes
the seventeen chapters of the Mathematics book in syllabus order. Every section gives
short-answer questions (the shape of a Group B question, usually split $2+3$ or
$1+2+2$), at least one long-answer question (the shape of a Group C question, split
$3+3+2$, $2+3+3$ or $4+2+2$), a complete model answer to each, and a list of what has
repeated.

::: key How to use a section
Attempt each question on paper *before* opening the model answer, and mark yourself
part by part, because the examiner does. In Mathematics a mark is earned by the
**formula or theorem quoted**, each **correct step**, and the **final answer with its
unit or its interval**. A correct answer with no working earns almost nothing in
Group B or C; a wrong answer with correct working earns most of the marks. Read the
"Most repeated" list at the end of each section last.
:::

::: caution What a year tag means here
**(NEB 2081)** is printed only on a question that we read in that year's board paper —
verified years are **2079, 2080, 2081 and 2082**, plus the **CDC model question 2080**
(tagged **(CDC model 2080)**). Where the printed wording depended on a figure we could
not reproduce, the data have been rebuilt and the question is untagged. Where a
printed item turned out to be unsolvable as recorded, the section says so and gives
the nearest corrected version. Untagged questions are original practice questions of
the same pattern. Every numerical answer was recomputed by computer algebra before
printing.
:::

## 12.1 Permutation and Combination

CDC allots **10 teaching hours** and the unit sits inside Algebra, which carries **20
of the 75 marks**. Counting appears as a Group A item (2081 Q2, 2082 Q1 and the CDC
model Q1), as a two-mark part of a Group B question (2080 Q13a, 2082 Q13a) and as a
three-mark part of a Group C question (CDC model Q20a).

| Result | Formula |
|---|---|
| Fundamental principle | $m$ ways then $n$ ways gives $m\times n$ ways |
| Permutation, all different | $P(n,r) = \dfrac{n!}{(n-r)!}$ |
| Not all different | $\dfrac{n!}{p!\,q!\,r!}$ for $p$, $q$, $r$ alike |
| Circular, all different | $(n-1)!$ |
| With repetition allowed | $n^{r}$ |
| Combination | $C(n,r) = \dfrac{n!}{r!\,(n-r)!}$ |
| Properties | $C(n,r)=C(n,n-r)$, $C(n,r)+C(n,r-1)=C(n+1,r)$ |
| Relation | $P(n,r) = r!\,C(n,r)$ |

**Short answer questions [5 marks each]**

1. (a) How many three-digit numbers can be formed from the digits $2,3,4,5,6,7$ (i) without repetition, (ii) with repetition allowed? [2] (b) Find $n$ if $P(n,4)=20\,P(n,2)$. [3] <span class="marks">[5]</span> (NEB 2080, part a)
2. (a) A committee is to be chosen from $a$ boys and $6$ girls and is to consist of $2$ boys and $3$ girls. If $120$ committees can be formed, find $a$. [2] (b) In how many ways can $7$ persons sit round a table if two particular persons must sit together? [3] <span class="marks">[5]</span> (NEB 2082, part a)
3. (a) Prove that $C(n,r)+C(n,r-1)=C(n+1,r)$. [3] (b) Find the number of arrangements of the letters of the word MATHEMATICS. [2] <span class="marks">[5]</span>
4. (a) In how many ways can $5$ boys and $3$ girls sit in a row so that no two girls sit together? [3] (b) A polygon has $54$ diagonals. Find the number of its sides. [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) The paper did not say whether digits may repeat, so both cases are answered.
(i) Without repetition: the hundreds place can be filled in $6$ ways, the tens in $5$, the units in $4$:
$$ 6\times5\times4 = 120 $$
(ii) With repetition each of the three places can be filled in $6$ ways:
$$ 6\times6\times6 = 216 $$
(b)
$$ n(n-1)(n-2)(n-3) = 20\,n(n-1) $$
Cancel $n(n-1)$, which is non-zero because $n\geq4$:
$$ (n-2)(n-3) = 20 \;\Rightarrow\; n^{2}-5n-14=0 \;\Rightarrow\; (n-7)(n+2)=0 $$
So $n=7$ (reject $n=-2$). **Check:** $P(7,4)=840$ and $20\,P(7,2)=20\times42=840$. ✓

**2.** (a) Boys can be chosen in $C(a,2)$ ways and girls in $C(6,3)=20$ ways, so
$$ C(a,2)\times C(6,3) = 120 \;\Rightarrow\; C(a,2)=6 \;\Rightarrow\; \frac{a(a-1)}{2}=6 $$
$$ a^{2}-a-12=0 \;\Rightarrow\; (a-4)(a+3)=0 \;\Rightarrow\; a=4 $$
(b) Tie the two particular persons together as **one unit**. There are then $6$ units to seat round the table, which can be done in $(6-1)! = 120$ ways. The two persons can swap places inside their unit in $2!$ ways:
$$ 120\times2 = 240 $$

**3.** (a) Write both terms with factorials:
$$ C(n,r)+C(n,r-1) = \frac{n!}{r!\,(n-r)!}+\frac{n!}{(r-1)!\,(n-r+1)!} $$
Take out the common factor $\dfrac{n!}{r!\,(n-r+1)!}$, using $(n-r+1)! = (n-r+1)(n-r)!$ and $r! = r\,(r-1)!$:
$$ = \frac{n!}{r!\,(n-r+1)!}\Big[(n-r+1)+r\Big] = \frac{n!\,(n+1)}{r!\,(n+1-r)!} $$
$$ = \frac{(n+1)!}{r!\,\big((n+1)-r\big)!} = C(n+1,r) $$
(b) MATHEMATICS has $11$ letters, in which M, A and T each occur twice:
$$ \frac{11!}{2!\,2!\,2!} = \frac{39\,916\,800}{8} = 4\,989\,600 $$

**4.** (a) First seat the $5$ boys in a row: $5! = 120$ ways. They leave $6$ gaps (one before, one after, four between). Put the three girls in **different** gaps, in order: $P(6,3)=120$ ways.
$$ 5!\times P(6,3) = 120\times120 = 14\,400 $$
(b) A polygon of $n$ sides has $C(n,2)-n = \dfrac{n(n-3)}{2}$ diagonals.
$$ \frac{n(n-3)}{2}=54 \;\Rightarrow\; n^{2}-3n-108=0 \;\Rightarrow\; (n-12)(n+9)=0 \;\Rightarrow\; n=12 $$
:::

**Long answer questions [8 marks each]**

1. (a) In how many ways can the letters of the word INTERVAL be arranged so that (i) all the vowels are always together, (ii) the relative positions of vowels and consonants are not changed, (iii) the vowels occupy only the odd positions? [3] (b) A committee of $5$ is to be chosen from $6$ men and $4$ women so that it has at least $2$ women. In how many ways can this be done? [3] (c) In how many ways can the letters of the word BANANA be arranged? [2] <span class="marks">[8]</span> (CDC model 2080, part a)

::: note Model answer — long
**1.** (a) INTERVAL has $8$ different letters: vowels I, E, A ($3$ of them) and consonants N, T, R, V, L ($5$ of them).
(i) Treat the three vowels as one block. Arrange $6$ objects (block + $5$ consonants) in $6!$ ways, and the vowels inside the block in $3!$ ways:
$$ 6!\times3! = 720\times6 = 4320 $$
(ii) If the positions of vowels and consonants are not to change, the vowels may only be rearranged among the three vowel positions and the consonants among the five consonant positions:
$$ 3!\times5! = 6\times120 = 720 $$
(iii) There are $4$ odd positions ($1,3,5,7$). Choose and arrange the three vowels in them in $P(4,3)=24$ ways; the five consonants fill the other five places in $5!=120$ ways:
$$ 24\times120 = 2880 $$
(b) "At least $2$ women" is easiest by subtraction from all committees. All committees: $C(10,5)=252$. Committees with no woman: $C(6,5)=6$. Committees with exactly one woman: $C(4,1)\times C(6,4)=4\times15=60$.
$$ 252-6-60 = 186 $$
(c) BANANA has $6$ letters with A three times and N twice:
$$ \frac{6!}{3!\,2!} = \frac{720}{12} = 60 $$
:::

::: tip Examiner's note — Permutation and Combination
Most repeated: **a committee or selection with a condition** (2082 Q13a, CDC Q20a); **arrangements of a word** with repeated or restricted letters; **$P(n,r)$ equations solved for $n$** (2080 Q13a style). Marks are lost by saying "arrangement" when the question says "selection", by forgetting to divide for repeated letters, and by not stating whether digits may repeat.
:::

## 12.2 Binomial Theorem

CDC allots **10 hours**. The unit supplies the **five one-mark recall parts** of Q12 (2079, 2081 and 2082 Q12 all open with binomial or series recall), a middle-term question (2079 Q12b, 2082 Q20a), a coefficient question (2080 Q13b, 2081 Q20a), and the approximation and $e^{x}$, $\log(1+x)$ expansions.

| Result | Formula |
|---|---|
| Theorem, positive integer $n$ | $(a+b)^{n} = \sum C(n,r)\,a^{n-r}b^{r}$ |
| General term | $T_{r+1} = C(n,r)\,a^{n-r}b^{r}$ |
| Middle term, $n$ even | $T_{n/2+1}$ |
| Middle terms, $n$ odd | $T_{(n+1)/2}$ and $T_{(n+3)/2}$ |
| Sum of coefficients of $(1+x)^{n}$ | $2^{n}$ |
| Any index, $-1<x<1$ | $(1+x)^{n}=1+nx+\frac{n(n-1)}{2!}x^{2}+\cdots$ |
| $e^{x}$ | $1+x+\frac{x^{2}}{2!}+\frac{x^{3}}{3!}+\cdots$ |
| $\log_e(1+x)$ | $x-\frac{x^{2}}{2}+\frac{x^{3}}{3}-\cdots$, $-1<x\leq1$ |

**Short answer questions [5 marks each]**

1. (a) Define binomial expansion. [1] (b) Find the middle term of $(2+3x)^{30}$. [2] (c) Find the sum of the $n$ binomial coefficients in the expansion of $(1+x)^{n}$ when $x=1$. [1] (d) What is meant by the argument of a complex number? [1] <span class="marks">[5]</span> (NEB 2079)
2. (a) If the middle term in the expansion of $\left(\frac{a}{2}+2\right)^{8}$ is $1120$, find the value of $a$. [2] (b) Prove that the coefficient of $x^{n}$ in $(1+x)^{2n}$ is twice the coefficient of $x^{n}$ in $(1+x)^{2n-1}$. [3] <span class="marks">[5]</span> (NEB 2082 Q20a; NEB 2081 Q20a)
3. (a) For what value of $r$ are the coefficients of $x^{r}$ and $x^{r+1}$ equal in the expansion of $(1+x)^{11}$? [3] (b) Expand $(1+x)^{-2}$ up to the term in $x^{3}$ and use it to find $(1.02)^{-2}$ approximately. [2] <span class="marks">[5]</span> (NEB 2080, part b)
4. (a) Write the expansions of $\log_e(1-x)$ for $-1<x<1$ and of $e^{x}$. [2] (b) Find the term independent of $x$ in $\left(2x^{2}-\dfrac{1}{x}\right)^{9}$. [3] <span class="marks">[5]</span> (NEB 2082, part of Q12)

::: note Model answers — short
**1.** (a) The **binomial expansion** is the formula that expresses a power $(a+b)^{n}$ of a binomial as a sum of terms of the form $C(n,r)a^{n-r}b^{r}$, for $r=0,1,\dots,n$.

(b) $n=30$ is even, so there is **one** middle term, $T_{16}$:
$$ T_{16} = C(30,15)\,(2)^{15}(3x)^{15} = C(30,15)\,2^{15}\,3^{15}\,x^{15} = C(30,15)\,6^{15}x^{15} $$
with $C(30,15)=155\,117\,520$.

(c) Put $x=1$: $(1+1)^{n} = C(n,0)+C(n,1)+\cdots+C(n,n)$, so the sum is $2^{n}$.

(d) If $z=x+iy=r(\cos\theta+i\sin\theta)$, then $\theta=\tan^{-1}(y/x)$, measured from the positive $x$-axis to the line joining the origin to the point $(x,y)$, is the **argument** of $z$, written $\arg z$.

**2.** (a) $n=8$, so the middle term is $T_{5}$:
$$ T_{5} = C(8,4)\Big(\frac{a}{2}\Big)^{4}(2)^{4} = 70\times\frac{a^{4}}{16}\times16 = 70a^{4} $$
$$ 70a^{4}=1120 \;\Rightarrow\; a^{4}=16 \;\Rightarrow\; a=\pm2 $$
(b) The coefficient of $x^{n}$ in $(1+x)^{2n}$ is $C(2n,n)$, and in $(1+x)^{2n-1}$ it is $C(2n-1,n)$. Dividing one by the other:
$$ \frac{C(2n,n)}{C(2n-1,n)} = \frac{(2n)!}{n!\,n!}\cdot\frac{n!\,(n-1)!}{(2n-1)!} = \frac{(2n)!}{(2n-1)!}\cdot\frac{(n-1)!}{n!} = 2n\cdot\frac{1}{n}=2 $$
So $C(2n,n)=2\,C(2n-1,n)$. ∎

**3.** (a) The coefficient of $x^{r}$ is $C(11,r)$ and of $x^{r+1}$ is $C(11,r+1)$. Since $C(n,p)=C(n,q)$ requires $p=q$ or $p+q=n$, and $r\neq r+1$,
$$ r+(r+1)=11 \;\Rightarrow\; r=5 $$
**Check:** $C(11,5)=C(11,6)=462$. ✓

(b) For any index, $(1+x)^{n}=1+nx+\dfrac{n(n-1)}{2!}x^{2}+\dfrac{n(n-1)(n-2)}{3!}x^{3}+\cdots$ with $n=-2$:
$$ (1+x)^{-2} = 1-2x+3x^{2}-4x^{3}+\cdots $$
Put $x=0.02$:
$$ (1.02)^{-2}\approx 1-0.04+0.0012-0.000032 = 0.961168 $$
(The exact value is $0.961169$.)

**4.** (a)
$$ \log_e(1-x) = -x-\frac{x^{2}}{2}-\frac{x^{3}}{3}-\frac{x^{4}}{4}-\cdots,\quad -1\leq x<1 $$
$$ e^{x} = 1+x+\frac{x^{2}}{2!}+\frac{x^{3}}{3!}+\cdots,\quad 2<e<3 $$
(b) $T_{r+1}=C(9,r)(2x^{2})^{9-r}\Big(-\dfrac1x\Big)^{r} = C(9,r)\,2^{9-r}(-1)^{r}\,x^{18-2r-r}$. The power of $x$ is $18-3r$, which is $0$ when $r=6$:
$$ T_{7}=C(9,6)\,2^{3}(-1)^{6} = 84\times8=672 $$
:::

**Long answer questions [8 marks each]**

1. (a) State the binomial theorem for a positive integral index and write its general term. [2] (b) If the coefficients of the $5$th, $6$th and $7$th terms of $(1+x)^{n}$ are in arithmetic progression, find $n$. [3] (c) Find the coefficient of $x^{4}$ in $\left(x+\dfrac{2}{x}\right)^{8}$, and the approximate value of $\sqrt{1.04}$ using the first three terms of the expansion. [3] <span class="marks">[8]</span>

::: note Model answer — long
**1.** (a) For a positive integer $n$,
$$ (a+b)^{n}=C(n,0)a^{n}+C(n,1)a^{n-1}b+C(n,2)a^{n-2}b^{2}+\cdots+C(n,n)b^{n} $$
and the general term, the $(r+1)$th, is $T_{r+1}=C(n,r)\,a^{n-r}b^{r}$.

(b) The $5$th, $6$th, $7$th coefficients are $C(n,4)$, $C(n,5)$, $C(n,6)$. In an A.P. the middle term is the mean of the other two:
$$ 2\,C(n,5) = C(n,4)+C(n,6) $$
Divide by $C(n,5)$ using $\dfrac{C(n,4)}{C(n,5)}=\dfrac{5}{n-4}$ and $\dfrac{C(n,6)}{C(n,5)}=\dfrac{n-5}{6}$:
$$ 2=\frac{5}{n-4}+\frac{n-5}{6} \;\Rightarrow\; 12(n-4)=30+(n-5)(n-4) $$
$$ n^{2}-21n+98=0 \;\Rightarrow\; (n-7)(n-14)=0 $$
So $n=7$ or $n=14$. **Check for $n=7$:** $C(7,4)=35$, $C(7,5)=21$, $C(7,6)=7$; $35,21,7$ is an A.P. with common difference $-14$. ✓

(c) $T_{r+1}=C(8,r)\,x^{8-r}\Big(\dfrac{2}{x}\Big)^{r} = C(8,r)\,2^{r}\,x^{8-2r}$. For $x^{4}$: $8-2r=4$, $r=2$:
$$ T_{3}=C(8,2)\,2^{2}x^{4}=28\times4\,x^{4}=112\,x^{4} $$
so the coefficient is $112$. Next, $\sqrt{1.04}=(1+0.04)^{1/2}$:
$$ (1+x)^{1/2}\approx1+\tfrac12x-\tfrac18x^{2} = 1+0.02-0.0002=1.0198 $$
(The exact value is $1.0198039\ldots$)
:::

::: tip Examiner's note — Binomial Theorem
Most repeated: **middle term** (2079, 2082), **coefficient comparison** (2080, 2081), the **five-part recall** (2079 Q12, 2081 Q12, 2082 Q12), and **expansion of $e^{x}$ or $\log(1\pm x)$**. A frequent loss: writing $T_{r}$ where $T_{r+1}$ is meant, and forgetting that for $\log(1-x)$ every sign is negative.
:::

## 12.3 Complex Numbers

CDC allots **8 hours**. De Moivre's theorem is the most repeated single theorem in Algebra: it was the subject of 2080 Q12 (five parts), 2081 Q13b and Q20b, 2082 Q12c, and CDC model Q13a.

| Result | Formula |
|---|---|
| Polar form | $z=r(\cos\theta+i\sin\theta)$, $r=\sqrt{x^{2}+y^{2}}$, $\theta=\tan^{-1}\frac{y}{x}$ (quadrant!) |
| Product / quotient | multiply moduli and **add** / divide moduli and **subtract** arguments |
| De Moivre | $[r(\cos\theta+i\sin\theta)]^{n}=r^{n}(\cos n\theta+i\sin n\theta)$ |
| $n$th roots | $r^{1/n}\Big[\cos\frac{\theta+2k\pi}{n}+i\sin\frac{\theta+2k\pi}{n}\Big]$, $k=0,\dots,n-1$ |
| Cube roots of unity | $1,\ \omega,\ \omega^{2}$ with $1+\omega+\omega^{2}=0$, $\omega^{3}=1$ |
| Euler's formula | $e^{i\theta}=\cos\theta+i\sin\theta$, so $e^{i\pi}+1=0$ |

**Short answer questions [5 marks each]**

1. For any positive integer $n$, $[r(\cos\theta+i\sin\theta)]^{n}=r^{n}[\cos n\theta+i\sin n\theta]$. (i) Name the theorem. [1] (ii) Write the statement when $n$ is replaced by $-n$. [1] (iii) What does $r$ represent? [1] (iv) What does $\theta$ represent? [1] (v) Write one application of the theorem. [1] <span class="marks">[5]</span> (NEB 2080)
2. The square roots of a complex number are $(\sqrt{3}+i)$ and $(-\sqrt{3}-i)$. (a) Find the complex number in rectangular form. [2] (b) Write it in polar form. [3] <span class="marks">[5]</span> (NEB 2081, part b)
3. Use De Moivre's theorem to find the square roots of $-(2+2\sqrt{3}\,i)$. <span class="marks">[5]</span> (NEB 2081 Q20b)
4. If $\omega$ is a complex cube root of unity, prove that (a) $1+\omega+\omega^{2}=0$, [2] (b) $(1-\omega+\omega^{2})(1+\omega-\omega^{2})=4$. [3] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (i) **De Moivre's theorem.**
(ii) $[r(\cos\theta+i\sin\theta)]^{-n}=r^{-n}[\cos n\theta-i\sin n\theta]$.
(iii) $r$ is the **modulus** of the complex number, $r=|z|=\sqrt{x^{2}+y^{2}}$, its distance from the origin on the Argand plane.
(iv) $\theta$ is the **argument** (amplitude) of the complex number, the angle its radius vector makes with the positive real axis.
(v) Finding powers and roots of complex numbers, for instance the $n$th roots of unity; also proving trigonometric identities for multiple angles.

**2.** (a) The complex number is the square of either root:
$$ z=(\sqrt{3}+i)^{2}=3+2\sqrt{3}\,i+i^{2}=2+2\sqrt{3}\,i $$
(b) $r=\sqrt{2^{2}+(2\sqrt{3})^{2}}=\sqrt{16}=4$ and $\tan\theta=\dfrac{2\sqrt{3}}{2}=\sqrt{3}$. The point $(2,2\sqrt{3})$ is in the **first quadrant**, so $\theta=\dfrac{\pi}{3}$:
$$ z=4\Big(\cos\frac{\pi}{3}+i\sin\frac{\pi}{3}\Big) $$
**Check:** square roots $2\big(\cos\frac{\pi}{6}+i\sin\frac{\pi}{6}\big)=\sqrt{3}+i$. ✓

**3.** Let $z=-2-2\sqrt{3}\,i$. Then $r=\sqrt{4+12}=4$ and $\tan\theta=\sqrt{3}$. The point $(-2,-2\sqrt{3})$ is in the **third quadrant**, so $\theta=\pi+\dfrac{\pi}{3}=\dfrac{4\pi}{3}$:
$$ z=4\Big(\cos\frac{4\pi}{3}+i\sin\frac{4\pi}{3}\Big) $$
By De Moivre's theorem for roots,
$$ z^{1/2}=4^{1/2}\Big[\cos\frac{4\pi/3+2k\pi}{2}+i\sin\frac{4\pi/3+2k\pi}{2}\Big],\quad k=0,1 $$
For $k=0$: $2\Big(\cos\dfrac{2\pi}{3}+i\sin\dfrac{2\pi}{3}\Big)=2\Big(-\dfrac12+\dfrac{\sqrt{3}}{2}i\Big)=-1+\sqrt{3}\,i$.
For $k=1$: $2\Big(\cos\dfrac{5\pi}{3}+i\sin\dfrac{5\pi}{3}\Big)=2\Big(\dfrac12-\dfrac{\sqrt{3}}{2}i\Big)=1-\sqrt{3}\,i$.
The square roots are $\pm(1-\sqrt{3}\,i)$. **Check:** $(1-\sqrt{3} i)^{2}=1-2\sqrt{3} i-3=-2-2\sqrt{3} i$. ✓

**4.** (a) The cube roots of unity satisfy $x^{3}-1=0$, that is $(x-1)(x^{2}+x+1)=0$. The non-real roots $\omega,\omega^{2}$ satisfy $x^{2}+x+1=0$, so $\omega^{2}+\omega+1=0$. ∎
(b) From (a), $1+\omega=-\omega^{2}$ and $1+\omega^{2}=-\omega$. Hence $1-\omega+\omega^{2}=(1+\omega^{2})-\omega=-2\omega$ and $1+\omega-\omega^{2}=(1+\omega)-\omega^{2}=-2\omega^{2}$:
$$ (-2\omega)(-2\omega^{2})=4\omega^{3}=4\times1=4 $$ ∎
:::

**Long answer questions [8 marks each]**

1. (a) Express $1+i\sqrt{3}$ in polar form and use De Moivre's theorem to find $(1+i\sqrt{3})^{6}$. [3] (b) Find the cube roots of $8i$. [3] (c) Show that $\omega$ and $\omega^{2}$ are the roots of $x^{2}+x+1=0$, where $\omega$ is a complex cube root of unity. [2] <span class="marks">[8]</span>

::: note Model answer — long
**1.** (a) $r=\sqrt{1+3}=2$ and $\tan\theta=\sqrt{3}$ with the point $(1,\sqrt{3})$ in the first quadrant, so $\theta=\dfrac{\pi}{3}$:
$$ 1+i\sqrt{3}=2\Big(\cos\frac{\pi}{3}+i\sin\frac{\pi}{3}\Big) $$
$$ (1+i\sqrt{3})^{6}=2^{6}\Big(\cos\frac{6\pi}{3}+i\sin\frac{6\pi}{3}\Big)=64(\cos2\pi+i\sin2\pi)=64 $$
(b) $8i=8\Big(\cos\dfrac{\pi}{2}+i\sin\dfrac{\pi}{2}\Big)$, so
$$ (8i)^{1/3}=2\Big[\cos\frac{\pi/2+2k\pi}{3}+i\sin\frac{\pi/2+2k\pi}{3}\Big],\quad k=0,1,2 $$
$k=0$: $2(\cos30^{\circ}+i\sin30^{\circ})=\sqrt{3}+i$.
$k=1$: $2(\cos150^{\circ}+i\sin150^{\circ})=-\sqrt{3}+i$.
$k=2$: $2(\cos270^{\circ}+i\sin270^{\circ})=-2i$.
**Check:** $(-2i)^{3}=-8i^{3}=8i$. ✓

(c) The cube roots of unity are the roots of $x^{3}=1$. Factorising, $x^{3}-1=(x-1)(x^{2}+x+1)=0$. The root $x=1$ comes from the first factor; the other two roots, $\omega=\dfrac{-1+i\sqrt{3}}{2}$ and $\omega^{2}=\dfrac{-1-i\sqrt{3}}{2}$, are the roots of $x^{2}+x+1=0$. Direct check: sum of roots $=\omega+\omega^{2}=-1$ and product $=\omega^{3}=1$, matching $x^{2}+x+1$. ∎
:::

::: tip Examiner's note — Complex Numbers
Most repeated: **square (or cube) roots by De Moivre** (2080, 2081 twice, CDC Q13a), **polar form from a given root** (2081), and **cube-roots-of-unity identities** (2079 Q1 MCQ). The commonest error is taking the wrong quadrant for $\theta$: always plot the point before writing $\tan^{-1}$.
:::

## 12.4 Sequence and Series

CDC allots **8 hours**. A proof by mathematical induction has appeared in **every verified year**: 2079 Q13a ($\sum n^{2}$), 2080 Q20b ($n!\geq 2^{n}$), 2081 Q20c, 2082 Q20b, CDC model Q20c. It is the nearest thing to a guaranteed Group B/C item in Algebra.

| Result | Formula |
|---|---|
| Sum of first $n$ natural numbers | $\sum n=\dfrac{n(n+1)}{2}$ |
| Sum of squares | $\sum n^{2}=\dfrac{n(n+1)(2n+1)}{6}$ |
| Sum of cubes | $\sum n^{3}=\Big[\dfrac{n(n+1)}{2}\Big]^{2}$ |
| Induction, step 1 | verify $P(1)$ (or the first value asked) |
| Induction, step 2 | assume $P(k)$, deduce $P(k+1)$ |
| Induction, step 3 | conclude "true for all $n$ by the principle of mathematical induction" |

**Short answer questions [5 marks each]**

1. (a) Prove by mathematical induction that $1^{2}+2^{2}+3^{2}+\cdots+n^{2}=\dfrac{n(n+1)(2n+1)}{6}$. [4] (b) Hence find the sum of the squares of the first $20$ natural numbers. [1] <span class="marks">[5]</span> (NEB 2079)
2. (a) Using mathematical induction, prove that $1+7+13+19+\cdots+(6n-5)=n(3n-2)$. [3] (b) Find $1\cdot2+2\cdot3+3\cdot4+\cdots+10\cdot11$. [2] <span class="marks">[5]</span> (NEB 2082, part b)
3. Use mathematical induction to prove that $n!\geq2^{n}$ for $n\geq4$. <span class="marks">[5]</span> (NEB 2080)
4. (a) Show that the sum of the cubes of the first $n$ natural numbers equals the square of their sum. [3] (b) Find $1^{3}+2^{3}+\cdots+15^{3}$. [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) Let $P(n):\ 1^{2}+2^{2}+\cdots+n^{2}=\dfrac{n(n+1)(2n+1)}{6}$.
*Step 1.* For $n=1$: LHS $=1$, RHS $=\dfrac{1\cdot2\cdot3}{6}=1$. So $P(1)$ is true.
*Step 2.* Assume $P(k)$ is true: $1^{2}+\cdots+k^{2}=\dfrac{k(k+1)(2k+1)}{6}$. Add $(k+1)^{2}$ to both sides:
$$ 1^{2}+\cdots+k^{2}+(k+1)^{2}=\frac{k(k+1)(2k+1)}{6}+(k+1)^{2} $$
$$ =\frac{(k+1)\big[k(2k+1)+6(k+1)\big]}{6}=\frac{(k+1)(2k^{2}+7k+6)}{6} $$
$$ =\frac{(k+1)(k+2)(2k+3)}{6}=\frac{(k+1)\big((k+1)+1\big)\big(2(k+1)+1\big)}{6} $$
which is $P(k+1)$.
*Step 3.* $P(1)$ is true and $P(k)\Rightarrow P(k+1)$, so $P(n)$ is true for every natural number $n$. ∎
(b)
$$ \sum_{1}^{20}n^{2}=\frac{20\times21\times41}{6}=2870 $$

**2.** (a) Let $P(n):\ 1+7+13+\cdots+(6n-5)=n(3n-2)$.
For $n=1$: LHS $=6(1)-5=1$, RHS $=1(3-2)=1$. True.
Assume $P(k)$. Add the $(k+1)$th term, $6(k+1)-5=6k+1$:
$$ k(3k-2)+(6k+1)=3k^{2}+4k+1=(3k+1)(k+1)=(k+1)\big(3(k+1)-2\big) $$
which is $P(k+1)$. By the principle of mathematical induction the result holds for all $n$. ∎
(b) The $r$th term is $r(r+1)=r^{2}+r$, so
$$ \sum_{r=1}^{10}r(r+1)=\frac{10\cdot11\cdot21}{6}+\frac{10\cdot11}{2}=385+55=440 $$
**Check:** the general formula $\dfrac{n(n+1)(n+2)}{3}$ gives $\dfrac{10\cdot11\cdot12}{3}=440$. ✓

**3.** Let $P(n):\ n!\geq2^{n}$, for $n\geq4$.
*Step 1.* For $n=4$: $4!=24$ and $2^{4}=16$; $24\geq16$, so $P(4)$ is true.
*Step 2.* Assume $P(k)$: $k!\geq2^{k}$ for some $k\geq4$. Then
$$ (k+1)!=(k+1)\,k!\geq(k+1)\,2^{k} $$
Since $k\geq4$, $k+1\geq5>2$, so $(k+1)\,2^{k}>2\cdot2^{k}=2^{k+1}$. Hence $(k+1)!\geq2^{k+1}$, which is $P(k+1)$.
*Step 3.* By induction, $n!\geq2^{n}$ for all $n\geq4$. ∎
Note that the base case is $n=4$, **not** $n=1$: the inequality is false for $n=3$ ($6<8$).

**4.** (a) The sum of the first $n$ natural numbers is $S=\dfrac{n(n+1)}{2}$, so $S^{2}=\dfrac{n^{2}(n+1)^{2}}{4}$. Prove $\sum k^{3}=S^{2}$ by induction. For $n=1$: $1=\Big(\dfrac{1\cdot2}{2}\Big)^{2}=1$. Assume it for $k$ and add $(k+1)^{3}$:
$$ \frac{k^{2}(k+1)^{2}}{4}+(k+1)^{3}=\frac{(k+1)^{2}\big[k^{2}+4(k+1)\big]}{4}=\frac{(k+1)^{2}(k+2)^{2}}{4} $$
which is the formula for $n=k+1$. ∎ So $1^{3}+2^{3}+\cdots+n^{3}=(1+2+\cdots+n)^{2}$.
(b) $n=15$: $\Big(\dfrac{15\times16}{2}\Big)^{2}=120^{2}=14\,400$.
:::

::: caution A printed item that cannot be proved as recorded
The copy of the 2081 paper we read asks for a proof, by induction, that $n!<2^{n}$ (Q20c). That inequality is true only for $n=1,2,3$ ($1<2$, $2<4$, $6<8$) and false from $n=4$ onwards ($24>16$), where the truth is the opposite inequality $n!\geq2^{n}$ — the statement proved in the 2080 paper (short question 3 above). If you meet an induction inequality, **test $n=1$, $2$, $3$, $4$ first** to find where it starts to hold; the base case of your proof must be that value.
:::

**Long answer questions [8 marks each]**

1. (a) Prove by the method of induction that $1\cdot3+2\cdot4+3\cdot5+\cdots+n(n+2)=\dfrac{n(n+1)(2n+7)}{6}$. [3] (b) If $x=\dfrac{y}{1!}+\dfrac{y^{2}}{2!}+\dfrac{y^{3}}{3!}+\cdots$, show that $y=x-\dfrac{x^{2}}{2}+\dfrac{x^{3}}{3}-\cdots$. [2] (c) Prove by induction that $n(n+1)(n+2)$ is divisible by $6$ for every natural number $n$. [3] <span class="marks">[8]</span> (CDC model 2080 part a-type; NEB 2080 part b)

::: note Model answer — long
**1.** (a) Let $P(n)$ be the statement. For $n=1$: LHS $=1\cdot3=3$; RHS $=\dfrac{1\cdot2\cdot9}{6}=3$. True.
Assume $P(k)$ and add the next term $(k+1)(k+3)$:
$$ \frac{k(k+1)(2k+7)}{6}+(k+1)(k+3)=\frac{(k+1)\big[k(2k+7)+6(k+3)\big]}{6}=\frac{(k+1)(2k^{2}+13k+18)}{6} $$
$$ =\frac{(k+1)(k+2)(2k+9)}{6}=\frac{(k+1)\big((k+1)+1\big)\big(2(k+1)+7\big)}{6} $$
which is $P(k+1)$. By induction the result holds for all $n$. ∎

(b) The series on the right is the expansion of $e^{y}-1$, so $x=e^{y}-1$, that is $1+x=e^{y}$. Taking natural logarithms, $y=\log_e(1+x)$, and expanding,
$$ y=x-\frac{x^{2}}{2}+\frac{x^{3}}{3}-\cdots $$ ∎

(c) $P(n)$: $n(n+1)(n+2)$ is a multiple of $6$. For $n=1$: $1\cdot2\cdot3=6$. True. Assume $k(k+1)(k+2)=6m$ for an integer $m$. Then
$$ (k+1)(k+2)(k+3)=k(k+1)(k+2)+3(k+1)(k+2)=6m+3(k+1)(k+2) $$
Of two consecutive integers $k+1$ and $k+2$, one is even, so $(k+1)(k+2)=2q$ and the expression equals $6m+6q=6(m+q)$, a multiple of $6$. This is $P(k+1)$. ∎
:::

::: tip Examiner's note — Sequence and Series
Most repeated: **an induction proof of an identity** (2079, 2082, CDC) or **of an inequality** (2080, 2081). Write the three steps with their labels; the examiner's scheme gives a mark each for the base case, the assumption and the inductive step. The mark most often lost is the closing sentence.
:::

## 12.5 Matrix Based System of Linear Equations

CDC allots **8 hours**. Every verified paper sets one full system of three equations: 2079 Q20 (foods, Group C), 2080 Q20c (Cramer, Group C), 2081 Q13 (row-equivalent, Group B), 2082 Q20c (matrix method, Group C) — and the Group A item "nature of a system" or "eliminate $x$".

| Method | When to use |
|---|---|
| Cramer's rule | $D\neq0$; needs four $3\times3$ determinants |
| Row-equivalent (Gauss) | always works; also shows no solution / infinitely many |
| Inverse matrix, $X=A^{-1}B$ | the determinant of $A$ is non-zero; slow by hand but **required** when the question says "by matrix method" with a cost or price part |
| Nature | zero row with non-zero constant $\Rightarrow$ no solution; zero row with zero constant $\Rightarrow$ infinitely many |

**Short answer questions [5 marks each]**

1. Use Cramer's rule to solve $2x+y=4$, $3y-z=3$, $2x+3z=11$. <span class="marks">[5]</span> (NEB 2080, part c, here with 5 marks)
2. Use the row-equivalent matrix method to solve $2x+3y+5z=23$, $3x-3y+8z=21$, $x+4y-z=6$. <span class="marks">[5]</span> (NEB 2081)
3. Solve $7x-2y=18$, $3x+7z=33$, $x+y+z=12$ by the matrix method. <span class="marks">[5]</span> (NEB 2082, part c, here with 5 marks)
4. (a) Discuss the nature of the solution of $x+y+z=3$, $2x+2y+2z=6$, $x-y+z=1$. [3] (b) Show that $x+y=2$, $x+y=3$ has no solution, and say what the row-reduced matrix looks like. [2] <span class="marks">[5]</span>

```figure caption="Short question 1, Cramer's rule. The coefficient determinant $D$ and $D_x$ (the $x$-column replaced by the constants $4, 3, 11$)."
fig = mateq(["$D =$", ("det", [["$2$","$1$","$0$"],["$0$","$3$","$-1$"],["$2$","$0$","$3$"]]),
             "$D_x =$", ("det", [["$4$","$1$","$0$"],["$3$","$3$","$-1$"],["$11$","$0$","$3$"]])],
            fontsize=11, colw=0.5, scale=0.6)
```

```figure caption="Short question 1, continued: $D_y$ (the $y$-column replaced) and $D_z$ (the $z$-column replaced)."
fig = mateq(["$D_y =$", ("det", [["$2$","$4$","$0$"],["$0$","$3$","$-1$"],["$2$","$11$","$3$"]]),
             "$D_z =$", ("det", [["$2$","$1$","$4$"],["$0$","$3$","$3$"],["$2$","$0$","$11$"]])],
            fontsize=11, colw=0.5, scale=0.6)
```

::: note Model answers — short
**1.** Expand each determinant along its first row (the four determinants are drawn above):
$$ D=2(9-0)-1(0+2)+0=16 $$
$$ D_x=4(9-0)-1(9+11)+0=36-20=16 $$
$$ D_y=2(9+11)-4(0+2)+0=40-8=32 $$
$$ D_z=2(33-0)-1(0-6)+4(0-6)=66+6-24=48 $$
Since $D\neq0$ the solution is unique:
$$ x=\frac{D_x}{D}=1,\qquad y=\frac{D_y}{D}=2,\qquad z=\frac{D_z}{D}=3 $$
**Check:** $2(1)+2=4$ ✓, $3(2)-3=3$ ✓, $2(1)+3(3)=11$ ✓.

**2.** Write the augmented matrix and use row operations; the figure shows the stages.
*Stage 1.* Interchange $R_1\leftrightarrow R_3$ so that the pivot is $1$.
*Stage 2.* $R_2\to R_2-3R_1$ and $R_3\to R_3-2R_1$ to clear the first column.
*Stage 3.* $R_2\to R_2-3R_3$ to clear the second column of the last row.

```figure caption="Short question 2: the augmented matrix reduced to triangular (echelon) form. Stage 1 swaps rows 1 and 3; stage 2 clears column 1; stage 3 clears column 2 below the pivot."
fig = mateq([[["$2$","$3$","$5$","$23$"],["$3$","$-3$","$8$","$21$"],["$1$","$4$","$-1$","$6$"]], "→",
             [["$1$","$4$","$-1$","$6$"],["$0$","$-15$","$11$","$3$"],["$0$","$-5$","$7$","$11$"]], "→",
             [["$1$","$4$","$-1$","$6$"],["$0$","$-5$","$7$","$11$"],["$0$","$0$","$-10$","$-30$"]]],
            fontsize=10, colw=0.72, scale=0.46)
```

In the stage-3 matrix (rows reordered so that the pivots descend), the last row says $-10z=-30$, so $z=3$. The middle row says $-5y+7z=11$, so $-5y=11-21=-10$ and $y=2$. The first row says $x+4y-z=6$, so $x=6-8+3=1$.
$$ x=1,\qquad y=2,\qquad z=3 $$
**Check in the original:** $2(1)+3(2)+5(3)=23$ ✓; $3(1)-3(2)+8(3)=21$ ✓; $1+8-3=6$ ✓.

**3.** The equations in full are $7x-2y+0z=18$, $3x+0y+7z=33$, $x+y+z=12$. Interchange $R_1\leftrightarrow R_3$ first, then $R_2\to R_2-3R_1$ and $R_3\to R_3-7R_1$:
$$ x+y+z=12,\qquad -3y+4z=-3,\qquad -9y-7z=-66 $$
Now $R_3\to R_3-3R_2$ gives $-19z=-57$, so $z=3$. Then $-3y+12=-3$ gives $y=5$, and $x=12-5-3=4$.
$$ x=4,\qquad y=5,\qquad z=3 $$
**Check:** $7(4)-2(5)=18$ ✓; $3(4)+7(3)=33$ ✓; $4+5+3=12$ ✓.

**4.** (a) Subtract $2\times$ the first equation from the second: $R_2\to R_2-2R_1$ gives $0x+0y+0z=0$, a **zero row with zero constant**. The system reduces to two equations in three unknowns:
$$ x+y+z=3,\qquad x-y+z=1 $$
Subtracting, $2y=2$ so $y=1$, and $x+z=2$. Putting $x=t$ gives $z=2-t$: the solutions are $(t,\,1,\,2-t)$ for every real $t$. The system is **consistent with infinitely many solutions**; this is the situation "$0\times z=0$" of the 2079 Group A item.
(b) Subtracting the equations gives $0=1$, which is impossible: the row-reduced augmented matrix has a row of zeros in the coefficient columns but the constant $1$ in the last column, a zero row with a **non-zero** constant. The system is **inconsistent — no solution**: two parallel lines never meet.
:::

**Long answer questions [8 marks each]**

1. A mixture is to be prepared from three foods A, B and C, which contain the nutrients P, Q and R as shown. The mixture must contain $30$ units of P, $36$ units of Q and $30$ units of R. (a) Express the information in equation form. [1] (b) Solve the equations by the matrix (inverse) method. [5] (c) If the cost per kg of the foods A, B and C is Rs. $40$, Rs. $60$ and Rs. $80$, find the total cost of the mixture. [2] <span class="marks">[8]</span> (NEB 2079)

| Food | P | Q | R |
|---|---|---|---|
| A | 2 | 2 | 4 |
| B | 3 | 5 | 0 |
| C | 4 | 3 | 5 |

```figure caption="Long question 1. The matrix equation $AX=B$ for the foods problem (rows are the nutrients P, Q, R; columns are the foods A, B, C)."
fig = mateq(["$A =$", [["$2$","$3$","$4$"],["$2$","$5$","$3$"],["$4$","$0$","$5$"]],
             "$X =$", [["$x$"],["$y$"],["$z$"]], "$B =$", [["$30$"],["$36$"],["$30$"]]],
            fontsize=11, colw=0.5, scale=0.6)
```

```figure caption="Long question 1, continued. The adjoint of $A$ is the transpose of its matrix of cofactors; $A^{-1}$ is the adjoint divided by $|A|=-24$."
fig = mateq(["$\\mathrm{adj}\\,A =$", [["$25$","$-15$","$-11$"],["$2$","$-6$","$2$"],["$-20$","$12$","$4$"]]],
            fontsize=11, colw=0.64, scale=0.62)
```

::: note Model answer — long
**1.** (a) Let $x$, $y$, $z$ kg of A, B, C be used. Counting each nutrient:
$$ 2x+3y+4z=30 \quad(\text{P}) $$
$$ 2x+5y+3z=36 \quad(\text{Q}) $$
$$ 4x+0y+5z=30 \quad(\text{R}) $$
(b) In matrix form $AX=B$, with $A$, $X$ and $B$ as in the first figure. Then $X=A^{-1}B$ provided $|A|\neq0$.
Determinant, expanding along the first row:
$$ |A|=2(25-0)-3(10-12)+4(0-20)=50+6-80=-24\neq0 $$
Cofactors, $C_{ij}=(-1)^{i+j}M_{ij}$:
$$ C_{11}=25,\quad C_{12}=-(10-12)=2,\quad C_{13}=0-20=-20 $$
$$ C_{21}=-(15-0)=-15,\quad C_{22}=10-16=-6,\quad C_{23}=-(0-12)=12 $$
$$ C_{31}=9-20=-11,\quad C_{32}=-(6-8)=2,\quad C_{33}=10-6=4 $$
The adjoint is the transpose of the cofactor matrix (second figure) and $A^{-1}=\dfrac{1}{|A|}\,\text{adj}\,A$, so $X=A^{-1}B=-\dfrac{1}{24}\,(\text{adj}\,A)\,B$. Multiply the adjoint into $B$ row by row:
$$ \text{row 1: } 25(30)-15(36)-11(30)=750-540-330=-120 $$
$$ \text{row 2: } 2(30)-6(36)+2(30)=60-216+60=-96 $$
$$ \text{row 3: } -20(30)+12(36)+4(30)=-600+432+120=-48 $$
Dividing each by $-24$:
$$ x=5,\qquad y=4,\qquad z=2 $$
So the mixture uses $5$ kg of A, $4$ kg of B and $2$ kg of C. **Check:** P: $10+12+8=30$ ✓; Q: $10+20+6=36$ ✓; R: $20+0+10=30$ ✓.

(c) Total cost $=40x+60y+80z$ (the product of the price row and the solution column):
$$ 40(5)+60(4)+80(2)=200+240+160=\text{Rs. }600 $$
:::

::: tip Examiner's note — Matrix Based System of Linear Equations
Most repeated: a **three-equation system with a context** (2079 foods, CDC-style), **Cramer's rule** (2080, and the 2082 MCQ for $y$), **row-equivalent method** (2081 Q13). State the method asked for: "by Cramer's rule" earns no marks if you use elimination. Show $D$ (or $|A|$) and say $D\neq0$ before dividing.
:::

## 12.6 Properties of a Triangle

CDC allots **8 hours**, and the grid footnote guarantees at least one Group A item from Trigonometry, Analytic Geometry and Vector each year. The half-angle formulae appeared as MCQs in 2081 Q3 and 2082 Q3 and as proofs in 2081 Q14a and Q15a; the sine law is proved in 2079 Q14b (by vectors) and used in 2082 Q21b.

| Result | Formula |
|---|---|
| Sine law | $\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}=2R$ |
| Cosine law | $\cos A=\dfrac{b^{2}+c^{2}-a^{2}}{2bc}$ |
| Projection law | $a=b\cos C+c\cos B$ |
| Tangent law | $\tan\dfrac{A-B}{2}=\dfrac{a-b}{a+b}\cot\dfrac{C}{2}$ |
| Half-angle, sine | $\sin^{2}\dfrac{A}{2}=\dfrac{(s-b)(s-c)}{bc}$ |
| Half-angle, cosine | $\cos^{2}\dfrac{A}{2}=\dfrac{s(s-a)}{bc}$ |
| Area | $\Delta=\sqrt{s(s-a)(s-b)(s-c)}$ |

**Short answer questions [5 marks each]**

1. (a) In any triangle $PQR$, if $p\sin^{2}\dfrac{R}{2}+r\sin^{2}\dfrac{P}{2}=\dfrac{q}{2}$, prove that the sides $p$, $q$, $r$ are in arithmetic progression. [3] (b) Prove the projection law $b\cos C+c\cos B=a$. [2] <span class="marks">[5]</span> (NEB 2081, part a)
2. (a) Show that $2\Big(a\sin^{2}\dfrac{C}{2}+c\sin^{2}\dfrac{A}{2}\Big)$ is less than the perimeter of triangle $ABC$. [3] (b) Prove that $\cos^{2}\dfrac{A}{2}=\dfrac{s(s-a)}{bc}$. [2] <span class="marks">[5]</span> (NEB 2081, part a)
3. (a) If the cosines of two angles of a triangle are proportional to the opposite sides, show that it is isosceles. [2] (b) Prove the tangent law $\tan\dfrac{A-B}{2}=\dfrac{a-b}{a+b}\cot\dfrac{C}{2}$. [3] <span class="marks">[5]</span> (NEB 2082, part b)
4. (a) In triangle $ABC$, if $a\cos A=b\cos B$, show that the triangle is isosceles or right-angled. [3] (b) Prove that $a(\sin B-\sin C)+b(\sin C-\sin A)+c(\sin A-\sin B)=0$. [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) In triangle $PQR$ with sides $p,q,r$ opposite $P,Q,R$, the half-angle formulae are
$$ \sin^{2}\frac{R}{2}=\frac{(s-p)(s-q)}{pq},\qquad \sin^{2}\frac{P}{2}=\frac{(s-q)(s-r)}{qr} $$
Substituting,
$$ p\cdot\frac{(s-p)(s-q)}{pq}+r\cdot\frac{(s-q)(s-r)}{qr}=\frac{s-q}{q}\big[(s-p)+(s-r)\big] $$
Since $(s-p)+(s-r)=2s-p-r=q$, the left-hand side is $\dfrac{s-q}{q}\cdot q=s-q$. Given that it equals $\dfrac{q}{2}$:
$$ s-q=\frac{q}{2}\;\Rightarrow\; s=\frac{3q}{2}\;\Rightarrow\; p+q+r=3q\;\Rightarrow\; p+r=2q $$
so $p,\,q,\,r$ are in A.P. ∎
(b) By the sine law $a=2R\sin A$, $b=2R\sin B$, $c=2R\sin C$. Then
$$ b\cos C+c\cos B=2R(\sin B\cos C+\cos B\sin C)=2R\sin(B+C) $$
$$ =2R\sin(180^{\circ}-A)=2R\sin A=a $$ ∎

**2.** (a) By the half-angle formula, $\sin^{2}\dfrac{C}{2}=\dfrac{(s-a)(s-b)}{ab}$ and $\sin^{2}\dfrac{A}{2}=\dfrac{(s-b)(s-c)}{bc}$. So
$$ a\sin^{2}\frac{C}{2}+c\sin^{2}\frac{A}{2}=\frac{(s-a)(s-b)}{b}+\frac{(s-b)(s-c)}{b}=\frac{s-b}{b}\big[(s-a)+(s-c)\big]=s-b $$
because $(s-a)+(s-c)=b$. Hence
$$ 2\Big(a\sin^{2}\frac{C}{2}+c\sin^{2}\frac{A}{2}\Big)=2(s-b)=a+c-b $$
and $a+c-b<a+b+c$ (the perimeter) because $b>0$. ∎ (In fact it is smaller by exactly $2b$.)
(b) From the cosine law, $\cos A=\dfrac{b^{2}+c^{2}-a^{2}}{2bc}$, and $2\cos^{2}\dfrac{A}{2}=1+\cos A$:
$$ 2\cos^{2}\frac{A}{2}=\frac{2bc+b^{2}+c^{2}-a^{2}}{2bc}=\frac{(b+c)^{2}-a^{2}}{2bc}=\frac{(b+c-a)(b+c+a)}{2bc} $$
With $b+c+a=2s$ and $b+c-a=2(s-a)$ this is $\dfrac{4s(s-a)}{2bc}$, so $\cos^{2}\dfrac{A}{2}=\dfrac{s(s-a)}{bc}$. ∎

**3.** (a) "Cosines proportional to the opposite sides" means $\dfrac{\cos A}{a}=\dfrac{\cos B}{b}$. By the sine law $a=2R\sin A$ and $b=2R\sin B$, so
$$ \frac{\cos A}{\sin A}=\frac{\cos B}{\sin B}\;\Rightarrow\;\cot A=\cot B\;\Rightarrow\;A=B $$
since $A,B$ lie between $0^{\circ}$ and $180^{\circ}$, where cotangent is one-to-one. Equal angles $A=B$ mean equal opposite sides $a=b$: the triangle is isosceles. ∎
(b) By the sine law $a=2R\sin A$, $b=2R\sin B$:
$$ \frac{a-b}{a+b}=\frac{\sin A-\sin B}{\sin A+\sin B}=\frac{2\cos\frac{A+B}{2}\sin\frac{A-B}{2}}{2\sin\frac{A+B}{2}\cos\frac{A-B}{2}}=\cot\frac{A+B}{2}\tan\frac{A-B}{2} $$
Since $A+B=180^{\circ}-C$, $\cot\dfrac{A+B}{2}=\tan\dfrac{C}{2}$. Therefore $\dfrac{a-b}{a+b}=\tan\dfrac{C}{2}\tan\dfrac{A-B}{2}$, that is
$$ \tan\frac{A-B}{2}=\frac{a-b}{a+b}\cot\frac{C}{2} $$ ∎

**4.** (a) By the sine law, $a\cos A=b\cos B$ becomes $\sin A\cos A=\sin B\cos B$, that is $\sin2A=\sin2B$. Two angles have equal sines when they are equal or supplementary:
$$ 2A=2B\;\Rightarrow\;A=B\quad\text{or}\quad 2A=180^{\circ}-2B\;\Rightarrow\;A+B=90^{\circ} $$
In the first case the triangle is isosceles ($a=b$); in the second $C=90^{\circ}$, so it is right-angled. ∎
(b) Let $a=k\sin A$, $b=k\sin B$, $c=k\sin C$ ($k=2R$). Then the expression is
$$ k\big[\sin A\sin B-\sin A\sin C+\sin B\sin C-\sin B\sin A+\sin C\sin A-\sin C\sin B\big]=0 $$
because the six terms cancel in pairs. ∎
:::

**Long answer questions [8 marks each]**

1. (a) Prove the cosine law $a^{2}=b^{2}+c^{2}-2bc\cos A$ by placing the triangle on coordinate axes. [3] (b) If $a=7$, $b=8$, $c=9$, find $\cos A$ and the angle $A$. [2] (c) Prove that $a(b\cos C-c\cos B)=b^{2}-c^{2}$. [3] <span class="marks">[8]</span>

::: note Model answer — long
**1.** (a) Place vertex $A$ at the origin and $AB$ along the positive $x$-axis, so $B=(c,0)$. Vertex $C$ has coordinates $(b\cos A,\ b\sin A)$, since $AC=b$ makes angle $A$ with $AB$. By the distance formula,
$$ a^{2}=BC^{2}=(b\cos A-c)^{2}+(b\sin A-0)^{2} $$
$$ =b^{2}\cos^{2}A-2bc\cos A+c^{2}+b^{2}\sin^{2}A=b^{2}+c^{2}-2bc\cos A $$
using $\cos^{2}A+\sin^{2}A=1$. ∎
(b)
$$ \cos A=\frac{b^{2}+c^{2}-a^{2}}{2bc}=\frac{64+81-49}{2\times8\times9}=\frac{96}{144}=\frac{2}{3} $$
$$ A=\cos^{-1}\frac{2}{3}=48.19^{\circ} $$
(c) By the cosine law, $\cos C=\dfrac{a^{2}+b^{2}-c^{2}}{2ab}$ and $\cos B=\dfrac{a^{2}+c^{2}-b^{2}}{2ac}$. So
$$ b\cos C=\frac{a^{2}+b^{2}-c^{2}}{2a},\qquad c\cos B=\frac{a^{2}+c^{2}-b^{2}}{2a} $$
$$ b\cos C-c\cos B=\frac{(a^{2}+b^{2}-c^{2})-(a^{2}+c^{2}-b^{2})}{2a}=\frac{2b^{2}-2c^{2}}{2a}=\frac{b^{2}-c^{2}}{a} $$
Multiplying by $a$ gives $a(b\cos C-c\cos B)=b^{2}-c^{2}$. ∎
:::

::: tip Examiner's note — Properties of a Triangle
Most repeated: a **half-angle proof of an "in A.P." or an inequality** (2081 twice), **the projection/sine/cosine law derived**, and a **"show that it is isosceles"** argument (2082). The method is the same each time: convert everything to sines with $a=2R\sin A$, or to half-angle formulae in $s$, then simplify. State which law you start from.
:::

## 12.7 Solution of Triangles

CDC allots only **4 hours**, but solving a triangle is a standard part of a Group C question (2081 Q21a) and supplies Group A items. Decide first which law to use: **two angles and a side** — sine law; **three sides** or **two sides and the included angle** — cosine law; **two sides and a non-included angle** — sine law, and check for *two* solutions.

| Given | Method |
|---|---|
| SSS | cosine law for each angle, or one angle then sine law |
| SAS | cosine law for the third side, then sine law (or tangent law) |
| ASA / AAS | third angle by subtraction, then sine law |
| SSA | sine law for $\sin B$; the ambiguous case gives $B$ and $180^{\circ}-B$ |

::: caution The 2081 item as recorded cannot be solved
In the copy of the 2081 paper we read, Q21a gives $a=3+\sqrt{3}\approx4.73$, $b=2$, $c=\sqrt{3}\approx1.73$. Here $b+c\approx3.73<a$, which violates the triangle inequality, so no such triangle exists; the printed data were presumably misread or misprinted. The question is therefore not reproduced below. **Before solving any triangle, check that the largest side is less than the sum of the other two.**
:::

**Short answer questions [5 marks each]**

1. Solve the triangle in which $a=\sqrt{3}+1$, $b=\sqrt{3}-1$ and $C=60^{\circ}$, using the tangent law. <span class="marks">[5]</span>
2. Solve the triangle with sides $a=7$, $b=8$, $c=9$. <span class="marks">[5]</span>
3. Solve the triangle in which $A=60^{\circ}$, $B=45^{\circ}$ and $a=12$. <span class="marks">[5]</span>
4. In a triangle $a=8$, $b=10$ and $A=30^{\circ}$. Show that two triangles are possible and solve both. <span class="marks">[5]</span>

::: note Model answers — short
**1.** Tangent law:
$$ \tan\frac{A-B}{2}=\frac{a-b}{a+b}\cot\frac{C}{2}=\frac{2}{2\sqrt{3}}\cot30^{\circ}=\frac{1}{\sqrt{3}}\times\sqrt{3}=1 $$
so $\dfrac{A-B}{2}=45^{\circ}$, that is $A-B=90^{\circ}$. Also $A+B=180^{\circ}-60^{\circ}=120^{\circ}$. Adding and subtracting,
$$ A=105^{\circ},\qquad B=15^{\circ} $$
Third side by the cosine law:
$$ c^{2}=a^{2}+b^{2}-2ab\cos C=(4+2\sqrt{3})+(4-2\sqrt{3})-2(3-1)\cdot\frac12=8-2=6 $$
$$ c=\sqrt{6}\approx2.45 $$
**Check by the sine law:** $\dfrac{c}{\sin C}=\dfrac{\sqrt{6}}{\sin60^{\circ}}=2.828$ and $\dfrac{a}{\sin105^{\circ}}=\dfrac{2.732}{0.9659}=2.828$. ✓

**2.** All three sides are given, so use the cosine law:
$$ \cos A=\frac{b^{2}+c^{2}-a^{2}}{2bc}=\frac{64+81-49}{144}=\frac{2}{3}\;\Rightarrow\;A=48.19^{\circ} $$
$$ \cos B=\frac{a^{2}+c^{2}-b^{2}}{2ac}=\frac{49+81-64}{126}=\frac{11}{21}\;\Rightarrow\;B=58.41^{\circ} $$
$$ C=180^{\circ}-48.19^{\circ}-58.41^{\circ}=73.40^{\circ} $$
**Check:** $\cos C=\dfrac{a^{2}+b^{2}-c^{2}}{2ab}=\dfrac{32}{112}=\dfrac{2}{7}$, and $\cos^{-1}(2/7)=73.40^{\circ}$. ✓

**3.** $C=180^{\circ}-60^{\circ}-45^{\circ}=75^{\circ}$. By the sine law $\dfrac{a}{\sin A}=\dfrac{12}{\sin60^{\circ}}=\dfrac{12}{0.8660}=13.856$, so
$$ b=13.856\times\sin45^{\circ}=9.80\qquad(=4\sqrt{6}) $$
$$ c=13.856\times\sin75^{\circ}=13.856\times0.9659=13.38 $$

**4.** By the sine law,
$$ \sin B=\frac{b\sin A}{a}=\frac{10\times0.5}{8}=0.625 $$
Because $a<b$ and $a>b\sin A=5$, this is the **ambiguous case**: $B=38.68^{\circ}$ or $B=180^{\circ}-38.68^{\circ}=141.32^{\circ}$. Both satisfy $A+B<180^{\circ}$ ($30^{\circ}+141.32^{\circ}=171.32^{\circ}$), so there are two triangles.
Triangle 1: $B=38.68^{\circ}$, $C=111.32^{\circ}$, $c=\dfrac{a\sin C}{\sin A}=\dfrac{8\times0.9317}{0.5}=14.91$.
Triangle 2: $B=141.32^{\circ}$, $C=8.68^{\circ}$, $c=\dfrac{8\times0.1510}{0.5}=2.42$.
:::

**Long answer questions [8 marks each]**

1. Solve the triangle whose sides are $a=13$, $b=14$, $c=15$. [4] Find (a) its area by Heron's formula, [2] and (b) its inradius $r=\Delta/s$ and circumradius $R=\dfrac{abc}{4\Delta}$. [2] <span class="marks">[8]</span>

::: note Model answer — long
**1.** *Angles (cosine law).*
$$ \cos A=\frac{b^{2}+c^{2}-a^{2}}{2bc}=\frac{196+225-169}{420}=\frac{252}{420}=\frac{3}{5}\;\Rightarrow\;A=53.13^{\circ} $$
$$ \cos B=\frac{a^{2}+c^{2}-b^{2}}{2ac}=\frac{169+225-196}{390}=\frac{198}{390}=0.5077\;\Rightarrow\;B=59.49^{\circ} $$
$$ C=180^{\circ}-53.13^{\circ}-59.49^{\circ}=67.38^{\circ} $$
(a) The semi-perimeter is $s=\dfrac{13+14+15}{2}=21$, so
$$ \Delta=\sqrt{s(s-a)(s-b)(s-c)}=\sqrt{21\times8\times7\times6}=\sqrt{7056}=84\ \text{square units} $$
(b)
$$ r=\frac{\Delta}{s}=\frac{84}{21}=4,\qquad R=\frac{abc}{4\Delta}=\frac{13\times14\times15}{4\times84}=\frac{2730}{336}=8.125 $$
**Check:** $\dfrac{a}{\sin A}=\dfrac{13}{0.8}=16.25=2R$. ✓
:::

::: tip Examiner's note — Solution of Triangles
Most repeated: **solving from three sides** and **from two sides and the included angle** (2081 Q21a). Always finish with a check (angles add to $180^{\circ}$ or the sine law ratio is constant). When the data are SSA, say explicitly whether there is one triangle, two, or none.
:::

## 12.8 Conic Sections

CDC allots **20 hours**, the second-longest unit. Conics are worth **9 marks** in the grid together with their share of the Group A items, and every verified year has a Group B conic question: 2081 Q14a, Q15b, Q21b; 2082 Q15a, Q15b, Q21c; 2080 Q21a; and MCQs on eccentricity (2079 Q6), conic identification (2080 Q5) and the parabolic reflector (2081 Q4).

| Conic | Standard equation | Key quantities |
|---|---|---|
| Circle, centre origin | $x^{2}+y^{2}=a^{2}$ | tangent if $c^{2}=a^{2}(1+m^{2})$ for $y=mx+c$ |
| Parabola | $y^{2}=4ax$ | focus $(a,0)$, directrix $x=-a$, latus rectum $4a$, $e=1$ |
| Ellipse | $\dfrac{x^{2}}{a^{2}}+\dfrac{y^{2}}{b^{2}}=1$ ($a>b$) | $c^{2}=a^{2}-b^{2}$, $e=\dfrac{c}{a}<1$, latus rectum $\dfrac{2b^{2}}{a}$ |
| Hyperbola | $\dfrac{x^{2}}{a^{2}}-\dfrac{y^{2}}{b^{2}}=1$ | $c^{2}=a^{2}+b^{2}$, $e=\dfrac{c}{a}>1$, latus rectum $\dfrac{2b^{2}}{a}$ |
| Tangent to $y^{2}=4ax$ at $(x_1,y_1)$ | $yy_1=2a(x+x_1)$ | normal slope $=-\dfrac{y_1}{2a}$ |

**Short answer questions [5 marks each]**

1. (a) Find the equation of the hyperbola with vertices $(0,-4)$ and $(0,4)$ and foci $(0,6)$ and $(0,-6)$. [3] (b) Find its eccentricity and the length of its latus rectum. [2] <span class="marks">[5]</span> (NEB 2081, part a)
2. (a) Find the eccentricity of the conic $3x^{2}-4y^{2}-6x=0$. [2] (b) Find the eccentricity of the ellipse whose major axis is four times its minor axis and which passes through the point $(4,2)$. [3] <span class="marks">[5]</span> (NEB 2082)
3. (a) Find the coordinates of the foci and the length of the latus rectum of the conic $\dfrac{x^{2}}{25}+\dfrac{y^{2}}{100}=1$. [3] (b) The condition for the line $y=mx+c$ to touch the circle $x^{2}+y^{2}=a^{2}$ is $c^{2}=a^{2}(1+m^{2})$. Justify it with an example. [2] <span class="marks">[5]</span> (NEB 2081, part b of each)
4. (a) Find the foci and the centre of the hyperbola $9x^{2}-16y^{2}-144=0$. [2] (b) A parabolic reflector is $20$ cm in diameter and $5$ cm deep. Find the position of its focus. [3] <span class="marks">[5]</span> (NEB 2080 Q21a; NEB 2081 Q4)
5. (a) Find the equations of the tangent and the normal to the parabola $y^{2}=8x$ at the point $(2,4)$. [3] (b) Find the equations of the tangent and normal to the circle $x^{2}+y^{2}=25$ at $(3,4)$. [2] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) The foci and vertices lie on the $y$-axis, so the hyperbola is $\dfrac{y^{2}}{a^{2}}-\dfrac{x^{2}}{b^{2}}=1$ with centre at the origin. The vertices give $a=4$ and the foci give $c=6$. Then
$$ b^{2}=c^{2}-a^{2}=36-16=20 $$
$$ \frac{y^{2}}{16}-\frac{x^{2}}{20}=1 $$
(b)
$$ e=\frac{c}{a}=\frac{6}{4}=\frac{3}{2},\qquad \text{latus rectum}=\frac{2b^{2}}{a}=\frac{2\times20}{4}=10 $$

**2.** (a) Complete the square in $x$:
$$ 3(x^{2}-2x)-4y^{2}=0 \;\Rightarrow\; 3(x-1)^{2}-4y^{2}=3 \;\Rightarrow\; \frac{(x-1)^{2}}{1}-\frac{y^{2}}{3/4}=1 $$
This is a **hyperbola** with $a^{2}=1$ and $b^{2}=\dfrac34$:
$$ e=\sqrt{1+\frac{b^{2}}{a^{2}}}=\sqrt{1+\frac34}=\frac{\sqrt{7}}{2} $$
(b) Take the ellipse $\dfrac{x^{2}}{a^{2}}+\dfrac{y^{2}}{b^{2}}=1$. "Major axis four times the minor axis" means $2a=4\times2b$, so $a=4b$.
Then $a^{2}=16b^{2}$. The point $(4,2)$ lies on it:
$$ \frac{16}{16b^{2}}+\frac{4}{b^{2}}=1\;\Rightarrow\;\frac{1}{b^{2}}+\frac{4}{b^{2}}=1\;\Rightarrow\;b^{2}=5,\quad a^{2}=80 $$
$$ e=\sqrt{1-\frac{b^{2}}{a^{2}}}=\sqrt{1-\frac{1}{16}}=\frac{\sqrt{15}}{4} $$
(If the major axis were taken along the $y$-axis the point gives $\dfrac{16}{b^{2}}+\dfrac{4}{16b^{2}}=1$, so $b^{2}=\dfrac{65}{4}$, and $e$ is still $\dfrac{\sqrt{15}}{4}$: the eccentricity depends only on the ratio $a:b$.)

**3.** (a) Here $a^{2}=100$ under $y^{2}$, which is the larger denominator, so the major axis lies along the **$y$-axis**, with $a=10$ and $b=5$.
$$ c^{2}=a^{2}-b^{2}=100-25=75\;\Rightarrow\;c=5\sqrt{3} $$
Foci: $(0,\,5\sqrt{3})$ and $(0,\,-5\sqrt{3})$. Latus rectum $=\dfrac{2b^{2}}{a}=\dfrac{2\times25}{10}=5$.
(b) **Example:** the circle $x^{2}+y^{2}=25$ ($a=5$) and the line $y=\dfrac34x+\dfrac{25}{4}$ ($m=\dfrac34$, $c=\dfrac{25}{4}$).
$$ c^{2}=\frac{625}{16},\qquad a^{2}(1+m^{2})=25\Big(1+\frac{9}{16}\Big)=25\times\frac{25}{16}=\frac{625}{16} $$
The condition holds. **Verification:** the line is $3x-4y+25=0$; its distance from the centre is $\dfrac{|25|}{\sqrt{9+16}}=5=a$, equal to the radius, so the line touches the circle. ✓

**4.** (a) Divide by $144$: $\dfrac{x^{2}}{16}-\dfrac{y^{2}}{9}=1$. So $a=4$, $b=3$, $c=\sqrt{16+9}=5$, and the centre is the origin. Foci: $(\pm5,\,0)$.
(b) Place the vertex at the origin and the axis along the $y$-axis: $x^{2}=4ay$. The rim of the reflector is $10$ cm from the axis and $5$ cm from the vertex, so $(10,5)$ lies on the parabola:
$$ 100=4a\times5\;\Rightarrow\;a=5 $$
The focus is at $(0,5)$, that is, $5$ cm from the vertex — exactly at the level of the rim.

**5.** (a) The tangent at $(x_1,y_1)$ to $y^{2}=4ax$ with $4a=8$, $a=2$ is $yy_1=2a(x+x_1)$:
$$ 4y=4(x+2)\;\Rightarrow\;y=x+2\;\Rightarrow\;x-y+2=0 $$
Its slope is $1$, so the normal has slope $-1$ and passes through $(2,4)$:
$$ y-4=-(x-2)\;\Rightarrow\;x+y-6=0 $$
(b) The tangent at $(x_1,y_1)$ to $x^{2}+y^{2}=a^{2}$ is $xx_1+yy_1=a^{2}$:
$$ 3x+4y=25 $$
The normal to a circle passes through the centre, so it is the line through $(0,0)$ and $(3,4)$: $y=\dfrac43x$, that is $4x-3y=0$.
:::

**Long answer questions [8 marks each]**

1. (a) Derive the standard equation $\dfrac{x^{2}}{a^{2}}+\dfrac{y^{2}}{b^{2}}=1$ of an ellipse from its definition as the locus of a point whose distances from two fixed points sum to a constant. [3] (b) For the ellipse $9x^{2}+16y^{2}=144$, find the lengths of the axes, the eccentricity, the foci and the latus rectum. [2] (c) Establish the condition that the line $ax+by+c=0$ may be a normal to the parabola $x^{2}=4Ay$. [3] <span class="marks">[8]</span> (NEB 2082, part c)

```figure caption="The ellipse as a locus: for every point $P$ on it, $PF_1+PF_2=2a$. The foci $F_1(-c,0)$ and $F_2(c,0)$ satisfy $c^{2}=a^{2}-b^{2}$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.6, 2.9))
a, b = 2.6, 1.6
c = (a*a - b*b) ** 0.5
th = np.linspace(0, 2*np.pi, 400)
ax.plot(a*np.cos(th), b*np.sin(th), color=INK, lw=1.8)
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
P = (a*np.cos(1.0), b*np.sin(1.0))
ax.plot([-c, P[0], c], [0, P[1], 0], color=ACCENT, lw=1.3)
for x0, lab in [(-c, "$F_1$"), (c, "$F_2$")]:
    ax.plot(x0, 0, "o", color=ACCENT, ms=4)
    ax.text(x0, -0.3, lab, ha="center", va="top", color=INK, fontsize=10)
ax.plot(*P, "o", color=INK, ms=4)
ax.text(P[0] + 0.08, P[1] + 0.1, "$P(x,y)$", color=INK, fontsize=10)
ax.text(a + 0.05, 0.08, "$A$", color=INK, fontsize=10)
ax.text(0.06, b + 0.06, "$B$", color=INK, fontsize=10)
ax.set_xlim(-3.3, 3.5); ax.set_ylim(-2.1, 2.1)
ax.set_aspect("equal"); ax.axis("off")
```

::: note Model answer — long
**1.** (a) Let the foci be $F_1(-c,0)$ and $F_2(c,0)$ and let $P(x,y)$ satisfy $PF_1+PF_2=2a$ with $a>c$.
$$ \sqrt{(x+c)^{2}+y^{2}}+\sqrt{(x-c)^{2}+y^{2}}=2a $$
Move one root across and square:
$$ (x+c)^{2}+y^{2}=4a^{2}-4a\sqrt{(x-c)^{2}+y^{2}}+(x-c)^{2}+y^{2} $$
$$ 4cx-4a^{2}=-4a\sqrt{(x-c)^{2}+y^{2}}\;\Rightarrow\;a^{2}-cx=a\sqrt{(x-c)^{2}+y^{2}} $$
Square again:
$$ a^{4}-2a^{2}cx+c^{2}x^{2}=a^{2}x^{2}-2a^{2}cx+a^{2}c^{2}+a^{2}y^{2} $$
$$ (a^{2}-c^{2})x^{2}+a^{2}y^{2}=a^{2}(a^{2}-c^{2}) $$
Put $b^{2}=a^{2}-c^{2}$ and divide by $a^{2}b^{2}$:
$$ \frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1 $$ ∎
(b) Divide by $144$: $\dfrac{x^{2}}{16}+\dfrac{y^{2}}{9}=1$, so $a=4$, $b=3$, $c=\sqrt{16-9}=\sqrt{7}$.
Major axis $2a=8$, minor axis $2b=6$. Eccentricity $e=\dfrac{c}{a}=\dfrac{\sqrt{7}}{4}$. Foci $(\pm\sqrt{7},0)$. Latus rectum $\dfrac{2b^{2}}{a}=\dfrac{2\times9}{4}=\dfrac{9}{2}$.
(c) Write the parabola $x^{2}=4Ay$ and take the point $(2At,\,At^{2})$ on it. From $2x=4A\,\dfrac{dy}{dx}$ the slope of the tangent is $\dfrac{x}{2A}=t$, so the slope of the normal is $-\dfrac{1}{t}$. The line $ax+by+c=0$ has slope $-\dfrac{a}{b}$; for it to be the normal at that point,
$$ -\frac{a}{b}=-\frac{1}{t}\;\Rightarrow\;t=\frac{b}{a} $$
The normal point must also lie on the line:
$$ a(2At)+b(At^{2})+c=0 $$
Substitute $t=\dfrac{b}{a}$:
$$ 2Ab+\frac{Ab^{3}}{a^{2}}+c=0\;\Rightarrow\;a^{2}c+2Aa^{2}b+Ab^{3}=0 $$
This is the required condition. ∎ (For a parabola written $x^{2}=4ay$ with the same letter $a$ as the line, rename the parabola's constant first, as above.)
:::

::: tip Examiner's note — Conic Sections
Most repeated: **eccentricity, foci and latus rectum from an equation** (2080, 2081, 2082), **the equation of a conic from its geometric data** (2081 Q14a), **a tangent or normal condition** (2081 Q15b, 2082 Q21c). Complete the square before reading $a$ and $b$; and find the **larger** denominator to decide the axis of an ellipse.
:::

## 12.9 Product of Vectors

CDC allots **12 hours**. Vectors are a guaranteed Group A item (grid footnote) and have a Group B or C part almost every year: 2079 Q14b (sine law by vectors), 2080 Q14b (area identity), 2081 Q14b and Q21c (dot product; area from diagonals), 2082 Q14b and Q21a (projection; scalar and vector product related).

| Result | Formula |
|---|---|
| Scalar product | $\vec{a}\cdot\vec{b}=ab\cos\theta=a_1b_1+a_2b_2+a_3b_3$ |
| Angle | $\cos\theta=\dfrac{\vec{a}\cdot\vec{b}}{ab}$ |
| Projection of $\vec{b}$ on $\vec{a}$ | $\dfrac{\vec{a}\cdot\vec{b}}{a}$ |
| Vector product | $\vec{a}\times\vec{b}=ab\sin\theta\,\hat{n}$, anti-commutative |
| Area of parallelogram (adjacent sides) | $\text{area}=\text{modulus of }\vec{a}\times\vec{b}$ |
| Area of parallelogram (diagonals $\vec{d_1},\vec{d_2}$) | $\tfrac12\times$ modulus of $\vec{d_1}\times\vec{d_2}$ |
| Area of triangle | $\tfrac12\times$ modulus of $\vec{a}\times\vec{b}$ |
| Lagrange's identity | $(\vec{a}\times\vec{b})^{2}+(\vec{a}\cdot\vec{b})^{2}=a^{2}b^{2}$ |

**Short answer questions [5 marks each]**

1. (a) Find the dot product of the vectors $2\vec{i}-\vec{j}+2\vec{k}$ and $3\vec{i}-2\vec{j}+6\vec{k}$. [2] (b) Find the angle between them. [3] <span class="marks">[5]</span> (NEB 2081, part b)
2. (a) If $\vec{a}=4\vec{i}-3\vec{j}+2\vec{k}$ and $\vec{b}=3\vec{i}-2\vec{j}+4\vec{k}$, find the projection of $\vec{b}$ on $\vec{a}$. [2] (b) Using vectors, prove that $\cos(A-B)=\cos A\cos B+\sin A\sin B$. [3] <span class="marks">[5]</span> (NEB 2082, part b)
3. (a) Find the area of the parallelogram whose diagonals are $\vec{a}=\vec{i}-2\vec{k}$ and $\vec{b}=4\vec{i}+3\vec{j}+\vec{k}$. [3] (b) Show that $\tfrac12\big|(\vec{a}-\vec{b})\times(\vec{a}+\vec{b})\big|=|\vec{a}||\vec{b}|\sin\theta$. [2] <span class="marks">[5]</span> (NEB 2081 Q21c; NEB 2080 Q14b)
4. (a) Using vector method, prove the sine law $\dfrac{\sin A}{a}=\dfrac{\sin B}{b}=\dfrac{\sin C}{c}$ in any triangle $ABC$. [3] (b) Verify Lagrange's identity for $\vec{a}=\vec{i}+2\vec{j}+3\vec{k}$ and $\vec{b}=2\vec{i}-\vec{j}+\vec{k}$. [2] <span class="marks">[5]</span> (NEB 2079, part b; NEB 2082 Q21a)

::: note Model answers — short
**1.** (a)
$$ \vec{a}\cdot\vec{b}=(2)(3)+(-1)(-2)+(2)(6)=6+2+12=20 $$
(b) $|\vec{a}|=\sqrt{4+1+4}=3$ and $|\vec{b}|=\sqrt{9+4+36}=7$:
$$ \cos\theta=\frac{\vec{a}\cdot\vec{b}}{|\vec{a}||\vec{b}|}=\frac{20}{21}\;\Rightarrow\;\theta=\cos^{-1}\frac{20}{21}=17.75^{\circ} $$

**2.** (a) $\vec{a}\cdot\vec{b}=12+6+8=26$ and $|\vec{a}|=\sqrt{16+9+4}=\sqrt{29}$:
$$ \text{projection of }\vec{b}\text{ on }\vec{a}=\frac{\vec{a}\cdot\vec{b}}{|\vec{a}|}=\frac{26}{\sqrt{29}}=4.83 $$
(b) Take unit vectors $\vec{u}=(\cos A,\sin A)$ and $\vec{v}=(\cos B,\sin B)$ in the $xy$-plane, making angles $A$ and $B$ with the $x$-axis. The angle between them is $A-B$ and both have magnitude $1$, so
$$ \vec{u}\cdot\vec{v}=(1)(1)\cos(A-B)=\cos(A-B) $$
By components,
$$ \vec{u}\cdot\vec{v}=\cos A\cos B+\sin A\sin B $$
Equating the two values gives $\cos(A-B)=\cos A\cos B+\sin A\sin B$. ∎

**3.** (a) The area of a parallelogram with diagonals $\vec{d_1}$, $\vec{d_2}$ is half the modulus of $\vec{d_1}\times\vec{d_2}$. With the determinant expansion,
$$ \vec{a}\times\vec{b}=\vec{i}\big(0\cdot1-(-2)(3)\big)-\vec{j}\big(1\cdot1-(-2)(4)\big)+\vec{k}\big(1\cdot3-0\cdot4\big) $$
$$ =6\vec{i}-9\vec{j}+3\vec{k} $$
$$ |\vec{a}\times\vec{b}|=\sqrt{36+81+9}=\sqrt{126}=3\sqrt{14} $$
$$ \text{Area}=\frac12\times3\sqrt{14}=\frac{3\sqrt{14}}{2}\approx5.61\ \text{square units} $$
(b) Expand using the distributive law and $\vec{a}\times\vec{a}=\vec{b}\times\vec{b}=\vec{0}$, $\vec{b}\times\vec{a}=-\vec{a}\times\vec{b}$:
$$ (\vec{a}-\vec{b})\times(\vec{a}+\vec{b})=\vec{a}\times\vec{a}+\vec{a}\times\vec{b}-\vec{b}\times\vec{a}-\vec{b}\times\vec{b}=2(\vec{a}\times\vec{b}) $$
Half of its modulus is the modulus of $\vec{a}\times\vec{b}$, which is $|\vec{a}||\vec{b}|\sin\theta$. ∎ (Geometrically $\vec{a}-\vec{b}$ and $\vec{a}+\vec{b}$ are the diagonals of the parallelogram on $\vec{a}$ and $\vec{b}$.)

**4.** (a) Let the sides be the vectors $\vec{BC}=\vec{a}$, $\vec{CA}=\vec{b}$, $\vec{AB}=\vec{c}$, taken round the triangle, so $\vec{a}+\vec{b}+\vec{c}=\vec{0}$. Cross this with $\vec{a}$ and with $\vec{b}$ in turn:
$$ \vec{a}\times(\vec{a}+\vec{b}+\vec{c})=\vec{0}\;\Rightarrow\;\vec{a}\times\vec{b}=\vec{c}\times\vec{a} $$
$$ \vec{b}\times(\vec{a}+\vec{b}+\vec{c})=\vec{0}\;\Rightarrow\;\vec{b}\times\vec{c}=\vec{a}\times\vec{b} $$
So $\vec{a}\times\vec{b}=\vec{b}\times\vec{c}=\vec{c}\times\vec{a}$. Taking moduli, and using that the angle between the head-to-tail vectors $\vec{a}$ and $\vec{b}$ is $180^{\circ}-C$ (similarly $180^{\circ}-A$ and $180^{\circ}-B$):
$$ ab\sin C=bc\sin A=ca\sin B $$
Divide throughout by $abc$:
$$ \frac{\sin C}{c}=\frac{\sin A}{a}=\frac{\sin B}{b} $$ ∎
(b) $\vec{a}\cdot\vec{b}=2-2+3=3$. The cross product is
$$ \vec{a}\times\vec{b}=\vec{i}(2\cdot1-3(-1))-\vec{j}(1\cdot1-3\cdot2)+\vec{k}(1(-1)-2\cdot2)=5\vec{i}+5\vec{j}-5\vec{k} $$
so $|\vec{a}\times\vec{b}|^{2}=75$. Then $|\vec{a}\times\vec{b}|^{2}+(\vec{a}\cdot\vec{b})^{2}=75+9=84$, and $|\vec{a}|^{2}|\vec{b}|^{2}=14\times6=84$. ✓ This is the relation between the scalar and the vector product: together they give $\tan\theta=\dfrac{|\vec{a}\times\vec{b}|}{\vec{a}\cdot\vec{b}}$.
:::

**Long answer questions [8 marks each]**

1. (a) Find a unit vector perpendicular to both $\vec{a}=2\vec{i}-\vec{j}+\vec{k}$ and $\vec{b}=\vec{i}+2\vec{j}-\vec{k}$, and find the sine of the angle between them. [3] (b) Find the area of the triangle with vertices $A(1,2,3)$, $B(3,5,7)$ and $C(2,4,5)$. [3] (c) A force $\vec{F}=2\vec{i}+3\vec{j}+4\vec{k}$ newton displaces a particle from $A(1,2,3)$ to $B(3,5,7)$. Find the work done. [2] <span class="marks">[8]</span> (CDC model 2080, Q21c pattern)

::: note Model answer — long
**1.** (a) A vector perpendicular to both is $\vec{a}\times\vec{b}$:
$$ \vec{a}\times\vec{b}=\vec{i}\big((-1)(-1)-(1)(2)\big)-\vec{j}\big((2)(-1)-(1)(1)\big)+\vec{k}\big((2)(2)-(-1)(1)\big) $$
$$ =-\vec{i}+3\vec{j}+5\vec{k} $$
$$ |\vec{a}\times\vec{b}|=\sqrt{1+9+25}=\sqrt{35} $$
$$ \text{unit vector}=\frac{-\vec{i}+3\vec{j}+5\vec{k}}{\sqrt{35}} $$
Since $|\vec{a}|=|\vec{b}|=\sqrt{6}$,
$$ \sin\theta=\frac{|\vec{a}\times\vec{b}|}{|\vec{a}||\vec{b}|}=\frac{\sqrt{35}}{6}=0.986 $$
(The negative of the unit vector is equally correct.)
(b) $\vec{AB}=2\vec{i}+3\vec{j}+4\vec{k}$ and $\vec{AC}=\vec{i}+2\vec{j}+2\vec{k}$:
$$ \vec{AB}\times\vec{AC}=\vec{i}(6-8)-\vec{j}(4-4)+\vec{k}(4-3)=-2\vec{i}+0\vec{j}+\vec{k} $$
$$ \text{Area}=\frac12\sqrt{4+0+1}=\frac{\sqrt{5}}{2}\approx1.12\ \text{square units} $$
(c) The displacement is $\vec{d}=\vec{AB}=2\vec{i}+3\vec{j}+4\vec{k}$ metre. Work done is the scalar product:
$$ W=\vec{F}\cdot\vec{d}=2(2)+3(3)+4(4)=4+9+16=29\ \text{J} $$
:::

::: tip Examiner's note — Product of Vectors
Most repeated: **dot product / projection / angle from components** (2081, 2082), **area of a triangle or parallelogram by the cross product** (2081 Q21c), and **a short vector proof of a trigonometric law** (2079 sine law, the compound-angle formula). Show the determinant expansion for $\vec{a}\times\vec{b}$; a cross product written down without working loses the method marks if one component is wrong.
:::

## 12.10 Correlation and Regression

CDC allots **8 hours**, and a numerical correlation or regression question from a small table has appeared in **every verified year**: 2079 Q16 (from two given regression lines), 2080 Q15, 2081 Q16, 2082 Q16, and the CDC model Q16. It is the most predictable Group B question in the paper. Work with **deviations from the mean** to keep the arithmetic small.

| Result | Formula |
|---|---|
| Karl Pearson | $r=\dfrac{\sum dx\,dy}{\sqrt{\sum dx^{2}\,\sum dy^{2}}}$, $dx=x-\bar{x}$, $dy=y-\bar{y}$ |
| Regression of $y$ on $x$ | $y-\bar{y}=b_{yx}(x-\bar{x})$, $b_{yx}=\dfrac{\sum dx\,dy}{\sum dx^{2}}$ |
| Regression of $x$ on $y$ | $x-\bar{x}=b_{xy}(y-\bar{y})$, $b_{xy}=\dfrac{\sum dx\,dy}{\sum dy^{2}}$ |
| Link | $r^{2}=b_{yx}\,b_{xy}$; $r$ has the sign of both coefficients |
| Both lines pass through | $(\bar{x},\bar{y})$ |
| Rank correlation | $r_{s}=1-\dfrac{6\sum d^{2}}{n(n^{2}-1)}$ |

**Short answer questions [5 marks each]**

1. The regression equations of age $(x)$ and blood pressure $(y)$ are $0.22x-y+81.1175=0$ and $x-1.623y+105.695=0$. (a) Find the regression coefficients. [2] (b) Find the correlation coefficient. [1] (c) Find the mean of $x$ and the mean of $y$. [2] <span class="marks">[5]</span> (NEB 2079)
2. The height $(x)$ in cm and weight $(y)$ in kg of $5$ persons are: $x$: $160,162,165,161,162$; $y$: $63,62,64,60,61$. Find the correlation coefficient between $x$ and $y$ and the regression coefficient of $y$ on $x$. [3+2] <span class="marks">[5]</span> (NEB 2080)
3. The supply $(X)$ and the price $(Y)$ of a commodity over six years are: $X$: $45,50,56,62,65,70$; $Y$: $65,70,75,80,90,100$. (a) Find the correlation coefficient. [2] (b) Calculate the supply when the price is Rs. $150$. [3] <span class="marks">[5]</span> (NEB 2082)
4. The supply $(x)$ and the price $(y)$ of a commodity over seven years are: $x$: $80,84,86,88,92,96,97$; $y$: $12,14,15,16,18,20,22$. Find the likely price when the supply is $120$. <span class="marks">[5]</span> (NEB 2081)
5. Two judges ranked six contestants: Judge 1: $1,2,3,4,5,6$; Judge 2: $2,1,4,3,6,5$. Find the rank correlation coefficient and interpret it. <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) Write the first equation as $y=0.22x+81.1175$: this is the line of $y$ on $x$, so $b_{yx}=0.22$. Write the second as $x=1.623y-105.695$: the line of $x$ on $y$, so $b_{xy}=1.623$.
(b) $r^{2}=b_{yx}\,b_{xy}=0.22\times1.623=0.3571$, and both coefficients are positive, so
$$ r=+\sqrt{0.3571}=0.598 $$
(c) Both lines pass through $(\bar{x},\bar{y})$. Substitute the first into the second:
$$ x=1.623(0.22x+81.1175)-105.695=0.3571x+131.654-105.695 $$
$$ 0.6429x=25.959\;\Rightarrow\;\bar{x}=40.375,\qquad \bar{y}=0.22(40.375)+81.1175=90.0 $$
Mean age $\approx40.4$ years, mean blood pressure $=90$ units.
(If you assign the lines the other way round, $b_{yx}=1/1.623=0.616$ and $b_{xy}=1/0.22=4.55$, whose product is $2.8>1$ — impossible. That test confirms the assignment above.)

**2.** $\bar{x}=\dfrac{810}{5}=162$, $\bar{y}=\dfrac{310}{5}=62$.

| $x$ | $y$ | $dx$ | $dy$ | $dx\,dy$ | $dx^{2}$ | $dy^{2}$ |
|---|---|---|---|---|---|---|
| 160 | 63 | $-2$ | $1$ | $-2$ | 4 | 1 |
| 162 | 62 | $0$ | $0$ | $0$ | 0 | 0 |
| 165 | 64 | $3$ | $2$ | $6$ | 9 | 4 |
| 161 | 60 | $-1$ | $-2$ | $2$ | 1 | 4 |
| 162 | 61 | $0$ | $-1$ | $0$ | 0 | 1 |
| Total | | $0$ | $0$ | $6$ | 14 | 10 |

$$ r=\frac{\sum dx\,dy}{\sqrt{\sum dx^{2}\sum dy^{2}}}=\frac{6}{\sqrt{14\times10}}=\frac{6}{11.83}=0.507 $$
$$ b_{yx}=\frac{\sum dx\,dy}{\sum dx^{2}}=\frac{6}{14}=0.429 $$
The correlation is positive and moderate: taller persons tend to be somewhat heavier.

**3.** $\bar{X}=\dfrac{348}{6}=58$, $\bar{Y}=\dfrac{480}{6}=80$.

| $X$ | $Y$ | $dX$ | $dY$ | $dX\,dY$ | $dX^{2}$ | $dY^{2}$ |
|---|---|---|---|---|---|---|
| 45 | 65 | $-13$ | $-15$ | 195 | 169 | 225 |
| 50 | 70 | $-8$ | $-10$ | 80 | 64 | 100 |
| 56 | 75 | $-2$ | $-5$ | 10 | 4 | 25 |
| 62 | 80 | $4$ | $0$ | 0 | 16 | 0 |
| 65 | 90 | $7$ | $10$ | 70 | 49 | 100 |
| 70 | 100 | $12$ | $20$ | 240 | 144 | 400 |
| Total | | $0$ | $0$ | 595 | 446 | 850 |

(a)
$$ r=\frac{595}{\sqrt{446\times850}}=\frac{595}{615.7}=0.966 $$
a very strong positive correlation.
(b) To estimate the **supply** from the **price**, use the regression of $X$ on $Y$:
$$ b_{XY}=\frac{\sum dX\,dY}{\sum dY^{2}}=\frac{595}{850}=0.70 $$
$$ X-58=0.70\,(Y-80)\;\Rightarrow\;X=58+0.70(150-80)=58+49=107 $$
The estimated supply at a price of Rs. $150$ is $107$ units.

**4.** $\bar{x}=\dfrac{623}{7}=89$ and $\bar{y}=\dfrac{117}{7}=16.71$. Deviations of $x$: $-9,-5,-3,-1,3,7,8$, with $\sum dx=0$ and $\sum dx^{2}=81+25+9+1+9+49+64=238$. Then
$$ \sum dx\cdot y=-9(12)-5(14)-3(15)-1(16)+3(18)+7(20)+8(22)=131 $$
Because $\sum dx=0$, $\sum dx\,dy=\sum dx\cdot y=131$. So
$$ b_{yx}=\frac{131}{238}=0.550 $$
$$ y-16.71=0.550\,(x-89) $$
$$ y=16.71+0.550(120-89)=16.71+17.06=33.78 $$
The likely price when the supply is $120$ is about Rs. $33.8$.

**5.** $d=R_1-R_2$: $-1,\ 1,\ -1,\ 1,\ -1,\ 1$, so $\sum d^{2}=6$ and $n=6$:
$$ r_{s}=1-\frac{6\times6}{6\,(36-1)}=1-\frac{36}{210}=0.829 $$
The two judges largely agree: a strong positive rank correlation (perfect agreement would give $1$).
:::

**Long answer questions [8 marks each]**

1. Five students obtained the following marks: $x$ (Mathematics): $2,4,6,8,10$; $y$ (Physics): $5,7,9,8,11$. (a) Calculate Karl Pearson's coefficient of correlation and interpret it. [3] (b) Obtain both regression lines. [3] (c) Estimate $y$ when $x=12$ and $x$ when $y=10$. [2] <span class="marks">[8]</span>

::: note Model answer — long
**1.** $\bar{x}=6$, $\bar{y}=8$.

| $x$ | $y$ | $dx$ | $dy$ | $dx\,dy$ | $dx^{2}$ | $dy^{2}$ |
|---|---|---|---|---|---|---|
| 2 | 5 | $-4$ | $-3$ | 12 | 16 | 9 |
| 4 | 7 | $-2$ | $-1$ | 2 | 4 | 1 |
| 6 | 9 | $0$ | $1$ | 0 | 0 | 1 |
| 8 | 8 | $2$ | $0$ | 0 | 4 | 0 |
| 10 | 11 | $4$ | $3$ | 12 | 16 | 9 |
| Total | | $0$ | $0$ | 26 | 40 | 20 |

(a)
$$ r=\frac{26}{\sqrt{40\times20}}=\frac{26}{28.28}=0.919 $$
There is a strong **positive** correlation: students who score more in Mathematics tend to score more in Physics.
(b)
$$ b_{yx}=\frac{26}{40}=0.65,\qquad b_{xy}=\frac{26}{20}=1.3 $$
Check: $b_{yx}\,b_{xy}=0.845=r^{2}$ ✓. The regression line of $y$ on $x$:
$$ y-8=0.65(x-6)\;\Rightarrow\;y=0.65x+4.1 $$
The regression line of $x$ on $y$:
$$ x-6=1.3(y-8)\;\Rightarrow\;x=1.3y-4.4 $$
(c) When $x=12$: $y=0.65(12)+4.1=11.9$. When $y=10$: $x=1.3(10)-4.4=8.6$.
:::

::: tip Examiner's note — Correlation and Regression
Most repeated: **correlation from a table** then **regression and an estimate** (2080, 2081, 2082); **both regression lines given** (2079). Always say which variable is being estimated: to estimate $x$ from $y$ use the regression of $x$ on $y$ — using the wrong line is the commonest mark-loser. Quote $r$ to three decimals and give a one-line interpretation.
:::

## 12.11 Probability

CDC allots only **4 hours** but supplies a Group A item every year: $P(B/A)$ from given probabilities appeared as an MCQ in **2080 Q7, 2081 Q6, 2082 Q6 and CDC model Q6** (the last asked the chance of $53$ Fridays or Saturdays in a leap year), and there is a Group B question on it in the grid.

| Result | Formula |
|---|---|
| Conditional probability | $P(B/A)=\dfrac{P(A\cap B)}{P(A)}$, $P(A)>0$ |
| Multiplication theorem | $P(A\cap B)=P(A)\,P(B/A)=P(B)\,P(A/B)$ |
| Independent events | $P(A\cap B)=P(A)P(B)$, equivalently $P(B/A)=P(B)$ |
| Addition theorem | $P(A\cup B)=P(A)+P(B)-P(A\cap B)$ |

**Short answer questions [5 marks each]**

1. (a) If $P(A)=\dfrac12$, $P(B)=\dfrac{1}{13}$ and $P(A\cap B)=\dfrac{1}{26}$, find $P(B/A)$. [2] (b) If $P(A)=\dfrac13$, $P(B)=\dfrac23$ and $P(A\cap B)=\dfrac15$, find $P(B/A)$. [3] <span class="marks">[5]</span> (NEB 2080 Q7; NEB 2082 Q6)
2. If $P(A\cap B)=\dfrac{1}{18}$, $P(B)=\dfrac{1}{18}$ and $2P(A)=5P(B)$, find $P(B/A)$ and $P(A/B)$, and decide whether $A$ and $B$ are independent. <span class="marks">[5]</span> (NEB 2081)
3. (a) What is the probability that a leap year has $53$ Fridays or $53$ Saturdays? [3] (b) Two cards are drawn one after the other, without replacement, from a pack of $52$. Find the probability that both are aces. [2] <span class="marks">[5]</span> (CDC model 2080, part a)
4. A bag contains $5$ red and $3$ white balls. Two balls are drawn one after another without replacement. Find the probability that (a) both are red, (b) one is red and one is white, (c) at least one is white. [2+2+1] <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a)
$$ P(B/A)=\frac{P(A\cap B)}{P(A)}=\frac{1/26}{1/2}=\frac{1}{13} $$
(b)
$$ P(B/A)=\frac{1/5}{1/3}=\frac35 $$
(Only $P(A)$ and $P(A\cap B)$ are used; $P(B)$ is a distractor.)

**2.** From $2P(A)=5P(B)=\dfrac{5}{18}$ we get $P(A)=\dfrac{5}{36}$.
$$ P(B/A)=\frac{1/18}{5/36}=\frac{1}{18}\times\frac{36}{5}=\frac25 $$
$$ P(A/B)=\frac{1/18}{1/18}=1 $$
Independence would need $P(A\cap B)=P(A)P(B)=\dfrac{5}{36}\times\dfrac{1}{18}=\dfrac{5}{648}$, but $P(A\cap B)=\dfrac{1}{18}$. So $A$ and $B$ are **dependent**. (Indeed $P(A\cap B)=P(B)$ means $B$ is wholly contained in $A$.)

**3.** (a) A leap year has $366=52\times7+2$ days: $52$ complete weeks and $2$ extra days. The extra pair is one of seven equally likely pairs: (Sun, Mon), (Mon, Tue), (Tue, Wed), (Wed, Thu), (Thu, Fri), (Fri, Sat), (Sat, Sun). A year has $53$ Fridays or $53$ Saturdays if the pair contains Friday or Saturday: (Thu, Fri), (Fri, Sat), (Sat, Sun) — $3$ pairs.
$$ P=\frac37 $$
(b) $P(\text{first ace})=\dfrac{4}{52}$ and, given that, $P(\text{second ace})=\dfrac{3}{51}$:
$$ P(\text{both aces})=\frac{4}{52}\times\frac{3}{51}=\frac{1}{221} $$

**4.** (a)
$$ P(RR)=\frac58\times\frac47=\frac{20}{56}=\frac{5}{14} $$
(b) Red then white, or white then red:
$$ P=\frac58\times\frac37+\frac38\times\frac57=\frac{15}{56}+\frac{15}{56}=\frac{30}{56}=\frac{15}{28} $$
(c) "At least one white" is the complement of "both red":
$$ P=1-\frac{5}{14}=\frac{9}{14} $$
**Check:** $P(RR)+P(RW\text{ or }WR)+P(WW)=\dfrac{20}{56}+\dfrac{30}{56}+\dfrac{6}{56}=1$. ✓
:::

::: caution A printed item whose events are actually independent
In 2080 Q7 the events are described as **dependent** with $P(A)=\dfrac12$, $P(B)=\dfrac{1}{13}$, $P(A\cap B)=\dfrac{1}{26}$. But $P(A)P(B)=\dfrac{1}{26}=P(A\cap B)$, which is the definition of independence, and $P(B/A)=\dfrac{1}{13}=P(B)$. The numerical answer $\dfrac{1}{13}$ is unaffected, but do not rely on the word "dependent" in a stem: compute $P(A\cap B)/P(A)$ and move on.
:::

**Long answer questions [8 marks each]**

1. (a) Define conditional probability and state the multiplication theorem of probability. [2] (b) For two events $P(A)=0.6$, $P(B)=0.5$ and $P(A\cup B)=0.8$. Find $P(A\cap B)$, $P(A/B)$ and $P(B/A)$, and decide whether $A$ and $B$ are independent. [3] (c) A bag holds $4$ red and $3$ black balls. Two balls are drawn in succession without replacement. Find the probabilities of (i) two red, (ii) one of each colour, (iii) two black, and check that they sum to $1$. [3] <span class="marks">[8]</span>

::: note Model answer — long
**1.** (a) The **conditional probability** of $B$ given that $A$ has occurred is $P(B/A)=\dfrac{P(A\cap B)}{P(A)}$, $P(A)>0$. The **multiplication theorem** states $P(A\cap B)=P(A)\,P(B/A)$.
(b) From the addition theorem:
$$ P(A\cap B)=P(A)+P(B)-P(A\cup B)=0.6+0.5-0.8=0.3 $$
$$ P(A/B)=\frac{0.3}{0.5}=0.6,\qquad P(B/A)=\frac{0.3}{0.6}=0.5 $$
Since $P(A/B)=0.6=P(A)$ (equivalently $P(A)P(B)=0.3=P(A\cap B)$), the events are **independent**.
(c)
$$ P(\text{two red})=\frac47\times\frac36=\frac27 $$
$$ P(\text{one of each})=\frac47\times\frac36+\frac37\times\frac46=\frac{12}{42}+\frac{12}{42}=\frac47 $$
$$ P(\text{two black})=\frac37\times\frac26=\frac17 $$
Sum: $\dfrac27+\dfrac47+\dfrac17=1$. ✓
:::

::: tip Examiner's note — Probability
Most repeated: **$P(B/A)$ from three given probabilities** (2080, 2081, 2082, CDC) — a one-line answer that a careless candidate still gets wrong by dividing by $P(B)$; and **draws without replacement**. Write the formula first, substitute, simplify.
:::

## 12.12 Derivatives

CDC allots **18 hours**, and with anti-derivatives and differential equations Calculus is the heaviest area, **22 of the 75 marks**. The years 2080, 2081, 2082 and the CDC model each set a hyperbolic or inverse-hyperbolic derivative (2080 Q8, 2081 Q17, 2082 Q17a and Q18a, CDC Q7), a L'Hospital limit (2080 Q17b, 2081 Q7), a tangent or normal (2081 Q18a, 2082 Q7) and a rate-of-change problem (2081 Q22a, 2082 Q22a, CDC Q10).

| Result | Formula |
|---|---|
| $\dfrac{d}{dx}\sinh x$, $\cosh x$ | $\cosh x$, $\sinh x$ |
| $\dfrac{d}{dx}\sinh^{-1}x$ | $\dfrac{1}{\sqrt{1+x^{2}}}$ |
| $\dfrac{d}{dx}\cosh^{-1}x$ | $\dfrac{1}{\sqrt{x^{2}-1}}$, $x>1$ |
| $\dfrac{d}{dx}\tanh^{-1}x$ | $\dfrac{1}{1-x^{2}}$, $-1<x<1$ |
| $\dfrac{d}{dx}\coth^{-1}x$ | $\dfrac{1}{1-x^{2}}$ for $x$ outside $[-1,1]$ |
| $\dfrac{d}{dx}\text{sech}^{-1}x$ | $-\dfrac{1}{x\sqrt{1-x^{2}}}$, $0<x<1$ |
| L'Hospital | $\lim\dfrac{f}{g}=\lim\dfrac{f'}{g'}$ for $\dfrac00$ or $\dfrac{\infty}{\infty}$ |
| Tangent | $y-y_1=m(x-x_1)$, $m=\dfrac{dy}{dx}$ at the point |
| Normal | slope $-\dfrac{1}{m}$ |
| Differential | $dy=f'(x)\,dx$; $\Delta y\approx dy$ |

**Short answer questions [5 marks each]**

1. (a) Find the derivative of $(\tan x)^{\log x}$. [2] (b) Find the equation of the tangent to $y=2x^{3}+x^{2}-7x-2$ at the point where $x=2$. [3] <span class="marks">[5]</span> (NEB 2079, part a; NEB 2081 Q18a)
2. (a) Find the derivative of $\coth^{-1}(\sin2x)$. [2] (b) Using L'Hospital's rule, evaluate $\displaystyle\lim_{x\to\infty}\frac{\ln(2x^{2}+5)}{\ln(3x^{3}-4)}$. [3] <span class="marks">[5]</span> (NEB 2082 Q18a; NEB 2080 Q17b)
3. (a) Find the rate of change of the volume of a sphere with respect to its surface area when the radius is $7$ cm. [2] (b) The volume of a sphere increases at the rate $25\ \text{cm}^{3}\text{s}^{-1}$. At what rate is the radius increasing at the instant when the surface area is $10\pi\ \text{cm}^{2}$? [3] <span class="marks">[5]</span> (NEB 2082, part a; CDC model 2080 Q10)
4. (a) A curve $y^{2}=8x$ changes its abscissa and ordinate at the same rate. Show that the ordinate is then double the abscissa. [2] (b) The side of a cube is measured as $10$ cm with a possible error of $0.01$ cm. Use differentials to find the percentage error in its volume. [3] <span class="marks">[5]</span> (NEB 2081 Q22a, for part a)
5. (a) Write the derivative of $\text{cosech}^{-1}x$. [1] (b) State L'Hospital's rule. [1] (c) Write the condition under which the curve $y=f(x)$ has a tangent parallel to the $y$-axis. [1] (d) Write $\displaystyle\int\frac{dx}{x^{2}-a^{2}}$. [1] (e) Write the standard form of a first-order linear differential equation. [1] <span class="marks">[5]</span> (NEB 2082 Q17)

::: note Model answers — short
**1.** (a) Take natural logarithms of $y=(\tan x)^{\ln x}$: $\ln y=\ln x\cdot\ln(\tan x)$. Differentiate:
$$ \frac{1}{y}\frac{dy}{dx}=\frac{1}{x}\ln(\tan x)+\ln x\cdot\frac{\sec^{2}x}{\tan x}=\frac{\ln(\tan x)}{x}+\frac{2\ln x}{\sin2x} $$
$$ \frac{dy}{dx}=(\tan x)^{\ln x}\Big[\frac{\ln(\tan x)}{x}+\frac{2\ln x}{\sin2x}\Big] $$
(b) At $x=2$: $y=2(8)+4-14-2=4$, so the point is $(2,4)$. The slope is
$$ \frac{dy}{dx}=6x^{2}+2x-7=24+4-7=21 $$
$$ y-4=21(x-2)\;\Rightarrow\;21x-y-38=0 $$
(As recorded, the 2081 question names the point $(2,5)$, which does not lie on this curve — $y(2)=4$ — so the tangent is taken at $x=2$.)

**2.** (a) With $u=\sin2x$, $\dfrac{d}{du}\coth^{-1}u=\dfrac{1}{1-u^{2}}$, so
$$ \frac{d}{dx}\coth^{-1}(\sin2x)=\frac{2\cos2x}{1-\sin^{2}2x}=\frac{2\cos2x}{\cos^{2}2x}=2\sec2x $$
(Strictly, $\coth^{-1}u$ is defined only for $|u|>1$, while $\sin2x$ never exceeds $1$; the printed question asks for the formal result, $2\sec2x$.)
(b) As $x\to\infty$ the form is $\dfrac{\infty}{\infty}$. Apply L'Hospital's rule:
$$ \lim\frac{\dfrac{4x}{2x^{2}+5}}{\dfrac{9x^{2}}{3x^{3}-4}}=\lim\frac{4x(3x^{3}-4)}{9x^{2}(2x^{2}+5)}=\lim\frac{12x^{4}-16x}{18x^{4}+45x^{2}} $$
Divide by $x^{4}$:
$$ =\lim\frac{12-16/x^{3}}{18+45/x^{2}}=\frac{12}{18}=\frac23 $$

**3.** (a) $V=\dfrac43\pi r^{3}$ and $S=4\pi r^{2}$, so $\dfrac{dV}{dr}=4\pi r^{2}$ and $\dfrac{dS}{dr}=8\pi r$:
$$ \frac{dV}{dS}=\frac{dV/dr}{dS/dr}=\frac{4\pi r^{2}}{8\pi r}=\frac{r}{2}=\frac72=3.5\ \text{cm} $$
(b) $4\pi r^{2}=10\pi$ at that instant. Since $\dfrac{dV}{dt}=4\pi r^{2}\dfrac{dr}{dt}$:
$$ 25=10\pi\,\frac{dr}{dt}\;\Rightarrow\;\frac{dr}{dt}=\frac{2.5}{\pi}=0.796\ \text{cm s}^{-1} $$

**4.** (a) Differentiate $y^{2}=8x$ with respect to $t$: $2y\dfrac{dy}{dt}=8\dfrac{dx}{dt}$. The abscissa and ordinate change at the same rate, $\dfrac{dy}{dt}=\dfrac{dx}{dt}$, so $2y=8$, $y=4$. Then $16=8x$ gives $x=2$. The point is $(2,4)$ and indeed $y=2x$. ∎
(b) $V=x^{3}$ so $dV=3x^{2}\,dx=3(100)(0.01)=3\ \text{cm}^{3}$:
$$ \frac{dV}{V}\times100=\frac{3}{1000}\times100=0.3\% $$
(Here $dy$ is the differential $f'(x)\,dx$ and $\Delta y$ the actual change; for small $dx$ they are nearly equal, which is why the percentage error is computed as $\dfrac{dy}{y}\times100$.)

**5.** (a) $\dfrac{d}{dx}\text{cosech}^{-1}x=-\dfrac{1}{|x|\sqrt{1+x^{2}}}$, $x\neq0$.
(b) If $f(a)=g(a)=0$ (or both tend to $\infty$) and $\lim\dfrac{f'(x)}{g'(x)}$ exists, then $\displaystyle\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)}$.
(c) $\dfrac{dy}{dx}\to\infty$, equivalently $\dfrac{dx}{dy}=0$.
(d) $\displaystyle\int\frac{dx}{x^{2}-a^{2}}=\frac{1}{2a}\ln\Big|\frac{x-a}{x+a}\Big|+C$.
(e) $\dfrac{dy}{dx}+Py=Q$, with $P$ and $Q$ functions of $x$ alone.
:::

**Long answer questions [8 marks each]**

1. (a) Find $\dfrac{dy}{dx}$ if $y=\sinh^{-1}(\tan x)$. [3] (b) Evaluate $\displaystyle\lim_{x\to0}\frac{e^{x}-1-x}{x^{2}}$. [2] (c) Find the equations of the tangent and the normal to the curve $y=x^{3}-3x$ at the point $(2,2)$. [3] <span class="marks">[8]</span>

::: note Model answer — long
**1.** (a) With $u=\tan x$ and $\dfrac{d}{du}\sinh^{-1}u=\dfrac{1}{\sqrt{1+u^{2}}}$:
$$ \frac{dy}{dx}=\frac{\sec^{2}x}{\sqrt{1+\tan^{2}x}}=\frac{\sec^{2}x}{\sec x}=\sec x $$
valid where $\cos x>0$, so that $\sqrt{\sec^{2}x}=\sec x$.
(b) The form is $\dfrac00$. Apply L'Hospital's rule twice:
$$ \lim\frac{e^{x}-1-x}{x^{2}}=\lim\frac{e^{x}-1}{2x}=\lim\frac{e^{x}}{2}=\frac12 $$
(c) The point $(2,2)$ lies on the curve: $8-6=2$. The slope is $\dfrac{dy}{dx}=3x^{2}-3=9$ at $x=2$.
$$ \text{Tangent: }y-2=9(x-2)\;\Rightarrow\;9x-y-16=0 $$
$$ \text{Normal (slope }-\tfrac19\text{): }y-2=-\tfrac19(x-2)\;\Rightarrow\;x+9y-20=0 $$
:::

::: tip Examiner's note — Derivatives
Most repeated: **inverse hyperbolic derivative** (2080, 2081, 2082, CDC), **L'Hospital limit** (2080, 2081), **rate of change** (2081, 2082, CDC) and the **five-part recall** (2081 Q17, 2082 Q17). In a related-rates question write the relation, differentiate with respect to $t$, *then* substitute the instant's values — substituting first kills the variable.
:::

## 12.13 Anti-derivatives

CDC allots **18 hours**. Partial fractions were set as a Group B integral in three of the four verified years (2079 Q17, 2081 Q18b, 2082 Q18b; 2080 set a substitution integral, Q22b); a half-angle substitution integral $\int dx/(a+b\cos x)$ in 2081 Q22b and 2082 Q22b; and standard forms as MCQs (2080 Q9, 2081 Q8, 2082 Q8).

| Standard form | Result |
|---|---|
| $\displaystyle\int\dfrac{dx}{x^{2}+a^{2}}$ | $\dfrac1a\tan^{-1}\dfrac{x}{a}+C$ |
| $\displaystyle\int\dfrac{dx}{x^{2}-a^{2}}$ | $\dfrac{1}{2a}\ln\Big|\dfrac{x-a}{x+a}\Big|+C$ |
| $\displaystyle\int\dfrac{dx}{a^{2}-x^{2}}$ | $\dfrac{1}{2a}\ln\Big|\dfrac{a+x}{a-x}\Big|+C$ |
| $\displaystyle\int\dfrac{dx}{\sqrt{x^{2}-a^{2}}}$ | $\ln\big|x+\sqrt{x^{2}-a^{2}}\big|+C$ |
| $\displaystyle\int\dfrac{f'(x)}{f(x)}dx$ | $\ln|f(x)|+C$ |
| Half-angle substitution | $t=\tan\dfrac{x}{2}$: $\cos x=\dfrac{1-t^{2}}{1+t^{2}}$, $dx=\dfrac{2\,dt}{1+t^{2}}$ |

**Short answer questions [5 marks each]**

1. (a) Define a proper rational fraction with an example. [1] (b) Integrate $\displaystyle\int\frac{2x^{2}+3}{x^{3}+3x^{2}+2x}\,dx$ using partial fractions. [4] <span class="marks">[5]</span> (NEB 2079)
2. (a) Integrate $\displaystyle\int\frac{dx}{x^{3}-x^{2}-2x}$. [3] (b) Write $\displaystyle\int\frac{dx}{9x^{2}+1}$. [2] <span class="marks">[5]</span> (NEB 2082 Q18b; NEB 2082 Q8)
3. Evaluate $\displaystyle\int\frac{2x^{2}-x+4}{x^{3}+4x}\,dx$. <span class="marks">[5]</span> (NEB 2081 Q18b)
4. (a) Prove that $\displaystyle\int\frac{dx}{1-e^{x}}=\ln|e^{x}|-\ln|1-e^{x}|+c$. [3] (b) Find $\displaystyle\int\frac{dx}{x^{2}-1}$. [2] <span class="marks">[5]</span> (NEB 2080 Q22b; NEB 2080 Q9)
5. Integrate $\displaystyle\int\frac{dx}{5-3\cos x}$. <span class="marks">[5]</span> (NEB 2082 Q22b, here with 5 marks)

::: note Model answers — short
**1.** (a) A rational fraction $\dfrac{f(x)}{g(x)}$ is **proper** if the degree of the numerator is less than the degree of the denominator, for example $\dfrac{x+1}{x^{2}+3x+2}$.
(b) The denominator factorises: $x^{3}+3x^{2}+2x=x(x+1)(x+2)$. The fraction is proper, so
$$ \frac{2x^{2}+3}{x(x+1)(x+2)}=\frac{A}{x}+\frac{B}{x+1}+\frac{C}{x+2} $$
Multiply through by $x(x+1)(x+2)$ and use the cover-up rule at the roots:
$$ x=0:\ A=\frac{3}{(1)(2)}=\frac32;\qquad x=-1:\ B=\frac{2+3}{(-1)(1)}=-5;\qquad x=-2:\ C=\frac{8+3}{(-2)(-1)}=\frac{11}{2} $$
$$ \int\frac{2x^{2}+3}{x^{3}+3x^{2}+2x}dx=\frac32\ln|x|-5\ln|x+1|+\frac{11}{2}\ln|x+2|+C $$

**2.** (a) $x^{3}-x^{2}-2x=x(x-2)(x+1)$ and
$$ \frac{1}{x(x-2)(x+1)}=\frac{A}{x}+\frac{B}{x-2}+\frac{C}{x+1} $$
By the cover-up rule: $A=\dfrac{1}{(-2)(1)}=-\dfrac12$, $B=\dfrac{1}{(2)(3)}=\dfrac16$, $C=\dfrac{1}{(-1)(-3)}=\dfrac13$.
$$ \int\frac{dx}{x^{3}-x^{2}-2x}=-\frac12\ln|x|+\frac16\ln|x-2|+\frac13\ln|x+1|+C $$
(b) $9x^{2}+1=9\big(x^{2}+\tfrac19\big)$, so with $a=\dfrac13$:
$$ \int\frac{dx}{9x^{2}+1}=\frac19\cdot\frac{1}{1/3}\tan^{-1}(3x)+C=\frac13\tan^{-1}(3x)+C $$

**3.** $x^{3}+4x=x(x^{2}+4)$, and the quadratic factor is irreducible:
$$ \frac{2x^{2}-x+4}{x(x^{2}+4)}=\frac{A}{x}+\frac{Bx+C}{x^{2}+4} $$
$$ 2x^{2}-x+4=A(x^{2}+4)+(Bx+C)x $$
Put $x=0$: $4=4A$, $A=1$. Compare $x^{2}$: $2=A+B$, $B=1$. Compare $x$: $-1=C$.
$$ \int\Big[\frac1x+\frac{x-1}{x^{2}+4}\Big]dx=\ln|x|+\frac12\ln(x^{2}+4)-\frac12\tan^{-1}\frac{x}{2}+C $$
using $\int\dfrac{x}{x^{2}+4}dx=\dfrac12\ln(x^{2}+4)$ and $\int\dfrac{dx}{x^{2}+4}=\dfrac12\tan^{-1}\dfrac x2$.

**4.** (a) Put $e^{x}=t$, so $e^{x}dx=dt$ and $dx=\dfrac{dt}{t}$:
$$ \int\frac{dx}{1-e^{x}}=\int\frac{dt}{t(1-t)}=\int\Big[\frac1t+\frac{1}{1-t}\Big]dt=\ln|t|-\ln|1-t|+c $$
$$ =\ln|e^{x}|-\ln|1-e^{x}|+c $$ ∎
(b) $\dfrac{1}{x^{2}-1}=\dfrac12\Big[\dfrac{1}{x-1}-\dfrac{1}{x+1}\Big]$, so
$$ \int\frac{dx}{x^{2}-1}=\frac12\ln\Big|\frac{x-1}{x+1}\Big|+C $$
Note the order: $\dfrac{x-1}{x+1}$, not $\dfrac{x+1}{x-1}$ — the distractor in the 2080 key.

**5.** Put $t=\tan\dfrac x2$, so $\cos x=\dfrac{1-t^{2}}{1+t^{2}}$ and $dx=\dfrac{2\,dt}{1+t^{2}}$:
$$ 5-3\cos x=\frac{5(1+t^{2})-3(1-t^{2})}{1+t^{2}}=\frac{2+8t^{2}}{1+t^{2}} $$
$$ \int\frac{dx}{5-3\cos x}=\int\frac{1+t^{2}}{2+8t^{2}}\cdot\frac{2\,dt}{1+t^{2}}=\int\frac{dt}{1+4t^{2}} $$
$$ =\frac12\tan^{-1}(2t)+C=\frac12\tan^{-1}\Big(2\tan\frac x2\Big)+C $$
:::

**Long answer questions [8 marks each]**

1. (a) Show that $\displaystyle\int\frac{dx}{a+b\cos x}$ depends on the relative sizes of $a$ and $b$: evaluate it for $a>b>0$ and state the results for $a<b$ and $a=b$. [4] (b) Evaluate $\displaystyle\int\frac{dx}{3+2\cos x}$. [2] (c) Evaluate $\displaystyle\int\frac{2x+3}{x^{2}+4x+13}\,dx$. [2] <span class="marks">[8]</span> (NEB 2081, part b)

::: note Model answer — long
**1.** (a) Put $t=\tan\dfrac x2$, so $a+b\cos x=\dfrac{(a+b)+(a-b)t^{2}}{1+t^{2}}$ and $dx=\dfrac{2\,dt}{1+t^{2}}$:
$$ \int\frac{dx}{a+b\cos x}=\int\frac{2\,dt}{(a+b)+(a-b)t^{2}} $$
**Case $a>b$:** $a-b>0$, so the denominator is a sum of squares:
$$ =\frac{2}{a-b}\int\frac{dt}{t^{2}+\frac{a+b}{a-b}}=\frac{2}{\sqrt{a^{2}-b^{2}}}\tan^{-1}\Big(\sqrt{\frac{a-b}{a+b}}\tan\frac x2\Big)+C $$
**Case $a<b$:** $a-b<0$, the denominator is a difference of squares and the result is logarithmic:
$$ \frac{1}{\sqrt{b^{2}-a^{2}}}\ln\Bigg|\frac{\sqrt{b+a}+\sqrt{b-a}\tan\frac x2}{\sqrt{b+a}-\sqrt{b-a}\tan\frac x2}\Bigg|+C $$
**Case $a=b$:** $a(1+\cos x)=2a\cos^{2}\dfrac x2$, so the integral is $\dfrac{1}{2a}\displaystyle\int\sec^{2}\dfrac x2\,dx=\dfrac1a\tan\dfrac x2+C$.
So the integral has an inverse-tangent form, a logarithmic form, or a tangent form according as $a>b$, $a<b$ or $a=b$.

(b) Here $a=3>b=2$: $\sqrt{a^{2}-b^{2}}=\sqrt{5}$ and $\sqrt{\dfrac{a-b}{a+b}}=\dfrac{1}{\sqrt{5}}$:
$$ \int\frac{dx}{3+2\cos x}=\frac{2}{\sqrt{5}}\tan^{-1}\Big(\frac{1}{\sqrt{5}}\tan\frac x2\Big)+C $$
(c) Write the numerator in terms of the derivative of the denominator, $\dfrac{d}{dx}(x^{2}+4x+13)=2x+4$:
$$ 2x+3=(2x+4)-1 $$
$$ \int\frac{2x+4}{x^{2}+4x+13}dx=\ln(x^{2}+4x+13) $$
and, completing the square $x^{2}+4x+13=(x+2)^{2}+9$,
$$ \int\frac{-1}{(x+2)^{2}+9}dx=-\frac13\tan^{-1}\frac{x+2}{3} $$
$$ \int\frac{2x+3}{x^{2}+4x+13}dx=\ln(x^{2}+4x+13)-\frac13\tan^{-1}\frac{x+2}{3}+C $$
:::

::: tip Examiner's note — Anti-derivatives
Most repeated: **partial fractions** with distinct linear factors (2079, 2082) or a linear × irreducible quadratic (2081), and **$\int dx/(a+b\cos x)$**. The substitution $t=\tan\frac x2$ and its three identities are worth memorising. Marks are lost for forgetting the constant $C$ and for mis-ordering the log quotient in $\int dx/(x^{2}-a^{2})$.
:::

## 12.14 Differential Equations

CDC allots **12 hours**. Three of the four verified papers carry differential-equation MCQs in Group A (2079 Q9, 2081 Q9–Q10, 2082 Q9–Q10); all four have a solve-it part (2079 Q15b, 2080 Q17a, 2082 Q22c) and a modelling or theory part in Group C (2079 Q22, 2080 Q22c, 2081 Q22c).

| Type | Method |
|---|---|
| Separable $f(y)\,dy=g(x)\,dx$ | integrate both sides |
| Homogeneous $\dfrac{dy}{dx}=F\Big(\dfrac{y}{x}\Big)$ | put $y=vx$, separate |
| Linear $\dfrac{dy}{dx}+Py=Q$ | I.F. $=e^{\int P\,dx}$; $y\cdot\text{I.F.}=\int Q\cdot\text{I.F.}\,dx$ |
| Exact $M\,dx+N\,dy=0$ | test $\dfrac{\partial M}{\partial y}=\dfrac{\partial N}{\partial x}$; solve $\int M\,dx+\int(\text{terms of }N\text{ free of }x)\,dy=C$ |
| Order, degree | highest derivative; its power after removing radicals and fractions |

**Short answer questions [5 marks each]**

1. (a) Find the integrating factor of $\sin x\dfrac{dy}{dx}+y\cos x=x\sin x$. [2] (b) Solve $(1+x)\,dy=dx\,(1+xy-x)$. [3] <span class="marks">[5]</span> (NEB 2079, Q9 and Q15b)
2. (a) Solve $\dfrac{dy}{dx}=\dfrac{1+y^{2}}{1+x^{2}}$. [2] (b) Solve $\dfrac{dy}{dx}=e^{x-y}$. [3] <span class="marks">[5]</span> (NEB 2080, part a; also NEB 2082 Q22c)
3. (a) Give an example of an exact differential equation and solve it, stating the characteristic of $M$ and $N$. [2] (b) Solve the homogeneous equation $(x^{2}+y^{2})\,dx=2xy\,dy$. [3] <span class="marks">[5]</span> (NEB 2081, part c)
4. (a) Find the order and degree of $\dfrac{d^{3}s}{dt^{3}}=\Big(4+\Big(\dfrac{d^{2}s}{dt^{2}}\Big)^{2}\Big)^{1/2}$. [2] (b) For $\dfrac{dv}{dt}=g\cos\alpha-kv$, where $g$, $\alpha$, $k$ are constants, find $v$, and state under which condition the formula for the solution fails. [3] <span class="marks">[5]</span> (NEB 2081 Q9; NEB 2080 Q22c)

::: note Model answers — short
**1.** (a) Divide by $\sin x$: $\dfrac{dy}{dx}+\cot x\cdot y=x$. So $P=\cot x$ and
$$ \text{I.F.}=e^{\int\cot x\,dx}=e^{\ln\sin x}=\sin x $$
(The left side is exactly $\dfrac{d}{dx}(y\sin x)$ — that is why the I.F. is $\sin x$.)
(b) Rewrite as a linear equation:
$$ \frac{dy}{dx}=\frac{1+xy-x}{1+x}\;\Rightarrow\;\frac{dy}{dx}-\frac{x}{1+x}\,y=\frac{1-x}{1+x} $$
$$ \int P\,dx=-\int\frac{x}{1+x}dx=-\int\Big(1-\frac{1}{1+x}\Big)dx=-x+\ln(1+x) $$
$$ \text{I.F.}=e^{-x+\ln(1+x)}=(1+x)e^{-x} $$
$$ y(1+x)e^{-x}=\int\frac{1-x}{1+x}(1+x)e^{-x}dx=\int(1-x)e^{-x}dx=xe^{-x}+C $$
because $\dfrac{d}{dx}\big(xe^{-x}\big)=(1-x)e^{-x}$. Therefore
$$ y=\frac{x+Ce^{x}}{1+x} $$
**Check:** $y'=\dfrac{(1+Ce^{x})(1+x)-(x+Ce^{x})}{(1+x)^{2}}$; substituting into $(1+x)y'-\dfrac{x(1+x)}{1+x}\,y$ reproduces $1-x$. ✓

**2.** (a) Separate the variables:
$$ \frac{dy}{1+y^{2}}=\frac{dx}{1+x^{2}}\;\Rightarrow\;\tan^{-1}y=\tan^{-1}x+C $$
or equivalently $\dfrac{y-x}{1+xy}=c$.
(b) $\dfrac{dy}{dx}=e^{x}e^{-y}$, so $e^{y}\,dy=e^{x}\,dx$:
$$ e^{y}=e^{x}+C $$

**3.** (a) **Example:** $(2xy+3)\,dx+(x^{2}+4y)\,dy=0$. Here $M=2xy+3$, $N=x^{2}+4y$, and
$$ \frac{\partial M}{\partial y}=2x=\frac{\partial N}{\partial x} $$
This equality is the **characteristic** of an exact equation: $M\,dx+N\,dy$ is then the total differential of some $F(x,y)$. Solution: $\int M\,dx=x^{2}y+3x$ (treating $y$ as constant); the terms of $N$ free of $x$ are $4y$, giving $2y^{2}$:
$$ x^{2}y+3x+2y^{2}=C $$
(b) $\dfrac{dy}{dx}=\dfrac{x^{2}+y^{2}}{2xy}$ is homogeneous of degree $0$. Put $y=vx$, $\dfrac{dy}{dx}=v+x\dfrac{dv}{dx}$:
$$ v+x\frac{dv}{dx}=\frac{1+v^{2}}{2v}\;\Rightarrow\;x\frac{dv}{dx}=\frac{1-v^{2}}{2v} $$
$$ \int\frac{2v}{1-v^{2}}dv=\int\frac{dx}{x}\;\Rightarrow\;-\ln|1-v^{2}|=\ln|x|+c' $$
$$ x(1-v^{2})=C\;\Rightarrow\;x\Big(1-\frac{y^{2}}{x^{2}}\Big)=C\;\Rightarrow\;x^{2}-y^{2}=Cx $$

**4.** (a) The highest derivative is $\dfrac{d^{3}s}{dt^{3}}$, so the **order is $3$**. Square to remove the radical:
$$ \Big(\frac{d^{3}s}{dt^{3}}\Big)^{2}=4+\Big(\frac{d^{2}s}{dt^{2}}\Big)^{2} $$
The highest derivative appears to the power $2$, so the **degree is $2$**.
(b) This is linear: $\dfrac{dv}{dt}+kv=g\cos\alpha$, $P=k$, I.F. $=e^{kt}$:
$$ ve^{kt}=\int g\cos\alpha\,e^{kt}dt=\frac{g\cos\alpha}{k}e^{kt}+C\;\Rightarrow\;v=\frac{g\cos\alpha}{k}+Ce^{-kt} $$
This formula fails when $k=0$, because it divides by $k$. The equation itself still has a solution then: $\dfrac{dv}{dt}=g\cos\alpha$ gives $v=gt\cos\alpha+C$. So it is the **closed form** that does not exist for $k=0$, not the solution of the equation (an answer the examiner's scheme for this item may phrase simply as "$k\neq0$").
:::

**Long answer questions [8 marks each]**

1. A water tank is filled in such a way that the rate at which the depth $h$ of water increases is proportional to the square root of the depth. Initially the depth is $n$ metres. (a) Write down a differential equation for $h$. [2] (b) Show that $\sqrt{h}=\dfrac{kt}{2}+\sqrt{n}$, where $k$ is a constant. [4] (c) When $h=16$ and $t=6$ hours, prove that $n=(4-3k)^{2}$. [2] <span class="marks">[8]</span> (NEB 2079)

::: note Model answer — long
**1.** (a) "Rate of increase of depth proportional to the square root of the depth":
$$ \frac{dh}{dt}=k\sqrt{h} $$
(b) Separate the variables and integrate:
$$ \frac{dh}{\sqrt{h}}=k\,dt\;\Rightarrow\;\int h^{-1/2}dh=\int k\,dt\;\Rightarrow\;2\sqrt{h}=kt+C $$
Initially $t=0$ and $h=n$, so $C=2\sqrt{n}$:
$$ 2\sqrt{h}=kt+2\sqrt{n}\;\Rightarrow\;\sqrt{h}=\frac{kt}{2}+\sqrt{n} $$ ∎
(c) Put $h=16$, $t=6$: $\sqrt{16}=\dfrac{6k}{2}+\sqrt{n}$, so
$$ 4=3k+\sqrt{n}\;\Rightarrow\;\sqrt{n}=4-3k\;\Rightarrow\;n=(4-3k)^{2} $$ ∎
:::

::: tip Examiner's note — Differential Equations
Most repeated: **linear first-order with an integrating factor** (2079, 2081, 2082), **separable** (2080, 2082), the **order/degree and "is it homogeneous?"** MCQs (2081, 2082), and **a modelling equation set up from words** (2079 Q22). Identify the type in one line before solving — the examiner's scheme gives a mark for naming it. Never forget $+C$, and apply the initial condition when one is given.
:::

## 12.15 Computational Methods

CDC allots **12 hours** and this unit is **one of two optional areas** (the other is Mechanics). The grid gives it $6$ marks: one Group A item and one Group B question. **A simplex LPP has appeared as a five-mark Group B question in every verified year** (compulsory in 2079 Q18 and 2080 Q18; as the Computational Methods option in 2081 Q19, 2082 Q19 and CDC model Q19b), and every year's MCQ about eliminating $x$ or $y$ from two equations belongs here too.

| Method | Rule |
|---|---|
| Gauss elimination | reduce the augmented matrix to triangular form, then back-substitute |
| Gauss–Seidel | rewrite each equation for its diagonal unknown; always use the **newest** value; start from $(0,0,0)$ unless told |
| Convergence | guaranteed if the matrix is **diagonally dominant** |
| Simplex | add slack variables; pivot column = most negative entry of the $Z$-row; pivot row = least ratio $\dfrac{\text{RHS}}{\text{column entry}}$ (positive entries only); stop when the $Z$-row has no negatives |

**Short answer questions [5 marks each]**

1. Solve $2x+y+z=7$, $x+3y+2z=13$, $3x+2y+z=10$ by Gauss elimination with partial pivoting. <span class="marks">[5]</span>
2. Using the simplex method, maximise $Z=7x+y$ subject to $3x+4y\leq12$, $y-x\leq2$, $x,y\geq0$. <span class="marks">[5]</span> (NEB 2079)
3. Using the simplex method, maximise $Z=25x+35y$ subject to $2x+3y\leq15$, $3x+y\leq12$, $x,y\geq0$. <span class="marks">[5]</span> (NEB 2081)
4. Using the simplex method, maximise $P=7x+5y$ subject to $\dfrac{x}{3}+\dfrac{y}{4}\leq1$, $\dfrac{x}{6}+\dfrac{y}{3}\leq1$, $x,y\geq0$. <span class="marks">[5]</span> (NEB 2080)

::: note Model answers — short
**1.** The largest coefficient in column 1 is $3$ (row 3), so interchange $R_1\leftrightarrow R_3$ (partial pivoting):
$$ 3x+2y+z=10,\quad x+3y+2z=13,\quad 2x+y+z=7 $$
Eliminate $x$ with $R_2\to3R_2-R_1$ and $R_3\to3R_3-2R_1$:
$$ 7y+5z=29,\qquad -y+z=1 $$
Eliminate $y$ with $R_3\to7R_3+R_2$: $12z=36$, so $z=3$. Back-substitute:
$$ 7y+15=29\;\Rightarrow\;y=2,\qquad 3x+4+3=10\;\Rightarrow\;x=1 $$
$$ (x,y,z)=(1,2,3) $$
**Check:** $2+2+3=7$ ✓; $1+6+6=13$ ✓; $3+4+3=10$ ✓.

**2.** Add slack variables: $3x+4y+s_1=12$, $-x+y+s_2=2$, and $Z-7x-y=0$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $s_1$ | 3 | 4 | 1 | 0 | 12 |
| $s_2$ | $-1$ | 1 | 0 | 1 | 2 |
| $Z$ | $-7$ | $-1$ | 0 | 0 | 0 |

Most negative in the $Z$-row: $-7$, so $x$ enters. Ratios: $\dfrac{12}{3}=4$ (the entry $-1$ is ignored), so $s_1$ leaves; pivot $=3$. Divide $R_1$ by $3$, then $R_2\to R_2+R_1$, $Z\to Z+7R_1$:

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | 1 | $\frac43$ | $\frac13$ | 0 | 4 |
| $s_2$ | 0 | $\frac73$ | $\frac13$ | 1 | 6 |
| $Z$ | 0 | $\frac{25}{3}$ | $\frac73$ | 0 | 28 |

No negative entry remains in the $Z$-row, so the solution is optimal:
$$ x=4,\quad y=0,\quad Z_{max}=28 $$
**Check at the corner points** of the feasible region: $(0,0)\to0$; $(4,0)\to28$; $\big(\tfrac47,\tfrac{18}{7}\big)\to6.57$; $(0,2)\to2$. The maximum is $28$ at $(4,0)$. ✓

**3.** Slack form: $2x+3y+s_1=15$, $3x+y+s_2=12$, $Z-25x-35y=0$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $s_1$ | 2 | 3 | 1 | 0 | 15 |
| $s_2$ | 3 | 1 | 0 | 1 | 12 |
| $Z$ | $-25$ | $-35$ | 0 | 0 | 0 |

$y$ enters ($-35$). Ratios: $\dfrac{15}{3}=5$, $\dfrac{12}{1}=12$; $s_1$ leaves, pivot $3$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $y$ | $\frac23$ | 1 | $\frac13$ | 0 | 5 |
| $s_2$ | $\frac73$ | 0 | $-\frac13$ | 1 | 7 |
| $Z$ | $-\frac53$ | 0 | $\frac{35}{3}$ | 0 | 175 |

$x$ enters ($-\frac53$). Ratios: $\dfrac{5}{2/3}=7.5$, $\dfrac{7}{7/3}=3$; $s_2$ leaves, pivot $\frac73$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $y$ | 0 | 1 | $\frac37$ | $-\frac27$ | 3 |
| $x$ | 1 | 0 | $-\frac17$ | $\frac37$ | 3 |
| $Z$ | 0 | 0 | $\frac{80}{7}$ | $\frac57$ | 180 |

All $Z$-row entries are non-negative:
$$ x=3,\quad y=3,\quad Z_{max}=180 $$
**Check:** $2(3)+3(3)=15$ ✓, $3(3)+3=12$ ✓, $25(3)+35(3)=180$ ✓.

**4.** Clear fractions: $\dfrac x3+\dfrac y4\leq1\Rightarrow4x+3y\leq12$ and $\dfrac x6+\dfrac y3\leq1\Rightarrow x+2y\leq6$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $s_1$ | 4 | 3 | 1 | 0 | 12 |
| $s_2$ | 1 | 2 | 0 | 1 | 6 |
| $P$ | $-7$ | $-5$ | 0 | 0 | 0 |

$x$ enters ($-7$); ratios $\dfrac{12}{4}=3$, $\dfrac61=6$; $s_1$ leaves, pivot $4$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | 1 | $\frac34$ | $\frac14$ | 0 | 3 |
| $s_2$ | 0 | $\frac54$ | $-\frac14$ | 1 | 3 |
| $P$ | 0 | $\frac14$ | $\frac74$ | 0 | 21 |

No negatives remain:
$$ x=3,\quad y=0,\quad P_{max}=21 $$
**Check:** corner points $(0,0)\to0$, $(3,0)\to21$, $(1.2,2.4)\to20.4$, $(0,3)\to15$. The maximum is $21$. ✓
:::

**Long answer questions [8 marks each]**

1. (a) Solve $10x+y+z=12$, $2x+10y+z=13$, $2x+2y+10z=14$ by the Gauss–Seidel method, starting from $(0,0,0)$ and carrying three iterations to four decimal places; say why the method converges. [4] (b) Using the simplex method, maximise $P=10x+3y$ subject to $6x+7y\leq42$, $x+3y\leq9$, $x,y\geq0$. [4] <span class="marks">[8]</span> (CDC model 2080 part 19-type; NEB 2082 Q19)

::: note Model answer — long
**1.** (a) **Convergence:** in each row the diagonal entry exceeds the sum of the others ($10>1+1$, $10>2+1$, $10>2+2$), so the matrix is **diagonally dominant** and the iteration converges.
Solve each equation for its diagonal unknown:
$$ x=\frac{12-y-z}{10},\qquad y=\frac{13-2x-z}{10},\qquad z=\frac{14-2x-2y}{10} $$

| Iteration | $x$ | $y$ | $z$ |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 1.2000 | 1.0600 | 0.9480 |
| 2 | 0.9992 | 1.0054 | 0.9991 |
| 3 | 0.9996 | 1.0002 | 1.0001 |

Working for iteration 1: $x=\dfrac{12-0-0}{10}=1.2$; $y=\dfrac{13-2(1.2)-0}{10}=1.06$ (uses the new $x$); $z=\dfrac{14-2(1.2)-2(1.06)}{10}=0.948$.
The iterates approach $(1,1,1)$, which satisfies all three equations exactly.

(b) The printed 2082 question lists three constraints, $6x+7y\leq42$, $x+3y\leq42$ and $x+3y\leq9$; the middle one is redundant (implied by $x+3y\leq9$), so two constraints are used here.
Slack form: $6x+7y+s_1=42$, $x+3y+s_2=9$, $P-10x-3y=0$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $s_1$ | 6 | 7 | 1 | 0 | 42 |
| $s_2$ | 1 | 3 | 0 | 1 | 9 |
| $P$ | $-10$ | $-3$ | 0 | 0 | 0 |

$x$ enters ($-10$). Ratios: $\dfrac{42}{6}=7$, $\dfrac91=9$; $s_1$ leaves, pivot $6$.

| Basis | $x$ | $y$ | $s_1$ | $s_2$ | RHS |
|---|---|---|---|---|---|
| $x$ | 1 | $\frac76$ | $\frac16$ | 0 | 7 |
| $s_2$ | 0 | $\frac{11}{6}$ | $-\frac16$ | 1 | 2 |
| $P$ | 0 | $\frac{26}{3}$ | $\frac53$ | 0 | 70 |

No negatives remain:
$$ x=7,\quad y=0,\quad P_{max}=70 $$
**Check:** corner points $(0,0)\to0$, $(7,0)\to70$, $\big(\tfrac{63}{11},\tfrac{12}{11}\big)\to60.5$, $(0,3)\to9$. ✓
:::

::: tip Examiner's note — Computational Methods
Most repeated: **simplex in two variables** (every year); **Gauss–Seidel** (CDC model Q19a); and the **eliminate $x$ / $y$** MCQ. In a simplex answer, examiners look for the slack-variable form, the initial table, the naming of the entering column and leaving row, the final table, and the stated optimum $(x,y,Z)$. Never pick a pivot from a zero or negative column entry.
:::

## 12.16 Mechanics (alternative to Unit 15)

CDC allots **12 hours**. This is the other optional area. In 2081, 2082 and the CDC model the two "Or" slots (Q11 and Q19) pair Computational Methods against Mechanics. In 2079 and 2080 the simplex question was compulsory (Q18) and Mechanics was paired with an input–output (economics) alternative that does not appear in the published 2078 curriculum, so it is not covered in this book. Mechanics was set in **2079 (projectile), 2080 (like parallel forces), 2081 (tensions; rocket), 2082 (inclined plane; maximum height) and the CDC model (bullet; like parallel forces)**.

| Result | Formula |
|---|---|
| Triangle law | three forces in equilibrium form a closed triangle |
| Lami's theorem | $\dfrac{P}{\sin\alpha}=\dfrac{Q}{\sin\beta}=\dfrac{R}{\sin\gamma}$ ($\alpha,\beta,\gamma$ the angles **opposite** each force) |
| Like parallel forces | $P\cdot AC=Q\cdot CB$, resultant $P+Q$ between them, nearer the larger |
| Newton's second law | $F=\dfrac{d(mv)}{dt}$; constant mass: $F=ma$ |
| Weight | $W=mg$ |
| Projectile ($u$, angle $\theta$) | time to top $\dfrac{u\sin\theta}{g}$; flight $\dfrac{2u\sin\theta}{g}$; height $\dfrac{u^{2}\sin^{2}\theta}{2g}$; range $\dfrac{u^{2}\sin2\theta}{g}$ |

```figure caption="A projectile launched at angle $\theta$ with speed $u$. The greatest height $H$ is reached at half the range $R$; the maximum range for a given $u$ occurs at $\theta=45^{\circ}$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.8, 2.6))
u, th, g = 10.0, np.radians(35), 9.8
T = 2*u*np.sin(th)/g
t = np.linspace(0, T, 200)
x = u*np.cos(th)*t; y = u*np.sin(th)*t - 0.5*g*t*t
R = x[-1]; H = y.max()
ax.plot(x, y, color=INK, lw=1.8)
ax.axhline(0, color=MUTED, lw=0.8)
ax.annotate("", xy=(2.2, 2.2*np.tan(th)), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.4))
ax.text(1.35, 0.15, r"$\theta$", color=INK, fontsize=10)
ax.text(0.6, 1.25, "$u$", color=ACCENT, fontsize=10)
ax.plot([R/2, R/2], [0, H], color=MUTED, lw=0.9, ls="--")
ax.text(R/2 + 0.1, H/2, "$H$", color=INK, fontsize=10)
ax.annotate("", xy=(R, -0.35), xytext=(0, -0.35), arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.9))
ax.text(R/2, -0.75, "$R$", ha="center", color=INK, fontsize=10)
ax.set_xlim(-0.4, R + 0.6); ax.set_ylim(-1.0, H + 0.6)
ax.axis("off")
```

**Short answer questions [5 marks each]**

1. A body of weight $78$ N is suspended by two strings of lengths $4$ m and $3$ m attached to two points in the same horizontal line $5$ m apart. Find the tensions in the strings. <span class="marks">[5]</span> (NEB 2081, Or, part a, here with 5 marks)
2. Two forces $A$ and $B$, acting parallel to the length and to the base of an inclined plane respectively, would each singly support a weight $R$ on the plane. Prove that $\dfrac{1}{A^{2}}=\dfrac{1}{B^{2}}+\dfrac{1}{R^{2}}$. <span class="marks">[5]</span> (NEB 2082, Or)
3. $X$ and $Y$ are two like parallel forces ($X>Y$) acting at $A$ and $B$. Show that if they interchange positions, the point of application of the resultant is displaced a distance $\dfrac{X-Y}{X+Y}\,AB$. <span class="marks">[5]</span> (NEB 2080 Q19)
4. A particle is thrown with initial velocity $120\ \text{m s}^{-1}$ at $30^{\circ}$ above the horizontal ($g=10\ \text{m s}^{-2}$). Find (a) the time to reach the highest point, (b) the time of flight, (c) the horizontal range, (d) the greatest height, (e) the maximum horizontal range for this speed. [1+1+1+1+1] <span class="marks">[5]</span> (NEB 2079 Q19)
5. (a) A bullet of mass $25$ g moving at $250\ \text{m s}^{-1}$ penetrates a tree trunk and is brought to rest in $0.02$ s. Find the distance of penetration. [3] (b) Find two like parallel forces acting $2.5$ m apart whose resultant is $30$ N, the line of action of one being $50$ cm from the resultant. [2] <span class="marks">[5]</span> (CDC model 2080, Or)

::: note Model answers — short
**1.** The two strings and the line joining the supports form a triangle with sides $4$, $3$, $5$. Since $3^{2}+4^{2}=5^{2}$, the angle at the body is $90^{\circ}$. Let $T_{1}$ be the tension in the $4$ m string and $T_{2}$ in the $3$ m string. The $4$ m string makes an angle $A$ with the horizontal and the $3$ m string an angle $B$, where
$$ \cos A=\frac{4}{5},\ \sin A=\frac35;\qquad \cos B=\frac35,\ \sin B=\frac45 $$
Horizontal equilibrium: $T_{1}\cos A=T_{2}\cos B$, so $\dfrac45T_{1}=\dfrac35T_{2}$, $T_{1}=\dfrac34T_{2}$.
Vertical equilibrium: $T_{1}\sin A+T_{2}\sin B=78$:
$$ \frac35\Big(\frac34T_{2}\Big)+\frac45T_{2}=78\;\Rightarrow\;\frac{9}{20}T_{2}+\frac{16}{20}T_{2}=78\;\Rightarrow\;T_{2}=62.4\ \text{N} $$
$$ T_{1}=\frac34\times62.4=46.8\ \text{N} $$
**Check:** the strings are perpendicular, so $T_{1}^{2}+T_{2}^{2}$ must equal $78^{2}$: $46.8^{2}+62.4^{2}=2190.24+3893.76=6084=78^{2}$. ✓

**2.** Let the plane make angle $\alpha$ with the horizontal and let the weight be $R$.
*Force $A$ parallel to the plane.* Resolving along the plane, $A=R\sin\alpha$.
*Force $B$ horizontal (parallel to the base).* Resolving along the plane, $B\cos\alpha=R\sin\alpha$, so $B=R\tan\alpha$.
Then
$$ \frac{1}{B^{2}}+\frac{1}{R^{2}}=\frac{\cot^{2}\alpha}{R^{2}}+\frac{1}{R^{2}}=\frac{1+\cot^{2}\alpha}{R^{2}}=\frac{\text{cosec}^{2}\alpha}{R^{2}}=\frac{1}{R^{2}\sin^{2}\alpha}=\frac{1}{A^{2}} $$ ∎

**3.** *Before the interchange:* $X$ at $A$, $Y$ at $B$. The resultant $X+Y$ acts at $P$ between $A$ and $B$ with $X\cdot AP=Y\cdot PB$. Since $AP+PB=AB$,
$$ AP=\frac{Y\cdot AB}{X+Y} $$
*After the interchange:* $Y$ at $A$, $X$ at $B$. The new point $P'$ satisfies $Y\cdot AP'=X\cdot P'B$, so
$$ AP'=\frac{X\cdot AB}{X+Y} $$
Both points lie on $AB$ measured from $A$, so the displacement is
$$ PP'=AP'-AP=\frac{(X-Y)\,AB}{X+Y} $$ ∎ (Because $X>Y$, the resultant moves towards $B$.)

**4.** $u=120$, $\theta=30^{\circ}$, $\sin\theta=\dfrac12$, $g=10$.
(a) Time to the highest point: $\dfrac{u\sin\theta}{g}=\dfrac{120\times0.5}{10}=6\ \text{s}$.
(b) Time of flight: $2\times6=12\ \text{s}$.
(c) Range: $\dfrac{u^{2}\sin2\theta}{g}=\dfrac{14400\times\sin60^{\circ}}{10}=1440\times0.8660=1247\ \text{m}$ $(=720\sqrt{3}\ \text{m})$.
(d) Greatest height: $\dfrac{u^{2}\sin^{2}\theta}{2g}=\dfrac{14400\times0.25}{20}=180\ \text{m}$.
(e) Maximum range at $\theta=45^{\circ}$: $\dfrac{u^{2}}{g}=\dfrac{14400}{10}=1440\ \text{m}$.

**5.** (a) $m=0.025$ kg, $u=250\ \text{m s}^{-1}$, final $v=0$, $t=0.02$ s. Retardation:
$$ a=\frac{v-u}{t}=\frac{0-250}{0.02}=-12\,500\ \text{m s}^{-2} $$
$$ s=ut+\tfrac12at^{2}=250(0.02)-\tfrac12(12\,500)(0.02)^{2}=5-2.5=2.5\ \text{m} $$
(Equivalently $s=\dfrac{u+v}{2}\,t=125\times0.02=2.5$ m. The resisting force is $ma=0.025\times12\,500=312.5$ N.)
(b) Let the forces be $P$ at distance $0.5$ m and $Q$ at distance $2.5-0.5=2.0$ m from the line of action of the resultant. Moments about the resultant balance: $P(0.5)=Q(2.0)$, so $P=4Q$. And $P+Q=30$:
$$ 5Q=30\;\Rightarrow\;Q=6\ \text{N},\qquad P=24\ \text{N} $$
:::

**Long answer questions [8 marks each]**

1. (a) State and prove Lami's theorem. [4] (b) A lamp of weight $100$ N hangs from two strings making angles of $30^{\circ}$ and $60^{\circ}$ with the horizontal ceiling line. Find the tension in each string. [4] <span class="marks">[8]</span>
2. (a) Derive, for a projectile launched with speed $u$ at angle $\theta$, the time of flight, the greatest height and the horizontal range. [4] (b) A particle is projected with speed $60\ \text{m s}^{-1}$ at $30^{\circ}$ to the horizontal ($g=10\ \text{m s}^{-2}$). Find the greatest height, the time of flight and the range. [4] <span class="marks">[8]</span>

::: note Model answers — long
**1.** (a) **Lami's theorem:** if three forces $P$, $Q$, $R$ acting at a point keep it in equilibrium, each force is proportional to the sine of the angle between the other two:
$$ \frac{P}{\sin\alpha}=\frac{Q}{\sin\beta}=\frac{R}{\sin\gamma} $$
where $\alpha$ is the angle between $Q$ and $R$, $\beta$ between $R$ and $P$, $\gamma$ between $P$ and $Q$.
**Proof.** By the triangle law the three forces, taken in order, form the sides of a closed triangle. The sides of this triangle are parallel to $P$, $Q$, $R$, and the interior angles are $180^{\circ}-\alpha$, $180^{\circ}-\beta$, $180^{\circ}-\gamma$ (the angle between two forces and the interior angle of the force triangle are supplementary). By the sine rule on this triangle,
$$ \frac{P}{\sin(180^{\circ}-\alpha)}=\frac{Q}{\sin(180^{\circ}-\beta)}=\frac{R}{\sin(180^{\circ}-\gamma)} $$
and $\sin(180^{\circ}-\theta)=\sin\theta$, which gives Lami's theorem. ∎
(b) Let $T_{1}$ act at $30^{\circ}$ to the horizontal and $T_{2}$ at $60^{\circ}$. The angle between the two strings is $180^{\circ}-30^{\circ}-60^{\circ}=90^{\circ}$. The angle between $T_{1}$ and the weight (vertical) is $90^{\circ}+30^{\circ}=120^{\circ}$, and between $T_{2}$ and the weight is $90^{\circ}+60^{\circ}=150^{\circ}$. By Lami:
$$ \frac{T_{1}}{\sin150^{\circ}}=\frac{T_{2}}{\sin120^{\circ}}=\frac{100}{\sin90^{\circ}} $$
$$ T_{1}=100\times\tfrac12=50\ \text{N},\qquad T_{2}=100\times\frac{\sqrt{3}}{2}=86.6\ \text{N} $$
**Check (resolving):** horizontal $50\cos30^{\circ}=43.3=86.6\cos60^{\circ}$ ✓; vertical $50\sin30^{\circ}+86.6\sin60^{\circ}=25+75=100$ ✓.

**2.** (a) Take the origin at the point of projection, $x$ horizontal and $y$ upward. Initial velocity components: $u\cos\theta$ and $u\sin\theta$. Horizontal motion is uniform; vertical motion has acceleration $-g$:
$$ x=u\cos\theta\,t,\qquad y=u\sin\theta\,t-\tfrac12gt^{2} $$
*Time of flight:* the particle returns to the ground when $y=0$, $t\neq0$:
$$ t\Big(u\sin\theta-\tfrac12gt\Big)=0\;\Rightarrow\;T=\frac{2u\sin\theta}{g} $$
*Greatest height:* at the top the vertical velocity $u\sin\theta-gt=0$, at $t=\dfrac{u\sin\theta}{g}$. Substituting,
$$ H=u\sin\theta\cdot\frac{u\sin\theta}{g}-\frac12g\frac{u^{2}\sin^{2}\theta}{g^{2}}=\frac{u^{2}\sin^{2}\theta}{2g} $$
*Range:* horizontal distance in time $T$:
$$ R=u\cos\theta\cdot\frac{2u\sin\theta}{g}=\frac{u^{2}\sin2\theta}{g} $$
(b) $u=60$, $\theta=30^{\circ}$, $g=10$:
$$ H=\frac{3600\times\frac14}{20}=45\ \text{m} $$
$$ T=\frac{2\times60\times\frac12}{10}=6\ \text{s} $$
$$ R=\frac{3600\times\sin60^{\circ}}{10}=360\times0.8660=311.8\ \text{m} $$
:::

::: tip Examiner's note — Mechanics
Most repeated: **a like-parallel-forces proof or numerical** (2080, CDC), **a projectile numerical** (2079, 2081 and 2082 MCQs), **resolving forces in equilibrium** (2081, 2082). Draw the force diagram before writing equations — the diagram mark is given separately. Take $g$ as instructed ($10$ in these papers) and quote units.
:::

## 12.17 Appendix: Retained Examinable Topics

CDC allots no separate hours: the 2078 curriculum retains these topics from the older course, and the verified papers still examine **group theory (2079 Q2, 2080 Q1)** and **Rolle's theorem and the Mean Value Theorem (2080 Q16 and Q22a)**; the trapezoidal and Simpson rules are in the CDC syllabus list as revision. Group theory and Rolle/MVT were **absent from 2081 and 2082**; treat them as a reserve, not a certainty.

| Result | Statement |
|---|---|
| Group $(G,*)$ | closure; associativity; identity $e$; inverse of every element |
| Abelian group | a group in which $a*b=b*a$ for all $a,b$ |
| Rolle | $f$ continuous on $[a,b]$, differentiable on $(a,b)$, $f(a)=f(b)$ $\Rightarrow$ $f'(c)=0$ for some $c$ |
| Mean Value | same conditions without $f(a)=f(b)$ $\Rightarrow$ $f'(c)=\dfrac{f(b)-f(a)}{b-a}$ |
| Trapezoidal ($n$ strips) | $\dfrac h2\big[y_0+y_n+2(y_1+\cdots+y_{n-1})\big]$ |
| Simpson ($n$ even) | $\dfrac h3\big[y_0+y_n+4(\text{odd})+2(\text{even})\big]$ |

**Short answer questions [5 marks each]**

1. (a) Show that the set of integers $\mathbb{Z}$ under addition is an abelian group. [3] (b) Show that $\mathbb{Z}$ under multiplication is **not** a group. [2] <span class="marks">[5]</span> (NEB 2079 Q2; NEB 2080 Q1)
2. Show that $\{1,-1,i,-i\}$ is an abelian group under multiplication, by completing its composition table. <span class="marks">[5]</span>
3. If $f(x)=\dfrac12-x$ for $x<\dfrac12$ and $f(x)=\big(\dfrac12-x\big)^{2}$ for $x\geq\dfrac12$, does $f$ obey the Mean Value Theorem on $[0,1]$? Give reasons. <span class="marks">[5]</span> (NEB 2080, Q22a, here with 5 marks)
4. (a) Verify Rolle's theorem for $f(x)=x(x-1)(x-2)$ on $[0,2]$. [3] (b) Verify the Mean Value Theorem for $f(x)=x^{2}$ on $[1,4]$. [2] <span class="marks">[5]</span>
5. Use the trapezoidal rule and Simpson's rule with $4$ strips to estimate $\displaystyle\int_{0}^{1}\frac{dx}{1+x^{2}}$ and compare with the exact value $\dfrac{\pi}{4}$. <span class="marks">[5]</span>

::: note Model answers — short
**1.** (a) For $a,b,c\in\mathbb{Z}$ under $+$:
*Closure:* $a+b\in\mathbb{Z}$.
*Associativity:* $(a+b)+c=a+(b+c)$.
*Identity:* $0\in\mathbb{Z}$ and $a+0=0+a=a$.
*Inverse:* for each $a$, $-a\in\mathbb{Z}$ and $a+(-a)=0$.
*Commutativity:* $a+b=b+a$.
All five hold, so $(\mathbb{Z},+)$ is an abelian group. ∎
(b) Under multiplication closure, associativity and the identity $1$ hold, but inverses fail: the inverse of $2$ would be $\tfrac12\notin\mathbb{Z}$. (Only $1$ and $-1$ have inverses, and $0$ has none.) So $(\mathbb{Z},\times)$ is not a group.

**2.** Composition table (row $\times$ column):

| $\times$ | $1$ | $-1$ | $i$ | $-i$ |
|---|---|---|---|---|
| $1$ | $1$ | $-1$ | $i$ | $-i$ |
| $-1$ | $-1$ | $1$ | $-i$ | $i$ |
| $i$ | $i$ | $-i$ | $-1$ | $1$ |
| $-i$ | $-i$ | $i$ | $1$ | $-1$ |

*Closure:* every entry is in the set. *Associativity:* inherited from multiplication of complex numbers. *Identity:* $1$ (its row and column repeat the headings). *Inverses:* $1^{-1}=1$, $(-1)^{-1}=-1$, $i^{-1}=-i$, $(-i)^{-1}=i$ (each row contains $1$). *Commutativity:* the table is symmetric about the leading diagonal. So it is an abelian group of order $4$. ∎

**3.** *Continuity at $x=\frac12$:* from the left, $\dfrac12-\dfrac12=0$; from the right, $\big(\dfrac12-\dfrac12\big)^{2}=0$; and $f\big(\tfrac12\big)=0$. So $f$ is continuous on $[0,1]$.
*Differentiability at $x=\frac12$:* left derivative $=\dfrac{d}{dx}\big(\tfrac12-x\big)=-1$; right derivative $=\dfrac{d}{dx}\big(\tfrac12-x\big)^{2}=-2\big(\tfrac12-x\big)=0$ at $x=\tfrac12$. They differ, so $f$ is **not differentiable at $x=\tfrac12$**, a point inside $(0,1)$. The hypothesis of the theorem fails.
*Does the conclusion hold anyway?* $\dfrac{f(1)-f(0)}{1-0}=\dfrac{\frac14-\frac12}{1}=-\dfrac14$. For $x<\tfrac12$, $f'=-1\neq-\tfrac14$. For $x>\tfrac12$, $f'=2x-1=-\tfrac14$ gives $x=\tfrac38$, which is **not** greater than $\tfrac12$. So no point $c$ exists: $f$ does not obey the Mean Value Theorem on $[0,1]$.

**4.** (a) $f$ is a polynomial, so continuous and differentiable everywhere. $f(0)=0$ and $f(2)=0$, so $f(0)=f(2)$. Rolle's conditions hold. $f(x)=x^{3}-3x^{2}+2x$, so $f'(x)=3x^{2}-6x+2=0$:
$$ x=\frac{6\pm\sqrt{36-24}}{6}=1\pm\frac{1}{\sqrt{3}} $$
Both $1-\frac{1}{\sqrt{3}}\approx0.423$ and $1+\frac{1}{\sqrt{3}}\approx1.577$ lie in $(0,2)$. Rolle's theorem is verified.
(b) $f(x)=x^{2}$ is continuous and differentiable. $\dfrac{f(4)-f(1)}{4-1}=\dfrac{16-1}{3}=5$ and $f'(c)=2c=5$ gives $c=2.5\in(1,4)$. Verified.

**5.** $h=\dfrac{1-0}{4}=0.25$ and $y=\dfrac{1}{1+x^{2}}$:

| $x$ | $0$ | $0.25$ | $0.5$ | $0.75$ | $1$ |
|---|---|---|---|---|---|
| $y$ | $1$ | $0.941176$ | $0.8$ | $0.64$ | $0.5$ |

Trapezoidal rule:
$$ T=\frac{0.25}{2}\big[1+0.5+2(0.941176+0.8+0.64)\big]=0.125\times6.262353=0.78279 $$
Simpson's rule:
$$ S=\frac{0.25}{3}\big[1+0.5+4(0.941176+0.64)+2(0.8)\big]=0.083333\times9.424706=0.78539 $$
The exact value is $\dfrac{\pi}{4}=0.785398$. Simpson's error is about $6\times10^{-6}$, the trapezoidal error about $2.6\times10^{-3}$: Simpson's rule is far more accurate for the same strips.
:::

**Long answer questions [8 marks each]**

1. (a) State and prove Rolle's theorem. [3] (b) Verify Rolle's theorem for $f(x)=x^{2}-4x+3$ on $[1,3]$. [2] (c) Using the Mean Value Theorem, show that if $f'(x)=0$ for every $x$ in $(a,b)$ then $f$ is constant on $[a,b]$. [3] <span class="marks">[8]</span>

::: note Model answer — long
**1.** (a) **Rolle's theorem:** if $f$ is continuous on $[a,b]$, differentiable on $(a,b)$ and $f(a)=f(b)$, there is at least one $c\in(a,b)$ with $f'(c)=0$.
**Proof.** Because $f$ is continuous on a closed interval it attains a greatest value $M$ and a least value $m$. If $M=m$, $f$ is constant and $f'(c)=0$ for every $c$. Otherwise at least one of $M,m$ differs from $f(a)=f(b)$, so is attained at an interior point $c\in(a,b)$; say $f(c)=M$. Then $f(c+h)-f(c)\leq0$ for small $h$, so the quotient $\dfrac{f(c+h)-f(c)}{h}$ is $\leq0$ for $h>0$ and $\geq0$ for $h<0$. Since $f'(c)$ exists, its limit from both sides must be equal, which forces $f'(c)=0$. The case $f(c)=m$ is identical. ∎
(b) $f$ is a polynomial, so continuous and differentiable. $f(1)=1-4+3=0$ and $f(3)=9-12+3=0$. Then $f'(x)=2x-4=0$ gives $c=2\in(1,3)$. Verified.
(c) Take any $x_1<x_2$ in $[a,b]$. $f$ is continuous and differentiable on $[x_1,x_2]$, so by the Mean Value Theorem there is $c\in(x_1,x_2)$ with
$$ f(x_2)-f(x_1)=f'(c)(x_2-x_1)=0 $$
since $f'(c)=0$. So $f(x_2)=f(x_1)$ for all $x_1,x_2$: $f$ is constant. ∎
:::

::: tip Examiner's note — Appendix topics
Most repeated: **"is $(S,*)$ an abelian group?"** with the five properties checked one by one (2079, 2080), and **"does $f$ obey the Mean Value Theorem?"** — always test continuity and differentiability at the joining point of a piecewise function (2080). These topics are sometimes missed in revision because they are labelled "retained"; they are still examinable.
:::

## Chapter summary

The table gathers what the verified papers (2079, 2080, 2081, 2082 and the CDC model 2080) ask, unit by unit, so that you can allocate revision time.

| Unit | Most repeated subjective item | Years seen |
|---|---|---|
| 12.1 Permutation and Combination | committee / word-arrangement counting | 2080, 2082, CDC |
| 12.2 Binomial Theorem | middle term; coefficient of $x^{r}$; recall | 2079, 2080, 2081, 2082 |
| 12.3 Complex Numbers | De Moivre, roots | 2080, 2081, CDC |
| 12.4 Sequence and Series | proof by induction | all five |
| 12.5 Linear Systems | three-equation system (Cramer / matrix) | all five |
| 12.6 Properties of a Triangle | half-angle or law proofs | 2079, 2081, 2082 |
| 12.7 Solution of Triangles | solve a triangle | 2081 |
| 12.8 Conics | eccentricity, foci; tangent/normal condition | 2080, 2081, 2082, CDC |
| 12.9 Product of Vectors | dot, projection, cross-product area | 2079, 2080, 2081, 2082 |
| 12.10 Correlation and Regression | table numerical | all five |
| 12.11 Probability | $P(B/A)$ | 2080, 2081, 2082, CDC (MCQ) |
| 12.12 Derivatives | inverse-hyperbolic; L'Hospital; rate | 2080, 2081, 2082, CDC |
| 12.13 Anti-derivatives | partial fractions; $\int dx/(a+b\cos x)$ | 2079, 2081, 2082 |
| 12.14 Differential Equations | linear (I.F.), separable, modelling | all five |
| 12.15 Computational Methods | simplex LPP | all five |
| 12.16 Mechanics | like parallel forces; projectile | all five (as the alternative) |
| 12.17 Appendix | group axioms; MVT | 2079, 2080 |

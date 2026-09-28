---
subject: Question Bank
grade: 12
unit: 11
title: Mathematics: Unit-wise Objective Question Bank
hours: 0
area: Mathematics
---

Group A is 11 marks out of 75 — one seventh of the whole Mathematics paper — and
it is decided in about fifteen minutes. It is also the cheapest block of marks on
the paper, because every item is a single formula, a single condition or a single
one-line calculation, and the same handful of formulae come back year after year.
Note one change that is verified on the 2082 paper itself: the eleven MCQs now
arrive as a **separate booklet, issued 30 minutes after the examination starts**,
and you write their answers on the same answer sheet. So you will begin with
Group B, and Group A will interrupt you. Plan for that.

::: key The real pattern, and the real grid
**Paper structure** (identical on the verified 2079, 2080, 2081 and 2082 papers
and on the CDC Model Question-2080):

| Group | Questions | Marks | Printed as |
|---|---|---|---|
| A — multiple choice | 11 (Q1–Q11) | 1 each | `11x1=11` |
| B — short answer | 8 (Q12–Q19) | 5 each | `8x5=40` |
| C — long answer | 3 (Q20–Q22) | 8 each | `3x8=24` |
| **Total** | **22** | **75** | Time 3 hrs |

There are **exactly two "Or" choices in the whole paper, always at Q11 and at
Q19**. Group C never carries an "Or". Everything else is compulsory.

**CDC Specification Grid 2078 — area-wise marks and MCQ counts:**

| Content area | Area-wise marks | MCQs |
|---|---|---|
| Algebra | 20 | 2 |
| Trigonometry | 6 | 3 shared |
| Analytic Geometry | 9 | (across these |
| Vector | 6 | three areas) |
| Statistics & Probability | 6 | 1 |
| Calculus | 22 | 4 |
| Computational Methods **or** Mechanics | 6 | 1 |
| **Total** | **75** | **11** |

**Correct a common error now.** The bracketed numbers printed beside each area in
the syllabus — Algebra 44, Trigonometry 12, Analytic Geometry 20, Vectors 12,
Statistics & Probability 12, Calculus 48, Computational Methods/Mechanics 12,
adding to **160** — are **working hours, not marks**. Many students and many
coaching sheets quote them as marks. They cannot be marks: the paper is 75. The
marks column is the one in the table above.

**The grid's own footnote, verbatim:** "At least one multiple choice question
should be asked from each area (Trigonometry, Analytic geometry and Vector)."
That single sentence is why a Trigonometry MCQ is effectively guaranteed every
year, even though Trigonometry is only 6 of the 75 marks.

A second printed note is worth knowing: "Questions should be prepared by giving
the context and one question may have more than one sub-questions." That is why
Group B items arrive as a table, a figure or a stated theorem followed by five
one-mark probes.
:::

This chapter is 216 multiple-choice questions, one section per syllabus unit, in
syllabus order. Every question carrying a year tag — `(NEB 2079)`, `(NEB 2080)`,
`(NEB 2081)`, `(NEB 2082)`, `(CDC model 2080)` — is a real item from that paper,
transcribed from the scan. Untagged questions were written for this book in the
same style. Every numerical answer in every key was recomputed with a computer
algebra system before printing.

## 11.1 Permutation and Combination

Of the two Algebra MCQs, one has come from this unit in 2081 and again in 2082.
Both times it was pure recall: a counting principle or the relation between $P$
and $C$. Nothing here needs more than one line of arithmetic.

| Result | Formula / condition |
|---|---|
| Basic counting principle | $m$ ways then $n$ ways gives $m \times n$ ways |
| Arrangements, all different | $P(n,r) = \frac{n!}{(n-r)!}$ |
| Selections, all different | $C(n,r) = \frac{n!}{r!(n-r)!}$ |
| Link between them | $C(n,r) \times r! = P(n,r)$ |
| Arrangements, not all different | $\frac{n!}{p!\,q!\,r!}$ for repeats $p,q,r$ |
| Repetition allowed, $r$ places | $n^{r}$ |
| Circular arrangement of $n$ | $(n-1)!$ |
| Garland / necklace of $n$ | $\frac{(n-1)!}{2}$ (clockwise = anticlockwise) |
| Symmetry of combination | $C(n,r) = C(n, n-r)$ |
| Pascal's rule | $C(n,r) + C(n,r-1) = C(n+1,r)$ |
| Total subsets | $\sum_{r=0}^{n} C(n,r) = 2^{n}$ |
| At least one chosen | $2^{n} - 1$ |
| Diagonals of an $n$-gon | $C(n,2) - n$ |
| Boundary values | $C(n,0) = C(n,n) = 1$, $P(n,0)=1$ |

**Multiple choice questions**

1. Which one is the relation between permutation and combination of $n$ things taken $r$ things at a time? (NEB 2082) <span class="marks">[1]</span>
   (a) $C(n,r) = r!\times P(n,r)$ (b) $C(n,r)\times r! = P(n,r)$ (c) $C(n,r)\times r = P(n,r)$ (d) $C(n,r) = P(n,r)\times r$
2. How many numbers are there in between $999$ and $10{,}000$? (NEB 2081) <span class="marks">[1]</span>
   (a) $9\times 10^{3}$ (b) $8\times 10^{3}$ (c) $9^{4}$ (d) $8^{4}$
3. The value of $P(5,3)$ is <span class="marks">[1]</span>
   (a) $10$ (b) $20$ (c) $60$ (d) $120$
4. The value of $C(10,8)$ is <span class="marks">[1]</span>
   (a) $45$ (b) $80$ (c) $90$ (d) $360$
5. If $C(n,2) = 15$ then $n$ equals <span class="marks">[1]</span>
   (a) $5$ (b) $6$ (c) $7$ (d) $15$
6. Five people are to be seated around a round table. The number of arrangements is <span class="marks">[1]</span>
   (a) $5$ (b) $20$ (c) $24$ (d) $120$
7. The number of distinct arrangements of the letters of the word COMMITTEE is <span class="marks">[1]</span>
   (a) $362880$ (b) $181440$ (c) $90720$ (d) $45360$
8. The number of diagonals of a regular decagon is <span class="marks">[1]</span>
   (a) $10$ (b) $35$ (c) $45$ (d) $90$
9. If $C(n,8) = C(n,12)$ then $n$ equals <span class="marks">[1]</span>
   (a) $4$ (b) $12$ (c) $20$ (d) $96$
10. How many three-digit numbers, with no digit repeated, can be formed from the digits $2,3,4,5,6,7$? <span class="marks">[1]</span>
    (a) $18$ (b) $20$ (c) $120$ (d) $216$
11. A cricket team of $11$ players is to be chosen from $15$. The number of ways is <span class="marks">[1]</span>
    (a) $165$ (b) $455$ (c) $1365$ (d) $32760$
12. The number of different garlands that can be made from $8$ distinct flowers is <span class="marks">[1]</span>
    (a) $5040$ (b) $2520$ (c) $40320$ (d) $20160$

::: note Answer key — 11.1
**1.** (b) — $C(n,r)$ counts selections; multiplying by $r!$ orders each selection, which is exactly $P(n,r)$.
**2.** (a) — the numbers strictly between are $1000$ to $9999$, i.e. all four-digit numbers: $9999-1000+1 = 9000 = 9\times10^{3}$.
**3.** (c) — $P(5,3) = 5\times4\times3 = 60$.
**4.** (a) — $C(10,8) = C(10,2) = \frac{10\times9}{2} = 45$.
**5.** (b) — $\frac{n(n-1)}{2}=15 \Rightarrow n^{2}-n-30=0 \Rightarrow n=6$ (the root $-5$ is rejected).
**6.** (c) — circular arrangement of $n$ objects is $(n-1)! = 4! = 24$.
**7.** (d) — $9$ letters with M, T, E each twice: $\frac{9!}{2!\,2!\,2!} = \frac{362880}{8} = 45360$.
**8.** (b) — $C(10,2) - 10 = 45-10 = 35$; the $10$ subtracted are the sides.
**9.** (c) — $C(n,r)=C(n,s)$ with $r \ne s$ forces $r+s=n$, so $n = 8+12 = 20$.
**10.** (c) — $6\times5\times4 = 120$, i.e. $P(6,3)$.
**11.** (c) — $C(15,11) = C(15,4) = \frac{15\times14\times13\times12}{24} = 1365$.
**12.** (b) — a garland can be flipped, so $\frac{(8-1)!}{2} = \frac{5040}{2} = 2520$.
:::

::: caution Distractor analysis — Permutation and Combination
**Reading $C(n,r)\times r! = P(n,r)$ backwards.** This is the exact trap in the
2082 MCQ 1. Option (a), $C(n,r) = r!\times P(n,r)$, is the same equation with the
$r!$ on the wrong side. Fix it by size: for $n=5$, $r=3$ we have $C=10$ and
$P=60$, so $P$ is the **bigger** number, so $r!$ multiplies $C$, never $P$.

**Order-blindness.** In Q11 the distractor $32760$ is $P(15,4)$: the student
selected *and* ordered eleven players. A team is a selection. If swapping two
chosen objects gives the same answer, use $C$.

**Forgetting the circle costs one factor.** In Q6 the distractor $120 = 5!$ is
the answer for a straight bench. Around a table, one person's seat is only
relative, so divide by $n$: $(n-1)!$.

**Forgetting that a garland flips.** In Q12 the distractor $5040 = 7!$ is the
circular count. A garland (or necklace) read clockwise equals the same garland
read anticlockwise, so halve it.

**Counting the sides as diagonals.** In Q8 the distractor $45$ is $C(10,2)$, the
number of *all* lines joining two vertices. Ten of those are sides.
:::

## 11.2 Binomial Theorem

Worth reading carefully, because of a fact the four verified papers make plain:
**Binomial Theorem has never appeared as an MCQ in 2079, 2080, 2081 or 2082.** It
appears every year, but in Group B (2079 Q12, 2080 Q13b, 2081 Q12, 2082 Q12a) and
Group C (2081 Q20a, 2082 Q20a). Learn the facts below for Group B; do not spend
Group A revision time here beyond one pass.

| Result | Formula / condition |
|---|---|
| Expansion, positive integral index | $(a+b)^{n} = \sum_{r=0}^{n} C(n,r)\,a^{n-r}b^{r}$ |
| General term | $T_{r+1} = C(n,r)\,a^{n-r}b^{r}$ |
| Number of terms | $n+1$ |
| Middle term, $n$ even | one term, the $\left(\frac{n}{2}+1\right)$th |
| Middle terms, $n$ odd | two, the $\frac{n+1}{2}$th and $\frac{n+3}{2}$th |
| Sum of all coefficients | $(1+x)^{n}$ at $x=1$ gives $2^{n}$ |
| Any index | $(1+x)^{n}$ valid only for $|x|<1$, infinitely many terms |
| Euler's number | $e = 1+\frac{1}{1!}+\frac{1}{2!}+\frac{1}{3!}+\cdots$, $2<e<3$ |
| Exponential series | $e^{x} = 1+\frac{x}{1!}+\frac{x^{2}}{2!}+\frac{x^{3}}{3!}+\cdots$ |
| General exponential | $a^{x} = 1 + x\log a + \frac{(x\log a)^{2}}{2!}+\cdots$ |
| Logarithmic series | $\log_e(1+x) = x-\frac{x^{2}}{2}+\frac{x^{3}}{3}-\cdots$ |
| Its validity | $-1 < x \leq 1$ |
| Other logarithmic series | $\log_e(1-x) = -x-\frac{x^{2}}{2}-\frac{x^{3}}{3}-\cdots$, $|x|<1$ |
| Approximation | for small $x$, $(1+x)^{n} \approx 1+nx$ |

**Multiple choice questions**

1. The number of terms in the expansion of $(2x+3y)^{12}$ is <span class="marks">[1]</span>
   (a) $11$ (b) $12$ (c) $13$ (d) $24$
2. In the expansion of $(a+b)^{10}$, the middle term is the <span class="marks">[1]</span>
   (a) $5$th (b) $6$th (c) $7$th (d) $5$th and $6$th
3. The middle term of $(2+3x)^{30}$ is the <span class="marks">[1]</span>
   (a) $15$th (b) $16$th (c) $17$th (d) $15$th and $16$th
4. The coefficient of $x^{5}$ in $(1+x)^{10}$ is <span class="marks">[1]</span>
   (a) $120$ (b) $210$ (c) $252$ (d) $504$
5. The sum of the binomial coefficients in the expansion of $(1+x)^{n}$ is <span class="marks">[1]</span>
   (a) $n$ (b) $n!$ (c) $2^{n}$ (d) $2^{n}-1$
6. In $(1+x)^{11}$ the coefficients of $x^{r}$ and $x^{r+1}$ are equal. Then $r$ is <span class="marks">[1]</span>
   (a) $4$ (b) $5$ (c) $6$ (d) $11$
7. The expansion of $\log_e(1+x)$ is valid for <span class="marks">[1]</span>
   (a) all $x$ (b) $x>0$ (c) $-1 < x \leq 1$ (d) $x \geq 1$
8. Euler's number $e$ is the sum of the series <span class="marks">[1]</span>
   (a) $\sum \frac{1}{n}$ (b) $\sum \frac{1}{n!}$ (c) $\sum \frac{1}{n^{2}}$ (d) $\sum \frac{(-1)^{n}}{n!}$
9. The coefficient of $x^{3}$ in the expansion of $e^{2x}$ is <span class="marks">[1]</span>
   (a) $\frac{1}{6}$ (b) $\frac{2}{3}$ (c) $\frac{4}{3}$ (d) $8$
10. Using the binomial expansion, $(1.01)^{5}$ correct to three decimal places is <span class="marks">[1]</span>
    (a) $1.005$ (b) $1.050$ (c) $1.051$ (d) $1.105$
11. The term independent of $x$ in the expansion of $\left(x+\frac{1}{x}\right)^{6}$ is <span class="marks">[1]</span>
    (a) $15$ (b) $20$ (c) $30$ (d) $64$
12. The number of terms in the expansion of $(1+x)^{-3}$, $|x|<1$, is <span class="marks">[1]</span>
    (a) $2$ (b) $3$ (c) $4$ (d) infinitely many

::: note Answer key — 11.2
**1.** (c) — a positive integral index $n$ gives $n+1$ terms, so $12+1=13$.
**2.** (b) — $n=10$ is even, so there is one middle term, the $\left(\frac{10}{2}+1\right)$th $=6$th.
**3.** (b) — $n=30$ is even: the $\left(\frac{30}{2}+1\right)$th $=16$th term.
**4.** (c) — $C(10,5) = 252$.
**5.** (c) — put $x=1$: $\sum C(n,r) = (1+1)^{n} = 2^{n}$.
**6.** (b) — $C(11,r) = C(11,r+1)$ needs $r+(r+1) = 11$, so $r=5$.
**7.** (c) — the series diverges at $x=-1$ and for $|x|>1$; it converges at $x=+1$ (giving $\log 2$).
**8.** (b) — $e = \sum_{n=0}^{\infty}\frac{1}{n!} = 1+1+\frac{1}{2}+\frac{1}{6}+\cdots$
**9.** (c) — $e^{2x} = \sum \frac{(2x)^{n}}{n!}$, so the $x^{3}$ coefficient is $\frac{2^{3}}{3!} = \frac{8}{6} = \frac{4}{3}$.
**10.** (c) — $(1+0.01)^{5} = 1+5(0.01)+10(0.0001)+\cdots = 1.05101\ldots \approx 1.051$.
**11.** (b) — $T_{r+1} = C(6,r)x^{6-2r}$; $6-2r=0$ gives $r=3$ and $C(6,3)=20$.
**12.** (d) — for a negative (or fractional) index the expansion is an infinite series; it only terminates for a positive integral index.
:::

::: caution Distractor analysis — Binomial Theorem
**Counting terms as $n$ instead of $n+1$.** Option (b) in Q1 is the commonest
wrong answer. The powers of $y$ run $0,1,2,\ldots,12$ — thirteen values.

**Confusing "$r$th term" with "coefficient of $x^{r}$".** $T_{r+1}$ carries
$x^{r}$. In Q4 the answer is $C(10,5)$, not $C(10,4)$; the distractor $210 =
C(10,4)$ is exactly the off-by-one.

**Applying the "two middle terms" rule to an even index.** In Q2 and Q3 the
distractor "(d) two middle terms" is the $n$ odd case. Even $n$ gives one middle
term. Count the terms first: $11$ terms has a 6th in the middle, $31$ terms has a
16th.

**Ignoring the validity condition.** In Q7 and Q12, option (a) "all $x$" treats a
power series as if it were a polynomial. The general binomial theorem and the
logarithmic series are only valid on a restricted interval, and the examiner asks
for that interval (2081 Q12c did, for 1 mark).
:::

## 11.3 Complex Numbers

This unit has supplied an Algebra MCQ twice in four years: 2079 asked for a
property of the cube roots of unity, 2081 for the polar form of a product. Both
are one-line recall. De Moivre's theorem itself has appeared every year, but in
Group B or C.

| Result | Formula / condition |
|---|---|
| Polar (modulus–amplitude) form | $z = r(\cos\theta + i\sin\theta)$ |
| Modulus | $r = |z| = \sqrt{x^{2}+y^{2}}$ |
| Argument | $\theta = \tan^{-1}\frac{y}{x}$, placed in the correct quadrant |
| Product in polar form | $z_1z_2 = r_1r_2\left[\cos(\theta_1+\theta_2)+i\sin(\theta_1+\theta_2)\right]$ |
| Quotient in polar form | moduli divide, arguments subtract |
| De Moivre's theorem | $\left[r(\cos\theta+i\sin\theta)\right]^{n} = r^{n}(\cos n\theta + i \sin n\theta)$ |
| Euler's formula | $e^{i\theta} = \cos\theta + i\sin\theta$, so $e^{i\pi} = -1$ |
| Cube roots of unity | $1,\ \omega,\ \omega^{2}$ with $\omega = \frac{-1+i\sqrt{3}}{2}$ |
| Their sum | $1+\omega+\omega^{2} = 0$ |
| Their product | $1\cdot\omega\cdot\omega^{2} = \omega^{3} = 1$ |
| Useful consequence | $\omega+\omega^{2} = -1$ and $(1+\omega)(1+\omega^{2}) = 1$ |
| $n$th roots of unity | $n$ distinct values, and they sum to $0$ |
| Powers of $i$ | $i^{4k}=1$, $i^{4k+1}=i$, $i^{4k+2}=-1$, $i^{4k+3}=-i$ |
| Conjugate | $z\bar{z} = |z|^{2}$ |

**Multiple choice questions**

1. The property of cube roots of unity where $\omega$ is the cube root of unity is (NEB 2079) <span class="marks">[1]</span>
   (a) $1+\omega+\omega^{2}=0$ (b) $\omega^{3}+1=0$ (c) $\omega = -\omega^{2}$ (d) $\omega+\omega^{2}=1$
2. It is given that $(r_1,\theta_1)$ and $(r_2,\theta_2)$ are polar co-ordinates of $z_1$ and $z_2$. What are the polar co-ordinates of the image of $z_1z_2$? (NEB 2081) <span class="marks">[1]</span>
   (a) $(r_1r_2,\ \theta_1-\theta_2)$ (b) $(r_1r_2,\ \theta_1+\theta_2)$ (c) $(r_1+r_2,\ \theta_1+\theta_2)$ (d) $(r_1-r_2,\ \theta_1+\theta_2)$
3. The modulus of $1+i\sqrt{3}$ is <span class="marks">[1]</span>
   (a) $1$ (b) $\sqrt{2}$ (c) $2$ (d) $4$
4. The argument of $-1+i$ is <span class="marks">[1]</span>
   (a) $\frac{\pi}{4}$ (b) $\frac{3\pi}{4}$ (c) $-\frac{\pi}{4}$ (d) $\frac{5\pi}{4}$
5. If $\omega$ is a complex cube root of unity, then $\omega^{10}+\omega^{11}$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $-1$ (d) $\omega$
6. If $\omega$ is a complex cube root of unity, then $(1+\omega)(1+\omega^{2})$ equals <span class="marks">[1]</span>
   (a) $-1$ (b) $0$ (c) $1$ (d) $2$
7. By De Moivre's theorem, $(\cos 20^{\circ}+i\sin 20^{\circ})^{9}$ equals <span class="marks">[1]</span>
   (a) $1$ (b) $-1$ (c) $i$ (d) $-i$
8. The value of $e^{i\pi/2}$ is <span class="marks">[1]</span>
   (a) $1$ (b) $-1$ (c) $i$ (d) $-i$
9. The number of distinct fifth roots of unity is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $5$ (d) infinitely many
10. The polar form of $1+i$ is <span class="marks">[1]</span>
    (a) $\sqrt{2}\left(\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}\right)$ (b) $2\left(\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}\right)$ (c) $\sqrt{2}\left(\cos\frac{\pi}{3}+i\sin\frac{\pi}{3}\right)$ (d) $\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}$
11. The value of $i^{37}$ is <span class="marks">[1]</span>
    (a) $1$ (b) $-1$ (c) $i$ (d) $-i$
12. The sum of all the fifth roots of unity is <span class="marks">[1]</span>
    (a) $0$ (b) $1$ (c) $5$ (d) $-1$

::: note Answer key — 11.3
**1.** (a) — $\omega$ satisfies $\omega^{3}=1$, i.e. $(\omega-1)(\omega^{2}+\omega+1)=0$; since $\omega \ne 1$, $1+\omega+\omega^{2}=0$.
**2.** (b) — multiplying complex numbers multiplies the moduli and adds the arguments.
**3.** (c) — $\sqrt{1^{2}+(\sqrt{3})^{2}} = \sqrt{4} = 2$.
**4.** (b) — the point $(-1,1)$ is in the second quadrant, so $\theta = \pi - \frac{\pi}{4} = \frac{3\pi}{4}$.
**5.** (c) — $\omega^{10}=\omega^{9}\cdot\omega=\omega$ and $\omega^{11}=\omega^{2}$, so the sum is $\omega+\omega^{2}=-1$.
**6.** (c) — expand: $1+\omega+\omega^{2}+\omega^{3} = 0 + 1 = 1$.
**7.** (b) — $\cos 180^{\circ}+i\sin 180^{\circ} = -1$; machine-checked.
**8.** (c) — $\cos\frac{\pi}{2}+i\sin\frac{\pi}{2} = 0+i = i$.
**9.** (c) — the equation $z^{5}=1$ has exactly $5$ distinct roots.
**10.** (a) — $r=\sqrt{2}$ and $\theta = \tan^{-1}1 = \frac{\pi}{4}$ (first quadrant).
**11.** (c) — $37 = 4(9)+1$, so $i^{37}=i^{1}=i$.
**12.** (a) — the roots of $z^{5}-1=0$ sum to minus the coefficient of $z^{4}$, which is $0$.
:::

::: caution Distractor analysis — Complex Numbers
**Writing $\omega^{3}+1=0$ instead of $\omega^{3}-1=0$.** Option (b) in the 2079
MCQ 1 is the cube root of $-1$, not of $1$. Anchor it on the real root: $\omega=1$
must satisfy the equation, and $1^{3}-1=0$.

**Losing the quadrant when finding an argument.** In Q4, $\tan^{-1}\frac{1}{-1} =
-\frac{\pi}{4}$ comes straight off a calculator, and it is option (c) — the wrong
answer, because $(-1,1)$ is in the second quadrant. Always plot the point first.

**Adding the moduli.** Option (c) in the 2081 MCQ, $(r_1+r_2,\theta_1+\theta_2)$,
treats multiplication as addition in the modulus. Moduli multiply; only arguments
add.

**Forgetting to reduce the power modulo $3$ (or $4$).** In Q5 and Q11 a student
who tries to compute $\omega^{10}$ directly loses time and accuracy. Use
$\omega^{3}=1$ and $i^{4}=1$ to knock the exponent down first.
:::

## 11.4 Sequence and Series

This unit is examined as a single-line recall MCQ or, far more often, as
mathematical induction in Group B/C — induction appears in **every** verified year
(2079 Q13a, 2080 Q20b, 2081 Q20c, 2082 Q20b, CDC model Q20c). Memorise the three
sum formulae exactly; every mark here hangs on them.

| Result | Formula |
|---|---|
| Sum of first $n$ natural numbers | $\sum n = \frac{n(n+1)}{2}$ |
| Sum of their squares | $\sum n^{2} = \frac{n(n+1)(2n+1)}{6}$ |
| Sum of their cubes | $\sum n^{3} = \left[\frac{n(n+1)}{2}\right]^{2}$ |
| A useful identity | $\sum n^{3} = \left(\sum n\right)^{2}$ |
| Sum of first $n$ odd numbers | $1+3+5+\cdots+(2n-1) = n^{2}$ |
| Sum of first $n$ even numbers | $2+4+6+\cdots+2n = n(n+1)$ |
| Induction, step 1 | verify the statement for $n=1$ (the base case) |
| Induction, step 2 | assume it true for $n=k$ (the inductive hypothesis) |
| Induction, step 3 | prove it for $n=k+1$ using that assumption |
| Induction, conclusion | true for all $n \in \mathbb{N}$ |

**Multiple choice questions**

1. The sum of the first $5$ odd natural numbers is (CDC model 2080) <span class="marks">[1]</span>
   (a) $15$ (b) $20$ (c) $25$ (d) $30$
2. The value of $1^{2}+2^{2}+3^{2}+\cdots+20^{2}$ is <span class="marks">[1]</span>
   (a) $2470$ (b) $2870$ (c) $3080$ (d) $4410$
3. The value of $1^{3}+2^{3}+3^{3}+\cdots+10^{3}$ is <span class="marks">[1]</span>
   (a) $385$ (b) $1000$ (c) $3025$ (d) $3850$
4. The value of $1+2+3+\cdots+100$ is <span class="marks">[1]</span>
   (a) $4950$ (b) $5000$ (c) $5050$ (d) $10100$
5. The sum of the first $n$ even natural numbers is <span class="marks">[1]</span>
   (a) $n^{2}$ (b) $n(n+1)$ (c) $\frac{n(n+1)}{2}$ (d) $2n$
6. $1^{2}+2^{2}+\cdots+n^{2}$ equals <span class="marks">[1]</span>
   (a) $\frac{n(n+1)}{2}$ (b) $\frac{n(n+1)(2n+1)}{6}$ (c) $\left[\frac{n(n+1)}{2}\right]^{2}$ (d) $\frac{n(n+1)(n+2)}{6}$
7. Which statement is true for every positive integer $n$? <span class="marks">[1]</span>
   (a) $\sum n^{2} = \left(\sum n\right)^{2}$ (b) $\sum n^{3} = \left(\sum n\right)^{2}$ (c) $\sum n^{3} = \left(\sum n^{2}\right)^{2}$ (d) $\sum n = \left(\sum n^{2}\right)^{2}$
8. In a proof by mathematical induction, the first thing you must do is <span class="marks">[1]</span>
   (a) assume the result for $n=k$ (b) verify the result for the smallest $n$ (c) prove the result for $n=k+1$ (d) differentiate both sides
9. The value of $1^{2}+2^{2}+\cdots+6^{2}$ is <span class="marks">[1]</span>
   (a) $36$ (b) $49$ (c) $91$ (d) $441$
10. The sum of the cubes of the first $5$ natural numbers is <span class="marks">[1]</span>
    (a) $125$ (b) $225$ (c) $325$ (d) $625$

::: note Answer key — 11.4
**1.** (c) — $1+3+5+7+9=25$, which is $5^{2}$: the sum of the first $n$ odd numbers is $n^{2}$.
**2.** (b) — $\frac{20\times21\times41}{6} = 2870$.
**3.** (c) — $\left[\frac{10\times11}{2}\right]^{2} = 55^{2} = 3025$.
**4.** (c) — $\frac{100\times101}{2} = 5050$.
**5.** (b) — $2(1+2+\cdots+n) = 2\cdot\frac{n(n+1)}{2} = n(n+1)$.
**6.** (b) — the standard result; (c) is the sum of cubes.
**7.** (b) — the sum of cubes is the square of the sum of the first powers, e.g. $1+8+27=36=6^{2}$.
**8.** (b) — the base case. Without it the inductive step proves nothing.
**9.** (c) — $\frac{6\times7\times13}{6} = 91$.
**10.** (b) — $\left[\frac{5\times6}{2}\right]^{2} = 15^{2} = 225$.
:::

::: caution Distractor analysis — Sequence and Series
**Swapping $\sum n^{2}$ and $\sum n^{3}$.** These two formulae are adjacent in
memory and are the most-swapped pair in the whole Algebra area. Check with $n=2$:
$\sum n^{2} = 5$ and $\sum n^{3} = 9$. Feed $n=2$ into a formula you are unsure of
and see which number comes out.

**$n^{2}$ versus $n(n+1)$ for the odd/even sums.** Q1 and Q5 pair these
deliberately. Odd numbers start at $1$ and sum to $n^{2}$; even numbers start at
$2$ and sum to $n(n+1)$, which is exactly twice $\sum n$.

**Skipping the base case in induction.** Option (a) in Q8 is what most scripts
actually do first, and it loses the mark the grid allocates to it. The 2081 paper
asked candidates to *state* the principle of mathematical induction for 2 marks —
both the base case and the inductive step must appear in words.

**Off-by-one in $\sum n$ for a range.** For "the sum of the integers from $1$ to
$100$", $4950$ (option (a) in Q4) is $\sum_{1}^{99}$. Substitute the top limit
itself, not one less.
:::

## 11.5 Matrix Based System of Linear Equations

The 2082 paper put Cramer's rule straight into Group A (MCQ 2), and Group C has
carried a full matrix-method system in 2079, 2080 and 2082. Learn the three
methods as three different tools for the same job, and learn the consistency
conditions — they are what the MCQ actually tests.

| Result | Formula / condition |
|---|---|
| Matrix form of a system | $AX = B$ |
| Cramer's rule | $x=\frac{D_x}{D}$, $y=\frac{D_y}{D}$, $z=\frac{D_z}{D}$ |
| $D_x$ | replace the $x$-column of $D$ by the constants |
| Unique solution | $D \ne 0$ |
| No solution (inconsistent) | $D=0$ but some $D_x, D_y, D_z \ne 0$ |
| Infinitely many solutions | $D = 0$ and $D_x=D_y=D_z=0$ |
| Inverse matrix method | $X = A^{-1}B$, valid only if $|A| \ne 0$ |
| The inverse itself | $A^{-1} = \frac{1}{|A|}\,\mathrm{adj}\,A$ |
| $2\times2$ inverse rule | swap the diagonal, negate the off-diagonal, divide by $|A|$ |
| Singular matrix | $|A| = 0$, so $A^{-1}$ does not exist |
| Determinant of the adjoint | $|\mathrm{adj}\,A| = |A|^{n-1}$ |
| Determinant of the inverse | $|A^{-1}| = \frac{1}{|A|}$ |
| Row-equivalent (Gauss) method | row-operate the augmented matrix to upper triangular form, then back-substitute |
| Augmented matrix | the coefficient matrix with the constant column attached |

For a two-variable system, Cramer's rule is three determinants and one division.
Draw them out before you substitute — that alone prevents most sign errors.

```figure caption="Cramer's rule for $p_1x+q_1y=r_1$, $p_2x+q_2y=r_2$. The $x$-column of $D$ is replaced by the constants to make $D_x$; the $y$-column is replaced to make $D_y$."
fig = mateq(["$D =$", ("det", [["$p_1$","$q_1$"],["$p_2$","$q_2$"]]),
             "$D_x =$", ("det", [["$r_1$","$q_1$"],["$r_2$","$q_2$"]]),
             "$D_y =$", ("det", [["$p_1$","$r_1$"],["$p_2$","$r_2$"]])],
            fontsize=11, colw=0.56, scale=0.62)
```

So $x = \dfrac{D_x}{D}$ and $y = \dfrac{D_y}{D}$ — written out,

$$ y = \frac{p_1r_2-p_2r_1}{p_1q_2-p_2q_1} $$

The row-equivalent method works on the augmented matrix instead. One row
operation at a time, and you write the operation beside the row you changed.

```figure caption="Augmented matrix of $2x+3y=8$, $x-y=-1$ and the result of the single row operation $R_2 \rightarrow 2R_2 - R_1$. The new second row reads $-5y=-10$, so $y=2$ and then $x=1$."
fig = mateq([[["$2$","$3$","$8$"],["$1$","$-1$","$-1$"]], "→",
             [["$2$","$3$","$8$"],["$0$","$-5$","$-10$"]]],
            fontsize=11, colw=0.56, scale=0.62)
```

**Multiple choice questions**

1. If the system of equations is $p_1x+q_1y=r_1$ and $p_2x+q_2y=r_2$, what is the value of $y$? (NEB 2082) <span class="marks">[1]</span>
   (a) $\frac{r_1q_2-r_2q_1}{p_1q_2-p_2q_1}$ (b) $\frac{p_1r_2-p_2r_1}{p_1q_2-p_2q_1}$ (c) $\frac{p_1q_2-p_2q_1}{p_1r_2-p_2r_1}$ (d) $\frac{p_2r_1-p_1r_2}{p_1q_2-p_2q_1}$
2. A system of linear equations has a unique solution if and only if <span class="marks">[1]</span>
   (a) $D=0$ (b) $D \ne 0$ (c) $D_x = 0$ (d) $D=D_x=D_y=0$
3. If $A$ has first row $(2,\ 3)$ and second row $(3,\ -1)$, then $|A|$ equals <span class="marks">[1]</span>
   (a) $-11$ (b) $-7$ (c) $7$ (d) $11$
4. A square matrix $A$ with $|A| = 0$ is called <span class="marks">[1]</span>
   (a) singular (b) non-singular (c) orthogonal (d) symmetric
5. The last column of the augmented matrix of the system $3x+2y-1=0$, $4x+y=3$ is <span class="marks">[1]</span>
   (a) $(1,\ 3)$ (b) $(-1,\ 3)$ (c) $(3,\ 4)$ (d) $(2,\ 1)$
6. In Cramer's rule, $x$ equals <span class="marks">[1]</span>
   (a) $\frac{D}{D_x}$ (b) $\frac{D_x}{D}$ (c) $D\cdot D_x$ (d) $\frac{D_y}{D}$
7. Solving $2x+3y=7$, $x-y=1$ by Cramer's rule gives $x$ equal to <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $-2$ (d) $\frac{10}{5}$ and $y=2$
8. If $D=0$ and $D_x \ne 0$, the system has <span class="marks">[1]</span>
   (a) a unique solution (b) exactly two solutions (c) infinitely many solutions (d) no solution
9. For a $3\times3$ matrix $A$ with $|A| = 4$, the value of $|\mathrm{adj}\,A|$ is <span class="marks">[1]</span>
   (a) $4$ (b) $8$ (c) $16$ (d) $64$
10. The inverse of a non-singular matrix $A$ is <span class="marks">[1]</span>
    (a) $|A|\cdot\mathrm{adj}\,A$ (b) $\frac{1}{|A|}\mathrm{adj}\,A$ (c) $\frac{\mathrm{adj}\,A}{A}$ (d) $\frac{1}{A}$
11. The row-equivalent method solves $AX=B$ by reducing the augmented matrix to <span class="marks">[1]</span>
    (a) the identity matrix (b) upper triangular (row echelon) form (c) a diagonal matrix of ones (d) its transpose
12. If $A$ is a $2\times2$ matrix with $|A| = 3$, then $|A^{-1}|$ equals <span class="marks">[1]</span>
    (a) $3$ (b) $9$ (c) $\frac{1}{3}$ (d) $-3$

::: note Answer key — 11.5
**1.** (b) — $y = \frac{D_y}{D}$, and $D_y$ replaces the $y$-column by the constants, giving $p_1r_2-p_2r_1$ over $p_1q_2-p_2q_1$. (The paper printed its four options as determinant ratios; they are written out here.)
**2.** (b) — $D \ne 0$ means $A^{-1}$ exists, so $X=A^{-1}B$ is the one and only solution.
**3.** (a) — $(2)(-1)-(3)(3) = -2-9 = -11$.
**4.** (a) — zero determinant means the rows are dependent; the matrix is singular and has no inverse.
**5.** (a) — write both in the form $ax+by=c$: $3x+2y=1$ and $4x+y=3$, so the constant column is $(1,\ 3)$.
**6.** (b) — numerator is the determinant with the $x$-column replaced; the denominator is always $D$.
**7.** (b) — $D = -5$, $D_x = (7)(-1)-(3)(1) = -10$, so $x = \frac{-10}{-5} = 2$ (and $y=1$).
**8.** (d) — $D=0$ kills the unique solution; a non-zero $D_x$ makes the equations contradict each other.
**9.** (c) — $|\mathrm{adj}\,A| = |A|^{n-1} = 4^{2} = 16$.
**10.** (b) — the adjoint divided by the determinant.
**11.** (b) — Gauss elimination stops at upper triangular form; back-substitution finishes the job.
**12.** (c) — $|A^{-1}| = \frac{1}{|A|} = \frac{1}{3}$.
:::

::: caution Distractor analysis — Matrix Based System of Linear Equations
**Inverting the Cramer fraction.** Option (c) in the 2082 MCQ 2 is $\frac{D}{D_y}$
— the right two determinants, upside down. The rule is always *the modified
determinant on top, $D$ underneath*. Check the dimensions in your head: if $D=0$
the answer must blow up, so $D$ belongs in the denominator.

**Replacing the wrong column.** Option (a) in the same question is $D_x$ over $D$,
i.e. the answer for $x$ offered as the answer for $y$. Replace the column of the
variable you are solving for.

**Not moving the constant across first.** In Q5 the equation is printed as
$3x+2y-1=0$. The constant is $+1$, not $-1$, once the $-1$ is moved to the right.
Option (b) is exactly this sign slip, and it is the same slip the 2082 Group B
item (write the augmented matrix of $3x+2y-1=0$ and $4x+y=3$) was testing.

**Confusing "no solution" with "infinitely many".** Both have $D=0$. The tie is
broken by $D_x$, $D_y$, $D_z$: all zero means infinitely many solutions; any one
non-zero means none. The 2079 MCQ 10 tested the "infinitely many" branch with the
line $0\times z = 0$.

**Cubing instead of squaring the adjoint determinant.** In Q9 the distractor $64$
uses $|A|^{n}$. The correct index is $n-1$.
:::

## 11.6 Properties of a Triangle

The grid's footnote guarantees a Trigonometry MCQ every year. But look at what has
actually filled that slot: **2081 and 2082 asked for a half-angle formula
($\cos\frac{A}{2}$ and $\sec\frac{B}{2}$), while 2079 and 2080 filled it with
Grade-11 carry-over — inverse circular functions and general solutions of
trigonometric equations.** All four are included below, tagged. So revise the
half-angle set *and* keep your Grade-11 inverse-circular and general-solution
formulae on the same card.

| Result | Formula |
|---|---|
| Sine law | $\frac{a}{\sin A}=\frac{b}{\sin B}=\frac{c}{\sin C}=2R$ |
| Cosine law | $\cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc}$ |
| Tangent law | $\tan\frac{B-C}{2} = \frac{b-c}{b+c}\cot\frac{A}{2}$ |
| Projection law | $a = b\cos C + c\cos B$ |
| Semi-perimeter | $s = \frac{a+b+c}{2}$ |
| Half angle, sine | $\sin\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{bc}}$ |
| Half angle, cosine | $\cos\frac{A}{2} = \sqrt{\frac{s(s-a)}{bc}}$ |
| Half angle, tangent | $\tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}}$ |
| Area, two sides and included angle | $\Delta = \frac{1}{2}ab\sin C$ |
| Area, three sides (Heron) | $\Delta = \sqrt{s(s-a)(s-b)(s-c)}$ |
| Angle sum | $A+B+C = 180^{\circ}$ |
| Inverse circular identity | $\sin^{-1}x = \cos^{-1}\sqrt{1-x^{2}}$ for $0 \leq x \leq 1$ |
| Domain of $\sin^{-1}x$ | $[-1,\ 1]$; range $\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$ |
| General solution, $\tan\theta = \tan\alpha$ | $\theta = n\pi + \alpha$ |
| General solution, $\cos\theta = \cos\alpha$ | $\theta = 2n\pi \pm \alpha$ |
| General solution, $\sin\theta = \sin\alpha$ | $\theta = n\pi + (-1)^{n}\alpha$ |

**Multiple choice questions**

1. In any triangle $ABC$, $a$, $b$, $c$ are the sides and $s$ is the semi-perimeter. Which one of the following is equal to $\cos\frac{A}{2}$? (NEB 2081) <span class="marks">[1]</span>
   (a) $\sqrt{\frac{s(s-a)}{bc}}$ (b) $\sqrt{\frac{(s-b)(s-c)}{s(s-a)}}$ (c) $\sqrt{\frac{s(s-a)}{(s-b)(s-c)}}$ (d) $\sqrt{\frac{(s-b)(s-c)}{bc}}$
2. Which one of the following is the value of $\sec\frac{B}{2}$? (NEB 2082) <span class="marks">[1]</span>
   (a) $\sqrt{\frac{ca}{s-b}}$ (b) $\sqrt{\frac{bc}{s(s-a)}}$ (c) $\sqrt{\frac{bc}{s(s-c)}}$ (d) $\sqrt{\frac{ca}{s(s-b)}}$
3. $\sin^{-1}x$ is equal to (NEB 2079) <span class="marks">[1]</span>
   (a) $\cos^{-1}\sqrt{x^{2}-1}$ (b) $\tan^{-1}\sqrt{1-x^{2}}$ (c) $\mathrm{cosec}^{-1}\sqrt{1-x^{2}}$ (d) $\cos^{-1}\sqrt{1-x^{2}}$
4. If $\tan x + \frac{1}{\sqrt{3}} = 0$ is a trigonometric equation, the general value of $x$ is (NEB 2079) <span class="marks">[1]</span>
   (a) $n\pi \pm \frac{\pi}{6}$ (b) $2n\pi + \frac{\pi}{6}$ (c) $2n\pi + \frac{5\pi}{6}$ (d) $n\pi + \frac{5\pi}{6}$
5. What is the domain of $y = \sin^{-1}x$? (NEB 2080) <span class="marks">[1]</span>
   (a) $(-1,\ 1)$ (b) $(-\infty,\ \infty)$ (c) $[0,\ 1]$ (d) $[-1,\ 1]$
6. Which one of the following is the general solution of $2\cos\theta - 1 = 0$? (NEB 2080) <span class="marks">[1]</span>
   (a) $n\pi + (-1)^{n}\frac{\pi}{3}$ (b) $n\pi \pm \frac{\pi}{3}$ (c) $n\pi + \frac{\pi}{3}$ (d) $2n\pi \pm \frac{\pi}{3}$
7. In any triangle $ABC$, $\frac{a}{\sin A}$ equals <span class="marks">[1]</span>
   (a) $R$ (b) $2R$ (c) $\frac{R}{2}$ (d) $4R$
8. The projection law gives $a$ as <span class="marks">[1]</span>
   (a) $b\cos C + c\cos B$ (b) $b\cos B + c\cos C$ (c) $b\sin C + c\sin B$ (d) $b\cos A + c\cos A$
9. The tangent law states that $\tan\frac{B-C}{2}$ equals <span class="marks">[1]</span>
   (a) $\frac{b+c}{b-c}\cot\frac{A}{2}$ (b) $\frac{b-c}{b+c}\cot\frac{A}{2}$ (c) $\frac{b-c}{b+c}\tan\frac{A}{2}$ (d) $\frac{b+c}{b-c}\tan\frac{A}{2}$
10. $\sin\frac{A}{2}$ equals <span class="marks">[1]</span>
    (a) $\sqrt{\frac{s(s-a)}{bc}}$ (b) $\sqrt{\frac{(s-b)(s-c)}{bc}}$ (c) $\sqrt{\frac{(s-b)(s-c)}{s(s-a)}}$ (d) $\sqrt{\frac{bc}{s(s-a)}}$
11. In a triangle with $b=4$, $c=5$ and $A=30^{\circ}$, the area is <span class="marks">[1]</span>
    (a) $5$ (b) $10$ (c) $\frac{5\sqrt{3}}{2}$ (d) $20$
12. In a triangle with $a=7$, $b=8$, $c=9$, the value of $\cos A$ is <span class="marks">[1]</span>
    (a) $\frac{1}{3}$ (b) $\frac{2}{3}$ (c) $\frac{11}{21}$ (d) $\frac{1}{6}$

::: note Answer key — 11.6
**1.** (a) — $\cos\frac{A}{2}=\sqrt{\frac{s(s-a)}{bc}}$; (d) is $\sin\frac{A}{2}$ and (b) is $\tan\frac{A}{2}$.
**2.** (d) — $\cos\frac{B}{2}=\sqrt{\frac{s(s-b)}{ca}}$, so its reciprocal is $\sqrt{\frac{ca}{s(s-b)}}$.
**3.** (d) — if $\sin\theta = x$ then $\cos\theta = \sqrt{1-x^{2}}$, so $\theta = \cos^{-1}\sqrt{1-x^{2}}$ (valid for $0 \leq x \leq 1$).
**4.** (d) — $\tan x = -\frac{1}{\sqrt{3}} = \tan\frac{5\pi}{6}$, so $x = n\pi + \frac{5\pi}{6}$. Machine-checked: $\tan\frac{5\pi}{6} = -\frac{\sqrt{3}}{3}$.
**5.** (d) — $\sin\theta$ takes every value in $[-1,1]$ including the endpoints, so the inverse is defined on the closed interval.
**6.** (d) — $\cos\theta = \frac{1}{2} = \cos\frac{\pi}{3}$, and the general solution of $\cos\theta=\cos\alpha$ is $\theta = 2n\pi \pm \alpha$.
**7.** (b) — the sine law's common ratio is the diameter of the circumcircle, $2R$.
**8.** (a) — each side is the sum of the projections of the other two onto it.
**9.** (b) — the difference of the sides over their sum, times $\cot$ of half the third angle.
**10.** (b) — $\sin\frac{A}{2}=\sqrt{\frac{(s-b)(s-c)}{bc}}$.
**11.** (a) — $\frac{1}{2}bc\sin A = \frac{1}{2}(4)(5)\left(\frac{1}{2}\right) = 5$.
**12.** (b) — $\cos A = \frac{8^{2}+9^{2}-7^{2}}{2(8)(9)} = \frac{96}{144} = \frac{2}{3}$.
:::

::: caution Distractor analysis — Properties of a Triangle
**Rotating the half-angle trio.** $\sin\frac{A}{2}$, $\cos\frac{A}{2}$ and
$\tan\frac{A}{2}$ share the same four ingredients $s$, $s-a$, $s-b$, $s-c$
arranged three ways, and every paper offers all three as options. Lock it with
one sentence: **sine takes $(s-b)(s-c)$ on top, cosine takes $s(s-a)$ on top, and
tangent is sine over cosine.** The 2081 MCQ 3 and 2082 MCQ 3 are both exactly this.

**Forgetting to reciprocate for $\sec$ and $\mathrm{cosec}$.** In the 2082 item the
question asks for $\sec\frac{B}{2}$, not $\cos\frac{B}{2}$. Option (b) has the
right shape with the wrong letter shifted; option (a) has dropped the $s$ out of
the denominator entirely. Write $\cos\frac{B}{2}$ first, then flip it.

**Using $2n\pi\pm\alpha$ for a tangent equation.** In the 2079 general-value item,
option (a) $n\pi\pm\frac{\pi}{6}$ mixes the tangent period with the cosine
$\pm$ pattern. Tangent has period $\pi$ and no $\pm$: $\theta = n\pi+\alpha$.
Cosine gets the $\pm$; sine gets the $(-1)^{n}$.

**Open versus closed interval for an inverse function.** In the 2080 domain item,
$(-1,1)$ (option (a)) excludes $\pm1$, but $\sin^{-1}(\pm1) = \pm\frac{\pi}{2}$
exists. Domains of $\sin^{-1}$ and $\cos^{-1}$ are closed.

**Using the wrong pair of sides in the area formula.** $\Delta =
\frac{1}{2}ab\sin C$ needs the angle **between** the two sides you use. In Q11 the
sides are $b$ and $c$, so the angle must be $A$.
:::

## 11.7 Solution of Triangles

Only 4 working hours, and no MCQ has yet come from it in 2079, 2080, 2081 or 2082.
It reached Group C once, in 2081 Q21a ("if $a = 3+\sqrt{3}$, $b=2$, $c=\sqrt{3}$
then solve the triangle"). Learn the decision rule — which law for which given
data — and move on.

| Data given | Method to use | Notes |
|---|---|---|
| Three sides $a,b,c$ | cosine law, or the half-angle formulae | always exactly one triangle |
| Two sides and the included angle | tangent law for the angles, then sine law | one triangle |
| Two angles and one side | sine law (find the third angle first) | one triangle |
| Two sides and a non-included angle | sine law | the **ambiguous case**: $0$, $1$ or $2$ triangles |
| Right angle present | Pythagoras and simple ratios | fastest route |
| $a=b$ | then $A=B$ (isosceles) | equal sides face equal angles |
| Largest side | faces the largest angle | use it to spot an obtuse triangle |
| Check | $A+B+C$ must come to $180^{\circ}$ | always do this |

**Multiple choice questions**

1. To solve a triangle when all three sides are given, the appropriate law is <span class="marks">[1]</span>
   (a) sine law (b) cosine law (c) projection law (d) tangent law
2. Two sides and the included angle are given. The law that leads directly to the other two angles is <span class="marks">[1]</span>
   (a) sine law (b) cosine law (c) tangent law (d) projection law
3. Two angles and one side are given. The right tool is <span class="marks">[1]</span>
   (a) sine law (b) cosine law (c) tangent law (d) Heron's formula
4. In $\Delta ABC$, if $a=b$ then <span class="marks">[1]</span>
   (a) $A=B$ (b) $A=C$ (c) $A+B=90^{\circ}$ (d) $C=90^{\circ}$
5. A triangle has $b=3$, $c=3$ and $A=60^{\circ}$. The triangle is <span class="marks">[1]</span>
   (a) right-angled (b) obtuse-angled (c) equilateral (d) impossible
6. In $\Delta ABC$, $A=45^{\circ}$, $B=105^{\circ}$ and $a=\sqrt{2}$. Then $c$ equals <span class="marks">[1]</span>
   (a) $1$ (b) $\sqrt{2}$ (c) $\sqrt{3}$ (d) $2$
7. The ambiguous case arises when the data given are <span class="marks">[1]</span>
   (a) three sides (b) two sides and the included angle (c) two sides and a non-included angle (d) two angles and one side
8. If $a=5$, $b=12$, $c=13$, then the largest angle of the triangle is <span class="marks">[1]</span>
   (a) $60^{\circ}$ (b) $90^{\circ}$ (c) $120^{\circ}$ (d) $150^{\circ}$

::: note Answer key — 11.7
**1.** (b) — the cosine law is the only one that gives an angle from three sides alone.
**2.** (c) — the tangent law gives $\frac{B-C}{2}$ directly, and $\frac{B+C}{2}=90^{\circ}-\frac{A}{2}$ is known, so $B$ and $C$ follow by adding and subtracting.
**3.** (a) — find the third angle from $A+B+C=180^{\circ}$, then the sine law gives the remaining sides.
**4.** (a) — equal sides face equal angles; by the sine law $\sin A = \sin B$.
**5.** (c) — $b=c$ makes it isosceles with $B=C$, and $B=C=\frac{180^{\circ}-60^{\circ}}{2}=60^{\circ}$, so all three angles are $60^{\circ}$.
**6.** (a) — $C = 180^{\circ}-45^{\circ}-105^{\circ}=30^{\circ}$, and $c = \frac{a\sin C}{\sin A} = \frac{\sqrt{2}\times\frac{1}{2}}{\frac{1}{\sqrt{2}}} = 1$.
**7.** (c) — the sine law can give two supplementary angles, so there may be two triangles, one, or none.
**8.** (b) — $5^{2}+12^{2}=169=13^{2}$, so the angle opposite $13$ is a right angle. Machine-checked: $\cos C = 0$.
:::

::: caution Distractor analysis — Solution of Triangles
**Reaching for the sine law when three sides are given.** The sine law needs an
angle to start from; with only sides you must use the cosine law (or half-angle
formulae). Option (a) in Q1 is the reflex answer and it is a dead end.

**Assuming an isosceles triangle cannot be equilateral.** In Q5, $b=c$ with
$A=60^{\circ}$ forces all angles to $60^{\circ}$. Students stop at "isosceles" and
pick (a) or (b) without finishing the angle sum.

**Missing the ambiguous case.** Given $a$, $b$ and $A$, $\sin B = \frac{b\sin
A}{a}$ has two solutions in $(0^{\circ},180^{\circ})$ whenever the value is
strictly between $0$ and $1$. Always test whether the obtuse partner still leaves
a positive third angle.

**Not checking the angle sum.** Every solved triangle must satisfy
$A+B+C=180^{\circ}$. It takes five seconds and catches almost every arithmetic
slip in a Group C answer.
:::

## 11.8 Conic Sections

The biggest MCQ payer in the book. Analytic Geometry carries 9 marks and shares 3
MCQs with Trigonometry and Vectors, and a conic item has appeared in **all four**
verified years: 2079 (eccentricity of a hyperbola), 2080 (identify the conic),
2081 (focus of a parabolic reflector), 2082 (tangency condition for a circle).
Learn the table below across, not down — the examiner's favourite move is to give
you a parabola formula in an ellipse question.

| | Circle $x^{2}+y^{2}=a^{2}$ | Parabola $y^{2}=4ax$ | Ellipse $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$ | Hyperbola $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$ |
|---|---|---|---|---|
| Eccentricity $e$ | $0$ | $1$ | $\sqrt{1-\frac{b^{2}}{a^{2}}}$, so $e<1$ | $\sqrt{1+\frac{b^{2}}{a^{2}}}$, so $e>1$ |
| Focus / foci | centre only | $(a,\ 0)$ | $(\pm ae,\ 0)$ | $(\pm ae,\ 0)$ |
| Directrix | none | $x=-a$ | $x = \pm\frac{a}{e}$ | $x = \pm\frac{a}{e}$ |
| Latus rectum | $2a$ (a diameter) | $4a$ | $\frac{2b^{2}}{a}$ | $\frac{2b^{2}}{a}$ |
| $b^{2}$ relation | — | — | $b^{2}=a^{2}(1-e^{2})$ | $b^{2}=a^{2}(e^{2}-1)$ |
| Tangency of $y=mx+c$ | $c^{2}=a^{2}(1+m^{2})$ | $c=\frac{a}{m}$ | $c^{2}=a^{2}m^{2}+b^{2}$ | $c^{2}=a^{2}m^{2}-b^{2}$ |
| Tangent at $(x_1,y_1)$ | $xx_1+yy_1=a^{2}$ | $yy_1 = 2a(x+x_1)$ | $\frac{xx_1}{a^{2}}+\frac{yy_1}{b^{2}}=1$ | $\frac{xx_1}{a^{2}}-\frac{yy_1}{b^{2}}=1$ |
| General centre form | $x^{2}+y^{2}+2gx+2fy+c=0$, centre $(-g,-f)$, radius $\sqrt{g^{2}+f^{2}-c}$ | axis is the $x$-axis | major axis $2a$, minor $2b$ | transverse $2a$, conjugate $2b$ |
| Length of tangent from $(x_1,y_1)$ | $\sqrt{x_1^{2}+y_1^{2}-a^{2}}$ | — | — | — |

```figure caption="The four conics, each panel drawn to the same scale, with focus $S$, directrix and latus rectum marked. Eccentricity is the ratio $SP/PM$ of the distance from the focus to the distance from the directrix: $e=0$ for a circle, $e=1$ for a parabola, $e<1$ for an ellipse, $e>1$ for a hyperbola."
import numpy as np
fig, axs = plt.subplots(2, 2, figsize=(5.0, 3.4))
XL, YL = (-1.75, 1.75), (-1.15, 1.15)
th = np.linspace(0, 2*np.pi, 400)

def frame(ax, title):
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_title(title, fontsize=8.6, pad=3)

# --- circle
ax = axs[0][0]; frame(ax, "Circle   e = 0")
ax.plot(0.85*np.cos(th), 0.85*np.sin(th), color=ACCENT, lw=1.6)
ax.plot([0], [0], "o", ms=3.2, color=INK)
ax.annotate("C", (0, 0), xytext=(4, 3), textcoords="offset points", fontsize=8)
ax.plot([-0.85, 0.85], [0, 0], color=SERIES[1], lw=1.3)
ax.text(0, -1.06, "diameter = 2a", ha="center", fontsize=7.4, color=SERIES[1])

# --- parabola
ax = axs[0][1]; frame(ax, "Parabola   e = 1")
a = 0.20
yy = np.linspace(-0.95, 0.95, 300)
ax.plot(-1.0 + yy**2/(4*a), yy, color=ACCENT, lw=1.6)
ax.plot([-1.0+a], [0], "o", ms=3.2, color=INK)
ax.annotate("S(a, 0)", (-1.0+a, 0), xytext=(9, -13), textcoords="offset points",
            fontsize=7.4)
ax.plot([-1.0-a, -1.0-a], [-1.0, 1.0], color=MUTED, lw=1.0, ls="--")
ax.text(-1.2, 1.03, "x = −a", ha="center", fontsize=7.4, color=MUTED)
ax.plot([-1.0+a, -1.0+a], [-2*a, 2*a], color=SERIES[1], lw=1.4)
ax.text(0.55, 0.60, "LR = 4a", ha="center", fontsize=7.4, color=SERIES[1])

# --- ellipse
ax = axs[1][0]; frame(ax, "Ellipse   e < 1")
A, B = 1.15, 0.70
e = np.sqrt(1-(B/A)**2)
ax.plot(A*np.cos(th), B*np.sin(th), color=ACCENT, lw=1.6)
for sgn in (-1, 1):
    ax.plot([sgn*A*e], [0], "o", ms=3.2, color=INK)
ax.annotate("S′", (-A*e, 0), xytext=(-4, 7), textcoords="offset points", fontsize=7.6)
ax.annotate("S", (A*e, 0), xytext=(-16, -13), textcoords="offset points", fontsize=7.6)
ax.plot([A*e, A*e], [-B**2/A, B**2/A], color=SERIES[1], lw=1.4)
ax.plot([A/e, A/e], [-0.85, 0.85], color=MUTED, lw=1.0, ls="--")
ax.text(A/e, 0.92, "x = a/e", ha="center", fontsize=7.4, color=MUTED)
ax.text(-0.15, -1.06, "LR = 2b²/a", ha="center", fontsize=7.4, color=SERIES[1])

# --- hyperbola
ax = axs[1][1]; frame(ax, "Hyperbola   e > 1")
A, B = 0.55, 0.60
e = np.sqrt(1+(B/A)**2)
tt = np.linspace(-1.1, 1.1, 260)
for sgn in (-1, 1):
    ax.plot(sgn*A*np.cosh(tt), B*np.sinh(tt), color=ACCENT, lw=1.6)
    ax.plot([sgn*A*e], [0], "o", ms=3.2, color=INK)
ax.annotate("S′", (-A*e, 0), xytext=(-4, 7), textcoords="offset points", fontsize=7.6)
ax.annotate("S", (A*e, 0), xytext=(7, -14), textcoords="offset points", fontsize=7.6)
ax.plot([A*e, A*e], [-B**2/A, B**2/A], color=SERIES[1], lw=1.4)
ax.plot([A/e, A/e], [-0.82, 0.82], color=MUTED, lw=1.0, ls="--")
ax.text(A/e, 0.90, "x = a/e", ha="center", fontsize=7.4, color=MUTED)
ax.text(0.15, -1.06, "LR = 2b²/a", ha="center", fontsize=7.4, color=SERIES[1])

fig.subplots_adjust(wspace=0.05, hspace=0.32)
```

**Multiple choice questions**

1. In which condition will the line $y=mx+c$ be tangent to the circle $x^{2}+y^{2}=a^{2}$? (NEB 2082) <span class="marks">[1]</span>
   (a) $a = c\sqrt{1+m^{2}}$ (b) $a = \pm c\sqrt{1+m^{2}}$ (c) $c = \pm a\sqrt{1+m^{2}}$ (d) $c = a\sqrt{1+m^{2}}$
2. A parabolic reflector is $20$ cm in diameter and $5$ cm deep. Which one of the following gives the co-ordinates of its focus? (NEB 2081) <span class="marks">[1]</span>
   (a) $(0,\ 5)$ (b) $(0,\ -5)$ (c) $(5,\ 0)$ (d) $(-5,\ 0)$
3. Which one of the following conics is represented by the equation $4x^{2}-16x+y^{2}=48$? (NEB 2080) <span class="marks">[1]</span>
   (a) hyperbola (b) ellipse (c) parabola (d) circle
4. The eccentricity of the hyperbola $\frac{x^{2}}{16}-\frac{y^{2}}{64}=1$ is (NEB 2079) <span class="marks">[1]</span>
   (a) $\frac{3}{5}$ (b) $\frac{5}{3}$ (c) $\frac{3}{4}$ (d) $\frac{4}{3}$
5. The eccentricity of a parabola is <span class="marks">[1]</span>
   (a) $0$ (b) $\frac{1}{2}$ (c) $1$ (d) greater than $1$
6. The length of the latus rectum of $y^{2}=12x$ is <span class="marks">[1]</span>
   (a) $3$ (b) $6$ (c) $12$ (d) $24$
7. The focus of the parabola $y^{2}=8x$ is <span class="marks">[1]</span>
   (a) $(0,\ 2)$ (b) $(2,\ 0)$ (c) $(4,\ 0)$ (d) $(8,\ 0)$
8. The directrix of the parabola $y^{2}=4x$ is <span class="marks">[1]</span>
   (a) $x=1$ (b) $x=-1$ (c) $y=1$ (d) $y=-1$
9. The eccentricity of the ellipse $\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$ is <span class="marks">[1]</span>
   (a) $\frac{3}{5}$ (b) $\frac{4}{5}$ (c) $\frac{5}{4}$ (d) $\frac{5}{3}$
10. The length of the latus rectum of $\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$ is <span class="marks">[1]</span>
    (a) $\frac{8}{5}$ (b) $\frac{16}{5}$ (c) $\frac{32}{5}$ (d) $\frac{50}{4}$
11. The eccentricity of $\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$ is <span class="marks">[1]</span>
    (a) $\frac{3}{5}$ (b) $\frac{4}{5}$ (c) $\frac{5}{4}$ (d) $\frac{5}{3}$
12. The length of the tangent drawn from $(5,\ 4)$ to the circle $x^{2}+y^{2}=16$ is <span class="marks">[1]</span>
    (a) $3$ (b) $4$ (c) $5$ (d) $\sqrt{41}$
13. The equation of the tangent to $x^{2}+y^{2}=25$ at the point $(3,\ 4)$ is <span class="marks">[1]</span>
    (a) $3x+4y=25$ (b) $4x+3y=25$ (c) $3x-4y=25$ (d) $3x+4y=5$
14. The line $y=mx+c$ touches the parabola $y^{2}=4ax$ if <span class="marks">[1]</span>
    (a) $c=am$ (b) $c=\frac{a}{m}$ (c) $c^{2}=a^{2}(1+m^{2})$ (d) $c^{2}=a^{2}m^{2}+b^{2}$
15. The centre of the circle $x^{2}+y^{2}-4x+6y-12=0$ is <span class="marks">[1]</span>
    (a) $(2,\ -3)$ (b) $(-2,\ 3)$ (c) $(4,\ -6)$ (d) $(-4,\ 6)$
16. The radius of the circle $x^{2}+y^{2}-4x+6y-12=0$ is <span class="marks">[1]</span>
    (a) $3$ (b) $4$ (c) $5$ (d) $12$
17. A normal drawn to a circle at any point on it always passes through <span class="marks">[1]</span>
    (a) the origin (b) the centre (c) the focus (d) the directrix
18. The eccentricity of the rectangular hyperbola $x^{2}-y^{2}=a^{2}$ is <span class="marks">[1]</span>
    (a) $1$ (b) $\sqrt{2}$ (c) $2$ (d) $\frac{1}{\sqrt{2}}$

::: note Answer key — 11.8
**1.** (c) — the perpendicular distance from the centre to the line must equal the radius: $\frac{|c|}{\sqrt{1+m^{2}}}=a$, so $c = \pm a\sqrt{1+m^{2}}$, i.e. $c^{2}=a^{2}(1+m^{2})$.
**2.** (c) — put the vertex at the origin, $y^{2}=4ax$. The rim is $10$ cm from the axis at a depth of $5$ cm, so $(5,10)$ lies on it: $100 = 20a$, $a=5$, focus $(5,0)$.
**3.** (b) — complete the square: $4(x-2)^{2}+y^{2}=64$, i.e. $\frac{(x-2)^{2}}{16}+\frac{y^{2}}{64}=1$ — an ellipse (both squares positive, unequal denominators).
**4.** **No printed option is correct.** With the numbers as printed, $a^{2}=16$, $b^{2}=64$ and $e=\sqrt{1+\frac{64}{16}}=\sqrt{5}\approx2.236$. Option (b) $\frac{5}{3}$ is the eccentricity of $\frac{x^{2}}{9}-\frac{y^{2}}{16}=1$, which is almost certainly the intended curve. Machine-checked both.
**5.** (c) — a parabola is the locus with $SP=PM$ exactly, so $e=1$.
**6.** (c) — $4a=12$, and the latus rectum of $y^{2}=4ax$ is $4a$, so $12$.
**7.** (b) — $4a=8$ gives $a=2$, so the focus is $(2,0)$.
**8.** (b) — $4a=4$ gives $a=1$; the directrix of $y^{2}=4ax$ is $x=-a=-1$.
**9.** (a) — $e=\sqrt{1-\frac{16}{25}}=\sqrt{\frac{9}{25}}=\frac{3}{5}$.
**10.** (c) — $\frac{2b^{2}}{a}=\frac{2(16)}{5}=\frac{32}{5}$.
**11.** (d) — $e=\sqrt{1+\frac{16}{9}}=\sqrt{\frac{25}{9}}=\frac{5}{3}$.
**12.** (c) — $\sqrt{x_1^{2}+y_1^{2}-a^{2}} = \sqrt{25+16-16}=5$.
**13.** (a) — the tangent to $x^{2}+y^{2}=a^{2}$ at $(x_1,y_1)$ is $xx_1+yy_1=a^{2}$, giving $3x+4y=25$.
**14.** (b) — substituting $y=mx+c$ into $y^{2}=4ax$ and setting the discriminant to zero gives $c=\frac{a}{m}$.
**15.** (a) — for $x^{2}+y^{2}+2gx+2fy+c=0$ the centre is $(-g,-f)$; here $2g=-4$, $2f=6$, so $(2,-3)$.
**16.** (c) — $\sqrt{g^{2}+f^{2}-c} = \sqrt{4+9+12}=\sqrt{25}=5$.
**17.** (b) — the radius is perpendicular to the tangent, and the normal is along the radius.
**18.** (b) — here $b=a$, so $e=\sqrt{1+1}=\sqrt{2}$.
:::

::: caution Distractor analysis — Conic Sections
**The tangency condition written with $a$ and $c$ swapped.** This is exactly the
2082 MCQ 4. Options (a) and (b) read $a = \pm c\sqrt{1+m^{2}}$, which makes the
radius depend on the intercept instead of the other way round. Test it on a case
you know: the horizontal line $y=c$ touches $x^{2}+y^{2}=a^{2}$ when $c=\pm a$, and
with $m=0$ the correct form gives $c = \pm a$. The swapped form gives $a=\pm c$
here too — so also test $m=1$, where only $c=\pm a\sqrt{2}$ is right.

**Using the ellipse eccentricity formula on a hyperbola.** $\sqrt{1-\frac{b^{2}}
{a^{2}}}$ and $\sqrt{1+\frac{b^{2}}{a^{2}}}$ differ by one sign and give answers on
opposite sides of $1$. Sanity-check the answer: **an ellipse must give $e<1$, a
hyperbola must give $e>1$.** In Q9 and Q11 the same pair of numbers $3,4,5$
produces $\frac{3}{5}$ for the ellipse and $\frac{5}{3}$ for the hyperbola.

**Taking $a^{2}$ as the larger denominator without looking at the sign.** In the
2080 "identify the conic" item, a student who sees $4x^{2}$ and $y^{2}$ with
different coefficients often answers "hyperbola". A hyperbola needs a **minus**
sign between the squares. Both signs positive with unequal coefficients is an
ellipse; both positive and equal is a circle.

**Confusing $4a$ with $a$ in a parabola.** In Q6, Q7 and Q8 the distractors are all
built from misreading $y^{2}=4ax$. Write $4a =$ (the coefficient) first, then
divide, then place the focus at $(a,0)$ and the directrix at $x=-a$.

**Halving or doubling the latus rectum of an ellipse.** In Q10 the distractor
$\frac{16}{5}$ is $\frac{b^{2}}{a}$ — the *semi*-latus rectum. The full chord is
$\frac{2b^{2}}{a}$.

**A printed option set can be wrong.** Question 4 above is a genuine 2079 MCQ whose
four options do not contain the right answer. If that happens to you in the hall,
do the calculation once more, pick the option nearest to a curve the numbers
*could* have described, and move on — do not lose four minutes on one mark.
:::

## 11.9 Product of Vectors

A vector MCQ has appeared in every one of 2079, 2080, 2081 and 2082, and in three
of those four years the item turned on **the sign of a cross product**. That is the
single most profitable thing in this section.

| Result | Formula / condition |
|---|---|
| Scalar product | $\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta = a_1b_1+a_2b_2+a_3b_3$ |
| Commutative | $\vec{a}\cdot\vec{b} = \vec{b}\cdot\vec{a}$ |
| Perpendicular test | $\vec{a}\cdot\vec{b}=0$ with neither vector $\vec{0}$ |
| Angle between vectors | $\cos\theta = \frac{\vec{a}\cdot\vec{b}}{|\vec{a}||\vec{b}|}$ |
| Projection of $\vec{b}$ on $\vec{a}$ | $\frac{\vec{a}\cdot\vec{b}}{|\vec{a}|}$ |
| Base-vector dots | $\hat{i}\cdot\hat{i}=1$, $\hat{i}\cdot\hat{j}=0$ |
| Vector product | $\vec{a}\times\vec{b} = |\vec{a}||\vec{b}|\sin\theta\,\hat{n}$ |
| **Anti-commutative** | $\vec{a}\times\vec{b} = -(\vec{b}\times\vec{a})$ |
| Base-vector crosses, cyclic | $\hat{i}\times\hat{j}=\hat{k}$, $\hat{j}\times\hat{k}=\hat{i}$, $\hat{k}\times\hat{i}=\hat{j}$ |
| Base-vector crosses, reversed | $\hat{j}\times\hat{i}=-\hat{k}$, $\hat{k}\times\hat{j}=-\hat{i}$, $\hat{i}\times\hat{k}=-\hat{j}$ |
| Self-cross | $\vec{a}\times\vec{a} = \vec{0}$ |
| Parallelogram from adjacent sides | area $= |\vec{a}\times\vec{b}|$ |
| Triangle from two sides | area $= \frac{1}{2}|\vec{a}\times\vec{b}|$ |
| Parallelogram from **diagonals** | area $= \frac{1}{2}|\vec{d_1}\times\vec{d_2}|$ |
| Link between the products | $|\vec{a}\times\vec{b}|^{2} + (\vec{a}\cdot\vec{b})^{2} = |\vec{a}|^{2}|\vec{b}|^{2}$ |
| Perpendicularity of the cross product | $(\vec{a}\times\vec{b})\cdot\vec{a} = (\vec{a}\times\vec{b})\cdot\vec{b} = 0$ |

```figure caption="The vector product. $\vec{a}\times\vec{b}$ points along the right-hand-rule normal $\hat{n}$, and its magnitude $|\vec{a}||\vec{b}|\sin\theta$ is the area of the shaded parallelogram. Reversing the order flips the arrow to $-\hat{n}$, which is why $\vec{a}\times\vec{b} = -(\vec{b}\times\vec{a})$."
import numpy as np
from matplotlib.patches import Polygon, Arc
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.axis("off"); ax.set_aspect("equal")
O = np.array([0.0, 0.0])
A = np.array([2.35, 0.0])          # a
B = np.array([0.95, 1.35])         # b
ax.add_patch(Polygon([O, A, A+B, B], closed=True, fc=ACCENT, ec="none", alpha=0.14))
ax.plot([A[0], (A+B)[0]], [A[1], (A+B)[1]], color=MUTED, lw=0.9, ls="--")
ax.plot([B[0], (A+B)[0]], [B[1], (A+B)[1]], color=MUTED, lw=0.9, ls="--")
for V, lab, dx, dy, col in [(A, r"$\vec{a}$", 0.08, -0.26, INK),
                            (B, r"$\vec{b}$", -0.30, 0.10, INK)]:
    ax.annotate("", xy=V, xytext=O,
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=col,
                                shrinkA=0, shrinkB=0))
    ax.text(V[0]*0.55+dx, V[1]*0.55+dy, lab, fontsize=11, color=col)
# normal
ax.annotate("", xy=(0.0, 2.15), xytext=O,
            arrowprops=dict(arrowstyle="-|>", lw=1.8, color=SERIES[1], shrinkA=0, shrinkB=0))
ax.text(0.10, 2.22, r"$\vec{a}\times\vec{b}$", fontsize=10.5, color=SERIES[1])
ax.annotate("", xy=(0.0, -0.95), xytext=O,
            arrowprops=dict(arrowstyle="-|>", lw=1.4, color=SERIES[4], shrinkA=0, shrinkB=0))
ax.text(0.10, -1.05, r"$\vec{b}\times\vec{a}$", fontsize=9.5, color=SERIES[4])
ax.add_patch(Arc(O, 1.05, 1.05, theta1=0, theta2=54.8, color=MUTED, lw=1.0))
ax.text(0.66, 0.20, "θ", fontsize=10, color=MUTED)
ax.text(1.45, 0.62, "area = |a × b|", fontsize=8.6, color=ACCENT, ha="center")
ax.text(-2.35, 1.72, "Right-hand rule:\nfingers curl\nfrom a to b,\nthumb gives\na × b",
        fontsize=8.2, color=MUTED, ha="left", va="center", linespacing=1.35)
ax.set_xlim(-2.45, 3.75); ax.set_ylim(-1.35, 2.75)
```

**Multiple choice questions**

1. What is $\vec{a}\times\vec{b}$ if $\vec{a}=(0,0,1)$ and $\vec{b}=(0,1,0)$? (NEB 2082) <span class="marks">[1]</span>
   (a) $(-1,0,0)$ (b) $(1,0,0)$ (c) $(0,1,0)$ (d) $(0,0,-1)$
2. If $\vec{a}$ and $\vec{b}$ are two vectors then the value of $(\vec{a}-\vec{b})\times(\vec{a}+\vec{b})$ is (NEB 2079) <span class="marks">[1]</span>
   (a) $2(\vec{a}\times\vec{b})$ (b) $|\vec{a}|^{2}-|\vec{b}|^{2}$ (c) $-2(\vec{a}\times\vec{b})$ (d) $2\left(|\vec{a}|^{2}-|\vec{b}|^{2}\right)$
3. Consider $\vec{a}\times\vec{b} = \vec{c}\times\vec{d}$ and $\vec{a}\times\vec{c} = \vec{b}\times\vec{d}$. Which one of the following is parallel to $(\vec{b}-\vec{c})$? (NEB 2080) <span class="marks">[1]</span>
   (a) $\vec{a}-\vec{b}$ (b) $\vec{a}-\vec{c}$ (c) $\vec{a}-\vec{d}$ (d) $\vec{c}-\vec{d}$
4. $\vec{a}$ and $\vec{b}$ are two non-zero vectors. Which of the following results is the smallest number? (NEB 2081) <span class="marks">[1]</span>
   (a) $(\vec{a}\times\vec{b})\cdot(\vec{b}\times\vec{a})$ (b) $(\vec{a}\times\vec{a})\cdot\vec{a}$ (c) $(\vec{b}\times\vec{b})\cdot\vec{b}$ (d) $(\vec{a}\times\vec{a})\cdot\vec{b}$
5. The value of $\hat{i}\cdot\hat{j}$ is <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $\hat{k}$ (d) $-\hat{k}$
6. The value of $\hat{j}\times\hat{k}$ is <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $\hat{i}$ (d) $-\hat{i}$
7. If $\vec{a}\cdot\vec{b}=0$ and neither vector is zero, then the vectors are <span class="marks">[1]</span>
   (a) parallel (b) perpendicular (c) equal (d) anti-parallel
8. Geometrically, $|\vec{a}\times\vec{b}|$ is the <span class="marks">[1]</span>
   (a) area of the parallelogram with $\vec{a}$, $\vec{b}$ as adjacent sides (b) area of the triangle with sides $\vec{a}$, $\vec{b}$ (c) volume of a parallelepiped (d) perimeter of the parallelogram
9. If $\vec{a}=2\hat{i}+3\hat{j}-\hat{k}$ and $\vec{b}=\hat{i}-\hat{j}+2\hat{k}$, then $\vec{a}\cdot\vec{b}$ is <span class="marks">[1]</span>
   (a) $-3$ (b) $1$ (c) $3$ (d) $7$
10. The angle between $\hat{i}+\hat{j}$ and $\hat{i}-\hat{j}$ is <span class="marks">[1]</span>
    (a) $0^{\circ}$ (b) $45^{\circ}$ (c) $60^{\circ}$ (d) $90^{\circ}$
11. If $\vec{a}=4\hat{i}-3\hat{j}+2\hat{k}$ and $\vec{b}=3\hat{i}-2\hat{j}+4\hat{k}$, the projection of $\vec{b}$ on $\vec{a}$ is <span class="marks">[1]</span>
    (a) $\frac{26}{\sqrt{29}}$ (b) $\frac{26}{29}$ (c) $\frac{29}{\sqrt{26}}$ (d) $26$
12. If $|\vec{a}|=3$, $|\vec{b}|=4$ and $\vec{a}\cdot\vec{b}=6$, then $|\vec{a}\times\vec{b}|$ is <span class="marks">[1]</span>
    (a) $6$ (b) $6\sqrt{3}$ (c) $12$ (d) $\sqrt{108}-6$
13. The value of $(\hat{i}+\hat{j})\times(\hat{i}-\hat{j})$ is <span class="marks">[1]</span>
    (a) $2\hat{k}$ (b) $-2\hat{k}$ (c) $\vec{0}$ (d) $2\hat{i}$
14. The area of the parallelogram whose diagonals are $\vec{a}=\hat{i}-2\hat{k}$ and $\vec{b}=4\hat{i}+3\hat{j}+\hat{k}$ is <span class="marks">[1]</span>
    (a) $3\sqrt{14}$ (b) $\frac{3\sqrt{14}}{2}$ (c) $\sqrt{126}$ (d) $\frac{\sqrt{14}}{2}$

::: note Answer key — 11.9
**1.** (a) — $\vec{a}=\hat{k}$ and $\vec{b}=\hat{j}$, and $\hat{k}\times\hat{j} = -\hat{i} = (-1,0,0)$. The cyclic order is $\hat{i}\rightarrow\hat{j}\rightarrow\hat{k}\rightarrow\hat{i}$; $\hat{k}\times\hat{j}$ runs backwards, so it takes a minus sign.
**2.** (a) — expand: $\vec{a}\times\vec{a}+\vec{a}\times\vec{b}-\vec{b}\times\vec{a}-\vec{b}\times\vec{b} = \vec{0}+\vec{a}\times\vec{b}+\vec{a}\times\vec{b}-\vec{0} = 2(\vec{a}\times\vec{b})$. (The paper prints the label "C)" twice; the fourth option is the intended (d).)
**3.** (c) — compute $(\vec{a}-\vec{d})\times(\vec{b}-\vec{c}) = \vec{a}\times\vec{b}-\vec{a}\times\vec{c}-\vec{d}\times\vec{b}+\vec{d}\times\vec{c}$. Using both given conditions this collapses to $\vec{0}$, so the two vectors are parallel. Machine-checked symbolically.
**4.** (a) — options (b), (c), (d) all contain $\vec{a}\times\vec{a}$ or $\vec{b}\times\vec{b}$, which is $\vec{0}$, so each equals $0$. Option (a) is $(\vec{a}\times\vec{b})\cdot\left(-(\vec{a}\times\vec{b})\right) = -|\vec{a}\times\vec{b}|^{2}$, which is negative (or zero) — the smallest.
**5.** (a) — $\hat{i}$ and $\hat{j}$ are perpendicular, so $\cos 90^{\circ}=0$.
**6.** (c) — $\hat{j}\times\hat{k}=\hat{i}$ by the cyclic rule.
**7.** (b) — $\cos\theta = 0$ forces $\theta = 90^{\circ}$.
**8.** (a) — $|\vec{a}||\vec{b}|\sin\theta$ is base times height for the parallelogram; half of it is the triangle.
**9.** (a) — $2(1)+3(-1)+(-1)(2) = 2-3-2 = -3$.
**10.** (d) — the dot product is $1(1)+1(-1) = 0$.
**11.** (a) — $\vec{a}\cdot\vec{b} = 12+6+8 = 26$ and $|\vec{a}|=\sqrt{16+9+4}=\sqrt{29}$, so the projection is $\frac{26}{\sqrt{29}}$.
**12.** (b) — $|\vec{a}\times\vec{b}| = \sqrt{|\vec{a}|^{2}|\vec{b}|^{2}-(\vec{a}\cdot\vec{b})^{2}} = \sqrt{144-36}=\sqrt{108}=6\sqrt{3}$.
**13.** (b) — $\hat{i}\times(-\hat{j})+\hat{j}\times\hat{i} = -\hat{k}-\hat{k} = -2\hat{k}$. Machine-checked.
**14.** (b) — for **diagonals** the area is $\frac{1}{2}|\vec{a}\times\vec{b}|$. Here $\vec{a}\times\vec{b} = 6\hat{i}-9\hat{j}+3\hat{k}$, of magnitude $\sqrt{126}=3\sqrt{14}$, so the area is $\frac{3\sqrt{14}}{2}$.
:::

::: caution Distractor analysis — Product of Vectors
**The sign error in the cross product.** Three separate things must be kept
straight, and the papers test all three.

- **The $\hat{j}$ component carries a minus.** Expanding a $3\times3$ determinant,
  the middle term is subtracted: $\vec{a}\times\vec{b} = (a_2b_3-a_3b_2)\hat{i} -
  (a_1b_3-a_3b_1)\hat{j} + (a_1b_2-a_2b_1)\hat{k}$. Dropping that minus is the
  commonest single error in the whole Vector area.
- **The cross product is anti-commutative but the dot product is not.**
  $\vec{a}\times\vec{b} = -(\vec{b}\times\vec{a})$, while
  $\vec{a}\cdot\vec{b} = \vec{b}\cdot\vec{a}$. Order matters for one and not the
  other.
- **The cyclic order.** $\hat{i}\times\hat{j}=\hat{k}$, $\hat{j}\times\hat{k}=\hat{i}$,
  $\hat{k}\times\hat{i}=\hat{j}$ — going *forwards* round the circle. Going
  backwards flips the sign. **The 2082 MCQ 5 is exactly this trap:**
  $\hat{k}\times\hat{j}$ runs backwards, so the answer is $-\hat{i}=(-1,0,0)$, not
  $+\hat{i}=(1,0,0)$. Option (b) is the trap, and it is the most-chosen wrong
  answer on that paper.

**Treating $(\vec{a}-\vec{b})\times(\vec{a}+\vec{b})$ like a difference of
squares.** Options (b) and (d) in the 2079 item are $|\vec{a}|^{2}-|\vec{b}|^{2}$,
which is what $(\vec{a}-\vec{b})\cdot(\vec{a}+\vec{b})$ gives. A cross product
cannot produce a scalar. Check the *type* of the answer before the value.

**Using the adjacent-sides formula on diagonals.** In Q14 the distractor
$3\sqrt{14}$ is $|\vec{d_1}\times\vec{d_2}|$ — twice the true area. When the
question says *diagonals*, halve it. The 2081 Group C item asked exactly this.

**Dividing by the wrong magnitude in a projection.** The projection of $\vec{b}$ on
$\vec{a}$ divides by $|\vec{a}|$, the vector you are projecting **onto**. Option (b)
in Q11 has divided by $|\vec{a}|^{2}$, which gives the scalar multiple, not the
length.
:::

## 11.10 Correlation and Regression

An important negative finding from the four verified papers: **the single
Statistics & Probability MCQ has gone to Probability every year, never to
correlation.** Correlation and regression appear instead as a full 5-mark Group B
question built on a small table — 2079 Q16, 2080 Q15, 2081 Q16, 2082 Q16 and the
CDC model Q16, without exception. So the questions below are mainly insurance and
formula drill; the marks in this unit are in Group B.

| Result | Formula / condition |
|---|---|
| Karl Pearson's coefficient | $r = \frac{\sum xy - n\bar{x}\bar{y}}{\sqrt{\left(\sum x^{2}-n\bar{x}^{2}\right)\left(\sum y^{2}-n\bar{y}^{2}\right)}}$ |
| Range | $-1 \leq r \leq 1$ |
| Regression line, $y$ on $x$ | $y-\bar{y} = b_{yx}(x-\bar{x})$ |
| Regression line, $x$ on $y$ | $x-\bar{x} = b_{xy}(y-\bar{y})$ |
| Regression coefficients | $b_{yx} = r\frac{\sigma_y}{\sigma_x}$, $b_{xy} = r\frac{\sigma_x}{\sigma_y}$ |
| $r$ from the coefficients | $r = \pm\sqrt{b_{yx}\cdot b_{xy}}$, sign of $b_{yx}$ |
| Product bound | $b_{yx}\cdot b_{xy} = r^{2} \leq 1$ |
| Point common to both lines | $(\bar{x},\ \bar{y})$ |
| $r=0$ | no linear relation; the two lines are perpendicular |
| $r=\pm1$ | perfect linear relation; the two lines coincide |
| Invariance | $r$ is unchanged by a change of origin or of scale |
| Rank correlation | $R = 1-\frac{6\sum d^{2}}{n(n^{2}-1)}$ |
| Signs | $b_{yx}$, $b_{xy}$ and $r$ always share one sign |
| To predict $y$ from $x$ | use the $y$-on-$x$ line only |
| To predict $x$ from $y$ | use the $x$-on-$y$ line only |

```figure caption="Both regression lines for the 2082 supply–price data. They cross at $(\bar{x},\bar{y})$ but they are different lines: the $y$-on-$x$ line minimises vertical gaps, the $x$-on-$y$ line minimises horizontal gaps. Use $y$-on-$x$ to predict a price, $x$-on-$y$ to predict a supply."
import numpy as np
X = np.array([45.0, 50, 56, 62, 65, 70]); Y = np.array([65.0, 70, 75, 80, 90, 100])
mx, my = X.mean(), Y.mean()
byx = ((X-mx)*(Y-my)).sum()/((X-mx)**2).sum()
bxy = ((X-mx)*(Y-my)).sum()/((Y-my)**2).sum()
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.scatter(X, Y, s=26, color=INK, zorder=4, label="data")
xs = np.linspace(41, 74, 50)
ax.plot(xs, my + byx*(xs-mx), color=ACCENT, lw=1.7, label="y on x")
ys = np.linspace(61, 104, 50)
ax.plot(mx + bxy*(ys-my), ys, color=SERIES[1], lw=1.7, ls="--", label="x on y")
ax.plot([mx], [my], "o", ms=7, mfc="white", mec=SERIES[2], mew=1.8, zorder=5)
ax.annotate("(x̄, ȳ) = (58, 80)", (mx, my), xytext=(-72, 26),
            textcoords="offset points", fontsize=8.4, color=SERIES[2],
            arrowprops=dict(arrowstyle="->", lw=0.9, color=SERIES[2]))
ax.set_xlabel("supply X"); ax.set_ylabel("price Y (Rs)")
ax.set_xlim(40, 76); ax.set_ylim(58, 108)
ax.grid(True, lw=0.6, color=GRID)
ax.spines[['top','right']].set_visible(False)
ax.legend(loc="lower right", fontsize=8.2)
```

**Multiple choice questions**

1. The range of the correlation coefficient $r$ is <span class="marks">[1]</span>
   (a) $0 \leq r \leq 1$ (b) $-1 \leq r \leq 1$ (c) $-1 < r < 1$ (d) $0 < r < 1$
2. If $b_{yx} = 0.22$ and $b_{xy} = 0.616$, the correlation coefficient is approximately <span class="marks">[1]</span>
   (a) $0.14$ (b) $0.37$ (c) $0.42$ (d) $0.84$
3. The two regression lines always intersect at <span class="marks">[1]</span>
   (a) the origin (b) $(\bar{x},\ \bar{y})$ (c) $(0,\ \bar{y})$ (d) $(\bar{x},\ 0)$
4. If $r=0$, the two variables are <span class="marks">[1]</span>
   (a) perfectly correlated (b) uncorrelated (linearly) (c) inversely proportional (d) identical
5. If $b_{yx}\cdot b_{xy} = 1$, then the two regression lines <span class="marks">[1]</span>
   (a) are perpendicular (b) coincide (c) are parallel but distinct (d) do not exist
6. The correlation coefficient is unchanged by <span class="marks">[1]</span>
   (a) a change of origin only (b) a change of scale only (c) a change of origin and of scale (d) neither
7. Spearman's rank correlation coefficient is <span class="marks">[1]</span>
   (a) $1-\frac{6\sum d^{2}}{n(n^{2}-1)}$ (b) $1-\frac{6\sum d}{n(n^{2}-1)}$ (c) $\frac{6\sum d^{2}}{n(n^{2}-1)}$ (d) $1-\frac{\sum d^{2}}{6n(n^{2}-1)}$
8. If $\sum d^{2}=30$ and $n=10$, the rank correlation coefficient is <span class="marks">[1]</span>
   (a) $0.18$ (b) $0.62$ (c) $0.82$ (d) $0.91$
9. The regression coefficient of $y$ on $x$ is <span class="marks">[1]</span>
   (a) $r\frac{\sigma_x}{\sigma_y}$ (b) $r\frac{\sigma_y}{\sigma_x}$ (c) $\frac{\sigma_y}{r\sigma_x}$ (d) $r\sigma_x\sigma_y$
10. If $r=0.8$, $\sigma_x=3$ and $\sigma_y=4$, then $b_{yx}$ equals <span class="marks">[1]</span>
    (a) $0.6$ (b) $1.07$ (c) $9.6$ (d) $0.94$
11. The two regression lines are perpendicular to each other when <span class="marks">[1]</span>
    (a) $r=1$ (b) $r=-1$ (c) $r=0$ (d) $r=0.5$
12. If the regression line of $y$ on $x$ is $y=2x+3$ and $\bar{x}=1$, then $\bar{y}$ is <span class="marks">[1]</span>
    (a) $2$ (b) $3$ (c) $5$ (d) $6$

::: note Answer key — 11.10
**1.** (b) — $r$ is a cosine-like ratio; both endpoints are attainable (perfect positive and perfect negative correlation).
**2.** (b) — $r = \sqrt{0.22\times0.616} = \sqrt{0.13555} = 0.3682$. Machine-checked; these are the 2079 Group B numbers.
**3.** (b) — both lines are written as deviations from the means, so both pass through $(\bar{x},\bar{y})$.
**4.** (b) — $r$ measures **linear** association only; $r=0$ rules out a straight-line trend, not every relationship.
**5.** (b) — $b_{yx}b_{xy}=r^{2}=1$ means $r=\pm1$, perfect linear correlation, and the two lines become one.
**6.** (c) — $r$ is a pure number, invariant under $x \rightarrow \frac{x-A}{h}$ and $y \rightarrow \frac{y-B}{k}$ for $h,k>0$.
**7.** (a) — the standard formula; note the $6$ multiplies $\sum d^{2}$.
**8.** (c) — $1-\frac{6(30)}{10(99)} = 1-\frac{180}{990} = 0.818$.
**9.** (b) — $b_{yx}$ scales $r$ by $\frac{\sigma_y}{\sigma_x}$: the *dependent* variable's spread goes on top.
**10.** (b) — $0.8\times\frac{4}{3} = 1.0667 \approx 1.07$.
**11.** (c) — no linear relation makes one line horizontal and the other vertical.
**12.** (c) — the $y$-on-$x$ line passes through $(\bar{x},\bar{y})$, so $\bar{y} = 2(1)+3 = 5$.
:::

::: caution Distractor analysis — Correlation and Regression
**Predicting with the wrong line.** The 2081 Group B item asked for the likely
**price** $y$ when the supply $x$ is $120$: that needs the $y$-on-$x$ line. The 2082
item asked for the **supply** $x$ when the price is Rs $150$: that needs the
$x$-on-$y$ line. Using one line for both questions is the most expensive mistake in
this unit, and the figure above shows why — the two lines are genuinely different.

**Inverting $\frac{\sigma_y}{\sigma_x}$ in the regression coefficient.** Option (a)
in Q9 is $b_{xy}$ offered as $b_{yx}$. Remember it by the subscript order:
$b_{yx}$ predicts $y$, so $\sigma_y$ goes on top.

**Forgetting to take the square root.** In Q2 the distractor $0.14$ is the *product*
$b_{yx}b_{xy} = r^{2}$. The correlation coefficient is its square root.

**Losing the sign of $r$.** $r = \pm\sqrt{b_{yx}b_{xy}}$ gives only the magnitude;
the sign is copied from either regression coefficient. If $b_{yx}$ is negative, $r$
is negative — the square root never tells you that.

**Treating $r=0$ as "no relationship at all".** $r=0$ only says there is no
*straight-line* trend. A perfect parabola through the data can still give $r=0$.
:::

## 11.11 Probability

The most reliable MCQ slot in the whole paper. **Conditional probability $P(B/A)$
was the Statistics & Probability MCQ in 2080, 2081 and 2082, and in the CDC model
question.** Four for four. Learn one formula properly and this mark is yours.

| Result | Formula / condition |
|---|---|
| Range of a probability | $0 \leq P(A) \leq 1$ |
| Complement | $P(A') = 1-P(A)$ |
| Addition rule | $P(A \cup B) = P(A)+P(B)-P(A \cap B)$ |
| Mutually exclusive | $P(A \cap B)=0$, so $P(A\cup B)=P(A)+P(B)$ |
| **Conditional probability** | $P(B/A) = \frac{P(A \cap B)}{P(A)}$, needs $P(A)>0$ |
| The other conditional | $P(A/B) = \frac{P(A \cap B)}{P(B)}$ |
| Multiplication rule, dependent | $P(A \cap B) = P(A)\cdot P(B/A)$ |
| Independent events | $P(A \cap B) = P(A)\cdot P(B)$, and then $P(B/A)=P(B)$ |
| Drawing without replacement | dependent: the second denominator drops by one |
| Drawing with replacement | independent: the denominator is unchanged |
| Certain / impossible event | $P=1$ / $P=0$ |
| Exhaustive events | probabilities add to $1$ |

**Multiple choice questions**

1. The range of the probability of any event $A$ is (NEB 2079) <span class="marks">[1]</span>
   (a) $0 \leq P(A) \leq 1$ (b) $0 \leq P(A) < 1$ (c) $-1 \leq P(A) \leq 1$ (d) $0 < P(A) < 1$
2. Consider $A$ and $B$ to be two dependent events. If $P(A)=\frac{1}{2}$, $P(B)=\frac{1}{13}$ and $P(A\cap B)=\frac{1}{26}$, what is $P(B/A)$? (NEB 2080) <span class="marks">[1]</span>
   (a) $\frac{1}{52}$ (b) $\frac{1}{26}$ (c) $\frac{1}{13}$ (d) $\frac{1}{2}$
3. Let $A$ and $B$ be two dependent events with $P(A\cap B)=\frac{1}{18}$, $P(B)=\frac{1}{18}$ and $2P(A)=5P(B)$. What is the value of $P(B/A)$? (NEB 2081) <span class="marks">[1]</span>
   (a) $\frac{1}{324}$ (b) $\frac{1}{18}$ (c) $\frac{5}{36}$ (d) $\frac{2}{5}$
4. If $P(A)=\frac{1}{3}$, $P(B)=\frac{2}{3}$ and $P(A\cap B)=\frac{1}{5}$, which one of the following is $P(B/A)$? (NEB 2082) <span class="marks">[1]</span>
   (a) $\frac{3}{5}$ (b) $\frac{2}{5}$ (c) $\frac{2}{15}$ (d) $\frac{1}{15}$
5. The probability that a leap year chosen at random contains $53$ Fridays or $53$ Saturdays is (CDC model 2080) <span class="marks">[1]</span>
   (a) $\frac{2}{7}$ (b) $\frac{3}{7}$ (c) $\frac{4}{7}$ (d) $\frac{1}{7}$
6. If $A$ and $B$ are independent with $P(A)=\frac{1}{2}$ and $P(B)=\frac{1}{3}$, then $P(A\cap B)$ is <span class="marks">[1]</span>
   (a) $\frac{1}{6}$ (b) $\frac{5}{6}$ (c) $\frac{2}{3}$ (d) $\frac{1}{5}$
7. $P(A/B)$ is defined as <span class="marks">[1]</span>
   (a) $\frac{P(A\cap B)}{P(A)}$ (b) $\frac{P(A\cap B)}{P(B)}$ (c) $\frac{P(A)}{P(B)}$ (d) $P(A)\cdot P(B)$
8. If $A$ and $B$ are mutually exclusive, then $P(A\cap B)$ is <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $P(A)P(B)$ (d) $P(A)+P(B)$
9. Two cards are drawn one after another, without replacement, from a well-shuffled pack of $52$. The probability that both are aces is <span class="marks">[1]</span>
   (a) $\frac{1}{169}$ (b) $\frac{1}{221}$ (c) $\frac{1}{13}$ (d) $\frac{4}{663}$
10. If $P(A)=0.3$, then $P(A')$ is <span class="marks">[1]</span>
    (a) $0.3$ (b) $0.7$ (c) $1.3$ (d) $-0.3$

::: note Answer key — 11.11
**1.** (a) — an impossible event has probability exactly $0$ and a certain event exactly $1$, so the interval is closed.
**2.** (c) — $P(B/A)=\frac{1/26}{1/2}=\frac{2}{26}=\frac{1}{13}$.
**3.** (d) — $P(A)=\frac{5}{2}P(B)=\frac{5}{2}\cdot\frac{1}{18}=\frac{5}{36}$, so $P(B/A)=\frac{1/18}{5/36}=\frac{36}{90}=\frac{2}{5}$.
**4.** (a) — $P(B/A)=\frac{1/5}{1/3}=\frac{3}{5}$.
**5.** (b) — a leap year is $52$ weeks plus $2$ extra consecutive days; there are $7$ equally likely such pairs, and three of them (Thu–Fri, Fri–Sat, Sat–Sun) contain a Friday or a Saturday, giving $\frac{3}{7}$.
**6.** (a) — independence gives $P(A\cap B)=\frac{1}{2}\times\frac{1}{3}=\frac{1}{6}$.
**7.** (b) — divide by the probability of the event that is **given**, which here is $B$.
**8.** (a) — mutually exclusive events cannot both happen.
**9.** (b) — $\frac{4}{52}\times\frac{3}{51} = \frac{12}{2652} = \frac{1}{221}$.
**10.** (b) — $1-0.3=0.7$.
:::

::: caution Distractor analysis — Probability
**Computing $P(B/A)$ as $\frac{P(A\cap B)}{P(B)}$.** This is *the* trap, and it has
been set four times running — 2080, 2081, 2082 and the CDC model. The rule is:
**divide by the probability of whatever comes after the slash.** For $P(B/A)$ that
is $P(A)$. Look at the 2080 item: $\frac{1/26}{1/13} = \frac{1}{2}$ is option (d),
which is wrong; $\frac{1/26}{1/2} = \frac{1}{13}$ is option (c), which is right. In
the 2082 item the wrong division gives $\frac{3}{10}$ and the right one $\frac{3}{5}$.

**Multiplying instead of dividing.** In the 2082 item, option (c) $\frac{2}{15}$ is
$P(A)\times\frac{2}{5}$-flavoured arithmetic, and option (d) $\frac{1}{15}$ is
$P(A)\cdot P(A\cap B)$. Conditional probability is a *division*.

**Missing an intermediate quantity.** In the 2081 item, $P(A)$ is not given
directly — it must be extracted from $2P(A)=5P(B)$ first. The distractor
$\frac{5}{36}$ is $P(A)$ itself, i.e. the answer to the sub-step offered as the
answer to the question.

**Treating "without replacement" as independent.** In Q9 the distractor
$\frac{1}{169}$ is $\left(\frac{4}{52}\right)^{2}$, which is the *with*-replacement
answer. Without replacement, both the numerator and the denominator drop by one.

**Reading "or" as "and" in a compound event.** In the leap-year item, $\frac{2}{7}$
is the probability of $53$ Fridays alone. The union needs the three pairs counted
once each — Friday–Saturday must not be double-counted.
:::

## 11.12 Derivatives

Calculus carries 22 marks and **four** of the eleven MCQs — more than any other
area. Two of those four, on the evidence of all four papers, come from this unit:
an inverse-hyperbolic or hyperbolic derivative, and either an L'Hospital limit or a
tangent/normal slope. The table below is the single highest-value thing to
memorise in this chapter.

| Function | Derivative | Valid for |
|---|---|---|
| $\sinh x$ | $\cosh x$ | all $x$ |
| $\cosh x$ | $\sinh x$ | all $x$ |
| $\tanh x$ | $\mathrm{sech}^{2}x$ | all $x$ |
| $\coth x$ | $-\mathrm{cosech}^{2}x$ | $x \ne 0$ |
| $\mathrm{sech}\,x$ | $-\mathrm{sech}\,x\tanh x$ | all $x$ |
| $\mathrm{cosech}\,x$ | $-\mathrm{cosech}\,x\coth x$ | $x \ne 0$ |
| $\sinh^{-1}x$ | $\frac{1}{\sqrt{x^{2}+1}}$ | all $x$ |
| $\cosh^{-1}x$ | $\frac{1}{\sqrt{x^{2}-1}}$ | $x>1$ |
| $\tanh^{-1}x$ | $\frac{1}{1-x^{2}}$ | $|x|<1$ |
| $\coth^{-1}x$ | $\frac{1}{1-x^{2}}$ | $|x|>1$ |
| $\mathrm{sech}^{-1}x$ | $\frac{-1}{x\sqrt{1-x^{2}}}$ | $0<x<1$ |
| $\mathrm{cosech}^{-1}x$ | $\frac{-1}{|x|\sqrt{1+x^{2}}}$ | $x \ne 0$ |

The rest of the unit's MCQ surface is limits and tangents:

| Result | Statement | Condition |
|---|---|---|
| L'Hospital's rule | $\lim\frac{f}{g} = \lim\frac{f'}{g'}$ | only for $\frac{0}{0}$ or $\frac{\infty}{\infty}$ |
| Slope of tangent at $(x_1,y_1)$ | $m = \left.\frac{dy}{dx}\right|_{(x_1,y_1)}$ | |
| Slope of normal | $-\frac{1}{m}$ | $m \ne 0$ |
| Tangent parallel to the $x$-axis | $\frac{dy}{dx}=0$ | |
| Tangent parallel to the $y$-axis | $\frac{dx}{dy}=0$, i.e. $\frac{dy}{dx}$ is infinite | |
| Differential | $dy = f'(x)\,dx$ | |
| Rate measure | $\frac{dA}{dt} = \frac{dA}{dr}\cdot\frac{dr}{dt}$ | chain rule |

**Multiple choice questions**

1. What is the derivative of $y = 2\sinh\frac{x}{2}$ with respect to $x$? (NEB 2080) <span class="marks">[1]</span>
   (a) $\cosh\frac{x}{2}$ (b) $2\cosh\frac{x}{2}$ (c) $\cosh\frac{x}{4}$ (d) $2\cosh\frac{x}{4}$
2. It is given that $f'(x)=3x^{2}$ and $g'(x)=2x$. What is the value of $\lim_{x\to1}\frac{f(x)}{g(x)}$ by L'Hospital's rule? (NEB 2081) <span class="marks">[1]</span>
   (a) $\frac{3}{2}$ (b) $\frac{1}{3}$ (c) $\frac{1}{2}$ (d) $\frac{1}{6}$
3. Which one of the following is the slope of the normal to the curve $y=3x^{2}-x$ at the point where $x=-1$? (NEB 2082) <span class="marks">[1]</span>
   (a) $-7$ (b) $-5$ (c) $\frac{1}{7}$ (d) $\frac{1}{5}$
4. The tangents to the curve $y=x^{3}$ at $x=2$ and $x=-2$ are (NEB 2079) <span class="marks">[1]</span>
   (a) parallel (b) perpendicular (c) intersecting (d) non-existent
5. The volume of a sphere is increasing at $25$ cm³/sec. At what rate is the radius increasing at the instant when the total surface area is $10\pi$ cm²? (CDC model 2080) <span class="marks">[1]</span>
   (a) $\frac{5}{2\pi}$ cm/sec (b) $\frac{2\pi}{5}$ cm/sec (c) $\frac{5}{\pi}$ cm/sec (d) $\frac{25}{4\pi}$ cm/sec
6. $\frac{d}{dx}(\sinh x)$ equals <span class="marks">[1]</span>
   (a) $\cosh x$ (b) $-\cosh x$ (c) $\mathrm{sech}^{2}x$ (d) $\cos x$
7. $\frac{d}{dx}\left(\cosh^{-1}x\right)$ equals <span class="marks">[1]</span>
   (a) $\frac{1}{\sqrt{1-x^{2}}}$ (b) $\frac{1}{\sqrt{x^{2}-1}}$ (c) $\frac{1}{\sqrt{x^{2}+1}}$ (d) $\frac{-1}{\sqrt{x^{2}-1}}$
8. $\frac{d}{dx}\left(\tanh^{-1}x\right)$ equals <span class="marks">[1]</span>
   (a) $\frac{1}{1+x^{2}}$ (b) $\frac{1}{1-x^{2}}$ (c) $\frac{1}{x^{2}-1}$ (d) $\mathrm{sech}^{2}x$
9. $\frac{d}{dx}\left(\mathrm{sech}^{-1}x\right) = \frac{-1}{x\sqrt{1-x^{2}}}$ holds under the condition <span class="marks">[1]</span>
   (a) $x>1$ (b) $0<x<1$ (c) $x<0$ (d) all real $x$
10. $\frac{d}{dx}\left(\mathrm{cosech}^{-1}x\right)$ equals <span class="marks">[1]</span>
    (a) $\frac{-1}{|x|\sqrt{1+x^{2}}}$ (b) $\frac{1}{|x|\sqrt{1+x^{2}}}$ (c) $\frac{-1}{x\sqrt{1-x^{2}}}$ (d) $\frac{1}{\sqrt{x^{2}+1}}$
11. $\lim_{x\to0}\frac{\sin x}{x}$ equals <span class="marks">[1]</span>
    (a) $0$ (b) $1$ (c) $\infty$ (d) undefined
12. $\lim_{x\to0}\frac{e^{x}-1}{x}$ equals <span class="marks">[1]</span>
    (a) $0$ (b) $1$ (c) $e$ (d) $\infty$
13. The slope of the tangent to $y=x^{2}-3x$ at $x=2$ is <span class="marks">[1]</span>
    (a) $-2$ (b) $1$ (c) $2$ (d) $4$
14. The slope of the tangent to $y=2x^{3}+x^{2}-7x-2$ at $x=2$ is <span class="marks">[1]</span>
    (a) $5$ (b) $13$ (c) $21$ (d) $28$
15. A tangent to a curve is parallel to the $x$-axis where <span class="marks">[1]</span>
    (a) $\frac{dy}{dx}=0$ (b) $\frac{dy}{dx}=1$ (c) $\frac{dx}{dy}=0$ (d) $\frac{d^{2}y}{dx^{2}}=0$
16. A tangent to the curve $y=f(x)$ is parallel to the $y$-axis where <span class="marks">[1]</span>
    (a) $\frac{dy}{dx}=0$ (b) $\frac{dy}{dx}=1$ (c) $\frac{dx}{dy}=0$ (d) $f(x)=0$
17. The differential $dy$ of $y=f(x)$ is <span class="marks">[1]</span>
    (a) $f'(x)$ (b) $f'(x)\,dx$ (c) $\frac{dx}{f'(x)}$ (d) $f(x)\,dx$
18. The rate of change of the area of a circle with respect to its radius, at $r=3$, is <span class="marks">[1]</span>
    (a) $3\pi$ (b) $6\pi$ (c) $9\pi$ (d) $12\pi$
19. $\lim_{x\to\infty}\frac{\ln(2x^{2}+5)}{\ln(3x^{3}-4)}$ equals <span class="marks">[1]</span>
    (a) $\frac{2}{3}$ (b) $\frac{3}{2}$ (c) $0$ (d) $1$
20. The rate of change of the volume of a sphere with respect to its surface area, when the radius is $7$ cm, is <span class="marks">[1]</span>
    (a) $\frac{7}{2}$ (b) $7$ (c) $14$ (d) $\frac{1}{14}$

::: note Answer key — 11.12
**1.** (a) — $\frac{d}{dx}\left(2\sinh\frac{x}{2}\right) = 2\cosh\frac{x}{2}\cdot\frac{1}{2} = \cosh\frac{x}{2}$. The chain-rule factor $\frac{1}{2}$ cancels the $2$ outside.
**2.** (a) — L'Hospital's rule replaces the ratio by $\frac{f'(1)}{g'(1)} = \frac{3}{2}$.
**3.** (c) — $\frac{dy}{dx}=6x-1$, so at $x=-1$ the tangent slope is $-7$ and the normal slope is $-\frac{1}{-7}=\frac{1}{7}$. (The paper prints the point as $(-1,1)$, but $y(-1)=4$; the $x$-value is what the slope depends on, so the answer is unaffected.)
**4.** (a) — $\frac{dy}{dx}=3x^{2}$ takes the value $12$ at both $x=2$ and $x=-2$: equal slopes, so parallel.
**5.** (a) — $S=4\pi r^{2}=10\pi$ gives $r^{2}=2.5$; then $\frac{dV}{dt}=4\pi r^{2}\frac{dr}{dt}=25$ gives $\frac{dr}{dt}=\frac{25}{10\pi}=\frac{5}{2\pi}$ cm/sec.
**6.** (a) — no minus sign here; the minus appears for $\frac{d}{dx}(\cos x)$, not $\frac{d}{dx}(\cosh x)$.
**7.** (b) — $\frac{1}{\sqrt{x^{2}-1}}$; (a) is $\frac{d}{dx}(\sin^{-1}x)$ and (c) is $\frac{d}{dx}(\sinh^{-1}x)$.
**8.** (b) — $\frac{1}{1-x^{2}}$ for $|x|<1$; (a) is $\frac{d}{dx}(\tan^{-1}x)$.
**9.** (b) — the $\sqrt{1-x^{2}}$ needs $|x|<1$ and the $\mathrm{sech}^{-1}$ branch used in NEB work is $0<x<1$. This is the 2081 Group B item 17b, worth 1 mark for exactly this condition.
**10.** (a) — machine-checked: $\frac{d}{dx}\mathrm{cosech}^{-1}x = \frac{-1}{|x|\sqrt{1+x^{2}}}$.
**11.** (b) — $\frac{0}{0}$ form; differentiate to get $\frac{\cos x}{1} \to 1$.
**12.** (b) — $\frac{0}{0}$ form; differentiate to get $\frac{e^{x}}{1} \to 1$.
**13.** (b) — $\frac{dy}{dx}=2x-3 = 4-3 = 1$.
**14.** (c) — $\frac{dy}{dx}=6x^{2}+2x-7 = 24+4-7 = 21$.
**15.** (a) — a horizontal tangent has zero slope.
**16.** (c) — a vertical tangent has infinite $\frac{dy}{dx}$, which is the same as $\frac{dx}{dy}=0$. This was worth 1 mark in 2082 Group B item 17c.
**17.** (b) — the differential is the derivative times the increment in $x$.
**18.** (b) — $A=\pi r^{2}$, so $\frac{dA}{dr}=2\pi r = 6\pi$.
**19.** (a) — by L'Hospital's rule the limit is $\lim\frac{4x/(2x^{2}+5)}{9x^{2}/(3x^{3}-4)}$, which tends to $\frac{2}{3}$; more quickly, the ratio of the leading powers' logarithms is $\frac{2}{3}$. Machine-checked.
**20.** (a) — $\frac{dV}{dS}=\frac{dV/dr}{dS/dr}=\frac{4\pi r^{2}}{8\pi r}=\frac{r}{2}=\frac{7}{2}$.
:::

::: caution Distractor analysis — Derivatives
**Circular versus hyperbolic derivatives.** $\frac{d}{dx}(\cos x)=-\sin x$ but
$\frac{d}{dx}(\cosh x)=+\sinh x$. **The hyperbolic pair has no minus sign; the
circular pair does.** The minus signs in the hyperbolic family belong to $\coth$,
$\mathrm{sech}$, $\mathrm{cosech}$ and to the two inverse functions
$\mathrm{sech}^{-1}$, $\mathrm{cosech}^{-1}$ — nowhere else.

**Inverse circular versus inverse hyperbolic.** The three most-confused pairs are
$\frac{1}{\sqrt{1-x^{2}}}$ (for $\sin^{-1}$) against $\frac{1}{\sqrt{x^{2}+1}}$ (for
$\sinh^{-1}$); $\frac{1}{1+x^{2}}$ (for $\tan^{-1}$) against $\frac{1}{1-x^{2}}$
(for $\tanh^{-1}$); and $\frac{1}{\sqrt{x^{2}-1}}$ (for $\cosh^{-1}$), which has no
circular twin at all. Questions 7, 8 and 10 above offer the wrong twin as a
distractor every time.

**Forgetting the chain-rule factor — or double-counting it.** The 2080 MCQ 8 is
built on this. $y=2\sinh\frac{x}{2}$ differentiates to $\cosh\frac{x}{2}$, because
$2\times\frac{1}{2}=1$. Option (b) keeps the outside $2$ and forgets the inside
$\frac{1}{2}$; option (d) halves the argument twice.

**Quoting the tangent slope when the normal slope was asked for.** The 2082 MCQ 7
offers $-7$ as option (a) — the correct *tangent* slope — and $\frac{1}{7}$ as
option (c), the normal slope that was asked for. Underline the word "normal" in the
stem before you compute anything.

**Using L'Hospital's rule where it does not apply.** The rule is only valid for
$\frac{0}{0}$ and $\frac{\infty}{\infty}$. Substituting first to check the form is
compulsory; the 2080 Group C item made candidates state the relation for the
$\frac{0}{0}$ case before using it.

**Differentiating with respect to the wrong variable.** In question 20 the question
asks for $\frac{dV}{dS}$, not $\frac{dV}{dr}$. The distractor $14$ is $2r$, i.e.
$\frac{dS}{dr}$ over $4\pi$ — a derivative taken with respect to the radius when
the surface area was wanted. Write down what the numerator and denominator are
before you differentiate anything.
:::

## 11.13 Anti-derivatives

The other reliable Calculus MCQ. An integral has been the subject of an MCQ in
2080, 2081 and 2082, and all three times it was the **same shape of question**: a
standard integral of the form $\int\frac{dx}{\text{quadratic}}$, with the four
options differing only in a constant or in an inverted argument. That is a
memory test, not a calculation, and the table below is the whole answer.

| Integral | Result |
|---|---|
| $\int x^{n}dx$ | $\frac{x^{n+1}}{n+1}+C$, $n \ne -1$ |
| $\int\frac{dx}{x}$ | $\log|x|+C$ |
| $\int e^{x}dx$ | $e^{x}+C$ |
| $\int a^{x}dx$ | $\frac{a^{x}}{\log a}+C$ |
| $\int\sin x\,dx$ | $-\cos x + C$ |
| $\int\cos x\,dx$ | $\sin x + C$ |
| $\int\tan x\,dx$ | $\log|\sec x|+C$ |
| $\int\sec x\,dx$ | $\log|\sec x+\tan x|+C$ |
| $\int\sinh x\,dx$ | $\cosh x + C$ |
| $\int\frac{dx}{x^{2}+a^{2}}$ | $\frac{1}{a}\tan^{-1}\frac{x}{a}+C$ |
| $\int\frac{dx}{x^{2}-a^{2}}$ | $\frac{1}{2a}\log\left|\frac{x-a}{x+a}\right|+C$ |
| $\int\frac{dx}{a^{2}-x^{2}}$ | $\frac{1}{2a}\log\left|\frac{a+x}{a-x}\right|+C$ |
| $\int\frac{dx}{\sqrt{a^{2}-x^{2}}}$ | $\sin^{-1}\frac{x}{a}+C$ |
| $\int\frac{dx}{\sqrt{x^{2}+a^{2}}}$ | $\log\left|x+\sqrt{x^{2}+a^{2}}\right|+C = \sinh^{-1}\frac{x}{a}+C$ |
| $\int\frac{dx}{\sqrt{x^{2}-a^{2}}}$ | $\log\left|x+\sqrt{x^{2}-a^{2}}\right|+C = \cosh^{-1}\frac{x}{a}+C$ |
| $\int\frac{f'(x)}{f(x)}dx$ | $\log|f(x)|+C$ |

Two supporting facts for the partial-fraction questions:

| Term | Meaning |
|---|---|
| Proper rational fraction | degree of numerator $<$ degree of denominator |
| Partial fractions | one fraction per distinct linear factor |

**Multiple choice questions**

1. Which one of the following is the result of $\int\frac{dx}{x^{2}+4}$? (NEB 2081) <span class="marks">[1]</span>
   (a) $\frac{1}{2}\tan^{-1}\frac{2}{x}+C$ (b) $\frac{1}{2}\tan^{-1}\frac{x}{2}+C$ (c) $2\tan^{-1}\frac{x}{2}+C$ (d) $\tan^{-1}\frac{x}{2}+C$
2. What is the integral of $\int\frac{dx}{9x^{2}+1}$? (NEB 2082) <span class="marks">[1]</span>
   (a) $\frac{1}{3}\tan^{-1}(3x)+C$ (b) $\frac{1}{27}\tan^{-1}(3x)+C$ (c) $\frac{1}{27}\tan^{-1}\frac{x}{3}+C$ (d) $\frac{1}{27}\tan^{-1}\frac{3}{x}+C$
3. Which of the following is the value of $\int\frac{dx}{x^{2}-1}$? (NEB 2080) <span class="marks">[1]</span>
   (a) $2\log\frac{x+1}{x-1}+C$ (b) $2\log\frac{x-1}{x+1}+C$ (c) $\log\frac{x-1}{x+1}+C$ (d) $\frac{1}{2}\log\frac{x+1}{x-1}+C$
4. $\int\frac{dx}{\sqrt{1-x^{2}}}$ equals <span class="marks">[1]</span>
   (a) $\sin^{-1}x+C$ (b) $\cos^{-1}x+C$ (c) $\tan^{-1}x+C$ (d) $\sinh^{-1}x+C$
5. $\int\frac{dx}{\sqrt{x^{2}-a^{2}}}$ equals <span class="marks">[1]</span>
   (a) $\sin^{-1}\frac{x}{a}+C$ (b) $\log\left|x+\sqrt{x^{2}-a^{2}}\right|+C$ (c) $\frac{1}{a}\tan^{-1}\frac{x}{a}+C$ (d) $\frac{1}{2a}\log\left|\frac{x-a}{x+a}\right|+C$
6. $\int\tan x\,dx$ equals <span class="marks">[1]</span>
   (a) $\sec^{2}x+C$ (b) $\log|\sec x|+C$ (c) $\log|\cos x|+C$ (d) $\log|\tan x|+C$
7. $\int\sec x\,dx$ equals <span class="marks">[1]</span>
   (a) $\sec x\tan x+C$ (b) $\log|\sec x|+C$ (c) $\log|\sec x+\tan x|+C$ (d) $\tan x + C$
8. $\int x^{3}dx$ equals <span class="marks">[1]</span>
   (a) $3x^{2}+C$ (b) $\frac{x^{4}}{4}+C$ (c) $\frac{x^{2}}{2}+C$ (d) $4x^{4}+C$
9. $\int e^{2x}dx$ equals <span class="marks">[1]</span>
   (a) $2e^{2x}+C$ (b) $\frac{e^{2x}}{2}+C$ (c) $e^{2x}+C$ (d) $\frac{e^{3x}}{3}+C$
10. $\int\frac{dx}{x^{2}-9}$ equals <span class="marks">[1]</span>
    (a) $\frac{1}{3}\log\left|\frac{x-3}{x+3}\right|+C$ (b) $\frac{1}{6}\log\left|\frac{x-3}{x+3}\right|+C$ (c) $\frac{1}{6}\log\left|\frac{x+3}{x-3}\right|+C$ (d) $\frac{1}{3}\tan^{-1}\frac{x}{3}+C$
11. $\int\frac{dx}{4-x^{2}}$ equals <span class="marks">[1]</span>
    (a) $\frac{1}{4}\log\left|\frac{2+x}{2-x}\right|+C$ (b) $\frac{1}{4}\log\left|\frac{x-2}{x+2}\right|+C$ (c) $\frac{1}{2}\log\left|\frac{2+x}{2-x}\right|+C$ (d) $\sin^{-1}\frac{x}{2}+C$
12. $\int\frac{dx}{x^{2}+2x+2}$ equals <span class="marks">[1]</span>
    (a) $\tan^{-1}(x+1)+C$ (b) $\frac{1}{2}\tan^{-1}(x+1)+C$ (c) $\log|x^{2}+2x+2|+C$ (d) $\tan^{-1}(x+2)+C$
13. $\int\frac{2x+1}{x^{2}+x+1}dx$ equals <span class="marks">[1]</span>
    (a) $\log|2x+1|+C$ (b) $\log|x^{2}+x+1|+C$ (c) $\frac{1}{2}\log|x^{2}+x+1|+C$ (d) $\tan^{-1}(2x+1)+C$
14. $\int\frac{dx}{x(x+1)}$ equals <span class="marks">[1]</span>
    (a) $\log\left|\frac{x}{x+1}\right|+C$ (b) $\log\left|\frac{x+1}{x}\right|+C$ (c) $\log|x(x+1)|+C$ (d) $\frac{1}{2}\log\left|\frac{x}{x+1}\right|+C$
15. A rational fraction $\frac{p(x)}{q(x)}$ is called **proper** when <span class="marks">[1]</span>
    (a) $\deg p < \deg q$ (b) $\deg p > \deg q$ (c) $\deg p = \deg q$ (d) $q(x)$ is linear
16. $\int\sinh x\,dx$ equals <span class="marks">[1]</span>
    (a) $\cosh x+C$ (b) $-\cosh x+C$ (c) $\mathrm{sech}^{2}x+C$ (d) $\sinh x+C$
17. The number of partial fractions needed for $\frac{1}{x(x-1)(x+2)}$ is <span class="marks">[1]</span>
    (a) $1$ (b) $2$ (c) $3$ (d) $4$
18. $\int a^{x}dx$ equals <span class="marks">[1]</span>
    (a) $a^{x}+C$ (b) $\frac{a^{x}}{\log a}+C$ (c) $a^{x}\log a+C$ (d) $\frac{a^{x+1}}{x+1}+C$

::: note Answer key — 11.13
**1.** (b) — $\int\frac{dx}{x^{2}+a^{2}}=\frac{1}{a}\tan^{-1}\frac{x}{a}$ with $a=2$, giving $\frac{1}{2}\tan^{-1}\frac{x}{2}$. Machine-checked.
**2.** (a) — take out the $9$: $\frac{1}{9}\int\frac{dx}{x^{2}+\frac{1}{9}} = \frac{1}{9}\cdot\frac{1}{1/3}\tan^{-1}(3x) = \frac{1}{3}\tan^{-1}(3x)$. Machine-checked.
**3.** **No printed option is exactly right.** The correct value is $\frac{1}{2}\log\left|\frac{x-1}{x+1}\right|+C$. Option (b) has the correct ratio $\frac{x-1}{x+1}$ with the constant $2$ in place of $\frac{1}{2}$; option (d) has the correct constant with the ratio inverted, which changes the sign of the whole answer. (b) is the closer of the two, and is the option a marker would have keyed. We machine-checked the integral.
**4.** (a) — $\sin^{-1}x+C$; note $\cos^{-1}x$ differentiates to $\frac{-1}{\sqrt{1-x^{2}}}$, the wrong sign.
**5.** (b) — this is $\cosh^{-1}\frac{x}{a}$, usually written in the logarithmic form.
**6.** (b) — $\int\frac{\sin x}{\cos x}dx = -\log|\cos x| = \log|\sec x|$.
**7.** (c) — the standard result; (b) is $\int\tan x\,dx$.
**8.** (b) — raise the index by one and divide by the new index.
**9.** (b) — divide by the coefficient of $x$ in the exponent.
**10.** (b) — $\frac{1}{2a}\log\left|\frac{x-a}{x+a}\right|$ with $a=3$, so $\frac{1}{6}$. Machine-checked.
**11.** (a) — $\frac{1}{2a}\log\left|\frac{a+x}{a-x}\right|$ with $a=2$, so $\frac{1}{4}\log\left|\frac{2+x}{2-x}\right|$. Machine-checked.
**12.** (a) — complete the square: $\int\frac{dx}{(x+1)^{2}+1} = \tan^{-1}(x+1)$. Machine-checked.
**13.** (b) — the numerator is exactly the derivative of the denominator, so the integral is $\log|f(x)|$.
**14.** (a) — $\frac{1}{x(x+1)} = \frac{1}{x}-\frac{1}{x+1}$, giving $\log|x|-\log|x+1|$. Machine-checked.
**15.** (a) — otherwise divide first to split off a polynomial part.
**16.** (a) — $\int\sinh x\,dx = \cosh x$; the minus sign belongs to $\int\sin x\,dx$.
**17.** (c) — three distinct linear factors give three partial fractions.
**18.** (b) — differentiating $\frac{a^{x}}{\log a}$ returns $a^{x}$.
:::

::: caution Distractor analysis — Anti-derivatives
**Differentiating when the question said integrate — and the reverse.** This is the
most expensive single confusion in the Calculus area, and both directions appear as
distractors. In question 18, option (c) $a^{x}\log a$ is the *derivative* of $a^{x}$
offered as its integral. In question 6, option (a) $\sec^{2}x$ is the derivative of
$\tan x$. In question 16, option (d) $\sinh x$ has done nothing at all.
Two habits fix it: (i) underline the word "integral" or "derivative" in the stem
before reading the options; (ii) **differentiate your chosen option and check it
gives back the integrand** — for a one-mark MCQ this takes ten seconds and is
completely reliable.

**$\frac{1}{a}\tan^{-1}\frac{x}{a}$ written as $\frac{1}{a}\tan^{-1}\frac{a}{x}$.**
The 2081 MCQ 8 offers exactly this as option (a). The argument of $\tan^{-1}$ must
be $\frac{x}{a}$ — the variable on top. Check it by differentiating, or by a
dimension-style argument: $\tan^{-1}$ needs a dimensionless argument that grows
with $x$, and $\frac{a}{x}$ shrinks.

**The misplaced constant in $\int\frac{dx}{9x^{2}+1}$.** The 2082 MCQ 8 offers
$\frac{1}{27}$ three times over. Do it in two clean steps. First factor:
$\frac{1}{9}\int\frac{dx}{x^{2}+\left(\frac{1}{3}\right)^{2}}$. Then apply the
formula with $a=\frac{1}{3}$: $\frac{1}{9}\times 3 = \frac{1}{3}$. The $27$ comes
from multiplying $\frac{1}{9}$ by $\frac{1}{3}$ instead of dividing.

**Integrating with respect to the wrong variable.** When the integrand contains two
letters — $\int\frac{dx}{a^{2}-x^{2}}$ — the $dx$ tells you $a$ is a constant. A
student who treats $a$ as the variable produces a logarithm of the wrong thing.
Read the differential before you start.

**Inverting the ratio in $\int\frac{dx}{x^{2}-a^{2}}$.** $\frac{x-a}{x+a}$ and
$\frac{x+a}{x-a}$ differ by a sign in the answer, because $\log\frac{1}{u} =
-\log u$. Fix the order by remembering that $\int\frac{dx}{x^{2}-a^{2}}$ has the
**minus on top** and $\int\frac{dx}{a^{2}-x^{2}}$ has the **plus on top** — the
sign pattern of the numerator copies the denominator.

**Using $\frac{1}{a}$ where $\frac{1}{2a}$ belongs.** In question 10, option (a)
$\frac{1}{3}$ is the $\tan^{-1}$ constant applied to a logarithm. The $\tan^{-1}$
family takes $\frac{1}{a}$; the logarithm family takes $\frac{1}{2a}$.
:::

## 11.14 Differential Equations

Two MCQs came from this unit in 2081 (degree, and identifying a homogeneous
equation) and two again in 2082 (homogeneous, and an integrating factor), plus one
in 2079 (integrating factor). It is the most heavily MCQ'd single unit in the
syllabus. Every one of those five items is answered by the table below without any
integration at all.

| Result | Formula / condition |
|---|---|
| Order | the order of the highest derivative present |
| Degree | the power of that highest derivative, **after** clearing radicals and fractions |
| Separable form | $\frac{dy}{dx}=f(x)g(y)$; integrate $\frac{dy}{g(y)} = f(x)dx$ |
| Homogeneous | $\frac{dy}{dx}=f\!\left(\frac{y}{x}\right)$; numerator and denominator of the same degree |
| Substitution for homogeneous | $y=vx$, so $\frac{dy}{dx}=v+x\frac{dv}{dx}$ |
| Linear standard form | $\frac{dy}{dx}+Py=Q$, with $P,Q$ functions of $x$ |
| **Integrating factor** | $\mathrm{I.F.} = e^{\int P\,dx}$ |
| Solution of a linear equation | $y\cdot\mathrm{I.F.} = \int Q\cdot\mathrm{I.F.}\,dx + C$ |
| Exact form | $M(x,y)dx+N(x,y)dy=0$ |
| Test for exactness | $\frac{\partial M}{\partial y}=\frac{\partial N}{\partial x}$ |
| $\frac{dy}{dx}=\frac{y}{x}$ | $y=cx$ |
| $x\,dy+y\,dx=0$ | $xy=c$ |
| $\frac{dy}{dx}=\frac{1+y^{2}}{1+x^{2}}$ | $\tan^{-1}y=\tan^{-1}x+c$ |
| $\frac{dy}{dx}+\frac{y}{x}=x^{2}$ | $\mathrm{I.F.}=x$ |

A **direction field** is the quickest way to see what a first-order equation is
saying: at every point it draws the slope $\frac{dy}{dx}$, and a solution curve is
any curve that follows the slopes.

```figure caption="Direction field of $\frac{dy}{dx}=x-y$ with the particular solution through $(0,0)$, namely $y=x-1+e^{-x}$, threaded through it. Every short stroke has the slope the equation demands at that point; the solution curve is tangent to every stroke it meets."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0, 3.0))
xs = np.linspace(-0.6, 3.2, 13)
ys = np.linspace(-1.4, 2.4, 11)
L = 0.24
for xv in xs:
    for yv in ys:
        s = xv - yv
        dx = L/np.sqrt(1+s*s); dy = s*dx
        ax.plot([xv-dx/2, xv+dx/2], [yv-dy/2, yv+dy/2],
                color=MUTED, lw=0.85, solid_capstyle="round")
xc = np.linspace(-0.6, 3.2, 300)
ax.plot(xc, xc - 1 + np.exp(-xc), color=ACCENT, lw=2.0, zorder=4)
ax.plot([0], [0], "o", ms=5.5, mfc="white", mec=SERIES[1], mew=1.6, zorder=5)
ax.annotate("(0, 0)", (0, 0), xytext=(-4, -22), textcoords="offset points",
            fontsize=8.4, color=SERIES[1],
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.92))
ax.annotate("y = x − 1 + e$^{-x}$", (2.55, 2.55-1+np.exp(-2.55)),
            xytext=(-100, 26), textcoords="offset points", fontsize=8.6,
            color=ACCENT, arrowprops=dict(arrowstyle="->", lw=0.9, color=ACCENT),
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.94))
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_xlim(-0.85, 3.45); ax.set_ylim(-1.75, 2.95)
ax.grid(True, lw=0.5, color=GRID)
ax.spines[['top','right']].set_visible(False)
```

**Multiple choice questions**

1. What is the degree of the ordinary differential equation $\frac{d^{3}s}{dt^{3}} = \left(4+\left(\frac{d^{2}s}{dt^{2}}\right)^{2}\right)^{1/2}$? (NEB 2081) <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $3$ (d) $4$
2. Which one of the following is an example of a homogeneous differential equation of the first order? (NEB 2081) <span class="marks">[1]</span>
   (a) $3x\,dy+2y\,dx=4$ (b) $x\,dy-y\,dx+1=0$ (c) $x\,dx+y\,dy=2$ (d) $(x^{2}+xy)dy-(xy-y^{2})dx=0$
3. Which one of the following is a homogeneous differential equation? (NEB 2082) <span class="marks">[1]</span>
   (a) $\frac{dy}{dx}=\frac{x^{2}+y^{2}}{x+y}$ (b) $\frac{dy}{dx}=\frac{x^{2}+y^{2}}{x-y}$ (c) $\frac{dy}{dx}=\frac{x^{2}+y^{2}}{x^{2}-y^{2}}$ (d) $\frac{dy}{dx}=\frac{x+y}{x^{2}+y^{2}}$
4. Which is the integrating factor of the linear differential equation $\cos^{2}x\,\frac{dy}{dx}=1-y$? (NEB 2082) <span class="marks">[1]</span>
   (a) $\tan x$ (b) $e^{\tan x}$ (c) $e^{\sec^{2}x}$ (d) $\sec^{2}x$
5. The integrating factor of the differential equation $\sin x\,\frac{dy}{dx}+y\cos x = x\sin x$ is (NEB 2079) <span class="marks">[1]</span>
   (a) $\sin x$ (b) $\cos x$ (c) $\tan x$ (d) $\cot x$
6. The order of $\frac{d^{2}y}{dx^{2}}+3\left(\frac{dy}{dx}\right)^{3}=0$ is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $3$ (d) $5$
7. The degree of $\frac{d^{2}y}{dx^{2}}+3\left(\frac{dy}{dx}\right)^{3}=0$ is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $3$ (d) $5$
8. The integrating factor of $\frac{dy}{dx}+\frac{y}{x}=x^{2}$ is <span class="marks">[1]</span>
   (a) $x$ (b) $x^{2}$ (c) $\log x$ (d) $e^{x}$
9. The integrating factor of $\frac{dy}{dx}+2y=e^{x}$ is <span class="marks">[1]</span>
   (a) $e^{x}$ (b) $e^{2x}$ (c) $2e^{x}$ (d) $e^{-2x}$
10. The equation $M\,dx+N\,dy=0$ is exact if <span class="marks">[1]</span>
    (a) $\frac{\partial M}{\partial x}=\frac{\partial N}{\partial y}$ (b) $\frac{\partial M}{\partial y}=\frac{\partial N}{\partial x}$ (c) $M=N$ (d) $\frac{\partial M}{\partial y}=-\frac{\partial N}{\partial x}$
11. The general solution of $\frac{dy}{dx}=\frac{y}{x}$ is <span class="marks">[1]</span>
    (a) $y=cx$ (b) $xy=c$ (c) $y=x+c$ (d) $y^{2}=x^{2}+c$
12. The solution of $\frac{dy}{dx}=\frac{1+y^{2}}{1+x^{2}}$ is <span class="marks">[1]</span>
    (a) $\tan^{-1}y=\tan^{-1}x+c$ (b) $\log(1+y^{2})=\log(1+x^{2})+c$ (c) $y=x+c$ (d) $\sin^{-1}y=\sin^{-1}x+c$
13. To solve a homogeneous first-order equation, the correct substitution is <span class="marks">[1]</span>
    (a) $y=vx$ (b) $y=v+x$ (c) $x=vy^{2}$ (d) $v=xy$
14. The order and degree of $\left(\frac{d^{3}y}{dx^{3}}\right)^{2}+y=0$ are respectively <span class="marks">[1]</span>
    (a) $2$ and $3$ (b) $3$ and $2$ (c) $3$ and $3$ (d) $2$ and $2$
15. The solution of $x\,dy+y\,dx=0$ is <span class="marks">[1]</span>
    (a) $x+y=c$ (b) $xy=c$ (c) $\frac{x}{y}=c$ (d) $x^{2}+y^{2}=c$
16. The integrating factor of $x\frac{dy}{dx}+2y=x^{3}$ is <span class="marks">[1]</span>
    (a) $x$ (b) $x^{2}$ (c) $x^{3}$ (d) $2x$

::: note Answer key — 11.14
**1.** (b) — square both sides to clear the radical: $\left(\frac{d^{3}s}{dt^{3}}\right)^{2}=4+\left(\frac{d^{2}s}{dt^{2}}\right)^{2}$. The highest derivative is now to the power $2$, so the degree is $2$ (the *order* is $3$).
**2.** (d) — every term of $(x^{2}+xy)$ and $(xy-y^{2})$ has total degree $2$, so the equation can be written as a function of $\frac{y}{x}$ alone. The others carry an isolated constant, which breaks homogeneity.
**3.** (c) — numerator and denominator are both of degree $2$, so replacing $x \to \lambda x$, $y \to \lambda y$ leaves the right-hand side unchanged.
**4.** (b) — divide by $\cos^{2}x$: $\frac{dy}{dx}+y\sec^{2}x=\sec^{2}x$. Then $P=\sec^{2}x$, $\int P\,dx = \tan x$ and $\mathrm{I.F.}=e^{\tan x}$. Machine-checked.
**5.** (a) — divide by $\sin x$: $\frac{dy}{dx}+y\cot x = x$. Then $\int\cot x\,dx=\log\sin x$, so $\mathrm{I.F.}=e^{\log\sin x}=\sin x$.
**6.** (b) — the highest derivative present is the second.
**7.** (a) — the *second* derivative appears to the first power; the cube is on the first derivative, which does not affect the degree.
**8.** (a) — $P=\frac{1}{x}$, $\int P\,dx=\log x$, $\mathrm{I.F.}=e^{\log x}=x$.
**9.** (b) — $P=2$, so $\mathrm{I.F.}=e^{2x}$.
**10.** (b) — both mixed partial derivatives of the same potential function must agree.
**11.** (a) — separate: $\frac{dy}{y}=\frac{dx}{x}$, so $\log y = \log x + \log c$, i.e. $y=cx$.
**12.** (a) — separate and integrate both sides directly. This was the 2080 Group B item 17a.
**13.** (a) — $y=vx$ turns a function of $\frac{y}{x}$ into a function of $v$ alone, making the equation separable.
**14.** (b) — highest derivative is the third (order $3$), raised to the power $2$ (degree $2$).
**15.** (b) — $\frac{dy}{y}=-\frac{dx}{x}$ gives $\log y + \log x = \log c$, i.e. $xy=c$.
**16.** (b) — divide by $x$ first: $\frac{dy}{dx}+\frac{2}{x}y=x^{2}$, so $P=\frac{2}{x}$, $\int P\,dx=2\log x$ and $\mathrm{I.F.}=x^{2}$. Machine-checked.
:::

::: caution Distractor analysis — Differential Equations
**Order confused with degree.** This is the real 2081 MCQ 9, and its four options
$1,2,3,4$ are chosen so that the order ($3$) and the degree ($2$) are both
available. Say the definitions out loud before answering: **order = how many times
you differentiated; degree = the power of that highest derivative, after the
equation has been cleared of radicals and fractions.** In question 1 above the
radical must be squared away *first* — a student who reads the exponent
$\frac{1}{2}$ off the right-hand side answers $1$.

**Taking the degree from the wrong derivative.** In question 7, option (c) is $3$,
the power on $\frac{dy}{dx}$. Only the power on the **highest-order** derivative
counts.

**Forgetting to divide into standard form before finding the I.F.** Both real
integrating-factor MCQs — 2079 MCQ 9 and 2082 MCQ 10 — are printed with a
coefficient in front of $\frac{dy}{dx}$. You must divide it out first. In the 2082
item, the un-divided equation suggests $\sec^{2}x$ (option (d)); dividing properly
gives $P=\sec^{2}x$ and then $\mathrm{I.F.}=e^{\tan x}$, option (b). Note the
sequence: **divide, identify $P$, integrate $P$, then exponentiate.** Option (c)
$e^{\sec^{2}x}$ skips the integration step.

**Calling an equation homogeneous because it merely looks symmetric.** In the 2082
MCQ 9, options (a) and (b) have a degree-$2$ numerator over a degree-$1$
denominator, so the right-hand side is *not* a function of $\frac{y}{x}$ alone. Test
it mechanically: replace $x$ by $\lambda x$ and $y$ by $\lambda y$; if every
$\lambda$ cancels, it is homogeneous. A lone constant term, as in the 2081 options
(a), (b) and (c), always kills homogeneity.

**Integrating instead of exponentiating.** Option (a) $\tan x$ in the 2082 item is
$\int P\,dx$ — one step short of the integrating factor, which is
$e^{\int P\,dx}$.
:::

## 11.15 Computational Methods

Exactly one MCQ comes from this area every year, and it has been at Q10 or Q11 in
all four verified papers. Three of those four were a **Gauss elimination** step:
you are shown two equations and asked what the elimination produces. Nothing is
being tested except arithmetic discipline, so this is a mark you should never drop.

::: note An anomaly worth knowing about
The 2079 and 2080 papers carry an economics / input–output ("Leontief") alternative
at Q11 and Q19 — demand-and-supply equilibrium and inter-industry output — which is
**not in the published CDC curriculum for Grade 12 Mathematics**. The 2080 version
asks for the equilibrium of a demand and supply pair and reduces to
$y^{2}+4y-44=0$. It has not reappeared in 2081 or 2082 and the specification grid
has no room for it. Read this paragraph, recognise the format if it appears, and
spend no more time on it: build your preparation on linear programming, Gauss
elimination, Gauss–Seidel and the simplex method, which are all in the curriculum.
:::

| Method | Key point |
|---|---|
| Gauss elimination | reduce the augmented matrix to **upper triangular**, then back-substitute |
| Elementary row operations | swap two rows; multiply a row by $k\ne0$; add a multiple of one row to another |
| Gauss–Jordan | continue to the **identity** matrix on the left, reading the solution off directly |
| Gauss–Seidel | iterative: use each new value immediately inside the same sweep |
| Convergence of Gauss–Seidel | guaranteed if the system is **diagonally dominant** |
| Unique solution | $\mathrm{rank}(A)=\mathrm{rank}(A\mid B)=n$ |
| Infinitely many solutions | $\mathrm{rank}(A)=\mathrm{rank}(A\mid B)<n$ |
| No solution (inconsistent) | $\mathrm{rank}(A)\ne\mathrm{rank}(A\mid B)$; a row reads $0=k$, $k\ne0$ |
| LP feasible region | the intersection of all the constraint half-planes |
| LP optimum | occurs at a **vertex** of the feasible region |
| Simplex: slack variable | converts $\leq$ into $=$; $\;3x+2y\leq12 \Rightarrow 3x+2y+s=12$ |
| Simplex: pivot column | the most negative entry of the objective (bottom) row |
| Simplex: pivot row | the smallest non-negative ratio $\dfrac{\text{RHS}}{\text{pivot-column entry}}$ |
| Simplex: stop when | no negative entries remain in the bottom row |

**Multiple choice questions**

1. In solving the system $x+3y=5$, $2x-y=3$ by Gauss elimination, the operation $R_2 \to 2R_1-R_2$ gives (NEB 2080) <span class="marks">[1]</span>
   (a) $5y=5$ (b) $7y=13$ (c) $7y=7$ (d) $y=7$
2. In solving $x+3y=7$, $2x-4y=4$ by Gauss elimination, the operation $R_2 \to 2R_1-R_2$ gives (NEB 2082) <span class="marks">[1]</span>
   (a) $10y=10$ (b) $10y=18$ (c) $2y=10$ (d) $-10y=10$
3. If in the row-echelon form of an augmented matrix the rank of the coefficient matrix equals the rank of the augmented matrix but is **less than** the number of unknowns, the system is (NEB 2079) <span class="marks">[1]</span>
   (a) inconsistent (b) consistent with a unique solution (c) inconsistent with infinitely many solutions (d) consistent with infinitely many solutions
4. Which elementary row operation is **not** permitted on an augmented matrix? (NEB 2081) <span class="marks">[1]</span>
   (a) interchanging two rows (b) adding a multiple of one row to another (c) multiplying a row by $0$ (d) multiplying a row by $-3$
5. Solving $2x+3y=8$, $x-y=-1$ by Gauss elimination, the operation $R_2 \to 2R_2-R_1$ gives <span class="marks">[1]</span>
   (a) $-5y=-10$ (b) $5y=10$ (c) $-5y=10$ (d) $y=-10$
6. The solution of the system in question 5 is <span class="marks">[1]</span>
   (a) $x=1,\;y=2$ (b) $x=2,\;y=1$ (c) $x=-1,\;y=2$ (d) $x=1,\;y=-2$
7. A system of linear equations is inconsistent when a row of the reduced augmented matrix reads <span class="marks">[1]</span>
   (a) $0\;\;0\;\mid\;0$ (b) $0\;\;0\;\mid\;5$ (c) $1\;\;0\;\mid\;0$ (d) $0\;\;1\;\mid\;3$
8. The Gauss–Seidel method is certain to converge if the coefficient matrix is <span class="marks">[1]</span>
   (a) symmetric (b) singular (c) diagonally dominant (d) triangular
9. In the Gauss–Jordan method the left block of the augmented matrix is reduced to <span class="marks">[1]</span>
   (a) an upper triangular matrix (b) the identity matrix (c) a diagonal matrix with zero entries (d) a null matrix
10. Introducing a slack variable turns the constraint $3x+2y\leq12$ into <span class="marks">[1]</span>
    (a) $3x+2y-s=12$ (b) $3x+2y+s=12$ (c) $3x+2y+s\leq12$ (d) $3x+2y=12-s^{2}$
11. In the simplex method, the entering variable is chosen from the column with <span class="marks">[1]</span>
    (a) the largest positive entry in the objective row (b) the most negative entry in the objective row (c) the largest right-hand side (d) the smallest ratio
12. The maximum value of a linear objective function over a bounded feasible region occurs <span class="marks">[1]</span>
    (a) at the centre of the region (b) at a vertex of the region (c) anywhere inside the region (d) only on the $x$-axis

::: note Answer key — 11.15
**1.** (c) — $2R_1 = 2x+6y=10$; subtracting $R_2 = 2x-y=3$ gives $7y=7$, so $y=1$ and then $x=2$. Machine-checked.
**2.** (a) — $2R_1 = 2x+6y=14$; subtracting $R_2 = 2x-4y=4$ gives $10y=10$, so $y=1$ and $x=4$. Machine-checked.
**3.** (d) — equal ranks means consistent; rank below the number of unknowns leaves a free variable, hence infinitely many solutions. Option (c) is self-contradictory and is the trap.
**4.** (c) — multiplying a row by $0$ destroys information and is not reversible; the scalar must be non-zero.
**5.** (a) — $2R_2 = 2x-2y=-2$; subtracting $R_1 = 2x+3y=8$ gives $-5y=-10$.
**6.** (a) — from $-5y=-10$, $y=2$, then $x-2=-1$ gives $x=1$. Machine-checked.
**7.** (b) — that row says $0=5$, which is impossible, so no solution exists.
**8.** (c) — diagonal dominance, $|a_{ii}| > \sum_{j\ne i}|a_{ij}|$ in every row, is the standard sufficient condition.
**9.** (b) — Gauss elimination stops at upper triangular; Gauss–Jordan goes all the way to $I$.
**10.** (b) — a slack variable absorbs the unused capacity and is itself $\ge 0$, turning the inequality into an equation.
**11.** (b) — the most negative objective-row entry marks the variable whose increase improves the objective fastest.
**12.** (b) — a linear function on a convex polygon attains its extremes at corner points.
:::

::: caution Distractor analysis — Computational Methods
**Subtracting in the wrong direction.** In both real elimination MCQs an option
carries the correct coefficient with the wrong sign — question 2's option (d) is
$-10y=10$. Write the operation on the paper exactly as the question states it
($R_2 \to 2R_1-R_2$ means *first row doubled minus second row*, not the reverse) and
do the constants in the same order as the coefficients.

**Doubling the coefficients but forgetting the constant.** Option (b) $10y=18$ in
question 2 comes from doubling only the left side of $R_1$. The row operation acts
on the **whole row of the augmented matrix**, constant column included. This is why
§11.5's augmented-matrix figure keeps the constants inside the bracket.

**"Inconsistent with infinitely many solutions."** The 2079 option (c) is a
sentence that cannot be true: inconsistent means *no* solution. Read all four
options before choosing; the examiner is testing whether you know the vocabulary,
not the arithmetic.

**Confusing the pivot column rule with the pivot row rule.** Question 11's option
(d) "the smallest ratio" is the rule for the **departing** variable (the pivot row),
not the entering one. Column first by the most negative objective entry, then row by
the smallest non-negative ratio.

**Treating rank alone as decisive.** Rank of the coefficient matrix on its own tells
you nothing: it must be compared with the rank of the *augmented* matrix, and then
both with $n$. Three quantities, two comparisons.
:::

## 11.16 Mechanics (alternative to Unit 15)

If your school teaches Mechanics instead of Computational Methods, this section
replaces §11.15 — you answer the "Or" at Q11 and again at Q19, not both. The MCQ has
been a **projectile** item in 2081 and 2082, a **weight** item in 2080 and a
**momentum** item in 2079. The projectile formulae below answer the first two in
about twenty seconds each.

| Quantity | Formula (launch speed $u$, angle $\theta$, gravity $g$) |
|---|---|
| Horizontal component | $u\cos\theta$, constant throughout |
| Vertical component | $u\sin\theta-gt$ |
| **Time to greatest height** | $t=\dfrac{u\sin\theta}{g}$ |
| **Time of flight** | $T=\dfrac{2u\sin\theta}{g}$ |
| **Greatest height** | $H=\dfrac{u^{2}\sin^{2}\theta}{2g}$ |
| **Horizontal range** | $R=\dfrac{u^{2}\sin 2\theta}{g}$ |
| Maximum range | $R_{\max}=\dfrac{u^{2}}{g}$, at $\theta=45^\circ$ |
| Equation of the path | $y=x\tan\theta-\dfrac{gx^{2}}{2u^{2}\cos^{2}\theta}$ (a parabola) |
| Weight of mass $m$ | $W=mg$ newtons |
| Newton's second law | $F=ma$ |
| Momentum | $p=mv$; change of momentum $=mv-mu$ |
| Impulse | $Ft = mv-mu$ |
| Triangle law of forces | three forces in equilibrium form a closed triangle taken in order |
| **Lami's theorem** | $\dfrac{P}{\sin\alpha}=\dfrac{Q}{\sin\beta}=\dfrac{R}{\sin\gamma}$ |
| Resultant of $P,Q$ at angle $\theta$ | $\sqrt{P^{2}+Q^{2}+2PQ\cos\theta}$ |
| Two like parallel forces | resultant $X+Y$, dividing $AB$ internally in the ratio $Y:X$ |

```figure caption="Projectile path for $u = 20\ \mathrm{m\,s^{-1}}$ at $\theta = 30^\circ$ with $g = 10\ \mathrm{m\,s^{-2}}$: greatest height $H = 5$ m reached at $t = 1$ s, range $R = 20\sqrt{3} \approx 34.6$ m, total time of flight $T = 2$ s. The velocity at the top is horizontal and equal to $u\cos\theta$. The vertical scale is exaggerated so that $H$ is visible; the launch arrow shows the true initial direction in the plotted coordinates."
import numpy as np
u, th, g = 20.0, np.radians(30.0), 10.0
T = 2*u*np.sin(th)/g
R = u**2*np.sin(2*th)/g
H = u**2*np.sin(th)**2/(2*g)
t = np.linspace(0, T, 300)
X = u*np.cos(th)*t
Y = u*np.sin(th)*t - 0.5*g*t**2
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.plot(X, Y, color=ACCENT, lw=2.0, zorder=3)
ax.plot([0, R], [0, 0], color=INK, lw=1.1)
# launch velocity arrow
ax.annotate("", (6.0, 6.0*np.tan(th)), (0, 0),
            arrowprops=dict(arrowstyle="->", lw=1.6, color=SERIES[2]))
ax.text(4.2, 1.2, "u = 20", fontsize=8.6, color=SERIES[2])
ax.text(1.4, 0.35, "θ = 30°", fontsize=8.4, color=MUTED)
# apex
ax.plot([R/2, R/2], [0, H], ls="--", lw=1.0, color=SERIES[1])
ax.plot([R/2], [H], "o", ms=5.0, color=SERIES[1], zorder=5)
ax.annotate("H = 5 m", (R/2, H/2), xytext=(8, -4), textcoords="offset points",
            fontsize=8.6, color=SERIES[1])
ax.annotate("", (R/2+5.5, H), (R/2, H),
            arrowprops=dict(arrowstyle="->", lw=1.4, color=SERIES[4]))
ax.text(R/2+1.0, H+0.55, "u cos θ at the top", fontsize=8.4, color=SERIES[4])
# range bracket
ax.annotate("", (0, -1.5), (R, -1.5),
            arrowprops=dict(arrowstyle="<->", lw=1.1, color=MUTED))
ax.text(R/2, -2.4, "R = 20√3 ≈ 34.6 m   (T = 2 s)", fontsize=8.6,
        color=MUTED, ha="center")
ax.set_xlim(-3.0, R+7.0); ax.set_ylim(-3.6, H+3.0)
ax.set_xlabel("horizontal distance (m)")
ax.set_ylabel("height (m)")
ax.grid(True, lw=0.5, color=GRID)
ax.spines[['top','right','bottom']].set_visible(False)
```

**Multiple choice questions**

1. What is the greatest height attained by a projectile whose initial velocity and angle of elevation are $160\ \mathrm{ms^{-1}}$ and $30^\circ$ respectively? ($g=10\ \mathrm{ms^{-2}}$) (NEB 2081) <span class="marks">[1]</span>
   (a) $203$ m (b) $230$ m (c) $320$ m (d) $640$ m
2. What is the maximum height attained by a particle in projectile motion if the initial velocity and angle of inclination are $40\ \mathrm{m/s}$ and $30^\circ$? ($g=10\ \mathrm{ms^{-2}}$) (NEB 2082) <span class="marks">[1]</span>
   (a) $20$ m (b) $40$ m (c) $80$ m (d) $160$ m
3. What is the amount of gravity exerted by the earth on a mass of $100$ kg? ($g$ is the acceleration due to gravity) (NEB 2080) <span class="marks">[1]</span>
   (a) $100$ newtons (b) $100g$ newtons (c) $\frac{g}{100}$ newtons (d) $\frac{100}{g}$ newtons
4. A force acts on a body of mass $m$ for a time $t$ and changes its velocity from $u$ to $v$. The change in momentum of the body in time $t$ is (NEB 2079) <span class="marks">[1]</span>
   (a) $\frac{mu-mv}{t}$ (b) $\frac{mv-mu}{t}$ (c) $\frac{tm-tv}{uv}$ (d) $\frac{u-v}{mt}$
5. The time of flight of the projectile of question 2 is <span class="marks">[1]</span>
   (a) $2$ s (b) $4$ s (c) $8$ s (d) $\frac{1}{2}$ s
6. A projectile is fired with speed $u$. Its horizontal range is greatest when the angle of projection is <span class="marks">[1]</span>
   (a) $30^\circ$ (b) $45^\circ$ (c) $60^\circ$ (d) $90^\circ$
7. At the highest point of its path the velocity of a projectile is <span class="marks">[1]</span>
   (a) zero (b) $u\sin\theta$ (c) $u\cos\theta$, horizontal (d) $u$, along the tangent
8. The path of a projectile under uniform gravity, with air resistance neglected, is <span class="marks">[1]</span>
   (a) a straight line (b) a circle (c) a parabola (d) an ellipse
9. Three forces $P$, $Q$, $R$ acting at a point are in equilibrium, with $\alpha$, $\beta$, $\gamma$ the angles opposite to them. Lami's theorem states <span class="marks">[1]</span>
   (a) $\frac{P}{\sin\alpha}=\frac{Q}{\sin\beta}=\frac{R}{\sin\gamma}$ (b) $P\sin\alpha=Q\sin\beta=R\sin\gamma$ (c) $\frac{P}{\cos\alpha}=\frac{Q}{\cos\beta}=\frac{R}{\cos\gamma}$ (d) $P+Q+R=0$
10. The resultant of two like parallel forces $X$ and $Y$ acting at $A$ and $B$ divides $AB$ internally in the ratio <span class="marks">[1]</span>
    (a) $X:Y$ (b) $Y:X$ (c) $X^{2}:Y^{2}$ (d) $1:1$

::: note Answer key — 11.16
**1.** (c) — $H=\frac{u^{2}\sin^{2}\theta}{2g}=\frac{160^{2}\times(1/2)^{2}}{2\times10}=\frac{25600\times0.25}{20}=320$ m. Machine-checked.
**2.** (a) — $H=\frac{40^{2}\times 0.25}{20}=\frac{400}{20}=20$ m. Machine-checked.
**3.** (b) — the gravitational force on a mass is its weight $W=mg=100g$ newtons. Option (a) drops $g$ and is the commonest answer given.
**4.** (b) — as printed. Strictly, the change of momentum is $mv-mu$ and $\frac{mv-mu}{t}$ is the average **force**; every printed option divides by $t$, so (b) is the only defensible choice. Flagged as a printing fault, not a mathematical result.
**5.** (b) — $T=\frac{2u\sin\theta}{g}=\frac{2\times40\times\frac12}{10}=\frac{40}{10}=4$ s. Note that $T$ is twice the time to the top, and that it does not depend on the horizontal component at all. Machine-checked.
**6.** (b) — $R=\frac{u^{2}\sin2\theta}{g}$ is largest when $\sin2\theta=1$, i.e. $2\theta=90^\circ$.
**7.** (c) — the vertical component has been reduced to zero; the horizontal component $u\cos\theta$ is unchanged throughout.
**8.** (c) — eliminating $t$ from $x=u\cos\theta\,t$ and $y=u\sin\theta\,t-\frac{1}{2}gt^{2}$ gives a quadratic in $x$.
**9.** (a) — each force is proportional to the sine of the angle between the other two.
**10.** (b) — the resultant is nearer the larger force, so the ratio of the segments is the **reciprocal** of the ratio of the forces.
:::

::: caution Distractor analysis — Mechanics
**Time of flight halved.** Question 5's option (a), $2$ s, is
$\frac{u\sin\theta}{g}$ — the time to the **greatest height**, which is half the
time of flight. The 2082 stem gives you the same $u$ and $\theta$ as the height
question above it, so the two are easy to answer in one breath and equally easy to
mix up: $t_{\text{top}}=\frac{u\sin\theta}{g}=2$ s, $T=4$ s.

**Halving in the wrong place.** In the 2081 item, $u^{2}=25600$ and
$\sin^{2}30^\circ=\frac14$; option (d) $640$ m is what you get from
$\frac{u^{2}\sin^{2}\theta}{g}$, forgetting the $2$ in the denominator, and option
(a) $203$ m is a decimal-slip distractor. Write $H=\frac{u^{2}\sin^{2}\theta}{2g}$
out fully before substituting.

**Squaring the sine, or not.** In the 2082 item, option (b) $40$ m is
$\frac{u^{2}\sin\theta}{2g}$ — the sine used un-squared. $H$ carries
$\sin^{2}\theta$; $R$ carries $\sin 2\theta$. These are different functions and the
options are built to punish swapping them: $\sin^{2}30^\circ=0.25$ but
$\sin 60^\circ\approx0.866$.

**Dropping $g$ from a weight.** The 2080 item's option (a), "$100$ newtons", treats
kilograms as newtons. Mass is in kilograms; weight is the force $mg$ in newtons. The
examiner left $g$ symbolic precisely so that you could not hide behind a number.

**Force confused with change of momentum.** The 2079 item's printed options all
divide by $t$, which makes them all forces. Impulse $=Ft=mv-mu$ is the change of
momentum; $\frac{mv-mu}{t}$ is the average force. Know both relations and you can
still pick the intended option, (b), while recognising that the question stem does
not match its options.

**Force ratio read the right way round.** In question 10, the resultant of two like
parallel forces sits **closer to the bigger force**, so $AP:PB = Y:X$, the inverse of
the force ratio. Test it with $X=3$, $Y=1$: the resultant should be a quarter of the
way from $A$, and $Y:X=1:3$ gives exactly that.
:::

## 11.17 Appendix: Retained Examinable Topics

A few topics sit outside the fifteen numbered units of the Grade 12 spine but have
still appeared as Group A questions. They are collected here so that you can see
**exactly how much time each deserves**, rather than guessing.

**Group Theory.** An MCQ in 2079 (recognising an abelian group) and again in 2080
(naming the associative law for a binary operation) — and then **absent from both
2081 and 2082**. The 2078 specification grid has no line for it. Treat it as a
fifteen-minute revision: learn the four group axioms and the word "abelian", and
move on. Do not learn subgroups, cosets or cyclic groups for this paper.

**Rolle's theorem and the Mean Value Theorem.** Appeared in **2080 only**, and not in
2079, 2081 or 2082. Learn the two statements and the difference between them —
that is the whole examinable surface.

**Numerical integration (trapezoidal and Simpson's rules).** Not seen as an MCQ in
any of the four verified years, but the formulae are short and they occasionally
appear inside a Group B part. Ten minutes.

**Sum and product of the roots of a quadratic.** A Grade 11 result, but it was
MCQ 2 in 2080. It costs one line to remember.

| Result | Statement |
|---|---|
| Group $(G,*)$ | closure, associativity, identity, inverse |
| Abelian group | additionally $a*b=b*a$ for all $a,b\in G$ |
| Associative law | $(a*b)*c = a*(b*c)$ |
| $(\mathbb{Z},+)$, $(\mathbb{Q}-\{0\},\times)$ | standard abelian groups |
| $(\mathbb{N},+)$ | **not** a group — no identity, no inverses |
| Rolle's theorem | $f$ continuous on $[a,b]$, differentiable on $(a,b)$, $f(a)=f(b)\Rightarrow f'(c)=0$ for some $c$ |
| Mean value theorem | same hypotheses without $f(a)=f(b)$: $f'(c)=\dfrac{f(b)-f(a)}{b-a}$ |
| Trapezoidal rule | $\dfrac{h}{2}\left[y_0+2(y_1+\dots+y_{n-1})+y_n\right]$ |
| Simpson's $\frac{1}{3}$ rule | $\dfrac{h}{3}\left[y_0+4(y_1+y_3+\dots)+2(y_2+y_4+\dots)+y_n\right]$ |
| Simpson's rule needs | an **even** number of sub-intervals |
| Sum of the roots of $ax^{2}+bx+c=0$ | $-\dfrac{b}{a}$ |
| Product of the roots | $\dfrac{c}{a}$ |

**Multiple choice questions**

1. Which of the following is an abelian group under the given operation? (NEB 2079) <span class="marks">[1]</span>
   (a) the set of integers under addition (b) the set of natural numbers under addition (c) the set of integers under multiplication (d) the set of all real numbers under multiplication
2. If $*$ is a binary operation on a set $G$ and $(a*b)*c = a*(b*c)$ for all $a,b,c\in G$, then $*$ satisfies the (NEB 2080) <span class="marks">[1]</span>
   (a) closure law (b) commutative law (c) identity law (d) associative law
3. The sum of the roots of the equation $x^{2}-6x+8=0$ is (NEB 2080) <span class="marks">[1]</span>
   (a) $2$ (b) $4$ (c) $6$ (d) $8$
4. If $f(x)=x^{2}-4x+3$ on $[1,3]$, the value of $c$ given by Rolle's theorem is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $3$ (d) $\frac{3}{2}$
5. Rolle's theorem requires, in addition to continuity and differentiability, that <span class="marks">[1]</span>
   (a) $f(a)=f(b)$ (b) $f(a)=0$ (c) $f'(a)=f'(b)$ (d) $f$ be increasing
6. For $f(x)=x^{2}$ on $[1,3]$, the value of $c$ given by the mean value theorem is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $\sqrt{3}$ (d) $\frac{5}{2}$
7. Simpson's $\frac{1}{3}$ rule can be applied only when the number of sub-intervals is <span class="marks">[1]</span>
   (a) odd (b) even (c) prime (d) a multiple of $3$
8. Using the trapezoidal rule with $n=2$, the value of $\int_{0}^{1}x^{2}\,dx$ is <span class="marks">[1]</span>
   (a) $\frac{1}{3}$ (b) $\frac{3}{8}$ (c) $\frac{1}{2}$ (d) $\frac{1}{4}$

::: note Answer key — 11.17
**1.** (a) — $(\mathbb{Z},+)$ has closure, associativity, identity $0$, inverse $-a$ and commutativity. $(\mathbb{N},+)$ has no identity or inverses; $(\mathbb{Z},\times)$ has no inverses; $\mathbb{R}$ under multiplication fails because $0$ has no inverse.
**2.** (d) — the bracket can be moved without changing the result; that is precisely associativity.
**3.** (c) — sum of the roots $=-\frac{b}{a}=-\frac{-6}{1}=6$. The roots are $2$ and $4$; option (a) and (b) are the roots themselves and (d) is their product. Machine-checked.
**4.** (b) — $f(1)=f(3)=0$, and $f'(x)=2x-4=0$ gives $c=2$, which lies in $(1,3)$. Machine-checked.
**5.** (a) — equal endpoint values are what force a horizontal tangent somewhere in between.
**6.** (b) — $\frac{f(3)-f(1)}{3-1}=\frac{9-1}{2}=4$, and $f'(c)=2c=4$ gives $c=2$. Machine-checked.
**7.** (b) — the rule pairs the sub-intervals, fitting one parabola across each pair, so their number must be even.
**8.** (b) — $h=\frac12$; $\frac{h}{2}[y_0+2y_1+y_2]=\frac14\left[0+2\times\frac14+1\right]=\frac{3}{8}$. The exact value is $\frac13$, so the trapezoidal rule over-estimates here — as it always does for a convex curve. Machine-checked.
:::

::: caution Distractor analysis — retained topics
**Answering with a root instead of the sum.** In the real 2080 item the roots of
$x^{2}-6x+8=0$ are $2$ and $4$, and both appear as options, as does the product
$8$. Use $-\frac{b}{a}$ and $\frac{c}{a}$ directly; do not solve the quadratic at all
— solving is what makes you reach for the wrong number.

**Sign lost from $-\frac{b}{a}$.** The sum of the roots is $-\frac{b}{a}$, not
$\frac{b}{a}$. With $b=-6$ the two differ only in sign, and in a paper where the
answer happens to be positive the mistake goes unnoticed until the year it does not.

**Confusing the group axioms by name.** The 2080 item prints all four axiom names as
options. Memorise them as a sentence: **closure** keeps you in the set,
**associativity** moves the brackets, **identity** does nothing, **inverse** undoes.
Commutativity is the *extra* one that makes a group abelian — it is not one of the
four.

**Calling $(\mathbb{N},+)$ a group.** It is closed and associative but has no
identity element ($0\notin\mathbb{N}$) and no inverses. This is option (b) in the
2079 item and it is the one most often chosen.

**Rolle answered with an endpoint.** In question 4, options (a) and (c) are $a$ and
$b$ themselves. Rolle's theorem promises a $c$ **strictly inside** $(a,b)$; an
endpoint can never be the answer.

**Trapezoidal answer replaced by the exact value.** In question 8, option (a)
$\frac13$ is $\int_0^1 x^2dx$ done exactly. The question asks what the *rule*
produces, which is deliberately not the exact value — that gap is the whole point of
an error estimate.
:::

## Chapter summary

- **Group A is eleven marks in fifteen minutes**, and since 2082 it arrives as a separate booklet thirty minutes after the paper starts. Do the eleven MCQs first, in one pass, and hand the booklet back before you settle into Group B.
- **Four of the eleven MCQs are Calculus** — the single largest block. Across 2079–2082 the reliable slots have been a derivative (often an inverse hyperbolic or inverse trigonometric one), a standard integral of the $\frac{1}{a}\tan^{-1}\frac{x}{a}$ family, and one or two differential-equation items on order/degree, homogeneity or the integrating factor.
- **One MCQ is guaranteed from each of Trigonometry, Analytic Geometry and Vector** by the grid's own footnote. In practice that has meant a half-angle or triangle law, a conic property (eccentricity, latus rectum or a tangency condition), and a dot- or cross-product item.
- **One MCQ is guaranteed from Computational Methods or Mechanics**, and three of the four verified years made it a Gauss-elimination row-operation step; the Mechanics alternative has twice been the greatest height of a projectile. Both are pure substitution.
- **The Statistics and Probability MCQ has gone to Probability every single year**, never to correlation or regression, and **conditional probability has appeared in 2080, 2081, 2082 and the CDC model**. $P(B/A)=\frac{P(A\cap B)}{P(A)}$ — divide by the event that has already happened.
- **Exactly two "Or" choices appear per paper, at Q11 and Q19, never in Group C.** Decide in advance which branch you are taking so that you do not spend reading time on both.
- **The traps that cost the most marks** are, in order of how often they are printed: differentiating when asked to integrate; the $\hat{j}$ sign and the non-commutativity of $\vec{a}\times\vec{b}$; $\frac{1}{a}\tan^{-1}\frac{a}{x}$ written for $\frac{1}{a}\tan^{-1}\frac{x}{a}$, and the constant misplaced in $\int\frac{dx}{9x^{2}+1}$; dividing by $P(B)$ instead of $P(A)$ in a conditional probability; degree read as order; $C(n,r)\times r! = P(n,r)$ read backwards; and $c^{2}=a^{2}(1+m^{2})$ with $a$ and $c$ swapped.
- **Binomial Theorem and Solution of Triangles have never carried an MCQ** in the four verified years, and **Group Theory vanished after 2080** while **Rolle/MVT appeared in 2080 only**. Prepare them for Groups B and C, not for Group A.
- **Every numerical answer key in this chapter was recomputed** with a computer algebra system before it was printed, including the option sets of the real past papers — where three genuine printing faults were found and are flagged in place.

::: tip How to attack Group A in fifteen minutes
**Minutes 0–1: sort, do not solve.** Read all eleven stems once and mark each one
*recall*, *one-line*, or *work*. Roughly half of any NEB Group A is pure recall —
order and degree, a group axiom, Lami's theorem, the exactness condition, the pivot
rule.

**Minutes 1–6: clear every recall item.** Answer them straight off the fact tables in
this chapter. Do not check them twice; you either know a definition or you do not.

**Minutes 6–12: the one-line items.** These are the substitution questions — greatest
height, an integrating factor, a conditional probability, a row operation, an
eccentricity. Write the formula down **before** you write any number. Nearly every
distractor in this book is generated by substituting into a half-remembered formula,
so the formula on the page is your defence.

**Minutes 12–15: the work items and a sweep.** Usually one or two: a determinant, a
cross product, a definite integral. Then sweep the whole sheet and confirm you have
shaded exactly eleven bubbles.

**Three habits worth more than any formula.** (i) *Read the operator.* "Find
$\int$…" versus "find $\frac{d}{dx}$…" and "$\hat{k}\times\hat{j}$" versus
"$\hat{j}\times\hat{k}$" change the sign or invert the whole answer. (ii) *Check the
variable.* Differentiate with respect to whatever the question names, not whatever
letter is most prominent. (iii) *Never leave a blank.* There is no negative marking;
eliminate the two options that are dimensionally or structurally impossible and
choose between the rest.
:::
